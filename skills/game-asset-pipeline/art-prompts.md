# Art prompts for ChatGPT (the way that worked)

The user generates all art in ChatGPT, which makes **one image per message**. Each prompt therefore packs many sprites or frames into one sheet, and the game cuts them apart. This format has worked across many games.

## Deliver prompts like this

- Write every prompt for a batch into **one file**, `~/Downloads/<game>-<topic>-prompts.md`, not into the repo.
- At the top of the file:
  - "Paste ONE prompt per ChatGPT message." Two in one message makes ChatGPT merge them into one tiny sheet.
  - The file name to save each result under (`hh-p16-night.png`).
  - Which images to attach, if any.
  - A table of what goes on which sheet.
- Number the sheets (P1, P2...). Put each prompt in its own fenced code block so it copies cleanly. Add a one-line heading that says what the sheet is.
- When the user drops results in `~/Downloads` (often as `ChatGPT Image <date>.png`), match them to the prompt numbers by content, cut them, and look at the cut before using it.

## The four blocks every sheet prompt has

1. **Style paragraph.** Describe the art style fully in words: medium, outline, shading, palette size, pixel size, lighting, mood, what to avoid ("no anti-aliasing, no blur, no gradients, no painterly brushwork"). Keep this paragraph **identical on every sheet of a game**, so sheets match.
2. **Background.** "The whole background is flat solid magenta #FF00FF, perfectly even: no shadows, no ground, no texture. Do not use any pink, magenta, purple or violet anywhere in the art. No text, no labels, no grid lines, no borders. No glow around anything."
3. **Layout, without a fixed size.** **Do not state image pixel dimensions, cell sizes or "fills 80 percent of its cell".** A fixed sheet size makes ChatGPT bend swords, shorten spears, curl tails and squash poses so everything fits (the user caught this on 2026-10-23). Write instead: "Two rows of four, evenly spaced with wide empty magenta gaps between every figure. Draw every figure complete and in its natural proportions: weapons, tails, wings and cloth at full length and never bent, shortened or cropped to fit. If something is long, leave more space around it rather than changing it." Then the facing and pose: "side view, facing RIGHT" (the game mirrors for left). For long weapons or wide poses, put fewer figures on the sheet (one row of four, or 2x2) instead of squeezing. `cut_sheet.py` finds sprites by shape, so the grid does not need equal cells.
4. **Items in reading order.** A numbered list. Each item gets a precise visual description: silhouette, colors, distinctive features, size relative to the others.

## Rules learned the hard way

- **Magenta keying:** no pink, purple or violet in the art, because it keys out with the background. Rarity colors and tints are drawn in code. **Glows over magenta key into a pink halo, so all glows, light, fire and beams are drawn in code.** Ask for flat pale spots on light organs.
- **Reference images (mandatory for a character's second sheet):**
  - The first sheet of a character is its model sheet. **Every later sheet of the same character must attach it** (ChatGPT: attach the file; Codex CLI: `--image <sheet>.png`) and say "Use the attached image as the exact reference: same person, same outfit, same head-to-body proportions, same art style, same pixel size, same scale." Name the files to attach. Never end a sheet of an existing character with "Do not ask for a reference image": a written description alone drifts, and on Driftborn (2026-10-26) the pose sheet came back with a third-size head, so the chibi lost his big head whenever he sat, begged or ate.
  - Spell the proportions out in measurable words, not just "chibi": "the head (hair included) is as tall as the whole body below the chin". "2.5 heads tall" alone was read loosely.
  - Prefer walk cycle and poses of one character on **one** sheet when they fit; same-sheet frames match best.
  - After cutting, compare head height across every frame of a character (standing frames should match within about 10 percent). If a sheet drifts, regenerate it with the reference; scaling cannot fix proportions.
  - Props, buildings, UI and enemies are written-only and fully described.
  - Without an attachment (a brand-new character or object), end with "Do not ask for a reference image; this description is complete."
- **Same scale on every sheet:** for pixel art, state the art pixel size ("one art pixel is about 4x4 image pixels", matching the backdrops); for painted art, state relative heights ("the enemy is twice the hero's height"). Never fix the sheet or cell size. `cut_sheet.py --scale` evens out what ChatGPT ignores.
- **Characters and world in one style:** the characters' rendering must match the backdrops (pixel heroes on a pixel world, painted on painted). Smooth anime figures on a pixel backdrop looked pasted on.
- **Characters need a hook, not an archetype.** Generic designs (copper-haired knight, black-coat swordsman, silver-haired priestess) fall flat. Give each one: a silhouette you can recognise in black (an odd weapon, a huge prop, a strange hat), one bold signature color that pops on the game's backgrounds, a personality in the face and stance (a grin, a sulk, a smug look), and one fun detail (a mascot, a quirk, a mismatched item).
- **Anything that spins or is a hit target:** ask for a perfectly centered, straight top-down circle.
- **Portrait busts:** 2 per image with wide margins (4 per image cut off the shoulders).
- **Figures must not touch:** ask for wide gaps, never a tighter grid; re-cut by proximity if two figures touch.

## Sheet types

**Character animation (8 frames).** One motion per sheet, read left to right, top row then bottom row:
- 8 in-between frames of one move: wind-up, anticipation, strike, impact, follow-through, recovery.
- The same character height, feet on one shared ground line, facing right, the weapon the same length in every frame.
- Describe each frame's pose in one line.
- For a three-hit boss chain, one sheet per hit.
- Effects (trails, sparks, blood, fire) are not in the art: "draw only the body and weapon; effects are added by the game".

**Enemies and creatures.** One sheet per enemy type: idle, walk 1 and 2, wind-up (a clear tell pose), attack, hurt, stagger or knocked down, death. Armor plates and weak spots must be clearly drawn when the game's combat uses them.

**Props and scenery pieces.** 8 per sheet, each with its function in the description (a breakable statue, a lantern checkpoint, a door). Things that will be interacted with are drawn so they read as usable. Never draw decorative things that look usable.

**Backdrops and panoramas.** 1536x1024 or wider, no magenta: a full painted scene for a far parallax layer. Describe depth bands (sky, far, mid), the time of day and the mood. Leave the bottom band plain where the game's ground goes.

**Tileable textures.** Square, "seamless tileable texture, top-down, evenly lit, no shadows from objects, no vignette".

**UI kit.** One magenta sheet of HUD pieces in the game's style: bar frames with **empty insides** (the game fills them), panel corners for 9-slicing, buttons (normal and pressed), icon frames, a rank or medal frame, a banner, a keycap. No text on anything.

**Icons.** 8 to 16 per sheet, each in the same frame or none, readable at 16 to 36 px.

**Thumbnail cover (always last).** 512x512 composition, full painted scene with no magenta, no text. Show the hero in a signature moment and hint at the story or the best creature. Painted, not a gameplay screenshot.

## After the user delivers

1. `cut_sheet.py <sheet> <out> --names ... --preview check.png`, then look at the preview.
2. Export the atlas (`--atlas`, WebP q88 method 6 for painted art; lossless or box-filtered for pixel art), check it at game size on dark and light backgrounds for halos.
3. Record source, sizes and bytes in `ART.md` ([art-standard.md](art-standard.md)).
4. Tell the user which prompts are done and which art is still a stand-in.
