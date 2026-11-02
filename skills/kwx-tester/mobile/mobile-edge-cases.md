# Mobile edge cases: the catalogue

A list an agent walks through for every new or changed screen. For each case: what goes wrong, how to cover it in code without a device (preferred), how to reproduce it on a device (with the tier from `mobile.md` section 2, so you know when to ask), and what to put in the user's checklist when only a person can confirm it. Most real mobile bugs come from these conditions, not from the happy path. Android's own "What to test" guide names several of them (network errors, malformed data, full storage, recreation on rotation). Device commands are detailed in `devices-emulators-and-adb.md`.

## Contents

1. How to use the catalogue
2. Lifecycle: process death, background and foreground, rotation and resize
3. Network: offline, flaky, airplane mode during a write
4. Permissions
5. Notifications
6. Deep links
7. App update with old data
8. Resources: low storage, low memory, battery saver and Doze, slow device
9. Time, locale, RTL
10. Display: font scale, display size, dark mode, screen sizes, edge to edge
11. Input: keyboard, back gesture, double tap
12. Interruptions and sessions
13. Checks

## 1. How to use the catalogue

For each screen, copy this table into your notes and fill the last column: covered (test name), not applicable (why), or user checklist.

| # | Case | Status |
|---|---|---|
| 1 | Process death and restore | |
| 2 | Background and foreground | |
| 3 | Rotation, resize, foldable, multi window | |
| 4 | Offline and flaky network | |
| 5 | Airplane mode during a write | |
| 6 | Permission denied, revoked, limited | |
| 7 | Notifications (permission, tap, while open) | |
| 8 | Deep link cold and warm | |
| 9 | App update with old data | |
| 10 | Low storage | |
| 11 | Low memory | |
| 12 | Battery saver and Doze | |
| 13 | Time zone and clock change | |
| 14 | Locale and RTL | |
| 15 | Font scale 200% | |
| 16 | Display size | |
| 17 | Dark mode | |
| 18 | Small and large screens | |
| 19 | Edge to edge, insets, notches | |
| 20 | Keyboard covering inputs | |
| 21 | Back gesture | |
| 22 | Double tap on buttons | |
| 23 | Slow device | |
| 24 | Interruptions and expired session | |

The report ends with the user checklist: only the items no test could prove, each a single action and expected result.

## 2. Lifecycle

### 2.1 Process death and state restore

- **Risk:** the OS kills a backgrounded app to free memory. When the user returns, Android recreates the last screen, but anything kept only in memory is gone: a half written form, a selected tab, an in progress upload. In React Native, all JS state is lost and the app starts at its initial route unless navigation state and drafts are persisted. Compose: plain `remember` is lost, `rememberSaveable` and `SavedStateHandle` survive.
- **In code:** RN: test that drafts are written to storage as the user types (debounced) and restored on mount (component test with the AsyncStorage or MMKV mock: render, type, unmount, render again, assert the text). Compose: `StateRestorationTester(composeTestRule).setContent { ... }` then `emulateSavedInstanceStateRestore()` and assert; view model: construct with a `SavedStateHandle` holding saved values and assert the state.
- **On a device (tier 2):** open the screen, type, press Home, `adb shell am kill <pkg>`, reopen from Recents. Or developer option "Don't keep activities" (user setting). `am force-stop` is not the same: it clears the task.
- **User check:** "Type in the note, switch to another app for a while (or use 'Don't keep activities'), come back: the text is still there."

### 2.2 Background and foreground

- **Risk:** timers, sockets, video and location keep running in background (battery, crashes), or do not restart on return (stale data, frozen spinners). Auth tokens expire while backgrounded.
- **In code:** RN: mock `AppState` change events (`AppState.addEventListener` listeners called with `'background'` then `'active'`) and assert that polling stops and a refresh happens. Compose / Android: lifecycle aware collection (`collectAsStateWithLifecycle`), test with `TestLifecycleOwner` moving through `ON_STOP` and `ON_START`.
- **On a device (tier 2):** `launchApp: { stopApp: false }` in Maestro after `pressKey: Home`.
- **User check:** "Leave the app open on the list, lock the phone for 10 minutes, unlock: the list refreshes, no endless spinner."

### 2.3 Rotation, resize, foldables, multi window

- **Risk:** Activity recreation loses state (2.1 again), layouts break in landscape, dialogs vanish. Android 16 ignores orientation, aspect ratio and resizability locks on screens 600 dp and wider for apps targeting API 36, so a "portrait only" app will be shown in landscape on tablets and unfolded foldables; Google warns of "overlapping layouts". The opt out property goes away at API 37.
- **In code:** Robolectric `ActivityScenario.recreate()` keeps input (`android-native.md` section 4). Compose screenshot tests at 360 dp, 600 dp and 840 dp widths and in landscape. RN: test layout logic that depends on `useWindowDimensions` by mocking the hook's return.
- **On a device (tier 2):** `wm size` to emulate a tablet size; rotation by the user.
- **User check:** "Rotate while editing: text stays, nothing overlaps. On a tablet or unfolded foldable: the screen fills sensibly."

## 3. Network

### 3.1 Offline and flaky network

- **Risk:** infinite spinners, raw error text, lost writes, duplicate writes after retry, crash on a malformed or partial response.
- **In code:** fake repository or MSW handlers returning: network error, timeout, 500, 401, 429, slow response, malformed JSON, empty list. Assert each shows a clear message and a retry. Test the offline queue: writes made offline are stored, replayed once on reconnect, and carry an idempotency key so a retried request is not applied twice. RN: mock `@react-native-community/netinfo` state changes.
- **On a device (tier 2):** `svc wifi disable` and `svc data disable`, emulator `adb emu network speed edge` and `network delay gprs`, Maestro `setAirplaneMode`. A real flaky network (elevator, train) only by the user.
- **User check:** "Turn on airplane mode, open the app: cached list shows with an offline note; create an item; turn airplane mode off: the item syncs once."

### 3.2 Airplane mode during a write

- **Risk:** the request left the phone but the response never came back. The app shows "failed", the user retries, the server now has two copies. Or the app shows "saved" while nothing was saved.
- **In code:** fake transport that applies the write on the server side then throws a network error; assert that the client retries with the same idempotency key and the server ends with one record. Fake that fails before sending; assert the item stays in the outbox with a visible "not synced" state.
- **On a device (tier 2):** toggle airplane mode in a Maestro flow between `tapOn: Save` and the assertion (timing is unreliable; use it as a smoke check, not proof).
- **User check:** "Press Save and switch on airplane mode at once: after reconnecting there is exactly one copy."

## 4. Permissions

- **Risk:** the app assumes "granted". Real states: granted; denied once (can ask again); denied permanently (Android: denied twice, `canAskAgain: false`; the app must send the user to Settings); revoked in Settings while the app runs (Android kills the process); "only this time" one time grants (Android 11+, location, camera, microphone) that expire after the app leaves the foreground; permissions auto reset for unused apps (Android 11+); approximate instead of precise location (Android 12+); partial photo access (Android 14 `READ_MEDIA_VISUAL_USER_SELECTED`, iOS limited library); notifications permission (Android 13+ `POST_NOTIFICATIONS`).
- **In code:** mock the permission module (`expo-location`, `expo-camera`, `expo-notifications`, `expo-media-library`, or the Android `ActivityResultContracts.RequestPermission` callback through a fake) with each state and assert the screen: explanation, fallback (manual city entry, pick from files), "Open settings" button when blocked. One test per state.
- **On a device:** Maestro `launchApp: { permissions: { all: deny } }` and `setPermissions` (tier 3 because Maestro drives the app); `adb shell pm revoke <pkg> android.permission.CAMERA` while the app runs (tier 2, kills the process: check the app recovers).
- **User check:** "Deny camera, then try the scan feature: a clear message and a way to continue. Allow 'only this time', leave and return: the app asks again without crashing. Choose 'Select photos' with two photos: only those two are shown."

## 5. Notifications

- **Risk:** permission never requested on Android 13+ (no notifications at all), tap opens the wrong screen or crashes on a cold start, a notification for deleted content, duplicate notifications, notifications while the app is in foreground not handled, OEM battery savers delaying them.
- **In code:** test the function that maps a notification payload to a route (pure function: payload in, route out, including unknown and malformed payloads). Test the foreground handler (`Notifications.setNotificationHandler` in Expo) with a mocked module.
- **On a device:** push from your server's test endpoint or the Expo push tool to a development build. Since Expo SDK 53, Expo Go on Android does not support remote push; use a development build. iOS simulator: `xcrun simctl push` (tier 2).
- **User check:** "With the app closed, tap the reminder notification: it opens the right note. With the app open: a banner shows, no crash."

## 6. Deep links

- **Risk:** link works warm but not cold (the app is not running and the navigator is not ready yet), unknown paths crash, missing parameters, a link to content the user cannot see, auth required (must return to the link after sign in), Android App Links not verified so links open the browser.
- **In code:** Expo Router `renderRouter(..., { initialUrl: '/note/42' })` for cold start routing, plus unknown path (`+not-found`), missing params, signed out redirect and return (`react-native-expo.md` section 5). Native: test the intent to route parser on the JVM.
- **On a device (tier 2):** cold: `am force-stop` then `adb shell am start -W -a android.intent.action.VIEW -d "notes://note/42" <pkg>`; warm: the same with the app in background. iOS: `xcrun simctl openurl booted "notes://note/42"`. App Links verification state: `adb shell pm get-app-links <pkg>` (read only).
- **User check:** "Tap a shared https link to a note in Messages with the app closed: the app opens on that note."

## 7. App update with old data

- **Risk:** the new version crashes on launch reading old storage (renamed key, changed JSON shape, missing DB migration), wipes data through a destructive fallback, or an OTA JS update expects a native module the installed binary lacks.
- **In code:** keep fixtures of every released storage format: an AsyncStorage or MMKV snapshot, a SQLite file or SQL dump per schema version, a Room schema JSON. Tests load each fixture and run the current code (Room `MigrationTestHelper`, SQLite migrations in Node through `better-sqlite3`, store hydration with old shapes). Test that unknown fields are ignored and missing fields get defaults.
- **On a device (tier 2 and 3):** install the previous release APK, create data, `adb install -r` the new build, open. This is a good Maestro flow for CI. For EAS Update, publish to a channel used by the oldest binary of that `runtimeVersion` and open it.
- **User check:** "Update from the store version to this build without uninstalling: all notes are still there."

## 8. Resources

### 8.1 Low storage

- **Risk:** writes fail (SQLite "database or disk is full", file download half written), the app crashes instead of reporting.
- **In code:** fake file system or DB adapter that throws a disk full error on write; assert a message and that the old data is intact (write to a temp file, then rename).
- **On a device:** fill the emulator's storage (tier 2, slow, ask), or leave to the user.
- **User check:** usually skipped unless the app downloads large files.

### 8.2 Low memory

- **Risk:** large images decoded at full size, leaks of screens or listeners, the OS killing the app often (then 2.1 matters).
- **In code:** leak checks with LeakCanary in debug builds (Android); image loading through a library that downsamples.
- **On a device (tier 2):** `am send-trim-memory <pkg> RUNNING_CRITICAL`; open and close a screen 20 times and compare `dumpsys meminfo` Activities count (read only).
- **User check:** "Scroll the photo grid quickly for 30 seconds on the older phone: no crash, no blank tiles that stay blank."

### 8.3 Battery saver and Doze

- **Risk:** scheduled work, alarms and syncs are delayed by hours; OEM savers kill background work; exact alarms need a special permission (Android 12+ `SCHEDULE_EXACT_ALARM`).
- **In code:** WorkManager `TestDriver` with constraints not met, then met (`android-native.md` section 10). Logic must not assume work ran on time; compute "due" from timestamps.
- **On a device (tier 2):** `dumpsys battery unplug` plus `dumpsys deviceidle force-idle`, then `unforce` and `battery reset`; App Standby bucket `rare`.
- **User check:** "Turn on battery saver overnight: the morning reminder still arrives (maybe a few minutes late), the daily sync ran when the phone woke."

### 8.4 Slow device

- **Risk:** jank, ANRs (main thread blocked 5 s), timeouts tuned on a fast phone, a double render visible as flicker.
- **In code:** move heavy work off the main thread and test it as a pure function; StrictMode in debug builds flags disk and network on the main thread.
- **On a device:** profile a release build on a cheap phone; Macrobenchmark on a real device (`android-native.md` section 11).
- **User check:** "On the oldest phone, open the app cold: first screen in about 2 seconds, scrolling the list stays smooth."

## 9. Time, locale, RTL

### 9.1 Time zone and clock change

- **Risk:** dates shown a day off, reminders at the wrong hour after travel or DST, "today" computed in UTC, token expiry checks fooled by a wrong device clock, 12 hour vs 24 hour format.
- **In code:** inject the clock and the zone. Tests with fixed instants on DST change days (for example 2026-03-29 and 2026-10-25 in Europe), at 23:30 local in a zone ahead of UTC, and in a zone behind it. Run the suite with `TZ=UTC` and add explicit tests for other zones through the injected formatter. Server decides expiry, not the device clock.
- **On a device:** emulator `-timezone` boot option, or the user changes zone and time in Settings.
- **User check:** "Change the phone's time zone to New York while the app is open: the reminder time shown follows the rule in the spec (local wall time or fixed instant)."

### 9.2 Locale and RTL

- **Risk:** strings truncated in German or Russian (30 to 40% longer than English), hard coded strings, wrong plural forms (Russian and Kazakh have several), number and date formats, Arabic and Hebrew mirroring (icons with direction, padding start and end, swipe directions).
- **In code:** test formatting functions with `ru`, `de`, `ar` locales; screenshot tests in RTL and with pseudolocales (Android `en-XA` for long accented text, `ar-XB` for RTL, enabled with `pseudoLocalesEnabled true` in debug builds); RNTL tests with `I18nManager.isRTL` mocked where layout logic depends on it.
- **On a device (tier 2):** per app language `cmd locale set-app-locales <pkg> --locales ar` (Android 13+).
- **User check:** "Switch the phone to Arabic: the layout mirrors, back arrows point the right way, nothing is cut off."

## 10. Display

### 10.1 Font scale 200%

- **Risk:** clipped labels, overlapping rows, buttons with fixed heights that cut text, text that does not scale at all. Android 14 allows up to 200% with nonlinear scaling; iOS accessibility sizes go higher.
- **In code:** Compose screenshot at `fontScale = 2f`; iOS snapshot at accessibility XXXL; RN: check no `allowFontScaling={false}` on body text and that `maxFontSizeMultiplier` is only used with a reason (`rg -n "allowFontScaling=\{false\}|maxFontSizeMultiplier"`).
- **On a device (tier 2):** `settings put system font_scale 2.0`, restore the recorded value.
- **User check:** "Set font size to the maximum: every button label is fully readable, rows grow instead of clipping."

### 10.2 Display size

- **Risk:** at the largest display size a 411 dp phone behaves like a 320 dp one; layouts tuned for 360 dp overflow.
- **In code:** screenshot at 320 dp width.
- **On a device (tier 2):** `wm density` higher, then `wm density reset`.
- **User check:** combined with 10.1 on the smallest phone.

### 10.3 Dark mode

- **Risk:** hard coded colors, dark text on dark background, images and icons without dark variants, a status bar with invisible icons.
- **In code:** screenshot tests in both themes; RN: grep for literal colors outside the theme file.
- **On a device (tier 2):** `cmd uimode night yes`; Maestro `assertDarkMode`.
- **User check:** "Switch the system to dark mode: every screen is readable, no white flashes on navigation."

### 10.4 Small and large screens

- **Risk:** content cut at 360 x 640 dp, huge empty space on tablets, bottom sheets taller than the screen.
- **In code:** screenshot widths 320, 360, 411, 600, 840 dp; layout logic by window size class tested as a function.
- **User check:** "On the small phone, every screen's main button is reachable without hidden overflow."

### 10.5 Edge to edge, insets, notches

- **Risk:** Android 15 enforces edge to edge for apps targeting API 35, so content goes under the status and navigation bars unless insets are applied; buttons under the gesture bar; content under a camera cutout.
- **In code:** Compose: screenshot tests with system bars (Roborazzi with a real Activity); RN: `react-native-safe-area-context` mock returns non zero insets in a test and the layout uses them.
- **User check:** "On a phone with gesture navigation, the bottom button is fully above the gesture bar; nothing hides under the camera hole."

## 11. Input

### 11.1 Keyboard covering inputs

- **Risk:** the soft keyboard hides the focused field or the Submit button; edge to edge makes this worse when IME insets are ignored.
- **In code:** hard to prove in Jest or Robolectric. Check the code uses the platform's keyboard handling (`KeyboardAvoidingView` or `react-native-keyboard-controller` in RN, `imePadding()` or `WindowInsets.ime` in Compose).
- **User check:** "On the small phone, tap the last field of the form: it stays visible above the keyboard, and Submit is reachable."

### 11.2 Back gesture

- **Risk:** back closes the app from a nested screen, discards a draft without asking, or does nothing. Android 16 enables predictive back animations by default for apps targeting API 36 and stops calling `onBackPressed`; old back handling silently stops working.
- **In code:** RN: `BackHandler` mocked and its listener invoked; Expo Router `testRouter.back()` with an unsaved changes guard. Compose: `BackHandler` / `PredictiveBackHandler` tested with `composeTestRule.activityRule.scenario.onActivity { it.onBackPressedDispatcher.onBackPressed() }`.
- **User check:** "With unsaved text, swipe back: the app asks before discarding. On the home screen, back leaves the app."

### 11.3 Double tap on buttons

- **Risk:** two orders, two notes, two navigations stacked, a crash from navigating twice.
- **In code:** press the button twice quickly (`await user.press(btn); await user.press(btn);` in RNTL, two `performClick()` in Compose) and assert one request and one navigation. Disable the button while the action runs and test `toBeDisabled()`. Server side idempotency still required.
- **User check:** "Double tap Save fast: one item is created."

## 12. Interruptions and sessions

- **Risk:** a phone call or another app's audio interrupts playback or recording; the system share sheet or camera returns while the app was killed; the session expired while backgrounded and the next request fails with 401 in a loop.
- **In code:** test the 401 path: refresh once, retry once, on refresh failure go to sign in with the current route remembered. Audio focus and interruption handlers as functions.
- **User check:** "Take a photo with the in app camera on the older phone: after the camera returns, the photo is attached (no restart to an empty form)."

## 13. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Catalogue walked | All 24 rows marked covered, not applicable, or user checklist | Table in the report |
| Lowest level used | Each "covered" row points to a unit, component or screenshot test where one is possible | Test names in the table |
| Device actions within the rules | Tier 2 and 3 actions only with the user's yes | Review commands |
| Settings restored | Every changed device setting set back to the recorded value | List in the report |
| User checklist short and concrete | One action and one expected result per line, only device only items | End of the report |
