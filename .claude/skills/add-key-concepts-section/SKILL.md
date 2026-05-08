---
name: add-key-concepts-section
description: Inserts a pedagogical "Key Concepts" glossary section into a metricsAI chapter notebook (.qmd), between Chapter Overview and Setup. Each entry has a bold term, a 1–2 sentence definition, and two side-by-side collapsible Quarto callouts — a dataset-grounded *Example* and a vivid *Analogy* — so readers can skim definitions and expand only the panels they need. The new section is ADDITIVE: it complements (does not replace) the chapter's existing inline `> **Key Concept N.M**` blockquotes by picking 5–8 concepts disjoint from them, sized to chapter complexity, and tied to the chapter's `**What you'll learn:**` bullets. Refuses to run if the section already exists. Fully autonomous one-shot — drafts content, inserts, syncs all formats (.ipynb / .md / .html), verifies the HTML render, and reports. Does not commit. Goal is to foster learning through dataset-grounded examples and vivid analogies. Invoke via /add-key-concepts-section chNN.
argument-hint: [chapter-number]
context: fork
agent: Explore
---

# Add Key Concepts Section Skill

Generates and inserts a pedagogical Key Concepts glossary section into a metricsAI chapter (.qmd). Modeled on the chapter format at `https://cmg777.github.io/intro2causal/book/_book/notebooks_quarto/02-regression.html` and the chapter 1 pilot in this project.

## Overview

Each entry in the section has three parts:

1. A **bold term** with a 1–2 sentence **definition** (no jargon undefined in earlier chapters).
2. A collapsible **Example** callout that uses the chapter's actual dataset and at least one real variable name, with a real number the chapter computes.
3. A collapsible **Analogy** callout that uses a vivid, non-academic comparison from a domain not used by sibling concepts.

Examples and analogies sit side-by-side in a two-column Quarto layout. The collapse-by-default behavior keeps the section compact so readers can skim 5–8 concepts in ~60 seconds.

**Use this skill when:**

- A chapter does not yet have an up-front Key Concepts glossary.
- You want to scaffold the chapter's Learning Objectives with definitions, examples, and analogies before readers hit the content.
- The chapter has been standardized (chapter-standard score ≥ 85) — the section relies on `**What you'll learn:**` and `## Setup` headings being in their canonical locations.

**The skill is fully autonomous one-shot:** it picks concepts, drafts content, inserts, syncs, verifies, and reports — all in a single invocation. There are no interactive checkpoints. If you want to review the concept list before content is drafted, edit the .qmd directly and remove the `## Key Concepts` heading; the skill will refuse to overwrite an existing section and you can iterate by deleting + re-running.

## Quick Start

```
/add-key-concepts-section ch05
```

Output:

```
✅ Added Key Concepts section to ch05 (6 concepts)

Concepts chosen (each tied to a `**What you'll learn:**` bullet):
  1. Correlation Coefficient → "How to compute and interpret correlation"
  2. Covariance              → "How to compute and interpret correlation"
  3. Joint Distribution      → "How to visualize joint distributions"
  ...

Disjoint from inline blockquotes ✓ (chapter has 4 inline Key Concepts; none duplicated)

Verification:
  .qmd:  1× '## Key Concepts' heading, 6 concept blocks   ✓
  HTML:  id="key-concepts" present, 6 .columns blocks     ✓
  ipynb: 0 hits for Quarto-only markup  ✓ (stripped)
  md:    section present=yes, callouts preserved=yes      ✓

Files modified:
  notebooks_quarto/ch05_Bivariate_Data_Summary.qmd
  notebooks_colab/ch05_Bivariate_Data_Summary.ipynb       (auto-sync)
  notebooks_md/ch05_Bivariate_Data_Summary.md             (auto-sync)
  book/_book/notebooks_quarto/ch05_Bivariate_Data_Summary.html (auto-sync)

Next step (run when ready):
  git add notebooks_quarto/ch05_*.qmd notebooks_colab/ch05_*.ipynb notebooks_md/ch05_*.md book/_book
  git commit -m "Add Key Concepts section to ch05"
```

## Workflow

When invoked, follow these steps **in order**. If any step fails, abort with a clear message and leave the chapter unchanged.

### Step 0 — Validate input

- The argument must match `^ch(0[0-9]|1[0-7])$`. Reject otherwise.
- Resolve the .qmd path: `notebooks_quarto/{chapter_id}_*.qmd`. Fail if zero or multiple matches.

### Step 1 — Detect re-run (idempotency)

Run `inspect_chapter.py`:

```bash
python3 .claude/skills/add-key-concepts-section/scripts/inspect_chapter.py chNN --pretty
```

If the returned `has_key_concepts_section` is `true`, abort with:

> `## Key Concepts` already exists at line N. To regenerate, delete the section first.

Do not modify any file. Exit normally.

### Step 2 — Read the pedagogical rubric

Before drafting any content, **read** `.claude/skills/add-key-concepts-section/references/pedagogical_rubric.md` end-to-end. The three hard rules and the seven self-check questions in that file govern every decision in Steps 3 and 4. Do not skip.

### Step 3 — Pick 5–8 concepts (the selection algorithm)

Using the JSON from Step 1:

1. **Build a candidate pool** of foundational concepts the chapter introduces, derived from:
   - Each bullet in `learning_objectives` (each bullet typically maps to 1 concept).
   - Bold-faced or italicized technical terms in the chapter's content sections (`**OLS**`, `*p-value*`).
   - Section headings (`## 5.3 Confidence Intervals` ⇒ candidate "Confidence Interval"). Read enough of the chapter body via the .qmd to recognize the central terms.
2. **Subtract** any concept already covered by an `inline_key_concepts` entry — match by normalized term (case-insensitive, ignoring "vs.", "and", articles). The new section is ADDITIVE, not duplicative.
3. **Rank** remaining candidates, preferring concepts that:
   - Map cleanly to a `learning_objectives` bullet (Pedagogy Rule 3 — concepts that don't map to a bullet are dropped, even if foundational).
   - A first-year student is most likely to confuse or get wrong.
   - The chapter actually computes or visualizes (so a dataset-grounded Example is possible).
4. **Pick the top 5–8** based on chapter scope:
   - **5–6** for short / introductory chapters (e.g., ch02 univariate stats, ch03 sample mean).
   - **6–7** for mid-complexity chapters (e.g., ch05 bivariate, ch06 OLS).
   - **7–8** for content-heavy chapters (e.g., ch11 multiple-regression inference, ch16 instrumental variables).
5. **Record the mapping** (concept → LO bullet) for the final report.

If after subtracting inline coverage you have fewer than 5 candidates that map to LO bullets, lower the count to as low as 4 — but explain in the report why fewer concepts fit (typically: short chapter where most concepts are already inline).

### Step 4 — Draft each concept

For every chosen concept, draft three pieces of content per `pedagogical_rubric.md`:

- **Definition** — 1–2 sentences. No jargon outside `prior_chapters_defined_terms` and not-yet-defined chapter-internal terms. Never reuse the term itself.
- **Example** — 2–4 sentences. MUST reference at least one variable from `dataset_variable_names`. MUST include a real number the chapter computes (read the chapter body to find it). Lead with the dataset's identity ("For the 29 Davis houses…").
- **Analogy** — 2–4 sentences. Vivid, concrete, from a different domain than every sibling concept's analogy in this chapter. Maintain a running list of "domains used so far in this section" and reject same-domain duplicates. End with a one-line bridge back to the concept.

Apply the **seven-question quality self-check** from the rubric to each concept before finalizing. Redraft any piece that fails.

### Step 5 — Read the section template

Read `.claude/skills/add-key-concepts-section/references/section_template.md` for the exact Quarto fence syntax (5/4/3 colons) and the section wrapper format. The template is the single source of truth for formatting — do not improvise.

### Step 6 — Assemble the markdown

Build the section as: `## Key Concepts` heading + intro paragraph + N concept blocks separated by blank lines. Use the spelled-out count word (`Five`, `Six`, `Seven`, `Eight`) in the intro.

**Do NOT include** a "Tip" line about Colab degradation. The export script `scripts/export_qmd_to_ipynb.py` calls `strip_key_concepts()` (defined at lines 60–69) and removes the entire section from every .ipynb automatically — no Colab reader ever sees it, so a Colab-targeted tip is misleading.

### Step 7 — Insert into the .qmd

Use a single `Edit` tool call. Build the unique anchor from the chapter's actual outline:

- **Old string:** `"- {last_outline_bullet}\n\n## Setup"` (the `last_outline_bullet` value from the inspect JSON guarantees uniqueness across chapters).
- **New string:** `"- {last_outline_bullet}\n\n{assembled_section}\n\n## Setup"`.

If `last_outline_bullet` is empty (chapter outline missing), fall back to inserting before the line number `insertion_point_line - 1`, but warn loudly in the report — this means the chapter's structure is non-standard.

### Step 8 — Sync all formats

```bash
bash scripts/sync_chapter.sh notebooks_quarto/{basename}.qmd
```

This regenerates `.ipynb` (Colab), `.md`, and the rendered HTML in `book/_book/`. The `.ipynb` regeneration automatically strips the new section via `strip_key_concepts()` — that is the intended design.

### Step 9 — Verify

```bash
python3 .claude/skills/add-key-concepts-section/scripts/verify_section.py chNN
```

The verify script returns exit code 0 on success and 1 on any failure. It checks:

- `.qmd` has exactly 1 `^## Key Concepts$` heading and 5–8 concept blocks.
- HTML render contains `id="key-concepts"` and ≥ N `class="columns"` blocks.
- `.ipynb` has 0 hits for Quarto-only markup (`## Key Concepts`, `callout-tip`, `callout-note`, `::::: {.columns}`, `:::: {.column`).
- `.md` mirror contains the section verbatim with callouts.

If verification fails, **do not roll back** — surface the specific failures in the report and let the user decide. Common failure modes: HTML wasn't re-rendered (sync script error), callout fence depth wrong (template drift).

### Step 10 — Report

Print the final report (format shown in the Quick Start above). Include:

- Concepts chosen, each with its LO bullet mapping.
- A "Disjoint from inline blockquotes" line confirming Pedagogy Rule subtraction was applied.
- The four verification check results.
- Files modified.
- A copy-pasteable `git add … && git commit -m …` command for the user (do not run it).

End. Do not commit. Do not modify anything else.

## Pedagogical contract

This skill exists to **foster learning**, not just to format a glossary. The three hard rules in `references/pedagogical_rubric.md` are non-negotiable:

1. **Examples are dataset-grounded** — every Example references the chapter's actual dataset and a real variable name; uses a real number the chapter computes; never falls back to "imagine a dataset".
2. **Definitions are short and assume only earlier vocabulary** — 1–2 sentences; no jargon undefined in chapters 0..N−1; no formula; never reuses the defined term.
3. **Each concept ties to a Learning Objective** — every chosen concept maps to a specific bullet in the chapter's `**What you'll learn:**` list. Concepts that don't map are dropped.

Plus the **analogy diversity rule**: no two analogies in the same chapter share a domain (cooking, sports, transportation, weather, money, music, geography, construction, common objects).

## Outputs

The skill modifies (via auto-sync from a single .qmd edit):

- `notebooks_quarto/{basename}.qmd` — direct edit (the new section).
- `notebooks_colab/{basename}.ipynb` — regenerated by `sync_chapter.sh` step 1; Quarto-only markup is stripped automatically by `strip_key_concepts()`.
- `notebooks_md/{basename}.md` — regenerated by `sync_chapter.sh` step 2; section preserved verbatim.
- `book/_book/notebooks_quarto/{basename}.html` — regenerated by `sync_chapter.sh` step 3; callouts and columns render natively.

The skill does **NOT** modify:

- `book/custom.css` (already styled chapter-agnostically by the ch01 pilot).
- `scripts/export_qmd_to_ipynb.py` (already strips the section chapter-agnostically).
- Any chapter other than the one specified.
- The 10 existing inline `> **Key Concept N.M**` blockquotes (additive design).
- Git index or working tree commit state (the skill never commits).

## Troubleshooting

### "Key Concepts already exists"

The skill refuses to run if `^## Key Concepts$` is found in the .qmd. To regenerate:

1. Open the .qmd, delete the entire section (from `## Key Concepts` to the line just before `## Setup`).
2. Re-run the skill.

This is by design — it prevents accidental overwrite of hand-edited concepts.

### Verification fails on HTML

Most likely the Quarto render did not re-run. Manually:

```bash
cd book && quarto render notebooks_quarto/{basename}.qmd
```

Then re-run the verify script:

```bash
python3 .claude/skills/add-key-concepts-section/scripts/verify_section.py chNN
```

If `id="key-concepts"` is still missing, check for "fence not closed" warnings in the Quarto output. The fix is to bump outer fences from `:::::` to `::::::` in `references/section_template.md`.

### Verification fails on .ipynb (forbidden markup found)

The strip in `scripts/export_qmd_to_ipynb.py:strip_key_concepts` (lines 60–69) didn't run. Either:

- The export script is older than the chapter 1 pilot (added 2026-05-08) — check git log.
- The `## Setup` heading is missing or renamed in the .qmd — `strip_key_concepts` uses it as the section terminator. Restore the canonical `## Setup` heading.

### Chapter has no `**What you'll learn:**` bullets

Pedagogy Rule 3 cannot be satisfied. Two options:

1. Add the `**What you'll learn:**` block to the chapter (run `/chapter-standard chNN --apply` to scaffold it).
2. Run the skill anyway — it will pick concepts based on section headings only and note in the report that LO mapping was skipped. Quality will be lower; consider hand-curating the section afterward.

### Chapter is non-standard (ch00 Preface, ch08 / ch13 case-study chapters)

The skill runs but the result may be awkward — Preface chapters have no Setup section to anchor the insert, and integrated case-study chapters (ch08, ch13) treat each section as a self-contained study. Inspect the output and either keep, edit, or delete manually.

## Integration with existing workflow

```bash
# 1. Standardize (ensure **What you'll learn:** and ## Setup are present)
/chapter-standard ch05 --apply

# 2. Add the Key Concepts section
/add-key-concepts-section ch05

# 3. Spot-check rendering in the browser
open book/_book/notebooks_quarto/ch05_*.html

# 4. (Optional) proofread prose quality
/proofread ch05 --fix

# 5. Commit when satisfied
git add notebooks_quarto/ch05_*.qmd notebooks_colab/ch05_*.ipynb notebooks_md/ch05_*.md book/_book
git commit -m "Add Key Concepts section to ch05"
```

## Files

- **Skill instructions**: `.claude/skills/add-key-concepts-section/SKILL.md` (this file)
- **Pedagogical rubric**: `.claude/skills/add-key-concepts-section/references/pedagogical_rubric.md`
- **Markdown template**: `.claude/skills/add-key-concepts-section/references/section_template.md`
- **Inspect script**: `.claude/skills/add-key-concepts-section/scripts/inspect_chapter.py`
- **Verify script**: `.claude/skills/add-key-concepts-section/scripts/verify_section.py`
- **Sync script** (project-wide): `scripts/sync_chapter.sh`
- **Strip script** (project-wide, applies to all chapters): `scripts/export_qmd_to_ipynb.py:strip_key_concepts`
- **Section CSS** (project-wide, applies to all chapters): `book/custom.css` (search for `KEY CONCEPTS GLOSSARY`)

## Version

- **Version**: 1.0
- **Created**: 2026-05-08
- **Pilot chapter**: ch01 (live in the rendered book)
- **Prerequisite**: chapter-standard score ≥ 85; `**What you'll learn:**` block present.
