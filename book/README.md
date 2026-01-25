# Econometrics Powered by AI - LaTeX Book

This directory contains the LaTeX source files for the complete book version of "Econometrics Powered by AI: An Introduction Using Cloud-based Python Notebooks."

## Current Status

**✅ COMPLETE - All 17 chapters compiled successfully**

- **Last Updated**: January 25, 2026
- **Total Pages**: 437 pages
- **File Size**: 16 MB
- **Status**: Production-ready PDF

## Book Structure

The book is organized into four parts:

### Preface
- Introduction to the AI-powered approach
- Three pillars: Foundational Concepts, Computational Notebooks, AI-Powered Learning
- Acknowledgments

### Part I: Statistical Foundations (Chapters 1-4)
- ✅ Chapter 1: Analysis of Economics Data
- ✅ Chapter 2: Univariate Data Summary
- ✅ Chapter 3: The Sample Mean
- ✅ Chapter 4: Statistical Inference for the Mean

### Part II: Bivariate Regression (Chapters 5-9)
- ✅ Chapter 5: Bivariate Data Summary
- ✅ Chapter 6: The Least Squares Estimator
- ✅ Chapter 7: Statistical Inference for Bivariate Regression
- ✅ Chapter 8: Case Studies for Bivariate Regression
- ✅ Chapter 9: Models with Natural Logarithms

### Part III: Multiple Regression (Chapters 10-13)
- ✅ Chapter 10: Data Summary for Multiple Regression
- ✅ Chapter 11: Statistical Inference for Multiple Regression
- ✅ Chapter 12: Further Topics in Multiple Regression
- ✅ Chapter 13: Case Studies for Multiple Regression

### Part IV: Advanced Topics (Chapters 14-17)
- ✅ Chapter 14: Regression with Indicator Variables
- ✅ Chapter 15: Regression with Transformed Variables
- ✅ Chapter 16: Checking the Model and Data
- ✅ Chapter 17: Panel Data, Time Series Data, Causation

## File Organization

```
book/
├── main.tex                    # Main LaTeX document
├── main.pdf                    # Compiled PDF (437 pages, 16 MB)
├── chapters/                   # Chapter source files
│   ├── preface.tex
│   ├── ch01_analysis_of_economics_data.tex
│   ├── ch02_univariate_data_summary.tex
│   ├── ch03_the_sample_mean.tex
│   ├── ch04_statistical_inference_for_the_mean.tex
│   ├── ch05_bivariate_data_summary.tex
│   ├── ch06_the_least_squares_estimator.tex
│   ├── ch07_statistical_inference_for_bivariate_regression.tex
│   ├── ch08_case_studies_for_bivariate_regression.tex
│   ├── ch09_models_with_natural_logarithms.tex
│   ├── ch10_data_summary_for_multiple_regression.tex
│   ├── ch11_statistical_inference_for_multiple_regression.tex
│   ├── ch12_further_topics_in_multiple_regression.tex
│   ├── ch13_case_studies_for_multiple_regression.tex
│   ├── ch14_regression_with_indicator_variables.tex
│   ├── ch15_regression_with_transformed_variables.tex
│   ├── ch16_checking_the_model_and_data.tex
│   └── ch17_panel_data_time_series_data_causation.tex
└── README.md                   # This file
```

## Design Features

### Color Scheme (Print-Optimized)
- **DeepNavy** (#0B1021) - Part titles
- **ElectricCyan** (#008CB7) - Chapter titles, links, key concepts
- **SynapsePurple** (#7A209F) - Section titles
- **DataPink** (#C21E72) - Subsection titles

### Key Concept Boxes
- Enhanced tcolorbox with cyan background
- White title text on cyan header
- Breakable across pages
- Consistent styling throughout

### Typography
- 11pt book class with A4 paper
- 1-inch margins
- Line spread: 1.08 for improved readability
- Latin Modern font family
- Microtype for improved typography

### Special Features
- Cover image (full-page background)
- Colored hyperlinks (purple for internal, cyan for URLs)
- Numbered sections and chapters only
- Table of contents includes chapters and sections only
- Colored bullet points (cyan, purple, pink)
- Professional code listings with syntax highlighting
- Full-width chapter summary images

## Compilation

To compile the book:

```bash
cd /Users/carlos/GitHub/metricsai/book
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex  # Second pass for cross-references
```

The double compilation is necessary to resolve cross-references and generate correct table of contents.

## LaTeX Packages Used

### Core Packages
- `book` - Document class
- `geometry` - Page layout
- `inputenc`, `fontenc`, `lmodern` - Font encoding and modern fonts
- `amsmath`, `amssymb` - Mathematical notation and symbols

### Visual Design
- `xcolor` - Color definitions
- `titlesec` - Custom heading styles
- `soul` - Text highlighting
- `graphicx` - Image inclusion
- `eso-pic` - Background images

### Content
- `listings` - Code blocks with syntax highlighting
- `booktabs`, `longtable` - Professional tables
- `tcolorbox` - Beautiful colored boxes for key concepts
- `framed` - Boxed environments

### Typography & Links
- `microtype` - Typography improvements
- `caption` - Enhanced captions
- `hyperref` - Hyperlinks and PDF bookmarks

## Conversion Notes

All chapters were converted from markdown format following these rules:
- `#` → `\chapter{}`
- `##` → `\section{}`
- `###` → `\subsection{}`
- Blockquotes with "**Key Concept:**" → `\begin{keyconcept}{Title}...\end{keyconcept}`
- Python code → `\begin{lstlisting}[language=Python]...\end{lstlisting}`
- Output text → `\begin{verbatim}...\end{verbatim}`
- Images → `\includegraphics[width=\textwidth]{path}` (chapter summaries full-width)
- Images → `\includegraphics[width=0.8\textwidth]{path}` (inline figures)

### Important Fixes Applied
- Escaped underscores in image paths removed (LaTeX doesn't need them in `\includegraphics`)
- Horizontal rule lines removed (cleaner visual separation)
- Subsections unnumbered via `\setcounter{secnumdepth}{1}`
- Subsections excluded from TOC via `\setcounter{tocdepth}{1}`

## Image References

All images are referenced relative to the chapter files:
- Chapter summary images: `../code_python/images/chXX_visual_summary.jpg`
- Inline figures: `../code_python/images/chXX_figure_name.png`

Make sure images exist at these paths before compilation.

## Known Issues

None currently. All 17 chapters compile successfully without errors.

## Version History

### v1.0 - January 25, 2026
- ✅ All 17 chapters compiled successfully
- ✅ 437 pages total
- ✅ Enhanced key concept boxes with white titles
- ✅ Full-width chapter summary images
- ✅ Proper subsection handling (unnumbered, not in TOC)
- ✅ Fixed image path issues in chapters 12-16
- ✅ Production-ready PDF

## Future Enhancements

Potential improvements for future versions:
- Index generation
- Bibliography/references section
- Appendices with additional resources
- Back cover design
- ISBN and publication metadata

## Credits

- **Content**: Based on A. Colin Cameron's "Analysis of Economics Data: An Introduction to Econometrics" (2022)
- **Python Implementation**: Carlos Mendez
- **LaTeX Compilation**: Automated conversion from markdown with AI assistance
- **Cover Design**: AI-generated book cover (book1cover.jpg)

## License

Please refer to the main project LICENSE file for terms of use.
