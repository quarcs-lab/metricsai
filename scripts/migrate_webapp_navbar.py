"""
One-shot rollout: inject the site navigation bar into each web-app
template.html (ch02..ch17) following the recipe verified on ch01.

Pattern recap (already documented in log/20260515_0907.md sibling):
  1. Insert Font Awesome CDN <link> after the Google Fonts <link>.
  2. Add `padding-top: 64px` to the body{} CSS rule.
  3. Inject the .site-nav* CSS block before `code, .mono {`.
  4. Insert the <nav class="site-nav"> markup + mobile drawer right after <body>.
  5. Delete the chapter header's <div class="header-controls"> block.
  6. Delete the now-orphaned .header-controls / .theme-toggle / .theme-toggle:hover CSS rules.
  7. Replace `const|var THEME_KEY = "metricsai-theme";` with the unified key.
  8. Replace the THEME TOGGLE IIFE with applyDarkMode/toggleDarkModeNav + add toggleSiteMobileMenu.
  9. Rewire applyLanguage: getElementById("languageLabel") -> ("siteLanguageLabel"),
     and remove the __themeLabelRefresh call block.
 10. Insert the 10 site-nav i18n keys into I18N.en and I18N.es (before the "common.reset" line).

The script is idempotent: re-running on a migrated chapter is a no-op.
It refuses to write if any required transformation didn't match exactly once.

Usage:
    python scripts/migrate_webapp_navbar.py              # all of ch02..ch17
    python scripts/migrate_webapp_navbar.py ch04 ch07    # only the listed chapters
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB_APPS = ROOT / "web-apps"

# ---------------------------------------------------------------------------
# Static fragments to inject (verified against ch01 output)
# ---------------------------------------------------------------------------

FA_LINK = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'

SITE_NAV_CSS = """/* ===== Site navigation bar (shared across metricsAI pages) ===== */
.site-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
  height: 64px;
}
html[data-theme="dark"] .site-nav { background: rgba(12, 16, 36, 0.85); }
.site-nav-inner { max-width: 1280px; margin: 0 auto; padding: 0 1rem; height: 100%; display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.site-nav-brand { display: flex; align-items: center; gap: 0.5rem; font-weight: 700; font-size: 1.15rem; color: var(--text); text-decoration: none; }
.site-nav-brand .ai-mark { color: var(--accent); }
.site-nav-links { display: flex; gap: 1.5rem; }
.site-nav-links a { color: var(--text-soft); text-decoration: none; font-weight: 500; font-size: 0.95rem; transition: color .2s ease; }
.site-nav-links a:hover { color: var(--accent); }
.site-nav-links a.active { color: var(--accent); border-bottom: 2px solid var(--accent); padding-bottom: 0.25rem; }
.site-nav-controls { display: flex; align-items: center; gap: 0.8rem; }
.site-nav-cameron { display: flex; flex-direction: column; align-items: center; padding: 0.25rem 0.6rem; border: 1px solid var(--border); border-radius: 0.5rem; background: var(--panel-2); text-decoration: none; line-height: 1.1; transition: background .2s ease; }
.site-nav-cameron:hover { background: var(--panel); }
.site-nav-cameron .cameron-pre { font-size: 0.6rem; color: var(--text-muted); }
.site-nav-cameron .cameron-name { font-size: 0.7rem; font-weight: 600; color: var(--text-soft); }
.site-nav-cameron .cameron-cta { font-size: 0.6rem; color: var(--text-muted); margin-top: 0.1rem; }
.site-nav-btn { background: transparent; border: none; color: var(--text-soft); cursor: pointer; padding: 0.4rem; border-radius: 0.4rem; font-size: 1.05rem; display: inline-flex; align-items: center; gap: 0.3rem; transition: color .2s ease, background .2s ease; }
.site-nav-btn:hover { color: var(--accent); background: var(--panel-2); }
.site-nav-btn .label { font-size: 0.75rem; font-weight: 600; }
.site-nav-hamburger { display: none; }

.site-nav-mobile { display: none; position: fixed; top: 64px; left: 0; right: 0; background: var(--panel); border-top: 1px solid var(--border); box-shadow: var(--shadow); z-index: 40; padding: 1rem; }
.site-nav-mobile a { display: block; padding: 0.6rem 0.4rem; color: var(--text-soft); text-decoration: none; font-weight: 500; border-bottom: 1px solid var(--border); }
.site-nav-mobile a.active { color: var(--accent); }
.site-nav-mobile a:last-of-type { border-bottom: none; }
.site-nav-mobile.open { display: block; }

@media (max-width: 768px) {
  .site-nav-links, .site-nav-cameron { display: none; }
  .site-nav-hamburger { display: inline-flex; }
}
/* ===== /Site navigation bar ===== */
"""

SITE_NAV_HTML = """<nav class="site-nav" aria-label="Site navigation">
  <div class="site-nav-inner">
    <a href="../../index.html" class="site-nav-brand">
      <i class="fa-solid fa-chart-line" style="color: var(--accent);"></i>
      <span>metrics<span class="ai-mark">AI</span></span>
    </a>
    <div class="site-nav-links">
      <a href="../../index.html#about" data-i18n="nav.about">About</a>
      <a href="../../index.html#curriculum" class="active" data-i18n="nav.notebooks">Python Notebooks</a>
      <a href="../../tutors.html" data-i18n="nav.tutors">AI Tutors</a>
      <a href="../../index.html#books" data-i18n="nav.books">Books</a>
      <a href="../../videos.html" data-i18n="nav.videos">Videos</a>
      <a href="https://open.spotify.com/show/2lN5pA3l10UdHe61ZCoHcF?si=IFFMpG3pROepG61o8qbnvg" target="_blank" rel="noopener" data-i18n="nav.podcasts">Podcasts</a>
      <a href="../../index.html#authors" data-i18n="nav.authors">Authors</a>
      <a href="../../index.html#more-resources" data-i18n="nav.resources">More Resources</a>
    </div>
    <div class="site-nav-controls">
      <a href="https://cameron.econ.ucdavis.edu/aed/index.html" target="_blank" rel="noopener" class="site-nav-cameron">
        <span class="cameron-pre" data-i18n="nav.cameron.pre">Content based on</span>
        <span class="cameron-name">Cameron (2022)</span>
        <span class="cameron-cta"><span data-i18n="nav.cameron.cta">Learn More</span> <i class="fa-solid fa-external-link-alt"></i></span>
      </a>
      <button type="button" class="site-nav-btn" onclick="toggleDarkModeNav()" title="Toggle dark mode" id="siteDarkModeToggle">
        <i class="fa-solid fa-moon" id="siteDarkModeIcon"></i>
      </button>
      <button type="button" class="site-nav-btn" onclick="toggleLanguage()" title="Switch language / Cambiar idioma" id="siteLanguageToggle">
        <i class="fa-solid fa-language"></i>
        <span class="label" id="siteLanguageLabel">EN</span>
      </button>
      <button type="button" class="site-nav-btn site-nav-hamburger" onclick="toggleSiteMobileMenu()" id="siteMobileMenuBtn">
        <i class="fa-solid fa-bars" id="siteHamburgerIcon"></i>
        <i class="fa-solid fa-times" id="siteCloseIcon" style="display:none"></i>
      </button>
    </div>
  </div>
</nav>
<div class="site-nav-mobile" id="siteMobileMenu">
  <a href="../../index.html#about" data-i18n="nav.about">About</a>
  <a href="../../index.html#curriculum" class="active" data-i18n="nav.notebooks">Python Notebooks</a>
  <a href="../../tutors.html" data-i18n="nav.tutors">AI Tutors</a>
  <a href="../../index.html#books" data-i18n="nav.books">Books</a>
  <a href="../../videos.html" data-i18n="nav.videos">Videos</a>
  <a href="https://open.spotify.com/show/2lN5pA3l10UdHe61ZCoHcF?si=IFFMpG3pROepG61o8qbnvg" target="_blank" rel="noopener" data-i18n="nav.podcasts">Podcasts</a>
  <a href="../../index.html#authors" data-i18n="nav.authors">Authors</a>
  <a href="../../index.html#more-resources" data-i18n="nav.resources">More Resources</a>
</div>
"""

NEW_THEME_BLOCK = """// ==================== THEME TOGGLE (site navbar) ====================
// Reads/writes localStorage.darkMode (shared with index.html / tutors.html)
// and applies html[data-theme="dark"] for this chapter's CSS.
function applyDarkMode(isDark) {
  document.documentElement.dataset.theme = isDark ? "dark" : "light";
  const icon = document.getElementById("siteDarkModeIcon");
  if (icon) icon.className = isDark ? "fa-solid fa-sun" : "fa-solid fa-moon";
  // Re-render all widgets so Plotly picks up the new CSS colors.
  for (const key in window) {
    if (key.startsWith("__rerender_") && typeof window[key] === "function") window[key]();
  }
}

function toggleDarkModeNav() {
  const isDark = document.documentElement.dataset.theme !== "dark";
  localStorage.setItem(THEME_KEY, isDark ? "dark" : "light");
  applyDarkMode(isDark);
}

(function() {
  const saved = localStorage.getItem(THEME_KEY);
  const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  const isDark = saved ? (saved === "dark") : prefersDark;
  applyDarkMode(isDark);
})();

// ==================== MOBILE MENU (site navbar) ====================
function toggleSiteMobileMenu() {
  const menu = document.getElementById("siteMobileMenu");
  const hamburger = document.getElementById("siteHamburgerIcon");
  const close = document.getElementById("siteCloseIcon");
  if (!menu || !hamburger || !close) return;
  const isOpen = menu.classList.toggle("open");
  hamburger.style.display = isOpen ? "none" : "";
  close.style.display = isOpen ? "" : "none";
}"""

I18N_EN_KEYS = """    // Site navigation (shared with index.html / tutors.html)
    "nav.about":        "About",
    "nav.notebooks":    "Python Notebooks",
    "nav.tutors":       "AI Tutors",
    "nav.books":        "Books",
    "nav.videos":       "Videos",
    "nav.podcasts":     "Podcasts",
    "nav.authors":      "Authors",
    "nav.resources":    "More Resources",
    "nav.cameron.pre":  "Content based on",
    "nav.cameron.cta":  "Learn More",

"""

I18N_ES_KEYS = """    // Site navigation (shared with index.html / tutors.html)
    "nav.about":        "Acerca de",
    "nav.notebooks":    "Cuadernos de Python",
    "nav.tutors":       "Tutores IA",
    "nav.books":        "Libros",
    "nav.videos":       "Videos",
    "nav.podcasts":     "Podcasts",
    "nav.authors":      "Autores",
    "nav.resources":    "Más recursos",
    "nav.cameron.pre":  "Contenido basado en",
    "nav.cameron.cta":  "Saber más",

"""

# ---------------------------------------------------------------------------
# Migration step helpers — each returns (new_text, did_change).
# Each raises AssertionError if a REQUIRED match is missing.
# ---------------------------------------------------------------------------

def insert_fa_link(s: str) -> str:
    if FA_LINK in s:
        return s
    # Match the Google Fonts <link href="..."> line, insert FA link right after.
    pat = re.compile(r'(<link href="https://fonts\.googleapis\.com/css2[^"]*"[^>]*>)')
    new, n = pat.subn(r'\1\n' + FA_LINK, s, count=1)
    assert n == 1, "could not find Google Fonts <link> to anchor FA CDN insert"
    return new

def add_body_padding(s: str) -> str:
    if 'padding-top: 64px' in s:
        return s
    # Inject padding-top at the END of the body{} block. Tolerant of pretty &
    # minified forms (with or without a trailing `;` before the closing `}`)
    # and of multi-rule single lines (the [^}]*? prevents crossing into other
    # rules; the engine backtracks past `body{` matches whose body lacks the
    # `transition:` marker until it finds the right one).
    pat = re.compile(
        r'(body\s*\{[^}]*?transition:\s*background-color\s*\.25s\s*ease,\s*color\s*\.25s\s*ease[^}]*?)(\})',
        re.DOTALL,
    )
    new, n = pat.subn(
        r'\1; padding-top: 64px; /* leave room for the fixed .site-nav */ \2',
        s, count=1,
    )
    assert n == 1, "could not find body{} rule with the canonical transition declaration"
    return new

def insert_site_nav_css(s: str) -> str:
    if '.site-nav {' in s:
        return s
    # Anchor on `code, .mono { font-family: ... }` — appears in every chapter
    pat = re.compile(r"(code,\s*\.mono\s*\{[^}]*\})", re.DOTALL)
    new, n = pat.subn(SITE_NAV_CSS + r"\n\1", s, count=1)
    assert n == 1, "could not find `code, .mono { ... }` anchor for site-nav CSS"
    return new

def insert_navbar_html(s: str) -> str:
    if '<nav class="site-nav"' in s:
        return s
    pat = re.compile(r'(<body>\s*\n)')
    new, n = pat.subn(r'\1\n' + SITE_NAV_HTML + '\n', s, count=1)
    assert n == 1, "could not find `<body>` to anchor navbar HTML"
    return new

def remove_header_controls_html(s: str) -> str:
    # Removes <div class="header-controls"> ... </div>. Tolerant of multi-line and minified.
    pat = re.compile(r'\s*<div class="header-controls">.*?</div>', re.DOTALL)
    return pat.sub('', s, count=1)

def remove_orphan_css_rules(s: str) -> str:
    # `.header-controls`, `.theme-toggle`, `.theme-toggle:hover` — each a single-rule selector.
    # Use negative-lookahead on the selector to avoid eating later rules.
    for selector in (r'\.header-controls', r'\.theme-toggle:hover', r'\.theme-toggle'):
        pat = re.compile(rf'{selector}\s*\{{[^}}]*\}}\s*', re.DOTALL)
        s = pat.sub('', s)
    return s

def replace_theme_key(s: str) -> str:
    if '"darkMode"' in s:
        return s
    pat = re.compile(r'(?:const|var)\s+THEME_KEY\s*=\s*"metricsai-theme"\s*;')
    new, n = pat.subn(
        'const THEME_KEY = "darkMode"; // unified with index.html / tutors.html',
        s, count=1,
    )
    assert n == 1, "could not find `THEME_KEY = \"metricsai-theme\"` to rename"
    return new

def replace_theme_iife(s: str) -> str:
    if 'function applyDarkMode' in s:
        return s
    # From `// ==== THEME(.* TOGGLE)? ====` comment to the IIFE's closing `})();`.
    # Use lazy matching so we stop at the FIRST closing of the theme IIFE.
    pat = re.compile(
        r'// =+\s*THEME(?: TOGGLE)?\s*=+\s*\n'
        r'\(function\s*\(\s*\)\s*\{.*?\}\)\(\s*\)\s*;',
        re.DOTALL,
    )
    new, n = pat.subn(NEW_THEME_BLOCK, s, count=1)
    assert n == 1, "could not match THEME TOGGLE IIFE block"
    return new

def rewire_language_label(s: str) -> str:
    return s.replace('getElementById("languageLabel")',
                     'getElementById("siteLanguageLabel")')

def remove_theme_label_refresh(s: str) -> str:
    # Match the optional comment line + the if(...){...} block.
    # Tolerant of pretty and minified forms.
    pat = re.compile(
        r'\s*(?://\s*Refresh\s*theme\s*button\s*label[^\n]*\n)?'
        r'\s*if\s*\(\s*typeof\s+window\.__themeLabelRefresh\s*===\s*"function"\s*\)\s*'
        r'\{\s*try\s*\{\s*window\.__themeLabelRefresh\(\)\s*;?\s*\}\s*catch\s*\([^)]*\)\s*\{\s*\}\s*\}',
        re.DOTALL,
    )
    return pat.sub('', s)

def insert_i18n_keys(s: str) -> str:
    if '"nav.about"' in s:
        return s
    # Find the two "common.reset" dictionary entries (EN first, ES second).
    pat = re.compile(r'^[ \t]*"common\.reset":', re.MULTILINE)
    positions = [m.start() for m in pat.finditer(s)]
    assert len(positions) >= 2, (
        f"expected >=2 dictionary 'common.reset' entries (EN+ES), found {len(positions)}"
    )
    # Insert from end to start so earlier offsets remain valid.
    es_pos = positions[-1]
    en_pos = positions[0]
    s = s[:es_pos] + I18N_ES_KEYS + s[es_pos:]
    s = s[:en_pos] + I18N_EN_KEYS + s[en_pos:]
    return s

# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

STEPS = [
    ("FA link",               insert_fa_link),
    ("body padding",          add_body_padding),
    ("site-nav CSS",          insert_site_nav_css),
    ("navbar HTML",           insert_navbar_html),
    ("header-controls HTML",  remove_header_controls_html),
    ("orphan CSS rules",      remove_orphan_css_rules),
    ("THEME_KEY rename",      replace_theme_key),
    ("THEME IIFE replace",    replace_theme_iife),
    ("languageLabel rewire",  rewire_language_label),
    ("__themeLabelRefresh",   remove_theme_label_refresh),
    ("i18n keys",             insert_i18n_keys),
]

def migrate(chapter_dir: Path) -> bool:
    tpl = chapter_dir / "template.html"
    if not tpl.exists():
        print(f"[skip] {chapter_dir.name}: no template.html")
        return False
    src = tpl.read_text()
    out = src
    for name, fn in STEPS:
        try:
            out = fn(out)
        except AssertionError as e:
            print(f"[FAIL] {chapter_dir.name} @ {name}: {e}")
            return False
    if out == src:
        print(f"[no-op] {chapter_dir.name} (already migrated)")
        return True
    tpl.write_text(out)
    print(f"[ok]   {chapter_dir.name}: template.html migrated")
    return True

def main():
    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    else:
        targets = [f"ch{n:02d}" for n in range(2, 18)]
    failed = []
    for ch in targets:
        ok = migrate(WEB_APPS / ch)
        if not ok:
            failed.append(ch)
    if failed:
        print(f"\n{len(failed)} chapter(s) failed: {failed}")
        sys.exit(1)
    print(f"\nAll {len(targets)} chapter(s) processed successfully.")

if __name__ == "__main__":
    main()
