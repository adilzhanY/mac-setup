#!/usr/bin/env python3
"""Claude Code hook that re-injects the kwx-designer quality gate.

SessionStart (startup, resume, clear, compact, fork): a short pointer plus the
headlines of the critical rules, so the main agent keeps them after /clear
and after compaction.
SubagentStart (ui-designer only): the full critical rules from SKILL.md plus
every [critical] row of quality/quality-gate.md, read at run time so the
injected text can never drift from the files.

Fails open: any error still prints a short inline fallback when it can, and
the script always exits 0. Standard library only.

Usage (from settings.json):
    python3 gate_hook.py --event SessionStart
    python3 gate_hook.py --event SubagentStart
    python3 gate_hook.py --selftest
"""

import json
import os
import re
import select
import subprocess
import sys
import tempfile

MARKER = "KWX GATE ACTIVE"
MAX_CHARS = 9000  # injected text budget; the full gate file is far larger
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Agent types that get the full gate. Case insensitive substring match, so an
# invalid value cannot crash the hook. Override with KWX_GATE_AGENTS="a,b".
DEFAULT_AGENTS = "ui-designer"
MISTAKES = os.path.expanduser("~/.claude/ui-designer/mistakes.md")

FALLBACK = (
    "Critical rules: intuitive beats clever; one primary action and one accent per view; "
    "hierarchy from type, weight, colour and space, not boxes; tokens before pixels; "
    "every action answers and every state exists (loading, empty, error, offline, limit); "
    "no AI slop (no emoji or symbol icons, no default purple gradients); honest psychology "
    "only; compute sizes and contrast instead of guessing, text never shrinks to fit; "
    "no em or en dashes. Run quality/quality-gate.md before calling any UI done."
)


def read_stdin(timeout=1.0):
    """Return the hook payload as a dict, or {} when stdin is empty, slow or not JSON."""
    try:
        if sys.stdin is None or sys.stdin.isatty():
            return {}
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if not ready:
            return {}
        raw = sys.stdin.read()
        raw = raw.lstrip("\ufeff")
        data = json.loads(raw) if raw.strip() else {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def critical_rules(skill_dir):
    """The numbered rules under '## Critical rules' in SKILL.md, joined per rule."""
    text = open(os.path.join(skill_dir, "SKILL.md"), encoding="utf-8").read()
    m = re.search(r"^## Critical rules[^\n]*\n(.*?)(?=^## )", text, re.S | re.M)
    if not m:
        raise ValueError("no Critical rules section in SKILL.md")
    rules, cur = [], None
    for line in m.group(1).splitlines():
        if re.match(r"^\d+\. ", line):
            if cur:
                rules.append(cur)
            cur = line.strip()
        elif cur and line.strip():
            cur += " " + line.strip()
    if cur:
        rules.append(cur)
    if not rules:
        raise ValueError("Critical rules section is empty")
    return rules


def headline(rule):
    m = re.match(r"^(\d+)\. \*\*(.+?)\*\*", rule)
    return f"{m.group(1)}. {m.group(2).rstrip('.')}" if m else rule[:90]


def critical_gate_rows(skill_dir):
    """Every '| X1 [critical] | check | pass | verify |' row of the quality gate."""
    text = open(os.path.join(skill_dir, "quality", "quality-gate.md"), encoding="utf-8").read()
    rows = []
    for line in text.splitlines():
        if line.startswith("|") and "[critical]" in line:
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
            if len(cells) >= 3:
                rid = cells[0].replace("[critical]", "").strip()
                rows.append(f"- {rid} {cells[1]}: {cells[2]}")
    if not rows:
        raise ValueError("no [critical] rows in quality-gate.md")
    return rows


def build_context(event, skill_dir=SKILL_DIR):
    """Text to inject. Always starts with the marker line, never raises."""
    head = f"{MARKER} (kwx-designer, {event})"
    gate = os.path.join(skill_dir, "quality", "quality-gate.md")
    try:
        rules = critical_rules(skill_dir)
        if event == "SubagentStart":
            parts = [
                head,
                "Follow kwx-designer for this UI work. Critical rules from SKILL.md:",
                *rules,
                "Critical items of the quality gate (each blocks shipping on its own):",
                *critical_gate_rows(skill_dir),
                f"Before reporting done run the whole gate: {gate}",
            ]
            if os.path.exists(MISTAKES):
                parts.append(f"Read the mistakes library in full before writing: {MISTAKES}")
        else:
            parts = [
                head,
                "UI work follows the kwx-designer skill and goes through the ui-designer agent where the user's rules say so.",
                f"No UI is done before {gate} passes. Critical rules: "
                + "; ".join(headline(r) for r in rules),
            ]
        text = "\n".join(parts)
    except Exception as exc:  # fail open: a read error never means "no rules"
        text = f"{head}\n{FALLBACK}\n(Built from the inline fallback: {type(exc).__name__}.)"
    if len(text) > MAX_CHARS:
        text = text[: MAX_CHARS - 40].rstrip() + "\n(truncated, read the gate file)"
    return text


def wanted(event, payload):
    """False only when we know for sure the gate is not for this agent."""
    if event != "SubagentStart":
        return True
    agent = payload.get("agent_type")
    if not isinstance(agent, str) or not agent.strip():
        return True  # unknown agent: inject rather than silently drop the gate
    names = [n.strip().lower() for n in os.environ.get("KWX_GATE_AGENTS", DEFAULT_AGENTS).split(",") if n.strip()]
    return not names or any(n in agent.lower() for n in names)


def output(event, payload, skill_dir=SKILL_DIR):
    """JSON string for stdout, or '' when nothing should be injected."""
    if not wanted(event, payload):
        return ""
    return json.dumps({
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": build_context(event, skill_dir),
        }
    })


def event_from(argv, payload):
    for i, a in enumerate(argv):
        if a == "--event" and i + 1 < len(argv):
            return argv[i + 1]
        if a.startswith("--event="):
            return a.split("=", 1)[1]
    ev = payload.get("hook_event_name")
    return ev if ev in ("SessionStart", "SubagentStart") else "SessionStart"


def main(argv):
    try:
        payload = read_stdin()
        event = event_from(argv, payload)
        out = output(event, payload)
        if out:
            sys.stdout.write(out + "\n")
    except Exception:
        try:
            ev = event_from(argv, {})
            sys.stdout.write(json.dumps({"hookSpecificOutput": {
                "hookEventName": ev, "additionalContext": f"{MARKER}\n{FALLBACK}"}}) + "\n")
        except Exception:
            pass
    return 0


def selftest():
    fails = []

    def check(name, cond):
        print(("PASS " if cond else "FAIL ") + name)
        if not cond:
            fails.append(name)

    # 1. Real skill files: both events, marker first, critical content present.
    for ev in ("SessionStart", "SubagentStart"):
        data = json.loads(output(ev, {"agent_type": "ui-designer"}))
        ctx = data["hookSpecificOutput"]["additionalContext"]
        check(f"{ev}: valid hookSpecificOutput JSON", data["hookSpecificOutput"]["hookEventName"] == ev)
        check(f"{ev}: marker is the first line", ctx.splitlines()[0].startswith(MARKER))
        check(f"{ev}: built from files, not the fallback", "inline fallback" not in ctx)
        check(f"{ev}: under the {MAX_CHARS} character budget", len(ctx) <= MAX_CHARS)
    sub = json.loads(output("SubagentStart", {"agent_type": "ui-designer"}))["hookSpecificOutput"]["additionalContext"]
    n_rules = len(critical_rules(SKILL_DIR))
    n_rows = len(critical_gate_rows(SKILL_DIR))
    check(f"SubagentStart: all {n_rules} critical rules present", all(r in sub for r in critical_rules(SKILL_DIR)))
    check(f"SubagentStart: all {n_rows} [critical] gate rows present", all(r in sub for r in critical_gate_rows(SKILL_DIR)))
    check("SubagentStart: gate row A1 present", "- A1 One obvious next step" in sub)
    start = json.loads(output("SessionStart", {}))["hookSpecificOutput"]["additionalContext"]
    check("SessionStart: short (under 2000 characters)", len(start) < 2000)

    # 2. Scoping: other agents get nothing, unknown agents still get the gate.
    check("SubagentStart: Explore agent gets nothing", output("SubagentStart", {"agent_type": "Explore"}) == "")
    check("SubagentStart: missing agent_type still injects", output("SubagentStart", {}) != "")
    check("SubagentStart: case insensitive match", output("SubagentStart", {"agent_type": "UI-Designer"}) != "")

    # 3. Missing skill files: fallback text, still valid JSON with the marker.
    with tempfile.TemporaryDirectory() as empty:
        ctx = json.loads(output("SubagentStart", {}, skill_dir=empty))["hookSpecificOutput"]["additionalContext"]
        check("missing files: fallback used", "inline fallback" in ctx and FALLBACK in ctx)
        check("missing files: marker still first", ctx.startswith(MARKER))

    # 4. As a real process, with good, bad and empty stdin: exit 0, JSON out.
    me = os.path.abspath(__file__)
    cases = {
        "good payload": (["--event", "SubagentStart"], '{"hook_event_name":"SubagentStart","agent_type":"ui-designer"}'),
        "malformed JSON": (["--event", "SessionStart"], "{not json"),
        "empty stdin": (["--event", "SessionStart"], ""),
        "BOM and no --event": ([], '\ufeff{"hook_event_name":"SubagentStart","agent_type":"ui-designer"}'),
    }
    for name, (args, stdin) in cases.items():
        p = subprocess.run([sys.executable, me, *args], input=stdin, capture_output=True, text=True, timeout=10)
        ok = p.returncode == 0 and p.stderr == ""
        try:
            ok = ok and json.loads(p.stdout)["hookSpecificOutput"]["additionalContext"].startswith(MARKER)
        except Exception:
            ok = False
        check(f"process, {name}: exit 0, clean stderr, marker JSON", ok)
    p = subprocess.run([sys.executable, me, "--event", "SubagentStart"], input='{"agent_type":"Explore"}',
                       capture_output=True, text=True, timeout=10)
    check("process, other agent: exit 0 and silent", p.returncode == 0 and p.stdout == "")

    print(f"\n{len(fails)} failed" if fails else "\nall passed")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main(sys.argv[1:]))
