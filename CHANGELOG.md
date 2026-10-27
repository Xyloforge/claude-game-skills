# Changelog

The plugin tracks commits on `main`; notable changes are listed here by date.

## 2026-10-27

- First public release as a Claude Code plugin marketplace (`game-skills@xyloforge-game-skills`).
- `game-detail-bar`: new **Performance** section: the coding patterns that make 2D canvas games slow on phones
  (full device-pixel-ratio canvases, repainting static layers, per-frame blur, save/restore per sprite, path fills
  per object, no culling, uncapped particles, O(n²) collision, first-use sheet uploads, unthrottled sounds), what
  to write instead, a 3D note, how to measure on a simulated phone, and targets. Done checklist updated.
- `game-detail-bar`: `scripts/phone_perf.mjs`, a general phone frame-time and canvas-call profiler with per-layer
  switches.
- Both skills made general: no pointers into any particular game's code; script paths use `${CLAUDE_SKILL_DIR}`.
