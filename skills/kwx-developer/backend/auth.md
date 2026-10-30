# Authentication and authorization

Read when: login, signup, sessions, tokens, passwords, password reset, MFA, passkeys, OAuth or social login, API keys, roles and permissions, multi-tenancy, Supabase RLS. The non-negotiable subset is repeated in `../security/security.md`.

Sources: OWASP cheat sheets (Authentication, Session Management, Password Storage, Authorization, JWT, CSRF), NIST SP 800-63B-4, RFC 9700 (OAuth 2.0 Security BCP), OAuth 2.1 draft 16, web.dev passkey guides, Supabase RLS docs and RLS performance guide, OWASP ASVS 5.0 chapters V6 to V10.

## Contents

1. Defaults in one table
2. Do not build what you can use
3. Sessions vs JWT
4. Cookies
5. Passwords: storage and rules
6. Login, enumeration, lockout
7. Reset, email change, re-authentication
8. MFA and passkeys
9. OAuth 2.1 and social login
10. API keys and service tokens
11. Authorization: check on the server, every time, per object
12. Multi-tenancy
13. Supabase and Postgres row level security
14. Checks

## 1. Defaults in one table

| Decision | Default |
|---|---|
| Auth provider | Use the framework's or platform's auth (Supabase Auth, Auth.js, Better Auth, Clerk, Lucia-style session code, `axum-login`/`tower-sessions`) before writing your own |
| Web app session | Opaque random server-side session in an `HttpOnly; Secure; SameSite=Lax` cookie with the `__Host-` prefix |
| Token in the browser | Never in `localStorage` or `sessionStorage` (OWASP: any XSS reads it) |
| Password hash | Argon2id, m=19456 KiB (19 MiB), t=2, p=1 minimum (OWASP) |
| Password policy | min 15 chars without MFA, min 8 with MFA, max at least 64, no composition rules, no forced rotation, blocklist breached passwords (NIST SP 800-63B-4) |
| MFA | Passkeys (WebAuthn) first, TOTP second, SMS only as a last resort |
| OAuth | Authorization code + PKCE (S256) for every client type; no implicit, no password grant (RFC 9700, OAuth 2.1) |
| Authorization | Deny by default, checked on the server on every request, scoped to the object and tenant |
| Session lifetime | Idle 15 to 30 min for low risk apps, 2 to 5 min for high value (OWASP); absolute 4 to 8 h for office apps; NIST AAL2: at most 24 h absolute, 1 h idle |

## 2. Do not build what you can use

Hand-written auth gets the details wrong: timing leaks, session fixation, token reuse, reset token storage. Use a maintained library or service, and spend the effort on authorization, which no library can do for you. If you must write session handling, follow sections 3 to 7 literally.

## 3. Sessions vs JWT

Default for a web app with its own backend: server-side sessions.

- Session ID: at least 128 bits from a CSPRNG (OWASP: minimum 64 bits of entropy; generate 128+, prefer 160+ when you make your own). 32 random bytes base64url encoded is the easy choice.
- Store a SHA-256 hash of the session token in the database, not the token itself, so a database leak does not leak live sessions (OWASP). Compare in constant time.
- Server-side revocation is a row delete: logout, "sign out everywhere", password change and account disable work instantly.

JWTs as session tokens trade that away: they cannot be revoked before `exp` without a denylist lookup on every request, which is a session store again. Use JWTs where their property (verification without a lookup) is worth it:

- Service-to-service calls and short-lived access tokens issued by an identity provider (Supabase, Auth0, Cognito, Clerk issue JWTs; that is fine, validate them properly).
- Access token lifetime 5 to 15 minutes, paired with a refresh token that is rotated on every use with reuse detection: if an old refresh token is presented, revoke the whole token family (RFC 9700 requires rotation or sender constraining for public clients).

JWT validation rules (OWASP JWT cheat sheet), every one of them:

- Pin the algorithm in your code (`algorithms: ["ES256"]` or `["RS256"]`). Never take it from the token header. Reject `alg: none`.
- Get the key from the trusted issuer's JWKS, chosen by the expected issuer, not from a `jku`/`x5u`/`jwk` header in the token.
- Validate `iss`, `aud` (your API's identifier), `exp`, and `nbf`. Require them to be present. Some libraries only check `aud` when you pass it.
- HMAC secrets (HS256) at least 256 random bits, never a password, never shared between issuers or audiences.
- Claims are readable by anyone (base64url, not encryption). No personal data, no secrets in claims.
- Authorization data in a JWT is stale until refresh: a removed team member still has the claim. For permission changes that must apply now, check the database (ASVS 8.3.2).
- Revocation when needed: denylist by `jti` until `exp` (OWASP REST).

## 4. Cookies

```
Set-Cookie: __Host-session=<token>; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=28800
```

- `Secure`: always. `HttpOnly`: always for session cookies.
- `SameSite=Lax` default (Strict breaks inbound links into logged-in pages; OWASP prefers Strict where usable). `SameSite=None` only with `Secure`, only for real cross-site embedding, and then CSRF tokens are mandatory.
- `__Host-` prefix: forces `Secure`, `Path=/`, no `Domain`, so a sibling subdomain cannot set or overwrite it (OWASP).
- No `Domain` attribute unless the cookie must be shared across subdomains (each subdomain is then part of your trust boundary).
- SameSite is defense in depth, not CSRF protection by itself. See `../security/browser-security.md`.

Session lifecycle:

- Regenerate the session ID on login and on every privilege change (role change, password change, MFA step up). Accepting a pre-login session ID after login is session fixation (OWASP).
- Logout deletes the server-side session. Clearing the cookie alone leaves a stolen copy valid (OWASP).
- Enforce idle and absolute timeouts on the server, never only on the client.
- On password change or reset: invalidate all other sessions and refresh tokens.
- Mobile apps: store tokens in the Keychain (iOS) or Keystore-backed storage (Android, `expo-secure-store`), never AsyncStorage or plain SharedPreferences.

## 5. Passwords: storage and rules

Hashing (OWASP Password Storage, exact parameters):

| Algorithm | When | Parameters |
|---|---|---|
| Argon2id | default | m=19456 KiB, t=2, p=1 (or m=47104 t=1, m=12288 t=3, m=9216 t=4, m=7168 t=5) |
| scrypt | no Argon2 available | N=2^17, r=8, p=1 |
| bcrypt | legacy only | cost at least 10 (raise to what the server allows); input limit 72 bytes, enforce it or pre-hash with HMAC + base64 as OWASP describes |
| PBKDF2 | FIPS required | HMAC-SHA256 600,000 iterations; HMAC-SHA512 220,000 |

```ts
import { hash, verify } from "@node-rs/argon2";
const phc = await hash(password, { memoryCost: 19456, timeCost: 2, parallelism: 1 }); // Argon2id is the default algorithm
const ok = await verify(phc, password);
```

```rust
use argon2::{Argon2, PasswordHasher, PasswordVerifier, password_hash::{SaltString, PasswordHash, rand_core::OsRng}};
// Argon2::default() is Argon2id with m=19456 KiB, t=2, p=1 (argon2 crate 0.5), matching OWASP's minimum
let phc = Argon2::default().hash_password(pw.as_bytes(), &SaltString::generate(&mut OsRng))?.to_string();
Argon2::default().verify_password(pw.as_bytes(), &PasswordHash::new(&phc)?)?;
```

- Store the PHC string (`$argon2id$v=19$m=19456,t=2,p=1$salt$hash`); it carries algorithm and parameters, so you can upgrade later: on successful login, if the stored parameters are weaker than current, rehash and save (OWASP).
- Never MD5, SHA-1, SHA-256 or any fast hash for passwords, salted or not. Never encrypt passwords (reversible).
- Hashing is CPU and memory heavy: rate limit login before hashing, and run hashing off the async event loop (the Node `argon2` libraries already do; in Rust use `spawn_blocking`).
- Optional pepper: an HMAC key kept outside the database (secret manager), applied before or after hashing. Defense in depth only (OWASP).

Rules (NIST SP 800-63B-4):

- Minimum 15 characters when the password is the only factor, 8 when it is part of MFA. Maximum at least 64. Count Unicode code points.
- Allow all characters including spaces and emoji. No composition rules ("one uppercase, one digit"). No forced periodic changes; force a change only on evidence of compromise.
- Check new passwords against a breached password list (Have I Been Pwned range API with k-anonymity: send only the first 5 hex chars of the SHA-1, compare suffixes locally). Tell the user why it was rejected.
- Allow paste and password managers (`autocomplete="current-password"` / `"new-password"`). Offer show password.
- Never silently truncate.

## 6. Login, enumeration, lockout

- Same response for unknown user, wrong password, and locked account: same message, same status code, and about the same time (OWASP). When the user does not exist, still verify against a dummy hash so the response takes as long.

```ts
const user = await db.user.findUnique({ where: { email } });
const ok = await verify(user?.passwordHash ?? DUMMY_ARGON2_HASH, password); // constant work either way
if (!user || !ok) return problem(401, "INVALID_CREDENTIALS", "Invalid email or password.");
```

- Signup and reset also must not reveal whether an email exists: "If an account exists for that address, we sent a link." For signup, send an email to the existing owner instead of an error on screen.
- Throttle per account and per IP (see `rate-limits-retries-timeouts.md`). Exponential delay after failures. Hard limit far below 100 consecutive failures per account (NIST cap). Lockout must not become a denial of service tool: allow password reset during lockout, and prefer delays over hard locks (OWASP).
- Log every authentication success and failure, lockout, reset and MFA change, without the password or token (OWASP Logging).

## 7. Reset, email change, re-authentication

Password reset tokens:

- 32 random bytes from a CSPRNG, sent by email as a link. Store only its SHA-256 hash, with the user ID and an expiry (default 30 minutes, at most a few hours).
- Single use: delete or mark used on success. Invalidate outstanding tokens when a new one is issued and when the password changes.
- After reset: invalidate all sessions and refresh tokens, notify the user by email, and do not log them in automatically if MFA is enabled (require the second factor).
- The reset link host comes from configuration, never from the request `Host` header (host header poisoning sends the token to the attacker's domain).
- Set `Referrer-Policy: no-referrer` on the reset page so the token does not leak to third party resources.

Re-authentication (OWASP): require the current password, a passkey, or MFA before changing password, email, MFA settings, payout details, or deleting the account. Security questions are not acceptable (ASVS 6.4.2).

Email change: confirm via a link sent to the new address, notify the old address, and keep the old email active until confirmed.

## 8. MFA and passkeys

Order of preference: passkeys (phishing resistant), TOTP authenticator apps, then email codes, then SMS (SIM swap and SMS pumping fraud).

Passkeys (WebAuthn), with a library (SimpleWebAuthn in TS, webauthn-rs in Rust):

- Fresh random challenge per ceremony, generated and stored server side, single use, expiring within minutes (web.dev).
- `rpID` is your registrable domain and must match exactly between registration and sign-in.
- `userVerification: "preferred"` and then check the UV flag in authenticator data if the passkey is the only factor; use `"required"` when policy needs it.
- `attestation: "none"` unless you have a regulated reason to verify device models.
- Store per credential: credential ID, public key, sign counter, transports, backup eligible/backed up flags, user handle, created and last used dates. Allow many passkeys per account.
- Conditional UI: `autocomplete="username webauthn"` on the username field and `navigator.credentials.get({ mediation: "conditional" })` on page load.
- Keep an account recovery path that is as strong as the login (another passkey, recovery codes stored hashed), or recovery becomes the weakest link.

TOTP: secret stored encrypted, accept the current step plus one step either side, reject reuse of a code within its window, rate limit attempts. Recovery codes: 8 to 10 single use codes, stored hashed.

## 9. OAuth 2.1 and social login

OAuth 2.1 is still an Internet-Draft (draft 16, September 2026) but consolidates RFC 9700, which is a published BCP. Rules:

- Authorization code flow with PKCE using `S256` for every client, public and confidential (RFC 9700: public clients MUST, servers MUST support).
- No implicit grant (`response_type=token`), no resource owner password grant (RFC 9700: MUST NOT).
- Exact string match on redirect URIs, no wildcards (localhost ports excepted for native apps).
- `state` bound to the user's browser session (or PKCE plus nonce in OIDC) to stop login CSRF.
- Tokens never in URLs or query strings; the code is single use.
- Refresh tokens for public clients: rotated on use or sender constrained (DPoP, mTLS).
- No open redirectors anywhere in the flow (`?next=` must be validated against an allowlist of relative paths).
- OIDC `id_token`: verify signature, `iss`, `aud` equal to your client ID, `exp`, and `nonce`.
- Account linking: link a social login to an existing account only when the provider asserts `email_verified: true`, and preferably after the user proves ownership of the existing account. Auto linking on an unverified email is account takeover.
- Identify users by the provider's `sub` (plus issuer), not by email. Emails change and get reassigned.

## 10. API keys and service tokens

- Generate 32 random bytes, show once, store only a hash (SHA-256 is fine for high entropy keys; no need for Argon2). Keep a prefix (`sk_live_ab12`) in clear for display and lookup.
- Prefix keys with a recognizable string (`sk_live_`, `myapp_pat_`) so secret scanners (GitHub push protection, gitleaks) can detect leaks.
- Scope keys to the minimum permissions and one tenant; support expiry and instant revocation; record `last_used_at`.
- Accept keys only in a header (`Authorization: Bearer ...`), never in the query string.
- API keys identify a client, they do not prove a user is present. Do not allow them on user-only operations (password change).

## 11. Authorization: check on the server, every time, per object

Broken access control has been number one in the OWASP Top 10 in both 2021 and 2025. The usual bug is not a missing login check; it is a logged-in user reading or changing another user's object by changing an ID (IDOR, BOLA).

Rules:

- Deny by default (OWASP). A route without an explicit policy is rejected. Put authentication in global middleware and require each route to declare its permission; a route that forgets is closed, not open.
- Check on every request, on the server (or in the database via RLS). Hiding a button is UX, not security (ASVS 8.3.1).
- Check the object, not just the type: "can edit invoices" is not "can edit invoice 123". Scope every query by the owner or tenant derived from the session, never from the request body.

```ts
// bad: any logged-in user can read any invoice by ID
const inv = await db.invoice.findUnique({ where: { id: req.params.id } });

// good: the tenant comes from the session; not found and not yours look the same
const inv = await db.invoice.findFirst({ where: { id: req.params.id, orgId: req.session.orgId } });
if (!inv) return problem(404, "NOT_FOUND");
```

```rust
// good: ownership in the WHERE clause, not an if after the fetch
let inv = sqlx::query_as!(Invoice, "SELECT * FROM invoices WHERE id = $1 AND org_id = $2", id, session.org_id)
    .fetch_optional(&pool).await?.ok_or(ApiError::NotFound)?;
```

- Writes too: `UPDATE ... WHERE id = $1 AND org_id = $2`, and check the row count. Check that IDs inside the body (`project_id` on a new task) also belong to the caller's tenant.
- Field level: a user may update their `display_name` but not `role`, `plan`, `org_id`, `email_verified`, `credits` (mass assignment, BOPLA in ASVS 8.2.3). Use an input schema with only the editable fields.
- Function level: admin endpoints check the admin role on the server, on every admin route, not only in the admin UI router.
- Fail closed: an exception during the authorization check denies (OWASP Top 10 2025 A10). Never `catch { return true }`.
- Permission changes apply immediately (ASVS 8.3.2): read roles from the database or a short lived cache that is invalidated on change, not only from a JWT issued yesterday.
- Act with the end user's permissions, not the service's (ASVS 8.3.3): a backend calling another service on behalf of a user passes the user's identity, and the callee checks it.
- Unguessable IDs (UUIDs) reduce enumeration but are not authorization (OWASP).
- Prefer attribute or relationship checks (owner, member of org, role in project) over a flat global role list (OWASP prefers ABAC/ReBAC). Centralize them in one module of policy functions (`canEditInvoice(user, invoice)`) and call it everywhere; scattered inline checks drift.
- Write tests for the deny cases: user A cannot read, update or delete user B's object, for every resource. These tests catch most IDOR bugs.

## 12. Multi-tenancy

- Every tenant-owned table has a non-null `org_id` (or `tenant_id`) column, indexed, part of composite unique keys (`UNIQUE (org_id, slug)`).
- The tenant ID comes from the session or token, never from a header or body the client controls.
- Enforce isolation in one place that cannot be forgotten: Postgres RLS with the tenant in a session variable or JWT claim, or a repository layer that requires the tenant in every query signature. Ad hoc `where: { orgId }` in each handler is where leaks come from.
- Background jobs, exports, search indexes, caches, file storage paths and analytics all carry the tenant too. Cross-tenant leaks often happen outside the main request path.

## 13. Supabase and Postgres row level security

When the client talks to the database directly (Supabase, PostgREST, Firebase-like setups), RLS is the authorization layer. Every rule here is from the Supabase docs.

- Enable RLS on every table in an exposed schema (`public`). A table without RLS is readable and writable by anyone with the anon key, which is public by design.
- Write one policy per operation (`select`, `insert`, `update`, `delete`). `USING` filters which existing rows are visible or changeable; `WITH CHECK` validates the new row, which stops a user inserting or moving rows into another user's ownership. Update needs both, plus a select policy.
- Always add `TO authenticated` (or `TO anon`) so the policy does not run for other roles.
- `auth.uid()` is null for anonymous requests. `null = user_id` is never true, so the policy happens to deny, but write the intent out so a later edit (an `OR`) cannot open it: `auth.uid() IS NOT NULL AND auth.uid() = user_id`.
- Wrap function calls in a subselect so they run once per statement, not once per row: `(select auth.uid()) = user_id`. Measured in the Supabase RLS performance guide: 179 ms to 9 ms for `auth.uid()`, 178,000 ms to 12 ms for a `has_role()` function.
- Index every column used in a policy (171 ms to under 0.1 ms in the same guide).
- Also filter in the query (`.eq('user_id', userId)`), it lets the planner use the index (171 ms to 9 ms).
- For "member of team" policies compare against a set, `team_id IN (select team_id from team_members where user_id = (select auth.uid()))`, instead of joining per row (9,000 ms to 20 ms).
- Never authorize on `raw_user_meta_data` / `user_metadata`: the user can edit it. Use `raw_app_meta_data` / `app_metadata`, which only the server can set, or a table.
- The `service_role` (secret) key bypasses RLS. It lives only on the server and never in client code, `NEXT_PUBLIC_*`, `EXPO_PUBLIC_*`, or a mobile bundle.
- Views bypass RLS by default: create them `WITH (security_invoker = true)` on Postgres 15+.
- `security definer` functions run as their owner: set `search_path = ''`, schema-qualify everything, and do not put them in an exposed schema.
- Server code (Next.js middleware, route handlers): authorize with `supabase.auth.getUser()` or `getClaims()`, which validate the token, not `getSession()`, which reads the cookie without revalidating it.
- Test policies: pgTAP per table (`supabase test db`), covering allow and deny for each operation and role. A denied update returns zero rows, not an error; assert that the row is unchanged.

```sql
alter table public.notes enable row level security;

create policy "notes: owner reads" on public.notes for select to authenticated
  using ((select auth.uid()) = user_id);
create policy "notes: owner inserts" on public.notes for insert to authenticated
  with check ((select auth.uid()) = user_id);
create policy "notes: owner updates" on public.notes for update to authenticated
  using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "notes: owner deletes" on public.notes for delete to authenticated
  using ((select auth.uid()) = user_id);

create index on public.notes (user_id);
```

## 14. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Strong password hash | Argon2id (or scrypt/bcrypt cost >= 10 legacy) with OWASP parameters | `rg -n "argon2\|bcrypt\|scrypt\|pbkdf2\|createHash\(.(md5\|sha1\|sha256)" -i` |
| No tokens in web storage | no auth token in `localStorage`/`sessionStorage`/AsyncStorage | `rg -n "(localStorage\|sessionStorage\|AsyncStorage)\.setItem\(.*(token\|jwt\|session)" -i` |
| Cookie flags | session cookie has `HttpOnly`, `Secure`, `SameSite`, ideally `__Host-` | `curl -si -X POST .../login ... \| grep -i set-cookie` |
| Session regenerated on login | login handler creates a new session ID | read login handler (`regenerate`, new token issued, old deleted) |
| Logout server side | logout deletes the session row or revokes the token | read logout handler |
| JWT validation pinned | `algorithms` list passed, `audience` and `issuer` passed | `rg -n "jwt\.verify\|jwtVerify\|decode::<\|Validation::new" ` and read args; `rg -n "jwt\.decode\(" ` (decode without verify) |
| Generic login failure | same message and status for unknown user and wrong password; dummy hash on unknown user | read login handler |
| Reset tokens hashed, single use, expiring | token stored as hash with `expires_at`, deleted on use | read reset flow and migration |
| Reset link host from config | no `req.headers.host`/`req.hostname` in email links | `rg -n "headers\.host\|req\.hostname\|Host\b" ` near mail code |
| Object level authorization | every query by ID also filters by owner/tenant from the session | `rg -n "findUnique\(\{ where: \{ id" `, `rg -n "WHERE id = \$1\"" ` and check for tenant predicate |
| Deny tests exist | tests assert user A gets 404/403 on user B's resources | `rg -n "another user\|other user\|forbidden\|404" tests/` |
| Authz fails closed | no `catch` that returns allow | `rg -n "catch.*\{[^}]*return true" -U` |
| RLS on every exposed table | `relrowsecurity` true for all `public` tables | `select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where nspname='public' and relkind='r' and not relrowsecurity;` returns nothing |
| Policies wrap auth.uid | no bare `auth.uid()` in policies | `select polname, pg_get_expr(polqual, polrelid) from pg_policy;` and look for `auth.uid()` not inside `select` |
| No service role in client | `service_role`/secret key absent from client bundles and public env vars | `rg -n "service_role\|SUPABASE_SERVICE\|sb_secret_" ` in client dirs; `rg -n "NEXT_PUBLIC_.*SERVICE\|EXPO_PUBLIC_.*SERVICE"` |
| No user_metadata in authz | policies and server checks do not read `user_metadata` | `rg -n "user_metadata\|raw_user_meta_data" ` |
| OAuth flow safe | PKCE S256, exact redirect URIs, state/nonce checked, linking only on verified email | read auth config; `rg -n "response_type=token\|grant_type=password\|email_verified" ` |
