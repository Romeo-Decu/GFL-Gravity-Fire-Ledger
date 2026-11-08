# Gravity Fire Ledger — brand assets (DEC-026)

The mark: a node-network flame (nodes = evidence values, edges = verified links) resting on three
hash-linked ledger blocks. Geometry is authored and fully defined by `make_logo.py` (fixed parameters,
no randomness, no third-party artwork, no stock image, no image generator). Regenerate with:

    python visualization/assets/brand/make_logo.py visualization/assets/brand

| File | Use |
|---|---|
| `GFL_mark_full.svg` / `GFL_mark_512.png` | Primary mark, dark background |
| `GFL_mark_full_inverted.svg` / `GFL_mark_512_light.png` | Light backgrounds, documents |
| `GFL_mark_flame.svg` | Flame only (no chain), large hero use |
| `GFL_mark_simple.svg` / `GFL_mark_128.png` / `GFL_mark_32.png` | Reduced node count for icons and favicon |

Previous mark (DEC-020): `archive/brand_v0/`.

## Icon set v1 (`icons/`)
22 icons in the same grammar as the mark: nodes joined by thin edges, outlines 1.5× thicker, on the dark rounded tile. The geometry is authored in `make_icons.py` on a 24×24 grid. There is no third-party artwork. Regenerate with:

    python visualization/assets/brand/make_icons.py visualization/assets/brand/icons

The preview is `icons/_preview_sheet.png`. Status: v1, waiting for the owner's review.
