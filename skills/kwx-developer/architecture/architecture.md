# Code architecture and organisation: the master file

Language independent. Read this before writing code in an existing codebase, before adding a module or folder, and whenever asked to audit, review or "clean up" a codebase. It holds the 20 rules and the audit procedure. The other files in this folder go deeper on one topic each.

## Contents

1. Files in this folder and when to read them
2. What good organisation means (the one definition to use)
3. The 20 rules
4. Audit procedure: reading a codebase for organisation problems
5. How to write up an organisation finding
6. Checks

## 1. Files in this folder and when to read them

| File | What is in it | Read when |
|---|---|---|
| `consistency.md` | The consistency dimensions to check across a codebase, how to measure each, and how to pick the house convention when the code is mixed | Before writing code in any existing repo; in every audit |
| `scripts/scan_conventions.py` (skill root, not this folder) | Script that tallies conventions per area and flags areas that disagree | Run it first in every audit: `python3 -I ${CLAUDE_SKILL_DIR}/scripts/scan_conventions.py <repo>` |
| `modules-and-boundaries.md` | Deep modules, information hiding, dependency direction, cycles, public surface, ports and adapters and when they are overkill, shared core for web and mobile | Adding a module, package, crate, service layer or interface |
| `folder-structure.md` | Feature vs layer folders, colocation, layouts for web, Expo, monorepo and Rust workspaces, when to split a file, barrels | Creating files or folders, or a structure feels wrong |
| `naming.md` | Naming rules, vocabulary consistency, TS and Rust specifics | Naming anything public; reviewing names |
| `abstraction-and-duplication.md` | When to extract, rule of three, the wrong abstraction and how to undo it, DRY as knowledge | Tempted to extract a helper, or a shared function has grown flags |
| `code-smells.md` | Fowler's smells and Ousterhout's red flags with TS and Rust shapes, detection and the fix | Reviewing code; auditing |
| `evolving-a-codebase.md` | Changing structure safely: Chesterton's fence, Hyrum's law, tidy first, parallel change, branch by abstraction, strangler fig, ratchets, when to leave it | Any refactor, migration, rename, or "should I clean this up?" |

## 2. What good organisation means

Use this definition and no other. A codebase is well organised when a developer who has never seen it can find where a change belongs, make it in one place, and know what else it affects. Organisation is measured by the cost of the next change, not by how the code looks.

Ousterhout (A Philosophy of Software Design) names three symptoms of complexity. Use them as the vocabulary of every finding:

- **Change amplification**: a simple change needs edits in many places.
- **Cognitive load**: a developer must hold a lot of information to make a change.
- **Unknown unknowns**: it is not clear what must change, or what must be known, to make a change. The worst of the three, because nothing tells you that you missed something.

And two causes: **dependencies** (code that cannot be understood or changed in isolation) and **obscurity** (important information that is not obvious).

Kent Beck (Tidy First?, after Constantine) gives the economic version: the cost of software is roughly the cost of changing it, and the cost of change is dominated by coupling, where changing one element forces changes to others. Parnas (1972) gives the construction rule: start from the list of difficult design decisions and decisions likely to change, and make each module hide one of them.

Consequences an agent must apply:

- "Clean" is not a goal (Abramov). Less duplication, shorter functions and more layers are only good when they lower the cost of the likely next changes.
- Every module, layer, interface, export and abstraction costs reader attention. It must hide more than it costs to learn.
- Consistency is a first class property. Two ways of doing the same thing doubles what every reader must learn and makes every tool, codemod and grep miss half the code.

## 3. The 20 rules

Each rule has a check. "Rg" means ripgrep; adapt the globs to the repo.

**R1. Match the house convention before your own taste.** Before writing, find how this codebase already exports, names, imports, handles errors, logs, reads config and places tests, and write the same way, even where you would choose differently. Google's style guide puts it plainly: the value is "the consistency of having one answer rather than the answer itself", and "if no other rule applies, the author should maintain consistency with the existing code". Check: your diff introduces no variant that `scan_conventions.py` would flag as OFF or MIX in the area you touched. Details: `consistency.md`.

**R2. When the code is mixed, decide the house convention explicitly, by precedence, and say which one you chose.** Precedence: enforced lint or formatter config, then written docs (CONTRIBUTING, ARCHITECTURE, style guide), then the direction of recent change (what new files use), then the majority in the area being edited, then the repo majority, then the language community standard. Never pick by taste. Check: the commit or PR text names the convention and its source.

**R3. Every module hides a decision.** Before creating a module, file, class, crate or package, state in one sentence what it hides (a data format, a vendor, an algorithm, a protocol, a policy). If the answer is "nothing, it groups code", it is a folder, not a module. Check: each module's doc comment or ARCHITECTURE entry can name its secret.

**R4. Deep modules over shallow ones.** An interface should be much simpler than its implementation. Do not create pass-through functions, wrappers that rename a call, one-method classes that only forward, or a "service" that calls a "repository" that calls the ORM with the same arguments. Check: for each new function, the body is not a single call with the same parameters (`code-smells.md`, Middle Man and Pass-through).

**R5. Dependencies point one way, toward the stable core, and never form a cycle.** UI and IO depend on domain logic; domain logic does not import UI, framework or transport code. Shared code never imports feature code. Check: `npx madge --circular --extensions ts,tsx src` or eslint `import/no-cycle` reports nothing; `cargo modules dependencies --lib --acyclic` passes; no file in the domain folder imports from `components/`, `app/`, `pages/` or an HTTP framework.

**R6. Every export is a promise; keep the public surface small.** Export only what is used outside the module. In Rust default to private, then `pub(crate)`, and use `pub` only for the crate's real API. Hyrum's law: with enough users every observable behaviour, including undocumented ones, will be depended on. Check: `npx knip` reports no unused exports; Rust `unreachable_pub` lint is clean in libraries.

**R7. Organise the top level by domain once the app is more than small; layer inside each domain.** Fowler: presentation, domain, data layering at the top is fine for small systems, but once a layer grows, "split your top level into domain oriented modules which are internally layered". Check: adding one feature touches one feature folder plus at most the app shell (router, registry), not five layer folders.

**R8. Colocate what changes together.** Tests, styles, helpers, types and fixtures that serve one feature live in that feature. A helper used by one file lives in that file. Check: `rg -l "from '.*/utils/<name>'"` returns one importer means the helper should move next to it.

**R9. Shared code must earn its place.** Promote code to `shared/`, `lib/`, `common/` or a shared crate only when a second, independent consumer needs the same knowledge, not because it "might be reusable". Check: every symbol in shared folders has importers in two or more features (`knip` plus rg on importers).

**R10. Prefer duplication over the wrong abstraction.** Do not extract on the second occurrence of similar text. Extract when two places encode the same knowledge and must change together. When a shared function grows boolean flags, mode parameters or caller specific branches, inline it back into the callers and re-extract (Metz). Check: no shared function has more than one boolean parameter or a `type`/`mode`/`kind` parameter that selects disjoint code paths. Details: `abstraction-and-duplication.md`.

**R11. One piece of knowledge, one authoritative place.** DRY is about knowledge, not text (Thomas and Hunt): a business rule, a constant, a schema, a URL, a permission check, an enum of states lives in one place and everything else derives from it. Check: grep the literal (a price, a role name, a route, a magic number) and find exactly one definition.

**R12. Pull complexity down.** A module should absorb hard cases instead of pushing them to every caller through parameters, options and required call order. Defaults cover the common case; configuration that can be computed is computed. Check: count call sites passing the same option values; if most pass the same thing, it should be the default.

**R13. Handle errors in one style, at deliberate layers.** Pick one error model per layer (Rust: `thiserror` enums in libraries, `anyhow` in binaries; TS: throw typed errors or return result objects, not both in one layer) and translate errors only at boundaries. Define errors out of existence where you can (an empty selection instead of a "no selection" case). Check: within one module the scan shows a single error variant; no `catch {}` that drops the error.

**R14. Side effects at the edges, logic in the middle.** Read config and environment once at startup into a typed object; do IO in adapters and handlers; keep decision logic in pure functions that take data and return data. Check: `rg "process\.env|import\.meta\.env|std::env::var"` hits only the config module and the entry point.

**R15. One term per concept, everywhere.** If the domain says "workspace", the code never also says "project", "space" or "org" for the same thing. Same verb for the same operation (`fetch` for network, `load` for disk, or whatever the codebase uses). Rename when meaning shifts (Pragmatic Programmer tip 74). Check: grep the synonyms; build a glossary in ARCHITECTURE.md when the domain has more than a handful of nouns.

**R16. No speculative generality.** Do not add parameters, hooks, plugin systems, interfaces with one implementation, or config for needs nobody has. YAGNI does not apply to keeping code easy to change (Fowler), so refactoring for clarity is fine; adding capability for an imagined future is not. Check: every new interface has two implementations or a real test double requirement; every new option has a caller that sets it to a non-default value.

**R17. Separate structure changes from behaviour changes.** Make the change easy, then make the easy change (Beck). Tidying (renames, moves, extractions) goes in its own commit or PR with no behaviour change, before or after the feature commit. Check: each commit is either pure structure (tests unchanged and passing) or behaviour (with test changes), never both.

**R18. Change structure incrementally, keeping the system working at every step.** Use parallel change (expand, migrate, contract), branch by abstraction, or a strangler fig. No big bang rewrites, no long lived branches that move half the codebase. Check: every step builds and passes tests; a migration has a tracked count of remaining old usages that only goes down.

**R19. Find out why before removing (Chesterton's fence).** Before deleting or "simplifying" odd looking code, run `git log -S '<snippet>'` and `git blame` and read the commit that added it, plus any linked issue. Check: the PR states why the removed code existed and why that reason no longer holds.

**R20. Enforce structure with tools, and write down the invariants tools cannot check.** Boundaries, cycles, naming, export style and file naming belong in lint config (eslint `import/no-restricted-paths`, `import/no-cycle`, `import/no-default-export`, `unicorn/filename-case`; Biome `noBarrelFile`, `noDefaultExport`; clippy `mod_module_files` or `self_named_module_files`). Invariants that tools cannot check, especially absences ("the model layer never depends on views"), go in a short ARCHITECTURE.md (matklad). Check: the convention you rely on has a lint rule or an ARCHITECTURE.md line; if neither exists, propose one.

## 4. Audit procedure: reading a codebase for organisation problems

Follow in order. Do not open random files first; build the map, then sample.

1. **Read the written rules.** README, CONTRIBUTING, ARCHITECTURE.md, docs/adr, `.editorconfig`, lint and formatter configs (`eslint.config.*`, `biome.json`, `tsconfig.json` paths, `clippy.toml`, `rustfmt.toml`, `Cargo.toml` `[lints]`). These are the declared conventions; everything else is compared against them.
2. **Map the structure.** `git ls-files | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head -40` for folder sizes; `tree -d -L 3 -I node_modules` for shape. Name the organising principle (feature, layer, mixed). Mixed at the same level is itself a finding.
3. **Run the convention scan.** `python3 -I ${CLAUDE_SKILL_DIR}/scripts/scan_conventions.py <repo>` (add `--depth 3` for monorepos). Every OFF and MIX line is a lead. Open two example files per side before reporting.
4. **Check the dependency graph.** Cycles (madge, `import/no-cycle`, `cargo modules dependencies --acyclic`), direction (does shared import features? does domain import UI or framework?), and fan-in hotspots (files imported by everything: are they stable and small, or a god module that changes weekly?). `git log --format= --name-only --since=6.months | sort | uniq -c | sort -rn | head -20` gives churn; a file high on both churn and fan-in is the top risk.
5. **Check the public surface.** `npx knip` for unused files, exports and dependencies; barrels that re-export everything; Rust `pub` items never used outside the crate.
6. **Look for duplicated knowledge.** `npx jscpd --min-lines 8 src` for copy paste; grep for repeated literals (role names, URLs, status strings, magic numbers); two libraries doing one job in `package.json` or `Cargo.toml` (axios and fetch wrappers, moment and date-fns, two validation libraries, two state managers).
7. **Sample deeply.** Read the 5 largest files, the 5 highest churn files, and one complete feature end to end. Apply `code-smells.md` and the Ousterhout red flags.
8. **Check change locality.** Pick a recent feature commit (`git log --stat`) and count the folders it touched. A small feature touching many unrelated folders is change amplification made visible.
9. **Rank and report.** Order findings by cost of the next likely change times how many places it affects, not by count. Use the template in section 5. Group by root cause: twenty files with default exports in one folder is one finding, not twenty.

## 5. How to write up an organisation finding

Every finding has these parts. A finding without evidence from both sides is an opinion.

```
### <short name of the problem>
Where: <paths, with file:line for at least two examples of each variant>
What: <the inconsistency or structural problem, in one or two sentences>
Why it will hurt: <the concrete future cost: change amplification, cognitive load,
  unknown unknowns, broken tooling, a bug class it enables>
House convention: <which variant wins and the precedence source (R2)>
Fix: <the smallest change that resolves it, plus the guard that keeps it fixed
  (lint rule, ARCHITECTURE.md line, codemod)>
Effort and risk: <files touched; whether it changes behaviour; do it now, with the
  next change in that area, or leave it>
```

Example (from a real scan of an Expo app):

```
### Two import path styles inside one app
Where: src/screens/* use the "@/" alias (227 of 380 imports), src/components/* use
  relative paths (193 of 246), e.g. src/screens/Home.tsx:3 vs src/components/Card.tsx:2
What: the same app imports internal code two ways depending on folder.
Why it will hurt: moving a file between folders changes how its imports must be
  written; grep for importers of a module needs two patterns; codemods miss half.
House convention: alias. tsconfig declares "@/*" and the newest files use it (R2 step 3).
Fix: run a codemod to rewrite relative imports that leave the current folder to "@/";
  add eslint no-restricted-imports for patterns ["../*"].
Effort and risk: mechanical, no behaviour change, one structure-only PR.
```

## 6. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| House convention found before writing | Diff uses the variants the scan shows as majority for the touched area | `python3 -I ${CLAUDE_SKILL_DIR}/scripts/scan_conventions.py <repo>` before and after; no new OFF or MIX line |
| No import cycles | Zero cycles | `npx madge --circular --extensions ts,tsx <src>`; eslint `import/no-cycle`; `cargo modules dependencies --lib --acyclic` |
| Dependency direction | Shared never imports features; domain never imports UI, framework or transport | eslint `import/no-restricted-paths` zones; `rg -n "from '.*(components|app|pages)/" <domain dir>` returns nothing |
| Public surface minimal | No unused exports or files | `npx knip`; Rust `#![warn(unreachable_pub)]` in libs; `cargo +nightly udeps` for deps |
| Config read in one place | Env reads only in config module and entry point | `rg -n "process\.env\|import\.meta\.env\|env::var" --glob '!**/config*'` |
| No pass-through layers added | New functions do more than forward | Read each new function: body is not one call with the same args |
| Structure and behaviour separated | No commit mixes a move or rename with a behaviour change | `git show --stat` per commit; renames (R100 in `git log -M --name-status`) never sit with test changes |
| Removal justified | Every deleted odd construct has its origin explained | PR text cites `git log -S` result |
| Invariants written down | ARCHITECTURE.md lists boundaries and absences for repos over about 10k lines | File exists and names each top level module and forbidden dependency |
| Findings have evidence | Every audit finding lists file:line for each variant | Read the report |
