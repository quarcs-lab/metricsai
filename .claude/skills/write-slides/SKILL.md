---
name: write-slides
description: Generate a branded Quarto reveal.js slide deck for a metricsAI chapter. Reads the chapter .qmd (notebooks_quarto/chNN_*.qmd) — its Overview, "What you'll learn" bullets, Key Concepts, numbered sections, figures, tables, equations, and Key Takeaways — exports the chapter's figures to PNG, then autonomously (no interview) distills the chapter to its most essential ideas as an assertion-titled, one-idea-per-slide, 3-act essentials deck (~15–22 slides). Writes slides.qmd + a metricsAI dark-brand SCSS theme + a visual-summary title-slide partial into slides/chNN/, renders with `quarto render` to index.html + slides_files/, and verifies (render + static smoke test + browser math-check). Dark brand (ElectricCyan/SynapsePurple/DataPink); assertion titles; one idea per slide; takeaway cards; the chapter visual summary is the title slide. English-only. Standalone — not wired into the book/website/PDF/auto-sync.
argument-hint: "<chNN> [--no-verify]"
disable-model-invocation: true
user-invocable: true
---

# Write Slide Deck: a branded Quarto reveal.js talk for a metricsAI chapter

Produce a **Quarto reveal.js deck** for a textbook chapter. The deck presents the chapter's most
essential ideas as an **assertion-titled, one-idea-per-slide narrative** — the chapter's own
figures, tables, and equations, restructured into a teaching talk with reveal.js's built-in
**menu, chalkboard, speaker view, preview-links, and overview**.

The deck is authored as a `slides.qmd` (`format: revealjs`) and rendered by the **Quarto CLI** to a
standalone **`slides/chNN/`** directory. It is branded to a **fixed** metricsAI dark theme and needs
no CDN (reveal + plugins are bundled by Quarto; only MathJax loads from a CDN).

The workflow is **autonomous** (a deliberate departure from the upstream `beautiful_deck`
interview): given `chNN`, the skill derives the audience (Teaching), the takeaways (from the
chapter's "What you'll learn" + Key Takeaways), and the full outline (from the chapter's sections),
then builds, renders, and verifies in one pass. The user reviews the rendered deck afterward. The
craft (3-act arc, assertion titles, pedagogical movement, MB/MC pacing, Devil's-Advocate) lives in
[`references/rhetoric-of-decks.md`](references/rhetoric-of-decks.md); the derivation heuristics that
replace each interview round are in
[`references/interview-questions.md`](references/interview-questions.md).

---

## What this skill does NOT do

- **Does not modify the chapter `.qmd` or any other chapter format.** It only reads the chapter and
  writes into `slides/chNN/`. (No link injection, no edits to `notebooks_quarto/`.)
- **Does not execute the chapter's code in the deck.** Deck code blocks are illustrative (`{.python}`,
  not `{python}`), so `quarto render slides.qmd` is a pure Pandoc render — no kernel or package install.
- **Does not re-run the chapter pipeline on every build.** Figures are exported once by
  `scripts/export_chapter_figures.py` (reusing the book-rendered PNGs, or rendering fresh with
  `--source render`).
- **Does not design a theme per deck.** The brand is **fixed** — `site-brand.scss` is copied verbatim
  every run (metricsAI dark brand).
- **Does not produce a single self-contained file.** The chalkboard plugin is incompatible with
  `embed-resources`, so the deck ships `index.html` + `slides_files/`.
- **Does not export a PDF.** It documents reveal.js's `?print-pdf` recipe (Phase 5).
- **Does not wire the deck into the book, website, PDF pipeline, or auto-sync hook.** `slides/` is a
  standalone artifact (the book uses an explicit chapter list; the sync hook is scoped to
  `notebooks_quarto/*.qmd`). Linking a deck from the website is a separate, manual step.
- **Does not commit, push, or open a PR.** Phase 5 prints a copy-pasteable commit snippet.
- **Does not create ES/JA copies.** English-only.
- **Requires the Quarto CLI** (`/Users/carlosmendez/opt/bin/quarto`, 1.8+) to (re)generate.

---

## Example invocations

```
# Standard run: read the chapter, export figures, derive the outline, write slides.qmd + theme +
# partial, `quarto render` → index.html + slides_files/, verify.
/write-slides ch05
/write-slides ch09

# Skip verification (render + smoke test + math-check). A minimal file sanity check still runs.
/write-slides ch07 --no-verify
```

---

## Deliverables

| Path | Purpose |
|---|---|
| `slides/chNN/slides.qmd` | Deck source (`format: revealjs`) — the only per-chapter authored file |
| `slides/chNN/site-brand.scss` | revealjs theme (copied verbatim from `references/templates/`) |
| `slides/chNN/title-slide.html` | title-slide partial rendering the chapter visual summary (copied verbatim) |
| `slides/chNN/figure-zoom.html` | click-to-zoom lightbox for figures + the title visual summary (copied verbatim; injected via `include-after-body`) |
| `slides/chNN/figures/` | the chosen chapter figures + `visual_summary.png` (copied from `_figcache/`) |
| `slides/chNN/index.html` | the rendered deck (`quarto render` output) |
| `slides/chNN/slides_files/` | reveal.js + plugins + libs (`quarto render` output, ~8 MB) |

**Commit the whole `slides/chNN/` dir** — source **and** rendered output (`index.html` +
`slides_files/` + `figures/`). The deck is a standalone pre-rendered artifact; nothing renders it
downstream. Only the staging cache and Quarto cache are gitignored (`slides/*/_figcache/`,
`slides/*/.quarto/`). See `references/render-and-fix.md` §8.

---

## metricsAI dark-brand palette (fixed — every deck)

`site-brand.scss` carries these (the metricsAI brand on a dark canvas); do not vary them.

| Token | Hex | Use in the deck |
|---|---|---|
| Canvas (dark) | `#0f1117` | The deck canvas — **dark mode**. Set via `$body-bg: $canvas`. |
| Body text | `#e6e9ef` | Body copy on the dark canvas. Set via `$body-color`. |
| Headings | `#f4f6fa` | Assertion titles / headings (near-white on the dark canvas). |
| Muted | `#9aa6bd` | Captions, figure/equation glosses, byline meta (`$muted`). |
| **ElectricCyan** | `#008CB7` | Assertion-title underline, list markers, `strong`, links, **Act I divider** |
| **SynapsePurple** | `#7A209F` | h3 column-header underline, **Act II divider**, optional big-number slide bg |
| **DataPink** | `#C21E72` | **Act III divider**, `.takeaway` accent card, `.bignum`, key table cell |
| Display/body font | Inter | Title, headings, body |
| Mono font | JetBrains Mono | Code blocks |

The DataPink also carries the **`.takeaway` card** — each content slide's concluding line (see the
**Takeaway card** component in `slide-archetypes.md`).

---

## Phase 1: Pre-flight (read-only)

Do not write any deck file in this phase (the figure exporter writes only into `_figcache/`).

### 1.1 Parse arguments
- **Chapter id** — first positional token, e.g. `ch05`. Mandatory.
- **`--no-verify`** — skip Phase 4 (a minimal file sanity check still runs).
Reject unknown flags.

### 1.2 Locate the chapter
Glob `notebooks_quarto/<chNN>_*.qmd`. Hard-fail with a clear message if absent.

### 1.3 Detect an existing deck
If `slides/<chNN>/` already has a `slides.qmd`, ask: **(a)** overwrite [default], **(b)** cancel.
(This is the one allowed interactive prompt — a safety guard, not an interview.)

### 1.4 Read the chapter
Read the chapter `.qmd` in full. Extract: `title:`; the Chapter Overview + the **"What you'll learn"**
bullets; the **Key Concepts** section (bold terms + definitions, and inline `> **Key Concept N.M**`
blocks); every numbered `## N.x` section with its interpretation prose (→ speaker notes); every
Markdown table; every `$$…$$`; the **Key Takeaways**. Note the chapter's key caveat (often
"association ≠ causation") for the Devil's-Advocate slide. **Identify the chapter's main tools** —
the packages/functions/methods it introduces (from the Setup imports, the `{python}` cells, and the
Key-Takeaways code summary), e.g. for ch05: `plt.scatter`, `df.corr()`/`df.cov()`, `pf.feols`. Each
main tool needs its own Code slide (see Phase 2 + `slide-mapping.md § Code coverage`).

### 1.5 Export the figures
Run:
```bash
python3 .claude/skills/write-slides/scripts/export_chapter_figures.py <chNN>
```
This writes `slides/<chNN>/_figcache/` with `figures_manifest.json` (each figure → `{cache_file,
src, section, heading}`) + `visual_summary.png`. Add `--source render` if the chapter's plots were
edited since the last book render (needs the `.venv` kernel). Read the manifest to build the figure
inventory. **Cap on-slide figures at 12**; plan to log any dropped filenames.

### 1.6 Derive the outline
Following [`references/interview-questions.md`](references/interview-questions.md) +
[`references/slide-mapping.md`](references/slide-mapping.md): audience = Teaching; takeaways ← "What
you'll learn" + Key Takeaways; title key visual = the chapter visual summary; arc = the 3-act
mapping over the chapter's **core** sections (one slide each), targeting **~15–22 slides**. Skip
Setup / code-summary / Practice Exercises / Case Studies.

---

## Phase 2: Derive the deck (autonomous — no interview)

This skill does **not** call `AskUserQuestion` (except the overwrite guard in 1.3). Apply the
heuristics in [`references/interview-questions.md`](references/interview-questions.md):

- **Audience** = Teaching (fixed).
- **Takeaways** = the chapter's "What you'll learn" bullets + Key Takeaways → Act-III assertions +
  per-slide `.takeaway` cards.
- **Outline** = the 3-act arc over the core sections (see the template in
  `interview-questions.md § Round 3`), ~15–22 slides, MB/MC-paced.
- **Code slides (required)** = **at least one Code slide per main tool** the chapter introduces
  (archetype 7; placed next to the section that introduces the tool). The Python code is the point of
  these chapters — a deck with zero code blocks fails verification. See `slide-mapping.md § Code
  coverage`.
- **Devil's-Advocate** = default-on for the chapter's key caveat.

Record the resolved outline (one line per slide: `archetype · assertion title`) in a short SCOPE
note printed to the user, then proceed directly to writing — no approval gate.

---

## Phase 3: Generate the deck

### 3.1 Create the folder
`slides/<chNN>/`.

### 3.2 Copy verbatim templates
Copy unchanged from `references/templates/`: **`site-brand.scss`**, **`title-slide.html`**, and
**`figure-zoom.html`** (the click-to-zoom lightbox — every figure **and the title visual summary**
become clickable to a full-screen overlay with zoom/pan controls; wired via the template's
`include-after-body: figure-zoom.html`).

### 3.3 Select + copy figures
From `_figcache/figures_manifest.json`, pick the single load-bearing figure per core section (match
on `heading`/`section`). Copy the chosen `_figcache/*.png` **and** `_figcache/visual_summary.png`
into `slides/<chNN>/figures/`. Reference each figure as `![caption](figures/<cache_file>)`.

### 3.4 Author `slides.qmd`
Start from `references/templates/slides.qmd.tmpl`. Fill the front matter:
- `title` (from the chapter) and a one-line `subtitle` (the chapter's framing).
- `deck-author: "Carlos Mendez"`, `deck-author-url: "https://carlos-mendez.org"`,
  `institute: "Nagoya University (GSID)"`, `date: today`, `date-format: long`.
- `visual-summary: "figures/visual_summary.png"`.

Write the body from the derived outline using
[`references/slide-archetypes.md`](references/slide-archetypes.md) +
[`references/slide-mapping.md`](references/slide-mapping.md): `##` assertion titles; figures
`![caption](figures/…)`; Markdown tables with `[cell]{.key}`; code ` ``` {.python
code-line-numbers="…"} ` (**illustrative, never `{python}`**); equations `$$…$$`; columns
`::: {.columns}`; speaker notes `::: {.notes}`; dividers `# … {.divider background-color="…"}`
(Act I `#008CB7`, Act II `#7A209F`, Act III `#C21E72`). **Code blocks must be self-contained and
runnable** — lead with a quiet install of any package Colab lacks (`!pip install -q pyfixest`), then
the imports *and* the chapter's own data-load line with the full URL inlined
(`pd.read_stata(GITHUB_DATA_URL + '…')`), so a reader can paste the block into an empty Colab cell
and reproduce the result (illustrative `{.python}`, never executed by the deck); **comment every
line pedagogically** (a short trailing `#` note on what each line does — put a long line's comment on
the line above to avoid overflow); **add the `↗ Try it in Colab` `.colab-link` pill** (to `https://colab.research.google.com/notebooks/empty.ipynb`) on its
own line below each code fence (archetype 7). **End each substantive content slide with its takeaway
card** — `[…]{.takeaway .fragment}`; reserve `.comment` for small figure/equation
glosses. **Write all on-slide math as LaTeX `$...$`, never literal Unicode** (`$R^2$` not `R²`);
notes stay Unicode (slide-mapping § "Math symbols → LaTeX"). Run the **MB/MC + one-idea-per-slide
pass** before rendering.

### 3.5 Render
```bash
cd slides/<chNN> && /Users/carlosmendez/opt/bin/quarto render slides.qmd
```
→ `index.html` + `slides_files/`. On failure, apply the **render-and-fix loop (max 3 attempts)**
from [`references/render-and-fix.md`](references/render-and-fix.md), then re-render. Confirm
`index.html` exists (> 30 KB) and no `{{…}}` marker remains.

---

## Phase 4: Verification (skip if `--no-verify`)

Run [`references/verification-checklist.md`](references/verification-checklist.md): **Layer 0**
(`quarto render` → `index.html` + `slides_files/`, render-and-fix loop); **Layer A** (local file
checks — `index.html` > 30 KB, `slides_files/` present, every `figures/*.png` resolves, no `{{…}}`);
**Layer B** (the Node static smoke test, incl. the title visual-summary image + figure-path checks);
and **Layer C** — a Playwright browser **math-render check** (`templates/math-check.cjs`) that loads
the deck, traverses every slide, and **fails on raw LaTeX**. Layer C is **mandatory when the deck
has math**: the static layers only see that `$…$` became `<span class="math">`, NOT that it
*renders*. If Playwright/Chrome is unavailable, eyeball the math manually (`$R^2$` must show as R²,
not `R^2`).

---

## Phase 5: Report + follow-ups

Print the `[✓]/[✗]/[~]` report from the checklist, then offer copy-pasteable follow-ups
(never auto-run):
```
NEXT STEPS (copy + paste)
=========================
1. Preview (press M=menu, B=chalkboard, S=speaker view, O=overview):
   open slides/<chNN>/index.html
   # or, if a file:// asset is blocked:
   python3 -m http.server -d slides/<chNN> 8000  &&  open http://localhost:8000/

2. Export a PDF handout (the skill does not build one):
   a) in-browser: open the deck, append ?print-pdf, Print → Save as PDF (landscape, no margins,
      background graphics on)
   b) scriptable — one page per slide, fragments flattened:
      CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
      "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
        --run-all-compositor-stages-before-draw --virtual-time-budget=40000 \
        --print-to-pdf=slides/<chNN>/deck.pdf \
        "file://$PWD/slides/<chNN>/index.html?print-pdf&pdfSeparateFragments=false"

3. Re-render after editing slides.qmd:
   cd slides/<chNN> && /Users/carlosmendez/opt/bin/quarto render slides.qmd

4. Refresh figures after editing the chapter's plots:
   python3 .claude/skills/write-slides/scripts/export_chapter_figures.py <chNN> --source render
   # then re-copy the chosen figures into slides/<chNN>/figures/ and re-render

5. Commit (source + rendered deck):
   git add slides/<chNN>/
   git commit -m "<chNN>: add Quarto reveal.js slide deck

   Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```
If any `[✗]`: surface the failed assertion with its path; suggest the matching `render-and-fix.md`
entry; offer a re-run.

---

## Reference files

- [`references/rhetoric-of-decks.md`](references/rhetoric-of-decks.md) — the ported philosophy
  (Three Laws, audience triad, 3-act arc, assertion titles, pedagogical movement, MB/MC,
  Devil's-Advocate, Beamer→Quarto-revealjs map).
- [`references/slide-archetypes.md`](references/slide-archetypes.md) — the 12 slide layouts as
  copy-paste **Quarto markdown**.
- [`references/interview-questions.md`](references/interview-questions.md) — the **autonomous
  derivation heuristics** that replace each former interview round.
- [`references/quarto-revealjs-guide.md`](references/quarto-revealjs-guide.md) — how the
  `.qmd`+`.scss`+partial compose; the render command; format options; math/code/figure/columns/notes
  mechanics; why not embed-resources.
- [`references/slide-mapping.md`](references/slide-mapping.md) — chapter → arc heuristics;
  figure/table/equation placement; the visual-summary title slide; the figure export + MB/MC pass.
- [`references/verification-checklist.md`](references/verification-checklist.md) — Phase-4 checks +
  report template.
- [`references/render-and-fix.md`](references/render-and-fix.md) — failure-mode catalog.
- `scripts/export_chapter_figures.py` — exports a chapter's figures + visual summary into `_figcache/`.
- `references/templates/` — `slides.qmd.tmpl`, `site-brand.scss`, `title-slide.html`, `smoke-test.js`,
  `math-check.cjs`.

---

## Acceptance tests (for the skill itself)

1. **Reference deck — `ch05`.** Invoke; expect `slides/ch05/{slides.qmd, site-brand.scss,
   title-slide.html, figures/}` written; `quarto render` → `index.html` + `slides_files/`; the title
   slide shows the chapter **visual summary**; the smoke test 100% `[✓]`; the math-check passes.
2. **Figure export.** `export_chapter_figures.py ch05` populates `_figcache/figures_manifest.json`
   and copies PNGs + `visual_summary.png`; the deck references only `figures/*.png` that exist.
3. **Essentials length.** The deck is ~15–22 slides (not a full section-by-section transcript);
   dropped figures (if the cap engaged) are logged.
3b. **Code coverage.** The deck has **≥1 Code slide per main tool** the chapter introduces (≥1
   overall; the smoke test fails a deck with zero code blocks). Each block is self-contained,
   runnable, fully commented, and carries the `↗ Try it in Colab` pill.
4. **`--no-verify`.** Phases 1–3 + 5 run; Phase 4 skipped; minimal file sanity still runs.
5. **Idempotent re-run.** A second run detects `slides/ch05/`, asks before overwriting, reproduces
   byte-identical `site-brand.scss`/`title-slide.html`.
6. **No embed-resources.** `embed-resources: true` is NOT set; the deck ships `index.html` +
   `slides_files/` (chalkboard works).
7. **Takeaway cards.** Substantive content slides end with a `[…]{.takeaway .fragment}` card
   (renders as the DataPink accent card, rises/fades in last); `.comment` is used only for small
   figure/equation glosses.
8. **Dark-brand title slide.** The title slide shows the ElectricCyan accent rule, the centred
   visual-summary image, and the refined byline; dividers are cyan/purple/pink by act.
9. **Standalone.** Nothing in `notebooks_quarto/`, the book, or the website changes; only `slides/`
   is written.
