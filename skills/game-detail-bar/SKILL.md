---
name: game-detail-bar
description: The attention-to-detail bar for building any game in any genre - presentation and camera, feedback on every player action, sound and music, animation, content that never repeats, characters and options that each play differently, scoring and balance, testing, art direction, UI and HUD layout that never spills out of its frames, UI motion, input and mobile, saves, performance and working method. Genre guides (action combat, side-view platforming, run-based roguelites, sims and economies, real-time multiplayer) add rules on top when the game fits. Use when pitching, specifying, building, reviewing or reporting on any game or game feature.
---

# Game detail bar

This skill is a quality bar for any game, in any genre. Each rule below is something an AI left out of a game and a
person had to ask for. Example numbers are in [reference.md](reference.md).

**The core rule:** a feature is not done when it works. It is done when it *looks, sounds, moves, reads and balances*
like a finished game. Build all of that in the same turn, not as "polish later".

This file holds the rules that apply to every game. Rules that only make sense for one kind of game live in the genre
guides below. Neither this file nor the guides name or point into any particular game: examples describe a kind of
thing ("a heavy enemy", "a fishing loop"), never a specific title.

## How to use this skill

1. **Pick the genre guides that fit** (table below) and read them too. A game can use several: an online co-op
   roguelite with fighting reads action combat, roguelite runs and real-time multiplayer.
2. **Pitching or speccing:** go through each section here and in the guides, and write the answers into the spec:
   camera plan, feedback per action, SFX list, animation list, what makes each character, option, opponent and area
   different, a scoring and balance model, a UI layout plan for phone and desktop, and a test plan.
3. **Building:** every new action, character, opponent, item, area or menu ships with its own camera, feedback, SFX,
   animation, HUD, layout check and tests, in the same turn.
4. **Before reporting done:** go through the checklist at the bottom and the checklist of every guide you used. In
   the summary, say which SFX are new and which are reused, which checks ran (with their numbers), and what is still
   a stand-in.

## Genre guides

| Guide | Read it when the game has |
| --- | --- |
| [genres/action-combat.md](genres/action-combat.md) | Real-time fighting of any kind: melee, shooting, spells, enemies that attack, bosses |
| [genres/platformer-side-view.md](genres/platformer-side-view.md) | A side view with jumping, ledges and levels the player travels through |
| [genres/roguelite-runs.md](genres/roguelite-runs.md) | Runs built from rooms, floors or waves, random rewards, builds, and progress kept between runs |
| [genres/sim-economy.md](genres/sim-economy.md) | A money or resource loop: days or seasons, shops, upgrades, orders, customers, quotas |
| [genres/multiplayer-realtime.md](genres/multiplayer-realtime.md) | Two or more players in one live game over a network, co-op or versus |

There is no guide yet for puzzle, racing, card, rhythm, turn-based or strategy games; the rules in this file still
apply to them. Add a guide only after shipping that kind of game, from what was actually learned. Never invent one.

---

## 1. Presentation and camera

These apply to any view: a board, a map, a side view, top-down or 3D.

- **Never lock the camera to its target.** Ease toward a target (lerp about 0.1 per frame, or `dt * 6` in seconds),
  with **look-ahead** in the direction of movement or attention. Look further while moving fast, less while the
  player is busy with something precise.
- **The camera reacts to events; the HUD never shakes.**
  - *Trauma shake:* squared trauma that decays every frame; the biggest event wins (`max`, not `+`).
  - *Directional kick:* a small push away from where the event came from, clamped.
  - *Spring jolt:* holds through any freeze, then snaps back with a slight overshoot.
  - *Zoom punch:* a quick scale or FOV change on the biggest moments (a heavy impact, a big catch, a combo clearing
    the board, a landing).
  - *Lean-in:* zoom in a little during a focused moment (a duel, a tense reel, a final move).
- **Portrait or narrow screens get their own framing** (distance, FOV, zoom), not the landscape one squeezed.
- **Scenery between the camera and the focus fades out** (walls, roofs, banners in 2.5D or 3D).
- **Off-screen things that matter get an edge arrow:** the objective, a teammate, a rare find.
- **Slow motion and zoom are rewards:** a perfect move, a final blow, a rare catch, the last piece falling into
  place. Keep them short and earned.
- **Cutscenes:** letterbox bars, the subject framed and clear of the bars at any zoom, and every cutscene skippable
  after it has been seen once.

## 2. Feedback on every player action

- **Every action answers at once in sight, sound and motion**, scaled by its weight: a light tap and a heavy blow,
  a small catch and a huge one, a 3-match and a 6-match each get their own shake, freeze, particle count and sound.
  Never one flat value for everything.
- **Response time is part of the feel.** Measure the time from a key press to the first visible change (a headless
  browser test that presses a key and polls the state). Locally it should be one or two frames; anything a player
  can feel (over about 50 ms) needs fixing. Online games: see the multiplayer guide.
- **Effects are tied to the art.** Trails follow the detected edge of the moving part, smoke leaves the actual
  muzzle, sparks come from the contact point. An effect that floats off the sprite reads as cheap.
- **Particles obey the world:** debris lands and stops, sparks bounce, liquids fade instead of popping, splashes
  only where something meets water, and only when visible.
- **A change of state recolors everything at once:** a power-up, element or upgrade changes trails, flashes, sparks
  and UI accents together.
- **Light:** flashes, impacts and magic briefly light their surroundings; in dark scenes they are the light.
- **Consequences read before they land:** a warning whose length matches the real timing, the same warning language
  everywhere in the game, and the warning code in one place so every source of danger uses it.
- **Input buffer:** a press a little early (about 0.15 s) still counts, exactly once, and a final press never skips
  the ending or reward screen.

## 3. Sound and music

- **UI and HUD count too:** button hover and press, a denied click, panels opening and closing, tabs, sliders, coin
  gain and count-up ticks, purchases, star pops, rank up, records, toasts, timer warnings, title cards, loading done.
  Each gets its own sound *and* its own animation, built together. The full list and the download tool are in the
  `game-asset-pipeline` skill's `sfx-guide.md`.
- **Every new action, opponent action, UI action and prop ships with its own fitting recorded SFX in the same turn.**
  No synth beeps, and no placeholder mix of unrelated samples. Reuse only when it truly fits (a whoosh for a whoosh).
  Prefer real recordings and avoid items marked AI-generated.
- **Document each sound** in `AUDIO.md` (title, author, ID, original bytes, runtime bytes) and the processing: trim
  silence below -50 dBFS, cap the length with a fade, mono 44.1 kHz, normalise per sound, MP3 64 kb/s.
- **Variation:** layer samples per event, pick one of 2 or 3 at random, and add slight pitch jitter so repeats never
  sound the same.
- **Mix discipline:** a global voice limit and a per-sound rate limit; voices and cries only on big events; quieter
  mixes for frequent sounds.
- **Ambience beds** per area or time of day (fire crackle, wind, sea, crowd murmur, crickets), with one-shots spaced
  out.
- **Music:**
  - Loop a section the song itself repeats, never through its outro (find it by matching spectral windows: play the
    intro once, then jump back by the section length).
  - Duck the music for pause, menus and cinematics, and resume from the same position.
  - Pause all audio when the tab is hidden (unless the game must keep running there, as an online host does).
- **Big entrances:** the biggest moment of an area (a boss, a finale, a final round) gets silence first, a scene
  built from sound, then its theme cutting in from its first bar on the title card. After a retry, the theme starts
  at once.
- **iOS/Safari:** unlock audio on the first tap with a silent buffer and resume on return. Sound must never block
  the game from starting.
- Music prompts for a generator give the vibe, the bpm and what the track is for, and ask for an instrumental,
  seamless loop. They never list instruments.

## 4. Animation

- **Several frames per main action** (anticipation, the action, follow-through), not one pose. A chain of three
  different actions gets three different animations.
- **Timing windows match the art:** an action takes effect on the frame where it visibly happens.
- **Every state needs a pose:** idle *breathing*, moving, acting, hurt or failing, celebrating, and a resting end
  state that stays (a knocked-out body, a toppled piece). Single-pose actions settle back to idle after a short
  recovery instead of freezing.
- **Motion by body type, not one wiggle for all:** a fish swings its tail, an eel ripples, a shell barely flexes,
  a heavy thing moves less and later. Movement amplitude scales with size.
- **Idle life in the world:** characters breathe and fidget, props bob, light drifts, background things pass.
- **Turning is smooth:** no instant flips, and a threshold so a character does not turn twice in a fraction of a
  second.
- **Physics where it belongs:** a carried weight swings, a charge draws back before it drives.
- **Draw order:** a held object goes under the holding hand and over the far hand; ground markers and shadows draw
  under characters.
- **Painted frames must agree with each other:** a detail that flips sides between frames of a cycle (a hat tip, a
  scarf end, a charm) flickers in motion. Check every cycle for it and regenerate or drop those frames.

## 5. Content that never repeats

- **Every player option does something new.** An ability, card, unit, tool, tower or piece needs its own verb (a
  turret, a decoy, a dash that leaves a trap, a wave that bounces). A fire version of an ice option is not a new
  option. Keep a written list of the verbs in use and check every new option against it.
- **Playable characters, classes or factions differ in how they play,** not only in stats: each has a few stats, one
  passive rule, a starting set of options and an affinity, and a reason to pick it. Check each one is *fun*, not just
  working: if players enjoy only one of them, give the others the same depth (a combo, a payoff, a second press that
  does something new), not bigger numbers.
- **Opponents and obstacles each have a job and a warning,** not a reskin with more health. A recolored variant is
  fine only with real behaviour changes.
- **Everything has a hook:** a silhouette you know in black, one signature color that pops on the game's backgrounds,
  a personality in the face and stance, and one surprising detail or joke. Typical archetypes (the generic knight,
  the generic skeleton) fall flat.
- **One idea per area, level or stage, and each changes the rules,** not just the look: its own opponents, layout,
  hazards, art and music. An area that reuses the last area's content as stand-ins is a stopgap and is reported as
  one.
- **Big moments change the rules partway through** (a boss phase, a final level, a last round with a twist), not
  only the numbers.
- **Items and upgrades change how you play.** Every one has a rule, not just +x%. Upgrades are visible in the world,
  come in levels, and the strongest lines cost the most.
- **Rarity tiers in fixed code colors** (common green, uncommon blue, rare purple, legendary gold) on everything,
  shown on tiles, cards and badges. Legendaries are strange and visually unique rather than bigger, truly rare, and
  arrive with a shimmer, a sound and a banner.
- **Collections are a goal of their own:** a journal with silhouettes for undiscovered things, flavor text, counts,
  records, and a NEW card with a count-up.
- **Seeded daily or rotating content** is the same on reload, and day or night (or season) variants get their own
  roster, art grade, ambience and music.

## 6. Scoring, economy and balance

- **Score rewards skill:** variety, precision, risk and speed raise it; repetition, mistakes and idling lower it.
  End with a rank and medals.
- **Results screens are mostly pictures:** stars pop in one by one, earnings count up, chips show the bonuses.
- **Goals are told up front** (a goal card at the start, progress in the pause menu, a first-run hint).
- **Model the economy before tuning by feel:** a simulator that plays the real rules with weak, average and good
  bots and prints the numbers that matter (pass rate, money, when each upgrade is owned). Tune to target times.
- **Scale with progress,** so nothing becomes free late.
- **Never take away earned progress.** Prefer optional risk the player chooses (a bonus for speed, a chance at more)
  over mechanics that confiscate what was won.
- **A harder mode is its own track** with its own records, never touching the normal ones.

## 7. Testing and verification

- **A `verify.js` with deterministic checks** for every rule: timing windows, odds tables, payouts exactly once,
  save migration, fairness rules. It grows with each feature (100 to 150 checks for a full game).
- **Bots play the real game** (skilled, average, careless), over several seeds, asserting ranges, not single values,
  with a comment explaining each bound. The genre guides say which bots fit.
- **Headless browser walk** (Playwright, `headless: true`, never a visible window) at 1280×720, 1366×768, 1920×1080
  and a phone landscape such as 844×390: every menu and every mode, 0 page errors. Cover failure paths too: missing or
  corrupt art, an audio timeout, retry.
- **Profile on a simulated phone before handing over** (section 12).
- **QA hooks behind `?qa=1` or typed cheats** (invincible, jump to a level, spawn a given thing), documented and
  gated before release.

## 8. Art direction

- **One coherent direction per game, never code-drawn stand-ins in the final build.** Tell the user what is still a
  stand-in.
- **Contrast:** a readable, colorful hero or focus against a calmer world; characters readable on any background.
- **Atmosphere layers:** parallax, fog, light shafts, floating particles, a vignette, darkness cut by light, a
  time-of-day grade.
- **Characters and world in one rendering style** (pixel on pixel, painted on painted).
- **Making the art:** the `game-asset-pipeline` skill (sheet prompts, generating with an image model, cutting,
  encoding, `ART.md`).
- **Thumbnails are painted covers** (512×512) with one subject, eye contact, a warm accent against a cool background,
  and no text; check them at 128 px.
- **Load smart:** an area's art loads behind a loading screen and is decoded before first draw; later areas load in
  the background once unlocked.

## 9. UI and HUD

### 9a. Look

- **Painted UI kit and bundled fonts, never system fonts or plain rect bars.** 9-slice panels, themed frames, icons
  at native sizes, fonts bundled as woff2 with their license.
- **A HUD that lives:** counters that roll up and bump, a time dial that pulses near the end, a recoverable-damage
  segment on bars, segmented meters, rank badges with their own colors, progress shown as a track with an icon
  instead of a number.
- **Diegetic where possible:** a chalkboard goal in the world, a poster that gets stamped, speech bubbles with a
  patience fuse.
- **Gauges grow out of the thing they measure** (a struggle bar out of the creature, a charge ring around the hand),
  show tick marks, glow in the zone, flash in danger, and shake when the player is losing.
- **Explain before the player commits:** standing at a shop item or a reward shows what it does, what it costs and
  what it replaces.
- **Prompts follow the bindings:** keycaps and tips show the bound key or pad button and switch when a pad is used.
  A full key strip on title and pause screens; keep the bottom edge clear in play.
- **Cards and toasts never block play:** a big card closes on the first press without firing an action; small toasts
  let input through; queued reveals wait their turn and pause their timers in menus.
- **Pause menu:** resume, separate music and SFX sliders (stored apart from the save), key bindings (rebind, swap on
  conflict, reset), how to play, fullscreen, and quit or reset with a confirm where "keep playing" is the default.

### 9b. Layout that never spills out of its frame

UI that leaks over its frame, overlaps other UI or hides under frame art is the most common thing a person has to
point out. Build these in from the start and prove them with screenshots.

- **One content-rect helper for every framed panel.** It takes the panel rectangle and the frame art's border width
  (measured from the art, scaled with the UI) and returns the safe inner rectangle. Titles, text, grids and buttons
  are laid out inside it, never at the frame edge and never on the rim. Footer buttons sit at a fixed offset inside
  the bottom border.
- **9-slice only stretches what can stretch.** Corners keep their size, edges stretch along one axis, the center
  fills. Corner ornaments must never be stretched down a side. When a panel is smaller than two corners, scale the
  corners down evenly instead of overlapping them.
- **Bar fills draw inside the frame's window, on top.** If the frame art has a solid middle, a fill drawn under it
  is invisible (a bar that "looks empty" is usually this). Measure the inner window of the frame art once and fill
  that rectangle, or cut the window out of the art. Check each bar at 0%, 50% and 100%.
- **All text fits its box.** Wrap to the box width; if it still does not fit, shrink toward a minimum readable size
  (about 11 px on phones), then cut with an ellipsis; never let it run past a border or under an icon row. Lay out
  from the longest real string in every language the game ships.
- **Layouts are computed from the content count.** Card rows, grids and lists get their size from how many items
  there are and the screen width; adding a seventh character or a tenth item must not push anything off a panel.
  Below a readable size, switch to more rows or paging instead of shrinking further. Re-check every screen whose
  content count changed.
- **Reserved HUD regions.** Give each kind of HUD element its own region (health top-left, map top-right, banners
  and boss or objective bars top-center, prompts near the player, key strip at the bottom) so they never stack; a
  banner moves other top-center elements aside while it shows.
- **HUD state has an owner and a lifetime.** Every element is cleared by the event that ends it (an area change, the
  end of a run, closing a menu). A bar or prompt that outlives its owner ends up floating over the next screen.
- **Phones get their own layout,** not the desktop one scaled down: bigger touch targets, fewer columns, safe areas
  for notches.
- **Prove it:** headless screenshots of every screen and state at desktop and phone sizes, before and after the
  change, checked for anything crossing a border, overlapping, clipped or too small to read. Report what was checked.

### 9c. Motion (every element moves, with intent)

A static HUD that only changes numbers reads as unfinished. Every HUD element has an enter, a change, an idle and an
exit motion, and each motion pairs with its sound (section 3).

- **Bars:** a lost chunk flashes, holds about 0.3 s, then drains (a "ghost" segment); heals fill with a glow at the
  leading edge; low values pulse; a full meter breathes and pops once when it fills; segmented meters fill segment by
  segment with a tick.
- **Numbers:** they pop in with an overshoot, arc up and fade; size and color differ by kind (critical, blocked,
  heal, miss); several fan out instead of overlapping; always outlined or shadowed for readability.
- **Turns, states and phases:** banners swipe in and out ("Your turn", "Round 2", "Perfect!") with a hold of about
  0.8 s and never block input longer; phase changes get a short screen-wide moment.
- **Buttons and menus:** hover lifts, press sinks, disabled shakes with the denied sound, selected glows; a focus ring
  glides between buttons; panels open with a scale-and-fade overshoot and close faster than they open; lists stagger
  in (30 to 50 ms apart); tabs slide their underline and cross-fade content.
- **Status icons** pop in, tick, blink in their last second and burst when removed; stacks show a count that bumps.
- **Rewards:** count-ups speed up then land with a pop; items fly from where they were won to the inventory; rarity
  reveals build longer and brighter at each tier.
- **Screen transitions:** wipes, fades or an iris between screens, never a hard cut; the HUD slides in at the start
  of play and out at the end.
- **Timing:** UI motion lasts 150 to 300 ms (reveals may run longer); ease-out to enter, ease-in to leave, a small
  overshoot on pops; UI runs on real time so it keeps moving during freezes and slow motion; the HUD never shakes with
  the camera; respect a reduced-motion setting.
- **Verify it:** screenshots or frame strips mid-motion, checking that no animation overlaps, clips off screen or
  hides the action at phone sizes.

## 10. Input, mobile and screens

- **Keyboard first, and every hold action on a key.** Many people play on a laptop touchpad: nothing may need a held
  mouse button, and click is an alternative, never the only way. Controller support (Gamepad API, rumble on big
  events). Every key rebindable, bindings stored in localStorage.
- **Phones:** a thumb stick or pads plus buttons on the other side, each finger tracked on its own; buttons that
  change role in context; touch slop on small buttons; swipeable pages.
- **First tap enters fullscreen and locks landscape** where allowed (or portrait, if that is the game's shape); the
  wrong orientation shows a "turn your phone" card and pauses. Respect notch safe areas.
- **The scene fills every aspect ratio** (16:10, ultrawide, tall phones) with no bars or empty edges.
- **Smoothness:** step by real frame time in sub-steps of at most 1/60 s (no judder at 90, 120 or 144 Hz), and
  everything in section 12.

## 11. Saves and respect for the player

- Save the run, day or level in progress so a reload resumes it. Migrate old saves. Make payouts exactly once (flags,
  so a reload cannot pay twice).
- Erasing progress needs a second confirm and keeps the settings.
- A failure costs a bounded, recoverable amount and offers a continue from the last checkpoint.

---

## 12. Performance (no slow patterns, measured on a phone)

A game that runs at 60 fps on a desktop can be unplayable on a phone: a desktop graphics card hides costs that a phone
pays in full. Build fast from the start; these are the patterns that make games slow and what to do instead. Most of
them are about *repainting things that did not change* and *paying a high cost per object when there are hundreds of
objects*.

### Slow patterns to avoid (2D canvas)
| Slow pattern | Why it hurts | Do instead |
| --- | --- | --- |
| Canvas at the full device pixel ratio (up to 3×) | 3× is 9× the pixels of 1×; every fill and sprite costs 9× | Cap the backing store (about 1.5× on phones, 2× on desktop) and step it down by 0.25 when frames run slow; layout and input stay in CSS pixels |
| Redrawing static layers every frame (ground textures, tiled floors, tints, backdrops) | Full-screen fills are the most expensive thing a phone draws, and several layers stack | Paint static layers once into tile canvases (a few hundred pixels square) and stamp them; paint tiles just outside the view ahead, one per frame; keep only animated bits live |
| Redrawing the paused game behind a menu, card pick or dialog | Hundreds of sprites redrawn under a dim overlay that never changes | Copy the canvas once when the menu opens and stamp the copy |
| `shadowBlur`, `filter` (blur, drop-shadow) or large gradients every frame, especially on animated elements | Blur is about the costliest canvas operation; animating size or scale defeats any browser caching | Pre-render glows and soft shadows once per colour and size into small canvases and stamp them |
| `save()` / `restore()` around every sprite | Copies the whole canvas state each time; hundreds per frame | Draw upright sprites straight into their rectangle; undo a flip or rotate transform by hand; reset `globalAlpha` yourself |
| Path fills per object (ellipse shadows, rounded bars, rings) | Each path is rasterized from scratch, hundreds per frame | Stamp a pre-rendered image (shadow ellipse, rounded bar frame and fill) |
| Drawing objects that are off screen | The draw calls still cost, and swarms spawn just off screen | Cull every sprite list (characters, pickups, shots, particles, numbers) against the view plus a margin |
| Unlimited particles and damage numbers | A big moment spawns thousands; outlined text is expensive | Cap them (a few hundred particles, a few dozen numbers) and drop the oldest |
| Text with outlines redrawn every frame for static labels | `strokeText` with thick round joins is costly | Cache static labels into canvases; only redraw text that changes |
| Every object checking every other object (collision, separation, targeting) | O(n²): 300 objects is 45,000 pair checks | Spatial grid or hash, rebuilt once a frame; query only nearby cells |
| Allocating closures, arrays or objects per object per frame in hot paths | Garbage-collector pauses show as stutter | Reuse arrays, inline hot loops, avoid callbacks in the innermost query |
| Big sprite sheets uploaded on first use | The first swarm or first boss hitches while the GPU uploads | Draw one pixel of each sheet (and any silhouette or tint copy) on the first ready frame |
| Many sounds started per frame | Audio thread overload, crackle and stutter | A voice limit and a per-sound rate limit |

For 3D (Three.js): too many draw calls (use instancing or merged geometry), shadows on everything (shadow-cast only
key objects, small shadow maps), full device pixel ratio, uncapped particles, and per-frame geometry or material
creation. The same "cache what does not change, cap and cull the rest" rule applies. In 3D scenes, never fill the
world with flat billboard grass, trees or shrubs.

### Measure it (before calling a game or big feature done)
- **Simulate a phone:** headless Chromium at a phone landscape size (844×390), `deviceScaleFactor: 3`,
  `isMobile: true`, and CPU throttling 4× through the DevTools protocol (`Emulation.setCPUThrottlingRate`). Hold the
  resolution fixed while measuring.
- **Measure the worst case:** the biggest crowd the game can produce, the busiest effect, and every animated menu or
  card screen (they are often slower than play).
- **Find the cost, don't guess:**
  - frame time with each draw layer switched off in turn; the layer whose removal saves the most is the one to fix;
  - canvas calls per frame (wrap the `CanvasRenderingContext2D.prototype` methods and count `save`, `fill`,
    `drawImage`, `strokeText` and so on);
  - a JavaScript CPU profile (DevTools protocol `Profiler`) to tell game logic from canvas drawing;
  - game-logic milliseconds with 0, 150 and 300 objects.
  `node ${CLAUDE_SKILL_DIR}/scripts/phone_perf.mjs <url> --setup "<js to reach the worst scene>" --off "<js to switch a layer off>"`
  does the frame-time, layer and call-count part for any page.
- **Targets on the simulated phone:** median frame at or near 16.7 ms in the worst case, no frames over 50 ms while
  scrolling onto new ground, game logic under about 2 ms for 300 objects, and fewer than about 500 `save`/`restore`
  pairs per frame.

## 13. Working method

- **Measure before and after, and report the numbers** (frame times, response time, bytes, pass rates). "It feels
  faster" is not a result.
- **Look at it:** screenshot every changed screen and state at desktop and phone sizes before reporting; a passing
  test does not prove that something looks right.
- **Rule out the environment first** when the user says something broke: an old cached build, a server that is down
  or unreachable, a different URL. Check it directly before changing code, and say what was found.
- **Correct earlier claims plainly.** If a previous explanation or recommendation turns out wrong or only partly
  right, say so in the next report.
- **Pitch before building:** design questions get two or three concrete pitches with a recommendation; brainstorms
  stay out of the codebase until one is picked.
- **Report honestly:** what is done, what was tested and how, what is a stand-in, what was not tested (for example
  "not tried on a real phone" or "not tested against the live server").

## Done checklist (go through it before saying "done")

- [ ] Camera eases and reacts (shake, kick, jolt, zoom); the HUD stays still; portrait has its own framing.
- [ ] Every action answers at once with sight, sound and motion scaled to its weight; response time measured;
      effects anchored to the art; warnings match real timings.
- [ ] Every new action has its own recorded SFX (list new vs reused), with variation and a voice limit; ambience and
      music loop cleanly; music ducks and pauses.
- [ ] Every state has a pose; main actions have several frames; cycles have no side-flipping details; the world
      idles.
- [ ] Every option, character, opponent and item has its own verb, job or rule and a hook; each area changes the
      rules; stand-ins are listed.
- [ ] Scoring rewards skill; a bot simulation supports the balance numbers; nothing takes earned progress.
- [ ] `verify.js` and bot runs pass; a headless walk at desktop and phone sizes shows 0 errors.
- [ ] UI: painted kit and bundled fonts; every panel uses the content rect; no text past a border; bars fill inside
      their frames; layouts survive the content count; HUD regions never stack; stale HUD clears; screenshots at
      desktop and phone sizes checked.
- [ ] Every HUD and UI element animates on enter, change, idle and exit, each with its own sound.
- [ ] Touch, pad and rebindable keys, nothing needs a held mouse button; fullscreen and rotate card; safe areas;
      fills every aspect ratio.
- [ ] Performance measured on a simulated phone (section 12): the worst case and every animated menu hold 60 fps or
      close, and none of the slow patterns are in the code.
- [ ] `SPEC.md`, `ART.md` and `AUDIO.md` updated with the real numbers.
- [ ] The checklist of every genre guide used.
