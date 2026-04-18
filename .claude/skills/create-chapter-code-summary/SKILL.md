---
name: create-chapter-code-summary
description: Creates a self-contained Python code summary ("cheat sheet") for a metricsAI chapter's Key Takeaways section. Reads the chapter .qmd and its web app to identify key libraries, functions, datasets, and concepts, then generates a single markdown code block that reproduces the chapter's core workflow. The code block is pedagogical (commented), self-contained (runs in an empty Colab notebook), and aligned with the web app's key concepts. Invoke via /create-chapter-code-summary chNN.
argument-hint: [chapter-number]
context: fork
agent: Explore
---

# Create Chapter Code Summary Skill

Generates a **Python Libraries and Code** subsection for a chapter's Key Takeaways section. The output is a single, self-contained markdown code block that students can copy into an empty Google Colab notebook and run end-to-end. It serves as a pedagogical cheat sheet of the chapter's most important libraries, functions, and analytical workflow.

## Why this skill exists

Students finishing a chapter need a quick-reference code summary that ties together everything they learned. Reading back through 40-70 cells to find the key commands is tedious. A well-designed cheat sheet:

- Reinforces the chapter's core workflow in a single scannable block
- Aligns with the web app's interactive key concepts, creating a bridge between reading and doing
- Gives students a runnable starting point they can modify for their own data
- Serves as a study aid before exams or when returning to material later

The pattern was proven on Chapter 1 and is now codified here for all chapters.

## When to use

Invoke with `/create-chapter-code-summary chNN` (e.g., `/create-chapter-code-summary ch05`) when:

- A chapter's content is finalized and all code cells are stable
- The chapter's web app exists (needed to identify key concepts)
- You want to add the code summary before generating PDFs or publishing the book

Do **not** invoke this skill if the chapter is still being actively edited or if major code changes are pending.

## Non-negotiables

**What this skill WILL do:**

- Read the chapter `.qmd` to extract all imports, datasets, key functions, and the analytical workflow
- Read the chapter's web app to identify key concepts that guide which code steps are most important
- Generate a single markdown code block (` ```python `) with pedagogical comments
- Insert it into the Key Takeaways section before the "Next Steps" divider
- Add a "Try it yourself!" line with a link to an empty Google Colab notebook
- Render the chapter with Quarto to verify no errors

**What this skill WILL NOT do:**

- Create executable code cells (`{python}`) — the block is markdown-only, for students to copy
- Use collapsible toggles (`code-fold`) — the code is always visible
- Include dark theme styling (`plt.style.use('dark_background')`, custom `rcParams`)
- Include infrastructure code (`os`, `random.seed`, `os.makedirs`, directory creation)
- Include case study datasets — only the chapter's primary dataset(s)
- Modify any code cells in the chapter body
- Touch the web app files

## Inputs

Before generating, collect these two sources:

1. **The chapter `.qmd`** — `notebooks_quarto/chNN_*.qmd`. Source of truth for all code: imports, data URLs, functions, analytical steps.
2. **The chapter web app** — `web-apps/chNN/template.html` (or `dashboard.html` if no template exists). Source of truth for which key concepts matter most — each widget title and key-concept callout tells you what the chapter's most important ideas are.

If the web app does not exist, proceed using only the `.qmd` — derive key concepts from the chapter's `> **Key Concept N.M:` blockquotes instead.

## Workflow

Follow these phases in order.

### Phase 1 — Read the chapter

Read the full chapter `.qmd` and extract:

- **All imports** from the Setup cell (the first code cell, usually with `code-fold: true`)
- **Dataset URL(s)** and loading method (`pd.read_stata()`, `pd.read_csv()`, etc.) — only the primary dataset, not case study datasets
- **Key functions and methods** used in the chapter body (e.g., `.describe()`, `ols().fit()`, `.summary()`, `ax.scatter()`, `ax.hist()`)
- **The analytical workflow** — the sequence of steps from data loading to final results
- **Key variable names** — the column names used in regressions, plots, and interpretations

### Phase 2 — Read the web app

Read `web-apps/chNN/template.html` and extract:

- **Widget titles** — each `<h2>` inside a `<section class="widget">` tells you the concept name
- **Key concept callouts** — each `.key-concept` box states the core idea the widget teaches
- **The progression** — widgets are ordered pedagogically; the code summary should follow the same arc

Build a mapping: widget title -> key concept -> corresponding code step in the chapter.

If no web app exists, extract key concepts from the chapter's `> **Key Concept N.M:` blockquotes instead.

### Phase 3 — Design the code block

Using the web app key concepts as a guide, decide:

1. **Which code steps to include** — each web app widget/key concept should map to at least one code step
2. **Which libraries to import** — only those actually used in the included steps
3. **What to exclude** — infrastructure, dark theme, case study data, redundant variations
4. **The step order** — follow the web app's pedagogical progression (which mirrors the chapter's narrative arc)

Typical structure for most chapters:

```
# LIBRARIES
# STEP 1: Load data
# STEP 2: Explore / describe (descriptive statistics)
# STEP 3: Visualize (the key visualization pattern of the chapter)
# STEP 4: Model / compute (the chapter's main analytical method)
# STEP 5: Interpret results (extract and print key statistics)
# STEP 6: Advanced application (comparison, diagnostics, or extension)
```

The number of steps varies by chapter (5-8 is typical). Each step should correspond to one or more web app key concepts.

### Phase 4 — Write the code block

Generate the code following these formatting rules:

**Structure:**

- Start with a banner: `# CHAPTER N CHEAT SHEET: Chapter Title`
- Group imports under `# --- Libraries ---` with inline comments explaining each library's role
- Separate each step with a banner: `# ===...=== / # STEP N: Description / # ===...===`
- End with the final analytical output (a summary table, a key statistic, or a comparison)

**Comments:**

- Every import gets an inline comment explaining its purpose (e.g., `# data loading and manipulation`)
- Every step gets a 1-2 line comment explaining **why** this step matters, not what it does syntactically
- Key methods get brief inline comments on first use (e.g., `# marginal effect: $/sq ft`)
- Do NOT over-comment — one comment per conceptual idea, not per line

**Self-containedness:**

- All imports at the top
- Dataset URL defined as a variable (full URL, not referencing a constant from the Setup cell)
- All intermediate variables defined within the block
- No references to variables from the chapter's other code cells
- Must run in a fresh Python environment (Google Colab)

**Styling:**

- Use default matplotlib colors (no hex codes from the dark theme)
- Use `figsize=(10, 6)` for plots (standard)
- Use descriptive axis labels and titles
- For regression output, use both `print()` for key stats and `.summary()` for the full table

### Phase 5 — Insert into the chapter

Insert the code summary into the Key Takeaways section of the `.qmd` file:

**Location:** After the last bold-header subsection in Key Takeaways (e.g., `**Prerequisites and Mathematical Background:**`) and before the `---` horizontal rule that precedes `**Next Steps:**`.

If no `---` / `**Next Steps:**` divider exists, insert before `## Practice Exercises`.

**Format:**

```markdown
**Python Libraries and Code:**

This single code block reproduces the core workflow of Chapter N. It is self-contained — copy it into an empty notebook and run it to review the complete pipeline from [brief description of what the pipeline covers].

` ` `python
[the generated code block]
` ` `

**Try it yourself!** Copy this code into an empty Google Colab notebook and run it: [Open Colab](https://colab.research.google.com/notebooks/empty.ipynb)
```

The intro sentence should be adapted to each chapter — mention the specific topic (e.g., "from data loading to hypothesis testing" or "from summary statistics to confidence intervals").

### Phase 6 — Verify

1. Render the chapter: `cd book && quarto render notebooks_quarto/chNN_*.qmd`
2. Confirm no rendering errors
3. Visually check the output — the code block should appear as a syntax-highlighted, always-visible block in the Key Takeaways section

## Code block design rules

These rules are non-negotiable. They encode the conventions proven on Chapter 1.

| Rule | Rationale |
|------|-----------|
| Markdown code block (` ```python `) | Students copy it; it's not executed in the notebook |
| Always visible — no `code-fold` | This is a reference cheat sheet, not hidden content |
| Self-contained | Must run end-to-end in an empty Google Colab notebook |
| No dark theme styling | Colab uses a white background by default |
| No infrastructure code | `os`, `random.seed`, `os.makedirs` are not core econometrics |
| Steps aligned with web app key concepts | The web app defines what matters most pedagogically |
| Comments explain purpose, not syntax | "regresses y on x" not "calls the ols function" |
| Banner separators between steps | `# ===...===` for visual clarity and scannability |
| Single code block | One cheat sheet, not a fragmented multi-block tutorial |
| Default matplotlib colors | No hex codes tuned for the book's dark theme |
| Primary dataset only | Case study datasets belong in Practice Exercises |
| 5-8 steps typical | Enough to cover the core workflow without overwhelming |
| End with Colab link | Always include the "Try it yourself!" line |

## What to include vs. exclude

**Always include:**

- The 3-4 core libraries the chapter uses (pandas, matplotlib, statsmodels, scipy, etc.)
- Loading the chapter's primary dataset from its GitHub URL
- Descriptive statistics (`.describe()`, `.value_counts()`, etc.) — every chapter uses these
- The chapter's signature visualization (scatter, histogram, box plot, etc.)
- The chapter's main analytical method (OLS, t-test, confidence interval, F-test, etc.)
- Extracting and printing key results with interpretation
- At least one step that connects to the chapter's central takeaway message

**Always exclude:**

- Setup infrastructure (`os`, `random`, `RANDOM_SEED`, directory creation)
- Dark theme code (`plt.style.use('dark_background')`, `plt.rcParams.update(...)`)
- Case study datasets (Mendez convergence clubs, DS4Bolivia) — those are for practice
- Redundant variations of the same analysis (e.g., if the chapter shows 3 scatter plots, include 1)
- Print statements for setup confirmations (`"Setup complete!"`)
- Intermediate debugging or exploration code
- Code that only exists to support later sections (e.g., helper functions used once)

**Use judgment for:**

- Multiple regression models — include if comparing models is a key concept, otherwise pick the main one
- Data cleaning steps — include if the chapter teaches data preparation, otherwise skip
- Advanced methods — include if they are a key concept in the web app, otherwise skip

## Handling chapters without web apps

If a chapter does not yet have a web app in `web-apps/chNN/`:

1. Extract key concepts from the chapter's `> **Key Concept N.M:` blockquotes
2. Use the chapter's section headers (`## N.1`, `## N.2`, etc.) to determine the narrative arc
3. Follow the same 6-phase workflow, substituting key concept blockquotes for web app widgets

## Handling chapters with existing code summaries

If the chapter already has a `**Python Libraries and Code:**` subsection:

1. Read the existing code block
2. Determine if it needs updating (e.g., chapter content changed, web app was added/modified)
3. If updating, replace the existing block — do not create a second one
4. If the existing block is adequate, report "Code summary already exists and is up to date" and stop

## Reference files

- `references/CH01_REFERENCE.md` — the Chapter 1 code summary with annotations explaining each design decision. Use this as the gold standard when generating summaries for other chapters.

## Relationship to other skills

```
/chapter-standard chNN              (ensure chapter structure is correct)
      |
/improve-readability chNN           (improve prose and code clarity)
      |
/proofread chNN                     (fix text quality issues)
      |
/create-chapter-code-summary chNN   (THIS SKILL — add code cheat sheet)
      |
/compile-book chNN                  (generate PDF)
```

The code summary should be one of the last things added before PDF generation, since it depends on the chapter's code being finalized.

The web app is an **input** to this skill (read-only), not a dependency that must be created first. If the web app exists, use it to guide key concept selection. If not, use the chapter's Key Concept blockquotes.

---

**Version:** 1.0
**Created:** 2026-04-18
**Prerequisite:** Chapter content finalized in `.qmd`. Web app recommended but not required.
**Audience:** Beginner econometrics students — comments and structure should assume no prior Python experience beyond the chapter itself.
