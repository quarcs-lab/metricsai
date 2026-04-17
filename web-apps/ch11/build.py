"""Build the Chapter 11 interactive dashboard.

Reads AED_HOUSE.DTA (29 houses in Davis, CA), runs three progressive
OLS models with standard and robust SEs, and injects pre-computed
results into template.html.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE = HERE / "template.html"
OUT_FILE = HERE / "dashboard.html"


def ols_pair(y, X, var_names):
    """Run OLS with both standard and HC1 SEs; return serializable dict."""
    m = sm.OLS(y, X).fit()
    mr = sm.OLS(y, X).fit(cov_type="HC1")
    return {
        "vars": var_names,
        "coef": [round(float(c), 2) for c in m.params],
        "se": [round(float(s), 2) for s in m.bse],
        "se_robust": [round(float(s), 2) for s in mr.bse],
        "t": [round(float(t), 4) for t in m.tvalues],
        "t_robust": [round(float(t), 4) for t in mr.tvalues],
        "p": [round(float(p), 6) for p in m.pvalues],
        "p_robust": [round(float(p), 6) for p in mr.pvalues],
        "r2": round(float(m.rsquared), 4),
        "r2_adj": round(float(m.rsquared_adj), 4),
        "f_stat": round(float(m.fvalue), 4),
        "f_pvalue": round(float(m.f_pvalue), 6),
        "n": int(m.nobs),
        "k": len(var_names),
        "df_resid": int(m.df_resid),
        "rss": round(float(np.sum(m.resid ** 2)), 2),
    }


def build_data() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_HOUSE.DTA")
    y = df["price"].values.astype(float)
    n = len(y)

    def cols(*names):
        return sm.add_constant(df[list(names)].astype(float))

    all_vars = ["size", "bedrooms", "bathrooms", "lotsize", "age", "monthsold"]

    # Three models
    m1 = ols_pair(y, cols("size"), ["const", "size"])
    m1["name"] = "Size only"

    m2 = ols_pair(y, cols("size", "bedrooms"), ["const", "size", "bedrooms"])
    m2["name"] = "Size + Bedrooms"

    m3 = ols_pair(y, cols(*all_vars), ["const"] + all_vars)
    m3["name"] = "Full model"

    # Subset F-test: full vs size-only
    rss_r = m1["rss"]
    rss_u = m3["rss"]
    q = len(all_vars) - 1  # 5 restrictions
    f_sub = ((rss_r - rss_u) / q) / (rss_u / m3["df_resid"])
    subset_ftest = {
        "q": q,
        "df_resid": m3["df_resid"],
        "f_stat": round(float(f_sub), 4),
        "rss_restricted": rss_r,
        "rss_unrestricted": rss_u,
    }

    # Correlation matrix for multicollinearity display
    corr_data = df[all_vars].astype(float).corr()
    correlations = {}
    for v1 in all_vars:
        for v2 in all_vars:
            if v1 < v2:
                correlations[f"{v1}__{v2}"] = round(float(corr_data.loc[v1, v2]), 4)

    # Raw data for scatter
    scatter = {v: [round(float(x), 2) for x in df[v]] for v in ["price"] + all_vars}

    return {
        "scatter": scatter,
        "models": [m1, m2, m3],
        "subset_ftest": subset_ftest,
        "correlations": correlations,
        "meta": {
            "chapter": "Chapter 11: Statistical Inference for Multiple Regression",
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
    m1 = data["models"][0]
    m3 = data["models"][2]
    sf = data["subset_ftest"]
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")
    print(
        f"[check] Model 1: size=${m1['coef'][1]:.2f}/sqft "
        f"(t={m1['t'][1]:.2f}), R²={m1['r2']:.4f}"
    )
    print(
        f"[check] Model 3: size=${m3['coef'][1]:.2f}/sqft "
        f"(se={m3['se'][1]:.2f}), R²={m3['r2']:.4f}, F={m3['f_stat']:.2f}"
    )
    print(f"[check] Subset F-test: F={sf['f_stat']:.4f} (q={sf['q']})")


if __name__ == "__main__":
    main()
