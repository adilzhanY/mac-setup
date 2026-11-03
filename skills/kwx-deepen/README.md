# kwx-deepen

A Claude Code skill that turns a request into a deeper version of itself, not a bigger
one, and then does the work.

Most requests are a summary of what someone wants. A top professional hears the same words
and does something different: they find the real goal, start from the primary record
instead of a summary, use a method they could name, and decide in advance what would prove
them wrong. kwx-deepen makes that difference explicit while keeping the deliverable the
same size.

## What it does

Before a task that deserves it, the skill shows a short block like this, then does the work
and reports the proof:

```
Deepened: software, same size (one fix, one PR)
Expert: test infrastructure engineer who has hunted timing and shared state flakes in CI
Real goal: a test that fails only when checkout is broken
Moves: reproduce first (50 runs, alone and in the suite); classify the cause before
  touching code; fix the cause, not the wait
Raw material: the last 20 CI logs, the test file, the code it covers
Method: repeated runs with a fixed seed, then shuffled order
Proof: 100 green runs, and the test still fails when the guarded line is broken on purpose
Not doing: refactoring the suite, raising global timeouts, adding retries
```

The steps:
0. **Gate**: skip trivial work; ask at most one round of questions, only when two readings
   lead to different deliverables.
1. **Expert**: a narrow, concrete expert, turned into moves (never an "act as" line, which
   research shows does not improve accuracy).
2. **Unasked moves**: the real goal, a quick pre mortem, 3 to 5 moves that change the
   inputs, the method or the check. Anything that makes the deliverable bigger goes on a
   not doing list.
3. **Raw material**: fetch the code, data, spec, statute or original paper; never cite or
   quote from memory.
4. **Methods**: things that can be run or followed, plus one rough estimate worked out
   another way.
5. **Outside proof**: a check that does not rest on the author's or the requester's
   judgment, defined before the work and able to fail.
6. **Rewrite and do it**: same size, with the proof result at the end.

It includes playbooks for nine fields (software, design, data, research, writing, learning,
media, product, business with money and legal), each listing the experts, the moves they
make unasked, raw material, methods, independent proof, amateur mistakes and scope traps.

## Install

Copy the folder into your Claude Code skills directory:

```
git clone https://github.com/adilzhanY/kwx-deepen ~/.claude/skills/kwx-deepen
```

or copy it into a project's `.claude/skills/` to use it in one project only.

## Use

- Type `/kwx-deepen` followed by your request, or say "deepen this", "go deeper", "do it
  like an expert would" or "improve my prompt first".
- Claude also loads it on its own for vague, short or high stakes requests, and leaves it
  alone for small edits, lookups and anything you ask to keep quick.
- To get only the improved prompt without running it, say so: "deepen this prompt, do not
  run it".

## Make it yours

- Add a line to `lessons.md` after a deepened task (what paid off, what was noise); the
  skill reads the lines for the field next time.
- Add a playbook for your own field in `fields/`, using the same headings as the others,
  and a row for it in the table in `SKILL.md`.
- Run `python3 scripts/check_skill.py` after any change; it checks the structure, the
  links, the versions and the playbook headings.

## Evidence

The rules come from three research notes in `sources/research_notes/`: how experts differ
from novices, what studies show about persona prompts, prompt rewriting and verification
for language models, and how to find primary sources and independent proof. The reading
list is `sources/books-and-papers.md`.

## Versions

See `RELEASES.md`.

## Licence

MIT, see `LICENSE`.
