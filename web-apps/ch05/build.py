"""Build the Chapter 5 interactive dashboard.

Reads AED_HOUSE.DTA, pre-computes regressions, LOWESS fits, synthetic
correlation data, and SS decomposition, then injects the JSON payload
into template.html → dashboard.html.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sp_stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE = HERE / "template.html"
OUT_FILE = HERE / "dashboard.html"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clean_list(series, decimals: int = 2) -> list[float]:
    return [round(float(v), decimals) for v in series]


def ols(x: np.ndarray, y: np.ndarray) -> dict:
    slope, intercept, r, _, _ = sp_stats.linregress(x, y)
    fitted = intercept + slope * x
    residuals = y - fitted
    y_mean = float(y.mean())
    tss = float(((y - y_mean) ** 2).sum())
    ess = float(((fitted - y_mean) ** 2).sum())
    rss = float((residuals ** 2).sum())
    se = float(np.sqrt(rss / (len(y) - 2)))
    return {
        "intercept": round(intercept, 2),
        "slope": round(slope, 6),
        "r": round(r, 4),
        "r_squared": round(r ** 2, 4),
        "se": round(se, 2),
        "fitted": [round(float(v), 2) for v in fitted],
        "residuals": [round(float(v), 2) for v in residuals],
        "tss": round(tss, 2),
        "ess": round(ess, 2),
        "rss": round(rss, 2),
        "y_mean": round(y_mean, 2),
    }


def lowess_fit(x: np.ndarray, y: np.ndarray, frac: float) -> dict:
    """LOWESS using statsmodels."""
    import statsmodels.api as sm
    result = sm.nonparametric.lowess(y, x, frac=frac)
    return {
        "x": [round(float(v), 2) for v in result[:, 0]],
        "y": [round(float(v), 2) for v in result[:, 1]],
    }


def kernel_smooth(x: np.ndarray, y: np.ndarray, bw: float) -> dict:
    """Nadaraya-Watson kernel regression with Gaussian kernel."""
    x_sorted = np.sort(x)
    x_grid = np.linspace(x_sorted[0], x_sorted[-1], 100)
    y_hat = np.zeros(len(x_grid))
    for i, xg in enumerate(x_grid):
        weights = np.exp(-0.5 * ((x - xg) / bw) ** 2)
        y_hat[i] = np.sum(weights * y) / np.sum(weights)
    return {
        "x": [round(float(v), 2) for v in x_grid],
        "y": [round(float(v), 2) for v in y_hat],
    }


# ---------------------------------------------------------------------------
# Dataset loaders
# ---------------------------------------------------------------------------

def load_house() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_HOUSE.DTA")
    return {
        "price": clean_list(df["price"], 0),
        "size": clean_list(df["size"], 0),
        "bedrooms": clean_list(df["bedrooms"], 0),
        "bathrooms": clean_list(df["bathrooms"], 0),
        "lotsize": clean_list(df["lotsize"], 2),
        "age": clean_list(df["age"], 0),
    }


def compute_regressions(house: dict) -> dict:
    price = np.array(house["price"])
    regs = {}
    for xvar in ["size", "bedrooms", "bathrooms", "lotsize", "age"]:
        x = np.array(house[xvar])
        regs[xvar] = ols(x, price)
    return regs


def compute_reverse_regression(house: dict) -> dict:
    price = np.array(house["price"])
    size = np.array(house["size"])
    return ols(price, size)


def compute_correlations(house: dict) -> dict:
    price = np.array(house["price"])
    corrs = {}
    for xvar in ["size", "bedrooms", "bathrooms", "lotsize", "age"]:
        x = np.array(house[xvar])
        r = float(np.corrcoef(price, x)[0, 1])
        corrs[xvar] = round(r, 4)
    return corrs


def generate_synthetic_r() -> dict:
    """Generate 21 synthetic datasets at target r = -1.0, -0.9, ..., 1.0."""
    np.random.seed(42)
    n = 30
    synth = {}
    for r_target_10 in range(-10, 11):
        r_target = r_target_10 / 10.0
        x = np.random.normal(3, 1, n)
        z = np.random.normal(0, 1, n)
        x_std = (x - x.mean()) / x.std()
        if abs(r_target) >= 0.999:
            y = x_std * (1 if r_target > 0 else -1)
        else:
            y = r_target * x_std + np.sqrt(1 - r_target ** 2) * z
        y = 5 + y  # shift to a reasonable range
        actual_r = float(np.corrcoef(x, y)[0, 1])
        synth[str(round(r_target, 1))] = {
            "x": [round(float(v), 3) for v in x],
            "y": [round(float(v), 3) for v in y],
            "actual_r": round(actual_r, 4),
        }
    return synth


def compute_lowess_fits(house: dict) -> dict:
    x = np.array(house["size"], dtype=float)
    y = np.array(house["price"], dtype=float)
    sort_idx = np.argsort(x)
    x_sorted = x[sort_idx]
    y_sorted = y[sort_idx]
    fits = {}
    for frac_pct in range(30, 105, 5):
        frac = frac_pct / 100.0
        fits[str(frac_pct)] = lowess_fit(x_sorted, y_sorted, frac)
    return fits


def compute_kernel_fits(house: dict) -> dict:
    x = np.array(house["size"], dtype=float)
    y = np.array(house["price"], dtype=float)
    x_std = x.std()
    fits = {}
    for bw_mult in [50, 100, 150, 200, 300]:
        bw = x_std * bw_mult / 100.0
        fits[str(bw_mult)] = kernel_smooth(x, y, bw)
    return fits


# ---------------------------------------------------------------------------
# Assemble JSON payload
# ---------------------------------------------------------------------------

def build_data() -> dict:
    house = load_house()
    regressions = compute_regressions(house)
    reverse = compute_reverse_regression(house)
    correlations = compute_correlations(house)
    synthetic_r = generate_synthetic_r()
    lowess = compute_lowess_fits(house)
    kernel = compute_kernel_fits(house)

    return {
        "house": house,
        "regression": regressions,
        "reverse": reverse,
        "correlation": correlations,
        "synthetic_r": synthetic_r,
        "lowess": lowess,
        "kernel": kernel,
        "meta": {
            "chapter": "Chapter 5: Bivariate Data Summary",
            "book": "metricsAI: An Introduction to Econometrics with Python and AI in the Cloud",
            "author": "Carlos Mendez",
        },
    }


# ---------------------------------------------------------------------------
# Template injection
# ---------------------------------------------------------------------------

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
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")

    # Sanity checks matching chapter prose
    reg = data["regression"]["size"]
    corr = data["correlation"]["size"]
    print(f"[check] mean price = ${np.mean(data['house']['price']):,.2f} (chapter: $253,910.34)")
    print(f"[check] mean size = {np.mean(data['house']['size']):,.2f} sqft (chapter: 1,882.76)")
    print(f"[check] r(price, size) = {corr} (chapter: 0.7858)")
    print(f"[check] slope = {reg['slope']} (chapter: 73.771)")
    print(f"[check] intercept = {reg['intercept']} (chapter: 115,017.28)")
    print(f"[check] R² = {reg['r_squared']} (chapter: 0.6175)")
    print(f"[check] SE = {reg['se']} (chapter: 23,550.66)")
    rev = data["reverse"]
    print(f"[check] reverse slope = {rev['slope']} (chapter: 0.00837)")
    print(f"[check] 1/forward slope = {round(1/reg['slope'], 6)} ≠ reverse slope")


if __name__ == "__main__":
    main()
