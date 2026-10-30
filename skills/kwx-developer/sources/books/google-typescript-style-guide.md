# Google TypeScript Style Guide

Legal source: https://google.github.io/styleguide/tsguide.html (public, Google). Read the first 100k characters of the page (everything up to the type system sections); the remaining part (about 25k characters covering `any`, `@ts-ignore` and some type guidance) was not read.

## What I read

Source file structure, imports and exports, module organisation, naming, classes, functions, control structures, exceptions, type assertions, enums, arrays, interfaces vs type aliases, null vs undefined.

## Key lessons used in languages/typescript/

- "Use named exports in all code"; default exports banned because they "provide no canonical name". Only export what is used outside the module; no `export let`; no container classes of statics; no `namespace`, no `require`. (modules-imports-exports.md 2 and 8)
- Type and non-null assertions are unsafe; prefer runtime checks; double assertions go through `unknown`; use annotations, not `as`, on object literals. (types-and-strictness.md 4)
- Throw only `new Error(...)` instances, never primitives; empty catch blocks need a comment. (errors-and-async.md 1 and 3)
- `===` always, except `== null`. `for...in` only on dict objects with own-property filtering. (javascript-without-types.md 4)
- `T[]`/`readonly T[]` for simple element types. Nullable aliases must not bake in `| null`. No general preference between null and undefined. (types-and-strictness.md 12)
- Must not use `const enum` (breaks isolated compilation). (types-and-strictness.md 9)
- Where this guide disagrees with Node/ESM practice: it uses snake_case file names and prefers relative imports for in-project files; kwx-developer defaults to kebab-case and one alias root across features, and says to follow the repo.
