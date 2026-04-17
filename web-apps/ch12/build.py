"""Build the Chapter 12 interactive dashboard.

Reads AED_HOUSE.DTA (29 houses) and AED_REALGDPPC.DTA (GDP growth),
pre-computes OLS regressions with default and robust SEs, ACF values,
and prediction interval components, then injects a compact JSON blob
into template.html -> dashboard.html.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.tsa.stattools import acf

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE = HERE / "template.html"
OUT_FILE = HERE / "dashboard.html"


def ols_fit(x: np.ndarray, y: np.ndarray) -> dict:
    """Compute OLS regression y = b0 + b1*x and return stats."""
    n = len(x)
    xbar = float(x.mean())
    ybar = float(y.mean())
    SSx = float(((x - xbar) ** 2).sum())
    SSxy = float(((x - xbar) * (y - ybar)).sum())
    b1 = SSxy / SSx
    b0 = ybar - b1 * xbar
    yhat = b0 + b1 * x
    residuals = y - yhat
    RSS = float((residuals ** 2).sum())
    se = float(np.sqrt(RSS / (n - 2)))
    SST = float(((y - ybar) ** 2).sum())
    R2 = 1 - RSS / SST if SST > 0 else 0.0
    return {
        "b0": round(b0, 4),
        "b1": round(b1, 4),
        "se": round(se, 4),
        "R2": round(R2, 4),
        "n": n,
        "xbar": round(xbar, 4),
        "SSx": round(SSx, 4),
    }


def load_house_data() -> dict:
    """Load AED_HOUSE.DTA and compute regressions."""
    df = pd.read_stata(DATA_DIR / "AED_HOUSE.DTA")

    # Raw data for scatter plots
    price = [round(float(v), 2) for v in df["price"]]
    size = [round(float(v), 2) for v in df["size"]]
    bedrooms = [round(float(v), 2) for v in df["bedrooms"]]
    bathrooms = [round(float(v), 2) for v in df["bathrooms"]]
    lotsize = [round(float(v), 2) for v in df["lotsize"]]
    age = [round(float(v), 2) for v in df["age"]]
    monthsold = [round(float(v), 2) for v in df["monthsold"]]

    # Simple regression: price ~ size
    simple = ols_fit(df["size"].values, df["price"].values)

    # Multiple regression with default and robust SEs
    vars_list = ["size", "bedrooms", "bathrooms", "lotsize", "age", "monthsold"]
    model_default = ols(
        "price ~ size + bedrooms + bathrooms + lotsize + age + monthsold",
        data=df,
    ).fit()
    model_robust = ols(
        "price ~ size + bedrooms + bathrooms + lotsize + age + monthsold",
        data=df,
    ).fit(cov_type="HC1")

    # Extract coefficients, default SEs, robust SEs
    multi_coefs = {}
    multi_se_default = {}
    multi_se_robust = {}
    multi_tstat_default = {}
    multi_tstat_robust = {}
    multi_pval_default = {}
    multi_pval_robust = {}

    all_vars = ["Intercept"] + vars_list
    for v in all_vars:
        multi_coefs[v] = round(float(model_default.params[v]), 4)
        multi_se_default[v] = round(float(model_default.bse[v]), 4)
        multi_se_robust[v] = round(float(model_robust.bse[v]), 4)
        multi_tstat_default[v] = round(float(model_default.tvalues[v]), 4)
        multi_tstat_robust[v] = round(float(model_robust.tvalues[v]), 4)
        multi_pval_default[v] = round(float(model_default.pvalues[v]), 6)
        multi_pval_robust[v] = round(float(model_robust.pvalues[v]), 6)

    rmse_multi = round(float(np.sqrt(model_default.mse_resid)), 4)
    r2_multi = round(float(model_default.rsquared), 4)

    # Residuals for diagnostics
    residuals_default = [round(float(v), 4) for v in model_default.resid]

    return {
        "price": price,
        "size": size,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "lotsize": lotsize,
        "age": age,
        "monthsold": monthsold,
        "n": len(df),
        "simple": simple,
        "vars": vars_list,
        "allVars": all_vars,
        "coefs": multi_coefs,
        "seDefault": multi_se_default,
        "seRobust": multi_se_robust,
        "tstatDefault": multi_tstat_default,
        "tstatRobust": multi_tstat_robust,
        "pvalDefault": multi_pval_default,
        "pvalRobust": multi_pval_robust,
        "rmseMulti": rmse_multi,
        "r2Multi": r2_multi,
        "residuals": residuals_default,
    }


def load_gdp_data() -> dict:
    """Load AED_REALGDPPC.DTA and compute ACF."""
    df = pd.read_stata(DATA_DIR / "AED_REALGDPPC.DTA")

    # Growth series (drop NaN)
    growth_series = df["growth"].dropna()
    growth = [round(float(v), 4) for v in growth_series]

    # Corresponding quarter indices for time axis
    valid_idx = growth_series.index.tolist()
    years = [round(float(df.loc[i, "year"]), 0) for i in valid_idx]
    quarters = [int(df.loc[i, "quarter"]) for i in valid_idx]

    # Create date-like labels: year + quarter fraction
    time_vals = [round(y + (q % 4) * 0.25, 2) for y, q in zip(years, quarters)]

    # ACF values
    acf_vals = acf(growth_series, nlags=20, fft=False)
    acf_list = [round(float(v), 6) for v in acf_vals]

    # Summary
    mean_growth = round(float(growth_series.mean()), 6)
    std_growth = round(float(growth_series.std()), 6)

    return {
        "growth": growth,
        "time": time_vals,
        "n": len(growth),
        "acf": acf_list,
        "meanGrowth": mean_growth,
        "stdGrowth": std_growth,
    }


def build_data() -> dict:
    house = load_house_data()
    gdp = load_gdp_data()
    return {
        "house": house,
        "gdp": gdp,
        "meta": {
            "chapter": "Chapter 12: Further Topics in Multiple Regression",
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
    h = data["house"]
    g = data["gdp"]
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")
    print(f"[check] house data: {h['n']} observations")
    print(
        f"[check] simple regression: b0={h['simple']['b0']:.4f} "
        f"b1={h['simple']['b1']:.4f} R2={h['simple']['R2']:.4f}"
    )
    print(
        f"[check] multi R2={h['r2Multi']:.4f} RMSE={h['rmseMulti']:.4f}"
    )
    print(f"[check] GDP growth: {g['n']} observations, mean={g['meanGrowth']:.4f}")
    print(f"[check] ACF lag 1: {g['acf'][1]:.4f}")


if __name__ == "__main__":
    main()
