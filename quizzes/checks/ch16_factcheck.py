#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch16.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Reproduces the chapter's exact settings: pyfixest OLS with HC1 (and default) SEs on
AED_EARNINGS_COMPLETE (earnings ~ age + education [+ agebyeduc]); statsmodels VIFs with a
constant; the auxiliary regression agebyeduc ~ age + education; Wald tests on the HC1 model;
AED_DEMOCRACY bivariate and multiple regressions with HC1; OLSInfluence on the statsmodels
twin of the multiple regression (DFITS 2*sqrt(k/n), DFBETAS 2/sqrt(n), Cook's 4/n); the AR(1)
simulation with seed 10101, n = 10,000, rho = 0.8 (draw order e then v).
Run:  python3 quizzes/checks/ch16_factcheck.py      (exit 1 on any failure)
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
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import OLSInfluence, variance_inflation_factor
from statsmodels.tsa.stattools import acf

warnings.filterwarnings("ignore")

CHAPTER = "ch16"
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
# --- Earnings: multicollinearity and heteroskedasticity (Sections 16.1, 16.5)
e = load("AED_EARNINGS_COMPLETE.DTA")
for c in ["earnings", "age", "education", "agebyeduc"]:
    e[c] = e[c].astype(float)  # age is int16 in the file
n_e = len(e)
base_hc1 = pf.feols("earnings ~ age + education", data=e, vcov="HC1")
base_def = pf.feols("earnings ~ age + education", data=e)
coll = pf.feols("earnings ~ age + education + agebyeduc", data=e, vcov="HC1")
corr = e[["age", "education", "agebyeduc"]].corr()
Xv = sm.add_constant(e[["age", "education", "agebyeduc"]])
vif = {v: variance_inflation_factor(Xv.values, i) for i, v in enumerate(Xv.columns)}
aux = pf.feols("agebyeduc ~ age + education", data=e)
r2_aux = aux._r2
e["age_c"] = e["age"] - e["age"].mean()
e["educ_c"] = e["education"] - e["education"].mean()
e["inter_c"] = e["age_c"] * e["educ_c"]
Xc = sm.add_constant(e[["age_c", "educ_c", "inter_c"]])
vif_c = [variance_inflation_factor(Xc.values, i) for i in range(1, 4)]
names = list(coll.coef().index)


def wald_p(vs):
    R = np.eye(len(names))[[names.index(v) for v in vs]]
    return float(coll.wald_test(R=R)["pvalue"])


p_joint_age = wald_p(["age", "agebyeduc"])
p_joint_educ = wald_p(["education", "agebyeduc"])
ratio_se = base_hc1.se() / base_def.se()
reset_m = smf.ols("earnings ~ age + education", data=e).fit()
e["yh"] = reset_m.fittedvalues
reset_F, reset_p, _ = smf.ols("earnings ~ age + education + I(yh**2) + I(yh**3)", data=e).fit().compare_f_test(reset_m)

print(f"FACTS earnings n={n_e}; educ range {e.education.min():.0f}-{e.education.max():.0f}; columns include experience? {'experience' in e.columns}")
print("FACTS base (HC1 / default):")
print(pd.DataFrame({"b": base_hc1.coef(), "se_hc1": base_hc1.se(), "se_def": base_def.se(), "ratio": ratio_se,
                    "t_hc1": base_hc1.tstat(), "t_def": base_def.tstat()}).round(4).to_string())
print(f"FACTS base R2={base_hc1._r2:.4f}  collinear R2={coll._r2:.4f}")
print(pd.DataFrame({"b": coll.coef(), "se": coll.se(), "t": coll.tstat(), "p": coll.pvalue()}).round(4).to_string())
print("FACTS corr:\n" + corr.round(4).to_string())
print(f"FACTS VIF: {{k: round(v, 3) for k, v in vif.items()}} -> {({k: round(v, 3) for k, v in vif.items()})}")
print(f"FACTS aux R2={r2_aux:.5f} 1/(1-R2)={1 / (1 - r2_aux):.3f}; centered VIFs={np.round(vif_c, 4)}")
print(f"FACTS Wald p (age, agebyeduc)={p_joint_age:.5f}; (education, agebyeduc)={p_joint_educ:.3e}")
print(f"FACTS RESET F={reset_F:.3f} p={reset_p:.2e}")

# --- Democracy and growth (Sections 16.7-16.8)
d = load("AED_DEMOCRACY.DTA")
n_d = len(d)
CTRL = "constraint + indcent + catholic + muslim + protestant"
biv = pf.feols("democracy ~ growth", data=d, vcov="HC1")
mul = pf.feols(f"democracy ~ growth + {CTRL}", data=d, vcov="HC1")
k_d = len(mul.coef())
dm = smf.ols(f"democracy ~ growth + {CTRL}", data=d).fit()
inf = OLSInfluence(dm)
dfits = inf.dffits[0]
th_dfits = 2 * math.sqrt(k_d / n_d)
dfb = inf.dfbetas
th_dfb = 2 / math.sqrt(n_d)
cooks = inf.cooks_distance[0]
th_cook = 4 / n_d
r_dem = pf.feols(f"democracy ~ {CTRL}", data=d)._u_hat
r_gro = pf.feols(f"growth ~ {CTRL}", data=d)._u_hat
av_slope = float(np.polyfit(r_gro, r_dem, 1)[0])
cor_d = d[["democracy", "growth", "constraint", "indcent", "catholic", "muslim", "protestant"]].corr()
print(f"\nFACTS democracy n={n_d} k={k_d}")
print(f"FACTS bivariate growth b={biv.coef()['growth']:.4f} se={biv.se()['growth']:.4f} t={biv.tstat()['growth']:.3f} R2={biv._r2:.4f}")
print(f"FACTS multiple growth b={mul.coef()['growth']:.4f} se={mul.se()['growth']:.4f} t={mul.tstat()['growth']:.3f} "
      f"p={mul.pvalue()['growth']:.4f} R2={mul._r2:.4f} reduction={1 - mul.coef()['growth'] / biv.coef()['growth']:.4f}")
print("FACTS multiple coefs:\n" + mul.coef().round(4).to_string())
print("FACTS corr with democracy/growth:\n" + cor_d[["democracy", "growth"]].round(3).to_string())
print(f"FACTS DFITS th={th_dfits:.4f} exceed={int((np.abs(dfits) > th_dfits).sum())} max|DFITS|={np.abs(dfits).max():.3f}")
print(f"FACTS DFBETAS th={th_dfb:.4f} exceed per coef={(np.abs(dfb) > th_dfb).sum(axis=0)}")
print(f"FACTS Cook th={th_cook:.4f} exceed={int((cooks > th_cook).sum())}; AV slope={av_slope:.4f}")

# --- AR(1) simulation (Section 16.6)
n_s = 10000
np.random.seed(10101)
eps = np.random.normal(0, 1, n_s)
u = np.zeros(n_s)
for t in range(1, n_s):
    u[t] = 0.8 * u[t - 1] + eps[t]
v = np.random.normal(0, 1, n_s)
x = np.zeros(n_s)
for t in range(1, n_s):
    x[t] = 0.8 * x[t - 1] + v[t]
ts = pd.DataFrame({"y1": 1 + 2 * x + u, "x": x})
fts = pf.feols("y1 ~ x", data=ts)
rho_hat = acf(fts._u_hat, nlags=10, fft=False)
L_rule = 0.75 * n_s ** (1 / 3)
hac = smf.ols("y1 ~ x", data=ts).fit(cov_type="HAC", cov_kwds={"maxlags": 16})
print(f"\nFACTS sim slope={fts.coef()['x']:.4f} se_def={fts.se()['x']:.5f} se_HAC16={hac.bse['x']:.5f} "
      f"ratio={hac.bse['x'] / fts.se()['x']:.3f}; acf={np.round(rho_hat, 4)}; L={L_rule:.3f}")
print()

# ---------------------------------------------------------------- 2. CHECKS (exam)
check("872 workers; 131 countries", n_e == 872 and n_d == 131)
check("E01: age robust SE 151 -> 719; coefficient 525 -> 127",
      (round(base_hc1.se()["age"]), round(coll.se()["age"]), round(base_hc1.coef()["age"]), round(coll.coef()["age"]))
      == (151, 719, 525, 127))
check("E02: aux R2 = 0.973; VIF ~37 (1/0.027 = 37.04; exact 36.88)",
      f3(r2_aux) == "0.973" and round(1 / (1 - 0.973)) == 37 and round(1 / (1 - r2_aux)) == 37)
check("E02 distractors: 1/0.973 = 1.03; sqrt(37) = 6.1; 1/(1-0.973^2) = 19",
      (f2(1 / 0.973), f1(math.sqrt(37)), round(1 / (1 - 0.973 ** 2))) == ("1.03", "6.1", 19))
check("E03: VIFs of centered age, education, interaction all below 1.05 (exact 1.004, 1.016, 1.018)",
      all(vv < 1.05 for vv in vif_c))
check("E03: uncentered VIFs (age 22.0, education 17.3, agebyeduc 36.9) all above 10",
      (f1(vif["age"]), f1(vif["education"]), f1(vif["agebyeduc"])) == ("22.0", "17.3", "36.9"))
check("E04: education VIF 17.3; sqrt(17.3) = 4.2; 17.3^2 = 299; 1 - 1/17.3 = 0.94",
      (f1(math.sqrt(17.3)), round(17.3 ** 2), f2(1 - 1 / 17.3)) == ("4.2", 299, "0.94"))
check("E05: age t = 0.18 (p = 0.86), agebyeduc t = 0.52 (p = 0.60), joint p ~ 0.002",
      (f2(coll.tstat()["age"]), f2(coll.pvalue()["age"]), f2(coll.tstat()["agebyeduc"]), f2(coll.pvalue()["agebyeduc"]),
       f3(p_joint_age)) == ("0.18", "0.86", "0.52", "0.60", "0.002"))
check("E06: R2 0.1150 (base) vs 0.1153 (with interaction)", (f"{base_hc1._r2:.4f}", f"{coll._r2:.4f}") == ("0.1150", "0.1153"))
check("E12: education coefficient 5,811; default SE 570; robust SE 642",
      (round(base_hc1.coef()["education"]), round(base_def.se()["education"]), round(base_hc1.se()["education"])) == (5811, 570, 642))
check("E12: shown factors 5,811/642 = 9.1; 5,811/570 = 10.2; 10.2 x 642/570 = 11.5; 642/5,811 = 0.11",
      (f1(5811 / 642), f1(5811 / 570), f1(5811 / 570 * 642 / 570), f2(642 / 5811)) == ("9.1", "10.2", "11.5", "0.11"))
check("E12: exact robust t 9.06 rounds to 9.1; default t 10.19", (f1(base_hc1.tstat()["education"]), f2(base_def.tstat()["education"])) == ("9.1", "10.19"))
check("E13: age SEs 154 (default) vs 151 (robust)", (round(base_def.se()["age"]), round(base_hc1.se()["age"])) == (154, 151))
check("E15/E16: residual ACF lag 1 = 0.80, lag 5 = 0.31, lag 10 = 0.09",
      (f2(rho_hat[1]), f2(rho_hat[5]), f2(rho_hat[10])) == ("0.80", "0.31", "0.09"))
check("E17: (1+0.8)/(1-0.8) = 9; 10,000/9 = 1,111; n(1-rho) = 2,000; n*rho = 8,000; 9n = 90,000",
      (round((1 + 0.8) / (1 - 0.8), 9), round(10000 / 9), round(10000 * (1 - 0.8)), round(10000 * 0.8), 9 * 10000)
      == (9, 1111, 2000, 8000, 90000))
check("E18: simulated slope 2.006 (true value 2)", f3(fts.coef()["x"]) == "2.006")
check("E19: 0.75 x 10,000^(1/3) = 16.2 (~16); 0.75 x sqrt(10,000) = 75; 10,000^(1/3) = 21.5 (~22); 0.75 x 10,000 = 7,500",
      (round(L_rule), round(0.75 * math.sqrt(10000)), round(10000 ** (1 / 3)), round(0.75 * 10000)) == (16, 75, 22, 7500))
check("E19: 0.75 x 8,000^(1/3) = 15; 8,000^(1/3) = 20; 0.75 x sqrt(8,000) = 67; 0.75 x 8,000 = 6,000",
      (round(0.75 * 8000 ** (1 / 3)), round(8000 ** (1 / 3)), round(0.75 * math.sqrt(8000)), round(0.75 * 8000)) == (15, 20, 67, 6000))
check("E20: growth 0.131 (t 6.7) -> 0.047 (t 1.8, p 0.07)",
      (f3(biv.coef()["growth"]), f1(biv.tstat()["growth"]), f3(mul.coef()["growth"]), f1(mul.tstat()["growth"]), f2(mul.pvalue()["growth"]))
      == ("0.131", "6.7", "0.047", "1.8", "0.07"))
check("E20 explanation: 64% reduction", round(100 * (1 - mul.coef()["growth"] / biv.coef()["growth"])) == 64)
check("E23: added-variable slope equals multiple-regression growth coefficient", abs(av_slope - mul.coef()["growth"]) < 1e-6)
check("E24: k = 7, n = 131; 2*sqrt(7/131) = 0.46; sqrt(7/131) = 0.23; 2/sqrt(131) = 0.17; 2*7/131 = 0.11",
      (k_d, f2(th_dfits), f2(math.sqrt(7 / 131)), f2(2 / math.sqrt(131)), f2(2 * 7 / 131)) == (7, "0.46", "0.23", "0.17", "0.11"))
check("E26: five of 131 countries exceed the DFITS threshold; 131 - 5 = 126",
      int((np.abs(dfits) > th_dfits).sum()) == 5 and n_d - 5 == 126)
check("E28: 4/131 = 0.031; 2/131 = 0.015; 1/131 = 0.008; 4/sqrt(131) = 0.35",
      (f3(4 / 131), f3(2 / 131), f3(1 / 131), f2(4 / math.sqrt(131))) == ("0.031", "0.015", "0.008", "0.35"))
check("E29: RESET on earnings ~ age + education rejects (p < 0.001)", reset_p < 0.001)

check("E03 feedback: centered VIFs 1.00, 1.02, 1.02", [f2(vv) for vv in vif_c] == ["1.00", "1.02", "1.02"])
check("E13 explanation / P03 / P04: ratios 0.98 and 1.12; VIF 5 <-> R2 0.80, VIF 10 <-> R2 0.90; sqrt(10) = 3.2",
      (f2(ratio_se["age"]), f2(ratio_se["education"]), round(1 / (1 - 0.80), 9), round(1 / (1 - 0.90), 9), f1(math.sqrt(10)))
      == ("0.98", "1.12", 5, 10, "3.2"))
check("E16 explanation: 0.8^5 = 0.33; P24 feedback sqrt(0.05) = 0.224; E24 sqrt(7/131) = 0.231",
      (f2(0.8 ** 5), f3(math.sqrt(0.05)), f3(math.sqrt(7 / 131))) == ("0.33", "0.224", "0.231"))

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic)
check("P02: 1/(1-0.95) = 20; 1/0.95 = 1.05; sqrt(20) = 4.5; 1/(1-0.95^2) = 10.3",
      (round(1 / (1 - 0.95)), f2(1 / 0.95), f1(math.sqrt(20)), f1(1 / (1 - 0.95 ** 2))) == (20, "1.05", "4.5", "10.3"))
check("P03: VIF = 1 <=> R2_j = 0", 1 / (1 - 0.0) == 1)
check("P04: sqrt(9) = 3; 9^2 = 81; 1 - 1/9 = 0.89", (math.sqrt(9), 9 ** 2, f2(1 - 1 / 9)) == (3.0, 81, "0.89"))
check("P12: 2.40/1.20 = 2.0; 2.40/0.80 = 3.0; 3.0 x 1.5 = 4.5; 1.20/2.40 = 0.5",
      (f1(2.4 / 1.2), f1(2.4 / 0.8), f1(2.4 / 0.8 * 1.2 / 0.8), f1(1.2 / 2.4)) == ("2.0", "3.0", "4.5", "0.5"))
check("P16: 0.6, 0.6^2 = 0.36, 0.6^3 = 0.22", (f2(0.6 ** 2), f2(0.6 ** 3)) == ("0.36", "0.22"))
check("P17: (1+0.5)/(1-0.5) = 3; 300/3 = 100; 300 x 0.5 = 150; 3 x 300 = 900; 300/sqrt(3) = 173",
      (round(1.5 / 0.5, 9), round(300 / 3), round(300 * 0.5), 3 * 300, round(300 / math.sqrt(3))) == (3, 100, 150, 900, 173))
check("P19: 0.75 x 1,000^(1/3) = 7.5; 0.75 x sqrt(1,000) = 24; 0.75 x 1,000 = 750; 1,000^(1/3) = 10",
      (f1(0.75 * 1000 ** (1 / 3)), round(0.75 * math.sqrt(1000)), round(0.75 * 1000), round(1000 ** (1 / 3))) == ("7.5", 24, 750, 10))
check("P20: (0.10-0.07)/0.10 = 30%; 0.03/0.07 = 43%; 0.07/0.10 = 70%; 0.10-0.07 = 0.03",
      (round(100 * (0.10 - 0.07) / 0.10), round(100 * 0.03 / 0.07), round(100 * 0.07 / 0.10), f2(0.10 - 0.07)) == (30, 43, 70, "0.03"))
check("P24: k = 5, n = 100: 2*sqrt(0.05) = 0.45; sqrt(0.05) = 0.22; 2/sqrt(100) = 0.20; 2*5/100 = 0.10",
      (f2(2 * math.sqrt(5 / 100)), f2(math.sqrt(5 / 100)), f2(2 / math.sqrt(100)), f2(2 * 5 / 100)) == ("0.45", "0.22", "0.20", "0.10"))
check("P25: n = 100: DFBETAS threshold 2/sqrt(100) = 0.20 < 0.35", 2 / math.sqrt(100) == 0.2 and 0.35 > 0.2)
check("P28: n = 200: 4/200 = 0.02; 2/200 = 0.01; 1/200 = 0.005; 4/sqrt(200) = 0.28",
      (f2(4 / 200), f2(2 / 200), f3(1 / 200), f2(4 / math.sqrt(200))) == ("0.02", "0.01", "0.005", "0.28"))

# ---------------------------------------------------------------- 3. CLAIMS
check("CLAIM E01/E05: interaction model inflates age SE more than 4-fold", coll.se()["age"] / base_hc1.se()["age"] > 4)
check("CLAIM E03: centering cuts every VIF from above 10 to about 1",
      min(vif["age"], vif["education"], vif["agebyeduc"]) > 10 and max(vif_c) < 1.05)
check("CLAIM E05: joint test of education and agebyeduc also highly significant (p < 0.001)", p_joint_educ < 0.001)
check("CLAIM E06: adding the interaction changes R2 by less than 0.001", abs(coll._r2 - base_hc1._r2) < 0.001)
check("CLAIM E13: robust/default SE ratios modest (age 0.98, education 1.12; both within 0.95-1.15)",
      0.95 < ratio_se["age"] < 1.0 and 1.0 < ratio_se["education"] < 1.15)
check("CLAIM E13: robust SE smaller than default for age", base_hc1.se()["age"] < base_def.se()["age"])
check("CLAIM E16/E15: residual ACF positive and declining over lags 1-10", all(rho_hat[i] > rho_hat[i + 1] > 0 for i in range(1, 10)))
check("CLAIM E16: lag-1 to lag-5 decay roughly geometric (0.8^5 = 0.33 vs 0.31)", abs(rho_hat[5] - 0.8 ** 5) < 0.03)
check("CLAIM E20: every control's democracy effect x its correlation with growth is positive (bias upward)",
      all(np.sign(mul.coef()[c]) * np.sign(cor_d.loc[c, "growth"]) > 0
          for c in ["constraint", "indcent", "catholic", "muslim", "protestant"]))
check("CLAIM E20: bivariate growth significant at 1%, multiple not at 5%", biv.pvalue()["growth"] < 0.01 and mul.pvalue()["growth"] > 0.05)
check("CLAIM E24/E26: no |DFITS| above 1 (max 0.70)", np.abs(dfits).max() < 1)
check("CLAIM Cook's: five countries above 4/n", int((cooks > th_cook).sum()) == 5)

# round-1 review claims
check("CLAIM E15: residuals uncorrelated with x by construction (|r| < 1e-8); R2 of y1 on x is 0.80 (old option C was true)",
      abs(np.corrcoef(fts._u_hat, x)[0, 1]) < 1e-8 and f2(fts._r2) == "0.80")
Xg = sm.add_constant(d[["growth", "constraint", "indcent", "catholic", "muslim", "protestant"]].astype(float))
vif_growth = variance_inflation_factor(Xg.values, 1)
check("CLAIM E10: growth not highly collinear in the data (VIF 1.57; r(growth, indcent) = -0.46)",
      f2(vif_growth) == "1.57" and f2(cor_d.loc["indcent", "growth"]) == "-0.46")
e["age2"], e["ed2"] = e["age"] ** 2, e["education"] ** 2
m_q = smf.ols("earnings ~ age + education + age2", data=e).fit()
e["yh_q"] = m_q.fittedvalues
reset_q_F, reset_q_p, _ = smf.ols("earnings ~ age + education + age2 + I(yh_q**2) + I(yh_q**3)", data=e).fit().compare_f_test(m_q)
p_both = smf.ols("earnings ~ age + education + age2 + ed2", data=e).fit().pvalues
p_age2 = smf.ols("earnings ~ age + education + age2", data=e).fit().pvalues["age2"]
p_ed2 = smf.ols("earnings ~ age + education + ed2", data=e).fit().pvalues["ed2"]
print(f"FACTS (default/iid SEs; HC1 p-values differ, same ordering) RESET with age2: F={reset_q_F:.2f} p={reset_q_p:.2e}; p(age2)={p_age2:.4f} p(ed2)={p_ed2:.2e}; joint model p={p_both[['age2', 'ed2']].round(6).to_dict()}")
check("CLAIM E29: RESET still rejects after adding age^2 (F = 22.4), so 'in age' would be unsupported",
      f1(reset_q_F) == "22.4" and reset_q_p < 0.001)
check("CLAIM E29: education^2 more significant than age^2 (default SEs; separately and jointly)", p_ed2 < p_age2 and p_both["ed2"] < p_both["age2"])

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
