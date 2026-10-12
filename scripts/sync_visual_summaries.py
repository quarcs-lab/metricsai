#!/usr/bin/env python3
"""Synchronize image-only changes without reexecuting chapter computations.

The image manifest selects the published versions. Quarto source files, existing
exports, and frozen/rendered book output receive the same filename substitution.
All other bytes, including notebook outputs and frozen computations, are retained.
Run with --write to synchronize, or without arguments to verify publication.
"""

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "images/visual_summaries.json"
ACTIVE_ROOTS = {"notebooks_quarto", "notebooks_colab", "notebooks_md"}
PATTERN = re.compile(r"(ch\d{2})_visual_summary(?:_v\d+)?\.(?:jpg|png)")


def active_files():
    paths = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT
    ).decode().split("\0")
    for name in paths:
        p = Path(name)
        if (name == "index.html" or (p.parts and p.parts[0] in ACTIVE_ROOTS)
                or name.startswith(("book/_book/", "book/_freeze/"))):
            if p.suffix in {".html", ".qmd", ".md", ".ipynb", ".json"}:
                yield ROOT / p


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    assert set(manifest) == {f"ch{i:02d}" for i in range(1, 18)}
    for filename in manifest.values():
        asset = ROOT / "images" / filename
        assert asset.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), asset
    changed = []
    references = 0
    for path in active_files():
        original = path.read_bytes()
        text = original.decode("utf-8")
        expected = PATTERN.sub(lambda m: manifest.get(m[1], m[0]), text)
        references += len(PATTERN.findall(text))
        if expected != text:
            changed.append(str(path.relative_to(ROOT)))
            if args.write:
                path.write_bytes(expected.encode("utf-8"))
    if changed and not args.write:
        raise SystemExit("Stale summaries in: " + ", ".join(changed))
    if args.write:
        print(f"Synchronized {len(changed)} files; preserved all non-image content.")
    for chapter, filename in manifest.items():
        for directory, extension in [("notebooks_quarto", "qmd"),
                                     ("notebooks_colab", "ipynb"),
                                     ("notebooks_md", "md"),
                                     ("book/_book/notebooks_quarto", "html")]:
            matches = list((ROOT / directory).glob(f"{chapter}_*.{extension}"))
            assert len(matches) == 1, (chapter, directory, matches)
            assert filename in matches[0].read_text(), matches[0]
        assert filename in (ROOT / "index.html").read_text()
        assert filename in (ROOT / "notebooks_md/metricsAI_complete_book.md").read_text()
    print(f"PASS: 17 chapter assets and {references} active image references agree.")


if __name__ == "__main__":
    main()
