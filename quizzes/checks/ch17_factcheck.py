#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch17.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Reproduces the chapter's exact settings:
  - NBA panel (AED_NBA): pyfixest pooled OLS lnrevenue ~ wins with default, HC1, and CRV1(teamid)
    SEs; FE lnrevenue ~ wins | teamid with CRV1(teamid); between/within SDs as in the cheat sheet.
  - Earnings (AED_EARNINGS_COMPLETE): dbigearn = earnings > 60,000; statsmodels logit
    dbigearn ~ age + education (HC1); LPM with pyfixest (HC1).
  - Interest rates (AED_INTERESTRATES): time = 0..T-1 (chapter overrides the file's column);
    gs10 ~ gs1 + time, default and NW(24 lags) SEs; dgs10 ~ dgs1; residual ACFs with
    statsmodels acf; ADL(2,2) as in the Key Takeaways cheat sheet.
Run:  python3 quizzes/checks/ch17_factcheck.py      (exit 1 on any failure)
"""

import json
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf
from statsmodels.formula.api import logit
from statsmodels.tsa.stattools import acf

warnings.filterwarnings("ignore")

CHAPTER = "ch17"
ROOT = Path(__file__).resolve().parents[2]
GITHUB_DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"


def load(name: str) -> pd.DataFrame:
    """Local data/ copy first, GitHub fallback (same source the chapter streams from)."""
    local = ROOT / "data" / name
    src = local if local.exists() else GITHUB_DATA_URL + name
    return pd.read_stata(src) if name.lower().endswith(".dta") else pd.read_csv(src)


checks: dict[str, bool] = {}


def check(label: str, ok: bool) -> None:
    checks[label] = bool(ok)


def f(x: float, d: int) -> str:
    return f"{x:.{d}f}"


# ---------------------------------------------------------------- 1. FACTS
# --- NBA panel (Sections 17.2-17.4)
nba = load("AED_NBA.DTA")
for c in ["teamid", "season", "wins", "playoff"]:
    nba[c] = nba[c].astype(float)  # int8 in the file
nba["lnrevenue"] = nba["lnrevenue"].astype(float)
n_teams = nba["teamid"].nunique()
n_seasons = nba["season"].nunique()
N_nba = len(nba)
obs_per_team = nba.groupby("teamid").size()
season_labels = sorted(nba["teamandyear"].str.extract(r"(\d{4}-\d{2})$")[0].dropna().unique())

y = nba["lnrevenue"]
sd_overall = y.std()
sd_between = nba.groupby("teamid")["lnrevenue"].mean().std()
sd_within = (y - nba.groupby("teamid")["lnrevenue"].transform("mean")).std()
w = nba["wins"]
w_between = nba.groupby("teamid")["wins"].mean().std()
w_within = (w - nba.groupby("teamid")["wins"].transform("mean")).std()

pool = pf.feols("lnrevenue ~ wins", data=nba, vcov={"CRV1": "teamid"})
pool_def = pf.feols("lnrevenue ~ wins", data=nba)
pool_hc1 = pf.feols("lnrevenue ~ wins", data=nba, vcov="HC1")
fe = pf.feols("lnrevenue ~ wins | teamid", data=nba, vcov={"CRV1": "teamid"})
b_pool, b_fe = pool.coef()["wins"], fe.coef()["wins"]

print("FACTS NBA panel:")
print(f"  teams={n_teams} seasons={n_seasons} N={N_nba} obs/team counts={obs_per_team.value_counts().to_dict()}")
print(f"  seasons {season_labels[0]} .. {season_labels[-1]}")
print(f"  lnrevenue SD overall={sd_overall:.4f} between={sd_between:.4f} within={sd_within:.4f}")
print(f"  wins SD overall={w.std():.4f} between={w_between:.4f} within={w_within:.4f}")
print(f"  pooled b={b_pool:.6f} se_def={pool_def.se()['wins']:.6f} se_hc1={pool_hc1.se()['wins']:.6f} "
      f"se_crv={pool.se()['wins']:.6f} t_def={pool_def.tstat()['wins']:.4f} t_crv={pool.tstat()['wins']:.4f} "
      f"p_crv={pool.pvalue()['wins']:.4f} R2={pool._r2:.4f}")
print(f"  FE b={b_fe:.6f} se_crv={fe.se()['wins']:.6f} t={fe.tstat()['wins']:.4f} R2_within={fe._r2_within:.4f} R2(LSDV)={fe._r2:.4f}")
print(f"  drop pooled->FE = {(b_pool - b_fe) / b_pool:.4f}")

# --- Earnings logit (Section 17.4, Nonlinear Models)
e = load("AED_EARNINGS_COMPLETE.DTA")
e["age"] = e["age"].astype(float)
e["education"] = e["education"].astype(float)
e["dbigearn"] = (e["earnings"] > 60000).astype(int)
lg = logit("dbigearn ~ age + education", data=e).fit(cov_type="HC1", disp=0)
p_at_means = float(1 / (1 + np.exp(-(lg.params["Intercept"] + lg.params["age"] * e["age"].mean()
                                     + lg.params["education"] * e["education"].mean()))))
mem = lg.get_margeff(at="mean").margeff  # [age, education]
ame = lg.get_margeff().margeff           # chapter's printed get_margeff() = average ("overall")
pr_logit = lg.predict()
lpm = pf.feols("dbigearn ~ age + education", data=e, vcov="HC1")
pr_lpm = lpm.predict()
print("FACTS earnings logit:")
print(f"  N={len(e)} share high={e['dbigearn'].mean():.4f} min earnings={e['earnings'].min():.0f}")
print(f"  logit b_age={lg.params['age']:.4f} b_educ={lg.params['education']:.4f} pseudoR2={lg.prsquared:.4f} nobs={int(lg.nobs)}")
print(f"  p at means={p_at_means:.4f} ME educ at means={mem[1]:.4f} AME educ={ame[1]:.4f} LPM educ={lpm.coef()['education']:.4f}")
print(f"  logit pred range {pr_logit.min():.4f}..{pr_logit.max():.4f}; LPM pred range {pr_lpm.min():.4f}..{pr_lpm.max():.4f}")

# --- Interest rates (Sections 17.5-17.6)
r = load("AED_INTERESTRATES.DTA")
first_date, last_date = r["daten"].min(), r["daten"].max()
gaps = r["daten"].diff().dt.days.dropna()
r["time"] = np.arange(len(r)).astype(float)  # chapter: data_rates['time'] = np.arange(len(data_rates))
lev = pf.feols("gs10 ~ gs1 + time", data=r)
lev_hac = pf.feols("gs10 ~ gs1 + time", data=r, vcov="NW", vcov_kwargs={"time_id": "time", "lag": 24})
acf_lev = acf(pd.Series(lev._u_hat).dropna(), nlags=10)
chg = pf.feols("dgs10 ~ dgs1", data=r)
acf_chg = acf(pd.Series(chg._u_hat).dropna(), nlags=10)
for col, (src, k) in {"dgs10_lag1": ("dgs10", 1), "dgs10_lag2": ("dgs10", 2),
                      "dgs1_lag1": ("dgs1", 1), "dgs1_lag2": ("dgs1", 2)}.items():
    r[col] = r[src].shift(k)
adl = pf.feols("dgs10 ~ dgs10_lag1 + dgs10_lag2 + dgs1 + dgs1_lag1 + dgs1_lag2", data=r)
ca = adl.coef()
g0, g1, g2 = ca["dgs1"], ca["dgs1_lag1"], ca["dgs1_lag2"]
print("FACTS interest rates:")
print(f"  T={len(r)} {first_date.date()}..{last_date.date()} monthly gaps {gaps.min():.0f}-{gaps.max():.0f} days")
print(f"  gs10 {r['gs10'].iloc[0]} -> {r['gs10'].iloc[-1]}; gs1 {r['gs1'].iloc[0]} -> {r['gs1'].iloc[-1]}")
print(f"  levels b_gs1={lev.coef()['gs1']:.4f} se_def={lev.se()['gs1']:.4f} se_hac={lev_hac.se()['gs1']:.4f} "
      f"ratio={lev_hac.se()['gs1'] / lev.se()['gs1']:.3f} R2={lev._r2:.4f} t_def={lev.tstat()['gs1']:.3f} t_hac={lev_hac.tstat()['gs1']:.3f}")
print(f"  levels resid ACF: {np.round(acf_lev, 4).tolist()}")
print(f"  changes b_dgs1={chg.coef()['dgs1']:.4f} R2={chg._r2:.4f} N={chg._N}")
print(f"  changes resid ACF: {np.round(acf_chg, 4).tolist()}")
print(f"  ADL(2,2): {ca.round(4).to_dict()} R2={adl._r2:.4f} N={adl._N}")
print(f"  cum1={g0 + g1:.4f} cum2={g0 + g1 + g2:.4f}")

# ---------------------------------------------------------------- 2. CHECKS
# NBA panel structure (E01)
check("29 teams", n_teams == 29)
check("10 seasons", n_seasons == 10)
check("286 team-season observations", N_nba == 286)
check("up to 10 seasons per team (28 teams x 10 + 1 team x 6)",
      obs_per_team.max() == 10 and obs_per_team.value_counts().to_dict() == {10: 28, 6: 1})
check("seasons 2001-02 .. 2010-11", season_labels[0] == "2001-02" and season_labels[-1] == "2010-11")

# Decomposition (E02)
check("overall SD 0.24", f(sd_overall, 2) == "0.24")
check("between SD 0.21", f(sd_between, 2) == "0.21")
check("within SD 0.11", f(sd_within, 2) == "0.11")
check("0.21^2 + 0.11^2 close to 0.24^2 (0.0562 vs 0.0576)", abs((0.21**2 + 0.11**2) - 0.24**2) < 0.002)
check("within SD 0.11 in logs ~ 11% (approximation; exp(0.11)-1 = 11.6%)", abs(np.exp(0.11) - 1 - 0.11) < 0.01)
# wins decomposition (E03)
check("wins between SD 7.0", f(w_between, 1) == "7.0")
check("wins within SD 10.4", f(w_within, 1) == "10.4")

# Cluster-robust SEs (E04, E05, E06)
check("default SE 0.0011", f(pool_def.se()["wins"], 4) == "0.0011")
check("HC1 SE 0.0010", f(pool_hc1.se()["wins"], 4) == "0.0010")
check("cluster SE 0.0019", f(pool.se()["wins"], 4) == "0.0019")
check("default t 6.42", f(pool_def.tstat()["wins"], 2) == "6.42")
check("cluster t 3.54", f(pool.tstat()["wins"], 2) == "3.54")
check("cluster p 0.001", f(pool.pvalue()["wins"], 3) == "0.001")
check("cluster t not 'roughly half' of default (ratio 0.55)", 0.5 < pool.tstat()["wins"] / pool_def.tstat()["wins"] < 0.6)
check("29 clusters < 30 (KC 17.2 caution)", n_teams < 30)

# FE (E07, E08, E11)
check("pooled coef 0.0068", f(b_pool, 4) == "0.0068")
check("FE coef 0.0045", f(b_fe, 4) == "0.0045")
check("100 x 0.0045 = 0.45% (and 4.5% is 10x)", abs(100 * 0.0045 - 0.45) < 1e-12 and abs(1000 * 0.0045 - 4.5) < 1e-12)
check("0.0045 million dollars = $4,500", abs(0.0045 * 1e6 - 4500) < 1e-6)
check("drop pooled -> FE about 33%", f((b_pool - b_fe) / b_pool, 2) == "0.33")
check("FE within R2 0.185", f(fe._r2_within, 3) == "0.185")
check("pooled R2 0.127", f(pool._r2, 3) == "0.127")
check("FE estimate significant (t > 5)", fe.tstat()["wins"] > 5)

# Logit (E15, E16, E17)
check("872 workers", len(e) == 872 and int(lg.nobs) == 872)
check("logit educ coef 0.374", f(lg.params["education"], 3) == "0.374")
check("logit age coef 0.0385", f(lg.params["age"], 4) == "0.0385")
check("predicted p at means 0.23", f(p_at_means, 2) == "0.23")
check("ME at means 0.066 (from shown 0.23, 0.374)", f(0.23 * 0.77 * 0.374, 3) == "0.066")
check("ME at means 0.066 (exact)", f(mem[1], 3) == "0.066")
check("distractor p*b = 0.086", f(0.23 * 0.374, 3) == "0.086")
check("distractor p(1-p) = 0.177", f(0.23 * 0.77, 3) == "0.177")
check("LPM min prediction -0.59", f(pr_lpm.min(), 2) == "-0.59")
check("LPM max prediction 0.73", f(pr_lpm.max(), 2) == "0.73")
check("logit min prediction 0.001", f(pr_logit.min(), 3) == "0.001")
check("logit max prediction 0.86", f(pr_logit.max(), 2) == "0.86")

# Time series (E18, E20, E21, E23, E24)
check("levels R2 0.947", f(lev._r2, 3) == "0.947")
check("levels resid ACF lag1 0.95", f(acf_lev[1], 2) == "0.95")
check("levels resid ACF lag5 0.71", f(acf_lev[5], 2) == "0.71")
check("levels resid ACF lag10 0.42", f(acf_lev[10], 2) == "0.42")
check("gs1 coef 0.508", f(lev.coef()["gs1"], 3) == "0.508")
check("default SE 0.0221", f(lev.se()["gs1"], 4) == "0.0221")
check("HAC SE 0.0808", f(lev_hac.se()["gs1"], 4) == "0.0808")
check("HAC t about 6.3 (shown values)", f(0.508 / 0.0808, 1) == "6.3")
check("HAC t about 6.3 (exact)", f(lev_hac.tstat()["gs1"], 1) == "6.3")
check("default t about 23 (shown values)", round(0.508 / 0.0221) == 23)
check("inverted ratio about 0.16", f(0.0808 / 0.508, 2) == "0.16")
check("E21 distractor: coefficient itself about 0.51", f(0.508, 2) == "0.51" and f(lev.coef()["gs1"], 2) == "0.51")
check("changes slope 0.72", f(chg.coef()["dgs1"], 2) == "0.72")
check("changes R2 0.571", f(chg._r2, 3) == "0.571")
check("changes resid ACF lag1 0.25", f(acf_chg[1], 2) == "0.25")

# ADL (E25, E26)
check("gamma0 0.74", f(g0, 2) == "0.74")
check("gamma1 -0.26", f(g1, 2) == "-0.26")
check("gamma2 0.05", f(g2, 2) == "0.05")
check("two-month cumulative 0.53 (shown and exact)", f(0.74 - 0.26 + 0.05, 2) == "0.53" and f(g0 + g1 + g2, 2) == "0.53")
check("one-month cumulative 0.48 (shown and exact)", f(0.74 - 0.26, 2) == "0.48" and f(g0 + g1, 2) == "0.48")
check("abs-sum distractor 1.05", f(0.74 + 0.26 + 0.05, 2) == "1.05")
check("own lag-1 coefficient +0.28", f(ca["dgs10_lag1"], 2) == "0.28")

# Numbers quoted in feedback/explanations
check("E02 0.21^2 + 0.11^2 = 0.056 and 0.24^2 = 0.058", f(0.21**2 + 0.11**2, 3) == "0.056" and f(0.24**2, 3) == "0.058")
check("E02 between SD about twice the within SD", 1.8 < sd_between / sd_within < 2.1)
check("E04 cluster SE about 1.8x default", f(pool.se()["wins"] / pool_def.se()["wins"], 1) == "1.8")
check("E15 AME educ 0.062 (chapter's printed get_margeff)", f(ame[1], 3) == "0.062")
check("E15 LPM educ 0.054", f(lpm.coef()["education"], 3) == "0.054")
check("E15 percentage points 6.6 / 37.4 / 8.6 / 17.7 = 100 x options",
      [f(100 * v, 1) for v in (0.066, 0.374, 0.086, 0.177)] == ["6.6", "37.4", "8.6", "17.7"])
check("E18 both rates above 14% in Jan 1982 and below 2% in Jan 2015",
      min(r["gs10"].iloc[0], r["gs1"].iloc[0]) > 14 and max(r["gs10"].iloc[-1], r["gs1"].iloc[-1]) < 2)

# Hypothetical scenarios (practice + exam): arithmetic
check("P02 0.30^2 + 0.40^2 = 0.50^2", abs(0.30**2 + 0.40**2 - 0.50**2) < 1e-12)
check("P02 0.30 + 0.40 = 0.70", abs(0.30 + 0.40 - 0.70) < 1e-12)
check("P04 effective obs: 100 clusters, 300 obs, 100/3 about 33", 100 * 3 == 300 and round(100 / 3) == 33)
check("P04/P05 t = 3.33 and 1.11 from coefficient 0.50", f(0.5 / 0.15, 2) == "3.33" and f(0.5 / 0.45, 2) == "1.11")
check("P07 100 x 0.0020 = 0.20%", abs(100 * 0.0020 - 0.20) < 1e-12)
check("P15 ME = 0.4*0.6*0.5 = 0.12", f(0.4 * 0.6 * 0.5, 2) == "0.12")
check("P15 distractors 0.30, 0.24", f(0.6 * 0.5, 2) == "0.30" and f(0.4 * 0.6, 2) == "0.24")
check("P21 HAC t 2.0, default t 8.0, inverted 0.5, ratio 4.0",
      f(0.40 / 0.20, 1) == "2.0" and f(0.40 / 0.05, 1) == "8.0" and f(0.20 / 0.40, 1) == "0.5" and f(0.20 / 0.05, 1) == "4.0")
check("P25 cumulative 0.55, one-month 0.65, average 0.18",
      f(0.40 + 0.25 - 0.10, 2) == "0.55" and f(0.40 + 0.25, 2) == "0.65" and f((0.40 + 0.25 - 0.10) / 3, 2) == "0.18")
check("P28 IV 4.0, OLS 1.5, inverted 0.25, sum 2.5",
      f(2.0 / 0.5, 1) == "4.0" and f(1.5 / 1.0, 1) == "1.5" and f(0.5 / 2.0, 2) == "0.25" and f(2.0 + 0.5, 1) == "2.5")
check("E28 IV 0.4, OLS 0.5, inverted 2.5, product 0.9",
      f(0.6 / 1.5, 1) == "0.4" and f(1.0 / 2.0, 1) == "0.5" and f(1.5 / 0.6, 1) == "2.5" and f(0.6 * 1.5, 1) == "0.9")

# ---------------------------------------------------------------- 3. CLAIMS
check("CLAIM NBA is a panel: same teams observed in several seasons", obs_per_team.min() > 1)
check("CLAIM between SD of lnrevenue > within SD", sd_between > sd_within)
check("CLAIM wins vary more within teams than between teams", w_within > w_between)
check("CLAIM HC1 SE close to default (ratio 0.95-1.0): heteroskedasticity not the driver",
      0.95 < pool_hc1.se()["wins"] / pool_def.se()["wins"] < 1.0)
check("CLAIM cluster SE larger than default", pool.se()["wins"] > pool_def.se()["wins"])
check("CLAIM pooled wins significant at 5% with cluster SEs", pool.pvalue()["wins"] < 0.05)
check("CLAIM FE coefficient < pooled coefficient (both positive)", 0 < b_fe < b_pool)
check("CLAIM clustering does not change the coefficient", abs(pool.coef()["wins"] - pool_def.coef()["wins"]) < 1e-12)
check("CLAIM team-average wins and team-average lnrevenue positively correlated",
      nba.groupby("teamid")[["wins", "lnrevenue"]].mean().corr().iloc[0, 1] > 0)
check("CLAIM no negative earnings in sample", e["earnings"].min() > 0)
check("CLAIM logit uses all 872 workers (none dropped)", int(lg.nobs) == len(e))
check("CLAIM logit age and education coefficients positive", lg.params["age"] > 0 and lg.params["education"] > 0)
check("CLAIM LPM coefficients positive", lpm.coef()["age"] > 0 and lpm.coef()["education"] > 0)
check("CLAIM all logit predictions inside (0,1)", pr_logit.min() > 0 and pr_logit.max() < 1)
check("CLAIM some LPM predictions below 0", pr_lpm.min() < 0)
check("CLAIM interest data monthly, Jan 1982 - Jan 2015",
      str(first_date.date()) == "1982-01-01" and str(last_date.date()) == "2015-01-01" and gaps.min() >= 28 and gaps.max() <= 31)
check("CLAIM both rates trend down over the sample",
      r["gs10"].iloc[-1] < r["gs10"].iloc[0] - 10 and r["gs1"].iloc[-1] < r["gs1"].iloc[0] - 10)
check("CLAIM levels residual ACF decays slowly and stays positive through lag 10",
      all(acf_lev[k] > acf_lev[k + 1] > 0 for k in range(1, 10)))
check("CLAIM levels residual ACF lag 1 positive (no sign alternation)", acf_lev[1] > 0)
check("CLAIM differencing reduced but did not eliminate residual autocorrelation", 0.2 < acf_chg[1] < acf_lev[1])
check("CLAIM HAC SE > default SE", lev_hac.se()["gs1"] > lev.se()["gs1"])
check("CLAIM clustering/HAC leave the coefficient unchanged", abs(lev.coef()["gs1"] - lev_hac.coef()["gs1"]) < 1e-12)
check("CLAIM dgs10/dgs1 are first differences of gs10/gs1",
      np.allclose(r["dgs10"].iloc[1:], r["gs10"].diff().iloc[1:], atol=1e-4)
      and np.allclose(r["dgs1"].iloc[1:], r["gs1"].diff().iloc[1:], atol=1e-4))
check("CLAIM changes slope below 1", chg.coef()["dgs1"] < 1)
check("CLAIM ADL own lag-1 coefficient positive (momentum, not reversal)", ca["dgs10_lag1"] > 0)
check("CLAIM dgs10 itself positively autocorrelated at lag 1", acf(r["dgs10"].dropna(), nlags=1)[1] > 0)

# ---------------------------------------------------------------- report
bank = json.loads((ROOT / "quizzes" / "banks" / f"{CHAPTER}.json").read_text(encoding="utf-8"))
for label, ok in checks.items():
    print(("OK  " if ok else "FAIL"), label)
nums = set()
for s in ("practice", "exam"):
    for item in bank[s]:
        blob = json.dumps({k: v for k, v in item.items() if k != "id"}, ensure_ascii=False)
        nums.update(n.rstrip(".,") for n in re.findall(r"\d[\d,]*\.?\d*", blob))
print("\nNumbers quoted in the bank (each must trace to a check above or be self-evident):")
print(", ".join(sorted(nums, key=lambda x: float(x.replace(",", "") or 0))))
failed = [k for k, ok in checks.items() if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
sys.exit(1 if failed or not checks else 0)
