# Widget: Log transformation — taming skew & linearizing exponential growth

## When to use

- Any chapter that introduces `ln(x)` as a variable transformation.
- Illustrating both cross-sectional (skew-taming) and time-series (hockey stick → line) benefits.
- Requires both a cross-sectional right-skewed variable and a long exponentially-growing time series.

## Pedagogical target

The log transformation does two things economists love. On a cross-section it compresses big values / stretches small ones, turning right-skew into symmetry. On a time series it turns exponential growth into a straight line whose slope is the growth rate.

## Adapt to your chapter

- **Cross-section (Section A):** point at a right-skewed chapter variable (earnings, income, population).
- **Time series (Section B):** for the hockey-stick effect to be visible, you need ≥ 150 years of data. Use Maddison-style long-run series via `scripts/fetch_maddison_us.py` or equivalent.
- If the chapter uses Maddison data, attribute it in the footer and in `web-apps/chNN/PLAN.md`.

## HTML snippet

```html
<section class="widget" id="log">
  <div class="widget-head">
    <div>
      <span class="section-tag">§ X.X · Key Concept X.X</span>
      <h2>Log transformation — taming skew and linearizing exponential growth</h2>
    </div>
  </div>
  <p class="lede">TODO chapter-specific lede covering both motivations.</p>

  <h3 class="subhead"><span class="subhead-tag">A ·</span>Cross-section: before and after ln()</h3>
  <div class="two-col">
    <div><div class="chart short" id="log-raw"></div></div>
    <div><div class="chart short" id="log-log"></div></div>
  </div>
  <div class="callout" id="log-callout"></div>

  <h3 class="subhead"><span class="subhead-tag">B ·</span>Time series: the hockey stick</h3>
  <div class="two-col">
    <div><div class="chart short" id="log-ts-raw"></div></div>
    <div><div class="chart short" id="log-ts-log"></div></div>
  </div>
  <div class="callout" id="log-ts-callout"></div>

  <div class="try-this">
    <div class="try-title">Try this</div>
    <ol><!-- TODO --></ol>
  </div>
</section>
```

## JS snippet

```js
// ==================== WIDGET: LOG TRANSFORM ====================
(function() {
  const callout = document.getElementById("log-callout");
  const tsCallout = document.getElementById("log-ts-callout");

  // TODO: point at your right-skewed cross-section variable
  const RAW_DATA = DATA.earnings;
  const RAW_AXIS = "Earnings ($)";

  // TODO: point at your long time series (years + values)
  const LONG_SERIES = DATA.gdp_long; // { years, values, source }
  const LONG_UNITS = "$ (2011 PPP)";

  function render() {
    const c = themeColors();

    // --- Cross-section ---
    const raw = RAW_DATA;
    const logv = raw.map(v => Math.log(v));
    const sR = summary(raw);
    const sL = summary(logv);

    const mkLayout = (title, titleColor, xAxis, skew, kurt) => baseLayout({
      height: 300,
      title: { text: title, font: { color: titleColor, size: 13 } },
      xaxis: Object.assign({}, baseLayout().xaxis, { title: { text: xAxis, font: { color: c.textSoft } } }),
      yaxis: Object.assign({}, baseLayout().yaxis, { title: { text: "Count", font: { color: c.textSoft } } }),
      annotations: [{
        x: 0.98, xref: "paper", y: 0.95, yref: "paper", xanchor: "right", showarrow: false,
        text: `skew = ${skew.toFixed(2)}<br>kurt = ${kurt.toFixed(2)}`,
        font: { color: c.purple, size: 11, family: "JetBrains Mono" }, align: "right"
      }]
    });
    Plotly.react("log-raw",
      [{ type: "histogram", x: raw, nbinsx: 25, marker: { color: c.cyan, line: { color: c.panel, width: 1 } }, opacity: 0.85 }],
      mkLayout("Raw", c.cyan, RAW_AXIS, sR.skew, sR.kurt), PLOTLY_CONFIG);
    Plotly.react("log-log",
      [{ type: "histogram", x: logv, nbinsx: 25, marker: { color: c.purple, line: { color: c.panel, width: 1 } }, opacity: 0.85 }],
      mkLayout("Log-transformed", c.purple, "ln(" + RAW_AXIS + ")", sL.skew, sL.kurt), PLOTLY_CONFIG);
    callout.innerHTML = `<strong>Before:</strong> skewness ${sR.skew.toFixed(2)}. <strong>After ln():</strong> skewness ${sL.skew.toFixed(2)}.`;

    // --- Time series ---
    const years = LONG_SERIES.years;
    const gdpv = LONG_SERIES.values;
    const logGdp = gdpv.map(v => Math.log(v));
    const fitLevel = linfit(years, gdpv);
    const fitLog = linfit(years, logGdp);
    const annualGrowthPct = fitLog.slope * 100;
    const totalYears = years[years.length - 1] - years[0];
    const cagr = (Math.pow(gdpv[gdpv.length - 1] / gdpv[0], 1 / totalYears) - 1) * 100;
    const y0 = years[0], yN = years[years.length - 1];
    const v0 = gdpv[0], vN = gdpv[gdpv.length - 1];
    const sourceTag = { x: 0.02, xref: "paper", y: -0.18, yref: "paper", xanchor: "left", showarrow: false,
      text: "Data: " + (LONG_SERIES.source || ""), font: { color: c.textSoft, size: 9 } };
    const mkXAxis = () => Object.assign({}, baseLayout().xaxis, { title: { text: "Year", font: { color: c.textSoft } } });

    Plotly.react("log-ts-raw", [
      { type: "scatter", mode: "lines", x: years, y: gdpv, line: { color: c.cyan, width: 2.2 }, name: "level" },
      { type: "scatter", mode: "lines", x: years, y: fitLevel.fitted, line: { color: c.pink, width: 1.4, dash: "dash" }, name: "linear fit" }
    ], baseLayout({
      height: 320,
      title: { text: `Level (${y0}–${yN})`, font: { color: c.cyan, size: 13 } },
      xaxis: mkXAxis(),
      yaxis: Object.assign({}, baseLayout().yaxis, { title: { text: LONG_UNITS, font: { color: c.textSoft } } }),
      margin: { l: 62, r: 18, t: 40, b: 58 },
      annotations: [sourceTag, {
        x: 0.98, xref: "paper", y: 0.06, yref: "paper", xanchor: "right", showarrow: false,
        text: `$${Math.round(v0).toLocaleString()} → $${Math.round(vN).toLocaleString()}<br>~${(vN/v0).toFixed(0)}× over ${totalYears} years`,
        font: { color: c.textSoft, size: 10, family: "JetBrains Mono" }, align: "right"
      }]
    }), PLOTLY_CONFIG);

    Plotly.react("log-ts-log", [
      { type: "scatter", mode: "lines", x: years, y: logGdp, line: { color: c.purple, width: 2.2 }, name: "ln(level)" },
      { type: "scatter", mode: "lines", x: years, y: fitLog.fitted, line: { color: c.pink, width: 1.4, dash: "dash" }, name: "linear fit" }
    ], baseLayout({
      height: 320,
      title: { text: `Log (${y0}–${yN})`, font: { color: c.purple, size: 13 } },
      xaxis: mkXAxis(),
      yaxis: Object.assign({}, baseLayout().yaxis, { title: { text: "ln(level)", font: { color: c.textSoft } } }),
      margin: { l: 62, r: 18, t: 40, b: 58 },
      annotations: [sourceTag, {
        x: 0.98, xref: "paper", y: 0.06, yref: "paper", xanchor: "right", showarrow: false,
        text: `fitted slope = ${annualGrowthPct.toFixed(2)}% / year`,
        font: { color: c.purple, size: 10, family: "JetBrains Mono" }, align: "right"
      }]
    }), PLOTLY_CONFIG);
    tsCallout.innerHTML = `Fitted slope <strong>${annualGrowthPct.toFixed(2)}%/yr</strong>; sample CAGR ${cagr.toFixed(2)}%.`;
  }

  window.__rerender_log = render;
  render();
})();
```

## Registry entry

Nothing — this widget has no controls (intentionally simple). No entry needed in `REG`.
