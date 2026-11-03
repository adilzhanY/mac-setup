---
name: kwx-deepen
description: Turns a request into a deeper version of itself, not a bigger one, before doing it. Names the narrow expert for this exact case and turns them into concrete moves, fetches the raw material (code, data, spec, statute, original paper) instead of summaries, picks methods that can be run, and defines an outside check that can fail, then rewrites the task with the same deliverable size and a not doing list. Playbooks for software, design, data, research, writing, learning, media, product, and business, money and legal. Use when the user types /kwx-deepen or /deepen, asks to go deeper, do it properly or like an expert, or to improve a prompt first; and on vague or high stakes requests where an expert and an amateur differ: a blog post, a pitch, a budget, a lesson, a vendor choice, numbers that look wrong. Works alongside other skills: it rewrites the task, then the skill that makes the file, video or report does the work. Skip trivial edits, lookups, chat, and requests to keep it quick.
---

# kwx-deepen

Version 1.0.1. Changes are listed in `RELEASES.md`.

A request is usually a summary of what someone wants. An expert hears the same words and
does something different: they find the real goal, start from the primary record instead
of a summary, use a method they could name, and decide in advance what would prove them
wrong. This skill makes that difference explicit, keeps the deliverable the same size,
and then does the work.

The evidence behind each rule is in `sources/research_notes/` (expertise research,
prompting and agent studies, sources and verification). Two findings shape everything:
a role label alone does not make a model more accurate, and a model checking its own
work without outside feedback often makes it worse. So the expert is turned into moves,
and the proof always comes from outside.

## When to deepen

Run the method when at least one of these holds:
- The user asks for it: `/kwx-deepen` or `/deepen`, "go deeper", "do it properly", "what would an expert do",
  "improve my prompt first".
- The result will be relied on: money, health, law, security, data loss, a public text, a
  decision, a release.
- Experts and amateurs do this very differently (most tasks in the field playbooks).
- It depends on facts that could be misremembered: versions, numbers, laws, quotes, APIs.
- An outside check exists that the request did not mention (a test, an official value, a
  dataset, real users).

## When not to deepen

Skip the method, and say nothing about it, for: one line edits, renames, typo fixes,
lookups, running a command, formatting, casual conversation, and any request where the
user says to keep it quick or small. The first answer to these is almost always right,
and the extra steps only cost time. If unsure, use the one line form in
`method/gate.md`.

## The six steps

Step 0 is the gate (`method/gate.md`): decide whether to deepen, how much, and whether one
question is needed.

1. **Name the expert, then turn them into moves** (`method/expert.md`). One sentence: role,
   narrow specialty, the situations they have handled. Ask them what they look at first,
   what tells them this case is not the usual one, and what a beginner misses. Never write
   "act as" into the task; write what they would do.
2. **Find what they would do that was not asked** (`method/moves.md`). Name the deep type of
   the problem and the real goal behind the request, run a quick pre mortem, and keep 3 to
   5 moves. A move counts only if it changes the inputs, the method or the check. Anything
   that adds a section, a feature or a file goes to the not doing list.
3. **Get the raw material** (`method/raw-material.md`). Name the primary record (the code,
   the log, the dataset, the spec, the statute, the original paper, the user's own words)
   and fetch it before planning. Never cite, quote or state a version from memory. Record
   where each fact came from.
4. **Name methods that can be run** (`method/methods.md`). A command, a test, a named
   procedure, a statistical test, a search query, a checklist. Add one rough estimate
   worked out a different way wherever there are numbers.
5. **Define the outside proof before the work** (`method/proof.md`). Something other than
   the author and the requester: a test written from the spec, a measurement, an official
   value, a primary source, a reproduction, real users. It must be able to fail. Prefer two
   checks that fail in different ways. If no outside check exists, say so.
6. **Rewrite the task and do it** (`method/rewrite.md`). Same deliverable, same size, with
   the inputs, the method, the proof and the not doing list. If the deeper version would
   change what is delivered, say so in one sentence and let the user choose. Then do the
   work and run the proof.

## Output

Before the work, show the rewrite in this shape, at most 10 lines (one line per field on a
small task):

```
Deepened: <field>, same size (<deliverable as a number: words, pages, files, tests>)
Expert: <role, specialty, the situations they have seen>
Real goal: <the goal behind the request>
Moves: <3 to 5, on one or two lines>
Raw material: <what, and where it was fetched from>
Method: <runnable steps or tools>
Proof: <the outside check, pass or fail, defined now>
Not doing: <the tempting additions, one line each>
Assumptions: <only if a guess was needed>
```

Then do the work. End with the proof result: the command and its output, the quote and its
location, or the measurement. Never write "verified" without the evidence. If the proof
failed, say so and what changed.

## Field playbooks

Read the one playbook that fits before step 1. Each has the expert roles, the moves experts
make unasked, raw material, methods, independent proof, amateur mistakes, scope traps and
a worked example.

| Request is about | Playbook |
|---|---|
| Code: features, bugs, refactors, reviews, APIs, security, infrastructure | `fields/software.md` |
| Screens, flows, design systems, accessibility | `fields/design.md` |
| Analysis, metrics, dashboards, experiments, spreadsheets | `fields/data.md` |
| Answering a factual question, literature, market or competitor research | `fields/research.md` |
| Articles, emails, cover letters, docs, reports, translation | `fields/writing.md` |
| Learning or teaching a topic, courses, exam or interview prep | `fields/learning.md` |
| Video, motion, audio, images, presentations | `fields/media.md` |
| Product ideas, roadmaps, pricing, positioning, launch, choosing a vendor | `fields/product.md` |
| Budgets, estimates, contracts, hiring, job applications, operations, legal | `fields/business.md` |

No playbook fits (travel, cooking, a hobby): use the six steps on their own; they work in
any field. `examples/worked-examples.md` shows the method on short requests from several
fields.

## Rules that hold everywhere

- Deeper, not bigger. The deliverable keeps its size, stated in units (one page, one PR,
  five slides). Depth goes into inputs, method and proof.
- The steps before the work stay much shorter than the work.
- Fetch what is load bearing: numbers, quotes, citations, versions, laws, file contents.
  Popular, stable facts may come from memory; long tail, recent or contested ones may not.
- The proof never rests on the author's or the requester's judgment, and is never a generic
  "double check".
- At most one round of questions, only when two readings lead to different deliverables and
  no tool can settle it (`method/gate.md`). Otherwise state the assumption and go on.
- No shouting ("CRITICAL", "MUST") in the rewrite, and no contradictions.
- Respect the user's own instructions and project files: they win over this skill.
- Do not stack: if the harness or another skill already plans, tests or reviews the work,
  feed this rewrite into it instead of adding a second layer of the same.

## Getting better over time

After a deepened task, add one line to `lessons.md`: which move or proof paid off, and
which was noise. Read the lines for the field before step 1 next time.

## Files

- `method/`: the gate and the six steps in detail.
- `fields/`: nine field playbooks with one shared shape.
- `examples/worked-examples.md`: short before and after rewrites.
- `lessons.md`: the learning log.
- `evals/triggers.json`, `evals/evals.json`: when it should fire and what a good run does.
- `scripts/check_skill.py`: validates the skill (`--selftest` tests the checker).
- `sources/`: research notes and the reading list.
