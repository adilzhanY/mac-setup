# Reading list: code architecture and organisation

Sources read for `architecture/` (2026-10-30). "Read" means fetched and read; "summary only" means only a secondary account was available.

## Books and long sources (notes in sources/books/)
- Ousterhout, A Philosophy of Software Design, 2nd ed., legal extract: https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf (read, OCR)
- Ousterhout and Martin, APOSD vs Clean Code debate: https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md (read)
- Software Engineering at Google, ch. 1 and ch. 8: https://abseil.io/resources/swe-book/html/ch01.html , https://abseil.io/resources/swe-book/html/ch08.html (read)
- Parnas 1972, On the Criteria To Be Used in Decomposing Systems into Modules: https://www.cse.sc.edu/~mgv/csce590f20/ParnasCriteria.pdf (read)

## Ousterhout
- CS 190 book discussion topics: https://web.stanford.edu/~ouster/cgi-bin/cs190-winter20/lecture.php?topic=bookReview (read, topic list only)
- Red flags list cross checked against secondary summaries: https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2 , https://yingang.github.io/aposd-zh/en/summary.html (search results only)

## Fowler and refactoring
- Refactoring catalog: https://refactoring.com/catalog/ (read, full list of 66)
- Code Smell: https://martinfowler.com/bliki/CodeSmell.html (read)
- Smells list of Refactoring 2nd ed. ch. 3 confirmed via TOC listings: https://www.informit.com/articles/article.aspx?p=2952392 (search result)
- Strangler Fig Application: https://martinfowler.com/bliki/StranglerFigApplication.html (read)
- Parallel Change: https://martinfowler.com/bliki/ParallelChange.html (read)
- Branch By Abstraction: https://martinfowler.com/bliki/BranchByAbstraction.html (read)
- Presentation Domain Data Layering: https://martinfowler.com/bliki/PresentationDomainDataLayering.html (read)
- Yagni: https://martinfowler.com/bliki/Yagni.html (read)
- Beck Design Rules: https://martinfowler.com/bliki/BeckDesignRules.html (read)
- Preparatory refactoring example: https://martinfowler.com/articles/preparatory-refactoring-example.html (read)
- Workflows of Refactoring: https://martinfowler.com/articles/workflowsOfRefactoring/ (slide deck, only headings readable)

## Kent Beck, Tidy First?
- Newsletter archive: https://newsletter.kentbeck.com/archive (read, no tidying posts on the visible page)
- Excerpt on dead code, getting untangled, coupling: https://newsletter.pragmaticengineer.com/p/dead-code-getting-untangled-and-coupling (read)
- Henrik Warne's review listing the tidyings and Constantine's equivalence: https://henrikwarne.com/2024/01/10/tidy-first/ (read, secondary)

## Abstraction and duplication
- Sandi Metz, The Wrong Abstraction: https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction (read)
- Kent C. Dodds, AHA Programming: https://kentcdodds.com/blog/aha-programming (read)
- Kent C. Dodds, Colocation: https://kentcdodds.com/blog/colocation (read)
- Dan Abramov, Goodbye, Clean Code: https://overreacted.io/goodbye-clean-code/ (read)
- Thomas and Hunt, Orthogonality and the DRY Principle (Artima): https://www.artima.com/articles/orthogonality-and-the-dry-principle (read)
- The Pragmatic Programmer tips: https://pragprog.com/tips/ (read, all 100 tips)

## Laws and principles
- Hyrum's law: https://www.hyrumslaw.com/ (read)
- Conway, How Do Committees Invent: https://www.melconway.com/Home/Committees_Paper.html (read)
- Chesterton's fence, source (The Thing, 1929) confirmed via: https://www.lesswrong.com/w/chesterton-s-fence (search results)
- Robert Martin package metrics (instability, main sequence): https://en.wikipedia.org/wiki/Software_package_metrics (search result summary)

## Architecture styles and structure
- Alistair Cockburn, Hexagonal Architecture: https://alistair.cockburn.us/hexagonal-architecture/ (read)
- matklad, ARCHITECTURE.md: https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html (read)
- matklad, Large Rust Workspaces: https://matklad.github.io/2021/08/22/large-rust-workspaces.html (read)
- bulletproof-react project structure: https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md (read)
- TkDodo, Please Stop Using Barrel Files: https://tkdodo.eu/blog/please-stop-using-barrel-files (read)
- Atlassian, Faster builds when removing barrel files: https://www.atlassian.com/blog/atlassian-engineering/faster-builds-when-removing-barrel-files (search summary: 75 percent build time cut)
- monorepo.tools: https://monorepo.tools/ (read; published by Nx, a vendor)
- Expo monorepo guide: https://docs.expo.dev/guides/monorepos/ (read)
- Destroy All Software, Functional Core Imperative Shell: https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell (page body not readable; idea used from general knowledge)

## Style guides and review
- Google eng practices, What to look for in a code review: https://google.github.io/eng-practices/review/reviewer/looking-for.html (read)
- Google eng practices, The standard of code review: https://google.github.io/eng-practices/review/reviewer/standard.html (read)
- Google TypeScript style guide: https://google.github.io/styleguide/tsguide.html (read, naming, exports, imports, file organisation)
- Rust API Guidelines, naming: https://rust-lang.github.io/api-guidelines/naming.html (read)
- The Rust Book ch. 7.5, module files: https://doc.rust-lang.org/book/ch07-05-separating-modules-into-different-files.html (read)
- Clippy lint configuration defaults: https://doc.rust-lang.org/clippy/lint_configuration.html (read, thresholds)

## Tools
- cargo-modules (structure, dependencies --acyclic, orphans): https://github.com/regexident/cargo-modules (read)
- knip: https://knip.dev/ (read, overview only)
- Biome rules noBarrelFile, noReExportAll, noNamespaceImport: https://biomejs.dev/linter/rules/noBarrelFile (search results)
