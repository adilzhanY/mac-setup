# A Philosophy of Software Design vs Clean Code (Ousterhout and Robert Martin, 2024 to 2025)

What I read: the full written debate (about 2300 lines of markdown): introductions, method length and its summary, comments and its summary, the PrimeGenerator rewrites, the TDD summary and closing remarks.

Legal URL: https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md (linked from the author's book page)

Key lessons:
- Shared premise: optimise for the reader, who is usually not the author.
- Deep vs shallow methods; over-decomposition produces shallow interfaces and entanglement ("conjoined" methods: to understand one you must read the other). Flipping back and forth between two implementations while reading is the red flag; merge them.
- Both agree Clean Code gives no guidance on recognising over-decomposition. Numeric limits (2 to 4 line functions) are not a design rule.
- Ousterhout: Clean Code's two general errors are failing to focus on what matters and failing to balance trade-offs: "Almost any design idea becomes a bad thing if taken to the extreme."
- Comments: interface comments are necessary to define an abstraction; implementation comments where code is non-obvious. Very long method names as a substitute for comments are worse.
- Neither author's naming or comments fully communicated the PrimeGenerator algorithm to the other: explanation is hard from inside the box; test it on a reader.
