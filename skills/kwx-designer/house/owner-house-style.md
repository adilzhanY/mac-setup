# Owner house style

Read this for ANY UI work for this user: the owner's Quickshell shell and the Iris apps (Koima, Grit, Tetik, Settings, kadr, Kezek, Aspan, Korme), and the owner's own web, mobile and desktop products. It is the owner's taste and house rules, distilled from what the owner polished for months, so that an agent using kwx-designer knows what the owner's own ui-designer agent knows.

## Contents

1. Order of authority and sources
2. Sizes and the one scale
3. Type
4. Icons
5. The Iris look in short
6. Where Iris applies
7. Motion
8. Behaviour
9. Showing options
10. Testing etiquette
11. Defect loop and output
12. Chrome and speed
13. Checks

---

## 1. Order of authority and sources

Highest first (the same order as SKILL.md rule 10):

1. The user's words in this conversation.
2. The global `~/.claude/CLAUDE.md`.
3. The local mistakes library `~/.claude/ui-designer/mistakes.md` (and a project's own one).
4. The project's CLAUDE.md and design system. For the shell: `~/.config/quickshell/ii/IRIS.md` and `~/.config/quickshell/ii/modules/iris/README.md`. For a product: its brand and its token file.
5. This file.
6. The rest of kwx-designer.

Sources this file distils. Open them when a rule here is unclear or seems to conflict: `~/.claude/CLAUDE.md`, `~/.claude/agents/ui-designer.md`, `~/.claude/ui-designer/mistakes.md`, IRIS.md, `modules/iris/README.md`, and the memory notes in `~/.claude/projects/-home-wopler/memory/` (glass-design-system, mac-look-project, iris-*, korme*, no-pointer-moves-for-tests, user-tests-shell-himself, system-ui-font-open-runde, lavish-use-sparingly and the other UI notes).

Palettes, part sizes, panel widths, radii and motion milliseconds live in IRIS.md and the Iris README. This file points at them instead of copying their tables, because a copy drifts.

## 2. Sizes and the one scale

- All shell sizing lives in `~/.config/quickshell/ii/modules/common/UiScale.qml`. Its `scale` property (1.1 now) multiplies every font size, dimension and radius at once. To resize the whole shell, change `scale` and nothing else.
- Fonts only from `Appearance.font.pixelSize.*`. At scale 1.0: smallest 12, smaller 13, smallie 15, small 16, normal 18 (body), large 20, larger 22, huge 25, hugeass 27; multiply by the scale for the real px. Never a literal font size, never below `smallest`. Text too big for its box means a bigger box, never smaller text.
- Every other pixel value goes through `UiScale.px(n)`, which is round(n x scale), or a named metric (`UiScale.rowHeight`, `controlSmall`, `fieldHeight`, `chartHeight`, `cardPadding`). Prefer the named metric when one fits.
- Never scale `Appearance.sizes.hyprlandGapsOut` (must match the compositor's gap), the `barShortenScreenWidthThreshold` values (comparisons against hardware pixels), `Appearance.rounding.full` (a pill sentinel) or `screenRounding`.
- Every "is there room" test accounts for the scale. A 1920 px screen at 1.25 lays out like 1536 px. In BarContent this is `Appearance.font.pixelSize.normal >= 22`, which means scale 1.25 and up (KM6).
- Editing a singleton may keep serving old values on a hot reload (Appearance's inline QtObject blocks did). If a singleton change seems to do nothing, verify with a value written somewhere you can observe instead of assuming it is live.
- Iris measures (row heights, disc sizes, panel widths): IRIS.md "Sizes".

## 3. Type

- The owner likes text on the large side. Shell body is 19.8 px (normal at 1.1), the floor 13.2 px (smallest at 1.1). When unsure, take the larger size and grow the box.
- The owner's own products: web and mobile body at least 16 px, desktop body at least 14 px, captions never below 12 px, the screen's key figure bold and tabular at the focal size (SKILL.md rule 4).
- Secondary text is quieter by colour, not by shrinking.
- Families: the shell uses SF Pro Rounded, bold globally, DemiBold for current or emphasised items. The system UI font is Open Runde (`appearance.fonts.ui.family`). The terminal font is Ioskeley Mono. The lock screen clock is SF Pro Display (Rounded was "too rounded" there).
- Weight is set only through `font.weight` (Settings > Fonts writes `appearance.fonts.weight` and `titleWeight`). Never put a ",Regular" styleName in kdeglobals and never relabel font faces: both broke weights across Qt once.
- Every font must cover Kazakh, Russian and German letters (`visual/typography.md` section 6 coverage rule). The owner types Kazakh.
- Browsers need their own restart to pick up a font change; say so instead of calling it live.

## 4. Icons

- Plain and light. The owner chose Lucide over Hugeicons (too detailed), at stroke 2.0, not 2.5.
- A custom icon is one simple object, never a stacked logo like composition (a stacked `iris_clipboard` was rejected).
- In the shell, `MaterialSymbol { text: "name" }` maps the name to a Lucide Shell glyph; IrisDisc takes `icon:`. Brand marks are images tinted with ColorOverlay.
- No emoji and no Unicode symbol used as an icon anywhere: no lock, lightning, check or star characters in any label.
- When Lucide has no glyph that clearly names the concept, draw one. The steps (iris-<name>.svg, aliases.json, manual-map.json, rebuild, `install -m644`, restart with Ctrl+Super+R and `koima --daemon`) are in `icons/icons.md` "No vague stand in".

## 5. The Iris look in short

- Surfaces are pieces of the black bezel growing out of a screen edge, not cards floating over the desktop.
- Black in day and night. Iris does not follow the light or dark theme.
- Square where a surface meets its edge, concave fillets into the edge, soft corners facing the desktop, and a ring of wallpaper (5 px, the compositor gap) around the outline.
- White means on: the on control, the main action and the current item are white with black glyphs. Everything else is dark grey on black.
- Depth from three greys (ink, raised, raisedHover). No glass, blur, shadows or accent colours; the search pill keeps its smoked glass. Danger red only for destructive actions.
- Floating app windows (Koima, Settings, kadr, Grit's window) use the same palette and parts without fillets or band.
- Build from `import qs.modules.iris` parts. Never redraw a part the library has. Translucency follows `Iris.surfaceOpacity`.
- Before building an edge surface, read IRIS.md "Building an edge surface: gotchas" in full.

## 6. Where Iris applies

- The owner moved from end-4 Material to Glass to Iris, wanting a panel that is "mine, not Apple's". Never propose Material or liquid glass as the default for the owner's desktop. The glass Control Center and the mac style notification cards are saved alternatives, not the direction.
- A product with its own brand (torq, belegfrei, nordwand, stundenwerk) uses its brand palette and type. Every non Iris rule in this file still applies to it: the one scale, the text floor, the icon rules, testing etiquette, the defect loop.
- Iris is never the look of a client product. Black and white only, with no semantic colours, would be wrong for a tool that must show status and money.

## 7. Motion

- Surfaces grow out of their edge and go back in. They never fade in mid screen.
- Closing is quicker than opening and has no bounce.
- Content arrives after the body; rows stagger in after it (KM10).
- Durations, easings and springs come from the `Iris.*` constants (IRIS.md "Motion", the Iris README). Never invent new numbers per component.
- Every Iris layer has `no_anim` and `blur = false` in `~/.config/hypr/custom/rules.lua`, because it draws its own motion.
- Qt spring calibration for anything outside Iris: `premium/motion-and-feel.md` "Qt/QML springs".

## 8. Behaviour

- Lists are keyboard first: Up/Down or j/k move, Enter opens, Left/Right or h/l go up and in, `/` or Ctrl+F searches, Ctrl+1..9 jumps.
- Esc steps back one level; it closes the surface only from its top level. Right click goes deeper inside the same surface.
- Live state from the real services, never placeholder values, also in prototypes.
- Nothing destructive on hover. Destructive actions sit behind "..." or a right click menu, then a confirm (KM7).
- Date sorts never put folders first.

## 9. Showing options

- When a look is not decided, show 2 to 4 named directions.
- QML ideas go to Korme (`~/dev/korme`, the /korme skill): one QML file per idea whose root implicit size is the stage, then `korme new`, `korme add`, `korme open`, and END THE TURN. Never `korme poll` or `lavish-axi poll`; the owner answers in chat. Read `korme show <id>` only when the owner says there are comments.
- If the owner says "don't run it", only compile check with a `Qt.createComponent` harness.
- An idea imports only modules that `korme.qml` imports (KM12).
- Web comparisons go to a lavish page; diagrams there are always Mermaid. A quick follow up question is answered in chat, not in a new page.

## 10. Testing etiquette

- Never move the pointer, click, type, focus or move windows, open panels on the owner's screens, set up screenshot watchers, or ask the owner to trigger a capture. The owner tests visual changes.
- A test that must open a window runs only on workspace 3 (HDMI-A-2), and only after asking.
- Shell: a change is live only when "Reloading configuration" plus "Configuration Loaded" appear in `qs log -c ii` after your last write of every changed file (KM15). `sed -i` or a bare `touch` may not trigger a reload; rewrite the file with its own content. A new inline component in an already loaded file, anchors, layer and window structure changes and new fonts need a restart. Watch the log for "polish() loop" and binding errors.
- Parallel agents on the shell: each owns its folders and takes the shell lock around every save (wait about 3 s, check the log, release). The main agent commits into `~/arch-config`.
- End with what only the owner's eyes can confirm.

## 11. Defect loop and output

- A defect the owner reports goes into `~/.claude/ui-designer/mistakes.md` first (what it looked like, the cause with numbers, the rule, the check), then the fix, then a generalized KM entry in `quality/mistakes-library.md`.
- Every review lists each mistakes library entry it checked, one line each.
- No em or en dashes anywhere: copy, code, comments, commit messages, file contents.
- Never a watermark, a credit line, a generator meta tag naming Claude or Anthropic, hidden text, or an EXIF or XMP credit. If a tool adds one on its own, say so and offer `exiftool -all= -overwrite_original <file>`.
- Desktop changes are committed and pushed as CLAUDE.md says (one change per commit, a one line message, no attribution).

## 12. Chrome and speed

- No chrome the owner does not use. The owner removed the traffic lights from Settings, the window title and the dark mode toggle from the bar, and the workspace grid from Spotlight; Koima shows previews only on a file click.
- Fast is premium to the owner. Apps stay resident so they open instantly. Wheel scroll moves 120 px per notch with 220 ms OutCubic. Transient surfaces leave in about 150 ms.
- When something clearly looks off, even outside your change, fix it or list it in the report.

## 13. Checks

| Rule | Check |
|---|---|
| One scale | `grep -nE 'pixelSize: *[0-9]'` over changed QML is empty; bare numbers in size properties each justified |
| Text floor | No size below `Appearance.font.pixelSize.smallest` (shell) or 12 px (products) |
| Icons | Emoji grep of quality-gate.md section 15 is clean; every concept has its own glyph |
| Iris parts | Changed shell files import `qs.modules.iris` and reuse its parts |
| Destructive | No destructive handler reachable from a hover revealed control |
| Live claim | A reload pair in `qs log -c ii` after the last write of each changed file |
| Etiquette | No pointer, keyboard, focus or screenshot commands in the transcript |
| Output | `grep -nP '[\x{2013}\x{2014}]'` over every touched file is empty; no credit or generator tag |
| Report | Mistakes library entries listed one by one; "Only your eyes can confirm" present |
