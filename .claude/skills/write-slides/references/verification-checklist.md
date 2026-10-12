# Verification checklist (Phase 4)

Four layers, all skipped only by `--no-verify`. The deck contains **no executable code** (code
blocks are `{.python}`, not `{python}`), so `quarto render` is a pure Pandoc render — no kernel
or package install is needed. All checks run against **local files** — the deck is a standalone
artifact, so there is no web server to probe.

---

## Layer 0 — Quarto render (with render-and-fix loop)

From the deck dir:

```bash
cd slides/chNN
/Users/carlosmendez/opt/bin/quarto render slides.qmd
```

Must produce `index.html` (> 30 KB) + a `slides_files/` directory. On failure, apply the
render-and-fix loop (max 3 attempts) using `render-and-fix.md`, then re-render. Common first-run
fix: if `embed-resources: true` is set, remove it (chalkboard is incompatible).

---

## Layer A — Local file / path checks (replaces the upstream Hugo HTTP checks)

No server. Assert on disk, from the deck dir:

| Check | Command / condition |
|---|---|
| `index.html` exists and is > 30 KB | `[ $(wc -c < index.html) -gt 30000 ]` |
| `slides_files/` assets dir exists | `[ -d slides_files ]` |
| the title visual summary resolves | `[ -f figures/visual_summary.png ]` |
| every `figures/*.png` referenced in `slides.qmd` exists | for each `![](figures/x.png)` → `[ -f figures/x.png ]` |
| no leaked `{{…}}` template markers | `! grep -q '{{[A-Z_]*}}' index.html` |

Layer B (the Node smoke test) automates the figure-path + marker checks; Layer A is the quick
manual gate if Node is unavailable.

---

## Layer B — Node static smoke test

```bash
BASE="$PWD/slides/chNN" node \
  .claude/skills/write-slides/references/templates/smoke-test.js
```

Exits 0/1, `[✓]/[✗]` per assertion. Checks the rendered files: `index.html` + `slides_files/` +
`slides.qmd` present; reveal structure; the **title visual-summary image** rendered; chalkboard +
menu wired in; speaker notes; **(if the deck has math) MathJax is referenced and the math spans
use `\(…\)` delimiters** — a static guard that catches the `html-math-method: katex` misconfig;
≥1 brand divider (`data-background-color`); 6 ≤ `<section>` ≤ 60; every `figures/*.png` referenced
exists on disk; no leaked `{{…}}` markers.

**Layer B's math guard is static** — it catches the **katex-misconfiguration** (wrong delimiters in
the emitted HTML), but it canNOT confirm math actually **renders at runtime** (e.g. a MathJax CDN
failure still ships raw `\hat\beta`). That is what Layer C catches.

**Takeaway-card check.** Confirm the deck's substantive content slides carry a `class="takeaway"`
element (the concluding DataPink accent card) — `grep -c 'class="[^"]*takeaway' index.html` should
be ≥1 and roughly match the number of content slides — and that the compiled theme CSS
(`slides_files/libs/revealjs/dist/theme/quarto-*.css`) contains the `.reveal .takeaway` rule. When
eyeballing (Layer C / preview), click through a takeaway slide and confirm the card renders as the
pink accent card and rises/fades in on its final fragment.

---

## Layer C — browser math-render check (MANDATORY when the deck has math)

The static layers cannot confirm runtime rendering. Drive a real browser to confirm the LaTeX
typesets — no `NODE_PATH` needed, `math-check.cjs` auto-locates Playwright:

```bash
node .claude/skills/write-slides/references/templates/math-check.cjs \
  "$PWD/slides/chNN/index.html"
# First run only, if Playwright is missing (exit 3):  npx playwright install chromium
```

`math-check.cjs` opens the deck in the system Chrome (bundled Chromium fallback), waits for MathJax,
traverses **every** slide (via `Reveal.next()`, covering the vertical content sub-slides under each
`#` divider), and **fails (`[✗]`) if any slide shows raw backslash-LaTeX** (`\hat`, `\(`, …); it
exits 0 only when all math rendered. If Playwright/Chrome is unavailable (exit 3), mark Layer C
`[~]` and fall back to a manual eyeball — open the deck and confirm `$R^2$` shows as R², not `R^2`.
**Never commit with raw LaTeX.**

---

## Report template (Phase 5)

```
VERIFICATION REPORT
===================
Deck:        slides/chNN/  (index.html + slides_files/)
Quarto:      <version>
Render:      <OK | FAILED>       Smoke test: <PASS | FAIL>

Render (Layer 0)
  [✓] quarto render → index.html (<size>) + slides_files/

Local file checks (Layer A)
  [✓] index.html > 30 KB · slides_files/ present
  [✓] figures resolve: <N>/<N> (incl. visual_summary.png)
  [✓] no leaked {{…}} markers

Node smoke test (Layer B)
  [✓] reveal structure · visual summary · chalkboard+menu · notes · figures · dividers
  OR [~] Skipped (--no-verify)

Browser math-render (Layer C)
  [✓] no raw LaTeX on any of <N> slides
  OR [~] Skipped (Playwright/Chrome unavailable — eyeballed instead)

Slide inventory
  [✓] <N> slides — <a> figure · <b> code · <c> table · <d> equation · Devil's-Advocate: <y/n>
  [✓] takeaway cards: <k> content slides end with a .takeaway card

Overall: <PASS | FAIL>
```

`[~]` = warning; PASS if no `[✗]`.

---

## Failure protocol

If any `[✗]`: surface the failed assertion with its path; suggest the matching `render-and-fix.md`
entry; offer a re-run. Do not report the deck as done.

---

## `--no-verify` minimal sanity (still do these)

- `index.html` exists and is > 30 KB; `slides_files/` exists; `slides.qmd` present.
- `figures/visual_summary.png` exists.

---

## Previewing note (Phase-5 follow-ups)

Open the deck directly: `open slides/chNN/index.html` (reveal.js runs from `file://`). Press **M**
(menu), **B** (chalkboard), **S** (speaker view), **O** (overview); `?print-pdf` exports a PDF. If
a `file://` quirk blocks an asset, serve locally instead:
`python3 -m http.server -d slides/chNN 8000` → `open http://localhost:8000/`.
