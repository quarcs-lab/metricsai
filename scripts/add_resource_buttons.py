#!/usr/bin/env python3
"""
Add resource buttons (AI Video, AI Slides, Cameron Slides, Quiz, AI Tutor)
below the Colab badge in each chapter notebook's first cell.

Inserts an HTML <div class="chapter-resources"> block after the Colab badge line.

Usage:
    python3 scripts/add_resource_buttons.py [--dry-run]
"""

import json
import sys
from pathlib import Path

NOTEBOOK_DIR = Path(__file__).parent.parent / "notebooks_colab"

# URL data for all 17 chapters, extracted from index.html
CHAPTER_DATA = {
    1: {
        "video": "RyE01v-zliM",
        "slides": "s01-analysis-of-economics-data-pdf",
        "cameron": "traedv1_01",
        "quiz": "69715fdb60956f50e60276b9",
        "tutor": "6971625960956f50e6028155",
    },
    2: {
        "video": "qegfQaM9UGE",
        "slides": "s02-univariate-data-summary-pdf",
        "cameron": "traedv1_02",
        "quiz": "6978644a2f5d08069e046930",
        "tutor": "69789c1e2f5d08069e06f856",
    },
    3: {
        "video": "pnv9ff_3hrI",
        "slides": "s03-the-sample-mean-pdf",
        "cameron": "traedv1_03",
        "quiz": "697864e12f5d08069e0471b5",
        "tutor": "69789d252f5d08069e06fdad",
    },
    4: {
        "video": "8wn00FpUz38",
        "slides": "s04-statistical-inference-for-the-mean-pdf",
        "cameron": "traedv1_04",
        "quiz": "6978656c2f5d08069e0479cb",
        "tutor": "69789d9f2f5d08069e06ffa5",
    },
    5: {
        "video": "sVT1KfjoZQg",
        "slides": "s05-bivariate-data-summary-pdf",
        "cameron": "traedv1_05",
        "quiz": "697865de2f5d08069e0482cc",
        "tutor": "69789e4c2f5d08069e0704c6",
    },
    6: {
        "video": "hSv0usYmlZc",
        "slides": "s06-the-least-squares-estimator-pdf",
        "cameron": "traedv1_06",
        "quiz": "697866592f5d08069e048b48",
        "tutor": "69789eae2f5d08069e070694",
    },
    7: {
        "video": "iMi1Fa-PYLs",
        "slides": "s07-statistical-inference-for-bivariate-regression-pdf",
        "cameron": "traedv1_07",
        "quiz": "697866e42f5d08069e04934f",
        "tutor": "69789f042f5d08069e070885",
    },
    8: {
        "video": "2hVGYcT9YE8",
        "slides": "s08-case-studies-for-bivariate-regression-pdf",
        "cameron": "traedv1_08",
        "quiz": "697867452f5d08069e049d1f",
        "tutor": "6978a02d2f5d08069e0711d6",
    },
    9: {
        "video": "rPy6m8_Wg4c",
        "slides": "s09-models-with-natural-logarithms-pdf",
        "cameron": "traedv1_09",
        "quiz": "697867a22f5d08069e04a411",
        "tutor": "6978a07f2f5d08069e0713c6",
    },
    10: {
        "video": "9398KshS_JA",
        "slides": "s10-data-summary-for-multiple-regression-pdf",
        "cameron": "traedv1_10",
        "quiz": "697868212f5d08069e04add5",
        "tutor": "6978a0fd2f5d08069e0715f8",
    },
    11: {
        "video": "yvcSMmluY5Y",
        "slides": "s11-statistical-inference-for-multiple-regression-pdf",
        "cameron": "traedv1_11",
        "quiz": "697868ad2f5d08069e04b748",
        "tutor": "6978a1572f5d08069e071814",
    },
    12: {
        "video": "0rM5db2lTPo",
        "slides": "s12-further-topics-in-multiple-regression-pdf",
        "cameron": "traedv1_12",
        "quiz": "6978693a2f5d08069e04bed3",
        "tutor": "6978a1a32f5d08069e0719da",
    },
    13: {
        "video": "auS4yrgbAQA",
        "slides": "s13-case-studies-for-multiple-regression-pdf",
        "cameron": "traedv1_13",
        "quiz": "697869f02f5d08069e04c94f",
        "tutor": "6978a2122f5d08069e071d09",
    },
    14: {
        "video": "Rkx1cY8_BBY",
        "slides": "s14-regression-with-indicator-variables-pdf",
        "cameron": "traedv1_14",
        "quiz": "69786a6a2f5d08069e04cf09",
        "tutor": "6978a2782f5d08069e071ecb",
    },
    15: {
        "video": "XJv1bfr9BI4",
        "slides": "s15-regression-with-transformed-variables-pdf",
        "cameron": "traedv1_15",
        "quiz": "69786b142f5d08069e04d9ed",
        "tutor": "6978a2c92f5d08069e072021",
    },
    16: {
        "video": "3JVkwVXsyr0",
        "slides": "s16-checking-the-model-and-data-pdf",
        "cameron": "traedv1_16",
        "quiz": "69786b812f5d08069e04e07f",
        "tutor": "6978a3122f5d08069e07219f",
    },
    17: {
        "video": "ZtjIHX6JYyM",
        "slides": "s17-panel-data-time-series-data-causation-pdf",
        "cameron": "traedv1_17",
        "quiz": "69786c262f5d08069e04e9a8",
        "tutor": "6978a3772f5d08069e0723a7",
    },
}


def build_html_block(ch_num: int) -> str:
    """Build the HTML resource buttons block for a given chapter."""
    d = CHAPTER_DATA[ch_num]
    lines = [
        '\n',
        '<div class="chapter-resources">\n',
        f'<a href="https://www.youtube.com/watch?v={d["video"]}" target="_blank" class="resource-btn">\U0001f3ac AI Video</a>\n',
        f'<a href="https://carlos-mendez.my.canva.site/{d["slides"]}" target="_blank" class="resource-btn">\u2728 AI Slides</a>\n',
        f'<a href="https://cameron.econ.ucdavis.edu/aed/{d["cameron"]}" target="_blank" class="resource-btn">\U0001f4ca Cameron Slides</a>\n',
        f'<a href="https://app.edcafe.ai/quizzes/{d["quiz"]}" target="_blank" class="resource-btn">\u270f\ufe0f Quiz</a>\n',
        f'<a href="https://app.edcafe.ai/chatbots/{d["tutor"]}" target="_blank" class="resource-btn">\U0001f916 AI Tutor</a>\n',
        '</div>\n',
    ]
    return lines


def find_colab_badge_line(source: list) -> int:
    """Find the index of the line containing the Colab badge in cell source."""
    for i, line in enumerate(source):
        if "colab-badge" in line and "[![" in line:
            return i
    return -1


def already_has_buttons(source: list) -> bool:
    """Check if the cell already contains the resource buttons."""
    for line in source:
        if 'class="chapter-resources"' in line:
            return True
    return False


def process_notebook(nb_path: Path, ch_num: int, dry_run: bool = False) -> bool:
    """Add resource buttons to a notebook's cell 0. Returns True if modified."""
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb.get("cells", [])
    if not cells:
        print(f"  WARNING: No cells found!")
        return False

    cell0 = cells[0]
    if cell0.get("cell_type") != "markdown":
        print(f"  WARNING: Cell 0 is not markdown!")
        return False

    source = cell0.get("source", [])

    if already_has_buttons(source):
        print(f"  Already has buttons, skipping.")
        return False

    badge_idx = find_colab_badge_line(source)
    if badge_idx < 0:
        print(f"  WARNING: Colab badge not found in cell 0!")
        return False

    # Insert the HTML block after the Colab badge line
    html_lines = build_html_block(ch_num)
    new_source = source[:badge_idx + 1] + html_lines + source[badge_idx + 1:]
    cell0["source"] = new_source

    if not dry_run:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
            f.write("\n")

    return True


def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("=== DRY RUN MODE (no files will be modified) ===\n")

    modified = 0
    for ch_num in range(1, 18):
        pattern = f"ch{ch_num:02d}_*.ipynb"
        matches = list(NOTEBOOK_DIR.glob(pattern))
        if not matches:
            print(f"CH{ch_num:02d}: notebook not found!")
            continue

        nb_path = matches[0]
        print(f"CH{ch_num:02d} ({nb_path.name}):", end=" ")
        if process_notebook(nb_path, ch_num, dry_run=dry_run):
            print("buttons added.")
            modified += 1

    print(f"\n{'='*60}")
    print(f"Total: {modified} notebooks modified")
    if dry_run:
        print("(DRY RUN - no files were modified)")


if __name__ == "__main__":
    main()
