# GitLab.com database outage postmortem, 31 January 2017

- Legal URL: https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/
- Read in full (via fetch) for kwx-developer data topic, 2026-10-30.

## What happened

- About 17:20 UTC an engineer took an LVM snapshot of production into staging (pgpool testing). About 19:00 load spiked (spam plus a background job hard deleting an employee account wrongly flagged as abuse).
- About 23:00 replication lagged; the primary had already removed WAL segments the secondary needed, and WAL archiving was off, so the secondary had to be rebuilt. `pg_basebackup` hung silently; `max_wal_senders` raised 3 to 32 prevented a restart, fixed by lowering `max_connections` 8000 to 2000.
- About 23:30, while resetting the secondary, an engineer wiped the data directory on the primary. Stopped within seconds, about 300 GB already deleted.
- Recovery from a 6 hour old LVM snapshot on staging; copying over slow Azure disks (about 60 Mbps) took about 18 hours. Database restored to 17:20 UTC state. Webhooks restored separately. Sequences bumped by 100,000 so new ids never reuse lost ones.
- Loss: about 6 hours of database changes, roughly 5,000 projects, 5,000 comments, 700 users. Git repositories and wikis unaffected.

## Why every safety net failed

1. Daily `pg_dump` to S3: bucket empty. `pg_dump` 9.2 ran against PostgreSQL 9.6 (job ran on an app server without a data dir, so the tooling defaulted to 9.2). Failure emails rejected by DMARC.
2. Azure disk snapshots: enabled for NFS servers, not database servers. Cross account restores could take days.
3. LVM snapshots: existed for staging refresh, not designed for disaster recovery; one 24 h old, one 6 h old by luck.
4. Replication: secondary wiped during rebuild; primary wiped by mistake.
5. Root causes: no owner for backups, restores never tested, failures not monitored.

## Lessons used in the skill

- A backup is only proven by an automated, scheduled restore test (#1102 in their list).
- Monitor that backups succeeded (Prometheus, #1095), not that failure mail arrived.
- PITR with continuous WAL archiving (#1097), hourly snapshots (#1098), snapshots for database servers (#1099).
- An owner for data durability (#1163).
- Distinguish production from staging in shell prompts (#1094).
- Stop hard deleting users flagged for spam (soft handling of abuse removals).
- Principle: aim for recovery, not for blocking commands; practise recovery so mistakes are cheap.

Used in: `data/backups-and-recovery.md` sections 1, 10, 11, 12.
