# A Philosophy of Software Design (John Ousterhout, 2nd ed., 2021)

What I read: the author's free 2nd edition extract (20 pages, image PDF, read through OCR): all of chapter 6 "General-Purpose Modules are Deeper", section 9.8 "A different opinion: Clean Code" and 9.9, section 12.6 "comments are failures" with the chapter 2 recap of complexity symptoms, and all of chapter 21 "Decide What Matters". Plus the CS 190 (Stanford) book review session topic list. Chapters on deep modules, information hiding, pass-through methods and defining errors out of existence were not in the extract; those rules in the skill come from the debate document below (where Ousterhout restates them) and from the book's well known red flags list, confirmed against several secondary summaries.

Legal URLs:
- Book page and extract: https://web.stanford.edu/~ouster/cgi-bin/aposd.php , https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf
- CS 190 book discussion: https://web.stanford.edu/~ouster/cgi-bin/cs190-winter20/lecture.php?topic=bookReview

Key lessons used in architecture/:
- Complexity = what makes a system hard to understand and modify. Three symptoms: change amplification, cognitive load, unknown unknowns. Two causes: dependencies and obscurity.
- "Somewhat general-purpose": the module's functionality reflects current needs, its interface does not. The text editor example: `insert(position, text)` and `delete(start, end)` replace `backspace(cursor)`, `delete(cursor)`, `deleteSelection(selection)`; less code overall, better information hiding, UI concepts no longer leak into the text class.
- Questions: simplest interface that covers current needs; in how many situations will this method be used (one is a red flag); is it easy to use for current needs (lots of glue means too general).
- Push specialisation up (into features) or down (into drivers behind a general interface). Separate the general mechanism (History with fences) from special purpose actions and from policy.
- Eliminate special cases (empty selection instead of "no selection").
- "Depth is more important than length: first make functions deep, then try to make them short enough to be easily read. Don't sacrifice depth for length." Splitting creates conjoined methods when pieces must be read together.
- Decide what matters; minimise what matters (defaults, computed config, errors handled low); emphasise it through prominence, repetition and centrality. Two mistakes: treating too many things as important (shallow classes, irrelevant arguments) and missing what is important.
- Comments are not failures; interface comments define abstractions.
