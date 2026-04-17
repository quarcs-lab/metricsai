"""Build the Chapter 2 interactive dashboard.

Reads the five .DTA datasets used in Chapter 2, produces a compact JSON blob,
and injects it into scripts/ch02_webapp_template.html, writing the final
self-contained HTML file to web-apps/ch02/dashboard.html.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE = Path(__file__).resolve().parent / "ch02_webapp_template.html"
OUT_DIR = ROOT / "web-apps" / "ch02"
OUT_FILE = OUT_DIR / "dashboard.html"


def iso_dates(series: pd.Series) -> list[str]:
    return [d.strftime("%Y-%m-%d") for d in pd.to_datetime(series)]


def load_earnings() -> list[int]:
    df = pd.read_stata(DATA_DIR / "AED_EARNINGS.DTA")
    return [int(x) for x in df["earnings"].tolist()]


def load_gdp() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_REALGDPPC.DTA")
    df = df.dropna(subset=["realgdppc"]).reset_index(drop=True)
    # NBER recession quarters covered by this sample (start, end as YYYY-MM-DD).
    recessions = [
        ["1960-04-01", "1961-02-01"],
        ["1969-12-01", "1970-11-01"],
        ["1973-11-01", "1975-03-01"],
        ["1980-01-01", "1980-07-01"],
        ["1981-07-01", "1982-11-01"],
        ["1990-07-01", "1991-03-01"],
        ["2001-03-01", "2001-11-01"],
        ["2007-12-01", "2009-06-01"],
        ["2020-02-01", "2020-04-01"],
    ]
    return {
        "dates": iso_dates(df["daten"]),
        "values": [round(float(v), 2) for v in df["realgdppc"]],
        "recessions": recessions,
    }


def load_health() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_HEALTHCATEGORIES.DTA")
    df = df.sort_values("expenditures", ascending=False).reset_index(drop=True)
    categories = [str(c).strip() for c in df["category"].tolist()]
    # cat_short in the source .DTA is partly blank / mislabeled; derive short labels from category
    short_map = {
        "Hospital": "Hospital",
        "Physician and clinical": "Physician",
        "Other Professional": "Other prof.",
        "Dental": "Dental",
        "Other Health & Personal": "Other health",
        "Home Health Care": "Home health",
        "Nursing Care": "Nursing",
        "Drugs & Supplies": "Drugs",
        "Govt. Administration": "Govt admin",
        "Net Cost Insurance": "Insurance",
        "Govt. Public Health": "Public health",
        "Noncommercial Research": "Research",
        "Structures & Equipment": "Structures",
    }
    short = [short_map.get(c, c) for c in categories]
    return {
        "categories": categories,
        "short": short,
        "values": [int(v) for v in df["expenditures"].tolist()],
    }


def load_fishing() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_FISHING.DTA")
    counts = df["mode"].value_counts()
    ordered = counts.sort_values(ascending=False)
    return {
        "modes": [str(m) for m in ordered.index.tolist()],
        "counts": [int(c) for c in ordered.values.tolist()],
    }


def load_maddison_us() -> dict:
    """Load the committed Maddison Project extract for the U.S."""
    import csv as _csv

    path = DATA_DIR / "maddison_us_gdppc.csv"
    if not path.exists():
        raise SystemExit(
            f"{path.name} not found. Run: python3 scripts/fetch_maddison_us.py"
        )
    years: list[int] = []
    values: list[float] = []
    with path.open(encoding="utf-8") as f:
        for row in _csv.DictReader(f):
            years.append(int(row["year"]))
            values.append(round(float(row["gdppc"]), 1))
    return {
        "years": years,
        "values": values,
        "source": "Maddison Project 2023 (Bolt & van Zanden)",
    }


def load_home_sales() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_MONTHLYHOMESALES.DTA")
    df = df.sort_values("daten").reset_index(drop=True)

    def clean(col: str) -> list[float | None]:
        return [None if pd.isna(v) else round(float(v), 1) for v in df[col]]

    return {
        "dates": iso_dates(df["daten"]),
        "original": clean("exsales"),
        "ma11": clean("exsales_ma11"),
        "sa": clean("exsales_sa"),
    }


def summary_stats(values: list[float]) -> dict:
    arr = np.asarray([v for v in values if v is not None], dtype=float)
    n = len(arr)
    mean = float(arr.mean())
    std = float(arr.std(ddof=1))
    centered = arr - mean
    skew = float(((centered ** 3).mean()) / (std ** 3)) if std > 0 else 0.0
    kurt = float(((centered ** 4).mean()) / (std ** 4) - 3) if std > 0 else 0.0
    return {
        "n": n,
        "mean": mean,
        "median": float(np.median(arr)),
        "std": std,
        "min": float(arr.min()),
        "max": float(arr.max()),
        "q1": float(np.quantile(arr, 0.25)),
        "q3": float(np.quantile(arr, 0.75)),
        "skew": skew,
        "kurt": kurt,
    }


def build_data() -> dict:
    earnings = load_earnings()
    gdp = load_gdp()
    home_sales = load_home_sales()
    return {
        "earnings": earnings,
        "gdp": gdp,
        "gdp_long": load_maddison_us(),
        "health": load_health(),
        "fishing": load_fishing(),
        "home_sales": home_sales,
        "summary": {
            "earnings": summary_stats(earnings),
            "gdp": summary_stats(gdp["values"]),
            "home_sales": summary_stats([v for v in home_sales["original"] if v is not None]),
        },
        "meta": {
            "chapter": "Chapter 2: Univariate Data Summary",
            "book": "metricsAI: An Introduction to Econometrics with Python and AI in the Cloud",
            "author": "Carlos Mendez",
        },
    }


def main() -> None:
    if not TEMPLATE.exists():
        raise SystemExit(f"Template not found: {TEMPLATE}")

    data = build_data()
    data_json = json.dumps(data, separators=(",", ":"), ensure_ascii=False)

    template = TEMPLATE.read_text(encoding="utf-8")
    if "{{DATA_JSON}}" not in template:
        raise SystemExit("Placeholder {{DATA_JSON}} not found in template")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rendered = template.replace("{{DATA_JSON}}", data_json)
    OUT_FILE.write_text(rendered, encoding="utf-8")

    size_kb = OUT_FILE.stat().st_size / 1024
    s = data["summary"]["earnings"]
    gl = data["gdp_long"]
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")
    print(
        f"[check] earnings: n={s['n']} mean={s['mean']:.2f} "
        f"median={s['median']:.0f} std={s['std']:.0f} "
        f"skew={s['skew']:.2f} kurt={s['kurt']:.2f}"
    )
    print(
        f"[check] maddison US: n={len(gl['years'])} "
        f"{gl['years'][0]}=${gl['values'][0]:,.0f} → "
        f"{gl['years'][-1]}=${gl['values'][-1]:,.0f}"
    )


if __name__ == "__main__":
    main()
