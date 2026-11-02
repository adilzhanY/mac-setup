#!/usr/bin/env python3
"""Rank source files by churn times untested code, so the audit starts where bugs are likely.

Usage: python3 -I riskgaps.py <lcov.info> [since="12 months ago"] [risk regex]   (run from the repo root)
       python3 -I riskgaps.py --selftest                                         prove it on built in fixtures
Output: the top 20 files, columns: score (commits x (uncovered lines + untaken branches)), commits,
line %, branch %, uncovered lines, untaken branches, path, and RISK when the path matches the risk regex
(default: pay, bill, price, money, auth, login, session, perm, role, migrat, sync, parse, import, export, delete).
Exit 0. Files with no commits in the window score 0; files outside the lcov report are not listed."""
import os, re, subprocess, sys
from collections import Counter, defaultdict

RISK = r'pay|bill|price|money|auth|login|session|perm|role|migrat|sync|parse|import|export|delete'


def churn_from_log(log_text):
    """Commit count per path from `git log --format=format: --name-only` output."""
    return Counter(l for l in log_text.splitlines() if l.strip())


def coverage(lines, root):
    """{path: [lines found, lines hit, branches found, branches taken]} from lcov lines."""
    cov, sf = defaultdict(lambda: [0, 0, 0, 0]), None
    for l in lines:
        l = l.strip()
        if l.startswith('SF:'): sf = os.path.relpath(os.path.abspath(os.path.join(root, l[3:])), root)
        elif l.startswith('DA:'):
            c = cov[sf]; c[0] += 1; c[1] += int(l[3:].split(',')[1]) > 0
        elif l.startswith('BRDA:'):
            c = cov[sf]; c[2] += 1; c[3] += l.rsplit(',', 1)[1] not in ('-', '0')
    return cov


def rank(churn, cov, risk, top=20):
    rows = []
    for path, (lf, lh, bf, bt) in cov.items():
        miss = (lf - lh) + (bf - bt)
        rows.append((churn.get(path, 0) * miss, churn.get(path, 0), 100 * lh / lf if lf else 100,
                     100 * bt / bf if bf else 100, lf - lh, bf - bt, path))
    return [f'{s:7d} {n:4d} commits  lines {lp:5.1f}%  branches {bp:5.1f}%  {ml:4d} lines {mb:4d} branches  {p}'
            + ('  RISK' if risk.search(p) else '')
            for s, n, lp, bp, ml, mb, p in sorted(rows, reverse=True)[:top]]


LOG = "\nsrc/sync.ts\nsrc/util.ts\n\nsrc/sync.ts\nREADME.md\n\nsrc/sync.ts\n\nsrc/dead.ts\n"
LCOV = """SF:src/util.ts
DA:1,1
DA:2,0
end_of_record
SF:src/sync.ts
DA:1,1
DA:2,0
DA:3,0
BRDA:1,0,0,1
BRDA:1,0,1,0
end_of_record
SF:src/dead.ts
DA:1,1
end_of_record
"""


def selftest():
    out = rank(churn_from_log(LOG), coverage(LCOV.splitlines(), os.getcwd()), re.compile(RISK))
    checks = [
        ('churned, untested sync file ranks first with score 3 x 3 = 9', out[0].split()[0] == '9' and out[0].endswith('src/sync.ts  RISK')),
        ('util ranks second with score 1 x 1 = 1, no RISK tag', out[1].split()[0] == '1' and out[1].endswith('src/util.ts')),
        ('fully covered file scores 0', out[2].split()[0] == '0' and 'src/dead.ts' in out[2]),
        ('README (not in lcov) is not listed', not any('README' in l for l in out)),
    ]
    for name, ok in checks: print(('PASS ' if ok else 'FAIL ') + name)
    bad = [n for n, ok in checks if not ok]
    if bad: print('\n'.join(out))
    print('selftest failed' if bad else 'selftest ok')
    return 1 if bad else 0


def main(argv):
    since = argv[1] if len(argv) > 1 else '12 months ago'
    risk = re.compile(argv[2] if len(argv) > 2 else RISK)
    log = subprocess.run(['git', 'log', f'--since={since}', '--format=format:', '--name-only', '--no-renames'],
                         capture_output=True, text=True, check=True).stdout
    with open(argv[0]) as f:
        for line in rank(churn_from_log(log), coverage(f, os.getcwd()), risk): print(line)
    return 0


if __name__ == '__main__':
    if sys.argv[1:2] in (['-h'], ['--help']) or not sys.argv[1:]: print(__doc__); sys.exit(0 if sys.argv[1:] else 2)
    if sys.argv[1:] == ['--selftest']: sys.exit(selftest())
    sys.exit(main(sys.argv[1:]))
