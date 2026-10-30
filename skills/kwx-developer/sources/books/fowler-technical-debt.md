# Martin Fowler: technical debt articles

What I read: "TechnicalDebt" (bliki), "TechnicalDebtQuadrant" (bliki), "Is High Quality Software Worth the Cost?".

Legal URLs:
- https://martinfowler.com/bliki/TechnicalDebt.html
- https://martinfowler.com/bliki/TechnicalDebtQuadrant.html
- https://martinfowler.com/articles/is-quality-worth-cost.html

Key lessons used in the skill:
- Cruft is internal quality deficiency that makes change harder. The extra effort on each change is interest; cleaning up is principal. Interest is only paid when someone works in that code, so high activity areas need zero tolerance and stable cruft can be left alone. This is why the audit ranks by churn.
- Quadrant: reckless or prudent, deliberate or inadvertent. Prudent deliberate debt in rarely changed code may never be worth paying. Prudent inadvertent debt (learning the right design after building) is inevitable even for great teams. Used to choose the recommended answer per finding.
- For a business owner: users cannot see internal quality; poor internal quality slows a team within weeks, not months; the cost of high internal quality is negative because features get cheaper. Cites Tornhill and Borg 2022 (15x defect density, over twice the resolution time).
