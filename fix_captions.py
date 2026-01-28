#!/usr/bin/env python3
"""
Fix redundant 'Table X.Y:' and 'Figure X.Y:' prefixes in LaTeX caption commands.
This script processes chapters 2-16 and removes the pattern "(Table|Figure) \d+\.\d+: "
from all \caption{} commands.
"""

import re
import os

# Define the chapters to process
chapters = [
    'ch02_univariate_data_summary.tex',
    'ch03_the_sample_mean.tex',
    'ch04_statistical_inference_for_the_mean.tex',
    'ch05_bivariate_data_summary.tex',
    'ch06_the_least_squares_estimator.tex',
    'ch07_statistical_inference_for_bivariate_regression.tex',
    'ch08_case_studies_for_bivariate_regression.tex',
    'ch09_models_with_natural_logarithms.tex',
    'ch10_data_summary_for_multiple_regression.tex',
    'ch11_statistical_inference_for_multiple_regression.tex',
    'ch12_further_topics_in_multiple_regression.tex',
    'ch13_case_studies_for_multiple_regression.tex',
    'ch14_regression_with_indicator_variables.tex',
    'ch16_checking_the_model_and_data.tex'
]

base_path = '/Users/carlosmendez/Documents/GitHub/metricsai/book/chapters'

# Pattern to match: \caption{Table X.Y: or \caption{Figure X.Y:
pattern = r'\\caption\{(Table|Figure) \d+\.\d+: '

def fix_captions_in_file(filepath):
    """Fix captions in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count matches before fixing
    matches = re.findall(pattern, content)
    count = len(matches)

    # Replace the pattern
    fixed_content = re.sub(pattern, r'\\caption{', content)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    return count

# Process all chapters
total_fixed = 0
results = []

for chapter in chapters:
    filepath = os.path.join(base_path, chapter)
    if os.path.exists(filepath):
        count = fix_captions_in_file(filepath)
        total_fixed += count
        results.append(f"{chapter}: {count} captions fixed")
        print(f"✓ {chapter}: {count} captions fixed")
    else:
        results.append(f"{chapter}: FILE NOT FOUND")
        print(f"✗ {chapter}: FILE NOT FOUND")

print(f"\n{'='*60}")
print(f"Total captions fixed: {total_fixed}")
print(f"{'='*60}")

# Write summary report
with open('/Users/carlosmendez/Documents/GitHub/metricsai/caption_fix_report.txt', 'w') as f:
    f.write("Caption Fix Report\n")
    f.write("="*60 + "\n\n")
    for result in results:
        f.write(result + "\n")
    f.write(f"\nTotal captions fixed: {total_fixed}\n")

print("\nReport saved to: caption_fix_report.txt")
