# Genre guide: run-based roguelites

Read this on top of the core rules in [../SKILL.md](../SKILL.md) for any game played in runs built from rooms, floors or
waves, with random rewards, a build that grows during the run, and progress kept between runs (dungeon crawlers,
survivor-likes, deck builders with maps). Combine it with the action combat guide when the runs are fought in real
time.

## 1. Run structure

- **Stages made of floors, floors made of rooms,** generated from a seed (the same seed gives the same floor, which
  also lets online guests build their own copy). A minimap shows known and visited rooms.
- **Room types with their own purpose:** combat, shop, treasure, new skill, rest, elite, boss, exit. Calm rooms are
  small; boss arenas are large and open.
- **Each stage is a new place with new rules:** its own enemy roster, room themes, hazards, art, textures and music.
  Moving enemies from one stage to the next as filler is a stopgap and is reported as one.
- **Stage select once a stage is beaten,** with a catch-up so starting later is not a punishment (some starting gold
  and one pick of a relic or item). Save which stages are cleared and which was played last.
- **Readable exits:** doors are lit and framed, locked doors look locked, and the way out after a fight is marked
  (chevrons, a light, a sound).

## 2. Rooms with identity

A plain box with random enemies feels bland. Give every combat room:

- **A theme** with its own enemy table, floor tint, props and ambience (a nest, a flooded cellar, a laundromat, a
  rooftop).
- **A shape:** L-shapes, a plus, pillars, a divider wall, a pit ring, a chasm with bridges, holes, ledges. Build rooms
  on a tile grid so shapes, collision, pathing and pits share one map. Keep door lanes clear in every layout.
- **Hazards and traps** that work on enemies too (spikes, snapping traps, webs, steam vents, slippery puddles,
  cracked floors, gas, a passing train, a wind gust), each with a warning before it acts and a first-time hint beside
  it.
- **Nests or spawners** (an egg sac, an anthill) that keep making enemies until they are broken, so the room has a
  target, not just a timer.
- **Pits** that cost a share of health (about 10%) and put the player back at the last safe spot, never an instant
  death; knocked or rolling enemies fall in and die.
- **Breakable props** that drop small rewards and block shots until broken.

## 3. Rewards and builds

- **Choices, not handouts:** a reward is a pick of two or three, shown as cards with the slot, the element and what
  it does.
- **Replacing never loses anything:** when a new skill or item replaces one, the old one drops on the floor and can be
  picked back up (which drops the other). In co-op a teammate can take it.
- **Shops explain before buying:** what the item does, its slot, and what it would replace; potions say how much they
  heal.
- **Every relic is one rule,** not +x%: the first hit in each room stuns, knockouts give a short speed and damage
  burst, being hit damages the attacker, once per run get back up at half health.
- **Builds have synergies the player can plan for:** elements that react, relics that favor a kind of skill,
  characters with an affinity.

## 4. Characters and meta progress

- **Characters as light classes** (stats, a passive, a starting kit, an affinity) picked at a wardrobe or roster
  screen that shows each one's kit icons and passive, and changes the starting kit when picked.
- **Meta currency must mean something.** If everything is unlocked from the start, a currency that used to unlock
  things is now pointless: remove it or give it a new use (cosmetics, starting choices, harder modes).
- **A hub between runs** where everything is a short walk: the roster, the spellbook or loadout, the shop for
  unlocks, the door to the run, and (online) the room code.

## 5. Testing

- **A run bot** that clears every room type and floor of every stage with each character over several seeds, with
  the player kept alive, asserting 0 page errors and no stuck rooms (a room that never unlocks, a nest that cannot be
  hit, an enemy stuck behind a wall).
- **Generation checks:** every generated floor is connected, door lanes are clear, no spawn point sits in a wall or
  pit, and every room shape leaves enemies a path to the player.
- **A screenshot per room theme and shape** at desktop and phone sizes.

## Checklist

- [ ] Seeded floors with clear room types and a minimap; each stage has its own roster, themes, art and music.
- [ ] Every combat room has a theme, a shape, hazards that hit enemies too and, where it fits, a nest to break.
- [ ] Pits cost a share of health and return the player to a safe spot.
- [ ] Rewards are picks; replaced items drop on the floor; shops explain what an item does and replaces.
- [ ] Every relic is one rule; meta currency has a purpose; stage select gives a catch-up.
- [ ] Run bot and generation checks pass for every stage and character.
