# One shared plan for kwx-designer, kwx-developer and kwx-tester

Rule: before any subagent starts, the main agent writes ONE PLAN.md in the scratchpad (never in the repo unless the owner asks). Each skill reads it and appends only its own section. Nobody re-derives the spec, the states or the risks.

Evidence: in the 2026-11-01 trial each skill rewrote the spec, states and risks in its own pass, at 2.2 to 3.2 times the output tokens of the arm without skills. The kwx-designer and kwx-tester skills use the same section names and point to this file.

## The sections of PLAN.md

Numbered, written by the main agent. One example line each:

1. **Owner rules.** The binding lines of `~/.claude/CLAUDE.md` and the project's CLAUDE.md, quoted; the agent definitions the task uses; the defect library entry ids that apply to this job.
   `"Never output the em dash or the en dash." (global CLAUDE.md); agents: ui-designer; mistakes.md entries 3, 7, 12`
2. **Day in the life.** Who uses it, the 5 jobs they repeat, the operator's jobs (`workflow/new-project-from-brief.md` section 3).
   `Freelancer, daily: start a timer, add yesterday's 1,5 h, check this week's total, invoice last month, export for the accountant`
3. **Acceptance criteria.** The requirement matrix rows: id, item, proof, status.
   `R4 | "invoices are numbered without gaps" | invoice.number.test.ts | done`
4. **States per screen.** The duet contract part 1 (`workflow/duet-with-kwx-designer.md` section 2).
   `Overview | empty week | "No hours this week" and the quick entry | items: []`
5. **API shapes, error codes, hook signatures.** The duet contract parts 2 and 3, including every derived value a screen shows.
   `GET /entries?from&to -> { items: Entry[], totalMinor, perProject: {id, minutes, amountMinor}[] }`
6. **Risk list.** Money, dates and zones, auth and abuse, data loss, the brief's hard rules.
   `Rounding: seconds per project to minutes once, half away from zero; VAT on the net total`
7. **Size class and subagents.** The size class (`SKILL.md` rule 11) and which subagents run, with one line why each.
   `Large; developer subagent (API and data), ui-designer (screens), one tester round (money and dates)`
8. **Not in scope.** What is out, and the variants beyond the brief that are deferred, with their trigger.
   `Localized 404 per language: deferred until the client asks; one bilingual 404 now`

## Appended sections

Each skill appends one section under its own name, and touches nothing else:

- **designer:** tokens, the screen list, the defect library entries checked.
- **developer:** files and their order, the Files read line (`SKILL.md` rule 10), the phase budget.
- **tester:** the test plan, by acceptance criterion id.

## Rules

- Every subagent brief names the PLAN.md path and the rows it owns.
- No subagent writes its own acceptance list. A subagent that finds a missing criterion reports it to the main agent.
- Changes to sections 3 to 5 go through the main agent, which updates the plan and tells both sides (`workflow/duet-with-kwx-designer.md` section 6).
- The plan stays in the scratchpad. The repo gets the code, the types file and the README, not the plan.

## Checks

| Check | Pass condition | How to verify |
|---|---|---|
| One plan | the same PLAN.md path is in every subagent brief | read the briefs |
| Owner rules quoted | section 1 quotes the binding global rules and names the defect library ids | read PLAN.md section 1 |
| No second spec | no subagent output contains its own acceptance list | read the subagent reports |
