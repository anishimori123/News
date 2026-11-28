# News

### 🌐 Open my website: **[anishimori123.github.io/News/](https://anishimori123.github.io/News/)**

My interest, my news, my curiosity. I dig into the roots and the "why" behind news and people.

## 🌐 Web version (colour, charts, printable)

Click a link to open the live page:

- 🏠 Home page: [anishimori123.github.io/News/](https://anishimori123.github.io/News/)
- ⚽ Maya Yoshida: [open page](https://anishimori123.github.io/News/sports/soccer/maya-yoshida.html)
- ⚾ Hideo Nomo: [open page](https://anishimori123.github.io/News/sports/baseball/hideo-nomo.html)
- ⚾ Teruaki Sato: [open page](https://anishimori123.github.io/News/sports/baseball/teruaki-sato.html)
- 🤝 Agents: [overview](https://anishimori123.github.io/News/agents/overview.html) · [Tetsuro Kiyooka](https://anishimori123.github.io/News/agents/tetsuro-kiyooka.html) · [Thomas Kroth](https://anishimori123.github.io/News/agents/thomas-kroth.html) · [Hai Berden](https://anishimori123.github.io/News/agents/hai-berden.html) · [Kees Ploegsma Jr.](https://anishimori123.github.io/News/agents/kees-ploegsma-jr.html) · [Don Nomura](https://anishimori123.github.io/News/agents/don-nomura.html) · [Wasserman](https://anishimori123.github.io/News/agents/wasserman.html) · [Bridging to the US](https://anishimori123.github.io/News/agents/bridging-to-the-us.html) · [VC Sports Group](https://anishimori123.github.io/News/agents/vc-sports-group.html) · [Shawn Novak](https://anishimori123.github.io/News/agents/shawn-novak.html)
- 📈 History of changes: [CHANGELOG.md](CHANGELOG.md)
- 👀 Who visits (only I can sign in): [website visitors on GoatCounter](https://anishimori-news.goatcounter.com/) · [repo visitors on GitHub](https://github.com/anishimori123/News/graphs/traffic) · [saved history](traffic/README.md)

The same pages are stored in this repo under the `docs/` folder.

**To see it on your PC:** download the repo (green **Code** button → **Download ZIP**), unzip it, open the `docs` folder, and double-click `index.html`. It opens in your browser.

**To print:** open a player page and click **🖨️ Print this page** (top right). In the print window, turn on **Background graphics** so the colours print.

**To put it online for free (GitHub Pages = GitHub's free website hosting):**
1. On GitHub, open this repo and click **Settings** (top row).
2. Click **Pages** in the left menu.
3. Under **Branch**, pick `main`, then pick the folder `/docs`, then click **Save**.
4. Wait about 1 minute. Success looks like: a green box with a link such as `https://anishimori123.github.io/News/`.

💲 Cost: free if this repo is **public**. If the repo is **private**, GitHub Pages needs a paid GitHub plan.

## 📁 What is in here

| Folder / file | What it is |
|---|---|
| `Sports/` | One folder per sport, one folder per person |
| `Sports/Soccer/maya-yoshida/data.json` | The "database" for one person: all facts in one file |
| `Sports/Soccer/maya-yoshida/README.md` | The profile, readable on GitHub (made automatically) |
| `Agents/` | Football and baseball agents, plus explainers on how Japanese players get overseas and how baseball players are bridged to the US; one folder and one `data.json` each |
| `Sports/Soccer/_TEMPLATE.md` | The standard sections every profile should have |
| `docs/` | The web pages (made automatically) |
| `traffic/` | Daily record of how many people (or bots) viewed and downloaded this repo; see `traffic/README.md` |
| `tools/build.py` | The small program that turns `data.json` into the README and the web page |
| `CHANGELOG.md` | The history of changes |

## 👤 People

| Sport | Person | Profile | Web page |
|---|---|---|---|
| ⚽ Soccer | Maya Yoshida 吉田麻也 | [Profile](Sports/Soccer/maya-yoshida/README.md) | `docs/sports/soccer/maya-yoshida.html` |
| ⚾ Baseball | Hideo Nomo 野茂英雄 | [Profile](Sports/Baseball/hideo-nomo/README.md) | `docs/sports/baseball/hideo-nomo.html` |

## 🤝 Agents

| Page | Profile | Web page |
|---|---|---|
| 🧭 How Japanese players get overseas | [Profile](Agents/overview/README.md) | `docs/agents/overview.html` |
| Tetsuro Kiyooka 清岡哲朗 | [Profile](Agents/tetsuro-kiyooka/README.md) | `docs/agents/tetsuro-kiyooka.html` |
| Thomas Kroth トーマス・クロート | [Profile](Agents/thomas-kroth/README.md) | `docs/agents/thomas-kroth.html` |
| Hai Berden ハイ・ベルデン (gateway chairman) | [Profile](Agents/hai-berden/README.md) | `docs/agents/hai-berden.html` |
| Kees Ploegsma Jr. | [Profile](Agents/kees-ploegsma-jr/README.md) | `docs/agents/kees-ploegsma-jr.html` |
| ⚾ Don Nomura 団野村 (Hideo Nomo's agent) | [Profile](Agents/don-nomura/README.md) | `docs/agents/don-nomura.html` |
| 🏢 Wasserman / THE·TEAM (US agency for Japanese baseball stars) | [Profile](Agents/wasserman/README.md) | `docs/agents/wasserman.html` |
| 🌉 Bridging Japanese athletes to the US (routes, life support, gaps) | [Profile](Agents/bridging-to-the-us/README.md) | `docs/agents/bridging-to-the-us.html` |

## 📷 Add your own photo

1. Save your photo with exactly the person's id as its name: `maya-yoshida.jpg` or `hideo-nomo.jpg`
2. Put it in that sport's images folder: `docs/sports/soccer/images/` or `docs/sports/baseball/images/`
3. Open the page again. Success looks like: your photo appears in the dashed box at the top right.

Only use photos you are allowed to use (for example, ones you took yourself).

## 🔧 Update a profile (optional, for when you learn more)

1. Edit `data.json` for that person.
2. Run this in a terminal (a window where you type commands) opened in the repo folder:
   ```
   python tools/build.py
   ```
3. Success looks like: a line that says `built docs/sports/soccer/maya-yoshida.html`.

It needs Python 3 (free). Nothing else to install. Or just ask Claude to update it.

## ✅ Rules for this database

- Every claim has a source link.
- Money numbers are labelled **OFFICIAL** or **ESTIMATE**.
- Things that could not be confirmed go in "Not verified", not in the main text.
- No private details: only what the person or reputable media made public.
