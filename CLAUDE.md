# CLAUDE.md — Project Instructions

## Project

- **Title:** metricsAI: An Introduction to Econometrics with Python and AI in the Cloud
- **Author:** Carlos Mendez
- **Tools:** Python, Jupyter/Colab notebooks, Quarto

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
├── notebooks_colab/    # 18 chapters (.ipynb + .md via Jupytext)
├── scripts/            # PDF generation pipeline + utilities
├── book/               # Quarto HTML book (symlinks to notebooks_colab/ and images/)
├── images/             # Cover images + chapter visual summaries
├── data/               # .DTA datasets from AED textbook
├── log/                # Timestamped session logs
├── legacy/             # Archived files (R, Stata, Python originals)
├── .venv/              # Python virtual environment (gitignored)
├── .claude/rules/      # Detailed workflow docs (PDF, Quarto)
├── .claude/skills/     # chapter-standard, compile-book, proofread
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

**Generate a single chapter PDF:**

```bash
cd notebooks_colab && jupyter nbconvert --to html ch05_*.ipynb && cd ..
python3 scripts/inject_print_css.py notebooks_colab/ch05_*.html notebooks_colab/ch05_*_printable.html
python3 scripts/generate_pdf_playwright.py ch05
```

**Generate all chapter PDFs:**

```bash
cd notebooks_colab && for nb in ch*.ipynb; do jupyter nbconvert --to html "$nb"; done && cd ..
python3 scripts/generate_pdf_playwright.py --all
```

**Render the HTML book:**

```bash
cd book && quarto render
```

**Render a single chapter in the book:**

```bash
cd book && quarto render notebooks_colab/ch05_Bivariate_Data_Summary.ipynb
```

**Sync Jupytext formats after editing a notebook:**

```bash
jupytext --sync notebooks_colab/ch05_*.ipynb
```

## Conventions

- **Notebook naming:** `chNN_Title_With_Underscores.ipynb` (ch00–ch17)
- **Images in notebooks:** Use absolute GitHub URLs (`https://raw.githubusercontent.com/quarcs-lab/metricsai/main/images/...`)
- **Markdown lists:** Always leave a blank line before any list (Pandoc requirement for Quarto)
- **Log entries:** `YYYYMMDD_HHMM.md` in `./log/`
- **Jupytext sync:** Each notebook has paired `.ipynb` and `.md` (MyST) files — edit either, Jupytext syncs automatically
- **Build artifacts:** HTML and PDF files in `notebooks_colab/` are gitignored

## Architecture

- **PDF pipeline:** `jupyter nbconvert` → `scripts/inject_print_css.py` → `scripts/generate_pdf_playwright.py` (all 3 steps required in order)
- **HTML book:** Quarto project in `book/` with symlinks (`book/notebooks_colab` → `../notebooks_colab`)
- **Skills:** `chapter-standard` (template compliance), `compile-book` (PDF compilation), `proofread` (content review)
- **Detailed workflow docs:** `.claude/rules/pdf-generation.md` and `.claude/rules/quarto-book.md`
