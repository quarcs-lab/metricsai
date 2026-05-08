# Pedagogical Rubric for the Key Concepts Section

This rubric is the heart of the skill. It is loaded into Claude's working context every time the skill runs. Every drafted concept must satisfy it before the section is inserted into the chapter.

The goal is simple: **foster learning as much as possible.** That means concrete, dataset-grounded examples and vivid, distinct analogies — not generic textbook prose.

---

## The three hard rules (non-negotiable)

### Rule 1 — Examples are dataset-grounded

Every Example MUST reference the chapter's actual dataset(s) and at least one real variable name.

- ✅ "For the 29 Davis houses, regressing `price` on `size` gives $\beta_1 \approx 73.77$ — each extra square foot is associated with about \$74 more in sale price."
- ❌ "Imagine a dataset of houses where price depends on size."
- ❌ "Consider a hypothetical regression…"
- ❌ "In economic data, …" (without naming a specific variable from this chapter)

If the chapter does not produce a numerical value for a concept, use the variable name and structure (e.g., "the slope of `price` on `size`") — but never fall back to a hypothetical.

### Rule 2 — Definitions are short and assume only earlier-chapter vocabulary

- 1–2 sentences.
- No jargon that has not been defined in chapters 0…N−1 (the skill consults `prior_chapters_defined_terms` from the inspect script).
- Never reuse the defined term inside the definition. ❌ "Correlation is the correlation between …" → ✅ "A number between −1 and +1 that summarizes how two variables move together."
- Plain prose. Active voice. No Latinate vocabulary where a Germanic word will do.
- Do not include the formula. The formula belongs in the chapter body, not the glossary entry.

### Rule 3 — Each concept ties to a Learning Objective bullet

Every chosen concept must map to a specific bullet in the chapter's `**What you'll learn:**` list (under `## Chapter Overview`). The skill records the mapping in the final report. Concepts that don't map to a bullet are dropped — even if they're foundational — because the section's job is to scaffold the chapter's stated outcomes.

It is acceptable for two concepts to map to the same bullet (e.g., "Correlation Coefficient" and "Covariance" both serve "How to compute and interpret correlation"). It is not acceptable for a concept to map to no bullet.

---

## Writing definitions — heuristics

Aim for a definition a 19-year-old reading their first econometrics chapter could parse on a single read.

- **Lead with the function the concept performs**: "a number that measures…", "a method for choosing…", "a model that predicts…". Not "the conditional expectation of…".
- **Prefer concrete to abstract**: "the difference between actual and predicted Y" beats "an estimate of the disturbance term".
- **Avoid passive voice**: "OLS picks the line that…" beats "The line is chosen so that…".
- **Avoid Latinate vocabulary** when a plainer word exists: "use" beats "utilize", "show" beats "demonstrate", "change" beats "modification".
- **Bound the concept** when relevant: "ranges from 0 to 1", "always positive", "between −1 and +1". Bounds anchor intuition.

---

## Writing examples — heuristics

The Example callout has one job: turn the definition into a concrete number from the chapter's dataset.

- **Lead with the dataset and N**: "For the 29 Davis houses…", "Across 108 countries from 1990–2014…", "Among 339 Bolivian municipalities…". This grounds the reader in the chapter's data.
- **Include at least one numeric value the chapter actually computes**. Pull it from regression output, descriptive statistics, or correlation tables that appear in the chapter body. If the chapter computes $R^2 = 0.6175$, write "$R^2 \approx 0.62$" — not "$R^2$ is high".
- **End with a one-clause real-world interpretation** tying the number back to the variable's meaning: "…each extra square foot is associated with about \$74 more in sale price", "…61% of provincial development variation is captured by night-time lights".
- **Keep it 2–4 sentences.** Longer examples obscure the point; shorter ones don't earn the callout's space.
- **Use Quarto-friendly syntax**: backticks for variable names (`size`), `$...$` for inline math, `\$74` for literal dollar signs.

---

## Writing analogies — heuristics

Vivid is more important than perfect. The analogy doesn't have to be mathematically airtight — it has to be sticky. Six months later the student should remember the analogy and reconstruct the concept from it.

- **Concrete and physical** beats abstract. Hanging a clothesline through fence-poles of different heights (OLS) beats "minimizing a quadratic objective".
- **Each analogy in the same chapter must come from a different domain.** The skill maintains a "domains-used-so-far" list while drafting and rejects same-domain duplicates. Suggested domain palette:
    - **Cooking & food** (recipes, ingredients, baking)
    - **Sports** (running pace, scoring, team play)
    - **Transportation** (taxi fares, GPS, trains)
    - **Weather & nature** (forecasts, river currents, gardens)
    - **Money & shopping** (rent, bargaining, tipping)
    - **Music & sound** (volume knobs, instruments tuning)
    - **Geography & travel** (maps, scaled distances)
    - **Construction & DIY** (clotheslines, scaffolds, shelves)
    - **Common objects** (rulers, scales, thermostats)
- **End with a one-line bridge** that names the concept: "…the same way a regression line balances residuals."
- **2–4 sentences.** Same length budget as the example.

---

## Anti-patterns to reject (auto-fail; redraft required)

- ❌ "Imagine a regression line…" — not concrete, not dataset-grounded. Violates Rule 1.
- ❌ "Like in calculus, where you take a derivative…" — other-discipline academic analogy; obscures rather than clarifies.
- ❌ "It's just like correlation but multiplied by …" — defining a term using a sibling technical term, no analogy at all.
- ❌ Two concepts in the same chapter using analogies from the same domain (e.g., two cooking analogies). Drop one and redraft from a different domain.
- ❌ Definition that contains the term itself ("Correlation is the correlation…").
- ❌ Definition that introduces a term not yet defined in this or prior chapters.
- ❌ Example that uses "imagine", "consider", "hypothetical", or "suppose" as its leading verb.
- ❌ Analogy that secretly assumes the math (e.g., "OLS is like minimization" — minimization IS the math, not an analogy).
- ❌ Bullet-point lists inside any callout. Callouts hold prose only.

---

## Quality self-check before finalizing each concept

Before assembling the section, read each drafted concept and answer:

1. Does the **example** name a real dataset variable from this chapter's setup?
2. Does the **example** include a real number the chapter computes?
3. Is the **definition** under 2 sentences and free of undefined jargon?
4. Does the **definition** avoid using the defined term itself?
5. Does the **analogy** come from a domain not used by any sibling concept in this chapter?
6. Does the **analogy** end with a sentence that bridges back to the concept?
7. Does this concept tie to a specific bullet in `**What you'll learn:**`?

If any answer is "no", redraft that piece before moving on. Better five strong concepts than seven mediocre ones.
