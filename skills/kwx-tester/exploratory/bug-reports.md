# Bug reports

A bug report is a tool to get a decision: fix it, defer it, or accept it. Cem Kaner's line in "Bug Advocacy" (2002): "The best tester isn't the one who finds the most bugs or who embarrasses the most programmers. The best tester is the one who gets the most bugs fixed", and a report also succeeds "if it enables an informed business decision", even a decision not to fix. This file covers the anatomy of a great report, how to investigate a failure before writing it (RIMGEA, follow up testing, non reproducible bugs), how to shrink a repro to the minimum (delta debugging), severity and priority, and the exact formats kwx-tester uses to hand bugs to kwx-developer and kwx-designer and to write them into a project's TODO.md.

## Contents

1. The rules that matter most
2. Anatomy of a great report
3. Investigate before you write: RIMGEA
4. Follow up testing: make it more serious, more general
5. Non reproducible and intermittent bugs
6. Minimal reproduction and delta debugging
7. Severity and priority
8. Handoff to kwx-developer and kwx-designer
9. The BUGS section in TODO.md
10. Checks

## 1. The rules that matter most

| # | Rule | Why | Evidence |
|---|---|---|---|
| B1 | One failure per report. If you see two, write two and cross reference them. | Combined reports get vague titles, get long, and one half gets fixed while the other is forgotten. | moderate (Kaner) |
| B2 | Write the title as `<what fails> when <condition>`, specific enough that the reader can picture the failure. | The title is often the only line people read. "Checkout broken" gets ignored. | moderate (Kaner, Bolton) |
| B3 | Give numbered steps from a known starting state, the shortest that still fail. | A developer who cannot reproduce it closes it. | moderate (Kaner) |
| B4 | State expected versus actual, and the source of "expected" (the oracle). | Without an oracle the report is an opinion. | moderate (Bolton) |
| B5 | Never call a bug reproducible unless you reproduced it. Say "always", "3 of 10 runs", or "once, could not repeat" with what you tried. | Honest reproducibility saves hours and protects credibility. | moderate (Kaner) |
| B6 | Reproduce on a second configuration before reporting (another locale, zone, OS version, a clean DB). | Configuration dependent bugs are credible only when the dependence is named. | moderate (Kaner) |
| B7 | Minimise: cut steps and input until removing anything makes the failure vanish. | Short repros are fixed faster and expose the cause. | strong (Zeller, delta debugging) |
| B8 | Attach evidence as text: the exact command, request, response, log lines, stack trace, DB row. | Text can be searched, diffed and replayed; an agent's evidence is text anyway. | moderate |
| B9 | Write neutral facts, no blame and no guesses dressed as facts. Mark guesses: "Suspect: ...". | People resist reports that attack them. | moderate (Kaner: "say it clearly and dispassionately") |
| B10 | Put severity (impact) and priority (when to fix) in separate fields. The tester sets severity; the owner sets priority. | They are different questions; mixing them hides both. | moderate (common practice) |
| B11 | Every confirmed bug gets a failing automated test, or a note saying why it cannot have one yet. | The test proves the fix and stops the regression. | strong (regression practice) |

## 2. Anatomy of a great report

```markdown
### B3. Habit streak resets to 0 when the device time zone changes eastward after 19:00

Severity: major (user visible data loss of a key feature). Priority: owner decides.
Reproducible: always (5 of 5), on two configurations.
Build: main @ 4f2c1a9 (app 1.6.0-dev), local Supabase 2.x.

Steps (from a fresh test user):
1. Create habit "Run" and tick it for 3 consecutive days with device zone Europe/Berlin.
2. On day 3 at 20:00 Berlin time, change the zone to Asia/Almaty (UTC+5).
3. Open the app (or call `computeStreak(ticks, now, "Asia/Almaty")`).

Expected: streak 3. Oracle: Claims, spec "Streaks" section: "a streak counts consecutive local days with a tick".
Actual: streak 0. The stats screen also shows today as unticked.

Evidence:
- Script: test-notes/S4-streak-tz.mjs (12 lines), output:
  computeStreak(...Berlin) = 3, computeStreak(...Almaty) = 0
- Ticks are stored as `date` in UTC (`ticks.day = '2026-10-30'`), compared with local "today" ('2026-10-31' in Almaty at 00:00+05).

Scope (generalised): any move eastward that crosses local midnight; westward moves double count a day (streak 4 after the reverse trip).
Workaround: none for the user.
Suspect (not confirmed): `src/lib/streak.ts:41` builds "today" from local time but the stored day from UTC.
Failing test: tests/streak.timezone.test.ts (red, 2 cases).
```

The parts and why each matters:

| Part | What goes in | Common mistake |
|---|---|---|
| Title | Failure + condition, in user terms | "Bug in streak.ts", "Doesn't work", the fix instead of the problem |
| Severity | Impact, from the scale in section 7 | Inflating everything to critical |
| Reproducible | Always, N of M, once; what you tried | "Reproducible" after one run |
| Build and environment | Commit, version, OS, locale, zone, device, DB state | Missing; the bug turns out to be fixed already |
| Steps | Numbered, from a known state, minimal | Starting mid flow; 20 steps when 3 suffice |
| Expected, with oracle | What should happen and who says so | "Should work correctly" |
| Actual | What happened, exact text of errors | Paraphrased error messages |
| Evidence | Command, request and response, log lines, stack trace, DB rows, minimal script | A screenshot only (agents usually cannot take one, and text is better anyway) |
| Scope | How general: which inputs, configurations, other places | Silent; the fix covers one case of many |
| Workaround | If any; its reasonableness affects priority (Bolton) | Omitted |
| Suspect | Your guess at the cause, clearly labelled | Presented as fact; or a full patch nobody asked for |
| Failing test | Path of the red test | Missing |

Kaner's summary rule: the title should let the reader "visualize the failure", show the limits of the bug (how narrow or broad), and hint at the consequences.

Bolton's checklist for a report ("PEOPLE WORKing"): a **P**roblem you observed, an **E**xample to show it, an **O**racle, **P**olite, **L**iterate (a story about a person and the product), **E**xtrapolation (greatest extent and significance, RIMGEA), and a **W**orkaround. The first three are almost always required.

## 3. Investigate before you write: RIMGEA

Kaner's mnemonic from the Black Box Software Testing (BBST) Bug Advocacy course, with Bolton's glosses:

| Step | Do | Agent action |
|---|---|---|
| **R**eplicate | Make it happen again, from a clean state | Re run the script from a fresh DB or temp dir; run it 5 to 10 times for flakiness |
| **I**solate | Find the critical condition: the step, the input, the setting that triggers it | Remove steps one by one; swap inputs; binary search the input (section 6) |
| **M**aximise | Show the worst plausible consequence: "the biggest, baddest bug it could possibly be" | Keep going after the first symptom: data corruption? crash? security exposure? |
| **G**eneralise | Find where else it happens: other inputs, other screens, mainstream values | Try normal values, not only the extreme one; try sibling endpoints and components |
| **E**xternalise | Consider what happens when the bug gets outside the lab: who is hurt, how much | Count affected users or data; name the user story it breaks |
| **A**nd say it clearly and dispassionately | Write it neutrally | Section 2 format |

Spend a bounded time on this: 5 to 15 tool calls for a normal bug. A crash or data loss deserves more.

## 4. Follow up testing: make it more serious, more general

From Kaner's "Bug Advocacy". When you see a failure, you are looking at a symptom, not the fault. The program is now in a state its author did not expect. Keep going:

**Make it more serious.**

- **Vary your behaviour**: do the failing action again and again (cumulative effect?); do related actions before it; do it faster or slower; interrupt it.
- **Vary options and settings**: different data, different persisted settings, different locale or zone.
- **Vary the configuration**: less memory, slower network, another OS version, a cold start.
- **Check if it is new**: run the previous release or `git stash` and the parent commit. A regression gets priority. Use `git bisect run` with the repro script to find the commit:

```bash
git bisect start HEAD v1.5.0
git bisect run sh -c 'npm run -s build >/dev/null && node test-notes/repro.mjs'   # exit 0 = good, 1 = bad
git bisect reset
```

**Make it more general.**

- **Uncorner the corner case**: you found it with a 10 000 character name; does a 60 character name fail too? If mainstream values fail, report it with those: "a very credible bug report" (Kaner). If only the extreme fails, say exactly where the range starts.
- **Look for configuration dependence**: reproduce in a second environment. If it fails only in one, that difference is the lead.

Write the main report with the shortest repro, then add an "Additional conditions" section for variations (Kaner).

## 5. Non reproducible and intermittent bugs

Always report them; a precise description often lets a developer find the code path. Kaner's advice:

- Write down everything right away, marking what you are sure of and what you are not.
- Note what you did before the failure; the trigger may be a delayed effect (a leak after 20 operations, a corrupted state from an earlier error).
- Search the tracker, TODO.md and git log for similar failures.
- "The fact that a bug is not reproducible is data": a condition you are not controlling matters.

Conditions testers often miss (Kaner's list, adapted): hidden input variables (env vars, feature flags, cached state, a file you thought was deleted), time of day or end of month, first run only (initial state), order of operations, race conditions and timeouts, error handling after an earlier error, corrupted data from an earlier step, a dependency's version, co resident software, load, and typing (or scripting) too slowly or too fast.

Agent techniques for flaky failures:

```bash
# run a test 50 times, count failures
for i in $(seq 50); do npx vitest run tests/sync.test.ts >/dev/null 2>&1 || echo fail; done | wc -l
# shuffle order to find order dependence
npx vitest run --sequence.shuffle
# Rust: repeat one test
for i in $(seq 50); do cargo test -q sync_merges -- --exact >/dev/null 2>&1 || echo fail; done | wc -l
```

Report the rate ("fails 7 of 50 runs"), the seed if the runner prints one, and the conditions that change the rate.

## 6. Minimal reproduction and delta debugging

Andreas Zeller's delta debugging (Zeller and Hildebrandt 2002; "Why Programs Fail" and the free "The Debugging Book", chapter "Reducing Failure-Inducing Inputs") automates "isolate": repeatedly remove chunks of the failing input, keep any smaller input that still fails, and refine the chunk size until no single element can be removed. The result is **1-minimal**: removing any one remaining element makes the failure go away. Best case it needs about log2(n) tests like binary search; worst case about n squared.

Zeller's lessons from that chapter: reducing failure inducing inputs "is helpful for testing and debugging"; delta debugging is "a simple and robust algorithm"; and "precisely specifying failure conditions helps to avoid false diagnoses" (check for the specific error, not "any exception", or the reducer will find a different bug).

Manual version for steps: remove half the steps; if it still fails, keep the cut; if not, restore and try the other half; then smaller groups, then single steps. Kaner's shortcut: watch for the first subtle symptom (an earlier error message, a delay, a flicker in a log) and try going straight from that step to the end.

Automated version for inputs, with the Debugging Book's Python package (from its docs; `pip install debuggingbook`, not run here):

```python
from debuggingbook.DeltaDebugger import DeltaDebugger

def parse_ok(s: str) -> None:
    my_parser(s)          # raises on the bug

with DeltaDebugger() as dd:
    parse_ok(failing_input)
print(dd.min_args())      # {'s': '<minimal failing input>'}
```

A dependency free ddmin you can paste into a scratch script (**verified** on a toy predicate: reduced a 40 character input to the 2 characters that trigger it):

```python
def ddmin(data, fails):
    """Return a 1-minimal sublist of data for which fails(data) is True."""
    n = 2
    while len(data) >= 2:
        chunk = max(1, len(data) // n)
        subsets = [data[i:i + chunk] for i in range(0, len(data), chunk)]
        reduced = False
        for i in range(len(subsets)):
            complement = [x for j, s in enumerate(subsets) if j != i for x in s]
            if fails(complement):
                data, n, reduced = complement, max(n - 1, 2), True
                break
        if not reduced:
            if n >= len(data):
                break
            n = min(n * 2, len(data))
    return data
```

Use it for failing inputs (characters of a string, lines of a file, items of a JSON array, steps of a scripted flow). Other tools: `git bisect` for commits, `creduce` and `cvise` for C-like source files, proptest and fast-check shrink failing generated inputs automatically.

The minimal repro goes into the report and becomes the regression test.

## 7. Severity and priority

**Severity** is how bad the impact is. The tester proposes it from evidence. **Priority** is when to fix it, given everything else; the owner decides, because it depends on release plans and cost. A typo on the landing page can be minor severity and top priority; a crash in a hidden debug menu can be critical severity and low priority.

Severity scale used by kwx-tester:

| Severity | Meaning | Examples |
|---|---|---|
| critical | Data loss or corruption, security or privacy breach, money wrong, crash on a main path, no workaround | User A can read user B's habits; double charge; app crashes on launch for Kazakh locale |
| major | A main feature fails or gives wrong results; a group of users is blocked (including accessibility blockers); workaround is unreasonable | Streak resets on time zone change; submit button unreachable by keyboard |
| minor | Secondary feature wrong, cosmetic issue on a main path, reasonable workaround | Plural "1 habits"; misaligned icon; slow export |
| trivial | Cosmetic, rarely seen | Spacing in an about screen |

Bolton's note: the significance of a problem may be proportional to how reasonable the workaround is. Say what the workaround is and let the owner weigh it.

## 8. Handoff to kwx-developer and kwx-designer

kwx-tester does not fix product code. It hands each bug to the role that owns it, through the main agent:

- **kwx-developer**: logic, data, API, security, performance, crashes, i18n plumbing, missing accessibility names and roles in code.
- **kwx-designer**: layout, visual hierarchy, contrast tokens, target sizes, copy and empty states, motion, anything about how it looks or reads.
- Both, when the fix spans design and code (an error state that is missing entirely).

Handoff block (one per bug, in the report to the main agent):

```markdown
#### BUG B3 -> kwx-developer
Title: Habit streak resets to 0 when the device time zone changes eastward after 19:00
Severity: major. Reproducible: always (5/5), 2 configurations.
Oracle: spec "Streaks": consecutive local days with a tick.
Minimal repro: `node test-notes/S4-streak-tz.mjs` prints 3 then 0 (expected 3 and 3).
Failing test: tests/streak.timezone.test.ts (red). Do not edit the test to pass; if you think it is wrong, flag it.
Scope: eastward moves across local midnight; westward moves double count.
Suspect: src/lib/streak.ts:41 mixes UTC stored day with local today.
Done when: the failing test is green, the full suite passes, and the westward case has a test too.
```

```markdown
#### BUG B7 -> kwx-designer
Title: Primary button text "Сохранить изменения" is cut off at system font 130 percent on 360 dp wide screens
Severity: major. Evidence: predicted from code (owner to confirm, checklist item 2): label 19 chars x ~9.5 px at 16 sp x 1.3 = ~235 px; button fixed width 200 dp, padding 16 each side.
Oracle: WCAG 1.4.4; Product consistency (other buttons wrap).
Where: src/components/PrimaryButton.tsx:22 (width: 200).
Done when: label fits or wraps at 200 percent font scale in ru and kk, owner confirms.
```

Rules for the handoff:

- Include the failing test path and the instruction not to weaken it (kwx-developer's own rule, `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 1).
- Say what "done" means as a check that can be run.
- Predicted visual bugs say "predicted from code" and point to the owner checklist item that confirms them.
- After the fix, kwx-tester re runs the repro and the neighbouring cases (Whittaker's garbage collector's tour around the fix) before closing.

## 9. The BUGS section in TODO.md

When the owner wants bugs recorded in the project (or the bug is not fixed in this task), write them into `TODO.md` following kwx-developer's TODO rules (`~/.claude/skills/kwx-developer/quality/tech-debt-and-todo.md` section 5): read the whole file first, match its heading, numbering, checkbox and wrapping style, and never duplicate.

Default format when the file has no style of its own:

```markdown
## Bugs

### Open

- [ ] **B3. Habit streak resets to 0 when the time zone changes eastward after 19:00** `bug:streak/timezone` [major]
      Repro: `node test-notes/S4-streak-tz.mjs` (or steps in tests/streak.timezone.test.ts). Always, 2 configs. Found 2026-10-31, build 4f2c1a9.
      Oracle: spec "Streaks". Suspect: `src/lib/streak.ts:41`. Failing test: `tests/streak.timezone.test.ts`.
- [ ] **B7. "Сохранить изменения" cut off at 130 percent font scale** `bug:ui/primary-button` [major, needs owner check]
      Predicted from code: 235 px label in a 200 dp button. `src/components/PrimaryButton.tsx:22`. Owner to confirm on device.

### Fixed

- [x] **B1. Search ignores Cyrillic case** `bug:search/case` [major]
      Done: 2026-10-31, `ILIKE` replaced `LIKE` in `search.sql`; test `tests/search.cyrillic.test.ts` green.
```

- Key in backticks: `bug:<area>/<topic>`, so later sessions can `grep -nF 'bug:streak/timezone' TODO.md` before adding.
- Severity in brackets on the title line; priority is the owner's, recorded only if they give one.
- Evidence line with the repro command, reproducibility, date and build.
- Never delete an item; tick it and add a `Done:` note with how the fix was verified.
- A fixed bug that comes back gets a new item `... (regressed, was B3)`.

## 10. Checks

- [ ] Each report covers one failure; related reports cross reference each other.
- [ ] Title is `<failure> when <condition>` in user terms.
- [ ] Steps are numbered, start from a known state, and are minimal (each remaining step is needed).
- [ ] Expected names its oracle; actual quotes exact output.
- [ ] Reproducibility is stated honestly (N of M), with the configurations tried.
- [ ] RIMGEA was applied: replicated, isolated, maximised, generalised, externalised.
- [ ] Evidence is text: command, request and response, logs, DB rows, script path.
- [ ] Severity is set from the scale; priority is left to the owner.
- [ ] A failing test exists for each confirmed bug, or the reason it cannot is written down.
- [ ] Handoff blocks go to the right role with a runnable "done when".
- [ ] TODO.md entries match the file's style, have a `bug:` key, and were checked for duplicates first.
- [ ] No blame words, no guesses presented as facts ("Suspect:" label used).
