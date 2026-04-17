"""Fetch U.S. GDP per capita (1820 → latest) from the Maddison Project Database.

Pulls the Our World in Data CSV mirror, filters to the United States from 1820
onwards, and writes a slim CSV to data/maddison_us_gdppc.csv. Rerun manually
whenever you want to refresh the extract; the main build script reads the
committed CSV and stays offline.

Citation: Bolt, J. & van Zanden, J. L. (2024). Maddison style estimates of the
evolution of the world economy: A new 2023 update. Journal of Economic Surveys.
"""

from __future__ import annotations

import csv
import io
import sys
import urllib.request
from pathlib import Path

OWID_URL = (
    "https://ourworldindata.org/grapher/"
    "gdp-per-capita-maddison-project-database.csv"
)
FALLBACK_URL = "https://dataverse.nl/api/access/datafile/421302"  # xlsx, needs UA
OUT = Path(__file__).resolve().parent.parent / "data" / "maddison_us_gdppc.csv"


def fetch_csv(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "metricsai/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def extract_us(raw: str) -> list[tuple[int, float]]:
    reader = csv.DictReader(io.StringIO(raw))
    rows: list[tuple[int, float]] = []
    # OWID headers: Entity, Code, Year, "GDP per capita", "GDP per capita (Annotations)"
    year_col = "Year"
    gdp_col = next(
        (c for c in reader.fieldnames or [] if c.lower().startswith("gdp per capita")),
        None,
    )
    if gdp_col is None:
        raise SystemExit(f"Could not find GDP column; got {reader.fieldnames}")
    for row in reader:
        if row.get("Entity") != "United States":
            continue
        try:
            year = int(row[year_col])
            val = float(row[gdp_col])
        except (TypeError, ValueError):
            continue
        if year >= 1820:
            rows.append((year, val))
    rows.sort(key=lambda r: r[0])
    return rows


def main() -> None:
    print(f"[fetch] {OWID_URL}")
    raw = fetch_csv(OWID_URL)
    rows = extract_us(raw)
    if not rows:
        raise SystemExit("No U.S. rows found in OWID CSV")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "gdppc"])
        for year, val in rows:
            w.writerow([year, round(val, 1)])

    first_year, first_val = rows[0]
    last_year, last_val = rows[-1]
    print(f"[ok] wrote {OUT.relative_to(OUT.parent.parent)} ({len(rows)} rows)")
    print(f"     {first_year}: ${first_val:,.0f}   {last_year}: ${last_val:,.0f}")
    print("     source: Maddison Project 2023 via Our World in Data")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[error] {exc}", file=sys.stderr)
        raise
