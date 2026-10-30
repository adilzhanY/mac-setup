# Effective Rust (David Drysdale)

Legal free edition by the author: https://www.lurklurk.org/effective-rust/ (also effective-rust.com). Print edition: O'Reilly, 2024.

## What I read

Table of contents (35 items), then in full: item 4 (idiomatic Error types), 12 (generics vs trait objects), 16 (avoid writing unsafe), 17 (shared-state parallelism), 18 (don't panic), 22 (minimize visibility), 23 (avoid wildcard imports), 24 (re-export dependencies whose types appear in your API), 25 (manage your dependency graph), 26 (feature creep), 29 (listen to Clippy), 30 (write more than unit tests), 32 (CI), 34 (control what crosses FFI boundaries).

## Key lessons used in languages/rust/

- Errors: implement `Error`; a `String` cannot be an `Error` (orphan rule), wrap it in a newtype. Nested errors as an enum with `From` impls and `source()`. Libraries emit typed, detailed errors and never expose `anyhow`; applications use `anyhow`. (errors.md)
- Panics: fine if you control `main`; otherwise return `Result`. Offer a panicking and a fallible pair when useful. Hidden panics: slice indexing, division by zero. `catch_unwind` is not exception handling; use it at FFI boundaries only. Use CI to catch new panicking code. (errors.md)
- Visibility: private by default; private to public is a minor bump, public to private is major. `pub(crate)`, `pub(super)`, `pub(in path)`. (modules-and-visibility.md)
- Wildcard imports from crates you do not control can break on their minor releases; exceptions are `use super::*` in tests and curated preludes. (modules-and-visibility.md)
- Re-export a dependency whose types appear in your API, or avoid exposing them: it couples your semver to theirs. (modules-and-visibility.md, api-design.md)
- Dependencies: semver compatible requirements, not `=x.y.z` or `*`; commit lockfiles for binaries; `cargo tree --duplicates`, `--invert`, `--edges features`; cargo-deny and cargo-udeps in CI. (tooling-and-lints.md)
- Features: additive; do not gate public struct fields or required trait methods; feature unification means any crate can enable yours; 2^N combinations need CI coverage. (tooling-and-lints.md)
- Generics by default; trait objects for heterogeneous collections, code size, runtime loading. Object safety rules and `where Self: Sized`. (api-design.md)
- Shared state: one lock per consistent set of data, consistent lock order, never call callbacks or return guards while locked, prefer message passing. (async-and-concurrency.md)
- Clippy: zero warning baseline, read the full lint list, prefer a small refactor to arguing about false positives. (tooling-and-lints.md)
- Testing: unit, integration, doc tests, examples (`cargo test --examples`), benchmarks with `black_box`, fuzzing with cargo-fuzz for untrusted input; write the failing test before the bug fix. (testing.md)
- CI: fmt check, clippy with warnings as errors, all feature combinations, MSRV build, build without lockfile, `cargo doc`, udeps, deny, regenerate generated files and diff. (tooling-and-lints.md)
- Unsafe: avoid writing it; look in std and crates first; wrap, document, keep small, test more, run Miri. (unsafe-and-ffi.md)
- FFI: `#[repr(C)]`, sized types, bindgen, `CString`/`CStr`, allocate and free on the same side, wrap handles with `Drop`, no panics across the boundary, prefix exported symbols. (unsafe-and-ffi.md)
