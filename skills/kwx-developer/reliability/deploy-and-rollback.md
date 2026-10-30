# Deploy and rollback

Most outages start with a change: a deploy, a config push, a migration, a flag flip, a data file. The goal of release engineering is that every change is small, reversible, exposed gradually, watched by automation, and undone without thinking. This file covers deploy strategies, rollback safety, database changes, feature flags, graceful shutdown, and mobile releases.

## Contents

1. The rules (D1 to D14)
2. Choosing a deploy strategy
3. Rollback safety: two phase changes
4. Database migrations: expand, migrate, contract
5. Feature flags
6. Graceful shutdown
7. Mobile (React Native / Expo) releases
8. Checks

## 1. The rules

**D1. Every change is reversible by one command, and rollback is the first response.** During an incident, roll back first, debug later. A rollback that needs a code change, a manual SQL script or a person who knows the system is not a rollback. Rollback also covers config, flags and data files, not only binaries.

**D2. Build once, deploy the same artifact everywhere.** The image or bundle tested in staging is the one promoted to production, identified by git SHA. No rebuild per environment; environment differences live in config. Builds are reproducible: lockfiles committed, `npm ci` / `cargo build --locked`, pinned base images (SRE book "Hermetic builds").

**D3. Small and frequent beats big and rare.** Frequent releases mean fewer changes per release, which makes testing and troubleshooting easier (SRE book ch. 8). One logical change per deploy where possible.

**D4. Config and data are deployed like code.** Config changes, feature flag rules, rule sets, ML feature files, quota policies: versioned, validated, staged and automatically rolled back like binaries. Cloudflare 2019 (a WAF regex pushed globally at once), Cloudflare 2025 (a bot feature file), Google Cloud June 2025 (a quota policy replicated globally in seconds) and CrowdStrike 2024 (a content file) were all global pushes of non-code changes that skipped the staged rollout code would get.

**D5. Expose gradually and watch automatically.** One box or canary first, then waves. Amazon: one box for at least 1 hour, then at most 33% of a region's capacity at a time, first region baked at least 12 hours (AWS "Automating safe, hands-off deployments"). Smaller teams: one canary instance or a 1 to 5% traffic slice for 15 to 60 minutes, comparing its error rate and latency against the rest.

**D6. Rollback is automatic on alarm.** The deploy watches the service's high severity alarms (error rate, latency, failing health checks, request count dropping to zero) and the canary scoped metrics, and rolls back without a human. Bake time includes a minimum number of requests seen, not only minutes (AWS: "wait for at least 100 requests to the Create API").

**D7. Old and new versions run side by side during every rolling deploy.** Every change must be safe when N and N+1 serve traffic at once and when N+1 is rolled back to N. Test exactly that (section 3).

**D8. Deploy when people are around.** Avoid late afternoon, Fridays, weekends and holidays for risky changes; issues may surface hours later (AWS). Emergency fixes still go through the pipeline, with shorter bake and more review, not around it.

**D9. Every running instance reports what it is.** Version (git SHA) in health responses, in log lines and in the crash reporter `release`. A change log of deploys and config pushes is the first place to look in an incident (SRE book: "check for recent changes and consider reverting them").

**D10. Database first, code second, cleanup last.** Schema changes ship before the code that needs them, and destructive changes (drop, rename, tighten) ship only after no running code uses the old shape (section 4).

**D11. Global data replication is a deploy.** Anything that propagates to every region or every client within seconds needs validation, staging and a kill switch. Google's June 2025 remediation: "data replication needs to be propagated incrementally with sufficient time to validate and detect issues."

**D12. New code paths ship dark behind a flag, default off.** Google's June 2025 outage: a new Service Control code path shipped without a feature flag; the region by region rollout never exercised it because it only ran when a specific policy existed. Remediation: "all changes to critical binaries to be feature flag protected and disabled by default." A rollout that does not execute the new code path proves nothing about it.

**D13. Kill switches for risky features exist before launch** and are tested. Cloudflare's 2019 recovery used a "global terminate" for the WAF; their 2025 remediation added more global kill switches. The kill switch must work when your own tools are down (Cloudflare 2019: staff could not log in to the control panel because their own Access product was down; Facebook 2021: internal tools depended on the DNS that was down).

**D14. Destructive operational commands have guardrails.** Tools that remove capacity, delete data or change routing: dry run by default, a limit on how much they can remove at once, a minimum capacity floor, and confirmation that names the target. AWS S3 2017 (a typo removed more servers than intended) led to removing capacity more slowly with a minimum floor. GitLab 2017 (`rm -rf` on the primary instead of the secondary) led to clearer host prompts.

## 2. Choosing a deploy strategy

| Strategy | How | Use when | Cost |
|---|---|---|---|
| Rolling | Replace instances in batches, waiting for readiness | Default for stateless services on Kubernetes, ECS, Fly, Render | Old and new coexist (D7). Rollback is another rolling deploy |
| Canary | A small slice (1 instance or 1 to 5% traffic) runs the new version, compared to the rest, then promote | Any service with enough traffic to compare error rates | Needs per version metrics and automated compare |
| Blue green | Two full environments, switch the router from blue to green; keep blue warm to switch back | Fast, near instant rollback; services with long startup | Double capacity during switch; shared database still needs D10; long lived connections must drain |
| Feature flag release | Code deployed dark, behavior turned on per cohort | Product features, risky logic changes | Flag debt (section 5) |
| Preview environments | One environment per PR | Web apps on Vercel, Netlify, Render | Not a production safety mechanism by itself |

Default: rolling deploy with readiness gating plus automatic rollback on alarm, and feature flags for anything user visible or risky. Add canary analysis when traffic is large enough that 1% gives a signal within an hour.

Canary metrics: start from the SLIs (error rate, latency of successful requests), at most about a dozen metrics, compared canary vs control at the same time, not before vs after (SRE Workbook ch. 16). Exclude 4xx from canary error rates unless the change is about them.

## 3. Rollback safety: two phase changes

The most common reason a rollback fails is a protocol or format change (AWS "Ensuring rollback safety during deployments"). If version N+1 writes data that version N cannot read, rolling back breaks reads of everything written in between. Even a changed constant can do it: raising a heartbeat interval from 5 s to 10 s makes old servers drop connections from new ones.

Split such a change into two deploys:

1. **Prepare**: the new version can read both old and new formats, still writes the old one. Safe to roll back.
2. **Activate** (after a bake period, often days): start writing the new format. Rolling back to Prepare is safe, because Prepare reads both.
3. **Cleanup** (only after a backfill rewrote all old data): remove the old reader.

Rules for serialized data (JSON in DB columns, queue messages, cache entries, files, API payloads):

- Use a standard format with schema evolution (JSON with optional fields, Protobuf). Never serialize language runtime objects directly.
- Readers tolerate and preserve unknown fields when they write back, so an old version does not wipe a new field.
- Version the serialized data and emit a metric of versions read and written.
- Roll forward readers before writers; roll back writers before readers.
- Test it: deploy N+1 to half the test fleet, then all, then roll back to N, exercising every API and background job in each stage (AWS upgrade/downgrade testing). A single instance test environment cannot catch these bugs because versions never coexist.

## 4. Database migrations: expand, migrate, contract

Parallel change (Fowler) applied to schemas. Never rename or drop in one step.

**Renaming a column `name` to `full_name`:**

1. Expand: add `full_name` (nullable). Deploy code that writes both and reads `name`.
2. Backfill `full_name` in batches.
3. Deploy code that reads `full_name` (still writes both).
4. Deploy code that stops writing `name`.
5. Contract: drop `name`, in a later release, after the rollback window.

Postgres specific rules (these are what take production down):

- Set `lock_timeout` (for example `SET lock_timeout = '5s'`) in every migration, and retry. A DDL waiting for a lock blocks every query queued behind it.
- `CREATE INDEX CONCURRENTLY` (outside a transaction) on any table with traffic. `DROP INDEX CONCURRENTLY` too.
- Add foreign keys and check constraints as `NOT VALID`, then `VALIDATE CONSTRAINT` in a separate statement (takes a weaker lock).
- `SET NOT NULL` on a big table: add a `CHECK (col IS NOT NULL) NOT VALID`, validate it, then `SET NOT NULL` (Postgres 12+ uses the validated check and skips the scan).
- Adding a column with a constant default is instant on Postgres 11+; a volatile default (`now()`, `gen_random_uuid()`) rewrites the table.
- Changing a column type usually rewrites the table and takes an exclusive lock: use expand and contract with a new column.
- Backfill in batches of a few thousand rows with a pause, outside the migration transaction, never `UPDATE big_table SET ...` in one statement.
- Primary keys and foreign keys are `bigint` (or uuid). GitHub (2021) and Heroku (2023) both had outages when an `int` id or a foreign key smaller than its referenced key overflowed at 2^31.
- After a major version upgrade or a blue green database switch, run `ANALYZE` before taking traffic (CircleCI 2025: the new database had no statistics and planned every query as a disk scan).
- Migrations run as a separate step before the new code rolls out, never on application startup from every instance at once.
- Every migration in a PR is reviewed for locks; use a linter (`squawk` for Postgres SQL files).

## 5. Feature flags

Categories (Hodgson, "Feature Toggles" on martinfowler.com), with different lifetimes:

| Type | Purpose | Lifetime | Rule |
|---|---|---|---|
| Release | Ship incomplete or risky code dark | Days to weeks | Remove after full rollout. Add the removal task when adding the flag |
| Ops / kill switch | Turn off an expensive or risky path under load | Long lived | Test both states; owner on call knows it exists |
| Experiment | A/B test | Until decision | Remove with the losing branch |
| Permission | Plans, beta users, internal users | Long lived | Is really authorization; keep it in the permission model |

Rules:

- **F1.** Flag evaluation has a safe default when the flag service is unreachable (usually the old behavior), and the SDK does not block startup on the flag service.
- **F2.** Tests run with the flag both on and off for any release flag (Hodgson: verify "both sides of a toggled feature").
- **F3.** Decision logic lives in one place (a toggle router), not `if (flags.x)` sprinkled through 30 files. Pass decisions in, so business code takes a boolean or a strategy.
- **F4.** Flags are inventory with a carrying cost. Every flag has an owner and an expiry date in its definition; CI fails or warns when a release flag is past expiry. Keep the count low.
- **F5.** Percentage rollouts use a stable hash of the user id, so a user does not flip between variants.
- **F6.** Flag changes are logged with who and when, and appear in the deploy change log (D9).
- **F7.** Never reuse a flag name for a different meaning. Knight Capital (2012) repurposed an old flag; one of eight servers missed the deploy, read the flag with its old meaning, ran dead "Power Peg" code unused since 2003, and the firm lost more than 460 million dollars in about 45 minutes (SEC order 34-70694, 2013). Delete dead code paths with their flag.

## 6. Graceful shutdown

On SIGTERM a service must stop taking new work, finish in-flight work, release resources and exit before the platform's kill timeout (Kubernetes default `terminationGracePeriodSeconds` is 30 s, then SIGKILL).

Order:

1. Mark not ready (readiness returns 503), so the load balancer stops sending new requests.
2. Wait a few seconds for endpoint removal to propagate (Kubernetes removes the pod from endpoints asynchronously; a `preStop` sleep of 5 to 10 s or an in-app delay covers it).
3. Stop accepting connections; close idle keep-alive connections; let in-flight requests finish.
4. Stop queue consumers from fetching; finish or release (nack) messages in progress.
5. Flush logs, traces, metrics and the crash reporter.
6. Close DB pools and other clients.
7. Exit 0. If any step exceeds the budget, exit 1 anyway, before SIGKILL.

```ts
let shuttingDown = false;
app.get("/readyz", (_req, res) => res.status(shuttingDown ? 503 : 200).send());

process.once("SIGTERM", async () => {
  shuttingDown = true;
  const hardStop = setTimeout(() => process.exit(1), 25_000).unref();
  await sleep(5_000);                       // let the load balancer notice
  server.close();                            // stop accepting, finish in-flight
  server.closeIdleConnections();             // Node 18.2+: drop idle keep-alive sockets
  await Promise.allSettled([worker.stop(), otelSdk.shutdown(), Sentry.close(2_000)]);
  await pool.end();
  clearTimeout(hardStop);
  process.exit(0);
});
```

```rust
let listener = tokio::net::TcpListener::bind(addr).await?;
axum::serve(listener, app).with_graceful_shutdown(shutdown_signal()).await?;
pool.close().await;

async fn shutdown_signal() {
    let ctrl_c = async { tokio::signal::ctrl_c().await.expect("install Ctrl+C handler") };
    let term = async {
        tokio::signal::unix::signal(tokio::signal::unix::SignalKind::terminate())
            .expect("install SIGTERM handler").recv().await;
    };
    tokio::select! { _ = ctrl_c => {}, _ = term => {} }
    // flip readiness here, then sleep a few seconds before returning
}
```

Container gotchas:

- Signals reach PID 1 only. `CMD ["npm", "start"]` and shell form `CMD npm start` may not forward SIGTERM to Node. Use exec form `CMD ["node", "dist/server.js"]`, or `--init` / `tini` as PID 1.
- A process running as PID 1 without its own SIGTERM handler ignores SIGTERM (Linux PID 1 has no default handler) and is SIGKILLed after the grace period.
- Long requests (uploads, streaming, WebSockets) need a plan: a max duration shorter than the grace period, or a client reconnect protocol.

## 7. Mobile (React Native / Expo) releases

Mobile releases cannot be rolled back on devices; old versions stay in the wild for months.

- **The API supports every app version still in use.** Backend changes are additive; old fields stay until usage of the old app versions is near zero (measure by app version header). Remove fields only behind a minimum supported version check.
- **Ship a minimum version gate** (the app asks the API for `minSupportedVersion` and shows an update screen) from the first release, because you cannot add it later to versions already shipped.
- **Staged rollouts in the stores**: Google Play percentage rollout (halt if crash rate rises), App Store phased release (7 day ramp, can pause).
- **Over the air updates** (EAS Update / expo-updates) are deploys: use channels and branches, roll out to a percentage, keep the previous update to roll back to (`eas update:rollback` or republish), and only ship JS compatible with the installed native runtime (`runtimeVersion` policy). Never use OTA to bypass store review for new functionality.
- **Crash free sessions** per release are the canary metric. Upload source maps / debug symbols per build so stacks are readable.
- Feature flags matter more on mobile than on the web, because they are the only fast rollback for code already on devices.

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| One artifact promoted | Production deploy uses the image tag / SHA tested in staging | Read the pipeline: build job once, deploy jobs take the artifact |
| Locked builds | Lockfile committed, CI uses `npm ci` / `pnpm install --frozen-lockfile` / `cargo build --locked` | `rg -n 'npm install\b|cargo build(?!.*--locked)' .github/workflows` (needs `rg -P`) |
| Pinned base images | `FROM` uses a version tag or digest, never `latest` | `rg -n '^FROM .*:latest|^FROM [^:@]+$' Dockerfile*` returns 0 |
| Version reported | Health endpoint and logs include git SHA | `curl -s .../readyz`; `rg -n 'GIT_SHA|COMMIT|release' src` |
| Auto rollback | Deploy config has health gating and rollback on alarm | k8s: `progressDeadlineSeconds`, readiness probe; Argo Rollouts / Flagger analysis; ECS circuit breaker `rollback: true` |
| Migrations lint | No locking DDL without safeguards | `squawk migrations/*.sql` in CI |
| lock_timeout in migrations | Every migration sets it or the runner does | `rg -L 'lock_timeout' migrations/` lists files missing it |
| Concurrent index creation | No `CREATE INDEX` without `CONCURRENTLY` on existing tables | `rg -n 'CREATE (UNIQUE )?INDEX (?!CONCURRENTLY)' -P migrations/` |
| No int primary keys | ids are bigint or uuid | `rg -n -i '\bserial\b|\bint(eger)?\b.*primary key|references' migrations/` and review types |
| Migrations not on app start | App boot does not run migrations in every replica | `rg -n 'migrate\(\)|runMigrations|sqlx::migrate!' src/main* src/server*` and read |
| Two phase for format changes | PRs that change a serialized format ship read-both first | Review checklist item; grep for version fields in serialized types |
| Flags have owner and expiry | Every flag definition has both | Read the flag registry file; CI script lists expired flags |
| Flags tested both ways | Tests set the flag on and off | `rg -n 'flag.*(true|false)|setFlag' tests src/**/*.test.*` |
| SIGTERM handled | Handler flips readiness, drains, exits under the grace period | `rg -n -A15 'SIGTERM' src`; run the container, `docker stop`, check logs for clean exit within 30 s |
| Exec form CMD | Node or binary is PID 1 or behind tini | `rg -n '^CMD' Dockerfile*` shows exec form JSON array with the binary, or `--init` used |
| Mobile min version gate | App checks min supported version on start | `rg -n -i 'minSupportedVersion|forceUpdate' app src` |
| OTA runtime pinned | `runtimeVersion` policy set | `rg -n 'runtimeVersion' app.json app.config.*` |
