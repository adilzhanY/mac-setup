# Accessibility testing

The cross platform master for accessibility (a11y) testing. It says what WCAG 2.2 level AA asks that a tester can actually check, which checks automation misses, how an agent tests accessibility by reading code and running tools when it may not look at the screen, short screen reader scripts for the owner, and where the platform specific detail lives. Platform files in this skill go deeper: `web/accessibility-testing.md` (axe, Playwright, keyboard, ARIA) and `mobile/mobile-accessibility-testing.md` (TalkBack, VoiceOver, Android and iOS scanners). kwx-designer owns accessible design; this file owns proving it.

## Contents

1. The rules that matter most
2. What automation finds and what it misses
3. WCAG 2.2 AA: what a tester checks
4. The manual checks automation misses
5. How an agent tests accessibility without a screen
6. Screen reader test scripts (for the owner)
7. Desktop apps (Qt/QML, GTK) and terminals
8. Reporting accessibility bugs
9. Checks

## 1. The rules that matter most

| # | Rule | Why | Evidence |
|---|---|---|---|
| A1 | Target WCAG 2.2 level AA unless the owner names another bar. | It is the legal and public sector baseline (GOV.UK requires 2.2 AA; the EU accessibility rules point at the same criteria). | strong (W3C Recommendation, 12 December 2024 edition) |
| A2 | Run automated checks, then do the manual checks. Never report "accessible" from a tool alone. | GDS planted 142 barriers: the best of 13 tools found 40 percent (2018). Deque reports 57 percent of issues by volume with axe (2021, vendor data). Either way, most criteria need a person. | strong (GDS audit), moderate (Deque) |
| A3 | Every interactive element must be reachable and usable by keyboard (or switch, or screen reader gestures), with a visible focus. | Keyboard access is the base that screen readers, switch access and voice control build on (2.1.1, 2.4.7). | strong (WCAG) |
| A4 | Every control has an accessible name that contains its visible label, a correct role and its state. | Without it a screen reader says "button" or nothing (4.1.2, 2.5.3). | strong (WCAG) |
| A5 | Check contrast in every state: default, hover, focus, pressed, disabled, error, dark mode, over images. | Tools test the default state only. | strong (WCAG 1.4.3, 1.4.11) |
| A6 | Check zoom and text size: 200 percent text, 400 percent page zoom (320 CSS px wide), and the largest system font on mobile. | Clipped and overlapping text is the most common failure after contrast. | strong (1.4.4, 1.4.10) |
| A7 | Touch and click targets at least 24 by 24 CSS px (WCAG 2.5.8 AA); 48 by 48 dp on Android and 44 by 44 pt on iOS by platform guidelines. | Small targets fail people with tremor and everyone on a bus. | strong (WCAG, platform docs) |
| A8 | Read the code for names, roles, focus order and live regions; that part an agent can do fully. | Most a11y defects are visible in the source. | moderate |
| A9 | Hand screen reader and visual checks to the owner as a short script if the user's rules forbid the agent to drive a browser, emulator or desktop. | Some things can only be confirmed by listening or looking. | house rule |
| A10 | Report each defect with the WCAG criterion number, the element, who is affected and the fix. | It turns "a11y is bad" into a fixable list. | moderate |

## 2. What automation finds and what it misses

Automated tools (axe-core, Lighthouse, WAVE, Android Accessibility Scanner and lint, Xcode Accessibility Inspector, eslint-plugin-jsx-a11y) reliably find:

- missing alt text, missing form labels, empty buttons and links,
- contrast of plain text on solid backgrounds in the rendered state,
- invalid ARIA (wrong roles, missing required attributes, `aria-hidden` on focusable elements),
- missing page language, duplicate ids, missing document title,
- some heading order problems.

They cannot judge:

- whether alt text or a label is **meaningful** ("image", "button 3", a file name),
- whether the **keyboard path** works and is in a logical order, and whether focus is trapped or lost,
- whether **focus is visible** and not hidden behind a sticky header (2.4.11),
- **reading order** versus visual order,
- whether **dynamic changes are announced** (toasts, errors, loading),
- **contrast in other states** and text over images or gradients,
- **zoom, reflow and text spacing** behaviour,
- **motion**, flashing, auto playing content,
- whether the **meaning survives without colour**,
- **cognitive** issues: unclear errors, time limits, puzzles in sign in (3.3.8).

GDS's result (13 tools, 142 planted barriers, best tool 40 percent, worst 13 percent) is the reason for rule A2.

## 3. WCAG 2.2 AA: what a tester checks

The criteria a tester can check in an exploratory session, grouped by what you do. Numbers are WCAG 2.2 success criteria; all are level A or AA.

| Check | Criteria | Pass condition |
|---|---|---|
| Text alternatives | 1.1.1 | Every informative image, icon button and chart has a text alternative with the same purpose; decorative images are hidden from assistive tech |
| Structure | 1.3.1, 2.4.6, 2.4.2 | Headings, lists, tables and form groups are real structure (not just bold text); headings and labels describe their content; each page or screen has a descriptive title |
| Reading order | 1.3.2, 2.4.3 | The order a screen reader or Tab follows makes sense and matches the visual order |
| Orientation | 1.3.4 | Works in portrait and landscape unless one is essential |
| Input purpose | 1.3.5 | Personal data fields declare their purpose (`autocomplete="email"`, `textContentType`, `autofillHints`) |
| Use of colour | 1.4.1 | Colour is never the only way to show information (error fields also have text or an icon) |
| Text contrast | 1.4.3 | 4.5:1 for normal text, 3:1 for large text (at least 24 px, or 18.66 px bold) |
| Resize text | 1.4.4 | Text resizes to 200 percent with no loss of content or function |
| Reflow | 1.4.10 | At 320 CSS px wide (400 percent zoom on a 1280 px window) no horizontal scrolling for text content |
| Non text contrast | 1.4.11 | Control borders, focus rings, icons that carry meaning, chart lines: 3:1 against neighbours |
| Text spacing | 1.4.12 | Nothing breaks with line height 1.5, paragraph spacing 2, letter spacing 0.12, word spacing 0.16 times the font size |
| Hover and focus content | 1.4.13 | Tooltips and popovers can be dismissed (Esc), hovered, and stay until dismissed |
| Keyboard | 2.1.1, 2.1.2, 2.1.4 | Everything works by keyboard; focus can always leave a component; single key shortcuts can be turned off or remapped |
| Time limits | 2.2.1 | The user can extend or turn off time limits (session timeout warnings) |
| Moving content | 2.2.2 | Anything that moves, blinks or auto updates for more than 5 seconds can be paused, stopped or hidden |
| Flashing | 2.3.1 | Nothing flashes more than three times per second |
| Bypass blocks | 2.4.1 | A skip link or landmarks let keyboard users skip repeated navigation (web) |
| Link purpose | 2.4.4 | Link text makes sense in context ("Read more" alone fails if there are ten of them) |
| Focus visible | 2.4.7 | Keyboard focus is always visible |
| Focus not obscured | 2.4.11 (new in 2.2) | A focused element is not entirely hidden by sticky headers, footers, cookie banners or chat widgets |
| Pointer gestures | 2.5.1 | Multi point or path gestures (pinch, swipe patterns) have a single pointer alternative |
| Pointer cancellation | 2.5.2 | Actions fire on release (up event), so a slip can be cancelled by moving away |
| Label in name | 2.5.3 | The accessible name contains the visible label text (voice control users say what they see) |
| Motion actuation | 2.5.4 | Shake or tilt features have a button alternative and can be turned off |
| Dragging movements | 2.5.7 (new in 2.2) | Anything done by dragging can also be done with single clicks or taps (reorder buttons, a menu) |
| Target size | 2.5.8 (new in 2.2) | Targets at least 24 by 24 CSS px, or spaced so a 24 px circle around each does not overlap another |
| Language | 3.1.1, 3.1.2 | The page or app declares its language; passages in another language are marked (`lang="kk"`) so screen readers switch voice |
| Predictable | 3.2.1, 3.2.2, 3.2.3, 3.2.4 | Focus or input does not trigger surprise context changes; navigation and naming are consistent |
| Consistent help | 3.2.6 (new in 2.2) | Help links or contact details appear in the same relative place on each page |
| Errors | 3.3.1, 3.3.3 | Errors are identified in text and suggest a fix |
| Labels and instructions | 3.3.2 | Inputs have labels or instructions before they are needed |
| Error prevention | 3.3.4 | Legal, financial and data deleting actions are reversible, checked or confirmed |
| Redundant entry | 3.3.7 (new in 2.2) | Information entered earlier in a flow is filled in or selectable, not asked again |
| Accessible authentication | 3.3.8 (new in 2.2) | Sign in does not require a cognitive test (remembering, transcribing, puzzles) unless there is an alternative; allow paste and password managers |
| Name, role, value | 4.1.2 | Custom controls expose name, role, state and value to assistive tech |
| Status messages | 4.1.3 | Status changes (saved, 3 results, error) are announced without moving focus (`role="status"`, `aria-live`, `accessibilityLiveRegion`, `announceForAccessibility`) |

4.1.1 Parsing was removed in WCAG 2.2. Mobile apps are judged against the same criteria as interpreted by the W3C's guidance on applying WCAG to mobile.

## 4. The manual checks automation misses

Run these on every UI change. The agent does the code half; the owner does the screen half if the agent may not look.

1. **Keyboard path.** Unplug the mouse (web, desktop) or connect a keyboard (Android emulator with a hardware keyboard, or a Bluetooth keyboard). Tab and Shift+Tab through the whole screen. Every control reachable, order logical, Enter and Space activate, Esc closes dialogs, arrow keys work inside menus, tabs and lists. Focus never gets lost (jumps to the top after a dialog closes) or trapped.
2. **Focus visible.** On every focused element there is a clearly visible indicator with at least 3:1 contrast against the background, and it is not hidden by a sticky bar.
3. **Meaningful names.** With a screen reader or the accessibility tree, every control's name says what it does: "Delete habit Morning run", not "button" or "icon". Icon only buttons are the usual offenders.
4. **Reading order.** Swipe through with a screen reader: content is read in the visual order; nothing important is skipped; decorative things are skipped.
5. **Announcements.** Trigger a save, an error, a loading state, a toast: each is spoken once, without stealing focus.
6. **Contrast in all states.** Default, hover, focus, pressed, selected, disabled (disabled text is exempt from 1.4.3 but must still be recognisable), error, placeholder text, dark mode, text on images and gradients.
7. **Zoom and reflow.** Web: browser zoom to 400 percent at 1280 px wide (or a 320 px wide window) and text only zoom 200 percent. Android: Settings font size largest plus display size largest. iOS: Larger Accessibility Sizes. Nothing clipped, overlapping or cut with an ellipsis that hides meaning.
8. **Text spacing.** Apply the 1.4.12 values with a bookmarklet or a stylesheet override; nothing overlaps.
9. **Motion.** With "reduce motion" on (OS setting, `prefers-reduced-motion`), large animations stop or shrink; no parallax or auto play carousel without pause.
10. **Target size.** Small icons, close buttons and links inside text: at least 24 by 24 CSS px on the web, 48 dp on Android.
11. **Colour alone.** View in greyscale: errors, statuses and chart series are still distinguishable.
12. **Forms and errors.** Submit empty and wrong values: each error is in text, next to the field, announced, and the typed data stays.

## 5. How an agent tests accessibility without a screen

Check the user's rules first. If the agent may not open a browser, drive an emulator or take screenshots, it can still do a lot:

In the table, `\|` inside a command is Markdown escaping for the table: type a plain `|` when you run it.

| Method | What it catches | Command or example |
|---|---|---|
| Lint the source | Missing alt, labels, roles, click handlers on non buttons | The project's `npx eslint .` with `eslint-plugin-jsx-a11y` (web) or `eslint-plugin-react-native-a11y` enabled; if neither is configured, propose adding it rather than running an ad hoc config. Android: `./gradlew lint` (checks ContentDescription, ClickableViewAccessibility, KeyboardInaccessibleWidget) |
| Unit and component tests with a11y queries | Names and roles exist | Testing Library `getByRole('button', { name: /delete habit/i })` fails when the name is missing; Compose `onNodeWithContentDescription`; `jest-axe` / `vitest-axe` in component tests |
| axe in CI | Rendered page rules | Write the Playwright plus `@axe-core/playwright` test into the project; running it locally needs the owner's yes when browsers are off for the agent, CI may run it (see `web/accessibility-testing.md`) |
| Read the code for each manual check | Focus order (`tabIndex` > 0 is a smell), focus traps in modals, `outline: none` without a replacement, live regions, `accessibilityLabel` on icon buttons, `importantForAccessibility`, `aria-hidden` on focusable things | `rg -n 'outline:\s*(none\|0)' src`; `rg -n 'tabIndex=\{?[1-9]' src`; `rg -n '<(Pressable\|TouchableOpacity)' src` then check each has `accessibilityRole` and `accessibilityLabel` when it has no text |
| Compute contrast from the design tokens | Every token pair used for text and controls | The script below over the theme file |
| Compute target sizes from the code | Hit areas below 24 px or 48 dp | Read `width`, `height`, `padding`, `hitSlop`, `minimumInteractiveComponentSize`; flag icon buttons under the minimum |
| Predict zoom and font scaling problems | Fixed heights on text containers, `numberOfLines={1}` without a fallback, `allowFontScaling={false}`, px font sizes | `rg -n 'allowFontScaling=\{false\}\|maxFontSizeMultiplier' src`; fixed `height:` on views that contain text |
| Check motion handling | Animations ignore reduce motion | `rg -n 'prefers-reduced-motion\|useReducedMotion\|AccessibilityInfo.isReduceMotionEnabled\|ANIMATOR_DURATION_SCALE' src` |

Contrast ratio from two hex colours (**verified**: `#767676` on white gives 4.54:1, `#959595` gives 2.99:1; WCAG says never round up):

```js
// contrast.mjs: node contrast.mjs "#767676" "#ffffff"   (WCAG 2.2 relative luminance, never round up)
const lum = (hex) => {
  const [r, g, b] = hex.replace("#", "").match(/../g).map((h) => parseInt(h, 16) / 255)
    .map((c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const [a, b] = process.argv.slice(2).map(lum).sort((x, y) => y - x);
const ratio = (a + 0.05) / (b + 0.05);
console.log((Math.floor(ratio * 100) / 100).toFixed(2) + ":1", ratio >= 4.5 ? "AA text" : ratio >= 3 ? "AA large text and UI only" : "FAIL");
```

Run it over every text and background token pair, in light and dark themes, including disabled and placeholder colours, and colours with alpha (blend them onto the background first).

Everything that needs hearing a screen reader, seeing focus, or feeling a target goes on the owner's checklist ([human-check-handoff.md](human-check-handoff.md)), most risky first.

## 6. Screen reader test scripts (for the owner)

Short scripts the owner can run in a few minutes. Hand over only the one for the platform under test, with the screen and the 3 to 5 things to listen for.

**TalkBack (Android).** Turn on: Settings, Accessibility, TalkBack (or hold both volume keys for 3 seconds if the shortcut is set). Swipe right to move to the next item, left for previous, double tap to activate, two finger swipe to scroll. Listen for: every control says a name and a role ("Add habit, button"); icons are not silent or "unlabelled"; the order follows the screen top to bottom; toasts and errors are spoken.

**VoiceOver (iOS).** Settings, Accessibility, VoiceOver, or triple click the side button if the shortcut is set. Swipe right and left to move, double tap to activate, rotor (two finger rotate) to jump by headings. Same things to listen for.

**VoiceOver (macOS).** Cmd+F5. VO keys are Ctrl+Option; VO+Right Arrow moves, VO+Space activates, VO+U opens the rotor (headings, links, form controls).

**NVDA (Windows, free).** Ctrl+Alt+N starts it. Down Arrow reads the next item, Tab moves between controls, H jumps by heading, Insert+F7 lists links and headings. Insert+Q quits.

**Orca (Linux).** Super+Alt+S in GNOME, or run `orca`. Tab and arrow keys move; Orca reads the focused control. Qt apps need `QT_ACCESSIBILITY=1` and the AT-SPI bridge; under Hyprland expect gaps, so treat Orca results on Linux as best effort.

GOV.UK's recommended minimum combinations for a public website (updated 2020): JAWS with Chrome or Edge, NVDA with Chrome, Firefox or Edge, VoiceOver iOS with Safari, TalkBack with Chrome, Windows Magnifier or Apple Zoom, Dragon with Chrome. For a solo developer's app, one screen reader per shipped platform is the realistic minimum.

## 7. Desktop apps (Qt/QML, GTK) and terminals

- **QML**: every interactive item needs `Accessible.role`, `Accessible.name` (and `Accessible.description` when useful); custom `MouseArea` buttons have none by default. `rg -n 'MouseArea' modules | head` then check each has an accessible sibling or parent with a role. Keyboard: `activeFocusOnTab: true`, `Keys.onReturnPressed`, a visible focus state bound to `activeFocus`.
- **Scaling**: text and boxes must grow together when the UI scale or system font changes; text in fixed size boxes is the usual defect. Compute from code: font pixel size times text length against the box width at the current scale.
- **GTK**: use real widgets; check with Accerciser (`accerciser`) if the owner can run it.
- **TUIs and CLIs**: colour is never the only signal (add symbols or words); respect `NO_COLOR`; output stays readable at 80 columns; no flashing; screen readers read terminals line by line, so avoid redrawing the whole screen for small updates.

## 8. Reporting accessibility bugs

Use the normal bug format ([bug-reports.md](bug-reports.md)) with three extra fields:

```markdown
- [ ] **B4. "Delete" icon button has no accessible name** `a11y:habits/list`
      WCAG 4.1.2 Name, Role, Value (A). Who: screen reader and voice control users.
      `src/screens/HabitList.tsx:88` `<Pressable onPress={remove}><TrashIcon/></Pressable>` has no accessibilityLabel or role.
      Expected: TalkBack says "Delete habit Morning run, button". Fix: add accessibilityRole="button" and accessibilityLabel={`Delete habit ${habit.name}`}.
```

Severity guide: anything that blocks a task for a group of users (no keyboard access to checkout, unlabelled submit button, focus trap) is **major** or higher; contrast and target size issues on primary actions are **major**; on secondary text, **minor**.

## 9. Checks

- [ ] Automated checks that exist in the project ran (lint with a11y rules, component a11y queries, axe in CI), and their output was read.
- [ ] Every interactive element touched by the change has a role, a name containing its visible label, and its state (from code).
- [ ] Contrast was computed for every text and control token pair used, in light and dark, including disabled, placeholder, focus and error states.
- [ ] Target sizes of new controls were computed from code: at least 24 by 24 CSS px (web) or 48 dp (Android), 44 pt (iOS).
- [ ] Keyboard and focus order were checked in code (no positive tabIndex, focus returned after dialogs, no outline removed without replacement), and the keyboard walk is on the owner's checklist if the agent cannot run it.
- [ ] Status messages and errors use live regions or announcements (code checked).
- [ ] Font scaling and zoom risks were listed (fixed heights, `allowFontScaling={false}`, nowrap labels).
- [ ] Reduce motion is respected by new animations.
- [ ] Screen reader and visual checks went to the owner as one short script for the platform under test.
- [ ] Each a11y bug names its WCAG criterion, the element (file and line), who is affected and the fix.
- [ ] The report does not claim "accessible" or "WCAG compliant"; it lists what was checked and what was not.
