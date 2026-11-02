# Mobile reading list

Every URL used for the `mobile/` folder, read on 2026-10-31, with one line on what it gave. Pages were read through a fetch tool that summarizes long pages, so exact quotes in the reference files come from code samples and short passages on the pages.

## React Native and Expo

- https://docs.expo.dev/develop/unit-testing/ : jest-expo install and config, test file naming, react-test-renderer deprecated, SDK 58 needs Jest 30, Expo prefers Maestro E2E over snapshots.
- https://docs.expo.dev/router/reference/testing/ : renderRouter forms, initialUrl, testRouter helpers, Router matchers, RNTL v14 requirement.
- https://oss.callstack.com/react-native-testing-library/ : RNTL v14 docs home (moved from callstack.github.io).
- https://oss.callstack.com/react-native-testing-library/docs/start/quick-start : install, `test-renderer` peer dependency, ESLint plugin, bundled LLM guidelines.
- https://oss.callstack.com/react-native-testing-library/docs/start/migration-v14 : every v13 to v14 breaking change and the codemods.
- https://oss.callstack.com/react-native-testing-library/docs/api/jest-matchers : the 18 built in matchers.
- https://oss.callstack.com/react-native-testing-library/docs/api/events/user-event : User Event methods, timing, advanceTimers.
- https://raw.githubusercontent.com/callstack/react-native-testing-library/main/docs/guides/llm-guidelines.md : query priority, async discipline, ARIA props.
- https://reactnative.dev/docs/testing-overview : test levels, "real objects better than mocks", component tests do not cover native code, snapshot caveats, E2E tools.
- https://docs.swmansion.com/react-native-reanimated/docs/guides/testing/ : Reanimated Jest resolver, setUpTests, toHaveAnimatedStyle, fake timers.
- https://docs.swmansion.com/react-native-worklets/docs/guides/testing/ : worklets mock and resolver options.
- https://docs.swmansion.com/react-native-gesture-handler/docs/guides/testing/ : jestSetup, fireGestureHandler, getByGestureTestId.
- Forum and community results on testing expo-sqlite in Jest (forums.expo.dev threads "Test SQLite with jest", "How do I mock expo-sqlite"; expo-sqlite-mock blog post): no official Node implementation, repository plus real SQLite approach.
- Local files in a fresh `create-expo-app` (SDK 58): `node_modules/jest-expo/jest-preset.js` (transformIgnorePatterns, passWithNoTests, tsconfig path mapping, platform presets), `react-native-screens/README.md`, the AsyncStorage and safe-area Jest mocks.

## E2E

- https://docs.maestro.dev/llms.txt : index of the Maestro docs.
- https://docs.maestro.dev/get-started/how-maestro-works.md : black box, device level input, driver app, Studio, Cloud.
- https://docs.maestro.dev/get-started/supported-platform/react-native.md : testID to id, Expo Go openLink, nested touchables on iOS.
- https://docs.maestro.dev/maestro-flows/flow-control-and-logic/how-to-use-selectors.md : selector types and best practices.
- https://docs.maestro.dev/maestro-flows/flow-control-and-logic/wait-commands.md : assertions as waits, extendedWaitUntil, waitForAnimationToEnd, retryTapIfNoChange.
- https://docs.maestro.dev/maestro-flows/flow-control-and-logic/permissions.md : permission names, allow, deny, unset, env driven values.
- https://docs.maestro.dev/reference/commands-available/launchapp.md : clearState, stopApp, permissions, launch arguments.
- https://docs.maestro.dev/reference/commands-available/assertscreenshot.md : threshold, cropOn.
- https://docs.maestro.dev/maestro-cli/how-to-install-maestro-cli.md : install command, Java 17.
- https://docs.maestro.dev/maestro-cli/maestro-cli-commands-and-options.md : `--format`, `--output`, `--include-tags`, `--test-output-dir`.
- https://docs.maestro.dev/maestro-flows/workspace-management/test-reports-and-artifacts.md : report formats and artifact folder.
- https://docs.expo.dev/eas/workflows/examples/e2e-tests/ : e2e-test build profile and Maestro workflow files.
- https://docs.expo.dev/eas/workflows/pre-packaged-jobs/ : maestro and maestro-cloud job parameters, nested virtualization runners.
- https://wix.github.io/Detox/docs/introduction/getting-started : Detox 20.x and the gray box idea.
- https://wix.github.io/Detox/docs/articles/how-detox-works : what Detox synchronizes on.
- Search results on Detox and Expo config plugins (npmjs.com/package/@config-plugins/detox, community fork notes): official plugin stopped around SDK 52, fork from SDK 54.
- https://github.com/ReactiveCircus/android-emulator-runner : GitHub Actions emulator, KVM step, inputs, AVD caching.

## Android native

- https://developer.android.com/training/testing/fundamentals/what-to-test : what to test per layer, edge cases.
- https://developer.android.com/develop/ui/compose/testing : rules, dependencies, basic finders and actions.
- https://developer.android.com/develop/ui/compose/testing/migrate-v2 : v2 test rules, StandardTestDispatcher, runComposeUiTest, ComposeUiTestConfig.
- https://developer.android.com/develop/ui/compose/testing/semantics : semantics tree basics.
- https://developer.android.com/training/testing/ui-tests/screenshot : screenshot testing guidance and trade offs.
- https://developer.android.com/studio/preview/compose-screenshot-testing-with-testsuites : Compose Preview Screenshot Testing on AGP test suites.
- https://github.com/takahirom/roborazzi : Roborazzi Gradle tasks, captureRoboImage, GraphicsMode NATIVE.
- https://github.com/cashapp/paparazzi : Paparazzi rule, tasks, Git LFS advice, 2.0 alpha status, limitations.
- https://github.com/android/nowinandroid : reference testing setup.
- https://developer.android.com/kotlin/coroutines/test : runTest, test dispatchers, MainDispatcherRule, backgroundScope.
- https://developer.android.com/training/data-storage/room/migrating-db-versions : schema export, MigrationTestHelper, testing all migrations, destructive fallback.
- https://developer.android.com/develop/background-work/background-tasks/testing/persistent/integration-testing : work-testing, TestDriver, TestListenableWorkerBuilder advice.
- https://developer.android.com/training/dependency-injection/hilt-testing : Hilt test setup and binding replacement.
- https://developer.android.com/topic/performance/benchmarking/macrobenchmark-overview : Macrobenchmark setup, emulator warning, commands.
- https://developer.android.com/training/testing/local-tests/robolectric : Robolectric uses and limits.
- https://developer.android.com/guide/topics/ui/accessibility/testing : manual and automated accessibility testing, Scanner, pre-launch report.
- Search results on Compose `enableAccessibilityChecks` (developer.android.com ComposeTestRule reference, Compose accessibility testing page, proandroiddev article): Compose 1.8, `ui-test-junit4-accessibility`, API 34+, not on Robolectric.
- Search results on Android 16 orientation and resizability changes (android-developers.googleblog.com, January 2025) and the Play target API requirement (developer.android.com/google/play/requirements/target-sdk, Play Console help 11926878).

## iOS

- https://github.com/swiftlang/swift-testing : Swift Testing scope, parallel by default, Swift 6 and Xcode 16, coexistence with XCTest.
- https://github.com/pointfreeco/swift-snapshot-testing : assertSnapshot, strategies, record modes, Swift Testing trait, same simulator rule.
- https://developer.apple.com/documentation/testing : page did not render through the fetch tool (JavaScript); Swift Testing facts taken from the GitHub README instead.
- Search results on TestFlight limits (developer.apple.com App Store Connect help "TestFlight overview", docs.expo.dev/submit/testflight): 100 internal, 10,000 external, 90 day expiry, Beta App Review.

## Stores, farms, market data

- https://support.google.com/googleplay/android-developer/answer/14151465 : 12 testers for 14 days for new personal accounts.
- https://support.google.com/googleplay/android-developer/answer/9842757 : pre-launch report.
- https://firebase.google.com/docs/test-lab/usage-quotas-pricing : Test Lab quotas and prices.
- Search results on Android vitals thresholds (developer.android.com/vitals, Android Developers blog October 2022): 1.09% crash, 0.47% ANR, 8% per phone model.
- Search results on AWS Device Farm pricing and BrowserStack Maestro support (devicelab.dev, stackshare and similar third party pages): treated as unverified, flagged in the file.
- Search results on StatCounter mobile OS share (gs.statcounter.com, June to August 2026) and Android version distribution (androidheadlines.com January 2026 citing Google's December 2025 numbers; gs.statcounter.com Android version share July 2026).

## Studies

- https://arxiv.org/abs/2103.02669 : Romano et al., UI based flaky tests (full PDF read).
- https://people.cs.vt.edu/nm8247/publications/empirical-study-flaky-pdf.pdf : Thorve et al., flaky tests in Android apps (full PDF read).

## Cited but not read

- Detox environment and project setup pages: not needed beyond the command shapes; Detox is not the default for this stack.
- Apple's Human Interface Guidelines page on hit targets (44 pt): known value, page not fetched this session.
- Turbine README (app.cash.turbine): API shape from common knowledge, not fetched; marked as moderate in the file.
- Firebase Test Lab gcloud reference: command shapes from common knowledge, model ids left as placeholders.
- MSW React Native integration page: not read; the file says MSW under jest-expo is unverified.
