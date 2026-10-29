# Genre guide: side-view platforming

Read this on top of the core rules in [../SKILL.md](../SKILL.md) for any game seen from the side with jumping, ledges
and levels the player travels through (platformers, side-scrolling action, runners). Combine it with the action combat
guide when the game also fights. Example numbers are in [../reference.md](../reference.md).

## 1. Camera

- **Vertical framing has rules.** Rest the camera on the floor the player last stood on and ease between floors;
  ease up faster than down, and snap down on a fall. During air combos or high jumps, rise so the player stays in the
  upper middle of the screen.
- **Show what is below when it matters:** sink the view over a pit, a moat or a hazard under a bridge.
- **Look ahead horizontally** in the facing direction, more when running or riding, less when standing.
- **Cutscene framing:** keep the characters' feet at a fixed share of the screen height (about 74%) at any zoom, so
  letterbox bars never cut them off.
- **Parallax:** the far layer moves at a fraction of the camera speed (about 28%); every layer is painted, none code
  drawn.

## 2. Movement feel

- **Coyote time** (a jump still works a few frames after leaving a ledge) and a **jump buffer** (a press just before
  landing still jumps).
- **Variable jump height** from how long the key is held, and faster falling than rising.
- **Landing has weight:** a squash, dust, a sound scaled by fall height, and a small camera dip on big drops.
- **Turning is not instant** for heavy characters (a short skid), and is instant for light ones.

## 3. Level design

- **One idea per area, and name it:** a hill, catacombs, a rooftop chase, a bell tower, a burning bridge, a mirror
  gallery. Each area changes the rules (lit only by fire, a rising flood, an escort, a stage on a mount).
- **Forward routes with height** (slopes, steps, one-way ledges, ceilings, an optional upper route with a reward)
  beat flat arenas of waves.
- **Chases and set pieces:** a wall of fire sweeping behind the player, a collapsing stair, a fight on something
  moving.
- **Enemies use the level:** they climb from ledge to ledge, leap down at a player below, jump to low ledges, stop at
  edges, wait under roofs, ambush from coffins or side doors.
- **Checkpoints placed by feel** (a lantern, a shrine): passing one lights it and heals. State that should persist
  across a death persists (broken walls, opened shortcuts, claimed caches).
- **Clean level art:** no duplicate platforms that look walkable but are not, no props that look usable but are not
  (a fake door), nothing floating, no random scatter of decoration.
- **Interactive props read as usable;** decoration never does.

## 4. Testing

- **A route bot** that runs each level start to finish with real inputs over several seeds, asserting a time range
  and that every checkpoint is reached.
- **Ledge checks:** every jump on the main route is reachable with the base move set (a deterministic check of
  distances and heights against jump reach).
- **Camera checks:** headless screenshots at each checkpoint and at the deepest drop at desktop and phone sizes, with
  the player inside the safe frame.

## Checklist

- [ ] Camera rests on floors, eases up and snaps down, sinks over hazards, keeps cutscene feet clear of letterbox.
- [ ] Coyote time, jump buffer, variable jump height, weighty landings.
- [ ] Each area has one named idea that changes the rules; routes have height and an optional upper path.
- [ ] Enemies use ledges and edges; checkpoints light and heal; persistent changes persist.
- [ ] No fake platforms or fake doors; route bot and ledge checks pass.
