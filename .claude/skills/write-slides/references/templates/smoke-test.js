// smoke-test.js — verifies a Quarto-rendered reveal.js deck WITHOUT a browser.
//
// Usage:
//   BASE=/abs/path/to/metricsai/slides/chNN node smoke-test.js
//
// The deck is rendered by `quarto render slides.qmd` to index.html + slides_files/
// (non-embedded, because the chalkboard plugin requires external assets). This script
// static-parses the rendered files and asserts structural invariants. Exits 0 on
// success, 1 on any failure, printing a [✓]/[✗] line per assertion.

const fs = require("fs");
const path = require("path");

const BASE = process.env.BASE;
if (!BASE) { console.error("smoke-test.js: BASE env variable required"); process.exit(2); }

function read(name) {
  try { return fs.readFileSync(path.join(BASE, name), "utf8"); }
  catch (e) { return null; }
}

const html = read("index.html");
const results = [];
function check(name, cond, detail) { results.push({ name, ok: !!cond, detail: detail || "" }); }

// 0. expected bundle files
check("index.html exists", html !== null);
check("slides_files/ assets dir exists", fs.existsSync(path.join(BASE, "slides_files")));
check("slides.qmd source committed", fs.existsSync(path.join(BASE, "slides.qmd")));

if (html !== null) {
  // 1. reveal structure
  check("reveal structure present (.reveal + .slides)",
        /class="reveal"/.test(html) && /class="slides"/.test(html));

  // 2. title visual-summary (full-bleed background painted by the custom title-slide partial)
  check("title visual-summary present (full-bleed background)",
        /data-background-image="[^"]*visual_summary/i.test(html) ||
        /class="[^"]*title-visual-summary/.test(html));

  // 3. core Quarto-revealjs features wired in
  check("chalkboard enabled", /chalkboard/i.test(html));
  check("menu plugin enabled", /menu/i.test(html));
  check("speaker notes present", /class="notes"/.test(html));
  check("figure click-to-zoom lightbox wired in", /figZoomOverlay/.test(html));

  // 3b. math engine sanity — catches the `html-math-method: katex` misconfig that ships raw
  //     LaTeX. MathJax emits `class="math inline">\(…`; broken KaTeX emits `…">\hat…`. This is
  //     a delimiter check only — runtime rendering is Layer C (the browser math-check.cjs).
  const mathSpans = (html.match(/class="math (inline|display)"/g) || []).length;
  if (mathSpans > 0) {
    check("math: MathJax engine referenced",
          /mathjax|tex-chtml|MathJax\.js/i.test(html), `${mathSpans} math span(s)`);
    check("math: spans use MathJax \\(…\\) delimiters, not raw \\command",
          !/class="math (inline|display)">\\[a-zA-Z]/.test(html));
  }

  // 3d. ≥1 Python code block — the deck must teach the chapter's main tools in code.
  const codeBlocks = (html.match(/<pre[^>]*class="[^"]*sourceCode/g) || []).length;
  check("≥1 Python code block present (main-tool coverage)", codeBlocks >= 1,
        `${codeBlocks} code block(s)`);

  // 4. brand dividers / dark slides
  const bg = (html.match(/data-background-color=/g) || []).length;
  check("≥1 brand divider / dark slide (data-background-color)", bg >= 1, `${bg} found`);

  // 5. slide-count sanity (Quarto wraps content; allow a wider band)
  const secs = (html.match(/<section/g) || []).length;
  check("slide count in 6..60", secs >= 6 && secs <= 60, `${secs} <section> tags`);

  // 6. figures referenced via figures/ (local bundle) exist on disk — the title-slide
  //    visual summary (a data-background-image) plus every body figure (<img src>).
  const imgs = [
    ...[...html.matchAll(/<img[^>]+src="(figures\/[^"]+)"/g)].map(m => m[1]),
    ...[...html.matchAll(/data-background-image="(figures\/[^"]+)"/g)].map(m => m[1]),
  ];
  const missing = imgs.filter(r => !fs.existsSync(path.resolve(BASE, r)));
  check("every figures/ path exists on disk", missing.length === 0,
        imgs.length ? `${imgs.length - missing.length}/${imgs.length} resolve` +
          (missing.length ? `; missing: ${missing.join(", ")}` : "") : "no figures referenced");

  // 7. no leaked template markers
  check("no leaked {{ }} substitution markers", !/\{\{[A-Z_]+\}\}/.test(html));
}

let failed = 0;
for (const r of results) {
  console.log(`${r.ok ? "[✓]" : "[✗]"} ${r.name}${r.detail ? "  (" + r.detail + ")" : ""}`);
  if (!r.ok) failed++;
}
console.log(`\n${results.length - failed} of ${results.length} checks passed`);
process.exit(failed === 0 ? 0 : 1);
