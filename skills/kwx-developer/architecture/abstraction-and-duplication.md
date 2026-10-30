# Abstraction and duplication

When to extract shared code, when to leave duplication alone, how to recognise an abstraction that has gone wrong, and how to undo it. Models over-abstract by default: they extract on the second similar block, add parameters to make a helper fit a new case, and build general frameworks for one use. This file exists to stop that, without swinging to copy paste everywhere.

## Contents

1. DRY is about knowledge, not text
2. When to extract (the decision)
3. When not to extract
4. The wrong abstraction: how it forms and how to spot it
5. Undoing a wrong abstraction
6. Good abstractions: what they look like
7. Detecting duplication
8. Checks

## 1. DRY is about knowledge, not text

Dave Thomas: "Most people take DRY to mean you shouldn't duplicate code. That's not its intention." The Pragmatic Programmer's definition: "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system."

- Two identical blocks that encode different knowledge (validation of a username and validation of a tag happen to share a regex today) are not a DRY violation. They will diverge; merging them couples unrelated things (an orthogonality violation: Hunt, "things that are not related conceptually should not be related in the system").
- Two different looking blocks that encode the same knowledge (a price calculated in the cart component and again in the order email template) are a DRY violation even though no text matches. When the pricing rule changes, one will be missed.
- The test: **if one changes, must the other change for the same reason?** Yes: one knowledge, extract. No: coincidental similarity, leave it.

Knowledge that must have exactly one home: business rules and formulas, constants with meaning (limits, prices, role names, status values), schemas and their validation, URL and route definitions, permission checks, mappings between enums and labels, the shape of an API response.

## 2. When to extract (the decision)

Extract when at least one holds:

- **Same knowledge, must change together.** The DRY test above says yes.
- **A bug was fixed in one copy and had to be fixed in another.** That is the evidence (Dodds fixed one bug in eight places).
- **Third occurrence, with the differences understood.** Rule of three: tolerate the second copy, extract on the third, when you can see which parts vary. Dodds (AHA, "Avoid Hasty Abstractions"): "the differences suggest what the function's parameters should be"; wait until you are confident you understand the use cases.
- **The extracted piece has a clean interface** you can name and describe without reading the body (Ousterhout's deep module test).
- **An invariant must be enforced** (a constructor that validates, a type that cannot hold an invalid value). Extract even on first use; that is not duplication removal, it is a boundary.

Before extracting, grep for an existing helper that does the job. Adding a second `formatCurrency` next to the first is worse than either duplication or abstraction.

## 3. When not to extract

- Two occurrences that look alike but serve different features owned by different people or changing for different reasons.
- Test code: tests should read top to bottom without jumping to helpers. Duplicate setup in tests is fine until it obscures what each test checks; then use a small builder with named overrides, not a generic fixture factory with flags.
- Configuration and markup that happen to be similar (two forms with the same three fields).
- When the only shared part is structure (a loop, a try/catch, a fetch call) and every caller fills it differently. A higher order function that takes five callbacks is harder than five plain loops.
- When extracting needs a boolean or mode parameter from day one. That is two functions sharing a name.

Abramov's lesson from "Goodbye, Clean Code": he deduplicated a colleague's resize handlers into a compact composed abstraction, and it was right to revert it. The duplicated version would have absorbed the later special cases per shape and handle easily; the abstraction would have become convoluted. "Clean code is not a goal." Optimise for how the code will change, not for how it looks today.

## 4. The wrong abstraction: how it forms and how to spot it

Sandi Metz's sequence:

1. Programmer A sees duplication, extracts it, names it. Looks clean.
2. A new requirement is almost, but not quite, served by the abstraction.
3. Programmer B adds a parameter and a conditional to make it fit.
4. Repeat. The abstraction becomes a tangle of parameters and branches that each caller uses a different slice of.
5. Sunk cost keeps everyone patching it.

"Duplication is far cheaper than the wrong abstraction." "If you find yourself passing parameters and adding conditional paths through shared code, the abstraction is incorrect."

Symptoms to look for in review and audits:

- A shared function with boolean parameters (`render(item, true, false)`), or an options object whose fields are each used by one caller.
- A `type`, `mode`, `variant` or `kind` parameter whose branches share almost no code.
- `if (caller === 'checkout')` or checks on which feature is calling.
- Callers that pass `undefined`/`null` for half the parameters.
- A generic component (`<DataTable>`, `<Form>`) with 20+ props, most used by one screen.
- Every change to the shared code needs re-testing every caller, and people are afraid to touch it.
- A Rust trait with one implementation plus a pile of `where` clauses, or a generic function instantiated with one type.

```ts
// Wrong abstraction, grown by accretion.
export function formatPrice(cents: number, opts: {
  currency?: string; compact?: boolean; forEmail?: boolean; hideZero?: boolean
} = {}) {
  if (opts.hideZero && cents === 0) return ''
  if (opts.forEmail) return `${(cents / 100).toFixed(2)} ${opts.currency ?? 'EUR'}`
  if (opts.compact) return compactFormat(cents, opts.currency)
  return new Intl.NumberFormat('de-DE', { style: 'currency', currency: opts.currency ?? 'EUR' })
    .format(cents / 100)
}
// Each caller uses one branch. Better: three small functions (or inline at the
// email call site), sharing only what is truly common (cents -> major units).
```

## 5. Undoing a wrong abstraction

Metz's steps, done as a structure-only change:

1. **Inline** the abstraction into every caller (each caller gets a copy of the body).
2. In each caller, use the arguments it actually passes to **delete the branches that caller never runs.**
3. Delete the now unused parameters and the shared function.
4. Look at the remaining copies with fresh eyes. Re-extract only what is truly the same knowledge, based on current requirements.

"When the abstraction is wrong, the fastest way forward is back." Do this before adding the next parameter, not after.

Keep tests green at each step. If the abstraction has no tests, write characterisation tests at the caller level first (see `evolving-a-codebase.md`).

## 6. Good abstractions: what they look like

- Named for what they are in the domain, not for the code they contain (`taxFor(order)`, not `calculateValues()`).
- A small interface hiding a meaningful decision (Ousterhout's deep module).
- Somewhat general purpose: the interface does not mention any one caller's concept (no `forCheckoutPage` parameters).
- Stable: callers do not need to change when it changes internally.
- No flags. Variation is expressed through data passed in (a value, a strategy function for a genuine extension point), not through modes.
- Beck's rules of simple design in priority order: passes the tests, reveals intention, no duplicated logic, fewest elements. Fowler notes "no duplication" and "reveals intention" usually reinforce each other; when they conflict, intention wins for the reader (Beck: "empathy wins").

## 7. Detecting duplication

```
# Copy paste detection, TS/JS (and many other languages)
npx jscpd --min-lines 8 --min-tokens 70 --reporters console src
# Repeated literals that carry meaning
rg -o "'(admin|owner|editor|viewer)'" src --no-filename | sort | uniq -c
rg -n "\b(3600|86400|1000 \* 60|0\.19|0\.07)\b" src
# Same helper implemented twice
rg -n "function (format|parse)(Date|Price|Currency|Money)" src
# Rust
rg -n "fn (format|parse)_\w+" crates src
```

For each hit, apply the knowledge test (section 1) before calling it a problem. Report duplicated knowledge (a rule or constant in two places) higher than duplicated code shape.

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Extraction justified | Each new shared helper has 2+ callers that change for the same reason, or enforces an invariant | read importers: `rg -l "<helperName>" src` |
| No existing helper duplicated | No second implementation of an existing helper | grep for the verb and noun before writing (section 7 patterns) |
| No flag growth | Shared functions have no boolean parameters and no mode or type selector with disjoint branches | `rg -n "\((\w+: \w+, )*\w+: boolean" src`; read options types of shared functions |
| No caller checks | Shared code does not branch on who called it | `rg -n "caller\|source === \|from === \|context === '" src/shared src/lib` |
| Knowledge single sourced | Each business constant and rule has one definition | grep the literal; one match outside tests |
| Copy paste under control | jscpd duplication below the repo's baseline; no new clones in the diff | `npx jscpd` before and after |
| Wrong abstractions undone, not patched | A change that needs a new branch in shared code inlines first | read the diff: new `if` on an options field in shared code is a red flag |
