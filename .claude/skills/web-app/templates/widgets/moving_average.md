# Widget: Moving-average smoother

## When to use

- Any chapter dealing with time series that exhibit seasonality or high-frequency noise.
- Teaching the smoothing / responsiveness trade-off.
- Demonstrating seasonal adjustment vs. moving average.

## Pedagogical target

A wider window removes more noise but smears turning points. There's an optimal window given the frequency you want to cancel.

## Adapt to your chapter

- Point at a time series with `dates`, `original`, and optionally `sa` (seasonally adjusted).
- Tune the window slider max to cover at least two full seasonal cycles.
- For monthly data use 1–24 months; for quarterly use 1–16 quarters.

## HTML snippet

```html
<section class="widget" id="ma">
  <div class="widget-head">
    <div>
      <span class="section-tag">§ X.X · Key Concept X.X</span>
      <h2>Moving averages &amp; seasonal adjustment</h2>
    </div>
    <button type="button" class="reset-btn" data-reset="ma">↺ Reset</button>
  </div>
  <p class="lede">TODO chapter-specific lede.</p>
  <div class="controls">
    <div class="ctrl">
      <label for="ma-window">MA window <span class="val" id="ma-window-val">11</span></label>
      <input type="range" id="ma-window" min="1" max="24" step="1" value="11">
    </div>
    <div class="ctrl">
      <label>Seasonally adjusted</label>
      <div class="toggle-group" id="ma-sa">
        <button type="button" data-val="off" class="active">Off</button>
        <button type="button" data-val="on">On</button>
      </div>
    </div>
    <div class="ctrl">
      <label>Recession shading</label>
      <div class="toggle-group" id="ma-recession">
        <button type="button" data-val="on" class="active">On</button>
        <button type="button" data-val="off">Off</button>
      </div>
    </div>
  </div>
  <div class="chart tall" id="ma-chart"></div>
  <div class="callout" id="ma-callout"></div>
  <div class="try-this">
    <div class="try-title">Try this</div>
    <ol><!-- TODO --></ol>
  </div>
</section>
```

## JS snippet

```js
// ==================== WIDGET: MOVING AVERAGE ====================
(function() {
  const winSlider = document.getElementById("ma-window");
  const winVal = document.getElementById("ma-window-val");
  const saGroup = document.getElementById("ma-sa");
  const recGroup = document.getElementById("ma-recession");
  const callout = document.getElementById("ma-callout");
  let saMode = "off", recMode = "on";

  // TODO: point at chapter series
  const SERIES = DATA.home_sales;  // { dates, original, sa? }
  const RECESSIONS = [["2007-12-01","2009-06-01"]]; // or empty

  function render() {
    const c = themeColors();
    const { dates, original, sa } = SERIES;
    const w = parseInt(winSlider.value, 10);
    winVal.textContent = w + (w === 1 ? " period (no smoothing)" : " periods");
    const smoothed = movingAverage(original, w);

    const traces = [{
      type: "scatter", mode: "lines", x: dates, y: original,
      line: { color: c.cyan, width: 1.1 }, opacity: 0.45,
      name: "Original", hovertemplate: "%{x}<br>%{y:,.0f}<extra></extra>"
    }];
    if (w > 1) {
      traces.push({
        type: "scatter", mode: "lines", x: dates, y: smoothed,
        line: { color: c.purple, width: 2.6 },
        name: w + "-period MA",
        hovertemplate: "%{x}<br>%{y:,.0f}<extra></extra>"
      });
    }
    if (saMode === "on" && sa) {
      traces.push({
        type: "scatter", mode: "lines", x: dates, y: sa,
        line: { color: c.pink, width: 1.8, dash: "dot" },
        name: "Seasonally adjusted"
      });
    }

    const shapes = [];
    if (recMode === "on") {
      for (const [s0, s1] of RECESSIONS) {
        shapes.push({ type: "rect", xref: "x", yref: "paper", x0: s0, x1: s1, y0: 0, y1: 1,
          fillcolor: c.pink, opacity: 0.11, line: { width: 0 } });
      }
    }

    const layout = baseLayout({
      height: 420,
      xaxis: Object.assign({}, baseLayout().xaxis, { title: { text: "Period", font: { color: c.textSoft } } }),
      yaxis: Object.assign({}, baseLayout().yaxis, { title: { text: "Value", font: { color: c.textSoft } } }),
      legend: { x: 0.01, y: 0.99, font: { color: c.text }, bgcolor: "rgba(0,0,0,0)" },
      shapes
    });
    Plotly.react("ma-chart", traces, layout, PLOTLY_CONFIG);
    callout.innerHTML = `<strong>Trade-off:</strong> wider window kills noise faster but smears turning points.`;
  }

  winSlider.addEventListener("input", render);
  [saGroup, recGroup].forEach(grp => {
    grp.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
      grp.querySelectorAll("button").forEach(x => x.classList.remove("active"));
      b.classList.add("active");
      if (grp === saGroup) saMode = b.dataset.val;
      else recMode = b.dataset.val;
      render();
    }));
  });
  window.__rerender_ma = render;
  render();
})();
```

## Registry entry

```js
ma: [
  { id: "ma-window", kind: "range", def: "11" },
  { group: "ma-sa", kind: "toggle", def: "off" },
  { group: "ma-recession", kind: "toggle", def: "on" }
]
```
