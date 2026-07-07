#!/usr/bin/env python3
"""Strict batch-edit applier for the audit campaign.

Usage: python3 apply_edits.py <target-file> <edits.json> [--dry-run]

edits.json: [{"finding_id": "ch05-F01", "old": "...", "new": "...",
              "count": 1}, ...]

Semantics: each edit's `old` must occur EXACTLY `count` times (default 1) in
the current working text (edits applied sequentially, in list order). Any
mismatch aborts the entire run and writes NOTHING. On success the file is
rewritten once — deliberately via this script (not the Edit/Write tools) so
the .qmd sync hook does not fire per edit.
"""
import json
import sys


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry = "--dry-run" in sys.argv
    if len(args) != 2:
        sys.exit("usage: apply_edits.py <target-file> <edits.json> [--dry-run]")
    target, edits_path = args

    with open(target, encoding="utf-8") as f:
        text = f.read()
    with open(edits_path, encoding="utf-8") as f:
        edits = json.load(f)

    errors = []
    for i, e in enumerate(edits):
        fid = e.get("finding_id", f"edit-{i}")
        old, new = e["old"], e["new"]
        expected = e.get("count", 1)
        found = text.count(old)
        if found != expected:
            errors.append(f"  {fid}: expected {expected} match(es), found {found}"
                          f" | old[:80]={old[:80]!r}")
            continue
        if old == new:
            errors.append(f"  {fid}: old == new (no-op edit)")
            continue
        text = text.replace(old, new)

    if errors:
        print(f"ABORT — {len(errors)} edit(s) failed to match; file NOT modified:")
        print("\n".join(errors))
        sys.exit(1)

    if dry:
        print(f"DRY-RUN OK — all {len(edits)} edits match exactly; file not written.")
        return

    with open(target, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"OK — applied {len(edits)} edits to {target}")


if __name__ == "__main__":
    main()
