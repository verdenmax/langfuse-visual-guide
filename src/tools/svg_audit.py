#!/usr/bin/env python3
"""Heuristic SVG label-overflow / tiny-font auditor.

The existing viewBox-bounds checker only verifies element ANCHOR coordinates
sit inside the viewBox; it cannot see that a long <text> label visually spills
past its containing <rect> or past the right edge of the viewBox. This tool
estimates rendered text width (CJK glyph approx = font-size px, latin approx =
0.55 x font-size) and flags:

  * box-overflow : text horizontal extent exceeds its smallest containing rect
  * canvas-overflow: text horizontal extent exceeds the viewBox width
  * tiny-cjk     : font-size < MIN_FONT and the text contains CJK glyphs

Run from src/:  python3 tools/svg_audit.py [--verbose]
Exit code is always 0 (advisory); parse the printed summary counts.
"""
import glob
import html
import os
import re
import sys

MIN_FONT = 6.5          # CJK below this is unreadable on a 720-wide viewBox
PAD = 6.0               # assumed inner padding of a box before text "touches" the edge
TOL = 2.0               # ignore sub-pixel overshoot

_SVG = re.compile(r'<svg viewBox="0 0 ([\d.]+) ([\d.]+)"(.*?)</svg>', re.S)
_RECT = re.compile(r'<rect x="(-?[\d.]+)" y="(-?[\d.]+)" width="([\d.]+)" height="([\d.]+)"')
_TEXT = re.compile(
    r'<text x="(-?[\d.]+)" y="(-?[\d.]+)"([^>]*)>(.*?)</text>', re.S)


def _is_cjk(ch):
    return '\u3000' <= ch <= '\u9fff' or '\uff00' <= ch <= '\uffef'


def _text_width(s, fs):
    w = 0.0
    for ch in s:
        if _is_cjk(ch):
            w += fs
        elif ch == ' ':
            w += fs * 0.3
        else:
            w += fs * 0.55
    return w


def _attr(attrs, name, default=None):
    m = re.search(name + r'="([^"]*)"', attrs)
    return m.group(1) if m else default


def audit_file(path):
    h = open(path, encoding='utf-8').read()
    findings = []  # (kind, label, detail)
    for sm in _SVG.finditer(h):
        W = float(sm.group(1))
        body = sm.group(3)
        rects = [tuple(map(float, r.groups())) for r in _RECT.finditer(body)]
        for tm in _TEXT.finditer(body):
            tx, ty = float(tm.group(1)), float(tm.group(2))
            attrs = tm.group(3)
            raw = re.sub(r'<[^>]+>', '', tm.group(4))
            label = html.unescape(raw).strip()
            if not label:
                continue
            fs = float(_attr(attrs, 'font-size', '12') or 12)
            anchor = _attr(attrs, 'text-anchor', 'start')
            tw = _text_width(label, fs)
            if anchor == 'middle':
                left, right = tx - tw / 2, tx + tw / 2
            elif anchor == 'end':
                left, right = tx - tw, tx
            else:
                left, right = tx, tx + tw

            # tiny CJK
            if fs < MIN_FONT and any(_is_cjk(c) for c in label):
                findings.append(('tiny-cjk', label, f'{fs}px'))

            # canvas overflow
            if right > W + TOL or left < -TOL:
                findings.append(('canvas-overflow', label,
                                 f'extent[{left:.0f},{right:.0f}] vb_w={W:.0f}'))
                continue  # canvas overflow dominates; skip box check

            # smallest containing rect (anchor point inside)
            best = None
            for (rx, ry, rw, rh) in rects:
                if rx - TOL <= tx <= rx + rw + TOL and ry - TOL <= ty <= ry + rh + TOL:
                    area = rw * rh
                    if best is None or area < best[4]:
                        best = (rx, ry, rw, rh, area)
            if best:
                rx, ry, rw, rh, _ = best
                inner_l, inner_r = rx + PAD, rx + rw - PAD
                over = max(0.0, right - inner_r) + max(0.0, inner_l - left)
                if over > TOL:
                    findings.append(('box-overflow', label,
                                     f'+{over:.0f}px past {rw:.0f}px box'))
    return findings


def main():
    verbose = '--verbose' in sys.argv
    # tool lives at <repo>/src/tools/svg_audit.py; lessons/ is at <repo>/lessons
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(repo_root)
    counts = {'box-overflow': 0, 'canvas-overflow': 0, 'tiny-cjk': 0}
    per_file = []
    for path in sorted(glob.glob('lessons/*.html')):
        fs = audit_file(path)
        if not fs:
            continue
        for kind, label, detail in fs:
            counts[kind] += 1
        per_file.append((path, fs))

    for path, fs in per_file:
        hot = [f for f in fs if f[0] != 'tiny-cjk']
        if hot or verbose:
            print(f'\n{os.path.basename(path)}')
            for kind, label, detail in fs:
                if kind == 'tiny-cjk' and not verbose:
                    continue
                print(f'  [{kind}] {label[:48]!r}  {detail}')

    print('\n=== SUMMARY ===')
    print(f"box-overflow    : {counts['box-overflow']}")
    print(f"canvas-overflow : {counts['canvas-overflow']}")
    print(f"tiny-cjk(<{MIN_FONT}) : {counts['tiny-cjk']}")


if __name__ == '__main__':
    main()
