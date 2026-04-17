# Chapter 2 Interactive Dashboard — Implementation Plan

## Context

The metricsAI book currently teaches Chapter 2 (Univariate Data Summary) through static matplotlib plots in Quarto notebooks. Students can execute the code in Colab, but they cannot manipulate parameters live to build intuition about how bin width affects a histogram, how skewness shifts the mean away from the median, how a log transform tames right-skew, or how a moving-average window reveals trend inside a noisy time series.

The goal is a single self-contained HTML dashboard — `web-apps/ch02/dashboard.html` — that covers the pedagogical core of Chapter 2 (sections 2.1–2.6) with sliders, toggles, and dropdowns. It will use the same real datasets and examples as the notebook so students can move fluidly between reading the chapter and exploring the concepts. This is the first of eighteen chapter dashboards; the pattern established here will inform the rest, and the deliverable should be ready to link from the project website as a new "Interactive Apps" section.

Design decisions confirmed with the user:

- **Charts:** Plotly.js via CDN.
- **Data:** Pre-computed JSON embedded inline (single self-contained file, works offline, no CORS).
- **Scope:** Sections 2.1–2.6 core concepts only (case studies deferred to a later dashboard).
- **Theming:** Light + dark toggle persisted to `localStorage`, matching book brand palette (#008CB7 / #7A209F / #C21E72) and fonts (Inter + JetBrains Mono).

## Deliverables

1. `scripts/build_ch02_webapp.py` — reads source datasets, computes derived fields, injects a JSON blob into an HTML template, writes final dashboard.
2. `scripts/ch02_webapp_template.html` — HTML + CSS + JS template with a `{{DATA_JSON}}` placeholder.
3. `web-apps/ch02/dashboard.html` — single self-contained file, distributable as-is.
4. `web-apps/ch02/PLAN.md` — this plan, preserved alongside the app for future reference.
5. `web-apps/README.md` — brief note on directory layout and how to add future chapter apps.

## Datasets used (same as notebook)

| Source file | Used for widget | Fields kept |
|---|---|---|
| `data/AED_EARNINGS.DTA` | Summary stats, histogram/KDE, log transform, z-score | `earnings` (n=171) |
| `data/AED_REALGDPPC.DTA` | Time-series line chart with recession shading | `daten`, `realgdppc` (quarterly 1959–2020) |
| `data/AED_HEALTHCATEGORIES.DTA` | Bar/pie toggle | `category`, `expenditures` (13 rows) |
| `data/AED_FISHING.DTA` | Categorical frequency table | `mode` counts (4 categories) |
| `data/AED_MONTHLYHOMESALES.DTA` | Moving-average / seasonal-adjustment explorer | `daten`, `exsales`, `exsales_ma11`, `exsales_sa` |

All five `.DTA` files already exist locally (confirmed in repo), so no network fetches at build time. Recession quarters for the GDP chart (1973-Q4 to 1975-Q1, 1980-Q1 to 1980-Q3, 1981-Q3 to 1982-Q4, 1990-Q3 to 1991-Q1, 2001-Q1 to 2001-Q4, 2007-Q4 to 2009-Q2, 2020-Q1 to 2020-Q2) will be hard-coded in the build script.

## Interactive widgets (mapped to chapter sections)

| § | Widget | Key interaction | Pedagogical point |
|---|---|---|---|
| 2.1 | **Summary-stats explorer** | Dropdown: earnings / GDP / home-sales. Displays mean, median, σ, min, max, Q1, Q3, IQR, skewness, kurtosis. Dot-plot with mean & median markers. | Mean-vs-median gap signals skew; show it numerically and visually. |
| 2.1 | **Outlier toggle** (earnings) | Slider to inject one extra high-earner ($50k–$500k); metrics update live. | The mean is pulled by outliers; the median barely moves. |
| 2.2 | **Histogram bin-width slider** (earnings) | Slider 1k–15k bin width; optional KDE overlay; vertical mean & median lines. | Bin choice shapes the story; KDE removes the arbitrariness. |
| 2.2 | **Box-plot outlier detector** | IQR-multiplier slider 1.0–3.0; flagged outliers listed below the chart. | Outlier definition is a convention, not a fact — the 1.5 rule is a choice. |
| 2.2 | **Time-series trend viewer** (GDP) | Toggle recession shading; date-range brush; toggle growth-rate overlay. | Trend, cycles, and structural breaks are visible to the eye once shading is on. |
| 2.3–2.4 | **Categorical charts** (health / fishing) | Dataset toggle; chart-type toggle (bar ↔ pie); sort toggle (alpha ↔ by value). | Bar charts usually beat pie charts for comparison; sort order changes perception. |
| 2.5 | **Log-transformation visualizer** (earnings) | Side-by-side histograms: raw vs ln(earnings); skewness labeled on each; toggle mean/median markers. | Log turns a 1.71-skew distribution into a near-symmetric one. |
| 2.5 | **Z-score calculator** | Slider over earnings range; shows z = (x − x̄)/s with interpretation and a marker on the standardized-earnings density. | Standardization places any observation on a comparable scale. |
| 2.6 | **Moving-average smoother** (home sales) | Window slider 1–24 months; toggle seasonally-adjusted overlay; recession shading. | Smoothing reveals the 2007–2011 housing bust hiding inside the seasonal noise. |

Each widget sits in its own glass-panel card. Cards are stacked vertically under a sticky section navigation bar.

## File-by-file design

### `scripts/build_ch02_webapp.py`

```
1. Load the five .DTA files with pandas.read_stata().
2. Build a DATA dict:
     {
       "earnings": [...],
       "gdp": {"dates": [...], "values": [...], "recessions": [[start,end], ...]},
       "health": {"categories": [...], "values": [...]},
       "fishing": {"modes": [...], "counts": [...]},
       "home_sales": {"dates": [...], "original": [...], "ma11": [...], "sa": [...]},
       "summary": {"earnings": {mean, median, std, ...}, ...}  # pre-computed
     }
3. Convert timestamps to ISO date strings (so Plotly parses cleanly).
4. Read scripts/ch02_webapp_template.html.
5. Replace a {{DATA_JSON}} placeholder with json.dumps(DATA).
6. Write web-apps/ch02/dashboard.html.
```

Dependencies already in `requirements.txt`: `pandas`, `numpy`. No new packages.

### `scripts/ch02_webapp_template.html` (new file; source for the generator)

Single HTML document. Structure:

```
<head>
  Google Fonts (Inter, JetBrains Mono)
  Plotly 2.35 CDN
  <style> … brand tokens, light/dark vars, glass panels, responsive grid … </style>
</head>
<body>
  <header> title, subtitle, theme toggle, chapter-2-of-18 badge </header>
  <nav> sticky anchor links to the eight widget sections </nav>
  <main>
    <section id="stats">   summary-stats explorer + outlier toggle </section>
    <section id="hist">    histogram bin slider + KDE toggle         </section>
    <section id="box">     boxplot + IQR-multiplier slider           </section>
    <section id="ts">      GDP time series + recession toggle        </section>
    <section id="cat">     bar/pie toggle for categorical data       </section>
    <section id="log">     log-transform side-by-side                </section>
    <section id="z">       z-score calculator                        </section>
    <section id="ma">      moving-average smoother                   </section>
  </main>
  <footer> link back to the book, Colab, GitHub </footer>

  <script type="application/json" id="ch02-data">{{DATA_JSON}}</script>
  <script>
    const DATA = JSON.parse(document.getElementById('ch02-data').textContent);
    // theme toggle (localStorage key "metricsai-theme")
    // one initWidget* function per section
    // small stats helpers: mean, median, quantile, std, skewness, kurtosis,
    //   kdeGaussian(values, bandwidth), movingAverage(values, window)
    // all Plotly calls share a common layout builder that reads CSS vars
    //   so charts re-theme on dark-mode toggle (Plotly.relayout on toggle)
  </script>
</body>
```

Statistics are computed in JavaScript from the raw arrays so sliders (e.g., outlier injection) recompute live. No external math library — ~40 lines of stats helpers.

### `web-apps/README.md`

Three short paragraphs: what the directory is, how to regenerate `web-apps/ch02/dashboard.html` (`python3 scripts/build_ch02_webapp.py`), and the pattern for adding chapter dashboards — one `web-apps/chNN/` folder per chapter, each with its own `dashboard.html` and `PLAN.md`, built by `scripts/build_chNN_webapp.py` + `scripts/chNN_webapp_template.html`.

## Visual design

- **Palette:** `--cyan: #008CB7`, `--purple: #7A209F`, `--pink: #C21E72`. Cyan = primary actions and data; purple = section headers and chart secondary series; pink = highlights (mean-vs-median gap, outlier markers).
- **Light mode:** near-white page (`#f7f9fc`), white glass panels, navy text (`#0B1021`).
- **Dark mode:** navy background (`#12162c`), slate panels (`#1b2040`), near-white text — matching the book's dark theme.
- **Typography:** Inter 400/600 for prose, JetBrains Mono 500 for numbers in the stats readouts.
- **Layout:** single-column on mobile, two-column on desktop for widget + interpretation. Sticky top nav.
- **Accessibility:** keyboard-operable sliders, visible focus rings, WCAG-AA contrast in both themes.

## Verification

1. **Build runs clean:** `python3 scripts/build_ch02_webapp.py` emits `web-apps/ch02/dashboard.html` without errors and with file size under ~1 MB. (Actual: 66 KB.)
2. **Opens offline:** double-click the HTML in Finder (no local server) and all eight widgets render. Disconnect Wi-Fi and confirm charts still draw (only the Plotly CDN and Google Fonts need first-load cache — document this in README).
3. **Each widget works end-to-end:**
   - Summary-stats dropdown changes all ten metrics and the dot-plot markers.
   - Outlier slider moves the mean but not the median on earnings.
   - Bin-width slider at 1k shows spikes; at 15k shows one blob; KDE overlay is smooth.
   - IQR-multiplier at 1.5 flags the expected high earners; at 3.0 flags fewer.
   - GDP recession toggle shades 1973, 1980, 1981, 1990, 2001, 2008, 2020.
   - Bar↔pie toggle swaps the health/fishing chart type.
   - Log-transform shows raw skewness ≈ 1.71 and log skewness ≈ −0.91 (numbers from chapter).
   - Z-score slider at $36,000 (median earnings) yields z ≈ −0.21.
   - Moving-average window at 11 on home sales matches the `exsales_ma11` reference trace.
4. **Theme toggle:** click the moon/sun button, both charts and panels re-theme; reload the page — the choice persists.
5. **Numbers match the book:** spot-check summary stats against the values quoted in `notebooks_colab/ch02_Univariate_Data_Summary.md` (mean $41,412.69, median $36,000, skewness 1.71, etc.).
6. **Responsive:** resize to 375 px width in browser dev tools; widgets stack, controls stay reachable.

## Out of scope (for this task)

- Case-study dashboards (convergence clubs, Bolivia municipalities) — flagged as good follow-ups.
- Auto-linking the dashboard from `index.html` — add in a follow-up so website changes aren't bundled with the app build.
- Dashboards for chapters 1, 3–17 — same template pattern, one chapter at a time.

## Critical files

- **New:** `scripts/build_ch02_webapp.py`
- **New:** `scripts/ch02_webapp_template.html`
- **New (generated):** `web-apps/ch02/dashboard.html`
- **New:** `web-apps/ch02/PLAN.md` (copy of this plan)
- **New:** `web-apps/README.md`
- **Read-only references:** `notebooks_colab/ch02_Univariate_Data_Summary.md`, `notebooks_quarto/ch02_Univariate_Data_Summary.qmd`, `book/custom.css`, `index.html`, `data/AED_*.DTA`
