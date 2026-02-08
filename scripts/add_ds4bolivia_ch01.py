#!/usr/bin/env python3
"""Add DS4Bolivia Case Study 2 to CH01 notebook."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = PROJECT_ROOT / 'notebooks_colab' / 'ch01_Analysis_of_Economics_Data.ipynb'


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
### Case Study 2: Can Satellites See Poverty? Predicting Local Development in Bolivia

**Research Question**: Can satellite data—nighttime lights and satellite image embeddings—predict local economic development across Bolivia's municipalities?

**Background**: Monitoring progress toward the United Nations Sustainable Development Goals (SDGs) requires timely, granular data on economic conditions. However, many developing countries lack comprehensive municipality-level statistics. Recent advances in remote sensing and machine learning offer a promising alternative: using satellite data to *predict* local development outcomes.

Two types of satellite data have proven particularly useful:

1. **Nighttime lights (NTL)**: Satellite images of Earth at night reveal the intensity of artificial lighting. Brighter areas typically correspond to greater economic activity, electrification, and urbanization. NTL data is available globally and annually, making it a powerful proxy for economic development in data-scarce regions ([Henderson et al., 2012](https://doi.org/10.1257/aer.102.2.994)).

2. **Satellite image embeddings**: Deep learning models trained on daytime satellite imagery (Sentinel-2, Landsat) can extract 64-dimensional feature vectors that capture visual patterns—road networks, building density, vegetation cover, agricultural activity—without requiring manual labeling. These abstract features often correlate strongly with socioeconomic outcomes ([Jean et al., 2016](https://doi.org/10.1126/science.aaf7894)).

**This Research** ([DS4Bolivia Project](https://github.com/quarcs-lab/ds4bolivia)): A comprehensive data science initiative that integrates satellite data with Bolivia's Municipal SDG Atlas ([Andersen et al., 2020](https://atlas.sdsnbolivia.org)) to study geospatial development patterns across all **339 municipalities**. The project demonstrates how machine learning models can predict SDG indicators from satellite features, achieving meaningful predictive accuracy for poverty and energy access indicators.

**The Data**: Cross-sectional dataset covering 339 Bolivian municipalities with over 350 variables, including:
- **Development outcomes**: Municipal Sustainable Development Index (IMDS, 0-100 composite), individual SDG indices (SDG 1-17)
- **Satellite data**: Log nighttime lights per capita (2012-2020), 64 satellite embedding dimensions (2017)
- **Demographics**: Population (2001-2020), municipality and department names
- **Socioeconomic indicators**: Unsatisfied basic needs, literacy rates, electricity coverage, health outcomes

**Your Task**: Use the descriptive analysis and regression tools from Chapter 1 to explore the DS4Bolivia dataset. You'll investigate whether nighttime lights predict municipal development, visualize satellite-development relationships, and begin to assess how useful remote sensing data is for SDG monitoring. This case study introduces a dataset that we will revisit throughout the textbook, applying increasingly sophisticated econometric methods in each chapter."""),

# ---------- Key Concept 1.9 ----------
make_md_cell("""\
> **Key Concept 1.9: Satellite Data as Economic Proxy**
>
> **Nighttime lights (NTL)** captured by satellites measure the intensity of artificial illumination on Earth's surface. Because lighting requires electricity and economic activity, NTL intensity strongly correlates with GDP, income levels, and urbanization. The log of NTL per capita transforms the highly skewed raw luminosity into a more symmetric variable suitable for regression analysis.
>
> **Satellite embeddings** are 64-dimensional feature vectors extracted by deep learning models from daytime satellite imagery. Each dimension captures abstract visual patterns (building density, road networks, vegetation) that correlate with socioeconomic conditions. Together, NTL and embeddings provide complementary information: NTL captures *nighttime economic activity* while embeddings capture *daytime physical infrastructure*."""),

# ---------- Load Data ----------
make_md_cell("""\
#### Load the DS4Bolivia Data

Let's load the comprehensive DS4Bolivia dataset directly from GitHub. This dataset integrates satellite data, SDG indicators, and demographic information for all 339 Bolivian municipalities."""),

make_code_cell("""\
# Load the DS4Bolivia dataset
url_bol = "https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv"
bol = pd.read_csv(url_bol)

# Display basic information
print("=" * 70)
print("DS4BOLIVIA DATASET")
print("=" * 70)
print(f"Dataset shape: {bol.shape[0]} municipalities, {bol.shape[1]} variables")
print(f"\\nDepartments: {bol['dep'].nunique()} unique departments")
print(f"Department names: {sorted(bol['dep'].unique())}")

# Select key variables for this case study
key_vars = ['mun', 'dep', 'imds', 'ln_NTLpc2017', 'pop2017',
            'index_sdg1', 'index_sdg4', 'index_sdg8', 'sdg1_1_ubn']
bol_key = bol[key_vars].copy()

print(f"\\nKey variables selected: {len(key_vars)}")
print("\\n" + "=" * 70)
print("FIRST 10 MUNICIPALITIES")
print("=" * 70)
print(bol_key.head(10))"""),

make_code_cell("""\
# Variable descriptions for this case study
print("=" * 70)
print("KEY VARIABLE DESCRIPTIONS")
print("=" * 70)
descriptions = {
    'mun': 'Municipality name',
    'dep': 'Department (administrative region, 9 total)',
    'imds': 'Municipal Sustainable Development Index (0-100, composite of all SDGs)',
    'ln_NTLpc2017': 'Log of nighttime lights per capita (2017, satellite-based)',
    'pop2017': 'Population in 2017',
    'index_sdg1': 'SDG 1 Index: No Poverty (0-100)',
    'index_sdg4': 'SDG 4 Index: Quality Education (0-100)',
    'index_sdg8': 'SDG 8 Index: Decent Work and Economic Growth (0-100)',
    'sdg1_1_ubn': 'Unsatisfied Basic Needs (% of population, 2012)',
}
for var, desc in descriptions.items():
    print(f"  {var:20s} — {desc}")"""),

# ---------- Task 1 ----------
make_md_cell("""\
#### Task 1: Data Exploration (Guided)

**Objective**: Understand the DS4Bolivia dataset structure and key variables.

**Instructions**:
1. Examine the output above: How many municipalities? How many departments?
2. Check for missing values in the key variables
3. Identify the range of the IMDS index (development measure)
4. Explore the distribution of departments (how many municipalities per department?)

**Key variables to focus on**:
- `imds`: Overall development index (our main dependent variable)
- `ln_NTLpc2017`: Log nighttime lights per capita (our main predictor)
- `dep`: Department (for regional comparisons)
- `pop2017`: Population (for context)

Run the code below to explore the data structure."""),

make_code_cell("""\
# Your code here: Explore the DS4Bolivia dataset
#
# Suggested explorations:
# 1. Check for missing values: bol_key.isnull().sum()
# 2. Municipalities per department: bol_key['dep'].value_counts()
# 3. Range of IMDS: bol_key['imds'].describe()
# 4. Largest/smallest municipalities: bol_key.nlargest(5, 'pop2017')

# Example: Check missing values
print("Missing values per variable:")
print(bol_key.isnull().sum())
print(f"\\nTotal municipalities: {len(bol_key)}")
print(f"Complete cases (no missing in key vars): {bol_key.dropna().shape[0]}")"""),

# ---------- Task 2 ----------
make_md_cell("""\
#### Task 2: Descriptive Statistics (Guided)

**Objective**: Generate summary statistics for key development and satellite variables.

**Instructions**:
1. Calculate descriptive statistics for `imds`, `ln_NTLpc2017`, and `pop2017`
2. Identify the municipality with the highest and lowest IMDS
3. Compare average IMDS across departments
4. Discuss what the summary statistics reveal about inequality across municipalities

**Apply what you learned in section 1.4**: Use `.describe()` and `.groupby()` methods like we did with the house price data."""),

make_code_cell("""\
# Your code here: Descriptive statistics for DS4Bolivia
#
# Steps:
# 1. Summary statistics for key variables
# 2. Identify top/bottom municipalities
# 3. Compare departments

# Example: Summary statistics
print("=" * 70)
print("DESCRIPTIVE STATISTICS: KEY VARIABLES")
print("=" * 70)
print(bol_key[['imds', 'ln_NTLpc2017', 'pop2017', 'sdg1_1_ubn']].describe().round(2))

# Top and bottom municipalities by IMDS
print("\\n" + "=" * 70)
print("TOP 5 MUNICIPALITIES BY DEVELOPMENT (IMDS)")
print("=" * 70)
print(bol_key.nlargest(5, 'imds')[['mun', 'dep', 'imds', 'ln_NTLpc2017']].to_string(index=False))

print("\\n" + "=" * 70)
print("BOTTOM 5 MUNICIPALITIES BY DEVELOPMENT (IMDS)")
print("=" * 70)
print(bol_key.nsmallest(5, 'imds')[['mun', 'dep', 'imds', 'ln_NTLpc2017']].to_string(index=False))"""),

# ---------- Key Concept 1.10 ----------
make_md_cell("""\
> **Key Concept 1.10: Subnational Development Analysis**
>
> National-level statistics can mask enormous variation in development outcomes within a country. Bolivia's 339 municipalities span a wide range of development levels—from highly urbanized departmental capitals with strong infrastructure to remote rural communities with limited services. Municipality-level analysis reveals this **within-country inequality** and helps identify specific areas where SDG progress lags behind. Satellite data is particularly valuable for subnational analysis because it provides spatially granular measurements even where traditional surveys are scarce or infrequent."""),

# ---------- Task 3 ----------
make_md_cell("""\
#### Task 3: Visualize the NTL-Development Relationship (Semi-guided)

**Objective**: Create scatter plots to visualize the relationship between nighttime lights and development.

**Instructions**:
1. Create a scatter plot of `ln_NTLpc2017` (x-axis) vs `imds` (y-axis)
2. Add appropriate axis labels and title
3. Optionally: Color-code points by department
4. Interpret the pattern: Is there a positive relationship? How strong does it look?

**Apply what you learned in section 1.5**: Use matplotlib to create scatter plots like the house price visualization.

**Hint**: Drop missing values before plotting with `.dropna()`"""),

make_code_cell("""\
# Your code here: Scatter plot of NTL vs Development
#
# Steps:
# 1. Prepare data (drop missing values)
# 2. Create scatter plot
# 3. Add labels and formatting
# 4. Interpret the pattern

# Example structure:
# plot_data = bol_key[['ln_NTLpc2017', 'imds']].dropna()
# fig, ax = plt.subplots(figsize=(10, 6))
# ax.scatter(plot_data['ln_NTLpc2017'], plot_data['imds'], alpha=0.5, color='navy')
# ax.set_xlabel('Log Nighttime Lights per Capita (2017)')
# ax.set_ylabel('Municipal Development Index (IMDS)')
# ax.set_title('Can Satellites See Development? NTL vs IMDS in Bolivia')
# plt.show()"""),

# ---------- Task 4 ----------
make_md_cell("""\
#### Task 4: Simple Regression Analysis (Semi-guided)

**Objective**: Estimate the relationship between nighttime lights and development using OLS.

**Research Question**: How much does nighttime light intensity predict municipal development levels?

**Instructions**:
1. Prepare regression data (drop missing values in key variables)
2. Estimate OLS regression: `imds ~ ln_NTLpc2017`
3. Display the regression summary
4. Interpret the slope coefficient: What does a 1-unit increase in log NTL mean for IMDS?
5. Report and interpret R-squared: How much variation in development does NTL explain?

**Apply what you learned in sections 1.6-1.7**: Use `ols()` from statsmodels."""),

make_code_cell("""\
# Your code here: OLS regression of IMDS on NTL
#
# Steps:
# 1. Prepare data
# 2. Estimate regression
# 3. Display and interpret results

# Example structure:
# reg_data = bol_key[['imds', 'ln_NTLpc2017']].dropna()
# model_bol = ols('imds ~ ln_NTLpc2017', data=reg_data).fit()
# print(model_bol.summary())
#
# # Extract key statistics
# print(f"\\nSlope: {model_bol.params['ln_NTLpc2017']:.4f}")
# print(f"R-squared: {model_bol.rsquared:.4f}")
# print(f"\\nInterpretation: A 1-unit increase in log NTL per capita")
# print(f"is associated with a {model_bol.params['ln_NTLpc2017']:.2f}-point increase in IMDS")"""),

# ---------- Task 5 ----------
make_md_cell("""\
#### Task 5: Regional Comparison (Independent)

**Objective**: Compare development and NTL patterns across Bolivia's nine departments.

**Research Question**: Do satellite-development patterns vary across Bolivia's regions?

**Instructions**:
1. Calculate mean IMDS and mean NTL by department
2. Create a bar chart or dot plot comparing department averages
3. Identify which departments are the most and least developed
4. Create scatter plots colored by department to see if the NTL-IMDS relationship differs by region
5. Discuss what might explain regional differences (geography, urbanization, economic structure)

**This extends Chapter 1 concepts**: You're using grouping and comparative analysis to explore heterogeneity."""),

make_code_cell("""\
# Your code here: Regional comparison
#
# Steps:
# 1. Group by department: bol_key.groupby('dep')[['imds', 'ln_NTLpc2017']].mean()
# 2. Create comparative bar chart
# 3. Create scatter plot colored by department
# 4. Identify top/bottom departments

# Example structure:
# dept_means = bol_key.groupby('dep')[['imds', 'ln_NTLpc2017']].mean().sort_values('imds')
# print(dept_means.round(2))
#
# fig, ax = plt.subplots(figsize=(10, 6))
# dept_means['imds'].plot(kind='barh', ax=ax, color='purple', alpha=0.7)
# ax.set_xlabel('Mean IMDS')
# ax.set_title('Average Municipal Development by Department')
# plt.tight_layout()
# plt.show()"""),

# ---------- Task 6 ----------
make_md_cell("""\
#### Task 6: Policy Brief on Satellite Data for SDG Monitoring (Independent)

**Objective**: Write a 200-300 word policy brief summarizing your findings.

**Your brief should address**:
1. **Key finding**: What is the relationship between nighttime lights and municipal development in Bolivia?
2. **Magnitude**: How strong is the association? What does the R-squared tell us about predictive power?
3. **Regional variation**: Do some departments show higher development levels? Is there a geographic pattern?
4. **Policy implications**: How could satellite data be used for SDG monitoring in Bolivia?
5. **Limitations**: What can satellite data *not* tell us about development? What other data sources are needed?

**Connection to Research**: The DS4Bolivia project uses machine learning (Random Forest, XGBoost) to predict SDG indicators from satellite embeddings, achieving R² up to 0.57 for extreme energy poverty. Your simple OLS regression provides a baseline for understanding how much satellite data captures about development outcomes.

**Looking ahead**: In subsequent chapters, we will revisit this dataset to:
- Summarize the distribution of development indicators (Chapter 2)
- Test whether development differences are statistically significant (Chapter 4)
- Explore bivariate relationships between NTL and specific SDG outcomes (Chapter 5)
- Add multiple satellite features as predictors (Chapters 10-12)
- Test for regional structural differences (Chapter 14)
- Check model assumptions and diagnostics (Chapter 16)
- Analyze NTL panel data over time (Chapter 17)"""),

make_code_cell("""\
# Your code here: Additional analysis for the policy brief
#
# You might want to:
# 1. Create a summary table of key results
# 2. Generate a visualization that tells a compelling story
# 3. Calculate specific statistics to cite in your brief

# Example: Summary of key results
# print("KEY RESULTS FOR POLICY BRIEF")
# print(f"Sample: {len(reg_data)} municipalities")
# print(f"NTL coefficient: {model_bol.params['ln_NTLpc2017']:.2f}")
# print(f"R-squared: {model_bol.rsquared:.2%}")
# print(f"Most developed department: {dept_means['imds'].idxmax()}")
# print(f"Least developed department: {dept_means['imds'].idxmin()}")"""),

# ---------- What You've Learned ----------
make_md_cell("""\
#### What You've Learned from This Case Study

Through this exploration of satellite data and municipal development in Bolivia, you've applied the Chapter 1 toolkit to a cutting-edge research application:

- **Data loading and exploration**: Worked with a real geospatial dataset covering 339 municipalities
- **Descriptive statistics**: Summarized development indicators and identified high/low performers
- **Visualization**: Created scatter plots revealing the satellite-development relationship
- **Regression analysis**: Quantified how nighttime lights predict development outcomes
- **Regional comparison**: Explored how the relationship varies across Bolivia's departments
- **Critical thinking**: Assessed the potential and limitations of satellite data for SDG monitoring

**Connection to the research**: The DS4Bolivia project extends this simple analysis by incorporating 64-dimensional satellite embeddings and advanced machine learning methods. Your OLS baseline provides the foundation for understanding what these more complex models improve upon.

**This dataset returns throughout the textbook**: Each subsequent chapter applies its specific econometric tools to the DS4Bolivia data, building progressively from univariate summaries (Chapter 2) through panel data analysis (Chapter 17). By the end of the book, you'll have a comprehensive econometric analysis of satellite-based development prediction.

---

**Well done!** You've now explored two real-world datasets—cross-country convergence and Bolivian municipal development—using the fundamental tools of econometrics."""),

]


def main():
    with open(NB_PATH, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # Find insertion point: after cell with "What You've Learned from This Case Study"
    # which is the closing of Case Study 1 (cell 54 based on our exploration)
    insert_idx = None
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if "What You've Learned from This Case Study" in source and "convergence" in source.lower():
                insert_idx = i + 1
                break

    if insert_idx is None:
        # Fallback: insert before the last empty cell
        insert_idx = len(notebook['cells']) - 1
        print(f"WARNING: Could not find Case Study 1 closing. Inserting at index {insert_idx}")

    print(f"Inserting {len(cells_to_add)} cells at index {insert_idx}")

    # Insert cells
    for j, cell in enumerate(cells_to_add):
        notebook['cells'].insert(insert_idx + j, cell)

    # Write modified notebook
    with open(NB_PATH, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
        f.write('\n')

    print(f"Done! Notebook now has {len(notebook['cells'])} cells (was {len(notebook['cells']) - len(cells_to_add)})")


if __name__ == '__main__':
    main()
