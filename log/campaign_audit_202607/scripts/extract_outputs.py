#!/usr/bin/env python3
"""Dump executed-notebook cell outputs to readable text for prose-number cross-checking.

Usage: python3 extract_outputs.py <executed.ipynb> [> chNN_outputs.txt]

For each code cell prints: cell index, first source line, then all textual
outputs (stream text, execute_result / display_data text/plain, and error
tracebacks marked with '!! ERROR').
"""
import json
import sys


def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)

    code_idx = 0
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        code_idx += 1
        source = cell.get("source", [])
        first_line = (source[0].rstrip() if source else "(empty cell)")
        print(f"\n{'=' * 78}")
        print(f"CELL {code_idx} | {first_line}")
        print("=" * 78)
        for out in cell.get("outputs", []):
            otype = out.get("output_type")
            if otype == "stream":
                sys.stdout.write("".join(out.get("text", [])))
            elif otype in ("execute_result", "display_data"):
                text = out.get("data", {}).get("text/plain")
                if text:
                    sys.stdout.write("".join(text) + "\n")
                elif "image/png" in out.get("data", {}):
                    print("[figure: image/png]")
            elif otype == "error":
                print(f"!! ERROR {out.get('ename')}: {out.get('evalue')}")
                for line in out.get("traceback", []):
                    print(line)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: extract_outputs.py <executed.ipynb>")
    main(sys.argv[1])
