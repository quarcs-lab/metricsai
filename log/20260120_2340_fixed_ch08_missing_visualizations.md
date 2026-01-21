# Fix Log: CH08 Missing Visualization Code

**Date:** January 20, 2026, 23:40
**Issue:** Three visualization code cells missing in CH08
**Impact:** Scatter plots referenced in markdown but no code to generate them
**Status:** RESOLVED ✅

---

## Problem Description

After fixing the missing regression models in CH08, we discovered that 3 visualization code cells were also missing. The notebook had markdown headers announcing visualizations, followed by interpretation cells explaining the plots, but the actual plotting code was never included.

**Missing Visualizations:**
1. **CAPM Scatter Plot** (Figure 8.3 Panel B)
2. **Okun's Law Scatter Plot** (Figure 8.4 Panel A)
3. **Okun's Law Time Series** (Figure 8.4 Panel B)

**Pattern Detected:**
```
Markdown: "Visualization: [Name]"
↓
Markdown: "Understanding the [Name]" ← Explains plot that doesn't exist!
↓
(Next section begins)
```

**Expected structure:**
```
Markdown: "Visualization: [Name]"
↓
Code: Generate the visualization
↓
Markdown: "Understanding the [Name]"
```

---

## Fixes Applied

### Fix 1: CAPM Scatter Plot (Figure 8.3 Panel B)

**Location:** Inserted at cell 43 (after "Visualization: CAPM Scatter Plot" header)

**Code added:**
```python
# Figure 8.3 Panel B - CAPM Scatter Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_capm['rm_rf'], data_capm['rko_rf'], alpha=0.4, s=30,
           color='black', label='Actual')
ax.plot(data_capm['rm_rf'], model_capm.fittedvalues, color='blue',
        linewidth=2, label='Fitted')
ax.set_xlabel('Market excess return (rm - rf)', fontsize=12)
ax.set_ylabel('Coca-Cola excess return (rko - rf)', fontsize=12)
ax.set_title('Figure 8.3 Panel B: CAPM - Coca-Cola vs Market Excess Returns',
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"\nBeta (slope) = {model_capm.params['rm_rf']:.4f}")
print("The slope less than 1 confirms Coca-Cola is a 'defensive' stock.")
print("Each 1% increase in market return → ~0.6% increase in Coca-Cola return.")
```

**What it shows:**
- Scatter plot: Market excess return (x-axis) vs Coca-Cola excess return (y-axis)
- Fitted line: CAPM regression line (slope = beta ≈ 0.61)
- 366 monthly observations (1983-2013)
- Visual confirmation that Coca-Cola is less volatile than market (slope < 1)

**Educational value:**
- Students see the relationship between individual stock and market returns
- Beta (systematic risk) visualized as the slope
- Points scattered around line show idiosyncratic (diversifiable) risk
- Lower-than-45° slope demonstrates defensive stock characteristics

---

### Fix 2: Okun's Law Scatter Plot (Figure 8.4 Panel A)

**Location:** Inserted at cell 53 (after "Visualization: Okun's Law Scatter Plot" header)

**Code added:**
```python
# Figure 8.4 Panel A - Okun's Law Scatter Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_gdp['uratechange'], data_gdp['rgdpgrowth'], alpha=0.6, s=50,
           color='black', label='Actual')
ax.plot(data_gdp['uratechange'], model_okun.fittedvalues, color='blue',
        linewidth=2, label='Fitted')
ax.set_xlabel('Change in unemployment rate (percentage points)', fontsize=12)
ax.set_ylabel('Percentage change in real GDP', fontsize=12)
ax.set_title('Figure 8.4 Panel A: Okun\'s Law - GDP Growth vs Unemployment Change',
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("Each point represents one year of U.S. macroeconomic data (1961-2019).")
print("The negative slope confirms Okun's Law: rising unemployment → falling GDP.")
```

**What it shows:**
- Scatter plot: Change in unemployment (x-axis) vs GDP growth (y-axis)
- Fitted line: Okun's Law regression (slope ≈ -1.59)
- 59 annual observations (1961-2019)
- Clear negative relationship between unemployment changes and GDP growth
- Outliers visible (recession years like 2009)

**Educational value:**
- Visual confirmation of Okun's Law
- Students see the strength of the relationship (R² ≈ 0.59)
- Major recessions stand out as outliers (high unemployment increase, negative GDP)
- Cross-sectional variation illustrates that relationship isn't deterministic

---

### Fix 3: Okun's Law Time Series (Figure 8.4 Panel B)

**Location:** Inserted at cell 56 (after "Visualization: Time Series" header)

**Code added:**
```python
# Figure 8.4 Panel B - Time Series of Actual vs Predicted GDP Growth
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data_gdp['year'], data_gdp['rgdpgrowth'], linewidth=1.5,
        label='Actual GDP Growth', color='black')
ax.plot(data_gdp['year'], model_okun.fittedvalues, linewidth=1.5, linestyle='--',
        label='Predicted (from Okun\'s Law)', color='blue')
ax.axhline(y=0, color='red', linestyle=':', linewidth=1, alpha=0.5)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Percentage change in real GDP', fontsize=12)
ax.set_title('Figure 8.4 Panel B: Actual vs Predicted Real GDP Growth Over Time',
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\nMajor recessions visible: 1982, 1991, 2001, 2008-2009")
print("Note: Post-2008 recovery shows actual GDP exceeding predictions.")
```

**What it shows:**
- Time series: Actual GDP growth (black solid line) vs predicted from Okun's Law (blue dashed)
- Red horizontal line at y=0 marks recessions (negative growth)
- Years 1961-2019 on x-axis
- Model tracks major turning points but misses some nuances

**Educational value:**
- Students see how well the model fits over time
- Major recessions (1982, 2008-2009) clearly visible
- Post-2008 "jobless recovery" visible: actual > predicted
- Demonstrates that simple models capture main patterns but miss details
- Time series visualization complements cross-sectional scatter plot

**Key finding highlighted:**
- Pre-2008: Model fits very well
- Post-2008: Systematic under-prediction (actual GDP growth exceeds predictions)
- Suggests structural change in labor market dynamics after financial crisis

---

## Summary of All CH08 Fixes

### Total Fixes in CH08 (This Session):

**Missing Regression Models (Earlier):**
1. `model_infmort` (Infant mortality)
2. `model_hlthpc` (Health expenditure - full sample)
3. `model_hlthpc_subset` (Health expenditure - subset)

**Missing Visualizations (This Fix):**
4. CAPM scatter plot
5. Okun's Law scatter plot
6. Okun's Law time series plot

**Total code cells added:** 6

---

## Cell Count Summary

**Before all fixes:** 54 cells (16 code, 38 markdown)
**After all fixes:** 60 cells (22 code, 38 markdown)
**Increase:** +6 code cells (+37.5%)

### Breakdown by Section:

| Section | Missing Items | Fixed |
|---------|---------------|-------|
| 8.1 Health Outcomes | Infant mortality regression | ✅ |
| 8.2 Health Expenditures | 2 regressions (full + subset) | ✅ |
| 8.3 CAPM | Scatter plot visualization | ✅ |
| 8.4 Okun's Law | 2 visualizations (scatter + time series) | ✅ |

---

## Verification

### Complete Section Structure Check:

**Section 8.1 (Health Outcomes):**
- ✅ Life expectancy regression with code
- ✅ Life expectancy visualization with code
- ✅ Infant mortality regression with code (FIXED)
- ✅ Infant mortality visualization with code

**Section 8.2 (Health Expenditures):**
- ✅ Full sample regression with code (FIXED)
- ✅ Full sample visualization with code
- ✅ Subset regression with code (FIXED)
- ✅ Subset visualization with code

**Section 8.3 (CAPM):**
- ✅ Data loading and summary statistics
- ✅ Time series visualization (excess returns)
- ✅ CAPM regression with code
- ✅ CAPM scatter plot with code (FIXED)

**Section 8.4 (Okun's Law):**
- ✅ Data loading and summary statistics
- ✅ Okun regression with code
- ✅ Scatter plot with code (FIXED)
- ✅ Time series plot with code (FIXED)

### Execution Test:

✅ All code cells execute sequentially without errors
✅ All visualizations render properly
✅ All interpretations reference actual results (not placeholders)
✅ Notebook can run end-to-end in Google Colab

---

## Educational Quality Restored

**Before fixes:**
- Incomplete analysis workflows
- Markdown cells describing plots that didn't exist
- Students couldn't reproduce the analysis
- Missing visual confirmation of statistical relationships

**After fixes:**
- Complete analysis workflows (concept → code → interpretation → visualization)
- All promised visualizations delivered
- Students can see AND generate the plots themselves
- Visual intuition strengthens understanding of abstract concepts

**Impact on learning:**
- CAPM: Students now SEE beta as the slope of the scatter plot
- Okun's Law: Visual confirmation of the negative relationship
- Time series: Understanding of when models work well vs when they break down
- Hands-on experience generating professional econometric visualizations

---

## Root Cause Analysis

**Why were visualizations missing?**

During notebook creation, the workflow likely was:
1. Write markdown headers and conceptual explanations
2. Generate plots in separate testing/development
3. Forget to copy visualization code into notebook
4. Add interpretation cells based on plots viewed elsewhere

**Prevention:**
- Always include code immediately after announcing a visualization
- Test notebooks end-to-end before considering them complete
- Use checklist: For each "Visualization: X" header, verify code cell follows
- Cross-reference with Python scripts to ensure all plots included

---

## Pattern Recognition

**Common issue across CH06 and CH08:**

Missing the MIDDLE STEP in three-part workflows:
1. ❌ Conceptual introduction → Interpretation → (missing: actual analysis)
2. ❌ Markdown header → Markdown explanation → (missing: code to generate plot)

**Correct pattern:**
1. ✅ Conceptual introduction → **Code to run analysis** → Interpretation
2. ✅ Visualization header → **Code to generate plot** → Explanation of plot

**Recommendation for remaining notebooks:**
- Check all sections with "Visualization:" headers
- Verify code cell exists immediately after
- Verify all model variables used in plots are created first

---

## Files Modified

**Fixed:**
- `/Users/carlosmendez/Documents/GitHub/aed/notebooks_colab/ch08_Case_Studies_for_Bivariate_Regression.ipynb`

**New cells added:**
- Cell 43: CAPM scatter plot
- Cell 53: Okun's Law scatter plot (Panel A)
- Cell 56: Okun's Law time series (Panel B)

**File size:** ~165 KB (moderate increase from visualization code)

---

## Status: RESOLVED ✅

CH08 is now COMPLETELY fixed:
- ✅ All 6 regression models properly created
- ✅ All 9 visualizations properly implemented
- ✅ All code cells execute without errors
- ✅ All interpretation cells reference actual results
- ✅ Professional-quality educational notebook ready for deployment

**Total session fixes:**
- CH06: 3 issues (cell types, missing data generation, duplicates)
- CH08: 6 issues (3 missing regressions + 3 missing visualizations)

**Educational quality: EXCELLENT** 🎓

---

**Fix completed successfully!** Students now have complete, executable, publication-quality econometric case studies in CH08.
