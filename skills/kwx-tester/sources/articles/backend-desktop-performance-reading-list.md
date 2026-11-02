# Backend, desktop and performance testing reading list

Every URL used for the `backend/`, `desktop/` and `performance/` folders of kwx-tester, read on 2026-10-31, with one line on what it gave. Per source notes are in `sources/books/` (file names in brackets).

## Supabase and Postgres (supabase-testing-docs.md, testcontainers-docs.md)

- https://supabase.com/docs/guides/local-development/testing/overview : `supabase test db`, CI workflow, recommendations (transactions, anon and authenticated, negative cases).
- https://supabase.com/docs/guides/database/testing : pgTAP file shape, `supabase/tests/database`, minimum CLI version.
- https://supabase.com/docs/guides/database/postgres/testing-row-level-security : `set local role`, JWT claim, `results_eq`/`is_empty`, app level test with supabase-js, the gotchas (do not drop the policy, filter by own ids).
- https://supabase.com/docs/guides/local-development/testing/pgtap-extended : dbdev, basejump test helpers, `throws_ok` with 42501, alphabetical file order.
- https://supabase.com/docs/reference/cli/supabase-start : `-x` container names, `--ignore-health-check`, `db reset` description.
- https://supabase.com/docs/reference/cli/supabase-test-db : pg_prove in a container, `.sql`/`.pg`, `--linked`, `--db-url`.
- https://supabase.com/docs/guides/local-development/cli/getting-started : Docker requirement, ports 54321 to 54324, Mailpit included.
- https://supabase.com/docs/guides/database/connecting-to-postgres/pooling-and-limits : pool size, pooler client limits per compute, behaviour at the limit.
- https://supabase.com/docs/guides/platform/performance : checked for load testing advice; none there.
- https://supabase.com/docs/guides/database/postgres/row-level-security : RLS performance advice, `(select auth.uid())` initPlan caching, index policy columns, `to` role clause.
- https://pglite.dev/docs/ : PGlite in memory, single exclusive connection, extensions API.
- https://testcontainers.com/guides/getting-started-with-testcontainers-for-nodejs/ : basic Postgres container lifecycle.
- https://node.testcontainers.org/modules/postgresql/ : connection getters, snapshot and restore with its caveats.

## API testing, contracts, schemas (owasp-api-security-top-10-2023.md, ietf-idempotency-key-draft.md, pact-docs.md, schemathesis-docs.md)

- https://api-security.owasp.org/editions/2023/en/0x11-t10 : the 2023 list API1 to API10.
- https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization : prevention list, "write tests", random ids.
- https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ : 400, 409, 422 semantics, fingerprint, expiry (draft 08).
- https://github.com/Xunnamius/next-test-api-route-handler : App Router support from next 14.0.4, must be first import, `testApiHandler`.
- https://docs.pact.io/getting_started/what_is_pact_good_for : when Pact fits and when it does not.
- https://docs.pact.io/getting_started/how_pact_works : consumer, pact file, provider verification, provider states.
- https://docs.pact.io/pact_broker/can_i_deploy : `can-i-deploy` and `record-deployment` commands.
- https://docs.pact.io/implementation_guides/javascript/docs/consumer : V4 builder consumer test.
- https://docs.pact.io/implementation_guides/javascript/docs/provider : Verifier options, state handlers warning, publish from CI.
- https://schemathesis.readthedocs.io/en/stable/ : supported specs, stateful testing, curl reproducers.
- https://schemathesis.readthedocs.io/en/stable/quick-start/ : `uvx schemathesis run`, auth header, replay, pytest.
- https://schemathesis.readthedocs.io/en/stable/reference/checks/ : every check and its default.
- https://www.oasdiff.com/ and https://github.com/oasdiff/oasdiff (README) : breaking rule, 778 checks, `--fail-on ERR`, GitHub Action.
- https://the-guild.dev/graphql/inspector/docs/commands/diff : diff command and breaking / dangerous / non-breaking classes.

## External services and time (stripe-testing-docs.md, mailpit-and-revenuecat-docs.md)

- https://docs.stripe.com/billing/testing : sandboxes per CI and local, test cards, triggered events carry fake data, failed payment testing.
- https://docs.stripe.com/billing/testing/test-clocks/api-advanced-usage : clock API calls, advance limits, events, limits per clock, deletion after 30 days.
- https://docs.stripe.com/webhooks : `stripe listen`, `stripe trigger`, retries, order, duplicates, signature tolerance.
- https://docs.stripe.com/api/idempotent_requests : idempotency key behaviour in API v1 and v2.
- https://github.com/stripe/stripe-node (README) : `generateTestHeaderString` for signed test payloads.
- https://www.revenuecat.com/docs/test-and-launch/sandbox : Test Store and platform sandboxes, recommended workflow.
- https://www.revenuecat.com/docs/test-and-launch/sandbox/google-play-store : license testers, accelerated renewal table, six renewals.
- https://mailpit.axllent.org/docs/install/docker/ : docker run command, ports, env vars.
- https://mailpit.axllent.org/docs/api-v1/ : REST API overview.
- https://raw.githubusercontent.com/axllent/mailpit/develop/server/ui/api/v1/swagger.json : exact API paths.

## Rust tooling (rust-concurrency-and-test-runner-docs.md, rust-fuzz-book.md, oss-fuzz-docs.md)

- https://nexte.st/docs/features/retries/ : retries, flaky result, JUnit flaky tags.
- https://nexte.st/docs/configuration/ : profiles, fail-fast, slow-timeout, inheritance.
- https://nexte.st/docs/configuration/test-groups/ : test groups with max-threads.
- https://nexte.st/docs/features/slow-tests/ : `terminate-after` syntax.
- https://docs.rs/loom/latest/loom/ : model, cfg, shim module, env vars, limits.
- https://docs.rs/tokio/latest/tokio/time/fn.pause.html : paused time rules and gotchas.
- https://docs.rs/sqlx/latest/sqlx/attr.test.html : `#[sqlx::test]` options and cleanup.
- https://rust-fuzz.github.io/book/cargo-fuzz/setup.html : install, nightly requirement.
- https://rust-fuzz.github.io/book/cargo-fuzz/tutorial.html : init, run, targets, artifacts.
- https://github.com/CodeIntelligenceTesting/jazzer.js (README) and https://registry.npmjs.org/@jazzer.js/core : usage, Jest runner; npm shows 4.0.0 published 2026-04-15, not deprecated.
- https://github.com/google/atheris (README) : Python 3.11 to 3.14, instrument_imports, FuzzedDataProvider.
- https://google.github.io/oss-fuzz/ : bug counts as of August 2023, languages.
- https://google.github.io/oss-fuzz/getting-started/new-project-guide/ : seed corpus, dictionaries, size checks, engine independence.

## Desktop, CLI and TUI (qt-quick-test-docs.md, electron-tauri-playwright-desktop-docs.md, cli-tui-testing-docs.md)

- https://doc.qt.io/qt-6/qtquicktest-index.html : harness, CMake, options, offscreen hint, setup class.
- https://doc.qt.io/qt-6/qml-qttest-testcase.html : full TestCase API.
- https://doc.qt.io/qt-6/qml-qttest-signalspy.html : SignalSpy members.
- https://doc.qt.io/qt-6/highdpi.html : scale factor environment variables for testing.
- https://codebrowser.dev/qt6/qtbase/src/plugins/platforms/offscreen/qoffscreenintegration.cpp.html and https://bugreports.qt.io/browse/QTBUG-83094 : offscreen `configfile` JSON with screens (seen through search summaries; then verified locally).
- https://www.electronjs.org/docs/latest/tutorial/automated-testing : options, Playwright example.
- https://www.electronjs.org/docs/latest/tutorial/testing-on-headless-ci : xvfb-maybe.
- https://playwright.dev/docs/api/class-electron : experimental, Electron v21+, nodeCliInspect fuse.
- https://v2.tauri.app/develop/tests/ : mock runtime and WebDriver overview, platform support.
- https://v2.tauri.app/develop/tests/mocking/ : mockIPC, mockWindows, clearMocks.
- https://v2.tauri.app/develop/tests/webdriver/ and https://v2.tauri.app/develop/tests/webdriver/manual-setup/ : tauri-driver install, WebKitWebDriver, msedgedriver, no macOS.
- https://docs.rs/tauri/latest/tauri/test/index.html : mock_builder, get_ipc_response example.
- https://docs.rs/assert_cmd/latest/assert_cmd/ and https://github.com/assert-rs/assert_cmd/blob/master/CHANGELOG.md : API and the cargo_bin deprecation history.
- https://docs.rs/trycmd/latest/trycmd/ : file format, wildcards, redactions, overwrite.
- https://bats-core.readthedocs.io/en/stable/writing-tests.html : run, status checks, separate stderr, temp dirs.
- https://ratatui.rs/recipes/testing/snapshots/ : TestBackend snapshots, colour limitation, PTY tests with termlens.
- https://docs.rs/expectrl/latest/expectrl/ : expect style PTY API.
- https://github.com/charmbracelet/vhs : tape format, golden text output, Wait, Require.

## Performance (tene-how-not-to-measure-latency.md, gregg-active-benchmarking-and-use-method.md, google-sre-book-slo-chapter.md, k6-docs.md, load-tool-readmes.md, criterion-user-guide.md, vitest-5-benchmarking.md, benchmark-tool-docs.md)

- https://qconsf.com/sf2012/dl/qcon-sanfran-2012/slides/GilTene_HowNotToMeasureLatency.pdf : the full deck, coordinated omission example, lessons.
- https://www.infoq.com/presentations/latency-response-time/ : talk page (abstract only; video not watched).
- https://github.com/giltene/wrk2 : corrected vs uncorrected numbers, `-R`, `--u_latency`.
- https://www.brendangregg.com/activebenchmarking.html : active vs passive benchmarking, disturbance list.
- https://www.brendangregg.com/usemethod.html : USE definition and resource list.
- https://www.brendangregg.com/USEmethod/use-linux.html : Linux commands per resource.
- https://www.brendangregg.com/blog/2014-05-03/the-benchmark-paradox.html : benchmark paradox.
- https://www.brendangregg.com/systems-performance-2nd-edition-book.html : checked for a free chapter 12; none.
- https://sre.google/sre-book/service-level-objectives/ : percentiles vs averages, aggregation windows.
- https://grafana.com/docs/k6/latest/using-k6/thresholds/ : threshold syntax.
- https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/ : executor list.
- https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/ : open vs closed, coordinated omission.
- https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/dropped-iterations/ : meaning and advice.
- https://grafana.com/docs/k6/latest/testing-guides/test-types/ : test types and guidance.
- https://grafana.com/docs/k6/latest/set-up/install-k6/ : install options (no Arch package).
- https://github.com/grafana/k6/releases/tag/v2.0.0 : breaking changes in k6 2.
- https://github.com/hatoo/oha (README and v1.16.0 release) : flags, latency correction.
- https://github.com/tsenart/vegeta (README) : rate, coordinated omission note, report types.
- https://bheisler.github.io/criterion.rs/book/analysis.html : analysis process.
- https://bheisler.github.io/criterion.rs/book/faq.html : CI noise, baselines, black_box.
- https://docs.rs/divan/latest/divan/ : divan setup and features.
- https://vitest.dev/guide/benchmarking and https://vitest.dev/guide/migration : Vitest 5 bench fixture and removed flags.
- https://github.com/evanwashere/mitata : mitata usage, do_not_optimize, gc modes.
- https://github.com/sharkdp/hyperfine/releases/tag/v2.0.0 : hyperfine 2 changes.
- https://codspeed.io/docs/instruments/cpu : CPU simulation instrument, integrations.
- https://bencher.dev/docs/explanation/thresholds/ : statistical thresholds.
- https://github.com/gungraun/gungraun (README) : iai-callgrind's new name.

## Version checks

- GitHub releases API and the npm and crates.io registries, queried 2026-10-31, for the current versions quoted in the files (k6 2.3.0, oha 1.16.0, Locust 2.47.0, hyperfine 2.0.0, nextest 0.9.150, insta 1.49.0, proptest 1.12.0, loom 0.7.2, cargo-fuzz 0.13.2, Schemathesis 4.32.7, Pact JS 17.1.4, Testcontainers Node 12.2.1 and Rust 0.28.0, Supabase CLI 2.122.0, Mailpit 1.33.0, vhs 0.12.1, bats-core 1.14.0, ratatui 0.30.2, Vitest 5.0.5, tinybench 6.2.2, supertest 7.3.1, fast-check 4.10.2, MSW 3.0.3, PGlite 0.5.14, criterion 0.8.2, divan 0.1.21, termlens 0.11.7, expectrl 0.9.0, axum 0.8.9, sqlx 0.9.0, tokio 1.54.1).

## Cited but not read

- Brendan Gregg, "Systems Performance", 2nd ed. (2020), chapter 12 Benchmarking: not free; lessons taken from his free web pages instead.
- Gil Tene's talk video (InfoQ, QCon SF 2015): the 2012 slides were read instead; the video was not watched.
- John Hughes, "QuickCheck testing for fun and profit" (2007): cited for state machine testing from general knowledge; another kwx-tester agent read Hughes' "How to Specify It!" (see `sources/books/hughes-how-to-specify-it.md`).
- Kaner, Bach, Pettichord, "Lessons Learned in Software Testing" (2001): cited for classic test design; not freely available.
