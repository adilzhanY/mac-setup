# Ownership, clones and performance

Ownership decisions, smart pointer choice, and the performance basics that matter without a profiler. Sources: Rust Performance Book (Nethercote), Effective Rust items 8, 9, 15, 20, Rust Design Patterns (borrow_clone anti-pattern, mem::take idiom), Book ch. 15.

## Contents

1. Own or borrow
2. Clone discipline
3. Fighting the borrow checker without cloning
4. Smart pointers: which one
5. Allocation
6. Iterators
7. Collections and hashing
8. Strings
9. Type sizes
10. IO
11. Build profiles
12. Measure before optimizing
13. Checks

## 1. Own or borrow

| Situation | Signature |
|---|---|
| read only | `&T`, or the borrowed form: `&str`, `&[T]`, `&Path` |
| mutate in place | `&mut T` |
| store it, send it to a thread or task, or consume it | `T` by value |
| sometimes store, usually not | `Cow<'_, str>` or take by value and let callers clone |
| struct field | owned (`String`, `Vec<T>`) by default. A lifetime on a struct (`struct Parser<'a> { input: &'a str }`) only for short lived views, parsers and iterators |

- Lifetimes on long lived structs (app state, services, config) spread to every user and are almost always wrong; own the data or share it with `Arc`.
- Return owned values from constructors and builders, borrowed views from accessors.

## 2. Clone discipline

- **A `.clone()` added to make a borrow error go away is a defect** (Rust Design Patterns anti-pattern "clone to satisfy the borrow checker"). The two copies are no longer in sync, and it costs an allocation for `String`, `Vec`, `HashMap`. Fix the structure (section 3) first.
- Clones that are fine: `Arc`/`Rc` clones (a counter increment), `Copy` types, cloning into a spawned task or thread that must own its data, cloning a small value once at startup, and clones in tests.
- Write reference counted clones as `Arc::clone(&state)`, so a reader can tell a cheap pointer copy from a deep copy. Enforce with `clippy::clone_on_ref_ptr`.
- `clippy::redundant_clone` (nursery) finds clones of values that are not used afterwards; `clippy::implicit_clone` (pedantic) finds `to_owned()`/`to_string()` that are clones in disguise.
- Taking `&T` and cloning inside the function hides the cost from the caller; take `T` by value instead (C-CALLER-CONTROL).
- `clone_from(&src)` reuses the destination's allocation when overwriting an existing `String`/`Vec` (`clippy::assigning_clones`, pedantic).

## 3. Fighting the borrow checker without cloning

| Error shape | Fix |
|---|---|
| need to move a field out of `&mut self` | `std::mem::take(&mut self.buf)` (leaves `Default`), `mem::replace(&mut self.state, State::Idle)`, `Option::take()` |
| change an enum variant in place while keeping its owned data | `match` on `&mut self`, then `mem::take` the `String` from the old variant into the new one |
| borrow two fields of `self` at once, one mutably | destructure: `let Self { items, index, .. } = self;`, or borrow the fields directly instead of calling a `&mut self` method |
| struct so big every method borrows all of it | split it into smaller structs that are borrowed independently (Rust Design Patterns, "compose structs") |
| mutate a collection while iterating it | collect the keys or indices to change first, or `retain`, `retain_mut`, `drain(..)`, `extract_if` |
| borrow lives too long | end it early with a smaller block `{ }`, or compute the value you need into a local first |
| shared ownership across a graph or callbacks | indices into a `Vec` (arena style) first; `Rc<RefCell<T>>` only when indices do not fit |
| closure needs some captured values cloned | clone into a new binding just before `move` (Rust Design Patterns, "pass variables to closure") |

## 4. Smart pointers: which one

| Need | Use | Notes |
|---|---|---|
| heap allocate, single owner, recursive type, large value | `Box<T>` | `Vec<Box<T>>` of small `T` is usually pointless (`clippy::vec_box`) |
| shared read only ownership, one thread | `Rc<T>` | |
| shared ownership across threads | `Arc<T>` | |
| shared mutable, one thread | `Rc<RefCell<T>>` | `RefCell` borrow errors are runtime panics; keep borrows short |
| shared mutable, threads | `Arc<Mutex<T>>` or `Arc<RwLock<T>>` | see async-and-concurrency.md |
| counter or flag across threads | `AtomicU64`, `AtomicBool` | not `Mutex<u64>` (`clippy::mutex_integer`, `mutex_atomic`) |
| immutable shared string or slice | `Arc<str>`, `Arc<[T]>` | not `Arc<String>` / `Arc<Vec<T>>`, one fewer indirection (`clippy::rc_buffer`) |
| init once, global | `std::sync::LazyLock` / `OnceLock` | not `lazy_static!` or `once_cell` in new code (`clippy::non_std_lazy_statics`) |
| break a reference cycle | `Weak<T>` for the back pointer (child -> parent) | an `Rc` cycle leaks |
| maybe owned, maybe borrowed | `Cow<'a, T>` | |

- Do not use `Rc`/`Arc` for values that are rarely shared; it adds an allocation and a counter.
- `Rc<Mutex<T>>` is a contradiction (single thread type with a thread lock): `clippy::rc_mutex`.
- `Cell<T>` for `Copy` values inside a single thread `&self` API, `RefCell<T>` otherwise.

## 5. Allocation

Profile first; if `malloc` is hot, these are the cheap wins (Rust Performance Book, "Heap allocations"):

- `Vec::with_capacity(n)` / `String::with_capacity(n)` / `HashMap::with_capacity(n)` when `n` is known or estimable. 20 pushes without it cost 4 allocations (capacity 4, 8, 16, 32).
- **Hoist buffers out of loops** and `clear()` them each iteration; `clear` keeps the capacity.
- Pass `&mut Vec<T>` into a function that fills it, when it is called in a loop, instead of returning a new `Vec` each time.
- Read lines with one reused `String` and `read_line` + `clear()`, not `lines()` (which allocates a `String` per line), when the loop only needs `&str`.
- `Box<[T]>` instead of `Vec<T>` for large collections that never change size (saves the capacity word).
- `SmallVec<[T; N]>` / `ArrayVec` for vectors that are almost always short; benchmark, as each operation is slightly slower.
- An alternative global allocator (`mimalloc`, `tikv-jemallocator`) is a one line change that often helps allocation heavy servers; measure.
- Guard a fixed allocation budget with a `dhat` heap test when it matters.

## 6. Iterators

- **Do not `collect()` only to iterate again** (`clippy::needless_collect`, nursery). Chain the adapters.
- `extend(iter)` into an existing collection instead of collecting into a temporary and appending.
- `filter_map` instead of `filter` + `map`; `iter().copied()` for small `Copy` items.
- `chunks_exact` instead of `chunks` when the size divides the length (removes a bounds check per chunk).
- Iterator chains compile to the same code as index loops, and they remove bounds checks; prefer them over `for i in 0..v.len()` (`clippy::needless_range_loop`). Plain `for x in &v` is fine when the body is imperative.
- Implement `size_hint` (or `ExactSizeIterator`) on custom iterators so `collect` preallocates.
- Avoid long `chain`s in hot loops; they are slower than one iterator.
- `sort_unstable` for primitives and keys where stability does not matter (`clippy::stable_sort_primitive`, pedantic).

## 7. Collections and hashing

- `Vec` by default. `VecDeque` for queues. `HashMap`/`HashSet` for lookup. `BTreeMap` when you need ordered iteration or deterministic output. `LinkedList` almost never (`clippy::linkedlist`).
- The default `HashMap` hasher (SipHash 1-3) resists HashDoS and is slow for small keys. For internal maps keyed by integers or small strings that attackers cannot control, `rustc_hash::FxHashMap`, `ahash` or `foldhash` are much faster. Keep the default for maps keyed by user input.
- If you switch hashers project wide, ban the std one with `disallowed-types` in `clippy.toml` so nobody reintroduces it.
- Iteration order of `HashMap` is random. Output that must be stable (files, snapshots, hashes, API responses) uses `BTreeMap`, an `IndexMap`, or sorts first (`clippy::iter_over_hash_type` flags hash iteration if you need determinism everywhere).
- `entry()` API instead of `contains_key` + `insert` (one lookup, `clippy::map_entry`).

## 8. Strings

- `&str` in, `String` out; `impl Into<String>` or `Cow<'static, str>` for constructors mixing literals and owned text.
- Build strings with `write!(s, ...)` or `push_str`, not `s += &format!(...)` (an extra allocation per call, `clippy::format_push_string`, pedantic).
- `to_owned()` on `&str` (or `String::from`) consistently; `str_to_string` (restriction) bans `"x".to_string()` if you want one spelling.
- Never slice strings by byte offsets from untrusted input (`&s[..n]` panics off a char boundary); use `char_indices`, `get(..n)`, or `split_at_checked`.
- Bytes that are not guaranteed UTF-8 stay `Vec<u8>` / `&[u8]` (or `bstr`); paths stay `PathBuf`/`OsString`. Do not `to_string_lossy()` and later write them back.

## 9. Type sizes

- Keep hot types at 128 bytes or less; larger values are `memcpy`d on every move.
- A rare, large enum variant gets its fields boxed (`clippy::large_enum_variant` warns at 200 bytes difference).
- Large error types slow down every `Result` return; box their payload (`clippy::result_large_err`, 128 bytes).
- Use `u32` indices instead of `usize` in large index heavy structures when the range allows.
- Pin the size of a hot type with a compile time assertion so a field addition cannot grow it silently:

```rust
#[cfg(target_pointer_width = "64")]
const _: () = assert!(std::mem::size_of::<Token>() == 16);
```

## 10. IO

- File and socket IO is unbuffered. Wrap in `BufReader`/`BufWriter` for many small reads or writes.
- Call `flush()` on a `BufWriter` explicitly before drop; drop flushes but silently ignores the error.
- `println!` locks stdout on every call. In a loop, `let mut out = std::io::stdout().lock();` once and `writeln!(out, ..)?`, buffered.

## 11. Build profiles

Defaults: `dev` is `opt-level = 0`, debug info, overflow checks on; `release` is `opt-level = 3`, no debug info, `lto = false`, `codegen-units = 16`, overflow checks off.

```toml
# root Cargo.toml only; profiles in member crates are ignored

[profile.dev.package."*"]
opt-level = 2          # optimize dependencies, keep your own crate fast to rebuild

[profile.dev]
debug = "line-tables-only"   # 20 to 40% faster dev builds, still readable backtraces

[profile.release]
lto = "thin"           # often 10 to 20% faster code
codegen-units = 1
debug = "line-tables-only"   # profilers and panics still get file and line

[profile.release-max]  # cargo build --profile release-max, for shipped binaries
inherits = "release"
lto = "fat"
panic = "abort"        # only if nothing relies on catch_unwind or unwinding
```

- Keep `overflow-checks = true` in release for code where silent wrap is a correctness or security bug (money, sizes from input) or use `checked_*` arithmetic there.
- `-C target-cpu=native` only for binaries that run on the build machine.
- Use a faster linker for dev builds (`mold`, or `lld`, which is the default on x86_64 Linux in recent Rust).
- PGO (`cargo-pgo`) can add 10% or more for CPU bound binaries once everything else is done.

## 12. Measure before optimizing

- Optimize after a profiler says where (Effective Rust item 20). `cargo flamegraph`, `perf`, `samply`, and DHAT (`dhat-rs`) for allocations.
- Benchmark with `criterion` (stable) or `divan`, and wrap inputs with `std::hint::black_box` so the optimizer does not delete the work.
- Never trade clarity for speed in code that is not hot. A clear `clone()` in startup code beats a lifetime puzzle.

## 13. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| No needless clones | zero warnings | `clippy::redundant_clone` (nursery), `clippy::implicit_clone`, `clippy::assigning_clones` (pedantic) |
| Ref counted clones explicit | zero warnings | `clippy::clone_on_ref_ptr` |
| No collect then iterate | zero warnings | `clippy::needless_collect` |
| No `Arc<String>` / `Arc<Vec<_>>` / `Rc<Mutex<_>>` | zero warnings | `clippy::rc_buffer`, `clippy::rc_mutex` |
| No `lazy_static!` / `once_cell` in new code | zero hits | `rg -n 'lazy_static!\|once_cell::' src`; `clippy::non_std_lazy_statics` |
| No `&s[a..b]` on untrusted strings | each hit justified | `rg -n '&\w+\[[^\]]*\.\.' src`, or `clippy::string_slice` in parsing modules |
| Buffers hoisted | no `Vec::new()`/`String::new()` inside hot loops | review hot paths found by the profiler |
| Profiles at root only | no `[profile` in member manifests | `rg -n '^\[profile' crates/*/Cargo.toml` |
| Hot type sizes pinned | `const _: () = assert!(size_of::<T>() == N)` for types in hot collections | `rg -n 'size_of::<' src` |
| Deterministic output | no HashMap iteration feeding files, snapshots or responses | `clippy::iter_over_hash_type` in those modules |
