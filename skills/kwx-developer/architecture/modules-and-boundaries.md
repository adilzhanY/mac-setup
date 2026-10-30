# Modules and boundaries

How to cut a system into modules, which way dependencies may point, how big the public surface should be, and when a formal architecture (ports and adapters, hexagonal, clean) pays for itself. "Module" means any unit with an interface: a function, a file, a class, a folder with a public entry, a package, a crate, a service.

## Contents

1. Decompose by secrets, not by steps (Parnas)
2. Deep modules (Ousterhout)
3. Information leakage and its shapes
4. Somewhat general purpose interfaces, and pulling complexity down
5. Define errors out of existence
6. Dependency direction and stability
7. Cycles: detect and break
8. Public surface and Hyrum's law
9. Ports and adapters: when it pays, when it is overkill
10. Shared domain core for web and mobile
11. Conway's law: boundaries follow teams
12. Checks

## 1. Decompose by secrets, not by steps

Parnas (1972) compared two decompositions of the same program. The conventional one made each processing step a module (read input, shift, sort, print). The better one made each difficult or changeable design decision a module (line storage format, input format, the index representation). His conclusion: "it is almost always incorrect to begin the decomposition of a system into modules on the basis of a flowchart. We propose instead that one begins with a list of difficult design decisions or design decisions which are likely to change. Each module is then designed to hide such a decision from the others."

Ousterhout calls the step based version **temporal decomposition**: code structured by the order operations run (`readConfig`, `parseConfig`, `validateConfig` in three modules that all know the config format). It spreads one decision across many modules.

Rules:

- Before creating a module, write its secret in one sentence. "Hides how sessions are stored (cookie vs DB vs JWT)." "Hides the Stripe API." "Hides the on-disk project format." No secret, no module.
- Group by knowledge. If reading and writing a file format both need to know the format, they belong in one module, even though they run at different times.
- Bad: `upload/validate.ts`, `upload/transform.ts`, `upload/save.ts`, each knowing the CSV column layout. Good: `csvImport.ts` that owns the column layout and exposes `importCsv(file): ImportResult`.

## 2. Deep modules

A module's value is the functionality it provides minus the cost of learning its interface. Deep modules hide a lot behind a small interface (Unix `open/read/write/close/lseek` hides file systems, caching, devices). Shallow modules have an interface nearly as complex as their body.

Red flags that a module is shallow (Ousterhout):

- **Pass-through method**: does nothing but call another method with a similar signature. Often a sign that responsibility between two classes is not clearly divided.
- **Pass-through variable**: a parameter threaded through five layers so the bottom one can use it. Fix with a context object or by moving the decision.
- **Wrapper that renames**: `export const getUser = (id) => db.user.findUnique({ where: { id } })` used once.
- **Classitis**: many tiny classes, each with a constructor and one method, that must all be learned to do one thing.
- **Conjoined methods**: two functions you cannot understand without reading both. Merge them.

Length is not depth. Ousterhout: "Depth is more important than length: first make functions deep, then try to make them short enough to be easily read. Don't sacrifice depth for length." Splitting a 40 line function into eight 5 line functions that are each called once and must be read together makes code harder, not easier. Split when a piece has a clean interface you could describe without reading its body.

```ts
// Shallow: three layers, one job, each must be read.
export class UserRepository { find(id: string) { return db.user.findUnique({ where: { id } }) } }
export class UserService { constructor(private repo: UserRepository) {}
  getUser(id: string) { return this.repo.find(id) } }
export class UserController { constructor(private svc: UserService) {}
  get(req: Req) { return this.svc.getUser(req.params.id) } }

// Deep enough: the handler owns the request, the query is one call.
export async function getUserHandler(req: Req) {
  const user = await db.user.findUnique({ where: { id: req.params.id } })
  return user ? json(user) : notFound()
}
```

Add a layer when it hides something: a second data source, caching, authorisation, a mapping between domain and storage shapes, a transaction boundary. Not before.

## 3. Information leakage and its shapes

Leakage: one design decision is reflected in several modules, so changing it changes all of them. It is the main cause of change amplification. Shapes to look for:

- The same file format, wire format, SQL table shape or JSON shape parsed in two places.
- UI concepts inside a data module (Ousterhout's text editor: `backspace(cursor)` and `deleteSelection(selection)` in the text class, instead of `delete(start, end)`).
- A function whose callers must call it in a certain order (`init()` before `load()` before `start()`), or must call a cleanup.
- A type exported only so callers can build the argument for one function: the module's internals have leaked into its signature.
- Implementation detail in a name or doc: `getUsersFromPostgres()`, a doc comment explaining the cache eviction to callers who should not care.
- Over exposure: a common case API that forces callers to learn rare features (Java's buffered vs unbuffered streams, which almost every caller wants buffered).

Fix by moving the knowledge into one module and giving the others a call that does not reveal it. When two modules share a lot of knowledge, merge them.

## 4. Somewhat general purpose interfaces, and pulling complexity down

From the book's chapter 6 (read in the legal extract):

- "The module's functionality should reflect your current needs, but its interface should not." A text class with `insert(position, text)` and `delete(start, end)` serves backspace, delete key, delete selection and search and replace; `backspace(cursor)` serves one key.
- Questions to ask: What is the simplest interface that covers all current needs? In how many situations will this method be used (one use is a red flag)? Is it easy to use for my current needs (if callers write lots of glue, it is too general)?
- **Push specialisation up or down.** Feature specific behaviour goes up into the feature code or down into a driver or adapter behind a general interface. It does not go into the shared middle.
- **Separate general purpose mechanism from special purpose policy.** The undo example: a `History` class that knows nothing about what actions do, action objects that each know one action, and grouping policy in the UI code. Each part can change without the others.
- **Eliminate special cases.** An empty selection instead of "no selection" removes every `if (selection)` check.
- **Pull complexity downwards.** It is better for one module to absorb a hard case than for every caller to handle it. Config parameters are often complexity pushed up: compute the value when the module can.

## 5. Define errors out of existence

Every error a module can raise is part of its interface and must be handled by every caller. Reduce them:

- Change the semantics so the case is not an error: deleting a key that does not exist succeeds (the postcondition "key absent" holds); `substring` clamps out of range indexes.
- Mask the error low down: retry a transient network failure inside the client so callers never see it.
- Aggregate: let errors propagate to one handler at a boundary instead of handling at every level.
- Crash on errors that are not worth handling (out of memory, corrupted internal invariant), with a clear message.

Do not apply this to errors the caller must react to (validation failures, permission denied, payment declined). Hiding those is a bug.

## 6. Dependency direction and stability

- **Depend toward stability.** A module many things depend on must change rarely; a module that changes often must have few dependents. Martin's instability metric I = Ce / (Ca + Ce) (outgoing over total coupling): dependencies should point from higher I to lower or equal I. In practice: features depend on domain and shared code; domain depends on nothing app specific; shared utilities depend on nothing internal.
- **Policy does not depend on mechanism.** Business rules do not import the HTTP framework, the ORM, React, Expo modules, or a vendor SDK. When the domain needs IO, it declares what it needs (a function parameter or a small interface) and the outer layer provides it.
- **Allowed direction in a typical app:** `app` (routing, composition) -> `features/*` -> `shared` (ui kit, lib) -> nothing internal. And `features/*` -> `domain` (or `core`) -> nothing. Features do not import each other; compose them in `app` (bulletproof-react's rule) or extract the shared knowledge downward.
- **Rust:** crates make direction physical: a lower crate cannot import a higher one, and cycles between crates are impossible. Use crate boundaries for the boundaries that matter most (domain core with no IO deps; adapters depend on it).

Enforce direction with tooling, not hope. Cockburn on layered diagrams: teams treat layer lines as optional, and "adding a layer without a way to detect violations doesn't prevent the problem from returning".

```js
// eslint.config.js (eslint-plugin-import)
'import/no-restricted-paths': ['error', { zones: [
  { target: './src/features/billing', from: './src/features', except: ['./billing'] },
  { target: './src/features', from: './src/app' },
  { target: ['./src/components', './src/lib', './src/hooks'], from: ['./src/features', './src/app'] },
  { target: './src/domain', from: ['./src/components', './src/app', './src/features'] },
]}]
```

Alternatives: `dependency-cruiser` (`forbidden` rules, also catches cycles and orphans), `eslint-plugin-boundaries`, Nx `enforce-module-boundaries` with tags.

## 7. Cycles: detect and break

A cycle means neither module can be understood, tested or reused without the other; they are one module pretending to be two. In JS/TS cycles also cause `undefined` at import time and bundler errors.

Detect:

```
npx madge --circular --extensions ts,tsx src
npx depcruise src --validate     # with a no-circular rule
# eslint: 'import/no-cycle': ['error', { maxDepth: 10 }]  (slow on big repos; run in CI)
cargo modules dependencies --lib --acyclic   # module level cycles inside a crate
```

Break, in this order of preference:

1. **Move the shared piece down.** Usually both modules need one type or helper; move it to a module both import.
2. **Merge.** If the two modules share a lot of knowledge, they are one module.
3. **Invert.** The lower module defines a callback or interface parameter; the higher one passes the implementation in.
4. **Events.** Only when the dependency is a notification, not a query.

Barrel files are the most common cause of cycles in TS apps: a file imports `../index`, which re-exports the file itself.

## 8. Public surface and Hyrum's law

Hyrum's law: "With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody." Inside one app, "users" are the other modules, and they will depend on ordering, timing, error messages and fields you never meant to promise.

- Export the minimum. Every export is something someone can import tomorrow; unused exports are dead weight for readers and block refactors (`npx knip`).
- Expose a feature's public API deliberately: either a single entry file that is the only allowed import path from outside (enforced by lint), or direct file imports with lint rules forbidding deep imports into another feature's internals. Pick one per repo.
- In packages, use `package.json` `"exports"` to make internals unimportable.
- In Rust, private by default; `pub(crate)` for crate internals; `pub` items in a library are the API. `#![warn(unreachable_pub)]` finds `pub` items that are not reachable from outside the crate.
- Do not return internal mutable structures; return copies, views or read only types.
- Randomise or document what you do not promise (iteration order, error text) if consumers are external.

## 9. Ports and adapters: when it pays, when it is overkill

Cockburn's intent: let the application be driven equally by users, programs, tests and batch scripts, and be developed and tested in isolation from its UI and databases. A **port** is a purposeful conversation ("for getting exchange rates", "for notifying users"); an **adapter** converts between the port and a technology (Postgres, Stripe, an HTTP handler, a test fake). He recommends two to four ports, not one per use case.

Use it (explicit interfaces for driven ports, domain free of IO) when at least two hold:

- Real business rules exist beyond CRUD: pricing, scheduling, permissions, state machines, calculations.
- More than one driver: HTTP and a queue worker and a CLI, or web and mobile sharing logic.
- An external system is slow, costly or flaky to test against (payment provider, LLM, hardware) and you need a fast fake.
- An infrastructure choice is genuinely likely to change (moving off a vendor, offline first sync).

It is overkill when:

- The app is CRUD over one database with validation. A handler that validates and calls the ORM is the right depth.
- An interface would have exactly one implementation and no test double need. That is speculative generality (R16).
- The "domain" would just copy ORM types into identical domain types with mappers both ways.

The cheap version that usually suffices: keep calculations and rules in pure functions that take plain data (functional core), and keep IO in handlers and small adapter modules (imperative shell). Introduce a formal port only at the one or two seams that need swapping.

## 10. Shared domain core for web and mobile

When a web app and a mobile app (Expo or native) share business rules:

- Put the shared code in a workspace package (`packages/core`, `packages/domain`) consumed with `"workspace:*"`. It contains types, validation schemas, pure business logic, formatting, and API client contracts.
- The core must not import platform code: no `react-dom`, `react-native`, `expo-*`, `next/*`, `window`, `document`, Node built-ins, or a storage API. Enforce with lint (`no-restricted-imports` in the package's eslint config) and by keeping those out of the package's dependencies.
- Platform specific IO (storage, notifications, secure store, fetch with auth) is injected or lives in each app.
- Share UI only through a deliberate cross platform layer (React Native Web, Tamagui, or a design token package). Sharing tokens and logic is cheap; sharing screens is expensive and often wrong.
- One version of `react` and `react-native` in the whole workspace; duplicates break at runtime (Expo monorepo guide). Check with `pnpm why react`.
- Rust equivalent: a `core` crate with no IO and no async runtime, used by the server binary, a CLI, and through FFI or WASM by clients.

## 11. Conway's law: boundaries follow teams

Conway (1968): organisations "are constrained to produce designs which are copies of the communication structures of these organizations". Practical consequences:

- A module boundary that cuts across one team's daily work will erode; a module owned by two teams will grow a negotiated, bloated interface.
- For a solo developer or a small team, this argues against microservices and many packages: boundaries cost coordination you do not need. Prefer a modular monolith with enforced internal boundaries.
- Organise teams and modules by feature or domain, not by layer (Fowler: "Developers don't have to be full-stack but teams should be").

## 12. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Each module has a secret | One sentence per module says what it hides | ARCHITECTURE.md codemap or module doc comments |
| No temporal decomposition | No format or protocol is known by more than one module | grep the format's key fields or column names; one module owns them |
| No pass-through layers | New functions and classes do more than forward | read: body is not a single delegating call |
| Direction enforced | Lint fails on feature to feature, shared to feature, domain to UI imports | `import/no-restricted-paths` zones or dependency-cruiser rules in CI |
| No cycles | Zero cycles | `npx madge --circular`; `cargo modules dependencies --lib --acyclic` |
| Minimal surface | No unused exports; Rust libs have no unreachable `pub` | `npx knip`; `#![warn(unreachable_pub)]` |
| Ports justified | Every interface has 2+ implementations or a named test double need | `rg -n "^export interface \w+(Port\|Repository\|Gateway\|Service)"` then count implementers |
| Shared core is platform free | Core package imports no platform modules | `rg -n "from '(react-native\|react-dom\|expo\|next)" packages/core` returns nothing |
| Errors minimised | Each module's error list is short and each error is one a caller can act on | read error enums and thrown types per module |
