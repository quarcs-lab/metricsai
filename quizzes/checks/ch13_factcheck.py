#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch13.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Reproduces the chapter's nine case-study estimations exactly (same samples, same vcov).
Run:  python3 quizzes/checks/ch13_factcheck.py      (exit 1 on any failure)
"""

import json
import math
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf
from scipy import stats

warnings.filterwarnings("ignore")

CHAPTER = "ch13"
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


def f1(x: float) -> str:
    return f"{x:.1f}"


def f2(x: float) -> str:
    return f"{x:.2f}"


def f3(x: float) -> str:
    return f"{x:.3f}"


# ---------------------------------------------------------------- 1. FACTS
# 13.1 API (int8/int16 columns cast to float)
api = load("AED_API99.DTA")
for c in ["api99", "meals", "englearn", "yearround", "credteach", "emerteach"]:
    api[c] = api[c].astype(float)
corr = api[["api99", "edparent", "meals", "englearn", "yearround", "credteach", "emerteach"]].corr()
api_biv = pf.feols("api99 ~ edparent", data=api, vcov="HC1")
api_mult = pf.feols("api99 ~ edparent + meals + englearn + yearround + credteach + emerteach", data=api, vcov="HC1")
api_meals = pf.feols("api99 ~ meals", data=api)
api_me = pf.feols("api99 ~ meals + edparent", data=api, vcov="HC1")
b_biv, b_ed = api_biv.coef()["edparent"], api_mult.coef()["edparent"]
print(f"FACTS API: n={len(api)} biv slope={b_biv:.4f} R2={api_biv._r2:.4f}; mult edparent={b_ed:.4f} meals={api_mult.coef()['meals']:.4f} "
      f"(p={api_mult.pvalue()['meals']:.4f}) R2={api_mult._r2:.4f}; r(api,meals)={corr.loc['api99','meals']:.4f} "
      f"r(meals,edparent)={corr.loc['meals','edparent']:.4f} r(cred,emer)={corr.loc['credteach','emerteach']:.4f}")

# 13.2 Cobb-Douglas (int16 -> float before logs), Newey-West lag 3
cb = load("AED_COBBDOUGLAS.DTA")
for c in "qkl":
    cb["ln" + c] = np.log(cb[c].astype(float))
cb["_time"] = range(len(cb))
cd = pf.feols("lnq ~ lnk + lnl", data=cb, vcov="NW", vcov_kwargs={"time_id": "_time", "lag": 3})
bk, bl, b0 = cd.coef()["lnk"], cd.coef()["lnl"], cd.coef()["Intercept"]
R = np.array([0.0, 1.0, 1.0])
F_crs = (R @ cd.coef().values - 1.0) ** 2 / (R @ cd._vcov @ R)
p_crs = 1 - stats.f.cdf(F_crs, 1, cd._N - 3)
s_cd = np.sqrt(np.sum(cd._u_hat ** 2) / (cd._N - 3))
print(f"FACTS Cobb-Douglas: years {int(cb.year.min())}-{int(cb.year.max())} n={len(cb)} b0={b0:.4f} bk={bk:.4f} bl={bl:.4f} sum={bk + bl:.4f} "
      f"F={F_crs:.4f} p={p_crs:.4f} R2={cd._r2:.4f} s={s_cd:.4f} factor={np.exp(s_cd ** 2 / 2):.4f}")

# 13.3 Phillips curve, Newey-West lags 3 (pre) and 5 (post)
ph = load("AED_PHILLIPS.DTA")
pre = ph[ph["year"] < 1970].copy()
pre["_time"] = range(len(pre))
post = ph[ph["year"] >= 1970].copy()
post["_time"] = range(len(post))
pc_pre = pf.feols("inflgdp ~ urate", data=pre, vcov="NW", vcov_kwargs={"time_id": "_time", "lag": 3})
pc_post = pf.feols("inflgdp ~ urate", data=post, vcov="NW", vcov_kwargs={"time_id": "_time", "lag": 5})
pe = post.dropna(subset=["inflgdp1yr"]).copy()
pe["_time"] = range(len(pe))
pc_aug = pf.feols("inflgdp ~ urate + inflgdp1yr", data=pe, vcov="NW", vcov_kwargs={"time_id": "_time", "lag": 5})
aux = pf.feols("inflgdp1yr ~ urate", data=pe)
gam, beta2, beta3 = aux.coef()["urate"], pc_aug.coef()["urate"], pc_aug.coef()["inflgdp1yr"]
print(f"FACTS Phillips: pre n={len(pre)} {int(pre.year.min())}-{int(pre.year.max())} slope={pc_pre.coef()['urate']:.4f} p={pc_pre.pvalue()['urate']:.4f}; "
      f"post n={len(post)} {int(post.year.min())}-{int(post.year.max())} slope={pc_post.coef()['urate']:.4f} p={pc_post.pvalue()['urate']:.4f}; "
      f"aug n={len(pe)} urate={beta2:.4f} (p={pc_aug.pvalue()['urate']:.4f}) exp={beta3:.4f} (p={pc_aug.pvalue()['inflgdp1yr']:.5f}); gamma={gam:.4f} "
      f"OVB={beta2 + beta3 * gam:.4f}")

# 13.4 Autos, clustered by manufacturer
au = load("AED_AUTOSMPG.DTA")
fe_kw = dict(data=au)
auto = pf.feols("lmpg ~ lhp + lcurbwt + ltorque + year", vcov={"CRV1": "mfr"}, **fe_kw)
auto_iid = pf.feols("lmpg ~ lhp + lcurbwt + ltorque + year", vcov="iid", **fe_kw)
ym = au.assign(curbwt=au["curbwt"].astype(float), hp=au["hp"].astype(float)).groupby("year")[["mpg", "curbwt", "hp"]].mean()
print(f"FACTS autos: n={len(au)} years {int(au.year.min())}-{int(au.year.max())} ({au.year.nunique()}) mfr={au.mfr.nunique()} "
      f"avg/cluster={len(au) / au.mfr.nunique():.1f}; weight={auto.coef()['lcurbwt']:.4f} hp={auto.coef()['lhp']:.4f} "
      f"torque={auto.coef()['ltorque']:.4f} year={auto.coef()['year']:.5f} R2={auto._r2:.4f}; se weight clustered={auto.se()['lcurbwt']:.5f} "
      f"iid={auto_iid.se()['lcurbwt']:.5f}")

# 13.5 RAND, year 1, clustered by family
hie = load("AED_HEALTHINSEXP.DTA")
y1 = hie[hie["year"] == 1]
rct = pf.feols("spending ~ coins25 + coins50 + coins95 + coinsmixed + coinsindiv", data=y1, vcov={"CRV1": "idfamily"})
cn = ["coins25", "coins50", "coins95", "coinsmixed", "coinsindiv"]
bb = np.array([rct.coef()[c] for c in cn])
ix = [list(rct.coef().index).index(c) for c in cn]
F_rct = float(bb @ np.linalg.inv(rct._vcov[np.ix_(ix, ix)]) @ bb / 5)
p_rct = 1 - stats.f.cdf(F_rct, 5, rct._N - 6)
plan_mean = y1.groupby("plan", observed=True)["spending"].mean()
plan_age = y1.groupby("plan", observed=True)["age"].mean()
print(f"FACTS RAND: y1 n={len(y1)} intercept={rct.coef()['Intercept']:.2f} c25={rct.coef()['coins25']:.2f} (p={rct.pvalue()['coins25']:.4f}) "
      f"c50={rct.coef()['coins50']:.2f} (p={rct.pvalue()['coins50']:.4f}) c95={rct.coef()['coins95']:.2f} (p={rct.pvalue()['coins95']:.5f}) "
      f"F={F_rct:.3f} p={p_rct:.2e} R2={rct._r2:.4f}; mean age free={plan_age['Free Care']:.2f} 95%={plan_age['95%/100% Coins']:.2f}")

# 13.6 DiD, clustered by community
acc = load("AED_HEALTHACCESS.DTA")
g = acc.groupby(["hightreat", "post"])["waz"].mean()
did = pf.feols("waz ~ hightreat + post + postXhigh", data=acc, vcov={"CRV1": "idcommunity"})
did_manual = (g[(1, 1)] - g[(1, 0)]) - (g[(0, 1)] - g[(0, 0)])
print(f"FACTS DiD: n={len(acc)} communities={acc.idcommunity.nunique()} means C0={g[(0, 0)]:.4f} C1={g[(0, 1)]:.4f} T0={g[(1, 0)]:.4f} T1={g[(1, 1)]:.4f} "
      f"DiD={did_manual:.4f} coef={did.coef()['postXhigh']:.4f} p={did.pvalue()['postXhigh']:.4f} hightreat={did.coef()['hightreat']:.4f} "
      f"(p={did.pvalue()['hightreat']:.4f})")

# 13.7 RD
inc = load("AED_INCUMBENCY.DTA")
rd = inc[inc["vote"].notna()].copy()
rdm = pf.feols("vote ~ win + margin", data=rd, vcov="HC1")
ci = rdm.confint().loc["win"].values
naive = rd.loc[rd["win"] == 1, "vote"].mean() - rd.loc[rd["win"] == 0, "vote"].mean()
print(f"FACTS RD: n_all={len(inc)} n={len(rd)} years {int(inc.year.min())}-{int(inc.year.max())} win={rdm.coef()['win']:.4f} "
      f"CI=[{ci[0]:.3f}, {ci[1]:.3f}] p={rdm.pvalue()['win']:.2e} margin={rdm.coef()['margin']:.4f} naive={naive:.4f}")

# 13.8 IV
ins = load("AED_INSTITUTIONS.DTA")
ols = pf.feols("logpgp95 ~ avexpr", data=ins, vcov="HC1")
fst = pf.feols("avexpr ~ logem4", data=ins, vcov="HC1")
iv = pf.feols("logpgp95 ~ 1 | avexpr ~ logem4", data=ins, vcov="HC1")
b_ols, b_iv = ols.coef()["avexpr"], iv.coef()["avexpr"]
F1 = fst.tstat()["logem4"] ** 2
print(f"FACTS IV: n={len(ins)} OLS={b_ols:.4f} first={fst.coef()['logem4']:.4f} F={F1:.3f} IV={b_iv:.4f} (a={iv.coef()['Intercept']:.4f}) "
      f"ratio={b_iv / b_ols:.4f} exp(IV)={math.exp(b_iv):.4f}")
print()

# ---------------------------------------------------------------- 2. CHECKS (exam)
# E01-E04: API
check("E01/E02: 807 schools; multiple-regression edparent = 73.9", len(api) == 807 and f1(b_ed) == "73.9")
check("E02: bivariate slope 79.5", f1(b_biv) == "79.5")
check("E02: 1.5 x 73.9 = 110.85 ~ 111 (exact 110.9); distractors 1.5 x 79.5 = 119, 73.9 / 1.5 = 49, 74",
      round(1.5 * 73.9) == 111 and round(1.5 * b_ed) == 111 and round(1.5 * 79.5) == 119 and round(73.9 / 1.5) == 49 and round(73.9) == 74)
check("E03: r(api99, meals) = -0.54", f2(corr.loc["api99", "meals"]) == "-0.54")
check("E03: meals coefficient +0.08, p = 0.39", f2(api_mult.coef()["meals"]) == "0.08" and f2(api_mult.pvalue()["meals"]) == "0.39")
check("E03: r(meals, edparent) = -0.60", f2(corr.loc["meals", "edparent"]) == "-0.60")
check("E04: r(credteach, emerteach) = -0.82", f2(corr.loc["credteach", "emerteach"]) == "-0.82")
# E05-E09: Cobb-Douglas
check("E06: ln Q = -0.18 + 0.23 ln K + 0.81 ln L; 1899-1922", (f2(b0), f2(bk), f2(bl)) == ("-0.18", "0.23", "0.81")
      and (int(cb.year.min()), int(cb.year.max()), len(cb)) == (1899, 1922, 24))
check("E06: 10% labor -> 8.1% (exact 0.807 x 10 = 8.1); distractors 0.81, 10.4 (sum x 10), 2.3 (capital)",
      f1(0.81 * 10) == "8.1" and f1(bl * 10) == "8.1" and f1((0.23 + 0.81) * 10) == "10.4" and f1(10 * (bk + bl)) == "10.4" and f1(0.23 * 10) == "2.3")
check("E07: sum = 1.040, HAC test p = 0.636", f3(bk + bl) == "1.040" and f3(p_crs) == "0.636")
check("E05: 24 consecutive years", len(cb) == 24 and (cb["year"].diff().dropna() == 1).all())
check("E09 explanation: s ~ 0.058, factor ~ 1.002", f3(s_cd) == "0.058" and f3(math.exp(s_cd ** 2 / 2)) == "1.002")
# E10-E13: Phillips
check("E10: 1949-1969 slope -1.03 (21 years)", f2(pc_pre.coef()["urate"]) == "-1.03" and (int(pre.year.min()), int(pre.year.max()), len(pre)) == (1949, 1969, 21))
check("E10 D distractor: mean inflation 1949-1969 is not -1.03", abs(pre["inflgdp"].mean() + 1.03) > 1)
check("E11: 1970-2014 slope positive, p = 0.42", pc_post.coef()["urate"] > 0 and f2(pc_post.pvalue()["urate"]) == "0.42"
      and (int(post.year.min()), int(post.year.max())) == (1970, 2014))
check("E12/E13: beta2 = -0.13, beta3 = 1.15, gamma = 0.34", (f2(beta2), f2(beta3), f2(gam)) == ("-0.13", "1.15", "0.34"))
check("E12: -0.13 + 1.15 x 0.34 = 0.261 ~ +0.26; distractors 0.39 (bias only), -0.13 (no bias), 1.02 (beta2 + beta3)",
      (f2(-0.13 + 1.15 * 0.34), f2(1.15 * 0.34), f2(-0.13 + 1.15)) == ("0.26", "0.39", "1.02"))
check("CLAIM E12 explanation: OVB prediction matches the chapter's bivariate post-1970 slope exactly (0.27; same 45-year sample)",
      f2(beta2 + beta3 * gam) == "0.27" and abs(beta2 + beta3 * gam - pc_post.coef()["urate"]) < 1e-10 and len(pe) == len(post) == 45)
check("E13: augmented urate p = 0.12 (> 0.05)", f2(pc_aug.pvalue()["urate"]) == "0.12")
# E14-E17: autos
check("E14: 26,995 vehicles, model years 1980-2006", len(au) == 26995 and (int(au.year.min()), int(au.year.max())) == (1980, 2006))
check("E14: weight elasticity -0.56; 10% -> 5.6% (exact 5.6)", f2(auto.coef()["lcurbwt"]) == "-0.56" and f1(10 * auto.coef()["lcurbwt"]) == "-5.6")
check("E15: year coefficient 0.0152 -> 1.5% per year", f"{auto.coef()['year']:.4f}" == "0.0152" and f1(100 * auto.coef()["year"]) == "1.5")
check("E16: 39 manufacturers, ~690 vehicles each", au.mfr.nunique() == 39 and round(len(au) / 39, -1) == 690)
check("E16 explanation: clustered SE of weight elasticity ~ 9 x default", round(auto.se()["lcurbwt"] / auto_iid.se()["lcurbwt"]) == 9)
# E19-E21: RAND
check("E19: 5,639 first-year observations", len(y1) == 5639)
check("E19: intercept $2,154 (free-care mean); 95% coefficient -$1,108",
      round(rct.coef()["Intercept"]) == 2154 and round(plan_mean["Free Care"]) == 2154 and round(rct.coef()["coins95"]) == -1108)
check("E19: 2,154 - 1,108 = 1,046 = 95% plan mean; distractors 3,262",
      2154 - 1108 == 1046 and round(plan_mean["95%/100% Coins"]) == 1046 and 2154 + 1108 == 3262)
check("E21: 25% -757 (p<0.001), 50% -368 (p=0.55), 95% p<0.001",
      round(rct.coef()["coins25"]) == -757 and rct.pvalue()["coins25"] < 0.001 and round(rct.coef()["coins50"]) == -368
      and f2(rct.pvalue()["coins50"]) == "0.55" and rct.pvalue()["coins95"] < 0.001)
check("E21: joint F = 11.39, p < 0.001", f2(F_rct) == "11.39" and p_rct < 0.001)
check("E21 D: 757 / 2,154 = 35% (not 25%)", round(100 * 757 / 2154) == 35)
# E22-E25: DiD
check("E22: means -0.414, -0.069 (low), -0.545, 0.321 (high)",
      (f3(g[(0, 0)]), f3(g[(0, 1)]), f3(g[(1, 0)]), f3(g[(1, 1)])) == ("-0.414", "-0.069", "-0.545", "0.321"))
check("E22: DiD 0.866 - 0.345 = 0.52 (exact 0.52; regression coefficient identical)",
      (f3(0.321 + 0.545), f3(-0.069 + 0.414), f2(0.866 - 0.345)) == ("0.866", "0.345", "0.52")
      and f2(did_manual) == "0.52" and abs(did.coef()["postXhigh"] - did_manual) < 1e-10)
check("E22 distractors: 0.87 (treated change), 0.39 (1998 gap), 1.21 (sum of changes)",
      (f2(0.866), f2(0.321 + 0.069), f2(0.866 + 0.345)) == ("0.87", "0.39", "1.21"))
check("E24 explanation: hightreat = -0.13 (p = 0.51)", f2(did.coef()["hightreat"]) == "-0.13" and f2(did.pvalue()["hightreat"]) == "0.51")
check("E25: 1,071 children in 54 communities", len(acc) == 1071 and acc.idcommunity.nunique() == 54)
# E26-E28: RD
check("E26: 1,297 elections with outcome, 1914-2010; win = 4.8; CI 3.1 to 6.5",
      len(rd) == 1297 and (int(inc.year.min()), int(inc.year.max())) == (1914, 2010) and f1(rdm.coef()["win"]) == "4.8"
      and (f1(ci[0]), f1(ci[1])) == ("3.1", "6.5"))
check("E27: naive winner-loser gap = 21.7 points", f1(naive) == "21.7")
# E29-E32: IV
check("E29: 64 colonies; 2SLS = 1.91 + 0.944 x avexpr", len(ins) == 64 and (f2(iv.coef()["Intercept"]), f3(b_iv)) == ("1.91", "0.944"))
check("E29: e^0.944 = 2.57 -> 157%; distractors 94%, 257%, 1 - e^-0.944 = 61%",
      f2(math.exp(0.944)) == "2.57" and round(100 * (math.exp(0.944) - 1)) == 157 and round(100 * (math.exp(b_iv) - 1)) == 157
      and round(100 * 0.944) == 94 and round(100 * math.exp(0.944)) == 257 and round(100 * (1 - math.exp(-0.944))) == 61)
check("E31: first-stage F = 16.3 (> 10)", f1(F1) == "16.3" and F1 > 10)
check("E31 C / explanation: first-stage R2 = 0.27 (settler mortality explains ~27%, not most, of institutions' variation)",
      f2(pf.feols("avexpr ~ logem4", data=ins)._r2) == "0.27" and pf.feols("avexpr ~ logem4", data=ins)._r2 < 0.5)
check("E13: bivariate post-1970 slope positive; augmented urate coefficient -0.13 (sign turns negative)",
      pc_post.coef()["urate"] > 0 and f2(beta2) == "-0.13")
check("E25 C: DiD coefficient significant at 5%", did.pvalue()["postXhigh"] < 0.05)
check("E32: IV about 80% larger than OLS (0.52 vs 0.94)", round(100 * (b_iv / b_ols - 1), -1) == 80 and (f2(b_ols), f2(b_iv)) == ("0.52", "0.94"))
# E34
check("E34: 1990-2019 quarterly = 120 quarters", (2019 - 1990 + 1) * 4 == 120)

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic)
check("P02: 5 x 1.6 = 8; 5 x 2.4 = 12; 1.6 / 5 = 0.32", (5 * 1.6, 5 * 2.4, f2(1.6 / 5)) == (8.0, 12.0, "0.32"))
check("P06: 10% capital x 0.35 = 3.5; 0.35; 9.5 (sum x 10); 6.0 (labor)", (f1(0.35 * 10), f1(0.95 * 10), f1(0.60 * 10)) == ("3.5", "9.5", "6.0"))
check("P08: 2^0.9 = 1.87 < 2", f2(2 ** 0.9) == "1.87")
check("P09: e^(0.25/2) = 1.13; e^0.5 = 1.65; e^0.25 = 1.28; e^0.0625 = 1.06",
      (f2(math.exp(0.125)), f2(math.exp(0.5)), f2(math.exp(0.25)), f2(math.exp(0.0625))) == ("1.13", "1.65", "1.28", "1.06"))
check("P12/P13: 0.08 + 0.05 x 0.60 = 0.11; bias 0.03; 0.05; 0.13",
      (f2(0.08 + 0.05 * 0.60), f2(0.05 * 0.60), f2(0.08 - 0.05 * 0.60), f2(0.08 + 0.05)) == ("0.11", "0.03", "0.05", "0.13"))
check("P14: 0.70 x 20 = 14%; 0.14", (f1(0.70 * 20), f2(0.70 * 20 / 100)) == ("14.0", "0.14"))
check("P19: 18,400 + 1,250 = 19,650; 18,400 - 1,250 = 17,150", (18400 + 1250, 18400 - 1250) == (19650, 17150))
check("P20 explanation: RAND R2 ~ 0.007", f3(rct._r2) == "0.007")
check("P21: 40 / 200 = 20%; 200 + 40 = 240", 40 / 200 == 0.20 and 200 + 40 == 240)
check("P22: (58-50) - (51-47) = 4; 8; 7; 12", ((58 - 50) - (51 - 47), 58 - 50, 58 - 51, (58 - 50) + (51 - 47)) == (4, 8, 7, 12))
check("P29: e^0.40 = 1.49 -> 49%; 149; 1 - e^-0.40 = 33%",
      round(100 * (math.exp(0.4) - 1)) == 49 and round(100 * math.exp(0.4)) == 149 and round(100 * (1 - math.exp(-0.4))) == 33)
check("P33: inner join of ids {1,2,3} and {1,2,4} keeps 2 rows",
      len(pd.merge(pd.DataFrame({"id": [1, 2, 3]}), pd.DataFrame({"id": [1, 2, 4]}), on="id", how="inner")) == 2)

# ---------------------------------------------------------------- 3. CLAIMS
check("CLAIM E01/E02: edparent coefficient falls from bivariate to multiple but stays large and significant",
      b_ed < b_biv and api_mult.pvalue()["edparent"] < 0.001)
check("CLAIM E03 A: meals not significant at 5% in the multiple regression", api_mult.pvalue()["meals"] > 0.05)
check("CLAIM E03 C: meals' simple slope is negative, but near zero once edparent alone is added",
      api_meals.coef()["meals"] < 0 and abs(api_me.coef()["meals"]) < 0.2 and api_me.pvalue()["meals"] > 0.05)
check("CLAIM E04: credteach/emerteach not perfectly collinear; both coefficients estimated",
      abs(corr.loc["credteach", "emerteach"]) < 0.99 and np.isfinite(api_mult.se()[["credteach", "emerteach"]]).all())
check("CLAIM E07: CRS not rejected at 5%", p_crs > 0.05)
check("CLAIM E11: post-1970 slope not significant at 5%", pc_post.pvalue()["urate"] > 0.05)
check("CLAIM E13 A: expected inflation highly significant in the augmented regression", pc_aug.pvalue()["inflgdp1yr"] < 0.001)
check("CLAIM E13 D: post-1970 unemployment and expected inflation positively related",
      gam > 0 and pe[["urate", "inflgdp1yr"]].corr().iloc[0, 1] > 0)
check("CLAIM E16: clustered SEs larger than default SEs for every slope",
      all(auto.se()[v] > auto_iid.se()[v] for v in ["lhp", "lcurbwt", "ltorque", "year"]))
check("CLAIM E17: 1985-2006 mean mpg stays within 24.5-26.0 ('near 25'); weight and horsepower rise",
      ym.loc[1985:2006, "mpg"].between(24.5, 26.0).all() and ym.loc[2006, "curbwt"] > ym.loc[1985, "curbwt"]
      and ym.loc[2006, "hp"] > ym.loc[1985, "hp"])
check("CLAIM E17 explanation: weight ~3,100 -> ~3,900 lb; hp roughly doubles (1985 -> 2006)",
      round(ym.loc[1985, "curbwt"], -2) == 3100 and round(ym.loc[2006, "curbwt"], -2) == 3900
      and 1.9 < ym.loc[2006, "hp"] / ym.loc[1985, "hp"] < 2.2)
check("CLAIM E17: positive year coefficient", auto.coef()["year"] > 0)
check("CLAIM E20: free-care and 95%-plan mean ages differ in the sample", abs(plan_age["Free Care"] - plan_age["95%/100% Coins"]) > 0.1)
check("CLAIM E21 C: 50% estimate lies between zero and the 25% estimate (not monotonic)",
      rct.coef()["coins25"] < rct.coef()["coins50"] < 0)
check("CLAIM E21: every cost-sharing plan's mean spending below free care", (plan_mean.drop("Free Care") < plan_mean["Free Care"]).all())
check("CLAIM E22: DiD significant at 5% (p = 0.031)", f3(did.pvalue()["postXhigh"]) == "0.031")
check("CLAIM E26: win coefficient significant (p < 0.001); positive margin slope", rdm.pvalue()["win"] < 0.001 and rdm.coef()["margin"] > 0)
check("CLAIM P27: win = 1 exactly when margin > 0", ((rd["margin"] > 0).astype(int) == rd["win"].astype(int)).all()
      and ((inc["margin"] > 0).astype(int) == inc["win"].astype(int)).all())
check("CLAIM E31: first-stage slope negative (higher mortality, weaker institutions)", fst.coef()["logem4"] < 0)
check("CLAIM E32: IV > OLS > 0", b_iv > b_ols > 0)
check("CLAIM report: API is slightly RIGHT-skewed (skew = +0.12), not left-skewed (qmd line 240)", f2(stats.skew(api["api99"])) == "0.12")
check("CLAIM report: average mpg rose ~31% from 1980 to 2005 (qmd line 884 says it 'didn't improve much')",
      round(100 * (ym.loc[2005, "mpg"] / ym.loc[1980, "mpg"] - 1)) == 31)
check("CLAIM report: RD margin ranges -100 to 100, inconsistent with 'vote share - 50%' (qmd line 1303)",
      inc["margin"].min() == -100 and inc["margin"].max() == 100)
check("CLAIM report: RAND data hold 5,915 distinct persons, not 5,809 (qmd lines 110, 954)", hie["idperson"].nunique() == 5915)
check("CLAIM report: expected inflation (inflgdp1yr) is missing for every pre-1970 year (qmd line 568 unverifiable)",
      pre["inflgdp1yr"].isna().all())
check("CLAIM report: HAC SEs are slightly SMALLER than classical SEs in the Cobb-Douglas fit",
      all(cd.se()[v] < pf.feols("lnq ~ lnk + lnl", data=cb).se()[v] for v in ["lnk", "lnl"]))

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
print(", ".join(sorted(nums, key=lambda v: float(v.replace(",", "") or 0))))
failed = [k for k, ok in checks.items() if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
sys.exit(1 if failed or not checks else 0)
