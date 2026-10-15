#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch03.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Run:  python3 quizzes/checks/ch03_factcheck.py      (exit 1 on any failure)

Note: the population parameters of the 1880 Census (mu = 24.13, sigma = 18.61 years,
N = 50,169,452) are given by the chapter; only the 100 sample means/SDs are in the data.
"""

import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

CHAPTER = "ch03"
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
coin = load("AED_COINTOSSMEANS.DTA")
xbar = coin["xbar"].astype(float)
c_mean, c_sd, c_min, c_max = xbar.mean(), xbar.std(), xbar.min(), xbar.max()
theo_sd30 = math.sqrt(0.25 / 30)

census = load("AED_CENSUSAGEMEANS.DTA")
am = census["mean"].astype(float)
asd = census["stdev"].astype(float)
a_mean, a_sd, a_min, a_max = am.mean(), am.std(), am.min(), am.max()
MU, SIGMA, N_POP = 24.13, 18.61, 50_169_452
sd25 = SIGMA / 5

# chapter's single 30-toss sample (seed 10101, uniform > 0.5)
np.random.seed(10101)
one = np.where(np.random.uniform(0, 1, 30) > 0.5, 1, 0)
one_mean, one_s = one.mean(), one.std(ddof=1)
one_se = one_s / math.sqrt(30)

# chapter's simulation (seed 10101, binomial)
np.random.seed(10101)
sim = np.array([np.random.binomial(1, 0.5, 30).mean() for _ in range(400)])

# chapter's weighted-mean example (seed 5)
np.random.seed(5)
inc_m = np.random.normal(60000, 15000, 50)
inc_w = np.random.normal(50000, 15000, 50)
true_pop = (inc_m.mean() + inc_w.mean()) / 2
s_m = np.random.choice(inc_m, size=15, replace=False)
s_w = np.random.choice(inc_w, size=35, replace=False)
samp = np.concatenate([s_m, s_w])
unw = samp.mean()
wtd = np.average(samp, weights=np.concatenate([np.repeat(1 / 0.3, 15), np.repeat(1 / 0.7, 35)]))

print(f"FACTS coin DTA: n={len(xbar)} mean={c_mean:.6f} sd={c_sd:.6f} min={c_min:.6f} max={c_max:.6f} "
      f"skew={stats.skew(xbar):.4f} theo sd={theo_sd30:.6f}")
print(f"FACTS single sample: heads={one.sum()} mean={one_mean:.4f} s={one_s:.6f} se={one_se:.6f}")
print(f"FACTS simulation: mean={sim.mean():.6f} sd(ddof0)={sim.std():.6f} min={sim.min():.4f} max={sim.max():.4f}")
print(f"FACTS census DTA: n={len(am)} mean={a_mean:.6f} sd={a_sd:.6f} min={a_min:.4f} max={a_max:.4f} "
      f"skew={stats.skew(am):.4f} exkurt={stats.kurtosis(am):.4f}; first means {am.head(3).round(2).tolist()}, "
      f"first s={asd.iloc[0]:.6f}")
print(f"FACTS weights: men={inc_m.mean():.2f} women={inc_w.mean():.2f} pop={true_pop:.2f} unw={unw:.2f} wtd={wtd:.2f}\n")

# ---------------------------------------------------------------- 2. CHECKS (exam)
# E01 unfair coin
check("E01: unfair coin mu 0.6, var 0.24; fair var 0.25",
      (f(0 * .4 + 1 * .6, 2), f((0 - .6) ** 2 * .4 + (1 - .6) ** 2 * .6, 2), (0 - .5) ** 2 * .5 + (1 - .5) ** 2 * .5) == ("0.60", "0.24", 0.25))
# E02 employment Bernoulli
v = (0 - .8) ** 2 * .2 + (1 - .8) ** 2 * .8
check("E02: var 0.16 = 0.128 + 0.032 = p(1-p); sd 0.4", (f(v, 3), f(0.64 * .2, 3), f(0.04 * .8, 3), f(.8 * .2, 2), f(math.sqrt(v), 1)) == ("0.160", "0.128", "0.032", "0.16", "0.4"))
# E03 / E20 census population and sample-mean range
check("E03/E20: census means range 14.6 to 33.4", (f(a_min, 1), f(a_max, 1)) == ("14.6", "33.4"))
check("E03: N = 50,169,452 (chapter constant)", N_POP == 50169452)
# E04 / E07 / E13 single sample
check("E04: 12 heads, xbar 0.40", one.sum() == 12 and one_mean == 0.4)
check("E04: gap 0.10 ~ 1.1 SD of xbar (0.1/0.0913)", f(0.1 / theo_sd30, 1) == "1.1")
pr12 = stats.binom.pmf(12, 30, 0.5)
check("E07: Pr(exactly 12 heads) ~ 8%, so ~92% differ", (round(100 * pr12), round(100 * (1 - pr12))) == (8, 92))
check("E13: s = 0.4983, se = 0.0910, 0.40 +/- 0.091 = 0.31 to 0.49", (f(one_s, 4), f(one_se, 4), f(0.4 - one_se, 2), f(0.4 + one_se, 2)) == ("0.4983", "0.0910", "0.31", "0.49"))
check("E13: se 0.0910 ~ 9.1% (distractor); individual s ~0.50", f(100 * one_se, 1) == "9.1" and f(one_s, 2) == "0.50")
# E05 coin DTA
check("E05: 400 means, avg 0.4994, sd 0.0863, range 0.2667-0.7333", (len(xbar), f(c_mean, 4), f(c_sd, 4), f(c_min, 4), f(c_max, 4)) == (400, "0.4994", "0.0863", "0.2667", "0.7333"))
check("E05: extremes = 8 and 22 heads of 30", (round(c_min * 30), round(c_max * 30)) == (8, 22))
# E08 SD of xbar n=100 and distractors
check("E08: 0.5/sqrt(100)=0.05; var 0.0025; 0.5/100=0.005", (0.5 / math.sqrt(100), 0.25 / 100, 0.5 / 100) == (0.05, 0.0025, 0.005))
# E09 halve SD
check("E09: 4x30=120; 2x30=60; sqrt2*30~42; 30^2=900; 0.0913/2 ~0.0456",
      (4 * 30, 2 * 30, round(math.sqrt(2) * 30), 30 ** 2, f(theo_sd30, 4), f(math.sqrt(.25 / 120), 4)) == (120, 60, 42, 900, "0.0913", "0.0456"))
# E12 se of first census sample
s1 = asd.iloc[0]
check("E12: first census sample xbar 27.84, s 20.71, n 25", (f(am.iloc[0], 2), f(s1, 2), census["numobs"].iloc[0]) == ("27.84", "20.71", 25))
check("E12: se 4.14; s/n 0.83; xbar/5 5.57; s^2/n 17.15; sigma/5 3.72",
      (f(s1 / 5, 2), f(s1 / 25, 2), f(am.iloc[0] / 5, 2), f(s1 ** 2 / 25, 2), f(sd25, 2)) == ("4.14", "0.83", "5.57", "17.15", "3.72"))
# E14 doubling n
check("E14: sigma/sqrt25 = 3.72, /sqrt50 = 2.63, /sqrt100 = 1.86; sqrt2 ~1.41",
      (f(SIGMA / 5, 2), f(SIGMA / math.sqrt(50), 2), f(SIGMA / 10, 2), f(math.sqrt(2), 2)) == ("3.72", "2.63", "1.86", "1.41"))
# E15 n for SD = 1
check("E15: n = 18.61^2 ~ 346; ~19; sqrt(18.61) ~ 4; (1.96*18.61)^2 ~ 1,330",
      (round(SIGMA ** 2), round(SIGMA), round(math.sqrt(SIGMA)), round((1.96 * SIGMA) ** 2, -1)) == (346, 19, 4, 1330))
# E17 bands (statement uses the 1-SD band, which is False for 95%)
lo, hi = 0.5 - 1.96 * theo_sd30, 0.5 + 1.96 * theo_sd30
check("E17: 0.5 +/- 1.96*0.0913 ~ 0.32 to 0.68; 0.5 +/- 0.0913 ~ 0.41 to 0.59",
      (f(lo, 2), f(hi, 2), f(0.5 - theo_sd30, 2), f(0.5 + theo_sd30, 2)) == ("0.32", "0.68", "0.41", "0.59"))
check("E17: normal 1-SD share ~68%; DTA shares 66% in [0.41, 0.59] and 97% in [0.32, 0.68]",
      round(100 * (stats.norm.cdf(1) - stats.norm.cdf(-1))) == 68
      and round(100 * ((xbar >= 0.41) & (xbar <= 0.59)).mean()) == 66
      and round(100 * ((xbar >= 0.32) & (xbar <= 0.68)).mean()) == 97)
# E18 z of largest coin-toss mean
check("E18: max coin mean 0.7333 (22/30); Z = 0.2333/0.0913 ~ 2.56; 0.7333/0.0913 ~ 8.03; 0.2333/0.5 ~ 0.47; 0.23",
      (f(c_max, 4), f((0.7333 - 0.5) / 0.0913, 2), f((c_max - 0.5) / theo_sd30, 2), f(0.7333 / 0.0913, 2), f((0.7333 - 0.5) / 0.5, 2), f(0.7333 - 0.5, 2))
      == ("0.7333", "2.56", "2.56", "8.03", "0.47", "0.23"))
check("E18: max is the largest of 400 means", c_max == xbar.max() and len(xbar) == 400)
check("E20: 100 census sample means span ~19 years (14.6 to 33.4)", round(a_max - a_min) == 19)
# E19 / E20 census summary
check("E19/E20: avg of 100 census means 23.78, sd 3.76 (~3.8)", (f(a_mean, 2), f(a_sd, 2), f(a_sd, 1), len(am)) == ("23.78", "3.76", "3.8", 100))
# E21 first sample gap
check("E21: 27.84 - 24.13 = 3.71 ~ one SD of xbar (3.72)", f(27.84 - MU, 2) == "3.71" and abs((27.84 - MU) / sd25 - 1) < 0.01)
# E22 second sample
check("E22: census sample means 27.84, 19.40, 23.28", [f(v, 2) for v in am.head(3)] == ["27.84", "19.40", "23.28"])
# E23 efficiency
check("E23: SD(xbar) 3.72 vs SD(X1) 18.61", f(SIGMA / math.sqrt(25), 2) == "3.72")
# E26 simulation with seed 10101
check("E26: simulation mean 0.5004, sd 0.0887 (chapter prints np.std, ddof=0)", (f(sim.mean(), 4), f(sim.std(), 4)) == ("0.5004", "0.0887"))
# E27 uniform threshold
check("E27: Pr(U > 0.7) = 0.3; distractor 0.7 - 0.5 = 0.2", (f(1 - 0.7, 1), f(0.7 - 0.5, 1)) == ("0.3", "0.2"))
# E28 weights and simulation
check("E28: w_men = 1/0.3 ~ 3.33, w_women = 1/0.7 ~ 1.43", (f(1 / 0.3, 2), f(1 / 0.7, 2)) == ("3.33", "1.43"))
check("E28: unweighted $54,023, pop $56,373, weighted $56,377", (round(unw), round(true_pop), round(wtd)) == (54023, 56373, 56377))

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic)
check("P01: mu = 200; simple avg 350; 600*0.2 = 120; 600-100 = 500", (100 * .8 + 600 * .2, (100 + 600) / 2, 600 * .2, 600 - 100) == (200, 350, 120, 500))
lv = (0 - 1) ** 2 * .9 + (10 - 1) ** 2 * .1
check("P02: lottery mu 1, var 9 (0.9 + 8.1), sd 3; unweighted 82; equal-weight var 25",
      (f(10 * .1, 1), f(lv, 1), f((0 - 1) ** 2 * .9, 1), f((10 - 1) ** 2 * .1, 1), f(math.sqrt(lv), 1), (0 - 1) ** 2 + (10 - 1) ** 2, (0 - 5) ** 2 * .5 + (10 - 5) ** 2 * .5)
      == ("1.0", "9.0", "0.9", "8.1", "3.0", 82, 25))
check("P07: Pr(exactly 15 heads of 30) ~ 14% (so ~86% differ), and 15 is the modal count",
      round(100 * stats.binom.pmf(15, 30, .5)) == 14 and round(100 * (1 - stats.binom.pmf(15, 30, .5))) == 86
      and stats.binom.pmf(15, 30, .5) == max(stats.binom.pmf(k, 30, .5) for k in range(31)))
check("P08: var 400/25 = 16, sd 4, 20/25 = 0.8", (400 / 25, math.sqrt(400 / 25), 20 / 25) == (16, 4, 0.8))
check("P09: 4*100 = 400; sqrt2*100 ~ 141; 100^2 = 10,000", (4 * 100, round(math.sqrt(2) * 100), 100 ** 2) == (400, 141, 10000))
check("P10: sigma^2 1,600; var(xbar) 100; sd 10; 40/16 = 2.5", (40 ** 2, 40 ** 2 / 16, 40 / math.sqrt(16), 40 / 16) == (1600, 100, 10, 2.5))
check("P12: se 1,500; s/n 150; 2 se = 3,000; s = 15,000", (15000 / 10, 15000 / 100, 2 * 15000 / 10) == (1500, 150, 3000))
check("P13: doubling n=400 -> se 800/sqrt2 ~ $566", round(800 / math.sqrt(2)) == 566)
check("P13/P14: se_B = 16,000/sqrt(400) = 800; 54,000 +/- 800 = 53,200 to 54,800", (16000 / math.sqrt(400), 54000 - 800, 54000 + 800) == (800, 53200, 54800))
check("P15: n = (80/10)^2 = 64; sqrt n 8; 6,400/10 = 640; sigma^2 6,400; se 5 -> 256", ((80 / 10) ** 2, 80 / 10, 80 ** 2 / 10, 80 ** 2, (80 / 5) ** 2) == (64, 8, 640, 6400, 256))
check("P16: 12/sqrt(64) = 1.5; 12/64 = 0.1875", (12 / math.sqrt(64), 12 / 64) == (1.5, 0.1875))
check("P18: Pr(48 < xbar < 52) ~ 0.82 (z = 1.33); using sigma=12 ~ 0.13; n=144 -> sd 1",
      (f(2 / 1.5, 2), f(stats.norm.cdf(2 / 1.5) - stats.norm.cdf(-2 / 1.5), 2), f(stats.norm.cdf(2 / 12) - stats.norm.cdf(-2 / 12), 2), 12 / math.sqrt(144))
      == ("1.33", "0.82", "0.13", 1.0))
check("P18: 0.68 and 0.95 are the 1-SD and ~2-SD normal shares", (f(stats.norm.cdf(1) - stats.norm.cdf(-1), 2), f(stats.norm.cdf(1.96) - stats.norm.cdf(-1.96), 2)) == ("0.68", "0.95"))
check("P20: 30,000/sqrt(100) = 3,000; /sqrt(400) = 1,500; gap 50,200 - 50,000 = 200; SE of avg of 200 means ~ $212; sqrt2 ~1.41",
      (30000 / math.sqrt(100), 30000 / math.sqrt(400), 50200 - 50000, round(3000 / math.sqrt(200)), f(math.sqrt(2), 2)) == (3000, 1500, 200, 212, "1.41"))
check("P20 claim: $200 gap is within chance (< 1 SE of the average of 200 means)", 200 / (3000 / math.sqrt(200)) < 1)
check("P23: var 4 -> sd 2, var 9 -> sd 3", (math.sqrt(4), math.sqrt(9)) == (2, 3))
check("P26: chapter's two coin runs: DTA mean 0.4994, simulation mean 0.5004; theory sd 0.0913", (f(c_mean, 4), f(sim.mean(), 4), f(theo_sd30, 4)) == ("0.4994", "0.5004", "0.0913"))
check("P28: 1/0.02 = 50; 1/0.10 = 10; 0.10/0.02 = 5", (round(1 / 0.02), round(1 / 0.10), round(0.10 / 0.02)) == (50, 10, 5))

# ---------------------------------------------------------------- 3. CLAIMS
check("coin DTA means are multiples of 1/30 (sample of 30 tosses)", np.allclose(xbar * 30, np.round(xbar * 30), atol=1e-4))
check("coin sample means much less spread than tosses (0.0863 vs 0.5)", c_sd < 0.5 / 5)
check("coin means roughly symmetric (|skew| < 0.2)", abs(stats.skew(xbar)) < 0.2)
check("census means roughly bell-shaped (|skew| < 0.5, |excess kurtosis| < 0.5)", abs(stats.skew(am)) < 0.5 and abs(stats.kurtosis(am)) < 0.5)
check("census means vary far less than ages (3.76 vs 18.61)", a_sd < SIGMA / 4)
check("gap 23.78 vs 24.13 within chance: |gap| < 2 * 3.72/sqrt(100)", abs(a_mean - MU) < 2 * sd25 / math.sqrt(100))
check("census sample means several years from mu exist (max gap > 5 years)", (am - MU).abs().max() > 5)
check("first census sample is above mu (27.84 > 24.13)", am.iloc[0] > MU)
check("unfair coin: higher mean, slightly lower variance than fair coin", 0.6 > 0.5 and 0.24 < 0.25)
check("weighted mean much closer to pop mean than unweighted", abs(wtd - true_pop) < abs(unw - true_pop) / 100)
check("unweighted mean understates pop mean (women oversampled, lower income)", unw < true_pop and inc_w.mean() < inc_m.mean())
check("P30 direction: oversampling a low group pulls unweighted mean down (illustration with chapter sim)", unw < true_pop)

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
