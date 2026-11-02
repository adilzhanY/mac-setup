# Android developer docs: Test your app with pseudolocales

- Author: Google (Android Developers)
- Year: current page, read 2026-10-31
- Legal URL: https://developer.android.com/guide/topics/resources/pseudolocales

## What I read

The full page.

## Key lessons used in exploratory/i18n-and-localisation-testing.md

- en-XA: accents, expanded text, brackets around each message; ar-XB: right to left with reversed text.
- Enable per build type: `isPseudoLocalesEnabled = true` (Kotlin DSL), usually on debug.
- Selected in system Settings, Languages, with developer options; affects all apps that support pseudolocales.
