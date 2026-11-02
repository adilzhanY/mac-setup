# The Debugging Book (and Why Programs Fail)

- Author: Andreas Zeller (CISPA)
- Year: The Debugging Book, online, text CC BY-NC-SA 4.0, code MIT (read 2026-10-31); Why Programs Fail, 2nd edition 2009 (not read, paid)
- Legal URL: https://www.debuggingbook.org/html/DeltaDebugger.html and https://www.debuggingbook.org/html/Intro_Debugging.html

## What I read

The chapters "Reducing Failure-Inducing Inputs" and "Introduction to Debugging".

## Key lessons used in exploratory/bug-reports.md and exploratory/exploratory.md

- ddmin removes chunks of the input, keeps smaller failing inputs, refines granularity; the result is 1-minimal. Best case about log2(n) tests, worst case about n squared.
- `DeltaDebugger` usage: `with DeltaDebugger() as dd: f(inp)` then `dd.min_args()`; the function must be deterministic.
- Lessons: reducing inputs helps testing and debugging; delta debugging is simple and robust; "precisely specifying failure conditions helps to avoid false diagnoses".
- Scientific debugging: question, hypothesis, prediction, experiment, conclusion; keep a log of experiments; fix causes, not symptoms.
- Vocabulary: mistake, defect, fault (infected state), failure (visible).
