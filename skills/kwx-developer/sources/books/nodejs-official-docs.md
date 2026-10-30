# Node.js official documentation

Legal sources: https://nodejs.org/api/packages.html, https://nodejs.org/api/typescript.html, https://nodejs.org/api/cli.html (first half), https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop.

## What I read

"Modules: Packages" (module type determination, syntax detection, `exports`, conditional exports, subpath imports, `require(esm)`), "Modules: TypeScript" (type stripping), the first half of the CLI reference (`--env-file`, permission flags, `--frozen-intrinsics`), and the "Don't Block the Event Loop" guide.

## Key lessons used in languages/typescript/

- `.mjs`/`.cjs` fixed, `.js` follows `"type"`; ambiguous files pay a detection cost, so set `"type"`; ESM never guesses extensions or index files; `exports` encapsulates and wins over `main`; condition order matters, `types` first and `default` last; `#` imports, `#/` prefix since 24.14/25.4; `require(esm)` fails on top-level await. (modules-imports-exports.md 5, 9, 10)
- Type stripping: stable 24.12/25.2, on by default since 22.18; no type checking, ignores tsconfig, no enums/namespaces/parameter properties/decorators/`.tsx`, explicit `.ts` extensions, `import type` required; recommended tsconfig with `erasableSyntaxOnly` and `rewriteRelativeImportExtensions`. (node-runtime.md 1, types-and-strictness.md 2)
- Event loop: bound input sizes, JSON of 50 MB costs 0.7 s to stringify and 1.3 s to parse, ReDoS patterns, no sync APIs on servers, partition or offload, do not spawn a process per request. (node-runtime.md 5)
- `--env-file` stable in 24.10. (node-runtime.md 1)
