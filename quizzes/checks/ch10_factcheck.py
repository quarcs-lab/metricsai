#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch10.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Run:  python3 quizzes/checks/ch10_factcheck.py      (exit 1 on any failure)

Note: AED_HOUSE stores bedrooms, lotsize, and monthsold as int8 and size as int16;
the data are cast to float before any arithmetic (1553 * int8 overflows).
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
from statsmodels.stats.outliers_influence import variance_inflation_factor

warnings.filterwarnings("ignore")

CHAPTER = "ch10"
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


def f3(x: float) -> str:
    return f"{x:.3f}"


def stata_ic(m):
    n_obs, n_par = int(m._N), len(m.coef())
    rss_m = float(np.sum(m._u_hat ** 2))
    const = n_obs * (1 + np.log(2 * np.pi))
    return (n_obs * np.log(rss_m / n_obs) + const + 2 * n_par,
            n_obs * np.log(rss_m / n_obs) + const + n_par * np.log(n_obs), rss_m)


# ---------------------------------------------------------------- 1. FACTS
d = load("AED_HOUSE.DTA").astype(float)
n = len(d)
REGS = ["size", "bedrooms", "bathrooms", "lotsize", "age", "monthsold"]
corr = d[["price"] + REGS].corr()

m_bed = pf.feols("price ~ bedrooms", data=d)
m_two = pf.feols("price ~ bedrooms + size", data=d)
m_size = pf.feols("price ~ size", data=d)
m_full = pf.feols("price ~ " + " + ".join(REGS), data=d)
cf, sef, ci = m_full.coef(), m_full.se(), m_full.confint()
k = len(cf)
rss = float(np.sum(m_full._u_hat ** 2))
tss = float(((d["price"] - d["price"].mean()) ** 2).sum())
s_e = math.sqrt(rss / (n - k))
aic_s, bic_s, rss_s = stata_ic(m_size)
aic_f, bic_f, _ = stata_ic(m_full)

# FWL
m_aux = pf.feols("size ~ bedrooms + bathrooms + lotsize + age + monthsold", data=d)
d["resid_size"] = np.asarray(m_aux._u_hat)
m_fwl = pf.feols("price ~ resid_size", data=d)

# VIF (chapter's method, with the intercept column)
X = d[REGS].copy()
X.insert(0, "const", 1.0)
vif = {v: variance_inflation_factor(X.values, i) for i, v in enumerate(REGS, start=1)}
r2_bed_aux = pf.feols("bedrooms ~ size + bathrooms + lotsize + age + monthsold", data=d)._r2

print(f"FACTS n={n} k={k} mean price={d['price'].mean():.2f} sd price={d['price'].std():.2f} mean size={d['size'].mean():.2f}")
print("FACTS corr:\n" + corr.round(4).to_string())
print(f"FACTS price~bedrooms: b={m_bed.coef()['bedrooms']:.4f} R2={m_bed._r2:.4f}")
print(f"FACTS price~bedrooms+size: {m_two.coef().round(4).to_dict()} t_bed={m_two.tstat()['bedrooms']:.4f} p_bed={m_two.pvalue()['bedrooms']:.4f}")
print(f"FACTS price~size: {m_size.coef().round(4).to_dict()} R2={m_size._r2:.6f} adjR2={m_size._adj_r2:.6f}")
print(f"FACTS full: {cf.round(4).to_dict()}")
print(f"FACTS full t: {m_full.tstat().round(4).to_dict()}")
print("FACTS full CI:\n" + ci.round(4).to_string())
print(f"FACTS full R2={m_full._r2:.6f} adjR2={m_full._adj_r2:.6f} RSS={rss:.1f} TSS={tss:.1f} s_e={s_e:.4f} corr(y,yhat)={np.corrcoef(d['price'], m_full.predict())[0, 1]:.6f}")
print(f"FACTS IC: size-only AIC={aic_s:.4f} BIC={bic_s:.4f}; full AIC={aic_f:.4f} BIC={bic_f:.4f}; ln29={math.log(29):.4f}")
print(f"FACTS FWL: aux R2={m_aux._r2:.6f} fwl coef={m_fwl.coef()['resid_size']:.10f} full size={cf['size']:.10f}")
print(f"FACTS VIF: { {k_: round(v, 4) for k_, v in vif.items()} } R2 bedrooms aux={r2_bed_aux:.6f}")
print()

# ---------------------------------------------------------------- 2. CHECKS (exam)
check("29 houses, k = 7 parameters in the full model", n == 29 and k == 7)
check("E01/E02: bivariate bedrooms 23,667 -> 1,553 with size", round(m_bed.coef()["bedrooms"]) == 23667 and round(m_two.coef()["bedrooms"]) == 1553)
check("E01 explanation: r(size, bedrooms) = 0.52", f2(corr.loc["size", "bedrooms"]) == "0.52")
check("E02: size coef 73.77 alone, 72.41 with bedrooms; shift 1.36", (f2(m_size.coef()["size"]), f2(m_two.coef()["size"]), f2(73.77 - 72.41)) == ("73.77", "72.41", "1.36"))
check("E02: bedrooms t = 0.20 in the two-regressor model", f2(m_two.tstat()["bedrooms"]) == "0.20")
check("E02: OVB identity 23,667 = 1,553 + 72.41 x slope(size on bedrooms)",
      abs(m_bed.coef()["bedrooms"] - (m_two.coef()["bedrooms"] + m_two.coef()["size"] * pf.feols("size ~ bedrooms", data=d).coef()["bedrooms"])) < 1e-6)
check("E02: and 73.77 = 72.41 + 1,553 x slope(bedrooms on size)",
      abs(m_size.coef()["size"] - (m_two.coef()["size"] + m_two.coef()["bedrooms"] * pf.feols("bedrooms ~ size", data=d).coef()["size"])) < 1e-6)
check("E05: r(price, age) = -0.07", f2(corr.loc["price", "age"]) == "-0.07")
check("E06 D: r(price, monthsold) = -0.21", f2(corr.loc["price", "monthsold"]) == "-0.21")
check("E06: matrix symmetric with unit diagonal", np.allclose(corr.values, corr.values.T) and np.allclose(np.diag(corr.values), 1))
check("E07: r(price,size)=0.79, r(price,bedrooms)=0.43, r(age,monthsold)=-0.37",
      (f2(corr.loc["price", "size"]), f2(corr.loc["price", "bedrooms"]), f2(corr.loc["age", "monthsold"])) == ("0.79", "0.43", "-0.37"))
check("E06/E07: 7 x 7 matrix", corr.shape == (7, 7))
check("E10: 200 x 68.37 = 13,674; 200 x 73.77 = 14,754; + intercept 137,791 = 151,465",
      (f2(cf["size"]), round(200 * 68.37), round(200 * 73.77), round(cf["Intercept"]), round(round(cf["Intercept"]) + 200 * 68.37)) == ("68.37", 13674, 14754, 137791, 151465))
check("E11: CIs size [36.45, 100.29], bedrooms [-16,379, 21,749], age [-2,325, 659]",
      (f2(ci.loc["size"].iloc[0]), f2(ci.loc["size"].iloc[1])) == ("36.45", "100.29")
      and (round(ci.loc["bedrooms"].iloc[0]), round(ci.loc["bedrooms"].iloc[1])) == (-16379, 21749)
      and (round(ci.loc["age"].iloc[0]), round(ci.loc["age"].iloc[1])) == (-2325, 659))
check("E11 E: 90 inside the size interval", ci.loc["size"].iloc[0] < 90 < ci.loc["size"].iloc[1])
check("E13: lot size coefficient 2,303; coded 1/2/3", round(cf["lotsize"]) == 2303 and sorted(d["lotsize"].unique()) == [1.0, 2.0, 3.0])
check("E14: bathrooms 6,833 ~ 100 x 68.37", round(cf["bathrooms"]) == 6833 and round(6833 / 68.37) == 100)
check("E15: 111,691 + 1,553 x 4 + 72.41 x 2,000 = 262,723; residual -18,723; 1,553 x 4 = 6,212; 72.41 x 2,000 = 144,820",
      (round(m_two.coef()["Intercept"]), round(111691 + 1553 * 4 + 72.41 * 2000), 244000 - 262723, 1553 * 4, round(72.41 * 2000))
      == (111691, 262723, -18723, 6212, 144820))
check("E15: a house with 4 bedrooms, 2,000 sq ft sold for $244,000",
      ((d["bedrooms"] == 4) & (d["size"] == 2000) & (d["price"] == 244000)).any())
check("E15 D: 244,000 - mean price 253,910 = -9,910", round(d["price"].mean()) == 253910 and 244000 - 253910 == -9910)
check("E16 D: mean size 1,883", round(d["size"].mean()) == 1883)
check("E17: FWL coefficient equals full-model size coefficient", abs(m_fwl.coef()["resid_size"] - cf["size"]) < 1e-8)
check("E18: aux R2 = 0.41 -> 59%; 1 - 0.41^2 = 83%", f2(m_aux._r2) == "0.41" and round(100 * (1 - 0.41)) == 59 and round(100 * (1 - 0.41 ** 2)) == 83)
check("E19: full R2 = 0.651", f3(m_full._r2) == "0.651")
check("E20: RSS 13.68 bn, TSS 39.15 bn", (f2(rss / 1e9), f2(tss / 1e9)) == ("13.68", "39.15"))
check("E20: adj R2 = 0.555 (exact and from rounded inputs)",
      f3(m_full._adj_r2) == "0.555" and f3(1 - (13.68 / 22) / (39.15 / 28)) == "0.555")
check("E20 distractors: R2 0.651; k=6 -> 0.575; inverted df ratio -> 0.725",
      (f3(1 - 13.68 / 39.15), f3(1 - (13.68 / 23) / (39.15 / 28)), f3(1 - (13.68 / 39.15) * 22 / 28)) == ("0.651", "0.575", "0.725"))
check("E20 key feedback: 13.68/22 = 0.622, 39.15/28 = 1.398", (f3(13.68 / 22), f3(39.15 / 28)) == ("0.622", "1.398"))
# E21: R2 never falls; adjusted R2 can fall (demonstrate with random regressors)
rng = np.random.default_rng(10)
falls, r2_ok = 0, True
for _ in range(200):
    d["noise"] = rng.normal(size=n)
    m_n = pf.feols("price ~ " + " + ".join(REGS) + " + noise", data=d)
    r2_ok &= m_n._r2 >= m_full._r2 - 1e-12
    falls += m_n._adj_r2 < m_full._adj_r2
check("E21: adding a random regressor never lowers R2; adjusted R2 falls in some draws", r2_ok and falls > 0)
coef_nonzero, se_rises, adj_below = True, 0, True
rng2 = np.random.default_rng(11)
for _ in range(200):
    d["noise"] = rng2.normal(size=n)
    m_n = pf.feols("price ~ " + " + ".join(REGS) + " + noise", data=d)
    coef_nonzero &= m_n.coef()["noise"] != 0
    s_n = math.sqrt(float(np.sum(m_n._u_hat ** 2)) / (n - len(m_n.coef())))
    se_rises += s_n > s_e
    adj_below &= m_n._adj_r2 < m_n._r2
check("E21 C false: the random regressor's coefficient is never exactly zero", coef_nonzero)
check("E21 E false: s_e rises in some draws although RSS cannot rise", se_rises > 0)
check("E21 B false: adjusted R2 stays below R2 in the expanded model", adj_below)
check("E22: s_e = 24,936", round(s_e) == 24936)
check("E22 explanation: mean price ~ 253,910", round(d["price"].mean()) == 253910)
check("E23: AIC/BIC size-only 668.1/670.8, full 675.5/685.1",
      (f"{aic_s:.1f}", f"{bic_s:.1f}", f"{aic_f:.1f}", f"{bic_f:.1f}") == ("668.1", "670.8", "675.5", "685.1"))
check("E24: ln 29 = 3.37; ln n > 2 iff n >= 8", f2(math.log(29)) == "3.37" and math.log(8) > 2 > math.log(7))
check("E26: size coef change 73.77 -> 68.37 is 5.40, about 7% (< 10%)",
      f2(73.77 - 68.37) == "5.40" and round(100 * (73.77 - 68.37) / 73.77) == 7)
check("E26: R2 0.617 -> 0.651 (rise ~0.03); adj 0.603 -> 0.555",
      (f3(m_size._r2), f3(m_full._r2), f2(m_full._r2 - m_size._r2), f3(m_size._adj_r2), f3(m_full._adj_r2))
      == ("0.617", "0.651", "0.03", "0.603", "0.555"))
d["size_twice"] = 2 * d["size"]
m_col = pf.feols("price ~ size + size_twice + bedrooms", data=d)
check("E27: size_twice dropped; remaining estimates match price ~ bedrooms + size",
      "size_twice" not in m_col.coef().index and np.allclose(m_col.coef()[["size", "bedrooms"]].values, m_two.coef()[["size", "bedrooms"]].values))
check("E28: bedrooms aux R2 = 0.423, VIF 1.73 (exact and from 0.423)",
      f3(r2_bed_aux) == "0.423" and f2(vif["bedrooms"]) == "1.73" and f2(1 / (1 - 0.423)) == "1.73" and f3(1 - 0.423) == "0.577")
check("E28 distractors: 1 - R2 = 0.58; 1/R2 = 2.36; 1/(1 - R2^2) = 1.22",
      (f2(1 - 0.423), f2(1 / 0.423), f2(1 / (1 - 0.423 ** 2))) == ("0.58", "2.36", "1.22"))

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic, hypothetical)
check("P04: 5 variables -> 10 pairs; 25 cells; 20 ordered", (5 * 4 // 2, 5 * 5, 5 * 4) == (10, 25, 20))
check("P05 A feedback: (-0.80)^2 = 0.64", f2((-0.80) ** 2) == "0.64")
check("P10: 3 x 1.2 = 3.60; +5 = 8.60; 3 x 1.6 = 4.80", (f2(3 * 1.2), f2(5 + 3 * 1.2), f2(3 * (1.2 + 0.4))) == ("3.60", "8.60", "4.80"))
check("P13: 2 x 5,000 = 10,000; 3 x 5,000 = 15,000; 5,000/3 = 1,667", (2 * 5000, 3 * 5000, round(5000 / 3)) == (10000, 15000, 1667))
check("P14: 0.4 + 1.2 = 1.60", f2(0.4 + 1.2) == "1.60")
check("P15: yhat = 12, residual -3", (2 + 3 * 2 + 4 * 1, 9 - 12) == (12, -3))
check("P18: 1 - 0.90 = 10%; sqrt(0.10) = 32%", round(100 * (1 - 0.90)) == 10 and round(100 * math.sqrt(0.10)) == 32)
check("P20: R2 0.640; adj 0.610 (k=5), 0.618 (n-4), 0.603 (TSS/n); smaller model 0.592; 18/48 = 0.375; 50/52 = 0.962",
      (f3(1 - 18 / 50), f3(1 - (18 / 48) / (50 / 52)), f3(1 - (18 / 49) / (50 / 52)), f3(1 - (18 / 48) / (50 / 53)),
       f3(1 - (20 / 51) / (50 / 52)), f3(18 / 48), f3(50 / 52)) == ("0.640", "0.610", "0.618", "0.603", "0.592", "0.375", "0.962"))
check("P21 A: adjusted R2 <= R2 when k >= 2 (illustration)", all(1 - (1 - r) * (52) / (53 - kk) <= r for r in (0.1, 0.5, 0.9) for kk in (2, 5)))
check("P21 C: adjusted R2 can be negative (R2 = 0.05, n = 20, k = 6)", 1 - (1 - 0.05) * 19 / 14 < 0)
check("P22: sqrt(20/51) = 0.63; sqrt(20/53) = 0.61; 20/51 = 0.39; 20/53 = 0.38",
      (f2(math.sqrt(20 / 51)), f2(math.sqrt(20 / 53)), f2(20 / 51), f2(20 / 53)) == ("0.63", "0.61", "0.39", "0.38"))
pen = math.log(500) - 2
check("P23: internally consistent (A: k=4, B: k=6 with n=500); AIC favors B, BIC favors A; ln 500 = 6.2",
      f"{1512.4 + 4 * pen:.1f}" == "1529.3" and f"{1509.8 + 6 * pen:.1f}" == "1535.1"
      and 1509.8 < 1512.4 and 1529.3 < 1535.1 and f"{math.log(500):.1f}" == "6.2")
check("P25: n = 200, adj 0.475 (k=3) and 0.468 (k=9); R2 rise 0.009",
      (f3(1 - 0.52 * 199 / 197), f3(1 - 0.511 * 199 / 191), f3(0.489 - 0.480)) == ("0.475", "0.468", "0.009"))
bic_diff = 1000 * math.log(0.74 / 0.80) + 4 * math.log(1000)
check("P26: n = 1,000 adj 0.199 and 0.256; BIC 5,210 -> 5,160 (consistent with R2 change)",
      (f3(1 - 0.8 * 999 / 998), f3(1 - 0.74 * 999 / 994), round(5210 + bic_diff, -1)) == ("0.199", "0.256", 5160))
check("P28: VIF 1/(1-0.75) = 4.0; 0.75/0.25 = 3.0; 1-0.75 = 0.25; 1+0.75 = 1.75",
      (f"{1 / (1 - 0.75):.1f}", f"{0.75 / 0.25:.1f}", f2(1 - 0.75), f2(1 + 0.75)) == ("4.0", "3.0", "0.25", "1.75"))
check("P29: sqrt(16) = 4", math.sqrt(16) == 4)
check("P30: bedrooms has the largest hypothetical VIF; all four exceed 10", max({"size": 40.1, "bedrooms": 57.8, "bathrooms": 34.7, "age": 21.0}.items(), key=lambda kv: kv[1])[0] == "bedrooms" and min(40.1, 57.8, 34.7, 21.0) > 10)

# ---------------------------------------------------------------- 3. CLAIMS
check("CLAIM E01/E08: houses with more bedrooms tend to be larger (r > 0.5)", corr.loc["size", "bedrooms"] > 0.5)
check("CLAIM E05: older houses sold for slightly less (r(price, age) negative, |r| < 0.1)", -0.1 < corr.loc["price", "age"] < 0)
check("CLAIM E06 C false: bathrooms correlate less with price than bedrooms, yet get the larger coefficient",
      corr.loc["price", "bathrooms"] < corr.loc["price", "bedrooms"] and cf["bathrooms"] > cf["bedrooms"])
offdiag = {(a, b): abs(corr.loc[a, b]) for i, a in enumerate(REGS) for b in REGS[i + 1:]}
check("CLAIM E07: size-bedrooms is the strongest correlation between two regressors", max(offdiag, key=offdiag.get) == ("size", "bedrooms"))
check("CLAIM E07: price-size is the strongest correlation with price", corr["price"].drop("price").abs().idxmax() == "size")
check("CLAIM E11/E14: size is the only regressor whose 95% CI excludes zero",
      [v for v in REGS if ci.loc[v].iloc[0] > 0 or ci.loc[v].iloc[1] < 0] == ["size"])
check("CLAIM E11 A: age estimate negative but CI includes 0", cf["age"] < 0 and ci.loc["age"].iloc[0] < 0 < ci.loc["age"].iloc[1])
check("CLAIM E11 C: bedrooms CI includes 0", ci.loc["bedrooms"].iloc[0] < 0 < ci.loc["bedrooms"].iloc[1])
check("CLAIM E26 B premise: none of the five added regressors is significant at 5% in the full model",
      all(ci.loc[v].iloc[0] < 0 < ci.loc[v].iloc[1] for v in REGS if v != "size"))
check("CLAIM E10 stem: full-model intercept 137,791", round(cf["Intercept"]) == 137791)
check("CLAIM E12: size coefficient smaller with the five controls (68.37 < 73.77)", cf["size"] < m_size.coef()["size"])
check("CLAIM E13: lot size coefficient not significant", ci.loc["lotsize"].iloc[0] < 0 < ci.loc["lotsize"].iloc[1])
check("CLAIM E14: size coefficient is the smallest in absolute value among slopes", cf.drop("Intercept").abs().idxmin() == "size")
check("CLAIM E02: with size fixed, bedrooms coefficient small and insignificant (|t| < 1)", abs(m_two.tstat()["bedrooms"]) < 1)
check("CLAIM E16 D false: FWL residuals differ from size minus its mean", not np.allclose(d["resid_size"], d["size"] - d["size"].mean()))
check("CLAIM E15: model over-predicts that house (residual negative)", 244000 < 111691 + 1553 * 4 + 72.41 * 2000)
check("CLAIM E28 explanation / chapter: all VIFs below 2", max(vif.values()) < 2)
check("CLAIM E28: bedrooms VIF = 1/(1 - R2 of bedrooms on the others)", abs(vif["bedrooms"] - 1 / (1 - r2_bed_aux)) < 1e-9)
check("CLAIM R2 = corr(y, yhat)^2 in the full model (P21 E)", abs(np.corrcoef(d["price"], m_full.predict())[0, 1] ** 2 - m_full._r2) < 1e-9)
check("CLAIM E23: size-only model has smaller AIC and BIC", aic_s < aic_f and bic_s < bic_f)
check("CLAIM chapter p = 0.85 for bedrooms (two-regressor): exact p rounds to 0.84 (reported contradiction)", f2(m_two.pvalue()["bedrooms"]) == "0.84")
check("CLAIM monthsold covers months 3-8 only", (d["monthsold"].min(), d["monthsold"].max()) == (3.0, 8.0))

# ---------------------------------------------------------------- report
bank = json.loads((ROOT / "quizzes" / "banks" / f"{CHAPTER}.json").read_text(encoding="utf-8"))
for label, ok in checks.items():
    print(("OK  " if ok else "FAIL"), label)
nums = set()
for s in ("practice", "exam"):
    for item in bank[s]:
        blob = json.dumps({k_: v for k_, v in item.items() if k_ != "id"}, ensure_ascii=False)
        nums.update(x.rstrip(".,") for x in re.findall(r"\d[\d,]*\.?\d*", blob))
print("\nNumbers quoted in the bank (each must trace to a check above or be self-evident):")
print(", ".join(sorted(nums, key=lambda x: float(x.replace(",", "") or 0))))
failed = [k_ for k_, ok in checks.items() if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
sys.exit(1 if failed or not checks else 0)
