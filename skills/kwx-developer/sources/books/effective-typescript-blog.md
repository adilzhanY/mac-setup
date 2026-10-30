# Effective TypeScript blog (Dan Vanderkam)

Legal source: the author's blog https://effectivetypescript.com/ (posts by the author, several are excerpts of book items). The book itself (Effective TypeScript, 2nd edition, O'Reilly 2024) was not read; only the free posts.

## What I read

"The Seven Sources of Unsoundness in TypeScript" (2021), "Item 31: Push Null Values to the Perimeter of Your Types" (2020), "The Golden Rule of Generics" (2020), "A Small Year for tsc, a Giant Year for TypeScript" (2025 review), plus the full post index to find relevant items (knip recommendation, Item 19 inferable types, Item 30 JSDoc repetition).

## Key lessons used in languages/typescript/

- Seven sources of unsoundness and their fixes: `any` (use `unknown`), assertions (narrow or validate with Zod), array/object lookups (`noUncheckedIndexedAccess`), wrong `.d.ts` (fix upstream, augment), array variance (`readonly` parameters), function calls not invalidating refinements (destructure to a const, `Readonly` callbacks). (types-and-strictness.md 13 and 14)
- Push nulls to the perimeter: values that are null together belong in one nullable object; avoid falsy checks that drop 0. (types-and-strictness.md 5 and 12)
- Golden rule of generics: a type parameter must appear at least twice; `parseYAML<T>(): T` is a disguised cast, return `unknown`. (types-and-strictness.md 11)
- 2025 review: Node 22.18+ runs TS by type stripping without checking; turn on `erasableSyntaxOnly`; keep `tsc` for checking; prefer standard ECMAScript features over TS-only ones (enums, parameter properties). (types-and-strictness.md 9, node-runtime.md 1)
- Do not repeat type information in JSDoc prose (Item 30). (javascript-without-types.md 3)
- Use knip for dead code and dead types. (tooling-and-lints.md, codebase-audit.md)
