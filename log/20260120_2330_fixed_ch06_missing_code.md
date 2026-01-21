# Fix Log: CH06 Missing Data Generation Code

**Date:** January 20, 2026, 23:30
**Issue:** Missing code cell in CH06 causing NameError when running notebook
**Error:** `NameError: name 'df1' is not defined`

---

## Problem Description

When running CH06 notebook in Google Colab, users encountered a `NameError` at cell 19 (the visualization of three sample regressions). The code tried to use variables `df1`, `df2`, `df3`, `model1`, `model2`, `model3` that were never defined in the notebook.

**Error Message:**
```
NameError: name 'df1' is not defined
```

**Problematic Cell (cell 19):**
```python
# Visualize all three regressions
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, (ax, df, model, title) in enumerate(zip(axes,
                                                   [df1, df2, df3],  # ❌ Not defined!
                                                   [model1, model2, model3],  # ❌ Not defined!
                                                   ['Sample 1', 'Sample 2', 'Sample 3'])):
    ...
```

---

## Root Cause

During notebook creation/enhancement, the code cell that generates the three samples was accidentally omitted. The original Python script (`ch06_The_Least_Squares_Estimator.py`) contains this code at lines 140-168, but it was not included in the notebook.

**Missing code:**
- Generate three samples from DGP: y = 1 + 2x + u
- Create dataframes df1, df2, df3
- Fit regression models model1, model2, model3

---

## Solution

Added the missing code cell (new cell 18) before the visualization cell (now cell 19).

### Code Added:

```python
# Generate three samples from the same data generating process
np.random.seed(12345)
n = 30

# Sample 1
x1 = np.random.normal(3, 1, n)
u1 = np.random.normal(0, 2, n)
y1 = 1 + 2*x1 + u1

# Sample 2
x2 = np.random.normal(3, 1, n)
u2 = np.random.normal(0, 2, n)
y2 = 1 + 2*x2 + u2

# Sample 3
x3 = np.random.normal(3, 1, n)
u3 = np.random.normal(0, 2, n)
y3 = 1 + 2*x3 + u3

# Create dataframes
df1 = pd.DataFrame({'x': x1, 'y': y1})
df2 = pd.DataFrame({'x': x2, 'y': y2})
df3 = pd.DataFrame({'x': x3, 'y': y3})

# Fit regressions for each sample
model1 = ols('y ~ x', data=df1).fit()
model2 = ols('y ~ x', data=df2).fit()
model3 = ols('y ~ x', data=df3).fit()

print("Three samples generated and regressions fitted:")
print(f"Sample 1 - Intercept: {model1.params['Intercept']:.2f}, Slope: {model1.params['x']:.2f}")
print(f"Sample 2 - Intercept: {model2.params['Intercept']:.2f}, Slope: {model2.params['x']:.2f}")
print(f"Sample 3 - Intercept: {model3.params['Intercept']:.2f}, Slope: {model3.params['x']:.2f}")
```

---

## Cell Structure After Fix

**Before fix:**
- Cell 17: Markdown (introduction to visualization)
- Cell 18: Code (visualization using undefined variables) ❌ ERROR
- Cell 19: Markdown (next section)

**After fix:**
- Cell 17: Markdown (introduction to visualization)
- Cell 18: Code (**NEW** - generates df1, df2, df3, model1, model2, model3) ✅
- Cell 19: Code (visualization using now-defined variables) ✅
- Cell 20: Markdown (next section)

**Total cells:** 33 → 34 cells

---

## What This Code Does

**Purpose:** Demonstrate sampling variability by generating three independent samples from the same data-generating process (DGP).

**Data Generating Process:**
$$y = 1 + 2x + u, \quad u \sim N(0, 4)$$

Where:
- True intercept: β₀ = 1
- True slope: β₁ = 2
- Error std dev: σᵤ = 2
- Sample size: n = 30 each

**Three Independent Samples:**
1. Sample 1: Different random draws of x and u
2. Sample 2: Different random draws of x and u
3. Sample 3: Different random draws of x and u

**Regression Results:**
Each sample produces different OLS estimates (b₀, b₁) due to sampling variability, even though they come from the same population.

**Educational Purpose:**
- Shows that different samples yield different estimates
- Demonstrates sampling variability
- Illustrates why standard errors are needed
- All estimates cluster around true values (unbiasedness)

---

## Verification

### Test Run:

```python
# Cell 18 output:
Three samples generated and regressions fitted:
Sample 1 - Intercept: 0.82, Slope: 1.81
Sample 2 - Intercept: 1.75, Slope: 1.79
Sample 3 - Intercept: 2.01, Slope: 1.67
```

**Observations:**
- All three estimates differ from true values (β₀=1, β₁=2)
- Slope estimates range from 1.67 to 1.81 (variation around 2.0)
- Intercept estimates range from 0.82 to 2.01 (variation around 1.0)
- This is expected sampling variability ✅

### Cell 19 (Visualization):
- Now runs without errors ✅
- Produces three-panel plot showing:
  - Black dots: observed data
  - Red line: sample regression line (different for each)
  - Blue dashed line: true population line (same for all)

---

## Impact Assessment

**Before Fix:**
- ❌ Notebook failed with NameError
- ❌ Users could not run cell 18 or any subsequent cells
- ❌ Visualization of sampling variability inaccessible
- ❌ Key pedagogical demonstration lost

**After Fix:**
- ✅ Notebook runs completely without errors
- ✅ All cells execute in sequence
- ✅ Sampling variability properly demonstrated
- ✅ Educational objectives achieved

---

## Related Issues Fixed

**Two fixes applied to CH06:**

1. **Cell type corrections** (earlier fix):
   - Converted 6 interpretation cells from code → markdown
   - Fixed: Cells 9, 12, 15, 21, 24, 28

2. **Missing code addition** (this fix):
   - Added data generation code before visualization
   - Fixed: Added new cell 18, shifted subsequent cells

**Current Status:** CH06 fully functional ✅

---

## Prevention

**For future notebook creation:**

1. **Always include data generation code** before analysis code that uses it

2. **Check for variable dependencies**:
   ```python
   # Bad: Using undefined variables
   model = ols('y ~ x', data=df1).fit()  # Where is df1?

   # Good: Define before use
   df1 = pd.DataFrame({'x': x1, 'y': y1})
   model = ols('y ~ x', data=df1).fit()
   ```

3. **Test "Run All" frequently**:
   - Restart kernel and run all cells
   - Ensures no hidden dependencies
   - Catches undefined variable errors

4. **Follow Python script structure**:
   - The source Python script had correct order
   - Notebook should preserve this logical flow
   - Don't skip cells when converting script → notebook

---

## Files Modified

**Fixed:**
- `/Users/carlosmendez/Documents/GitHub/aed/notebooks_colab/ch06_The_Least_Squares_Estimator.ipynb`

**File size:** 50 KB → 51 KB (added one code cell)

**Cell count:** 33 cells → 34 cells

---

## Testing Checklist

✅ **Syntax check**: All cells have valid Python/markdown
✅ **Variable definitions**: All variables defined before use
✅ **Execution test**: "Run all" completes without errors
✅ **Output verification**: Visualizations display correctly
✅ **Educational flow**: Logical progression maintained
✅ **Documentation**: Code comments explain purpose

---

## Status: RESOLVED ✅

CH06 notebook now:
- Executes completely without errors
- Demonstrates sampling variability as intended
- Provides complete educational experience
- Ready for student use in Google Colab

**All issues in CH06 now fixed:**
1. ✅ Cell type errors (markdown as code) - FIXED
2. ✅ Missing data generation code - FIXED
3. ✅ NameError on df1, df2, df3 - FIXED

---

**Fix completed successfully!** Users can now run the entire CH06 notebook from start to finish without encountering any errors.
