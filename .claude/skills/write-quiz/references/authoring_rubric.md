# Authoring rubric: metricsAI chapter quizzes

Read this file end-to-end before writing a single item. Every rule below was earned on the
Chapter 1 quiz (`quizzes/banks/ch01.json`, the gold example) — most of them by an
adversarial reviewer catching a real defect.

The quiz must measure **understanding of the chapter**, not test-taking skill. A student who
has not learned the concept should not be able to pass by elimination, option length, answer
position, feedback leaks, or cross-references between items.

---

## 1. Scope

- **In scope:** the chapter from the top through the last numbered section before the
  end-of-chapter `## … Case Studies` heading: Chapter Overview, Key Concepts glossary,
  numbered sections, inline `> **Key Concept N.M**` blockquotes, Key Takeaways, Practice
  Exercises, and the chapter's own datasets and printed results.
- **Out of scope:** the end-of-chapter Case Studies (convergence clubs, DS4Bolivia,
  satellite data), Python syntax / code-reading items, anything not taught in this chapter.
- **ch08 and ch13 are case-study chapters:** their applications *are* the content, so they
  are quizzed (concepts and interpretation of each application).
- Later chapters may reuse ideas from earlier chapters, but every item must be answerable
  from this chapter's text.

## 2. Blueprint

- **Size:** from `inspect_chapter.py` (`sizing.n_items`, `sizing.minutes`). Practice and
  Exam both have exactly `n_items` items. Pass mark is always 80%.
- **Topics:** allocate items in proportion to the chapter's sections and Key Concepts. Every
  "What you'll learn" bullet is assessed at least once per set. Order items to follow the
  chapter's flow (the quiz shows them in fixed order).
- **Parallel sets:** Practice mirrors the Exam topic by topic, item type by item type, but
  never with the same scenario and the same answer (see §7).
- **Type mix** (`inspect_chapter.py` → `type_mix`): ~63% `single` (4 options), ~17% `multi`
  (4–5 options, all-or-nothing), ~20% `tf`.
- **Difficulty** (`difficulty_mix`): ~15% recall (definitions), ~35% understanding (explain,
  distinguish), ~50% application (interpret the chapter's own numbers, compute a prediction
  or difference, transfer to a new scenario, spot a fallacy).
- **Exam** items are grounded in the chapter's datasets and results. **Practice** items use
  parallel scenarios (e.g., the chapter's Practice Exercises, other plausible economic
  examples) so practice trains the skill without pre-teaching exam answers.

## 3. Stems

- One clear question. Quote the numbers needed; never require a table or plot
  (the quiz is text + math only).
- Use "Suppose …" for hypothetical scenarios; never present invented numbers as real data.
- For `tf`, the stem is a single declarative statement that is unambiguously true or false
  as worded. Avoid statements that are "trivially false" by an absolute nobody believes;
  prefer a tempting misconception (e.g., "an R² well below 1 means the regression is
  useless").
- `multi` stems end with "(Select all that apply.)"; `single` stems ask for the *best*
  answer only when several options are partially right by design.

## 4. Options

- Exactly one correct option for `single`; 2+ correct for `multi`; `tf` options are
  exactly `["True", "False"]`.
- Every distractor is a **real misconception** a student could hold after reading the
  chapter (reversed roles, causal reading of an association, slope vs. R², forgetting the
  intercept, extrapolation, wrong units, wrong subtraction order…), not a joke option.
- **Every option is wrong or right for a reason the chapter teaches.** A distractor must
  not be defensible: check it against the data (§6), against the reverse case (e.g., R² of
  y on x equals R² of x on y in simple regression), and against strong-student readings.
- **No logical-negation pairs** (option B = "not option E"): feedback on one gives away
  the other. The same applies to two-way splits with no third choice ("left-skewed" vs.
  "right-skewed" with no "symmetric" option; "lighter tails" vs. "heavier tails"): add a
  third, independent alternative.
- **Numeric distractors trace to a named misconception** (forgot the intercept, divided by
  the mean instead of the SD, part-to-rest instead of part-to-whole, used the median, one
  category instead of the group…). No number that no plausible error produces.
- **No complement of the key** (26% when the key is 74%) and **no second option with the
  key's number** unless the item is fully crossed (two values × two interpretations, as in
  the ch02 IQR item); otherwise wrong-option feedback on the twin gives the key away.
- **Hypothetical scenarios start with "Suppose"** so students never mistake invented
  numbers for the chapter's data.

## 5. Cue control (the validator warns on most of these — fix, don't ignore)

- **Key positions:** single-answer keys spread evenly across A–D; T/F answers split
  ~50/50; multi keys vary in pattern (never all odd/even positions, never always "A, C")
  and in the number of correct options.
- **Multi option counts:** vary the number of *wrong* options too. If every 4-option item
  has 2 keys and every 5-option item has 3 (always two distractors, as in the first drafts of
  ch01 and ch02), the option count tells students how many boxes to tick.
- **Key sequence:** do **not** rotate keys through A–D in blocks (ch02 round 1: every run of
  four items was a permutation of A–D, so no letter ever repeated and students could rule
  out the previous letter). About 1 in 4 consecutive single items should share a key letter,
  with no run of 3+. Plan the sequence, then check with the validator.
- **Length:** the key must not be systematically the longest. Trim the key or lengthen
  distractors so lengths overlap.
- **Hedges and absolutes:** don't put "about / tends / may" only on the key and
  "always / exactly / never / guarantees / only" only on distractors.
- **Grammar and punctuation:** all options in an item share sentence form and end
  punctuation.
- **Echo:** the key must not repeat the stem's wording while distractors don't.
- **Concept labels** (`concept`, shown to failing students) are neutral topic names with a
  section reference, never the answer. Good: "Making predictions with the fitted line
  (Section 1.9)". Bad: "Extrapolation is unreliable (Section 1.9)".

## 6. Numbers and data claims

- Every number comes from the chapter's **facts sheet** (`quizzes/checks/chNN_factcheck.py`)
  and is rounded **from the exact value** in the precision the item shows.
- When an item uses the chapter's rounded equation (e.g., `115,017 + 73.77 × size`), state
  it in the stem and compute options from that rounded equation; check them in the facts
  sheet.
- **Any claim about how variables relate in the data** (sign, strength, ordering, ranges)
  must be asserted in the fact-check's CLAIMS block. Chapter prose is *not* evidence:
  ch01 said "bigger houses tend to be newer", but r(size, age) = 0.08 in AED_HOUSE.
- Beware "arbitrary" distractors that are not arbitrary in the data (AED_HOUSE rows are
  sorted by price, so "row order" correlates 0.88 with price). Use truly random things
  ("a random number assigned by a computer").
- **Check the data's coverage before describing it** (first/last dates, number of
  observations per period): AED_REALGDPPC ends in 2020 Q1, although the chapter says
  "1959 to 2020". Say "early 2020", not "end of 2020".
- **Chapter prose can be conceptually wrong too.** ch02 line 934 says z-scores "can
  normalize skewed distributions", but standardizing never changes a distribution's shape.
  Never build an item whose key contradicts a chapter sentence without making the item
  unambiguous on its own terms, and report the sentence as a contradiction.

## 7. Independence

- **Within the exam:** no item may answer another. Check that no stem, option, feedback,
  or explanation states a fact another exam item tests (e.g., one item's options stating
  the t-statistic formula verbatim while another item asks students to compute t).
  Students navigate freely between exam items.
- **Practice → Exam:** practice may teach the same concept, but never the same scenario
  with the same answer, the same distractor set in the same roles, or explanations that
  name an exam item's answer. Mirror rather than clone (ch02: practice uses a
  *left*-skewed exam-score example where the exam uses right-skewed earnings).
- **Stems leak too:** an exam stem that states a fact (e.g., "mean ± 1 SD contains 75%")
  can rule out options in another exam item. Read every exam stem against every other
  exam item.

## 8. Feedback and explanations

Every option has its own `feedback`; every item has an `explanation` ("Key idea").

- **Correct-option feedback:** "Correct. …" plus why.
- **Practice wrong-option feedback:** may teach directly (the key is shown anyway).
- **Exam wrong-option feedback is shown to failing students *without* the key.** It must:
  - explain why *that* choice fails or point to the concept/section to revisit;
  - **never** state the correct value or option, quote the key, give the one-step correction
    ("you divided instead of multiplying", "you forgot the intercept"), or negate a sibling
    option;
  - TF items are exempt (the leak is accepted), but still prefer "revisit Section X".
  - Good: "Check how the t value is formed from the coefficient and its standard error
    (Section 1.7)." Bad: "This ratio is upside down."
- **Explanation (Key idea):** 1–3 sentences, cites the Key Concept or section, may state
  the answer and the worked computation (shown only with the full key).

## 9. Statistical wording

Use the chapter's terminology and keep definitions precise:

- regression measures **association**; causal claims need more than observational data;
- standard error = **precision** of an estimate (smaller = more precise);
- t = coefficient ÷ standard error; p-value: probability, **if the null were true**, of a
  result **at least as extreme** as the one observed — not the probability the null is true;
- R² = share of the variation in **Y** explained; fit, not causation; unit-free;
- RMSE = typical size of a prediction error, in units of Y;
- residual = actual − predicted (vertical distance);
- confidence intervals and tests only at the depth the chapter teaches them.

## 10. Style and markup

- US spelling; **serial (Oxford) comma**, as in the chapter ("direction, strength, and form").
- `$` is **currency only**. Math uses KaTeX delimiters `\( … \)` (inline) and `\[ … \]`
  (display); in JSON, backslashes are doubled: `"\\( \\hat{\\beta}_1 \\)"`.
- Allowed inline HTML: `<b> <i> <sub> <sup> <br> <code>`. A literal less-than sign is
  `&lt;` (e.g., `p &lt; 0.001`).
- Plain Unicode is fine for simple symbols (R², β₁, ×, −, ≈, ÷).
- Never put `<script` anywhere (the validator rejects it).
