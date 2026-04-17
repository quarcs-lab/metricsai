"""Build the Chapter 08 interactive dashboard.

Reads AED_HEALTH2009.DTA, AED_CAPM.DTA, and AED_GDPUNEMPLOY.DTA,
pre-computes OLS regressions and summary statistics, and injects a compact
JSON blob into template.html -> dashboard.html.
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

GITHUB_DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"


def ols_fit(x: np.ndarray, y: np.ndarray) -> dict:
    """Compute OLS regression y = b1 + b2*x and return stats."""
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
    SST = float(((y - ybar) ** 2).sum())
    se = float(np.sqrt(RSS / (n - 2)))
    se_b2 = se / np.sqrt(SSx)
    se_b1 = se * np.sqrt((1 / n) + (xbar ** 2) / SSx)
    R2 = 1 - RSS / SST if SST > 0 else 0.0
    t_b2 = b2 / se_b2
    t_b1 = b1 / se_b1
    return {
        "b1": round(b1, 6),
        "b2": round(b2, 6),
        "se_b1": round(se_b1, 6),
        "se_b2": round(se_b2, 6),
        "t_b1": round(t_b1, 4),
        "t_b2": round(t_b2, 4),
        "se": round(se, 4),
        "R2": round(R2, 4),
        "n": n,
        "xbar": round(xbar, 4),
        "ybar": round(ybar, 4),
        "SSx": round(SSx, 4),
        "RSS": round(RSS, 4),
    }


def load_health() -> dict:
    """Load AED_HEALTH2009.DTA: 34 OECD countries."""
    df = pd.read_stata(DATA_DIR / "AED_HEALTH2009.DTA")

    # Life expectancy regression: lifeexp ~ hlthpc
    x_life = df["hlthpc"].values.astype(float)
    y_life = df["lifeexp"].values.astype(float)
    reg_life = ols_fit(x_life, y_life)

    # Infant mortality regression: infmort ~ hlthpc
    x_inf = df["hlthpc"].values.astype(float)
    y_inf = df["infmort"].values.astype(float)
    reg_inf = ols_fit(x_inf, y_inf)

    # Health expenditure ~ GDP (all countries)
    x_gdp = df["gdppc"].values.astype(float)
    y_hlth = df["hlthpc"].values.astype(float)
    reg_hlth_all = ols_fit(x_gdp, y_hlth)

    # Health expenditure ~ GDP (excluding USA and Luxembourg)
    mask = ~df["code"].isin(["USA", "LUX"])
    df_sub = df[mask]
    x_gdp_sub = df_sub["gdppc"].values.astype(float)
    y_hlth_sub = df_sub["hlthpc"].values.astype(float)
    reg_hlth_sub = ols_fit(x_gdp_sub, y_hlth_sub)

    return {
        "codes": [str(c).strip() for c in df["code"].tolist()],
        "hlthpc": [round(float(v), 2) for v in df["hlthpc"]],
        "lifeexp": [round(float(v), 2) for v in df["lifeexp"]],
        "infmort": [round(float(v), 2) for v in df["infmort"]],
        "gdppc": [round(float(v), 2) for v in df["gdppc"]],
        "regLifeexp": reg_life,
        "regInfmort": reg_inf,
        "regHlthAll": reg_hlth_all,
        "regHlthSub": reg_hlth_sub,
        "outlierCodes": ["USA", "LUX"],
    }


def load_capm() -> dict:
    """Load AED_CAPM.DTA: monthly stock returns 1983-2013."""
    df = pd.read_stata(DATA_DIR / "AED_CAPM.DTA")

    # Market excess return and stock excess returns
    rm_rf = df["rm_rf"].values.astype(float)

    stocks = {}
    for col, label in [("rko_rf", "Coca-Cola"), ("rtgt_rf", "Target"), ("rwmt_rf", "Walmart")]:
        y = df[col].values.astype(float)
        reg = ols_fit(rm_rf, y)
        stocks[col] = {
            "label": label,
            "values": [round(float(v), 6) for v in y],
            "reg": reg,
        }

    return {
        "rm_rf": [round(float(v), 6) for v in rm_rf],
        "n": len(rm_rf),
        "stocks": stocks,
    }


def load_okun() -> dict:
    """Load AED_GDPUNEMPLOY.DTA: annual US data 1961-2019."""
    df = pd.read_stata(DATA_DIR / "AED_GDPUNEMPLOY.DTA")
    df = df.dropna(subset=["rgdpgrowth", "uratechange"]).reset_index(drop=True)

    x = df["uratechange"].values.astype(float)
    y = df["rgdpgrowth"].values.astype(float)
    reg = ols_fit(x, y)

    return {
        "years": [int(v) for v in df["year"]],
        "rgdpgrowth": [round(float(v), 4) for v in y],
        "uratechange": [round(float(v), 4) for v in x],
        "reg": reg,
    }


def build_data() -> dict:
    health = load_health()
    capm = load_capm()
    okun = load_okun()

    return {
        "health": health,
        "capm": capm,
        "okun": okun,
        "meta": {
            "chapter": "Chapter 08: Case Studies for Bivariate Regression",
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
    h = data["health"]
    c = data["capm"]
    o = data["okun"]
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")
    print(f"[check] health: {len(h['codes'])} countries")
    print(
        f"[check] lifeexp reg: b1={h['regLifeexp']['b1']:.4f} "
        f"b2={h['regLifeexp']['b2']:.6f} R2={h['regLifeexp']['R2']:.4f}"
    )
    print(
        f"[check] infmort reg: b1={h['regInfmort']['b1']:.4f} "
        f"b2={h['regInfmort']['b2']:.6f} R2={h['regInfmort']['R2']:.4f}"
    )
    print(
        f"[check] hlth~gdp all: b2={h['regHlthAll']['b2']:.4f} R2={h['regHlthAll']['R2']:.4f}"
    )
    print(
        f"[check] hlth~gdp sub: b2={h['regHlthSub']['b2']:.4f} R2={h['regHlthSub']['R2']:.4f}"
    )
    ko_reg = c["stocks"]["rko_rf"]["reg"]
    print(
        f"[check] CAPM KO: alpha={ko_reg['b1']:.4f} beta={ko_reg['b2']:.4f} R2={ko_reg['R2']:.4f}"
    )
    print(
        f"[check] Okun: b1={o['reg']['b1']:.4f} b2={o['reg']['b2']:.4f} R2={o['reg']['R2']:.4f}"
    )


if __name__ == "__main__":
    main()
