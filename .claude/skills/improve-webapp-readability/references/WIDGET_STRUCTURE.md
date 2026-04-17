# Widget Structure Reference

Copy-pasteable HTML skeleton and CSS for the six-part widget pattern. Every widget in a metricsAI chapter web app must follow this order after `/improve-webapp-readability`.

---

## The six-part order

```
<section class="widget" id="…">
  1. widget-head (h2 + Reset button)     — existing
  2. .motivation                         — NEW
  3. .key-concept                        — NEW
  4. .widget-howto                       — NEW
  5. .controls  +  .chart  +  .callout   — existing, untouched
  6. .try-this (with reveals)            — REWRITTEN
  7. .takeaway                           — NEW
</section>
```

Do not reorder. Do not interleave. Do not add new top-level blocks without good reason.

---

## HTML skeleton (drop-in for any widget)

Replace the `…` placeholders. Everything inside `.controls`, `.chart`, `.stats-grid`, `.delta-row`, `.callout`, etc. stays as it was.

```html
<section class="widget" id="WIDGET_ID">
  <div class="widget-head">
    <div>
      <h2>WIDGET TITLE</h2>
    </div>
    <button type="button" class="reset-btn" data-reset="WIDGET_ID">↺ Reset</button>
  </div>

  <p class="motivation">ONE OR TWO SHORT QUESTION-FRAMED SENTENCES on why the tool matters. Use <em>italic</em> for the reveal word.</p>

  <div class="key-concept">
    <span class="kc-title">ONE BOLDED PLAIN-ENGLISH SENTENCE STATING THE CONCEPT.</span> FOLLOWING SENTENCES, COPIED FROM THE CHAPTER'S KEY CONCEPT BLOCKQUOTE, LIGHTLY TIGHTENED. USE <strong>BOLD</strong> FOR ANCHOR TERMS LIKE <strong>bin width</strong>, <strong>mean</strong>, <strong>IQR</strong>.
  </div>

  <div class="widget-howto">
    <div class="howto-title">What you can do here</div>
    <ul>
      <li><strong>ACTION 1</strong> — plain-language explanation.</li>
      <li><strong>ACTION 2</strong> — plain-language explanation.</li>
      <li><strong>ACTION 3</strong> — plain-language explanation.</li>
    </ul>
  </div>

  <div class="controls"> … unchanged … </div>
  <div class="chart" id="WIDGET_ID-chart"></div>
  <div class="callout" id="WIDGET_ID-callout"></div>

  <div class="try-this">
    <div class="try-title">Try this</div>
    <ol>
      <li><strong>Bolded directive.</strong> Neutral description of what happens. <em>The reveal sentence.</em></li>
      <li><strong>Bolded directive.</strong> Neutral description of what happens. <em>The reveal sentence.</em></li>
      <li><strong>Bolded directive.</strong> Neutral description of what happens. <em>The reveal sentence.</em></li>
    </ol>
  </div>

  <p class="takeaway"><strong>Take-away:</strong> ONE CLEAN SENTENCE SUMMARIZING THE WIDGET. <a href="../../book/_book/notebooks_quarto/chNN_FILENAME.html#SECTION-ANCHOR" target="_blank" rel="noopener">Read §N.M in the chapter →</a></p>
</section>
```

### Notes

- The `section-tag` span badge that used to sit above the `<h2>` is removed. The concept ID is redundant once the `.key-concept` callout is present.
- The `kc-label` span that used to sit at the top of the `.key-concept` box is also removed. The first bolded sentence already signals "this is the concept."
- Keep the Reset button in the `widget-head`, not elsewhere.
- For non-interactive widgets (pure comparison views with no sliders), omit the Reset button and write the `.widget-howto` bullets as observations ("**Compare Panel A and Panel B** — look for the kink in the log slope.") rather than actions.

---

## CSS (drop-in for any chapter)

Append to the chapter's `<style>` block, just after the existing `.try-this` rules. Remove the old `.section-tag` rule once no widget uses it.

```css
.try-this li { margin: 0.35rem 0; }
.try-this li strong { color: var(--text); }

.motivation {
  font-size: 1.0rem;
  line-height: 1.55;
  color: var(--text);
  background: color-mix(in srgb, var(--accent-3) 7%, transparent);
  border-left: 3px solid var(--accent-3);
  padding: 0.7rem 0.95rem;
  border-radius: 8px;
  margin: 0.3rem 0 0.9rem;
  max-width: 820px;
}
.motivation em { color: var(--accent-3); font-style: normal; font-weight: 500; }

.key-concept {
  background: color-mix(in srgb, var(--accent-2) 10%, transparent);
  border-left: 4px solid var(--accent-2);
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin: 0 0 0.9rem;
  font-size: 0.95rem;
  color: var(--text);
  max-width: 820px;
}
.key-concept .kc-title { font-weight: 600; color: var(--accent-2); }

.widget-howto {
  margin: 0.2rem 0 0.9rem;
  font-size: 0.9rem;
  color: var(--text-soft);
}
.widget-howto .howto-title {
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
}
.widget-howto ul { margin: 0; padding-left: 1.15rem; }
.widget-howto li { margin: 0.15rem 0; }
.widget-howto li strong { color: var(--text); font-weight: 600; }

.takeaway {
  margin: 0.9rem 0 0;
  padding-top: 0.7rem;
  border-top: 1px dashed var(--border);
  font-size: 0.88rem;
  color: var(--text-soft);
}
.takeaway strong { color: var(--text); }
.takeaway a {
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
}
.takeaway a:hover { text-decoration: underline; }
```

### Palette reuse (no new colors)

| Class | Accent variable | Why |
|---|---|---|
| `.motivation` | `--accent-3` (pink) | The "why it matters" opener is the most emotional block — pink signals it. |
| `.key-concept` | `--accent-2` (purple) | Purple is the brand's concept/knowledge color — reused here. |
| `.widget-howto` | `--text-muted` | Quiet supporting text — no accent. |
| `.takeaway` | `--accent` (cyan) | Cyan closes the loop: Try-this is cyan, take-away link is cyan. |
| `.try-this` | `--accent` (cyan) | Unchanged. |

If a chapter app uses different brand variables, map by role, not by name: pink for motivation, purple for the concept, quiet for how-to, cyan for interaction/links.

---

## Optional — global intro card

Include only when the user asks for it. Chapter 2 removed its intro card on review because the widget structure is already self-explanatory.

```html
<section class="howto-card" aria-label="How to read this dashboard">
  <h2>How to read this dashboard</h2>
  <p>Each widget below teaches one <strong>Key Concept</strong> from Chapter N.</p>
  <ul>
    <li><strong>Why this matters</strong> — short motivation.</li>
    <li><strong>Key Concept box</strong> (purple) — the concept in the book's own words.</li>
    <li><strong>What you can do here</strong> — the controls explained.</li>
    <li><strong>Interactive chart</strong> — play with sliders and toggles.</li>
    <li><strong>Try this</strong> — short experiments with the insight each reveals.</li>
    <li><strong>Take-away</strong> — one sentence plus a link back to the chapter.</li>
  </ul>
</section>
```

Its CSS (only if used):

```css
.howto-card {
  background: linear-gradient(135deg,
    color-mix(in srgb, var(--accent) 6%, transparent),
    color-mix(in srgb, var(--accent-2) 6%, transparent));
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.1rem 1.2rem;
  margin-bottom: 1.5rem;
}
.howto-card h2 { margin: 0 0 0.4rem; font-size: 1.05rem; color: var(--accent-2); }
.howto-card ul { margin: 0.3rem 0 0; padding-left: 1.2rem; font-size: 0.92rem; color: var(--text-soft); }
.howto-card li { margin: 0.2rem 0; }
.howto-card li strong { color: var(--text); }
```

---

## Pitfalls to avoid

- **Do not** turn `.key-concept` into a paraphrase. Copy the chapter's `.qmd` blockquote body, then tighten sentences — never invent meaning.
- **Do not** add a second "Key Concept 2.X" title above the box. The bolded opening sentence is the title.
- **Do not** merge `.motivation` into the lede prose. The whole point is that it is visually distinct.
- **Do not** write `.takeaway` text longer than one sentence. If you need two sentences, the first belongs in `.motivation` and the second is the take-away.
- **Do not** change the `id` of any widget or the `data-reset` attribute of its Reset button. JS depends on both.
- **Do not** move any `<div class="chart" id="…">` placeholder — Plotly mounts into those by id.
