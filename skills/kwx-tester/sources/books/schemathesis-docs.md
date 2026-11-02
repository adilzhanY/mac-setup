# Schemathesis documentation

- Author: Schemathesis project (Dmitry Dygalo and contributors)
- Year: living documentation, read 2026-10-31 (v4.32)
- Legal URL: https://schemathesis.readthedocs.io/en/stable/ ; https://schemathesis.readthedocs.io/en/stable/quick-start/ ; https://schemathesis.readthedocs.io/en/stable/reference/checks/

## What I read

Home page, quick start, checks reference.

## Key lessons used in backend/contract-and-schema-testing.md (also api-testing.md)

- Supports OpenAPI 2.0 to 3.2 and GraphQL; stateful testing through OpenAPI links; failures come with a curl reproducer.
- `uvx schemathesis run <schema-url> --header ...`, `--url` for a local schema file, `schemathesis replay <ID>`.
- All checks on by default except `max_response_time`; includes `ignored_auth`, `use_after_free`, `ensure_resource_availability`, and `object_level_authorization` when two or more peers are configured.
- pytest integration with `schemathesis.openapi.from_url` and `case.call_and_validate()`.
