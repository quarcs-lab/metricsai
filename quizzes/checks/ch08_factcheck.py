#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch08.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Run:  python3 quizzes/checks/ch08_factcheck.py      (exit 1 on any failure)
"""

import json
import re
import sys
from pathlib import Path

import pandas as pd
import pyfixest as pf
from scipy import stats

CHAPTER = "ch08"
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


# ---------------------------------------------------------------- 1. FACTS
h = load("AED_HEALTH2009.DTA")
c = load("AED_CAPM.DTA")
g = load("AED_GDPUNEMPLOY.DTA")
row = h.set_index("code")

le = pf.feols("lifeexp ~ hlthpc", data=h)
le_r = pf.feols("lifeexp ~ hlthpc", data=h, vcov="HC1")
im = pf.feols("infmort ~ hlthpc", data=h)
im_r = pf.feols("infmort ~ hlthpc", data=h, vcov="HC1")
hx = pf.feols("hlthpc ~ gdppc", data=h)
hx_r = pf.feols("hlthpc ~ gdppc", data=h, vcov="HC1")
sub = h[~h["code"].isin(["USA", "LUX"])]
hs = pf.feols("hlthpc ~ gdppc", data=sub)
capm = pf.feols("rko_rf ~ rm_rf", data=c)
okun = pf.feols("rgdpgrowth ~ uratechange", data=g)

a_le, b_le = le.coef()["Intercept"], le.coef()["hlthpc"]
a_im, b_im = im.coef()["Intercept"], im.coef()["hlthpc"]
a_hx, b_hx = hx.coef()["Intercept"], hx.coef()["gdppc"]
b_hs = hs.coef()["gdppc"]
alpha, beta = capm.coef()["Intercept"], capm.coef()["rm_rf"]
se_beta = capm.se()["rm_rf"]
a_ok, b_ok = okun.coef()["Intercept"], okun.coef()["uratechange"]
se_ok = okun.se()["uratechange"]
res_le = h["lifeexp"] - le.predict()
res_im = h["infmort"] - im.predict()
res_hx = h["hlthpc"] - hx.predict()
g = g.assign(pred=okun.predict(), res=g["rgdpgrowth"] - okun.predict())
mean_gdp, mean_hlth = h["gdppc"].mean(), h["hlthpc"].mean()
elast = b_hx * mean_gdp / mean_hlth

print(f"FACTS health: n={len(h)} lifeexp: a={a_le:.4f} b={b_le:.7f} t={le.tstat()['hlthpc']:.3f} p={le.pvalue()['hlthpc']:.5f} "
      f"robust se={le_r.se()['hlthpc']:.7f} (classical {le.se()['hlthpc']:.7f}) t={le_r.tstat()['hlthpc']:.3f} p={le_r.pvalue()['hlthpc']:.4f} R2={le._r2:.4f}")
print(f"FACTS infmort: a={a_im:.4f} b={b_im:.7f} t={im.tstat()['hlthpc']:.3f} p={im.pvalue()['hlthpc']:.4f} "
      f"robust t={im_r.tstat()['hlthpc']:.3f} p={im_r.pvalue()['hlthpc']:.4f} R2={im._r2:.4f}")
print(f"FACTS hlthpc~gdppc: a={a_hx:.2f} b={b_hx:.6f} se={hx.se()['gdppc']:.5f} robust se={hx_r.se()['gdppc']:.5f} "
      f"robust t={hx_r.tstat()['gdppc']:.3f} R2={hx._r2:.4f}; subset b={b_hs:.6f} R2={hs._r2:.4f}; "
      f"means gdp={mean_gdp:.2f} hlth={mean_hlth:.2f} elasticity={elast:.4f}")
print(f"FACTS USA: hlthpc={row.loc['USA','hlthpc']} lifeexp={row.loc['USA','lifeexp']:.1f} infmort={row.loc['USA','infmort']:.1f} "
      f"gdppc={row.loc['USA','gdppc']:.0f}; LUX gdppc={row.loc['LUX','gdppc']:.0f} hlthpc={row.loc['LUX','hlthpc']}")
print(f"FACTS CAPM: n={len(c)} {c['date'].min():%Y-%m}..{c['date'].max():%Y-%m} alpha={alpha:.5f} t={capm.tstat()['Intercept']:.3f} "
      f"beta={beta:.5f} se={se_beta:.5f} t={capm.tstat()['rm_rf']:.3f} R2={capm._r2:.4f} mean rko_rf={c['rko_rf'].mean():.5f} "
      f"sd rko_rf={c['rko_rf'].std():.4f} sd rm_rf={c['rm_rf'].std():.4f}")
print(f"FACTS Okun: n={len(g)} years {int(g['year'].min())}-{int(g['year'].max())} a={a_ok:.4f} b={b_ok:.5f} se={se_ok:.5f} "
      f"t(-2)={(b_ok + 2) / se_ok:.4f} R2={okun._r2:.4f} CI={okun.confint().loc['uratechange'].values.round(3)}")
print()

# ---------------------------------------------------------------- 2. CHECKS (exam)
# E01, E21: coverage of the chapter's datasets
check("E01/E21: Okun data 1961-2019, 59 annual obs", (int(g["year"].min()), int(g["year"].max()), len(g)) == (1961, 2019, 59))
check("E01/P17: CAPM data May 1983 - Oct 2012, 354 months",
      (f"{c['date'].min():%Y-%m}", f"{c['date'].max():%Y-%m}", len(c)) == ("1983-05", "2012-10", 354))
check("E01: health data 34 countries, all 2009", len(h) == 34 and set(h["year"]) == {2009})
# E02, E03: life expectancy equation 73.08 + 0.00111 x hlthpc
check("E02/E03: lifeexp = 73.08 + 0.00111 x hlthpc", (f2(a_le), f"{b_le:.5f}") == ("73.08", "0.00111"))
check("E02: 1,000 x 0.00111 = 1.11 ~ 1.1 years", f2(1000 * 0.00111) == "1.11" and f1(1000 * b_le) == "1.1")
check("E03: U.S. spends 7,990, life exp 76.0", row.loc["USA", "hlthpc"] == 7990 and f1(row.loc["USA", "lifeexp"]) == "76.0")
pred_us = 73.08 + 0.00111 * 7990
check("E03: predicted 81.95, residual -5.95 ~ -6 (rounded eq); exact residual -5.97 ~ -6",
      f2(pred_us) == "81.95" and round(76.0 - pred_us) == -6 and round(res_le[h["code"] == "USA"].iloc[0]) == -6)
check("E03 distractors: vs mean -0.70 ~ -1; spending in thousands +2.91 ~ +3; slope term 8.87 ~ +9",
      round(76.0 - h["lifeexp"].mean()) == -1 and round(76.0 - (73.08 + 0.00111 * 7.99)) == 3 and round(0.00111 * 7990) == 9)
check("E03 explanation: U.S. has the most negative life-expectancy residual", res_le.idxmin() == h.index[h["code"] == "USA"][0])
# E04, E06: life expectancy inference
check("E04/E06: classical t = 3.9", f1(le.tstat()["hlthpc"]) == "3.9")
check("E06: crit 2.04 at 32 df; robust t 2.4 > 2.04", f2(stats.t.ppf(0.975, 32)) == "2.04" and le_r.tstat()["hlthpc"] > stats.t.ppf(0.975, 32))
check("E06: robust t = 2.4, p = 0.02 (< 0.05)", f1(le_r.tstat()["hlthpc"]) == "2.4" and f2(le_r.pvalue()["hlthpc"]) == "0.02" and le_r.pvalue()["hlthpc"] < 0.05)
check("E06: robust SE > classical SE; coefficient identical", le_r.se()["hlthpc"] > le.se()["hlthpc"] and abs(le_r.coef()["hlthpc"] - b_le) < 1e-12)
# E07, E08: infant mortality
check("E07: classical t = -2.3, p = 0.03", f1(im.tstat()["hlthpc"]) == "-2.3" and f2(im.pvalue()["hlthpc"]) == "0.03")
check("E07: robust t = -1.3, p = 0.19 (> 0.05)", f1(im_r.tstat()["hlthpc"]) == "-1.3" and f2(im_r.pvalue()["hlthpc"]) == "0.19")
check("E08/P03: infmort = 6.70 - 0.000693 x hlthpc", (f2(a_im), f"{b_im:.6f}") == ("6.70", "-0.000693"))
check("E08: 3,000 x 0.000693 = 2.08 ~ 2.1; distractors 4,500 x = 3.12 ~ 3.1; per 1,000 = 0.69 ~ 0.7; level at 4,500 = 3.58 ~ 3.6",
      (f2(3000 * 0.000693), f1(3000 * 0.000693), f1(4500 * 0.000693), f1(1000 * 0.000693), f1(6.70 - 4500 * 0.000693))
      == ("2.08", "2.1", "3.1", "0.7", "3.6"))
check("E08 explanation: 2.079 x 100 = 208 deaths per 100,000 births", round(3000 * 0.000693 * 100) == 208)
check("E08: 1,500 and 4,500 within the sample's spending range (923-7,990)", h["hlthpc"].min() < 1500 and h["hlthpc"].max() > 4500)
# E09, E10, E11: health spending and income
check("E09: hlthpc = 285 + 0.0899 x gdppc", (round(a_hx), f"{b_hx:.4f}") == (285, "0.0899"))
check("E09: 1,000 x 0.0899 = 89.9 ~ $90", round(1000 * 0.0899) == 90)
check("E10: means 33,054 and 3,256", (round(mean_gdp), round(mean_hlth)) == (33054, 3256))
check("E10: elasticity 0.0899 x 33,054 / 3,256 = 0.91 (exact 0.91)", f2(0.0899 * 33054 / 3256) == "0.91" and f2(elast) == "0.91")
check("E10 distractors: inverted 1.10; means swapped 0.009; slope 0.09",
      (f2(3256 / (0.0899 * 33054)), f"{0.0899 * 3256 / 33054:.3f}", f2(0.0899)) == ("1.10", "0.009", "0.09"))
# E12, E13: outliers
check("E12/E13: full slope 0.090, R2 0.60; subset slope 0.127, R2 0.93",
      (f"{b_hx:.3f}", f2(hx._r2), f"{b_hs:.3f}", f2(hs._r2)) == ("0.090", "0.60", "0.127", "0.93"))
check("E12: slope rises ~41% (0.127/0.090 and exact)", round(100 * (0.127 / 0.090 - 1)) == 41 and round(100 * (b_hs / b_hx - 1)) == 41)
check("E12: subset has 32 countries", len(sub) == 32)
check("E12 explanation: USA residual ~ +3,640", round(res_hx[h["code"] == "USA"].iloc[0], -1) == 3640)
check("CLAIM report: LUX residual ~ -2,950 (below the line, contrary to qmd lines 498/528/1137)", round(res_hx[h["code"] == "LUX"].iloc[0], -1) == -2950)
# E14-E20: CAPM
check("E16/E18: beta 0.61, R2 0.20", (f2(beta), f2(capm._r2)) == ("0.61", "0.20"))
check("E16: 0.61 x 3 = 1.83 ~ 1.8 (exact beta x 3 = 1.8); distractors R2 x 3 = 0.6, 3 / 0.61 = 4.9, beta = 1 -> 3",
      (f1(0.61 * 3), f1(beta * 3), f1(0.20 * 3), f1(3 / 0.61)) == ("1.8", "1.8", "0.6", "4.9"))
check("E17/P17: alpha 0.0068 = 0.68% per month", f"{alpha:.4f}" == "0.0068")
check("E17 explanation: mean Coca-Cola excess return 1.02% per month (not 0.68%)", f2(100 * c["rko_rf"].mean()) == "1.02")
check("E18: beta t = 9.4 with 354 months", f1(capm.tstat()["rm_rf"]) == "9.4" and len(c) == 354)
check("E19: 1 - R2 ~ 80%", round(100 * (1 - capm._r2)) == 80)
check("E20: beta 0.606, se 0.0644", (f"{beta:.3f}", f"{se_beta:.4f}") == ("0.606", "0.0644"))
check("E20: t(beta=1) = (0.606-1)/0.0644 = -6.1 (exact -6.1); crit 1.97 (352 df)",
      f1((0.606 - 1) / 0.0644) == "-6.1" and f1((beta - 1) / se_beta) == "-6.1" and f2(stats.t.ppf(0.975, len(c) - 2)) == "1.97")
check("E20 distractors: -0.39 (no SE), 24.9 (wrong-sign null), -0.65 (divide by estimate)",
      (f2(0.606 - 1), f1((0.606 + 1) / 0.0644), f2((0.606 - 1) / 0.606)) == ("-0.39", "24.9", "-0.65"))
# E21-E25: Okun
check("E21/E22: growth = 3.01 - 1.59 x URATEchange", (f2(a_ok), f2(b_ok)) == ("3.01", "-1.59"))
check("E21 D: mean change in unemployment is not -1.59 (it is -0.03)", f2(g["uratechange"].mean()) == "-0.03")
check("E22: 3.01 - 1.59 x 3 = -1.76 (exact -1.76); distractors -4.77, 7.78, 1.42",
      (f2(3.01 - 1.59 * 3), f2(a_ok + b_ok * 3), f2(-1.59 * 3), f2(3.01 + 1.59 * 3), f2(3.01 - 1.59)) == ("-1.76", "-1.76", "-4.77", "7.78", "1.42"))
check("E22 explanation: 2009 unemployment change ~ +3.5 points (sample max)",
      f1(g.loc[g["year"] == 2009, "uratechange"].iloc[0]) == "3.5" and g["uratechange"].idxmax() == g.index[g["year"] == 2009][0])
check("E23: b = -1.589, se = 0.175", (f"{b_ok:.3f}", f"{se_ok:.3f}") == ("-1.589", "0.175"))
check("E23: t(-2) = 0.411/0.175 = 2.35 (exact 2.35); crit 2.00 (57 df)",
      f2((-1.589 + 2) / 0.175) == "2.35" and f2((b_ok + 2) / se_ok) == "2.35" and f2(stats.t.ppf(0.975, 57)) == "2.00")
check("E23 distractors: -9.08 (null 0), 0.41 (no SE), -20.5 (wrong sign of null)",
      (f2(-1.589 / 0.175), f2(-1.589 + 2), f1((-1.589 - 2) / 0.175)) == ("-9.08", "0.41", "-20.5"))
check("E24 explanation: estimate -1.59 differs from -2.0", f2(b_ok) == "-1.59")
check("E25: R2 = 0.59", f2(okun._r2) == "0.59")
dec = g[(g["year"] >= 2010) & (g["year"] <= 2019)]
check("E25: actual below predicted in 9 of 10 years 2010-2019", len(dec) == 10 and int((dec["res"] < 0).sum()) == 9)
y1115 = g[(g["year"] >= 2011) & (g["year"] <= 2015)]
check("E25 D: predicted >= ~4% in 2011-2015 (min 4.09), actual between 1.5% and 3% in 2011-2016",
      y1115["pred"].min() > 4.0 and g[(g["year"] >= 2011) & (g["year"] <= 2016)]["rgdpgrowth"].between(1.5, 3.0).all())
check("E25 D: unemployment fell in every year 2011-2019", (g[(g["year"] >= 2011)]["uratechange"] < 0).all())

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic)
check("P02: 1,000 x 0.00045 = 0.45", f2(1000 * 0.00045) == "0.45")
pred_p03 = 6.70 - 0.000693 * 6000
check("P03: predicted 2.54, residual +2.5; slope term 4.16; thousands -1.7; no intercept +9.2; slope-only -4.2",
      (f2(pred_p03), f1(5.0 - pred_p03), f2(0.000693 * 6000), f1(5.0 - (6.70 - 0.000693 * 6)), f1(5.0 + 0.000693 * 6000), f1(-0.000693 * 6000))
      == ("2.54", "2.5", "4.16", "-1.7", "9.2", "-4.2"))
check("P07: (2.6 + 1.5)/2 = 2.05", f2((2.6 + 1.5) / 2) == "2.05")
check("P08: 10,000 x 0.00025 = 2.5; 40,000 x = 10.0; per 1,000 = 0.25; level 12.0",
      (f1(10000 * 0.00025), f1(40000 * 0.00025), f2(1000 * 0.00025), f1(2.0 + 40000 * 0.00025)) == ("2.5", "10.0", "0.25", "12.0"))
check("P09/P10: 1,000 x 0.12 = 120; line passes through means: 2,000 + 0.12 x 50,000 = 8,000", 1000 * 0.12 == 120 and 2000 + 0.12 * 50000 == 8000)
check("P11: elasticity 0.75 -> 0.75% per 1%", 0.75 * 1 == 0.75)
check("P10: elasticity 0.75; inverted 1.33; ratio 6.25; 10% -> 7.5%",
      (f2(0.12 * 50000 / 8000), f2(8000 / (0.12 * 50000)), f2(50000 / 8000), f1(10 * 0.75)) == ("0.75", "1.33", "6.25", "7.5"))
check("P12: 1.2 / 0.8 = 1.5 (+50%); 40 - 2 = 38", f1(1.2 / 0.8) == "1.5" and 40 - 2 == 38)
check("P16: 0.45 x 10 = 4.5; 1 - 0.45 -> 5.5; 10 + 4.5 = 14.5", (f1(0.45 * 10), f1((1 - 0.45) * 10), f1(10 + 0.45 * 10)) == ("4.5", "5.5", "14.5"))
check("P17: 12 x 0.68% = 8.2%; 12 x 0.0068 = 0.08; 0.68/12 = 0.06",
      (f1(12 * 0.68), f2(12 * 0.0068), f2(0.68 / 12)) == ("8.2", "0.08", "0.06") and f1(12 * 100 * alpha) == "8.2")
check("P19: 1 - 0.10 = 0.90", f2(1 - 0.10) == "0.90")
check("P20: (1.30-1)/0.10 = 3.0; 1.30/0.10 = 13.0; gap 0.30; 0.30/1.30 = 0.23; crit 1.97",
      (f1((1.30 - 1) / 0.10), f1(1.30 / 0.10), f2(1.30 - 1), f2(0.30 / 1.30)) == ("3.0", "13.0", "0.30", "0.23"))
check("P22: 2.5 - 1.2 x (-1.5) = 4.3; 2.5 - 1.8 = 0.7; slope term 1.8; one point 3.7",
      (f1(2.5 - 1.2 * -1.5), f1(2.5 - 1.2 * 1.5), f1(1.2 * 1.5), f1(2.5 + 1.2)) == ("4.3", "0.7", "1.8", "3.7"))
check("P23: (-1.20+2)/0.50 = 1.6; -1.20/0.50 = -2.4; gap 0.8; (-1.20-2)/0.50 = -6.4",
      (f1((-1.20 + 2) / 0.50), f1(-1.20 / 0.50), f1(-1.20 + 2), f1((-1.20 - 2) / 0.50)) == ("1.6", "-2.4", "0.8", "-6.4"))

# ---------------------------------------------------------------- 3. CLAIMS
check("CLAIM life expectancy slope positive; infant mortality slope negative", b_le > 0 and b_im < 0)
check("CLAIM E12: USA above the full-sample line, LUX below it (largest |residuals|)",
      res_hx[h["code"] == "USA"].iloc[0] > 0 and res_hx[h["code"] == "LUX"].iloc[0] < 0
      and set(h.loc[res_hx.abs().nlargest(2).index, "code"]) == {"USA", "LUX"})
check("CLAIM E12: Luxembourg has the highest GDP per capita; USA the highest health spending",
      h.loc[h["gdppc"].idxmax(), "code"] == "LUX" and h.loc[h["hlthpc"].idxmax(), "code"] == "USA")
check("CLAIM E12: GDP slope stays significant in the 32-country subsample", hs.pvalue()["gdppc"] < 0.001)
check("CLAIM E06/E07: robust SE larger than classical in the life-expectancy and infant-mortality regressions",
      le_r.se()["hlthpc"] > le.se()["hlthpc"] and im_r.se()["hlthpc"] > im.se()["hlthpc"])
check("CLAIM E09 (avoided distractor): average health share of GDP ~9.7%, so 'about 9% of GDP' would be near-true",
      abs(h["hlthgdp"].mean() - 9.67) < 0.01)
check("CLAIM E17: intercept differs from mean excess return because market mean excess return is not zero",
      c["rm_rf"].mean() > 0.005 and abs(alpha - c["rko_rf"].mean()) > 0.003)
check("CLAIM E15/E17: alpha significant at 5% (p = 0.02)", capm.pvalue()["Intercept"] < 0.05 and f2(capm.pvalue()["Intercept"]) == "0.02")
check("CLAIM E20: beta significantly below 1 at 5%", (beta - 1) / se_beta < -stats.t.ppf(0.975, len(c) - 2))
check("CLAIM E23: 95% CI for Okun slope [-1.94, -1.24] excludes -2",
      tuple(f2(v) for v in okun.confint().loc["uratechange"].values) == ("-1.94", "-1.24") and okun.confint().loc["uratechange"].values[0] > -2)
check("CLAIM E25: 2010 is the one year of 2010-2019 with actual above predicted", dec.loc[dec["res"] > 0, "year"].tolist() == [2010.0])
check("CLAIM report: recession years (1982, 2009) have rising unemployment and negative growth (lower-right quadrant, not upper-left)",
      all((g.loc[g["year"] == y, "uratechange"].iloc[0] > 0) and (g.loc[g["year"] == y, "rgdpgrowth"].iloc[0] < 0) for y in (1982, 2009)))
check("CLAIM report: Coca-Cola's excess returns are MORE volatile than the market's despite beta < 1 (KC 8.5 prose)",
      c["rko_rf"].std() > c["rm_rf"].std() and beta < 1)
check("CLAIM report: chapter table 'R2 +55%' is +54% from exact values", round(100 * (hs._r2 / hx._r2 - 1)) == 54)

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
