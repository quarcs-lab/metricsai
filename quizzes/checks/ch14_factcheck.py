#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch14.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Run:  python3 quizzes/checks/ch14_factcheck.py      (exit 1 on any failure)

Notes
- AED_EARNINGS_COMPLETE stores earnings as float32 and gender/hours as int8; every column
  used is cast to float64 before estimation.
- pyfixest's wald_test() prints the Wald statistic (q x F), not F. The chapter prints 32.57
  for the joint test of the four gender terms in Model 5; the F-statistic is 32.57/4 = 8.14.
  The bank quotes only the p-value of that test (p < 0.001), which is unambiguous.
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

CHAPTER = "ch14"
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


def r0(x: float) -> int:
    return int(round(x))


def f2(x: float) -> str:
    return f"{x:.2f}"


def joint(fit, names: list[str]) -> tuple[float, float]:
    """F-statistic and p-value of H0: all listed coefficients are zero (fit's own vcov)."""
    idx = [list(fit.coef().index).index(v) for v in names]
    b = fit.coef().values[idx]
    V = fit._vcov[np.ix_(idx, idx)]
    q = len(idx)
    F = float(b @ np.linalg.solve(V, b)) / q
    return F, float(stats.f.sf(F, q, fit._N - len(fit.coef())))


# ---------------------------------------------------------------- 1. FACTS
d = load("AED_EARNINGS_COMPLETE.DTA")
VARS = ["earnings", "gender", "education", "genderbyeduc", "age", "genderbyage", "hours",
        "genderbyhours", "dself", "dprivate", "dgovt"]
for c in VARS:
    d[c] = d[c].astype(float)
n = len(d)
fem, mal = d[d.gender == 1], d[d.gender == 0]
yf, ym = fem.earnings, mal.earnings
SPECS = {
    "M1": "earnings ~ gender",
    "M2": "earnings ~ gender + education",
    "M3": "earnings ~ gender + education + genderbyeduc",
    "M4": "earnings ~ gender + education + genderbyeduc + age + hours",
    "M5": "earnings ~ gender + education + genderbyeduc + age + genderbyage + hours + genderbyhours",
}
rob = {k: pf.feols(s, data=d, vcov="HC1") for k, s in SPECS.items()}
dflt = {k: pf.feols(s, data=d) for k, s in SPECS.items()}
b1, b2, b3, b5 = rob["M1"].coef(), rob["M2"].coef(), rob["M3"].coef(), rob["M5"].coef()
welch = stats.ttest_ind(yf, ym, equal_var=False)
classic = stats.ttest_ind(yf, ym, equal_var=True)
welch_se = math.sqrt(yf.var() / len(yf) + ym.var() / len(ym))
F3, p3 = joint(rob["M3"], ["gender", "genderbyeduc"])
F5, p5 = joint(rob["M5"], ["gender", "genderbyeduc", "genderbyage", "genderbyhours"])
sep = {g: pf.feols("earnings ~ education + age + hours", data=d[d.gender == g], vcov="HC1") for g in (1, 0)}
w1 = pf.feols("earnings ~ dself + dgovt + education + age", data=d, vcov="HC1")
w2 = pf.feols("earnings ~ dself + dprivate + dgovt + education + age - 1", data=d, vcov="HC1")
w3 = pf.feols("earnings ~ dprivate + dgovt + education + age", data=d, vcov="HC1")
wtype = np.where(d.dself == 1, "self", np.where(d.dprivate == 1, "private", "govt"))
grp = d.groupby(wtype).earnings.agg(["mean", "median", "count"])
grp_x = d.groupby(wtype)[["education", "age"]].mean()
anova = stats.f_oneway(*(d.earnings[wtype == g] for g in ("self", "private", "govt")))
a_reg = pf.feols("earnings ~ dself + dgovt", data=d)
Fa, pa = joint(a_reg, ["dself", "dgovt"])
Fw1, pw1 = joint(w1, ["dself", "dgovt"])
Fw3, pw3 = joint(w3, ["dprivate", "dgovt"])

print(f"FACTS n={n}  women={len(fem)} men={len(mal)}  dtypes cast to float64")
print(f"FACTS means F={yf.mean():.2f} M={ym.mean():.2f} diff={yf.mean() - ym.mean():.2f}  sd F={yf.std():.2f} M={ym.std():.2f}")
print(f"FACTS medians F={yf.median():.0f} M={ym.median():.0f}; educ F={fem.education.mean():.3f} M={mal.education.mean():.3f}")
print(f"FACTS t classical={classic.statistic:.4f} welch={welch.statistic:.4f}  welch se={welch_se:.2f}")
for k in SPECS:
    print(f"FACTS {k}: R2={rob[k]._r2:.4f}")
    print(pd.DataFrame({"b": rob[k].coef(), "rse": rob[k].se(), "rt": rob[k].tstat(), "rp": rob[k].pvalue(),
                        "t_default": dflt[k].tstat()}).round(4).to_string())
print(f"FACTS joint M3 F={F3:.3f} p={p3:.2e}; joint M5 F={F5:.3f} p={p5:.2e} (pyfixest Wald = {4 * F5:.2f})")
for g, lab in ((1, "F"), (0, "M")):
    print(f"FACTS separate {lab}: N={sep[g]._N} " + str(sep[g].coef().round(2).to_dict()))
for nm, w in (("W1 base private", w1), ("W2 no intercept", w2), ("W3 base self", w3)):
    print(f"FACTS {nm}: R2={w._r2:.6f} " + str(w.coef().round(2).to_dict()) + " p=" + str(w.pvalue().round(4).to_dict()))
print(grp.round(2).to_string())
print(grp_x.round(3).to_string())
print(f"FACTS ANOVA F={anova.statistic:.4f} p={anova.pvalue:.5f}; regression F={Fa:.4f}; worker joint w/ controls F={Fw1:.4f} vs {Fw3:.4f}")
print()

# ---------------------------------------------------------------- 2. CHECKS (exam)
check("872 workers: 378 women, 494 men; worker types 79 / 663 / 130",
      n == 872 and (len(fem), len(mal)) == (378, 494)
      and (grp.loc["self", "count"], grp.loc["private", "count"], grp.loc["govt", "count"]) == (79, 663, 130))
check("E01: gender, dself, dgovt are 0/1; genderbyeduc = gender x education takes many values",
      all(set(d[v].unique()) == {0.0, 1.0} for v in ("gender", "dself", "dgovt"))
      and (d.genderbyeduc == d.gender * d.education).all() and d.genderbyeduc.nunique() > 2)
check("E02/E03: M1 intercept 63,476 = men's mean; gender coef -16,396 = difference in means",
      r0(b1["Intercept"]) == 63476 and r0(b1["gender"]) == -16396 and r0(ym.mean()) == 63476
      and abs(b1["gender"] - (yf.mean() - ym.mean())) < 1e-6)
check("E03: women's mean 47,080 = 63,476 - 16,396; recoded fit 47,080 + 16,396 male",
      r0(yf.mean()) == 47080 and 63476 - 16396 == 47080
      and r0(pf.feols("earnings ~ male", data=d.assign(male=1 - d.gender)).coef()["male"]) == 16396)
check("E04: M1 fitted values take exactly two distinct values",
      len(np.unique(np.round(dflt["M1"].predict(), 6))) == 2)
check("E06: default-SE t = -4.71 equals classical t-test; Welch and robust t both -5.10",
      f2(dflt["M1"].tstat()["gender"]) == "-4.71" and abs(classic.statistic - dflt["M1"].tstat()["gender"]) < 1e-8
      and f2(welch.statistic) == "-5.10" and f2(rob["M1"].tstat()["gender"]) == "-5.10")
check("E08: SDs 31,597 (women) and 61,713 (men)", (r0(yf.std()), r0(ym.std())) == (31597, 61713))
check("E08: Welch se from shown SDs = 3,217 (exact 3,217); robust regression se also 3,217",
      r0(math.sqrt(31597 ** 2 / 378 + 61713 ** 2 / 494)) == 3217 and r0(welch_se) == 3217
      and r0(rob["M1"].se()["gender"]) == 3217)
check("E08 feedback: variance terms 2,641,000 and 7,710,000 (nearest thousand)",
      round(31597 ** 2 / 378, -3) == 2641000 and round(61713 ** 2 / 494, -3) == 7710000)
check("E08 distractors: sum of SEs 4,402; no n 69,332; pooled-n 2,348",
      r0(31597 / math.sqrt(378) + 61713 / math.sqrt(494)) == 4402
      and r0(math.sqrt(31597 ** 2 + 61713 ** 2)) == 69332
      and r0(math.sqrt((31597 ** 2 + 61713 ** 2) / 872)) == 2348)
check("E09: M1 R2 = 0.025, gender p < 0.001 (robust and default)",
      f"{rob['M1']._r2:.3f}" == "0.025" and rob["M1"].pvalue()["gender"] < 0.001 and dflt["M1"].pvalue()["gender"] < 0.001)
check("E09 distractor: '2.5% less' is not the gap (gap = 25.8% of men's mean)",
      f"{16396 / 63476:.3f}" == "0.258")
check("E10/E11: M2 = -17,552 - 18,258 gender + 5,907 education",
      (r0(b2["Intercept"]), r0(b2["gender"]), r0(b2["education"])) == (-17552, -18258, 5907))
check("E11: M1 and M2 use the same 872 workers (no missing education)",
      rob["M1"]._N == rob["M2"]._N == 872 and d.education.isna().sum() == 0)
check("E11 explanation: education 14.0 (women) vs 13.7 (men)",
      (f"{fem.education.mean():.1f}", f"{mal.education.mean():.1f}") == ("14.0", "13.7"))
check("E13-E15: M3 = -31,451 + 20,219 gender + 6,921 educ - 2,765 gender x educ",
      (r0(b3["Intercept"]), r0(b3["gender"]), r0(b3["education"]), r0(b3["genderbyeduc"])) == (-31451, 20219, 6921, -2765))
check("E13 distractor: gap at mean education (~14 years) differs from 20,219",
      f"{d.education.mean():.0f}" == "14" and r0(b3["gender"] + b3["genderbyeduc"] * d.education.mean()) == -18084)
check("E14: women's slope 6,921 - 2,765 = 4,156 (= separate polyfit slope 4,156); distractor 9,686",
      6921 - 2765 == 4156 and 6921 + 2765 == 9686 and r0(np.polyfit(fem.education, fem.earnings, 1)[0]) == 4156)
check("E15: gap at 16 = 20,219 - 2,765 x 16 = -24,021; distractors 17,454, -44,240, 64,459",
      20219 - 2765 * 16 == -24021 and 20219 - 2765 == 17454 and -2765 * 16 == -44240 and 20219 + 2765 * 16 == 64459
      and abs(-24021 - (b3["gender"] + 16 * b3["genderbyeduc"])) < 5)
check("E15 explanation: gap crosses zero at about 7 years of education",
      f"{-b3['gender'] / b3['genderbyeduc']:.0f}" == "7")
check("E16: M3 gender t = 1.32, p = 0.19; r(gender, genderbyeduc) = 0.97; joint p < 0.001",
      f2(rob["M3"].tstat()["gender"]) == "1.32" and f2(rob["M3"].pvalue()["gender"]) == "0.19"
      and f2(d.gender.corr(d.genderbyeduc)) == "0.97" and p3 < 0.001)
check("E17: M5 robust p = 0.074, 0.053, 0.86, 0.094; joint p < 0.001",
      (f"{rob['M5'].pvalue()['gender']:.3f}", f"{rob['M5'].pvalue()['genderbyeduc']:.3f}",
       f2(rob["M5"].pvalue()["genderbyage"]), f"{rob['M5'].pvalue()['genderbyhours']:.3f}") == ("0.074", "0.053", "0.86", "0.094")
      and p5 < 0.001)
check("E17: none of the four individually significant at 5%",
      all(rob["M5"].pvalue()[v] > 0.05 for v in ("gender", "genderbyeduc", "genderbyage", "genderbyhours")))
check("E19: separate hours slopes 691 (F), 1,621 (M); age 500 (F), 549 (M); N 378 / 494",
      (r0(sep[1].coef()["hours"]), r0(sep[0].coef()["hours"]), r0(sep[1].coef()["age"]), r0(sep[0].coef()["age"])) == (691, 1621, 500, 549)
      and (sep[1]._N, sep[0]._N) == (378, 494))
check("E20: dself + dprivate + dgovt = 1 for all 872 workers", ((d.dself + d.dprivate + d.dgovt) == 1).all())
check("E22/E23: base private: -47,249 + 17,098 dself - 2,025 dgovt + 5,865 educ + 488 age",
      tuple(r0(w1.coef()[v]) for v in ("Intercept", "dself", "dgovt", "education", "age")) == (-47249, 17098, -2025, 5865, 488))
check("E23: base self dgovt = -2,025 - 17,098 = -19,123 (matches Approach 3); distractors 15,073, -17,098",
      -2025 - 17098 == -19123 and r0(w3.coef()["dgovt"]) == -19123 and 17098 - 2025 == 15073
      and r0(w3.coef()["dprivate"]) == -17098)
check("E24: no-intercept dself = -30,151 (negative, not a mean); self-employed mean 72,306",
      r0(w2.coef()["dself"]) == -30151 and r0(grp.loc["self", "mean"]) == 72306 and d.earnings.min() > 0)
check("E25/E26 support: identical R2 = 0.12 across the three parameterizations",
      abs(w1._r2 - w2._r2) < 1e-9 and abs(w1._r2 - w3._r2) < 1e-9 and f2(w1._r2) == "0.12")
check("E25: private is the largest group (663 of 872) and has the lowest mean earnings",
      grp["count"].idxmax() == "private" and grp["mean"].idxmin() == "private")
check("E25 distractor: lowest-mean base does not guarantee positive coefficients (dgovt < 0 with controls)",
      w1.coef()["dgovt"] < 0)
check("E26: joint worker-type F identical with private or self-employed as base", abs(Fw1 - Fw3) < 1e-8)
check("E27: means 72,306 / 54,521 / 56,105; dgovt = 1,584; distractor -16,201",
      (r0(grp.loc["self", "mean"]), r0(grp.loc["private", "mean"]), r0(grp.loc["govt", "mean"])) == (72306, 54521, 56105)
      and 56105 - 54521 == 1584 and r0(a_reg.coef()["dgovt"]) == 1584 and 56105 - 72306 == -16201)
check("E27 explanation: no-control dself = 17,785", r0(a_reg.coef()["dself"]) == 17785)
check("E28: ANOVA F = 4.24, p = 0.015 (rejects at 5%, not at 1%); equals default-SE regression joint F",
      f2(anova.statistic) == "4.24" and f"{anova.pvalue:.3f}" == "0.015" and 0.01 < anova.pvalue < 0.05
      and abs(Fa - anova.statistic) < 1e-8)
check("E29: Figure 14.2 slopes differ: men 6,921 vs women 4,156 per year",
      (r0(np.polyfit(mal.education, mal.earnings, 1)[0]), r0(np.polyfit(fem.education, fem.earnings, 1)[0])) == (6921, 4156))
check("E30: private mean 54,521 vs median 42,000; self 72,306 vs 45,000; govt 56,105 vs 50,000",
      (r0(grp.loc["private", "median"]), r0(grp.loc["self", "median"]), r0(grp.loc["govt", "median"])) == (42000, 45000, 50000))

check("E22 A (round 1): raw self-employed vs private gap is 17,785, not 17,098, so 'before controls' reading is false",
      r0(grp.loc["self", "mean"] - grp.loc["private", "mean"]) == 17785 and r0(w1.coef()["dself"]) != 17785)
check("E11 D (round 1): education 14.03 (women) vs 13.72 (men)",
      (f2(fem.education.mean()), f2(mal.education.mean())) == ("14.03", "13.72"))

check("E07 D (round 2): SEs differ: default t -4.71 vs Welch -5.10; robust se 3,217.43 vs Welch 3,217.25",
      f2(dflt["M1"].tstat()["gender"]) == "-4.71" and f2(welch.statistic) == "-5.10"
      and f2(rob["M1"].se()["gender"]) == "3217.43" and f2(welch_se) == "3217.25")

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic)
check("P02/P22-P24: y = 1 + 3d2 + 5d3 -> means 1, 4, 6; base d3: d1 = -5, d2 = -2; 3 - 5 = -2", (1, 1 + 3, 1 + 5) == (1, 4, 6) and 4 - 6 == -2 and 1 - 6 == -5)
check("P03: means 30 and 20 -> 20 + 10d", 30 - 20 == 10)
check("P08: sqrt(12^2/36 + 10^2/25) = 2.83; sum of SEs 4.00; no n 15.62; no sqrt 8.00",
      f2(math.sqrt(144 / 36 + 100 / 25)) == "2.83" and f2(12 / 6 + 10 / 5) == "4.00"
      and f2(math.sqrt(144 + 100)) == "15.62" and f2(144 / 36 + 100 / 25) == "8.00")
check("P13-P15: 10,000 + 5,000x - 8,000g - 2,000gx: woman no educ 2,000; women's slope 3,000; gap at 12 = -32,000",
      10000 - 8000 == 2000 and 5000 - 2000 == 3000 and -8000 - 2000 * 12 == -32000
      and -2000 * 12 == -24000 and -8000 - 2000 == -10000 and -8000 + 24000 == 16000 and 5000 + 2000 == 7000)
check("P17: p 0.21, 0.08, 0.12 > 0.05 (smallest 0.08); joint 0.004 < 0.01", min(0.21, 0.08, 0.12) == 0.08 > 0.05 and 0.004 < 0.01)
check("P19: 1.20 - 0.80 = 0.40", f2(1.20 - 0.80) == "0.40")
check("P27: 79 - 70 = 9; 79 - 74 = 5; charter 74 - 70 = 4", 79 - 70 == 9 and 79 - 74 == 5 and 74 - 70 == 4)

# ---------------------------------------------------------------- 3. CLAIMS (data relationships)
check("CLAIM E11: women average more education than men", fem.education.mean() > mal.education.mean())
check("CLAIM E11: education positively related to earnings (Model 2 coefficient > 0, significant)",
      b2["education"] > 0 and rob["M2"].pvalue()["education"] < 0.001)
check("CLAIM E11: adding education widens the gap (|M2| > |M1|)", abs(b2["gender"]) > abs(b1["gender"]))
check("CLAIM E13: almost no worker has zero education (9 of 872)", int((d.education == 0).sum()) == 9)
check("CLAIM E16: gender and genderbyeduc nearly collinear (r > 0.95)", d.gender.corr(d.genderbyeduc) > 0.95)
check("CLAIM E17/KC: M5 gender coefficients reproduce the separate regressions exactly",
      abs(b5["Intercept"] - sep[0].coef()["Intercept"]) < 1e-4
      and abs(b5["Intercept"] + b5["gender"] - sep[1].coef()["Intercept"]) < 1e-4
      and abs(b5["education"] + b5["genderbyeduc"] - sep[1].coef()["education"]) < 1e-4)
check("CLAIM E19: men's hours slope is more than twice women's", sep[0].coef()["hours"] > 2 * sep[1].coef()["hours"])
check("CLAIM E30: mean > median for every worker type and for both genders",
      all(grp["mean"] > grp["median"]) and yf.mean() > yf.median() and ym.mean() > ym.median())
check("CLAIM E09: 872 workers but R2 tiny: within-group spread dominates (SD men 61,713 vs gap 16,396)",
      ym.std() > 3 * abs(b1["gender"]))

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
