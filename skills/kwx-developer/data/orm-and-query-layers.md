# ORMs, query builders and raw SQL

Which data access layer to use in TypeScript and Rust, how to use it without N+1, injection or type lies, and how to audit one. Sources: Prisma docs (query optimization, raw queries, transactions), Drizzle and Kysely docs, sqlx README, Use The Index Luke, comparison write ups (treated as opinion).

## Contents

1. Choosing
2. Rules for any layer
3. Prisma
4. Drizzle
5. Kysely
6. sqlx (Rust), and Diesel / SeaORM
7. Supabase client (PostgREST)
8. Detecting N+1 and counting queries in tests
9. Auditing a codebase's data layer
10. Checks

## 1. Choosing

| Layer | Strength | Cost | Default when |
|---|---|---|---|
| Raw SQL with a thin driver (postgres.js, pg, better-sqlite3) | full SQL, no magic | types by hand unless generated | small services, heavy reporting SQL |
| Kysely | typed SQL builder, dynamic queries stay typed, no runtime engine | you write SQL shaped code; types generated from the DB (kysely-codegen) | SQL fluent team, complex dynamic filters |
| Drizzle | schema in TS, SQL shaped builder plus a relational query API, light runtime, edge friendly, drizzle-kit migrations | migration generator needs review; relational API has its own limits | default for new TypeScript projects |
| Prisma | most polished DX, schema file, generated client, Studio | own query engine semantics, N+1 via loops, raw SQL needed for many Postgres features (partial indexes historically, CTEs, locking reads, SKIP LOCKED) | existing Prisma projects: keep it, follow section 3 |
| sqlx (Rust) | SQL checked against a real schema at compile time, async | dynamic queries need `QueryBuilder` | default for Rust |
| Diesel (Rust) | fully typed DSL, sync (diesel-async exists) | heavier generics, slower compiles | team already on it |
| SeaORM (Rust) | ActiveRecord style, dynamic | runtime errors instead of compile time | rapid CRUD |

Do not switch an existing project's data layer as a side quest. Follow what the codebase uses; consistency across the repo beats the "better" tool in one folder.

## 2. Rules for any layer

1. **Parameters, never string building.** Every value goes in as a bind parameter. Identifiers (column names for sorting) come from an allowlist map, never from the request.
   ```ts
   // bad
   db.execute(sql.raw(`select * from users where email = '${email}'`));
   // good
   db.execute(sql`select * from users where email = ${email}`);
   // dynamic sort: allowlist
   const sortCols = { created: posts.createdAt, title: posts.title } as const;
   const col = sortCols[req.query.sort as keyof typeof sortCols] ?? posts.createdAt;
   ```
   The unsafe escape hatches to grep for: Prisma `$queryRawUnsafe` / `$executeRawUnsafe`, Drizzle and Kysely `sql.raw(`, `sql.identifier` with user input, knex `.raw(` with string concatenation, sqlx `query(&format!(...))`.
2. **Select the columns you need** in list queries. `select *` / default "all fields" ships password hashes and large blobs into memory and logs, and blocks index only scans.
3. **No query inside a loop.** Use joins, `IN (...)`, relational includes or a dataloader. See section 8.
4. **One place per entity writes it.** Business writes to `orders` go through one module (`orders/repo.ts` or `orders/service.ts`), so invariants and side effects live in one place. Do not wrap the ORM in a generic `Repository<T>` with `findById`/`save`: it hides the query layer's features and adds nothing.
5. **Types come from the database schema**, not hand written interfaces that can drift: Drizzle schema, Prisma generate, kysely-codegen, `supabase gen types typescript`, sqlx macros. CI regenerates and fails on a diff.
6. **Transactions are explicit and passed down** (`tx` parameter). A function that may be called inside a transaction takes the executor as an argument.
7. **bigint and numeric stay exact.** Drivers return Postgres `bigint` and `numeric` as strings (pg) or `BigInt` for good reason; do not configure them to parse as JS `number` unless ids and amounts are guaranteed below 2^53.
8. **Map constraint errors** (unique, FK, check) to domain errors in the data layer, once, not in every handler.
9. **Migrations are SQL files in the repo**, generated or hand written, read before merge, linted with Squawk (see `migrations.md`).
10. **Timeouts on every pool**: connect timeout, statement timeout, and for Prisma the interactive transaction `timeout` (default 5 s) and `maxWait` (default 2 s).

## 3. Prisma

- N+1: a loop of `findUnique` calls in the same tick is batched by Prisma's dataloader; `findMany` in a loop is not. Use `include` / `select` with relations (2 queries) or `relationLoadStrategy: 'join'` (1 query, Postgres and MySQL; check its filter limitations).
- Logging to catch N+1: `new PrismaClient({ log: [{ emit: 'event', level: 'query' }] })` and count `query` events in tests.
- Unique violation is `PrismaClientKnownRequestError` with `code === 'P2002'`; FK is `P2003`; record not found on update/delete is `P2025`.
- Raw SQL: use the tagged template `prisma.$queryRaw\`... ${value}\`` (parameterized) or TypedSQL (`.sql` files with generated types). Never `$queryRawUnsafe` with interpolated input.
- Atomic updates: `update({ data: { stock: { decrement: 1 } }, where: { id, stock: { gt: 0 } } })` instead of read then write. For `FOR UPDATE` or `SKIP LOCKED`, use `$queryRaw` inside `$transaction`.
- Interactive transactions (`$transaction(async tx => ...)`) hold a connection; never call outside services inside. Use `tx`, not `prisma`, inside the callback (using `prisma` silently runs outside the transaction).
- Serverless: use the Prisma driver adapters or Accelerate / a pooler; a client per invocation exhausts connections.
- `prisma db push` is for prototypes. `prisma migrate dev` generates SQL in `prisma/migrations/`; read it. A rename in schema.prisma becomes drop plus add unless you edit the SQL.

## 4. Drizzle

- Two APIs: the SQL shaped builder (`db.select().from(t).where(...)`) and the relational API (`db.query.users.findMany({ with: { posts: true } })`), which loads relations in one query. Use the relational API or a join for nested data, not a loop.
- `sql\`...\`` templates are parameterized; `sql.raw()` is not. Grep for `sql.raw(`.
- `logger: true` (or a custom `Logger`) logs every statement; use a counting logger in tests.
- drizzle-kit: `generate` writes SQL migrations to review; `migrate` applies them; `push` is for prototypes. Review renames (it asks interactively; in CI it cannot).
- Postgres error codes come through on `error.cause.code` or `error.code` depending on the driver (postgres.js vs node-postgres); centralize the mapping.
- Use `$type<...>()` on jsonb columns plus runtime validation (zod) at the boundary: the type is a promise, not a check.

## 5. Kysely

- Generate the `DB` interface from the live schema with kysely-codegen (or from Prisma/Drizzle schema), commit it, and regenerate in CI.
- Conditional filters stay typed: `let q = db.selectFrom('orders').selectAll(); if (status) q = q.where('status', '=', status);` This is the right way to avoid "smart logic" `OR $1 IS NULL` queries.
- `sql\`\`` is parameterized; `sql.raw` and `sql.ref`/`sql.id` with user input are injection risks; allowlist identifiers.
- `jsonArrayFrom` / `jsonObjectFrom` helpers (Postgres) load nested relations in one query.
- Transactions: `db.transaction().execute(async trx => ...)`, pass `trx` down.

## 6. sqlx (Rust)

- Use `query!` / `query_as!` macros: SQL is checked against the database schema at compile time, including column types and nullability. Commit the `.sqlx` directory from `cargo sqlx prepare` and build CI with `SQLX_OFFLINE=true`, so builds do not need a live database. CI also runs `cargo sqlx prepare --check` to catch stale metadata.
- Nullability overrides: `select count(*) as "count!"` forces non null; `"col?"` forces Option. Use them deliberately, they bypass the check.
- Dynamic queries: `QueryBuilder` with `push_bind` for values; never `format!` values into SQL.
  ```rust
  let mut qb = sqlx::QueryBuilder::new("select id, title from posts where team_id = ");
  qb.push_bind(team_id);
  if let Some(s) = status { qb.push(" and status = ").push_bind(s); }
  qb.push(" order by created_at desc, id desc limit ").push_bind(limit);
  let rows = qb.build_query_as::<Post>().fetch_all(&pool).await?;
  ```
- Transactions: `let mut tx = pool.begin().await?; ... tx.commit().await?;` A dropped `tx` rolls back, so an early `?` return is safe.
- Map `sqlx::Error::Database(e)` with `e.code()` (`"23505"`) or `e.is_unique_violation()` to domain errors.
- Money: `rust_decimal::Decimal` for numeric, `i64` for minor units, never `f64`. Time: `time::OffsetDateTime` or `chrono::DateTime<Utc>` for timestamptz.
- Diesel: `diesel print-schema` keeps `schema.rs` in sync; `belonging_to` plus `grouped_by` loads children for many parents in one query (its N+1 fix).

## 7. Supabase client (PostgREST)

- Every `supabase.from(...)` call from a browser runs as the user under RLS; RLS is the authorization layer. Add the explicit filter too (`.eq('user_id', userId)`): it lets Postgres use the index instead of relying on the policy alone.
- Nested selects (`select('id, title, author:profiles(name)')`) load relations in one request; do not loop `from('profiles')` per row.
- Multi step writes that must be atomic do not belong in several client calls (each is its own transaction). Put them in a Postgres function and call `rpc()`.
- `supabase gen types typescript --linked > src/db/types.ts` in CI; fail on diff.
- The service role key bypasses RLS: server only, never in a bundle (grep the built output for `service_role`).

## 8. Detecting N+1 and counting queries in tests

The test that catches N+1: call a list endpoint with 1 item and with 20 items; the query count must be equal.

```ts
// Drizzle example; same idea with Prisma query events or a pg Pool wrapper
let queries = 0;
const db = drizzle(pool, { logger: { logQuery: () => { queries++; } } });

test('feed query count does not grow with rows', async () => {
  await seedPosts(1);  queries = 0; await getFeed(db); const one = queries;
  await seedPosts(20); queries = 0; await getFeed(db); const many = queries;
  expect(many).toBe(one);
});
```

- In production: `pg_stat_statements` sorted by `calls` shows the per row query with a call count far above request count.
- GraphQL: every resolver that loads by id goes through a per request DataLoader.

## 9. Auditing a codebase's data layer

Look for inconsistency as much as bugs:

1. More than one data access library for the same database (Prisma in one service folder, raw `pg` in another, Supabase client in a third). Pick the dominant one; list the rest as migration debt.
2. Queries scattered in route handlers and components vs a data module. Count `grep -rlE "from\(['\"]\w+['\"]\)|prisma\.\w+\.|db\.select|db\.query" src/` by folder.
3. Two shapes of the same entity type (hand written `User` interface plus generated type).
4. Unsafe raw SQL hits (section 2 rule 1 grep list).
5. Loops containing `await` on a query (section 8).
6. Transactions that call `fetch`, SDK clients or queue publishers.
7. Error handling for constraint codes duplicated per handler, or missing (500s on duplicate email).
8. Migrations not in the repo, or schema drift between repo and production.

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| No unsafe raw SQL | none, or input is allowlisted | `grep -rnE "queryRawUnsafe\|executeRawUnsafe\|sql\.raw\(\|\.raw\(\`\|format!\(\"(select\|insert\|update\|delete)" -i src/` |
| No N+1 | query count equal for 1 and 20 rows | query counting test (section 8) |
| Generated types fresh | no diff | regenerate in CI (`prisma generate`, `kysely-codegen`, `supabase gen types`, `cargo sqlx prepare --check`) then `git diff --exit-code` |
| One data layer per database | one library | `grep -rlE "@prisma/client\|drizzle-orm\|kysely\|from 'pg'\|postgres\(\|@supabase/supabase-js" src/ \| sort` |
| tx used inside transactions | no global client inside a transaction callback | read each `$transaction(` / `transaction(` block for `prisma.` / `db.` instead of `tx.` |
| No float money in code | none | `grep -rnE "parseFloat\(.*(amount\|price\|total)\|f64.*(amount\|price\|cents)" src/` |
| service role key not in client bundle | none | `grep -rn "service_role" dist/ build/ .next/static/` |
| sqlx offline data committed | `.sqlx/` present and checked | `ls .sqlx && SQLX_OFFLINE=true cargo check` |
