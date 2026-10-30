# Browser facing security: XSS, CSRF, CORS, headers, redirects

Read when: building a web frontend, an API called from browsers, cookie auth, rendering user content, setting response headers, or redirecting.

Sources: OWASP cheat sheets (Cross Site Scripting Prevention, CSRF Prevention, REST Security, Session Management, Unvalidated Redirects), MDN CORS guide, OWASP ASVS 5.0 V3.

## Contents

1. XSS: the framework protects you until you opt out
2. CSRF: which defense for which setup
3. CORS: what it is and is not
4. Security headers: a default set
5. Open redirects
6. Checks

## 1. XSS: the framework protects you until you opt out

React, Vue, Svelte, Angular and server templates with auto escaping encode text by default. XSS appears at the escape hatches (OWASP XSS cheat sheet):

| Stack | Escape hatch |
|---|---|
| React | `dangerouslySetInnerHTML`, `href={userUrl}` with `javascript:` (React 19 blocks it in `href`/`src`, older versions do not), refs + `innerHTML` |
| Vue | `v-html` |
| Svelte | `{@html ...}` |
| Angular | `bypassSecurityTrustHtml/Url/...` |
| DOM | `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, `setTimeout(string)`, `new Function` |
| Templates | `{{{ }}}` (Handlebars), `| safe` (Jinja, Nunjucks), `<%- %>` (EJS), `Markup()`, Askama `|safe` |
| Markdown | renderers with raw HTML enabled (`marked` default allows HTML; `markdown-it` `html: true`) |

Rules:

- Render user content as text. Use `textContent`, not `innerHTML`.
- When user HTML is the feature (rich text, Markdown with HTML), sanitize with DOMPurify (or `sanitize-html` on the server, `ammonia` in Rust) at render time, configured with the smallest tag and attribute allowlist that works. Do not modify the HTML after sanitizing (OWASP). Keep the sanitizer updated; bypasses are found regularly.
- URLs from users: parse with `new URL()` and allow only `http:` and `https:` (and `mailto:` if needed) before putting them in `href` or `src`.
- Never build HTML strings with template literals from data: `el.innerHTML = \`<b>${name}</b>\``.
- JSON embedded in a server-rendered page: serialize with an encoder that escapes `<` (`serialize-javascript`, or `JSON.stringify(data).replace(/</g, "\\u003c")`), otherwise `</script>` in a value breaks out.
- Do not put user data into `<script>` blocks, inline event handlers (`onclick="..."`), `style` attributes, or CSS (OWASP dangerous contexts).
- CSP is defense in depth, not the fix (section 4). Trusted Types (`require-trusted-types-for 'script'`) make DOM sinks reject plain strings in Chromium browsers; worth enabling on apps with a lot of DOM code.

## 2. CSRF: which defense for which setup

CSRF is possible when the browser attaches credentials automatically: cookies (and HTTP auth, client certs). APIs authenticated only by an `Authorization: Bearer` header set by JS are not CSRF-prone (the attacker's page cannot set that header cross-origin) but then the token lives where XSS can reach it.

| Setup | Defense |
|---|---|
| Framework with built-in CSRF (Rails, Django, Laravel, SvelteKit form actions, Next.js Server Actions origin check) | Use it. Do not disable it globally to make a webhook work; exempt only the webhook route |
| Cookie session + JSON API from your own SPA | `SameSite=Lax` (or Strict) cookie, plus a check of `Sec-Fetch-Site` and/or `Origin` on unsafe methods, plus require `Content-Type: application/json` or a custom header (forces a CORS preflight) |
| Cookie session + HTML forms | Synchronizer token (per session, in a hidden field, compared server side) or signed double submit cookie bound to the session with HMAC |
| Bearer tokens in headers only | No CSRF token needed; spend the effort on XSS |

Rules (OWASP CSRF cheat sheet):

- Never change state on GET. `SameSite=Lax` still sends cookies on top-level GET navigations.
- Fetch Metadata check, the cheap primary signal: reject unsafe methods (POST, PUT, PATCH, DELETE) when `Sec-Fetch-Site` is `cross-site`. Fall back to `Origin` (then `Referer`) when the header is absent. Compare the full origin exactly, not a prefix (`https://example.com.attacker.net` must fail). Do not allowlist `Origin: null`.

```ts
const SAFE = new Set(["GET", "HEAD", "OPTIONS"]);
app.use((req, res, next) => {
  if (SAFE.has(req.method)) return next();
  const site = req.get("sec-fetch-site");
  if (site && site !== "same-origin" && site !== "none") return res.status(403).end();
  if (!site) {
    const origin = req.get("origin");
    if (!origin || origin !== process.env.APP_ORIGIN) return res.status(403).end();
  }
  next();
});
```

- Naive double submit (cookie value equals form value, unsigned) is insecure: a sibling subdomain can write the cookie (OWASP). Use the signed, session-bound variant.
- Login forms need CSRF protection too (login CSRF logs the victim into the attacker's account).
- XSS defeats every CSRF defense. CSRF tokens do not help if script runs on your origin.
- CAPTCHA is not a CSRF defense (OWASP).

## 3. CORS: what it is and is not

CORS lets a server allow pages from other origins to read its responses in a browser. It is not access control: the request still reaches your server, and curl or a server-side attacker ignores CORS entirely (MDN).

Rules:

- If no other origin needs to call the API from a browser, send no CORS headers at all (OWASP REST). Same-origin apps (Next.js app calling its own `/api`) need none.
- Allowlist exact origins. Reflecting the request `Origin` back unconditionally, or matching with a regex like `/example\.com/` (matches `example.com.evil.net`) or "ends with `example.com`" (matches `evilexample.com`), is the classic misconfiguration.
- Never `Access-Control-Allow-Origin: *` together with credentials (browsers refuse it, so developers "fix" it by reflecting the origin, which is worse).
- With credentials: explicit origin, `Access-Control-Allow-Credentials: true`, explicit method and header lists (no `*`).
- `Vary: Origin` whenever the response depends on the origin, including when the origin is rejected, so caches do not mix them up (MDN).
- Do not allow `null` as an origin (sandboxed iframes and `file:` pages send it).
- `Access-Control-Max-Age`: a few minutes to hours (browsers cap it; Chromium at 2 hours) to cut preflight traffic.

```ts
const ALLOWED = new Set(["https://app.example.com", "https://admin.example.com"]);
app.use((req, res, next) => {
  res.vary("Origin");
  const origin = req.get("origin");
  if (origin && ALLOWED.has(origin)) {
    res.set("Access-Control-Allow-Origin", origin);
    res.set("Access-Control-Allow-Credentials", "true");
  }
  next();
});
```

## 4. Security headers: a default set

For HTML responses:

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{random}' 'strict-dynamic'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
Cross-Origin-Opener-Policy: same-origin
```

For JSON API responses (OWASP REST): `Cache-Control: no-store` on authenticated data, `Content-Type: application/json`, `X-Content-Type-Options: nosniff`, `Content-Security-Policy: frame-ancestors 'none'`, HSTS.

Rules:

- HSTS: only after the whole domain (and subdomains, if `includeSubDomains`) serve HTTPS. Start with a short `max-age` and raise it.
- CSP: nonce or hash based `script-src` with `'strict-dynamic'` is the modern default. `'unsafe-inline'` in `script-src` removes most of the XSS protection. Allowlisting whole CDNs (`https://cdn.jsdelivr.net`) lets an attacker load any package from it. Roll out with `Content-Security-Policy-Report-Only` first.
- `frame-ancestors 'none'` (or `'self'`) stops clickjacking; `X-Frame-Options: DENY` is the legacy fallback.
- Scripts from a third party CDN: pin the version and add Subresource Integrity (`integrity="sha384-..." crossorigin="anonymous"`), or self-host.
- Use a maintained middleware (`helmet` for Express, Next.js `headers()` config, `tower-http` `SetResponseHeader` layers in axum) instead of hand-setting headers in each route.
- Remove `X-Powered-By` and detailed `Server` banners.

## 5. Open redirects

`/login?next=https://evil.example` that redirects after login turns your domain into a phishing tool and leaks OAuth codes (RFC 9700: MUST NOT expose open redirectors).

- Accept only relative paths for `next`/`returnTo`: must start with a single `/`, not `//` and not `/\` (both are protocol-relative to browsers). Better: parse with `new URL(next, APP_ORIGIN)` and require `url.origin === APP_ORIGIN`.
- Or keep an allowlist of named destinations and pass a key, not a URL.

## 6. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| No unsanitized HTML sinks | every `dangerouslySetInnerHTML`/`v-html`/`{@html}`/`innerHTML` input passes through DOMPurify or is a constant | `rg -n "dangerouslySetInnerHTML\|v-html\|\{@html\|\.innerHTML *=\|insertAdjacentHTML\|document\.write\|bypassSecurityTrust" ` and read each |
| User URLs scheme-checked | `href`/`src` from user data only allow http(s) | `rg -n "href=\{[a-z]+\.(url\|link\|website)" ` and check validation |
| Markdown renderer safe | raw HTML disabled or output sanitized | `rg -n "marked\(\|markdown-it\|html: true\|rehype-raw" ` |
| No state change on GET | GET routes do not write | read GET handlers for `create\|update\|delete\|insert` |
| CSRF defense present | cookie-authenticated unsafe routes check Sec-Fetch-Site/Origin or a token | read middleware; `curl -X POST -H "Origin: https://evil.test" -b "session=..." ` returns 403 |
| CORS not reflective | no `origin: true`, no `cors()` with defaults on credentialed APIs, no regex/endsWith origin checks | `rg -n "origin: (true\|\"\*\"\|'\*')\|Access-Control-Allow-Origin.*\*\|cors\(\)\|endsWith\(.*origin\|CorsLayer::permissive\|allow_origin\(Any\)" ` |
| Vary: Origin | set when ACAO is dynamic | `curl -sI -H "Origin: https://app.example.com" ` |
| Headers set | HSTS, CSP, nosniff, frame-ancestors on HTML; nosniff and no-store on APIs | `curl -sI https://host/ ` and an API route; or securityheaders.com style check |
| No unsafe-inline scripts | CSP `script-src` has no `'unsafe-inline'` (or has nonces with strict-dynamic) | `rg -n "unsafe-inline\|unsafe-eval" ` |
| Third party scripts pinned | CDN scripts have `integrity` and a fixed version | `rg -n "<script[^>]+src=\"https?://" ` without `integrity` |
| No open redirect | `next`/`returnTo`/`redirect` params validated to same origin | `rg -n "redirect\((req\.query\|searchParams\.get)\|next=\|returnTo" ` |
