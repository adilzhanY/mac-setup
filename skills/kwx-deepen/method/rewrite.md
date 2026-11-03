# Step 6: rewrite the task, then do it

## The order of the rewrite

1. The deliverable and its size as a number: 300 words, one page, one PR touching 2 files,
   five slides, one function. The same as a plain answer would be. Anything beyond that number
   which is not part of the proof goes on the not doing list, and before finishing, compare the
   result with the number (a 300 word post that came out at 900 words is bigger, not deeper).
2. The inputs to fetch (step 3).
3. The method (step 4).
4. The proof, defined now (step 5).
5. The not doing list: every tempting addition from step 2 that failed the deeper test, one
   line each, plus anything outside the real goal.
6. Assumptions, only if a guess was needed.

The output block in `SKILL.md` shows these, plus the expert, the real goal and the moves,
in at most 10 lines. When the rewrite is handed to another agent, or is itself the
deliverable (an improved prompt), write it as plain instructions instead, like the code
blocks at the end of each playbook's worked example.

## Rules for the text

- Write moves, not personas: no "act as", no "you are a world class".
- No shouting ("CRITICAL", "MUST", capitals) and no contradictions. Newer models follow
  instructions literally and over react to emphasis.
- If the deeper version would change what is delivered, not only how it is made, say so in
  one sentence and let the user choose before doing it. Never quietly turn "fix this email"
  into "rewrite the onboarding".
- When the user asked to improve a prompt rather than run it, the rewrite is the
  deliverable: give the rewritten prompt and stop.

## After the work: look back

Run the proof and report what it showed (Polya's last step: look back). Then one line in
`lessons.md` if a move or a proof paid off or turned out to be noise.
