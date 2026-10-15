#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch06.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Simulations reproduce the chapter's own code exactly (same seeds, same draw order):
three samples with np.random.seed(12345); the 1,000-sample Monte Carlo with np.random.seed(42).
OLS is computed in closed form (identical to pyfixest.feols for y ~ x).
Run:  python3 quizzes/checks/ch06_factcheck.py      (exit 1 on any failure)
"""

import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

CHAPTER = "ch06"
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


def ols(x, y):
    """Simple-regression OLS: returns b1, b2, residuals, s_e, Sxx."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    sxx = ((x - x.mean()) ** 2).sum()
    b2 = ((x - x.mean()) * (y - y.mean())).sum() / sxx
    b1 = y.mean() - b2 * x.mean()
    e = y - b1 - b2 * x
    s_e = math.sqrt((e ** 2).sum() / (len(x) - 2))
    return b1, b2, e, s_e, sxx


def f2(v):
    return f"{v:.2f}"


# ---------------------------------------------------------------- 1. FACTS
# Generated data (Table 6.1): 5 observations from y = 1 + 2x + u
g = load("AED_GENERATEDDATA.DTA")
gb1, gb2, ge, gse, gsxx = ols(g["x"], g["y"])
g_r2 = 1 - (ge ** 2).sum() / ((g["y"] - g["y"].mean()) ** 2).sum()
g_seb2 = gse / math.sqrt(gsxx)
row4 = g[g["x"] == 4].iloc[0]
row3 = g[g["x"] == 3].iloc[0]

# Three samples (seed 12345, n = 30): x ~ N(3,1), u ~ N(0,2) drawn in this order per sample
np.random.seed(12345)
three = []
for _ in range(3):
    xs = np.random.normal(3, 1, 30)
    us = np.random.normal(0, 2, 30)
    three.append(ols(xs, 1 + 2 * xs + us)[:2])

# Monte Carlo (seed 42): 1,000 samples, n = 30
np.random.seed(42)
mc_b1, mc_b2, mc_x = [], [], []
for _ in range(1000):
    xs = np.random.normal(3, 1, 30)
    us = np.random.normal(0, 2, 30)
    b1, b2, *_ = ols(xs, 1 + 2 * xs + us)
    mc_b1.append(b1)
    mc_b2.append(b2)
    mc_x.append(xs)
mc_b1, mc_b2, mc_x = np.array(mc_b1), np.array(mc_b2), np.concatenate(mc_x)
sd1, sd2 = mc_b1.std(), mc_b2.std()  # np.std (ddof=0), as in the chapter

# Same Monte Carlo with n = 120 (seed 42): for the "quadruple n halves the SD" item
np.random.seed(42)
mc120 = []
for _ in range(1000):
    xs = np.random.normal(3, 1, 120)
    us = np.random.normal(0, 2, 120)
    mc120.append(ols(xs, 1 + 2 * xs + us)[1])
sd120 = np.std(mc120)

# Manual example (Section 6.4): (y, x) = (1,1), (2,2), (2,3), (2,4), (3,5)
mb1, mb2, me, mse, msxx = ols([1, 2, 3, 4, 5], [1, 2, 2, 2, 3])
mrss = (me ** 2).sum()

print(f"FACTS generated: b1={gb1:.6f} b2={gb2:.6f} R2={g_r2:.6f} s_e={gse:.6f} Sxx={gsxx} se(b2)={g_seb2:.6f} "
      f"mean y={g['y'].mean():.6f} u={g['u'].round(4).tolist()} resid={np.round(ge, 4).tolist()}")
print(f"FACTS three samples (b1, b2): {[(round(a, 4), round(b, 4)) for a, b in three]}")
print(f"FACTS MC n=30: b1 mean={mc_b1.mean():.4f} sd={sd1:.4f}; b2 mean={mc_b2.mean():.4f} sd={sd2:.4f} "
      f"min={mc_b2.min():.4f} max={mc_b2.max():.4f}; MC n=120: b2 sd={sd120:.4f}")
print(f"FACTS manual: b1={mb1:.4f} b2={mb2:.4f} RSS={mrss:.4f} s_e={mse:.4f} se(b2)={mse / math.sqrt(msxx):.4f}\n")

# ---------------------------------------------------------------- 2. CHECKS (exam)
check("generated data: 5 obs, x = 1..5, Eygivenx = 1 + 2x", len(g) == 5 and list(g["x"]) == [1, 2, 3, 4, 5]
      and np.allclose(g["Eygivenx"], 1 + 2 * g["x"]))
check("E01/E04/E05: sample line 2.81 + 1.05x", (f2(gb1), f2(gb2)) == ("2.81", "1.05"))
check("E02: obs at x = 3 has y = 4.49; sample mean of y = 5.97; E[y|x=3] = 7; distractor 2x3 = 6",
      f2(row3["y"]) == "4.49" and f2(g["y"].mean()) == "5.97" and 1 + 2 * 3 == 7)
check("E02 explanation: error at x = 3 is about -2.51", f2(row3["u"]) == "-2.51")
check("E04: obs x = 4 has y = 7.37; u = 7.37 - 9 = -1.63 (exact u rounds to -1.63)",
      f2(row4["y"]) == "7.37" and f2(7.37 - 9) == "-1.63" and f2(row4["u"]) == "-1.63")
check("E04 distractor: residual from stated line 7.37 - (2.81 + 1.05*4) = 0.36", f2(7.37 - (2.81 + 1.05 * 4)) == "0.36")
check("E05: four of the five error draws are negative", (g["u"] < 0).sum() == 4)
check("E06: three slopes 1.81, 1.79, 1.67", [f2(b) for _, b in three] == ["1.81", "1.79", "1.67"])
check("E14: MC slope mean 1.9944; 2 - mean ~ 0.006", f"{mc_b2.mean():.4f}" == "1.9944" and f"{2 - mc_b2.mean():.3f}" == "0.006")
check("E15/E16/E17/E23/E25: MC slope SD 0.38 (exact 0.3836)", f"{sd2:.4f}" == "0.3836" and f2(sd2) == "0.38")
check("E15: 2 +/- 2(0.38) = 1.24 to 2.76; +/-1 SD 1.62-2.38; +/-3 SD 0.86-3.14",
      (f2(2 - 0.76), f2(2 + 0.76), f2(2 - 0.38), f2(2 + 0.38), f2(2 - 3 * 0.38), f2(2 + 3 * 0.38))
      == ("1.24", "2.76", "1.62", "2.38", "0.86", "3.14"))
check("E15 distractor: 2 +/- 2(0.38/sqrt 30) = 1.86 to 2.14", (f2(2 - 2 * 0.38 / math.sqrt(30)), f2(2 + 2 * 0.38 / math.sqrt(30))) == ("1.86", "2.14"))
check("E15 explanation: 957 of 1,000 slopes (95.7%) in [1.24, 2.76]", ((mc_b2 >= 1.24) & (mc_b2 <= 2.76)).sum() == 957)
check("E16 distractor: 0.38 / sqrt(10) ~ 0.12", f2(0.38 / math.sqrt(10)) == "0.12")
check("E17: slopes range ~0.78 to ~3.25 (so not all within 0.5 of 2)", (f2(mc_b2.min()), f2(mc_b2.max())) == ("0.78", "3.25")
      and (np.abs(mc_b2 - 2) > 0.5).any())
check("E19: RSS = 0.4, s_e = sqrt(0.4/3) ~ 0.37 (0.365); distractors /n 0.28, s_e^2 0.13, /(n-1) 0.32",
      abs(mrss - 0.4) < 1e-12 and (f2(mse), f"{mse:.3f}", f2(math.sqrt(0.4 / 5)), f2(0.4 / 3), f2(math.sqrt(0.4 / 4)), f"{0.4 / 3:.3f}")
      == ("0.37", "0.365", "0.28", "0.13", "0.32", "0.133"))
check("E19: manual fit is 0.8 + 0.4x", (f"{mb1:.1f}", f"{mb2:.1f}") == ("0.8", "0.4"))
check("E20/E21: generated s_e = 1.05, Sxx = 10", f2(gse) == "1.05" and gsxx == 10)
check("E21: 1.05/sqrt 10 = 0.33 (= exact se(b2) 0.33); distractors 1.05/10 = 0.11, 1.05*sqrt10 = 3.32, 1.05/sqrt5 = 0.47",
      (f2(1.05 / math.sqrt(10)), f2(g_seb2), f2(1.05 / 10), f2(1.05 * math.sqrt(10)), f2(1.05 / math.sqrt(5)))
      == ("0.33", "0.33", "0.11", "3.32", "0.47"))
check("E23: 0.38/2 = 0.19; distractors 0.38/4 ~ 0.10, 2 x 0.38 = 0.76", (f2(0.38 / 2), f2(sd2 / 4), f2(2 * 0.38)) == ("0.19", "0.10", "0.76"))
check("E23 explanation: simulated SD with n = 120 is about 0.18-0.19, closest option 0.19",
      0.18 <= sd120 < 0.195 and min([0.10, 0.19, 0.38, 0.76], key=lambda v: abs(v - sd120)) == 0.19)
check("E25: intercept SD 1.21 (exact 1.2069)", f"{sd1:.4f}" == "1.2069" and f2(sd1) == "1.21")
check("E30: 1.85 +/- 0.35 = 1.50 to 2.20", (f2(1.85 - 0.35), f2(1.85 + 0.35)) == ("1.50", "2.20"))
check("E20: true sigma_u = 2 differs from s_e = 1.05", 2 != round(gse, 2))

# ---------------------------------------------------------------- 2b. CHECKS (practice arithmetic)
check("P02: 3 + 5*2 = 13; 5*2 = 10; 3 + 5 = 8", (3 + 5 * 2, 5 * 2, 3 + 5) == (13, 10, 8))
check("P04: fitted 7 + 4.5*4 = 25 -> e = 0; u = 25 - (8 + 16) = 1", (7 + 4.5 * 4, 25 - (7 + 4.5 * 4), 25 - (8 + 4 * 4)) == (25, 0, 1))
check("P14: 3.004 - 3 = 0.004", f"{3.004 - 3:.3f}" == "0.004")
check("P15: 0.5 +/- 0.2 = 0.3-0.7; +/-0.1 = 0.4-0.6; +/-0.3 = 0.2-0.8",
      (f"{0.5 - 0.2:.1f}", f"{0.5 + 0.2:.1f}", f"{0.5 - 0.3:.1f}", f"{0.5 + 0.3:.1f}") == ("0.3", "0.7", "0.2", "0.8"))
check("P15: ~99.7% within 3 SD, ~68% within 1 SD (normal)", round(100 * (2 * 0.99865 - 1), 1) == 99.7)
check("P16: 5,000 / 500 = 10 (sqrt 10 distractor)", 5000 / 500 == 10)
check("P19: sqrt(112/28) = 2; 112/28 = 4; sqrt(112/30) = 1.93; sqrt(112/29) = 1.97",
      (math.sqrt(112 / 28), 112 / 28, f2(math.sqrt(112 / 30)), f2(math.sqrt(112 / 29))) == (2.0, 4.0, "1.93", "1.97"))
check("P21: 2/sqrt50 = 0.28 (0.283); 2/50 = 0.04; 2*sqrt50 = 14.1; 2/sqrt30 = 0.37",
      (f2(2 / math.sqrt(50)), f"{2 / math.sqrt(50):.3f}", 2 / 50, f"{2 * math.sqrt(50):.1f}", f2(2 / math.sqrt(30)))
      == ("0.28", "0.283", 0.04, "14.1", "0.37"))
check("P21 explanation: Sxx 200 = 4 x 50 halves se(b2)", math.isclose(2 / math.sqrt(200), 0.5 * 2 / math.sqrt(50)))
check("P23: halving se needs 4n = 400; n^2 = 10,000; doubling -> x 1/sqrt2", (4 * 100, 100 ** 2) == (400, 10000))
check("P23/P24: doubling n multiplies se by 1/sqrt2 ~ 0.71 (cut ~30%)",
      f2(1 / math.sqrt(2)) == "0.71" and round(100 * (1 - 1 / math.sqrt(2))) == 29)
check("P30: 15 +/- 8 = 7-23; +/-4 = 11-19; +/-2 = 13-17; +/-12 = 3-27",
      (15 - 8, 15 + 8, 15 - 4, 15 + 4, 15 - 2, 15 + 2, 15 - 12, 15 + 12) == (7, 23, 11, 19, 13, 17, 3, 27))

# ---------------------------------------------------------------- 3. CLAIMS
check("E02/E04/E05: generated-data errors: obs at x=3 below the line (u < 0)", row3["u"] < 0)
check("E04 explanation: residual and error differ for obs x = 4 (0.35 vs -1.63)", f2(ge[3]) == "0.35" and abs(ge[3] - row4["u"]) > 1)
check("E05: sample slope below true slope, intercept above (n = 5)", gb2 < 2 and gb1 > 1)
check("E06: all three samples have different slopes and none equals 2", len({round(b, 4) for _, b in three}) == 3
      and all(abs(b - 2) > 0.1 for _, b in three))
check("E14/E17: MC slopes centered on 2 (|mean - 2| < 0.01) while individual estimates spread (SD > 0.3)",
      abs(mc_b2.mean() - 2) < 0.01 and sd2 > 0.3)
check("E17: slope histogram approximately bell-shaped (|skew| < 0.2, |excess kurtosis| < 0.4)",
      abs(pd.Series(mc_b2).skew()) < 0.2 and abs(pd.Series(mc_b2).kurt()) < 0.4)
check("E25: MC intercept mean ~1 (unbiased, |mean - 1| < 0.05)", abs(mc_b1.mean() - 1) < 0.05)
check("E25: x centered at 3, x = 0 far from most x values (< 1% of simulated x below 0)", abs(mc_x.mean() - 3) < 0.05 and (mc_x < 0).mean() < 0.01)
check("E25: intercept SD > slope SD", sd1 > sd2)
check("E16: SD of the estimates does not depend on the number of simulations (first 500 vs all 1,000 within 0.03)",
      abs(mc_b2[:500].std() - sd2) < 0.03)
check("E17: about 61% of MC slopes miss 2 by more than 0.2 (607 of 1,000)", (np.abs(mc_b2 - 2) > 0.2).sum() == 607)
check("E17 option E / E14: MC slope mean within 0.01 of 2 (no bias at n = 30)", abs(mc_b2.mean() - 2) < 0.01)
check("E15 stem: MC slope mean about 2.0", f"{mc_b2.mean():.1f}" == "2.0")
check("E09: chapter's own simulations draw x at random (x ~ N(3,1)) and OLS stays unbiased", abs(mc_b2.mean() - 2) < 0.01 and mc_x.std() > 0.9)
# P25: centering schooling at 15 lowers se(b1) and leaves b2, se(b2) unchanged (any sample with x in 10-20)
rng = np.random.default_rng(0)
xs = rng.uniform(10, 20, 200); ys = 5 + 1.0 * xs + rng.normal(0, 3, 200)
def se_both(x, y):
    b1, b2, e, s_e, sxx = ols(x, y)
    return b2, s_e / math.sqrt(sxx), math.sqrt(s_e ** 2 * (x ** 2).sum() / (len(x) * sxx)), (x ** 2).sum()
r_raw, r_c = se_both(xs, ys), se_both(xs - 15, ys)
check("P25: centering x at 15 cuts se(b1) and sum x^2; slope and se(b2) unchanged",
      r_c[2] < r_raw[2] / 5 and r_c[3] < r_raw[3] and math.isclose(r_c[0], r_raw[0]) and math.isclose(r_c[1], r_raw[1]))
check("P22: 400 = 4 x 100 plots; 0-200 kg range wider than 90-110 kg", 400 == 4 * 100 and 200 - 0 > 110 - 90)
check("generated data R2 = 0.769 (chapter table)", f"{g_r2:.3f}" == "0.769")

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
