# iOS: tests in short

The minimum an agent needs to test the iOS side of an app: XCTest, Swift Testing, XCUITest, snapshot tests with Point-Free's `swift-snapshot-testing`, simulator commands, and TestFlight. Most of the owner's apps are Expo apps built Android first, so the iOS binary is usually tested by the same Jest suite and Maestro flows (`react-native-expo.md`, `e2e-maestro-detox.md`) on a macOS runner in CI. Native Swift tests matter when the app has its own Swift code (an Expo module, a widget, a share extension). iOS tests need macOS and Xcode; on a Linux machine, write them and run them in CI.

## Contents

1. Which framework for what
2. Swift Testing
3. XCTest and XCUITest
4. Snapshot tests
5. Simulator commands and the user's device rules
6. Running in CI
7. TestFlight
8. Checks

## 1. Which framework for what

| Need | Use |
|---|---|
| Unit and integration tests of Swift code | Swift Testing (new code), XCTest (existing suites). Both can live in one target |
| UI tests that drive the app | XCUITest (Swift Testing does not cover UI tests) |
| Performance metrics in tests | XCTest `measure(metrics:)` |
| Visual regression of views | `swift-snapshot-testing` |
| Cross platform E2E with Android | Maestro |
| Real users before release | TestFlight |

## 2. Swift Testing

Ships with the Swift 6 toolchain and Xcode 16; tests run in parallel by default (swift-testing README).

```swift
import Testing
@testable import Notes

@Suite("Note title validation")
struct TitleValidationTests {
    @Test func rejectsEmptyTitle() {
        #expect(validateTitle("") == .empty)
    }

    @Test(arguments: ["a", String(repeating: "x", count: 200)])
    func acceptsBoundaryLengths(_ title: String) {
        #expect(validateTitle(title) == .valid)
    }

    @Test func parsesSavedNote() throws {
        let note = try #require(Note(json: #"{"id":"1","title":"Shopping"}"#))
        #expect(note.title == "Shopping")
    }
}
```

- `#expect` records a failure and continues; `#require` stops the test (use it to unwrap optionals). Both print the values of the expression on failure.
- Traits: `.tags(.network)`, `.disabled("reason, link to issue")`, `.timeLimit(.minutes(1))`, `.enabled(if: ...)`, `@Suite(.serialized)` for tests that share a resource.
- Parallel by default means shared mutable state (singletons, `UserDefaults.standard`, a shared database file) causes flakes. Give each test its own instance; use `.serialized` only as a last resort.
- Migration from XCTest: `XCTAssert*` to `#expect`, `XCTUnwrap` to `#require`, `setUp`/`tearDown` to `init`/`deinit` on a struct suite. Migrate file by file.

## 3. XCTest and XCUITest

XCUITest runs the app in a separate process and drives it through the accessibility layer, like Maestro.

```swift
final class CreateNoteUITests: XCTestCase {
    func testCreateNote() throws {
        let app = XCUIApplication()
        app.launchArguments = ["-uiTesting", "-resetData"]
        app.launch()

        app.buttons["Add note"].tap()
        let title = app.textFields["Title"]
        XCTAssertTrue(title.waitForExistence(timeout: 5))
        title.tap()
        title.typeText("Shopping")
        app.buttons["Save"].tap()

        XCTAssertTrue(app.staticTexts["Shopping"].waitForExistence(timeout: 5))
    }

    func testAccessibilityAudit() throws {
        let app = XCUIApplication()
        app.launch()
        try app.performAccessibilityAudit()   // Xcode 15+
    }
}
```

- Find elements by accessibility label or `accessibilityIdentifier` (React Native `testID` maps to the identifier). Wait with `waitForExistence(timeout:)` or `XCTNSPredicateExpectation`, never `sleep`.
- Pass launch arguments to reset state and point at a test backend; read them in the app with `ProcessInfo.processInfo.arguments`.
- Handle system alerts (permissions) with `addUIInterruptionMonitor`, or set permissions before launch with `simctl privacy` (section 5).
- `performAccessibilityAudit()` checks contrast, hit regions, labels, Dynamic Type clipping and more on the current screen.

## 4. Snapshot tests

`swift-snapshot-testing` (Point-Free, 1.12+):

```swift
import SnapshotTesting
import Testing
import SwiftUI

@MainActor
@Suite(.snapshots(record: .failed))
struct NoteCardSnapshotTests {
    @Test func longTitleWraps() {
        let view = NoteCard(note: .init(id: "1", title: "A very long title that must wrap"))
        assertSnapshot(of: UIHostingController(rootView: view), as: .image(on: .iPhoneSe))
    }
}
```

- First run records a reference and fails; commit the reference after looking at it.
- Strategies: `.image` and `.image(on: .iPhoneSe / .iPhoneX / .iPadMini)` for views and view controllers, `.recursiveDescription`, `.dump` for any value, `.json` for `Encodable`.
- Record mode: `record: .failed` re-records only failures; never `.all` across a suite to turn CI green.
- Compare on the same simulator model and OS that recorded the reference; rendering differs between simulators and Xcode versions. Pin both in CI.
- Snapshot the risky states: longest text, largest Dynamic Type size (`.image(traits: .init(preferredContentSizeCategory: .accessibilityExtraExtraExtraLarge))`), dark mode, RTL.

## 5. Simulator commands and the user's device rules

`xcrun simctl` controls simulators on macOS. Same tiers as Android (`mobile.md` section 2):

| Command | What | Tier |
|---|---|---|
| `xcrun simctl list devices booted` | List running simulators | 1, read only |
| `xcrun simctl spawn booted log stream --predicate 'process == "Notes"'` | Stream app logs | 1 |
| `xcrun simctl io booted screenshot shot.png` | Screenshot | 1 |
| `xcrun simctl openurl booted "notes://note/1"` | Deep link | 2, changes state |
| `xcrun simctl privacy booted grant photos com.example.notes` (also `revoke`, `reset`) | Set a permission | 2 |
| `xcrun simctl push booted com.example.notes payload.apns` | Simulated push notification | 2 |
| `xcrun simctl status_bar booted override --time 9:41` | Clean status bar for screenshots | 2 |
| `xcrun simctl boot`, `create`, `erase`, downloading runtimes in Xcode | Start, create or wipe simulators | Ask; under "reuse one device" rules do not create or download |
| `xcodebuild test` with a UI test target | Drives the app | 3 |

## 6. Running in CI

```sh
xcodebuild test \
  -scheme Notes \
  -destination 'platform=iOS Simulator,name=iPhone 16,OS=latest' \
  -resultBundlePath build/Tests.xcresult
```

For Expo apps, an EAS Workflows `maestro` job with an iOS simulator build (`ios.simulator: true` in the `e2e-test` profile) runs the same flows as Android (`e2e-maestro-detox.md`). GitHub Actions needs a `macos-*` runner for anything iOS.

## 7. TestFlight

- Internal testers: up to 100 App Store Connect users; a build is available to them right after processing.
- External testers: up to 10,000 per app, by email or public link; the first external build of a version goes through Beta App Review.
- Builds expire 90 days after upload.
- Expo: `eas build -p ios --profile production` then `eas submit -p ios`, or `npx testflight` (Expo docs).
- Give testers a "What to test" note with 3 to 5 concrete tasks and the edge cases you want checked (`mobile-edge-cases.md`), and read crash reports and feedback screenshots in App Store Connect before release. Details in `stores-and-device-farms.md`.

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Swift logic covered | Swift Testing or XCTest tests exist for native code | `fd -e swift . | rg -i test` |
| No sleeps in UI tests | Waits use `waitForExistence` or expectations | `rg -n "sleep\(" --glob '*Tests*.swift'` |
| Tests independent under parallel runs | No shared singletons or shared files without `.serialized` and a reason | Read suites |
| Accessibility audit in one UI test per main screen | `performAccessibilityAudit()` present | `rg -n performAccessibilityAudit` |
| Snapshot references pinned | CI uses the same simulator model and OS as the references | Read the CI destination string |
| Simulator actions followed the user's rules | No simulator created, erased or downloaded without a yes | Review commands |
| TestFlight build has tester instructions | "What to test" filled in | App Store Connect, or ask the user |
