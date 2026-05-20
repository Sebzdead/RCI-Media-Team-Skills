---
name: rci-media-design
description: Use this skill to generate well-branded interfaces and assets for the Revolutionary Communist International (RCI) Media Team — Instagram article/story posts, YouTube thumbnails, video title cards, podcast covers, and internal slide decks. Contains essential design guidelines, the brand palette (red / off-white / ink), the compressed-caps display type stack, real photographic textures, and UI-kit components for prototyping.
user-invocable: true
---

Read the `README.md` file within this skill first — it contains:
- The full content + voice rules (Spanish-friendly, collective voice, no emoji, headline-as-hook).
- The visual foundations: palette, type, textures, layout, motion.
- The iconography stance (Lucide for tiny UI affordances; photography as primary symbol).
- An index of the other files in this folder.

Then explore as needed:
- `colors_and_type.css` — drop into any HTML file with `<link rel="stylesheet" href="colors_and_type.css">` to get the full design-token surface (CSS custom properties, semantic element styles, type scale).
- `assets/logos/` — RCI wordmark + compact mark, dark & light. **Placeholders** until real logo SVGs arrive.
- `assets/textures/` — paper, film grain, paint-peel, halftone, light-specks. Overlay at 8–20% opacity, `mix-blend-mode: multiply` on light surfaces or `screen` on dark.
- `preview/` — one card per token / component, viewable in the Design System tab.
- `ui_kits/instagram/` — feed posts, stories, podcast promos, book reviews, date posts. `index.html` is the entry; component JSX files are factored per surface.
- `ui_kits/youtube/` — thumbnail + title card templates.
- `slides/` — title slide, big quote, section divider, comparison, photo-bleed.

When generating an artifact:
1. **Start by linking `colors_and_type.css`** and pulling the brand variables. Never invent new colors.
2. **Headlines are always the compressed-caps display face** (`var(--font-display)`), all-caps, tight leading (0.9–0.95), accent red on the politically loaded word.
3. **Always overlay a texture** on photos and on the off-white paper background — never ship a clean flat surface.
4. **One photo, real, cropped tight**, never illustration, never stock-business smiles.
5. **No emoji. No soft shadows. No round corners > 4px. No gradients beyond a subtle texture multiply.**
6. **End with the gut-check** from the manual: Can I read it? Does the image read? Does it reinforce a revolutionary identity? Would it stop a scroll?

If the user invokes this skill without other guidance, ask what they want to make (post / story / thumbnail / slide / poster), what the headline + photo is, and whether the surface is light (paper) or dark (ink). Then build it as a static HTML artifact unless they ask for production code.
