# Software engineering

## When this playbook applies

- Build a feature: "add login", "add checkout", "add an export button".
- Fix a bug: "this crashes sometimes", "users see the wrong total".
- Refactor: "clean up this module", "split this file", "make it faster".
- Review code: "review this PR", "is this safe to merge".
- Design or change an API: new endpoint, new webhook, versioning, pagination.
- Security work: auth, sessions, rate limits, secrets, permissions, uploads.
- Infrastructure: deploys, backups and restores, CI, monitoring, scaling, migrations.

## The expert

Pick the one whose failures this request would cause, and adapt the description to the exact case. It goes on the `Expert:` line of the output block; the rewritten task itself carries the moves, never a persona line (`method/expert.md`).

- **Staff backend engineer, 12 years, payments and billing at a card processor.** Fits checkout, invoices, refunds, subscriptions, anything that moves money or must happen exactly once.
- **Application security engineer, 10 years, web pentesting and OWASP ASVS audits.** Fits login, signup, password reset, rate limits, file upload, admin panels, any endpoint reachable by strangers.
- **Site reliability engineer, 8 years, on call for a high traffic service at a large cloud company.** Fits deploys, backups, restores, migrations, alerts, timeouts, "it is slow", "it went down".
- **Principal engineer, 15 years, maintaining a large legacy codebase.** Fits refactors, "clean this up", upgrades, and reviews of large diffs.
- **API platform engineer, 9 years, public developer APIs used by thousands of clients.** Fits new endpoints, SDKs, webhooks, breaking changes, pagination, error formats.

## Moves the expert makes unasked

1. **Writes down what "done" means as checkable behaviour before coding.**
   Why: without it the author grades their own work against what they happened to build.
   Check: the task or PR lists acceptance cases with inputs and expected outputs, written before the code.

2. **Asks "what can a stranger do with this?" for every new input and endpoint (threat model in four questions: what are we building, what can go wrong, what do we do about it, did we do a good job).**
   Why: happy path tests never exercise abuse paths, so they ship open unless someone lists them.
   Check: a short list of abuse cases exists and each has a test or a written reason it is out of scope.

3. **Derives the client IP only from a trusted proxy hop, never from the leftmost X-Forwarded-For value.**
   Why: any client can send that header, so a rate limit keyed on it is bypassed by changing one string.
   Check: a test sends a forged X-Forwarded-For and the limiter still counts the request against the real peer.

4. **Makes login protection unable to lock out a real user on a stranger's behalf:** a hard limit per client address (from a trusted proxy setting, never a raw X-Forwarded-For) plus a growing delay per account that never refuses the right password, and an attempt limit on every other endpoint that checks a secret (change password, delete account, passphrase).
   Why: a hard per-account lockout lets anyone who knows a username deny that person access.
   Check: after the threshold, the real owner can still get in (delay, CAPTCHA, or reset flow), and the lock is temporary with growing delays.

5. **Makes every money-moving or side-effecting request idempotent.**
   Why: networks retry, users double click, and the result is a double charge or a duplicate order.
   Check: sending the same request twice with the same idempotency key creates one charge and returns the stored first response.

6. **Stores money as integer minor units or exact decimals, with a currency, and names the rounding rule.**
   Why: binary floats cannot hold 0.10 exactly, so totals drift by a cent and reconciliations fail.
   Check: grep the money paths for float or double types; a test sums 0.10 three times and gets exactly 0.30.

7. **Stores instants in UTC, and future local events as local time plus an IANA zone ID.**
   Why: "9:00 in Berlin next March" changes meaning if the offset rules change, and day boundaries differ per user.
   Check: tests cover a DST transition day, a user east of UTC+12 or west of UTC-10, and the end of a month.

8. **Validates a backup or import fully before touching live data, and proves restores work.**
   Why: a restore that deletes first and then fails on row 9000 leaves nothing; nobody needs backups, people need restores.
   Check: a test feeds a corrupt backup and the live data is unchanged; a restore has been run end to end at least once.

9. **Reproduces a bug with a failing test before changing code.**
   Why: a fix without a reproduction often fixes a neighbour of the real bug.
   Check: the PR contains a test that fails on the old code and passes on the new.

10. **Pins current behaviour with characterization tests before refactoring.**
    Why: a refactor is only a refactor if behaviour does not change, and you cannot know that without a record of the behaviour.
    Check: tests capturing existing outputs were added before the first structural change, and they pass unchanged after it.

11. **Treats any observable behaviour of an API as a contract (Hyrum's law).**
    Why: clients depend on field order, error text and timing that you never promised.
    Check: the change notes list every visible difference (fields, status codes, ordering, defaults) and how old clients are handled.

12. **Returns errors in one documented shape (for example RFC 9457 problem details) and leaks nothing.**
    Why: inconsistent errors break clients, and stack traces or "user not found" messages help attackers.
    Check: every error path returns the same shape; login says the same thing for a wrong password and an unknown user.

13. **Sets timeouts, limits and pagination on every outbound call and every list.**
    Why: one slow dependency or one huge table takes the whole service down.
    Check: grep for HTTP and DB calls without a timeout; list endpoints have a maximum page size.

14. **Defines how the change is observed in production (a service level indicator, a log line, an alert on symptoms).**
    Why: you cannot tell a broken release from a quiet day without a signal.
    Check: there is a named metric or log to watch after deploy and a rollback step written down.

15. **Says plainly what is not finished, in the PR description or the README that already exists.**
    Why: the next person assumes everything shown works; an unstated gap becomes a production incident.
    Check: each stub or TODO left in the code is named in a line of the PR description or README (a line, not a new document).

## Raw material

What the expert starts from, and where to get it:

- **The real code path, end to end.** Read the handler, the middleware, the data layer and the config that runs in production, not the file the request mentions. Use grep for every caller of what you will change.
- **The real error.** The full stack trace, the exact log lines with timestamps, the failing request and response. Get them from logs, the error tracker, or by reproducing.
- **The real data shape.** A sample of real rows (sanitized), the actual schema from the database (`\d table`, migration files), not the ORM model you assume matches.
- **The primary spec.** The RFC (RFC 9110 for HTTP semantics, RFC 9457 for errors), the vendor's API reference (for example Stripe's idempotency page), the language docs for the exact version in the lockfile.
- **The deploy reality.** The proxy chain in front of the app (CDN, load balancer, ingress), how many hops add X-Forwarded-For, which env vars exist in production.
- **Git history and blame** of the lines you change, plus the linked issues, to learn why odd code exists.
- **The existing tests**, read as a statement of what the authors thought mattered.

What to distrust:

- Blog posts and Q&A answers that do not state a version. Check against the docs for the version you run.
- Code comments and READMEs that claim behaviour. Verify by running.
- The ORM model as a picture of the database. Migrations drift.
- A green CI run as proof of correctness. It proves only what the tests check.
- Your own memory of an API. Look it up.
- An AI summary of a library or a log. Read the source lines.

## Methods and tools

- **Threat modeling (four questions, STRIDE as a prompt list).** For any feature reachable by users or the network. Output is a list of abuse cases.
- **OWASP ASVS.** As a checklist for auth, session, access control, input handling and logging. Level 1 is the floor; ASVS itself recommends level 2 for most applications, and anything with money or personal data needs it.
- **OWASP Authentication and Session cheat sheets.** For login, lockout, reset, MFA and cookies.
- **Idempotency keys with stored responses.** For POST requests that charge, send, create or enqueue.
- **Money value object (amount plus currency, integer minor units or decimal).** For any price, total, balance or tax.
- **Characterization tests (Feathers).** Before refactoring code without good tests.
- **Refactoring in small named steps (Fowler's catalogue), tests green after each.** For any restructuring.
- **Property based testing (Hypothesis, fast-check, proptest).** For parsers, money math, date math, sorting, anything with a large input space.
- **Mutation testing (Stryker, mutmut, cargo-mutants).** To check that the tests actually catch changes, on the critical module only.
- **Static analysis and dependency audit (Semgrep, CodeQL, `npm audit`, `cargo audit`).** On every security sensitive change.
- **DAST scan (ZAP baseline scan, formerly OWASP ZAP).** Against a running staging build of a web app.
- **Load test (k6, wrk).** When the change touches a hot path, a list endpoint, or a rate limit.
- **SLIs and SLOs with symptom based alerts (Google SRE book ch. 4 and 6).** For any new service or endpoint that matters.
- **Restore drill.** For any backup, import, migration or data deletion feature.
- **Blameless postmortem format.** After an outage or a serious bug: timeline, impact, root causes, action items with owners.

## Independent proof

What shows the result is right, other than the author saying so:

- **Tests written from the spec, not from the code.** Expected values come from the acceptance cases or the vendor spec. In one unpublished A/B comparison of AI-built apps, the builds that avoided money, auth and restore defects were the ones with independent tests written from the spec (a small comparison, not a published study). How an agent runs it: write the tests first from the acceptance list, run them, see them fail, then implement.
- **A failing test turned green.** For a bug fix, the reproduction test fails on the old commit. Run: `git stash`, run the test, see red, `git stash pop`, see green.
- **Abuse tests.** Forged X-Forwarded-For, a lockout attempt on someone else's account, the same idempotency key sent twice concurrently, a corrupt backup file, an oversized upload. Each is a scripted request with `curl` or a test client, and the expected result is written before running.
- **Mutation score on the critical module.** Surviving mutants in money or auth code mean the tests do not check it.
- **A real end to end run.** Start the app as a user would, drive the flow with `curl` or the project's E2E runner, and read the database afterwards to confirm the state.
- **Scanners.** Semgrep or CodeQL with zero new high findings; dependency audit clean or each finding explained.
- **A second reviewer who did not write it.** A fresh agent given the diff and the spec, not the author's explanation. Good for finding issues, but its opinion is still a model's judgment: never the only proof.
- **Production signal after deploy.** The named SLI stays inside its objective for an agreed period.

## Amateur mistakes

1. Rate limiting keyed on the first X-Forwarded-For value, which the client controls.
2. Per-account hard lockout after N failures, so a stranger can lock out any user.
3. Checkout or "send" endpoints with no idempotency, so a retry double charges.
4. Money in floats, or totals rounded at display time only.
5. Storing local times without a zone, or computing "today" in server time.
6. Restore or import that deletes current data before validating the new data.
7. Error messages that reveal whether an account exists ("no user with that email").
8. Fixing the visible symptom in one caller while the shared function stays broken for the others.
9. Tests that assert whatever the code currently returns, copied from a run, so they pass by definition.
10. No timeouts on outbound HTTP or database calls.
11. A README that describes the finished vision while half the features are stubs.
12. Secrets in the repo, in logs, or in client side bundles.

## Scope traps

How "deeper" turns into "bigger" here:

- A login request becomes "build a full identity platform with SSO, roles and audit logs."
- A bug fix becomes a rewrite of the module.
- A review becomes a refactor of everything the reviewer dislikes.
- "Add idempotency" becomes "introduce an event sourcing architecture."
- "Make it secure" becomes a full ASVS level 3 audit of an app with no users.
- Monitoring becomes a new observability stack.
- Adding a new framework, queue, or service to solve a problem the current stack already handles.

Deeper means the same deliverable done the way the expert would: the same endpoint, now with the abuse cases closed and tests from the spec.

Typical "not doing" items:

- No new dependencies unless the standard library or an installed one cannot do it.
- No refactor outside the touched code path.
- No new features beyond the request (no SSO, no admin UI, no roles).
- No change to public API shapes unless the request is about the API.
- No migration of unrelated data.
- No performance work without a measured problem.

## Worked example

Vague request: "Add a checkout page to my shop so people can pay."

1. **Expert:** staff backend engineer, 12 years, payments at a card processor.
2. **Unasked moves (top 5):** idempotency on the charge; integer minor units with currency; prices recomputed on the server, never trusted from the client; webhook signature check and dedupe by event ID; an explicit order state machine (pending, paid, failed).
3. **Raw material:** the payment provider's API reference for the pinned SDK version (idempotency, webhooks, test cards), the current product and order schema from migrations, the proxy setup for the webhook URL.
4. **Methods:** idempotency keys with stored responses, Money value object, webhook signature verification, threat model of the checkout endpoint.
5. **Independent proof:** spec tests written first: double submit gives one charge; a client sending a lower price is ignored; a replayed webhook changes nothing; 3 x 0.10 totals exactly 0.30; a forged signature is rejected. Plus one E2E run with a test card and a database check.
6. **Rewritten task:**

```
Add checkout using the provider's hosted payment flow.
Server computes the total from DB prices in integer minor units plus currency.
Every charge call sends an idempotency key tied to the order; repeats return the first result.
Webhooks: verify the signature, dedupe by event ID, move order pending -> paid/failed only.
Write these tests first from this spec: double submit, tampered price, replayed webhook, forged signature, 0.10 x 3.
Done = tests pass + one E2E test-card purchase verified in the DB; the PR description lists what is not finished.
Not doing: refunds UI, coupons, multi-currency, saved cards, new dependencies beyond the provider SDK.
```

## Sources

- OWASP Authentication Cheat Sheet (lockout threshold, window, duration, denial of service, generic errors): https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- OWASP Web Security Testing Guide, Testing for Weak Lock Out Mechanism: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/03-Testing_for_Weak_Lock_Out_Mechanism
- OWASP Application Security Verification Standard: https://owasp.org/www-project-application-security-verification-standard/
- OWASP Threat Modeling Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html
- Threat Modeling Manifesto (the four questions): https://www.threatmodelingmanifesto.org/
- MDN, X-Forwarded-For security and privacy concerns (pick the rightmost untrusted address): https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For
- Stripe, Idempotent requests: https://docs.stripe.com/idempotency
- Martin Fowler, Money pattern (Patterns of Enterprise Application Architecture): https://martinfowler.com/eaaCatalog/money.html
- Jon Skeet, Storing UTC is not a silver bullet: https://codeblog.jonskeet.uk/2019/03/27/storing-utc-is-not-a-silver-bullet/
- Google SRE book, ch. 4 Service Level Objectives: https://sre.google/sre-book/service-level-objectives/
- Google SRE book, ch. 6 Monitoring Distributed Systems: https://sre.google/sre-book/monitoring-distributed-systems/
- Google SRE book, ch. 15 Postmortem Culture: https://sre.google/sre-book/postmortem-culture/
- Google SRE book, ch. 26 Data Integrity (restores, not backups): https://sre.google/sre-book/data-integrity/
- Google Engineering Practices, What to look for in a code review: https://google.github.io/eng-practices/review/reviewer/looking-for.html
- Martin Fowler, Refactoring catalogue: https://refactoring.com/
- Michael Feathers, Working Effectively with Legacy Code (Prentice Hall, 2004), characterization tests: https://www.oreilly.com/library/view/working-effectively-with/0131177052/
- Hyrum's law: https://www.hyrumslaw.com/
- RFC 9110, HTTP Semantics (safe and idempotent methods): https://www.rfc-editor.org/rfc/rfc9110
- RFC 9457, Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc9457
- Martin Kleppmann, Designing Data-Intensive Applications: https://dataintensive.net/
- Hypothesis (property based testing): https://hypothesis.readthedocs.io/
- Stryker (mutation testing): https://stryker-mutator.io/
- OWASP ZAP: https://www.zaproxy.org/
- Grafana k6 (load testing): https://grafana.com/docs/k6/latest/
- Unpublished A/B comparison of AI-built apps (the defect list and the effect of independent spec tests). Not a public source and not peer reviewed; treat it as one practitioner observation.
