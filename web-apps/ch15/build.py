"""Build the Chapter 15 interactive dashboard.

Reads AED_EARNINGS_COMPLETE.DTA (872 workers), runs several regression
specifications with transformed variables, and injects pre-computed
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


def ols_result(y, X, var_names):
    m = sm.OLS(y, X).fit(cov_type="HC1")
    return {
        "vars": var_names,
        "coef": [round(float(c), 6) for c in m.params],
        "se": [round(float(s), 6) for s in m.bse],
        "t": [round(float(t), 4) for t in m.tvalues],
        "p": [round(float(p), 6) for p in m.pvalues],
        "r2": round(float(m.rsquared), 4),
        "n": int(m.nobs),
        "resid": [round(float(r), 2) for r in m.resid],
        "fitted": [round(float(f), 4) for f in m.fittedvalues],
    }


def build_data() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_EARNINGS_COMPLETE.DTA")
    y = df["earnings"].values.astype(float)
    lny = df["lnearnings"].values.astype(float)

    def cols(*names):
        return sm.add_constant(df[list(names)].astype(float))

    # --- scatter data ---
    scatter = {
        "education": [round(float(x), 1) for x in df["education"]],
        "earnings": [round(float(x), 2) for x in df["earnings"]],
        "lnearnings": [round(float(x), 4) for x in df["lnearnings"]],
        "age": [int(x) for x in df["age"]],
        "gender": [int(x) for x in df["gender"]],
    }

    # --- models ---
    # 1. Levels: earnings ~ education
    m_lev = ols_result(y, cols("education"), ["const", "education"])
    m_lev["name"] = "Levels"
    m_lev["dv"] = "earnings"

    # 2. Log-linear: lnearnings ~ education
    m_log = ols_result(lny, cols("education"), ["const", "education"])
    m_log["name"] = "Log-linear"
    m_log["dv"] = "lnearnings"

    # 3. Quadratic levels: earnings ~ age + agesq
    m_quad_age = ols_result(
        y, cols("age", "agesq"), ["const", "age", "agesq"]
    )
    m_quad_age["name"] = "Quadratic (age)"

    # 4. Linear age: earnings ~ age
    m_lin_age = ols_result(y, cols("age"), ["const", "age"])
    m_lin_age["name"] = "Linear (age)"

    # 5. Mincer: lnearnings ~ education + age + agesq
    m_mincer = ols_result(
        lny, cols("education", "age", "agesq"),
        ["const", "education", "age", "agesq"],
    )
    m_mincer["name"] = "Mincer"
    m_mincer["dv"] = "lnearnings"

    # 6. Full log: lnearnings ~ education + age + agesq + gender + lnhours
    m_full = ols_result(
        lny, cols("education", "age", "agesq", "gender", "lnhours"),
        ["const", "education", "age", "agesq", "gender", "lnhours"],
    )
    m_full["name"] = "Full log model"
    m_full["dv"] = "lnearnings"

    # 7. Levels interaction: earnings ~ education + age + education*age
    m_interact = ols_result(
        y, cols("education", "age", "agebyeduc"),
        ["const", "education", "age", "educ×age"],
    )
    m_interact["name"] = "Interaction (levels)"

    # --- standardized coefficients (full log model) ---
    full_vars = ["education", "age", "agesq", "gender", "lnhours"]
    stds_x = df[full_vars].astype(float).std()
    std_y = float(pd.Series(lny).std())
    full_coefs = m_full["coef"][1:]  # skip intercept
    standardized = []
    for name, coef, sx in zip(full_vars, full_coefs, stds_x):
        beta_star = coef * sx / std_y
        standardized.append({
            "var": name,
            "raw": round(coef, 6),
            "std": round(float(beta_star), 4),
        })

    # --- retransformation ---
    resid = m_full["resid"]
    fitted_ln = m_full["fitted"]
    resid_var = float(np.var(resid, ddof=1))
    smearing = float(np.exp(resid_var / 2))
    naive_preds = [round(float(np.exp(f)), 2) for f in fitted_ln]
    corrected_preds = [round(float(smearing * np.exp(f)), 2) for f in fitted_ln]
    retransformation = {
        "resid_var": round(resid_var, 6),
        "smearing_factor": round(smearing, 6),
        "naive_mean": round(float(np.mean(naive_preds)), 2),
        "corrected_mean": round(float(np.mean(corrected_preds)), 2),
        "actual_mean": round(float(y.mean()), 2),
        "naive_preds": naive_preds[:50],  # sample for histogram
        "corrected_preds": corrected_preds[:50],
    }

    # --- turning points ---
    tp_quad = round(-m_quad_age["coef"][1] / (2 * m_quad_age["coef"][2]), 1)
    tp_mincer = round(-m_mincer["coef"][2] / (2 * m_mincer["coef"][3]), 1)

    # Strip large arrays from models to save space (keep only for residual widget)
    levels_resid = m_lev["resid"]
    log_resid = m_log["resid"]
    for m in [m_lev, m_log, m_quad_age, m_lin_age, m_mincer, m_full, m_interact]:
        del m["resid"]
        del m["fitted"]

    return {
        "scatter": scatter,
        "models": {
            "levels_educ": m_lev,
            "log_educ": m_log,
            "quad_age": m_quad_age,
            "lin_age": m_lin_age,
            "mincer": m_mincer,
            "full_log": m_full,
            "interact": m_interact,
        },
        "turning_points": {"quad_age": tp_quad, "mincer": tp_mincer},
        "standardized": standardized,
        "retransformation": retransformation,
        "residuals": {
            "levels": levels_resid,
            "log": log_resid,
        },
        "mean_vals": {
            "education": round(float(df["education"].mean()), 2),
            "age": round(float(df["age"].mean()), 2),
            "earnings": round(float(y.mean()), 2),
        },
        "meta": {
            "chapter": "Chapter 15: Regression with Transformed Variables",
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
    ml = data["models"]["levels_educ"]
    mlog = data["models"]["log_educ"]
    tp = data["turning_points"]
    rt = data["retransformation"]
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")
    print(
        f"[check] Levels: educ=${ml['coef'][1]:,.2f}/yr, R²={ml['r2']:.4f}"
    )
    print(
        f"[check] Log-linear: educ={mlog['coef'][1]:.4f} "
        f"({mlog['coef'][1]*100:.2f}%/yr), R²={mlog['r2']:.4f}"
    )
    print(f"[check] Turning point (quad): {tp['quad_age']} yrs")
    print(
        f"[check] Retransformation: naive=${rt['naive_mean']:,.0f} "
        f"corrected=${rt['corrected_mean']:,.0f} "
        f"actual=${rt['actual_mean']:,.0f} "
        f"(smearing={rt['smearing_factor']:.4f})"
    )


if __name__ == "__main__":
    main()
