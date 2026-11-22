#!/usr/bin/env python3
"""Save GitHub's repo traffic numbers so they are not lost after 14 days.

GitHub only keeps 14 days of traffic. This script is run once a day by
.github/workflows/traffic.yml. It reads the four JSON files the workflow
downloaded and adds any new days to the CSV files in traffic/.

Run by hand:  python tools/save_traffic.py <folder with views.json, clones.json, referrers.json, paths.json>
Needs only Python 3.
"""
import csv
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "traffic"


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def merge_daily(name, data, key):
    """One row per day: date, total, unique people. A newer reading of the same day replaces the old one."""
    if not isinstance(data, dict) or key not in data:
        print(f"skip {name}: no data (is the TRAFFIC_TOKEN secret set?)")
        return False
    f = OUT / f"{name}.csv"
    rows = {}
    if f.exists():
        for r in csv.DictReader(f.open(encoding="utf-8")):
            rows[r["date"]] = (int(r["count"]), int(r["unique"]))
    for d in data[key]:
        day = d["timestamp"][:10]
        old = rows.get(day, (0, 0))
        rows[day] = (max(old[0], d["count"]), max(old[1], d["uniques"]))
    with f.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date", "count", "unique"])
        for day in sorted(rows):
            w.writerow([day, *rows[day]])
    return True


def append_snapshot(name, data, label):
    """Top-10 lists (where visitors came from, which files they opened), one snapshot per day."""
    if not isinstance(data, list):
        print(f"skip {name}: no data")
        return
    f = OUT / f"{name}.csv"
    today = date.today().isoformat()
    old = []
    if f.exists():
        old = [r for r in csv.reader(f.open(encoding="utf-8"))][1:]
        old = [r for r in old if r and r[0] != today]
    with f.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["snapshot_date", label, "count_14_days", "unique_14_days"])
        w.writerows(old)
        for d in data:
            w.writerow([today, d.get(label) or d.get("path", ""), d["count"], d["uniques"]])


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    OUT.mkdir(exist_ok=True)
    ok = merge_daily("views", load(src / "views.json"), "views")
    ok = merge_daily("clones", load(src / "clones.json"), "clones") and ok
    append_snapshot("referrers", load(src / "referrers.json"), "referrer")
    append_snapshot("paths", load(src / "paths.json"), "path")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
