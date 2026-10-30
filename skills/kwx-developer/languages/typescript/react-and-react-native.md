# React and React Native

Read when: writing or reviewing React components, hooks, state, effects, data fetching, lists, or React Native screens. For Next.js server/client rules read nextjs.md. For visual design and accessibility of the UI itself, use the kwx-designer skill; this file covers code correctness and performance.

## Contents

1. Versions this file assumes
2. Rules of React (purity, hooks)
3. State: what to store and where
4. Effects: you probably do not need one
5. Data fetching
6. Memoization and the React Compiler
7. Keys and lists
8. Components and props
9. Forms
10. Context
11. Errors and loading
12. React Native specifics
13. Checks

## 1. Versions this file assumes

React 19.x (19.2: `<Activity>`, `useEffectEvent`), React Compiler 1.0 stable, `eslint-plugin-react-hooks` 6+ whose `recommended` flat preset includes the compiler-derived rules. React Native 0.82+ runs only the New Architecture; 0.84 made Hermes V1 the default engine. Check `package.json` before applying version-specific advice; an older project gets the advice for its version.

## 2. Rules of React

- Components and hooks are pure during render: same props and state give the same JSX; no mutation of props, state, module variables or refs during render; no side effects (fetching, subscriptions, `Math.random()`, `Date.now()` that affects output) in the render body. React may render twice (Strict Mode) or discard renders.
- Hooks only at the top level of a component or custom hook: never in conditions, loops, after an early `return`, or in event handlers. Custom hooks start with `use`.
- Never call a component as a function (`{Header()}`); render it (`<Header />`).
- Never define a component inside another component: it gets a new identity every render, so its state resets and its DOM remounts. Lint: `react-hooks/static-components`.
- Treat state as immutable: `setItems([...items, x])`, `setUser({ ...user, name })`, never `items.push(x); setItems(items)`.
- Lint: `eslint-plugin-react-hooks` `recommended` (rules-of-hooks, exhaustive-deps, purity, refs, immutability, set-state-in-render, set-state-in-effect, static-components, and more). These rules work with or without the compiler; when the compiler meets code that breaks them it skips that component.

## 3. State: what to store and where

From the React docs, "Choosing the state structure":

- **Do not store what you can compute.** `const fullName = first + " " + last;` not a `fullName` state kept in sync.
- **No contradictory state.** One `status: "typing" | "sending" | "sent"` instead of `isSending` plus `isSent`.
- **No duplicated objects.** Store `selectedId` and derive `items.find((i) => i.id === selectedId)`, not a copy of the selected item that goes stale.
- **Do not mirror props in state.** `useState(props.color)` only reads the prop on the first render. Use the prop directly, or name it `initialColor` when ignoring later changes is the intent.
- **Flatten nested data** that you update by ID (`byId` maps plus ID arrays).
- **Group values that always change together** (`{ x, y }`).
- **Keep state as low as possible**, lift it only to the closest common parent. A state change at the root re-renders everything below (React Native docs: this can block the JS thread for hundreds of milliseconds).
- **Server data is not UI state.** Do not copy fetched data into `useState`; it belongs to a cache (TanStack Query, SWR, RSC, a router loader). See section 5.
- **URL state** (filters, tabs, pagination, selected item) lives in the URL so reload, back button and sharing work.
- **Global client state** (Zustand, Redux, Jotai) only for state many distant components truly share and that is not server data. Most apps need far less than they think. Use whichever the repo already has; never add a second.

## 4. Effects: you probably do not need one

"If there is no external system involved, you shouldn't need an Effect." Replace these common Effects:

| You wrote | Write instead |
|---|---|
| `useEffect(() => setX(f(a, b)), [a, b])` | `const x = f(a, b);` during render (`useMemo` only if measured slow) |
| Effect that resets state when a prop changes | `<Profile key={userId} />` |
| Effect that adjusts part of state on prop change | store an ID and derive; or adjust during render |
| Effect reacting to a state flag set by a click (`if (submitted) post(...)`) | do the work in the event handler |
| Effect calling `onChange(value)` after `setValue` | call both in the same event handler, or lift state up |
| Effect chains (A sets B, an Effect on B sets C) | compute in render, set all next state in one handler |
| Effect subscribing to a store or browser API with `useState` mirror | `useSyncExternalStore` |
| App init in `useEffect(..., [])` that must run once | module-level code guarded by `typeof window !== "undefined"`, or a module-level `let didInit` flag |

Effects are right for synchronising with something outside React: a non-React widget, a browser API subscription, a WebSocket, analytics on display. Every such Effect returns a cleanup that undoes it.

Rules for the Effects you keep:

- Dependencies are complete; never silence `exhaustive-deps`. If an Effect re-runs too often, the fix is to move logic out, or use `useEffectEvent` (React 19.2) for the non-reactive "event" part, never to drop a dependency.
- `useEffectEvent` functions are never dependencies, are called only from inside Effects, and are not a way to silence the lint rule.
- No synchronous `setState` in an Effect body to derive state (lint: `react-hooks/set-state-in-effect`).
- Object and function dependencies created during render change every render. Move them inside the Effect, or derive primitives.

## 5. Data fetching

- Prefer the framework's data layer: React Server Components (Next.js), route loaders (React Router, TanStack Router, Expo Router), or a cache library (TanStack Query, SWR). These handle caching, deduplication, race conditions, retries, revalidation and loading states. A raw `useEffect` + `fetch` + `useState` handles none of them.
- If you must fetch in an Effect, guard against races and abort on cleanup:

```tsx
useEffect(() => {
  const controller = new AbortController();
  fetchResults(query, { signal: controller.signal })
    .then(setResults)
    .catch((err: unknown) => {
      if (err instanceof DOMException && err.name === "AbortError") return;
      setError(err);
    });
  return () => controller.abort();
}, [query]);
```

- Parse responses with a schema (validation-at-boundaries.md); a typed `fetch` wrapper that returns `T` without parsing is a cast.
- Avoid waterfalls: a parent that fetches, renders a child that fetches, renders a grandchild that fetches. Fetch in parallel at the route level, or use RSC/loaders.
- Mutations: send them from event handlers or form actions, then invalidate the affected queries. Optimistic UI with `useOptimistic` or the cache library's API, always with rollback on failure.

## 6. Memoization and the React Compiler

- With the React Compiler enabled (check for `babel-plugin-react-compiler` or `reactCompiler: true` in the framework config), do not add `useMemo`, `useCallback` or `React.memo` in new code. The compiler memoizes components, hooks and values in render. Use the hooks only as an escape hatch, for example when a memoized value is an Effect dependency.
- Do not remove existing manual memoization in compiled code without testing; it can change compiler output.
- Without the compiler: memoize only after measuring (React DevTools Profiler, "why did this render"). `useMemo` for expensive computations (over about 1 ms, measured with `console.time`) and for referential stability of values passed to memoized children or used as dependencies. `React.memo` on components that re-render often with the same props and are expensive.
- Memoization does not fix re-renders caused by state placed too high or by context values that change every render. Fix the structure first.

## 7. Keys and lists

- Keys are stable, unique IDs from the data (`item.id`). Never `Math.random()` or `crypto.randomUUID()` during render (remounts everything every render).
- Index keys only for static lists that never reorder, filter or insert. With reorderable lists, index keys attach state (input text, checkbox, animation) to the wrong item.
- Keys are unique among siblings only, not globally.
- Changing a `key` resets a subtree on purpose (section 4).

## 8. Components and props

- Props types: `type Props = {...}` (or the repo's interface convention) next to the component. Do not use `React.FC`; type the props parameter and let the return type infer (`function Card({ title }: Props)`).
- React 19: `ref` is a normal prop for function components; do not add `forwardRef` in new code. `<Context value={...}>` replaces `<Context.Provider>`.
- Children: `children: React.ReactNode`. Render props and slot props (`header: React.ReactNode`) over boolean prop explosions (`showHeader`, `headerVariant`, `headerCompact`).
- Avoid prop drilling deeper than about three levels by composition first (pass the rendered element down as `children`), context second.
- Event handler props are named `onX`, handler functions `handleX`.
- No business logic or data fetching in leaf UI components; they take data and callbacks.
- Conditional rendering with numbers: `{count && <Badge />}` renders `0`. Write `{count > 0 && <Badge />}`.
- Server-rendered markup must match the first client render: no `typeof window` branches, `Date.now()` or random values in render output (hydration mismatch). Read browser-only values in an Effect or with `useSyncExternalStore` and a server snapshot.

## 9. Forms

- Uncontrolled inputs with `FormData` and form actions (`<form action={fn}>`, `useActionState`, `useFormStatus`) for simple forms; React 19 resets uncontrolled forms after a successful action.
- Controlled inputs (or React Hook Form) when you need per-keystroke validation, dependent fields or formatting.
- Validate with the same schema on client and server; the server is the authority.
- Disable the submit button while pending and make submission idempotent on the server (double clicks, retries).

## 10. Context

- Context is for values that many components at different depths need and that change rarely (theme, locale, current user, a store instance). Not a replacement for props or a state manager.
- Every consumer re-renders when the value identity changes. Keep the value stable (memoize the object, or pass a store and let consumers subscribe to slices), and split contexts by update frequency (state context and dispatch context).
- Provide a custom hook that throws a clear error when used outside the provider:

```tsx
const CartContext = createContext<CartStore | null>(null);
export function useCart(): CartStore {
  const store = use(CartContext);
  if (!store) throw new Error("useCart must be used inside <CartProvider>");
  return store;
}
```

## 11. Errors and loading

- Error boundaries around independent regions (a widget failing must not blank the page). They catch render errors only; handle event and async errors in the handler.
- `<Suspense>` boundaries placed where a loading state makes sense to the user, not one at the root.
- Every async UI has four states designed and coded: loading, empty, error (with retry), success. The discriminated union in types-and-strictness.md section 5 models them.

## 12. React Native specifics

Performance (React Native docs, "Performance overview"):

- The budget is 16.67 ms per frame at 60 FPS (8.3 ms at 120 Hz). A 200 ms JS task drops about 12 frames. The JS thread runs React, business logic and touch handling; when it is busy, JS-driven animations freeze and touch feedback lags.
- Profile only release builds. Dev mode is much slower and misleading.
- Remove `console.*` from production bundles (`babel-plugin-transform-remove-console` in the production env); logging is a major JS-thread cost, including libraries such as redux-logger.
- Animations run on the UI thread: Reanimated worklets, or `Animated` with `useNativeDriver: true`. Animate `transform` and `opacity`, not `width`/`height`/`top`.
- Long lists: never `ScrollView` + `map` for more than a screenful. Use `FlatList` with a stable `keyExtractor`, memoized row components, `renderItem` defined outside JSX (or `useCallback`), and `getItemLayout` when rows have a fixed height. Tune `initialNumToRender` to one screen, `windowSize` (default 21 viewports) down for memory. FlashList v2 (Shopify) or Legend List for heavy lists; FlashList v2 needs no size estimates, recycles rows (so never keep item-specific state in a row without `useRecyclingState`), and needs memoized props.
- Images: thumbnails sized for the view, cached (`expo-image` or a fast-image library), never full-resolution photos in list rows.
- Heavy work after a press: let the press feedback render first (`requestAnimationFrame`, `startTransition`, or defer with `requestIdleCallback`).

Platform and correctness:

- Styles with `StyleSheet.create` outside the component (or the repo's styling system); not new inline style objects on hot list rows.
- Platform differences with `Platform.select` or `.ios.tsx` / `.android.tsx` files, not scattered `Platform.OS ===` checks in render.
- Secrets and tokens in `expo-secure-store` / Keychain / Keystore, never `AsyncStorage` (plain text on disk).
- Safe areas via `react-native-safe-area-context`, not hardcoded paddings.
- Text must be inside `<Text>`; a raw string in a `<View>` crashes.
- Never ship API secrets in the bundle: anything in JS is extractable from the app. Call your backend.
- Handle app state changes (background/foreground) for timers, sockets and polling (`AppState`).
- Native modules: on 0.82+ only New Architecture (TurboModules/Fabric) libraries work. Check a library's support before adding it.

## 13. Checks

- **Hooks lint on.** Pass: `eslint-plugin-react-hooks` `recommended` enabled, zero errors, no disabled `exhaustive-deps`. Verify: `rg -n 'react-hooks' -g 'eslint.config.*' .`; `rg -n 'eslint-disable.*(exhaustive-deps|rules-of-hooks)' -t ts -t js .` returns nothing.
- **No derived-state Effects.** Pass: no Effect whose body only calls setters from props/state. Verify: `rg -nU 'useEffect\(\(\) => \{?\s*set[A-Z]\w*\(' -t ts -t js .` and review; lint `react-hooks/set-state-in-effect`.
- **No raw fetch in Effects without abort.** Pass: every `fetch` inside `useEffect` has an `AbortController` or an ignore flag. Verify: `rg -nU -A8 'useEffect\(' -g '*.{tsx,jsx}' . | rg 'fetch\('` then check each for `abort`.
- **No index or random keys on dynamic lists.** Pass: zero in lists that change. Verify: `rg -n 'key=\{(index|i|idx)\}|key=\{Math\.random|key=\{crypto\.randomUUID' -g '*.{tsx,jsx}' .`
- **No components defined inside components.** Pass: lint clean. Verify: `react-hooks/static-components`.
- **No manual memo in compiled code (new code).** Pass: new files under the compiler have no `useMemo`/`useCallback`/`memo(` without a comment. Verify: `rg -n 'useMemo|useCallback|React\.memo|\bmemo\(' -g '*.{tsx,jsx}' .` on changed files.
- **No forwardRef in new React 19 code.** Pass: zero in new files. Verify: `rg -n 'forwardRef' -g '*.{tsx,jsx}' .`
- **No `count &&` rendering zero.** Pass: numeric conditions compare explicitly. Verify: `rg -nP '\{\s*\w+\.(length|count|size)\s*&&' -g '*.{tsx,jsx}' .`
- **RN: no console in release.** Pass: the remove-console plugin is configured for production. Verify: `rg -n 'transform-remove-console' babel.config.* .babelrc* 2>/dev/null` or equivalent bundler setting.
- **RN: no ScrollView lists.** Pass: no `ScrollView` wrapping `.map(`. Verify: `rg -nU -A5 '<ScrollView' -g '*.tsx' . | rg '\.map\('`
- **RN: no tokens in AsyncStorage.** Pass: zero. Verify: `rg -n 'AsyncStorage\.setItem\(.*(token|secret|password|key)' -i -g '*.{ts,tsx}' .`
- **One client state library.** Pass: at most one of redux, zustand, jotai, mobx, recoil, valtio. Verify: `rg -o '"(@reduxjs/toolkit|redux|zustand|jotai|mobx|recoil|valtio)"' -g 'package.json' -g '!**/node_modules/**' . | sort | uniq -c`
