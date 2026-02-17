# More Resources Section Redesign

**Date:** 2026-02-18
**Status:** Complete

## Summary

Redesigned the "More Resources" section of `index.html` from a static 2x2 grid of topic cards into a **data-driven, filterable card system**. Each resource is now its own card, categories are browsable via filter pills, and adding/removing resources requires editing only a JavaScript array.

## What Changed

### Before
- 4 hand-coded HTML topic cards in a 2x2 grid
- 13 resources as bullet-point links grouped under topic headings
- Adding a resource meant editing nested HTML

### After
- **Data-driven rendering:** Resources stored in a JS `RESOURCES` array, rendered dynamically
- **Filter pills:** 5 category filters (All, Python, Google Colab, Python in Economics, AI for Economics) with live counts
- **Individual cards:** Each resource gets its own card with type badge, category icon, title, description, and action link
- **5 resource types:** Video (red), Article (blue), Interactive (green), Website (slate), Course (purple)
- **3-column responsive grid:** lg:3 / md:2 / sm:1
- **Show More button:** Appears when >9 resources match a filter
- **Smooth transitions:** Staggered fade-in animation on filter change (50ms per card)
- **Video integration:** Video cards call the existing `openVideoModal()` function

### Resource Inventory (17 total)

| # | Title | Category | Type |
|---|-------|----------|------|
| 1 | Python Tutorial for Beginners | Python | Video |
| 2 | Python Programming for Economics and Finance | Python | Course |
| 3 | Google Colab Tutorial for Beginners | Colab | Video |
| 4 | Google Colab - Notebooks and Data Analysis | Colab | Video |
| 5 | Google Colab Beginner's Guide | Colab | Article |
| 6 | QuantEcon | Economics | Website |
| 7 | A First Course in Quantitative Economics | Economics | Course |
| 8 | Intermediate Quantitative Economics with Python | Economics | Course |
| 9 | Quantitative Economics with JAX | Economics | Course |
| 10 | Quantitative Economics with Julia | Economics | Course |
| 11 | URFIE - Introductory Econometrics | Economics | Website |
| 12 | DS4DS - Data Science for Development | Economics | Website |
| 13 | DS4Bolivia | Economics | Website |
| 14 | Generative AI for Economic Research | AI | Website |
| 15 | Economics Teaching & Learning with AI | AI | Article |
| 16 | AI for Economists | AI | Website |
| 17 | Teaching Effectively with ChatGPT | AI | Website |

**Filter counts:** All (17), Python (2), Google Colab (3), Python in Economics (8), AI for Economics (4)

### New resources added this session
- Python Programming for Economics and Finance (python-programming.quantecon.org)
- A First Course in Quantitative Economics (intro.quantecon.org)
- Intermediate Quantitative Economics with Python (python.quantecon.org)
- Quantitative Economics with JAX (jax.quantecon.org)
- Quantitative Economics with Julia (julia.quantecon.org)

### Resources removed this session
- LearnPython.org (replaced by QuantEcon Python course)

## How to Add a Resource

Append one object to the `RESOURCES` array in `index.html`:

```javascript
{ title: 'Resource Name',
  description: 'Brief description.',
  category: 'python',   // python | colab | econ | ai
  type: 'video',        // video | article | interactive | website | course
  videoId: null,         // YouTube ID or null
  url: 'https://...' },
```

## Files Modified
- `index.html` — CSS transitions, section HTML, JS data + rendering logic (net +163 lines)
