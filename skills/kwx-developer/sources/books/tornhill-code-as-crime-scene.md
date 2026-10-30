# Adam Tornhill: Your Code as a Crime Scene (article, Code Maat, CodeScene docs)

What I read: the free original article "Code as a Crime Scene" (2013), the Code Maat README (the open source tool behind the book), CodeScene's public docs on hotspots and indentation complexity, InfoQ write-ups of his 2015 and 2017 QCon talks, and the abstract of Tornhill and Borg's "Code Red" paper (2022). I did not read the book itself (Pragmatic Bookshelf, paid; no legal free copy).

Legal URLs:
- https://www.adamtornhill.com/articles/crimescene/codeascrimescene.htm
- https://github.com/adamtornhill/code-maat
- https://codescene.io/docs/guides/technical/hotspots.html
- https://codescene.io/docs/guides/technical/complexity-trends.html
- https://www.infoq.com/news/2015/03/code-as-a-crime-scene
- https://www.infoq.com/news/2017/04/tornhill-prioritise-tech-debt
- https://arxiv.org/abs/2203.04374 (Code Red)

Key lessons used in the skill:
- A hotspot is where complexity and change frequency overlap. "Complexity is only a problem when we need to deal with it." Complex code nobody touches is low priority.
- Change frequency is counted as revisions (commits touching a file) from version control. Activity concentrates in a few files with a long tail; this holds at function level too.
- Complexity can be approximated by indentation (logical indent levels over non blank, non comment lines): language neutral, fast, correlates with cyclomatic complexity (CodeScene docs). Style changes in indentation bias it.
- Temporal (change) coupling: files that change in the same commits, with or without a code dependency. Code Maat defaults: min revisions 5, min shared revisions 5, min coupling 30%, max changeset size 30. Degree = shared revisions over the average of the two files' revisions. Test coupling to its own module is healthy; cross service or cross layer coupling signals a misplaced boundary ("shotgun surgery").
- Code Maat log command: `git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames --after=YYYY-MM-DD`, then `-c git2 -a coupling|revisions|age|authors|...`.
- Case study numbers (InfoQ 2015): 400 KLOC, 89 developers, hotspots held 7 of the 8 most defect dense parts; 4% of code had 72% of defects.
- Code Red (39 proprietary codebases): low quality code had 15x more defects and 124% longer time in development; issue resolution times far less predictable.
- Most technical debt is organisational; coordination cost shows where several teams touch the same code (not relevant for this user's solo repos).
