#!/usr/bin/env python3
"""Consistency check for the kwx-designer skill. Standard library only.

Checks, all relative to the skill root:
  paths     every file path named in SKILL.md exists
  linked    every .md outside sources/ (and evals/ data) is linked from SKILL.md
  scripts   every scripts/<name> a doc names exists
  dashes    no em or en dash characters in any file outside sources/
  pins      load bearing phrases are still present (see PINS)
  contents  every reference file over 100 lines starts with a Contents list
  budget    SKILL.md stays under about 5k tokens, description under 1024 chars
  greps     the emoji and palette greps in quality-gate.md section 15 still
            catch known bad lines and pass known clean ones (runs real grep)
  agent     ~/.claude/agents/ui-designer.md still points at SKILL.md (if present)
  mistakes  every KM entry of quality/mistakes-library.md has its Looked like,
            Cause, Rule, Check and Source lines; a WARNING (not a problem) for
            each id of ~/.claude/ui-designer/mistakes.md no KM Source names
  router    at most 3 rows of the "Read what you need" table are bold in the
            Read when column
  reversed  rules reversed in 1.1.0 (the 0.55 width factor, destructive on
            hover, the uppercase EMAIL label, one accent per view with dark
            neutral header actions) never come back outside sources/
  tablegrep no backticked grep in a markdown table row contains an escaped
            pipe: copied raw, a backslash pipe is a literal pipe and the grep finds nothing
  version   VERSION, metadata.version in SKILL.md and the first release heading
            in RELEASES.md agree (checked when VERSION exists)

Usage:
    python3 check_skill.py            check the skill this script lives in
    python3 check_skill.py <root>     check another copy
    python3 check_skill.py --selftest prove every check catches its failure
Exit code 0 when clean, 1 when a problem was found.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENT = os.path.expanduser("~/.claude/agents/ui-designer.md")
LOCAL_MISTAKES = os.path.expanduser("~/.claude/ui-designer/mistakes.md")
ROUTER_BOLD_MAX = 3
KM_FIELDS = ("Looked like", "Cause", "Rule", "Check", "Source")
# Rules 1.1.0 reversed. A match outside sources/ means an old rule came back.
REVERSED = [
    r"times about 0\.55|0\.55 \(average glyph width\)",
    r"rare and destructive ones on hover",
    r"destructive actions in tight space appear on hover",
    r"\"x\" \(chosen\)|hover \"x\" \(chosen\)",
    r"small caps grey label \"EMAIL\"",
    r"header actions dark neutral",
    r"One accent fill per view; header actions neutral",
    r"[Oo]ne accent fill per view",
]
DASHES = re.compile("[\u2013\u2014]")
SKILL_CHAR_BUDGET = 20000  # about 5k tokens at 4 characters per token
CONTENTS_THRESHOLD = 100
TEXT_EXT = (".md", ".py", ".sh", ".json", ".txt", ".svg", ".html", ".css", ".js")

# Phrases that other files, hooks and agent prompts rely on. Rewording one trips
# the check, which is the reminder to update every copy that repeats it.
PINS = {
    "SKILL.md": [
        "## Critical rules",
        "One primary action per view",
        "Text never shrinks to fit; the box grows",
        "Never guess sizes on screen",
        "No em or en dashes",
        "Run `quality/quality-gate.md` in full",
        "Read the mistakes library before you write UI",
        "owner-house-style.md",
        "Daily use first",
    ],
    "quality/quality-gate.md": [
        "An item marked **[critical]** blocks shipping on its own.",
        "## 15. Fast code checks",
        *[f"| {i} [critical] |" for i in ("A1", "A2", "A13", "B1", "C1", "C8", "C10", "C13", "D1", "E1", "E10",
                                          "F1", "F2", "H1", "I1", "I3", "K1", "L1", "L2")],
        "or 0.65 (semibold, bold)",
        "Mistakes library:",
        "never by taking screenshots",
        "Only your eyes can confirm",
    ],
    "workflow/lean-build.md": ["kwx-defer: <the limit>, <when to upgrade>"],
    "quality/enforcement.md": ["KWX GATE ACTIVE", "wired in ~/.claude/settings.json"],
    "quality/predict-from-code.md": ["0.65", "0.40 to 0.55"],
    "platforms/desktop/qt-qml.md": ["UiScale.px", "pixelSize.smallest"],
    "house/owner-house-style.md": ["Order of authority"],
}

# Lines the section 15 greps must and must not report.
EMOJI_HITS = ["\u25b6 Play", "\u23f8 Pause", "reset \u21bb", "Next \u2192", "\u2605 4.8",
              "\u2713 Saved", "\U0001f680 Launch", "\u26a1 Fast", "\u2764\ufe0f", "\u2b50 star"]
EMOJI_CLEAN = ["Delete report", "price \u20ac12,50", "a \u00d7 b", "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u04d9\u04e9\u04af"]
PALETTE_HITS = ["background: linear-gradient(#667eea, #764ba2)", "color: #764BA2", "fill: #7c3aed"]
PALETTE_CLEAN = ["color: #667eeb", "background: #1a1a1a"]


def rel(root, path):
    return os.path.relpath(path, root).replace(os.sep, "/")


def files(root, exts=None, skip_sources=True):
    for d, dirs, names in os.walk(root):
        dirs[:] = sorted(x for x in dirs if not x.startswith(".") and x != "__pycache__")
        if skip_sources and rel(root, d).split("/")[0] == "sources":
            continue
        for n in sorted(names):
            if exts is None or n.endswith(exts):
                yield os.path.join(d, n)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def check_paths(root, skill):
    out = []
    for m in sorted(set(re.findall(r"(?<![\w./~-])((?:[\w-]+/)+[\w.-]+\.(?:md|py|sh|json))", skill))):
        if not os.path.exists(os.path.join(root, m)):
            out.append(f"paths: SKILL.md names {m}, which does not exist")
    return out


def check_linked(root, skill):
    out = []
    for p in files(root, (".md",)):
        r = rel(root, p)
        if r != "SKILL.md" and f"`{r}`" not in skill:
            out.append(f"linked: {r} is not linked from SKILL.md")
    return out


def check_scripts(root):
    out = []
    pat = re.compile(r"(?:\$\{CLAUDE_SKILL_DIR\}/|(?<![\w/.~$}-]))scripts/([\w-]+\.(?:py|sh))")
    for p in files(root, (".md",)):
        for name in sorted(set(pat.findall(read(p)))):
            if not os.path.exists(os.path.join(root, "scripts", name)):
                out.append(f"scripts: {rel(root, p)} names scripts/{name}, which does not exist")
    return out


def check_dashes(root):
    out = []
    for p in files(root, TEXT_EXT):
        for i, line in enumerate(read(p).splitlines(), 1):
            if DASHES.search(line):
                out.append(f"dashes: {rel(root, p)}:{i} has an em or en dash")
    return out


def check_pins(root, pins):
    out = []
    for r, phrases in pins.items():
        p = os.path.join(root, r)
        if not os.path.exists(p):
            out.append(f"pins: {r} is missing")
            continue
        text = read(p)
        out += [f"pins: {r} lost the phrase {ph!r}" for ph in phrases if ph not in text]
    return out


def check_contents(root):
    out = []
    for p in files(root, (".md",)):
        r = rel(root, p)
        text = read(p)
        if r == "SKILL.md" or text.count("\n") + 1 <= CONTENTS_THRESHOLD:
            continue
        if "## Contents" not in "\n".join(text.splitlines()[:30]):
            out.append(f"contents: {r} has over {CONTENTS_THRESHOLD} lines and no Contents list at the top")
    return out


def check_budget(skill):
    out = []
    if len(skill) > SKILL_CHAR_BUDGET:
        out.append(f"budget: SKILL.md is {len(skill)} characters, over {SKILL_CHAR_BUDGET} (about 5k tokens)")
    m = re.search(r"^description:\s*(.+)$", skill, re.M)
    if not m:
        out.append("budget: SKILL.md has no description line in its frontmatter")
    elif len(m.group(1)) > 1024:
        out.append(f"budget: description is {len(m.group(1))} characters, over 1024")
    return out


def fast_check_patterns(gate_text):
    """(emoji -P pattern, palette -iE pattern) from the grep lines under their comments."""
    emoji = palette = None
    comment = ""
    for line in gate_text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            comment = s.lower()
            continue
        m = re.match(r"grep -rn(i?)([PE]) '(.*)' \"\$SRC\"", s)
        if m and "emoji" in comment and m.group(2) == "P" and emoji is None:
            emoji = m.group(3)
        if m and "palette" in comment and palette is None:
            palette = m.group(3)
    return emoji, palette


def grep_lines(flags, pattern, lines):
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as f:
        f.write("\n".join(lines) + "\n")
        name = f.name
    try:
        p = subprocess.run(["grep", "-n" + flags, pattern, name], capture_output=True, text=True,
                           env={**os.environ, "LC_ALL": "C.UTF-8"})
        if p.returncode > 1:
            return None
        return {int(x.split(":", 1)[0]) for x in p.stdout.splitlines() if x}
    finally:
        os.unlink(name)


def check_greps(root):
    gate = os.path.join(root, "quality", "quality-gate.md")
    if not os.path.exists(gate):
        return ["greps: quality/quality-gate.md is missing"]
    if shutil.which("grep") is None:
        return []  # nothing to run the patterns with; not a skill problem
    emoji, palette = fast_check_patterns(read(gate))
    out = []
    for name, pat, flags, hits, clean in (("emoji", emoji, "P", EMOJI_HITS, EMOJI_CLEAN),
                                          ("palette", palette, "iE", PALETTE_HITS, PALETTE_CLEAN)):
        if pat is None:
            out.append(f"greps: no {name} grep found in quality-gate.md section 15")
            continue
        got = grep_lines(flags, pat, hits + clean)
        if got is None:
            out.append(f"greps: the {name} grep is not a valid pattern")
            continue
        out += [f"greps: the {name} grep misses {hits[i - 1]!r}" for i in range(1, len(hits) + 1) if i not in got]
        out += [f"greps: the {name} grep wrongly hits {clean[i - 1]!r}" for i in range(1, len(clean) + 1)
                if i + len(hits) in got]
    return out


def check_agent(agent_path):
    if not agent_path or not os.path.exists(agent_path):
        return []
    if "kwx-designer/SKILL.md" not in read(agent_path):
        return [f"agent: {agent_path} no longer points at kwx-designer/SKILL.md"]
    return []


def km_blocks(text):
    """{'KM1': block text, ...} for every '## KMn.' heading."""
    out = {}
    parts = re.split(r"^(?=## KM\d+\.)", text, flags=re.M)
    for p in parts:
        m = re.match(r"## (KM\d+)\.", p)
        if m:
            out[m.group(1)] = p
    return out


def check_mistakes(root, local_path=LOCAL_MISTAKES):
    """(problems, warnings). Problems for malformed KM entries, warnings for local drift."""
    lib = os.path.join(root, "quality", "mistakes-library.md")
    if not os.path.exists(lib):
        return ["mistakes: quality/mistakes-library.md is missing"], []
    blocks = km_blocks(read(lib))
    if not blocks:
        return ["mistakes: quality/mistakes-library.md has no '## KMn.' entries"], []
    problems = []
    for km, block in blocks.items():
        lines = [l.strip() for l in block.splitlines()]
        for field in KM_FIELDS:
            if not any(l.startswith(field) for l in lines):
                problems.append(f"mistakes: {km} has no '{field}' line")
    warnings = []
    if local_path and os.path.exists(local_path):
        local = set(re.findall(r"^## (M\d+)\.", read(local_path), re.M))
        local |= set(re.findall(r"^- \*\*(M\d+)\.", read(local_path), re.M))
        sources = " ".join(l for b in blocks.values() for l in b.splitlines() if l.strip().startswith("Source"))
        for mid in sorted(local, key=lambda x: int(x[1:])):
            if not re.search(rf"\b{mid}\b", sources):
                warnings.append(f"WARNING mistakes: local {mid} in {local_path} has no KM entry naming it")
    return problems, warnings


def check_router(skill):
    m = re.search(r"^## Read what you need.*?(?=^## )", skill, re.S | re.M)
    if not m:
        return ["router: SKILL.md has no 'Read what you need' table"]
    bold = []
    for line in m.group(0).splitlines():
        cells = [c.strip() for c in line.strip().split("|")[1:-1]]
        if len(cells) >= 3 and cells[0].startswith("`") and "**" in cells[-1]:
            bold.append(cells[0])
    if len(bold) > ROUTER_BOLD_MAX:
        return [f"router: {len(bold)} bold must-read rows, over {ROUTER_BOLD_MAX}: {', '.join(bold)}"]
    return []


def check_reversed(root):
    out = []
    pats = [re.compile(p) for p in REVERSED]
    for p in files(root, (".md",)):
        for i, line in enumerate(read(p).splitlines(), 1):
            for pat in pats:
                if pat.search(line):
                    out.append(f"reversed: {rel(root, p)}:{i} brings back a reversed rule ({pat.pattern})")
    return out


TABLE_GREP = re.compile(r"`[^`]*\bgrep\b[^`]*\\\|[^`]*`")


def check_tablegrep(root):
    out = []
    for p in files(root, (".md",)):
        for i, line in enumerate(read(p).splitlines(), 1):
            if line.lstrip().startswith("|") and TABLE_GREP.search(line):
                out.append(f"tablegrep: {rel(root, p)}:{i} has a grep with an escaped pipe in a table cell; "
                           "use a character class or repeat -e")
    return out


def check_version(root, skill):
    vpath = os.path.join(root, "VERSION")
    if not os.path.exists(vpath):
        return []
    version = read(vpath).strip()
    meta = re.search(r"^\s+version:\s*(\S+)", skill, re.M)
    rpath = os.path.join(root, "RELEASES.md")
    release = re.search(r"^## (\d+\.\d+\.\d+)", read(rpath), re.M) if os.path.exists(rpath) else None
    found = {"VERSION": version, "SKILL.md metadata.version": meta and meta.group(1),
             "RELEASES.md first heading": release and release.group(1)}
    if len(set(found.values())) != 1:
        return ["version: versions disagree: " + ", ".join(f"{k} {v}" for k, v in found.items())]
    return []


def run_checks(root, pins=PINS, agent_path=AGENT, local_path=None, warnings=None):
    skill_path = os.path.join(root, "SKILL.md")
    if not os.path.exists(skill_path):
        return ["paths: SKILL.md is missing"]
    skill = read(skill_path)
    mistakes, warn = check_mistakes(root, local_path)
    if warnings is not None:
        warnings.extend(warn)
    return (check_paths(root, skill) + check_linked(root, skill) + check_scripts(root)
            + check_dashes(root) + check_pins(root, pins) + check_contents(root)
            + check_budget(skill) + check_greps(root) + check_agent(agent_path)
            + mistakes + check_router(skill) + check_reversed(root) + check_tablegrep(root)
            + check_version(root, skill))


def selftest():
    fails = []

    def expect(name, problems, tag):
        ok = any(p.startswith(tag + ":") for p in problems) if tag else not problems
        print(("PASS " if ok else "FAIL ") + name + ("" if ok else f" -> {problems}"))
        if not ok:
            fails.append(name)

    pins = {"SKILL.md": ["One primary action per view"], "quality/quality-gate.md": ["| A1 [critical] |"]}
    with tempfile.TemporaryDirectory() as tmp:
        def build(name):
            d = os.path.join(tmp, name)
            os.makedirs(os.path.join(d, "quality"))
            os.makedirs(os.path.join(d, "scripts"))
            os.makedirs(os.path.join(d, "sources"))
            shutil.copy(os.path.join(ROOT, "quality", "quality-gate.md"), os.path.join(d, "quality"))
            for s in ("contrast_check.py", "icon_check.py"):
                open(os.path.join(d, "scripts", s), "w").close()
            with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as f:
                f.write("---\nname: t\ndescription: test skill\n---\n# t\n"
                        "One primary action per view.\n\n## Read what you need\n\n"
                        "| File | What | Read when |\n|---|---|---|\n"
                        "| `quality/quality-gate.md` | gate | **before done** |\n"
                        "| `quality/mistakes-library.md` | defects | **before writing** |\n\n## End\n")
            with open(os.path.join(d, "quality", "mistakes-library.md"), "w", encoding="utf-8") as f:
                f.write("# lib\n\n## KM1. Overflow\n\nLooked like: x\nCause: y\nRule: z\n"
                        "Check: w\nStacks: s\nSource: user M1, 2026-10-18.\n")
            with open(os.path.join(d, "sources", "notes.md"), "w", encoding="utf-8") as f:
                f.write("research with a dash \u2014 allowed here, never linked\n")
            return d

        def write(d, r, text, mode="w"):
            with open(os.path.join(d, r), mode, encoding="utf-8") as f:
                f.write(text)

        expect("clean tree passes", run_checks(build("clean"), pins, None), None)

        d = build("paths")
        write(d, "SKILL.md", "| `quality/missing.md` | x |\n", "a")
        expect("missing linked file is caught", run_checks(d, pins, None), "paths")

        d = build("linked")
        write(d, "quality/orphan.md", "# orphan\n")
        expect("unlinked reference file is caught", run_checks(d, pins, None), "linked")

        d = build("scripts")
        write(d, "quality/quality-gate.md", "\nRun `python3 ${CLAUDE_SKILL_DIR}/scripts/nope.py`.\n", "a")
        expect("doc naming a missing script is caught", run_checks(d, pins, None), "scripts")

        d = build("dashes")
        write(d, "SKILL.md", "A rule \u2014 with a dash.\n", "a")
        expect("em dash outside sources is caught", run_checks(d, pins, None), "dashes")

        d = build("pins")
        write(d, "SKILL.md", read(os.path.join(d, "SKILL.md")).replace("One primary action per view", "One main action"))
        expect("lost pinned phrase is caught", run_checks(d, pins, None), "pins")

        d = build("contents")
        write(d, "quality/long.md", "# long\n" + "line\n" * 120)
        write(d, "SKILL.md", "| `quality/long.md` | x |\n", "a")
        expect("long file without Contents is caught", run_checks(d, pins, None), "contents")

        d = build("budget")
        write(d, "SKILL.md", "x" * (SKILL_CHAR_BUDGET + 1), "a")
        expect("oversized SKILL.md is caught", run_checks(d, pins, None), "budget")

        d = build("greps")
        g = os.path.join(d, "quality", "quality-gate.md")
        text = read(g)
        emoji, _ = fast_check_patterns(text)
        write(d, "quality/quality-gate.md", text.replace(emoji, "[\\x{1F300}-\\x{1FAFF}\\x{2600}-\\x{27BF}]"))
        expect("old pictograph only emoji grep is caught", run_checks(d, pins, None), "greps")

        d = build("palette")
        text = read(g := os.path.join(d, "quality", "quality-gate.md"))
        write(d, "quality/quality-gate.md", text.replace("667eea|764ba2|", ""))
        expect("palette grep without #667eea is caught", run_checks(d, pins, None), "greps")

        d = build("km")
        write(d, "quality/mistakes-library.md",
              read(os.path.join(d, "quality", "mistakes-library.md")).replace("Check: w\n", ""))
        expect("KM entry without a Check line is caught", run_checks(d, pins, None), "mistakes")

        d = build("drift")
        write(tmp, "local-mistakes.md", "# lib\n\n## M1. a\n\n## M2. b\n\n- **M3. c:** d\n")
        warn = []
        probs = run_checks(d, pins, None, os.path.join(tmp, "local-mistakes.md"), warn)
        ok = not probs and any("M2" in w for w in warn) and any("M3" in w for w in warn) \
            and not any(" M1 " in w for w in warn)
        print(("PASS " if ok else "FAIL ") + "local id with no KM entry warns, does not fail"
              + ("" if ok else f" -> {probs} {warn}"))
        if not ok:
            fails.append("drift")

        d = build("router")
        write(d, "SKILL.md", read(os.path.join(d, "SKILL.md")).replace(
            "\n\n## End", "\n| `a/b.md` | x | **always** |\n| `c/d.md` | x | **always** |\n\n## End"))
        expect("4 bold router rows are caught", run_checks(d, pins, None), "router")

        d = build("reversed")
        write(d, "quality/quality-gate.md", "\nFont px times characters times about 0.55 against the box.\n", "a")
        expect("reversed 0.55 width factor is caught", run_checks(d, pins, None), "reversed")

        d = build("tablegrep")
        write(d, "quality/quality-gate.md", "\n| G7 | dashes | `grep -nP '\\x{2014}\\|\\x{2013}'` |\n", "a")
        expect("grep with an escaped pipe in a table row is caught", run_checks(d, pins, None), "tablegrep")

        d = build("version")
        write(d, "VERSION", "1.2.0\n")
        write(d, "RELEASES.md", "# r\n\n## 1.1.0 (2026-11-01)\n")
        write(d, "SKILL.md", "| `RELEASES.md` | x |\n", "a")
        write(d, "SKILL.md", read(os.path.join(d, "SKILL.md")).replace("---\n# t", "metadata:\n  version: 1.2.0\n---\n# t"))
        expect("VERSION and RELEASES.md disagreeing is caught", run_checks(d, pins, None), "version")
        write(d, "RELEASES.md", "# r\n\n## 1.2.0 (2026-11-02)\n")
        expect("matching versions pass", run_checks(d, pins, None), None)

        agent = os.path.join(tmp, "agent.md")
        write(tmp, "agent.md", "Read some other skill.\n")
        expect("agent prompt not pointing at SKILL.md is caught", check_agent(agent), "agent")

    print(f"\n{len(fails)} failed" if fails else "\nall passed")
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    root = os.path.abspath(argv[0]) if argv else ROOT
    warnings = []
    problems = run_checks(root, local_path=LOCAL_MISTAKES, warnings=warnings)
    for w in warnings:
        print(w)
    for p in problems:
        print(p)
    print(f"{len(problems)} problems" if problems else "check_skill: clean")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
