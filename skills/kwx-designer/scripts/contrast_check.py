#!/usr/bin/env python3
"""Contrast of foreground colours against a background, WCAG 2.2 and APCA.

    contrast_check.py <bg> <fg> [<fg> ...]
    contrast_check.py "#0E0F0E" "#C8FE23" "#8A8F86" "rgba(255,255,255,0.6)"
    contrast_check.py --surface <bg> <fill> [<fill> ...]
    contrast_check.py --selftest

Colours: #rgb, #rrggbb, #rrggbbaa, rgb()/rgba(). A translucent foreground is
blended over the background first, which is what the screen shows.

Prints per foreground: the WCAG ratio with AA/AAA verdicts for body text,
large text (24px, or 18.7px bold) and UI parts (3:1), and the APCA Lc value
(the newer perceptual measure; |Lc| 75 body, 60 large/fluent text, 45 large
headings, 30 non-text, 15 the floor for anything visible).

--surface: does a filled control (a pill, a button, a well) separate from the
surface it sits on? Prints the largest per channel sRGB difference, the OKLCH
lightness difference (information only), and VANISHES when the largest channel
difference is under 10, else "separates". A labelled control's fill needs this
separation, not WCAG 1.4.11 3:1 (that applies when the boundary alone identifies
the control); its label still needs 4.5:1, so run the normal mode on the label.
"""
import re
import sys


def parse(c):
    c = c.strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{3,8})", c)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h)
        if len(h) not in (6, 8):
            raise ValueError(f"bad hex colour: {c}")
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return [int(h[i:i + 2], 16) for i in (0, 2, 4)], a
    m = re.fullmatch(r"rgba?\(([^)]*)\)", c.replace(" ", ""))
    if m:
        parts = m.group(1).split(",")
        if len(parts) not in (3, 4):
            raise ValueError(f"bad rgb colour: {c}")
        return [int(float(p)) for p in parts[:3]], float(parts[3]) if len(parts) == 4 else 1.0
    raise ValueError(f"unknown colour format: {c} (use #rrggbb or rgba())")


def blend(fg, a, bg):
    return [round(f * a + b * (1 - a)) for f, b in zip(fg, bg)]


def wcag_lum(rgb):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = map(ch, rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def wcag_ratio(a, b):
    la, lb = sorted((wcag_lum(a), wcag_lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def apca_lc(text, bg):
    """APCA 0.0.98G-4g, the constants published by Myndex."""
    def y(rgb):
        r, g, b = ((v / 255) ** 2.4 for v in rgb)
        v = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
        return v if v > 0.022 else v + (0.022 - v) ** 1.414
    yt, yb = y(text), y(bg)
    if abs(yb - yt) < 0.0005:
        return 0.0
    if yb > yt:  # dark text on light background
        s = (yb ** 0.56 - yt ** 0.57) * 1.14
        return 0.0 if s < 0.1 else (s - 0.027) * 100
    s = (yb ** 0.65 - yt ** 0.62) * 1.14
    return 0.0 if s > -0.1 else (s + 0.027) * 100


SURFACE_MIN = 10  # per channel; the user's rule from mistakes library M4 (#050506 on #000000)


def oklch_l(rgb):
    """OKLab lightness L (0 to 1) of an sRGB colour."""
    def lin(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = map(lin, rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (x ** (1 / 3) for x in (l, m, s))
    return 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_


def surface(bg_s, fill_s):
    """(max channel difference, OKLCH L difference, verdict) of a fill on its surface."""
    bg, bga = parse(bg_s)
    if bga < 1:
        raise ValueError("the surface must be opaque; blend it over what is behind it first")
    fill, a = parse(fill_s)
    shown = blend(fill, a, bg)
    delta = max(abs(f - b) for f, b in zip(shown, bg))
    dl = abs(oklch_l(shown) - oklch_l(bg))
    return delta, dl, "VANISHES" if delta < SURFACE_MIN else "separates"


def surface_report(bg_s, fill_s):
    delta, dl, verdict = surface(bg_s, fill_s)
    return (f"{fill_s:>24} on {bg_s}: max channel difference {delta:3d}  "
            f"OKLCH L difference {dl:.3f}  {verdict}")


def report(bg_s, fg_s):
    bg, bga = parse(bg_s)
    if bga < 1:
        raise ValueError("the background must be opaque; blend it over what is behind it first")
    fg, a = parse(fg_s)
    shown = blend(fg, a, bg)
    r = wcag_ratio(shown, bg)
    lc = apca_lc(shown, bg)
    ok = lambda x: "pass" if x else "FAIL"
    return (f"{fg_s:>24} on {bg_s}: {r:5.2f}:1  body AA {ok(r >= 4.5)} AAA {ok(r >= 7)}  "
            f"large AA {ok(r >= 3)}  UI {ok(r >= 3)}  APCA Lc {lc:6.1f}"
            f" ({'body ok' if abs(lc) >= 75 else 'large only' if abs(lc) >= 60 else 'headings only' if abs(lc) >= 45 else 'not for text'})")


def selftest():
    assert abs(wcag_ratio([0, 0, 0], [255, 255, 255]) - 21) < 0.01
    assert abs(wcag_ratio([119, 119, 119], [255, 255, 255]) - 4.48) < 0.01
    assert abs(apca_lc([0, 0, 0], [255, 255, 255]) - 106.0) < 0.5
    assert abs(apca_lc([255, 255, 255], [0, 0, 0]) + 107.9) < 0.5
    assert blend([255, 255, 255], 0.5, [0, 0, 0]) == [128, 128, 128]
    assert parse("#fff") == ([255, 255, 255], 1.0)
    assert surface("#000000", "#050506")[2] == "VANISHES"
    assert surface("#000000", "#161618")[2] == "separates"
    assert surface("#000000", "rgba(255,255,255,0.02)")[2] == "VANISHES"
    print("selftest ok")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--selftest"]:
        selftest()
    elif args and args[0] == "--surface":
        if len(args) < 3:
            sys.exit(__doc__)
        try:
            for fill in args[2:]:
                print(surface_report(args[1], fill))
        except ValueError as e:
            sys.exit(f"error: {e}")
    elif len(args) < 2:
        sys.exit(__doc__)
    else:
        try:
            for fg in args[1:]:
                print(report(args[0], fg))
        except ValueError as e:
            sys.exit(f"error: {e}")
