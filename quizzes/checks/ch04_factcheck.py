#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch04.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Run:  python3 quizzes/checks/ch04_factcheck.py      (exit 1 on any failure)
"""

import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

CHAPTER = "ch04"
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


def f(x: float, d: int) -> str:
    return f"{x:.{d}f}"


# ---------------------------------------------------------------- 1. FACTS
# Women's earnings (Sections 4.1-4.4, 4.6)
x = load("AED_EARNINGS.DTA")["earnings"]
n, mean, sd = len(x), x.mean(), x.std(ddof=1)
se = sd / np.sqrt(n)
tc95, tc90, tc99 = (stats.t.ppf(q, n - 1) for q in (0.975, 0.95, 0.995))
ci = {lvl: (mean - c * se, mean + c * se) for lvl, c in ((90, tc90), (95, tc95), (99, tc99))}
t40 = (mean - 40000) / se
p40 = 2 * stats.t.sf(abs(t40), n - 1)
p40_one = stats.t.sf(t40, n - 1)

# Gasoline prices (Section 4.5)
g = load("AED_GASPRICE.DTA")["price"]
ng, mg, sdg = len(g), g.mean(), g.std(ddof=1)
seg = sdg / np.sqrt(ng)
tg = (mg - 3.81) / seg
pg = 2 * stats.t.sf(abs(tg), ng - 1)
tcg = stats.t.ppf(0.975, ng - 1)

# Male earnings (Section 4.5)
m = load("AED_EARNINGSMALE.DTA")["earnings"]
nm, mm = len(m), m.mean()
sem = m.std(ddof=1) / np.sqrt(nm)
tm = (mm - 50000) / sem
pm = 2 * stats.t.sf(abs(tm), nm - 1)

# Real GDP per capita growth (Section 4.5)
gdp = load("AED_REALGDPPC.DTA")
gr_rows = gdp.dropna(subset=["growth"])
gr = gr_rows["growth"]
ngr, mgr = len(gr), gr.mean()
segr = gr.std(ddof=1) / np.sqrt(ngr)
tgr = (mgr - 2.0) / segr
pgr = 2 * stats.t.sf(abs(tgr), ngr - 1)
yoy = 100 * (gdp["realgdppc"] / gdp["realgdppc"].shift(4) - 1)

# Proportions (Section 4.7, voters: numbers given in the chapter)
nv, kv = 921, 480
ph = kv / nv
seph = math.sqrt(ph * (1 - ph) / nv)
z0 = (ph - 0.5) / math.sqrt(0.25 / nv)
pz = 2 * stats.norm.sf(abs(z0))

print(f"FACTS women: n={n} mean={mean:.4f} sd={sd:.4f} se={se:.4f} tc90={tc90:.4f} tc95={tc95:.4f} tc99={tc99:.4f}")
print(f"      CI90={ci[90]} CI95={ci[95]} CI99={ci[99]} t40={t40:.4f} p40={p40:.4f} p40_one={p40_one:.4f}")
print(f"FACTS gas: n={ng} mean={mg:.4f} sd={sdg:.4f} se={seg:.4f} t={tg:.4f} p={pg:.2e} tc={tcg:.4f}")
print(f"FACTS men: n={nm} mean={mm:.2f} se={sem:.2f} t={tm:.4f} p={pm:.4f}")
print(f"FACTS growth: n={ngr} mean={mgr:.4f} se={segr:.4f} t={tgr:.4f} p={pgr:.4f} "
      f"first={gr_rows['date'].iloc[0]} last={gr_rows['date'].iloc[-1]} ac1={gr.autocorr(1):.3f}")
print(f"FACTS voters: phat={ph:.4f} se={seph:.4f} z={z0:.4f} p={pz:.4f}\n")

# ---------------------------------------------------------------- 2. CHECKS (exam)
check("women n = 171", n == 171)
check("mean $41,413 (41,412.69)", round(mean) == 41413 and f(mean, 2) == "41412.69")
check("SD $25,527", round(sd) == 25527)
check("SE $1,952", round(se) == 1952)
check("E03: men SD ~$65,035, SE ~$4,706; sqrt(191) = 13.82 (~13.8); SD/SE ~14",
      round(m.std(ddof=1)) == 65035 and round(sem) == 4706 and round(65035 / np.sqrt(191)) == 4706
      and f(np.sqrt(191), 2) == "13.82" and f(np.sqrt(191), 1) == "13.8" and round(m.std(ddof=1) / sem) == 14)
check("E03 distractors: SD/n = $340; mean/sqrt(n) = $3,788", (round(65035 / 191), round(52354 / np.sqrt(191))) == (340, 3788))
check("E02: SE at n = 684 ~ $976 (half)", round(sd / np.sqrt(684)) == 976 and round(1952 / 2) == 976)
check("95% CI [$37,559, $45,266], width $7,707", (round(ci[95][0]), round(ci[95][1]), round(ci[95][1] - ci[95][0])) == (37559, 45266, 7707))
check("99% CI width $10,171", round(ci[99][1] - ci[99][0]) == 10171)
check("critical values 1.974 / ~1.97, 2.61, 1.654", (f(tc95, 3), f(tc95, 2), f(tc99, 2), f(tc90, 3)) == ("1.974", "1.97", "2.61", "1.654"))
check("E10: 36,000 rejected (t ~ 2.77), 46,500 rejected (t ~ -2.61)",
      f((mean - 36000) / se, 2) == "2.77" and f((mean - 46500) / se, 2) == "-2.61" and abs((mean - 36000) / se) > tc95 and abs((mean - 46500) / se) > tc95)
check("E10: 38,000 and 44,000 not rejected (inside CI)", all(abs((mean - v) / se) < tc95 for v in (38000, 44000)) and ci[95][0] < 38000 and 44000 < ci[95][1])
check("t(40,000) = 0.72 (exact 0.7237; rounded inputs 0.7239)", f(t40, 4) == "0.7237" and f((41413 - 40000) / 1952, 2) == "0.72")
check("E13 distractors: /SD 0.06, /n 8.26, mean/SE 21.22", (f(1413 / 25527, 2), f(1413 / 171, 2), f(41413 / 1952, 2)) == ("0.06", "8.26", "21.22"))
check("p(40,000) two-sided 0.4703 (~0.47)", f(p40, 4) == "0.4703")
check("E25: one-sided 0.2351; distractors 0.9406 (doubled), 0.7649 (wrong tail Pr[T <= t])",
      f(p40_one, 4) == "0.2351" and f(2 * 0.4703, 4) == "0.9406" and f(stats.t.cdf(t40, n - 1), 4) == "0.7649")
check("E24: gap 2.0 - mean ~ 0.01 points (D's 0.07 is |t|, not the gap)", f(2.0 - mgr, 2) == "0.01" and f(abs(tgr), 2) == "0.07")
check("E19 explanation: n = 684 doubles t to ~1.45", f(2 * t40, 2) == "1.45")
check("gas n = 32, mean $3.67 (3.6697), SE $0.027 (0.0267)", ng == 32 and f(mg, 4) == "3.6697" and f(mg, 2) == "3.67" and f(seg, 3) == "0.027" and f(seg, 4) == "0.0267")
check("gas t = -5.26, p < 0.0001, crit +/-2.04 (df 31)", f(tg, 2) == "-5.26" and pg < 1e-4 and f(tcg, 2) == "2.04")
check("gas gap $0.14; $2.10 per 15-gallon tank; ~$109/year", f(3.81 - mg, 2) == "0.14" and f(15 * (3.81 - mg), 2) == "2.10" and round(52 * 15 * (3.81 - mg)) == 109)
check("E11: 3.67 +/- 2(0.027) = [3.62, 3.72]; also with exact values", (f(3.67 - 0.054, 2), f(3.67 + 0.054, 2)) == ("3.62", "3.72")
      and (f(mg - 2 * seg, 2), f(mg + 2 * seg, 2)) == ("3.62", "3.72"))
check("E11 distractors: +/-1 SE [3.64, 3.70]; centered on 3.81 [3.76, 3.86]; +/-4 SE [3.56, 3.78]",
      (f(3.67 - 0.027, 2), f(3.67 + 0.027, 2), f(3.81 - 0.054, 2), f(3.81 + 0.054, 2), f(3.67 - 0.108, 2), f(3.67 + 0.108, 2))
      == ("3.64", "3.70", "3.76", "3.86", "3.56", "3.78"))
check("E11 explanation: interval excludes 3.81", mg + 2 * seg < 3.81)
check("men n = 191, mean $52,354, p = 0.62", nm == 191 and round(mm) == 52354 and f(pm, 2) == "0.62" and f(pm, 4) == "0.6175")
check("growth n = 241, mean 1.99%, t = -0.07, p = 0.95", ngr == 241 and f(mgr, 2) == "1.99" and f(tgr, 2) == "-0.07" and f(pgr, 2) == "0.95")
check("growth covers 1960 Q1 to 2020 Q1 ('1960 to early 2020')", str(gr_rows["date"].iloc[0])[:10] == "1960-01-01" and str(gr_rows["date"].iloc[-1])[:10] == "2020-01-01")
check("voters: phat 0.521, se 0.0165", f(ph, 3) == "0.521" and f(seph, 4) == "0.0165")
check("E28 distractors: no n 0.500; no sqrt 0.0003; sqrt/n 0.0005",
      (f(math.sqrt(ph * (1 - ph)), 3), f(ph * (1 - ph) / nv, 4), f(math.sqrt(ph * (1 - ph)) / nv, 4)) == ("0.500", "0.0003", "0.0005"))
check("voters: p = 0.20 (z = 1.29)", f(pz, 2) == "0.20" and f(z0, 2) == "1.29")
check("voters: 95% CI [48.9%, 55.3%]; margin ~3.2 points", (f(100 * (ph - 1.96 * seph), 1), f(100 * (ph + 1.96 * seph), 1), f(100 * 1.96 * seph, 1)) == ("48.9", "55.3", "3.2"))
check("voters: 2,500 with 52% share -> significant (z = 2.00, p < 0.05)", f(0.02 / math.sqrt(0.25 / 2500), 2) == "2.00" and 2 * stats.norm.sf(2.0) < 0.05)

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic)
check("P01: 16,000/8 = 2,000; distractors 250, 5,625", (16000 / 8, 16000 / 64, 45000 / 8) == (2000, 250, 5625))
check("P02: n = 256 halves SE; 128 -> /1.41; 4,096 -> /8", (16000 / math.sqrt(256), f(math.sqrt(2), 2), math.sqrt(4096) / 8) == (1000, "1.41", 8))
check("P03: both SDs = 12 (1.2 x 10, 0.6 x 20)", (round(1.2 * 10, 6), round(0.6 * 20, 6)) == (12, 12))
check("P06: t(9) 2.262, t(10) 2.228, one-sided t(9) 1.833", (f(stats.t.ppf(.975, 9), 3), f(stats.t.ppf(.975, 10), 3), f(stats.t.ppf(.95, 9), 3)) == ("2.262", "2.228", "1.833"))
check("P07: t(99) ~ 1.98", f(stats.t.ppf(.975, 99), 2) == "1.98")
check("P08: midpoint 52,000, margin 4,000, width 8,000", ((48000 + 56000) / 2, (56000 - 48000) / 2) == (52000, 4000))
check("P09: se 1.82; 95% margin 3.6 -> [26.4, 33.6]; inverted [27.5, 32.5]",
      (f(3 / 1.645, 2), f(30 - 3 * 1.96 / 1.645, 1), f(30 + 3 * 1.96 / 1.645, 1), f(30 - 3 * 1.645 / 1.96, 1), f(30 + 3 * 1.645 / 1.96, 1))
      == ("1.82", "26.4", "33.6", "27.5", "32.5"))
check("P11: 45,000 +/- 4,000; +/-2,000; +/-32,000; +/-16,000", (45000 - 4000, 45000 + 4000, 45000 - 2000, 45000 + 2000, 45000 - 32000, 45000 + 32000, 45000 - 16000, 45000 + 16000)
      == (41000, 49000, 43000, 47000, 13000, 77000, 29000, 61000))
check("P13: t = 5/3 = 1.67; 105/3 = 35; 5/7 = 0.71", (f(5 / 3, 2), 105 / 3, f(5 / 7, 2)) == ("1.67", 35, "0.71"))
check("P14: t(48) crit ~2.01; p ~ 0.10", f(stats.t.ppf(.975, 48), 2) == "2.01" and f(2 * stats.t.sf(5 / 3, 48), 2) == "0.10")
check("P16/P25: se 3, t = -1.00, crit(35) 2.03, p2 0.32, p1 0.16, 0.84, 0.64",
      18 / 6 == 3 and (72 - 75) / 3 == -1 and f(stats.t.ppf(.975, 35), 2) == "2.03" and f(2 * stats.t.cdf(-1, 35), 2) == "0.32"
      and f(stats.t.cdf(-1, 35), 2) == "0.16" and f(stats.t.sf(-1, 35), 2) == "0.84" and f(2 * 0.32, 2) == "0.64")
check("P21: 0.02 hours = 1.2 minutes", round(0.02 * 60, 6) == 1.2)
check("P22: t = 5 and 0.5", (5 / 1, 5 / 10) == (5, 0.5))
check("P24: t = 0.5/0.25 = 2.0; p ~ 0.046 (df 399); not < 0.01", 0.5 / 0.25 == 2 and f(2 * stats.t.sf(2, 399), 3) == "0.046")
check("P28: se 0.022 (0.0222); margin 1.96 x se = 0.044; +/-1 SE [0.528, 0.572]",
      f(math.sqrt(.55 * .45 / 500), 3) == "0.022" and f(1.96 * math.sqrt(.55 * .45 / 500), 3) == "0.044"
      and (f(.55 - math.sqrt(.55 * .45 / 500), 3), f(.55 + math.sqrt(.55 * .45 / 500), 3)) == ("0.528", "0.572"))
se28 = math.sqrt(.55 * .45 / 500)
check("P28 exact: CI [0.506, 0.594], centered 0.50 [0.456, 0.544], 99% [0.493, 0.607] (exact se)",
      (f(.55 - 1.96 * se28, 3), f(.55 + 1.96 * se28, 3), f(.5 - 1.96 * se28, 3), f(.5 + 1.96 * se28, 3), f(.55 - 2.576 * se28, 3), f(.55 + 2.576 * se28, 3))
      == ("0.506", "0.594", "0.456", "0.544", "0.493", "0.607"))
check("P29: z = 2.24, p ~ 0.025", f(0.05 / math.sqrt(.25 / 500), 2) == "2.24" and f(2 * stats.norm.sf(0.05 / math.sqrt(.25 / 500)), 3) == "0.025")
check("P30: n = 5,000 -> z ~ 7.1", f(0.05 / math.sqrt(.25 / 5000), 1) == "7.1")

# ---------------------------------------------------------------- 3. CLAIMS
check("women: sample mean above 40,000 (Ha side of the upper-tailed test)", mean > 40000)
check("one-sided p is exactly half the two-sided p", math.isclose(p40_one, p40 / 2, rel_tol=1e-9))
check("women: not rejected at 5% and at 1% (two-sided and one-sided)", p40 > 0.05 and p40_one > 0.05)
check("gas: rejected at 1% as well; prices below 3.81", pg < 0.01 and mg < 3.81)
check("gas varies little across stations vs earnings (CV gas << CV earnings)", sdg / mg < 0.1 < sd / mean)
check("growth column = 4-quarter (year-over-year) % change of real GDP pc (quarterly, overlapping)",
      np.allclose(gdp["growth"].dropna().values, yoy.dropna().values, atol=1e-3))
check("growth quarterly: 241 obs over ~60 years (not 241 separate years)", gr_rows["year"].nunique() == 61)
check("growth strongly autocorrelated across neighboring quarters (lag-1 r > 0.8)", gr.autocorr(1) > 0.8)
check("men: sample mean above 50,000 but not significant", mm > 50000 and pm > 0.05)
check("voters: 50% inside 95% CI", ph - 1.96 * seph < 0.5 < ph + 1.96 * seph)
check("t critical values exceed 1.96 for df 31 and 170", tcg > 1.96 and tc95 > 1.96)

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
