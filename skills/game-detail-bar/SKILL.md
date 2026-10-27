---
name: game-detail-bar
description: The user's attention-to-detail bar for building any game (camera, game feel, SFX and music, animation variety, enemy/boss/item uniqueness, non-repetitive stages, scoring and balance, bot testing, art direction, UI and HUD, mobile, performance). Use when pitching, specifying, building, reviewing or reporting on any game or game feature, including new games, new stages, new enemies, bosses, items, moves, menus and HUDs.
---

# Game detail bar

This skill is a quality bar for any game. Each rule below is something an AI left out and the user had to ask for. Example numbers are in [reference.md](reference.md).

**The core rule:** a feature is not done when it works. It is done when it *looks, sounds, moves, reads and balances* like a finished game. Build all of that in the same turn, not as "polish later".

## How to use this skill

1. **Pitching or speccing:** run through each section and write the answers into the spec: camera plan, feel per action, SFX list, animation list, what makes each enemy and item unique, one idea per area or room, a scoring and balance model, and a bot test plan.
2. **Building:** every new move, enemy, item, room or menu ships with its own camera, feel, SFX, animation, HUD and test pieces, in the same turn.
3. **Before reporting done:** go through the checklist at the bottom. In the summary, say which SFX are new and which are reused, which checks ran, and what is still a stand-in.

---

## 1. Camera

- **Never lock the camera to the player.** Ease toward a target (lerp about 0.1 per frame, or `dt * 6` in seconds), with **look-ahead** in the facing or moving direction. Look ahead more while moving, less while attacking, more when mounted or fast.
- **Vertical framing has rules.** Rest the camera on the floor the player last stood on, and ease between levels. Ease up faster than down, and snap down on a fall. Rise for air juggles so the player stays in the upper-middle. Sink the view to show a hazard below (a burning moat under a bridge).
- **Camera reacts to events; the HUD never shakes.**
  - *Trauma shake:* squared trauma, decays every frame, biggest event wins (`max`, not `+`).
  - *Directional kick:* knocked away from the hit direction, clamped.
  - *Spring jolt:* holds through hit-stop, snaps back with slight overshoot.
  - *Zoom punch:* FOV or scale on big hits, launches, landings, a fish breaching the surface.
  - *Lean-in:* zoom in a little during a focused moment such as a reel fight.
- **Cutscene and boss cameras:** letterbox bars, focus on the boss, and **keep feet clear of the letterbox** (put the floor at a fixed share of the screen, about 74%, at any zoom). Keep the whole creature in frame during a transformation.
- **Arena lock only for bosses.** Elsewhere the player can push past. A boss waits until the regular enemies near its arena are down.
- **Portrait or narrow screens get their own camera distance and FOV**, not the landscape one squeezed.
- **Scenery between the camera and the player fades out** (walls, gates, banners in 2.5D).
- **Off-screen things that matter get an edge arrow:** objective, horse, legendary fish.
- **Slow motion is a reward:** perfect dodge (about 1 s), gate-breaking blow (short), boss killing blow (longer), a fish breaching the surface.

## 2. Game feel and impact (on every hit, not only big ones)

- **Hit-stop scaled per move or species** (about 0.02 to 0.16 s), plus a white or tinted hit flash on the victim, knockback, and a recoil pose.
- **Scale feedback by weight:** small fish get shake 1.3 and 35 ms stop; a tuna gets 4.8 and 115 ms; particle counts scale too. Never one flat value for everything.
- **Lights:** muzzle flashes, blade hits, clashes and spells briefly light their surroundings. In dark stages they cut the darkness, and a bullet lights its whole path.
- **Tie VFX to the art.** Slash trails follow the detected blade points, and smoke comes out of the actual muzzle. An effect that floats off the sprite reads as cheap.
- **Particles obey the world:** blood lands on the ground and stops, sparks bounce. Blood and wake fade instead of popping. Splashes only at the waterline, and only when visible.
- **Element and upgrade changes recolor everything at once:** the thunder spear turns trails, hit flash, Special blast and sparks blue.
- **Danger reads before damage:** a wind-up glow (yellow = parryable, red = dodge only), ground lanes that track until about 70% of the wind-up then lock, a warning ring whose duration matches the real wind-up, and tells such as eyes in the dark or dust at the edge. Keep the tell code in **one place** so every enemy in every stage uses it.
- **Press buffer** of 0.15 to 0.18 s, spent exactly once. A killing-blow press must not skip the ending cutscene.

## 3. Sound and music

- **UI and HUD count too:** button hover and press, a denied click, panels opening and closing, tabs, sliders, coin gain and count-up ticks, purchases, star pops, rank up, records, toasts, timer warnings, title cards, loading done. Each gets its own sound *and* its own animation, built together. The full list and the Pixabay download tool are in the `game-asset-pipeline` skill's `sfx-guide.md`.
- **Every new move, skill, enemy action, UI action and prop ships with its own fitting recorded SFX in the same turn.** No synth beeps, and no placeholder mix of unrelated samples. Reuse only when it truly fits (a whoosh for a whoosh). Source from Pixabay and avoid AI-generated items.
- **Document each sound** in `AUDIO.md` (title, author, ID, original bytes, runtime bytes) and the processing: trim silence below -50 dBFS, cap the length with a fade, mono 44.1 kHz, normalise per sound, MP3 64 kb/s.
- **Variation:** layer samples per event, pick one of 2 or 3 at random, and add slight pitch jitter so repeated hits never sound the same.
- **Mix discipline:** rate-limit creature voices globally. Pain cries only on heavy blows (about 5 s between them). Light hits and probes are voiceless. Use quieter mixes for frequent hits.
- **Ambience beds:** fire crackle, wind, sea, distant gulls spaced out, crickets at night. Each stage or time of day has its own.
- **Music** (Suno, made by the user):
  - Loop a section the song itself repeats, never through its outro. Find it by matching spectral windows: play the intro once, then jump back by the section length.
  - Duck the music for pause, menus, cinematics and big catches, and resume from the same position.
  - Pause all audio when the tab is hidden.
- **Boss entrance:** the stage music fades to silence, sound builds the scene (gates, heartbeat, bell, organ, candles), and the boss theme **cuts in from its first bar on the title card**. After a death, the theme starts at once.
- **iOS/Safari:** unlock audio on the first tap with a silent buffer and resume on return. Sound must never block the game from starting.
- Suno prompts give vibe, bpm, what it is for, and "instrumental, seamless loop". Never list instruments.

## 4. Animation variety

- **8-frame sheets per main move** (wind-up, impact, follow-through), not one pose per attack. Each hit in a boss's 3-hit chain gets its own sheet.
- **Hit windows match the art:** they start on the mid-swing frame and end on the impact frame.
- **Every state needs a pose:** idle *breathing*, run, jump, land, hurt, stagger or kneel, death, and a corpse that lies where it fell. An executed boss *holds* its stagger pose and flinches at each blow. Single-pose moves settle back to guard after a short recovery instead of freezing.
- **Motion by body type, not one wiggle for all:**
  - fish swing their tail; eels ripple the whole body;
  - rays ripple gently; shells barely flex;
  - squid pump their mantle.
  - Thrash scales with size.
- **Idle life in the world:** a vendor who breathes, wipes her hands and waves; bobbing props; drifting light rays; passing gulls; loot that sways in a current; chests that rock and puff sand.
- **Turning is smooth:** no instant flips, and a turn threshold (only when the player is more than about 60 units behind, not twice in 0.3 s).
- **Physics feel where it belongs:** speared loot swings like a weight on a rope, and charges draw back, then drive.
- **Draw order:** a held weapon goes under the holding hand and over the far hand. Ground markers and shadows draw under characters, over uneven ground.

## 5. Enemies and bosses: each one unique

- **Each enemy has a distinct job and tell**, not a reskin with more HP:
  - *hounds:* packs that circle and split, a yellow low snap, a red pounce, a howl;
  - *priests:* keep distance, lob, and cast a ward (a hit breaks it);
  - *ghouls:* cling to ceilings and drop;
  - *pikemen:* a long narrow lane;
  - *royal guards:* block frontal hits.
  - A recolored "veteran" is fine only with real behaviour changes (thrusts twice, hits harder) and a different score weight.
- **Enemies use the level:** climb ledge to ledge, leap down at a player below, jump up to low ledges, stop charges at edges, wait under roofs, ambush from coffins or side gates.
- **Bosses:**
  - 2 or more phases, with an enrage below 50% that *changes* moves (charged ground, double passes, blood moon), not only speed;
  - weighted move picks that never repeat the last one;
  - they *read* the player (punish healing in sight, punish range camping, adapt to dodge spam).
  - Each boss gets an intro scene with arena props, a title card with an epithet, and a skippable replay after death.
  - A memorable signature mechanic: the mirror phase where only the real one casts a shadow; the shadow clone that learns your last 96 actions; the Moon Hunt runs from off screen.
- **Fairness:** every unblockable is readable. Clashes have a still beat before the mash. A boss is out of ground reach while hovering, so the player must jump, shoot or chain up to it.
- **Hazards are interactive:** knock enemies into pyres, effigies and spikes for environment kills and big style points. Hazards deal a share of max HP instead of one-shotting.

## 6. Items, upgrades and collectables: each one changes how you play

- **Rarity tiers drawn in code colors:** common green, uncommon blue, rare purple, legendary gold. Apply them to everything (fish, hats, finds, upgrade levels) and show them on tiles, cards and badges.
- **Legendaries are about being strange and visually unique, not bigger** (goblin shark, leafy sea dragon). They are truly rare (about 1% base, more with a charm), arrive with a shimmer, sound and banner, and leave if ignored.
- **Every upgrade is visible in the world:** a brass scope clamps on the rail, the stall hangs the fish you landed, a hat raises the sale. Every relic has a mechanical rule, not just +x%.
- **Upgrades come in levels** (3, plus a gated legendary level 4). Price the "too good" lines highest. The skewer was asked to be "not too OP, expensive but balanced".
- **Collections are a goal of their own:** a journal with silhouettes for undiscovered items, flavor text, times found, records, and a NEW or BIGGEST card with a count-up.

## 7. Stages and levels: no repetition

- **One idea per area or room**, and name them: graveyard hill, catacombs, rooftop fire chase, bell tower, burning bridge; organ room, belfry collapse chase, portrait gallery, mirror gallery.
- **Forward routes with height** (slopes, steps, one-way ledges, ceilings, an optional upper route with a reward) beat flat arenas of waves.
- **Each stage changes the rules:** a dark forest lit only by fire, a rising-blood climb, an escort ram, a stage won on horseback. A new stage reusing the last stage's enemies and art as stand-ins is a stopgap and must be listed as one.
- **Chases and set pieces:** a fire wall sweeping at 330 units/s, a collapsing stair, a lit-up final fight.
- **Day or tide variety:** seeded daily content (the same on reload), alternating day and night with its own roster, art grade, ambience and music.
- **Checkpoints placed by feel** (lanterns, candle racks): passing one lights it and heals. State that should persist across death persists (broken windows, claimed caches).
- **Clean the level art:** no duplicate platforms that read as walkable, no dead props that look usable (a fake door), nothing floating, and no indiscriminately scattered decoration. In 3D maps, never use flat billboard grass, trees or shrubs.

## 8. Scoring, economy and balance

- **Score multipliers from skill:** style rank D to SSS (up for variety, parries, perfect dodges and environment kills; down for repetition, damage and idling), plus a time bonus and a stage rank with medals.
- **Results screens show the skill stats** (perfect dodge count, KOs, rank) and are mostly pictures: stars pop in one by one, earnings count up, chips show quota, bonus and streak.
- **Goals told up front:** a market card with three star goals at the start of a tide, progress in the pause menu, and a day-1 hint pointing at the first goal.
- **Model the economy before tuning by feel.** Write a simulator that plays whole days or stages with weak, average and good bots and prints quota rate, coins, and the day each upgrade is owned. Tune prices to target times ("average player owns everything around day 11 to 14").
- **Scale with progress:** quotas, order mix and targets keep growing with the player's gear, so nothing becomes free late.
- **Fairness rules:**
  - letting go always loses the fish;
  - full gear wins every fight within its tier's time;
  - orders never ask for what the player cannot have yet;
  - missing a quota costs a streak, never coins.
  - **Never take away earned progress** (the shark thief was rejected); prefer opt-in risk and reward.
- **Hard Mode as a separate track:** 1.5x hits and damage, faster wind-ups with matching warning rings, a darker look, and its own best-rank medal that never touches normal ranks.

## 9. Bot testing and verification

- **`verify.js` with deterministic checks** for every rule: windows, combos, quotas, odds, save migration, exactly-once payouts. It grows with each feature (100 to 150 checks for a full game).
- **Play the real game with bots:** skilled, button-masher and rider (or weak, average and good). Assert ranges, not single values:
  - a bot clear averages 2 to 5 minutes;
  - a masher who never dodges does *not* always clear;
  - a skilled rider clears 5 of 6.
  - Bots behave like players (pick up heals, step off charged ground).
  - Comment why each floor is what it is.
- **Fight-balance sweeps over seeds per species or boss** (8 seeds), plus a `CURVE=1` or season mode that prints land rates per gear setup.
- **Headless browser walk** (Playwright, `headless: true`) at 1280×720, 1366×768, 1920×1080 and a phone landscape such as 844×390. Cover every menu and fight and get 0 page errors. Also cover failure paths: 404 or corrupt art, an audio timeout, and retry.
- **Profile fps on a simulated phone before handing over** (section 14). Frame rate is part of the feel; desktop numbers hide phone problems.
- **QA hooks behind `?qa=1` or typed cheats** (one-shot, undying, start a given fight or tide) for testing, documented, and removed or gated before release.

## 10. Art theme and style

- **One coherent painted direction per game, never code-drawn stand-ins in the final build.** Replace code palms, banners and bushes with painted art. Tell the user when stand-ins remain.
- **Contrast in the art:** a readable, colorful hero against a desaturated, oppressive world. Characters stay readable on any background (use a second tell when a shadow is hard to see on carpet).
- **Atmosphere layers:** parallax (the far panorama at about 28% camera speed), fog, light shafts, marine snow, embers, a vignette, darkness cut by light, and a day or night grade.
- **Pipeline per [[chatgpt-sprite-sheet-workflow]]:** magenta sheets (wide gaps, no fixed image or cell size, so weapons are never bent to fit), chroma key, cutter, WebP q84 to 90. Record sources, sizes and budget exceptions in `ART.md`. Re-cut by proximity when figures touch. Never upscale tiny art into mush.
- **Thumbnails are painted covers** (512×512 WebP) with a story hint, not a gameplay screenshot.
- **Load smart:** a stage's art loads behind a loading screen (stage painting, lore line, turning sigil) and is decoded before first draw to avoid hitches. Later stages load in the background only once unlocked.

## 11. UI and HUD

- **Painted UI kit and bundled fonts, never system fonts or plain rect bars.** Use 9-slice panels, rope-knot or gothic frames, and icons at native sizes. Fonts are bundled woff2 with their OFL license.
- **HUD that lives:**
  - a coin counter that rolls up and bumps on income;
  - a tide or time dial with a travelling sun and a warm pulse in the last 20 s;
  - a Rally (recoverable damage) segment on the health bar;
  - meters in segments;
  - a style rank with its own colors;
  - relic medallions;
  - an escort progress track with a cart icon instead of a number.
- **Diegetic where possible:** a chalkboard quota on the pier, a wanted poster that gets stamped PAID, customer speech bubbles with a burning patience fuse (amber, then red, then the customer sighs and leaves).
- **Motion in menus:** short overshoot on open, cards lift on hover, stars pop with sparkles, count-ups pop when they land, the HUD slides in at start.
- **Gauges grow out of the thing they measure** (the catch bar from the fish), show tick marks, glow when you're in the zone, flash in danger, and the frame shakes when you're losing.
- **Prompts follow the bindings:** keycaps, tips and the key strip show the bound key or pad button and switch when a pad is used. A full key strip on title and pause screens; keep the bottom edge clear in play.
- **Cards and toasts never block play:** a big card closes on the first press without firing; small toasts let the shot through; dismiss old reveals before a new struggle; unlock cards queue separately from routine notices and pause their timers in menus.
- **Pause menu:** Resume, separate Music and SFX sliders (stored apart from the save), key bindings (rebind, swap on conflict, reset), how to play, fullscreen, and Quit or Reset with a confirm where "keep playing" is the default.

## 11b. HUD and UI animation (every element moves, with intent)

A static HUD that only changes numbers reads as unfinished. Every HUD element has an enter, a change, an idle and an exit motion, and each motion pairs with its sound (section 3).

- **Health and resource bars:**
  - Damage: the lost chunk flashes white, holds about 0.3 s, then drains with an ease-out (a delayed "ghost" segment). A heal fills smoothly with a soft glow at the leading edge.
  - Low health: the bar pulses, the screen edge glows red with a heartbeat rhythm, and the portrait looks hurt.
  - Full meter (ultimate, ember): a breathing glow and a small shimmer travelling along it; it pops once when it fills.
  - Segmented meters fill segment by segment, each with a tick.
- **Damage and feedback numbers:**
  - They pop in with an overshoot, arc up and fade.
  - Size and color differ by kind: crit or perfect hit bigger with a flash, blocked hits small and grey, heals green and rising, misses as a word.
  - Several numbers stack and fan out instead of overlapping, and they stay readable on any background (outline or dark shadow).
- **Turn, state and phase changes:**
  - Turn-order portraits slide into the new order; the active one lifts, scales up a little and glows.
  - Banners swipe in and out ("Your turn", "Boss phase 2", "Perfect!") with a hold of about 0.8 s, never blocking input longer than that.
  - Phase changes get a short screen-wide moment (a flash, a sting, the boss bar cracking or changing color).
- **Buttons and menus:**
  - States: hover (lift and brighten), pressed (sink and darken), disabled (dimmed; a click shakes it and plays the denied sound), selected (outline or glow).
  - A gamepad or keyboard focus ring that glides between buttons instead of jumping.
  - Panels open with a scale-and-fade overshoot, and close faster than they open. Lists stagger in item by item (about 30 to 50 ms apart).
  - Tabs slide their underline, and the content cross-fades.
- **Status effects and icons:** they pop in when applied, tick or flash when they count down, blink in their last second, and burst when removed or cleansed. Stacks show a count that bumps.
- **Rewards and progress:** count-ups that speed up then land with a pop; items fly from where they were won to the inventory or purse; rarity reveals that build up longer and brighter at each tier (a legendary gets a sunburst and a pause); records and NEW stamps slam in.
- **Screen transitions:** wipes, fades or an iris between title, map, fight, shop and results; never a hard cut. The HUD slides in at the start of play and out at the end.
- **Idle life:** a slow shimmer on legendary items, a soft bob on a prompt waiting for input, a flicker on candle or torch frames, a gently turning sigil on loading.
- **Timing and easing rules:**
  - UI motion lasts 150 to 300 ms (rewards and reveals may run longer).
  - Ease-out to enter, ease-in to leave, a small overshoot (about 5 to 10%) on pops.
  - Animations run on real time, not game time, so they keep moving during hit-stop and slow motion, and pause with the pause menu only where it makes sense.
  - The HUD never shakes with the camera; it gets its own small bump instead.
  - Respect a reduced-motion setting by shortening or skipping big motions.
- **Verify it:** take headless screenshots or short frame strips of each HUD animation mid-motion, and check that no animation overlaps, clips off screen, or hides the action at phone sizes.

## 12. Input, mobile and screens

- **Keyboard first, and every hold action on a key.** The user plays on a touchpad, so nothing should need a held mouse button. Add controller support (Gamepad API, rumble on big hits). Make every key rebindable and store bindings in localStorage.
- **Phones:**
  - thumb joystick or pads plus right-side buttons, each finger tracked on its own;
  - buttons that change role in context (fire becomes the winch);
  - touch slop on small buttons;
  - swipeable pages.
- **First tap enters fullscreen and locks landscape** where allowed. Portrait shows a "turn your phone" card and pauses. Respect notch safe areas. Give phones their own HUD layout (centre the boss bar in the gap, not over the fight).
- **The scene fills every aspect ratio** (16:10, ultrawide) with no bars or empty edges.
- **Smoothness:**
  - step by real frame time in sub-steps of at most 1/60 s (no judder at 90, 120 or 144 Hz);
  - everything in section 14 (performance).

## 13. Saves and respect for the player

- Save the run or tide in progress, so a reload resumes it instead of restarting. Migrate old saves (one-off purchases become level 1). Make payouts exactly once (open-tide flags so a reload can't pay twice).
- Erase progress needs a second confirm and keeps the volume settings.
- A death costs a bounded amount (Guilt: 40% of carried currency, recoverable) and offers Continue from the last checkpoint.

---

## 14. Performance (no slow patterns, measured on a phone)

A game that runs at 60 fps on a desktop can be unplayable on a phone: a desktop graphics card hides costs that a phone pays in full. Build fast from the start; these are the patterns that make games slow and what to do instead. Most of them are about *repainting things that did not change* and *paying a high cost per object when there are hundreds of objects*.

### Slow patterns to avoid (2D canvas)
| Slow pattern | Why it hurts | Do instead |
| --- | --- | --- |
| Canvas at the full device pixel ratio (up to 3×) | 3× is 9× the pixels of 1×; every fill and sprite costs 9× | Cap the backing store (about 1.5× on phones, 2× on desktop) and step it down by 0.25 when frames run slow; layout and input stay in CSS pixels |
| Redrawing static layers every frame (ground textures, tiled floors, the road, tints, backdrops) | Full-screen fills are the most expensive thing a phone draws, and several layers stack | Paint static layers once into tile canvases (a few hundred pixels square) and stamp them; paint tiles just outside the view ahead, one per frame; keep only animated bits live |
| Redrawing the paused game behind a menu, card pick or dialog | Hundreds of sprites redrawn under a dim overlay that never changes | Copy the canvas once when the menu opens and stamp the copy |
| `shadowBlur`, `filter` (blur, drop-shadow) or large gradients every frame, especially on animated elements | Blur is about the costliest canvas operation; animating size or scale defeats any browser caching | Pre-render glows and soft shadows once per colour and size into small canvases and stamp them |
| `save()` / `restore()` around every sprite | Copies the whole canvas state each time; hundreds per frame | Draw upright sprites straight into their rectangle; undo a flip or rotate transform by hand; reset `globalAlpha` yourself |
| Path fills per object (ellipse shadows, rounded bars, rings) | Each path is rasterized from scratch, hundreds per frame | Stamp a pre-rendered image (shadow ellipse, rounded bar frame and fill) |
| Drawing objects that are off screen | The draw calls still cost, and swarms spawn just off screen | Cull every sprite list (enemies, pickups, shots, particles, numbers) against the view plus a margin |
| Unlimited particles and damage numbers | A big fight spawns thousands; outlined text is expensive | Cap them (a few hundred particles, a few dozen numbers) and drop the oldest |
| Text with outlines redrawn every frame for static labels | `strokeText` with thick round joins is costly | Cache static labels into canvases; only redraw text that changes |
| Every object checking every other object (collision, separation, targeting) | O(n²): 300 enemies is 45,000 pair checks; 300 × probes × 1,400 trees for collision | Spatial grid or hash, rebuilt once a frame; query only nearby cells |
| Allocating closures, arrays or objects per object per frame in hot paths | Garbage-collector pauses show as stutter | Reuse arrays, inline hot loops, avoid callbacks in the innermost query |
| Big sprite sheets uploaded on first use | The first horde or first boss hitches while the GPU uploads | Draw one pixel of each sheet (and any silhouette or tint copy) on the first ready frame |
| Many sounds started per frame | Audio thread overload, crackle and stutter | A voice limit and a per-sound rate limit |

For 3D (Three.js): too many draw calls (use instancing or merged geometry), shadows on everything (shadow-cast only key objects, small shadow maps), full device pixel ratio, uncapped particles, and per-frame geometry or material creation. The same "cache what does not change, cap and cull the rest" rule applies.

### Measure it (before calling a game or big feature done)
- **Simulate a phone:** headless Chromium at a phone landscape size (844×390), `deviceScaleFactor: 3`, `isMobile: true`, and CPU throttling 4× through the DevTools protocol (`Emulation.setCPUThrottlingRate`). Hold the resolution fixed while measuring.
- **Measure the worst case:** the biggest swarm the game can produce, a boss with all effects, and every animated menu or card screen (they are often slower than play).
- **Find the cost, don't guess:**
  - frame time with each draw layer switched off in turn (ground, sprites, shadows, HUD, text, effects); the layer whose removal saves the most is the one to fix;
  - canvas calls per frame (wrap the `CanvasRenderingContext2D.prototype` methods and count `save`, `fill`, `drawImage`, `strokeText` and so on);
  - game-logic milliseconds with 0, 150 and 300 enemies.
  `node ${CLAUDE_SKILL_DIR}/scripts/phone_perf.mjs <url> --setup "<js to reach the worst scene>" --off "<js to switch a layer off>"` does the frame-time, layer and call-count part for any page.
- **Targets on the simulated phone:** median frame at or near 16.7 ms in the worst case, no frames over 50 ms while scrolling onto new ground, game logic under about 2 ms for 300 enemies, and fewer than about 500 `save`/`restore` pairs per frame.

## Done checklist (go through it before saying "done")

- [ ] Camera eases, looks ahead, frames vertically, and reacts (kick, jolt, zoom); the HUD stays still; cutscene feet sit clear of the letterbox.
- [ ] Every hit has hit-stop, flash, recoil and particles scaled to its weight; light comes from shots and hits; VFX are anchored to the sprite.
- [ ] Every new action has its own recorded SFX (list new vs reused), with variation and a voice limit; ambience and music loop cleanly; music ducks and pauses; the boss entrance has a silence-then-theme moment.
- [ ] Every state has a pose; main moves have multi-frame wind-up, impact and follow-through; motion fits the body type; the world idles.
- [ ] Each enemy, boss and item has a unique job, tell and visual; bosses have phases, an intro and a signature mechanic.
- [ ] Each area has its own idea; nothing reads as copy-paste; stand-ins are listed.
- [ ] Scoring rewards skill; a balance sim with weak, average and good bots supports the numbers; nothing takes earned progress.
- [ ] `verify.js` and bot runs pass; a headless walk at desktop and phone sizes shows 0 errors.
- [ ] Performance measured on a simulated phone (section 14): the worst-case scene and every animated menu hold 60 fps or close, and none of the slow patterns in 14 are in the code.
- [ ] Every HUD and UI element animates on enter, change, idle and exit (bars drain with a ghost segment, numbers pop and arc, banners swipe, buttons have all states, transitions instead of cuts), each with its own sound.
- [ ] Painted art and UI kit, bundled fonts, no system-font HUD, no plain rect bars, no emoji icons, no milky white flashes, no circle smoke.
- [ ] Touch, pad and rebindable keys; fullscreen and rotate card; safe areas; fills every aspect ratio.
- [ ] `SPEC.md`, `ART.md` and `AUDIO.md` updated with the real numbers.
