"""Build the 23 Nov 2026 world-news image as HTML, then render it to PNG
with Edge headless at 1024x1024.

usage: python design/build.py [variant ...]   (default: all variants)
"""

import pathlib
import subprocess
import sys

from scenes import SCENES

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

DAY = "MONDAY 23 NOVEMBER 2026"

# Only stories marked verified in news-20261123.md. Each: scene, region tag,
# headline, one-line explainer.
STORIES = [
    ("cop31", "CLIMATE · TURKEY",
     "COP31 climate summit ends with no deal",
     "190+ nations split; final draft dropped coal, oil &amp; gas after a Saudi-led push. "
     "First UN climate talks without an agreement since 2009."),
    ("warship", "WAR · LIBYA / UKRAINE",
     "Ukraine says its sea drone sank a Russian warship in Libya",
     "Ukraine's claim: corvette sunk at Benghazi port. Not independently confirmed."),
    ("hormuz", "MIDDLE EAST · SHIPPING",
     "More ships hit in the Strait of Hormuz",
     "3+ vessels struck by projectiles; Iran warns it will answer any US attack."),
    ("gaza", "MIDDLE EAST · GAZA",
     "Israeli strikes kill aid workers in Gaza",
     "Food deliverers and a UN (UNRWA) worker among the dead; settler arson in the West Bank."),
    ("house", "USA · POLITICS",
     "Democrats reach 259 House seats",
     "Their most since the 1992 elections, with 3 races still not called."),
    ("factory", "ASIA · INDONESIA",
     "Factory fire in Banten: 34 workers missing",
     "Blaze at a sweets factory west of Jakarta; about 300 people were inside."),
]

EXTRA = ("protest", "EUROPE · PROTESTS",
         "Students march across Europe",
         "Tens of thousands in Rome, 100+ Italian cities and Paris; also Spain, Germany, UK.")

ALSO = [
    "Student protests across Europe: Rome, Paris and 100+ Italian cities",
    "Zanzibar: six beach hotels burn, ~180 tourists evacuated",
]

NOTE = ("Stories reported on Mon 23 Nov 2026 (some events took place over the weekend). "
        "Claims are labelled as claims.")

BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 1024px; height: 1024px; overflow: hidden; }
body { -webkit-font-smoothing: antialiased; }
svg { display: block; width: 100%; height: 100%; }
"""


def page(css, body):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}{css}'
            f'</style></head><body>{body}</body></html>')


# ---------- Variant A: newspaper front page, 3x2 even grid ----------
def front_page():
    css = """
body { background: #f6f1e7; color: #151515; font-family: Georgia, 'Times New Roman', serif;
       padding: 22px 26px; display: flex; flex-direction: column; }
.mast { text-align: center; border-bottom: 4px double #151515; padding-bottom: 8px; }
.mast .k { font: 700 15px Arial, sans-serif; letter-spacing: 6px; }
.mast h1 { font-size: 64px; line-height: 1; letter-spacing: -1px; margin: 2px 0 4px; }
.mast .d { font: 700 26px Bahnschrift, Arial, sans-serif; letter-spacing: 3px; color: #b3001b; }
.grid { flex: 1; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: 1fr 1fr;
        gap: 14px; margin-top: 12px; }
.c { display: flex; flex-direction: column; min-height: 0; border-top: 3px solid #151515; padding-top: 6px; }
.c .pic { height: 205px; border: 1px solid #151515; overflow: hidden; }
.tag { font: 700 11px Arial, sans-serif; letter-spacing: 1.5px; color: #b3001b; margin-top: 6px; }
.c h2 { font-size: 21px; line-height: 1.08; margin-top: 3px; }
.c p { font-size: 13px; line-height: 1.3; margin-top: 4px; color: #333; }
.also { border-top: 2px solid #151515; margin-top: 10px; padding-top: 6px; font: 13px Arial, sans-serif; }
.also b { color: #b3001b; letter-spacing: 1px; }
.note { font: italic 11px Georgia, serif; color: #555; margin-top: 4px; text-align: center; }
"""
    cells = "".join(
        f'<div class="c"><div class="pic">{SCENES[s]()}</div><div class="tag">{t}</div>'
        f'<h2>{h}</h2><p>{p}</p></div>' for s, t, h, p in STORIES)
    body = (f'<div class="mast"><div class="k">THE WORLD IN ONE DAY</div><h1>World News</h1>'
            f'<div class="d">{DAY}</div></div><div class="grid">{cells}</div>'
            f'<div class="also"><b>ALSO TODAY:</b> {" &nbsp;·&nbsp; ".join(ALSO)}</div>'
            f'<div class="note">{NOTE}</div>')
    return page(css, body)


# ---------- Variant B: dark bento, hero tile for the lead story ----------
def bento():
    css = """
body { background: #0f1724; color: #f4f6fa; font-family: 'Segoe UI', Arial, sans-serif;
       padding: 20px; display: flex; flex-direction: column; }
.top { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 12px; }
.top .w { font: 700 50px/0.95 Bahnschrift, Arial, sans-serif; letter-spacing: 1px; }
.top .d { text-align: right; font: 700 30px/1 Bahnschrift, Arial, sans-serif; color: #ffcc33; }
.top .d small { display: block; font: 600 13px 'Segoe UI', Arial; color: #9fb0c8; letter-spacing: 2px; margin-bottom: 4px; }
.g { flex: 1; display: grid; grid-template-columns: 1fr 1fr 1fr; grid-template-rows: 1.25fr 1fr 1fr;
     gap: 10px; min-height: 0; }
.t { background: #1b2638; border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; min-height: 0; }
.t .pic { flex: 1; min-height: 0; }
.t .tx { padding: 7px 10px 9px; }
.t .tag { font: 700 10px Arial; letter-spacing: 1.5px; color: #ffcc33; }
.t h2 { font: 700 17px/1.12 'Segoe UI', Arial; margin-top: 2px; }
.t p { font-size: 12px; line-height: 1.28; color: #c3cedd; margin-top: 3px; }
.hero { grid-column: span 2; }
.hero h2 { font-size: 26px; }
.hero p { font-size: 14px; }
.key { justify-content: center; background: #24324a; }
.key h2 { font-size: 20px; }
.also { margin-top: 10px; background: #ffcc33; color: #0f1724; border-radius: 10px; padding: 7px 12px;
        font: 600 13px 'Segoe UI', Arial; }
.note { font-size: 11px; color: #8394ad; margin-top: 6px; text-align: center; }
"""
    tiles = []
    for i, (s, t, h, p) in enumerate(STORIES + [EXTRA]):
        cls = "t hero" if i == 0 else "t"
        tiles.append(f'<div class="{cls}"><div class="pic">{SCENES[s]()}</div><div class="tx">'
                     f'<div class="tag">{t}</div><h2>{h}</h2><p>{p}</p></div></div>')
    key = ('<div class="t key"><div class="tx"><div class="tag">HOW TO READ</div><h2>7 stories, 6 regions</h2>'
           '<p>Each tile: one event first reported on Monday 23 November 2026, with where it happened. '
           'Ukraine&#39;s warship report is its own claim.</p></div></div>')
    body = (f'<div class="top"><div class="w">WORLD<br>NEWS</div><div class="d"><small>THE DAY IN ONE IMAGE</small>'
            f'{DAY}</div></div><div class="g">{"".join(tiles)}{key}</div>'
            f'<div class="also">ALSO: {ALSO[1]}</div><div class="note">{NOTE}</div>')
    return page(css, body)


# ---------- Variant C: picture-first poster, captions overlaid ----------
def poster():
    css = """
body { background: #ffffff; color: #111; font-family: Bahnschrift, 'Segoe UI', Arial, sans-serif;
       display: flex; flex-direction: column; }
.hd { background: #c8102e; color: #fff; padding: 14px 22px 12px; display: flex; align-items: baseline;
      justify-content: space-between; }
.hd .w { font: 700 44px/1 Bahnschrift, Arial; letter-spacing: 2px; }
.hd .d { font: 700 30px/1 Bahnschrift, Arial; }
.g { flex: 1; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: repeat(3, 1fr); gap: 4px;
     background: #111; padding: 4px; min-height: 0; }
.t { position: relative; overflow: hidden; min-height: 0; }
.t .cap { position: absolute; left: 0; right: 0; bottom: 0; padding: 26px 12px 8px;
          background: linear-gradient(transparent, rgba(0,0,0,.86) 38%); color: #fff; }
.t .n { position: absolute; top: 8px; left: 8px; background: #c8102e; color: #fff; font: 700 11px Arial;
        letter-spacing: 1.2px; padding: 3px 7px; border-radius: 3px; }
.t h2 { font: 700 21px/1.1 Bahnschrift, Arial; }
.t p { font: 13px/1.25 'Segoe UI', Arial; color: #e6e6e6; margin-top: 3px; }
.ft { padding: 7px 18px 9px; font: 13px 'Segoe UI', Arial; background: #111; color: #eee; }
.ft b { color: #ff5a6e; }
.ft i { display: block; color: #aaa; font-size: 11px; margin-top: 2px; }
"""
    tiles = "".join(
        f'<div class="t">{SCENES[s]()}<div class="n">{t}</div><div class="cap"><h2>{h}</h2><p>{p}</p></div></div>'
        for s, t, h, p in STORIES)
    body = (f'<div class="hd"><div class="w">WORLD NEWS</div><div class="d">{DAY}</div></div>'
            f'<div class="g">{tiles}</div><div class="ft"><b>ALSO:</b> {" · ".join(ALSO)}<i>{NOTE}</i></div>')
    return page(css, body)


ZANZIBAR = ("zanzibar", "AFRICA · TANZANIA",
            "Fire destroys six beach hotels in Zanzibar",
            "About 180 tourists evacuated from hotels at Nungwi beach.")


# ---------- Variant D: bento, iterated on the judges' notes ----------
def bento2():
    css = """
body { background: #0f1724; color: #f4f6fa; font-family: 'Segoe UI', Arial, sans-serif;
       padding: 18px 20px 14px; display: flex; flex-direction: column; }
.top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;
       border-bottom: 3px solid #ffcc33; padding-bottom: 10px; }
.top .w { font: 700 54px/0.92 Bahnschrift, Arial, sans-serif; letter-spacing: 1px; }
.top .d { text-align: right; font: 700 40px/1 Bahnschrift, Arial, sans-serif; color: #ffcc33; }
.top .d small { display: block; font: 700 14px 'Segoe UI', Arial; color: #9fb0c8; letter-spacing: 3px;
                margin-bottom: 6px; }
.g { flex: 1; display: grid; grid-template-columns: 1fr 1fr 1fr; grid-template-rows: 1.1fr 1fr 1fr;
     gap: 10px; min-height: 0; }
.t { background: #1b2638; border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; min-height: 0; }
.t .pic { flex: 1; min-height: 0; }
.t .tx { padding: 6px 10px 8px; }
.tag { font: 700 10.5px Arial; letter-spacing: 1.5px; color: #ffcc33; }
.t h2 { font: 700 18.5px/1.1 'Segoe UI', Arial; margin-top: 2px; }
.t p { font-size: 12px; line-height: 1.25; color: #c3cedd; margin-top: 3px; }
.hero { grid-column: span 2; flex-direction: row; }
.hero .pic { flex: 0 0 56%; }
.hero .tx { flex: 1; display: flex; flex-direction: column; justify-content: center; padding: 12px 16px; }
.hero h2 { font-size: 30px; line-height: 1.05; margin-top: 6px; }
.hero p { font-size: 14px; margin-top: 8px; }
.claim { display: inline-block; background: #ffcc33; color: #0f1724; font: 800 10px Arial; letter-spacing: 1px;
         padding: 1px 5px; border-radius: 3px; margin-left: 4px; vertical-align: 1px; }
.note { margin-top: 9px; font-size: 12px; color: #9fb0c8; text-align: center; }
.note b { color: #ffcc33; }
"""
    stories = STORIES + [EXTRA, ZANZIBAR]
    tiles = []
    for i, (s, t, h, p) in enumerate(stories):
        if s == "warship":
            t += ' <span class="claim">CLAIM</span>'
        cls = "t hero" if i == 0 else "t"
        tiles.append(f'<div class="{cls}"><div class="pic">{SCENES[s]()}</div><div class="tx">'
                     f'<div class="tag">{t}</div><h2>{h}</h2><p>{p}</p></div></div>')
    body = (f'<div class="top"><div class="w">WORLD<br>NEWS</div><div class="d"><small>THE DAY IN ONE IMAGE</small>'
            f'{DAY}</div></div><div class="g">{"".join(tiles)}</div>'
            f'<div class="note"><b>8 stories from around the world</b> · reported on Monday 23 November 2026, '
            f'some from weekend events · claims are marked as claims</div>')
    return page(css, body)


VARIANTS = {"a-front-page": front_page, "b-bento": bento, "c-poster": poster, "d-bento2": bento2}


def render(name):
    OUT.mkdir(exist_ok=True)
    html = OUT / f"{name}.html"
    png = OUT / f"{name}.png"
    html.write_text(VARIANTS[name](), encoding="utf-8")
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--screenshot={png}",
                    "--window-size=1024,1024", html.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return png


if __name__ == "__main__":
    for n in sys.argv[1:] or VARIANTS:
        print(render(n))
