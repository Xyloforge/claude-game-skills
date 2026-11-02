# Genre guide: 3D scenes

Read this on top of the core rules in [../SKILL.md](../SKILL.md) for any game drawn in 3D, whatever its genre: an
action game, a racer, a cosy sim, a 2.5D side view built from 3D models. It covers models, animation, lighting,
shadows and 3D performance, with notes for three.js in a browser, Godot and Unity. Pair it with
[open-world.md](open-world.md) when the world is large.

## 1. Models

- **One convention for every model:** glTF or GLB as the exchange format, 1 unit = 1 metre, Y up, the origin at the
  feet (or the base of a prop), and every model facing the same way. Fix scale and rotation in the modelling tool or
  the import settings, never with a different correction per model in game code. Check each new model next to the
  player character in game before using it.
- **Budgets by device.** Decide triangle and texture budgets per kind of model before making them, and write them in
  the spec. As a phone starting point: a few thousand triangles for a main character, a few hundred to a thousand
  for a common prop, 1024 px textures at most per character, less for props. Anything large or repeated gets
  levels of detail (LODs) that switch by distance.
- **Compressed for the GPU, not only for download:**
  - Geometry: meshopt or Draco compression in a browser (three.js `MeshoptDecoder`, `DRACOLoader`); engines pack
    meshes on import.
  - Textures: a decoded 2048 × 2048 RGBA texture is 16 MB of GPU memory; GPU formats cut that to about a quarter or
    less. In a browser, KTX2 with Basis Universal (three.js `KTX2Loader`), which becomes the right format for each
    device. In Godot, the "VRAM Compressed" import mode; in Unity, per-platform compression (ASTC on phones).
  - Colour textures (albedo, emissive) are sRGB; data textures (normal, roughness, metalness, ambient occlusion)
    are linear. A data map marked sRGB makes surfaces look wrong in a way that is hard to spot.
- **Look at it in the game,** at the play camera's distance and angle, under the game's lighting: a model that looks
  right in a viewer can read as a blob, float above the ground or clip into it in play.

## 2. Loading and memory

- **Load behind a screen and warm up:** download, decode and upload every model and texture of the area, then draw
  every material once before play, so shaders compile behind the loading screen instead of hitching on first sight
  (three.js `renderer.compileAsync(scene, camera)`; Unity `ShaderVariantCollection.WarmUp`; in Godot, show every
  material and effect once in view behind the loading screen). Effects that spawn later (a spell, an explosion) are
  warmed up too.
- **Free what leaves:** when an area or a model goes away, release its geometry, materials and textures (three.js
  `dispose()` on each; engines free unreferenced resources, so drop the references). Walk through several areas and
  check that memory returns to the same level.

## 3. Animation

- **Skeletal clips played through the engine's mixer** (three.js `AnimationMixer`, Godot `AnimationTree`, Unity
  Animator). Characters that share a skeleton share clips.
- **Never snap between clips:** cross-fade about 0.1 to 0.25 s (shorter into attacks and hits, longer between idle
  and walk). Movement blends by speed between idle, walk and run, and the playback speed matches the movement speed,
  so feet never slide on the ground.
- **Layers:** the upper body can attack, aim or carry while the legs keep walking; hit reactions are added on top
  instead of replacing the current clip.
- **Events on frames:** footstep sounds and dust on the frame where the foot lands, hit checks on the frame where
  the blow connects (the core rule that timing windows match the art).
- **Decide root motion once:** either clips move the character (root motion) or code moves it and clips play in
  place. Mixing the two per clip makes characters drift.
- **Death and big knockbacks** may hand the body to physics (a ragdoll with joint limits, see the core simulation
  rules) and blend back to animation when getting up.

## 4. Lighting

- **A small, deliberate light rig:** one key light (sun or moon) that casts shadows, a soft fill from an environment
  map or hemisphere light, and a few accent lights without shadows (torches, windows, magic). Each extra shadowed
  light costs a full extra render of the scene.
- **Bake what does not move:** lightmaps and ambient occlusion for static scenery where the engine supports it
  (Godot `LightmapGI`; Unity baked lighting and light probes), so phones get rich light for free. Real-time global
  illumination is a desktop setting at most.
- **Colour pipeline set once:** sRGB output and a filmic tone mapper (three.js `renderer.outputColorSpace =
  THREE.SRGBColorSpace` and ACES or AgX tone mapping; the Environment's tonemap in Godot; the post-processing
  tonemapping in Unity), so the same model looks the same in every scene.
- **Fog and atmosphere** give depth and hide the far edge of the draw distance; the core atmosphere rules (light
  shafts, particles, a time-of-day grade) apply in 3D too.

## 5. Shadows

- **Only what matters casts:** characters, enemies and large props. Grass, small debris, particles and distant
  scenery do not.
- **A tight shadow camera:** the key light's shadow area follows the player and covers only what the camera can see
  near them; a tight area gives sharp shadows from a small map. Shadow maps around 2048 on desktop and 1024 or less
  on phones, with a quality setting.
- **Every character touches the ground:** a soft contact shadow (a blob under the feet) even when real-time shadows
  are off or far away, so nothing seems to float. Crowds on phones use blobs only.

## 6. Materials, transparency and readability

- **Consistent materials:** physically based materials with consistent roughness and metalness across the game,
  shared materials and texture atlases so many objects draw in one batch.
- **Few true transparents:** foliage, fences and hair use alpha cutout (alpha test), not blending; blended
  transparency is kept for effects, glass and water, because it sorts badly and overdraws.
- **No flat billboard scenery:** grass, trees and shrubs are real low-poly meshes, drawn as instances.
- **The player reads at a glance:** a silhouette and colour that stand out from the world, a rim light or outline
  when the scene is busy, scenery between the camera and the player fading out (core section 1), and a camera that
  pulls in instead of passing through walls.

## 7. Performance and measurement

- **Draw calls are the first budget.** Repeated objects are instanced (three.js `InstancedMesh` or `BatchedMesh`,
  Godot `MultiMeshInstance3D`, Unity GPU instancing or the SRP Batcher), static scenery is merged or batched, and
  far objects drop to lower LODs or disappear by distance (Godot visibility ranges, Unity LOD Groups).
- **Resolution and effects:** cap the render resolution on phones (three.js `renderer.setPixelRatio(Math.min(
  devicePixelRatio, 1.5))`; render scale in Godot and Unity) and lower it when frames run slow; bloom, depth of field,
  screen-space reflections and ambient occlusion are quality settings, off or low by default on phones.
- **No per-frame garbage:** reuse temporary vectors, matrices and quaternions instead of creating new ones in the
  update; never create geometry or materials during play.
- **Measure:** draw calls, triangles and texture memory in the busiest view (three.js `renderer.info`; Godot
  Monitors and the visual profiler; Unity Stats panel, Frame Debugger and Profiler), on a phone (core section 13).
  As a phone starting point: draw calls in the low hundreds at most, visible triangles in the low hundreds of
  thousands, and the frame-time targets of the core rules.

## Checklist

- [ ] Every model uses the same scale, up axis, origin and facing; budgets per kind of model written in the spec;
      LODs on large or repeated models; checked in game at play distance.
- [ ] Geometry and textures GPU-compressed for the target; colour maps sRGB and data maps linear.
- [ ] Areas load behind a screen with every material and effect warmed up; memory returns to the same level after
      changing areas.
- [ ] Animation cross-fades, blends by speed without foot sliding, layers upper body and hit reactions, and fires
      sounds and hits on the right frames; root motion decided once.
- [ ] One shadowed key light, soft fill, shadowless accents, baked light for static scenery where possible; one
      colour pipeline with tone mapping; fog for depth.
- [ ] Only key objects cast shadows from a tight shadow camera; every character has a contact shadow.
- [ ] Cutout for foliage, few blended transparents, no billboard scenery; the player reads at a glance.
- [ ] Draw calls, triangles and texture memory measured in the busiest view on a phone, with instancing, batching,
      a capped resolution and phone presets for effects.
