# Art encoding and acceptance standard

An art encoding standard for any web game.

## Source and runtime files
- Keep the original master outside the game folder, and record where it is and how it was made (tool and prompt file). Ship only art the game uses.
- A loading screen, ZIP or HTTP compression is not image optimization. Measure the encoded files.

## Format and encoding
| Art | Start with | Check |
| --- | --- | --- |
| Painted characters and scenery | Lossy WebP q84 to 90, method 6, alpha kept | detail, silhouette, color at real size and the largest view |
| Pixel art, fine lines | Lossless WebP or PNG; downscale with a premultiplied box filter, then hard alpha | hard edges kept, no blur or color bleed; never upscale tiny art into mush |
| Art with transparency | WebP or PNG with alpha | look on light and dark backgrounds for halos |
| Simple vector shapes | SVG or canvas | do not rasterize just for consistency |

- Record atlas rectangles, padding and anchors (`cut_sheet.py` writes them). Check sampling stays aligned after encoding.
- One detail level across all sheets of a game, so sprites drawn at different source pixel sizes match (for example 1.25 atlas px per logical px, chosen from a side-by-side comparison).
- Transfer size is not memory: a W × H RGBA image takes about W × H × 4 bytes decoded.

## Budgets (defaults; record exceptions with the reason)
- One image: 512 KiB. All raster art per game: 1 MiB. Thumbnail: 400 KiB, 512 × 512.
- Larger games exceed this on purpose. Load per stage behind a loading screen, and record the measured bytes and why in ART.md. Never shrink art until it is unreadable.
- Report original and final bytes and the reduction percentage.

## Loading and recovery
- Gate play on download **and decode** of required art. Upload sprite sheets during loading screens to avoid a first-draw hitch.
- Finite deadlines (30 s per request, 5 s per decode), retry, and a playable fallback or an honest error. Lock input while loading.
- Use determinate progress only when totals are known. Ignore stale callbacks after a retry.

## Acceptance before sharing
1. Compare source and runtime at real size and the largest view: characters, fine lines, transparency, seams.
2. Test cold and cached loads, a missing file, a timeout, a corrupt image, retry, and thumbnail mode before the art arrives.
3. Check at desktop and phone sizes. Desktop emulation is not a real-phone test; say so.

## ART.md record
```markdown
## Source and layout
- Tool and prompt file; master location:
- Runtime atlases, grid, padding, anchors, alpha:
## Encoding and measurements
- Encoder, version, options, resize:
| File | Source size / bytes | Runtime size / bytes |
- Total before / after, reduction %, budget exceptions:
## Verification
- What was compared at which size, viewports tested, load/retry results:
```
