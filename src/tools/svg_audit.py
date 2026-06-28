#!/usr/bin/env python3
"""Heuristic SVG label-overflow / tiny-font auditor.

The existing viewBox-bounds checker only verifies element ANCHOR coordinates
sit inside the viewBox; it cannot see that a long <text> label visually spills
past its containing <rect> or past the right edge of the viewBox. This tool
estimates rendered text width (CJK glyph approx = font-size px, latin approx =
0.55 x font-size) and flags:

  * box-overflow : text horizontal extent crosses its smallest containing
                   <rect> border (real overflow, TOL px heuristic slack)
  * canvas-overflow: text horizontal extent exceeds the viewBox width
  * tiny-cjk     : font-size < MIN_FONT and the text contains CJK glyphs

Width is estimated conservatively (CJK glyph = font-size px, latin = 0.55 x,
space = 0.3 x); inheritance of font-size / text-anchor from wrapping <g>
groups is resolved so labels are measured at their true rendered size.

Run from src/:  python3 tools/svg_audit.py [--verbose]
Exit code is non-zero if any box-overflow / canvas-overflow / tiny-cjk is found
(so it gates CI); the printed summary lists the per-kind counts.
"""
import glob
import html
import os
import re
import sys

MIN_FONT = 6.5          # CJK below this is unreadable on a 720-wide viewBox
TOL = 2.0               # heuristic slack: ignore sub-glyph width-estimate error

_SVG = re.compile(r'<svg viewBox="0 0 ([\d.]+) ([\d.]+)"(.*?)</svg>', re.S)
_RECT = re.compile(r'<rect x="(-?[\d.]+)" y="(-?[\d.]+)" width="([\d.]+)" height="([\d.]+)"')


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
        # Walk the body in order, tracking <g> font-size / text-anchor so <text>
        # inherits them (many older diagrams set these once on a wrapping group).
        gstack = []  # list of (font_size_or_None, anchor_or_None)
        for tok in re.finditer(r'<g\b([^>]*)>|</g>|<text x="(-?[\d.]+)" y="(-?[\d.]+)"([^>]*)>(.*?)</text>', body, re.S):
            if tok.group(0) == '</g>':
                if gstack:
                    gstack.pop()
                continue
            if tok.group(0).startswith('<g'):
                gattr = tok.group(1)
                gstack.append((_attr(gattr, 'font-size'), _attr(gattr, 'text-anchor')))
                continue
            # a <text>
            tx, ty = float(tok.group(2)), float(tok.group(3))
            attrs = tok.group(4)
            raw = re.sub(r'<[^>]+>', '', tok.group(5))
            label = html.unescape(raw).strip()
            if not label:
                continue
            inh_fs = next((fs for fs, _ in reversed(gstack) if fs), None)
            inh_an = next((an for _, an in reversed(gstack) if an), None)
            fs = float(_attr(attrs, 'font-size', inh_fs or '12') or '12')
            anchor = _attr(attrs, 'text-anchor', inh_an or 'start')
            tw = _text_width(label, fs)
            if anchor == 'middle':
                left, right = tx - tw / 2, tx + tw / 2
            elif anchor == 'end':
                left, right = tx - tw, tx
            else:
                left, right = tx, tx + tw

            if fs < MIN_FONT and any(_is_cjk(c) for c in label):
                findings.append(('tiny-cjk', label, f'{fs}px'))

            if right > W + TOL or left < -TOL:
                findings.append(('canvas-overflow', label,
                                 f'extent[{left:.0f},{right:.0f}] vb_w={W:.0f}'))
                continue

            # Canvas-top titles (y<=24) are centered captions over the whole
            # diagram, not labels meant to fit one box; canvas-overflow above
            # already guards them against spilling off the page.
            if ty <= 24:
                continue
            # Smallest <rect> whose body contains the text anchor.
            best = None
            for (rx, ry, rw, rh) in rects:
                if rx - TOL <= tx <= rx + rw + TOL and ry - TOL <= ty <= ry + rh + TOL:
                    area = rw * rh
                    if best is None or area < best[4]:
                        best = (rx, ry, rw, rh, area)
            if best:
                rx, ry, rw, rh, _ = best
                # Real overflow = text extent crossing the actual rect border.
                over = max(0.0, right - (rx + rw)) + max(0.0, rx - left)
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
    # Gate: non-zero exit if any real overflow or undersized CJK is found,
    # so CI fails instead of silently passing.
    return 1 if (counts['box-overflow'] or counts['canvas-overflow'] or counts['tiny-cjk']) else 0


if __name__ == '__main__':
    sys.exit(main())
