# divan, mitata, hyperfine 2, CodSpeed, Bencher, gungraun docs

- Authors: Nikolai Vazquez (divan); evanwashere (mitata); David Peter (hyperfine); CodSpeed; Bencher; gungraun maintainers
- Year: read 2026-10-31 (divan 0.1.21, mitata 1.0, hyperfine 2.0.0, codspeed-rust 6.0, bencher 0.6.16, gungraun 0.20)
- Legal URL: https://docs.rs/divan/latest/divan/ ; https://github.com/evanwashere/mitata ; https://github.com/sharkdp/hyperfine/releases/tag/v2.0.0 ; https://codspeed.io/docs/instruments/cpu ; https://bencher.dev/docs/explanation/thresholds/ ; https://github.com/gungraun/gungraun

## What I read

divan crate docs; mitata README; hyperfine 2.0 release notes; CodSpeed CPU instrument page; Bencher thresholds page; gungraun README header and crates.io metadata.

## Key lessons used in performance/benchmarks.md

- divan: `harness = false`, `divan::main()`, `#[divan::bench(args = [...])]`, `black_box`, AllocProfiler.
- mitata: `do_not_optimize`, gc modes `once`/`inner`, runs on many JS engines.
- hyperfine 2: no shell by default (`-S` for shell syntax), peak memory and `--metrics`, JSON schema v2, `--env`.
- CodSpeed: CPU simulation from instructions and cache misses, syscalls excluded; compat crates for criterion and divan; Vitest and tinybench plugins.
- Bencher: t-test, z-score, percentage, IQR, log normal and static thresholds; `--error-on-alert`.
- iai-callgrind was renamed gungraun (crate created 2025-08).
