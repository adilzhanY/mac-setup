# Software Engineering at Google (Winters, Manshreck, Wright, 2020)

What I read: chapter 1 "What Is Software Engineering?" (time, scale, trade-offs, Hyrum's law, Beyonce rule, churn rule, shifting left) and chapter 8 "Style Guides and Rules" (principles for rules, consistency, enforcement, changing rules), in the free online edition published by the authors.

Legal URL: https://abseil.io/resources/swe-book (ch01: https://abseil.io/resources/swe-book/html/ch01.html , ch08: https://abseil.io/resources/swe-book/html/ch08.html)

Key lessons:
- "Software engineering is programming integrated over time." Expected lifespan decides how much the practices matter.
- Hyrum's law with the hash ordering example; dependencies on unpromised behaviour propagate to callers of callers.
- "It's programming if 'clever' is a compliment, but it's software engineering if 'clever' is an accusation."
- Beyonce rule: "If you liked it, you should have put a CI test on it."
- Rules must pull their weight; optimise for the reader ("simple to read" over "simple to write"); be consistent: "It's the consistency of having one answer rather than the answer itself that is the valuable part"; consistency scopes from file to team to codebase; avoid error-prone and surprising constructs; concede to practicalities.
- Enforce with tools first (about 90 percent of C++ guide rules are checkable), formatters end formatting debates, human judgment for the rest.
- Rule changes need evidence from real code, documented rationale, and arbiters.
