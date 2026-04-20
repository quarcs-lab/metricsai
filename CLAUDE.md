# CLAUDE.md — Project Instructions

## Project

- **Title:** metricsAI: An Introduction to Econometrics with Python and AI in the Cloud
- **Author:** Carlos Mendez
- **Tools:** Python, Quarto, Google Colab

## Critical Rules

### NEVER Delete Data

Under no circumstances delete any data files. Protected formats:

- **Statistical:** `.dta`, `.sav`, `.sas7bdat`
- **Spreadsheets:** `.xlsx`, `.xls`, `.csv`, `.tsv`
- **Spatial:** `.shp`, `.geojson`, `.kml`, `.gpkg`
- **Databases:** `.db`, `.sqlite`, `.sql`
- **Raw:** `.txt`, `.json`, `.xml`, `.parquet`

### NEVER Delete Programs

Under no circumstances delete any program files. Protected formats:

- **Scripts:** `.do`, `.R`, `.py`, `.jl`, `.m`
- **Notebooks:** `.ipynb`, `.Rmd`, `.qmd`, `.md`
- **Config:** `.yaml`, `.yml`, `.toml`, `.ini`, `.txt`
- **Docs:** `.md`, `.tex`

### Stay Within This Directory

All work must remain within the `metricsai` project folder. NEVER go up out of this directory.

### Maintain Progress Logs

The `./log/` directory preserves context across sessions. Chat sessions can die unexpectedly — logs bridge the gap.

- **When:** After significant work, before ending sessions, after major decisions
- **Format:** `YYYYMMDD_HHMM.md` with: current state, work done, decisions made, blockers, next steps
- **On startup:** Always check `./log/` for recent entries

## Project Structure

```text
metricsai/
├── notebooks_quarto/   # 18 chapters (.qmd) — SOURCE OF TRUTH
├── notebooks_colab/    # 18 chapters (.ipynb) — generated for Colab
├── notebooks_md/       # 18 chapters (.md) — markdown versions (auto-synced)
├── code/               # 17 Python code summaries (.py) + code/short/codeSummary.md
├── scripts/            # PDF generation, conversion, web-app builders, and utilities
├── web-apps/           # Interactive HTML dashboards (one folder per chapter)
├── book/               # Quarto HTML book (symlinks to notebooks_quarto/ and images/)
├── tutors/             # 9 AI tutor instruction files (customized Google Gemini Gems)
├── images/             # Cover images + chapter visual summaries
├── data/               # .DTA datasets from AED textbook (with comprehensive README)
├── log/                # Timestamped session logs
├── legacy/             # Archived files (R, Stata, Python originals)
├── .venv/              # Python virtual environment (gitignored)
├── .claude/rules/      # Detailed workflow docs (PDF, Quarto)
├── .claude/skills/     # 7 skills (see Architecture section)
├── index.html          # Project website (standalone)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Key Commands

**Activate the virtual environment:**

```bash
source .venv/bin/activate
```

**Set up a new virtual environment:**

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

**Render the HTML book:**

```bash
cd book && quarto render
```

**Render a single chapter in the book:**

```bash
cd book && quarto render notebooks_quarto/ch05_Bivariate_Data_Summary.qmd
```

**Export .qmd chapters to Colab notebooks (.ipynb):**

```bash
python3 scripts/export_qmd_to_ipynb.py --all
python3 scripts/export_qmd_to_ipynb.py ch05   # single chapter
```

**Generate a single chapter PDF:**

```bash
quarto render notebooks_quarto/ch05_*.qmd --to html --output-dir notebooks_colab
python3 scripts/inject_print_css.py notebooks_colab/ch05_*.html notebooks_colab/ch05_*_printable.html
python3 scripts/generate_pdf_playwright.py ch05
```

**Generate all chapter PDFs:**

```bash
python3 scripts/generate_pdf_playwright.py --all
```

**Scaffold a new chapter web app:**

```bash
python3 .claude/skills/web-app/scripts/scaffold_chapter.py ch05 "Bivariate Data Summary"
```

**Build a chapter web app:**

```bash
python3 web-apps/ch02/build.py
```

**Verify a chapter web app:**

```bash
python3 .claude/skills/web-app/scripts/verify_app.py web-apps/ch02/dashboard.html
```

## Conventions

- **Source files:** `chNN_Title_With_Underscores.qmd` in `notebooks_quarto/` (ch00–ch17) — edit these
- **Colab notebooks:** `.ipynb` files in `notebooks_colab/` are generated via `scripts/export_qmd_to_ipynb.py`
- **Images in notebooks:** Use absolute GitHub URLs (`https://raw.githubusercontent.com/quarcs-lab/metricsai/main/images/...`)
- **Markdown lists:** Always leave a blank line before any list (Pandoc requirement for Quarto)
- **Log entries:** `YYYYMMDD_HHMM.md` in `./log/`
- **Build artifacts:** HTML and PDF files in `notebooks_colab/` and `notebooks_quarto/` are gitignored

## Architecture

- **Source of truth:** `.qmd` files in `notebooks_quarto/` — all editing happens here
- **HTML book:** Quarto project in `book/` with symlinks (`book/notebooks_quarto` → `../notebooks_quarto`)
- **Colab export:** `scripts/export_qmd_to_ipynb.py` converts `.qmd` → `.ipynb` for Google Colab
- **Markdown export:** `notebooks_md/` contains `.md` versions of all chapters (auto-synced)
- **Auto-sync hook:** Editing any `.qmd` file automatically updates `.ipynb` (Colab), `.md` (Markdown), and `.html` (book) via `scripts/sync_chapter.sh`
- **PDF pipeline:** `quarto render` → `scripts/inject_print_css.py` → `scripts/generate_pdf_playwright.py`
- **Skills:** `chapter-standard` (template compliance), `compile-book` (PDF compilation), `proofread` (content review), `improve-readability` (notebook readability), `improve-webapp-readability` (web app pedagogy), `web-app` (interactive dashboards), `create-chapter-code-summary` (Python code cheat sheets)
- **Web apps:** Single-file Plotly.js dashboards in `web-apps/chNN/dashboard.html`, built by `web-apps/chNN/build.py` from `web-apps/chNN/template.html`
- **Detailed workflow docs:** `.claude/rules/pdf-generation.md` and `.claude/rules/quarto-book.md`
