# Widget Catalog

Concept → widget mapping. When a chapter introduces a concept below, the corresponding widget snippet in `templates/widgets/` is the starting point. When a chapter needs a widget not listed here, invent it and add a row.

## Current widgets

| Widget | Target concept(s) | Typical chapters | Snippet |
|---|---|---|---|
| Summary stats + outlier injector | Mean vs. median under skew; robustness to outliers | 2, 5, 7, 9, 10 | `templates/widgets/summary_stats.md` |
| Histogram + KDE (bin-width slider) | Shape of a distribution; bin choice subjectivity | 2, 5, 7, 9, 10 | `templates/widgets/histogram_kde.md` |
| Box plot + IQR multiplier | Outlier conventions; quartiles; IQR | 2, 5 | `templates/widgets/boxplot_iqr.md` |
| Time-series 3-way (Level/Log/Growth) | Trend, cycles, growth rates; log-linearization | 2, 6, 10, 14 | `templates/widgets/timeseries_scale.md` |
| Categorical bar/pie + sort | Summarizing counts; chart-type trade-offs | 2, 3 | `templates/widgets/categorical_barpie.md` |
| Log transformation (xs + ts) | Skew taming; hockey stick → straight line | 2 (heavy), 10 | `templates/widgets/log_transform.md` |
| Z-score calculator | Standardization; empirical rule (68-95-99.7) | 2, 4 | `templates/widgets/zscore_calculator.md` |
| Moving-average smoother | Smoothing vs. responsiveness; seasonal adjustment | 2, 14 | `templates/widgets/moving_average.md` |

## Likely new widgets (not yet built)

When a chapter needs these, invent them, author a Markdown snippet, and add a row here.

| Widget (proposed) | Target concept | Likely chapter | Notes |
|---|---|---|---|
| Scatter + regression line + correlation | Bivariate relationship, Pearson's r | 5 | Interactive r-target slider on synthetic data for intuition; real scatter below |
| OLS line fitter with draggable slope | Slope/intercept interpretation, SSR minimization | 7–8 | Draggable anchors; live R² readout |
| Sampling distribution simulator | Central Limit Theorem; standard error | 9 | "Run 10/100/1000 samples" button; animated histogram |
| Confidence interval visualizer | Coverage vs. sample count | 9 | N intervals drawn; count those covering true mean |
| Hypothesis testing power explorer | Type-I/II errors; effect size; sample size | 11 | Two densities with shaded α and β regions |
| p-value vs. critical value | Test statistic placement on null distribution | 11 | Slider for test statistic; shaded tails |
| Multiple regression coefficient comparer | Added-variable plots; omitted-variable bias | 13 | Toggle controls whether a covariate is in the model |
| Dummy variable interaction | Interpreting interaction coefficients | 15 | Two regression lines with slope/intercept dummies |

## Principles for inventing a new widget

1. **One concept per widget.** If it's teaching two, split it.
2. **Real chapter data, not synthetic**, except when the concept *requires* a controlled simulation (CLT, bootstrap).
3. **Controls drive the chart in < 100 ms.** No expensive recomputes on slider drag.
4. **Use `baseLayout()` and `themeColors()`** from the shared helpers. Don't hard-code colors.
5. **Expose `window.__rerender_<id>`** so theme toggle + hash state can drive re-renders.
6. **Save the pattern back here.** A widget built for chapter 5 is a gift to chapter 10.
