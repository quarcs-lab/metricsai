#!/usr/bin/env python3
"""Fact-check for quizzes/banks/ch01.json: every number and data claim in the bank.

Built from .claude/skills/write-quiz/scripts/factcheck_template.py.
Run:  python3 quizzes/checks/ch01_factcheck.py      (exit 1 on any failure)
"""

import json
import re
import sys
from pathlib import Path

import pandas as pd
import pyfixest as pf

CHAPTER = "ch01"
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
m = pf.feols("price ~ size", data=d)
b0, b1 = m.coef()["Intercept"], m.coef()["size"]
se1, t0, t1 = m.se()["size"], m.tstat()["Intercept"], m.tstat()["size"]
r2 = m._r2
r2_bed = pf.feols("price ~ bedrooms", data=d)._r2
rmse = float((m.resid() ** 2).mean() ** 0.5)
print(f"FACTS  N={len(d)} b0={b0:.6f} b1={b1:.6f} se1={se1:.6f} t0={t0:.6f} t1={t1:.6f} "
      f"r2={r2:.6f} r2_bedrooms={r2_bed:.6f} rmse={rmse:.3f}\n")

# The chapter's rounded equation (Section 1.9): price = 115,017 + 73.77 x size
B0, B1 = round(b0), round(b1, 2)
pred = lambda s: B0 + B1 * s  # noqa: E731

# ---------------------------------------------------------------- 2. CHECKS
check("N = 29", len(d) == 29)
check("intercept 115,017", B0 == 115017)
check("slope 73.77", B1 == 73.77)
check("slope 73.771", round(b1, 3) == 73.771)
check("SE 11.175", round(se1, 3) == 11.175)
check("t = 6.60", f"{t1:.2f}" == "6.60")
check("intercept t > 5", t0 > 5)
check("p < 0.001", float(m.pvalue()["size"]) < 0.001)
check("R2 0.6175", f"{r2:.4f}" == "0.6175")
check("R2 ~62%", round(r2 * 100) == 62)
check("R2 remainder ~38%", round((1 - r2) * 100) == 38)
check("bedrooms R2 ~0.18", f"{r2_bed:.2f}" == "0.18")
check("RMSE 22,724 (~$22,700)", round(rmse) == 22724 and round(rmse, -2) == 22700)
check("mean price 253,910", round(d.price.mean()) == 253910)
check("mean size 1,883", round(d["size"].mean()) == 1883)
check("size range 1,400-3,300", (d["size"].min(), d["size"].max()) == (1400, 3300))
check("price per sq ft ~135", round(d.price.mean() / d["size"].mean()) == 135)
check("pred 2000 = 262,557", round(pred(2000)) == 262557)
check("resid 270k = +7,443", round(270000 - pred(2000)) == 7443)
check("270k - intercept = 154,983", 270000 - B0 == 154983)
check("pred 2500 = 299,442", round(pred(2500)) == 299442)
check("slope*2500 = 184,425", round(B1 * 2500) == 184425)
check("intercept + slope = 115,091", round(B0 + B1) == 115091)
check("300 sq ft diff = 22,131", round(B1 * 300) == 22131)
check("intercept + 22,131 = 137,148", round(B0 + B1 * 300) == 137148)
check("pred 6000 ~ 557,600", round(pred(6000), -2) == 557600)
check("100 sq ft = 7,377 (~7,400)", round(B1 * 100) == 7377)
check("per-100 slope 7,377 (exact)", round(b1 * 100) == 7377)
check("SE/coef ~0.15", f"{se1 / b1:.2f}" == "0.15")
check("coef*SE ~824", round(b1 * se1) == 824)
check("practice: resid -5,000", 75000 - (20000 + 5000 * 12) == -5000)
check("practice: t = 2.4/0.8 = 3.0", round(2.4 / 0.8, 6) == 3.0)
check("practice: pred 100,000", 20000 + 5000 * 16 == 100000)
check("practice: diff 20,000", 5000 * 4 == 20000)
check("practice: 12 -> 0.012", abs(12 / 1000 - 0.012) < 1e-12)

# ---------------------------------------------------------------- 3. CLAIMS
check("RMSE is ~9% of mean price (E22 distractor '38% off' is false)", round(rmse / d.price.mean(), 2) == 0.09)
check("age NOT an omitted-variable example: |r(size, age)| < 0.2", abs(d["size"].corr(d["age"])) < 0.2)
check("row order tracks price (file sorted by price), so not a 'random' distractor", d.price.reset_index(drop=True).corr(pd.Series(range(len(d)))) > 0.8)

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
