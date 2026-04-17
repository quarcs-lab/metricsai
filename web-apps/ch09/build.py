"""Build the Chapter 09 interactive dashboard.

Reads AED_EARNINGS.DTA (171 workers, earnings~education), AED_SP500INDEX.DTA
(S&P 500 1927-2019), and the Mendez 2020 convergence-clubs dataset, pre-computes
OLS for four model specifications (lin-lin, log-lin, log-log, lin-log) and
exponential growth regressions, and injects a compact JSON blob into
template.html -> dashboard.html.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE = HERE / "template.html"
OUT_FILE = HERE / "dashboard.html"

CONVERGENCE_URL = (
    "https://raw.githubusercontent.com/quarcs-lab/mendez2020-convergence-clubs-code-data"
    "/master/assets/dat.csv"
)
CONVERGENCE_CACHE = DATA_DIR / "mendez2020_convergence.csv"


def ols_fit(x: np.ndarray, y: np.ndarray) -> dict:
    """Compute OLS regression y = b1 + b2*x and return stats."""
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    n = len(x)
    xbar = float(x.mean())
    ybar = float(y.mean())
    SSx = float(((x - xbar) ** 2).sum())
    SSxy = float(((x - xbar) * (y - ybar)).sum())
    b2 = SSxy / SSx
    b1 = ybar - b2 * xbar
    yhat = b1 + b2 * x
    residuals = y - yhat
    RSS = float((residuals ** 2).sum())
    se = float(np.sqrt(RSS / (n - 2)))
    se_b2 = se / np.sqrt(SSx)
    SST = float(((y - ybar) ** 2).sum())
    R2 = 1 - RSS / SST if SST > 0 else 0.0
    return {
        "b1": round(b1, 4),
        "b2": round(b2, 4),
        "se_b2": round(se_b2, 4),
        "se": round(se, 4),
        "R2": round(R2, 4),
        "n": n,
        "xbar": round(xbar, 4),
        "ybar": round(ybar, 4),
        "SSx": round(SSx, 4),
        "RSS": round(RSS, 2),
    }


def load_earnings() -> dict:
    """Load earnings-education data and pre-compute 4 model specifications."""
    df = pd.read_stata(DATA_DIR / "AED_EARNINGS.DTA")

    earnings = df["earnings"].values
    education = df["education"].values
    ln_earnings = np.log(earnings)
    ln_education = np.log(education)

    # Four model specifications
    m1_linlin = ols_fit(education, earnings)
    m2_loglin = ols_fit(education, ln_earnings)
    m3_loglog = ols_fit(ln_education, ln_earnings)
    m4_linlog = ols_fit(ln_education, earnings)

    return {
        "education": [round(float(v), 2) for v in education],
        "earnings": [round(float(v), 2) for v in earnings],
        "lnEarnings": [round(float(v), 4) for v in ln_earnings],
        "lnEducation": [round(float(v), 4) for v in ln_education],
        "models": {
            "linlin": m1_linlin,
            "loglin": m2_loglin,
            "loglog": m3_loglog,
            "linlog": m4_linlog,
        },
    }


def load_sp500() -> dict:
    """Load S&P 500 data and compute exponential growth regression."""
    df = pd.read_stata(DATA_DIR / "AED_SP500INDEX.DTA")

    year = df["year"].values.astype(float)
    sp500 = df["sp500"].values
    lnsp500 = np.log(sp500)

    # Exponential growth model: ln(sp500) = b1 + b2*year
    growth_reg = ols_fit(year, lnsp500)

    return {
        "year": [int(v) for v in year],
        "sp500": [round(float(v), 2) for v in sp500],
        "lnsp500": [round(float(v), 4) for v in lnsp500],
        "growthReg": growth_reg,
    }


def load_convergence() -> dict:
    """Load convergence clubs 2014 cross-section for case study widget."""
    if CONVERGENCE_CACHE.exists():
        df = pd.read_csv(CONVERGENCE_CACHE)
    else:
        df = pd.read_csv(CONVERGENCE_URL)
        df.to_csv(CONVERGENCE_CACHE, index=False)
        print(f"[cache] saved {CONVERGENCE_CACHE.relative_to(ROOT)}")

    # Use 2014 cross-section
    df2014 = df[df["year"] == 2014].dropna(subset=["lp", "kl", "h"]).copy()

    lp = df2014["lp"].values
    kl = df2014["kl"].values
    h = df2014["h"].values
    ln_lp = np.log(lp)
    ln_kl = np.log(kl)

    # Log-log model: ln(lp) ~ ln(kl)
    loglog_kl = ols_fit(ln_kl, ln_lp)
    # Log-linear model: ln(lp) ~ h
    loglin_h = ols_fit(h, ln_lp)

    return {
        "countries": df2014["country"].tolist(),
        "lp": [round(float(v), 2) for v in lp],
        "kl": [round(float(v), 2) for v in kl],
        "h": [round(float(v), 4) for v in h],
        "lnLp": [round(float(v), 4) for v in ln_lp],
        "lnKl": [round(float(v), 4) for v in ln_kl],
        "loglogKl": loglog_kl,
        "loglinH": loglin_h,
    }


def build_data() -> dict:
    earn = load_earnings()
    sp = load_sp500()
    conv = load_convergence()
    return {
        "earnings": earn,
        "sp500": sp,
        "convergence": conv,
        "meta": {
            "chapter": "Chapter 09: Models with Natural Logarithms",
            "book": "metricsAI: An Introduction to Econometrics with Python and AI in the Cloud",
            "author": "Carlos Mendez",
        },
    }


def main() -> None:
    if not TEMPLATE.exists():
        raise SystemExit(f"Template not found: {TEMPLATE}")

    data = build_data()
    data_json = json.dumps(data, separators=(",", ":"), ensure_ascii=False)

    template = TEMPLATE.read_text(encoding="utf-8")
    if "{{DATA_JSON}}" not in template:
        raise SystemExit("Placeholder {{DATA_JSON}} not found in template")

    rendered = template.replace("{{DATA_JSON}}", data_json)
    OUT_FILE.write_text(rendered, encoding="utf-8")

    size_kb = OUT_FILE.stat().st_size / 1024
    e = data["earnings"]
    sp = data["sp500"]
    conv = data["convergence"]
    n_earn = e["models"]["linlin"]["n"]
    n_sp = len(sp["year"])
    n_conv = len(conv["countries"])

    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")
    print(f"[check] earnings: {n_earn} observations")
    print(
        f"[check] lin-lin: b2={e['models']['linlin']['b2']:.2f}, "
        f"log-lin: b2={e['models']['loglin']['b2']:.4f}, "
        f"log-log: b2={e['models']['loglog']['b2']:.4f}, "
        f"lin-log: b2={e['models']['linlog']['b2']:.2f}"
    )
    print(f"[check] S&P 500: {n_sp} years, growth rate={sp['growthReg']['b2']:.6f}")
    print(
        f"[check] convergence: {n_conv} countries, "
        f"elasticity(kl)={conv['loglogKl']['b2']:.4f}, "
        f"semi-elast(h)={conv['loglinH']['b2']:.4f}"
    )


if __name__ == "__main__":
    main()
