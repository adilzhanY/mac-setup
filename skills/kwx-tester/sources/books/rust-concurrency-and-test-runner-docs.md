# loom, tokio time, cargo-nextest, sqlx test docs

- Authors: tokio project (loom, tokio), nextest project (Rain and contributors), sqlx project
- Year: read 2026-10-31 (loom 0.7.2, tokio 1.54, nextest 0.9.150, sqlx 0.9)
- Legal URL: https://docs.rs/loom/latest/loom/ ; https://docs.rs/tokio/latest/tokio/time/fn.pause.html ; https://nexte.st/docs/features/retries/ ; https://nexte.st/docs/configuration/ ; https://nexte.st/docs/configuration/test-groups/ ; https://nexte.st/docs/features/slow-tests/ ; https://docs.rs/sqlx/latest/sqlx/attr.test.html

## What I read

loom crate docs; tokio `time::pause` docs; nextest pages on retries and flaky results, configuration profiles, test groups and slow tests; the `#[sqlx::test]` attribute docs.

## Key lessons used in backend/rust-services-testing.md

- loom: `loom::model`, `cfg(loom)` dependency, shim module, `LOOM_MAX_PREEMPTIONS` 2 or 3, checkpoint files, cannot model all Relaxed reorderings, spin loops need `yield_now`.
- tokio pause: needs `test-util`, current thread runtime, auto advance to the next timer, blocking tasks inhibit auto advance, only tokio's Instant.
- nextest: flaky tests count as success by default; `flaky-result = "fail"`; `--retries` disables per test overrides; profiles with `fail-fast`, `slow-timeout` with `terminate-after`; test groups with `max-threads`.
- sqlx test: new database per test, migrations applied, fixtures in order, failed test databases kept.
