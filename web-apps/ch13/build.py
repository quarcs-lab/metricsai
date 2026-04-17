"""Build the Chapter 13 interactive dashboard.

Reads 6 datasets for the chapter's case studies (Cobb-Douglas, Phillips curve,
RAND insurance, DiD health access, RD incumbency, IV institutions),
pre-computes all regression results, and injects JSON into template.html.
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


def r(v, d=4):
    return round(float(v), d)


def load_cobbdouglas() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_COBBDOUGLAS.DTA")
    X = sm.add_constant(df[["lnk", "lnl"]])
    fit = sm.OLS(df["lnq"], X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    r_mat = np.array([[0, 1, 1]])
    q_vec = np.array([1])
    ftest = fit.f_test((r_mat, q_vec))
    pred_lnq = fit.fittedvalues
    pred_q = np.exp(pred_lnq) * np.exp(fit.resid.var() / 2)
    return {
        "year": [int(y) for y in df["year"]],
        "q": [r(v, 2) for v in df["q"]],
        "q_pred": [r(v, 2) for v in pred_q],
        "lnk": [r(v) for v in df["lnk"]],
        "lnl": [r(v) for v in df["lnl"]],
        "alpha": r(fit.params["lnk"]), "beta": r(fit.params["lnl"]),
        "intercept": r(fit.params["const"]),
        "sum_ab": r(fit.params["lnk"] + fit.params["lnl"]),
        "r2": r(fit.rsquared), "crs_p": r(float(ftest.pvalue)), "n": len(df),
    }


def load_phillips() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_PHILLIPS.DTA")
    pre = df[df["year"] < 1970].copy()
    post = df[df["year"] >= 1970].copy()
    X_pre = sm.add_constant(pre[["urate"]])
    fit_pre = sm.OLS(pre["inflgdp"], X_pre).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    X_post = sm.add_constant(post[["urate"]])
    fit_post = sm.OLS(post["inflgdp"], X_post).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    X_aug = sm.add_constant(post[["urate", "inflgdp1yr"]])
    fit_aug = sm.OLS(post["inflgdp"], X_aug).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    fit_aux = sm.OLS(post["inflgdp1yr"], sm.add_constant(post[["urate"]])).fit()
    gamma = fit_aux.params["urate"]
    return {
        "pre": {"urate": [r(v) for v in pre["urate"]], "inflgdp": [r(v) for v in pre["inflgdp"]],
                "coef": r(fit_pre.params["urate"]), "intercept": r(fit_pre.params["const"]),
                "r2": r(fit_pre.rsquared), "n": len(pre)},
        "post": {"urate": [r(v) for v in post["urate"]], "inflgdp": [r(v) for v in post["inflgdp"]],
                 "coef": r(fit_post.params["urate"]), "intercept": r(fit_post.params["const"]),
                 "r2": r(fit_post.rsquared), "n": len(post)},
        "augmented": {"coef_urate": r(fit_aug.params["urate"]), "coef_inflgdp1yr": r(fit_aug.params["inflgdp1yr"]),
                      "intercept": r(fit_aug.params["const"]), "r2": r(fit_aug.rsquared)},
        "ovb": {"gamma": r(gamma), "predicted_bias": r(fit_aug.params["inflgdp1yr"] * gamma),
                "actual_bivariate": r(fit_post.params["urate"])},
    }


def load_rand() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_HEALTHINSEXP.DTA")
    df1 = df[df["year"] == 1].copy()
    plans = ["coins0", "coins25", "coins50", "coins95", "coinsmixed", "coinsindiv"]
    labels = ["Free care", "25% cost-sharing", "50% cost-sharing", "95% cost-sharing", "Mixed deductible", "Individual deductible"]
    means = []
    for p, lbl in zip(plans, labels):
        sub = df1[df1[p] == 1]
        means.append({"plan": lbl, "key": p, "mean": r(sub["spending"].mean(), 2), "n": len(sub)})
    X = sm.add_constant(df1[["coins25", "coins50", "coins95", "coinsmixed", "coinsindiv"]])
    fit = sm.OLS(df1["spending"], X).fit(cov_type="cluster", cov_kwds={"groups": df1["idfamily"]})
    ftest = fit.f_test("coins25=coins50=coins95=coinsmixed=coinsindiv=0")
    return {"plans": means, "f_stat": r(float(ftest.fvalue), 2), "f_p": r(float(ftest.pvalue)),
            "r2": r(fit.rsquared), "n": len(df1)}


def load_did() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_HEALTHACCESS.DTA")
    groups = df.groupby(["hightreat", "post"])["waz"].mean()
    table = {"ctrl_pre": r(groups[(0, 0)]), "ctrl_post": r(groups[(0, 1)]),
             "treat_pre": r(groups[(1, 0)]), "treat_post": r(groups[(1, 1)])}
    table["ctrl_change"] = r(table["ctrl_post"] - table["ctrl_pre"])
    table["treat_change"] = r(table["treat_post"] - table["treat_pre"])
    table["did"] = r(table["treat_change"] - table["ctrl_change"])
    X = sm.add_constant(df[["hightreat", "post", "postXhigh"]])
    fit = sm.OLS(df["waz"], X).fit(cov_type="cluster", cov_kwds={"groups": df["idcommunity"]})
    ci = fit.conf_int().loc["postXhigh"]
    return {"table": table, "coef": r(fit.params["postXhigh"]), "se": r(fit.bse["postXhigh"]),
            "p": r(fit.pvalues["postXhigh"]), "ci_lo": r(float(ci.iloc[0])), "ci_hi": r(float(ci.iloc[1])), "n": len(df)}


def load_rd() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_INCUMBENCY.DTA")
    df = df.dropna(subset=["vote", "margin", "win"]).copy()
    X = sm.add_constant(df[["win", "margin"]])
    fit = sm.OLS(df["vote"], X).fit(cov_type="HC1")
    ci = fit.conf_int().loc["win"]
    df["margin_bin"] = pd.cut(df["margin"], bins=40)
    binned = df.groupby("margin_bin", observed=True).agg(
        margin_mid=("margin", "mean"), vote_mean=("vote", "mean"), n=("vote", "count")).reset_index(drop=True)
    binned = binned[binned["n"] >= 3]
    return {
        "margin": [r(v, 2) for v in df["margin"]], "vote": [r(v, 2) for v in df["vote"]],
        "win": [int(v) for v in df["win"]],
        "binned_margin": [r(v, 2) for v in binned["margin_mid"]],
        "binned_vote": [r(v, 2) for v in binned["vote_mean"]],
        "coef_win": r(fit.params["win"]), "coef_margin": r(fit.params["margin"]),
        "intercept": r(fit.params["const"]), "se_win": r(fit.bse["win"]),
        "p_win": r(fit.pvalues["win"], 6), "ci_lo": r(float(ci.iloc[0])), "ci_hi": r(float(ci.iloc[1])),
        "r2": r(fit.rsquared), "n": len(df),
    }


def load_iv() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_INSTITUTIONS.DTA")
    df = df.dropna(subset=["logpgp95", "avexpr", "logem4"]).copy()
    X_ols = sm.add_constant(df[["avexpr"]])
    ols = sm.OLS(df["logpgp95"], X_ols).fit(cov_type="HC1")
    X_fs = sm.add_constant(df[["logem4"]])
    fs = sm.OLS(df["avexpr"], X_fs).fit(cov_type="HC1")
    df["avexpr_hat"] = fs.fittedvalues
    X_iv = sm.add_constant(df[["avexpr_hat"]])
    iv = sm.OLS(df["logpgp95"], X_iv).fit()
    return {
        "logpgp95": [r(v) for v in df["logpgp95"]], "avexpr": [r(v) for v in df["avexpr"]],
        "logem4": [r(v) for v in df["logem4"]], "avexpr_hat": [r(v) for v in df["avexpr_hat"]],
        "ols": {"coef": r(ols.params["avexpr"]), "intercept": r(ols.params["const"]),
                "se": r(ols.bse["avexpr"]), "r2": r(ols.rsquared)},
        "first_stage": {"coef": r(fs.params["logem4"]), "intercept": r(fs.params["const"]),
                        "f_stat": r(float(fs.fvalue), 2), "r2": r(fs.rsquared)},
        "iv": {"coef": r(iv.params["avexpr_hat"]), "intercept": r(iv.params["const"])},
        "n": len(df),
    }


def build_data() -> dict:
    return {
        "cobbdouglas": load_cobbdouglas(), "phillips": load_phillips(),
        "rand": load_rand(), "did": load_did(), "rd": load_rd(), "iv": load_iv(),
        "meta": {"chapter": "Chapter 13: Case Studies for Multiple Regression",
                 "book": "metricsAI: An Introduction to Econometrics with Python and AI in the Cloud",
                 "author": "Carlos Mendez"},
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
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")
    cd, ph, rnd = data["cobbdouglas"], data["phillips"], data["rand"]
    did, rd, iv = data["did"], data["rd"], data["iv"]
    print(f"[check] Cobb-Douglas: alpha={cd['alpha']}, beta={cd['beta']}, sum={cd['sum_ab']}, CRS p={cd['crs_p']}")
    print(f"[check] Phillips pre: coef={ph['pre']['coef']}, post: coef={ph['post']['coef']}")
    print(f"[check] RAND F={rnd['f_stat']}, p={rnd['f_p']}, n={rnd['n']}")
    print(f"[check] DiD coef={did['coef']}, p={did['p']}, CI=[{did['ci_lo']},{did['ci_hi']}]")
    print(f"[check] RD win={rd['coef_win']}, CI=[{rd['ci_lo']},{rd['ci_hi']}], n={rd['n']}")
    print(f"[check] IV: OLS={iv['ols']['coef']}, IV={iv['iv']['coef']}, 1st F={iv['first_stage']['f_stat']}")


if __name__ == "__main__":
    main()
