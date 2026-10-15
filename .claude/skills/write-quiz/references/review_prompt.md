# Reviewer prompts: adversarial quiz review (two rounds)

The skill spawns ONE `general-purpose` subagent for round 1, then continues the **same**
agent with `SendMessage` for round 2 (it keeps its context). Fill the `{…}` placeholders.
The reviewer only reports; the skill applies fixes.

After each round, **verify every data claim the reviewer makes before acting on it**
(run a one-off computation or add it to the fact-check CLAIMS block). In ch01, a reviewer
suggestion of "row order" as an arbitrary distractor was false: the data file is sorted by
price.

---

## Round 1 prompt

```text
You are an expert econometrics instructor and assessment designer doing an ADVERSARIAL
review of a {N_TOTAL}-item quiz bank for Chapter {CH_NUM} ({CHAPTER_TITLE}) of an intro
econometrics book. Do NOT edit any files — report only.

Read fully:
- Quiz bank: {BANK_PATH} ({N} "practice" items P01–P{N}, {N} "exam" items E01–E{N};
  types: single = one correct option, multi = select-all-that-apply scored
  all-or-nothing, tf = true/false). Options are shown in FIXED order (no shuffling) and
  exam retakes are unlimited, so position patterns and leaks persist across attempts.
- Chapter source: {QMD_PATH}, lines {FIRST_LINE}–{LAST_LINE} (the in-scope part).
- Facts sheet: run `python3 {FACTCHECK_PATH}` to see the exact values; the data are in
  data/ (load with pandas.read_stata). Verify any data claim you make against the data
  before reporting it.
- Authoring rules the bank must follow: .claude/skills/write-quiz/references/authoring_rubric.md

Context: undergraduates new to econometrics; scope is concepts & interpretation (no Python
code{SCOPE_NOTE}). Math is written as \( … \) and rendered by KaTeX.

Critical design rule: in Exam mode, a student who scores below 80% sees ONLY the feedback
for the wrong option(s) they picked plus the item's "concept" label — never the correct
option or the explanation. So EXAM wrong-option feedback must not name, quote, or make
trivially identifiable the correct option (no one-step corrections, no negating a sibling
option). TF items are exempt. Concept labels must be neutral.

Check every item for:
1. Key errors: is the marked key correct and every other option wrong? For multi items,
   is each option's status defensible? Also check against the data and against reverse
   readings (e.g., the reverse regression).
2. Ambiguity: could a strong student defend a distractor or attack the key?
3. Statistical accuracy and alignment with the chapter's terminology and sections.
4. Exam feedback leaks (see the design rule) and concept labels that name the answer.
5. Test-wiseness cues: key positions, multi key patterns (odd/even, same count of
   correct options), key longest/most hedged, absolutes only in distractors, punctuation
   or grammar cues, logical-negation pairs.
6. Cross-item giveaways inside the exam, and practice items that give away a specific
   exam answer (same scenario + same answer, or explanations naming it).
7. Numbers: any figure not supported by the facts sheet or rounded inconsistently.
8. Typos, grammar, US spelling, serial commas, markup (&lt; for '<', KaTeX delimiters).

Output: a concise list grouped by severity — MUST FIX (wrong key, factual or data error,
real ambiguity, exam leak), SHOULD FIX (cues, cross-item giveaways, misleading wording),
NICE TO HAVE. For each: item id, the problem in one or two sentences, and exact
replacement text. End with a short overall assessment (difficulty mix, coverage of the
"What you'll learn" bullets, residual risks). Don't invent problems; skip items that are fine.
```

`{SCOPE_NOTE}`: for regular chapters `", no end-of-chapter case studies"`; for ch08/ch13
`"; this chapter consists of case studies, which ARE in scope"`.

---

## Round 2 prompt (SendMessage to the same agent)

```text
Round 2 review: I applied your round-1 findings to {BANK_PATH} — please re-review the
REVISED file (read-only, report only).

Changes made: {CHANGE_SUMMARY}
Not applied (with reason): {DECLINED_SUMMARY}
{RENUMBERING_NOTE}

Please verify: (1) no wrong keys or new ambiguity introduced by the rewrites — especially
{RISKY_ITEMS}; (2) remaining exam wrong-option feedback leaks; (3) remaining cues
(positions, length, multi patterns); (4) cross-item and practice→exam giveaways;
(5) any new data claim, checked against the data; (6) typos. Same MUST / SHOULD / NICE
format, only real problems, with exact replacement text.
```

---

## Applying findings

- Apply all MUST FIX items. Apply SHOULD FIX items unless they conflict with the
  instructor's fixed decisions (fixed question/option order, 80% pass, no Python items,
  no end-of-chapter case studies), then say why in the log.
- Apply NICE TO HAVE items when cheap and safe.
- Re-run the validator and the fact-check after every batch of edits. A fix that adds a
  number or a data claim needs a matching check.
