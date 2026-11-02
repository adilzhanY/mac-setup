#!/usr/bin/env python3
"""List changed lines that tests never ran, and changed lines with a branch never taken.

Usage: python3 -I diffgaps.py <lcov.info> [base=origin/main]   (run from the repo root)
       python3 -I diffgaps.py --selftest                        prove it on built in fixtures
Reads any lcov file (Vitest, Jest, cargo llvm-cov, coverage.py `coverage lcov`) and `git diff -U0 <base>`.
Output: "path:line  NOT RUN" or "path:line  BRANCH taken/total taken", then a count on stderr.
Exit 1 when there are gaps, 0 when every changed instrumented line ran with all its branches.
A changed file missing from the lcov report is skipped silently (tests, config, or outside coverage.include)."""
import os, re, subprocess, sys
from collections import defaultdict


def changed_lines(diff_text):
    """{path: set of new line numbers} from `git diff -U0` output."""
    changed, f = defaultdict(set), None
    for l in diff_text.splitlines():
        if l.startswith('+++ '): f = None if l[4:] == '/dev/null' else l[6:]
        m = re.match(r'@@ -\S+ \+(\d+)(?:,(\d+))? @@', l)
        if m and f:
            start, n = int(m.group(1)), int(m.group(2) or 1)
            changed[f].update(range(start, start + n))
    return changed


def read_lcov(lines, root):
    """(line hits {path: {line: count}}, branches {path: {line: [taken, ...]}}) from lcov lines."""
    hits, branches, sf = defaultdict(dict), defaultdict(lambda: defaultdict(list)), None
    for l in lines:
        l = l.strip()
        if l.startswith('SF:'): sf = os.path.relpath(os.path.abspath(os.path.join(root, l[3:])), root)
        elif l.startswith('DA:'):
            n, c = l[3:].split(',')[:2]; hits[sf][int(n)] = int(c)
        elif l.startswith('BRDA:'):
            n, _, _, taken = l[5:].split(','); branches[sf][int(n)].append(taken not in ('-', '0'))
    return hits, branches


def gaps(changed, hits, branches):
    out = []
    for path in sorted(changed):
        if path not in hits: continue
        for n in sorted(changed[path]):
            if hits[path].get(n) == 0: out.append(f'{path}:{n}  NOT RUN')
            elif n in branches[path] and not all(branches[path][n]):
                b = branches[path][n]; out.append(f'{path}:{n}  BRANCH {sum(b)}/{len(b)} taken')
    return out


DIFF = """diff --git a/src/price.ts b/src/price.ts
--- a/src/price.ts
+++ b/src/price.ts
@@ -3,0 +4,3 @@ export function price(c, coupon) {
+  if (coupon) return c * 0.9
+  const tax = c * 0.2
+  return c + tax
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -1 +1 @@
-old
+new
"""
LCOV = """SF:src/price.ts
DA:1,3
DA:4,3
DA:5,0
DA:6,3
DA:7,3
BRDA:4,0,0,3
BRDA:4,0,1,0
end_of_record
"""


def selftest():
    got = gaps(changed_lines(DIFF), *read_lcov(LCOV.splitlines(), os.getcwd()))
    want = ['src/price.ts:4  BRANCH 1/2 taken', 'src/price.ts:5  NOT RUN']
    ok = got == want
    print(('PASS' if ok else 'FAIL') + f' untaken branch and unrun line found, README skipped: {got}')
    full = LCOV.replace('DA:5,0', 'DA:5,1').replace('BRDA:4,0,1,0', 'BRDA:4,0,1,1')
    clean = gaps(changed_lines(DIFF), *read_lcov(full.splitlines(), os.getcwd()))
    print(('PASS' if not clean else 'FAIL') + f' fully covered change gives no gaps: {clean}')
    ok = ok and not clean
    print('selftest ok' if ok else 'selftest failed')
    return 0 if ok else 1


def main(argv):
    lcov, base = argv[0], (argv[1] if len(argv) > 1 else 'origin/main')
    diff = subprocess.run(['git', 'diff', '-U0', base, '--'], capture_output=True, text=True, check=True).stdout
    with open(lcov) as f:
        found = gaps(changed_lines(diff), *read_lcov(f, os.getcwd()))
    for g in found: print(g)
    print(f'{len(found)} gap(s) in changed code', file=sys.stderr)
    return 1 if found else 0


if __name__ == '__main__':
    if sys.argv[1:2] in (['-h'], ['--help']) or not sys.argv[1:]: print(__doc__); sys.exit(0 if sys.argv[1:] else 2)
    if sys.argv[1:] == ['--selftest']: sys.exit(selftest())
    sys.exit(main(sys.argv[1:]))
