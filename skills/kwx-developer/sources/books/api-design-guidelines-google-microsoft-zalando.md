# API design guidelines: Google AIP, Microsoft Azure REST guidelines, Zalando RESTful guidelines

Legal free sources:
- Google API Improvement Proposals: https://google.aip.dev/ (read AIP-158 Pagination, AIP-180 Backwards compatibility, AIP-193 Errors)
- Microsoft REST API Guidelines (Azure): https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md (read most of the document)
- Zalando RESTful API Guidelines: https://opensource.zalando.com/restful-api-guidelines/ (read the rule index and the compatibility, naming, pagination, error and idempotency rules)

## Key lessons used in backend/api-design.md

- Paginate every list from day one; adding pagination later is a breaking change because old clients stop at page one (AIP-158, Microsoft). Opaque URL-safe tokens, not user parseable (base64 is not obfuscation), tokens never grant authorization, reject changed filters between pages, empty next token is the only end signal, may expire (about 3 days).
- Prefer cursor pagination, avoid offset and total counts (Zalando #160, #254).
- Breaking changes (AIP-180): removing or renaming anything, changing types even when wire compatible, adding required fields, changing defaults or default serialization, stricter validation or resource name formats, raising max lengths, changing value formats, adding pagination.
- Errors (AIP-193): stable machine reason (max 63 chars, UPPER_SNAKE) plus domain, request specific data in metadata not in the message, check permission before existence to avoid leaking it.
- Microsoft: PATCH with JSON Merge Patch, PUT for full replace, no nulls in responses, do not return secrets on GET, reject unknown fields with 400, LRO when p99 over 1 s with 202 and Operation-Location, keep status 24 h, ETags preferred over timestamps, repeatability headers for POST, integers within 2^53, RFC 3339 dates, units in duration names, extensible enums, never remove enum values.
- Zalando: API first with OpenAPI, tolerant reader, top level JSON objects only, snake_case properties, kebab-case paths, avoid versioning and never URL versioning, null and absent mean the same, never null booleans or null arrays, money as decimal amount plus ISO 4217 currency and as a closed type, idempotent POST via secondary key or Idempotency-Key, 429 with headers, problem JSON, no stack traces.
