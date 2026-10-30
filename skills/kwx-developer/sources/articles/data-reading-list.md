# Data topic reading list

Sources read for `data/` (2026-10-30). "Read" means fetched and read; "skimmed" means search results only.

## PostgreSQL docs (read)

- Explicit locking (lock modes, conflicts, deadlocks, advisory locks): https://www.postgresql.org/docs/current/explicit-locking.html
- ALTER TABLE (lock per subcommand, rewrites, NOT VALID, SET NOT NULL scan skip, USING INDEX): https://www.postgresql.org/docs/current/sql-altertable.html
- Transaction isolation (levels, 40001, retries, SSI advice): https://www.postgresql.org/docs/current/transaction-iso.html
- CREATE INDEX (CONCURRENTLY, invalid indexes, INCLUDE, NULLS NOT DISTINCT): https://www.postgresql.org/docs/current/sql-createindex.html
- Partial indexes: https://www.postgresql.org/docs/current/indexes-partial.html
- Using EXPLAIN: https://www.postgresql.org/docs/current/using-explain.html
- Constraints (FK not auto indexed, ON DELETE, EXCLUDE, NULLs in unique): https://www.postgresql.org/docs/current/ddl-constraints.html
- Generated columns (PG 18 virtual default): https://www.postgresql.org/docs/current/ddl-generated-columns.html
- JSON types (jsonb vs json, GIN opclasses, document design): https://www.postgresql.org/docs/current/datatype-json.html
- ALTER TYPE (enum ADD VALUE, no DROP VALUE): https://www.postgresql.org/docs/current/sql-altertype.html
- Continuous archiving and PITR: https://www.postgresql.org/docs/current/continuous-archiving.html
- pg_dump: https://www.postgresql.org/docs/current/app-pgdump.html
- Wiki, Don't Do This: https://wiki.postgresql.org/wiki/Don't_Do_This

## Use The Index, Luke (read, see sources/books/use-the-index-luke.md)

- https://use-the-index-luke.com/sql/where-clause/the-equals-operator/concatenated-keys
- https://use-the-index-luke.com/sql/where-clause/searching-for-ranges/greater-less-between-tuning-sql-access-filter-predicates
- https://use-the-index-luke.com/sql/where-clause/obfuscation
- https://use-the-index-luke.com/no-offset
- https://use-the-index-luke.com/sql/partial-results/fetch-next-page

## SQLite docs (read)

- WAL: https://www.sqlite.org/wal.html
- When to use: https://www.sqlite.org/whentouse.html
- STRICT tables: https://www.sqlite.org/stricttables.html
- Foreign keys: https://www.sqlite.org/foreignkeys.html
- VACUUM / VACUUM INTO: https://www.sqlite.org/lang_vacuum.html
- Backup API: https://www.sqlite.org/backup.html

## SQLite BUSY behaviour (skimmed, consistent across sources)

- Bert Hubert, SQLITE_BUSY despite timeout: https://berthub.eu/articles/posts/a-brief-post-on-sqlite3-database-locked-despite-timeout
- Simon Willison, SQLite busy: https://simonwillison.net/2025/Feb/17/sqlite-busy
- SQLite forum on DEFERRED vs IMMEDIATE: https://sqlite.org/forum/forumpost/04ed1d235b

## Migrations (read)

- strong_migrations README: https://github.com/ankane/strong_migrations
- Squawk rules index: https://squawkhq.com/docs/rules
- Squawk require-timeout-settings: https://squawkhq.com/docs/require-timeout-settings
- Squawk adding-serial-primary-key-field: https://squawkhq.com/docs/adding-serial-primary-key-field
- Squawk CLI and config: https://squawkhq.com/docs/cli
- GitLab migration style guide: https://docs.gitlab.com/development/migration_style_guide/
- Stripe, Online migrations at scale: https://stripe.com/blog/online-migrations
- GitHub, gh-ost: https://github.blog/engineering/infrastructure/gh-ost-github-s-online-migration-tool-for-mysql/

## Transactions and integrity (read)

- Brandur, Implementing Stripe-like idempotency keys in Postgres: https://brandur.org/idempotency-keys
- Brandur, Soft deletion probably isn't worth it: https://brandur.org/soft-deletion

## Supabase (read)

- Row level security: https://supabase.com/docs/guides/database/postgres/row-level-security
- Backups and PITR: https://supabase.com/docs/guides/platform/backups

## Local first and sync (read)

- Ink and Switch, Local-first software: https://www.inkandswitch.com/essay/local-first/
- PowerSync consistency: https://docs.powersync.com/architecture/consistency
- ElectricSQL write patterns: https://electric.ax/docs/guides/writes

## Backups (read)

- GitLab 2017 postmortem: https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/
- Litestream, how it works: https://litestream.io/how-it-works/

## ORMs (read or skimmed)

- Prisma query optimization: https://www.prisma.io/docs/orm/prisma-client/queries/query-optimization-performance
- Drizzle vs Prisma vs Kysely comparisons (skimmed, opinion): https://www.pkgpulse.com/guides/drizzle-orm-v1-vs-prisma-6-vs-kysely-2026

## Keys and UUIDs (skimmed)

- credativ, UUIDv4 vs UUIDv7 in PostgreSQL 18: https://www.credativ.de/en/blog/postgresql-en/a-deeper-look-at-old-uuidv4-vs-new-uuidv7-in-postgresql-18/
- Better Stack, PostgreSQL 18 UUID guide: https://betterstack.com/community/guides/databases/postgresql-18-uuid/

## Backup practice and law (skimmed)

- 3 2 1 rule and restore testing: https://dev.to/ryan_bell/the-3-2-1-backup-rule-in-practice-and-the-restore-test-everyone-skips-47i
- GDPR Article 20 explained: https://www.legiscope.com/blog/gdpr-article-20-portability-text-explained.html

## Not read

- Squawk per rule pages beyond the three above (rule names only).
- Prisma transactions reference (interactive transaction default timeouts taken from memory: timeout 5 s, maxWait 2 s; verify).
- Drizzle and Kysely official docs pages (API names from prior knowledge).
- Litestream configuration and tips pages (single writer and checkpoint advice from prior knowledge).
