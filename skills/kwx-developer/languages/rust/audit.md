# Auditing a Rust codebase

A repeatable pass for finding structural problems and inconsistencies in an existing Rust project: the same thing done two ways in two places. Run the commands from the workspace root, collect the hits, and report each finding with its file, the convention the majority of the code follows, and the fix. Do not change code during an audit unless asked.

## Contents

1. Order of the pass
2. Machine checks first
3. Layout and module consistency
4. Visibility and API surface
5. Error handling consistency
6. Async and concurrency
7. Dependencies and manifests
8. Tests
9. Reporting
10. Checks

## 1. Order of the pass

1. Read `Cargo.toml` (root and members), `README`, `ARCHITECTURE.md` if present, and `cargo metadata --no-deps` to learn the crates and their roles.
2. Run the machine checks (section 2). Their output is objective and comes first in the report.
3. Run the consistency greps (sections 3 to 8). For each category, find the **majority convention** and list the outliers. A codebase that does something one way 40 times and another way 3 times has a 3 item fix list, not a style debate.
4. Read the hot spots: the largest files, the modules with the most `pub` items, the files with the most `unwrap`/`clone`/`unsafe`.

```sh
# biggest source files (candidates for splitting)
fd -e rs -E target -x wc -l {} | sort -rn | head -20
# densest unwrap / clone / unsafe users
rg -c '\.unwrap\(\)' --glob '!tests/**' -g '*.rs' | sort -t: -k2 -rn | head
rg -c '\.clone\(\)' -g '*.rs' | sort -t: -k2 -rn | head
rg -c 'unsafe' -g '*.rs' | sort -t: -k2 -rn | head
```

## 2. Machine checks first

```sh
cargo fmt --all --check
cargo clippy --workspace --all-targets --all-features -- -W clippy::pedantic 2>&1 | rg '^warning' | sort | uniq -c | sort -rn | head -40
cargo test --workspace --all-features
cargo tree -d                     # duplicate dependency versions
cargo deny check 2>&1 | tail -40  # if installed
cargo machete                     # unused dependencies, if installed
```

The `uniq -c` of clippy warnings shows which rules the codebase breaks systematically (a fix for the whole category) versus once (a local fix).

## 3. Layout and module consistency

```sh
# module file style: both present = inconsistent
find . -name mod.rs -path '*/src/*' -not -path '*/target/*'
# a foo.rs next to a foo/ directory (non-mod-rs style)
find src crates -type d -not -path '*/target/*' 2>/dev/null | while read -r d; do [ -f "$d.rs" ] && echo "$d.rs + $d/"; done
# junk drawer modules
fd -t f '^(utils?|helpers?|common|misc|shared)\.rs$' -E target
# inline modules that should be files (over ~50 lines is a judgement call)
rg -n '^\s*(pub(\(crate\))? )?mod \w+ \{' -g '*.rs' | rg -v 'mod tests'
# kind-based folders (models/services/handlers) vs feature folders
fd -t d '^(models|services|handlers|controllers|repositories|dto)$' -E target
# thin main?
wc -l src/main.rs src/bin/*.rs crates/*/src/main.rs 2>/dev/null
```

Findings to report: mixed `mod.rs` and `foo.rs`; `utils` modules (list what is inside and where each function belongs); kind folders in a feature organised codebase or vice versa; business logic in `main.rs`.

## 4. Visibility and API surface

```sh
# public modules in library roots
rg -n '^pub mod' crates/*/src/lib.rs src/lib.rs 2>/dev/null
# how items are exported: count each style per crate
rg -c '^pub fn' -g '*.rs'; rg -c '^pub\(crate\) fn' -g '*.rs'; rg -c '^pub\(super\) fn' -g '*.rs'
# re-export styles: crate root re-exports vs deep paths used by other crates
rg -n '^pub use' -g 'lib.rs'
rg -n 'use \w+::\w+::\w+::\w+' -g '*.rs' | rg -v '^.*use (std|core|alloc)::' | head -30
# glob imports of external crates
rg -n 'use [a-z_]+(::[a-z_]+)*::\*;' -g '*.rs' | rg -v 'super::\*|prelude::\*'
# mixed pub and private fields
cargo clippy -- -W clippy::partial_pub_fields 2>&1 | rg partial_pub
# getters with get_ prefix
rg -n 'fn get_\w+\(&self\)' -g '*.rs'
```

Report: crates where the same kind of item is `pub` in one module and `pub(crate)` in another with no API reason; other crates importing through deep internal paths instead of the root re-exports; `get_` getters; public internal modules.

## 5. Error handling consistency

```sh
# error crates per member: mixing thiserror, anyhow, snafu, eyre, hand impls
rg -n '^(thiserror|anyhow|snafu|eyre|color-eyre|failure)\b' crates/*/Cargo.toml Cargo.toml
rg -c 'impl (std::)?error::Error for|impl Error for' -g '*.rs'
# anyhow in library public signatures
rg -n 'pub (async )?fn .*anyhow::' -g '*.rs'
# stringly typed and unit errors
rg -n 'Result<[^,>]+, (String|&.static str|\(\))>' -g '*.rs'
rg -n 'Box<dyn (std::error::)?Error>' -g '*.rs' | rg -v 'Send'
# lossy conversions and silent drops
rg -n 'map_err\(\|_\|' -g '*.rs'
rg -n '\.ok\(\);|let _ = .*\?;|let _ = .*\.ok\(\)' -g '*.rs'
# messages: capitalised or trailing full stop
rg -n '#\[error\("[A-Z]' -g '*.rs'
rg -n '#\[error\("[^"]*\.\"' -g '*.rs'
# source printed twice
rg -n '#\[error\("[^"]*\{(0|source|e|err)\}' -g '*.rs'
# expect message style
rg -n '\.expect\("' -g '*.rs' | rg -v 'should' | head -20
# logging and returning the same error
rg -n -A2 '(error|warn)!\(' -g '*.rs' | rg 'return Err|\?;'
```

Report: one error library per role (the majority one), the outliers; library functions returning `anyhow`; every `map_err(|_|`; capitalised messages; expects without a "should" reason.

## 6. Async and concurrency

```sh
rg -n 'std::thread::sleep|thread::sleep' -g '*.rs'
rg -n 'std::fs::|std::net::|reqwest::blocking' -g '*.rs'      # check enclosing fn is not async
rg -n 'tokio::sync::Mutex' -g '*.rs'                            # justify each: is the guard held across an await on purpose?
rg -n '^\s*tokio::spawn\(' -g '*.rs'                            # handle dropped
rg -n 'unbounded_channel' -g '*.rs'
rg -n 'block_on|Runtime::new' -g '*.rs'
rg -n 'lazy_static!|once_cell::' -g '*.rs'                      # replace with std LazyLock/OnceLock
cargo clippy -- -W clippy::significant_drop_in_scrutinee -W clippy::future_not_send 2>&1 | rg '^warning' | sort | uniq -c
```

Report: blocking calls in async functions, `tokio::Mutex` used where a std mutex would do (or vice versa: std guard held across await, which clippy's `await_holding_lock` flags), fire and forget spawns, unbounded channels, two different lazy init mechanisms.

## 7. Dependencies and manifests

```sh
# same crate declared with different versions across members
rg -n '^(\w[\w-]*)\s*=\s*(\{[^}]*version\s*=\s*)?"[^"]+"' crates/*/Cargo.toml | \
  sed -E 's/^([^:]+):[0-9]+:([a-z0-9_-]+).*/\2 \1/' | sort | awk '{print $1}' | uniq -c | sort -rn | head
# members not inheriting workspace deps / lints / package fields
rg --files-without-match '^\[lints\]' crates/*/Cargo.toml
rg -n 'edition\s*=\s*"' crates/*/Cargo.toml                    # should be edition.workspace = true
# lint config in rustflags or source instead of the manifest
rg -n 'rustflags' .cargo/config.toml 2>/dev/null
rg -n '#!\[(deny|warn|allow)\(' -g 'lib.rs' -g 'main.rs'
# two crates doing the same job (pick one)
cargo tree -e normal --prefix none | sort -u | rg -n '^(chrono|time|jiff|log|tracing|reqwest|ureq|hyper|surf|serde_json|simd-json|rand|fastrand|lazy_static|once_cell|parking_lot|failure|anyhow|eyre) '
```

Report: version drift between members, members not using `workspace = true`, duplicate crates for one job (two time libraries, two HTTP clients, `log` and `tracing` both used directly), lints configured in three places.

## 8. Tests

```sh
ls tests/*.rs crates/*/tests/*.rs 2>/dev/null | wc -l           # >1 per crate: consolidate into tests/it
rg -n 'mod common;' -g 'tests/**'
rg -n 'thread::sleep|time::sleep' -g 'tests/**' -g '*test*.rs'
rg -n 'assert!\(\w+\.is_(ok|err)\(\)\)' -g '*.rs'
rg -n '#\[ignore\]' -g '*.rs'                                   # no reason given
rg -n '#\[should_panic\]' -g '*.rs'                             # no expected message
find . -name '*.snap.new' -o -name '*.pending-snap' | rg -v target
```

Report: integration test binaries to merge, sleeps, untestable logic in `main.rs`, missing tests for parsers of untrusted input (fuzz target candidates).

## 9. Reporting

For each finding:

- **What**: one sentence, plain words.
- **Where**: every file and line (or the command that lists them).
- **Majority convention**: what the rest of the codebase does, with a count ("37 modules use `foo.rs`, these 4 use `mod.rs`").
- **Fix**: the concrete change, and the lint or check that keeps it fixed (`clippy::mod_module_files`, a `disallowed-methods` entry, a CI step).
- **Risk**: whether the fix is mechanical (rename, move) or behavioural (changes error types, visibility of a published API, which is a semver break).

Rank by impact: correctness and security first (UB, panics on input, blocking in async, lost errors), then API and structure, then style. Prefer findings that come with a lint to keep them fixed.

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Every finding has a location | file:line or a command that lists them | review the report |
| Every finding names the majority convention | count included | review the report |
| Every recurring finding has a guard | a lint, clippy.toml entry or CI step proposed | review the report |
| Machine checks ran | fmt, clippy, test, tree -d outputs included | command outputs in the report |
| No changes made during the audit | clean working tree | `git status --porcelain` empty unless fixes were requested |
