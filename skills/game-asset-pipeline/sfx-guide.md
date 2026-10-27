# Sound effects guide

**The more realistic, the better.** Real recorded foley from Pixabay, layered, trimmed and mixed. The user rejects synth beeps, placeholder sounds, and one sample reused for unrelated actions.

## Everything gets a sound, including the UI and HUD

Make a sound list as part of the feature, before building it, and source all of it in the same turn. Reuse a file only when it genuinely fits (a whoosh for a whoosh). In the report, list which sounds are new and which are reused.

**Gameplay:** every attack (light, heavy, charged), every impact by material (flesh, armor, wood, stone, water), parry or clash, dodge, jump and land, footsteps by surface, hurt, death, body fall, pickups, ammo and reload, an empty click, every enemy's tell, attack and pain (rate-limited), every boss move, environment hazards, doors, gates, bells, breakables.

**UI and HUD (the part AIs skip):**
- **Buttons:** hover tick, click or press, back or cancel, a denied click (can't afford, locked).
- **Menus:** open and close (a paper rustle, wood, stone or metal to match the game's material), tab switch, page turn or swipe, slider tick, toggle on and off.
- **Economy:** coin gain (small and big variants), coin count-up ticks, purchase, upgrade level-up, equip.
- **Progress:** star pop (one per star, rising pitch), rank up, new record, NEW discovery card, level complete, quota met, streak.
- **Alerts:** a notification or toast, the timer's warning pulse in the last seconds, low health heartbeat, a boss bar appearing, a title card hit, loading done, a game over sting.
- **Collection:** a journal opening, an item reveal, a rarity reveal that sounds bigger at each tier.

Every UI sound pairs with an animation of the same moment: a button pressing in, a panel opening with an overshoot, a counter bumping, a star popping with sparkles. Sound and motion are built together.

## Finding sounds on Pixabay

Use the tool. It drives a real headless Chrome, which is the only thing that gets past Pixabay's bot protection:

```sh
node ~/.claude/skills/game-asset-pipeline/scripts/pixabay_sfx.mjs search <raw-dir> "sword clash" "armor impact" "wood ui click"
node ~/.claude/skills/game-asset-pipeline/scripts/pixabay_sfx.mjs get <raw-dir> clang1=241729 clang2=393837
```

- `search` saves the results and prints id, length, title and author, and flags AI-generated items. **Avoid AI-generated items.**
- `get` downloads by id inside the same browser session and saves `<name>-source.json` (title, author, id, page URL, SHA-256) for AUDIO.md.
- Keep raw downloads outside the game folder; only processed files ship.

**Choosing:** search 2 to 4 phrasings per sound. Prefer short, dry, close recordings; a sound pack's single hits beat a long montage. Take 2 or 3 variants for anything that repeats (swings, hits, footsteps, coins). Read titles critically: "cinematic" and "epic" are often over-produced.

**Why other tools fail (and what not to do):** Pixabay sits behind Cloudflare bot protection. curl, wget, Python requests, Node fetch, and Playwright's bundled Chromium (it announces "HeadlessChrome") get a 403 or a verification page. What works:
- installed Chrome (`channel: "chrome"`) with a normal Chrome user-agent;
- load the search page and read `window.__BOOTSTRAP__.page.results`;
- fetch each result's `sources.src` from inside that page;
- pause about 2 s between requests and keep batches to a few dozen.

Never solve CAPTCHAs or guess CDN URLs. If a search returns a verification page, or the sandbox has no real internet, stop. Ask the user to pick and download the sounds by hand on pixabay.com into a folder such as `~/Downloads/<game>-sfx/`, then run only the processing step, which needs no network. Pixabay's content license allows use in games without attribution, but record the sources anyway.

## Processing

```sh
python3 ~/.claude/skills/game-asset-pipeline/scripts/process_sfx.py <raw-dir> <game>/audio spec.json
```

Per sound in `spec.json`: `max` seconds kept, `fade` out, `peak` dBFS (impacts -1 to -2, swings -3, UI -4 to -6, loops and ambience -6 to -8), optional `start`, `lowpass` / `highpass`, `loop`. Defaults: lead silence trimmed below -50 dBFS, mono 44.1 kHz, MP3 64 kb/s (long ambience 40 to 96 kb/s). It prints the byte table for AUDIO.md.

Shape the sound to the moment: low-pass a can so it lands dull and waterlogged, cut the rumble off a chest, keep a splash under 650 ms so it matches the visible spray.

## Playback rules (in the game's audio code)

- Layer samples per event and pick one at random with slight pitch jitter, so repeats never sound identical.
- Rate-limit voices globally. Pain cries only on heavy blows; light hits and probes are silent.
- Separate buses and sliders for SFX and music, saved apart from the save file.
- Pause everything when the game pauses or the tab is hidden; cancel pending cues.
- Unlock audio on the first tap (silent buffer for iOS). Loading sound never blocks the start; until a file decodes, play nothing or a quiet synth stand-in.
- Ambience beds per area and time of day (fire crackle, wind, sea, crickets), with occasional one-shots spaced out (distant gulls).

## AUDIO.md record

A source table (runtime file, Pixabay title, author, ID linked, original bytes, runtime bytes), the processing settings, the total reduction, what was reused, and the music section ([music-guide.md](music-guide.md)).
