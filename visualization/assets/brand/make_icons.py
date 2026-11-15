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
    out.update(more_icons())
    return out


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def arc(cx, cy, r, a0, a1, n):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / (n - 1))),
             cy - r * math.sin(math.radians(a0 + (a1 - a0) * i / (n - 1)))) for i in range(n)]


def more_icons():
    """Coverage for every GFL function (ledger, vault, science modules, roles, states)."""
    o = {}
    # --- ledger and evidence ---------------------------------------------------------
    head = ring(7, 15, 3.6, 8, 0)
    crown = [(8, 9), (9.5, 3.5), (12, 6.5), (14.5, 3.5), (16, 9)]
    o["owner_key"] = dict(outlines=closed(head) + [((10.6, 15), (21, 15))] + chain(crown) + [((16, 9), (8, 9))],
                          edges=[((17, 15), (17, 18.5)), ((20, 15), (20, 18))],
                          nodes=[*head[::2], (21, 15), (17, 18.5), (20, 18), *crown])
    o["anchor_git"] = dict(outlines=[((7, 3), (7, 21))], edges=[((7, 15), (17, 8)), ],
                           nodes=[(7, 3), (7, 9), (7, 15), (7, 21), (17, 8)])
    o["derivation"] = dict(outlines=closed(rect(9, 8, 15, 16)),
                           edges=[((2.5, 12), (9, 12)), ((15, 12), (21.5, 12)), ((9, 16), (15, 8))],
                           nodes=[(2.5, 12), (21.5, 12), *rect(9, 8, 15, 16)])
    o["supersession"] = dict(outlines=closed(rect(3, 4, 11, 12)) + closed(rect(13, 12, 21, 20)),
                             edges=[((3, 12), (11, 4)), ((11, 8), (17, 8)), ((17, 8), (17, 12))],
                             nodes=[*rect(3, 4, 11, 12), *rect(13, 12, 21, 20), (17, 8)])
    o["chain_of_custody"] = dict(outlines=closed(rect(2, 9, 7, 15)) + closed(rect(17, 9, 22, 15)),
                                 edges=[((7, 12), (17, 12)), ((12, 12), (12, 5))],
                                 nodes=[*rect(2, 9, 7, 15), *rect(17, 9, 22, 15), (12, 12), (12, 5)])
    # --- vault -----------------------------------------------------------------------
    safe = rect(3, 4, 21, 20)
    dial = ring(12, 12, 4, 8, 90)
    o["evidence_vault"] = dict(outlines=closed(safe) + closed(dial),
                               edges=[((12, 12), dial[0]), ((12, 12), dial[3]), ((12, 12), dial[5])],
                               nodes=[*safe, *dial[::2], (12, 12)])
    cube_f = rect(4, 9, 15, 20)
    cube_b = [(9, 4), (20, 4), (20, 15)]
    o["black_box"] = dict(outlines=closed(cube_f) + [((4, 9), (9, 4)), ((9, 4), (20, 4)), ((15, 9), (20, 4)),
                                                    ((20, 4), (20, 15)), ((15, 20), (20, 15))],
                          edges=[((4, 20), (15, 9)), ((4, 9), (15, 20))],
                          nodes=[*cube_f, *cube_b, (9.5, 14.5)])
    o["worm"] = dict(outlines=closed(rect(5, 11, 19, 20)) + chain(arc(12, 11, 4.5, 0, 180, 6)),
                     edges=[((12, 2.5), (12, 8)), ((10, 6), (12, 8)), ((14, 6), (12, 8)), ((12, 14), (12, 17))],
                     nodes=[*rect(5, 11, 19, 20), (12, 2.5), (12, 14), (12, 17)])
    # --- science modules -------------------------------------------------------------
    flask = [(9.5, 3), (9.5, 9), (4, 20), (20, 20), (14.5, 9), (14.5, 3)]
    o["experiment"] = dict(outlines=chain(flask) + [((8, 3), (16, 3))], edges=[((6.5, 15), (17.5, 15))],
                           nodes=[*flask, (6.5, 15), (17.5, 15), (11, 17.5), (13.5, 16.5)])
    o["comparison"] = dict(outlines=[((7, 3), (7, 21)), ((17, 3), (17, 21))],
                           edges=[((7, 7), (17, 9)), ((7, 12), (17, 12)), ((7, 17), (17, 15))],
                           nodes=[(7, 3), (7, 7), (7, 12), (7, 17), (7, 21), (17, 3), (17, 9), (17, 12), (17, 15),
                                  (17, 21)])
    c1, c2 = ring(9, 12, 6, 10, 90), ring(15, 12, 6, 10, 90)
    o["similarity"] = dict(outlines=closed(c1) + closed(c2), edges=[((12, 7), (12, 17))],
                           nodes=[*c1[::2], *c2[::2], (12, 12)])
    o["synthesis"] = dict(outlines=closed(rect(13, 6, 21, 18)),
                          edges=[((3, 4), (13, 9)), ((3, 12), (13, 12)), ((3, 20), (13, 15)),
                                 ((15, 10), (19, 10)), ((15, 13), (19, 13))],
                          nodes=[(3, 4), (3, 12), (3, 20), *rect(13, 6, 21, 18)])
    o["transferability"] = dict(outlines=closed(rect(2, 8, 8, 16)) + closed(ring(18, 12, 4, 8, 90)),
                                edges=[((8, 12), (14, 12)), ((11.5, 9.5), (14, 12)), ((11.5, 14.5), (14, 12))],
                                nodes=[*rect(2, 8, 8, 16), *ring(18, 12, 4, 8, 90)[::2]])
    series = [(2.5, 15), (6, 14), (9, 15.5), (11.5, 4), (14, 15), (17.5, 14), (21.5, 15)]
    o["anomaly"] = dict(outlines=chain(series), edges=[((11.5, 4), (11.5, 20))], nodes=series)
    bulb = ring(12, 17, 3.5, 8, 90)
    o["thermo"] = dict(outlines=closed(bulb) + [((10, 14), (10, 4)), ((14, 14), (14, 4)), ((10, 4), (14, 4))],
                       edges=[((12, 17), (12, 7)), ((14, 8), (17, 8)), ((14, 11), (17, 11))],
                       nodes=[*bulb[::2], (12, 17), (12, 7), (10, 4), (14, 4)])
    o["regime"] = dict(outlines=[((3, 21), (21, 21)), ((3, 21), (3, 3))] + chain([(3, 15), (9, 13), (13, 8), (14, 3)])
                       + chain([(9, 13), (21, 17)]), edges=[],
                       nodes=[(3, 15), (9, 13), (13, 8), (14, 3), (21, 17), (8, 7), (17, 10), (12, 18)])
    loop = [(12 + 7 * math.sin(math.radians(t)), 12 + 4.5 * math.sin(math.radians(2 * t))) for t in range(0, 360, 30)]
    o["nonlinear"] = dict(outlines=closed(loop), edges=[], nodes=loop[::2])
    orbit = ring(12, 12, 9, 14, 90)
    o["microgravity"] = dict(outlines=closed(ring(12, 12, 3.5, 8, 90)),
                             edges=[(orbit[i], orbit[i + 1]) for i in range(0, 14, 2)],
                             nodes=[orbit[2], *ring(12, 12, 3.5, 8, 90)[::2]])
    ap = ring(12, 12, 8.5, 6, 0)
    o["exposure"] = dict(outlines=closed(ap), edges=[(ap[i], ap[(i + 2) % 6]) for i in range(6)], nodes=ap)
    o["scale"] = dict(outlines=closed(rect(2, 9, 22, 15)),
                      edges=[((x, 9), (x, 12 if x % 4 else 13)) for x in range(4, 22, 2)],
                      nodes=rect(2, 9, 22, 15))
    # --- process, roles, states ------------------------------------------------------
    o["pm"] = dict(outlines=closed(rect(5, 4, 19, 21)) + closed(rect(9, 2.5, 15, 5.5)),
                   edges=[((8, 10), (16, 10)), ((8, 14), (16, 14)), ((8, 18), (13, 18))],
                   nodes=[*rect(5, 4, 19, 21), (8, 10), (8, 14), (8, 18)])
    hd = ring(12, 7.5, 3.5, 8, 90)
    o["human"] = dict(outlines=closed(hd) + chain([(4.5, 21), (6, 15.5), (12, 13), (18, 15.5), (19.5, 21)]), edges=[],
                      nodes=[*hd[::2], (4.5, 21), (12, 13), (19.5, 21)])
    o["decision"] = dict(outlines=closed(rect(4, 3, 17, 21)),
                         edges=[((7, 8), (14, 8)), ((7, 12), (14, 12)), ((13, 18), (16, 21)), ((16, 21), (21, 14))],
                         nodes=[*rect(4, 3, 17, 21), (21, 14), (16, 21)])
    tri = [(12, 3), (21.5, 20), (2.5, 20)]
    o["issue"] = dict(outlines=closed(tri), edges=[((12, 9), (12, 14.5))], nodes=[*tri, (12, 9), (12, 17.5)])
    bl = ring(12, 9.5, 6, 10, 90)
    o["idea"] = dict(outlines=closed(bl) + [((9.5, 18), (14.5, 18)), ((10, 21), (14, 21))],
                     edges=[((9.5, 15), (9.5, 18)), ((14.5, 15), (14.5, 18)), ((12, 6.5), (12, 12))],
                     nodes=[*bl[::2], (9.5, 18), (14.5, 18), (12, 12)])
    sr = ring(10, 10, 6, 10, 90)
    o["search"] = dict(outlines=closed(sr) + [((14.3, 14.3), (21, 21))], edges=[], nodes=[*sr[::2], (21, 21)])
    o["export"] = dict(outlines=chain([(4, 14), (4, 20), (20, 20), (20, 14)]),
                       edges=[((12, 3), (12, 15)), ((8, 11), (12, 15)), ((16, 11), (12, 15))],
                       nodes=[(4, 14), (4, 20), (20, 20), (20, 14), (12, 3), (12, 15)])
    rr = arc(12, 12, 8, 30, 330, 11)
    o["reproducible"] = dict(outlines=chain(rr), edges=[(rr[-1], (16.5, 21)), (rr[-1], (20.5, 14.5))],
                             nodes=rr[::2] + [rr[-1]])
    o["code"] = dict(outlines=chain([(8, 6), (2.5, 12), (8, 18)]) + chain([(16, 6), (21.5, 12), (16, 18)]),
                     edges=[((14, 4), (10, 20))], nodes=[(8, 6), (2.5, 12), (8, 18), (16, 6), (21.5, 12), (16, 18)])
    spokes = ring(12, 12, 8.5, 4, 45)
    o["orchestrator"] = dict(outlines=closed(ring(12, 12, 3, 6, 90)),
                             edges=[((12, 12), p) for p in spokes] + closed(spokes),
                             nodes=[*spokes, (12, 12)])
    steps = [(3, 12), (9, 12), (15, 12), (21, 12)]
    o["pipeline"] = dict(outlines=chain(steps), edges=[((15, 8), (15, 16))], nodes=steps)
    eye = arc(12, 18, 10, 30, 150, 7) + arc(12, 6, 10, 210, 330, 7)
    o["blind"] = dict(outlines=closed(eye), edges=[((4, 20), (20, 4))], nodes=[(12, 12), eye[0], eye[6]])
    o["established"] = dict(outlines=[((3, 12), (21, 12))], edges=[], nodes=[(3, 12), (21, 12)])
    o["provisional"] = dict(outlines=[], edges=[((3, 12), (21, 12))], nodes=[(3, 12), (21, 12), (12, 12)])
    o["unresolved"] = dict(outlines=[((3, 12), (6.5, 12)), ((9.5, 12), (14.5, 12)), ((17.5, 12), (21, 12))],
                           edges=[], nodes=[(3, 12), (21, 12)])
    q = arc(12, 8.5, 5, 160, -60, 7)
    o["unknown"] = dict(outlines=chain(q) + [(q[-1], (12, 15))], edges=[], nodes=[q[0], (12, 15), (12, 20)])
    o["info"] = dict(outlines=closed(ring(12, 12, 9, 12, 90)), edges=[((12, 10.5), (12, 17.5))],
                     nodes=[(12, 7), (12, 10.5), (12, 17.5)])
    return o


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
    (out / "light").mkdir(exist_ok=True)
    for name, spec in icons().items():
        (out / f"{name}.svg").write_text(build(spec), encoding="utf-8")
        # Light variant for documents (same geometry, inverted colours, as the mark).
        (out / "light" / f"{name}.svg").write_text(build(spec, bg=FG, fg=BG), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
