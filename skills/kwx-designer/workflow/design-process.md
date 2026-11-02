# Design process

The order to design anything new: brief, references, reference layout (with directions when the look is open), system first, build, critique, polish. Each step has an output; do not start a step until the previous output exists. For an existing screen, use `redesign-method.md` instead.

## Contents

1. Brief
2. References
3. Reference layout
4. System first
5. Build
6. Critique
7. Polish
8. The whole process as a checklist

---

## 1. Brief

Output: a short written brief (15 lines or fewer).

0. **Day in the life** (5 lines): the 3 tasks the user repeats most, with how often, and the one question they open the product to answer. Each repeated task must be doable in one action with defaults, and the answer must be visible on the first screen (`patterns/daily-use.md`).
1. **Who and what job**: the user, the task they came to do, how often.
2. **Business goal**, as a measurable line. Example from Tim Gabe's workshop: "Ensure 80% of users experience the product's core value within their first two sessions."
3. **Problems to solve**, as "How might we..." lines ("...surface the most valuable features early without overwhelming new users?").
4. **Platform and context**: web, desktop, mobile; one hand on a bus or a desk with a mouse.
5. **Content**: the real data, its range (shortest, longest, empty), and what varies (images, counts, names).
6. **Constraints**: existing design system, brand colour, frameworks, accessibility needs.
7. **Success test**: how we will know it works (task time, first win reached, fewer support tickets).

For every house component you use, open its source and write down its real sizes, paddings, default props and the colours it paints (which icon size a disc picks, which fill a pill uses without its on-dark variant); predictions use these numbers, not the names in a design doc.

If the user gave no brief, write one from the request and state your assumptions in one line each. Ask only when a wrong guess would waste the work.

Write the user goal as one sentence and check the finished work against its purpose, not its letter: "send the digest as one message" is not done if the code still loops one email per subscriber. A vague request ("build me X") gets the smallest complete version: the core job with every daily question and move it implies, built now. The left out parts named are options and abstractions, never a daily workflow or information element. When a requested element has no job, say so in one line before building it.

## 2. References

Output: 3 to 6 reference screens from real products, with one line each on what to take from it, and what each shows on the equivalent screen (the facts and actions it puts in front of the user), so gate row J9 can compare your screen with them.

1. Search a pattern library of real apps (Mobbin is the one every video recommends) by flow and screen type: "onboarding", "product page", "pricing", "bottom sheet", "filter and sort", "checkout".
2. Study the **full journey**, not one screen: discover, detail, checkout, confirmation, saved items, tracking (uxpeak). What comes before and after this screen matters as much as the screen.
3. Prefer reference apps known for quality in the same domain: Linear, Notion, Resend, Stripe, Spotify, Apple's own apps, Duolingo for onboarding, Resend and Supabase for pricing.
4. Take mechanisms, not looks: what they ask for and when, how they handle empty and error, what they hide.
5. When an agent can pull references (a Mobbin MCP or similar), use it to build a mood board quickly (Kole Jain built "12 directions" for a banking app in about 2 minutes), then choose one direction deliberately. A mood board is input, never output: decent is the floor everyone can now reach (Tim Gabe's "commodity ceiling").

## 3. Reference layout

Output: a wireframe of content blocks in priority order, before any styling.

1. List the blocks the user needs, in the order they need them. The strawberry reference layout: category label plus badge, title, social proof, price, description, attributes, buy area.
2. Mark side margins and section spacing bands on it.
3. For each block, decide its form from its data (chip, number, avatar, timeline, chart).
4. Rank every action by frequency and importance and place it: always visible, visible icon, hover, menu.
5. Mobile: one job per screen, one scroll direction per section, decide tab bar vs sidebar as home.
6. Write down every state the screen needs (loading, empty first run, no results, error, offline, limit).

### Show directions

When the look or layout is not decided, or for a surface the user sees daily, build 2 to 4 named, genuinely different directions as small working prototypes in the medium the product runs in (Korme for QML, a lavish page for web). Each gets a one paragraph note and its open questions, and uses real data shapes. The user picks; build only the pick, and record the session and the pick in the project notes. In an unattended run pick one, say why in one line, and list the others.

A preview may only use what the viewer's own entry loads. A harness that imports the extra module itself proves nothing (KM12): compare the idea's imports with the viewer's entry, and read the viewer's own log after opening.

## 4. System first

Output: tokens, before the first component. Follow `design-system-first.md`.

- If the project has a design system or token file, use it and add nothing literal. Extend it only through its own mechanism.
- If not: one brand colour to an 11 step ramp, neutrals, semantic colours, one font, a capped type scale, 4 pt spacing, radii, shadows by elevation, state tokens.

## 5. Build

Output: working UI.

1. Build from shared components. A new screen reuses the nav, header, buttons, inputs, empty and error components; never restyle locally. For anything new, follow the reach order in `lean-build.md`: house component, then native element or platform API, then an installed dependency, then new code. Native date, colour and file inputs come before a custom picker unless the brief needs one.
2. Real content of realistic length from the start. No lorem ipsum, no "John Doe".
3. Build every state from the list in step 3, not only the happy case. "Happy case, one HTML file" is the exact prompt that produced the AI look in Tim Gabe's video.
4. Let code tools write logic and features when told exactly what; you own layout, colour, and which cards exist (Kole Jain).
5. Every literal size, colour and duration goes through a token.

## 6. Critique

Output: a findings list. Follow `quality/critique-method.md`.

1. Squint and blur, count the primaries.
2. Stress the content (dark, bright, busy, long, empty).
3. Screen 80 next to screen 1.
4. Break it on purpose.
5. Compare with a reference app at the same zoom.
6. The three questions per action.
7. Check against `quality/ai-slop-tells.md`.

## 7. Polish

Output: the gate report.

1. Fix every finding, blockers first.
2. Go beyond fixing: what would make the task itself easier? (Sticky action area, total in the button, presets from data, cross sell, the title moving into the nav.) "Strong product design is not just about fixing what is broken. It's about making the whole experience feel easier."
3. Add micro interactions only where a result is otherwise invisible (copy, save).
4. Spend the remaining effort on the worst moment (a failure), not the home screen: that is where premium is decided.
5. Run `quality/quality-gate.md` in full. Ship on its line: no `[critical]` row fails and no open FAIL. The scoring rubric is not used for builds.

## 8. The whole process as a checklist

Mirrors the workflow in SKILL.md.

```
[ ] 1 House first: local mistakes library in full, quality/mistakes-library.md, house/owner-house-style.md (this user), the project's design system, the source of each house component used
[ ] 2 Brief: who, job, platform, what exists; day in the life (3 repeated tasks with frequency, the one daily question)
[ ] 3 Job sized (tiny fix, one screen, new product) and its recipe in SKILL.md opened
[ ] 4 3 to 6 references, what each shows on the equivalent screen (skip for a tiny fix)
[ ] 5 System: tokens through one scale, or the existing system loaded
[ ] 6 Structure: daily questions answered, one primary action, what is hidden until needed; directions shown when the look is open
[ ] 7 Built: reuse first, real content and data shapes, every state
[ ] 8 Predicted and critiqued: quality/predict-from-code.md arithmetic, each mistakes entry one line
[ ] 9 Quality gate: every row run, criticals and FAILs written up, report written
```
