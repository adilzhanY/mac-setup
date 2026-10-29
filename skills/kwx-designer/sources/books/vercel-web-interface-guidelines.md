# Vercel Web Interface Guidelines

- **Status:** free.
- **Legal source:** https://vercel.com/design/guidelines
- **Read:** the full guidelines (interactions, animations, layout, content, forms, performance, design, copywriting), October 2026.
- **Who:** Vercel's design team; grew out of Rauno Freiberg's interfaces.rauno.me. Widely adopted as a checklist by design engineers.

## Interactions

Keyboard everywhere per WAI-ARIA. `:focus-visible` rings, never covered by sticky elements; `:focus-within` for groups. Trap focus in modals and return it. Hit targets: if the visual is under 24px, expand the hit area to 24px; on mobile at least 44px. Mobile inputs 16px+ (or a viewport that prevents zoom). Never disable browser zoom. Hydration keeps focus and values. Never block paste. Loading buttons keep the label and add a spinner. Spinners: show delay about 150 to 300ms, minimum visible about 300 to 500ms. State in the URL (share, refresh, back). Optimistic UI with rollback or undo. Ellipsis on menu items that open a follow up and on in-progress labels. Confirm destructive actions or offer undo in a safe window. `touch-action: manipulation`. Set `-webkit-tap-highlight-color`. Forgiving controls with generous hit areas. Delay the first tooltip in a group, none for neighbours. `overscroll-behavior: contain` on modals and drawers; on fine pointers `overscroll-behavior: none` on html. Restore scroll on back and forward. Autofocus primary input on desktop, rarely mobile. Anything that looks interactive is interactive. Deep link filters, tabs, pagination, expanded panels. During drag: no text selection, `inert` on the dragged element. Every gesture has a click or keyboard alternative. Real links for navigation. Polite aria-live for async updates. Localize shortcuts for non QWERTY and show platform symbols.

## Animations

Reduced motion variants. Prefer CSS, then WAAPI, then JS libraries. Animate `transform` and `opacity`, not layout properties. Animate only to clarify cause and effect or for deliberate delight. Easing chosen by what changes. User input cancels animations. No autoplay; motion longer than 5s needs pause, stop or hide. Transforms anchored where the motion physically starts. Never `transition: all`. SVG: animate `<g>` wrappers with `transform-box: fill-box; transform-origin: center`.

## Layout

About 1px optical adjustments when optics beat geometry. Align every element to something intentional. Balance weight, size, spacing and colour when text and icons sit together. Test mobile, laptop, ultra wide (zoom to 50% to simulate). Respect safe areas with `env()`. Avoid unnecessary scrollbars; preview Windows behaviour with macOS scrollbars set to Always. Let flex, grid and intrinsic sizing lay out; do not measure in JS.

## Content

Inline help over tooltips. Skeletons match final content exactly. Accurate `<title>`. Every screen has a next step or recovery path. Design empty, sparse, dense and error states. Curly quotes. Avoid widows and orphans. Tabular numerals for comparisons. Never colour alone for status. Icons have text labels for assistive tech. Visually hidden labels keep accessible names. Single ellipsis character. `scroll-margin-top` on anchored headings. Handle short, average and very long user content. Locale formatting. Language from `Accept-Language` and `navigator.languages`, never IP or GPS. `translate="no"` on brand names and code. Accurate aria labels; decorative elements `aria-hidden`; verify the accessibility tree. Name icon-only buttons. Native HTML over ARIA. Hierarchical headings and a skip link. Captions and transcripts. Right click on the logo can surface brand assets. Non breaking spaces to keep units, shortcuts and names together.

## Forms

Enter submits a single input; with many controls, on the last one. Textarea: Cmd/Ctrl+Enter submits, Enter adds a line. Every control labelled; label click focuses. Submit enabled until submission starts, then disabled with spinner and an idempotency key. Do not block keystrokes, show validation. Do not disable submit before completion; let people submit and see errors. Checkbox and radio share one hit area with the label. Errors beside fields; focus the first error on submit. `autocomplete` and `name`. Spellcheck off for emails, codes, usernames. Correct `type` and `inputmode`. Placeholders end with an ellipsis and show an example. Warn before leaving with unsaved data. Support password managers and pasted one time codes; do not trigger them on non auth fields. Trim trailing whitespace. Explicit `background-color` and `color` on `<select>` for Windows dark mode.

## Performance

Test iOS Low Power Mode and macOS Safari; disable extensions when measuring; minimize re-renders; throttle CPU and network; batch DOM reads and writes; POST, PATCH and DELETE under 500ms; prefer uncontrolled inputs; virtualize long lists; preload above the fold images only, lazy load the rest; explicit image dimensions; preconnect to asset origins; preload critical fonts; subset with `unicode-range` and limit variable axes; heavy work in Web Workers; looping `<video>` instead of GIFs with a reduced motion still.

## Design

At least two shadow layers. Combine borders and shadows with semi transparent borders. Child radius at most the parent's and concentric. Tint borders, shadows and text toward the background hue. Colour blind friendly chart palettes. Prefer APCA over WCAG 2 for contrast. Hover, active and focus need more contrast than rest. `theme-color` matches the background. `color-scheme: dark` in dark themes. Blurry text after transforms: animate a wrapper or use `translateZ(0)` / `will-change: transform`. Avoid gradient banding from CSS masks.

## Copywriting (Vercel house style)

Active voice. Title Case for headings and buttons (Chicago) in product; sentence case on marketing pages. Be brief. "&" over "and". Action oriented language. Consistent terms. Second person. `YOUR_API_TOKEN_HERE` and `0123456789` as placeholders. Numerals for counts. Currency with 0 or 2 decimals, never mixed. Space (non breaking) between number and unit. Frame errors positively; errors explain the fix. Specific button labels ("Save API Key", not "Continue").

## Used in

`../../premium/details-and-polish.md`, `../../premium/motion-and-feel.md`, `../../premium/copywriting-and-tone.md`, `../../premium/materials-depth-light.md`, `../../premium/typography-craft.md`.
