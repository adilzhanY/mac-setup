# API design

The Rust API Guidelines checklist (rust-lang.github.io/api-guidelines) turned into rules with defaults, plus the type design rules from Effective Rust and Zero To Production. Applies to every public item of a library and to the crate internal API of a large application. Naming lives in modules-and-visibility.md section 7.

## Contents

1. Make invalid states unrepresentable
2. Newtypes and parse, don't validate
3. Function signatures
4. Constructors and builders
5. Traits to implement (and derive)
6. Conversions
7. Generics, `impl Trait` and `dyn Trait`
8. Designing traits
9. Future proofing a public API
10. Documentation
11. Macros
12. Checks

## 1. Make invalid states unrepresentable

- Model states as an enum whose variants carry only the data valid in that state, not a struct of `Option`s and flags:

```rust
// Bad: four fields, many illegal combinations (connected with no socket, etc.)
struct Conn { connected: bool, socket: Option<TcpStream>, retry_at: Option<Instant>, error: Option<String> }

// Good
enum Conn {
    Connected { socket: TcpStream },
    Backoff { retry_at: Instant, last_error: io::Error },
    Closed,
}
```

- **No `bool` or `Option` parameters that select behaviour** (C-CUSTOM-TYPE). `copy(src, dst, true)` is unreadable at the call site; `copy(src, dst, Overwrite::Yes)` is not. Two or more bools in a signature or struct are flagged by `clippy::fn_params_excessive_bools` / `struct_excessive_bools` (pedantic).
- Sets of flags are `bitflags`, not an enum and not a `u32` with consts (C-BITFLAG).
- Typestate (a type parameter per state, `Request<Unsent>` -> `Request<Sent>`) is worth it only when misuse is costly and the state machine is small. Do not reach for it by default; an enum is usually enough.

## 2. Newtypes and parse, don't validate

- A value with an invariant gets a newtype with a **private field** and a **fallible constructor**. After construction the type is proof the check ran; nothing re-validates (Alexis King, "Parse, don't validate", applied in Zero To Production ch. 6).

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Email(String); // field private: only `parse` can build one

impl Email {
    pub fn parse(s: impl Into<String>) -> Result<Self, ParseEmailError> {
        let s = s.into();
        if !is_valid_email(&s) {
            return Err(ParseEmailError { input: s });
        }
        Ok(Self(s))
    }
}

impl AsRef<str> for Email {
    fn as_ref(&self) -> &str { &self.0 }
}
```

- Give read access with `AsRef<str>`/`as_str()`/`Deref` only for smart pointer like wrappers (see C-DEREF below). Never `&mut` access to the inner value: it lets callers break the invariant.
- Implement `FromStr` and/or `TryFrom<String>` when parsing from text is the natural entry point, so `"x@y.z".parse::<Email>()` and serde's `#[serde(try_from = "String")]` work.
- Use newtypes for units and ids that are easy to mix up: `UserId(u64)` vs `OrderId(u64)`, `Meters(f64)` vs `Feet(f64)` (C-NEWTYPE). The cost is zero at runtime.
- `parse` returns an error, never panics, on bad input.
- Newtypes also work around the orphan rule (implementing a foreign trait for a foreign type).

## 3. Function signatures

- **Borrow the most general form for inputs you only read:** `&str` not `&String`, `&[T]` not `&Vec<T>`, `&T` not `&Box<T>`, `&Path` not `&PathBuf` (Rust Design Patterns, "use borrowed types for arguments"; `clippy::ptr_arg` catches the first two).
- **Take ownership when you store it** (C-CALLER-CONTROL): `fn set_name(&mut self, name: String)`. Do not take `&str` and `.to_string()` inside; the caller may already own a `String` it no longer needs. `impl Into<String>` is acceptable for constructors where ergonomics matter.
- **Generic inputs where it costs nothing:** `impl AsRef<Path>` for paths (like `File::open`), `impl IntoIterator<Item = T>` instead of `&[T]` when you only iterate (C-GENERIC). Keep the generic shim thin and forward to a non-generic inner function to avoid monomorphization bloat:

```rust
pub fn load(path: impl AsRef<Path>) -> Result<Config, LoadConfigError> {
    load_inner(path.as_ref())
}
fn load_inner(path: &Path) -> Result<Config, LoadConfigError> { /* real body */ }
```

- **Readers and writers by value**: `fn write_to<W: Write>(w: W)`. Callers pass `&mut file` because `&mut W: Write` (C-RW-VALUE).
- **No out parameters** (C-NO-OUT): return a tuple or struct. The exception is a caller supplied buffer for reuse (`read(&mut buf)`), which is a performance API.
- **Return intermediate results** you computed anyway (C-INTERMEDIATE): `HashMap::insert` returns the old value, `binary_search` returns the insertion point on `Err`.
- **A method with a clear receiver is a method**, not a free function (C-METHOD).
- **Return `impl Iterator<Item = T>`** rather than `Vec<T>` when callers usually iterate once; return a `Vec` when they need to index, sort or store.
- **More than about 5 parameters** means a struct or builder. `clippy::too_many_arguments` fires at 7.
- **Mark functions whose result must be used:** `#[must_use]` on pure functions returning a new value and on builders (`clippy::must_use_candidate` is too noisy to enable globally; `clippy::return_self_not_must_use` in pedantic covers builders).

## 4. Constructors and builders

- Constructors are associated functions: `new`, `with_capacity`, `from_parts`, `open`, `connect` (C-CTOR). `new` takes the essential arguments only.
- If a no argument constructor makes sense, implement `Default` **and** `new()` (C-COMMON-TRAITS); `clippy::new_without_default` enforces it.
- **Builder** when there are several optional settings (C-BUILDER). Default to a consuming builder (`fn x(mut self, ..) -> Self`, like reqwest's `ClientBuilder`), which chains in one expression and can move owned resources into `build`. Use `&mut self` setters (like `std::process::Command`) when the builder is configured across several statements or reused to build many values. `build` returns `Result` if the combination can be invalid.

```rust
#[derive(Debug, Default)]
#[must_use]
pub struct ClientBuilder { timeout: Option<Duration>, retries: u32 }

impl ClientBuilder {
    pub fn timeout(mut self, t: Duration) -> Self { self.timeout = Some(t); self }
    pub fn retries(mut self, n: u32) -> Self { self.retries = n; self }
    pub fn build(self) -> Result<Client, BuildClientError> { /* validate, then construct */ }
}
```

- Do not write a builder for a struct with 3 required fields and nothing optional. A plain struct with public fields plus `..Default::default()` is a fine "builder" for passive config data.

## 5. Traits to implement (and derive)

- **Every public type implements `Debug`** (C-DEBUG); enforce with `missing_debug_implementations` in libraries. `Debug` output is never empty (C-DEBUG-NONEMPTY). Hand write `Debug` (or use `secrecy::SecretString`) for types holding secrets so tokens and passwords never reach logs.
- **Derive eagerly** the traits your users cannot add later because of the orphan rule (C-COMMON-TRAITS): `Clone`, `Copy` (small plain values only, it is a semver promise), `PartialEq`/`Eq`, `Hash`, `PartialOrd`/`Ord` when there is a natural order, `Default` when there is a natural empty value. `Display` for types that have a user facing text form.
- `PartialEq` derived on a type that could be `Eq` should derive `Eq` too (`clippy::derive_partial_eq_without_eq`).
- `Hash` and `Eq` must agree; `Ord` and `PartialOrd` must agree. Do not hand implement one and derive the other (`clippy::derived_hash_with_manual_eq`, `derive_ord_xor_partial_ord`).
- **`Send` and `Sync`** where possible (C-SEND-SYNC); add a compile time test so a refactor that adds an `Rc` field is caught:

```rust
#[test]
fn types_are_thread_safe() {
    fn assert_send_sync<T: Send + Sync>() {}
    assert_send_sync::<Client>();
}
```

- Collections implement `FromIterator` and `Extend` (C-COLLECT). Types that wrap binary numbers implement `LowerHex`, `UpperHex`, `Octal`, `Binary` (C-NUM-FMT).
- `serde::Serialize`/`Deserialize` for data types, behind an optional feature named exactly `serde` in libraries (C-SERDE); see serde.md.
- **`Deref` only for smart pointers** (C-DEREF). Implementing `Deref<Target = Inner>` on a domain wrapper to "inherit" methods is the Deref polymorphism anti-pattern. Smart pointers do not add inherent methods (C-SMART-PTR): `Arc::clone(&a)`, not `a.clone_arc()`.
- Operator overloads only where the meaning is unsurprising (C-OVERLOAD): `Add` for vectors and money, not for "append to a log".
- **Destructors never fail and never block** (C-DTOR-FAIL, C-DTOR-BLOCK). If cleanup can fail or block (flush, close a connection), provide an explicit `close(self) -> Result<..>` and keep `Drop` as a best effort fallback.

## 6. Conversions

- Conversions go through `From`, `TryFrom`, `AsRef`, `AsMut`, `FromStr` (C-CONV-TRAITS). Implement `From`, never `Into` directly (`clippy::from_over_into`); `Into` comes free.
- `From` is infallible and lossless. If it can fail or lose information, it is `TryFrom` or a named method. A `From` impl that panics is flagged by `clippy::fallible_impl_from` (nursery).
- Put the conversion method on the more specific type (C-CONV-SPECIFIC): `str::as_bytes` lives on `str`, not on `[u8]`, because every `str` is bytes but not every byte slice is a `str`. Likewise `Email::as_str`, `Email::into_string(self)` or `impl From<Email> for String` are right, while the reverse direction is `impl TryFrom<String> for Email` because it can fail.
- Numeric conversions: `u32::from(x)` / `u64::try_from(x)?` instead of `as`. `as` silently truncates, wraps and saturates. The pedantic `cast_possible_truncation`, `cast_sign_loss`, `cast_possible_wrap`, `cast_lossless` lints catch it.

## 7. Generics, `impl Trait` and `dyn Trait`

Default to generics; use `dyn` when one of its specific benefits is needed (Effective Rust item 12).

| Need | Choose |
|---|---|
| speed, several trait bounds at once, static types known at compile time | generics / `impl Trait` |
| heterogeneous collection (`Vec<Box<dyn Handler>>`) | `dyn Trait` |
| compile time or binary size matters more than a vtable call | `dyn Trait` |
| plugin loaded at runtime | `dyn Trait` |
| hiding a long iterator or closure type in a return | `impl Trait` (internal APIs) or a named newtype (public APIs that need `Clone`/`Debug` on the result, C-NEWTYPE-HIDE) |

- `impl Trait` in argument position cannot be turbofished by callers; if callers may need to name the type, use a named generic `<P: AsRef<Path>>`.
- Keep bounds on `impl` blocks and functions, not on the struct (C-STRUCT-BOUNDS): `struct Cache<K, V> { .. }` with `impl<K: Hash + Eq, V> Cache<K, V>`. Bounds on the struct spread to every user and adding one later is breaking. Exceptions: bounds needed by an associated type in a field, `?Sized`, or a `Drop` impl.
- When a bound list grows long and repeats, define a trait with a blanket impl (Rust Design Patterns, "use custom traits to avoid complex type bounds").

## 8. Designing traits

- Decide up front whether the trait is used as `dyn` (C-OBJECT). To be dyn compatible: no generic methods, no `Self` by value outside the receiver. Methods that break this get `where Self: Sized` so the rest of the trait still works as an object.
- **Small required surface, default methods for the rest** (Effective Rust item 13): `Iterator` needs only `next`.
- A trait with exactly one implementation and no test double is not an abstraction yet. Do not create a `UserRepository` trait for one Postgres struct "for testability"; test against the real thing or introduce the trait when the second implementation arrives.
- **Sealed traits** (C-SEALED) when outsiders may use but must not implement the trait, so you can add methods later without a breaking change:

```rust
pub trait Shape: private::Sealed {
    fn area(&self) -> f64;
}
mod private {
    pub trait Sealed {}
}
impl private::Sealed for Circle {}
impl Shape for Circle { fn area(&self) -> f64 { /* ... */ 0.0 } }
```

- `async fn` in a public trait: callers cannot add a `Send` bound to the returned future. Use the `trait-variant` crate (`#[trait_variant::make(Service: Send)]`) or write `fn call(&self) -> impl Future<Output = T> + Send`. For `dyn` use of an async trait, use the `async-trait` crate or return `Pin<Box<dyn Future<Output = T> + Send + '_>>`. See async-and-concurrency.md.

## 9. Future proofing a public API

- Private struct fields (C-STRUCT-PRIVATE). Public fields freeze the representation.
- `#[non_exhaustive]` on public enums and structs that will grow, when you cannot afford a major version for each addition. It forces a `_ =>` arm on users, so prefer a major bump for enums users must handle exhaustively (Rust Design Patterns, "privacy for extensibility").
- Seal traits you might extend.
- Wrap returned adapter chains in a newtype (C-NEWTYPE-HIDE) instead of exposing `Enumerate<Skip<I>>`.
- Do not expose a dependency's types unless you also re-export the dependency; prefer your own types at the boundary (Effective Rust item 24).
- Public dependencies of a 1.0 crate must themselves be 1.0 (C-STABLE).
- Check every release with `cargo semver-checks` (it catches removed items, changed signatures of many kinds; it does not catch every type change).
- Validate arguments (C-VALIDATE): prefer static enforcement (types), then dynamic checks returning `Result`, then `debug_assert!` only for checks too costly for release, documented.

## 10. Documentation

- Crate level `//!` docs in `lib.rs`: what the crate does, a minimal example, feature flags (C-CRATE-DOC).
- Every public item has a `///` doc with at least one sentence; enforce with `missing_docs = "warn"` in libraries.
- Examples use `?`, not `unwrap()` (C-QUESTION-MARK): a doc test can `fn main() -> Result<(), Box<dyn std::error::Error>>` hidden with `#` lines.
- Sections in this exact spelling (C-FAILURE): `# Errors` (when it returns `Err`, `clippy::missing_errors_doc`), `# Panics` (`clippy::missing_panics_doc`), `# Safety` for every `unsafe fn` (`clippy::missing_safety_doc`, default on).
- Link related items with intra-doc links: ``[`Client::send`]`` (C-LINK); `cargo doc` with `-D rustdoc::broken_intra_doc_links` in CI.
- `Cargo.toml` metadata complete for published crates: `description`, `license`, `repository`, `readme`, `keywords`, `categories`, `rust-version` (C-METADATA; `clippy::cargo_common_metadata`).
- Keep release notes (C-RELNOTES) and do not hand edit a generated changelog.

## 11. Macros

- Write a function or generic first; a macro only when the input cannot be expressed in types (repetitive impls for many types, a DSL, compile time format checking) (Effective Rust item 28).
- Macro input looks like the output it produces (C-EVOCATIVE); item macros accept attributes and visibility (C-MACRO-ATTR, C-MACRO-VIS) and work wherever items are allowed (C-ANYWHERE).
- Use `$crate::` paths inside `macro_rules!` so the macro works when the crate is renamed.
- A proc macro crate costs compile time for every downstream build; reach for `macro_rules!` first.

## 12. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| No `&String` / `&Vec` / `&Box` params | zero | `clippy::ptr_arg` (default), `clippy::borrowed_box` (default); `rg -n 'fn .*: &(String|Vec<|Box<)' src` |
| No bool flag params | at most one bool per fn and it is a plain value, not a mode | `clippy::fn_params_excessive_bools`; `rg -n 'fn \w+\([^)]*: bool[^)]*: bool' src` |
| Every public type is Debug | zero warnings | `missing_debug_implementations` |
| Eq derived with PartialEq where possible | zero warnings | `clippy::derive_partial_eq_without_eq` |
| From not Into | zero | `clippy::from_over_into` |
| new has Default | zero | `clippy::new_without_default` |
| No struct bounds that belong on impls | `rg -n 'struct \w+<[^>]*:' src` hits only the listed exceptions | manual review of hits |
| No Deref on non pointer types | each `impl Deref for` is a smart pointer or guard | `rg -n 'impl(<.*>)? (std::ops::)?Deref for' src` and inspect |
| Public items documented | zero warnings | `missing_docs`, `clippy::missing_errors_doc`, `clippy::missing_panics_doc` |
| Docs build with valid links | exit 0 | `RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --all-features` |
| Semver respected | no deny level findings | `cargo semver-checks` before publishing |
| Thread safety asserted | test compiles | `assert_send_sync::<T>()` test present for public types used across threads |
