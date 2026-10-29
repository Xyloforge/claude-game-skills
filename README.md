# Claude Game Skills

[![validate](https://github.com/Xyloforge/claude-game-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Xyloforge/claude-game-skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Skills for [Claude Code](https://code.claude.com) that make it build web games to a finished standard instead of a
working prototype: game feel, camera, sound, animation, enemy and level variety, balance testing, UI, mobile and
performance on real phones.

Each rule in these skills is something an AI left out of a game and a person had to ask for. Loaded into Claude
Code, they make those things part of the first build.

**General by design.** The skills are for any game, not one game: no rule names or points into a particular title,
its code, its characters or its files. Rules that hold for every game live in each skill's `SKILL.md`; rules that only
make sense for one kind of game live in a genre guide that Claude reads when the game fits.

## What's inside

| Skill | What it does | Use it when |
| --- | --- | --- |
| [`game-detail-bar`](skills/game-detail-bar/SKILL.md) | The quality bar for any game: camera, feedback on every action, SFX and music, animation, content and characters that each play differently, scoring and balance, bot tests, art, **UI layout that never spills out of its frames**, UI motion, input and mobile, saves, **performance** (the coding patterns that make canvas games slow on phones and what to write instead) and working method. Plus genre guides (below). Ends with a done checklist. | Pitching, speccing, building, reviewing or reporting on a game or a game feature. |
| [`game-asset-pipeline`](skills/game-asset-pipeline/SKILL.md) | How to get art, sound and music made and processed: sprite-sheet prompt format for image models (pasted by hand or generated from the command line), effect sheets, a sheet cutter, a Pixabay SFX search and download tool, SFX loudness processing, music prompts and loop-point finding, an art encoding standard and a balance-bot pattern. | A game needs sprites, effects, backdrops, UI art, sound effects, ambience or music. |

### Genre guides (inside `game-detail-bar`)

| Guide | For games with |
| --- | --- |
| [action combat](skills/game-detail-bar/genres/action-combat.md) | Real-time fighting: hit feel, telegraphs, ability kits, enemies, bosses, combat bots |
| [side-view platforming](skills/game-detail-bar/genres/platformer-side-view.md) | Jumping and levels seen from the side: vertical camera, movement feel, level design |
| [run-based roguelites](skills/game-detail-bar/genres/roguelite-runs.md) | Runs of rooms or floors: rooms with identity, rewards and builds, meta progress |
| [sims and economies](skills/game-detail-bar/genres/sim-economy.md) | Money or resource loops: goals, fairness, upgrades, collections, balance simulation |
| [real-time multiplayer](skills/game-detail-bar/genres/multiplayer-realtime.md) | Live online play: choosing a netcode model, each player owning their character, smooth snapshots, testing with lag |

A game can use several guides at once. Genres without a guide (puzzle, racing, cards, rhythm, turn-based, strategy)
still get every core rule; a guide is added only after shipping that kind of game, from what was learned.

Both skills load on their own when Claude Code sees a matching task. You can also call them directly as
`/game-skills:game-detail-bar` and `/game-skills:game-asset-pipeline`.

## Install

In Claude Code:

```text
/plugin marketplace add Xyloforge/claude-game-skills
/plugin install game-skills@xyloforge-game-skills
```

Or from a shell:

```sh
claude plugin marketplace add Xyloforge/claude-game-skills
claude plugin install game-skills@xyloforge-game-skills
```

## Updates

The plugin tracks this repository's commits, so every change on `main` is a new version.

- **Automatic (recommended):** run `/plugin`, open **Marketplaces**, select `xyloforge-game-skills` and choose
  **Enable auto-update**. Claude Code then checks for updates in the background at startup. Third-party
  marketplaces have auto-update off until you turn it on.
- **By hand:** `claude plugin marketplace update xyloforge-game-skills`, then `claude plugin update game-skills@xyloforge-game-skills`.

A running session keeps the version it started with; new sessions (or `/reload-plugins`) pick up the update.

## Requirements for the bundled tools

The skills themselves are plain Markdown and need nothing. The scripts they call need:

| Tool | Needs |
| --- | --- |
| `game-detail-bar/scripts/phone_perf.mjs` (frame time and canvas calls on a simulated phone) | Node 18+, Playwright (`npm i -g playwright`) |
| `game-asset-pipeline/scripts/pixabay_sfx.mjs` | Node 18+, Playwright, Google Chrome |
| `cut_sheet.py` | Python 3, Pillow, NumPy, SciPy |
| `process_sfx.py`, `find_loop.py` | Python 3, NumPy, ffmpeg |

## Measuring performance on a phone

`phone_perf.mjs` loads any game page at a phone landscape size with a 3× screen and 4× slower CPU, and reports
frame times and 2D canvas calls per frame. Switch draw layers off one at a time to find what is expensive:

```sh
node skills/game-detail-bar/scripts/phone_perf.mjs "http://localhost:8080/my-game/" \
  --setup "startGame(); spawnSwarm(300);" \
  --off "game.drawGround = () => {}" \
  --off "game.drawParticles = () => {}"
```

The `game-detail-bar` skill lists the slow patterns (full-resolution canvases, repainting static layers,
per-frame blur, save/restore per sprite, no culling, O(n²) collision and more) and the targets to hit.

## Repository layout

```text
.claude-plugin/
  plugin.json          plugin manifest (skills list)
  marketplace.json     marketplace manifest (one plugin, this repo)
skills/
  game-detail-bar/     SKILL.md (core rules), reference.md, genres/*.md (genre guides), scripts/phone_perf.mjs
  game-asset-pipeline/ SKILL.md, guides, scripts/
tools/validate.mjs     repository checks run in CI
```

## Contributing

Issues and pull requests are welcome. Keep rules general (no game titles, characters, files or code paths from a
particular game), concrete (numbers, not adjectives) and written for Claude to act on. A rule that holds for every
game goes in `SKILL.md`; a rule for one kind of game goes in the matching genre guide (or a new guide, once there is
real experience behind it). `tools/validate.mjs` also rejects private note links, `~/.claude/skills` paths and home
folders. Run the checks before opening a pull request:

```sh
node tools/validate.mjs
claude plugin validate .
```

See [CHANGELOG.md](CHANGELOG.md) for what changed.

## License

[MIT](LICENSE) © Xyloforge
