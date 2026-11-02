# oha, vegeta and wrk2 READMEs (load generators)

- Authors: hatoo (oha); Tomas Senart (vegeta); Gil Tene (wrk2)
- Year: read 2026-10-31 (oha 1.16, vegeta 12.13)
- Legal URL: https://github.com/hatoo/oha ; https://github.com/tsenart/vegeta ; https://github.com/giltene/wrk2

## What I read

The oha README options and the coordinated omission section, vegeta README usage and rate flag, wrk2 README.

## Key lessons used in performance/load-testing.md (also performance.md)

- oha `-q` plus `--latency-correction` measures from the scheduled time; ignored without `-q` or `--burst-delay`; `--disable-keepalive`; JSON output.
- vegeta attacks at a constant `-rate` and is designed to avoid coordinated omission; `-rate=0` means as fast as possible.
- wrk2 `-R` constant throughput; `--u_latency` prints the uncorrected distribution.
