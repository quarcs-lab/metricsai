# Visual-summary mathematical errata

Reviewed on 2026-10-12. All 18 main visual summaries displayed by the book were inspected: the preface (00) and chapters 01–17. Chapters 01–17 have now been recreated as corrected illustrated mind maps. The preface remains unchanged.

## Corrected publication

The current image selection is recorded in [../images/visual_summaries.json](../images/visual_summaries.json): Chapter 1 v4, Chapters 2–3 v3, and Chapters 4–17 v2. Each selected image has a companion prompt and visual review in this directory. All were made with the built-in image-generation tool. Original JPGs are retained for comparison; earlier PNG drafts are not published.

All 54 audit findings are addressed in the selected replacement summaries, either with corrected mathematics, explicit conditions, or removal of the misleading claim/graphic. The two CSVs below preserve the original audit snapshot, including the original-image fingerprints and initial `open` statuses. Use [publication.json](publication.json) for the final image hashes and finding-to-replacement status, and the per-chapter review notes for details. This avoids misrepresenting the unchanged original JPGs as corrected.

`python3 scripts/sync_visual_summaries.py --write` propagates the manifest's filenames to Quarto sources, website cards, notebook/Markdown exports, rendered HTML, and frozen book content. Running it without `--write` verifies consistency. Synchronization preserves all non-image bytes, including code, notebook outputs, and frozen computation results.

[verification.json](verification.json) records successful local browser checks and post-push verification: all 17 public image hashes, the deployed website, all 17 live book pages, and all 17 public notebooks matched the selected summaries. GitHub Pages successfully built publication commit `9aa5624`.

## Files and categories

- [visual_summary_errata.csv](visual_summary_errata.csv): the correction checklist, with 54 findings. Each row has a stable ID, chapter, image path, location, original content, corrected equation in LaTeX, replacement wording, reasoning and edit status.
- [chapter_review.csv](chapter_review.csv): all 18 images, their source-book references, SHA-256 fingerprints, review status and finding counts. This records reviewed chapters even when no error was identified.

The checklist separates **18 confirmed errors**, **33 items needing qualification**, and **3 ambiguous graphics**. These are not 54 literal equation typos.

- **confirmed_error**: an incorrect equation, mathematical label, diagram, or conceptual claim requiring correction.
- **needs_qualification**: a statement or formula that needs a condition, definition, approximation marker or narrower interpretation. Some can be valid in an intended context; do not treat them as unconditional errors.
- **ambiguous_graphic**: a diagram can suggest an incorrect mathematical relationship, but its intended meaning is unclear. The proposed replacement removes that ambiguity.

The CSV edit_status values record the initial audit state. The corrected_equation_latex field contains mathematical reference text; replacement_text is concise wording adapted to the corrected images. Multiple occurrences of the same error within one image can share one row.

## Coverage

| Chapter | Confirmed errors | Needs qualification | Ambiguous graphics |
| --- | ---: | ---: | ---: |
| 00 | 0 | 0 | 0 |
| 01 | 0 | 0 | 0 |
| 02 | 1 | 4 | 0 |
| 03 | 1 | 1 | 0 |
| 04 | 2 | 1 | 0 |
| 05 | 1 | 0 | 0 |
| 06 | 2 | 2 | 0 |
| 07 | 1 | 3 | 0 |
| 08 | 3 | 1 | 0 |
| 09 | 2 | 2 | 0 |
| 10 | 2 | 2 | 0 |
| 11 | 0 | 3 | 0 |
| 12 | 2 | 3 | 0 |
| 13 | 0 | 2 | 1 |
| 14 | 0 | 2 | 0 |
| 15 | 0 | 3 | 0 |
| 16 | 1 | 2 | 0 |
| 17 | 0 | 2 | 2 |
| **Total** | **18** | **33** | **3** |

No mathematical error was identified in the preface or Chapter 1. Chapters with only qualification/ambiguity findings do not have a confirmed typo merely because they have checklist entries.

## Confirmed corrections

The CSV contains the exact replacement equations and full explanations. This index highlights the definite corrections.

| ID | Location | Correction |
| --- | --- | --- |
| VS-02-01 | Bottom right: Growth rates | Multiply the log difference by 100 to approximate percentage growth. |
| VS-03-01 | Right bottom: Estimator properties, Efficient | Minimum variance among LINEAR unbiased estimators under the stated common-variance and independence assumptions. |
| VS-04-01 | Bottom center: two-sided critical-region diagram | Put a minus sign only at the left cutoff and a plus sign only at the right cutoff. |
| VS-04-03 | Lower right: Generalization and proportions, General form | For approximately symmetric pivotal distributions, estimate ± the appropriate critical value × SE. A proportion uses a normal approximation here, not an exact t law. |
| VS-05-01 | Upper right: slope triangle | Label the vertical leg Δŷ (rise), the horizontal leg Δx (run), and the ratio b₂ (slope). |
| VS-06-01 | Upper left: diagram beside Var(u\|x)=σ_u² | Draw equal vertical spread at each x for homoskedasticity. |
| VS-06-02 | Bottom center: population line / fitted line / u and e diagram | At one observed point (xᵢ,yᵢ), draw uᵢ vertically to the population mean and eᵢ vertically to the fitted line. |
| VS-07-01 | Upper right: t-statistics and inference equation | Remove the second division by SE(b₂). |
| VS-08-01 | Upper right: CAPM beta interpretation | Beta measures signed exposure to market movements. Beta below 1 does not imply lower total volatility. |
| VS-08-03 | Lower right: Okun's law coefficient interpretation | Use percentage-point units. The recreated image also aligns the regression direction with the chapter's data: fitted GDP growth = 3.01 − 1.59 × change in unemployment (percentage points). See the Chapter 8 review. |
| VS-08-04 | Lower left: first General lessons bullet | Causal claims need a credible identification design and assumptions. Multiple regression is neither necessary nor sufficient. |
| VS-09-01 | Upper right: Semi-elasticity; lower-left table row 1 | b₂ is fractional change per unit x; approximate percent change is 100b₂ per unit x. |
| VS-09-03 | Upper-left approximation qualifier and lower-right Approximations heading | Use small ABSOLUTE relative changes, for example \|h\|<0.1; log expansion also requires h>−1. |
| VS-10-01 | Upper-right heading: small purple formula icon | Replace the decorative equation with ŷ=Xb or a valid OLS objective. |
| VS-10-02 | Bottom right: adjusted R² formula | Remove the extra ] after (n−k). Define k as the number of estimated coefficients including the intercept. |
| VS-12-03 | Upper right: Individual forecast variance box | Label the quantity as prediction-error variance, Var(y*−ŷ*), assuming the future error is independent of the estimation sample. |
| VS-12-05 | Bottom right: Hybrid approach | After variable selection, use an inference method that accounts for selection, such as an appropriately designed sample split or a justified post-selection procedure. |
| VS-16-01 | Middle right: omitted-variable-bias equation | γ is the auxiliary-regression SLOPE of the omitted variable z on x, not its correlation coefficient. |

## Method and limits

Book configuration and image references were used only to select the main summary files. Corrections were derived through independent mathematical reasoning, not by treating the chapter prose or earlier repository audits as authoritative. The local images in images/ were reviewed; remote image bytes were not fetched or compared. The chapter pages reference the corresponding filenames on the repository's main branch.

Every full image was visually inspected. Small signs, brackets, arrows and handwritten variables were rechecked in enlarged local crops when needed. Independent numerical checks covered percentage scaling, a counterexample to unrestricted efficiency of the sample mean, the CAPM volatility counterexample, the scale factor in omitted-variable bias, the sum of the Cobb–Douglas coefficients, normal coverage percentages, finite differences versus derivatives, and nonzero conditional means with zero regressor-error covariance.

Reported case-study estimates (for example dollar effects, R² ranges and the NBA coefficient) were not re-estimated from their datasets. Their mathematical interpretations and internal arithmetic were reviewed. Claims requiring unavailable standard errors or covariances are marked as needing qualification rather than assigned invented significance results. Pure spelling/style issues and course-organization labels are outside this mathematical checklist. “No error identified” is a review outcome, not a proof that an image is flawless.

Conventions in corrections: k counts all fitted regression coefficients, including the intercept; t_{ν,p} is the p quantile of Student's t distribution; RSS means residual sum of squares and TSS means total centered sum of squares. Conditions attached to one formula should accompany that formula in the eventual corrected image.

## Useful checks for the correction task

- Chapter 3: for n=10 and Uniform(0,1) sampling, Var(sample mean)=1/120, whereas Var(11 max(Xᵢ)/20)=1/480. Thus the sample mean is not minimum variance among all unbiased estimators under the image's general assumptions.
- Chapter 8: β=0.5, market variance 1 and orthogonal residual variance 4 imply stock variance 4.25, despite β<1.
- Chapter 16: if the omitted variable has auxiliary slope 3 and outcome coefficient 4, omitted-variable bias is 12. Replacing the auxiliary slope by a raw correlation gives an incorrect magnitude.
- Chapter 10: the partial-slope identity using original y and residualized xⱼ is valid. Do not “correct” it by declaring that residualizing y is necessary for the coefficient identity.
- Chapter 15: the z glyph in the interaction model resembles 2, but the expressions are consistent derivatives of an xz interaction. Do not replace z with a numeric 2 or a square.
