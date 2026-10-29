# iOS vs Android: what changes, what must not

Do not ship the same pixels to both. Ship the same product, structure and brand, and let each platform's conventions carry the interaction. People use one platform all day; anything that behaves like the other one feels broken. Sources: Apple HIG 2026, Material 3 tokens and docs, Android developer guidance.

## Contents

1. Keep the same on both
2. Adapt per platform (table)
3. Typography and icons
4. Back, up and dismissal
5. Primary actions
6. Controls that differ
7. Cross platform frameworks (React Native, Flutter, Compose Multiplatform)
8. Tests

## 1. Keep the same on both

- Information architecture: same top level destinations, same names, same order.
- Content, copy tone, brand color, illustration style, product logic.
- Data states: the same empty, error and offline cases exist on both.
- Accessibility outcomes: both work at maximum text size, with a screen reader, with switch / keyboard control.

## 2. Adapt per platform

| Topic | iOS / iPadOS | Android (Material 3) |
|---|---|---|
| Min target | 44 x 44 pt | 48 x 48 dp |
| Body text | SF Pro 17 pt (Body) | Roboto / Google Sans / brand font, 14 to 16 sp |
| Text scaling | Dynamic Type, 12 sizes, AX5 Body 53 pt | Font scale up to 200 percent, nonlinear on Android 14+ |
| Top bar | Navigation bar, large title that collapses on scroll, back chevron with previous title | Top app bar 64 dp (medium 112, large 152), up arrow, title start aligned |
| Bottom navigation | Tab bar, floating on Liquid Glass in iOS 26, filled icons when selected | Navigation bar 64 to 80 dp, active indicator pill, 3 to 5 items |
| Wide windows | Sidebar, split view, tab bar on top on iPad | Navigation rail, expanded rail, list-detail panes |
| Main create action | Toolbar button (often top trailing or bottom toolbar) | FAB (56 dp) or extended FAB, bottom trailing |
| Back | Leading edge swipe plus back button; no system back button | System back gesture from either edge or 3 button nav; predictive back animation |
| Modal sheets | Page / form sheets with detents, grabber, Cancel leading, Done trailing | Modal bottom sheet with drag handle and scrim, dialogs with 28 dp corners |
| Alerts | Centered alert, buttons stacked or side by side, destructive red | Dialog with text buttons bottom trailing, confirm on the right |
| Action choice | Action sheet / menu with destructive item last | Bottom sheet or dropdown menu |
| Transient message | No toast pattern; use inline status or a banner | Snackbar (48 dp, optional action), at the bottom above nav |
| Switch | UISwitch 51 x 31 pt look | M3 switch 52 x 32 dp track, handle grows when selected |
| Pickers | Wheels, compact date picker, menus | Date picker dialog, time dial, exposed dropdown menus |
| Selection in lists | Edit mode with circles, swipe actions | Long press to enter multi select, contextual top bar |
| Pull to refresh | System refresh control at top | Swipe refresh indicator (circle) |
| Haptics | UIFeedbackGenerator: notification, impact, selection | HapticFeedbackConstants, VibrationEffect primitives |
| Materials | Liquid Glass for controls, blur materials | Tonal surfaces, elevation as color shift, no blur by default |
| Shape | Continuous corner (squircle) curves | Corner scale 4 / 8 / 12 / 16 / 28 dp, full pill |
| Motion | Springs by damping and response, no overshoot by default | Durations 50 to 1000 ms with emphasized easing, or M3 springs (damping 0.9, stiffness 700) |
| Edge to edge | Safe area insets | Forced since Android 15; draw behind bars, pad controls by insets |
| Icons | SF Symbols, weight matched to text | Material Symbols (outlined / rounded / sharp, fill axis for selection) |
| Settings | In app settings screen, or a page in the system Settings app | In app settings screen |
| Widgets / live surfaces | Widgets, Live Activities, Dynamic Island | Widgets, ongoing notifications, Quick Settings tiles |

## 3. Typography and icons

- Use the system font unless the brand truly needs its own. SF Pro on iOS gets optical sizes and tracking automatically; a custom font needs manual tracking and must implement Dynamic Type and Bold Text.
- Icons: SF Symbols on iOS (they scale with Dynamic Type and match text weight), Material Symbols on Android. A single custom set across both is acceptable if it follows each platform's sizes (iOS symbols align to text; Android icons 24 dp in 48 dp targets).
- Never use emoji as UI icons.

## 4. Back, up and dismissal

- iOS: every pushed screen has the back chevron top leading and supports the leading edge swipe. Modals close with Cancel / Close or swipe down.
- Android: system back must always work and must do the expected thing: close the topmost sheet or dialog, then go up the stack, then leave the app. Support predictive back so users see where back goes before committing.
- Never intercept back to show "Are you sure you want to exit?" except to protect unsaved user input.

## 5. Primary actions

- Android: one FAB per screen at most, for the single most important create action. No FAB for minor or destructive actions. It sits above the navigation bar, inside the gesture inset.
- iOS: the primary action is a prominent toolbar button (trailing) or a large button in content. A floating circle button looks foreign on iOS unless it is the app's identity (for example a camera shutter).

## 6. Controls that differ

- Do not draw iOS wheels on Android or Material dropdowns on iOS. Use each platform's picker.
- Segmented control (iOS) vs segmented buttons or tabs (Android).
- Alert button order: iOS puts the preferred action on the trailing side (right) with Cancel on the leading side; Android dialogs put the confirming action on the far right too, dismissive to its left. Both: destructive actions are explicitly labeled.
- Text fields: iOS uses plain fields with placeholders and grouped forms; Android uses filled or outlined fields with floating labels. Keep the label visible after typing on both.

## 7. Cross platform frameworks

- React Native / Expo: use native stack navigators and native tabs (they give real back swipe and large titles). Use `Platform.select` for the table above; do not fake one platform's controls on the other.
- Flutter: use Cupertino widgets on iOS where the user expects them (navigation, switches, pickers, alerts) or an adaptive constructor (`Switch.adaptive`). Material on iOS is the most common "this app feels off" complaint.
- Compose Multiplatform: same rule; wrap platform navigation and pickers.
- Test on real devices of both platforms; the simulator hides haptics, grip and glare.

## 8. Tests

- A daily iPhone user and a daily Android user each try the build. Any moment where they say "that is not how my phone works" is a defect.
- Back test on Android: press system back from every screen and every open sheet.
- Swipe test on iOS: leading edge swipe on every pushed screen.
- Compare one screen side by side: same structure and content, platform appropriate bars, controls and type.
