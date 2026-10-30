# Schema design

Rules for tables, keys and types that models get wrong by default. Postgres first, SQLite notes where they differ.

## Contents

1. Normal forms in practice
2. Keys: surrogate vs natural, bigint vs UUIDv7
3. Types: time, money, text, booleans, enums
4. JSONB vs columns
5. Generated columns
6. Constraints that belong in every schema
7. Soft delete trade offs
8. Multi tenant tables
9. Naming
10. Checks

## 1. Normal forms in practice

- Default to third normal form: every non-key column depends on the key, the whole key and nothing but the key. Duplicate data only on purpose, with the mechanism that keeps it in sync written down (trigger, generated column, or the single function that writes both).
- A denormalized counter (`posts.comment_count`) is fine when it is updated in the same transaction as the source row, with `SET comment_count = comment_count + 1`. It is a bug when it is computed in app code from a stale read.
- Snapshot data is not denormalization. An order line stores the `unit_price` at purchase time, because the product price will change. Copy it, do not join to `products.price`.
- Never store a list in a delimited string (`tags = 'a,b,c'`). Use a join table, or a `text[]` / `jsonb` array only when you never join on the elements.
- One fact, one place. If two columns can disagree (`is_active` and `deactivated_at`), drop one and derive it, or add a CHECK that ties them: `CHECK ((deactivated_at IS NULL) = is_active)`.

## 2. Keys

### Surrogate vs natural

- Use a surrogate primary key for entities. Natural keys (email, username, ISBN, country code for a user's country) change, get reused, or arrive malformed. Keep the natural key as a `UNIQUE` constraint so the database still rejects duplicates.
- Natural keys are fine as the primary key for stable code tables (ISO 4217 currency codes, ISO 3166 country codes) and for join tables: `PRIMARY KEY (user_id, group_id)`.
- Email uniqueness: `CREATE UNIQUE INDEX users_email_key ON users (lower(email));` or a `citext` column. A plain `UNIQUE (email)` lets `Bob@x.com` and `bob@x.com` both in.

### bigint vs UUIDv7 vs UUIDv4

| Key | Size | Insert locality | Use when |
|---|---|---|---|
| `bigint generated always as identity` | 8 bytes | append only | default; one database mints all ids |
| UUIDv7 (`uuidv7()` in PG 18, a library elsewhere) | 16 bytes | append only (time ordered prefix) | ids minted on clients (offline apps), merged across databases, or must exist before the insert |
| UUIDv4 (`gen_random_uuid()`) | 16 bytes | random, splits B-tree pages | never as a primary key on a large hot table; fine as an unguessable token column |

- Random UUIDv4 keys scatter inserts across the whole index, causing page splits and cache misses; credativ measured an ordered scan over a UUIDv7 key about 3 times faster with about 100 times fewer buffer hits than over UUIDv4 on 1M rows. UUIDv7 inserts land within roughly 15% of bigint in published tests.
- UUIDv7 leaks creation time to anyone who sees the id. If that matters (user signup dates), expose a separate random public id.
- Sequential bigint ids leak volume (order 1042 means about 1000 orders). For public URLs of business objects use a second column `public_id` (UUIDv7, UUIDv4, or a short random token) with a unique index, and keep bigint internally.
- `serial` is legacy. Use `generated always as identity`; it blocks accidental manual inserts into the key and has cleaner ownership and permissions.
- Use `bigint` for every id and every counter that can grow. An `int` key overflows at 2.1 billion, and the type change on a large table is a full rewrite. Squawk flags this (`prefer-bigint-over-int`).

```sql
-- good
create table orders (
  id         bigint generated always as identity primary key,
  public_id  uuid not null default uuidv7() unique,
  user_id    bigint not null references users(id),
  created_at timestamptz not null default now()
);
-- bad: serial, int, random uuid primary key, nullable foreign key
create table orders (id serial primary key, uid uuid default gen_random_uuid(), user_id int references users);
```

## 3. Types

### Time

- An instant (created_at, paid_at, expires_at) is `timestamptz`. Postgres stores it as UTC and converts on output using the session `TimeZone`. Set the session time zone to UTC in the app connection so serialized values are predictable.
- Do not put a precision on timestamps (`timestamptz(0)`): Postgres rounds, so a stored `now()` can be up to half a second in the future.
- A calendar day (birthday, due date, a daily habit row) is `date`, not a timestamp at midnight. A midnight timestamp shifts a day when read in another zone.
- A future local event (a 09:00 meeting in Berlin next March) is stored as local wall time plus the IANA zone name (`'Europe/Berlin'`), and converted to an instant when needed. Zone rules change after you store the row; an instant stored today can end up an hour off.
- Range queries use half open intervals: `created_at >= $start AND created_at < $end`. Never `BETWEEN` with timestamps (it includes both ends, so midnight rows land in two days).
- Store durations as `interval` or as integer seconds or milliseconds with the unit in the column name (`duration_ms`).
- SQLite has no time type. Store instants as INTEGER unix milliseconds (sortable, compact) or TEXT ISO 8601 with `Z`. Pick one per database and never mix.

### Money

- Integer minor units (`amount_cents bigint`) plus a currency column, or `numeric(20, 6)` when you need fractions of a minor unit (FX rates, per unit cloud pricing). Not every currency has 2 decimals: JPY has 0, KWD has 3. Keep a currency table with its exponent.
- Never `float`/`double`/`real` (0.1 + 0.2 is not 0.3) and never Postgres `money` (no currency, depends on `lc_monetary`, no fractions of a cent).
- In JavaScript, amounts above 2^53 lose precision as `number`. Drivers return `bigint` and `numeric` as strings for that reason. Keep them as strings or `BigInt` until the edge; do not `parseFloat` them.
- Round once, at a defined step, with a stated rule (banker's rounding or half up), and store the rounded result. Allocate remainders explicitly when splitting (3 people paying 10.00: 3.34, 3.33, 3.33).

### Text

- `text` everywhere. Add `CHECK (char_length(name) <= 200)` when a real limit exists. `varchar(n)` gives no speed benefit in Postgres and its limit is changed with a type change. Never `char(n)`: it pads with spaces.
- Normalize before storing anything you compare: trim, lower case emails, Unicode NFC.

### Booleans and states

- A boolean that will grow a third value becomes a `status` text column now. `is_draft` plus `is_published` plus `is_archived` is three booleans that can contradict each other; one `status` column with a CHECK cannot.
- Record when a state changed, not only the state: `published_at timestamptz` beats `is_published boolean` because it answers "since when" for free.

### Enums

- Postgres enum: values can be added (`ALTER TYPE ... ADD VALUE`) and renamed, never dropped; removing a value means recreating the type and rewriting every column that uses it. Inside a transaction block the new value cannot be used until commit. Use a Postgres enum only for sets that never shrink.
- Default to `text` plus a CHECK constraint, or a lookup table with a foreign key when the set needs metadata (label, sort order, is_active). Changing a CHECK is cheap: add the new one NOT VALID, validate, drop the old.
- In SQLite use `TEXT` with `CHECK (status IN (...))`.

## 4. JSONB vs columns

- Use `jsonb`, never `json`, unless you must keep key order or duplicate keys. `json` has no equality operator, which breaks `SELECT DISTINCT` and GROUP BY.
- Make it a real column when you filter, join, sort, aggregate, constrain or foreign-key on it, or when every row has it. The planner keeps no statistics on keys inside a `jsonb` value, so estimates on `doc->>'status' = 'x'` are guesses, and you lose NOT NULL, foreign keys and type checks.
- Keep `jsonb` for data you store and return whole: provider webhooks, user preferences blobs, an audit snapshot, sparse attributes that differ per row.
- Indexing: a GIN index with `jsonb_path_ops` is smaller and faster for `@>` containment; default `jsonb_ops` also supports key existence (`?`). For one hot key, use an expression B-tree index instead: `CREATE INDEX ON events ((payload->>'user_id'));` and query with the same expression.
- Any update rewrites the whole document and locks the whole row. Keep documents small; a growing array in a jsonb column (comments, events) belongs in a child table.
- Validate shape at the boundary (zod, serde) and, for critical keys, with a CHECK: `CHECK (jsonb_typeof(settings->'theme') = 'string')`.

## 5. Generated columns

- Use a generated column for a value derived from the same row (full name for search, `lower(email)`, a tsvector, a total). It cannot drift, unlike a value maintained by app code.
- PG 18: virtual is the default (computed on read, no storage); add `STORED` when reads are frequent and the expression is expensive, or when the column must be indexed directly or replicated. Expressions may use only immutable functions and the current row.
- Adding a STORED generated column to an existing table rewrites the table. Adding a virtual one does not.
- SQLite supports `GENERATED ALWAYS AS (...) VIRTUAL|STORED` since 3.31; only VIRTUAL can be added with ALTER TABLE.

## 6. Constraints in every schema

- `NOT NULL` on every column that has no real "unknown" state.
- `REFERENCES` on every column that points at another row, with an explicit `ON DELETE`: `CASCADE` for owned children (order lines), `RESTRICT` for things that must not vanish under you (an invoice's customer), `SET NULL (col)` for optional links. Default `NO ACTION` is fine but say which you meant.
- `CHECK` for ranges and shapes: `CHECK (quantity > 0)`, `CHECK (ends_at > starts_at)`, `CHECK (email ~ '^[^@]+@[^@]+$')` (loose on purpose).
- `UNIQUE` for every business uniqueness rule, including composite ones (`UNIQUE (team_id, slug)`). Nullable columns in a unique constraint allow many NULLs by default; use `NULLS NOT DISTINCT` (PG 15+) when one NULL is the limit.
- `EXCLUDE USING gist` for "no overlapping bookings": `EXCLUDE USING gist (room_id WITH =, tstzrange(starts_at, ends_at) WITH &&)` (needs `btree_gist`).
- CHECK constraints cannot reference other rows or tables in Postgres. Cross-row rules go in UNIQUE, EXCLUDE, FOREIGN KEY, or a trigger.

## 7. Soft delete trade offs

`deleted_at timestamptz` looks cheap and costs a lot:

- Every query needs `AND deleted_at IS NULL`; one forgotten clause leaks deleted data (often to the user who deleted it, or to an export).
- Foreign keys stop protecting you: a "deleted" customer still satisfies `invoices.customer_id`.
- Unique constraints break: a deleted user's email blocks a new signup. You need partial unique indexes: `CREATE UNIQUE INDEX ON users (lower(email)) WHERE deleted_at IS NULL;`
- Data protection law (GDPR erasure) still requires a real delete later, so you build the hard delete anyway.
- Brandur (Heroku, Stripe) reports nobody used soft delete to undelete in over ten years.

Default: hard delete, and copy the row into an archive table in the same statement.

```sql
create table deleted_record (
  id             bigint generated always as identity primary key,
  deleted_at     timestamptz not null default now(),
  original_table text not null,
  original_id    text not null,
  data           jsonb not null
);

with d as (delete from customer where id = $1 returning *)
insert into deleted_record (original_table, original_id, data)
select 'customer', id::text, to_jsonb(d.*) from d;

-- retention
delete from deleted_record where deleted_at < now() - interval '90 days';
```

Use `deleted_at` only for a user facing trash with restore. Then: a partial unique index for every unique rule, a view (`active_customers`) or ORM default scope that every read goes through, and a scheduled job that hard deletes after the retention period.

## 8. Multi tenant tables

- Put `tenant_id` (or `team_id`) on every tenant owned table, including child tables, so every query and every index can lead with it. Composite foreign keys `(tenant_id, parent_id)` stop a row from pointing at another tenant's parent.
- Lead indexes with `tenant_id`: `(tenant_id, created_at)`.
- With Supabase or any Postgres exposed to clients: enable RLS on every table in an exposed schema, one policy per operation, `TO authenticated`, wrap `auth.uid()` as `(select auth.uid())` so it is evaluated once per statement, index every column a policy filters on, never authorize on `user_metadata` (users can edit it). Views bypass RLS unless created `with (security_invoker = true)` (PG 15+). The `service_role` key bypasses RLS and never ships to a client.

## 9. Naming

- `snake_case`, lower case, plural or singular table names but one convention per database. Never quoted mixed case identifiers (`"userId"`): every tool then needs quotes.
- Foreign key column: `<referenced_singular>_id` (`user_id`). Timestamps: `<verb>_at`. Booleans: `is_`/`has_`. Amounts: unit in the name (`amount_cents`, `duration_ms`, `size_bytes`).
- Name constraints and indexes explicitly (`orders_user_id_idx`, `orders_quantity_positive`) so migrations can drop them by name on every environment.

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| No `serial`, no `int` keys | none, or justified | `grep -rniE "\bserial\b\|\bint(eger)?\b\s+(primary\|references)" migrations/` |
| No random UUID primary keys on hot tables | none | `grep -rniE "uuid.*primary key.*(gen_random_uuid\|uuid_generate_v4)\|primary key.*default (gen_random_uuid\|uuid_generate_v4)" migrations/` |
| timestamptz for instants | none plain | `grep -rniE "\btimestamp\b" migrations/ \| grep -viE "timestamptz\|with time zone"` |
| No float or money for amounts | none | `grep -rniE "\b(real\|float\|double precision\|money)\b" migrations/` and inspect |
| No varchar(n) habit, no char(n) | each justified | `grep -rniE "varchar\(\|char\(\|character\(" migrations/` |
| json not used | none | `grep -rniE "\bjson\b" migrations/ \| grep -vi jsonb` |
| Unique email is case insensitive | lower() index or citext | `grep -rniE "unique.*email\|email.*unique" migrations/` |
| Soft delete has partial unique indexes | each unique on a soft deleted table has `WHERE deleted_at IS NULL` | `grep -rn "deleted_at" migrations/` then inspect uniques on those tables |
| Nullable columns justified | review list | `select table_name, column_name from information_schema.columns where table_schema='public' and is_nullable='YES' order by 1;` |
| RLS enabled (Supabase) | no rows | `select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where nspname='public' and relkind='r' and not relrowsecurity;` |
