#!/usr/bin/env python3
"""
Chapter Standard Auto-Fix Script
Applies safe, deterministic fixes to chapter notebooks
Only performs additive changes - never deletes content
"""

import json
import shutil
import sys
import glob
from pathlib import Path
from datetime import datetime

def find_notebook(chapter_prefix):
    """Find notebook file matching chapter prefix"""
    pattern = f'notebooks_colab/{chapter_prefix}_*.ipynb'
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError(f"No notebook found for {chapter_prefix}")
    return matches[0]

def backup_notebook(notebook_path):
    """
    Create timestamped backup before modifications.

    Args:
        notebook_path: Path to notebook file

    Returns:
        Path to backup file
    """
    backup_dir = Path('notebooks_colab/backups')
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    notebook_name = Path(notebook_path).stem
    backup_path = backup_dir / f"{notebook_name}_backup_{timestamp}.ipynb"

    shutil.copy(notebook_path, backup_path)
    return backup_path

def fix_visual_summary(nb, chapter_prefix):
    """
    Add missing visual summary image to Cell 0.

    Args:
        nb: Notebook dictionary
        chapter_prefix: Chapter identifier (e.g., 'ch05')

    Returns:
        Tuple of (success: bool, message: str)
    """
    if not nb['cells']:
        return False, "No cells in notebook"

    cell_0_content = ''.join(nb['cells'][0]['source'])

    # Check if already present
    if 'visual_summary' in cell_0_content.lower() and '<img' in cell_0_content:
        return False, "Visual summary already present"

    # Extract chapter number
    chapter_num = int(chapter_prefix.replace('ch', ''))

    # Create visual summary template
    template = f'''<p align="center">
  <img src="https://raw.githubusercontent.com/quarcs-lab/metricsai/main/images/ch{chapter_num:02d}_visual_summary.jpg" alt="Chapter {chapter_num:02d} Visual Summary" width="65%">
</p>

'''

    # Prepend to Cell 0
    if nb['cells'][0]['cell_type'] == 'markdown':
        nb['cells'][0]['source'].insert(0, template)
        return True, "Added visual summary image to Cell 0"
    else:
        return False, "Cell 0 is not markdown - cannot add visual summary"

def add_key_concept_placeholder(nb, section_cell_idx):
    """
    Insert placeholder Key Concept box after specified section.

    Args:
        nb: Notebook dictionary
        section_cell_idx: Cell index to insert after

    Returns:
        True if placeholder added
    """
    placeholder = {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '\n',
            '> **Key Concept**: [TODO: Add 2-3 sentence synthesis of main idea. ',
            'Focus on conceptual understanding, not procedural steps.]\n',
            '\n'
        ]
    }

    # Insert after section header
    nb['cells'].insert(section_cell_idx + 1, placeholder)
    return True

def fix_empty_closing_cell(nb):
    """
    Add empty closing cell if missing.

    Args:
        nb: Notebook dictionary

    Returns:
        True if empty cell added
    """
    # Check if last cell is empty markdown
    if nb['cells']:
        last_cell = nb['cells'][-1]
        last_content = ''.join(last_cell['source']).strip()

        if last_cell['cell_type'] == 'markdown' and len(last_content) < 10:
            return False  # Already has empty closing cell

    # Add empty markdown cell
    nb['cells'].append({
        'cell_type': 'markdown',
        'metadata': {},
        'source': []
    })
    return True

def fix_spacing_after_headers(nb):
    """
    Ensure blank lines after section headers.

    Args:
        nb: Notebook dictionary

    Returns:
        Number of cells fixed
    """
    fixed_count = 0

    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown':
            source_lines = cell['source'] if isinstance(cell['source'], list) else [cell['source']]

            # Check each header
            modified = False
            new_source = []

            for i, line in enumerate(source_lines):
                new_source.append(line)

                # If this is a header and next line isn't blank, add blank line
                if line.startswith('#') and not line.strip().endswith('---'):
                    next_idx = i + 1
                    if next_idx < len(source_lines):
                        next_line = source_lines[next_idx]
                        if next_line.strip() != '':
                            new_source.append('\n')
                            modified = True

            if modified:
                cell['source'] = new_source
                fixed_count += 1

    return fixed_count

def find_sections_needing_key_concepts(nb, current_kc_count):
    """
    Identify sections that should have Key Concept boxes.

    Args:
        nb: Notebook dictionary
        current_kc_count: Current number of Key Concepts

    Returns:
        List of cell indices for sections needing Key Concepts
    """
    # If we already have 7+ Key Concepts, don't add more
    if current_kc_count >= 7:
        return []

    # Find all main section headers (## X.Y)
    main_sections = []

    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            content = ''.join(cell['source'])
            # Look for main section headers (## X.Y, not case study)
            import re
            match = re.search(r'^##\s+(\d+\.\d+)\s+', content, re.MULTILINE)
            if match:
                section_num = match.group(1)
                # Skip case study sections (usually X.8 or higher)
                minor = int(section_num.split('.')[1])
                if minor < 8:
                    main_sections.append({
                        'cell': i,
                        'section': section_num,
                        'content': content
                    })

    # Find sections without Key Concepts in next few cells
    sections_needing_kc = []

    for section in main_sections:
        has_kc = False
        # Check next 5 cells for Key Concept
        for j in range(section['cell'], min(section['cell'] + 6, len(nb['cells']))):
            cell_content = ''.join(nb['cells'][j]['source']) if nb['cells'][j]['cell_type'] == 'markdown' else ''
            if 'Key Concept' in cell_content:
                has_kc = True
                break

        if not has_kc:
            sections_needing_kc.append(section['cell'])

    # Return only as many as needed to reach 7 total
    needed = max(0, 7 - current_kc_count)
    return sections_needing_kc[:needed]

def apply_fixes(chapter_prefix, fix_list=None, dry_run=False):
    """
    Apply specified fixes to chapter notebook.

    Args:
        chapter_prefix: Chapter identifier (e.g., 'ch05')
        fix_list: List of fixes to apply (None = all safe fixes)
        dry_run: If True, don't save changes (just report what would be done)

    Returns:
        Dictionary with:
            - applied: List of fixes applied
            - backup: Path to backup file
            - modified: Whether notebook was modified
    """
    notebook_path = find_notebook(chapter_prefix)
    backup_path = None

    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    applied = []
    modified = False

    # Count current Key Concepts
    current_kc_count = 0
    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown':
            content = ''.join(cell['source'])
            if 'Key Concept' in content:
                current_kc_count += 1

    # Apply fixes (only safe ones)
    if fix_list is None or 'visual_summary' in fix_list:
        success, msg = fix_visual_summary(nb, chapter_prefix)
        if success:
            applied.append(f"Visual summary: {msg}")
            modified = True

    if fix_list is None or 'empty_closing' in fix_list:
        if fix_empty_closing_cell(nb):
            applied.append("Added empty closing cell")
            modified = True

    if fix_list is None or 'spacing' in fix_list:
        count = fix_spacing_after_headers(nb)
        if count > 0:
            applied.append(f"Fixed spacing after headers in {count} cells")
            modified = True

    if fix_list is None or 'key_concepts' in fix_list:
        sections_needing = find_sections_needing_key_concepts(nb, current_kc_count)
        for section_idx in sections_needing:
            add_key_concept_placeholder(nb, section_idx)
            applied.append(f"Added Key Concept placeholder after Cell {section_idx}")
            modified = True

    # Save changes if modifications were made
    if modified and not dry_run:
        # Create backup first
        backup_path = backup_notebook(notebook_path)

        # Save modified notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)

    return {
        'applied': applied,
        'backup': str(backup_path) if backup_path else None,
        'modified': modified
    }

def main():
    """Main execution for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python apply_fixes.py <chapter> [--dry-run]")
        print("\nExamples:")
        print("  python apply_fixes.py ch05")
        print("  python apply_fixes.py ch05 --dry-run")
        print("\nThis script applies safe fixes:")
        print("  - Add missing visual summary image")
        print("  - Add empty closing cell")
        print("  - Fix spacing after headers")
        print("  - Add Key Concept placeholders (if needed)")
        print("\nA backup is created automatically in notebooks_colab/backups/")
        sys.exit(1)

    chapter = sys.argv[1]

    # Normalize chapter format
    if not chapter.startswith('ch'):
        chapter = f'ch{int(chapter):02d}'

    dry_run = '--dry-run' in sys.argv

    try:
        result = apply_fixes(chapter, dry_run=dry_run)

        if dry_run:
            print(f"\n{'='*70}")
            print(f"DRY RUN MODE - No changes saved")
            print(f"{'='*70}\n")

        print(f"Chapter: {chapter}")
        print(f"Modified: {'Yes' if result['modified'] else 'No'}")

        if result['applied']:
            print(f"\nFixes applied ({len(result['applied'])}):")
            for fix in result['applied']:
                print(f"  ✅ {fix}")
        else:
            print("\n✅ No fixes needed - chapter is already compliant!")

        if result['backup'] and not dry_run:
            print(f"\nBackup created: {result['backup']}")

        if result['modified'] and not dry_run:
            print("\n" + "="*70)
            print("NEXT STEPS:")
            print("="*70)
            print("1. Review changes in Jupyter/VSCode")
            print("2. Fill in any TODO placeholders with actual content")
            print("3. Run verification: python verify_chapter.py " + chapter)
            print("4. If compliance ≥ 90, generate PDF")
            print("\nIf you need to revert:")
            print(f"  cp {result['backup']} {find_notebook(chapter)}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nAvailable chapters in notebooks_colab/:")
        pattern = 'notebooks_colab/ch*.ipynb'
        matches = glob.glob(pattern)
        if matches:
            for match in sorted(matches):
                print(f"  - {Path(match).stem[:4]}")
        else:
            print("  (none found)")
        sys.exit(1)
    except Exception as e:
        print(f"Error applying fixes: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
