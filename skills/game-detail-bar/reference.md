# Reference: example numbers

Example numbers from shipped games. They are starting points, not targets: tune each game with its own bot sweep.

## Camera
| What | Example | Numbers |
| --- | --- | --- |
| 2D follow, floor resting, juggle rise, moat drop | 2D action game | x ease `dt*6` (12 in focus), floor ease up 8 / down 3.5, drop 110 to 330 on the bridge |
| Cutscene feet line | 2D action game | 0.74 of screen height at any zoom |
| Spring jolt + trauma shake | 2D action game | spring K 1500, damping 48; shake decays 40/s; rumble when the amount is 4 or more |
| 3D follow with look-ahead | 3D crowd battler | lead 0.55 idle / 1.45 moving / 1.15 attacking, ×1.8 mounted; ease 0.1; portrait FOV 55 vs 40 |
| Directional impact | 3D crowd battler | kick clamped ±0.55 / ±0.4, zoom punch via FOV |
| Lean-in, kicks by event | fishing game | launch kick 2.4 + hit-stop 0.09; breach kick 3.2 big / 1.2 small; camera pulled back to 0.85 |

## Feel per enemy weight (fishing game)
| | Sardine | Mackerel | Yellowfin | Snapper |
| --- | --- | --- | --- | --- |
| Shake / hit-stop | 1.3 / 35 ms | 2.2 / 55 ms | 4.8 / 115 ms | 3.6 / 90 ms |
| Blood / bubbles / ring | 6/7/9 | 10/11/12 | 24/24/22 | 18/17/17 |

Before a run, a fish trembles, a "!" pops over it, the marker shakes and the line creaks.

## Sound
- 50 Pixabay files, 3.18 MB down to 538 KB; layered random picks with pitch jitter; synth fallback until decode.
- Music loop by spectral matching: Stage 3 repeats 80.000 s apart (52.56 to 132.56 s, similarity 0.93). Streamed media element, not decoded (3 min would hold about 60 MB).
- Audio checks assert that the splash cue matches the visible spray within 650 ms, no blood before a hit, gulls spaced out, silence on pause.

## Bosses with signature mechanics (examples)
- Ghost Knight: ghost armor that only parries crack.
- Griffin: hovers, so air hits wear its wings down until it crashes.
- Ulric: man to werewolf at half health; the Moon Hunt runs 3 to 4 times from off screen with eye and dust warnings.
- Hunter's Shadow: replays your last 96 actions with your vials, relics and blessings.
- Vampire: mirror phase (only the real one casts a shadow), reads vials, range and dodge spam; blood moon at 50%; a transformation cutscene.
- 3D battler: the Horse General's lance lane locks at 70%; the King's spear clash has a 1.2 s still beat and a tug-of-war bar; the Elephant King in two phases inside a ring of fire.

## Balance and bots
- Balance sim: weak, average and good skill profiles (delay, look-ahead, noise, aim time, hit chance, focus), the real `barStep` fights, measured customer timings, a greedy shop order. Targets: average 98% quota on days 1 to 10; everything owned around day 11.
- Bot checks: skilled, masher and rider bots over seeds; clear time 2 to 5 bot minutes; masher no more than 8 of 10; rider at least 5 of 6; each floor explained in a comment.
- About 100 deterministic checks for a full action game.

## Things the user explicitly rejected
- Cheap VFX: flat polygon slash fans, circle smoke, emoji icons, plain rect health bars, system-font HUD, milky white hit flashes, trails off the sword.
- Synth beeps, or one placeholder sample for many actions.
- Losing earned catches (the shark thief).
- Flat billboard scenery in 3D.
- Music that plays its outro and cuts.
- Lock-on aim that plays the game for you (an aim guide was cut back to 4 dots; a longer reach is an upgrade).
- Low frame rate, especially on phones ("unplayable", "frame drop so bad when the cards show up").
