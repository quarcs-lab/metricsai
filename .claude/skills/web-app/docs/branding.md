# Branding

Matches the metricsAI book and website. Do not introduce new colors or fonts.

## Palette

| Token | Hex | Purpose |
|---|---|---|
| `--cyan` / ElectricCyan | `#008CB7` | Primary interactive elements; main data series; active states |
| `--purple` / SynapsePurple | `#7A209F` | Section H2, secondary data series, structural emphasis |
| `--pink` / DataPink | `#C21E72` | Highlights: mean–median gap, outlier markers, recession shading, fitted lines |

Dark-mode soft variants (`--cyan-soft #22d3ee`, `--purple-soft #c084fc`, `--pink-soft #f472b6`) are used automatically via CSS custom properties; widget code never references them directly — it goes through `themeColors()`.

## Fonts

- Body and UI: **Inter** (weights 300, 400, 500, 600, 700) from Google Fonts.
- Monospace, numbers, code, axis ticks, stats readouts: **JetBrains Mono** (400, 500, 600).

These match the book's Quarto theme and the project website's `index.html`.

## Layout

- Max content width: **1120 px**. Centered.
- Card radius: 16 px outer, 10 px inner (controls, stats).
- Shadow: a single tier defined by `--shadow`.
- Section spacing: 1.5 rem between widgets. 1 rem between elements inside a widget.
- Responsive: 1 column ≤ 720 px; 2 columns for `.two-col` above.

## Typography

- `h1.title` uses a cyan→purple gradient. Use once, in the header.
- `h2` inside widgets is purple. Keep widget titles to one short line.
- `.lede` is one 1–2 sentence paragraph under the title explaining *why* the widget exists.
- Numeric readouts use JetBrains Mono and the cyan accent for the active metric.

## Accessibility

- All interactive controls (range, select, button) are keyboard operable — use the native elements, not styled divs.
- Focus ring is inherited from the browser defaults; do not suppress it.
- WCAG AA contrast in both light and dark modes — spot-check if you change colors.
- Sliders have accompanying `.val` readouts so the current value is always visible.

## Chart styling

- Always go through `baseLayout()`. Don't build a layout from scratch.
- `paper_bgcolor` and `plot_bgcolor` are transparent so the card's background and theme show through.
- Axis line, grid, and zero-line colors all come from `--grid` (the theme variable).
- No chart titles for single-chart widgets (the `<h2>` and `.lede` already label them). For side-by-side comparisons (e.g. raw vs. log), small colored `title:` is fine.
- Hide the mode bar (`displayModeBar: false` is default in `PLOTLY_CONFIG`). Export via OS-level screenshot if needed.
- Hover labels are panel-colored with the theme's border + text colors — already set in `baseLayout()`.

## Attribution

The chapter's footer includes:

- Link back to the book
- Chapter number and title
- Author
- GitHub link
- `{{ATTRIBUTION}}` — filled in if any supplementary (non-book) data is used. Minimum: dataset name + citation + link. Example:

  ```
  <p style="font-size:0.8rem;margin-top:0.4rem">Long-run GDP data: Bolt, J. & van Zanden, J. L. (2024), "Maddison style estimates of the evolution of the world economy: A new 2023 update," <em>Journal of Economic Surveys</em>. <a href="...">Maddison Project Database 2023</a>.</p>
  ```

If no supplementary data is used, replace `{{ATTRIBUTION}}` with empty string.
