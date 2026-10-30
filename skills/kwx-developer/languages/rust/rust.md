# Rust: the rules that matter most, and where to read more

Master file for Rust work. Read it first on any Rust task, then open only the topic file the task needs. Every rule here is the short form; the topic file has the reason, examples and the full check.

## Contents

1. The 20 rules
2. Router: which file to read
3. Defaults when the user did not say
4. Checks

## 1. The 20 rules

Each rule names the topic file that owns it.

1. **Library errors are typed enums, application errors are `anyhow`.** A library (or any module whose callers branch on the failure) returns `thiserror` enums. A binary's top level, CLI glue and request handlers use `anyhow::Result` with `.context(...)`. Never put `anyhow::Error` in a public library signature. (errors.md)
2. **Wrap a source error in `source()` or in the message, never both.** `#[error("read config {path}")] Io { path: PathBuf, #[source] source: io::Error }`. Writing `{0}` or `{source}` in the message of a variant that also has `#[source]`/`#[from]` prints the cause twice in every report. (errors.md)
3. **No `unwrap()` outside tests and examples you never ship. `expect("... should ...")` only for a real invariant.** The message states why the value is present ("config is validated in `load`, so `port` should be set"). Enforced by `clippy::unwrap_used`. (errors.md, tooling-and-lints.md)
4. **Log an error once, where it is handled, never where it is propagated.** A function that returns `Err` with `?` adds context, it does not also `tracing::error!`. (errors.md)
5. **Everything is private until a caller outside the module needs it, and then it gets the narrowest visibility that works:** private, `pub(super)`, `pub(crate)`, `pub`. In a library, enable `unreachable_pub` so a `pub` item that is not reachable from the crate root is flagged. (modules-and-visibility.md)
6. **Module files use `foo.rs` + `foo/bar.rs`, never `foo/mod.rs`, and one crate uses one style.** Enforced by `clippy::mod_module_files`. (modules-and-visibility.md)
7. **The public API is shaped in `lib.rs` with `pub use`, not by making internal module paths public.** Internal modules stay `mod x;` (private), the crate root re-exports the types users need. (modules-and-visibility.md)
8. **Validate at construction, then trust the type.** A value with an invariant is a newtype with a private field and a fallible `parse`/`new` (or `TryFrom`). Functions take `EmailAddress`, not `&str` they re-check. (api-design.md)
9. **Arguments borrow the most general form; storage owns.** Take `&str`, `&[T]`, `&Path`, `impl AsRef<Path>`, `impl IntoIterator`; never `&String`, `&Vec<T>`, `&Box<T>`. If the function stores the value, take it by value (`String`) and let the caller decide whether to clone. (api-design.md, ownership-and-performance.md)
10. **No `bool` or `Option` parameters that change behaviour; no out parameters.** Use an enum (`Overwrite::Yes`) or a builder. Return values, including tuples or structs, instead of filling `&mut` arguments. (api-design.md)
11. **Every public type implements `Debug`; data types derive the common traits they can** (`Clone, PartialEq, Eq, Hash, Default`, `PartialOrd, Ord` when ordering is meaningful). Public error types are `Send + Sync + 'static`. (api-design.md)
12. **A `.clone()` that only exists to silence the borrow checker is a defect.** Restructure (split borrows, `mem::take`, scope the borrow, pass ownership) first. `Arc::clone(&x)` is written that way so cheap clones are visible. (ownership-and-performance.md)
13. **Do not allocate in loops you can hoist out of.** `Vec::with_capacity` when the size is known, reuse a buffer with `clear()`, do not `collect()` only to iterate again. Measure before anything fancier. (ownership-and-performance.md)
14. **Never block an async executor thread.** No `std::thread::sleep`, blocking file or network IO, or CPU work longer than about 100 microseconds between `.await` points. Use `spawn_blocking` for blocking IO, rayon or a dedicated thread for CPU work. (async-and-concurrency.md)
15. **Never hold a lock guard across `.await`.** Use `std::sync::Mutex` (or parking_lot) for short critical sections inside non-async methods; `tokio::sync::Mutex` only when the guard must live across an await. (async-and-concurrency.md)
16. **Every future inside `select!`, `timeout` or `try_join!` must be cancel safe, or be moved into a spawned task.** `read_exact`, `write_all`, `Mutex::lock` and a half-finished multi-step update are not. (async-and-concurrency.md)
17. **Every `unsafe` block has a `// SAFETY:` comment, the smallest scope, and lives in a small private module that upholds the invariant.** Crates with no need for unsafe set `unsafe_code = "forbid"`. (unsafe-and-ffi.md)
18. **Lints live in `Cargo.toml` `[lints]` (or `[workspace.lints]`), not in `#![deny(warnings)]`.** CI fails on warnings through `CARGO_BUILD_WARNINGS=deny` or `-D warnings`. Suppress a lint with `#[expect(lint, reason = "...")]`, never a bare `#[allow]`. (tooling-and-lints.md)
19. **Unit tests sit next to the code in `#[cfg(test)] mod tests`; integration tests are one crate, `tests/it/main.rs`, not one binary per file.** Snapshot tests (insta) for large outputs, proptest for parsers and invariants. (testing.md)
20. **Features are additive and named after what they add (`serde`, `std`), never `no-x` or `with-x`.** Test the feature combinations with `cargo hack --each-feature`. Workspaces share versions through `[workspace.dependencies]`. (tooling-and-lints.md)

## 2. Router: which file to read

| File | What is in it | Read when |
|---|---|---|
| `modules-and-visibility.md` | crate and module layout, file style, `pub(crate)`, re-exports, imports, naming, where functions live, workspace layout | creating files or modules, deciding where code goes, making something `pub`, auditing structure |
| `errors.md` | thiserror vs anyhow by intent, error enum design, context, Display and source rules, panics, logging errors, HTTP mapping | any function that can fail, any new error type, reviewing `unwrap` or `map_err` |
| `api-design.md` | the API Guidelines checklist turned into rules: naming, conversions, traits to implement, newtypes, builders, generics vs `dyn`, sealed traits, future proofing, docs | designing a public function, struct, trait or crate API, or reviewing one |
| `serde.md` | serde attribute conventions, enum representations, config structs, untrusted input | adding `Serialize`/`Deserialize`, reading config or JSON, designing a wire format |
| `ownership-and-performance.md` | borrow vs own, clone discipline, smart pointer choice, allocation, iterators, collections, type sizes, release profiles, profiling | the borrow checker fights back, a hot path, a "make it faster" request |
| `async-and-concurrency.md` | blocking in async, locks, cancellation safety, `select!`, shutdown, task structure, async traits, threads and channels | any tokio or async code, any `Mutex`, `Arc`, channel or thread |
| `testing.md` | unit and integration layout, test helpers, insta, proptest, doc tests, nextest, fuzzing, benchmarks | writing or organising tests, fixing a bug (write the failing test first) |
| `tooling-and-lints.md` | the recommended `[lints]` block, `clippy.toml`, `rustfmt`, `deny.toml`, CI commands, profiles, features, MSRV, workspaces | setting up a crate or workspace, CI, adding a dependency, a feature or a lint |
| `unsafe-and-ffi.md` | when unsafe is acceptable, SAFETY comments, module containment, Miri, 2024 edition unsafe changes, FFI boundaries | any `unsafe`, `extern`, raw pointer, `transmute`, `static mut`, C interop |
| `audit.md` | commands that find inconsistency and structural problems in an existing Rust codebase | asked to review, audit or clean up a Rust project, or before a large refactor |

## 3. Defaults when the user did not say

- Edition `2024`, `rust-version` set to the oldest toolchain you actually test in CI (for an app: the current stable minus nothing; for a library: about 6 months back).
- Async runtime: tokio. HTTP server: axum. HTTP client: reqwest. Serialization: serde. Logging: `tracing` + `tracing-subscriber` with `EnvFilter`. CLI: clap with derive. Errors: thiserror + anyhow (see errors.md). Tests: built-in + insta + proptest. Follow the project's existing choice over these defaults.
- New crate in an existing workspace: inherit `version`, `edition`, `rust-version`, `license` from `[workspace.package]`, dependencies from `[workspace.dependencies]`, lints with `[lints] workspace = true`.
- Before claiming done: `cargo fmt --check`, `cargo clippy --all-targets --all-features`, `cargo test --all-features` (plus `cargo test --doc` if using nextest). All clean.

## 4. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Builds clean with lints | zero warnings | `CARGO_BUILD_WARNINGS=deny cargo clippy --all-targets --all-features` (Cargo 1.97+), else `cargo clippy --all-targets --all-features -- -D warnings` |
| Formatted | no diff | `cargo fmt --all --check` |
| Tests pass | exit 0 | `cargo test --all-features --workspace` |
| No unwrap in shipped code | no hits outside tests | `clippy::unwrap_used` enabled with `allow-unwrap-in-tests = true`; quick grep `rg -n '\.unwrap\(\)' --glob '!tests/**' src` |
| No `mod.rs` | none | `find . -name mod.rs -path '*/src/*' -not -path './target/*'` |
| No blanket deny | none | `rg -n '#!\[deny\(warnings\)\]'` |
| Every unsafe block justified | each `unsafe {` has `// SAFETY:` above | `clippy::undocumented_unsafe_blocks` |
| Lints configured in manifest | `[lints]` or `[workspace.lints]` present | `rg -n '^\[(workspace\.)?lints' Cargo.toml` |
| Dependency hygiene | no advisories, no banned licenses | `cargo deny check` |
