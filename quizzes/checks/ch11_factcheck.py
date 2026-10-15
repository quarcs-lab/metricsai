#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch11.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Run:  python3 quizzes/checks/ch11_factcheck.py      (exit 1 on any failure)
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

CHAPTER = "ch11"
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


def tcrit(p: float, df: int) -> float:
    return stats.t.ppf(p, df)


# ---------------------------------------------------------------- 1. FACTS
d = load("AED_HOUSE.DTA")
n = len(d)
FULL = "price ~ size + bedrooms + bathrooms + lotsize + age + monthsold"
m = pf.feols(FULL, data=d)
rb = pf.feols(FULL, data=d, vcov="HC1")
m1 = pf.feols("price ~ size", data=d)
m2 = pf.feols("price ~ size + bedrooms", data=d)
k = len(m.coef())
df = n - k
b, se, tt, pv = m.coef(), m.se(), m.tstat(), m.pvalue()
ci = m.confint()
rse, rp = rb.se(), rb.pvalue()
rss_u = float((m._u_hat ** 2).sum())
rss_r = float((m1._u_hat ** 2).sum())
tss = float(((d["price"] - d["price"].mean()) ** 2).sum())
ess = tss - rss_u
s_e = math.sqrt(rss_u / df)
s_e1 = math.sqrt(rss_r / (n - 2))
q_sub = k - 2
F_sub = ((rss_r - rss_u) / q_sub) / (rss_u / df)
p_sub = stats.f.sf(F_sub, q_sub, df)
F_all = (m._r2 / (k - 1)) / ((1 - m._r2) / df)
p_all = stats.f.sf(F_all, k - 1, df)
c95, c90, c99 = tcrit(0.975, df), tcrit(0.95, df), tcrit(0.995, df)
c95_27 = tcrit(0.975, n - 2)
aux = pf.feols("size ~ bedrooms + bathrooms + lotsize + age + monthsold", data=d)
corr = d[["price", "size", "bedrooms", "bathrooms", "lotsize", "age", "monthsold"]].corr()


def t_null(c: float) -> float:
    return (b["size"] - c) / se["size"]


print(f"FACTS n={n} k={k} df={df}  R2={m._r2:.4f} adjR2={m._adj_r2:.4f} s_e={s_e:.2f}")
print(pd.DataFrame({"b": b, "se": se, "t": tt, "p": pv, "lo": ci.iloc[:, 0], "hi": ci.iloc[:, 1],
                    "rse": rse, "rp": rp, "pct": 100 * (rse / se - 1)}).round(4).to_string())
print(f"FACTS crit t22: .975={c95:.4f} .95={c90:.4f} .995={c99:.4f}; t27 .975={c95_27:.4f}")
print(f"FACTS F overall={F_all:.4f} p={p_all:.6f} crit={stats.f.ppf(.95, k - 1, df):.4f}")
print(f"FACTS F subset={F_sub:.4f} p={p_sub:.4f} crit={stats.f.ppf(.95, q_sub, df):.4f} RSSr={rss_r:,.0f} RSSu={rss_u:,.0f} TSS={tss:,.0f} ESS={ess:,.0f}")
for name, mm in (("M1", m1), ("M2", m2), ("M3", m)):
    print(f"FACTS {name}: b_size={mm.coef()['size']:.4f} se={mm.se()['size']:.4f} R2={mm._r2:.4f} adj={mm._adj_r2:.4f}")
print(f"FACTS s_e size-only={s_e1:.2f}; R2(size on others)={aux._r2:.4f}")
for c in (0, 30, 50, 60, 100, 105):
    print(f"FACTS null {c}: t={t_null(c):.4f} |t|>crit={abs(t_null(c)) > c95}")
print(corr.round(3).to_string())
print()

# ---------------------------------------------------------------- 2. CHECKS (exam)
check("29 houses; full model k = 7, n - k = 22; six regressors", n == 29 and k == 7 and df == 22)
check("E01: r(age, monthsold) = -0.37; lot size takes three values (1, 2, 3)",
      f2(corr.loc["age", "monthsold"]) == "-0.37" and sorted(d["lotsize"].unique().tolist()) == [1, 2, 3])
check("E04/E10/E16: b_size = 68.37, se = 15.39", (f2(b["size"]), f2(se["size"])) == ("68.37", "15.39"))
check("E07: size-only b = 73.77, se = 11.17; full se 15.39",
      (f2(m1.coef()["size"]), f2(m1.se()["size"])) == ("73.77", "11.17"))
check("E08: t crit 2.052 (size only, 27 df) and 2.074 (full, 22 df)", (f"{c95_27:.3f}", f"{c95:.3f}") == ("2.052", "2.074"))
check("E09: root MSE of full model = $24,936", round(s_e) == 24936)
check("E10: 90% crit 1.717; shown factors 1.717 x 15.39 = 26.42 -> [41.95, 94.79]",
      f"{c90:.3f}" == "1.717" and f2(1.717 * 15.39) == "26.42"
      and (f2(68.37 - 26.42), f2(68.37 + 26.42)) == ("41.95", "94.79"))
check("E10: exact 90% CI [41.94, 94.80] differs only in the last digit (bank uses shown factors)",
      (f2(b["size"] - c90 * se["size"]), f2(b["size"] + c90 * se["size"])) == ("41.94", "94.80"))
check("E10 distractors: +/- 13.21 (half margin) = [55.16, 81.58]; +/- 15.39 = [52.98, 83.76]; +/- 1.717 = [66.65, 70.09]",
      f2(26.42 / 2) == "13.21" and (f2(68.37 - 13.21), f2(68.37 + 13.21)) == ("55.16", "81.58")
      and (f2(68.37 - 15.39), f2(68.37 + 15.39)) == ("52.98", "83.76")
      and (f2(68.37 - 1.717), f2(68.37 + 1.717)) == ("66.65", "70.09"))
check("E10 distractors all lie inside the 95% CI [36.45, 100.29] (no elimination by E12/E13)",
      all(36.45 < v < 100.29 for v in (55.16, 81.58, 52.98, 83.76, 66.65, 70.09, 41.95, 94.79)))
check("E11/E20: bedrooms b = 2,685, se = 9,193, p = 0.773",
      (round(b["bedrooms"]), round(se["bedrooms"]), f"{pv['bedrooms']:.3f}") == (2685, 9193, "0.773"))
check("E11: 2,685 +/- 2 x 9,193 = [-15,701, 21,071]", (2685 - 2 * 9193, 2685 + 2 * 9193) == (-15701, 21071))
check("E11 distractors: +/- 9,193 = [-6,508, 11,878]; +/- 2 x 9,193/sqrt(29) = [-729, 6,099]; +/- 4 x 9,193 = [-34,087, 39,457]",
      (2685 - 9193, 2685 + 9193) == (-6508, 11878) and (round(2685 - 2 * 9193 / math.sqrt(29)), round(2685 + 2 * 9193 / math.sqrt(29))) == (-729, 6099)
      and (2685 - 4 * 9193, 2685 + 4 * 9193) == (-34087, 39457))
check("E11: all four candidate intervals contain zero", all(lo < 0 < hi for lo, hi in ((-15701, 21071), (-6508, 11878), (-729, 6099), (-34087, 39457))))
check("E12/E13: 95% CI for size [36.45, 100.29]", (f2(ci.loc["size"].iloc[0]), f2(ci.loc["size"].iloc[1])) == ("36.45", "100.29"))
check("E13: nulls 0, 30, 105 rejected; 60, 100 not (exact t vs 2.074)",
      all(abs(t_null(c)) > c95 for c in (0, 30, 105)) and all(abs(t_null(c)) < c95 for c in (60, 100)))
check("E13: same split by the CI (0, 30, 105 outside; 60, 100 inside)",
      all(not (ci.loc["size"].iloc[0] < c < ci.loc["size"].iloc[1]) for c in (0, 30, 105))
      and all(ci.loc["size"].iloc[0] < c < ci.loc["size"].iloc[1] for c in (60, 100)))
check("E14: every 95% CI containing zero also contains zero at 99% (99% crit > 95% crit)",
      c99 > c95 and all((b[v] - c99 * se[v]) < 0 < (b[v] + c99 * se[v]) for v in b.index if ci.loc[v].iloc[0] < 0 < ci.loc[v].iloc[1]))
check("E15/E18: age b = -833, se = 719", (round(b["age"]), round(se["age"])) == (-833, 719))
check("E16: (68.37-50)/15.39 = 1.19; 68.37/15.39 = 4.44; 15.39/18.37 = 0.84; (68.37-50)/68.37 = 0.27",
      (f2((68.37 - 50) / 15.39), f2(68.37 / 15.39), f2(15.39 / (68.37 - 50)), f2((68.37 - 50) / 68.37)) == ("1.19", "4.44", "0.84", "0.27"))
check("E16: exact t for null 50 = 1.19", f2(t_null(50)) == "1.19")
check("E17/E34: size p = 0.0002 (classical) and robust p < 0.01", f"{pv['size']:.4f}" == "0.0002" and rp["size"] < 0.01)
check("E18: |t_age| = 1.16 < 2.074", abs(tt["age"]) < c95 and f2(abs(tt["age"])) == "1.16")
check("E23: overall F = 6.83, p = 0.0003; only size significant among slopes",
      f2(F_all) == "6.83" and f"{p_all:.4f}" == "0.0003"
      and [v for v in b.index if v != "Intercept" and pv[v] < 0.05] == ["size"])
check("E24: overall F ~ F(6, 22)", (k - 1, df) == (6, 22) and n - 6 == 23)
check("E27: RSS_r = 14,975 million, RSS_u = 13,679 million; 7 parameters, 29 houses, q = 5",
      (round(rss_r / 1e6), round(rss_u / 1e6)) == (14975, 13679) and (k, n, q_sub) == (7, 29, 5))
check("E27: F = (1,296/5)/(13,679/22) = 259.2/621.8 = 0.42 (shown numbers) and exact subset F = 0.42",
      14975 - 13679 == 1296 and f"{1296 / 5:.1f}" == "259.2" and f"{13679 / 22:.1f}" == "621.8"
      and f2((1296 / 5) / (13679 / 22)) == "0.42" and f2(F_sub) == "0.42")
check("E27 distractors: n - k_r = 27 -> 0.51; q = 6 -> 0.35; RSS_r in denominator -> 0.38",
      (f2((1296 / 5) / (13679 / 27)), f2((1296 / 6) / (13679 / 22)), f2((1296 / 5) / (14975 / 22))) == ("0.51", "0.35", "0.38"))
check("E27 explanation: F(5, 22) 5% critical value 2.66", f2(stats.f.ppf(0.95, q_sub, df)) == "2.66" and q_sub == 5)
check("E28: R2 unchanged gives F = 0 in the R2 form", ((0.5 - 0.5) / 5) / ((1 - 0.5) / 22) == 0)
check("E29: subset p = 0.83 (not rejected at 5%)", f2(p_sub) == "0.83" and p_sub > 0.05)
check("E30: TSS unchanged across models (depends only on price); RSS falls 14,975 -> 13,679 million; ESS rises",
      abs(((m1._u_hat ** 2).sum() + ((m1.predict() - d["price"].mean()) ** 2).sum()) - tss) / tss < 1e-9
      and rss_u < rss_r and ess > tss - rss_r)
check("E31: intercept p = 0.035 -> ** (0.01 <= p < 0.05)", f"{pv['Intercept']:.3f}" == "0.035" and 0.01 <= pv["Intercept"] < 0.05)
check("E32: R2 0.617/0.618/0.651, adj R2 0.603/0.589/0.555",
      tuple(f"{mm._r2:.3f}" for mm in (m1, m2, m)) == ("0.617", "0.618", "0.651")
      and tuple(f"{mm._adj_r2:.3f}" for mm in (m1, m2, m)) == ("0.603", "0.589", "0.555"))
check("E32: Model 1 highest adj R2, lowest R2; Model 2 lower RSS than Model 1",
      m1._adj_r2 > max(m2._adj_r2, m._adj_r2) and m1._r2 < min(m2._r2, m._r2)
      and (m2._u_hat ** 2).sum() < (m1._u_hat ** 2).sum())
check("E34 A false: size t 4.44 -> 4.45 (robust)", (f2(tt["size"]), f2(rb.tstat()["size"])) == ("4.44", "4.45"))
check("E34: robust SE smaller than classical for size (not larger for every coefficient)", rse["size"] < se["size"])
check("E34: coefficient estimates identical under HC1", np.allclose(rb.coef().values, b.values))
check("E34: intercept SE +6.6% vs size -0.2% (larger % change for intercept)",
      (f"{100 * (rse['Intercept'] / se['Intercept'] - 1):.1f}", f"{100 * (rse['size'] / se['size'] - 1):.1f}") == ("6.6", "-0.2")
      and abs(rse["Intercept"] / se["Intercept"] - 1) > abs(rse["size"] / se["size"] - 1))
check("E34/E35 explanations: size SE 15.39 -> 15.36; intercept SE 61,465 -> 65,545; intercept p 0.035 -> 0.047",
      (f2(rse["size"]), round(se["Intercept"]), round(rse["Intercept"]), f"{pv['Intercept']:.3f}", f"{rp['Intercept']:.3f}")
      == ("15.36", 61465, 65545, "0.035", "0.047"))
check("E35: same coefficients significant at 5% under classical and robust SEs",
      [v for v in b.index if pv[v] < 0.05] == [v for v in b.index if rp[v] < 0.05] == ["Intercept", "size"])

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic)
check("P08: t crit 2.048 (28 df) and 2.064 (24 df); 30 - 2 = 28, 30 - 6 = 24",
      (f"{tcrit(0.975, 28):.3f}", f"{tcrit(0.975, 24):.3f}") == ("2.048", "2.064"))
check("P10: n = 200, k = 4 -> 196 df, crit 1.972; 1.972 x 2.0 = 3.944 -> [1.06, 8.94]",
      f"{tcrit(0.975, 196):.3f}" == "1.972" and (f2(5 - 1.972 * 2), f2(5 + 1.972 * 2)) == ("1.06", "8.94"))
check("P10 distractors: 5 +/- 1.972 = [3.03, 6.97]; 5 +/- 2 = [3.00, 7.00]; 5 +/- 7.888 = [-2.89, 12.89]",
      (f2(5 - 1.972), f2(5 + 1.972)) == ("3.03", "6.97") and (f2(5 - 2 * 3.944), f2(5 + 2 * 3.944)) == ("-2.89", "12.89"))
check("P11/P13: 7 +/- 2 x 2 = [3, 11]; 7 +/- 2 = [5, 9]; 0 +/- 4; 7 +/- 8 = [-1, 15]",
      (7 - 4, 7 + 4, 7 - 2, 7 + 2, 7 - 8, 7 + 8) == (3, 11, 5, 9, -1, 15))
check("P13: nulls 0 and 12 outside [3, 11]; 4 and 10 inside", not (3 <= 0 <= 11) and 12 > 11 and all(3 < c < 11 for c in (4, 10)))
check("P16: (7-10)/2 = -1.50; 7/2 = 3.50; 10/2 = 5.00; (10-7)/2 = 1.50", ((7 - 10) / 2, 7 / 2, 10 / 2, (10 - 7) / 2) == (-1.5, 3.5, 5.0, 1.5))
check("P16: |t| = 1.5 < 1.972 (not rejected)", 1.5 < tcrit(0.975, 196))
check("P18: t = 5.0/2.0 = 2.5 > 1.972", 5 / 2 == 2.5 and 2.5 > tcrit(0.975, 196))
check("P20: p = 0.40 > 0.05 -> 95% CI contains 0", 0.40 > 0.05)
check("P22/P24: q = 3; F(3, 94); restricted df 100 - 3 = 97", (6 - 3, 100 - 6, 100 - 3) == (3, 94, 97))
check("P23: p = 0.32 above 0.10", 0.32 > 0.10)
check("P27: F = (40-30)/3 / (30/47) = 5.22; no q 15.67; inverted 0.19; 50 df 5.56",
      (f2((10 / 3) / (30 / 47)), f2(10 / (30 / 47)), f2((30 / 47) / (10 / 3)), f2((10 / 3) / (30 / 50))) == ("5.22", "15.67", "0.19", "5.56"))
check("P27 explanation: 10/3 = 3.333, 30/47 = 0.638", (f"{10 / 3:.3f}", f"{30 / 47:.3f}") == ("3.333", "0.638"))
check("P27: F(3, 47) 5% critical value 2.80 < 5.22", f"{stats.f.ppf(0.95, 3, 47):.2f}" == "2.80" and 5.22 > stats.f.ppf(0.95, 3, 47))
check("P30: TSS 500, RSS 200 -> 60% explained, not 40%", (500 - 200) / 500 == 0.6)
check("P31: p = 0.07 -> * (0.05 <= p < 0.10)", 0.05 <= 0.07 < 0.10)
check("P32: n = 40, k = 2/3/4: R2 0.300/0.330/0.335 -> adj 0.282/0.294/0.280; Model 2 highest",
      tuple(f"{1 - (1 - r2) * 39 / (40 - kk):.3f}" for r2, kk in ((0.300, 2), (0.330, 3), (0.335, 4))) == ("0.282", "0.294", "0.280"))

# ---------------------------------------------------------------- 3. CLAIMS
check("size and bedrooms positively correlated (r = 0.52)", f2(corr.loc["size", "bedrooms"]) == "0.52")
check("bedrooms positively correlated with price (r = 0.43): a non-significant partial effect is not 'no relationship'",
      corr.loc["price", "bedrooms"] > 0.4)
check("regressors are not mutually uncorrelated (E03 E false)", (corr.drop(index="price", columns="price").abs().values[np.triu_indices(6, 1)] > 0.01).all())
check("E04 B: average price per square foot ($135) is not 68.37", round(d["price"].mean() / d["size"].mean()) == 135)
check("E07: size SE rises mainly through collinearity: sqrt(1/(1-R2_aux)) = 1.30 vs s_e ratio 1.06",
      f2(math.sqrt(1 / (1 - aux._r2))) == "1.30" and f2(s_e / s_e1) == "1.06")
check("E07 D: root MSE did NOT fall when regressors were added (23,551 -> 24,936)", round(s_e1) == 23551 and s_e > s_e1)
check("E07: same 29 houses in both models", int(m1._N) == int(m._N) == 29)
check("E13: null 100 sits just inside the CI (|t| = 2.06 < 2.074)", f2(abs(t_null(100))) == "2.06")
check("E33/E07: size coefficient 73.77 -> 72.41 -> 68.37", tuple(f2(mm.coef()["size"]) for mm in (m1, m2, m)) == ("73.77", "72.41", "68.37"))
check("chapter prose line 1126: intercept is NOT the largest % SE change (lotsize -26%, bathrooms +23%)",
      abs(rse["Intercept"] / se["Intercept"] - 1) < max(abs(rse["lotsize"] / se["lotsize"] - 1), abs(rse["bathrooms"] / se["bathrooms"] - 1)))

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
print(", ".join(sorted(nums, key=lambda v: float(v.replace(",", "") or 0))))
failed = [k_ for k_, ok in checks.items() if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
sys.exit(1 if failed or not checks else 0)
