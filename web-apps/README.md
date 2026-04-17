# metricsAI Interactive Web Apps

Self-contained HTML dashboards that let students manipulate the key concepts of each chapter with sliders, toggles, and dropdowns. Every app is a single HTML file with data pre-computed and embedded, so it opens with a double-click and works offline once the Plotly CDN is cached.

## Layout

```
web-apps/
├── README.md           ← this file
├── ch01/
│   ├── build.py        ← build script (reads data, injects JSON)
│   ├── template.html   ← HTML/CSS/JS template with {{DATA_JSON}}
│   ├── dashboard.html  ← generated — open in a browser
│   └── PLAN.md         ← design notes for this chapter's app
├── ch02/ …
├── ch03/ …
└── chNN/ …
```

One folder per chapter. Each folder holds the build script, template, rendered `dashboard.html`, and a design plan (`PLAN.md`) so anyone returning later can see what decisions were made and why.

## Opening an app

```bash
open web-apps/ch02/dashboard.html        # macOS
# or just double-click the file in Finder / File Explorer
```

The dashboards require only an internet connection on first load (to fetch the Plotly.js bundle and Google Fonts from their CDNs). After that they run entirely from the single HTML file.

## Regenerating / editing an app

Each chapter's build files live inside its own directory:

- `web-apps/chNN/build.py` — reads the chapter's datasets, computes summary stats, injects a JSON blob into the template.
- `web-apps/chNN/template.html` — HTML + CSS + JavaScript with a `{{DATA_JSON}}` placeholder. This is where you edit widgets, styling, and copy.

Rebuild a chapter's dashboard with:

```bash
source .venv/bin/activate
python3 web-apps/ch02/build.py
```

## Adding a dashboard for a new chapter

1. Create `web-apps/chNN/` with `build.py` and `template.html` (use an existing chapter as reference).
2. Update the dataset loaders in `build.py` for the chapter's data.
3. Adjust widgets in `template.html` for the chapter's concepts.
4. Run the build script and commit the generated `dashboard.html` alongside a `PLAN.md`.

## Supplementary data

Most widgets use the book's own datasets (`data/AED_*.DTA`). The Chapter 2 log-transformation widget additionally uses a 1820→2022 long-run U.S. GDP per capita series from the **Maddison Project Database 2023** (Bolt & van Zanden, *Journal of Economic Surveys*, 2024) to illustrate the hockey-stick-becomes-a-line intuition. The slim extract lives at `data/maddison_us_gdppc.csv` and is refreshed by `python3 scripts/fetch_maddison_us.py` (pulls from Our World in Data's public CSV mirror).

## Design conventions

- **Brand palette:** `#008CB7` (ElectricCyan), `#7A209F` (SynapsePurple), `#C21E72` (DataPink) — matches the book and project website.
- **Fonts:** Inter (body) and JetBrains Mono (numbers, code).
- **Theme:** light mode by default; a toggle persists the user's choice in `localStorage` under the key `metricsai-theme`.
- **Charts:** Plotly.js via CDN. Paper and plot backgrounds are transparent so panels and theme colors show through.
- **Data:** embedded as JSON inside a `<script type="application/json">` island — no network requests for data.
