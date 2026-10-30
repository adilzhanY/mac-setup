# Architecture decision records: Nygard, MADR, Zimmermann, Henderson

What I read: Michael Nygard's original post (2011), the MADR 4.0.0 site and minimal template, adr.github.io, Olaf Zimmermann's "ADR creation" practices and anti-patterns (2023), and Joel Parker Henderson's ADR repository guidance.

Legal URLs:
- https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- https://adr.github.io/ and https://adr.github.io/madr/
- https://github.com/adr/madr/blob/develop/template/adr-template-minimal.md
- https://www.ozimmer.ch/practices/2023/04/03/ADRCreation.html
- https://github.com/joelparkerhenderson/architecture-decision-record

Key lessons used in the skill:
- Nygard: Title (short noun phrase), Context (forces, value neutral, including tension), Decision ("We will ..."), Status (proposed, accepted, deprecated, superseded), Consequences (all of them, good and bad). One or two pages. Numbered sequentially, never reused. Reversed decisions are kept and marked superseded. One ADR, one significant decision. Significant = affects structure, non-functional characteristics, dependencies, interfaces, construction techniques.
- MADR 4.0.0 (2024-09): files `docs/decisions/NNNN-title-with-dashes.md`; front matter status, date, decision-makers, consulted, informed; sections Context and Problem Statement, Considered Options, Decision Outcome (Consequences, Confirmation), optional pros and cons. Minimal and bare variants exist.
- Zimmermann: decisions costly to undo must not be deferred; disclose confidence; anti-patterns Fairy Tale (only pros), Sales Pitch, Free Lunch Coupon (hidden consequences), Dummy Alternative, Sprint (one option only), Tunnel Vision, Mega-ADR, Blueprint in Disguise. Y-statement one sentence form.
- Henderson: do not write ADRs for minor, temporary or experimental decisions or for what a standard already covers; never rewrite history (amend or supersede), though his teams found dated notes on a living record practical. The skill takes: never edit decision text, append dated notes for clarifications, supersede for changes.
