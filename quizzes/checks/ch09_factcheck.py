#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch09.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Run:  python3 quizzes/checks/ch09_factcheck.py      (exit 1 on any failure)
"""

import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf
from scipy import stats

CHAPTER = "ch09"
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


def pct_exact(dln: float) -> float:
    """Exact % change implied by a log change: 100 (e^dln - 1)."""
    return 100 * (math.exp(dln) - 1)


# ---------------------------------------------------------------- 1. FACTS
d = load("AED_EARNINGS.DTA")
d["lnearn"] = np.log(d["earnings"])
d["lneduc"] = np.log(d["education"])
m1 = pf.feols("earnings ~ education", data=d)
m2 = pf.feols("lnearn ~ education", data=d)
m3 = pf.feols("lnearn ~ lneduc", data=d)
m4 = pf.feols("earnings ~ lneduc", data=d)
a1, b1 = m1.coef()["Intercept"], m1.coef()["education"]
a2, b2 = m2.coef()["Intercept"], m2.coef()["education"]
a3, b3 = m3.coef()["Intercept"], m3.coef()["lneduc"]
a4, b4 = m4.coef()["Intercept"], m4.coef()["lneduc"]
r2 = {k: m._r2 for k, m in zip(("lin", "loglin", "loglog", "linlog"), (m1, m2, m3, m4))}

sp = load("AED_SP500INDEX.DTA")
ms = pf.feols("lnsp500 ~ year", data=sp)
asp, bsp = ms.coef()["Intercept"], ms.coef()["year"]

print(f"FACTS earnings: n={len(d)} mean={d.earnings.mean():.2f} median={d.earnings.median():.0f} "
      f"min={d.earnings.min():.0f} max={d.earnings.max():.0f} skew(pop)={stats.skew(d.earnings):.3f} "
      f"skew(ln)={stats.skew(d.lnearn):.3f}")
print(f"FACTS education: mean={d.education.mean():.4f} min={d.education.min()} max={d.education.max()} age unique={d.age.unique()}")
print(f"FACTS M1 linear:     a={a1:.4f} b={b1:.4f} se={m1.se()['education']:.4f} t={m1.tstat()['education']:.4f} R2={r2['lin']:.6f}")
print(f"FACTS M2 log-linear: a={a2:.6f} b={b2:.6f} se={m2.se()['education']:.6f} t={m2.tstat()['education']:.4f} "
      f"p={m2.pvalue()['education']:.3g} R2={r2['loglin']:.6f} exact%={pct_exact(b2):.4f}")
print(f"FACTS M3 log-log:    a={a3:.6f} b={b3:.6f} se={m3.se()['lneduc']:.6f} t={m3.tstat()['lneduc']:.4f} R2={r2['loglog']:.6f}")
print(f"FACTS M4 linear-log: a={a4:.4f} b={b4:.4f} b/100={b4 / 100:.4f} R2={r2['linlog']:.6f}")
print(f"FACTS S&P: n={len(sp)} years={sp.year.min():.0f}-{sp.year.max():.0f} first={sp.sp500.iloc[0]:.4f} last={sp.sp500.iloc[-1]:.4f} "
      f"a={asp:.4f} b={bsp:.6f} R2={ms._r2:.4f} exact r={100 * (math.exp(bsp) - 1):.4f}% rule72={72 / (100 * bsp):.2f}")
print()

# ---------------------------------------------------------------- 2. CHECKS (exam)
check("data coverage: 171 workers, all aged 30", len(d) == 171 and set(d.age.unique()) == {30})
check("E01: S&P 1927 = 17.66, 2019 = 3,230.78; 93 annual obs 1927-2019",
      f2(sp.sp500.iloc[0]) == "17.66" and f2(sp.sp500.iloc[-1]) == "3230.78" and len(sp) == 93
      and (int(sp.year.min()), int(sp.year.max())) == (1927, 2019) and (sp.year.diff().dropna() == 1).all())
check("E01 expl: ln(3230.78/17.66) = 5.21; proportionate change = 182",
      f2(math.log(3230.78 / 17.66)) == "5.21" and round((3230.78 - 17.66) / 17.66) == 182)
check("E01: lnsp500 is the natural log of sp500", np.allclose(sp.lnsp500, np.log(sp.sp500), atol=1e-5))
check("E02 expl: ln(1)=0, ln(e)=1, power rule, exp(ln x)=x; ln(a+b) != ln a + ln b",
      math.log(1) == 0 and math.isclose(math.log(math.e), 1) and math.isclose(math.log(3 ** 4), 4 * math.log(3))
      and math.isclose(math.exp(math.log(7.3)), 7.3) and not math.isclose(math.log(2 + 5), math.log(2) + math.log(5)))
check("E03: ln(0.5) = -0.693 < 0; ln(2) = 0.693", f"{math.log(0.5):.3f}" == "-0.693" and f"{math.log(2):.3f}" == "0.693")
check("E04: 100 ln(1.5) = 40.5; 100(e^0.5 - 1) = 64.9; ln(1.5) = 0.41",
      (f1(100 * math.log(60000 / 40000)), f1(pct_exact(0.5)), f2(math.log(1.5))) == ("40.5", "64.9", "0.41"))
check("E07: log-linear a = 8.561, b = 0.1314", (f"{a2:.3f}", f"{b2:.4f}") == ("8.561", "0.1314"))
check("E07: 100 b = 13.1; b = 0.13", f1(100 * b2) == "13.1" and f2(b2) == "0.13")
check("E08: 100(e^0.1314 - 1) = 14.0; distractors 1.14 (e^b), 113.0 (100e^b - 1), 0.14 (e^b - 1)",
      (f1(pct_exact(0.1314)), f2(math.exp(0.1314)), f1(100 * math.exp(0.1314) - 1), f2(math.exp(0.1314) - 1))
      == ("14.0", "1.14", "113.0", "0.14"))
check("E08: exact from exact b also 14.0", f1(pct_exact(b2)) == "14.0")
check("E09 expl: 13.1% of 30,000 ~ 3,900; of 100,000 = 13,100",
      round(0.131 * 30000, -2) == 3900 and round(0.131 * 100000) == 13100)
check("E10: se = 0.0143, t = 9.21, p < 0.001",
      f"{m2.se()['education']:.4f}" == "0.0143" and f2(m2.tstat()["education"]) == "9.21" and m2.pvalue()["education"] < 0.001)
check("E10 distractor/expl: 9.21 ~ 92%; 0.1314/0.0143 = 9.19 ~ 9.21 (rounded se); R2 = 0.334",
      round(9.21 * 10) == 92 and abs(0.1314 / 0.0143 - 9.21) < 0.05 and f"{r2['loglin']:.3f}" == "0.334")
check("E11: log-log a = 6.545, b = 1.478 (~1.48); 148", (f"{a3:.3f}", f"{b3:.3f}", f2(b3), round(100 * b3)) == ("6.545", "1.478", "1.48", 148))
check("E12: max education 20; 1% of 20 = 0.2; 10% = 2; mean education 14.4, 1% = 0.14",
      d.education.max() == 20 and f1(0.01 * 20) == "0.2" and f1(0.1 * 20) == "2.0"
      and f1(d.education.mean()) == "14.4" and f2(0.01 * d.education.mean()) == "0.14")
check("E13: 147.8/12 = 12.3, 147.8/18 = 8.2; 1/12 = 8.3%, 1/18 = 5.6%",
      (f1(147.8 / 12), f1(147.8 / 18), f1(100 / 12), f1(100 / 18)) == ("12.3", "8.2", "8.3", "5.6"))
check("E13 distractors: 1.478 x 12 = 17.7, x 18 = 26.6; 1.478 ~ 1.5",
      (f1(1.478 * 12), f1(1.478 * 18), f1(1.478)) == ("17.7", "26.6", "1.5"))
check("E13: exact-b version also 12.3 / 8.2", (f1(100 * b3 / 12), f1(100 * b3 / 18)) == ("12.3", "8.2"))
d64 = d.assign(le64=np.log(d.education.astype(float)), lm64=np.log(12 * d.education.astype(float)))
m3y = pf.feols("lnearn ~ le64", data=d64)
m3m = pf.feols("lnearn ~ lm64", data=d64)
check("E14: education in months leaves the log-log slope unchanged and shifts the intercept by -b ln(12) (float64)",
      math.isclose(m3m.coef()["lm64"], m3y.coef()["le64"], rel_tol=1e-9)
      and math.isclose(m3m.coef()["Intercept"], m3y.coef()["Intercept"] - m3y.coef()["le64"] * math.log(12), rel_tol=1e-9))
# Precision note: the chapter's np.log(education) runs on an int8 column and returns float16, so its
# log-log and linear-log numbers carry float16 rounding. The bank quotes the chapter's printed values
# (b = 1.478, a = 6.545; 54,433 and -102,718); with float64 logs they are 1.478, 6.543; 54,452, -102,767.
m4y = pf.feols("earnings ~ le64", data=d64)
print(f"FACTS float64 logs: log-log a={m3y.coef()['Intercept']:.4f} b={m3y.coef()['le64']:.5f} R2={m3y._r2:.4f}; "
      f"linear-log a={m4y.coef()['Intercept']:.2f} b={m4y.coef()['le64']:.2f} R2={m4y._r2:.4f}")
check("precision note: chapter ln(education) is float16; float64 log-log slope still rounds to 1.478 and R2 to 0.286",
      np.log(d.education).dtype == np.float16 and f"{m3y.coef()['le64']:.3f}" == "1.478" and f"{m3y._r2:.3f}" == "0.286")
check("E15: linear-log a = -102,718, b = 54,433; /100 = 544; /10 = 5,443; /10,000 = 5.44",
      (round(a4), round(b4), round(54433 / 100), round(54433 / 10), f2(54433 / 10000)) == (-102718, 54433, 544, 5443, "5.44"))
check("E16 distractor / E17: linear a = -31,056, b = 5,021", (round(a1), round(b1)) == (-31056, 5021))
check("E16: linear-log dollar gain of one more year falls with education (exact model)",
      all(b4 * (math.log(e + 1) - math.log(e)) > b4 * (math.log(e + 2) - math.log(e + 1)) for e in range(3, 20)))
check("E17: 5,021 x 6 = 30,126; pred(18) = 59,322; 18 x 5,021 = 90,378",
      (5021 * 6, -31056 + 5021 * 18, 5021 * 18) == (30126, 59322, 90378))
check("E18: R2 = 0.289, 0.334, 0.286, 0.231",
      tuple(f"{r2[k]:.3f}" for k in ("lin", "loglin", "loglog", "linlog")) == ("0.289", "0.334", "0.286", "0.231"))
check("E18 expl: log-linear > log-log; linear > linear-log", r2["loglin"] > r2["loglog"] and r2["lin"] > r2["linlog"])
check("E19: mean 41,413 > median 36,000; min 1,050 > 0; linear t = 8.30",
      round(d.earnings.mean()) == 41413 and d.earnings.median() == 36000 and d.earnings.min() == 1050
      and f2(m1.tstat()["education"]) == "8.30")
check("E20 expl: education ranges 3 to 20 (no zeros)", (d.education.min(), d.education.max()) == (3, 20))
check("E22: S&P a = -124.09, b = 0.0653 (~6.5%, 0.065)",
      (f2(asp), f"{bsp:.4f}", f1(100 * bsp), f"{bsp:.3f}") == ("-124.09", "0.0653", "6.5", "0.065"))
check("E23 expl: R2 of ln(sp500) on year = 0.958", f"{ms._r2:.3f}" == "0.958")
check("E24: 72/2.4 = 30; 72/0.024 = 3,000; 72 x 2.4 = 173; 100/2.4 = 42",
      (round(72 / 2.4), round(72 / 0.024), round(72 * 2.4), round(100 / 2.4)) == (30, 3000, 173, 42))
check("E25: 72/3 = 24", 72 / 3 == 24)

check("E08 (rev): 2 x 0.1314 = 0.2628; exact 30.1; approx 26.3; 2 x 14.0 = 28.0; e^0.2628 = 1.30",
      (f"{2 * 0.1314:.4f}", f1(pct_exact(0.2628)), f1(100 * 0.2628), f1(2 * 14.0), f2(math.exp(0.2628)), f"{math.exp(0.2628) - 1:.3f}")
      == ("0.2628", "30.1", "26.3", "28.0", "1.30", "0.301"))
pred_ll = np.exp(a2 + b2 * d.education.astype(float))
check("E09 (rev): $30,000 and $60,000 lie within the log-linear predicted range; 13.1% of 60,000 ~ 7,900",
      pred_ll.min() < 30000 and pred_ll.max() > 60000 and round(0.131 * 60000, -2) == 7900)
print(f"FACTS log-linear predicted earnings range: {pred_ll.min():.0f} to {pred_ll.max():.0f}")
check("E16 feedback: ln13 - ln12 = 0.080; ln19 - ln18 = 0.054",
      (f"{math.log(13) - math.log(12):.3f}", f"{math.log(19) - math.log(18):.3f}") == ("0.080", "0.054"))
check("E18 C (rev): log-log 0.286 > linear-log 0.231 (different dependent variables)", r2["loglog"] > r2["linlog"])
check("E07 (rev): AED_EARNINGS is all women (gender 0; AED_EARNINGSMALE is gender 1)",
      set(d.gender.unique()) == {0} and set(load("AED_EARNINGSMALE.DTA").gender.unique()) == {1})

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic)
check("P01: ln2 = 0.693, ln5 = 1.609, ln10 = 2.30; ln2 x ln5 = 1.12",
      (f"{math.log(2):.3f}", f"{math.log(5):.3f}", f2(math.log(10)), f2(math.log(2) * math.log(5))) == ("0.693", "1.609", "2.30", "1.12"))
check("P02: ln(5) = 1.61, ln(10) - ln(5) = 0.69", (f2(math.log(5)), f2(math.log(10) - math.log(5))) == ("1.61", "0.69"))
check("P04: 100 ln1.1 = 9.53 (~9.5); ln1.1 = 0.0953 (~0.095%); 100(e^0.1 - 1) = 10.5",
      (f2(100 * math.log(1.1)), f"{math.log(1.1):.4f}", f"{math.log(1.1):.3f}", f1(pct_exact(0.1))) == ("9.53", "0.0953", "0.095", "10.5"))
check("P06: 10 x 0.6 = 6", 10 * 0.6 == 6)
check("P08: 5 x 0.085 = 0.425; exact 53.0; e^0.425 - 1 = 0.53; 100 e^0.425 = 153.0",
      (f"{5 * 0.085:.3f}", f1(pct_exact(0.425)), f2(math.exp(0.425) - 1), f1(100 * math.exp(0.425)), f1(100 * 0.425))
      == ("0.425", "53.0", "0.53", "153.0", "42.5"))
check("P09: 8.5% of $40 = 3.40, of $20 = 1.70", (f2(0.085 * 40), f2(0.085 * 20)) == ("3.40", "1.70"))
check("P12: 1% of 250 = 2.5; 10% = 25; 0.1% = 0.25", (0.01 * 250, 0.1 * 250, 0.001 * 250) == (2.5, 25.0, 0.25))
check("P13: 1/25 = 4%, 1/50 = 2%; x0.5 = 2%, 1%; 0.5 x 25 = 12.5, 0.5 x 50 = 25",
      (100 / 25, 100 / 50, 0.5 * 100 / 25, 0.5 * 100 / 50, 0.5 * 25, 0.5 * 50) == (4, 2, 2, 1, 12.5, 25))
check("P14: 0.085/12 = 0.0071", f"{0.085 / 12:.4f}" == "0.0071")
check("P15/P16: 3,000/100 = 30; /10 = 300; 1% rise adds ln(1.01) ~ 0.01 at any income", (3000 / 100, 3000 / 10) == (30, 300) and f2(math.log(1.01)) == "0.01")
check("P17: 4 + 1.5 x 16 = 28; 1.5 x 16 = 24; 4 + 1.5 = 5.5; 4 x 16 = 64",
      (4 + 1.5 * 16, 1.5 * 16, 4 + 1.5, 4 * 16) == (28, 24, 5.5, 64))
check("P22: 0.021 -> 2.1%; x1000 = 21", (f1(100 * 0.021), round(1000 * 0.021)) == ("2.1", 21))
check("P23: ln(1.03) ~ 0.03", f2(math.log(1.03)) == "0.03")
check("P24: 72/24 = 3; 24/72 = 0.3; 100/24 = 4.2", (72 / 24, f1(24 / 72), f1(100 / 24)) == (3, "0.3", "4.2"))
check("P25: 72/2 = 36, 72/4 = 18 (ratio 2, not 4)", (72 / 2, 72 / 4, (72 / 2) / (72 / 4)) == (36, 18, 2))

# ---------------------------------------------------------------- 3. CLAIMS
check("CLAIM E04/P04: log approximation understates the exact % change for increases",
      100 * math.log(1.5) < 50 and 100 * math.log(1.1) < 10)
check("CLAIM E08: exact % change (14.0) exceeds the 13.1 approximation", pct_exact(b2) > 100 * b2)
check("CLAIM E19: earnings right-skewed (mean > median, skew > 0)", d.earnings.mean() > d.earnings.median() and stats.skew(d.earnings) > 0)
check("CLAIM E19: every worker has positive earnings", (d.earnings > 0).all())
check("CLAIM E22: S&P slope positive, index positive throughout", bsp > 0 and (sp.sp500 > 0).all())
check("CLAIM E23: levels path curves upward (log fit R2 0.958 >> linear-in-year fit of the level)",
      ms._r2 > pf.feols("sp500 ~ year", data=sp)._r2)
check("CLAIM E10: positive association education-earnings (both log-linear and linear slopes > 0)", b2 > 0 and b1 > 0)
check("CLAIM E13: log-log implied % return per extra year falls with education", 100 * b3 / 12 > 100 * b3 / 18)

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
