#!/usr/bin/env python3
"""Heuristic test smell scan for JS/TS, Rust, Kotlin and Python test files.

Usage: python3 -I smellscan.py [file or dir]...    (default: the current directory)
       python3 -I smellscan.py --selftest          prove every flag fires on built in fixtures
Output: one line per suspicious test, "path:line  name  FLAGS". Exit 0 (it reports, it does not gate).
Flags: EMPTY, NO-ASSERT, EAGER=k (over 5 distinct things checked), SLEEP, BRANCH (an assertion inside a branch), PRINT, NET (a real host in a network call), SAME (x equals x).
Assertion helpers defined in any scanned file count as assertions, so scan a test folder with its helper files together.
A folder walk opens test files, plus Rust .rs files that hold an inline #[cfg(test)] module.
A hit is a lead, not a finding: open the test and confirm."""
import os, re, sys

EXT = {'.ts': 'js', '.tsx': 'js', '.js': 'js', '.jsx': 'js', '.mjs': 'js',
       '.rs': 'rs', '.kt': 'kt', '.py': 'py'}
START = {
    'js': re.compile(r'\b(?:it|test)(?:\.(?:only|concurrent|fails))?(?:\.each\(.*?\))?\(\s*([\'"`])(.*?)\1\s*,\s*(?:\{[^{}]*\}\s*,\s*)?(?:async\s*)?(?:\([^)]*\)|\w+)\s*=>\s*\{'),
    'rs': re.compile(r'#\[(?:tokio::)?test[^\]]*\](?:\s*#\[[^\]]*\])*\s*(?:async\s+)?fn\s+(\w+)\s*\([^)]*\)[^{]*\{'),
    'kt': re.compile(r'@Test\b[^\n]*\n(?:\s*@\w+[^\n]*\n)*\s*fun\s+`?([^`(]+)`?\s*\([^)]*\)[^{=]*\{'),
}
ASSERT = re.compile(r'\b(?:expect|assert|verify)\w*(?:\.\w+)*!?\s*\(|\bassert\s+\S|\bshould\w*|'
                    r'pytest\.(?:raises|fail|warns)|should_panic|\bthrow\b|\bpanic!\s*\(')
SUBJECT = re.compile(r'\b(?:expect|assert|verify)\w*(?:\.\w+)*!?\s*\(\s*(?:await\s+|&|\*|!)*([A-Za-z_]\w*)')
HELPER_DEF = re.compile(r'(?:function\s+(\w+)\s*\([^)]*\)[^{]*|(?:const|let)\s+(\w+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|\w+)\s*(?::[^=]*)?=>\s*|(?<!#\[test\]\n)fn\s+(\w+)\s*\([^)]*\)[^{]*)\{')
RESERVED = re.compile(r'(^|\.)(example(\.(com|net|org))?|test|invalid|localhost|local)$|^(127\.0\.0\.1|0\.0\.0\.0|\[::1\])$')
NETCALL = re.compile(r'\b(?:fetch|axios|got|request|urlopen|goto|navigate|reqwest|ureq|requests\.\w+|http\.\w+|(?:get|post|put|patch|delete))\s*[!(.]')
CHECKS = [('SLEEP', re.compile(r'sleep\s*\(|setTimeout\s*\(|waitForTimeout\s*\(|Thread\.sleep|delay\s*\(\s*\d')),
          ('PRINT', re.compile(r'console\.log\(|println!?\(|\bprint\(|dbg!\(')),
          ('SAME', re.compile(r'(?:assert_eq!|assertEquals)\(\s*(\w+)\s*,\s*\1\s*\)|assert\s+(\w+)\s*==\s*\2\s*$|expect\((\w+)\)\.toBe\(\3\)', re.M))]

def brace_body(src, i):
    depth = 0
    for j in range(i, len(src)):
        if src[j] == '{': depth += 1
        elif src[j] == '}':
            depth -= 1
            if depth == 0: return src[i + 1:j]
    return src[i + 1:]

def tests(src, lang):
    if lang == 'py':
        lines = src.splitlines()
        for n, l in enumerate(lines):
            m = re.match(r'(\s*)(?:async\s+)?def\s+(test\w*)\s*\(', l)
            if not m: continue
            ind, body = len(m.group(1)), []
            for b in lines[n + 1:]:
                if b.strip() and len(b) - len(b.lstrip()) <= ind: break
                body.append(b)
            yield n + 1, m.group(2), '\n'.join(body)
        return
    for m in START[lang].finditer(src):
        yield src.count('\n', 0, m.start()) + 1, m.groups()[-1], brace_body(src, m.end() - 1)

def helpers(src):
    # same file functions whose body asserts: a call to one counts as an assertion
    names = set()
    for m in HELPER_DEF.finditer(src):
        name = next(g for g in m.groups() if g)
        if ASSERT.search(brace_body(src, m.end() - 1)): names.add(name)
    return names

def branch_asserts(code, verbs):
    # BRANCH only when an assertion (not a throw) sits inside an if/else/switch/match/when
    for m in re.finditer(r'\b(?:if|else|switch|match|when)\b', code):
        i, depth = m.end(), 0
        while i < len(code):
            c = code[i]
            if c == '(': depth += 1
            elif c == ')': depth -= 1
            elif depth == 0 and c == '{': seg = brace_body(code, i); break
            elif depth == 0 and c in ';\n' and code[m.end():i].strip(): seg = code[m.end():i]; break
            i += 1
        else: seg = code[m.end():]
        if verbs.search(seg): return True
    return False

def net(code):
    for line in code.splitlines():
        for host in re.findall(r'https?://([^/\s\'"`)]+)', line):
            host = host.split(':')[0].lower()
            if '.' in host and not RESERVED.search(host) and NETCALL.search(line): return True
    return False

SHARED = set()   # assertion helpers found in every scanned file (tests/helpers.ts, common.rs)

def scan(path):
    lang = EXT.get(os.path.splitext(path)[1])
    if not lang: return
    src = open(path, encoding='utf-8', errors='replace').read()
    hs = (helpers(src) | SHARED) if lang != 'py' else set()
    hcall = re.compile(r'\b(?:' + '|'.join(map(re.escape, hs)) + r')\s*\(') if hs else None
    verbs = re.compile(r'\b(?:expect|assert|verify)\w*(?:\.\w+)*!?\s*\(|\bassert\s+\S' + (r'|' + hcall.pattern if hcall else ''))
    for line, name, body in tests(src, lang):
        code = re.sub(r'^\s*(?://|#).*$', '', body, flags=re.M).strip()
        flags = []
        if not code or code in ('pass', '...'): flags.append('EMPTY')
        else:
            n = len(ASSERT.findall(code)) + (len(hcall.findall(code)) if hcall else 0)
            subjects = set(SUBJECT.findall(code))
            if n == 0: flags.append('NO-ASSERT')
            elif len(subjects) > 5: flags.append(f'EAGER={len(subjects)}')
            if branch_asserts(code, verbs): flags.append('BRANCH')
            if net(code): flags.append('NET')
            flags += [f for f, rx in CHECKS if rx.search(code)]
        if flags: print(f'{path}:{line}  {name.strip()}  {" ".join(flags)}')

TEST_PATH = re.compile(r'(\.(test|spec)\.[jt]sx?$|(^|/)tests?/|_test\.py$|(^|/)test_\w+\.py$|Test\.kt$|/src/test/)')


def walk(args):
    paths = []
    for arg in args or ['.']:
        if os.path.isfile(arg): paths.append(arg); continue
        for root, dirs, files in os.walk(arg):
            dirs[:] = [d for d in dirs if d not in ('node_modules', 'target', '.git', 'build', 'dist', '.venv')]
            for p in (os.path.join(root, f) for f in files):
                if TEST_PATH.search(p) or (p.endswith('.rs') and '#[cfg(test)]' in open(p, encoding='utf-8', errors='replace').read()):
                    paths.append(p)
    for p in paths:
        if EXT.get(os.path.splitext(p)[1]) not in (None, 'py'):
            SHARED.update(helpers(open(p, encoding='utf-8', errors='replace').read()))
    for p in paths: scan(p)


FIXTURES = {
    'a.test.ts': """
it('empty', () => {
})
it('no assert', () => { render(<App/>) })
it('sleeps', async () => { await page.waitForTimeout(500); expect(x).toBe(1) })
it('branches', () => {
  if (isCI) { expect(a).toBe(1) }
})
it('same', () => { expect(total).toBe(total) })
it('good', () => { expect(sum(1, 2)).toBe(3) })
""",
    'b_test.py': """
def test_print():
    print(x)
    assert x == 1

def test_good():
    assert add(1, 2) == 3
""",
    'c.rs': """
#[test]
fn net_call() {
    let r = get("https://api.stripe.com/v1/x");
    assert_eq!(r, 1);
}
#[test]
fn many() { assert!(a); assert!(b); assert!(c); assert!(d); assert!(e); assert!(f); }
#[test]
fn migrate_twice_is_a_no_op() {
    let mut conn = open_memory();
    migrate(&mut conn).unwrap();
    migrate(&mut conn).unwrap();
}
""",
    'e.test.ts': """
import assert from 'node:assert/strict';
import { test } from 'node:test';
test('node assert', async (t) => { const r = await call(); assert.equal(r.status, 201); });
test('t assert', (t) => { t.assert.ok(x) });
test('with options', { timeout: 5000 }, () => { build() })
function expectCents(a, b) { expect(Math.round(a * 100)).toBe(b) }
test('helper', () => { expectCents(f(1), 11) })
test('collects mismatches', () => {
  const bad = [];
  for (const x of xs) { if (f(x) !== g(x)) bad.push(x) }
  expect(bad).toEqual([]);
})
test('throws in loop', () => {
  for (const x of xs) { if (f(x) < 0) throw new Error(String(x)) }
})
test('url as data', async () => {
  const r = await submit({ origin: 'https://evil.example', site: 'http://x' });
  expect(r.ok).toBe(false);
})
test('one subject', () => {
  expect(row.a).toBe(1); expect(row.b).toBe(2); expect(row.c).toBe(3);
  expect(row.d).toBe(4); expect(row.e).toBe(5); expect(row.f).toBe(6); expect(row.g).toBe(7);
})
test('conditional assert', () => {
  if (status === 201) assert.equal(res.status, 201);
})
test.each([1, 2])('each %s', (n) => { expect(n).toBeGreaterThan(0) })
test.each([1, 2])('each no assert %s', (n) => { run(n) })
""",
    'helpers.ts': """
export function bookOk(app, token, id) { expect(book(app, token, id).status).toBe(201) }
""",
    'f.test.ts': """
import { bookOk } from './helpers';
test('books', () => { bookOk(app, t, 1) })
""",
    'DTest.kt': """
class DTest {
    @Test
    fun `no assert here`() {
        build()
    }
}
""",
}
# written under proj/src/ and found by a folder walk, not passed by name
INLINE_RS = {'db.rs': """
pub fn migrate() {}
#[cfg(test)]
mod tests {
    #[test]
    fn inline_no_assert() { migrate(); }
}
""", 'util.rs': 'pub fn plain() {}\n'}
EXPECT = [('a.test.ts', 'empty', 'EMPTY'), ('a.test.ts', 'no assert', 'NO-ASSERT'),
          ('a.test.ts', 'sleeps', 'SLEEP'), ('a.test.ts', 'branches', 'BRANCH'), ('a.test.ts', 'same', 'SAME'),
          ('b_test.py', 'test_print', 'PRINT'), ('c.rs', 'net_call', 'NET'), ('c.rs', 'many', 'EAGER=6'),
          ('c.rs', 'migrate_twice_is_a_no_op', 'NO-ASSERT'), ('db.rs', 'inline_no_assert', 'NO-ASSERT'),
          ('DTest.kt', 'no assert here', 'NO-ASSERT'), ('e.test.ts', 'with options', 'NO-ASSERT'),
          ('e.test.ts', 'conditional assert', 'BRANCH'), ('e.test.ts', 'each no assert %s', 'NO-ASSERT')]
CLEAN = [('a.test.ts', 'good'), ('b_test.py', 'test_good'), ('e.test.ts', 'node assert'), ('e.test.ts', 't assert'),
         ('e.test.ts', 'helper'), ('e.test.ts', 'collects mismatches'), ('e.test.ts', 'throws in loop'),
         ('e.test.ts', 'url as data'), ('e.test.ts', 'one subject'), ('e.test.ts', 'each %s'),
         ('f.test.ts', 'books')]


def selftest():
    import contextlib, io, tempfile
    out = io.StringIO()
    with tempfile.TemporaryDirectory() as d:
        for name, text in FIXTURES.items():
            with open(os.path.join(d, name), 'w') as f: f.write(text)
        with contextlib.redirect_stdout(out):
            # one walk over every fixture, as on a real repo: helpers.ts feeds f.test.ts
            walk([os.path.join(d, name) for name in FIXTURES])
            src = os.path.join(d, 'proj', 'src'); os.makedirs(src)
            for name, text in INLINE_RS.items():
                with open(os.path.join(src, name), 'w') as f: f.write(text)
            walk([os.path.join(d, 'proj')])
    lines = out.getvalue().splitlines()
    fails = 0
    for f, name, flag in EXPECT:
        ok = any(f in l and f'  {name}  ' in l and flag in l.split('  ')[-1].split() for l in lines)
        print(('PASS ' if ok else 'FAIL ') + f'{flag} on {f} {name!r}'); fails += not ok
    for f, name in CLEAN:
        ok = not any(f in l and f'  {name}  ' in l for l in lines)
        print(('PASS ' if ok else 'FAIL ') + f'no flag on clean test {f} {name!r}'); fails += not ok
    print(f'{fails} failed' if fails else 'selftest ok')
    return 1 if fails else 0


if __name__ == '__main__':
    if sys.argv[1:2] in (['-h'], ['--help']): print(__doc__); sys.exit(0)
    if sys.argv[1:] == ['--selftest']: sys.exit(selftest())
    walk(sys.argv[1:])
