# Remediation Brief — actioning the 191 judgment-call items (Phase 2 of the campaign)

You are the FIXER for one chapter. The author has approved actioning ALL report items per the recommendations in `JUDGMENT_CALLS_REPORT.md`. Produce a reconciled, exact-once edit-set to `log/campaign_audit_202607/patches/{ch}_remediation.json`, then validate it with `apply_edits.py --dry-run`. READ-ONLY on the repo except writing your patch file.

## Read first (in order)
1. `log/campaign_audit_202607/JUDGMENT_CALLS_REPORT.md` — Part 1 (structural clusters) + your chapter's Part 2 block. The **recommendation** for each item is what you implement.
2. `log/campaign_audit_202607/findings/{ch}.json` — the ground-truth. For every "flip"/"re-sync" item, the correct numbers are in the finding's `evidence` and `verify_note`. USE THESE VALUES. Do not recompute unless you must (you may run read-only Python in `.venv` to confirm).
3. `log/campaign_audit_202607/conventions.md` — number precision, format targets, house style.
4. `notebooks_quarto/{file}.qmd` — CURRENT source (already has the campaign's committed fixes). Your `old` strings must match THIS file exactly once.
5. `log/campaign_audit_202607/exec/{ch}_outputs.txt` — executed output dump for cross-checking.

## Which items to action
- Implement the item's **recommendation**. Where the report says "leave as-is / defensible / low-priority-skip / optional", DO NOT edit — skip it (record in `excluded`).
- Where the report gives a recommendation with a specific target (numbers, wording, code), implement exactly that.
- For low-confidence items the report says to prefer a superseding fix, implement the superseding one only.

## The five edit kinds (all encoded as exact-once text edits for apply_edits.py)
1. **Number re-sync / prose rewrite:** `old` = exact current text, `new` = corrected text using the findings' ground-truth numbers. For conclusion flips, rewrite the claim to match executed reality (e.g. ch17: "clustering widens the SE ~1.8× but the effect stays significant", NOT "complete reversal").
2. **Code-line fix:** `old` = exact code line(s), `new` = fixed. E.g. `nlargest(5,'residual')`→abs-based; `pd.cut(bins=3)`→`pd.qcut(...,q=3,...)`; `replace=False`→`replace=True`; bare mid-cell `df`→`display(df)`; statsmodels scaffolds→pyfixest `wald_test`/`feols` idiom; ch11 `model._f_statistic`→a classical-F helper computed from `model._r2` and dof, applied at EVERY site listed in the finding (define the helper once in the relevant cell, reuse).
3. **Cell insertion / RESTORE (ch12 §1, ch06 §3):** `old` = the exact stub header + its following prose anchor, `new` = same anchor text with a new ```` ```{python} ```` cell inserted at the correct spot. LIFT the code from that chapter's own cheat sheet (the report cites the exact STEP and line range), adapt variable names to the body's, and FIX any stale hardcoded numbers in the template to executed truth. The restored cell MUST run top-to-bottom using variables already defined earlier in the chapter. After you draft it, the driver will execute it — but you must reason that it runs and that its output will match the numbers the interpreting prose quotes (re-sync that prose too if needed, same edit-set).
4. **Block move:** encode as TWO edits — delete at source (`old` = the block incl. surrounding blank lines, `new` = "" or a single newline) and insert at target (`old` = target anchor, `new` = anchor + block). Ensure both `old`s match exactly once and the two spans don't overlap.
5. **Cell split:** `old` = the one large cell body (or the fence-delimited region), `new` = first half + closing fence + a one-sentence markdown lead-in + opening fence + second half. Keep both halves runnable.

## Hard rules
- Never change heading WORDS (web-app deep links depend on them). Renaming a heading = report-only unless the item explicitly authorizes it (e.g. ch11-F31 pyfixest title — the report says needs owner sign-off → SKIP, leave for author).
- ch16 merged `16.2-16.4` heading: NO edit (keep).
- Use `display()` for mid-cell tables; `print()` for scalars. No new imports beyond what the chapter already imports, EXCEPT where a restore needs `statsmodels`/`scipy` that the chapter already imports in Setup (check).
- Every `old` must match the CURRENT file exactly once — read the file to get exact whitespace. Edits must be non-overlapping.
- Preserve section numbering. The ±4-cell budget is LIFTED this phase (restorations add cells) — but don't add gratuitous cells.

## Chapter-specific must-dos (from the report; cross-check finding IDs)
- **ch11:** classical-F helper replacing `_f_statistic` at F31/F32/F34/F35/F36/F37/F39/F46/F47; fix the L571 `wald_test` restriction (F33); CS1 loader `rk/hc`→`kl/h` (F38); make the F-dist figure caption conditional (F35/F47); reflow §11.3–11.7 interpretation blocks after their cells (F59–F66); merge/trim F68; delete/keep F67 empty cell (delete). SKIP F31-heading-rename (needs sign-off) unless it's the wald_test title fix that keeps words → then keep.
- **ch10:** centered VIF via `add_constant`, report non-constant VIFs (F01/F36/F37); reframe Exercise 5 table as an explicitly hypothetical severe-collinearity scenario (F02/F31); AIC/BIC helper `n·ln(RSS/n)+n(1+ln2π)+2k` at the 5 sites (F22); CS1 loader fence `python`→`{python}` (F32); sync outline punctuation (F68).
- **ch12:** restore SE-ratio (cheat STEP3 L1252–1259), CI-vs-PI plot (STEP4 L1265–1299), HAC (STEP5 L1302–1323), power-curve (STEP6 L1336–1364) cells under their existing headers; re-sync the stale numbers in those blocks ($280k→$262,559; CI [$253k,$272k]; PI [$213k,$312k]; s_e $23,551; ratio ≈5.25×); dropna() in ACF/plot_acf (F49/F55, lag-1≈0.866); reconcile HAC lag 4 vs 5; mid-cell display() (F70/F71/F72); CS2 PI redesign via `pred ± t·s_e` (F21/F26/F27); precision claim (F60); move bootstrap/Type-I blocks (F76/F77); fill/convert empty cells (F74/F75).
- **ch06:** restore population/sample regression + Monte-Carlo + manual-SE cells (cheat STEP4 L1004–1022 for MC) under Figure 6.2 headers; DELETE the 1880-census references (F01/F25/F36/F40/F46); `replace=True` in Task 3/5 (F05/F39); move F47 interpretation after its cell; fix Panel A/B heading level (F42).
- **ch17:** rewrite the "complete reversal" false claims → "widens SE ~1.8×, stays significant" (F01/F15/F16/F30/F31), FE "precisely estimated" (F02/F24/F32/F33), re-sync SE tables (F14/F17); two-way clustering VARIANCE formula (F04); logit mid-cell `print()`/`display()` (F08); re-sync ADL/AR KC + R² table signs/values (F25/F26/F27/F28); expand Next Steps (F47).
- **ch08:** rewrite infant-mortality as sig-under-classical-not-robust (F02/F03/F27/F53); add robust-fit cells under the 3 empty "…with Robust Standard Errors" headers (F04/F05/F70/F71/F72/F93/F94); Okun direction reversal (F52); Exercise 3 betas 0.75/1.07 or keep hypothetical (F51 — keep hypothetical per report).
- **ch14:** gender-gap suppression/widening rewrite (F01/F02/F13/F14/F15/F19/F20/F21); worker-type signs inverted (F16/F22); `anova_lm`→`wald_test` scaffold (F08). Leave F17/F18 (defensible).
- **ch15:** MEM=AME rewrite (F01/F15/F31); std-coef ranking correction (F17/F22/F30/F33); age-coef drift $525 (F27), ~0.8% (F28); interaction-insignificance reframe (F02/F16/F23/F29/F32).
- **ch16:** endogeneity example `democracy~growth` (F02); CS1 bullets `kl/h/GDPpc/TFP` (F07); CS2 `OLSInfluence` scaffold→smf.ols pattern (F08); reframe §16.6 AR(1) block to the simulated data ρ≈0.80 (F22/F26); intercept-VIF line (F15); soften robust-SE "20–40%" → "modest/mild" (F23/F28).
- **ch05:** `qcut` terciles (F19/F44); combined KC 5.9 units+notation (F07 merged w/ F38 already applied — check current text); std-resid convention (F15 — divide by s_e per report? report says convention choice; apply s_e for consistency); relabel/abs outlier table (F45); merge §5.2 wrap-ups (F53); move §5.7 uncertainty block to §5.8 (F60).
- **ch13:** OVB "slope not correlation" (F03); CRS test → HAC Wald OR update prose 0.636→0.663 (F04/F12 — prefer HAC Wald to preserve prose); Phillips significance caveat (F43); split the 2 long cells (F44/F45).
- **ch07:** CS2 slope β₁→β₂ (F07); Exercise 8 self-consistent averages (F41); move "Artificial Data" heading+lead-in to its cell (F48/F66); relocate robust-SE lecture to §7.7 (F49); re-indent 1-space sub-bullets to 4 (F96); computed-t formula harmonize (F06 — low priority, do the 3-site harmonization). Leave nothing that needs heading-word change beyond F97 task-heading demotion (do F97).
- **ch03:** harmonize SE definition σ/√n vs s/√n (F11); reseed/enlarge weighted-mean demo (F21); move sim-interpretation block to §3.6 (F27/F29); `replace=True` (F09/F14/F23).
- **ch09:** R² caveat (F10, note stale `old`—use actual L760 text); classical-SE sentence at first inference (F38); Task 2 `100×(e^β−1)` or sub-question (F60).
- **ch02:** region_mapping task uses existing column (F18); matplotlib `vert=`/`labels=`→`orientation=`/`tick_labels=` at the 5 sites (F23); variance-stabilization reframe (F54); Exercise 4 exact-log enhancement (F13 — optional, do it).
- **ch04:** Exercise 8(d) null μ=55→μ=50 for Type-I ≈0.05 (F26).
- **ch01:** F-statistic bullet (F03 — replace with RMSE line); R² analogy ≈62% (F20); significance sentence pointing to Ch7 (F21).
- **ch00:** Linearmodels→pyfixest at 3 sites (F06); "Gemini PRO"→"Gemini Pro" (F08).

## Output
Write `patches/{ch}_remediation.json` = array of `{finding_id, old, new, count}`. Then run `python3 log/campaign_audit_202607/scripts/apply_edits.py notebooks_quarto/{file}.qmd log/campaign_audit_202607/patches/{ch}_remediation.json --dry-run` and iterate until it prints DRY-RUN OK. Return: ch, edit_count, excluded_count, dry_run_ok, whether it adds code cells (restore/split — flag high-risk), a commit-message-body summary, and notes (esp. which restored cells produce which numbers, and any item you left for the author with the reason).
