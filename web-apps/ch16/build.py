"""Build the Chapter 16 interactive dashboard.

Reads AED_EARNINGS_COMPLETE.DTA (872 workers) and AED_DEMOCRACY.DTA (131 countries),
pre-computes OLS regressions, VIF values, influence diagnostics, and injects
a compact JSON blob into template.html -> dashboard.html.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import variance_inflation_factor, OLSInfluence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE = HERE / "template.html"
OUT_FILE = HERE / "dashboard.html"

GITHUB_DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"


def ols_fit_simple(x: np.ndarray, y: np.ndarray) -> dict:
    """Compute OLS y = b0 + b1*x and return stats."""
    n = len(x)
    xbar = float(x.mean())
    ybar = float(y.mean())
    SSx = float(((x - xbar) ** 2).sum())
    SSxy = float(((x - xbar) * (y - ybar)).sum())
    b1 = SSxy / SSx
    b0 = ybar - b1 * xbar
    yhat = b0 + b1 * x
    resid = y - yhat
    RSS = float((resid ** 2).sum())
    SST = float(((y - ybar) ** 2).sum())
    se = float(np.sqrt(RSS / (n - 2)))
    se_b1 = se / np.sqrt(SSx)
    R2 = 1 - RSS / SST if SST > 0 else 0.0
    return {
        "b0": round(b0, 6),
        "b1": round(b1, 6),
        "se_b1": round(se_b1, 6),
        "R2": round(R2, 6),
        "n": n,
    }


def load_earnings() -> dict:
    """Load earnings data and compute VIF / regression results."""
    df = pd.read_stata(DATA_DIR / "AED_EARNINGS_COMPLETE.DTA")

    # Base model: earnings ~ age + education
    m_base = ols("earnings ~ age + education", data=df).fit()
    m_base_rob = ols("earnings ~ age + education", data=df).fit(cov_type="HC1")

    # Collinear model: earnings ~ age + education + agebyeduc
    m_coll = ols("earnings ~ age + education + agebyeduc", data=df).fit()
    m_coll_rob = ols("earnings ~ age + education + agebyeduc", data=df).fit(cov_type="HC1")

    # VIF for base model
    X_base = sm.add_constant(df[["age", "education"]])
    vif_base = {
        "age": round(variance_inflation_factor(X_base.values, 1), 2),
        "education": round(variance_inflation_factor(X_base.values, 2), 2),
    }

    # VIF for collinear model
    X_coll = sm.add_constant(df[["age", "education", "agebyeduc"]])
    vif_coll = {
        "age": round(variance_inflation_factor(X_coll.values, 1), 2),
        "education": round(variance_inflation_factor(X_coll.values, 2), 2),
        "agebyeduc": round(variance_inflation_factor(X_coll.values, 3), 2),
    }

    # Correlation matrix
    corr = df[["age", "education", "agebyeduc"]].corr()
    corr_dict = {
        "vars": ["age", "education", "agebyeduc"],
        "matrix": [[round(corr.iloc[i, j], 4) for j in range(3)] for i in range(3)],
    }

    # SE comparison (standard vs robust)
    se_compare = {}
    for var in ["Intercept", "age", "education"]:
        se_compare[var] = {
            "standard": round(float(m_base.bse[var]), 2),
            "robust": round(float(m_base_rob.bse[var]), 2),
            "ratio": round(float(m_base_rob.bse[var] / m_base.bse[var]), 4),
        }

    # Residuals for heteroskedasticity visualization
    yhat_base = m_base.fittedvalues.values
    resid_base = m_base.resid.values

    return {
        "n": len(df),
        "age": [round(float(v), 1) for v in df["age"]],
        "education": [round(float(v), 1) for v in df["education"]],
        "earnings": [round(float(v), 0) for v in df["earnings"]],
        "agebyeduc": [round(float(v), 1) for v in df["agebyeduc"]],
        "baseModel": {
            "params": {k: round(float(v), 4) for k, v in m_base.params.items()},
            "se_standard": {k: round(float(v), 4) for k, v in m_base.bse.items()},
            "se_robust": {k: round(float(v), 4) for k, v in m_base_rob.bse.items()},
            "R2": round(float(m_base.rsquared), 4),
        },
        "collinearModel": {
            "params": {k: round(float(v), 4) for k, v in m_coll.params.items()},
            "se_standard": {k: round(float(v), 4) for k, v in m_coll.bse.items()},
            "se_robust": {k: round(float(v), 4) for k, v in m_coll_rob.bse.items()},
            "R2": round(float(m_coll.rsquared), 4),
        },
        "vifBase": vif_base,
        "vifCollinear": vif_coll,
        "correlation": corr_dict,
        "seCompare": se_compare,
        "yhat": [round(float(v), 2) for v in yhat_base],
        "residuals": [round(float(v), 2) for v in resid_base],
    }


def load_democracy() -> dict:
    """Load democracy data and compute regression + influence diagnostics."""
    df = pd.read_stata(DATA_DIR / "AED_DEMOCRACY.DTA")

    # Bivariate model
    m_biv = ols("democracy ~ growth", data=df).fit(cov_type="HC1")

    # Multiple regression with controls
    m_mult = ols(
        "democracy ~ growth + constraint + indcent + catholic + muslim + protestant",
        data=df,
    ).fit(cov_type="HC1")

    # Standard SE version for comparison
    m_mult_std = ols(
        "democracy ~ growth + constraint + indcent + catholic + muslim + protestant",
        data=df,
    ).fit()

    # Influence diagnostics
    influence = OLSInfluence(m_mult_std)
    dfits_vals = influence.dffits[0]
    dfbetas_vals = influence.dfbetas
    n = len(df)
    k = len(m_mult.params)
    thresh_dfits = 2 * np.sqrt(k / n)
    thresh_dfbetas = 2 / np.sqrt(n)

    # Residuals and fitted values for diagnostic plots
    yhat = m_mult_std.fittedvalues.values
    uhat = m_mult_std.resid.values

    # Bivariate residuals
    yhat_biv = m_biv.fittedvalues.values
    uhat_biv = m_biv.resid.values

    # DFBETAS for growth coefficient (index 1)
    growth_idx = list(m_mult_std.params.index).index("growth")
    dfbetas_growth = dfbetas_vals[:, growth_idx]

    return {
        "n": n,
        "k": k,
        "countries": df["country"].tolist(),
        "democracy": [round(float(v), 4) for v in df["democracy"]],
        "growth": [round(float(v), 4) for v in df["growth"]],
        "bivariate": {
            "b0": round(float(m_biv.params["Intercept"]), 4),
            "b1": round(float(m_biv.params["growth"]), 4),
            "se": round(float(m_biv.bse["growth"]), 4),
            "R2": round(float(m_biv.rsquared), 4),
            "yhat": [round(float(v), 4) for v in yhat_biv],
            "resid": [round(float(v), 4) for v in uhat_biv],
        },
        "multiple": {
            "params": {k_: round(float(v), 6) for k_, v in m_mult.params.items()},
            "se": {k_: round(float(v), 6) for k_, v in m_mult.bse.items()},
            "R2": round(float(m_mult.rsquared), 4),
            "yhat": [round(float(v), 4) for v in yhat],
            "resid": [round(float(v), 4) for v in uhat],
        },
        "controlVars": ["constraint", "indcent", "catholic", "muslim", "protestant"],
        "controlData": {
            col: [round(float(v), 4) for v in df[col]]
            for col in ["constraint", "indcent", "catholic", "muslim", "protestant"]
        },
        "dfits": [round(float(v), 4) for v in dfits_vals],
        "dfbetasGrowth": [round(float(v), 4) for v in dfbetas_growth],
        "threshDfits": round(float(thresh_dfits), 4),
        "threshDfbetas": round(float(thresh_dfbetas), 4),
        "pctReduction": round(
            (float(m_biv.params["growth"]) - float(m_mult.params["growth"]))
            / float(m_biv.params["growth"])
            * 100,
            1,
        ),
    }


def build_data() -> dict:
    earnings = load_earnings()
    democracy = load_democracy()
    return {
        "earnings": earnings,
        "democracy": democracy,
        "meta": {
            "chapter": "Chapter 16: Checking the Model and Data",
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
    e = data["earnings"]
    d = data["democracy"]
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")
    print(f"[check] earnings: {e['n']} workers")
    print(
        f"[check] VIF collinear: age={e['vifCollinear']['age']}, "
        f"educ={e['vifCollinear']['education']}, "
        f"agebyeduc={e['vifCollinear']['agebyeduc']}"
    )
    print(
        f"[check] SE ratio (education): "
        f"{e['seCompare']['education']['ratio']:.4f}"
    )
    print(f"[check] democracy: {d['n']} countries")
    print(
        f"[check] growth coef: bivariate={d['bivariate']['b1']:.4f}, "
        f"multiple={d['multiple']['params']['growth']:.4f} "
        f"({d['pctReduction']}% reduction)"
    )
    print(
        f"[check] DFITS threshold: {d['threshDfits']:.4f}, "
        f"influential: {sum(1 for v in d['dfits'] if abs(v) > d['threshDfits'])}"
    )


if __name__ == "__main__":
    main()
