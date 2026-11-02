# Supabase testing documentation

- Author: Supabase
- Year: living documentation, read 2026-10-31 (CLI 2.122)
- Legal URL: https://supabase.com/docs/guides/local-development/testing/overview ; https://supabase.com/docs/guides/database/testing ; https://supabase.com/docs/guides/database/postgres/testing-row-level-security ; https://supabase.com/docs/guides/local-development/testing/pgtap-extended ; https://supabase.com/docs/reference/cli/supabase-start ; https://supabase.com/docs/reference/cli/supabase-test-db ; https://supabase.com/docs/guides/local-development/cli/getting-started ; https://supabase.com/docs/guides/database/connecting-to-postgres/pooling-and-limits

## What I read

Testing overview, database testing with pgTAP, RLS testing guide, advanced pgTAP guide with test helpers, CLI reference for start, test db and db reset, local development getting started, pooling and limits.

## Key lessons used in backend/database-testing.md (also backend.md, api-testing.md, external-services-and-time.md, performance/load-testing.md)

- Tests in `supabase/tests/database/*.sql`, run by `supabase test db` (pg_prove in a container); `--linked` runs against the remote project.
- Each file: `begin; select plan(n); ... select * from finish(); rollback;`.
- Act as a user with `set local role authenticated;` and JWT claims in `request.jwt.claim(s)`.
- A blocked update returns no rows (assert with `is_empty`), a blocked insert raises 42501 (`throws_ok`).
- Do not drop the policy to test denial; add a temporary `using (true)` policy and see a test fail.
- A `pg_policies` check can pass while the policy is wrong; test through roles and returned rows.
- App level tests cannot roll back: unique ids, filter by own ids, no whole table assertions.
- basejump-supabase_test_helpers: `tests.create_supabase_user`, `tests.authenticate_as`, `tests.rls_enabled`.
- Local ports 54321 to 54324 (API, DB, Studio, Mailpit); `supabase start -x` to exclude containers.
- Poolers stop accepting new clients at the compute's limit.
