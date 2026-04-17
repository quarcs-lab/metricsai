"""Build the Chapter 1 interactive dashboard.

Reads AED_HOUSE.DTA, pre-computes OLS regressions for each predictor,
and injects the payload into scripts/ch01_webapp_template.html.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE = Path(__file__).resolve().parent / "ch01_webapp_template.html"
OUT_DIR = ROOT / "web-apps" / "ch01"
OUT_FILE = OUT_DIR / "dashboard.html"


def summary_stats(values: list[float]) -> dict:
    arr = np.asarray(values, dtype=float)
    m = float(arr.mean())
    s = float(arr.std(ddof=1))
    centered = arr - m
    skew = float(((centered ** 3).mean()) / (s ** 3)) if s > 0 else 0.0
    kurt = float(((centered ** 4).mean()) / (s ** 4) - 3) if s > 0 else 0.0
    return {
        "n": len(arr), "mean": m, "median": float(np.median(arr)),
        "std": s, "min": float(arr.min()), "max": float(arr.max()),
        "q1": float(np.quantile(arr, 0.25)),
        "q3": float(np.quantile(arr, 0.75)),
        "skew": skew, "kurt": kurt,
    }


def ols(x: np.ndarray, y: np.ndarray) -> dict:
    mx, my = x.mean(), y.mean()
    slope = float(((x - mx) * (y - my)).sum() / ((x - mx) ** 2).sum())
    intercept = float(my - slope * mx)
    yhat = intercept + slope * x
    ss_res = float(((y - yhat) ** 2).sum())
    ss_tot = float(((y - my) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    n = len(x)
    se_slope = float(np.sqrt(ss_res / (n - 2) / ((x - mx) ** 2).sum()))
    residuals = [round(float(v), 2) for v in (y - yhat)]
    return {
        "intercept": round(intercept, 2),
        "slope": round(slope, 4),
        "r2": round(r2, 4),
        "se_slope": round(se_slope, 4),
        "residuals": residuals,
    }


def build_data() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_HOUSE.DTA")

    price = [int(v) for v in df["price"]]
    size = [int(v) for v in df["size"]]
    bedrooms = [int(v) for v in df["bedrooms"]]
    bathrooms = [float(v) for v in df["bathrooms"]]
    lotsize = [int(v) for v in df["lotsize"]]
    age = [round(float(v), 1) for v in df["age"]]

    price_arr = np.array(price, dtype=float)
    predictors = {
        "size": {"values": size, "label": "Size (sq ft)", "short": "Size"},
        "bedrooms": {"values": bedrooms, "label": "Bedrooms", "short": "Bedrooms"},
        "bathrooms": {"values": bathrooms, "label": "Bathrooms", "short": "Baths"},
        "lotsize": {"values": lotsize, "label": "Lot size (units)", "short": "Lot size"},
        "age": {"values": age, "label": "Age (years)", "short": "Age"},
    }

    regressions = {}
    for key, info in predictors.items():
        x = np.array(info["values"], dtype=float)
        reg = ols(x, price_arr)
        regressions[key] = {**reg, "label": info["label"], "short": info["short"]}

    return {
        "price": price,
        "predictors": {k: v["values"] for k, v in predictors.items()},
        "predictor_labels": {k: v["label"] for k, v in predictors.items()},
        "predictor_short": {k: v["short"] for k, v in predictors.items()},
        "regressions": regressions,
        "summary": {
            "price": summary_stats(price),
            "size": summary_stats(size),
            "bedrooms": summary_stats(bedrooms),
        },
        "meta": {
            "chapter": "Chapter 1: Analysis of Economics Data",
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
    r = data["regressions"]["size"]
    s = data["summary"]["price"]
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")
    print(
        f"[check] price: n={s['n']} mean={s['mean']:,.2f} "
        f"(chapter says $253,910)"
    )
    print(
        f"[check] OLS price~size: intercept={r['intercept']:,.2f} "
        f"slope={r['slope']:.4f} R2={r['r2']:.4f}"
    )
    print(f"        (chapter: intercept=$115,017 slope=$73.77 R2=0.6175)")


if __name__ == "__main__":
    main()
