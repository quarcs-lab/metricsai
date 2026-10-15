#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch02.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Run:  python3 quizzes/checks/ch02_factcheck.py      (exit 1 on any failure)
"""

import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

CHAPTER = "ch02"
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


# ---------------------------------------------------------------- 1. FACTS
x = load("AED_EARNINGS.DTA")["earnings"]
n, mean, med, sd = len(x), x.mean(), x.median(), x.std()
q1, q3 = x.quantile(0.25), x.quantile(0.75)
iqr = q3 - q1
skew, exk, rawk = stats.skew(x), stats.kurtosis(x), stats.kurtosis(x, fisher=False)
fence = q3 + 1.5 * iqr
lnx = np.log(x)
within1 = ((x >= mean - sd) & (x <= mean + sd)).mean()

gdp = load("AED_REALGDPPC.DTA")
r = gdp["realgdppc"]
yearly = gdp.groupby("year")["realgdppc"].mean()

health = load("AED_HEALTHCATEGORIES.DTA")
exp_by = dict(zip(health["category"], health["expenditures"]))
total_h = health["expenditures"].sum()

fish = load("AED_FISHING.DTA")["mode"].value_counts()

hs = load("AED_MONTHLYHOMESALES.DTA")
hs = hs[hs["year"] >= 2005]
by_month = hs.groupby(pd.to_datetime(hs["month"]).dt.month)["exsales"].mean()

print(f"FACTS earnings: n={n} mean={mean:.2f} median={med} sd={sd:.2f} q1={q1} q3={q3} iqr={iqr} "
      f"skew={skew:.4f} exkurt={exk:.4f} raw={rawk:.4f} fence={fence} within1sd={within1:.4f} "
      f"ln skew={stats.skew(lnx):.4f}")
print(f"FACTS gdp: first={r.iloc[0]:.1f} last={r.iloc[-1]:.1f}; health total={total_h}; fishing={fish.to_dict()}")
print(f"FACTS home sales mean by month: {by_month.round(0).to_dict()}\n")

# ---------------------------------------------------------------- 2. CHECKS (exam)
check("n = 171", n == 171)
check("mean $41,413", round(mean) == 41413)
check("median $36,000", med == 36000)
check("SD $25,527", round(sd) == 25527)
check("SD ~$25,500 (rounded to hundreds)", round(sd, -2) == 25500)
check("SD = 62% of mean", round(100 * sd / mean) == 62)
check("Q1 $25,000, Q3 $49,000, IQR $24,000", (q1, q3, iqr) == (25000, 49000, 24000))
check("distractor: Q1 + Q3 = $74,000; IQR/2 = $12,000", (q1 + q3, iqr / 2) == (74000, 12000))
check("max $172,000, min $1,050", (x.max(), x.min()) == (172000, 1050))
check("86th value is the median of 171", (n + 1) / 2 == 86)
check("89 women earn <= $36,000", (x <= 36000).sum() == 89)
check("replace max by $500,000: mean rises ~$1,918", round((500000 - 172000) / n) == 1918)
check("band mean +/- 1 SD = $15,886 to $66,940", (round(mean - sd), round(mean + sd)) == (15886, 66940))
check("band holds ~75% of women", round(100 * within1) == 75)
check("skewness 1.71", f"{skew:.2f}" == "1.71")
check("excess kurtosis 4.32, raw 7.32", (f"{exk:.2f}", f"{rawk:.2f}") == ("4.32", "7.32"))
check("upper fence Q3 + 1.5 IQR = $85,000 (1.5 x 24,000 = 36,000)", fence == 85000 and 1.5 * iqr == 36000)
check("7 earnings above the fence", (x > fence).sum() == 7)
check("log-earnings skewness -0.91", f"{stats.skew(lnx):.2f}" == "-0.91")
check("e^10 = $22,026, e^11 = $59,874", (round(math.exp(10)), round(math.exp(11))) == (22026, 59874))
check("59,874 / 22,026 ~ 2.718; difference $37,848", f"{59874 / 22026:.3f}" == "2.718" and 59874 - 22026 == 37848)
check("e - 1 ~ 172%", round(100 * (math.e - 1)) == 172)
check("z(max) ~ 5.1", f"{(172000 - mean) / sd:.1f}" == "5.1")
check("distractors: 172,000/SD ~6.7, 172,000/mean ~4.2, SD/172,000 ~0.15",
      (f"{172000 / sd:.1f}", f"{172000 / mean:.1f}", f"{sd / 172000:.2f}") == ("6.7", "4.2", "0.15"))
check("health total $3,653B, 13 categories", total_h == 3653 and len(health) == 13)
check("hospital $1,192B = 32.6% (~33%)", exp_by["Hospital"] == 1192 and f"{100 * 1192 / total_h:.1f}" == "32.6")
check("fishing 1,182: charter 452, private 418, pier 178, beach 134",
      (fish.sum(), fish["charter"], fish["private"], fish["pier"], fish["beach"]) == (1182, 452, 418, 178, 134))
check("boat share 870/1,182 = 73.6% (~74%); charter 38.2%; shore 26.4%",
      (452 + 418, f"{100 * 870 / 1182:.1f}", f"{100 * 452 / 1182:.1f}", f"{100 * 312 / 1182:.1f}") == (870, "73.6", "38.2", "26.4"))
check("real GDP pc ~$17,700 early 1959, ~$57,600 end 2020", (round(r.iloc[0], -2), round(r.iloc[-1], -2)) == (17700, 57600))

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic)
s5 = pd.Series([5, 2, 2, 8, 3])
check("P: {5,2,2,8,3} mean 4, median 3, mode 2", (s5.mean(), s5.median(), s5.mode()[0]) == (4, 3, 2))
check("P: IQR 60 - 25 = 35; 35-25 = 10; 60-35 = 25; 25+60 = 85", (60 - 25, 35 - 25, 60 - 35, 25 + 60) == (35, 10, 25, 85))
check("P: normal, P(-2 < Z < -1) ~ 13-14%", 13 <= 100 * (stats.norm.cdf(-1) - stats.norm.cdf(-2)) <= 14)
check("P: roads 25/100 = 25%; 25/40 = 62.5%", (25 / 100, 100 * 25 / 40) == (0.25, 62.5))
check("P: transit 60/200 = 30%; 60/150 = 40%", (60 / 200, 60 / 150) == (0.30, 0.40))
check("P: e^0.5 ~ 1.65 -> ~65%; e^0.05 - 1 ~ 5.1%", (f"{math.exp(0.5):.2f}", round(100 * (math.exp(0.5) - 1)), f"{100 * (math.exp(0.05) - 1):.1f}") == ("1.65", 65, "5.1"))
check("P: z = (130-100)/15 = 2.0; 130/15 ~ 8.7; 130/100 = 1.3", ((130 - 100) / 15, f"{130 / 15:.1f}", 130 / 100) == (2.0, "8.7", 1.3))

# ---------------------------------------------------------------- 3. CLAIMS
check("right-skewed: mean > median", mean > med)
check("fewer than half earn more than the mean (61 of 171)", (x > mean).sum() == 61)
check("~65% of earnings in $15k-$45k (chapter prose)", round(100 * ((x >= 15000) & (x <= 45000)).mean()) == 65)
check("hospital > physician + drugs combined", exp_by["Hospital"] > exp_by["Physician and clinical"] + exp_by["Drugs & Supplies"])
check("home sales peak in late spring/summer (top 3 months within May-Aug), trough in Jan-Feb (2005-2015 monthly means)",
      set(by_month.nlargest(3).index) <= {5, 6, 7, 8} and set(by_month.nsmallest(2).index) <= {1, 2, 11, 12})
check("recession dips: 2009 < 2007 and 2020 < 2019 (real GDP pc)", yearly[2009] < yearly[2007] and yearly[2020] < yearly[2019])
check("nominal GDP pc < real before 2012, > real after 2012",
      (gdp[gdp.year < 2012]["gdppc"] < gdp[gdp.year < 2012]["realgdppc"]).all()
      and (gdp[gdp.year > 2012]["gdppc"] > gdp[gdp.year > 2012]["realgdppc"]).all())

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
