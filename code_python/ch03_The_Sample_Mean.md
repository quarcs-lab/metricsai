# Chapter 3: The Sample Mean - Python Script Report

> **Data Science Report Template**
> This template follows the **Code → Results → Interpretation** structure for educational data science reporting.

## Introduction

This report demonstrates the fundamental statistical concepts surrounding the **sample mean**—one of the most important estimators in statistics and econometrics. Chapter 3 explores how sample means behave when we repeatedly draw samples from a population, introducing key concepts like the **sampling distribution**, **Central Limit Theorem**, and **properties of estimators**.

We investigate three different sampling scenarios:
1. **Coin tosses**: Controlled experiment with known probability (p = 0.5)
2. **1880 U.S. Census**: Sampling from a finite population of real-world age data
3. **Computer simulations**: Generating random samples from theoretical distributions

**Learning Objectives:**

- Understand the concept of the sampling distribution of the sample mean
- Explore the Central Limit Theorem through simulations and real data
- Learn about unbiasedness: why E[x̄] = μ
- Understand the standard error: how σ_x̄ = σ/√n
- Gain practical experience generating random samples using Python
- Compare empirical distributions with theoretical predictions

---

## 1. Setup and Environment Configuration

### 1.1 Code

```python
# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import random
import os

# Set random seeds for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)

# GitHub data URL
GITHUB_DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

# Create output directories
IMAGES_DIR = 'images'
TABLES_DIR = 'tables'
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
```

### 1.2 Results

```
Environment configured successfully:
- Random seed: 42 (for reproducibility)
- Data source: GitHub repository (streaming)
- Output directories: images/ and tables/
- Plotting style: whitegrid with 10x6 figure size
```

### 1.3 Interpretation

**Reproducibility**: Setting `RANDOM_SEED = 42` ensures that all random number generation (coin tosses, random samples) produces identical results every time the script runs. This is crucial for teaching, debugging, and scientific reproducibility.

**Data streaming**: Rather than requiring local data files, the script streams datasets directly from GitHub. This makes the code more portable and eliminates file path issues.

**Environment variables**: Setting `PYTHONHASHSEED` ensures that Python's internal hash functions also use the same seed, providing complete reproducibility across different Python sessions and platforms.

**Why this matters**: When studying sampling distributions, we need to verify that our empirical results match theoretical predictions. Reproducible random number generation allows us to confirm that observed patterns are consistent, not artifacts of random variation.

---

## 2. Coin Tosses - Single Sample

### 2.1 Code

```python
# Draw one sample of size 30 from Bernoulli with p = 0.5
np.random.seed(10101)
u = np.random.uniform(0, 1, 30)
x = np.where(u > 0.5, 1, 0)

print("\nSingle coin toss sample (n=30):")
print(f"Number of heads (x=1): {np.sum(x)}")
print(f"Number of tails (x=0): {np.sum(1-x)}")
print(f"Sample mean: {np.mean(x):.4f}")
print(f"Sample std dev: {np.std(x, ddof=1):.4f}")

# Create histogram of single sample
fig, ax = plt.subplots(figsize=(8, 6))
ax.hist(x, bins=[-0.5, 0.5, 1.5], edgecolor='black', alpha=0.7, color='steelblue')
ax.set_xlabel('Heads = 1 and Tails = 0', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Figure 3.1 Panel A: Single Sample of 30 Coin Tosses',
             fontsize=14, fontweight='bold')
ax.set_xticks([0, 1])
ax.grid(True, alpha=0.3, axis='y')

output_file = os.path.join(IMAGES_DIR, 'ch03_fig1a_single_coin_toss_sample.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.close()
```

### 2.2 Results

```
Single coin toss sample (n=30):
Number of heads (x=1): 12
Number of tails (x=0): 18
Sample mean: 0.4000
Sample std dev: 0.4983
```

![Figure 3.1 Panel A: Single Sample of 30 Coin Tosses](images/ch03_fig1a_single_coin_toss_sample.png)

### 2.3 Interpretation

**Sample vs. Population**: Even though the coin is fair (p = 0.5 for heads), this particular sample of 30 tosses yielded only 12 heads (40%), demonstrating **sampling variability**. The sample mean (0.40) differs from the true population mean (0.50).

**Bernoulli random variable**: We code heads as 1 and tails as 0. For a Bernoulli(0.5) random variable:
- Population mean: μ = p = 0.5
- Population variance: σ² = p(1-p) = 0.25
- Population std dev: σ = 0.5

**Sample statistics**: The sample standard deviation (0.4983) is close to the theoretical value (0.5), showing that even a single sample can provide useful information about population variability.

**Why this example**: Coin tosses provide the simplest possible random variable (only two outcomes), making them ideal for understanding fundamental sampling concepts. The known true probability (p = 0.5) lets us compare sample statistics with exact theoretical values.

---

## 3. Distribution of Sample Means - Coin Tosses

### 3.1 Code

```python
# Read in data for 400 coin toss samples
data_cointoss = pd.read_stata(GITHUB_DATA_URL + 'AED_COINTOSSMEANS.DTA')

print("Coin toss means data (400 samples of size 30):")
cointoss_summary = data_cointoss.describe()
print(cointoss_summary)
print("\nFirst 5 observations:")
print(data_cointoss.head())
cointoss_summary.to_csv(os.path.join(TABLES_DIR, 'ch03_cointoss_descriptive_stats.csv'))

xbar = data_cointoss['xbar']

# Create histogram with normal overlay
fig, ax = plt.subplots(figsize=(10, 6))

# Histogram of sample means
n, bins, patches = ax.hist(xbar, bins=30, density=True,
                            edgecolor='black', alpha=0.7, color='steelblue',
                            label='Sample means')

# Overlay normal distribution
xbar_range = np.linspace(xbar.min(), xbar.max(), 100)
normal_pdf = stats.norm.pdf(xbar_range, xbar.mean(), xbar.std())
ax.plot(xbar_range, normal_pdf, 'r-', linewidth=2,
        label=f'Normal({xbar.mean():.3f}, {xbar.std():.3f})')

ax.set_xlabel('Sample mean from each of 400 samples', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('Figure 3.1 Panel B: Distribution of Sample Means (400 samples)',
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch03_fig1b_distribution_sample_means.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.close()

print(f"\nSample mean of the 400 sample means: {xbar.mean():.4f}")
print(f"Standard deviation of the 400 sample means: {xbar.std():.4f}")
print(f"Theoretical: μ = 0.5, σ/√n = √(0.25/30) = {np.sqrt(0.25/30):.4f}")
```

### 3.2 Results

**Summary Statistics for 400 Sample Means:**

| Statistic | xbar | stdev | numobs |
|-----------|------|-------|--------|
| count | 400.0 | 400.0 | 400.0 |
| mean | 0.499 | 0.501 | 30.0 |
| std | 0.086 | 0.010 | 0.0 |
| min | 0.267 | 0.450 | 30.0 |
| 25% | 0.433 | 0.498 | 30.0 |
| 50% | 0.500 | 0.504 | 30.0 |
| 75% | 0.567 | 0.507 | 30.0 |
| max | 0.733 | 0.508 | 30.0 |

```
Sample mean of the 400 sample means: 0.4994
Standard deviation of the 400 sample means: 0.0863
Theoretical: μ = 0.5, σ/√n = √(0.25/30) = 0.0913
```

![Figure 3.1 Panel B: Distribution of Sample Means](images/ch03_fig1b_distribution_sample_means.png)

### 3.3 Interpretation

**Central Limit Theorem in action**: The histogram shows that the distribution of sample means is approximately normal, even though the underlying data (coin tosses) follow a Bernoulli distribution (decidedly non-normal). This demonstrates the **Central Limit Theorem**: for large enough sample sizes, the sampling distribution of the mean approaches normality.

**Unbiasedness verified**: The mean of the 400 sample means (0.4994) is extremely close to the true population mean (0.5000). This empirically demonstrates that the sample mean is an **unbiased estimator**: E[x̄] = μ.

**Standard error**: The standard deviation of the sample means (0.0863) measures the **standard error** of the estimator. Theory predicts:

σ_x̄ = σ/√n = 0.5/√30 = 0.0913

Our empirical value (0.0863) is close to this theoretical prediction, with the small difference due to sampling variation in our 400 samples.

**Efficiency**: Notice how the distribution of sample means (std = 0.0863) is much tighter than individual coin tosses (std = 0.5). By averaging 30 observations, we reduce uncertainty by a factor of √30 ≈ 5.48. This shows why larger samples provide more precise estimates.

**Why 400 samples**: Drawing 400 samples allows us to construct an accurate empirical sampling distribution. With fewer samples, the histogram would be too sparse; with more, we'd gain little additional insight while increasing computation time.

---

## 4. Census Data - Sampling from a Finite Population

### 4.1 Code

```python
# Read in census age means data
data_census = pd.read_stata(GITHUB_DATA_URL + 'AED_CENSUSAGEMEANS.DTA')

print("\nCensus age means data (100 samples of size 25):")
census_summary = data_census.describe()
print(census_summary)
print("\nFirst 5 observations:")
print(data_census.head())
census_summary.to_csv(os.path.join(TABLES_DIR, 'ch03_census_descriptive_stats.csv'))

# Get the mean variable
if 'mean' in data_census.columns:
    age_means = data_census['mean']
elif 'xmean' in data_census.columns:
    age_means = data_census['xmean']
else:
    age_means = data_census.iloc[:, 0]

# Create histogram with normal overlay
fig, ax = plt.subplots(figsize=(10, 6))

# Histogram
n, bins, patches = ax.hist(age_means, bins=20, density=True,
                            edgecolor='black', alpha=0.7, color='coral',
                            label='Sample means')

# Overlay normal distribution
age_range = np.linspace(age_means.min(), age_means.max(), 100)
normal_pdf = stats.norm.pdf(age_range, age_means.mean(), age_means.std())
ax.plot(age_range, normal_pdf, 'b-', linewidth=2,
        label=f'Normal({age_means.mean():.2f}, {age_means.std():.2f})')

ax.set_xlabel('Sample mean age from each of 100 samples', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('Figure 3.3: Distribution of Sample Means from 1880 U.S. Census',
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch03_fig3_census_age_means.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.close()

print(f"\nMean of sample means: {age_means.mean():.2f}")
print(f"Standard deviation of sample means: {age_means.std():.2f}")
```

### 4.2 Results

**Summary Statistics for 100 Census Sample Means:**

| Statistic | mean | stdev | numobs |
|-----------|------|-------|--------|
| count | 100.0 | 100.0 | 100.0 |
| mean | 23.78 | 18.25 | 25.0 |
| std | 3.76 | 2.89 | 0.0 |
| min | 14.60 | 12.36 | 25.0 |
| 25% | 22.02 | 16.15 | 25.0 |
| 50% | 23.76 | 18.43 | 25.0 |
| 75% | 26.19 | 20.39 | 25.0 |
| max | 33.44 | 25.31 | 25.0 |

```
Mean of sample means: 23.78
Standard deviation of sample means: 3.76
```

![Figure 3.3: Distribution of Sample Means from 1880 U.S. Census](images/ch03_fig3_census_age_means.png)

### 4.3 Interpretation

**Real-world data**: Unlike the coin toss example with a known population, the 1880 U.S. Census represents a **finite population** of real individuals. Each sample of n=25 is drawn without replacement from this historical dataset.

**Normality with small samples**: The distribution of sample means appears approximately normal, even with only 100 samples (versus 400 for coin tosses). This suggests the underlying age distribution may be closer to normal than the highly skewed Bernoulli distribution of coin tosses.

**Mean of sample means**: The average across all 100 sample means is 23.78 years, which estimates the true population mean age in the 1880 census. The fact that this is quite young reflects historical demographic patterns—high birth rates and shorter life expectancies in the 19th century.

**Standard error**: The standard deviation of sample means (3.76) is the **standard error**, measuring how much sample means vary around the population mean. This is larger than the coin toss standard error (0.0863) because:
1. Age has higher inherent variability than binary coin tosses
2. Sample size is similar (n=25 vs n=30), so less averaging occurs

**Finite population correction**: When sampling without replacement from a finite population, the standard error formula needs adjustment. However, if the sample size is small relative to the population size (as with 25 individuals from thousands in the census), the standard √(σ²/n) approximation still works well.

**Historical context**: Using 1880 census data provides a concrete example of how sampling theory applies to real demographic research. Census bureaus routinely use sampling methods to estimate population characteristics between full enumerations.

---

## 5. Computer Generation of Random Samples

### 5.1 Code

```python
# Generate single samples from different distributions
np.random.seed(10101)
x_uniform = np.random.uniform(3, 9, 100)
y_normal = np.random.normal(5, 2, 100)

print("\nSingle sample from Uniform(3, 9):")
print(f"  Mean: {x_uniform.mean():.4f}, Std: {x_uniform.std():.4f}")
print(f"  Theoretical: Mean = 6.0, Std = {np.sqrt((9-3)**2/12):.4f}")

print("\nSingle sample from Normal(5, 2):")
print(f"  Mean: {y_normal.mean():.4f}, Std: {y_normal.std():.4f}")
print(f"  Theoretical: Mean = 5.0, Std = 2.0")
```

### 5.2 Results

```
Single sample from Uniform(3, 9):
  Mean: 6.1775, Std: 1.8002
  Theoretical: Mean = 6.0, Std = 1.7321

Single sample from Normal(5, 2):
  Mean: 5.0308, Std: 2.1279
  Theoretical: Mean = 5.0, Std = 2.0
```

### 5.3 Interpretation

**Uniform distribution**: The Uniform(3, 9) distribution assigns equal probability to all values between 3 and 9. The theoretical mean is (3+9)/2 = 6.0, and the theoretical standard deviation is (9-3)/√12 = 1.732. Our sample statistics (mean=6.18, std=1.80) are close but not identical—demonstrating sampling variability.

**Normal distribution**: The Normal(5, 2) distribution has mean μ=5 and standard deviation σ=2. Again, our sample statistics (mean=5.03, std=2.13) approximate but don't exactly match the theoretical values.

**Random number generation**: Modern programming languages use **pseudorandom number generators** (PRNGs) that produce sequences appearing random but are actually deterministic given a seed. The `np.random.seed(10101)` ensures reproducibility.

**Why multiple distributions**: Demonstrating uniform and normal distributions shows that random sample generation is a general tool, not limited to coin tosses. Different distributions model different real-world phenomena:
- **Uniform**: Random sampling from a bounded interval, lottery numbers
- **Normal**: Heights, IQ scores, measurement errors (by Central Limit Theorem)

**Sample size considerations**: With n=100, the Law of Large Numbers suggests sample means should be close to population means. We see this: both sample means are within one standard error of their true values.

---

## 6. Simulation - 400 Coin Toss Samples

### 6.1 Code

```python
# Simulate 400 coin toss samples each of size 30
print("Simulation: 400 samples of 30 coin tosses")

np.random.seed(10101)
n_simulations = 400
sample_size = 30

result_mean = np.zeros(n_simulations)
result_std = np.zeros(n_simulations)

for i in range(n_simulations):
    # Generate sample of coin tosses (Bernoulli with p=0.5)
    sample = np.random.binomial(1, 0.5, sample_size)
    result_mean[i] = sample.mean()
    result_std[i] = sample.std(ddof=1)

print(f"\nMean of the 400 sample means: {result_mean.mean():.4f}")
print(f"Std dev of the 400 sample means: {result_mean.std():.4f}")
print(f"Min: {result_mean.min():.4f}, Max: {result_mean.max():.4f}")

print(f"\nTheoretical values:")
print(f"  Expected value of sample mean: 0.5000")
print(f"  Expected std dev of sample mean: {np.sqrt(0.25/30):.4f}")

# Create visualization
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(result_mean, bins=30, density=True,
        edgecolor='black', alpha=0.7, color='lightgreen',
        label='Simulated sample means')

# Overlay theoretical normal distribution
x_range = np.linspace(result_mean.min(), result_mean.max(), 100)
theoretical_pdf = stats.norm.pdf(x_range, 0.5, np.sqrt(0.25/30))
ax.plot(x_range, theoretical_pdf, 'r-', linewidth=2,
        label='Theoretical Normal(0.5, 0.091)')

ax.set_xlabel('Sample mean', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('Simulated Distribution of Sample Means (400 simulations)',
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch03_simulated_sample_means.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.close()
```

### 6.2 Results

```
Simulation: 400 samples of 30 coin tosses

Mean of the 400 sample means: 0.5004
Std dev of the 400 sample means: 0.0887
Min: 0.2667, Max: 0.7667

Theoretical values:
  Expected value of sample mean: 0.5000
  Expected std dev of sample mean: 0.0913
```

![Simulated Distribution of Sample Means](images/ch03_simulated_sample_means.png)

### 6.3 Interpretation

**Monte Carlo simulation**: This code demonstrates a **Monte Carlo simulation**—using computer-generated random samples to study statistical properties. The loop generates 400 independent samples, each containing 30 coin tosses, and computes the sample mean for each.

**Verification of theory**: The empirical results closely match theoretical predictions:
- Mean of sample means: 0.5004 ≈ 0.5000 (unbiasedness)
- Std of sample means: 0.0887 ≈ 0.0913 (standard error formula)

The slight discrepancy (0.0887 vs 0.0913) is due to **simulation error**—with infinite simulations, these would converge exactly.

**Range of sample means**: The minimum (0.2667) and maximum (0.7667) show that even with n=30, individual sample means can deviate substantially from the true mean (0.5). This highlights the importance of:
1. **Understanding uncertainty**: A single sample mean might be quite far from the truth
2. **Confidence intervals**: We need to quantify this uncertainty (covered in later chapters)
3. **Larger samples**: Increasing n reduces the standard error and tightens the range

**Visual confirmation**: The histogram overlay with the theoretical normal distribution (red curve) shows excellent agreement. This visually confirms the Central Limit Theorem: even though individual coin tosses are Bernoulli (0 or 1), the distribution of sample means is approximately normal.

**Practical implications**: Simulation studies like this are crucial in modern statistics when analytical solutions are intractable. Researchers use Monte Carlo methods to:
- Validate new statistical methods
- Compute power for hypothesis tests
- Approximate complex probability distributions
- Check robustness of assumptions

**Computational efficiency**: Generating 400 × 30 = 12,000 coin tosses takes milliseconds on modern computers. This makes simulation an accessible tool for students to build intuition about sampling distributions.

---

## 7. Summary and Key Findings

### 7.1 Code

```python
print("\n" + "=" * 70)
print("CHAPTER 3 ANALYSIS COMPLETE")
print("=" * 70)
print("\nKey concepts demonstrated:")
print("  - Sampling distribution of the sample mean")
print("  - Central Limit Theorem")
print("  - Properties of estimators (unbiasedness, efficiency)")
print("  - Computer simulation of random samples")
print("  - Comparison of theoretical and empirical distributions")
```

### 7.2 Results

```
======================================================================
CHAPTER 3 ANALYSIS COMPLETE
======================================================================

Key concepts demonstrated:
  - Sampling distribution of the sample mean
  - Central Limit Theorem
  - Properties of estimators (unbiasedness, efficiency)
  - Computer simulation of random samples
  - Comparison of theoretical and empirical distributions
```

### 7.3 Interpretation

**Foundation for inference**: The sample mean is the workhorse estimator in statistics. This chapter establishes three critical properties:

1. **Unbiasedness**: E[x̄] = μ (the estimator targets the true value on average)
2. **Consistency**: As n → ∞, x̄ → μ (larger samples give better estimates)
3. **Asymptotic normality**: For large n, x̄ ~ N(μ, σ²/n) (enables hypothesis testing and confidence intervals)

**Central Limit Theorem**: The most important result in statistics. It states that regardless of the population distribution's shape, the sampling distribution of the mean approaches normality as sample size increases. This is why normal-based inference (t-tests, confidence intervals) works even for non-normal data.

**Standard error vs. standard deviation**: Students often confuse these:
- **Standard deviation (σ)**: Measures variability in the population
- **Standard error (σ/√n)**: Measures variability in the sample mean
- The standard error decreases with sample size; the standard deviation does not

**Practical takeaways**:
- Larger samples provide more precise estimates (standard error ∝ 1/√n)
- Sample means vary around the population mean—we must quantify this uncertainty
- Computer simulation can verify theoretical results and build intuition

---

## Conclusion

This chapter provided a comprehensive exploration of the sample mean—the foundation of statistical inference. We covered:

1. **Setup**: Reproducible random number generation in Python
2. **Single sample**: Observing sampling variability in one coin toss sample
3. **Sampling distribution**: Empirical verification using 400 samples
4. **Real data**: Applying concepts to 1880 U.S. Census age data
5. **Random generation**: Creating samples from uniform and normal distributions
6. **Simulation**: Monte Carlo verification of theoretical predictions

**Key Takeaways for Students**:

- **Code Skills**: Proficiency with numpy random number generation, pandas for data manipulation, matplotlib for distributions, scipy.stats for theoretical distributions
- **Statistical Concepts**: Deep understanding of sampling distributions, Central Limit Theorem, unbiasedness, standard error, and the distinction between population and sample statistics
- **Simulation Thinking**: Using computers to verify theory, build intuition, and explore scenarios where analytical solutions are difficult
- **Theory-Practice Connection**: Consistently comparing empirical results (from samples) with theoretical predictions (from formulas)

**Next Steps**:

- **Chapter 4**: Hypothesis testing using the normal distribution
- **Chapter 5**: Confidence intervals for the population mean
- **Extensions**: Explore other estimators (median, variance), larger sample sizes (n=100, n=1000), non-normal populations (exponential, Poisson)

**Practical Skills Gained**:

Students can now:
- Generate random samples from common distributions (Bernoulli, uniform, normal)
- Understand why sample statistics differ from population parameters
- Interpret standard errors correctly
- Visualize sampling distributions with histograms and theoretical overlays
- Conduct Monte Carlo simulations to verify statistical theory
- Explain the Central Limit Theorem with concrete examples

This chapter bridges the gap between probability theory (what we expect in the long run) and statistical inference (what we conclude from finite samples). The sample mean's beautiful properties—unbiasedness, efficiency, and asymptotic normality—make it the cornerstone of parametric statistics.

---

**References**:

- Data source: Cameron, A.C. (2021). *Analysis of Economics Data: An Introduction to Econometrics*
- Python libraries: numpy, pandas, matplotlib, seaborn, scipy
- Datasets: AED_COINTOSSMEANS.DTA, AED_CENSUSAGEMEANS.DTA

**Data Citations**:

- Coin toss data: Simulated Bernoulli(0.5) samples, n=30, 400 replications
- Census data: 1880 U.S. Census age data, 100 samples of size n=25
- Simulations: Computer-generated random samples using numpy pseudorandom number generator

**Key Formulas**:

- **Population mean**: μ = E[X]
- **Population variance**: σ² = E[(X - μ)²]
- **Sample mean**: x̄ = (1/n) Σxᵢ
- **Standard error**: SE(x̄) = σ/√n
- **Central Limit Theorem**: x̄ ~ N(μ, σ²/n) for large n
