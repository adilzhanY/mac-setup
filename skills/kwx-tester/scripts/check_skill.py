#!/usr/bin/env python3
"""Consistency check for the kwx-tester skill. Standard library only.

Checks, all relative to the skill root:
  paths     every file path named in SKILL.md exists
  linked    every .md outside sources/ is linked from SKILL.md
  refs      every skill path (strategy/..., quality/..., scripts/...) named
            in any reference file exists
  scripts   every scripts/<name> a doc names exists
  dashes    no em or en dash characters in any text file, sources/ included
  contents  every reference file over 100 lines starts with a Contents list
  endcheck  every reference file over 100 lines ends with a Checks section
  version   VERSION matches metadata.version in the SKILL.md frontmatter
  budget    SKILL.md stays under about 5k tokens, description under 1024 chars
  pins      load bearing phrases are still present (see PINS)

Usage:
    python3 check_skill.py            check the skill this script lives in
    python3 check_skill.py <root>     check another copy
    python3 check_skill.py --selftest prove every check catches its failure
Exit code 0 when clean, 1 when a problem was found.
"""

import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASHES = re.compile("[\u2013\u2014]")
SKILL_CHAR_BUDGET = 20000  # about 5k tokens at 4 characters per token
LONG = 100
TEXT_EXT = (".md", ".py", ".sh", ".json", ".txt", ".yml", ".yaml", ".toml")
SKILL_DIRS = ("ai-agents", "backend", "desktop", "evals", "exploratory", "mobile",
              "performance", "quality", "scripts", "strategy", "web", "workflow")

# Phrases that the router, evals and other files rely on. Rewording one trips
# the check, which is the reminder to update every copy that repeats it.
PINS = {
    "SKILL.md": ["## Critical rules", "~/.claude/ui-designer/mistakes.md", "section 5a"],
    "quality/quality-gate.md": [
        "An item marked **[critical]** blocks shipping on its own.",
        "## Fast checks",
        *[f"| {i} [critical] |" for i in ("A1", "A2", "B1", "B2", "C1", "C2", "C3", "C4",
                                          "D1", "F1", "F2", "F3", "G7")],
    ],
    "strategy/strategy.md": ["## 5a. Effort tiers"],
    "workflow/test-suite-audit.md": ["| (a) later | `Later` |", "| (b) plan | `Plan a fix` |",
                                     "| (c) keep | `Keep as is` |"],
}


def rel(root, path):
    return os.path.relpath(path, root).replace(os.sep, "/")


def files(root, exts=None, sources=False):
    for d, dirs, names in os.walk(root):
        dirs[:] = sorted(x for x in dirs if not x.startswith(".") and x != "__pycache__")
        if not sources and rel(root, d).split("/")[0] == "sources":
            continue
        for n in sorted(names):
            if exts is None or n.endswith(exts):
                yield os.path.join(d, n)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def strip_fences(text):
    return re.sub(r"^```.*?^```[^\n]*$", "", text, flags=re.S | re.M)


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


def check_refs(root):
    out = []
    pat = re.compile(r"(?<![\w./~$}-])((?:%s)/(?:[\w-]+/)*[\w.-]+\.(?:md|py|sh|json))" % "|".join(SKILL_DIRS))
    for p in files(root, (".md",)):
        r = rel(root, p)
        if r == "SKILL.md":
            continue
        for m in sorted(set(pat.findall(read(p)))):
            if not os.path.exists(os.path.join(root, m)):
                out.append(f"refs: {r} names {m}, which does not exist")
    return out


def check_scripts(root):
    out = []
    pat = re.compile(r"(?:\$\{CLAUDE_SKILL_DIR\}/|kwx-tester/|(?<![\w/.~$}-]))scripts/([\w-]+\.(?:py|sh))")
    for p in files(root, (".md",)):
        for name in sorted(set(pat.findall(read(p)))):
            if not os.path.exists(os.path.join(root, "scripts", name)):
                out.append(f"scripts: {rel(root, p)} names scripts/{name}, which does not exist")
    return out


def check_dashes(root):
    out = []
    for p in files(root, TEXT_EXT, sources=True):
        for i, line in enumerate(read(p).splitlines(), 1):
            if DASHES.search(line):
                out.append(f"dashes: {rel(root, p)}:{i} has an em or en dash")
    return out


def long_docs(root):
    for p in files(root, (".md",)):
        r = rel(root, p)
        text = read(p)
        if r != "SKILL.md" and text.count("\n") + 1 > LONG:
            yield r, text


def check_contents(root):
    return [f"contents: {r} has over {LONG} lines and no Contents list at the top"
            for r, text in long_docs(root) if "## Contents" not in "\n".join(text.splitlines()[:30])]


def check_endcheck(root):
    out = []
    for r, text in long_docs(root):
        heads = re.findall(r"^## (.+)$", strip_fences(text), re.M)
        if not heads or "Checks" not in heads[-1]:
            out.append(f"endcheck: {r} has over {LONG} lines and does not end with a Checks section")
    return out


def frontmatter(skill):
    m = re.match(r"---\n(.*?)\n---", skill, re.S)
    return m.group(1) if m else ""


def check_version(root, skill):
    vpath = os.path.join(root, "VERSION")
    if not os.path.exists(vpath):
        return ["version: VERSION file is missing"]
    want = read(vpath).strip()
    m = re.search(r"^metadata:\s*\n(?:[ \t]+.*\n)*?[ \t]+version:\s*[\"']?([\w.+-]+)", frontmatter(skill) + "\n", re.M)
    if not m:
        return ["version: SKILL.md frontmatter has no metadata.version"]
    if m.group(1) != want:
        return [f"version: VERSION says {want}, SKILL.md metadata.version says {m.group(1)}"]
    return []


def check_budget(skill):
    out = []
    if len(skill) > SKILL_CHAR_BUDGET:
        out.append(f"budget: SKILL.md is {len(skill)} characters, over {SKILL_CHAR_BUDGET} (about 5k tokens)")
    m = re.search(r"^description:\s*(.+)$", frontmatter(skill), re.M)
    if not m:
        out.append("budget: SKILL.md has no description line in its frontmatter")
    elif len(m.group(1)) > 1024:
        out.append(f"budget: description is {len(m.group(1))} characters, over 1024")
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


def run_checks(root, pins=PINS):
    skill_path = os.path.join(root, "SKILL.md")
    if not os.path.exists(skill_path):
        return ["paths: SKILL.md is missing"]
    skill = read(skill_path)
    return (check_paths(root, skill) + check_linked(root, skill) + check_refs(root) + check_scripts(root)
            + check_dashes(root) + check_contents(root) + check_endcheck(root) + check_version(root, skill)
            + check_budget(skill) + check_pins(root, pins))


def selftest():
    fails = []

    def expect(name, problems, tag):
        ok = any(p.startswith(tag + ":") for p in problems) if tag else not problems
        print(("PASS " if ok else "FAIL ") + name + ("" if ok else f" -> {problems}"))
        if not ok:
            fails.append(name)

    pins = {"SKILL.md": ["## Critical rules"], "quality/quality-gate.md": ["## Fast checks"]}
    with tempfile.TemporaryDirectory() as tmp:
        def write(d, r, text, mode="w"):
            os.makedirs(os.path.dirname(os.path.join(d, r)), exist_ok=True)
            with open(os.path.join(d, r), mode, encoding="utf-8") as f:
                f.write(text)

        def build(name):
            d = os.path.join(tmp, name)
            os.makedirs(os.path.join(d, "scripts"))
            write(d, "quality/quality-gate.md", "# gate\n## Fast checks\nRun `scripts/smellscan.py`.\n")
            open(os.path.join(d, "scripts", "smellscan.py"), "w").close()
            write(d, "VERSION", "1.2.3\n")
            write(d, "SKILL.md", "---\nname: t\ndescription: test skill\nmetadata:\n  version: 1.2.3\n---\n"
                  "# t\n## Critical rules\n| `quality/quality-gate.md` | gate |\n")
            write(d, "sources/notes.md", "research notes, never linked from SKILL.md\n")
            return d

        expect("clean tree passes", run_checks(build("clean"), pins), None)

        d = build("paths")
        write(d, "SKILL.md", "| `quality/missing.md` | x |\n", "a")
        expect("missing linked file is caught", run_checks(d, pins), "paths")

        d = build("linked")
        write(d, "workflow/orphan.md", "# orphan\n")
        expect("unlinked reference file is caught", run_checks(d, pins), "linked")

        d = build("refs")
        write(d, "quality/quality-gate.md", "\nSee `workflow/gone.md` for more.\n", "a")
        expect("reference file naming a missing skill file is caught", run_checks(d, pins), "refs")

        d = build("scripts")
        write(d, "quality/quality-gate.md", "\nRun `python3 ${CLAUDE_SKILL_DIR}/scripts/nope.py`.\n", "a")
        expect("doc naming a missing script is caught", run_checks(d, pins), "scripts")

        d = build("scripts2")
        write(d, "quality/quality-gate.md", "\nRun `python3 -I ~/.claude/skills/kwx-tester/scripts/gone.py`.\n", "a")
        expect("doc naming a missing script by its home path is caught", run_checks(d, pins), "scripts")

        d = build("dashes")
        write(d, "SKILL.md", "A rule \u2014 with a dash.\n", "a")
        expect("em dash outside sources is caught", run_checks(d, pins), "dashes")

        d = build("dashes-sources")
        write(d, "sources/notes.md", "pages 1\u20132 of a paper\n", "a")
        expect("en dash inside sources is caught", run_checks(d, pins), "dashes")

        d = build("contents")
        write(d, "workflow/long.md", "# long\n" + "line\n" * 120 + "## 9. Checks\n")
        write(d, "SKILL.md", "| `workflow/long.md` | x |\n", "a")
        expect("long file without Contents is caught", run_checks(d, pins), "contents")

        d = build("endcheck")
        write(d, "workflow/long.md", "# long\n## Contents\n" + "line\n" * 120
              + "## 9. Checks\n```\n## not a heading, inside a fence\n```\n## 10. Notes\n")
        write(d, "SKILL.md", "| `workflow/long.md` | x |\n", "a")
        expect("long file not ending with Checks is caught", run_checks(d, pins), "endcheck")

        d = build("version")
        write(d, "VERSION", "1.2.4\n")
        expect("VERSION out of step with SKILL.md is caught", run_checks(d, pins), "version")

        d = build("budget")
        write(d, "SKILL.md", "x" * (SKILL_CHAR_BUDGET + 1), "a")
        expect("oversized SKILL.md is caught", run_checks(d, pins), "budget")

        d = build("pins")
        write(d, "SKILL.md", read(os.path.join(d, "SKILL.md")).replace("## Critical rules", "## Rules"))
        expect("lost pinned phrase is caught", run_checks(d, pins), "pins")

    print(f"\n{len(fails)} failed" if fails else "\nall passed")
    return 1 if fails else 0


def main(argv):
    if argv[:1] in (["-h"], ["--help"]):
        print(__doc__)
        return 0
    if "--selftest" in argv:
        return selftest()
    root = os.path.abspath(argv[0]) if argv else ROOT
    problems = run_checks(root)
    for p in problems:
        print(p)
    print(f"{len(problems)} problems" if problems else "check_skill: clean")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
