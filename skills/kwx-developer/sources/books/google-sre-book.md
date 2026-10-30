# Site Reliability Engineering (Google, 2016) and The Site Reliability Workbook (Google, 2018)

Legal free editions by the authors: https://sre.google/books/ (CC BY-NC-ND 4.0). Read online chapter by chapter.

## What I read

SRE book: ch. 3 Embracing Risk (skimmed), ch. 4 SLOs (skimmed), ch. 6 Monitoring Distributed Systems (full), ch. 8 Release Engineering (full), ch. 10 Practical Alerting (skimmed), ch. 15 Postmortem Culture (full), ch. 17 Testing for Reliability (skimmed), ch. 21 Handling Overload (full), ch. 22 Addressing Cascading Failures (full).
Workbook: ch. 4 Monitoring (skimmed), ch. 5 Alerting on SLOs (key sections and tables), ch. 10 Postmortem Culture (skimmed), ch. 16 Canarying Releases (key sections).

## Key lessons used in reliability/

- Four golden signals: latency, traffic, errors, saturation. Page on symptoms, use causes for debugging. Every page must be urgent, actionable, need intelligence, and be about a novel problem.
- Measure latency as histograms with roughly exponential buckets; the mean hides the tail; a backend's p99 becomes the frontend's median under fan out.
- Remove alert rules not exercised in a quarter and signals on no dashboard or alert.
- Cascading failures: overload is the most common cause. Queues sized 10x the thread pool turn 100 ms into 1.1 s; prefer queue length at most 50% of threads for steady load. Shed load with 503 when in-flight requests exceed a limit; consider LIFO or CoDel.
- Retries: randomized exponential backoff, per request limit, per process retry budget (example: 60 per minute), retry at one layer only (3 retries at 3 layers = 64x load), separate retryable and permanent errors, return an explicit "overloaded, do not retry" status.
- Google uses at most 3 attempts per request and a per client retry ratio under 10%, which caps growth near 1.1x instead of 3x. Adaptive client throttling rejects locally once requests exceed K x accepts (K = 2 preferred).
- Deadlines: set one at the top, propagate the remaining time, check it before each stage, cancel downstream work. Deadlines orders of magnitude above mean latency cause thread exhaustion under bimodal latency (worked example: 5% hung requests with a 100 s deadline lead to about 80% errors).
- Latency cache vs capacity cache; cold caches after restarts; ramp load slowly.
- Separate process health (for the scheduler) from service health (for the load balancer); health check driven restarts can make an overload worse.
- Load test to failure and beyond, test recovery, test with gradual and impulse load, test noncritical backends that blackhole.
- Release engineering: hermetic, reproducible builds; build ID on every binary; tests rerun on the release branch; config treated like code and versioned with binaries; frequent small releases.
- Postmortem triggers decided in advance (user visible downtime, any data loss, on-call intervention, long resolution, monitoring failure). Blameless. "An unreviewed postmortem might as well never have existed." No end user data in postmortems.
- SLO alerting (Workbook ch. 5): alert on error budget burn rate, multiwindow. Page at 2% budget in 1 h (burn 14.4) and 5% in 6 h (burn 6); ticket at 10% in 3 days (burn 1). Short window 1/12 of the long one for fast reset. "for: duration" clauses miss bursty errors; a 5 min on / 5 min off 100% error pattern never fired while burning 35% of the budget.
- Canarying (Workbook ch. 16): canary vs control at the same time beats before vs after; start from SLIs, at most about a dozen metrics; canary impact on the error budget is proportional to traffic exposed (5% canary x 20% errors = 1% overall).
