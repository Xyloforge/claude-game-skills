---
name: game-asset-pipeline
description: How to get game art, sound and music made and processed, for any game. Sprite-sheet prompts for image models (pasted into ChatGPT by the user, or run by Claude through an image-generation CLI such as Codex), magenta and black-background sheets, a sheet cutter, resizable decorated UI frames, a Pixabay SFX search and download tool (headless Chrome), SFX processing, music-generator prompts and loop-point finding, the art encoding standard, and a balance-bot pattern. Use whenever a game needs new art, sprite sheets, backdrops, UI kit, thumbnails, sound effects, ambience or music, or when processing or recording assets.
---

# Game asset pipeline

This is how a game gets its art and sound. Pair it with the `game-detail-bar` skill, which defines the quality bar. All tools are in `scripts/` next to this file; call them by their full path, `${CLAUDE_SKILL_DIR}/scripts/...`.

## The workflow at a glance

| Asset | Who makes it | Guide | Tool |
| --- | --- | --- | --- |
| Sprites, enemies, props, UI kit, effects, backdrops, textures, portraits, thumbnail | An image model, from prompts Claude writes: the user pastes them into ChatGPT, or Claude runs them through an image-generation CLI | [art-prompts.md](art-prompts.md) | `cut_sheet.py` |
| Panels, buttons and bars that resize, decorated anywhere | An image model (UI kit sheet), then Claude | [ui-frames.md](ui-frames.md) | `slice_frame.py` |
| Encoding and recording art | Claude | [art-standard.md](art-standard.md) | `cut_sheet.py --atlas` |
| Sound effects and ambience | Claude, from Pixabay | [sfx-guide.md](sfx-guide.md) | `pixabay_sfx.mjs`, `process_sfx.py` |
| Music | The user, in a music generator such as Suno, from prompts Claude writes | [music-guide.md](music-guide.md) | `find_loop.py` |
| Balance numbers | Claude | [balance-bots.md](balance-bots.md) | your own sim, from the pattern |

## Rules that apply to every asset

1. **Write prompts and lists before generating anything.** Put them in one file, `~/Downloads/<game>-<topic>-prompts.md`, never in the repo until the user picks. One prompt per ChatGPT or Suno message. When Claude generates the art itself, make a few test sprites first for the user to check before running the whole batch.
2. **Every feature gets its assets in the same turn**, including the small ones: each UI and HUD action gets its own sound and its own animation (see the sfx guide's UI list). Never ship a placeholder beep, a shared "generic click" for everything, or a static panel that just appears.
3. **Sound must be as realistic as possible:** real recorded foley from Pixabay (avoid items marked AI-generated), layered and processed. Synth tones only as a fallback while the file loads.
4. **Music prompts describe the game, not the instruments:** what the player is doing, the vibe and theme, fast or slow, the bpm, "instrumental, seamless loop".
5. **Record everything:** `ART.md` (source file, sizes, bytes, encoding, checks) and `AUDIO.md` (Pixabay title, author, ID, original and runtime bytes, cuts, loop points).
6. **Look at the result in the game** at real size before reporting: halos, chopped tails, seams, levels that are too loud, music seams.

## Tools

```sh
# Cut a magenta sheet into sprites (preview first, then an atlas with foot anchors)
python3 ${CLAUDE_SKILL_DIR}/scripts/cut_sheet.py "~/Downloads/<sheet>.png" <out> --names idle,walk1,... --preview check.png
python3 ${CLAUDE_SKILL_DIR}/scripts/cut_sheet.py "~/Downloads/<sheet>.png" <out> --names ... --scale 0.75 --atlas hero-run

# Measure a decorated UI frame for resizing (corners, ornaments that keep their size, repeating edges) + preview
python3 ${CLAUDE_SKILL_DIR}/scripts/slice_frame.py <frame.png> <frame.json> --preview sizes.png

# Find and download Pixabay sound effects (real headless Chrome, polite pauses)
node ${CLAUDE_SKILL_DIR}/scripts/pixabay_sfx.mjs search <raw-dir> "sword clash" "metal armor impact" "ui click wood"
node ${CLAUDE_SKILL_DIR}/scripts/pixabay_sfx.mjs get <raw-dir> clang1=241729 clang2=393837

# Trim, fade, normalise and encode them (spec.json per sound), prints the AUDIO.md byte table
python3 ${CLAUDE_SKILL_DIR}/scripts/process_sfx.py <raw-dir> <game>/audio spec.json

# Find a loop body inside a Suno song that ends on an outro, plus a seam preview to listen to
python3 ${CLAUDE_SKILL_DIR}/scripts/find_loop.py "~/Downloads/<song>.mp3" --preview seam.wav
```

Requirements: Python 3 with Pillow, NumPy and SciPy (`slice_frame.py` needs only Pillow and NumPy) (run without `-I` so user site-packages load); FFmpeg (Homebrew); Node with Playwright (any cached `playwright-core` is found automatically) and Google Chrome installed. Browser work always runs headless.
