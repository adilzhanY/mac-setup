# Qt Quick Test, TestCase, SignalSpy, High DPI docs

- Author: The Qt Company
- Year: Qt 6 documentation, read 2026-10-31 (local Qt 6.12.0)
- Legal URL: https://doc.qt.io/qt-6/qtquicktest-index.html ; https://doc.qt.io/qt-6/qml-qttest-testcase.html ; https://doc.qt.io/qt-6/qml-qttest-signalspy.html ; https://doc.qt.io/qt-6/highdpi.html

## What I read

Qt Quick Test overview (harness, CMake, options, offscreen hint), TestCase type reference, SignalSpy reference, High DPI page (environment variables). Also the qoffscreenintegration source discussion for the offscreen config file (QTBUG-83094).

## Key lessons used in desktop/desktop.md

- Harness scans for `tst_*.qml`; `-input`, `-import`, `-functions`; `QUICK_TEST_MAIN` and `QUICK_TEST_MAIN_WITH_SETUP` with `qmlEngineAvailable`.
- Tests show a window unless run with `-platform offscreen`.
- `when: windowShown` before input; `tryCompare`/`tryVerify` default 5000 ms; `createTemporaryObject` cleans up even on failure; `failOnWarning` since 6.3; `ignoreWarning` fails if the warning never appears.
- SignalSpy `wait()` fails the test when the signal is not emitted.
- `QT_SCALE_FACTOR` tests HiDPI without hardware; `QT_SCREEN_SCALE_FACTORS` for testing only; `QT_ENABLE_HIGHDPI_SCALING` no effect on Wayland.
- Offscreen platform `configfile=` JSON with named screens and dpr (verified locally).
