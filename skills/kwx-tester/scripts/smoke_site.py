#!/usr/bin/env python3
"""Browserless smoke test for a static or server rendered site.
Usage: python3 -I smoke_site.py http://localhost:4173 / /about/ /pricing/
Checks each page's status, head tags and links, then robots.txt and a 404.
Run `python3 -I smoke_site.py --selftest` to check the script itself (no network, no browser)."""
import sys, urllib.request, urllib.error, urllib.parse
from html.parser import HTMLParser

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None; self.title = ""; self.in_title = False
        self.meta = {}; self.links = []; self.h1 = 0; self.imgs_no_alt = []
        self.canonical = None; self.ids = set(); self.viewport = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        if tag == "html": self.lang = a.get("lang")
        elif tag == "title": self.in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key: self.meta[key] = a.get("content", "")
            if a.get("name") == "viewport": self.viewport = True
        elif tag == "link" and a.get("rel") == "canonical": self.canonical = a.get("href")
        elif tag == "a" and a.get("href"): self.links.append(a["href"])
        elif tag == "h1": self.h1 += 1
        elif tag == "img" and "alt" not in a: self.imgs_no_alt.append(a.get("src"))
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.title += data

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "smoke-test"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, r.headers.get("content-type", ""), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("content-type", ""), ""

def main(base, paths):
    problems, checked = [], {}
    def status(url):
        if url not in checked: checked[url] = fetch(url)[0]
        return checked[url]
    for path in paths:
        url = urllib.parse.urljoin(base, path)
        code, ctype, body = fetch(url)
        if code != 200 or "text/html" not in ctype:
            problems.append(f"{path}: status {code}, content-type {ctype!r}"); continue
        p = Page(); p.feed(body)
        need = {"lang on <html>": p.lang, "<title>": p.title.strip(), "meta viewport": p.viewport,
                "meta description": p.meta.get("description"), "canonical": p.canonical,
                "og:title": p.meta.get("og:title"), "og:image": p.meta.get("og:image")}
        problems += [f"{path}: missing {k}" for k, v in need.items() if not v]
        if p.h1 != 1: problems.append(f"{path}: {p.h1} <h1> elements (expected 1)")
        problems += [f"{path}: <img src={s}> has no alt" for s in p.imgs_no_alt]
        if "localhost" in (p.canonical or "") + p.meta.get("og:image", ""):
            problems.append(f"{path}: canonical or og:image points at localhost")
        for href in p.links:
            if href.startswith("#"):
                if href[1:] and href[1:] not in p.ids: problems.append(f"{path}: anchor {href} has no target id")
                continue
            target = urllib.parse.urljoin(url, href)
            if urllib.parse.urlparse(target).netloc != urllib.parse.urlparse(base).netloc: continue  # external: use lychee
            if status(target.split("#")[0]) != 200: problems.append(f"{path}: link {href} -> {checked[target.split('#')[0]]}")
    if status(urllib.parse.urljoin(base, "/robots.txt")) != 200: problems.append("robots.txt missing")
    if status(urllib.parse.urljoin(base, "/this-page-does-not-exist-404-check")) != 404:
        problems.append("unknown path does not return 404 (soft 404)")
    for line in problems: print("FAIL", line)
    print(f"{len(paths)} pages, {len(checked)} extra URLs checked, {len(problems)} problems")
    return 1 if problems else 0

def selftest():
    """Serve a tiny broken site from a temp dir and check the expected problems are found."""
    import tempfile, threading, functools, http.server, os, io, contextlib
    good = ('<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width">'
            '<title>T</title><meta name="description" content="d"><link rel="canonical" href="https://x.test/">'
            '<meta property="og:title" content="T"><meta property="og:image" content="https://x.test/o.png"></head>'
            '<body><h1>T</h1><a href="/about/">ok</a><a href="/gone.html">bad</a><a href="#nope">bad</a><img src="a.png"></body></html>')
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(f"{d}/about"); open(f"{d}/index.html", "w").write(good)
        open(f"{d}/about/index.html", "w").write("<html><title>A</title><h1>A</h1></html>"); open(f"{d}/robots.txt", "w").write("")
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *args): pass
        handler = functools.partial(Quiet, directory=d)
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        out = io.StringIO()
        with contextlib.redirect_stdout(out): code = main(f"http://127.0.0.1:{srv.server_address[1]}", ["/", "/about/"])
        srv.shutdown()
    text = out.getvalue()
    for expected in ["link /gone.html -> 404", "anchor #nope", "has no alt", "/about/: missing lang", "/about/: missing og:image"]:
        assert expected in text, f"selftest: expected {expected!r} in:\n{text}"
    assert code == 1 and "soft 404" not in text and "robots.txt missing" not in text, text
    print("selftest ok")

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]: sys.exit(selftest())
    if sys.argv[1:2] in (["--help"], ["-h"]): print(__doc__); sys.exit(0)
    if len(sys.argv) < 3: sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2:]))
