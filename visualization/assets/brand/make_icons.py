"""Generate the GFL icon set in the visual language of the mark (make_logo.py).

Same grammar as the logo: dark rounded tile, white nodes (filled circles) joined by
thin edges; outlines drawn 1.5x thicker. Every icon is defined below as plain
geometry on a 24x24 grid (no third-party artwork, no stock image, no image
generator); the output is fully reproducible from this file.

    python visualization/assets/brand/make_icons.py visualization/assets/brand/icons
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

BG, FG = "#0b0f14", "#ffffff"


def ring(cx, cy, r, n, start=90.0):
    return [(cx + r * math.cos(math.radians(start + 360 * i / n)),
             cy - r * math.sin(math.radians(start + 360 * i / n))) for i in range(n)]


def closed(points):
    return list(zip(points, points[1:] + points[:1]))


def chain(points):
    return list(zip(points, points[1:]))


# Each icon: outlines (edge list drawn thick), edges (thin), nodes (filled circles).
def icons():
    out = {}

    box = [(5, 9), (19, 9), (19, 20), (5, 20)]
    out["ingest"] = dict(
        outlines=closed(box), edges=[((12, 2), (12, 13)), ((8.5, 9.5), (12, 13)), ((15.5, 9.5), (12, 13))],
        nodes=[(12, 2), (12, 13), *box])

    hexa = ring(12, 12, 8.5, 6, 90)
    out["seal"] = dict(outlines=closed(hexa), edges=[(p, (12, 12)) for p in hexa[::2]],
                       nodes=[*hexa, (12, 12)])

    blocks, edges, nodes = [], [], []
    for i in range(3):
        x = 2 + i * 7.6
        sq = [(x, 9), (x + 5.2, 9), (x + 5.2, 14.2), (x, 14.2)]
        blocks += closed(sq)
        edges.append(((x, 14.2), (x + 5.2, 9)))
        nodes += sq
        if i < 2:
            blocks.append(((x + 5.2, 11.6), (x + 7.6, 11.6)))
    out["ledger"] = dict(outlines=blocks, edges=edges, nodes=nodes)

    head = ring(8, 12, 4.2, 8, 0)
    out["key"] = dict(outlines=closed(head) + [((12.2, 12), (21, 12))],
                      edges=[((17, 12), (17, 15.5)), ((20, 12), (20, 15))],
                      nodes=[*head[::2], (12.2, 12), (17, 15.5), (20, 15), (21, 12)])

    clock = ring(12, 12, 8.5, 12, 90)
    out["timestamp"] = dict(outlines=closed(clock), edges=[((12, 12), (12, 6)), ((12, 12), (16.5, 14.5))],
                            nodes=[*clock[::3], (12, 12), (12, 6), (16.5, 14.5)])

    circ = ring(12, 12, 9, 12, 90)
    check = [(7.5, 12.5), (10.8, 15.8), (16.8, 8.5)]
    out["verified"] = dict(outlines=closed(circ) + chain(check), edges=[],
                           nodes=[*circ[::3], *check])

    out["altered"] = dict(outlines=[((2.5, 12), (8.5, 12)), ((15.5, 12), (21.5, 12))],
                          edges=[((10, 9), (14, 15)), ((14, 9), (10, 15))],
                          nodes=[(2.5, 12), (8.5, 12), (15.5, 12), (21.5, 12)])

    dash = ring(12, 12, 8, 12, 90)
    out["missing"] = dict(outlines=[(dash[i], dash[i + 1]) for i in range(0, 12, 2)],
                          edges=[((12, 8.5), (12, 13)), ], nodes=[(12, 8.5), (12, 13), (12, 16)])

    tree = {"a": (12, 3.5), "b": (6, 11), "c": (18, 11), "d": (3.5, 19.5), "e": (9.5, 19.5), "f": (18, 19.5)}
    out["lineage"] = dict(outlines=[], edges=[(tree["a"], tree["b"]), (tree["a"], tree["c"]), (tree["b"], tree["d"]),
                                             (tree["b"], tree["e"]), (tree["c"], tree["f"]), (tree["e"], tree["f"])],
                          nodes=list(tree.values()))

    flag = [(6, 4), (19, 7.5), (6, 12)]
    out["qualifier"] = dict(outlines=[((6, 3), (6, 21))] + chain(flag), edges=[((6, 8), (19, 7.5))],
                            nodes=[(6, 3), (6, 21), *flag])

    fl = [(9, 20), (5.5, 15), (7, 9.5), (10, 4), (13, 9.5), (14.5, 15), (12.5, 20)]
    out["flame_front"] = dict(outlines=chain(fl) + [((12.5, 20), (9, 20)), ((19, 3), (19, 21))],
                              edges=[((7, 9.5), (13, 9.5)), ((5.5, 15), (14.5, 15)), ((10, 4), (10, 20))],
                              nodes=[*fl, (19, 3), (19, 21)])

    out["spread_rate"] = dict(outlines=[((3, 20), (21, 20)), ((3, 20), (3, 3))],
                              edges=[((5, 17), (10, 13.5)), ((10, 13.5), (15, 9.5)), ((15, 9.5), (19.5, 6))],
                              nodes=[(5, 17), (10, 13.5), (15, 9.5), (19.5, 6), (3, 20), (21, 20), (3, 3)])

    cam = [(3, 7), (21, 7), (21, 19), (3, 19)]
    lens = ring(12, 13, 4, 8, 90)
    out["frame"] = dict(outlines=closed(cam) + closed(lens) + [((8, 7), (9.5, 4.5)), ((9.5, 4.5), (14.5, 4.5)),
                                                               ((14.5, 4.5), (16, 7))],
                        edges=[], nodes=[*cam, *lens[::2]])

    grid = [(x, y) for y in (5, 12, 19) for x in (5, 12, 19)]
    out["dataset"] = dict(outlines=[], edges=[(grid[i], grid[i + 1]) for i in (0, 1, 3, 4, 6, 7)]
                          + [(grid[i], grid[i + 3]) for i in range(6)], nodes=grid)

    t1, t2 = ring(12, 12, 9, 12, 90), ring(12, 12, 4.5, 6, 90)
    out["red_team"] = dict(outlines=closed(t1) + closed(t2),
                           edges=[((12, 1.5), (12, 7.5)), ((12, 16.5), (12, 22.5)), ((1.5, 12), (7.5, 12)),
                                  ((16.5, 12), (22.5, 12))], nodes=[(12, 12), *t1[::3]])

    mag = ring(10, 10, 6, 10, 90)
    out["auditor"] = dict(outlines=closed(mag) + [((14.3, 14.3), (21, 21))], edges=[(mag[0], mag[5]), (mag[2], mag[7])],
                          nodes=[*mag[::2], (21, 21)])

    tri = [(5, 4), (19, 12), (5, 20)]
    out["validator"] = dict(outlines=closed(tri), edges=[((5, 12), (19, 12)), ((5, 4), (12, 16)), ((5, 20), (12, 8))],
                            nodes=[*tri, (5, 12), (12, 8), (12, 16)])

    bars = [(5, 13, 4), (12, 9, 5.5), (19, 11, 3)]
    e, n = [], []
    for x, y, d in bars:
        e += [((x, y - d), (x, y + d)), ((x - 1.8, y - d), (x + 1.8, y - d)), ((x - 1.8, y + d), (x + 1.8, y + d))]
        n.append((x, y))
    out["uncertainty"] = dict(outlines=[], edges=e + [(n[0], n[1]), (n[1], n[2])], nodes=n)

    sh = [(12, 2.5), (20, 6), (19, 14), (12, 21.5), (5, 14), (4, 6)]
    tick = [(8.5, 12), (11, 14.5), (15.8, 9)]
    out["approval"] = dict(outlines=closed(sh) + chain(tick), edges=[], nodes=[*sh, *tick])

    ag = ring(12, 12, 8.5, 6, 0)
    out["ai_agent"] = dict(outlines=closed(ag), edges=[(p, (12, 12)) for p in ag] + [(ag[0], ag[3])][:0],
                           nodes=[*ag, (12, 12)])

    out["source"] = dict(outlines=[((5, 5), (19, 5)), ((5, 5), (5, 19)), ((19, 5), (19, 19)), ((5, 19), (19, 19)),
                                   ((5, 10), (19, 10)), ((5, 14.5), (19, 14.5))], edges=[],
                         nodes=[(5, 5), (19, 5), (5, 10), (19, 10), (5, 14.5), (19, 14.5), (5, 19), (19, 19)])

    db = [(4, 20), (4, 13), (10, 20), (10, 8), (16, 20), (16, 11), (21, 20), (21, 4)]
    out["dashboard"] = dict(outlines=[((3, 20), (21.5, 20))] + [(db[i], db[i + 1]) for i in range(0, 8, 2)],
                            edges=[(db[1], db[3]), (db[3], db[5]), (db[5], db[7])], nodes=db[1::2])
    return out


def build(spec, size=256, bg=BG, fg=FG) -> str:
    pad, s = size * 0.2, size * 0.6 / 24
    t = lambda p: (pad + p[0] * s, pad + p[1] * s)
    sw, r = size * 0.012, size * 0.022
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">',
         f'<rect width="{size}" height="{size}" rx="{size * 0.22:.1f}" fill="{bg}"/>']
    for kind, width, op in (("outlines", sw * 1.5, 1.0), ("edges", sw, 0.8)):
        for a, b in spec[kind]:
            (x1, y1), (x2, y2) = t(a), t(b)
            o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{fg}" '
                     f'stroke-width="{width:.2f}" stroke-opacity="{op}" stroke-linecap="round"/>')
    o += [f'<circle cx="{t(p)[0]:.1f}" cy="{t(p)[1]:.1f}" r="{r:.2f}" fill="{fg}"/>' for p in spec["nodes"]]
    return "\n".join(o + ["</svg>"]) + "\n"


def main() -> int:
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for name, spec in icons().items():
        (out / f"{name}.svg").write_text(build(spec), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
