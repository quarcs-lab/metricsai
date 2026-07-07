# Judgment-Call Report — metricsAI Audit Campaign (202607)

## What this report is

This document lists the **191 audit findings that were deliberately NOT auto-fixed** because each needs an author decision, not a mechanical edit. A finding lands here (rather than in a committed patch) when it meets one of four gates: (1) the correct fix would **flip a stated significance or qualitative conclusion**; (2) there are **multiple defensible conventions** and picking one changes displayed output; (3) the repair is a **structural change beyond sentence scope** (adding/deleting code cells, moving 40–260 line blocks, renaming heading words); or (4) the issue is a **plausibly-intentional AED adaptation** where "wrong" and "as-designed" are both readable. Everything clear-cut — number resyncs, colon→space heading normalization, robust-SE refits that did *not* flip conclusions, dedup of redundant blocks, list-spacing, Next-Steps blocks — is **already committed per-chapter** (commits `def9ccb`…`6d71b13`, 756 edits, one commit per chapter; see `STATE.md`). Read Part 1 first (the big-ticket structural calls), then Part 2 (the per-chapter remainder). Each accepted item can be applied as an isolated follow-up edit.

---

# PART 1 — Top priority / structural decisions

These nine clusters carry most of the pedagogical risk. Each states the defect, why it was not auto-fixed, the options, and a recommendation.

---

## 1. ch12 — orphaned prose interpreting figures/tables/computations that no code cell produces

**What's wrong.** Sections 12.2, 12.3, 12.5 and 12.7 contain large interpretation blocks (and two stub section headers) that walk readers through outputs the chapter never generates. The executed notebook jumps straight past them (exec dump `ch12_outputs.txt`). Specifically:

- **SE-ratio comparison table** — §12.2 says "Let's systematically compare the standard errors" and the interpretation repeatedly cites "the SE Ratio column," but only two bare `.summary()` outputs exist; no ratio table is ever built. `ch12-F28`, `ch12-F50`, `ch12-F56`, `ch12-F64` (L291–325).
- **CI-vs-PI two-panel figure + "Prediction at Specific Values" + "Manual Calculation of Standard Errors"** — §12.3 interprets "the two panels" (blue PI / red CI), a 2,000-sq-ft prediction with intervals, and a manual-SE walk-through; the only code is the simple regression. The two announcing headers (L656 "Prediction at Specific Values", L660 "Manual Calculation of Standard Errors") are **stubs with no code**. `ch12-F30`, `ch12-F52`, `ch12-F53`, `ch12-F58`, `ch12-F66`, `ch12-F67` (L491–662).
- **HAC three-way comparison** — "Interpreting HAC Standard Errors" compares default / HAC-lag-0 / HAC-lag-5 SEs for mean GDP growth; no HAC SE is computed anywhere in the body (and the cheat-sheet uses lag 4, not 5). `ch12-F29`, `ch12-F51`, `ch12-F57`, `ch12-F65` (L396–438).
- **Power curve "Figure 12.3"** — "Reading the Power Curve" interprets Figure 12.3 feature-by-feature, and §12.7's "Illustration: Power of a Test" (L1160) promises the visualization; no power-curve cell exists (and this block sits in §12.5, two sections from its home). `ch12-F31`, `ch12-F54`, `ch12-F61`, `ch12-F68`, `ch12-F69` (L943–1162).

**Why not auto-fixed.** The remedy is either adding ~4 code cells or deleting/rewriting ~200 lines of prose — both structural, both beyond the sentence-level patch scope, and net cell additions would blow past the ±4-cell/chapter budget. Locked convention (`conventions.md` §"Structural issues that are REPORT") flags exactly this.

**Options.** **(A)** Restore the missing code cells. The evidence strongly suggests these cells existed and were lost in the statsmodels→pyfixest migration: the prose numbers are internally consistent, and the chapter's own **non-executed cheat sheet already contains ready-made templates** for every one — STEP 3 (SE-ratio loop, L1252–1259), STEP 4 (CI-vs-PI plot, L1265–1299), STEP 5 (HAC, L1302–1323), STEP 6 (power curve, L1336–1364), none needing new imports. **(B)** Delete the orphaned prose and stub headers, leaving a leaner chapter.

**Recommendation: Option A**, lifting the four cheat-sheet templates into the body under their existing headers. This preserves the pedagogy §12.2/12.3/12.7 were built around. Two mandatory riders: (i) the stale hand-typed numbers in these blocks ($280k point prediction, CI $250k–$310k, PI $180k–$380k, RMSE ≈$90k) must be **re-synced to executed truth** (point $262,559; CI [$253k,$272k]; PI [$213k,$312k]; s_e $23,551; PI/CI ratio ≈5.25×) — same seed error already noted in the pre-verified ch12 seed for the KC block L101–126; (ii) reconcile "HAC lag 5" prose with the rule-of-thumb lag 4. Fall back to Option B only if a shorter chapter is preferred.

**Two related empty/no-op cells (same section):** `ch12-F74` (§12.5 cell prints only bare outline headers "1. Gauss-Markov Theorem:" … with nothing under them, L1043) and `ch12-F75` (§12.4 cell is a banner + one comment, zero output, L833). Delete, convert to markdown, or give real content — author's call.

---

## 2. ch12 — NaN autocorrelation: ACF/correlogram run on a NaN-containing series

**What's wrong.** The GDP-growth series `data_gdp['growth']` has 4 missing values. statsmodels `acf` does not drop them, so the autocorrelation cell **prints NaN at every lag (Lag 0…Lag 5 = nan)** and the correlogram (fed the same series) is empty — yet the code comment (L369) says "Positive lag 1 correlation suggests persistence," the printed line (L382) says "The correlogram shows autocorrelation at various lags," and KC callout L91 claims "the chapter computes a positive lag-1 autocorrelation." `ch12-F49` (L365–369), `ch12-F55` (L91).

**Is it fixable?** Yes — trivially. Passing `data_gdp['growth'].dropna()` to `acf`/`plot_acf` yields lag-1 ACF = 0.866 (positive), which makes the prose directionally correct and matches what the interpretation already claims.

**Why reported, not auto-fixed.** Three reasons: (i) it changes executed output, crossing the fix/report boundary the campaign locked for conclusion-adjacent code; (ii) it interlocks with the missing HAC computation (item 1: `ch12-F29/F51/F57`) — the same NaNs would break the cheat-sheet HAC fit at L1318 — so dropna and the HAC cell should be fixed together; (iii) the exact lag-1 value the prose quotes must be re-verified against the fixed output. **Recommendation: apply `dropna()` in the acf/plot_acf calls, add the HAC cell (item 1), then re-sync any quoted lag-1 figure.** Low risk, high value.

---

## 3. ch06 — orphaned prose for missing cells + a phantom "1880 Census" example

**What's wrong.** ch06 has **only 5 executable cells** (exec dump), but five interpretation sections analyze specific numeric outputs that no cell produces, and the chapter three times promises a second example that does not exist:

- **Missing regression/figure cells** — "Figure 6.2 Panel A/B" headings and their interpretation blocks discuss a population regression (intercept 1.0000, R²=1.000) and a sample regression (ŷ=2.81+1.05x, R²=0.769); a 1,000-run Monte Carlo (means 0.9960/1.9944, SDs 1.2069/0.3836) with described histograms ("green line", "red curve"); and a "Manual Computation of Standard Errors" example that even claims "our manual calculations match the model output exactly" (L737) — none of which is computed or plotted. `ch06-F02`, `ch06-F03`, `ch06-F04`, `ch06-F22`, `ch06-F23`, `ch06-F24`, `ch06-F34`, `ch06-F35`, `ch06-F41`, `ch06-F42`, `ch06-F43`, `ch06-F44`, `ch06-F45`. (Audit recomputed the narrated numbers as internally correct — the cells were written, then lost.)
- **Phantom census example** — §6.2, the datasets bullet (L50), and Key Takeaways (L889, "Samples from 1880 Census (1.06 million males aged 60-70)") all reference an 1880 U.S. Census finite-population example that appears nowhere. `ch06-F01`, `ch06-F25`, `ch06-F36`, `ch06-F40`, `ch06-F46`.

**Why not auto-fixed.** Same class as ch12: add ~5 cells (over budget) vs. delete/rewrite prose + three references. Structural.

**Options / recommendation.** For the **regression/MC/manual-SE blocks (A)** restore the cells (the cheat-sheet STEP 4 at L1004–1022 is a ready MC template) — recommended, since the prose is numerically correct and the chapter's core lesson (sampling distribution of OLS) is otherwise never shown to Colab readers. For the **1880 Census example**, recommend **deleting the three references** rather than sourcing AED census microdata — this is a plausibly-intentional AED adaptation where the example was dropped but the mentions weren't cleaned up. Also note one ordering issue: `ch06-F47` (interpretation of the three sample regressions at L350–382 sits *before* the cell that generates them at L392) and a heading-level slip (Panel A is H3, Panel B is H4, in `ch06-F42`).

---

## 4. ch11 — the `_f_statistic` code-bug cascade (executed "Fail to reject" contradicts prose "Reject")

**What's wrong.** `model_full._f_statistic` in pyfixest returns the **joint Wald statistic including the intercept**, not the classical overall F — and one `wald_test` call at L571 (whose restriction matrix `[[0,0,0,0,0,1,0]]` selects `age`, not `size`) **overwrites** it to 1.5069 for all downstream cells. As executed, this makes the chapter visibly contradict itself:

- Overall F-test cell prints **F=1.5069, p=0.222, "Fail to reject H₀"** while the prose says F=6.83, p=0.0003, "Reject." `ch11-F32`, `ch11-F46` (L676–700).
- Manual verification cell prints "From model output: 1.5069 / **Match: False**" twice. `ch11-F34` (L828–838).
- F-distribution figure caption prints "The observed F-statistic (1.51) **exceeds** the critical value (2.55)… reject" — false, 1.51 < 2.55. `ch11-F35`, `ch11-F47` (L1197–1219).
- Model-comparison table prints 1707.27 / 1097.69 / 1.5069 vs. correct 43.58 / 21.03 / 6.83. `ch11-F36` (L1066).
- Cheat-sheet STEP 5 and CS1 Task 4 print the same wrong statistics (435.40; 39204.25). `ch11-F37` (L1384), `ch11-F39` (L1645).
- The `wald_test` restriction targeting the wrong coefficient. `ch11-F33` (L571).

**Plus a hard crash:** CS1 references Mendez columns `rk`/`hc` that don't exist (actual: `kl`/`h`), so the loader raises `KeyError` and none of CS1 runs. `ch11-F38` (L1572+, spans loader/formula/CI/t-test/bullets).

**Why not auto-fixed.** The executed conclusion currently flips the stated prose conclusion, and the correct fix (compute F classically from `model._r2`, e.g. `(R²/(k-1))/((1-R²)/df)`, and repair the wrong-column loader) spans 6+ cells — structural, conclusion-touching.

**Recommendation.** **Fix the code** (`_f_statistic` → classical F everywhere; fix the CS1 column names to `kl`/`h`; make the figure-caption print conditional on `f_stat > f_crit`). No qualitative conclusion actually flips once corrected (the model *is* jointly significant); this restores agreement between output and prose. This is the single highest-value code repair in the campaign. Treat as one coordinated edit.

---

## 5. ch10 — VIF miscomputation (uncentered vs. centered) cascade

**What's wrong.** The §10.8 VIF cell passes the design matrix to statsmodels `variance_inflation_factor` **without an intercept column**, producing uncentered VIFs (max 57.82) and printing "Warning: Maximum VIF = 57.82 indicates multicollinearity issues." This contradicts the chapter's own glossary claim (L148) that the six Davis predictors "show only moderate VIFs" and misapplies KC 10.8's VIF>5/>10 rule. Correct **centered** VIFs (with `add_constant`) are all below 1.75 → no multicollinearity. `ch10-F01`, `ch10-F36`, `ch10-F37` (L592–612, L148). The buggy values are echoed verbatim in **Exercise 5's hand-typed table** (40.1/57.8/34.7/21.0), `ch10-F02`, `ch10-F31` (L978–993).

**Why not auto-fixed.** Fixing the code **flips the cell's stated conclusion** (warning branch → "no serious multicollinearity") and **invalidates Exercise 5's premise**, which must be resolved together — conclusion-touching, multi-location.

**Options.** (A) Add the constant, report VIFs only for non-constant regressors (centered, correct), and either reframe Exercise 5 as an explicitly *hypothetical* severe-multicollinearity scenario or regenerate it; (B) reword the L148 glossary claim to match the buggy displayed output. **Recommendation: Option A** — the correct econometrics is that the Davis predictors are *not* collinear (pairwise r≈0.5, all coefficients estimable), so the code is the thing that's wrong; relabel Exercise 5 as hypothetical to preserve the teaching drill.

---

## 6. Significance / conclusion flips (robust & clustered SEs) — ch17, ch08, ch12

Per the locked SE policy (`conventions.md` §SE convention), silently-iid inference fits were refit with `vcov='HC1'` (cluster in ch17) **only when the conclusion did not flip**; every case where it *does* flip is reported here for an author call. These are the highest-severity interpretation defects in the campaign.

### ch17 — the chapter's headline lesson ("clustering/FE kills significance") is empirically false in this dataset
The prose repeatedly claims cluster-robust or fixed-effects SEs render the wins coefficient insignificant, but the executed fits are highly significant:

- **Pooled OLS**: prose "default t=3.00 / cluster t=1.38, p=0.17 — Not significant! **Complete reversal of inference!**"; executed cluster t=3.54, p=0.0014 (default t=6.42), cluster/default ratio only 1.81×. `ch17-F01`, `ch17-F15`, `ch17-F30` (L528–585), and the NBA-example restatement `ch17-F16`, `ch17-F31` (L574–585).
- **Fixed effects**: prose "Surprisingly not significant" (t≈1.25, p≈0.21), "imprecisely estimated," "need longer panel"; executed FE t=5.35, p<0.001, within-R²=0.185. `ch17-F02`, `ch17-F24`, `ch17-F32`, `ch17-F33` (L780–798).
- The stale "Typical Results" tables carry the wrong SEs/R² feeding these claims. `ch17-F14` (L445), `ch17-F17` (L655).

**Recommendation:** rewrite so the lesson becomes "clustering widens the SE ~1.8× but the effect stays significant" and "FE is precisely estimated here" — i.e., keep the pedagogy about *why* clustering matters, drop the false "reversal." (The audit supplies the corrected numbers.) This is the most important interpretation fix in ch17.

### ch08 — infant-mortality significance genuinely flips under robust SEs
Prose: "highly statistically significant (t≈−5.9, p<0.001)"; executed iid t=−2.33 (p=0.027, sig at 5%), **HC1 t=−1.35 (p=0.188, NOT significant)** — and KC 8.2 directly below calls robust SEs "essential." `ch08-F03`, `ch08-F27`, `ch08-F53` (L358). Life-expectancy weakens but survives: prose p<0.001 vs HC1 p≈0.023 (still sig at 5%). `ch08-F02` (L269). **Recommendation:** rewrite the infant-mortality paragraph to present it as significant under classical SEs but insignificant under the robust SEs the chapter recommends; fix the stale t≈−5.9/≈5.3/≈21.5/≈3.4 numbers throughout (see also the empty robust-SE headings, item below).

**Empty "…with Robust Standard Errors" section headers** (ch08): three H3 headers promise robust results and deliver nothing — CAPM (`ch08-F04`, `ch08-F70`, `ch08-F93`, L711), Okun (`ch08-F05`, `ch08-F71`, `ch08-F94`, L886), life-exp (`ch08-F72`, L269). Here HC1 refits do **not** flip conclusions, so the recommendation is to **add the robust-fit cell** under each (heading words are load-bearing — do not delete), correcting the adjacent stale t-stats.

### ch12 — "multiple regression provides more precise predictions" is contradicted by its own numbers
Printed conclusion is false here: the six-regressor model's RMSE ($24,936, df=22) is **larger** than the simple model's s_e ($23,551, df=27) because the df penalty outweighs the R² gain (0.617→0.651), so individual-prediction precision is slightly *worse*. `ch12-F60` (L704). **Recommendation:** replace the sentence with the honest observation that adding weak predictors need not improve individual-prediction precision.

### Related conclusion/significance flips (not robust-SE, but same "conclusion could flip" class)
- **ch14 — gender-gap direction reversed (suppression).** Prose says controlling for education *shrinks* the gap to ≈−$10k (and further to −$5k/−$8k); executed Model 2 gender coefficient is **−$18,258**, *larger* than the −$16,396 unconditional gap (women average more schooling → suppression). No fitted model yields −$5k/−$8k. `ch14-F01`, `ch14-F02`, `ch14-F13`, `ch14-F14`, `ch14-F15`, `ch14-F19`, `ch14-F20`, `ch14-F21` (L135–136, L495–498, L518–519). **Recommendation:** rewrite the model-evolution narrative and KC example to describe the *widening/suppression* the data show. Students meet this false claim twice (narrative + KC), so it is high-priority.
- **ch15 — "returns to education rise 4–5× with age" rests on an insignificant interaction.** The `age×education` coefficient is +$29/yr with **t=0.52, p=0.605**; the real ME-of-education ramp is 1.17× ($5,241→$6,112), not the "$2,500→$11,500, 4–5×" claimed, and "education's effect is age-dependent" is drawn from a joint F-test that only shows education matters *at all*. `ch15-F02`, `ch15-F16`, `ch15-F23`, `ch15-F29`, `ch15-F32` (L106, L121, L883–948). **Recommendation:** reframe §15.5 and the MER glossary example around the insignificant interaction; drop the age-dependence policy claims.

---

## 7. ch16 — merged heading "16.2–16.4" (keep AED-faithful vs. split into three)

**What's wrong (per the checker, not per the audit findings).** Sections 16.2, 16.3 and 16.4 are deliberately merged under one heading to mirror AED's structure; this is a **locked convention** (`conventions.md` L20: "KEEP ch16 merged 16.2–16.4 … deliberate AED alignment"). The consequence is that the chapter-standard template checker now flags a **section-number gap** as a structural defect.

**Options.** (A) **Keep merged** — faithful to AED, which the chapter intentionally follows; accept the checker's false-positive gap. (B) **Split into 16.2 / 16.3 / 16.4** — makes the checker green but diverges from the source text's organization and changes anchors.

**Recommendation: keep merged (A)** and instead teach the checker to accept the documented gap (or annotate it), consistent with how ch17's deliberate start-at-17.2 is already handled. The tradeoff is purely "AED fidelity vs. a green automated check"; fidelity was the locked call, and nothing in the reader-facing content is wrong. (No specific `chNN-F##` finding covers this — it is a convention decision surfaced by the template checker; flagged here because it looks like a defect in the structural scan.)

---

## 8. ch05 — "terciles" mislabel: `pd.cut` (equal-width) vs. `pd.qcut` (equal-frequency)

**What's wrong.** Case Study 2 Task 1 instructs students to bin `imds` into "three equal-frequency groups … (terciles)" and the comments say "Bin imds into terciles," but the code uses `pd.cut(bins=3)` (equal **width**), producing groups of **170 / 157 / 12** of 339 — nowhere near terciles (~113 each). `ch05-F19`, `ch05-F44` (L2058–2086).

**Why not auto-fixed.** Two defensible fixes that change different things: (A) switch code to `pd.qcut(q=3)` — statistically matches the "terciles" label but **changes every crosstab number** downstream; (B) keep the code and reword prose/comments to "three equal-width groups," dropping "terciles."

**Recommendation: Option A (`qcut`).** The surrounding task compares group sizes, and the equal-width binning yields a degenerate 12-municipality "High" group that undercuts the exercise; equal-frequency terciles are what the task's stated concept intends. Accept the crosstab renumber. Choose B only if minimizing executed-output churn outweighs conceptual fidelity.

---

## 9. Finite-population correction (FPC) in Monte-Carlo sampling case studies — ch03 & ch06 (recurring)

**What's wrong.** Case-study starter code samples **without replacement** from small "populations" (N=108 countries) while the questions ask students to verify iid `σ/√n` theory. The FPC makes the empirical SE fall systematically below `σ/√n` — ~16% low at n=30, ~73% low at n=100 — so "how close is the empirical SE to the theoretical prediction?" and "verify SE decreases as 1/√n" cannot be satisfied as written. ch03: `ch03-F14`, `ch03-F23`, `ch03-F09` (L1413–1514). ch06: `ch06-F05`, `ch06-F39` (Task 3 template `replace=False` at L1331; Task 5 doubles n=50→100, nearly exhausting the population).

**Why not auto-fixed.** Two defensible conventions: (A) change `replace=False`→`replace=True` so the iid theory the hints cite actually applies (minimal, matches KC 3.10/3.11 and KC 6.10); (B) keep sampling-without-replacement and add an FPC caveat to the tasks. **Recommendation: Option A** across both chapters (one-token change per template) — it aligns the exercise with the theory being taught and is the smaller, cleaner change.

---

# PART 2 — Per-chapter remainder (grouped by theme)

Items already detailed in Part 1 are cross-referenced, not repeated. Format: `finding_id — summary (recommendation)`. Near-duplicate cross-lens findings are collapsed onto one line.

---

## ch00 — Preface (2)
- **Methods/results:** `ch00-F06` — "Modern Python Stack" credits *Linearmodels* (never imported, absent from requirements.txt) and omits *pyfixest*, the actual engine in 14 chapters; same false claim at L42 & L242 (*replace Linearmodels with pyfixest at all three sites*).
- **Format:** `ch00-F08` — "Gemini PRO" (all-caps) is nonstandard branding, 3× at L116/158/234 (*normalize to "Gemini Pro" if branding consistency wanted; low priority*).

## ch01 (4)
- **Methods:** `ch01-F03` — §1.7 tells students to read an "F-statistic (top right)" that pyfixest's summary never prints (*delete the bullet, or replace with the RMSE line pyfixest does print, or note F=t² for the bivariate case*).
- **Code:** `ch01-F12` — Setup imports pyfixest with no `!pip install`, so a fresh Colab session fails, contradicting the "no local setup required" claim at L15; project-wide across all 18 setup cells (*decide a project convention: inject `%pip install pyfixest -q` at export time or in Setup cells*).
- **Interpretation/results:** `ch01-F20` — R² analogy "roughly two-thirds" (66.7%) vs actual 61.75%, and inconsistent with the sibling panel's "about 62%" (*change to ≈62%; low priority, illustrative*). `ch01-F21` — headline slope discussed for magnitude/R² but not significance (t=6.60, p<0.001); if adding a significance sentence, point to **Chapter 7** (bivariate-regression inference), not Ch 3–4.

## ch02 (4)
- **Methods:** `ch02-F13` — Exercise 4's delta-ln approximation (50%) is far from exact (64.9%) at a 0.5 log change, with no prompt to confront the exact formula (*optional enhancement bullet; exact log is Ch9, so defensible as-is*).
- **Code:** `ch02-F18` — Task 6 tells students to hand-build a ~50-entry `region_mapping` dict, but the dataset already has a `region` column, and the hint's taxonomy/example countries ("Nigeria", "USA") don't match the data (*rewrite the task to use/validate the existing column, or keep the drill but state the column exists and fix the taxonomy*). `ch02-F23` — deprecated matplotlib `vert=`/`labels=` kwargs in 5 places (L340/1397/1765/1843/2182); break at matplotlib 3.13 (*project-wide compat decision; `orientation=` doesn't exist pre-3.10*).
- **Interpretation:** `ch02-F54` — "variance stabilization" uses SD/mean of a log variable (6%), which isn't unit-invariant, so it's not valid evidence (*reframe around "SD of logs ≈0.62 ≈ ±62% proportional spread"; also at L1000*).

## ch03 (7) — FPC items (`F09`/`F14`/`F23`) in Part 1 §9
- **Methods:** `ch03-F11` — SE definition is internally inconsistent: KC 3.4 & Key Takeaways define SE as *estimated* `s/√n`, while KC 3.10/3.11 and L645/L1010 call `σ/√n` the "standard error" (*harmonize, e.g. "SE(ȳ)=σ/√n, estimated in practice by s/√n"; needs coordinated web-app string update in ch03.js*).
- **Results:** `ch03-F21` — the weighted-mean (IPW) demo prints a "corrected" mean 5× *farther* from truth than the "biased" one (unlucky seed 42), undermining the lesson; cheat-sheet L1186–1210 replicates it (*change the seed and/or enlarge subsamples so the demo shows the intended result — changes all displayed numbers*).
- **Readability/ordering:** `ch03-F27` ≡ `ch03-F29` — the "Interpreting the Simulation Results" block sits in §3.4 but interprets the §3.6 Monte Carlo (~140 lines later), so readers meet mean 0.5004/SD 0.0887 before the sim runs (*move the 40-line block into §3.6 after the simulation cell at L852; also gives that cell its missing interpretation*).

## ch04 (1)
- **Results:** `ch04-F26` — Exercise 8(d)'s stated answer (≈0.05) is wrong: data from N(50,·) make H₀:μ=55 a *false* null, so the rejection rate is power (≈1 if var=100), not 0.05 (*either change the null to μ=50 — a Type-I simulation consistent with ≈0.05 — or keep μ=55 and restate the answer as the test's power*).

## ch05 (7) — tercile items (`F19`/`F44`) in Part 1 §8
- **Methods:** `ch05-F07` — KC 5.9 writes the slope as β₁ contradicting the chapter's b₂=slope / β₁=true-intercept convention; **and** its "in thousands of USD" is a 1000× units error (Mendez data are raw 2011 USD) (*apply the combined correction from the verify_note: b₂, "in 2011 USD," "per additional dollar" — merge with F38*).
- **Code:** `ch05-F15` — standardized residuals divide by `_u_hat.std()` (ddof=0, $22,724) not the chapter's s_e=$23,551 (n−2); obs-27 value shifts 2.11→2.04 but the flagged set is unchanged (*convention choice — divide by s_e for consistency, or keep the z-score standardization; no conclusion flips*).
- **Results/interpretation:** `ch05-F45` — the outlier table is labeled "Top 5 largest residuals (in absolute value)" but `nlargest(5,'residual')` sorts *signed* values, silently dropping obs 4 (residual −$45,436) (*relabel to "most positive residuals," or sort by `.abs()` — the latter changes displayed rows*).
- **Readability/ordering:** `ch05-F53` — two overlapping wrap-up blocks at end of §5.2 restate the same three limitations (*merge/keep one*). `ch05-F60` — "Understanding Prediction Uncertainty" block (§5.7) discusses the $262,559 prediction and PIs that §5.8 introduces (*move into §5.8 after the prediction cell*).

## ch06 (21) — nearly all in Part 1 §3 (orphaned prose + phantom census + FPC)
- **Remaining ordering/format:** `ch06-F47` — interpretation of the three sample regressions (L350–382) precedes the cell that generates them (L392) (*move after the visualization cell*). Heading-level slip (Panel A H3 vs Panel B H4) noted in `ch06-F42`.

## ch07 (8)
- **Methods:** `ch07-F06` — the computed-t formula writes population `σ_u` in the denominator, conflating the Z and T constructions (*genuine looseness, but a single-site swap desyncs L314/L1166 — harmonize all three sites or leave all as the theoretical formula; low priority*). `ch07-F07` — Case Study 2 calls the slope "β₁" while the rest of the chapter reserves β₁=intercept, β₂=slope (spans task prose + code across L2491–2628) (*rename CS2 slope to β₂ for consistency*).
- **Interpretation:** `ch07-F41` — Exercise 8's stated averages (x̄=10, ȳ=5) are inconsistent with its OLS output (intercept 2.5, slope 3.2): the line must pass through (x̄,ȳ), giving ȳ=34.5≠5 (*change the averages, coefficients, or units to make them consistent*).
- **Readability/format:** `ch07-F48` ≡ `ch07-F66` — "### Example with Artificial Data" heading + lead-in stranded ~100 lines before its code cell (L625 vs L727) (*move the heading+lead-in to the cell*). `ch07-F49` — a ~260-line robust-SE lecture sits in §7.5 though robust SEs are §7.7's topic; KC 7.6 sits under §7.4 (*relocate under §7.7*). `ch07-F96` — sub-bullets indented 1 space render as flat un-nested lists in 6 blocks (*re-indent to 4 spaces; visually acceptable now*). `ch07-F97` — case-study Task headings are H3 (siblings of "Case Study N") and CS2 mixes an H4; the verify script expects "#### Task N" (*coordinated demotion; web-app deep links derive from heading text*).

## ch08 (13) — robust-SE flips (`F02`/`F03`/`F27`/`F53`) & empty headings (`F04`/`F05`/`F70`/`F71`/`F72`/`F93`/`F94`) in Part 1 §6
- **Results:** `ch08-F51` — Exercise 3(a) states Walmart β=0.45 / Target β=1.25; actual dataset betas are 0.75 / 1.07 (*keep as a deliberate hypothetical, or update to 0.75/1.07; chapter never regresses these two stocks in the body*).
- **Interpretation:** `ch08-F52` — the post-2008 Okun actual-vs-predicted discussion is **direction-reversed** (actual GDP is *below* prediction 9 of 10 years after 2010, not above; 2009 is slightly over-predicted), and L1032 calls the cyan actual line "black" (*rewrite the multi-bullet block: post-2010 predictions exceed actuals*).

## ch09 (3)
- **Methods/code:** `ch09-F10` — Key Takeaway 3 presents R² model-selection without the same-dependent-variable caveat (*add the caveat; note the finding's `old` text is stale — actual L760 is "R² comparison (higher is better, but not the only criterion)"*). `ch09-F38` — add one sentence noting all fits use classical iid SEs (AED-faithful pre-Ch12) (*place at the first inference discussion in §9.3, not deep in Task 2c at L1091, so main-body readers see it*).
- **Interpretation:** `ch09-F60` — Task 2 guides `100×β₁` as the % productivity gain, but β̂≈1.18 is far outside the |β|<0.1 validity range (approx 118% vs exact ≈225%) (*add a sub-question or switch the print to `100×(e^β−1)`*).

## ch10 (8) — VIF cascade (`F01`/`F02`/`F31`/`F36`/`F37`) in Part 1 §5
- **Code:** `ch10-F22` — pyfixest `Feols` has no `_aic`/`_bic`, so the hasattr-guarded AIC/BIC columns are always NaN in §10.7, the cheat sheet, and Task 5 hints (5 locations); ground-truth Stata-formula values exist and match Exercise 4 (*add a small `n·ln(RSS/n)+n(1+ln2π)+2k` helper; mirror in cheat sheet + 2 hints*). `ch10-F32` — CS1 loader is a plain ```` ```python ```` fence, so `dat_2014` never loads in the book/Colab, unlike the ch09 convention and CS2 in this same chapter (*convert L1025 to `{python}`*).
- **Format:** `ch10-F68` — chapter-outline punctuation drifts from the load-bearing headings (colon vs hyphen, em-dash vs hyphen at L51/L55) (*sync the outline lines to the headings*).

## ch11 (25) — F-stat cascade (`F31`–`F39`, `F46`, `F47`) & CS1 crash (`F38`) in Part 1 §4
- **Methods/interpretation:** `ch11-F04` ≡ `ch11-F49` — KC 11.10 says the joint F-test shows factors matter "beyond what each contributes alone," conflating collective significance with incremental subset tests (*if edited, use F49's precise wording distinguishing joint vs subset tests; clause is defensible, low confidence*). `ch11-F53` — causal verb "adds at least $36 to the price" on a CI lower bound (*prefer the F03 fix already applied, which supersedes this*).
- **Format/code:** `ch11-F31` — heading "### Using statsmodels t_test" is wrong; the cell uses pyfixest `wald_test` and the lead-in credits pyfixest (*rename to a pyfixest wald_test title — heading words are load-bearing, needs owner sign-off*).
- **Readability (interpretation-before-output cluster — all structural block moves):** `ch11-F59` (CIs, L398 before L416), `ch11-F60` (hypothesis test, L472 before §11.4 cell), `ch11-F61` (overall + subset F-tests, L603/L650 before their cells), `ch11-F62` (SoS decomposition, §11.5 before §11.6 cell), `ch11-F63` (subset F-test, before §11.6 cell), `ch11-F64` (model comparison, before §11.7 cell), `ch11-F65` (coefficient stability, before its cell), `ch11-F66` ≡ `ch11-F99` (orphaned "### Manual F-test Calculation" heading L925 immediately followed by another H3; robust-SE interpretation precedes its cell) (*move each interpretation block after the cell it interprets — one coordinated reflow of §11.3–11.7*). `ch11-F67` — comment-only §11.1 cell renders as an empty-output cell (*delete or keep as a section marker*). `ch11-F68` — "### Economic Interpretation" (L361) largely duplicates "### Interpreting the Regression Results" (L305) (*merge/trim*).

## ch12 (29) — orphaned prose, NaN ACF, empty cells, precision flip all in Part 1 §1/§2/§6
- **Code (prediction-interval redesign):** `ch12-F21`, `ch12-F26`, `ch12-F27` — CS2 Tasks 3/4 (and L1594/L1804 templates) call `pred.summary_frame(...)`/`mean_ci_lower`/`obs_ci_lower` on an undefined `pred` using statsmodels-only API that pyfixest predictions (plain numpy arrays) lack → NameError/AttributeError; Task 4 is also internally contradictory (*redesign: approximate PI via `pred ± t·s_e` from `model._u_hat` as in §12.3; the conditional-mean CI needs `x0'Vx0` matrix algebra not taught here — rework instructions + ~15-line template*).
- **Readability (misplaced blocks):** `ch12-F76` — the ~67-line "Bootstrap Confidence Intervals" block sits under §12.4 but belongs to §12.6, where it's summarized again (*move/consolidate*). `ch12-F77` — the "Type I vs Type II Error Tradeoff" block (2×2 table) sits under §12.4 but duplicates §12.7's identical table (*consolidate into §12.7*).

## ch13 (6)
- **Methods:** `ch13-F03` — KC 13.5 says OVB = omitted coef × "correlation with the included regressor," but the bias term is β₃×γ where γ is the auxiliary-regression *slope*, not a correlation; the chapter's own formula block defines γ correctly (*reword to "slope from regressing the omitted on the included variable"; web-app ch13.js repeats the wording in EN/ES/JA → coordinate*). `ch13-F04` ≡ `ch13-F12` — the constant-returns-to-scale test is a classical iid RSS-based F-test (p=0.663) run right after the section declares default iid SEs "WRONG here!" and mandates HAC; a HAC-robust Wald test gives p=0.636, matching the hand-typed prose value (*either switch to the HAC Wald test — preserves every prose number, consistent with the section — or keep the classical test and update prose 0.636→0.663; no conclusion flips (fail to reject CRS either way); also in cheat sheet L1756–1765*).
- **Interpretation:** `ch13-F43` — the post-1970 Phillips "sign reversal"/"stagflation" and the augmented model's "return" of the negative slope are presented as substantive, but both urate coefficients are insignificant (t=0.81, p=0.42; t=−1.58, p=0.12) and significance is never noted (*add a significance caveat; the OVB point-estimate demo is intentional pedagogy, so wording is author's judgment*).
- **Readability:** `ch13-F44` (RAND RCT cell, ~47 lines, 3 independent outputs) and `ch13-F45` (Institutions/IV cell, ~56 lines, 4 outputs) exceed the split threshold (*split each at the suggested points with one-line lead-ins*).

## ch14 (13) — gender-gap direction flips (`F01`/`F02`/`F13`/`F14`/`F15`/`F19`/`F20`/`F21`) in Part 1 §6
- **Code:** `ch14-F08` — Task 5 scaffold uses statsmodels `anova_lm` (never imported, doesn't work on pyfixest) and undefined vars `model_base/model_dep_only/model_full` (fits are `fit_*`) (*rewrite the joint-test hint in pyfixest's `wald_test` idiom*).
- **Interpretation/results:** `ch14-F16` ≡ `ch14-F22` — the worker-type "Example Interpretation" **inverts every earnings sign**: self-employed are shown earning ~$5k *less* than private, but they earn ~$17k *more* and are the top group (raw means Self 72,306 > Govt 56,105 > Private 54,521) (*rewrite the example and its mirror block with the executed signs*). `ch14-F17` — Key Takeaways cites the classical t=−4.71 for the gender coef while the headline Model 1 uses HC1 (robust t=−5.10) (*defensible as-is: L968 is in the regression↔t-test-equivalence section where −4.71 is the intended value; low confidence*). `ch14-F18` — §14.3 characterizes the Gender×Education interaction as "−$1,000 to −$2,000" vs executed −$2,100 to −$2,800 (*hedged illustrative range followed by a hypothetical β=−1,500 worked example — changing it would clash; low priority*).

## ch15 (14) — interaction-significance flips (`F02`/`F16`/`F23`/`F29`/`F32`) in Part 1 §6
- **Methods/results (MEM = AME for a quadratic):** `ch15-F01` ≡ `ch15-F15` ≡ `ch15-F31` — the MEM Key Concept claims the marginal-effect-at-the-mean *differs* from the AME for the quadratic earnings model and quotes +$1,000–$1,500/yr, but for a quadratic ME is linear in age so **MEM = AME = $536 exactly** (*replace with the corrected sentence: MEM=AME for a quadratic; they diverge only for genuinely nonlinear ME curves — logit, cubic+*).
- **Results (standardized-coefficient ranking):** `ch15-F17` ≡ `ch15-F22` ≡ `ch15-F30` ≡ `ch15-F33` — the narrative and glossary call education/lnhours the largest standardized effects and rank age as "moderate (β*≈0.15–0.20)," but executed β* are age 0.68, age² −0.57, education 0.30, lnhours 0.22 (*correct the ranking; hedge that age's large β* is partly a quadratic artifact of the age/age² pair — author frames*).
- **Results (levels/log age-coef drift):** `ch15-F27` — levels age effect stated ≈$800–$1,200/~$1,000 but executed coef is 525 (also L527) (*correct to ≈$525*). `ch15-F28` — log-linear age coef stated 0.01–0.02 (1–2%) but executed 0.0078 (~0.8%) (*correct to ~0.8%; minor*).

## ch16 (8) — merged heading in Part 1 §7
- **Methods/interpretation:** `ch16-F02` — the Endogeneity KC example says the chapter regresses "growth on democracy" (democracy endogenous), but the actual model is `democracy ~ growth` (democracy is the outcome) (*rewrite the example to match; interlocks with the reversed research-question framing at L885*).
- **Code:** `ch16-F07` — CS1 dataset bullet documents `rk`/`hc`/`rgdppc`/`tfp`, none of which exist (actual `kl`/`h`/`GDPpc`/`TFP`); descriptions need domain judgment (`kl` is capital *per worker*) (*revise the bullets; stale project-memory carryover shared across chapters*). `ch16-F08` — CS2 Task 4 scaffold calls `OLSInfluence(model)`/`model.params` on a pyfixest fit (`model` undefined; OLSInfluence needs a statsmodels result); the main text correctly uses `smf.ols(...).fit()` at L1279 (*rewrite the commented scaffold to the smf.ols pattern*).
- **Results/interpretation (AR(1) "interest rate" orphaned essay):** `ch16-F22` ≡ `ch16-F26` — the entire §16.6 block interprets an empirical "interest rate / levels regression" (ρ₁≈0.95–0.98, variance-inflation factor 39, Fed policy, 10-yr vs 1-yr rate) that the chapter **never runs** — the code only simulates generic AR(1) data (ρ=0.8, executed lag-1 ACF 0.797, factor 9) (*reframe the whole block to the simulated AR(1) exercise, or add a real interest-rate dataset; a student who ran the sim cannot reconcile ρ₁≈0.80 with the narrative*). `ch16-F15` — intercept VIF stated ≈10–15 but statsmodels reports 411.3 (*drop the line or state intercept VIF is not econometrically meaningful*). `ch16-F23` ≡ `ch16-F28` — robust SEs described as "20–40% larger" but actual ratios are 0.98× (age) and 1.13× (education), and "reveals heteroskedasticity" overstates near-1.0 ratios (also stale table at L562–563) (*soften to "modest differences… mild heteroskedasticity at most"*).

## ch17 (18) — cluster-significance flips (`F01`/`F02`/`F15`/`F16`/`F17`/`F24`/`F30`/`F31`/`F32`/`F33`) & SE tables (`F14`/`F17`) in Part 1 §6
- **Methods:** `ch17-F04` — the two-way clustering formula is written "SE_two-way = SE_team + SE_time − SE_pooled," but SEs aren't additive; per Cameron-Gelbach-Miller, *variance matrices* combine as V_team + V_time − V_(team×time) (*correct to the variance form; the subtracted term is the team×time intersection, not the pooled/classical variance*).
- **Code:** `ch17-F08` — in the logit cell, `model_logit.summary()` (L886) and `marginal_effects.summary()` (L891) are bare mid-cell expressions, so neither table renders (Jupyter shows only the last expression), and KC 3's marginal-effect claim can't be seen (*wrap both in `print()`/`display()` or restructure the cell*).
- **Results (KC/table sign errors in the ADL/AR time-series section):** `ch17-F25` — KC AR(p) example claims a negative own-lag (~−0.20 mean reversion) but the fitted coef is +0.28 (positive momentum). `ch17-F26` — KC ADL example hand-types γ = 0.50/0.20/0.08 and LRM 0.78, but the fit gives 0.74/−0.26/0.05 and LRM 0.53 (γ₁ sign flips). `ch17-F27` — §17.6 ADL(2,2) ranges have two wrong signs and out-of-range magnitudes vs the fit. `ch17-F28` — "Comparing Models" R² table conflicts with the fits (static R²=0.25 vs executed 0.571; AR2 0.10 vs 0.125; ADL 0.45 vs 0.611) (*re-sync all four to the fitted values the audit supplies; these are hand-typed, not executed in the body*).
- **Format:** `ch17-F47` — Key Takeaways ends with a one-line "**Next steps:**" instead of the ch01-style 3–5-bullet block (*expand to the standard block; terminal-chapter content is generative, author's call*).

---

# How to action this

- You can reply **chapter-by-chapter** (e.g. "ch12: do Part 1 §1 Option A and §2 dropna") or **theme-by-theme** (e.g. "apply all the significance-flip rewrites in Part 1 §6", "resync all ch17 ADL numbers").
- For each accepted item, the fix is applied as an **isolated follow-up edit** on the already-committed chapter, then re-synced (.ipynb/.md/book HTML) and re-executed — the same per-chapter gate the campaign used. No PDFs.
- The highest-leverage decisions, in rough priority order: **§4 (ch11 F-stat cascade)** and **§5 (ch10 VIF)** — pure code repairs that stop the chapters contradicting their own output; **§6 (ch17/ch08/ch14/ch15 conclusion flips)** — the interpretation errors most likely to mislead students; **§1–§3 (ch12/ch06 orphaned prose)** — add-code vs delete-prose, the largest structural calls; then **§7–§9** convention choices (ch16 heading, ch05 terciles, ch03/ch06 FPC).
- Every "flip" and "re-sync" item in this report has audit-verified ground-truth numbers in `findings/chNN.json` (the `evidence`/`verify_note` fields), so accepted edits carry their own target values.
