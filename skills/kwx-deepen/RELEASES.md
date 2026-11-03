# Releases

Semantic versions. A change to the six steps, the gate or the output block is minor or
major; a new playbook or rule is minor; wording and fixes are patch. Every release runs
`python3 scripts/check_skill.py` clean and gets a git tag `vX.Y.Z`.

## 1.0.1 (2026-11-03)

- MIT licence added; the repository is public.

## 1.0.0 (2026-11-03)

First release.
- The gate (step 0) and six steps: expert turned into moves, unasked moves with the deeper
  test, raw material fetched not recalled, runnable methods, an outside proof defined before
  the work, a rewrite with the same deliverable size and a not doing list.
- Built on three research notes: expertise (44 sources), prompting and agent evidence (46),
  sources and verification (37). Key changes from the original "deeper, not bigger" prompt:
  no persona labels, a trigger gate, a question gate, a cap of 3 to 5 moves, and a proof that
  can never be the author's or the requester's judgment.
- Nine field playbooks with one shape: software, design, data, research, writing, learning,
  media, product, business (money and legal).
- Worked examples, a lessons log, trigger and behaviour evals, and `scripts/check_skill.py`.
- First eval (evals/results-2026-11-03.md, 6 cases, one run each, graded by reading): 19 of 22
  assertions with the skill against 10 of 22 without. Fixes from it are in this release: the
  size stated as a number and checked at the end, the person's own numbers asked first for
  personal decisions, no conclusion from an unfetched law, the growing login delay written
  into the software move, a silent skip on trivial work, and a description that names the
  implicit task types and works alongside other skills.
- Known gaps: several book sources were read through summaries and are marked (secondary)
  in the notes; market research and interview preparation have no dedicated method source;
  the evals have not yet been run against a live model.
