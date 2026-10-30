# JavaScript without TypeScript syntax

Read when: the files you edit are `.js`, `.mjs`, `.cjs` or `.jsx` (a JS-only project, config files, scripts, a userscript, a browser extension, a Quickshell/QML-adjacent JS helper), or you must decide whether a new file should be JS or TS.

## Contents

1. Should this file be JavaScript at all?
2. Get type checking anyway: `// @ts-check` and `checkJs`
3. JSDoc types that TypeScript understands
4. Language rules for plain JS
5. Modules in plain JS
6. Linting plain JS
7. Checks

## 1. Should this file be JavaScript at all?

- In a TypeScript project, new source files are `.ts`/`.tsx`. Plain JS is acceptable only for tool config files, tiny scripts run without a build step on old Node, and generated code.
- With Node 22.18+ type stripping, even scripts can be `.ts` and run with `node script.ts`. Prefer that over untyped JS.
- In a JS-only repo, follow the repo: do not convert files to TS as a side effect of another change. Propose a migration separately (`allowJs` + `checkJs` first, then rename file by file).
- Libraries that ship JS with JSDoc types (no build step) are a legitimate style (Svelte's codebase is the well-known example). They still get full type checking through `checkJs` and emit `.d.ts` with `tsc`.

## 2. Get type checking anyway: `// @ts-check` and `checkJs`

Every JS file you write or substantially edit is type checked:

- Single file: first line `// @ts-check`. Editors (VS Code) then report type errors using JSDoc and inference.
- Whole project: a `jsconfig.json` or `tsconfig.json` with:

```jsonc
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": true,
    "noEmit": true,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "module": "nodenext",          // or "preserve" with a bundler
    "target": "es2022",
    "skipLibCheck": true,
    "types": ["node"]
  },
  "include": ["src", "scripts"]
}
```

- CI runs `npx tsc -p jsconfig.json` (or `tsconfig.json`) exactly as for TS.
- Opt a file out with `// @ts-nocheck` only for vendored or generated files.
- Library authors ship types from JS: `tsc --allowJs --declaration --emitDeclarationOnly --outDir types`, and point `"types"` in `package.json` `exports` at them.

## 3. JSDoc types that TypeScript understands

Write types in JSDoc; TypeScript reads these tags (handbook, "JSDoc Reference"):

```js
// @ts-check

/** @import { Order, LineItem } from "./types.js" */      // type-only import, no runtime cost (TS 5.5+)

/**
 * @typedef {object} Money
 * @property {bigint} amountMinor
 * @property {"USD" | "EUR" | "JPY"} currency
 */

/**
 * Sum line items in minor units.
 * @param {readonly LineItem[]} items
 * @param {{ currency: Money["currency"] }} options
 * @returns {Money}
 */
export function total(items, { currency }) {
  /** @type {bigint} */
  let sum = 0n;
  for (const item of items) sum += item.priceMinor * BigInt(item.quantity);
  return { amountMinor: sum, currency };
}

/**
 * @template T
 * @param {readonly T[]} xs
 * @returns {T | undefined}
 */
export const first = (xs) => xs[0];

/** @satisfies {Record<string, `/${string}`>} */
export const routes = { home: "/", settings: "/settings" };

const el = /** @type {HTMLInputElement} */ (document.querySelector("#q")); // cast: the parentheses are required
```

Rules:

- Every exported function has `@param` and `@returns` types. Local variables rely on inference, as in TS.
- Optional parameters: `@param {string} [name]`; with a default: `@param {number} [limit=20]`.
- Shared shapes go in `@typedef` (or a `.d.ts` file imported with `@import`), not repeated in every comment.
- Do not repeat types in prose ("@param {string} name - the name string"); the description says what the value means, not its type (Effective TypeScript item 30).
- A cast is the same as `as` in TS: same ladder of alternatives (types-and-strictness.md section 4). Prefer a runtime check.
- Unsupported tags are ignored silently (`@memberof`, `@yields`, `@async`). Do not rely on them for types.
- `@ts-expect-error` with a reason works in JS too; `@ts-ignore` is banned the same way.

## 4. Language rules for plain JS

Without a type checker watching, these are the bugs that slip through most:

- `const` by default, `let` when reassigned, never `var`.
- `===` and `!==` always; `== null` is the one accepted loose comparison (checks null and undefined).
- `??` for defaults, not `||` (which replaces `0`, `""`, `false`). `?.` for optional access, but not as a habit on values that must exist: a missing required value should throw, not silently become `undefined`.
- Numbers: `Number(x)` or `Number.parseInt(x, 10)` with an explicit radix, then `Number.isNaN` / `Number.isFinite` checks. Never global `isNaN` (coerces). `parseInt("08")` without radix is legacy-ambiguous; `parseInt("1e3")` is 1.
- Sorting: `arr.sort()` sorts as strings (`[10, 9, 1]` becomes `[1, 10, 9]`). Always pass a comparator, and prefer `toSorted()` to avoid mutating.
- Do not mutate inputs: `toSorted`, `toReversed`, `toSpliced`, `with`, spread, `structuredClone`.
- Iteration: `for...of` over arrays and iterables; `Object.entries` for objects; `for...in` only with `Object.hasOwn` checks (it walks the prototype chain).
- Use `Object.hasOwn(obj, key)`, not `obj.hasOwnProperty(key)` (breaks on `Object.create(null)`).
- Dictionaries keyed by user input: `Map`, or `Object.create(null)`; plain objects have `__proto__` and `constructor` keys.
- `typeof null === "object"`. Check `x !== null && typeof x === "object"`.
- `Array.isArray(x)` to detect arrays, not `typeof`.
- Strings with user content in HTML: never `innerHTML`; use `textContent` or DOM APIs (XSS).
- `JSON.parse` returns untrusted data: validate it (validation-at-boundaries.md works the same in JS).
- Throw `new Error(...)` with `cause` (errors-and-async.md); all the async rules apply unchanged, and without types the floating promise is even easier to miss, so lint matters more.
- Strict mode is automatic in ES modules and classes. In a CJS script, start with `"use strict";`.

## 5. Modules in plain JS

- ESM (`import`/`export`) with `"type": "module"`; `.cjs` only for tools that require CommonJS config.
- Relative imports include the extension (`./util.js`): Node ESM does not guess, and the browser needs the full URL.
- Named exports, same as TS (modules-imports-exports.md), except where a tool requires `export default` (most `*.config.js` files).
- Browser scripts without a bundler: `<script type="module">`, import maps for bare specifiers, no global variables shared between files.
- Userscripts and extensions: wrap in a module or IIFE, never leak globals into the page; feature-detect APIs.

## 6. Linting plain JS

- `@eslint/js` `recommended` at minimum. In a TS repo, JS files get `tseslint.configs.disableTypeChecked` (type-aware rules need TS program info that JS config files often lack).
- In a JS-only repo with `checkJs`, typed linting still works: point `parserOptions.projectService` at the jsconfig and use the type-checked configs; `no-floating-promises` works on JS.
- Add `eslint-plugin-n` for Node scripts (`n/no-missing-import`, `n/no-process-exit`) and `eslint-plugin-regexp`.
- Same formatter as the rest of the repo.

## 7. Checks

- **Type checked.** Pass: every JS source file is covered by `checkJs` or starts with `// @ts-check`. Verify: `rg --files-without-match '^// @ts-check' -g '*.{js,mjs,jsx}' -g '!**/{node_modules,dist,build}/**' src` lists unchecked files when no `checkJs: true` config exists; `rg -n '"checkJs":\s*true' -g '{js,ts}config*.json' .`
- **Typecheck passes.** Pass: exit 0. Verify: `npx tsc -p jsconfig.json --noEmit` (or the tsconfig).
- **Exported functions typed.** Pass: each `export function` is preceded by a JSDoc block with `@param`/`@returns`. Verify: `rg -nUP '(?<!\*/\n)^export (async )?function' -g '*.{js,mjs}' .` lists functions without a JSDoc block directly above.
- **No `var`.** Pass: zero. Verify: `rg -n '^\s*var ' -g '*.{js,mjs,cjs,jsx}' -g '!**/node_modules/**' .`; ESLint `no-var`.
- **No loose equality.** Pass: only `== null`/`!= null`. Verify: `rg -nP '[^=!]==[^=]|!=[^=]' -g '*.{js,mjs,jsx}' . | rg -v '[!=]= null'`; ESLint `eqeqeq` with `{ null: "ignore" }`.
- **No comparator-less sort.** Pass: zero. Verify: `rg -n '\.sort\(\)' -g '*.{js,mjs,ts,tsx}' .`
- **No parseInt without radix.** Pass: zero. Verify: `rg -nP 'parseInt\([^,()]*\)' -g '*.{js,mjs,ts}' .`; ESLint `radix`.
- **No innerHTML with dynamic content.** Pass: zero non-constant assignments. Verify: `rg -n 'innerHTML\s*=' -g '*.{js,mjs,jsx,ts,tsx}' .` and review.
- **ESM extensions.** Pass: relative imports end with `.js`/`.mjs` in non-bundled code. Verify: `rg -nP "from ['\"]\.\.?/[^'\"]*(?<!\.m?js)['\"]" -g '*.{js,mjs}' .`
