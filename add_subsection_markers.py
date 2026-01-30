#!/usr/bin/env python3
"""
Add fine-grained subsection markers to Python scripts for Jupyter-style execution.
Targets 10-20 lines per cell by adding descriptive # %% markers.
"""

import re
import os
from pathlib import Path

def add_subsection_markers(file_path):
    """Add fine-grained # %% markers to a Python script."""

    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    i = 0

    while i < len(lines):
        current_line = lines[i]
        next_line = lines[i + 1] if i + 1 < len(lines) else ""

        # Add the current line
        new_lines.append(current_line)

        # Check if we should add a marker after this line
        should_add_marker = False
        marker_text = ""

        # Pattern 1: After saving files (CSV, figure)
        if re.search(r'\.to_csv\(|print\(f["\'].*saved to:', current_line):
            # Check if next line is a figure creation or new data load
            if re.search(r'(fig.*=.*plt\.subplots|pd\.read_stata|pd\.read_csv|# Figure|# Table)', next_line):
                should_add_marker = True

                # Determine marker text based on next operation
                if 'pd.read_stata' in next_line or 'pd.read_csv' in next_line:
                    # Extract dataset name from URL or file path
                    match = re.search(r'["\'].*[/\\](\w+)\.(DTA|dta|csv|CSV)', next_line)
                    if match:
                        dataset = match.group(1).lower().replace('aed_', '')
                        marker_text = f"# %% Load {dataset} data"
                    else:
                        marker_text = "# %% Load data"

                elif 'fig' in next_line and 'subplots' in next_line:
                    # Look ahead to find figure description in comments
                    for j in range(i+1, min(i+5, len(lines))):
                        comment_match = re.search(r'# (Figure \d+\.\d+|Table \d+\.\d+):?\s*(.+)', lines[j])
                        if comment_match:
                            desc = comment_match.group(2).strip()
                            marker_text = f"# %% Create {desc.lower()}"
                            break
                    if not marker_text:
                        marker_text = "# %% Create figure"

        # Pattern 2: After data loading, before processing
        elif re.search(r'pd\.read_stata|pd\.read_csv', current_line):
            # Check if next few lines contain .describe(), .info(), or print statements
            for j in range(i+1, min(i+10, len(lines))):
                if re.search(r'\.(describe|info|head)\(\)|print\(', lines[j]) and not re.search(r'^# %%', lines[j-1]):
                    should_add_marker = True
                    marker_text = "# %% Explore data structure"
                    break

        # Pattern 3: After .describe() calls, before calculations
        elif re.search(r'\.describe\(\)', current_line):
            # Check if there's a calculation or transformation coming
            for j in range(i+1, min(i+10, len(lines))):
                if re.search(r'(stats\.|\.mean\(\)|\.median\(\)|\.std\(\)|=.*\()', lines[j]) and not re.search(r'print|^#', lines[j]):
                    should_add_marker = True
                    marker_text = "# %% Calculate statistics"
                    break

        # Pattern 4: Before model estimation
        elif re.search(r'ols\(|\.fit\(\)', current_line) and i > 0:
            # Check if previous line doesn't already have a marker
            if not re.search(r'^# %%', lines[i-1]):
                # Insert marker before current line
                marker_text = "# %% Estimate regression model"
                new_lines.insert(-1, f"\n{marker_text}\n\n")

        # Pattern 5: Before printing model summary
        elif re.search(r'print\(model\.summary|print\(.*\.summary\(\)', current_line):
            if i > 0 and not re.search(r'^# %%', lines[i-1]):
                marker_text = "# %% Display regression results"
                new_lines.insert(-1, f"\n{marker_text}\n\n")

        # Pattern 6: After figure close, before next major operation
        elif 'plt.close()' in current_line:
            # Check if next significant line is a new figure, data load, or calculation
            for j in range(i+1, min(i+5, len(lines))):
                if re.search(r'(fig.*=|pd\.read|# Figure|# Table|ols\(|print\(["\'].*=.*70)', lines[j]):
                    if not re.search(r'^# %%', lines[j]) and not re.search(r'^# %%', lines[j-1]):
                        should_add_marker = True
                        # Determine appropriate marker based on next operation
                        if 'pd.read' in lines[j]:
                            marker_text = "# %% Load next dataset"
                        elif 'fig' in lines[j]:
                            marker_text = "# %% Create next figure"
                        else:
                            marker_text = "# %% Continue analysis"
                        break

        # Pattern 7: Between different print section headers
        elif re.search(r'print\(["\'].*=.*70["\']\)', current_line):
            # This is a section header separator (e.g., print("=" * 70))
            # Check if this is NOT immediately after a # %% marker
            if i > 1 and not re.search(r'^# %%', lines[i-2]):
                # Check if there's actual code between this and the last marker
                code_lines = 0
                for j in range(i-1, max(0, i-20), -1):
                    if re.search(r'^# %%', lines[j]):
                        break
                    if lines[j].strip() and not lines[j].strip().startswith('#'):
                        code_lines += 1

                # Only add marker if there's been substantial code (>15 lines)
                if code_lines > 15:
                    should_add_marker = True
                    # Extract section title if available
                    section_match = re.search(r'print\(["\'](.+)["\']\)', next_line)
                    if section_match:
                        title = section_match.group(1).strip()
                        if title and not re.search(r'=+', title):
                            marker_text = f"# %% {title.capitalize()}"

        # Add marker if needed
        if should_add_marker and marker_text:
            new_lines.append(f"\n{marker_text}\n")

        i += 1

    return new_lines

def process_chapter(file_path):
    """Process a single chapter file."""
    print(f"Processing {file_path.name}...")

    # Count original markers
    with open(file_path, 'r') as f:
        original_content = f.read()
    original_markers = original_content.count('\n# %%')

    # Add new markers
    new_lines = add_subsection_markers(file_path)

    # Write back
    with open(file_path, 'w') as f:
        f.writelines(new_lines)

    # Count new markers
    with open(file_path, 'r') as f:
        new_content = f.read()
    new_markers = new_content.count('\n# %%')

    # Calculate metrics
    total_lines = len(new_lines)
    avg_lines_per_cell = total_lines / new_markers if new_markers > 0 else 0

    print(f"  ✓ {file_path.name}: {original_markers} → {new_markers} markers")
    print(f"    Total lines: {total_lines}, Avg lines/cell: {avg_lines_per_cell:.1f}")
    print()

def main():
    """Process all chapter files."""
    code_dir = Path("code_python")

    # Get all chapter files (ch01-ch17)
    chapter_files = sorted(code_dir.glob("ch[0-9][0-9]_*.py"))

    # Skip ch02 (already processed manually)
    chapter_files = [f for f in chapter_files if not f.name.startswith('ch02')]

    print(f"Found {len(chapter_files)} chapter files to process\n")
    print("=" * 70)

    for file_path in chapter_files:
        try:
            process_chapter(file_path)
        except Exception as e:
            print(f"  ✗ Error processing {file_path.name}: {e}\n")

    print("=" * 70)
    print("Processing complete!")

    # Print summary
    print("\nSummary:")
    for file_path in sorted(code_dir.glob("ch[0-9][0-9]_*.py")):
        with open(file_path, 'r') as f:
            content = f.read()
        markers = content.count('\n# %%') + (1 if content.startswith('# %%') else 0)
        lines = len(content.split('\n'))
        avg = lines / markers if markers > 0 else 0
        print(f"  {file_path.name:50s}: {markers:3d} cells, {avg:5.1f} lines/cell")

if __name__ == "__main__":
    main()
