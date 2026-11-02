# Criterion.rs user guide (book)

- Author: Brook Heisler and contributors
- Year: living documentation, read 2026-10-31 (crate version 0.8)
- Legal URL: https://bheisler.github.io/criterion.rs/book/analysis.html ; https://bheisler.github.io/criterion.rs/book/faq.html

## What I read

The "Analysis Process" chapter and the FAQ.

## Key lessons used in performance/benchmarks.md

- Phases: warmup with doubling iterations, linear sampling, analysis with bootstrap confidence intervals and modified Tukey outlier classification, comparison with a T-test and a noise threshold (example +-1%).
- Cloud CI virtualization adds a lot of noise; instruction counting (Iai, now gungraun) is the alternative.
- Baseline workflow: run on main, then on the branch, compare.
- `black_box` prevents optimisations; parameters are black boxed automatically in parameterised benchmarks.
- libtest rejects unknown arguments, which is why `harness = false` and `--bench <name>` are needed for flags like `--save-baseline`.
