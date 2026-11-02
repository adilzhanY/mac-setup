# The Idempotency-Key HTTP Header Field (Internet-Draft)

- Authors: Jayadeba Jena, Sanjay Dalal (IETF HTTPAPI working group)
- Year: draft-ietf-httpapi-idempotency-key-header-08, 22 October 2026
- Legal URL: https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/

## What I read

The datatracker page summary and the error handling, fingerprint and expiry sections.

## Key lessons used in backend/api-testing.md

- 400 when a required key is missing, 422 when a key is reused with a different payload, 409 when a retry arrives while the first request is in progress.
- Optional payload fingerprint to detect a reused key with a different body.
- Resources publish their expiry policy for keys.
