# Edge case catalogue

The big list an agent pulls test inputs from. Do not invent edge cases from memory during a session: open this file, pick the sections that match the inputs and state of the feature, and try each row that applies. Every row says what to try and what usually breaks. Values marked **verified** were run on this machine (Node 24.21, Python 3.14, 2026-10-31); the rest come from the cited sources.

Sources: Big List of Naughty Strings (BLNS, MIT licence, 515 strings in `blns.json`), Hendrickson's Test Heuristics Cheat Sheet (2006), the "Falsehoods programmers believe" collection (github.com/kdeldycke/awesome-falsehood): names (McKenzie 2010), time (Sussman 2012), addresses (Tandy), phone numbers (libphonenumber), email. Unicode UAX 15 (Normalization, Unicode 18.0, 2026).

## Contents

1. How to use the catalogue
2. Strings
3. Unicode in depth
4. Numbers and money
5. Dates and time
6. Names and addresses
7. Emails, phone numbers, URLs
8. Files and paths
9. Lists and collections
10. Network
11. Concurrency
12. Permissions and roles
13. State and lifecycle
14. Driving the catalogue from a script
15. Checks

## 1. How to use the catalogue

1. List every input and every piece of state the feature touches (SFDPOT "Data" and "Time", [heuristics.md](heuristics.md) section 2).
2. For each, take the matching section here. Start with the rows marked **[core]**: they find the most bugs for the least effort.
3. Try each value through every path the data travels: create, update, search, display, export, import (follow the data).
4. Check the result in storage, not only in the response: query the DB, read the file.
5. A value that fails becomes a bug report ([bug-reports.md](bug-reports.md)) and then a regression test. Put repeatable values into a fixture file in the repo (`tests/fixtures/naughty.json`).

Only use attack strings (injection, terminal escapes) against software the owner controls. BLNS warns that using them on third party software may be a crime.

## 2. Strings

| Input | Example | What breaks |
|---|---|---|
| **[core]** Empty | `""` | Required checks only in the UI; DB stores `''` vs `NULL` inconsistently |
| **[core]** Whitespace only | `" "`, `"\t"`, `"\n"`, `"\u00A0"` (no break space), `"\u3000"` (ideographic space) | `trim()` in JS removes U+00A0 and U+3000, but `str.strip()` rules differ by language; "blank" names pass |
| Leading and trailing spaces | `" anna "` | Duplicate accounts "anna" and "anna "; login fails after copy paste |
| **[core]** Very long | 255, 256, 257, 1000, 1024, 2048, 10 000, 1 000 000 characters | Silent truncation at `varchar(255)`; layout overflow; request body limits; regex backtracking (ReDoS) |
| Long without spaces | `"a" * 300` | No wrapping: text runs out of its box |
| Byte vs character length | 100 Kazakh letters = 200 bytes in UTF-8 | Limits checked in characters in the UI and bytes in the DB (MySQL `utf8` 3 byte, C buffers) |
| Delimiters | `` " ' ` \| / \ , ; : & < > ^ * ? `` and Tab | CSV export breaks on comma and quote; shell commands break on quotes |
| Line endings | `"a\r\nb"`, `"a\rb"`, a trailing `\n` | Pasted values with a trailing newline fail equality; Windows files parsed as one line |
| Null byte | `"a\u0000b"` | Postgres rejects `\0` in text (error 22021); C strings cut at it |
| **[core]** HTML looking | `<b>bold</b>`, `<script>alert(1)</script>`, `<img src=x onerror=alert(1)>` | Rendered instead of escaped (XSS); or escaped twice (`&amp;lt;`) |
| SQL looking | `' OR '1'='1`, `'; DROP TABLE users;--`, `O'Brien` | Injection, or a legit apostrophe name that fails to save |
| Template looking | `{{7*7}}`, `${7*7}`, `#{7*7}`, `%s %n` | Server side template injection, format string bugs; "49" appears |
| Path looking | `../../etc/passwd`, `C:\Windows`, `CON`, `nul`, `aux.txt` | Path traversal in uploads; Windows reserved names fail to save |
| Numeric strings | `"0"`, `"-0"`, `"1e3"`, `"0x10"`, `"Infinity"`, `"NaN"`, `"00123"` | JS coercion: `"0"` falsy in some checks; leading zeros lost (postcodes, phone) |
| Reserved words | `null`, `undefined`, `true`, `None`, `NaN` as text | A user named "Null" breaks a system that stringifies missing values |
| Terminal escapes | `"\u001b[31mred"`, `"\u001b]0;title\u0007"` | Logs and TUIs change colour or title; CLI output corrupted |
| Scunthorpe | "Scunthorpe", "Essex", "Dickens" | Profanity filters block real names and places |
| Case changing length | `"ß".toUpperCase()` gives `"SS"`, `"İ".toLowerCase()` gives two code points (**verified**) | Length checks before and after case mapping disagree; buffer sizes |

Use BLNS for the long tail: its sections cover reserved strings, numeric strings, special characters, Unicode symbols and accents, quotation marks, two byte characters, strings that change length when lowercased, emoji, Unicode numbers, right to left strings, trick Unicode, Zalgo text, upside down text, script injection, SQL injection, server code injection, unwanted interpolation, file inclusion, known CVEs, MSDOS and Windows special file names, the Scunthorpe problem, terminal escape codes, and strings that crashed iMessage.

## 3. Unicode in depth

| Input | Example | What breaks |
|---|---|---|
| **[core]** Cyrillic | `Привет`, `Ёлка` (ё and е), `йод` | Search: "елка" does not find "Ёлка"; case insensitive search works only for ASCII (`ILIKE` is fine in Postgres, SQLite `LIKE` is ASCII only) |
| **[core]** Kazakh letters | `ә ө ү ұ қ ғ ң һ і` and capitals `Ә Ө Ү Ұ Қ Ғ Ң Һ І` (U+04D9, U+04E9, U+04AF, U+04B1, U+049B, U+0493, U+04A3, U+04BB, U+0456) | Fonts without these glyphs show boxes (tofu) or fall back to another font; Kazakh `і` (U+0456) looks identical to Latin `i` so search misses it; users without a Kazakh layout type Latin `h` for `һ` and `i` for `і` |
| Mixed script homoglyphs | `аpple` (Cyrillic а + Latin pple), `Аlmaty` | Two accounts that look the same; search misses; phishing in usernames |
| Combining marks (NFD) | `"e\u0301"` vs `"é"` (U+00E9); `"и\u0306"` vs `"й"` | Equal on screen, unequal in code: `"e\u0301" === "é"` is false (**verified**); macOS file names arrive in NFD; Russian й typed on some keyboards is decomposed |
| Normalisation | Normalise with `s.normalize("NFC")` before compare and store | NFC is the W3C recommendation for content (UAX 15). NFKC also folds compatibility characters (`ﬁ` becomes `fi`, `①` becomes `1`): use only for identifiers and search keys, never to rewrite user text |
| Precomposed only letters | `ә` (U+04D9) has no decomposition; `й` decomposes to и + U+0306 (**verified**) | Code that strips combining marks to "remove accents" turns й into и but leaves ә alone: inconsistent search folding |
| **[core]** Emoji, skin tone | `👍🏽` is 2 code points, 4 UTF-16 units (**verified**) | `.length` limits cut the modifier off; one emoji counted as 2 or 4 characters |
| ZWJ sequences | `👨‍👩‍👧‍👦` is 1 grapheme, 11 UTF-16 units (**verified**) | Truncation in the middle produces separate people; cursor moves inside the emoji; use `Intl.Segmenter` to count graphemes |
| Flags | `🇰🇿` (two regional indicators) | Split in half becomes two letters "K" "Z" |
| Zero width | `"a\u200Bb"` (zero width space), `"\u200D"` (ZWJ), `"\uFEFF"` (BOM), `"\u2060"` | Invisible duplicates ("admin" vs "adm\u200Bin"); BOM at start of an uploaded CSV breaks the first header name |
| **[core]** RTL text | `مرحبا`, `שלום`, mixed `Order #123 شكرا` | Punctuation and numbers jump to the wrong side; layout not mirrored |
| Bidi control characters | `"\u202Eabc"` (right to left override), `"\u2066"` to `"\u2069"` (isolates) | File name "invoice\u202Efdp.exe" displays as "invoiceexe.pdf"; following text on the line is reversed |
| Zalgo | `Z̵̡̢̛͓a̸͎l̷g̶o̴` (many stacked marks) | Overflows line height, overlaps text above and below |
| Astral plane characters | `𝐀` (U+1D400), `𠀀` (CJK ext B) | UTF-16 surrogate pairs split; MySQL `utf8` (3 byte) rejects them; must be `utf8mb4` |
| Other scripts | Chinese `中文`, Japanese `日本語`, Thai `ภาษาไทย` (no spaces between words), Devanagari `हिन्दी` | Word wrap, line height, missing fonts |

## 4. Numbers and money

| Input | Example | What breaks |
|---|---|---|
| **[core]** Zero | `0`, `-0`, `0.0` | Division by zero; `0` treated as "missing" (`if (!qty)`); `Math.round(-0.5)` is `-0` (**verified**) |
| **[core]** Negative | `-1`, `-0.01` | Negative quantity gives a refund; negative age accepted |
| Integer limits | 32767, 32768, 65535, 65536, 2147483647, 2147483648, 4294967296, 2^53 (9007199254740992) | Overflow in `i16`/`i32` columns; JS loses precision above 2^53: `2**53 + 1` prints `9007199254740992` (**verified**). JS timers clamp delays above 2147483647 ms (about 24.8 days) and fire at once: check every configured duration handed to a timer (TanStack gcTime, session TTL, retry delay, reminder) against the runtime maximum, unless the library documents its own limit |
| Huge | `1e308`, `1e309` (Infinity), 100 digit numbers | Infinity stored or shown; layout overflow |
| Tiny | `1e-16`, `0.0001` | Rounds to zero; displayed as `1e-16` |
| Float arithmetic | `0.1 + 0.2` gives `0.30000000000000004` (**verified**); `(1.005).toFixed(2)` gives `"1.00"` (**verified**) | Money totals off by a cent; never use binary floats for money: store minor units as integers or use a decimal type |
| **[core]** Decimal separator by locale | `1,5` vs `1.5`; `Number("1,5")` is `NaN`, `parseFloat("1,5")` is `1` (**verified**) | German, Russian and Kazakh users type a comma; the app silently drops the decimals |
| Grouping separators | `1,234,567`, `1.234.567,89`, `1 234 567` | Russian and Kazakh `Intl` output uses U+00A0 as the group separator, French uses U+202F (**verified**): a test that compares with a normal space fails, and parsing your own formatted output fails |
| Indian grouping | `en-IN` formats 1234567.891 as `12,34,567.891` (**verified**) | Hard coded 3 digit grouping |
| Empty and spaces | `Number("")` and `Number(" ")` are `0` (**verified**) | An empty field becomes 0 instead of an error |
| NaN | `NaN`, `"NaN"` | `NaN !== NaN`; `JSON.stringify({a: NaN})` gives `{"a":null}` (**verified**): NaN turns into null in the API |
| Scientific notation | `1e3`, `1E-16` | Accepted by `Number()` where the spec wants digits only |
| Currency | KZT has 2 minor units in ISO 4217 but cash has no tiyn in practice; JPY has 0 minor units; KWD has 3 | Hard coded 2 decimals; `ja-JP` JPY 1234.5 formats as `￥1,235` (**verified**): rounding happens in display |
| Currency symbol position | `kk-KZ` KZT: `1 234,50 ₸`; `ru-RU` KZT: `1 234,50 KZT` (**verified**) | Symbol before the number hard coded; missing ₸ glyph in the font |
| Percentages and rounding | 33.333 percent times 3 | Parts do not add up to 100; rounding mode (banker's vs half up) differs between DB and app |
| Prices | Falsehoods about prices: prices are not always positive, a currency can change, tax can be included or not | Discounts below zero; tax added twice |

## 5. Dates and time

| Input | Example | What breaks |
|---|---|---|
| **[core]** Midnight | 00:00, 23:59:59, 24:00 | "Today" computed in UTC on the server, local on the client: a habit ticked at 00:30 in Almaty (UTC+5) lands on yesterday |
| **[core]** Time zones | `Asia/Almaty` (UTC+5 since 1 March 2024, was UTC+6; **verified** with `Intl`), `Asia/Kolkata` (+05:30), `Asia/Kathmandu` (+05:45), `Pacific/Chatham` (+13:45 in summer), `Pacific/Kiritimati` (+14), `America/St_Johns` (-03:30) | Offsets assumed to be whole hours; stored offsets go stale when a country changes its zone (Kazakhstan 2024): store the IANA zone name, not the offset |
| **[core]** DST gap | `Europe/Berlin` 29 March 2026, 02:00 to 03:00 does not exist; `TZ=Europe/Berlin` parsing `2026-03-29T02:30:00` gives 03:30 local (01:30Z) (**verified**) | A reminder at 02:30 never fires or fires twice; a day has 23 hours |
| DST overlap | `Europe/Berlin` 25 October 2026, 02:30 happens twice (+02:00 then +01:00) (**verified**) | Duplicate events; durations negative; "add 24 hours" is not "same time tomorrow" |
| Invalid dates | 30 February, 31 April, 31 September, 29 February 2027 | `new Date("2026-02-30")` in V8 rolls over to 2 March instead of failing (**verified**) |
| Leap years | 29 Feb 2028; 1900 not leap, 2000 leap | Age and anniversary on 29 Feb; "one year later" |
| Leap seconds | 23:59:60 | Parsers reject it; most systems smear it. No new leap seconds are planned before 2035 (CGPM 2022 decision) but old data can contain them |
| Week start | `en-US` week starts Sunday (firstDay 7), `ru-RU` Monday (firstDay 1) (**verified** via `Intl.Locale.getWeekInfo()`); Kazakhstan uses Monday | Calendar grids and "this week" stats wrong for one group |
| 12 and 24 hour | `en-US` shows `12:30 AM` (**verified**) | "12 AM" vs "12 PM" confusion; parsing "0:30 PM"; space before AM/PM was U+202F in some ICU versions and is a normal space in Node 24 (**verified**): tests that hard code either break across versions |
| Date formats | `06/05/2001` (US: June 5, UK: 5 June), `05.06.2001` (ru, kk), `2001-06-05` | Ambiguous parsing; always parse ISO 8601 and format with `Intl` |
| Far future and past | 1 Jan 1970, 31 Dec 1969 (negative epoch), 19 Jan 2038 03:14:08 UTC (32 bit overflow), year 9999, year 10000, year 0001 | Year 2038 bugs in `i32` timestamps; 4 digit year assumptions |
| Clocks wrong | Device clock set 3 years ahead, or 5 minutes behind the server | JWT "not yet valid"; streaks jump; Sussman: "the server clock and the client clock will always be set to the same time" is false |
| Durations across zone change | A flight from Almaty to Berlin during a streak | Habit "today" changes length or repeats |
| Timeouts | A session idle for exactly the timeout, plus one second | Off by one in expiry checks |
| **[core]** Zero length interval | start == stop (timer stopped in the same second), duration 0, a booking whose end equals its start | A 0:00 line reaches an invoice or a report, division by duration, an unstable sort. Expected: what the spec says (discard or refuse to save); if silent, a spec question, and a 0 length entry never reaches anything billed |

Falsehoods about time that matter most (Sussman 2012): there are not always 24 hours in a day; months are not only 30 or 31 days; a week can start and end in different months and years; the time zone a program runs in can change; the system clock can be wildly wrong; client and server clocks differ, sometimes by decades.

Agent tools: every suite with date code runs under the business zone and a far zone, on the server and on the client (`../backend/external-services-and-time.md` section 2). Freeze time with fake timers or an injected clock, and use dates that cross a DST boundary in fixtures.

## 6. Names and addresses

From McKenzie's "Falsehoods programmers believe about names" (2010) and the addresses list. Each falsehood is a test:

| Falsehood (it is false that...) | Test value |
|---|---|
| People have exactly one canonical full name | Name change after marriage; old name on past orders |
| Names fit in a defined amount of space | `Wolfeschlegelsteinhausenbergerdorff`; a 300 character name |
| **[core]** Names are written in ASCII | `Zoë Ärger-Öztürk`, a Kazakh name with ә ө ү (`Әсел Өмірбекова Үсенқызы`), `Łukasz`, `Nguyễn` |
| Names are written in a single character set | `Анна Smith` |
| Names are case sensitive / insensitive | `van der Berg`, `McDonald`, `ALL CAPS NAME`, `bell hooks` |
| Names have no numbers | `Louis XIV`, `John Smith 3rd` |
| People have first and last names | Mononyms: `Sukarno`, many Indonesians; patronymic only |
| First and last names are different | `Ng Ng` |
| Names have a fixed order | Family name first: `Nazarbayev Nursultan` in some Kazakh documents, Chinese, Hungarian |
| Prefixes and suffixes can be ignored | `de la Cruz`, `O'Brien`, `Jr.` |
| Names are globally unique | Two `Aidos Serikov` in one class |

Kazakh specifics: patronymic suffixes `-ұлы` (son of) and `-қызы` (daughter of) are part of the surname; Russian style patronymics (`Серикович`) are also common; Latin transliteration varies (`Nurgali`, `Nurghali`, `Nurğali`).

Addresses: no postcode (many countries), postcode with letters (UK `SW1A 1AA`), a house number like `12A` or `12/3` (common in Kazakhstan: building and flat), no street name (rural `аул`), very long lines, addresses in two scripts. Never validate an address format beyond "not empty" unless the spec demands a specific country.

## 7. Emails, phone numbers, URLs

**Emails** (RFC 5321 and 5322; "Falsehoods about email"):

| Value | Valid? | What breaks |
|---|---|---|
| `a@b.co` | yes | Over strict regex rejects short domains |
| `first.last+tag@example.com` | yes | `+` stripped or rejected; duplicates via tags |
| `"john doe"@example.com` | yes (quoted local part) | Rejected; rare, decide in the spec |
| **[core]** `user@müller.de`, `user@xn--80ak6aa92e.com` and `user@пример.рф` | yes (IDN) | Unicode domain rejected or not punycoded |
| `ÄLIA@Example.COM` | yes | Case: the domain is case insensitive, the local part technically is not, but treat as insensitive for login |
| `a@b` | valid syntax, not routable | Accepted then mail bounces |
| 254+ characters | no | Length limits |
| Trailing space or newline | no | Paste from a mail client |

An invalid email test without a valid but unusual counterpart (IDN) is incomplete. The only real validation is sending a confirmation email.

**Phone numbers** (libphonenumber "Falsehoods about phone numbers"): phone numbers are not numbers (keep as strings, leading zeros and `+`); a person has more than one; numbers get reused; a country calling code can serve several countries (`+7` is Russia and Kazakhstan); numbers are not always written in ASCII digits (Arabic Indic digits `٠١٢`); you cannot always text a number. Test values: `+7 701 123 45 67`, `87011234567` (Kazakh domestic format with 8), `+44 20 7946 0958`, `+1 (555) 010-0000`, extensions `ext. 12`. Use libphonenumber, not a regex.

**URLs**: `https://пример.рф`, a URL with a space, `javascript:alert(1)` (must be rejected in link fields), a 2000+ character URL, `http://localhost`, `http://169.254.169.254/` (SSRF on servers that fetch URLs).

## 8. Files and paths

| Input | What breaks |
|---|---|
| **[core]** Empty file (0 bytes) | Parser assumes a header line; division by zero in progress bars |
| **[core]** Huge file (larger than RAM, larger than upload limit) | Loads into memory; no clear limit message; timeout |
| Wrong extension (`photo.png` that is a PDF), no extension, double extension (`a.pdf.exe`) | Type trusted from the name; MIME sniffing |
| Truncated file (cut in the middle of a UTF-8 sequence or a ZIP) | Crash instead of an error |
| Non UTF-8 text (Windows 1251 Cyrillic, UTF-16 with BOM, UTF-8 with BOM) | Mojibake `Ð¿Ñ€Ð¸Ð²ÐµÑ‚`; first CSV column named `\uFEFFname` |
| **[core]** Unicode file names (`Отчёт 2026.pdf`, `әлем.txt`, NFD names from macOS) | Upload renames to `____.pdf`; two names that look the same |
| Long names (255 bytes, which is only 127 Cyrillic letters in UTF-8) | ENAMETOOLONG on Linux at 255 bytes, not characters |
| Special characters in names (`space * ? / \ \| < > , . ( ) [ ] { } ; : ' " ! @ # $ % ^ &`) and names starting with `-` | Shell scripts break; `rm -file` read as flags |
| Windows reserved names (`CON`, `PRN`, `AUX`, `NUL`, `COM1`, `LPT1`) | Cannot be created on Windows; sync to a Windows user fails |
| Read only file, no read permission (`chmod 000`), directory instead of file, symlink loop | Wrong error message or crash |
| Disk full, quota exceeded | Partial write left behind; data loss when overwriting in place (write to a temp file and rename) |
| File changed or deleted while open | Stale reads; crash |
| Already exists, locked by another process, on a network or removable drive | Overwrite without asking; hang |
| Path traversal (`../../`), absolute paths in archives (zip slip) | Writes outside the target directory |

## 9. Lists and collections

| Input | What breaks |
|---|---|
| **[core]** Empty | Blank screen instead of an empty state; `max()` of empty list throws; "0 items" plural |
| **[core]** One | Plural "1 items"; layout designed for a grid of many |
| Two | Off by one, "between" logic |
| **[core]** Many (1000, 10 000, 100 000) | Slow render without virtualisation; N+1 queries; API without pagination |
| Exactly the page size, page size plus one | Last page empty or missing |
| Duplicates | Same item twice in a set; React key warnings; double charge |
| Sorting with locale | Default JS sort puts `Z` before `a` and `ä` after `z`; `["ә","а","б","я","ё","е"]` sorts as `аәбеёя` only with `Intl.Collator("kk")` (**verified**); Swedish sorts `ä` after `z`, German after `a` (**verified**) |
| Numeric strings sorted as text | "Item 10" before "Item 2"; use `Intl.Collator(undefined, {numeric: true})` |
| Sort stability | Equal keys reorder between page loads; pagination shows an item twice |
| Item added or removed while paging | Offset pagination skips or repeats items; use cursor pagination |
| Nested and recursive structures | A category that is its own parent; cycles in a tree hang the renderer |

## 10. Network

| Condition | How an agent provokes it | What breaks |
|---|---|---|
| **[core]** Offline | Stop the local backend; set the API URL to a closed port (`http://127.0.0.1:9`) | Spinner forever; unhandled promise rejection; data typed by the user lost |
| Slow (3G, 2 s latency) | A delaying proxy, or `tc qdisc` in a container (needs the user's yes and sudo); in tests, MSW `delay(2000)` | Timeouts too short; double taps while waiting; race between old and new responses |
| **[core]** Drop mid request | Kill the server during a request; MSW returning `HttpResponse.error()` | Half saved state; client thinks it failed but the server committed |
| Retry duplicates | Send the same POST twice with the same body (two `curl` calls) | Two orders, two charges; fix with idempotency keys |
| Out of order responses | Search as you type with a slow first request | Old results overwrite new ones |
| 4xx and 5xx with HTML body | Return a proxy error page | `JSON.parse` crash; error message shows HTML |
| Captive portal, DNS failure, TLS error | Point at an unresolvable host | Generic error with no retry |
| Large responses | 10 MB JSON | Memory spikes on mobile |

## 11. Concurrency

| Case | Agent probe | What breaks |
|---|---|---|
| **[core]** Double submit | Two identical requests at once: `for i in 1 2; do curl -s -X POST ... & done; wait` | Duplicate rows, double charges |
| Two tabs, same user | Two scripts with the same session editing the same record | Lost update: last write wins silently; fix with version columns or `updated_at` checks |
| Two devices | Two clients syncing offline changes to the same record | Conflicts resolved by losing data |
| Read modify write | Increment a counter from 50 parallel requests | Final count below 50 |
| Unique constraints under race | Two sign ups with the same email in parallel | Both succeed if uniqueness is only checked in code, not by a DB constraint |
| Background job and user action | Edit a record while a scheduled job updates it | Job overwrites user change |
| Cancel then retry | Abort a request and start a new one | Both complete |

## 12. Permissions and roles

| Case | What breaks |
|---|---|
| **[core]** Logged out user calls a protected API directly | Server trusts the UI to hide the button (`curl` without a token must get 401) |
| **[core]** User A reads or edits user B's record by changing the id | IDOR; in Supabase, missing or wrong Row Level Security policies (query with the anon key and another user's JWT) |
| Role downgraded while logged in | Old JWT keeps admin rights until expiry |
| Account deleted or suspended mid session | Requests still succeed |
| OS permissions denied (camera, notifications, location, storage) | Crash or silent failure instead of an explanation; permission revoked in settings while the app runs |
| Permission granted "only this time" or approximate location (Android 12+) | Logic assumes full permission |

## 13. State and lifecycle

| Case | What breaks |
|---|---|
| **[core]** First run, empty database, no settings file | Crash on a missing key; no onboarding |
| **[core]** Upgrade from the previous version with real old data | Migration fails; settings reset; cached schema mismatch |
| Downgrade or reinstall | New data format unreadable by old app |
| Logged out mid action (token expired) | Form data lost on redirect to sign in |
| App killed and restored (mobile process death) | Screen state lost; navigation stack broken |
| Interrupted migration | Half migrated database |
| Corrupted local state (bad JSON in storage) | App never starts again; catch parse errors and reset safely |
| Long running (days) | Memory leaks; timers drift; tokens expire |
| Feature flag flipped mid session | Mixed old and new UI |
| Clock or time zone changed while running | Schedules recomputed wrongly |

## 14. Driving the catalogue from a script

Throw BLNS at an API and look for 500s, network errors and values that do not round trip. Run only against a local or test backend. The script below was **verified** against a toy local server that returns 500 on a null byte and truncates names at 255 UTF-16 units: it reported the 500, the truncation of a 300 character name, and two BLNS strings (index 96 and 113, 260 and 269 units long) that the truncation also cut, with no false positives.

```bash
# fetch once into the scratchpad (MIT licence)
curl -sL -o "$SCRATCH/blns.json" \
  https://raw.githubusercontent.com/minimaxir/big-list-of-naughty-strings/master/blns.json
```

```js
// naughty.mjs: node naughty.mjs blns.json http://localhost:3000/api/profile
import { readFileSync } from "node:fs";
const [, , file, url] = process.argv;
const strings = JSON.parse(readFileSync(file, "utf8"));
for (const [i, s] of strings.entries()) {
  const res = await fetch(url, {
    method: "PATCH",
    headers: { "content-type": "application/json", authorization: `Bearer ${process.env.TOKEN}` },
    body: JSON.stringify({ name: s }),
  }).catch((e) => ({ status: "NETWORK", text: async () => String(e) }));
  if (res.status >= 500 || res.status === "NETWORK") {
    console.log(i, res.status, JSON.stringify(s).slice(0, 80));
    continue;
  }
  if (res.status < 300) {
    const back = await (await fetch(url, { headers: { authorization: `Bearer ${process.env.TOKEN}` } })).json();
    // stored as sent, or as its NFC form, both count as a round trip
    if (back.name !== s && back.name !== s.normalize("NFC")) console.log(i, "ROUNDTRIP", JSON.stringify(s).slice(0, 40), "->", JSON.stringify(back.name).slice(0, 40));
  }
}
```

The same pattern works for a Rust function with `proptest` (see `~/.claude/skills/kwx-developer/languages/rust/testing.md`) or a CLI (`while IFS= read -r s; do ./tool add "$s" || echo "FAIL $s"; done < blns.txt`, skipping lines starting with `#`). Every failing string goes into a fixture and a named test.

## 15. Checks

- [ ] Every input and state of the feature was listed and matched to a section here.
- [ ] All **[core]** rows of the matching sections were tried.
- [ ] Results were checked in storage (DB row, file) and on the way back out, not only in the response code.
- [ ] Cyrillic, Kazakh, emoji with ZWJ and one RTL string went through every path (create, update, search, display, export).
- [ ] Numbers were tried with a comma decimal separator and at the integer and float limits that the types allow.
- [ ] Dates were tried at midnight, across a DST change, in a half hour zone, and on 29 February.
- [ ] Every interval or duration had a zero length case (start == stop), and nothing of length 0 reached a bill or a report unless the spec allows it.
- [ ] Every email field had a valid IDN case (`user@müller.de`) beside its invalid cases; every name field had `Zoë Ärger-Öztürk` and a Kazakh name.
- [ ] Double submit and two sessions on the same record were tried for every write endpoint touched.
- [ ] Every protected endpoint was called without a token and with another user's token.
- [ ] Attack strings were used only against software the owner controls.
- [ ] Failing values were saved as fixtures and turned into named tests.
