# Hotspots: rank findings by where the work actually happens

An audit finds more problems than anyone will fix. Hotspot analysis decides the order. Code that is complex AND changed often costs money on every change; complex code nobody touches costs nothing until someone does. Every command here except Code Maat (section 11, from its README) is plain `git` plus `awk` and was run on real repos (a 383 commit Rust workspace and a 373 commit Next.js app) on 2026-10-30.

## Contents

1. Why churn decides priority (the evidence)
2. Before you run anything: the window and the exclusions
3. Churn: which files change most
4. Complexity proxy without a parser (indentation)
5. Hotspot score: churn times complexity
6. Change coupling: files that always change together
7. Bug clusters, firefighting and ownership
8. Drilling down: complexity trend and function level history
9. Reading the results
10. Feeding hotspots into the audit
11. Deeper tool: Code Maat
12. Checks

## 1. Why churn decides priority

- Fowler: interest on technical debt is paid only when someone works in that code. "Areas of high activity need a zero-tolerance attitude to cruft", while crufty code that is rarely touched can stay ([TechnicalDebt](https://martinfowler.com/bliki/TechnicalDebt.html)).
- Tornhill: hotspots are where complexity and development activity overlap. "Complexity is only a problem when we need to deal with it" ([Code as a Crime Scene](https://www.adamtornhill.com/articles/crimescene/codeascrimescene.htm)). In his reported case study (400 KLOC, 89 developers), hotspots held 7 of the 8 most defect dense parts and 4% of the code held 72% of defects ([InfoQ 2015](https://www.infoq.com/news/2015/03/code-as-a-crime-scene)).
- Tornhill and Borg 2022, 39 proprietary codebases: low quality ("Red") code had 15 times more defects and 124% longer time in development than healthy code ([arXiv 2203.04374](https://arxiv.org/abs/2203.04374)). Use this number when explaining priority to an owner.
- Activity is concentrated: most change lands in a few files with a long tail. On the Rust workspace measured here, 10 of the 166 Rust files touched in the year took 53% of all edits (1091 of 2063).

Rule: never order audit findings by tool severity alone. Order by hotspot rank first, then severity.

## 2. The window and the exclusions

- Window: last 12 months for a mature repo; the whole history if the repo is younger than a year. Tornhill uses 2 to 3 months of heavy activity for change coupling.
- Pass `--no-renames` so a rename does not count as a delete plus an add on two names, and run from the repo root with a pathspec, not from a subfolder (paths must match `git ls-files`).
- Exclude what is not hand written source: lockfiles, changelogs, generated code, snapshots, migrations, vendored code. Use a pathspec so the exclusion is visible in the command:

```bash
# bash: source only, tests ranked separately
SRC=( -- '*.ts' '*.tsx' '*.rs' ':!*.d.ts' ':!**/generated/**' ':!**/__snapshots__/**' ':!**/tests/**' ':!*.test.*' ':!*.spec.*' )
git log --since="12 months ago" --format=format: --name-only --no-renames "${SRC[@]}" | grep -v '^$' | sort | uniq -c | sort -rn | head
```

- Squash merge repos record one commit per PR: churn still works, ownership does not (it shows the merger).
- A file that no longer exists is skipped (`[ -f "$f" ] || continue`), otherwise deleted files top the list.

## 3. Churn

Revisions per file, last 12 months:

```bash
git log --since="12 months ago" --format=format: --name-only --no-renames -- '*.rs' ':!*/tests/*' \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -20
```

Output: `revisions path`. Revisions (commits touching the file) is Code Maat's measure. Lines added plus deleted (`--numstat`) is noisier because formatting commits inflate it; use revisions.

Read it: high churn alone may only mean active feature work. It becomes a finding when it meets complexity (section 5), bug fixes (section 7) or missing tests ([codebase-audit-tools.md](codebase-audit-tools.md) section 9).

## 4. Complexity proxy: indentation

Tornhill's whitespace complexity: count logical indentation levels over non blank, non comment lines. CodeScene documents it as language neutral, fast, and correlating well with cyclomatic complexity ([CodeScene docs](https://codescene.io/docs/guides/technical/complexity-trends.html)). It works the same for Rust, TypeScript, QML and SQL, which is why it is the default here.

```bash
# indent complexity of one file: total logical indents, lines, indents per line
awk '/^[[:space:]]*$/ {next} /^[[:space:]]*(\/\/|#|\*|\/\*)/ {next}
     { match($0,/^[ \t]*/); s=substr($0,1,RLENGTH); gsub(/\t/,"    ",s); ind+=int(length(s)/4); loc++ }
     END { printf "%d loc  %d indent  %.2f per line\n", loc, ind, ind/loc }' path/to/file.rs
```

Use 4 spaces per level; for a 2 space codebase change `/4` to `/2`, or the ranking stays right but absolute numbers double. Prefer a real metric when one is already installed: `scc --by-file -s complexity` counts branch tokens (comparable only within one language), `cargo clippy -W clippy::cognitive_complexity` names functions.

## 5. Hotspot score

```bash
git log --since="12 months ago" --format=format: --name-only --no-renames -- '*.rs' ':!*/tests/*' \
 | grep -v '^$' | sort | uniq -c | sort -rn | head -40 \
 | while read revs f; do [ -f "$f" ] || continue
     awk -v revs="$revs" -v f="$f" '
       /^[[:space:]]*$/ {next} /^[[:space:]]*(\/\/|#|\*|\/\*)/ {next}
       { match($0,/^[ \t]*/); s=substr($0,1,RLENGTH); gsub(/\t/,"    ",s); ind+=int(length(s)/4); loc++ }
       END { printf "%8d  %4d revs  %6d loc  %7d indent  %s\n", revs*ind/100, revs, loc, ind, f }' "$f"
   done | sort -rn | head -15
```

Swap `'*.rs'` for `'*.ts' '*.tsx'` and so on. Real output (Rust workspace):

```
   28994   193 revs    4211 loc    15023 indent  crates/sahna-editor/src/app.rs
   12604    92 revs    3320 loc    13701 indent  crates/sahna-editor/src/views/timeline.rs
   12123    86 revs    4659 loc    14097 indent  crates/sahna-render/src/plan.rs
    7694    33 revs    5468 loc    23318 indent  crates/sahna-core/src/effects.rs
```

`app.rs` is 2.3 times the next file: that is the single place where cleanup pays back fastest. `effects.rs` is the most complex file but changes a sixth as often: lower priority, leave it unless a feature goes there.

The score is relative. Compare files within one repo, never across repos. Only the top 5 to 10 matter.

## 6. Change coupling

Two files that change in the same commits most of the time are coupled, whether or not one imports the other. Formula and defaults follow Code Maat ([code-maat](https://github.com/adamtornhill/code-maat)): degree = shared commits / average revisions of the two, at least 5 revisions each, at least 5 shared, degree at least 30%, commits touching more than 30 files ignored (bulk renames and formatting).

```bash
git log --since="12 months ago" --format='format:@@' --name-only --no-renames -- '*.rs' \
 | awk '
   function flush(   i,j) { if (n>0 && n<=30) for(i=1;i<=n;i++){ rev[f[i]]++; for(j=i+1;j<=n;j++) pair[(f[i]<f[j]) ? f[i] SUBSEP f[j] : f[j] SUBSEP f[i]]++ } n=0 }
   /^@@$/ { flush(); next }  NF { f[++n]=$0 }
   END { flush(); for (p in pair) { split(p, ab, SUBSEP); avg=(rev[ab[1]]+rev[ab[2]])/2
           if (pair[p]>=5 && rev[ab[1]]>=5 && rev[ab[2]]>=5 && 100*pair[p]/avg>=30)
             printf "%3d%%  %3d shared  %s <-> %s\n", 100*pair[p]/avg, pair[p], ab[1], ab[2] } }' \
 | sort -k1,1nr -k2,2nr | head -20
```

Note `--format='format:@@'`: a bare `--format='@@'` is rejected by git as an invalid pretty format.

Real output and how to read each kind:

```
 95%   11 shared  crates/sahna-expr/src/lib.rs <-> crates/sahna-expr/tests/expressions.rs
 90%   30 shared  crates/sahna-core/src/text.rs <-> crates/sahna-text/src/lib.rs
 68%   20 shared  crates/sahna-core/src/effects.rs <-> crates/sahna-render/src/effects/mod.rs
```

| Pair kind | Meaning | Finding? |
|---|---|---|
| Source and its own test | Tests move with code | No, healthy. CodeScene says the same |
| Two files in the same module | Normal cohesion | Only if one is a hotspot |
| Across crates, packages or layers (`core/text.rs` and `text/lib.rs`, 90%) | A concept is split over two places; every change is "shotgun surgery" | Yes: key `coupling`, ask whether the concept should live in one place |
| Source and a test of a DIFFERENT module, or an end to end test | Brittle test or hidden dependency | Yes, low priority |
| Client and server files, or two services | Contract duplicated by hand | Yes: shared schema or generated types |
| Copy pasted siblings (`FooTool.tsx` and `BarTool.tsx`) | Duplication; confirm with jscpd | Yes: key `duplicate` |

## 7. Bug clusters, firefighting and ownership

From [piechowski.io](https://piechowski.io/post/git-commands-before-reading-code/); they depend on commit message discipline, so check a few messages first.

```bash
# files most often touched by fix commits
git log --since="12 months ago" -i -E --grep='fix|bug|broken|regress|crash' --name-only --format='' --no-renames \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -20
# reverts and hotfixes: a handful a year is normal, every couple of weeks means the release path is not trusted
git log --oneline --since="1 year ago" | grep -iE 'revert|hotfix|emergency|rollback'
# bus factor: one person over 60% of commits, or the top author absent for 6 months
git shortlog -sn --no-merges
git shortlog -sn --no-merges --since="6 months ago"
```

A file high on BOTH the churn list and the fix list is the highest risk file in the repo: patched repeatedly, never fixed. Report it first.

For a solo project (most of this user's repos) skip the bus factor; it is always one person.

## 8. Drilling down

Complexity trend of one hotspot (is it getting worse?):

```bash
f=crates/sahna-editor/src/app.rs
git log --format='%h %ad' --date=short --no-renames -- "$f" | awk 'NR%20==1' | while read h d; do
  git show "$h:$f" 2>/dev/null | awk -v d="$d" '/^[[:space:]]*$/{next} /^[[:space:]]*\/\//{next}
    {match($0,/^[ \t]*/); s=substr($0,1,RLENGTH); gsub(/\t/,"    ",s); i+=int(length(s)/4); n++}
    END{printf "%s  %5d loc  %6d indent  %.2f per line\n", d, n, i, i/n}'
done
```

Read: rising total with flat "per line" means the file grows by adding similar code (split it by feature). Rising "per line" means deeper nesting (extract functions, early returns). On the measured `app.rs`, 1370 to 4216 lines in three days and per line 2.96 to 3.57: both at once.

Function level history (Tornhill's X-ray, done by hand). `git log -L` follows one function by name:

```bash
git log -L ':step_playback:crates/sahna-editor/src/app.rs' -s --format='%h %ad' --date=short | wc -l
```

Run it for the 5 to 10 largest functions of a hotspot file (largest by `clippy::too_many_lines` or by eye) to find the one function that takes the edits. Refactor that function, not the whole file.

## 9. Reading the results

| Churn | Complexity | Action |
|---|---|---|
| High | High | Top priority. Refactor in small steps behind tests. Report as P1 if it also has bug fixes or no tests |
| High | Low | Healthy active code. Keep it that way: no finding |
| Low | High | Stable legacy. Leave it. Touch only when a feature lands there, and add tests first then. P3 at most |
| Low | Low | Ignore |

- A hotspot is a place to look, not a verdict. Open the file and confirm a concrete problem (a 900 line function, 6 levels of nesting, one switch handling 40 cases) before writing a finding.
- A config file or a route table can churn heavily and be fine. Name the reason when you dismiss one.
- Young repos (under ~50 commits) have no meaningful churn signal: rank by size and risk instead and say so in the report.

## 10. Feeding hotspots into the audit

1. Run section 5 once per language at the start of the audit, before any other tool. Keep the top 15 list.
2. Every finding from [codebase-audit-tools.md](codebase-audit-tools.md) gets the hotspot rank of its file (or "cold").
3. Priority in [tech-debt-and-todo.md](tech-debt-and-todo.md) uses that rank: a layering violation in the number 1 hotspot outranks the same violation in a cold file.
4. In the owner facing summary, translate rank into plain words: "this file was changed 193 times this year; every new feature touches it".

## 11. Deeper tool: Code Maat

When the shell versions are not enough (author analysis, entity effort, age), use Code Maat (Clojure, needs Java):

```bash
git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames --after=2025-10-30 > /tmp/repo.log
java -jar code-maat-standalone.jar -l /tmp/repo.log -c git2 -a coupling      # entity, coupled, degree, average-revs
java -jar code-maat-standalone.jar -l /tmp/repo.log -c git2 -a revisions
java -jar code-maat-standalone.jar -l /tmp/repo.log -c git2 -a age           # months since last change
```

Defaults: `--min-revs 5`, `--min-shared-revs 5`, `--min-coupling 30`, `--max-changeset-size 30`. The awk in section 6 reproduces `coupling` with the same defaults, so Code Maat is optional.

## 12. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Hotspots computed before findings are ranked | The audit report lists a top hotspot table with revs, loc, indent | Read the report |
| Exclusions applied | No lockfile, `.d.ts`, generated, snapshot or deleted file in the top 15 | Scan the list for `lock`, `generated`, `.d.ts`; every path passes `test -f` |
| Window stated | Report says the window ("last 12 months") and commit count | Read the report |
| Coupling uses git2 defaults | min 5 revs, min 5 shared, at least 30%, changesets over 30 files dropped | Read the awk thresholds |
| Test coupling not reported as a problem | No finding whose pair is a file and its own test | Grep findings for `test` pairs |
| Hotspot confirmed by reading | Each hotspot finding names a concrete construct (function, line range) | Read the finding text |
| Young repo handled | Under 50 commits: report says churn is not meaningful | `git rev-list --count HEAD` |
