#!/usr/bin/env python3
"""Tally coding conventions per area of a repo and flag where areas disagree.

Usage: python3 -I scan_conventions.py <repo-root> [--depth N] [--min N]
       python3 -I scan_conventions.py --selftest

An "area" is the first N directory levels under the root (default 2, so
src/features, apps/web, crates/core). For each dimension (export style,
function form, import paths, async style, error style, logging, config
access, test placement, file naming, Rust module files...) it counts each
variant, names the repo majority (the candidate house convention) and lists
areas whose own majority is a different variant (OFF), areas with 20% or
more of another variant (MIX), and, for per file dimensions such as export
style, the files that break their area's majority (ODD, with paths).
Framework files that must look a certain way (Next.js page/layout/route,
Expo Router app/ files, *.config.*, stories) are left out of the export
census. Counts are regex based: treat them as leads to read, not as verdicts.
"""
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict

SKIP_DIRS = {
    "node_modules", "target", "dist", "build", "out", ".git", ".next", ".nuxt",
    ".expo", ".turbo", "coverage", "vendor", ".svelte-kit", "android", "ios",
    "__pycache__", ".venv", "venv", "generated", "gen",
}
TS_EXT = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".mts", ".cts")
RS_EXT = (".rs",)

# dimension -> variant -> regex counted per occurrence (multiline)
TS_RULES = {
    "exported function form": {
        "function declaration": r"^export (?:default )?(?:async )?function\b",
        "arrow const": r"^export const \w+\s*(?::[^=]+)?=\s*(?:async\s*)?(?:\([^)]*\)|\w+)\s*(?::[^=]+)?=>",
    },
    "import paths": {
        "relative": r"""from ['"]\.{1,2}/""",
        "alias (@/ ~/ #)": r"""from ['"](?:@/|~/|#)""",
    },
    "deep relative imports (3+ ../)": {
        "deep relative": r"""from ['"](?:\.\./){3,}""",
    },
    "type declaration": {
        "interface": r"^\s*(?:export )?interface \w+",
        "type alias object": r"^\s*(?:export )?type \w+(?:<[^>]*>)?\s*=\s*\{",
    },
    "async style": {
        "await": r"\bawait\b",
        ".then chain": r"\.then\(",
    },
    "error handling": {
        "throw": r"\bthrow new \w+",
        "result object return": r"return \{\s*(?:ok|success): (?:true|false)|return (?:err|ok)\(",
    },
    "logging": {
        "console.*": r"\bconsole\.(?:log|warn|error|info|debug)\(",
        "logger": r"\b(?:logger|log)\.(?:info|warn|error|debug|trace)\(",
    },
    "config access": {
        "direct env read": r"\bprocess\.env\.|\bimport\.meta\.env\.",
    },
    "type-only imports": {
        "import type": r"^import type\b|import \{[^}]*\btype \w+",
    },
}

RS_RULES = {
    "error type": {
        "anyhow": r"\banyhow::(?:Result|Error|anyhow|bail|Context)\b|\banyhow!\(|\bbail!\(",
        "thiserror": r"#\[derive\([^)]*\bError\b|\bthiserror::",
        "Box<dyn Error>": r"Box<dyn (?:std::error::)?Error",
        "String error": r"Result<[^,>]+,\s*String>",
    },
    "panicking unwrap": {
        "unwrap()/expect() outside tests/": r"\.unwrap\(\)|\.expect\(",
    },
    "visibility": {
        "pub": r"^\s*pub (?:fn|struct|enum|trait|type|const|mod|use)\b",
        "pub(crate)": r"^\s*pub\(crate\)",
    },
    "logging": {
        "println!/eprintln!": r"\be?println!\(",
        "tracing/log": r"\b(?:tracing::|log::)?(?:info|warn|error|debug|trace)!\(",
    },
    "path imports": {
        "use crate::": r"^\s*use crate::",
        "use super:: (not the test glob)": r"^\s*use super::(?!\*;)",
    },
    "glob imports (use super::* in tests excluded)": {
        "glob import": r"^\s*use (?!super::\*;)[\w:]+::\*;",
    },
}

DEFAULT_EXPORT = re.compile(r"^export default\b|^export \{[^}]*\bas default\b", re.M)
NAMED_EXPORT = re.compile(r"^export (?:async )?(?:const|let|function|class|type|interface|enum|abstract class)\b|^export \{", re.M)
# files whose default export is required by a framework; never a finding
FRAMEWORK_FILE = re.compile(
    r"(^|/)(page|layout|route|loading|error|not-found|template|default|global-error|middleware|instrumentation)\.[jt]sx?$"
    r"|(^|/)pages/|(^|/)_(app|document|layout)\.[jt]sx?$|\.config\.|\.stories\.|(^|/)\+")
# per file dimensions get ODD lines naming the files that break their area's majority
ODD_DIMS = {"[ts] export style (per file)", "[ts] test placement", "[rs] module file style"}

CASE_PATTERNS = [
    ("kebab-case", re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")),
    ("snake_case", re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)+$")),
    ("PascalCase", re.compile(r"^[A-Z][a-zA-Z0-9]*$")),
    ("camelCase", re.compile(r"^[a-z][a-z0-9]*[A-Z][a-zA-Z0-9]*$")),
    ("single word", re.compile(r"^[a-z0-9]+$")),
]


def file_case(stem):
    stem = stem.split(".")[0]  # foo.test -> foo, Button.stories -> Button
    for name, pat in CASE_PATTERNS:
        if pat.match(stem):
            return name
    return "other"


def area_of(rel, depth):
    parts = rel.split(os.sep)[:-1]
    return "/".join(parts[:depth]) or "."


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for f in filenames:
            yield os.path.join(dirpath, f)


def scan(root, depth=2, min_count=3):
    """Return (exit code, report lines) for the repo at root."""
    out = []
    tally = defaultdict(lambda: defaultdict(Counter))  # dim -> area -> variant -> n
    where = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))  # dim -> area -> variant -> files
    try:
        expo_router = "expo-router" in open(os.path.join(root, "package.json"), encoding="utf-8").read()
    except OSError:
        expo_router = False
    examples = defaultdict(dict)  # (dim, variant) -> first file seen
    compiled = {}
    for lang, rules in (("ts", TS_RULES), ("rs", RS_RULES)):
        for dim, variants in rules.items():
            for v, rx in variants.items():
                compiled[(lang, dim, v)] = re.compile(rx, re.M)

    rs_module_dirs = []
    for path in walk(root):
        rel = os.path.relpath(path, root)
        base = os.path.basename(path)
        is_ts = base.endswith(TS_EXT) and not base.endswith(".d.ts")
        is_rs = base.endswith(RS_EXT)
        if not (is_ts or is_rs):
            continue
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        area = area_of(rel, depth)
        lang = "ts" if is_ts else "rs"
        rules = TS_RULES if is_ts else RS_RULES
        in_tests = bool(re.search(r"(^|/)(tests?|__tests__|benches|examples)/", rel)) or ".test." in base or ".spec." in base
        posix = rel.replace(os.sep, "/")
        framework = is_ts and bool(FRAMEWORK_FILE.search(posix) or (expo_router and posix.startswith("app/")))
        for dim, variants in rules.items():
            if in_tests and dim == "panicking unwrap":
                continue  # unwrap in tests is idiomatic
            if framework and dim == "exported function form":
                continue  # the framework dictates the shape of these files
            for v in variants:
                n = len(compiled[(lang, dim, v)].findall(text))
                if n:
                    tally[f"[{lang}] {dim}"][area][v] += n
                    examples[f"[{lang}] {dim}"].setdefault(v, rel)

        stem = base.rsplit(".", 1)[0]
        if is_ts:
            is_test = bool(re.search(r"\.(test|spec)\.", base))
            if not is_test and not framework:
                kind = ("default export" if DEFAULT_EXPORT.search(text)
                        else "named exports only" if NAMED_EXPORT.search(text) else None)
                if kind:
                    dim = "[ts] export style (per file)"
                    tally[dim][area][kind] += 1
                    where[dim][area][kind].append(posix)
                    examples[dim].setdefault(kind, posix)
            if is_test:
                place = ("__tests__ folder" if "__tests__" in rel.split(os.sep)
                         else "top-level test dir" if rel.split(os.sep)[0] in ("test", "tests", "e2e")
                         else "colocated")
                tally["[ts] test placement"][area][place] += 1
                where["[ts] test placement"][area][place].append(rel)
                examples["[ts] test placement"].setdefault(place, rel)
            if stem == "index" and re.fullmatch(r"(?:\s*(?://[^\n]*|export \*[^\n]*|export \{[^}]*\}[^\n]*|export type \{[^}]*\}[^\n]*)\s*)*", text):
                tally["[ts] barrel files (index of pure re-exports)"][area]["barrel"] += 1
                examples["[ts] barrel files (index of pure re-exports)"].setdefault("barrel", rel)
            if not is_test and stem not in ("index", "main", "App", "app"):
                c = file_case(stem)
                if c == "single word":  # fits every case style, so it carries no signal
                    continue
                tally["[ts] file naming"][area][c] += 1
                examples["[ts] file naming"].setdefault(c, rel)
        else:
            if base == "mod.rs":
                tally["[rs] module file style"][area]["mod.rs"] += 1
                where["[rs] module file style"][area]["mod.rs"].append(rel)
                examples["[rs] module file style"].setdefault("mod.rs", rel)
            elif ("src" in rel.split(os.sep) and stem not in ("main", "lib")
                  and os.path.isdir(os.path.join(os.path.dirname(path), stem))):
                tally["[rs] module file style"][area]["foo.rs + foo/"] += 1
                where["[rs] module file style"][area]["foo.rs + foo/"].append(rel)
                examples["[rs] module file style"].setdefault("foo.rs + foo/", rel)

    if not tally:
        return 1, ["No .ts/.tsx/.js/.rs sources found under " + root]

    out.append(f"Convention scan of {root} (areas = first {depth} dir levels)")
    out.append("")
    for dim in sorted(tally):
        areas = tally[dim]
        total = Counter()
        for c in areas.values():
            total.update(c)
        if sum(total.values()) < min_count:
            continue
        variants = total.most_common()
        major, major_n = variants[0]
        share = major_n / sum(total.values())
        out.append(f"== {dim}")
        out.append("   repo: " + ", ".join(f"{v} {n}" for v, n in variants)
                   + (f"  -> majority '{major}' ({share:.0%})" if len(variants) > 1 else ""))
        for v, _ in variants:
            ex = examples[dim].get(v)
            if ex:
                out.append(f"   e.g. {v}: {ex}")
        if len(variants) == 1:
            out.append("")
            continue
        dissent = []
        for area, c in sorted(areas.items()):
            n = sum(c.values())
            if n < min_count:
                continue
            top, top_n = c.most_common(1)[0]
            minority = n - c[top]
            if top != major:
                dissent.append(f"   OFF  {area}: mostly '{top}' ({top_n}/{n})")
            elif (n - c[major]) / n >= 0.2:
                dissent.append(f"   MIX  {area}: {dict(c)}")
            if top == major and minority and dim in ODD_DIMS:
                for v, k in c.items():
                    if v != top:
                        files = sorted(where[dim][area][v])
                        more = f" (+{len(files) - 5} more)" if len(files) > 5 else ""
                        dissent.append(f"   ODD  {area}: {k} of {n} files '{v}': " + ", ".join(files[:5]) + more)
        out.extend(dissent if dissent else ["   every area follows the majority"])
        out.append("")
    out.append("Read the flagged files before calling anything a problem: a variant can be "
               "required by a framework (default export for Next.js pages, Expo Router routes, "
               "config files) or be the newer convention the team is migrating to.")
    return 0, out


def selftest():
    """Build a repo with a known mix and check every flag the audit relies on."""
    files = {
        "package.json": '{"name": "fixture"}',
        # lib: 6 files export by name, 1 by default -> one ODD line naming that file
        **{f"src/lib/util{i}.ts": f"export function f{i}() {{ return {i} }}\n" for i in range(6)},
        "src/lib/cropUtils.ts": "export default async function getCroppedImg() {}\n",
        # hooks: named, like lib
        **{f"src/hooks/use{i}.ts": f"export function use{i}() {{ return {i} }}\n" for i in range(4)},
        # components: every file default -> the area is OFF against the repo majority
        **{f"src/components/Card{i}.tsx": f"export default function Card{i}() {{ return null }}\n" for i in range(4)},
        # framework files: must never be counted
        "app/page.tsx": "export default function Page() { return null }\n",
        "app/layout.tsx": "export default function Layout() { return null }\n",
        "app/blog/page.tsx": "export default function Blog() { return null }\n",
        "next.config.ts": "export default {}\n",
        # rust: one crate with mod.rs, others with foo.rs + foo/ -> module style split
        "crates/a/src/lib.rs": "pub mod net;\n",
        "crates/a/src/net/mod.rs": "pub fn get() {}\n",
        "crates/b/src/lib.rs": "pub mod io;\n",
        "crates/b/src/io.rs": "pub mod read;\n",
        "crates/b/src/io/read.rs": "pub fn read() {}\n",
        "crates/c/src/lib.rs": "pub mod db;\n",
        "crates/c/src/db.rs": "pub mod pool;\n",
        "crates/c/src/db/pool.rs": "pub fn pool() {}\n",
    }
    checks = [
        ("single default export in a named folder is ODD with its path",
         lambda o: any(l.startswith("   ODD  src/lib:") and "src/lib/cropUtils.ts" in l for l in o)),
        ("folder that exports by default is OFF",
         lambda o: any(l.startswith("   OFF  src/components:") and "default export" in l for l in o)),
        ("named folders are not flagged",
         lambda o: not any(l.split(":")[0].strip().endswith("src/hooks") for l in o if l.startswith("   "))),
        ("framework files are left out of the export census",
         lambda o: not any("page.tsx" in l or "layout.tsx" in l or "next.config" in l for l in o)),
        ("export census counts files, not statements",
         lambda o: any("named exports only 10" in l and "default export 5" in l for l in o)),
        ("rust module file styles are both counted",
         lambda o: any("[rs] module file style" in l for l in o)
         and any("mod.rs 1" in l and "foo.rs + foo/ 2" in l for l in o)),
    ]
    fails = 0
    with tempfile.TemporaryDirectory() as tmp:
        for rel, text in files.items():
            path = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        code, out = scan(tmp, depth=2, min_count=3)
        for name, ok in checks:
            good = code == 0 and ok(out)
            fails += not good
            print(("PASS " if good else "FAIL ") + name)
        if fails:
            print("\n".join(out))
        empty = os.path.join(tmp, "empty")
        os.makedirs(empty)
        good = scan(empty)[0] == 1
        fails += not good
        print(("PASS " if good else "FAIL ") + "a tree with no sources exits 1 instead of looking clean")
    print(f"\n{fails} failed" if fails else "\nall passed")
    return 1 if fails else 0


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args[0] == "--selftest":
        return selftest()
    root = os.path.abspath(args[0])
    depth = int(args[args.index("--depth") + 1]) if "--depth" in args else 2
    min_count = int(args[args.index("--min") + 1]) if "--min" in args else 3
    code, out = scan(root, depth, min_count)
    print("\n".join(out))
    return code


if __name__ == "__main__":
    sys.exit(main())
