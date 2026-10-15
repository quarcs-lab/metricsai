#!/usr/bin/env python3
"""Fact-check for quizzes/banks/CHAPTER.json: every number and data claim in the bank.

Copy to quizzes/checks/CHAPTER_factcheck.py, set CHAPTER, then fill the three blocks:

  1. FACTS   load the chapter's datasets and compute EXACT values (print a facts sheet).
             Write the bank only from these printed values, rounding from the exact
             value (never re-round an already rounded number).
  2. CHECKS  one assert per number quoted in the bank, in the same rounding the bank uses.
             Include arithmetic used in options (predictions, differences, distractor values).
  3. CLAIMS  one assert per statement about how variables relate in the data
             (signs, correlations, orderings, ranges). Chapter prose is not evidence:
             ch01's "bigger houses tend to be newer" is false in AED_HOUSE (r = 0.08).

Run:  python3 quizzes/checks/CHAPTER_factcheck.py      (exit 1 on any failure)
"""

import json
import re
import sys
from pathlib import Path

import pandas as pd

CHAPTER = "chNN"  # <- set me
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
# import pyfixest as pf
# d = load("AED_HOUSE.DTA")
# m = pf.feols("price ~ size", data=d)
# b0, b1 = m.coef()["Intercept"], m.coef()["size"]
# print(f"b0={b0:.6f} b1={b1:.6f} se1={m.se()['size']:.6f} t1={m.tstat()['size']:.6f} r2={m._r2:.6f}")

# ---------------------------------------------------------------- 2. CHECKS
# check("slope 73.77", round(b1, 2) == 73.77)
# check("t = 6.60", f"{m.tstat()['size']:.2f}" == "6.60")
# check("pred 2000 = 262,557 (rounded equation)", round(round(b0) + round(b1, 2) * 2000) == 262557)

# ---------------------------------------------------------------- 3. CLAIMS
# check("size and age essentially unrelated (|r| < 0.2)", abs(d["size"].corr(d["age"])) < 0.2)

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
