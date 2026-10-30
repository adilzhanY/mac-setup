# Backups and recovery

How to back up databases and files so that a restore actually works, and how to prove it on a schedule. Sources: GitLab's 31 January 2017 database outage postmortem (read in full), PostgreSQL docs (continuous archiving and PITR, pg_dump), SQLite docs (backup API, VACUUM INTO, WAL), Litestream docs, Supabase backup docs, GDPR Articles 12 and 20.

## Contents

1. What GitLab 2017 teaches
2. Targets first: RPO, RTO, retention
3. The 3 2 1 rule, extended
4. Postgres: logical, physical, PITR
5. Managed Postgres (Supabase, Neon, RDS)
6. SQLite: backup API, VACUUM INTO, Litestream
7. Files and object storage
8. Encryption and keys
9. Retention and deletion
10. Monitoring backups
11. The restore test (set this up)
12. Before a destructive operation
13. Exporting user data
14. Checks

## 1. What GitLab 2017 teaches

On 31 January 2017 an engineer, working late to repair replication, ran `rm -rf` on the primary's data directory instead of the secondary's. About 300 GB was gone in seconds. GitLab had five protection mechanisms and none worked:

- **Daily pg_dump to S3**: the bucket was empty. The job ran `pg_dump` 9.2 against a 9.6 server (it ran on a host without a data directory, so the tooling picked the old binary), and it failed every time. The failure emails were rejected by DMARC, so nobody saw them.
- **Azure disk snapshots**: enabled for the NFS servers, not for the database servers.
- **LVM snapshots**: existed only to refresh staging; one was 6 hours old by luck (taken manually that afternoon).
- **Replication**: the secondary had just been wiped as part of the repair; replication had broken because WAL segments were removed before the secondary consumed them (no WAL archiving).
- **Restore**: copying the 6 hour old snapshot from staging took about 18 hours because staging used slow disks (about 60 Mbps).

Result: 18 hours down, about 6 hours of data lost (roughly 5,000 projects, 5,000 comments, 700 users). Root cause in their own words: no recent usable backup, backup failures went unnoticed, and nobody owned testing restores.

Lessons that become rules here:

1. A backup job that has not been restored is untested code. Restore automatically, on a schedule (section 11).
2. Alert on backup success missing, not on failure email arriving (section 10). Silence must page someone.
3. The backup tool version must be at least the server's major version. Pin it and check it in the job.
4. Know where every backup lives and how long a full restore takes from there, including copy time. Measure it.
5. Continuous WAL archiving (PITR) for any production Postgres you run yourself.
6. One named owner for data durability.
7. Make prod and non prod shells look different (prompt colour, hostname in prompt). The fix is recovery, not banning `rm`.
8. After restoring, bump sequences past any id the lost period might have issued (GitLab added 100,000), so external references to lost rows never point at new rows.

## 2. Targets first

Write these down per database before choosing tools:

- **RPO** (recovery point objective): how much data you can lose. Nightly dump = up to 24 h. PITR = seconds to minutes. Litestream = about 1 s.
- **RTO** (recovery time objective): how long you can be down. Measure the real restore time (download plus restore plus index build), never guess.
- **Retention**: how far back you can go. Corruption or a bad migration is often noticed days later, so 7 days is a minimum; 30 days plus monthly copies for a year is a common default (subject to deletion law, section 9).

## 3. The 3 2 1 rule, extended

- **3** copies of the data (production plus 2 backups).
- **2** different kinds of storage or providers (the database disk and object storage; or two clouds).
- **1** copy off site (another region and another account).
- Plus **1 immutable or offline** copy: object lock (S3 Object Lock in compliance mode, Backblaze B2 object lock), or an append only key for restic/borg. Ransomware and a compromised production credential delete reachable backups first. Production credentials must not be able to delete or overwrite backups.
- Plus **0 errors** in the last restore test.

A replica is not a backup: `DROP TABLE` and a bad `UPDATE` replicate in milliseconds. A snapshot on the same disk or the same cloud account is not off site.

## 4. Postgres: logical, physical, PITR

| Method | What | RPO | Restore granularity | Use for |
|---|---|---|---|---|
| `pg_dump -Fc` / `-Fd -j N` | logical SQL dump of one database, consistent snapshot, ACCESS SHARE locks only | time since last dump | one table or the whole DB; restores into newer major versions | second line backup, migrations between versions, per table recovery, small DBs |
| `pg_dumpall --globals-only` | roles, tablespaces (pg_dump omits them) | | | always alongside pg_dump |
| `pg_basebackup` | physical copy of the whole cluster | time since backup | whole cluster only, same major version | base for PITR, new replicas |
| Base backup plus WAL archiving (PITR) | replay WAL to any moment | seconds | whole cluster, any second after the base backup | primary backup for self hosted production |

- Self hosted production: use pgBackRest or WAL-G (they handle base backups, WAL archiving, compression, encryption, retention and verification). Do not hand roll `archive_command` with `cp` unless you follow the docs exactly: it must refuse to overwrite an existing file and return zero only on success.
- If archiving fails, WAL piles up in `pg_wal` until the disk fills and Postgres stops (PANIC). Alert on `pg_stat_archiver.failed_count` growing and on `last_archived_time` age.
- `pg_dump` refuses to dump a newer major server. Use the client binary matching the server or newer, and log `pg_dump --version` in the job.
- `pg_dump` holds a long transaction for its duration: it delays VACUUM and blocks DDL (migrations wait behind it). Run it on a replica or off peak, with `--lock-wait-timeout`.
- Keep pg_dump as a second, independent line even with PITR: it survives physical corruption that replays faithfully, and it lets you restore one table.

```bash
pg_dump --version
pg_dump -Fc --no-owner --lock-wait-timeout=60s -d "$DATABASE_URL" -f "db-$(date -u +%Y%m%dT%H%MZ).dump"
pg_dumpall --globals-only --no-role-passwords -d "$ADMIN_URL" > globals.sql
pg_restore -l db-*.dump > /dev/null   # fails if the archive is truncated or corrupt
```

## 5. Managed Postgres

- Supabase: daily backups on paid plans (Pro 7 days, Team 14, Enterprise up to 30); PITR is a paid add on (to the second, worst case RPO about 2 minutes, 7/14/28 days). Free projects have no backups: run `supabase db dump` yourself. Storage bucket objects are not in database backups (only their metadata). Custom role passwords are not restored. Deleting a project deletes its backups.
- Every managed provider: backups live in the same account as the database. Deleting the project, a billing lapse, or a compromised account takes both. Keep an independent nightly `pg_dump` in storage under a different account, with object lock.
- Restoring in place overwrites the database and causes downtime. Prefer restoring to a new project or branch (Supabase "restore to new project", Neon branches, RDS restore to new instance), then copy back what you need.

## 6. SQLite

- Never `cp app.db` while the app is running: committed data may still be in `app.db-wal`, and a copy taken mid write is torn. Use one of:
  - `sqlite3 app.db ".backup 'backup.db'"` (online backup API; consistent; restarts if another connection writes during the copy, so it can starve under constant writes).
  - `sqlite3 app.db "VACUUM INTO 'backup-2026-10-30.db'"` (consistent snapshot, compacted, purges deleted content; target file must not exist; needs no exclusive lock). Default for nightly copies.
  - Litestream for continuous replication to S3 compatible storage: it takes over checkpointing, ships WAL pages about every second, snapshots daily by default, restores to a point in time with `litestream restore -o restored.db s3://bucket/app.db` (`-timestamp` to pick the moment, `-dry-run` to preview). Default retention is 24 hours; raise it. Do not run another tool that checkpoints the same database. Run one writer process.
- After every backup: `sqlite3 backup.db "PRAGMA integrity_check;"` must print `ok`.
- Mobile apps: the OS backup (iCloud, Android Auto Backup) may copy the files while open, or exclude them. Do not rely on it for synced data; for local only apps, offer an in app export (section 13) and checkpoint (`PRAGMA wal_checkpoint(TRUNCATE)`) before the OS backup window if you rely on it.

## 7. Files and object storage

- User uploads in S3/R2/Supabase Storage are not in the database backup. Turn on bucket versioning plus a lifecycle rule that keeps noncurrent versions for the retention period, and replicate to a second bucket in another account or region.
- Database rows that reference files must be restorable together with the files: after restoring the database to time T, files deleted after T must still exist. Versioning gives you that.
- Server files and configs: restic or borg with an append only or object locked repository, `restic check --read-data-subset=5%` weekly.

## 8. Encryption and keys

- Encrypt before upload, with a key the storage provider does not hold: `age` (public key on the server, private key offline), restic/borg/pgBackRest/WAL-G built in encryption, or gpg.
- The server that makes backups only needs the public key (age recipient). The private key lives in a password manager and a sealed offline copy. A backup whose key was on the lost server is lost.
- Test decryption in the restore test, with the key from where a human would get it in a disaster.
- Backups contain everything sensitive (password hashes, tokens, PII). Restrict who can read the bucket; log access.

```bash
pg_dump -Fc -d "$DATABASE_URL" | age -r "$AGE_RECIPIENT" > "db-$(date -u +%F).dump.age"
age -d -i ~/.config/age/backup.key db-2026-10-30.dump.age > db.dump
```

## 9. Retention and deletion

- Grandfather father son: keep 7 dailies, 4 weeklies, 12 monthlies (adjust to law and contract). Let the tool (restic `forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12`, pgBackRest `repo1-retention-full`, S3 lifecycle) delete old backups, never a hand written `rm`.
- Personal data in backups: GDPR erasure does not usually require rewriting backups, but restored data must not resurrect erased users. Keep a deletion log (user ids erased, with dates) outside the backup, and re-apply it after any restore. State the backup retention period in the privacy policy.
- Shorter retention is a feature for personal data: do not keep backups longer than you need them.

## 10. Monitoring backups

- Use a dead man's switch: the backup job pings a URL (healthchecks.io, Better Stack heartbeat, Uptime Kuma push, Cronitor) only after the backup and its verification succeed. No ping within the interval plus grace pages someone. This catches jobs that never run, which failure emails cannot.
- Also alert on: backup size dropping more than about 20% from the previous one, newest backup older than the interval, WAL archive lag, Litestream replica lag.
- A public or team dashboard listing every data store, its backup method, newest backup age and last restore test result (GitLab's commitment after 2017).

## 11. The restore test

Run weekly (daily for critical data) on a schedule, on a machine that is not production. It restores the newest backup into a throwaway database, checks it, and pings the monitor only on success.

```bash
#!/usr/bin/env bash
# restore-test.sh: restore the newest Postgres backup into a scratch container and verify it.
# Needs: docker, aws (or rclone), age, the age private key at $AGE_KEY, and $HEALTHCHECK_URL.
set -euo pipefail

BUCKET="${BUCKET:?}"                 # s3://my-backups/db/
PG_MAJOR="${PG_MAJOR:-17}"           # must match or exceed production's major version
WORK="$(mktemp -d)"
trap 'docker rm -f restore-test >/dev/null 2>&1 || true; rm -rf "$WORK"' EXIT

latest="$(aws s3 ls "$BUCKET" | sort | tail -n1 | awk '{print $4}')"
[ -n "$latest" ] || { echo "no backup found"; exit 1; }

# 1. Age of the newest backup: fail if older than 26 h (daily job plus grace)
ts="$(aws s3 ls "$BUCKET$latest" | awk '{print $1" "$2}')"
age_h=$(( ( $(date -u +%s) - $(date -u -d "$ts" +%s) ) / 3600 ))
[ "$age_h" -le 26 ] || { echo "newest backup is ${age_h}h old"; exit 1; }

# 2. Download and decrypt with the offline key
aws s3 cp "$BUCKET$latest" "$WORK/db.dump.age"
age -d -i "$AGE_KEY" "$WORK/db.dump.age" > "$WORK/db.dump"

# 3. Restore into a fresh Postgres
docker run -d --name restore-test -e POSTGRES_PASSWORD=x -v "$WORK:/work" "postgres:$PG_MAJOR" >/dev/null
until docker exec restore-test pg_isready -U postgres >/dev/null 2>&1; do sleep 1; done
start=$(date +%s)
docker exec restore-test pg_restore -U postgres -d postgres --no-owner --exit-on-error -j 4 /work/db.dump
echo "restore took $(( $(date +%s) - start ))s"

# 4. Sanity checks: edit to the app's real tables
q() { docker exec restore-test psql -U postgres -d postgres -tAc "$1"; }
users=$(q "select count(*) from users")
[ "$users" -gt "${MIN_USERS:-1}" ] || { echo "users table too small: $users"; exit 1; }
newest=$(q "select extract(epoch from now() - max(created_at))/3600 from orders")
awk -v h="$newest" 'BEGIN{exit !(h < 48)}' || { echo "newest order is ${newest}h old"; exit 1; }
q "select count(*) from pg_index where not indisvalid" | grep -qx 0

# 5. Report success only now
curl -fsS -m 10 --retry 3 "$HEALTHCHECK_URL" >/dev/null
echo "restore test passed: $latest"
```

- Schedule with a systemd timer, cron, or a CI scheduled workflow (GitHub Actions `schedule:`), with the restore host's credentials read only.
- For SQLite: download, decrypt, `sqlite3 restored.db "PRAGMA integrity_check;"` must print `ok`, then the same count and recency queries.
- For PITR: once a month, restore to a specific timestamp into a new instance (managed: "restore to new project"; pgBackRest: `--type=time --target=...`) and check a row written just before that time exists and one written just after does not.
- Record the restore duration each run; that is your measured RTO. Once a quarter a human runs the full disaster runbook from a clean laptop, using only the written docs.

## 12. Before a destructive operation

Any `DROP`, `TRUNCATE`, `DELETE` without a narrow WHERE, bulk `UPDATE`, data migration, or `rm` on a server:

1. Confirm the host and database (`select current_database(), inet_server_addr();`, `hostname`). GitLab's outage was the right command on the wrong host.
2. Take a fresh backup or snapshot of what you will touch (`pg_dump -Fc -t table`, `create table x_backup_20261030 as table x;`, a provider snapshot), and verify it exists.
3. Run it in a transaction when possible: `BEGIN; DELETE ...;` check the row count it reports against what you expected; then `COMMIT` or `ROLLBACK`.
4. Write the undo command before running the do command.
5. Agents: never run destructive commands against production data on your own. Prepare them, show them, and let the user run them.

## 13. Exporting user data

- Offer every user an export of their data in a structured, commonly used, machine readable format (JSON, CSV; not only PDF). GDPR Article 20 requires this for data the user provided when processing is based on consent or contract; Article 12(3) gives one month to respond (extendable by two months for complex cases).
- Build it as a background job that writes a zip (one JSON or CSV per entity, plus their uploaded files), stores it with a short lived signed URL, and emails or notifies the user. Do not build it synchronously in a request.
- Use the same queries the app uses for authorization (by `user_id` / tenant). Test that the export of user A contains nothing of user B.
- Include stable ids and ISO 8601 UTC timestamps so the export can be re-imported. A local first app should offer import of its own export format; that is its longevity guarantee.

## 14. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Restore test scheduled | job exists, last success younger than its interval | the healthcheck dashboard or `systemctl list-timers`, CI scheduled run history |
| Backup off site and immutable | a copy in another account with object lock or append only | bucket policy: `aws s3api get-object-lock-configuration --bucket ...` |
| Production cannot delete backups | delete denied | try `aws s3 rm` with the production role on a test object; expect AccessDenied |
| Tool version matches server | client major >= server major | the job logs `pg_dump --version` and `select version()` |
| WAL archiving healthy (self hosted) | `failed_count` not growing, last archived recent | `select * from pg_stat_archiver;` |
| No raw copy of a live SQLite file | none | `grep -rniE "cp .*\.(db\|sqlite)\b\|copyFile.*\.(db\|sqlite)" scripts/ src/` |
| SQLite backup integrity | `ok` | `sqlite3 backup.db "PRAGMA integrity_check;"` |
| Backups encrypted | ciphertext in the bucket | `head -c 32 file` shows the age header `age-encryption.org/v1`, not `PGDMP` or `SQLite format 3` |
| Storage files covered | bucket versioning on | `aws s3api get-bucket-versioning --bucket ...` returns `Enabled` |
| User export exists | endpoint or job present, tested for isolation | `grep -rniE "export" src/` plus a test with two users |
| Runbook | written restore steps with measured RTO | `docs/runbooks/restore.md` exists and has a date from the last drill |
