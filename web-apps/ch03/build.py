"""Build the Chapter 3 interactive dashboard.

Reads coin-toss and census sample-means .DTA datasets used in Chapter 3,
produces a compact JSON blob, and injects it into template.html,
writing the final self-contained HTML file to web-apps/ch03/dashboard.html.
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
    centered = arr - m
    skew = float(((centered**3).mean()) / (s**3)) if s > 0 else 0.0
    kurt = float(((centered**4).mean()) / (s**4) - 3) if s > 0 else 0.0
    return {
        "n": n,
        "mean": round(m, 6),
        "median": round(float(np.median(arr)), 6),
        "std": round(s, 6),
        "min": round(float(arr.min()), 6),
        "max": round(float(arr.max()), 6),
        "q1": round(float(np.quantile(arr, 0.25)), 6),
        "q3": round(float(np.quantile(arr, 0.75)), 6),
        "skew": round(skew, 4),
        "kurt": round(kurt, 4),
    }


def load_coin_tosses() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_COINTOSSMEANS.DTA")
    xbar = [round(float(x), 6) for x in df["xbar"]]
    stdev = [round(float(x), 6) for x in df["stdev"]]
    return {
        "xbar": xbar,
        "stdev": stdev,
        "n": int(df["numobs"].iloc[0]),
        "pop_mean": 0.5,
        "pop_sd": 0.5,
    }


def load_census_ages() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_CENSUSAGEMEANS.DTA")
    col = "mean" if "mean" in df.columns else "xmean"
    means = [round(float(x), 6) for x in df[col]]
    stdevs = [round(float(x), 6) for x in df["stdev"]]
    return {
        "mean": means,
        "stdev": stdevs,
        "n": int(df["numobs"].iloc[0]),
        "pop_mean": 24.13,
        "pop_sd": 18.61,
    }


def build_data() -> dict:
    coin = load_coin_tosses()
    census = load_census_ages()
    return {
        "coin": coin,
        "census": census,
        "summary": {
            "coin_xbar": summary_stats(coin["xbar"]),
            "census_mean": summary_stats(census["mean"]),
        },
        "meta": {
            "chapter": "Chapter 3: The Sample Mean",
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
    cs = data["summary"]["coin_xbar"]
    ce = data["summary"]["census_mean"]
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")
    print(
        f"[check] coin xbar: n={cs['n']} mean={cs['mean']:.4f} "
        f"std={cs['std']:.4f} (theoretical SE={0.5 / 30**0.5:.4f})"
    )
    print(
        f"[check] census mean: n={ce['n']} mean={ce['mean']:.2f} "
        f"std={ce['std']:.2f} (theoretical SE={18.61 / 25**0.5:.2f})"
    )


if __name__ == "__main__":
    main()
