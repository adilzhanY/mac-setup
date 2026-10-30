# Indexes and queries

How to make queries use indexes, how to prove it, and the query shapes that defeat indexes. Main source: Markus Winand, "Use The Index, Luke" (use-the-index-luke.com), plus the PostgreSQL docs.

## Contents

1. How to design an index
2. Index types and options
3. Indexes you must have, and indexes to drop
4. Query shapes that defeat an index
5. Reading EXPLAIN
6. Pagination
7. N+1 and other app side query bugs
8. Checks

## 1. How to design an index

- Start from the queries, not the table. List the WHERE, JOIN and ORDER BY of each hot query, then design the fewest indexes that serve them all.
- A B-tree on `(a, b, c)` serves queries on `a`, `a, b` and `a, b, c`. It does not serve a query on `b` alone (leftmost prefix rule). One well ordered composite index beats two single column ones: less storage, cheaper writes.
- **Equality first, range last.** Columns compared with `=` go first, then at most one range column (`<`, `>`, `BETWEEN`, `LIKE 'x%'`). After a range column, later columns are only filter predicates: they are checked row by row, they do not narrow the scan.

```sql
-- query
select * from orders where user_id = $1 and created_at >= $2 order by created_at desc limit 20;
-- good: equality, then range and sort column
create index orders_user_created_idx on orders (user_id, created_at desc);
-- bad: range column first, the scan reads every user's recent orders
create index orders_created_user_idx on orders (created_at, user_id);
```

- An index that matches the ORDER BY (same columns, same direction or fully reversed) lets the database stop after `LIMIT` rows ("pipelined" top-N). Without it the database sorts every matching row first.
- Keep non-unique indexes to about 3 columns (strong_migrations rule). Wider indexes cost writes and rarely add selectivity.
- Covering index: `CREATE INDEX ... (user_id, created_at) INCLUDE (status, total_cents)` allows an Index Only Scan for a list query that reads only those columns. INCLUDE columns cannot be searched and bloat the index; use it only for a proven hot query.
- Every index slows every INSERT, every UPDATE of an indexed column (and kills HOT updates in Postgres), and costs disk and cache. Do not index "just in case".

## 2. Index types and options

| Need | Index |
|---|---|
| Equality, range, sort, prefix LIKE | B-tree (default) |
| Case insensitive lookup | expression index `(lower(email))`, query with `lower(email) = lower($1)` |
| Subset of rows (unbilled orders, active rows, not deleted) | partial index `WHERE billed IS NOT TRUE`; the query must contain the same predicate literally, a bind parameter does not match |
| Unique among a subset | partial unique index `WHERE deleted_at IS NULL` |
| `jsonb` containment | GIN `jsonb_path_ops`; for one key, a B-tree on `(doc->>'key')` |
| Full text | GIN on a tsvector (stored generated column) |
| `LIKE '%term%'` / fuzzy | GIN with `pg_trgm` (`gin_trgm_ops`) |
| Overlapping ranges, geometry | GiST |
| Huge append only table ordered by time | BRIN on the time column (tiny, coarse) |

- Do not create one partial index per category value (`WHERE category = 1`, `= 2` ...). The planner tests each one. Use one composite index `(category, data)` or partitioning.
- In SQLite, partial and expression indexes also exist; `EXPLAIN QUERY PLAN` shows `USING INDEX` vs `SCAN`.

## 3. Indexes you must have, and indexes to drop

Must have:

- An index on each foreign key column (Postgres and SQLite do not create it). Without it, deleting a parent row scans the whole child table, under a lock, and joins from parent to children seq scan.
- An index that leads with `tenant_id` / `user_id` on tenant owned tables, and on every column used in an RLS policy.

Find unindexed foreign keys (Postgres):

```sql
select c.conrelid::regclass as table_name, a.attname as fk_column
from pg_constraint c
join pg_attribute a on a.attrelid = c.conrelid and a.attnum = c.conkey[1]
where c.contype = 'f'
  and not exists (
    select 1 from pg_index i
    where i.indrelid = c.conrelid and i.indkey[0] = c.conkey[1]
  );
```

Drop candidates (after 30 days of stats, on the primary and every replica that serves reads):

```sql
select relname, indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
from pg_stat_user_indexes
where idx_scan = 0 and indexrelname not like '%_pkey'
order by pg_relation_size(indexrelid) desc;
```

Also drop exact duplicates and indexes that are a leftmost prefix of another index (`(a)` when `(a, b)` exists), unless the narrow one is unique.

Invalid indexes left by a failed `CREATE INDEX CONCURRENTLY` still cost writes and are never used:

```sql
select indexrelid::regclass from pg_index where not indisvalid;
```

## 4. Query shapes that defeat an index

| Bad | Why | Good |
|---|---|---|
| `where date(created_at) = '2026-10-01'` | function on the column | `where created_at >= '2026-10-01' and created_at < '2026-10-02'` |
| `where lower(email) = $1` with an index on `email` | expression does not match the index | index `(lower(email))`, or store normalized |
| `where id::text = $1`, or comparing a text column to a number | type cast on the column side | cast the parameter, keep column types matching |
| `where (a = $1 or $1 is null) and (b = $2 or $2 is null)` ("smart logic") | one plan for all cases, usually a seq scan | build the WHERE dynamically with only the filters given (query builder) |
| `where price * 1.2 > 100` | math on the column | `where price > 100 / 1.2` |
| `where first_name \|\| ' ' \|\| last_name = $1` | concatenated columns | compare columns separately, or index the expression |
| `where name like '%term'` | leading wildcard | trigram GIN index, or full text search |
| `where x not in (select y from t)` | returns nothing if any `y` is NULL, and plans badly | `where not exists (select 1 from t where t.y = x.x)` |
| `select *` in hot list queries | blocks index only scans, ships unused columns, breaks when columns are added | name the columns |
| `count(*)` on a big table for a badge | full scan every time | maintain a counter, or `pg_class.reltuples` for an estimate |
| `order by random() limit 1` | sorts the whole table | `tablesample`, or pick a random key in range |

## 5. Reading EXPLAIN

- Use `EXPLAIN (ANALYZE, BUFFERS)` on a copy of production data size. ANALYZE executes the statement; wrap writes in `BEGIN; ... ROLLBACK;`. Plans on a 100 row dev table say nothing about a 10M row table: the planner seq scans small tables on purpose.
- Read in this order:
  1. Estimated `rows=` vs `actual rows=` on each node. Off by 10x or more means bad statistics: run `ANALYZE table;`, and for correlated columns `CREATE STATISTICS`.
  2. `loops=`: per loop numbers times loops is the real cost. A nested loop with `loops=50000` over an Index Scan is the N+1 of SQL.
  3. `Rows Removed by Filter`: large compared to rows returned means a missing or badly ordered index (the condition is a filter, not an index condition).
  4. `Seq Scan` on a large table with a selective WHERE: missing index or an obfuscated condition (section 4).
  5. `Sort` with `external merge Disk`: raise `work_mem` for that query or add an index that matches ORDER BY.
  6. `shared read` (disk) vs `shared hit` (cache) in BUFFERS.
- In app code, log slow queries instead of guessing: Postgres `log_min_duration_statement = 250ms` and the `pg_stat_statements` extension (`select query, calls, mean_exec_time, total_exec_time from pg_stat_statements order by total_exec_time desc limit 20;`). Total time, not mean time, finds the query worth fixing.
- SQLite: `EXPLAIN QUERY PLAN select ...`; `SCAN table` on a big table is the seq scan; `SEARCH table USING INDEX` is good. Run `ANALYZE` (or `PRAGMA optimize` before closing long lived connections) so the planner has statistics.

## 6. Pagination

- OFFSET reads and throws away every skipped row, so page 500 costs 500 pages of work, and rows inserted between requests shift the pages (duplicates and gaps in infinite scroll).
- Use keyset (seek) pagination with a unique tie breaker and a matching index:

```sql
create index posts_feed_idx on posts (created_at desc, id desc);

-- first page
select id, title, created_at from posts order by created_at desc, id desc limit 20;
-- next page: the cursor is the last row's (created_at, id)
select id, title, created_at from posts
where (created_at, id) < ($1, $2)
order by created_at desc, id desc
limit 20;
```

- Row value comparison `(a, b) < ($1, $2)` uses the index in Postgres and SQLite (3.15+). MySQL evaluates it correctly but may not use it as an index range; expand it there: `a < $1 or (a = $1 and b < $2)`.
- Encode the cursor as an opaque base64 string in the API; never let clients send raw SQL fragments or column names.
- Keep OFFSET only for small admin tables or when "jump to page N" is a hard requirement, and cap the max page.

## 7. N+1 and other app side query bugs

- N+1: one query for a list, then one per item. It hides in ORM lazy loading, GraphQL resolvers, and `await` inside `for` / `.map`.

```ts
// bad: 1 + N queries
const posts = await db.select().from(postsTable).limit(50);
for (const p of posts) p.author = await db.query.users.findFirst({ where: eq(users.id, p.authorId) });

// good: 2 queries, or one join
const posts = await db.select().from(postsTable).limit(50);
const authors = await db.select().from(users).where(inArray(users.id, [...new Set(posts.map(p => p.authorId))]));
```

- Detection: count queries per request in tests. Fail the test when a list endpoint issues more than a fixed number of queries for 1 row and for 20 rows (the count must be equal). See `orm-and-query-layers.md` for per ORM logging.
- Batch writes: one multi row `INSERT ... VALUES (...), (...)` or `COPY` / `unnest` arrays, not 1000 single inserts. In SQLite, wrap bulk inserts in one transaction (each autocommit insert is an fsync).
- Upsert with `INSERT ... ON CONFLICT (key) DO UPDATE` rather than select then insert (which races).
- Connection pools: one pool per process, sized near `(cores * 2)` on the database side in total, not per instance. Serverless functions need a pooler (PgBouncer in transaction mode, Supavisor, Neon pooler); in transaction mode, session state (`SET`, prepared statements, advisory session locks) does not survive between transactions.

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| New query on a big table uses an index | Index Scan / Index Only Scan / Bitmap, no large Rows Removed by Filter | `EXPLAIN (ANALYZE, BUFFERS)` on production sized data, pasted in the PR |
| FK columns indexed | query returns no rows | SQL in section 3 |
| No invalid indexes | no rows | `select indexrelid::regclass from pg_index where not indisvalid;` |
| No unused indexes | each zero scan index justified | SQL in section 3 |
| No functions on indexed columns in WHERE | none | `grep -rniE "where[^;]*\b(date\|lower\|upper\|trunc\|cast)\(" src/` then inspect |
| No `NOT IN (select` | none | `grep -rniE "not in \(\s*select" src/ migrations/` |
| No OFFSET on user facing lists | each justified | `grep -rniE "\boffset\b\|\.offset\(\|skip:" src/` |
| No await in loop over query results | none | `grep -rnE "for .* of .*\)\s*\{" -A3 src/ \| grep -E "await .*(find\|select\|query)"` then inspect |
| Slow query log on | enabled | `show log_min_duration_statement;` is not `-1`; `pg_stat_statements` installed |
