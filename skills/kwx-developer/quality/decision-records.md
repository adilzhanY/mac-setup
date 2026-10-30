# Decision records: write down what was decided so it is never asked again

When the owner says "this is intentional, keep it", that answer must outlive the conversation. It goes into `DECISIONS.md` at the project root, in a form the next audit can match mechanically, and, where a tool would flag it again, into that tool's config with the decision id. An agent that asks the same question twice wastes the owner's time and teaches them to ignore the audit.

## Contents

1. Three places a decision lives
2. Where the file is, and respecting the format already there
3. The entry format
4. Examples
5. When to write a full ADR instead
6. Reading decisions before an audit (the do-not-flag list)
7. Recording outcome (c), step by step
8. Changing a decision later
9. Writing rules and anti-patterns
10. Checks

## 1. Three places a decision lives

| Place | Holds | Read by |
|---|---|---|
| `DECISIONS.md` | Every decision with its why, scope and audit key | The agent before every audit and every design change; the owner |
| Tool config (`knip.json`, `.dependency-cruiser.cjs`, ast-grep `ignores`, `[lints.clippy]`, `[package.metadata.cargo-machete]`) | The machine form of an exception, with the D-id in a comment | The tools, so they stop reporting it |
| Inline marker at the exact spot | A one place exception: `#[expect(clippy::x, reason = "D-14 ...")]`, `// eslint-disable-next-line rule -- D-07 ...`, `/** @lintignore D-09 */` | Readers of that file, and the tools |

The D-id ties them together: `grep -rn "D-07" .` finds the record and every place it is enforced. A decision only in chat, or only in a tool config without a why, does not count.

## 2. Where the file is, and the format already there

1. Look first: `ls DECISIONS.md docs/decisions docs/adr doc/adr doc/arch 2>/dev/null`, and grep `CLAUDE.md`/`AGENTS.md` for "decision".
2. If a `DECISIONS.md` exists, keep its style, numbering and order. This user's repos already use three styles, all valid:
   - `## D-01 Title` with **Accepted** / **Proposed** / **Replaced by D-xx**, and a "Rejected:" paragraph (sahna).
   - `## 1. Title`, a date line, then **Context** / **Decision** / **Rejected** / **Consequences**, "Superseded by #N" (orda).
   - `## YYYY-MM-DD Title`, a review log of where the human overruled the agent (bauwerk).
   Add the audit fields of section 3 as extra lines inside new entries. Never reformat or renumber old entries.
3. If none exists, create `DECISIONS.md` at the root with this header, and add one line to `CLAUDE.md` (or `AGENTS.md`): "Read DECISIONS.md before changing structure or auditing; never re-flag an Accepted decision."

```markdown
# Decisions

Every decision that shapes this project, why it was made, and what was rejected. Newest at the bottom, numbered D-01, D-02, ... and never renumbered. Never edit or delete an entry: when a decision changes, write a new one and mark the old one **Replaced by D-xx**. Entries with an `Audit:` line are intentional exceptions; the codebase audit reads them and never reports them again.

Status is **Accepted** (in force), **Proposed** (planned, open to change) or **Replaced by D-xx**.
```

## 3. The entry format

```markdown
## D-07 Short noun phrase naming the decision

2026-10-30. **Accepted.**
Audit: export-style:lib
Scope: `lib/cropUtils.ts`
Keep: the default export of `getCroppedImg`.
Why: one or more full sentences in the owner's terms: the force that makes this right for THIS project.
Rejected: the alternative and why it lost (one line each).
Revisit when: a concrete trigger (optional).
Enforced by: `ignores: [lib/cropUtils.ts]` in `rules/lib-named.yml` (or "nothing, reviewed by hand").
```

Field rules:

- **Title**: a short noun phrase (Nygard). "Default export kept in lib/cropUtils.ts", not "Exports".
- **Date and status** on the first line. Date is the day the owner decided.
- **Audit**: one or more finding keys from the fixed `kind:area` vocabulary in [codebase-audit-tools.md](codebase-audit-tools.md) section 10 (`export-style`, `naming`, `import-style`, `duplicate`, `layering`, `cycle`, `dead-code`, `unused-dep`, `error-handling`, `untested-risk`, `hotspot`, `coupling`, `lint`). Present only on decisions that suppress a finding. This line is what makes matching mechanical.
- **Scope**: path globs, as narrow as the owner's answer. "This file" is `lib/cropUtils.ts`, not `lib/**`. A whole-project convention is `**`.
- **Keep**: what stays exactly as it is. One sentence.
- **Why**: the reason the owner gave, in plain words. If the owner gave no reason, write "Owner's call, no reason given" rather than inventing one. An invented why will be argued with later.
- **Rejected**: options considered and not taken. Skip for a pure keep-as-is exception.
- **Revisit when**: a checkable trigger ("when the crop dialog is rewritten", "when the API gets a second client", "above 10k users"). No vague "later".
- **Enforced by**: where the machine form lives, or "nothing".

Keep each entry under ~15 lines. Longer means it is an architecture decision: section 5.

## 4. Examples

Convention exception (from an audit, outcome c):

```markdown
## D-07 Default export kept in lib/cropUtils.ts

2026-10-30. **Accepted.**
Audit: export-style:lib
Scope: `lib/cropUtils.ts`
Keep: `export default async function getCroppedImg`.
Why: the file is a copy of react-easy-crop's documented helper and is replaced as a whole when the library updates it. The other 41 files in lib/ stay named-export only.
Revisit when: the crop dialog is rewritten.
Enforced by: `ignores` in `rules/lib-named.yml` (ast-grep).
```

Whole project convention (decides the majority, so the minority becomes a finding):

```markdown
## D-08 anyhow everywhere, no thiserror

2026-10-30. **Accepted.**
Audit: error-handling:**
Scope: `**`
Keep: every crate returns `anyhow::Result`, including library crates.
Why: all crates are internal to one app and no caller matches on error kinds; errors are shown to the user as text. Typed errors would add an enum per crate with no reader.
Rejected: thiserror enums in library crates (the usual Rust convention; right when a crate is published or callers branch on the error).
Revisit when: a crate is published or a caller needs to branch on an error kind.
Enforced by: nothing, reviewed by hand.
```

Lint group exception:

```markdown
## D-12 Lossy float casts allowed in the renderer

2026-10-30. **Accepted.**
Audit: lint:clippy::cast_precision_loss, lint:clippy::cast_possible_truncation
Scope: `crates/sahna-render/**`, `crates/sahna-core/**`
Keep: `as f32` / `as u32` casts on pixel and time values.
Why: values are bounded by frame sizes and durations far below f32's exact integer range (2^24); checked conversions on every pixel would cost speed for no safety.
Enforced by: `[workspace.lints.clippy]` in `Cargo.toml`, `cast_precision_loss = "allow"  # D-12`.
```

Layering decision that CREATES findings (code violating it is reported, with priority):

```markdown
## D-05 Geometry is pure and Three.js free

2026-09-05. **Accepted.**
Scope: `src/geometry/**`
Why: geometry is unit tested in Vitest without a WebGL context; the correctness argument must not depend on rendering.
Enforced by: `geometry-is-pure` rule in `.dependency-cruiser.cjs`.
```

No `Audit:` line, because it suppresses nothing. A violation of it is a finding that quotes the decision: "`src/geometry/x.ts` imports `three`, which D-05 forbids".

## 5. When to write a full ADR instead

A `DECISIONS.md` entry covers conventions and exceptions. Write a full Architecture Decision Record when at least one holds:

- It is costly to reverse: database, sync model (last write wins vs CRDT), auth provider, framework, process boundaries, public API shape, data format on disk. Zimmermann: decisions costly to undo "cannot wait until sprint n, with n larger than 3".
- There are two or more viable options with real trade-offs that the owner should see side by side.
- The explanation needs more than ~15 lines, or includes measurements.
- Nygard's test: it affects structure, non-functional characteristics (speed, safety, cost), dependencies, interfaces, or construction techniques.

Do NOT write an ADR for: style conventions, one-off exceptions, temporary workarounds, experiments, anything already fixed by a standard or tool config ([joelparkerhenderson/architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record)).

Location and naming (MADR 4.0.0): `docs/decisions/NNNN-title-with-dashes.md`, numbered consecutively, never reused. Add a one-line entry in `DECISIONS.md` pointing to it so there is one index: `## D-15 Plain pg over an ORM. See docs/decisions/0003-plain-pg-over-orm.md`.

Template (MADR minimal plus Nygard's status and consequences; "one or two pages long" at most):

```markdown
---
status: accepted            # proposed | accepted | rejected | deprecated | superseded by 0007
date: 2026-10-30
decision-makers: owner
---
# Plain pg over an ORM

## Context and Problem Statement
Two to five sentences: the forces, including the ones pulling the other way. Facts, value neutral.

## Considered Options
* plain `pg` with SQL migrations
* Prisma
* TypeORM

## Decision Outcome
Chosen option: "plain pg", because the schema is two tables and the one query that matters (`UPDATE ... WHERE id = $1 AND version = $2`) is the kind an ORM hides.

### Consequences
* Good, because every query is visible and testable against a real Postgres.
* Bad, because migrations and row mapping are written by hand.

### Confirmation
How compliance is checked: no `@prisma/client` or `typeorm` in package.json; `knip` reports unlisted deps.
```

One sentence form for small but real decisions (Zimmermann's Y-statement): "In the context of <use case>, facing <concern>, we decided for <option> and against <other options>, to achieve <quality>, accepting <downside>." Split into two sentences if it reads badly.

## 6. Reading decisions before an audit

Do this before running any tool in [codebase-audit-tools.md](codebase-audit-tools.md).

1. Find every record: `DECISIONS.md`, `docs/decisions/*.md`, `docs/adr/*.md`, plus "do not" and "always" lines in `CLAUDE.md` and `AGENTS.md`. Read each file completely; a 300 line `DECISIONS.md` is read in full, never with `head`.
2. Keep only entries in force: status Accepted (or no status in a log style file). Skip Proposed, Rejected, Replaced, Superseded, Deprecated.
3. Build the do-not-flag list from entries with an `Audit:` line:

```bash
# key, scope and id of every machine-readable exception
awk '/^## /{id=$2; a=""; off=0} /Replaced by|Superseded by|\*\*Proposed|\*\*Rejected/{off=1}
     /^Audit:/{a=$0} /^Scope:/ && a && !off {print id"\t"a"\t"$0}' DECISIONS.md
# D-07  Audit: export-style:lib  Scope: `lib/cropUtils.ts`
```

4. For older entries with no `Audit:` line, read them and decide which finding kinds they cover. bauwerk's "Plain pg over an ORM" covers any "consider an ORM" suggestion; "Room identity by centroid" covers any "match by id instead" suggestion. When unsure whether an old entry covers a finding, treat it as covered and mention the entry in the report instead of asking.
5. Match each confirmed finding:
   - Same kind and the finding's path inside the scope globs: drop it. Do not mention it, do not ask.
   - Same kind, path outside the scope: report it, and say which decision is related ("D-07 covers only `lib/cropUtils.ts`; `lib/format.ts` is a new default export"). Never widen a scope on your own.
   - The finding is a VIOLATION of a decision (code breaks D-05): report it with the decision quoted, priority one level above what it would otherwise get. The decision was the owner's; drift from it is a regression.
   - A `Revisit when:` trigger has happened (the crop dialog was rewritten): ask once, quoting the entry: "D-07 said revisit when the crop dialog is rewritten. It was rewritten on 10-28. Keep the exception or switch to a named export?"
6. Also drop findings that match an open `TODO.md` item ([tech-debt-and-todo.md](tech-debt-and-todo.md) section 5): already decided as "later".

## 7. Recording outcome (c), step by step

When the owner answers "intentional, keep it":

1. Write the entry (section 3) with the next free number, at the bottom of `DECISIONS.md`. Use the owner's reason; ask one short follow-up ("Why should it stay? One sentence is enough.") only if the reason is needed to set the scope correctly.
2. Set the scope to exactly what the owner said. "Keep it" about one file is that file. If the owner says "this whole folder does it differently on purpose", the scope is the folder.
3. Encode it where a tool would report it again, with the D-id:

| Tool | Where | Example |
|---|---|---|
| ESLint | inline, reason after ` -- ` | `// eslint-disable-next-line import-x/no-default-export -- D-07 copy of the library helper` |
| ESLint | config override for a scope | `{ files: ["lib/cropUtils.ts"], rules: { "import-x/no-default-export": "off" } } // D-07` |
| knip | JSDoc tag on the export plus `"tags": ["-lintignore"]` | `/** @lintignore D-09 public API */ export function ...` |
| dependency-cruiser | `pathNot` on the rule, comment with the id | `pathNot: "^src/legacy/" // D-11` |
| ast-grep | rule `ignores` | `ignores: [ "lib/cropUtils.ts" ]  # D-07` |
| clippy | `[lints.clippy]` or `#[expect(..., reason = "D-12 ...")]` | `cast_precision_loss = "allow"  # D-12` |
| cargo-machete | `[package.metadata.cargo-machete] ignored = ["crate"]` | `ignored = ["sahna-audio"]  # D-16 used only behind a feature` |

   Prefer `#[expect]` over `#[allow]` in Rust: it warns when the exception is no longer needed.
4. If the project has no tool config for it yet, do not add one just to record the exception (that would be a new tool, which needs a yes). "Enforced by: nothing" is fine.
5. Show the owner the entry in one short block, then continue with the next finding.
6. Commit the `DECISIONS.md` change on its own when the project's rules say to commit (this user's desktop and app repos do: one line message such as "Record D-07: default export kept in cropUtils").

If the owner calls something intentional that is a real risk (a swallowed error on a payment path, a secret in the repo, an injection), say the risk once in one plain sentence before recording, then record it with that risk under "Why" or "Consequences". The owner decides; the record shows they decided knowingly.

## 8. Changing a decision later

- Never edit the text of an Accepted entry and never delete one. History of why matters more than tidiness (Nygard: "we will keep the old one around, but mark it as superseded").
- To change: write a new entry, then change only the old one's status line to `**Replaced by D-21.**` and add `Replaced by D-21` where its tools reference it.
- Small clarifications that do not change the decision: append a dated line at the end of the entry, `Note 2026-11-15: scope also covers lib/cropUtils.test.ts.` Never rewrite the original lines.
- When a decision is replaced, the exceptions it created become findings again: remove the tool exemptions in the same change.

## 9. Writing rules and anti-patterns

- One decision per entry. "Use pg, and also last write wins" is two entries (bauwerk's log combines them; new entries should not).
- Decision sentences in active voice: "We keep", "We use", "lib/ exports by name".
- State the forces, including the ones against. A why with only upsides is Zimmermann's "Fairy Tale" ("we chose a load balancer because it balances load").
- Never list an option nobody would pick to make the choice look good ("Dummy Alternative").
- Never hide the cost ("Free Lunch Coupon"): if the exception means a new contributor will trip over a mixed style, say so.
- No marketing words, no "best practice" as a reason. "Best practice" is not a force; the project's situation is.
- No speculative scope. Record what the owner decided, not what you think they would also accept.
- Dates are absolute (`2026-10-30`), never "today" or "last week".

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Decisions read before tools | Audit notes name the decision files read and the count of do-not-flag entries | Read the audit log |
| No re-flagged decision | No reported finding matches an Accepted entry's `Audit:` key and `Scope:` | Run the awk in section 6 and compare keys and paths with the findings list |
| Every intentional answer recorded | Each finding the owner marked (c) has a D-entry with Audit, Scope, Keep, Why | `grep -c '^Audit:' DECISIONS.md` grew by the number of (c) answers |
| Ids unique and never reused | No duplicate D-number | `grep -oE '^## D-[0-9]+' DECISIONS.md \| sort \| uniq -d` is empty |
| Tool exemptions cite the id | Every exemption added in this session contains its D-id | `git diff \| grep -E '^\+.*(eslint-disable\|@lintignore\|expect\(\|allow\|ignores\|ignored)'` lines all contain `D-` |
| No edited history | Old entries unchanged except status lines and appended `Note` lines | `git diff DECISIONS.md` shows only additions, or `-`/`+` pairs on a status line |
| Scope not widened | Each new Scope equals what the owner said | Compare with the owner's answer in the conversation |
| ADR only when warranted | Each new file in `docs/decisions/` meets a section 5 criterion and has a pointer line in DECISIONS.md | Read both |
| Header rule in CLAUDE.md | Projects with a DECISIONS.md tell agents to read it | `grep -n DECISIONS CLAUDE.md AGENTS.md` |
