# Google Play Console help (testing) and Firebase Test Lab docs

- Authors: Google
- Year: read 2026-10-31
- Legal URLs: https://support.google.com/googleplay/android-developer/answer/14151465 (testing requirements for new personal accounts), https://support.google.com/googleplay/android-developer/answer/9842757 (pre-launch reports), https://firebase.google.com/docs/test-lab/usage-quotas-pricing

## What I read

The three pages in full.

## Key lessons used in mobile/stores-and-device-farms.md (also mobile/mobile-accessibility-testing.md)

- Personal accounts created after November 13, 2023: closed test with at least 12 testers opted in continuously for 14 days before applying for production; review usually within 7 days; more testing can be required for low engagement.
- Pre-launch report: crawls the app for several minutes on Android 9+ devices chosen by Google; stability, performance, accessibility (touch targets, contrast, labels, implementation) and screenshots; test account credentials, Robo scripts, up to three deep links; no purchases, US location, no rooted device checks.
- Test Lab Spark plan: 10 virtual and 5 physical test runs per day; Blaze: 60 virtual and 30 physical free minutes per day, then $1 and $5 per device hour, billed per minute.
