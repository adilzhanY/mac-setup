# Caching: layers, invalidation, failure modes

Read when: adding a cache of any kind (HTTP headers, CDN, Redis, in-process memo, client query cache), setting `Cache-Control`, or debugging stale or leaked data.

Sources: AWS Builders' Library "Caching challenges and strategies", Google SRE book ch. 22 (cold caches), RFC 9111 (HTTP caching), RFC 5861 (stale-while-revalidate, stale-if-error), MDN CORS (Vary), OWASP REST Security cheat sheet, TanStack Query docs.

## Contents

1. Decide first: does this need a cache
2. HTTP caching headers: the defaults
3. CDN and shared caches: the data leak risk
4. Application caches (Redis, in-process)
5. Invalidation
6. Stampedes and cold starts
7. Client side caches
8. Checks

## 1. Decide first: does this need a cache

A cache is a second copy of the data with its own consistency bugs and its own outage modes. AWS: add one only for a measured need (latency, cost, or availability of a dependency), only when the same data is read many times (hit ratio), and only when callers tolerate stale data.

Before caching, try: an index on the slow query, removing an N+1, selecting fewer columns, or HTTP caching headers (free and correct by default).

Two kinds of cache, and they fail differently (Google SRE):

- Latency cache: the system can serve full load with the cache empty, just slower. Safe.
- Capacity cache: the system cannot serve full load without it. A flush, a deploy that changes keys, or a cache node loss overloads the database. If you have one, you must load test with the cache cold, warm it before shifting traffic, and protect the database with load shedding (AWS).

## 2. HTTP caching headers: the defaults

Set `Cache-Control` explicitly on every response. Leaving it out lets browsers and proxies apply heuristic caching.

| Response | Header |
|---|---|
| Fingerprinted static assets (`app.3f9a1c.js`, hashed images, fonts) | `Cache-Control: public, max-age=31536000, immutable` |
| HTML documents, `index.html`, service worker script | `Cache-Control: no-cache` (store but revalidate every time, with an `ETag`) |
| Authenticated API responses, anything with personal data | `Cache-Control: no-store` (OWASP REST) or `private, no-cache` if you want browser revalidation via ETag |
| Public API data that changes slowly (catalog, exchange rates) | `Cache-Control: public, max-age=60, stale-while-revalidate=300, stale-if-error=86400` |
| Responses that set cookies | `no-store` or `private`. Never `public` |
| Errors (4xx/5xx) | `no-store`, unless you deliberately negative-cache a 404 for a short time |

Meanings that are often confused:

- `no-cache` does not mean "do not cache". It means "cache, but revalidate before every use".
- `no-store` means do not store anywhere.
- `private` means only the end user's browser may store it, not a CDN or proxy.
- `max-age` is for browsers, `s-maxage` overrides it for shared caches (CDN).
- `stale-while-revalidate=N`: after `max-age`, serve stale for up to N seconds while refreshing in the background (RFC 5861). Revalidation only happens if a request arrives in that window.
- `stale-if-error=N`: on a 500, 502, 503 or 504 from the origin, serve the stale copy for up to N seconds (RFC 5861). Cheap availability insurance for public data.

Validators: send `ETag` (or `Last-Modified`) so revalidation is a 304 with no body. A weak ETag from a hash of the serialized body is fine.

## 3. CDN and shared caches: the data leak risk

The worst caching bug is serving one user's data to another. It happens when:

- An authenticated response is marked `public` or has `s-maxage`, and the CDN caches it under a key that does not include the user.
- The CDN is configured to "cache everything" on a path that also serves personalized JSON.
- A response varies by a header (`Origin`, `Accept-Language`, `Authorization`, cookie) but does not list it in `Vary`. Example: a CORS response that reflects `Access-Control-Allow-Origin` without `Vary: Origin` gets cached and served to another origin (MDN).
- Web cache deception: `/account/settings.css` routes to the account page, and the CDN caches it because of the `.css` extension. Mitigation: unknown path suffixes return 404, and cache rules key on the response `Content-Type` and `Cache-Control`, not the URL extension.

Rules:

- Default every authenticated route to `no-store` in a middleware; opt in to caching per route.
- Never cache a response that contains `Set-Cookie` in a shared cache.
- When a response depends on a request header, add it to `Vary`.
- Treat cache poisoning as an input validation problem: headers like `X-Forwarded-Host` that change the response must not be trusted from clients (AWS, ASVS 4.1.3).

## 4. Application caches (Redis, in-process)

Default pattern: cache-aside (read: try cache, on miss load from DB and set with TTL; write: update DB then delete the key).

```ts
async function getProduct(id: string): Promise<Product> {
  const key = `product:v3:${id}`;                       // v3 = schema version of the cached value
  const hit = await redis.get(key);
  if (hit) return JSON.parse(hit);
  const row = await db.product.findUniqueOrThrow({ where: { id } });
  const ttl = 300 + Math.floor(Math.random() * 60);      // jittered TTL: no synchronized expiry
  await redis.set(key, JSON.stringify(toDto(row)), "EX", ttl);
  return toDto(row);
}
```

Rules:

- Every cached entry has a TTL, even when you also invalidate explicitly. The TTL is the safety net for invalidation bugs. No TTL means stale data forever after one missed delete.
- Jitter TTLs (for example base plus 0 to 20%) so keys written together do not expire together.
- Put a schema version in the key (`product:v3:`). Old and new code run side by side during a deploy; new code must not crash on old entries and old code must not crash on new ones (AWS: "treat cached data like persistent data"). Bumping the version is also the bulk invalidation tool, but it causes a cold cache: do it at low traffic.
- Cache DTOs (what you return), not ORM objects with lazy relations or functions.
- Key by everything the value depends on: tenant, user (for personalized data), locale, permissions. A key without the tenant ID is a cross-tenant leak.
- Do not cache authorization decisions longer than you can tolerate a revoked permission still working (ASVS 8.3.2). Default: seconds, or invalidate on role change.
- Negative caching: cache "not found" and error results with a short TTL (for example 30 to 60 s) so a missing item or a failing dependency is not hammered on every request (AWS: missing negative caching worsened real outages).
- Soft and hard TTL (AWS): refresh after the soft TTL; if the refresh fails, keep serving the old value until the hard TTL. Gives availability during a dependency outage.
- Handle cache failure: a Redis timeout must not fail the request when the database is healthy. Short timeout on cache calls (for example 50 to 200 ms), then fall through. But if the cache is a capacity cache, falling through to the DB for all traffic is itself the outage; shed load instead (AWS).
- In-process caches (an LRU map) are per instance: N instances each hold their own copy and each miss hits the DB. Bound their size (`lru-cache` with `max`, `moka` in Rust); an unbounded `Map` used as a cache is a memory leak.
- Do not cache what is cheap to compute or unique per request; it only adds memory and staleness.
- Measure: hit rate, miss rate, evictions, cache latency, and downstream request rate (AWS).

## 5. Invalidation

Order of operations on write: update the database, commit, then delete the cache key. Delete, do not set: setting the new value from the writer races with a concurrent reader that loaded the old row and writes it after you.

```
reader: miss -> reads old row from DB ..................... -> SET old value (stale until TTL)
writer:                 UPDATE row -> COMMIT -> DEL key
```

The race above still exists with delete (the reader's SET lands after the DEL). Mitigations, in order of preference:

1. Short TTL that bounds the staleness. Usually enough.
2. Delete again after a short delay (for example 1 s) via a job ("delayed double delete").
3. Store a version with the value and only SET if the version is newer (Lua compare-and-set).
4. Invalidate from the database change stream (logical replication, Debezium, Supabase Realtime) instead of from application code, so no write path can forget.

Rules:

- Every write path that changes cached data invalidates it. Grep every `UPDATE`/`update(` on the table and confirm each one deletes the key, including admin tools, migrations, and background jobs. A missed path is the classic stale data bug.
- Invalidate inside the same unit of work that commits, after commit. Invalidating before commit lets a reader repopulate with the old row.
- For list or aggregate caches (a user's order list), either delete the list key on every child write, or do not cache lists and cache only items.
- Prefer tag or prefix versioning for groups: keep `org:{id}:ver` and include it in every key for that org; bump it to invalidate everything for the org at once.

## 6. Stampedes and cold starts

When a hot key expires, every concurrent request misses and hits the database at once (thundering herd). When a new instance starts or the cache is flushed, all keys miss.

- Single flight (request coalescing): only one in-flight load per key, others await it (AWS). In process: a map of key to promise (see `rate-limits-retries-timeouts.md` section 8). Across instances: a short Redis lock (`SET key:lock 1 NX PX 5000`), others serve stale or wait briefly.
- Refresh ahead: refresh hot keys in the background before they expire (soft TTL), or probabilistic early expiration (refresh with rising probability as expiry approaches).
- Jittered TTLs (section 4).
- Warm up slowly: ramp traffic onto new instances or new cache versions (Google SRE). Load test with caches disabled to know the real capacity of the database (AWS).

## 7. Client side caches

- Server state on the client belongs in a query cache (TanStack Query, SWR, RTK Query, Apollo), not copied into a global store by hand. Copies go stale and are never invalidated.
- After a mutation, invalidate the affected queries (`queryClient.invalidateQueries({ queryKey: ["orders"] })`) or update them from the mutation response. Do not leave the list showing pre-mutation data.
- Query keys include every input (`["orders", orgId, filters]`). Missing an input means two different requests share one cache entry.
- On logout, clear the query cache and any persisted cache (`queryClient.clear()`), or the next user on the device sees the previous user's data.
- Do not persist personal data to `localStorage` caches by default; it survives logout and is readable by any XSS.
- Service worker caches: never cache authenticated API responses or HTML containing user data with a cache-first strategy.

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Authenticated responses not shared-cached | every authenticated route sends `no-store` or `private` | `curl -sI -H "Cookie: ..." https://host/api/me \| grep -i cache-control` |
| Hashed assets immutable | `/assets/*.[hash].js` returns `max-age=31536000, immutable` | `curl -sI` an asset |
| HTML revalidates | `index.html` returns `no-cache` or short max-age with ETag | `curl -sI /` |
| Vary on reflected headers | responses that echo `Origin` or depend on `Accept-Language` include it in `Vary` | `curl -sI -H "Origin: https://a.example" ...` |
| Every cache set has a TTL | no `redis.set(k, v)` without `EX`/`PX`, no `SET` without expiry | `rg -n "\.set\([^)]*\)" ` and review; `rg -n "redis.*set" ` for missing `EX` |
| Keys versioned and tenant scoped | cache keys include a version segment and the tenant/user when data is scoped | `rg -n "redis\.(get\|set)\(\`" ` and read key templates |
| Invalidation on every write path | each write to a cached table deletes the key after commit | list `rg -n "update\(\|UPDATE <table>" ` and confirm a `del` follows |
| Bounded in-process caches | in-memory caches have a max size | `rg -n "new Map\(\)" ` used as cache; prefer `new LRUCache({ max })` |
| Cache failure is not request failure | cache calls have a short timeout and a fallback | read the cache wrapper; stop Redis locally and hit the endpoint |
| Client cache cleared on logout | logout calls `queryClient.clear()` or equivalent | `rg -n "logout\|signOut" ` and read the handler |
