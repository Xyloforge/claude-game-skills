# Genre guide: action combat

Read this on top of the core rules in [../SKILL.md](../SKILL.md) for any game with real-time fighting: melee,
shooting, spells, enemies that attack, bosses. It works for side views, top-down, isometric and 3D. Example numbers
are in [../reference.md](../reference.md).

## 1. Hit feel

- **Hit-stop scaled per move and per target** (about 0.02 to 0.16 s), plus a white or tinted flash on the victim,
  knockback and a recoil pose. Small targets get a small shake and stop, heavy ones a big one; particle counts scale
  too.
- **Trails and sparks come from the weapon or hand,** taken from the art (detected blade points, a muzzle point), never
  floating beside the sprite.
- **Lights:** muzzle flashes, blade clashes and spells light their surroundings; in dark scenes a shot lights its
  whole path.
- **Damage numbers** pop and arc, bigger for critical hits, small and grey for blocked ones.
- **The camera kicks away from the hit direction,** zooms a little on launches and heavy finishers, and rests a
  little ahead of where the player is aiming.

## 2. Reading danger

- **Every attack has a wind-up that reads before it lands:** a glow, a pose and a sound. Pick one color language and
  keep it everywhere (for example yellow = can be parried, red = dodge only).
- **Ground telegraphs:** a lane or ring that tracks the target until about 70% of the wind-up, then locks, with its
  duration equal to the real wind-up.
- **Tells for things off screen or in the dark:** eyes in the dark, dust at the edge, a sound from the side.
- **One telegraph module** used by every enemy in every area, so the language never drifts.
- **Clashes and grabs have a still beat** before any mash prompt, and every grab has an escape (dash or mash).

## 3. The player's kit

- **Slots with jobs:** a basic attack, a movement option (dash, roll, blink), a standard skill and a signature or
  ultimate are a good default. Any character can usually equip any skill.
- **Every skill has its own verb** (see the core rules): a turret, a decoy, a leap slam, a bouncing wave, a teleport
  behind a marked target, a replay of recent hits. An element swap of another skill is not a new skill.
- **The basic attack is a real combo:** two or three quick hits and a finisher with more reach, weight or a special
  effect. A press during recovery chains the next hit; holding repeats.
- **The signature is on a cooldown** and gets **empowered** when a meter (filled by damage dealt) is full, instead of
  needing the full meter to cast at all.
- **A second press does something new:** a summoned object can be pressed again to swap places with it, detonate it
  or kick it.
- **Movement pays off:** a dash that leaves something behind, ends in a burst, passes through enemies or sets up the
  next attack.
- **Launching and juggling:** some hits pop enemies into the air, where they hang helpless, take extra damage and are
  kept up by further hits. Bosses, elites and fliers stay down.
- **Elements and reactions:** statuses that build up (chill to freeze, shock, burn) and reactions between them (a
  heavy hit shatters the frozen, wind spreads fire, shock jumps further through the chilled).
- **Characters as light classes:** a few stats, one passive, a starting kit and an affinity bonus (for example +20%
  with their own element). If only one character is fun, give the others the same depth (combo, payoff, second press),
  not bigger numbers.
- **Mechanics that remember or copy** (replays of recent hits, a twin that copies attacks, rhythm timing windows) need
  extra care in online play: decide where the memory and the timing live (see the multiplayer guide).
- **Aim help is light:** soft auto-aim inside a cone and range; never a lock-on that plays the game for the player.
- **Keyboard only must work:** basic, dash, skill and signature each on a key; holding a key repeats.

## 4. Enemies

- **Each enemy has a distinct job and a tell,** not a reskin with more health: a pack that circles and splits, a
  caster that keeps distance and shields an ally until the caster is hit, a ceiling clinger that drops, a long narrow
  lane attacker, a shield bearer that blocks frontal hits until a heavy hit breaks the guard, a grabber that throws
  the player into the others.
- **Give each enemy a hook,** ideally a joke tied to its attacks (a bell-ringer whose head is the bell), not the
  typical skeleton or ghost.
- **Enemies use the space:** they path around obstacles, climb ledges, wait under cover, ambush from doors, stop at
  edges (how they find paths is below).
- **Groups have roles:** a lookout that calls others, a leader that buffs, a support that heals or shields. Killing
  the right one first is a decision.
- **Breakable props** react to hits (shake, crack, break into debris) and are drawn so they read as breakable.
- **Hazards hurt enemies too:** knocking enemies into spikes, traps or fire is a reward (style points, a kill), and
  hazards take a share of max health instead of one-shotting.

### How enemies think

- **One state machine per enemy, with named states** (idle, patrol, notice, chase, wind-up, attack, recover, hurt,
  dead). Each state has enter, update and exit: enter starts its animation, sound and telegraph; exit cleans up
  (stops looping sounds, removes telegraphs, restores speed). Transitions live in one place. Hurt and death can
  interrupt any state and always run the current state's exit, so nothing is left behind.
- **Notice before chasing.** Enemies perceive through a sight range and cone with line of sight, and hear loud
  actions; on first sight they play a short reaction beat (about 0.3 to 0.5 s, a "!" and a sound) before they chase.
  When they lose the player they search the last seen place for a while, then return.
- **Only a few attack at once.** Hand out a small number of attack tokens (about 2 or 3, fewer on easy): an enemy
  needs one to start a wind-up and returns it after recovering. The rest circle, reposition or wait at range, so a
  crowd stays readable and fair.
- **Movement by steering:** seek and arrive (slowing down near the target instead of overshooting), separation from
  nearby enemies through the spatial grid, and a turn-rate limit so they never jitter or spin.
- **Paths:** A\* on a grid or nav mesh when a few enemies have their own goals; one flow field from the player for
  many enemies chasing the same target. Rebuild when the map changes, spread the work over several frames, and
  re-plan a few times a second rather than every frame.
- **Think slower than they move:** decisions run about 5 to 10 times a second, staggered across enemies; movement and
  animation run every step.
- **Bigger brains only when needed:** when a state machine gets tangled (a boss, a squad with roles), use a behaviour
  tree or utility scores (rate each option by distance, health, cooldowns and what was just used, then pick the best
  with a little randomness and never the same move twice in a row).
- **A debug view behind the QA flag** shows each enemy's state, target, path, sight cone and whether it holds an
  attack token.

## 5. Bosses

- **Two or more phases that change the rules,** not just the speed: a boss that sits and parries, then duels, then
  turns the lights out so only the player's own light and spells show the room.
- **Weighted move picks that never repeat the last move,** and an enrage that changes moves (double passes, charged
  ground), not only damage.
- **They read the player:** punish healing in sight, range camping and dodge spam.
- **An entrance:** the area music fades to silence, sound builds the scene, the theme cuts in from its first bar on a
  title card with an epithet. The intro is skippable after the first time.
- **A signature mechanic** that only this boss has (armor only a parry can crack, a hover that air hits wear down, a
  shadow that copies your last actions, a mirror phase where only the real one casts a shadow).
- **Fairness:** every unblockable is readable; the boss is out of reach only when there is a way up to it.
- **Arena lock only for bosses,** and the boss waits until the regular enemies near its arena are down.

## 6. Scoring and difficulty

- **Style rank** (for example D to SSS): up for variety, parries, perfect dodges and environment kills; down for
  repetition, damage taken and idling.
- **Slow motion as a reward:** a perfect dodge (about 1 s), a gate-breaking blow (short), a boss's final blow
  (longer).
- **Hard mode:** about 1.5× hits and damage, faster wind-ups with matching warnings, a darker look, its own medals.

## 7. Testing

- **Whole-fight bots that press real inputs:** a skilled bot (dodges tells, picks up heals, steps off hazards), a
  button-masher (never dodges) and one bot per special mode. 6 to 10 seeds each, asserting ranges: a skilled clear
  takes 2 to 5 bot minutes; a masher does not always clear (at most 8 of 10).
- **A soak bot** that mashes every key in every area and boss phase for minutes, with the player kept alive: 0 page
  errors and no stuck states (a hidden player sprite, a cast that never ends, an enemy frozen in a wind-up).
- **Cancel paths:** dash, get hit or fall out of every skill mid-cast and check that the skill's cleanup ran (the
  player visible, movement restored, looping sounds stopped).
- **Deterministic checks** for windows, combo routing and damage tables in `verify.js`.

## Checklist

- [ ] Hit-stop, flash, knockback and particles scaled per move and target; trails from the weapon.
- [ ] Every attack has a readable wind-up in one color language; ground telegraphs lock before landing.
- [ ] Every skill has its own verb; the basic attack is a combo with a finisher; the signature empowers at a full
      meter; at least one second-press skill; movement pays off.
- [ ] Each enemy has a job, a tell and a hook; enemies path around obstacles; hazards hurt enemies.
- [ ] Enemies run named states with enter and exit cleanup; they notice before chasing; attack tokens limit how many
      attack at once; steering with separation; paths re-planned a few times a second; a debug view of states.
- [ ] Bosses: phases that change rules, an entrance, a signature mechanic, fair unblockables.
- [ ] Skilled, masher and soak bots pass; every skill survives being cancelled mid-cast.
