# Electron automated testing, Playwright Electron API, Tauri v2 testing

- Authors: Electron project; Microsoft Playwright team; Tauri project
- Year: read 2026-10-31 (Playwright 1.64)
- Legal URL: https://www.electronjs.org/docs/latest/tutorial/automated-testing ; https://www.electronjs.org/docs/latest/tutorial/testing-on-headless-ci ; https://playwright.dev/docs/api/class-electron ; https://v2.tauri.app/develop/tests/ ; https://v2.tauri.app/develop/tests/mocking/ ; https://v2.tauri.app/develop/tests/webdriver/ ; https://v2.tauri.app/develop/tests/webdriver/manual-setup/ ; https://docs.rs/tauri/latest/tauri/test/index.html

## What I read

Electron automated testing and headless CI pages; Playwright Electron class; Tauri testing overview, mocking, WebDriver and manual setup pages; `tauri::test` module docs.

## Key lessons used in desktop/desktop.md

- Electron maintains no own test tool; lists WebdriverIO, Selenium, Playwright, custom driver.
- Playwright Electron support is experimental, Electron v21+; `nodeCliInspect` fuse must not be false.
- `xvfb-maybe` on headless Linux CI.
- Tauri: mock runtime for Rust, `mockIPC`/`mockWindows`/`clearMocks` for the frontend, WebDriver via tauri-driver on Linux and Windows only (no macOS driver); `cargo install tauri-driver --locked`; WebKitWebDriver on Linux.
