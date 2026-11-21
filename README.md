# News

My interest, my news, my curiosity. I dig into the roots and the "why" behind news and people.

## 🌐 Web version (colour, charts, printable)

- Home page: `docs/index.html`
- Maya Yoshida: `docs/sports/soccer/maya-yoshida.html`

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
| `Sports/Soccer/_TEMPLATE.md` | The standard sections every profile should have |
| `docs/` | The web pages (made automatically) |
| `tools/build.py` | The small program that turns `data.json` into the README and the web page |
| `CHANGELOG.md` | The history of changes |

## 👤 People

| Sport | Person | Profile | Web page |
|---|---|---|---|
| ⚽ Soccer | Maya Yoshida 吉田麻也 | [Profile](Sports/Soccer/maya-yoshida/README.md) | `docs/sports/soccer/maya-yoshida.html` |

## 📷 Add your own photo

1. Save your photo with exactly this name: `maya-yoshida.jpg`
2. Put it in the folder `docs/sports/soccer/images/`
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
