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

- **Register:** です/ます form (polite-neutral textbook tone). Examples: 「〜と呼びます」「〜について見てみましょう」「〜になります」. Do NOT use だ/である form — too academic-detached for the textbook's invitational voice. Mirror the slightly conversational EN tone within です/ます constraints.
- **Acronyms:** Keep Latin script for `OLS`, `R²`, `MELI` (or `BLUE`), `IV`, `FE`, `RE`, `DiD`, `ACF`, `PACF`, `CLT`, `F-stat`, `t-stat`, `p-value`, `HAC`, `HC1`, `KDE`, `LOWESS`, `DFFITS`, `DFBETAS`, `ANOVA`, `CV`, `CAGR`. Add a Japanese gloss in parentheses on the **first occurrence per chapter** only, then bare Latin thereafter. Example first occurrence: `OLS(最小二乗法)`; example subsequent: `OLSで推定します`. This matches Japanese econometric textbook convention (Kuroda et al.) and keeps Cameron's source vocabulary recognisable.
- **Numbers and decimals:** Western numerals throughout. `10,000` (not `10千`, not `10,000円`). `0.5` (not `0.5割`, not `五割`). Decimal point is `.`, thousands separator is `,`. No 漢数字 in technical contexts.
- **Punctuation:** Full-width 「。」「、」 in prose. Half-width `,` `.` inside numeric values, code blocks, math expressions, and acronym-heavy sentences. Do NOT introduce 全角 spaces. Use 「」 not "" for quoted phrases in prose.
- **Inline tags preserved:** keep `<strong>`, `<em>`, `<a>`, `<sub>`, `<sup>`, `<li>` exactly as in EN. Do not translate HTML attribute values inside these tags (e.g., `href`). Same rule as ES.
- **Interpolation:** `{name}`, `{age}` etc. tokens are positional placeholders; preserve exactly. Japanese is SOV — word order around the placeholder may shift, but the placeholder itself never moves into a different `{` `}` form.
- **Currency:** keep `$253,910` (USD, with Western thousands separator). Do NOT convert to yen. The underlying datasets are USD-denominated.
- **Units:** `sq ft → 平方フィート` (or `sqft` if space-constrained in chart labels); other SI/imperial units kept verbatim (`kg`, `m`, `°C`).
- **Code identifiers:** Python/Stata/R variable names, function names, and any text inside `<pre>` code blocks stay 100% in English in every language. Never translate code. Tool names (`Python`, `Stata`, `R`) and package names (`pyfixest`, `statsmodels`, `linearmodels`) stay in Latin.
- **Proper nouns:** keep verbatim — `Acemoglu-Johnson-Robinson`, `Newey-West`, `Breusch-Pagan`, `Cook`, `Frisch-Waugh-Lovell`, `Gauss-Markov`, `Wooldridge`, `Cameron`, `Mendez`, `Maddison Project`. Author names get a JA gloss only if they have a well-known Japanese rendering and the chapter introduces them pedagogically.
- **Style guide source:** When a term is missing or contested, prefer vocabulary from Kuroda 黒田 (basic Japanese econometrics textbook tradition) over Western-loanword-heavy alternatives. Example: 「不偏推定量」 (Kuroda canonical) not 「アンバイアスドエスティメーター」 (katakana loanword). For modern causal-inference vocabulary (DiD, IV, RCT), the Imbens-Rubin Japanese translation is acceptable but not required — keep the Latin acronym.
- **Common pitfalls:**
  - Do NOT use `[JA]` or any placeholder prefix.
  - Do NOT translate the keys (left side of `:` in the strings file). Only translate the right-hand string values.
  - Do NOT change `{name}` interpolation placeholders.
  - Do NOT introduce 全角 numerals (`１，２，３`) into chart titles or any value rendered by Plotly.
  - Do NOT insert spaces around 「」 brackets in prose.
  - Do NOT double-translate Latin acronyms (avoid `OLS(最小二乗法、OLS)` — gloss exactly once on first occurrence).
  - Do NOT translate `code.tab.python`, `code.tab.stata`, `code.tab.r` values — they are tool names.
- **Strings-file-specific subrules (added after ch01 pilot, 2026-05-15):**
  - **No Latin-acronym JA gloss in strings files.** Strings files have no narrative order — the runtime stitches them onto a page in arbitrary sequence, so "first occurrence per chapter" is undefined. In `_shared/strings/*.js` always use bare Latin (`OLS`, `R²`, `IQR`, `MELI`) without a parenthetical Japanese gloss. The chapter prose (`.qmd`) handles first-introduction glosses.
  - **Stat-card / button-label entries strip the parenthetical.** Even if `canonical-terms.md` lists a term as `IQR（四分位範囲）`, a stat-card or short button label gets bare `IQR`. Use the parenthetical form only inside descriptive sentences where horizontal space is unconstrained.
  - **Inside escaped `\"...\"` JS string values, keep Western `"..."` quotes.** Only use 「」 for unescaped prose. Mixing 「」 inside `\"escaped\"` JS strings risks Plotly / DOM rendering surprises.
  - **Em-dash `—` strict preservation.** When EN has `—` between phrases, keep `—` in JA. Do NOT substitute Japanese 「、」 even where mid-sentence flow might prefer it. (Maintains visual parity across languages and avoids subtle reflow during language toggles.)
  - **Currency `$` is USD throughout.** Never swap `$` to `¥`. Datasets are USD-denominated; the `$` is part of the data, not the language. Leave `$253,910` exactly as-is in JA values.

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
