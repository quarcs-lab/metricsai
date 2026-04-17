# Widget: Histogram with bin-width slider + KDE overlay

## When to use

- Teaching the shape of a numeric distribution.
- Showing that bin-width choice changes the story, while KDE doesn't.
- Whenever the chapter shows a histogram. Always.

## Pedagogical target

One Key Concept about the subjectivity of bin choice and how a KDE removes it.

## Adapt to your chapter

- Define `DATASETS` registry with per-dataset `binRange` `[lo, hi]`, `defaultBin`, `axisLabel`, `values()`, `fmt`.
- Register controls `hist-dataset`, `hist-binwidth`, and toggle groups `hist-overlay`, `hist-markers`.

## HTML snippet

```html
<section class="widget" id="hist">
  <div class="widget-head">
    <div>
      <span class="section-tag">§ X.X · Key Concept X.X</span>
      <h2>Histograms &amp; kernel density — bin width matters</h2>
    </div>
    <button type="button" class="reset-btn" data-reset="hist">↺ Reset</button>
  </div>
  <p class="lede">Histograms summarize shape, but bin width changes the story. Narrow bins expose noise; wide bins paper over it. A kernel density estimate smooths across every choice of bin edge at once.</p>
  <div class="controls">
    <div class="ctrl">
      <label for="hist-dataset">Dataset</label>
      <select id="hist-dataset"><!-- TODO: options --></select>
    </div>
    <div class="ctrl">
      <label for="hist-binwidth">Bin width <span class="val" id="hist-binwidth-val"></span></label>
      <input type="range" id="hist-binwidth" min="0" max="100" step="1" value="30">
    </div>
    <div class="ctrl">
      <label>Overlay</label>
      <div class="toggle-group" id="hist-overlay">
        <button type="button" data-val="none" class="active">None</button>
        <button type="button" data-val="kde">KDE</button>
      </div>
    </div>
    <div class="ctrl">
      <label>Markers</label>
      <div class="toggle-group" id="hist-markers">
        <button type="button" data-val="on" class="active">Mean &amp; median</button>
        <button type="button" data-val="off">Off</button>
      </div>
    </div>
  </div>
  <div class="chart" id="hist-chart"></div>
  <div class="callout" id="hist-callout"></div>
  <div class="try-this">
    <div class="try-title">Try this</div>
    <ol><!-- TODO --></ol>
  </div>
</section>
```

## JS snippet

```js
// ==================== WIDGET: HISTOGRAM + KDE ====================
(function() {
  const DATASETS = {
    // TODO: key: { label, axisLabel, values: () => DATA.key, binRange: [lo, hi], defaultBin, fmt }
  };

  const select = document.getElementById("hist-dataset");
  const bwSlider = document.getElementById("hist-binwidth");
  const bwVal = document.getElementById("hist-binwidth-val");
  const overlayGroup = document.getElementById("hist-overlay");
  const markerGroup = document.getElementById("hist-markers");
  const callout = document.getElementById("hist-callout");
  let overlayMode = "none", markerMode = "on";

  function sliderToBin(key) {
    const [lo, hi] = DATASETS[key].binRange;
    return Math.round(lo + (bwSlider.value / 100) * (hi - lo));
  }
  function binToSlider(key, bw) {
    const [lo, hi] = DATASETS[key].binRange;
    return Math.round((bw - lo) / (hi - lo) * 100);
  }

  function render() {
    const key = select.value;
    const ds = DATASETS[key];
    const values = ds.values();
    const binWidth = sliderToBin(key);
    bwVal.textContent = ds.fmt(binWidth);
    const c = themeColors();
    const s = summary(values);

    const traces = [{
      type: "histogram", x: values, xbins: { size: binWidth },
      marker: { color: c.cyan, line: { color: c.panel, width: 1 } },
      opacity: 0.85, name: "Count"
    }];

    const shapes = [], annotations = [];
    if (markerMode === "on") {
      shapes.push(
        { type: "line", x0: s.mean, x1: s.mean, yref: "paper", y0: 0, y1: 1, line: { color: c.cyan, width: 2 } },
        { type: "line", x0: s.median, x1: s.median, yref: "paper", y0: 0, y1: 1, line: { color: c.pink, width: 2, dash: "dot" } }
      );
      annotations.push(
        { x: s.mean, yref: "paper", y: 1.02, text: "mean", showarrow: false, font: { color: c.cyan, size: 11 } },
        { x: s.median, yref: "paper", y: 1.08, text: "median", showarrow: false, font: { color: c.pink, size: 11 } }
      );
    }

    if (overlayMode === "kde") {
      const lo = Math.min(...values), hi = Math.max(...values);
      const xs = linspace(lo, hi, 200);
      const bw = silvermanBW(values);
      const dens = gaussianKDE(values, xs, bw);
      const scaled = dens.map(d => d * values.length * binWidth);
      traces.push({
        type: "scatter", mode: "lines", x: xs, y: scaled,
        line: { color: c.purple, width: 2.5 }, name: "KDE"
      });
    }

    const layout = baseLayout({
      height: 360, barmode: "overlay",
      xaxis: Object.assign({}, baseLayout().xaxis, { title: { text: ds.axisLabel, font: { color: c.textSoft } } }),
      yaxis: Object.assign({}, baseLayout().yaxis, { title: { text: "Count", font: { color: c.textSoft } } }),
      showlegend: overlayMode === "kde",
      legend: { x: 0.98, y: 0.98, xanchor: "right", yanchor: "top", font: { color: c.text } },
      shapes, annotations
    });
    Plotly.react("hist-chart", traces, layout, PLOTLY_CONFIG);
    callout.innerHTML = `<strong>Now:</strong> skewness ${s.skew.toFixed(2)}. Mean ${ds.fmt(s.mean)} ${s.mean > s.median ? "above" : "below"} median ${ds.fmt(s.median)}.`;
  }

  select.addEventListener("change", () => {
    bwSlider.value = binToSlider(select.value, DATASETS[select.value].defaultBin);
    render();
  });
  bwSlider.addEventListener("input", render);
  overlayGroup.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
    overlayGroup.querySelectorAll("button").forEach(x => x.classList.remove("active"));
    b.classList.add("active"); overlayMode = b.dataset.val; render();
  }));
  markerGroup.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
    markerGroup.querySelectorAll("button").forEach(x => x.classList.remove("active"));
    b.classList.add("active"); markerMode = b.dataset.val; render();
  }));
  bwSlider.value = binToSlider(select.value, DATASETS[select.value].defaultBin);
  window.__rerender_hist = render;
  render();
})();
```

## Registry entry

```js
hist: [
  { id: "hist-dataset", kind: "select", def: "<your-default>" },
  { id: "hist-binwidth", kind: "range", def: "30" },
  { group: "hist-overlay", kind: "toggle", def: "none" },
  { group: "hist-markers", kind: "toggle", def: "on" }
]
```
