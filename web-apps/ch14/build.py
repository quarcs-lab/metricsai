"""Build the Chapter 14 interactive dashboard.

Reads AED_EARNINGS_COMPLETE.DTA (872 full-time workers), runs five
progressive OLS models, and injects pre-computed results into
template.html.
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
    """Run OLS with HC1 robust SEs; return serializable dict."""
    m = sm.OLS(y, X).fit(cov_type="HC1")
    return {
        "vars": var_names,
        "coef": [round(float(c), 2) for c in m.params],
        "se": [round(float(s), 2) for s in m.bse],
        "t": [round(float(t), 4) for t in m.tvalues],
        "p": [round(float(p), 6) for p in m.pvalues],
        "r2": round(float(m.rsquared), 4),
        "r2_adj": round(float(m.rsquared_adj), 4),
        "n": int(m.nobs),
    }


def build_data() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_EARNINGS_COMPLETE.DTA")
    y = df["earnings"].values.astype(float)
    n = len(y)

    # --- raw data for scatter plots (education, earnings, gender) ---
    education = [round(float(x), 1) for x in df["education"]]
    earnings = [round(float(x), 2) for x in df["earnings"]]
    gender = [int(x) for x in df["gender"]]
    age = [int(x) for x in df["age"]]
    hours = [int(x) for x in df["hours"]]

    # worker type as string
    def wtype(row):
        if row["dself"] == 1:
            return "self"
        if row["dgovt"] == 1:
            return "govt"
        return "private"

    worker_type = [wtype(df.iloc[i]) for i in range(n)]

    # --- five progressive models ---
    def cols(*names):
        return sm.add_constant(df[list(names)].astype(float))

    models = [
        {
            "name": "Gender only",
            **ols_result(y, cols("gender"), ["const", "gender"]),
        },
        {
            "name": "Gender + Education",
            **ols_result(
                y, cols("gender", "education"), ["const", "gender", "education"]
            ),
        },
        {
            "name": "Gender + Educ + Interaction",
            **ols_result(
                y,
                cols("gender", "education", "genderbyeduc"),
                ["const", "gender", "education", "gender×educ"],
            ),
        },
        {
            "name": "Full controls",
            **ols_result(
                y,
                cols("gender", "education", "genderbyeduc", "age", "hours"),
                ["const", "gender", "education", "gender×educ", "age", "hours"],
            ),
        },
        {
            "name": "Full interactions",
            **ols_result(
                y,
                cols(
                    "gender",
                    "education",
                    "genderbyeduc",
                    "age",
                    "genderbyage",
                    "hours",
                    "genderbyhours",
                ),
                [
                    "const",
                    "gender",
                    "education",
                    "gender×educ",
                    "age",
                    "gender×age",
                    "hours",
                    "gender×hours",
                ],
            ),
        },
    ]

    # --- worker type models (3 base categories) ---
    worker_models = {}
    for base_name, drop_col in [
        ("private", "dprivate"),
        ("self", "dself"),
        ("govt", "dgovt"),
    ]:
        include = [c for c in ["dself", "dprivate", "dgovt"] if c != drop_col]
        var_names = ["const"] + include
        X = sm.add_constant(df[include].astype(float))
        worker_models[base_name] = ols_result(y, X, var_names)

    # --- group means ---
    def group_stats(mask):
        vals = y[mask]
        m = float(vals.mean())
        s = float(vals.std(ddof=1))
        se = s / np.sqrt(len(vals))
        return {"n": int(len(vals)), "mean": round(m, 2), "sd": round(s, 2), "se": round(se, 2)}

    group_means = {
        "male": group_stats(df["gender"].values == 0),
        "female": group_stats(df["gender"].values == 1),
        "self_employed": group_stats(df["dself"].values == 1),
        "private": group_stats(df["dprivate"].values == 1),
        "government": group_stats(df["dgovt"].values == 1),
    }

    # --- separate gender regressions (earnings ~ education) ---
    gender_reg = {}
    for g, label in [(0, "male"), (1, "female")]:
        mask = df["gender"].values == g
        Xg = sm.add_constant(df.loc[mask, "education"].astype(float))
        mg = sm.OLS(y[mask], Xg).fit(cov_type="HC1")
        gender_reg[label] = {
            "intercept": round(float(mg.params.iloc[0]), 2),
            "slope": round(float(mg.params.iloc[1]), 2),
            "r2": round(float(mg.rsquared), 4),
            "n": int(mg.nobs),
        }

    # --- mean values for prediction (needed by JS) ---
    mean_vals = {
        "education": round(float(df["education"].mean()), 2),
        "age": round(float(df["age"].mean()), 2),
        "hours": round(float(df["hours"].mean()), 2),
    }

    return {
        "scatter": {
            "education": education,
            "earnings": earnings,
            "gender": gender,
        },
        "models": models,
        "worker_models": worker_models,
        "group_means": group_means,
        "gender_reg": gender_reg,
        "mean_vals": mean_vals,
        "meta": {
            "chapter": "Chapter 14: Regression with Indicator Variables",
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
    gm = data["group_means"]
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")
    print(
        f"[check] Model 1: gender coef = ${m1['coef'][1]:,.2f} "
        f"(t = {m1['t'][1]:.4f}), R² = {m1['r2']:.4f}"
    )
    print(
        f"[check] Male mean = ${gm['male']['mean']:,.2f}, "
        f"Female mean = ${gm['female']['mean']:,.2f}, "
        f"Gap = ${gm['female']['mean'] - gm['male']['mean']:,.2f}"
    )
    print(
        f"[check] Worker types: Self=${gm['self_employed']['mean']:,.2f} "
        f"Private=${gm['private']['mean']:,.2f} "
        f"Govt=${gm['government']['mean']:,.2f}"
    )


if __name__ == "__main__":
    main()
