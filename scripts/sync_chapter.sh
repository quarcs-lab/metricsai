#!/bin/bash
# sync_chapter.sh — Sync a single chapter across all output formats
# Usage: scripts/sync_chapter.sh notebooks_quarto/ch05_Bivariate_Data_Summary.qmd
#
# Triggered automatically by Claude Code hook after editing a .qmd file.
# Updates: notebooks_colab (.ipynb), notebooks_md (.md), book/_book (.html)

set -e

FILE="$1"
if [[ -z "$FILE" || ! "$FILE" == *.qmd ]]; then
    echo "[sync] Skipping: not a .qmd file"
    exit 0
fi

# Extract chapter ID (e.g., "ch05" from "notebooks_quarto/ch05_Bivariate_Data_Summary.qmd")
BASENAME=$(basename "$FILE" .qmd)
CHAPTER_ID=$(echo "$BASENAME" | cut -d'_' -f1)

# Resolve project root (script lives in scripts/)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# Activate virtual environment if available
if [[ -f ".venv/bin/activate" ]]; then
    source .venv/bin/activate
fi

echo "[sync] Syncing $CHAPTER_ID ($BASENAME)..."

# 1. Export to Colab notebook (.ipynb)
echo "[sync] 1/3 Exporting to notebooks_colab/ (.ipynb)..."
python3 scripts/export_qmd_to_ipynb.py "$CHAPTER_ID" 2>&1 | tail -1

# 2. Convert to Markdown (.md)
echo "[sync] 2/3 Converting to notebooks_md/ (.md)..."
python3 -c "
import re
with open('notebooks_quarto/${BASENAME}.qmd', 'r') as f:
    content = f.read()
content = re.sub(r'\`\`\`\{python\}', '\`\`\`python', content)
content = re.sub(r'^#\|.*\n', '', content, flags=re.MULTILINE)
with open('notebooks_md/${BASENAME}.md', 'w') as f:
    f.write(content)
print('[ok] notebooks_md/${BASENAME}.md')
"

# 3. Render book chapter (.html)
echo "[sync] 3/3 Rendering book chapter (.html)..."
cd book && quarto render "notebooks_quarto/${BASENAME}.qmd" 2>&1 | tail -1
cd "$PROJECT_ROOT"

echo "[sync] Done: $CHAPTER_ID synced across all formats."
