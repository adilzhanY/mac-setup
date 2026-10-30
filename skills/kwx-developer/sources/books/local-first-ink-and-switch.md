# Local-first software: you own your data, in spite of the cloud (Ink and Switch, 2019)

- Authors: Martin Kleppmann, Adam Wiggins, Peter van Hardenberg, Mark McGranaghan.
- Legal URL: https://www.inkandswitch.com/essay/local-first/ (free essay; also published at Onward! 2019)
- Read for kwx-developer data topic, 2026-10-30.

## What I read

The whole essay via fetch: the seven ideals, the survey of existing approaches, the CRDT findings from their prototypes (Trellis, Pixelpusher, PushPin), and the "what you can do today" recommendations.

## Key lessons

- Seven ideals: fast (no spinners), multi device, offline, collaboration, longevity, privacy and security by default, user ownership and control.
- Primary copy of the data lives on the device; servers are supporting peers (discovery, backup, burst compute), not the source of truth.
- CRDTs work: integrating Automerge was usually easy; default merge rules sufficed in all their prototypes; "conflicts are not as significant a problem as we feared".
- CRDT costs: history of every change grows without bound and is hard to truncate because a collaborator may return months later; concurrent edits to the same property still need a resolution policy; peer to peer networking (NAT traversal) is unsolved; users find "partly online" states hard to reason about.
- Practical advice: cache and prefetch so the UI never waits on the network; test offline by really turning the network off; export to standard formats (JSON, PDF) for longevity; tell users what stays on device; let users back up, duplicate and delete their documents.

Used in: `data/sqlite-and-local-first.md` sections 7 and 9.
