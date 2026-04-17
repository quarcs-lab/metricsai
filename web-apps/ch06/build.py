"""Build the Chapter 06 interactive dashboard.

Reads AED_GENERATEDDATA.DTA (5-observation manual example) and the
Mendez 2020 convergence-clubs dataset (108 countries, 2014 cross-section),
pre-computes population OLS on the convergence data, and injects a compact
JSON blob into template.html → dashboard.html.
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

CONVERGENCE_URL = (
    "https://raw.githubusercontent.com/quarcs-lab/mendez2020-convergence-clubs-code-data"
    "/master/assets/dat.csv"
)
CONVERGENCE_CACHE = DATA_DIR / "mendez2020_convergence.csv"


def ols_fit(x: np.ndarray, y: np.ndarray) -> dict:
    """Compute OLS regression y = b1 + b2*x and return stats."""
    n = len(x)
    xbar = float(x.mean())
    ybar = float(y.mean())
    SSx = float(((x - xbar) ** 2).sum())
    SSxy = float(((x - xbar) * (y - ybar)).sum())
    b2 = SSxy / SSx
    b1 = ybar - b2 * xbar
    yhat = b1 + b2 * x
    residuals = y - yhat
    RSS = float((residuals ** 2).sum())
    se = float(np.sqrt(RSS / (n - 2)))
    se_b2 = se / np.sqrt(SSx)
    SST = float(((y - ybar) ** 2).sum())
    R2 = 1 - RSS / SST if SST > 0 else 0.0
    return {
        "b1": round(b1, 4),
        "b2": round(b2, 4),
        "se_b2": round(se_b2, 4),
        "se": round(se, 4),
        "R2": round(R2, 4),
        "n": n,
        "xbar": round(xbar, 4),
        "ybar": round(ybar, 4),
        "SSx": round(SSx, 4),
    }


def load_generated_data() -> dict:
    """Load the 5-observation generated dataset."""
    df = pd.read_stata(DATA_DIR / "AED_GENERATEDDATA.DTA")
    return {
        "x": [round(float(v), 4) for v in df["x"]],
        "y": [round(float(v), 4) for v in df["y"]],
        "Ey": [round(float(v), 4) for v in df["Eygivenx"]],
    }


def load_convergence_2014() -> dict:
    """Load convergence-clubs 2014 cross-section (108 countries)."""
    if CONVERGENCE_CACHE.exists():
        df = pd.read_csv(CONVERGENCE_CACHE)
    else:
        df = pd.read_csv(CONVERGENCE_URL)
        df.to_csv(CONVERGENCE_CACHE, index=False)
        print(f"[cache] saved {CONVERGENCE_CACHE.relative_to(ROOT)}")

    df2014 = df[df["year"] == 2014][["country", "GDPpc", "kl"]].dropna().copy()
    df2014.columns = ["country", "productivity", "capital"]

    x = df2014["capital"].values
    y = df2014["productivity"].values
    pop = ols_fit(x, y)

    return {
        "countries": df2014["country"].tolist(),
        "productivity": [round(float(v), 2) for v in y],
        "capital": [round(float(v), 2) for v in x],
        "popRegression": pop,
    }


def build_data() -> dict:
    gen = load_generated_data()
    conv = load_convergence_2014()
    return {
        "genData": gen,
        "convergence": conv,
        "dgp": {
            "beta1": 1,
            "beta2": 2,
            "sigmaU": 2,
            "muX": 3,
            "sigmaX": 1,
        },
        "reference": {
            "mc1000": {
                "b1_mean": 0.9960,
                "b1_sd": 1.2069,
                "b2_mean": 1.9944,
                "b2_sd": 0.3836,
            },
            "threeSamples": [
                {"b1": 0.82, "b2": 1.81},
                {"b1": 1.75, "b2": 1.79},
                {"b1": 2.01, "b2": 1.67},
            ],
        },
        "meta": {
            "chapter": "Chapter 06: The Least Squares Estimator",
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
    pop = data["convergence"]["popRegression"]
    n_countries = len(data["convergence"]["countries"])
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")
    print(f"[check] generated data: {len(data['genData']['x'])} observations")
    print(f"[check] convergence: {n_countries} countries (2014)")
    print(
        f"[check] pop regression: b1={pop['b1']:.4f} b2={pop['b2']:.4f} "
        f"se(b2)={pop['se_b2']:.4f} R2={pop['R2']:.4f}"
    )


if __name__ == "__main__":
    main()
