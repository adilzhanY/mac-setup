# Evolving a codebase safely

How to change the structure of existing code without breaking it, how to sequence structure and behaviour changes, and how to decide whether to clean something up at all. Models tend to fail here in two directions: they rewrite or "tidy" far beyond the task (big diffs, silent behaviour changes, removed guards they did not understand), or they pile a new pattern on top of an old one and never finish the migration.

## Contents

1. Before you remove or change anything: Chesterton's fence
2. Observable behaviour is the contract: Hyrum's law
3. Two hats: structure changes and behaviour changes
4. Tidy first, after, later, or never
5. Safety net: characterisation tests
6. Parallel change (expand, migrate, contract)
7. Branch by abstraction
8. Strangler fig
9. Large mechanical changes: codemods and ratchets
10. When to leave it alone
11. Checks

## 1. Before you remove or change anything: Chesterton's fence

G. K. Chesterton (The Thing, 1929): a reformer finds a fence across a road and says "I don't see the use of this; let us clear it away." The wiser answer: if you do not see the use, go and find out; then you may remove it.

In code, the odd `setTimeout(0)`, the duplicated check, the `sleep(50)`, the strange ordering, the catch that retries once, the `// do not remove` comment: each may encode a bug fix nobody wrote down.

Procedure before deleting or simplifying code you do not understand:

```
git log -S '<distinctive snippet>' --oneline -- <path>   # commit that added it
git log -L '/<function name>/,+20:<path>'                  # history of a function
git blame -w -C -C <path>                                  # ignore whitespace, follow moves
```

Read the introducing commit message, its diff, and any linked issue or PR. Then either:

- the reason still holds: keep it, and add a comment stating the reason so the next reader does not repeat the dig;
- the reason no longer holds: remove it, and state in the commit why it is safe ("added for Safari 13 bug, minimum supported is now Safari 16");
- no reason can be found: keep it unless you can test the case it might cover. If you remove it, do it in its own commit so it can be reverted alone.

## 2. Observable behaviour is the contract: Hyrum's law

"With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody." Inside an app the "users" are other modules, stored data, other services, and the humans using the product.

So a refactor must preserve: return values and their order, error types and messages that anything matches on, default values, event and callback order, timing that UI relies on, serialised formats (JSON field names, DB columns, local storage keys, URL shapes), log lines that alerts or scripts grep.

Before a structural change, list which of these the code exposes and who reads them (`rg` for the field names, keys and messages across the repo, including tests and scripts). Software Engineering at Google's example: code depending on hash map iteration order works until the hash changes. The Beyonce rule from the same book: if a behaviour matters, put a test on it.

## 3. Two hats: structure changes and behaviour changes

Kent Beck's two hats: at any moment you are either refactoring (changing structure, behaviour preserved, tests unchanged and green) or adding function (changing behaviour, tests change). Never both in one step.

- One commit is either structure only or behaviour only. Beck (Tidy First?): keep tidyings in separate commits, ideally separate PRs.
- Structure commits are reviewed for "is it really behaviour preserving?"; behaviour commits for "is the behaviour right?". Mixed commits get neither review properly.
- A structure commit should be safe to revert alone.
- If you find yourself mid-feature with a tangle of both, Beck's preferred fix is to throw the work away and redo it tidying first; the second pass is usually smaller and clearer. The polite minimum is to split it into separate commits before review.
- Moving and changing a file in one commit breaks `git log --follow` rename detection. Move in one commit, edit in the next.

## 4. Tidy first, after, later, or never

Beck's question is not "should this be cleaned up?" but "when?". Tidyings are small structure changes: guard clauses, delete dead code, normalise symmetries (make the same thing look the same everywhere), new interface with old implementation, reading order, cohesion order (put things that change together next to each other), explaining variables and constants, explicit parameters, extract helper, chunk statements, one pile (gather scattered code before re-splitting it).

- **Tidy first** when the tidying makes the behaviour change you are about to make easier, and it is small. "Make the change easy (warning: this may be hard), then make the easy change" (Beck). Example: extract the function you need to change, rename the confusing variable, then change behaviour.
- **Tidy after** when you now understand the code better than before and the area will be touched again soon.
- **Tidy later** (write it down) when the cleanup is larger than the feature, or touches code outside the task's area.
- **Never** when the code works, rarely changes, and nobody needs to read it. Code that never changes does not need to be pretty.

Scope rule for agents: tidy only code your task touches or reads to do its job. The broken windows principle (Pragmatic Programmer tip 5: "Fix bad designs, wrong decisions, and poor code when you see them") applies inside your task's area; outside it, report what you saw instead of fixing it in the same diff. A feature PR that also reformats twenty unrelated files hides the feature.

## 5. Safety net: characterisation tests

Refactoring needs tests that would fail if behaviour changed. When the code has none:

- Write characterisation tests: call the code with representative inputs and assert whatever it currently returns, even if it looks wrong. They pin behaviour, not correctness.
- Test at the highest level that is fast: the public function of the module, an HTTP handler, a CLI invocation. Tests on internals break with the refactor and protect nothing.
- Snapshot or golden file tests are acceptable for this purpose (Rust `insta`, Vitest `toMatchSnapshot`), as long as you review the snapshots.
- Run the full suite before the first structural step, so you know which failures are pre-existing.

## 6. Parallel change (expand, migrate, contract)

For changing an interface that has callers you cannot or should not all update in one commit (Fowler, Danilo Sato):

1. **Expand.** Add the new version alongside the old one. Both work. Old callers untouched.
2. **Migrate.** Move callers one at a time (or in batches) to the new version. Each step builds and passes tests. A useful variant: reimplement the old function in terms of the new one, then inline it at each call site.
3. **Contract.** When nothing uses the old version, delete it, and rename the new one back to the clean name if it carried a suffix.

Rules:

- Mark the old version so nobody adds new callers: `/** @deprecated use createInvoice */`, Rust `#[deprecated(note = "use create_invoice")]`, plus a lint rule if possible.
- Track the count of remaining old usages (`rg -c "oldName" src | awk -F: '{s+=$2} END {print s}'`) in the PR or issue.
- Finish the contract step. Fowler's warning: an unfinished parallel change leaves the codebase worse than before, with two ways to do one thing. This is where `V2`, `New` and `Legacy` names come from.
- For data (DB columns, stored JSON, local storage keys), the same pattern: write both, backfill, read new, stop writing old, drop old. Each step deployable on its own.

## 7. Branch by abstraction

For replacing a widely used dependency or subsystem (an ORM, a state library, an HTTP client, a storage backend) while continuing to ship:

1. Introduce an abstraction (a module or interface) that captures how callers use the current implementation; route one group of callers through it.
2. Move all callers to the abstraction, one part at a time. Add tests against the abstraction.
3. Build the new implementation behind the same abstraction; switch one group of callers (a feature flag can switch it per environment).
4. Switch the rest; delete the old implementation.
5. Delete the abstraction if it no longer hides anything worth hiding (R4).

The system builds and runs at every step. Prefer this over a long lived branch.

## 8. Strangler fig

For replacing a whole legacy system or a large legacy area (Fowler): build the new system around the edges of the old, intercept requests or entry points, move behaviour piece by piece, until the old system can be removed. Key points:

- Big bang rewrites "go down in flames most of the time": the old system's behaviour is hard to specify, much of it is not wanted, and nothing ships until the end.
- Find seams (routes, message types, screens, CLI commands) where traffic can be redirected to new code.
- Accept transitional architecture (proxies, adapters, dual writes) as a real cost that buys lower risk and earlier value.
- If the habits that produced the old mess do not change, the new system ends up the same.

## 9. Large mechanical changes: codemods and ratchets

- **Codemods over hand edits** for anything touching more than about 10 files: `jscodeshift`, `ts-morph`, `ast-grep` (`sg run -p 'old($A)' -r 'new($A)' -l ts`), `comby`, rust-analyzer structural search and replace, `cargo clippy --fix`, `cargo fix --edition`. They are complete and repeatable; hand edits miss cases.
- **One mechanical change per PR**, separate from behaviour. Reviewers check the codemod and a sample, not every line.
- **Ratchet** when you cannot fix everything now: turn on the lint rule as an error, with an explicit list of files allowed to violate it (eslint overrides with `files: [...]` set to `warn` or `off`, a baseline file, or clippy `#[expect(...)]` per item). The list only shrinks; new code cannot add violations. Remove each file from the list when it is fixed.
- **Keep a count.** Record the number of remaining old pattern uses in a tracking issue or in CI output so progress is visible.

## 10. When to leave it alone

Do not restructure when:

- The area has no tests and you cannot write characterisation tests cheaply. First make it safe, or leave it.
- The code is stable (no commits in a year: `git log -1 --format=%cr -- <path>`) and nothing planned touches it.
- The change is taste only and the existing code is consistent.
- The cleanup would be larger than the task and nobody asked for it. Write it up as a finding with the template in `architecture.md` section 5 instead.
- You are not sure what behaviour depends on it (Hyrum's law) and cannot find out.

Do restructure when the next planned change is hard because of the structure (preparatory refactoring), when the same bug class keeps appearing, or when a migration is half done and the two ways of doing things are spreading.

## 11. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Origin known before removal | Every removed odd construct has its introducing commit cited | PR text; `git log -S` |
| Observable behaviour preserved | No changed output, error text, field name, storage key or order in a structure change | tests green without edits; `git diff` shows no test changes in structure commits |
| Commits single hat | Each commit is structure only or behaviour only | `git log --stat`; structure commits change no test expectations |
| Moves separate from edits | Renamed files appear with 100 percent similarity in their own commit | `git log -M --name-status` shows `R100` for moves |
| Safety net exists | Code being restructured has tests at its public interface before the first step | test files for the module exist and fail when behaviour is broken deliberately |
| Parallel changes finished | No `@deprecated` item with zero callers left; no `V2`/`New`/`Legacy` twin whose original has no callers | `rg -n "@deprecated\|#\[deprecated" src` then count callers |
| Ratchet only shrinks | Allowlist of violating files is not longer than in the previous commit | diff the lint override list |
| Scope respected | Diff touches only files the task needed, plus separate tidying commits in that area | `git diff --stat main...HEAD` |
| Codemod used for wide changes | Mechanical changes over about 10 files come from a tool, with the command in the PR | PR description |
