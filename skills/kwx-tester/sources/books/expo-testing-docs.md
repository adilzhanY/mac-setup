# Expo testing documentation

- Authors: Expo
- Year: read 2026-10-31 (SDK 58 era)
- Legal URLs: https://docs.expo.dev/develop/unit-testing/ , https://docs.expo.dev/router/reference/testing/ , https://docs.expo.dev/eas/workflows/examples/e2e-tests/ , https://docs.expo.dev/eas/workflows/pre-packaged-jobs/

## What I read

The unit testing guide, the Expo Router testing reference, the EAS Workflows E2E example, and the maestro and maestro-cloud job sections of the pre-packaged jobs page.

## Key lessons used in mobile/react-native-expo.md, mobile/e2e-maestro-detox.md, mobile/mobile.md

- `npx expo install jest-expo jest @types/jest --dev` and `@testing-library/react-native`; preset `jest-expo`; react-test-renderer deprecated (no React 19 support).
- SDK 58+ requires Jest 30; Expo Router tests need RNTL v14 (v13 only on SDK 57).
- Expo recommends Maestro E2E via EAS Workflows over snapshot unit tests for UI.
- renderRouter with inline mocks, string arrays or fixture folders; initialUrl for deep links; testRouter helpers are async; matchers toHavePathname, toHaveSegments, toHaveSearchParams, toHaveRouterState; keep tests out of app/.
- e2e-test build profile (withoutCredentials, iOS simulator, Android apk); maestro job params build_id, flow_path, shards, retries, record_screen, include_tags; Android emulator runs on linux nested virtualization workers; the Maestro job is alpha.
