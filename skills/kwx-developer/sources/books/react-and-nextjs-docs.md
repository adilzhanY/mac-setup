# React, React Native and Next.js official docs

Legal sources: https://react.dev (docs and blog), https://reactnative.dev/docs, https://nextjs.org/docs (all public).

## What I read

React: "You Might Not Need an Effect", "Choosing the State Structure", "React Compiler: Introduction", "eslint-plugin-react-hooks" reference, the React 19.2 release post, the plugin README (flat config). React Native: "Performance Overview", "Optimizing FlatList Configuration", the 0.82 and 0.84 release posts (via search summaries), FlashList v2 changes page. Next.js: "Server and Client Components", "Data Security" guide, `proxy.js` reference, "Caching" (Cache Components).

## Key lessons used in languages/typescript/

- Effects only for external systems; the table of Effect replacements (derive in render, `key` reset, handlers, lift state, `useSyncExternalStore`); fetching in Effects needs race protection. (react-and-react-native.md 4 and 5)
- State structure: group, no contradictions, no redundancy, no duplication, flatten, do not mirror props. (react-and-react-native.md 3)
- React Compiler is stable; new code relies on it instead of `useMemo`/`useCallback`; do not strip existing memoization without tests; the hooks plugin ships compiler-derived rules in `recommended`. (react-and-react-native.md 6)
- React 19.2 `useEffectEvent` rules. (react-and-react-native.md 4)
- React Native: 16.67 ms frame budget, profile release builds, strip `console.*`, `FlatList` tuning numbers and `getItemLayout`, native driver, `requestAnimationFrame` for heavy press handlers, FlashList v2 recycling rules. (react-and-react-native.md 12)
- Next.js: `"use client"` marks a module-graph boundary, place it on leaves; serializable props; `server-only`; `NEXT_PUBLIC_` exposure; DAL with DTOs; server actions are reachable by direct POST and must re-authenticate and authorize; return minimal data; no mutations in render; audit checklist; `proxy.ts` is not an authorization layer; Cache Components caching model. (nextjs.md)
