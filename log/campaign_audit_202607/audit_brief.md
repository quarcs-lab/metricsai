# Audit Brief — metricsAI campaign (read this FIRST, follow it exactly)

You are auditing one chapter of the metricsAI econometrics book (based on Cameron's *Analysis of Economics Data*, AED). Repo root: `/Users/carlosmendez/Documents/GitHub/metricsai`. The `.qmd` in `notebooks_quarto/` is the sole source of truth. **Phase 1 is READ-ONLY: never modify any repo file.** You produce findings only.

## Global facts

- Regression engine is **pyfixest** (`pf.feols`) everywhere; robust SEs = `vcov='HC1'`; pyfixest default is `iid` (classical). statsmodels appears only for `lowess` (+2 `smf.ols` in ch16); scipy.stats for distributions.
- Outputs are produced at render time and NEVER stored in the .qmd — every number in prose is hand-typed and may be stale. Fresh execution dumps: `log/campaign_audit_202607/exec/chNN_outputs.txt` (cell-by-cell outputs of the whole chapter, executed 2026-07-07). Trust the dump over prose. To recompute something ad hoc: `source .venv/bin/activate` and run Python (data URLs are in the chapter Setup cells).
- The exported Colab notebook keeps ALL `{python}` cells as runnable (including `#| eval: false` ones) and keeps plain ```python fences as non-runnable markdown. Inline `{python}` expressions in prose are PROHIBITED (they'd render as literal text in Colab).
- Chapter title heading words are LOAD-BEARING: 90+ web-app deep links derive from heading text. **Never propose changing the words of any heading** — only numbering/punctuation format per the table below.
- Key Concept numbering (`> **Key Concept N.M**`) is sequential and decoupled from section numbers. Before proposing any KC renumber, grep `web-apps/_shared/strings/chNN*.js` and `web-apps/chNN/template.html` for "Key Concept N.M" references.

## Lens A — Methods presentation
- CI interpretation: repeated-sampling wording. "95% probability that β is in this interval" is allowed ONLY inside explicitly labeled misconception/WRONG blocks (e.g. ch07 ~L451–471, ch04 misconception exercises) — those are intentional pedagogy, do NOT flag.
- t vs normal: t(n−1) for mean, t(n−2) bivariate, t(n−k) multiple; bare 1.96 only with an explicit large-sample note.
- R²: "proportion/fraction of variation in y explained"; R² = r² claimed only for bivariate; never causal wording.
- Log interpretations (canonical phrasing = ch09 §9.2): log-linear "≈100×β % change per unit of x, accurate for |β|<0.1; exact effect 100×(e^β−1)%"; log-log = elasticity "β% per 1%"; linear-log "β/100 units per 1% increase".
- Dummies: interpretation relative to the stated omitted category; in log-y models with |β|>0.1 use 100×(e^β−1)% for exact effect.
- OVB direction claims must argue BOTH parts (sign of omitted's effect on y × sign of correlation with included regressor).
- ch17 only: FE removes only time-invariant heterogeneity; RE requires effects uncorrelated with regressors; panel inference should cluster by unit; spurious-regression/stationarity caveat before levels-on-levels time-series regressions.
- Test language: "fail to reject", never "accept H₀"; p-value = probability under H₀, not P(H₀ true).

## Lens B — Code implementation
- SE type must match prose claims. Prose says robust ⇒ fit has `vcov='HC1'`; cluster ⇒ `vcov={'CRV1': ...}`. A silently-iid fit under robust-claiming prose = error.
- No statsmodels kwargs/credit where pyfixest does the work (`cov_type=` → `vcov=`; "statsmodels" credited for estimation → pyfixest).
- Manual dof correct (s_e uses n−k; manual t/F correct); CI levels match prose (ppf(0.975) for 95%).
- Prediction interval formula has the "1 +" term iff prose says individual outcome; CI-for-mean lacks it.
- Simulations must be seeded wherever prose hand-types their numeric results; otherwise prose must say results vary.
- Cells students run in Colab must actually run top-to-bottom: flag `#| eval: false` cells that would error in Colab (missing upstream definitions) and code referencing variables/columns that don't exist (check dump).

## Lens C — Results/numbers (cross-check vs execution dump)
- A prose number is CORRECT iff it equals the executed value rounded to the precision displayed (0.617453 → "0.62" ✓ "0.617" ✓ "0.618" ✗). Every occurrence of the same quantity must agree at the coarsest shared precision. Canonical precision: R² 3 dp, money whole dollars with commas, coefficients/t-stats 2 dp.
- Check EVERY specific number in markdown prose, hand-typed tables, Key Concept callouts/blockquotes, exercises with stated answers, and the Key Takeaways cheat-sheet comments. Recompute derived claims ("X times wider", "≈9% of average price") — don't eyeball.
- "Roughly/approximately X" is acceptable within 5% of truth; beyond → finding.
- Hand-typed tables: keep short teaching/preview tables that precede/annotate live output (values must sync exactly); zero-annotation duplicates of adjacent `.summary()` output → propose deletion (if >10 rows, action=report).

## Lens D — Interpretation
- Units correct and consistent (dollars vs thousands; per-sqft vs per-100-sqft).
- Headline coefficients discussed for BOTH magnitude and significance.
- Causal discipline: "associated with" in observational settings; causal verbs only for RCT/IV/DiD/RD with a design sentence. Existing careful language is good — flag gaps, don't rewrite what works.

## Lens R — Readability
- Split a code cell only if >45 lines AND ≥2 independently interpretable outputs (two separate figures; load+clean+model each printing). A cohesive multi-panel figure is ONE output — don't split; propose per-panel banner comments.
- Every non-Setup code cell should have ≥1-sentence markdown lead-in (what it does + what to look for in the output) and an interpretation after notable output. Missing → finding with proposed text.
- Comment house style: banner first line (`# Table 7.1 - Basic regression` / `# 7.1 Example: ...`), stanza comments, sparing inline arg comments. Under-commented cells → propose comments in this style.
- NEVER touch `#| code-fold: true` Setup cells. Net cell-count change per chapter ≤ ±4. No new imports.

## Lens F — Format (normalization table; propose exact old→new)
| Rule | Applies to |
|---|---|
| Section headers `## N.M: Title` → `## N.M Title` (remove colon ONLY; words verbatim) | ch08, ch10, ch11, ch12, ch14, ch15, ch16, ch17 |
| KEEP ch16 merged `16.2-16.4` heading and ch17 starting at 17.2 (deliberate AED alignment) — only colon→space | ch16, ch17 |
| ch17 duplicate `Key Concept 17.10`: L1848→17.11, L1907→17.12 (web-app checked: safe) | ch17 |
| `### Exercise N:` H3 → `**Exercise N: Title**` bold | ch04 |
| Case-study wrap-up header "What You've Learned..." → H4 `####` | ch02, ch03, ch05, ch09 (H3→H4) |
| `### **Bold Title**` → strip bold markers, words verbatim | ch13 |
| Redundant `**Key Takeaways:**` bold line right under `## Key Takeaways` → delete | ch07, ch09 |
| Missing `**Next Steps:**` block (3–5 bullets, ch01 style, end of Key Takeaways) → propose text | ch04, ch05, ch06, ch10, ch11, ch12, ch16, ch17 |
| "Dataset(s) used": grammatical agreement (singular iff one dataset) | all (ch01/10/11 singular is correct) |
| Exercise counts (8/7/6) — leave; do NOT propose changes | all |
| ch00 `title: Untitled` → proper title | ch00 |

## SE-convention policy (AED: robust taught in ch07, default from §12.2)
- ch01–06, ch10: classical fine. If prose draws a significance conclusion from an iid fit, propose ONE labeling/softening sentence, not a refit.
- ch09, ch11: AED-faithful classical. Propose ONE sentence per chapter at the first inference discussion: classical SEs used as AED does before Ch 12; §12.2 introduces robust SEs, preferred in practice. NO refits.
- ch08: prose quotes iid output → labeling sentence; prose CLAIMS robust but code is iid → align code to prose + flag affected numbers.
- ch12–17: silently-iid fit that prose draws inference from → propose refit `vcov='HC1'` (ch17 panel contexts: cluster by unit) + list every prose number that will change. Mechanics-only iid fits (pure coefficient/prediction demos) → leave. If the refit would FLIP a stated significance conclusion → action=report with both numbers.

## Fix vs report boundary
action="fix" iff ground truth computable/citable AND pedagogy + section numbering preserved AND no stated conclusion flips. action="report" for: conclusion flips, multiple defensible conventions, structural changes beyond sentence scope, plausibly-intentional AED adaptations, >10-row duplicate tables.

## Pre-verified seed findings (include in your output for your chapter, marked confidence=high, evidence="pre-verified by execution")
- ch05: s_e $23,162 → $23,551 at L158, L795, L819, L824, L1038 (truth 23,550.66); L1450 R² 0.618 → 0.617.
- ch07: L97 s_e $23,162 → $23,551; L206 "(in thousands of dollars)" → "(in dollars)"; L1636 & L2431 statsmodels credited for estimation → pyfixest; L2543 `cov_type='HC1'` → `vcov='HC1'`.
- ch12: KC block L101–126: s_e ≈$90,000 → $23,551; 95% PI [$180k,$380k] → [$213k,$312k] at size 2,000; "three to four times wider" → about five times (5.25×); CI at 2,000 sqft = [$253k,$272k].
- ch17: duplicate Key Concept 17.10 (keep L1756; L1848→17.11; L1907→17.12).
- ch09: (a) Tasks 3/4/5 cells at L1122/L1165/L1197 are `{python}` `#| eval: false` → convert to plain ```python fences (Tasks 1/2 pattern); loader cell L1014 → remove `#| eval: false` so data_cc loads in Colab and the book; (b) prose says columns `rk`/`hc` but actual Mendez columns are `kl`/`h` (code is right, prose wrong — dataset bullets L1011–1012 and task texts L1087/L1117/L1160/L1163); (c) L1174–1175 `['ln_rk']` → `['ln_kl']` (Task 3 defines ln_kl).

## Output format
Return findings as structured output. For each: `lines` [start,end] in the .qmd; `category` (methods|code|results|interpretation|readability|format); `severity` (error = wrong; drift = stale/inconsistent number; style); `action` (fix|report); `summary` (one sentence); `old` + `new` = EXACT text to replace and replacement (verbatim, unique enough to match exactly once in the file — include surrounding context if needed; for additive insertions, `old` = the anchor text and `new` = anchor + inserted text); `evidence` (executed value from dump / computation / AED citation / rule from this brief); `confidence` (high|medium|low). Do not report the absence of problems; only findings. Quality over quantity — every finding must be defensible, but be EXHAUSTIVE on numbers (Lens C): every hand-typed number gets checked.
