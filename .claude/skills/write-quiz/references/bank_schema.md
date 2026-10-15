# Quiz bank schema: `quizzes/banks/chNN.json`

The bank is the single source of truth for a chapter quiz. `scripts/build_quiz.py` validates
it and inlines it (base64) into `quizzes/_template.html` to produce `quizzes/chNN.html`.
Gold example: `quizzes/banks/ch01.json`.

## Top level

```json
{
  "meta": {
    "chapter": "05",
    "chapter_title": "Bivariate Data Summary",
    "book_title": "metricsAI: An Introduction to Econometrics with Python and AI in the Cloud",
    "minutes": 55,
    "pass_pct": 80,
    "n_items": 35
  },
  "practice": [ /* exactly n_items items, ids P01… */ ],
  "exam":     [ /* exactly n_items items, ids E01… */ ]
}
```

| Field | Rule (enforced by `build_quiz.py`) |
|---|---|
| `chapter` | two digits, e.g. `"05"` (shown as "Chapter 5") |
| `chapter_title` | the `.qmd` title without the "N. " prefix |
| `n_items` | from `inspect_chapter.py`: multiple of 5 in [20, 40] |
| `minutes` | 1.5 × `n_items`, rounded up to a multiple of 5 |
| `pass_pct` | always `80` |

## Item

```json
{
  "id": "E07",
  "type": "single",
  "concept": "Interpreting the slope (Sections 1.1, 1.6, and 1.7, Key Concept 1.4)",
  "stem": "The fitted line is predicted price = 115,017 + 73.77 × size. Which statement correctly interprets the number 73.77?",
  "options": [
    {"text": "…", "correct": false, "feedback": "…"},
    {"text": "…", "correct": true,  "feedback": "Correct. …"}
  ],
  "explanation": "Key Concept 1.4: …"
}
```

| Field | Rule |
|---|---|
| `id` | `P01`…/`E01`…, sequential in display order, unique |
| `type` | `single` (3–5 options, exactly 1 correct; use 4), `multi` (≥3 options, ≥2 correct; use 4–5), `tf` (exactly `["True","False"]`, 1 correct) |
| `concept` | neutral topic + section/Key Concept reference; shown to failing students |
| `stem` | question text; trusted inline HTML + KaTeX allowed |
| `options[].feedback` | non-empty for every option (exam wrong-option feedback must not leak the key) |
| `explanation` | "Key idea", shown only with the full key |

Stems must be unique across both sets (normalized). Items display in array order; options
display in array order (no shuffling), so the author controls key positions.

## Markup

- Inline HTML: `<b> <i> <sub> <sup> <br> <code>`. Literal `<` → `&lt;`.
- Math (KaTeX, rendered in the browser): inline `\( … \)`, display `\[ … \]`.
  In JSON every backslash is doubled:
  `"stem": "The estimator is \\( \\hat{\\beta}_1 = \\frac{\\sum (x_i-\\bar x)(y_i-\\bar y)}{\\sum (x_i-\\bar x)^2} \\)."`
- `$` is reserved for currency (`$73.77`); the validator rejects `$` followed by anything
  but a digit. Write "dollars" when no number follows.
- Unicode is fine for light notation: R², β₁, ε, ×, −, ≈, ÷, √, Σ.

## House style for the JSON file

Keep the compact layout of `ch01.json` (easy diffs and hand edits): one key per line for
item fields, one option per line, two-space indentation, UTF-8, `ensure_ascii=False`.
After any programmatic edit (or after inserting/moving items), normalize the file and
renumber ids in display order with:

```bash
python3 .claude/skills/write-quiz/scripts/format_bank.py chNN
```

## Engine facts the author can rely on

- Practice: answer → "Check" → verdict + every option marked with its feedback + Key idea.
- Exam: free navigation and flags; on submit, below 80% the review shows only the
  student's picks, feedback on their *wrong* picks, "At least one option that also applies
  was not selected" for incomplete multi answers, and the concept label. At 80%+ the full
  key unlocks and a certificate is printable. Retakes are unlimited (attempts counted per
  browser).
- Countdown = `meta.minutes` in both modes; warnings at 5:00 and 1:00; auto-submit at 0.
