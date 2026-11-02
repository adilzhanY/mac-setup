# Desktop app testing

How to test desktop applications: Qt/QML (including Quickshell shells), Electron, Tauri and, briefly, GTK, with the Linux specific problems that break them: Wayland, HiDPI scale factors, several monitors and fonts. The goal is that most tests run without a visible window, so an agent can run them without touching the user's screen, mouse or keyboard. Command line tools and terminal UIs have their own file, `cli-and-tui-testing.md`.

## Contents

1. Before you start: the user's rules
2. The rules that matter most
3. Qt and QML: Qt Quick Test
4. Quickshell and other QML shells
5. Electron
6. Tauri
7. GTK, briefly
8. Linux specifics: Wayland, HiDPI, multiple monitors, fonts
9. What stays manual
10. Files in this folder
11. Checks

## 1. Before you start: the user's rules

Read the user's CLAUDE.md (global and project) and follow it. Typical rules and what they mean here:

| If the rules say | Then |
|---|---|
| Never move the mouse or type for the user | never use `ydotool`, `wtype`, `xdotool` or compositor dispatch commands that move focus; send input only inside a test harness (QML `keyClick`, Playwright, WebDriver) to a window that is not on the user's screen |
| Browser automation is off | you may write Playwright or WebDriver tests (Electron, Tauri), but ask before running them locally; CI may run them |
| Do not launch GUI apps | run only offscreen (`QT_QPA_PLATFORM=offscreen`) or headless; if even that is unclear, ask |
| Visual checks go to the user | end the task with a short checklist of what to look at, instead of taking screenshots of their desktop |
| Specific workspace or monitor for tests | follow it; never open test windows on the workspace where the user works |

An offscreen Qt test draws into memory: no window appears and no real input device is used, so it does not touch the user's session. That makes it the default for agents. Evidence: moderate (verified locally, see section 3).

## 2. The rules that matter most

1. **Put logic where it can be tested without a window.** Pure QML or JS functions, C++ or Rust models, Tauri commands, Electron main process modules. Most bugs are in logic; test it as plain code. Evidence: strong (Humble Object pattern, Meszaros "xUnit Test Patterns").
2. **Run UI tests offscreen or headless by default.** Qt: `QT_QPA_PLATFORM=offscreen`. Electron and Tauri in CI: `xvfb-run` or a headless Wayland compositor. Evidence: moderate (Qt and Electron docs).
3. **Wait for conditions, never for time.** QML `tryCompare` and `SignalSpy.wait`, Playwright `expect(locator)`, WebDriver explicit waits. A fixed `wait(500)` is a flaky test. Evidence: strong.
4. **Send input through the test framework, not the OS.** QML `keyClick`/`mouseClick`, Playwright, WebDriver. These target the app under test only. Evidence: moderate.
5. **Test at more than one scale factor.** At least 1.0 and 2.0, plus the user's real one (for example 1.25 or 1.5). Text clipping and blurry icons show up only at fractional scales. Evidence: moderate (Qt High DPI docs).
6. **Pin fonts in any test that measures text or compares pixels.** Different fonts change widths and break layout tests and screenshots between machines. Evidence: moderate.
7. **Fail on QML warnings.** Binding loops, `undefined` property reads and type errors are bugs. Use `failOnWarning(/.*/)` in `initTestCase()` or check the log. Evidence: moderate (Qt docs).
8. **Each test creates its own objects and leaves nothing behind.** `createTemporaryObject` in QML, a fresh app instance per Electron test file. Evidence: strong.
9. **Keep pixel comparison tests few and tolerant.** They break on font, driver and scale changes. Prefer asserting geometry and properties (`width`, `implicitHeight`, `visible`, `text`). Evidence: moderate.
10. **Visual polish is checked by the user,** guided by a checklist, unless the user has said otherwise. Evidence: opinion (house rule on many machines).

## 3. Qt and QML: Qt Quick Test

Qt Quick Test runs `TestCase` QML files. Files named `tst_*.qml` are found by scanning the input directory (Qt docs).

### Running tests

```bash
# Arch Linux: /usr/bin/qmltestrunner may be the Qt 5 build (from qt5-declarative).
# Use the Qt 6 one explicitly:
QT_QPA_PLATFORM=offscreen /usr/lib/qt6/bin/qmltestrunner -input tests/ -import src/
```

Verified 2026-10-31 with Qt 6.12.0: four test functions (including a data driven one and a `SignalSpy`) passed offscreen, a deliberately wrong expectation failed with exit code 1 and an Actual/Expected diff, and `-o results.xml,junitxml -o -,txt` wrote JUnit XML for CI while still printing to the terminal. Running `/usr/bin/qmltestrunner` (the Qt 5 binary on that machine) on the same Qt 6 test exited 1 with no output at all: check `pacman -Qo $(command -v qmltestrunner)` or the "Using QtTest library" line before trusting a silent failure.

Other options: `-functions` lists test functions; pass `TestCaseName::test_function` to run one; `-platform offscreen` works instead of the environment variable.

For a C++ project, the harness is `QUICK_TEST_MAIN(name)` (or `QUICK_TEST_MAIN_WITH_SETUP(name, SetupClass)` to register C++ types and context properties in `qmlEngineAvailable`), built with `find_package(Qt6 REQUIRED COMPONENTS QuickTest Qml)` and registered with `add_test` (Qt docs). Set `QUICK_TEST_SOURCE_DIR` so it finds the QML files.

### A complete example (verified)

```qml
// tst_counter.qml
import QtQuick
import QtTest

TestCase {
    id: tc
    name: "Counter"
    width: 200; height: 200
    when: windowShown                 // keyboard and mouse events need a shown window

    Component { id: counterComp; Counter {} }
    SignalSpy { id: spy; signalName: "reachedFive" }

    function test_up_key_increments_data() {
        return [ { tag: "once", presses: 1, expected: 1 }, { tag: "four", presses: 4, expected: 4 } ]
    }
    function test_up_key_increments(data) {
        const c = createTemporaryObject(counterComp, tc)   // destroyed after the test, even on failure
        c.forceActiveFocus()
        for (let i = 0; i < data.presses; ++i) keyClick(Qt.Key_Up)
        compare(c.count, data.expected)
    }
    function test_signal_fires_at_five() {
        const c = createTemporaryObject(counterComp, tc)
        spy.target = c
        spy.clear()
        c.forceActiveFocus()
        for (let i = 0; i < 5; ++i) keyClick(Qt.Key_Up)
        compare(spy.count, 1)
    }
}
```

### TestCase API worth knowing (Qt docs)

| Need | Use |
|---|---|
| Compare / assert | `compare(actual, expected, msg)`, `verify(cond, msg)`, `fuzzyCompare(a, b, delta)` |
| Async change | `tryCompare(obj, "prop", value, timeoutMs)`, `tryVerify(() => cond, timeoutMs)` (default 5000 ms) |
| Signals | `SignalSpy { target; signalName }`, `count`, `signalArguments`, `wait(ms)` (fails if not emitted), `clear()` |
| Objects per test | `createTemporaryObject(component, parent, props)`, `createTemporaryQmlObject(qmlString, parent)` |
| Input | `keyClick(Qt.Key_X)`, `keyPress`/`keyRelease`, `mouseClick(item, x, y)`, `mouseDrag`, `mouseWheel` (keys go to the focused item) |
| Find items | `findChild(parent, "objectName")`; give testable items an `objectName` |
| Rendering | `waitForRendering(item)`, `grabImage(item)` (pixel access, `equals`, `save`) |
| Data driven | `test_x_data()` returns rows with a `tag`; `test_x(row)` runs per row |
| Warnings | `failOnWarning(/regex/)` (Qt 6.3+), `ignoreWarning(msg)` (fails if the warning never appears) |
| Lifecycle | `initTestCase`, `init`, `cleanup`, `cleanupTestCase` |
| Skip / known bug | `skip(msg)`, `expectFail(tag, msg)` |

Rules:

1. **Bind `when: windowShown` for any test that sends input.** Without it, events arrive before the window exists. Evidence: moderate (Qt docs).
2. **Use `wait()` only to let the event loop run, never as a synchronisation guess.** `sleep()` blocks the event loop entirely; avoid it. Evidence: moderate.
3. **Test sizes as numbers.** For layout rules ("text fits its box"), assert `label.implicitWidth <= box.width` and `label.truncated === false` (Text has a `truncated` property) at each scale factor you care about. Evidence: opinion (works well for the "text overflows" class of bugs).
4. **Give items an `objectName` only where tests need them,** and find them with `findChild`. Evidence: moderate.

### C++ and Rust models behind QML

Test C++ models with Qt Test (`QTest`, `QSignalSpy`, `QAbstractItemModelTester` to check a model follows the model contract). For Rust backends (cxx-qt), test the Rust logic with `cargo test` and keep the QML layer thin.

## 4. Quickshell and other QML shells

Quickshell configs use Quickshell types (`PanelWindow`, `Hyprland`, `Process`, `FileView`) that need the running shell and a compositor, so `qmltestrunner` cannot load a whole shell. What works:

1. **Move logic into plain QML components, JS libraries (`.pragma library`) and singletons with no Quickshell imports.** Test those with `qmltestrunner` offscreen.
2. **Stub the Quickshell module for components that only read a little from it.** A folder `stubs/Quickshell/qmldir` with fake types, passed with `-import stubs`, takes priority over the installed module. Verified 2026-10-31: a component importing `Quickshell` and calling `Quickshell.env("HOME")` was tested against a stub singleton.

```text
stubs/Quickshell/qmldir:
    module Quickshell
    singleton Quickshell 1.0 QuickshellStub.qml
```

```qml
// stubs/Quickshell/QuickshellStub.qml
pragma Singleton
import QtQuick
QtObject {
    property string shellDir: "/tmp/fake-shell"
    function env(name) { return name === "HOME" ? "/home/test" : "" }
}
```

```bash
QT_QPA_PLATFORM=offscreen /usr/lib/qt6/bin/qmltestrunner -import stubs -input tst_home.qml
```

3. **Check the running shell's log after a reload,** instead of interacting with it: QML errors and warnings appear there. Do not move the pointer or switch workspaces to "see" the change unless the user allows it.
4. **Respect the shell's own sizing rules in tests.** If the project has a global scale (for example a `UiScale` singleton) or named font sizes, stub them with the real values and test layout at each scale the user uses.
5. **Visual review is a checklist for the user:** which panel, which state (empty, full, long text, light and dark theme), which scale.
6. **Harness parity, from the UI mistakes library (`~/.claude/ui-designer/mistakes.md`, M11 to M14):**
   1. A harness proves nothing if it imports modules the real entry does not: load the component through the same entry file (or assert the import list matches) and read the real instance log after launch.
   2. Sample animation and scroll checks on `frameSwapped`, not on a timer.
   3. For a size that drives an animation, assert the drawn height equals the measured one within 1 px.
   4. Read two different files or items in a row and compare a field that differs, to catch a reused reader returning the previous one.

## 5. Electron

Electron does not maintain its own test tool; its docs list WebdriverIO, Selenium, Playwright and a custom IPC driver. Playwright's Electron support is experimental and covers Electron v21+ (Playwright docs).

```ts
// tests/app.spec.ts (Playwright docs pattern)
import { test, expect, _electron as electron } from '@playwright/test';

test('opens the main window', async () => {
  const app = await electron.launch({ args: ['.'] });
  const isPackaged = await app.evaluate(async ({ app }) => app.isPackaged); // runs in the main process
  expect(isPackaged).toBe(false);

  const window = await app.firstWindow();
  await expect(window.getByRole('heading', { name: 'Library' })).toBeVisible();
  await app.close();
});
```

Rules:

1. **Unit test the main process modules with Vitest in Node,** and the renderer with component tests; use `_electron` only for a few end to end flows. Evidence: moderate.
2. **Test IPC handlers as functions.** Export the handler, call it with a fake event, assert the result; then one end to end test proves the channel is wired. Evidence: opinion.
3. **On headless Linux CI, prefix with `xvfb-maybe` or `xvfb-run`** (Electron docs). Evidence: moderate.
4. **If launch times out,** the `nodeCliInspect` fuse must not be set to `false` (Playwright known issues). Evidence: moderate.
5. **Test the packaged app at least once per release** (`electron-builder` output), because asar packing, paths and fuses differ from development. Evidence: moderate.
6. Running these locally starts a browser engine and a window. Check the user's rules first (section 1).

## 6. Tauri

Tauri v2 offers three layers (Tauri docs):

| Layer | Tool | Runs a webview? |
|---|---|---|
| Rust commands and app logic | `cargo test`; `tauri::test` mock runtime (`mock_builder()`, `mock_context(noop_assets())`, `get_ipc_response`) | no |
| Frontend calling `invoke` | `@tauri-apps/api/mocks`: `mockIPC((cmd, args) => ...)`, `mockWindows('main')`, `clearMocks()` in `afterEach` | no (jsdom or happy-dom) |
| End to end | WebDriver through `tauri-driver` (or WebdriverIO's `@wdio/tauri-service`) | yes |

Rust command test with the mock runtime (shape from the `tauri::test` docs; not run here):

```rust
#[tauri::command]
fn add(a: i32, b: i32) -> i32 { a + b }

#[cfg(test)]
mod tests {
    use tauri::test::{mock_builder, mock_context, noop_assets, get_ipc_response, INVOKE_KEY};
    use tauri::ipc::{InvokeBody, CallbackFn};
    use tauri::webview::InvokeRequest;

    #[test]
    fn add_command() {
        let app = mock_builder()
            .invoke_handler(tauri::generate_handler![super::add])
            .build(mock_context(noop_assets()))
            .unwrap();
        let webview = tauri::WebviewWindowBuilder::new(&app, "main", Default::default()).build().unwrap();
        let res = get_ipc_response(&webview, InvokeRequest {
            cmd: "add".into(),
            callback: CallbackFn(0),
            error: CallbackFn(1),
            url: "http://tauri.localhost".parse().unwrap(),
            body: InvokeBody::Json(serde_json::json!({ "a": 2, "b": 3 })),
            headers: Default::default(),
            invoke_key: INVOKE_KEY.to_string(),
        });
        assert_eq!(res.unwrap().deserialize::<i32>().unwrap(), 5);
    }
}
```

Testing the plain function behind a command is not enough: it never runs the command layer. Every Tauri app gets:

- **(a) a name check:** the set of invoke names under `src/` equals the set in `generate_handler!` (the command is in the fast checks of `../quality/quality-gate.md`, verified on the trial repos). A registered command nothing invokes is reported too.
- **(b) one `get_ipc_response` test per command** that sends the exact JSON keys the frontend sends (camelCase, since Tauri renames snake_case Rust arguments: `project_id` arrives as `projectId`) and asserts the response shape.

Generated bindings (tauri-specta) replace (b) when the frontend imports them. Trial: stundenwerk A had 30 commands and 65 spec tests, none of which ran commands.rs.

WebDriver facts (Tauri docs): `cargo install tauri-driver --locked`; on Linux it needs `WebKitWebDriver` (check with `which WebKitWebDriver`; Debian packages it as `webkit2gtk-driver`, some distributions ship it with WebKitGTK); on Windows it needs `msedgedriver` matching the installed Edge. macOS has no WKWebView driver, so direct WebDriver tests do not run there. In CI on Linux, run under `xvfb-run`. Running it locally opens a real window: check the user's rules.

## 7. GTK, briefly

- Keep logic out of widgets and test it as plain code (Rust with gtk4-rs, Python, C).
- For end to end tests, accessibility based tools (dogtail and other AT-SPI clients) find widgets by role and name. They depend on the accessibility bus and are fragile under Wayland. Use them only for a few flows. Evidence: opinion.
- Run under a headless compositor or `xvfb-run` with `GDK_BACKEND=x11` in CI. Evidence: moderate.

## 8. Linux specifics: Wayland, HiDPI, multiple monitors, fonts

### Platforms

| Need | How |
|---|---|
| No window at all (Qt) | `QT_QPA_PLATFORM=offscreen` |
| Real X11 rendering in CI | `xvfb-run -a <command>` |
| Real Wayland in CI | a headless compositor: `weston --backend=headless`, or `sway` with `WLR_BACKENDS=headless WLR_LIBINPUT_NO_DEVICES=1`, then point the app at its socket with `WAYLAND_DISPLAY` |
| Layer shell apps (bars, panels, notification popups) | need a wlroots style compositor (headless sway); offscreen Qt cannot test layer shell placement |

Wayland behaviour differs from X11: apps cannot place their own windows, read global pointer position or grab input. A test that passes under `xvfb-run` can still fail on Wayland. Run at least the window management tests under a Wayland compositor if the app targets Wayland. Evidence: moderate.

### HiDPI and scale factors

Qt reads these (Qt High DPI docs):

| Variable | Use |
|---|---|
| `QT_SCALE_FACTOR=2` | global factor, to test HiDPI without HiDPI hardware; multiplies the platform's own ratio |
| `QT_SCREEN_SCALE_FACTORS="1;1.5"` | per screen factors (testing only; it overrides system DPI) |
| `QT_SCALE_FACTOR_ROUNDING_POLICY=PassThrough` | fractional factors pass through (default in Qt 6) |
| `QT_ENABLE_HIGHDPI_SCALING=0` | disables scaling, testing only, no effect on Wayland |

Run the same QML suite at several factors in CI:

```bash
for s in 1 1.25 1.5 2; do
  QT_QPA_PLATFORM=offscreen QT_SCALE_FACTOR=$s /usr/lib/qt6/bin/qmltestrunner -input tests/ || exit 1
done
```

Verified 2026-10-31 that the suite runs with `QT_SCALE_FACTOR=1.5` offscreen. What it catches depends on your assertions: assert `truncated`, implicit sizes against containers, and icon sizes against their backgrounds.

Electron: `--force-device-scale-factor=2`. GTK: `GDK_SCALE=2` (integer) and `GDK_DPI_SCALE` for text.

### Multiple monitors

The Qt offscreen platform reads a JSON file with virtual screens (`-platform offscreen:configfile=<path>`), each with `name`, `x`, `y`, `width`, `height`, `logicalDpi`, `logicalBaseDpi` and `dpr`. Verified 2026-10-31 with Qt 6.12: a test saw two screens, the second named `HDMI-A-2` with `devicePixelRatio` 2.

```json
{ "screens": [
  { "name": "DP-1",     "x": 0,    "y": 0, "width": 2560, "height": 1440, "logicalDpi": 96, "logicalBaseDpi": 96, "dpr": 1 },
  { "name": "HDMI-A-2", "x": 2560, "y": 0, "width": 3840, "height": 2160, "logicalDpi": 96, "logicalBaseDpi": 96, "dpr": 2 }
] }
```

```bash
/usr/lib/qt6/bin/qmltestrunner -platform offscreen:configfile=$PWD/screens.json -input tests/
```

The screen reports the width you wrote; check whether your code expects logical or physical pixels. Test: a window or panel per screen, mixed scale factors, a screen to the left of the primary (negative or offset coordinates), and the case where the preferred screen is missing (it cannot be unplugged live in this mode).

### Fonts

- Tests that check text fit must use the font the app ships or requires. Bundle it in the test assets, or install the same package in CI, and fail early if `fc-match "<family>"` returns a fallback.
- Test with long words in other scripts the user needs (for example Cyrillic, Kazakh letters such as ә ө ү, German compound words, CJK if relevant) and check the font covers them: `fc-list ':charset=04d9' family` lists fonts that cover U+04D9.
- Pixel tests and fonts: antialiasing and hinting settings in fontconfig change pixels; run pixel tests only in a pinned CI image.

## 9. What stays manual

Agents cannot judge: how it feels (animation smoothness, hover states, focus rings), colour harmony, real compositor behaviour (blur, transparency, layer order), real input devices, and real multi monitor hardware. For these, finish the work and give the user a checklist: the exact state to open, what to look for, at which scale and theme. Keep it short (5 to 10 lines).

## 10. Files in this folder

| File | Read when |
|---|---|
| `cli-and-tui-testing.md` | testing a command line tool or a terminal UI (Rust ratatui, shell scripts): exit codes, golden output, PTY tests, key events |
| `../performance/benchmarks.md` | measuring startup time or frame rate of a desktop app |

## 11. Checks

| Check | Pass condition |
|---|---|
| User rules | read; no OS level input, no windows on the user's screen; browser and GUI runs only when allowed |
| Logic testable | logic lives in plain components or modules with unit tests |
| Offscreen default | QML tests run with `QT_QPA_PLATFORM=offscreen` and the Qt 6 `qmltestrunner` |
| No time waits | `tryCompare`, `SignalSpy.wait`, Playwright auto waits; no fixed sleeps |
| Warnings fail | `failOnWarning` or log check for QML warnings |
| Scale factors | suite runs at 1.0, 2.0 and the user's real factor |
| Text fit | layout tests assert `truncated` and implicit sizes |
| Multi monitor | multi screen config tested where the app places windows per screen |
| Fonts | required font present in CI; coverage checked for the user's scripts |
| Electron / Tauri | logic unit tested; few end to end flows; packaged build tested per release |
| Tauri IPC contract | invoke names equal the `generate_handler!` set; each command crossed once through `get_ipc_response` with the frontend's camelCase keys, or tauri-specta bindings imported by the frontend |
| QML harness parity | harness loads through the real entry file; frame checks sample `frameSwapped`; drawn vs measured size within 1 px; two different items read in a row |
| CI artifacts | JUnit XML produced (`-o results.xml,junitxml`) |
| Manual checklist | short, concrete checklist handed to the user for visual and feel checks |
