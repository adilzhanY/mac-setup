#!/usr/bin/env python3
"""Post deploy smoke test driven by a checks file. No browser, standard library only.

Usage: python3 -I smoke_checks.py <base url> <checks file>
       python3 -I smoke_checks.py --selftest      prove it on a local test server (no network)
Each line of the checks file is "path expected_status [text that must appear in the body]".
Blank lines and lines starting with # are skipped. Example:
    /                200 Sign in
    /api/health      200 "ok":true
    /no-such-page    404
Output: "ok   path status seconds" or "FAIL path: reason" per line. Exit 1 if any check failed.
Redirects are followed, so the status is the final one."""
import sys, time, urllib.error, urllib.request


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "smoke-checks"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError) as e:
        return 0, str(e)


def run(base, lines):
    base, fail = base.rstrip("/"), 0
    for raw in lines:
        parts = raw.strip().split(None, 2)
        if not parts or parts[0].startswith("#"): continue
        path, want, text = parts[0], (parts[1] if len(parts) > 1 else "200"), (parts[2] if len(parts) > 2 else "")
        t0 = time.monotonic()
        code, body = fetch(base + path)
        t = time.monotonic() - t0
        if str(code) != want: print(f"FAIL {path}: status {code}, want {want}"); fail = 1
        elif text and text not in body: print(f"FAIL {path}: text '{text}' missing"); fail = 1
        else: print(f"ok   {path} {code} {t:.2f}s")
    return fail


def selftest():
    import contextlib, functools, http.server, io, os, tempfile, threading
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "index.html"), "w") as f: f.write("<h1>Sign in</h1>")
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *args): pass
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=d))
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{srv.server_address[1]}"
        cases = [
            ("passing checks exit 0", ["# comment", "", "/ 200 Sign in", "/missing 404"], 0, []),
            ("wrong status is caught", ["/missing 200"], 1, ["FAIL /missing: status 404, want 200"]),
            ("missing text is caught", ["/ 200 Pricing"], 1, ["FAIL /: text 'Pricing' missing"]),
        ]
        fails = 0
        for name, lines, want_code, want_out in cases:
            out = io.StringIO()
            with contextlib.redirect_stdout(out): code = run(base, lines)
            ok = code == want_code and all(w in out.getvalue() for w in want_out)
            print(("PASS " if ok else "FAIL ") + name + ("" if ok else f" -> {code} {out.getvalue()!r}"))
            fails += not ok
        srv.shutdown()
    print(f"{fails} failed" if fails else "selftest ok")
    return 1 if fails else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]: sys.exit(selftest())
    if sys.argv[1:2] in (["--help"], ["-h"]): print(__doc__); sys.exit(0)
    if len(sys.argv) != 3: print(__doc__); sys.exit(2)
    with open(sys.argv[2]) as f: sys.exit(run(sys.argv[1], f))
