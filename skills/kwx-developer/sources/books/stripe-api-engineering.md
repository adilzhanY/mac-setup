# Stripe API engineering: docs and engineering blog, plus brandur.org on idempotency keys

Legal free sources:
- Idempotent requests: https://docs.stripe.com/api/idempotent_requests
- Webhooks: https://docs.stripe.com/webhooks (read in full, German locale was served)
- Scaling your API with rate limiters: https://stripe.com/blog/rate-limiters
- APIs as infrastructure: future-proofing Stripe with versioning: https://stripe.com/blog/api-versioning
- Designing APIs for humans: object IDs: https://dev.to/stripe/designing-apis-for-humans-object-ids-3o5a
- Implementing Stripe-like idempotency keys in Postgres (Brandur Leach, ex-Stripe): https://brandur.org/idempotency-keys

## Key lessons used in backend/

- Idempotency keys: client generated V4 UUIDs, up to 255 chars, no personal data; server saves status and body of the first execution (including 500s) and replays it; parameter mismatch errors; validation failures and concurrent conflicts are not saved; keys pruned after 24 h. Brandur: unique (user_id, key), request fingerprint, locked_at, recovery points per atomic phase, SERIALIZABLE, 409 on concurrent use, derived keys for downstream calls, staged jobs (outbox), completer and reaper, keep 24 to 72 h.
- Webhooks: verify on the raw body; HMAC-SHA256 `v1` scheme only (ignore others against downgrade); constant time compare; 5 minute default tolerance; multiple signatures during secret rolling (old secret valid up to 24 h); ack 2xx before complex logic; process with an async queue; 3xx is a failure; retries up to 3 days in live mode; duplicates happen, dedupe by event ID; no ordering guarantee, do not use `created` for ordering; exempt the route from CSRF; subscribe only to needed events; fetch the latest object.
- Rate limiters: request rate limiter (token bucket in Redis) first, concurrent request limiter, fleet load shedder reserving 20% for critical traffic with 503, worker utilization shedder as last resort; dark launch; fail open on limiter errors; actionable messages; 429 vs 503.
- Versioning: date versions, account pinned on first request, `Stripe-Version` header override, version change modules transform responses backwards so old versions stay out of core code. Adding endpoints and fields is compatible; removing, renaming or retyping is not.
- Prefixed IDs (`cus_`, `pi_`, `sk_live_`): readable, polymorphic lookup, greppable for secret scanning, live/test separation.
