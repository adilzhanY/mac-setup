# The Rust Performance Book (Nicholas Nethercote)

Free, by the author: https://nnethercote.github.io/perf-book/

## What I read

Chapters: Build Configuration, Heap Allocations, Hashing, Iterators, Type Sizes, I/O.

## Key lessons used in languages/rust/ownership-and-performance.md

- Build configuration: `codegen-units = 1`, thin or fat LTO (10 to 20% or more), `panic = "abort"`, alternative allocators (mimalloc, jemalloc), `target-cpu=native` only for local binaries, PGO (10% or more). Dev build speed: `debug = "line-tables-only"` or `false` (20 to 40% faster), faster linkers (lld default on Linux since 1.90, mold, wild). Profiles only take effect in the workspace root.
- Allocation: profile with DHAT first; `with_capacity` (20 pushes = 4 allocations otherwise); reuse collections with `clear()`; `SmallVec`/`ArrayVec`; avoid `format!` where a literal works; `clone_from`; `Cow`; box large fields; read lines into one reused `String`; dhat heap tests guard regressions.
- Hashing: default SipHash 1-3 is slow for small keys; FxHash, FNV, aHash are faster when HashDoS does not matter; ban the std map with clippy's disallowed types when switching.
- Iterators: no `collect` then iterate; return `impl Iterator`; `extend`; implement `size_hint`; avoid `chain` in hot loops; `filter_map`; `chunks_exact`; `copied()` for small items.
- Type sizes: keep hot types at 128 bytes or less; box rare large variants; smaller integer indices; `Box<[T]>`; `ThinVec`; static size assertions; do not reorder fields by hand.
- IO: lock stdout once; `BufReader`/`BufWriter`; flush explicitly to see errors; raw bytes with `read_until` when UTF-8 is not needed.
