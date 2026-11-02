# Exploratory testing

This folder is the thinking tester. Scripted checks prove that what someone thought of still works. Exploratory testing finds what nobody thought of: the input that crashes the parser, the second tab that overwrites the first, the Kazakh name that the font cannot draw. This master file says what exploratory testing is, how to run it as chartered, time boxed sessions, how an AI agent explores when it may not look at a screen, and the report it hands back. The other files in the folder hold the heuristics, the input catalogue, i18n and accessibility testing, bug reports and the handoff to a human.

## Contents

1. What exploratory testing is
2. The rules that matter most
3. Charters
4. Session based test management, adapted for an agent
5. How an agent explores without a screen
6. Oracles: how you know it is a bug
7. The session report
8. Files in this folder
9. Checks

## 1. What exploratory testing is

Cem Kaner coined the term in 1984. The definition he and others drafted after the 2006 Exploratory Testing Research Summit (posted on kaner.com) reads: "a style of software testing that emphasizes the personal freedom and responsibility of the individual tester to continually optimize the value of her work by treating test-related learning, test design, test execution, and test result interpretation as mutually supportive activities that run in parallel throughout the project". The short form: you learn, design and run tests at the same time, and each result changes the next test.

James Bach and Michael Bolton went further in "Exploratory Testing 3.0" (2015): all real testing is exploratory, and scripting is a technique used inside it. Their definition: "Testing is the process of evaluating a product by learning about it through exploration and experimentation". They separate **checking** (an algorithmic comparison of output against an expectation, which a machine can do fully) from **testing** (the whole human or agent process of questioning, modelling, observing and judging, which includes checks). A test suite is a set of checks. This folder is about the rest.

Elisabeth Hendrickson ("Explore It!", 2013) gives the working form: write a charter, explore it in a time box, take notes, report what you found. Her point that matters most for an agent: "A good charter is a prompt: it suggests sources of inspiration without dictating precise actions or outcomes."

Exploratory testing does not replace automated checks. It feeds them: every bug found by exploring becomes a regression test (see `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md`, section 3, failing test first).

## 2. The rules that matter most

| # | Rule | Why | Evidence |
|---|---|---|---|
| E1 | Read the user's CLAUDE.md and the project's rules before the first test. If they forbid browsers, emulator input or screenshots, explore through code, scripts, APIs, logs and the database, and hand visual checks to the owner ([human-check-handoff.md](human-check-handoff.md)). | The owner's rules beat any testing habit. A forbidden tool used once costs more trust than a found bug earns. | house rule |
| E2 | Start every session from a written charter: `Explore <target> with <resources> to discover <information>`. | Without a target you wander; without "to discover" you cannot tell when you are done. | moderate (Hendrickson) |
| E3 | Time box sessions: 30 to 90 minutes of agent work, or a budget of about 40 tool calls. Stop, write the report, then pick the next charter. | Bounded sessions make the work reviewable and stop one rabbit hole eating the day. | moderate (J. Bach 2000) |
| E4 | Build a model of the product before testing it: list its structure, functions, data, interfaces, platform, operations and time (SFDPOT, [heuristics.md](heuristics.md) section 2). | Software is invisible. You only test what your model shows you. | moderate (HTSM v6.3) |
| E5 | Drive the real code. Prefer calling the real function, the real HTTP endpoint, the real CLI binary or the real database over reading code and imagining the result. | Reading code tells you what the author meant; running it tells you what happens. | strong (common practice, Zeller) |
| E6 | Name the oracle for every bug: which spec line, claim, comparable product or consistency rule says this is wrong (HICCUPPS, section 6). | A bug with no oracle is an opinion and gets closed. | moderate (Bolton) |
| E7 | Pull inputs from the catalogue, not from your head: empty, one, many, too big, Unicode, time zones, offline, double submit ([edge-case-catalogue.md](edge-case-catalogue.md)). | Agents, like people, test the happy path they imagine. A list beats imagination. | moderate (Hendrickson cheat sheet) |
| E8 | Write notes as you go, in a session file, with every command you ran and its output summary. | Notes make bugs reproducible and the session reviewable. Memory fails, logs do not. | moderate (J. Bach, Zeller "keep a log") |
| E9 | When something looks wrong, stop exploring and investigate: replicate, isolate, maximise, generalise (RIMGEA, [bug-reports.md](bug-reports.md)). Then go back to the charter. | A vague bug is worse than none. A sharp one gets fixed. | moderate (Kaner) |
| E10 | Separate bugs (product problems) from issues (questions, blockers, missing information about the project). Report both. | Issues are often the more valuable output: "the spec does not say what happens when the account is suspended". | moderate (J. Bach 2000) |
| E11 | Report coverage honestly: what you tested, what you did not, and how deep (level 0 to 3, section 7). Never "everything works". | Test case counts and pass rates mean nothing without context. Silence about gaps reads as coverage. | moderate (Bolton 2017) |
| E12 | Use safety language: "so far", "in the cases I tried", "I did not check". | It stops the reader treating a sample as proof. | moderate (Bolton) |
| E13 | Turn every confirmed bug into a failing automated test or a TODO item before the session ends. | Exploration finds the bug once; a check keeps it found. | strong (regression practice) |

## 3. Charters

### The template

Hendrickson's template has three parts:

```
Explore <target>
with <resources>
to discover <information>
```

- **Target**: one area, feature, requirement, module or flow. Small enough to finish in one or two sessions.
- **Resources**: tools, data, techniques, heuristics, configurations. For an agent: `curl`, a test script, the BLNS file, a second user account, the Postgres shell, a slow network shim.
- **Information**: the kind of problem or question. "whether usernames bypass validation when edited", "how the app behaves when the session expires mid save".

### Good and bad charters

| Charter | Verdict |
|---|---|
| Explore the app with everything to discover bugs | Too broad. You never finish and cannot say what you covered. |
| Enter "abc" in the name field and check it saves | Too narrow. That is a test case, not a charter. |
| Explore profile editing with the BLNS strings and the Kazakh letter set to discover input that is stored, displayed or searched incorrectly | Good. One area, named resources, a kind of information. |
| Explore order checkout with two sessions of the same user to discover double charges and lost updates | Good. Names the risk. |
| Explore the CLI `import` command with empty, huge, non UTF-8 and read only files to discover crashes and silent data loss | Good. |

### Where charters come from

Hendrickson lists the sources; an agent can mine each one without asking anyone:

1. **The spec and the task**: every requirement, every "should", every ambiguous word. When the spec says "all fields are editable", charter the field nobody thought of (the username).
2. **Questions that show uncertainty**: "I'll have to think about that" in a spec or chat means a charter. Interactions between a new feature and existing ones (suspended accounts, privacy settings) are the classic case.
3. **Implicit expectations**: performance, security model, data integrity, accessibility. Nobody writes "must not take a minute" but it must not.
4. **Existing artifacts**: the bug tracker, TODO.md, git log of fixes (`git log --oneline --grep=fix`), comments like `// don't touch, it works`, support messages, crash logs.
5. **Hotspots**: files changed most often (`git log --format= --name-only | sort | uniq -c | sort -rn | head -20`). Bugs cluster.
6. **Discoveries during a session**: every "I want to look at that too" becomes a new charter in the notes, not a detour.

Ask the owner to confirm the top charters when the risk ranking is unclear: "If users could put their accounts into an unusable state, would you want to know?" Information nobody will act on is waste (Hendrickson).

### The daily-use charter (every product with a daily user)

Play one realistic day and week as the brief's user, then do the 3 most repeated tasks 10 times in a row, keyboard first. Time tracker example: enter yesterday 9:30 to 11 with loose input (930, gestern, 1,5, 90m), step back one week and forward again, find what is overdue and by how many days, stop a timer forgotten overnight and fix its end, mark an invoice paid with its date, export last month. Admin example: delete a spam signup, sign out.

Count fields, clicks and keystrokes per repetition. Every step that is impossible, needs more than one screen, hides the number the user needs, refuses a format the user would type, or repeats an input that could be defaulted is a finding of type UX gap (minor or major) handed to kwx-designer.

Run it through rendered component tests, API or IPC calls and the CLI; never inject input into the user's desktop, a browser or a device. What needs real eyes and hands goes on the owner's list (`human-check-handoff.md`).

Why: in the kwx trial (2026-11-01) the no-skills arm won on daily-use features no spec test checked: period navigation, a payment date, the forgotten timer, duration formats, admin delete and logout.

## 4. Session based test management, adapted for an agent

Jonathan and James Bach built session based test management (SBTM) in 2000 to make exploratory work reviewable. A session is "an uninterrupted block of reviewable, chartered test effort". Their sessions were about 90 minutes; an agent's are measured in tool calls.

### Session sheet

Write one file per session (in the scratchpad, or `test-notes/` if the owner wants them kept):

```markdown
# Session S3: profile editing, Unicode input
Charter: Explore profile editing with BLNS and Kazakh letters to discover input stored, shown or searched wrongly
Start: 2026-10-31 14:10  Duration: short (about 25 tool calls)
Build: main @ 4f2c1a9, local Supabase
Task breakdown: design and run 60%, bug investigation 30%, setup 10%
Charter vs opportunity: 80 / 20

## Test notes
- PATCH /profile with "Әлия Нұрғали" -> 200, stored NFC, search "алия" finds 0 rows (expected 1?) see B1
- 300 char name -> 200, DB column is varchar(255): stored truncated silently, see B2
- "\u202Eabc" (RTL override, sent as JSON escape) -> stored, list page renders reversed text (not checked visually, H1)

## Bugs
- B1 Search ignores case for Cyrillic only in ASCII range ...
- B2 Names over 255 chars are truncated without an error ...

## Issues
- I1 Spec does not say whether names are unique.
- I2 Could not run the web UI (browser forbidden by user rules), handed to owner as H1.

## Coverage
profile.name: level 2. profile.avatar: level 0 (not touched).
```

The parts come from J. Bach's session sheet: charter, tester, start, task breakdown (test design and execution, bug investigation, setup), data files, test notes, bugs, issues. Keep the "charter vs opportunity" split: it is fine to leave the charter when you find something important, as long as the sheet says so.

### Debrief: PROOF

At the end of a session, answer the five PROOF questions in the report (J. Bach's debrief agenda):

- **Past**: what happened during the session?
- **Results**: what was achieved (bugs, issues, coverage)?
- **Obstacles**: what got in the way (rules, missing data, flaky env)?
- **Outlook**: what still needs to be done (next charters)?
- **Feelings**: for an agent, confidence: how sure are you, and where is it thin?

### Rules from the SBTM paper that transfer

- If the charter cannot be fulfilled (environment broken, no data), abort the session and start a different one. Report it as an issue.
- If the session spent most of its time on opportunity, rewrite the charter to match what was done. The original charter goes back in the queue.
- Keep a queue ("the hopper") of todo charters, ranked by risk. Work from the top.

## 5. How an agent explores without a screen

Many owners forbid the agent to open a browser, inject input into an emulator, or take screenshots (check the user's CLAUDE.md). The agent still has more reach than a human clicking a UI. Use these, in roughly this order:

In the table, `\|` inside a command is Markdown escaping for the table: type a plain `|` when you run it.

| Channel | What it finds | Examples |
|---|---|---|
| Read the code path end to end | Missing validation, unhandled branches, inconsistent rules between create and update, error swallowing | Trace one input from UI handler to DB column. List every place it is checked or transformed. |
| Call the real function from a script | Logic bugs at boundaries, Unicode and number handling | `node -e "import('./src/lib/price.js').then(m => console.log(m.format(0.1+0.2)))"`, `cargo test -- --nocapture`, a Python one liner over the module |
| Hit the real API | Validation, auth, status codes, race conditions, idempotency | `curl -sS -X POST localhost:3000/api/orders -H 'content-type: application/json' -d @order.json -w '%{http_code}\n'`; two `curl` in parallel with `&` to probe double submit |
| Query the database | What really got stored: truncation, normalisation, duplicates, orphan rows | `psql "$DATABASE_URL" -c "select id, name, length(name), name = normalize(name, NFC) from profiles order by id desc limit 5"` |
| Read the logs | Swallowed errors, retries, slow queries, warnings during a flow | `journalctl --user -u app -n 100`, Quickshell or Expo logs, server stdout |
| Run the CLI or TUI binary | Exit codes, stdin edge cases, signals, terminal size | `printf '' \| ./target/release/tool import -; echo "exit=$?"`, `timeout -s INT 1 ./tool watch` |
| Render to text or a file | Layout facts without looking: lengths, overflow, missing glyphs | Count characters against a fixed width in code; `fc-list ':charset=4d9' family` for glyph coverage; static HTML through a validator |
| Run the automated a11y and lint tools the project has | Missing labels, roles, contrast in code tokens | `npx eslint` with jsx-a11y, axe in CI, Android lint |
| Hand the visual and tactile part to the owner | Anything that needs eyes, a finger or a screen reader | A checklist of at most about 10 lines ([human-check-handoff.md](human-check-handoff.md)) |

Practical rules:

- **Verify the build is the one you think it is.** Print the version, commit or a timestamp before testing. Many "fixed" bugs were tested against the old binary.
- **Use a disposable environment.** A local database, a test Supabase project, a temp directory. Never explore against production data unless the owner says so, and never send real emails or payments.
- **Write throwaway drivers in the scratchpad, not in the repo.** If a driver finds a bug, turn its core into a proper test in the repo.
- **Do not trust your reading of a UI.** If you predict "this label overflows", say it is a prediction from code (font size times characters against the box) and put it on the owner's checklist.
- **Watch for side effects you did not ask for**: files created, rows written, network calls made. `git status`, `ls -la`, row counts before and after.

## 6. Oracles: how you know it is a bug

An oracle is "a means of recognizing a problem when it happens during testing" (Bolton). Oracles are heuristic: they can be wrong in both directions. Name one in every bug report.

The main sources, from Bolton's FEW HICCUPPS (full list with examples in [heuristics.md](heuristics.md) section 3):

- **Claims**: the spec, the task, README, docs, UI text, the commit message.
- **Product**: other parts of the same product behave differently (create validates, update does not).
- **History**: the previous version did it right.
- **Comparable products**: the platform convention, a well known app.
- **User desires**: what a reasonable user wants, even if nobody wrote it.
- **Purpose**: what the feature is for.
- **Statutes and standards**: WCAG, GDPR, RFC 5322, platform guidelines.
- **World**: dates, money, names and physics work the way they do in reality.

Precedence when oracles disagree: an explicit claim from the owner beats everything; then standards and laws; then consistency inside the product; then comparable products. When the spec itself looks wrong, report it as an issue, not a bug, and do not change tests to match the code (see `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 2).

## 7. The session report

Every exploratory task ends with this report to the caller (the owner, or kwx-developer and kwx-designer through the main agent). Keep it under one screen where possible.

```markdown
## Exploratory testing report: <feature> (<date>)

Charters run: S1 profile Unicode input (done), S2 two sessions editing (done), S3 offline save (aborted: no network shim, issue I2)
Build: <commit or version>. Environment: <local DB, test project, OS>.

### Bugs (most severe first)
- B1 [major] Editing the same profile in two tabs silently keeps the older save. Oracle: user desire, no lost updates. Repro: test-notes/S2.md steps 1 to 5. Failing test added: tests/profile.concurrency.test.ts (red).
- B2 [minor] ...

### Issues (questions and blockers)
- I1 Spec does not say if names must be unique. Need a decision.

### Coverage
| Area | Depth | Notes |
|---|---|---|
| profile.name input | 2 | BLNS, Kazakh, RTL, length. Visual rendering not seen. |
| profile two sessions | 2 | API level only |
| avatar upload | 0 | not touched |

### Daily use
| Task (10 repetitions) | Fields | Clicks | Keystrokes | Friction (UX gap id) |
|---|---|---|---|---|
| enter yesterday 9:30 to 11 | 3 | 4 | 14 | U1 [minor] "1,5" refused as a duration |
| mark an invoice paid | 1 | 3 | 0 | U2 [major] no payment date field |

### Handed to the owner
6 visual checks, see the checklist below (or at <path>).

### Confidence
So far, in the cases tried, name input is safe from injection and stored correctly. Thin areas: rendering of RTL and long names (not seen), mobile keyboard input (not run).
```

Coverage depth uses Bolton's levels: **0** we know the area exists, nothing more; **1** smoke and reconnaissance; **2** core and critical aspects tested with focused tests on the main quality criteria; **3** deep, harsh, varied testing, a remaining problem would be a surprise.

Do not report test case counts or pass rates as a measure of quality. They hide what was not tested.

## 8. Files in this folder

| File | Read when |
|---|---|
| [heuristics.md](heuristics.md) | Planning what to test: SFDPOT, HICCUPPS, CRUD, Goldilocks, zero one many, interruptions, follow the data, tours, the HTSM |
| [edge-case-catalogue.md](edge-case-catalogue.md) | Choosing concrete inputs: strings, numbers, dates, names, files, lists, network, concurrency, permissions, state |
| [i18n-and-localisation-testing.md](i18n-and-localisation-testing.md) | The product shows text, dates, numbers or money in more than one language, or users type Cyrillic, Kazakh or RTL text |
| [accessibility-testing.md](accessibility-testing.md) | Any UI change: what WCAG 2.2 AA asks, manual checks automation misses, screen reader scripts |
| [bug-reports.md](bug-reports.md) | Writing up a bug, minimising a repro, handing bugs to kwx-developer or kwx-designer, the TODO.md BUGS format |
| [human-check-handoff.md](human-check-handoff.md) | Something can only be confirmed by eyes or hands and the agent may not look: write the owner's checklist |

Related elsewhere: `~/.claude/skills/kwx-developer/reliability/testing-strategy.md` (the automated test mix), `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` (never weaken a test to pass), `web/accessibility-testing.md` and `mobile/mobile-accessibility-testing.md` in this skill.

## 9. Checks

- [ ] The user's CLAUDE.md and project rules were read; no forbidden tool was used (browser, emulator input, screenshots, pointer).
- [ ] Every session had a written charter with target, resources and information.
- [ ] A product with a daily user has the daily-use charter in the plan with at least 5 steps, its counts per task in the report, and its UX gaps in the bug list.
- [ ] A product model (SFDPOT list) exists for the area under test.
- [ ] The build under test was identified (commit, version or timestamp printed).
- [ ] Inputs came from [edge-case-catalogue.md](edge-case-catalogue.md), including at least: empty, one, many, too long, Unicode (Cyrillic and Kazakh), and one concurrency or interruption case.
- [ ] Every bug names its oracle and has a minimal repro.
- [ ] Every confirmed bug became a failing test or a TODO.md BUGS item.
- [ ] Issues (questions, blockers) are listed separately from bugs.
- [ ] The report states coverage per area with depth 0 to 3 and names what was not tested.
- [ ] Visual and tactile checks went to the owner as a short checklist, not attempted.
- [ ] No production data touched, no real emails, payments or pushes sent.
- [ ] Session notes and the report contain no em or en dashes.
