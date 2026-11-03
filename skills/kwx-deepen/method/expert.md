# Step 1: name the expert, then turn them into moves

The expert is a way to retrieve methods, cues and checks. The name on its own does
nothing: studies of persona prompts found that "you are an expert in X" does not raise
accuracy and sometimes lowers it, even when the expert matches the domain. What helped was
content: a description of how the expert works, and the steps they would take
(`sources/research_notes/prompting-evidence.md`, persona section).

## Write one sentence

Role, narrow specialty, and the situations they have handled. Concrete enough that two
readers would picture the same person.

| Weak | Strong |
|---|---|
| A senior developer | A payments backend engineer who has handled chargebacks and double charge incidents at a mid size shop |
| A writing expert | A technical recruiter who screens 200 backend CVs a week for fintech roles |
| A data scientist | An experimentation analyst who has run sample ratio checks on hundreds of A/B tests |
| A lawyer | A contract lawyer in the client's jurisdiction who drafts freelance agreements |

Write the description for this exact request; do not pick from a fixed menu.

Prefer an expert from a field with fast, clear feedback on exactly this kind of work (a
site reliability engineer on outages, a copy editor on clarity). Where the field gives
little feedback (long range forecasts, taste), say so and lean harder on step 5
(Kahneman and Klein 2009, in `sources/research_notes/expertise.md`).

## Ask them four questions

Adapted from the probes of the Critical Decision Method (Klein, Calderwood and
MacGregor 1989), an interview method first built from studies of fireground commanders:
1. What do you look at first?
2. What would tell you this case is not the usual one?
3. What does a beginner miss here?
4. What would make you change course halfway?

The answers become the moves in step 2, the raw material in step 3 and the checks in
step 5.

## Never

- Write "act as", "you are a world class" or any persona line into the rewritten task.
  Write the moves instead.
- Use a demographic persona, or a person with less knowledge than the task needs.
- Cite "the expert would agree" as evidence. The expert is a source of questions, not of
  proof.
