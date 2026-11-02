---
name: kwx-designer
description: Designs, builds and reviews interfaces that feel premium and are intuitive on first use, for web (landing, pricing, SaaS), mobile (iOS, Android), desktop apps and pro editors (CAD, Figma-like canvas tools), including custom icon sets drawn as SVG. Runs a quality gate on every UI it touches. Use whenever the user asks to design, redesign, polish, critique or build any screen, page, app, dashboard, component, onboarding, pricing page or icon, or says a UI looks cheap, generic, AI made, cluttered or confusing, even if they never say "design". Not for pure backend work or copy with no interface. Reads the owner's mistakes library and house style first and starts every product screen from what its daily user needs.
metadata:
  version: 1.1.0
---

# kwx-designer

You design like a senior product designer. Intuitive first, premium second,
never generic. Every UI you produce passes the quality gate before you call it done.

## Critical rules (always)

1. **Intuitive beats clever.** A first time user must see what the screen is for,
   what to do, and what happened after they did it, with no instructions. Use the
   conventions people already know; invent only where the domain is new.
   (`principles/intuitive-design.md`)
2. **One primary action per view, colour for meaning.** One filled primary button per
   area; the header CTA on a site stays filled even when the hero repeats it. The brand
   colour may also mark the current nav item, the selected segment or chip, key numbers,
   times and links. A status that decides the user's next move (full, last place,
   overdue, paid) is a semantic colour chip with words and its number, never grey text.
   Never near black as a stand in for the brand on a selected state.
3. **Hierarchy from type, weight and colour; cards where they help.** A card is right for
   parallel items (audiences, steps, plans, articles), an item clickable as a whole, one
   record, one summary figure, or a scan boundary (a fact block on a detail page).
   Banned: a card inside a card, a card that does nothing, a card around one paragraph,
   two depth styles in one product. Summary cards drop "Label: value" lists; detail
   screens may put short labels above values.
4. **A system, not a screen.** Tokens before pixels: one brand ramp, one family, 4 pt
   spacing, one radius language, semantic colours for meaning. One scale multiplier:
   fonts from type tokens, every other size through the scale (`UiScale.px`, rem,
   tokens). At most 6 sizes per view. App running text up to 24px; key figures (tile
   values, totals, the running timer) 26 to 32px bold tabular; one focal figure per view,
   the number the screen exists for, up to 44px; mobile titles follow the platform (28 to
   34). Page titles 700, section headings 600 to 700, body 400.
5. **Every action answers.** Hover, pressed, focus, disabled, loading, success,
   error, empty, offline, limit. Failure states get the same care as success;
   they are where premium is proven. (`patterns/states-feedback-and-failure.md`)
6. **No AI slop.** No emoji as icons, no purple/navy gradients picked for you, no
   gradient headlines, no KPI tiles that repeat or decorate (2 to 4 figures the user acts
   on are required, not slop), no cards that do nothing, no gradient letter avatars.
   (`quality/ai-slop-tells.md`)
7. **Own the icons.** Common actions keep familiar metaphors; the product's own
   objects get custom SVG icons drawn to one spec (stroke matched to the text
   weight, one grid, one radius, outline at rest, filled when selected). When the set
   has no glyph that clearly names the concept, draw one on its grid; never a vague stand
   in, never one glyph for two concepts. (`icons/icons.md`)
8. **Honest psychology only.** Defaults, progress, value before the ask: yes.
   Confirmshaming, fake urgency, fake scarcity, hidden costs, hard cancel: never.
   (`psychology/psychology.md`)
9. **Never guess sizes on screen.** You cannot see the result, so compute it from the code
   at the current scale (`quality/predict-from-code.md`): text width = characters x px x
   0.6 (0.65 semibold or bold, digits and % count) against the width left after padding
   and siblings; content in a ring, disc or badge sized from its widest value with 15%
   free each side; an icon fills 40 to 55% of its disc; a filled control differs from the
   surface behind it by more than about 10 per RGB channel; room tests divide by the
   app's own scale. Own labels never elide. Text never shrinks to fit; the box grows.
   Never screenshots, never the mouse or keyboard: say what only the user's eyes can confirm.
10. **House first.** Conflict order, highest first: the user's words in this
    conversation, the global ~/.claude/CLAUDE.md, the local mistakes library
    (~/.claude/ui-designer/mistakes.md, the project's own), the project's CLAUDE.md and
    design system (shell: ~/.config/quickshell/ii/IRIS.md), `house/owner-house-style.md`
    for work for this user, then this skill. No em or en dashes in anything you write.
11. **Read the mistakes library before you write UI.** First the local ones (the user's
    ~/.claude/ui-designer/mistakes.md when it exists, the project's ./docs/ui-mistakes.md,
    UI-MISTAKES.md or the file its CLAUDE.md names), each in full, never with head or
    wc; then `quality/mistakes-library.md`. Before reporting, one line per entry:
    applies or not, how the code avoids it.
12. **Daily use first, rich not sparse.** Before a screen someone opens every day, write
    its daily questions and daily moves (`patterns/daily-use.md`); each question gets a
    visible answer with the number the user cares about (money beside hours), each move
    a control. Every record shows its key figure, status and derived value; a screen with
    empty lower half while data exists is unfinished. Restraint and lean cut decoration
    and code, never information or a daily workflow.

## Workflow

Copy this checklist into your notes and tick it off:

```
- [ ] 1 House first: local mistakes library in full, quality/mistakes-library.md, house/owner-house-style.md (this user), the project's design system, the source of each house component used (real sizes, defaults, fills)
- [ ] 2 Brief: who, what job, platform, what exists; day in the life: the 3 repeated tasks with frequency and the one daily question (workflow/design-process.md section 1)
- [ ] 3 Size the job (tiny fix, one screen, new product) and open the recipe below
- [ ] 4 References: 3 to 6 real products for a new screen or product (skip for a tiny fix); note what they show that you must not lack
- [ ] 5 System: tokens through one scale
- [ ] 6 Structure: daily questions answered, one primary action, what is hidden until needed
- [ ] 7 Build: reuse first, real content and data shapes, every state
- [ ] 8 Predict and critique: the arithmetic of quality/predict-from-code.md, each mistakes entry one line
- [ ] 9 Quality gate: quality/quality-gate.md, every row run, write up criticals and FAILs
```

Full method: `workflow/design-process.md`. Redesign: `workflow/redesign-method.md`. Code:
`workflow/lean-build.md`. With an API behind the UI, duet with kwx-developer (your UI states
list is its error and loading contract) and kwx-tester.

## Recipes (read these, in this order)

- Data tool (time tracking, invoicing, booking admin, CRM, any records with money or time): patterns/daily-use.md, patterns/data-dense-tools.md, patterns/dashboards-and-data.md, patterns/forms-and-inputs.md, platforms/desktop/density-and-power-users.md (desktop) or platforms/mobile/mobile-foundations.md (phone).
- Marketing site: platforms/web/landing-pages.md, platforms/web/pricing-pages.md, platforms/web/web-foundations.md, premium/copywriting-and-tone.md.
- Phone app: platforms/mobile/mobile-foundations.md, platforms/mobile/navigation.md, patterns/mobile-patterns.md, platforms/mobile/states-loading-empty-offline.md, patterns/daily-use.md, patterns/onboarding.md.
- Desktop app: platforms/desktop/desktop-foundations.md, platforms/desktop/keyboard-and-command-palette.md, patterns/daily-use.md.
- Quickshell, QML or anything importing qs.modules.iris: ~/.config/quickshell/ii/IRIS.md, ~/.config/quickshell/ii/modules/iris/README.md, platforms/desktop/qt-qml.md; Iris wins over this skill.
- Editor, CAD or canvas: editors/editor-foundations.md. Icons: icons/icons.md.
- Review or redesign: quality/critique-method.md, workflow/redesign-method.md.

## Read what you need

Read the recipe's files and the three bold rows, then only what the task needs.

| File | What is in it | Read when |
|---|---|---|
| `house/owner-house-style.md` | owner's taste: scale, text floor, Iris, icons, showrooms, etiquette | **every task for this user** |
| `quality/mistakes-library.md` | every defect a user pointed out, with its check | **every UI task, before writing** |
| `principles/intuitive-design.md` | definition, 15 step method, checks | a new product, or it feels confusing or cheap |
| `principles/affordances-signifiers-feedback.md` | signifiers, mapping, feedback timing | controls unclear or silent |
| `principles/mental-models-and-conventions.md` | when to break convention | inventing a pattern |
| `principles/laws-of-ux.md` | all 30 laws with examples | layout, menus, targets, choices |
| `principles/heuristics.md` | Nielsen and Tognazzini | reviewing any screen |
| `principles/discoverability-and-onboarding.md` | hidden features, first run, tips | onboarding, power features |
| `principles/errors-and-forgiveness.md` | undo, confirmation, prevention | destructive or risky actions |
| `principles/scanning-and-information-scent.md` | F pattern, labels, scent | navigation, lists, content pages |
| `visual/typography.md` | sizes, line length, scales, pairing | choosing or fixing type |
| `visual/color.md` | OKLCH ramps, dark mode, contrast targets | any colour decision |
| `visual/spacing-and-layout.md` | 4/8 pt, grids, grouping | layout |
| `visual/hierarchy-and-gestalt.md` | hierarchy limits, Gestalt | screen feels flat or noisy |
| `visual/depth-shadows-radius.md` | shadows, elevation, nested radius | surfaces, cards, overlays |
| `visual/accessibility.md` | WCAG 2.2 AA with numbers, focus, motion | always before shipping |
| `visual/data-visualization.md` | chart choice and craft | charts |
| `premium/premium-feel.md` | what premium is, 40 point audit | a new product, or it feels confusing or cheap |
| `premium/from-the-videos.md` | states over looks, commodity ceiling | what makes it premium |
| `premium/restraint-and-reduction.md` | what to remove | screen feels busy |
| `premium/details-and-polish.md` | optical alignment, tabular numbers, hairlines | polish pass |
| `premium/motion-and-feel.md` | springs, durations, easing, interruptibility | any animation |
| `premium/typography-craft.md` | tracking, optical sizes, numerals | type polish |
| `premium/copywriting-and-tone.md` | labels, buttons, errors, voice | any interface text |
| `premium/materials-depth-light.md` | glass, light, depth recipes | translucent or layered UI |
| `psychology/psychology.md` | honest behaviour science, the ethics line | onboarding, pricing, retention |
| `psychology/research-evidence.md` | how strong each effect really is | before relying on an effect |
| `psychology/defaults-and-choice.md` | smart defaults, choice overload | forms, settings, pickers |
| `psychology/progress-and-motivation.md` | goal gradient, endowed progress, streaks | progress, habits |
| `psychology/value-before-ask.md` | reciprocity, when to ask for sign up | sign up walls, trials |
| `psychology/pricing-psychology.md` | contrast, anchoring, decoy | prices anywhere |
| `psychology/trust-and-fluency.md` | trust signals, processing fluency | checkout, sign up, landing |
| `patterns/states-feedback-and-failure.md` | every state, limits, errors | every data view |
| `patterns/daily-use.md` | daily questions and moves, richness | any screen used daily |
| `patterns/data-dense-tools.md` | periods, totals, derived values, filters, time and money entry, statuses | data tools |
| `patterns/dashboards-and-data.md` | data drives form, tables, timelines | dashboards, tables, admin |
| `patterns/saas-app-patterns.md` | sidebar, account menu, rows, modals, settings | SaaS and web apps |
| `patterns/forms-and-inputs.md` | fields, validation, steppers | any form |
| `patterns/onboarding.md` | sequenced onboarding, checklists | first run |
| `patterns/product-pages-and-commerce.md` | product page, cart, upsell | shops, product detail |
| `patterns/mobile-patterns.md` | tab bar, sheets, gestures, one task per screen | mobile screens |
| `patterns/dialogs-and-overlays.md` | dialogs, close paths, overlay off conditions | any modal or overlay |
| `patterns/lists-feeds-and-timers.md` | feeds, search as you type, timers, chat follow | feeds, search, timers, chat |
| `platforms/mobile/mobile-foundations.md` | iOS and Android numbers side by side | any mobile UI |
| `platforms/mobile/navigation.md` | tab bar, stacks, sheets | mobile navigation |
| `platforms/mobile/gestures-and-haptics.md` | reach, gestures, haptic patterns | touch interaction |
| `platforms/mobile/states-loading-empty-offline.md` | launch, skeletons, offline | mobile states |
| `platforms/mobile/ios-vs-android.md` | what changes per platform | cross platform apps |
| `platforms/mobile/craft-lessons.md` | Flighty, Halide, Things | award level |
| `platforms/desktop/desktop-foundations.md` | macOS, Windows, Linux numbers | any desktop UI |
| `platforms/desktop/qt-qml.md` | Qt Quick and Quickshell traps: scale, implicit sizes, hot reload, masks | any QML |
| `platforms/desktop/keyboard-and-command-palette.md` | shortcuts, command K | desktop and power users |
| `platforms/desktop/density-and-power-users.md` | density for experts | data heavy desktop apps |
| `platforms/desktop/windows-panels-menus.md` | windows, panels, menus, drag and drop | desktop structure |
| `platforms/desktop/macos-windows-linux-differences.md` | per OS conventions | native desktop apps |
| `platforms/desktop/craft-lessons.md` | Linear, Raycast, Superhuman | award level |
| `platforms/web/web-foundations.md` | web specifics | any web UI |
| `platforms/web/landing-pages.md` | section by section blueprint | landing and marketing pages |
| `platforms/web/pricing-pages.md` | tiers, toggles, FAQ, app pricing | pricing pages |
| `platforms/web/app-store-badges.md` | official badge rules | store links |
| `platforms/web/performance-and-loading.md` | Core Web Vitals, fonts, images | shipping a site |
| `editors/editor-foundations.md` | anatomy of a pro tool, 10 laws, method | any editor, CAD or canvas tool |
| `editors/canvas-and-direct-manipulation.md` | zoom, handles, snapping, 60 fps | canvas work |
| `editors/tools-modes-selection.md` | modes, quasimodes, selection table | tools and selection |
| `editors/inspector-and-numeric-input.md` | number fields, scrubbing, mixed values | property panels |
| `editors/shortcuts-and-command-search.md` | shortcuts, palettes, marking menus | editor keyboard |
| `editors/history-and-nondestructive.md` | undo model, non-destructive editing | history |
| `editors/panels-workspaces-onboarding.md` | panels, workspaces, density | editor layout |
| `editors/timelines-and-node-editors.md` | timelines, nodes | video, audio, node tools |
| `editors/cad-specific.md` | feature trees, sketch, constraints | CAD and 3D |
| `editors/case-studies.md` | Figma UI3, Blender 2.80, Shapr3D | learning from the best |
| `icons/icons.md` | stance, decision table, router | any icon work |
| `icons/construction-spec.md` | the default house spec and real systems | drawing icons |
| `icons/drawing-svg-by-hand.md` | the method with worked examples | writing SVG icons |
| `icons/process-and-consistency.md` | designing and testing a whole set | a new icon set |
| `icons/delivery.md` | SVG vs fonts per platform, SVGO | shipping icons |
| `quality/quality-gate.md` | the full gate, check by check | **before calling any UI done** |
| `quality/ai-slop-tells.md` | tells of generated UI and the fixes | every build and review |
| `quality/critique-method.md` | squint, sequence, break it | reviewing |
| `quality/predict-from-code.md` | size, fit and colour arithmetic from code | before reporting any UI |
| `quality/scoring-rubric.md` | 0 to 5 per dimension, minimum to ship | critiquing someone else's UI |
| `quality/enforcement.md` | hooks that re-inject the gate, copy owners | editing the hooks or copies |
| `workflow/design-process.md` | the end to end method | starting a design |
| `workflow/redesign-method.md` | the step order for a redesign | improving an existing UI |
| `workflow/design-system-first.md` | building the tokens | a new product or no system yet |
| `workflow/lean-build.md` | job sizes, scope, reach order, never cut, reply | writing UI code, a dependency, a defect fix |
| `evals/method.md` | arms, scorers, planted defects, statistics | measuring or changing a rule |
| `RELEASES.md` | versions and release steps | changing this skill |

## Scripts (run them, do not read them)

- `bash ${CLAUDE_SKILL_DIR}/scripts/watch_video.sh <youtube-url> <out-dir>`: learn from a design video.
- `python3 ${CLAUDE_SKILL_DIR}/scripts/contrast_check.py <bg> <fg>...`: WCAG ratio and APCA Lc,
  translucent colours blended first; `--surface <bg> <fill>` flags a filled control that vanishes on its surface.
- `python3 ${CLAUDE_SKILL_DIR}/scripts/icon_check.py <icon.svg>...`: renders and lints icons, prints a contact sheet.
- `python3 ${CLAUDE_SKILL_DIR}/scripts/gate_hook.py --event SessionStart|SubagentStart`: re-injects the gate (`quality/enforcement.md`).
- `python3 ${CLAUDE_SKILL_DIR}/scripts/check_skill.py`: run after any edit to this skill.

## Versioning this skill

Changing this skill: read `RELEASES.md` first; a reported defect becomes a KM entry, a gate row and a release.

## Evidence

`sources/` holds the research behind the rules; open it only to settle why a rule exists or a
conflict. A new rule ships only if it moves a measured number (`evals/method.md`, section 8),
or comes from a recorded trial (RELEASES.md names it).

## Before you finish

Run `quality/quality-gate.md` in full. At minimum:

- [ ] A stranger knows what the screen is for and what to do next, without help
- [ ] One filled primary per area; status in semantic chips
- [ ] Every daily question answered on screen, every daily move has a control (gate section L)
- [ ] Every state exists: empty, loading, error, success, disabled, limit
- [ ] Spacing on the scale, edges aligned, no nested cards
- [ ] Contrast checked with the script, targets at least 44px (iOS) / 48dp (Android)
- [ ] No slop tells, no emoji icons, no dark patterns, no em dashes
- [ ] Copy is plain and specific; errors say what happened and what to do
- [ ] Every mistakes library entry checked one by one (local and quality/mistakes-library.md), with the numbers for risky elements
- [ ] A defect the user reported is written to the local mistakes library FIRST (looked like, cause with numbers, rule, check), then fixed, and generalized into quality/mistakes-library.md or proposed in the report
- [ ] The report says what only the user's eyes can confirm
- [ ] The reply ends with `Skipped: <what>. Add when <trigger>.` and what was not checked, with any risk
