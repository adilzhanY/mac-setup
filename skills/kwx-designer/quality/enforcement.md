# Enforcement: making the gate permanent

The quality gate says it is permanent, but today it reaches an agent only when the skill triggers and the agent reads SKILL.md. A `/clear`, a compaction or a freshly spawned subagent drops it. This file is the design for hooks that bring it back every time, adapted from how the ponytail plugin keeps its rules alive (SessionStart plus SubagentStart hooks, a marker line, fail open everywhere). The pieces are built (`scripts/gate_hook.py`, `scripts/check_skill.py`); **the hooks are not wired yet**, section 6 has the snippet.

## Contents

1. What breaks the gate today
2. The design
3. Rules for the hook
4. Rules for any future trigger
5. Keeping the copies in sync
6. Switching it on
7. Verifying it works

---

## 1. What breaks the gate today

- **Compaction and `/clear`.** A rule read once is gone the first time the context is compacted.
- **Subagents start blank.** SessionStart context never reaches a spawned agent. The ui-designer agent gets the gate only because its prompt says "read SKILL.md".
- **Skipped skill loads.** A small "one line style change" often never triggers the skill.

## 2. The design

| Event | Matcher | What is injected | Size |
|---|---|---|---|
| SessionStart | `startup\|resume\|clear\|compact\|fork` | Marker line, a pointer to the gate, the headlines of the 10 critical rules | about 700 characters |
| SubagentStart | `ui-designer` | Marker line, the full critical rules from SKILL.md, every `[critical]` row of `quality-gate.md`, the gate path, the mistakes library path | about 3,600 characters |

- Re-inject on every SessionStart source, not only `startup`, so the rules return after every `/clear`, every compaction and in a forked session.
- Inject the compact version, not the manual. The full gate is about 16 KB; the critical rules plus the `[critical]` rows are what must never be missed, and they point to the full file.
- Build the injected text from the files at run time (`gate_hook.py` parses SKILL.md and the gate table). A pasted copy drifts the first time a rule is edited.
- Scope the subagent injection to the agents that build UI, so Explore and backend agents do not pay for it.

## 3. Rules for the hook

1. **Marker line first.** Every injection starts with `KWX GATE ACTIVE`. A test, a reviewer or another hook can check for it, and the model can be asked to quote it (section 7).
2. **Use the `hookSpecificOutput` form:** `{"hookSpecificOutput": {"hookEventName": "SubagentStart", "additionalContext": "..."}}`. Raw stdout from a SubagentStart hook is dropped.
3. **Fail open.** A missing file, a bad payload or an exception still injects the short inline fallback; the script always exits 0 and never blocks a turn or a tool call. A frozen session costs more than a missed reminder.
4. **Doubt means inject.** A missing or empty `agent_type` gets the gate; only a known other agent type is skipped. Scoping must never silently drop the rules.
5. **Never echo file text from a project into the prompt.** The hook reads only the skill's own files and passes the mistakes library as a path, not its contents.
6. **Stay inside a budget.** The script caps the text at 9,000 characters and truncates with a pointer to the gate file.
7. **No gate levels.** There is no "lite gate". If depth ever varies, vary depth, never whether the gate runs; a level that skips it becomes the way to skip it.
8. **No blocking hook.** A Stop hook that refuses to finish is a different, riskier design. If one is ever added, it fails open and explains itself in its message.

## 4. Rules for any future trigger

For a possible UserPromptSubmit reminder on UI prompts (not built):

- Stay silent on ordinary prompts. A reminder on every turn trains the reader to ignore it.
- Match a trigger only on whole words, and test it against near misses. Ponytail's off switch once matched inside "add a normal mode toggle" and turned itself off mid task; it now fires only when the whole message is the command.
- A one shot command (a critique run) must not latch as a session mode.
- Offer any setup step at most once; repeating it every session turns a hint into a nag.

## 5. Keeping the copies in sync

The same rules live in several places: SKILL.md, `quality/quality-gate.md`, the ui-designer agent prompt (`~/.claude/agents/ui-designer.md`) and the user's CLAUDE.md.

- One owner per rule. The others point to it instead of restating it. The ui-designer prompt reads SKILL.md rather than copying it; keep it that way.
- Where a copy cannot be avoided, pin its load bearing phrases. `scripts/check_skill.py` fails when "Text never shrinks", "One primary action per view" or a `[critical]` gate id disappears, which is the reminder to update every copy.
- Test documented commands by running them, not by comparing copies: `check_skill.py` takes the emoji and palette greps out of `quality-gate.md` section 14 and runs them on lines that must hit and lines that must not. A copied regex only tests the copy.
- Run `python3 scripts/check_skill.py` after every edit to the skill. It could later run from `arch-config-push` or a git pre-commit hook (not wired).

## 6. Switching it on

On the author's machine these hooks are wired since 2026-10-30. On a new machine, merge this into the `hooks` object of `~/.claude/settings.json`. Append the SessionStart entry to the existing SessionStart array (it already holds the herdr hook); do not replace that array.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact|fork",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/kwx-designer/scripts/gate_hook.py --event SessionStart",
            "timeout": 5
          }
        ]
      }
    ],
    "SubagentStart": [
      {
        "matcher": "ui-designer",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/kwx-designer/scripts/gate_hook.py --event SubagentStart",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

The SubagentStart matcher is a regex on the agent type, and `agent_type` is in the hook input (Claude Code hooks docs, read 2026-10-29). The script also checks `agent_type` itself (`KWX_GATE_AGENTS`, default `ui-designer`, comma separated, case insensitive), so the scoping holds even if a matcher is ignored. Before merging, run `python3 scripts/gate_hook.py --selftest`.

## 7. Verifying it works

- **Execution is not delivery.** A hook that ran may still have printed the wrong shape. After wiring, start a ui-designer agent and ask it to quote the first line of its injected context. The answer must be `KWX GATE ACTIVE (kwx-designer, SubagentStart)`, a string that exists nowhere else.
- **Delivery is not compliance.** A delivered gate still has to change behaviour. That needs the paired runs in `evals/method.md`.
- Keep a small verification record: step, Claude Code version, result, date. Mark open steps "not yet run" instead of dropping them.

| Step | Result | Date |
|---|---|---|
| `gate_hook.py --selftest` | 22 of 22 pass | 2026-10-29 |
| Hooks merged into settings.json | not yet run | |
| ui-designer quotes the marker line | not yet run | |
| SessionStart text survives `/compact` | not yet run | |
