#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch15.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Run:  python3 quizzes/checks/ch15_factcheck.py      (exit 1 on any failure)
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

warnings.filterwarnings("ignore")

CHAPTER = "ch15"
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


def f(x: float, nd: int) -> str:
    return f"{x:.{nd}f}"


def pct_exact(b: float) -> float:
    """Exact % change implied by a log change b: 100 (e^b - 1)."""
    return 100 * (math.exp(b) - 1)


def wald(m, names):
    """Joint Wald (F) test that the named coefficients are zero (as in the chapter)."""
    idx = list(m.coef().index)
    R = np.eye(len(idx))[[idx.index(v) for v in names]]
    return m.wald_test(R=R)


# ---------------------------------------------------------------- 1. FACTS
raw = load("AED_EARNINGS_COMPLETE.DTA")
COLS = ["earnings", "lnearnings", "age", "agesq", "education", "agebyeduc", "gender",
        "dself", "dgovt", "dprivate", "lnhours", "lnage", "hours"]
# gender/hours are int8, age int16, the rest float32: cast everything to float64.
d = raw[COLS].astype(float)

lin = pf.feols("earnings ~ age + education", data=d, vcov="HC1")
ll = pf.feols("lnearnings ~ age + education", data=d, vcov="HC1")
lg = pf.feols("lnearnings ~ lnage + education", data=d, vcov="HC1")
q = pf.feols("earnings ~ age + agesq + education", data=d, vcov="HC1")
mix = pf.feols("earnings ~ gender + age + agesq + education + dself + dgovt + lnhours", data=d, vcov="HC1")
it = pf.feols("earnings ~ age + education + agebyeduc", data=d, vcov="HC1")
lm = pf.feols("lnearnings ~ gender + age + agesq + education + dself + dgovt + lnhours", data=d, vcov="HC1")

cl, cll, clg, cq, cmix, cit, clm = (m.coef() for m in (lin, ll, lg, q, mix, it, lm))
bq2, bq3 = cq["age"], cq["agesq"]
tp_q = -bq2 / (2 * bq3)
me_q = lambda a: bq2 + 2 * bq3 * a  # noqa: E731
sd_y = d.earnings.std()
bstar = {v: cmix[v] * d[v].std() / sd_y for v in ["gender", "age", "agesq", "education", "dself", "dgovt", "lnhours"]}
u = ll._u_hat
rmse = float(np.sqrt(np.mean(u ** 2)))           # the chapter's s_e (no df correction)
se_df = float(np.sqrt(np.sum(u ** 2) / (len(d) - 3)))
adj = math.exp(rmse ** 2 / 2)
smear = float(np.mean(np.exp(u)))
naive = np.exp(ll.predict())
F_q = wald(q, ["age", "agesq"])
F_age_it = wald(it, ["age", "agebyeduc"])
F_educ_it = wald(it, ["education", "agebyeduc"])

print(f"FACTS data: n={len(d)} age {d.age.min():.0f}-{d.age.max():.0f} mean age={d.age.mean():.4f} "
      f"educ {d.education.min():.0f}-{d.education.max():.0f} hours {d.hours.min():.0f}-{d.hours.max():.0f} "
      f"earnings mean={d.earnings.mean():.2f} median={d.earnings.median():.0f} min={d.earnings.min():.0f} "
      f"max={d.earnings.max():.0f} skew={d.earnings.skew():.3f} skew(ln)={d.lnearnings.skew():.3f}")
print(f"FACTS levels:  {dict(cl.round(4))} R2={lin._r2:.4f}")
print(f"FACTS loglin:  {dict(cll.round(6))} R2={ll._r2:.4f} exact educ%={pct_exact(cll['education']):.3f}")
print(f"FACTS loglog:  {dict(clg.round(6))} R2={lg._r2:.4f}")
print(f"FACTS quad:    {dict(cq.round(4))} t={dict(q.tstat().round(3))} R2={q._r2:.4f} TP={tp_q:.4f}")
print(f"FACTS quad ME: " + ", ".join(f"{a}:{me_q(a):.2f}" for a in (25, 30, 40, 45, 50, 55, 60, 65))
      + f" AME={me_q(d.age).mean():.4f} MEM={me_q(d.age.mean()):.4f}")
print(f"FACTS joint F: quad age={F_q['statistic']:.3f} (p={F_q['pvalue']:.2g}); "
      f"inter age={F_age_it['statistic']:.3f} (p={F_age_it['pvalue']:.2g}); inter educ={F_educ_it['statistic']:.3f} (p={F_educ_it['pvalue']:.2g})")
print(f"FACTS corr: age-agesq={d.age.corr(d.agesq):.4f} age-agebyeduc={d.age.corr(d.agebyeduc):.4f} "
      f"educ-agebyeduc={d.education.corr(d.agebyeduc):.4f}")
print(f"FACTS mix(levels): {dict(cmix.round(3))} sd_y={sd_y:.3f} sd_educ={d.education.std():.4f}")
print(f"FACTS beta*: {dict((k, round(v, 4)) for k, v in bstar.items())}")
print(f"FACTS inter:   {dict(cit.round(4))} se_int={it.se()['agebyeduc']:.4f} t_int={it.tstat()['agebyeduc']:.4f} "
      f"p_int={it.pvalue()['agebyeduc']:.4f} p_educ={it.pvalue()['education']:.4f} t_age={it.tstat()['age']:.4f}")
print(f"FACTS retrans: rmse={rmse:.5f} s_e(df)={se_df:.5f} factor={adj:.5f} smear={smear:.5f} actual={d.earnings.mean():.2f} "
      f"naive={naive.mean():.2f} adj={adj * naive.mean():.2f} smear_mean={smear * naive.mean():.2f}")
print(f"FACTS logmix:  {dict(clm.round(7))} p={dict(lm.pvalue().round(4))} R2={lm._r2:.4f} "
      f"TP={-clm['age'] / (2 * clm['agesq']):.3f}")
print()

# ---------------------------------------------------------------- 2. CHECKS (exam)
check("coverage: 872 workers aged 25-65; education 0-20; hours 35-99",
      len(d) == 872 and (d.age.min(), d.age.max()) == (25, 65) and (d.education.min(), d.education.max()) == (0, 20)
      and (d.hours.min(), d.hours.max()) == (35, 99))
check("derived columns are what the chapter says (lnearnings, agesq, agebyeduc, lnhours)",
      np.allclose(d.lnearnings, np.log(d.earnings), atol=1e-5) and np.allclose(d.agesq, d.age ** 2)
      and np.allclose(d.agebyeduc, d.age * d.education) and np.allclose(d.lnhours, np.log(d.hours), atol=1e-5))
check("float32 storage does not change the quadratic coefficients (raw vs float64)",
      np.allclose(pf.feols("earnings ~ age + agesq + education", data=raw, vcov="HC1").coef().values, cq.values, rtol=1e-6))
check("E01: log-linear 8.962 + 0.0078 age + 0.1006 educ; 10.1% (approx), 0.10",
      (f(cll["Intercept"], 3), f(cll["age"], 4), f(cll["education"], 4), f(100 * cll["education"], 1), f(cll["education"], 2))
      == ("8.962", "0.0078", "0.1006", "10.1", "0.10"))
check("E01 expl: exact one-year effect 10.6%", f(pct_exact(cll["education"]), 1) == "10.6")
check("E02: 4 x 0.1006 = 0.4024; exact 49.5; approx 40.2; 4 x exact-1yr 42.3; 100e^x 149.5",
      f(4 * 0.1006, 4) == "0.4024" and f(pct_exact(0.4024), 1) == "49.5" and f(100 * 0.4024, 1) == "40.2"
      and f(4 * pct_exact(0.1006), 1) == "42.3" and f(100 * math.exp(0.4024), 1) == "149.5")
check("E02: exact from exact coefficient also 49.5", f(pct_exact(4 * cll["education"]), 1) == "49.5")
check("E03: log-log 8.009 + 0.346 ln(age) + 0.1004 educ; 0.35 and 34.6",
      (f(clg["Intercept"], 3), f(clg["lnage"], 3), f(clg["education"], 4), f(clg["lnage"], 2), f(100 * clg["lnage"], 1))
      == ("8.009", "0.346", "0.1004", "0.35", "34.6"))
check("E03 expl: 1% of age 40 = 0.4 years", f(0.01 * 40, 1) == "0.4")
check("E04: 0.0078 x 60,000 = 468; 0.78; 4.68 (0.0078%); 11.7 ~ 12 (log-log formula, age 40); 0.78%",
      round(0.0078 * 60000) == 468 and f(100 * 0.0078, 2) == "0.78" and f(0.0078 / 100 * 60000, 2) == "4.68"
      and round(0.0078 * 60000 / 40) == 12)
check("E05: mean 56,369 > median 44,200; min 4,000 > 0",
      round(d.earnings.mean()) == 56369 and d.earnings.median() == 44200 and d.earnings.min() == 4000)
check("E06: R2 log-linear 0.190, levels 0.115", (f(ll._r2, 3), f(lin._r2, 3)) == ("0.190", "0.115"))
check("E07/E08/E09: quad -98,620 + 3,105 age - 29.66 age^2 + 5,740 educ",
      (round(cq["Intercept"]), round(bq2), f(bq3, 2), round(cq["education"])) == (-98620, 3105, "-29.66", 5740))
check("E08: TP 52.3 (shown and exact); 4b3 26.2; no-2 104.7; mean age 43.3",
      f(3105 / (2 * 29.66), 1) == "52.3" and f(tp_q, 1) == "52.3" and f(3105 / (4 * 29.66), 1) == "26.2"
      and f(3105 / 29.66, 1) == "104.7" and f(d.age.mean(), 1) == "43.3")
check("E08 expl: 2 x 29.66 = 59.32", f(2 * 29.66, 2) == "59.32")
check("E09: ME(40) = 732; 3105 - 29.66x40 = 1,919; -2x29.66x40 = -2,373",
      round(3105 - 2 * 29.66 * 40) == 732 and round(me_q(40)) == 732 and round(3105 - 29.66 * 40) == 1919
      and round(-2 * 29.66 * 40) == -2373)
check("E09 expl / E10 expl: ME(25) = 1,622; ME(60) = -454", round(me_q(25)) == 1622 and round(me_q(60)) == -454)
check("E12: AME = MEM = 536", math.isclose(me_q(d.age).mean(), me_q(d.age.mean()), rel_tol=1e-9) and round(me_q(d.age.mean())) == 536)
check("E14: t(age) 2.86, t(agesq) -2.38; corr 0.99; F 18.6, p < 0.001",
      (f(q.tstat()["age"], 2), f(q.tstat()["agesq"], 2), f(d.age.corr(d.agesq), 2), f(F_q["statistic"], 1))
      == ("2.86", "-2.38", "0.99", "18.6") and F_q["pvalue"] < 0.001)
check("E15: mix educ 5,399; s_educ 2.884; s_y 51,516; beta* 0.30",
      (round(cmix["education"]), f(d.education.std(), 3), round(sd_y), f(bstar["education"], 2)) == (5399, "2.884", 51516, "0.30"))
check("E15 distractors: 0.10 (no s_x), 0.87 (variance), 15,571 (no s_y); shown-value key 0.30",
      (f(5399 / 51516, 2), f(5399 * 2.884 ** 2 / 51516, 2), round(5399 * 2.884), f(5399 * 2.884 / 51516, 2))
      == ("0.10", "0.87", 15571, "0.30"))
check("E15 expl: SD education about 2.9 years", f(d.education.std(), 1) == "2.9")
check("E16/E17: beta* lnhours 0.22, age 0.68, agesq -0.57, gender -0.14, dself 0.05, dgovt -0.002",
      (f(bstar["lnhours"], 2), f(bstar["age"], 2), f(bstar["agesq"], 2), f(bstar["gender"], 2), f(bstar["dself"], 2), f(bstar["dgovt"], 3))
      == ("0.22", "0.68", "-0.57", "-0.14", "0.05", "-0.002"))
check("E16 expl: 0.22 x 51,516 ~ $11,300 (shown values; exact b* gives 11,500)",
      round(0.22 * 51516, -2) == 11300 and round(bstar["lnhours"] * sd_y, -2) == 11500)
check("E20 expl: ME of education at mean age 43.3 ~ $5,770 (shown and exact)",
      round(4515 + 29.04 * 43.3, -1) == 5770 and round(cit["education"] + cit["agebyeduc"] * d.age.mean(), -1) == 5770
      and f(d.age.mean(), 1) == "43.3" and round(d.age.mean()) == 43)
check("E18/E21: interaction -29,089 + 127 age + 4,515 educ + 29.04 age x educ",
      (round(cit["Intercept"]), round(cit["age"]), round(cit["education"]), f(cit["agebyeduc"], 2)) == (-29089, 127, 4515, "29.04"))
check("E18: ME educ at 50 = 5,967; 29.04 x 50 = 1,452; 4,515 + 29.04 = 4,544",
      round(4515 + 29.04 * 50) == 5967 and round(cit["education"] + cit["agebyeduc"] * 50) == 5967
      and round(29.04 * 50) == 1452 and round(4515 + 29.04) == 4544)
check("E19: interaction se 56.05, t 0.52, p 0.60; about $29",
      (f(it.se()["agebyeduc"], 2), f(it.tstat()["agebyeduc"], 2), f(it.pvalue()["agebyeduc"], 2), round(cit["agebyeduc"]))
      == ("56.05", "0.52", "0.60", 29))
check("E21: ME age at educ 16 = 592; 29.04 x 16 = 465 (464.6); 4,515 + 464.6 = 4,980",
      round(127 + 29.04 * 16) == 592 and round(cit["age"] + cit["agebyeduc"] * 16) == 592
      and round(29.04 * 16) == 465 and f(29.04 * 16, 1) == "464.6" and round(4515 + 29.04 * 16) == 4980)
check("E23: s_e 0.615 (chapter RMSE); factor 1.21 (shown and exact); df-corrected s_e also gives 1.21",
      f(rmse, 3) == "0.615" and f(math.exp(0.615 ** 2 / 2), 2) == "1.21" and f(adj, 2) == "1.21"
      and f(math.exp(se_df ** 2 / 2), 2) == "1.21")
check("E23 distractors: exp(s/2) 1.36, exp(s^2) 1.46, exp(s) 1.85; exp(0.189)",
      (f(math.exp(0.615 / 2), 2), f(math.exp(0.615 ** 2), 2), f(math.exp(0.615), 2), f(0.615 ** 2 / 2, 3))
      == ("1.36", "1.46", "1.85", "0.189"))
check("E23 expl: naive mean ~45,800, adjusted ~55,400, actual 56,369",
      round(naive.mean(), -2) == 45800 and round(adj * naive.mean(), -2) == 55400 and round(d.earnings.mean()) == 56369)
check("E24 expl: smearing gives essentially the same correction as the normal factor (1.22 vs 1.21)",
      abs(smear - adj) < 0.02 and f(smear, 2) == "1.22")
check("E26: logmix gender -0.193 (unrounded -0.1928); approx 19%; 0.19; exact -17.5% from the unrounded value",
      f(clm["gender"], 3) == "-0.193" and f(clm["gender"], 4) == "-0.1928" and round(100 * 0.193) == 19
      and f(pct_exact(clm["gender"]), 1) == "-17.5")
check("E27: lnhours 0.975; 10% -> 9.75% (approx); exact 9.74%; 0.975 x 4 = 3.9; 97.5",
      f(clm["lnhours"], 3) == "0.975" and f(0.975 * 10, 2) == "9.75" and f(100 * (1.1 ** 0.975 - 1), 2) == "9.74"
      and f(100 * (1.1 ** clm["lnhours"] - 1), 2) == "9.74" and f(0.975 * 4, 1) == "3.9" and f(100 * 0.975, 1) == "97.5"
      and 44 / 40 == 1.1)
check("E28: age 0.0561, agesq -0.000549; ME% at 30 = 2.3 (shown and exact); 5.6; 4.0; 0.023",
      (f(clm["age"], 4), f(clm["agesq"], 6)) == ("0.0561", "-0.000549")
      and f(100 * (0.0561 - 2 * 0.000549 * 30), 1) == "2.3" and f(100 * (clm["age"] + 2 * clm["agesq"] * 30), 1) == "2.3"
      and f(100 * 0.0561, 1) == "5.6" and f(100 * (0.0561 - 0.000549 * 30), 1) == "4.0"
      and f(0.0561 - 2 * 0.000549 * 30, 3) == "0.023")
check("E28 expl: 0.0232, 0.0329; logmix TP about 51", f(0.0561 - 2 * 0.000549 * 30, 4) == "0.0232"
      and f(2 * 0.000549 * 30, 4) == "0.0329" and round(-clm["age"] / (2 * clm["agesq"])) == 51)
check("E29: lnhours / educ about ten times (0.975 / 0.093)", f(clm["education"], 3) == "0.093" and round(clm["lnhours"] / clm["education"]) == 10)
check("E30: dself -0.118 (p 0.24), dgovt 0.070 (p 0.13)",
      (f(clm["dself"], 3), f(lm.pvalue()["dself"], 2), f(clm["dgovt"], 3), f(lm.pvalue()["dgovt"], 2)) == ("-0.118", "0.24", "0.070", "0.13"))

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic)
check("P01: 100(e^0.08 - 1) = 8.3", f(pct_exact(0.08), 1) == "8.3")
check("P02: 28.4 exact, 22.1 reversed base, 128.4 no -1",
      (f(pct_exact(0.25), 1), f(100 * (1 - math.exp(-0.25)), 1), f(100 * math.exp(0.25), 1)) == ("28.4", "22.1", "128.4"))
check("P04: 0.03 x 40,000 = 1,200; 0.0003 x 40,000 = 12; /10 = 120", (0.03 * 40000, round(0.0003 * 40000), 0.03 * 40000 / 10) == (1200, 12, 120))
check("P07: U shape min at x = 4", -(-4) / (2 * 0.5) == 4)
check("P08: TP -0.375; -0.75; -0.1875", (-3 / 8, -3 / 4, -3 / 16) == (-0.375, -0.75, -0.1875))
check("P09-P12: ME = 3 + 8x: 11, 19, 27; AME 19; 3 + 4x2 = 11; 2x4x2 = 16",
      [3 + 8 * x for x in (1, 2, 3)] == [11, 19, 27] and sum(3 + 8 * x for x in (1, 2, 3)) / 3 == 19 and 3 + 4 * 2 == 11 and 2 * 4 * 2 == 16)
check("P15/P17: beta* educ 0.36, age 0.20, hours 0.064; 0.12; 1.08; 9,000; ratios 2.5 vs 3.1",
      (3000 * 3 / 25000, 500 * 10 / 25000, 200 * 8 / 25000, 3000 / 25000, 3000 * 9 / 25000, 3000 * 3) == (0.36, 0.2, 0.064, 0.12, 1.08, 9000)
      and 500 / 200 == 2.5 and f(0.2 / 0.064, 1) == "3.1")
check("P18/P21: ME_x(d=1) 9; 2+4+7 = 13; ME_d(x=3) 25; 4+7 = 11; 7x3 = 21",
      (2 + 7, 2 + 4 + 7, 4 + 7 * 3, 4 + 7, 7 * 3) == (9, 13, 25, 11, 21))
check("P23: e^3 = 20.09; x e^0.045 = 21.01; x e^0.09 = 21.98; x e^0.15 = 23.34; 1.046; 4.6%",
      (f(math.exp(3), 2), f(math.exp(3.045), 2), f(math.exp(3.09), 2), f(math.exp(3.15), 2), f(math.exp(0.045), 3), f(pct_exact(0.045), 1))
      == ("20.09", "21.01", "21.98", "23.34", "1.046", "4.6"))
check("P25: exp(0.8^2/2) = exp(0.32) = 1.377 ~ 1.38, about 38%",
      math.isclose(0.8 ** 2 / 2, 0.32) and f(math.exp(0.32), 3) == "1.377" and round(100 * (math.exp(0.32) - 1)) == 38)
check("P26: exact rural -11.3%", f(pct_exact(-0.12), 1) == "-11.3")
check("P27: 0.6 x 5 = 3; 5/0.6 = 8.3", (round(0.6 * 5, 6), f(5 / 0.6, 1)) == (3.0, "8.3"))
check("P28: 0.04 - 2x0.0005x10 = 0.03; 0.04 - 0.0005x10 = 0.035",
      (round(0.04 - 2 * 0.0005 * 10, 6), round(0.04 - 0.0005 * 10, 6)) == (0.03, 0.035))

# ---------------------------------------------------------------- 3. CLAIMS
check("E05: earnings right-skewed (mean > median, skew > 1) and ln(earnings) nearly symmetric",
      d.earnings.mean() > d.earnings.median() and d.earnings.skew() > 1 and abs(d.lnearnings.skew()) < 0.3)
check("E06: in-sample, the bias-corrected log model predicts dollars slightly better than levels (so only 'does not show' is safe)",
      np.mean((d.earnings - adj * naive) ** 2) < np.mean((d.earnings - lin.predict()) ** 2))
check("E07/E10: inverted U; predicted earnings fall between the turning point and 65; ME(65) < 0",
      bq3 < 0 and bq2 > 0 and 25 < tp_q < 65 and me_q(65) < 0)
check("E10: ME declines with age (ME(25) > ME(40) > ME(60))", me_q(25) > me_q(40) > me_q(60))
check("E14: both quadratic terms individually significant at 5%",
      q.pvalue()["age"] < 0.05 and q.pvalue()["agesq"] < 0.05 and abs(q.tstat()["agesq"]) > 1.96)
check("E14: corr(age, agesq) is high but not perfect", 0.95 < d.age.corr(d.agesq) < 1)
check("E17: dgovt standardized coefficient essentially zero (|b*| < 0.01)", abs(bstar["dgovt"]) < 0.01)
check("E19: interaction insignificant (p > 0.5) while education joint test rejects (p < 0.001)",
      it.pvalue()["agebyeduc"] > 0.5 and F_educ_it["pvalue"] < 0.001)
check("E21 context: age joint test in the interaction model rejects although t(age) is tiny",
      F_age_it["pvalue"] < 0.01 and abs(it.tstat()["age"]) < 0.5)
check("E22: OLS log residuals average zero (so the 'negative average' distractor is false)", abs(u.mean()) < 1e-8)
check("E22: Jensen in the data: mean exp(u) > 1", smear > 1)
check("E23/E25: naive predictions underpredict the mean; corrected mean closer to actual",
      naive.mean() < d.earnings.mean() and abs(adj * naive.mean() - d.earnings.mean()) < abs(naive.mean() - d.earnings.mean()))
check("E26: gender coefficient is negative and significant", clm["gender"] < 0 and lm.pvalue()["gender"] < 0.001)
check("E26 note: raw log gap (-0.197) is close to the controlled -0.193, so no 'before controls' distractor is used",
      abs((d.lnearnings[d.gender == 1].mean() - d.lnearnings[d.gender == 0].mean()) - clm["gender"]) < 0.01)
check("E26: gender R2-type share is not 19% (R2 of ln(earnings) on gender alone far from 0.19)",
      abs(pf.feols("lnearnings ~ gender", data=d)._r2 - 0.19) > 0.1)
check("E27: 40 and 44 hours are inside the data's 35-99 range", d.hours.min() <= 40 and d.hours.max() >= 44)
check("E28: age 30 inside the range; ME% positive at 30", 25 <= 30 <= 65 and clm["age"] + 2 * clm["agesq"] * 30 > 0)
check("E30: sector dummies are exclusive, private sector is the omitted group",
      ((d.dself + d.dgovt + d.dprivate) == 1).all() and (d.dself + d.dgovt).max() == 1)
check("E30: dself and dgovt insignificant at 5%", lm.pvalue()["dself"] > 0.05 and lm.pvalue()["dgovt"] > 0.05)
check("E04/E13 context: quadratic within data range (no prediction outside 25-65 asked)", d.age.between(25, 65).all())

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
