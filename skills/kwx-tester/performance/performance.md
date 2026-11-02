# Performance testing

How to find out, with numbers you can defend, whether a system is fast enough and stays fast enough: under normal load, under stress, over hours, during spikes, and as code changes. kwx-developer `reliability/performance.md` covers budgets and profiling from the builder's side (measure before optimising, P1 to P12). This folder is the tester's side: designing the test, generating load correctly, reading percentiles, avoiding the measurement traps that make most published numbers wrong, and reporting results honestly.

## Contents

1. Kinds of performance tests
2. The rules that matter most
3. Requirements: budgets as percentiles
4. Percentiles, not averages
5. Coordinated omission
6. The test environment problem
7. Active benchmarking: find the limiter
8. Reporting results honestly
9. Files in this folder
10. Checks

## 1. Kinds of performance tests

| Test | Question | Shape | Typical length (k6 guidance) |
|---|---|---|---|
| Smoke | does the script work, and is the system fine at minimal load? | very low load | seconds to minutes |
| Average load (load test) | does it meet the budget at normal production traffic? | ramp up, plateau, ramp down | 5 to 60 minutes |
| Stress | how does it behave above normal, near its limits? | higher plateau | 5 to 60 minutes |
| Soak (endurance) | does it degrade over time: leaks, growing queues, filling disks, connection exhaustion? | average load | hours |
| Spike | does it survive a sudden surge, and recover? | jump to very high, short | a few minutes |
| Breakpoint (capacity) | where does it break, and how? | load rises step by step until failure | as long as needed |
| Scalability | does throughput grow with resources (instances, cores)? | same test at 1, 2, 4 units | per run |
| Benchmark | is A faster than B, or did this commit regress? | repeated controlled runs of one operation | seconds to minutes per case |

Start with a smoke test, then an average load test; the others answer specific risks. No single type covers everything (k6 docs). Evidence: moderate.

## 2. The rules that matter most

1. **Write the requirement before the test, as percentiles at a stated load.** "p95 under 200 ms and p99 under 500 ms at 50 requests per second with under 1% errors." A test without a pass condition produces numbers, not answers. Evidence: strong (Gil Tene; Google SRE book).
2. **Report percentiles and the maximum, never the average alone, never the standard deviation.** Latency is not normally distributed; averages and standard deviation hide the tail users feel. Evidence: strong (Gil Tene, "How NOT to Measure Latency"; SRE book).
3. **Generate load at a fixed arrival rate (open model) when you measure latency.** A closed loop generator waits for slow responses and stops measuring exactly when the system is bad (coordinated omission). Evidence: strong (Gil Tene; k6 docs; wrk2).
4. **Test your measurement tool before trusting it.** Run it against a fake server with a known pause and check the report shows the pause. Evidence: strong (Gil Tene's first lesson).
5. **Run the load generator on a different machine from the system under test** (or at least check it is not the bottleneck). Evidence: strong (Brendan Gregg, active benchmarking).
6. **Use a production like environment and data volume,** and state every difference in the report. Debug builds and dev servers lie by 2x to 10x (kwx-developer P3). Evidence: strong.
7. **Find the limiter while the test runs.** If you cannot say why the result is X and not 2X, the result is not explained (Brendan Gregg). Watch CPU, memory, disk, network and connection pools with the USE method. Evidence: strong.
8. **Change one thing per comparison run, and repeat runs.** One run is an anecdote; compare distributions. Evidence: strong.
9. **Error rate is part of the result.** A fast response that is an error is not a success. Count errors and check response content in the load script. Evidence: strong.
10. **Never load test production or a shared service without the owner's explicit yes and a stop plan.** This includes a hosted Supabase project, a payment sandbox, or a third party API with rate limits. Evidence: strong (incidents, provider terms).
11. **Keep regression checks in CI relative, not absolute.** Shared CI runners are noisy; compare against a baseline on the same runner type, or count instructions. Evidence: moderate (criterion FAQ, CodSpeed docs).
12. **Report honestly:** environment, versions, load shape, duration, percentiles, max, errors, what limited it, what you did not test. Evidence: moderate.

## 3. Requirements: budgets as percentiles

Gil Tene's interview method turns "we need 20 ms average" into a real requirement by asking about the worst case and how often slow responses are acceptable. The result looks like:

| Percentile | Budget |
|---|---|
| 50% | better than 20 ms |
| 90% | better than 50 ms |
| 99.9% | better than 500 ms |
| 100% (max) | better than 2 s |

Questions to ask the owner (or infer from kwx-developer `reliability/performance.md` section 2 budgets when they do not know):

1. What load: requests per second at a normal peak hour, and at the highest spike you expect?
2. Which operations matter: list the top 3 to 5 endpoints or user actions.
3. What is "too slow" for a user here, and how often is it acceptable?
4. What is never acceptable (the max)?
5. What error rate is acceptable under load?

Remember that a user makes many requests per session. If a page load triggers 20 requests, the chance that at least one hits the p99 is 1 - 0.99^20, about 18%. Tene's point: "a single user may have 100 interactions per session", so the 99th percentile is what many users see. Evidence: strong (simple probability; Tene).

## 4. Percentiles, not averages

- **Latency distributions are multi modal:** a fast mode, a slower mode (cache miss, GC, lock wait) and rare freezes. A mean describes none of them. Evidence: strong (Tene).
- **The SRE book:** "Using percentiles for indicators allows you to consider the shape of the distribution", and a simple average "can obscure these tail latencies, as well as changes in them". Its example: a typical request near 50 ms while 5% of requests are 20 times slower. Evidence: strong.
- **Always record the max,** and ask what caused it. Evidence: strong (Tene: "Always measure Max time").
- **Percentiles cannot be averaged.** The mean of per minute p99 values is not the p99 of the hour. Aggregate raw data or mergeable histograms (HdrHistogram), not summary numbers. Evidence: strong.
- **Watch the aggregation window.** A 1 minute average rate hides bursts that last seconds (SRE book example: 200 req/s on even seconds and 0 on odd ones averages to 100). Evidence: strong.
- **Enough samples:** a p99 from 200 requests is two data points. For a stable p99 you want thousands of samples; for p99.9, tens of thousands. Evidence: moderate (basic statistics).
- **HdrHistogram** records values over a wide range (for example 1 microsecond to 1 hour) at fixed precision with constant cost, and is what wrk2 and many tools use. Evidence: moderate (Tene).

## 5. Coordinated omission

The trap (Tene): a simple load tester sends a request, waits for the response, records the time, sends the next. When the server stalls, the tester also stalls, so it sends fewer requests during the bad period and records only one slow sample instead of all the requests that real users would have sent. The tool "coordinates" with the server to avoid measuring the problem.

Tene's example: a system answers 100 requests per second in 1 ms, then freezes for 100 seconds. A closed loop tester records 10,000 samples at 1 ms and one at 100 s. It reports p99.99 = 1 ms and an average of 10.9 ms. The honest description: the average over the 200 s is about 25 s, the median is 1 ms, p75 is about 50 s, p99.99 is about 100 s. The naive numbers are wrong by orders of magnitude. The wrk2 README shows the same on a real run: with a 1.4 s pause, the corrected p99 was about 1.27 s and the uncorrected one about 6 ms, roughly 200x apart.

How to avoid it:

| Tool | How |
|---|---|
| k6 | use an arrival rate executor (`constant-arrival-rate`, `ramping-arrival-rate`); watch `dropped_iterations` (k6 docs call the closed model problem coordinated omission) |
| oha | `-q <rate> --latency-correction` (measures from the scheduled send time) |
| vegeta | constant `-rate`; designed to avoid coordinated omission (vegeta README) |
| wrk2 | `-R <rate>`; `--u_latency` also prints the uncorrected numbers for comparison |
| wrk, ab, plain closed loops | do not use for latency percentiles; fine for a rough max throughput number |

Rule: **in an open model test, if the generator cannot start requests on time (k6 `dropped_iterations` above zero, or the achieved rate below the target), the run is invalid or the system is saturated; say which.** Evidence: strong (k6 docs).

## 6. The test environment problem

Most performance results are wrong because of the environment, not the code. Before running:

| Factor | What to do |
|---|---|
| Build | release or production build (`--release`, `next build && next start`, `NODE_ENV=production`) |
| Data volume | production like row counts and payload sizes; an empty table makes every query fast |
| Caches | decide warm or cold, state it, and warm up before measuring warm |
| Neighbours | no other heavy processes; on cloud VMs, noisy neighbours vary between runs |
| CPU frequency | laptops throttle on battery and heat; note the power mode; for benchmarks pin the governor if you can |
| Network | generator to server path similar to real clients, or state the difference (same host is unrealistically fast) |
| Generator capacity | the generator's CPU below about 70%; otherwise it is the bottleneck |
| Limits | file descriptors (`ulimit -n`), connection pool sizes, rate limits of the platform |
| Versions | record app commit, runtime, database, OS, tool versions |
| Hosted backends | Supabase and other platforms have compute tiers, pooler connection limits and auth rate limits that differ from local; a local run does not predict hosted behaviour and the reverse |

Gregg's checklist of what disturbs benchmarks: other system events or neighbours, software resource controls or the network throttling the test, a single threaded benchmark tool being the limit, different client or server versions between runs, measuring disk instead of file system I/O, and an unrealistic workload. Evidence: strong (Brendan Gregg, active benchmarking).

## 7. Active benchmarking: find the limiter

Passive benchmarking runs the tool and reports its numbers. Active benchmarking analyses the system while the test runs, so the result comes with its cause (Gregg). Steps:

1. Run long enough to reach a steady state (minutes, not seconds).
2. During the run, watch every resource with the USE method: for each resource, check utilization, saturation and errors.
3. Name the limiter and the evidence ("CPU bound in JSON serialization: 1 core at 100% in `pidstat -t 1`, others idle").
4. Only then do statistics on the numbers; statistics on a misconfigured test make wrong results look trustworthy ("iostat first, R later").

USE quick checks on Linux (Gregg's Linux checklist):

| Resource | Utilization | Saturation | Errors |
|---|---|---|---|
| CPU | `mpstat -P ALL 1` (all but idle and iowait); `vmstat 1` us+sy+st | `vmstat 1` column `r` greater than CPU count | `dmesg` |
| Memory | `free -m` | `vmstat 1` columns `si`/`so` (swapping); `dmesg \| grep -i killed` (OOM) | `dmesg` |
| Disk | `iostat -xz 1` `%util` | `iostat -x` queue size above 1, high `await` | `dmesg`, smart tools |
| Network | `sar -n DEV 1` throughput vs link speed | `sar -n EDEV 1` drops, `ss -s` | `ip -s link` errors |
| Software | thread pools, DB connection pool, event loop lag | queue length, waiting acquirers, `pg_stat_activity` waiting rows | timeouts, pool exhaustion errors |

For Postgres backed APIs also watch `pg_stat_statements` (top queries by total time), lock waits, and connection count against `max_connections` and the pooler limit.

## 8. Reporting results honestly

Template for every performance result (paste into the report or PR):

```text
Question:      Does GET /api/feed meet p95 < 200 ms at 50 req/s?
Answer:        Yes up to 50 req/s; no at 80 req/s (p95 410 ms, limiter: DB pool of 10 connections saturated)
Environment:   app abc1234 release build on <machine/tier>; Postgres 17 <tier>; 250k rows in posts
Generator:     k6 2.3.0 on a separate machine, constant-arrival-rate, 0 dropped iterations
Load shape:    ramp 1 min to 50 req/s, hold 10 min, ramp down; warm caches
Results:       p50 38 ms, p90 95 ms, p95 140 ms, p99 260 ms, max 1.9 s; errors 0.02% (all 503 during ramp)
Runs:          3 runs, p95 range 132 to 151 ms
Limiter:       none at 50 req/s (CPU 40%); at 80 req/s pool waits in pg_stat_activity
Not tested:    cold start, spikes, write heavy endpoints, real client network
Raw data:      k6 JSON summary attached
```

Rules:

1. **State what was not tested.** Evidence: moderate.
2. **Give ranges across runs,** not one number. Evidence: strong.
3. **Do not round away the bad news:** report the max and error spikes even when the percentiles pass. Evidence: moderate.
4. **Benchmark claims comparing two options need the same environment, same data, interleaved runs,** and a statement of noise. Gregg's benchmark paradox: if each comparison is closer to a coin toss than you think, winning several in a row is mostly luck. Evidence: moderate.

## 9. Files in this folder

| File | Read when |
|---|---|
| `load-testing.md` | writing and running a load, stress, soak or spike test against an API: k6 scripts, thresholds, scenarios, quick runs with oha or vegeta, Supabase and Postgres backed APIs, reading results |
| `benchmarks.md` | comparing implementations or catching regressions in code: criterion, divan, Vitest bench, tinybench, mitata, CI benchmarking, startup time and frame rate pointers |

Related elsewhere: mobile performance (Android Macrobenchmark, startup, jank) in `../mobile/android-native.md`; web page performance (Core Web Vitals) in `../web/performance-and-seo-checks.md`; profiling and fixing in kwx-developer `reliability/performance.md`.

## 10. Checks

| Check | Pass condition |
|---|---|
| Requirement | written as percentiles and max at a stated load, with an error rate, before the test |
| Test type | chosen for the risk (smoke first, then average load; others as needed) |
| Open model | latency measured with an arrival rate generator; dropped or late requests reported |
| Tool checked | measurement tool validated against a known pause, or a trusted tool used as documented |
| Generator | separate from the system under test, or shown not to be the bottleneck |
| Environment | release build, realistic data, warm or cold stated, versions recorded |
| Permission | no load on production or shared services without the owner's yes and a stop plan |
| Limiter | named with evidence from USE checks |
| Statistics | p50, p90, p95, p99, max, error rate, sample count; several runs with ranges |
| Report | template filled, including "Not tested" |
