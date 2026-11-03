# Step 5: the outside proof

This is the step the evidence supports most strongly. A model asked to check and correct
its own reasoning without outside feedback often gets worse (in Huang et al. 2024, GPT-3.5 on
CommonSenseQA fell from 75.8 to 38.1 percent); models rate their own outputs higher than others'; and people
and reward models favour answers that agree with them. So the proof can come from neither
the author nor the requester (`sources/research_notes/prompting-evidence.md`, verification;
`sources/research_notes/raw-material-and-proof.md`, part B).

## What counts

The proof must carry information the author did not supply:
- a test written from the spec before reading the code, seen failing first;
- a measurement against a baseline recorded before the change;
- an official or reference value (the regulator's calculator, a standard's test vectors,
  a known correct example);
- a primary source that states the fact, quoted with its location;
- a reproduction by a fresh run, a clean checkout, or a second agent given only the raw
  inputs, whose output (a rerun, an extraction, a completed task) can be compared;
- real users doing the task, or real behaviour data.

## How to run it

1. **Define it before the work**, as pass or fail where possible, so it cannot be bent to
   fit the result.
2. **Prefer two checks that fail in different ways**, for example a test and a
   measurement, or a source and a rough estimate (triangulation).
3. **Answer fact checks without the draft in view.** Write the check questions, answer each
   one fresh from the source, then compare with the draft (chain of verification).
4. **Report the evidence**, not the word "verified": the command and its output, the quote
   and its location, the number and how it was measured.
5. **If it fails, say so**, fix, and run it again.

## What does not count

- "I reviewed it and it looks right."
- "The user approved it."
- A generic "double check" step: it adds cost without finding more.
- Agreement between several samples of the same model: a weak signal, never proof.
- A fresh agent's opinion that the work looks good: it finds issues, but it is still a
  model's judgment.

## When no outside check exists

Say so plainly in the rewrite (`Proof: none available; the result rests on X`) instead of
sounding confident. Taste and long range forecasts often fall here; then the best you can
do is a reference class figure and a clear statement of the uncertainty.
