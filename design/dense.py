"""Dense one-day front page: masthead, region chips, UTC timeline, 3 leads,
a day-in-numbers panel, 10 story cards, an ALSO list, a pinned world map,
a DATE CHECK box and a sourcing footer. Driven by a JSON story file.

usage: python design/dense.py design/day.json [out-name]
"""

import html
import json
import pathlib
import sys

from icons import banner
from scenes import SCENES

HERE = pathlib.Path(__file__).resolve().parent

BADGE = {"REPORTED": "#2e7d32", "OFFICIAL": "#1d4e89", "CONFIRMED": "#2e7d32",
         "CLAIM": "#e09f00", "ONGOING": "#1d6fa3", "PROVISIONAL": "#6a4c93"}
REGION = {"EUROPE": "#2563c9", "MIDDLE EAST": "#c62828", "AFRICA": "#2e7d32", "ASIA": "#ef6c00",
          "AMERICAS": "#7b3fa0", "OCEANIA": "#00897b", "WORLD": "#37474f"}

# Coarse land mask on a 60x26 grid: column = 6 deg of longitude from -180,
# row = 5 deg of latitude from 75N. Boxes are (col0, col1, row0, row1), inclusive.
LAND = [
    (2, 6, 1, 3), (6, 14, 1, 4), (17, 20, 1, 4), (15, 16, 1, 1), (15, 16, 4, 4), (21, 26, 0, 2),
    (9, 18, 5, 8), (10, 16, 9, 9), (17, 17, 9, 9), (11, 14, 10, 10), (13, 15, 11, 11), (15, 16, 12, 12),
    (17, 21, 12, 13), (16, 23, 14, 15), (17, 24, 16, 16), (17, 23, 17, 19), (18, 22, 20, 21),
    (18, 20, 22, 23), (18, 19, 24, 25),
    (30, 34, 1, 3), (28, 29, 3, 4), (29, 35, 4, 5), (28, 34, 6, 6), (28, 30, 7, 7), (32, 33, 7, 7),
    (34, 37, 6, 7), (35, 59, 0, 3), (36, 55, 4, 4), (37, 49, 5, 5), (37, 52, 6, 6), (51, 52, 6, 7),
    (53, 54, 6, 8), (42, 50, 7, 9), (38, 40, 7, 9), (35, 39, 9, 11), (41, 44, 9, 11), (42, 43, 12, 12),
    (45, 48, 10, 13), (50, 50, 11, 12), (45, 47, 14, 14), (49, 53, 14, 15), (48, 50, 16, 16),
    (28, 35, 7, 8), (27, 36, 9, 12), (37, 38, 11, 12), (29, 38, 13, 13), (31, 37, 14, 15),
    (32, 37, 16, 19), (38, 38, 17, 19), (33, 35, 20, 21),
    (49, 54, 17, 18), (48, 55, 19, 20), (49, 55, 21, 21), (53, 54, 22, 22), (57, 58, 22, 24),
]
COLS, ROWS = 60, 26
NUDGE = [(0, 0), (-10, -6), (10, -6), (-10, 6), (10, 6), (0, -12), (0, 12), (-20, 0), (20, 0)]


def land_cells():
    cells = set()
    for c0, c1, r0, r1 in LAND:
        for c in range(c0, c1 + 1):
            for r in range(r0, r1 + 1):
                cells.add((c, r))
    return cells


def world_map(pins, w=250, h=150):
    sx, sy = w / COLS, h / ROWS
    out = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    for c, r in sorted(land_cells()):
        out.append(f'<circle cx="{(c + .5) * sx:.1f}" cy="{(r + .5) * sy:.1f}" r="1.9" fill="#a9b4c2"/>')
    import math
    placed = []
    marks, lines = [], []
    for n, lat, lon, col in pins:
        x0 = min(max((lon + 180) / 360 * w, 9), w - 9)
        y0 = (75 - lat) / 130 * h
        spot = None
        for ring in (0, 11, 15, 19, 23, 27, 31):
            for k in range(12 if ring else 1):
                a_ = math.pi * 2 * k / 12 + 0.4
                x, y = x0 + ring * math.cos(a_), y0 + ring * math.sin(a_)
                if 8 <= x <= w - 8 and 8 <= y <= h - 8 and not any(abs(x - px) < 11 and abs(y - py) < 11 for px, py in placed):
                    spot = (x, y)
                    break
            if spot:
                break
        x, y = spot or (x0, y0)
        placed.append((x, y))
        if (x, y) != (x0, y0):
            lines.append(f'<path d="M{x0:.1f},{y0:.1f} L{x:.1f},{y:.1f}" stroke="{col}" stroke-width="1.2"/>'
                         f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="1.8" fill="{col}"/>')
        marks.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.4" fill="{col}" stroke="#fff" stroke-width="1"/>'
                     f'<text x="{x:.1f}" y="{y + 2.8:.1f}" font-family="Arial" font-weight="700" font-size="7.2" '
                     f'fill="#fff" text-anchor="middle">{n}</text>')
    out.extend(lines)
    out.extend(marks)
    out.append("</svg>")
    return "".join(out)


def esc(s):
    return html.escape(s, quote=False)


def pic(s):
    if s.get("scene") in SCENES:
        return SCENES[s["scene"]]()
    return banner(s.get("scene", "government"), s.get("text"))


def card(n, s, lead=False):
    col = REGION.get(s["region"], "#37474f")
    bcol = BADGE.get(s["badge"], "#2e7d32")
    cls = "card lead" if lead else "card"
    return (f'<div class="{cls}" style="--rc:{col}"><div class="pic">{pic(s)}'
            f'<div class="place"><i>{n}</i>{esc(s["place"])}</div>'
            f'<div class="badge" style="background:{bcol}">{s["badge"]}</div></div>'
            f'<div class="tx"><div class="kick">{esc(s["region"])} · {esc(s["field"])}</div>'
            f'<h2>{esc(s["headline"])}</h2><p>{esc(s["dek"])}</p><div class="src">{esc(s["source"])}</div></div></div>')


CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 1024px; height: 1024px; overflow: hidden; }
body { background: #f7f3ea; color: #15181d; font-family: 'Segoe UI', Arial, sans-serif; -webkit-font-smoothing: antialiased;
       display: flex; flex-direction: column; }
body > * { flex: none; }
svg { display: block; width: 100%; height: 100%; }
.bar { background: #15181d; color: #fff; display: flex; justify-content: space-between; padding: 3px 12px;
       font: 700 11px Bahnschrift, Arial; letter-spacing: 1.5px; }
.bar b { color: #ffcc33; }
.mast { text-align: center; padding: 2px 10px 0; }
.mast h1 { font: 700 68px/0.98 Georgia, 'Times New Roman', serif; letter-spacing: -1.5px; color: #15181d; }
.mast .tag { font: italic 700 19px Georgia, serif; color: #b3001b; margin-top: 2px; }
.chips { display: flex; justify-content: center; gap: 6px; margin: 5px 0 4px; }
.chips span { font: 700 11px Bahnschrift, Arial; color: #fff; padding: 2px 8px; border-radius: 3px; letter-spacing: .6px; }
.utc { margin: 0 10px; background: #15181d; color: #e8e8e8; border-radius: 4px; padding: 3px 8px; font-size: 10.5px;
       white-space: nowrap; overflow: hidden; }
.utc b { color: #ff5a6e; margin-right: 6px; }
.utc span { margin-right: 8px; }
.utc em { color: #ffcc33; font-style: normal; font-weight: 700; margin-right: 3px; }
.leads { display: grid; grid-template-columns: 1fr 1fr 1fr 178px; gap: 8px; margin: 6px 10px 0; height: 222px; }
.rows { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin: 6px 10px 0; height: 180px; }
.card { background: #fff; border: 1px solid #d8d2c4; border-top: 4px solid var(--rc); display: flex; flex-direction: column;
        min-height: 0; overflow: hidden; }
.card .pic { position: relative; height: 60px; flex: none; }
.card.lead .pic { height: 86px; }
.place { position: absolute; left: 5px; top: 5px; background: rgba(255,255,255,.94); color: #15181d; padding: 1px 6px 1px 2px;
         border-radius: 3px; font: 700 10.5px Bahnschrift, Arial; letter-spacing: .4px; display: flex; align-items: center; gap: 4px; }
.place i { font-style: normal; background: var(--rc); color: #fff; border-radius: 50%; width: 15px; height: 15px;
           display: inline-flex; align-items: center; justify-content: center; font-size: 9.5px; }
.badge { position: absolute; right: 5px; bottom: 5px; color: #fff; font: 700 9px Arial; letter-spacing: .8px;
         padding: 2px 5px; border-radius: 2px; }
.tx { padding: 4px 7px 4px; display: flex; flex-direction: column; flex: 1; min-height: 0; }
.kick { font: 700 9.5px Arial; letter-spacing: .8px; color: var(--rc); text-transform: uppercase; }
.card h2 { font: 700 14.5px/1.08 Georgia, serif; margin-top: 2px; }
.card.lead h2 { font-size: 20px; }
.card p { font-size: 10.5px; line-height: 1.22; color: #333; margin-top: 3px; }
.card.lead p { font-size: 11.5px; }
.src { margin-top: auto; font-size: 9px; color: #777; padding-top: 2px; }
.nums { background: #15253d; color: #fff; padding: 7px 10px; display: flex; flex-direction: column; gap: 4px; }
.nums h3 { font: 700 12px Bahnschrift, Arial; letter-spacing: 1px; border-bottom: 1px solid #3b4d6b; padding-bottom: 3px; }
.nums div b { display: block; font: 700 21px/1 Bahnschrift, Arial; color: #ffcc33; }
.nums div span { font-size: 10px; color: #c8d3e3; line-height: 1.15; display: block; }
.also { min-width: 0; }
.bottom { display: grid; grid-template-columns: minmax(0, 1fr) 280px; gap: 8px; margin: 6px 10px 0; height: 146px; }
.also h3, .map h3 { font: 700 12.5px Bahnschrift, Arial; letter-spacing: 1px; border-bottom: 2px solid #15181d; padding-bottom: 2px; margin-bottom: 3px; }
.also ol { list-style: none; columns: 3; column-gap: 12px; }
.also li { font-size: 10.2px; line-height: 1.25; break-inside: avoid; margin-bottom: 2px; white-space: nowrap; overflow: hidden; }
.also li b { font-weight: 700; }
.also li i { font-style: normal; color: #b3001b; font-weight: 700; margin-right: 3px; }
.lab { color: #fff; font: 700 8px Arial; padding: 0 3px; border-radius: 2px; margin-right: 3px; vertical-align: 1px; }
.also li small { color: #777; font-size: 9px; margin-left: 3px; }
.map { background: #fff; border: 1px solid #d8d2c4; padding: 4px 6px; display: flex; flex-direction: column; }
.map .m { flex: 1; min-height: 0; }
.check { margin: 6px 10px 0; border: 2px solid #c62828; background: #fff; padding: 4px 8px; font-size: 10.5px; line-height: 1.3; }
.check .h { display: flex; gap: 8px; align-items: center; font-weight: 700; font-size: 12px; }
.check .h span { background: #c62828; color: #fff; padding: 1px 7px; font: 700 12px Bahnschrift, Arial; letter-spacing: 1px; }
.check .h em { margin-left: auto; color: #c62828; font-style: normal; font-size: 11px; }
.check u { text-decoration: none; color: #c62828; font-weight: 700; }
.foot { text-align: center; font-size: 9.5px; color: #555; padding: 3px 10px 0; }
"""


def small(a):
    short = len(a[2]) + len(a[0]) <= (30 if len(a) > 4 and a[4] != "REPORTED" else 40)
    return f'<small>{esc(a[0])}</small>' if short else ""


def tag(a):
    if len(a) > 4 and a[4] != "REPORTED":
        return f'<span class="lab" style="background:{BADGE[a[4]]}">{a[4]}</span>'
    return ""


def build(day):
    every = day["leads"] + day["stories"]
    counts = {}
    for s in every + [{"region": a[1]} for a in day["also"]]:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    total = len(every) + len(day["also"])
    chips = "".join(f'<span style="background:{REGION.get(r, "#37474f")}">{esc(r)} {n}</span>'
                    for r, n in sorted(counts.items(), key=lambda kv: -kv[1]))
    utc = "".join(f'<span><em>{esc(t)}</em>{esc(x)}</span>' for t, x in day["timeline"])
    nums = "".join(f'<div><b>{esc(v)}</b><span>{esc(t)}</span></div>' for v, t in day["numbers"])
    leads = "".join(card(i + 1, s, True) for i, s in enumerate(day["leads"]))
    rest = [card(i + 4, s) for i, s in enumerate(day["stories"])]
    also = "".join(f'<li><i>{i + 14}</i>{tag(a)}<b>{esc(a[2])}</b>{small(a)}</li>'
                   for i, a in enumerate(day["also"]))
    pins = [(i + 1, s["lat"], s["lon"], REGION.get(s["region"], "#37474f")) for i, s in enumerate(every)]
    left = " · ".join(f'{esc(t)} <u>{esc(d)}</u>' for t, d in day["left_out"])
    body = f"""
<div class="bar"><span>THE WORLD IN ONE DAY</span><span><b>{total} STORIES · {len(counts)} REGIONS</b> · ALL FROM THIS ONE DAY</span></div>
<div class="mast"><h1>{esc(day["day"])}</h1><div class="tag">{esc(day["tagline"])}</div></div>
<div class="chips">{chips}</div>
<div class="utc"><b>UTC</b>{utc}</div>
<div class="leads">{leads}<div class="nums"><h3>THE DAY IN NUMBERS</h3>{nums}</div></div>
<div class="rows">{"".join(rest[:5])}</div>
<div class="rows">{"".join(rest[5:10])}</div>
<div class="bottom"><div class="also"><h3>ALSO ON {esc(day["short"])}</h3><ol>{also}</ol></div>
<div class="map"><h3>WHERE IT HAPPENED</h3><div class="m">{world_map(pins)}</div></div></div>
<div class="check"><div class="h"><span>DATE CHECK</span>{esc(day["check"])}<em>Left out on purpose: first reported on an earlier day</em></div>{left}<br><b>Not yet:</b> {esc(day["not_yet"])}</div>
<div class="foot">{esc(day["foot"])}</div>
"""
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'


CHECK_JS = """<script>addEventListener('load',()=>{const bad=[];
document.querySelectorAll('.card p,.card h2,.also li,.kick,.src,.utc,.tx').forEach(e=>{
 if(e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1)bad.push(e.className+':'+e.textContent.slice(0,40));});
const pre=document.createElement('pre');pre.id='overflow';pre.textContent='OVERFLOW '+JSON.stringify(bad);document.body.appendChild(pre);});</script>"""


def overflow(html_path):
    import subprocess
    from build import EDGE
    r = subprocess.run([EDGE, "--headless", "--disable-gpu", "--dump-dom", "--window-size=1024,1024",
                        html_path.as_uri()], capture_output=True, text=True, encoding="utf-8")
    i = r.stdout.find("OVERFLOW")
    return r.stdout[i:r.stdout.find("</pre>", i)] if i >= 0 else "no report"


if __name__ == "__main__":
    from build import OUT, EDGE
    import subprocess
    src = pathlib.Path(sys.argv[1])
    name = sys.argv[2] if len(sys.argv) > 2 else src.stem
    OUT.mkdir(exist_ok=True)
    h = OUT / f"{name}.html"
    png = OUT / f"{name}.png"
    page_html = build(json.loads(src.read_text(encoding="utf-8")))
    h.write_text(page_html.replace("</body>", CHECK_JS + "</body>"), encoding="utf-8")
    print(overflow(h))
    h.write_text(page_html, encoding="utf-8")
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--screenshot={png}", "--window-size=1024,1024", h.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(png)
