#!/usr/bin/env python3
"""Phase 4 migration: rewire every web-apps/chNN/template.html to load the
shared i18n runtime + shared string tables instead of carrying its own inline
I18N dict + applyLanguage/toggleLanguage helpers.

Idempotent: running twice on the same chapter is a no-op (detected by the
presence of the shared <script src> block).

For each chapter:
  1. Parse the inline `(const|var) I18N = { defaultLang, storageKey, en: {...}, es: {...} };`
     block. Extract every (key, en_value, es_value) triple.
  2. Drop keys that already live in the shared strings files (nav, common, code,
     chapter-titles). Warn on per-chapter values that diverge from canonical;
     use the canonical anyway.
  3. Drop `header.title` — its data-i18n attribute will be rewritten to point at
     `chapter.chNN.title` (the canonical Phase-2 key).
  4. Decode unicode escapes (\\uXXXX) to direct UTF-8 — ch13 and ch17 had escapes.
  5. Write the remaining chapter-specific keys to web-apps/_shared/strings/chXX.js.
  6. In template.html:
     - Insert <script src="../_shared/..."> tags BEFORE the inline <script> that
       contains the I18N block.
     - Delete the `(const|var) I18N = {...};` block.
     - Delete the `function t(...)`, `function applyLanguage(...)`,
       `function toggleLanguage()` definitions.
     - Delete the boot try/catch block that reads localStorage and sets window.__lang.
     - Rewrite every `data-i18n="header.title"` to `data-i18n="chapter.chNN.title"`.
  7. Re-run the chapter's `build.py` to regenerate `dashboard.html` from the new
     template.

Usage: python3 scripts/migrate_to_shared_i18n.py [--dry-run] [chNN ...]

If chapter numbers are given as positional args (e.g. `ch04 ch10`), only those
chapters are migrated. Otherwise all 17 are processed.
"""

from __future__ import annotations

import codecs
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB_APPS = ROOT / "web-apps"
SHARED_DIR = WEB_APPS / "_shared"
SHARED_STRINGS_DIR = SHARED_DIR / "strings"

SHARED_FILES = ["nav.js", "common.js", "code.js", "chapter-titles.js"]

# How the new <script src> block looks. Order matters: config -> runtime -> tables.
SHARED_SCRIPT_BLOCK_TEMPLATE = """\
<!-- Shared i18n runtime + string tables (Phase 4) -->
<script src="../_shared/i18n-config.js"></script>
<script src="../_shared/i18n-runtime.js"></script>
<script src="../_shared/strings/nav.js"></script>
<script src="../_shared/strings/common.js"></script>
<script src="../_shared/strings/code.js"></script>
<script src="../_shared/strings/chapter-titles.js"></script>
<script src="../_shared/strings/{ch}.js"></script>

"""

IDEMPOTENCY_MARKER = '<script src="../_shared/i18n-runtime.js"'


# ----------------------------------------------------------------------------
# Shared key inventory (canonical values come from these files)
# ----------------------------------------------------------------------------

def load_shared_keys() -> dict[str, dict[str, str]]:
    """Return {key: {lang: value}} aggregating every entry in the 4 shared files."""
    if not SHARED_STRINGS_DIR.is_dir():
        sys.exit(f"[fatal] shared strings dir missing: {SHARED_STRINGS_DIR}")
    entry_re = re.compile(
        r'"([\w.\-]+)"\s*:\s*\{\s*((?:[a-z]{2}\s*:\s*"(?:\\.|[^"\\])*"\s*,?\s*)+)\}',
        re.DOTALL,
    )
    lang_re = re.compile(r'([a-z]{2})\s*:\s*"((?:\\.|[^"\\])*)"')
    merged: dict[str, dict[str, str]] = {}
    for name in SHARED_FILES:
        path = SHARED_STRINGS_DIR / name
        text = path.read_text(encoding="utf-8")
        for m in entry_re.finditer(text):
            key = m.group(1)
            body = m.group(2)
            langs = {lm.group(1): _json_unescape(lm.group(2)) for lm in lang_re.finditer(body)}
            merged[key] = langs
    return merged


def _json_unescape(s: str) -> str:
    """Decode JS string escapes from a JSON-like literal body. Used for canonical comparison."""
    try:
        return json.loads('"' + s + '"')
    except Exception:
        return s


# ----------------------------------------------------------------------------
# Chapter-template parsing
# ----------------------------------------------------------------------------

I18N_BLOCK_RE = re.compile(r"^(?:const|var)\s+I18N\s*=\s*\{", re.MULTILINE)


def find_balanced_block_end(text: str, start: int) -> int:
    """Given an index `start` pointing at `{`, return the index AFTER its matching `}`.

    Handles strings ("..."), single-line // comments, and nested braces. Does NOT
    handle template literals or block comments; the chapter I18N blocks do not use them.
    """
    if text[start] != "{":
        raise ValueError(f"expected `{{` at index {start}, got {text[start]!r}")
    depth = 0
    i = start
    in_str = False
    str_quote = ""
    in_line_comment = False
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
        elif in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == str_quote:
                in_str = False
        else:
            if ch == "/" and nxt == "/":
                in_line_comment = True
                i += 2
                continue
            if ch in ("'", '"', "`"):
                in_str = True
                str_quote = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return i + 1
        i += 1
    raise ValueError(f"unmatched `{{` starting at {start}")


def parse_i18n_block(text: str) -> tuple[int, int, dict[str, dict[str, str]]]:
    """Locate the chapter's `(const|var) I18N = {...};` block.

    Returns (block_start, block_end, entries) where entries = {key: {en, es}}.
    block_start is the index of the keyword (`const` or `var`).
    block_end is the index right after the closing `};`.
    """
    m = I18N_BLOCK_RE.search(text)
    if not m:
        raise ValueError("no `(const|var) I18N = {` found")
    keyword_start = m.start()
    brace_open = text.index("{", m.end() - 1)
    brace_close = find_balanced_block_end(text, brace_open)
    # Skip trailing `;` if present
    end = brace_close
    while end < len(text) and text[end] in (";", " ", "\t"):
        end += 1
    # Consume the newline that follows so we don't leave a blank slot
    if end < len(text) and text[end] == "\n":
        end += 1

    block_body = text[brace_open + 1 : brace_close - 1]
    # Find the `en: {` and `es: {` sub-blocks inside block_body
    entries: dict[str, dict[str, str]] = {}
    for lang in ("en", "es"):
        sub_m = re.search(rf"\b{lang}\s*:\s*\{{", block_body)
        if not sub_m:
            raise ValueError(f"no `{lang}: {{` in I18N block")
        sub_open = block_body.index("{", sub_m.end() - 1)
        sub_close = find_balanced_block_end(block_body, sub_open)
        sub_body = block_body[sub_open + 1 : sub_close - 1]
        for key, raw in _iter_key_value(sub_body):
            entries.setdefault(key, {})[lang] = raw
    return keyword_start, end, entries


def _iter_key_value(body: str):
    """Yield (key, raw_value) pairs from a `"key": "value", ...` body.

    Tolerates single OR double-quoted keys/values, escape sequences, trailing commas,
    and // comments between entries. Does NOT decode \\uXXXX — left as raw for later
    pass (so we can decide whether to decode in the chapter output).
    """
    i = 0
    while i < len(body):
        ch = body[i]
        if ch in (" ", "\t", "\n", "\r", ","):
            i += 1
            continue
        if ch == "/" and i + 1 < len(body) and body[i + 1] == "/":
            nl = body.find("\n", i)
            i = nl + 1 if nl != -1 else len(body)
            continue
        if ch in ("'", '"'):
            key_quote = ch
            key_start = i + 1
            j = key_start
            while j < len(body):
                if body[j] == "\\":
                    j += 2
                    continue
                if body[j] == key_quote:
                    break
                j += 1
            key = body[key_start:j]
            i = j + 1
            # Skip whitespace + `:`
            while i < len(body) and body[i] in (" ", "\t", "\n", "\r"):
                i += 1
            if i >= len(body) or body[i] != ":":
                continue
            i += 1
            while i < len(body) and body[i] in (" ", "\t", "\n", "\r"):
                i += 1
            if i >= len(body) or body[i] not in ("'", '"'):
                continue
            val_quote = body[i]
            val_start = i + 1
            j = val_start
            while j < len(body):
                if body[j] == "\\":
                    j += 2
                    continue
                if body[j] == val_quote:
                    break
                j += 1
            raw_val = body[val_start:j]
            i = j + 1
            yield key, raw_val
        else:
            i += 1


def decode_value(raw: str) -> str:
    """Decode a raw JS string literal body (without surrounding quotes) into a Python str.

    Handles \\n, \\t, \\", \\', \\\\, \\uXXXX. Treats unknown escapes (e.g. \\&) by
    keeping the literal characters.
    """
    # codecs.decode with 'unicode_escape' handles \\uXXXX and standard escapes.
    # We need to careful: it would also interpret \\xNN. JS uses \\uXXXX so this is fine.
    try:
        return codecs.decode(raw.encode("latin-1", "backslashreplace"), "unicode_escape")
    except Exception:
        return raw.replace("\\'", "'").replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")


# ----------------------------------------------------------------------------
# Helpers/boot deletion region
# ----------------------------------------------------------------------------

# The chapter's `function t`, `function applyLanguage`, `function toggleLanguage`,
# and the synchronous boot try/catch all come right after the I18N block. We delete
# from the I18N keyword through the end of the boot `} catch (e) {}` line.
BOOT_END_RE = re.compile(
    r"//\s*Read persisted language[^\n]*\n"
    r"try\s*\{\s*(?:const|var)\s+stored\s*=\s*localStorage\.getItem\(I18N\.storageKey\);\s*\n"
    r"\s*if\s*\(stored\s*===\s*\"en\"\s*\|\|\s*stored\s*===\s*\"es\"\s*\)\s*window\.__lang\s*=\s*stored;\s*\n"
    r"\}\s*catch\s*\(e\)\s*\{\s*\}\s*\n"
)


def find_deletion_range(text: str, i18n_block_start: int, i18n_block_end: int) -> tuple[int, int]:
    """Return (start, end) covering the I18N block + helpers + boot IIFE."""
    boot_match = BOOT_END_RE.search(text, i18n_block_end)
    if not boot_match:
        raise ValueError(
            "could not find boot try/catch block after I18N — chapter may use a non-standard pattern"
        )
    return i18n_block_start, boot_match.end()


# ----------------------------------------------------------------------------
# Insertion of the shared <script src> block
# ----------------------------------------------------------------------------

# We insert just BEFORE the `<script>` opening tag that contains the I18N block.
# Strategy: walk backwards from i18n_block_start until we hit `<script>\n` (no src attr).


def find_inline_script_open(text: str, i18n_block_start: int) -> int:
    """Return index of `<` for the `<script>` tag enclosing the I18N block."""
    # Look back for a <script> with no src= attribute that hasn't been closed.
    # The chapter template's inline data block is preceded by an inline <script> tag
    # without attributes. Walk back to find `<script>` (without src).
    open_re = re.compile(r"<script(?:\s+(?!src=)[^>]*)?>", re.IGNORECASE)
    close_re = re.compile(r"</script>", re.IGNORECASE)
    last_open = -1
    for m in open_re.finditer(text, 0, i18n_block_start):
        last_open = m.start()
    if last_open == -1:
        raise ValueError("no enclosing <script> tag before I18N block")
    # Ensure there's no </script> between last_open and i18n_block_start
    between = text[last_open:i18n_block_start]
    if close_re.search(between[len("<script>"):]):
        raise ValueError("found stray </script> between candidate <script> and I18N block")
    return last_open


# ----------------------------------------------------------------------------
# Emit chXX.js
# ----------------------------------------------------------------------------

CHAPTER_HEADER = """\
/* Per-chapter strings for {ch} — registered into window.I18N by i18n-runtime.js.
 * Shared keys (nav.*, common.* 3 keys, theme.*, code.*, chapter.{ch}.title) live in
 * web-apps/_shared/strings/*.js. This file holds the {ch}-specific keys only.
 * Generated by scripts/migrate_to_shared_i18n.py.
 */
"""


def emit_chapter_strings(ch: str, entries: dict[str, dict[str, str]]) -> Path:
    """Write web-apps/_shared/strings/chXX.js."""
    out_path = SHARED_STRINGS_DIR / f"{ch}.js"
    lines = [CHAPTER_HEADER.format(ch=ch).rstrip(), "window.I18N_REGISTER({"]
    for key in sorted(entries):
        en = entries[key].get("en")
        es = entries[key].get("es")
        if en is None or es is None:
            print(f"[{ch}] [WARN] key {key!r} missing language: en={en is not None}, es={es is not None}")
            continue
        en_lit = json.dumps(en, ensure_ascii=False)
        es_lit = json.dumps(es, ensure_ascii=False)
        lines.append(f'  {json.dumps(key)}: {{ en: {en_lit}, es: {es_lit} }},')
    if lines[-1].endswith(","):
        lines[-1] = lines[-1].rstrip(",")
    lines.append("});\n")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


# ----------------------------------------------------------------------------
# Main migration per chapter
# ----------------------------------------------------------------------------

REPLACEMENT_MARKER = (
    "// (i18n runtime + strings loaded above; widget IIFEs use bare t(...) which resolves to window.t)\n"
)


def migrate_chapter(ch: str, shared_keys: dict[str, dict[str, str]], dry_run: bool) -> dict:
    """Migrate web-apps/chNN/template.html. Returns a summary dict."""
    template_path = WEB_APPS / ch / "template.html"
    if not template_path.is_file():
        print(f"[{ch}] [SKIP] no template at {template_path}")
        return {"ch": ch, "status": "skip"}
    text = template_path.read_text(encoding="utf-8")

    # Idempotency
    if IDEMPOTENCY_MARKER in text:
        print(f"[{ch}] [SKIP] already migrated (found {IDEMPOTENCY_MARKER!r})")
        return {"ch": ch, "status": "already-migrated"}

    # Parse I18N
    try:
        i18n_start, i18n_end, entries = parse_i18n_block(text)
    except ValueError as e:
        print(f"[{ch}] [ERR] {e}")
        return {"ch": ch, "status": "parse-error", "error": str(e)}

    # Find deletion range (I18N + helpers + boot)
    try:
        del_start, del_end = find_deletion_range(text, i18n_start, i18n_end)
    except ValueError as e:
        print(f"[{ch}] [ERR] {e}")
        return {"ch": ch, "status": "boundary-error", "error": str(e)}

    # Find <script> open tag for inserting the shared <script src> block
    try:
        script_open = find_inline_script_open(text, i18n_start)
    except ValueError as e:
        print(f"[{ch}] [ERR] {e}")
        return {"ch": ch, "status": "insertion-error", "error": str(e)}

    # Decode values and split shared vs per-chapter
    canonical_chapter_title_key = f"chapter.{ch}.title"
    chapter_keys: dict[str, dict[str, str]] = {}
    divergences: list[str] = []
    drops: int = 0
    for key, langs in entries.items():
        decoded = {lang: decode_value(val) for lang, val in langs.items()}
        if key == "header.title":
            # Replaced by canonical chapter.chNN.title in HTML below
            drops += 1
            continue
        if key in shared_keys:
            # Verify match against canonical; warn if divergent
            canonical = shared_keys[key]
            for lang in ("en", "es"):
                if lang in canonical and lang in decoded and canonical[lang] != decoded[lang]:
                    divergences.append(
                        f"[{ch}] {key!r} ({lang}): chapter={decoded[lang]!r} vs canonical={canonical[lang]!r}"
                    )
            drops += 1
            continue
        chapter_keys[key] = decoded

    for msg in divergences:
        print(msg)

    # Write chXX.js
    if not dry_run:
        out_path = emit_chapter_strings(ch, chapter_keys)
        print(f"[{ch}] wrote {out_path.relative_to(ROOT)} ({len(chapter_keys)} keys; dropped {drops} shared)")
    else:
        print(f"[{ch}] [DRY] would write {ch}.js with {len(chapter_keys)} keys (drop {drops} shared)")

    # Patch template.html
    insert = SHARED_SCRIPT_BLOCK_TEMPLATE.format(ch=ch)
    indent = ""  # The <script> tag starts at column 0 in the template
    # Determine indentation of script_open
    line_start = text.rfind("\n", 0, script_open) + 1
    indent = text[line_start:script_open]
    indent_block = "".join((indent + line if line else "\n") for line in insert.splitlines(keepends=True))

    # Compose new text:
    # text[:script_open] + indent_block + text[script_open:del_start] + REPLACEMENT_MARKER + text[del_end:]
    indented_marker = indent + REPLACEMENT_MARKER
    new_text = (
        text[:script_open]
        + indent_block
        + text[script_open:del_start]
        + indented_marker
        + text[del_end:]
    )
    # Rewrite data-i18n="header.title" -> data-i18n="chapter.chNN.title"
    new_text = new_text.replace(
        'data-i18n="header.title"',
        f'data-i18n="{canonical_chapter_title_key}"',
    )

    if not dry_run:
        template_path.write_text(new_text, encoding="utf-8")
        print(f"[{ch}] patched {template_path.relative_to(ROOT)}")
    else:
        delta = len(new_text) - len(text)
        print(f"[{ch}] [DRY] would patch template.html (delta {delta} chars)")

    return {
        "ch": ch,
        "status": "migrated",
        "kept_keys": len(chapter_keys),
        "dropped_keys": drops,
        "divergences": len(divergences),
    }


def regen_dashboard(ch: str) -> None:
    """Run web-apps/chNN/build.py to refresh dashboard.html from template.html."""
    cwd = WEB_APPS / ch
    if not (cwd / "build.py").is_file():
        print(f"[{ch}] [WARN] no build.py — skipping regen")
        return
    res = subprocess.run([sys.executable, "build.py"], cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[{ch}] [ERR] build.py failed:\n{res.stdout}\n{res.stderr}")
    else:
        # Suppress chatty output; just confirm.
        print(f"[{ch}] dashboard.html regenerated")


def main(argv: list[str]) -> int:
    dry_run = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("--")]
    chapters = args or [f"ch{n:02d}" for n in range(1, 18)]

    print(f"Loading shared keys from {SHARED_STRINGS_DIR}…")
    shared_keys = load_shared_keys()
    print(f"  {len(shared_keys)} shared keys across {len(SHARED_FILES)} files")

    summary: list[dict] = []
    for ch in chapters:
        result = migrate_chapter(ch, shared_keys, dry_run)
        summary.append(result)

    if not dry_run:
        print("\nRegenerating dashboards…")
        for r in summary:
            if r["status"] == "migrated":
                regen_dashboard(r["ch"])

    # Summary
    print("\n=== Summary ===")
    migrated = [r for r in summary if r["status"] == "migrated"]
    skipped = [r for r in summary if r["status"] in ("skip", "already-migrated")]
    errored = [r for r in summary if r["status"] in ("parse-error", "boundary-error", "insertion-error")]
    print(f"  migrated: {len(migrated)}")
    print(f"  skipped:  {len(skipped)}")
    print(f"  errors:   {len(errored)}")
    if errored:
        for r in errored:
            print(f"    {r['ch']}: {r['status']} — {r.get('error', '')}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
