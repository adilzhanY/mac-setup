# Tooling, lints, Cargo and CI

The configuration a Rust project should have: lints in the manifest, `clippy.toml`, rustfmt, cargo-deny, unused dependency checks, features, MSRV, profiles and the CI command list. The lint block below was checked against clippy 0.1.98 (Rust 1.98): every lint name exists and the groups are correct.

## Contents

1. Lint policy
2. The recommended `[lints]` block
3. Library only additions
4. `clippy.toml`
5. Suppressing a lint
6. rustfmt
7. Dependencies: versions, lockfile, cargo-deny, unused deps
8. Features
9. MSRV and toolchain
10. CI command list
11. Checks

## 1. Lint policy

- **Lints are configured in `Cargo.toml`**, in `[lints]` (single crate) or `[workspace.lints]` with `[lints] workspace = true` in every member (Rust 1.74+). Not in `.cargo/config.toml` rustflags (that invalidates caches and is invisible to rust-analyzer) and not in a pile of `#![warn(..)]` attributes copied into every `lib.rs`.
- **Never `#![deny(warnings)]` in source** (Rust Design Patterns anti-pattern): a new compiler or clippy release then breaks every downstream build. Fail on warnings in CI only: `CARGO_BUILD_WARNINGS=deny` (Cargo 1.97+; also `[build] warnings = "deny"` in `.cargo/config.toml`) or, on older Cargo, `cargo clippy -- -D warnings`.
- **Groups get `priority = -1`** so that individual lint entries (priority 0) override them. Without it Cargo may order the group after the individual lint and the override silently does nothing.
- **Pedantic: on, with a few opt outs.** It is production ready by Clippy's own description (Clippy lints itself with it). **Nursery and restriction: never as whole groups**; restriction lints contradict each other by design. Pick individual lints, listed below with the reason for each.
- **Zero warnings policy.** A clean baseline makes every new warning visible (Effective Rust item 29). When a lint is wrong for a spot, use `#[expect(lint, reason = "...")]` there; when it is wrong for the project, turn it off in the manifest with a comment.

## 2. The recommended `[lints]` block

For a workspace root (for a single crate, drop `workspace.` from the table names):

```toml
[workspace.lints.rust]
unsafe_code = "deny"                 # forbid in crates that never need it (forbid cannot be overridden)
unsafe_op_in_unsafe_fn = "deny"      # each unsafe op in an unsafe fn needs its own unsafe block
rust_2018_idioms = { level = "warn", priority = -1 }
let_underscore_drop = "warn"         # `let _ = guard_or_value` drops immediately, usually a bug
unused_qualifications = "warn"
unused_lifetimes = "warn"
redundant_lifetimes = "warn"
unit_bindings = "warn"
trivial_numeric_casts = "warn"

[workspace.lints.clippy]
pedantic = { level = "warn", priority = -1 }
# pedantic opt outs: noisy, low value for most codebases
must_use_candidate = "allow"         # fires on nearly every pure fn; add #[must_use] by judgement
missing_errors_doc = "allow"         # keep "warn" in published libraries
missing_panics_doc = "allow"         # keep "warn" in published libraries

# nursery picks: high signal, low false positive rate
redundant_clone = "warn"             # clone of a value never used again
needless_collect = "warn"            # collect() then iterate again
or_fun_call = "warn"                 # unwrap_or(expensive()) evaluates eagerly
significant_drop_in_scrutinee = "warn"   # match on mutex.lock() holds the lock for the whole match
significant_drop_tightening = "warn"     # guard kept alive longer than needed
use_self = "warn"                    # `Self` inside impls, one spelling
derive_partial_eq_without_eq = "warn"
collection_is_never_read = "warn"
needless_pass_by_ref_mut = "warn"
trait_duplication_in_bounds = "warn"
type_repetition_in_bounds = "warn"
unused_peekable = "warn"
read_zero_byte_vec = "warn"
path_buf_push_overwrite = "warn"     # push("/abs") replaces the whole path
string_lit_as_bytes = "warn"
useless_let_if_seq = "warn"
iter_with_drain = "warn"
set_contains_or_insert = "warn"
debug_assert_with_mut_call = "warn"  # side effect disappears in release
unnecessary_struct_initialization = "warn"

# restriction picks: each one encodes a project rule
unwrap_used = "warn"                 # use ?, or expect("... should ...") for invariants
get_unwrap = "warn"
unwrap_in_result = "warn"            # a fn returning Result should not panic inside
panic = "warn"
todo = "warn"
unimplemented = "warn"
dbg_macro = "warn"
exit = "warn"                        # process::exit outside main skips destructors
mem_forget = "warn"
allow_attributes = "warn"            # use #[expect], which errors when the lint stops firing
allow_attributes_without_reason = "warn"
undocumented_unsafe_blocks = "warn"  # every unsafe block needs // SAFETY:
multiple_unsafe_ops_per_block = "warn"
clone_on_ref_ptr = "warn"            # Arc::clone(&x) so cheap clones are visible
rc_buffer = "warn"                   # Arc<str> not Arc<String>
rc_mutex = "warn"
map_err_ignore = "warn"              # map_err(|_| ..) drops the cause
unused_result_ok = "warn"            # `let _ = r.ok()` silently drops an error
try_err = "warn"
str_to_string = "warn"               # one spelling: to_owned()
lossy_float_literal = "warn"
verbose_file_reads = "warn"
infinite_loop = "warn"
rest_pat_in_fully_bound_structs = "warn"
empty_structs_with_brackets = "warn"
empty_enum_variants_with_brackets = "warn"
mod_module_files = "warn"            # foo.rs + foo/, never foo/mod.rs
renamed_function_params = "warn"     # trait impl keeps the trait's parameter names
same_name_method = "warn"
unnecessary_self_imports = "warn"
partial_pub_fields = "warn"          # all fields pub (plain data) or none
assertions_on_result_states = "warn"
tests_outside_test_module = "warn"
cfg_not_test = "warn"
```

Each member crate:

```toml
[lints]
workspace = true
```

A member cannot extend the workspace table, so per crate additions go as crate level attributes in that crate's `lib.rs` (next section).

Optional restriction lints for specific code, enabled per module with `#![warn(clippy::...)]`:

| Lint | Turn on for |
|---|---|
| `indexing_slicing`, `string_slice`, `arithmetic_side_effects` | parsers and decoders of untrusted input, money math |
| `as_conversions` | FFI and binary format code, to force `TryFrom` |
| `wildcard_enum_match_arm` | state machines where every new variant must be handled explicitly |
| `iter_over_hash_type` | code whose output must be deterministic |
| `print_stdout`, `print_stderr` | libraries (section 3) |
| `std_instead_of_core`, `std_instead_of_alloc` | `no_std` capable crates |
| `float_cmp_const` | numeric code |

## 3. Library only additions

At the top of each library's `lib.rs`:

```rust
#![warn(
    missing_docs,
    missing_debug_implementations,
    unreachable_pub,
    clippy::missing_errors_doc,
    clippy::missing_panics_doc,
    clippy::print_stdout,
    clippy::print_stderr,
    clippy::future_not_send, // async libraries: public futures must be Send
)]
```

For a published crate also enable the `cargo` group (metadata, wildcard versions, negative feature names) and allow `multiple_crate_versions`, which cargo-deny handles better:

```toml
[lints.clippy]
cargo = { level = "warn", priority = -1 }
multiple_crate_versions = "allow"
```

Do not enable `clippy::redundant_pub_crate` together with `unreachable_pub`; they demand opposite things.

## 4. `clippy.toml`

At the workspace root (Clippy searches upward from the manifest dir):

```toml
# tests may unwrap, panic, print and dbg
allow-unwrap-in-tests = true
allow-expect-in-tests = true
allow-panic-in-tests = true
allow-print-in-tests = true
allow-dbg-in-tests = true

# project bans; add a reason so the warning teaches the replacement
disallowed-methods = [
  { path = "std::thread::sleep", reason = "blocks the async runtime, use tokio::time::sleep" },
  { path = "std::env::set_var", reason = "racy and unsafe in edition 2024, pass config explicitly" },
]
disallowed-types = [
  # only if the project standardised on a faster hasher:
  # { path = "std::collections::HashMap", reason = "use FxHashMap", replacement = "rustc_hash::FxHashMap" },
]

# thresholds (defaults in brackets)
too-many-arguments-threshold = 6   # [7]
too-many-lines-threshold = 80      # [100], pedantic too_many_lines
```

- `msrv` is read from `rust-version` in `Cargo.toml`; do not repeat it here.
- `disallowed-methods`/`disallowed-types`/`disallowed-macros` are the cheapest way to turn a project convention ("we use `jiff`, not `chrono`") into a lint.

## 5. Suppressing a lint

```rust
#[expect(clippy::cast_possible_truncation, reason = "len is checked <= u16::MAX above")]
let n = len as u16;
```

- `#[expect]` (Rust 1.81+) instead of `#[allow]`: it warns when the lint no longer fires, so stale suppressions get cleaned up. Enforced by `clippy::allow_attributes`.
- Always a `reason` (`clippy::allow_attributes_without_reason`).
- On the smallest item (the expression's statement or the function), never `#![allow(...)]` at the crate root to silence a lint project wide; that belongs in the manifest with a comment.
- Generated code (`include!` from `OUT_DIR`, bindgen output) goes in its own module with one `#[allow(..)]` block at the module, plus a reason.

## 6. rustfmt

- Run `cargo fmt` and never hand format. CI runs `cargo fmt --all --check`.
- Keep `rustfmt.toml` empty or minimal: `edition` and `style_edition = "2024"` if needed. Unstable options (`imports_granularity`, `group_imports`) require nightly rustfmt; do not add them to a stable project, because contributors' formatters will disagree.
- Never mix formatting changes with logic changes in one commit.

## 7. Dependencies: versions, lockfile, cargo-deny, unused deps

- Version requirements: `serde = "1"` or `tokio = "1.38"` (caret, minimum you need). Never `"*"` (`clippy::wildcard_dependencies`), never `"=1.2.3"` pins in libraries (blocks security fixes and causes resolution conflicts downstream).
- **Commit `Cargo.lock` for everything** (the current Cargo guidance covers libraries too); in libraries, also test without it in CI (`cargo update` then test, or `cargo hack --version-range`/`-Z minimal-versions` on nightly) since users do not get your lockfile.
- Every dependency is build time, binary size, supply chain and maintenance cost. Before adding one for a few lines of code, write the few lines. Check `cargo tree -i <crate>` for why something is in the graph and `cargo tree -d` for duplicate versions.
- `default-features = false` and enable only the features you use on heavy dependencies (`tokio`, `reqwest`, `serde_json` are fine with defaults; `tokio = { features = ["full"] }` in a library is not).
- Workspace: every shared dependency is declared once in `[workspace.dependencies]` and members use `x.workspace = true`.
- **cargo-deny** in CI for advisories (RustSec), licenses, bans and sources. A starting `deny.toml`:

```toml
[graph]
all-features = true

[advisories]
ignore = []                      # every entry: advisory id + reason + date to revisit

[licenses]
allow = ["MIT", "Apache-2.0", "Apache-2.0 WITH LLVM-exception", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unicode-3.0", "Zlib"]
confidence-threshold = 0.9

[bans]
multiple-versions = "warn"       # "deny" once the graph is clean; use `skip` for known pairs
wildcards = "deny"
allow-wildcard-paths = true      # internal path deps without a version
deny = [
  # { crate = "openssl", reason = "use rustls" },
]

[sources]
unknown-registry = "deny"
unknown-git = "deny"
```

- **Unused dependencies:** `cargo machete` (stable, fast, heuristic; may false positive on macro only use, fix with `[package.metadata.cargo-machete] ignored = [...]`) in CI; `cargo +nightly udeps --all-targets` (precise, compiles) occasionally. `rustc`'s `unused_crate_dependencies` lint is noisy with dev dependencies; do not enable it globally.
- `cargo update` regularly (weekly bot: Dependabot or Renovate) so the lockfile does not rot.

## 8. Features

- **Additive only.** Enabling a feature never removes API or changes behaviour of existing API. Cargo unifies features across the whole graph, so any crate can turn yours on.
- Name a feature after what it adds: `serde`, `std`, `tls-rustls`. Never `no_std`, `no-x`, `with-x`, `use-x` (`clippy::negative_feature_names`, `redundant_feature_names`).
- `no_std` crates use `#![no_std]` plus a `std` feature (default on) that adds std only APIs.
- Use `dep:` in feature lists so optional dependencies do not create implicit features: `serde = ["dep:serde", "chrono?/serde"]` (`?` enables `chrono/serde` only if `chrono` is already enabled).
- Do not gate public struct fields or required trait methods behind features (another crate in the graph may enable the feature without your users knowing).
- Mutually exclusive features are a last resort; if unavoidable, `compile_error!` on the conflicting combination.
- Removing a feature, removing a feature from `default`, or moving existing API behind a feature is a breaking change.
- Test combinations: `cargo hack check --each-feature --no-dev-deps` on every PR; `cargo hack check --feature-powerset --depth 2` when features interact.
- Inspect what is on and why: `cargo tree -e features -i <crate>`.

## 9. MSRV and toolchain

- Set `rust-version` in `[package]` (or `[workspace.package]`). Cargo then errors clearly on older toolchains, `cargo add` picks compatible versions, the `incompatible_msrv` lint flags newer std APIs, and resolver 3 (default in edition 2024) prefers dependency versions compatible with it.
- Choose a policy and write it in the README: applications track latest stable; libraries typically support the last 6 to 12 months of stable releases. Raising MSRV is a minor version change, called out in release notes.
- Verify it in CI: `cargo hack check --rust-version --workspace --all-targets` (or `cargo +<msrv> check`). `cargo msrv find` discovers the real minimum.
- Applications pin the toolchain with `rust-toolchain.toml` (`channel = "1.98"`, `components = ["clippy", "rustfmt"]`) so local and CI agree; libraries usually do not pin.
- Workspaces: new crates use the latest edition (`2024`); upgrade old crates with `cargo fix --edition`.

## 10. CI command list

Order from fastest to slowest so failures come early:

```sh
cargo fmt --all --check
CARGO_BUILD_WARNINGS=deny cargo clippy --workspace --all-targets --all-features --locked
cargo test --workspace --all-features --locked            # or: cargo nextest run ... && cargo test --doc
cargo test --workspace --no-default-features --locked     # libraries with default features
RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --all-features
cargo hack check --each-feature --no-dev-deps             # crates with features
cargo hack check --rust-version --workspace --all-targets # libraries with an MSRV
cargo deny check
cargo machete
cargo semver-checks                                       # published libraries, before release
```

Scheduled (nightly or weekly), not per PR: `cargo +nightly udeps --all-targets`, `cargo +nightly miri test` for crates with unsafe, fuzzing, benchmarks against a baseline, `cargo update` + full test run.

- Use `--locked` so CI fails if `Cargo.lock` is out of date instead of silently resolving new versions.
- Cache `~/.cargo/registry` and `target/` keyed on `Cargo.lock` (for GitHub Actions, `Swatinem/rust-cache`).
- Generated files checked into the repo are regenerated in CI and diffed; any diff fails (Effective Rust item 32).

## 11. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Lints in manifest | `[lints]` or `[workspace.lints]` exists; members have `[lints] workspace = true` | `rg -n '^\[(workspace\.)?lints' Cargo.toml; rg --files-without-match '^\[lints\]' crates/*/Cargo.toml` (lists members missing it) |
| Groups have priority -1 | every group entry (`pedantic`, `nursery`, `cargo`, `rust_2018_idioms`, `all`) has `priority = -1` | `rg -n '^(pedantic\|nursery\|cargo\|all\|rust_2018_idioms)\s*=' Cargo.toml` and confirm `priority` |
| No restriction or nursery group wholesale | none | `rg -n '^(restriction\|nursery)\s*=' Cargo.toml` returns nothing |
| No blanket deny or allow in source | none | `rg -n '#!\[(deny\(warnings\)\|allow\(clippy::(all\|pedantic)\))'` |
| Suppressions use expect with reason | zero warnings | `clippy::allow_attributes`, `clippy::allow_attributes_without_reason` |
| Lint names valid | no `unknown lint` warnings | `cargo clippy 2>&1 \| rg 'unknown lint'` |
| clippy.toml test allowances | present when `unwrap_used` is on | `rg -n 'allow-unwrap-in-tests' clippy.toml` |
| Lockfile committed | tracked | `git ls-files Cargo.lock` |
| No wildcard versions | zero | `clippy::wildcard_dependencies`; `cargo deny check bans` |
| Advisories and licenses clean | exit 0 | `cargo deny check` |
| No unused deps | empty report | `cargo machete` |
| Features additive and tested | each feature builds alone | `cargo hack check --each-feature --no-dev-deps` |
| MSRV declared and tested | `rust-version` present; MSRV build passes | `rg -n 'rust-version' Cargo.toml`; `cargo hack check --rust-version` |
| Shared deps inherited | no member pins its own version of a crate listed in `[workspace.dependencies]` | `rg -n '^(serde\|tokio\|anyhow\|thiserror)\s*=\s*"' crates/*/Cargo.toml` |
