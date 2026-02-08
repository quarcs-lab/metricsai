#!/usr/bin/env python3
"""Add DS4Bolivia Case Study 2 to CH10 notebook."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = PROJECT_ROOT / 'notebooks_colab' / 'ch10_Data_Summary_for_Multiple_Regression.ipynb'


def make_md_cell(source):
    """Create a markdown cell dict."""
    lines = source.split('\n')
    source_list = [line + '\n' if i < len(lines) - 1 else line
                   for i, line in enumerate(lines)]
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source_list
    }


def make_code_cell(source):
    """Create a code cell dict."""
    lines = source.split('\n')
    source_list = [line + '\n' if i < len(lines) - 1 else line
                   for i, line in enumerate(lines)]
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_list
    }


# ============================================================
# Case Study 2 content cells
# ============================================================

cells_to_add = [

# ---------- Introduction ----------
make_md_cell("""\
### Case Study 2: Multiple Satellite Predictors of Development

**Research Question**: Do satellite image embeddings improve our ability to predict municipal development beyond nighttime lights alone?

In Chapter 1, we introduced the DS4Bolivia project and estimated a bivariate regression of development on nighttime lights. Now we extend this analysis using Chapter 10's **multiple regression** tools, adding satellite image embeddings as additional predictors to test whether they improve our ability to predict municipal development.

**Background**: Nighttime lights (NTL) are a well-established proxy for economic activity, but they capture only one dimension of a municipality's characteristics — nocturnal luminosity. Daytime satellite imagery contains far richer information: building density, road networks, agricultural patterns, vegetation cover. Deep learning models can extract this information as **64-dimensional embedding vectors**, where each dimension captures abstract visual patterns learned automatically from the data.

**The key question for multiple regression**: Does adding these satellite embeddings as extra regressors significantly improve explanatory power compared to NTL alone? And if so, which embeddings matter most?

**Variables for this case study:**
- `imds` — Municipal Sustainable Development Index (0-100, outcome variable)
- `ln_NTLpc2017` — Log nighttime lights per capita (established predictor from Chapter 1)
- `A00`, `A10`, `A20`, `A30`, `A40` — Selected satellite image embedding dimensions (new predictors)
- `mun`, `dep` — Municipality and department identifiers

**Your Task**: Use correlation analysis, multiple regression, the FWL theorem, and model comparison tools from Chapter 10 to evaluate whether satellite embeddings add predictive value beyond nighttime lights."""),

# ---------- Load Data ----------
make_md_cell("""\
#### Load the DS4Bolivia Data

Let's load the DS4Bolivia dataset and select the variables needed for our multiple regression analysis. We focus on the development index, nighttime lights, and five selected satellite embedding dimensions."""),

make_code_cell("""\
# Load the DS4Bolivia dataset
url_bol = "https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv"
bol = pd.read_csv(url_bol)

# Select key variables for this case study
key_vars = ['mun', 'dep', 'imds', 'ln_NTLpc2017', 'A00', 'A10', 'A20', 'A30', 'A40']
bol_sat = bol[key_vars].copy()

print("=" * 70)
print("DS4BOLIVIA DATASET — SATELLITE PREDICTORS")
print("=" * 70)
print(f"Dataset shape: {bol_sat.shape[0]} municipalities, {bol_sat.shape[1]} variables")
print(f"Departments: {bol['dep'].nunique()} unique departments")
print(f"Complete cases: {bol_sat.dropna().shape[0]}")
print("\\n" + "=" * 70)
print("FIRST 10 MUNICIPALITIES")
print("=" * 70)
print(bol_sat.head(10).to_string(index=False))"""),

# ---------- Task 1 ----------
make_md_cell("""\
#### Task 1: Explore Variables (Guided)

**Objective**: Understand the satellite embedding variables and how they compare to nighttime lights.

**Instructions**:
1. Generate summary statistics for all predictor variables using `describe()`
2. Compare the scale and distribution of NTL vs. embedding variables
3. Check for missing values across all selected variables
4. Consider: What are satellite embeddings? How do they differ from NTL?

**Key insight**: Unlike NTL (which has a clear physical interpretation — light intensity), embedding dimensions are **abstract features** extracted by neural networks. Dimension `A00` doesn't mean "vegetation" or "roads" — it captures a learned combination of visual patterns."""),

make_code_cell("""\
# Your code here: Explore the satellite predictor variables
#
# Step 1: Summary statistics for all numeric variables
print("=" * 70)
print("DESCRIPTIVE STATISTICS: DEVELOPMENT AND SATELLITE PREDICTORS")
print("=" * 70)
print(bol_sat[['imds', 'ln_NTLpc2017', 'A00', 'A10', 'A20', 'A30', 'A40']].describe().round(3))

# Step 2: Check for missing values
print("\\n" + "=" * 70)
print("MISSING VALUES")
print("=" * 70)
print(bol_sat.isnull().sum())

# Step 3: Compare variable ranges
print("\\n" + "=" * 70)
print("VARIABLE RANGES")
print("=" * 70)
for var in ['imds', 'ln_NTLpc2017', 'A00', 'A10', 'A20', 'A30', 'A40']:
    col = bol_sat[var].dropna()
    print(f"  {var:16s}  range: [{col.min():.3f}, {col.max():.3f}]  std: {col.std():.3f}")"""),

# ---------- Task 2 ----------
make_md_cell("""\
#### Task 2: Correlation Analysis (Guided)

**Objective**: Compute and visualize the correlation structure among all predictors and the outcome variable.

**Instructions**:
1. Compute the correlation matrix for `imds`, `ln_NTLpc2017`, and all five embedding variables
2. Display the correlation matrix as a heatmap
3. Identify: Which embeddings correlate most strongly with `imds`?
4. Identify: Do the embeddings correlate with each other (potential multicollinearity)?
5. Do the embeddings correlate with NTL, or do they capture different information?

**Apply what you learned in section 10.3**: Use `seaborn.heatmap()` with annotated correlation values."""),

make_code_cell("""\
# Your code here: Correlation analysis of satellite predictors
#
# Step 1: Compute correlation matrix
corr_vars = ['imds', 'ln_NTLpc2017', 'A00', 'A10', 'A20', 'A30', 'A40']
corr_sat = bol_sat[corr_vars].dropna().corr()

print("=" * 70)
print("CORRELATION MATRIX: DEVELOPMENT AND SATELLITE PREDICTORS")
print("=" * 70)
print(corr_sat.round(3))

# Step 2: Visualize as heatmap
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_sat, annot=True, fmt='.3f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
ax.set_title('Correlation Matrix: IMDS, NTL, and Satellite Embeddings',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# Step 3: Highlight strongest correlations with IMDS
print("\\nCorrelations with IMDS (development index):")
imds_corr = corr_sat['imds'].drop('imds').sort_values(key=abs, ascending=False)
for var, r in imds_corr.items():
    print(f"  {var:16s}  r = {r:+.3f}")"""),

# ---------- Key Concept 10.12 ----------
make_md_cell("""\
> **Key Concept 10.12: High-Dimensional Satellite Features**
>
> Satellite embeddings are **64 abstract features** extracted by deep learning models (convolutional neural networks) from daytime satellite imagery. Unlike handcrafted variables (e.g., NDVI for vegetation), each embedding dimension captures complex visual patterns — road density, building structures, agricultural layouts — learned automatically from the data. These features are not directly interpretable (dimension A00 doesn't have a specific meaning), but they collectively encode rich information about a municipality's physical landscape."""),

# ---------- Task 3 ----------
make_md_cell("""\
#### Task 3: Multiple Regression (Semi-guided)

**Objective**: Estimate a multiple regression model with NTL and satellite embeddings as predictors.

**Instructions**:
1. Estimate the full model: `imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40`
2. Display the regression summary
3. Compare $R^2$ with the bivariate NTL-only model from Chapter 1
4. Interpret: How much does adding embeddings improve explanatory power?
5. Which embedding coefficients are statistically significant?

**Apply what you learned in section 10.4**: Use `ols()` from statsmodels and interpret partial effects."""),

make_code_cell("""\
# Your code here: Multiple regression with satellite predictors
#
# Step 1: Prepare data (drop missing values)
reg_data = bol_sat[['imds', 'ln_NTLpc2017', 'A00', 'A10', 'A20', 'A30', 'A40']].dropna()
print(f"Regression sample: {len(reg_data)} municipalities (complete cases)")

# Step 2: Bivariate model (NTL only — baseline from Chapter 1)
model_ntl = ols('imds ~ ln_NTLpc2017', data=reg_data).fit()
print("\\n" + "=" * 70)
print("MODEL 1: BIVARIATE — imds ~ ln_NTLpc2017")
print("=" * 70)
print(model_ntl.summary())

# Step 3: Multiple regression (NTL + all 5 embeddings)
model_full_sat = ols('imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40',
                     data=reg_data).fit()
print("\\n" + "=" * 70)
print("MODEL 2: MULTIPLE — imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40")
print("=" * 70)
print(model_full_sat.summary())

# Step 4: Compare R-squared
print("\\n" + "=" * 70)
print("R-SQUARED COMPARISON")
print("=" * 70)
print(f"NTL only:           R² = {model_ntl.rsquared:.4f}")
print(f"NTL + 5 embeddings: R² = {model_full_sat.rsquared:.4f}")
print(f"Improvement:        ΔR² = {model_full_sat.rsquared - model_ntl.rsquared:.4f}")"""),

# ---------- Task 4 ----------
make_md_cell("""\
#### Task 4: Partial Effects via FWL (Semi-guided)

**Objective**: Demonstrate the Frisch-Waugh-Lovell theorem by showing that the NTL coefficient in the multiple regression equals the coefficient from regressing residualized IMDS on residualized NTL.

**Instructions**:
1. Regress `imds` on all embedding variables (`A00`, `A10`, `A20`, `A30`, `A40`), save residuals $e_y$
2. Regress `ln_NTLpc2017` on all embedding variables, save residuals $e_x$
3. Regress $e_y$ on $e_x$ (bivariate regression of residuals)
4. Verify that the coefficient matches the NTL coefficient from the full multiple regression

**Apply what you learned in section 10.5**: This demonstrates that the partial effect of NTL is computed from the variation in NTL that is *independent* of the satellite embeddings."""),

make_code_cell("""\
# Your code here: FWL theorem demonstration
#
# Step 1: Regress imds on embeddings only, save residuals e_y
model_y_on_emb = ols('imds ~ A00 + A10 + A20 + A30 + A40', data=reg_data).fit()
e_y = model_y_on_emb.resid

# Step 2: Regress ln_NTLpc2017 on embeddings only, save residuals e_x
model_x_on_emb = ols('ln_NTLpc2017 ~ A00 + A10 + A20 + A30 + A40', data=reg_data).fit()
e_x = model_x_on_emb.resid

# Step 3: Regress e_y on e_x
fwl_data = pd.DataFrame({'e_y': e_y, 'e_x': e_x})
model_fwl = ols('e_y ~ e_x', data=fwl_data).fit()

# Step 4: Compare coefficients
print("=" * 70)
print("FWL THEOREM DEMONSTRATION")
print("=" * 70)
print(f"NTL coefficient from FULL multiple regression:  {model_full_sat.params['ln_NTLpc2017']:.10f}")
print(f"Coefficient from FWL residual regression:       {model_fwl.params['e_x']:.10f}")
print(f"Difference (numerical precision):                {abs(model_full_sat.params['ln_NTLpc2017'] - model_fwl.params['e_x']):.15f}")
print("\\nThe coefficients are identical — confirming the FWL theorem!")
print("\\nInterpretation: The partial effect of NTL on IMDS is computed using")
print("only the variation in NTL that is NOT explained by the satellite embeddings.")"""),

# ---------- Task 5 ----------
make_md_cell("""\
#### Task 5: Model Comparison (Independent)

**Objective**: Compare multiple model specifications using fit statistics and information criteria.

**Your tasks**:
1. Estimate three models:
   - **Model 1**: `imds ~ ln_NTLpc2017` (NTL only)
   - **Model 2**: `imds ~ ln_NTLpc2017 + A00 + A10` (NTL + 2 embeddings)
   - **Model 3**: `imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40` (NTL + 5 embeddings)
2. Create a comparison table reporting $R^2$, adjusted $R^2$, AIC, and BIC for each model
3. Use `model.rsquared`, `model.rsquared_adj`, `model.aic`, `model.bic`
4. Which model is "best" by each criterion?
5. Does the parsimony principle favor fewer or more embedding variables?

*Hint: Use `pd.DataFrame()` to create a clean comparison table.*"""),

make_code_cell("""\
# Your code here: Model comparison
#
# Step 1: Estimate three models
# model_1 = ols('imds ~ ln_NTLpc2017', data=reg_data).fit()
# model_2 = ols('imds ~ ln_NTLpc2017 + A00 + A10', data=reg_data).fit()
# model_3 = ols('imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40', data=reg_data).fit()
#
# Step 2: Create comparison table
# comparison = pd.DataFrame({
#     'Model': ['NTL only', 'NTL + 2 embeddings', 'NTL + 5 embeddings'],
#     'R²': [model_1.rsquared, model_2.rsquared, model_3.rsquared],
#     'Adj R²': [model_1.rsquared_adj, model_2.rsquared_adj, model_3.rsquared_adj],
#     'AIC': [model_1.aic, model_2.aic, model_3.aic],
#     'BIC': [model_1.bic, model_2.bic, model_3.bic],
#     'N': [len(reg_data)] * 3
# })
# print(comparison.to_string(index=False))
#
# Step 3: Interpret — which model is preferred by each criterion?"""),

# ---------- Key Concept 10.13 ----------
make_md_cell("""\
> **Key Concept 10.13: Incremental Predictive Power**
>
> When adding predictors to a regression model, $R^2$ can only increase or stay the same — it never decreases. This makes $R^2$ misleading for model comparison when models have different numbers of predictors. **Adjusted $R^2$** penalizes for additional variables, while **AIC** and **BIC** balance fit against complexity. In the satellite prediction context, adding all 64 embeddings would maximize $R^2$ but might overfit; information criteria help identify the most parsimonious model."""),

# ---------- Task 6 ----------
make_md_cell("""\
#### Task 6: Policy Brief on Satellite Prediction (Independent)

**Objective**: Write a 200-300 word policy brief summarizing the value of satellite embeddings for development prediction.

**Your brief should address:**
1. **Improvement**: How much does adding satellite embeddings improve development prediction compared to NTL alone?
2. **Complexity trade-off**: Is the improvement worth the added model complexity? What do adjusted $R^2$, AIC, and BIC suggest?
3. **Partial effects**: After controlling for embeddings, does NTL remain a significant predictor? What does the FWL theorem reveal about NTL's independent contribution?
4. **SDG monitoring implications**: How could multi-source satellite data enhance SDG monitoring in data-scarce countries like Bolivia?
5. **Limitations**: What can satellite data *not* capture about development? What are the risks of relying on abstract embedding features for policy decisions?

**Connection to Research**: The DS4Bolivia project uses all 64 embedding dimensions plus machine learning methods (Random Forest, XGBoost) to predict SDG indicators, achieving meaningful predictive accuracy. Your multiple regression analysis provides a transparent, interpretable baseline for comparison."""),

make_code_cell("""\
# Your code here: Additional analysis for the policy brief
#
# You might want to:
# 1. Create a summary table of key results across models
# 2. Generate a visualization comparing model fit
# 3. Calculate the percentage improvement in R² from adding embeddings
# 4. Discuss which embeddings contribute most to prediction
#
# Example:
# print("KEY RESULTS FOR POLICY BRIEF")
# print(f"NTL-only R²:          {model_1.rsquared:.4f}")
# print(f"NTL + 5 embed R²:     {model_3.rsquared:.4f}")
# print(f"R² improvement:       {(model_3.rsquared - model_1.rsquared) / model_1.rsquared * 100:.1f}%")
# print(f"NTL coef (bivariate): {model_1.params['ln_NTLpc2017']:.4f}")
# print(f"NTL coef (multiple):  {model_3.params['ln_NTLpc2017']:.4f}")"""),

# ---------- What You've Learned ----------
make_md_cell("""\
#### What You've Learned from This Case Study

Through this analysis of multiple satellite predictors of Bolivian municipal development, you've applied the full Chapter 10 toolkit to a cutting-edge research application:

- **Correlation analysis**: Explored the correlation structure among NTL, satellite embeddings, and development outcomes
- **Multiple regression**: Estimated models with multiple satellite predictors and interpreted partial effects
- **FWL theorem**: Demonstrated that the partial effect of NTL equals the coefficient from regressing residualized IMDS on residualized NTL
- **Model comparison**: Evaluated competing specifications using $R^2$, adjusted $R^2$, AIC, and BIC
- **Critical assessment**: Weighed the predictive gains from additional satellite features against model complexity

**Connection to upcoming chapters**: In Chapter 11, we'll test whether the satellite embeddings are *statistically* significant using F-tests for joint significance. In Chapter 12, we'll address robust inference and prediction intervals.

**This dataset returns throughout the textbook**: Each subsequent chapter applies its specific econometric tools to the DS4Bolivia data, building progressively toward a comprehensive satellite-based development prediction framework.

---

**Well done!** You've now analyzed how multiple satellite data sources can predict development outcomes, moving from simple bivariate regression (Chapter 1) to the richer multiple regression framework of Chapter 10."""),

]


def main():
    with open(NB_PATH, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    original_count = len(notebook['cells'])

    # ------------------------------------------------------------------
    # Step 1: Rename "### Case Study:" to "### Case Study 1:" if needed
    # ------------------------------------------------------------------
    for cell in notebook['cells']:
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            # Match "### Case Study:" without a number
            if '### Case Study:' in source and '### Case Study 1:' not in source and '### Case Study 2:' not in source:
                new_source = source.replace('### Case Study:', '### Case Study 1:')
                lines = new_source.split('\n')
                cell['source'] = [line + '\n' if i < len(lines) - 1 else line
                                  for i, line in enumerate(lines)]
                print("Renamed '### Case Study:' -> '### Case Study 1:'")
                break

    # ------------------------------------------------------------------
    # Step 2: Find insertion point — after "What You've Learned" closing
    #         of Case Study 1 (the Mendez convergence clubs case study)
    # ------------------------------------------------------------------
    insert_idx = None
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if "What You've Learned" in source and ("cross-country" in source.lower() or "productivity" in source.lower()):
                insert_idx = i + 1
                break

    if insert_idx is None:
        # Fallback: look for the last "What You've Learned" before Practice Exercises/end
        for i, cell in enumerate(notebook['cells']):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                if "What You've Learned" in source and "chapters ahead" in source.lower():
                    insert_idx = i + 1
                    break

    if insert_idx is None:
        # Last resort: insert before the final empty cell
        insert_idx = len(notebook['cells']) - 1
        print(f"WARNING: Could not find Case Study 1 closing. Inserting at index {insert_idx}")

    print(f"Inserting {len(cells_to_add)} cells at index {insert_idx}")

    # ------------------------------------------------------------------
    # Step 3: Insert cells
    # ------------------------------------------------------------------
    for j, cell in enumerate(cells_to_add):
        notebook['cells'].insert(insert_idx + j, cell)

    # ------------------------------------------------------------------
    # Step 4: Write modified notebook
    # ------------------------------------------------------------------
    with open(NB_PATH, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
        f.write('\n')

    print(f"Done! Notebook now has {len(notebook['cells'])} cells (was {original_count})")


if __name__ == '__main__':
    main()
