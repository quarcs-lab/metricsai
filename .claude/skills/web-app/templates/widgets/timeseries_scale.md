# Widget: Time series with Level/Log/Growth 3-way toggle

## When to use

- Any chapter that plots a time-ordered economic series.
- Teaching the connection between level, log-level, and growth rate.
- Showing recessions / structural breaks (shading toggle).

## Pedagogical target

Three complementary views of the same data: Level for the growth story, Log for whether growth is steady, Growth for the volatility story. Eliminates the "what happens if both toggles are on?" confusion of a two-toggle design.

## Adapt to your chapter

- Data key: expects `DATA.<series>` with `dates` (ISO strings), `values`, optional `recessions` (array of `[start, end]` date pairs).
- Adjust the period label in growth mode (`QoQ`, `YoY`, etc.) to match the frequency.
- The series frequency affects the y-label for Growth view.

## HTML snippet

```html
<section class="widget" id="ts">
  <div class="widget-head">
    <div>
      <span class="section-tag">§ X.X · Key Concept X.X</span>
      <h2>Time-series line chart — trend, cycles, and shocks</h2>
    </div>
    <button type="button" class="reset-btn" data-reset="ts">↺ Reset</button>
  </div>
  <p class="lede">TODO chapter-specific lede</p>
  <div class="controls">
    <div class="ctrl">
      <label>View</label>
      <div class="toggle-group" id="ts-view">
        <button type="button" data-val="level" class="active">Level</button>
        <button type="button" data-val="log">Log</button>
        <button type="button" data-val="growth">Growth</button>
      </div>
    </div>
    <div class="ctrl">
      <label>Recession shading</label>
      <div class="toggle-group" id="ts-shading">
        <button type="button" data-val="on" class="active">On</button>
        <button type="button" data-val="off">Off</button>
      </div>
    </div>
  </div>
  <div class="chart tall" id="ts-chart"></div>
  <div class="callout"><strong>Level</strong> tells the growth story · <strong>Log</strong> shows whether growth is steady (straight line) · <strong>Growth</strong> tells the volatility story.</div>
  <div class="try-this">
    <div class="try-title">Try this</div>
    <ol><!-- TODO --></ol>
  </div>
</section>
```

## JS snippet

```js
// ==================== WIDGET: TIME SERIES 3-WAY ====================
(function() {
  const viewGroup = document.getElementById("ts-view");
  const shadingGroup = document.getElementById("ts-shading");
  let view = "level", shading = "on";

  // TODO: point at chapter data
  const SERIES = DATA.gdp;         // { dates, values, recessions }
  const PERIOD_LABEL = "Quarter";  // or "Month", "Year"
  const GROWTH_LABEL = "QoQ growth rate (%)"; // or "YoY", etc.
  const LEVEL_LABEL = "Real GDP per capita ($)";
  const LOG_LABEL = "ln(GDP per capita)";

  function render() {
    const c = themeColors();
    const { dates, values, recessions = [] } = SERIES;
    let y, yTitle, color, hoverFmt, name;
    if (view === "level") {
      y = values; yTitle = LEVEL_LABEL; color = c.cyan; name = "Level";
      hoverFmt = "%{x}<br>$%{y:,.0f}<extra></extra>";
    } else if (view === "log") {
      y = values.map(v => Math.log(v)); yTitle = LOG_LABEL; color = c.purple; name = "ln(level)";
      hoverFmt = "%{x}<br>ln = %{y:.3f}<extra></extra>";
    } else {
      y = [null];
      for (let i = 1; i < values.length; i++) {
        y.push(values[i - 1] ? (values[i] / values[i - 1] - 1) * 100 : null);
      }
      yTitle = GROWTH_LABEL; color = c.pink; name = "growth";
      hoverFmt = "%{x}<br>%{y:.2f}%<extra></extra>";
    }

    const traces = [{ type: "scatter", mode: "lines", x: dates, y,
      line: { color, width: 2.2 }, name, hovertemplate: hoverFmt }];

    const shapes = [];
    if (shading === "on") {
      for (const [s0, s1] of recessions) {
        shapes.push({ type: "rect", xref: "x", yref: "paper",
          x0: s0, x1: s1, y0: 0, y1: 1,
          fillcolor: c.pink, opacity: 0.12, line: { width: 0 } });
      }
    }
    if (view === "growth") {
      shapes.push({ type: "line", xref: "paper", yref: "y", x0: 0, x1: 1, y0: 0, y1: 0,
        line: { color: c.grid, width: 1 } });
    }

    const layout = baseLayout({
      height: 400,
      xaxis: Object.assign({}, baseLayout().xaxis, { title: { text: PERIOD_LABEL, font: { color: c.textSoft } } }),
      yaxis: Object.assign({}, baseLayout().yaxis, { title: { text: yTitle, font: { color: c.textSoft } } }),
      shapes
    });
    Plotly.react("ts-chart", traces, layout, PLOTLY_CONFIG);
  }

  viewGroup.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
    viewGroup.querySelectorAll("button").forEach(x => x.classList.remove("active"));
    b.classList.add("active"); view = b.dataset.val; render();
  }));
  shadingGroup.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
    shadingGroup.querySelectorAll("button").forEach(x => x.classList.remove("active"));
    b.classList.add("active"); shading = b.dataset.val; render();
  }));
  window.__rerender_ts = render;
  render();
})();
```

## Registry entry

```js
ts: [
  { group: "ts-view", kind: "toggle", def: "level" },
  { group: "ts-shading", kind: "toggle", def: "on" }
]
```
