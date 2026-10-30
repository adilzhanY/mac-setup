# Performance

Measure first, then change one thing, then measure again. Models tend to "optimize" by guessing (memoize everything, add a cache, rewrite a loop) without a profile, which adds complexity and often no speed. This file sets the budgets, the measurement tools per stack, the common real causes, and the checks.

## Contents

1. Rules (P1 to P12)
2. Budgets (defaults)
3. Backend and database
4. Node profiling
5. Rust profiling and benchmarks
6. Web frontend
7. React Native
8. Checks

## 1. Rules

**P1. No optimization without a measurement that shows the problem and a measurement that shows the fix.** Record before and after numbers in the PR description (p50, p95 or p99, and the load or input size).

**P2. Measure the right thing at the right percentile.** Users feel the tail; report p95/p99 for latency, p75 for web vitals (the threshold Google uses), and the distribution, not the mean (SRE book: a 100 ms average can hide 1% of requests at 5 s).

**P3. Measure in production like conditions.** Production build (`NODE_ENV=production`, `--release`, React Native release build), realistic data sizes, a mid range or low end device for mobile, throttled network for web. Debug builds and dev servers lie by 2x to 10x.

**P4. Set budgets and enforce them in CI** (section 2). A budget without a check is a wish.

**P5. Fix the algorithm and the I/O pattern before micro optimizing.** In application code most slowness is N+1 queries, missing indexes, unbounded result sets, serial awaits that could be parallel, large payloads, re-renders, or blocking the event loop or the UI thread. Not loop syntax.

**P6. Benchmarks are statistical.** Warm up, repeat, report variance, compare against a baseline in the same environment (`criterion`, `divan`, `hyperfine`, `vitest bench`, `mitata`). One run is noise. CI runners are noisy: compare relative change or use instruction counts (iai-callgrind, CodSpeed) for gating.

**P7. Caches are a last resort, and every cache has a bound, a TTL and an invalidation story.** A cache is also a new failure mode (see `resilience-patterns.md` R25 on capacity caches).

**P8. Do not block the event loop (Node) or the async runtime (Rust).** CPU work over about 10 ms per call goes to a worker thread (`worker_threads`, `piscina`) or `tokio::task::spawn_blocking` / a rayon pool. No sync file or crypto APIs (`fs.readFileSync`, `crypto.pbkdf2Sync`) in request handlers.

**P9. Pagination and limits everywhere.** Every list endpoint and query has a maximum page size; keyset (cursor) pagination for large or deep lists instead of `OFFSET`.

**P10. Payloads are budgeted.** Responses select the fields the client needs; images resized and in modern formats; compression on (gzip or brotli) for text.

**P11. Regressions are caught where they are introduced.** Performance tests on main against a stored baseline; bundle size check on every PR.

**P12. Remove the measurement scaffolding or keep it as real telemetry.** Ad hoc `console.time` and `Instant::now()` prints do not ship.

## 2. Budgets (defaults)

Adjust per product, but start with these and write them down:

| Area | Budget | Source / reason |
|---|---|---|
| Web LCP | 2.5 s or less at p75 | Core Web Vitals "good" threshold |
| Web INP | 200 ms or less at p75 | Core Web Vitals |
| Web CLS | 0.1 or less at p75 | Core Web Vitals |
| Initial JS (compressed) for a content or marketing page | about 100 to 170 KB | Fits LCP on a mid range phone over slow 4G; enforce with `size-limit` |
| API read endpoint | p99 under 300 ms server time | Leaves room for network on mobile |
| API write endpoint | p99 under 1 s | |
| DB query in a request path | under 50 ms, and at most about 10 queries per request | Above that, look for N+1 |
| Node event loop delay | p99 under 50 ms | Above that, every request waits |
| Mobile app cold start to interactive | under 2 s on a mid range Android | Android vitals flags 5 s+ cold starts as excessive |
| Mobile frame rate | 60 fps on JS and UI thread during scroll and animation (16.7 ms per frame) | Dropped frames read as jank |

## 3. Backend and database

Most backend latency is in the database. Tools and habits:

- `EXPLAIN (ANALYZE, BUFFERS)` every new query against production sized data. Look for `Seq Scan` on large tables, row estimate far from actual rows (stale stats: `ANALYZE`), and `Sort` or `Hash` spilling to disk.
- Enable `pg_stat_statements` and review the top queries by `total_exec_time` weekly; that list, not intuition, picks what to optimize.
- `log_min_duration_statement = 250ms` (or similar) in production to catch slow queries; `auto_explain` for plans of slow ones.
- N+1 detection: count queries per request in the canonical log line (`db_query_count`); a test can assert a maximum query count for a list endpoint. Fix with a join, `WHERE id = ANY($1)`, or a dataloader.
- Index the columns used in `WHERE`, `JOIN` and `ORDER BY` of hot queries; every foreign key column used in joins or cascading deletes gets an index (Postgres does not create it automatically).
- Connection pool size is small: start near `cores * 2` per database server across all app instances, not 100 per instance. Too many connections slow Postgres down. Use PgBouncer (transaction mode) when instances times pool size exceeds what the server handles.
- Run independent awaits in parallel (`Promise.all`, `tokio::join!`), but bounded (`p-limit`, `buffer_unordered(n)`), never an unbounded `Promise.all` over user sized input.

## 4. Node profiling

| Question | Tool |
|---|---|
| Where is CPU time going? | `node --cpu-prof server.js` (writes `.cpuprofile`, open in Chrome DevTools Performance tab), or `node --inspect` and record in `chrome://inspect`; flame graph with `0x` |
| Is the event loop blocked? | `perf_hooks.monitorEventLoopDelay()` exported as a metric; `--cpu-prof` during a spike |
| Memory leak? | `node --heap-prof`, or heap snapshots via `--inspect` (take three, compare retained objects); watch RSS and heap used over hours |
| Async waits (DB, HTTP)? | Traces (OpenTelemetry) show where time goes across awaits; CPU profiles do not |
| Load test | `autocannon`, `k6`, `oha` against a production build |

Note: the Clinic.js tool family is no longer maintained; prefer the built in `--cpu-prof` / `--heap-prof` and DevTools.

## 5. Rust profiling and benchmarks

- Profile release builds with symbols: `CARGO_PROFILE_RELEASE_DEBUG=true cargo flamegraph --bin app` (cargo-flamegraph, uses `perf`), or `samply record ./target/release/app` (opens the Firefox Profiler UI). Keep `debug = "line-tables-only"` in a `[profile.profiling]` that inherits release.
- Benchmarks: `criterion` (statistical, HTML reports) or `divan` (simple, fast); `hyperfine` for whole CLI commands.
- Allocation heavy code: `dhat` or `heaptrack`; look for clones in hot loops, `String` building in loops, `Vec` without `with_capacity` when the size is known.
- Async: `tokio-console` for tasks that never yield or are starved; any `std::thread::sleep` or blocking I/O inside async code is a bug.
- `cargo build --timings` for slow compile times; build speed is developer performance too.

## 6. Web frontend

- Measure real users with the `web-vitals` library sent to your analytics or RUM, segmented by device class; lab tests (Lighthouse, WebPageTest) are for debugging, not for the verdict.
- Enforce bundle budgets with `size-limit` or the bundler's budget feature on every PR; inspect with `vite-bundle-visualizer` / `@next/bundle-analyzer` before adding a dependency.
- Common real causes: one large dependency imported for one function (moment, lodash full import, a chart library on every page), client side data waterfalls (fetch in child after parent rendered; fix with route level loaders or parallel queries), unoptimized hero image (LCP), layout shift from images and ads without dimensions (CLS), long tasks from heavy event handlers (INP).
- React: profile with React DevTools Profiler before adding `memo`, `useMemo`, `useCallback`. Memoization has a cost and only helps when a profile shows wasted renders of expensive subtrees. If the project uses the React Compiler, do not hand memoize.
- Virtualize long lists (`@tanstack/react-virtual`) beyond a few hundred rows.

## 7. React Native

- Always measure in a release build on a real mid range Android device; iOS simulators and debug builds hide most problems.
- Tools: the Perf Monitor overlay (JS and UI frame rates), React DevTools Profiler (renders), Hermes sampling profiler (`npx react-native profile-hermes` or the React Native DevTools performance panel on newer versions), Flashlight (`flashlight measure`) for a performance score on Android, Android Studio / Xcode Instruments for native.
- Lists: `FlashList` (Shopify) or `FlatList` with `keyExtractor`, stable `renderItem`, `getItemLayout` or `estimatedItemSize`; never `ScrollView` with `.map` over a long list.
- Animations on the UI thread: Reanimated worklets or `useNativeDriver: true`; never `setState` per frame.
- Images: sized to display size, cached (`expo-image`).
- Startup: lazy load screens, defer non critical SDK initialization (analytics, crash reporting extras) until after first render, keep the JS bundle small (Hermes bytecode helps but does not remove the cost of big modules).
- No `console.log` in production builds; it is synchronous over the bridge in some setups and costs frames.

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Perf PRs show numbers | Before and after measurements in the description | PR review |
| Bundle budget enforced | `size-limit` or bundler budget in CI | `rg -n 'size-limit|performanceBudget|budgets' package.json .github/workflows` |
| Web vitals collected | `web-vitals` reporting wired | `rg -n "from ['\"]web-vitals" src` |
| No sync APIs in request paths | 0 hits in server handlers | `rg -n 'readFileSync|writeFileSync|pbkdf2Sync|scryptSync|execSync' src/server src/routes src/api` |
| No blocking in async Rust | 0 hits in async fns | `rg -n 'std::thread::sleep|std::fs::' src` then check context; clippy is not enough, review |
| Bounded parallelism | No `Promise.all(items.map(` over user sized input without a limit | `rg -n 'Promise\.all\(\w+\.map' src` and review sizes |
| Pagination limits | Every list query has a `LIMIT` and a max page size | `rg -n -i 'select .* from' src | rg -vi 'limit'` and review list endpoints |
| No OFFSET pagination on large tables | Keyset pagination for big lists | `rg -n -i 'offset \$|\.offset\(' src` |
| FK columns indexed | Every FK used in joins has an index | SQL: compare `pg_constraint` FKs to `pg_index` (query in a script under `scripts/`) |
| pg_stat_statements on | Extension enabled in production | `psql -c "select * from pg_extension where extname='pg_stat_statements'"` |
| Query count per request bounded | Canonical log has `db_query_count`; list endpoint tests assert a max | `rg -n 'queryCount|db_query_count' src tests` |
| Event loop delay measured | Metric exported | `rg -n 'monitorEventLoopDelay' src` |
| Rust benches exist for hot paths | `benches/` with criterion or divan | `ls benches`; `rg -n 'criterion|divan' Cargo.toml` |
| RN long lists virtualized | No `ScrollView` + `.map` over data arrays | `rg -n -U '<ScrollView[\s\S]{0,400}\.map\(' src app` |
| No hand memoization when React Compiler is on | Few `useMemo`/`useCallback` added in new code | `rg -c 'useMemo|useCallback' src` trend; check `babel-plugin-react-compiler` in config |
