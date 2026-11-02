# Benchmarks

How to measure the speed of a piece of code or a command so that a comparison means something: microbenchmarks in Rust (criterion, divan) and JavaScript (Vitest bench, tinybench, mitata), command benchmarks with hyperfine, noise and warmup, catching regressions in CI (CodSpeed, Bencher, instruction counts), and pointers for app startup time and frame rate. kwx-developer `reliability/performance.md` P6 says benchmarks are statistical; this file is how to run them that way. Load tests of whole services are in `load-testing.md`.

## Contents

1. When a microbenchmark is the right tool
2. The rules that matter most
3. Rust: criterion
4. Rust: divan
5. JavaScript: Vitest bench, tinybench, mitata
6. Commands and CLIs: hyperfine
7. Noise: where it comes from and how to reduce it
8. Benchmarks in CI
9. App startup time and frame rate
10. Checks

## 1. When a microbenchmark is the right tool

| Question | Tool |
|---|---|
| Is implementation A faster than B for this input? | microbenchmark (criterion, divan, Vitest bench) |
| Did this commit make a hot function slower? | microbenchmark with a baseline, in CI with instruction counts or a dedicated runner |
| How long does the CLI take to start or run? | hyperfine |
| Is the API fast enough under traffic? | load test (`load-testing.md`), not a microbenchmark |
| Why is it slow? | a profiler (kwx-developer `reliability/performance.md` sections 4 and 5), not a benchmark |

A microbenchmark measures code in isolation, with warm caches and a predictable branch history. It answers "which is faster here", not "will users notice". Evidence: moderate.

## 2. The rules that matter most

1. **Benchmark a release build.** `cargo bench` uses the bench profile (optimised); for JS, benchmark the built code path the app runs. Evidence: strong.
2. **Stop the compiler from deleting the work.** Pass inputs and results through `std::hint::black_box` (Rust) or mitata's `do_not_optimize` (JS); otherwise an optimiser can remove code whose result is unused. Evidence: strong (criterion FAQ, mitata README).
3. **Warm up, then take many samples, and report a distribution** (median and spread or a confidence interval), not one timing. Evidence: strong (criterion analysis docs).
4. **Compare on the same machine, same build settings, same input, close in time,** ideally interleaved. Evidence: strong.
5. **Treat small differences as noise until shown otherwise.** criterion ignores changes inside its noise threshold (default 1%) and reports significance; shared CI runners vary much more than that. Evidence: strong (criterion docs).
6. **Benchmark realistic inputs and sizes,** and several sizes (10, 1,000, 100,000) to see the growth, not one toy input. Evidence: moderate.
7. **Measure allocations too when they matter** (divan `AllocProfiler`, hyperfine 2 peak memory). Evidence: moderate.
8. **In CI, gate on instruction counts or on a dedicated quiet runner,** never on wall time from a shared cloud runner. Evidence: strong (criterion FAQ, CodSpeed docs).
9. **Keep the benchmark code reviewed like test code.** A benchmark that measures setup instead of the operation is a common mistake: move setup out of the timed closure. Evidence: moderate.

## 3. Rust: criterion

criterion (0.8) is the established statistics driven harness. Process (criterion book, "Analysis"): warm up by running the routine with a doubling iteration count until the warm-up time is reached (3 s default), then take samples with linearly increasing iteration counts (100 samples, 5 s measurement by default), classify outliers with a modified Tukey method (kept, but flagged), bootstrap confidence intervals, and compare with the previous run (significance level 0.05 and noise threshold 0.01 by default). Defaults are from the `Criterion` builder documentation.

```toml
[dev-dependencies]
criterion = "0.8"

[[bench]]
name = "parse"
harness = false
```

```rust
// benches/parse.rs
use criterion::{criterion_group, criterion_main, BenchmarkId, Criterion, Throughput};
use std::hint::black_box;

fn bench_parse(c: &mut Criterion) {
    let mut group = c.benchmark_group("parse_config");
    for size in [10usize, 1_000, 100_000] {
        let input = my_crate::fixtures::config_with_keys(size);
        group.throughput(Throughput::Bytes(input.len() as u64));
        group.bench_with_input(BenchmarkId::from_parameter(size), &input, |b, input| {
            b.iter(|| my_crate::parse(black_box(input)))
        });
    }
    group.finish();
}

criterion_group!(benches, bench_parse);
criterion_main!(benches);
```

Baselines for A/B comparison (criterion book):

```bash
git switch main     && cargo bench --bench parse -- --save-baseline main
git switch feature  && cargo bench --bench parse -- --baseline main
```

- Use `iter_batched` when each iteration needs fresh input (for example a vector to sort), so setup is not timed.
- `--save-baseline` with the default libtest harness causes an "unrecognized option" error; that is why `harness = false` is required and why you target one bench with `--bench name` (criterion FAQ).
- HTML reports land in `target/criterion/report/index.html`; read the distribution plot, not only the headline number.

## 4. Rust: divan

divan (0.1.21, requires Rust 1.80) is a lighter harness with attribute based registration, parameter lists and allocation counting.

Verified 2026-10-31: the benchmark below ran with `cargo bench`, printing fastest, slowest, median and mean per argument with 100 samples each.

```toml
[dev-dependencies]
divan = "0.1.21"

[[bench]]
name = "parse"
harness = false
```

```rust
// benches/parse.rs
fn main() { divan::main(); }

#[divan::bench(args = ["a=1", "long_key_name = some value here"])]
fn parse_kv(line: &str) -> Option<(&str, &str)> {
    my_crate::parse_kv(divan::black_box(line))
}
```

Count allocations by installing its allocator in the bench binary (divan docs): `#[global_allocator] static ALLOC: divan::AllocProfiler = divan::AllocProfiler::system();`. Output then shows allocations and bytes per iteration, which is often the real cause of a slowdown.

Pick criterion for statistical comparison against saved baselines and long term tracking; pick divan for quick, readable, parameterised benchmarks with allocation counts. Both have CodSpeed compatible drop in crates (section 8).

## 5. JavaScript: Vitest bench, tinybench, mitata

**Vitest 5 changed the benchmark API.** `bench` is no longer imported from `vitest`; it is a fixture from the test context, usable only in files matched by `benchmark.include` (default `**/*.{bench,benchmark}.?(c|m)[jt]s?(x)`). `--compare` and `--outputJson` were removed; use `writeResult` with `bench.from()` and the JSON reporter (Vitest 5 migration guide). Examples written for Vitest 1 to 4 (`import { bench } from 'vitest'`) do not run on Vitest 5.

Verified 2026-10-31 with Vitest 5.0.5 (`npx vitest bench`):

```ts
// parse.bench.ts
import { test, expect } from 'vitest';

test('split vs regex', async ({ bench }) => {
  const line = 'key = value';
  const result = await bench.compare(
    bench('split', () => line.split('=')),
    bench('regex', () => /^(.*?)=(.*)$/.exec(line)),
  );
  expect(result.get('split')).toBeDefined();
  // for a large, known gap you can assert it, with a margin so noise does not flip it (Vitest docs):
  // expect(result.get('fast')).toBeFasterThan(result.get('slow'), { delta: 0.1 });
});
```

- `bench.compare()` interleaves iterations of the candidates to reduce bias from throttling and GC (Vitest docs).
- Plain `vitest` runs skip benchmark files unless `benchmark.enabled: true`; `vitest bench` runs only benchmarks.
- Options such as `iterations` and `time` go in the last argument of `bench.compare()` and are passed to Tinybench.
- Use performance assertions (`toBeFasterThan` with `delta`) only for large, stable gaps; for small ones, record numbers instead of asserting.

**tinybench** (6.2) is the library under Vitest bench; use it directly in plain Node scripts.

**mitata** (1.0) has very low overhead measurement loops, boxplots and summaries, and runs on Node, Bun, Deno and several JS engines:

```js
import { run, bench, summary, do_not_optimize } from 'mitata';

summary(() => {
  bench('JSON.parse', () => do_not_optimize(JSON.parse('{"a":1}')));
  bench('custom', () => do_not_optimize(customParse('{"a":1}')));
}).gc('inner');   // run GC before each iteration batch to reduce GC noise

await run();
```

JS specific traps: the JIT optimises after many calls, so warmup matters more than in Rust; dead code elimination removes unused results (use `do_not_optimize` or keep the result); benchmark in the runtime the app uses (Node vs Bun vs a browser differ); GC pauses add tail noise, so look at p75 and p99 per iteration, not only the mean. Evidence: moderate (mitata README, Vitest docs).

## 6. Commands and CLIs: hyperfine

hyperfine (2.0, October 2026) benchmarks whole commands with warmup, statistics and comparison. Version 2 changes (release notes): commands run directly without a shell by default (`--shell=none`), so use `-S` (`--shell=default`) for pipes or shell syntax; peak memory is shown by default and `--metrics` selects others (instructions, cycles, cache misses); the `--export-json` format changed to schema version 2.

```bash
hyperfine --warmup 3 'kwx --version'                               # startup time
hyperfine --warmup 3 -N 'kwx parse big.toml' 'kwx-old parse big.toml' # compare two builds
hyperfine -S --warmup 3 'cat big.log | kwx filter error'           # needs a shell for the pipe
hyperfine --prepare 'sync; echo 3 | sudo tee /proc/sys/vm/drop_caches' 'kwx index ./repo'   # cold cache (needs sudo)
hyperfine -P threads 1 8 --env 'RAYON_NUM_THREADS={threads}' 'kwx index ./repo'
hyperfine --export-json bench.json --export-markdown bench.md 'kwx index ./repo'
```

Report the mean with its spread and the min, and compare commands in the same invocation so hyperfine prints the relative speed. Cold cache runs need `sudo` on Linux; if the user's rules forbid running sudo, ask, or report warm results only and say so.

## 7. Noise: where it comes from and how to reduce it

Sources (criterion FAQ, Brendan Gregg): other processes and VMs competing for CPU and memory, CPU frequency scaling and thermal throttling, turbo boost, SMT siblings, memory layout and alignment changes between builds, page cache state, interrupts, and on laptops the power mode.

Reduction, in order of effort:

1. Close heavy apps; do not benchmark during a build or a video call. Plug in the laptop.
2. Run more samples and longer measurement times; compare distributions.
3. Interleave A and B (Vitest `bench.compare`, hyperfine with both commands) instead of running all of A then all of B.
4. Pin to a core (`taskset -c 2 cargo bench`) and use the performance governor (`cpupower frequency-set -g performance`, needs root).
5. Disable turbo and SMT on a dedicated benchmark machine.
6. Use instruction counts instead of time (section 8) when you only need to detect regressions.

Check stability first: run the same benchmark twice without changes. If the two runs differ by 5%, a 3% "improvement" means nothing. Evidence: strong.

## 8. Benchmarks in CI

criterion's FAQ warns that the virtualization of cloud CI providers adds a great deal of noise, and points to instruction counting instead. Options:

| Approach | How it works | Use |
|---|---|---|
| Instruction count benchmarks | gungraun (formerly iai-callgrind, renamed 2025) runs benchmarks under Valgrind and counts instructions and cache events; deterministic, independent of machine load | Rust regression gates on any CI runner |
| CodSpeed | CPU simulation: runs each benchmark once and estimates cycles from instructions and cache misses (system calls excluded); also a walltime mode on its own runners | Rust (`codspeed-criterion-compat`, `codspeed-divan-compat`), Node (`@codspeed/vitest-plugin`, tinybench plugin), Python; posts PR reports |
| Bencher | stores results from any harness and runs statistical thresholds (t-test, z-score, percentage, IQR and others) against history per branch and testbed; `bencher run --error-on-alert` fails the job | long term tracking with your own runners |
| Dedicated self hosted runner | a quiet machine with pinned frequency running criterion with baselines | when wall time itself matters (IO, syscalls) |

Rules:

1. **Gate PRs only on deterministic metrics or a dedicated runner,** and with a threshold above the measured noise. Evidence: strong.
2. **Track the trend on `main`,** not only PR diffs; slow drifts of 1% per change add up. Evidence: moderate.
3. **Instruction counts do not see IO, syscalls or parallel speedups.** Pair them with an occasional wall time run for IO heavy code. Evidence: moderate (CodSpeed docs).
4. **A benchmark regression is a finding to explain, not to silence.** Report the change, the likely commit, and the profile. Evidence: opinion.

## 9. App startup time and frame rate

Pointers, not full guides:

| App type | Startup | Frame rate and jank |
|---|---|---|
| CLI / TUI | `hyperfine --warmup 3 'app --version'` and a typical command | for TUIs, time from key event to rendered frame with an in-app timer behind a debug flag |
| Qt / QML (including Quickshell) | timestamps from `main()` to the first `frameSwapped` signal of the window; or `QT_LOGGING_RULES="qt.scenegraph.time.renderloop=true"` to log render loop timing | `QSG_RENDER_TIMING=1` prints per frame timing; the QML Profiler (`qmlprofiler` or Qt Creator) shows binding and JS cost per frame |
| Electron | `app.on('ready')` and the first `did-finish-load` with `performance.now()`; Playwright can measure from `electron.launch` to `firstWindow` | Chrome DevTools Performance panel on the renderer |
| Tauri | timestamps in Rust `setup` and on the frontend first paint | WebView DevTools performance panel |
| Android (Expo, React Native, Compose) | Jetpack Macrobenchmark `StartupTimingMetric`, see `../mobile/android-native.md` | Macrobenchmark `FrameTimingMetric`; React Native perf monitor |
| Web pages | Core Web Vitals and Lighthouse, see `../web/performance-and-seo-checks.md` | Performance panel, INP |

Rules: measure a cold start (after reboot or dropping caches) and a warm start separately and say which; measure on the slowest hardware the app supports; repeat at least 10 times and report the median and the worst. For frame rate, report the share of frames over budget (16.7 ms at 60 Hz, 8.3 ms at 120 Hz) during a defined interaction, not an average FPS. Evidence: moderate (Android Macrobenchmark docs use these metrics; Tene's argument against averages applies to frames too).

## 10. Checks

| Check | Pass condition |
|---|---|
| Right tool | microbenchmark only for code level questions; load test or profiler otherwise |
| Release build | benchmarks run optimised |
| Optimiser | inputs and outputs passed through `black_box` / `do_not_optimize` |
| Setup outside timing | `iter_batched`, `beforeEach`, or setup outside the closure |
| Sizes | several realistic input sizes |
| Statistics | warmup, many samples, median and spread or CI reported |
| Noise measured | same benchmark run twice; differences smaller than that noise are not claimed |
| Vitest 5 | `bench` used as a test context fixture in `*.bench.*` files |
| hyperfine 2 | `-S` used for shell syntax; warmup set |
| CI | gated on instruction counts, CodSpeed, Bencher thresholds or a dedicated runner; never raw time on shared runners |
| Startup / frames | cold and warm stated; median and worst of at least 10 runs; frames over budget reported |
