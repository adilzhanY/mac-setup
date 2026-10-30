# Total TypeScript Essentials and Total TypeScript articles (Matt Pocock)

Legal free edition by the author: https://www.totaltypescript.com/books/total-typescript-essentials (the whole book is free online). Free articles: https://www.totaltypescript.com/articles. Print edition: No Starch Press, 2024.

## What I read

Book chapters "Annotations and Assertions", "The Weird Parts", "Unions, Literals and Narrowing". Articles: "The TSConfig Cheat Sheet", "Type vs Interface: Which Should You Use?", "Four Essential TypeScript Patterns" (branded types, globals, type predicates and assertion functions, assertion methods on classes). The "Why I don't like enums" URL returned 404.

## Key lessons used in languages/typescript/

- tsconfig base: `strict`, `noUncheckedIndexedAccess` ("should be part of strict"), `noImplicitOverride`, `verbatimModuleSyntax`, `isolatedModules`, `moduleDetection: force`, `skipLibCheck`; `module: preserve` + `noEmit` with a bundler, `NodeNext` when `tsc` emits; `declaration`, `composite`, `declarationMap` for libraries and monorepos. Pocock treats `noUnusedLocals`/`noUnusedParameters`/`noImplicitReturns` as optional noise. (types-and-strictness.md 1 and 2)
- Annotation vs `satisfies` vs `as`: annotation when the variable's type should win, `satisfies` to check without widening (`as const satisfies X`, `as const` first), `as` only when you know more than the checker; `{} as T` compiles with every property missing; double casts need `unknown`. (types-and-strictness.md 4 and 8)
- `@ts-expect-error` over `@ts-ignore`, because it fails once the error is gone. (types-and-strictness.md 15)
- Weird parts: excess property checks only on fresh literals; callback return values need an annotation to get them; `Object.keys` returns `string[]`; `{}` means non-nullish, not empty object; evolving `any` on unannotated `let`. (types-and-strictness.md 8 and 13)
- Narrowing: truthiness drops `""` and `0`; destructuring a discriminated union in the parameter list loses narrowing; discriminated unions over bags of optionals; `catch` values are `unknown`, narrow with `instanceof Error` and rethrow the rest. (types-and-strictness.md 5, 12; errors-and-async.md 3)
- `type` by default, `interface` for `extends` (cached by name, faster than intersections); interface declaration merging is a surprise source. (types-and-strictness.md 10)
- Branded types and assertion functions as the safe home for casts. (types-and-strictness.md 4 and 7)
