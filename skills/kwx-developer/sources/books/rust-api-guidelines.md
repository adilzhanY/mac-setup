# Rust API Guidelines (Rust library team)

Official, free: https://rust-lang.github.io/api-guidelines/ (checklist at /checklist.html).

## What I read

The full checklist (all IDs, 9 sections), and the full chapters on Naming, Interoperability, Flexibility and Future proofing.

## Key lessons used in languages/rust/

- Naming (C-CASE, C-CONV, C-GETTER, C-ITER, C-ITER-TY, C-FEATURE, C-WORD-ORDER): RFC 430 casing with acronyms as one word (`Uuid`); `as_` free borrowed to borrowed, `to_` expensive, `into_` consuming; no `get_` prefix; feature names without `use-`/`with-`/`no-`; verb-object-error order like `ParseIntError`. (modules-and-visibility.md section 7)
- Interoperability (C-COMMON-TRAITS, C-CONV-TRAITS, C-COLLECT, C-SERDE, C-SEND-SYNC, C-GOOD-ERR, C-NUM-FMT, C-RW-VALUE): derive the common traits eagerly because of the orphan rule; `Default` plus `new()`; serde behind a feature named exactly `serde`; assert `Send`/`Sync` in tests; errors are `Error + Send + Sync + 'static`, never `()`, messages lowercase without trailing punctuation; readers and writers by value. (api-design.md, serde.md, errors.md)
- Flexibility (C-INTERMEDIATE, C-CALLER-CONTROL, C-GENERIC, C-OBJECT): return intermediate results; take ownership only when needed and let the caller clone; accept `impl IntoIterator`, `AsRef<Path>`; decide object safety early. (api-design.md)
- Type safety (C-NEWTYPE, C-CUSTOM-TYPE, C-BITFLAG, C-BUILDER). (api-design.md)
- Predictability (C-SMART-PTR, C-CONV-SPECIFIC, C-METHOD, C-NO-OUT, C-OVERLOAD, C-DEREF, C-CTOR). (api-design.md, modules-and-visibility.md section 6)
- Dependability and debuggability (C-VALIDATE, C-DTOR-FAIL, C-DTOR-BLOCK, C-DEBUG, C-DEBUG-NONEMPTY). (api-design.md)
- Future proofing (C-SEALED pattern, C-STRUCT-PRIVATE, C-NEWTYPE-HIDE vs `impl Trait`, C-STRUCT-BOUNDS with its three exceptions). (api-design.md)
- Documentation (C-CRATE-DOC, C-EXAMPLE, C-QUESTION-MARK, C-FAILURE, C-LINK, C-METADATA, C-RELNOTES, C-HIDDEN) and necessities (C-STABLE, C-PERMISSIVE). (api-design.md)
