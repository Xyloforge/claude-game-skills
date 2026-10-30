"""Measure a UI frame (panel, button, bar) for slicing, including ornaments that sit anywhere along its edges.

Usage:
  python3 slice_frame.py <frame.png> <out.json> [--preview sizes.png] [--sizes 0.6x0.6,1.6x1,2.6x1.6]
          [--fixed top=120-180,left=40-70] [--pixel]

<frame.png> is one cut frame on a transparent background (from cut_sheet.py). The script writes a slice layout:
- insets l, t, r, b: the corners, as deep as the deepest corner or edge ornament so nothing is cut through;
- fixed spans per edge: places that break the edge's usual look (a gem, a crest, a skull): deeper, sticking out, or
  a different colour from the edge's repeating pattern. They are drawn at their own size; only the spans between
  them grow;
- a repeat period per edge: when an edge carries a pattern (rivets, vines, stitching) the growing spans are tiled by
  whole periods instead of stretched; 0 means a plain edge, which is stretched;
- the centre mode: "tile" for a textured fill, "stretch" for a flat one.
An ornament the detection misses (one close to the edge's own colours) can be named with --fixed (pixel spans along
that edge of the source image). Always look at --preview: it draws the frame at several sizes with
the same layout as the renderer in ui-frames.md. A smeared or repeated ornament there means a missed fixed span.
--pixel: whole-number corner scaling and nearest-neighbour sampling, for pixel art.
Needs Pillow and NumPy.
"""
import argparse
import json

import numpy as np
from PIL import Image, ImageDraw

EDGES = ("top", "bottom", "left", "right")


def edge_view(arr, edge):
    """The array turned so `edge` is the top row, positions along it in source order (x for top/bottom, y for sides)."""
    if edge == "top":
        return arr
    if edge == "bottom":
        return arr[::-1]
    t = arr.transpose(1, 0, *range(2, arr.ndim))
    return t if edge == "left" else t[::-1]


def inside_mask(a):
    """Pixels that look like the panel's fill (or transparent, for a hollow frame)."""
    h, w = a.shape[:2]
    patch = a[h * 2 // 5:h * 3 // 5 + 1, w * 2 // 5:w * 3 // 5 + 1].reshape(-1, 4)
    ref = np.median(patch, axis=0)
    if ref[3] < 24:
        return a[..., 3] < 24, "stretch"
    spread = np.abs(patch[:, :3] - ref[:3]).sum(-1)
    tol = max(48.0, float(np.percentile(spread, 95)) * 1.3)
    inside = (np.abs(a[..., :3] - ref[:3]).sum(-1) < tol) & (a[..., 3] > 200)
    return inside, "tile" if np.percentile(spread, 90) > 24 else "stretch"


def profile(alpha, inside):
    """Per position along the top edge: first solid row (outer) and first fill row after it (inner)."""
    h = max(1, alpha.shape[0] // 2)
    solid, ins = alpha[:h] > 24, inside[:h]
    outer = np.where(solid.any(0), solid.argmax(0), h)
    after = ins & (np.arange(h)[:, None] > outer[None, :])
    inner = np.where(after.any(0), after.argmax(0), h)
    return outer, inner


def runs(mask, gap=3, min_len=3):
    out = []
    for i in np.flatnonzero(mask):
        if out and i - out[-1][1] <= gap:
            out[-1][1] = i + 1
        else:
            out.append([int(i), int(i) + 1])
    return [r for r in out if r[1] - r[0] >= min_len]


def band_sig(rgba, depth):
    """Per position along the top edge: the mean colour of the border band, weighted by alpha."""
    band = rgba[:max(1, depth)]
    return (band[..., :3] * (band[..., 3:] / 255.0)).mean(0)


def autocorr_period(sig):
    """(lag, strength) of the clearest repeat in a band signature; lag 0 when it is plain or does not repeat."""
    n = len(sig)
    if n < 12 or np.abs(sig - sig.mean(0)).sum(-1).mean() < 4:
        return 0, 0.0
    x = np.diff(sig, axis=0)  # changes, not levels: a smooth blob (a gem, a shaded corner) must not look periodic
    x = x - x.mean(0)
    n -= 1
    r = {}
    for p in range(3, n // 2):
        a, b = x[:-p], x[p:]
        r[p] = float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum() + 1e-9))
    best = max(r.values())
    if best < 0.5:
        return 0, best
    peaks = [p for p, v in r.items() if v >= 0.85 * best and v >= r.get(p - 1, -1) and v >= r.get(p + 1, -1)]
    return min(peaks), best


def find_period(sig):
    """Repeat length of an edge pattern, or 0. Several windows are tried, because a big ornament inside one window
    swamps the pattern there; the window with the clearest repeat wins."""
    n = len(sig)
    cuts = [(0, n)] + [(round(n * a), round(n * b)) for a, b in ((0.15, 0.4), (0.38, 0.62), (0.6, 0.85))]
    found = [autocorr_period(sig[a:b]) for a, b in cuts]
    p, strength = max(found, key=lambda f: f[1] if f[0] else -1)
    return p


def odd_positions(sig, p):
    """Positions whose colour breaks the edge's usual look (its repeating pattern, or its plain colour)."""
    n = len(sig)
    mid = np.arange(n // 4, max(n // 4 + 1, 3 * n // 4))
    if p:
        expect = np.array([np.median(sig[mid[mid % p == ph]], 0) for ph in range(p)])
        dist = np.min([np.abs(sig - expect[(np.arange(n) + s) % p]).sum(-1) for s in (-1, 0, 1)], 0)
    else:
        dist = np.abs(sig - np.median(sig[mid], 0)).sum(-1)
    thr = max(20.0, 3 * float(np.median(dist[mid])))
    # Grow each clear hit over its faint neighbours, so the thin tips of a round gem stay with it.
    strong, weak = dist > thr, dist > max(8.0, thr * 0.35)
    out = np.zeros(n, bool)
    for a, b in runs(weak, gap=0, min_len=1):
        if strong[a:b].any():
            out[a:b] = True
    return out


def period(rgba, span, depth):
    a, b = span
    return find_period(band_sig(rgba[:, a:b], depth)) if b - a >= 12 and depth >= 1 else 0


def parse_fixed(text):
    out = {e: [] for e in EDGES}
    for item in filter(None, (text or "").split(",")):
        edge, span = item.split("=")
        s, e = span.split("-")
        out[edge.strip()].append([int(s), int(e)])
    return out


def measure(arr, manual):
    h, w = arr.shape[:2]
    inside, center = inside_mask(arr)
    info = {}
    for edge in EDGES:
        outer, inner = profile(edge_view(arr[..., 3], edge), edge_view(inside, edge))
        n = len(outer)
        mid = slice(n // 4, max(n // 4 + 1, 3 * n // 4))
        base_o, base_i = float(np.median(outer[mid])), float(np.median(inner[mid]))
        sig = band_sig(edge_view(arr, edge), int(base_i))
        orn = (inner > base_i + max(2.0, 0.15 * (base_i - base_o))) | (outer < base_o - 2)
        orn |= odd_positions(sig, find_period(sig))
        rs = runs(orn)
        start = rs[0][1] if rs and rs[0][0] <= 2 else 0
        end = n - rs[-1][0] if rs and rs[-1][1] >= n - 2 else 0
        middle = [r for r in rs if r[0] > 2 and r[1] < n - 2]
        deepest = max([int(inner[a:b].max()) for a, b in middle] + [int(base_i)])
        info[edge] = {"start": start, "end": end, "middle": middle, "depth": deepest, "n": n}

    ins = {
        "l": max(info["left"]["depth"], info["top"]["start"], info["bottom"]["start"]),
        "r": max(info["right"]["depth"], info["top"]["end"], info["bottom"]["end"]),
        "t": max(info["top"]["depth"], info["left"]["start"], info["right"]["start"]),
        "b": max(info["bottom"]["depth"], info["left"]["end"], info["right"]["end"]),
    }
    ins = {k: int(v) for k, v in ins.items()}
    ends = {"top": ("l", "r"), "bottom": ("l", "r"), "left": ("t", "b"), "right": ("t", "b")}
    depth = {"top": ins["t"], "bottom": ins["b"], "left": ins["l"], "right": ins["r"]}
    fixed, periods = {}, {}
    for edge in EDGES:
        lo, hi = ins[ends[edge][0]], info[edge]["n"] - ins[ends[edge][1]]
        spans = [[int(max(lo, a - 2)), int(min(hi, b + 2))] for a, b in info[edge]["middle"] + manual[edge]]
        merged = []
        for s, e in sorted(x for x in spans if x[1] > x[0]):
            if merged and s <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], e)
            else:
                merged.append([s, e])
        fixed[edge] = merged
        gaps = [g for g in parts(info[edge]["n"], ins[ends[edge][0]], ins[ends[edge][1]], merged) if not g[2]]
        longest = max(gaps, key=lambda g: g[1] - g[0], default=None)
        periods[edge] = int(period(edge_view(arr, edge), longest[:2], depth[edge])) if longest else 0
    return {"w": w, "h": h, "insets": ins, "fixed": fixed, "period": periods, "center": center}


# Layout below mirrors drawFrame() in ui-frames.md; keep the two in step.
def parts(n, a0, a1, fixed):
    out, x = [], a0
    for s, e in fixed:
        if s > x:
            out.append((x, s, False))
        out.append((s, e, True))
        x = e
    if n - a1 > x:
        out.append((x, n - a1, False))
    return out


def place(lst, length, k):
    fixed_len = sum((b - a) * k for a, b, f in lst if f)
    grow_src = sum(b - a for a, b, f in lst if not f)
    if not grow_src:  # the whole edge is ornament: scale it evenly so it still reaches both corners
        total = sum(b - a for a, b, f in lst) or 1
        lst, fixed_len, grow_src = [(a, b, False) for a, b, f in lst], 0, total
    shrink = length / fixed_len if fixed_len > length else 1
    extra = max(0, length - fixed_len)
    out, d = [], 0.0
    for a, b, f in lst:
        size = (b - a) * k * shrink if f else (extra * (b - a) / grow_src if grow_src else 0)
        out.append((a, b, d, d + size, f))
        d += size
    return out


def render(img, m, w, h, k=1.0):
    ins = m["insets"]
    l, t, r, b = ins["l"], ins["t"], ins["r"], ins["b"]
    c = min(k, w / max(1, l + r), h / max(1, t + b))
    if m.get("pixel") and c >= 1:
        c = float(int(c))
    L, T, R, B = l * c, t * c, r * c, b * c
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    resample = Image.NEAREST if m.get("pixel") else Image.LANCZOS

    def blit(sx, sy, sw, sh, dx, dy, dw, dh):
        x0, y0, x1, y1 = round(dx), round(dy), round(dx + dw), round(dy + dh)
        if x1 > x0 and y1 > y0 and sw > 0 and sh > 0:
            piece = img.crop((sx, sy, sx + sw, sy + sh)).resize((x1 - x0, y1 - y0), resample)
            out.alpha_composite(piece, (x0, y0))

    def edge(n, a0, a1, fixed, per, length, draw):
        for a, b, da, db, f in place(parts(n, a0, a1, fixed), length, c):
            p = per if not f and 0 < per <= b - a else 0
            reps = max(1, round((db - da) / (p * c))) if p else 1
            step = (db - da) / reps
            for i in range(reps):
                draw(a, p or b - a, da + i * step, step)

    cw, ch = m["w"] - l - r, m["h"] - t - b
    if m["center"] == "tile" and cw > 0 and ch > 0:
        nx, ny = max(1, round((w - L - R) / (cw * c))), max(1, round((h - T - B) / (ch * c)))
        sw, sh = (w - L - R) / nx, (h - T - B) / ny
        for i in range(nx):
            for j in range(ny):
                blit(l, t, cw, ch, L + i * sw, T + j * sh, sw, sh)
    else:
        blit(l, t, cw, ch, L, T, w - L - R, h - T - B)
    fx, pr, W, H = m["fixed"], m["period"], m["w"], m["h"]
    edge(W, l, r, fx["top"], pr["top"], w - L - R, lambda sa, sl, da, dl: blit(sa, 0, sl, t, L + da, 0, dl, T))
    edge(W, l, r, fx["bottom"], pr["bottom"], w - L - R,
         lambda sa, sl, da, dl: blit(sa, H - b, sl, b, L + da, h - B, dl, B))
    edge(H, t, b, fx["left"], pr["left"], h - T - B, lambda sa, sl, da, dl: blit(0, sa, l, sl, 0, T + da, L, dl))
    edge(H, t, b, fx["right"], pr["right"], h - T - B,
         lambda sa, sl, da, dl: blit(W - r, sa, r, sl, w - R, T + da, R, dl))
    blit(0, 0, l, t, 0, 0, L, T)
    blit(W - r, 0, r, t, w - R, 0, R, T)
    blit(0, H - b, l, b, 0, h - B, L, B)
    blit(W - r, H - b, r, b, w - R, h - B, R, B)
    return out


def preview(img, m, sizes, path):
    shots = [render(img, m, max(1, round(m["w"] * sx)), max(1, round(m["h"] * sy))) for sx, sy in sizes]
    shots = [img] + shots
    gap = 24
    sheet = Image.new("RGBA", (sum(s.width for s in shots) + gap * (len(shots) + 1),
                               max(s.height for s in shots) + gap * 2 + 14), (90, 90, 90, 255))
    d, x = ImageDraw.Draw(sheet), gap
    for i, s in enumerate(shots):
        sheet.alpha_composite(s, (x, gap + 14))
        d.text((x, 4), "source" if i == 0 else f"{s.width}x{s.height}", fill=(255, 255, 0, 255))
        if i == 0:
            ins = m["insets"]
            g = (0, 255, 0, 255)
            for gx in (ins["l"], s.width - ins["r"]):
                d.line([(x + gx, gap + 14), (x + gx, gap + 14 + s.height)], fill=g)
            for gy in (ins["t"], s.height - ins["b"]):
                d.line([(x, gap + 14 + gy), (x + s.width, gap + 14 + gy)], fill=g)
            for a, b in m["fixed"]["top"]:
                d.rectangle([x + a, gap + 14, x + b, gap + 14 + ins["t"]], outline=(255, 160, 0, 255))
            for a, b in m["fixed"]["bottom"]:
                d.rectangle([x + a, gap + 14 + s.height - ins["b"], x + b, gap + 14 + s.height], outline=(255, 160, 0, 255))
            for a, b in m["fixed"]["left"]:
                d.rectangle([x, gap + 14 + a, x + ins["l"], gap + 14 + b], outline=(255, 160, 0, 255))
            for a, b in m["fixed"]["right"]:
                d.rectangle([x + s.width - ins["r"], gap + 14 + a, x + s.width, gap + 14 + b], outline=(255, 160, 0, 255))
        x += s.width + gap
    sheet.convert("RGB").save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frame"); ap.add_argument("out")
    ap.add_argument("--preview"); ap.add_argument("--sizes", default="0.6x0.6,1.6x1,2.6x1.6")
    ap.add_argument("--fixed"); ap.add_argument("--pixel", action="store_true")
    a = ap.parse_args()

    img = Image.open(a.frame).convert("RGBA")
    m = measure(np.asarray(img).astype(np.float32), parse_fixed(a.fixed))
    m["pixel"] = a.pixel
    with open(a.out, "w") as f:
        json.dump(m, f, indent=1)
    ins = m["insets"]
    print(f"insets l{ins['l']} t{ins['t']} r{ins['r']} b{ins['b']}, fixed "
          + ", ".join(f"{e} {m['fixed'][e]}" for e in EDGES if m["fixed"][e])
          + f"; period {m['period']}; centre {m['center']} -> {a.out}")
    if a.preview:
        sizes = [tuple(float(v) for v in s.split("x")) for s in a.sizes.split(",")]
        preview(img, m, sizes, a.preview)


if __name__ == "__main__":
    main()
