# Rust reading list

Sources used for `languages/rust/`. "Read" means fetched and read for this work on 2026-10-30; "not read" means listed but not accessed.

## Official docs and guidelines (read)

- Rust API Guidelines, checklist and the Naming, Interoperability, Flexibility, Future proofing chapters: https://rust-lang.github.io/api-guidelines/checklist.html
- Clippy usage (lint groups, restriction advice, `CARGO_BUILD_WARNINGS=deny`): https://doc.rust-lang.org/clippy/usage.html
- Clippy configuration and `clippy.toml`: https://doc.rust-lang.org/clippy/configuration.html
- Clippy lint configuration keys (test allowances, thresholds, disallowed lists): https://doc.rust-lang.org/clippy/lint_configuration.html
- Clippy lint list and group membership: verified locally with `cargo clippy -- -W help` on clippy 0.1.98 (the web list is https://rust-lang.github.io/rust-clippy/master/)
- Cargo manifest (`[lints]`, priority, edition, publish): https://doc.rust-lang.org/cargo/reference/manifest.html
- Cargo features (additive, `dep:`, `?/`, unification, resolver 2, semver): https://doc.rust-lang.org/cargo/reference/features.html
- Cargo workspaces (virtual manifest, inheritance, `workspace.lints`): https://doc.rust-lang.org/cargo/reference/workspaces.html
- Cargo profiles (defaults, overrides, custom profiles): https://doc.rust-lang.org/cargo/reference/profiles.html
- Cargo `rust-version` and MSRV policy: https://doc.rust-lang.org/cargo/reference/rust-version.html
- Rust Book ch. 7.5, separating modules into files: https://doc.rust-lang.org/book/ch07-05-separating-modules-into-different-files.html
- `std::error::Error` docs (message style, source vs Display rule): https://doc.rust-lang.org/std/error/trait.Error.html
- `Result::expect` recommended message style: https://doc.rust-lang.org/std/result/enum.Result.html
- Rustonomicon, "How Safe and Unsafe Interact": https://doc.rust-lang.org/nomicon/safe-unsafe-meaning.html
- Rustonomicon, "Working with Unsafe": https://doc.rust-lang.org/nomicon/working-with-unsafe.html
- Rust 2024 edition guide (landing page only; details from prior knowledge, verified against rustc 1.98 lint list): https://doc.rust-lang.org/edition-guide/rust-2024/index.html
- Rust blog, async fn and RPIT in traits: https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/

## Tokio and async (read)

- Tokio tutorial, select (cancellation, pinning, preconditions): https://tokio.rs/tokio/tutorial/select
- `tokio::select!` API docs (cancel safety list, `biased`): https://docs.rs/tokio/latest/tokio/macro.select.html
- Tokio tutorial, shared state (std vs tokio Mutex, guards across await): https://tokio.rs/tokio/tutorial/shared-state
- Tokio graceful shutdown (CancellationToken, TaskTracker): https://tokio.rs/tokio/topics/shutdown
- `spawn_blocking` docs: https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html
- Alice Ryhl, "Async: What is blocking?": https://ryhl.io/blog/async-what-is-blocking/
- Rain (sunshowers), "Cancelling async Rust" (RustConf 2025, written version): https://sunshowers.io/posts/cancelling-async-rust/

## Errors (read)

- anyhow docs: https://docs.rs/anyhow/latest/anyhow/
- thiserror docs: https://docs.rs/thiserror/latest/thiserror/
- Luca Palmieri, "Error Handling In Rust: A Deep Dive": https://www.lpalmieri.com/posts/error-handling-rust/

## Books and long series (read, see sources/books/)

- Effective Rust (David Drysdale), 14 of 35 items: https://www.lurklurk.org/effective-rust/
- Rust Design Patterns, selected pages: https://rust-unofficial.github.io/patterns/
- Rust Performance Book, 6 chapters: https://nnethercote.github.io/perf-book/
- Zero To Production, free chapters 4 and 6: https://www.lpalmieri.com/posts/2020-09-27-zero-to-production-4-are-we-observable-yet/ and https://www.lpalmieri.com/posts/2020-12-11-zero-to-production-6-domain-modelling/

## Structure and testing (read)

- matklad, "Large Rust Workspaces": https://matklad.github.io/2021/08/22/large-rust-workspaces.html
- matklad, "ARCHITECTURE.md": https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html
- matklad, "Delete Cargo Integration Tests": https://matklad.github.io/2021/02/27/delete-cargo-integration-tests.html
- matklad, "How to Test": https://matklad.github.io/2021/05/31/how-to-test.html
- insta API docs: https://docs.rs/insta/latest/insta/
- proptest book, getting started: https://proptest-rs.github.io/proptest/proptest/getting-started.html

## Serde (read)

- Enum representations: https://serde.rs/enum-representations.html
- Container attributes: https://serde.rs/container-attrs.html
- Field attributes: https://serde.rs/field-attrs.html

## Tooling (read)

- cargo-deny config: https://embarkstudios.github.io/cargo-deny/checks/cfg.html
- cargo-udeps: https://github.com/est31/cargo-udeps
- cargo-machete: https://github.com/bnjbvr/cargo-machete
- cargo-hack: https://github.com/taiki-e/cargo-hack
- cargo-semver-checks: https://github.com/obi1kenobi/cargo-semver-checks
- Embark Studios standard lints (summary only): https://github.com/EmbarkStudios/rust-ecosystem/blob/main/lints.toml

## Not read

- Rust for Rustaceans (Jon Gjengset): the free sample chapter at https://nostarch.com/download/samples/RustforRustaceans_Ch1.pdf returned an HTML page instead of the PDF; the rest of the book is paid. No content from it is used.
- Jon Gjengset's "Crust of Rust" streams (video, not transcribed).
- nextest docs (https://nexte.st/docs/ returned 404); the nextest facts used (process per test, no doc tests) are from prior knowledge.
- Rust Book chapters on traits, smart pointers and concurrency, Rust Reference visibility chapter, Rust by Example: not fetched; the decisions taken from them are standard and were cross checked against Effective Rust and the API Guidelines.
- The full Clippy lint list web page (group membership was taken from the installed clippy instead).
