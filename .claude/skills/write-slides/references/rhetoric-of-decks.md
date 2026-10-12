# The Rhetoric of Decks (ported to HTML)

This is the *substance* `write-slides` carries over from Scott Cunningham's
`beautiful_deck` skill. The upstream skill compiles Beamer/LaTeX; we render
reveal.js HTML instead. **The format is the medium; the rhetoric is the
substance.** Every principle below is format-independent — only the mechanics
(§ "Beamer → Quarto revealjs" at the end) change.

Read this in Phase 1 (to shape the proposed arc) and Phase 3 (while writing each
slide). It governs *what goes on a slide and why*; `slide-mapping.md` governs the
*post → slide* transformation; `slide-archetypes.md` gives the HTML.

---

## The Three Laws

1. **Beauty is function.** A slide is beautiful when every element earns its
   presence: the eye knows where to go and the mind grasps the idea instantly.
   Decoration without function is noise. The most beautiful slide is often three
   words on white space.
2. **Cognitive load is the enemy.** **One idea per slide** (two only for an
   inseparable contrast). If you need the word "also," you need a new slide. Test:
   can you state the slide's point in one sentence? If it takes two, split it.
3. **The slide serves the spoken word.** A slide is a *visual anchor* for speech,
   not a document to be read aloud. If the deck is fully self-explanatory without a
   speaker, you've written a paper, not a talk — push the prose into speaker notes
   (`<aside class="notes">`, press **S**).

---

## The Aristotelian triad — and audience triage

Every deck balances three appeals; the mix is set by the **audience**. For metricsAI
chapter decks the audience is always **Teaching** (students) — the other rows below are
retained as reference for the rhetorical trade-offs, not as a choice the skill makes:

- **Ethos (credibility):** methodology, acknowledged limitations, the Devil's-
  Advocate slide, honest scorecards. *Why trust this?*
- **Pathos (emotion):** the opening hook, the stakes, human impact. *Why care?*
- **Logos (logic):** figures, tables, equations, the chain of reasoning. *Does it
  hold up?*

| Audience | Logos | Ethos | Pathos | Deck implications |
|---|---|---|---|---|
| **Teaching** (students) — *default for tutorials* | 45% | 20% | 35% | Clarity > compression; slow build; worked intuition before formalism; recap slides allowed; an Agenda slide is fine. ~16–22 slides. |
| **Seminar** (peers) | 50% | 40% | 10% | Sparse, performative; identification/method early; one coefficient at a time; **Devil's-Advocate required**. ~20–30 slides. |
| **Conference** (~15–20 min) | 50% | 35% | 15% | Ruthless one-idea-per-slide; headline result by slide ~2; no lit review; figure-first. ~10–14 slides. |
| **Working / External** (collaborators, policy, general) | 30–60% | 25–30% | 15–45% | Define jargon; lead with the picture; document choices; minimal derivation. Devil's-Advocate when collaborators. ~16–22 slides. |

The Teaching profile sets the slide count (~15–22, essentials only), the MB/MC threshold
(below), and which archetypes are foregrounded (figure-first, intuition before formalism,
an Agenda slide is fine, Devil's-Advocate offered for the "association ≠ causation" caveat).

---

## The narrative arc (three acts)

Titles read in sequence must tell a coherent story. Structure every deck as:

- **Act I — Tension (2–4 slides).** Title → a hook (a provocative question,
  surprising statistic, or concrete problem — **never** an agenda or a definition)
  → the stakes. Pathos lives here. The post's "spoiler" figure often belongs here.
- **Act II — Investigation (60–75% of the deck).** The method and evidence.
  Identification/approach early; one idea per slide; alternate dense slides with
  lighter ones so the deck *breathes*. A Devil's-Advocate slide near the end.
- **Act III — Resolution (2–4 slides).** The headline result (a claim + one figure
  or one number) → implications → a **closing slide that is one declarative
  sentence** (the thesis), never "Questions?" or "Thank you."

Each act opens with a full-bleed **divider** slide (brand colour) so the audience
feels the structure.

---

## Titles are assertions

A title is a claim the slide proves, not a label for a topic. Read the titles
alone — they should be the talk's abstract.

| Weak (label) | Strong (assertion) |
|---|---|
| "Results" | "Rigorous Double-LASSO restores a sensible −0.096" |
| "Identification" | "We exploit the 10% WTO tariff ceiling as a mechanical dose" |
| "Methodology" | "Cross-validation over-selects 150 controls; theory selects 8" |

Forbidden as a slide title: a bare noun ("Data", "Model", "Discussion") or a
figure's name ("Figure 3"). The figure's *finding* is the title; the figure is the
evidence.

---

## The pedagogical movement

Within a teaching/method section, move in ONE direction:

```
Narrative → Application → Picture → Codeblock → Technical
(story)     (example)     (figure)  (code)      (equation/theorem)
```

Intuition is the content; the technical statement is what the audience *walks away
with*, not what they walk in on. The anti-pattern is the lecture that opens with a
definition, proves a theorem, and offers an example "for intuition" at the end —
that treats the formalism as primary and the intuition as decorative. Invert it.

---

## MB/MC equivalence (the pacing pass)

After drafting, walk every slide (and every fragment) and rate its **marginal
benefit** (audience understanding gained) against its **marginal cost** (time and
attention spent). A well-paced deck holds MB/MC roughly equal across slides.

- **Overloaded** (MB/MC too low — competing ideas, a wall of text, three data
  series): split or simplify.
- **Underloaded** (MB/MC too high — one word where a sentence belongs, or a slide
  the audience already inferred): merge or cut.

Concrete caps (tighten for conference, relax for teaching): ≤ 5 bullets/slide; no
slide needs > 4 fragment advances; proofs/derivations the audience won't follow on
sight go to speaker notes. Deliberate "jump scares" (one dense table or provocative
claim for rhetorical effect) are allowed — one or two per deck, on purpose.

---

## White space and the wall of sentences

White space is confidence; crowded slides signal anxiety. **No wall of sentences** —
multiple prose sentences stacked vertically belong in a paper. Acceptable text on a
slide: a labeled setup ("From the FOC:"), a single concluding line, or *structured*
content (a short list, a table, a labeled contrast). Everything else → speaker notes.

---

## The Devil's-Advocate slide

One slide that states the strongest objection or misconception (in DataPink) and
answers it (in ElectricCyan). It builds ethos — you've done the hard thinking — and
pre-empts the obvious pushback. For teaching chapters this is the natural home for the
chapter's key caveat. Example: *"A strong correlation means $x$ causes $y$."* → *"Association
is not causation — confounders, reverse causality, and selection can all produce it."*

---

## Beamer → Quarto revealjs (what changes, what doesn't)

The deck is authored as `slides.qmd` and rendered with `quarto render`. The rhetoric is
unchanged; only the mechanics differ.

| Beamer mechanic (upstream) | Quarto-revealjs equivalent (this skill) |
|---|---|
| `\frametitle{...}` | `## Assertion title` (h2, auto-underlined by the theme) |
| `\section` / `\transitionslide` | `# Act Title {.divider background-color="…"}` |
| `\onslide` / `\pause` | `. . .`, `::: {.incremental}`, `{.fragment}`, `code-line-numbers="2|5"` |
| `\includegraphics{fig.pdf}` | `![caption](figures/<cache_file>.png)` (auto-stretch bounds it) |
| `booktabs` table | a markdown table (theme-styled; `[cell]{.key}` highlights the headline) |
| `lstlisting` code block | ` ``` {.r code-line-numbers="…"} ` (highlighted, not executed) |
| LaTeX math | plain `$…$` / `$$…$$` (Pandoc + MathJax) |
| Beamer notes | `::: {.notes}` (press **S** for speaker view) |
| `pdflatex` zero-warning compile loop | `quarto render` + local file checks + Node smoke test + browser math-check |
| `/tikz`, `referee2`, graphics audit sub-agents | not ported (Beamer/LaTeX-specific) |
| original theme per deck | **fixed metricsAI dark brand** (`site-brand.scss`, never per-deck) |
| Beamer PDF output | reveal.js HTML (menu/chalkboard/speaker view); manual `?print-pdf` for a handout |

**Escaping note.** A `.qmd` is **Pandoc, not Goldmark** — write **plain LaTeX** (single
backslashes, raw underscores, `$5` for currency, e.g. `$\hat\beta_j$`, `$\|y-X\beta\|_2^2$`) and
**drop** any `index.md` Goldmark escaping when porting an equation. The full conversion table is
the canonical `slide-mapping.md §Porting equations`; MathJax's macro set still applies
(`render-and-fix.md §7`).

---

## The one-line test for every slide

Before finalising a slide, confirm: **one idea**, **an assertion title**, **one
load-bearing visual** (figure / equation / table / number / code), and **the rest is
speaker notes**. If two of those fight for the slide, make two slides.
