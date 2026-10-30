# Errors and panics

How to design, propagate, report and log errors in Rust. The common model failures: `anyhow` in a library API, `Box<dyn Error>` everywhere, `map_err(|_| ...)` that throws away the cause, the cause printed twice, the same error logged at every layer, and `unwrap()` in request paths.

## Contents

1. Decide by intent: enum or opaque
2. Designing an error enum with thiserror
3. Display and source: the two rules
4. Adding context
5. Application errors with anyhow
6. Converting at layer boundaries
7. Who logs, and how
8. Panics: when they are allowed
9. Option and Result style
10. Anti-patterns
11. Checks

## 1. Decide by intent: enum or opaque

Ask one question: **will the caller do something different depending on which failure happened?** (Luca Palmieri, "Error Handling in Rust".)

| Answer | Error type | Tool |
|---|---|---|
| Yes: retry on timeout, 404 on not found, re-prompt on bad input | an enum with one variant per decision the caller makes | `thiserror` |
| No: it will only be reported to a human or a log | opaque | `anyhow::Error` (applications), or a private enum behind an opaque public struct (libraries) |

Defaults that follow:

- **Library crate public API:** always a concrete type (enum or opaque struct) implementing `std::error::Error + Send + Sync + 'static`. Never `anyhow::Error`, never `Box<dyn Error>` without `Send + Sync`, never `String`, never `()` (C-GOOD-ERR).
- **Binary crate:** `anyhow::Result<T>` in `main`, CLI commands, startup and glue; typed enums only in the modules where some caller matches on them.
- **Web handler:** a handler error enum with a `Validation(..)`-style variant per client error the client must see, plus `#[error(transparent)] Unexpected(#[from] anyhow::Error)` for everything that becomes a 500.

The slogan "thiserror for libraries, anyhow for applications" is a decent approximation; the intent question above is the rule.

## 2. Designing an error enum with thiserror

```rust
use std::path::PathBuf;

#[derive(Debug, thiserror::Error)]
#[non_exhaustive] // public library enum that will grow
pub enum LoadConfigError {
    #[error("could not read config file {path}")]
    Read {
        path: PathBuf,
        #[source]
        source: std::io::Error,
    },
    #[error("config file {path} is not valid TOML")]
    Parse {
        path: PathBuf,
        #[source]
        source: toml::de::Error,
    },
    #[error("`port` must be between 1 and 65535, got {0}")]
    InvalidPort(u32),
}
```

Rules:

- **One variant per decision, not per dependency.** `Read` and `Parse` are different actions for the user. Two steps that both fail with `sqlx::Error` get two variants (`InsertUser`, `InsertToken`) so the message says which step failed; one `Database(#[from] sqlx::Error)` variant cannot.
- **Carry the data that makes the message actionable:** the path, the key, the id, the limit. "No such file or directory" with no path is the classic useless error.
- **`#[from]` only when the conversion is unambiguous.** `#[from] io::Error` is wrong as soon as two different steps can produce `io::Error`: `?` will silently pick the same variant for both. Use `#[source]` plus an explicit `.map_err(|source| LoadConfigError::Read { path: path.clone(), source })`.
- **Scope error types to a module or operation**, not one giant `crate::Error` with 40 variants that every function returns. A function's error type should list only failures that function can produce. A crate root `Error` that wraps the per module errors is fine for a library's top level API.
- **Name them verb-object-Error** (`ParseHeaderError`, `LoadConfigError`) per C-WORD-ORDER, or `module::Error` when the module is the namespace.
- **Keep the error small.** Box large payloads; `clippy::result_large_err` warns above 128 bytes because every `Result` carries the error's size.
- **`#[non_exhaustive]`** on public enums that will gain variants, so adding one is not a breaking change. Do not use it on internal enums: you want the compiler to make you handle the new variant.
- **Return the consumed argument on failure** when the caller may want to retry: `SendError(pub T)`, `String::from_utf8` returning the bytes in `FromUtf8Error` (Rust Design Patterns idiom).
- An opaque public library error that can still evolve:

```rust
#[derive(Debug, thiserror::Error)]
#[error(transparent)]
pub struct Error(#[from] ErrorKind); // public, opaque

#[derive(Debug, thiserror::Error)]
enum ErrorKind { /* private variants, free to change */ }

impl Error {
    pub fn is_not_found(&self) -> bool { matches!(self.0, ErrorKind::NotFound { .. }) }
}
```

## 3. Display and source: the two rules

From the `std::error::Error` docs:

1. **Messages are lowercase, concise, with no trailing punctuation.** `"invalid digit found in string"`, not `"Error: Invalid digit found in string."`. They get concatenated into chains ("load config: could not read config file x: permission denied"); capitals and full stops break the chain.
2. **A wrapped error is returned by `source()` or printed in the message, never both.**

```rust
// Bad: the io error text appears twice in any chain report
#[error("could not read {path}: {source}")]
Read { path: PathBuf, #[source] source: io::Error },

// Good: the message describes this layer, source() carries the cause
#[error("could not read {path}")]
Read { path: PathBuf, #[source] source: io::Error },

// Good: a pure pass-through layer adds nothing
#[error(transparent)]
Io(#[from] io::Error),
```

- `#[from]` implies `#[source]`. A field named `source` is a source automatically.
- Do not write `#[error("{0}")]` on a variant that wraps another error with `#[from]`; use `#[error(transparent)]` (forwards both `Display` and `source()`), or write a real message.
- `{path}` works for `Path`/`PathBuf` fields in thiserror (it calls `.display()` for you).
- Print a full chain at the top: `anyhow` does it with `{:#}` (one line, `: ` separated) or `{:?}` (multi line with "Caused by:"). For your own types, walk `source()`:

```rust
fn report(err: &dyn std::error::Error) -> String {
    let mut out = err.to_string();
    let mut cur = err.source();
    while let Some(cause) = cur {
        out.push_str(": ");
        out.push_str(&cause.to_string());
        cur = cause.source();
    }
    out
}
```

## 4. Adding context

- **Every `?` that crosses an IO, network, parse or process boundary in application code gets context** that says what was being attempted, with the identifying data:

```rust
use anyhow::Context;

let raw = std::fs::read_to_string(&path)
    .with_context(|| format!("reading config from {}", path.display()))?;
let cfg: Config = toml::from_str(&raw)
    .with_context(|| format!("parsing config from {}", path.display()))?;
```

- Use `.with_context(|| ...)` (lazy) when the message allocates, `.context("static text")` otherwise.
- Context describes the operation of this layer, not the cause ("reading config from x", not "file not found"). The cause is already in the chain.
- `.context()` also works on `Option`: `map.get(k).context("missing key `user`")?` turns `None` into an error with a message, instead of `unwrap()`.
- **Never `map_err(|_| ...)`.** It discards the cause, which is the most useful part of the report. Keep it as `#[source]` or use `.context`. Enforced by `clippy::map_err_ignore`.
- **Never `.ok()` a `Result` just to drop the error** (`let _ = x.ok();`, `if let Some(v) = fallible().ok()` with no logging). If ignoring is correct, say why: `if let Err(e) = flush() { tracing::warn!(error = %e, "flush failed, continuing"); }`. `clippy::unused_result_ok` flags the silent form.

## 5. Application errors with anyhow

- `fn main() -> anyhow::Result<()>` prints the chain with `Error: ...` and `Caused by:` and exits with code 1. For a custom exit code, `match run() { Err(e) => { eprintln!("error: {e:#}"); ExitCode::from(2) } .. }`.
- `anyhow::bail!("...")` for an early error return, `anyhow::ensure!(cond, "...")` for a checked precondition. Both are fine in applications; in library code return a typed error instead.
- To branch on a specific cause inside an `anyhow::Error`, `err.downcast_ref::<MyError>()`. If you do this in more than one place, the error should have been typed.
- Backtraces: captured when `RUST_BACKTRACE=1` or `RUST_LIB_BACKTRACE=1` is set (Rust 1.65+). Set `RUST_LIB_BACKTRACE=0` in production if capture cost matters on hot error paths.

## 6. Converting at layer boundaries

- Lower layers do not know about upper layers. A repository function returns `StoreError`, not an HTTP status. Map to HTTP once, on the handler's error type:

```rust
impl axum::response::IntoResponse for ApiError {
    fn into_response(self) -> axum::response::Response {
        use axum::http::StatusCode;
        let status = match &self {
            ApiError::Validation(_) => StatusCode::BAD_REQUEST,
            ApiError::NotFound => StatusCode::NOT_FOUND,
            ApiError::Unexpected(_) => StatusCode::INTERNAL_SERVER_ERROR,
        };
        if status.is_server_error() {
            tracing::error!(error = ?self, "request failed"); // the one log, at the edge
            return status.into_response(); // no internals in the body
        }
        (status, self.to_string()).into_response()
    }
}
```

- The client gets only what it can act on. A 500 body does not contain SQL, paths, stack traces or the `Debug` of an internal error.
- Do not implement a framework trait (`IntoResponse`, `ResponseError`) for a low level error like `sqlx::Error`; the mapping then leaks into every layer and every `?` becomes an implicit HTTP decision.

## 7. Who logs, and how

- **Log where the error is handled, not where it is propagated.** A function that returns the error with `?` does not log it; it adds context. Logging at every layer produces five copies of one failure.
- Log with the full chain and as a structured field: `tracing::error!(error = ?err, user_id = %id, "charge failed")`. `?` (Debug) on an `anyhow::Error` prints the chain; `%` (Display) prints only the top message.
- Every `let _ = ...` on a `Result` or `#[must_use]` value is either removed or replaced with an explicit, commented ignore. `clippy::let_underscore_must_use` and rustc's `let_underscore_drop` help.

## 8. Panics: when they are allowed

A panic is for bugs (a broken invariant inside your own code), not for bad input, missing files, network failure or anything a user can cause.

Allowed:

- Tests, benches, build scripts, and examples' `main` if they are not copied by users (examples users copy should return `Result` and use `?`).
- Startup in a binary before serving anything, when there is no sensible recovery: `let cfg = load().expect("config should be valid at startup");` (still better as `main() -> anyhow::Result` with context).
- An invariant the code itself guarantees, with an `expect` message phrased as "should": `self.items.last().expect("items is non-empty after push")`. The std docs recommend this "should" style because the message then reads as the violated assumption.
- A paired API: a panicking convenience and a fallible version (`Vec::remove` vs `get`), with the panic documented in a `# Panics` doc section (`clippy::missing_panics_doc`).

Not allowed:

- `unwrap()` on anything derived from input, config, environment, IO, network, user data or another thread (`mutex.lock().unwrap()` is the one common tolerated exception: poisoning means another thread already panicked).
- Implicit panics on untrusted input: slice indexing `buf[i]`, `&s[a..b]` on a non char boundary, integer division by a value from input, `as` casts that wrap. Use `get`, `checked_*`, `TryFrom`. For parsers of untrusted data, enable `clippy::indexing_slicing` and `clippy::arithmetic_side_effects` in that module.
- `panic!` inside `Drop` or across an FFI boundary (unsafe-and-ffi.md).
- Relying on `catch_unwind` as exception handling. It does nothing when `panic = "abort"` and on targets that always abort; use it only to stop panics at FFI or thread pool boundaries.
- `todo!()`, `unimplemented!()`, `dbg!()` in committed code (`clippy::todo`, `clippy::unimplemented`, `clippy::dbg_macro`).
- In request handling servers, one panic can take down a worker; return errors.

## 9. Option and Result style

- Prefer combinators and `?` over nested `match` for plain plumbing: `opt.map(..)`, `.ok_or_else(..)`, `.and_then(..)`, `.unwrap_or_default()`, `let Some(x) = opt else { return ... };` (`let else`, `clippy::manual_let_else` in pedantic). Use `match` when each arm does real work.
- `Option<T>` means "absent is normal". If absence is an error the caller should hear about, return `Result`.
- Do not return `Result<Option<T>, E>` and `Option<Result<T, E>>` interchangeably in one codebase; `Result<Option<T>, E>` ("lookup can fail, and the thing may not exist") is the usual one.
- `assert!(result.is_ok())` in tests hides the error; use `result.unwrap()` or `assert_eq!(result, Ok(..))` (`clippy::assertions_on_result_states`).

## 10. Anti-patterns

| Anti-pattern | Fix |
|---|---|
| `pub fn f() -> anyhow::Result<T>` in a library | typed enum or opaque struct error |
| `Result<T, String>` / `Result<T, ()>` | a real error type implementing `Error` |
| `Box<dyn Error>` without `+ Send + Sync + 'static` | add the bounds, or use `anyhow::Error` |
| `map_err(|_| MyError::Failed)` | keep the source: `map_err(MyError::Failed)` with `#[source]`, or `.context` |
| `#[error("x failed: {0}")] X(#[from] io::Error)` | `#[error("x failed")] X(#[source] io::Error)` or `#[error(transparent)]` |
| one `Database(#[from] sqlx::Error)` for every query | one variant per step |
| `tracing::error!` before `return Err(e)` | add context, log once at the edge |
| `.unwrap()` in handlers | `?` with a typed error |
| `expect("failed")` | `expect("<value> should <hold> because <reason>")` |
| error type with `Capitalized message.` | lowercase, no trailing punctuation |

## 11. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| No anyhow in library signatures | zero hits in `pub fn` of lib crates | `rg -n 'pub (async )?fn .*anyhow::' crates/*/src` (exclude bins) |
| No lossy map_err | zero hits | `clippy::map_err_ignore`; `rg -n 'map_err\(\|_\|'` |
| No double printed sources | no `{0}`/`{source}` in an `#[error]` on a variant with `#[from]` or `#[source]` | `rg -n -B1 -A3 '#\[error\("[^"]*\{(0|source)\}' src` and inspect |
| Messages lowercase, no trailing dot | all `#[error("...")]` | `rg -n '#\[error\("[A-Z]' src; rg -n '#\[error\("[^"]*\.\"\)' src` |
| No unwrap outside tests | zero warnings | `clippy::unwrap_used` with `allow-unwrap-in-tests = true` |
| No leftover todo/dbg | zero | `clippy::todo`, `clippy::dbg_macro`, `clippy::unimplemented` |
| Public errors are Send + Sync | compiles | `fn _assert<T: Send + Sync + 'static>() {} _assert::<MyError>();` in a test |
| Panics documented | every public fn that can panic has `# Panics` | `clippy::missing_panics_doc` (pedantic) |
| Error type size | no `result_large_err` warnings | default clippy |
| Log once | no `error!` immediately followed by `return Err` / `?` in the same block | `rg -n -A2 'error!\(' src \| rg 'return Err\|\?;'` and inspect |
