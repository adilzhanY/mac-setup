# Load testing

How to write, run and read a load test for an HTTP API: k6 as the default (scripts, scenarios, thresholds, checks), quick one line runs with oha or vegeta, the specifics of Supabase and Postgres backed APIs, and how to read the results without fooling yourself. Read `performance.md` first: requirements as percentiles, coordinated omission, and the environment rules apply to every run here.

## Contents

1. Tool choice
2. k6: a complete script
3. k6: scenarios and executors
4. k6: thresholds and checks
5. k6: test types as scenarios
6. Data, auth and realistic traffic
7. Quick runs: oha, vegeta, hey/wrk
8. Supabase and Postgres backed APIs
9. Reading the results
10. Checks

## 1. Tool choice

| Tool | Model | Use for | Notes |
|---|---|---|---|
| k6 (2.3, September 2026) | open (arrival rate) or closed (VUs) | scripted scenarios, thresholds as pass/fail, CI | JavaScript or TypeScript scripts; Docker image `grafana/k6`; k6 2.0 removed the `externally-controlled` executor and old cloud commands |
| oha (1.16) | open with `-q` and `--latency-correction` | quick single endpoint checks, live TUI | in Arch `extra`; JSON output with `--output-format json` |
| vegeta (12.13) | open (constant `-rate`) | quick runs, piping targets, HDR plots | designed to avoid coordinated omission |
| Locust (2.47) | closed (users) | teams that prefer Python, complex user flows | users wait for responses: closed model, read latency with care |
| wrk2 | open (`-R`) | high rate HTTP benchmarks | C, Lua scripts; unmaintained but correct |
| wrk, ab, hey | closed | rough max throughput only | do not use their latency percentiles under saturation |

Default: k6. It has thresholds that fail the run, an open model executor, and a JSON summary for reports. Evidence: moderate (k6 docs).

Install: Arch has no official package (use the AUR, a release binary, or Docker). The Docker form needs nothing installed:

```bash
docker run --rm -i --network host -e BASE_URL=http://127.0.0.1:3000 grafana/k6:2.3.0 run - < script.js
```

## 2. k6: a complete script

Verified 2026-10-31 with `grafana/k6:2.3.0` against a local server: 501 iterations at 50 per second, 0 dropped, all thresholds passed, exit code 0.

```js
// load/feed.js
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    steady: {
      executor: 'constant-arrival-rate',   // open model: start 50 iterations per second regardless of latency
      rate: 50,
      timeUnit: '1s',
      duration: '10m',
      preAllocatedVUs: 20,                  // VUs ready at start
      maxVUs: 200,                          // k6 may add VUs up to this when responses slow down
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],                    // under 1% errors
    http_req_duration: ['p(95)<200', 'p(99)<500'],     // the requirement
    dropped_iterations: ['count<1'],                   // generator kept the rate; otherwise the run is invalid
    checks: ['rate>0.99'],
  },
  summaryTrendStats: ['min', 'med', 'p(90)', 'p(95)', 'p(99)', 'max'],
};

export default function () {
  const res = http.get(`${__ENV.BASE_URL}/api/feed?limit=20`, {
    headers: { Authorization: `Bearer ${__ENV.TOKEN}` },
    tags: { name: 'GET /api/feed' },                   // groups URLs with ids under one name
  });
  check(res, {
    'status is 200': (r) => r.status === 200,
    'has 20 items': (r) => r.json('items').length === 20,
  });
}
```

Run and keep the raw summary:

```bash
k6 run -e BASE_URL=http://127.0.0.1:3000 -e TOKEN="$TOKEN" --summary-export=summary.json load/feed.js
echo "exit=$?"     # non zero when a threshold failed
```

Rules:

1. **Run a smoke version first** (`rate: 1`, `duration: '30s'`) and read every check. A script that sends wrong requests produces fast 401s that look great. Evidence: strong (k6 docs: "Start with a smoke test").
2. **Tag requests with a `name`** when URLs contain ids, or every URL becomes its own metric series. Evidence: moderate (k6 docs).
3. **Thresholds are the pass condition. Make the CI step depend on k6's exit code.** Evidence: moderate.
4. **Check content, not just status,** because a 200 with an error body or an empty list is not success. Evidence: moderate.
5. **Do not add `sleep()` to arrival rate scenarios to "pace" users.** The executor already paces iterations; sleep only adds VUs. In VU based (closed) scenarios, think time with `sleep()` is realistic. Evidence: moderate (k6 docs).

## 3. k6: scenarios and executors

| Executor | Model | Use |
|---|---|---|
| `constant-arrival-rate` | open | latency at a fixed request rate (default for budgets) |
| `ramping-arrival-rate` | open | ramps, spikes, breakpoint tests |
| `constant-vus` | closed | N users looping as fast as responses allow |
| `ramping-vus` | closed | user count ramps |
| `shared-iterations` / `per-vu-iterations` | closed | a fixed amount of work (data setup, smoke) |

Open vs closed (k6 docs): in the closed model a VU starts its next iteration only when the previous one finishes, so a slow system receives less load and latency looks better than reality. k6 names this coordinated omission. In the open model, arrivals do not depend on response times.

`dropped_iterations` counts iterations an arrival rate executor could not start because no VU was free. Drops at the start usually mean too few pre-allocated VUs; drops later usually mean the system is slowing down. Put a threshold on it (k6 docs). Evidence: moderate.

Several scenarios in one test, for a realistic mix:

```js
export const options = {
  scenarios: {
    browse: { executor: 'constant-arrival-rate', rate: 40, timeUnit: '1s', duration: '10m',
              preAllocatedVUs: 20, maxVUs: 200, exec: 'browse' },
    post:   { executor: 'constant-arrival-rate', rate: 5,  timeUnit: '1s', duration: '10m',
              preAllocatedVUs: 5,  maxVUs: 50,  exec: 'createPost' },
  },
  thresholds: {
    'http_req_duration{scenario:browse}': ['p(95)<200'],
    'http_req_duration{scenario:post}':   ['p(95)<400'],
    http_req_failed: ['rate<0.01'],
  },
};
export function browse() { /* GET requests */ }
export function createPost() { /* POST requests */ }
```

## 4. k6: thresholds and checks

Threshold forms (k6 docs):

```js
thresholds: {
  http_req_failed: ['rate<0.01'],
  http_req_duration: [
    'p(95)<200',
    { threshold: 'p(99)<1500', abortOnFail: true, delayAbortEval: '30s' },   // stop a doomed run early
  ],
  'http_req_duration{name:GET /api/feed}': ['p(99)<500'],     // per tagged request
  checks: ['rate>0.99'],
}
```

- `abortOnFail` stops the test when a threshold is clearly broken; `delayAbortEval` waits so early warmup samples do not abort it.
- A `check` failing does not fail the run by itself; add a threshold on `checks`.
- Thresholds on percentiles need enough samples. A 30 second run at 5 requests per second gives 150 samples: its p99 is about one request.

## 5. k6: test types as scenarios

Shapes from the k6 test type guide, written with arrival rate executors so latency stays honest:

```js
// average load: ramp, hold, ramp down
{ executor: 'ramping-arrival-rate', startRate: 0, timeUnit: '1s', preAllocatedVUs: 50, maxVUs: 500,
  stages: [ { target: 50, duration: '2m' }, { target: 50, duration: '15m' }, { target: 0, duration: '1m' } ] }

// stress: hold above normal (for example 2x)
stages: [ { target: 100, duration: '5m' }, { target: 100, duration: '20m' }, { target: 0, duration: '2m' } ]

// spike: sudden jump, short, then check recovery
stages: [ { target: 50, duration: '1m' }, { target: 500, duration: '30s' }, { target: 500, duration: '2m' },
          { target: 50, duration: '30s' }, { target: 50, duration: '3m' } ]

// breakpoint: keep rising until thresholds fail; use abortOnFail
stages: [ { target: 1000, duration: '30m' } ]

// soak: average load for hours; watch memory, connections, disk, queue length over time
stages: [ { target: 50, duration: '5m' }, { target: 50, duration: '4h' }, { target: 0, duration: '5m' } ]
```

For spikes, the interesting result is the recovery: does latency return to normal after the spike, and how long does it take? For soak tests, plot memory and connection counts of the server over time; a slow upward line is a leak even when latency passes. Evidence: moderate.

## 6. Data, auth and realistic traffic

- **Use many test users and many ids,** not one. One user hitting one row is served from one cache line and one lock; real traffic is spread. Load ids from a file with `SharedArray`:

```js
import { SharedArray } from 'k6/data';
const users = new SharedArray('users', () => JSON.parse(open('./users.json')));
export default function () {
  const u = users[Math.floor(Math.random() * users.length)];
  http.get(`${__ENV.BASE_URL}/api/feed`, { headers: { Authorization: `Bearer ${u.token}` } });
}
```

- **Create tokens before the test** (in `setup()` or a separate script), not in every iteration. Login endpoints are rate limited and slow by design (password hashing); logging in per iteration measures the hash function. Test login on its own if it matters.
- **Mix reads and writes as in production.** Writes change caches, locks and table sizes. Clean up created data after the run, or use a disposable environment.
- **Payload sizes and query parameters from real usage:** page sizes, search terms, filters.
- **Do not reuse one connection for everything unless clients do.** k6 reuses connections per VU by default; browsers open several. For a "new users arriving" test, set `noConnectionReuse: true` in options.

## 7. Quick runs: oha, vegeta, hey/wrk

For a five minute "how does this endpoint behave at 200 req/s?" check.

oha (README):

```bash
# 60 s at 200 requests per second, latency measured from scheduled send time
oha -z 60s -q 200 --latency-correction --disable-keepalive -c 50 http://127.0.0.1:3000/api/health
oha -z 60s -q 200 --latency-correction --output-format json http://127.0.0.1:3000/api/feed > oha.json
```

`--latency-correction` is ignored unless `-q` (or `--burst-delay`) is set. `--disable-keepalive` simulates new connections per request (README). Without `-q`, oha is a closed loop throughput test.

vegeta (README):

```bash
echo "GET http://127.0.0.1:3000/api/feed" | vegeta attack -rate=200/s -duration=60s | tee results.bin | vegeta report
vegeta report -type=hist[0,50ms,100ms,200ms,500ms,1s] results.bin
```

`-rate=0` means "as fast as possible", which turns it into a closed style throughput test.

wrk and hey: closed loop. Use them only for "what is the maximum throughput before it falls over", and do not report their latency percentiles from a saturated run.

## 8. Supabase and Postgres backed APIs

What is special:

- **Where to run it.** Locally (`supabase start`) for finding slow queries and N+1 patterns; a separate hosted project or branch with the same compute tier for real numbers. Never the production project without the owner's yes. Local numbers do not predict hosted numbers: different hardware, no network latency, different pooler.
- **Connection limits.** Hosted Supabase puts a pooler (Supavisor, or a dedicated PgBouncer) in front of Postgres. Each compute size has a maximum number of pooler clients and a pool size; when the pooler reaches its client limit it stops accepting new connections until others close (Supabase pooling docs). Serverless functions that open a connection per request hit this first. A load test should show where it happens.
- **Which path you test.** PostgREST (`/rest/v1/...` with the anon or user JWT), RPC functions (`/rest/v1/rpc/...`), Edge Functions, or your own API server with a direct or pooled connection. They have different limits; test the path clients use.
- **RLS costs time.** Policies run per row. Test with the user JWT, not the service role key, or you measure a path that bypasses RLS. Wrap `auth.uid()` in `(select auth.uid())` in policies so Postgres caches it per statement instead of calling it per row, and index every column policies filter on; a load test before and after shows the difference (Supabase RLS docs). Evidence: moderate.
- **Auth rate limits.** Sign in, sign up, OTP and email endpoints are rate limited on hosted projects. Pre-create users and tokens.
- **Watch the database during the run:**

```sql
-- top queries by total time (needs pg_stat_statements)
select calls, round(total_exec_time) as total_ms, round(mean_exec_time, 1) as mean_ms, left(query, 80)
from pg_stat_statements order by total_exec_time desc limit 10;

-- connections by state, and who is waiting
select state, wait_event_type, count(*) from pg_stat_activity group by 1, 2 order by 3 desc;
```

- **Reset statistics before the run** (`select pg_stat_statements_reset();`) so the numbers belong to this test.
- **Data volume:** seed realistic row counts first (`generate_series`). An endpoint that is fast on 100 rows and slow on 1 million is the usual finding (missing index; see kwx-developer `data/indexes-and-queries.md`).

## 9. Reading the results

Read in this order:

1. **Was the run valid?** Checks near 100%, `dropped_iterations` 0 (or explained), the achieved rate equals the target, the generator was not overloaded, no unexpected status codes.
2. **Errors:** rate and type (`http_req_failed`, status breakdown). Timeouts and 5xx under load are the most important finding.
3. **Percentiles against the requirement:** p50, p90, p95, p99, max.
4. **Over time, not only the totals:** a test can pass overall and still have a 2 minute bad period. Export time series (`k6 run --out json=raw.json` or to a time series database) and look at latency and errors per 10 seconds.
5. **The limiter** (USE checks from `performance.md`): CPU, memory, connections, locks, a slow query.
6. **Compare with the previous run** under the same conditions. A regression is a change bigger than the run to run spread.

Typical patterns:

| Pattern | Likely cause |
|---|---|
| Latency flat, then a knee and a steep rise | a resource saturated (CPU, pool, a lock); the knee is your capacity |
| p50 fine, p99 and max bad | GC pauses, cold caches, lock contention, one slow query plan, noisy neighbour |
| Latency grows steadily over a soak test | leak, growing table without index, queue backlog |
| Errors start at a round number of connections | pool or pooler limit, `ulimit -n`, `max_connections` |
| Throughput stops rising while CPU is low | waiting on IO, locks, a downstream service, or the generator itself |
| Great numbers with many 4xx | the script is wrong (auth, ids) |

## 10. Checks

| Check | Pass condition |
|---|---|
| Permission | target environment approved; not production or a shared service unless the owner agreed |
| Smoke first | smoke run read and all checks passing before the real run |
| Open model | arrival rate executor (or oha `-q --latency-correction`, vegeta `-rate`) used for latency |
| Thresholds | requirement encoded as k6 thresholds; CI uses the exit code |
| Validity | `dropped_iterations` threshold; achieved rate equals target; generator not saturated |
| Content checks | checks assert content, and a threshold on `checks` exists |
| Data | many users and ids; tokens prepared before the run; realistic data volume |
| Supabase | user JWT path tested (not service role); pooler limits and auth rate limits considered; `pg_stat_statements` read |
| Over time | results inspected as a time series, not only totals |
| Limiter | named with evidence |
| Report | `performance.md` section 8 template filled; raw summary kept |
