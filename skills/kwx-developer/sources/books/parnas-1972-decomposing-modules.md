# On the Criteria To Be Used in Decomposing Systems into Modules (David Parnas, CACM 15(12), 1972)

What I read: the full paper (KWIC index example, both modularizations, changeability, independent development, comprehensibility, hierarchical structure, conclusion).

Legal URL: https://www.cse.sc.edu/~mgv/csce590f20/ParnasCriteria.pdf (course copy with ACM notice); DOI 10.1145/361598.361623

Key lessons:
- Two decompositions of the same program can be identical after assembly yet differ hugely in changeability, independent development and comprehensibility.
- The conventional (flowchart, step per module) decomposition puts important design decisions in the interfaces; the information hiding decomposition hides each decision likely to change in one module (input format, storing lines in core, packing characters, index vs stored shifts).
- Conclusion, verbatim: "it is almost always incorrect to begin the decomposition of a system into modules on the basis of a flowchart. We propose instead that one begins with a list of difficult design decisions or design decisions which are likely to change. Each module is then designed to hide such a decision from the others."
- A "uses" hierarchy (partial order, low levels never use high levels) lets you prune upper levels and reuse the trunk; hierarchy and clean decomposition are independent, both desirable.
