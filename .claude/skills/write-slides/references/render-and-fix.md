# Render-and-fix catalog

Failure modes for `write-slides` (Quarto revealjs), each with symptom → cause → fix. Apply the
**render-and-fix loop** (max 3 attempts) on a `quarto render` failure. Grows over time — append
new modes with the symptom quoted from the error.

---

## 1. Chalkboard incompatible with self-contained output  (the headline gotcha)

**Symptom.** `quarto render` errors: `Reveal plugin 'RevealChalkboard is not compatible with
self-contained output`.

**Cause.** `embed-resources: true` (self-contained single file) cannot bundle the chalkboard
plugin's assets.

**Fix.** Do **not** use `embed-resources: true`. The deck ships `index.html` + `slides_files/`
(the default). The template already omits `embed-resources`. Only enable it if a deck drops
chalkboard.

---

## 2. SCSS theme compile error

**Symptom.** `quarto render` fails in Dart Sass (e.g. "Undefined variable `$primary`", or a
bad `lighten()` argument).

**Cause.** A `site-brand.scss` rule references a variable Quarto hasn't defined yet, or a typo.

**Fix.** Keep variable *overrides* in `/*-- scss:defaults --*/` and *rules* in
`/*-- scss:rules --*/`. Use the brand tokens defined at the top of `site-brand.scss`
(`$cyan`/`$purple`/`$pink`/`$cyan-bright`/`$canvas`), not Quarto-internal names. Re-render.

---

## 3. Title slide has no visual summary / partial error

**Symptom.** The title slide shows no image, or render errors on the partial.

**Cause.** `visual-summary:` missing/malformed in the front matter, the referenced file isn't in
`figures/`, or `title-slide.html` was edited incorrectly. The partial renders
`$if(visual-summary)$<img class="title-visual-summary" src="$visual-summary$">$endif$`.

**Fix.** Ensure the front matter has `visual-summary: "figures/visual_summary.png"` and that the
file exists in the deck's `figures/` dir (the skill copies it from `_figcache/visual_summary.png`).
Keep `title-slide.html` verbatim from `templates/`. If the partial proves brittle, fall back: drop
`template-partials` and place the image as a custom first `## {.center}` slide instead.

---

## 4. Figure not found at render / broken image

**Symptom.** `quarto render` warns "resource not found", or the deck shows a broken image.

**Cause.** The figure wasn't copied from `_figcache/` into the deck's `figures/` dir, or the
filename in `slides.qmd` doesn't match the `cache_file` in the manifest.

**Fix.** Reference the exact file as `figures/<cache_file>.png` and confirm it exists in
`slides/chNN/figures/`. Cross-check against `_figcache/figures_manifest.json`. Re-run
`export_chapter_figures.py chNN` (add `--source render` if the chapter's plots changed since the
last book render), then re-copy the chosen figures.

---

## 5. An equation renders as a MathJax error

**Symptom.** An equation shows a "Math Processing Error" / red text; the static smoke test passed.

**Cause.** A macro MathJax can't process (rare — MathJax's macro set is broad), or a typo.

**Fix.** Correct the macro/typo (`\hat`/`\sum`/`\bar`/`\|…\|`/`\pm`/`R^2` are all fine). Always
eyeball math in a **real browser**, not just the static smoke test (see §7).

---

## 6. Slide overflows / figure too big

**Symptom.** Content spills past the slide.

**Cause.** A figure with `auto-stretch` disabled, or a slide overloaded with content.

**Fix.** Keep `auto-stretch: true` (default) and `fig-align: center` — Quarto bounds the image to
the slide. For text, apply the MB/MC pass (`rhetoric-of-decks.md`): one idea per slide; push
overflow to `::: {.notes}`. The theme caps images at `max-width:100%`.

---

## 7. Math shows as raw LaTeX (`\hat\alpha`) instead of typeset

**Symptom.** Slides display the LaTeX **source** — `\hat\beta \pm 2\,\mathrm{SE}` — not the typeset
math. The static smoke test passed (it only checks that `$…$` became `<span class="math">` spans,
NOT that they actually *render*).

**Cause.** `html-math-method: katex` is **broken in Quarto revealjs**: it emits
`<span class="math inline">\hat\beta</span>` (raw) and loads KaTeX, but adds **no auto-render
call**, so KaTeX is never invoked.

**Fix.** Use the **default MathJax** — do NOT set `html-math-method`. MathJax (the reveal math
plugin) renders `\(…\)` across the whole slide DOM (body, captions, headings, table cells).
**Verify in a real browser** — the static smoke test cannot see unrendered math. See the Playwright
math-render check in `verification-checklist.md` + `templates/math-check.cjs`.

---

## 8. The deck's rendered output must be committed

**Symptom.** After sharing/publishing the repo, the deck renders unstyled/broken — `index.html` or
`slides_files/` is missing.

**Cause.** Only the source (`slides.qmd`) was committed; the rendered output wasn't.

**Fix.** The metricsAI deck is a **standalone, pre-rendered artifact** — nobody renders it
downstream, so the rendered files must be in git. Commit the **whole** `slides/chNN/` dir —
`slides.qmd` + `site-brand.scss` + `title-slide.html` (source), `figures/` (the chosen PNGs +
`visual_summary.png`), **and** `index.html` + `slides_files/` (the served deck). Only the staging
cache and Quarto's local cache are ignored (`slides/*/_figcache/`, `slides/*/.quarto/`). Never add
a `.gitignore` rule that catches `slides_files/`.
