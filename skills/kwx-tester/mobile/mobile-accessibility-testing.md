# Mobile accessibility testing

How to test that a mobile app works for people who use a screen reader, large text, switch access or reduced motion: automated checks inside the tests you already write (RNTL, Compose, Espresso, XCUITest), the Android Accessibility Scanner and the Play pre-launch report, touch target and font scaling checks, and short manual scripts for TalkBack and VoiceOver that you hand to the user. Automated checks find missing labels, small targets and low contrast; only a person with a screen reader finds a confusing reading order or an unusable flow, so both are needed. Web accessibility (WCAG in browsers) is covered elsewhere in the skill; this file is mobile only.

## Contents

1. What to check, and which part a machine can check
2. React Native: props to set and assert
3. Compose and Espresso automated checks
4. iOS automated checks
5. Accessibility Scanner and the pre-launch report
6. Touch targets
7. Font scaling, display size, contrast, motion
8. TalkBack test script
9. VoiceOver test script
10. Checks

## 1. What to check, and which part a machine can check

| Property | Machine check | Person check |
|---|---|---|
| Every control has a name | RNTL `toHaveAccessibleName`, `getByRole(..., { name })`; Compose and Espresso checks; `performAccessibilityAudit` | Is the name meaningful ("Delete note Shopping", not "Button 3")? |
| Correct role and state | RNTL `getByRole`, `toBeChecked`, `toBeDisabled`, `toBeExpanded`; Compose `assertIsOn`, `assertIsSelected` | Does TalkBack say "switch, on"? |
| Touch target at least 48 dp / 44 pt | Compose and Espresso checks, Accessibility Scanner, pre-launch report | Can you hit it with a thumb? |
| Contrast 4.5:1 for text, 3:1 for large text and UI parts | Accessibility Scanner, Compose checks, iOS audit | In sunlight, in dark mode |
| Reading and focus order | Compose traversal check (partial) | Swipe through the screen: does the order make sense? |
| Text scales to 200% without clipping | Screenshot tests at font scale 2.0 | Real device at maximum size |
| Errors and changes are announced | Assert `aria-live` / live region props are set | Does TalkBack read the error after Save? |
| Gestures have alternatives | Assert `accessibilityActions` exist for swipe actions | Can you delete without swiping? |
| Motion can be reduced | Unit test the reduced motion branch | Animations off when the system setting is on |

Evidence: moderate (Android accessibility testing guide; Apple Human Interface Guidelines; WCAG 2.2 contrast and target size criteria).

## 2. React Native: props to set and assert

Since React Native 0.71 the ARIA style props are preferred (RNTL's guidance for v14 says the same):

| Need | Prop | Assert in RNTL |
|---|---|---|
| Name | `aria-label="Delete note"` (or `accessibilityLabel`) | `getByRole('button', { name: 'Delete note' })`, `toHaveAccessibleName('Delete note')` |
| Name from visible text elsewhere | `aria-labelledby="titleId"` with `nativeID="titleId"` on the label | `getByLabelText('Email')` |
| Role | `role="button"`, `"switch"`, `"checkbox"`, `"header"`, `"link"`, `"tab"`, `"slider"`, `"alert"` (or `accessibilityRole`) | `getByRole('switch', { name: 'Dark mode' })` |
| Hint | `accessibilityHint="Opens the note editor"` | Read the prop; keep hints short and optional |
| State | `aria-disabled`, `aria-checked` (true, false, `"mixed"`), `aria-selected`, `aria-expanded`, `aria-busy` | `toBeDisabled`, `toBeChecked`, `toBePartiallyChecked`, `toBeSelected`, `toBeExpanded`, `toBeCollapsed`, `toBeBusy` |
| Value | `aria-valuemin`, `aria-valuemax`, `aria-valuenow`, `aria-valuetext` | `toHaveAccessibilityValue({ now: 3, min: 0, max: 5 })` |
| Announce changes | `aria-live="polite"` (Android live region); `AccessibilityInfo.announceForAccessibility(msg)` for one off messages | Assert the prop on the error container; mock `AccessibilityInfo` and assert the message |
| Hide decoration | `aria-hidden` / `importantForAccessibility="no-hide-descendants"` on decorative views; `accessible={false}` on icons inside a labelled button | `queryByRole('image')` returns null for decorative icons |
| Group | `accessible` on a row container with a combined label, so the row is read once | `getByRole('button', { name: 'Shopping, 3 items, edited today' })` |
| Modal | `aria-modal` / `accessibilityViewIsModal` (iOS) on custom dialogs | Prop assertion |
| Gesture alternative | `accessibilityActions={[{ name: 'delete', label: 'Delete' }]}` with `onAccessibilityAction` | `await user.accessibilityAction(row, 'delete')` (RNTL 14.1), then assert the row is gone |

Test pattern: write the screen test with role and name queries from the start. If `getByRole` cannot find a control, the control is not exposed to assistive technology: fix the component (often a `Pressable` wrapped in a `View` with `accessible`, or an icon button with no label). Never switch the query to `getByTestId` to make it pass.

Verified (RNTL 14.1.0, 2026-10-31), with each row a `Pressable` with `role="button"`, an `aria-label` of "<title>, note", `accessibilityActions={[{ name: 'delete', label: 'Delete' }]}` and an `onAccessibilityAction` handler, and a `<View role="switch" accessible aria-checked={false} aria-label="Dark mode" />`:

```tsx
test('each note row can be deleted without a swipe', async () => {
  const user = userEvent.setup();
  await render(<NotesList notes={[{ id: '1', title: 'Shopping' }]} />);
  const row = screen.getByRole('button', { name: /Shopping/ });
  expect(row).toHaveAccessibleName('Shopping, note');
  await user.accessibilityAction(row, 'delete');
  expect(screen.queryByRole('button', { name: /Shopping/ })).not.toBeOnTheScreen();
  expect(screen.getByRole('switch', { name: 'Dark mode' })).not.toBeChecked();
});
```

Lint: `eslint-plugin-react-native-a11y` flags missing labels and invalid roles in RN code (check the plugin's support for ARIA props in your RN version).

## 3. Compose and Espresso automated checks

Compose (1.8+):

```kotlin
// androidTestImplementation("androidx.compose.ui:ui-test-junit4-accessibility")
class NotesA11yTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test
    fun notesScreen_passesAccessibilityChecks() {
        rule.enableAccessibilityChecks()
        rule.setContent { AppTheme { NotesScreen(uiState = sampleState, onAdd = {}) } }
        rule.onRoot().tryPerformAccessibilityChecks()
        rule.onNodeWithContentDescription("Add note").performClick()   // checks run on every action too
    }
}
```

Per the API reference it needs API 34+ and does not run on Robolectric, so it lives in `androidTest` and needs a device (tier 3 under the user's rules; CI or Firebase Test Lab otherwise). It checks touch target size, contrast, missing labels, duplicate descriptions and traversal order using Google's Accessibility Test Framework.

On the JVM you can still assert semantics: `onNodeWithContentDescription("Add note").assertHasClickAction()`, `assert(SemanticsMatcher.expectValue(SemanticsProperties.Role, Role.Switch))`, and check `Modifier.minimumInteractiveComponentSize()` is not removed. Compose Preview "UI Check" mode in Android Studio flags contrast and large screen issues for the user to look at.

Espresso (View based screens): add `androidx.test.espresso:espresso-accessibility` and call `AccessibilityChecks.enable()` once (for example in a `@BeforeClass`); every `ViewAction` then runs the Accessibility Test Framework checks on the view hierarchy. Use `.setRunChecksFromRootView(true)` to check the whole screen, and suppress known third party issues with a matcher, never globally.

## 4. iOS automated checks

`try XCUIApplication().performAccessibilityAudit()` (Xcode 15+) in a UI test audits the current screen for contrast, hit region size, missing labels, Dynamic Type clipping, element detection and traits. Run it on each main screen after navigating there. Snapshot tests at the largest accessibility text size catch clipping on the JVM equivalent side (`ios.md` section 4). Xcode's Accessibility Inspector audits a running simulator manually.

## 5. Accessibility Scanner and the pre-launch report

- **Accessibility Scanner** (Google app on the Play Store, uses the Accessibility Test Framework): the user turns it on, opens a screen, taps the scanner button, and gets suggestions for labels, touch targets, contrast and text scaling. It can record a whole flow. It runs on the user's device, so it goes into the user checklist: "Run Accessibility Scanner on the three main screens and send me the results."
- **Play pre-launch report** runs the same framework on Google's devices for every uploaded bundle and lists touch target, contrast, labeling and implementation issues in its Accessibility tab. Read it on every testing release (`stores-and-device-farms.md` section 4). Free, no local device.
- Android Studio's lint also has accessibility checks for Views (`ContentDescription`, `ClickableViewAccessibility`, `KeyboardInaccessibleWidget`).

## 6. Touch targets

- Android: at least 48 x 48 dp (Material and Android accessibility guidance). Compose Material components enforce it through `minimumInteractiveComponentSize`.
- iOS: at least 44 x 44 pt (Apple Human Interface Guidelines).
- WCAG 2.2 criterion 2.5.8 (level AA) asks for at least 24 x 24 CSS px or enough spacing; mobile platform guidance is stricter, use it.
- React Native: a 24 px icon button needs padding or `hitSlop` to reach 48 dp. A test can read the style and `hitSlop` and compute the size; the reliable check is the Compose or Espresso framework, the pre-launch report, or the Scanner.

## 7. Font scaling, display size, contrast, motion

- **Font scale:** Android allows up to 200% (nonlinear since Android 14); iOS accessibility sizes are larger still. Text must grow and containers must grow with it. Flag `allowFontScaling={false}` on body text and any fixed `height` on text containers. Screenshot tests at font scale 2.0 (`android-native.md` section 7) and at iOS AX5 (`ios.md`). Device check: `adb shell settings put system font_scale 2.0` (tier 2) or the user changes it.
- **Display size:** largest display size makes the layout narrower in dp; test at 320 dp width.
- **Contrast:** 4.5:1 for normal text, 3:1 for large text (18 pt, or 14 pt bold) and for icons and control borders (WCAG 1.4.3 and 1.4.11). Check both themes. A unit test can compute contrast ratios of theme token pairs (foreground on background) with the WCAG formula, which catches regressions when someone edits the palette.
- **Reduced motion:** read `AccessibilityInfo.isReduceMotionEnabled()` (RN) or Reanimated's `useReducedMotion()`; test both branches by mocking the value. Large parallax, auto playing and looping motion must stop when the setting is on.
- **Color is not the only signal:** errors need text or an icon with a label, not only a red border. Assert the error text in the component test.

## 8. TalkBack test script

Hand this to the user (or follow it yourself only if the rules allow driving the device). About 5 minutes per screen.

Setup: Settings, Accessibility, TalkBack, on (or hold both volume keys for 3 seconds if the shortcut is set). In TalkBack settings, Developer settings, turn on "Display speech output" so the spoken text also appears on screen. Gestures: swipe right or left to move to the next or previous item, double tap anywhere to activate the focused item, two finger swipe to scroll, swipe down then right to go back (or the back button).

For each main screen:

1. Open the screen. Where does focus start? It should start at the top (title or back) or at the main content, not in the middle.
2. Swipe right through every item to the end. Write down what is read. Each control should say a name, a role and a state: "Save, button", "Dark mode, switch, off", "Shopping, 3 items, button".
3. Check nothing is skipped (every button reachable) and nothing is extra (decorative images, separators and icons inside a labelled button are not read).
4. Check list rows are read once as a group, not as 5 separate fragments.
5. Activate the main action with a double tap. Is the result announced (for example "Note saved") or does focus move to the new content?
6. Trigger an error (empty required field, airplane mode). Is the error read without hunting for it?
7. Open a dialog or bottom sheet. Focus moves into it and cannot escape to the screen behind; closing returns focus to where it was.
8. For any swipe only action (swipe to delete, drag to reorder), open the TalkBack actions menu on the item (swipe up then right, or three finger tap depending on the version) and check the action is offered.
9. Turn TalkBack off at the end.

Report format per screen: "Read order: ...; Problems: Save icon read as 'unlabelled button'; error not announced."

## 9. VoiceOver test script

Setup on iPhone: Settings, Accessibility, VoiceOver, on, or set the Accessibility Shortcut to triple click the side button. Gestures: swipe right or left to move, double tap to activate, three finger swipe to scroll, two finger scrub (a Z shape) to go back or close, two finger double tap for the "Magic Tap" main action (if the app supports it), rotate two fingers to open the rotor.

For each main screen: the same steps 1 to 7 as TalkBack, plus:

- Use the rotor's "Headings" item to jump between section headers. Headers must have `role="header"` / the header trait.
- Use the rotor's "Actions" item on rows with swipe actions; the actions must be listed.
- Check that the two finger scrub closes custom modals.
- Check Dynamic Type at the largest accessibility size in Settings, Accessibility, Display and Text Size, Larger Text.

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Controls found by role and name in tests | Screen tests use `getByRole(..., { name })` / Compose text or description finders for every control | `rg -c "ByRole|onNodeWithContentDescription"` vs `rg -c "ByTestId|onNodeWithTag"` |
| No unlabeled icon buttons | Every icon only button has a label | `rg -n "<Pressable|<TouchableOpacity|IconButton" -A3` reviewed for `aria-label` / `contentDescription` |
| States exposed | Toggles, checkboxes, expanders assert their state in tests | Test names and matchers |
| Gesture alternatives | Each swipe or drag action has an accessibility action and a test | `rg -n "accessibilityActions|customActions"` and matching tests |
| Automated framework checks wired | Compose `enableAccessibilityChecks()` or Espresso `AccessibilityChecks.enable()` or iOS `performAccessibilityAudit()` in device tests | `rg -n "enableAccessibilityChecks|AccessibilityChecks.enable|performAccessibilityAudit"` |
| Font scaling not disabled without reason | No `allowFontScaling={false}` on body text | `rg -n "allowFontScaling=\{false\}"` reviewed |
| Contrast of theme tokens | Unit test computes ratios for text and UI token pairs, both themes | Test exists and passes |
| Reduced motion branch tested | Both values of the setting tested | Test names |
| Pre-launch accessibility items triaged | None open without a decision | Play Console |
| Manual scripts handed over | TalkBack and VoiceOver steps in the user checklist for changed screens | End of the report |
