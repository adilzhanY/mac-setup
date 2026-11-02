# ISTQB Certified Tester Foundation Level Syllabus v4.0.1, and the ISTQB Boundary Value Analysis white paper

- Authors: ISTQB; white paper by Matthias Hamburg and Adam Roman
- Year: syllabus v4.0 2023 (v4.0.1 current); white paper 2025
- Legal URL: https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/ (free download, syllabus id 3345); white paper https://istqb.org/wp-content/uploads/2025/10/Boundary-Value-Analysis-white-paper.pdf

## What I read

Syllabus chapter 4 (black box, white box and experience based techniques) and chapter 5 sections 5.1 and 5.2 (test plan, entry and exit criteria, estimation, prioritization, pyramid, quadrants, risk). The whole white paper.

## Key lessons used in strategy/test-design-techniques.md and strategy/strategy.md

- EP coverage items are partitions, including invalid ones; "each choice" coverage for several inputs.
- BVA applies to ordered partitions; 2 value (boundary plus neighbour in adjacent partition) vs 3 value (boundary plus both neighbours); 3 value catches `x <= 10` written as `x == 10`.
- BVA steps: domain, partitions, boundary values, coverage items, union, test cases; login length 6 to 15 worked example.
- Decision tables: feasible columns are coverage items; tables reveal gaps and contradictions; minimize or use risk when columns explode.
- State transition coverage: all states, valid transitions (0 switch, most used), all transitions (minimum for safety critical); one invalid transition per test to avoid defect masking.
- White box testing cannot find requirements that were never implemented.
- Error guessing categories and fault attacks; checklists should not hold items that can be automated.
- Test plan contents, entry and exit criteria (out of time is a valid exit if stakeholders accept the risk), DoR and DoD.
- Risk level from likelihood and impact; product vs project risks; risk based testing.
