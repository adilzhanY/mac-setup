# Vitest 5 benchmarking guide and migration notes

- Author: Vitest team
- Year: Vitest 5.0.5, read 2026-10-31
- Legal URL: https://vitest.dev/guide/benchmarking ; https://vitest.dev/guide/migration ; source https://github.com/vitest-dev/vitest/blob/main/docs/guide/benchmarking.md

## What I read

The full benchmarking guide and the benchmark part of the Vitest 5 migration guide.

## Key lessons used in performance/benchmarks.md

- `bench` is a test context fixture, only in files matched by `benchmark.include`; module level `bench()` removed.
- `vitest bench` runs only benchmarks; `benchmark.enabled` runs them after tests in an isolated group.
- `bench.compare()` interleaves iterations; options go to Tinybench.
- `toBeFasterThan` / `toBeSlowerThan` with `delta`.
- `--compare` and `--outputJson` removed; use `writeResult`, `bench.from()` and the JSON reporter.
