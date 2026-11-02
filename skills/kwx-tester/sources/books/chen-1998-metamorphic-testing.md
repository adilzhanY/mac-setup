# Metamorphic Testing: A New Approach for Generating Next Test Cases

- Authors: T. Y. Chen, S. C. Cheung, S. M. Yiu
- Year: 1998 (Technical Report HKUST-CS98-01; posted by the authors on arXiv in 2020)
- Legal URL: https://arxiv.org/abs/2002.12543

## What I read

The full report: motivation (successful test cases carry information; oracles are often unattainable, citing Weyuker), the binary search and shortest path examples.

## Key lessons used in strategy/test-oracles.md

- Build follow up test cases from successful ones, using relations that must hold between outputs, so no oracle for a single output is needed.
- Shortest path example: checking that a path is the shortest is hard, but relations between related inputs (subpaths, swapped endpoints) are easy to check.
- Binary search example: rerun with a key taken from the array; the program must find it.

The later survey (Chen, Kuo, Liu, Poon, Towey, Tse, Zhou, "Metamorphic Testing: A Review of Challenges and Opportunities", ACM Computing Surveys 51(1), 2018) is cited but was not read: the author repository copy sits behind a Cloudflare challenge that the tools here could not pass.
