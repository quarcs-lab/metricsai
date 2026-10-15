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
- **Strengthening a stem can kill a distractor:** adding "a large effect" made "too small to
  matter" a free elimination (ch08 E05). Re-read every option after editing a stem.
- **Exact-vs-approximate items need a near distractor** (e.g., 2 × the one-year exact value),
  not only far-off scaling errors (ch09 E08).
- **Ordinal words can be read two ways:** "the 5th and 95th" reads as percentiles; write
  "positions 50 and 950" (ch12 E21).
- **No distractor may contradict the item's own stem** ("the coin must be unfair" when the
  stem says "a fair coin"; "ages were normal" when the stem says "far from normal"). Such
  options are free eliminations (ch03 E04, E19).

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
- **Hedges in T/F:** if every True statement is hedged ("most likely", "about") and every
  False one is absolute ("any", "always"), the wording predicts the answer. Mix them, and
  plan T/F flips together: flipping one item to fix a cue can force a second flip to keep
  the split (ch03 E03 → E17).
- **Length, both ways:** aim for the key being the longest option in roughly 20–40% of
  wordy items. Padding distractors until the key is *never* longest is a cue too
  ("avoid the longest" worked in ch12's first revision). In multis, the correct options must
  not all be longer than the wrong ones, and 4-option multis must not all have exactly 2 keys.
- **Length:** the key must not be systematically the longest. Trim the key or lengthen
  distractors so lengths overlap.
- **Hedges and absolutes:** don't put "about / tends / may" only on the key and
  "always / exactly / never / guarantees / only" only on distractors.
- **Grammar and punctuation:** all options in an item share sentence form and end
  punctuation.
- **Echo:** the key must not repeat the stem's wording while distractors don't.
- **Concept labels** (`concept`, shown to failing students) are neutral topic names with a
  section reference, never the answer, and never the property under test (ch03 "Efficiency",
  ch06 "Monte Carlo simulation and unbiasedness", "Asymptotic normality"). Good: "Making predictions with the fitted line
  (Section 1.9)". Bad: "Extrapolation is unreliable (Section 1.9)".

- **Validator HINT lines** (`build_quiz.py`, "leak hints") flag likely one-step-correction
  feedback, a computed key value printed in another exam item, and practice keys worded like
  exam keys. They are heuristics: read every one, fix it or note why it is a false positive.

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
- **Rounded products:** when an item shows "a × b ≈ c" with rounded a and b, c must equal the
  product of the *shown* factors (ch07: the chapter's 2.052 × 11.17 ≈ 22.93 is really 22.92),
  or write the factor symbolically ("× se(b₂)").
- **Simulation chapters:** reproduce the chapter's seeds and draw order exactly in the
  fact-check; chapters print `np.std` (ddof = 0) for simulated SDs while pandas `.std()` uses
  ddof = 1. Phrase what-if values ("with n = 120…") as "closest to" so the key holds for any seed.
- **Coincidental collisions leak too:** a key value that equals another exam item's printed
  statistic (2.4 vs. t ≈ 2.4) is a leak even if the meanings differ; rescale the scenario (ch08).
- **Predictions stay inside the model's fitted range** (ch09: $100,000 was beyond the log model's
  maximum prediction). Hypothetical scenarios must be internally consistent: check R² vs.
  adjusted R², intervals, and p-values in the fact-check (ch11 P32 was impossible).
- **A key that contradicts chapter prose** (even when the data back it) must be checkable from the
  stem; otherwise choose another key and report the prose (ch08: Luxembourg's spending).
- **AED columns are often int8/int16:** cast with `.astype(float)` before arithmetic or logs
  (overflow; `np.log` returns float16). Note where the chapter's printed values carry this error.
- **Constants the data can't verify** (e.g., ch03's census μ and σ, given by the chapter) go in
  a labeled block of the fact-check, not among the data checks.
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
- **Computed values leak:** a number an item asks students to compute must not be printed in
  any other exam stem or option (ch07: se = 11.17 appeared in three stems, so the SE item was
  free). Watch derivable formulas too: ch03 printed σ = 18.61, SD(X̄) = 3.72, and n = 25 in
  different stems, so σ/√n could be recovered without knowing it.
- **Printed results decide other items:** a confidence interval or p-value printed in one exam
  stem settles any test of that coefficient elsewhere (ch11: a printed p = 0.83 ruled out
  F > 1 options; a printed CI ruled out large t values). Choose distractors on both sides.
- **Options teach rules:** an option or a true T/F statement must not state a rule that another
  exam item tests (ch04: "|t| above the critical value means reject" answered the next item;
  ch07: "3 degrees of freedom with n = 5" taught n − 2 for the df item).
- **Practice feedback and explanations** must not state an exam item's answer, even in a
  different scenario (ch03 P11/P24, ch06 P10/P26, ch07 P03).
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
  - **Fully crossed items** (two dimensions × two values, including scale × units, as in
    log-model interpretations, ch09): give every wrong option the *same*
    neutral feedback. Distinct feedback says which half is wrong and points to the key
    (ch06 E04, E10).
  - Reviewer-caught one-step corrections to avoid: "Check the value on which the interval is
    centered", "Check which tail a lower-tailed test uses", "Check the size of the difference",
    "Check which standard deviation belongs in the denominator", "Check the last step".
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
- Plain Unicode is fine for simple symbols (R², β₁, ×, −, ≈, ÷). Within one item, write a
  symbol either in KaTeX or in Unicode, not both (mixed fonts in ch06 E18).
- Never put `<script` anywhere (the validator rejects it).
