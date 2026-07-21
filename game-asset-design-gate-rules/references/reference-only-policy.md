# Reference-Only Policy

Use this file when the request mentions asset packs, store pages, screenshots, downloaded art, paid marketplaces, or external game visuals.

## Goal

Convert references into a new production direction instead of directly shipping the referenced art.
This applies equally to free packs, paid packs, marketplace previews, store screenshots, and user-provided reference screenshots.

## Allowed Uses Of References

- study silhouette hierarchy
- study camera angle and framing
- study color grouping and contrast
- study prop density and scene layering
- study material breakup
- study timing and pose count for animation
- study how maps separate walkable ground, blockers, props, and points of interest
- study what makes a marketplace preview feel commercial-grade

## Disallowed Uses

- shipping a downloaded asset unchanged
- shipping a marketplace screenshot or edited crop as final art
- shipping a lightly recolored or resized copy
- tracing a distinctive asset too closely
- preserving a unique composition or shape arrangement from one source pack
- mixing third-party packs into final art when the task is supposed to create an original project identity

## Extraction Method

For each reference, summarize it in abstract production language:

- silhouette: heavy / sharp / round / wide / tall / compact
- palette: muted / warm / cold / high-contrast / low-saturation
- materials: cloth / leather / bone / metal / slime / wood
- detail density: sparse / medium / dense
- readability trick: outline contrast / accent color / oversized weapon / negative space

Then recombine those findings into a new brief instead of reproducing the source image.

## Good Transformation Example

Bad:

```text
Use this Kenney enemy and make it darker.
```

Good:

```text
Borrow the readable top-down angle, broad silhouette separation, and clean value blocks from this pack, but redesign the enemy as a swamp brute with a wider torso, asymmetrical arm weapon, and a more grounded color palette that matches this project.
```

## Project-Fit Checklist

Before finalizing, confirm:

- the asset fits the game's genre and camera
- the asset matches the project's visual family
- the asset reads correctly during motion
- the asset is original enough to stand on its own
- the asset can be imported cleanly into Godot
- the chosen reference was explicitly confirmed by the user before design production began
