# Translation style notes — metricsAI

Per-language tone and voice guidance for translators (humans or LLM subagents). Read this before translating; pair it with `canonical-terms.md` for vocabulary.

## Spanish (es)

- **Register:** informal "tú" (not "usted"). Matches the textbook's English "you" — students addressed as peers.
- **Formality:** explanatory, conversational, but precise on technical terms. Mirror the slightly playful EN voice (e.g., callouts that say "the answer: it lies, and our p-values lie with it" become "la respuesta: miente, y nuestros valores p mienten con él").
- **Inline tags preserved:** keep `<strong>`, `<em>`, `<a>`, `<sub>`, `<sup>`, `<li>` exactly as in EN. Do not translate HTML attribute values inside these tags (e.g., `href`).
- **Numbers and decimals:** keep the source format. The chapter prose mixes `0.5` and `0,5`; default to `0.5` (matches the chart numerics, which Plotly renders with periods).
- **Currency:** keep `$` and the comma-thousands format (`$253,910`). Do not convert to local currency.
- **Units:** `sq ft → pies²`; `ft² → pies²` is acceptable but `pies²` is preferred. Other SI/imperial units kept verbatim.
- **Acronyms:** prefer the Spanish acronym when canonical (`MCO`, `MELI`, `IC`, `EE`, `RIC`, `FIV`, `MC2E`, `VI`, `FAC`, `SVO`, `EM`, `IP`, `gl`, `ECM`, `RECM`, `TCAC`, `ECA`). When an acronym has no canonical Spanish form, keep the English form (`HAC`, `HC1`, `KDE`, `LOWESS`, `DFFITS`, `DFBETAS`, `ANOVA`, `DiD`, `CV`, `CAGR`).
- **Proper nouns:** keep verbatim — `Acemoglu-Johnson-Robinson`, `Newey-West`, `Breusch-Pagan`, `Cook`, `Frisch-Waugh-Lovell`, `Gauss-Markov`, `Maddison Project`, etc.
- **Code identifiers:** Python/Stata/R variable names, function names, and any text inside `<pre>` code blocks stay 100% in English in every language. Never translate code.
- **Spelling:** modern peninsular orthography (use `c` not `s` in `heterocedasticidad` / `homocedasticidad`).
- **Common pitfalls (from earlier review):**
  - Do NOT use `[ES]` or any placeholder prefix.
  - Do NOT translate the keys (left side of `:` in the strings file). Only translate the right-hand string values.
  - Do NOT change `{name}` interpolation placeholders. They must appear in the translated string in the same form (e.g., `t("greeting", {name: "Ana"})` expects the Spanish string to contain `{name}`).

## Japanese (ja)

*(To be filled in when JA rollout starts. Stub guidance below.)*

- **Register:** to be decided — likely です/ます form (polite-neutral) for textbook tone; not casual だ/である.
- **Numbers:** Plotly chart numerics will likely stay Western (10,000 not 10千). Confirm during JA pilot chapter.
- **Acronyms:** likely keep most English acronyms (OLS, R², etc.) since Japanese econometric texts commonly do; canonical-terms.md to be extended with `JA` column once a domain glossary is sourced.
- **HTML preservation:** same rule as Spanish — keep `<strong>`, `<em>`, `<a>`, `{name}` interpolations exactly.
- **Code identifiers:** untouched, same as Spanish.
- **Style guide source:** consider grounding on Cameron's Japanese textbook editions if available, or on a standard Japanese econometric textbook (Kuroda's edition for example) for vocabulary.

---

## Subagent prompt template

When dispatching a subagent to translate `web-apps/_shared/strings/<file>.js`:

```
Translate the EN values in <file> into <lang>. Use:
  - web-apps/_shared/glossary/canonical-terms.md  (vocabulary — non-negotiable)
  - web-apps/_shared/glossary/style-notes.md      (tone, register, formatting)

Rules:
  1. Add a `<lang>: "..."` field to every entry that's missing it. Do not modify EN values.
  2. Use canonical-terms.md verbatim for any term it lists. If a term is missing,
     ADD a row to canonical-terms.md with your choice + a one-line rationale, then translate.
  3. Preserve all `{name}` interpolation placeholders.
  4. Preserve all HTML inline tags (<strong>, <em>, <a>, <sub>, <sup>, <li>).
  5. Do not translate keys, code, or HTML attribute values.
  6. After editing, run `python3 scripts/i18n_check.py` and report its output.
  7. Reply with: number of entries translated, vocabulary additions made (if any),
     and the i18n_check.py exit code.
```
