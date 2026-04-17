# Widget: Box plot with IQR-multiplier slider

## When to use

- Teaching the 1.5·IQR outlier convention and that it's a choice, not a law.
- Showing how changing a rule changes the set of "outliers."
- Any chapter that introduces outliers or robust statistics.

## Pedagogical target

Outlier definition is a convention. Change the multiplier, change the verdict.

## HTML snippet

```html
<section class="widget" id="box">
  <div class="widget-head">
    <div>
      <span class="section-tag">§ X.X</span>
      <h2>Box plot &amp; the IQR rule for outliers</h2>
    </div>
    <button type="button" class="reset-btn" data-reset="box">↺ Reset</button>
  </div>
  <p class="lede">The convention is to flag any point farther than 1.5 × IQR from the nearest quartile as an outlier — but 1.5 is a choice, not a law. Drag the multiplier.</p>
  <div class="controls">
    <div class="ctrl">
      <label for="box-dataset">Dataset</label>
      <select id="box-dataset"><!-- TODO --></select>
    </div>
    <div class="ctrl">
      <label for="box-mult">IQR multiplier <span class="val" id="box-mult-val">1.5</span></label>
      <input type="range" id="box-mult" min="1" max="3" step="0.1" value="1.5">
    </div>
  </div>
  <div class="chart short" id="box-chart"></div>
  <div class="callout" id="box-callout"></div>
  <div style="margin-top:.5rem"><div class="outlier-list" id="box-list"></div></div>
  <div class="try-this">
    <div class="try-title">Try this</div>
    <ol><!-- TODO --></ol>
  </div>
</section>
```

## JS snippet

```js
// ==================== WIDGET: BOX PLOT + IQR OUTLIERS ====================
(function() {
  const DATASETS = {
    // TODO: key: { label, axisLabel, values: () => DATA.key, fmt }
  };

  const select = document.getElementById("box-dataset");
  const mult = document.getElementById("box-mult");
  const multVal = document.getElementById("box-mult-val");
  const callout = document.getElementById("box-callout");
  const listEl = document.getElementById("box-list");

  function render() {
    const key = select.value;
    const ds = DATASETS[key];
    const values = ds.values();
    const s = summary(values);
    const iqr = s.q3 - s.q1;
    const m = parseFloat(mult.value);
    multVal.textContent = m.toFixed(1);
    const lowFence = s.q1 - m * iqr;
    const highFence = s.q3 + m * iqr;
    const outliers = values.filter(v => v < lowFence || v > highFence).sort((a, b) => b - a);

    const c = themeColors();
    const trace = {
      type: "box", x: values, orientation: "h", name: ds.label,
      boxpoints: "outliers",
      marker: { color: c.pink, size: 5, outliercolor: c.pink },
      line: { color: c.purple }, fillcolor: "rgba(0,140,183,0.12)",
      hoverinfo: "x+name"
    };
    const layout = baseLayout({
      height: 240,
      xaxis: Object.assign({}, baseLayout().xaxis, { title: { text: ds.axisLabel, font: { color: c.textSoft } } }),
      yaxis: Object.assign({}, baseLayout().yaxis, { showticklabels: false }),
      shapes: [
        { type: "line", x0: lowFence, x1: lowFence, yref: "paper", y0: 0, y1: 1, line: { color: c.pink, width: 1.5, dash: "dash" } },
        { type: "line", x0: highFence, x1: highFence, yref: "paper", y0: 0, y1: 1, line: { color: c.pink, width: 1.5, dash: "dash" } }
      ],
      annotations: [
        { x: lowFence, yref: "paper", y: 1.05, text: "−" + m.toFixed(1) + "·IQR", showarrow: false, font: { color: c.pink, size: 10 } },
        { x: highFence, yref: "paper", y: 1.05, text: "+" + m.toFixed(1) + "·IQR", showarrow: false, font: { color: c.pink, size: 10 } }
      ]
    });
    Plotly.react("box-chart", [trace], layout, PLOTLY_CONFIG);

    callout.innerHTML = `<strong>At ${m.toFixed(1)}× IQR:</strong> ${outliers.length} point${outliers.length === 1 ? "" : "s"} flagged.
      Fences [${ds.fmt(lowFence)}, ${ds.fmt(highFence)}]. IQR = ${ds.fmt(iqr)}.`;
    listEl.innerHTML = outliers.length
      ? "Flagged: " + outliers.slice(0, 20).map(ds.fmt).join(", ") + (outliers.length > 20 ? ` … (+${outliers.length - 20} more)` : "")
      : "No observations outside the fences.";
  }

  select.addEventListener("change", render);
  mult.addEventListener("input", render);
  window.__rerender_box = render;
  render();
})();
```

## Registry entry

```js
box: [
  { id: "box-dataset", kind: "select", def: "<your-default>" },
  { id: "box-mult", kind: "range", def: "1.5" }
]
```
