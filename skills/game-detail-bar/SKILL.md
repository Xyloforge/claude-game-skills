---
name: game-detail-bar
description: The attention-to-detail bar for building any game in any genre - presentation and camera, feedback on every player action, sound and music, animation, content that never repeats, characters and options that each play differently, scoring and balance, testing, art direction, UI and HUD layout that never spills out of its frames, UI motion, accessibility, teaching the player, input and rebinding, mobile, simulation timing, seeded randomness and physics, saves and error recovery, performance and working method, for a browser, Godot, Unity or any engine. Genre guides (action combat, side-view platforming, run-based roguelites, sims and economies, real-time multiplayer, open worlds, 3D scenes, voxel worlds) add rules on top when the game fits. Use when pitching, specifying, building, reviewing or reporting on any game or game feature.
---

# Game detail bar

This skill is a quality bar for any game, in any genre. Each rule below is something an AI left out of a game and a
person had to ask for. Example numbers are in [reference.md](reference.md).

**The core rule:** a feature is not done when it works. It is done when it *looks, sounds, moves, reads and balances*
like a finished game. Build all of that in the same turn, not as "polish later".

This file holds the rules that apply to every game. Rules that only make sense for one kind of game live in the genre
guides below. Neither this file nor the guides name or point into any particular game: examples describe a kind of
thing ("a heavy enemy", "a fishing loop"), never a specific title.

**Any engine.** The rules say *what* a finished game does and hold in a browser, Godot, Unity or anything else. Where
the *how* differs, a rule says so: "in a browser" for web games (canvas, WebGL, the DOM), and the engine's own name
(Godot, Unity) for its equivalent. Use the one that matches the game.

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
| [genres/open-world.md](genres/open-world.md) | One large continuous world the player roams freely, far bigger than the screen |
| [genres/3d-scenes.md](genres/3d-scenes.md) | A 3D world of any genre: models, animation, lighting, shadows and 3D performance |
| [genres/voxel-worlds.md](genres/voxel-worlds.md) | A world, characters or props built from blocks, especially with breakable terrain or big crowds |

There is no guide yet for puzzle, racing, card, rhythm, turn-based or strategy games; the rules in this file still
apply to them. Add a guide only after shipping that kind of game, from what was actually learned. Never invent one.

---

## 1. Presentation and camera

These apply to any view: a board, a map, a side view, top-down or 3D.

- **Never lock the camera to its target.** Ease toward a target by `1 - exp(-6 * dt)` of the gap each frame (about
  0.1 at 60 fps; a fixed 0.1 per frame would ease faster on a 144 Hz screen, see section 11), with **look-ahead** in
  the direction of movement or attention. Look further while moving fast, less while the player is busy with
  something precise.
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
  - Pause all audio when the game goes to the background (a hidden browser tab, a minimized window, a paused phone
    app), unless the game must keep running there, as an online host does.
- **Big entrances:** the biggest moment of an area (a boss, a finale, a final round) gets silence first, a scene
  built from sound, then its theme cutting in from its first bar on the title card. After a retry, the theme starts
  at once.
- **Sound must never block the game from starting.** In a browser, audio only starts after a user gesture: unlock it
  on the first tap or key with a silent buffer, and resume the audio context on return (iOS Safari suspends it).
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
- **Smooth comes from consistent frames, not more frames:** frames generated one at a time drift in proportions,
  outline, face and limb length, and large painted sprites show every drift as jitter. Lay each cycle out side by
  side on its foot anchor (and play it in a loop) before using it; regenerate any frame whose silhouette or size
  jumps from its neighbours. About 8 to 12 frames a second is enough when the frames agree, the position moves
  every display frame, and every state change (land, get up, turn, dash) has its own in-between frames instead of a
  snap.

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
- **An automated walk through every menu and mode** at 1280×720, 1366×768, 1920×1080 and a phone landscape such as
  844×390, with 0 errors, and screenshots of each screen. Cover failure paths too: missing or corrupt art, an audio
  timeout, retry, an error thrown mid-play (section 12).
  - In a browser: Playwright with `headless: true`, never a visible window.
  - Godot: run scenes and tests from the command line with `godot --headless` (a test framework such as GUT or
    GdUnit4), and capture screenshots from the viewport in a windowed run at each size.
  - Unity: Test Runner play-mode tests, run from the command line with `-batchmode -runTests -testPlatform
    PlayMode`, and screenshots from a play-mode test at each resolution.
- **Profile on a phone before handing over** (section 13).
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
- **Cover and store art is painted key art** with one subject, eye contact, a warm accent against a cool background,
  and no small text. Make it at every size the game is listed at (a web portal tile, an itch.io cover, Steam
  capsules, a phone store icon), recompose rather than crop for very wide or very tall shapes, and check each one at
  the smallest size it is shown (often about 128 px or less).
- **Load smart:** an area's art loads behind a loading screen and is decoded before first draw; later areas load in
  the background once unlocked.
- **Every frame name exists.** A missing frame usually draws nothing and raises no error, so a character blinks out
  on one step of a cycle or vanishes in one pose. Check every frame name used in code and data against the sheets as
  part of the build, and in play log one warning per unknown name instead of failing silently. Never reference a
  frame that has not been drawn yet; reuse an existing one until it is.

## 9. UI and HUD

### 9a. Look

- **Painted UI kit and bundled fonts, never system fonts or plain rect bars.** 9-slice panels, themed frames, icons
  at native sizes, fonts bundled with the game with their license (woff2 in a browser).
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
  On touch, no keyboard keys anywhere: prompts drop their keycap and any key-based text ("press K again") gets touch
  wording ("tap the spell button again").
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
- **Framed panels resize without smearing their art.** Corners and every ornament along an edge (a gem, a crest, a
  spike) keep their size; only the plain parts between them grow, patterned edges repeat instead of stretching, and
  the center fills. Decoration can sit anywhere on the frame. A panel smaller than its corners scales down evenly
  instead of overlapping them. UI that never resizes (a title frame) can be one fixed image; ornaments that animate
  are separate sprites placed on the frame.
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

### 9d. Accessibility

Players with low vision, colour blindness, motion sickness, photosensitivity, hearing loss or limited hand use are a
large share of any audience. These settings cost little when built in from the start.

- **Never colour alone.** Every meaning carried by colour (a telegraph, a team, rarity, a status, a correct or wrong
  answer) also has a shape, an icon, a pattern or a word. Check the main screens under the three common colour-vision
  deficiencies (protanopia, deuteranopia, tritanopia): in a browser, the DevTools protocol does this headlessly with
  `Emulation.setEmulatedVisionDeficiency`; in an engine, run the test screenshots through a colour-blindness
  simulation (an image tool, or a full-screen filter shader behind the QA flag).
- **Readable text:** at least 4.5:1 contrast against what is behind it (a plate or outline over a busy scene), a text
  size setting with at least three steps that the layout rules in 9b survive, and no text that disappears before it
  can be read: dialogue and tips advance on a press, or stay long enough.
- **Motion and flashes:** a screen shake slider (0 to 100%), a reduced flashes option, and a reduced motion option
  that tones down camera kicks, zoom punches and UI overshoot (in a browser, default it from
  `prefers-reduced-motion`). Never more than three full-screen flashes in one second.
- **Sound has a picture:** subtitles for all speech, with the speaker's name, and captions or an on-screen cue for
  sounds that carry information (danger behind the player, a timer about to end, an enemy off screen).
- **Hands:** every hold action can be switched to a toggle, every control is rebindable (section 10), nothing needs
  fast repeated mashing without an option to hold instead, and touch targets are at least about 44 px.
- **An assist option** in games with hard timing (slower game speed, more health, wider windows, or skipping a
  section), offered plainly without shaming the player. Assisted results keep their own records, like a harder mode.
- **Settings are reachable before play** (on the title screen as well as in pause), stored with the other settings
  apart from the save, and shown as a preview while changing them.

### 9e. Teaching the player (the first minutes)

Most players who leave do it in the first minutes, usually because they did not understand what to do or why they
failed. Teaching is part of the game, built with it, not a manual added at the end.

- **Playing within seconds:** one or two presses from the title to control, no account or settings screens first,
  and any story intro short and skippable.
- **Teach by doing, one thing at a time.** Each new verb first appears where it is the only thing needed and failing
  costs nothing, then is asked for under light pressure, then combined with what the player already knows
  (introduce, test, twist). Never teach two new things in the same moment.
- **Prompts in the world, not text walls:** one short line next to where it matters, showing the bound key or the
  touch button (9a). A prompt disappears when the player has done the thing, not after a timer, and comes back if
  the player seems stuck (no progress for a while).
- **The first failures are gentle and explain themselves:** early mistakes cost little, a retry is instant, and the
  fail screen names the cause with one tip that fits it ("the red ring means dodge, not block").
- **New things are taught when they are first met,** later in the game too: a first-time card or a short coach
  moment for a new enemy type, item or mechanic, not everything at the start.
- **Once per player, always replayable:** tutorials and first-time cards are remembered with the settings, skippable
  for returning players, and a how-to-play page with pictures sits in the pause menu.
- **Prove it:** a run from a fresh profile (cleared storage or save folder) reaches real control in seconds and
  shows every first-time prompt exactly once; then watch one person who has never seen the game play it without
  help, and note every place they stop, guess or fail without knowing why.

## 10. Input, mobile and screens

- **Keyboard first, and every hold action on a key.** Many people play on a laptop touchpad: nothing may need a held
  mouse button, and click is an alternative, never the only way. Controller support (rumble on big events; in a
  browser, the Gamepad API).
- **Game code reads actions, never raw keys.** A binding table maps keys, mouse buttons, pad buttons and touch buttons
  to named actions (move, jump, attack, interact, pause), and gameplay asks only about actions. Rebinding, pads,
  touch and the key prompts in 9a all work from that one table.
- **Press, hold and release are different questions.** A press fires once, on the frame the button goes down, and
  never repeats while held unless the action is meant to repeat; a hold is read every step; a release ends charges.
  Record presses as they arrive and hand them to the next game step, so a tap shorter than one step is never lost and
  never counted twice (this matters with the fixed step in section 11).
- **Every key and button rebindable:** press the new key to bind it, Escape cancels, a key already in use offers to
  swap, one button resets to defaults, mouse and pad buttons rebind too, and the bindings are saved by action name
  with the settings. Bind physical keys (in a browser, `KeyboardEvent.code`) so the same positions work on any
  keyboard layout, and show the player's own key label in prompts (`navigator.keyboard.getLayoutMap()` where the
  browser has it).
- **Analog and diagonal movement:** sticks get a circular deadzone (about 0.15 to 0.2) with the rest of the range
  rescaled to start from zero, so slow movement is smooth; keyboard diagonals are normalized so they are not faster
  than straight lines.
- **Nothing stays stuck:** when the window loses focus or the app goes to the background, every held input is
  released (the key-up never arrives) and the game pauses.
- **Phones:** a thumb stick or pads plus buttons on the other side, each finger tracked on its own; buttons that
  change role in context; touch slop on small buttons; swipeable pages.
- **Touch buttons carry the state the desktop bar showed** (cooldown sweep, charges, meter rings, a recast glow), and
  the desktop slot bar hides: it duplicates the buttons and sits under a thumb. Context buttons (use, talk, open)
  appear and glow only when something is in reach. An on-screen pause button, with the other corner HUD stepping
  aside for it. Any physical key switches to keyboard mode and any touch switches back.
- **The game owns the screen:** fullscreen and the game's orientation (landscape, or portrait if that is its shape),
  notch safe areas respected, and a Fullscreen On/Off setting. A native or engine build sets these in its export or
  player settings. In a browser, the first tap enters fullscreen and locks the orientation where allowed;
  fullscreen comes back on the next tap after the player swipes out (on by default for phones); the setting hides
  where the browser has no element fullscreen; and the wrong orientation shows a "turn your phone" card and pauses
  (an online host keeps running for its guests).
- **The scene fills every aspect ratio** (16:10, ultrawide, tall phones) with no bars or empty edges.

## 11. Simulation timing and physics

A game whose logic steps by the frame time plays differently on a 60 Hz phone and a 144 Hz monitor: jumps reach a
different height, fast objects pass through walls, and bots and replays stop being repeatable.

- **Game logic and physics run at a fixed step** (usually 60 a second): each frame adds the real elapsed time to an
  accumulator and runs as many fixed steps as fit. Use the engine's own fixed step where it has one (Godot
  `_physics_process`, Unity `FixedUpdate`); in a browser loop, write the accumulator yourself.
- **Drawing interpolates** between the previous and the current step by the leftover fraction, so motion is smooth on
  any refresh rate and never judders at 90, 120 or 144 Hz.
- **Cap the steps per frame** (about 5) and drop the remaining time after a long stall (returning to a hidden tab, a
  loading hitch), so the game never tries to catch up on seconds of simulation at once.
- **Everything outside the fixed step uses real time:** easing by `1 - exp(-k * dt)` instead of a fixed fraction per
  frame, timers and cooldowns in seconds, never in frames.
- **Hit-stop and slow motion scale the simulation's time,** while UI and menus run on real time (9c).
- **Fast objects never pass through walls.** A small object moving more than about half the thickness of the thinnest
  wall in one step can skip past it. Cap speeds, trace a ray or sweep from the previous to the new position for
  bullets and thrown things, turn on the engine's continuous collision for fast bodies, and keep walls thicker than
  one step of the fastest object.
- **Stable physics:** connected or stacked bodies within about 10:1 of each other's mass, angle limits on every joint
  of a ragdoll or chain, more solver iterations (not a smaller step) when stacks jitter, and resting bodies allowed to
  sleep.
- **Seeded randomness.** Every gameplay choice (spawns, loot, damage rolls, level layout, enemy decisions) draws from
  one seeded generator passed to the code that needs it, never from the global one (`Math.random()` in a browser,
  `UnityEngine.Random` in Unity, the global `randf()` in Godot). Use a small seedable generator in a browser
  (mulberry32 or sfc32), a seeded `RandomNumberGenerator` in Godot, and `System.Random` or
  `Unity.Mathematics.Random` with a seed in Unity.
  - Cosmetic randomness (particles, idle fidgets, sound pitch jitter) uses a separate generator, so changing an
    effect never changes what drops.
  - The run's seed and the generator's current state go into the save, so reloading cannot re-roll a reward.
  - Daily content takes its seed from the date in UTC, so every player gets the same day.
  - The seed shows in the QA overlay and bug reports, and a QA option starts a run from a given seed.
- **Prove it:** run the same inputs at a forced 30, 60 and 144 frames a second and compare the results (jump height,
  distance run, a projectile's path, a bot's score); they match within a small tolerance. The same seed and inputs
  give the same run every time, and bots run faster than real time with the same results.

## 12. Saves and respect for the player

- Save the run, day or level in progress so a reload resumes it. Make payouts exactly once (flags, so a reload cannot
  pay twice).
- **Save plain data, never live objects:** each system writes its own part of one versioned object (`{ version: 3,
  ... }`) of numbers, strings, lists and ids, and loading rebuilds the objects from it.
- **Every save has a version, and old versions migrate:** one small function per version step (2 to 3, 3 to 4), run
  in order on load. Keep a sample save from every released version and load each one in `verify.js`.
- **A broken save never loses progress:** write the new save before replacing the old one (a temporary file renamed
  over it, or two alternating slots in browser storage) and keep the previous one as a backup. On load, if the save
  does not parse or fails its checks, load the backup and tell the player; never crash and never silently start a
  new game.
- **Check what loads:** types, ranges, and ids of content that no longer exists (dropped or replaced with something
  fair). Players edit saves.
- **Storage can fail:** in a browser, `localStorage` throws in some private modes and when full, and can be cleared by
  the browser; on desktop and phones, write into the platform's user data folder (Godot `user://`, Unity
  `Application.persistentDataPath`). Catch every failure, keep playing, and show a small notice that progress is not
  being saved.
- **When to save:** at checkpoints, right after rewards and purchases, when the player pauses or quits, and when the
  game goes to the background (in a browser, `visibilitychange` and `pagehide`; on phones, the app pause event). An
  autosave runs at most every few seconds, never every frame, and shows a small saving icon.
- **Long games get slots,** each showing where the player is, time played and when it was saved.
- **Settings are stored apart from progress,** so erasing or losing a save keeps them.
- **An error never freezes the game or costs the save.**
  - Catch what escapes: in a browser, `window.onerror` and `unhandledrejection`; in Unity,
    `Application.logMessageReceived` for exceptions; in Godot, a script error aborts only the function it happened
    in and the game runs on, so watch the error output in tests and guard the code that must finish (saving, scene
    changes).
  - Show a friendly card in the game's own style with "try again" and "back to menu", never a frozen frame, a blank
    screen or a raw stack trace. A failed download or load gets the same card with a retry.
  - Never write a save from a state that just failed; the last good save stays (saves happen before risky moments
    such as a scene change).
  - Log the details for a bug report (message, stack, game version, scene, seed, recent actions) and offer a "copy
    details" button on the card.
  - Test it: throw an error on purpose in an update, in a scene change and while loading (behind the QA flag), and
    check that the card shows, the game recovers and the save is intact.
- Erasing progress needs a second confirm and keeps the settings.
- A failure costs a bounded, recoverable amount and offers a continue from the last checkpoint.

---

## 13. Performance (no slow patterns, measured on a phone)

A game that runs at 60 fps on a desktop can be unplayable on a phone: a desktop graphics card hides costs that a phone
pays in full. Build fast from the start; these are the patterns that make games slow and what to do instead. Most of
them are about *repainting things that did not change* and *paying a high cost per object when there are hundreds of
objects*.

### Slow patterns in any engine
| Slow pattern | Why it hurts | Do instead |
| --- | --- | --- |
| Drawing or updating objects that are off screen | The draw calls and updates still cost, and swarms spawn just off screen | Cull every list (characters, pickups, shots, particles, numbers) against the view plus a margin; far objects update less often |
| Unlimited particles and damage numbers | A big moment spawns thousands; outlined text is expensive | Cap them (a few hundred particles, a few dozen numbers) and drop the oldest |
| Every object checking every other object (collision, separation, targeting) | O(n²): 300 objects is 45,000 pair checks | Spatial grid or hash, rebuilt once a frame; query only nearby cells |
| Allocating objects, arrays or closures per object per frame in hot paths | Garbage-collector pauses show as stutter (JavaScript, C#, GDScript arrays and dictionaries alike) | Reuse arrays and temporary vectors, pool objects that come and go (shots, particles, enemies), inline hot loops |
| Creating and destroying objects all the time | Spawning a node, GameObject or sprite is far more costly than moving one | Pool them: hide and reuse instead of destroy and create |
| Looking things up every frame | Finding nodes or components by name or type in every update is slow | Look them up once and keep the reference |
| One-time work done the first time it is needed (decoding art, building caches or tinted copies, compiling shaders, decoding sounds, loading fonts, filling pools) | The first hit, effect, enemy type, boss or area hitches mid-play, often for 100 ms or more | Do it ahead, behind a loading screen, a menu or a transition, and check the warm-up really did the work: a token warm-up (a tiny draw, a muted play) can look done while the real cost still waits |
| Too much decoded art held at once | A decoded image costs width × height × 4 bytes whatever its file size (a 2048 × 2048 atlas is 16 MB); phone browsers reload or kill the tab at roughly 200 to 300 MB, and phone apps get killed too | Add up the decoded size of every atlas; under about 150 MB load it all up front; above that, load per level or area, prefetch the next one behind play, and release the rest. GPU-compressed textures (see the 3D guide, or the engine's texture import settings) cut it by 4 to 8 times |
| Rendering at the full device resolution | A phone at 3× pixel density draws 9× the pixels of 1× | Cap the render resolution on phones (about 1.5×) and lower it further when frames run slow; keep UI sharp at native resolution |
| Many sounds started per frame | Audio thread overload, crackle and stutter | A voice limit and a per-sound rate limit |

### In a browser (2D canvas)
| Slow pattern | Why it hurts | Do instead |
| --- | --- | --- |
| Canvas at the full device pixel ratio (up to 3×) | Every fill and sprite costs 9× at 3× | Cap the backing store (about 1.5× on phones, 2× on desktop) and step it down by 0.25 when frames run slow; layout and input stay in CSS pixels |
| Redrawing static layers every frame (ground textures, tiled floors, tints, backdrops) | Full-screen fills are the most expensive thing a phone draws, and several layers stack | Paint static layers once into tile canvases (a few hundred pixels square) and stamp them; paint tiles just outside the view ahead, one per frame; keep only animated bits live |
| Redrawing the paused game behind a menu, card pick or dialog | Hundreds of sprites redrawn under a dim overlay that never changes | Copy the canvas once when the menu opens and stamp the copy |
| `shadowBlur`, `filter` (blur, drop-shadow) or large gradients every frame, especially on animated elements | Blur is about the costliest canvas operation; animating size or scale defeats any browser caching | Pre-render glows and soft shadows once per colour and size into small canvases and stamp them |
| `save()` / `restore()` around every sprite | Copies the whole canvas state each time; hundreds per frame | Draw upright sprites straight into their rectangle; undo a flip or rotate transform by hand; reset `globalAlpha` yourself |
| Path fills per object (ellipse shadows, rounded bars, rings) | Each path is rasterized from scratch, hundreds per frame | Stamp a pre-rendered image (shadow ellipse, rounded bar frame and fill) |
| Text with outlines redrawn every frame for static labels | `strokeText` with thick round joins is costly | Cache static labels into canvases; only redraw text that changes |

### In an engine (Godot, Unity)
| Slow pattern | Why it hurts | Do instead |
| --- | --- | --- |
| Sprites from many separate textures | Each texture change breaks a batch and adds a draw call | Pack sprites that draw together into atlases (Unity Sprite Atlas; Godot batches 2D items that share a texture and material) |
| Thousands of objects each running their own per-frame update | Per-object update calls (`_process`, `Update`) add up long before the work inside them does | One manager loops over plain data for crowds, bullets and particles; turn processing off on objects that are idle or far away |
| Physics bodies on decoration | Every body costs in the physics step even when nothing touches it | Colliders only on what gameplay needs; static bodies for walls; simple shapes (circles, boxes, capsules) instead of polygons |
| Large transparent layers stacked on screen | Overdraw: phones pay for every pixel of every layer | Trim transparent sprites tight, avoid full-screen transparent overlays, use opaque materials where possible |
| Full-screen effects left at desktop settings | Glow, blur and anti-aliasing passes cost the most on phones | A quality setting with lower presets for phones, chosen by default on them |

### Loading (the first screen shows fast)

- **Menu first, game after.** Only what the title screen or menu needs (its code, UI art, fonts, menu music) loads
  first. The game's code and art load behind the menu while the player reads it, and anything still missing loads
  behind a short loading screen when they press play. A player sees a working menu within a second or two on a
  phone, never a blank screen while the whole game loads. In an engine, keep the first scene small and load the
  rest in the background (Godot `ResourceLoader.load_threaded_request`, Unity asynchronous scene loading or
  Addressables).
- **One packed data file.** All game data (levels, items, enemies, abilities, dialogue, balance numbers) ships as one
  file, not dozens of small ones read at startup: in a browser, one request, compressed by the server, parsed once,
  with a version in its URL so it can be cached for a long time and an update is picked up at once; in an engine,
  resources inside the game package rather than loose files. Art stays in atlases for the same reason.

3D games: read [genres/3d-scenes.md](genres/3d-scenes.md) (draw calls, shadows, texture compression, shader
warm-up, 3D measurement).

### Measure it (before calling a game or big feature done)
- **Measure on a phone:**
  - In a browser, simulate one: headless Chromium at a phone landscape size (844×390), `deviceScaleFactor: 3`,
    `isMobile: true`, and CPU throttling 4× through the DevTools protocol (`Emulation.setCPUThrottlingRate`). Hold
    the resolution fixed while measuring.
  - In an engine, run a development build on a real low-to-mid phone with the profiler attached (Godot remote
    debugging with the Profiler and Monitors; Unity Profiler attached to a Development Build). A desktop gives no
    reliable phone simulation for native builds.
- **Read frame time, not FPS.** The frame rate is capped at the screen's refresh rate (60, 120 or 144 Hz), so two
  versions that both show "60 FPS" can differ several times over in cost; the cheaper one just idles longer. Compare
  milliseconds of work per frame, the worst frame, draw calls and triangles, and push the load up until the cap
  breaks to find the real headroom.
- **A live readout behind the QA flag:** frame time, worst frame in the last half second, draw calls, triangles or
  sprites, and object counts.
- **Measure the worst case:** the biggest crowd the game can produce, the busiest effect, and every animated menu or
  card screen (they are often slower than play).
- **Find the cost, don't guess:**
  - frame time with each draw layer switched off in turn; the layer whose removal saves the most is the one to fix;
  - draw calls per frame: in a browser, wrap the `CanvasRenderingContext2D.prototype` methods and count `save`,
    `fill`, `drawImage`, `strokeText` and so on (or read `renderer.info` in three.js); in Godot, the draw call
    monitors; in Unity, the Frame Debugger and the Stats panel;
  - a CPU profile to tell game logic from drawing (the DevTools protocol `Profiler` in a browser, the engine
    profiler elsewhere);
  - game-logic milliseconds with 0, 150 and 300 objects.
  In a browser,
  `node ${CLAUDE_SKILL_DIR}/scripts/phone_perf.mjs <url> --setup "<js to reach the worst scene>" --off "<js to switch a layer off>"`
  does the frame-time, layer and call-count part for any page.
- **Find stutter, not only slowness:** report the 99th percentile and the worst frame, not just the median; a smooth
  median with one 150 ms frame still feels broken. Time every game function and keep the top few for each frame over
  about 35 ms, so a spike names its cause. Measure from a fresh start and watch every "first" (first hit, first
  status effect, first enemy type, first boss, first new area): one-time costs never show on a warmed-up run.
- **Targets on the phone:** median frame at or near 16.7 ms in the worst case, no frames over 50 ms while moving onto
  new ground or meeting anything for the first time, and game logic under about 2 ms for 300 objects. In a browser,
  fewer than about 500 `save`/`restore` pairs per frame; in an engine, draw calls in the low hundreds at most.

## 14. Working method

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
      idles; every frame name used in code and data exists in the art.
- [ ] Every option, character, opponent and item has its own verb, job or rule and a hook; each area changes the
      rules; stand-ins are listed.
- [ ] Scoring rewards skill; a bot simulation supports the balance numbers; nothing takes earned progress.
- [ ] `verify.js` and bot runs pass; an automated walk at desktop and phone sizes shows 0 errors.
- [ ] UI: painted kit and bundled fonts; every panel uses the content rect; no text past a border; bars fill inside
      their frames; layouts survive the content count; HUD regions never stack; stale HUD clears; screenshots at
      desktop and phone sizes checked.
- [ ] Every HUD and UI element animates on enter, change, idle and exit, each with its own sound.
- [ ] Accessibility: nothing carried by colour alone (checked under colour-blind simulation); text contrast and size
      setting; shake, flash and motion settings; subtitles and cues for important sounds; hold-to-toggle; an assist
      option where timing is hard; settings reachable from the title screen.
- [ ] Teaching: control within seconds of the title; one new thing at a time, taught by doing; prompts leave when
      done and return when stuck; fail screens name the cause; first-time cards once per player; checked from a
      fresh profile and by watching one new player.
- [ ] Touch, pad and rebindable keys, nothing needs a held mouse button; gameplay reads actions from one binding
      table; presses fire once; rebinding swaps conflicts and resets; deadzone and normalized diagonals; inputs
      release on focus loss; no keyboard keys shown on touch; touch buttons show cooldowns and charges; on-screen
      pause; fullscreen (re-entered, with a setting) and rotate card; safe areas; fills every aspect ratio.
- [ ] Logic and physics on a fixed step with interpolated drawing; results match at 30, 60 and 144 fps; fast objects
      cannot pass through walls; gameplay randomness comes from a seeded generator kept apart from cosmetic
      randomness, saved with the run, so the same seed and inputs replay the same run.
- [ ] Saves are versioned plain data with migrations tested from every old version, a backup on a broken save, a
      notice when storage fails, and saves on checkpoints, rewards, pause and going to the background.
- [ ] Errors: a thrown error, a failed load and a broken scene change each show a friendly card with retry and
      leave the save intact (tested on purpose).
- [ ] Performance measured on a phone (section 13; simulated in a browser, a real device for engine builds): the
      worst case and every animated menu hold 60 fps or close, the worst frame from a fresh start is reported, and
      none of the slow patterns are in the code.
- [ ] The menu shows before the game code and art finish loading; game data ships as one packed file.
- [ ] `SPEC.md`, `ART.md` and `AUDIO.md` updated with the real numbers.
- [ ] The checklist of every genre guide used.
