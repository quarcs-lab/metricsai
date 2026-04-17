"""Build the Chapter 4 interactive dashboard.

Reads earnings, gas price, male earnings, and GDP growth .DTA datasets
used in Chapter 4, produces a compact JSON blob, and injects it into
template.html, writing the final self-contained HTML to dashboard.html.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE = HERE / "template.html"
OUT_FILE = HERE / "dashboard.html"


def summary_stats(values: list[float]) -> dict:
    arr = np.asarray([v for v in values if v is not None], dtype=float)
    n = len(arr)
    m = float(arr.mean())
    s = float(arr.std(ddof=1))
    return {
        "n": n,
        "mean": round(m, 4),
        "std": round(s, 4),
        "se": round(s / np.sqrt(n), 4),
        "min": round(float(arr.min()), 4),
        "max": round(float(arr.max()), 4),
        "median": round(float(np.median(arr)), 4),
    }


def load_earnings() -> list[int]:
    df = pd.read_stata(DATA_DIR / "AED_EARNINGS.DTA")
    return [int(x) for x in df["earnings"]]


def load_gas() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_GASPRICE.DTA")
    return {
        "prices": [round(float(x), 4) for x in df["price"]],
        "ca_avg": 3.81,
    }


def load_earnings_male() -> list[int]:
    df = pd.read_stata(DATA_DIR / "AED_EARNINGSMALE.DTA")
    return [int(x) for x in df["earnings"]]


def load_gdp_growth() -> list[float]:
    df = pd.read_stata(DATA_DIR / "AED_REALGDPPC.DTA")
    growth = df["growth"].dropna()
    return [round(float(x), 4) for x in growth]


def build_data() -> dict:
    earnings = load_earnings()
    gas = load_gas()
    earnings_male = load_earnings_male()
    gdp_growth = load_gdp_growth()
    return {
        "earnings": earnings,
        "gas": gas,
        "earnings_male": earnings_male,
        "gdp_growth": gdp_growth,
        "summary": {
            "earnings": summary_stats(earnings),
            "gas": summary_stats(gas["prices"]),
            "earnings_male": summary_stats(earnings_male),
            "gdp_growth": summary_stats(gdp_growth),
        },
        "meta": {
            "chapter": "Chapter 4: Statistical Inference for the Mean",
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

    rendered = template.replace("{{DATA_JSON}}", data_json)
    OUT_FILE.write_text(rendered, encoding="utf-8")

    size_kb = OUT_FILE.stat().st_size / 1024
    se = data["summary"]["earnings"]
    sg = data["summary"]["gas"]
    sm = data["summary"]["earnings_male"]
    sgd = data["summary"]["gdp_growth"]
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")
    print(
        f"[check] earnings: n={se['n']} mean=${se['mean']:,.2f} "
        f"sd=${se['std']:,.2f} se=${se['se']:,.2f}"
    )
    print(
        f"[check] gas: n={sg['n']} mean=${sg['mean']:.4f} "
        f"sd=${sg['std']:.4f} se=${sg['se']:.4f}"
    )
    print(
        f"[check] male earnings: n={sm['n']} mean=${sm['mean']:,.2f}"
    )
    print(
        f"[check] gdp growth: n={sgd['n']} mean={sgd['mean']:.4f}%"
    )


if __name__ == "__main__":
    main()
