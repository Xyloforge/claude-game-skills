"""Key a ChatGPT magenta (#FF00FF) sheet and cut it into sprites, in reading order.

Usage:
  python3 cut_sheet.py <sheet.png> <out-dir> [--names idle,walk1,walk2,...] [--scale 0.75] [--atlas name]
          [--rows 2] [--pad 4] [--min-area 400] [--preview check.png]

- Keys magenta and its pink/violet fringe to transparency (soft edge, de-spilled), so no pink halo remains.
- Finds each sprite as a connected blob (small fragments within --join px are merged into the nearest big blob, so a
  sword tip or loose spark stays with its owner), then sorts them into --rows rows, left to right.
- Without --atlas: writes <name>.png per sprite. With --atlas: packs them into <atlas>.webp (q88, method 6, alpha) and
  <atlas>.json with each frame's rectangle and its foot anchor (bottom centre of the opaque pixels), so every
  frame stands on the same ground line.
- --scale resizes with Lanczos so sheets drawn at different sizes match in game (pick one target height per
  character, e.g. 300 px).
- --preview draws every cut box and name on a grey copy for a visual check. Always look at it: tails or weapons that
  cross into the next cell come out chopped or attached to the wrong sprite; fix with --join or by re-cutting by hand.
Needs Pillow, NumPy and SciPy. Record source file, sizes and bytes in the game's ART.md.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage


def key_magenta(img):
    rgb = np.asarray(img.convert("RGB")).astype(np.float32)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    # Magenta-ness: red and blue high, green low. Fringes are partially magenta.
    m = np.clip((np.minimum(r, b) - g) / 255.0, 0, 1)
    alpha = np.clip(1.0 - (m - 0.35) / 0.4, 0, 1)
    # De-spill: pull remaining magenta out of the edge pixels.
    spill = np.clip(np.minimum(r, b) - g, 0, None) * (1 - alpha)
    rgb[..., 0] -= spill
    rgb[..., 2] -= spill
    out = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def find_sprites(alpha, min_area, join):
    solid = alpha > 24
    labels, count = ndimage.label(ndimage.binary_dilation(solid, iterations=2))
    boxes = ndimage.find_objects(labels)
    areas = ndimage.sum(solid, labels, range(1, count + 1))
    big = [i for i in range(count) if areas[i] >= min_area]
    small = [i for i in range(count) if areas[i] < min_area]
    rects = {i: [boxes[i][1].start, boxes[i][0].start, boxes[i][1].stop, boxes[i][0].stop] for i in big}
    for i in small:  # merge fragments into the nearest big blob within `join` px, else drop them as noise
        s = boxes[i]
        cx, cy = (s[1].start + s[1].stop) / 2, (s[0].start + s[0].stop) / 2
        best, dist = None, join
        for j, (x0, y0, x1, y1) in rects.items():
            d = max(x0 - cx, 0, cx - x1) + max(y0 - cy, 0, cy - y1)
            if d <= dist:
                best, dist = j, d
        if best is not None:
            x0, y0, x1, y1 = rects[best]
            rects[best] = [min(x0, s[1].start), min(y0, s[0].start), max(x1, s[1].stop), max(y1, s[0].stop)]
    return list(rects.values())


def reading_order(rects, rows):
    # Rows may hold different counts (4 walk rows of 3, then a pose row of 4), so split at the
    # rows-1 widest vertical gaps between figure centres instead of assuming equal-sized rows.
    rects = sorted(rects, key=lambda r: (r[1] + r[3]) / 2)
    centres = [(r[1] + r[3]) / 2 for r in rects]
    gaps = sorted(range(1, len(rects)), key=lambda i: centres[i] - centres[i - 1], reverse=True)
    cuts = sorted(gaps[:max(0, rows - 1)])
    ordered, start = [], 0
    for end in cuts + [len(rects)]:
        ordered += sorted(rects[start:end], key=lambda r: r[0])
        start = end
    return ordered


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet"); ap.add_argument("out")
    ap.add_argument("--names"); ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--atlas"); ap.add_argument("--rows", type=int, default=2)
    ap.add_argument("--pad", type=int, default=4); ap.add_argument("--min-area", type=int, default=400)
    ap.add_argument("--join", type=int, default=40); ap.add_argument("--preview")
    a = ap.parse_args()

    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    keyed = key_magenta(Image.open(a.sheet))
    alpha = np.asarray(keyed)[..., 3]
    rects = reading_order(find_sprites(alpha, a.min_area, a.join), a.rows)
    names = a.names.split(",") if a.names else [f"f{i + 1}" for i in range(len(rects))]
    if len(names) != len(rects):
        print(f"warning: found {len(rects)} sprites but {len(names)} names; check --preview, --min-area and --join")

    sprites = []
    for name, (x0, y0, x1, y1) in zip(names, rects):
        if name in ("", "-", "none"):
            continue
        box = (max(0, x0 - a.pad), max(0, y0 - a.pad), min(keyed.width, x1 + a.pad), min(keyed.height, y1 + a.pad))
        im = keyed.crop(box)
        if a.scale != 1.0:
            im = im.resize((max(1, round(im.width * a.scale)), max(1, round(im.height * a.scale))), Image.LANCZOS)
        sprites.append((name, im))

    if a.preview:
        prev = Image.new("RGBA", keyed.size, (90, 90, 90, 255)); prev.alpha_composite(keyed)
        d = ImageDraw.Draw(prev)
        for name, r in zip(names, rects):
            d.rectangle(r, outline=(0, 255, 0, 255), width=2); d.text((r[0] + 3, r[1] + 3), name, fill=(255, 255, 0, 255))
        prev.convert("RGB").save(a.preview)

    if not a.atlas:
        for name, im in sprites:
            im.save(out / f"{name}.png")
        print(f"{len(sprites)} sprites -> {out}")
        return

    gap = 2
    w = sum(im.width for _, im in sprites) + gap * (len(sprites) - 1)
    h = max(im.height for _, im in sprites)
    atlas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    frames, x = {}, 0
    for name, im in sprites:
        atlas.paste(im, (x, 0))
        ys, xs = np.nonzero(np.asarray(im)[..., 3] > 24)
        foot = [int((xs.min() + xs.max()) / 2), int(ys.max())] if len(xs) else [im.width // 2, im.height]
        frames[name] = {"x": x, "y": 0, "w": im.width, "h": im.height, "foot": foot}
        x += im.width + gap
    path = out / f"{a.atlas}.webp"
    atlas.save(path, "WEBP", quality=88, method=6)
    (out / f"{a.atlas}.json").write_text(json.dumps(frames, indent=1))
    print(f"{len(frames)} frames -> {path} ({w} x {h}, {path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
