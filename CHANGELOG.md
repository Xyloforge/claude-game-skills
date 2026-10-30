# Changelog

The plugin tracks commits on `main`; notable changes are listed here by date.

## 2026-10-30

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
