---
name: write-quiz
description: Create the interactive self-assessment quiz for a metricsAI chapter (ch01–ch17). Reads the chapter .qmd (notebooks_quarto/chNN_*.qmd), sizes the quiz with a content-unit formula (sections + inline Key Concepts + learning objectives + glossary terms → 20–40 questions per set, 1.5 min each), builds a facts sheet from the chapter's own datasets, and autonomously writes a Practice set and a separate Exam set of single-answer, select-all, and true/false questions with rich per-option feedback — concepts & interpretation only (no Python code; end-of-chapter case studies skipped except in the case-study chapters ch08 and ch13). Fact-checks every number and data claim, runs two adversarial reviewer-subagent rounds, validates cue balance, builds quizzes/chNN.html (countdown timer, Exam certificate at 80%, key hidden below 80%, print-to-PDF report), runs Playwright browser tests, writes a session log, and reports. English-only. Build only — never changes the website/chapter quiz links. Does not commit. Invoke via /write-quiz chNN.
argument-hint: "<chNN>"
disable-model-invocation: true
user-invocable: true
---

# Write Quiz: an interactive Practice + Exam quiz for a metricsAI chapter

Produce **`quizzes/chNN.html`**, a self-contained quiz page that works in any browser with
internet access and no AI: students enter their name, choose **Practice** (instant rich
feedback after each question) or **Exam** (feedback at the end; full key and a printable
certificate only at ≥ 80%; otherwise a key-free review and a printable report), under a
countdown. The quiz content lives in **`quizzes/banks/chNN.json`**; the shared engine
(`quizzes/_template.html`) and builder (`scripts/build_quiz.py`) turn it into the page.

The Chapter 1 quiz is the gold standard: `quizzes/banks/ch01.json` (bank),
`quizzes/checks/ch01_factcheck.py` (fact-check), `quizzes/ch01.html` (page).

Run **fully autonomously** from start to finish. The only allowed question to the user is
the overwrite confirmation in Phase 0.

## What this skill does NOT do

- Does **not** change any link: the edcafe "Quiz" links in `index.html`, the chapter
  `.qmd` resource bar, `scripts/add_resource_buttons.py`, and `README.md` stay as they are
  (the report prints the swap locations for the user).
- Does **not** edit the chapter `.qmd` or data files. If the data contradict the chapter's
  prose, it **reports** the contradiction (e.g., ch01 line 143) and works around it.
- Does **not** change the engine's design (modes, timer, 80% pass, fixed order, print-to-PDF).
  Engine bugs found while testing may be fixed in `quizzes/_template.html` — then rebuild
  and retest **every** existing quiz.
- Does **not** commit, push, or open a PR.
- Does **not** run on ch00 (Preface).

## Example invocations

```text
/write-quiz ch02
/write-quiz ch13      # case-study chapter: its applications are quizzed
```

## Deliverables

| Path | What |
|---|---|
| `quizzes/banks/chNN.json` | the question bank (Practice + Exam), house layout |
| `quizzes/checks/chNN_factcheck.py` | facts sheet + asserts for every number/data claim (exit 0 = all pass) |
| `quizzes/chNN.html` | built quiz page (~150–250 KB, self-contained) |
| `log/YYYYMMDD_HHMM.md` | session log for this run |

Browser-test screenshots and PDFs go to `<SCRATCH>/quiz_tests/chNN/`, where `<SCRATCH>` is
the session scratchpad directory named in the system prompt; if there is none, use
`quizzes/.tests/chNN/` (gitignored).

---

## Phase 0 — Pre-flight

1. **Parse the argument.** Exactly one argument matching `^ch(0[1-9]|1[0-7])$`. Otherwise stop:
   `Usage: /write-quiz chNN   (ch01–ch17; one chapter per run)`.
2. **Locate the chapter:** exactly one `notebooks_quarto/chNN_*.qmd`.
3. **Existing quiz?** If `quizzes/banks/chNN.json` exists, ask **once** with AskUserQuestion:
   "A quiz for chNN already exists. Regenerate it from scratch?" → *Overwrite* / *Cancel*.
   On Cancel, stop without changes. (This is the only interactive prompt.)
4. **Environment:** `source .venv/bin/activate`; confirm `python3 -c "import playwright, pyfixest"`.
5. **Read, end to end, before writing anything:**
   - [`references/authoring_rubric.md`](references/authoring_rubric.md) — the rules (non-negotiable)
   - [`references/bank_schema.md`](references/bank_schema.md) — the JSON contract and markup
   - [`references/review_prompt.md`](references/review_prompt.md) — how the two reviews run
   - `quizzes/banks/ch01.json` — skim 6–8 items of each type as the quality bar

## Phase 1 — Inspect and size

```bash
python3 .claude/skills/write-quiz/scripts/inspect_chapter.py chNN
```

Returns JSON: in-scope line range (stops at the end-of-chapter `## … Case Studies`
heading; ch08/ch13 fully in scope), unit counts, **`sizing.n_items` / `sizing.minutes`**
(units rounded up to a multiple of 5, clamped to 20–40; 1.5 min per item rounded up to 5;
pass 80%), `type_mix`, `difficulty_mix`, the lists of sections / Key Concepts / objectives /
glossary terms, the datasets loaded in scope (with local `data/` copies), and existing files.
Use these numbers as-is; do not re-size by judgment.

## Phase 2 — Read the chapter and build the facts sheet

1. **Read the in-scope part of the `.qmd` in full** (not just headings): definitions,
   Key Concepts, worked results, Key Takeaways, Practice Exercises. Note the chapter's
   own terminology and section numbers for `concept` labels.
2. **Printed outputs:** the `.qmd` has no outputs; read them from
   `book/_freeze/notebooks_quarto/chNN_*/execute-results/html.json` when useful, but
   **recompute** every number you will quote.
3. **Write `quizzes/checks/chNN_factcheck.py`** from
   [`scripts/factcheck_template.py`](scripts/factcheck_template.py) (set `CHAPTER`). In
   block 1 (FACTS) load the in-scope datasets with `load("AED_….DTA")` (local `data/`
   first, GitHub fallback), reproduce the chapter's key computations, and print exact
   values. Run it to get the facts sheet. Blocks 2–3 (CHECKS, CLAIMS) are filled as items
   are written.
4. **Data claims:** before writing any statement about how variables relate (sign,
   strength, ordering, "tends to"), compute it. Chapter prose is not evidence. Record
   prose/data contradictions for the report.

## Phase 3 — Blueprint (write it down before items)

Draft a blueprint table (it goes into the log):

| # | Topic (section / Key Concept) | Practice items | Exam items | Types | Difficulty |
|---|---|---|---|---|---|

Rules (details in the rubric §2, §5, §7):

- Totals equal `n_items` per set; type counts equal `type_mix`; difficulty ≈ `difficulty_mix`.
- Every "What you'll learn" bullet assessed at least once per set; order follows the chapter.
- Practice and Exam parallel by topic and type; Exam grounded in the chapter's own results,
  Practice in parallel scenarios.
- Plan key positions up front: single-answer keys balanced A–D but **not** cycled in blocks
  (about 1 in 4 consecutive single items share a letter, no run of 3+); T/F split ~50/50;
  multi keys with varied patterns (not all odd/even positions) and varied numbers of
  correct options.

## Phase 4 — Write the bank

Write `quizzes/banks/chNN.json` per the schema and rubric: meta from Phase 1
(`chapter`, `chapter_title` without the "N. " prefix, `book_title`, `minutes`, `pass_pct: 80`,
`n_items`), then `practice` and `exam`. For every item: neutral `concept` label with section
reference; stem; options in planned order; feedback for **every** option (exam wrong-option
feedback never leaks the key); Key-idea `explanation`.

As you write, add a CHECKS line to the fact-check for every number in the bank (including
distractor arithmetic) and a CLAIMS line for every data claim. Then:

```bash
python3 .claude/skills/write-quiz/scripts/format_bank.py chNN   # house layout + sequential ids
```

## Phase 5 — Validate

```bash
python3 scripts/build_quiz.py chNN --check      # schema/policy errors must be 0
python3 quizzes/checks/chNN_factcheck.py        # must exit 0; every quoted number traced
```

Fix all errors. Resolve every `WARN` cue warning (or, if a warning is a deliberate,
justified exception, note why in the log). Eyeball the fact-check's "numbers quoted in the
bank" list: each must trace to a check or be self-evident (years, item counts).

## Phase 6 — Adversarial review, round 1

Spawn one `general-purpose` subagent with the **Round 1 prompt** from
[`references/review_prompt.md`](references/review_prompt.md), placeholders filled.
When it reports:

1. **Verify every data claim** in its findings against the data before acting (add CLAIMS
   checks as needed). Reviewers can be wrong.
2. Apply all MUST FIX; apply SHOULD FIX unless it conflicts with the fixed design; apply
   cheap NICE TO HAVE. Keep a list of what was changed, declined (and why), and which
   items became risky.
3. `format_bank.py chNN` → re-run Phase 5.

## Phase 7 — Adversarial review, round 2

Continue the **same** reviewer with `SendMessage` using the **Round 2 prompt** (change
summary, declined items, any renumbering, risky items). Verify its data claims, apply
fixes, `format_bank.py`, re-run Phase 5. Two rounds always run, even if round 1 is clean.

## Phase 8 — Build and browser-test

```bash
python3 scripts/build_quiz.py chNN
python3 .claude/skills/write-quiz/scripts/test_quiz.py chNN --out <SCRATCH>/quiz_tests/chNN
```

All checks must pass (exit 0) with no console errors. Then **look** at the outputs (Read the
PNGs): `welcome_light_1280.png`, `practice_feedback_light_1280.png`,
`fail_review_light_1280.png` (no key visible in missed items), `exam_question_dark_375.png`,
`certificate_render-1.png`, `report_render-1.png`, and `math_*.png` if the bank has math
(formulas typeset, nothing clipped). Fix and re-run, at most 3 loops; if still failing,
stop and report the failures honestly.

## Phase 9 — Log and report

Write `log/YYYYMMDD_HHMM.md` (current state, blueprint, type mix and key balance,
fact-check result, review findings fixed/declined, test result, data-vs-prose
contradictions, next steps). Then print exactly this report:

```text
✅ Quiz written: chNN — <chapter title>
   Size: <n> + <n> questions, <m>-minute countdown, pass 80%   (units <u>: sec <s>, kc <k>, lo <l>, gloss <g>)
   Types per set: single <a> / multi <b> / tf <c>   |  keys A<.>B<.>C<.>D<.>  T/F <t>/<f>
   Fact-check: <x>/<x> checks   |  Validator: 0 errors, <w> warnings
   Review: round 1 <M> must / <S> should fixed; round 2 <M2> / <S2>   (declined: <d>, see log)
   Browser tests: <p>/<p> passed (screenshots: <SCRATCH>/quiz_tests/chNN/)
   ⚠ Data vs. chapter prose: <none | short description + qmd line>

Files:
   quizzes/banks/chNN.json
   quizzes/checks/chNN_factcheck.py
   quizzes/chNN.html
   log/<stamp>.md

NEXT STEPS (not run — copy + paste when ready)
   Try it:      open quizzes/chNN.html
   Link it:     replace the chNN edcafe "Quiz" URL in index.html (chapter card),
                notebooks_quarto/chNN_*.qmd (resource bar, line ~22),
                scripts/add_resource_buttons.py ("quiz" entry), README.md (chapter table)
                with https://quarcs-lab.github.io/metricsai/quizzes/chNN.html
   Commit:      git add quizzes/banks/chNN.json quizzes/checks/chNN_factcheck.py quizzes/chNN.html log/<stamp>.md
                git commit -m "quiz: add chNN practice + exam quiz"
```

End. Do not commit. Do not modify anything else.

---

## Pedagogical contract (summary — the rubric is authoritative)

1. **Measures understanding, not test-wiseness:** no position, length, hedge, punctuation,
   negation-pair, or cross-item cues; multi keys vary.
2. **Below 80%, the key stays hidden:** exam wrong-option feedback teaches without revealing.
3. **Every number and data claim is verified against the data**, rounded from exact values.
4. **Practice teaches; it never hands over exam answers.**
5. **Application-heavy:** half the items ask students to interpret or use the chapter's results.

## Reference files

- [`references/authoring_rubric.md`](references/authoring_rubric.md) — item-writing and cue rules (ch01 lessons)
- [`references/bank_schema.md`](references/bank_schema.md) — bank JSON contract, markup, KaTeX, house layout
- [`references/review_prompt.md`](references/review_prompt.md) — round 1 / round 2 reviewer prompts and how to apply findings
- [`scripts/inspect_chapter.py`](scripts/inspect_chapter.py) — scope, unit count, sizing, mixes, datasets (`--all --table` for an overview)
- [`scripts/factcheck_template.py`](scripts/factcheck_template.py) — skeleton for `quizzes/checks/chNN_factcheck.py`
- [`scripts/format_bank.py`](scripts/format_bank.py) — house layout + sequential ids
- [`scripts/test_quiz.py`](scripts/test_quiz.py) — Playwright end-to-end tests + screenshots/PDFs
- `scripts/build_quiz.py` (project) — validator, cue warnings, builder (`--check` to validate only)
- `quizzes/_template.html` (project) — the quiz engine (KaTeX, certificate, report)

## Acceptance tests

- `inspect_chapter.py --all --table` reproduces the sizing table (ch01 → 30/45, ch02 → 25/40,
  ch05 → 35/55, ch13 → 35/55).
- `build_quiz.py ch01 --check` → 0 errors, 0 warnings; `quizzes/checks/ch01_factcheck.py` → all pass;
  `test_quiz.py ch01` → all pass.
- A deliberately broken bank (bad `n_items`, `$\beta$`, unbalanced `\(`, bare `<`) fails validation.
- A fresh run on a new chapter produces the four deliverables, passes Phases 5 and 8, and
  changes no other files (`git status`).

## Version

- **Version:** 1.0
- **Created:** 2026-10-15
- **Pilot chapter:** ch02 (after the ch01 prototype)
