# Widget: Categorical — bar vs. pie, sort toggles

## When to use

- Teaching how to summarize categorical data.
- Showing why bar charts usually beat pie charts for comparison.
- Anywhere the chapter presents counts or shares by category.

## Pedagogical target

Sort order and chart type are design choices that change what the viewer notices.

## HTML snippet

```html
<section class="widget" id="cat">
  <div class="widget-head">
    <div>
      <span class="section-tag">§ X.X · Key Concept X.X</span>
      <h2>Charts for categorical data</h2>
    </div>
    <button type="button" class="reset-btn" data-reset="cat">↺ Reset</button>
  </div>
  <p class="lede">Categorical data has no intrinsic ordering, so you impose one.</p>
  <div class="controls">
    <div class="ctrl">
      <label for="cat-dataset">Dataset</label>
      <select id="cat-dataset"><!-- TODO --></select>
    </div>
    <div class="ctrl">
      <label>Chart type</label>
      <div class="toggle-group" id="cat-type">
        <button type="button" data-val="bar" class="active">Bar</button>
        <button type="button" data-val="pie">Pie</button>
      </div>
    </div>
    <div class="ctrl">
      <label>Sort</label>
      <div class="toggle-group" id="cat-sort">
        <button type="button" data-val="value" class="active">By value</button>
        <button type="button" data-val="alpha">Alphabetical</button>
      </div>
    </div>
  </div>
  <div class="chart" id="cat-chart"></div>
  <div class="callout" id="cat-callout"></div>
  <div class="try-this">
    <div class="try-title">Try this</div>
    <ol><!-- TODO --></ol>
  </div>
</section>
```

## JS snippet

```js
// ==================== WIDGET: CATEGORICAL ====================
(function() {
  const DATASETS = {
    // TODO: key: { labels: () => [...], values: () => [...], unitLabel }
  };

  const select = document.getElementById("cat-dataset");
  const typeGroup = document.getElementById("cat-type");
  const sortGroup = document.getElementById("cat-sort");
  const callout = document.getElementById("cat-callout");
  let chartType = "bar", sortMode = "value";

  function render() {
    const c = themeColors();
    const ds = DATASETS[select.value];
    let labels = ds.labels().slice();
    let values = ds.values().slice();
    const idx = labels.map((_, i) => i);
    if (sortMode === "value") idx.sort((a, b) => values[b] - values[a]);
    else idx.sort((a, b) => labels[a].localeCompare(labels[b]));
    labels = idx.map(i => labels[i]);
    values = idx.map(i => values[i]);
    const total = values.reduce((a, b) => a + b, 0);
    const palette = [c.cyan, c.purple, c.pink, "#1aa6c4", "#933cb8", "#d73f88", "#00a3d1", "#8f39b3", "#56c3dc", "#b36bd1", "#e06aa5", "#0798c4", "#7a3fa3"];

    let traces, layout;
    if (chartType === "bar") {
      traces = [{
        type: "bar", x: labels, y: values,
        marker: { color: values.map((_, i) => palette[i % palette.length]) },
        hovertemplate: "%{x}<br>%{y:,.0f} (%{customdata:.1f}%)<extra></extra>",
        customdata: values.map(v => (v / total) * 100)
      }];
      layout = baseLayout({
        height: 360,
        xaxis: Object.assign({}, baseLayout().xaxis, { automargin: true, tickangle: -30 }),
        yaxis: Object.assign({}, baseLayout().yaxis, { title: { text: ds.unitLabel, font: { color: c.textSoft } } })
      });
    } else {
      traces = [{
        type: "pie", labels, values,
        marker: { colors: labels.map((_, i) => palette[i % palette.length]), line: { color: c.panel, width: 2 } },
        textinfo: "label+percent", textposition: "outside",
        hovertemplate: "%{label}<br>%{value:,.0f} (%{percent})<extra></extra>",
        hole: 0.35, sort: false
      }];
      layout = baseLayout({ height: 400, margin: { l: 20, r: 20, t: 30, b: 20 } });
    }
    Plotly.react("cat-chart", traces, layout, PLOTLY_CONFIG);
    callout.innerHTML = `<strong>${labels[0]}</strong> accounts for ${(values[0] / total * 100).toFixed(1)}% of the total.`;
  }

  select.addEventListener("change", render);
  [typeGroup, sortGroup].forEach(grp => {
    grp.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
      grp.querySelectorAll("button").forEach(x => x.classList.remove("active"));
      b.classList.add("active");
      if (grp === typeGroup) chartType = b.dataset.val;
      else sortMode = b.dataset.val;
      render();
    }));
  });
  window.__rerender_cat = render;
  render();
})();
```

## Registry entry

```js
cat: [
  { id: "cat-dataset", kind: "select", def: "<your-default>" },
  { group: "cat-type", kind: "toggle", def: "bar" },
  { group: "cat-sort", kind: "toggle", def: "value" }
]
```
