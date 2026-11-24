"""Hand-drawn SVG scenes, one per story. Each returns an <svg> string
with viewBox 0 0 240 140 so every layout can scale it freely."""

import math


def _svg(body, bg):
    return (
        '<svg viewBox="0 0 240 140" xmlns="http://www.w3.org/2000/svg" '
        'preserveAspectRatio="xMidYMid slice">'
        f'<rect width="240" height="140" fill="{bg}"/>{body}</svg>'
    )


def smoke(x, y, s=1.0, c="#5b5b66"):
    """A rising plume of three overlapping puffs."""
    puffs = [(0, 0, 9), (6, -12, 12), (16, -26, 15), (30, -38, 17)]
    return "".join(
        f'<circle cx="{x + dx * s:.1f}" cy="{y + dy * s:.1f}" r="{r * s:.1f}" '
        f'fill="{c}" opacity="{0.85 - i * 0.12:.2f}"/>'
        for i, (dx, dy, r) in enumerate(puffs)
    )


def flame(x, y, s=1.0):
    """Teardrop flame: red outer, orange middle, yellow core."""
    def drop(w, h, col):
        return (
            f'<path d="M{x},{y - h * s} C{x + w * s},{y - h * 0.45 * s} '
            f'{x + w * s},{y} {x},{y} C{x - w * s},{y} {x - w * s},'
            f'{y - h * 0.45 * s} {x},{y - h * s}Z" fill="{col}"/>'
        )
    return drop(11, 30, "#d7261e") + drop(7.5, 21, "#f77f00") + drop(4, 12, "#ffd23f")


def cop31():
    """Empty summit stage, COP31 banner, a red NO DEAL stamp, smokestacks."""
    b = []
    # far skyline: smokestacks puffing (the fossil-fuel subtext)
    for x in (22, 206):
        b.append(f'<rect x="{x}" y="58" width="12" height="52" fill="#8a8f98"/>')
        b.append(smoke(x + 6, 52, 0.9, "#a7abb3"))
    # stage
    b.append('<rect x="0" y="100" width="240" height="40" fill="#2f4858"/>')
    b.append('<rect x="44" y="30" width="152" height="34" rx="3" fill="#1d6fa3"/>')
    b.append('<text x="120" y="54" font-family="Bahnschrift,Arial" font-weight="700" '
             'font-size="20" fill="#fff" text-anchor="middle">COP31</text>')
    b.append('<text x="120" y="40" font-family="Arial" font-size="6.5" fill="#cfe6f5" '
             'text-anchor="middle">UN CLIMATE CHANGE CONFERENCE · TÜRKİYE</text>')
    # long empty table with empty chairs
    b.append('<rect x="30" y="86" width="180" height="8" fill="#d9c7a3"/>')
    b.append('<rect x="30" y="94" width="180" height="14" fill="#b89c6c"/>')
    for i in range(7):
        cx = 44 + i * 25
        b.append(f'<rect x="{cx}" y="70" width="12" height="16" rx="2" fill="#6b4f3a"/>')
        b.append(f'<rect x="{cx + 3}" y="88" width="6" height="3" fill="#eee"/>')
    # stamp
    b.append('<g transform="rotate(-12 120 92)">'
             '<rect x="72" y="76" width="96" height="30" rx="4" fill="none" '
             'stroke="#d7261e" stroke-width="4"/>'
             '<text x="120" y="99" font-family="Arial Black,Arial" font-weight="900" '
             'font-size="19" fill="#d7261e" text-anchor="middle">NO DEAL</text></g>')
    return _svg("".join(b), "#e6edf2")


def warship():
    """Grey corvette listing and sinking beside a port quay, smoke, a drone wake."""
    b = []
    b.append('<rect x="0" y="0" width="240" height="78" fill="#f2c18d"/>')  # dawn sky
    b.append('<rect x="150" y="62" width="90" height="18" fill="#8d7a63"/>')  # quay
    b.append('<rect x="200" y="22" width="5" height="42" fill="#5a4a3a"/>')  # crane
    b.append('<rect x="176" y="22" width="40" height="4" fill="#5a4a3a"/>')
    b.append('<rect x="0" y="78" width="240" height="62" fill="#2c6e8f"/>')  # sea
    # ship, tilted and half under
    b.append('<g transform="rotate(14 100 88)">'
             '<path d="M40,80 L160,80 L150,98 L52,98Z" fill="#6c7680"/>'
             '<rect x="82" y="62" width="40" height="18" fill="#7f8a94"/>'
             '<rect x="96" y="48" width="10" height="14" fill="#7f8a94"/>'
             '<rect x="70" y="72" width="10" height="3" fill="#59616a"/>'
             '<rect x="130" y="70" width="18" height="3" fill="#59616a"/></g>')
    b.append('<rect x="0" y="96" width="240" height="44" fill="#2c6e8f" opacity="0.92"/>')
    for y in (104, 116, 128):
        b.append(f'<path d="M0,{y} q15,-5 30,0 t30,0 t30,0 t30,0 t30,0 t30,0 t30,0 t30,0" '
                 'fill="none" stroke="#5fa3c4" stroke-width="1.5"/>')
    b.append(flame(112, 76, 0.8))
    b.append(smoke(112, 52, 1.0, "#3f3f46"))
    # sea drone and its wake
    b.append('<path d="M8,122 L44,112" stroke="#e8f4fa" stroke-width="2" stroke-dasharray="4 3"/>')
    b.append('<path d="M44,108 l12,2 l-12,4z" fill="#222"/>')
    return _svg("".join(b), "#f2c18d")


def hormuz():
    """Tanker ablaze in a narrow strait between two coasts."""
    b = []
    b.append('<rect x="0" y="0" width="240" height="140" fill="#3a7ca5"/>')
    b.append('<path d="M0,0 L240,0 L240,30 C190,44 140,26 90,40 C50,50 20,36 0,44Z" fill="#d9b382"/>')
    b.append('<path d="M0,140 L240,140 L240,112 C200,100 160,122 110,108 C60,96 30,116 0,104Z" fill="#c9a06c"/>')
    b.append('<text x="214" y="30" font-family="Arial" font-weight="700" font-size="12" fill="#4a3519" text-anchor="middle">IRAN</text>')
    b.append('<text x="36" y="126" font-family="Arial" font-weight="700" font-size="12" fill="#4a3519" text-anchor="middle">OMAN</text>')
    # tanker
    b.append('<path d="M60,78 L178,78 L170,92 L68,92Z" fill="#8c2f2f"/>')
    b.append('<rect x="60" y="72" width="118" height="6" fill="#4a4a4a"/>')
    b.append('<rect x="152" y="58" width="20" height="14" fill="#f0f0f0"/>')
    b.append('<rect x="158" y="50" width="6" height="8" fill="#333"/>')
    for x in (80, 100, 120):
        b.append(f'<rect x="{x}" y="68" width="12" height="4" fill="#666"/>')
    b.append(flame(98, 72, 1.0))
    b.append(smoke(98, 40, 1.15, "#2b2b2b"))
    # second struck ship in the distance
    b.append('<path d="M188,56 L222,56 L219,61 L191,61Z" fill="#555"/>')
    b.append(smoke(205, 50, 0.45, "#444"))
    return _svg("".join(b), "#3a7ca5")


def gaza():
    """A burnt-out aid truck with spilled flour sacks among rubble."""
    b = []
    b.append('<rect x="0" y="0" width="240" height="100" fill="#cfc6b8"/>')
    # ruined buildings
    b.append('<path d="M0,100 L0,40 L30,40 L30,30 L52,30 L52,58 L60,52 L60,100Z" fill="#a39a8c"/>')
    b.append('<path d="M180,100 L180,48 L196,36 L214,50 L214,26 L240,26 L240,100Z" fill="#a39a8c"/>')
    for x, y in ((8, 50), (36, 40), (188, 60), (220, 36), (222, 60)):
        b.append(f'<rect x="{x}" y="{y}" width="8" height="8" fill="#6f675c"/>')
    b.append('<rect x="0" y="100" width="240" height="40" fill="#b5a68f"/>')
    # truck
    b.append('<rect x="70" y="58" width="80" height="40" fill="#3d3a36"/>')
    b.append('<rect x="150" y="70" width="28" height="28" fill="#2e2b28"/>')
    b.append('<rect x="156" y="74" width="16" height="10" fill="#1a1a1a"/>')
    b.append('<text x="110" y="84" font-family="Arial Black,Arial" font-weight="900" font-size="15" '
             'fill="#9a948a" text-anchor="middle">AID</text>')
    for x in (88, 132, 166):
        b.append(f'<circle cx="{x}" cy="100" r="9" fill="#1e1e1e"/>')
    # flour sacks
    for x, y in ((40, 112), (54, 116), (186, 114), (200, 110), (196, 122)):
        b.append(f'<rect x="{x}" y="{y}" width="16" height="11" rx="3" fill="#f3efe6" stroke="#bdb5a4"/>')
    b.append(smoke(112, 50, 1.0, "#4a4743"))
    return _svg("".join(b), "#cfc6b8")


def house():
    """US House hemicycle: 259 Democratic seats, 3 uncalled, the rest Republican."""
    b = []
    seats, rows = 435, 10
    r0, r1 = 50, 104
    radii = [r0 + (r1 - r0) * i / (rows - 1) for i in range(rows)]
    total_len = sum(radii)
    counts = [round(seats * r / total_len) for r in radii]
    counts[-1] += seats - sum(counts)
    pts = []
    for r, n in zip(radii, counts):
        for k in range(n):
            a = math.pi * (k + 0.5) / n
            pts.append((a, r))
    pts.sort(key=lambda p: (-p[0], p[1]))  # left to right across the arc
    cx, cy = 120, 118
    for i, (a, r) in enumerate(pts):
        col = "#2563c9" if i < 259 else ("#b8b8b8" if i < 262 else "#d63a3a")
        x, y = cx + r * math.cos(a), cy - r * math.sin(a)
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{col}"/>')
    b.append('<text x="120" y="98" font-family="Bahnschrift,Arial" font-weight="700" '
             'font-size="28" fill="#2563c9" text-anchor="middle">259</text>')
    b.append('<text x="120" y="108" font-family="Arial" font-weight="700" font-size="9" fill="#2563c9" '
             'text-anchor="middle">OF 435 SEATS</text>')
    b.append('<text x="120" y="118" font-family="Arial" font-weight="700" font-size="7.5" fill="#b02a2a" '
             'text-anchor="middle">REP 173 · 3 OPEN</text>')
    return _svg("".join(b), "#f4f1ea")


def factory():
    """Sawtooth-roof factory in flames, firefighters' hose arc."""
    b = []
    b.append('<rect x="0" y="0" width="240" height="140" fill="#2b2d42"/>')  # night
    b.append('<rect x="0" y="112" width="240" height="28" fill="#3d3d3d"/>')
    b.append('<path d="M40,112 L40,64 L70,46 L70,64 L100,46 L100,64 L130,46 L130,64 L160,46 '
             'L160,64 L190,46 L190,112Z" fill="#7a6a5a"/>')
    for x in (52, 82, 112, 142, 172):
        b.append(f'<rect x="{x}" y="80" width="12" height="14" fill="#ffb347"/>')
    for x, s in ((70, 1.3), (110, 1.6), (150, 1.25)):
        b.append(flame(x, 64, s))
    b.append(smoke(112, 18, 1.0, "#55556a"))
    # fire truck + water arc
    b.append('<rect x="196" y="98" width="40" height="14" fill="#c62828"/>')
    b.append('<path d="M206,98 Q190,60 160,72" fill="none" stroke="#9fd3ff" stroke-width="2.2"/>')
    return _svg("".join(b), "#2b2d42")


def protest():
    """Crowd of students with placards."""
    b = ['<rect x="0" y="0" width="240" height="140" fill="#fde9c9"/>']
    for i in range(12):
        x = 12 + i * 19
        y = 96 + (i % 3) * 6
        b.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#5b4636"/>')
        b.append(f'<rect x="{x - 8}" y="{y + 7}" width="16" height="40" rx="6" fill="#{["e63946", "457b9d", "2a9d8f", "f4a261"][i % 4]}"/>')
    for (x, w), label in zip(((26, 64), (150, 64)), ("ROMA", "PARIS")):
        b.append(f'<rect x="{x + w / 2 - 1}" y="52" width="2" height="34" fill="#6b4f3a"/>')
        b.append(f'<rect x="{x}" y="34" width="{w}" height="22" fill="#fff" stroke="#333"/>')
        b.append(f'<text x="{x + w / 2}" y="49" font-family="Arial Black,Arial" font-weight="900" '
                 f'font-size="10" fill="#c8102e" text-anchor="middle">{label}</text>')
    return _svg("".join(b), "#fde9c9")


def zanzibar():
    """Beach hotels burning behind palm trees, tourists on the sand."""
    b = ['<rect x="0" y="0" width="240" height="140" fill="#ffd6a5"/>']
    b.append('<rect x="0" y="92" width="240" height="20" fill="#2a9d8f"/>')
    b.append('<rect x="0" y="108" width="240" height="32" fill="#f1dca7"/>')
    for i in range(6):
        x = 16 + i * 36
        b.append(f'<rect x="{x}" y="62" width="30" height="34" fill="#f7f3ea" stroke="#b9a98c"/>')
        b.append(f'<path d="M{x - 3},64 L{x + 15},50 L{x + 33},64Z" fill="#9c6b3c"/>')
        for wx in (x + 5, x + 18):
            b.append(f'<rect x="{wx}" y="72" width="7" height="8" fill="#ff9f1c"/>')
        b.append(flame(x + 15, 54, 0.6 + 0.12 * (i % 2)))
    b.append(smoke(100, 18, 0.9, "#6c6c74"))
    for x in (10, 236):
        b.append(f'<rect x="{x - 2}" y="70" width="4" height="40" fill="#7a5230"/>')
        b.append(f'<path d="M{x},70 q-16,-2 -20,8 M{x},70 q16,-2 20,8 M{x},70 q-6,-14 -18,-12 M{x},70 q6,-14 18,-12" '
                 'stroke="#2d6a4f" stroke-width="4" fill="none"/>')
    for x in (60, 72, 150, 162, 174):
        b.append(f'<circle cx="{x}" cy="116" r="3.2" fill="#5b4636"/>')
        b.append(f'<rect x="{x - 3}" y="119" width="6" height="11" rx="2" fill="#457b9d"/>')
    return _svg("".join(b), "#ffd6a5")


SCENES = {
    "zanzibar": zanzibar,
    "cop31": cop31,
    "warship": warship,
    "hormuz": hormuz,
    "gaza": gaza,
    "house": house,
    "factory": factory,
    "protest": protest,
}
