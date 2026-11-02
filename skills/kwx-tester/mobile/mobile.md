# Mobile testing: the master file

Read this first for any test work on a mobile app: React Native and Expo (the default here), native Android with Kotlin and Compose, and iOS. It says which tests run without a device (prefer those), what makes mobile different from web, the default setup for an Expo app and for a Compose app, the rules that matter most, and which file to read next. General test design (pyramid, mocking policy, flaky policy, naming) lives in `~/.claude/skills/kwx-developer/reliability/testing-strategy.md`; this folder goes deeper on mobile only.

## Contents

1. File map: what to read when
2. Device rules: read the user's rules first
3. The 14 rules
4. Test levels on mobile, and what runs without a device
5. What is special about mobile
6. Default setup: Expo app
7. Default setup: Compose app
8. When the user asks "test this screen"
9. Checks

## 1. File map: what to read when

| File | Read when |
|---|---|
| `react-native-expo.md` | Writing or fixing Jest tests in an RN or Expo app: jest-expo, RNTL v14, mocks for native and Expo modules, Expo Router, Reanimated, gesture handler, stores, SQLite, AsyncStorage, Supabase, error messages |
| `e2e-maestro-detox.md` | Writing device E2E flows (Maestro first, Detox, Appium), picking a tool, fixing flaky E2E, running E2E in EAS Workflows or GitHub Actions |
| `android-native.md` | Kotlin or Compose app: JVM tests, Robolectric, Compose UI tests, Espresso, screenshot tests, Macrobenchmark, WorkManager, Room migrations, Hilt, coroutines and Flow |
| `ios.md` | Any iOS target: XCTest, Swift Testing, XCUITest, snapshot tests, TestFlight |
| `devices-emulators-and-adb.md` | Choosing a device and OS matrix, reading logs and state from a device, which adb commands are read only and which drive the device |
| `mobile-edge-cases.md` | Testing a screen or feature for real world conditions: process death, rotation, offline, permissions, deep links, migrations, font scale, Doze, time zones |
| `stores-and-device-farms.md` | Before a release: Play testing tracks and pre-launch report, the 12 testers rule, Firebase Test Lab, device farms, TestFlight, crash reporting, staged rollout |
| `mobile-accessibility-testing.md` | Any screen with controls: TalkBack and VoiceOver scripts, automated accessibility checks, RN accessibility props, touch targets, font scaling |

## 2. Device rules: read the user's rules first

Before you run anything that touches a phone or an emulator, read the user's `CLAUDE.md` (global and project) and follow it. Mobile testing is the area where an agent can most easily do something the user did not want: start a second emulator, download a 6 GB system image, or tap through the user's own device.

Sort every action into one of four tiers and act by the user's rules:

| Tier | What | Examples | Default when the rules are strict |
|---|---|---|---|
| 0. No device | Tests that run in Node or on the JVM | `npx jest`, `./gradlew testDebugUnitTest`, Robolectric, Roborazzi, Paparazzi, Compose Preview screenshot tests | Always allowed. Prefer these. |
| 1. Read only | Reads from a device that is already running | `adb devices`, `adb logcat -d`, `dumpsys meminfo`, `getprop`, `uiautomator dump` | Allowed if the rules allow using the device at all |
| 2. Changes state, no input | Installs, launches, toggles settings, kills the process | `adb install`, `am start -d`, `pm revoke`, `am kill`, `settings put system font_scale`, airplane mode | Ask first, unless the user already said yes for this task. Restore every setting afterwards. |
| 3. Input injection | Anything that taps, swipes or types on the device | `adb shell input ...`, `adb shell monkey`, local runs of Maestro, Detox, Appium, Espresso, UI Automator, Macrobenchmark | If the rules forbid input injection: never run `input` or `monkey`; run a test framework on the local device only after the user says yes for that run. Otherwise hand over the exact command. |

If the user's rules say something like "one emulator only, never download another" (this machine's rules do), then: reuse the existing AVD, never create an AVD, never run `sdkmanager` to fetch a system image, and if no emulator is running, ask the user to start it instead of starting it yourself. CI machines are different: a workflow may download images and boot emulators, because that does not touch the user's machine.

Visual checks you cannot make without driving the device go into a short checklist for the user at the end of the task (section 8).

## 3. The 14 rules

1. **Push every check to the lowest level that can catch it, and run that level without a device.** Logic, reducers, hooks, view models, repositories, navigation decisions and most screen behavior can be tested in Jest or on the JVM in seconds. Reason: device tests are 10 to 100 times slower and flakier; React Native's own docs call E2E "more prone to flakiness". Evidence: moderate (reactnative.dev testing overview, Android "What to test").
2. **Test what the user sees and does.** RN: query by role and label (`getByRole('button', { name: 'Save' })`), act with `userEvent`. Compose: find by text or content description first, `testTag` only when there is no visible label. Reason: the test survives refactors and checks accessibility for free. Evidence: moderate (RNTL docs, Compose testing docs).
3. **Await everything in RNTL v14.** `await render(...)`, `await user.press(...)`, `await fireEvent...`, `await renderHook(...)`. A missing `await` fails with "`render` function has not been called". Evidence: verified (RNTL 14.1.0, jest-expo 58, 2026-10-31).
4. **Mock at the native boundary, not inside your own code.** Mock the native module (`AsyncStorage`, `expo-camera`, `expo-notifications`) or the network; never mock your own hooks, stores or repositories in a screen test. Prefer fakes that keep state over mocks that record calls. Evidence: moderate (React Native testing overview "using real objects is better than mocks"; Now in Android uses no mocking library at all).
5. **Keep the native layers testable on the JVM.** Inject dispatchers, repositories and clocks; use Hilt `@TestInstallIn` fakes; run Compose UI tests under Robolectric when you cannot use a device. Evidence: moderate (Android coroutine testing guide, Now in Android).
6. **Never wait for a fixed time.** Jest: `findBy*`, `waitFor`, fake timers. Compose: idling, `waitUntil`, `mainClock`. Maestro: `assertVisible`, `extendedWaitUntil`. Reason: async wait is the top root cause of flaky UI tests (45% of 235 flaky UI tests; 32.5% on mobile). Evidence: strong (Romano et al., ICSE 2021).
7. **Device E2E covers only the few journeys that must never break.** Sign in, the core action, payment, offline then reconnect, upgrade with old data. Five to fifteen Maestro flows, run on a release build. Evidence: moderate (reactnative.dev, Expo docs).
8. **Every stored format change ships with a migration test that starts from real old data.** Room `MigrationTestHelper`, SQLite migrations from a fixture file, AsyncStorage or MMKV keys read by the new version. Reason: an upgrade that crashes on launch reaches every user at once and cannot be fixed by a new screen test. Evidence: moderate (Android Room docs).
9. **Walk the edge case catalogue for every new screen.** Process death, rotation, offline, permission denied, font scale 200%, dark mode, small screen, keyboard over inputs, double tap. Most can be checked with a unit or component test; the rest go into the user's checklist. See `mobile-edge-cases.md`. Evidence: moderate (Android "What to test" lists rotation, full storage, network errors).
10. **Test permission flows in all states:** granted, denied, denied permanently, revoked while running, limited ("only this time", partial photos). Evidence: moderate (Android permission docs, Maestro `launchApp permissions`).
11. **Pick devices by real market share and by risk, not by what is on the desk.** Cover the lowest supported OS, the most used OS, the newest OS, a small cheap phone, a large phone, and a tablet or foldable if supported. See `devices-emulators-and-adb.md`. Evidence: moderate (StatCounter, Play distribution data).
12. **Screenshot tests are few and chosen.** One per meaningful state and theme, rendered on the JVM (Roborazzi, Paparazzi, Compose Preview Screenshot Testing) or by `swift-snapshot-testing`; record them on CI, not on a laptop. Evidence: moderate (Android screenshot testing guide).
13. **Check accessibility in the same tests.** Assert accessible names and roles in RNTL, enable Compose `enableAccessibilityChecks()` or Espresso `AccessibilityChecks.enable()` on device runs, keep touch targets at 48 dp (Android) and 44 pt (iOS). Evidence: moderate (Android and Apple docs).
14. **Treat store and crash data as tests that run on real users.** Read the Play pre-launch report, roll out in stages, gate the next stage on crash free sessions and ANR rate. Evidence: moderate (Play Console help).

## 4. Test levels on mobile, and what runs without a device

| Level | React Native / Expo | Android native | iOS | Needs a device? |
|---|---|---|---|---|
| Static | `tsc --noEmit`, ESLint with `eslint-plugin-testing-library` | `./gradlew lint`, detekt or ktlint | SwiftLint, compiler warnings | No |
| Unit | Jest on pure TS modules, stores, hooks (`renderHook`) | JUnit on the JVM (`src/test`), `runTest`, Turbine | XCTest or Swift Testing | No |
| Component / screen | Jest + RNTL, Expo Router `renderRouter` | Compose UI tests under Robolectric, or on device | XCTest with view models; `swift-snapshot-testing` | No (Robolectric, Jest). Yes for the device variant |
| Screenshot | Not standard in RN Jest (use Maestro `assertScreenshot` on device sparingly) | Roborazzi, Paparazzi, Compose Preview Screenshot Testing | `swift-snapshot-testing` on a fixed simulator | No for JVM tools; iOS needs a simulator |
| Integration with real backend | Jest in Node against a local Supabase (`supabase start`) | JVM tests against a local server or MockWebServer | XCTest against a local server | No |
| Instrumented / E2E | Maestro (default), Detox | Espresso, Compose on device, UI Automator, Maestro | XCUITest, Maestro | Yes |
| Performance | Release build profiling, Flashlight, Maestro timings | Macrobenchmark, baseline profiles | XCTest metrics, Instruments | Yes, a real device for numbers |
| Real users | Pre-launch report, beta tracks, Sentry | Same, plus Android vitals | TestFlight, Xcode Organizer | Store infrastructure |

When the user's rules restrict emulator use, everything above the "Instrumented" row is still available. A good Expo or Compose project can prove most behavior there and leave the device for a short final checklist.

## 5. What is special about mobile

- **Lifecycle.** The OS can pause, stop and kill your process at any time and later restore it. Data that lives only in memory is lost. In React Native, app state lives in JS memory, so after process death the JS starts again and the app opens at its initial route unless the code persists navigation state and data. Test that drafts and in progress work are persisted.
- **Permissions** change at runtime and can be revoked from Settings while the app runs (on Android that kills the process).
- **Devices and OS versions.** Thousands of screen sizes, OEM skins, OS versions from about 5 years back. Behavior changes per target SDK: for example Android 15 enforces edge to edge for apps targeting API 35, and Android 16 ignores orientation and resizability locks on screens 600 dp and wider for apps targeting API 36.
- **Network** is slow, flaky or missing, and switches between Wi-Fi and cellular in the middle of a request.
- **Background limits.** Doze, App Standby buckets, battery savers from OEMs and iOS background rules delay or drop scheduled work.
- **Stores.** You cannot hotfix a native binary in minutes. Review takes hours to days, users update late, and old versions stay in use for months. Every server and data format must keep working with the oldest app version still in use.
- **Input.** Touch, back gesture, hardware keyboard, screen readers, a soft keyboard that covers half the screen.
- **OTA updates** (EAS Update) can change JS without a store release, so the JS bundle and the native binary can mismatch. Test an update against the oldest binary in the `runtimeVersion` it targets.

## 6. Default setup: Expo app

Verified on a fresh `create-expo-app` (Expo SDK 58, React Native 0.88, React 19.3, Jest 30, jest-expo 58.0.13, RNTL 14.1.0, test-renderer 1.3.1) on 2026-10-31.

```sh
npx expo install jest-expo jest @types/jest @testing-library/react-native test-renderer --dev
```

`--dev` goes before any `--`; text after `--` is passed to npm (where `--dev` does nothing, so the packages land in `dependencies`). Verified.

```json
{
  "scripts": { "test": "jest" },
  "jest": {
    "preset": "jest-expo",
    "setupFilesAfterEnv": ["./jest-setup.ts"]
  }
}
```

- Tests live in `__tests__` folders and end in `-test.tsx` (the jest-expo default) or `.test.tsx`. Never put tests in `app/`: every file there is a route.
- Add `"jest"` to `compilerOptions.types` in `tsconfig.json`.
- Add the Reanimated resolver and setup only if the app uses Reanimated (see `react-native-expo.md` section 6).
- E2E: Maestro flows in `.maestro/`, run in EAS Workflows on every pull request (`e2e-maestro-detox.md`).
- Do not add `react-test-renderer`; it does not support React 19 and RNTL v14 replaced it with `test-renderer`.

## 7. Default setup: Compose app

Follow Now in Android (github.com/android/nowinandroid), Google's reference app:

- Local JVM tests in `src/test` for view models, repositories, use cases (`./gradlew testDebugUnitTest`).
- Test doubles that implement the production interface, swapped in with Hilt `@TestInstallIn`. No mocking library.
- A `demo` flavor with static local data so UI and screenshot tests are deterministic. Run tests per variant (`testDemoDebug`), not the global `test` task.
- Compose UI tests with the v2 rule (`androidx.compose.ui.test.junit4.v2.createComposeRule`), runnable under Robolectric in `src/test` and on a device in `src/androidTest`.
- Roborazzi screenshot tests on the JVM (`recordRoborazziDemoDebug`, `verifyRoborazziDemoDebug`), recorded and verified on Linux CI.
- `kotlinx-coroutines-test` with a `MainDispatcherRule`, Turbine for Flows.
- Room schemas exported to `schemas/` and a migration test per version step.
- Macrobenchmark and a baseline profile module, run on a real device by a person or in a device farm.

Details and code in `android-native.md`.

## 8. When the user asks "test this screen"

1. Read the spec or the issue. Write down the behaviors to prove before you read the implementation.
2. List the states: loading, empty, content, error, offline, permission denied, signed out.
3. Write component tests for each state and each user action (RNTL or Compose under Robolectric). Assert what the user sees.
4. Walk `mobile-edge-cases.md` and add a test for every case that a unit or component test can cover.
5. If the screen is on a critical journey, add or extend one Maestro flow. Do not run it locally unless the user said yes; CI runs it.
6. Run the device free suite and report the exact command and result.
7. End with a checklist for the user, for what only a person on a device can confirm, for example:
   - Rotate on the edit screen with text typed: text stays.
   - Font size at maximum in system settings: no clipped labels on the Save row.
   - TalkBack on: the Save button is read as "Save, button".

## 9. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| User's device rules read | Actions match the tiers allowed by `CLAUDE.md` | State in the report which tier each command was |
| No emulator started or image downloaded by the agent | None | Review your own commands: no `emulator -avd`, `avdmanager create`, `sdkmanager "system-images..."` |
| No input injection without a yes | No `adb shell input`, `monkey`; framework runs only after explicit approval | Review your commands |
| Device free suite exists and passes | `npx jest` or `./gradlew testDebugUnitTest` green | Run it, paste the summary line |
| Async discipline | No unawaited RNTL calls, no fixed sleeps | `rg -n "^\s*(render|fireEvent|renderHook)\(" __tests__ src` returns nothing; `rg -n "setTimeout\(|Thread.sleep|waitForTimeout" --glob '*test*'` |
| Queries are user facing | `getByTestId` and `onNodeWithTag` are a minority | `rg -c "ByTestId|onNodeWithTag" ` vs `rg -c "ByRole|ByText|ByLabel|onNodeWithText"` |
| Edge case catalogue walked | Each case marked covered, not applicable, or in the user checklist | Table in the report |
| Migration test for every stored format change | Present in the same change | Diff contains a migration test when schemas or storage keys change |
| E2E flows only for critical journeys | 5 to 15 flows, each named after a journey | `ls .maestro` |
| User checklist written | Every visual or device only check is listed | End of the report |
