# Genre guide: open worlds

Read this on top of the core rules in [../SKILL.md](../SKILL.md) for any game with one large, continuous world the
player roams freely (top-down or 3D), where the whole map is far bigger than the screen. A game made of separate
rooms or levels that load one at a time does not need this guide.

The rule behind everything here: **never draw, update or hold the whole world.** Draw only what the camera can see,
draw many copies of a thing in one go, and keep only the area around the player loaded.

## 1. Split the world into chunks

- **The world is a grid of fixed-size chunks** (square tiles of terrain plus everything placed on them: props,
  foliage, spawns). Pick a size that puts roughly 9 to 25 chunks around the player at the normal view distance.
- **Each chunk owns its contents.** Props, spawn points and static colliders are stored per chunk, so loading,
  drawing or freeing a chunk is one operation, never a search through the whole world list.
- **Chunk data is precomputed at build time** (terrain mesh or tile layer, prop lists, bounds), not generated while
  the player walks.

## 2. Chunk culling (draw only what can be seen)

- **Test each chunk's bounds against the view first** (the camera rectangle plus a margin in 2D, the view frustum in
  3D). A chunk outside the view skips all of its contents in one check; only chunks that pass test their objects.
- **Moving objects (players, enemies, projectiles) are culled too,** against the same view, through a spatial grid
  rather than a full list.
- **Distance matters as well as direction:** past the view distance, nothing is drawn even if it is inside the
  frustum. Far chunks use cheaper versions (fewer props, simpler meshes, no shadows) before they drop out.
- **Simulation follows the same rule:** enemies and effects in far chunks sleep or run at a low tick, and wake up
  before the player can see them.

## 3. Streaming chunks in and out

- **Keep a ring of loaded chunks around the player** and load the next ring ahead in the direction of travel, in the
  background, one piece per frame, so walking never hitches.
- **Free chunks well behind the player,** with a gap between the load and free distances so walking back and forth
  over a border does not load and free the same chunk over and over.
- **Measure memory while walking a long route:** decoded art and geometry must stay flat, not climb with distance
  travelled.

## 4. Instancing (many copies, one draw)

- **Repeated things are drawn as instances:** trees, rocks, grass clumps, fences, crates and crowds of the same enemy
  use one mesh or sprite with a per-copy list of position, rotation, scale and tint, drawn in one call per chunk (in
  3D: `InstancedMesh` or `drawElementsInstanced`; in 2D WebGL: one batched sprite buffer).
- **Group by mesh and material per chunk,** so a visible chunk costs a handful of draw calls, not one per object.
- **Variety comes from per-instance data** (tint, scale, rotation, an atlas frame), not from more unique meshes.
- **Count draw calls in the busiest view** and report them; on phones keep them in the low hundreds at most.
- In 3D, foliage is real low-poly meshes drawn as instances, never flat billboard grass or trees.

## Checklist

- [ ] The world is chunked; each chunk owns its contents; chunk data is built ahead, not while walking.
- [ ] Chunks are culled against the view and a view distance; moving objects culled through a grid; far chunks
      simplified and far simulation asleep.
- [ ] Chunks stream in ahead and free behind with a gap; a long walk shows no hitches and flat memory.
- [ ] Repeated objects are instanced per chunk; draw calls in the busiest view counted and reported.
