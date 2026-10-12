#!/usr/bin/env python3
"""export_chapter_figures.py — stage a chapter's rendered figures for a slide deck.

metricsAI chapter plots are produced by executed matplotlib (`plt.show()`) at Quarto
render time — there are no pre-saved PNGs with stable names. This helper collects the
figures Quarto already emits to `<chapter>_files/figure-html/cell-*-output-*.png`, maps
each to the section heading it appears under, and copies them (plus the chapter's
visual-summary image) into the deck's `_figcache/` staging dir with ordered, meaningful
names and a manifest.

The write-slides skill then reads `figures_manifest.json`, picks the single load-bearing
figure per core section (an "essentials" deck), and copies the chosen ones into
`slides/chNN/figures/`. The deck itself never executes code — it references the copied
PNGs by relative path, so `quarto render slides.qmd` is a pure Pandoc render.

Figure source (in order of preference, `--source auto` default):
  1. The book-rendered HTML at book/_book/notebooks_quarto/<base>.html, if present and
     newer than the chapter .qmd (reuse — no execution needed).
  2. Otherwise render the chapter fresh: `quarto render <qmd> --to html` (executes the
     chapter; output + _files land next to the .qmd and are gitignored).

Usage:
  python3 .claude/skills/write-slides/scripts/export_chapter_figures.py ch05
  python3 .../export_chapter_figures.py ch05 --source render   # force a fresh render
  python3 .../export_chapter_figures.py ch05 --out slides/ch05/_figcache

Output:
  <out>/fig_<section>_<nn>.png        one per chapter figure, document order
  <out>/visual_summary.png            the chapter's visual-summary image (if found)
  <out>/figures_manifest.json         [{index, cache_file, src, section, heading}, ...]
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]   # scripts → write-slides → skills → .claude → root
QUARTO = "/Users/carlosmendez/opt/bin/quarto"

# A heading (any level) OR a figure <img> whose src points into a figure-html dir.
TOKEN_RE = re.compile(
    r'<h([1-6])[^>]*>(.*?)</h\1>'
    r'|<img\b[^>]*?\bsrc="([^"]*figure-html/[^"]*\.png)"',
    re.DOTALL | re.IGNORECASE,
)
TAG_RE = re.compile(r"<[^>]+>")
SEC_RE = re.compile(r"^(\d+(?:\.\d+)*)")


def resolve_chapter_qmd(chid: str) -> Path:
    matches = sorted((PROJECT_ROOT / "notebooks_quarto").glob(f"{chid}_*.qmd"))
    if not matches:
        sys.exit(f"[export] No chapter .qmd found for '{chid}' in notebooks_quarto/")
    return matches[0]


def pick_source_html(qmd: Path, source: str) -> Path:
    """Return the rendered chapter HTML whose sibling *_files/figure-html/ holds the PNGs."""
    base = qmd.stem
    book_html = PROJECT_ROOT / "book" / "_book" / "notebooks_quarto" / f"{base}.html"
    local_html = qmd.with_suffix(".html")

    def has_figures(h: Path) -> bool:
        base_name = h.stem  # strip .html
        return h.exists() and (h.parent / f"{base_name}_files" / "figure-html").is_dir()

    if source == "book":
        if not book_html.exists():
            sys.exit(f"[export] --source book but {book_html} is missing. Render the book first.")
        return book_html
    if source == "auto" and has_figures(book_html):
        stale = book_html.stat().st_mtime < qmd.stat().st_mtime
        note = "  (NOTE: chapter .qmd is newer — pass --source render to refresh plots)" if stale else ""
        print(f"[export] Using book-rendered HTML: {book_html.relative_to(PROJECT_ROOT)}{note}")
        return book_html
    if source == "auto" and has_figures(local_html):
        print(f"[export] Using local rendered HTML: {local_html.relative_to(PROJECT_ROOT)}")
        return local_html

    # Render fresh (source == "render", or no rendered output with figures under "auto").
    print(f"[export] Rendering chapter fresh: {QUARTO} render {qmd.name} --to html")
    try:
        subprocess.run([QUARTO, "render", str(qmd), "--to", "html"],
                       cwd=qmd.parent, check=True)
    except FileNotFoundError:
        sys.exit(f"[export] quarto not found at {QUARTO}")
    except subprocess.CalledProcessError as e:
        sys.exit(f"[export] quarto render failed (exit {e.returncode}). "
                 f"Activate .venv so the Python kernel is available, or use --source book.")
    if not local_html.exists():
        sys.exit(f"[export] Render produced no HTML at {local_html}")
    return local_html


def clean_heading(raw: str) -> str:
    return re.sub(r"\s+", " ", TAG_RE.sub("", raw)).strip()


def parse_figures(html: str):
    """Walk the HTML in document order, tagging each figure with its current heading."""
    current = "intro"
    figs = []
    for m in TOKEN_RE.finditer(html):
        if m.group(2) is not None:               # a heading
            heading = clean_heading(m.group(2))
            if heading and heading.lower() != "table of contents":
                current = heading
        elif m.group(3) is not None:             # a figure img
            figs.append({"src": m.group(3), "heading": current})
    return figs


def section_token(heading: str) -> str:
    sm = SEC_RE.match(heading)
    return sm.group(1).replace(".", "-") if sm else "x"


def copy_visual_summary(chid: str, out: Path):
    candidates = sorted((PROJECT_ROOT / "images").glob(f"{chid}_visual_summary*.png"))
    if not candidates:
        print(f"[export] WARNING: no visual summary found (images/{chid}_visual_summary*.png)")
        return None
    chosen = candidates[-1]   # highest version suffix (…_v2 > …_v1 > base) by lexical sort
    dest = out / "visual_summary.png"
    shutil.copy2(chosen, dest)
    print(f"[export] Visual summary: {chosen.name} → {dest.name}")
    return chosen.name


def main():
    ap = argparse.ArgumentParser(description="Stage a chapter's figures for a slide deck.")
    ap.add_argument("chapter", help="chapter id, e.g. ch05")
    ap.add_argument("--out", help="staging dir (default: slides/<chid>/_figcache)")
    ap.add_argument("--source", choices=["auto", "book", "render"], default="auto",
                    help="where figures come from (default: auto)")
    args = ap.parse_args()

    chid = args.chapter
    qmd = resolve_chapter_qmd(chid)
    out = Path(args.out).resolve() if args.out else (PROJECT_ROOT / "slides" / chid / "_figcache")
    out.mkdir(parents=True, exist_ok=True)

    html_path = pick_source_html(qmd, args.source)
    files_dir = html_path.parent
    html = html_path.read_text(encoding="utf-8")

    figs = parse_figures(html)
    manifest = []
    per_section = {}
    for i, fig in enumerate(figs):
        src_png = (files_dir / fig["src"]).resolve()
        if not src_png.exists():
            print(f"[export] WARNING: figure missing on disk, skipping: {fig['src']}")
            continue
        sec = section_token(fig["heading"])
        per_section[sec] = per_section.get(sec, 0) + 1
        cache_file = f"fig_{sec}_{per_section[sec]:02d}.png"
        shutil.copy2(src_png, out / cache_file)
        manifest.append({
            "index": i,
            "cache_file": cache_file,
            "src": fig["src"],
            "section": sec,
            "heading": fig["heading"],
        })

    visual = copy_visual_summary(chid, out)

    manifest_path = out / "figures_manifest.json"
    manifest_path.write_text(json.dumps({
        "chapter": chid,
        "source_html": str(html_path.relative_to(PROJECT_ROOT)),
        "visual_summary": visual,
        "figures": manifest,
    }, indent=2), encoding="utf-8")

    print(f"[export] {len(manifest)} figure(s) staged → {out.relative_to(PROJECT_ROOT)}")
    for f in manifest:
        print(f"         {f['cache_file']:20s}  §{f['section']:5s}  {f['heading']}")
    print(f"[export] Manifest: {manifest_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
