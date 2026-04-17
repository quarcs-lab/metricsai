# Widget: <name>

Template for authoring a new widget pattern. When you invent one for a chapter, save a copy of this file, fill it in, and commit it so the next chapter can reuse it. Update `docs/widget_catalog.md` too.

## When to use

- Concrete pedagogical situations where this widget is the right tool.

## Pedagogical target

- The single Key Concept this widget is designed to teach.
- Why this particular interaction (what slider / toggle / etc.) makes that concept stick.

## Adapt to your chapter

- Which dataset shape does this expect? (`{ values: [...] }` or `{ x: [...], y: [...] }` etc.)
- What controls does the author need to register?
- Any chart-type-specific gotchas (scale, axis formatting, etc.)?

## HTML snippet

```html
<section class="widget" id="<widget-id>">
  <div class="widget-head">
    <div>
      <span class="section-tag">§ X.X · Key Concept X.X</span>
      <h2><title></h2>
    </div>
    <button type="button" class="reset-btn" data-reset="<widget-id>">↺ Reset</button>
  </div>
  <p class="lede">TODO</p>
  <div class="controls">
    <!-- controls here -->
  </div>
  <div class="chart" id="<widget-id>-chart"></div>
  <div class="callout" id="<widget-id>-callout"></div>
  <div class="try-this">
    <div class="try-title">Try this</div>
    <ol><!-- 2-4 numbered imperative experiments --></ol>
  </div>
</section>
```

## JS snippet

```js
// ==================== WIDGET: <NAME> ====================
(function() {
  // TODO: grab controls, call render() on each change
  function render() {
    const c = themeColors();
    // Build traces + layout, call Plotly.react("<widget-id>-chart", ..., ..., PLOTLY_CONFIG)
  }
  window.__rerender_<widget_id> = render;
  render();
})();
```

## Registry entry

```js
<widget_id>: [
  // { id: "<ctrl-id>", kind: "select"|"range", def: "<value>" },
  // { group: "<group-id>", kind: "toggle", def: "<value>" }
]
```

## Rules

- Expose `window.__rerender_<widget_id>` for the theme toggle and hash/reset layer.
- Use `themeColors()` inside `render()` so dark/light mode flips work.
- Use `baseLayout(overrides)` — never hand-roll a Plotly layout from scratch.
- Every `render()` call goes through `Plotly.react` (not `.newPlot`) so resizes are cheap.
- Write the Try-this block yourself for the chapter — don't paste generic prompts.
