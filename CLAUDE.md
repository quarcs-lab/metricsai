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
