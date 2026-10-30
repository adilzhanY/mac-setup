# Dates, time and money

Read when: code stores, computes, compares, serializes or displays money, prices, percentages of money, dates, times, durations, time zones or deadlines.

## Contents

1. Money: never floats
2. Money: representation, arithmetic, rounding, allocation
3. Money: storage, wire format, display
4. Time: pick the right kind of value
5. Time: `Date` pitfalls
6. Time: Temporal, and what to use until it is everywhere
7. Time: storage, wire format, display
8. Testing time
9. Checks

## 1. Money: never floats

`0.1 + 0.2 === 0.30000000000000004`. Binary floating point cannot represent most decimal fractions, so sums drift, comparisons fail, and rounding happens in the wrong place. No money value is ever a JavaScript `number` with a fractional part, and no money value is ever parsed with `parseFloat`.

## 2. Money: representation, arithmetic, rounding, allocation

- Represent an amount as an integer count of the currency's minor unit, plus the currency code, always together:

```ts
type Money = { readonly amountMinor: bigint; readonly currency: CurrencyCode }; // or number if amounts stay below 2^53
```

- Minor units differ per currency (ISO 4217 exponent): USD/EUR 2 (cents), JPY and KRW 0, KWD/BHD/JOD/OMR/TND 3. Never assume 100. Stripe-style APIs expect `1099` for 10.99 USD and `10` for 10 JPY; some currencies (ISK, UGX, HUF and TWD payouts) have provider-specific exceptions, so read the provider's currency table.
- `number` integers are exact up to `Number.MAX_SAFE_INTEGER` (about 9.007e15). That is 90 trillion dollars in cents, enough for most apps, but not for crypto amounts (18 decimals) or aggregated totals in high-inflation currencies. Use `bigint` there, or a decimal library.
- Never add amounts in different currencies. Make `add(a, b)` throw on mismatch.
- Multiplying by a rate (tax, discount, FX, interest) produces fractions. Do it in a decimal type (`decimal.js`, `big.js`, `dinero.js`, or scaled `bigint`), then round once, explicitly, with a named rounding mode, at the point the business rules say (per line or per invoice; this changes totals, so ask or follow the spec).
- Rounding mode is a business decision: half-up (`halfExpand`) is common for retail; banker's rounding (`halfEven`) is common in accounting and some tax rules. Name it in code.
- Splitting an amount must not lose or create minor units. 100 cents split three ways is 34 + 33 + 33, not 33.33 x 3:

```ts
function allocate(total: bigint, parts: number): bigint[] {
  const n = BigInt(parts);
  const base = total / n;                 // bigint division truncates toward zero
  const remainder = total - base * n;     // assumes total >= 0
  return Array.from({ length: parts }, (_, i) => (BigInt(i) < remainder ? base + 1n : base));
}
// allocate(100n, 3) -> [34n, 33n, 33n]; the sum is always the total
```

- Percentages and rates stored as decimals in strings or basis points (integer, 1 bp = 0.01 %), not floats.
- If the repo uses a money library (dinero.js, currency.js, a `Money` class), use it everywhere; mixing a library in one module with raw numbers in another is a finding.

## 3. Money: storage, wire format, display

- Database: integer/`BIGINT` minor units plus a currency column, or `NUMERIC(19,4)` (Postgres `numeric`) when sub-minor precision is needed. Never `FLOAT`/`REAL`/`DOUBLE`. Note that many Postgres drivers return `numeric` and `bigint` as strings; keep them strings until converted to your money type.
- JSON: integer minor units (`"amount": 1099, "currency": "USD"`) or a decimal string (`"amount": "10.99"`). Never a JSON float (`10.99`), because every consumer parses it into a binary float.
- Display with `Intl.NumberFormat` and the currency code; it knows the symbol, position, grouping and the currency's default fraction digits (JPY shows none). Create the formatter once and reuse it (construction is comparatively expensive):

```ts
const formatters = new Map<string, Intl.NumberFormat>();
export function formatMoney(m: Money, locale: string): string {
  const key = `${locale}|${m.currency}`;
  let f = formatters.get(key);
  if (!f) {
    f = new Intl.NumberFormat(locale, { style: "currency", currency: m.currency });
    formatters.set(key, f);
  }
  const digits = f.resolvedOptions().maximumFractionDigits ?? 2;
  // Convert minor units to a decimal string, so no float is ever created.
  const s = m.amountMinor.toString().padStart(digits + 1, "0");
  const decimal = digits === 0 ? s : `${s.slice(0, -digits)}.${s.slice(-digits)}`;
  return f.format(decimal as Intl.StringNumericLiteral);
}
```

`Intl.NumberFormat.prototype.format` accepts decimal strings and keeps their precision (ES2023 `Intl.NumberFormat` v3). The `-` sign is handled by `padStart` only for non-negative values; handle negatives explicitly if they occur.

- Never format money by string concatenation (`"$" + amount.toFixed(2)`): wrong for other locales and currencies, and `toFixed` rounds binary floats (`(1.005).toFixed(2) === "1.00"`).
- Parsing user-entered amounts: accept a constrained pattern (`/^\d{1,12}([.,]\d{1,3})?$/`), convert to minor units with string operations, and validate the fraction digits against the currency.

## 4. Time: pick the right kind of value

Most date bugs come from using one type for different concepts. Decide which of these you have:

| Concept | Example | Temporal type | Store as |
|---|---|---|---|
| Exact moment | order placed, log event, token expiry | `Temporal.Instant` | UTC timestamp (`timestamptz`, ISO with `Z`, epoch ms) |
| Moment in a place | meeting at 09:00 in Berlin | `Temporal.ZonedDateTime` | local date-time plus IANA zone (`2026-11-02T09:00[Europe/Berlin]`), or instant plus zone |
| Calendar date | birthday, holiday, due date, "valid until" a day | `Temporal.PlainDate` | `date` column, `"YYYY-MM-DD"` string |
| Wall-clock time | store opens at 08:00 every day | `Temporal.PlainTime` | `"HH:MM"` |
| Local date-time without zone | form input before the zone is known | `Temporal.PlainDateTime` | rarely stored |
| Length of time | 90 minutes, 3 months | `Temporal.Duration` | ISO 8601 duration `"PT1H30M"` or integer seconds |

Rules that follow:

- A birthday is not a moment. Storing it as a `Date` at UTC midnight shows the previous day to every user west of UTC.
- Future local events (a dentist appointment next year) are stored as local time plus zone, not as a UTC instant: time zone rules change (governments move DST), and the appointment stays at 09:00 local.
- Time zones are IANA names (`Europe/Berlin`), never fixed offsets (`+01:00`) or abbreviations (`CET`, `EST`), which do not encode DST.
- "Add one day" to a moment in a zone is not "add 24 hours": a DST day has 23 or 25 hours. Do calendar math in `ZonedDateTime` or `PlainDate`.
- Durations in months are calendar-dependent (Jan 31 plus 1 month). Define what the product means and test month ends.

## 5. Time: `Date` pitfalls

`Date` is a UTC instant with local-time getters. Known traps:

- `new Date("2026-10-30")` (date only) parses as UTC midnight; `new Date("2026-10-30T00:00")` (no offset) parses as local midnight. Same-looking strings, different instants.
- Non-ISO strings (`"10/30/2026"`, `"Oct 30 2026"`) parse in implementation-defined ways. Never pass them to `new Date()`.
- Months are 0-based in the constructor and `getMonth()`: `new Date(2026, 0, 15)` is January.
- Setters mutate in place; a `Date` passed to a function can be changed by it.
- `getTimezoneOffset()` is the device zone at that instant; it says nothing about the user's intended zone.
- Comparing with `===` compares object identity. Compare `a.getTime() === b.getTime()`.
- `Date.now()` and `new Date()` in business logic make code untestable; inject a clock (section 8).
- An invalid date does not throw: `new Date("nope").getTime()` is `NaN`. Check `Number.isNaN(d.getTime())` after any parse.

## 6. Time: Temporal, and what to use until it is everywhere

Temporal is TC39 Stage 4 and immutable, zone-aware and explicit. Availability as of late 2026: Firefox 139+, Chrome/Edge 144+, Node 26 (enabled by default); Safari has not shipped it. TypeScript 6.0+ includes the types (`"lib": ["esnext"]` or `"esnext.temporal"`).

- Node 26+ servers: use `Temporal` directly.
- Browsers and older Node: use the polyfill (`@js-temporal/polyfill` from the champions, or the smaller `temporal-polyfill`) and import `Temporal` from it explicitly, so code works the same everywhere and the import can be removed later.
- Existing code on date-fns, Luxon or Day.js: keep the repo's library; do not add a second date library. Moment.js is in maintenance mode: do not add it to new code; replace it when touching it heavily.
- Never mix two date libraries in one module.

```ts
import { Temporal } from "temporal-polyfill"; // drop once all targets ship Temporal

const due = Temporal.PlainDate.from("2026-12-31");
const daysLeft = Temporal.Now.plainDateISO("Europe/Berlin").until(due, { largestUnit: "days" }).days;

const meeting = Temporal.ZonedDateTime.from("2026-03-28T09:00[Europe/Berlin]");
meeting.add({ days: 1 });   // 2026-03-29T09:00, same wall-clock time
meeting.add({ hours: 24 }); // 2026-03-29T10:00, because clocks jump forward that night
```

## 7. Time: storage, wire format, display

- Database: `timestamptz` (Postgres) for instants. `timestamp without time zone` only for genuinely local values with the zone in another column. `date` for calendar dates.
- JSON: ISO 8601 / RFC 3339 strings with an offset or `Z` for instants (`"2026-10-30T14:05:00Z"`), `"YYYY-MM-DD"` for dates, IANA zone in a separate field when needed. Not epoch numbers without a unit in the field name; if you use epoch, name it `createdAtMs`.
- Validate on input: `z.iso.datetime({ offset: true })`, `z.iso.date()`.
- Display with `Intl.DateTimeFormat` (or `toLocaleString`) and an explicit `timeZone` when the zone is not the viewer's: `new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short", timeZone: event.zone })`. Relative times with `Intl.RelativeTimeFormat`. Cache formatters like number formatters.
- Server rendering: the server's zone is not the user's. Rendering local times on the server causes hydration mismatches and wrong times. Render instants in the user's saved zone, or on the client.
- Servers run in UTC (`TZ=UTC`); never depend on the host zone.

## 8. Testing time

- Inject time: functions take `now: Temporal.Instant` (or a `Clock` object) instead of calling `Date.now()` inside. Then tests pass fixed values.
- When injection is impractical, use the test runner's fake timers (`vi.useFakeTimers(); vi.setSystemTime(new Date("2026-03-29T00:30:00Z"))`), and restore them after each test.
- Always test: a DST transition day in a zone with DST, month ends (Jan 31 plus 1 month), Feb 29, year boundary, a zone west of UTC (`America/Los_Angeles`) and one east (`Asia/Tokyo`), and midnight UTC vs local midnight.
- Money tests: allocation sums to the total, rounding mode at .5 boundaries, zero-decimal and three-decimal currencies, negative amounts (refunds).
- Run the test suite with `TZ=America/Los_Angeles` once in CI to flush out hidden local-zone assumptions.

## 9. Checks

- **No float money.** Pass: no `parseFloat`, `toFixed`, or fractional literals on money fields. Verify: `rg -n -i '(price|amount|total|cost|balance|fee|tax)\w*\s*[:=].*(parseFloat|toFixed|\d+\.\d+)' -t ts -t js .` and review; `rg -n 'toFixed\(' -t ts -t js .`
- **Money has a currency.** Pass: money types include a currency code. Verify: `rg -n 'amount\w*\s*:\s*(number|bigint|string)' -t ts .` then check each type also has `currency`.
- **No float columns for money.** Pass: zero. Verify: `rg -n -i '(price|amount|total|balance)\w*.*(float|double|real)\b' -g '*.{sql,prisma,ts}' .`
- **Formatting through Intl.** Pass: no hand-built currency strings. Verify: `rg -nP "['\"\x60][$€£¥]['\"\x60]?\s*\+|\.toFixed\(2\)" -t ts -t js .` returns nothing that formats money.
- **No ambiguous Date parsing.** Pass: `new Date(` only receives ISO strings with offsets, epoch numbers, or no argument. Verify: `rg -nP 'new Date\((?!\)|\d|Date\.now)' -t ts -t js .` and review each.
- **No Moment in new code.** Pass: `moment` not added; one date library at most. Verify: `rg -o '"(moment|moment-timezone|dayjs|date-fns|luxon|@js-temporal/polyfill|temporal-polyfill)"' -g 'package.json' -g '!**/node_modules/**' . | sort | uniq -c`
- **IANA zones, not offsets.** Pass: no hardcoded `+01:00`-style zones or `EST`/`CET` used as zones. Verify: `rg -n "timeZone:\s*['\"](EST|PST|CET|CEST|GMT[+-])" -t ts .`
- **Clock injected in domain logic.** Pass: no `Date.now()`/`new Date()` inside domain/service modules. Verify: `rg -n 'Date\.now\(\)|new Date\(\)' -t ts src/domain src/services 2>/dev/null`
- **Timestamps stored with zone.** Pass: Postgres instants are `timestamptz`. Verify: `rg -n -i 'timestamp(?! ?with time zone)(?!tz)' -P -g '*.sql' .`
- **Tests cover DST and month ends.** Pass: at least one test per date utility uses a DST date. Verify: `rg -n '03-29|03-08|10-25|11-01|-01-31|02-29' -g '*.test.*' .`
