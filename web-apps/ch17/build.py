"""Build the Chapter 17 interactive dashboard.

Reads AED_NBA.DTA and AED_INTERESTRATES.DTA, pre-computes panel data
models (pooled OLS, FE), variance decomposition, cluster SEs, time series
regressions, ACF values, and ADL model, then injects JSON into template.html.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE = HERE / "template.html"
OUT_FILE = HERE / "dashboard.html"


def r(v, d=4):
    return round(float(v), d)


# ---------------------------------------------------------------------------
# NBA Panel Data
# ---------------------------------------------------------------------------

def load_nba() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_NBA.DTA")
    teams = sorted(df["teamid"].unique().tolist())
    seasons = sorted(df["season"].unique().tolist())

    # Raw data for scatter
    nba = {
        "lnrevenue": [r(v) for v in df["lnrevenue"]],
        "wins": [r(v, 1) for v in df["wins"]],
        "teamid": [int(v) for v in df["teamid"]],
        "team": df["team"].tolist(),
        "season": [int(v) for v in df["season"]],
        "n_teams": len(teams),
        "n_seasons": len(seasons),
        "n_obs": len(df),
    }

    # Variance decomposition
    overall_mean = float(df["lnrevenue"].mean())
    overall_std = float(df["lnrevenue"].std())
    between_std = float(df.groupby("teamid")["lnrevenue"].mean().std())
    within = df["lnrevenue"] - df.groupby("teamid")["lnrevenue"].transform("mean") + overall_mean
    within_std = float(within.std())

    # Same for wins
    wins_overall = float(df["wins"].std())
    wins_between = float(df.groupby("teamid")["wins"].mean().std())
    wins_within_vals = df["wins"] - df.groupby("teamid")["wins"].transform("mean") + df["wins"].mean()
    wins_within = float(wins_within_vals.std())

    nba["variance"] = {
        "lnrevenue": {"overall": r(overall_std), "between": r(between_std), "within": r(within_std)},
        "wins": {"overall": r(wins_overall, 2), "between": r(wins_between, 2), "within": r(wins_within, 2)},
    }

    # Pooled OLS with 3 SE types
    X = sm.add_constant(df[["wins"]])
    y = df["lnrevenue"]

    pooled_default = sm.OLS(y, X).fit()
    pooled_robust = sm.OLS(y, X).fit(cov_type="HC1")
    pooled_cluster = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": df["teamid"]})

    nba["pooled"] = {
        "coef": r(pooled_cluster.params["wins"], 6),
        "intercept": r(pooled_cluster.params["const"], 4),
        "r2": r(pooled_cluster.rsquared),
        "se_default": r(pooled_default.bse["wins"], 6),
        "se_robust": r(pooled_robust.bse["wins"], 6),
        "se_cluster": r(pooled_cluster.bse["wins"], 6),
        "t_default": r(pooled_default.tvalues["wins"]),
        "t_robust": r(pooled_robust.tvalues["wins"]),
        "t_cluster": r(pooled_cluster.tvalues["wins"]),
        "p_default": r(pooled_default.pvalues["wins"]),
        "p_robust": r(pooled_robust.pvalues["wins"]),
        "p_cluster": r(pooled_cluster.pvalues["wins"]),
    }

    # Fixed effects (within transformation)
    df["lnrev_dm"] = df["lnrevenue"] - df.groupby("teamid")["lnrevenue"].transform("mean")
    df["wins_dm"] = df["wins"] - df.groupby("teamid")["wins"].transform("mean")
    fe = sm.OLS(df["lnrev_dm"], df["wins_dm"]).fit(cov_type="cluster", cov_kwds={"groups": df["teamid"]})
    fe_default = sm.OLS(df["lnrev_dm"], df["wins_dm"]).fit()

    nba["fe"] = {
        "coef": r(fe.params.iloc[0], 6),
        "r2_within": r(fe.rsquared),
        "se_cluster": r(fe.bse.iloc[0], 6),
        "se_default": r(fe_default.bse.iloc[0], 6),
        "t_cluster": r(fe.tvalues.iloc[0]),
        "p_cluster": r(fe.pvalues.iloc[0]),
    }

    # De-meaned data for FE scatter
    nba["demeaned_lnrev"] = [r(v) for v in df["lnrev_dm"]]
    nba["demeaned_wins"] = [r(v, 1) for v in df["wins_dm"]]

    return nba


# ---------------------------------------------------------------------------
# Interest Rates Time Series
# ---------------------------------------------------------------------------

def load_interest_rates() -> dict:
    df = pd.read_stata(DATA_DIR / "AED_INTERESTRATES.DTA")

    # Time series data
    dates = [str(d.date()) if hasattr(d, "date") else str(d)[:10] for d in pd.to_datetime(df["date"])]
    gs10 = [r(v) for v in df["gs10"]]
    gs1 = [r(v) for v in df["gs1"]]
    dgs10 = [None if pd.isna(v) else r(v) for v in df["dgs10"]]
    dgs1 = [None if pd.isna(v) else r(v) for v in df["dgs1"]]

    ts = {
        "dates": dates,
        "gs10": gs10,
        "gs1": gs1,
        "dgs10": dgs10,
        "dgs1": dgs1,
        "n": len(df),
    }

    # Levels regression
    X_lev = sm.add_constant(df[["gs1"]])
    lev = sm.OLS(df["gs10"], X_lev).fit()
    lev_hac = sm.OLS(df["gs10"], X_lev).fit(cov_type="HAC", cov_kwds={"maxlags": 24})
    resid_acf_lev = acf(lev.resid, nlags=24)

    ts["levels"] = {
        "coef": r(lev.params["gs1"]),
        "intercept": r(lev.params["const"]),
        "r2": r(lev.rsquared),
        "se_default": r(lev.bse["gs1"]),
        "se_hac": r(lev_hac.bse["gs1"]),
        "se_ratio": r(lev_hac.bse["gs1"] / lev.bse["gs1"], 2),
        "acf": [r(v) for v in resid_acf_lev],
    }

    # Changes regression
    df_ch = df.dropna(subset=["dgs10", "dgs1"]).copy()
    X_ch = sm.add_constant(df_ch[["dgs1"]])
    chg = sm.OLS(df_ch["dgs10"], X_ch).fit()
    resid_acf_ch = acf(chg.resid, nlags=24)

    ts["changes"] = {
        "coef": r(chg.params["dgs1"]),
        "intercept": r(chg.params["const"]),
        "r2": r(chg.rsquared),
        "se_default": r(chg.bse["dgs1"]),
        "acf": [r(v) for v in resid_acf_ch],
    }

    # ADL(2,2) model
    df_ch["dgs10_L1"] = df_ch["dgs10"].shift(1)
    df_ch["dgs10_L2"] = df_ch["dgs10"].shift(2)
    df_ch["dgs1_L1"] = df_ch["dgs1"].shift(1)
    df_ch["dgs1_L2"] = df_ch["dgs1"].shift(2)
    df_adl = df_ch.dropna().copy()
    adl_vars = ["dgs10_L1", "dgs10_L2", "dgs1", "dgs1_L1", "dgs1_L2"]
    X_adl = sm.add_constant(df_adl[adl_vars])
    adl = sm.OLS(df_adl["dgs10"], X_adl).fit()
    resid_acf_adl = acf(adl.resid, nlags=24)

    ts["adl"] = {
        "coefs": {v: r(adl.params[v]) for v in adl_vars},
        "coef_const": r(adl.params["const"]),
        "se": {v: r(adl.bse[v]) for v in adl_vars},
        "pvals": {v: r(adl.pvalues[v]) for v in adl_vars},
        "r2": r(adl.rsquared),
        "acf": [r(v) for v in resid_acf_adl],
    }

    # Cumulative multipliers for ADL
    gamma = [adl.params["dgs1"], adl.params["dgs1_L1"], adl.params["dgs1_L2"]]
    cumulative = [r(sum(gamma[:i+1])) for i in range(len(gamma))]
    ts["adl"]["multipliers"] = {
        "impact": r(gamma[0]),
        "cumulative": cumulative,
    }

    return ts


# ---------------------------------------------------------------------------
# Assemble JSON payload
# ---------------------------------------------------------------------------

def build_data() -> dict:
    nba = load_nba()
    ts = load_interest_rates()
    return {
        "nba": nba,
        "ts": ts,
        "meta": {
            "chapter": "Chapter 17: Panel Data, Time Series Data, Causation",
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
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")

    nba = data["nba"]
    ts = data["ts"]
    print(f"[check] NBA: {nba['n_obs']} obs, {nba['n_teams']} teams, {nba['n_seasons']} seasons")
    print(f"[check] pooled wins coef = {nba['pooled']['coef']} (cluster SE = {nba['pooled']['se_cluster']})")
    print(f"[check] FE wins coef = {nba['fe']['coef']} (cluster SE = {nba['fe']['se_cluster']})")
    print(f"[check] SE ratio (cluster/default) = {nba['pooled']['se_cluster']/nba['pooled']['se_default']:.2f}x")
    print(f"[check] between SD = {nba['variance']['lnrevenue']['between']}, within SD = {nba['variance']['lnrevenue']['within']}")
    print(f"[check] levels R² = {ts['levels']['r2']} (residual ACF1 = {ts['levels']['acf'][1]})")
    print(f"[check] changes R² = {ts['changes']['r2']} (residual ACF1 = {ts['changes']['acf'][1]})")
    print(f"[check] HAC/default SE ratio = {ts['levels']['se_ratio']}x")
    print(f"[check] ADL(2,2) R² = {ts['adl']['r2']} (residual ACF1 = {ts['adl']['acf'][1]})")


if __name__ == "__main__":
    main()
