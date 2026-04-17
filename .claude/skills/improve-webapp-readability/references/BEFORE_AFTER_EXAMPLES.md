# Before / After Examples

Real rewrites from the Chapter 2 pass. Use these as the style baseline for every chapter.

---

## Example 1 — Summary statistics widget (`#stats`, §2.1)

### Before

```html
<section class="widget" id="stats">
  <div class="widget-head">
    <div>
      <span class="section-tag">§ 2.1 · Key Concept 2.1</span>
      <h2>Summary statistics &amp; the mean–median gap</h2>
    </div>
    <button type="button" class="reset-btn" data-reset="stats">↺ Reset</button>
  </div>
  <p class="lede">For symmetric data, the mean and median nearly coincide. For skewed data, the mean gets pulled toward the long tail. Pick a dataset and watch both move. Then drag the outlier slider on the earnings series to see how the mean chases a single extreme observation while the median barely notices.</p>
```

**What is wrong:**

- The concept label (`§ 2.1 · Key Concept 2.1`) is a faint badge above the heading. A beginner reads the lede first, interacts, and only realizes which concept it maps to afterward.
- The `.lede` is four sentences of 18–28 words each. Dense and jargon-forward ("skewed," "long tail," "mean chases").
- There is no sentence answering the student's implicit question: *why should I care about this?*
- No bulleted how-to — the controls are described only implicitly inside the lede.
- No take-away pointing the student back to the chapter.

### After

```html
<section class="widget" id="stats">
  <div class="widget-head">
    <div>
      <h2>Summary statistics &amp; the mean–median gap</h2>
    </div>
    <button type="button" class="reset-btn" data-reset="stats">↺ Reset</button>
  </div>

  <p class="motivation">What is a <em>typical</em> worker's earnings? One common answer is "the average." But averages can mislead when a few people earn much more than the rest. Which number should you trust — the mean or the median?</p>

  <div class="key-concept">
    <span class="kc-title">Summary statistics condense a dataset into a few interpretable numbers.</span> They describe the <strong>center</strong> (mean, median) and the <strong>spread</strong> (standard deviation, quartiles). The median is more <strong>robust to outliers</strong> than the mean, which makes it preferred for skewed data like incomes and wealth.
  </div>

  <div class="widget-howto">
    <div class="howto-title">What you can do here</div>
    <ul>
      <li><strong>Pick a dataset</strong> — earnings (skewed), GDP (roughly symmetric), or home sales.</li>
      <li><strong>Watch the mean and median</strong> update together in the stats cards and on the chart.</li>
      <li><strong>Drag the outlier slider</strong> (earnings only) to add one fake high earner and see who moves.</li>
    </ul>
  </div>

  <!-- controls + chart unchanged -->

  <div class="try-this">
    <div class="try-title">Try this</div>
    <ol>
      <li><strong>Add one fake high earner.</strong> On the earnings dataset, drag the slider to $500k. The mean jumps by thousands; the median barely moves. <em>That is what "robust to outliers" means.</em></li>
      <li><strong>Switch to U.S. real GDP per capita.</strong> The mean and median are almost identical. The distribution over time is close to symmetric — no long tail pulling the mean.</li>
      <li><strong>Switch to monthly home sales.</strong> The mean sits above the median again. Housing markets have big boom months but floors in the bust, so the right tail pulls the mean up.</li>
    </ol>
  </div>

  <p class="takeaway"><strong>Take-away:</strong> when the mean and median disagree, the data is skewed — and the median usually gives the more honest summary. <a href="../../book/_book/notebooks_quarto/ch02_Univariate_Data_Summary.html#summary-statistics" target="_blank" rel="noopener">Read §2.1 in the chapter →</a></p>
</section>
```

**What improved:**

- The `.motivation` opens with a question anchored to the student's intuition — not to a math concept.
- The `.key-concept` states the idea in one bolded sentence, then uses the chapter's own words for the body. Anchor terms are bolded for scan-reading.
- The `.widget-howto` bullets describe each control with a **bolded action** and a plain explanation.
- Each Try-this step ends with a reveal (`The mean jumps by thousands; the median barely moves.`) — the student gets the insight without having to infer it.
- The take-away is one sentence plus a chapter link.

---

## Example 2 — Z-score widget (`#z`, §2.5)

### Before

```html
<p class="lede">Standardization expresses every observation as a distance from the mean, measured in standard deviations: <code>z = (x − mean) / sd</code>. Roughly 68% of a bell-shaped distribution falls within ±1, 95% within ±2, and 99.7% within ±3. Drag the slider to pick an earnings value and read off its z-score.</p>
```

**What is wrong:**

- Opens with the formula. A beginner has not yet been told *why* they would standardize anything.
- The 68/95/99.7 rule is a dense run-on. Should be a bulleted list.
- "Drag the slider to pick an earnings value and read off its z-score" is instrumentation, not motivation.

### After

```html
<p class="motivation">Is $100,000 a high income? The word <em>high</em> has no meaning by itself. High compared to whom? Standardization gives us one: <em>how many standard deviations away from the mean?</em></p>

<div class="key-concept">
  <span class="kc-title">A z-score rescales any observation onto a common ruler.</span> The formula is simple: <code>z = (x − mean) / sd</code>. It measures distance from the mean <strong>in units of standard deviation</strong>. For bell-shaped data, three rules of thumb:
  <ul style="margin:0.45rem 0 0 0;padding-left:1.15rem">
    <li>About <strong>68%</strong> of observations fall within ±1.</li>
    <li>About <strong>95%</strong> within ±2.</li>
    <li>About <strong>99.7%</strong> within ±3.</li>
  </ul>
</div>

<div class="widget-howto">
  <div class="howto-title">What you can do here</div>
  <ul>
    <li><strong>Drag the slider</strong> to pick any earnings value.</li>
    <li><strong>Read the z-score</strong> and plain-language interpretation live.</li>
    <li><strong>Watch the chart</strong> show where your pick sits on the distribution.</li>
  </ul>
</div>
```

**What improved:**

- Motivation opens with a concrete income the student can picture, not with a definition.
- The formula appears *inside* the `.key-concept`, after one sentence has already explained what a z-score is conceptually.
- The 68/95/99.7 rule is bulleted, so the eye can lock onto the three numbers.

### Try-this before

```html
<li>Drag to $36,000 (the median). The z-score should be close to zero.</li>
<li>Drag to $100,000. Interpretation: this observation is rare on the high side — roughly how many SD above the mean?</li>
<li>Drag to the maximum ($172,000). Does it exceed the 2σ rule of thumb? Would you call this an outlier, and why or why not?</li>
```

**What is wrong:** step 2 ends in a question with no reveal; step 3 asks the student to decide without giving the numerical anchor to confirm their answer.

### Try-this after

```html
<li><strong>Drag to $36,000</strong> (the median). The z-score lands near zero. This earner is typical — right at the center of the distribution.</li>
<li><strong>Drag to $100,000.</strong> The z-score is around +2, which puts this earner in the top ~2.5% by the rule of thumb. Rare, but not impossibly so.</li>
<li><strong>Drag to the maximum (~$172,000).</strong> The z-score is well above +3. Under the 2σ rule this is a clear outlier — fewer than one in a hundred observations would land this high in a bell-shaped distribution.</li>
```

**What improved:** every step now ends with a concrete numerical anchor and an insight sentence. No ambiguity; the student can check their understanding.

---

## Example 3 — Log transform widget (`#log`, §2.5), non-interactive

### Before

```html
<p class="lede">The natural log does two things economists love. On a cross-section it compresses the big values and stretches the small ones, turning a right-skewed distribution into something close to symmetric. On a time series it turns exponential growth into a straight line, so the slope reads directly as the growth rate.</p>
```

Followed later by:

```html
<li><strong>Cross-section:</strong> compare the skewness numbers on the two earnings histograms. 1.70 → roughly zero is the textbook before/after.</li>
```

Combined with **the first sentence of §2.6's moving-average widget**, the student had also been told "Try widening the window…" — but the log-transform widget has **no slider**. Copy/paste leftover.

### After

```html
<p class="motivation">When most observations are small and a few are huge, a histogram looks like a wall with a long tail. Exponential growth over two centuries looks like a vertical cliff. The natural log rebalances both views — revealing shape where the raw data hides it.</p>

<div class="key-concept">
  <span class="kc-title">Taking the log of a variable compresses the big values and stretches the small ones.</span> That has two concrete payoffs: (1) a right-skewed cross-section often becomes close to <strong>symmetric</strong>, which is friendlier for the statistics that come later; and (2) an exponential time series becomes a <strong>straight line</strong>, where the slope reads directly as the growth rate.
</div>

<div class="widget-howto">
  <div class="howto-title">What you can do here</div>
  <ul>
    <li><strong>Compare four charts side by side</strong> — this widget has no controls, only observations to make.</li>
    <li><strong>Panel A:</strong> the same earnings data shown raw (left) vs. after <code>ln()</code> (right).</li>
    <li><strong>Panel B:</strong> 200 years of U.S. real GDP per capita shown raw (left) vs. on a log scale (right).</li>
    <li><strong>Watch the skewness number</strong> on the earnings histograms, and the <strong>shape</strong> of the GDP curve.</li>
  </ul>
</div>
```

**What improved:**

- The motivation gives two concrete visual metaphors — "a wall with a long tail," "a vertical cliff" — before naming the tool.
- The `.widget-howto` explicitly states "this widget has no controls, only observations to make." The old lede had contradicted this. **Non-interactive widgets need this signal, or users will hunt for a slider that does not exist.**

---

## Pattern summary

Every rewrite above followed the same moves:

| Move | What it fixes |
|---|---|
| Replace `.lede` with `.motivation` + `.key-concept` | Student sees *why* before *how*; the concept is visually distinct from the prose. |
| Remove `section-tag` badge and `kc-label` | Two pieces of "Key Concept 2.X" labeling compete; keep only the visible box. |
| Add `.widget-howto` bullets | Controls become self-documenting; the eye can scan them. |
| Rewrite each Try-this `<li>` with **action → description → reveal** | The student never has to guess what they were supposed to learn. |
| Add `.takeaway` with chapter link | Closes the loop and points the student back to the book. |

No new datasets. No new charts. No new JavaScript. Just prose that leads.
