"""Wide banner scenes (viewBox 0 0 240 90) for story cards, one per kind of
event, all hand-drawn SVG. banner(kind, text=None) returns an <svg> string;
`text` puts a big scoreboard-style figure in the corner (a score, a toll)."""

from scenes import flame, smoke

W, H = 240, 90


def _svg(body, sky, text=None):
    tag = ""
    if text:
        w = 14 + 9.5 * len(text)
        tag = (f'<rect x="{W - w - 8}" y="8" width="{w}" height="24" rx="3" fill="#111"/>'
               f'<text x="{W - 8 - w / 2}" y="26" font-family="Bahnschrift,Arial" font-weight="700" '
               f'font-size="18" fill="#ffd23f" text-anchor="middle">{text}</text>')
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
            f'preserveAspectRatio="xMidYMid slice"><rect width="{W}" height="{H}" fill="{sky}"/>'
            f'{body}{tag}</svg>')


def _ground(col, y=72):
    return f'<rect x="0" y="{y}" width="{W}" height="{H - y}" fill="{col}"/>'


def _city(col="#5d6b7d", y=72, seed=3):
    out = []
    x = 0
    k = seed
    while x < W:
        k = (k * 7 + 3) % 11
        w, h = 14 + k * 2, 18 + k * 3
        out.append(f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{col}"/>')
        for wy in range(y - h + 5, y - 4, 8):
            out.append(f'<rect x="{x + 4}" y="{wy}" width="3" height="3" fill="#ffe08a" opacity=".7"/>')
        x += w + 2
    return "".join(out)


def fire(text=None):
    b = [_ground("#3a3a3a"), '<rect x="60" y="40" width="120" height="32" fill="#7a6a5a"/>',
         '<path d="M60,40 L80,28 L80,40 L100,28 L100,40 L120,28 L120,40 L140,28 L140,40 L160,28 L160,40 L180,28 L180,40Z" fill="#6b5b4b"/>']
    for x in (70, 98, 128, 156):
        b.append(f'<rect x="{x}" y="52" width="12" height="10" fill="#ffb347"/>')
    for x, s in ((84, 0.9), (120, 1.15), (158, 0.85)):
        b.append(flame(x, 34, s))
    b.append(smoke(118, 8, 0.6, "#55556a"))
    return _svg("".join(b), "#2b2d42", text)


def ship(text=None):
    b = ['<rect x="0" y="56" width="240" height="34" fill="#2c6e8f"/>',
         '<path d="M50,52 L180,52 L170,66 L60,66Z" fill="#8c2f2f"/>',
         '<rect x="50" y="46" width="130" height="6" fill="#4a4a4a"/>',
         '<rect x="152" y="32" width="20" height="14" fill="#f0f0f0"/>']
    b.append(flame(96, 46, 0.8))
    b.append(smoke(96, 22, 0.7, "#2b2b2b"))
    for y in (74, 84):
        b.append(f'<path d="M0,{y} q15,-4 30,0 t30,0 t30,0 t30,0 t30,0 t30,0 t30,0 t30,0" fill="none" stroke="#5fa3c4" stroke-width="1.4"/>')
    return _svg("".join(b), "#f2c18d", text)


def strike(text=None):
    b = [_city("#6f675c"), _ground("#a39a8c")]
    b.append('<circle cx="130" cy="44" r="26" fill="#f77f00" opacity=".55"/>')
    b.append(flame(130, 64, 1.1))
    b.append(smoke(126, 18, 0.75, "#3f3f46"))
    return _svg("".join(b), "#cfc6b8", text)


def drone(text=None):
    b = [_city("#2e3a59", seed=5), _ground("#1d2433")]
    for x, y in ((40, 18), (92, 12), (150, 22), (200, 10)):
        b.append(f'<path d="M{x - 9},{y} L{x + 9},{y} M{x},{y - 4} L{x},{y + 4}" stroke="#ccd" stroke-width="2"/>'
                 f'<path d="M{x + 2},{y + 3} L{x - 14},{y + 22}" stroke="#ffb347" stroke-width="1.2" stroke-dasharray="2 2"/>')
    b.append(flame(120, 66, 0.8))
    return _svg("".join(b), "#141b2d", text)


def ballot(text=None):
    b = [_ground("#c9d6e3", 70), '<rect x="86" y="34" width="68" height="40" rx="3" fill="#1d4e89"/>',
         '<rect x="104" y="30" width="32" height="5" fill="#0d2c54"/>',
         '<rect x="108" y="10" width="24" height="28" fill="#fff" stroke="#888"/>',
         '<path d="M113,24 l5,6 l10,-12" stroke="#2a9d8f" stroke-width="3" fill="none"/>',
         '<text x="120" y="62" font-family="Arial" font-weight="700" font-size="11" fill="#fff" text-anchor="middle">VOTE</text>']
    return _svg("".join(b), "#e8f0f7", text)


def protest(text=None):
    b = [_ground("#e3cfa8", 76)]
    for i in range(13):
        x = 10 + i * 18
        y = 56 + (i % 3) * 4
        b.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#5b4636"/>')
        b.append(f'<rect x="{x - 7}" y="{y + 6}" width="14" height="30" rx="5" fill="#{["e63946", "457b9d", "2a9d8f", "f4a261"][i % 4]}"/>')
    for x in (34, 112, 188):
        b.append(f'<rect x="{x}" y="34" width="2" height="22" fill="#6b4f3a"/>'
                 f'<rect x="{x - 18}" y="16" width="38" height="20" fill="#fff" stroke="#333"/>')
    return _svg("".join(b), "#fde9c9", text)


def court(text=None):
    b = [_ground("#d6cfc2", 74), '<path d="M60,30 L120,8 L180,30Z" fill="#b8ad99"/>',
         '<rect x="62" y="30" width="116" height="6" fill="#a39880"/>']
    for x in (70, 92, 114, 136, 158):
        b.append(f'<rect x="{x}" y="38" width="10" height="34" fill="#efe9dd"/>')
    b.append('<g transform="rotate(-30 196 50)"><rect x="180" y="44" width="32" height="12" rx="2" fill="#6b4f3a"/>'
             '<rect x="194" y="56" width="4" height="22" fill="#6b4f3a"/></g>')
    return _svg("".join(b), "#eef1f5", text)


def storm(text=None):
    b = [_city("#4a5568", seed=7), _ground("#2f5d7c", 74)]
    b.append('<ellipse cx="90" cy="16" rx="60" ry="14" fill="#5a6270"/><ellipse cx="170" cy="20" rx="54" ry="13" fill="#4b5260"/>')
    for x in range(20, 240, 14):
        b.append(f'<path d="M{x},30 l-6,16" stroke="#9fc5e8" stroke-width="1.6"/>')
    b.append('<path d="M150,28 l-10,18 h10 l-8,18" stroke="#ffd23f" stroke-width="3" fill="none"/>')
    return _svg("".join(b), "#8a94a6", text)


def quake(text=None):
    b = [_ground("#8d7a63", 70), '<path d="M0,70 L80,70 L96,56 L112,76 L130,60 L146,72 L240,70 L240,90 L0,90Z" fill="#6f5f4c"/>',
         '<g transform="rotate(8 70 50)"><rect x="50" y="30" width="40" height="40" fill="#bfb6a5"/></g>',
         '<g transform="rotate(-10 180 50)"><rect x="162" y="26" width="36" height="44" fill="#a9a08f"/></g>',
         '<path d="M104,70 l6,-12 l-6,-8 l8,-10" stroke="#3a2f24" stroke-width="2" fill="none"/>']
    return _svg("".join(b), "#e9e2d4", text)


def sport(text=None):
    b = ['<rect x="0" y="40" width="240" height="50" fill="#2f8f3a"/>',
         '<rect x="0" y="40" width="240" height="6" fill="#246f2d"/>',
         '<path d="M120,46 L120,90 M20,46 L20,90 M220,46 L220,90" stroke="#e8f5e9" stroke-width="1.5"/>',
         '<circle cx="120" cy="68" r="12" fill="none" stroke="#e8f5e9" stroke-width="1.5"/>']
    for i in range(12):
        b.append(f'<rect x="{i * 20}" y="{14 + (i % 2) * 4}" width="16" height="22" fill="#{["b23a48", "3d5a80", "e0e0e0"][i % 3]}" opacity=".8"/>')
    b.append('<path d="M108,24 h24 v6 a12,12 0 0 1 -24,0z M116,42 h8 v-6 h-8z" fill="#ffd23f"/>')
    return _svg("".join(b), "#20304a", text)


def market(text=None):
    b = [_ground("#1b2a3a", 0)]
    for y in (20, 40, 60):
        b.append(f'<path d="M10,{y} H230" stroke="#2f4357" stroke-width="1"/>')
    b.append('<path d="M10,24 L50,30 L80,22 L110,40 L140,36 L170,58 L200,54 L230,72" stroke="#ff5a5f" stroke-width="3" fill="none"/>')
    b.append('<path d="M222,64 L230,72 L218,74" stroke="#ff5a5f" stroke-width="3" fill="none"/>')
    return _svg("".join(b), "#1b2a3a", text)


def health(text=None):
    b = [_ground("#d9e2ec", 72), '<rect x="70" y="20" width="100" height="52" fill="#f7f9fb" stroke="#b8c4d0"/>',
         '<rect x="110" y="28" width="20" height="20" fill="#fff"/>',
         '<path d="M120,30 v16 M112,38 h16" stroke="#d62828" stroke-width="5"/>']
    for x in (80, 146):
        b.append(f'<rect x="{x}" y="54" width="14" height="10" fill="#9fc5e8"/>')
    return _svg("".join(b), "#e7eef5", text)


def plane(text=None):
    b = [_ground("#6b7280", 74), '<rect x="0" y="70" width="240" height="4" fill="#ffd23f" opacity=".7"/>',
         '<g transform="rotate(-12 120 40)"><path d="M60,40 L180,40 Q196,40 196,46 Q196,52 180,52 L60,52Z" fill="#f4f6fa"/>'
         '<path d="M110,46 L90,74 L104,74 L134,46Z M110,46 L96,20 L108,20 L134,46Z" fill="#cbd5e1"/>'
         '<path d="M64,40 L56,24 L68,24 L78,40Z" fill="#2563c9"/></g>']
    return _svg("".join(b), "#bcd7f0", text)


def diplomacy(text=None):
    b = [_ground("#5b3a29", 66), '<rect x="30" y="56" width="180" height="10" fill="#7a4e33"/>']
    for x, c in ((70, "#d62828"), (120, "#1d4e89"), (170, "#2a9d8f")):
        b.append(f'<rect x="{x}" y="14" width="2" height="42" fill="#555"/><rect x="{x + 2}" y="14" width="26" height="16" fill="{c}"/>')
    b.append('<path d="M96,60 q12,-10 24,0 q12,-10 24,0" stroke="#f1c27d" stroke-width="6" fill="none"/>')
    return _svg("".join(b), "#e8e1d6", text)


def government(text=None):
    b = [_ground("#c8c1b3", 74), '<rect x="60" y="34" width="120" height="40" fill="#efe9dd"/>',
         '<path d="M96,34 a24,22 0 0 1 48,0z" fill="#d9d1c2"/>', '<rect x="118" y="2" width="2" height="12" fill="#555"/>',
         '<rect x="120" y="2" width="14" height="8" fill="#c8102e"/>']
    for x in range(66, 180, 14):
        b.append(f'<rect x="{x}" y="42" width="6" height="30" fill="#d9d1c2"/>')
    return _svg("".join(b), "#dfe7ef", text)


def tech(text=None):
    b = [_ground("#0f2027", 0), '<rect x="90" y="16" width="60" height="58" rx="4" fill="#203a43" stroke="#5eead4"/>',
         '<rect x="104" y="30" width="32" height="30" fill="#2c5364"/>']
    for i in range(6):
        y = 22 + i * 9
        b.append(f'<path d="M70,{y} H90 M150,{y} H170" stroke="#5eead4" stroke-width="2"/>')
    return _svg("".join(b), "#0f2027", text)


def flood(text=None):
    b = [_city("#7a8796", y=60, seed=4), '<rect x="0" y="54" width="240" height="36" fill="#6b8fa8" opacity=".92"/>']
    for y in (64, 76):
        b.append(f'<path d="M0,{y} q15,-4 30,0 t30,0 t30,0 t30,0 t30,0 t30,0 t30,0 t30,0" fill="none" stroke="#cfe3f0" stroke-width="1.4"/>')
    b.append('<path d="M150,50 l14,-4 l2,10 l-14,4z" fill="#e76f51"/>')
    return _svg("".join(b), "#9aa8b8", text)


def climate(text=None):
    b = [_ground("#2f4858", 70)]
    for x in (30, 200):
        b.append(f'<rect x="{x}" y="30" width="12" height="40" fill="#8a8f98"/>' + smoke(x + 6, 26, 0.6, "#a7abb3"))
    b.append('<rect x="66" y="14" width="108" height="26" rx="3" fill="#1d6fa3"/>'
             '<text x="120" y="33" font-family="Bahnschrift,Arial" font-weight="700" font-size="15" fill="#fff" text-anchor="middle">COP31</text>')
    b.append('<g transform="rotate(-10 120 58)"><rect x="80" y="46" width="80" height="22" rx="3" fill="none" stroke="#d7261e" stroke-width="3"/>'
             '<text x="120" y="63" font-family="Arial Black,Arial" font-weight="900" font-size="14" fill="#d7261e" text-anchor="middle">NO DEAL</text></g>')
    return _svg("".join(b), "#e6edf2", text)


def aid(text=None):
    b = [_city("#a39a8c", seed=2), _ground("#b5a68f"),
         '<rect x="80" y="40" width="64" height="30" fill="#3d3a36"/><rect x="144" y="48" width="22" height="22" fill="#2e2b28"/>',
         '<text x="112" y="60" font-family="Arial Black,Arial" font-weight="900" font-size="12" fill="#9a948a" text-anchor="middle">AID</text>']
    for x in (94, 132, 156):
        b.append(f'<circle cx="{x}" cy="72" r="7" fill="#1e1e1e"/>')
    b.append(smoke(112, 30, 0.6, "#4a4743"))
    return _svg("".join(b), "#cfc6b8", text)


def police(text=None):
    b = [_city("#4b5563", seed=6), _ground("#374151"),
         '<rect x="80" y="54" width="70" height="18" rx="4" fill="#f4f6fa"/><rect x="96" y="44" width="38" height="12" rx="3" fill="#f4f6fa"/>',
         '<rect x="106" y="40" width="8" height="4" fill="#2563eb"/><rect x="116" y="40" width="8" height="4" fill="#dc2626"/>',
         '<circle cx="94" cy="72" r="6" fill="#111"/><circle cx="136" cy="72" r="6" fill="#111"/>']
    return _svg("".join(b), "#1f2937", text)


def space(text=None):
    b = [_ground("#0b1026", 0)]
    for x, y in ((20, 12), (60, 30), (200, 16), (170, 50), (40, 64), (220, 70)):
        b.append(f'<circle cx="{x}" cy="{y}" r="1.4" fill="#fff"/>')
    b.append('<path d="M120,10 q12,14 8,44 h-16 q-4,-30 8,-44z" fill="#e5e7eb"/><path d="M112,54 h16 l-8,20z" fill="#f77f00"/>')
    return _svg("".join(b), "#0b1026", text)


def rally(text=None):
    b = [_ground("#0f2a1d", 0)]
    for y in (20, 40, 60):
        b.append(f'<path d="M10,{y} H230" stroke="#1f4a33" stroke-width="1"/>')
    b.append('<path d="M10,76 L50,70 L80,74 L110,58 L140,62 L170,36 L200,40 L226,14" stroke="#34d399" stroke-width="3.5" fill="none"/>')
    b.append('<path d="M214,14 L228,12 L226,26" stroke="#34d399" stroke-width="3.5" fill="none"/>')
    return _svg("".join(b), "#0f2a1d", text)


def eu(text=None):
    import math
    b = [_ground("#c8c1b3", 76), '<rect x="70" y="8" width="2" height="68" fill="#555"/>',
         '<rect x="72" y="8" width="96" height="62" fill="#003399"/>']
    for k in range(12):
        a = math.pi * 2 * k / 12
        b.append(f'<circle cx="{120 + 20 * math.cos(a):.1f}" cy="{39 + 20 * math.sin(a):.1f}" r="2.6" fill="#ffcc00"/>')
    return _svg("".join(b), "#dfe7ef", text)


def nato(text=None):
    b = [_ground("#c8c1b3", 76), '<rect x="70" y="8" width="2" height="68" fill="#555"/>',
         '<rect x="72" y="8" width="96" height="62" fill="#004990"/>',
         '<path d="M120,18 L124,35 L141,39 L124,43 L120,60 L116,43 L99,39 L116,35Z" fill="#fff"/>',
         '<circle cx="120" cy="39" r="13" fill="none" stroke="#fff" stroke-width="1.5"/>']
    return _svg("".join(b), "#dfe7ef", text)


def podium(text=None):
    b = [_ground("#5b6b7d", 72), '<rect x="40" y="10" width="160" height="40" fill="#2c3e50"/>',
         '<rect x="96" y="44" width="48" height="30" fill="#7f8c8d"/><rect x="92" y="40" width="56" height="6" fill="#95a5a6"/>']
    for x in (108, 120, 132):
        b.append(f'<path d="M{x},40 L{x},28" stroke="#222" stroke-width="2"/><circle cx="{x}" cy="26" r="3.5" fill="#222"/>')
    return _svg("".join(b), "#bdc3c7", text)


def cricket(text=None):
    b = ['<rect x="0" y="34" width="240" height="56" fill="#3f9b47"/>',
         '<rect x="96" y="40" width="48" height="50" fill="#c9b37e"/>']
    for x in (112, 120, 128):
        b.append(f'<rect x="{x - 1.5}" y="40" width="3" height="22" fill="#f5f0e1"/>')
    b.append('<rect x="109" y="39" width="22" height="3" fill="#f5f0e1"/><circle cx="160" cy="60" r="4" fill="#b71c1c"/>')
    for i in range(12):
        b.append(f'<rect x="{i * 20}" y="{10 + (i % 2) * 4}" width="16" height="20" fill="#{["1e3a5f", "e0e0e0", "f4a261"][i % 3]}" opacity=".8"/>')
    return _svg("".join(b), "#20304a", text)


def union(text=None):
    b = [_ground("#6b7280", 76), '<rect x="20" y="12" width="200" height="34" fill="#9ca3af"/>',
         '<path d="M20,12 L60,2 L100,12 L140,2 L180,12 L220,2 L220,12Z" fill="#6b7280"/>']
    for i in range(12):
        x = 16 + i * 19
        b.append(f'<circle cx="{x}" cy="56" r="5.5" fill="#5b4636"/><rect x="{x - 6}" y="61" width="12" height="22" rx="4" fill="#d62828"/>')
    for x in (50, 150):
        b.append(f'<rect x="{x}" y="22" width="2" height="34" fill="#444"/><rect x="{x + 2}" y="22" width="30" height="18" fill="#d62828"/>')
    return _svg("".join(b), "#cbd5e1", text)


def sanctions(text=None):
    b = [_ground("#8d8a82", 76), '<path d="M50,30 L120,6 L190,30Z" fill="#d9d3c5"/><rect x="56" y="30" width="128" height="6" fill="#c9c2b0"/>']
    for x in (64, 88, 112, 136, 160):
        b.append(f'<rect x="{x}" y="38" width="12" height="36" fill="#efe9dd"/>')
    b.append('<rect x="50" y="74" width="140" height="6" fill="#c9c2b0"/>')
    b.append('<g transform="rotate(-8 120 48)"><rect x="76" y="34" width="88" height="26" rx="3" fill="#fff" stroke="#c62828" stroke-width="3"/>'
             '<text x="120" y="53" font-family="Arial Black,Arial" font-weight="900" font-size="15" fill="#c62828" text-anchor="middle">SWIFT X</text></g>')
    return _svg("".join(b), "#dfe7ef", text)


def warning(text=None):
    b = [_ground("#3b3b3b", 74), '<rect x="30" y="10" width="180" height="64" fill="#1f2a3a"/>']
    b.append('<rect x="100" y="42" width="40" height="32" fill="#7f8c8d"/><rect x="96" y="38" width="48" height="6" fill="#95a5a6"/>')
    for x in (112, 128):
        b.append(f'<path d="M{x},38 L{x},26" stroke="#222" stroke-width="2"/><circle cx="{x}" cy="24" r="3.5" fill="#222"/>')
    b.append('<path d="M36,44 L72,44 M168,44 L204,44" stroke="#ffd23f" stroke-width="3" stroke-dasharray="6 4"/>')
    b.append('<path d="M52,18 l10,18 h-20z M188,18 l10,18 h-20z" fill="#ffd23f"/>'
             '<text x="52" y="33" font-family="Arial Black" font-size="9" fill="#1f2a3a" text-anchor="middle">!</text>'
             '<text x="188" y="33" font-family="Arial Black" font-size="9" fill="#1f2a3a" text-anchor="middle">!</text>')
    return _svg("".join(b), "#cfd8e3", text)


def carstrike(text=None):
    b = [_ground("#6b7280", 76), '<rect x="10" y="12" width="220" height="34" fill="#9ca3af"/>',
         '<path d="M10,12 L55,0 L100,12 L145,0 L190,12 L230,0 L230,12Z" fill="#6b7280"/>']
    for x, c in ((30, "#d62828"), (120, "#1d4e89")):
        b.append(f'<path d="M{x},66 h54 l-6,-14 h-34z" fill="{c}"/><rect x="{x - 2}" y="64" width="58" height="8" rx="3" fill="{c}"/>'
                 f'<circle cx="{x + 12}" cy="73" r="5" fill="#111"/><circle cx="{x + 42}" cy="73" r="5" fill="#111"/>')
    for i in range(6):
        x = 18 + i * 14
        b.append(f'<circle cx="{x}" cy="52" r="4.5" fill="#5b4636"/><rect x="{x - 4.5}" y="56" width="9" height="14" rx="3" fill="#d62828"/>')
    b.append('<rect x="176" y="24" width="2" height="48" fill="#444"/><rect x="178" y="24" width="40" height="22" fill="#d62828"/>'
             '<text x="198" y="40" font-family="Arial Black" font-size="10" fill="#fff" text-anchor="middle">STREIK</text>')
    return _svg("".join(b), "#cbd5e1", text)


def trophy(text=None):
    b = ['<rect x="0" y="50" width="240" height="40" fill="#2f8f3a"/>', '<path d="M60,50 L60,90 M180,50 L180,90" stroke="#e8f5e9" stroke-width="1.5"/>',
         '<g transform="translate(38,6)">',
         '<path d="M96,14 h48 v18 a24,24 0 0 1 -48,0z" fill="#ffd23f"/><path d="M96,18 h-12 q-4,16 14,20 M144,18 h12 q4,16 -14,20" stroke="#ffd23f" stroke-width="4" fill="none"/>'
         '<rect x="114" y="52" width="12" height="12" fill="#e0b21f"/><rect x="100" y="64" width="40" height="8" rx="2" fill="#b8860b"/></g>']
    return _svg("".join(b), "#20304a", text)


def carbomb(text=None):
    b = [_city("#8a8f98", y=64, seed=9), _ground("#4b5563", 64)]
    b.append('<circle cx="120" cy="50" r="30" fill="#f77f00" opacity=".5"/>')
    b.append('<path d="M92,62 h56 l-6,-14 h-40z" fill="#9aa4b2"/><rect x="88" y="60" width="64" height="9" rx="3" fill="#7b8696"/>'
             '<circle cx="104" cy="70" r="5.5" fill="#111"/><circle cx="138" cy="70" r="5.5" fill="#111"/>')
    b.append(flame(112, 48, 0.85))
    b.append(flame(130, 50, 0.65))
    b.append(smoke(120, 24, 0.55, "#3f3f46"))
    for x in (36, 60, 184, 208):
        b.append(f'<path d="M{x},66 l4,-6 l5,8 l4,-9" stroke="#c9ced6" stroke-width="2" fill="none"/>')
    return _svg("".join(b), "#c6cdd6", text)


KINDS = {f.__name__: f for f in (fire, ship, strike, drone, ballot, protest, court, storm, quake, sport,
                                 market, health, plane, diplomacy, government, tech, flood, climate,
                                 aid, police, space, rally, eu, nato, podium, cricket, union, sanctions, warning, carstrike, trophy, carbomb)}


def banner(kind, text=None):
    return KINDS.get(kind, government)(text)
