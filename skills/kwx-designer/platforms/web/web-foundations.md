# Web foundations

The baseline every web page meets before any visual polish. Condensed from Vercel's Web Interface Guidelines (vercel.com/design/guidelines), web.dev and WCAG 2.2, rewritten as testable rules.

## Contents

1. Document setup
2. Interactions
3. Navigation and state
4. Forms
5. Content and copy details
6. Visual details
7. Motion
8. Responsive behaviour
9. Review checklist

## 1. Document setup

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">  <!-- never maximum-scale or user-scalable=no -->
  <title>Appname: one line saying what it does</title>
  <meta name="description" content="150 to 160 characters, the value proposition in plain words.">
  <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#101114" media="(prefers-color-scheme: dark)">
  <meta name="color-scheme" content="light dark">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">  <!-- 180 x 180 -->
  <meta property="og:title" content="..."><meta property="og:image" content="/og.png"> <!-- 1200 x 630 -->
  <link rel="canonical" href="https://example.com/">
</head>
```

- `theme-color` matches the page background in each scheme (Vercel). `color-scheme` makes form controls and scrollbars follow the theme.
- One `h1`, landmarks (`header`, `nav`, `main`, `footer`), a skip link as the first focusable element.
- Page title accurate to the current context; social preview image designed, not a default screenshot.

## 2. Interactions

- Everything works with the keyboard; visible `:focus-visible` ring on every focusable element (see `visual/accessibility.md`).
- Hit target matches or exceeds the visual: expand anything under 24 px to 24 px on desktop, 44 px on touch.
- Anything that looks interactive is interactive; anything interactive looks it. Cursor `pointer` only on links and buttons.
- Navigation uses real `<a href>`, so cmd-click, middle-click and "open in new tab" work. Buttons for actions.
- Button loading state keeps the label and adds a spinner; delay spinners about 150 to 300 ms and keep them at least about 300 to 500 ms to avoid flicker.
- Confirm destructive actions or offer Undo.
- `touch-action: manipulation` on controls removes the double-tap zoom delay; style `-webkit-tap-highlight-color` instead of leaving the default grey flash.
- Hover effects only under `@media (hover: hover) and (pointer: fine)`; touch devices get pressed states instead.
- Tooltips: delay the first, show peers instantly; never put essential information only in a tooltip. Prefer inline help.
- Never disable paste, zoom or text selection on content.
- Every drag, swipe or pinch has a tap or keyboard alternative.

## 3. Navigation and state

- Put UI state in the URL (tabs, filters, billing period on a pricing page: `?billing=yearly`) so refresh, share and Back work.
- Read and write it with `URLSearchParams` (`getAll("tag")` for repeated keys, `append` to build them). Every value comes back as a string (`"2"`), so parse and validate it where it is read: a URL is user input.
- `history.replaceState` while a filter is typed or a slider dragged, `pushState` only for a real step (another tab, another page of results), so Back is not one entry per keystroke.
- Restore scroll position on Back. Anchored headings get `scroll-margin-top` equal to the sticky header height.
- Sticky headers: 56 to 72 px tall on desktop, 48 to 64 on mobile; they must not cover focused elements.
- Mobile menu: a full-height sheet with large targets, closes on Esc, traps focus while open, returns focus to the menu button on close.

## 4. Forms

- Every control has a visible label; clicking the label focuses the control.
- Correct `type`, `inputmode` and `autocomplete` (an email waitlist field: `type="email" autocomplete="email" inputmode="email" spellcheck="false"`).
- Input text at least 16 px on mobile (iOS zooms otherwise).
- Enter submits single-field forms. Keep submit enabled until submission starts, then disable it and show progress; send an idempotency key.
- Errors beside the field, in text, focus the first error on submit. Placeholders show an example and end with an ellipsis.
- Success state replaces the form with a clear confirmation ("You are on the list. We will email you at name@example.com on launch day.").

## 5. Content and copy details

- Curly quotes, the single ellipsis character, non-breaking spaces in `10&nbsp;MB`, `Cmd&nbsp;K`, and brand names.
- Tabular numerals for prices, comparisons and counters.
- Format dates, numbers and currency with `Intl` for the visitor's locale; detect language from browser settings, not IP.
- Never hardcode the locale (`"en-US"`) in a formatter that claims to be locale aware: pass `undefined` or `navigator.languages`. Take the currency code from the data, never from the locale: a German visitor sees a USD price as `1.234.567,89 $`.
- Never write user or server text into `innerHTML` with a template string (`${item.title}` is an injection hole): set `textContent` or let the framework escape it. In QML a `Text` defaults to `Text.AutoText` and renders anything that looks like markup, so labels that show user text set `textFormat: Text.PlainText`.
- Design empty, loading, error, sparse and very long content states; skeletons match the final layout.
- Never rely on colour alone; icon-only buttons get an accessible name.
- Specific labels: "Join the waitlist", "Start free trial", "Compare plans". Not "Continue", "Submit", "Learn more" everywhere.
- Sentence case for marketing headings and buttons reads friendlier and scans faster than Title Case.

## 6. Visual details

- Layer at least two shadows; combine with a semi-transparent border (see `visual/depth-shadows-radius.md`).
- Nested radii concentric. Borders, shadows and muted text tinted toward the background hue.
- Hover, active and focus states have more contrast than rest.
- Gradients: use `in oklch` interpolation and a subtle noise or background image to avoid banding on large areas.
- Scrollbars: hide only the ones that should not exist; never hide a scrollbar on scrollable content.
- `-webkit-font-smoothing: antialiased` on dark backgrounds on macOS for lighter-looking text; leave default on light.

## 7. Motion

- Provide a reduced-motion variant; prefer CSS, then the Web Animations API, then JS libraries.
- Animate only `transform` and `opacity`; never `transition: all`.
- Durations: 150 to 250 ms for small UI (hover, toggles), 250 to 400 ms for panels and sheets, 400 to 700 ms for one hero entrance. Ease out for entering, ease in for leaving.
- User input cancels running animations. No autoplay except muted, non-essential loops with a pause control.
- Transform origin starts where the motion physically begins (a menu grows from its button).
- Content is visible without JavaScript and without the animation finishing.

## 8. Responsive behaviour

- Test at 360, 390, 768, 1024, 1280, 1440, 1920 px and at 50 percent zoom.
- Respect `env(safe-area-inset-*)`; use `100dvh` instead of `100vh` for full-height mobile sections (the URL bar changes `vh`).
- Images: `width` and `height` attributes on every `<img>` to prevent layout shift; `srcset` and `sizes` for responsive images.
- Let CSS size things (Grid, Flexbox, `clamp()`, container queries); never measure with JavaScript for layout.

## 9. Review checklist

- [ ] `lang`, viewport without zoom lock, `theme-color` per scheme, `color-scheme`, title, description, OG image.
- [ ] One h1, landmarks, skip link, real links for navigation.
- [ ] Focus visible everywhere; targets 24 px desktop, 44 px touch.
- [ ] Hover effects gated by `(hover: hover)`.
- [ ] State in the URL; scroll margin under sticky header.
- [ ] Forms labelled, typed, autocomplete set, 16 px inputs.
- [ ] Only transform and opacity animated; reduced motion handled; no content behind animation.
- [ ] No layout shift from images, fonts or late banners.
