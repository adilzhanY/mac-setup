# Validation at boundaries

Read when: data enters the program from anywhere the type checker cannot see (HTTP, forms, URL, env, files, storage, queues, webhooks, third-party APIs, LLM output), or when you are about to write `as SomeType` on parsed data.

## Contents

1. What counts as a boundary
2. Parse, don't validate: the schema is the source of truth
3. Choosing a library
4. Patterns per boundary
5. Schema rules that prevent real bugs
6. Inside the boundary: trust the types
7. Checks

## 1. What counts as a boundary

TypeScript types are erased at runtime. A type annotation on external data is a promise nobody checks. Every one of these returns data that must be parsed before use:

| Source | Typical call |
|---|---|
| HTTP request body, query, params, headers, cookies | `req.body`, `await request.json()`, `searchParams.get()` |
| Next.js / React server functions (`"use server"`) and route params | the action's arguments, `await params`, `await searchParams` |
| Form submissions | `FormData` |
| Responses from your own or third-party APIs | `await res.json()` |
| Environment and config files | `process.env`, `import.meta.env`, YAML/JSON config |
| Browser storage, URL hash, `postMessage`, `BroadcastChannel` | `localStorage.getItem`, `event.data` |
| Message queues, webhooks, WebSocket frames | `JSON.parse(msg)` |
| Database JSON columns, files, CSV imports | `row.metadata`, `readFile` |
| LLM structured output | the model's JSON |
| `catch (err)` | `unknown` by design |

Rule: data from these sources is `unknown` until a schema has parsed it. `res.json()` returns `Promise<any>`; assign it to `unknown` immediately.

## 2. Parse, don't validate: the schema is the source of truth

Define the schema once; derive the static type from it. Never write an interface and a schema for the same shape: they drift.

```ts
import * as z from "zod";

export const CreateOrder = z.strictObject({
  customerId: z.uuid(),
  items: z.array(z.strictObject({
    sku: z.string().min(1).max(64),
    quantity: z.int().min(1).max(1_000),
  })).min(1).max(200),
  note: z.string().max(2_000).optional(),
});
export type CreateOrder = z.infer<typeof CreateOrder>;   // same name for schema and type is idiomatic
```

- A parse function returns a typed value or fails. After it, the rest of the code never re-checks.
- Use `safeParse` at boundaries where failure is expected (user input) and return a structured 400/422 with the issues. Use `parse` (throws) where failure means a bug or a broken upstream (your own config, internal service responses).
- When input and output differ (transforms, coercion, defaults), the type before parsing is `z.input<typeof S>` and after is `z.output<typeof S>` (`z.infer` is the output). Form libraries need the input type.
- Branded output for values that must be proven valid elsewhere: `z.email().brand<"Email">()` (see types-and-strictness.md section 7).

## 3. Choosing a library

| Situation | Choose |
|---|---|
| The repo already has a validator | that one. Two validation libraries in one app is an inconsistency to report |
| Default for apps and servers | Zod 4 (`zod`): stable, largest ecosystem; 6 to 15x faster parsing than Zod 3 and far fewer type instantiations |
| Client bundle size matters (mobile web, widgets) | Valibot, or `zod/mini` (about 1.9 kB gzipped core vs 5.4 kB for `zod`) |
| You need JSON Schema too (OpenAPI, LLM tool schemas) | Zod 4 `z.toJSONSchema()`, or TypeBox if the JSON Schema is primary |
| You write a library that accepts user schemas | accept any Standard Schema (`StandardSchemaV1` from `@standard-schema/spec`); Zod, Valibot and ArkType implement it, so users bring their own |

Do not hand-write validation (`typeof body.x === "string" && ...`) beyond two or three fields; it misses nested cases and produces no error report. Do not use `class-validator` decorators in new code (decorators conflict with `erasableSyntaxOnly` and Node type stripping).

## 4. Patterns per boundary

### HTTP handler

```ts
export async function POST(request: Request): Promise<Response> {
  const body: unknown = await request.json().catch(() => undefined);
  const parsed = CreateOrder.safeParse(body);
  if (!parsed.success) {
    return Response.json({ error: "invalid_body", issues: z.treeifyError(parsed.error) }, { status: 422 });
  }
  const order = await createOrder(parsed.data);   // parsed.data is CreateOrder
  return Response.json({ id: order.id }, { status: 201 });
}
```

- Limit body size before parsing (framework option or reverse proxy, Node best practices 6.14). `JSON.parse` of a 50 MB string blocks the Node event loop for about 1.3 s.
- Validate path params and query strings too; they are strings, so coerce explicitly: `z.coerce.number().int().positive()`.

### Server actions (Next.js, React)

Every `"use server"` function is a public POST endpoint, reachable without your UI. Inside each one: parse the arguments, authenticate, authorize the specific resource, then act. See nextjs.md.

### Environment variables

Parse once at startup, export the typed result, and read `process.env` nowhere else. A missing variable must stop the process at boot, not fail at 3 a.m. on the first request that needs it (Node best practices 1.4).

```ts
// src/config.ts
const Env = z.object({
  NODE_ENV: z.enum(["development", "test", "production"]),
  DATABASE_URL: z.url(),
  PORT: z.coerce.number().int().default(3000),
  STRIPE_SECRET_KEY: z.string().startsWith("sk_"),
  FEATURE_X: z.stringbool().default(false),   // accepts "true"/"false"/"1"/"0"/"yes"/"no"
});
export const env = Env.parse(process.env);
```

Never `Boolean(process.env.X)` or `process.env.X === "true"` scattered around: `"false"` is truthy.

### Third-party API responses

Parse responses from services you do not control, at least the fields you use. Prefer `z.object` (strips unknown keys, tolerates additions) over `z.strictObject` here, so the provider adding a field does not break you. A schema failure should raise a clear upstream error with the URL and the issue path, not crash deep inside business logic.

### Forms

- Same schema on client (instant feedback) and server (authority). The client copy is UX; the server copy is security.
- `FormData` values are `string | File`. Use `z.coerce.*` or `z.stringbool()` deliberately; `z.coerce.number()` turns `""` into `0`, so add `.min()` or preprocess empty strings to `undefined`.

### Storage, URL state, messages

`localStorage` content can be from an older app version or edited by the user. Parse it, and on failure fall back to defaults and overwrite. Version persisted shapes (`{ v: 2, ... }`).

### Webhooks

Verify the signature over the raw body first (constant-time compare via the provider SDK), then parse. Never parse, then verify.

### LLM output

Treat it like any external input: parse with the same schema you gave the model, retry or fail on mismatch, and never `eval` or execute it.

## 5. Schema rules that prevent real bugs

- **Bound every size.** Strings get `.max()`, arrays `.max()`, numbers `.min()`/`.max()`. Unbounded input is a denial-of-service and storage-cost bug.
- **Unknown keys.** Zod `z.object` strips unknown keys (safe against mass assignment as long as you use the parsed output, not the raw body). Use `z.strictObject` for your own API inputs so client typos (`quantty`) fail loudly instead of being silently dropped. Use `z.looseObject` only when passing data through untouched.
- **Never spread raw input into a DB write.** `db.user.update({ data: req.body })` lets the client set `role: "admin"`. Spread only `parsed.data`, and only from a schema that lists the writable fields.
- **Integers are integers.** Money, counts and IDs use `z.int()` (or `z.int32()`), not `z.number()`, which accepts `1.5`, and never accept money as a float from the wire (see dates-and-money.md).
- **Dates.** Accept ISO 8601 strings (`z.iso.datetime({ offset: true })`, `z.iso.date()`), then convert. Do not accept arbitrary strings into `new Date()`.
- **Enums.** Closed sets are `z.enum([...])` from the same `as const` array that defines the TypeScript union.
- **Error messages.** Customize with the `error` parameter (Zod 4) only where users see them; keep machine-readable issue paths for APIs. `z.prettifyError()` for logs and CLIs.
- **Do not trust a client-supplied ID for ownership.** Validation checks shape; authorization checks that this user may touch this resource. Both are required.

## 6. Inside the boundary: trust the types

- Once parsed, do not re-validate the same data in every function. Defensive `if (typeof x !== "string")` deep inside typed code is noise that hides the real boundary.
- Internal function arguments are typed, not parsed. Use assertions (`assert(x > 0)` or a throwing check) for invariants a bug could break, not schemas.
- Keep schemas next to the boundary that uses them (`routes/orders.schema.ts`, `config.ts`), or in a shared package when client and server both need them. Do not build a global `schemas/` dump.

## 7. Checks

- **No unparsed JSON.** Pass: every `res.json()`, `request.json()`, `JSON.parse(` result flows into a schema parse or a typed guard before property access. Verify: `rg -n '\.json\(\)|JSON\.parse\(' -t ts -t js .` and read each hit for a `.parse(`/`.safeParse(` within a few lines; lint `@typescript-eslint/no-unsafe-member-access` and `no-unsafe-assignment` flag the `any` flowing on.
- **No casts on parsed data.** Pass: zero `as` right after `json()`/`JSON.parse`. Verify: `rg -nP '(\.json\(\)|JSON\.parse\([^)]*\))\)?\s*as\s' -t ts .`
- **Env read in one place.** Pass: `process.env` appears only in the config module (and framework config files). Verify: `rg -n 'process\.env\.' -t ts -t js -g '!**/*.config.*' . | rg -v 'src/config'` (adjust the path); `n/no-process-env` lint rule.
- **No boolean env sniffing.** Pass: zero. Verify: `rg -n "process\.env\.\w+ === ['\"]true['\"]|Boolean\(process\.env" -t ts -t js .`
- **Bounded schemas.** Pass: every `z.string()` and `z.array(` in input schemas has a `.max(` (or is an enum/format with inherent bounds). Verify: `rg -n 'z\.string\(\)(?!.*\.max\()|z\.array\((?!.*\.max\()' -P -t ts .` and review the hits in boundary schemas.
- **No raw body writes.** Pass: no `req.body`/`await request.json()` passed directly into an ORM call. Verify: `rg -n '(data|values|set):\s*(req\.body|body)\b' -t ts .`
- **One validation library.** Pass: at most one of zod, valibot, yup, joi, superstruct, io-ts, arktype, ajv (ajv may coexist for JSON Schema). Verify: `rg -o '"(zod|valibot|yup|joi|superstruct|io-ts|arktype|class-validator)"' -g 'package.json' -g '!**/node_modules/**' . | sort | uniq -c`
- **Server actions validate.** Pass: every exported function in a `"use server"` file calls a schema parse and an auth check before its first DB call. Verify: `rg -l "^['\"]use server['\"]" -t ts .` then read each export.
- **Interface and schema not duplicated.** Pass: no `interface X` next to `const X = z.object`. Verify: `rg -n 'z\.infer<' -t ts . | wc -l` vs manual types with the same names; review.
