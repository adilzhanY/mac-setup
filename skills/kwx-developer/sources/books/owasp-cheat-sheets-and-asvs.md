# OWASP Cheat Sheet Series, OWASP Top 10 2025, OWASP ASVS 5.0

Legal free sources by OWASP (CC BY-SA 4.0):
- Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- Top 10 2025: https://top10.owasp.org/2025/ (introduction: https://top10.owasp.org/2025/0x00_2025-Introduction/)
- ASVS 5.0.0 (30 May 2025): https://github.com/OWASP/ASVS/tree/master/5.0/en , site https://asvs.owasp.org/

## What I read

Cheat sheets, read through for their rules: Authentication, Session Management, Password Storage, Authorization, Input Validation, SQL Injection Prevention, Cross Site Scripting Prevention, Cross-Site Request Forgery Prevention, Server Side Request Forgery Prevention, File Upload, Secrets Management, Logging, JSON Web Token, REST Security, Mass Assignment, Denial of Service.
Top 10 2025: the list and the introduction (what changed from 2021).
ASVS 5.0: "What is the ASVS" (levels), chapter list, V4 API and Web Service, V5 File Handling, V8 Authorization requirement tables.

## Key lessons used in security/ and backend/

- Password storage: Argon2id m=19456 KiB t=2 p=1 minimum (or the equivalent m/t pairs); scrypt N=2^17 r=8 p=1; bcrypt cost 10+ with a 72 byte limit; PBKDF2-SHA256 600,000 iterations. Store algorithm and parameters with the hash and rehash on login.
- Authentication: generic messages and equal timing for unknown user vs wrong password, also for reset and signup; throttle per account; MFA is the best defense; re-authenticate before sensitive changes; no security questions.
- Sessions: 64 bits of entropy minimum (128+ when self generated), `__Host-` cookies with Secure, HttpOnly, SameSite; idle timeout 2 to 5 min for high value, 15 to 30 min for low risk; regenerate on privilege change; server-side invalidation on logout; never tokens in localStorage.
- Authorization: deny by default, validate on every request, object level checks (IDOR), unguessable IDs are not a control, prefer ABAC/ReBAC, fail closed, test the deny cases.
- Input validation is separate from parameterization and output encoding; reject unknown JSON properties explicitly; anchor regexes and bound input length (ReDoS); validate data from internal systems when it crosses a trust boundary.
- SQL injection: parameterize even validated values; identifiers from fixed mappings; stored procedures and ORMs are not automatically safe; least privilege DB accounts.
- XSS: framework escape hatches are where XSS lives; safe sinks (`textContent`); DOMPurify for HTML; CSP and Trusted Types as defense in depth; WAFs and input filters do not fix XSS.
- CSRF: Fetch Metadata `Sec-Fetch-Site` as primary signal, Origin fallback, signed session bound double submit cookie, naive double submit is insecure, SameSite is defense in depth, login CSRF, XSS defeats all CSRF defenses.
- SSRF: allowlists, block private and metadata ranges, resolve then connect to the validated IP (DNS rebinding), disable redirects, only http(s), beware parser differentials.
- File upload: extension allowlist plus content checks, generated names, size limits including decompressed size, store off the web root or on another domain, re-encode images.
- Secrets: centralize, least privilege, rotate, dynamic secrets, env vars not recommended when better options exist, scan before commit, on leak revoke first.
- Logging: when, where, who, what; log auth and authorization failures; never log session IDs, tokens, passwords, keys, connection strings; encode CR/LF and prefer structured logs.
- JWT: reject `alg: none`, pin algorithms, key chosen by expected issuer, HMAC secret 160+ bits (256 for HS256), claims are readable, validate iss/aud/exp, denylist by jti.
- Top 10 2025: A01 Broken Access Control (SSRF folded in), A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions (new: fail open, error handling).
- ASVS 5.0 levels: L1 about 20% of ~350 requirements (first layer), L2 about 70% cumulative ("most applications should be striving to achieve this level"), L3 all (defense in depth). 17 chapters, new standalone V9 Self-contained Tokens, V10 OAuth and OIDC, V17 WebRTC.
