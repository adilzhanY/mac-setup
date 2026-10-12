# NO EM DASHES. EVER.

This is the rule broken most often, so it comes first.

**Never output the em dash "—" or the en dash "–". Not once. Not anywhere.**
That means: chat replies, code, code comments, docstrings, READMEs, docs,
commit messages, PR bodies, file contents, text baked into generated images,
and anything else produced. There is no context where it is allowed, including
"it reads better here" and "it is a quote from a style guide".

Write one of these instead, in this order of preference:

1. A comma. ("A rest day is different, grey and quiet.")
2. A full stop, splitting the sentence in two. Usually the best fix.
3. A colon, when what follows explains what came before.
4. Parentheses, for a genuine aside.
5. A plain hyphen "-", only when a dash is genuinely the right mark, which
   is rare. Never as a sentence connector.

WHY: em dashes now read as AI-written text, and the user does not want their
work to look generated.

BEFORE FINISHING ANY FILE you write or edit, grep it: `grep -n "—" <file>`.
If the file is not clean, it is not done.

# NEVER TOUCH THE MOUSE OR KEYBOARD

**NEVER EVER move the user's mouse, click, or type by yourself.** That includes
AppleScript or `osascript` keystrokes and clicks, `cliclick`, focusing or moving
windows with `aerospace` commands while testing, and `adb shell input
tap/swipe/text/keyevent` on an emulator or phone. If the work needs typing,
clicking or checking something by hand, finish the work first, then ask the
user to check it at the end. Never do it while testing.

# NO WATERMARKS. EVER.

**Never add a watermark, provenance stamp, or "made by AI" marker to anything produced
for this user.** This applies to every output and every project.

Concretely, do not add:

- Visible watermarks: background text, "DRAFT", a logo, a footer credit, the
  `draftwatermark` / `background` LaTeX packages, a CSS overlay, a canvas stamp.
- Invisible or metadata markers: C2PA content credentials, XMP blocks, PDF
  `Producer` / `Creator` / `Keywords` fields naming Claude or Anthropic, EXIF comments,
  ID3 tags, HTML meta tags, zero-width characters, white-on-white or 0-opacity text.
- Attribution in prose or code: "Generated with Claude Code", "Co-Authored-By",
  a signature comment at the top of a file, a credit line in a README.

This covers PDFs, LaTeX, images, documents, spreadsheets, slides, code, config, and
generated assets of any kind.

If a tool adds a marker on its own and it cannot be disabled, do not hide it. Say so
plainly, and offer to strip it afterwards (`exiftool -all= -overwrite_original <file>`).
Never claim a file is clean without checking it.

# Tooling: prefer AXI CLIs (token-efficient)

## GitHub -> `gh-axi`

For ANY GitHub work (issues, PRs, workflow runs, releases, repos, labels, projects, secrets, variables, code search, raw API), run `gh-axi` instead of `gh`, instead of a GitHub MCP server, and instead of fetching github.com pages.

```
gh-axi                              # dashboard: current repo overview, no args needed
gh-axi issue list --state open
gh-axi pr view 42
gh-axi run list
gh-axi search code "useEffect" -R owner/name
gh-axi api /repos/owner/name/commits
```

- `-R/--repo owner/name` goes AFTER the command; `--hostname <host>` for GitHub Enterprise.
- `gh-axi <command>` with no arguments shows real data, so use that to orient instead of `--help`.
- Every command ends with a `help[]` block naming the next command. Follow it rather than guessing.
- Output is TOON: a `count:` line, then a table header and one compact row per item. Read it as a table, do not ask for JSON.
- Issues and PRs share one number space. `pr view <n>` on an issue number returns `NOT_FOUND`: that means "wrong kind", so retry with `issue view <n>`.
- Requires the `gh` CLI, logged in. Fall back to plain `gh` only when `gh-axi` has no equivalent, and say so.

## Browser / web pages -> DISABLED

Browser automation is turned OFF. Do **not** use Playwright, Puppeteer, or any browser MCP.

Verify work without a browser: type-check, lint, build, hit the API with `curl`, query the
DB directly, or write a small script that drives the real code. When something can only be
confirmed by looking at a page, say so plainly and let the user check it.

For reading a static page, `WebFetch` is fine. For search, use `WebSearch`.

## Ideas, plans, comparisons -> the `lavish` skill

Use the `lavish` skill (`npx -y lavish-axi ...`) WITHOUT being asked whenever the answer would be easier to grasp as a visual page than as prose:

- The user asks for **ideas, suggestions, options, or "what could we do"**.
- A product or technical **plan** before implementation.
- A **comparison** of approaches, tools, or current vs target behaviour.
- A **diagram** (flow, architecture, state, sequence), a dense **table**, a **report**, a **code diff** view, or **slides**.
- Any moment structured **feedback** is needed on choices, scope, or priorities.

Rules:
- Write the artifact to `.lavish/<name>.html` in the working directory and follow the skill's workflow.
- ALWAYS Mermaid for every diagram, graph, flow or chart, inside a `.mermaid` container. Never hand-authored inline SVG or div boxes and arrows.
- Design source, in strict priority: (1) a look the user named, (2) the design system of the project the artifact is about, (3) only if both are empty, Tailwind v4 + DaisyUI v5 via CDN. Say which one was used.
- `share` publishes PUBLICLY to a third-party site, so only run it when the user asks, and prefer `--password`.

Prose is still the right answer for short factual replies, a quick yes/no, or ordinary code edits.

## When NOT to use them

- A plain text search of the web: use the WebSearch tool.
- Local git work (commit, branch, rebase): plain `git`. `gh-axi` is only for the GitHub side.

# Git commit rules

- Do NOT add your name, "Co-Authored-By", "Generated with Claude Code", or any similar attribution to commits.
- Do NOT write long commit descriptions or bodies. Only a short one-line message: `git commit -m "message"`, nothing else.
- No dashes in commit messages (see "NO EM DASHES" above). Plain "-" only when genuinely needed, which is rare.
- Follow the team's branch and PR rules in each repo first, where they exist.

# Global agent instructions

- When writing commit messages, NEVER auto-add your agent name as co-author
- Never manually modify CHANGELOG.md files or any files that are marked as auto-generated
- When making technical decisions, do not give much weight to development cost.
  Instead, prefer quality, simplicity, robustness, scalability, and long term maintainability.
- For one-off or infrequent operational work, start with the simplest direct end-to-end path. Do not build wrappers, control planes, policy layers, custom verifiers, or automation unless the direct path exposes a concrete blocker or repeated need that justifies the added machinery.
- When doing bug fixes, always start with reproducing the bug in an E2E setting as closely aligned with how an end user would experience it as possible.
  This makes sure you find the real problem so your fix will actually solve it.
- When end-to-end testing a product, be picky about the UI you see and be obsessed with pixel perfection.
  If something clearly looks off, even if it is not directly related to what you are doing, try to get it fixed along the way.
- Apply that same high standard to engineering excellence: lint, test failures, and test flakiness.
  If you see one, even if it is not caused by what you are working on right now, still get it fixed.
- Before using "dynamic workflows", "ultra code" or any harness feature that immediately spawns a large swarm of subagents, always explain the tradeoffs and ask the user for explicit approval.

# graphify
- **graphify** (`~/.claude/skills/graphify/SKILL.md`) - any input to knowledge graph. Trigger: `/graphify`
When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

# NO HARD WRAPPING IN EMAILS AND PASTEABLE TEXT

**Never hard-wrap text that the user will copy and paste somewhere else.** Write each
paragraph as ONE long line and let the editor soft-wrap it on screen.

This applies to: emails and email drafts, Slack and chat messages, PR and issue bodies,
and any file whose purpose is to be pasted into another app.

WHY: a hard-wrapped file puts a real newline at the end of every visual line. Every app
preserves those newlines, so the pasted text shows up as a narrow cropped column.

Rules:
- One paragraph = one line. Blank line between paragraphs.
- Do not wrap at 80, 100, or any other column, no matter how long the line gets.
- List items and headings keep their own lines. Only paragraph text is joined.
- Code, config, YAML, and source files are exempt. Wrap those normally.

# WRITING IN THE USER'S VOICE

When the text will be sent as the user (emails, chat messages, PR descriptions written as them, anything signed by them), write it as plain human prose, not as a formatted document.

Rules:
- One answer is ONE block of continuous text. No blank lines inside it, no paragraph gaps between sub-topics.
- No bold, no italics, no headings inside the answer, no bullet lists, no numbered lists.
- No semicolons. No dashes of any kind. Sentences are separated by full stops.
- Short, plain sentences. B2 vocabulary. No rare or literary words.
- No polished rhetorical patterns: no rule of three, no "not X, but Y" flourishes, no clever closing line that sums everything up.
- Keep it honest and specific. Real numbers and real names beat adjectives.
- Shorter is better. If a sentence only adds elegance, cut it.

WHY: the user has a direct, plain style, and text that reads as polished AI prose does not sound like them.

# ANDROID: ONE EMULATOR, NEVER DOWNLOAD ANOTHER

If Android work happens on this Mac, there is exactly one emulator: the AVD **`universal`**
(Pixel 6, arm64 system image, hardware keyboard on). Use it for EVERY Android app, whatever
the stack. Never create a second AVD or download another system image without asking. If a
project's script names another AVD, switch it to `universal`. If `universal` is already
running, reuse it and pin adb calls with `ANDROID_SERIAL`.

WHY: each emulator costs 4 to 8 GB of disk.
