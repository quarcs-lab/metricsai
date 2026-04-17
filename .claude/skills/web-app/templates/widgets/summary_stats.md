# Widget: Summary statistics & the mean–median gap

## When to use

- Teaching measures of central tendency and dispersion on a single numeric variable.
- Illustrating how the mean chases outliers but the median barely moves.
- Any chapter that quotes mean/median/std for a specific dataset — use that dataset here.

## Pedagogical target

One Key Concept about robust vs. non-robust summary statistics. The outlier slider is what makes this widget land.

## Adapt to your chapter

- Replace the `DATASETS` registry with chapter datasets. Each entry needs `label`, `axisLabel`, `values()` returning an array, and a `fmt` function (`fmtMoney`, `fmtInt`, `fmt`).
- If a dataset doesn't make sense for outlier injection, disable the slider (`canOutlier = false`).
- Write 3–4 specific Try-this prompts tied to the chapter's actual numbers.
- Register controls in `REG` as `stats-dataset` (select) and `stats-outlier` (range).

## HTML snippet

```html
<section class="widget" id="stats">
  <div class="widget-head">
    <div>
      <span class="section-tag">§ X.X · Key Concept X.X</span>
      <h2>Summary statistics &amp; the mean–median gap</h2>
    </div>
    <button type="button" class="reset-btn" data-reset="stats">↺ Reset</button>
  </div>
  <p class="lede">For symmetric data, the mean and median nearly coincide. For skewed data, the mean gets pulled toward the long tail. Drag the outlier slider to see how the mean chases one extreme observation while the median barely notices.</p>
  <div class="controls">
    <div class="ctrl">
      <label for="stats-dataset">Dataset</label>
      <select id="stats-dataset">
        <!-- TODO: one <option> per chapter dataset -->
      </select>
    </div>
    <div class="ctrl" id="stats-outlier-wrap">
      <label for="stats-outlier">Inject synthetic outlier <span class="val" id="stats-outlier-val">off</span></label>
      <input type="range" id="stats-outlier" min="0" max="500" step="10" value="0">
    </div>
  </div>
  <div class="stats-grid" id="stats-grid"></div>
  <div class="delta-row hidden" id="stats-delta"></div>
  <div class="chart short" id="stats-chart"></div>
  <div class="callout" id="stats-callout"></div>
  <div class="try-this">
    <div class="try-title">Try this</div>
    <ol>
      <!-- TODO: 3–4 numbered imperative prompts specific to the chapter's data -->
    </ol>
  </div>
</section>
```

## JS snippet

```js
// ==================== WIDGET: SUMMARY STATS ====================
(function() {
  const DATASETS = {
    // TODO: replace with the chapter's real datasets
    // key: { label, axisLabel, values: () => DATA.key, fmt: fmtMoney|fmtInt|fmt, outlierScale: 1000 }
  };

  const select = document.getElementById("stats-dataset");
  const outlier = document.getElementById("stats-outlier");
  const outlierVal = document.getElementById("stats-outlier-val");
  const outlierWrap = document.getElementById("stats-outlier-wrap");
  const gridEl = document.getElementById("stats-grid");
  const callout = document.getElementById("stats-callout");
  const deltaEl = document.getElementById("stats-delta");

  function render() {
    const key = select.value;
    const ds = DATASETS[key];
    const values = [...ds.values()];
    const baseline = summary(ds.values());
    const canOutlier = ds.outlierScale !== undefined;
    outlierWrap.style.opacity = canOutlier ? "1" : "0.4";
    outlier.disabled = !canOutlier;
    if (canOutlier && outlier.value > 0) {
      values.push(Number(outlier.value) * ds.outlierScale);
      outlierVal.textContent = ds.fmt(Number(outlier.value) * ds.outlierScale) + " added";
    } else {
      outlierVal.textContent = "off";
    }
    const s = summary(values);

    const cells = [
      ["n", fmt(s.n, 0), ""],
      ["Mean", ds.fmt(s.mean), "mean"],
      ["Median", ds.fmt(s.median), "median"],
      ["Std dev", ds.fmt(s.std), "spread"],
      ["Min", ds.fmt(s.min), ""],
      ["Q1", ds.fmt(s.q1), ""],
      ["Q3", ds.fmt(s.q3), ""],
      ["Max", ds.fmt(s.max), ""],
      ["IQR", ds.fmt(s.q3 - s.q1), "spread"],
      ["Skewness", s.skew.toFixed(2), ""],
      ["Excess kurt.", s.kurt.toFixed(2), ""]
    ];
    gridEl.innerHTML = cells.map(([l, v, cls]) =>
      `<div class="stat ${cls}"><div class="label">${l}</div><div class="value">${v}</div></div>`
    ).join("");

    if (canOutlier && outlier.value > 0) {
      const dMean = s.mean - baseline.mean;
      const dMedian = s.median - baseline.median;
      const sign = v => v > 0 ? "+" : (v < 0 ? "−" : "");
      deltaEl.classList.remove("hidden");
      deltaEl.innerHTML =
        `<span><span class="label">Δ mean vs baseline:</span><span class="delta-mean">${sign(dMean)}${ds.fmt(Math.abs(dMean))}</span></span>` +
        `<span><span class="label">Δ median vs baseline:</span><span class="delta-median">${sign(dMedian)}${ds.fmt(Math.abs(dMedian))}</span></span>` +
        `<span><span class="label">mean moved</span><span class="delta-mean">${(Math.abs(dMean) / Math.max(Math.abs(dMedian), 1e-9)).toFixed(1)}×</span><span class="label">more than median</span></span>`;
    } else {
      deltaEl.classList.add("hidden");
      deltaEl.innerHTML = "";
    }

    const skewLabel = Math.abs(s.skew) < 0.5 ? "approximately symmetric"
                    : Math.abs(s.skew) < 1 ? "moderately " + (s.skew > 0 ? "right-skewed" : "left-skewed")
                    : "highly " + (s.skew > 0 ? "right-skewed" : "left-skewed");
    const gap = s.mean - s.median;
    callout.innerHTML = `<strong>Read:</strong> the distribution is <em>${skewLabel}</em>
      (skewness ${s.skew.toFixed(2)}). Mean exceeds median by ${ds.fmt(Math.abs(gap))}
      (${(Math.abs(gap) / s.mean * 100).toFixed(1)}% of mean).`;

    const c = themeColors();
    const trace = {
      type: "box", x: values, name: ds.label, orientation: "h",
      boxpoints: "all", jitter: 0.5, pointpos: 0,
      marker: { color: c.cyan, size: 4, opacity: 0.55 },
      line: { color: c.purple }, fillcolor: "rgba(122,32,159,0.12)", hoverinfo: "x"
    };
    const layout = baseLayout({
      height: 300,
      xaxis: Object.assign({}, baseLayout().xaxis, { title: { text: ds.axisLabel, font: { color: c.textSoft } } }),
      yaxis: Object.assign({}, baseLayout().yaxis, { showticklabels: false }),
      shapes: [
        { type: "line", yref: "paper", y0: 0, y1: 1, x0: s.mean, x1: s.mean, line: { color: c.cyan, width: 2 } },
        { type: "line", yref: "paper", y0: 0, y1: 1, x0: s.median, x1: s.median, line: { color: c.pink, width: 2, dash: "dot" } }
      ],
      annotations: [
        { yref: "paper", y: 1.0, x: s.mean, text: "mean", showarrow: false, yanchor: "bottom", font: { color: c.cyan, size: 11 } },
        { yref: "paper", y: 1.08, x: s.median, text: "median", showarrow: false, yanchor: "bottom", font: { color: c.pink, size: 11 } }
      ]
    });
    Plotly.react("stats-chart", [trace], layout, PLOTLY_CONFIG);
  }

  select.addEventListener("change", () => { outlier.value = 0; render(); });
  outlier.addEventListener("input", render);
  window.__rerender_stats = render;
  render();
})();
```

## Registry entry

```js
stats: [
  { id: "stats-dataset", kind: "select", def: "<your-default-key>" },
  { id: "stats-outlier", kind: "range", def: "0" }
]
```
