# UI frames: decorated panels, buttons and bars that resize

A framed panel is drawn at many sizes (a tooltip, a dialog, a shop card, a list row), so it cannot be one stretched
image: stretching smears every gem and spike. Plain 9-slice (four corners, four stretched edges, a centre) fixes the
corners but forces all decoration into them. This guide keeps decoration **anywhere on the frame** and still lets
the panel resize.

## Pick the method per piece of UI

| The UI piece | Method |
| --- | --- |
| Resizes (dialogs, tooltips, cards, list rows, buttons, bars) | **Sliced frame with fixed spans** (below): corners and ornaments keep their size, only the parts between them grow |
| Ornaments that animate, glow or change with state (a gem that turns red at low HP) | A simpler frame plus **ornament sprites placed on top** at set points (the middle of an edge, 25 percent along, a fixed distance from a corner) |
| One long pattern that must never be cut (a carved frieze) | Panel sizes **snap to whole repeats** of the pattern |
| Never resizes (title screen, a boss card, the main shop) | **One fixed-size image**; decorate it however you like |

A game usually mixes them: a fixed title frame, sliced dialogs, and overlaid gems on the HUD.

## How a sliced frame with fixed spans works

```
corner | grow | GEM | grow | SKULL | grow | corner      (each edge, on its own)
```

- **Corners** keep their size.
- **Fixed spans** (gems, crests, spikes, torn-cloth pieces) keep their size and stay in place along the edge.
- **Grow spans** between them take the extra length, shared in proportion to their source length, so a centred gem
  stays centred. An edge with a repeating pattern (rivets, vines, stitching) **tiles** its grow spans by whole
  repeats instead of stretching them; a plain edge stretches.
- **The centre** stretches when flat and tiles when textured.
- Smaller than the source: everything shrinks evenly; an edge that is ornament from end to end scales evenly too.

## 1. Prompt

Add to the UI kit sheet (see [art-prompts.md](art-prompts.md)), with the game's usual style paragraph and magenta
background:

> Ornate frames in the game's style. Decorate them anywhere: corners, along the edges, the middle of each side.
> Each ornament (gem, crest, skull, spike, cloth tatter) is a separate, complete shape, with a stretch of plain frame
> on both sides of it, never touching the next ornament. Between ornaments, each edge is either plain or carries one
> short pattern (rivets, vines, stitching) at a steady spacing. The inside is a flat colour or a fine even texture,
> or empty. Buttons come in normal and pressed versions with the same border width. Bars have an empty inside.
> No text.

The "plain frame on both sides" line is what lets the tool tell ornament from border; the model keeps full freedom
over where and how much to decorate. For ornaments that should animate or change colour, ask for them as
separate items on the same sheet.

## 2. Measure

Cut the sheet with `cut_sheet.py`, then measure each frame:

```sh
python3 ${CLAUDE_SKILL_DIR}/scripts/slice_frame.py <frame.png> <frame.json> --preview sizes.png
python3 ${CLAUDE_SKILL_DIR}/scripts/slice_frame.py <frame.png> <frame.json> --pixel --sizes 2x2,4x1    # pixel art
python3 ${CLAUDE_SKILL_DIR}/scripts/slice_frame.py <frame.png> <frame.json> --fixed top=120-180          # add a missed ornament
```

It finds the corners, every ornament (by shape: deeper or sticking out; and by colour: breaking the edge's usual
pattern), each edge's repeat length, and the centre mode, and writes:

```json
{"w": 736, "h": 181, "insets": {"l": 188, "t": 67, "r": 176, "b": 73},
 "fixed": {"top": [ [255, 276], [277, 426] ], "bottom": [ [317, 390] ], "left": [ [67, 108] ], "right": [ [67, 108] ]},
 "period": {"top": 0, "bottom": 0, "left": 0, "right": 12}, "center": "stretch", "pixel": false}
```

**Look at the preview** (the frame at several sizes, with corners in green and fixed spans in orange on the source).
A smeared, doubled or cut ornament means a missed span: add it with `--fixed`, or regenerate the frame with more
plain border around that ornament. Merge the JSON into the atlas entry (`x`, `y` = the frame's place in the atlas)
and record the frame and its checks in `ART.md`.

## 3. Draw

The same layout as the preview, for canvas. Draw each panel size once into an offscreen canvas and reuse it; never
re-slice every frame.

```js
// m: the frame's JSON (+ x, y in the atlas); img: the atlas. k: UI scale for the corners and ornaments.
function frameParts(n, a0, a1, fixed) {
  const out = []; let x = a0;
  for (const [s, e] of fixed) { if (s > x) out.push([x, s, false]); out.push([s, e, true]); x = e; }
  if (n - a1 > x) out.push([x, n - a1, false]);
  return out;
}
function framePlace(list, len, k) {
  let fixedLen = 0, growSrc = 0;
  for (const [a, b, f] of list) f ? (fixedLen += (b - a) * k) : (growSrc += b - a);
  if (!growSrc) { // the whole edge is ornament: scale it evenly
    list = list.map(([a, b]) => [a, b, false]); fixedLen = 0; growSrc = list.reduce((t, [a, b]) => t + b - a, 0) || 1;
  }
  const shrink = fixedLen > len ? len / fixedLen : 1, extra = Math.max(0, len - fixedLen);
  let d = 0;
  return list.map(([a, b, f]) => {
    const size = f ? (b - a) * k * shrink : extra * (b - a) / growSrc;
    const r = [a, b, d, d + size, f]; d += size; return r;
  });
}
function drawFrame(ctx, img, m, x, y, w, h, k = 1) {
  const { l, t, r, b } = m.insets;
  let c = Math.min(k, w / (l + r), h / (t + b));
  if (m.pixel && c >= 1) c = Math.floor(c);
  const L = l * c, T = t * c, R = r * c, B = b * c, ox = m.x || 0, oy = m.y || 0;
  ctx.imageSmoothingEnabled = !m.pixel;
  const blit = (sx, sy, sw, sh, dx, dy, dw, dh) => {
    const x0 = Math.round(x + dx), y0 = Math.round(y + dy), x1 = Math.round(x + dx + dw), y1 = Math.round(y + dy + dh);
    if (x1 > x0 && y1 > y0 && sw > 0 && sh > 0) ctx.drawImage(img, ox + sx, oy + sy, sw, sh, x0, y0, x1 - x0, y1 - y0);
  };
  const edge = (n, a0, a1, fixed, period, len, draw) => {
    for (const [a, b, da, db, f] of framePlace(frameParts(n, a0, a1, fixed), len, c)) {
      const p = !f && period > 0 && period <= b - a ? period : 0;
      const reps = p ? Math.max(1, Math.round((db - da) / (p * c))) : 1, step = (db - da) / reps;
      for (let i = 0; i < reps; i++) draw(a, p || b - a, da + i * step, step);
    }
  };
  const cw = m.w - l - r, ch = m.h - t - b, iw = w - L - R, ih = h - T - B;
  if (m.center === "tile" && cw > 0 && ch > 0) {
    const nx = Math.max(1, Math.round(iw / (cw * c))), ny = Math.max(1, Math.round(ih / (ch * c)));
    for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) blit(l, t, cw, ch, L + i * iw / nx, T + j * ih / ny, iw / nx, ih / ny);
  } else blit(l, t, cw, ch, L, T, iw, ih);
  const { fixed: fx, period: pr, w: W, h: H } = m;
  edge(W, l, r, fx.top, pr.top, iw, (sa, sl, da, dl) => blit(sa, 0, sl, t, L + da, 0, dl, T));
  edge(W, l, r, fx.bottom, pr.bottom, iw, (sa, sl, da, dl) => blit(sa, H - b, sl, b, L + da, h - B, dl, B));
  edge(H, t, b, fx.left, pr.left, ih, (sa, sl, da, dl) => blit(0, sa, l, sl, 0, T + da, L, dl));
  edge(H, t, b, fx.right, pr.right, ih, (sa, sl, da, dl) => blit(W - r, sa, r, sl, w - R, T + da, R, dl));
  blit(0, 0, l, t, 0, 0, L, T); blit(W - r, 0, r, t, w - R, 0, R, T);
  blit(0, H - b, l, b, 0, h - B, L, B); blit(W - r, H - b, r, b, w - R, h - B, R, B);
}
```

For DOM menus, a frame with **no fixed spans** can use CSS instead:
`border-image: url(frame.png) <t> <r> <b> <l> fill / <t>px <r>px <b>px <l>px round;` (`round` for patterned
edges, `stretch` for plain ones, plus `image-rendering: pixelated` for pixel art). A frame with fixed spans is drawn
into a canvas with `drawFrame` and used as the element's background.

Content goes inside the frame's safe inner rectangle (the insets scaled by `c`), never on the rim; see the UI layout
rules in the `game-detail-bar` skill.

## 4. Check

- Draw every frame at the smallest and largest size the game uses, plus one odd size, on dark and light
  backgrounds: no smeared or doubled ornament, no seam where tiles meet, no magenta fringe, corners not overlapping.
- Buttons: normal and pressed line up exactly (same insets), so the press does not jump.
- Pixel art: corners scale by whole numbers only, and patterned edges tile.
