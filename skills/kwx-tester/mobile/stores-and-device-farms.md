# Stores and device farms

How to use the stores and hosted devices as part of testing: Google Play testing tracks, the pre-launch report, the rule that new personal developer accounts need 12 testers for 14 days before production, Firebase Test Lab, AWS Device Farm, BrowserStack, TestFlight, crash reporting as a test signal, and staged rollouts. These run on other people's devices, so they never conflict with a "do not drive my emulator" rule, and they cover the device matrix a solo developer does not own. Facts were checked on 2026-10-31 against Play Console Help, Firebase docs and Apple's App Store Connect help; prices and limits change, so recheck before you quote them to the user.

## Contents

1. Release pipeline as a test pipeline
2. Google Play testing tracks
3. The 12 testers for 14 days rule
4. Pre-launch report
5. Firebase Test Lab
6. Other device farms
7. TestFlight
8. Crash reporting as a test signal
9. Staged rollouts and Android vitals
10. Checks

## 1. Release pipeline as a test pipeline

```
local and CI tests  ->  internal track / TestFlight internal  ->  closed track (+ pre-launch report)
                    ->  open track or TestFlight external  ->  production at 1% -> 5% -> 20% -> 50% -> 100%
```

Each step has an exit condition written down before the build goes in: no new crash cluster in Sentry or Crashlytics, pre-launch report has no new stability errors, testers completed the "what to test" tasks, crash free sessions above the target. Evidence: moderate (Play Console help; common release practice).

## 2. Google Play testing tracks

| Track | Who | Use for |
|---|---|---|
| Internal testing | Up to 100 testers you list by email; builds reach them quickly, no full review wait | Every build you want to try on real phones; the owner's own devices |
| Closed testing | Email lists or Google Groups; can have several tracks | Friends and beta users; the 12 testers rule (section 3); pre-launch report |
| Open testing | Anyone can join from the store listing | Wider beta before production |
| Internal app sharing | Anyone with the link; no track, no review | Sending one test build to one person quickly |
| Production | Everyone, with staged rollout | Release |

Tips:

- Use the same signing and the same build type as production on testing tracks, so testers test what users will get.
- Write release notes for testers with 3 to 5 tasks and the edge cases you care about (from `mobile-edge-cases.md`): "Rotate while editing", "Use the app in airplane mode, then reconnect".
- Expo: `eas build -p android --profile production` then `eas submit -p android` (submit to the internal track first; set the track in `eas.json` `submit.production.android.track`).

## 3. The 12 testers for 14 days rule

Play Console Help (answer 14151465, checked 2026-10-31): developers with personal accounts created after November 13, 2023 must run a closed test with "a minimum of 12 testers who have been opted in continuously for at least 14 days" before they can apply for production access. A tester who opts out and back in restarts their 14 days. After the test, apply from the Dashboard; review usually takes up to 7 days, and Google can ask for more testing if testers were too few or not engaged. (News reports from December 2024 say the number was lowered from 20 to 12; the help page now states only 12.)

What this means for planning:

- Start the closed test at least 3 weeks before the planned launch.
- Recruit 15 or more testers, so one or two dropping out does not reset the clock below 12.
- Testers must actually use the app; give them tasks and ask for feedback through the Play "send feedback" link or a form. Google asks about engagement in the production access form.
- Organization accounts are not covered by the rule.

## 4. Pre-launch report

What Play Console Help says:

- When you upload an app bundle, Google installs it on real devices in its test lab (powered by Firebase Test Lab), launches it and crawls it for several minutes, typing, tapping and swiping. Devices run Android 9 or later and are chosen for ecosystem coverage (popularity, crash frequency, screen resolution); you cannot pick them. Phones, tablets, Wear OS and Chromebooks are included.
- Results usually arrive within an hour, in tabs for Stability (crashes, ANRs with stack traces), Performance, Accessibility (touch target size, low contrast, content labels, implementation), and Screenshots per device, plus a launch recommendation.
- Give it a dedicated test account in "Pre-launch report settings" so the crawler gets past sign in (automatic filling works only with standard Android widgets, not WebView sign in). Sign in with Google is handled automatically.
- Record a Robo script in Android Studio to drive the crawler through a key path first; add up to three deep links as extra starting points.
- Limits: no purchases, devices are in the US (geo restricted content shows US only), apps that block rooted devices are not supported, obfuscated stack traces unless you upload the mapping or symbol file.

How to use it: read every Stability and Accessibility item before promoting a build. Treat a crash on any device as a bug to reproduce with a test (`devices-emulators-and-adb.md` section 8). Look at the screenshots for clipped text on small screens and tablets: it is a free visual check across devices you do not own.

## 5. Firebase Test Lab

Runs Robo crawls and instrumented tests (Espresso, UI Automator, Compose on device) on virtual and physical devices in Google's data centers.

Quotas and prices (Firebase docs, checked 2026-10-31):

- Spark (free) plan: up to 15 test runs per day, 10 on virtual devices and 5 on physical devices.
- Blaze plan: each day 60 minutes on virtual and 30 minutes on physical devices free, then $1 per virtual device hour and $5 per physical device hour, billed per minute of test time.

Commands (gcloud CLI, from the Firebase docs; not run here):

```sh
gcloud firebase test android models list
gcloud firebase test android run --type robo \
  --app app-release.apk \
  --device model=<virtual-model-id>,version=34 \
  --device model=<physical-model-id>,version=33 \
  --timeout 5m
gcloud firebase test android run --type instrumentation \
  --app app-debug.apk --test app-debug-androidTest.apk \
  --device model=<model>,version=<api>
```

Use it to run the `androidTest` suite and a Robo crawl on 3 to 5 devices from your matrix in CI, without any local emulator. Results include video, logcat and performance graphs.

## 6. Other device farms

| Service | What it runs | Notes |
|---|---|---|
| Maestro Cloud | Maestro flows on hosted emulators and simulators | Paid plan; 20 minute soft limit per flow; integrates with EAS Workflows (`maestro-cloud` job) and GitHub Actions |
| AWS Device Farm | Appium, Espresso, XCUITest, fuzz tests on real devices | Pay per device minute (about $0.17 according to third party pricing pages in 2026; check the AWS pricing page) |
| BrowserStack App Automate / App Live | Automated tests on real devices; manual sessions in the browser | Supports Appium, Espresso, XCUITest, and Maestro according to secondary sources; check current docs |
| EAS Workflows | Maestro on Android emulators and iOS simulators | Simplest for Expo apps (`e2e-maestro-detox.md` section 9) |

Choose by what you already run: Maestro flows go to EAS or Maestro Cloud; Espresso goes to Firebase Test Lab; Appium suites go to AWS or BrowserStack. A manual session on a real device in BrowserStack App Live is a cheap way for the owner to check one bug on a device model he does not have.

## 7. TestFlight

From App Store Connect help and Expo docs:

- Internal testers: up to 100 App Store Connect users; the build is available right after processing.
- External testers: up to 10,000 per app, by email or public link; the first build of a version needs Beta App Review.
- Builds expire 90 days after upload.
- Testers send feedback with screenshots from the TestFlight app; crashes from TestFlight builds appear in App Store Connect and Xcode Organizer.
- Expo: `eas build -p ios --profile production` and `eas submit -p ios`, or `npx testflight`.

## 8. Crash reporting as a test signal

Crash and error reporting turns every beta tester into a test run.

- Install one: Sentry (`@sentry/react-native` with its Expo config plugin) or Firebase Crashlytics (`@react-native-firebase/crashlytics`, or the native SDK). One tool, not both.
- Upload source maps (JS) and mapping or symbol files (R8, dSYM) on every release build, or stack traces are useless. Check this in CI: a release without symbols is a failed release step.
- Tag every event with app version, build number, OTA update id (EAS Update), and environment. Do not attach personal data.
- Before promoting a build, compare it with the previous one: new issue groups, crash free sessions and users, ANR rate (Play), hangs (iOS). A new crash group in beta blocks promotion until it has a failing test and a fix.
- Test the reporting itself once per setup: a hidden debug action that throws, and confirm the event arrives with a readable stack trace.

## 9. Staged rollouts and Android vitals

- Play production releases can roll out to a percentage of users and be halted. Start at 1 to 5%, wait at least 24 hours with enough sessions, then increase. Halt on a new crash cluster; a halted release stops reaching new users, and a fix ships as a new version code.
- iOS phased release spreads automatic updates over 7 days (1%, 2%, 5%, 10%, 20%, 50%, 100%) and can be paused; users can still update manually.
- Android vitals bad behavior thresholds (Android developers site): user perceived crash rate 1.09% and user perceived ANR rate 0.47% overall, 8% for a single phone model. Above them, Play may lower the app's visibility and show a warning on the store listing. Use lower internal targets (for example crash free users above 99.5%).
- EAS Update has its own staged rollout (`eas update --rollout-percentage`, Expo docs) and rollback; treat an OTA update like a release, with the same exit conditions.

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Closed test planned for new personal accounts | 12 or more testers opted in for 14 continuous days before applying, with 15+ recruited | Play Console testers list and dates; ask the user |
| Pre-launch report read | Every Stability and Accessibility item triaged | Play Console, or ask the user to share the report |
| Tester instructions written | Each testing build has tasks and edge cases | Release notes text |
| Device matrix covered by farms | Each slot in the matrix has a farm run or a tester device | Matrix table with sources |
| Crash reporting works | Test event received with symbolicated stack | Sentry or Crashlytics event link |
| Symbols uploaded per release | Source maps and mapping files present | CI logs, Sentry release artifacts |
| Exit conditions written per stage | Numbers for crash free sessions, ANR, new issues | Release checklist |
| Rollout staged | Production starts below 100% with a halt plan | Play Console rollout percentage |
