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
├── scripts/            # PDF generation, conversion, web-app builders, i18n tooling, and utilities
├── web-apps/           # Interactive HTML dashboards (one folder per chapter)
│   └── _shared/        # Shared i18n runtime, 23 string tables (EN/ES/JA), canonical glossary
├── slides/             # Quarto reveal.js chapter decks (one folder per chapter: slides/chNN/)
├── quizzes/            # Chapter quizzes: banks/chNN.json (source) → chNN.html; checks/ fact-checks; _template.html engine
├── book/               # Quarto HTML book (symlinks to notebooks_quarto/ and images/)
├── tutors/             # 9 AI tutor instruction files (customized Google Gemini Gems)
├── images/             # Cover images + chapter visual summaries
├── data/               # .DTA datasets from AED textbook (with comprehensive README)
├── log/                # Timestamped session logs
├── legacy/             # Archived files (R, Stata, Python originals)
├── .venv/              # Python virtual environment (gitignored)
├── .claude/rules/      # Detailed workflow docs (PDF, Quarto)
├── .claude/skills/     # 10 skills (see Architecture section)
├── index.html          # Project website (standalone)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```


## Self-learning 
When I correct you, or you catch yourself making a mistake: before continuing， add the lesson as a one-line rule under ### Lessons, so it never happens again.

### Lessons 
- Connect localized image assets to the homepage language renderer and verify switching and persisted reloads before calling localization complete.
- Size short illustration badge labels to use the available space; equal card dimensions do not require equal font sizes.
- Balance three-badge illustrations with mirrored side badges, a centered lower badge, and consistent connector lengths.
- Place illustration badges next to their corresponding objects and use short, quiet pointers.
- Verify that illustration connectors terminate on the intended object, especially when the foreground brain overlaps the background clouds.
- Preserve the book cover's visual hierarchy in related artwork: a dominant foreground brain with a connected cloud backdrop behind it.
-（Claude adds lessons/rules here）
- Check generated illustrations for unrequested mathematical claims, and label finite log-model percentage changes as approximations.
- Check the staged diff, including newly added files, before reporting that whitespace validation passed.
- Round reported statistics from exact values, never from already-rounded printed output (double rounding turned t = 5.9953 into "5.99" instead of 6.00).
- Verify quiz claims about a dataset (e.g., which variables move together) against the data, not the chapter prose ("bigger houses tend to be newer" is false in AED_HOUSE: r = 0.08).
- In key-hidden exam feedback, point to the concept or section to revisit; never state the correction, quote the key, or negate a sibling option.
- Never cycle quiz answer keys through A–D in fixed blocks; balance letters but let about 1 in 4 consecutive keys repeat.
- Check a dataset's actual coverage (first/last date, observations per period) before describing its range (AED_REALGDPPC ends in 2020 Q1, not "end of 2020").
- In quiz items, a number students must compute must not appear in any other exam stem or option, and fully crossed items get identical neutral wrong-option feedback.
- When correcting a chapter claim, grep and fix the same claim in its slides (EN/ES/JA), web-app template + string tables, code summary, and quiz bank, then rebuild each.

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

**Generate a chapter slide deck (Quarto reveal.js):**

```bash
/write-slides ch05            # autonomous: reads the chapter, exports figures, builds + renders slides/ch05/
```

**Generate a chapter quiz (Practice + Exam, certificate at 80%):**

```bash
/write-quiz ch05             # autonomous: sizes, writes, fact-checks, double-reviews, builds + tests quizzes/ch05.html
```

**Validate + rebuild a chapter quiz after editing its bank:**

```bash
python3 scripts/build_quiz.py ch05            # validate quizzes/banks/ch05.json, print cue warnings, write quizzes/ch05.html
python3 quizzes/checks/ch05_factcheck.py     # re-verify every number in the bank against the data
```

**Export a chapter's figures for a slide deck (used by /write-slides):**

```bash
python3 .claude/skills/write-slides/scripts/export_chapter_figures.py ch05
python3 .claude/skills/write-slides/scripts/export_chapter_figures.py ch05 --source render  # refresh plots
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

**Validate i18n strings parity (gate before any commit touching `web-apps/_shared/strings/`):**

```bash
python3 scripts/i18n_check.py
```

**Run the headless browser i18n smoke test (gate before any commit touching the i18n runtime, boot order, or `__rerender_*` registrations):**

```bash
python3 scripts/smoke_i18n.py
```

**Add a new language to the project website (PT, ZH, DE, …):** see `log/20260515_1502.md` for the worked JA example. The 6-phase recipe is: (1) write a new section in `web-apps/_shared/glossary/style-notes.md`; (2) dispatch 1 subagent to fill the new column in `web-apps/_shared/glossary/canonical-terms.md`; (3) pilot 1 chapter; (4) review + promote new vocab; (5) fan out 22 parallel translator subagents; (6) append the 2-letter code to `web-apps/_shared/i18n-config.js` and extend `LANG_CYCLE` in `scripts/smoke_i18n.py`. **No HTML files touched.**

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
- **Skills:** `chapter-standard` (template compliance), `compile-book` (PDF compilation), `proofread` (content review), `improve-readability` (notebook readability), `improve-webapp-readability` (web app pedagogy), `web-app` (interactive dashboards), `create-chapter-code-summary` (Python code cheat sheets), `add-key-concepts-section` (pedagogical glossary section), `write-slides` (Quarto reveal.js chapter decks → `slides/chNN/`), `write-quiz` (Practice + Exam chapter quizzes → `quizzes/chNN.html`)
- **Web apps:** Single-file Plotly.js dashboards in `web-apps/chNN/dashboard.html`, built by `web-apps/chNN/build.py` from `web-apps/chNN/template.html`
- **Quizzes:** Single-file quiz pages `quizzes/chNN.html`, built by `scripts/build_quiz.py` from `quizzes/_template.html` + `quizzes/banks/chNN.json` (edit the bank, never the built page). Fact-checks in `quizzes/checks/`. English source; a header globe button machine-translates the page to ES/JA via Google Translate (follows the site's saved language; certificate/report, math, and names stay English). Linked from `index.html`, the README table, and each chapter's resource bar (`https://quarcs-lab.github.io/metricsai/quizzes/chNN.html`; template in `scripts/add_resource_buttons.py`).
- **Shared i18n runtime:** All 19 web pages (`index.html`, `tutors.html`, `web-apps/ch01`–`ch17/dashboard.html`) load the runtime + per-page string tables from `web-apps/_shared/`. Languages: EN + ES + JA. Adding a 4th language is a pure data task across `_shared/strings/*.js` — zero HTML touched. Validators: `scripts/i18n_check.py` (parity gate) + `scripts/smoke_i18n.py` (Playwright regression).
- **Detailed workflow docs:** `.claude/rules/pdf-generation.md` and `.claude/rules/quarto-book.md`
