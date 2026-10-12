# Images

This directory contains image assets for the metricsAI project.

## Current Files

- **cover.jpg** - Cover image for the project, displayed on the main README and website
- **visual_summaries.json** - Authoritative selection of corrected chapter summaries: Chapter 1 v4, Chapters 2–3 v3, Chapters 4–17 v2 (PNG).
- **ch00_visual_summary.jpg** - Unchanged preface summary.
- **chNN_visual_summary.jpg** - Original summaries, retained for historical comparison.

The corrected PNGs use rectangular illustrated mind maps. Mathematical review notes and generation prompts are in `../errata/`. Run `python3 scripts/sync_visual_summaries.py` from the project root to check that website, book and notebooks use the current selection; use `--write` to synchronize image filenames while preserving all other content.

## Generated Figures

When running the Jupyter notebooks, visualizations and plots are generated dynamically within the notebooks themselves. No image files need to be stored locally as all figures are created inline using matplotlib and seaborn.

## Usage

The cover image is referenced in:

- Main README.md: `![](images/cover.jpg)`
- Project documentation
- Website homepage

Chapter summaries are pre-generated images. Other data visualizations (scatter plots, histograms, regression plots, etc.) are created on-the-fly in the interactive notebooks.
