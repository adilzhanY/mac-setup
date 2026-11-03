# UI and UX design

## When this playbook applies

- Design or build a screen: "make a settings page", "design the dashboard home".
- Design a flow: signup, onboarding, checkout, password reset, multi step forms.
- Redesign or polish: "make it look less cheap", "clean up this page".
- Build or extend a design system: tokens, components, variants, documentation.
- Accessibility work: "make it accessible", "pass an audit", keyboard and screen reader support.
- Critique: "review this design", "why do users drop off here".
- Responsive and platform work: "make it work on mobile", "port this to iOS".

## The expert

Pick the one whose failures this request would cause, and adapt the description to the exact case. It goes on the `Expert:` line of the output block; the rewritten task itself carries the moves, never a persona line (`method/expert.md`).

- **Senior product designer, 10 years, B2B SaaS with daily power users.** Fits dashboards, settings, tables, admin tools, anything used for hours a day.
- **Interaction designer, 8 years, government digital services (GOV.UK style).** Fits forms, multi step flows, error handling, anything a first time user must finish without help.
- **Accessibility specialist, 12 years, WCAG audits and assistive technology testing.** Fits "make it accessible", any public facing page, any custom widget (menus, dialogs, comboboxes, tabs).
- **Design systems lead, 9 years, component libraries used by many product teams.** Fits tokens, component APIs, theming, dark mode, "make it consistent".
- **UX researcher, 11 years, usability testing and task analysis.** Fits "why do users drop off", critiques, onboarding, and any redesign of something already live.

## Moves the expert makes unasked

1. **Names the primary user, their main task, and how often they do it, before drawing anything.**
   Why: a screen used once a year and one used fifty times a day need opposite trade offs.
   Check: the brief states user, task, frequency and context (device, hurry, expertise) in two or three lines.

2. **Designs every state, not just the full one: empty, loading, partial, error, offline, no permission, too much data.**
   Why: a new account starts empty and real networks fail, so these states are often the first thing a user sees.
   Check: there is a list of states for each view and each one is rendered or specified.

3. **Uses real content at its real length, including the longest name, a long translation, and a zero.**
   Why: lorem ipsum hides overflow, wrapping and truncation problems.
   Check: the mock or code is filled with realistic worst case strings and numbers, and nothing clips or overlaps.

4. **Checks the layout at 320 CSS pixels wide and at 400 percent zoom with no sideways scroll.**
   Why: WCAG 1.4.10 Reflow requires it, and phone layouts wider than the screen are a common shipped defect.
   Check: at 320px viewport width, `document.documentElement.scrollWidth <= innerWidth` and nothing is cut off.

5. **Gives every pointer target at least 24 by 24 CSS px (WCAG 2.5.8), and 44pt or 48dp on touch platforms.**
   Why: small targets cause misses for everyone and block people with motor impairments.
   Check: measure each icon button's hit area in code, not its glyph size.

6. **Meets contrast: 4.5:1 for body text, 3:1 for large text and for UI parts like borders, focus rings and icons.**
   Why: low contrast text and invisible input borders fail on real screens in daylight.
   Check: compute the ratio for each text and control colour against the colour actually behind it, in both light and dark themes.

7. **Makes everything work by keyboard, with a visible focus indicator and a logical order.**
   Why: keyboard users, screen reader users and power users all depend on it, and custom widgets break it silently.
   Check: tab through the whole flow; every control is reachable, operable, shows focus, and Escape closes overlays.

8. **Uses native elements first, and the WAI-ARIA Authoring Practices pattern when a custom widget is truly needed.**
   Why: a div with a click handler has no role, no keyboard support and no name.
   Check: every interactive element is a button, link or form control, or follows an APG pattern with its documented keys.

9. **Writes error messages that say what went wrong and how to fix it, next to the field, plus a summary.**
   Why: "Invalid input" in red leaves the user stuck; colour alone fails colour blind users.
   Check: each validation rule has its own specific message; errors are announced and not shown by colour alone.

10. **Never makes the user remember or retype: preserves input on error, offers sensible defaults, and allows undo for destructive actions.**
    Why: lost form data and irreversible deletes cost users work they cannot get back, and they abandon or write to support.
    Check: submit a form with one error and confirm every other field keeps its value; delete has undo or a clear confirmation.

11. **Uses labels in the user's words and keeps them consistent across the product.**
    Why: match between system and real world, and consistency, are two of the ten core usability heuristics.
    Check: no internal jargon in UI text; the same action has the same name everywhere.

12. **Builds from existing tokens and components instead of new one-off values.**
    Why: one-off colours, sizes and spacings are what make a product look inconsistent and cheap.
    Check: grep the change for literal colours, font sizes and spacings that are not tokens.

13. **Respects user settings: reduced motion, text scaling, dark mode, high contrast.**
    Why: animation can cause nausea, and text that ignores user scaling is unreadable for low vision users.
    Check: with `prefers-reduced-motion` on, large motion is removed; at 200 percent text size nothing clips.

14. **Tests with five representative users on real tasks, or at least a structured heuristic review, before calling it done.**
    Why: Nielsen's model puts five users at about 85 percent of the problems one user group meets (an average; single samples of five vary widely), and the designer is never a representative user.
    Check: a short findings list exists with the task, what the user did, and the severity of each problem.

## Raw material

What the expert starts from, and where to get it:

- **The real users and their tasks.** Support tickets, sales call notes, analytics funnels, session recordings, interviews. If none exist, a written assumption that is flagged as an assumption.
- **The real content.** Actual product names, user names, numbers, error texts, translations, from the database or the content owner. The longest and the shortest real values.
- **The existing product.** Current screens, the current component library and tokens, the code that renders them. Read the design system source, not a screenshot of it.
- **Platform guidelines for the target.** Apple Human Interface Guidelines, Material Design, the web platform (HTML elements and their built in behaviour).
- **Standards text.** WCAG 2.2 success criteria and their Understanding documents, the WAI-ARIA Authoring Practices patterns.
- **Research on the pattern.** Nielsen Norman Group articles, Baymard Institute for e-commerce and checkout, GOV.UK Design System for forms and errors (each pattern there is backed by testing with real users).

What to distrust:

- Dribbble and Behance shots: they show one ideal state with fake content, never the error or the empty state.
- Your own taste and your team's opinions as proof that a flow is usable.
- Competitor screens as evidence: you see the result, not whether it worked for them.
- Accessibility overlays and automated scores alone: automated tools catch only part of WCAG failures.
- Stakeholder statements about what users want, without user evidence.
- Screenshots at one size on one device.

## Methods and tools

- **Task analysis and user journey mapping.** At the start of any flow; lists the steps the user takes and where they decide or wait.
- **Content first design (write real copy before layout).** For any new screen.
- **State inventory (each view times empty, loading, partial, error, success, permission).** For every new view or component.
- **Heuristic evaluation with Nielsen's ten heuristics.** For critiques and before user testing; rate each issue by severity.
- **Usability testing, think aloud, five users per round.** For flows and redesigns; repeat after fixes.
- **WCAG 2.2 AA checklist with the Understanding documents.** For any public or work product.
- **WAI-ARIA Authoring Practices Guide patterns.** When building a custom dialog, menu, tabs, combobox, listbox or tree.
- **axe-core or Lighthouse accessibility checks.** On every page, in CI if possible, as a floor, not a pass.
- **Screen reader pass (VoiceOver, NVDA, TalkBack).** For any custom widget or flow change.
- **Contrast calculation from the WCAG formula.** For every text and UI colour pair, both themes.
- **Design tokens (colour, type scale, spacing, radius, motion).** For any design system or consistency work.
- **Responsive checks at 320, 375, 768, 1024, 1440 px and at 200 and 400 percent zoom.** For every layout.
- **HEART metrics (happiness, engagement, adoption, retention, task success).** To decide how a redesign will be judged after launch.

## Independent proof

What shows the result is right, other than the designer saying so:

- **Users completing the task.** Five representative users try the main tasks without help; record completion, time, errors. An agent cannot run real users, so it writes the test script (tasks, success criteria, questions) and flags the test as not done.
- **Computed measurements from the code.** An agent can read the code and compute: text width (font size times character count times roughly 0.5 to 0.6 for common proportional UI fonts; measure when the margin is thin) against the box width, contrast ratios from the hex values, hit area sizes, the widest element at 320px. Write the numbers down.
- **Automated accessibility checks.** Run axe-core (for example with `@axe-core/cli` or the project's test runner) against the built page; zero violations is the floor.
- **Scripted keyboard pass.** An E2E test that tabs through the flow, asserts focus order, and checks that each control responds to Enter or Space and that Escape closes dialogs.
- **Layout assertions.** An E2E test at 320px width asserting no element is wider than the viewport and no text overflows its container.
- **Heuristic review by a second reviewer.** A fresh agent given the screens and the ten heuristics, not the designer's rationale, lists issues by severity. It finds problems; it is not proof that users can finish the task.
- **Post launch metrics chosen before launch.** Task success rate, drop off at each step, support tickets on the flow.

When proof needs eyes on a real screen and none is available, say so plainly and list exactly what a person should check.

## Amateur mistakes

1. Designing only the happy state with perfect content; the empty, error and long text states are left to the developer.
2. Layouts that are wider than a phone screen, causing sideways scroll.
3. Icon buttons with a 16px hit area and no accessible name.
4. Grey placeholder text used as the label, which disappears on typing and fails contrast.
5. Error shown only by turning the border red, with no text and no announcement.
6. A custom dropdown built from divs with no keyboard support.
7. Removing the focus outline because it "looks ugly", with nothing in its place.
8. New one-off colours and spacings in every screen instead of tokens.
9. Truncating important data (names, amounts) with an ellipsis and no way to see the full value.
10. Animations that cannot be turned off and ignore reduced motion.
11. Confirm dialogs on every action, which trains users to click "OK" without reading, while the truly destructive action has no undo.
12. Text set in light grey on white or white on a bright brand colour.

## Scope traps

How "deeper" turns into "bigger" here:

- "Polish this page" becomes a full rebrand with new fonts, colours and illustrations.
- "Fix this form" becomes a redesign of the whole onboarding.
- "Make it accessible" becomes a rebuild of every component in the library.
- A screen request grows a new design system.
- One flow grows dark mode, theming, animations and an illustration set nobody asked for.
- A critique turns into producing three alternative full designs.

Deeper means the same screen, now with every state, real content, accessibility and a way to prove users can finish the task.

Typical "not doing" items:

- No new brand colours, fonts or logo.
- No changes to screens outside the flow.
- No new components when an existing one fits.
- No illustrations or animation beyond what the task needs.
- No dark mode or theming work unless the product already has it (then it must work in both).
- No user research recruiting; the test script is written, the sessions are flagged as not run.

## Worked example

Vague request: "Make a signup page for my app."

1. **Expert:** interaction designer, 8 years, government digital services forms.
2. **Unasked moves (top 5):** labels always visible, never placeholders; a specific inline error for each backend rule plus a summary, with input kept; password rules shown up front with "show password"; the states submitting, email taken, network error and success; a 320px layout that passes a keyboard only run.
3. **Raw material:** the backend's real validation rules and error codes, the existing component library and tokens, GOV.UK patterns for email, passwords and validation, WCAG 2.2 criteria 1.4.3, 1.4.10, 2.4.7, 2.5.8, 3.3.1.
4. **Methods:** content first copy, state inventory, heuristic review, APG pattern only if a custom control is needed, axe check.
5. **Independent proof:** an E2E test at 320px asserting no horizontal overflow; a keyboard test through the form; axe with zero violations; computed contrast for every text colour; a five task usability script flagged as not run.
6. **Rewritten task:**

```
Build the signup page with existing components and tokens.
Fields: email, password (rules visible, show toggle). Labels always visible.
Every backend error gets a specific inline message plus a top summary; inputs keep their values.
States: idle, submitting, email taken, network error, success.
Proof: E2E at 320px (no overflow), keyboard-only completion, axe zero violations, contrast numbers listed.
Not doing: social login, new brand styles, onboarding after signup, running user sessions (script only).
```

## Sources

- Nielsen Norman Group, 10 Usability Heuristics for User Interface Design: https://www.nngroup.com/articles/ten-usability-heuristics/
- Nielsen Norman Group, Why You Only Need to Test with 5 Users: https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/
- Nielsen Norman Group, Thinking Aloud, the number 1 usability tool: https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/
- Nielsen Norman Group, Usability Testing 101: https://www.nngroup.com/articles/usability-testing-101/
- Nielsen Norman Group, Designing Empty States in Complex Applications: https://www.nngroup.com/articles/empty-state-interface-design/
- W3C, Web Content Accessibility Guidelines (WCAG) 2.2: https://www.w3.org/TR/WCAG22/
- W3C, Understanding SC 1.4.10 Reflow (320 CSS px, no two dimensional scroll): https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- W3C, Understanding SC 1.4.3 Contrast (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- W3C, Understanding SC 2.5.8 Target Size (Minimum), 24 by 24 CSS px: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- W3C, WAI-ARIA Authoring Practices Guide: https://www.w3.org/WAI/ARIA/apg/
- GOV.UK Design System, Error message component: https://design-system.service.gov.uk/components/error-message/
- GOV.UK Design System, Validation pattern: https://design-system.service.gov.uk/patterns/validation/
- GOV.UK Service Manual, Start by learning user needs: https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs
- Apple Human Interface Guidelines, Accessibility (44 by 44 pt targets): https://developer.apple.com/design/human-interface-guidelines/accessibility
- Android Developers, Make apps more accessible (48 dp touch targets): https://developer.android.com/guide/topics/ui/accessibility/apps
- Baymard Institute, Checkout usability research: https://baymard.com/research/checkout-usability
- Heydon Pickering, Inclusive Components: https://inclusive-components.design/
- Microsoft Inclusive Design toolkit: https://inclusive.microsoft.design/
- Deque, axe-core: https://github.com/dequelabs/axe-core
- Rodden, Hutchinson, Fu, Measuring the User Experience on a Large Scale (HEART), CHI 2010: https://research.google/pubs/pub36299/
- Steve Krug, Don't Make Me Think and Rocket Surgery Made Easy: https://sensible.com/
