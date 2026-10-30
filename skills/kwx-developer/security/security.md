# Security: the rules that are never cut

Read this for any change that touches user input, auth, sessions, permissions, files, URLs fetched by the server, HTML rendering, secrets, dependencies, CI, or payments. These rules survive every "keep it simple" and "smallest diff" instruction: a shortcut here is a vulnerability, not a simplification.

## Contents

1. Never cut: the rules
2. Map: which file to read
3. Security review of a diff in five minutes
4. Checks

## 1. Never cut: the rules

Each rule names the file with the details and the check.

Access control

1. Every request is authorized on the server, against the specific object, with the user and tenant taken from the session. Not found and not yours look the same (404). Client-side checks are UX only. (`../backend/auth.md` section 11)
2. Deny by default: a route or table with no explicit policy is closed. In Supabase, RLS is enabled on every exposed table with `USING` and `WITH CHECK`, and the service role key never reaches a client. (`../backend/auth.md` section 13)
3. Request bodies never bind directly to models; only allowlisted fields are writable, per role. (`input-and-injection.md` section 5)

Input and output

4. Validate every input at the trust boundary with a strict schema (types, lengths, ranges, unknown fields rejected, body size limit). LLM output, webhooks, queue messages and third party responses are inputs. (`input-and-injection.md` section 2)
5. Parameterize every SQL value; identifiers come from allowlists; no `*Unsafe`/`raw` query APIs with input. (`input-and-injection.md` section 3)
6. No shell strings, `eval`, or `new Function` with input; run processes with argument arrays. (`input-and-injection.md` section 4)
7. Render user content as text. Any HTML sink gets sanitized input (DOMPurify / ammonia). User URLs are restricted to http(s). (`browser-security.md` section 1)
8. Server-side fetches of user-influenced URLs go through an SSRF guard: http(s) only, resolved IP checked against private and metadata ranges, no redirects, timeouts. (`input-and-injection.md` section 7)
9. Uploads: authenticated, size-limited while streaming, type checked by content, stored under generated names off the app origin, served with `nosniff` and `attachment`. (`input-and-injection.md` section 8)

Authentication and sessions

10. Passwords hashed with Argon2id (m=19456 KiB, t=2, p=1 minimum) or scrypt/bcrypt; never a fast hash, never encryption. (`../backend/auth.md` section 5)
11. Sessions: opaque random tokens in `HttpOnly; Secure; SameSite` cookies, regenerated on login, deleted server-side on logout. No tokens in `localStorage`. JWTs verified with a pinned algorithm, `iss`, `aud` and `exp`. (`../backend/auth.md` sections 3, 4)
12. Login, reset, OTP and signup are rate limited per account and per IP, and do not reveal whether an account exists. (`../backend/auth.md` section 6)
13. Reset and verification tokens: 32 random bytes, stored hashed, single use, short expiry, link host from config. (`../backend/auth.md` section 7)
14. Cookie-authenticated state changes are protected from CSRF (Fetch Metadata / Origin check or tokens); GET never changes state. (`browser-security.md` section 2)

Secrets and supply chain

15. No secrets in code, git history, logs, URLs, client bundles or public env vars. A leaked secret is revoked first, cleaned up second. (`secrets-and-supply-chain.md` sections 2 to 4)
16. Tokens, keys and codes come from a CSPRNG. Secret comparisons are constant time. (`secrets-and-supply-chain.md` section 2)
17. Lockfile committed and installs frozen in CI; new dependencies vetted; install scripts restricted; CI actions pinned by SHA with least-privilege permissions and no untrusted input in `run:`. (`secrets-and-supply-chain.md` sections 6 to 10)

Integrity and failure

18. Webhooks are verified on the raw body with a constant time HMAC check and a timestamp window before any processing. (`../backend/webhooks-and-jobs.md` section 2)
19. The server computes prices, totals, roles and limits; it never trusts them from the client. Limited resources (balances, coupons, seats) are changed with conditional updates or row locks. (`owasp-checklist.md` section 8)
20. Errors fail closed: an exception in an auth, payment or validation path denies. Error responses never include stack traces, SQL, or internal hosts. (`owasp-checklist.md` section 12)
21. Security events are logged (auth success and failure, permission denied, admin actions, credential changes) without passwords, tokens or session IDs. (`../backend/backend.md` section 4)
22. TLS verification is never disabled outside a test harness. (`owasp-checklist.md` section 4)

## 2. Map: which file to read

| File | What is in it | Read when |
|---|---|---|
| `security/input-and-injection.md` | validation with Zod/serde, SQL injection by ORM, command injection, mass assignment, path traversal, SSRF rules and blocked ranges, file uploads, deserialization, prototype pollution, LLM output | any handler that takes input; any file, URL, query or process built from data |
| `security/browser-security.md` | XSS sinks per framework, sanitization, CSRF defenses by setup, CORS rules and code, security headers and CSP, open redirects | web frontends, cookie auth, APIs called from browsers, response headers |
| `security/secrets-and-supply-chain.md` | where secrets live, client bundle exposure, leak response, scanning, dependency vetting, lockfiles, pnpm/npm hardening, cargo-deny, GitHub Actions hardening, publishing | env vars, keys, adding or updating dependencies, CI and publish changes |
| `security/owasp-checklist.md` | OWASP Top 10 2025 as runnable checks, 2021 mapping, ASVS 5.0 levels, report format | security review or audit of a PR or a codebase |
| `backend/auth.md` | sessions, JWT, cookies, password hashing, login, reset, MFA, passkeys, OAuth, API keys, authorization, multi-tenancy, Supabase RLS | identity and permission work |
| `backend/webhooks-and-jobs.md` | webhook verification and dedupe, outgoing webhook SSRF | webhooks |
| `backend/rate-limits-retries-timeouts.md` | rate limit keys and numbers for auth routes, client IP handling | abuse-prone endpoints |

## 3. Security review of a diff in five minutes

For each changed handler, job, or component, answer in order; any "no" is a finding:

1. Who can reach this code? Is authentication enforced by middleware, not by the handler remembering?
2. Which object does it read or write, and is the query scoped to the caller's user or tenant from the session?
3. Is every input parsed by a strict schema with bounds before use?
4. Does any input reach a sink (SQL, shell, HTML, file path, URL fetch, redirect, header, log) without the safe API for that sink?
5. Does it trust any client value that the server should compute (price, role, owner, status)?
6. Does it add a secret, an env var, a dependency, or a CI step? Apply `secrets-and-supply-chain.md`.
7. What happens on error? Does it fail closed and leak nothing?
8. Could it be called 10,000 times a minute by one user? Is there a limit?

Then run the automated checks below on the changed files.

## 4. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Static analysis | no high findings | `semgrep --config p/owasp-top-ten --config p/secrets` on the diff (`--baseline-commit origin/main`) |
| Dependency audit | no high or critical production advisories | `npm audit --omit=dev --audit-level=high`, `pnpm audit --prod`, `cargo deny check advisories` |
| Secret scan | no findings | `gitleaks git -v --log-opts="origin/main..HEAD"` |
| Authorization tests | deny tests for new resources exist and pass | tests asserting another user's object returns 404 |
| RLS coverage (Supabase) | every public table has RLS and per-operation policies | SQL in `../backend/auth.md` section 14 |
| Workflow audit | no findings on changed workflows | `zizmor .github/workflows` |
| Dangerous sinks | no new unreviewed hits | grep patterns in `input-and-injection.md` section 11 and `browser-security.md` section 6 on changed files |
| TLS verification | no disabled verification | `rg -n "rejectUnauthorized: *false\|NODE_TLS_REJECT_UNAUTHORIZED\|danger_accept_invalid\|verify=False" ` |
| Fail closed | no allow in `catch` blocks of auth or payment code | `rg -n "catch" ` in those files and read |
