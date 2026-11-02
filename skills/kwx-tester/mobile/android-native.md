# Android native: Kotlin and Compose tests

How to test a native Android app written in Kotlin with Jetpack Compose: what runs on the local JVM (most of it), Robolectric, Compose UI tests and the semantics tree, Espresso and UI Automator, screenshot tests (Roborazzi, Paparazzi, Compose Preview Screenshot Testing), Macrobenchmark and baseline profiles, WorkManager, Room migrations, Hilt, and coroutines with `runTest` and Turbine. The reference architecture is Google's Now in Android app (github.com/android/nowinandroid). Commands are from the Android docs or project READMEs unless marked verified; none of the Gradle commands here were run for this file.

## Contents

1. Where tests live and what needs a device
2. Test doubles: fakes over mocks
3. Coroutines and Flow
4. Robolectric
5. Compose UI tests
6. Espresso and UI Automator
7. Screenshot tests
8. Hilt
9. Room migrations
10. WorkManager
11. Macrobenchmark and baseline profiles
12. Gradle tasks and the user's device rules
13. Checks

## 1. Where tests live and what needs a device

| Source set | Runs on | Put here | Command |
|---|---|---|---|
| `src/test` | Local JVM, no device | View models, repositories, use cases, mappers, Compose UI tests under Robolectric, Roborazzi or Paparazzi screenshots | `./gradlew testDebugUnitTest` (per variant, for example `testDemoDebug`) |
| `src/screenshotTest` | Host, Layoutlib | Compose Preview screenshot tests | See section 7 |
| `src/androidTest` | Emulator or phone | Compose UI tests that need real rendering, Espresso, UI Automator, Room migration tests, WorkManager integration | `./gradlew connectedDebugAndroidTest` |
| `:benchmark` or `:baselineprofile` module (`com.android.test`) | Real phone | Macrobenchmark, baseline profile generation | `./gradlew :benchmark:connectedCheck` |

Android's "What to test" guide: unit tests for view models, the data layer (especially repositories), domain use cases and utilities; screen UI tests for critical interactions on each screen ("one test class per screen is a good starting point"); a few navigation or user flow tests; do not unit test activities, fragments or services, which should hold no logic. Edge cases it lists for unit tests: negative and boundary numbers, every network error, malformed JSON, full storage, objects recreated on rotation. Evidence: moderate (official guide).

Now in Android note: run variant tasks (`testDemoDebug`, `connectedDemoDebugAndroidTest`), not the global `./gradlew test` or `connectedAndroidTest`, which run every variant (NiA README).

## 2. Test doubles: fakes over mocks

Now in Android "does not use any mocking libraries." Each dependency has an interface; tests use a test double that implements it (`TestUserDataRepository`, `TestNewsRepository`) and keeps state in memory, often backed by a `MutableSharedFlow` the test can push into. Production modules are replaced with Hilt test modules. The README's reason: "less brittle tests that may exercise more production code."

```kotlin
class TestNotesRepository : NotesRepository {
    private val notes = MutableStateFlow<List<Note>>(emptyList())
    override fun observeNotes(): Flow<List<Note>> = notes
    override suspend fun save(note: Note) { notes.update { it + note } }
    fun sendNotes(list: List<Note>) { notes.value = list }   // test only control
}
```

Use MockK or Mockito only at boundaries you do not own and cannot fake simply (a platform service, a vendor SDK). Evidence: moderate (Now in Android; Software Engineering at Google ch. 13, cited in kwx-developer).

## 3. Coroutines and Flow

From the Android coroutine testing guide (kotlinx-coroutines-test 1.6+ APIs):

- One `runTest` per test, as an expression body. `runTest` skips `delay` with virtual time and fails if the test runs longer than its timeout (60 s by default for waiting on child coroutines, per the guide).
- `runTest` uses `StandardTestDispatcher`: new coroutines are queued until the test yields. Call `advanceUntilIdle()`, `advanceTimeBy(ms)` or `runCurrent()`. `UnconfinedTestDispatcher` runs new coroutines eagerly; fine for simple tests and for collecting Flows.
- Inject dispatchers into classes (`class Repo(private val io: CoroutineDispatcher)`); never hard code `Dispatchers.IO`. In tests pass `StandardTestDispatcher(testScheduler)`. All test dispatchers in one test must share one scheduler.
- Replace `Dispatchers.Main` in local tests with a rule; do not replace it in instrumented tests.

```kotlin
class MainDispatcherRule(
    val testDispatcher: TestDispatcher = UnconfinedTestDispatcher(),
) : TestWatcher() {
    override fun starting(description: Description) = Dispatchers.setMain(testDispatcher)
    override fun finished(description: Description) = Dispatchers.resetMain()
}

class NotesViewModelTest {
    @get:Rule val mainDispatcherRule = MainDispatcherRule()
    private val repo = TestNotesRepository()

    @Test
    fun `shows notes from the repository`() = runTest {
        val vm = NotesViewModel(repo)
        val states = mutableListOf<NotesUiState>()
        backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) { vm.uiState.toList(states) }
        repo.sendNotes(listOf(Note("1", "Shopping")))
        assertEquals(NotesUiState.Success(listOf(Note("1", "Shopping"))), states.last())
    }
}
```

`backgroundScope` cancels the collector when the test ends. For `stateIn(..., WhileSubscribed(5_000), ...)` flows there must be a collector, or the state never updates.

**Turbine** (`app.cash.turbine:turbine`) makes Flow assertions short and strict:

```kotlin
@Test
fun `save emits Saving then Saved`() = runTest {
    val vm = EditViewModel(repo)
    vm.events.test {
        vm.save("Shopping")
        assertEquals(EditEvent.Saving, awaitItem())
        assertEquals(EditEvent.Saved, awaitItem())
        cancelAndIgnoreRemainingEvents()
    }
}
```

Turbine fails if an unexpected item is left unconsumed at the end, which catches extra emissions. Evidence: moderate (Android guide; Turbine README).

## 4. Robolectric

Robolectric runs Android framework code on the JVM: you can launch an Activity, drive its lifecycle, recreate it, and run Compose UI tests and Espresso view tests without a device.

```kotlin
android {
    testOptions { unitTests { isIncludeAndroidResources = true } }
}
dependencies {
    testImplementation("org.robolectric:robolectric:4.13")   // use the current release
    testImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
```

```kotlin
@RunWith(AndroidJUnit4::class)
class AddContactActivityTest {
    @Test
    fun inputTextIsKeptAfterRecreation() {
        val scenario = ActivityScenario.launch(AddContactActivity::class.java)
        onView(withId(R.id.contact_name_text)).perform(typeText("Test User"))
        scenario.recreate()   // configuration change, as on rotation
        onView(withId(R.id.contact_name_text)).check(matches(withText("Test User")))
    }
}
```

What the Android docs say about limits: Robolectric "is not a complete replacement for an emulator"; it has no real screen, some APIs are partial, and you still need a device for system UI such as edge to edge, picture in picture, and for `WebView`. Use it for behavior tests and for screenshots where pixel accuracy is not critical. Pin the SDK per test with `@Config(sdk = [35])` when behavior differs per API level.

When the user's rules restrict the emulator, Robolectric is how you still run screen tests. Most `androidTest` Compose tests can move to `src/test` unchanged.

## 5. Compose UI tests

### 5.1 The rule: use the v2 APIs

Compose UI test 1.11 added v2 test rules that use `StandardTestDispatcher`, like production, instead of the old eager `UnconfinedTestDispatcher` that "could inadvertently mask real timing issues or race conditions." The v1 rules are deprecated. Change the import only:

```kotlin
import androidx.compose.ui.test.junit4.v2.createComposeRule          // was ...junit4.createComposeRule
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.compose.ui.test.v2.runComposeUiTest
```

If a test now fails because a coroutine has not run yet, wait for idle instead of reverting:

```kotlin
viewModel.loadData()
composeTestRule.waitForIdle()                       // or runOnIdle { ... }
assertEquals(Success, viewModel.state.value)
```

Do not combine `createComposeRule` with `runTest`: that makes two clocks. Use `runComposeUiTest { ... }`, which runs inside its own `runTest` with one clock. v2 rules also force touch input mode at the start of each test; pass `ComposeUiTestConfig(inputMode = InputMode.Keyboard)` for focus tests (Compose 1.13+). Evidence: moderate (Android docs, "Test configuration and execution (v2)").

### 5.2 A screen test

```kotlin
class NotesScreenTest {
    @get:Rule val composeTestRule = createComposeRule()

    @Test
    fun emptyState_showsHintAndAddButton() {
        composeTestRule.setContent {
            AppTheme { NotesScreen(uiState = NotesUiState.Success(emptyList()), onAdd = {}) }
        }
        composeTestRule.onNodeWithText("No notes yet").assertIsDisplayed()
        composeTestRule.onNodeWithContentDescription("Add note").assertIsEnabled().assertHasClickAction()
    }

    @Test
    fun pressingAdd_callsOnAdd() {
        var added = false
        composeTestRule.setContent { NotesScreen(uiState = NotesUiState.Success(emptyList()), onAdd = { added = true }) }
        composeTestRule.onNodeWithContentDescription("Add note").performClick()
        assertTrue(added)
    }
}
```

Test the stateless screen composable with a fake `uiState`. Test the view model separately on the JVM. Add one test with the real view model and Hilt for wiring.

### 5.3 Finders, assertions, actions

- Finders: `onNodeWithText`, `onNodeWithContentDescription`, `onNodeWithTag`, `onAllNodesWithText(...)[i]`, `onNode(hasText("Save") and hasClickAction())`, `onNodeWithText("x").onParent()`, `onChildren()`.
- Assertions: `assertIsDisplayed`, `assertExists`, `assertDoesNotExist`, `assertIsEnabled`, `assertIsNotEnabled`, `assertIsOn`, `assertIsSelected`, `assertTextEquals`, `assertContentDescriptionEquals`, `assert(SemanticsMatcher.expectValue(...))`, `assertCountEquals` on collections.
- Actions: `performClick`, `performTextInput`, `performTextReplacement`, `performImeAction`, `performScrollTo`, `performScrollToNode(hasText("Item 40"))`, `performTouchInput { swipeLeft() }`, `performSemanticsAction`.
- Waiting: `composeTestRule.waitUntil(timeoutMillis = 5_000) { onAllNodesWithText("Saved").fetchSemanticsNodes().isNotEmpty() }` or `waitUntilExactlyOneExists(hasText("Saved"))`. Control animations with `mainClock.autoAdvance = false` and `mainClock.advanceTimeBy(ms)`.

### 5.4 The semantics tree, merged and unmerged

Compose tests read the semantics tree, the same tree accessibility services use. Some composables (Button, ListItem, anything with `Modifier.semantics(mergeDescendants = true)` or `clickable`) merge their children into one node: a Button with an icon and the text "Like" is one node with text "Like". Finders search the merged tree by default.

- To reach a child inside a merged node: `onNodeWithTag("price", useUnmergedTree = true)`.
- To see what the test sees: `composeTestRule.onRoot().printToLog("TREE")` (or `onRoot(useUnmergedTree = true)`), then read Logcat or the test output.
- `Modifier.testTag("notes_list")` only when no text or content description identifies the node. For Maestro, UI Automator and Macrobenchmark to see tags as resource ids, set `Modifier.semantics { testTagsAsResourceId = true }` on the root.
- `clearAndSetSemantics { contentDescription = "Rating 4 of 5" }` replaces children's semantics; test that the combined description reads well.
- If a finder cannot find a visible element, the screen reader likely has a problem too. Fix semantics, then the test.

### 5.5 Accessibility checks in Compose tests

Compose 1.8 added automated accessibility checks. Add `androidx.compose.ui:ui-test-junit4-accessibility`, call `composeTestRule.enableAccessibilityChecks()` on an `AndroidComposeTestRule`, and every action then runs the Accessibility Test Framework checks (contrast, touch target size, labels, traversal order); call `tryPerformAccessibilityChecks()` to check without an action. Per the API reference it needs API 34+ and does not work on Robolectric, so it runs only in `androidTest`. Details in `mobile-accessibility-testing.md`.

## 6. Espresso and UI Automator

- **Espresso** drives View based UI inside your app process and syncs with the main thread and registered idling resources. Use it for legacy View screens and for interop (a Compose screen inside a Fragment). `onView(withId(R.id.save)).perform(click())`, `check(matches(isDisplayed()))`. Register an `IdlingResource` for background work Espresso cannot see, or better, inject a test dispatcher.
- **UI Automator** drives the whole device: other apps, system dialogs, notifications, Settings. Use it for permission dialogs and notification taps that leave your app, and inside Macrobenchmark. Newer versions have a Kotlin DSL (`uiAutomator { startApp(pkg) }`, seen in the current Macrobenchmark docs).
- Disable animations on test devices (developer options: window, transition and animator scale to 0). Espresso's own guidance; Romano et al. found delay fixes less common on Android than on web partly because Espresso recommends this.
- Both inject input on the device. Under the user's device rules they count as tier 3 (see `mobile.md`).

## 7. Screenshot tests

Android's guide: screenshot testing "is the recommended way to verify visual attributes in Compose UIs." One screenshot replaces many assertions and catches layout regressions across sizes, but references are cumbersome, Linux, macOS and Windows render slightly differently, and the tests are slower. So: choose screenshots that give unique feedback (not every theme times every font size), keep references in git or Git LFS, and record and verify on one platform (CI on Linux).

| Tool | Runs on | Engine | Record / verify | Notes |
|---|---|---|---|---|
| **Roborazzi** | JVM (`src/test`) | Robolectric Native Graphics | `./gradlew recordRoborazziDebug` / `verifyRoborazziDebug` (also `compareRoborazziDebug`) | Full Robolectric power: interactions before capture, Hilt, navigation. Used by Now in Android. Needs `@GraphicsMode(GraphicsMode.Mode.NATIVE)` |
| **Paparazzi** (Cash App) | JVM | Layoutlib | `./gradlew recordPaparazziDebug` / `verifyPaparazziDebug` | Static components, fast, no emulator. 2.0 is still alpha. Compose code that checks `LocalInspectionMode` needs a wrapper |
| **Compose Preview Screenshot Testing** (Google) | Host | Layoutlib | Test suites: `./gradlew update{Suite}{Target}{Variant}TestSuite` / `test{Suite}{Target}{Variant}TestSuite` | Turns `@PreviewTest @Preview` composables into tests in `src/screenshotTest`. Experimental; the standalone `com.android.compose.screenshot` plugin is deprecated in favour of AGP test suites (AGP 9.5.0-alpha03+) |

Roborazzi example:

```kotlin
@RunWith(AndroidJUnit4::class)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@Config(qualifiers = "w360dp-h640dp-xhdpi")
class NoteCardScreenshotTest {
    @get:Rule val composeTestRule = createAndroidComposeRule<ComponentActivity>()

    @Test
    fun noteCard_longTitle_darkTheme() {
        composeTestRule.setContent { AppTheme(darkTheme = true) { NoteCard(Note("1", "A very long title that must wrap to two lines")) } }
        composeTestRule.onRoot().captureRoboImage()
    }
}
```

Pick screenshots for risk: the longest realistic text, font scale 2.0 (wrap the content in `CompositionLocalProvider(LocalDensity provides Density(LocalDensity.current.density, fontScale = 2f))`, or call Robolectric's `RuntimeEnvironment.setFontScale(2f)` before `setContent`), dark theme, a small (360 dp) and a large (840 dp) width, RTL. Never re-record all references to make CI green; review each diff image.

## 8. Hilt

From the Android Hilt testing guide:

```kotlin
dependencies {
    testImplementation("com.google.dagger:hilt-android-testing:<hilt>")
    kspTest("com.google.dagger:hilt-android-compiler:<hilt>")
    androidTestImplementation("com.google.dagger:hilt-android-testing:<hilt>")
    kspAndroidTest("com.google.dagger:hilt-android-compiler:<hilt>")
}
```

- Annotate the test with `@HiltAndroidTest`; declare `@get:Rule(order = 0) val hiltRule = HiltAndroidRule(this)` before the Compose rule (`order = 1`).
- Instrumented: a custom `AndroidJUnitRunner` whose `newApplication` returns `HiltTestApplication`, set as `testInstrumentationRunner`. Robolectric: `@Config(application = HiltTestApplication::class)` or `application = dagger.hilt.android.testing.HiltTestApplication` in `robolectric.properties`.
- Replace a binding for all tests in a source set with a `@TestInstallIn(components = [SingletonComponent::class], replaces = [NotesModule::class])` module that binds the fake. Prefer this: `@UninstallModules` plus `@BindValue` builds a new component per test class and "can significantly impact unit test build times."
- If you use `hiltViewModel()` from `hilt-navigation-compose`, add its annotation processors to test dependencies too.

## 9. Room migrations

A missing or wrong migration crashes the app on launch for every user who upgrades, or (with destructive fallback) deletes their data. Test every step and the full chain.

1. Export schemas and commit them. Room 2.x: Gradle plugin `androidx.room` with `room { schemaDirectory("$projectDir/schemas") }`. Room 3 (current docs): plugin `androidx.room3`, extension `room3 { schemaDirectory(...) }`, artifact `androidx.room3:room3-testing`. Auto migrations need the exported schemas of both versions.
2. A test per migration that inserts realistic old data with raw SQL (DAOs expect the newest schema), runs the migration, and checks the data, not only the schema:

```kotlin
@RunWith(AndroidJUnit4::class)
class MigrationTest {
    private val instrumentation = InstrumentationRegistry.getInstrumentation()

    @get:Rule
    val helper = MigrationTestHelper(
        instrumentation = instrumentation,
        databaseClass = AppDatabase::class,
        driver = AndroidSQLiteDriver(),
        file = instrumentation.targetContext.getDatabasePath("migration-test"),
    )

    @Test
    fun migrate1To2_keepsNotesAndFillsNewColumn() = runTest {
        helper.createDatabase(1).apply {
            execSQL("INSERT INTO Note (id, title) VALUES (1, 'Shopping')")
            close()
        }
        val db = helper.runMigrationsAndValidate(2, listOf(MIGRATION_1_2))
        db.prepare("SELECT title, pinned FROM Note WHERE id = 1").use {
            assertTrue(it.step())
            assertEquals("Shopping", it.getText(0))
            assertEquals(0L, it.getLong(1))
        }
        db.close()
    }
}
```

(The snippet follows the Room 3 docs; Room 2.x uses `MigrationTestHelper(InstrumentationRegistry.getInstrumentation(), AppDatabase::class.java)` and `SupportSQLiteDatabase`.)

3. A test that creates version 1, then opens the latest database through `Room.databaseBuilder(...).addMigrations(*ALL_MIGRATIONS).build()`, so Room validates the whole chain.
4. Grep for `fallbackToDestructiveMigration()`. It "permanently deletes all data" when a path is missing. Allow it only by explicit decision; prefer `fallbackToDestructiveMigrationFrom(versions)` for known broken old versions.

Migration tests are instrumented in the docs (`androidTest`), so they need a device. Under strict device rules, write them, run what you can on the JVM, and hand the `connected...AndroidTest` command to the user or CI.

## 10. WorkManager

- **Unit test the worker** with `TestListenableWorkerBuilder<SyncWorker>(context).setInputData(...).build()` and `worker.doWork()`; it does not need WorkManager initialized. The docs strongly recommend it for `CoroutineWorker`, because `work-testing` otherwise runs on `Dispatchers.Default`, not your worker's dispatcher. Runs under Robolectric on the JVM.
- **Integration test** (`androidx.work:work-testing`): `WorkManagerTestInitHelper.initializeTestWorkManager(context, Configuration.Builder().setExecutor(SynchronousExecutor()).build())`, enqueue, then use the `TestDriver` to pretend time and conditions passed: `setAllConstraintsMet(id)`, `setInitialDelayMet(id)`, `setPeriodDelayMet(id)`. Assert `WorkInfo.State` and output data.
- Test the cases users hit: constraints never met (offline for days), retry with backoff after `Result.retry()`, unique work policy (`KEEP` vs `REPLACE`) when the user triggers sync twice, work surviving a reboot. Real Doze behavior needs a device (`mobile-edge-cases.md`).

## 11. Macrobenchmark and baseline profiles

- Macrobenchmark measures startup, scrolling and animations of a release like build from a separate `com.android.test` module. The target build type (`benchmark`, `initWith(release)`, debug signing) must be non debuggable and `profileable`.
- `StartupTimingMetric()` with `StartupMode.COLD`, `WARM` or `HOT`; `FrameTimingMetric()` for jank while scrolling. Set `iterations` (5 to 10) and compare medians and P90 between builds, not single runs.
- Google discourages emulators: they "don't produce performance numbers representative of the end-user experience," and Macrobenchmark returns errors on an emulator or a low battery device unless you suppress them. Numbers come from a real phone, ideally a mid range one.
- Baseline profiles (generated with `BaselineProfileRule` and the `androidx.baselineprofile` Gradle plugin) precompile the startup path. Regenerate when startup code changes (NiA README). Now in Android generates them on an AOSP emulator, which is fine for profile generation but not for timing.
- Every Macrobenchmark and profile generation run starts and drives the app: tier 3 under the user's device rules. Write the benchmark, ask before running, or leave it to the user or a device farm.

## 12. Gradle tasks and the user's device rules

| Task | Tier (see `mobile.md`) |
|---|---|
| `testDebugUnitTest`, `testDemoDebug`, `verifyRoborazzi*`, `verifyPaparazzi*`, screenshot test suites, `lint` | 0: run freely |
| `connected*AndroidTest`, `:benchmark:connectedCheck`, baseline profile generation | 3: drives the device; needs the user's yes |
| Any task using Gradle Managed Devices (`testOptions.managedDevices`, tasks like `pixel6Api34DebugAndroidTest`) | Downloads system images and creates its own AVDs. Never run locally under a "one emulator, no downloads" rule. Fine on CI |

## 13. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| JVM suite green | `./gradlew testDebugUnitTest` (or the project's variant) passes | Run it, paste the summary |
| Logic in local tests | View models, repositories, use cases tested in `src/test` | `fd -e kt . app/src/test` lists them |
| Fakes over mocks | Mocking libraries only at boundaries you do not own | `rg -n "mockk|Mockito" app/src/test` and review each |
| Dispatchers injected | No hard coded `Dispatchers.IO` in classes under test | `rg -n "Dispatchers\.(IO|Default)" app/src/main` reviewed |
| One scheduler per test | Test dispatchers built from `testScheduler` | Read tests |
| v2 Compose rules | No deprecated v1 imports | `rg -n "compose\.ui\.test\.junit4\.createComposeRule|compose\.ui\.test\.runComposeUiTest" app/src` returns nothing |
| No `createComposeRule` plus `runTest` | Use `runComposeUiTest` instead | `rg -n "runTest" ` in Compose test files reviewed |
| Semantics first | `testTag` only where no text or description exists | `rg -c "onNodeWithTag"` vs `rg -c "onNodeWithText|onNodeWithContentDescription"` |
| Screenshot references reviewed | Changed `.png` files in the diff each explained | `git diff --stat -- '*.png'` |
| Room schemas committed and migrations tested | `schemas/` in git, one test per version step and one chain test | `git ls-files schemas`; `rg -n "runMigrationsAndValidate" app/src` |
| No silent data loss | No bare `fallbackToDestructiveMigration()` | `rg -n "fallbackToDestructiveMigration\(\)" app/src/main` |
| Hilt fakes via `@TestInstallIn` | `@UninstallModules` used only where one test class needs a special binding | `rg -c "UninstallModules|TestInstallIn" app/src` |
| Worker logic tested on the JVM | `TestListenableWorkerBuilder` tests exist for each worker | `rg -n "TestListenableWorkerBuilder" app/src/test` |
| No device task run without a yes | Only tier 0 tasks ran unless approved | Review commands |
