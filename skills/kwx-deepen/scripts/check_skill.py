#!/usr/bin/env python3
"""Validate the kwx-deepen skill: frontmatter, links, field playbook shape, evals, versions, dashes.

usage: check_skill.py [skill_dir]      (default: the folder above this script)
       check_skill.py --selftest
"""
import json
import re
import sys
import tempfile
from pathlib import Path

DASHES = re.compile("[\u2013\u2014]")
FIELD_HEADINGS = [
    "## When this playbook applies",
    "## The expert",
    "## Moves the expert makes unasked",
    "## Raw material",
    "## Methods and tools",
    "## Independent proof",
    "## Amateur mistakes",
    "## Scope traps",
    "## Worked example",
    "## Sources",
]
SKILL_PINS = ["## The six steps", "## When to deepen", "## When not to deepen", "## Output"]


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def check(root: Path):
    errors = []
    skill = root / "SKILL.md"
    if not skill.exists():
        return ["SKILL.md missing"]
    text = skill.read_text()
    fm = frontmatter(text)
    if not fm:
        errors.append("SKILL.md: no frontmatter")
    else:
        if fm.get("name") != root.name:
            errors.append(f"SKILL.md: name {fm.get('name')!r} differs from folder {root.name!r}")
        desc = fm.get("description", "")
        if not desc:
            errors.append("SKILL.md: empty description")
        elif len(desc) > 1024:
            errors.append(f"SKILL.md: description is {len(desc)} chars, limit 1024")
    for pin in SKILL_PINS:
        if pin not in text:
            errors.append(f"SKILL.md: missing section {pin!r}")
    # every backticked relative path in SKILL.md must exist
    for ref in sorted(set(re.findall(r"`((?:method|fields|examples|evals|scripts|sources)/[\w./-]+)`", text))):
        if not (root / ref).exists():
            errors.append(f"SKILL.md: points at missing {ref}")
    # field playbooks keep one shape
    for f in sorted((root / "fields").glob("*.md")):
        body = f.read_text()
        for h in FIELD_HEADINGS:
            if h not in body:
                errors.append(f"fields/{f.name}: missing heading {h!r}")
    # evals
    for name, key in (("triggers.json", None), ("evals.json", "evals")):
        p = root / "evals" / name
        if not p.exists():
            errors.append(f"evals/{name} missing")
            continue
        try:
            data = json.loads(p.read_text())
        except json.JSONDecodeError as e:
            errors.append(f"evals/{name}: invalid JSON ({e})")
            continue
        if key and not data.get(key):
            errors.append(f"evals/{name}: no {key}")
        if name == "triggers.json" and not (data.get("should_trigger") and data.get("should_not_trigger")):
            errors.append("evals/triggers.json: needs should_trigger and should_not_trigger lists")
    # versions agree
    version = (root / "VERSION").read_text().strip() if (root / "VERSION").exists() else None
    releases = (root / "RELEASES.md").read_text() if (root / "RELEASES.md").exists() else ""
    if not version:
        errors.append("VERSION missing")
    elif f"## {version}" not in releases:
        errors.append(f"RELEASES.md has no entry for VERSION {version}")
    if version and f"Version {version}" not in text:
        errors.append(f"SKILL.md does not state Version {version}")
    # no em or en dashes anywhere
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.suffix in {".md", ".json", ".py"} and ".git" not in p.parts:
            for i, line in enumerate(p.read_text().splitlines(), 1):
                if DASHES.search(line):
                    errors.append(f"{p.relative_to(root)}:{i}: em or en dash")
    return errors


def selftest():
    good_field = "\n".join(h + "\nx\n" for h in FIELD_HEADINGS)
    def make(d, desc="Deepens a task.", field=good_field, version="1.0.0", extra=""):
        (d / "fields").mkdir(parents=True)
        (d / "evals").mkdir()
        (d / "method").mkdir()
        (d / "method" / "steps.md").write_text("ok\n")
        (d / "SKILL.md").write_text(f"---\nname: {d.name}\ndescription: {desc}\n---\nVersion {version}\n"
                                    + "\n".join(SKILL_PINS) + "\nSee `method/steps.md`.\n" + extra)
        (d / "fields" / "a.md").write_text(field)
        (d / "evals" / "triggers.json").write_text('{"should_trigger": ["a"], "should_not_trigger": ["b"]}')
        (d / "evals" / "evals.json").write_text('{"evals": [{"id": 1}]}')
        (d / "VERSION").write_text(version + "\n")
        (d / "RELEASES.md").write_text(f"## {version} (2026-11-03)\n")
    cases = [
        ("clean skill passes", {}, 0),
        ("long description fails", {"desc": "x" * 1100}, 1),
        ("missing field heading fails", {"field": "## The expert\n"}, 1),
        ("dangling link fails", {"extra": "See `method/missing.md`.\n"}, 1),
        ("dash fails", {"extra": "a \u2014 b\n"}, 1),
    ]
    failed = 0
    for label, kw, expect_errors in cases:
        with tempfile.TemporaryDirectory() as t:
            d = Path(t) / "kwx-deepen"
            d.mkdir()
            make(d, **kw)
            errs = check(d)
            ok = (len(errs) == 0) if expect_errors == 0 else (len(errs) >= 1)
            print(("PASS " if ok else "FAIL ") + label + ("" if ok else f": {errs}"))
            failed += not ok
    with tempfile.TemporaryDirectory() as t:
        d = Path(t) / "kwx-deepen"
        d.mkdir()
        make(d)
        (d / "RELEASES.md").write_text("## 0.9.0\n")
        ok = any("RELEASES.md" in e for e in check(d))
        print(("PASS " if ok else "FAIL ") + "version drift fails")
        failed += not ok
    print("all passed" if not failed else f"{failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    errs = check(root)
    for e in errs:
        print(e)
    print("check_skill: clean" if not errs else f"check_skill: {len(errs)} problems")
    sys.exit(1 if errs else 0)
