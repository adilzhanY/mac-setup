# Browser automation for agents

How an AI agent should look at and drive a web page. Two paths: when the user allows browser automation, use a headless browser with an isolated profile, act on the accessibility snapshot rather than on screenshots, read console and network errors, and record what you did. When the user does not allow it, verify everything you can without a browser (type checks, build output, `curl`, HTML parsing, API and database calls), and hand the user a short visual checklist. This file has the decision flow, the tool choice, the isolation rules, what to record, and a verified browserless smoke test script (`scripts/smoke_site.py` in this skill).

## Contents

1. Rules
2. Step 0: read the user's rules
3. When browsers are allowed: which tool
4. Isolation: profile, accounts, origins, the user's desktop
5. Accessibility snapshot or screenshot
6. Reading console and network errors
7. What to record
8. When browsers are not allowed: the verification ladder
9. The browserless smoke test
10. Handing over a visual checklist
11. Checks

## 1. Rules

1. **Read the user's instructions before the first browser action** (global and project `CLAUDE.md` or `AGENTS.md`, memory). If they turn browser automation off, do not launch Playwright, Puppeteer, Lighthouse, a browser MCP, chrome devtools tools or a browser extension yourself, not even headless. Evidence: house rule.
2. **Writing browser tests into a project is not running a browser.** You may always write Playwright tests and configs. Running them locally needs the user's explicit yes when automation is off; CI may run them. Evidence: house rule.
3. **When allowed, run headless with a fresh, isolated profile.** Never the user's real browser profile, never their logged in sessions, never extension mode that attaches to their open tabs. Evidence: moderate (Playwright MCP README: "Playwright MCP is not a security boundary").
4. **Never move the user's mouse, type into their apps, or inject input into their phone or emulator.** A headless browser in its own process is fine when automation is allowed; driving the user's desktop is not. Evidence: house rule.
5. **Act on the accessibility snapshot, not on pixels.** Snapshots give stable element references and cost fewer tokens; screenshots are for judging looks, and even then a person should confirm. Evidence: moderate (Playwright MCP README).
6. **Always read the console and the failed network requests** after loading a page and after each important action. Many bugs show only there. Evidence: opinion.
7. **Turn anything you find worth keeping into a test in the project.** An agent's browser session is gone when it ends; a Playwright test runs on every change. Evidence: opinion.
8. **Never claim a visual result you did not see.** If no browser ran, say so and hand over the checklist. Evidence: house rule.

## 2. Step 0: read the user's rules

```text
Read ~/.claude/CLAUDE.md (or the platform's global instructions), the project CLAUDE.md / AGENTS.md, memory files.
 |
 |-- Browser automation is off ------------------> section 8 (browserless) + section 10 (checklist)
 |      (you may still write tests; running them locally needs the user's yes; CI may run them)
 |
 |-- Allowed, with conditions (only headless, only a test account, only localhost)
 |                                     ------------> follow the conditions exactly, then sections 3 to 7
 |
 |-- Allowed ------------------------------------> sections 3 to 7
 |
 |-- Not mentioned ------------------------------> ask once: "May I run a headless browser with a fresh profile
                                                     against localhost to check this?" Then follow the answer.
```

Also check: rules about the mouse and keyboard, about emulators and phones, about which workspace or monitor test windows may appear on, about network access, and about secrets. Rules written for one user may be stricter than this file; the stricter rule wins.

## 3. When browsers are allowed: which tool

| Need | Tool | Why |
|---|---|---|
| A check that should keep running after today | **A Playwright test in the project** (`npx playwright test e2e/x.spec.ts --project=chromium`) | Repeatable, reviewed, runs in CI. The best output of any browser session |
| Look at a page, click through a flow, find elements, read errors, from a coding agent | **`playwright-cli`** (`npm install -g @playwright/cli@latest`, or `npx playwright cli`) | Headless by default, profile in memory by default, compact output. The Playwright docs position it for coding agents because it avoids loading large tool schemas and accessibility trees into context |
| Long exploratory loops that keep page state and reason over structure | **Playwright MCP** (`npx @playwright/mcp@latest --headless --isolated`) | Rich page introspection through `browser_snapshot`; heavier on tokens |
| Performance traces, CPU profiles, CDP level debugging in Chrome | **Chrome DevTools MCP** (`npx chrome-devtools-mcp@latest --headless --isolated`) | Performance insights, source mapped console stacks. Sends usage statistics to Google by default (opt out with `--no-usage-statistics`; it is off when `CI` is set) and may send trace URLs to CrUX (`--no-performance-crux`) |
| Lighthouse numbers | `npx @lhci/cli autorun` or a CI job | Repeated runs with budgets; see `performance-and-seo-checks.md` |
| The user's own Chrome with their logins (Claude in Chrome, MCP `--extension` mode, connecting to a running Chrome) | **Only when the user explicitly asks for it in this conversation** | It acts as the user, with their accounts and data |

`playwright-cli` commands (playwright.dev "Getting started with CLI"):

```bash
playwright-cli open http://localhost:3000        # headless; add --headed only if the user wants to watch
playwright-cli snapshot                          # elements with refs like e15
playwright-cli click e15                         # act by ref (role or CSS selectors also work)
playwright-cli console error                     # console messages at or above a level
playwright-cli requests                          # network requests since page load
playwright-cli screenshot --filename=home.png
playwright-cli close
```

Named sessions keep projects apart (`playwright-cli -s=myapp open ...`), `--persistent` saves a profile to disk (avoid it unless needed), and headless sessions close themselves after an idle hour.

Playwright MCP flags worth setting (checked with `npx @playwright/mcp@0.0.84 --help`, verified 2026-10-31): `--headless` (default is headed), `--isolated` (profile in memory; the default is a persistent profile under `~/.cache/ms-playwright/mcp-...`), `--storage-state <file>` (start logged in as a test account), `--allowed-origins` / `--blocked-origins`, `--block-service-workers`, `--output-dir`, `--viewport-size`, `--device`, `--console-level`, `--secrets <file>`, `--save-session`. Extra tool groups are opt in with `--caps` (for example `network`, `storage`, `vision`, `devtools`, `testing`).

## 4. Isolation: profile, accounts, origins, the user's desktop

- **Profile**: in memory (`--isolated`, or `playwright-cli` default). Never pass the user's real `--user-data-dir`. Never attach to the user's running browser.
- **Accounts**: test accounts only, created for testing, with credentials from environment variables or a secrets file the user set up. If a flow needs a real account, stop and ask.
- **Where**: localhost, a local Docker stack, or a preview deployment the user named. Not production, unless the user asks and the actions are read only.
- **Origins**: restrict with `--allowed-origins "http://localhost:3000;http://127.0.0.1:54321"` so a stray link does not take the session to the open web. The README says origin lists are not a security boundary; they reduce accidents only.
- **Side effects**: do not submit real payments, send real emails or messages, or post to real social accounts. Route those endpoints to stubs or use sandbox modes.
- **The user's screen**: headless browsers do not open windows. A headed browser can take focus and move the pointer on some desktops (tiling compositors warp the cursor to new windows). Do not run headed unless the user asks, and follow any rule about where test windows may appear.
- **Clean up**: close sessions (`playwright-cli close-all`), stop servers you started, delete temporary storage state files that contain tokens.

## 5. Accessibility snapshot or screenshot

| | Accessibility snapshot | Screenshot |
|---|---|---|
| What it is | The page's accessibility tree as text: roles, names, states, element refs | Pixels |
| Use for | Finding and acting on elements, checking structure, labels, headings, what a screen reader would get | Judging layout, colors, overlaps, visual polish |
| Stability | Deterministic for the same DOM | Varies with fonts, timing, GPU |
| Cost | Usually smaller | Image tokens, and a vision model's reading can be wrong |
| Playwright MCP says | `browser_snapshot`: "this is better than screenshot" | `browser_take_screenshot`: "You can't perform actions based on the screenshot, use browser_snapshot for actions" |

Practical rules:

- Navigate, then snapshot, then act by ref. Re-snapshot after each navigation or big change, since refs can go stale.
- A control that is missing from the snapshot, or has no name, is an a11y bug. Report it; do not fall back to clicking coordinates.
- Take a screenshot only to answer a visual question, save it to the output directory, and say in the report that it needs a human look. Do not judge "looks good" from your own reading of an image when the change is a design change.
- In tests, turn the snapshot into an assertion: `await expect(region).toMatchAriaSnapshot(...)` (see `playwright.md` section 2).

## 6. Reading console and network errors

After loading a page and after each important action, collect:

- **Console errors and warnings**: `playwright-cli console warning`, MCP `browser_console_messages`, in tests `page.on('console')` or `page.consoleMessages()` (1.56 and later).
- **Uncaught exceptions**: in tests `page.on('pageerror')` or `page.pageErrors()`.
- **Failed and slow requests**: `playwright-cli requests`, MCP `browser_network_requests`; in tests `page.on('requestfailed')` and responses with status 400 and above.

Triage:

| Finding | Usually means |
|---|---|
| Uncaught `TypeError` / `ReferenceError` | A real bug, often in a state the developer never hit |
| React hydration mismatch warning | Server and client render differ (dates, random ids, `window` checks in render). Real bug in Next.js apps |
| 4xx on your own `/api` | Wrong request, missing auth, or a missing route |
| 5xx on your own `/api` | Server bug: read the server log next |
| CORS error | Wrong origin or missing headers; often only in production config |
| 404 on a font, image, `og:image` | Broken asset path, often a base path or case sensitivity problem that only shows on Linux hosting |
| Mixed content warning | An `http://` asset on an `https://` page |
| CSP violation | The policy blocks something the page needs, or something injected |
| Third party noise (ads, extensions, analytics) | Note it, keep an allowlist, do not let it hide your own errors |

Then turn the important ones into a test assertion (the `failOnPageErrors` fixture in `playwright.md` section 10).

## 7. What to record

For every browser session, write down in the report (and in the bug report, if there is a bug):

1. Goal of the session and the user's permission (quote the rule or the user's yes).
2. Tool and versions: browser and engine, Playwright or MCP version, headless or headed, viewport, device preset, color scheme.
3. URL, commit or build id, and how the app was started (`next build && next start`, preview URL).
4. Steps as a numbered list, each with the element by role and name ("clicked button 'Save'"), not by ref id, so a person can repeat it.
5. Expected and actual result for each check.
6. Console errors, page errors and failed requests, copied as text.
7. Paths of saved artifacts: trace zip, screenshots, snapshot excerpts, HAR. Keep them in the scratchpad or an ignored output directory. Do not commit them.
8. What you did not check.

Redact tokens, cookies, session ids and personal data from everything you paste. Storage state files and traces contain cookies and request bodies; treat them as secrets.

## 8. When browsers are not allowed: the verification ladder

Go down this ladder as far as the change needs. Every step runs without a browser.

| Step | Command (examples) | Proves |
|---|---|---|
| 1. Types | `npx tsc --noEmit` | The code is consistent with itself |
| 2. Lint | `npx eslint .` (with `jsx-a11y`, `testing-library`, `playwright` plugins) | Common bugs and a11y mistakes in source |
| 3. Unit and component tests | `npx vitest run` (jsdom) | Behaviour of logic and components, forms, error states with MSW |
| 4. Build | `npx next build` (read the whole output: warnings, route list, static or dynamic markers, sizes if printed) | It compiles for production; which routes are static |
| 5. Start the production server in the background | `npx next start -p 3100` (or `python3 -m http.server 4173 --directory out` for a static export), then poll until ready: `until curl -sf -o /dev/null http://localhost:3100; do sleep 0.5; done` (use the agent harness's own wait mechanism if foreground sleep is not allowed) | The server boots |
| 6. Smoke test | `python3 -I ~/.claude/skills/kwx-tester/scripts/smoke_site.py http://localhost:3100 / /pricing/ /login` | Status codes, 404s, head tags, internal links and anchors, alt text, one h1 |
| 7. Content check | `grep -c "Pro plan" <(curl -s http://localhost:3100/pricing)` or parse the HTML for the text the spec promises | The server rendered HTML contains what the spec says |
| 8. API calls | `curl -s -X POST localhost:3100/api/projects -H 'content-type: application/json' -d '{"name":""}' -w '\n%{http_code}\n'` | Validation, status codes, auth (with and without a token) |
| 9. Database | `psql "$DATABASE_URL" -c "select ..."` or the Supabase CLI against the local stack | The action changed the right rows, RLS holds |
| 10. Static output checks | `npx html-validate --preset recommended,a11y "out/**/*.html"`, `npx linkinator ./out --recurse --check-fragments`, `npx size-limit` | Valid HTML, no broken links, bundle within budget |
| 11. Write the browser tests for CI | Playwright journeys, axe scans, screenshots | Someone with a browser (CI, or the user) will verify the rest |
| 12. Checklist for the user | Section 10 | The visual and interactive parts |
| 13. Stop the server you started | `kill %1` or the harness's task stop | Leaves the machine as you found it |

What the ladder cannot prove: layout, CSS, colors and contrast, focus visibility, animations, anything rendered only on the client (content fetched in `useEffect`, `dynamic(..., { ssr: false })`, canvas), real click and keyboard behaviour, browser specific bugs. Note that Next.js does server render Client Components on first load, so their initial HTML is visible to curl; only client side fetched or client only content is not.

## 9. The browserless smoke test

`scripts/smoke_site.py` in this skill is a standard library only Python script (no dependencies, no browser). For each listed path it checks: status 200 and `text/html`; `lang` on `<html>`; a non empty `<title>`; meta viewport; meta description; canonical; `og:title` and `og:image`; exactly one `<h1>`; `<img>` without `alt`; canonical or `og:image` pointing at localhost; every internal link returns 200; every `#anchor` has a matching `id`. Then `/robots.txt` exists and an unknown path returns 404 (no soft 404). It exits 1 and prints one `FAIL` line per problem.

```bash
python3 -I ~/.claude/skills/kwx-tester/scripts/smoke_site.py --selftest          # checks the script itself, offline
python3 -I ~/.claude/skills/kwx-tester/scripts/smoke_site.py http://localhost:3100 / /pricing/ /about/
```

Verified 2026-10-31: the self test passes, and against a fixture site served by `python3 -m http.server` it reported exactly the planted problems (missing alt, a 404 link, a missing anchor target, missing `lang`, viewport, description, canonical, Open Graph tags and two `h1` on the second page), and exited 1.

Limits, by design: it reads server HTML only (no JavaScript), checks internal links only (use lychee for external ones), and its head tag list suits public pages. For a logged in app page, pass a cookie with a small change or check those pages with API calls instead. Adapt the `need` dictionary to the project's spec (for example drop `og:image` for an internal tool), and say in the report that you did.

A shell only version for a quick look at one page:

```bash
URL=http://localhost:3100/pricing
curl -s -o /tmp/page.html -w 'status %{http_code}, %{content_type}, %{size_download} bytes, %{time_total}s\n' "$URL"
grep -oiE '<html[^>]*lang="[^"]+"' /tmp/page.html || echo "FAIL no lang"
grep -oiE '<title>[^<]+' /tmp/page.html || echo "FAIL no title"
echo "h1 count: $(grep -oi '<h1' /tmp/page.html | wc -l)"
grep -oiE '<img[^>]*>' /tmp/page.html | grep -vi 'alt=' && echo "FAIL img without alt"
```

## 10. Handing over a visual checklist

When no browser ran, end the report with a short, specific checklist. Rules for writing it:

- Only what the change could affect. Five to ten lines, not a generic QA list.
- Each line names the page or component, the state, and what "right" looks like, so the user can tick it in seconds.
- Include widths, theme and input type when they matter.
- Say which checks were already done without a browser, so the user does not repeat them.

Template:

```text
Not verified by me (browser automation is off). Please check on http://localhost:3100 (I left `next start` stopped; run `npm run build && npm run start`):

1. /pricing at phone width (about 360 px): the three plan cards stack, the "Pro" badge does not cover the price.
2. /pricing in dark mode: card borders visible, price text readable.
3. Click "Choose Pro": the checkout dialog opens, focus is on the email field, Escape closes it and focus returns to the button.
4. Tab through the pricing page with the keyboard only: you can see where the focus is at every step.
5. Zoom to 200%: nothing is cut off and the "Choose" buttons are still reachable.

Already verified without a browser: types, lint, 42 unit and component tests, production build, smoke test of 6 pages (status, head tags, links), HTML validation, API returns 400 on an empty plan id.
```

## 11. Checks

- [ ] I read the user's rules and quoted the one that applies (or the user's yes) in the report.
- [ ] If browsers were off: I did not launch any browser, browser MCP, Lighthouse or devtools tool, and I did not run Playwright locally without the user's yes.
- [ ] If browsers were on: headless, isolated profile, test accounts, local or named preview URL, origins restricted, no real payments or messages.
- [ ] I acted on accessibility snapshots, not coordinates; missing or unnamed controls were reported as a11y bugs.
- [ ] Console errors, page errors and failed requests were read and listed.
- [ ] Session recorded: tool, versions, URL, build, steps by role and name, expected and actual, artifacts paths, secrets redacted.
- [ ] Findings worth keeping became Playwright or component tests in the project.
- [ ] The browserless ladder ran as far as the change needed, including the smoke test.
- [ ] The report ends with what was not verified and a short, specific checklist for the user.
- [ ] Servers and browser sessions I started are stopped.
