# Slide mapping (chapter → deck)

Heuristics that turn a metricsAI chapter (`notebooks_quarto/chNN_*.qmd`) + its exported
figures into an assertion-titled, one-idea-per-slide, 3-act **essentials** deck (~15–22 slides).
Read this in Phase 1 (to draft the outline) and Phase 3 (to assemble slides). It applies the
principles in `rhetoric-of-decks.md` using the Quarto markdown in `slide-archetypes.md`.

The audience is always **Teaching** (students) — these are textbook chapters. The goal is the
chapter's *most essential ideas* in a clear, sequenced narrative, not full coverage.

---

## Chapter element → slide → act

| Chapter element | Slide archetype | Act |
|---|---|---|
| `title:` + the chapter's one-line framing | Title (1) — **visual summary** is the key visual | — |
| Chapter Overview hook / the motivating example | Narrative/Hook (4) | I |
| "What you'll learn" bullets | Agenda (2) | I |
| Key Concepts (the chapter's bold terms + definitions) | Narrative (4) / Two-column (9) | I → II |
| Each core numbered section (`## 5.x`) | Figure (5) / Equation (8) / Table (6) — one per section | II |
| A display equation `$$…$$` (e.g. the OLS line, R²) | Equation (8) — one each | II |
| A `{python}` code cell teaching the workflow | Code (7) — illustrative `{.python}` | II |
| A section's exported figure (from the manifest) | Figure (5), caption-as-assertion | II |
| A results / summary-statistics table | Table (6), key cell highlighted | II → III |
| A headline relationship (e.g. slope, r, R²) | Headline-result (11) — optional | III |
| "Association ≠ causation" / assumptions / caveats | Devil's-Advocate (10) | III |
| Key Takeaways | Closing (12), single sentence | III |
| Each slide's concluding line | Takeaway card `[…]{.takeaway .fragment}` (component) | any |

Each act is preceded by a Divider (3). The **per-slide** takeaway card (the DataPink accent card
each content slide ends on) is distinct from the single **Closing** divider — the card restates
that one slide's assertion; the Closing is the deck's final thesis.

---

## Principles applied

- **Figure-first, code-first.** A figure or code block is its *own* slide titled with its finding
  — never buried under bullets.
- **One idea per slide.** Split any source paragraph that carries two assertions into two slides;
  merge adjacent thin slides.
- **Assertion titles.** Every content slide's `##` is a sentence stating the finding (see
  `rhetoric-of-decks.md` examples). Pull the claim from the chapter's interpretation prose for
  that figure/table/section.
- **Speaker notes carry the prose.** The chapter's explanatory text goes into `::: {.notes}`, not
  onto the slide.

---

## Essentials coverage — target ~15–22 slides

Textbook chapters have 8–12 numbered sections plus illustrations and practice exercises. A deck
that mirrors all of them is a lecture transcript, not a talk. For the **essentials** deck:

- Keep **one slide per *core* section** — the sections that carry the chapter's load-bearing ideas
  (for ch05: scatter → correlation → regression line → model fit → association-vs-causation).
- Fold minor "Illustration:" / "Special case:" subsections into the parent section's slide or into
  speaker notes.
- **Skip** the Setup block, the code-summary cheat sheet, and the Practice Exercises / Case Studies
  (they are hands-on, not talk material).
- Build the agenda from the "What you'll learn" bullets; build the Key Concepts slide(s) from the
  chapter's bold **Key Concept** terms.

If the mapping would exceed ~22 slides, drop the least load-bearing figures (see capping) and merge
thin narrative slides. If it falls under ~15, the chapter is short — that's fine; do not pad.

---

## Code coverage (REQUIRED — one code slide per main tool)

The Python code is the point of these chapters. **Every deck MUST include at least one Code slide
(archetype 7), and in general one per *main tool* the chapter introduces** — the new packages,
functions, or methods a student is meant to walk away able to use. Identify them in Phase 1 from the
chapter's `{python}` cells, its "Setup" imports, and its Key-Takeaways code summary; the smoke test
fails a deck with zero code blocks.

Rule of thumb for the essentials deck:

- **One code slide per distinct tool/method**, placed next to the section that introduces it — e.g.
  for ch05: `plt.scatter(...)` (visualize) · `df.corr()` / `df.cov()` (measure) · `pf.feols(...)`
  (estimate). Three tools → three short code slides.
- Each block is **self-contained and runnable** (quiet install if needed + imports + data load + the
  tool call), **every line commented**, with the `↗ Try it in Colab` pill — see `slide-archetypes.md`
  archetype 7.
- If two tools are tiny and naturally paired, one slide may show both; never cram more than one
  *concept* onto a code slide, and keep each block ≤ ~10 lines (push extra to the notes).
- A theory-only chapter with no new tool is the rare exception — still include the one code slide that
  reproduces its core computation.

## The MB/MC pacing pass (run before rendering)

Walk every slide and every fragment; apply `rhetoric-of-decks.md` § MB/MC:

- Cut/merge **underloaded** slides (a word that wants a sentence; a point the audience already inferred).
- Split/simplify **overloaded** slides (> 5 bullets, two data series, a wall of prose). Push overflow
  to `::: {.notes}`.
- No slide should need > 4 fragment advances.
- Allow one or two deliberate dense "jump scare" slides for effect — on purpose.

---

## Figures: export, selection, capping

- **Export** the chapter's figures in Phase 1 with
  `python3 .claude/skills/write-slides/scripts/export_chapter_figures.py chNN`. This reuses the
  book-rendered PNGs (or renders fresh) and writes `slides/chNN/_figcache/figures_manifest.json` —
  each entry `{cache_file, src, section, heading}` — plus `visual_summary.png`. The chapter plots use
  `plt.style.use('dark_background')`, so the PNGs already sit on a dark canvas that matches the deck.
- **Select** the single load-bearing figure per core section from the manifest (match on the
  `heading` / `section` field). Copy the chosen `_figcache/*.png` into `slides/chNN/figures/` and
  reference each as `![caption](figures/<cache_file>)`.
- **Cap at 12 on-slide figures.** If more are load-bearing, keep one per distinct finding and **log
  the dropped filenames** in the Phase-5 report — never silently drop.
- Pass `--source render` to the exporter after editing a chapter's plots, so the figures are current.

---

## Tables: Markdown → Quarto markdown

Reuse the chapter's table almost verbatim (archetype 6). Keep the 2–3 columns that carry the
argument; the rest → notes. Tag the headline cell `[…]{.key}` (renders DataPink). The theme styles
it booktabs-ish and right-aligns numbers (`tabular-nums`).

## Title slide: the visual summary, full-bleed

The title slide is **only** the chapter's visual-summary image, filling the whole slide — no title,
subtitle, or byline text. Set the front-matter `visual-summary:` field to `figures/visual_summary.png`
(copied from `_figcache/` by the skill); the `title-slide.html` partial paints it as the slide
**background** (`data-background-image`, `size=contain` → the entire summary, no crop). There is **no
numeric key-result strip** (that was for research posts).

---

## Writing equations (plain LaTeX — the .qmd is Pandoc)

Chapter `.qmd` files are already Pandoc + MathJax, so copy a display equation straight across — no
Goldmark escaping to strip. Inline math `$…$`, display `$$…$$`. Verify visually in the browser
(MathJax errors render visibly but the static smoke test can't catch them — see `render-and-fix.md`
§7 for unsupported macros, §12 for the katex-not-mathjax guard).

## Math symbols → LaTeX (never literal Unicode)

`R²`, `α̂`, and other Unicode math render inconsistently. Convert **all on-slide** math symbols to
LaTeX `$...$`:

| Unicode | LaTeX | · | Unicode | LaTeX |
|---|---|---|---|---|
| `R²` | `$R^2$` | · | `±` | `$\pm$` |
| `α̂` `β̂` | `$\hat\alpha$` `$\hat\beta$` | · | `≈` | `$\approx$` |
| `α` `β` `λ` `σ` | `$\alpha$` `$\beta$` `$\lambda$` `$\sigma$` | · | `∑` `∈` `×̄` | `$\sum$` `$\in$` `$\bar x$` |

- **Mixed numbers:** in captions/bullets/comments/labels write the full expression (`slope $b_2 =
  61.5$`); but keep the DataPink `[…]{.key}` table cells and the giant `[…]{.bignum}` as **styled
  text** (math drops their colour/size). Plain standalone numbers (284, 0.79) stay text.
- **Notes stay Unicode.** The reveal speaker-notes window doesn't run the math renderer, so LaTeX
  source would show raw there — keep `R²`, `α̂` etc. inside `::: {.notes}`.
- Engine: **MathJax** — Quarto revealjs's default, from a CDN (reveal.js is bundled locally; math
  needs a network). Do NOT set `html-math-method: katex` — it is broken in revealjs (why, and the
  static/browser guards that catch it → `render-and-fix.md §12`).

---

## Edge cases (full handling in `render-and-fix.md`)

- **No exported figures (a theory-heavy chapter):** lean on Narrative + Equation + Two-column +
  Closing; the visual summary still anchors the title slide; do not auto-draw diagrams.
- **No single headline number:** that is normal for teaching chapters — skip the optional
  Headline-result slide and let the assertion titles + takeaway cards carry the argument.
- **Very long code:** skeleton on-slide (`{.python}`, illustrative) + full workflow in notes; if
  still overflowing, split into a vertical sub-slide stack.
- **A chapter edited after the last book render:** pass `--source render` to the exporter so the
  figures reflect the current plots.
