# Changelog

<!-- SUMMARY:START (this block is rebuilt by tools/build.py; do not edit by hand) -->
## At a glance

![Growth of pages and total words on the site since the first day](docs/changelog-chart.svg)

| Version | Date | 🆕 New people / pages | What changed, in one line | Pages on site | Words on site | Time spent |
|---|---|---|---|---|---|---|
| **v0.3.4** | 2026-11-21 |  | Maya Yoshida's money section now explains why his pay changed, year by year, including the 43% cut after winning the 2024 title. | 8 | 27,325 | about 15 minutes |
| **v0.3.3** | 2026-11-21 |  | README now starts with a clickable link to the live website, and every page in its list is a live link. | 8 | 26,723 | about 5 minutes |
| **v0.3.2** | 2026-11-21 |  | Changelog table now highlights versions that add a new person or page with 🆕. | 8 | 26,723 | about 10 minutes |
| **v0.3.1** | 2026-11-21 |  | Changelog chart now shows the blue pages line and the grey words line together on one graph. | 8 | 26,723 | about 10 minutes |
| **v0.3.1** | 2026-11-21 |  | Every page now shows a small icon on the browser tab, so the site is easy to spot. | 8 | 26,723 | about 5 minutes |
| **v0.3.0** | 2026-11-21 | 🆕 **⚾ Hideo Nomo, 🤝 Don Nomura** | New sport and person: Hideo Nomo (baseball), plus a page for his agent Don Nomura; the build tool now works for any sport. | 8 | 26,723 | about 50 minutes (6 research helpers running in parallel) |
| **v0.2.7** | 2026-11-21 |  | Changelog chart gains a grey line for total words on the site; page and word counts are now filled in automatically. | 6 | 16,701 | about 15 minutes |
| **v0.2.6** | 2026-11-21 |  | Changelog chart now runs by date, to show progress over months and years. | 6 | 16,701 | about 10 minutes |
| **v0.2.5** | 2026-11-21 |  | Chart and summary table added at the top of this changelog. | 6 | 16,701 | about 10 minutes |
| **v0.2.4** | 2026-11-21 |  | Left-side chapter menu on every page. | 6 | 16,701 | about 10 minutes |
| **v0.2.3** | 2026-11-21 |  | 'In his own words' section from Yoshida's X account. | 6 | 16,701 | about 10 minutes |
| **v0.2.2** | 2026-11-21 |  | 'What fans are saying' section from Yahoo! News Japan comments. | 6 | 16,519 | about 10 minutes |
| **v0.2.1** | 2026-11-21 | 🆕 **🚪 Hai Berden, 🇳🇱 Kees Ploegsma Jr.** | Agents overview gets the story, trends and 2026 outlook; new pages for Hai Berden and Kees Ploegsma Jr. | 6 | 16,079 | about 20 minutes |
| **v0.2.0** | 2026-11-21 | 🆕 **🧭 How Japanese players get overseas: agents explained, 🤝 Tetsuro Kiyooka, 🇩🇪 Thomas Kroth** | New Agents folder: overview, Tetsuro Kiyooka and Thomas Kroth; Yoshida's agent details corrected. | 4 | 13,216 | about 45 minutes (5 research helpers running in parallel) |
| **v0.1.2** | 2026-11-21 |  | Three deep dives for Yoshida: the Vera&John ad deal, being a target, sports agents. | 1 | 7,170 | about 25 minutes |
| **v0.1.1** | 2026-11-21 |  | Controversies and criticism section added to Yoshida and to the template. | 1 | 5,100 | about 10 minutes |
| **v0.1.0** | 2026-11-21 | 🆕 **⚽ Maya Yoshida** | First person added: Maya Yoshida profile, printable web page, build tool and template. | 1 | 4,618 | about 1 hour (one Claude session, with 5 research helpers running in parallel) |

🆕 = this version added a new person or page. 🤖 = found by the weekly scheduled check. Words are counted in the profile text, without link addresses. Full details for each version are below.
<!-- SUMMARY:END -->

How to add an entry: put it directly below this line, newest first. Start with `## vX.Y.Z — YYYY-MM-DD`, then `**Summary:**` (one sentence) and `**Time spent:**`, `**What changed**` and `**Why**`. `python tools/build.py` fills in `**New pages:**`, `**Pages on site:**` and `**Words on site:**` for the newest entry and updates the chart and table above.

## v0.3.4 — 2026-11-21
**Summary:** Maya Yoshida's money section now explains why his pay changed, year by year, including the 43% cut after winning the 2024 title.  
**Pages on site:** 8  
**Words on site:** 27325  
**Time spent:** about 15 minutes

**What changed**
- New table "Why his pay changed, year by year" in the money section: each change, the reason, the source, and how sure the reason is.
- The 2024 to 2025 drop is explained with the Los Angeles Times report: the league's salary cap, the timing of his contract ending, and why he accepted it.
- The 2025 to 2026 rise is shown as official numbers with the reason marked "not confirmed".

**Why**
- The salary table showed a big gap between 2024 and 2025 with no explanation.

## v0.3.3 — 2026-11-21
**Summary:** README now starts with a clickable link to the live website, and every page in its list is a live link.  
**Pages on site:** 8  
**Words on site:** 26723  
**Time spent:** about 5 minutes

**What changed**
- A large link to the website home page sits at the very top of `README.md`.
- The page list under it now links straight to each live page, including the agent pages that were missing from the list.

**Why**
- To get from the GitHub repo to the website in one click.

## v0.3.2 — 2026-11-21
**Summary:** Changelog table now highlights versions that add a new person or page with 🆕.  
**Pages on site:** 8  
**Words on site:** 26723  
**Time spent:** about 10 minutes

**What changed**
- The summary table has a new column, "🆕 New people / pages". A version that adds someone shows 🆕 and their names, each with an emoji for the kind of page (⚽ soccer, ⚾ baseball, 🤝 agent and so on).
- The build tool works out the new names for the newest version by itself.

**Why**
- To spot at a glance which versions added a new person and which only improved existing pages.

## v0.3.1 — 2026-11-21
**Summary:** Changelog chart now shows the blue pages line and the grey words line together on one graph.  
**Pages on site:** 8  
**Words on site:** 26723  
**Time spent:** about 10 minutes

**What changed**
- Both lines are on one graph. Because pages are counted in single digits and words in thousands, each line is drawn as growth since the first day: 1x is the size on day one, 2x is twice as big.
- The real latest numbers are written at the right end of each line, and the table still lists exact counts for every version.

**Why**
- One graph is easier to read at a glance, and it shows whether the site is growing by adding pages or by making pages deeper.

## v0.3.1 — 2026-11-21
**Summary:** Every page now shows a small icon on the browser tab, so the site is easy to spot.  
**Time spent:** about 5 minutes

**What changed**
- The home page tab shows 📚. Each person's tab shows their sport (⚽ or ⚾). Each agent page shows its own icon.
- The icon is drawn by the build tool, so there is no extra image file to keep.

**Why**
- With many tabs open, the News pages were hard to find.

## v0.3.0 — 2026-11-21
**Summary:** New sport and person: Hideo Nomo (baseball), plus a page for his agent Don Nomura; the build tool now works for any sport.  
**New pages:** ⚾ Hideo Nomo, 🤝 Don Nomura  
**Pages on site:** 8  
**Words on site:** 26723  
**Time spent:** about 50 minutes (6 research helpers running in parallel)

**What changed**
- New sport folder `Sports/Baseball/` and a new person: **Hideo Nomo (野茂英雄)**. Full profile: why "going his own way" worked (six patterns with evidence) and what it cost, career charts and season table (Japan and USA; totals checked: 201 wins, 3,122 strikeouts), timeline, headline news in Japanese, English and Spanish, roots, controversies, money, and what he is doing in November 2026.
- Five deep dives in his profile: the 1994–95 escape step by step, the people around him (agent, gateway, mentors), what changed after him (posting system), what he does now, and his own words from interviews.
- "What fans are saying": first sample, the top 30 Yahoo! News Japan comments under the 17 Nov 2026 article about his Asian Hall of Fame photo, grouped into seven themes.
- New agent page: **Don Nomura (団野村)**, with timeline, a confidence-marked client table, method, criticism and defence, and his two American partners (Arn Tellem, Jean Afterman).
- `tools/build.py` now works for sports other than soccer. A data file can set its own table words (`labels`), summary tiles (`tiles`), chart scale (`chart_max`), extra season columns (`season_columns`), money chart title and home-page icon. Maya Yoshida's page is unchanged.

**Why**
- Nomo is the player who reopened the door from Japanese baseball to MLB, and his story is mostly about an agent finding a gap in the rules. It is the baseball mirror of the soccer gateway stories already here.

**Corrections to common beliefs**
- He was the second Japanese major leaguer, not the first (Masanori Murakami, 1964).
- A "six years, 2 billion yen" contract demand could not be found in any source; three different sourced versions are listed.
- Who paid Don Nomura, and how much, is not public.

## v0.2.7 — 2026-11-21
**Summary:** Changelog chart gains a grey line for total words on the site; page and word counts are now filled in automatically.  
**Pages on site:** 6  
**Words on site:** 16701  
**Time spent:** about 15 minutes

**What changed**
- The chart at the top now has two panels that share the same dates: pages on the site (blue) and total words on the site (grey).
- The table has a new "Words on site" column.
- Word counts for earlier versions were measured from the saved history of this repo. From now on the build tool counts pages and words for the newest entry by itself.

**Why**
- Page count stays flat when an existing page gets deeper. Word count shows that growth.

## v0.2.6 — 2026-11-21
**Summary:** Changelog chart now runs by date, to show progress over months and years.  
**Pages on site:** 6  
**Words on site:** 16701  
**Time spent:** about 10 minutes

**What changed**
- The line chart at the top of this file now has dates along the bottom (months, then years as time passes) instead of version numbers. There is one point for each day that had an update.

**Why**
- To track how the database grows over the year.

## v0.2.5 — 2026-11-21
**Summary:** Chart and summary table added at the top of this changelog.  
**Pages on site:** 6  
**Words on site:** 16701  
**Time spent:** about 10 minutes

**What changed**
- The top of `CHANGELOG.md` now has a line chart (pages on the site after each version) and a table with one line per version.
- Both are rebuilt automatically by `tools/build.py` from the entries below, so they stay up to date.

**Why**
- To see the history at a glance before reading the details.

## v0.2.4 — 2026-11-21
**Summary:** Left-side chapter menu on every page.  
**Pages on site:** 6  
**Words on site:** 16701  
**Time spent:** about 10 minutes

**What changed**
- Every page with three or more chapters now has a "Chapters" menu on the left side. Click a chapter to jump to it. The menu stays in view while you scroll and highlights the chapter you are reading.
- On a narrow screen or phone the menu moves to the top and can be folded away. It is hidden when printing.
- The menu is built automatically from each page's chapter headings, so new people and new sections get it with no extra work.

**Why**
- Profiles are getting long. This gives a quick snapshot of what is on the page and a fast way to move around.

## v0.2.3 — 2026-11-21
**Summary:** 'In his own words' section from Yoshida's X account.  
**Pages on site:** 6  
**Words on site:** 16701  
**Time spent:** about 10 minutes

**What changed**
- New section in Maya Yoshida's profile: "In his own words (social posts)", with three recent posts from his X account described and linked. Noted that he had posted nothing about leaving LA Galaxy as of this date.
- Template and build script updated so any athlete can have this section.

**Why**
- A person's own posts are first-hand statements and often come before news reports. They are kept apart from fan comments.

## v0.2.2 — 2026-11-21
**Summary:** 'What fans are saying' section from Yahoo! News Japan comments.  
**Pages on site:** 6  
**Words on site:** 16519  
**Time spent:** about 10 minutes

**What changed**
- New section in Maya Yoshida's profile: "What fans are saying (opinions, not facts)". First sample: the top 30 of 141 reader comments on Yahoo! News Japan under the article about him leaving LA Galaxy, grouped into seven themes.
- The section is clearly labelled as opinion, keeps no usernames and copies no comments.
- Template and build script updated so any athlete can have this section.

**Why**
- To see how ordinary fans react, without mixing their opinions with reported facts.

## v0.2.1 — 2026-11-21
**Summary:** Agents overview gets the story, trends and 2026 outlook; new pages for Hai Berden and Kees Ploegsma Jr.  
**New pages:** 🚪 Hai Berden, 🇳🇱 Kees Ploegsma Jr.  
**Pages on site:** 6  
**Words on site:** 16079  
**Time spent:** about 20 minutes

**What changed**
- Overview page: added the story of how Japanese players went overseas (seven steps, 1977 to today), the main trends pulling them to Europe, how agents and clubs find players in Japan, and what changes from 2026.
- New page: Hai Berden, the VVV-Venlo chairman who opened the Dutch door.
- New page: Kees Ploegsma Jr., the Dutch agent named in Honda's 2009 sale to CSKA Moscow.

**Why**
- To understand the gateway people behind Honda and Yoshida, and where the market is heading after the J.League's 2026 calendar change.

## v0.2.0 — 2026-11-21
**Summary:** New Agents folder: overview, Tetsuro Kiyooka and Thomas Kroth; Yoshida's agent details corrected.  
**New pages:** 🧭 How Japanese players get overseas: agents explained, 🤝 Tetsuro Kiyooka, 🇩🇪 Thomas Kroth  
**Pages on site:** 4  
**Words on site:** 13216  
**Time spent:** about 45 minutes (5 research helpers running in parallel)

**What changed**
- New `Agents/` folder with three pages:
  1. An overview: how Japanese players get overseas, who pays agents, gateways, rules and warnings.
  2. Tetsuro Kiyooka: timeline, a confidence-marked table of clients and transfers, how the Dutch door really opened, and the 2010 national team pay fight.
  3. Thomas Kroth: timeline, a confidence-marked table of Japanese transfers, his method, the Kagawa deal, who pays him, criticism and defence, and whether he is still the door to Germany.
- `tools/build.py` now builds any `Agents/<id>/data.json` into a profile and a web page, and the home page has an Agents section.
- Corrected Maya Yoshida's profile: the Dutch door was opened by VVV's chairman and a former Nagoya coach, not by the agent; his agent as of 2021 was CAA Base; no source shows Kiyooka working with Yoshida on union matters.

**Why**
- Agents are a key part of the story for Japanese athletes who play overseas, and the research showed that some popular beliefs about them are not supported by sources.

## v0.1.2 — 2026-11-21
**Summary:** Three deep dives for Yoshida: the Vera&John ad deal, being a target, sports agents.  
**Pages on site:** 1  
**Words on site:** 7170  
**Time spent:** about 25 minutes

**What changed**
- Added a "Deep dives" section to Maya Yoshida's profile with three topics:
  1. The Vera&John ad deal: who was involved, a timeline from 2021 to the 2025 law change, and lessons about the sports business.
  2. When he was a target (2013 to 2024) and how he came through it.
  3. Sports agents and Japanese players abroad: his own path, how the agent business works, his advice on agents, and the people who helped him.
- Updated the Vera&John entry with his management office's February 2025 statement and the contract end date (June 2023).
- `tools/build.py` and the player template now support deep dives.

**Why**
- To understand the pro sports industry: how sponsorship decisions are made, who carries the risk, and how agents shape a career abroad.

## v0.1.1 — 2026-11-21
**Summary:** Controversies and criticism section added to Yoshida and to the template.  
**Pages on site:** 1  
**Words on site:** 5100  
**Time spent:** about 10 minutes

**What changed**
- Added a new section to Maya Yoshida's profile: "Controversies and criticism" (6 items, each with a source and how it ended).
- Corrected the Vera&John sponsor years to 2021–2023 and linked it to the new section.
- Added the same section to the player template, so every future person gets a controversy check.
- `tools/build.py` now builds the new section for the profile and the web page.

**Why**
- A profile that only shows the good side is not honest. Result of the check: no real scandal found; the closest item is criticism of an online-casino-brand ad deal.

## v0.1.0 — 2026-11-21
**Summary:** First person added: Maya Yoshida profile, printable web page, build tool and template.  
**New pages:** ⚽ Maya Yoshida  
**Pages on site:** 1  
**Words on site:** 4618  
**Time spent:** about 1 hour (one Claude session, with 5 research helpers running in parallel)

**What changed**
- Created the `Sports/Soccer/` folder and a reusable player template.
- Added the first person: Maya Yoshida (吉田麻也). Leadership analysis, year-by-year timeline, season table, achievements, headline news in five languages, roots, personal events, money, and a video appendix.
- Added `tools/build.py`, which turns each person's `data.json` into a GitHub profile (`README.md`) and a printable colour web page in `docs/`.
- Added the web home page `docs/index.html`.

**Why**
- LA Galaxy announced on 20 Nov 2026 that Yoshida's contract had ended. I wanted to understand what made his leadership abroad special, and to start my own database of athletes I follow.
- One data file per person keeps the GitHub profile and the web page in step, and makes the next person quick to add.

**Known gaps**
- Direct YouTube links are not confirmed (search links are used).
- Europe and Japan salaries are estimates; only the MLS figures are official.
- See "Not verified" in the profile for the full list.
