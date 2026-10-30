# The Rustonomicon (Rust project)

Official, free: https://doc.rust-lang.org/nomicon/

## What I read

Only the two chapters that decide when and how unsafe is acceptable: "How Safe and Unsafe Interact" and "Working with Unsafe". Not the rest of the book (layout, ownership internals, uninitialized memory, FFI chapter).

## Key lessons used in languages/rust/unsafe-and-ffi.md

- `unsafe` on a fn, trait or impl declares a contract; on a block it asserts the contract is upheld.
- Soundness: no safe client can cause undefined behaviour, whatever it does.
- Unsafe code may trust safe code it controls but not generic safe code supplied by clients (a broken `Ord` must not cause UB in `BTreeMap`); rely on an `unsafe trait` when correctness of the impl is needed for safety.
- Soundness is non local: safe code in the same module can break the invariants an unsafe block relies on (the `Vec::make_room` example). "The only bullet-proof way to limit the scope of unsafe code is at the module boundary with privacy."
