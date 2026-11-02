# Rust services: testing tools in depth

The tester's extras for Rust services, on top of kwx-developer `languages/rust/testing.md` (read it first: layout, `tests/it/main.rs`, insta basics, proptest basics, the `check` helper, anti-patterns). This file adds what that file leaves out: nextest configuration for CI, insta settings that matter for API output, proptest strategies and state machine tests, quickcheck, loom for lock free and concurrent code, tokio paused time in detail, `#[sqlx::test]` options, Testcontainers and wiremock. Fuzzing has its own file, `fuzzing.md`.

## Contents

1. cargo-nextest in CI
2. insta for API and error output
3. proptest beyond the basics
4. quickcheck, and when to pick it
5. loom for concurrency
6. tokio: paused time and deterministic async tests
7. `#[sqlx::test]` options
8. Testcontainers and wiremock
9. Checks

## 1. cargo-nextest in CI

nextest (0.9.150, October 2026) runs each test in its own process, which isolates global state and gives per test timeouts and retries. It does not run doc tests; run `cargo test --doc` too.

`.config/nextest.toml` (syntax from the nextest docs):

```toml
[profile.default]
slow-timeout = { period = "30s", terminate-after = 4 }   # kill a hung test after 2 minutes

[profile.ci]
fail-fast = false          # report every failure, not just the first
retries = 2                # stopgap only; see flaky rule below
flaky-result = "fail"      # a test that passes only on retry still fails the run
slow-timeout = { period = "60s", terminate-after = 5 }

[profile.ci.junit]
path = "junit.xml"         # written under target/nextest/ci/

[test-groups]
serial-db = { max-threads = 1 }

[[profile.default.overrides]]
filter = 'test(/^db_serial::/)'
test-group = 'serial-db'
```

Run: `cargo nextest run --profile ci`, and `cargo test --doc` in the same job.

Rules:

1. **Set `flaky-result = "fail"` in CI.** By default nextest counts a test that passes on retry as a success, so retries silently hide flakiness. With `fail`, the run fails and the JUnit file marks the test with `<flakyFailure>`. Evidence: moderate (nextest docs).
2. **`--retries` on the command line disables per test overrides and backoff settings from the config.** Configure retries in the profile, not on the command line. Evidence: moderate (nextest docs).
3. **Use test groups instead of `--test-threads=1` for the whole suite** when only a few tests share a resource. Evidence: moderate.
4. **Always set a `terminate-after`.** A hung async test otherwise blocks CI until the job timeout. Evidence: opinion.
5. **Reproduce a CI failure locally with the same profile and the same seed** (`PROPTEST_` env vars, `--run-ignored` flags) before declaring it flaky. Evidence: opinion.

## 2. insta for API and error output

Beyond the basics in the developer file:

- **Snapshot JSON responses with redactions,** and sort maps so key order is stable:

```rust
insta::with_settings!({ sort_maps => true }, {
    insta::assert_json_snapshot!(body, {
        ".id" => "[id]",
        ".created_at" => "[timestamp]",
        ".items[].id" => "[id]",
    });
});
```

- **Snapshot error messages and `Display` output of error types.** These are part of the user facing contract and change by accident.
- **Use `insta::glob!` for file driven tests:** one snapshot per input file in `tests/data/*.json`. Adding a case is adding a file.
- **Filters for paths and durations:** `insta::with_settings!({ filters => vec![(r"\d+ms", "[duration]")] }, { ... })`.
- **Review with `cargo insta review` (needs `cargo install cargo-insta`).** Without it, a failing inline snapshot cannot be accepted automatically; you edit the `@"..."` literal by hand. Verified 2026-10-31: an empty inline snapshot on a ratatui `TestBackend` failed with a clear diff, and the corrected literal passed.
- In CI (`CI` set), insta never writes snapshots, so a changed snapshot fails the build. Keep it that way.

## 3. proptest beyond the basics

- **Build strategies for domain types, not only primitives:**

```rust
use proptest::prelude::*;

fn amount() -> impl Strategy<Value = i64> { 0i64..=1_000_000_00 }        // cents, within limits
fn email() -> impl Strategy<Value = String> { "[a-z]{1,10}@[a-z]{1,10}\\.(com|de|kz)" }

prop_compose! {
    fn order()(lines in prop::collection::vec(amount(), 1..20), coupon in prop::option::of("[A-Z]{5}")) -> Order {
        Order { lines, coupon }
    }
}

proptest! {
    #[test]
    fn total_never_negative(o in order()) {
        prop_assert!(o.total() >= 0);
    }
}
```

- **State machine tests** (`proptest-state-machine` crate): generate sequences of operations (create, update, delete, list) against the real system and a simple model (a `HashMap`), and assert they agree after every step. This finds ordering bugs that example tests miss. Evidence: strong (Hughes, "QuickCheck testing for fun and profit"; model based testing literature).
- **Bias toward edges:** proptest generates boundary values for integers often, but for strings use regex strategies that include empty, unicode (`\\PC*`) and very long cases explicitly.
- **Shrinking needs determinism.** If the code under test uses the clock or randomness, inject them, or shrinking produces nonsense.
- **Case count:** default 256. Raise it in a nightly job with `PROPTEST_CASES=10000`, not in every PR run.
- Verified 2026-10-31 with proptest 1.12: a round trip property and a "never panics on any printable string" property ran in the `tests/it` crate in milliseconds.

## 4. quickcheck, and when to pick it

`quickcheck` (1.1) generates values from the type (`Arbitrary`) and shrinks per type. It is simpler, with less control over value ranges. Prefer proptest for new code (strategies per test, regression files, better shrinking of composite values); keep quickcheck where a project already uses it. `bolero` (0.13) runs the same harness as a property test under `cargo test` and as a fuzz target under libFuzzer or AFL, which is useful when you want both (see `fuzzing.md`). Evidence: moderate (crate docs).

## 5. loom for concurrency

Use loom when the code has its own synchronization: atomics, a custom lock, a channel, a lock free queue, a cache with double checked locking. loom runs the test closure many times and explores the possible thread interleavings under the C11 memory model.

Setup (loom 0.7.2 docs):

```toml
[target.'cfg(loom)'.dependencies]
loom = "0.7"
```

```rust
// src/sync.rs: one shim module so the same code builds with std or loom
#[cfg(loom)]
pub(crate) use loom::sync::{Arc, Mutex, atomic::{AtomicUsize, Ordering}};
#[cfg(not(loom))]
pub(crate) use std::sync::{Arc, Mutex, atomic::{AtomicUsize, Ordering}};
```

```rust
// tests/loom_counter.rs
#![cfg(loom)]
use loom::thread;

#[test]
fn two_increments_are_not_lost() {
    loom::model(|| {
        let c = std::sync::Arc::new(my_crate::Counter::new());
        let c2 = c.clone();
        let t = thread::spawn(move || c2.incr());
        c.incr();
        t.join().unwrap();
        assert_eq!(c.get(), 2);
    });
}
```

Run: `RUSTFLAGS="--cfg loom" cargo test --test loom_counter --release`.

Rules and limits (loom docs):

- Only types from loom are modelled. Code that uses `std` atomics directly is invisible to loom; that is why the shim module exists.
- The number of interleavings explodes with threads and operations. Keep models to 2 or 3 threads and few operations. `LOOM_MAX_PREEMPTIONS=2` or 3 catches most bugs in practice.
- loom cannot model every reordering that `Relaxed` allows, so a passing loom test is strong evidence, not proof.
- Spin loops must call `loom::thread::yield_now()`, or the model hangs.
- To debug, `LOOM_CHECKPOINT_FILE=fail.json LOOM_CHECKPOINT_INTERVAL=1` saves the failing interleaving for replay, and `LOOM_LOG=trace LOOM_LOCATION=1` prints where threads switched.
- loom does not test tokio tasks. For async code, test with tokio's tools (section 6); tokio itself uses loom internally for its primitives.

Evidence: moderate (loom docs; tokio uses it for its own scheduler and channels).

## 6. tokio: paused time and deterministic async tests

`tokio::time::pause` facts (tokio docs): needs the `test-util` and `time` features and the `current_thread` runtime; `Instant::now()` (tokio's, not std's) returns a saved value; when the runtime has nothing else to do, the clock jumps to the next pending timer; `advance(d)` moves it by hand; a running blocking task stops the auto advance.

```toml
[dev-dependencies]
tokio = { version = "1", features = ["macros", "rt", "time", "test-util"] }
```

Verified 2026-10-31 with tokio 1.54: a retry helper that sleeps 10 s between three tries reports exactly 20 s elapsed, and the test finishes instantly.

```rust
#[tokio::test(start_paused = true)]
async fn retry_waits_twenty_seconds_without_real_waiting() {
    let start = tokio::time::Instant::now();
    let tries = my_crate::with_retry(|| false).await;
    assert_eq!(tries, 3);
    assert_eq!(start.elapsed(), std::time::Duration::from_secs(20));
}
```

Rules:

1. **Use tokio's `Instant` and `sleep` in the code under test,** not `std::time::Instant` or `std::thread::sleep`, or paused time has no effect. Evidence: strong (tokio docs).
2. **Timeouts become testable:** with paused time, `tokio::time::timeout(Duration::from_secs(30), fut)` resolves in microseconds when `fut` never completes. Test every timeout path this way. Evidence: moderate.
3. **Do not mix paused time with real network IO.** The clock auto advances while the socket waits, and timeouts fire early. Use paused time for logic with fake IO; use real time with generous limits for socket tests. Evidence: moderate.
4. **Test cancellation:** drop a future halfway (`tokio::select!` with a timer) and assert no half written state remains. Evidence: opinion.
5. **Find tasks that never finish:** tests that pass while spawned tasks still run hide errors. Keep the `JoinHandle` and await it, or use a `JoinSet` and assert it drains. Evidence: opinion.

## 7. `#[sqlx::test]` options

Requires `DATABASE_URL` with a role that can create databases (sqlx docs).

| Attribute | Effect |
|---|---|
| `#[sqlx::test]` | new database per test; migrations from `./migrations` applied if the folder exists |
| `#[sqlx::test(migrations = "db/migrations")]` | other folder, relative to `CARGO_MANIFEST_DIR` |
| `#[sqlx::test(migrator = "my_crate::MIGRATOR")]` | migrator from another crate |
| `#[sqlx::test(migrations = false)]` | empty database (for testing migrations themselves) |
| `#[sqlx::test(fixtures("users", "posts"))]` | runs `fixtures/users.sql` then `fixtures/posts.sql`, in that order (order them for foreign keys) |
| `#[sqlx::test(fixtures(path = "./fixtures", scripts("users")))]` | fixtures from another folder |

Test arguments: `PgPool`, `PoolConnection<Postgres>`, or `PoolOptions<Postgres>` plus connect options when the test builds its own pool. Databases of passing tests are dropped; failed tests keep theirs for debugging, and leftovers are cleaned on the next run.

Migration test with sqlx: `#[sqlx::test(migrations = false)]`, then run migrations up to N-1 with a `Migrator` filtered to those versions, insert data, run the rest, assert (recipe in `database-testing.md` section 6).

## 8. Testcontainers and wiremock

Testcontainers for Rust (0.28, with `testcontainers-modules` 0.15) when tests must own the container:

```rust
use testcontainers_modules::{postgres::Postgres, testcontainers::{ImageExt, runners::AsyncRunner}};

#[tokio::test]
async fn with_container() -> anyhow::Result<()> {
    let node = Postgres::default().with_tag("17").start().await?;
    let url = format!(
        "postgres://postgres:postgres@127.0.0.1:{}/postgres",
        node.get_host_port_ipv4(5432).await?
    );
    let pool = sqlx::PgPool::connect(&url).await?;
    // run migrations, test...
    Ok(())
}
```

Starting a container per test is slow; start one per test binary (a `OnceCell`) and create a database per test inside it. (Snippet from the crate docs pattern; not run here.)

wiremock (0.6) for third party HTTP:

```rust
use wiremock::{MockServer, Mock, ResponseTemplate, matchers::{method, path}};

#[tokio::test]
async fn retries_on_503_then_succeeds() {
    let server = MockServer::start().await;
    Mock::given(method("POST")).and(path("/v1/charges"))
        .respond_with(ResponseTemplate::new(503)).up_to_n_times(2).mount(&server).await;
    Mock::given(method("POST")).and(path("/v1/charges"))
        .respond_with(ResponseTemplate::new(200).set_body_json(serde_json::json!({"id": "ch_1"})))
        .expect(1).mount(&server).await;

    let client = PaymentClient::new(server.uri());
    assert_eq!(client.charge(500).await.unwrap().id, "ch_1");
}   // `expect(1)` is verified when `server` drops
```

Test the slow path with `ResponseTemplate::new(200).set_delay(Duration::from_secs(10))` and a client timeout of 1 s; assert the timeout error variant.

## 9. Checks

| Check | Pass condition |
|---|---|
| nextest config | CI profile with `fail-fast = false`, `flaky-result = "fail"`, `slow-timeout` with `terminate-after`, JUnit output |
| Doc tests | `cargo test --doc` runs next to nextest |
| Snapshots | JSON snapshots redacted and map sorted; no `.snap.new` files committed |
| Properties | domain strategies; state machine test for stateful components; nightly high case count job |
| loom | every custom synchronization primitive has a loom model behind `cfg(loom)` with a shim module |
| Async time | timeouts and retries tested with `start_paused`; tokio `Instant` used in code under test |
| Tasks | spawned tasks awaited or drained in tests |
| sqlx | `#[sqlx::test]` per DB test; fixtures ordered for foreign keys; migration tests use `migrations = false` |
| Containers | one container per binary, database per test |
| Third parties | wiremock with `expect(n)`; retry, error and timeout paths covered |
