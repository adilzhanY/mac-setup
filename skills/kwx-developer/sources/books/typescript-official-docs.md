# TypeScript official documentation and team wiki

Legal sources: https://www.typescriptlang.org/tsconfig/ (TSConfig reference), https://www.typescriptlang.org/docs/handbook/modules/guides/choosing-compiler-options.html, https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html, https://www.typescriptlang.org/docs/handbook/intro-to-js-ts.html, https://github.com/microsoft/TypeScript/wiki/Performance, https://devblogs.microsoft.com/typescript/announcing-typescript-6-0/.

## What I read

The full TSConfig reference (both halves) for the strict family, the extra strictness flags, module and resolution options, `verbatimModuleSyntax`, `isolatedModules`, `isolatedDeclarations`, `erasableSyntaxOnly`, `moduleDetection`, `skipLibCheck`, `allowJs`/`checkJs`, `libReplacement`, `incremental`. The modules guide on choosing compiler options. The JSDoc reference. The performance wiki. The TypeScript 6.0 announcement. TypeScript 7.0 details came from InfoQ's release report (https://www.infoq.com/news/2026/08/typescript-7-released/), since the official 7.0 post was not found.

## Key lessons used in languages/typescript/

- The strict family members and the flags outside it, each with its reason. (types-and-strictness.md 1)
- TS 6.0 defaults (`strict` on, `types: []`, `module esnext`, `target es2025`, `noUncheckedSideEffectImports` on) and deprecations (`baseUrl`, `moduleResolution node`, `target es5`, `outFile`, AMD/UMD/System, `esModuleInterop false`); `types` alone gives 20 to 50 % faster builds; Temporal types; `#/` subpath imports. (types-and-strictness.md 1, typescript.md 4)
- Recommended settings per project kind; libraries must not use `moduleResolution: bundler` with `tsc` emit because it lets extensionless imports that fail in Node ship; strictest settings for libraries; arethetypeswrong before publishing. (types-and-strictness.md 2, modules-imports-exports.md 10)
- Performance: interfaces over intersections, return annotations, unions over a dozen members are costly, named complex types, project references (5 to 20 projects), tight `include`, explicit `types`, `--extendedDiagnostics`, `--explainFiles`, `--generateTrace`. (types-and-strictness.md 16)
- JSDoc tags TypeScript supports (`@import`, `@typedef`, `@template`, `@satisfies`, parenthesised casts) and the unsupported ones. (javascript-without-types.md 3)
- TS 7.0: 8 to 12x faster builds, no stable API until 7.1, so typescript-eslint stays on 6.0. (tooling-and-lints.md 2)
