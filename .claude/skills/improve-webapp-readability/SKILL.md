---
name: improve-webapp-readability
description: Audits and improves the readability and pedagogical scaffolding of a metricsAI chapter web app (web-apps/chNN/template.html). Restructures each widget into a six-part pattern proven on Chapter 2 — Motivation → Key Concept → What you can do here → Controls + Chart → Try-this with reveals → Take-away. Uses the chapter's .qmd as the source of truth for Key Concept wording. Invoke via /improve-webapp-readability chNN [--apply] [--all]. Only touches prose scaffolding and CSS; never touches JavaScript, data, or chart behavior.
argument-hint: [chapter-number] [--apply] [--all]
---

# Improve Web App Readability Skill

Audits and improves the readability and pedagogical scaffolding of an interactive chapter dashboard in `web-apps/chNN/`. Focuses on the prose a beginner reads before, during, and after touching each widget — never the JavaScript, data, or chart rendering.

## Why this skill exists

A chapter web app can be mechanically correct (charts render, sliders work, numbers match the chapter) and still fail pedagogically: beginners do not know which concept a widget teaches, why they should care, or what insight each experiment should reveal. This skill encodes the pattern proven on the Chapter 2 app so every future chapter app teaches with the same rhythm.

## The six-part widget pattern

Every widget in the web app is rewritten to present information in this order. Deviation requires a deliberate reason.

1. **Heading** — widget title (existing `<h2>`).
2. **Motivation** (`.motivation`) — one or two short, question-framed sentences on *why the tool matters*. Pink accent. Comes before any math.
3. **Key Concept callout** (`.key-concept`) — purple-bordered box containing the concept body, using wording adapted from the chapter's own Key Concept callout. Opens with a **bolded first sentence** that states the concept in plain English.
4. **What you can do here** (`.widget-howto`) — a small heading plus 2–4 plain-language bullets describing each control. Bold the action, then explain.
5. **Controls + chart** — unchanged. The existing `.controls`, `.chart`, `.stats-grid`, `.delta-row`, `.callout`, etc. stay exactly as they are.
6. **Try-this with reveals** (`.try-this`) — existing block, but every `<li>` is rewritten to bold the action and end with an *insight sentence* (not a question). A Try-this step without a reveal is not finished.
7. **Take-away** (`.takeaway`) — single-sentence footer plus an arrow link back to the chapter's corresponding `.qmd` section.

A global `.howto-card` intro at the top of `<main>` and a closing "Keep learning" card at the bottom are optional. The Chapter 2 history showed them to be skippable — include only if the user asks.

## When to use

Invoke with `/improve-webapp-readability chNN` (e.g. `/improve-webapp-readability ch05`) when:

- A chapter web app has been scaffolded by the `web-app` skill but the prose is dense or technique-first.
- A chapter's `.qmd` Key Concepts were updated and the web app needs to re-sync its callouts.
- You want to apply the Chapter 2 convention to any new or legacy chapter dashboard.

Do not invoke this skill to add new widgets, change chart behavior, or edit chapter notebooks. Those are out of scope.

## Non-negotiables

**What this skill WILL change (prose scaffolding only):**

- Lede prose around each widget.
- CSS classes: `.motivation`, `.key-concept`, `.widget-howto`, `.takeaway`.
- Redundant header badges (`section-tag`, `kc-label`) inside widgets.
- Global intro / closing card (only if requested).

**What this skill WILL NOT change:**

- JavaScript, event handlers, chart rendering, URL-hash state.
- The data JSON, `build.py`, or any computed numbers.
- The light/dark theme system or brand palette.
- The number of widgets or their interactive behavior.
- Any file outside `web-apps/chNN/`.
- Any chapter `.qmd` file (it is the source of truth, read-only here).
- **Never inject MathJax, KaTeX, or any math engine.** The web apps are standalone single-file dashboards that do not load a math renderer. All math must be expressed with HTML entities and tags (see "Math and symbols" below).

## Inputs this skill needs

Before editing, collect:

1. **The chapter `.qmd`** — `notebooks_quarto/chNN_*.qmd`. Source of truth for Key Concept wording and section anchors.
2. **The web app template** — `web-apps/chNN/template.html`. The file you edit.
3. **The build script** — `web-apps/chNN/build.py`. Run it to regenerate `dashboard.html` after edits.

If any of these three is missing, stop and report — do not invent.

## Workflow

Follow these phases in order.

### Phase 1 — Read the chapter's Key Concepts

Grep the chapter `.qmd` for `> **Key Concept N.M:` (the Quarto blockquote convention used across metricsAI). For each match, capture:

- The Key Concept ID (e.g. `2.1`) and title (e.g. `Summary Statistics`).
- The body text (usually 1–3 sentences immediately following the title inside the blockquote).
- The section anchor the chapter Quarto build will produce (convert the nearest `##` heading to its kebab-case slug).

This list becomes the **Key Concept source of truth** — the web app must not invent wording that contradicts the chapter.

### Phase 2 — Inventory the web app

Read `web-apps/chNN/template.html` top to bottom. Build a short table, one row per `<section class="widget">`:

| Widget id | Title | Key Concept cited | Has `.motivation`? | Has `.key-concept`? | Has `.widget-howto`? | Has `.takeaway`? | Has redundant `.section-tag`/`.kc-label`? | Try-this reveals? |
|---|---|---|---|---|---|---|---|---|

For the "Try-this reveals" column, a widget passes if **every** `<li>` under `.try-this` ends with a sentence stating what the student should notice (not a bare directive or open-ended question).

### Phase 3 — Audit and score

Each widget can earn up to 100 points. Deduct:

| Gap | Deduction |
|---|---|
| Missing `.motivation` (no why-this-matters opener) | -15 |
| Missing `.key-concept` callout, or callout wording contradicts the .qmd | -20 |
| Missing `.widget-howto` bullets | -10 |
| Missing `.takeaway` + chapter link | -10 |
| Any Try-this `<li>` without a reveal sentence | -4 each (cap -20) |
| Redundant header badge (`.section-tag` or `.kc-label`) | -3 each |
| Lede sentence > 25 words (per offender) | -2 each (cap -10) |
| Passive / formula-first opener instead of beginner-friendly motivation | -5 |
| Prose contradicts the chapter's numerical example | -15 (hard flag) |
| Missing a Reset button where the widget has interactive controls | -5 |
| Raw LaTeX in prose (`$x$`, `$\bar{X}$`, `\sqrt{n}`, etc.) that no math engine will render | -5 per offending widget (cap -15) |

Global deductions (applied once to the whole app):

- No global "How to read" card AND app is ≥ 6 widgets — -0 (optional). Skip unless the user asks.
- CSS classes missing — -0 here; will be added in Phase 5 automatically.

**Tiers:**

- **90–100:** Excellent — matches the Chapter 2 convention.
- **75–89:** Good — a few gaps to close.
- **60–74:** Uneven — several widgets lack scaffolding.
- **< 60:** Needs a full rewrite — invoke with `--apply`.

### Phase 4 — Report

Output a Markdown report with three blocks:

1. **Summary table** — widget id · title · score · top gap.
2. **HIGH priority** per widget, with line numbers and concrete rewrites. Include at least one proposed motivation sentence and one take-away sentence per widget.
3. **Auto-fixable vs. requires-judgment** — split findings into the two buckets described below.

### Phase 5 — Apply (if `--apply`)

Perform the mechanical rewrites **first**, then propose stubs for the judgment calls.

**Auto-fixable (do it):**

- Insert the four CSS classes from `references/WIDGET_STRUCTURE.md` if they are missing from the `<style>` block. Idempotent — check before inserting.
- Delete `<span class="section-tag">…</span>` lines inside widget headers.
- Delete `<span class="kc-label">…</span>` lines inside `.key-concept` boxes.
- Delete the `.section-tag` and `.kc-label` CSS rules once the spans are gone.
- For each widget, if `.key-concept` is missing, insert a scaffolded callout populated from the chapter's `.qmd` Key Concept body (wording copied, lightly tightened — never invented).
- For each widget, if `.widget-howto` is missing, generate bullets by scanning `.controls > .ctrl > label` and rewriting each label as a plain-language sentence ("**Slide the bin width** from narrow to wide.").
- For each widget, if `.takeaway` is missing, insert a stub `<p class="takeaway"><strong>Take-away:</strong> …<a href="…chapter anchor…">Read §N.M in the chapter →</a></p>`. Mark the body with `⚠ TODO` so the author sees it.
- **Scan for raw LaTeX in prose** (inline `$...$`, display `$$...$$`, or backslash commands like `\bar`, `\mu`, `\sigma`, `\sqrt`, `\cdots`, `\hat`) in the widget-facing prose — motivation, key-concept, widget-howto, callouts, try-this, take-away. Convert to the HTML entities in `references/WIDGET_STRUCTURE.md` → "Math and symbols" (e.g. `$\bar{X}$` → `X&#772;`, `$\sigma/\sqrt{n}$` → `&sigma;/&radic;n`, `$x$` → `<em>x</em>`). Never inject `<script>` tags for MathJax or KaTeX. Ignore `$` inside JS template literals, data values, and HTML option labels (e.g. `$100k`, `${reg.slope}`) — those are not math.

**Requires-judgment (propose, do not force):**

- **Motivation sentences** — pink-accent `.motivation` paragraph. These need pedagogy. Suggest one candidate per widget using a question frame ("Is $100k a lot? Compared to what?") — but flag them `⚠ REVIEW` so the author accepts, edits, or replaces.
- **Try-this reveals** — rewrite each `<li>` to bold the action and end with a reveal sentence. Propose rewrites; do not overwrite unless the current text is a bare directive with no insight.
- **Contradictions with the `.qmd`** — if the web app states a number, claim, or interpretation that the chapter contradicts, flag HIGH and stop. Do not silently "fix" numbers.

After applying, rebuild and verify:

```bash
python3 web-apps/chNN/build.py
python3 .claude/skills/web-app/scripts/verify_app.py web-apps/chNN/dashboard.html
```

Both must pass. If either fails, roll back the offending edit and report.

### Phase 6 — Report what changed

After `--apply`, print a diff-style summary:

- CSS classes added / removed.
- Widgets that received `.motivation`, `.key-concept`, `.widget-howto`, `.takeaway`.
- Widgets whose Try-this was rewritten.
- `⚠ REVIEW` / `⚠ TODO` markers that still need human attention.
- Build + verifier results.

Tell the user explicitly which items still need their judgment. Do not mark the task complete until the author has reviewed the `⚠` items.

## Batch mode (`--all`)

Audit every chapter with a web app (scan `web-apps/ch*/template.html`). Produce one summary table, one row per chapter, with columns: widgets · score · top gap. Do **not** apply fixes in batch mode — only report. The author chooses which chapters to rewrite individually.

## Conventions for prose you write

Follow these when drafting motivation, key-concept, how-to, try-this, or take-away text:

- **Short sentences.** Aim for 12–18 words. If you have to use a comma to glue two clauses, consider two sentences.
- **Plain vocabulary first, jargon second.** "Typical value" → then "(the median)". "Spread" → then "(standard deviation)".
- **Question-framed motivations.** "Is X rare? Compared to what?" beats "Standardization expresses…".
- **Bold the action** in Try-this bullets: `<strong>Slide to the narrowest bin.</strong>` — then the reveal.
- **Italicise the reveal noun** for emphasis: `<em>That is what "robust to outliers" means.</em>`
- **Use the chapter's own language** inside `.key-concept`. Do not paraphrase away precision.
- **One take-away per widget.** Not two sentences. Not a paragraph. One clean sentence plus the chapter link.
- **No emojis.** The brand palette + typography carries the tone.
- **No new colors.** Use `--cyan`, `--purple`, `--pink`, `--panel`, `--text`, `--text-soft`, `--text-muted`, `--border` only.
- **Math: never raw LaTeX in prose.** The web apps do not load MathJax or KaTeX — `$x$` renders as the three characters `$`, `x`, `$`; `$\bar{X}$` renders as the eight characters of its source. Use HTML entities and tags instead (full lookup in `references/WIDGET_STRUCTURE.md` → "Math and symbols"): `&mu;`, `&sigma;`, `&radic;n`, `&Sigma;`, `X&#772;` for X̄, `<em>x</em>` / `<em>y</em>` for italic variable names, `<sub>i</sub>` for subscripts, `&#x22EF;` for midline ellipsis (⋯). Chapter 2's app is the reference — grep `web-apps/ch02/template.html` for any symbol you're unsure about. The only place `$` is allowed in prose is when it means a literal dollar sign (e.g. `$73.77/sq ft`).

## Reference files

- `references/WIDGET_STRUCTURE.md` — the six-part HTML skeleton + the four CSS classes, copy-pasteable.
- `references/BEFORE_AFTER_EXAMPLES.md` — real before/after rewrites from the Chapter 2 pass (summary stats, Z-score, log transform).
- `.claude/skills/web-app/SKILL.md` — the upstream skill that scaffolded the web app in the first place.
- `.claude/skills/improve-readability/SKILL.md` — the sibling skill that improves chapter notebooks.

## Relationship to other skills

```
/web-app chNN                          (scaffold the dashboard)
      ↓
/improve-webapp-readability chNN       (this skill — rewrite scaffolding prose)
      ↓
manual review of ⚠ REVIEW / ⚠ TODO markers
      ↓
/improve-webapp-readability chNN       (re-audit, target score ≥ 90)
```

The chapter `.qmd` is upstream of all web-app work. If the chapter's Key Concept wording is wrong, fix it in the `.qmd` first (via `/improve-readability chNN`), then re-run this skill to re-sync the web app.

---

**Version:** 1.1
**Created:** 2026-04-17
**Updated:** 2026-04-17 — Added math-rendering convention. Web apps do not load MathJax/KaTeX, so the skill now bans raw LaTeX `$...$` in prose, scores it in Phase 3, auto-converts common tokens to HTML entities in Phase 5, and documents the full entity lookup in `references/WIDGET_STRUCTURE.md`.
**Prerequisite:** Web app exists (`web-apps/chNN/template.html` + `build.py`). Chapter Key Concepts defined in the `.qmd`.
**Audience:** Beginner econometrics students.
