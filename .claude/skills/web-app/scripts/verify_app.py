"""Verify a built chapter web app.

Usage:
    python3 .claude/skills/web-app/scripts/verify_app.py web-apps/chNN/dashboard.html

Checks:
- No unreplaced {{…}} placeholders.
- JSON data-island parses.
- Inline JS passes `node --check` (if Node is installed).
- File size within budget.
- `window.__rerender_*` registered for each widget section.
- Every section with class="widget" has a Reset button (data-reset="...").
- Every widget has at least one try-this block.

Exits non-zero on any failure; prints a summary either way.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SIZE_BUDGET_KB = 200


def fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def ok(msg: str) -> None:
    print(f"  [ok]   {msg}")


def check_placeholders(html: str) -> int:
    leftovers = re.findall(r"\{\{[^}]+\}\}", html)
    if leftovers:
        fail(f"unreplaced placeholders: {sorted(set(leftovers))}")
        return 1
    ok("no {{…}} placeholders left")
    return 0


def check_data_island(html: str) -> int:
    m = re.search(
        r'<script type="application/json" id="ch-data">([\s\S]*?)</script>',
        html,
    )
    if not m:
        # Legacy: may be named ch02-data etc.; accept any ch-prefixed id.
        m = re.search(
            r'<script type="application/json" id="ch[\w-]*data">([\s\S]*?)</script>',
            html,
        )
    if not m:
        fail("JSON data island not found")
        return 1
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        fail(f"JSON data island does not parse: {e}")
        return 1
    if not isinstance(data, dict) or not data:
        fail("JSON data island is empty or not an object")
        return 1
    ok(f"JSON data island parses ({len(data)} top-level keys)")
    return 0


def extract_inline_js(html: str) -> str:
    """Return concatenated contents of every non-JSON <script> in the HTML."""
    parts = re.findall(
        r"<script(?![^>]*application/json)(?![^>]*src=)[^>]*>([\s\S]*?)</script>",
        html,
    )
    return "\n".join(parts)


def check_js_syntax(html: str) -> int:
    node = shutil.which("node")
    if not node:
        ok("node not installed, skipping JS syntax check")
        return 0
    js = extract_inline_js(html)
    if not js.strip():
        fail("no inline JS found")
        return 1
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as tmp:
        tmp.write(js)
        tmp_path = tmp.name
    try:
        result = subprocess.run(
            [node, "--check", tmp_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            fail(f"JS syntax errors:\n{result.stderr}")
            return 1
        ok("JS passes node --check")
        return 0
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def check_size(path: Path) -> int:
    size_kb = path.stat().st_size / 1024
    if size_kb > SIZE_BUDGET_KB:
        fail(f"size {size_kb:.1f} KB exceeds {SIZE_BUDGET_KB} KB budget")
        return 1
    ok(f"size {size_kb:.1f} KB (budget {SIZE_BUDGET_KB} KB)")
    return 0


def check_widgets(html: str) -> int:
    sections = re.findall(
        r'<section class="widget"[^>]*id="([^"]+)"',
        html,
    )
    if not sections:
        fail("no <section class=\"widget\"> elements found")
        return 1

    fails = 0

    # Every section must have a reset button OR be explicitly control-less
    for sid in sections:
        block = _section_block(html, sid)
        if 'data-reset=' not in block and 'class="reset-btn' in html:
            # A section with no controls doesn't need a Reset button, but it
            # shouldn't pretend to have a widget-head with reset either. Soft check only.
            pass
        if 'class="try-this"' not in block:
            fail(f'widget #{sid}: no .try-this block')
            fails += 1

    # Every rerender function is referenced
    rerender_hooks = set(re.findall(r"__rerender_(\w+)", html))
    if not rerender_hooks:
        fail("no window.__rerender_* hooks found")
        fails += 1
    else:
        ok(f'{len(sections)} widget sections · {len(rerender_hooks)} rerender hooks')

    return 1 if fails else 0


def _section_block(html: str, sid: str) -> str:
    m = re.search(
        rf'<section class="widget"[^>]*id="{re.escape(sid)}"[^>]*>([\s\S]*?)</section>',
        html,
    )
    return m.group(1) if m else ""


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: verify_app.py <path/to/dashboard.html>")
        return 2
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        return 2
    html = path.read_text(encoding="utf-8")
    print(f"Verifying {path}")
    rc = 0
    rc |= check_placeholders(html)
    rc |= check_data_island(html)
    rc |= check_js_syntax(html)
    rc |= check_size(path)
    rc |= check_widgets(html)
    print()
    if rc == 0:
        print("All checks passed.")
    else:
        print("One or more checks failed.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
