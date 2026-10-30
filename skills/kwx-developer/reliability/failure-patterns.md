# Failure patterns from real postmortems

Big outages repeat a small number of patterns. Each pattern below comes from a published postmortem, states the rule it teaches, and says how to check for it in a codebase. Use this file when reviewing a design, a config pipeline, a retry loop, a migration or an operational script, and when writing a postmortem.

## Contents

1. Patterns (FP1 to FP18)
2. How to write a postmortem
3. Checks

## 1. Patterns

### FP1. Internally generated data is trusted and crashes the fleet

- **Cloudflare, 18 Nov 2025.** A database permission change made a query return duplicate rows, which more than doubled a Bot Management "feature file" generated every five minutes. The proxy had a limit of 200 features, preallocated for performance; the larger file hit the limit and Rust code called `Result::unwrap()` on the error, panicking every proxy worldwide. Some database nodes produced good files and some bad, so the network failed and recovered every five minutes, which first looked like a DDoS attack.
- **CrowdStrike, 19 Jul 2024.** A content update for Channel File 291 used a template with 21 input fields while the sensor supplied 20. The content validator checked against 21; the interpreter had no runtime bounds check and read past the array, crashing Windows hosts worldwide.
- **Rule.** Validate every file, config and dataset your own systems produce exactly as you validate user input: schema, size, counts, ranges. When the new input is invalid, keep serving with the last good version and alert. Never `unwrap` or index unchecked on it.
- **Check.** Find every place that loads config or data at runtime (`rg -n 'reload|watch|refresh|load_config|readFile' src`) and confirm: validation before swap, last good fallback, a metric for rejected updates.

### FP2. A global, instant push of a non-code change

- **Cloudflare, 2 Jul 2019.** A WAF managed rule with a catastrophically backtracking regular expression was pushed to every server at once (the rule SOP allowed global pushes; software went through staged PoPs). CPU on every HTTP serving core went to 100%. Even "simulate" mode executed the regex.
- **Google Cloud, 12 Jun 2025.** A quota policy with unintended blank fields was replicated globally within seconds and hit a null pointer in a new Service Control code path, crashing it in every region.
- **Rule.** Config, rules and data get the same staged rollout, health gating and rollback as binaries (`deploy-and-rollback.md` D4, D11). A "test mode" that still executes the new logic is not a safe mode.
- **Check.** List every path by which a change reaches production without the deploy pipeline (admin panels, rule editors, flag UIs, replicated tables). Each needs staging and a kill switch.

### FP3. New code path not behind a flag, and the rollout never exercised it

- **Google Cloud, June 2025.** The new quota check code went through region by region rollout weeks earlier, but only ran when a specific policy appeared, so the rollout proved nothing. It had no feature flag and no error handling for blank fields.
- **Rule.** New code paths ship behind a flag, default off; enable gradually after the binary is everywhere. Error handling for malformed data is part of the feature.
- **Check.** PR review: any new branch in a critical request path is behind a flag and has a test for malformed input.

### FP4. Crashing on bad input instead of failing open or rejecting the input

- **Google Cloud, June 2025** ("improve our static analysis and testing practices to correctly handle errors and if need be fail open"), **Cloudflare 2025**, **CrowdStrike 2024**.
- **Rule.** Decide per component whether failure should be closed (deny: auth, payments) or open (allow with degraded behavior: quotas, bot scores, recommendations). Write the decision down. A crash is never the chosen behavior.
- **Check.** For each optional or advisory module (scoring, quota, enrichment), find the error branch and confirm it degrades rather than panics.

### FP5. Restart herd with no backoff

- **Google Cloud, June 2025.** As Service Control tasks restarted in us-central1, they all hit the same Spanner table at once; Service Control "did not have the appropriate randomized exponential backoff", the herd overloaded the table, and that region took up to about 2 h 40 min to fully recover while other regions recovered within about 2 hours.
- **Cloudflare, Nov 2025.** After the fix, a backlog of logins plus retries overwhelmed the dashboard.
- **Rule.** Every client, including startup code that loads config, uses capped exponential backoff with jitter; recovery is planned for the thundering herd (ramp traffic back, see `resilience-patterns.md`).
- **Check.** `rg` for startup fetch and reconnect loops; each has backoff with jitter and a cap.

### FP6. Retries multiply load during an overload

- **SRE book, ch. 22**: a frontend with 10 retries per request turned a 1% overload into a meltdown that continued after load dropped. Retries at 3 layers create 64x load on the database.
- **Rule.** Retry at one layer, at most 3 attempts, with a retry budget, and return "overloaded, do not retry".
- **Check.** `resilience-patterns.md` checks R6 to R12.

### FP7. A fallback that is worse than the failure

- **Amazon, about 2001 (AWS Builders' Library).** When the shipping speed cache failed, web servers fell back to querying the supply chain database directly. When all caches failed together the database locked up, taking down the website and every fulfillment center.
- **Rule.** No fallback that sends more load to a shared dependency. Prefer failing the feature.
- **Check.** `rg -n -i 'fallback|catch.*(db|query|fetch)' src` and review any catch that calls a heavier path.

### FP8. Health checks that amplify failure

- **AWS Builders' Library.** A bug made some web servers render blank error pages very fast; the server did not know it was unhealthy, and the load balancer favored the fast servers, sending them more traffic. Deep health checks that fail on a shared dependency remove the whole fleet at once.
- **Facebook, 4 Oct 2021.** A maintenance command took down the whole backbone. DNS servers, by design, withdrew their BGP routes when they could not reach the data centers, which made Facebook unreachable globally. Internal tools depended on the same DNS, and data center access controls slowed physical recovery.
- **Rule.** Liveness checks the process only; readiness checks local health; dependency health drives alerts, not automatic removal. Rely on fail-open when every target is unhealthy. Recovery tooling must not depend on the system that is down.
- **Check.** `resilience-patterns.md` R28 to R33; list your incident tools (VPN, SSO, dashboards, deploy) and what each depends on.

### FP9. A short blip triggers automation that causes a long outage

- **GitHub, 21 Oct 2018.** 43 seconds of lost connectivity during network maintenance made Orchestrator fail MySQL primaries over to the West Coast. Writes then landed in two regions, and recovery took 24 hours and 11 minutes. GitHub chose data integrity over availability and paused webhooks and Pages builds.
- **Rule.** Automated failover across regions needs a delay and a human or quorum check proportional to its blast radius; automation that cannot be undone quickly must be slow to trigger. When forced to choose, protect data integrity first and degrade features (pause background jobs) instead of serving inconsistent data.
- **Check.** List automatic failover and auto remediation; for each, document the trigger threshold, the minimum duration, and how to undo it.

### FP10. An operational command with too much reach

- **AWS S3, 28 Feb 2017.** A command from an established playbook, run to remove a few billing servers, had one input entered incorrectly and removed a large part of the index and placement subsystems. Those had not been fully restarted in years, and restart plus safety checks took hours. The AWS status dashboard itself depended on S3.
- **GitLab, 31 Jan 2017.** A tired engineer ran `rm -rf` on the primary database directory instead of the secondary; 300 GB were gone in seconds.
- **Rule.** Destructive tools: dry run by default, rate limited, refuse to go below a minimum capacity, print the exact target and require it typed back. Restart and recovery paths are exercised regularly, at production size. Status pages are hosted independently.
- **Check.** Review scripts in `scripts/`, `bin/`, runbooks: `rg -n 'rm -rf|DROP|DELETE FROM|TRUNCATE|terminate|destroy' scripts bin`. Each has a dry run and a target confirmation.

### FP11. Backups that were never restored

- **GitLab, Jan 2017.** Of five backup or replication mechanisms, none worked when needed: `pg_dump` ran with version 9.2 against a 9.6 database and silently produced nothing, failure emails were rejected, and snapshots were not enabled. Recovery used a 6 hour old staging snapshot.
- **Rule.** A backup exists only if an automated restore of it succeeds on a schedule, with the restored data checked (row counts, latest timestamp). Backup failures alert loudly. Tool versions match the server.
- **Check.** A scheduled job restores the latest backup to a scratch database and verifies it; `ci-pipeline.md` section 7.

### FP12. Integer overflow on ids and counters

- **GitHub, May 2021.** A foreign key on the scoped tokens table hit the 32 bit integer maximum; Actions and Pages failed for 9 h 48 min. **Heroku, Jun 2023.** A foreign key column was a smaller type than the primary key it referenced, and overflowed.
- **Rule.** Ids and foreign keys are `bigint` or UUID from the start; foreign key types match their referenced key; alert when any sequence passes 50% of its type's range.
- **Check.** SQL: `select sequencename, last_value, max_value from pg_sequences where last_value > max_value * 0.5;` and compare FK column types with referenced columns.

### FP13. Time and dates

- **Azure, 29 Feb 2012.** Certificates valid for "one year" were computed as the current date with the year plus one, producing an invalid date of 29 Feb 2013, which broke VM creation.
- **Leap seconds** (Linux 2012, Cloudflare DNS 2017: time went backwards and code assumed it never does). **Mozilla, May 2019:** an intermediate certificate expired and disabled most Firefox add-ons.
- **Rule.** Use a date library for calendar math; measure durations with a monotonic clock (`performance.now()`, `process.hrtime.bigint()`, `std::time::Instant`), never wall clock subtraction; store UTC; test leap days, DST transitions, month ends and year ends; monitor certificate and domain expiry with alerts weeks ahead.
- **Check.** `rg -n 'getFullYear\(\) *\+ *1|setFullYear|Date\.now\(\) *-' src`; `rg -n 'SystemTime::now\(\)' src` used for durations; expiry monitor exists.

### FP14. Cache TTL or traffic shape changes overload the database

- **GitHub, 2022 to 2023 availability reports.** Client apps had quietly increased read traffic 10x; a weekend change shortened a user settings cache TTL from 12 h to 2 h; at Monday peak the combined load overwhelmed the database.
- **Rule.** Treat cache TTL, cache key and eviction changes as capacity changes: estimate the miss rate impact, roll out gradually, and watch DB load. Track per client request rates.
- **Check.** PRs that change TTLs or cache keys include a load estimate.

### FP15. A database upgrade or failover goes live without statistics or warm caches

- **CircleCI, Apr 2025.** A blue green upgrade of the workflows database succeeded, but the new database had no planner statistics, so queries ran against disk. **GitHub**: a schema migration triggered failover to a replica with a cold buffer pool, which then failed back.
- **Rule.** After an upgrade, restore or failover, run `ANALYZE` and warm critical caches before taking full traffic; ramp traffic.
- **Check.** The upgrade runbook includes `ANALYZE` (or `vacuumdb --analyze-in-stages`) and a ramp step.

### FP16. Dead code and reused flags

- **Knight Capital, 1 Aug 2012.** New code reused a flag that used to enable "Power Peg", code unused since 2003. One of eight servers did not get the new deploy, so that server ran Power Peg on live orders; over 4 million orders in 45 minutes, a loss of more than 460 million dollars (SEC order 34-70694).
- **Rule.** Delete dead code and its flag together; never reuse a flag name; deploys verify every target got the new version (version in health checks, deploy fails on mismatch).
- **Check.** Flag registry with owners and expiry; `rg` for flags no longer read; deploy pipeline compares running versions after rollout.

### FP17. Two rare bugs plus a recent change

- **Stripe, 10 Jul 2019.** A database shard could not elect a new primary because of a failover bug that arrived with a minor version upgrade three months earlier, combined with a node in a specific state. The widely used shard starved API compute. The second, longer outage came from the remediation: rolling back to a "known stable" version interacted badly with a recent configuration change.
- **Rule.** Rollbacks are changes too; know what else changed since the version you roll back to (config, schema, flags). Monitor for nodes that silently stop reporting (Stripe added monitoring for nodes that stop reporting replication lag). Isolate shards so one failing shard cannot exhaust shared request capacity (bulkheads: per shard concurrency limits).
- **Check.** Each shared resource pool (threads, connections) has per dependency or per shard limits.

### FP18. Error and diagnostic output overwhelms the system

- **Cloudflare, Nov 2025** remediation: "Eliminating the ability for core dumps or other error reports to overwhelm system resources." **AWS**: a fallback that logs a stack trace per failure turned a CPU bound app into an I/O bound one.
- **Rule.** Rate limit error logging and crash reporting; sample repeated identical errors; cap core dumps.
- **Check.** Logger or reporter has rate limiting or sampling configured for errors.

### Cross-cutting lessons

- **The trigger is rarely the root cause.** Most big outages combine a latent weakness (no bounds check, no backoff, a 32 bit id, untested restore) with a routine trigger (a permission change, maintenance, a typo). Fix the latent weaknesses; triggers will always come.
- **Recovery paths decay.** Restarting a subsystem, restoring a backup, failing back, using the kill switch: if it is not exercised regularly, it fails or is slow when needed (S3 2017, GitLab 2017, Cloudflare 2019 bypass access).
- **Make the system observable from outside itself.** Synthetic checks and client side metrics caught Cloudflare 2019 within minutes; a server that cannot log cannot report its own failure.

## 2. How to write a postmortem

Triggers for writing one (decide before incidents, SRE book ch. 15): user visible downtime or degradation over a threshold, any data loss, on-call intervention (rollback, traffic reroute), resolution time over a threshold, or a monitoring failure (a human found it before alerts did).

Template:

```markdown
# <Date> <one line description of user impact>
Status: draft | reviewed | actions complete
## Summary            Two or three sentences: what users saw, how long, how bad.
## Impact             Who, how many, which features, data loss (yes/no, how much), duration in UTC.
## Timeline (UTC)     Detection, escalation, key decisions, mitigation, resolution. Include what we believed at each point.
## Root causes        The latent conditions and the trigger, as a causal chain. No names.
## What went well     Detection, tools, decisions that shortened the incident.
## What went poorly   Including where we were lucky.
## Action items       Each: type (prevent, detect, mitigate), owner, priority, tracking issue.
## Supporting data    Graphs, log queries, links.
```

Rules: blameless (systems and processes are fixed, people are not blamed; assume everyone acted reasonably with the information they had), reviewed by someone senior before publishing ("an unreviewed postmortem might as well never have existed"), shared widely, no personal data, and action items tracked to completion with owners. Prefer action items that remove a class of failure (a validation, a bound, a staged rollout) over "be more careful".

## 3. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Runtime loaded config/data validated | Schema + size limits + last good fallback | `rg -n 'reload|refresh|watch' src` and read each loader |
| No panics on loaded data | No `unwrap`/`expect`/unchecked index in loaders | `rg -n '\.unwrap\(\)|\.expect\(|\[\w+\]' src/config src/loader*` (Rust) |
| Non-code changes staged | Config, rules, flags go through staged rollout | Review the change pipelines; each has stages and rollback |
| New critical code paths flagged | Flag default off for new request path logic | PR checklist |
| Backoff on startup and reconnect | Every reconnect/startup fetch loop has jittered backoff | `rg -n 'reconnect|retry|connect\(' src` and read |
| Destructive scripts guarded | Dry run default, target confirmation, limits | `rg -n 'rm -rf|DROP |TRUNCATE|DELETE FROM|terminate' scripts bin` |
| Restore tested | Scheduled restore job exists and passes | CI schedule or cron; last run status |
| Sequence headroom | No sequence above 50% of max | `select sequencename, last_value, max_value from pg_sequences where last_value > max_value/2;` |
| FK types match | FK columns equal referenced column type | SQL comparing `information_schema` columns for each FK |
| Monotonic durations | No wall clock subtraction for durations | `rg -n 'Date\.now\(\) *-|new Date\(\) *-' src`; `rg -n 'SystemTime::now' src` |
| Cert expiry monitored | Alert 21+ days ahead | Monitoring config or scheduled job |
| Error log rate limited | Sampling or rate limit on repeated errors | Logger/reporter config |
| Postmortem criteria written | Criteria documented before incidents | `rg -il 'postmortem' docs` |
