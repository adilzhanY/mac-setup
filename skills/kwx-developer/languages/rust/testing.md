# Testing

Where Rust tests live, how to keep them fast and cheap to write, and when to reach for snapshots, property tests, fuzzing and benchmarks. Sources: Rust Book ch. 11, Effective Rust item 30, matklad "Delete Cargo Integration Tests" and "How to Test", insta and proptest docs, Zero To Production.

## Contents

1. Layout
2. What to test, and at which boundary
3. Writing tests
4. Snapshot tests with insta
5. Property tests with proptest
6. Async, IO and databases
7. Doc tests and examples
8. Running tests: cargo test, nextest, CI
9. Fuzzing and benchmarks
10. Anti-patterns
11. Checks

## 1. Layout

| Kind | Where | Sees | Built as |
|---|---|---|---|
| unit | `#[cfg(test)] mod tests` at the bottom of the file, or `src/foo/tests.rs` via `#[cfg(test)] mod tests;` | private items | part of the lib test binary |
| integration | `tests/` | public API only | **one binary per top level file in `tests/`** |
| doc | `///` examples | public API | one binary per doc test (slow to build) |
| examples | `examples/*.rs` | public API | `cargo test` only builds them; `cargo test --examples` runs them |
| bench | `benches/` | public API | `cargo bench` |

Rules:

- **Integration tests are one crate:** `tests/it/main.rs` with `mod api; mod storage; mod support;` and files beside it. Every top level `tests/*.rs` file is a separate binary that relinks the whole library; consolidating Cargo's own tests cut compile time about 3x and disk use about 5x (matklad). Shared helpers become a normal module (`tests/it/support.rs`), not `tests/common/mod.rs` repeated in every file.
- **Large unit test modules go in their own file:** `#[cfg(test)] mod tests;` + `src/parser/tests.rs`. Editing tests then does not rebuild the non test library, and the source file stays readable.
- **Library with a public API:** test mostly through the public API (integration crate `tests/it`), so tests double as API usage feedback. **Internal crate in a workspace:** unit tests are enough; skip the integration binary.
- **Large internal workspaces:** consider `[lib] doctest = false` on crates whose docs are not user facing; doc tests are each linked separately and dominate test build time.
- Test data files live in `tests/data/` (or `tests/fixtures/`) and are located with `env!("CARGO_MANIFEST_DIR")`, never with a path relative to the current directory.

```rust
let path = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("tests/data/sample.json");
```

## 2. What to test, and at which boundary

- **Test features, not functions** (matklad). Tests at a stable boundary (public API, HTTP endpoint, CLI invocation) survive refactors; tests of private helpers break on every refactor and catch little.
- **Push IO to the edges** so the core is a pure function of data ("sans-io"): parse, decide, compute in pure code tested with plain values; one thin layer does the IO. Pure tests are fast and need no mocks.
- **Prefer real dependencies over mocks.** A real Postgres in a container, a real temp dir, a real HTTP server on `127.0.0.1:0`. Mock only what you cannot run (a third party payment API), and then with an HTTP level fake (`wiremock`) rather than a trait created only to be mocked.
- **Bug fix = failing test first.** Reproduce the bug as a test, watch it fail, fix, watch it pass.
- **Test the boundaries of every validated type:** the max length accepted, max + 1 rejected, empty, whitespace, each forbidden character (Zero To Production's `SubscriberName` tests).
- Error paths are behaviour: test that the right variant comes back, not only that "it is an error": `assert!(matches!(err, ParseError::UnexpectedEof { .. }))`.

## 3. Writing tests

- **One `check` helper per feature under test.** Tests call `check(input, expected)`; when the API changes, one function changes, not fifty tests (matklad).

```rust
#[track_caller] // failures point at the test line, not inside check()
fn check(input: &str, expected: &[Token]) {
    let actual = tokenize(input);
    assert_eq!(actual, expected, "input: {input:?}");
}

#[test]
fn numbers() { check("1 2", &[Token::Num(1), Token::Num(2)]); }
```

- Table driven tests for many small cases: a `&[(&str, Expected)]` array iterated in one test, with the case printed in the assert message.
- Tests may `unwrap()`/`expect()`; better, return `Result<(), Box<dyn std::error::Error>>` (or `anyhow::Result<()>`) and use `?`, which keeps the error chain in the failure output.
- `assert_eq!(actual, expected)` gives a diff; `assert!(a == b)` does not. For large structs use `pretty_assertions::assert_eq` or a snapshot.
- Name tests after the behaviour: `rejects_name_longer_than_256_graphemes`, not `test_parse_3`. No `test_` prefix inside a `tests` module (`clippy::redundant_test_prefix`, restriction).
- `#[should_panic(expected = "...")]` always with `expected`, otherwise any panic passes (`clippy::should_panic_without_expect`, pedantic).
- `#[ignore = "reason"]` with a reason (`clippy::ignore_without_reason`, pedantic). Slow tests are gated by an env var checked at the start of the test and run in CI, not silently ignored forever.
- No sleeps to wait for background work. Await the task, use a channel to signal, or poll a condition with a deadline. With tokio, `#[tokio::test(start_paused = true)]` (needs tokio's `test-util` feature in dev-dependencies) makes `sleep` and `timeout` instant and deterministic.
- Tests must be independent and parallel safe: unique temp dirs (`tempfile::tempdir()`), random free ports (`bind("127.0.0.1:0")`), one database per test (or a transaction rolled back). Never depend on test order or on a shared global.
- Tests that mutate process state (`std::env::set_var`, which is `unsafe` in the 2024 edition, or the current dir) are a race in the parallel runner. Pass config explicitly instead.

## 4. Snapshot tests with insta

Use for outputs that are large or tedious to write by hand: rendered text, error reports, ASTs, JSON responses, CLI output.

```rust
#[test]
fn renders_invoice() {
    let html = render(&sample_invoice());
    insta::assert_snapshot!(html);
}

#[test]
fn api_response_shape() {
    let resp = get_user(1);
    insta::assert_json_snapshot!(resp, { ".created_at" => "[timestamp]", ".id" => "[id]" });
}
```

- Workflow: run tests, then `cargo insta review` (or `cargo insta test --review`) to accept or reject. Commit the `.snap` files under `snapshots/`.
- In CI, insta never writes snapshots (`INSTA_UPDATE` defaults to `no` when `CI` is set), so a changed snapshot fails the build. Do not set `INSTA_UPDATE=always` in CI.
- Redact anything non deterministic (timestamps, ids, paths, durations) with selectors (`redactions` feature) or filters. A snapshot that changes on every run is worse than none.
- Inline snapshots (`assert_snapshot!(value, @"...")`) for short outputs, so the expectation sits in the test.
- Review snapshot diffs like code: accepting a wrong snapshot bakes the bug in.
- Speed up debug builds: `[profile.dev.package.insta] opt-level = 3` and the same for `similar`.

## 5. Property tests with proptest

Use for parsers, serializers, encoders, data structures, and any function with an invariant you can state.

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn roundtrip(value in any::<Config>()) {          // needs Arbitrary or a strategy
        let text = to_string(&value).unwrap();
        prop_assert_eq!(from_str(&text).unwrap(), value);
    }

    #[test]
    fn parse_never_panics(s in "\\PC{0,200}") {        // any printable text up to 200 chars
        let _ = parse(&s);
    }
}
```

- Properties worth writing: round trip (`decode(encode(x)) == x`), never panics on any input, idempotence (`normalize(normalize(x)) == normalize(x)`), equivalence to a simple reference implementation, invariants after every operation (sorted, balanced, length preserved).
- Commit the `proptest-regressions/` directory; it replays past failures. Copy an important shrunk failure into a plain unit test too.
- `prop_assert!`/`prop_assert_eq!` inside `proptest!` for cleaner shrinking output.
- Default is 256 cases; raise with `ProptestConfig::with_cases(..)` for critical code, or via `PROPTEST_CASES` in a nightly CI job.
- Exhaustive testing beats random testing when the domain is small (all `u8`, all 3 letter strings): just loop.

## 6. Async, IO and databases

- `#[tokio::test]` (current thread by default); `#[tokio::test(flavor = "multi_thread")]` only when the test needs real parallelism.
- Spawn the real app on a random port in a `spawn_app()` helper that returns its address and handles, and test with a real HTTP client (Zero To Production pattern). With axum, `tower::ServiceExt::oneshot` tests the router without a socket.
- Databases: `sqlx::test` creates a fresh database per test; otherwise create a uniquely named database or schema per test, or run each test inside a rolled back transaction.
- Keep test logs silent by default; print only when `TEST_LOG` is set.

## 7. Doc tests and examples

- Every public item in a library has a doc example that compiles and runs (C-EXAMPLE). Use `?` with a hidden `fn main() -> Result<..>`:

```rust
/// Parses a duration like `"5s"`.
///
/// ```
/// # fn main() -> Result<(), Box<dyn std::error::Error>> {
/// let d = mycrate::parse_duration("5s")?;
/// assert_eq!(d.as_secs(), 5);
/// # Ok(())
/// # }
/// ```
```

- `no_run` for examples that need a network or server; `compile_fail` to document misuse the type system prevents. Avoid `ignore`, which tests nothing.
- `examples/` programs are what users copy: no `unwrap()`, `main` returns `Result`. Run them in CI with `cargo test --examples` or `cargo run --example`.

## 8. Running tests: cargo test, nextest, CI

- `cargo test --workspace --all-features` locally and in CI; add `--no-default-features` and `cargo hack --each-feature` runs for libraries with features.
- `cargo nextest run` is faster on large suites (each test in its own process, better parallelism, retries for known flaky tests, slow test reporting). It does **not** run doc tests: run `cargo test --doc` as well.
- Flaky tests are bugs: fix or quarantine them with a tracking issue the same day. A retry setting is a stopgap, not a fix.
- Coverage: `cargo llvm-cov` (accurate, uses LLVM instrumentation). Use it to find untested branches in critical code, not as a percentage target.

## 9. Fuzzing and benchmarks

- **Fuzz every parser of untrusted input** (file formats, network protocols, user supplied text) with `cargo fuzz` (libFuzzer, nightly). A panic found by the fuzzer is a denial of service bug. Run it for minutes to hours before releases or on a schedule, not on every PR; keep the corpus.
- Structure aware fuzzing with the `arbitrary` crate when the input is a structured value rather than bytes.
- Benchmarks with `criterion` or `divan` on stable; wrap inputs in `std::hint::black_box`. Shared CI runners are too noisy for absolute numbers; compare against a baseline on the same machine, or use instruction count benchmarks (`iai-callgrind`) in CI.

## 10. Anti-patterns

| Anti-pattern | Fix |
|---|---|
| many `tests/*.rs` files | one `tests/it/main.rs` crate with modules |
| `tests/common/mod.rs` `mod common;` in each file | `tests/it/support.rs` module |
| trait created only so a mock can implement it | test with the real dependency or an HTTP fake |
| `assert!(result.is_ok())` | `result.unwrap()` or `?`, so the error is printed |
| `thread::sleep(100ms)` to wait for a task | await it, signal with a channel, or `start_paused` |
| snapshot containing timestamps or random ids | redactions |
| tests that only pass in order | independent setup per test |
| `#[ignore]` with no reason forever | gate with an env var and run in CI, or delete |
| test named `test1`, `it_works` | name the behaviour |

## 11. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Integration tests consolidated | at most one top level file or dir entry point in `tests/` (plus data dirs) | `ls tests/*.rs 2>/dev/null \| wc -l` is 0 or 1 |
| No sleeps in tests | zero | `rg -n 'thread::sleep\|time::sleep' tests src --glob '*test*'`, inspect hits |
| No result state asserts | zero warnings | `clippy::assertions_on_result_states` |
| should_panic has expected | zero warnings | `clippy::should_panic_without_expect` |
| ignore has reason | zero warnings | `clippy::ignore_without_reason` |
| Snapshots committed and clean | no `.snap.new` / `.pending-snap` files | `fd -e new -e pending-snap` (or `find . -name '*.snap.new' -o -name '*.pending-snap'`) |
| Proptest regressions committed | `proptest-regressions/` tracked | `git ls-files proptest-regressions` |
| Doc tests run | pass | `cargo test --doc` (separately if using nextest) |
| Examples run | pass | `cargo test --examples` |
| Parsers fuzzed | a `fuzz/` target exists for each untrusted input parser | `ls fuzz/fuzz_targets` |
| Tests do not use cwd relative paths | data paths built from `CARGO_MANIFEST_DIR` | `rg -n '"(\./)?tests/data' tests src` without `CARGO_MANIFEST_DIR` nearby |
