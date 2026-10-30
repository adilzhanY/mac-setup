# Backend, APIs and security: reading list

Sources read for `backend/` and `security/` (2026-10-30). "Read" means the page was fetched and its rules extracted; "partial" means only the named sections.

## API design

- Google AIP-158 Pagination: https://google.aip.dev/158 (read)
- Google AIP-180 Backwards compatibility: https://google.aip.dev/180 (read)
- Google AIP-193 Errors: https://google.aip.dev/193 (read)
- Microsoft Azure REST API Guidelines: https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md (read, first 100k characters)
- Zalando RESTful API Guidelines: https://opensource.zalando.com/restful-api-guidelines/ (partial: rule index and main rules; appendices not read)
- RFC 9457 Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc9457.html (read)
- Stripe idempotent requests: https://docs.stripe.com/api/idempotent_requests (read)
- Brandur Leach, Implementing Stripe-like idempotency keys in Postgres: https://brandur.org/idempotency-keys (read)
- Stripe, APIs as infrastructure: future-proofing Stripe with versioning: https://stripe.com/blog/api-versioning (read)
- Stripe, Designing APIs for humans: object IDs: https://dev.to/stripe/designing-apis-for-humans-object-ids-3o5a (read)
- Markus Winand, No Offset: https://use-the-index-luke.com/no-offset (read)

## Rate limits, retries, timeouts, overload

- AWS Architecture Blog, Exponential Backoff And Jitter: https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/ (read; formulas are images, taken from known text)
- AWS Builders' Library, Timeouts, retries, and backoff with jitter: https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter (read)
- AWS Builders' Library, Using load shedding to avoid overload: https://builder.aws.com/content/3Eun1EEyX6p2e3VYNyRLSJzLuMV/using-load-shedding-to-avoid-overload (read)
- AWS Builders' Library, Avoiding insurmountable queue backlogs: https://builder.aws.com/content/3EuRcgkTP1MI0c7zM8W6HL3WIqA/avoiding-insurmountable-queue-backlogs (read)
- Google SRE book ch. 21 Handling Overload: https://sre.google/sre-book/handling-overload/ (read)
- Google SRE book ch. 22 Addressing Cascading Failures: https://sre.google/sre-book/addressing-cascading-failures/ (read)
- Stripe, Scaling your API with rate limiters: https://stripe.com/blog/rate-limiters (read)
- Cloudflare, How we built rate limiting capable of scaling to millions of domains: https://blog.cloudflare.com/counting-things-a-lot-of-different-things/ (read)
- IETF draft-ietf-httpapi-ratelimit-headers-11 (May 2026): https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/ (read summary)
- Martin Fowler, CircuitBreaker: https://martinfowler.com/bliki/CircuitBreaker.html (read)
- TanStack Query, Important defaults: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults (read)

## Caching

- AWS Builders' Library, Caching challenges and strategies: https://builder.aws.com/content/3K9TeXp6strMiJ4vhakpRD7BQWO/caching-challenges-and-strategies (read)
- RFC 5861 HTTP Cache-Control extensions for stale content: https://www.rfc-editor.org/rfc/rfc5861.html (read)

## Webhooks, queues, jobs

- Stripe webhooks: https://docs.stripe.com/webhooks (read in full)
- Standard Webhooks specification: https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md (read)
- microservices.io, Transactional outbox: https://microservices.io/patterns/data/transactional-outbox.html (read)

## Auth

- OWASP Authentication, Session Management, Password Storage, Authorization, JSON Web Token cheat sheets: https://cheatsheetseries.owasp.org/ (read)
- NIST SP 800-63B-4: https://pages.nist.gov/800-63-4/sp800-63b.html (partial: passwords and reauthentication)
- RFC 9700 OAuth 2.0 Security Best Current Practice: https://www.rfc-editor.org/rfc/rfc9700.html (first 100k characters)
- OAuth 2.1 draft 16 status: https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/ (status only)
- web.dev, Sign in with a passkey through form autofill: https://web.dev/articles/passkey-form-autofill (read)
- Supabase, Row Level Security: https://supabase.com/docs/guides/database/postgres/row-level-security (read)
- Supabase, RLS performance and best practices: https://supabase.com/docs/guides/troubleshooting/rls-performance-and-best-practices-Z5Jjwv (read)

## Security

- OWASP Top 10 2025: https://top10.owasp.org/2025/ and introduction https://top10.owasp.org/2025/0x00_2025-Introduction/ (read)
- OWASP ASVS 5.0.0: https://github.com/OWASP/ASVS/tree/master/5.0/en (partial: levels, V4, V5, V8)
- OWASP cheat sheets: Input Validation, SQL Injection Prevention, Cross Site Scripting Prevention, Cross-Site Request Forgery Prevention, Server Side Request Forgery Prevention, File Upload, Secrets Management, Logging, REST Security, Mass Assignment, Denial of Service (read)
- MDN, Cross-Origin Resource Sharing guide: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS (read)

## Supply chain

- GitHub, Security hardening for GitHub Actions: https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions (read)
- npm, Generating provenance statements: https://docs.npmjs.com/generating-provenance-statements (read)
- pnpm, Supply chain security: https://pnpm.io/supply-chain-security (read)
- npm `min-release-age` (v11.10): https://docs.npmjs.com/cli/v11/using-npm/config (not opened; facts from classmethod article https://dev.classmethod.jp/articles/npm-v11-min-release-age/ and npm/cli PR #9378)
- cargo-deny book: https://embarkstudios.github.io/cargo-deny/ (read overview)
- actions/dependency-review-action: https://github.com/actions/dependency-review-action (read)
- gitleaks README and pre-commit hook definition: https://github.com/gitleaks/gitleaks (read)
- trufflehog README: https://github.com/trufflesecurity/trufflehog (read usage)

## Covered by other agents' notes

- `sources/books/aws-builders-library.md` and `sources/books/google-sre-book.md` (reliability agent) cover the same AWS and SRE chapters in more breadth.
