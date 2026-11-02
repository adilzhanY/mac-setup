# External services and time

How to test the parts of a backend that depend on things you do not control: payment providers, webhooks, email, queues, scheduled jobs, and the clock. The default run uses fakes at the network boundary and a controlled clock, so it is fast and deterministic. A small separate suite runs against the providers' sandboxes on a schedule. kwx-developer `~/.claude/skills/kwx-developer/backend/webhooks-and-jobs.md` covers how to build handlers and jobs; this file covers how to prove they work.

## Contents

1. Three layers: fake, sandbox, production smoke
2. Freezing and moving time
3. Payments: Stripe sandbox and test clocks
4. In-app purchases: RevenueCat and store sandboxes
5. Webhooks: signature, retries, duplicates, order
6. Email with Mailpit
7. Queues and background jobs
8. Cron and scheduled jobs
9. Checks

## 1. Three layers: fake, sandbox, production smoke

| Layer | Runs | Uses | Proves |
|---|---|---|---|
| Fake | every test run | MSW (TS) or `wiremock` (Rust) at the HTTP layer; signed fake webhook payloads; in-memory outbox | your code handles every response shape, error and timeout |
| Sandbox | nightly or before release | provider test mode (Stripe sandbox, Google Play license testers, RevenueCat Test Store) | your assumptions about the provider are still true |
| Production smoke | after deploy, read only or with a tiny real transaction the owner approved | real keys | the deploy is wired up (keys, webhook URL, DNS) |

Rules:

1. **Never put live keys in a test environment.** Check that test configs use `sk_test_` style keys, and fail the test run at startup if a live key pattern appears. Evidence: strong (a live charge from a test suite is real money).
2. **Build fakes from recorded real responses,** including real error bodies, and refresh them when the sandbox suite shows drift. Evidence: moderate.
3. **Test every failure mode of the dependency:** 4xx with an error body, 5xx, timeout, connection refused, malformed JSON, slow response beyond your timeout. Evidence: strong (kwx-developer T10).

## 2. Freezing and moving time

Anything with expiry, trials, renewals, rate limits, retries, "send reminder in 3 days" needs a controlled clock. Never sleep in a test.

| Stack | Tool | Snippet |
|---|---|---|
| Vitest | fake timers | `vi.useFakeTimers(); vi.setSystemTime(new Date('2026-01-31T23:59:00Z')); ... vi.advanceTimersByTime(60_000); vi.useRealTimers();` |
| Jest | fake timers | `jest.useFakeTimers({ now: new Date('2026-01-31') }); jest.advanceTimersByTime(ms);` |
| Rust tokio | paused time | `#[tokio::test(start_paused = true)]`, `tokio::time::advance(d)`; see `rust-services-testing.md` |
| Rust, any | injected clock | pass a `Clock` (trait or `fn() -> DateTime<Utc>`) into the service; tests pass a fixed or steppable clock |
| Postgres | parameter | pass `$now` into queries; `now()` is frozen inside a transaction anyway (`database-testing.md` section 8) |
| Stripe | test clocks | section 3 |

Rules:

1. **Inject the clock at the boundary; do not read the system time deep in business logic.** Then every time based rule is a pure function test. Evidence: strong (SWE at Google ch. 13 on fakes; kwx-developer T9).
2. **Test the dangerous instants:** end of month (Jan 31 plus one month), Feb 29, DST start and end in the user's time zone, midnight UTC vs local midnight, year end, leap second free assumptions, timestamps far in the future. Evidence: moderate.
3. **Fake timers and real IO do not mix well.** A fake timer can stall a library that waits on a real socket. Fake only `Date` (`vi.useFakeTimers({ toFake: ['Date'] })`) when the code also does IO. Evidence: moderate (Vitest docs).
4. **Restore real timers in `afterEach`.** A leaked fake clock breaks the next test file. Evidence: moderate.
5. **Run every suite with date code under two zones.** Every test command for code that formats, groups or compares dates runs twice: TZ=<the business zone, e.g. Europe/Berlin> and TZ=Pacific/Auckland (or Pacific/Kiritimati), for the server and the client app. Put both runs in package.json (`"test:tz": "TZ=Pacific/Auckland npm test"`) or a CI matrix entry. At least one test asserts that a displayed time is the business zone wall clock whatever the device zone, unless the spec says device time. Trial: Android A formatted course times in the device zone; a run under Pacific/Auckland would have shown it. Evidence: house rule from the kwx trial (2026-11-01).

## 3. Payments: Stripe sandbox and test clocks

Unit and HTTP tests fake Stripe at the network layer (or use `stripe-mock`, Stripe's HTTP server built from its API spec). The sandbox suite proves the real lifecycle.

Stripe testing facts (Stripe docs, October 2026):

- Use a separate sandbox for CI and for local development so automated tests do not change shared products, prices or webhook endpoints.
- Test cards: `4242 4242 4242 4242` succeeds; `4000 0000 0000 0341` attaches but fails when charged (use it with a short trial to test a failed renewal); `4000 0027 6000 3184` requires 3D Secure.
- Webhooks triggered with `stripe trigger` carry fake data that does not match your objects. The reliable test is a real test subscription and the events it produces.

Test clocks simulate time for Billing objects:

```bash
# create a clock frozen at a start time
curl https://api.stripe.com/v1/test_helpers/test_clocks \
  -u "$STRIPE_TEST_KEY:" -d frozen_time=1767225600 -d "name=annual renewal"

# create a customer on the clock (subscriptions inherit the clock from the customer)
curl https://api.stripe.com/v1/customers -u "$STRIPE_TEST_KEY:" \
  -d test_clock=clock_123 -d payment_method=pm_card_visa \
  -d "invoice_settings[default_payment_method]=pm_card_visa"

# advance time
curl https://api.stripe.com/v1/test_helpers/test_clocks/clock_123/advance \
  -u "$STRIPE_TEST_KEY:" -d frozen_time=1769904000

# clean up (also deletes the clock's customers and cancels their subscriptions)
curl -X DELETE https://api.stripe.com/v1/test_helpers/test_clocks/clock_123 -u "$STRIPE_TEST_KEY:"
```

Limits and behaviour (Stripe docs):

- Time only moves forward. You can advance at most two intervals of the shortest subscription period at a time (two months for a monthly plan); with no subscriptions, up to two years from the frozen start.
- Up to three customers per clock, three subscriptions (including schedules) per customer, ten quotes not linked to customers.
- Advancing takes a few seconds. Wait for the `test_helpers.test_clock.ready` event or poll the clock's `status`, do not sleep a fixed time.
- New invoices stay `draft` for about one hour; advance one more hour to see them finalized and paid.
- List endpoints hide clock objects unless you filter by customer or clock.
- Clocks are deleted automatically 30 days after creation.
- Bank debit payments (for example `us_bank_account`) are not collected during an advance; they are collected after it.

Scenarios to run in the sandbox suite:

| Scenario | Advance | Assert in your app |
|---|---|---|
| Trial converts | past trial end | access stays on; `invoice.paid` handled; trial ending email sent 3 days before (`customer.subscription.trial_will_end`) |
| Renewal fails | past period end with the 0341 card | `invoice.payment_failed` handled; user sees the right state; access per your grace policy |
| Upgrade mid cycle | half a period, then change plan | proration on next invoice matches the spec |
| Cancel at period end | past period end | `customer.subscription.deleted` handled; access removed at the right instant |
| Annual renewal | 12 months in steps | invoice amount, tax, email |

## 4. In-app purchases: RevenueCat and store sandboxes

RevenueCat recommends building with its **Test Store** first (provisioned with every project, needs no store accounts, uses a separate API key; purchases update `CustomerInfo` and entitlements), then testing with the platform sandboxes before review. Evidence: moderate (RevenueCat docs).

Google Play sandbox facts (RevenueCat docs): add testers under Play Console license testing; test subscriptions renew fast and renew at most six times.

| Production period | Sandbox renewal |
|---|---|
| 1 week | 5 minutes |
| 1 month | 5 minutes |
| 3 months | 10 minutes |
| 6 months | 15 minutes |
| 1 year | 30 minutes |

Store sandboxes return unreliable prices and product names; test the flow (purchase, entitlement unlocked, restore, expiry), not the price text.

Backend side: RevenueCat webhooks are tested like any webhook (section 5): an authorization header you configure, duplicates, order. Your server should re-fetch the subscriber from the RevenueCat API rather than trust the event body alone; test that a forged or stale event does not grant access.

Device purchase flows are manual. Hand the user a short checklist (buy, restore on a second install, cancel, let it expire) instead of driving the phone. Check the user's rules: on this kind of machine, injecting taps into an emulator is often forbidden.

## 5. Webhooks: signature, retries, duplicates, order

Provider facts (Stripe docs, typical of others):

- Retries with exponential backoff for up to three days in live mode; in a sandbox, three attempts over a few hours.
- Each retry gets a new timestamp and signature.
- Order is not guaranteed. Do not use the event's `created` time to order events or to detect duplicates; track event ids.
- The same event can arrive more than once; occasionally two different event objects describe the same change (dedupe on `data.object.id` plus `type`).
- Libraries reject signatures older than a tolerance (Stripe default 5 minutes). A tolerance of 0 disables the check.

Test cases for every webhook endpoint:

| Case | Expected |
|---|---|
| Valid signature, new event | 2xx; side effect happens once |
| Missing signature header | 400; no side effect |
| Wrong secret / tampered body (change one byte after signing) | 400; no side effect |
| Valid signature, timestamp older than tolerance (move the clock, do not wait) | 400 |
| Body parsed and re-serialized before verification | test fails: verification must use the raw body bytes |
| Same event delivered twice | second delivery returns 2xx and does nothing |
| Same event delivered twice concurrently | one side effect (unique constraint on event id) |
| Events out of order (`invoice.paid` before `customer.subscription.created`) | final state correct; handler fetches missing objects or defers |
| Handler throws midway | non 2xx so the provider retries; no half applied state (transaction or outbox) |
| Unknown event type | 2xx, ignored |
| Slow processing | handler acknowledges fast and queues the work, if the provider times out quickly |

Signing a test payload with the real library (stripe-node README):

```js
const payload = JSON.stringify({ id: 'evt_test_1', object: 'event', type: 'invoice.paid', data: { object: { id: 'in_1' } } });
const secret = 'whsec_test_secret';
const header = stripe.webhooks.generateTestHeaderString({ payload, secret });

const res = await request(app).post('/webhooks/stripe')
  .set('Stripe-Signature', header).set('Content-Type', 'application/json').send(payload);
expect(res.status).toBe(200);
```

For local end to end checks against the sandbox: `stripe listen --forward-to localhost:4242/webhook` prints the signing secret to use, and `stripe trigger payment_intent.succeeded` sends an event (Stripe CLI docs).

## 6. Email with Mailpit

Never assert that "the email function was called". Assert on the email that arrived.

Mailpit catches all SMTP mail and exposes it over HTTP (Mailpit docs):

```bash
docker run -d --name=mailpit -p 8025:8025 -p 1025:1025 axllent/mailpit
# SMTP on 1025, web UI and API on 8025
```

The Supabase local stack already includes Mailpit on port 54324, so auth emails (confirm, magic link, reset) are testable there.

API endpoints (Mailpit OpenAPI file):

| Need | Call |
|---|---|
| List messages | `GET /api/v1/messages` |
| Search | `GET /api/v1/search?query=to:alice@test.local` |
| Latest message | `GET /api/v1/message/latest` |
| One message | `GET /api/v1/message/{ID}` |
| Delete all | `DELETE /api/v1/messages` |

```ts
await request(app).post('/api/password-reset').send({ email: 'alice@test.local' });
const found = await (await fetch('http://127.0.0.1:8025/api/v1/search?query=to:alice@test.local')).json();
expect(found.messages).toHaveLength(1);
const msg = await (await fetch(`http://127.0.0.1:8025/api/v1/message/${found.messages[0].ID}`)).json();
expect(msg.Subject).toBe('Reset your password');
const link = msg.Text.match(/https?:\/\/\S+reset\S+/)[0];
// follow the link through the API and assert the reset works once, then fails on reuse
```

Cases: the email arrives once (not twice on retry), goes to the right address only, has no other user's data, links work and expire, unsubscribe link present where required, plain text part exists, unicode names render. Rate limit: ten reset requests send one email or are throttled.

Mailpit is shared state. Use a unique recipient per test and search by it, or clear messages in a serial test file.

## 7. Queues and background jobs

Whether the queue is pg-boss, graphile-worker, Supabase Queues (pgmq), BullMQ or a Rust job table:

| Case | How |
|---|---|
| Job does its work | call the handler directly with a payload; assert state |
| Job is idempotent | run the same job twice; assert one side effect (kwx-developer `~/.claude/skills/kwx-developer/backend/webhooks-and-jobs.md` checks) |
| Failure retries | make the dependency fail N times then succeed; assert retries and final success |
| Poison message | always failing job ends in the dead letter state after max attempts; alert or record exists |
| Enqueue is atomic with the write | the business row and the job are created in one transaction (outbox); kill the process between them in a test and assert neither or both exist |
| Ordering assumptions | two jobs for the same entity processed out of order still give the right final state |
| Backoff timing | assert computed next run time with a fake clock, not by waiting |

Run the real queue in integration tests (it is usually just Postgres or Redis in Docker); keep an in-memory fake with the same interface for unit tests, and run one contract test suite against both (SWE at Google, "fakes should be tested").

## 8. Cron and scheduled jobs

- **Test the job function, not the scheduler.** The job takes `now` as an argument; tests call it with chosen instants.
- **Test the schedule expression separately** if it matters ("every weekday at 09:00 Europe/Berlin"): parse it with the same library and assert the next five run times across a DST change.
- **Missed runs:** the server was down at 09:00. Does the job catch up, skip, or run twice when two instances start? Test the chosen behaviour with a lock (advisory lock or a unique "run" row).
- **Overlap:** a run takes longer than the interval. Assert the second run waits or skips, never runs concurrently on the same data.
- **Supabase `pg_cron`:** test the SQL function it calls with a time parameter; check the `cron.job` row exists in a pgTAP test.

## 9. Checks

| Check | Pass condition |
|---|---|
| No live keys | test config uses test keys only; startup guard rejects live key patterns |
| Fakes | third parties faked at the HTTP layer from recorded responses; every failure mode covered |
| Sandbox suite | exists, runs on a schedule, separate from the default run |
| Clock | injected; no `sleep`; dangerous instants tested; real timers restored |
| Two zones | each suite with date code ran under the business zone and a far zone (Pacific/Auckland), server and client, both runs in the Ran block; one test pins the business zone wall clock |
| Stripe | lifecycle scenarios run with test clocks; clocks deleted after tests |
| In-app purchases | Test Store used in development; store sandbox checklist handed to the user for device flows |
| Webhooks | signature (missing, wrong, old), raw body, duplicate, concurrent duplicate, out of order, handler failure covered |
| Email | asserted through Mailpit content, once, right recipient, working and expiring links |
| Jobs | idempotent, retries, dead letter, atomic enqueue covered |
| Cron | job function tested with explicit times; missed run and overlap behaviour tested |
