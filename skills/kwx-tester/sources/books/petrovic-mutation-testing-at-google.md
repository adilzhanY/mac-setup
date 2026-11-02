# Practical Mutation Testing at Scale: A view from Google; Does mutation testing improve testing practices?

- Authors: Goran Petrović, Marko Ivanković, Gordon Fraser, René Just
- Year: 2021 (IEEE TSE / arXiv 2102.11378; ICSE 2021 / arXiv 2103.07189). Builds on "State of Mutation Testing at Google" (Petrović and Ivanković, ICSE SEIP 2018)
- Legal URL: https://arxiv.org/abs/2102.11378 and https://arxiv.org/abs/2103.07189 (arXiv); Google Research page https://research.google/pubs/state-of-mutation-testing-at-google/

## What I read

The arXiv versions of both 2021 papers: introduction, the mutagenesis process, arid node heuristics, evaluation summaries and conclusions. The 2018 paper was read only through its abstract.

## Key lessons used in strategy/mutation-testing.md

- Coverage can mislead when statements are covered but outcomes are not asserted (the Buffer.Append example).
- Mutation testing at Google runs only on changed lines during code review; mutants are surfaced as review findings.
- Evaluation: almost 17 million mutants, 760 000 changes, 2 million mutants surfaced in review; more than 24 000 developers.
- 85% of reported mutants were first judged unproductive; suppressing arid nodes (logging, trivial code) and limiting mutants per line raised productive mutants from 15% to 89%.
- Tests that assert implementation details to kill unproductive mutants are "change detectors" and harm the suite.
- Developers exposed to mutants write more tests over time; mutants were coupled with 70% of a sample of high priority bugs.
