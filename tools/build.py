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
# Chart colours: one fixed colour per club, in career order (colour-blind-safe set).
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
E = html.escape


def link(text, url):
    return f'<a href="{E(url, quote=True)}">{E(text)}</a>' if url else E(text)


# ---------------------------------------------------------------- charts (SVG)
def chart_seasons(d):
    clubs = {c["id"]: (c, SERIES[i]) for i, c in enumerate(d["clubs"])}
    rows = d["seasons"]
    bw, gap, left, top, h = 26, 8, 40, 18, 220
    width = left + len(rows) * (bw + gap) + 10
    mx = 50
    out = [f'<svg viewBox="0 0 {width} {h + 130}" role="img" aria-label="Matches played per season, coloured by club" class="chart">']
    for t in (0, 10, 20, 30, 40, 50):
        y = top + h - t / mx * h
        out.append(f'<line x1="{left}" x2="{width - 5}" y1="{y:.1f}" y2="{y:.1f}" class="grid"/>'
                   f'<text x="{left - 6}" y="{y + 4:.1f}" class="tick" text-anchor="end">{t}</text>')
    for i, r in enumerate(rows):
        c, col = clubs[r["club"]]
        x = left + i * (bw + gap)
        bh = max(r["apps"] / mx * h, 1.5)
        y = top + h - bh
        out.append(f'<path d="M{x},{top + h} V{y + 4:.1f} q0,-4 4,-4 h{bw - 8} q4,0 4,4 V{top + h} Z" fill="{col}">'
                   f'<title>{E(r["season"])} {E(c["name"])}: {r["apps"]} matches, {r["goals"]} goals</title></path>')
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
@media(max-width:720px){.hero,.grid2{grid-template-columns:1fr}.tiles{grid-template-columns:repeat(2,1fr)}}
@media print{body{font-size:11.5pt;background:#fff}main{max-width:none;padding:0}.printbtn,nav.top{display:none}h2{break-after:avoid}tr,.card,.tile{break-inside:avoid}a{color:inherit;text-decoration:none}
*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
"""


def page(title, body, depth):
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title)}</title><style>{CSS}</style></head><body><main>{body}</main></body></html>')


def table(headers, rows, num_cols=()):
    th = "".join(f'<th class="{"n" if i in num_cols else ""}">{E(h)}</th>' for i, h in enumerate(headers))
    trs = "".join("<tr>" + "".join(f'<td class="{"n" if i in num_cols else ""}">{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>"


# ---------------------------------------------------------------- HTML page
def build_html(d, sport):
    clubs = {c["id"]: c for c in d["clubs"]}
    apps = sum(c["apps"] for c in d["clubs"])
    goals = sum(c["goals"] for c in d["clubs"])
    b = []
    b.append('<nav class="top"><a href="../../index.html">← All people</a><button class="printbtn" onclick="window.print()">🖨️ Print this page</button></nav>')
    b.append('<div class="hero"><div>'
             f'<h1>{E(d["name"])} <span class="ja">{E(d["name_ja"])}</span></h1>'
             f'<p>{E(d["summary"])}</p>'
             f'<div class="status"><b>📌 Status ({E(d["updated"])}):</b> {E(d["status"])}</div></div>'
             f'<div class="photo"><img src="{E(d["photo"])}" alt="" onerror="this.remove()">{FIGURE}'
             '<div>Generic drawing, not a portrait.<br>📷 Add your own photo: see README.</div></div></div>')
    b.append('<div class="tiles">'
             f'<div class="tile"><b>{len({c["country"] for c in d["clubs"]})}</b><span>countries, all in the top division</span></div>'
             f'<div class="tile"><b>{apps}</b><span>club matches ({goals} goals)</span></div>'
             '<div class="tile"><b>127</b><span>matches for Japan (12 goals)</span></div>'
             '<div class="tile"><b>3 + 3</b><span>World Cups + Olympics</span></div></div>')
    b.append(table(["Quick fact", "Detail"], [[f"<b>{E(k)}</b>", E(v)] for k, v in d["quick_facts"]]))

    b.append("<h2>🧭 1. What makes his leadership special?</h2>")
    b.append(f'<div class="box">{E(d["leadership_intro"])}</div>')
    for i, L in enumerate(d["leadership"], 1):
        ev = "".join(f"<li>{E(t)} {link('[source]', u)}</li>" for t, u in L["evidence"])
        b.append(f'<div class="card"><h3>{L["emoji"]} {i}. {E(L["title"])}</h3><p>{E(L["simple"])}</p><ul>{ev}</ul></div>')
    b.append('<h3>⚖️ The honest view</h3><div class="honest"><ul>' + "".join(f"<li>{E(x)}</li>" for x in d["honest_view"]) + "</ul></div>")

    b.append("<h2>📊 2. Career in charts</h2><h3>Matches played each season</h3>")
    b.append(chart_seasons(d))
    b.append(f'<p class="small">{E(d["seasons_note"])}</p><h3>Matches by country</h3>')
    b.append(chart_hbars([(f'{c["country"]}: {c["name"]}', c["apps"]) for c in d["clubs"]], "matches", colors=SERIES))
    b.append(table(["", "Club", "Country", "League", "Years", "Matches", "Goals"],
                   [[c["flag"], E(c["name"]), E(c["country"]), E(c["league"]), E(c["years"]), c["apps"], c["goals"]] for c in d["clubs"]]
                   + [["", "<b>Total</b>", "", "", "", f"<b>{apps}</b>", f"<b>{goals}</b>"]], num_cols=(5, 6)))

    b.append("<h2>🗓️ 3. Year-by-year timeline</h2>")
    icon = {"club": "🏟️ Club", "japan": "🎌 Japan", "life": "🌱 Life"}
    b.append(table(["Year", "Age", "", "Type", "What happened"],
                   [[f'<b>{E(t["year"])}</b>', t["age"], t["flag"], icon[t["tag"]], E(t["event"])] for t in d["timeline"]], num_cols=(1,)))
    b.append("<h3>Season by season (all competitions)</h3>")
    b.append(table(["Season", "Club", "Matches", "Goals"],
                   [[E(s["season"]), f'{clubs[s["club"]]["flag"]} {E(clubs[s["club"]]["name"])}', s["apps"], s["goals"]] for s in d["seasons"]], num_cols=(2, 3)))

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
    m = d.get("money")
    if m:
        b.append("<h2>💰 8. Money: contracts, salary, sponsors</h2>")
        b.append(f'<div class="box">{E(m["intro"])}</div><h3>LA Galaxy salary (official union figures, guaranteed pay per year)</h3>')
        b.append(chart_hbars(m["salary_chart"], "US dollars", fmt=lambda v: f"${v:,.0f}"))
        b.append(table(["Period", "Club", "Reported pay", "How sure?", "Where from"],
                       [[E(s["period"]), E(s["club"]), E(s["figure"]), f'<span class="tag {s["label"]}">{s["label"]}</span>', link(s["note"] or "–", s["url"])] for s in m["salary"]]))
        b.append("<h3>Contracts and transfers</h3>")
        b.append(table(["Date", "Event"], [[E(c["date"]), f'{E(c["event"])} {link("[source]", c["url"])}'] for c in m["contracts"]]))
        b.append("<h3>Sponsors, advertising and other public income</h3>")
        b.append(table(["What", "When", "Status"], [[link(e["what"], e["url"]), E(e["when"]), E(e["status"])] for e in m["endorsements"]]))
        b.append("<ul>" + "".join(f"<li>{E(n)}</li>" for n in m["notes"]) + "</ul>")

    b.append("<h2>❓ 9. Not verified / sources disagree</h2><ul>" + "".join(f"<li>{E(u)}</li>" for u in d["unverified"]) + "</ul>")

    v = d.get("videos")
    if v:
        b.append(f'<h2>🎥 Appendix: videos and interviews</h2><p class="small">{E(v["intro"])}</p>')
        b.append(table(["Type", "Title", "Language", "Why watch", "Link"],
                       [[E(i["type"]), f'{E(i["title"])}<br><span class="small">{E(i["by"])}</span>', E(i["lang"]), E(i["why"]), link(i["link"], i["url"])] for i in v["items"]]))
    b.append(f'<p class="small">Last updated {E(d["updated"])}. Built from <code>Sports/{sport}/{d["id"]}/data.json</code> with <code>tools/build.py</code>. Every claim links to its source; salary estimates are labelled.</p>')
    return page(f'{d["name"]} | {sport}', "".join(b), 2)


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
    o = [f'# {d["name"]} ({d["name_ja"]})', "", f'> {d["summary"]}', "",
         f'**Last updated:** {d["updated"]}  ', f'**📌 Status:** {d["status"]}', "",
         f'🖨️ **Colour web page (best for printing):** `docs/sports/{sport.lower()}/{d["id"]}.html`', "",
         "_This file is generated from `data.json` by `tools/build.py`. Edit `data.json`, not this file._", "",
         "## Quick facts", md_table(["Item", "Detail"], d["quick_facts"]), "",
         "## 🧭 1. What makes his leadership special?", d["leadership_intro"], ""]
    for i, L in enumerate(d["leadership"], 1):
        o += [f'### {L["emoji"]} {i}. {L["title"]}', L["simple"], ""] + [f"- {t} ({mdl('source', u)})" for t, u in L["evidence"]] + [""]
    o += ["### ⚖️ The honest view"] + [f"- {x}" for x in d["honest_view"]] + [""]
    o += ["## 📊 2. Career by club",
          md_table(["", "Club", "Country", "League", "Years", "Matches", "Goals"],
                   [[c["flag"], c["name"], c["country"], c["league"], c["years"], c["apps"], c["goals"]] for c in d["clubs"]] + [["", "**Total**", "", "", "", f"**{apps}**", f"**{goals}**"]]),
          "", "_" + d["seasons_note"] + "_", "",
          "## 🗓️ 3. Year-by-year timeline",
          md_table(["Year", "Age", "", "What happened"], [[t["year"], t["age"], t["flag"], t["event"]] for t in d["timeline"]]), "",
          "### Season by season (all competitions)",
          md_table(["Season", "Club", "Matches", "Goals"], [[s["season"], clubs[s["club"]]["name"], s["apps"], s["goals"]] for s in d["seasons"]]), "",
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
    m = d.get("money")
    if m:
        o += ["## 💰 8. Money: contracts, salary, sponsors", m["intro"], "",
              md_table(["Period", "Club", "Reported pay", "How sure?", "Where from"], [[s["period"], s["club"], s["figure"], f'**{s["label"]}**', mdl(s["note"] or "–", s["url"])] for s in m["salary"]]), "",
              "### Contracts and transfers", md_table(["Date", "Event", "Source"], [[c["date"], c["event"], mdl("link", c["url"])] for c in m["contracts"]]), "",
              "### Sponsors, advertising and other public income", md_table(["What", "When", "Status", "Source"], [[e["what"], e["when"], e["status"], mdl("link", e["url"])] for e in m["endorsements"]]), ""]
        o += [f"- {n}" for n in m["notes"]] + [""]
    o += ["## ❓ 9. Not verified / sources disagree"] + [f"- {u}" for u in d["unverified"]] + [""]
    v = d.get("videos")
    if v:
        o += ["## 🎥 Appendix: videos and interviews", v["intro"], "",
              md_table(["Type", "Title", "By", "Language", "Why watch", "Link"], [[i["type"], i["title"], i["by"], i["lang"], i["why"], mdl(i["link"], i["url"])] for i in v["items"]]), ""]
    return "\n".join(o) + "\n"


def main():
    people = []
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
    cards = "".join(f'<div class="card"><h3>⚽ <a href="sports/{s.lower()}/{d["id"]}.html">{E(d["name"])} {E(d["name_ja"])}</a></h3>'
                    f'<p>{E(d["summary"])}</p><p class="small">{E(s)} · updated {E(d["updated"])}</p></div>' for s, d in people)
    (ROOT / "docs" / "index.html").write_text(page("News: people I follow", f"<h1>📚 People I follow</h1><p>My own database of athletes: career, leadership, roots and news.</p><h2>Sports</h2>{cards}", 0), encoding="utf-8")
    (ROOT / "docs" / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    main()
