# How to Specify It! A Guide to Writing Properties of Pure Functions

- Author: John Hughes
- Year: 2020 (TFP 2019 proceedings, LNCS 12053, pp. 58 to 83)
- Legal URL: Chalmers research repository, https://research.chalmers.se/publication/517894 (full text PDF https://research.chalmers.se/publication/517894/file/517894_Fulltext.pdf)

## What I read

The full paper: the five kinds of properties on a binary search tree, the note on generation and test data distribution, the bug hunting evaluation (eight planted bugs, Fig. 8 and Fig. 9), lessons and discussion.

## Key lessons used in strategy/property-based-testing.md (also test-oracles.md)

- Five kinds of properties: invariant (validity), postcondition, metamorphic, inductive, model based.
- Validity properties missed five of eight bugs; every bug was found by at least one postcondition, one metamorphic and one model based property.
- Mean tests to failure: model based 5.8, metamorphic 56, postcondition 77. UnionPost needed about 50 tests, the equivalent UnionModel about 8.4, because the model check compares the whole result.
- Metamorphic properties are "less effective individually, but powerful in combination"; weak versions with preconditions missed bugs.
- With time short, write model based plus validity properties; use metamorphic properties when a model is expensive or too close to the implementation.
- Measure the distribution of generated data: in about 80% of tests the key was absent from the tree; a smaller key range fixed it. Collisions matter.
- Test generators and shrinkers for validity, or other properties fail with confusing counterexamples.
- Stateful code needs sequences of operations; state machine models (Quviq) apply the model based idea.
