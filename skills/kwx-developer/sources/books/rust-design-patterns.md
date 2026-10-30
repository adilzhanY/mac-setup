# Rust Design Patterns (rust-unofficial)

Free, community book: https://rust-unofficial.github.io/patterns/ (source: github.com/rust-unofficial/patterns).

## What I read

The full table of contents (SUMMARY.md), then the pages: anti-patterns "Clone to satisfy the borrow checker", "#[deny(warnings)]", "Deref polymorphism"; idioms "Use borrowed types for arguments", "mem::take/replace", "Return consumed argument on error", "Privacy for extensibility (non_exhaustive)"; patterns "Compose structs", "Contain unsafety in small modules", "Use custom traits to avoid complex type bounds".

## Key lessons used in languages/rust/

- A clone added to silence the borrow checker desynchronises two copies and costs an allocation; `Rc`/`Arc` clones are the exception; run clippy for needless clones. (ownership-and-performance.md)
- `#![deny(warnings)]` in source breaks builds on every new compiler or lint; set the policy in CI (`RUSTFLAGS="-D warnings"` or Cargo's warnings setting) or deny specific lints. (tooling-and-lints.md)
- `Deref` to emulate inheritance is surprising, breaks generic code and offers only single "inheritance"; use composition with explicit methods or traits. (modules-and-visibility.md, api-design.md)
- Take `&str`, `&[T]`, `&T` instead of `&String`, `&Vec<T>`, `&Box<T>`. (api-design.md)
- `mem::take`/`mem::replace` move owned data out of `&mut` without cloning. (ownership-and-performance.md)
- Return the consumed argument inside the error so callers can retry without cloning (`String::from_utf8` does this). (errors.md)
- `#[non_exhaustive]` only works across crates and makes users write wildcard arms; prefer a major version bump unless modelling something that changes outside your control. (api-design.md)
- Split large structs so fields can be borrowed independently. (ownership-and-performance.md)
- Put unsafe code in the smallest module that can uphold its invariants and build a safe interface on top. (unsafe-and-ffi.md)
