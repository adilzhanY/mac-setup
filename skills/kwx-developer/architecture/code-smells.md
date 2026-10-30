# Code smells: catalog with TS and Rust shapes, detection and fixes

A smell is "a surface indication that usually corresponds to a deeper problem" (Fowler). It is a lead, not a verdict: "some long methods are just fine". For each smell: how it looks, how to detect it by reading or by command, and the refactoring that usually fixes it (names from Fowler's catalog at refactoring.com, so they can be looked up). Then Ousterhout's red flags, then the smells AI agents add most often.

## Contents

1. Fowler's smells (Refactoring, 2nd edition, chapter 3)
2. Ousterhout's red flags
3. Smells agents add (check every diff for these)
4. Checks

## 1. Fowler's smells

**Mysterious Name.** A name that does not say what the thing does or is. Detect: you had to read the body to know what it returns. Fix: Change Function Declaration (rename), Rename Variable, Rename Field. If no good name comes, the design is unclear (`naming.md`).

**Duplicated Code.** Same logic in several places. Detect: `npx jscpd`; same bug fixed twice in `git log`. Fix: Extract Function, Slide Statements, Pull Up Method. Apply the knowledge test first (`abstraction-and-duplication.md`).

**Long Function.** Detect: eslint `max-lines-per-function`, clippy `too_many_lines`; more importantly, comments that label sections ("// validate", "// save") and deep nesting. Fix: Extract Function on each commented section, Decompose Conditional, Replace Conditional with Polymorphism, Split Loop. Do not split conjoined code that must be read together (Ousterhout: depth over length).

**Long Parameter List.** TS `createUser(name, email, role, orgId, sendEmail, isAdmin, locale)`; Rust clippy `too_many_arguments` (default 7). Fix: Introduce Parameter Object, Preserve Whole Object, Replace Parameter with Query, Remove Flag Argument. In Rust a builder or a config struct.

**Global Data.** Module level mutable variables, singletons, `static mut`, `lazy_static` with interior mutability used as shared state. Detect: `rg -n "^(export )?let " src`; `rg -n "static mut|OnceLock<Mutex|lazy_static" `. Fix: Encapsulate Variable (wrap in functions with one owner), pass state explicitly.

**Mutable Data.** A value mutated in many places; a function that mutates its argument and returns it. Detect: `rg -n "\.push\(|\.splice\(|\bdelete \w+\[" src` on parameters; `&mut` threaded widely in Rust. Fix: Split Variable, Separate Query from Modifier, Replace Derived Variable with Query, return new values. Rust's ownership helps; watch for `RefCell` and `Arc<Mutex<_>>` used to dodge design.

**Divergent Change.** One module changed for many unrelated reasons (DB schema changes and UI copy changes both edit `user.ts`). Detect: `git log --format=%s -- path/file.ts | head -30` shows unrelated commit topics. Fix: Split Phase, Move Function, Extract Class: one module per reason to change.

**Shotgun Surgery.** One change needs small edits in many modules (adding a field touches type, form, validation, API, mapper, test fixtures, email template). Detect: `git log --stat` on feature commits touching many folders; grep for the field name. Fix: Move Function, Move Field, Combine Functions into Class, Inline Function to gather the knowledge into one module. It is the reverse of divergent change; both are change amplification.

**Feature Envy.** A function that uses another module's data more than its own (`order.customer.address.country.taxRate` logic living in the cart UI). Detect: count references to the other object's fields. Fix: Move Function to where the data is, or Extract Function then move.

**Data Clumps.** The same group of values passed together everywhere (`lat, lng`; `start, end`; `amount, currency`). Fix: Introduce Parameter Object or Extract Class; in Rust a struct or newtype. Then look for behaviour that belongs on it.

**Primitive Obsession.** Strings and numbers standing for domain concepts: `status: string`, money as `number`, IDs as plain strings that can be swapped. TS fix: string literal unions, branded types (`type UserId = string & { __brand: 'UserId' }`), a `Money` value. Rust fix: newtypes (`struct UserId(Uuid)`), enums instead of strings. Fowler: Replace Primitive with Object, Replace Type Code with Subclasses.

**Repeated Switches.** The same `switch` or `if` chain on a type code appears in several places, so adding a case means finding them all. Detect: `rg -n "case '(draft|sent|paid)'" src` showing multiple files. Fix: Replace Conditional with Polymorphism, or one lookup table keyed by the type. In Rust one `match` in a method on the enum, and rely on exhaustiveness (no `_ =>` arm, so the compiler finds every site when a variant is added). In TS use a `Record<Status, ...>` or a `switch` with an exhaustive `never` check.

**Loops.** Imperative loops where a pipeline says the intent more directly. Fix: Replace Loop with Pipeline (`filter`/`map`, Rust iterators). Do not convert loops with early exits or complex state into unreadable chains.

**Lazy Element.** A function, class or module that does not pull its weight: a wrapper that renames, a class with one trivial method, a file with one re-export. Fix: Inline Function, Inline Class, Collapse Hierarchy.

**Speculative Generality.** Hooks, parameters, abstract classes, generic type parameters and config "in case we need it". Detect: interfaces with one implementation, parameters always passed the same value, generics instantiated with one type, unused options. `npx knip` for unused exports. Fix: Collapse Hierarchy, Inline Function, Change Function Declaration to remove parameters, Remove Dead Code.

**Temporary Field.** A field set only in some circumstances, `undefined` the rest of the time, so readers wonder why it is empty. Fix: Extract Class for the fields that go together; Introduce Special Case; in Rust an enum whose variants carry only the data valid in that state.

**Message Chains.** `a.getB().getC().getD().value`, `config.services.payments.stripe.keys.live`. Callers are coupled to the whole navigation path. Fix: Hide Delegate, or Extract Function and Move Function so the chain lives in one place.

**Middle Man.** A class or module where most methods only delegate. Ousterhout's pass-through methods. Fix: Remove Middle Man, Inline Function. Keep a delegating layer only if it hides something (vendor, caching, auth).

**Insider Trading.** Modules exchanging too much private data, reaching into each other's internals (importing `features/billing/internal/state` from `features/auth`). Detect: deep imports across feature boundaries; Rust `pub` fields read from other modules. Fix: Move Function and Move Field to reduce the talk, Hide Delegate, or extract the shared part into a module both use.

**Large Class.** Too many fields and methods; often several classes inside one. Detect: file and class length, fields used by only some methods (cluster them). Fix: Extract Class, Extract Superclass, Replace Type Code with Subclasses. React equivalent: a component with many `useState` and `useEffect` hooks for unrelated concerns; extract custom hooks or child components per concern.

**Alternative Classes with Different Interfaces.** Two modules doing the same job with different method names (`S3Storage.put` vs `LocalStorage.save`). Fix: Change Function Declaration to align them, then Extract Superclass or an interface. This is a consistency finding too.

**Data Class.** A record with fields and no behaviour, while the logic that uses it is spread over callers. Fix: Move Function to put behaviour on the data, Encapsulate Record. Exception: plain data transfer types at boundaries (API DTOs, serde structs) are fine as data classes; that is their job.

**Refused Bequest.** A subclass that ignores or overrides away most of what it inherits. Fix: Replace Subclass with Delegate, Replace Superclass with Delegate. Prefer composition; in TS avoid deep class hierarchies; in Rust prefer small traits.

**Comments.** Comments that explain what confusing code does are a smell of the code (Fowler: Extract Function, Rename, Introduce Assertion). Comments that explain why, invariants, units, and interface contracts are not a smell; Ousterhout argues they are essential and that missing interface comments cost more than imperfect ones. Delete comments that restate the code; keep and write the why.

## 2. Ousterhout's red flags

From A Philosophy of Software Design. Each signals complexity; check new code for them.

| Red flag | What it looks like | Fix |
|---|---|---|
| Shallow module | Interface nearly as complex as the body | Merge into caller or a deeper module |
| Information leakage | One design decision visible in several modules | Move the knowledge into one module |
| Temporal decomposition | Modules named by when things happen (`read`, `process`, `write`) that share format knowledge | Re-cut by knowledge (`modules-and-boundaries.md` section 1) |
| Overexposure | Common use requires learning rarely used features or options | Defaults for the common case; separate advanced API |
| Pass-through method | Method forwards to another with the same signature | Remove the layer or give it a real job |
| Repetition | The same nontrivial code appears again and again | Find the missing abstraction |
| Special-general mixture | Feature specific code inside a general mechanism | Push specialisation up or down |
| Conjoined methods | Cannot understand one without reading the other | Merge, or redraw the boundary |
| Comment repeats code | The comment adds nothing beyond the code | Delete it, or write what the code cannot say |
| Implementation documentation contaminates interface | Interface doc explains internals callers do not need | Move to implementation comments |
| Vague name | `data`, `info`, `handle`, `result` | Precise name (`naming.md`) |
| Hard to pick name | No short precise name exists | The entity does too much or has no clear purpose; redesign |
| Hard to describe | The doc comment must be long to be complete | The interface is too complex; simplify |
| Nonobvious code | Behaviour or meaning cannot be understood quickly | Better names, a comment on the why, or restructure |

## 3. Smells agents add (check every diff for these)

These come from how coding agents work: each file written in isolation, a bias toward "complete" looking code, and no memory of what already exists. Check every agent diff, including your own, for them.

| Smell | Looks like | Detect | Fix |
|---|---|---|---|
| Parallel helper | A new `formatDate`, `cn`, `sleep`, `retry`, `debounce` beside an existing one | `rg -n "function <name>\|const <name> =\|fn <name>"` before adding | Use the existing helper |
| Convention drift | New file uses default export, arrow form, other import style than its folder | `scan_conventions.py` before and after | Match the area (`consistency.md`) |
| Defensive noise | `try/catch` that logs and continues; `?? []` and `?.` on values that cannot be null; `if (!x) return` on typed non-optional params | `rg -n "catch \(\w+\) \{\s*console" src`; read types | Remove; handle errors at the boundary |
| Speculative options | New function with options nobody passes, `config` objects for one call | read call sites | Delete the option |
| Layer cake | Controller, service, repository for a CRUD read | read: each layer forwards | One handler (`modules-and-boundaries.md` section 2) |
| Wrapper for a library | `export const http = { get: (u) => axios.get(u) }` | read | Use the library, or wrap only to hide a real decision (auth, base URL, retries) |
| Type duplication | A hand written type copying a generated one or a zod schema | `rg -n "interface User\b\|type User =" src` | Derive (`z.infer`, generated types, `Pick`/`Omit`) |
| Stringly typed state | `status: string` where a union exists elsewhere | grep the union name | Reuse the union or enum |
| Narrating comments | `// Loop through users`, `// Return the result` | read | Delete; keep why comments |
| Dead scaffolding | Unused imports, unused params prefixed `_`, unused exports, commented-out code, `TODO: implement` stubs | `npx knip`; `tsc --noUnusedLocals --noUnusedParameters`; `cargo clippy` dead code warnings | Delete |
| `any` and `as` escapes | `as any`, `as unknown as T`, `// @ts-ignore`, Rust `.unwrap()` on input paths | `rg -n "as any\|as unknown as\|@ts-ignore\|@ts-expect-error" src` | Type it properly; validate at the boundary |
| Version suffixes | `UserCardNew.tsx`, `handlerV2`, `old_parse` left behind | `rg --files \| rg "(New\|V2\|Old\|Legacy\|Copy)\."` | Finish the migration, delete the old |
| Silent behaviour change in a refactor | A "cleanup" that also changes a default, an order, or an error message | diff review; tests at the caller level | Split structure from behaviour (R17) |

## 4. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| No new copy paste | jscpd reports no new clones in changed files | `npx jscpd --min-lines 8 <changed paths>` |
| No repeated switches on one type code | Each type code has one dispatch site or an exhaustive table | `rg -n "case '<value>'" src` shows one file per type |
| No new pass-through layers | New functions do more than forward | read the diff |
| No speculative generality | No new interface with one implementation, no option without a caller setting it | `rg -n "implements <Iface>\|impl <Trait> for"`; read call sites |
| No dead code left | Zero unused exports, locals, imports | `npx knip`; `tsc --noEmit --noUnusedLocals --noUnusedParameters`; `cargo clippy -- -D warnings` |
| No type escapes added | No new `as any`, `@ts-ignore`, non-test `unwrap()` on input | `git diff \| rg "^\+.*(as any\|@ts-ignore\|\.unwrap\(\))"` |
| Agent smells table clear | Every row in section 3 checked against the diff | walk the table |
| Ousterhout red flags | No new shallow module, leakage or conjoined pair | read the diff against section 2 |
