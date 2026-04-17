---
name: web-app
description: Creates a single-file interactive HTML dashboard for a metricsAI chapter. Follows the design and pedagogical conventions established by the Chapter 2 app (Plotly.js, brand palette, light/dark theme, embedded JSON, URL-hash state, Try-this prompts per widget, Reset buttons, delta readouts). Flexible across chapters via reusable widget snippets and a scaffolding script. Invoke via /web-app <chNN>. The goal is pedagogical learning through interaction — design widgets that target specific Key Concepts, not pretty charts.
context: fork
agent: Explore
---

# Web App Skill — Interactive Chapter Dashboards

Produces a single self-contained HTML dashboard for a metricsAI chapter, where students manipulate sliders, toggles, and dropdowns to build intuition for that chapter's Key Concepts. One app per chapter, stored in `web-apps/chNN/dashboard.html`.

## When to use

Invoke with `/web-app chNN` (e.g. `/web-app ch05`) when the user wants a new chapter dashboard. Do not auto-activate on keyword matches — the skill requires a plan-approval step that benefits from explicit invocation.

## Guiding principle

**The skill is a scaffold, not a generator.** Every new chapter needs real pedagogical thinking about which Key Concepts benefit from interaction and what specific experiments students should try. The skill automates the infrastructure (branding, theme system, hash state, stats helpers) so authorship effort goes into teaching, not plumbing.

Read `docs/pedagogical_principles.md` before starting any chapter. It is the durable statement of why this skill exists.

## Workflow

Five phases. Do not skip ahead.

### Phase 1 — Understand the chapter

Read the chapter source of truth:

- `notebooks_quarto/chNN_*.qmd` (authoritative)
- `notebooks_colab/chNN_*.md` (for quick reference)

Extract into an inventory (keep it short, present to user at phase 2):

- Chapter title, number of sections
- Key Concepts (labeled boxes, typically 7–11 per chapter) — list each with its topic
- Datasets referenced — file paths, key columns, row counts
- Specific numerical examples quoted in prose — these become correctness anchors
- Formulas introduced
- Case studies present (note their existence; do not include them in this app)

Use the Explore agent if the chapter is unfamiliar. Do not propose a widget list yet.

### Phase 2 — Design widgets

Decide which 6–10 widgets to build. For each:

- Target Key Concept (one widget ↔ one concept)
- Widget pattern from `templates/widgets/` (or propose a new one if no existing pattern fits)
- Dataset(s) used
- Default state (what the chart looks like on first load and after Reset)
- One-line learning objective

Consult `docs/widget_catalog.md` for the mapping from concepts to widget patterns.

Skip Key Concepts that are purely definitional — not every concept needs interactivity. Prefer fewer, sharper widgets over many shallow ones.

**Present the design as a plan file. Get user approval before scaffolding.** The plan file lives at `web-apps/chNN/PLAN.md` (it will be updated later with what was actually built).

### Phase 3 — Scaffold

Run:

```bash
python3 .claude/skills/web-app/scripts/scaffold_chapter.py chNN "<Chapter Title>"
```

This creates (without content):

- `scripts/build_chNN_webapp.py` — from `templates/build_webapp.py`
- `scripts/chNN_webapp_template.html` — from `templates/base.html`
- `web-apps/chNN/` directory (empty until build)

### Phase 4 — Implement

Per widget, in this order:

1. Copy the widget's HTML snippet from `templates/widgets/<pattern>.md` into the template inside `<main>`, between the existing placeholder markers.
2. Copy the JS snippet into the `<script>` section of the template before the reset/hash layer.
3. Adapt to the chapter's datasets (dataset IDs, axis labels, default values).
4. Author the Try-this block: 2–4 numbered imperative experiments specific to this dataset. Not generic. Specific.
5. Register the widget's controls in `REG` inside the reset/hash layer (widget-head `data-reset` attribute, per-control `id`/`group` with sensible chapter-default).
6. Add a nav anchor link.
7. In `build_chNN_webapp.py`, write the dataset loader and add to the JSON payload.
8. Run `python3 scripts/build_chNN_webapp.py`.
9. Sanity-check printed summary stats against the chapter's quoted numbers.
10. Repeat for next widget.

### Phase 5 — Verify + document

```bash
python3 .claude/skills/web-app/scripts/verify_app.py web-apps/chNN/dashboard.html
```

This runs:

- `node --check` on the inlined JS
- Placeholder leftover scan (`{{…}}`)
- JSON data-island structural check
- Optional headless browser render (if Playwright is installed)

Then update `web-apps/chNN/PLAN.md`:

- What was built (list widgets, concepts covered)
- What was skipped (with reasoning)
- Supplementary datasets used (with attribution)
- Known issues / future improvements

Run `docs/checklist.md` end to end and sign off each item.

Open the dashboard in a browser for visual confirmation. Commit.

## Conventions (non-negotiable)

These are hard-earned from Chapter 2. Do not deviate without explicit user discussion.

- **Stack**: Plotly.js 2.35 via CDN, Inter + JetBrains Mono from Google Fonts, vanilla JavaScript (no framework). No build step beyond `build_chNN_webapp.py`.
- **Palette**: ElectricCyan `#008CB7`, SynapsePurple `#7A209F`, DataPink `#C21E72`. See `docs/branding.md`.
- **File layout**:

  ```
  scripts/
    build_chNN_webapp.py           # build script
    chNN_webapp_template.html      # HTML template with {{DATA_JSON}}
    fetch_<source>.py              # (optional) external data fetchers
  web-apps/
    chNN/
      dashboard.html               # built artifact (committed)
      PLAN.md                      # chapter-specific plan + sign-off
  data/
    <chapter data>                 # .DTA / .csv / etc. (source)
  ```

- **Data**: embedded as a JSON `<script type="application/json">` island. Pre-computed in the build script. No runtime network fetches for data.
- **Theming**: light/dark toggle with `localStorage` key `metricsai-theme`. Charts re-render on toggle by reading CSS variables.
- **State**: every interactive control registered in the `REG` registry at the bottom of the template. URL hash reflects non-default state so scenarios are shareable.
- **Resets**: every widget has a `↺ Reset` button returning its controls to the chapter default.
- **Try-this**: every widget has a cyan-bordered `.try-this` block with 2–4 numbered imperative experiments tied to the target Key Concept.
- **Fidelity**: any summary statistic displayed in the app must match the value quoted in the chapter prose, within rounding. Diverging values must be flagged in `PLAN.md`.

## Flexibility across chapters

Four dimensions:

1. **New widget types.** When a chapter needs a pattern not in `templates/widgets/`, invent it for that chapter. Then save it back to the catalog as `templates/widgets/<name>.md` so the next chapter can reuse it. Update `docs/widget_catalog.md`.
2. **New data sources.** Add `scripts/fetch_<source>.py` as needed. Keep the build script offline (reads committed CSV/DTA).
3. **Narrative concepts.** Not every Key Concept needs interactivity. A widget may have no controls, just a labelled static illustration. Document the reasoning in `PLAN.md`.
4. **Shared widgets across chapters.** Many widgets (histogram, boxplot, scatter, regression) appear in multiple chapters. Reuse snippets; do not author new ones for the same pattern.

## Out of scope

- Case-study apps (convergence clubs, Bolivia, etc.) — separate dashboards per chapter. Plan independently.
- Auto-linking from the project website — do in a follow-up after several chapter apps exist.
- Modifying the book itself (`.qmd`, Quarto config) — the apps are parallel artifacts.
- Multi-page apps — one chapter, one HTML file.
- Frameworks (React, Vue, etc.) — vanilla JS only.

## References

| File | Purpose |
|---|---|
| `docs/pedagogical_principles.md` | The "why" — the 10 rules the skill is built around |
| `docs/widget_catalog.md` | Concept → widget pattern mapping |
| `docs/branding.md` | Palette, fonts, layout, accessibility |
| `docs/checklist.md` | Pre-commit verification list |
| `templates/base.html` | Full HTML scaffold (CSS + JS helpers + theme + hash/reset) |
| `templates/build_webapp.py` | Python build-script template |
| `templates/widgets/*.md` | Reusable widget patterns (HTML + JS in Markdown) |
| `scripts/scaffold_chapter.py` | Creates per-chapter build script, template, plan directory |
| `scripts/verify_app.py` | Runs JS check, JSON structural check, placeholder scan |
| `web-apps/ch02/dashboard.html` | Reference implementation — the app this skill was distilled from |
| `web-apps/ch02/PLAN.md` | Reference plan format |
