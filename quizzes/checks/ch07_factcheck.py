#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch07.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Run:  python3 quizzes/checks/ch07_factcheck.py      (exit 1 on any failure)
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

CHAPTER = "ch07"
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


def f2(x: float) -> str:
    return f"{x:.2f}"


# ---------------------------------------------------------------- 1. FACTS
d = load("AED_HOUSE.DTA")
n = len(d)
df = n - 2
m = pf.feols("price ~ size", data=d)
rb = pf.feols("price ~ size", data=d, vcov="HC1")
b1, b2 = m.coef()["Intercept"], m.coef()["size"]
se1, se2 = m.se()["Intercept"], m.se()["size"]
t2, p2 = m.tstat()["size"], m.pvalue()["size"]
p1 = m.pvalue()["Intercept"]
ci = m.confint().loc["size"].values
rse1, rse2 = rb.se()["Intercept"], rb.se()["size"]
rci = rb.confint().loc["size"].values
resid = d["price"] - m.predict()
s_e = math.sqrt((resid ** 2).sum() / df)
sx = d["size"].std()
c95, c90, c99 = stats.t.ppf(0.975, df), stats.t.ppf(0.95, df), stats.t.ppf(0.995, df)

mb = pf.feols("price ~ bedrooms", data=d)
bb, sb, tb, pb = mb.coef()["bedrooms"], mb.se()["bedrooms"], mb.tstat()["bedrooms"], mb.pvalue()["bedrooms"]

art = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [1, 2, 2, 2, 3]})
ma = pf.feols("y ~ x", data=art)
ba, sa = ma.coef()["x"], ma.se()["x"]
ca = stats.t.ppf(0.975, 3)
cia = ma.confint().loc["x"].values


def t_null(c: float) -> float:
    return (b2 - c) / se2


print(f"FACTS house: n={n} df={df} b1={b1:.4f} se1={se1:.4f} b2={b2:.6f} se2={se2:.6f} t2={t2:.4f} p2={p2:.3g} p1={p1:.3g} "
      f"CI95=[{ci[0]:.4f}, {ci[1]:.4f}] R2={m._r2:.4f}")
print(f"FACTS crit: t27 .975={c95:.4f} .95={c90:.4f} .995={c99:.4f}; s_e={s_e:.2f} sd(size)={sx:.2f} "
      f"size range={d['size'].min()}-{d['size'].max()} mean price={d['price'].mean():.2f}")
print(f"FACTS robust HC1: se1={rse1:.2f} se2={rse2:.4f} t={rb.tstat()['size']:.4f} CI=[{rci[0]:.4f}, {rci[1]:.4f}]")
print(f"FACTS bedrooms: b={bb:.2f} se={sb:.2f} t={tb:.4f} p={pb:.4f}")
print(f"FACTS artificial: b={ba:.4f} se={sa:.4f} crit3={ca:.4f} CI=[{cia[0]:.4f}, {cia[1]:.4f}]")
for c in (45, 52, 75, 80, 90, 95, 99, 100):
    t = t_null(c)
    print(f"FACTS null {c}: t={t:.4f} p2={2 * stats.t.sf(abs(t), df):.4f} p_lower={stats.t.cdf(t, df):.4f} p_upper={stats.t.sf(t, df):.4f}")
print()

# ---------------------------------------------------------------- 2. CHECKS (exam)
check("n = 29 houses, 27 df", n == 29 and df == 27)
check("b2 = 73.77, se = 11.17", (f2(b2), f2(se2)) == ("73.77", "11.17"))
check("95% CI [50.84, 96.70]", (f2(ci[0]), f2(ci[1])) == ("50.84", "96.70"))
check("t crit 27 df: 2.052 (5%), 1.703 (10%/one-sided 5%), 2.771 (1%)",
      (f"{c95:.3f}", f"{c90:.3f}", f"{c99:.3f}") == ("2.052", "1.703", "2.771"))
check("E05: t-based margin ~5% wider than normal-based", round(100 * (c95 / 1.96 - 1)) == 5)
check("E05 explanation: 1.96 x se = 21.90, crit x se = 22.93 (exact)", (f2(1.96 * se2), f2(c95 * se2)) == ("21.90", "22.93"))
check("E06: 116 = 4 x 29 houses", 116 == 4 * 29)
check("E07: s_e ~ 23,551, sd(size) ~ 398", round(s_e) == 23551 and round(sx) == 398)
check("E07: 796 = 2 x 398, chapter sd(size) (n-1 convention) rounds to 398", 796 == 2 * 398 and round(sx) == 398 and round(d["size"].std(ddof=1)) == 398)
check("E07: 23,551/(sqrt29 x 796) = 5.5; sqrt29 x 796 = 4,287", f"{23551 / (math.sqrt(29) * 796):.1f}" == "5.5" and round(math.sqrt(29) * 796) == 4287)
check("E07 distractors: 23,551/796 = 29.6 (no sqrt n); 23,551/(29 x 796) = 1.0 (n); 23,551/(sqrt29 x 199) = 22.0 (spread reversed)",
      (f"{23551 / 796:.1f}", f"{23551 / (29 * 796):.1f}", f"{23551 / (math.sqrt(29) * 398 / 2):.1f}") == ("29.6", "1.0", "22.0"))
check("E07: doubling sd(x) halves se (shortcut)", abs((23551 / (math.sqrt(29) * 796)) * 2 - 23551 / (math.sqrt(29) * 398)) < 1e-9)
check("E07 explanation: exact se uses sqrt(n-1): s_e/(sd*sqrt(28)) = 11.17", f2(s_e / (sx * math.sqrt(n - 1))) == "11.17")
check("E08: 1.703 x 11.17 = 19.02 -> [54.75, 92.79]",
      f2(1.703 * 11.17) == "19.02" and (f2(73.77 - 19.02), f2(73.77 + 19.02)) == ("54.75", "92.79"))
check("E08 distractors: 73.77 +/- 1.703 = [72.07, 75.47]; +/- 9.51 = [64.26, 83.28]",
      (f2(73.77 - 1.703), f2(73.77 + 1.703), f2(73.77 - 19.02 / 2), f2(73.77 + 19.02 / 2)) == ("72.07", "75.47", "64.26", "83.28"))
check("E08 distractor: 73.77 +/- 11.17 = [62.60, 84.94]", (f2(73.77 - 11.17), f2(73.77 + 11.17)) == ("62.60", "84.94"))
check("E09: 5 of 100 intervals expected to miss at 95%", round(100 * (1 - 0.95)) == 5)
check("E20: t = 0.06/0.02 = 3.0 > 1% critical ~2.58 (large n)", f"{0.06 / 0.02:.1f}" == "3.0" and f2(stats.norm.ppf(0.995)) == "2.58" and 0.06 / 0.02 > stats.t.ppf(0.995, 100000 - 2))
check("E28 B false: robust t 6.51 < classical t 6.60", rb.tstat()["size"] < t2 and (f2(rb.tstat()["size"]), f2(t2)) == ("6.51", "6.60"))
check("E11: rounded 2.052 x 11.17 = 22.92, so the bank cites 22.93 only as the half-width / exact se", f2(2.052 * 11.17) == "22.92")
check("E11: half-width (96.70-50.84)/2 = 22.93; width 45.86", (f2((96.70 - 50.84) / 2), f2(96.70 - 50.84)) == ("22.93", "45.86"))
check("E12: Davis width ~46, other town width 140, other town CI excludes 0", round(96.70 - 50.84) == 46 and 145 - 5 == 140 and 5 > 0)
check("E13: artificial slope 0.40, se 0.115, crit 3.182, CI [0.03, 0.77], margin 0.37",
      (f2(ba), f"{sa:.3f}", f"{ca:.3f}", f2(cia[0]), f2(cia[1]), f2(ca * sa)) == ("0.40", "0.115", "3.182", "0.03", "0.77", "0.37"))
check("E13: artificial slope significant at 5% (t > 3.182)", ba / sa > ca)
check("E14/E18: slope p < 0.001", p2 < 0.001)
check("E15: bedrooms slope 23,667, se 9,638, t 2.46, p ~0.02", (round(bb), round(sb), f2(tb), f"{pb:.2f}") == (23667, 9638, "2.46", "0.02"))
check("E15: 2.052 < t_bedrooms < 2.771", c95 < tb < c99 and f2(23667 / 9638) == "2.46")
check("E17: 200 x 73.77 = 14,754; 100 x = 7,377; +intercept = 129,771; 200 x 11.17 = 2,234",
      (round(200 * 73.77), round(100 * 73.77), round(115017 + 200 * 73.77), round(200 * 11.17)) == (14754, 7377, 129771, 2234))
check("E17: average price ~ $254,000", round(d["price"].mean(), -3) == 254000)
check("E18: 73.77 ~ $74", round(b2) == 74)
check("E19: intercept 115,017, p < 0.001; size range 1,400-3,300", round(b1) == 115017 and p1 < 0.001 and (d["size"].min(), d["size"].max()) == (1400, 3300))
check("E19: intercept se 21,489 > slope se", round(se1) == 21489 and se1 > se2)
check("E21: (73.77-100)/11.17 = -2.35; -26.23; -0.26; 6.60",
      (f2((73.77 - 100) / 11.17), f2(73.77 - 100), f2((73.77 - 100) / 100), f2(t2)) == ("-2.35", "-26.23", "-0.26", "6.60"))
check("E21: |t| for null 100 > 2.052 (exact)", abs(t_null(100)) > c95)
check("E22: 45 and 99 rejected; 52, 75, 95 not (exact t vs 2.052)",
      all(abs(t_null(c)) > c95 for c in (45, 99)) and all(abs(t_null(c)) < c95 for c in (52, 75, 95)))
check("E22: 45 < 50.84 and 99 > 96.70; 52, 75, 95 inside", 45 < ci[0] and 99 > ci[1] and all(ci[0] < c < ci[1] for c in (52, 75, 95)))
check("E22 explanation: t(45) = 2.57, t(99) = -2.26", (f2(t_null(45)), f2(t_null(99))) == ("2.57", "-2.26"))
check("E23/E25: null 90 two-sided p = 0.158, not rejected at 5%; t = -1.45",
      f"{2 * stats.t.sf(abs(t_null(90)), df):.3f}" == "0.158" and f2(t_null(90)) == "-1.45")
check("E23: 60 and 75 inside the CI", all(ci[0] < c < ci[1] for c in (60, 75)))
check("E25: one-sided lower p = 0.079 (0.05 < p < 0.10); 2 x 0.158 = 0.316; 1 - 0.079 = 0.921",
      f"{stats.t.cdf(t_null(90), df):.3f}" == "0.079" and 0.05 < stats.t.cdf(t_null(90), df) < 0.10
      and f"{2 * 0.158:.3f}" == "0.316" and f"{stats.t.sf(t_null(90), df):.3f}" == "0.921")
check("E26: upper test of 80: t = -0.56, p_upper = 0.71 > 0.5", f2(t_null(80)) == "-0.56" and f2(stats.t.sf(t_null(80), df)) == "0.71")
check("E28: robust se 11.33, CI [50.52, 97.02], still significant",
      (f2(rse2), f2(rci[0]), f2(rci[1])) == ("11.33", "50.52", "97.02") and rci[0] > 0)
check("E28: robust width 46.5 > classical 45.9", (f"{rci[1] - rci[0]:.1f}", f"{ci[1] - ci[0]:.1f}") == ("46.5", "45.9"))
check("E28/E29: slope SE +1.4%, intercept SE -5.5%",
      (f"{100 * (rse2 / se2 - 1):.1f}", f"{100 * (rse1 / se1 - 1):.1f}") == ("1.4", "-5.5"))
check("E29: intercept robust SE 20,299 < classical 21,489", (round(rse1), round(se1)) == (20299, 21489) and rse1 < se1)

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic)
check("P04: 100 - 2 = 98", 100 - 2 == 98)
check("P05 explanation: t crit 3.182 (3 df), 2.306 (8 df), 1.984 (98 df)",
      tuple(f"{stats.t.ppf(0.975, k):.3f}" for k in (3, 8, 98)) == ("3.182", "2.306", "1.984"))
check("P07: 12/(6x2) = 1.0; 12/2 = 6.0; 12/72 = 0.17; 12/6 = 2.0",
      (12 / (math.sqrt(36) * 2), 12 / 2, f2(12 / 72), 12 / 6) == (1.0, 6.0, "0.17", 2.0))
check("P02/P08: 5.2 +/- 1.8 = [3.4, 7.0]; +/- 2.0 = [3.2, 7.2]; +/- 3.6 = [1.6, 8.8]; +/- 7.2 = [-2.0, 12.4]",
      tuple(f"{v:.1f}" for v in (5.2 - 1.8, 5.2 + 1.8, 5.2 - 2, 5.2 + 2, 5.2 - 3.6, 5.2 + 3.6, 5.2 - 7.2, 5.2 + 7.2))
      == ("3.4", "7.0", "3.2", "7.2", "1.6", "8.8", "-2.0", "12.4"))
check("P11: (8.8-1.6)/2 = 3.6; 3.6/2.0 = 1.8; width 7.2", (f"{(8.8 - 1.6) / 2:.1f}", f"{3.6 / 2.0:.1f}", f"{8.8 - 1.6:.1f}") == ("3.6", "1.8", "7.2"))
check("P12: A width 2, B width 8 (four times)", (4 - 2, 7 - (-1)) == (2, 8))
check("P13: crit 4.303 (n=4, 2 df), 2.009 (n=52, 50 df); 4.303 > 2 x 2.009",
      (f"{stats.t.ppf(0.975, 2):.3f}", f"{stats.t.ppf(0.975, 50):.3f}") == ("4.303", "2.009") and 4.303 > 2 * 2.009)
check("P14: 1 - 0.03 = 97%", round(100 * (1 - 0.03)) == 97)
check("P15: t = 5.2/1.8 = 2.89 > 2.63 > 1.98 (98 df crit 1.984, 2.627)",
      f2(5.2 / 1.8) == "2.89" and (f"{stats.t.ppf(0.975, 98):.2f}", f"{stats.t.ppf(0.995, 98):.2f}") == ("1.98", "2.63") and 5.2 / 1.8 > 2.63)
check("P17: 4 x 5.20 = 20.80; 5.2/4 = 1.30; 5.2 + 4 = 9.20; 4 x 1.8 = 7.20",
      (f2(4 * 5.2), f2(5.2 / 4), f2(5.2 + 4), f2(4 * 1.8)) == ("20.80", "1.30", "9.20", "7.20"))
check("P18: 0.50 x 2,000 h = $1,000 a year", 0.5 * 2000 == 1000)
check("P19: t_A = 0.5, t_B = 5", (0.05 / 0.10, round(0.05 / 0.01, 6)) == (0.5, 5.0))
check("P21: (5.2-6)/1.8 = -0.44; 5.2-6 = -0.80; (5.2-6)/6 = -0.13; 5.2/1.8 = 2.89",
      (f2((5.2 - 6) / 1.8), f2(5.2 - 6), f2((5.2 - 6) / 6), f2(5.2 / 1.8)) == ("-0.44", "-0.80", "-0.13", "2.89"))
check("P22: 0 and 9.5 outside [1.6, 8.8]; 2.0 and 6.0 inside", not (1.6 <= 0 <= 8.8) and 9.5 > 8.8 and all(1.6 < c < 8.8 for c in (2.0, 6.0)))
check("P25: t = (5.2-3)/1.8 = 1.22; Phi(1.22) = 0.89; upper 0.11; two-sided 0.22; 0.89/2 = 0.44",
      f2((5.2 - 3) / 1.8) == "1.22" and (f2(stats.norm.cdf(1.22)), f2(stats.norm.sf(1.22)), f2(2 * stats.norm.sf(1.22)), f2(stats.norm.cdf(1.22) / 2))
      == ("0.89", "0.11", "0.22", "0.44"))
check("P25 D: upper tail of t = 2.89 ~ 0.002", f"{stats.norm.sf(5.2 / 1.8):.3f}" == "0.002")
check("P27: 22.5 vs 15.0 is a 50% gap (> 20%)", (22.5 / 15.0 - 1) == 0.5)

# ---------------------------------------------------------------- 3. CLAIMS
check("slope positive and significant at 5% (t > crit)", b2 > 0 and t2 > c95)
check("intercept significant (CI excludes 0)", m.confint().loc["Intercept"].values[0] > 0)
check("t-based 95% interval wider than normal-based (2.052 > 1.96)", c95 > 1.96)
check("90% interval narrower than 95%, 99% wider (critical values ordered)", c90 < c95 < c99)
check("bedrooms slope positive", bb > 0)
check("robust slope SE > classical; robust intercept SE < classical (robust not always larger)", rse2 > se2 and rse1 < se1)
check("coefficient unchanged under HC1", abs(rb.coef()["size"] - b2) < 1e-9)
check("robust t = 6.51, still > 2.052", f2(rb.tstat()["size"]) == "6.51" and rb.tstat()["size"] > c95)
check("one-sided p = two-sided p / 2 when sign as predicted (null 90, lower tail)",
      abs(stats.t.cdf(t_null(90), df) - stats.t.sf(abs(t_null(90)), df) * 2 / 2) < 1e-12)

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
