# Before/After Examples

Concrete examples for each readability category. Use these as templates when suggesting improvements.

---

## Category 1: Code Cell Clarity

### 1A. Setup cell annotation

**BEFORE:**

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import random
import os

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)

GITHUB_DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

IMAGES_DIR = 'images'
TABLES_DIR = 'tables'
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

plt.style.use('dark_background')
plt.rcParams.update({
    'axes.facecolor': '#1a2235',
    ...
})
```

**AFTER:**

```python
# --- Libraries ---
import numpy as np                        # numerical operations
import pandas as pd                       # data manipulation
import matplotlib.pyplot as plt           # plotting
import statsmodels.api as sm              # statistical models
from statsmodels.formula.api import ols   # OLS with formula syntax
import random
import os

# --- Reproducibility ---
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)

# --- Data source ---
GITHUB_DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

# --- Output directories (for saving figures/tables locally) ---
IMAGES_DIR = 'images'
TABLES_DIR = 'tables'
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# --- Plotting style (dark theme matching book design) ---
plt.style.use('dark_background')
plt.rcParams.update({
    'axes.facecolor': '#1a2235',
    ...
})
```

### 1C. Magic numbers

**BEFORE:**

```python
ax.scatter(x, y, color='#22d3ee', s=50, alpha=0.7)
```

**AFTER:**

```python
ax.scatter(x, y, color='#22d3ee', s=50, alpha=0.7)  # s = marker size, alpha = transparency
```

**BEFORE:**

```python
ci_lower = mean - 1.96 * se
ci_upper = mean + 1.96 * se
```

**AFTER:**

```python
z_crit = 1.96  # 95% CI: P(-1.96 < Z < 1.96) = 0.95
ci_lower = mean - z_crit * se
ci_upper = mean + z_crit * se
```

**BEFORE:**

```python
t_crit = stats.t.ppf(0.975, df)
```

**AFTER:**

```python
# 0.975 = upper tail for 95% two-sided CI (2.5% in each tail)
t_crit = stats.t.ppf(0.975, df)
```

### 1E. Raw `.summary()` without key extraction

**BEFORE:**

```python
model = ols('price ~ size', data=data_house).fit()
model.summary()
```

**AFTER:**

```python
model = ols('price ~ size', data=data_house).fit()

# Key results
intercept = model.params['Intercept']
slope     = model.params['size']
r_squared = model.rsquared

print(f"Estimated equation: price = {intercept:,.0f} + {slope:.2f} x size")
print(f"Slope: each additional sq ft is associated with ${slope:,.2f} higher price")
print(f"R-squared: {r_squared:.4f} ({r_squared*100:.1f}% of variation explained)")

# Full regression output
model.summary()
```

---

## Category 2: Explanation Ordering

### 2A. Formula before intuition

**BEFORE:**

```markdown
Under the assumption of a simple random sample:

$$E[\bar{X}] = \mu$$

This means the expected value of the sample mean equals the population mean.
```

**AFTER:**

```markdown
On average, sample means equal the true population mean. If you repeated
your survey many times and averaged all the sample means, you'd get exactly μ.

Mathematically:

$$E[\bar{X}] = \mu$$
```

### 2B. Code before context

**BEFORE:**

```markdown
## 5.3 Correlation

​```{python}
r = data['price'].corr(data['size'])
print(f"Correlation: {r:.4f}")
​```
```

**AFTER:**

```markdown
## 5.3 Correlation

Let's quantify the strength of the linear relationship between price and size using the correlation coefficient.

​```{python}
r = data['price'].corr(data['size'])
print(f"Correlation: {r:.4f}")
​```
```

---

## Category 3: Interpretation Guidance

### 3A. Visualizations without "what to look for"

**BEFORE:**

```markdown
​```{python}
ax.scatter(data['size'], data['price'])
plt.show()
​```

> **Key Concept 5.1: Scatter Plots**
> ...
```

**AFTER:**

```markdown
​```{python}
ax.scatter(data['size'], data['price'])
plt.show()
​```

**What to look for in this scatter plot:**

- **Direction**: Positive — larger houses tend to have higher prices
- **Form**: Roughly linear — the points follow an upward-sloping pattern
- **Scatter**: Not all points lie exactly on a line — this variation is the "error" that regression cannot explain

> **Key Concept 5.1: Scatter Plots**
> ...
```

### 3B. Interpretation buried in code comments

**BEFORE:**

```python
ax.scatter(data['size'], data['price'])
plt.show()

# What do you see?
# - Positive relationship: Larger houses tend to have higher prices
# - Roughly linear: The points follow an upward-sloping pattern
# - Some scatter: Not all points lie exactly on a line
```

**AFTER:**

```python
ax.scatter(data['size'], data['price'])
plt.show()
```

Then in a new markdown cell:

```markdown
**What to look for:**

- **Direction**: Positive — larger houses tend to have higher prices
- **Form**: Roughly linear — the points follow an upward-sloping pattern
- **Scatter**: Not all points lie on a line — this is the "error"
```

---

## Category 4: Regression Output

### 4A. Summary table shown first

(Same as 1E example above — extract key numbers, print interpretation, then show full summary.)

### 4B. No interpretation bridge

**BEFORE:**

```markdown
​```{python}
model.summary()
​```

## 5.6 Next Section
```

**AFTER:**

```markdown
​```{python}
model.summary()
​```

We already extracted the key numbers above. Here's how to read them:

- **Intercept** (β₀ = $115,952): The predicted price when size = 0. Not economically meaningful, but anchors the line.
- **Slope** (β₁ = $73.77/sq ft): Our main result — each additional square foot is associated with $73.77 higher price.
- **R-squared** (0.6175): House size explains about 62% of price variation.

## 5.6 Next Section
```

---

## Category 5: Prose Quality

### 5A. Passive voice in introductions

**BEFORE:**

```markdown
## 3.4 The Central Limit Theorem

The distribution of sample means is examined in this section. It is shown that...
```

**AFTER:**

```markdown
## 3.4 The Central Limit Theorem

Let's examine how sample means are distributed. We'll discover that...
```

### 5B. Orphaned transitions

**BEFORE:**

```markdown
Having visualized a clear positive relationship between house size and price,
we're ready to quantify this relationship precisely using regression analysis.

> **Key Concept 1.3: Visual Exploration Before Regression**
```

**AFTER:**

(Remove the orphaned sentence entirely — the Key Concept box provides the transition.)

```markdown
> **Key Concept 1.3: Visual Exploration Before Regression**
```

### 5C. Walls of text

**BEFORE:**

```markdown
Economics primarily uses observational data where we observe economic behavior in
uncontrolled settings rather than experimental data. Unlike experimental data where
the researcher can control conditions and randomly assign treatments, observational
data requires careful statistical methods to establish relationships between variables
and, when possible, causal effects. The three main types of data collection in
economics are cross-section data which observes many individuals at a single point
in time, time series data which tracks a single entity over multiple time periods,
and panel data which combines both dimensions by tracking multiple entities over time.
```

**AFTER:**

```markdown
Economics primarily uses **observational data** — we observe economic behavior in
uncontrolled settings, rather than running experiments.

The three main types of economic data:

- **Cross-section**: Many individuals at one point in time
- **Time series**: One entity tracked over multiple periods
- **Panel data**: Multiple entities tracked over time (combines both)

Because we can't run controlled experiments, we need careful statistical methods
to establish relationships and (when possible) causal effects.
```

---

## Category 6: Jargon Management

### 6A. Terms used before definition

**BEFORE:**

```markdown
We estimate the model using OLS and examine the heteroskedasticity-robust
standard errors.
```

**AFTER:**

```markdown
We estimate the model using **OLS (Ordinary Least Squares)** — the method that
finds the line minimizing squared prediction errors. We use
**heteroskedasticity-robust standard errors** (standard errors that remain valid
even when error variance differs across observations; see Chapter 7).
```

### 6B. Missing cross-references

**BEFORE:**

```markdown
As we discussed earlier, the t-distribution has heavier tails than the normal.
```

**AFTER:**

```markdown
The t-distribution has heavier tails than the normal (see Chapter 4, Section 4.2),
meaning extreme values are more likely when sample sizes are small.
```
