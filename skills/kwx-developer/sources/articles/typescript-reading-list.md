# TypeScript and JavaScript reading list

Sources used for `languages/typescript/`. "Read" means fetched and read for this work on 2026-10-30; "secondary" means a news or blog report used only where the primary source was not found; "not read" means listed but not accessed.

## TypeScript (read)

- TSConfig reference, full page: https://www.typescriptlang.org/tsconfig/
- Modules guide, choosing compiler options: https://www.typescriptlang.org/docs/handbook/modules/guides/choosing-compiler-options.html
- JSDoc reference: https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html
- JS projects utilizing TypeScript: https://www.typescriptlang.org/docs/handbook/intro-to-js-ts.html
- TypeScript performance wiki: https://github.com/microsoft/TypeScript/wiki/Performance
- Announcing TypeScript 6.0: https://devblogs.microsoft.com/typescript/announcing-typescript-6-0/
- TypeScript 7.0 release (secondary, InfoQ): https://www.infoq.com/news/2026/08/typescript-7-released/
- Total TypeScript, TSConfig cheat sheet: https://www.totaltypescript.com/tsconfig-cheat-sheet
- Total TypeScript, type vs interface: https://www.totaltypescript.com/type-vs-interface-which-should-you-use
- Total TypeScript, four essential patterns: https://www.totaltypescript.com/four-essential-typescript-patterns
- Total TypeScript Essentials, annotations and assertions: https://www.totaltypescript.com/books/total-typescript-essentials/annotations-and-assertions
- Total TypeScript Essentials, the weird parts: https://www.totaltypescript.com/books/total-typescript-essentials/the-weird-parts
- Total TypeScript Essentials, unions, literals and narrowing: https://www.totaltypescript.com/books/total-typescript-essentials/unions-literals-and-narrowing
- Effective TypeScript blog index: https://effectivetypescript.com/
- Seven sources of unsoundness: https://effectivetypescript.com/2021/05/06/unsoundness/
- Push null values to the perimeter: https://effectivetypescript.com/2020/03/24/null-values-to-perimeter/
- Golden rule of generics: https://effectivetypescript.com/2020/08/12/generics-golden-rule/
- A small year for tsc (2025 review): https://effectivetypescript.com/2025/12/19/ts-2025/
- Google TypeScript style guide (first 100k characters): https://google.github.io/styleguide/tsguide.html

## Lint, format, tooling (read)

- typescript-eslint shared configs: https://typescript-eslint.io/users/configs/
- typescript-eslint `strict-type-checked` rule list (source): https://raw.githubusercontent.com/typescript-eslint/typescript-eslint/main/packages/eslint-plugin/src/configs/eslintrc/strict-type-checked.ts
- typescript-eslint typed linting: https://typescript-eslint.io/getting-started/typed-linting/
- typescript-eslint `consistent-type-imports`: https://typescript-eslint.io/rules/consistent-type-imports/
- ESLint `preserve-caught-error`: https://eslint.org/docs/latest/rules/preserve-caught-error
- ESLint v10 release (via search summary of the official post): https://eslint.org/blog/2026/02/eslint-v10.0.0-released/
- eslint-plugin-import-x `no-cycle`: https://github.com/un-ts/eslint-plugin-import-x/blob/master/docs/rules/no-cycle.md
- eslint-plugin-react-hooks README: https://raw.githubusercontent.com/facebook/react/main/packages/eslint-plugin-react-hooks/README.md
- Biome v2 announcement: https://biomejs.dev/blog/biome-v2/
- Oxlint type-aware linting: https://oxc.rs/docs/guide/usage/linter/type-aware.html
- Prettier options: https://prettier.io/docs/options
- knip home and issue types: https://knip.dev/ and https://knip.dev/reference/issue-types
- dependency-cruiser rules tutorial: https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-tutorial.md
- typescript-eslint and TS 7 status (secondary, search summary of GitHub threads and blogs)

## Modules and barrels (read)

- Vercel, how we optimized package imports in Next.js: https://vercel.com/blog/how-we-optimized-package-imports-in-next-js
- Marvin Hagemeister, speeding up the JavaScript ecosystem part 7 (barrel files): https://marvinh.dev/blog/speeding-up-javascript-ecosystem-part-7/
- Atlassian, faster builds when removing barrel files: https://www.atlassian.com/blog/atlassian-engineering/faster-builds-when-removing-barrel-files
- Default export debate (search results only: dev.to and Zenn opinion pieces; used only to confirm the arguments, not cited as authority)

## Node.js (read)

- Packages (ESM/CJS, exports, imports): https://nodejs.org/api/packages.html
- TypeScript type stripping: https://nodejs.org/api/typescript.html
- CLI options (first half): https://nodejs.org/api/cli.html
- Don't block the event loop: https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop
- Node.js best practices README (about two thirds): https://github.com/goldbergyoni/nodebestpractices
- Node 26 and Temporal (secondary): https://www.helpnetsecurity.com/2026/05/07/node-js-26-released/

## Errors, async, validation (read)

- MDN, using promises: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises
- MDN, AbortSignal: https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal
- Zod 4 release notes: https://zod.dev/v4
- Standard Schema: https://standardschema.dev/

## React, React Native, Next.js (read)

- You might not need an effect: https://react.dev/learn/you-might-not-need-an-effect
- Choosing the state structure: https://react.dev/learn/choosing-the-state-structure
- React Compiler introduction: https://react.dev/learn/react-compiler/introduction
- eslint-plugin-react-hooks reference: https://react.dev/reference/eslint-plugin-react-hooks
- React 19.2: https://react.dev/blog/2025/10/01/react-19-2
- React Native performance overview: https://reactnative.dev/docs/performance
- Optimizing FlatList configuration: https://reactnative.dev/docs/optimizing-flatlist-configuration
- React Native 0.82 and 0.84 posts (via search summaries): https://reactnative.dev/blog/2025/10/08/react-native-0.82 and https://reactnative.dev/blog/2026/02/11/react-native-0.84
- FlashList v2 changes: https://shopify.github.io/flash-list/docs/v2-changes
- Next.js server and client components: https://nextjs.org/docs/app/getting-started/server-and-client-components
- Next.js data security: https://nextjs.org/docs/app/guides/data-security
- Next.js proxy.js reference: https://nextjs.org/docs/app/api-reference/file-conventions/proxy
- Next.js caching (Cache Components): https://nextjs.org/docs/app/getting-started/caching

## Dates and money (read)

- MDN Temporal: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Temporal
- MDN Intl.NumberFormat constructor: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat
- Stripe supported currencies (minor units, zero-decimal and special cases): https://docs.stripe.com/currencies
- Temporal browser support (secondary, search summaries; MDN marks it limited availability)

## Not read

- Effective TypeScript, 2nd edition (book; only the author's free posts were read)
- Total TypeScript "Why I don't like enums" (URL returned 404)
- Google TypeScript style guide, last 25k characters
- Node.js CLI reference, second half (`--unhandled-rejections` text; the default `throw` comes from prior knowledge of Node 15+)
- arethetypeswrong and publint docs (tools recommended from the TypeScript handbook mention and common use)
- TanStack Query docs, Valibot docs, Biome rule reference for the installed version
