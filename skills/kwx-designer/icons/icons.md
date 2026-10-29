# Icons: the master file

Read this first for any icon work: a new icon, a set for a new product, a review of existing icons, or choosing between a pack and custom drawing. The other files go deeper:

- `construction-spec.md`: the house spec (canvas, padding, keyshapes, stroke, radii, gaps, angles, states, sizes), how to derive a spec from a project's typeface and brand, and the comparison table of real systems.
- `drawing-svg-by-hand.md`: the step by step method for drawing an icon as SVG code, with 3 worked icons and the common failure modes.
- `process-and-consistency.md`: designing a whole set (inventory, metaphor research, seed set, expansion), testing, lint and review, naming.
- `delivery.md`: shipping icons on web, React Native, iOS, Android and Qt/QML, SVGO settings, `currentColor`.
- `examples/`: the 3 worked icons as files (`lock.svg`, `deck.svg`, `calendar-check.svg`), the filled twin `lock-filled.svg`, and the reference keyshapes `ref-circle.svg` and `ref-square.svg` to put on every contact sheet.
- `../scripts/icon_check.py`: lints, renders, measures and previews icons, and builds a contact sheet. Run it on every icon you draw.

## Contents

1. The stance: own the icon system
2. The decision table: pack, hybrid or fully custom
3. The four rules every icon in a product shares
4. Restraint: fewer, smaller, labelled
5. The workflow in nine steps
6. The quality gate (run before handing anything over)

---

## 1. The stance: own the icon system

A premium app owns its icons. Icons pulled straight from a font or a stock pack, at the pack's default stroke and size, are one of the clearest signals that an interface was assembled rather than designed. Critics name Lucide and Heroicons at default settings, and "an icon in a tinted rounded square on every feature card", as the look of generated apps. The products with the most admired iconography (Apple SF Symbols, Figma UI3, Atlassian, Uber Base, Spotify, GitHub Octicons, Raycast, Shopify Polaris, IBM Carbon) all draw their own.

Owning the system does not mean inventing every glyph. It means **the specification is yours** and every icon on screen obeys it, whatever its origin. The reasons the big redraws give are concrete:

- **Typeface coherence.** SF Symbols come in nine weights matched to San Francisco and sit on its baseline. Uber drew its set and its typeface as "two expressions of one visual alphabet". Atlassian tuned its stroke to "the stroke of standard UI text". An icon set that shares stroke weight, terminal shape and vertical metrics with the UI font reads as one product.
- **Domain metaphors.** No pack ships "pull request", "auto layout" or a Linear style issue state. GitHub drew Octicons because stock icons had "metaphors that just barely fit". The product's own objects are where users look most and where packs fail.
- **A state language.** Outline at rest, filled when selected, with enough contrast that the change is visible (Uber's black on black selected state was invisible to many users).
- **No drift.** Mixed sources drift. Atlassian found 1,000+ team-drawn icons with conflicting meanings; Raycast's old set "combined icons from packs and custom variations".

The model is the **hybrid**, which Apple's HIG endorses directly: "Whether you use only custom icons or mix custom and system-provided ones, all interface icons in your app need to use a consistent size, level of detail, stroke thickness (or weight), and perspective."

- **Borrow the verbs, drawn to your spec.** Search, close, share, delete, settings, chevrons: users already know these pictures. Keep the familiar metaphor (a magnifier stays a magnifier) but redraw or tune it to your canvas, stroke, caps and radii. Redrawing "trash" into a new metaphor buys nothing and costs learnability.
- **Own the nouns, drawn custom.** The product's own objects, states and features get original drawings on the same grid, so the two halves cannot be told apart.

Be honest about the evidence: no user research or A/B test was found that shows users notice or prefer custom icons. The case rests on craft, coherence and domain fit. That is enough, but never claim a measured preference.

## 2. The decision table: pack, hybrid or fully custom

Answer from the top; the first row that matches wins.

| Situation | Do this | Why |
|---|---|---|
| Native Apple app (iOS, iPadOS, macOS, watchOS, visionOS) | SF Symbols for everything they cover; custom symbols made from an exported SF template only for missing concepts | Free weight matching, Dynamic Type, accessibility and OS upgrades; custom art takes all of that on |
| Licence forbids the pack where you need it (SF Symbols in a logo or app icon, Polaris outside Shopify apps) | Draw custom | Licence, not taste |
| Prototype, features still changing weekly | One pack, tuned once: stroke matched to the text stem, size, corner style (`construction-spec.md` section 7) | A custom set gives dozens of icons and a permanent backlog; wait until the noun list is stable |
| Shipping product, one team, under ~50 product nouns (the default case) | **Hybrid**: a base pack retuned to the house spec for verbs, custom icons for every product noun, all checked by `icon_check.py` | Best ratio of craft to cost |
| The user asks for a premium, distinctive look, or the brand has a strong typeface | Fully custom set, verbs redrawn with conventional metaphors, nouns invented | The spec and the drawing hand are both yours |
| Many surfaces, several teams, or a public extension API | Fully owned set with a written spec, naming rules, metadata, lint in CI, contact sheet review | Drift is the failure mode at scale (Atlassian, Uber, Raycast) |
| Expressive brand moments (empty states, onboarding, category tabs) | Illustration or brand iconography, a separate track from UI glyphs | Brand style overpowered Atlassian's UI when used as glyphs; Airbnb's 3D icons are brand, not utility |

A pack is not bad. A pack used **at its defaults, decoratively, everywhere, mixed with another pack** is. If you keep a pack, retune it and add the missing nouns on its grid. The user's own shell does exactly this: Lucide built into a font at 2px, plus hand-drawn `iris-*.svg` glyphs on Lucide's grid for concepts Lucide lacks (edge tabs, the notch, Grit, dictation, workspaces) in `~/.local/share/lucide/custom/`.

## 3. The four rules every icon in a product shares

Every redraw in the research (Atlassian, Uber, Spotify, Raycast) was triggered by breaking one of these, never by the mere use of a pack. They are non-negotiable, whatever the icon's origin:

1. **One canvas and padding.** Same viewBox, same live area, same keyshape sizes.
2. **One stroke, matched to the stem of the body text** at the size the icon is shown. Never mix stroke widths inside a set.
3. **One corner and terminal rule.** Same caps, joins and radius rule everywhere (round caps with radius 2, or square caps with sharp corners, never both).
4. **One state rule.** Outline at rest, filled (same silhouette) when selected or active, and the difference survives the brand colour and dark mode.

The numbers for each live in `construction-spec.md`.

## 4. Restraint: fewer, smaller, labelled

Premium is also about the icons you do not draw. Linear's 2026 refresh earned its calm look by **reducing icon use, scaling icons down and removing coloured icon backgrounds**. Jon Hicks's test: remove the icon first and see whether the design works without it.

- Do not put an icon on every nav item, card, list row and heading. If every item has one, keep only the one that matters most (the cart, the primary action) or drop them all.
- No "icon in a tinted rounded square" on feature cards unless the brand truly needs it.
- Label icons with visible text by default. NN/g found only home, print and the magnifier for search widely recognised; hover-only labels fail on touch. Icon-only is allowed for the universal few, for dense pro toolbars with tooltips, and for media controls.
- If you need more than five seconds to think of an icon for a concept, the concept needs a label, not an icon (NN/g).
- Never rely on colour alone for meaning; pair it with shape.

## 5. The workflow in nine steps

1. **Read the project.** Find its existing icons, UI font, body size, corner radii and icon sizes. Check for a project spec file. If none, use the house spec in `construction-spec.md`, adjusted by its section 7.
2. **Inventory.** List every concept that needs an icon and mark each one verb (shared) or noun (product's own). Cut the ones that fail the restraint test. (`process-and-consistency.md` section 1)
3. **Metaphor.** For each concept, find the convention first; invent only when none exists. Write the metaphor in one sentence. (`process-and-consistency.md` section 2)
4. **Seed set.** Draw the reference circle and square plus 4 to 6 icons that exercise every rule (badge, diagonal, inner gap, organic shape, dense icon). (`process-and-consistency.md` section 3)
5. **Draw each icon in words, then in code.** Primitives first, integer coordinates, the fixed root element. (`drawing-svg-by-hand.md`)
6. **Check each icon.** `python3 ~/.claude/skills/kwx-designer/scripts/icon_check.py <files>`; fix every error and warning or justify it in one line.
7. **Check the family.** Open the contact sheet PNG the script prints and compare weight, size and style across the set, light and dark.
8. **Check in context.** Put the icons into the real UI next to real text at real size, light and dark. (`process-and-consistency.md` section 5)
9. **Ship.** Export per platform with `currentColor` and accessible markup. (`delivery.md`)

## 6. The quality gate (run before handing anything over)

Every line must be true. Each one is checkable.

- [ ] Every icon passed `icon_check.py` with 0 errors; every remaining warning has a written reason.
- [ ] Root element identical across the set (same viewBox, stroke-width, caps, joins); children carry geometry only.
- [ ] Stroke matches the text stem rule in `construction-spec.md` section 7, written down with the measured stem.
- [ ] Contact sheet reviewed: no icon visibly heavier, lighter, larger or smaller than its neighbours (coverage within the family's range, see `process-and-consistency.md` section 5).
- [ ] Verbs use the conventional metaphor; every new metaphor passed a recognition check (`process-and-consistency.md` section 5).
- [ ] No two icons in the set share a meaning, and no single icon carries two meanings.
- [ ] Selected and resting states differ by fill, not only by colour, and both are visible on light and dark.
- [ ] Icons sit next to text with their optical centre on the text's cap height middle, at the size given by the spec.
- [ ] Every icon button has an accessible name describing the action (`delivery.md` section 2).
- [ ] No emoji, no Unicode symbols as icons, no hard-coded colours inside the SVG.
- [ ] The restraint test was applied: every icon left on screen earns its place.
