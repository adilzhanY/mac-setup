# Snapshot and golden tests

A snapshot (or golden file) test stores an output once, after a person approves it, and fails when the output changes. It is the cheapest way to check large outputs, and the easiest way to end up with tests nobody reads: the expected value is whatever was there last time, and one command accepts every change. This file says when snapshots help, when they rot, the review rules that keep them honest, and the tools for the owner's stacks.

kwx-developer has the short rules (`~/.claude/skills/kwx-developer/reliability/testing-strategy.md` section 10, `~/.claude/skills/kwx-developer/languages/rust/testing.md` section 4). This file is the full version, with the agent specific rule: an agent never accepts a snapshot change it has not read and justified.

## Contents

1. What they are and what they are good for
2. When they rot
3. Rules for writing them
4. Rules for reviewing and updating them
5. Making output deterministic
6. Tools
7. Golden files without a library
8. Checks

## 1. What they are and what they are good for

A snapshot test is still an assertion, like `toBe`: the expected value is stored outside the test (a `.snap` file, a golden file) or inline in it. The oracle is the human review of the first version and of every change (`test-oracles.md` section 6).

Good uses, where writing the expected value by hand is tedious and the output is meant to be read:

- CLI output and help text (Rust CLIs with `trycmd` or `insta`).
- TUI frames: ratatui renders into a `TestBackend` buffer, which snapshots as plain text.
- Error messages and diagnostics shown to users or developers (Kent C. Dodds lists error messages as a prime use).
- Generated code, SQL from a query builder, migration plans, serialized config.
- Parser output (ASTs), formatter output.
- Before and after diffs of a transformation (`snapshot-diff` in Jest, or a snapshot of only the changed part).

## 2. When they rot

Justin Searls (quoted by Dodds in "Effective Snapshot Testing"): snapshot tests are "tests you don't understand, so when they fail, you don't usually understand why or how to fix it", and "most developers, upon seeing a snapshot test fail, will sooner just nuke the snapshot and record a fresh passing one." Dodds: "When your snapshot is more than a few dozen lines it's going to suffer major maintenance issues."

Signs of rot:

- Snapshots of whole rendered component trees (hundreds of lines of markup); any style change rewrites them.
- A change touches 30 snapshot files and the commit message says "update snapshots".
- Snapshots contain timestamps, random ids, absolute paths or durations, so they change every run and get updated blindly.
- Nobody can say what a given snapshot is supposed to show.
- Obsolete snapshot entries pile up for tests that no longer exist.

A snapshot that fails on every unrelated change trains people (and agents) to accept changes without reading, which turns real regressions into accepted behaviour.

## 3. Rules for writing them

1. **Small and focused.** Snapshot the part that matters, not the whole page or object. Under about 50 lines per entry; enforce it in Jest with `eslint-plugin-jest`'s `no-large-snapshots`. Evidence: moderate (Jest docs, Dodds).
2. **Inline for short outputs.** `toMatchInlineSnapshot()` (Jest, Vitest) and `insta::assert_snapshot!(value, @"...")` keep the expected value in the test, so a reviewer sees it in the diff. Verified with Vitest 5.0.5: the first run writes the literal into the test file.
3. **Descriptive names.** The snapshot name says what the output should be: `exports["<Price /> shows 'Contact us' above 50 seats"]`, not `price 3` (Jest docs best practice).
4. **One explicit assertion next to it for the key fact.** `expect(out).toContain("Total: 125.00 €")` plus the snapshot. If the snapshot is accepted wrongly, the explicit assertion still guards the fact the test exists for.
5. **Deterministic output only** (section 5). A snapshot that changes between runs is worse than none.
6. **Not for behaviour you can assert directly.** If the point is "the button is disabled", assert that. Snapshots are for outputs meant to be read as a whole.
7. **Not as the only test of logic.** A pricing function gets example tests and properties; a snapshot of its formatted price table is an extra, not the test.

## 4. Rules for reviewing and updating them

For humans and agents alike:

- **Never update all snapshots to make a run green.** Not `jest -u`, `vitest -u`, `cargo insta accept`, `INSTA_UPDATE=always`, or `TRYCMD=overwrite` across the suite, unless every changed snapshot was read first. Jest docs: if other snapshots fail because of an unintentional bug, "fix the bug before re-generating snapshots".
- **Update narrowly.** `vitest -u -t "price table"`, `jest -u --testNamePattern "price table"`, `cargo insta review` (interactive, one by one: `a` accept, `r` reject, `s` skip).
- **Read every changed snapshot diff like code.** For each one, say why the change is intended and which spec line or task requires it. A change you cannot explain is a bug until proven otherwise.
- **CI never writes snapshots.** Jest and Vitest do not write new snapshots when run in CI (Vitest verified: with `CI=1`, a test with no stored snapshot fails with "Snapshot ... mismatched" instead of writing one). insta's default `INSTA_UPDATE=auto` means `no` in CI (insta 1.49.0 docs). Never set update modes in CI config.
- **Delete obsolete snapshots** in the same change that removes the test: `cargo insta test --unreferenced=reject` fails on leftovers (`delete` removes them); Jest and Vitest list obsolete snapshots in the run summary; remove them in the same change.

### The agent rule

An agent that changes code and sees snapshot failures must, for each failing snapshot:

1. Read the diff.
2. Decide: intended by the task (cite the line of the request or spec), or a regression.
3. Update only the intended ones, one test at a time, and list them in the report with the reason.
4. Treat a regression like any failing test: fix the code, not the snapshot.

This is the snapshot form of kwx-developer's rule against weakening tests (`~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 1): an unread snapshot update is a loosened assertion.

## 5. Making output deterministic

| Source of noise | Fix |
|---|---|
| Timestamps, dates | Fixed clock (fake timers, injected clock); or redact: Jest/Vitest property matchers `expect.any(Date)`, insta redactions `{ ".created_at" => "[timestamp]" }` |
| Random ids, UUIDs | Seeded generator, sequence based ids in tests, or redact |
| Absolute paths, home directory | Print paths relative to the project root; custom serializer or insta filters to replace the temp dir with `[TMP]` |
| Durations ("took 34 ms") | Redact, or do not print timing in the tested output |
| Terminal colours and width | Set `NO_COLOR=1` (or the tool's colour flag) and a fixed width in the test; ratatui `TestBackend::new(80, 24)` |
| Locale and time zone | `TZ=UTC`, a fixed locale (`LANG=C.UTF-8`, `Intl` locale passed explicitly) |
| Hash map iteration order | Sort before printing; `BTreeMap` in Rust; sorted keys in JSON serializers |
| Line endings (Windows contributors) | Normalize `\r\n` to `\n` in the serializer; `.gitattributes` for snapshot files |
| Floating point formatting | Round to the precision the spec cares about before printing |

## 6. Tools

### Jest and Vitest

```ts
expect(formatInvoice(inv)).toMatchInlineSnapshot();               // filled in on first run
expect(user).toMatchSnapshot({ id: expect.any(String), createdAt: expect.any(Date) });
await expect(renderCliHelp()).toMatchFileSnapshot("./__golden__/help.txt"); // Vitest: plain file, easy to read in review
```

`toMatchFileSnapshot` (Vitest, verified) writes the raw text to a file you name, which reads better in review than an escaped string in a `.snap` file. React Native component tree snapshots (`toJSON()` of a whole screen) are the classic rot case; test what the user sees with Testing Library queries instead.

### insta (Rust)

```rust
#[test]
fn renders_summary_frame() {
    let mut terminal = Terminal::new(TestBackend::new(60, 12)).unwrap();
    terminal.draw(|f| draw_summary(f, &sample_week())).unwrap();
    insta::assert_snapshot!(terminal.backend());   // the buffer prints as text
}
```

Workflow: `cargo insta test --review` (or `cargo test` then `cargo insta review`); commit the `.snap` files; `cargo insta pending-snapshots` lists what is waiting; `--unreferenced=reject` in CI catches leftovers. `INSTA_UPDATE` values: `auto` (default; `no` in CI, `new` locally, writing `.snap.new` files for review), `new`, `always` (writes directly, skips review: avoid), `unseen`, `no`, `force` (insta 1.49.0 docs).

### trycmd and snapbox (Rust CLIs)

`trycmd` runs a CLI from `.toml` or `.md` case files and compares stdout and stderr with the stored expectation; `TRYCMD=overwrite cargo test` rewrites them (trycmd docs). The `.md` form doubles as documentation: the README examples are the tests. The same review rules apply to `overwrite`.

### expect-test (Rust)

Inline expectations `expect![[...]]` updated with `UPDATE_EXPECT=1 cargo test` (used across rust-analyzer). Same rules: run the update only for the tests you mean to change.

### Visual screenshots

Pixel snapshots (Playwright `toHaveScreenshot`, Compose screenshot tests, Paparazzi, Roborazzi) follow the same review rules, plus thresholds and fixed fonts and devices. Running them may need a browser or emulator; see the user's rules (`strategy.md` section 3) and the web and mobile folders of this skill.

## 7. Golden files without a library

For any language, the pattern is: compare with a file; when an explicit update flag is set, write the file instead; never set the flag in CI.

```ts
// golden.ts
import { readFileSync, writeFileSync, existsSync } from "node:fs";

export function expectGolden(actual: string, path: URL) {
  if (process.env.UPDATE_GOLDEN === "1" && !process.env.CI) {
    writeFileSync(path, actual);
    return;
  }
  if (!existsSync(path)) throw new Error(`Golden file missing: ${path.pathname}. Run with UPDATE_GOLDEN=1 and review it.`);
  expect(actual).toBe(readFileSync(path, "utf8"));
}
```

Name golden files after the case (`help-no-args.txt`, `summary-empty-week.txt`), keep them next to the tests, and keep them small.

## 8. Checks

| Check | Pass condition |
|---|---|
| Right use | Snapshots cover outputs meant to be read as a whole; logic has explicit tests |
| Size | Entries under about 50 lines; `no-large-snapshots` or a size check in place |
| Deterministic | Run twice with no changes: no snapshot differs; clocks, ids, paths, colours, locale fixed or redacted |
| Key fact asserted | Each snapshot test also asserts the fact it exists for |
| No blind updates | No suite wide `-u`, `accept`, `always` or `overwrite` in the change; each updated snapshot listed with its reason |
| CI read only | CI never writes snapshots; no update env vars in CI config |
| No leftovers | No `.snap.new` or `.pending-snap` files committed; obsolete entries removed (`fd -e new -e pending-snap`) |
