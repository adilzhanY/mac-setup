# The Humane Interface (Jef Raskin, 2000)

## What was read, and where

- Course notes on chapters 1 to 3, Brown University CSCI 0920 (2005): https://cs.brown.edu/courses/csci0920/2005/bell.raskin.pdf (read in full via pdftotext)
- Raskin Center for Humane Interfaces, "Core principles of humane interface design": https://www.raskincenter.org/rchi/core-principles
- Raskin, "Intuitive equals familiar", Communications of the ACM 37(9), 1994, hosted by Tognazzini: https://asktog.com/papers/raskinintuit.html (read in full; an article, not part of the book, but it is Raskin's central argument about intuitiveness)
- Secondary descriptions of the book's treatment of modes and confirmation habituation (InformIT listing, encyclopedia.pub).

## Key lessons

1. **Intuitive equals familiar.** A feature is intuitive to the degree it resembles something already learned. Precise definition: "using readily transferred, existing skills". The mouse experiment: a computer-literate teacher who had never seen a mouse lifted it, spun the ball upside down and gave up; after one explanation she used it at once.
2. **The innovation trap:** a much better interface must differ, and difference gets called "not intuitive". Usability ratings that weight "intuitiveness" reward sameness.
3. **Humane:** "An interface is humane if it is responsive to human needs and considerate of human frailties." Users should set the pace. Simple tasks should always be simple, however powerful the system.
4. **Locus of attention:** attention is a spotlight on one thing at a time. Everything outside it is perceived and ignored. Interruptions must be proportional to importance.
5. **Habituation:** repeated actions become automatic, and that cannot be prevented. A confirmation answered "Yes" every time becomes a reflex and protects nothing. The fix is undo, not a cleverer dialog.
6. **Modes:** a mode exists when the same gesture gives different results depending on state that is not at the user's locus of attention. Indicators help but do not solve mode errors. Eliminate modes; convert the rest into quasimodes (held physically, like Shift). Transient modes cause fewer errors than persistent ones.
7. **Noun-verb over verb-noun:** choose the object first, then the action; fewer cancel steps, focus returns to the content. Palettes in paint tools are the accepted exception.
8. **Monotony:** ideally exactly one way to achieve each effect, which speeds habituation. Users given several ways usually settle on one anyway.
9. **Visible versus invisible features:** invisible features must be memorised or hunted for.
10. **Preferences are modes in disguise.** Designers should design an effective interface rather than hand the decision to inexpert users, who optimise for liking rather than usability. Adaptive interfaces that rearrange themselves prevent habituation.
11. **Content persistence and universal undo:** save continuously so "Save" disappears; make every action reversible so exploring is safe.
12. **Quantify:** task time, error rate, learning time, retention after non-use. Some changes called improvements measured worse.

## Where this lives in the skill

`principles/intuitive-design.md` section 1, `principles/heuristics.md` section 4, modes in `principles/affordances-signifiers-feedback.md` section 9, habituation and undo in `principles/errors-and-forgiveness.md`.
