# Test heuristics

A heuristic is a fallible method for solving a problem: a guideword that makes you think of a test you would otherwise miss. This file is the set an agent walks through when it plans what to explore. Each heuristic has a short definition, how to use it as an agent, and a worked example on a mobile app or website. Most come from James Bach's Heuristic Test Strategy Model (HTSM, v6.3, 2024), Michael Bolton's FEW HICCUPPS oracles (2012), Elisabeth Hendrickson's Test Heuristics Cheat Sheet (2006) and James Whittaker's books and tours (2002, 2009). They are prompts, not procedures: Bolton's warning is that oracle principles are "fallible and context-dependent; to be applied, not followed."

The running examples use two products the owner builds: **Habit**, an Expo app (Android first) that tracks daily habits and syncs to Supabase, and **Shop**, a Next.js site with a cart and checkout.

## Contents

1. How to use this file
2. SFDPOT: the product elements (San Francisco Depot)
3. FEW HICCUPPS: consistency oracles
4. Quality criteria: what "good" means
5. The nine general test techniques (HTSM)
6. Hendrickson's cheat sheet heuristics
7. CRUD
8. Goldilocks and boundaries
9. Zero, one, many
10. Interruptions
11. Follow the data
12. Configurations
13. Whittaker's attacks (How to Break Software)
14. Whittaker's tours (Exploratory Software Testing)
15. Checks

## 1. How to use this file

1. Build the product model first with SFDPOT (section 2). Write it as a short list per letter.
2. For each risky element, pick two or three heuristics from sections 6 to 14 and turn them into charters ([exploratory.md](exploratory.md) section 3).
3. During the session, judge results with the HICCUPPS oracles (section 3).
4. At the end, check the quality criteria list (section 4) for any category you never looked at, and say so in the report.

Evidence level for everything in this file: **moderate** (well known practitioners, widely taught in Rapid Software Testing and BBST). None of it is backed by controlled studies; the value is in coverage of ideas.

## 2. SFDPOT: the product elements

Bach's mnemonic "San Francisco Depot" lists the product factors in HTSM. Walk through each letter and write what exists in the product under test.

| Letter | Factor | Sub items (HTSM v6.3) | Agent channel |
|---|---|---|---|
| S | Structure: everything that constitutes the physical product | code, hardware, services, non executable files, collateral (docs, packaging, licences) | file tree, package manifests, build outputs |
| F | Function: everything the product does | business rules, multi user and social, calculation, security related, transformations, state transitions, multimedia, error handling, interactions, testability features | read handlers, call them |
| D | Data: everything it processes and produces | input and output, preset (defaults, seed data), persistent, interdependent, sequences and combinations, cardinality (zero, one, many, max), big and little, invalid and noise, lifecycle (create, access, modify, delete) | DB schema, fixtures, API payloads |
| I | Interfaces: every conduit by which it is accessed or expressed | user interfaces, system interfaces (logs, disk, network, other programs), API and SDK, import and export | routes, CLI flags, IPC, files written |
| P | Platform: everything it depends on outside the project | external hardware, external software (OS, fonts, drivers, browsers), embedded components (libraries), product footprint (memory, file handles) | lockfiles, OS versions, fonts installed |
| O | Operations: every experience people could have with it | users (kinds and roles), environment (noise, light, distraction), common use, uncommon use (backups, updates), extreme use, disfavored use (ignorant, careless, malicious) | personas, logs of real use |
| T | Time: any relationship with time | time related data (timeouts, time zones, holidays), input and output timing, pacing (fast, slow, bursts, letting it sit), concurrency | timers, schedulers, clocks |

**Worked example, Habit (Expo app):**

- S: Expo app, Kotlin widget module, Supabase project, Edge Function for reminders, app store listing text.
- F: create habit, tick today, streak calculation (calculation), reminders (state transitions), sync conflict resolution (interactions), sign in (security).
- D: habit names (free text, Unicode), tick records with dates (persistent, lifecycle), streak counts (big and little: 0 days, 3650 days), seed habits shown on first run (preset).
- I: React Native screens, home screen widget, Supabase REST, push notifications, export to CSV.
- P: Android 10 to 16, OEM battery savers that kill background work, system font size, the Kazakh keyboard, Supabase availability.
- O: one user with three habits (common), one user with 200 habits (extreme), user who changes phone time zone on a flight (uncommon), user who taps "done" twenty times fast (disfavored).
- T: midnight rollover, DST change, device clock wrong, two devices ticking the same day, reminder at 23:59.

Each line is a charter seed. "T: two devices ticking the same day" becomes `Explore tick sync with two signed in clients (two scripts against the REST API) to discover lost or double ticks`.

## 3. FEW HICCUPPS: consistency oracles

Bolton's list of consistency heuristics (first published 2005, extended 2012). Each one says: we expect the product to be consistent with X. An inconsistency is a reason to suspect a problem, not proof.

| Oracle | Expect the product to be consistent with | Worked example |
|---|---|---|
| **F**amiliarity | not showing patterns of familiar problems | Shop: the cart total is computed with floats; familiar money bug, check 0.1 + 0.2 |
| **E**xplainability | behaviour we can explain clearly | Habit: streak drops from 12 to 0 after a DST night and nobody can say why: suspect a bug |
| **W**orld | what we know about the world | Shop: delivery date picker allows 30 February |
| **H**istory | past versions of itself | Habit: v1.4 kept ticks on reinstall, v1.5 loses them |
| **I**mage | the image the organisation wants to project | Shop: error page shows a raw stack trace with the DB host name |
| **C**omparable products | similar products, siblings, competitors, alternative algorithms | Habit: every calendar app on Android starts the week on Monday in Kazakhstan, Habit uses Sunday |
| **C**laims | what important people say about it: spec, docs, UI text, marketing, commit messages | Shop: README claims "prices include VAT", invoice adds VAT again |
| **U**ser desires (earlier: user expectations) | what reasonable users might want | Habit: undo after an accidental tick |
| **P**roduct | other elements of the same product | Shop: sign up rejects "a@b" but profile edit accepts it |
| **P**urpose | explicit and implicit uses of the product | Habit: a habit tracker whose reminder fires after the day is over |
| **S**tatutes and standards | laws, regulations, standards | Shop: no cookie consent for analytics in the EU; focus not visible (WCAG 2.4.7) |

Agent use: when you write a bug, fill the oracle line with one of these names and the concrete reference ("Claims: README line 14"). When you are unsure whether something is a bug, run through the list; two or more inconsistent oracles make a strong report.

## 4. Quality criteria: what "good" means

HTSM lists the dimensions in which people judge a product. Treat each as a risk category and check that at least one charter touched the ones that matter.

| Category | Sub items | Example question |
|---|---|---|
| Capability | sufficiency, correctness | Can a user actually export all their data? |
| Reliability | robustness, error handling, data integrity, safety | Does a crash mid sync lose ticks? |
| Usability | learnability, operability, accessibility | Can a TalkBack user tick a habit? |
| Charisma | aesthetics, uniqueness, entrancement, image | Does the empty state look broken or intentional? |
| Security | authentication, authorization, privacy, security holes | Can user A read user B's habits through the REST API (RLS)? |
| Scalability | | What happens with 10 000 ticks? |
| Compatibility | application, OS, hardware, backward, footprint | Does the app open data saved by the previous version? |
| Performance | | Does the list scroll smoothly with 200 habits? |
| Installability | system requirements, configuration, uninstallation, upgrades | Does an upgrade keep settings? |
| Development | supportability, testability, maintainability, portability, localizability | Can the strings be translated without code changes? |

## 5. The nine general test techniques (HTSM)

Every specific technique is a mix of these families. Use the list to check you are not doing only one kind.

| Technique | Core move | Agent version |
|---|---|---|
| Function testing | Test what it can do, one function at a time | Call each handler or command with a normal input and check the result |
| Domain testing | Partition the data: boundaries, typical, invalid, best representatives; force the whole range of outputs | Pick inputs per partition from [edge-case-catalogue.md](edge-case-catalogue.md) |
| Stress testing | Overwhelm the product: big data, high load, long runs, low memory | Seed 10 000 rows, run 50 parallel requests |
| Flow testing | Do one thing after another without resetting; vary timing and sequence | A script that runs create, edit, delete, undo, sync in a row |
| Scenario testing | A compelling story of how someone who matters does something that matters | "A nurse logs habits on night shift across midnight with a dying battery" |
| Claims testing | Challenge every claim in docs, UI text, specs, marketing | List every claim in README and UI copy, test each |
| User testing | Involve or simulate real users and roles | Use real usage logs if they exist; simulate several roles, not one |
| Risk testing | Imagine a problem, then look for it | "Could a user be charged twice?" becomes a charter |
| Tool supported testing | Use tools for many actions and checks | Property based tests, fuzzers, change detectors, data generators |

## 6. Hendrickson's cheat sheet heuristics

From the Test Heuristics Cheat Sheet (Hendrickson, Lyndsay, Emery, 2006). The ones with their own sections below are marked with the section number.

| Heuristic | Meaning | Worked example |
|---|---|---|
| Variable analysis | Find anything whose value can change: obvious, subtle or hidden | Shop: currency, locale, cart size, coupon state, time of day, logged in or not |
| Touch points | Any public or private interface that gives visibility or control | Habit: Supabase tables are a touch point to provoke and observe sync without the UI |
| Boundaries (8) | Approaching, at, just past | Name max length 50: try 49, 50, 51 |
| Goldilocks (8) | Too big, too small, just right | |
| CRUD (7) | Create, read, update, delete | |
| Follow the data (11) | A sequence of actions on data, checking integrity at each step | |
| Configurations (12) | Vary configuration variables | |
| Interruptions (10) | Log off, shut down, reboot, kill process, disconnect, hibernate, timeout, cancel | |
| Starvation | CPU, memory, network or disk at capacity | Habit: device storage full while saving an export |
| Position | Beginning, middle, end | Edit the first, a middle and the last habit in a reordered list |
| Selection | Some, none, all | Shop: apply a filter with no categories, some, all selected |
| Count (9) | 0, 1, many | |
| Multi user | Simultaneous create, update, delete from two accounts, or the same account twice | Habit: the same user on phone and tablet deleting the same habit |
| Flood | Many simultaneous requests flooding the queue | Shop: 100 add to cart requests in one second |
| Dependencies | "has a" relationships; apply CRUD, count, position, selection to them | Shop: delete a product that sits in 0, 1, many carts; delete the last line item then read the cart |
| Constraints | Violate them: required fields blank, invalid combinations, duplicate ids | Habit: two habits with the same name, end date before start date |
| Input method | Typing, paste, import, drag and drop, GUI versus API | Paste a name with a trailing newline; send via API what the UI forbids |
| Sequences | Vary order, undo and redo, reverse, combine, invert, simultaneous | Shop: apply coupon then change quantity, versus change quantity then apply coupon |
| Sorting | Alpha versus numeric, across pages | "Habit 10" sorts before "Habit 2"; sort stable across page 1 and 2 |
| State analysis | Draw states and transitions, then test each transition and the illegal ones | Order: cart, paid, shipped, refunded. Try refund before paid. |
| Map making | Pick a home state, take one step, return, repeat | Habit: from the home screen, each menu item one step deep and back |
| Users and scenarios | Use cases, soap operas, personas, extreme personalities | A soap opera: user renames a habit, changes time zone, reinstalls, restores backup, all in one day |

Frameworks on the same sheet: Lyndsay's judgment framework (inconsistencies, absences and extras against internal, external specific and external cultural references), input/processing/output, Gause and Weinberg's users/functions/attributes/constraints, and nouns and verbs (the objects in the system and what is done to them, plus adjectives and adverbs like "quickly, repeatedly, randomly" to generate scenarios).

## 7. CRUD

For every kind of thing the product stores, try create, read, update and delete, and then the combinations: read after delete, update after delete, delete twice, create a duplicate, update to the same value.

**Worked example, Shop addresses:**

| Step | Check |
|---|---|
| Create address | Appears in list and in checkout dropdown |
| Read | Same text everywhere (list, checkout, invoice, email) |
| Update while an order uses it | Old order keeps the old address (or the spec says otherwise) |
| Delete the default address | Another becomes default, or checkout asks; no crash |
| Delete, then press browser Back and submit the old form | Server rejects or recreates cleanly; no 500 |
| Delete twice (two tabs) | Second delete is a no op or a clear 404 |

Agent version: a script that does each step through the API and queries the table after each one.

## 8. Goldilocks and boundaries

Try values that are too big, too small and just right, and the values on and next to every boundary. Boundaries hide in the spec ("up to 50 characters"), in the code (`varchar(255)`, `u16`, `Int32`), in the platform (SMS 160 characters, file name 255 bytes) and in the UI (a box 120 px wide).

**Worked example, Habit reminder time and name:**

- Name: 0 characters, 1, 49, 50, 51, 255, 256, 10 000; 50 Kazakh letters (100 bytes in UTF-8, so a byte limit of 50 fails at 25 letters).
- Reminder: 00:00, 23:59, 24:00 (invalid), the minute that does not exist on a DST spring night.
- Streak: 0, 1, 999, 1000 (does "1,000" fit the badge?), 3650.

Find the hidden boundaries by reading the schema and types: `rg -n 'varchar\(|maxLength|max_length|\bu8\b|\bu16\b|\bi32\b|Int32' src supabase`.

## 9. Zero, one, many

Count heuristic: for every collection, test with none, exactly one and many (and the maximum if there is one). Bugs live in the empty state and in plural handling.

**Worked example, Shop orders page:**

- 0 orders: an empty state that says what to do, not a blank page or a spinner forever.
- 1 order: "1 order" not "1 orders"; in Russian "1 заказ", "2 заказа", "5 заказов" (see [i18n-and-localisation-testing.md](i18n-and-localisation-testing.md)).
- Many: 1000 orders: pagination, sort stability, load time.
- Apply to relations too: a customer with 0, 1, many invoices; an invoice with 0 line items.

## 10. Interruptions

Stop the product in the middle of something and see what state it comes back in. Hendrickson's list: log off, shut down, reboot, kill process, disconnect, hibernate, timeout, cancel. Mobile adds: incoming call, app to background, OS kills the app for memory, rotation, permission revoked while running, low battery mode.

**Worked example, Habit sync:**

| Interruption | How an agent can provoke it without touching the device UI | Expect |
|---|---|---|
| Network drops mid sync | Stop the local Supabase (`supabase stop`) during a sync script; or point the client at a proxy that closes the connection | No lost ticks; retry later; no duplicate rows |
| Process killed mid write | Kill the Node or test process during a batch write (`timeout -s KILL 0.2 node sync-test.js`) | Data either fully written or not at all |
| Session expires mid action | Shorten JWT expiry in the local config, run a long flow | Clear re sign in, no silent failure |
| Cancel | Call the abort signal on a running request | UI state returns to before; no half saved record |

App to background, rotation and OS kill need the device. Put them on the owner's checklist ([human-check-handoff.md](human-check-handoff.md)); never inject input into an emulator if the user's rules forbid it.

## 11. Follow the data

Perform a sequence of actions on one piece of data and check its integrity at each step. Hendrickson's example chain: enter, search, report, export, import, update, view. Whittaker's FedEx tour is the same idea.

**Worked example, Shop product name "Қымыз & Co <b>"**:

1. Create it in admin. Check DB: stored exactly, NFC.
2. Search for "қымыз" (lowercase). Found?
3. Show it on the product page. Escaped (no bold), all letters drawn.
4. Add to cart, check the cart API response.
5. Pay; check the order email and the PDF invoice (font has Kazakh glyphs?).
6. Export orders to CSV; open with a script, check UTF-8 and the comma inside the name is quoted.
7. Import the CSV into a fresh DB; compare with the original byte for byte.

Each hop is a place where encoding, escaping, truncation or normalisation can break.

## 12. Configurations

Vary the settings around the product: screen size and density, system font size, dark mode, language and region, network speed and latency, memory and disk, number of monitors, input devices, OS version, browser, feature flags, env vars.

**Worked example, Habit:**

- Android system font at 200 percent (owner check), display size largest, dark theme.
- Locale kk-KZ, ru-RU, en-US; region with week starting Sunday versus Monday.
- 24 hour versus 12 hour clock.
- Battery saver on (background work deferred).
- Env: `EXPO_PUBLIC_SUPABASE_URL` pointing at a slow or failing host.

An agent can run locale and time zone variants in tests directly: `TZ=Asia/Almaty npm test`, `LANG=kk_KZ.UTF-8 cargo test`, `TZ=Pacific/Chatham node script.js`.

## 13. Whittaker's attacks (How to Break Software)

Whittaker's 2002 book organises testing as attacks on the four places a program gets or gives information: the user interface, the file system, the operating system and other software. The attack names below are recalled from the book's table of contents (not verified against the full text, which was not read). Use them as prompts.

| Area | Attack |
|---|---|
| Input | Force every error message to appear. Force the defaults (leave everything empty). Explore allowed character sets and data types. Overflow input buffers. Find inputs that interact and test combinations. Repeat the same input many times. |
| Output | Force different outputs for each input. Force invalid outputs. Force properties of an output to change. Force the screen to refresh. |
| Data | Use a variety of initial conditions. Force a data structure to hold too many or too few values. Find other ways to change internal data constraints. |
| Computation | Invalid operand and operator combinations. Force a function to call itself recursively. Force results too large or too small. Find features that share data or interact poorly. |
| File system | Fill the file system. Make the medium busy or unavailable. Damage the medium. Invalid file names. Vary access permissions. Vary or corrupt file contents. |
| Software and OS interfaces | Make the dependencies fail: missing libraries, failing calls, low memory, network errors. |

**Worked example, a Rust CLI `tool import`:** force every error message (`rg -n 'bail!|anyhow!|eprintln!' src` lists them; write one input per message), repeat the same import ten times (idempotent?), import a file on a full tmpfs, import a file with no read permission (`chmod 000`), import a file truncated in the middle of a UTF-8 sequence.

The "force every error message" attack is the most productive for an agent: the list of messages is in the code, and each one is a test that error handling works, the message is clear, and the program recovers.

## 14. Whittaker's tours (Exploratory Software Testing)

Whittaker (2009, first described in his Microsoft blog "The touring test", February 2009) uses a tourism metaphor: the product is a city with districts, and each tour is a focused route through it. The blog post names Supermodel, Money, Intellectual, Garbage collector's, Competitor's, Museum, After hours, FedEx, Prior version, Guidebook, Saboteur, TOGOF and Rained out. The other tours below are from the book and are recalled, not checked against the full text. What the tester does on each:

| Tour | What you do | Worked example |
|---|---|---|
| Guidebook | Follow the user manual or onboarding exactly and check it is true | Shop: follow the README "Getting started" literally on a clean machine |
| Money | Test the features that sell the product, the ones in demos and the store listing | Habit: streaks and the widget, because the listing screenshots show them |
| Landmark | Pick key features and visit them in different orders | Habit: create, tick, stats, export, in four different orders |
| Intellectual | Ask the software the hardest questions: the most complex inputs | Shop: a cart with 99 items, 3 coupons, 2 currencies |
| FedEx | Follow data through the system (section 11) | |
| Garbage collector's | Visit every screen or command once by the shortest route, checking the obvious; also after a fix, sweep the neighbours | A script that hits every route and checks for 200 and no console errors |
| Bad neighbourhood | Go where bugs were found before; bugs cluster | `git log --oneline --grep=fix -- src/sync` shows the sync module had 9 fixes: spend a session there |
| Museum | Test legacy code and old data | Open a backup written by v1.0 |
| Prior version | Check that what the old version did still works | Run the old test plan against the new build |
| Supermodel | Look only at the surface: layout, alignment, text | Hand to the owner as visual checks |
| Back alley | Use the least used features | Settings, export, account deletion |
| All nighter / After hours | Keep it running a long time; what happens to background jobs, memory, sessions | Run the app's sync loop for an hour in a script and watch memory |
| Saboteur | Take away resources it needs: network, disk, permissions | Revoke notification permission, fill disk |
| Antisocial | Do the opposite of what is expected, enter the wrong input on purpose | Cancel every dialog, go back at every step |
| Obsessive compulsive | Do the same thing over and over | Tick and untick 100 times; does the streak drift? |
| Collector's | Try to make every possible output appear | Every error state, every empty state, every toast |
| Rained out | Start an operation and cancel it at different points | Cancel an upload at 0, 50 and 99 percent |
| Couch potato | Do as little as possible, accept all defaults | Sign up and press Next on every screen |
| Competitor's | Compare with a competing product | |

The value of tours for an agent is vocabulary: a charter can say "Explore sync with the saboteur and rained out tours to discover data loss".

## 15. Checks

- [ ] An SFDPOT list exists for the area under test, with at least one line per letter.
- [ ] At least one charter came from each of: Data (D), Time (T) and Operations (O, disfavored use).
- [ ] Count (0, 1, many) and Goldilocks (boundaries from the schema and types) were applied to every input and collection touched.
- [ ] CRUD was applied to every entity touched, including read after delete and delete twice.
- [ ] At least one interruption and one multi user or concurrency case was tried, or handed to the owner.
- [ ] One piece of data was followed end to end through every interface it passes (UI, API, DB, export, email).
- [ ] Every error message in the changed code was forced at least once (`rg` for the message sites).
- [ ] Every bug names a HICCUPPS oracle.
- [ ] The quality criteria list was reviewed and untouched categories are named in the report.
