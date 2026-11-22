# Traffic (who visits)

GitHub only keeps 14 days of visit numbers for a repo. A small automatic job
(`.github/workflows/traffic.yml`) saves them here every day so the history is kept.

| File | What it holds |
|---|---|
| `views.csv` | Per day: how many times the repo page was opened, and by how many different people |
| `clones.csv` | Per day: how many times the whole repo was downloaded ("cloned"), and by how many different people or bots |
| `referrers.csv` | Daily snapshot: the top sites visitors came from (last 14 days) |
| `paths.csv` | Daily snapshot: the most-opened files (last 14 days) |

These are counts only. GitHub never says who the visitors were.
A sudden jump in `clones.csv` is the best sign that bots are copying the repo.

The job needs a secret named `TRAFFIC_TOKEN`: a fine-grained access token for this repo
with the permission **Administration: Read-only**. It expires after at most one year;
when the job starts failing, make a new token and replace the secret.

## Where to look

- Website visits: https://anishimori-news.goatcounter.com/ (sign in with the GoatCounter account). The code name is set in `tools/site_config.json`.
- Repo visits, last 14 days: https://github.com/anishimori123/News/graphs/traffic (only the owner can open it).
- Repo visits, full history: the CSV files in this folder.
