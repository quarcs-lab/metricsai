# Autonomous derivation heuristics (Phase 2)

> **This skill is autonomous — there is no interview.** The upstream `beautiful_deck` skill asked
> the user to confirm audience, takeaways, headline numbers, and the outline via `AskUserQuestion`
> rounds. For metricsAI chapter decks the skill derives all of that from the chapter itself and
> builds the deck in one pass (the user reviews the rendered result). This file documents the
> heuristics that *replace* each interview round. **Do not call `AskUserQuestion`** in this skill.

The old rounds map to automatic decisions as follows.

---

## Round 1 → Audience is always **Teaching**

metricsAI chapters are a textbook. The audience is always students. This fixes the rhetorical
balance (clarity > compression, intuition before formalism, an Agenda slide is fine), the slide
count (**~15–22, essentials only**), and the MB/MC threshold — see `rhetoric-of-decks.md` § audience
table (Teaching row). No choice to make.

---

## Round 2 → Takeaways + key visual, derived from the chapter

- **Takeaways** ← the chapter's **"What you'll learn"** bullets (in Chapter Overview) and the
  **Key Takeaways** section. These seed both the Act-III assertion titles **and** the per-slide
  `.takeaway` cards (the DataPink accent card each content slide ends on; see `slide-archetypes.md`).
- **Key concepts** ← the chapter's bold **Key Concept** terms + the "Key Concepts" section → the
  Agenda and the one or two concept slides.
- **Title key visual** ← the chapter's **visual-summary image** (no numeric headline strip). The
  exporter copies it to `figures/visual_summary.png`; set it in the front-matter `visual-summary:`
  field. Teaching chapters rarely have a single headline number, so the optional Headline-result
  slide (archetype 11) is used only when one genuinely exists.

Never invent results — read assertions and numbers from the chapter's prose, tables, and figures.

---

## Round 3 → Outline, derived from the chapter's sections

Build the 3-act arc automatically from the chapter structure (see `slide-mapping.md § Chapter
element → slide → act`):

```
Title (visual summary)
Act I  · Divider              — the hook / motivating question
  Hook                        — the motivating example
  Agenda                      — from "What you'll learn"
  Key Concepts                — the chapter's bold terms
Act II · Divider              — the investigation
  one slide per CORE section  — figure / equation / table / code, assertion-titled
  (fold "Illustration:" / "Special case:" subsections into the parent or into notes)
Act III· Divider              — the resolution
  Devil's-Advocate            — the chapter's key caveat (e.g. association ≠ causation)
  Headline-result (optional)  — only if one memorable number exists
  Key Takeaways               — restated as assertions
  Closing                     — one declarative thesis sentence
```

Keep it to ~15–22 slides: **one slide per core section**, skip Setup / code-summary / Practice
Exercises / Case Studies. If the draft exceeds ~22, drop the least load-bearing figures and merge
thin narrative slides (log any dropped figure in the Phase-5 report). Run the MB/MC pass
(`slide-mapping.md`) before rendering.

---

## Round 4 → Devil's-Advocate is default-on for the chapter's caveat

Every data-analysis chapter carries a caveat worth a Devil's-Advocate slide — most often
**"association ≠ causation"**, but also "correlation misses nonlinearity", "R² isn't everything",
"extrapolation beyond the data is risky". Include one, steelmanning the common misconception
(DataPink) and correcting it (ElectricCyan). There is no button-collision question (the deck is a
standalone `slides/chNN/` artifact; nothing to collide with).

---

## No confirmation gate

The skill writes, renders, and verifies without waiting for a `y`. The user reviews the rendered
deck (`open slides/chNN/index.html`) and requests changes afterward. Report what was built,
including any figures dropped by the cap and any `[~]` verification warnings.
