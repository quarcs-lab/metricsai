# Widget: Z-score calculator

## When to use

- Any chapter that introduces standardization or the empirical rule (68-95-99.7).
- Teaching how to compare observations across different scales.

## Pedagogical target

Standardization expresses every observation as a distance from the mean, measured in standard deviations.

## HTML snippet

```html
<section class="widget" id="z">
  <div class="widget-head">
    <div>
      <span class="section-tag">§ X.X · Key Concept X.X</span>
      <h2>Z-scores — how unusual is this observation?</h2>
    </div>
    <button type="button" class="reset-btn" data-reset="z">↺ Reset</button>
  </div>
  <p class="lede">Standardization: <code>z = (x − mean) / sd</code>. Roughly 68% within ±1, 95% within ±2, 99.7% within ±3.</p>
  <div class="controls">
    <div class="ctrl" style="min-width:260px">
      <label for="z-val">Observation value <span class="val" id="z-val-display"></span></label>
      <input type="range" id="z-val" min="0" max="1" step="0.001" value="0.5">
    </div>
    <div class="ctrl">
      <label>Z-score</label>
      <div class="mono" id="z-score-display" style="font-size:1.4rem;color:var(--accent);font-weight:500"></div>
    </div>
    <div class="ctrl">
      <label>Interpretation</label>
      <div id="z-interp" style="font-size:.92rem;color:var(--text-soft)"></div>
    </div>
  </div>
  <div class="chart short" id="z-chart"></div>
  <div class="try-this">
    <div class="try-title">Try this</div>
    <ol><!-- TODO --></ol>
  </div>
</section>
```

## JS snippet

```js
// ==================== WIDGET: Z-SCORE ====================
(function() {
  const slider = document.getElementById("z-val");
  const valDisplay = document.getElementById("z-val-display");
  const zDisplay = document.getElementById("z-score-display");
  const interp = document.getElementById("z-interp");

  // TODO: point at chapter data
  const ARR = DATA.earnings;
  const FMT = fmtMoney; // or fmtInt, fmt

  const sStat = summary(ARR);
  const vmin = sStat.min, vmax = sStat.max;

  function render() {
    const c = themeColors();
    const frac = parseFloat(slider.value);
    const x = vmin + frac * (vmax - vmin);
    const z = (x - sStat.mean) / sStat.std;
    valDisplay.textContent = FMT(x);
    zDisplay.textContent = (z >= 0 ? "+" : "") + z.toFixed(2);
    const abs = Math.abs(z);
    interp.textContent = abs < 1 ? "Within 1 SD — middle ~68%."
      : abs < 2 ? "1–2 SD away — outer ~27%."
      : abs < 3 ? "2–3 SD away — outer ~5%: notably unusual."
      : "More than 3 SD — outer ~0.3%: very unusual.";

    const zArr = ARR.map(v => (v - sStat.mean) / sStat.std);
    const xs = linspace(Math.min(...zArr) - 0.3, Math.max(...zArr) + 0.3, 200);
    const bw = silvermanBW(zArr);
    const ys = gaussianKDE(zArr, xs, bw);

    const layout = baseLayout({
      height: 280,
      xaxis: Object.assign({}, baseLayout().xaxis, {
        title: { text: "Z-score (SDs from mean)", font: { color: c.textSoft } },
        zeroline: true, zerolinecolor: c.grid
      }),
      yaxis: Object.assign({}, baseLayout().yaxis, { title: { text: "Density", font: { color: c.textSoft } } }),
      shapes: [
        { type: "line", x0: z, x1: z, yref: "paper", y0: 0, y1: 1, line: { color: c.pink, width: 3 } },
        { type: "rect", x0: -1, x1: 1, yref: "paper", y0: 0, y1: 1, fillcolor: c.cyan, opacity: 0.07, line: { width: 0 } }
      ],
      annotations: [
        { x: z, y: 1.02, yref: "paper", text: `z = ${z.toFixed(2)}`, showarrow: false, font: { color: c.pink, size: 11 } },
        { x: 0, y: 0.04, yref: "paper", text: "±1 SD (~68%)", showarrow: false, font: { color: c.cyan, size: 10 } }
      ]
    });
    Plotly.react("z-chart", [{
      type: "scatter", mode: "lines", x: xs, y: ys,
      line: { color: c.purple, width: 2.5 }, fill: "tozeroy",
      fillcolor: "rgba(122,32,159,0.12)", name: "Density"
    }], layout, PLOTLY_CONFIG);
  }

  // init slider to median
  const medianFrac = (sStat.median - vmin) / (vmax - vmin);
  slider.value = medianFrac.toFixed(3);
  slider.addEventListener("input", render);
  window.__rerender_z = render;
  render();
})();
```

## Registry entry

```js
z: [
  // def should be the fraction representing the median — compute dynamically.
  // For chapter-specific default, set to the median-fraction string here:
  { id: "z-val", kind: "range", def: "0.21" }  // TODO: replace with actual median fraction
]
```

**Note:** the z-slider default should be `(median - min) / (max - min)` so Reset goes back to the median. You can compute this in Python and write it into the registry entry, or set it in the template during scaffolding.
