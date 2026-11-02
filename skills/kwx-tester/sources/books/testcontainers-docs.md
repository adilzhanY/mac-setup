# Testcontainers for Node.js (guide and PostgreSQL module)

- Author: Testcontainers project (AtomicJar / Docker)
- Year: read 2026-10-31 (@testcontainers/postgresql 12.2.1)
- Legal URL: https://testcontainers.com/guides/getting-started-with-testcontainers-for-nodejs/ ; https://node.testcontainers.org/modules/postgresql/

## What I read

The Node getting started guide and the PostgreSQL module page.

## Key lessons used in backend/database-testing.md (also backend.md)

- `new PostgreSqlContainer(image).start()`, `getConnectionUri()`, `stop()` in afterAll.
- `snapshot()` and `restoreSnapshot()`; close connections first; do not use the `postgres` database name with snapshots.
