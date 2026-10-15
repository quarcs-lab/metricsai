#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch05.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Run:  python3 quizzes/checks/ch05_factcheck.py      (exit 1 on any failure)
"""

import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf
from scipy.ndimage import gaussian_filter1d
from statsmodels.nonparametric.smoothers_lowess import lowess

CHAPTER = "ch05"
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
d = load("AED_HOUSE.DTA")
price, size = d["price"], d["size"]
n = len(d)
m = pf.feols("price ~ size", data=d)
b1, b2 = m.coef()["Intercept"], m.coef()["size"]
se_b2, t_b2 = m.se()["size"], m.tstat()["size"]
ci = m.confint().loc["size"].to_numpy()
r2 = m._r2
u = np.asarray(m._u_hat)
rss = float((u ** 2).sum())
tss = float(((price - price.mean()) ** 2).sum())
ess = tss - rss
s_e = math.sqrt(rss / (n - 2))
r = price.corr(size)
cov = price.cov(size)
sx, sy = size.std(), price.std()

rev = pf.feols("size ~ price", data=d)
c2, r2_rev = rev.coef()["price"], rev._r2
r2_bed = pf.feols("price ~ bedrooms", data=d)._r2
r_bed = price.corr(d["bedrooms"])
r_age = price.corr(d["age"])

price_rng = pd.cut(price, bins=[0, 249999, np.inf], labels=["lo", "hi"])
size_rng = pd.cut(size, bins=[0, 1799, 2399, np.inf], labels=["S", "M", "L"])
tab = pd.crosstab(price_rng, size_rng)

resid = pd.Series(u, index=d.index)
std_resid = resid / s_e
drop_slopes = pd.Series({i: pf.feols("price ~ size", data=d.drop(i)).coef()["size"] for i in d.index})
i_big = size.idxmax()
lw = lowess(price, size, frac=0.6)
_o = np.argsort(size.to_numpy())
kern_gap = np.abs(gaussian_filter1d(price.to_numpy()[_o].astype(float), 2) - (b1 + b2 * size.to_numpy()[_o]))
lw_gap = np.abs(lw[:, 1] - (b1 + b2 * lw[:, 0]))


def pred(x: float) -> float:
    """Prediction from the chapter's rounded equation 115,017 + 73.77 x."""
    return 115017 + 73.77 * x


print(f"FACTS n={n} mean price={price.mean():.2f} median={price.median()} sd={sy:.4f} "
      f"min={price.min()} max={price.max()}")
print(f"FACTS size mean={size.mean():.4f} median={size.median()} sd={sx:.4f} min={size.min()} max={size.max()}")
print(f"FACTS b1={b1:.4f} b2={b2:.6f} se(b2)={se_b2:.4f} t={t_b2:.4f} CI={ci} R2={r2:.6f}")
print(f"FACTS TSS={tss:.6e} ESS={ess:.6e} RSS={rss:.6e} s_e={s_e:.4f}")
print(f"FACTS r={r:.6f} cov={cov:.2f} sy/sx={sy / sx:.4f} reverse slope={c2:.7f} reverse R2={r2_rev:.6f} 1/b2={1 / b2:.6f}")
print(f"FACTS r(price,bedrooms)={r_bed:.4f} R2(price~bedrooms)={r2_bed:.4f} r(price,age)={r_age:.4f}")
print(f"FACTS crosstab:\n{tab}")
print(f"FACTS std resid max={std_resid.max():.4f} at size={size[std_resid.idxmax()]}, price={price[std_resid.idxmax()]}, "
      f"resid={resid.max():.2f}; drop-one slopes {drop_slopes.min():.4f}..{drop_slopes.max():.4f}; "
      f"drop largest house -> {drop_slopes[i_big]:.4f}; LOWESS-OLS max gap {lw_gap.max():.0f}; kernel-OLS max gap {kern_gap.max():.0f} (bank avoids the kernel claim)\n")

# ---------------------------------------------------------------- 2. CHECKS (exam)
check("n = 29 houses", n == 29)
check("mean price $253,910, median $244,000", round(price.mean()) == 253910 and price.median() == 244000)
check("SD price $37,391, SD size 398 sq ft", round(sy) == 37391 and round(sx) == 398)
check("size range 1,400 to 3,300 sq ft", (size.min(), size.max()) == (1400, 3300))
check("crosstab: <$250k: 11 / 6 / 0 (17); >=$250k: 2 / 7 / 3 (12)",
      tab.loc["lo"].tolist() == [11, 6, 0] and tab.loc["hi"].tolist() == [2, 7, 3])
check("E02: 11/13 ~85%; distractors 11/29 ~38%, 11/17 ~65%, 13/29 ~45%",
      (round(100 * 11 / 13), round(100 * 11 / 29), round(100 * 11 / 17), round(100 * 13 / 29)) == (85, 38, 65, 45))
check("r = 0.7858 (~0.79)", f"{r:.4f}" == "0.7858" and f"{r:.2f}" == "0.79")
check("covariance ~11.7 million", f"{cov / 1e6:.1f}" == "11.7")
check("r(price, age) = -0.07", f"{r_age:.2f}" == "-0.07")
check("slope 73.77, intercept 115,017", f"{b2:.2f}" == "73.77" and round(b1) == 115017)
check("slope = cov / var(size)", math.isclose(b2, cov / size.var()))
check("slope in thousands of dollars = 0.07377", f"{b2 / 1000:.5f}" == "0.07377")
check("E12: 600 x 73.77 = 44,262; 73.77 x 2,100 = 154,917; pred(2,100) = 269,934; 44,262 + 115,017 = 159,279",
      (round(600 * 73.77), round(73.77 * 2100), round(pred(2100)), 44262 + 115017) == (44262, 154917, 269934, 159279))
check("intercept-only regression = mean price $253,910",
      round(pf.feols("price ~ 1", data=d).coef()["Intercept"]) == 253910)
check("line passes through (mean size, mean price)", math.isclose(b1 + b2 * size.mean(), price.mean()))
check("R2 = 0.617 (61.7%)", f"{r2:.3f}" == "0.617")
check("R2(price ~ bedrooms) = 0.18", f"{r2_bed:.2f}" == "0.18")
check("s_e = $23,551", round(s_e) == 23551)
check("output row: SE 11.17, t 6.60, CI 50.84 to 96.70",
      (f"{se_b2:.2f}", f"{t_b2:.2f}", f"{ci[0]:.2f}", f"{ci[1]:.2f}") == ("11.17", "6.60", "50.84", "96.70"))
check("E23: pred(2,500) = 299,442; 73.77 x 2,500 = 184,425; 184,425 - 115,017 = 69,408",
      (round(pred(2500)), round(73.77 * 2500), round(73.77 * 2500) - 115017) == (299442, 184425, 69408))
check("E23 distractor: 115,017 + 73.77 = 115,091 (size of 1)", round(115017 + 73.77) == 115091)
check("P27: roughly a third of residuals exceed s_e (10 of 29)", round(100 * (np.abs(u) > s_e).mean()) == 34)
check("P23: 1,250 + 960 = 2,210", 1250 + 960 == 2210)
check("E24: pred(5,000) = 483,867", round(pred(5000)) == 483867)
check("E25: 2,400 sq ft house sold for $340,000; pred(2,400) = 292,065; residual +47,935",
      ((size == 2400) & (price == 340000)).sum() == 1 and round(pred(2400)) == 292065 and 340000 - 292065 == 47935)
check("E26: exactly one |std resid| > 2, at ~2.04", (std_resid.abs() > 2).sum() == 1 and f"{std_resid.abs().max():.2f}" == "2.04")
check("E28: reverse slope ~0.0084; r x sy/sx = 73.8 (with 398); 1/73.77 = 0.0136",
      (f"{c2:.4f}", f"{0.7858 * 398 / 37391:.4f}", f"{0.7858 * 37391 / 398:.1f}", f"{1 / 73.77:.4f}") == ("0.0084", "0.0084", "73.8", "0.0136"))
check("E30: 200 x 73.77 = 14,754", round(200 * 73.77) == 14754)
check("E31: reverse R2 = 0.617 (same); r = 0.786; 1/0.617 = 1.62",
      f"{r2_rev:.3f}" == "0.617" and f"{1 / 0.617:.2f}" == "1.62" and f"{r:.3f}" == "0.786")
check("mean size 1,883 sq ft", round(size.mean()) == 1883)

check("explanations: s_e ~9% of mean price; ~38% unexplained; reverse slope 0.00837; CI ~$51 to ~$97; residual ~$47,900",
      round(100 * s_e / price.mean()) == 9 and round(100 * (1 - r2)) == 38 and f"{c2:.5f}" == "0.00837"
      and (round(ci[0]), round(ci[1])) == (51, 97) and round(resid.max(), -2) == 47900)
check("P02 explanation: 20/60 ~33%; P06: 0.35^2 ~0.12", round(100 * 20 / 60) == 33 and f"{0.35 ** 2:.2f}" == "0.12")

check("E34: LOWESS stays within ~$14,000 of the OLS line (< s_e)", round(lw_gap.max(), -3) == 14000 and lw_gap.max() < s_e)
check("E32: slope highly significant (p < 0.001)", m.pvalue()["size"] < 0.001)
check("E19: s_e with divisor n - 1 would be smaller, not larger, than with n - 2", math.sqrt(rss / (n - 1)) < s_e)
check("E21: RSS/TSS ~38% (0.383)", round(100 * rss / tss) == 38 and f"{1 - r2:.3f}" == "0.383")
check("E27: the 3,300 sq ft house sold for $375,000, the highest price", price[i_big] == 375000 == price.max())
check("P10: r^2 = 0.36; P23: 400 + 960 + 400 = 1,760", f"{0.6 ** 2:.2f}" == "0.36" and 400 + 960 + 400 == 1760)

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic)
check("P02: 30/40 = 75%; 30/100 = 30%; 30/50 = 60%; 40/100 = 40%", (30 / 40, 30 / 100, 30 / 50, 40 / 100) == (0.75, 0.30, 0.60, 0.40))
check("P07: covariance 15,000 / 1,000 = 15; x1,000 = 15,000,000; /1,000^2 = 0.015",
      (15000 / 1000, 15000 * 1000, 15000 / 1000 ** 2) == (15, 15000000, 0.015))
check("P09: r = 20/sqrt(50*10) = 0.894; 20/50 = 0.4; 20/10 = 2; 20/500 = 0.04",
      (f"{20 / math.sqrt(500):.3f}", 20 / 50, 20 / 10, 20 / 500) == ("0.894", 0.4, 2.0, 0.04))
check("P12: 4 x 2.5 = 10; 5 + 2.5 x 12 = 35; 5 + 10 = 15", (4 * 2.5, 5 + 2.5 * 12, 5 + 4 * 2.5) == (10, 35, 15))
check("P13: 25 - 0.4 x 10 = 21; 25 + 4 = 29; 25/10 = 2.5", (25 - 0.4 * 10, 25 + 0.4 * 10, 25 / 10) == (21, 29, 2.5))
check("P16: 0.8 x 5 = 4 (thousand dollars); slope in dollars of sales per thousand = 800", (round(0.8 * 5, 6), round(0.8 * 1000)) == (4, 800))
check("P21: ESS = 500 - 125 = 375; R2 = 0.75", (500 - 125, 375 / 500) == (375, 0.75))
check("P23: 400 + 1.2 x 800 = 1,360; 1.2 x 800 = 960; 400 + 1.2 = 401.20", (400 + 1.2 * 800, 1.2 * 800, 400 + 1.2) == (1360, 960, 401.2))
check("P25: 1,300 - 1,360 = -60", 1300 - 1360 == -60)
check("P26: 420/150 = 2.8; 150/420 = 0.36; 420/300 = 1.4; 420 - 150 = 270",
      (420 / 150, f"{150 / 420:.2f}", 420 / 300, 420 - 150) == (2.8, "0.36", 1.4, 270))
check("P28: 0.6 x 10/4 = 1.5; 0.6 x 4/10 = 0.24; 10/4 = 2.5", (0.6 * 10 / 4, round(0.6 * 4 / 10, 6), 10 / 4) == (1.5, 0.24, 2.5))
check("P31: 1/0.9 = 1.11", f"{1 / 0.9:.2f}" == "1.11")
check("P10: Fahrenheit is a positive linear rescaling, so r is unchanged",
      math.isclose(np.corrcoef(1.8 * size + 32, price)[0, 1], r))

# ---------------------------------------------------------------- 3. CLAIMS
check("E01/E07: house 1,400 sq ft at $204,000 is below average in both size and price",
      ((size == 1400) & (price == 204000)).any() and 1400 < size.mean() and 204000 < price.mean())
check("E05: positive direction (r > 0) and prices vary among same-size houses (1,600 sq ft: $212,000-$258,500)",
      r > 0 and (price[size == 1600].min(), price[size == 1600].max()) == (212000, 258500))
check("E05: chapter's nonparametric curves track OLS (LOWESS within s_e of the line everywhere)", lw_gap.max() < s_e)
check("E06: distractor false -- only ~38% of houses sell above the mean price (not 79%)", round(100 * (price > price.mean()).mean()) == 38)
check("E10: positive covariance but some larger house sold for less than some smaller one",
      cov > 0 and any(((size > s0) & (price < p0)).any() for s0, p0 in zip(size, price)))
check("E10: covariance and correlation share the same sign", np.sign(cov) == np.sign(r))
check("E19: s_e < SD of price; some residuals exceed s_e in size (10 houses)",
      s_e < sy and (np.abs(u) > s_e).sum() == 10)
check("E22: every house sold for more than $96.70 per sq ft (min ~$106.90)", (price / size).min() > 96.70)
check("E27: dropping the largest house (3,300 sq ft) cuts the slope from 73.77 to 63.49 (-14%)",
      size[i_big] == 3300 and f"{drop_slopes[i_big]:.2f}" == "63.49" and round(100 * (drop_slopes[i_big] / b2 - 1)) == -14)
check("E27: the largest house has a small standardized residual (~0.7)", f"{std_resid[i_big]:.1f}" == "0.7")
check("E28/E31: reverse slope is not the reciprocal; product of slopes = R2", not math.isclose(c2, 1 / b2) and math.isclose(b2 * c2, r2))
check("E09: |r(price, age)| < 0.3 (weak)", abs(r_age) < 0.3)
check("E18: R2(size) > R2(bedrooms); R2(bedrooms) = r(price, bedrooms)^2", r2 > r2_bed and math.isclose(r2_bed, r_bed ** 2))
check("E13: smallest house 1,400 sq ft (x = 0 far outside the data)", size.min() == 1400)

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
