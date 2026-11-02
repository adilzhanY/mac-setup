# Mobile E2E: Maestro, Detox, Appium

How to write and run end to end tests that drive a real app on an emulator, simulator or phone: Maestro flows (the default), Detox (gray box, React Native only), Appium (overview), which one to pick for Expo, why mobile E2E is flaky and how to fix each cause, and how the tests run in CI (EAS Workflows, GitHub Actions with an emulator) compared with local runs. Local runs tap and type on the device, so under rules like "never inject input into an emulator" they need the user's yes for each run. The short version of this topic is in `~/.claude/skills/kwx-developer/reliability/testing-strategy.md` section 8.

## Contents

1. When to write an E2E test
2. Local runs and the user's rules
3. Maestro: flows, selectors, assertions
4. Maestro: structure, Studio, Cloud
5. Detox
6. Appium
7. Which tool to pick
8. Why mobile E2E is flaky, and the fix for each cause
9. Running E2E in CI
10. Checks

## 1. When to write an E2E test

Write one only for a journey that must never break and that lower levels cannot prove: the app boots on a real OS, the native modules link, navigation and the backend work together. Typical set for a small app, 5 to 15 flows:

- First launch and onboarding, then sign up or sign in.
- The core action (create, save, send) and seeing its result.
- Payment or purchase (in a sandbox).
- Offline: do the core action in airplane mode, reconnect, see it sync.
- Upgrade: install the previous release, create data, install the new build, data is still there.
- Deep link into a screen, cold and warm.
- Permission denied path for the main permission.

Every edge case that a component test can cover belongs in the component test (React Native's docs: cover vital parts with E2E, "use faster JS tests for the non-vital parts"). Evidence: moderate.

## 2. Local runs and the user's rules

Maestro "reproduces physical actions, like thumbs on a screen, by sending low-level device commands for tap events, swipe gestures, and text input" through a driver app it installs on the device (Maestro docs, "How Maestro works"). Detox, Appium, Espresso and UI Automator do the same. A local run is input injection.

Before any local run:

1. Read the user's `CLAUDE.md`. If it forbids injecting input into an emulator or phone, do not run the suite yourself. Write the flows, check their YAML or code, and ask: "May I run `maestro test .maestro/` on your running emulator now? It will tap through the app for about 2 minutes." Run only after a clear yes, for that run.
2. Never start an emulator, create an AVD or download a system image when the rules say to reuse one emulator. If the emulator is not running, ask the user to start it.
3. Never run on the user's personal phone unless they name it.
4. Prefer CI: EAS Workflows or GitHub Actions run the same flows on a throwaway emulator (section 9). That needs no permission from the local rules, only a push.
5. Report what ran, where, and the result. If nothing ran, say so plainly: "Flows written and linted, not run; CI will run them on the pull request."

## 3. Maestro: flows, selectors, assertions

Install (Maestro docs; needs Java 17+): `curl -fsSL "https://get.maestro.mobile.dev" | bash`. Pin a version on CI with `MAESTRO_VERSION`.

A flow is a YAML file: config, `---`, then commands.

```yaml
# .maestro/create-note.yml
appId: com.example.notes
name: Create a note and see it in the list
tags:
  - core
---
- launchApp:
    clearState: true
    permissions:
      all: deny
      notifications: allow
- runFlow: subflows/sign-in.yml
- tapOn:
    id: "new_note_button"
- tapOn: "Title"
- inputText: "Shopping"
- hideKeyboard
- tapOn:
    text: "Save"
    enabled: true
- assertVisible: "Shopping"
- assertNotVisible: "Saving..."
```

Selectors (Maestro docs, "How to use Selectors"):

- A plain string is a text selector, and text and `id` are regular expressions by default (`"Saved .*"`).
- `id` matches React Native `testID`, Android resource id, Compose `testTag` (only with `testTagsAsResourceId = true` on a root `Modifier.semantics`), iOS `accessibilityIdentifier`.
- Combine attributes for an AND match: `id`, `text`, `enabled`, `checked`, `focused`, `selected`, `index`, relational `below`, `above`, `leftOf`, `rightOf`, `childOf`, `containsChild`.
- Maestro's own advice: prefer visible text (it checks what the user sees), use `id` for icons and for localized apps, anchor dynamic elements with relational selectors, add `enabled: true` before tapping a button that waits for validation or an API call.

Assertions and waiting:

- `assertVisible` and `assertNotVisible` poll until the condition holds or the timeout passes. Use them as your waits.
- `extendedWaitUntil: { visible: "Payment confirmed", timeout: 30000 }` for slow operations. Do not set 60 s everywhere; a slow screen is a bug to see.
- `waitForAnimationToEnd` after transitions; `tapOn: { ..., retryTapIfNoChange: true }` for taps that land before the button is ready.
- `assertTrue: ${output.count > 0}` with JavaScript for computed checks.
- `assertScreenshot: { path: ..., cropOn: ..., thresholdPercentage: 95 }` for a visual check. Use sparingly and crop to the element; device and font differences break full screen comparisons.
- Never use a fixed sleep. Maestro has no `sleep`, and `waitForAnimationToEnd` is not a sleep.

Device control useful for edge cases (all are device state changes): `setAirplaneMode: enabled`, `toggleAirplaneMode`, `setLocation`, `setPermissions`, `setClipboard`, `openLink` (deep links), `killApp`, `stopApp`, `clearState`, `launchApp: { stopApp: false }` (bring back from background without restart), `pressKey: back`, `assertDarkMode`.

Permissions: `launchApp` grants all permissions by default. Set them explicitly so the flow tests one path: `permissions: { all: deny, camera: allow }`. A value can come from an env variable, so one flow covers both granted and denied: `camera: ${CAMERA_PERMISSION_STATE}` with `--env CAMERA_PERMISSION_STATE=deny`.

Expo specifics (Maestro docs, React Native page):

- Test a development or release build with `launchApp` and your `appId`. With Expo Go you cannot use `launchApp` with your own `appId`; use `openLink: exp://127.0.0.1:8081` instead. Prefer a release like build: E2E on a debug build with Metro is slower and fails for reasons users never see.
- On iOS, nested touchables can swallow taps. Make the inner element `accessible` and the outer one `accessible={false}`.
- `testID` on React Native components becomes `id` in Maestro on both platforms.

## 4. Maestro: structure, Studio, Cloud

```
.maestro/
  config.yaml            # optional: flows to include, executionOrder, tags
  subflows/sign-in.yml   # reused by runFlow, not run on its own
  create-note.yml
  offline-sync.yml
  upgrade-keeps-data.yml
```

- One flow per journey, named after the journey. Shared steps in `subflows/` called with `runFlow`, with env parameters.
- Each flow starts from a known state: `launchApp: { clearState: true }` and its own test account or seeded data. No flow depends on another flow having run.
- `onFlowStart` and `onFlowComplete` hooks for setup and cleanup (for example a JavaScript `http.post` to a test endpoint that seeds data).
- Tags (`core`, `slow`) let CI run a smoke set on every pull request and the full set nightly: `maestro test --include-tags core .maestro/`.
- Reports: `maestro test --format junit --output build/report.xml .maestro/` (also `html`, `html-detailed`); screenshots and logs go to `~/.maestro/tests/` on macOS and Linux, or to `--test-output-dir=build/maestro-results` (Maestro docs, "Test reports and artifacts").
- `maestro hierarchy` prints the accessibility tree of the current screen. It is read only and is the fastest way to find a selector (it still needs a running device).
- **Maestro Studio** is a desktop app that mirrors the device; you click an element and it suggests the command. It is for the user to build flows by hand. An agent should not drive it.
- **Maestro Cloud** runs flows in parallel on hosted devices (paid plan, 20 minute soft limit per flow): `maestro cloud --app-file app.apk --flows .maestro/`. Pick OS and model with `--device-os` and `--device-model`. Useful when the user has no CI emulator and does not want local runs.

## 5. Detox

Detox (wix.github.io/Detox, version 20.x) is a gray box framework for React Native. It runs inside the app and waits until the app is idle before each step. It watches in flight network requests, the main thread queue, layout (including the Yoga shadow queue), JS timers, animations (Animated and Reanimated), the JS thread, and the native module thread. That removes most manual waits.

Costs:

- It needs native build steps and a test runner (Jest) wired into the Android `androidTest` source set. For Expo that means `expo prebuild` and a config plugin. The official `@config-plugins/detox` stopped at about SDK 52 and a community fork took over from SDK 54 (search results, 2026; check before adopting).
- An app that is never idle (a looping animation, a polling `setInterval`, an open WebSocket that keeps sending) makes Detox wait until it times out. Fix the app or exclude the resource; `device.disableSynchronization()` is a last resort that brings back manual waits.
- Configuration names a device. Under a "one emulator only" rule, set the AVD name to the user's existing emulator and never let Detox create one.

Shape of a test (Detox docs; not verified here):

```js
describe('Notes', () => {
  beforeAll(async () => { await device.launchApp({ newInstance: true, delete: true }); });

  it('creates a note', async () => {
    await element(by.id('new_note_button')).tap();
    await element(by.id('title_input')).typeText('Shopping');
    await element(by.text('Save')).tap();
    await expect(element(by.text('Shopping'))).toBeVisible();
  });
});
```

Commands: `detox build --configuration android.emu.release`, then `detox test --configuration android.emu.release`.

## 6. Appium

Appium (version 3 since 2025) is a WebDriver server with drivers per platform (UiAutomator2 and Espresso for Android, XCUITest for iOS) and clients in many languages (WebdriverIO for JS). It is black box and language neutral, works for any app stack, and is what most device farms support first. It is also the slowest to write and the most verbose, and it has no built in waiting comparable to Maestro or Detox. Choose it when a QA team already uses it, when tests must be written in Java or Python, or when a device farm requires it.

## 7. Which tool to pick

| Situation | Pick | Why |
|---|---|---|
| Expo app, solo developer | **Maestro** | No code in the app, no native setup, YAML an agent and the owner can both read, first class EAS Workflows job, works on Android and iOS |
| Bare RN app with heavy async work and native build skills | Detox | Gray box sync removes waits; worth it only if the team maintains native test setup |
| Native Android only | Compose UI tests and Espresso in `androidTest`, plus a few Maestro flows for cross screen journeys | First party, runs under Robolectric too |
| Native iOS only | XCUITest, plus Maestro if you also ship Android | First party |
| Existing Appium suite or a farm that requires it | Appium | Do not rewrite a working suite |

Default for this owner's stack: Maestro flows in `.maestro/`, run by EAS Workflows on pull requests. Evidence: moderate (Expo docs recommend Maestro via EAS Workflows; Maestro docs).

## 8. Why mobile E2E is flaky, and the fix for each cause

Data: in 83 flaky mobile UI tests studied by Romano et al. (ICSE 2021), async wait caused 32.5% (resource rendering, animation timing, network loading), platform issues 21.7%, incorrect test runner interaction 16.9%, incorrect resource load order 13.3%, test order dependency 7.2%. In Android app commits studied by Thorve et al. (ICSME 2018), concurrency caused 36% of flakiness, dependency on OS, hardware or third party libraries 22%, program logic 12%, network 8%, UI design 8%. Evidence: strong (two peer reviewed empirical studies, small samples).

| Cause | Symptom | Fix |
|---|---|---|
| Acting before the screen is ready | Tap lands on nothing, element "not found" | Wait on a condition (`assertVisible`, `enabled: true`, Detox sync), never a sleep |
| Animations | Tap on a moving element, screenshot mid transition | Disable animations on CI emulators (window, transition, animator scales to 0; android-emulator-runner does this by default), `waitForAnimationToEnd` |
| Emulator not fully booted | First flow fails, later ones pass | Wait for `sys.boot_completed` (`adb wait-for-device shell 'while [ -z "$(getprop sys.boot_completed)" ]; do sleep 1; done'`) before tests |
| System dialogs | "App isn't responding", Play services update, notification permission prompt cover the app | Set permissions in `launchApp`, use a `google_apis` image without Play Store on CI, give the emulator enough RAM and CPU |
| Shared backend state | Passes alone, fails in the suite | Each flow creates its own user and data; never share accounts between parallel shards |
| Test order dependency | Fails when run alone or shuffled | `clearState: true` per flow; no flow relies on another |
| Network | Timeouts on CI | Point E2E builds at a local or staging backend you control; stub third party services at your backend |
| OS and device differences | Fails only on one API level or screen size | Pin the CI image and device profile; add a second profile on purpose, not by accident |
| Keyboard covering the next field | Tap on hidden field fails | `hideKeyboard` before tapping below the fold; `scrollUntilVisible` |
| Debug build | Red box, Metro reload, slow JS | Test a release or `e2e-test` profile build |
| Long lists | Element not rendered yet (virtualized) | `scrollUntilVisible` with a selector |
| Locale, time, time zone | Date text differs between machines | Fix locale and time zone on the CI device, assert with regex |

A flow that passes only on retry is flaky. Retries in CI (`retries: 1` in EAS, `retry` in Maestro) hide flakes; allow at most one, track every flow that needed it, and fix or delete it within two weeks (flaky policy in kwx-developer `testing-strategy.md` section 11).

## 9. Running E2E in CI

### 9.1 EAS Workflows (Expo default)

From the Expo docs (the Maestro job is marked alpha there):

```json
// eas.json
{
  "build": {
    "e2e-test": {
      "withoutCredentials": true,
      "ios": { "simulator": true },
      "android": { "buildType": "apk" }
    }
  }
}
```

```yaml
# .eas/workflows/e2e-test-android.yml
name: e2e-test-android
on:
  pull_request:
    branches: ['*']
jobs:
  build_android_for_e2e:
    type: build
    params:
      platform: android
      profile: e2e-test
  maestro_test:
    needs: [build_android_for_e2e]
    type: maestro
    runs_on: linux-large-nested-virtualization
    params:
      build_id: ${{ needs.build_android_for_e2e.outputs.build_id }}
      flow_path: ['.maestro/']
      include_tags: ['core']
      retries: 1
      record_screen: true
```

Other `maestro` job params: `shards`, `exclude_tags`, `android_system_image_package`, `device_identifier`, `skip_build_check`; hooks `before_maestro_tests` and `after_maestro_tests`. A `maestro-cloud` job type sends the same build to Maestro Cloud instead.

### 9.2 GitHub Actions with an emulator

From the `reactivecircus/android-emulator-runner` README (not run here):

```yaml
jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Enable KVM
        run: |
          echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' | sudo tee /etc/udev/rules.d/99-kvm4all.rules
          sudo udevadm control --reload-rules
          sudo udevadm trigger --name-match=kvm
      - run: curl -fsSL "https://get.maestro.mobile.dev" | bash
      - run: ./gradlew :app:assembleRelease   # or download the EAS build artifact
      - uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 35
          arch: x86_64
          target: google_apis
          profile: pixel_7
          disable-animations: true
          script: |
            adb install app/build/outputs/apk/release/app-release.apk
            $HOME/.maestro/bin/maestro test --format junit --output maestro-report.xml .maestro/
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: maestro-report
          path: |
            maestro-report.xml
            ~/.maestro/tests/
```

Notes: Ubuntu runners are faster and cheaper than macOS ones for Android (README). Cache `~/.android/avd/*` keyed by API level to skip the cold boot. iOS simulators need a macOS runner. On CI, downloading system images is normal; this does not conflict with a local "never download images" rule.

### 9.3 Local, with the user's yes

```sh
adb devices                          # read only: confirm exactly one device and its serial
ANDROID_SERIAL=emulator-5554 maestro test --include-tags core .maestro/
```

Pin the serial so Maestro cannot pick a different device. Restore anything the flows changed (airplane mode, permissions, dark mode) if a flow failed half way.

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| No local run without a yes | Local E2E ran only after explicit approval in this conversation, or not at all | Review your commands and the conversation |
| Flows cover journeys, not edge cases | 5 to 15 flows, each named after a journey | `ls .maestro` |
| Each flow starts clean | `clearState: true` or equivalent at the top of each flow | `rg --files-without-match clearState .maestro/*.yml` lists none (subflows excepted) |
| Permissions explicit | `launchApp` sets `permissions` | `rg -n "permissions:" .maestro` |
| No fixed waits | No sleep like commands, no 60 s timeouts as a habit | `rg -n "timeout: [6-9][0-9]{4}" .maestro` reviewed |
| Selectors stable | `id` for icons and localized text; text for user visible labels | Read the flows |
| Release like build | CI tests an `e2e-test` or release profile, not a debug build | Read `eas.json` and the workflow |
| CI runs flows | Workflow on pull requests with JUnit report and recordings uploaded | Read `.eas/workflows/` or `.github/workflows/` |
| Retries bounded | At most 1 retry, flaky flows tracked | Read workflow params and the issue list |
| Detox configs reuse the existing device | No AVD creation, named AVD equals the user's | Read `.detoxrc.js` |
