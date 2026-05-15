#!/usr/bin/env python3
"""Validate the metricsAI shared i18n setup.

Checks performed across web-apps/_shared/strings/*.js + the HTML pages that consume them:

  1. Parse every I18N_REGISTER({...}) block. Build a {key: {lang: value}} map.
  2. For every key, verify it has a value for every language in I18N_CONFIG.languages.
  3. Detect duplicate key definitions across files (last-write-wins is silent — flag it).
  4. Walk every HTML page that references the i18n runtime; collect every data-i18n="..."
     attribute and every t("...") call in inline <script>. Verify each referenced key has
     a definition. Verify every defined key is referenced somewhere.
  5. Print a per-file report. Exit 0 if everything is clean, 1 otherwise.

Usage: python3 scripts/i18n_check.py
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "web-apps" / "_shared"
STRINGS_DIR = SHARED / "strings"
CONFIG_FILE = SHARED / "i18n-config.js"


def read_languages() -> list[str]:
    """Parse the languages array out of i18n-config.js."""
    text = CONFIG_FILE.read_text(encoding="utf-8")
    m = re.search(r"languages\s*:\s*\[([^\]]+)\]", text)
    if not m:
        sys.exit(f"[fatal] could not find `languages: [...]` in {CONFIG_FILE}")
    return [s.strip().strip('"').strip("'") for s in m.group(1).split(",") if s.strip()]


def parse_strings_file(path: Path) -> dict[str, dict[str, str]]:
    """Parse I18N_REGISTER({...}) calls and return {key: {lang: value}}.

    Format expected (one or more REGISTER blocks per file):
      window.I18N_REGISTER({
        "key.name": { en: "...", es: "...", ja: "..." },
        ...
      });

    Tolerates trailing commas, single OR double-quoted lang keys, multi-line strings via
    string concatenation are NOT supported (one literal per language slot).
    """
    text = path.read_text(encoding="utf-8")
    # Find every "key": { ... } entry. Allow keys with dots, dashes, underscores.
    # Match { en: "...", es: "..." } — values are double-quoted with escaped quotes.
    entry_re = re.compile(
        r'"([\w.\-]+)"\s*:\s*\{\s*((?:[a-z]{2}\s*:\s*"(?:\\.|[^"\\])*"\s*,?\s*)+)\}',
        re.DOTALL,
    )
    lang_re = re.compile(r'([a-z]{2})\s*:\s*"((?:\\.|[^"\\])*)"')
    entries: dict[str, dict[str, str]] = {}
    for m in entry_re.finditer(text):
        key = m.group(1)
        body = m.group(2)
        langs = {lm.group(1): lm.group(2) for lm in lang_re.finditer(body)}
        entries[key] = langs
    return entries


def collect_all_strings() -> tuple[dict[str, dict[str, str]], dict[str, list[Path]]]:
    """Walk strings/*.js and aggregate. Returns (merged_strings, key_to_files)."""
    if not STRINGS_DIR.is_dir():
        sys.exit(f"[fatal] strings dir missing: {STRINGS_DIR}")
    merged: dict[str, dict[str, str]] = {}
    key_to_files: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(STRINGS_DIR.glob("*.js")):
        entries = parse_strings_file(path)
        for k, v in entries.items():
            key_to_files[k].append(path)
            if k in merged:
                # Last write wins, but flag.
                merged[k] = v
            else:
                merged[k] = v
    return merged, key_to_files


def collect_html_references() -> dict[Path, set[str]]:
    """Walk every HTML page that loads i18n-runtime.js. Collect all data-i18n="..." attributes
    and all t("...") calls. Returns {path: {keys}}.
    """
    pages: dict[Path, set[str]] = {}
    candidates: list[Path] = []
    for p in [ROOT / "index.html", ROOT / "tutors.html"]:
        if p.exists():
            candidates.append(p)
    for p in (ROOT / "web-apps").glob("ch*/dashboard.html"):
        candidates.append(p)
    attr_re = re.compile(r'data-i18n\s*=\s*"([\w.\-]+)"')
    call_re = re.compile(r'\bt\(\s*"([\w.\-]+)"')
    for path in candidates:
        text = path.read_text(encoding="utf-8")
        if "i18n-runtime.js" not in text:
            continue  # Page hasn't been migrated yet; ignore for now.
        keys = set(attr_re.findall(text)) | set(call_re.findall(text))
        pages[path] = keys
    return pages


def main() -> int:
    languages = read_languages()
    print(f"[i18n-check] languages: {languages}")

    merged, key_to_files = collect_all_strings()
    print(f"[i18n-check] {len(merged)} keys defined across {len(list(STRINGS_DIR.glob('*.js')))} string file(s)")

    issues = 0

    # Check 1: every key has every language.
    missing_lang: list[str] = []
    for key, langs_map in sorted(merged.items()):
        for lang in languages:
            if lang not in langs_map:
                missing_lang.append(f"  {key}: missing `{lang}` (defined in {[p.name for p in key_to_files[key]]})")
    if missing_lang:
        print(f"\n[FAIL] {len(missing_lang)} keys missing a language value:")
        for line in missing_lang[:50]:
            print(line)
        if len(missing_lang) > 50:
            print(f"  ... and {len(missing_lang) - 50} more")
        issues += len(missing_lang)
    else:
        print(f"[ok] every key has all {len(languages)} language values")

    # Check 2: duplicate definitions.
    dupes = {k: paths for k, paths in key_to_files.items() if len(paths) > 1}
    if dupes:
        print(f"\n[FAIL] {len(dupes)} keys defined in more than one file:")
        for k, paths in sorted(dupes.items())[:30]:
            print(f"  {k} → {[p.name for p in paths]}")
        issues += len(dupes)
    else:
        print("[ok] no duplicate key definitions across string files")

    # Check 3: HTML references.
    pages = collect_html_references()
    if not pages:
        print("\n[warn] no HTML pages found that reference i18n-runtime.js — skipping HTML cross-check")
        print("       (this is expected before any page has been migrated)")
    else:
        print(f"\n[i18n-check] {len(pages)} migrated HTML page(s)")
        all_referenced: set[str] = set()
        for keys in pages.values():
            all_referenced |= keys
        # Keys referenced but not defined.
        undefined = sorted(all_referenced - set(merged.keys()))
        if undefined:
            print(f"\n[FAIL] {len(undefined)} keys referenced in HTML/JS but not defined:")
            for k in undefined[:30]:
                hosts = [p.relative_to(ROOT).as_posix() for p, ks in pages.items() if k in ks]
                print(f"  {k}  (referenced in: {hosts[:3]}{'...' if len(hosts) > 3 else ''})")
            if len(undefined) > 30:
                print(f"  ... and {len(undefined) - 30} more")
            issues += len(undefined)
        else:
            print("[ok] every referenced key has a definition")
        # Keys defined but not referenced.
        orphan = sorted(set(merged.keys()) - all_referenced)
        if orphan:
            print(f"\n[warn] {len(orphan)} keys defined but never referenced (orphaned, not a hard fail):")
            for k in orphan[:20]:
                print(f"  {k}  (defined in: {[p.name for p in key_to_files[k]]})")
            if len(orphan) > 20:
                print(f"  ... and {len(orphan) - 20} more")
        else:
            print("[ok] every defined key is referenced")

    print()
    if issues == 0:
        print("[i18n-check] ALL CLEAN ✓")
        return 0
    print(f"[i18n-check] {issues} issue(s) — fix before shipping")
    return 1


if __name__ == "__main__":
    sys.exit(main())
