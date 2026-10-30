# Types and strictness

Read when: writing or reviewing any TypeScript, choosing a tsconfig, or when tempted to write `any`, `as`, `!`, `enum`, or a `@ts-` comment.

## Contents

1. The compiler settings (what to turn on, and why)
2. Recommended tsconfig per project kind
3. `any` vs `unknown`
4. Assertions: the ladder of alternatives to `as`
5. Model data so wrong states cannot be written
6. Exhaustiveness
7. Branded types for IDs and validated values
8. `satisfies`, annotations and inference
9. Enums, namespaces and other non-erasable syntax
10. `type` vs `interface`
11. Generics: the golden rule
12. Null, undefined and optional properties
13. Indexing, `Object.keys`, and other holes in soundness
14. Readonly inputs
15. Suppression comments
16. Compiler performance in big repos
17. Checks

## 1. The compiler settings

TypeScript 6.0 (March 2026) turned `strict` on by default and made `types` default to `[]`. TypeScript 7.0 (the Go compiler, stable August 2026) makes the 6.0 deprecations hard errors. Do not rely on defaults anyway: write the flags out so the file states intent and survives a version bump.

| Flag | In `strict`? | Turn on? | Why |
|---|---|---|---|
| `strict` | umbrella | always | Enables the whole strict family: `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitThis`, `useUnknownInCatchVariables`, `alwaysStrict`, `strictBuiltinIteratorReturn`. Never turn a member off to "get it compiling". |
| `noUncheckedIndexedAccess` | no | always for new code | `arr[i]` and `record[key]` become `T \| undefined`. Out-of-range reads are one of the seven documented sources of unsoundness (Vanderkam). Matt Pocock: "should be part of strict". |
| `exactOptionalPropertyTypes` | no | new code yes, retrofit only if cheap | `{ a?: string }` no longer accepts `{ a: undefined }`. Catches "present but undefined" bugs with spread and `Object.keys`. Noisy against some libraries' types. |
| `noImplicitOverride` | no | yes | A subclass method that silently stops overriding (base renamed) becomes a compile error. |
| `noFallthroughCasesInSwitch` | no | yes | Cheap, catches a real bug class. |
| `noImplicitReturns` | no | optional | Mostly covered by return type annotations and lint. |
| `noUnusedLocals`, `noUnusedParameters` | no | no, use the linter | They block compiling half-finished code. `@typescript-eslint/no-unused-vars` reports the same as a lint error. |
| `noPropertyAccessFromIndexSignature` | no | optional | Forces `obj["key"]` for index-signature reads so dynamic keys look dynamic. |
| `verbatimModuleSyntax` | no | always | Imports without `type` stay, imports with `type` vanish. Makes emit predictable for every transpiler, and errors when ESM syntax would be rewritten to `require`. Implies `isolatedModules`. |
| `isolatedModules` | no | yes (implied by the above) | Each file must be transpilable alone (esbuild, swc, Babel, Node type stripping). |
| `erasableSyntaxOnly` | no | yes for new code (TS 5.8+) | Errors on `enum`, runtime `namespace`, parameter properties, `import =`. Exactly the syntax Node's type stripping cannot run. |
| `moduleDetection: "force"` | no | yes | Every file is a module, so no accidental global scripts and no "cannot redeclare block-scoped variable". |
| `skipLibCheck` | no | yes | Skips checking `.d.ts` in `node_modules`. Large speed win. Cost: conflicting library types go unreported. |
| `isolatedDeclarations` | no | libraries and big monorepos | Exported API needs explicit types so `.d.ts` can be emitted per file in parallel. |
| `noUncheckedSideEffectImports` | no | yes (default in 6.0) | `import "./styles.css"` that resolves to nothing is an error, not silence. |
| `types` | n/a | list explicitly | `"types": ["node"]` or `[]`. Stops every `@types/*` package leaking globals; Microsoft reports 20 to 50 % faster builds from this alone. |

Deprecated in 6.0, removed in 7.0, so delete them when you see them: `baseUrl` (prefix `paths` entries instead), `moduleResolution: "node"`/`"node10"`/`"classic"`, `target: "es5"`, `downlevelIteration`, `outFile`, `module: "amd"|"umd"|"system"|"none"`, `esModuleInterop: false`, `allowSyntheticDefaultImports: false`, `alwaysStrict: false`, `import ... assert {}` (use `with {}`). `ignoreDeprecations: "6.0"` is a bridge only, it does nothing on 7.0.

## 2. Recommended tsconfig per project kind

Base, shared by all kinds:

```jsonc
{
  "compilerOptions": {
    "target": "es2022",              // or newer; match your lowest runtime
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "verbatimModuleSyntax": true,
    "erasableSyntaxOnly": true,
    "moduleDetection": "force",
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "types": []                      // add "node", "vitest/globals" etc. explicitly
  }
}
```

Then exactly one of these blocks:

| Project | Add | Notes |
|---|---|---|
| App built by a bundler (Vite, Next.js, Expo/Metro, esbuild) | `"module": "preserve"`, `"noEmit": true`, `"lib": ["es2022","dom","dom.iterable"]` for browsers | `preserve` implies `moduleResolution: "bundler"`: no file extensions needed. Type checking is `tsc --noEmit`; the bundler emits. |
| Node app compiled by `tsc` | `"module": "nodenext"`, `"outDir": "dist"`, `"rootDir": "src"`, `"types": ["node"]` | `nodenext` implies `moduleResolution: "nodenext"`, `esModuleInterop`. Relative imports need `.js` extensions. |
| Node app run directly with type stripping (Node 22.18+, stable in 24.12+) | `"module": "nodenext"`, `"noEmit": true`, `"rewriteRelativeImportExtensions": true`, `"allowImportingTsExtensions": true` | Write `import { x } from "./x.ts"`. Node ignores tsconfig entirely, so `paths` do nothing at runtime: use package.json `"imports"` (`#/*`). |
| Published library | `"module": "nodenext"` (or `"node18"`), `"declaration": true`, `"declarationMap": true`, `"sourceMap": true`, `"rootDir": "src"`, `"outDir": "dist"`, `"isolatedDeclarations": true` | Never `moduleResolution: "bundler"` for a library you emit with `tsc`: it lets you publish `export * from "./utils"` which breaks in Node with `ERR_MODULE_NOT_FOUND` (TS handbook, "Choosing compiler options"). |
| Monorepo package | library block plus `"composite": true` | Use project references. The TS performance wiki suggests 5 to 20 projects, evenly sized. |

## 3. `any` vs `unknown`

Rule: `any` does not appear in hand-written code. Data whose type you do not know is `unknown` and gets narrowed or parsed.

```ts
// Bad: any spreads. Everything touched by `data` is now unchecked.
const data: any = await res.json();
sendEmail(data.user.email);

// Good: unknown, then parse at the boundary (see validation-at-boundaries.md).
const data: unknown = await res.json();
const { user } = OrderSchema.parse(data);
sendEmail(user.email);
```

- `JSON.parse`, `res.json()`, `localStorage.getItem` results, `postMessage` data, `catch (e)` and third-party callbacks all return or receive unknown data. Treat them as `unknown` even when the declared type says `any`.
- A function that does not care about a value's type takes `unknown`, not a generic and not `any`: `function log(value: unknown)`.
- The only acceptable `any`: inside a generic constraint where TypeScript requires it (`(...args: any[]) => unknown` for "any function"), and one-off interop shims with a comment. `no-explicit-any` with an inline disable and a reason.
- `any` is contagious through return types. `no-unsafe-assignment`, `no-unsafe-member-access`, `no-unsafe-call`, `no-unsafe-return`, `no-unsafe-argument` (typescript-eslint, in `recommended-type-checked`) catch the spread from library `any`s too.

## 4. Assertions: the ladder of alternatives to `as`

`as` changes what the checker believes and nothing at runtime. `{} as User` compiles with every property missing. Never use `as` to make an error go away. Before writing `as`, walk down this ladder and stop at the first step that works:

1. Fix the type at its source (wrong annotation, missing generic argument, wrong library version).
2. Narrow with a runtime check: `typeof`, `instanceof`, `in`, `Array.isArray`, a discriminant comparison.
3. Parse with a schema at the boundary (`Schema.parse(x)` returns the right type).
4. Write a type guard (`x is T`) or assertion function (`asserts x is T`) whose body really checks. The guard is the one place where a cast is acceptable, because the check sits next to it.
5. Annotate (`const user: User = {...}`) or use `satisfies`, which check instead of override.
6. Last resort: `as` with a one-line comment stating why it is true. Double casts go through `unknown`, never `any`: `x as unknown as T` (Google TS style guide).

Allowed without ceremony: `as const`; `as` on a value just validated by code in the same function; test fixtures built with `satisfies Partial<T>` then completed.

Non-null assertion `!` follows the same rule. `user.profile!.bio` throws at runtime when the profile is missing. Replace with a check that throws a named error, or with `?.` plus a fallback that the caller can handle:

```ts
// Bad
const el = document.getElementById("app")!;

// Good: the failure says what broke
const el = document.getElementById("app");
if (!el) throw new Error("Missing #app root element");
```

## 5. Model data so wrong states cannot be written

- Use a discriminated union instead of a bag of optional fields. `{ status: "loading" | "error" | "success"; data?: T; error?: string }` allows `loading` with `data`. Write:

```ts
type Fetch<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "error"; error: Error }
  | { status: "success"; data: T };
```

- Replace two booleans that cannot both be true (`isSending`, `isSent`) with one string union (React docs, "Choosing the state structure").
- Push nulls to the perimeter (Effective TypeScript item 31): values that are null together live in one nullable object. Prefer `range: [min: number, max: number] | null` over `min: number | undefined; max: number | undefined`.
- Do not destructure the discriminant away from the rest in a parameter list (`({ kind, ...rest }: Shape)`): narrowing on `kind` will not narrow `rest`. Narrow on `shape.kind`, then destructure inside the branch.
- Literal unions over `string` for closed sets: `type Role = "admin" | "member"`. Derive them from a const array when you also need the runtime list:

```ts
export const ROLES = ["admin", "member", "guest"] as const;
export type Role = (typeof ROLES)[number];
```

## 6. Exhaustiveness

Every `switch` or `if` chain over a union handles every member, and adding a member must break the build.

```ts
function label(s: Fetch<unknown>): string {
  switch (s.status) {
    case "idle": return "Idle";
    case "loading": return "Loading";
    case "error": return s.error.message;
    case "success": return "Done";
    default: {
      const unreachable: never = s; // compile error when a new status appears
      throw new Error(`Unhandled status: ${JSON.stringify(unreachable)}`);
    }
  }
}
```

Enforce with `@typescript-eslint/switch-exhaustiveness-check` (not in any preset: add it by hand). For maps, `satisfies Record<Role, string>` makes a missing key a compile error.

## 7. Branded types for IDs and validated values

Two `string` IDs are interchangeable to the checker, so `transfer(toId, fromId)` with swapped arguments compiles. Brand values whose meaning matters:

```ts
declare const brand: unique symbol;
type Brand<T, B extends string> = T & { readonly [brand]: B };

type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;
type Cents = Brand<number, "Cents">;
type Email = Brand<string, "Email">;

// The only way in is a parser, so a branded value is proof of validation.
const UserIdSchema = z.uuid().brand<"UserId">();
```

- Create branded values in exactly one place per brand (the schema or a `parseX()` function). A grep for `as UserId` must return only that function.
- Brand at boundaries where mix-ups cost money or data: IDs of different tables, money units, sanitized HTML, absolute vs relative paths, validated email.
- Do not brand everything. A brand used in one file adds noise for nothing.

## 8. `satisfies`, annotations and inference

| Want | Write |
|---|---|
| Check a value against a type and keep the narrow inferred type (config objects, lookup tables) | `const routes = {...} as const satisfies Record<string, Route>` (`as const` comes first) |
| The variable's type is the declared type, period | annotation: `const user: User = {...}` |
| Local variable with an obvious type | no annotation (Effective TypeScript item 19: avoid cluttering code with inferable types) |
| Exported function | annotate the return type. Stops accidental API changes, speeds the checker (performance wiki), and is required by `isolatedDeclarations` |
| Object literal assigned to a type | annotation or `satisfies`, never `as` (Google TS style guide) |

Excess property checks only fire on fresh object literals. A callback's returned object is not checked for extra keys unless the callback has a return annotation: write `(row): Album => ({...})`.

## 9. Enums, namespaces and other non-erasable syntax

Default: no `enum`, no `const enum`, no runtime `namespace`, no parameter properties, no `import x = require()`. `erasableSyntaxOnly` enforces it.

Why: they are the only TypeScript features with runtime behaviour, so Node type stripping rejects them (`ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX`), `isolatedModules` breaks `const enum` across files, numeric enums accept any number, and string enums reject the literal string they contain.

```ts
// Instead of: enum Status { Active = "active", Archived = "archived" }
export const Status = { Active: "active", Archived: "archived" } as const;
export type Status = (typeof Status)[keyof typeof Status]; // "active" | "archived"
```

In an existing codebase that already uses enums consistently, do not convert piecemeal; flag it as a follow-up.

## 10. `type` vs `interface`

Pick one default per repo and follow it; consistency beats either choice. When no convention exists:

- `type` for unions, mapped, conditional, function and tuple types (only `type` can express them).
- `interface` for object shapes that other shapes `extends`: interface inheritance is cached by name and reports conflicts, while `A & B` intersections are recomputed and can silently produce `never` (TS performance wiki).
- Beware: two `interface X` declarations in scope merge silently. Two `type X` declarations are an error.
- Enforce the repo's choice with `@typescript-eslint/consistent-type-definitions` (in `stylistic`).

## 11. Generics: the golden rule

A type parameter must appear at least twice in the signature (Vanderkam, "The Golden Rule of Generics"). One appearance relates nothing.

```ts
// Bad: T appears once. Callers can claim any return type with zero checking.
function parseYaml<T>(input: string): T;
// Good: return unknown and make the caller parse it.
function parseYaml(input: string): unknown;

// Bad: K used once
function getLength<T extends { length: number }>(x: T): number;
// Good
function getLength(x: { length: number }): number;
```

`@typescript-eslint/no-unnecessary-type-parameters` (in `strict-type-checked`) flags these.

## 12. Null, undefined and optional properties

- Pick one "absent" value per layer. Default: `undefined` in TypeScript code (it is what optional properties, `?.`, missing keys and default parameters produce); `null` only where an external format requires it (JSON APIs, SQL NULL). Convert at the boundary. Google's guide states no global preference, so follow the repo.
- `field?: T` means "may be missing". `field: T | undefined` means "always present, may be undefined" (for example a required function parameter). With `exactOptionalPropertyTypes` these are different types; choose deliberately.
- Never test presence with truthiness when `0`, `""` or `false` are valid: `if (count)` drops zero. Use `count !== undefined` or `count != null` (the one accepted use of `!=`).
- Default values with `??`, not `||`. `||` replaces `0`, `""` and `false`.

## 13. Indexing, `Object.keys`, and other holes in soundness

Vanderkam's seven sources of unsoundness, with the fix to apply:

| Hole | Fix |
|---|---|
| `any` | `unknown` plus parsing |
| type assertions | the ladder in section 4 |
| array and record lookups | `noUncheckedIndexedAccess`; or pass the item itself rather than an index or ID |
| wrong `.d.ts` | fix upstream (DefinitelyTyped); augment locally with declaration merging; assert as last resort |
| array variance (`Cat[]` passed as `Animal[]`, then pushed a `Dog`) | take `readonly Animal[]` parameters |
| a function call does not undo narrowing | destructure the narrowed field to a `const` before calling out; pass `Readonly<T>` to callbacks |

`Object.keys(obj)` returns `string[]` by design (objects are open). Iterate with `Object.entries` and type the entry, or keep a typed key list (`ROLES` above). Do not write `Object.keys(obj) as (keyof T)[]` on a value that may hold extra keys.

## 14. Readonly inputs

- Function parameters that are arrays or objects you do not mutate are typed `readonly T[]` / `Readonly<T>` / `ReadonlyMap`. This documents the contract and closes the variance hole.
- Do not mutate arguments. Return a new value: `toSorted()`, `toReversed()`, `toSpliced()`, `with()`, spread, `structuredClone` for deep copies.
- `Readonly<T>` is shallow. Do not claim deep immutability unless a type such as a recursive `DeepReadonly` or runtime `Object.freeze` backs it.

## 15. Suppression comments

- `@ts-ignore`: never. It keeps suppressing after the error is gone and hides unrelated errors on the same line.
- `@ts-expect-error: <reason, at least 10 characters>` when a suppression is unavoidable (tests that pass bad input on purpose, known upstream type bugs with an issue link). It fails once the error disappears, so it cleans itself up. `ban-ts-comment` with `minimumDescriptionLength: 10` is the `strict` preset setting.
- `@ts-nocheck` only on generated or vendored files, never on files you edit.
- `eslint-disable` comments name the rule and give a reason: `// eslint-disable-next-line @typescript-eslint/no-explicit-any -- untyped plugin API`. Enforce with `eslint-comments/require-description` or ESLint's `reportUnusedDisableDirectives` (on by default since ESLint 9).

## 16. Compiler performance in big repos

From the TypeScript team's performance wiki:

- Unions with more than about a dozen members get expensive (assignability against each member, quadratic de-duplication). Prefer a base type with subtypes.
- Name complex conditional types with a type alias so they are cached.
- `extends` on interfaces instead of chained intersections.
- Restrict `include` to source folders. Once you set `exclude`, re-add `**/node_modules` and `**/.*/` yourself.
- Diagnose with `tsc --extendedDiagnostics` (high Program or I/O time means `include` is too broad), `--explainFiles` (why is this file included), `--traceResolution`, `--generateTrace <dir>` then `npx @typescript/analyze-trace <dir>`.
- On TypeScript 7 (`tsc` from the Go port), full builds are reported 8 to 12x faster; `--checkers`/`--builders` tune parallelism. Tools that need the compiler API (typescript-eslint typed rules, Vue/Svelte/Astro tooling, webpack loaders) wait for 7.1; `@typescript/typescript6` provides `tsc6` side by side during migration.

## 17. Checks

Run every command from the repo root. Always pass an explicit path (`.`) to `rg`: without one, ripgrep reads stdin when stdin is not a terminal and hangs in agent shells.

- **Strict on.** Pass: `strict: true` (or TS 6+ with no `strict: false`) and `noUncheckedIndexedAccess: true`. Verify: `npx tsc --showConfig | rg -n 'strict|noUnchecked|exactOptional|verbatim|erasable'`
- **No deprecated options.** Pass: none of `baseUrl`, `moduleResolution: node`, `target: es5`, `downlevelIteration`, `outFile`, `ignoreDeprecations`. Verify: `rg -n '"(baseUrl|downlevelIteration|outFile|ignoreDeprecations)"|"moduleResolution":\s*"node(10)?"|"target":\s*"es5"' -g 'tsconfig*.json' .`
- **Typecheck clean.** Pass: exit code 0. Verify: `npx tsc --noEmit -p .` (or `npx tsc -b` with project references).
- **No `any` in source.** Pass: zero hits outside `.d.ts` and generated code, or each hit carries a disable comment with a reason. Verify: `rg -nP -t ts ':\s*any\b|<any>|\bas any\b' -g '!*.d.ts' .` and lint rule `@typescript-eslint/no-explicit-any`.
- **`as` is rare and justified.** Pass: each non-`const` assertion sits inside a guard or parser, or carries a comment. Verify: `rg -nP -t ts '\bas (?!const\b)[A-Za-z_{\[(]' -g '!*.d.ts' . | rg -v ':\s*(import|export) '` then read each hit; lint `no-unnecessary-type-assertion`.
- **No non-null assertions.** Pass: zero, or each justified. Verify: lint `@typescript-eslint/no-non-null-assertion` (authoritative); quick grep `rg -nP -t ts '\w!(\.|\[|\)|\s*[-+*/,;])' .` misses some forms.
- **No `@ts-ignore`.** Pass: zero hits. Verify: `rg -n '@ts-ignore' -t ts -t js .`
- **`@ts-expect-error` has a reason.** Pass: no bare directive. Verify: `rg -n '@ts-expect-error\s*$' -t ts .` returns nothing.
- **No enums or runtime namespaces in new code.** Pass: zero, unless the repo already standardised on them. Verify: `rg -nP -t ts '^\s*(export\s+)?(declare\s+)?(const\s+)?enum\s+\w+\s*\{|^\s*(export\s+)?namespace\s+[\w.]+\s*\{' .` and `erasableSyntaxOnly: true`.
- **Exhaustive switches.** Pass: rule enabled and lint passes. Verify: `rg -n 'switch-exhaustiveness-check' -g 'eslint.config.*' .`
- **Exported functions have return types.** Pass: lint passes. Verify: `@typescript-eslint/explicit-module-boundary-types` enabled, or `isolatedDeclarations: true` and `tsc` passes.
- **Generic parameters used twice.** Pass: lint passes. Verify: `@typescript-eslint/no-unnecessary-type-parameters` (in `strict-type-checked`).
- **Branded values have one constructor.** Pass: each `as <BrandName>` occurs only in its parser. Verify: `rg -n 'as (UserId|OrderId|Cents)\b' -t ts .` (substitute the repo's brand names).
