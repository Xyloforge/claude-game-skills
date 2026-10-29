# Reference: example numbers

Example numbers measured in shipped games. They are starting points, not targets: tune each game with its own bots
and measurements. Each table says which kind of game it came from.

## Camera
| What | Kind of game | Numbers |
| --- | --- | --- |
| 2D follow, floor resting, juggle rise, moat drop | Side-view action | x ease `dt*6` (12 in focus), floor ease up 8 / down 3.5, drop 110 to 330 over a bridge |
| Cutscene feet line | Side-view action | 0.74 of screen height at any zoom |
| Spring jolt + trauma shake | Side-view action | spring K 1500, damping 48; shake decays 40/s; rumble when the amount is 4 or more |
| 3D follow with look-ahead | 3D crowd battler | lead 0.55 idle / 1.45 moving / 1.15 attacking, ×1.8 mounted; ease 0.1; portrait FOV 55 vs 40 |
| Directional impact | 3D crowd battler | kick clamped ±0.55 / ±0.4, zoom punch via FOV |
| Lean-in, kicks by event | Fishing sim | launch kick 2.4 + hit-stop 0.09; breach kick 3.2 big / 1.2 small; camera pulled back to 0.85 |
| Top-down view height | Top-down action roguelite | about 580 world units of view height on desktop, so rooms and threats fit |

## Feedback scaled by weight (fishing sim)
| | Small | Medium | Large | Heavy-medium |
| --- | --- | --- | --- | --- |
| Shake / hit-stop | 1.3 / 35 ms | 2.2 / 55 ms | 4.8 / 115 ms | 3.6 / 90 ms |
| Particles (three kinds) | 6/7/9 | 10/11/12 | 24/24/22 | 18/17/17 |

Before a run, the target trembles, a "!" pops over it, the marker shakes and the line creaks.

## Sound
- 50 recorded files, 3.18 MB down to 538 KB; layered random picks with pitch jitter; a synth stand-in only until a
  file decodes.
- Music loop by spectral matching: a stage track repeats 80.000 s apart (52.56 to 132.56 s, similarity 0.93).
  Streamed through a media element, not decoded (3 minutes would hold about 60 MB).
- Audio checks assert that a splash cue matches the visible spray within 650 ms, no impact sound before the hit,
  ambient one-shots spaced out, silence on pause.

## Bosses with signature mechanics (side-view and 3D action)
- An armored knight whose ghost armor only a parry can crack.
- A flying beast that hovers, so air hits wear its wings down until it crashes.
- A hunter who turns into a beast at half health and hunts from off screen 3 to 4 times, with eye and dust warnings.
- A shadow double that replays your last 96 actions with your items.
- A mirror phase where only the real boss casts a shadow, a boss that reads healing, range and dodge spam, and a
  phase change at 50% with a transformation scene.
- A mounted general whose lance lane locks at 70% of its wind-up; a spear clash with a 1.2 s still beat and a
  tug-of-war bar; a two-phase boss inside a ring of fire.
- A seated boss who parries and calls guards, then duels with telegraphed sword lines, then cuts the lights so only
  the players' own light and spells show the room.

## Abilities with their own verbs (top-down action roguelite)
Fast melee combo with a wave finisher; a charge blast (tap for a puff, hold for a blast); a channelled beam; heavy
two-punch melee; a ranged volley; a multi-dash that leaves live wires; dig and emerge; a dash that gathers enemies; a
decoy; an arrival burst; a sticky bomb; homing summons; a turret you can swap places with; a wall you can kick apart;
a push wave; a delayed meteor; a lance that pins; a leap slam; expanding rings; becoming a tornado; marks cashed in
by a finisher; a teleport behind the most-marked enemy; a twin that copies your attacks; darkening the room; a
rhythm combo on a 120 BPM beat with a ±90 ms window; a dash that leaves a pulsing speaker; a wave that bounces off
walls; replaying every hit of the last 3.5 s.

## UI layout
- Phone checks at 844×390 with a 3× pixel ratio; desktop at 1280×720.
- Minimum readable text about 11 px on phones; card text wraps inside the content rect, not the frame rect.
- A seven-card character row: card width computed as about `W / (count × 186 + 40)` scale, so the row always fits.

## Balance and bots
- Economy sim: weak, average and good skill profiles (delay, look-ahead, noise, aim time, hit chance, focus), the real
  fight step, measured customer timings, a greedy shop order. Targets: average 98% quota on days 1 to 10; everything
  owned around day 11.
- Whole-fight bots: skilled, masher and rider over seeds; clear time 2 to 5 bot minutes; masher no more than 8 of 10;
  rider at least 5 of 6; each bound explained in a comment.
- About 100 deterministic checks for a full action game.

## Online co-op (owner-runs-their-character, browser, WebSocket relay)
| What | Before (host streams a picture) | After (each player runs their own character) |
| --- | --- | --- |
| Key press to own character moving, no lag | about 115 ms | 23 to 48 ms (one to three frames) |
| Same, 70 ± 25 ms each way | 250 to 430 ms | 37 ms |
| Guest's hits landing on the host | a round trip later | applied as actions on arrival |

- Host snapshots: 30 a second, 3 to 5 KB each in a 16-enemy fight with two casters (about 100 KB/s per guest).
- Guest interpolation delay: about 45 ms on a clean line, 95 to 115 ms with 70 ± 25 ms lag; under 1.5% of frames
  extrapolated.
- A hidden host tab ticking from a worker timer kept sending about 25 snapshots a second.
- Guest frame time at 4× CPU throttle during a busy fight: median 20 ms; the profile was almost all canvas drawing, the
  network code under 2%.

## Things people explicitly rejected
- Cheap effects: flat polygon slash fans, circle smoke, emoji icons, plain rect health bars, system-font HUD, milky
  white hit flashes, trails that do not follow the weapon.
- Synth beeps, or one placeholder sample for many actions.
- Losing something already won (a thief that steals the catch).
- Flat billboard scenery in 3D.
- Music that plays its outro and cuts.
- Lock-on aim that plays the game for you (an aim guide was cut back to 4 dots; a longer reach is an upgrade).
- Low frame rate, especially on phones ("unplayable", "frame drop so bad when the cards show up").
- Typical enemy archetypes with no hook (the generic skeleton archer, ghost or ghoul).
- Characters whose abilities are only re-colored copies of another's.
- UI that spills past its frame, bars that look empty under their frame art, and a boss bar left floating over the
  next screen.
