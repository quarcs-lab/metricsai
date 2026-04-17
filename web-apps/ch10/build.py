"""Build the Chapter 10 interactive dashboard.

Reads AED_HOUSE.DTA, pre-computes all 63 possible OLS models (6 predictors),
correlation matrix, VIF values, and FWL demonstration data, then injects
the JSON payload into template.html → dashboard.html.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats as sp_stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE = HERE / "template.html"
OUT_FILE = HERE / "dashboard.html"

PREDICTORS = ["size", "bedrooms", "bathrooms", "lotsize", "age", "monthsold"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clean_list(series, decimals: int = 2) -> list[float]:
    return [round(float(v), decimals) for v in series]


def model_key(vars_list: list[str]) -> str:
    return ",".join(sorted(vars_list))


# ---------------------------------------------------------------------------
# Dataset loader
# ---------------------------------------------------------------------------

def load_house() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_HOUSE.DTA")
    return {
        "price": clean_list(df["price"], 0),
        "size": clean_list(df["size"], 0),
        "bedrooms": clean_list(df["bedrooms"], 0),
        "bathrooms": clean_list(df["bathrooms"], 1),
        "lotsize": clean_list(df["lotsize"], 2),
        "age": clean_list(df["age"], 0),
        "monthsold": clean_list(df["monthsold"], 0),
    }


# ---------------------------------------------------------------------------
# Compute all 63 OLS models
# ---------------------------------------------------------------------------

def compute_all_models(house: dict) -> dict:
    df = pd.DataFrame(house)
    y = df["price"].values
    models = {}

    for k in range(1, len(PREDICTORS) + 1):
        for combo in combinations(PREDICTORS, k):
            vars_list = list(combo)
            key = model_key(vars_list)
            X = sm.add_constant(df[vars_list])
            fit = sm.OLS(y, X).fit()

            coefs = {}
            se = {}
            tvals = {}
            pvals = {}
            ci_lo = {}
            ci_hi = {}
            conf = fit.conf_int(alpha=0.05)
            for i, name in enumerate(fit.model.exog_names):
                label = name if name != "const" else "const"
                coefs[label] = round(float(fit.params.iloc[i]), 4)
                se[label] = round(float(fit.bse.iloc[i]), 4)
                tvals[label] = round(float(fit.tvalues.iloc[i]), 4)
                pvals[label] = round(float(fit.pvalues.iloc[i]), 4)
                ci_lo[label] = round(float(conf.iloc[i, 0]), 2)
                ci_hi[label] = round(float(conf.iloc[i, 1]), 2)

            models[key] = {
                "vars": vars_list,
                "coefs": coefs,
                "se": se,
                "tvals": tvals,
                "pvals": pvals,
                "ci_lo": ci_lo,
                "ci_hi": ci_hi,
                "r2": round(float(fit.rsquared), 4),
                "adj_r2": round(float(fit.rsquared_adj), 4),
                "aic": round(float(fit.aic), 2),
                "bic": round(float(fit.bic), 2),
                "rmse": round(float(np.sqrt(fit.mse_resid)), 2),
                "n": int(fit.nobs),
                "k": len(vars_list) + 1,  # including constant
                "fitted": [round(float(v), 2) for v in fit.fittedvalues],
                "residuals": [round(float(v), 2) for v in fit.resid],
            }

    return models


# ---------------------------------------------------------------------------
# Correlation matrix
# ---------------------------------------------------------------------------

def compute_correlations(house: dict) -> dict:
    df = pd.DataFrame(house)
    cols = ["price"] + PREDICTORS
    corr = df[cols].corr()
    return {
        "columns": cols,
        "matrix": [[round(float(corr.iloc[i, j]), 4)
                     for j in range(len(cols))]
                    for i in range(len(cols))],
    }


# ---------------------------------------------------------------------------
# VIF for full model and progressive models
# ---------------------------------------------------------------------------

def compute_vif(house: dict) -> dict:
    df = pd.DataFrame(house)
    results = {}

    # VIF for full model
    X_full = df[PREDICTORS].values
    full_vif = {}
    for i, col in enumerate(PREDICTORS):
        full_vif[col] = round(float(variance_inflation_factor(X_full, i)), 2)
    results["full"] = full_vif

    # VIF for progressively smaller models
    for drop_var in PREDICTORS:
        remaining = [v for v in PREDICTORS if v != drop_var]
        if len(remaining) < 2:
            continue
        X_sub = df[remaining].values
        sub_vif = {}
        for i, col in enumerate(remaining):
            sub_vif[col] = round(float(variance_inflation_factor(X_sub, i)), 2)
        results["drop_" + drop_var] = sub_vif

    return results


# ---------------------------------------------------------------------------
# Assemble JSON payload
# ---------------------------------------------------------------------------

def build_data() -> dict:
    house = load_house()
    models = compute_all_models(house)
    correlations = compute_correlations(house)
    vif = compute_vif(house)

    return {
        "house": house,
        "models": models,
        "correlations": correlations,
        "vif": vif,
        "predictors": PREDICTORS,
        "meta": {
            "chapter": "Chapter 10: Data Summary for Multiple Regression",
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

    # Sanity checks
    m_size = data["models"]["size"]
    m_full = data["models"][model_key(PREDICTORS)]
    m_sb = data["models"][model_key(["size", "bedrooms"])]
    m_bed = data["models"]["bedrooms"]

    print(f"[check] n = {m_full['n']} houses")
    print(f"[check] bivariate bedrooms coef = ${m_bed['coefs']['bedrooms']:,.2f} (chapter: $23,667)")
    print(f"[check] multiple bedrooms coef (size+bed) = ${m_sb['coefs']['bedrooms']:,.2f} (chapter: $1,553)")
    print(f"[check] simple R² (size) = {m_size['r2']} (chapter: 0.6175)")
    print(f"[check] simple adj R² (size) = {m_size['adj_r2']} (chapter: 0.6033)")
    print(f"[check] full R² = {m_full['r2']} (chapter: 0.6506)")
    print(f"[check] full adj R² = {m_full['adj_r2']} (chapter: 0.5552)")
    print(f"[check] full AIC = {m_full['aic']} (chapter: 675.48)")
    print(f"[check] full BIC = {m_full['bic']} (chapter: 685.05)")
    print(f"[check] full size coef = ${m_full['coefs']['size']:.2f}/sqft (chapter: $68.37)")
    print(f"[check] total models pre-computed: {len(data['models'])}")


if __name__ == "__main__":
    main()
