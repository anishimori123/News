# Changelog

## v0.2.0 — 2026-11-21
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
**Time spent:** about 10 minutes

**What changed**
- Added a new section to Maya Yoshida's profile: "Controversies and criticism" (6 items, each with a source and how it ended).
- Corrected the Vera&John sponsor years to 2021–2023 and linked it to the new section.
- Added the same section to the player template, so every future person gets a controversy check.
- `tools/build.py` now builds the new section for the profile and the web page.

**Why**
- A profile that only shows the good side is not honest. Result of the check: no real scandal found; the closest item is criticism of an online-casino-brand ad deal.

## v0.1.0 — 2026-11-21
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
