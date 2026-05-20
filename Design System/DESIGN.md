---
name: RCI Media Design System
colors:
  # RCI Brand Palette
  red: "#da0d10"
  red-hot: "#e6002b"
  red-dark: "#8a0608"
  offwhite: "#f6efef"
  white: "#ffffff"
  ink: "#222222"
  ink-soft: "#3a3a3a"
  ash: "#6b6b6b"
  fog: "#c9c2c2"

  # Semantic Mappings
  primary: "{colors.red}"
  secondary: "{colors.ink}"
  tertiary: "{colors.red-hot}"
  neutral: "{colors.offwhite}"
  surface: "{colors.offwhite}"
  on-surface: "{colors.ink}"
  error: "{colors.red-hot}"

typography:
  headline-display:
    fontFamily: "Built Titling"
    fontSize: 120px
    fontWeight: 700
    lineHeight: 0.9
  headline-lg:
    fontFamily: "Built Titling"
    fontSize: 56px
    fontWeight: 700
    lineHeight: 0.9
    letterSpacing: 0.005em
  headline-md:
    fontFamily: "Built Titling"
    fontSize: 40px
    fontWeight: 700
    lineHeight: 0.92
  headline-sm:
    fontFamily: "Trade Gothic Next LT Pro"
    fontSize: 28px
    fontWeight: 800
    lineHeight: 1.0
    letterSpacing: 0.01em
  condensed:
    fontFamily: "Trade Gothic Next LT Pro Condensed"
    fontSize: 22px
    fontWeight: 700
    lineHeight: 1.0
    letterSpacing: 0.04em
  lead:
    fontFamily: "Khand"
    fontSize: 20px
    fontWeight: 500
    lineHeight: 1.2
  body-lg:
    fontFamily: "Cheltenham BT"
    fontSize: 19px
    fontWeight: 400
    lineHeight: 1.45
  body-md:
    fontFamily: "Codec Warm"
    fontSize: 17px
    fontWeight: 400
    lineHeight: 1.45
  body-sm:
    fontFamily: "Codec Warm"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.4
  label-eyebrow:
    fontFamily: "Trade Gothic Next LT Pro Condensed"
    fontSize: 13px
    fontWeight: 700
    lineHeight: 1.0
    letterSpacing: 0.18em

rounded:
  none: 0px
  sm: 2px
  md: 4px

spacing:
  base: 16px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 32px
  xl: 64px
  space-1: 4px
  space-2: 8px
  space-3: 12px
  space-4: 16px
  space-5: 24px
  space-6: 32px
  space-7: 48px
  space-8: 64px
  space-9: 96px

components:
  button-primary:
    backgroundColor: "{colors.red}"
    textColor: "{colors.offwhite}"
    rounded: "{rounded.none}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.red-dark}"
    textColor: "{colors.offwhite}"
  button-primary-active:
    backgroundColor: "{colors.red-dark}"
    textColor: "{colors.offwhite}"
  button-secondary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.offwhite}"
    rounded: "{rounded.none}"
    padding: 12px
  button-secondary-hover:
    backgroundColor: "{colors.ink-soft}"
    textColor: "{colors.offwhite}"
  card-article:
    backgroundColor: "{colors.offwhite}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "{spacing.space-4}"
  headline-slab:
    backgroundColor: "{colors.red}"
    textColor: "{colors.offwhite}"
    rounded: "{rounded.none}"
    padding: "8px 12px"
  badge-breaking:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.white}"
    rounded: "{rounded.sm}"
    padding: "4px 8px"
  badge-error:
    backgroundColor: "{colors.error}"
    textColor: "{colors.white}"
    rounded: "{rounded.sm}"
    padding: "4px 8px"
  divider:
    backgroundColor: "{colors.fog}"
    height: "2px"
  text-byline:
    textColor: "{colors.ash}"
---

# RCI Media Design System

## Overview
This design system distills the visual identity of the Revolutionary Communist International (RCI) Media Team. It is tailored for podcasts, social media, and YouTube content covering revolutionary history, theory, and analysis. The core aesthetic goals are **professional, serious, and revolutionary**. 

It achieves a high-contrast print-like appearance through a strict three-stop primary palette (red / off-white / ink), compressed display typography at heroic scales, hand-textured surfaces, and real photography—**never** illustration, generic icons, or smooth digital gradients.

## Colors
The color palette is strict for UI elements and overlays, and non-strict for photography. 
- **Primary Red (`--rci-red` / `#da0d10`):** Used for headlines, titles, key accents, link underlines, and ink stamp effects.
- **Accent Red (`--rci-red-hot` / `#e6002b`):** Reserved for banners, urgent notifications, and "BREAKING" tags.
- **Deep Red (`--rci-red-dark` / `#8a0608`):** Used for hover/pressed states of red UI surfaces.
- **Off-white Paper (`--rci-offwhite` / `#f6efef`):** The default background surface for all readable layouts. It mimics newsprint and is preferred over pure white.
- **Pure White (`--rci-white` / `#ffffff`):** Used only for flash highlights or photo cutouts.
- **Ink Black (`--rci-ink` / `#222222`):** Body text, heavy rules, and hard container surfaces.
- **Soft Ink (`--rci-ink-soft` / `#3a3a3a`):** Subtitle text and borders.
- **Ash (`--rci-ash` / `#6b6b6b`):** Metadata, bylines, and caption text.
- **Fog (`--rci-fog` / `#c9c2c2`):** Dividing lines and hairlines on paper backgrounds.

## Typography
The system utilizes a single compressed display sans-serif at heroic scale for headings, paired with editorial serifs and clean grotesque sans-serifs for body copy:
- **Headlines & Display:** Built Titling Bold (heavy, compressed, all-caps) establishes a bold, serious, and urgent tone. Headlines must always be in display caps, using tight leading (0.9 to 0.95).
- **Secondary Headings:** Trade Gothic Next LT Pro (or DIN Condensed/Oswald as fallbacks).
- **Long-form Body Copy:** Cheltenham BT (slab-serif styling resembling print newspapers).
- **UI & Minor Body Copy:** Codec Warm (humanist grotesque).
- **Subheads & Lead Paragraphs:** Khand (clean condensed).

## Layout
The layout model is print-inspired, mimicking physical posters and broadsheet newspapers:
- **Margins & Safe Zones:** Margins must be comfortable. Text must never touch the edges. Whitespace should live primarily in the margins, rather than in between elements.
- **Grid Alignment:** Use a strict 8px spacing grid. Maintain a single alignment format per composition (e.g., all-left, all-right, or justified). 
- **Scale Contrast:** Hierarchy must be dramatic. The primary headline should be roughly 3–5× the size of metadata or body text.
- **Photo Collages:** Layered photography, offset crops, and text slabs should be layered together, ensuring text always sits on a high-contrast background (red or ink slab).

## Elevation & Depth
The aesthetic is strictly flat-print; iOS-style shadows and glassmorphism are forbidden:
- **No Soft Drop Shadows:** Use flat, solid offset ink shadows instead (e.g., `6px 6px 0 #222222`) to create a stamped or layered paper feel.
- **No Translucency or Blur:** Avoid glassmorphism. Surfaces must be fully opaque red, ink, or off-white.
- **Borders & Dividers:** Use thick, solid borders (`2px` to `8px`) in ink black. Do not use subtle grey lines.
- **Hover & Active States:** 
  - On hover, red buttons darken to `--rci-red-dark`, and off-white surfaces darken by a 4% ink tint.
  - On press, the entire element offsets 1–2px (`transform: translate(2px, 2px)`) and its offset shadow disappears, producing a mechanical "stamp" feel.

## Shapes
Visual shapes reflect mechanical, editorial precision:
- **Sharp Corners:** All boxes, cards, and buttons use sharp `0px` corners by default. 
- **Minimal Rounding:** A maximum of `2px` or `4px` corner radius is allowed only on small tag chips or badges.
- **Photo Crops:** Photos must be cropped in strict rectangular shapes, never round (avatars are the only exception).

## Components
Components are defined by their hard edges, heavy outlines, and flat shadows:
- **Buttons:** Sharp corners, high contrast background and text, with flat `6px` offset shadows.
- **Headline Slabs:** Slabs of solid red or ink behind display text to guarantee legibility over photos.
- **Article Cards:** Sharp off-white paper containers bounded by thick ink-black borders.
- **Pull Quotes:** Bold serif styling with thick top and bottom dividers.

## Iconography
The system is type-and-photo first; icons are rare:
- **Lucide Icons:** Neutral geometric icons (2px stroke, no fill) may be used for tiny UI controls (play, links, chevrons).
- **Unicode Ornaments:** Geometric unicode shapes (■, ▶, →, ★, ✕) are encouraged as printer's marks inside display headers.
- **No Emojis:** Emojis are strictly banned to maintain the serious political register.
- **Photography as Symbols:** Prefer cropped real photographs (e.g., a clenched fist, a flag in a crowd) over generic illustrative icons.

## Content Fundamentals
- **Voice:** Authoritative, urgent, and collective (always use "we / our / comrades", avoid first-person singular "I" or influencer-style "you").
- **Mechanical Casing:** Headlines are always all-caps. Bolding must be used editorially to highlight the politically relevant phrase.
- **Length Caps:** Instagram captions under 220 characters; feed headlines 3–7 words; carousels capped at 10 panels.

## Do's and Don'ts
- **Do** bold the politically relevant phrase in body copy.
- **Do** overlay a faint paper or grain texture (e.g., multiply at 8–20% opacity) on solid backgrounds and photos.
- **Do** maintain WCAG AA contrast ratio (4.5:1) for all text elements.
- **Don't** use emojis, soft drop shadows, or rounded corners larger than 4px.
- **Don't** use stock illustrations or AI-generated images.
- **Don't** use tertiary colors or smooth gradients.
