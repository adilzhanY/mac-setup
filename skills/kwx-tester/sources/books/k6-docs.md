# Grafana k6 documentation and release notes

- Author: Grafana Labs
- Year: living documentation, read 2026-10-31 (k6 2.3.0; v2.0.0 release notes of 2026-05-11)
- Legal URL: https://grafana.com/docs/k6/latest/using-k6/thresholds/ ; https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/ ; https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/ ; https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/dropped-iterations/ ; https://grafana.com/docs/k6/latest/testing-guides/test-types/ ; https://grafana.com/docs/k6/latest/set-up/install-k6/ ; https://github.com/grafana/k6/releases/tag/v2.0.0

## What I read

Thresholds, executors, open vs closed model, dropped iterations, test types, install page, v2.0.0 release notes.

## Key lessons used in performance/load-testing.md (also performance.md)

- Threshold syntax including `abortOnFail`, `delayAbortEval`, tag and group thresholds, `checks` rate.
- Closed model waits for the previous iteration and is called coordinated omission; open model arrivals do not depend on response time.
- `dropped_iterations`: early drops mean too few VUs, later drops mean the system degrades; add a threshold.
- Test types: smoke, average load, stress, soak, spike, breakpoint; start with smoke; simple load patterns.
- k6 2.0 removed the externally-controlled executor and old cloud commands; `--summary-mode` replaces `--no-summary`.
