# Android developer testing guides (collection)

- Authors: Google, developer.android.com
- Year: pages read 2026-10-31
- Legal URLs:
  - What to test: https://developer.android.com/training/testing/fundamentals/what-to-test
  - Compose testing: https://developer.android.com/develop/ui/compose/testing
  - Compose test v2 migration: https://developer.android.com/develop/ui/compose/testing/migrate-v2
  - Screenshot testing: https://developer.android.com/training/testing/ui-tests/screenshot
  - Compose Preview Screenshot Testing with test suites: https://developer.android.com/studio/preview/compose-screenshot-testing-with-testsuites
  - Robolectric: https://developer.android.com/training/testing/local-tests/robolectric
  - Coroutines testing: https://developer.android.com/kotlin/coroutines/test
  - Room migrations: https://developer.android.com/training/data-storage/room/migrating-db-versions
  - WorkManager integration testing: https://developer.android.com/develop/background-work/background-tasks/testing/persistent/integration-testing
  - Hilt testing: https://developer.android.com/training/dependency-injection/hilt-testing
  - Macrobenchmark: https://developer.android.com/topic/performance/benchmarking/macrobenchmark-overview
  - Accessibility testing: https://developer.android.com/guide/topics/ui/accessibility/testing

## What I read

Each page above in full (through a fetch tool that summarizes long pages, so some details were checked against code samples on the page).

## Key lessons used in mobile/android-native.md, mobile/mobile-accessibility-testing.md, mobile/mobile-edge-cases.md

- Unit tests for view models, repositories, use cases; one screen UI test class per screen; do not unit test activities and fragments. Edge cases named: network errors, malformed JSON, full storage, recreation on rotation.
- Compose test v2 rules (ui-test 1.11+) use StandardTestDispatcher; v1 deprecated because eager dispatch "could inadvertently mask real timing issues"; do not combine createComposeRule with runTest, use runComposeUiTest.
- Screenshot testing is "the recommended way to verify visual attributes in Compose UIs"; keep the count small, platforms render differently.
- Compose Preview Screenshot Testing moved to AGP test suites (AGP 9.5.0-alpha03+, experimental); the standalone plugin is deprecated.
- Robolectric is "not a complete replacement for an emulator"; good for behavior tests and low fidelity screenshots.
- runTest uses StandardTestDispatcher; one scheduler per test; MainDispatcherRule pattern; backgroundScope for collectors.
- Room 3 artifacts (androidx.room3) and MigrationTestHelper with a driver; test every migration and the full chain; destructive fallback deletes all data.
- WorkManager: TestListenableWorkerBuilder for CoroutineWorker; TestDriver for constraints and delays.
- Hilt: HiltAndroidRule first, prefer @TestInstallIn over @UninstallModules (build time).
- Macrobenchmark: emulators discouraged and errored; module and build type setup; StartupMode and CompilationMode.
