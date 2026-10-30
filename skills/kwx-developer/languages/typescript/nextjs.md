# Next.js (App Router)

Read when: working in a Next.js App Router project (an `app/` directory next to `next.config.*`). Covers the server/client split, data access, server actions, caching and the security mistakes models make most. Check the installed version first (`rg '"next":' package.json`): this file reflects Next.js 16 (October 2026 docs). For Pages Router projects, only sections 1, 4 and 7 apply.

## Contents

1. Server Components by default, `"use client"` at the leaves
2. What may cross the server/client boundary
3. Keeping server code and secrets on the server
4. Data access: one approach, a Data Access Layer for new apps
5. Server actions are public endpoints
6. Route handlers, `proxy.ts`, and params
7. Caching (version dependent)
8. Performance defaults
9. Auditing a Next.js app
10. Checks

## 1. Server Components by default, `"use client"` at the leaves

- Pages and layouts are Server Components. They fetch data, read secrets, and send no JavaScript for themselves.
- A file needs `"use client"` only if it uses state, effects, event handlers, browser APIs, or hooks that use them. Everything that file imports, and every component it renders directly, joins the client bundle. So put `"use client"` on the smallest interactive leaf (`<SearchBox>`), not on a layout or page.
- Server Components can be passed into Client Components as `children` or other props. They render on the server and arrive as output; they are not imported into the client graph. Use this to keep a server-rendered `<Cart>` inside a client `<Modal>`.
- Context providers are client components that take `children`; render them as deep as possible (wrap `{children}`, not `<html>`).
- Third-party components that use hooks but lack `"use client"`: wrap them in a one-line client file (`"use client"; export { Carousel } from "acme-carousel";`).
- Library authors: put `"use client"` on client entry points and check the bundler keeps the directive.

## 2. What may cross the server/client boundary

- Props passed from a Server Component to a Client Component are serialized. Only serializable values: plain objects, arrays, primitives, `Date`, `Map`, `Set`, promises, server actions, JSX. Not class instances, plain functions, or symbols.
- Everything in those props is visible in the browser (in the RSC payload). Pass the fields the component renders, never a whole database row. A Client Component prop typed `user: User` (the full DB type) is a leak waiting to happen; type it `{ name: string; avatarUrl: string }`.
- Server action return values are serialized to the client too. Return `{ ok: true }` or the minimal view model, not the updated record.
- Optional hardening: React taint APIs (`experimental_taintObjectReference`, `experimental_taintUniqueValue`, `experimental.taint: true`) block marked objects from reaching the client. They are a second layer, not a replacement for DTOs.

## 3. Keeping server code and secrets on the server

- Add `import "server-only"` at the top of every module that touches the database, secrets, or internal APIs. Importing it from client code becomes a build error instead of a silent leak. `import "client-only"` marks the reverse.
- Only `NEXT_PUBLIC_*` variables reach the browser; everything else is replaced with an empty string in client code. Never prefix a secret with `NEXT_PUBLIC_`. Treat every `NEXT_PUBLIC_` value as published.
- Only the Data Access Layer reads `process.env` secrets (Next.js data security guide). Parse env once in a `server-only` config module (validation-at-boundaries.md).

## 4. Data access: one approach, a Data Access Layer for new apps

Next.js names three approaches and says to pick one per app and not mix them:

| Approach | When |
|---|---|
| External HTTP API (REST/GraphQL called with `fetch` from Server Components) | existing backend owned by another team; apply zero trust |
| Data Access Layer (DAL) | default for new apps |
| Component-level queries in Server Components | prototypes only; easy to leak whole rows to the client |

A DAL is a `server-only` module that: reads the session itself (with `React.cache` so it runs once per request), performs authorization, queries with parameterized APIs, and returns minimal DTOs.

```ts
// data/projects.ts
import "server-only";
import { cache } from "react";

export const getCurrentUser = cache(async () => {
  const session = await verifySession();          // reads cookies, throws if absent
  return { id: session.userId, role: session.role };
});

export async function getProjectCard(projectId: string) {
  const user = await getCurrentUser();
  const project = await db.project.findUnique({ where: { id: projectId } });
  if (!project || project.ownerId !== user.id) throw new NotFoundError("project", projectId);
  return { id: project.id, name: project.name, updatedAt: project.updatedAt.toISOString() };
}
```

Pages call `getProjectCard`, never the ORM directly. Database packages imported outside `data/` (or the agreed DAL folder) are a finding.

## 5. Server actions are public endpoints

Every exported function in a `"use server"` file, and every inline `"use server"` function, is reachable with a direct POST, whether or not your UI calls it. Action IDs are encrypted and unused actions are removed at build, but Next.js says to "treat Server Actions as reachable via direct POST requests and verify authentication and authorization inside each one."

Each action, in this order:

1. Parse the arguments with a schema (they are attacker-controlled, including hidden form fields and bound arguments).
2. Authenticate: read the session inside the action. A page-level `redirect("/login")` does not protect actions defined on that page.
3. Authorize the specific resource (ownership or role). Checking "logged in" without checking "may touch this record" is an IDOR bug.
4. Perform the mutation through the DAL.
5. Revalidate (`revalidatePath`/`revalidateTag`/`updateTag`) and return a minimal result.

```ts
"use server";
import * as z from "zod";
import { deleteProject } from "@/data/projects";   // DAL does authn + authz
import { revalidatePath } from "next/cache";

const Input = z.strictObject({ projectId: z.uuid() });

export async function deleteProjectAction(raw: unknown) {
  const { projectId } = Input.parse(raw);
  await deleteProject(projectId);
  revalidatePath("/projects");
  return { ok: true as const };
}
```

More rules:

- Never mutate during render (no logout on `?logout=1`, no DB writes in a page). Mutations go through actions or route handlers (POST).
- Closures captured by inline actions are encrypted and round-tripped through the client. Do not capture secrets anyway.
- Self-hosting on several instances: set `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` (32-byte base64) so all instances share the key.
- Behind proxies with a different public host, configure `serverActions.allowedOrigins`; Next.js rejects actions whose `Origin` does not match `Host`.
- Rate-limit actions that send email, SMS or expensive work.

## 6. Route handlers, `proxy.ts`, and params

- `route.ts` handlers export named methods (`GET`, `POST`). Validate body, query and params like any HTTP endpoint and return proper status codes.
- Next.js 16 renamed `middleware.ts` to `proxy.ts` (codemod: `npx @next/codemod@canary middleware-to-proxy .`); it runs on the Node.js runtime. Use it for redirects, rewrites, headers and optimistic auth redirects only. It is not an authorization layer: server functions are POSTs to the page route, so a matcher change or moved action silently removes coverage. Authorize in the DAL and in each action.
- Without a `matcher`, proxy runs on every request including static assets; always set one.
- In Next.js 15+, `params` and `searchParams` are Promises: `const { id } = await params`. Bracket folders (`[id]`) are user input: validate the value (`z.uuid().parse(id)`) before querying.
- Do not trust `searchParams` for authorization (`?isAdmin=true`). Re-verify from the session.

## 7. Caching (version dependent)

Next.js caching has changed in every major release. Before writing caching code, check `next.config.*` for `cacheComponents` and read the docs for the installed version. As of Next.js 16 with Cache Components (the `create-next-app` default):

- Nothing is cached unless you say so. `"use cache"` at the top of an async function or component caches its result; arguments and captured values form the cache key. Pair every `"use cache"` with `cacheLife(...)` and tag shared data with `cacheTag(...)`.
- Uncached async work and runtime APIs (`cookies()`, `headers()`, `searchParams`, dynamic `params`) must sit inside `<Suspense>`; the dev overlay flags blocking routes. Push `await` of runtime data down the tree so more of the page joins the static shell.
- `Math.random()`, `Date.now()`, `crypto.randomUUID()` in render need `await connection()` (per request) or `"use cache"` (shared).
- The default runtime cache is per instance and in memory (lost on serverless); `"use cache: remote"` for shared durable caching, `"use cache: private"` for per-user data in the browser cache.
- After a mutation, invalidate with `revalidateTag`/`updateTag`/`revalidatePath` in the action.
- Never cache per-user data in a shared cache entry. A cached function that reads the session and is keyed only by `projectId` serves one user's data to another.

Projects without `cacheComponents` use the previous model (fetch cache options, `export const revalidate`, `dynamic`); follow the "Caching and Revalidating (Previous Model)" guide instead. Do not mix the two models.

## 8. Performance defaults

- Use `next/image` (sizing, lazy loading, modern formats) and `next/font` (self-hosted, no layout shift). Give images explicit `width`/`height` or `fill` with a sized parent.
- `next/link` for internal navigation (prefetching).
- Large client-only widgets (charts, editors, maps) via `next/dynamic` or `React.lazy` inside client components.
- Barrel-heavy packages: add to `experimental.optimizePackageImports` if not already in the default list.
- Check the client bundle after adding a dependency to a client component (`next build` output, or `@next/bundle-analyzer`). A date library or icon pack pulled into the client is a common regression.
- Parallel data loading in Server Components: start independent fetches together (`Promise.all`) or in sibling components under separate `<Suspense>` boundaries; avoid await chains in one component.

## 9. Auditing a Next.js app

From the Next.js data security guide, look hardest at:

- The DAL: do database packages and `process.env` secrets appear outside it?
- `"use client"` files: do props accept private data or whole DB types?
- `"use server"` files: are arguments validated, the user re-authenticated and authorized for the resource, return values minimal, DB access delegated to `server-only` code?
- `[param]` folders: are params validated?
- `proxy.ts` and `route.ts`: audit with normal API security techniques.

## 10. Checks

- **Client boundary is small.** Pass: no `"use client"` in `layout.tsx` or `page.tsx` unless the whole route is interactive. Verify: `rg -l "^['\"]use client['\"]" -g '**/{layout,page}.{tsx,jsx}' app src/app 2>/dev/null`
- **Server-only modules marked.** Pass: every module importing the DB client or reading secrets imports `server-only`. Verify: `rg -l "from ['\"](@prisma/client|drizzle-orm|pg|mysql2|mongodb|@/lib/db|#/db)" -t ts . | xargs rg --files-without-match "import ['\"]server-only['\"]"` lists offenders.
- **DB not imported from components.** Pass: DB imports only under the DAL folder. Verify: `rg -l "from ['\"](@prisma/client|drizzle-orm|@/lib/db|#/db)" -t ts app components 2>/dev/null`
- **No secrets in public env.** Pass: no `NEXT_PUBLIC_` name containing SECRET, KEY (except publishable keys), TOKEN, PASSWORD. Verify: `rg -n 'NEXT_PUBLIC_\w*(SECRET|TOKEN|PASSWORD|PRIVATE)' -i .`
- **Every action validates and authorizes.** Pass: each exported async function in a `"use server"` file calls a schema parse and an auth/DAL function before any DB call. Verify: `rg -l "^['\"]use server['\"]" -t ts .` then `rg -n 'export async function' <file>` and read each.
- **Actions return minimal data.** Pass: no `return db.` or `return await db.` in actions. Verify: `rg -n 'return (await )?(db|prisma)\.' $(rg -l "^['\"]use server['\"]" -t ts .)`
- **No mutation during render.** Pass: no `cookies().delete`/`set`, DB writes, or `revalidate*` calls in `page.tsx`/`layout.tsx` bodies. Verify: `rg -n '\.(delete|set)\(|revalidate(Path|Tag)\(|\.(create|update|delete)(Many)?\(' -g '**/{page,layout}.tsx' .`
- **Params validated.** Pass: values from `await params` pass a schema or explicit check before DB use. Verify: `rg -n 'await params' -t ts .` and read each.
- **Proxy has a matcher and is not the only auth.** Pass: `config.matcher` present; actions still authorize. Verify: `rg -n 'matcher' proxy.ts middleware.ts src/proxy.ts 2>/dev/null`
- **One caching model.** Pass: either `cacheComponents: true` with `"use cache"`, or the previous model, not both. Verify: `rg -n 'cacheComponents|use cache|export const (revalidate|dynamic)' -t ts .`
- **Middleware renamed on Next 16+.** Pass: no `middleware.ts` when `next` is 16 or newer. Verify: `ls middleware.ts src/middleware.ts 2>/dev/null`
