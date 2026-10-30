#!/usr/bin/env python3
"""Consistency check for the kwx-developer skill. Standard library only.

Checks, all relative to the skill root:
  paths     every file path named in SKILL.md exists
  linked    every .md outside sources/ is linked from SKILL.md
  refs      every skill path (architecture/..., quality/..., scripts/...) named
            in any reference file exists
  scripts   every scripts/<name> a doc names exists
  dashes    no em or en dash characters in any file outside sources/
  contents  every reference file over 100 lines starts with a Contents list
  endcheck  every reference file over 100 lines ends with a Checks section
  version   VERSION matches metadata.version in the SKILL.md frontmatter
  budget    SKILL.md stays under about 5k tokens, description under 1024 chars
  pins      load bearing phrases are still present (see PINS)
  greps     the fast check greps in quality/quality-gate.md section 12 still
            catch known bad lines and pass known clean ones (runs real grep)

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
DASHES = re.compile("[\u2013\u2014]")
SKILL_CHAR_BUDGET = 20000  # about 5k tokens at 4 characters per token
LONG = 100
TEXT_EXT = (".md", ".py", ".sh", ".json", ".txt", ".yml", ".yaml", ".toml")
SKILL_DIRS = ("ai-agents", "architecture", "backend", "data", "evals", "languages",
              "quality", "reliability", "scripts", "security", "workflow")

# Phrases that the router, evals and other files rely on. Rewording one trips
# the check, which is the reminder to update every copy that repeats it.
PINS = {
    "SKILL.md": ["## Critical rules"],
    "quality/quality-gate.md": [
        "An item marked **[critical]** blocks shipping on its own.",
        "## 12. Fast checks",
        *[f"| {i} [critical] |" for i in ("A1", "A3", "A4", "B1", "B4", "C1", "C2", "C3", "D1",
                                          "E1", "E2", "F1", "F2", "F3", "F4", "H1", "I1")],
    ],
    "workflow/audit-and-ask.md": ["| (a) later | `Later` |", "| (b) plan | `Plan a fix` |",
                                  "| (c) keep | `Keep as is` |", "Never re-ask, never fix unasked"],
    "workflow/codebase-first.md": ["**the map lives in the conversation.**"],
}

# Lines the section 12 greps must and must not report, keyed by a word in the
# comment above each grep. Each sample is prefixed like a line of added.txt.
GREP_CASES = {
    "swallowed": (["catch (e) {}", "} catch {}", ".catch(() => {})", ".catch(() => null)",
                   "let _ = fs::remove_file(&p);", "except Exception: pass", "conn.close().ok();"],
                  ["catch (e) { log.error(e); throw e }", ".catch((e) => report(e))",
                   "let _guard = lock.lock();", "if ok():"]),
    "stubs": (["// TODO finish", "todo!()", "raise NotImplementedError", 'throw new Error("Not implemented")'],
              ["const todos = []", "fetchTodo(id)", "// explains why"]),
    "focused": (["it.only('x', fn)", "describe.skip('y', fn)", "xit('z', fn)", "#[ignore]", "@pytest.mark.skip"],
                ["iter().skip(1)", "query.skip(10)", "it('runs', fn)"]),
    "secrets": (['const k = "sk_' 'live_abcdefghijklmnop1234";', "AWS=AKIA" "ABCDEFGHIJKLMNOP",
                 'password: "hunter2hunter2"', "apiKey = 'abcd1234efgh'", "-----BEGIN RSA " "PRIVATE KEY-----"],
                ["password: z.string().min(8)", "const token = await getToken()",
                 "apiKey: process.env.API_KEY", "type Secret = string"]),
    "sql": (["db.query(`SELECT * FROM t WHERE id = ${id}`)", 'conn.execute("SELECT * FROM t WHERE id=" + id)',
             'format!("SELECT * FROM t WHERE id = {}", id)', "execSync(`rm -rf ${dir}`)"],
            ["sql`SELECT * FROM t WHERE id = ${id}`", 'db.query("SELECT * FROM t WHERE id = $1", [id])',
             'sqlx::query!("SELECT 1")']),
    "dashes": (["a \u2014 b", "pages 1\u20132"], ["a - b", "x -> y"]),
}


def rel(root, path):
    return os.path.relpath(path, root).replace(os.sep, "/")


def files(root, exts=None):
    for d, dirs, names in os.walk(root):
        dirs[:] = sorted(x for x in dirs if not x.startswith(".") and x != "__pycache__")
        if rel(root, d).split("/")[0] == "sources":
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


def gate_patterns(gate_text):
    """{case name: (grep flag, pattern)} from the section 12 greps, matched by their comment."""
    found, comment = {}, ""
    for line in gate_text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            comment = s.lower()
            continue
        m = re.match(r"grep -([EP]) '(.*)' \"\$A\"", s)
        if m:
            for name in GREP_CASES:
                if name in comment and name not in found:
                    found[name] = (m.group(1), m.group(2))
    return found


def grep_lines(flag, pattern, lines):
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as f:
        f.write("\n".join("src/x.ts:1: " + x for x in lines) + "\n")
        name = f.name
    try:
        p = subprocess.run(["grep", "-n" + flag, pattern, name], capture_output=True, text=True,
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
    pats = gate_patterns(read(gate))
    out = []
    for name, (hits, clean) in GREP_CASES.items():
        if name not in pats:
            out.append(f"greps: no '{name}' grep found in quality-gate.md section 12")
            continue
        flag, pat = pats[name]
        got = grep_lines(flag, pat, hits + clean)
        if got is None:
            out.append(f"greps: the {name} grep is not a valid pattern")
            continue
        out += [f"greps: the {name} grep misses {hits[i - 1]!r}" for i in range(1, len(hits) + 1) if i not in got]
        out += [f"greps: the {name} grep wrongly hits {clean[i - 1]!r}" for i in range(1, len(clean) + 1)
                if i + len(hits) in got]
    return out


def run_checks(root, pins=PINS):
    skill_path = os.path.join(root, "SKILL.md")
    if not os.path.exists(skill_path):
        return ["paths: SKILL.md is missing"]
    skill = read(skill_path)
    return (check_paths(root, skill) + check_linked(root, skill) + check_refs(root) + check_scripts(root)
            + check_dashes(root) + check_contents(root) + check_endcheck(root) + check_version(root, skill)
            + check_budget(skill) + check_pins(root, pins) + check_greps(root))


def selftest():
    fails = []

    def expect(name, problems, tag):
        ok = any(p.startswith(tag + ":") for p in problems) if tag else not problems
        print(("PASS " if ok else "FAIL ") + name + ("" if ok else f" -> {problems}"))
        if not ok:
            fails.append(name)

    pins = {"SKILL.md": ["## Critical rules"], "quality/quality-gate.md": ["| A1 [critical] |"]}
    with tempfile.TemporaryDirectory() as tmp:
        def write(d, r, text, mode="w"):
            os.makedirs(os.path.dirname(os.path.join(d, r)), exist_ok=True)
            with open(os.path.join(d, r), mode, encoding="utf-8") as f:
                f.write(text)

        def build(name):
            d = os.path.join(tmp, name)
            os.makedirs(os.path.join(d, "scripts"))
            gate = read(os.path.join(ROOT, "quality", "quality-gate.md"))
            section12 = gate[gate.index("## 12. Fast checks"):gate.index("## 13.")]
            write(d, "quality/quality-gate.md", "# gate\n| A1 [critical] | x |\n" + section12)
            open(os.path.join(d, "scripts", "scan_conventions.py"), "w").close()
            write(d, "VERSION", "1.2.3\n")
            write(d, "SKILL.md", "---\nname: t\ndescription: test skill\nmetadata:\n  version: 1.2.3\n---\n"
                  "# t\n## Critical rules\n| `quality/quality-gate.md` | gate |\n")
            write(d, "sources/notes.md", "research with a dash \u2014 allowed here, never linked\n")
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

        d = build("dashes")
        write(d, "SKILL.md", "A rule \u2014 with a dash.\n", "a")
        expect("em dash outside sources is caught", run_checks(d, pins), "dashes")

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

        d = build("greps")
        g = os.path.join(d, "quality", "quality-gate.md")
        write(d, "quality/quality-gate.md", read(g).replace(r"\blet _ = |", ""))
        expect("swallowed error grep that lost a branch is caught", run_checks(d, pins), "greps")

        d = build("greps2")
        g = os.path.join(d, "quality", "quality-gate.md")
        write(d, "quality/quality-gate.md", read(g).replace(r"\b(it|test|describe|context)\.(only|skip)\(", r"\.(only|skip)\("))
        expect("focused test grep that hits Iterator::skip is caught", run_checks(d, pins), "greps")

    print(f"\n{len(fails)} failed" if fails else "\nall passed")
    return 1 if fails else 0


def main(argv):
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
