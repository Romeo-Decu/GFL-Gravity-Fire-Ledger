"""Generate the GFL mark: a node-network flame resting on three hash-linked ledger blocks.

Original geometry, authored here (no third-party artwork, no stock image, no AI
image generator): the flame outline is a closed parametric curve, nodes are
sampled on two nested outlines plus a core, edges are the Delaunay
triangulation kept inside the outline.  The output is fully reproducible from
this file (fixed parameters, no randomness).

Reading of the mark: nodes = evidence values, edges = verified links (graph);
blocks = ledger entries, the thick link = hash chain.

    python visualization/assets/brand/make_logo.py <out_dir>
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from matplotlib.path import Path as MPath
from scipy.spatial import Delaunay

BG, FG = "#0b0f14", "#ffffff"


def outline(n: int, scale: float = 1.0) -> np.ndarray:
    """Flame outline: round base, pointed leaning tip.  Half-width w(h) = 1.55*h^0.55*(1-h)^1.25,
    centre line c(h) = 0.38*h^2.2, h in [0,1] (height 2.2).  n nodes equally spaced by arc length."""
    h = np.linspace(0, 1, 400)
    w = 1.55 * h ** 0.55 * (1 - h) ** 1.25
    c = 0.38 * h ** 2.2
    y = 2.2 * h
    poly = np.r_[np.c_[c + w, y], np.c_[c - w, y][::-1][1:-1]]
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(np.r_[poly, poly[:1]], axis=0).T))]
    k = np.searchsorted(d, np.linspace(0, d[-1], n, endpoint=False))
    k[0] = 0
    tip = int(np.argmax(poly[:, 1]))
    k[np.argmin(abs(k - tip))] = tip                            # always keep the tip as a node
    pts = poly[np.unique(k)]
    m = np.array([0.04, 0.75])
    return (pts - m) * scale + m


def flame_nodes():
    return [outline(20), outline(11, 0.55) + [0.02, -0.08], np.array([[0.05, 0.62]])]


def place(rings, box):
    allp = np.vstack(rings)
    lo, hi = allp.min(0), allp.max(0)
    sc = min(box[2] / (hi - lo)[0], box[3] / (hi - lo)[1])
    off = np.array(box[:2]) + (np.array(box[2:]) - (hi - lo) * sc) / 2
    out = []
    for r in rings:
        p = (r - lo) * sc + off
        p[:, 1] = 2 * box[1] + box[3] - p[:, 1]                 # SVG y grows downward
        out.append(p)
    return out


def flame_svg(rings, sw, r, fg):
    pts = np.vstack(rings)
    outer = MPath(rings[0])
    edges = set()
    for t in Delaunay(pts).simplices:
        if outer.contains_point(pts[t].mean(0)):
            for a, b in ((t[0], t[1]), (t[1], t[2]), (t[0], t[2])):
                edges.add((min(a, b), max(a, b)))
    poly = " L".join(f"{x:.1f},{y:.1f}" for x, y in rings[0])
    o = [f'<path d="M{poly} Z" fill="none" stroke="{fg}" stroke-width="{sw * 1.5:.2f}" stroke-linejoin="round"/>']
    o += [f'<line x1="{pts[a][0]:.1f}" y1="{pts[a][1]:.1f}" x2="{pts[b][0]:.1f}" y2="{pts[b][1]:.1f}" '
          f'stroke="{fg}" stroke-width="{sw:.2f}" stroke-opacity="0.8"/>' for a, b in sorted(edges)]
    o += [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{fg}"/>' for x, y in pts]
    return o


def chain_svg(cx, y, w, sw, r, fg):
    s = w / 3.6
    gap = s * 0.3
    x0 = cx - (3 * s + 2 * gap) / 2
    o = []
    for i in range(3):
        x = x0 + i * (s + gap)
        o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}" rx="{s * 0.08:.1f}" fill="none" stroke="{fg}" stroke-width="{sw * 1.5:.2f}"/>')
        o.append(f'<line x1="{x:.1f}" y1="{y + s:.1f}" x2="{x + s:.1f}" y2="{y:.1f}" stroke="{fg}" stroke-width="{sw:.2f}" stroke-opacity="0.8"/>')
        o += [f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.2f}" fill="{fg}"/>'
              for px, py in ((x, y), (x + s, y), (x, y + s), (x + s, y + s))]
        if i < 2:
            o.append(f'<line x1="{x + s:.1f}" y1="{y + s / 2:.1f}" x2="{x + s + gap:.1f}" y2="{y + s / 2:.1f}" stroke="{fg}" stroke-width="{sw * 2.4:.2f}"/>')
    return o


def build(size=512, chain=True, simple=False, bg=BG, fg=FG) -> str:
    sw, r = (6.0, 10.0) if simple else (2.4, 5.0)
    rings = [outline(9), np.array([[0.05, 0.62]])] if simple else flame_nodes()
    box = (size * 0.27, size * 0.10, size * 0.46, size * (0.54 if chain else 0.78))
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">',
         '<title>Gravity Fire Ledger</title>',
         f'<rect width="{size}" height="{size}" rx="{size * 0.22:.0f}" fill="{bg}"/>']
    o += flame_svg(place(rings, box), sw, r, fg)
    if chain:
        o += chain_svg(size / 2, size * 0.72, size * 0.5, sw, r, fg)
    return "\n".join(o + ["</svg>"]) + "\n"


VARIANTS = {"GFL_mark_full.svg": {}, "GFL_mark_flame.svg": {"chain": False},
            "GFL_mark_simple.svg": {"simple": True},
            "GFL_mark_full_inverted.svg": {"bg": "#ffffff", "fg": "#0b0f14"}}


def main() -> int:
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for name, kw in VARIANTS.items():
        (out / name).write_text(build(**kw), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
