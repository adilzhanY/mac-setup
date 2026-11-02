# Rust Fuzz Book (cargo-fuzz chapters)

- Author: rust-fuzz project
- Year: living documentation, read 2026-10-31 (cargo-fuzz 0.13.2)
- Legal URL: https://rust-fuzz.github.io/book/cargo-fuzz/setup.html ; https://rust-fuzz.github.io/book/cargo-fuzz/tutorial.html

## What I read

Setup and tutorial chapters.

## Key lessons used in backend/fuzzing.md

- `cargo install cargo-fuzz`; nightly is required because of `-Z` flags for sanitizers.
- `cargo fuzz init` creates `fuzz/`; commit it. `cargo fuzz list`, `cargo fuzz run <target>`.
- Targets in `fuzz/fuzz_targets/<name>.rs` with `fuzz_target!`; crashes written under `fuzz/artifacts/`.
- Structure aware fuzzing with `arbitrary` (chapter linked from the book).
