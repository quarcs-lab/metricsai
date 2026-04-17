"""Build the Chapter {{CHAPTER_NUMBER}} interactive dashboard.

Reads the chapter's datasets, produces a JSON payload, and injects it into
template.html, writing the final self-contained HTML to dashboard.html.

Pattern notes (do not delete):

- Keep this script OFFLINE. External fetches belong in separate scripts.
- Every dataset loader returns a serializable dict — lists of numbers and
  ISO-date strings, no pandas objects. Pre-round values to keep payload small.
- Timestamps must be ISO date strings ("YYYY-MM-DD") so Plotly parses them.
- NaN / NA values must be converted to None; JSON doesn't accept NaN.
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def iso_dates(series: pd.Series) -> list[str]:
    return [d.strftime("%Y-%m-%d") for d in pd.to_datetime(series)]


def summary_stats(values: list[float]) -> dict:
    arr = np.asarray([v for v in values if v is not None], dtype=float)
    n = len(arr)
    mean = float(arr.mean())
    std = float(arr.std(ddof=1))
    centered = arr - mean
    skew = float(((centered ** 3).mean()) / (std ** 3)) if std > 0 else 0.0
    kurt = float(((centered ** 4).mean()) / (std ** 4) - 3) if std > 0 else 0.0
    return {
        "n": n,
        "mean": mean,
        "median": float(np.median(arr)),
        "std": std,
        "min": float(arr.min()),
        "max": float(arr.max()),
        "q1": float(np.quantile(arr, 0.25)),
        "q3": float(np.quantile(arr, 0.75)),
        "skew": skew,
        "kurt": kurt,
    }


def clean_nums(series: pd.Series, decimals: int = 2) -> list[float | None]:
    """Convert a pandas Series to a JSON-safe list (None for NaN, rounded floats)."""
    return [None if pd.isna(v) else round(float(v), decimals) for v in series]


# ---------------------------------------------------------------------------
# Dataset loaders — one function per dataset. Fill these in.
# ---------------------------------------------------------------------------

# TODO: replace the examples below with the chapter's actual loaders.
# Each returns a JSON-serializable dict suitable for embedding.

def load_example() -> dict:
    """TODO: replace with real loader. Returns {'values': [...], 'meta': ...}."""
    # df = pd.read_stata(DATA_DIR / "CHAPTER_SPECIFIC.DTA")
    # return {
    #     "values": [float(v) for v in df["somecol"].tolist()],
    # }
    return {"values": []}


# ---------------------------------------------------------------------------
# Assemble the JSON payload
# ---------------------------------------------------------------------------

def build_data() -> dict:
    # TODO: call each dataset loader and compose the payload.
    return {
        # "earnings": [...],
        # "gdp": {"dates": [...], "values": [...]},
        # Add one key per dataset or logical group.
        #
        # "summary": {
        #     "earnings": summary_stats(earnings),
        #     ...
        # },
        "meta": {
            "chapter": "Chapter {{CHAPTER_NUMBER}}: {{CHAPTER_TITLE}}",
            "book": "metricsAI: An Introduction to Econometrics with Python and AI in the Cloud",
            "author": "Carlos Mendez",
        },
    }


# ---------------------------------------------------------------------------
# Template injection
# ---------------------------------------------------------------------------

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
    print(f"[ok] wrote {OUT_FILE.relative_to(ROOT)} ({size_kb:.1f} KB)")

    # TODO: add chapter-specific sanity-check prints that match values quoted
    # in the chapter prose. Example:
    # s = data["summary"]["earnings"]
    # print(f"[check] earnings mean={s['mean']:.2f} (chapter says 41,412.69)")


if __name__ == "__main__":
    main()
