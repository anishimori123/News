#!/usr/bin/env python3
"""Build the player pages from the data files.

For every Sports/<Sport>/<player>/data.json this script writes:
  1. Sports/<Sport>/<player>/README.md   (the profile you read on GitHub)
  2. docs/sports/<sport>/<player>.html   (the colour web page you can print)
It also rebuilds docs/index.html (the home page listing every player).

How to run (from the repo folder):   python tools/build.py
Needs only Python 3. No extra installs.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def analytics_tag():
    """Visitor counter. Put your GoatCounter code name in tools/site_config.json to switch it on.
    Empty = no counter on any page."""
    import re
    cfg = ROOT / "tools" / "site_config.json"
    code = json.loads(cfg.read_text(encoding="utf-8")).get("goatcounter_code", "").strip() if cfg.exists() else ""
    if not re.fullmatch(r"[a-z0-9-]{1,60}", code):
        return ""
    return f'<script data-goatcounter="https://{code}.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'


def auto_check(key):
    """Is this page kept up to date by a scheduled task? The list lives in tools/site_config.json ("auto_checks").
    key looks like "Sports/Soccer/maya-yoshida" or "Agents/bridging-to-the-us". Returns the task's details or None.
    This is only a label: remove the entry from site_config.json when the task is paused or deleted."""
    from fnmatch import fnmatch
    cfg = ROOT / "tools" / "site_config.json"
    checks = json.loads(cfg.read_text(encoding="utf-8")).get("auto_checks", []) if cfg.exists() else []
    for c in checks:
        if any(fnmatch(key, pat) for pat in c.get("pages", [])):
            return c
    return None


def auto_badge(key):
    c = auto_check(key)
    return f' <span class="auto" title="{E(c["task"])}">🔄 Auto-check: {E(c["when_short"])}</span>' if c else ""


def auto_note(key):
    c = auto_check(key)
    if not c:
        return ""
    return (f'<div class="autonote">🔄 <b>Checked automatically:</b> {E(c["when"])}, by the scheduled task “{E(c["task"])}”. '
            f'It updates this page only when it finds confirmed news. Each run uses some plan usage; pause it in Claude’s scheduled tasks list when it is no longer needed.</div>')


def search_tag():
    """Search engines. In tools/site_config.json, "show_in_search": false adds a 'noindex' line to every page,
    which asks Google, Bing and others not to list it. true (or missing) = pages may be listed."""
    cfg = ROOT / "tools" / "site_config.json"
    show = json.loads(cfg.read_text(encoding="utf-8")).get("show_in_search", True) if cfg.exists() else True
    return "" if show else '<meta name="robots" content="noindex">'
# Chart colours: one fixed colour per club, in career order (colour-blind-safe set).
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
E = html.escape


def link(text, url):
    return f'<a href="{E(url, quote=True)}">{E(text)}</a>' if url else E(text)


# Words that differ by sport. A data file can override any of them with a "labels" block.
DEFAULT_LABELS = {
    "apps": "matches", "goals": "goals", "apps_title": "Matches", "goals_title": "Goals",
    "chart_heading": "Matches played each season", "country_heading": "Matches by country",
    "seasons_heading": "Season by season (all competitions)",
    "leadership_title": "What makes his leadership special?",
    "club_title": "Career by club",
}


def labels_of(d):
    return {**DEFAULT_LABELS, **d.get("labels", {})}


# ---------------------------------------------------------------- charts (SVG)
def chart_seasons(d):
    lb = labels_of(d)
    clubs = {c["id"]: (c, SERIES[i]) for i, c in enumerate(d["clubs"])}
    rows = d["seasons"]
    bw, gap, left, top, h = 26, 8, 40, 18, 220
    width = left + len(rows) * (bw + gap) + 10
    mx = d.get("chart_max", 50)
    out = [f'<svg viewBox="0 0 {width} {h + 130}" role="img" aria-label="{E(lb["chart_heading"])}, coloured by club" class="chart">']
    for t in [mx * k // 5 for k in range(6)]:
        y = top + h - t / mx * h
        out.append(f'<line x1="{left}" x2="{width - 5}" y1="{y:.1f}" y2="{y:.1f}" class="grid"/>'
                   f'<text x="{left - 6}" y="{y + 4:.1f}" class="tick" text-anchor="end">{t}</text>')
    for i, r in enumerate(rows):
        c, col = clubs[r["club"]]
        x = left + i * (bw + gap)
        bh = max(r["apps"] / mx * h, 1.5)
        y = top + h - bh
        out.append(f'<path d="M{x},{top + h} V{y + 4:.1f} q0,-4 4,-4 h{bw - 8} q4,0 4,4 V{top + h} Z" fill="{col}">'
                   f'<title>{E(r["season"])} {E(c["name"])}: {r["apps"]} {E(lb["apps"])}, {r["goals"]} {E(lb["goals"])}</title></path>')
        out.append(f'<text x="{x + bw / 2}" y="{y - 4:.1f}" class="val" text-anchor="middle">{r["apps"]}</text>')
        out.append(f'<text transform="translate({x + bw / 2 + 4},{top + h + 10}) rotate(60)" class="tick">{E(r["season"])}</text>')
    per_row = 3
    for n, (cid, (c, col)) in enumerate(clubs.items()):
        label = f'{c["name"]} ({c["country"]})'
        lx = left + (n % per_row) * 240
        ly = h + 80 + (n // per_row) * 22
        out.append(f'<rect x="{lx}" y="{ly}" width="12" height="12" rx="3" fill="{col}"/>'
                   f'<text x="{lx + 17}" y="{ly + 10}" class="leg">{E(label)}</text>')
    out.append("</svg>")
    return "".join(out)


def chart_hbars(items, unit, mx=None, fmt=str, colors=None):
    """items = [(label, value)]. One horizontal bar per row with the value written at the end."""
    mx = mx or max(v for _, v in items)
    lh, left, w = 34, 190, 760
    out = [f'<svg viewBox="0 0 {w} {len(items) * lh + 8}" role="img" aria-label="{E(unit)}" class="chart">']
    for i, (lab, v) in enumerate(items):
        y = i * lh + 6
        bl = max(v / mx * (w - left - 110), 2)
        col = colors[i] if colors else SERIES[0]
        out.append(f'<text x="{left - 10}" y="{y + 16}" class="leg" text-anchor="end">{E(lab)}</text>')
        out.append(f'<path d="M{left},{y} h{bl - 4:.1f} q4,0 4,4 v14 q0,4 -4,4 h-{bl - 4:.1f} Z" fill="{col}">'
                   f'<title>{E(lab)}: {E(fmt(v))} {E(unit)}</title></path>')
        out.append(f'<text x="{left + bl + 8:.1f}" y="{y + 16}" class="val">{E(fmt(v))}</text>')
    out.append("</svg>")
    return "".join(out)


# A faceless pitcher seen from behind at the top of a twisting windup, in a manga style (bold ink lines, flat
# shading, speed lines). The number comes from the data file. Drawn from scratch as a symbol: not a portrait of
# anyone, not copied from any photo, and not any existing manga or anime character.
PITCHER = """<svg viewBox="0 0 200 300" class="figure" style="width:180px" role="img" aria-label="Manga-style illustration of a pitcher at the top of a twisting windup, seen from behind (generic figure, not a portrait)">
<g stroke-linecap="round"><path d="M191.9 154.6 L289.8 159.5" stroke="#d5dbe8" stroke-width="1.2"/><path d="M203.9 175.9 L286.3 196.5" stroke="#d5dbe8" stroke-width="2.7"/><path d="M191.0 192.0 L278.2 232.4" stroke="#d5dbe8" stroke-width="1.7"/><path d="M196.8 217.9 L265.7 266.2" stroke="#d5dbe8" stroke-width="3.2"/><path d="M180.1 229.0 L249.1 297.2" stroke="#d5dbe8" stroke-width="2.2"/><path d="M163.1 235.4 L228.9 324.5" stroke="#d5dbe8" stroke-width="1.2"/><path d="M159.4 261.3 L205.4 347.6" stroke="#d5dbe8" stroke-width="2.7"/><path d="M141.0 261.3 L179.4 365.8" stroke="#d5dbe8" stroke-width="1.7"/><path d="M130.3 284.8 L151.4 378.6" stroke="#d5dbe8" stroke-width="3.2"/><path d="M112.0 277.9 L122.2 385.9" stroke="#d5dbe8" stroke-width="2.2"/><path d="M96.2 267.4 L92.4 387.3" stroke="#d5dbe8" stroke-width="1.2"/><path d="M78.9 282.4 L62.8 382.9" stroke="#d5dbe8" stroke-width="2.7"/><path d="M65.7 266.1 L34.1 372.8" stroke="#d5dbe8" stroke-width="1.7"/><path d="M44.7 273.2 L7.0 357.1" stroke="#d5dbe8" stroke-width="3.2"/><path d="M35.6 252.0 L-17.7 336.4" stroke="#d5dbe8" stroke-width="2.2"/><path d="M30.2 230.5 L-39.6 311.1" stroke="#d5dbe8" stroke-width="1.2"/><path d="M9.3 225.6 L-58.1 281.8" stroke="#d5dbe8" stroke-width="2.7"/><path d="M9.2 202.2 L-72.6 249.3" stroke="#d5dbe8" stroke-width="1.7"/><path d="M-9.7 188.6 L-82.9 214.3" stroke="#d5dbe8" stroke-width="3.2"/><path d="M-4.3 165.3 L-88.7 177.7" stroke="#d5dbe8" stroke-width="2.2"/><path d="M4.1 145.2 L-89.8 140.5" stroke="#d5dbe8" stroke-width="1.2"/><path d="M-7.9 123.1 L-86.3 103.5" stroke="#d5dbe8" stroke-width="2.7"/><path d="M5.3 106.2 L-78.2 67.6" stroke="#d5dbe8" stroke-width="1.7"/><path d="M19.8 93.7 L-65.7 33.8" stroke="#d5dbe8" stroke-width="3.2"/><path d="M16.8 67.9 L-49.1 2.8" stroke="#d5dbe8" stroke-width="2.2"/><path d="M34.2 60.9 L-28.9 -24.5" stroke="#d5dbe8" stroke-width="1.2"/><path d="M38.4 34.6 L-5.4 -47.6" stroke="#d5dbe8" stroke-width="2.7"/><path d="M57.4 34.2 L20.6 -65.8" stroke="#d5dbe8" stroke-width="1.7"/><path d="M74.8 38.1 L48.6 -78.6" stroke="#d5dbe8" stroke-width="3.2"/><path d="M87.5 17.2 L77.8 -85.9" stroke="#d5dbe8" stroke-width="2.2"/><path d="M103.9 27.6 L107.6 -87.3" stroke="#d5dbe8" stroke-width="1.2"/><path d="M121.9 12.7 L137.2 -82.9" stroke="#d5dbe8" stroke-width="2.7"/><path d="M135.7 29.2 L165.9 -72.8" stroke="#d5dbe8" stroke-width="1.7"/><path d="M146.0 47.5 L193.0 -57.1" stroke="#d5dbe8" stroke-width="3.2"/><path d="M166.9 44.0 L217.7 -36.4" stroke="#d5dbe8" stroke-width="2.2"/><path d="M172.7 66.1 L239.6 -11.1" stroke="#d5dbe8" stroke-width="1.2"/><path d="M194.0 71.6 L258.1 18.2" stroke="#d5dbe8" stroke-width="2.7"/><path d="M194.5 95.7 L272.6 50.7" stroke="#d5dbe8" stroke-width="1.7"/><path d="M191.5 117.8 L282.9 85.7" stroke="#d5dbe8" stroke-width="3.2"/><path d="M208.3 134.1 L288.7 122.3" stroke="#d5dbe8" stroke-width="2.2"/></g>
<g fill="none" stroke-linecap="round" stroke="#9cc3f5">
<path d="M14 118 C40 86 156 78 188 108" stroke-width="5" opacity=".55"/>
<path d="M10 214 C36 252 164 258 192 214" stroke-width="6" opacity=".55"/>
<path d="M26 170 C22 150 30 136 44 128" stroke-width="3" opacity=".5"/>
<path d="M176 160 C182 178 176 196 164 206" stroke-width="3" opacity=".5"/>
</g>
<ellipse cx="108" cy="287" rx="58" ry="6" fill="#b9c0d2"/>
<g stroke="#1b1b1f" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round">
<path d="M46 176 C40 198 43 222 48 240 L63 240 C62 220 63 202 67 188 Z" fill="#fbfaf6"/>
<path d="M48 240 L63 240 L62 259 L50 259 Z" fill="#2f7fe6"/>
<path d="M50 259 L62 259 L64 268 C58 275 44 274 37 266 C40 262 46 260 50 259 Z" fill="#1b1b1f"/>
<path d="M74 150 L104 152 L101 174 C88 188 72 196 57 196 C45 196 40 186 45 175 C52 164 62 156 74 150 Z" fill="#fbfaf6"/>
<path d="M99 150 L131 150 C134 180 131 205 128 224 C127 236 126 243 125 250 L110 250 C109 236 107 220 106 206 C104 186 100 170 99 150 Z" fill="#fbfaf6"/>
<path d="M110 250 L125 250 L124 271 L111 271 Z" fill="#2f7fe6"/>
<path d="M109 271 L125 271 C134 273 142 278 142 285 L109 285 Z" fill="#1b1b1f"/>
</g>
<path d="M121 152 L130 152 C133 180 130 205 127 224 L124 249 L118 249 C122 220 125 186 121 152 Z" fill="#c5cde2"/>
<path d="M47 177 C43 186 46 194 57 194 C71 194 87 187 99 174 L100 166 C88 178 70 185 57 183 C51 182 48 180 47 177 Z" fill="#c5cde2"/>
<path d="M58 192 C57 208 58 226 58 239 L62 239 C61 220 62 203 65 190 Z" fill="#c5cde2"/>
<path d="M113 172 C115 190 114 204 116 218 M62 166 C70 171 80 174 92 174" fill="none" stroke="#1b1b1f" stroke-width="1.3" stroke-linecap="round"/>
<g fill="none" stroke-linecap="round" stroke-linejoin="round">
<path d="M61 50 L96 20" stroke="#1b1b1f" stroke-width="17"/><path d="M61 50 L96 20" stroke="#2f7fe6" stroke-width="12.4"/>
<path d="M141 50 L106 20" stroke="#1b1b1f" stroke-width="17"/><path d="M141 50 L106 20" stroke="#1a4fa0" stroke-width="12.4"/>
<path d="M74 88 L62 54" stroke="#1b1b1f" stroke-width="26"/><path d="M74 88 L62 54" stroke="#fbfaf6" stroke-width="21.4"/>
<path d="M128 88 L140 54" stroke="#1b1b1f" stroke-width="26"/><path d="M128 88 L140 54" stroke="#c5cde2" stroke-width="21.4"/>
</g>
<path d="M92 60 h18 v18 h-18 z" fill="#f0c6a2"/><path d="M103 60 h7 v18 h-7 z" fill="#d9a47c"/>
<ellipse cx="85" cy="53" rx="3.4" ry="5.4" fill="#f0c6a2" stroke="#1b1b1f" stroke-width="1.6"/><ellipse cx="117" cy="53" rx="3.4" ry="5.4" fill="#d9a47c" stroke="#1b1b1f" stroke-width="1.6"/>
<ellipse cx="101" cy="50" rx="15" ry="17" fill="#f0c6a2" stroke="#1b1b1f" stroke-width="2"/>
<path d="M85 50 L83 60 L88 57 L88 66 L93 61 L95 71 L100 63 L104 72 L108 62 L113 67 L113 58 L119 61 L117 50 Z" fill="#1b1b1f" stroke="#1b1b1f" stroke-width="1.2" stroke-linejoin="round"/>
<path d="M84 52 C81 28 121 28 118 52 C108 57 94 57 84 52 Z" fill="#2f7fe6" stroke="#1b1b1f" stroke-width="2.2" stroke-linejoin="round"/>
<path d="M106 33 C114 36 118 44 117.5 52 C113 54 109 55 105 55.5 C108 48 108 40 106 33 Z" fill="#1a4fa0"/>
<circle cx="101" cy="33.5" r="2.2" fill="#1b1b1f"/>
<path d="M90 36 C88 37 87 39 86.5 41" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/>
<path d="M68 80 C84 70 118 70 134 80 L138 102 C136 122 133 140 132 152 L72 152 C70 138 67 122 64 102 Z" fill="#fbfaf6" stroke="#1b1b1f" stroke-width="2.4" stroke-linejoin="round"/>
<path d="M120 76 C126 77 130 78 133 81 L136.5 102 C135 122 132 138 131 150 L118 150 C122 128 124 100 120 76 Z" fill="#c5cde2"/>
<path d="M90 73 C96 80 106 80 112 73" fill="none" stroke="#1b1b1f" stroke-width="1.8"/>
<path d="M77 96 C81 104 81 114 79 124 M84 142 C94 146 108 146 118 141" fill="none" stroke="#1b1b1f" stroke-width="1.3" stroke-linecap="round"/>
<text x="99" y="130" text-anchor="middle" font-size="40" font-weight="900" fill="#2f7fe6" stroke="#1b1b1f" stroke-width="1.6" paint-order="stroke" font-family="Arial Black, Arial, Helvetica, sans-serif" letter-spacing="1">{number}</text>
<path d="M71 148 h62 l-1 9 h-60 z" fill="#1b1b1f"/>
<path d="M84 148 v9 M101 148 v9 M118 148 v9" stroke="#fbfaf6" stroke-width="2.2"/>
<path d="M88 20 C84 6 96 -1 104 2 C116 1 122 12 116 22 C112 30 94 31 88 20 Z" fill="#a8642c" stroke="#1b1b1f" stroke-width="2.4" stroke-linejoin="round"/>
<path d="M106 4 C115 5 119 13 115 21 C112 27 104 28 100 27 C106 21 108 12 106 4 Z" fill="#7a4418"/>
<path d="M95 7 C97 12 97 18 95 23 M102 5 C104 11 104 18 102 25" fill="none" stroke="#1b1b1f" stroke-width="1.3" stroke-linecap="round"/>
<g fill="#1b1b1f"><path d="M150 30 l3 9 l9 3 l-9 3 l-3 9 l-3 -9 l-9 -3 l9 -3 z" fill="#fff" stroke="#1b1b1f" stroke-width="1.2"/><path d="M40 60 l2 6 l6 2 l-6 2 l-2 6 l-2 -6 l-6 -2 l6 -2 z" fill="#fff" stroke="#1b1b1f" stroke-width="1"/></g>
</svg>"""

# The back of a plain jersey with a name and number. Colours, name and number come from the data file
# ("figure": "jersey", "figure_name", "figure_number", "figure_color", "figure_body"). No team logo or wordmark.
JERSEY = """<svg viewBox="0 0 200 222" class="figure" style="width:180px" role="img" aria-label="Drawing of the back of a baseball jersey with a name and number (not a portrait)">
<path d="M78 16 C88 25 112 25 122 16 L160 28 L195 78 L168 101 L150 80 L150 206 L50 206 L50 80 L32 101 L5 78 L40 28 Z" fill="{body}" stroke="#1b1b1f" stroke-width="3" stroke-linejoin="round"/>
<path d="M132 20 L160 28 L195 78 L168 101 L150 80 L150 206 L128 206 C134 150 136 80 132 20 Z" fill="#000" opacity=".1"/>
<path d="M78 16 C88 25 112 25 122 16 L126 19 C114 32 86 32 74 19 Z" fill="{color}" stroke="#1b1b1f" stroke-width="2.2" stroke-linejoin="round"/>
<path d="M50 80 L57 42 M150 80 L143 42 M13 74 L38 96 M187 74 L162 96 M52 198 H148" fill="none" stroke="#1b1b1f" stroke-width="1.4" stroke-linecap="round" opacity=".55"/>
<path id="figArc" d="M46 84 Q100 50 154 84" fill="none"/>
<text font-size="27" font-weight="900" fill="{color}" font-family="Arial Black, Arial, Helvetica, sans-serif" letter-spacing="5" text-anchor="middle"><textPath href="#figArc" startOffset="50%">{name}</textPath></text>
<text x="100" y="178" text-anchor="middle" font-size="96" font-weight="900" fill="{color}" font-family="Arial Black, Arial, Helvetica, sans-serif">{number}</text>
</svg>"""


# Just the name and number, as on the back of a shirt but with no shirt drawn ("figure": "nameplate").
NAMEPLATE = """<svg viewBox="0 0 200 170" class="figure" style="width:180px" role="img" aria-label="{name} {number}">
<path id="figArc2" d="M30 62 Q100 22 170 62" fill="none"/>
<text font-size="{size}" font-weight="900" fill="{color}" font-family="Arial Black, Arial, Helvetica, sans-serif" letter-spacing="{gap}" text-anchor="middle"><textPath href="#figArc2" startOffset="50%">{name}</textPath></text>
<text x="100" y="160" text-anchor="middle" font-size="112" font-weight="900" fill="{color}" font-family="Arial Black, Arial, Helvetica, sans-serif">{number}</text>
</svg>"""


def jersey_svg(d):
    out = NAMEPLATE if d.get("figure") == "nameplate" else JERSEY
    size = min(36, 170 // max(len(str(d.get("figure_name", ""))), 1))  # long names get smaller letters so they fit the arch
    out = out.replace("{size}", str(size)).replace("{gap}", str(round(size / 6, 1)))
    for k, v in (("name", d.get("figure_name", "")), ("number", d.get("figure_number", "")),
                 ("color", d.get("figure_color", "#1d5aa8")), ("body", d.get("figure_body", "#fbfaf6"))):
        out = out.replace("{" + k + "}", E(str(v), quote=True))
    return out


FIGURE = """<svg viewBox="0 0 120 150" class="figure" role="img" aria-label="Generic illustration of a captain (not a portrait)">
<circle cx="60" cy="26" r="16" fill="#d9d7d0"/>
<path d="M30 52 q30 -14 60 0 l14 34 -14 6 -6 -14 v52 h-48 v-52 l-6 14 -14 -6 z" fill="#2a78d6"/>
<rect x="88" y="62" width="15" height="9" rx="2" fill="#eda100" transform="rotate(22 95 66)"/>
<text x="60" y="98" text-anchor="middle" font-size="26" font-weight="700" fill="#fff" font-family="sans-serif">C</text>
<circle cx="98" cy="134" r="11" fill="#fff" stroke="#52514e" stroke-width="2"/>
</svg>"""

CSS = """
:root{--ink:#0b0b0b;--ink2:#52514e;--line:#e3e1da;--bg:#fcfcfb;--blue:#2a78d6;--soft:#eef4fc;--warm:#fff6e0;--good:#e8f6ee;--bad:#fdecec}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,"Segoe UI","Hiragino Sans","Yu Gothic",Meiryo,sans-serif}
main{max-width:980px;margin:0 auto;padding:24px 20px 60px}
a{color:#1b5fb4}h1{font-size:2.2rem;margin:.2em 0 0}h2{font-size:1.45rem;margin:2.2em 0 .6em;padding-bottom:.25em;border-bottom:3px solid var(--blue)}
h3{font-size:1.08rem;margin:1.2em 0 .3em}.ja{color:var(--ink2);font-weight:400;font-size:1.3rem}
.hero{display:grid;grid-template-columns:1fr 200px;gap:24px;align-items:start}
.photo{border:2px dashed #b9b6ab;border-radius:12px;min-height:230px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:var(--ink2);font-size:.82rem;padding:10px;background:#fff}
.photo img{max-width:100%;border-radius:8px}.figure{width:110px}
.auto{display:inline-block;background:#e6f4ea;border:1px solid #9ccfa8;color:#1e5c2f;border-radius:999px;padding:1px 9px;font-size:.78rem;font-weight:600;white-space:nowrap}
.autonote{background:#e6f4ea;border-left:6px solid #3d9a5a;padding:8px 14px;border-radius:8px;margin:10px 0;font-size:.9rem}
.status{background:var(--warm);border-left:6px solid #eda100;padding:12px 16px;border-radius:8px;margin:14px 0}
.box{background:var(--soft);border-left:6px solid var(--blue);padding:12px 16px;border-radius:8px;margin:14px 0}
.honest{background:var(--bad);border-left:6px solid #e34948;padding:12px 16px;border-radius:8px}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0}
.tile{background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 14px}.tile b{display:block;font-size:1.9rem;line-height:1.1}.tile span{color:var(--ink2);font-size:.85rem}
table{border-collapse:collapse;width:100%;font-size:.92rem;margin:10px 0}th,td{border-bottom:1px solid var(--line);padding:7px 8px;text-align:left;vertical-align:top}
th{background:#f3f1ea;font-weight:600}td.n,th.n{text-align:right;white-space:nowrap}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 18px;margin:12px 0;break-inside:avoid}
.card h3{margin-top:0}.card ul{margin:.4em 0 0;padding-left:1.2em}.card li{margin:.25em 0}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.tag{display:inline-block;border-radius:999px;padding:1px 9px;font-size:.75rem;font-weight:600;border:1px solid}
.OFFICIAL{background:var(--good);border-color:#008300;color:#075c07}.ESTIMATE{background:var(--warm);border-color:#c98500;color:#6e4a00}.NONE{background:#eee;border-color:#999;color:#555}
.club{color:#0b0b0b}.japan{color:#0b0b0b}.chart{width:100%;height:auto;display:block;margin:8px 0}
.grid{stroke:#e3e1da;stroke-width:1}.tick{font-size:10px;fill:#52514e}.val{font-size:11px;fill:#0b0b0b;font-weight:600}.leg{font-size:12px;fill:#0b0b0b}
.small{color:var(--ink2);font-size:.85rem}nav.top{font-size:.9rem;margin-bottom:10px}
.printbtn{float:right;border:1px solid var(--line);background:#fff;border-radius:8px;padding:6px 12px;cursor:pointer;font-size:.9rem}
.layout{display:grid;grid-template-columns:250px minmax(0,980px);gap:8px;justify-content:center;align-items:start}
.layout main{margin:0;max-width:none}
.toc{position:sticky;top:0;max-height:100vh;overflow-y:auto;padding:24px 8px 24px 16px;font-size:.88rem}
.toc summary{font-weight:700;font-size:1rem;cursor:pointer;margin-bottom:8px;list-style:none}
.toc ol{list-style:none;margin:0;padding:0;border-left:2px solid var(--line)}
.toc li a{display:block;padding:5px 10px;margin-left:-2px;border-left:2px solid transparent;color:var(--ink2);text-decoration:none;line-height:1.3}
.toc li a:hover{color:var(--ink);background:#f3f1ea}
.toc li a.on{color:var(--ink);font-weight:600;border-left-color:var(--blue);background:var(--soft)}
.toc p{margin:12px 0 0 10px}
html{scroll-behavior:smooth}h2[id]{scroll-margin-top:12px}
@media(max-width:1000px){.layout{display:block}.toc{position:static;max-height:none;padding:12px 20px 0}.toc details:not([open]) summary{margin-bottom:0}.toc ol{columns:2}}
@media(max-width:720px){.hero,.grid2{grid-template-columns:1fr}.tiles{grid-template-columns:repeat(2,1fr)}.toc ol{columns:1}}
@media print{body{font-size:11.5pt;background:#fff}main{max-width:none;padding:0}.layout{display:block}.printbtn,nav.top,.toc{display:none}h2{break-after:avoid}tr,.card,.tile{break-inside:avoid}a{color:inherit;text-decoration:none}
*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
"""


TOC_JS = """<script>
(function(){var d=document.querySelector('.toc details');if(d&&window.innerWidth<=1000)d.removeAttribute('open');})();
(function(){var links=[].slice.call(document.querySelectorAll('.toc a'));if(!links.length||!('IntersectionObserver' in window))return;
var map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a;});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.remove('on');});
var a=map[e.target.id];if(a)a.classList.add('on');}});},{rootMargin:'-10% 0px -80% 0px'});
document.querySelectorAll('main h2[id]').forEach(function(h){io.observe(h);});})();
</script>"""


def favicon(icon):
    """The small picture on the browser tab: an emoji drawn as a tiny image, so no extra file is needed."""
    from urllib.parse import quote
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">{icon}</text></svg>'
    return f'<link rel="icon" href="data:image/svg+xml,{quote(svg)}">'


def page(title, body, depth, icon="📚"):
    """Wrap a page. Every <h2> becomes a chapter in a jump menu on the left side."""
    import re
    chapters = []

    def add_id(m):
        label = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        cid = f"ch{len(chapters) + 1}"
        chapters.append((cid, label))
        return f'<h2 id="{cid}">{m.group(1)}</h2>'

    body = re.sub(r"<h2>(.*?)</h2>", add_id, body, flags=re.S)
    head = (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title)}</title>{favicon(icon)}<style>{CSS}</style>{search_tag()}{analytics_tag()}</head><body>')
    if len(chapters) < 3:
        return f'{head}<main>{body}</main></body></html>'
    items = "".join(f'<li><a href="#{cid}">{label}</a></li>' for cid, label in chapters)
    toc = (f'<nav class="toc" aria-label="Chapters"><details open><summary>📑 Chapters</summary>'
           f'<ol>{items}</ol><p><a href="#top">↑ Back to top</a></p></details></nav>')
    return f'{head}<div class="layout" id="top">{toc}<main>{body}</main></div>{TOC_JS}</body></html>'


def table(headers, rows, num_cols=()):
    th = "".join(f'<th class="{"n" if i in num_cols else ""}">{E(h)}</th>' for i, h in enumerate(headers))
    trs = "".join("<tr>" + "".join(f'<td class="{"n" if i in num_cols else ""}">{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>"


# ---------------------------------------------------------------- HTML page
def build_html(d, sport):
    clubs = {c["id"]: c for c in d["clubs"]}
    apps = sum(c["apps"] for c in d["clubs"])
    goals = sum(c["goals"] for c in d["clubs"])
    lb = labels_of(d)
    b = []
    b.append('<nav class="top"><a href="../../index.html">← All people</a><button class="printbtn" onclick="window.print()">🖨️ Print this page</button></nav>')
    b.append('<div class="hero"><div>'
             f'<h1>{E(d["name"])} <span class="ja">{E(d["name_ja"])}</span></h1>'
             f'<p>{E(d["summary"])}</p>'
             f'<div class="status"><b>📌 Status ({E(d["updated"])}):</b> {E(d["status"])}</div>{auto_note(f"Sports/{sport}/" + d["id"])}</div>'
             f'<div class="photo"><img src="{E(d["photo"])}" alt="" onerror="this.remove()">'
             + (f'{FIGURE}<div>Generic drawing, not a portrait.<br>📷 Add your own photo: see README.</div>' if d.get("figure", "captain") == "captain"
                else f'{jersey_svg(d)}<div>Drawing of a jersey back, not a portrait.<br>📷 Add your own photo: see README.</div>' if d.get("figure") == "jersey"
                else f'{jersey_svg(d)}<div>{E(d.get("figure_note", ""))}</div>' if d.get("figure") == "nameplate"
                else f'{PITCHER.replace("{number}", E(str(d.get("figure_number", ""))))}<div>Generic drawing, not a portrait.<br>📷 Add your own photo: see README.</div>' if d.get("figure") == "pitcher"
                else '<div>📷 Add your own photo: see README.</div>') + '</div></div>')
    if d.get("tiles"):
        b.append('<div class="tiles">' + "".join(f'<div class="tile"><b>{E(str(big))}</b><span>{E(small)}</span></div>' for big, small in d["tiles"]) + '</div>')
    else:
        b.append('<div class="tiles">'
                 f'<div class="tile"><b>{len({c["country"] for c in d["clubs"]})}</b><span>countries, all in the top division</span></div>'
                 f'<div class="tile"><b>{apps}</b><span>club matches ({goals} goals)</span></div>'
                 '<div class="tile"><b>127</b><span>matches for Japan (12 goals)</span></div>'
                 '<div class="tile"><b>3 + 3</b><span>World Cups + Olympics</span></div></div>')
    b.append(table(["Quick fact", "Detail"], [[f"<b>{E(k)}</b>", E(v)] for k, v in d["quick_facts"]]))

    b.append(f"<h2>🧭 1. {E(lb['leadership_title'])}</h2>")
    b.append(f'<div class="box">{E(d["leadership_intro"])}</div>')
    for i, L in enumerate(d["leadership"], 1):
        ev = "".join(f"<li>{E(t)} {link('[source]', u)}</li>" for t, u in L["evidence"])
        b.append(f'<div class="card"><h3>{L["emoji"]} {i}. {E(L["title"])}</h3><p>{E(L["simple"])}</p><ul>{ev}</ul></div>')
    b.append('<h3>⚖️ The honest view</h3><div class="honest"><ul>' + "".join(f"<li>{E(x)}</li>" for x in d["honest_view"]) + "</ul></div>")

    b.append(f"<h2>📊 2. Career in charts</h2><h3>{E(lb['chart_heading'])}</h3>")
    b.append(chart_seasons(d))
    b.append(f'<p class="small">{E(d["seasons_note"])}</p><h3>{E(lb["country_heading"])}</h3>')
    b.append(chart_hbars([(f'{c["country"]}: {c["name"]}', c["apps"]) for c in d["clubs"]], lb["apps"], colors=SERIES))
    b.append(table(["", "Club", "Country", "League", "Years", lb["apps_title"], lb["goals_title"]],
                   [[c["flag"], E(c["name"]), E(c["country"]), E(c["league"]), E(c["years"]), c["apps"], c["goals"]] for c in d["clubs"]]
                   + [["", "<b>Total</b>", "", "", "", f"<b>{apps}</b>", f"<b>{goals}</b>"]], num_cols=(5, 6)))

    b.append("<h2>🗓️ 3. Year-by-year timeline</h2>")
    icon = {"club": "🏟️ Club", "japan": "🎌 Japan", "life": "🌱 Life"}
    b.append(table(["Year", "Age", "", "Type", "What happened"],
                   [[f'<b>{E(t["year"])}</b>', t["age"], t["flag"], icon[t["tag"]], E(t["event"])] for t in d["timeline"]], num_cols=(1,)))
    b.append(f"<h3>{E(lb['seasons_heading'])}</h3>")
    cols = d.get("season_columns") or [["apps", lb["apps_title"]], ["goals", lb["goals_title"]]]
    b.append(table(["Season", "Club"] + [t for _, t in cols],
                   [[E(s["season"]), f'{clubs[s["club"]]["flag"]} {E(clubs[s["club"]]["name"])}'] + [E(str(s.get(k, "")))for k, _ in cols] for s in d["seasons"]],
                   num_cols=tuple(range(2, 2 + len(cols)))))

    b.append("<h2>🏆 4. What he achieved</h2>")
    b.append(table(["Type", "Achievement", "Year"], [[E(a["type"]), E(a["item"]), E(a["year"])] for a in d["achievements"]]))

    b.append("<h2>📰 5. Headline news</h2><p class='small'>Original headline, with an English translation when the original is not English.</p>")
    rows = []
    for h in d["headlines"]:
        eng = "" if h["english"] == "(same)" else f'<br><span class="small">EN: {E(h["english"])}</span>'
        rows.append([E(h["date"]), E(h["lang"]), f'{link(h["original"], h["url"])}{eng}<br><span class="small">{E(h["source"])}</span>', E(h["why"])])
    b.append(table(["Date", "Language", "Headline", "Why it matters"], rows))

    b.append("<h2>🌱 6. Roots: where he comes from</h2><div class='grid2'>")
    for r in d["roots"]:
        b.append(f'<div class="card"><h3>{r["emoji"]} {E(r["title"])}</h3><p>{E(r["text"])} {link("[source]", r["url"])}</p></div>')
    b.append("</div><h3>Personal events</h3>")
    b.append(table(["Date", "Event"], [[E(p["date"]), f'{E(p["event"])} {link("[source]", p["url"])}'] for p in d["personal"]]))

    c = d.get("controversies")
    if c:
        b.append(f'<h2>⚠️ 7. Controversies and criticism</h2><div class="box">{E(c["intro"])}</div>')
        b.append(table(["When", "His part", "What happened", "How it ended"],
                       [[E(i["date"]), E(i["kind"]), f'<b>{E(i["title"])}</b><br>{E(i["what"])} {link("[source]", i["url"])}', E(i["outcome"])] for i in c["items"]]))
    for n, dd in enumerate(d.get("deep_dives", []), 1):
        if n == 1:
            b.append("<h2>🔎 8. Deep dives</h2>")
        b.append(f'<h3 style="font-size:1.25rem">{dd["emoji"]} 8.{n} {E(dd["title"])}</h3><div class="box">{E(dd["intro"])}</div>')
        for part in dd["parts"]:
            b.append(f'<h3>{E(part["heading"])}</h3>')
            if part["kind"] == "table":
                b.append(table(part["headers"], [[E(x) for x in r["cells"][:-1]] + [f'{E(r["cells"][-1])} {link("[source]", r.get("url"))}' if r.get("url") else E(r["cells"][-1])] for r in part["rows"]]))
            else:
                b.append("<ul>" + "".join(f'<li>{E(t)} {link("[source]", u) if u else ""}</li>' for t, u in part["rows"]) + "</ul>")
    m = d.get("money")
    if m:
        b.append("<h2>💰 9. Money: contracts, salary, sponsors</h2>")
        b.append(f'<div class="box">{E(m["intro"])}</div><h3>{E(m.get("chart_heading", "LA Galaxy salary (official union figures, guaranteed pay per year)"))}</h3>')
        # money.chart_unit / chart_prefix / chart_suffix let a page show pay in another currency (default: US dollars)
        pre, suf = m.get("chart_prefix", "$"), m.get("chart_suffix", "")
        b.append(chart_hbars(m["salary_chart"], m.get("chart_unit", "US dollars"), fmt=lambda v: f"{pre}{v:,.0f}{suf}"))
        b.append(table(["Period", "Club", "Reported pay", "How sure?", "Where from"],
                       [[E(s["period"]), E(s["club"]), E(s["figure"]), f'<span class="tag {s["label"]}">{s["label"]}</span>', link(s["note"] or "–", s["url"])] for s in m["salary"]]))
        if m.get("changes"):
            b.append('<h3>Why his pay changed, year by year</h3>')
            if m.get("changes_intro"):
                b.append(f'<div class="status">{E(m["changes_intro"])}</div>')
            b.append(table(["Years", "What changed", "Why", "How sure?"],
                           [[f'<b>{E(c["period"])}</b>', E(c["change"]), f'{E(c["why"])} {link("[source]", c["url"])}', E(c["label"])] for c in m["changes"]]))
        b.append("<h3>Contracts and transfers</h3>")
        b.append(table(["Date", "Event"], [[E(c["date"]), f'{E(c["event"])} {link("[source]", c["url"])}'] for c in m["contracts"]]))
        b.append("<h3>Sponsors, advertising and other public income</h3>")
        b.append(table(["What", "When", "Status"], [[link(e["what"], e["url"]), E(e["when"]), E(e["status"])] for e in m["endorsements"]]))
        b.append("<ul>" + "".join(f"<li>{E(n)}</li>" for n in m["notes"]) + "</ul>")

    ow = d.get("own_words")
    if ow:
        b.append(f'<h2>🗣️ 10. In his own words (social posts)</h2><div class="box">{E(ow["intro"])}</div>'
                 f'<p class="small">{E(ow["account"])}. Read on {E(ow["read_on"])}. {E(ow["note"])}</p>')
        b.append(table(["Date", "What he posted (in my words)", "What it tells us"], [[E(i["date"]), f'{E(i["what"])} {link("[post]", i["url"])}', E(i["tells"])] for i in ow["items"]]))
    fv = d.get("fan_voices")
    if fv:
        b.append(f'<h2>💬 11. What fans are saying (opinions, not facts)</h2><div class="status">{E(fv["intro"])}</div>')
        for sm in fv["samples"]:
            b.append(f'<h3>{link(sm["source"], sm["url"])}</h3><p class="small">Read on {E(sm["read_on"])}. {E(sm["sample"])}</p>')
            b.append(table(["Theme", "How common", "What readers said (in my words)"], [[f"<b>{E(t)}</b>", E(n), E(x)] for t, n, x in sm["themes"]]))
            b.append("<ul>" + "".join(f"<li>{E(x)}</li>" for x in sm["notes"]) + "</ul>")
    b.append("<h2>❓ 12. Not verified / sources disagree</h2><ul>" + "".join(f"<li>{E(u)}</li>" for u in d["unverified"]) + "</ul>")

    v = d.get("videos")
    if v:
        b.append(f'<h2>🎥 Appendix: videos and interviews</h2><p class="small">{E(v["intro"])}</p>')
        b.append(table(["Type", "Title", "Language", "Why watch", "Link"],
                       [[E(i["type"]), f'{E(i["title"])}<br><span class="small">{E(i["by"])}</span>', E(i["lang"]), E(i["why"]), link(i["link"], i["url"])] for i in v["items"]]))
    b.append(f'<p class="small">Last updated {E(d["updated"])}. Built from <code>Sports/{sport}/{d["id"]}/data.json</code> with <code>tools/build.py</code>. Every claim links to its source; salary estimates are labelled.</p>')
    return page(f'{d["name"]} | {sport}', "".join(b), 2, d.get("emoji", "⚽"))


# ---------------------------------------------------------------- Markdown profile
def md_table(headers, rows):
    def cell(c):
        return str(c).replace("|", "\\|").replace("\n", " ")
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(cell(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def mdl(text, url):
    return f"[{text}]({url.replace(' ', '%20')})" if url else text


def build_md(d, sport):
    clubs = {c["id"]: c for c in d["clubs"]}
    apps = sum(c["apps"] for c in d["clubs"]); goals = sum(c["goals"] for c in d["clubs"])
    lb = labels_of(d)
    cols = d.get("season_columns") or [["apps", lb["apps_title"]], ["goals", lb["goals_title"]]]
    o = [f'# {d["name"]} ({d["name_ja"]})', "", f'> {d["summary"]}', "",
         f'**Last updated:** {d["updated"]}  ', f'**📌 Status:** {d["status"]}', "",
         f'🖨️ **Colour web page (best for printing):** `docs/sports/{sport.lower()}/{d["id"]}.html`', "",
         "_This file is generated from `data.json` by `tools/build.py`. Edit `data.json`, not this file._", "",
         "## Quick facts", md_table(["Item", "Detail"], d["quick_facts"]), "",
         f"## 🧭 1. {lb['leadership_title']}", d["leadership_intro"], ""]
    for i, L in enumerate(d["leadership"], 1):
        o += [f'### {L["emoji"]} {i}. {L["title"]}', L["simple"], ""] + [f"- {t} ({mdl('source', u)})" for t, u in L["evidence"]] + [""]
    o += ["### ⚖️ The honest view"] + [f"- {x}" for x in d["honest_view"]] + [""]
    o += [f"## 📊 2. {lb['club_title']}",
          md_table(["", "Club", "Country", "League", "Years", lb["apps_title"], lb["goals_title"]],
                   [[c["flag"], c["name"], c["country"], c["league"], c["years"], c["apps"], c["goals"]] for c in d["clubs"]] + [["", "**Total**", "", "", "", f"**{apps}**", f"**{goals}**"]]),
          "", "_" + d["seasons_note"] + "_", "",
          "## 🗓️ 3. Year-by-year timeline",
          md_table(["Year", "Age", "", "What happened"], [[t["year"], t["age"], t["flag"], t["event"]] for t in d["timeline"]]), "",
          f"### {lb['seasons_heading']}",
          md_table(["Season", "Club"] + [t for _, t in cols], [[s["season"], clubs[s["club"]]["name"]] + [s.get(k, "") for k, _ in cols] for s in d["seasons"]]), "",
          "## 🏆 4. What he achieved", md_table(["Type", "Achievement", "Year"], [[a["type"], a["item"], a["year"]] for a in d["achievements"]]), "",
          "## 📰 5. Headline news",
          md_table(["Date", "Lang", "Headline (original)", "English", "Why it matters"],
                   [[h["date"], h["lang"], mdl(h["original"], h["url"]) + f' ({h["source"]})', h["english"], h["why"]] for h in d["headlines"]]), "",
          "## 🌱 6. Roots: where he comes from"]
    o += [f'- **{r["emoji"]} {r["title"]}:** {r["text"]} ({mdl("source", r["url"])})' for r in d["roots"]]
    o += ["", "### Personal events", md_table(["Date", "Event", "Source"], [[p["date"], p["event"], mdl("link", p["url"])] for p in d["personal"]]), ""]
    c = d.get("controversies")
    if c:
        o += ["## ⚠️ 7. Controversies and criticism", c["intro"], "",
              md_table(["When", "His part", "What happened", "How it ended", "Source"], [[i["date"], i["kind"], f'**{i["title"]}**: {i["what"]}', i["outcome"], mdl("link", i["url"])] for i in c["items"]]), ""]
    for n, dd in enumerate(d.get("deep_dives", []), 1):
        if n == 1:
            o += ["## 🔎 8. Deep dives", ""]
        o += [f'### {dd["emoji"]} 8.{n} {dd["title"]}', dd["intro"], ""]
        for part in dd["parts"]:
            o += [f'#### {part["heading"]}']
            if part["kind"] == "table":
                o += [md_table(part["headers"] + ["Source"], [r["cells"] + [mdl("link", r["url"]) if r.get("url") else ""] for r in part["rows"]]), ""]
            else:
                o += [f"- {t}" + (f" ({mdl('source', u)})" if u else "") for t, u in part["rows"]] + [""]
    m = d.get("money")
    if m:
        o += ["## 💰 9. Money: contracts, salary, sponsors", m["intro"], "",
              md_table(["Period", "Club", "Reported pay", "How sure?", "Where from"], [[s["period"], s["club"], s["figure"], f'**{s["label"]}**', mdl(s["note"] or "–", s["url"])] for s in m["salary"]]), "",
              *(["### Why his pay changed, year by year", m.get("changes_intro", ""), "",
                 md_table(["Years", "What changed", "Why", "How sure?", "Source"], [[c["period"], c["change"], c["why"], c["label"], mdl("link", c["url"])] for c in m["changes"]]), ""] if m.get("changes") else []),
              "### Contracts and transfers", md_table(["Date", "Event", "Source"], [[c["date"], c["event"], mdl("link", c["url"])] for c in m["contracts"]]), "",
              "### Sponsors, advertising and other public income", md_table(["What", "When", "Status", "Source"], [[e["what"], e["when"], e["status"], mdl("link", e["url"])] for e in m["endorsements"]]), ""]
        o += [f"- {n}" for n in m["notes"]] + [""]
    ow = d.get("own_words")
    if ow:
        o += ["## 🗣️ 10. In his own words (social posts)", ow["intro"], "", f'_{ow["account"]}. Read on {ow["read_on"]}. {ow["note"]}_', "",
              md_table(["Date", "What he posted (in my words)", "What it tells us", "Post"], [[i["date"], i["what"], i["tells"], mdl("link", i["url"])] for i in ow["items"]]), ""]
    fv = d.get("fan_voices")
    if fv:
        o += ["## 💬 11. What fans are saying (opinions, not facts)", "> " + fv["intro"], ""]
        for sm in fv["samples"]:
            o += [f'### {mdl(sm["source"], sm["url"])}', f'_Read on {sm["read_on"]}. {sm["sample"]}_', "",
                  md_table(["Theme", "How common", "What readers said (in my words)"], sm["themes"]), ""]
            o += [f"- {x}" for x in sm["notes"]] + [""]
    o += ["## ❓ 12. Not verified / sources disagree"] + [f"- {u}" for u in d["unverified"]] + [""]
    v = d.get("videos")
    if v:
        o += ["## 🎥 Appendix: videos and interviews", v["intro"], "",
              md_table(["Type", "Title", "By", "Language", "Why watch", "Link"], [[i["type"], i["title"], i["by"], i["lang"], i["why"], mdl(i["link"], i["url"])] for i in v["items"]]), ""]
    return "\n".join(o) + "\n"

# ---------------------------------------------------------------- generic pages (agents, topics)
def parts_html(parts):
    b = []
    for part in parts:
        if part.get("heading"):
            b.append(f'<h3>{E(part["heading"])}</h3>')
        if part["kind"] == "table":
            b.append(table(part["headers"], [[E(x) for x in r["cells"][:-1]] + [f'{E(r["cells"][-1])} {link("[source]", r.get("url"))}' if r.get("url") else E(r["cells"][-1])] for r in part["rows"]]))
        elif part["kind"] == "text":
            b.append(f'<p>{E(part["text"])}</p>')
        else:
            b.append("<ul>" + "".join(f'<li>{E(t)} {link("[source]", u) if u else ""}</li>' for t, u in part["rows"]) + "</ul>")
    return "".join(b)


def parts_md(parts):
    o = []
    for part in parts:
        if part.get("heading"):
            o += [f'#### {part["heading"]}']
        if part["kind"] == "table":
            o += [md_table(part["headers"] + ["Source"], [r["cells"] + [mdl("link", r["url"]) if r.get("url") else ""] for r in part["rows"]]), ""]
        elif part["kind"] == "text":
            o += [part["text"], ""]
        else:
            o += [f"- {t}" + (f" ({mdl('source', u)})" if u else "") for t, u in part["rows"]] + [""]
    return o


def build_generic_html(d, folder):
    b = ['<nav class="top"><a href="../index.html">← Home</a><button class="printbtn" onclick="window.print()">🖨️ Print this page</button></nav>']
    ja = f' <span class="ja">{E(d["name_ja"])}</span>' if d.get("name_ja") else ""
    b.append(f'<h1>{d.get("emoji", "")} {E(d["name"])}{ja}</h1><p>{E(d["summary"])}</p>')
    if d.get("status"):
        b.append(f'<div class="status"><b>📌 Status ({E(d["updated"])}):</b> {E(d["status"])}</div>')
    b.append(auto_note(f"{folder}/" + d["id"]))
    if d.get("quick_facts"):
        b.append(table(["Quick fact", "Detail"], [[f"<b>{E(k)}</b>", E(v)] for k, v in d["quick_facts"]]))
    for n, sec in enumerate(d["sections"], 1):
        b.append(f'<h2>{sec["emoji"]} {n}. {E(sec["title"])}</h2>')
        if sec.get("intro"):
            b.append(f'<div class="{sec.get("box", "box")}">{E(sec["intro"])}</div>')
        b.append(parts_html(sec["parts"]))
    if d.get("unverified"):
        b.append("<h2>❓ Not verified / sources disagree</h2><ul>" + "".join(f"<li>{E(u)}</li>" for u in d["unverified"]) + "</ul>")
    b.append(f'<p class="small">Last updated {E(d["updated"])}. Built from <code>{folder}/{d["id"]}/data.json</code> with <code>tools/build.py</code>. Professional role and public sources only.</p>')
    return page(f'{d["name"]} | {folder}', "".join(b), 1, d.get("emoji") or "🤝")


def build_generic_md(d, folder):
    ja = f' ({d["name_ja"]})' if d.get("name_ja") else ""
    o = [f'# {d.get("emoji", "")} {d["name"]}{ja}', "", f'> {d["summary"]}', "", f'**Last updated:** {d["updated"]}  ']
    if d.get("status"):
        o += [f'**📌 Status:** {d["status"]}']
    o += ["", f'🖨️ **Colour web page:** `docs/{folder.lower()}/{d["id"]}.html`', "",
          "_This file is generated from `data.json` by `tools/build.py`. Edit `data.json`, not this file._", ""]
    if d.get("quick_facts"):
        o += ["## Quick facts", md_table(["Item", "Detail"], d["quick_facts"]), ""]
    for n, sec in enumerate(d["sections"], 1):
        o += [f'## {sec["emoji"]} {n}. {sec["title"]}']
        if sec.get("intro"):
            o += [sec["intro"], ""]
        o += parts_md(sec["parts"])
    if d.get("unverified"):
        o += ["## ❓ Not verified / sources disagree"] + [f"- {u}" for u in d["unverified"]] + [""]
    return "\n".join(o) + "\n"

# ---------------------------------------------------------------- changelog summary (chart + table)
def count_site():
    """Pages = number of data.json files. Words = words in the generated profiles (links removed)."""
    import re
    pages, words = 0, 0
    for data in list(ROOT.glob("Sports/*/*/data.json")) + list(ROOT.glob("Agents/*/data.json")):
        pages += 1
        readme = data.parent / "README.md"
        if readme.exists():
            text = re.sub(r"\]\([^)]*\)", "]", readme.read_text(encoding="utf-8"))
            text = re.sub(r"https?://\S+", "", text)
            words += len(re.findall(r"[^\s|]+", text))
    return pages, words


SPORT_EMOJI = {"Soccer": "⚽", "Baseball": "⚾", "Basketball": "🏀", "Tennis": "🎾", "Golf": "⛳", "Rugby": "🏉", "Volleyball": "🏐",
               "Boxing": "🥊", "Figure-Skating": "⛸️", "Swimming": "🏊", "Athletics": "🏃", "Sumo": "🤼", "Judo": "🥋", "Racing": "🏎️"}


def site_pages():
    """Every page on the site as 'emoji Name', for the changelog's New pages column."""
    labels = []
    for data in sorted(ROOT.glob("Sports/*/*/data.json")):
        d = json.loads(data.read_text(encoding="utf-8"))
        labels.append(f'{SPORT_EMOJI.get(data.parent.parent.name, "🏅")} {d["name"]}')
    for data in sorted(ROOT.glob("Agents/*/data.json")):
        d = json.loads(data.read_text(encoding="utf-8"))
        labels.append(f'{d.get("emoji") or "🤝"} {d["name"]}')
    return labels


def update_changelog():
    """Fill in page/word counts for the newest entry, then rebuild the chart and table at the top of CHANGELOG.md."""
    import re
    from datetime import date, timedelta
    path = ROOT / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8")
    if "<!-- SUMMARY:START" not in text:
        return
    pages_now, words_now = count_site()
    newest = re.search(r"(?m)^## v[\d.]+ — [\d-]+\n", text)
    if newest:  # the newest entry always carries the current counts
        nxt = re.search(r"(?m)^## v", text[newest.end():])
        end = newest.end() + (nxt.start() if nxt else len(text) - newest.end())
        block = text[newest.end():end]
        for name, val in (("Words on site", words_now), ("Pages on site", pages_now)):
            line = f"**{name}:** {val}  "
            if re.search(rf"\*\*{name}:\*\*", block):
                block = re.sub(rf"\*\*{name}:\*\*.*", line, block, count=1)
            else:
                m = re.search(r"\*\*Summary:\*\*.*\n", block)
                pos = m.end() if m else 0
                block = block[:pos] + line + "\n" + block[pos:]
        if "**New pages:**" not in block:  # pages whose name no older entry lists as new
            older = " ".join(re.findall(r"\*\*New pages:\*\*(.*)", text[end:]))
            fresh = [lab for lab in site_pages() if lab.split(" ", 1)[1] not in older]
            if fresh:
                m = re.search(r"\*\*Summary:\*\*.*\n", block)
                pos = m.end() if m else 0
                block = block[:pos] + "**New pages:** " + ", ".join(fresh) + "  \n" + block[pos:]
        text = text[:newest.end()] + block + text[end:]
    entries = []
    for block in re.split(r"(?m)^(?=## v)", text)[1:]:
        head = re.match(r"## (v[\d.]+) — ([\d-]+)", block)
        if not head:
            continue

        def field(name):
            m = re.search(rf"\*\*{name}:\*\*\s*(.+)", block)
            return m.group(1).strip() if m else ""

        def num(name):
            m = re.match(r"[\d,]+", field(name))
            return int(m.group().replace(",", "")) if m else None

        summary = field("Summary")
        if not summary:  # fall back to the first bullet under "What changed"
            m = re.search(r"(?m)^- (.+)", block)
            summary = (m.group(1).strip() if m else "")[:140]
        entries.append({"v": head.group(1), "date": head.group(2), "time": field("Time spent"), "summary": summary,
                        "pages": num("Pages on site"), "words": num("Words on site"), "new": field("New pages"), "auto": "weekly scheduled check" in block})
    entries.reverse()  # oldest first
    lp = lw = 0
    for e in entries:  # an entry without a count keeps the previous one
        e["pages"] = lp = e["pages"] if e["pages"] is not None else lp
        e["words"] = lw = e["words"] if e["words"] is not None else lw
    days = {}  # one point per day: the counts at the end of that day, and the versions released
    for e in entries:
        d0 = date.fromisoformat(e["date"])
        days.setdefault(d0, {"versions": []})
        days[d0].update(pages=e["pages"], words=e["words"])
        days[d0]["versions"].append(e["v"])
    pts = sorted(days.items())
    first, last_day = pts[0][0], pts[-1][0]
    end_day = max(last_day, first + timedelta(days=90))  # always show at least three months of timeline
    span = (end_day - first).days
    # ONE chart, two lines. Pages (single digits) and words (thousands) cannot share a raw scale,
    # so both are drawn as growth since the first day: 1x = the size on day one, 2x = twice as big.
    import math
    w, h, left, top, bottom = 760, 330, 56, 58, 62
    X = lambda d0: left + 22 + (d0 - first).days / span * (w - left - 150)
    kfmt = lambda n: (f"{n / 1000:.1f}".rstrip("0").rstrip(".") + "k") if n >= 1000 else str(n)
    series = [("pages", "Pages", "#2a78d6", lambda n: f"{n} pages"), ("words", "Total words", "#7a7974", lambda n: f"{kfmt(n)} words")]
    base = {k: max(pts[0][1][k], 1) for k, *_ in series}
    top_ratio = max(v[k] / base[k] for _, v in pts for k, *_ in series)
    raw = max(2.0, top_ratio * 1.15) / 4
    mag = 10 ** math.floor(math.log10(raw))
    stepv = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    mx = stepv * 4
    Y = lambda r: top + (h - top - bottom) * (1 - r / mx)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="sans-serif" role="img" aria-label="Growth of pages and total words on the site since the first day">',
           f'<rect width="{w}" height="{h}" fill="#fcfcfb"/>'
           f'<text x="{left}" y="20" font-size="13" font-weight="700" fill="#0b0b0b">Growth since the first day ({first.isoformat()})</text>']
    lx = left
    for k, name, color, lab in series:  # legend
        txt = f"{name} (day one: {lab(pts[0][1][k])})"
        out.append(f'<rect x="{lx}" y="30" width="12" height="12" rx="3" fill="{color}"/><text x="{lx + 17}" y="40" font-size="11" fill="#0b0b0b">{E(txt)}</text>')
        lx += 40 + len(txt) * 6.2
    for i in range(5):
        t = mx * i / 4
        lab = f"{t:g}x"
        out.append(f'<line x1="{left}" x2="{w - 20}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="#e3e1da"/>'
                   f'<text x="{left - 8}" y="{Y(t) + 4:.1f}" font-size="10" fill="#52514e" text-anchor="end">{lab}</text>')
    ends = []
    for k, name, color, lab in series:
        if len(pts) > 1:
            out.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="' + " ".join(f"{X(d0):.1f},{Y(v[k] / base[k]):.1f}" for d0, v in pts) + '"/>')
        for d0, v in pts:
            vers = v["versions"][0] if len(v["versions"]) == 1 else f'{v["versions"][0]} to {v["versions"][-1]}'
            out.append(f'<circle cx="{X(d0):.1f}" cy="{Y(v[k] / base[k]):.1f}" r="5" fill="{color}" stroke="#fcfcfb" stroke-width="2">'
                       f'<title>{d0.isoformat()}: {lab(v[k])} ({E(vers)})</title></circle>')
        d0, v = pts[-1]
        ends.append([Y(v[k] / base[k]), lab(v[k]), color])
    ends.sort()  # write the real latest numbers at the right end of each line, kept apart
    if len(ends) == 2 and ends[1][0] - ends[0][0] < 16:
        mid = (ends[0][0] + ends[1][0]) / 2
        ends[0][0], ends[1][0] = mid - 8, mid + 8
    xe = X(pts[-1][0]) + 12
    for y, txt, color in ends:
        out.append(f'<rect x="{xe:.1f}" y="{y - 5:.1f}" width="8" height="8" rx="2" fill="{color}"/>'
                   f'<text x="{xe + 12:.1f}" y="{y + 3:.1f}" font-size="11" font-weight="700" fill="#0b0b0b">{E(txt)}</text>')
    ticks, cur = [], date(first.year, first.month, 1)
    step = 1 if span <= 400 else (3 if span <= 800 else 12)
    while cur <= end_day:
        if cur >= first:
            ticks.append((cur, cur.strftime("%b %Y") if step < 12 else str(cur.year)))
        m = cur.month - 1 + step
        cur = date(cur.year + m // 12, m % 12 + 1, 1)
    yb = h - bottom
    out.append(f'<line x1="{left}" x2="{w - 20}" y1="{yb}" y2="{yb}" stroke="#b9b6ab"/>')
    for d0, lab in ticks:
        if X(d0) < w - 60:
            out.append(f'<line x1="{X(d0):.1f}" x2="{X(d0):.1f}" y1="{yb}" y2="{yb + 5}" stroke="#b9b6ab"/>'
                       f'<text x="{X(d0):.1f}" y="{yb + 18}" font-size="10" fill="#52514e" text-anchor="middle">{lab}</text>')
    d0, v = pts[-1]
    out.append(f'<text x="{w / 2}" y="{h - 22}" font-size="10" fill="#52514e" text-anchor="middle">1x = the size on the first day. 2x = twice as big. One point per day with an update.</text>'
               f'<text x="{w / 2}" y="{h - 8}" font-size="10" fill="#52514e" text-anchor="middle">Latest: {d0.isoformat()}, {E(v["versions"][-1])}, {v["pages"]} pages, {v["words"]:,} words.</text></svg>')
    (ROOT / "docs" / "changelog-chart.svg").write_text("".join(out), encoding="utf-8")
    rows = [[("🤖 " if e["auto"] else "") + f'**{e["v"]}**', e["date"], ("🆕 **" + e["new"] + "**") if e["new"] else "",
             e["summary"], e["pages"], f'{e["words"]:,}', e["time"]] for e in reversed(entries)]
    block = ("<!-- SUMMARY:START (this block is rebuilt by tools/build.py; do not edit by hand) -->\n"
             "## At a glance\n\n![Growth of pages and total words on the site since the first day](docs/changelog-chart.svg)\n\n"
             + md_table(["Version", "Date", "🆕 New people / pages", "What changed, in one line", "Pages on site", "Words on site", "Time spent"], rows)
             + "\n\n🆕 = this version added a new person or page. 🤖 = found by the weekly scheduled check. Words are counted in the profile text, without link addresses. Full details for each version are below.\n<!-- SUMMARY:END -->")
    text = re.sub(r"<!-- SUMMARY:START.*?<!-- SUMMARY:END -->", lambda m: block, text, flags=re.S)
    path.write_text(text, encoding="utf-8")


def main():
    people, others = [], []
    for data in sorted(ROOT.glob("Sports/*/*/data.json")):
        d = json.loads(data.read_text(encoding="utf-8"))
        sport = data.parent.parent.name
        (data.parent / "README.md").write_text(build_md(d, sport), encoding="utf-8")
        out = ROOT / "docs" / "sports" / sport.lower() / f'{d["id"]}.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        (out.parent / "images").mkdir(exist_ok=True)
        out.write_text(build_html(d, sport), encoding="utf-8")
        people.append((sport, d))
        print("built", out.relative_to(ROOT))
    # Generic folders: every <Folder>/<id>/data.json becomes docs/<folder>/<id>.html
    for folder in ("Agents",):
        for data in sorted(ROOT.glob(f"{folder}/*/data.json")):
            d = json.loads(data.read_text(encoding="utf-8"))
            (data.parent / "README.md").write_text(build_generic_md(d, folder), encoding="utf-8")
            out = ROOT / "docs" / folder.lower() / f'{d["id"]}.html'
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(build_generic_html(d, folder), encoding="utf-8")
            others.append((folder, d))
            print("built", out.relative_to(ROOT))
    cards = "".join(f'<div class="card"><h3>{d.get("emoji", "⚽")} <a href="sports/{s.lower()}/{d["id"]}.html">{E(d["name"])} {E(d["name_ja"])}</a></h3>'
                    f'<p>{E(d["summary"])}</p><p class="small">{E(s)} · updated {E(d["updated"])}{auto_badge(f"Sports/{s}/" + d["id"])}</p></div>' for s, d in people)
    others.sort(key=lambda x: (x[1].get("order", 5), x[1]["name"]))
    ocards = "".join(f'<div class="card"><h3>{d.get("emoji", "🤝")} <a href="{f.lower()}/{d["id"]}.html">{E(d["name"])} {E(d.get("name_ja", ""))}</a></h3>'
                     f'<p>{E(d["summary"])}</p><p class="small">{E(f)} · updated {E(d["updated"])}{auto_badge(f"{f}/" + d["id"])}</p></div>' for f, d in others)
    body = f"<h1>📚 People I follow</h1><p>My own database: athletes, the people around them, and how the sports business works.</p><h2>🏅 Sports</h2>{cards}"
    if ocards:
        body += f"<h2>🤝 Agents</h2>{ocards}"
    cfg = ROOT / "tools" / "site_config.json"
    checks = json.loads(cfg.read_text(encoding="utf-8")).get("auto_checks", []) if cfg.exists() else []
    if checks:
        rows = [[E(c["task"]), E(c["when"]), E(c["covers"])] for c in checks]
        body += ('<h2>🔄 Automatic checks</h2><p>Pages with the green <span class="auto">🔄 Auto-check</span> label are checked for news by a scheduled task. '
                 'Each run uses some plan usage. To stop one, pause or delete it in Claude’s scheduled tasks list, then remove it from <code>tools/site_config.json</code> so the label disappears.</p>'
                 + table(["Scheduled task", "When it runs", "Pages it covers"], rows))
    (ROOT / "docs" / "index.html").write_text(page("News: people I follow", body, 0), encoding="utf-8")
    (ROOT / "docs" / ".nojekyll").write_text("", encoding="utf-8")
    update_changelog()


if __name__ == "__main__":
    main()
