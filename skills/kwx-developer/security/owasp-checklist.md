# OWASP checklist: Top 10 2025 as checks an agent can run

Read when: reviewing a codebase or a PR for security, before shipping a feature that touches auth, input, files or money, or when asked for a security audit. Each item is a check you can run by reading code or running a command. Fix guidance lives in the topic files; this file finds the problems.

Sources: OWASP Top 10 2025 (top10.owasp.org/2025), OWASP Top 10 2021, OWASP ASVS 5.0.0 (May 2025), OWASP Cheat Sheet Series.

## Contents

1. How to run an audit
2. The 2025 list and what changed from 2021
3. A01 Broken Access Control (includes SSRF)
4. A02 Security Misconfiguration
5. A03 Software Supply Chain Failures
6. A04 Cryptographic Failures
7. A05 Injection
8. A06 Insecure Design
9. A07 Authentication Failures
10. A08 Software or Data Integrity Failures
11. A09 Security Logging and Alerting Failures
12. A10 Mishandling of Exceptional Conditions
13. ASVS levels: how deep to go
14. Report format

## 1. How to run an audit

1. Map the attack surface first: list every route (`rg -n "app\.(get|post|put|patch|delete)\(|router\.|export (async )?function (GET|POST|PUT|PATCH|DELETE)|#\[(get|post|put|patch|delete)\(|\.route\(" `), every webhook, every job consumer, every place that fetches a URL, reads a file, or runs a process, and every table exposed to clients (Supabase).
2. For each route note: who can call it, which object it touches, how that object is scoped.
3. Run the automated tools that exist for the stack (they are cheap and catch the obvious):
   - `semgrep --config p/owasp-top-ten --config p/secrets` (plus `p/typescript`, `p/react`, `p/nextjs`, `p/rust` as relevant)
   - `npm audit --omit=dev --audit-level=high` / `pnpm audit --prod`, `cargo deny check`
   - `gitleaks git -v`
   - `zizmor .github/workflows` for CI
   - Supabase: the dashboard Security Advisor, or the `splinter` lints SQL
4. Then the manual checks below, in order. A01 first: it is the most common and the least found by tools.
5. Report findings with the format in section 14.

## 2. The 2025 list and what changed from 2021

| 2025 | 2021 equivalent |
|---|---|
| A01 Broken Access Control | A01, plus A10:2021 SSRF folded in |
| A02 Security Misconfiguration | A05:2021, moved up |
| A03 Software Supply Chain Failures | expands A06:2021 Vulnerable and Outdated Components to build systems and distribution |
| A04 Cryptographic Failures | A02:2021 |
| A05 Injection (includes XSS) | A03:2021 |
| A06 Insecure Design | A04:2021 |
| A07 Authentication Failures | A07:2021 Identification and Authentication Failures |
| A08 Software or Data Integrity Failures | A08:2021 |
| A09 Security Logging and Alerting Failures | A09:2021, renamed to stress alerting |
| A10 Mishandling of Exceptional Conditions | new: error handling, logic errors, failing open |

## 3. A01 Broken Access Control (includes SSRF)

| Check | Fail looks like | How |
|---|---|---|
| Object level authz (IDOR/BOLA) | fetch or update by ID with no owner/tenant predicate | `rg -n "findUnique\(\{\s*where:\s*\{\s*id" `, `rg -n "findById\(\|get\(.*params\.id\|WHERE id = \\$1\"" `; read each and look for the session's user or org in the query |
| Tenant from client | `orgId`/`tenantId`/`userId` read from body, query or header | `rg -n "(body\|query\|params\|headers)\.(org\|tenant\|user\|owner)_?[iI]d" ` |
| Field level (mass assignment) | request body spread into an update | `rg -n "data: req\.body\|\.\.\.req\.body\|Object\.assign\([^,]+, *req\.body" ` |
| Function level | admin routes without a server-side role check | list routes under `/admin`, `/internal`; confirm middleware |
| Default deny | routes without auth middleware that are not deliberately public | compare route list to auth middleware coverage |
| Client side only checks | permission checks only in components (`{isAdmin && <Button/>}`) with no server check | for each such UI action, find its API route and read it |
| Supabase RLS | public tables without RLS, `using (true)` policies on private data, `user_metadata` in policies, missing `with check` | `select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where nspname='public' and relkind='r' and not relrowsecurity;` and `select * from pg_policies;` |
| Service key in client | `service_role`/secret key reachable from client code | `rg -n "service_role\|SERVICE_ROLE\|sb_secret_" ` outside server-only dirs |
| Storage access | public buckets holding private files; signed URLs with long expiry | read storage config; `rg -n "public: true\|getPublicUrl\|createSignedUrl\(.*[0-9]{5,}" ` |
| CORS | reflected origin with credentials, regex/endsWith matching | `rg -n "origin: true\|cors\(\)\|endsWith\(.*origin\|allow_origin\(Any\)" ` |
| CSRF | cookie auth, unsafe methods, no token or origin check | see `browser-security.md` |
| SSRF | server fetches a URL from input without the guarded client | `rg -n "fetch\(\|axios\.(get\|post)\(\|reqwest::get\(\|\.get\(&?url" ` and trace the URL's origin |
| Open redirect | `redirect(req.query.next)` | `rg -n "redirect\((req\.query\|searchParams\.get\|params)" ` |
| Path traversal | file paths from input | `rg -n "(readFile\|createReadStream\|sendFile\|File::open\|fs::read)\(.*(req\|params\|query)" ` |

## 4. A02 Security Misconfiguration

| Check | Fail looks like | How |
|---|---|---|
| Debug in production | debug flags, verbose errors, stack traces returned | `rg -n "debug: true\|DEBUG=1\|showStack\|stack: err\.stack\|RUST_BACKTRACE=1" `; curl a failing route |
| Default credentials | default passwords, sample users, `admin/admin` seeds in prod | `rg -n "password.*(admin\|changeme\|password123)" -i` |
| Security headers missing | no HSTS, CSP, nosniff, frame-ancestors | `curl -sI https://host/` |
| Permissive CORS | `*` on authenticated APIs | see A01 |
| Exposed admin or dev endpoints | `/graphql` introspection, `/swagger`, `/debug`, `/metrics`, `/.env`, `/.git/` public | curl each path on the deployed host |
| Cloud storage public | S3/GCS/Supabase bucket public by default | read IaC (`rg -n "acl.*public-read\|public = true" `) |
| Cookies | missing `Secure`/`HttpOnly`/`SameSite` | check `Set-Cookie` |
| TLS verification disabled | `rejectUnauthorized: false`, `NODE_TLS_REJECT_UNAUTHORIZED=0`, `danger_accept_invalid_certs(true)`, `verify=False` | `rg -n "rejectUnauthorized: *false\|NODE_TLS_REJECT_UNAUTHORIZED\|danger_accept_invalid\|verify=False\|InsecureSkipVerify" ` |
| XML external entities | XML parser with DTD/entities enabled | read parser config |
| Unneeded features | unused routes, sample apps, directory listing | review route list |

## 5. A03 Software Supply Chain Failures

Run the checks table in `secrets-and-supply-chain.md` section 12. Minimum: lockfile committed, frozen installs in CI, audit clean for production dependencies, install scripts controlled, release age gate, actions pinned by SHA, workflow `permissions:` declared, no script injection in workflows, CDN scripts with SRI.

## 6. A04 Cryptographic Failures

| Check | Fail looks like | How |
|---|---|---|
| Password hashing | fast hash or encryption for passwords | `rg -n "createHash\(['\"](md5\|sha1\|sha256)['\"]\).*pass\|md5\(\|sha1\(" -i`; expect argon2id/scrypt/bcrypt |
| Weak randomness for secrets | `Math.random()`, `rand::thread_rng` is fine but `rand` seeded with time is not, `uuid v1` as token | `rg -n "Math\.random\(\)" ` near token/code/secret/password/otp/id |
| Homemade crypto | custom encryption, ECB mode, static IV, `createCipher(` (deprecated, no IV) | `rg -n "createCipher\(\|aes-.*-ecb\|iv *= *['\"]\|Iv::from_slice\(b\"" ` |
| Plain HTTP | `http://` to APIs or in redirects; missing HSTS | `rg -n "http://(?!localhost\|127\.0\.0\.1)" -P` |
| Secrets in code | keys, tokens, private keys in repo | `gitleaks git -v` |
| Sensitive data at rest | tokens, reset codes, API keys stored in plain text in the DB | read migrations: token columns should be hashes |
| Sensitive data in transit to logs/analytics | PII or tokens sent to logging, Sentry, analytics | read logger redaction and Sentry `beforeSend` |
| JWT | `alg` not pinned, `decode` used instead of `verify`, weak HS256 secret | `rg -n "jwt\.decode\(\|algorithms\|HS256" ` |
| Comparison of secrets | `===` on HMACs, tokens, API keys | `rg -n "(signature\|hmac\|token\|apiKey\|digest) *===" ` ; expect `timingSafeEqual`/constant time |

## 7. A05 Injection

Run the checks table in `input-and-injection.md` section 11 (SQL, shell, eval, schemas, deserialization, prototype pollution) and in `browser-security.md` section 6 (XSS sinks, Markdown, URLs). Also:

- Log injection: user values in log messages without structured logging (`logger.info("login " + username)`). Use structured fields.
- Header injection: user values in response headers or `Content-Disposition` without encoding.
- LLM prompt injection reaching tools: model output used as SQL, shell, URLs or HTML (see `input-and-injection.md` section 10).

## 8. A06 Insecure Design

Design flaws are found by asking questions, not by grepping. For each feature ask:

- Can it be automated at scale for profit? (signup bonuses, referral credits, free trial abuse, coupon stacking, SMS/email sending) Needs per account and per device limits.
- Does the server trust a value it should compute? Prices, totals, discounts, quantities, roles, plan, currency sent from the client. Recompute on the server from IDs.
- Are multi-step flows enforced in order on the server? (checkout: pay before ship; reset: verify token before change; onboarding steps). Can a step be skipped by calling the last endpoint directly?
- Race conditions on limited resources: double spending a balance, redeeming a coupon twice, booking the last seat twice. Needs a transaction with a row lock (`SELECT ... FOR UPDATE`), a conditional update (`UPDATE ... SET balance = balance - $1 WHERE id = $2 AND balance >= $1`), or a unique constraint.
- Are limits defined for everything users can create? (items, file storage, API calls, members, projects) Unlimited is a DoS and a cost vector.
- Is there a threat model for the feature? For anything involving money, identity or other users' data, write down who the attacker is and what they want before coding.

## 9. A07 Authentication Failures

| Check | Fail looks like | How |
|---|---|---|
| Rate limits on auth | login, reset, OTP, signup without limits | read route middleware |
| Enumeration | different messages, status codes or timing for unknown user vs wrong password; "email already registered" on signup | read handlers; time both cases with curl |
| Password policy | composition rules, max length under 64, min under 8 (15 without MFA), no breach check | read validation |
| Session handling | no regeneration on login, no server-side logout, tokens in localStorage, long-lived JWT without revocation | see `../backend/auth.md` checks |
| Reset flow | token not hashed, not single use, long expiry, link host from request | read reset code |
| MFA | missing for admin accounts; MFA bypass via alternate login path (API key, OAuth, "remember me") | list all login paths |
| OAuth | implicit flow, no PKCE, no state/nonce, wildcard redirect URIs, account linking on unverified email | read OAuth config |
| Credential stuffing defense | no per account throttling, no breached password check | read login and signup |

## 10. A08 Software or Data Integrity Failures

| Check | Fail looks like | How |
|---|---|---|
| Unsigned webhooks | webhook handlers without signature verification | see `../backend/webhooks-and-jobs.md` checks |
| Unsafe deserialization | pickle, YAML full load, PHP unserialize, `node-serialize` on input | `rg -n "pickle\.loads\|yaml\.load\(\|unserialize\(\|node-serialize" ` |
| Client trusted for integrity | prices or totals from the client; signed data not verified | read checkout and order code |
| Updates without verification | auto-update downloads without signature or checksum check; `curl \| sh` | `rg -n "curl .*\| *(sh\|bash)" ` |
| CDN scripts without SRI | `<script src="https://...">` without `integrity` | `rg -n "<script[^>]+src=\"https?://" ` |
| CI artifact trust | `workflow_run` or `pull_request_target` using PR artifacts | `rg -n "workflow_run\|pull_request_target" .github/workflows` |

## 11. A09 Security Logging and Alerting Failures

| Check | Fail looks like | How |
|---|---|---|
| Security events logged | no log on login failure, lockout, permission denied, password change, admin action | `rg -n "logger\.\|log::\|tracing::" ` in auth and admin code |
| Who, what, when, where | log lines without user/tenant ID, request ID, timestamp, route | read logger setup |
| No sensitive data | passwords, tokens, cookies, full request bodies logged | `rg -n "(log\|logger\|console)\.\w+\(.*(password\|token\|authorization\|cookie\|req\.body\|headers)" -i` |
| Injection safe | string-concatenated log lines with user input | structured logging fields instead |
| Alerting | nobody is alerted on spikes of auth failures, 5xx, DLQ messages, rate limit hits | check alert config exists |
| Retention | logs kept for an agreed period and protected from edit | check platform settings |

## 12. A10 Mishandling of Exceptional Conditions

| Check | Fail looks like | How |
|---|---|---|
| Fail open | `catch` that grants access, returns success, or skips a check | `rg -n "catch[^{]*\{\s*(return (true\|next\(\))\|\})" -U`; read auth and payment `catch` blocks |
| Swallowed errors | empty `catch {}`, `.catch(() => {})`, `let _ = result;`, `.ok();` discarding errors on writes | `rg -n "catch *(\([^)]*\))? *\{\s*\}\|\.catch\(\(\) => \{\s*\}\)\|let _ = .*\.(await\|send\|execute)\|\.ok\(\);" -U` |
| Panics on input (Rust) | `unwrap()`/`expect()` on parse results, request data, I/O in handlers | `rg -n "\.unwrap\(\)\|\.expect\(" src/` and read hits in request paths |
| Unhandled async errors (Node) | no handler for `unhandledRejection`; Express 4 async handlers without a wrapper | `rg -n "unhandledRejection" `; check Express version |
| Error leaks | stack traces, SQL errors, internal paths returned to clients | curl failing routes |
| Partial failure leaves bad state | multi-step writes outside a transaction; side effects before commit | read write paths for `$transaction`/`BEGIN` |
| Resource cleanup | locks, files, connections not released on error paths | `try/finally`, RAII, `using` |
| Unexpected values | `switch` without default for external enums; `as` casts on external data | `rg -n "as unknown as\|as any" ` on external data |
| Timeouts and limits | missing timeouts turn slow failures into outages | see `../backend/rate-limits-retries-timeouts.md` checks |

## 13. ASVS levels: how deep to go

OWASP ASVS 5.0.0 (May 2025) has about 350 requirements in 17 chapters (V1 Encoding and Sanitization, V2 Validation and Business Logic, V3 Web Frontend Security, V4 API and Web Service, V5 File Handling, V6 Authentication, V7 Session Management, V8 Authorization, V9 Self-contained Tokens, V10 OAuth and OIDC, V11 Cryptography, V12 Secure Communication, V13 Configuration, V14 Data Protection, V15 Secure Coding and Architecture, V16 Security Logging and Error Handling, V17 WebRTC).

- Level 1: about 20% of requirements, first layer defenses against common attacks that need no other vulnerability. Every app, including side projects and MVPs.
- Level 2: about 70% cumulative. "Most applications should be striving to achieve this level." Any app with user accounts, personal data, or payments.
- Level 3: all requirements, defense in depth for high assurance (banking, health, critical infrastructure).

Default for this skill: write code to ASVS Level 2 for apps with accounts, Level 1 for internal tools and prototypes without personal data. When a requirement is relevant, cite it by ID (for example `8.2.2` object level authorization) so the finding is traceable. The full text: github.com/OWASP/ASVS, folder `5.0/en`.

## 14. Report format

One finding per entry, ranked by severity (exploitability times impact):

```
[HIGH] A01 IDOR on GET /api/invoices/:id
Where: src/routes/invoices.ts:42
What: query filters by id only; any logged-in user can read any invoice by changing the id.
Proof: as user A, GET /api/invoices/<id of user B's invoice> returns 200 with B's data.
Fix: scope by session org: findFirst({ where: { id, orgId: session.orgId } }); add a deny test.
Ref: ASVS 8.2.2
```

Severity guide: Critical (unauthenticated access to data or code execution, leaked production secret), High (authenticated user reaches other users' data or escalates role, SSRF to metadata), Medium (missing rate limits on auth, CSRF on a state change, stored XSS behind login), Low (missing headers, verbose errors without secrets). Do not pad the report with low items to look thorough; say what was not checked.

## 15. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Every category was looked at | The report lists A01 to A10, each with findings or "none found" | Read the report headings |
| Each finding has proof | Every finding names a file and line and a request or input that triggers it | Read each finding |
| Level chosen | The report states the ASVS level used and why | Search the report for "ASVS" |
