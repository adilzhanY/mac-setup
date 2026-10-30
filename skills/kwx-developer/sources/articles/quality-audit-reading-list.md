# Reading list: codebase audit, decisions, tech debt, hotspots

Sources read for `quality/` (2026-10-30). "Read" means fetched and read; "summary only" means only a secondary account was available. "Run" means the tool was executed on a real local repo to verify the command and output.

## Books and long sources (notes in sources/books/)
- Tornhill, Code as a Crime Scene, article: https://www.adamtornhill.com/articles/crimescene/codeascrimescene.htm (read; the book itself not read, paid)
- Google eng-practices, standard of review and what to look for: https://google.github.io/eng-practices/review/reviewer/standard.html , https://google.github.io/eng-practices/review/reviewer/looking-for.html (read)
- Nygard, Documenting Architecture Decisions: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions (read)
- Fowler, TechnicalDebt, TechnicalDebtQuadrant, Is High Quality Software Worth the Cost: https://martinfowler.com/bliki/TechnicalDebt.html , https://martinfowler.com/bliki/TechnicalDebtQuadrant.html , https://martinfowler.com/articles/is-quality-worth-cost.html (read)

## Hotspots and change coupling
- Code Maat README (git2 log format, analyses, coupling defaults): https://github.com/adamtornhill/code-maat (read)
- CodeScene hotspots: https://codescene.io/docs/guides/technical/hotspots.html (read)
- CodeScene complexity trends and indentation complexity: https://codescene.io/docs/guides/technical/complexity-trends.html (search summary only)
- InfoQ, Code as a Crime Scene (2015 numbers): https://www.infoq.com/news/2015/03/code-as-a-crime-scene (search summary only)
- InfoQ, Tornhill on prioritising tech debt (2017): https://www.infoq.com/news/2017/04/tornhill-prioritise-tech-debt (read)
- Tornhill and Borg, Code Red (2022): https://arxiv.org/abs/2203.04374 (abstract and summaries only)
- Git commands before reading code (churn, bug clusters, bus factor, reverts): https://piechowski.io/post/git-commands-before-reading-code/ (read)

## Decision records
- ADR organisation: https://adr.github.io/ (read)
- MADR 4.0.0: https://adr.github.io/madr/ , minimal template https://github.com/adr/madr/blob/develop/template/adr-template-minimal.md (read)
- Zimmermann, ADR creation practices and anti-patterns: https://www.ozimmer.ch/practices/2023/04/03/ADRCreation.html (read)
- Henderson, ADR guidance: https://github.com/joelparkerhenderson/architecture-decision-record (read)
- Y-statements: https://medium.com/olzzio/y-statements-10eb07b5a177 (search summary only)

## Tools (docs read, then run locally)
- dependency-cruiser CLI and rules: https://github.com/sverweij/dependency-cruiser/blob/main/doc/cli.md , https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md (read; v18.7.0 run)
- madge: https://github.com/pahen/madge (read; v8.0.0 run)
- knip CLI, issue types, configuration: https://knip.dev/reference/cli , https://knip.dev/reference/issue-types , https://knip.dev/reference/configuration (read; v6.44.0 run)
- ts-prune: https://github.com/nadeesha/ts-prune (read; not run)
- eslint-plugin-import-x: https://github.com/un-ts/eslint-plugin-import-x (read; not run)
- eslint-plugin-boundaries: https://github.com/javierbrea/eslint-plugin-boundaries (read; not run; rule name `boundaries/dependencies` taken from README)
- jscpd: https://github.com/kucherenko/jscpd (README 404 and npm 403 via fetch; options taken from `--help`; v4.3.0 and v5.4.2 run)
- ast-grep rule config and YAML reference: https://ast-grep.github.io/guide/rule-config.html , https://ast-grep.github.io/reference/yaml.html (read; v0.51.0 run, five rules tested)
- semgrep rule syntax: https://docs.semgrep.dev/writing-rules/rule-syntax (read; v1.183.0 run through uvx)
- Clippy usage: https://doc.rust-lang.org/clippy/usage.html (read; clippy 0.1.98 run)
- cargo-machete: https://github.com/bnjbvr/cargo-machete (read; run)
- cargo-udeps: https://github.com/est31/cargo-udeps (read; not run, needs nightly)
- cargo-modules: https://github.com/regexident/cargo-modules (read; not run, long build)
- scc: https://github.com/boyter/scc (read; not run, not installed)
- tokei: run (v15.0.0), no doc fetched
