# Modules, visibility, layout and naming

How a Rust crate and workspace are laid out, what is visible to whom, and where a new function goes. Most of the "this codebase is inconsistent" findings in Rust come from this file.

## Contents

1. Crate layout
2. Module files: one style
3. Visibility: the ladder
4. The public API is shaped at the crate root
5. Imports
6. Where a function lives
7. Naming
8. Workspaces
9. Anti-patterns
10. Checks

## 1. Crate layout

- `src/lib.rs` holds the logic, `src/main.rs` is thin: parse args, build config, call the library, map the error to an exit code. A binary that is all `main.rs` cannot be integration tested and cannot be reused. Check: `main.rs` under about 100 lines and contains no business logic.
- `lib.rs` contains module declarations, `pub use` re-exports and crate docs. Real code lives in modules. Check: `lib.rs` has no function bodies longer than a few lines.
- Several binaries in one package go in `src/bin/<name>.rs` (or `src/bin/<name>/main.rs`), each one thin over the same library.
- Build automation (codegen, release, dist) goes in an `xtask` crate run as `cargo xtask <cmd>`, not in a growing `Makefile` of shell (matklad, "Large Rust Workspaces").
- Keep `src/` even for a single file crate; crates grow.

## 2. Module files: one style

Rust accepts two file layouts for module `net` with child `tcp`:

| Style | Files | Status |
|---|---|---|
| Non-mod-rs (use this) | `src/net.rs` + `src/net/tcp.rs` | idiomatic since the 2018 edition, the Book's default |
| mod-rs | `src/net/mod.rs` + `src/net/tcp.rs` | older, still compiles |

Rules:

- Use `net.rs` + `net/`. Many open tabs named `mod.rs` are indistinguishable, which is the Book's stated reason.
- One crate uses one style. A mix is the single most common layout inconsistency. Enforce with `clippy::mod_module_files = "warn"` (it flags every `mod.rs`). The opposite lint, `self_named_module_files`, enforces the other style; enable exactly one of them.
- Inline `mod x { ... }` blocks are for `#[cfg(test)] mod tests` and for tiny private helpers. A module over about 50 lines gets its own file.
- `#[path = "..."]` on a `mod` is a smell outside generated code. It hides where code lives.

## 3. Visibility: the ladder

Pick the lowest rung that compiles:

| Visibility | Visible to | Use for |
|---|---|---|
| (private) | this module and its children | default for everything |
| `pub(super)` | the parent module and its children | helpers a sibling module needs |
| `pub(in crate::a::b)` | the named ancestor module | rare; std uses it for iterator internals re-exported elsewhere |
| `pub(crate)` | the whole crate | crate internal API shared across modules |
| `pub` | everyone who can name the path | the crate's public API, and only if it is re-exported or reachable |

Rules:

- **Private by default.** Making a private item public later is a minor version change, making a public item private is a major one (Effective Rust item 22). Exposed helpers get depended on.
- **Struct fields are private** unless the struct is plain passive data with no invariant (a config DTO, a `#[repr(C)]` mirror). A struct with an invariant exposes getters and a fallible constructor (C-STRUCT-PRIVATE).
- **Do not mix public and private fields in one struct.** Either it is plain data (all `pub`) or it is encapsulated (none `pub`). Enforced by `clippy::partial_pub_fields`.
- **Library crates:** enable the rustc lint `unreachable_pub`. It flags `pub` items that are not reachable from outside the crate and suggests `pub(crate)`, so `pub` then means "public API" everywhere in the crate. Do not also enable `clippy::redundant_pub_crate`, which demands the opposite.
- **Binary crates:** nothing is reachable from outside, so pick one convention and hold it: either plain `pub` inside private modules everywhere, or `pub(crate)` everywhere. The audit finding is a mix of both in one crate.
- `pub enum` makes every variant and its fields public. If the enum will grow, mark it `#[non_exhaustive]` (cross crate only) or keep it private behind an accessor.
- A `pub trait` makes every method public; seal it (api-design.md) if outsiders must not implement it.

Good:

```rust
// src/lib.rs
mod parser;          // private module
mod store;

pub use parser::{parse, ParseError};   // the API, re-exported at the root
pub use store::Store;
```

```rust
// src/parser.rs
pub fn parse(input: &str) -> Result<Ast, ParseError> { /* ... */ }
pub(crate) fn tokenize(input: &str) -> Vec<Token> { /* ... */ } // used by store.rs too
fn skip_ws(input: &str) -> &str { /* ... */ }                    // private helper
```

Bad: `pub mod parser; pub mod store; pub mod util;` in `lib.rs`, with every helper `pub`. Users import `mycrate::util::internal_helper`, and every refactor is now a breaking change.

## 4. The public API is shaped at the crate root

- Users import from the crate root or from a small number of documented public modules. Internal module paths are not API.
- Re-export with `pub use` in `lib.rs`. One item, one public path: do not expose the same type at `crate::Foo` and `crate::foo::Foo` unless the second is a deliberate module for grouping.
- Re-export dependency crates whose types appear in your public API (`pub use http;`), so users name the exact version you compiled against instead of fighting "trait bound not satisfied" errors between two versions of the same crate (Effective Rust item 24). Better still, avoid putting a dependency's types in your API at all: it ties your semver to theirs.
- A `prelude` module is only for crates whose users import many traits at once. Most crates should not have one.
- `#[doc(hidden)] pub` is for items that must be public for macros and are not API. Never use it to hide sloppy visibility.

## 5. Imports

- **Functions:** import the parent module and call `module::function()` (`use std::fs; fs::read_to_string(..)`), so the call site shows where it comes from. **Types, traits, macros:** import the item itself (`use std::collections::HashMap;`). This is the Book's idiom (ch. 7.4).
- **No glob imports from crates you do not control** (`use some_crate::*`). A new item in their minor release can clash with yours (Effective Rust item 23). Allowed: `use super::*;` in `mod tests`, a crate's documented `prelude::*`, and `use MyEnum::*` inside a function body that matches on it. Enforce with `clippy::wildcard_imports` (in pedantic).
- `use crate::x::Y` for crate-internal paths, `super::` only for the direct parent. `super::super::` is a sign the module tree is too deep or the item lives in the wrong place.
- Group imports: std, external crates, `crate::`. `cargo fmt` sorts within groups; group separation is your job (or `group_imports = "StdExternalCrate"` on nightly rustfmt).
- Do not rename imports (`use foo::Bar as FooBar`) except to resolve a real name clash.

## 6. Where a function lives

Decision order for a new function:

1. **It has a clear receiver?** Make it a method on that type (C-METHOD): `invoice.total()`, not `compute_total(&invoice)`.
2. **It constructs a type?** An associated function on that type: `Config::from_env()`, `Invoice::parse(..)` (C-CTOR). Not a free `make_config()`.
3. **It converts between two types?** Implement `From`/`TryFrom`/`AsRef` on the more specific type (C-CONV-SPECIFIC), not a free `foo_to_bar()`.
4. **It is a helper used by one module?** Private free function at the bottom of that module.
5. **Used by several modules of the same feature?** `pub(crate)` in the feature module that owns the concept.
6. **Truly cross cutting?** A module named after the concept (`time.rs`, `retry.rs`), never `utils.rs`, `helpers.rs`, `common.rs` or `misc.rs`. A `utils` module becomes the place every unowned function goes, and nothing in it has a home.

Organise modules by feature or domain (`billing/`, `auth/`), not by kind (`models/`, `services/`, `handlers/`). Kind folders force every change to touch every folder.

Order inside a file: module docs, `use`, public types and their `impl`s, public functions, private helpers, `#[cfg(test)] mod tests` last. Keep a type's `impl` blocks next to the type; scattering `impl Foo` across files hides the API (`clippy::multiple_inherent_impl` flags it if you want it enforced).

## 7. Naming

From RFC 430 and the API Guidelines (C-CASE, C-CONV, C-GETTER, C-ITER, C-WORD-ORDER):

| Item | Convention | Example |
|---|---|---|
| crates | `snake_case` in code, kebab or snake in Cargo; no `-rs` or `rust-` | `serde_json` |
| modules, functions, locals | `snake_case` | `parse_header` |
| types, traits, variants | `UpperCamelCase`, acronyms as one word | `HttpClient`, `Uuid`, not `HTTPClient` |
| consts, statics | `SCREAMING_SNAKE_CASE` | `MAX_RETRIES` |
| type params, lifetimes | short | `T`, `K`, `'a`, `'de` |
| features | the thing added, no filler | `serde`, `std`, not `with-serde`, `use-std`, `no-std` |

- Conversions: `as_x` is free and borrowed to borrowed, `to_x` is expensive or borrowed to owned, `into_x` consumes `self`. `into_inner()` unwraps a wrapper.
- Getters have no `get_` prefix: `fn name(&self) -> &str`, `fn name_mut(&mut self)`. `get` alone is for "the one obvious thing" (`Cell::get`, map lookup).
- Iterators: `iter`, `iter_mut`, `into_iter`; their types are `Iter`, `IterMut`, `IntoIter`.
- One word order per crate, matching std: verb-object-Error (`ParseConfigError`, like `ParseIntError`).
- Do not repeat the module name in the item: `http::Client`, not `http::HttpClient` (`clippy::module_name_repetitions`, a restriction lint you may enable). Exception: the error type, where `crate::Error` is common and fine.
- Booleans read as predicates: `is_empty`, `has_children`, `can_retry`.

## 8. Workspaces

Use a workspace when you have more than one crate or a crate that takes more than about 30 seconds to rebuild incrementally.

- **Root is a virtual manifest** (only `[workspace]`, no `[package]`), with `resolver = "3"` set explicitly (a virtual manifest has no edition to infer it from).
- **Flat layout:** every crate in `crates/<crate-name>/`, `members = ["crates/*"]`. Folder name equals crate name exactly, no prefix stripping. Flat scales to hundreds of crates (rust-analyzer has 30+ in `crates/`); nested hierarchies do not, because Cargo's namespace is flat anyway.
- **Internal crates** set `publish = false` (and may use `version = "0.0.0"`). Crates you publish with a stable API go in a separate `libs/` folder, and nothing in `libs/` depends on `crates/`.
- **Shared metadata and versions:** `[workspace.package]` (edition, rust-version, license, repository), `[workspace.dependencies]` for every external crate used by more than one member, `[workspace.lints]` once. Members write `serde.workspace = true` and `[lints] workspace = true`. Features in a member's dependency are added to the workspace's features, not replacing them.
- **Profiles live only in the root manifest.** Profile settings in a member are ignored.
- **Split crates along dependency direction:** `core` (pure logic, no IO) at the bottom, adapters (db, http) above it, binaries on top. A lower crate never depends on a higher one; that is the architecture, and the crate graph enforces it for free.
- Write an `ARCHITECTURE.md` for any workspace over about 10k lines: bird's eye view, a codemap naming the crates and what each owns, and invariants stated as absences ("`core` does not depend on `tokio`").

## 9. Anti-patterns

| Anti-pattern | Why it hurts | Fix |
|---|---|---|
| `pub mod` everything in `lib.rs` | internal paths become API, every move is breaking | private `mod`, `pub use` at root |
| `utils.rs` / `helpers.rs` / `common.rs` | unowned junk drawer | name the module after the concept, or move the function to its single caller |
| mixed `mod.rs` and `foo.rs` | inconsistent navigation | one style, `clippy::mod_module_files` |
| mixed `pub` and `pub(crate)` for the same kind of item | readers cannot tell what is API | `unreachable_pub` in libs, one convention in bins |
| `Deref` to fake inheritance (`impl Deref for Manager { Target = Employee }`) | surprising, breaks generics, only single "inheritance" | composition with explicit delegate methods, or a trait (Rust Design Patterns anti-pattern) |
| `models/`, `services/`, `controllers/` folders | each feature change touches every folder | feature folders |
| re-declaring the same constant or helper in two modules | drift | one owner, `pub(crate)` |
| `super::super::super::thing` | tree too deep or item in the wrong place | move the item up, or `use crate::...` |

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| One module file style | no `mod.rs` (or no `foo.rs` + `foo/` if the project chose mod-rs) | `clippy::mod_module_files = "warn"`; `find . -name mod.rs -path '*/src/*' -not -path '*/target/*'` |
| No junk drawer modules | no `utils`, `helpers`, `common`, `misc` modules | `fd -t f '^(utils|helpers|common|misc)\.rs$' src; rg -n '^\s*(pub )?mod (utils|helpers|common|misc);'` |
| Library has no unreachable pub | zero `unreachable_pub` warnings | `[lints.rust] unreachable_pub = "warn"`, run clippy |
| No public internal modules in libs | `lib.rs` has `mod x;`, not `pub mod x;`, unless the module is a documented API grouping | `rg -n '^pub mod' src/lib.rs` and justify each hit |
| No glob imports of external crates | only `super::*` in tests, `prelude::*`, local enums | `clippy::wildcard_imports` (pedantic); `rg -n 'use [a-z_]+::.*\*;' src` |
| No mixed pub/private fields | zero hits | `clippy::partial_pub_fields` |
| No `get_` getters | none on simple accessors | `rg -n 'fn get_[a-z_]+\(&self\)' src` |
| Thin main | `main.rs` under ~100 lines, no domain logic | `wc -l src/main.rs src/bin/*.rs` |
| Workspace inheritance used | members use `.workspace = true` for shared deps and `[lints] workspace = true` | `rg -n 'workspace = true' crates/*/Cargo.toml`; flag a member that pins its own version of a dep the workspace declares |
| Flat workspace | all members one level under `crates/` | `cargo metadata --format-version 1 --no-deps \| jq -r '.packages[].manifest_path'` |
