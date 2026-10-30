# Google Engineering Practices: code review guide

What I read: "The Standard of Code Review" and "What to look for in a code review" from Google's public eng-practices site.

Legal URLs:
- https://google.github.io/eng-practices/review/reviewer/standard.html
- https://google.github.io/eng-practices/review/reviewer/looking-for.html

Key lessons used in the skill:
- Approve a change once it definitely improves overall code health, even if imperfect; never accept one that degrades it.
- Technical facts and data overrule opinions and personal preferences. On style the style guide is the authority; anything it does not cover is preference, so follow the existing code, and with no precedent the author's choice stands. Used to drop preference findings from the audit.
- Consistency: when the guide only recommends, lean toward it unless the local inconsistency would be confusing; if no rule applies, be consistent with existing code; file cleanup of existing inconsistencies separately (a TODO). This is the audit's "majority of the folder decides" rule.
- Prefix optional points with "Nit:". Do not block on personal style.
- What to look for: design first, functionality, complexity ("can't be understood quickly by code readers"), over-engineering (be especially vigilant; solve the problem known now), tests that would fail if the code broke, naming, comments that explain why, style, docs, every line, context beyond the diff.
