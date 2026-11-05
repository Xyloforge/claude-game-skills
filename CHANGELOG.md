# Changelog

The plugin tracks commits on `main`; notable changes are listed here by date.

## 2026-11-05

- **New genre guide `voxel-worlds.md`:** block grid and coordinate conventions, face culling, greedy meshing, baked
  per-vertex ambient occlusion, padded atlas tiles, chunk rebuilds (off the main thread when large), grid (DDA) ray
  casts and per-axis box collision with step-up, walkable maps and flow fields that update when blocks break,
  destruction and instanced debris, instanced rigid-part crowds with outfits and gore from the model's own colours,
  first-person voxel weapons with arms aimed at an off-screen elbow and keyframed reloads, the voxel art pipeline and
  budgets.
- **Measuring (core section 13):** read frame time, not FPS, since the refresh rate caps FPS; build a live readout, a
  low/high detail toggle and a stress key into the game behind the QA flag.
- **3D scenes:** crowds from instanced rigid parts or shader-baked animation instead of one skinned mesh each, small
  lights faked with emissive meshes and glow decals, and a new first-person view part (own render pass, matched
  lighting, arms always joined to the body, sway, bob, recoil, draw and casings).

## 2026-11-02

- **Reference images in art prompts** (`game-asset-pipeline/art-prompts.md`): use a reference whenever one helps,
  since models follow a picture better than words for framing, angle, size and layout; turn a reference from another
  game or a photo into a plain layout guide (measured flat shapes) so the model copies the composition, not the art;
  bordered screen-shaped frames for art that must meet the screen edges; and on refusals or repeated misses, ask the
  user for a reference or give them the prompt for another tool instead of rewording around the filter.
- **Any engine:** `game-detail-bar` and `game-asset-pipeline` now say what to do in a browser, Godot and Unity
  wherever the how differs:
  - automated walks and screenshots (Playwright, `godot --headless` with GUT or GdUnit4, Unity Test Runner);
  - performance split into patterns for any engine, browser canvas patterns, and engine patterns (atlases and
    batching, per-object updates, physics on decoration, overdraw, effect presets), with measurement on a real
    phone through the engine profiler for native builds;
  - menu-first loading and packed data for engines, audio unlock and fullscreen as browser notes, backgrounding in
    general terms;
  - art standard for engine builds (lossless masters, engine texture compression; download budgets only for web);
  - UI frames with Godot and Unity 9-slice and fixed-span drawing;
  - multiplayer testing with several instances of any kind.
- Cover and store art at every size the game is listed at, instead of a single 512 px thumbnail.
- New core part **9e teaching the player**: control within seconds, teach by doing one thing at a time, prompts that
  leave when done and return when stuck, fail screens that name the cause, first-time cards later in the game,
  fresh-profile and new-player checks.
- **Seeded randomness** in section 11: one seeded generator for gameplay (per engine), a separate one for
  cosmetics, state saved with the run, daily seeds in UTC, seed shown and replayable in QA.
- **Errors never freeze the game** in section 12: catching what escapes (per engine), a friendly card with retry,
  no save from a failed state, details for bug reports, tested on purpose.
- New **3D scenes** genre guide: model conventions and budgets, GPU texture compression and colour spaces, loading
  with shader warm-up and freeing memory, animation blending and layers, a small light rig with baked light and
  tone mapping, tight shadows with contact shadows, transparency and readability, draw calls and 3D measurement.

- `game-detail-bar` core rules, written for any engine with browser notes where they differ:
  - New **simulation timing and physics** section: a fixed step with an accumulator and interpolated drawing, a cap
    on catch-up steps, real-time easing and timers, time scale for hit-stop, no tunneling (speed caps, sweeps,
    continuous collision), stable joints and stacks, and a 30/60/144 fps comparison test. The camera ease in
    section 1 is now frame-rate independent.
  - **Saves** expanded: plain versioned data, migrations tested from every old version, a backup when a save is
    broken, load checks, storage failures, when to save, slots, settings kept apart.
  - New **accessibility** part (9d): never colour alone (with colour-blind simulation), contrast and text size,
    shake/flash/motion settings and the three-flashes rule, subtitles and sound cues, hold-to-toggle, assist
    options, settings before play.
  - **Input** expanded: gameplay reads actions from one binding table, press/hold/release with presses handed to
    the fixed step, a full rebinding flow on physical keys, stick deadzone and normalized diagonals, inputs released
    on focus loss.
  - Sections renumbered: simulation is 11, saves 12, performance 13, working method 14. Done checklist updated.
- `game-detail-bar` action combat guide: **how enemies think**: named states with enter and exit cleanup, noticing
  before chasing, attack tokens, steering, A\* or flow-field paths re-planned a few times a second, slower thinking
  than moving, behaviour trees or utility scores only when needed, a debug view.

- `game-detail-bar`: new **open worlds** genre guide: the world split into chunks that own their contents, chunk
  culling against the view and a view distance, streaming chunks in ahead and freeing them behind, and instanced
  drawing of repeated objects per chunk.
- `game-detail-bar` real-time multiplayer guide: frequent messages (snapshots, inputs) are sent as binary with one
  shared layout instead of JSON.
- `game-detail-bar` core rules: a new loading part in performance: the menu shows first while the game loads behind
  it, and game data ships as one versioned packed file instead of many small fetches. Done checklist updated.

## 2026-10-30

- `game-asset-pipeline`: new **UI frames** guide and `slice_frame.py`. Frames can be decorated anywhere, not only in
  the corners: the tool finds corners, ornaments along each edge (by shape and by colour) and repeating edge
  patterns, and writes a layout where ornaments keep their size and only the plain spans between them grow (tiled
  when patterned). Includes the UI kit prompt wording, a canvas `drawFrame` that matches the tool's preview, the CSS
  `border-image` case, and when to use overlays or a fixed image instead. `game-detail-bar` UI layout rule updated
  to match.
- `game-detail-bar` core rules: smooth animation comes from frames that agree with each other (check each cycle side
  by side on its anchor, regenerate frames that jump), 8 to 12 frames a second with per-frame movement and
  in-between frames for state changes; decoded art memory budget (width × height × 4), with per-level loading only
  above about 150 MB.

## 2026-10-29

- `game-detail-bar` core rules: every frame name must exist (a missing frame silently draws nothing); first-time
  costs (decoding art, building caches or tinted copies, shaders, sounds, fonts, pools) happen behind a loading
  screen, menu or transition, replacing the old "draw one pixel of each sheet" advice; stutter is measured by the
  worst and 99th-percentile frames from a fresh load, with each long frame naming its cause; touch shows no keyboard
  keys, touch buttons carry cooldowns and charges, an on-screen pause; fullscreen comes back after a swipe out, with a
  setting. Done checklist updated to match.
- `game-detail-bar` split into **core rules for every game** (`SKILL.md`) and **genre guides** (`genres/`): action
  combat, side-view platforming, run-based roguelites, sims and economies, real-time multiplayer. Combat, platforming
  and economy rules that only fit one kind of game moved out of the core into their guides.
- New core rules: response time as part of feel, every player option has its own verb, characters that differ in how
  they play (and are fun, not just working), a hook for everything, side-flipping details in animation cycles, and a
  working-method section (measure, look at it, rule out the environment, correct earlier claims).
- New **UI layout** section: one content-rect helper per framed panel, 9-slice that never stretches corners, bar
  fills inside the frame window, text that always fits, layouts computed from the content count, reserved HUD
  regions, HUD state with an owner and a lifetime, screenshots at desktop and phone sizes.
- New **real-time multiplayer** guide: choosing a netcode model, each player owning their character with actions sent
  to the host, health and takeovers, move counters, interpolation buffers, feedback routing without echoes, co-op
  design, protocol versions, hidden host tabs, lag-proxy testing, troubleshooting and next steps.
- `reference.md`: example numbers grouped by kind of game with no titles or character names; new online co-op and
  UI numbers.
- `game-asset-pipeline`: written for any image model (pasted by hand or generated from the command line), new effect
  sheets on black and a command-line generation section; hard-coded `~/.claude/skills` paths replaced with
  `${CLAUDE_SKILL_DIR}`; personal anecdotes removed.
- `tools/validate.mjs`: rejects private wiki links, `~/.claude/skills` paths and home-folder paths in skills.

## 2026-10-27

- First public release as a Claude Code plugin marketplace (`game-skills@xyloforge-game-skills`).
- `game-detail-bar`: new **Performance** section: the coding patterns that make 2D canvas games slow on phones
  (full device-pixel-ratio canvases, repainting static layers, per-frame blur, save/restore per sprite, path fills
  per object, no culling, uncapped particles, O(n²) collision, first-use sheet uploads, unthrottled sounds), what
  to write instead, a 3D note, how to measure on a simulated phone, and targets. Done checklist updated.
- `game-detail-bar`: `scripts/phone_perf.mjs`, a general phone frame-time and canvas-call profiler with per-layer
  switches.
- Both skills made general: no pointers into any particular game's code; script paths use `${CLAUDE_SKILL_DIR}`.
