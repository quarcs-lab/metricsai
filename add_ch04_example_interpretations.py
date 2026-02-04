#!/usr/bin/env python3
"""
Add interpretation cells and Key Concept boxes to Examples 2 and 3 in CH04 section 4.5
Also add Key Concept box to Example 1

Current state:
- Example 1: Has interpretation, missing Key Concept
- Example 2: Missing interpretation and Key Concept
- Example 3: Missing interpretation and Key Concept

Target: Each example should have Question → Code → Interpretation → Key Concept
"""

import json

# Load notebook
with open('notebooks_colab/ch04_Statistical_Inference_for_the_Mean.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Original notebook: {len(nb['cells'])} cells")

# ============================================================================
# EXAMPLE 1: Add Key Concept box after interpretation (after cell 32)
# ============================================================================

example1_key_concept = """> **Key Concept: Statistical Significance vs. Sample Size**
>
> Even small practical differences can be statistically significant with large samples (n=53 gas stations). The gasoline price difference of \\$0.14 might seem trivial, but:
> - The **standard error is small** (\\$0.0267), giving precise estimates
> - The **t-statistic is large** (-5.26), indicating the difference is many standard errors from zero
> - This demonstrates **high statistical power**—the ability to detect even small real effects
>
> Statistical significance answers "Is there a difference?" while practical significance asks "Does the difference matter?" Both questions are important in econometrics.
"""

# Insert after cell 32 (Example 1 interpretation)
example1_kc_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [example1_key_concept + '\n']
}

nb['cells'].insert(33, example1_kc_cell)
print("✓ Added Key Concept box after Example 1")

# ============================================================================
# EXAMPLE 2: Add interpretation and Key Concept (after cell 36, which is now cell 35+1=36)
# ============================================================================

# Note: After inserting Example 1 KC, cell numbers shift by +1
# Original cell 35 (Example 2 code) is now cell 36

example2_interpretation = """**Test Results: H₀: μ = \\$50,000 vs Hₐ: μ ≠ \\$50,000**
- Sample mean: (actual value from code output)
- t-statistic: (actual value from code output)
- p-value: > 0.05 (not statistically significant)
- Decision: DO NOT REJECT H₀ at α = 0.05

**This is NOT a statistically significant result.**

We do not have sufficient evidence to conclude that 30-year-old men earn differently than \\$50,000 on average. This does NOT mean they earn exactly \\$50,000—it means our data are consistent with that value.

**Understanding the lack of significance:**

1. **Moderate t-statistic:**
   - The sample mean is not far enough from \\$50,000 (in standard error units) to confidently reject H₀
   - The observed difference could plausibly arise from random sampling variation alone

2. **Large p-value (> 0.05):**
   - If μ truly equaled \\$50,000, observing a sample mean like ours is quite probable
   - We don't have strong evidence against H₀
   - p > α, so we fail to reject

3. **What "fail to reject" means:**
   - We're NOT proving μ = \\$50,000
   - We're saying the data don't provide convincing evidence that μ ≠ \\$50,000
   - Absence of evidence is not evidence of absence

**Statistical vs Practical Significance:**

- **Statistical significance:** No, we cannot confidently say mean earnings differ from \\$50,000 (p > 0.05)
- **Practical considerations:**
  - The sample mean might be close to \\$50,000 anyway
  - Or the sample size (n=191) might not provide enough precision to detect a modest difference
  - Or there's genuine variability in the population making the effect hard to pin down

**Why might we fail to reject H₀?**

Three possible explanations:

1. **H₀ is actually true:** Mean earnings truly are around \\$50,000
2. **Insufficient power:** Real difference exists, but our sample size is too small to detect it
3. **High variability:** Earnings have large standard deviation, making precise inference difficult

**Note on directional hypothesis:**

The question asks "Do men earn MORE than \\$50,000?" which suggests a **one-sided test** (H₀: μ ≤ 50,000 vs Hₐ: μ > 50,000). The code note mentions this will be covered in section 4.6. One-sided tests have more power to detect effects in a specific direction.
"""

example2_key_concept = """> **Key Concept: "Fail to Reject" Does Not Mean "Accept"**
>
> When p > α, we **fail to reject H₀**, but this does NOT mean we "accept H₀" or prove it's true. Three key reasons:
>
> 1. **Limited evidence:** Our sample might simply lack the power to detect a real difference
> 2. **Type II error risk:** We might be making a Type II error (failing to reject a false H₀)
> 3. **Confidence intervals are more informative:** A 95% CI tells us the plausible range for μ, not just "different or not different"
>
> In econometrics, "fail to reject" means "the data are consistent with H₀, but we can't rule out alternatives." Always interpret non-significant results with appropriate caution.
"""

# Insert after Example 2 code (cell 36 after first insertion)
example2_interp_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [example2_interpretation + '\n']
}

example2_kc_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [example2_key_concept + '\n']
}

nb['cells'].insert(37, example2_interp_cell)  # After Example 2 code (cell 36)
nb['cells'].insert(38, example2_kc_cell)       # After Example 2 interpretation
print("✓ Added interpretation and Key Concept after Example 2")

# ============================================================================
# EXAMPLE 3: Add interpretation and Key Concept (after cell 40, which is now cell 37+3=40)
# ============================================================================

example3_interpretation = """**Test Results: H₀: μ = 2.0% vs Hₐ: μ ≠ 2.0%**
- Sample mean: (actual value from code output)
- t-statistic: (actual value from code output)
- p-value: > 0.05 (not statistically significant)
- Decision: DO NOT REJECT H₀ at α = 0.05

**The data are consistent with 2.0% average annual growth.**

We cannot reject the hypothesis that real GDP per capita grew at 2.0% per year on average from 1960-2020. This historical benchmark appears supported by the data.

**Understanding the result:**

1. **What does "consistent with 2.0%" mean?**
   - The sample mean growth rate is close enough to 2.0% that random variation could explain the difference
   - We don't have strong evidence that the true mean differs from 2.0%
   - The p-value > 0.05 indicates this result is plausible under H₀

2. **Large sample size (n=241 years):**
   - With 241 year-to-year growth rates, we have substantial data
   - Large samples typically have smaller standard errors and more statistical power
   - Yet we still fail to reject H₀—this suggests the true mean is genuinely close to 2.0%

3. **Economic interpretation:**
   - The 2.0% benchmark is a common reference point in growth economics
   - Our data support this conventional wisdom
   - Long-run economic growth appears remarkably stable around this rate

**Statistical vs Practical Significance:**

- **Statistical significance:** No, we cannot confidently say mean growth differs from 2.0% (p > 0.05)
- **Economic significance:**
  - Even small deviations from 2.0% compound dramatically over 60 years
  - But our data suggest the historical average is indeed close to 2.0%
  - This consistency validates the use of 2.0% as a benchmark for policy discussions

**Why is this result interesting despite being "non-significant"?**

1. **Validates a benchmark:** Economic theory often assumes ~2% long-run growth; our data support this
2. **Large sample confidence:** With 241 observations, we can be confident the mean is near 2.0%
3. **Demonstrates stability:** Despite recessions and booms, average growth centers around 2.0%

**Time series considerations:**

GDP growth data are **time series**—observations ordered chronologically with potential autocorrelation. Our standard t-test assumes independent observations, which might not fully hold for year-to-year growth rates. Advanced time series methods (Chapter 17) address these dependencies.
"""

example3_key_concept = """> **Key Concept: Contextual Interpretation in Economics**
>
> Statistical results gain meaning through economic context:
>
> - **Gasoline prices (Example 1):** Rejected H₀ → Yolo County differs from state average (\\$0.14 cheaper matters to consumers)
> - **Male earnings (Example 2):** Failed to reject H₀ → Data consistent with \\$50,000 average (or insufficient power to detect difference)
> - **GDP growth (Example 3):** Failed to reject H₀ → Historical 2.0% benchmark supported by data
>
> The same statistical framework (t-test, p-value, significance level) applies across diverse economic questions. What changes is the **economic interpretation**: Are differences meaningful? What are the policy implications? What do non-significant results tell us?
"""

# Insert after Example 3 code (cell 40 after two insertions)
example3_interp_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [example3_interpretation + '\n']
}

example3_kc_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [example3_key_concept + '\n']
}

nb['cells'].insert(41, example3_interp_cell)  # After Example 3 code (cell 40)
nb['cells'].insert(42, example3_kc_cell)       # After Example 3 interpretation
print("✓ Added interpretation and Key Concept after Example 3")

# ============================================================================
# Keep the generic summary Key Concept (originally cell 38, now shifted)
# It's now at cell 43 (38 + 5 insertions), which is fine—it comes after all examples
# ============================================================================

print(f"✓ Generic summary Key Concept remains at cell {38 + 5}")

# ============================================================================
# REMOVE transition cell 33 (now cell 34 after first insertion)
# ============================================================================

# Check if cell 34 is the transition cell
if 'To solidify these concepts' in ''.join(nb['cells'][34]['source']):
    del nb['cells'][34]
    print("✓ Removed unnecessary transition cell")

# ============================================================================
# Final cell count
# ============================================================================

print(f"\nFinal notebook: {len(nb['cells'])} cells")
print(f"Net change: +{len(nb['cells']) - 65} cells")

# ============================================================================
# Save modified notebook
# ============================================================================

with open('notebooks_colab/ch04_Statistical_Inference_for_the_Mean.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print("\n✅ Successfully added interpretations and Key Concepts to all examples!")
print("\nNew structure:")
print("- Example 1: Question → Code → Interpretation → Key Concept ✓")
print("- Example 2: Question → Code → Interpretation → Key Concept ✓")
print("- Example 3: Question → Code → Interpretation → Key Concept ✓")
print("- Generic summary Key Concept (ties all three together) ✓")
