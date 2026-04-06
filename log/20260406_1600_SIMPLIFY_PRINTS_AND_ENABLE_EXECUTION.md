# 2026-04-06: Simplify print() Calls and Enable Notebook Execution

## Summary

Simplified verbose `print()` calls across all 18 chapters and enabled code execution in the Quarto book so results appear in the published HTML.

## Print Simplification

Removed ~1,800 unnecessary `print()` calls across ch01–ch17:

- **Decorative banners removed**: All `print("=" * 70)` and `print("TITLE")` header patterns (~430 instances) replaced with `# comment`
- **Expressions unwrapped**: `print(df.describe())` → `df.describe()`, `print(model.summary())` → `model.summary()` (~200 instances)
- **Formatted output kept**: `print(f"Slope: {slope:.4f}")` retained where it provides computed values
- **Setup messages kept**: `print("✓ Setup complete!")` retained for student feedback

Before/after print counts:
- Before: ~3,400 total print() calls
- After: ~1,500 (kept: f-strings with values, loop outputs, status messages)

## Execution Setup

### Environment
- Created fresh `.venv` with Python 3.12 via `uv venv --python 3.12`
- Installed all dependencies from `requirements.txt` + `linearmodels`
- Registered kernel as `python3` for Jupyter/Quarto

### Configuration Changes
- Updated YAML front matter in all 18 `.qmd` files: `execute: enabled: true, warning: false`
- Added `execute: freeze: auto` to `book/_quarto.yml` for cached execution
- Added `#| eval: false` to case study code blocks that reference unavailable datasets

### Data Issues Found (pre-existing)
- `AED_ConvergenceClubs.dta` does not exist in the data repo (used in ch07, ch09 case studies)
- `A00`, `A10`, etc. satellite embedding columns not in DS4Bolivia dataset (used in ch10, ch12, ch16 case studies)
- **Resolution**: Case study exercise blocks marked `#| eval: false` — main chapter content executes fully

## Verification

- All 18 chapters render with code execution in `quarto render`
- Full book builds successfully: `book/_book/index.html`
- All 18 `.ipynb` files regenerated via `export_qmd_to_ipynb.py --all`

## Files Changed

- `notebooks_quarto/ch01–ch17*.qmd` — simplified prints + enabled execution
- `book/_quarto.yml` — added `execute: freeze: auto`
- `notebooks_colab/ch00–ch17*.ipynb` — regenerated from .qmd

## Next Steps

- Fix case study data URLs (AED_ConvergenceClubs.dta, satellite embeddings)
- Review executed output quality in the published book
