# Maestro documentation

- Authors: mobile.dev (Maestro team)
- Year: read 2026-10-31
- Legal URL: https://docs.maestro.dev/ (index at https://docs.maestro.dev/llms.txt; every page has a .md version)

## What I read

How Maestro works, the React Native platform page, selectors, wait commands, permissions, launchApp, assertScreenshot, CLI install, CLI commands and options, test reports and artifacts, and the Cloud and EAS integration list.

## Key lessons used in mobile/e2e-maestro-detox.md

- Black box: drives the device through the accessibility layer and "low-level device commands for tap events, swipe gestures, and text input" via a driver app; so a local run is input injection.
- Prefer visible text selectors, id for icons and localized apps, relational selectors for dynamic elements, `enabled: true` before tapping a button that waits on validation.
- Assertions poll and are the main wait; extendedWaitUntil for long operations; waitForAnimationToEnd; retryTapIfNoChange for ghost taps; avoid 60 s timeouts.
- launchApp grants all permissions by default; set them explicitly; values can come from env variables.
- Expo Go needs openLink instead of launchApp with your appId; testID maps to id.
- Reports with `--format junit|html --output`, artifacts in ~/.maestro/tests or `--test-output-dir`.
- Cloud: 20 minute soft limit per execution; pre-packaged EAS jobs.
