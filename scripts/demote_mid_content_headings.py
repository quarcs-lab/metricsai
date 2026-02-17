#!/usr/bin/env python3
"""
Demote non-numbered, non-structural ## headings to ### in metricsAI notebooks.

This script processes ch01-ch17 notebooks and:
1. Identifies ## headings that are NOT section-numbered (X.Y) and NOT structural
   (Chapter Overview, Setup, Key Takeaways, Practice Exercises, Case Studies)
2. Demotes them from ## to ###
3. Cascades sub-headings within the demoted heading's zone:
   ### → ####, #### → #####

Usage:
    python3 scripts/demote_mid_content_headings.py [--dry-run]
"""

import json
import re
import sys
from pathlib import Path

NOTEBOOK_DIR = Path(__file__).parent.parent / "notebooks_colab"

# Structural headings to keep at ## level (case-insensitive)
STRUCTURAL_HEADINGS = {
    "chapter overview",
    "setup",
    "key takeaways",
    "practice exercises",
    "case studies",
}

# Pattern for section-numbered headings: ## X.Y or ## X.Y:
NUMBERED_PATTERN = re.compile(r"^##\s+\d+\.\d+")


def is_structural_heading(line: str) -> bool:
    """Check if a ## heading is a structural heading (keep at ##)."""
    # Remove the ## prefix and strip
    text = line.lstrip("#").strip()
    # Also handle optional section numbers before structural names
    # e.g., "## 1.10 Practice Exercises" should be kept
    text_lower = text.lower()
    for name in STRUCTURAL_HEADINGS:
        if name in text_lower:
            return True
    return False


def is_numbered_heading(line: str) -> bool:
    """Check if a ## heading has a section number (X.Y format)."""
    return bool(NUMBERED_PATTERN.match(line))


def should_keep_h2(line: str) -> bool:
    """Return True if this ## heading should remain at ## level."""
    return is_numbered_heading(line) or is_structural_heading(line)


def classify_h2_line(line: str) -> str:
    """Classify a ## line as 'keep' or 'demote'."""
    if should_keep_h2(line):
        return "keep"
    return "demote"


def process_notebook(nb_path: Path, dry_run: bool = False) -> list:
    """Process a single notebook, demoting mid-content ## headings.

    Returns a list of change descriptions.
    """
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    changes = []
    cells = nb.get("cells", [])

    # Phase 1: Identify which cells contain ## headings and classify them.
    # Build a map of cell_index -> list of (line_index, heading_level, action)
    # Then determine cascading zones.

    # First pass: find all ## headings and classify
    h2_info = []  # (cell_idx, line_idx, line_text, action)
    for ci, cell in enumerate(cells):
        if cell.get("cell_type") != "markdown":
            continue
        source = cell.get("source", [])
        for li, line in enumerate(source):
            stripped = line.rstrip("\n")
            # Match exactly ## (not ### or more)
            if re.match(r"^## (?!#)", stripped):
                action = classify_h2_line(stripped)
                h2_info.append((ci, li, stripped, action))

    # Phase 2: Determine cascading zones.
    # A "demote zone" starts at a demoted ## heading and extends until the next
    # ## heading (of any kind) in a subsequent cell.
    # Within a demote zone, ### → ####, #### → #####

    # Build set of cells in demote zones (excluding the ## heading cell itself,
    # since that's handled directly)
    demote_zones = []  # list of (start_cell_idx, end_cell_idx_exclusive)

    for i, (ci, li, text, action) in enumerate(h2_info):
        if action != "demote":
            continue
        # Zone starts at this cell (the ## heading cell)
        start_ci = ci
        # Zone ends at the next ## heading's cell (exclusive)
        if i + 1 < len(h2_info):
            end_ci = h2_info[i + 1][0]
        else:
            end_ci = len(cells)
        demote_zones.append((start_ci, end_ci))

    # Phase 3: Apply changes
    # Track which cells are in demote zones for cascading
    def cell_in_demote_zone(ci: int) -> bool:
        for start, end in demote_zones:
            if start <= ci < end:
                return True
        return False

    # Set of (cell_idx, line_idx) for ## headings being demoted
    demote_h2_set = set()
    for ci, li, text, action in h2_info:
        if action == "demote":
            demote_h2_set.add((ci, li))

    modified = False
    for ci, cell in enumerate(cells):
        if cell.get("cell_type") != "markdown":
            continue
        source = cell.get("source", [])
        new_source = []
        for li, line in enumerate(source):
            stripped = line.rstrip("\n")
            newline_suffix = line[len(stripped):]

            # Check if this is a ## heading being demoted
            if (ci, li) in demote_h2_set:
                new_line = "#" + line  # ## X → ### X
                new_source.append(new_line)
                changes.append(f"  ## → ###: {stripped.strip()}")
                modified = True
                continue

            # Check if this cell is in a demote zone (for cascading)
            if cell_in_demote_zone(ci) and (ci, li) not in demote_h2_set:
                # Cascade ### → ####
                if re.match(r"^### (?!#)", stripped):
                    # But only if this ### is not itself a structural heading
                    new_line = "#" + line  # ### X → #### X
                    new_source.append(new_line)
                    changes.append(f"  ### → ####: {stripped.strip()}")
                    modified = True
                    continue
                # Cascade #### → #####
                elif re.match(r"^#### (?!#)", stripped):
                    new_line = "#" + line  # #### X → ##### X
                    new_source.append(new_line)
                    changes.append(f"  #### → #####: {stripped.strip()}")
                    modified = True
                    continue

            new_source.append(line)

        cell["source"] = new_source

    if modified and not dry_run:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
            f.write("\n")

    return changes


def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("=== DRY RUN MODE (no files will be modified) ===\n")

    total_changes = 0
    chapters_modified = 0

    for ch_num in range(1, 18):
        # Find the notebook file
        pattern = f"ch{ch_num:02d}_*.ipynb"
        matches = list(NOTEBOOK_DIR.glob(pattern))
        if not matches:
            print(f"CH{ch_num:02d}: notebook not found!")
            continue

        nb_path = matches[0]
        changes = process_notebook(nb_path, dry_run=dry_run)

        if changes:
            chapters_modified += 1
            total_changes += len(changes)
            print(f"CH{ch_num:02d} ({nb_path.name}): {len(changes)} changes")
            for c in changes:
                print(c)
            print()
        else:
            print(f"CH{ch_num:02d}: no changes needed")

    print(f"\n{'='*60}")
    print(f"Total: {total_changes} heading changes across {chapters_modified} chapters")
    if dry_run:
        print("(DRY RUN - no files were modified)")


if __name__ == "__main__":
    main()
