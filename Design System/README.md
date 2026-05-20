# RCI Media — Design System

**Revolutionary Communist International — Media Team**
Podcasts · Social media · Long-form YouTube on revolutionary history, theory & analysis.

This design system distills the brand guidance from the source manual
(**Manual de Identidad Visual** of the Partido Comunista Revolucionario, the
Mexican section that originated the visual language now used by the RCI media
team) into a reusable kit: tokens, fonts, textures, components and ready-made
templates for the kinds of artifacts the team ships every day —
**article posts, story posts, podcast covers, YouTube thumbnails, video
title cards** and **internal slide decks**.

The visual identity is **professional, serious, and revolutionary**. It does
this through a tight three-stop palette (red / off-white / ink), a single
compressed sans-serif at heroic scale, hand-textured surfaces (paper, paint,
film grain), and real photography of comrades, marches and meetings —
**never** illustration, illustration-style icons, or stock gradients.

---

## Sources

| Source | Provided as | Stored here |
|---|---|---|
| **Manual de Identidad Visual — PCR** (PDF, 30pp, Spanish) | `uploads/Manual-de-Identidad-Visual-PCR.pdf` | Text extracted and summarized below. The PDF references Instagram handles **@marxismomx** and **@revcomintern** as the real-world reference accounts. |
| **TextureLabs grunge / film pack** (20 high-res JPGs) | `uploads/Texturelabs_*.jpg`, `uploads/Texturelabs_Film_*.jpg` | Curated subset downsized & saved to `assets/textures/`. |
| **AU-FG film/grain texture pack** (8K JPGs) | `uploads/AU-FG-Texture*.jpg` | Curated subset in `assets/textures/`. |

No Figma or codebase was supplied. If/when the team has them, paste links in
this README so future runs can pull the real source of truth (Figma library,
existing post template files, the actual logo SVGs, the licensed font files).

---

## Index — what lives in this folder

| Path | What it is |
|---|---|
| `README.md` | This file. Context + content & visual foundations + iconography. |
| `SKILL.md` | Cross-compatible skill file (works as an Agent Skill in Claude Code). |
| `colors_and_type.css` | Color tokens, font stack, type scale, spacing, semantic element styles. **Import this first.** |
| `fonts/` | Licensed brand fonts — Built Titling (full family + italics), Trade Gothic Next LT Pro Heavy, Revolution Gothic (full family). Wired up in `colors_and_type.css`. |
| `assets/logos/` | `rci-square.svg` (social icon) + `rci-flag-en.svg` (English wordmark/flag). |
| `assets/textures/` | **70+** curated, web-sized textures — paper (50 variants, `paper-NNN.jpg`), grunge (`grunge-NNN.jpg`, `grunge-light-specks.jpg`, `grunge-peeled-paint.jpg`, `halftone-mesh.jpg`), film grain (`film-grain.jpg`, `film-158.jpg`), AU-FG film stock (`au-fg-1/4/7.jpg`), and an alternative red paper (`red-paper-alt.jpg`). |
| `assets/icons/` | The icon set used inline (Lucide via CDN — see Iconography). |
| `preview/` | One HTML card per token / component, rendered into the Design System tab. |
| `ui_kits/instagram/` | Instagram post & story templates (article extract, podcast promo, book review, date post). |
| `ui_kits/youtube/` | YouTube thumbnail + video title-card templates. |
| `slides/` | Internal-deck slide templates (title, big quote, section divider, comparison, photo-bleed). |
| `pdf_pages/` | (empty) — PDF page renders skipped due to render-time limits; see Caveats. |

---

## Content Fundamentals

The team writes like an organizer making a poster, not like a brand
ghost-writing copy. The guiding principle, lifted straight from the manual,
is **less is more.** Or, as Lenin put it: *“Better fewer, but better.”*

### Voice & tone
- **Authoritative, urgent, organized.** Every piece is recruitment-adjacent:
  the first contact a potential comrade has with the party is usually a post
  or a sticker, so the question every artifact must pass is — *do we look
  professional? serious? revolutionary?*
- **Collective, not personal.** "We / our / comrades." First-person
  plural always. **Avoid "I"**. Avoid
  influencer/lifestyle "you."- **Polemical, named, specific.** Name the bourgeoisie, the state, the boss,
  the party by name. No vague "stakeholders," no euphemism.
- **Hook-first.** Titles are made to stop a scroll, not to summarize.

### Casing & mechanics
- **HEADLINES IN ALL CAPS.** Built Titling / Anton style. Hard-edged compressed
  sans. Body copy is sentence case.
- **Bold the politically relevant phrase** inside body copy. The manual is
  explicit about this — bolding is editorial, not decorative.
- **No emoji.** None. Not even one. The political register is too serious;
  emoji read as social-media-manager-speak and dilute the message.
- **No exclamation-mark inflation.** One exclamation, used like a slogan,
  is fine. Strings of exclamations are not.
- **Quotation marks are typographic** (curly), not straight.
- **Numbers are spelled out under 10** in body copy; digits are fine in
  posters and data callouts where impact matters.

### Length
- Caption: **≤ 220 chars** for Instagram feed, ≤ 70 for a video sub.
- Headline on a post: **3–7 words**, two lines max.
- Carousel: **≤ 10 panels.** The manual explicitly caps this.
- Video: **< 3 min** for reels; longer-form is OK on YouTube but cut filler.

### Concrete examples (from the manual / observed posts)
- *“TRUMP FACES AN IMPOSSIBLE DILEMMA — against an Iran that has the advantage”*
  → headline + secondary clause, both in display caps, accent red on the verb.
- *“TORNEL RUBBER, A STRIKE UNDER ATTACK BY MANAGEMENT”* → name the place,
  name the action, name the antagonist. No editorializing in the title; the
  body does the analysis.
- *“LESS IS MORE — or as Lenin would say: ‘Better fewer, but better.’”*
  → quotes a leader by name, deploys the quote as the rule, not as decoration.

### What to do before publishing (the manual's gut-check)
> 1. Can I read it?
> 2. Is the image legible?
> 3. Does the image reinforce our identity as a revolutionary organization?
> 4. Would it stop me while I was walking past, or scrolling?

---

## Visual Foundations

### Palette

| Token | Hex | Use |
|---|---|---|
| `--rci-red` | `#da0d10` | Primary. Title accents, link hits, ink-stamps. |
| `--rci-red-hot` | `#e6002b` | Accent / alarm. Banners, urgent stickers, "BREAKING". |
| `--rci-red-dark` | `#8a0608` | Hover/pressed state of red surfaces; oil-ink overprints. |
| `--rci-offwhite` | `#f6efef` | Default paper. Use over `#ffffff` everywhere unless flash highlight. |
| `--rci-white` | `#ffffff` | Flash white. Highlights, photo cutouts. |
| `--rci-ink` | `#222222` | Body text. Heavy rules. Hard surfaces. |

The palette is **strict for UI/chrome** and **non-strict for photography** —
photos can carry their own color, but anything overlaid (text, bars, frames,
logos) lives in these stops. No tertiary colors, no purples, no greens, no
gradient swatches.

### Type

**Headline (mandatory):** Built Titling Bold — compressed, all-caps, heavy.
This is the single most identity-defining element of the system. Anything
that is a title — poster, post headline, video subtitle, podcast cover — uses
this face.

**Secondary (subtitles, body on posters):** Trade Gothic Next LT Pro;
DIN Condensed for very dense overlays. Khand is the friendlier subhead.

**Long-form body (articles, captions):** Cheltenham BT Regular — slab-serif
weight that reads like newspaper editorial.

**Additional acceptable faces:** Revolution Gothic (extra bold), Khand
(bold/medium), Eastman Compressed.

**Substitutions used in this design system:** The brand fonts are
**commercial** and were not provided as files. The closest free analogues
on Google Fonts are loaded by `colors_and_type.css`:

| Original | Loaded font | Notes |
|---|---|---|
| Built Titling Bold | **Built Titling** ✓ | Full family in `/fonts` (EL/LT/RG/SB/BD + italics). First in display stack. |
| Trade Gothic Next LT Pro | **Trade Gothic Next LT Pro** ✓ | Full family: LT/RG/BD/HV + italics. First in headline + body stacks. |
| Trade Gothic Next LT Pro Condensed | **Trade Gothic Next LT Pro Condensed** ✓ | Cn / BdCn / HvCn + italics. Backs `--font-condensed`. |
| Trade Gothic Next LT Pro Compressed | **Trade Gothic Next LT Pro Compressed** ✓ | Cm / HvCm + standalone Compressed. Backs `--font-compressed`. |
| Revolution Gothic (extra bold) | **Revolution Gothic** ✓ | Full family (EL/LT/RG/EB + italics). Available via `--font-accent`. |
| Cheltenham BT Regular | **Cheltenham BT** ✓ | RG / IT / BD / BD-IT. Backs `--font-serif`. |
| Codec Warm | **Codec Warm** ✓ | Light → Heavy + italics. Body/UI font — backs `--font-body` and `--font-ui`. |
| Athelas | **Athelas** ✓ | Regular only. Alternative serif via `--font-serif-alt`. |
| Khand | **Khand** ✓ | Google Fonts; backs `--font-subhead`. |
| DIN Condensed | Oswald (substitute) | Acceptable fallback inside `--font-condensed` stack. |
| Eastman Compressed | Saira Condensed (substitute) | Acceptable fallback inside `--font-compressed` stack. |

> ✓ All licensed brand fonts present — the only remaining substitutes are
> DIN Condensed and Eastman Compressed, kept as fallbacks within the
> condensed / compressed stacks.

### Backgrounds & surfaces

The default surface is **off-white paper (`#f6efef`) with a faint paper or
film-grain texture** overlaid at 8–20% opacity, multiply-blended. The
secondary surface is **flat ink (`#222222`) with film grain on top**. The
red is **never** a full-bleed surface for body copy — only for poster
headlines, callouts, stickers, and the occasional title bar.

**Composition is collage.** Layered photography, cut and offset, with text
sitting on a red or ink slab so it always passes contrast. Photos are
real (marches, mitins, meetings, prensa) — never stock, never illustration.

### Imagery — color & treatment

- Warm, slightly **desaturated, contrasty** — like a hand-printed poster.
- Acceptable to push to **duotone red+ink** when photo quality is low or
  when the photo competes with other on-page color.
- **Grain is always on.** A film grain or paper texture sits over every
  photo at low opacity. This is what gives the brand its hand-printed feel.
- Avoid: smooth product shots, glossy gradients, AI-generated portraits,
  pristine stock photography.

### Layout rules

- **Text never touches the edge.** Comfortable margins; whitespace lives
  in the margins, not as islands in the middle of the composition.
- **One alignment per composition.** Left, right, justified or centered —
  pick one; columns are encouraged where columns are appropriate.
- **Rule of thirds.** The hero photo and the title sit on the thirds, not
  centered for the sake of centering.
- **Hierarchy is dramatic.** Title is roughly **3–5×** the size of metadata.
  Date/time is smaller than venue; venue is smaller than title.

### Borders, rules, capsules

- Borders are **hard, ink-coloured, 2–8px**. No subtle 1px greys.
- Pills/capsules are **square** corners by default (`--radius-0`).
  A 2px round is the maximum we use, only on small chips/badges
  (`--radius-1`, `--radius-2`).
- **No protection gradients.** When text sits on a photo, it sits on a
  solid red or ink slab, not a fade.

### Shadows / elevation

- **No soft drop shadows.** Ever.
- Use **offset ink shadows** (`6px 6px 0 #222`) for poster-style call-outs
  and the occasional button-press "stamped" feel.
- Photos can carry a faint **inner edge vignette** if they need it, but
  not a glow.

### Corner radii

- **0–4px** across the whole system. Posters and headline slabs are always
  sharp. Buttons may use 0–2px. Photos are rectangular crops, never circles
  (avatars excluded — the avatar in a thumbnail credit is fine round).

### Transparency & blur

- **Transparency** is reserved for the texture overlays (paper, grain) —
  8–20% multiply. Never for translucent UI panels.
- **Blur** is not used. No glassmorphism. The aesthetic is print, not iOS.

### Hover / press

- **Hover:** primary red → `--rci-red-dark`. Off-white surface → `+4%` ink
  tint (i.e. background gets slightly darker, no shadow change).
- **Press:** the whole element nudges 1–2px on both axes
  (`transform: translate(2px, 2px)`) and the offset shadow disappears,
  reading like a stamp pressed into paper.
- **Focus:** 2px ink outline, 2px offset. No glow.

### Animation

- **Animation is minimal and editorial**, not playful.
  - Posters/title cards: hold-cut. No animation.
  - Reels/shorts: hard cuts, **rapid 100–250ms** ease-outs on supers and
    lower-thirds. Text "stamps" onto the screen — small overshoot, no bounce.
  - Easings: `cubic-bezier(0.2, 0.7, 0.1, 1)` for entries; linear for grain
    drift.
  - **No spring physics**, no parallax, no fades-into-place beyond 250ms.

---

## Iconography & logos

The brand is **type-and-photo first** — icons are intentionally rare. When
icons are used, the rules are:

- **Lucide** (CDN) is the default icon set — thin-stroke, 2px, no fill.
  Loaded from `https://unpkg.com/lucide@latest`. Used for small UI
  affordances only: play, link, chevron, share, calendar.
  **Substitution flag:** Lucide is not what the source manual uses (the
  manual doesn't specify an icon system at all). It is chosen as the
  closest open-source match for "minimal, geometric, neutral." If the
  team has their own set, swap it in.
- **Emoji: never.** Already covered in Content Fundamentals — they break
  the political register.
- **Unicode shapes** (`■`, `▶`, `→`, `★`, `✕`) are acceptable as
  typographic ornaments inside the display face, where they read as
  printer's marks rather than icons.
- **Logos:** the brand provides two master logos, both red (`#EA1917`)
  with a white sickle-and-R glyph:
  - `assets/logos/rci-square.svg` — the universal social-media square
    icon (1156×1156 viewBox). Use this as the avatar, thumbnail badge,
    Stories sticker, and footer mark. **Default to this everywhere a
    small mark is needed.**
  - `assets/logos/rci-flag-en.svg` — the English horizontal flag/wordmark
    (1106×644 viewBox). Use this when a wider lockup is wanted (deck
    title slide, channel banner, article header).
  Note the brand red on the master logos is `#EA1917` — a near-twin of
  the manual's `#DA0D10`. The system uses `#DA0D10` as the canonical
  UI red; the logos sit happily next to it.
- **Photos as icons.** The manual's strongest "iconography" is the
  photo-as-symbol — a clenched fist in a march photo, a flag in a crowd
  shot. Where a feature would normally take an icon, prefer a cropped
  real photo.

---

## Caveats & known limitations

- **PDF page renders skipped** — the source manual is a 30-page PDF;
  rendering each page to PNG kept hitting the script timeout. The
  *text* of the manual was extracted in full and informs every section
  above; only the in-PDF photo grids and the original logo lockups were
  not extracted as images.
- **Real logo files ✓** — the team's master logos (`rci-square.svg`,
  `rci-flag-en.svg`) are in `assets/logos/`. The earlier typographic
  placeholders have been removed; all kits and slides reference the real
  files.
- **Homepage URL** — every artifact defaults to `marxist.com` in its
  footer lockup. The Instagram handles (`@revcomintern`, `@marxismomx`)
  remain on channel-specific surfaces only.
- **Brand fonts fully wired up** — Built Titling (full family + italics),
  Trade Gothic Next LT Pro Heavy, and Revolution Gothic (full family) are
  all loaded via `@font-face`. Only Cheltenham BT, DIN Condensed and Eastman
  Compressed remain on Google-Fonts substitutes (IBM Plex Serif, Oswald,
  Saira Condensed respectively).
- **Photography placeholders** — UI kit & slide examples use generic
  Unsplash CDN photos (B&W, march-style framing) as stand-ins. Replace
  with real `@revcomintern` photography.
- **No Figma, no codebase** — UI kits were built from the manual + the
  team's stated workflow alone. If a Figma library or existing post
  template files exist, paste them in and re-run.
