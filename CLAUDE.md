# CLAUDE.md – AI Assistant Instructions

**READ THIS FILE FIRST** upon entering this project.

This file contains critical rules and context for working on this project. These rules are non-negotiable.

---

## Critical Rules

### 1. NEVER DELETE DATA
Under no circumstances are you ever to DELETE any data files. Protected formats include:
- **Statistical data:** `.dta`, `.sav`, `.sas7bdat`
- **Spreadsheets:** `.xlsx`, `.xls`, `.csv`, `.tsv`
- **Spatial data:** `.shp`, `.geojson`, `.kml`, `.gpkg`
- **Databases:** `.db`, `.sqlite`, `.sql`
- **Raw data:** `.txt`, `.json`, `.xml`, `.parquet`
- **Add other formats as needed for your project**

### 2. NEVER DELETE PROGRAMS
Under no circumstances are you ever to DELETE any program files. Protected formats include:
- **Scripts:** `.do`, `.R`, `.py`, `.jl`, `.m`
- **Notebooks:** `.ipynb`, `.Rmd`, `.qmd`, `.md`
- **Configuration:** `.yaml`, `.yml`, `.toml`, `.ini`, `.txt`
- **Documentation:** `.md`, `.tex`
- **Add other formats as needed for your project**

### 3. STAY WITHIN THIS DIRECTORY
Under no circumstances are you ever to GO UP OUT OF THIS ONE FOLDER called `aed_2026-01-20_08-57-26`. All work must remain within this project directory.

### 4. MAINTAIN PROGRESS LOGS
The `./log/` directory contains progress logs that preserve conversation context across sessions.

**Why:** Chat sessions can die unexpectedly. When a new Claude starts, it has no memory of previous work. Logs bridge this gap.

**When to log:**
- After completing significant work
- Before ending a session
- After major decisions
- When context is building up

**What to include:**
- Current state of the project
- Summary of work done (include key results, tables, or figures)
- Key decisions made
- Any issues or blockers
- Next steps planned

**How:** Create timestamped entries (`YYYYMMDD_HHMM.md`) documenting what was done, current state, and next steps.

**On startup:** Always check `./log/` for recent entries to understand what was happening before.

---

## Project Context

- **Project Title:** metricsAI: An Introduction to Econometrics with Python and AI in the Cloud
- **Primary Tools:** Python, Jupyter/Colab notebooks
- **Authors:** Carlos Mendez

---

## Note Improvement Template

The `./notes/` directory contains study notes for 17 chapters. A standard template has been established to maximize learning effectiveness.

**Reference implementation:** `notes/s01 Analysis of Economics Data.md`

**Template components:**
1. **Learning Objectives** (opening) - Sets clear learning expectations
2. **Content sections with Key Concept boxes** - Immediate reinforcement after each section
3. **Consolidated Key Takeaways** (closing) - Comprehensive chapter review

**See `notes/README.md` for complete template documentation.**

**When improving notes:**
- Follow the exact structure from Chapter 1
- Maintain consistency across all chapters
- No deletions (additive only)
- Document changes in log files

**Quality standard:** Each chapter should be ~9 KB, with 3 visual separators, Learning Objectives, Key Concepts after every section, and consolidated Key Takeaways at the end.

---

## Exporting Notebooks to PDF

### Overview

The project includes a complete workflow for exporting Jupyter notebooks to high-quality PDF files. This is useful for:
- Distributing to students without Python/Colab access
- Printing for offline study
- Creating archival versions with all outputs
- Generating professional reports

### Export Method: HTML → Browser Print → PDF

**Why this approach?**
- Direct `jupyter nbconvert --to pdf` fails on notebooks with SVG images (Colab badges)
- LaTeX-based PDF export has complex dependencies and can fail
- HTML → Print gives reliable, high-quality results
- Full control over formatting via CSS

### Quick Reference

**Single notebook:**
```bash
jupyter nbconvert --to html notebooks_colab/NOTEBOOK.ipynb --output-dir notebooks_pdf_ready
python3 inject_print_css.py notebooks_pdf_ready/NOTEBOOK.html notebooks_pdf_ready/NOTEBOOK_printable.html
open notebooks_pdf_ready/NOTEBOOK_printable.html
# Then: Cmd+P → Save as PDF
```

**All notebooks:**
```bash
./export_notebooks_to_pdf.sh
```

### Key Files

1. **`notebook_pdf_styles.css`** - Enhanced print optimization CSS with brand identity
   - **Brand color hierarchy:** ElectricCyan (h1), SynapsePurple (h2), DataPink (h3), DeepNavy (h4)
   - **Modern typography:** Inter (body text), JetBrains Mono (code)
   - **Perfect spacing:** 20px padding for input cells, 22px for output cells
   - **Enhanced visuals:** Visual summary images with borders/shadows, styled tables with alternating rows
   - **Print optimized:** Portrait orientation (8.5" × 11"), 0.4-0.5" margins, font sizes 9-11pt
   - **Professional design:** Color-coded headings, bordered code blocks, enhanced table headers

2. **`inject_print_css.py`** - CSS injection script
   - Reads HTML export
   - Injects custom styles
   - Creates print-ready file

3. **`export_notebooks_to_pdf.sh`** - Batch processor
   - Converts all notebooks to HTML
   - Applies CSS to each
   - Organizes in `notebooks_pdf_ready/` folder

### CSS Customization

**Brand color hierarchy (heading styles):**
```css
/* H1: Chapter Title - ElectricCyan (#008CB7) with bottom border */
h1 {
    color: #008CB7;
    border-bottom: 3px solid #008CB7;
}

/* H2: Section - SynapsePurple (#7A209F) with left border */
h2 {
    color: #7A209F;
    border-left: 4px solid #7A209F;
    padding-left: 12pt;
}

/* H3: Subsection - DataPink (#C21E72) */
h3 {
    color: #C21E72;
}
```

**Perfect spacing for code cells:**
```css
/* Input cells: 20px left padding */
.input_area {
    background-color: #f7fafc !important;
    border-left: 3px solid #008CB7 !important;
    padding: 10px 18px 10px 20px !important; /* top right bottom left */
}

/* Output cells: 22px left padding */
.output pre,
.output_area pre,
.output_subarea pre {
    padding: 10px 18px 10px 22px !important;
}
```

**Enhanced table styling:**
```css
/* Table headers with brand colors */
table thead {
    background-color: #f7fafc;
    border-bottom: 2px solid #008CB7;
}

/* Alternating row colors for readability */
table tbody tr:nth-child(even) {
    background-color: #f7fafc;
}

/* Regression tables: compact 8pt font */
.dataframe, .simpletable {
    font-size: 8pt !important;
}
```

**Page orientation:**
```css
/* Current: Portrait with narrow margins */
@page {
    size: letter portrait;
    margin: 0.5in 0.4in;
}

/* Alternative: Landscape (for very wide tables) */
@page {
    size: letter landscape;
    margin: 0.5in;
}
```

### Formatting Guidelines

**DO:**
- Use brand color hierarchy for headings (ElectricCyan, SynapsePurple, DataPink, DeepNavy)
- Maintain perfect spacing: 20px left padding for input cells, 22px for output cells
- Keep tables at 9-10pt for readability (8pt for regression output)
- Use portrait orientation (standard documents)
- Enable text wrapping for wide content
- Test print preview before batch export
- Include visual summary images with borders and shadows
- Use modern typography (Inter for body, JetBrains Mono for code)

**DON'T:**
- Make fonts too small (< 8pt unreadable)
- Use very wide margins (wastes space)
- Delete the CSS/script files (needed for future exports)
- Modify source notebooks for PDF (export as-is)
- Use dark backgrounds (wastes ink)
- Remove brand color styling (maintains visual identity)

### Troubleshooting

**Tables too wide:**
- Reduce font size in CSS (try 8-9px)
- Switch to landscape orientation
- Adjust margins to 0.2in

**Tables too small:**
- Increase font size in CSS (try 11-12px)
- Verify in print preview before saving

**Missing dependencies:**
```bash
# Install Jupyter nbconvert
pip install nbconvert

# Install Pandoc (required for HTML conversion)
brew install pandoc
```

### Workflow Integration

This export method is now the standard for:
- Creating distribution copies of notebooks
- Generating course materials
- Archiving executed notebooks
- Producing professional reports

The files (`notebook_pdf_styles.css`, `inject_print_css.py`, `export_notebooks_to_pdf.sh`) are maintained in the repository root for easy access.
