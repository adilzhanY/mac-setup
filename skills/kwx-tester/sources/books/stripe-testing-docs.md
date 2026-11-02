# Stripe testing documentation (billing testing, test clocks, webhooks, idempotency, stripe-node)

- Author: Stripe
- Year: living documentation, read 2026-10-31 (served in German to this machine; read in that language, facts checked against the English API page for idempotency)
- Legal URL: https://docs.stripe.com/billing/testing ; https://docs.stripe.com/billing/testing/test-clocks/api-advanced-usage ; https://docs.stripe.com/webhooks ; https://docs.stripe.com/api/idempotent_requests ; https://github.com/stripe/stripe-node (README)

## What I read

Billing testing guide, test clock advanced usage including limits, the webhooks guide sections on local testing, retries, order, duplicates and signature tolerance, the idempotent requests API page, and the stripe-node README section on testing webhook signing.

## Key lessons used in backend/external-services-and-time.md (also api-testing.md, backend.md)

- Separate sandboxes for CI and local development.
- Test cards 4242 (success), 4000 0000 0000 0341 (fails when charged), 4000 0027 6000 3184 (3D Secure).
- Test clocks: create with `frozen_time`, attach customers, advance up to two intervals at a time, wait for `test_helpers.test_clock.ready`, three customers per clock, three subscriptions per customer, deleted after 30 days, list endpoints hide clock objects.
- Webhooks: retries up to three days live, three times over hours in sandbox; order not guaranteed; duplicates happen; dedupe on event id; 5 minute default signature tolerance, never 0.
- `stripe listen --forward-to`, `stripe trigger`; triggered events carry fake data.
- Idempotency (v1): first response saved including 500s; keys up to 255 chars; pruned after at least 24 hours; different parameters error; validation failures and concurrent conflicts are not saved.
- `generateTestHeaderString` signs test payloads.
