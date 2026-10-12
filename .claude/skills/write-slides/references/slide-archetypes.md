# Slide archetypes (Quarto markdown)

The 12 slide layouts a deck is built from, expressed as **Quarto markdown** (the deck is
authored as `slides.qmd` and rendered with `quarto render`). Each entry is a copy-paste
skeleton — substitute the ALL-CAPS placeholders. Read this in Phase 3 while writing the
`.qmd` body. The visual styling lives in `site-brand.scss`; the engine config lives in the
`.qmd` front matter (see `slides.qmd.tmpl`).

Conventions:

- `##` (h2) = a **content slide**; its heading is the **assertion title** (auto-underlined
  ElectricCyan by the theme). `#` (h1) = a **section/divider slide**.
- `center: true` (front matter) vertically centers every slide — dividers land in the middle,
  content blocks use the white space.
- Speaker notes: `::: {.notes} … :::` (press **S**). Fill from the chapter's explanatory prose.
- Reveal one step at a time: `. . .` (a pause between blocks), `::: {.incremental}` (a list),
  or `{.fragment}` on a span/element.
- Figures use a local bundle path: `![caption](figures/<cache_file>)` — the PNGs are copied into
  `slides/chNN/figures/` from `_figcache/` (see `slide-mapping.md § Figures`).
- **Math: write LaTeX, never literal Unicode** (`R² → $R^2$`, `α̂ → $\hat\alpha$`, `± → $\pm$`). The
  full rules — the Unicode→LaTeX table, **mixed numbers** (keep `[…]{.key}`/`[…]{.bignum}` as styled
  text), and **notes stay Unicode** — are the canonical `slide-mapping.md §Math symbols → LaTeX`.

---

## 1. Title — front matter only (no body slide)

The title slide is the **chapter visual summary, full-bleed, and nothing else** — no title,
subtitle, or byline text on it. The custom `title-slide.html` partial paints the visual summary as
the slide's **background image** (`data-background-image`, `size=contain`), so the *whole* summary
shows with no cropping and fills the slide edge-to-edge (the summaries are 16:9, matching the
1280×720 canvas). Fill the front matter:

```yaml
title: "5. Bivariate Data Summary"            # used for the browser tab / metadata, not shown on the title slide
subtitle: "How two variables move together — and what that does (and doesn't) tell us"
deck-author: "Carlos Mendez"                   # retained for metadata (not rendered on the title slide)
deck-author-url: "https://carlos-mendez.org"
institute: "Nagoya University (GSID)"
date: today
date-format: long
visual-summary: "figures/visual_summary.png"   # the chapter's visual summary — the ENTIRE title slide
```

**Use:** always. No `#`/`##` for it — it is the rendered title slide. (`deck-author` /
`deck-author-url` / `visual-summary` are custom fields the partial reads.)

**Behaviour.** With `visual-summary:` set, the partial renders a single empty `<section>` whose
background *is* the image — no overlaid text. Clicking it opens the same **click-to-zoom** overlay as
the body figures (full-screen + zoom/pan controls, from `figure-zoom.html`). If a deck has **no**
`visual-summary`, the partial falls back to a text title slide (title + ElectricCyan accent rule + subtitle + hyperlinked author +
institute + date); both paths live in `title-slide.html` / `site-brand.scss`.

---

## 2. Agenda (optional)

```markdown
## Where we're going

::: {.incremental}
- ROADMAP ITEM 1
- ROADMAP ITEM 2
- ROADMAP ITEM 3
:::
```

**Use:** teaching decks > ~15 slides. Build directly from the chapter's **"What you'll learn"** bullets.

---

## 3. Section divider

```markdown
# ACT TITLE {.divider background-color="#008CB7"}

[Act I]{.act}
```

**Use:** one before each act. Per-act colour: **Act I → `#008CB7`** (ElectricCyan), **Act II →
`#7A209F`** (SynapsePurple), **Act III → `#C21E72`** (DataPink). The `.divider` class gives white
centred text; `center: true` puts it in the middle of the slide.

---

## 4. Narrative / Hook

```markdown
## ONE-SENTENCE PROVOCATION OR STAKE

A single concrete line — a named dataset, question, or tension.

. . .

The turn or the question that opens the investigation. *Italic for emphasis.*

::: {.notes}
The story you tell aloud; the slide only anchors it.
:::
```

**Use:** open Act I (and to re-engage mid-Act II). Minimal text, high pathos. For a chapter, the hook
is the motivating example (e.g. "Do bigger houses really sell for more — and by how much?").

---

## 5. Figure slide

```markdown
## WHAT THE FIGURE SHOWS, AS A CLAIM

![One-line reading aid — never "Figure 3".](figures/fig_5-3_01.png)

::: {.notes}
Walk the audience through what to look at first.
:::
```

**Use:** the deck's backbone — figure-first. Quarto's **`auto-stretch`** (on by default) bounds the
image to the slide and `fig-align: center` centres it — no overflow, no manual sizing. One figure,
one message. The alt/caption is the reading aid; the `##` is the finding. Figures come from the
`figures/` bundle (see `slide-mapping.md § Figures`). Every figure is **click-to-zoom** automatically
(full-screen overlay + zoom/pan controls, from `figure-zoom.html`) — no per-figure markup needed.

---

## 6. Table slide

```markdown
## WHAT THE TABLE PROVES

| Variable | Mean | Std. dev. |
|---|---:|---:|
| Price ($) | [265{,}000]{.key} | 38{,}000 |
| Size (sq ft) | 1{,}910 | 410 |

[One-line takeaway under the table.]{.takeaway .fragment}
```

**Use:** where a summary-statistics or results table lands the point. Trim to the 2–3 load-bearing
columns; tag the headline cell `[…]{.key}` (renders DataPink). The theme styles it booktabs-ish (no
vertical rules, ElectricCyan head rule). Close with the takeaway card (component below).

---

## 7. Code slide

```markdown
## WHAT THESE LINES DO, IN ONE CLAIM

``` {.python code-line-numbers="1|3-4|6-8|10-11"}
!pip install -q pyfixest                   # install pyfixest in Colab (-q = quiet; not preinstalled)

import pandas as pd                         # pandas → load & handle tabular data
import pyfixest as pf                        # pyfixest → fast OLS regression + tidy output

# dataset: 29 house sales in Davis, CA (price, size, …)
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA"
houses = pd.read_stata(url)                 # read the Stata .dta file into a DataFrame

m = pf.feols("price ~ size", data=houses)   # fit OLS: regress price on size
m.summary()                                 # report intercept b1, slope b2, SEs, R²
```

[↗ Try it in Colab](https://colab.research.google.com/notebooks/empty.ipynb){.colab-link target="_blank" data-preview-link="false"}

::: {.notes}
Self-contained — paste it into the empty Colab notebook and it runs end to end.
:::
```

**Use:** when the deck teaches code. `{.python}` highlights **without executing** (the deck has no
kernel); `code-line-numbers="a|b|c"` reveals groups as fragments. **Make the block self-contained
and runnable** — lead with a quiet install of any package Colab lacks
(`!pip install -q pyfixest` — pyfixest/wooldridge/etc. aren't preinstalled; pandas/numpy/statsmodels
are), then the imports *and the data load* (use the chapter's own
`pd.read_stata(GITHUB_DATA_URL + '…')` / `pd.read_csv(...)` line, with the full URL inlined) so a
reader can paste it into an empty Colab cell and reproduce the result — don't assume a `houses`
variable already exists. Keep ≤ ~10 lines; if a full listing would overflow, show the load +
headline call here and push extra detail to the notes. **Comment every line pedagogically** — a
short trailing `#` note saying what that line does (what each import is *for*, what the data-load
reads, what the model call fits, what the output reports) so a learner can follow the block without
the chapter open. For a long line (e.g. a data URL), put its comment on the line *above* it to avoid
horizontal overflow.

**Always add the Colab link** on its own line right below the code fence — the branded `.colab-link`
pill to the empty-notebook URL, so a reader can open a scratch notebook and paste the block:

```markdown
[↗ Try it in Colab](https://colab.research.google.com/notebooks/empty.ipynb){.colab-link target="_blank" data-preview-link="false"}
```

`target="_blank"` opens it in a new tab; `data-preview-link="false"` stops reveal's inline
link-preview from intercepting the click.

---

## 8. Equation slide

```markdown
## WHAT THE EQUATION SAYS, IN WORDS

$$\hat{y} = b_1 + b_2 x$$

[The fitted line predicts $y$ from $x$: $b_1$ is the intercept, $b_2$ the slope — the predicted
change in $y$ per one-unit change in $x$.]{.comment}
```

**Use:** one equation per slide with a plain-language gloss (`.comment`, small/centred — it
*explains* the equation). If the closing line is instead the slide's **concluding takeaway** (not a
gloss of the math), use `[…]{.takeaway .fragment}` (component below). Plain LaTeX — Pandoc/MathJax
render it.

---

## 9. Two-column compare

```markdown
## A VS B — THE LOAD-BEARING CONTRAST

:::: {.columns}
::: {.column width="50%"}
### CORRELATION
- unit-free, in $[-1, 1]$
- symmetric in $x$ and $y$
:::
::: {.column width="50%"}
### COVARIANCE
- carries the units of $x \times y$
- sign only, scale not comparable
:::
::::
```

**Use:** the one place two ideas may share a slide — an *inseparable* contrast (correlation vs
covariance; association vs causation). Column `###` headers get a SynapsePurple underline.

---

## 10. Devil's-Advocate

```markdown
## The tempting mistake — and the correction

[Objection.]{.objection} A STRONG CORRELATION MEANS $x$ CAUSES $y$.

. . .

[Response.]{.rebuttal} ASSOCIATION IS NOT CAUSATION — CONFOUNDERS, REVERSE CAUSALITY, AND SELECTION
CAN ALL PRODUCE IT.
```

**Use:** late Act II / early Act III — ideal for the "association ≠ causation" caveat every
data-summary chapter carries. Steelman the misconception (DataPink), then correct it (ElectricCyan).

---

## 11. Headline-result (optional for teaching chapters)

```markdown
## THE RESULT, AS A SENTENCE {background-color="#7A209F"}

[+61.5]{.bignum}

[dollars of predicted price per extra square foot (OLS slope $b_2$)]{.bignum-label}
```

**Use:** only when the chapter *does* have one memorable number worth a full-bleed slide. One giant
number + one line on a full-bleed SynapsePurple slide that lifts off the dark canvas
(`has-dark-background` keeps text light; the theme makes `.bignum` bright pink there). Many teaching
chapters have no single headline number — skip this archetype then.

---

## 12. Closing

```markdown
# THE ONE SENTENCE YOU WANT THEM TO REMEMBER. {.divider background-color="#C21E72"}
```

**Use:** always, the final slide. A declarative thesis (the resolution of the Act-I hook) as a
centred `#` section slide on a full-bleed brand colour (DataPink, or ElectricCyan to bookend an
Act-I cyan divider). **Never** "Questions?", "Thank you", or a contact list.

---

## Takeaway card — the concluding line of a content slide

Not a full archetype — a **component** most content slides (Narrative, Figure, Table) should end
with: the slide's assertion restated as one memorable sentence, rendered as a prominent brand
**accent card** (soft DataPink fill, bold pink left bar, larger semibold text) that **rises + fades
in** as the final fragment.

```markdown
[One-sentence takeaway — the point, stated so it sticks.]{.takeaway .fragment}
```

- **`.takeaway` vs `.comment`.** `.takeaway` is the prominent card — the slide's conclusion.
  `.comment` stays the small grey caption/gloss that *explains* a figure/table/equation. Don't swap
  them: a takeaway is a claim you want remembered; a gloss is a reading aid.
- **Always a `.fragment`** so it lands last, after the evidence above it. It counts as one fragment
  advance (keep the slide's total ≤ ~4).
- Sits on content slides (never on a `.divider`); the styling lives in `site-brand.scss`.
- This is the per-slide takeaway — distinct from the single **Closing** divider (archetype 12),
  which is the deck's one final thesis.

---

## Assembly notes

- Order follows the derived Phase-2 outline: front-matter title → Act I divider → … → Closing. The
  auto title slide is first; the body starts at the Act I `#` divider.
- Prefer ending each substantive content slide with a `[…]{.takeaway .fragment}` — the assertion
  title states the claim; the takeaway card restates it as the memorable line.
- Prefer horizontal slides; use a vertical sub-stack only when one idea genuinely needs sub-steps
  (Quarto: nest with `##` under a `#`, or use `. . .`).
- Every content slide gets a `##` assertion; only the title, dividers, and closing use `#` or the
  front matter.
- Put `::: {.notes}` on any slide whose spoken content exceeds what's shown — most of them.
