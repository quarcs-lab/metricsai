#!/usr/bin/env python3
"""
Reorganize Chapter 4: Move Case Study to after Practice Exercises
Current: Sections 4.1-4.7 → Case Study → Key Takeaways → Practice Exercises
Target:  Sections 4.1-4.7 → Key Takeaways → Practice Exercises → Case Study
"""

import json

# Load notebook
notebook_path = 'notebooks_colab/ch04_Statistical_Inference_for_the_Mean.ipynb'
print(f"Loading notebook: {notebook_path}")

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

original_count = len(nb['cells'])
print(f"Original cell count: {original_count}")

# Current structure:
# Cells 0-49: Content (Title → Setup → Sections 4.1-4.7)
# Cells 50-62: Case Study (13 cells)
# Cell 63: Key Takeaways
# Cell 64: Practice Exercises

# Extract the cells we need to reorganize
content_cells = nb['cells'][:50]  # Cells 0-49
case_study_cells = nb['cells'][50:63]  # Cells 50-62 (13 cells)
key_takeaways_cell = nb['cells'][63]  # Cell 63
practice_exercises_cell = nb['cells'][64]  # Cell 64

# Verify extraction
print(f"\nExtracted:")
print(f"  Content cells: 0-49 ({len(content_cells)} cells)")
print(f"  Case study cells: 50-62 ({len(case_study_cells)} cells)")
print(f"  Key Takeaways: cell 63")
print(f"  Practice Exercises: cell 64")

# Build new structure
new_cells = []
new_cells.extend(content_cells)  # 0-49
new_cells.append(key_takeaways_cell)  # 50
new_cells.append(practice_exercises_cell)  # 51
new_cells.extend(case_study_cells)  # 52-64

# Update notebook
nb['cells'] = new_cells

new_count = len(nb['cells'])
print(f"\nNew structure:")
print(f"  Cells 0-49: Content (Title → Setup → Sections 4.1-4.7)")
print(f"  Cell 50: Key Takeaways")
print(f"  Cell 51: Practice Exercises")
print(f"  Cells 52-64: Case Study (13 cells)")
print(f"\nTotal cells: {new_count} (unchanged)")

# Save
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print(f"\n✅ Notebook reorganized successfully!")

# Verify the new structure
print(f"\nVerification:")
for i in range(48, min(66, len(nb['cells']))):
    cell = nb['cells'][i]
    if cell['cell_type'] == 'markdown':
        content = ''.join(cell['source'])
        header = content.split('\n')[0][:60]
        print(f"Cell {i}: {header}")
    else:
        print(f"Cell {i}: [code cell]")

if __name__ == '__main__':
    pass
