# Input validation, injection, SSRF, file uploads

Read when: code accepts data from outside its trust boundary (HTTP bodies, query strings, headers, webhooks, queue messages, files, URLs, LLM output, third party API responses) and uses it in a query, a shell command, HTML, a file path, an outgoing request, or a model.

Sources: OWASP cheat sheets (Input Validation, SQL Injection Prevention, Mass Assignment, Server Side Request Forgery Prevention, File Upload, Denial of Service, REST Security, XSS Prevention), OWASP ASVS 5.0 (V1, V2, V5), OWASP Top 10 2025 (A01, A05).

## Contents

1. The model: validate at the boundary, encode at the sink
2. Validation rules
3. SQL injection
4. Command injection and code execution
5. Mass assignment
6. Path traversal
7. SSRF
8. File uploads
9. Deserialization, prototype pollution, XML, ReDoS
10. LLM output is untrusted input
11. Checks

## 1. The model: validate at the boundary, encode at the sink

Two separate controls, both required:

- Validation at the trust boundary rejects data that is not the shape the operation expects. It is not a security control by itself: a valid name can still contain an apostrophe.
- Safe handling at the sink (the place the data is used) makes any value harmless there: parameterized SQL, argument arrays instead of shell strings, context-aware HTML encoding, fixed URL hosts, generated file names.

OWASP: validation "does not replace" parameterization or output encoding, and a valid account ID does not mean the caller may access that account (authorization is a third, separate check).

Trust boundaries include more than the browser: internal APIs, partner feeds, queue messages, webhook payloads, database rows written by another system, and LLM output all get validated when they cross into your code (OWASP Input Validation).

## 2. Validation rules

- Validate on the server, always. Client validation is UX only.
- Use a schema library at the edge of every handler: Zod, Valibot or TypeBox in TS; `serde` with typed structs plus `validator` or `garde` in Rust. Parse, do not just check: the handler body works with the parsed, typed value only.
- Reject unknown fields: Zod `.strict()`; serde `#[serde(deny_unknown_fields)]`. OWASP: listing a property in a schema neither requires it nor rejects unknown fields; configure both.
- Allowlist, do not denylist: define what is allowed (type, length, range, format, enum) and reject everything else. Do not try to strip "bad characters".
- Bound everything: max string length, max array length, max nesting depth, numeric min and max, max body size (enforced before parsing). An unbounded array of IDs is a denial of service.
- Semantic checks after syntax: end date after start date, quantity within stock, currency supported for this account.
- Normalize once if comparison needs it (Unicode NFC for usernames, lowercase for emails used as login), before validating, storing and comparing, and the same way everywhere (OWASP).
- Regex: anchor the full value (`^...$` or a full match API), bound the input length first, avoid nested quantifiers (ReDoS); in Rust the `regex` crate is linear time by design, in JS consider `re2` for user-supplied patterns.
- Emails: use a library check plus a confirmation email. Format validity does not prove ownership (OWASP).
- Reject on failure with a clear 400/422; never continue with partially validated data.
- Do not log rejected input verbatim; log the field name and the failure (OWASP Input Validation, log injection).

```ts
const CreateOrder = z.object({
  items: z.array(z.object({ sku: z.string().regex(/^[A-Z0-9-]{3,32}$/), qty: z.number().int().min(1).max(100) })).min(1).max(50),
  currency: z.enum(["EUR", "USD"]),
  note: z.string().max(500).optional(),
}).strict();
```

```rust
#[derive(serde::Deserialize, garde::Validate)]
#[serde(deny_unknown_fields)]
struct CreateOrder {
    #[garde(length(min = 1, max = 50), dive)] items: Vec<Item>,
    #[garde(skip)] currency: Currency,          // enum: unknown values fail to deserialize
    #[garde(length(max = 500))] note: Option<String>,
}
```

## 3. SQL injection

- Parameterize every value. Never build SQL with string concatenation, template literals, or `format!`, even after validation (OWASP: binding "still applies").
- Know your ORM's escape hatches; they are where injection lives now:
  - Prisma: `$queryRawUnsafe`, `$executeRawUnsafe`, `Prisma.raw()` are unsafe with input. Tagged `$queryRaw\`... ${x}\`` is parameterized.
  - Drizzle: `sql.raw()` is unsafe; `sql\`... ${x}\`` is parameterized.
  - Knex: `.raw("... " + x)`, `whereRaw` with concatenation.
  - TypeORM / Sequelize: `query()` with concatenated strings, `literal()`.
  - sqlx: `sqlx::query(&format!(...))` is unsafe; `query!`/`query("... $1").bind(x)` is safe. Diesel: `sql_query(format!(...))`.
  - Supabase JS: `.or()` / `.filter()` with interpolated strings build PostgREST filter syntax; validate the value or use the typed methods (`.eq`, `.in`).
- Identifiers (table, column, sort field, direction) cannot be parameters. Map user choices to fixed strings from an allowlist (OWASP):

```ts
const SORTS = { newest: "created_at DESC, id DESC", oldest: "created_at ASC, id ASC" } as const;
const orderBy = SORTS[parsed.sort] ?? SORTS.newest;   // never `ORDER BY ${req.query.sort}`
```

- `LIKE` patterns: parameterize and escape `%` and `_` in the user value if they must be literal.
- Least privilege database roles: the app role owns no DDL, is not a superuser, and cannot bypass RLS (OWASP: "DO NOT ASSIGN DBA OR ADMIN TYPE ACCESS"). Migrations run as a separate role.
- NoSQL injection: in MongoDB, an input of `{"$ne": null}` where a string was expected bypasses a login query. Validate types strictly (a string schema rejects objects) and use `$eq` explicitly.

## 4. Command injection and code execution

- Do not shell out when a library exists (image processing, archives, git, PDF).
- If you must run a process, pass an argument array without a shell: Node `execFile`/`spawn(cmd, args)` with `shell: false` (the default), Rust `std::process::Command::new(cmd).arg(x)`. Never `exec(\`convert ${file}\`)`, never `sh -c` with input.
- Arguments that start with `-` are options: put `--` before user-supplied positional arguments, or validate they do not start with `-` (`git` and `tar` option injection).
- Never `eval`, `new Function`, `vm.runInContext` as a sandbox, `setTimeout(string)`, or template engines rendering user-supplied templates (server-side template injection).

## 5. Mass assignment

Binding a request body straight onto a model lets a user set fields they should not (`role`, `is_admin`, `org_id`, `plan`, `balance`, `email_verified`, `owner_id`).

- Use a DTO or input schema listing only the editable fields (OWASP: allowlist, not a denylist of protected fields; a new sensitive column stays bindable unless someone remembers).
- Bad: `db.user.update({ data: req.body })`, `Object.assign(user, req.body)`, `{ ...existing, ...req.body }`, `User::from(payload)` with all fields public.
- Different roles get different schemas (`UserSelfUpdate` vs `AdminUserUpdate`), not one schema with `if` branches.

## 6. Path traversal

- Never build file paths from user input. Store files under generated names (UUIDs) and map IDs to paths in the database (OWASP File Upload, ASVS 5.3.2).
- If a user-supplied name must be used: reject `/`, `\`, `..`, NUL and control characters; resolve the final path and verify it is inside the base directory after resolution (`path.resolve(base, name).startsWith(base + path.sep)`; in Rust canonicalize and `starts_with`). Watch symlinks.
- Archive extraction (zip slip): ignore entry paths, or validate each resolved entry path stays inside the target; reject symlink entries (ASVS 5.3.3, 5.2.5).

## 7. SSRF

Any feature that fetches a URL the user influences is SSRF prone: link previews, avatar from URL, import from URL, webhook endpoints, PDF/HTML renderers, OAuth/OIDC discovery URLs, image proxies. Targets: the cloud metadata service (`169.254.169.254`, `metadata.google.internal`) that hands out credentials, internal admin panels, Redis on localhost. OWASP folded SSRF into A01 Broken Access Control in 2025.

Rules (OWASP SSRF cheat sheet):

1. Prefer an allowlist of hosts. If the feature only talks to known services, accept an identifier, not a URL, and build the URL yourself with a fixed scheme, host and path.
2. If arbitrary URLs are the feature (link previews, customer webhooks):
   - Allow only `http` and `https`. Reject `file:`, `gopher:`, `dict:`, `ftp:`, `data:`, `jar:`, `phar:`.
   - Resolve DNS yourself, check every returned A/AAAA address against blocked ranges, then connect to that exact validated IP (keep the hostname for `Host` and TLS SNI). Checking the hostname and then letting the HTTP client resolve again is defeated by DNS rebinding (OWASP: "Domain allowlisting alone does not prevent DNS rebinding").
   - Block: `127.0.0.0/8`, `0.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `100.64.0.0/10`, `::1/128`, `fc00::/7`, `fe80::/10`, `::ffff:0:0/96` (IPv4-mapped), multicast, and your own public IPs.
   - Disable redirects in the client, or re-validate every hop.
   - Timeouts, a max response size, and no response body echoed back verbatim when not needed.
   - Do not accept URLs with credentials (`user@host`), and reject inputs whose host differs between URL parsers (`http://example.com\@evil.com`, OWASP).
3. Use an egress proxy that enforces this (Stripe's `smokescreen`) or a vetted library (`ssrf-req-filter`, `request-filtering-agent` for Node), and run fetching workers in a network segment without access to internal services.
4. Cloud: require IMDSv2 on AWS (token-based metadata), which blocks most SSRF credential theft.

## 8. File uploads

Rules (OWASP File Upload, ASVS V5):

- Authenticate uploads and authorize downloads per file. A public bucket with guessable keys is an IDOR.
- Allowlist extensions and validate content: check magic bytes against the claimed type; do not trust `Content-Type` from the client or the filename extension alone.
- Size limits on the request and per file, enforced while streaming, not after buffering everything in memory. Per user quota on count and total bytes (ASVS 5.2.4).
- Generate the stored name (UUID plus validated extension). Keep the original name only as metadata, sanitized when echoed in `Content-Disposition` (RFC 6266 `filename*`).
- Store outside the web root, ideally in object storage on a different domain (for example a separate `usercontent` domain), never on the app's own origin. An HTML or SVG file served from your origin is stored XSS.
- Serve user files with `Content-Disposition: attachment` unless inline display is required, `X-Content-Type-Options: nosniff`, and a correct `Content-Type`. For inline images, serve only re-encoded raster images.
- Images: decode and re-encode (strips metadata and polyglots), cap pixel dimensions before decoding to stop decompression bombs (ASVS 5.2.6).
- SVG: treat as HTML (it can contain script). Sanitize (DOMPurify with SVG profile) or rasterize, or serve as attachment only.
- Archives: check uncompressed size and file count before extracting (ASVS 5.2.3); zip slip rules above.
- Direct-to-storage uploads (S3 presigned POST, Supabase Storage signed upload URL): sign with a content length range and content type condition, short expiry (minutes), and a server-chosen key. Then validate the object server side before marking it usable.
- Scan with antivirus or a sandbox where users share files with other users (ASVS 5.4.3).

## 9. Deserialization, prototype pollution, XML, ReDoS

- Never deserialize untrusted data with formats that can instantiate types: Python `pickle`, Java native serialization, PHP `unserialize`, YAML loaders with custom tags (`yaml.load` without `SafeLoader`), `node-serialize`. JSON into a schema is fine. Serde into concrete structs is fine.
- Prototype pollution (JS): deep merge or path-set helpers fed with `{"__proto__": {"isAdmin": true}}` poison every object. Do not deep-merge request bodies into objects; validate with a strict schema first; use `Object.create(null)` or `Map` for user-keyed dictionaries; reject `__proto__`, `constructor`, `prototype` keys.
- XML: disable external entities and DTDs (XXE). In Node, most parsers do not resolve external entities by default; in other stacks configure it explicitly. Prefer JSON.
- GraphQL: depth limit, cost limit or persisted query allowlist, and introspection off in production for private APIs (ASVS 4.3.1, 4.3.2).

## 10. LLM output is untrusted input

Text produced by a model that read user content or web pages is attacker influenced (prompt injection). Treat it like a request body:

- Never pass it to `eval`, a shell, raw SQL, or `innerHTML`.
- Tools called by an agent run with the end user's permissions, not a service account's, and with allowlisted arguments validated by schema.
- URLs the model emits are SSRF inputs when fetched server side and exfiltration channels when rendered as images or links client side (data in the query string). Allowlist domains for auto-fetched or auto-rendered URLs.

## 11. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| No string-built SQL | no SQL with interpolation or concatenation of variables | `rg -n "(query\|execute\|raw\|Raw)(Unsafe)?\(\s*\`[^\`]*\\$\{" --type ts`; `rg -n "\$queryRawUnsafe\|\$executeRawUnsafe\|sql\.raw\(\|whereRaw\(\|Prisma\.raw\(" `; Rust `rg -n "query(_as)?\(&format!\|sql_query\(format!" ` |
| Identifiers from allowlists | `ORDER BY`, column and table names never come from input | `rg -n "ORDER BY \\$\{\|orderBy: req\.\|order_by.*format!" ` |
| No shell with input | no `exec(`/`execSync(` with template strings; no `shell: true`; no `sh -c` | `rg -n "exec(Sync)?\(\`\|shell: true\|\"sh\", \"-c\"\|Command::new\(\"sh\"\)" ` |
| No eval | no `eval(`, `new Function(`, `vm.runIn` on input | `rg -n "\beval\(\|new Function\(\|vm\.runIn" ` |
| Strict schemas | input schemas reject unknown keys | `rg -n "z\.object\(" ` without `.strict()` on request schemas; `rg -n "derive\(.*Deserialize" ` structs used as request bodies lack `deny_unknown_fields` |
| No mass assignment | no `data: req.body`, `Object.assign(x, req.body)`, `...req.body` | `rg -n "data: req\.body\|Object\.assign\([^,]+, req\.body\|\.\.\.req\.body" ` |
| Body size limit | JSON body limit configured | `rg -n "json\(\{ *limit\|bodyLimit\|DefaultBodyLimit\|content_length_limit" ` |
| No user paths | file system calls do not use request values in paths | `rg -n "(readFile\|createReadStream\|writeFile\|unlink\|File::open)\(.*(req\.\|params\|query)" ` |
| SSRF guard | every server-side fetch of a user-influenced URL goes through the guarded client | `rg -n "fetch\((req\.\|body\.\|url\b\|input\.)" `; list URL-taking features and read each |
| Upload validation | uploads check size, magic bytes, generate names, store off-origin | read upload handler; `rg -n "originalname\|file\.name" ` used as storage key |
| Safe deserialization | no `pickle.loads`, `yaml.load(` without SafeLoader, `unserialize(`, `node-serialize` | `rg -n "pickle\.loads\|yaml\.load\(\|unserialize\(\|node-serialize" ` |
| Prototype pollution | no deep merge of request data; lodash `merge`/`set` not fed input | `rg -n "_\.merge\(\|_\.set\(\|deepmerge\(.*req\." ` |
| Static analysis | Semgrep OWASP rulesets pass | `semgrep --config p/owasp-top-ten --config p/javascript --config p/typescript` (Rust: `--config p/rust`) |
