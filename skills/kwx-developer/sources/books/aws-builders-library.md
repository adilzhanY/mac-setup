# Amazon Builders' Library (collection of long articles by Amazon principal engineers)

Free on AWS: https://aws.amazon.com/builders-library/ (now served via AWS Builder Center).

## What I read in full

- Timeouts, retries, and backoff with jitter (Marc Brooker)
- Ensuring rollback safety during deployments (Sandeep Pokkunuri)
- Implementing health checks (David Yanacek)
- Avoiding fallback in distributed systems (Jacob Gabrielson)

## What I read in part

- Automating safe, hands-off deployments (Clare Liguori): pipeline stages, one box, waves, bake times, time windows
- Instrumenting distributed systems for operational visibility (David Yanacek): request log practices
- Making retries safe with idempotent APIs (Malcolm Featonby): client request tokens
- Avoiding insurmountable queue backlogs (David Yanacek): queue age metrics, DLQ, backlog math
- Using load shedding to avoid overload (David Yanacek): goodput, testing past the breaking point

## Key lessons

- Timeout on every remote call and cross process call, connect and request; choose from the dependency's p99.9 at an accepted false timeout rate; watch for timers that include connection setup.
- Retries are selfish; retry at a single point in the stack (5 layers x 3 tries = 243x); local token bucket retry limiting instead of circuit breakers; retry only idempotent calls; jitter all periodic work, with deterministic per host jitter.
- Rollback safety: protocol and format changes are the top reason rollbacks fail; two phase deploy (prepare to read both, then activate writing); verify every host reached the prepare phase; bake between phases; readers before writers when rolling forward; serializers versioned, tolerant of and preserving unknown fields; upgrade-downgrade testing with versions coexisting.
- Health checks: liveness, local, dependency checks and anomaly detection; fail open when all fail; restrict fast load balancer checks to local health; prioritize health check responses; extra workers beyond max connections; return the software version to catch zombies; deployments must wait for health.
- Fallback: hard to test, often makes things worse, latent for years; the 2001 shipping speed cache fallback took down Amazon retail and fulfillment. Prefer improving the primary, letting the caller handle errors, pushing data proactively, or converting fallback into always-on failover.
- Deployments: one box for 1 h, rolling at most 33% per batch, first region baked 12 h, later waves 2 to 4 h, minimum request counts during bake, automatic rollback on aggregate alarms, deployment time windows excluding nights, weekends and often Fridays.
- Request logs: one structured entry per unit of work, log intent early, sanitize input, separate success latency, per error reason counters, trace id propagation, do not log payloads that failed to parse, protect logs.
- Idempotency: caller provided client request id; same id returns a semantically equivalent response; same id with different parameters is an error.
- Queues: backlog drain needs extra capacity; measure age of messages (and age at first attempt), DLQ alarms.
- Load shedding: load test far beyond the breaking point; goodput should plateau; keep rejected request latency out of success metrics; false positive rejections should be zero.
