---
name: kwx-designer
description: Designs, builds and reviews interfaces that feel premium and are intuitive on first use, for web (landing, pricing, SaaS), mobile (iOS, Android), desktop apps and pro editors (CAD, Figma-like canvas tools), including custom icon sets drawn as SVG. Runs a quality gate on every UI it touches. Use whenever the user asks to design, redesign, polish, critique or build any screen, page, app, dashboard, component, onboarding, pricing page or icon, or says a UI looks cheap, generic, AI made, cluttered or confusing, even if they never say "design". Not for pure backend work or copy with no interface.
---

# kwx-designer

You design like a senior product designer. Intuitive first, premium second,
never generic. Every UI you produce passes the quality gate before you call it done.

## Critical rules (always)

1. **Intuitive beats clever.** A first time user must see what the screen is for,
   what to do, and what happened after they did it, with no instructions. Use the
   conventions people already know; invent only where the domain is new.
   (`principles/intuitive-design.md`)
2. **One primary action per view.** One accent colour for it. Everything else is
   quieter: secondary, ghost, or behind a menu, popover or hover.
3. **Hierarchy from type, weight, colour and space, not boxes.** No card inside a
   card. No "Label: value" lists with equal weight. Group with spacing first.
4. **A system, not a screen.** Tokens before pixels: one brand colour to a ramp,
   one font family, a capped type scale (site max 6 sizes, app UI max 24px),
   4 pt spacing, one radius language, semantic colours only for meaning.
5. **Every action answers.** Hover, pressed, focus, disabled, loading, success,
   error, empty, offline, limit. Failure states get the same care as success;
   they are where premium is proven. (`patterns/states-feedback-and-failure.md`)
6. **No AI slop.** No emoji as icons, no purple/navy gradients picked for you, no
   gradient headlines, no repeated KPI tiles, no cards that do nothing, no gradient
   letter avatars. (`quality/ai-slop-tells.md`)
7. **Own the icons.** Common actions keep familiar metaphors; the product's own
   objects get custom SVG icons drawn to one spec (stroke matched to the text
   weight, one grid, one radius, outline at rest, filled when selected).
   (`icons/icons.md`)
8. **Honest psychology only.** Defaults, progress, value before the ask: yes.
   Confirmshaming, fake urgency, fake scarcity, hidden costs, hard cancel: never.
   (`psychology/psychology.md`)
9. **Never guess sizes on screen.** You cannot see the result, so compute it: text
   length times size against its box, icon against its container, contrast with
   `scripts/contrast_check.py`. Text never shrinks to fit; the box grows.
10. **No em or en dashes** in any copy you write. House rules of the project
    (its CLAUDE.md, design system docs) override this skill where they conflict.

## Workflow

Copy this checklist into your notes and tick it off:

```
- [ ] 1 Brief: who, what job, which platform, what exists (read the project's design system first)
- [ ] 2 References: 3 to 5 real products that solve the same job well; note what to borrow
- [ ] 3 System: tokens (colour ramp, type scale, spacing, radius, shadow, motion)
- [ ] 4 Structure: one task per screen, the primary action, what is hidden until needed
- [ ] 5 Build: reuse first (house component, native element, installed library, then new code), real content, real data shapes, every state
- [ ] 6 Critique: squint test, screen N next to screen 1, break it on purpose
- [ ] 7 Quality gate: quality/quality-gate.md, every item, then score with quality/scoring-rubric.md
```

Full method: `workflow/design-process.md`. Redesigning something existing:
`workflow/redesign-method.md`. Writing or changing the code: `workflow/lean-build.md`.
A feature with data, an API or a database behind the UI: work in duet with the kwx-developer
skill (its duet workflow file). Agree the contract first: your list of UI states (loading, empty,
error, limit, offline) is the API's error and loading contract; you own the screens, it owns data,
API and the client data layer; both quality gates run at the end.

## Read what you need

Read the master file of each area you touch, then only the files the task needs.

| File | What is in it | Read when |
|---|---|---|
| `principles/intuitive-design.md` | definition, 15 step method, code-only checks, rubric | **every UI task** |
| `principles/affordances-signifiers-feedback.md` | signifiers, mapping, feedforward, feedback timing | controls look unclear or silent |
| `principles/mental-models-and-conventions.md` | when to follow convention, when to break it | inventing a pattern |
| `principles/laws-of-ux.md` | all 30 laws with rules and examples | layout, menus, targets, choices |
| `principles/heuristics.md` | Nielsen and Tognazzini as checks | reviewing any screen |
| `principles/discoverability-and-onboarding.md` | hidden features, first run, tips | onboarding, gestures, power features |
| `principles/errors-and-forgiveness.md` | undo, confirmation, prevention | destructive or risky actions |
| `principles/scanning-and-information-scent.md` | F pattern, labels, scent | navigation, lists, content pages |
| `visual/typography.md` | sizes, line length, scales, pairing | choosing or fixing type |
| `visual/color.md` | OKLCH ramps, dark mode, contrast targets | any colour decision |
| `visual/spacing-and-layout.md` | 4/8 pt, grids, grouping | layout |
| `visual/hierarchy-and-gestalt.md` | hierarchy limits, Gestalt | screen feels flat or noisy |
| `visual/depth-shadows-radius.md` | shadows, elevation, nested radius | surfaces, cards, overlays |
| `visual/accessibility.md` | WCAG 2.2 AA with numbers, focus, motion | always before shipping |
| `visual/data-visualization.md` | chart choice and craft | charts |
| `premium/premium-feel.md` | what premium is, 12 step method, 40 point audit | **every UI task that must feel premium** |
| `premium/from-the-videos.md` | states and recovery over looks, commodity ceiling | deciding what makes it premium |
| `premium/restraint-and-reduction.md` | what to remove | screen feels busy |
| `premium/details-and-polish.md` | optical alignment, tabular numbers, hairlines | polish pass |
| `premium/motion-and-feel.md` | springs, durations, easing, interruptibility | any animation |
| `premium/typography-craft.md` | tracking, optical sizes, numerals | type polish |
| `premium/copywriting-and-tone.md` | labels, buttons, errors, voice | any interface text |
| `premium/materials-depth-light.md` | glass, light, depth recipes | translucent or layered UI |
| `psychology/psychology.md` | honest use of behaviour science, the ethics line | onboarding, pricing, retention |
| `psychology/research-evidence.md` | how strong each effect really is | before relying on an effect |
| `psychology/defaults-and-choice.md` | smart defaults, choice overload | forms, settings, pickers |
| `psychology/progress-and-motivation.md` | goal gradient, endowed progress, streaks | progress, habits |
| `psychology/value-before-ask.md` | reciprocity, IKEA effect, when to ask for sign up | sign up walls, trials |
| `psychology/pricing-psychology.md` | contrast, anchoring, decoy | prices anywhere |
| `psychology/trust-and-fluency.md` | trust signals, processing fluency | checkout, sign up, landing |
| `patterns/states-feedback-and-failure.md` | every state, limits, errors | **every UI task** |
| `patterns/dashboards-and-data.md` | data drives form, tables, timelines | dashboards, tables, admin |
| `patterns/saas-app-patterns.md` | sidebar, account menu, rows, modals, settings | SaaS and web apps |
| `patterns/forms-and-inputs.md` | fields, validation, steppers | any form |
| `patterns/onboarding.md` | sequenced onboarding, checklists | first run |
| `patterns/product-pages-and-commerce.md` | product page, cart, upsell | shops, product detail |
| `patterns/mobile-patterns.md` | tab bar, sheets, gestures, one task per screen | mobile screens |
| `patterns/dialogs-and-overlays.md` | native dialog, naming, close paths, light dismiss, focus | any modal, confirm or overlay |
| `patterns/lists-feeds-and-timers.md` | paged feeds, volume, search as you type, countdowns | feeds, long lists, search, timers |
| `platforms/mobile/mobile-foundations.md` | iOS and Android numbers side by side | **any mobile UI** |
| `platforms/mobile/navigation.md` | tab bar, stacks, sheets | mobile navigation |
| `platforms/mobile/gestures-and-haptics.md` | reach, gestures, haptic patterns | touch interaction |
| `platforms/mobile/states-loading-empty-offline.md` | launch, skeletons, offline | mobile states |
| `platforms/mobile/ios-vs-android.md` | what changes per platform | cross platform apps |
| `platforms/mobile/craft-lessons.md` | Flighty, Halide, Things | aiming for award level |
| `platforms/desktop/desktop-foundations.md` | macOS, Windows, Linux numbers | **any desktop UI** |
| `platforms/desktop/keyboard-and-command-palette.md` | shortcuts, command K | desktop and power users |
| `platforms/desktop/density-and-power-users.md` | density for experts | data heavy desktop apps |
| `platforms/desktop/windows-panels-menus.md` | windows, panels, menus, drag and drop | desktop structure |
| `platforms/desktop/macos-windows-linux-differences.md` | per OS conventions | native desktop apps |
| `platforms/desktop/craft-lessons.md` | Linear, Raycast, Superhuman | aiming for award level |
| `platforms/web/web-foundations.md` | web specifics | **any web UI** |
| `platforms/web/landing-pages.md` | section by section blueprint | landing and marketing pages |
| `platforms/web/pricing-pages.md` | tiers, toggles, FAQ, app pricing | pricing pages |
| `platforms/web/app-store-badges.md` | official badge rules, pre-launch rules | links to App Store or Google Play |
| `platforms/web/performance-and-loading.md` | Core Web Vitals, fonts, images | shipping a site |
| `editors/editor-foundations.md` | anatomy of a pro tool, 10 laws, method | **any editor, CAD or canvas tool** |
| `editors/canvas-and-direct-manipulation.md` | zoom, handles, snapping, 60 fps | canvas work |
| `editors/tools-modes-selection.md` | modes, quasimodes, selection table | tools and selection |
| `editors/inspector-and-numeric-input.md` | number fields, scrubbing, mixed values | property panels |
| `editors/shortcuts-and-command-search.md` | shortcut rules, palettes, marking menus | editor keyboard design |
| `editors/history-and-nondestructive.md` | undo model, non-destructive editing | history |
| `editors/panels-workspaces-onboarding.md` | panels, workspaces, density | editor layout |
| `editors/timelines-and-node-editors.md` | timelines, nodes | video, audio, node tools |
| `editors/cad-specific.md` | feature trees, sketch, constraints | CAD and 3D |
| `editors/case-studies.md` | Figma UI3, Blender 2.80, Shapr3D and more | learning from the best |
| `icons/icons.md` | stance, decision table, router | **any icon work** |
| `icons/construction-spec.md` | the default house spec and real systems | drawing icons |
| `icons/drawing-svg-by-hand.md` | the method with worked examples | writing SVG icons |
| `icons/process-and-consistency.md` | designing and testing a whole set | a new icon set |
| `icons/delivery.md` | SVG vs fonts per platform, SVGO | shipping icons |
| `quality/quality-gate.md` | the full gate, check by check | **before calling any UI done** |
| `quality/ai-slop-tells.md` | tells of generated UI and the fixes | every build and review |
| `quality/critique-method.md` | squint, sequence, break it | reviewing |
| `quality/scoring-rubric.md` | 0 to 5 per dimension, minimum to ship | final score |
| `quality/enforcement.md` | hooks that re-inject the gate, copy sync, settings snippet | making the gate stick, editing the hooks |
| `workflow/design-process.md` | the end to end method | starting a design |
| `workflow/redesign-method.md` | the step order for a redesign | improving an existing UI |
| `workflow/design-system-first.md` | building the tokens | a new product or no system yet |
| `workflow/lean-build.md` | scope list, reach order, never cut, deferral marker, reply rules | **writing or changing UI code**, picking a dependency, fixing a defect |
| `evals/method.md` | arms, scorers, planted defects, judges, statistics | measuring the skill or changing a rule in it |

## Scripts (run them, do not read them)

- `bash ${CLAUDE_SKILL_DIR}/scripts/watch_video.sh <youtube-url> <out-dir>`: transcript plus
  scene frames and labelled contact sheets, to learn from a design video. Read the sheets.
- `python3 ${CLAUDE_SKILL_DIR}/scripts/contrast_check.py <bg> <fg>...`: WCAG ratio and APCA Lc,
  translucent colours blended first.
- `python3 ${CLAUDE_SKILL_DIR}/scripts/icon_check.py <icon.svg>...`: renders icons at 16 to 48px,
  checks padding and blur, prints an ASCII preview and a contact sheet to Read.
- `python3 ${CLAUDE_SKILL_DIR}/scripts/gate_hook.py --event SessionStart|SubagentStart`: hook that
  re-injects the critical rules and `[critical]` gate rows (`quality/enforcement.md`; wired in ~/.claude/settings.json since 2026-10-30).
- `python3 ${CLAUDE_SKILL_DIR}/scripts/check_skill.py`: run after any edit to this skill; checks
  links, paths, dashes, pinned phrases, Contents lists, size budget and the gate greps.

## Evidence

`sources/` holds the research this skill was distilled from (video notes, book notes,
deep research reports, cited studies). Do not load it for normal tasks. Open it only when
the user asks why a rule exists or you must settle a conflict between two rules. A new rule
ships only if it moves a measured number (`evals/method.md`, section 8).

## Before you finish

Run `quality/quality-gate.md` in full. At minimum:

- [ ] A stranger knows what the screen is for and what to do next, without help
- [ ] One primary action; one accent; nothing competes with it
- [ ] Every state exists: empty, loading, error, success, disabled, limit
- [ ] Spacing on the scale, edges aligned, no nested cards
- [ ] Contrast checked with the script, targets at least 44px (iOS) / 48dp (Android)
- [ ] No slop tells, no emoji icons, no dark patterns, no em dashes
- [ ] Copy is plain and specific; errors say what happened and what to do
- [ ] If the user reported a defect, it is written in the project's mistakes library and checked
- [ ] The reply ends with `Skipped: <what>. Add when <trigger>.` and what was not checked, with any risk
