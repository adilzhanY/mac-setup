# Devices, emulators and adb

Which devices and OS versions to test on, when an emulator is enough and when only a real phone will do, the read only diagnostics an agent can collect with adb without touching the screen, the commands that change device state, and the commands that count as driving the device. It also holds the generic rule for emulators: reuse the one the user already has, never create another or download a system image unless the user asks. All adb commands here are standard platform tools commands; only `adb version`, `adb devices -l` and `emulator -list-avds` were run for this file (no device was running).

## Contents

1. The emulator rule
2. Device and OS matrix by market share
3. Emulator, real device, or device farm
4. The three kinds of adb command
5. Read only diagnostics
6. Commands that change state (ask first)
7. Commands that drive the device (input injection)
8. Reading a crash or an ANR
9. Checks

## 1. The emulator rule

- Read the user's `CLAUDE.md` first. Many owners have one emulator and a full disk; each extra AVD costs 4 to 8 GB.
- Reuse the emulator the user has. Find it with `emulator -list-avds` (read only; it lists, it does not start). Use whatever project needs it, React Native, Expo, Kotlin, Flutter: the same AVD.
- Never create an AVD (`avdmanager create avd`), never download a system image (`sdkmanager "system-images;..."`), never use a project specific AVD name. If a project's scripts or Detox config name another AVD, change them to the user's AVD.
- Do not start the emulator yourself if the rules say so; ask the user. If one is running for another project, reuse it and pin your commands with `ANDROID_SERIAL=<serial>` (from `adb devices`).
- Gradle Managed Devices and some test runners download images and create AVDs on their own. Do not run them locally under this rule; run them on CI.
- Tests that need a different OS version, a 16 KB page size image, a foldable or a tablet go to CI, a device farm or Firebase Test Lab, not to a new local AVD.

## 2. Device and OS matrix by market share

Numbers as of 2026 (check the sources again before a release):

- Worldwide mobile OS share, StatCounter August 2026: Android about 67.5%, iOS about 32.5%. In the United States iOS leads (about 58% in June 2026); in North America about 60%. Know where the users are.
- Android versions, Google's figures for December 2025 (from Play devices): Android 15 19.3%, Android 14 17.2%, Android 13 13.9%, Android 11 13.7%, Android 16 7.5%. StatCounter (web traffic, July 2026): Android 16 about 25.5%, 15 about 17.2%, 13 about 14.8%, 14 about 13.1%, 12 about 10.1%. Old versions stay in use for years; Android 11 and 12 together are still about a fifth of devices.
- Android Studio's "New Project" wizard shows the cumulative share per API level; use it to pick `minSdk`.
- Play's target API rule (Play Console help): from August 31, 2026, new apps and updates must target Android 16 (API 36); existing apps must target at least API 35 to stay visible to new users on newer devices.

A small but sufficient matrix:

| Slot | Why | Example |
|---|---|---|
| Lowest supported OS (`minSdk`) | Missing APIs, old WebView, old permission model | Android 9 to 11 phone, iOS minimum target |
| Most used OS | Most of your users | Android 15 |
| Newest OS and your `targetSdk` | New behavior changes (edge to edge, predictive back, large screen rules) | Android 16, latest iOS |
| Small, cheap, slow phone | Layout on 360 dp width, slow CPU, low RAM, aggressive OEM battery saver | 2 to 3 GB RAM Samsung A or Xiaomi Redmi |
| Large phone | Long lists, one hand reach | Pixel Pro or Galaxy Ultra size |
| Tablet or foldable (if supported, and for Android 16 behavior on 600 dp+) | Orientation and resizability locks are ignored on large screens for apps targeting API 36 | Pixel Tablet, Galaxy Fold, or emulator profiles on CI |
| One OEM skin other than Pixel | Samsung One UI, Xiaomi HyperOS change notifications, background work and permissions | Any Samsung |

Cover the matrix across the whole test effort (unit tests run everywhere, the matrix applies to device runs, the pre-launch report and beta testers), not with every test on every device.

## 3. Emulator, real device, or device farm

| Question | Emulator | Real device | Farm / Test Lab |
|---|---|---|---|
| Functional E2E flows | Good, fast, resettable | Good | Good, many models in parallel |
| Performance numbers (startup, jank) | No. Google discourages emulators for Macrobenchmark and it returns errors there | Yes, a mid range phone | Yes, on physical devices |
| Camera, Bluetooth, NFC, sensors, biometrics with real hardware | Simulated at best | Yes | Some |
| OEM specific behavior (battery savers, notification quirks) | No (AOSP or Google images) | Yes | Some |
| Push notifications end to end | Google APIs images with Play services can receive FCM | Yes | Yes |
| Agent can run it | Only within the user's rules (often: not by itself) | Usually no | Yes, through CI, without touching the user's machine |

## 4. The three kinds of adb command

| Kind | Effect | Default under strict rules |
|---|---|---|
| Read only | Reads logs, state, the view tree | Allowed on a device that is already running |
| Changes state | Installs, launches, toggles settings, kills or clears the app; no touch input | Ask first, say what you will change and how you will restore it, restore afterwards |
| Drives the device | Taps, swipes, types, random events, or runs a test framework that does | Never `input` or `monkey` if the rules forbid input injection; a test framework run only after an explicit yes for that run |

Always pin the device: `adb -s emulator-5554 ...` or `ANDROID_SERIAL=emulator-5554`, so a command never lands on the user's phone by accident.

## 5. Read only diagnostics

```sh
adb devices -l                                        # which devices, which serial
adb shell getprop ro.build.version.sdk                # API level
adb shell getprop ro.product.model
adb shell pm list packages | grep example             # is the app installed
adb shell dumpsys package com.example.notes | grep -E "versionName|versionCode|targetSdk"
adb shell dumpsys package com.example.notes | grep -A20 "runtime permissions"   # granted or not
adb shell pidof com.example.notes                     # running? which pid
```

Logs:

```sh
adb logcat -d -v time --pid=$(adb shell pidof -s com.example.notes)   # dump this app's log and exit
adb logcat -d -b crash                                # crash buffer only
adb logcat -d '*:E'                                   # errors from everything
adb logcat -d ReactNativeJS:V ReactNative:V '*:S'     # React Native JS console and native RN tags
adb logcat -d AndroidRuntime:E '*:S'                  # Java/Kotlin uncaught exceptions
adb logcat -d StrictMode:D '*:S'                      # StrictMode violations (if enabled in debug builds)
```

Use `-d` (dump and exit) so the command ends. `adb logcat -c` clears the buffer: that is a state change, but harmless; say so when you do it.

App and system state:

```sh
adb shell dumpsys activity activities | grep -E "topResumedActivity|mResumedActivity"   # what is on screen
adb shell dumpsys activity processes | grep -A2 com.example.notes                      # process state
adb shell dumpsys meminfo com.example.notes           # PSS, Java heap, native heap, views, activities
adb shell dumpsys gfxinfo com.example.notes           # frames rendered, janky frames, percentiles
adb shell dumpsys gfxinfo com.example.notes framestats
adb shell dumpsys jobscheduler | grep -A5 com.example.notes   # WorkManager jobs and constraints
adb shell dumpsys alarm | grep -A3 com.example.notes
adb shell dumpsys deviceidle                          # Doze state
adb shell dumpsys notification --noredact | grep -A5 com.example.notes
adb shell pm get-app-links com.example.notes          # Android 12+: verified app link domains
adb shell uiautomator dump /sdcard/ui.xml && adb pull /sdcard/ui.xml   # the current view tree (writes one file on the device)
adb exec-out screencap -p > screen.png                # a screenshot
```

What to look for:

- `meminfo`: a count of `Activities` that grows each time you open and close a screen is a leak. Compare before and after.
- `gfxinfo`: "Janky frames" percentage and the 90th and 99th percentile frame times. Reset with `dumpsys gfxinfo <pkg> reset` (state change) before a scenario.
- StrictMode: enable in debug builds (`StrictMode.setThreadPolicy(...detectAll().penaltyLog())`) and read the `StrictMode` tag for disk or network on the main thread.

## 6. Commands that change state (ask first)

Use these to reproduce edge cases (`mobile-edge-cases.md`). Each one needs the user's yes under strict rules, and each has a restore command.

| Purpose | Command | Restore |
|---|---|---|
| Install a build | `adb install -r app-release.apk` | `adb uninstall` (loses data) |
| Deep link, cold or warm | `adb shell am start -W -a android.intent.action.VIEW -d "notes://note/42" com.example.notes` | Not needed |
| Process death (app in background) | `adb shell am kill com.example.notes` (only kills a background process) | Reopen from Recents |
| Full stop (not the same as process death: clears the task) | `adb shell am force-stop com.example.notes` | Launch again |
| Wipe app data | `adb shell pm clear com.example.notes` | None. Ask first, always |
| Grant or revoke a permission | `adb shell pm grant com.example.notes android.permission.CAMERA` / `pm revoke ...` (revoking kills the process, like a user doing it in Settings) | The opposite command |
| Font scale 200% | `adb shell settings put system font_scale 2.0` | `settings put system font_scale 1.0` |
| Display size | `adb shell wm density 560` | `adb shell wm density reset` |
| Screen size | `adb shell wm size 720x1280` | `adb shell wm size reset` |
| Dark mode | `adb shell cmd uimode night yes` | `cmd uimode night no` (or the user's previous value) |
| Wi-Fi or data off | `adb shell svc wifi disable`, `adb shell svc data disable` | `enable` |
| Airplane mode | `adb shell cmd connectivity airplane-mode enable` | `disable` |
| Slow network (emulator only) | `adb emu network speed edge`, `adb emu network delay gprs` | `adb emu network speed full`, `delay none` |
| Doze | `adb shell dumpsys battery unplug && adb shell dumpsys deviceidle force-idle` | `adb shell dumpsys deviceidle unforce && adb shell dumpsys battery reset` |
| App Standby bucket | `adb shell am set-standby-bucket com.example.notes rare` | `am set-standby-bucket com.example.notes active` |
| Memory pressure signal | `adb shell am send-trim-memory com.example.notes RUNNING_CRITICAL` | Not needed |
| Per app language (Android 13+) | `adb shell cmd locale set-app-locales com.example.notes --locales ar` | `--locales ""` (check `cmd locale help` on the device) |
| Animations off for E2E | `adb shell settings put global window_animation_scale 0` (also `transition_animation_scale`, `animator_duration_scale`) | Put back the previous values (read them first with `settings get`) |

Before changing a setting, read and record its current value (`adb shell settings get system font_scale`), and put that value back at the end, not a default.

Time zone and clock: on an emulator, the cleanest way is a boot option (`-timezone Europe/Berlin`), which means restarting the emulator: hand that to the user. On a device, change it in Settings by hand (user checklist).

## 7. Commands that drive the device (input injection)

These tap, swipe or type, or run something that does:

- `adb shell input tap|swipe|text|keyevent|draganddrop ...`
- `adb shell monkey -p com.example.notes ...` (random events)
- `adb shell am instrument ...` and every Gradle `connected*AndroidTest` task (Espresso, Compose on device, UI Automator)
- Maestro, Detox, Appium runs on a local device
- Macrobenchmark and baseline profile generation
- `adb shell uiautomator runtest`, scrcpy with input enabled

Under rules like "never inject input into an emulator or phone": never run `input` or `monkey` at all, and run the test frameworks only after the user says yes for that run. Otherwise write the test, push it to CI, or hand the exact command to the user. Check the rules every session; a yes for one run is not a yes for the next.

## 8. Reading a crash or an ANR

- Crash: `adb logcat -d -b crash` shows the last fatal exceptions with stack traces. For React Native, also `adb logcat -d ReactNativeJS:V '*:S'` for the JS error that came before a native crash.
- ANR: the system writes traces to `/data/anr/`, which is not readable without root on user builds. Use `adb bugreport bugreport.zip` (read only, large, takes a minute; it contains the ANR traces under `FS/data/anr/`), or `adb shell dumpsys dropbox --print data_app_anr` for recent ANR entries. In the app, `ActivityManager.getHistoricalProcessExitReasons()` (Android 11+) reports why the process died last time; log it at startup in debug builds.
- Play Console Android vitals and Firebase Crashlytics or Sentry show the same crashes and ANRs from real users with device and OS breakdown (`stores-and-device-farms.md`).
- A crash report from the user: ask for the app version, device model, Android version, and the steps. Reproduce first at the lowest level (a unit test with the same input) before touching the device.

## 9. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| User's rules read before any adb command | Yes | State it in the report |
| One device, pinned | Every device command used `-s` or `ANDROID_SERIAL` | Review commands |
| No AVD created, no image downloaded | None | No `avdmanager create`, no `sdkmanager "system-images...`, no Gradle Managed Device task locally |
| No input injection without approval | No `input`, no `monkey`; frameworks only after a yes | Review commands |
| State changes restored | Every changed setting set back to its recorded value | List of changes and restores in the report |
| Matrix chosen by data | Device and OS slots justified by share and risk | Matrix table in the test plan |
| Performance numbers from real hardware | No benchmark numbers quoted from an emulator | Read the report |
