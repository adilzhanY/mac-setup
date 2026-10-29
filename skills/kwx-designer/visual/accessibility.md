# Accessibility

Accessible design is intuitive design under harder conditions: low vision, a keyboard, a screen reader, a shaky hand, a bright sun, a slow phone. Target WCAG 2.2 AA as the floor on every page.

## Contents

1. WCAG 2.2 AA essentials with numbers
2. Focus states
3. Targets and pointer input
4. Motion
5. Text, zoom and reflow
6. Semantics and screen readers
7. Forms and errors
8. Media and images
9. Testing without a browser
10. Review checklist

## 1. WCAG 2.2 AA essentials with numbers

| Criterion | Requirement |
|---|---|
| 1.1.1 Non-text content | Meaningful images have alt text; decorative ones `alt=""`. |
| 1.3.1 Info and relationships | Structure is in the markup (headings, lists, tables, labels), not only in the visuals. |
| 1.4.1 Use of colour | Colour is never the only signal. |
| 1.4.3 Contrast | Text 4.5:1, large text (24 px, or 18.66 px bold) 3:1. |
| 1.4.4 Resize text | 200 percent text size without loss of content. |
| 1.4.10 Reflow | No 2D scrolling at 320 CSS px width. |
| 1.4.11 Non-text contrast | 3:1 for UI component boundaries, meaningful icons, focus indicators, chart marks. |
| 1.4.12 Text spacing | Survives line height 1.5, paragraph spacing 2x, letter 0.12 em, word 0.16 em. |
| 1.4.13 Hover/focus content | Tooltips are dismissible (Esc), hoverable, persistent. |
| 2.1.1 Keyboard | Everything works by keyboard, with no traps. |
| 2.2.2 Pause, stop, hide | Anything that moves for more than 5 s, autoplays and sits beside other content has a pause control. |
| 2.3.1 Three flashes | Nothing flashes more than 3 times per second. |
| 2.4.1 Bypass blocks | A skip link to main content. |
| 2.4.3 Focus order | Tab order follows reading order. |
| 2.4.7 Focus visible | A visible focus indicator always. |
| 2.4.11 Focus not obscured (new in 2.2) | A focused element is never entirely hidden by sticky headers, cookie bars or chat widgets. |
| 2.5.7 Dragging movements (new) | Every drag has a single-pointer alternative (buttons, tap to select). |
| 2.5.8 Target size minimum (new) | Pointer targets at least 24 x 24 CSS px, or spaced so a 24 px circle around each does not overlap another. |
| 3.1.1 Language | `<html lang="en">` (and `lang` on passages in other languages). |
| 3.2.6 Consistent help (new) | Help links appear in the same relative place on every page. |
| 3.3.1 / 3.3.3 Errors | Errors identified in text, with a suggestion how to fix. |
| 3.3.7 Redundant entry (new) | Do not ask for the same information twice in one flow. |
| 3.3.8 Accessible authentication (new) | No cognitive tests to log in without an alternative; allow paste and password managers. |
| 4.1.2 Name, role, value | Custom controls expose their name, role and state. |

4.1.1 Parsing was removed in WCAG 2.2.

## 2. Focus states

Practical rules (Sara Soueidan, WCAG 2.4.13):

- Never `outline: none` without a replacement. Use `:focus-visible` so mouse clicks do not show the ring and keyboard users always see it.
- Use `outline`, not only `box-shadow`: outline does not shift layout and survives Windows forced colours mode.
- Thickness 2 px minimum, 3 px preferred; offset 2 px so it does not merge with the element.
- 3:1 contrast against adjacent colours, and 3:1 between focused and unfocused states.
- Two-tone ring works on any background:

```css
:focus-visible {
  outline: 3px solid var(--focus);   /* accent step 8 or 9 */
  outline-offset: 2px;
  box-shadow: 0 0 0 6px var(--bg);   /* inner halo keeps it visible on any fill */
}
```

- Dashed or dotted rings need about 4 px to reach the same area.
- Sticky headers: add `scroll-padding-top` equal to the header height so focused or anchored elements are not hidden (2.4.11).

## 3. Targets and pointer input

- Touch: 44 x 44 pt (Apple HIG) or 48 x 48 dp (Material). WCAG minimum is 24 x 24, which is a floor, not a goal.
- Expand small visual controls with padding or a pseudo-element hit area; the visual icon can stay 20 px.
- At least 8 px between adjacent targets on touch.
- Hover is a bonus, never the only way: wrap hover effects in `@media (hover: hover) and (pointer: fine)`.
- Every swipe, drag or pinch has a button alternative (carousel arrows, not only swipe).

## 4. Motion

- Respect `prefers-reduced-motion`. Best pattern: no motion by default, add it under `no-preference`:

```css
@media (prefers-reduced-motion: no-preference) {
  .reveal { animation: rise 400ms cubic-bezier(.2,.8,.2,1) both; }
}
```

- Under reduced motion remove: parallax, zooms, large slides, scroll-jacking, autoplaying video, animated gradients. Keep: short opacity fades (150 to 200 ms), colour changes, state changes that convey meaning.
- JS animation libraries: read `matchMedia('(prefers-reduced-motion: reduce)')` and listen for changes.
- Autoplaying hero video: muted, no audio track, a visible pause button, a poster image, and paused under reduced motion.
- Content must never depend on an entrance animation finishing. A hero that starts at `opacity: 0` and waits for JavaScript shows a blank page to slow devices, screenshots and some crawlers (observed on a Linear capture that rendered only the nav, and a Copilot Money capture caught mid fade).

## 5. Text, zoom and reflow

- Never disable zoom (`user-scalable=no` or `maximum-scale=1`).
- Font sizes in rem; layout tested at 200 percent text and 400 percent zoom.
- Inputs at least 16 px font on mobile, or iOS Safari zooms the page on focus.
- Minimum text anywhere: 12 px, and only for legal fine print and captions.

## 6. Semantics and screen readers

- Use native elements first: `<button>`, `<a href>`, `<input type="radio">`, `<details>`, `<dialog>`. ARIA is the fallback, not the default.
- Links go somewhere, buttons do something. A store badge is a link (`<a href="https://apps.apple.com/...">`) whose image has alt text "Download on the App Store".
- One `h1` per page; headings in order without skipping levels; landmarks `header`, `nav`, `main`, `footer`.
- Icon-only buttons need an accessible name (`aria-label="Close"`). Decorative icons get `aria-hidden="true"`.
- A billing toggle is a radio group or a pair of `aria-pressed` buttons with visible labels ("Monthly" / "Yearly"), not an unlabeled switch.
- Announce toasts and inline validation with `aria-live="polite"`.
- Pricing tables: real `<table>` with `<th scope>` for the comparison grid; checkmark cells need text ("Included") for screen readers.

## 7. Forms and errors

- Every input has a visible `<label>`; placeholder is not a label.
- `autocomplete` attributes (`email`, `name`, `one-time-code`), correct `type` and `inputmode`.
- Errors next to the field, in text, with how to fix; focus the first error on submit.
- Do not disable the submit button before the user tries; validate on submit and explain.

## 8. Media and images

- Videos: captions; a transcript for spoken content; no autoplay sound.
- Device screenshots in a hero: alt text describes what the screen shows ("Flight card showing a 43 minute delay and the reason"), not "screenshot".
- Text over images needs consistent contrast: add a scrim (gradient overlay) or place text on a solid area.

## 9. Testing without a browser

- Run `axe-core` or `pa11y` from the command line against the built HTML.
- Compute contrast for every token pair with a script (APCA `apca-w3` package and WCAG ratio).
- Grep for `outline: none`, `user-scalable`, `maximum-scale`, `font-size: 1[0-1]px`, missing `alt=`, `<div onclick`.
- Read the DOM order: it must match the visual order.
- Ask the user to try keyboard-only navigation and VoiceOver at the end; never drive their mouse or keyboard.

## 10. Review checklist

- [ ] Contrast meets 4.5:1 text, 3:1 large text and UI, in both themes.
- [ ] Visible `:focus-visible` ring, 2 to 3 px, 3:1, never hidden by sticky UI.
- [ ] Touch targets 44 px; nothing under 24 px.
- [ ] Reduced motion variant; no content gated behind animation.
- [ ] Zoom allowed; layout reflows at 320 px; text in rem.
- [ ] Native elements, one h1, ordered headings, skip link, `lang` set.
- [ ] Every image, icon button and badge has an accessible name.
