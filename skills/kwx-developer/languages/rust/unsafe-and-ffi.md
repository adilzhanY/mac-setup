# Unsafe and FFI

When `unsafe` is acceptable, how to write and contain it, and how to cross a C boundary without undefined behaviour. Sources: the Rustonomicon ("How Safe and Unsafe Interact", "Working with Unsafe"), Effective Rust items 16, 34, 35, Rust Design Patterns (contain unsafety in small modules, FFI idioms), the Rust 2024 edition guide.

## Contents

1. When unsafe is acceptable
2. The soundness rule
3. Writing an unsafe block
4. Containing unsafe in a module
5. Unsafe functions and traits
6. Rust 2024 edition changes
7. Verifying unsafe code
8. FFI: calling C
9. FFI: exposing Rust to C
10. Anti-patterns
11. Checks

## 1. When unsafe is acceptable

Default: **do not write `unsafe`.** Application crates set `unsafe_code = "forbid"`.

Acceptable, after checking that std or a well reviewed crate does not already do it:

- FFI: calling C or exposing Rust to C.
- A measured hot path where a bounds check or initialization shows up in the profile, and a safe rewrite (iterators, `chunks_exact`, slice patterns, `split_at`) did not remove it.
- Implementing a low level data structure or synchronization primitive that cannot be expressed safely (and that no crate provides).
- Hardware, memory mapped IO, OS interfaces (`libc`, `nix`, `rustix` first).

Not acceptable: silencing the borrow checker, `transmute` between types for convenience, `unsafe impl Send/Sync` to make a `!Send` error go away, extending a lifetime, "performance" without a profile.

Check std and crates first: `Rc`, `Arc`, `Cell`, `RefCell`, `OnceLock`, `mem::take/swap/replace`, atomics, `bytemuck` (safe casts of plain data), `zerocopy`, `memchr`, `cxx` (C++ interop), `bindgen`.

## 2. The soundness rule

**No safe code, however it is called, may cause undefined behaviour.** A safe function that can trigger UB for some input is unsound even if no current caller passes that input (Rustonomicon).

Consequences:

- Unsafe code may trust safe code it controls (its own module) but **must not trust generic safe code supplied by callers.** A buggy user `Ord`, `Hash`, `Iterator::size_hint`, `Read` or `Drop` impl may misbehave, but must not cause UB in your code. If you need to rely on a trait's correctness for memory safety, make it an `unsafe trait`.
- Soundness is **non local**: changing `<` to `<=` in safe code next to an `unsafe` block can make it unsound. The unit of review is the module, not the block.

## 3. Writing an unsafe block

- **Every `unsafe` block gets a `// SAFETY:` comment** directly above it that names each precondition of each unsafe operation and why it holds here. Enforced by `clippy::undocumented_unsafe_blocks`.
- **One unsafe operation per block** where practical, so each has its own justification (`clippy::multiple_unsafe_ops_per_block`).
- **Smallest scope**: only the unsafe call inside the block, not the surrounding logic.

```rust
// Good
let idx = self.find(key)?;          // returns an index < self.items.len()
// SAFETY: `find` only returns indices of existing elements, and `items` is not
// modified between the call and this access.
let item = unsafe { self.items.get_unchecked(idx) };

// Bad: no justification, logic inside the block, several operations
let item = unsafe {
    let i = self.find(key).unwrap();
    let p = self.items.as_ptr().add(i);
    &*p
};
```

- Prefer the checked API until a profile says otherwise; `get_unchecked` saves a branch the optimizer often removes anyway.
- Raw pointer creation is safe, dereference is not. Create references from raw pointers only when the pointee is valid, aligned, initialized and not aliased mutably for the whole lifetime of the reference.
- `MaybeUninit<T>` for uninitialized memory, never `mem::uninitialized` or `mem::zeroed` on types where all zeros is not a valid value (references, `NonZero`, enums, `bool` patterns).
- `transmute`: almost always replaceable by `from_ne_bytes`, `to_bits`/`from_bits`, `as` on pointers, `bytemuck::cast`, or `ptr::cast`. If you must, annotate both types: `transmute::<u32, f32>(x)`.

## 4. Containing unsafe in a module

- Put unsafe code in the **smallest private module that can uphold its invariants**, expose a safe API from it, and let the rest of the crate be safe (Rust Design Patterns). Mark that module `#[expect(unsafe_code, reason = "...")]` with the crate set to `unsafe_code = "deny"` so new unsafe elsewhere fails the build.
- **Fields that the unsafe code relies on are private.** The Rustonomicon's `Vec` example: a safe `fn make_room(&mut self) { self.cap += 1 }` added in the same module breaks `push`. Privacy is "the only bullet-proof way to limit the scope of unsafe code".
- Write the invariants on the type as a doc comment (`/// Invariant: len <= cap, and the first len slots are initialized.`) and keep them true at every exit of every method, including early returns and panics (a panic mid update with a `Drop` impl reading the state is a classic UB source).
- One crate per unsafe concern in a workspace is even better: `foo-sys` (raw bindings) and `foo` (safe wrapper).

## 5. Unsafe functions and traits

- `unsafe fn` means "callers must uphold a contract". Document it in a `# Safety` section (`clippy::missing_safety_doc`, default on). A function whose body uses unsafe but which is sound for all inputs is a **safe** `fn` with an unsafe block inside.
- Provide a safe checked variant next to any `_unchecked` one (`get` / `get_unchecked`) (C-GETTER).
- `unsafe trait` when implementors must uphold something unsafe code relies on (`Send`, `Sync`, `GlobalAlloc`). `unsafe impl` gets a `// SAFETY:` comment too.
- `unsafe impl Send for X {}` / `Sync`: only for types containing raw pointers whose thread safety you have proven; write the proof in the SAFETY comment. `clippy::non_send_fields_in_send_ty` (nursery) catches fields that make it wrong.

## 6. Rust 2024 edition changes

- The body of an `unsafe fn` is no longer an unsafe context; each operation needs its own `unsafe {}` block (`unsafe_op_in_unsafe_fn` warns; set it to `deny`).
- `extern` blocks are written `unsafe extern "C" { ... }`, and each item can be marked `safe fn` or `unsafe fn`:

```rust
unsafe extern "C" {
    pub safe fn abs(x: i32) -> i32;                  // callable without unsafe
    pub unsafe fn strlen(p: *const std::ffi::c_char) -> usize;
}
```

- Attributes that can cause UB are written `#[unsafe(no_mangle)]`, `#[unsafe(export_name = "..")]`, `#[unsafe(link_section = "..")]`.
- References to `static mut` are denied (`static_mut_refs`); use `&raw const` / `&raw mut`, or better, an atomic, `Mutex`, `OnceLock` or `thread_local!` instead of `static mut`.
- `std::env::set_var` and `remove_var` are `unsafe` (they race with any thread reading the environment, including C code). Call them only before spawning threads, or not at all.

## 7. Verifying unsafe code

- **Miri** on every crate with unsafe: `cargo +nightly miri test`. It detects out of bounds access, use after free, invalid values, data races and aliasing violations (Stacked/Tree Borrows) in the code paths your tests exercise. It cannot run FFI calls; gate those tests with `#[cfg_attr(miri, ignore)]`.
- More tests than usual, especially around boundaries (empty, full, capacity growth, panics in user callbacks).
- Sanitizers (nightly): `RUSTFLAGS="-Zsanitizer=address"` and `thread` for code Miri cannot run (FFI).
- `loom` for custom concurrency primitives with atomics.
- Fuzz safe APIs that wrap unsafe internals.
- Track unsafe in dependencies with `cargo geiger` if the project has a safety budget.

## 8. FFI: calling C

- Generate declarations with `bindgen` (in a `build.rs` or checked in) rather than writing them by hand; mismatched C and Rust declarations are not caught by the linker, they fail at runtime.
- Layout: `#[repr(C)]` on every struct and enum that crosses the boundary. Use fixed size types (`u32`, `i64`) or `std::ffi::c_int`/`c_long`/`c_char`, never Rust `usize` for C `int`.
- Strings: `CString::new(s)?` (fails on interior NUL) to pass owned strings in, `CStr::from_ptr(p)` to read borrowed ones, and keep the `CString` alive while C uses the pointer:

```rust
let name = CString::new(name)?;
// SAFETY: `name` outlives the call and lib_open does not keep the pointer.
let handle = unsafe { ffi::lib_open(name.as_ptr()) };
// Bad: let p = CString::new(name)?.as_ptr(); the CString is freed at the end of
// that statement, so `p` dangles (rustc lint dangling_pointers_from_temporaries).
```

- **Memory is freed by the side that allocated it**: C memory with the C library's free function, Rust memory by Rust. Never `free()` a `Box` or drop a C pointer as a `Box`.
- **Wrap every C handle in a Rust type** that holds a non null pointer (`NonNull<T>`), frees it in `Drop`, and exposes safe methods. The constructor returns `Result` when C returns NULL. Mark it `!Send`/`!Sync` unless the C library documents thread safety (raw pointers make it so by default; do not override without proof).
- Translate C error codes into a Rust error enum at the wrapper; callers never see an `int` status.
- Put raw declarations in a `foo-sys` crate with `links = "foo"` in its `Cargo.toml`, and the safe API in `foo`.
- Callbacks from C into Rust: `extern "C" fn` trampolines that catch panics (next section) and take a `*mut c_void` user data pointer that you turn back into `&mut T` only while you know it is alive.

## 9. FFI: exposing Rust to C

- Export with `#[unsafe(no_mangle)] pub extern "C" fn mylib_thing_new(..)`, prefix every symbol with the library name (C has one global namespace).
- **Panics must not unwind into C** (UB with `extern "C"`; with `extern "C-unwind"` they may unwind, only if the C++ side expects it). Wrap each exported function body in `std::panic::catch_unwind` and convert to an error code, or build with `panic = "abort"`.
- Hand out heap objects as opaque pointers: `Box::into_raw(Box::new(obj))`, and provide `mylib_thing_free(ptr)` that checks for NULL and does `drop(Box::from_raw(ptr))`. Never return a pointer to a stack value.
- Accept incoming pointers with `ptr.as_ref()` / `NonNull::new(ptr)` and handle NULL, rather than dereferencing blindly.
- Errors: return an integer code (0 for success) and offer `mylib_last_error_message()` or an out parameter; Rust Design Patterns "FFI errors" idiom: flat enums become integers, structured errors become a code plus a message function.
- Generate the C header with `cbindgen`.

## 10. Anti-patterns

| Anti-pattern | Fix |
|---|---|
| `unsafe` block with no SAFETY comment | document every precondition |
| large `unsafe { ... }` wrapping ordinary logic | shrink to the single operation |
| `unsafe impl Send` to silence a compiler error | find the `Rc`/guard/raw pointer, fix the design |
| `transmute` for numeric or pointer casts | `to_bits`/`from_bits`, `cast`, `bytemuck` |
| `static mut COUNTER` | `AtomicUsize`, `OnceLock`, `Mutex` |
| `let p = CString::new(x)?.as_ptr();` then passing `p` to C | bind the `CString` to a variable that outlives the call |
| public fields on a type whose unsafe methods rely on them | private fields, invariants documented |
| safe fn that is UB for some inputs | make it `unsafe fn` with `# Safety`, or check the input |
| panicking inside an `extern "C" fn` | `catch_unwind`, convert to an error code |

## 11. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Unsafe forbidden where unused | crates with no unsafe have `unsafe_code = "forbid"` (or deny at workspace) | `rg -n 'unsafe_code' Cargo.toml crates/*/Cargo.toml`; `rg -c 'unsafe ' crates/*/src` to find crates that have none |
| Every unsafe block justified | zero warnings | `clippy::undocumented_unsafe_blocks`, `clippy::multiple_unsafe_ops_per_block` |
| Unsafe fns document safety | zero warnings | `clippy::missing_safety_doc` (default on) |
| Explicit unsafe in unsafe fns | zero warnings | `unsafe_op_in_unsafe_fn = "deny"` |
| Unsafe confined | every `unsafe` is inside modules marked `#[expect(unsafe_code, ..)]` | `rg -n 'unsafe \{\|unsafe fn\|unsafe impl' src` and compare with the allowed modules |
| No `static mut` | zero | `rg -n 'static mut ' src` |
| No casual transmute | each `transmute` has turbofish types and a SAFETY comment | `rg -n -B2 'transmute' src` |
| Miri clean | pass | `cargo +nightly miri test` |
| FFI types repr(C) | every type in an `extern` signature is `#[repr(C)]` or a primitive | review `rg -n 'extern "C"' src` signatures |
| No panic across FFI | every exported `extern "C" fn` body uses `catch_unwind` or the profile sets `panic = "abort"` | `rg -n -A3 'pub (unsafe )?extern "C" fn' src` |
