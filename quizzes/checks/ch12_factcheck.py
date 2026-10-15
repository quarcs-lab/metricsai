#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch12.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Reproduces the chapter's exact settings: default (iid) and HC1 standard errors from pyfixest;
HAC (Newey-West) SEs from statsmodels on an intercept-only model with maxlags 0 and
int(0.75 * T**(1/3)) = 4; the power curve with se = 15, n = 30 (29 df), two-sided 5% test.
Run:  python3 quizzes/checks/ch12_factcheck.py      (exit 1 on any failure)
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
from statsmodels.regression.linear_model import OLS as smOLS
from statsmodels.tsa.stattools import acf

CHAPTER = "ch12"
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


def r100(x: float) -> int:
    return int(round(x / 100.0)) * 100


# ---------------------------------------------------------------- 1. FACTS
# --- Davis houses: multiple regression, default vs HC1 (Section 12.2)
h = load("AED_HOUSE.DTA")
n = len(h)
FORM = "price ~ size + bedrooms + bathrooms + lotsize + age + monthsold"
md = pf.feols(FORM, data=h)
mr = pf.feols(FORM, data=h, vcov="HC1")
ratio = mr.se() / md.se()
k = len(md.coef())
s_e_multi = math.sqrt(float(np.sum(md._u_hat ** 2)) / (n - k))
t22 = stats.t.ppf(0.975, n - k)
new_house = pd.DataFrame({"size": [2000], "bedrooms": [4], "bathrooms": [2], "lotsize": [2], "age": [40], "monthsold": [6]})
pred_multi = float(md.predict(newdata=new_house)[0])

print("FACTS multiple regression (default vs HC1):")
print(pd.DataFrame({"coef": md.coef(), "se": md.se(), "se_hc1": mr.se(), "ratio": ratio,
                    "p": md.pvalue(), "p_hc1": mr.pvalue()}).round(4).to_string())
print(f"FACTS R2={md._r2:.4f} s_e(multi)={s_e_multi:.2f} df={n - k} t22={t22:.4f} pred(new house)={pred_multi:.2f}")

# --- Davis houses: simple regression and prediction at 2,000 sq ft (Section 12.3)
ms = pf.feols("price ~ size", data=h)
b0, b1 = ms.coef()["Intercept"], ms.coef()["size"]
s_e = math.sqrt(float(np.sum(ms._u_hat ** 2)) / (n - 2))
t27 = stats.t.ppf(0.975, n - 2)
xs = h["size"].to_numpy(dtype=float)
xbar = xs.mean()
Sxx = float(np.sum((xs - xbar) ** 2))
x_star = 2000
pred = b0 + b1 * x_star
dist = (x_star - xbar) ** 2 / Sxx
se_cm = s_e * math.sqrt(1 / n + dist)
se_f = s_e * math.sqrt(1 + 1 / n + dist)
ci = (pred - t27 * se_cm, pred + t27 * se_cm)
pi = (pred - t27 * se_f, pred + t27 * se_f)
print(f"FACTS simple: b0={b0:.2f} b1={b1:.4f} s_e={s_e:.2f} n={n} xbar={xbar:.2f} size range={xs.min():.0f}-{xs.max():.0f} t27={t27:.4f}")
print(f"FACTS x*=2000: pred={pred:.2f} 1/n={1 / n:.4f} dist={dist:.4f} se_cm={se_cm:.2f} se_f={se_f:.2f} "
      f"CI=[{ci[0]:.0f}, {ci[1]:.0f}] PI=[{pi[0]:.0f}, {pi[1]:.0f}] ratio={(pi[1] - pi[0]) / (ci[1] - ci[0]):.3f}")

# --- GDP growth: autocorrelation and HAC (Section 12.2)
gdp = load("AED_REALGDPPC.DTA")
growth = gdp["growth"].dropna()
T = len(growth)
first_date, last_date = gdp.loc[growth.index[0], "daten"], gdp.loc[growth.index[-1], "daten"]
lag_rule = int(0.75 * T ** (1 / 3))
se_def = growth.std() / math.sqrt(T)
X = np.ones(T)
se_hac0 = smOLS(growth, X).fit(cov_type="HAC", cov_kwds={"maxlags": 0}).bse.iloc[0]
se_hac = smOLS(growth, X).fit(cov_type="HAC", cov_kwds={"maxlags": lag_rule}).bse.iloc[0]
rho = acf(growth, nlags=5, fft=False)
yoy = (gdp["realgdppc"] / gdp["realgdppc"].shift(4) - 1) * 100
print(f"FACTS growth: T={T} first={first_date:%Y-%m} last={last_date:%Y-%m} mean={growth.mean():.4f} sd={growth.std():.4f}")
print(f"FACTS growth SEs: default={se_def:.6f} HAC0={se_hac0:.6f} HAC{lag_rule}={se_hac:.6f} ratio={se_hac / se_def:.3f}; "
      f"m=0.75*T^(1/3)={0.75 * T ** (1 / 3):.3f}; acf={np.round(rho, 4)}")

# --- Power curve (Section 12.7, Figure 12.3)
df_p = 29
c_p = stats.t.ppf(0.975, df_p)


def power(b: float) -> float:
    ncp = b / 15
    return 1 - (stats.t.cdf(c_p - ncp, df_p) - stats.t.cdf(-c_p - ncp, df_p))


print(f"FACTS power: crit={c_p:.4f} " + " ".join(f"P({b})={power(b):.4f}" for b in (0, 15, 30, 44, 56, 60)))
print()

# ---------------------------------------------------------------- 2. CHECKS (exam)
check("29 houses; 241 growth observations", n == 29 and T == 241)
check("E01: size coefficient 68.37 under both default and HC1",
      f2(md.coef()["size"]) == "68.37" and abs(mr.coef()["size"] - md.coef()["size"]) < 1e-9)
check("E02: SE ratios size 0.998, bathrooms 1.227, lot size 0.737",
      (f"{ratio['size']:.3f}", f"{ratio['bathrooms']:.3f}", f"{ratio['lotsize']:.3f}") == ("0.998", "1.227", "0.737"))
check("E02 explanation: bathrooms ~23% larger, lot size ~26% smaller",
      round(100 * (ratio["bathrooms"] - 1)) == 23 and round(100 * (1 - ratio["lotsize"])) == 26)
check("E05: N-k = 2,395, N-1 = 2,399, G-k = 19, G-1 = 23", (2400 - 5, 2400 - 1, 24 - 5, 24 - 1) == (2395, 2399, 19, 23))
check("E06: lag-1 autocorrelation 0.866", f"{rho[1]:.3f}" == "0.866")
check("E06: data 1960 Q1 to 2020 Q1, quarterly", (first_date.year, first_date.month, last_date.year, last_date.month) == (1960, 1, 2020, 1))
check("E07: 0.75 x 241 = 180.75 (~181); 0.75 x sqrt(241) = 11.6; 241^(1/3) = 6.2; 0.75 x 241^(1/3) = 4.7 (code: 4)",
      (round(0.75 * 241), f"{0.75 * math.sqrt(241):.1f}", f"{241 ** (1 / 3):.1f}", f"{0.75 * 241 ** (1 / 3):.1f}", lag_rule)
      == (181, "11.6", "6.2", "4.7", 4))
check("E08: mean 1.99, default SE 0.140, HAC SE 0.264, SD 2.18",
      (f2(growth.mean()), f"{se_def:.3f}", f"{se_hac:.3f}", f2(growth.std())) == ("1.99", "0.140", "0.264", "2.18"))
check("E08: shown factors: 1.99 +/- 1.96 x 0.264 = [1.47, 2.51]; x 0.140 = [1.72, 2.26]; +/- 0.264 = [1.73, 2.25]; x 2.18 = [-2.28, 6.26]",
      (f2(1.99 - 1.96 * 0.264), f2(1.99 + 1.96 * 0.264), f2(1.99 - 1.96 * 0.140), f2(1.99 + 1.96 * 0.140),
       f2(1.99 - 0.264), f2(1.99 + 0.264), f2(1.99 - 1.96 * 2.18), f2(1.99 + 1.96 * 2.18))
      == ("1.47", "2.51", "1.72", "2.26", "1.73", "2.25", "-2.28", "6.26"))
check("E08: exact HAC interval also [1.47, 2.51]",
      (f2(growth.mean() - 1.96 * se_hac), f2(growth.mean() + 1.96 * se_hac)) == ("1.47", "2.51"))
check("E08 explanation: HAC/default ratio 1.885 (about 1.9 times)", f"{se_hac / se_def:.3f}" == "1.885")
check("E09: HAC lag 0 (0.1400) ~ default (0.1403)", abs(se_hac0 - se_def) / se_def < 0.01)
check("E10: point prediction $262,559 at 2,000 sq ft; s_e $23,551", round(pred) == 262559 and round(s_e) == 23551)
check("E11: s_e 23,551, 1/n 0.0345, distance 0.0031", (round(s_e), f"{1 / n:.4f}", f"{dist:.4f}") == (23551, "0.0345", "0.0031"))
check("E11: shown factors: 23,551 x sqrt(1.0376) = 23,990; x sqrt(0.0376) = 4,567; x 1.0376 = 24,437",
      (round(23551 * math.sqrt(1.0376)), round(23551 * math.sqrt(0.0376)), round(23551 * 1.0376)) == (23990, 4567, 24437))
check("E11: exact se_f = 23,989 (rounded-input key 23,990 within $1); exact se_cm = 4,565",
      round(se_f) == 23989 and abs(23990 - se_f) < 1.5 and round(se_cm) == 4565)
check("E12/E10: CI [253,192, 271,927], PI [213,338, 311,781], both centered on 262,559",
      (round(ci[0]), round(ci[1]), round(pi[0]), round(pi[1])) == (253192, 271927, 213338, 311781)
      and round((ci[0] + ci[1]) / 2) == round((pi[0] + pi[1]) / 2) == 262559)
check("E14: mean size ~1,883; range 1,400-3,300", round(xbar) == 1883 and (xs.min(), xs.max()) == (1400, 3300))
check("E15: six-regressor s_e 24,936 > size-only 23,551", round(s_e_multi) == 24936 and s_e_multi > s_e)
check("E16: predicted 257,691; t(22) = 2.074", round(pred_multi) == 257691 and f"{t22:.3f}" == "2.074")
check("E16: key [$206,000, $309,400] from shown factors and from the chapter's exact interval",
      (r100(257691 - 2.074 * 24936), r100(257691 + 2.074 * 24936)) == (206000, 309400)
      and (r100(pred_multi - t22 * s_e_multi), r100(pred_multi + t22 * s_e_multi)) == (206000, 309400))
check("E16 distractors: +/- s_e [232,800, 282,600]; /sqrt(29) [248,100, 267,300]; +/- 2 x half-width [154,300, 361,100]",
      (r100(257691 - 24936), r100(257691 + 24936),
       r100(257691 - 2.074 * 24936 / math.sqrt(29)), r100(257691 + 2.074 * 24936 / math.sqrt(29)),
       r100(257691 - 2 * 2.074 * 24936), r100(257691 + 2 * 2.074 * 24936))
      == (232800, 282600, 248100, 267300, 154300, 361100))
check("E19: 1/0.02 = 50; 1 - 0.02 = 0.98; 1/0.10 = 10", (round(1 / 0.02), round(1 - 0.02, 2), round(1 / 0.10)) == (50, 0.98, 10))
check("E21: 90% percentile CI with B = 1,000 uses the 50th and 950th values; 95% uses 25th and 975th; 10% tails 100th/900th",
      (round(0.05 * 1000), round(0.95 * 1000), round(0.025 * 1000), round(0.975 * 1000), round(0.10 * 1000), round(0.90 * 1000))
      == (50, 950, 25, 975, 100, 900))
check("E25/E30: bedrooms p = 0.773 (default)", f"{md.pvalue()['bedrooms']:.3f}" == "0.773")
check("E27: power at beta = 44 is 0.81; Type II probability 0.19", f2(power(44)) == "0.81" and f2(1 - power(44)) == "0.19")
check("E27 explanation: power at beta = 0 equals alpha = 0.05", f2(power(0)) == "0.05")
check("E28: 60 x 0.05 = 3; 60 - 3 = 57", (round(60 * 0.05), 60 - round(60 * 0.05)) == (3, 57))
check("E29: halving the detectable effect needs 4x n (MDE ~ 1/sqrt(n))", math.isclose(1 / math.sqrt(4), 0.5))

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic)
check("P02: t = 5.0/2.0 = 2.50, 5.0/3.5 = 1.43, 7.0/2.0 = 3.50, 7.0/1.8 = 3.89",
      (f2(5 / 2), f2(5 / 3.5), f2(7 / 2), f2(7 / 1.8)) == ("2.50", "1.43", "3.50", "3.89"))
check("P03: -0.90/0.40 = -2.25; -0.90/0.52 = -1.73", (f2(-0.9 / 0.4), f2(-0.9 / 0.52)) == ("-2.25", "-1.73"))
check("P05: G-1 = 49, N-k = 5,996, G = 50, N-G = 5,950", (50 - 1, 6000 - 4, 6000 - 50) == (49, 5996, 5950))
check("P07: 125^(1/3) = 5; 0.75 x 5 = 3.75; 0.75 x 125 = 93.75; 0.75 x 125/3 = 31.25; 5/0.75 = 6.67",
      (round(125 ** (1 / 3), 9), 0.75 * 5, 0.75 * 125, 0.75 * 125 / 3, f2(5 / 0.75)) == (5.0, 3.75, 93.75, 31.25, "6.67"))
check("P08: 0.25 +/- 1.96 x 0.05 = [0.15, 0.35]; x 0.02 = [0.21, 0.29]; +/- 0.05 = [0.20, 0.30]; x 0.07 = [0.11, 0.39]",
      (f2(0.25 - 1.96 * 0.05), f2(0.25 + 1.96 * 0.05), f2(0.25 - 1.96 * 0.02), f2(0.25 + 1.96 * 0.02),
       f2(0.25 - 0.05), f2(0.25 + 0.05), f2(0.25 - 1.96 * 0.07), f2(0.25 + 1.96 * 0.07))
      == ("0.15", "0.35", "0.21", "0.29", "0.20", "0.30", "0.11", "0.39"))
check("P10: 10 + 2x5 + 3x3 = 29; 2x5 + 3x3 = 19; 10 + 2x3 + 3x5 = 31; 10 + 2 + 3 = 15",
      (10 + 2 * 5 + 3 * 3, 2 * 5 + 3 * 3, 10 + 2 * 3 + 3 * 5, 10 + 2 + 3) == (29, 19, 31, 15))
check("P11: sqrt(0.8^2 + 2^2) = 2.15; 0.8 + 2.0 = 2.80; 0.64 + 4 = 4.64",
      (f2(math.sqrt(0.8 ** 2 + 2 ** 2)), f2(0.8 + 2.0), f2(0.8 ** 2 + 2 ** 2)) == ("2.15", "2.80", "4.64"))
check("P13: n x 100 shrinks se_cm by about 10 (1/sqrt(100))", math.isclose(1 / math.sqrt(20000 / 200), 0.1))
check("P13: 1.96 x 2.0 = 3.92 > 1", 1.96 * 2.0 > 1)
check("P16: 29 +/- 1.96 x 2.15 = [24.79, 33.21]; x 0.8 = [27.43, 30.57]; +/- 2.15 = [26.85, 31.15]; x 2.80 = [23.51, 34.49]",
      (f2(29 - 1.96 * 2.15), f2(29 + 1.96 * 2.15), f2(29 - 1.96 * 0.8), f2(29 + 1.96 * 0.8),
       f2(29 - 2.15), f2(29 + 2.15), f2(29 - 1.96 * 2.8), f2(29 + 1.96 * 2.8))
      == ("24.79", "33.21", "27.43", "30.57", "26.85", "31.15", "23.51", "34.49"))
check("P19: 1/0.05 = 20; 1/0.5 = 2; 1/0.95 = 1.05", (round(1 / 0.05), round(1 / 0.5), f2(1 / 0.95)) == (20, 2, "1.05"))
check("P21: B = 4,000, 95%: 100th and 3,900th; 5% tails: 200th and 3,800th",
      (round(0.025 * 4000), round(0.975 * 4000), round(0.05 * 4000), round(0.95 * 4000)) == (100, 3900, 200, 3800))
check("P27: 1 - 0.60 = 0.40", f2(1 - 0.60) == "0.40")
check("P28: 0.05/10 = 0.005; 0.05 x 10 = 0.5", (round(0.05 / 10, 4), round(0.05 * 10, 2)) == (0.005, 0.5))
check("P30: two-sided p 0.45 -> one-sided at most 0.225 > 0.10", 0.45 / 2 == 0.225 and 0.225 > 0.10)

# ---------------------------------------------------------------- 3. CLAIMS
check("HC1 leaves every coefficient unchanged", np.allclose(md.coef().values, mr.coef().values))
check("E02: robust SE larger for bathrooms, smaller for lot size and bedrooms (robust not always larger)",
      ratio["bathrooms"] > 1 and ratio["lotsize"] < 1 and ratio["bedrooms"] < 1)
check("E02: bathrooms has the ratio farthest above 1", ratio.idxmax() == "bathrooms")
check("E03: only size significant at 5% under default and under HC1 (same set of significant regressors)",
      [v for v in md.coef().index if v != "Intercept" and md.pvalue()[v] < 0.05] == ["size"]
      and [v for v in mr.coef().index if v != "Intercept" and mr.pvalue()[v] < 0.05] == ["size"])
check("E06: lag-1 autocorrelation strongly positive", rho[1] > 0.8)
check("E06: growth is the 4-quarter (year-on-year) % change in real GDP per capita, observed quarterly",
      float((yoy.loc[growth.index] - growth).abs().max()) < 1e-3)
check("E08: HAC SE larger than default SE", se_hac > se_def)
check("E11: forecast SE exceeds s_e", se_f > s_e)
check("E13: se_cm -> 0 and se_f -> s_e as n grows (formula at n = 1e6, same spread)",
      s_e * math.sqrt(1 / 1e6 + dist * n / 1e6) < 0.01 * s_e)
check("E14: conditional-mean SE smallest at x* = mean size", all(
      s_e * math.sqrt(1 / n + (x - xbar) ** 2 / Sxx) >= s_e * math.sqrt(1 / n) for x in (1400, 2000, 3300, xbar)))
check("E15: six-regressor 95% PI wider than size-only PI for a house at the sample means",
      t22 * s_e_multi * math.sqrt(1 + 1 / n) > t27 * s_e * math.sqrt(1 + 1 / n))
Xm = np.column_stack([np.ones(n)] + [h[v].to_numpy(dtype=float) for v in ("size", "bedrooms", "bathrooms", "lotsize", "age", "monthsold")])
x0 = np.array([1, 2000, 4, 2, 2, 40, 6], dtype=float)
se_cm_multi = s_e_multi * math.sqrt(float(x0 @ np.linalg.inv(Xm.T @ Xm) @ x0))
print(f"FACTS multi at new house: se_cm={se_cm_multi:.2f} exact se_f={math.sqrt(s_e_multi ** 2 + se_cm_multi ** 2):.2f}")
check("E16: chapter's approximate PI (t x s_e) is narrower than the exact PI (omits the estimation term)",
      math.sqrt(s_e_multi ** 2 + se_cm_multi ** 2) > s_e_multi)
check("E16/E10: PI width / CI width = 5.25 (point prediction shared)", f2((pi[1] - pi[0]) / (ci[1] - ci[0])) == "5.25")
check("E27: power curve symmetric and rising in |beta|", math.isclose(power(30), power(-30)) and power(15) < power(30) < power(44) < power(56))
check("E30: bedrooms positively correlated with price (r = 0.43) and with size (r = 0.52)",
      f2(h["price"].corr(h["bedrooms"])) == "0.43" and f2(h["size"].corr(h["bedrooms"])) == "0.52")
check("E30: bedrooms not significant under HC1 either (p = 0.749)", f"{mr.pvalue()['bedrooms']:.3f}" == "0.749")
check("E10 distractor: sample mean price $253,910 (differs from the prediction at 2,000 sq ft)", round(h["price"].mean()) == 253910)
check("E27 C false: P(|estimate - 44| < 15) = P(|T29| < 1) ~ 0.67, not 0.81", f2(stats.t.cdf(1, 29) - stats.t.cdf(-1, 29)) == "0.67")
check("E03 explanation: size p = 0.0002 under both methods", f"{md.pvalue()['size']:.4f}" == "0.0002" and f"{mr.pvalue()['size']:.4f}" == "0.0002")
check("E09 explanation: HAC0 0.1400, default 0.1403, HAC4 0.2645",
      (f"{se_hac0:.4f}", f"{se_def:.4f}", f"{se_hac:.4f}") == ("0.1400", "0.1403", "0.2645"))
check("E11 explanation: se_f / se_cm = 5.3", f"{se_f / se_cm:.1f}" == "5.3")
check("E15 explanation: df 22 vs 27", (n - k, n - 2) == (22, 27))
check("E16: 2.074 x 24,936 = 51,717", round(2.074 * 24936) == 51717)
check("E20: n = 25 within the chapter's small-sample range (n < 30-50); n = 8 below 10", 25 < 30 and 8 < 10)
check("E25: age p = 0.259 (default), not significant at 5%", f"{md.pvalue()['age']:.3f}" == "0.259" and md.pvalue()["age"] > 0.05)
check("E12 E: 2,600 sq ft lies inside the observed size range", 1400 <= 2600 <= 3300)
check("E02 key: bathrooms is the only one of size/bathrooms/lot size with ratio > 1", ratio["bathrooms"] > 1 and ratio["size"] < 1 and ratio["lotsize"] < 1)
check("E28 explanation: 20 tests x 0.05 = 1", round(20 * 0.05) == 1)
check("E07 feedback: 241^(1/3) = 6.22", f2(241 ** (1 / 3)) == "6.22")
check("E08 feedback: margin 1.96 x 0.264 = 0.52; HAC/default 0.264/0.140 ~ 1.9", f2(1.96 * 0.264) == "0.52" and f"{0.264 / 0.140:.1f}" == "1.9")
check("E02 distractor: 1 - 0.998 = 0.2%", f"{100 * (1 - 0.998):.1f}" == "0.2")
check("P16: 1.96 x 2.15 = 4.21; P13: 1.96 x 2.0 = 3.92; P08: 1.96 x 0.05 = 0.098",
      (f2(1.96 * 2.15), f2(1.96 * 2.0), f"{1.96 * 0.05:.3f}") == ("4.21", "3.92", "0.098"))
check("P02/P03/P16 'about 1.96' is the large-sample 5% critical value", f2(stats.norm.ppf(0.975)) == "1.96")
check("P30 internally consistent: estimate 5, 95% CI [-8, 18] (half-width 13) implies p ~ 0.45",
      (5 - 13, 5 + 13) == (-8, 18) and f2(2 * stats.norm.sf(5 / (13 / 1.96))) == "0.45")

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
