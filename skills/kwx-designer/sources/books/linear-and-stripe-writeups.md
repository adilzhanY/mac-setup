# Linear and Stripe design writeups

## Linear: How we redesigned the Linear UI

- **Legal source:** https://linear.app/now/how-we-redesigned-the-linear-ui
- **Read:** full post, October 2026. (A guessed URL `linear.app/now/quality` returned 404; `linear.app/method` lists section titles only; Karri Saarinen's Lenny's Podcast page gives chapter titles only, so neither is quoted.)

**Colour system**
- Moved light and dark themes to LCH, a perceptually uniform space, so colours at the same lightness look equally light and generated themes are consistent.
- Theme generation went from 98 variables per theme to three inputs: base colour, accent colour, contrast. The contrast input produces high contrast themes for accessibility.
- Used less of the blue chrome colour in calculations for a more neutral, timeless look.
- Darkened text and neutral icons in light mode and lightened them in dark mode for readability.

**Typography:** Inter Display for headings (expression with readability), regular Inter for everything else.

**Density and alignment**
- Goal: "reduce visual noise, maintain visual alignment, and increase the hierarchy and density of navigation elements."
- Tested from very condensed to spacious; leaned on Apple's standards for a native app feel.
- Aligned sidebar and tab labels, icons and buttons vertically and horizontally: hard to notice at first, felt after a few minutes of use.

**Process:** navigation structure kept out of scope; hundreds of Figma explorations by Karri Saarinen before choosing a direction; small team, about six weeks; five milestones (stress tests, behaviour definitions, sidebar and chrome refresh behind a flag, private beta, GA); an internal toggle to compare old and new.

**Context from secondary sources (not quoted as Linear's words):** Linear prioritizes craft over A/B tests and metric goals; early work focuses on function, polish comes before general release; it hires for taste across roles; Saarinen (previously principal designer at Airbnb, founding designer at Coinbase) frames quality as the foundation, not an afterthought.

## Stripe: Designing accessible color systems

- **Legal source:** https://stripe.com/blog/accessible-color-systems
- **Read:** full post, October 2026.

**Goal:** predictable accessibility, clear vibrant hues, consistent visual weight across hues.

- HSL failed: its lightness is not perceptual (yellow looks lighter than blue at the same L). Stripe used CIELAB and built an internal tool to see changes live and what colours are possible.
- Original audit: none of the default small text colours except black met WCAG 2 (4.5:1 small text, 3:1 large).
- Darkening existing colours one step left some failing and others muddy. Instead every hue got the same lightness curve in Lab, keeping hue and saturation near the originals.
- Result: **any two colours at least five levels apart pass for small text; four levels apart pass for icons and large text.** Badges were fixed by moving background and text up one level each, with no per combination tuning.
- "Accessible doesn't mean vibrant": WCAG measures only contrast; vibrancy needs separate attention.
- Some combinations are impossible (dark, high chroma yellow); a visual tool exposes the limits quickly.

## Stripe Design Team reading list

- **Legal source:** https://www.stripe.press/recommended/design-books.html (39 books, credited to the team, no reasons given). Captured in `README.md`.

## Used in

`../../premium/materials-depth-light.md` (colour), `../../premium/details-and-polish.md` (alignment), `../../premium/typography-craft.md`.
