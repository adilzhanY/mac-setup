# Test data and fixtures

How to build the data a test needs so that the test is readable, independent and realistic: fixture strategies, builders, object mothers and factories, seeded random data, realistic edge data, rules for production data, cleanup and isolation. kwx-developer covers the basics (a factory with overrides, unique emails, fixed clock, `#[sqlx::test]`, Postgres isolation options) in `~/.claude/skills/kwx-developer/reliability/testing-strategy.md` sections 5 and 7; this file goes further and adds the patterns behind them.

## Contents

1. Vocabulary: fixture, setup, teardown
2. Fixture strategies
3. Smells: Mystery Guest, General Fixture, Irrelevant Information
4. Builders, object mothers and factories
5. Database factories
6. Seeded random data
7. Realistic data: what real users type
8. Reserved and fictional values
9. Production data rules
10. Cleanup and isolation
11. Fixture files
12. Checks

## 1. Vocabulary: fixture, setup, teardown

A test fixture is everything that must be in place before the test acts: objects, rows, files, a clock time, a signed in user (Meszaros). Setup builds it; teardown removes what outlives the test (rows, files, processes). In memory fixtures disappear by themselves; persistent ones (a database, the disk, a local Supabase) do not.

## 2. Fixture strategies

From xUnit Test Patterns, in order of preference:

| Strategy | What | Use when | Risk |
|---|---|---|---|
| Fresh transient fixture | Each test builds its own in memory data | Default for small tests | None |
| Fresh persistent fixture | Each test creates its own rows or files and they are made private (unique ids, own database, rollback) | Medium tests against a real database | Leftovers if teardown fails; collisions if ids are not unique |
| Immutable shared fixture | Reference data built once and never changed by any test (country list, plan catalogue) | Setup is slow and the data is read only | A test that writes to it breaks the others |
| Mutable shared fixture | Data built once and changed by tests | Avoid | Interacting tests, order dependence, "test run wars" when two runs share a database |

Meszaros: a fresh fixture "prevents Erratic Tests" and makes tests readable as documentation. If fresh fixtures are too slow, try an immutable shared fixture before a mutable one. Luo et al. (2014) found that 74% of order dependent flaky tests were fixed by cleaning shared state, which is what fresh fixtures avoid in the first place.

## 3. Smells: Mystery Guest, General Fixture, Irrelevant Information

These are causes of Meszaros' "Obscure Test":

- **Mystery Guest:** the test depends on data you cannot see in the test: a row with a literal id that some seed script created, a file in `fixtures/` whose content decides the result. The reader cannot connect cause and effect. Fix: build the data inline with a builder; if a file is needed, give it a name that says what is special about it.
- **General Fixture:** one big setup serves many tests, and each test uses a little of it. Nobody knows which parts matter, and changing it breaks unrelated tests (a fragile fixture). Fix: minimal fixture per test.
- **Irrelevant Information:** the test shows every field of every object, so the one value that matters is lost. Fix: defaults in a builder; override only what the test is about.

The test should show the values that matter, and only those.

## 4. Builders, object mothers and factories

| Pattern | What | Strength | Weakness |
|---|---|---|---|
| Object Mother (Thoughtworks, named by Fowler) | Named factory methods returning ready objects: `aTrialUser()`, `anExpiredSubscription()` | Readable personas the team shares | Grows a new method for every variation; becomes bloated (Pryce) |
| Test Data Builder (Nat Pryce) | An object with safe defaults for every field and chainable `with...` methods | Any variation inline, tests isolated from structure they do not care about | More code per type in languages without spread or struct update |
| Factory function with overrides (TS idiom) | `buildUser({ plan: "pro" })` returning defaults merged with overrides | Short, typed | Nested overrides get awkward without deep merge |

Combine them: builders or factory functions underneath, a few mother functions on top for the personas that recur across many tests.

### TypeScript

```ts
let seq = 0;
const next = () => ++seq;

export function buildUser(o: Partial<User> = {}): User {
  const n = next();
  return {
    id: `user-${n}`,
    email: `user${n}@example.test`,
    displayName: `Test User ${n}`,
    plan: "free",
    locale: "en",
    createdAt: new Date("2026-01-15T10:00:00Z"),
    ...o,
  };
}

// Mothers built on the factory, for recurring personas only.
export const aStudent = (o: Partial<User> = {}) => buildUser({ plan: "yearly", isStudent: true, ...o });
export const aLifetimeOwner = (o: Partial<User> = {}) => buildUser({ plan: "lifetime", ...o });
```

`fishery` (npm) adds sequences, associations and `create` hooks if hand written factories get repetitive. Do not add it for three types.

### Rust

```rust
impl Workout {
    /// Test default: a valid 30 minute workout. Override with struct update syntax.
    pub fn test_default() -> Self {
        Self { id: Uuid::nil(), title: "Morning run".into(), seconds: 1800, started_at: fixed_now() }
    }
}

let w = Workout { seconds: 0, ..Workout::test_default() }; // only `seconds` matters here
```

Keep `test_default` in a `#[cfg(test)]` module or a `test-support` crate so it never reaches production. For deeper graphs, write a small builder struct with `with_*` methods.

### Kotlin

Data classes with default arguments are builders already: `fun aWorkout(seconds: Int = 1800, title: String = "Morning run") = Workout(...)`, then `aWorkout(seconds = 0)`.

## 5. Database factories

For medium tests, factories insert rows and return them. Rules:

- **Insert through the same path production uses** where it matters (the repository, the API, or for Supabase the signed in client so RLS applies), and through direct SQL or the service role only for setup that is not under test.
- **Return the created entity** so the test uses its real id: `const w = await insertWorkout(db, { userId: u.id })`.
- **Unique values for every unique column** (email, username, slug), from a sequence or a UUID, so parallel tests never collide.
- **One factory per table,** defaults that satisfy every constraint, foreign keys created on demand (`insertWorkout` creates a user if none is given).
- **Supabase auth users:** create a fresh user per test with the admin API (`supabase.auth.admin.createUser({ email, password, email_confirm: true })`) using the local service role key, then sign in with the anon client as that user. Two users per RLS test: the owner and a stranger.

## 6. Seeded random data

Random data finds cases you did not think of, but a failure you cannot reproduce is worth little. So:

- **Seed every random source and print the seed on failure.** Property libraries do this for you (fast-check prints `seed` and `path`; Hypothesis keeps a database of failing examples; proptest writes `proptest-regressions/`).
- **Faker:** `faker.seed(42)` makes the sequence repeatable. Verified with `@faker-js/faker` 10.6.0: two runs with the same seed give the same name and email. Faker emails use real looking public domains (`...@gmail.com` in the verified run), so pass a reserved domain: `faker.internet.email({ provider: "example.test" })` (verified). For dates, fix the reference date: `faker.setDefaultRefDate("2026-01-01T00:00:00Z")`.
- **Seed per test, not per file,** so adding a test does not change the data of the tests after it.
- **Random is for discovery, literals are for meaning.** If a value decides the outcome, write it as a literal in the test. Random filler for the rest is fine.
- **When random data finds a bug,** copy the minimal failing value into a plain example test as a permanent regression.

## 7. Realistic data: what real users type

Tests with only `"John"` and `"test@test.com"` miss what production sees. Keep a shared list of realistic values in the test support module and use it in builders and property generators. The exploratory folder's edge case catalogue has the long list; the ones that break the owner's kinds of apps most often:

- Names: `O'Brien` (apostrophe), `Zoë` (combining or precomposed), `Ásgeir`, `李小龍`, `Әйгерім` (Kazakh letters ә ө ү ң), a 60 character name, a single letter name, a name with an emoji, right to left text (`مريم`).
- Text fields: leading and trailing spaces, only spaces, a newline pasted from a notes app, 10 000 characters, SQL and HTML special characters (`'; drop table`, `<b>`), zero width characters.
- Numbers and money: 0, negative, very large, values that do not round evenly (`0.1 + 0.2`), currencies with no minor unit (JPY) or three (KWD), comma as decimal separator in German or Russian locales.
- Time: `2026-03-29` and `2026-10-25` (EU DST changes), `2028-02-29`, 23:59:59 and 00:00:00, users in UTC+5 (Almaty) and UTC-10, a workout that starts before midnight and ends after it.
- Collections: empty, one, exactly a page size, page size plus one, thousands.
- Files: empty file, huge file, wrong extension, name with spaces and Cyrillic characters, file that disappears while being read.

The Big List of Naughty Strings (github.com/minimaxir/big-list-of-naughty-strings) is a ready source for string inputs.

## 8. Reserved and fictional values

Test data leaks: into logs, error reports, screenshots, emails sent by mistake. Use values that can never reach a real person:

- Domains: `example.com`, `example.org`, `example.net` (RFC 2606) and the `.test`, `.example`, `.invalid` top level domains (RFC 2606, RFC 6761). Prefer `@example.test`.
- Phone numbers: ranges reserved for drama and testing, such as UK `07700 900000` to `07700 900999` (Ofcom). Do not invent numbers that might be real.
- Payment cards: the provider's documented test numbers (Stripe `4242 4242 4242 4242`, and its decline test cards). Never a real card.
- People: obviously fictional names in fixtures that might be shown to others; no real persons, no celebrities in fixtures that end up in screenshots.

## 9. Production data rules

- **Do not copy production personal data into development, test, CI, fixtures or an agent's context.** Not "just for one bug". Under the GDPR, pseudonymised data (names replaced by ids, but re identifiable) is still personal data; only data that is truly anonymous falls outside it (GDPR Recital 26).
- **Prefer synthetic data shaped like production.** To reproduce a production bug, extract the shape (field lengths, counts, the odd character, the time zone), not the values, and rebuild it with factories.
- **If real data is unavoidable** (a migration rehearsal on a copy), the owner decides, the copy stays in a protected environment, it is masked before it reaches anyone else (emails replaced with `user<n>@example.test`, names and free text replaced, ids kept for joins), and it is deleted after use.
- **Secrets are not test data.** No real API keys, tokens or cookies in fixtures; use the provider's test mode keys from environment variables, never committed.
- **Logs and snapshots** of tests must not contain real personal data either; check recorded HTTP fixtures (cassettes) for tokens and emails before committing.

## 10. Cleanup and isolation

Isolation beats cleanup: a test that cannot see other tests' data needs no cleanup to be correct.

Order of preference for persistent fixtures:

1. **Nothing to clean:** in memory, or temp dirs created per test (`fs.mkdtemp`, `tempfile::tempdir()`), removed automatically.
2. **Rollback:** each test runs in a transaction rolled back at the end (fast; does not work when the code under test opens its own connections or commits on purpose).
3. **Database per test:** created from a migrated template (`#[sqlx::test]` does this in Rust).
4. **Unique data per test in a shared database:** unique user per test, every query scoped to that user. This is the practical choice for local Supabase, where auth users and RLS make per test databases awkward. Reset the whole local database between full runs with `supabase db reset` (re-applies migrations and `supabase/seed.sql`, from the Supabase CLI docs).
5. **Explicit teardown** in `afterEach` or a Rust `Drop` guard, written so it runs even when the test fails, and failing loudly if it cannot clean (Fowler: make teardown failures visible).

Other shared state to reset: environment variables (`vi.stubEnv` with `unstubAllEnvs: true`), module singletons (`vi.resetModules()`), global fetch handlers (`server.resetHandlers()` in MSW), fake timers (`vi.useRealTimers()`), the current directory, `localStorage` and `AsyncStorage`, the file system cache of a desktop app (`XDG_CONFIG_HOME` pointed at a temp dir).

Check: the suite passes in shuffled order and when one test runs alone. A test that passes alone and fails in the suite (or the reverse) has a shared state problem (`flaky-tests.md`).

## 11. Fixture files

- Put them in `tests/fixtures/` (or next to the test), named by what is special: `gpx-with-missing-timestamps.gpx`, not `test2.gpx`.
- Keep them small: the smallest file that shows the behaviour. A 5 MB fixture is a Mystery Guest.
- Generated fixtures come with the script that generates them, committed together, so they can be rebuilt.
- Load paths relative to the project, not the current directory (`env!("CARGO_MANIFEST_DIR")` in Rust, `new URL("./fixtures/x.json", import.meta.url)` in ESM).
- Recorded HTTP responses are fixtures too: scrub tokens and personal data, and validate them against the API schema (`test-doubles.md` section 7).

## 12. Checks

| Check | Pass condition |
|---|---|
| Fresh fixtures | Each test builds its own data; no mutable shared fixture |
| No Mystery Guest | Values that decide the outcome are visible in the test |
| Minimal data | Builders with defaults; tests override only what they are about |
| Unique values | Unique columns get sequence or UUID values; parallel runs never collide |
| Seeds | Random data is seeded and the seed is printed on failure; found bugs become literal regression tests |
| Realistic values | Builders and generators include Unicode, long, empty and time zone edge values |
| Reserved values | Emails on `example.test` or RFC 2606 domains, test card numbers, fictional phone ranges |
| No production personal data | No real emails, names, tokens or cookies in fixtures, cassettes, snapshots or logs |
| Isolation | Suite passes shuffled and each test passes alone; teardown runs on failure and fails loudly |
| Fixture files | Small, named by content, generated ones come with their script |
