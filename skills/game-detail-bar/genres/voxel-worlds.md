# Genre guide: voxel worlds

Read this on top of the core rules in [../SKILL.md](../SKILL.md) and [3d-scenes.md](3d-scenes.md) for any game built
from blocks: a blocky world, voxel characters and props, terrain or walls the player can break. Pair it with
[open-world.md](open-world.md) when the world is large.

Why voxels suit the web and phones: colour lives on the geometry instead of in large painted textures, almost
everything is opaque (no sorting, no overdraw), characters animate as rigid parts instead of skinned meshes, and the
flat-shaded look reads as a finished style without normal maps or high-poly models. A blocky game that draws a big
crowd, lots of gore particles and breakable walls can run where a painted 2D game of the same scope would not. These
rules keep it that way.

## 1. One block grid, decided up front

- **Pick the block size per layer and write it in the spec:** a coarse world grid (about 0.25 to 1 m) for terrain and
  buildings, a finer grid for models (about 1 to 2 cm for a first-person weapon, 3 to 6 cm for characters and props).
  Halving the world block size gives 8 times the cells and about 4 times the surface, so the world grid is the
  expensive one.
- **The world is a flat array of block ids** (one byte each is enough for most games), indexed so a column or a chunk
  is contiguous. Block types live in a table: colour or texture tile, toughness, whether it blocks movement, sight or
  bullets.
- **One coordinate convention:** where block (x, y, z) sits in world units, which layer is the ground and where y = 0
  is. Write the conversion helpers once (world to block, block to world centre) and use them everywhere; off-by-one
  errors between the mesher, collision and ray casts are the classic voxel bug.

## 2. Meshing (turning blocks into triangles)

- **Only faces that touch air are drawn.** A solid block buried in the wall makes no triangles.
- **Greedy meshing:** neighbouring faces with the same colour or tile, the same direction and no occlusion merge into
  one rectangle. It typically halves the triangles or better on models with flat areas; measure before and after.
  Faces with corner occlusion (below) stay single so the shading stays right.
- **Baked ambient occlusion per vertex:** for each face corner, count the solid neighbours around it (two sides and
  the diagonal) and darken the vertex colour, from about 0.45 for a fully enclosed corner up to 1. Flip the quad's
  diagonal when the occlusion is uneven, so the shading does not crease. It costs nothing at draw time and gives the
  depth that makes voxels look finished.
- **Colour variety without unique art:** a small per-block brightness variation from a hash of its position, plus
  colours authored with noise, so large walls are not flat paint.
- **Textured faces when the style wants them:** one small tile per block face (about 16 px per block) in an atlas,
  each tile padded with its own edge pixels so mipmaps never bleed into the neighbour. Faces of noisy materials
  (asphalt, grass, stone) get a random 90° rotation per block to hide repetition; patterned ones (bricks, planks) do
  not. Greedy merging needs repeating textures, so textured world faces stay one quad per face, or use a texture
  array with repeat.
- **Chunks of about 16 × 16 columns,** one mesh each. Breaking a block rebuilds only its chunk, plus the neighbour when
  the block sits on the chunk border. Rebuild dirty chunks at most once per frame, batched.
- **Mesh off the main thread when rebuilds are big** (explosions, terrain streaming): in a browser, a Web Worker that
  returns typed arrays (transferred, not copied); in Godot a `WorkerThreadPool` task; in Unity the Jobs system with
  Burst. A single block broken by a bullet can stay on the main thread.

## 3. Ray casts and collision

- **Ray casts walk the grid** with the Amanatides-Woo (DDA) traversal: step block by block along the ray and stop at
  the first solid one, which also gives the face normal for impact effects. It is exact and far cheaper than a
  physics-engine ray against triangle meshes.
- **Characters collide with the grid as boxes,** one axis at a time (x, then z, then y), so they slide along walls.
  Step up automatically onto ledges of one block when walking into them; anything taller needs a jump.
- **Crowds use a 2D walkable map** (columns with nothing solid up to head height) for movement and a flow field
  (action-combat guide) for paths. Rebuild the column and mark the flow field dirty when a block breaks.
- **Bullets check the world and every enemy, and take the nearest hit.** Enemy hit boxes are boxes in the enemy's own
  turned frame (head first for headshots), not the drawn mesh.

## 4. Destruction

- **Every breakable block has hit points by material:** crates break in one hit, brick in a few, the ground and the
  map border never. Write the table in the spec.
- **Every hit leaves something:** chips in the block's colour plus a spark on every impact, and a bigger burst of
  chunks when a block breaks.
- **Debris is one instanced cube** with a per-copy colour, bounced against the grid with simple per-axis collision,
  settling on the ground and shrinking out after a few seconds. Cap the count (a few thousand) and reuse the oldest.
- **Decide what happens to floating blocks** (fall, crumble or stay) and make it consistent; an unsupported tower that
  hangs in the air reads as a bug in a game where walls break.

## 5. Voxel characters and crowds

- **Characters are rigid parts** (legs, torso, arms, head, plus small glowing or accent pieces), each a voxel model
  with its pivot at the joint. Animation is joint rotations written in code or keyed per clip, and every part of the
  same kind across the whole crowd is one instanced mesh.
- **Variety from outfits and per-copy tint:** a few full outfit sets (each its own set of part meshes) and a small
  brightness tint per copy. Turning, head tilt, gait speed and arm sway are randomised per character so a crowd never
  marches in step.
- **Gore and deaths use the model itself:** on death, spawn chunks at random points inside each part's box in that
  part's colours (shirt, skin, shoes, blood), thrown away from the shot. A headshot throws the head harder.
- **Far characters drop to the low model** (plain boxes in the outfit colours) and lower update rates; a toggle between
  the two is also the quickest way to measure what the detail costs.

## 6. First-person weapon and hands

- **Built on its own fine grid** (about 1 cm), with real detail (rails, vents, sights, a textured grip), and drawn in
  its own pass (the 3D-scenes guide).
- **Arms aim at an elbow point below the screen every frame,** so the forearm always joins the hand to the body while
  the hand moves through a reload. Fixed arm angles break the moment the hand leaves its rest pose.
- **Reloads are keyframed tracks** (weapon tilt and offset, hand path, magazine and bolt offsets) with sound events at
  set times. The magazine follows the hand while gripped, the old one drops away as its own falling object, the
  weapon jolts when the new one seats, and the ammo refills on that frame, not at the end. A reload with rounds left
  skips the bolt and is shorter.
- **Colour space matches the rest of the rig:** colours authored by eye are sRGB and must be converted to linear
  before going into vertex colours, or the model looks washed out next to parts coloured through the material.

## 7. Art pipeline

- **Models are made, not drawn in code:** MagicaVoxel (`.vox`) or another voxel editor, or generated and then fixed by
  hand, loaded and greedy-meshed at load time. Code places and animates them. Building shapes from code boxes is fine
  for a test, not for the shipped game.
- **One palette per game** (or per area), with lighter and darker steps of each material so models stay consistent.
- **Check every model in game** at play distance under the game's light (the 3D-scenes rule), and every first-person
  model at both hip and aim.

## 8. Budgets and measurement

- **Count triangles and draw calls in the busiest view** with the detail toggle and a stress key (core section 13),
  and keep the numbers in the spec. As a starting point: a voxel character a few thousand triangles after greedy
  meshing, a first-person weapon about ten thousand, the whole visible world under about a million triangles on a
  desktop and a few hundred thousand on a phone, draw calls in the low hundreds.
- **Shadows double the triangle count** of everything that casts: crowds and big props cast, litter, decals and
  debris do not.
- **Memory is small but not free:** a 160 × 24 × 160 world is 600 KB of block ids; chunk meshes and debris buffers
  are where the memory goes. Free a chunk's old geometry when it is rebuilt.

## Checklist

- [ ] Block sizes for world and models written in the spec; one conversion helper used by mesher, collision and rays.
- [ ] Faces culled, greedy meshing on models, per-vertex AO with diagonal flipping, colour variation per block.
- [ ] Atlas tiles padded against bleeding; noisy materials rotated per block; chunks rebuilt only when dirty, big
      rebuilds off the main thread.
- [ ] DDA ray casts with face normals; box collision per axis with a one-block step-up; walkable map and flow field
      updated when blocks break.
- [ ] Breakable materials have hit points; every hit chips, every break bursts; debris instanced and capped; floating
      blocks handled one consistent way.
- [ ] Characters are instanced rigid parts with outfits, tint and per-character motion; deaths burst into the model's
      own colours; far characters use the low model.
- [ ] First-person arms aim at an off-screen elbow; reloads keyframed with sounds on events and ammo at the seat;
      model colours in the right colour space.
- [ ] Models from a voxel editor or generation, one palette, checked in game.
- [ ] Triangles, draw calls and worst frame measured with the detail toggle and a stress test; only key objects cast
      shadows.
