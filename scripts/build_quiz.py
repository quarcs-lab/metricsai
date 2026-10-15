"""Validate a chapter quiz bank and build the self-contained quiz page.

Reads quizzes/banks/chNN.json, checks it against the bank schema, prints a
summary (type mix, answer-position balance), and writes quizzes/chNN.html by
inlining the bank (base64) into quizzes/_template.html.

Usage:
    python3 scripts/build_quiz.py ch01
    python3 scripts/build_quiz.py ch01 --bank path/to/bank.json --out path/to/out.html
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUIZ_DIR = ROOT / "quizzes"
TEMPLATE = QUIZ_DIR / "_template.html"

META_KEYS = ("chapter", "chapter_title", "book_title", "minutes", "pass_pct", "n_items")
SETS = ("practice", "exam")
TYPES = ("single", "multi", "tf")
LETTERS = "ABCDEFGH"


def norm(text: str) -> str:
    """Normalize a stem for duplicate detection (strip tags, collapse spaces, lowercase)."""
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def nonempty(value) -> bool:
    return isinstance(value, str) and value.strip() != ""


def validate(bank: dict) -> list[str]:
    errors: list[str] = []

    meta = bank.get("meta")
    if not isinstance(meta, dict):
        return ["bank: missing 'meta' object"]
    for key in META_KEYS:
        if key not in meta:
            errors.append(f"meta: missing '{key}'")
    n_items = meta.get("n_items")
    if not isinstance(n_items, int) or n_items < 1:
        errors.append("meta.n_items must be a positive integer")
        n_items = None
    for key in ("minutes", "pass_pct"):
        if key in meta and not (isinstance(meta[key], (int, float)) and meta[key] > 0):
            errors.append(f"meta.{key} must be a positive number")

    if "<script" in json.dumps(bank, ensure_ascii=False).lower():
        errors.append("bank: contains '<script' (not allowed)")

    seen_ids: dict[str, str] = {}
    seen_stems: dict[str, str] = {}

    for set_name in SETS:
        items = bank.get(set_name)
        if not isinstance(items, list):
            errors.append(f"{set_name}: missing list")
            continue
        if n_items is not None and len(items) != n_items:
            errors.append(f"{set_name}: has {len(items)} items, expected {n_items}")

        for idx, item in enumerate(items, start=1):
            where = f"{set_name}[{idx}]"
            if not isinstance(item, dict):
                errors.append(f"{where}: not an object")
                continue
            item_id = item.get("id")
            if nonempty(item_id):
                where = f"{set_name}[{idx}] {item_id}"
                if item_id in seen_ids:
                    errors.append(f"{where}: duplicate id (also {seen_ids[item_id]})")
                seen_ids[item_id] = where
            else:
                errors.append(f"{where}: missing id")

            for field in ("concept", "stem", "explanation"):
                if not nonempty(item.get(field)):
                    errors.append(f"{where}: missing or empty '{field}'")

            stem = item.get("stem")
            if nonempty(stem):
                key = norm(stem)
                if key in seen_stems:
                    errors.append(f"{where}: duplicate stem (also {seen_stems[key]})")
                seen_stems[key] = where

            qtype = item.get("type")
            if qtype not in TYPES:
                errors.append(f"{where}: type must be one of {TYPES}, got {qtype!r}")
                continue

            options = item.get("options")
            if not isinstance(options, list) or not options:
                errors.append(f"{where}: missing options")
                continue
            for o_idx, opt in enumerate(options):
                label = LETTERS[o_idx] if o_idx < len(LETTERS) else str(o_idx)
                if not isinstance(opt, dict):
                    errors.append(f"{where} option {label}: not an object")
                    continue
                if not nonempty(opt.get("text")):
                    errors.append(f"{where} option {label}: empty text")
                if not nonempty(opt.get("feedback")):
                    errors.append(f"{where} option {label}: empty feedback")
                if not isinstance(opt.get("correct"), bool):
                    errors.append(f"{where} option {label}: 'correct' must be true/false")

            n_correct = sum(1 for o in options if isinstance(o, dict) and o.get("correct") is True)
            if qtype == "single":
                if not 3 <= len(options) <= 5:
                    errors.append(f"{where}: single needs 3-5 options, has {len(options)}")
                if n_correct != 1:
                    errors.append(f"{where}: single needs exactly 1 correct, has {n_correct}")
            elif qtype == "tf":
                texts = [o.get("text") if isinstance(o, dict) else None for o in options]
                if texts != ["True", "False"]:
                    errors.append(f"{where}: tf options must be exactly ['True', 'False'], got {texts}")
                if n_correct != 1:
                    errors.append(f"{where}: tf needs exactly 1 correct, has {n_correct}")
            elif qtype == "multi":
                if len(options) < 3:
                    errors.append(f"{where}: multi needs >= 3 options, has {len(options)}")
                if n_correct < 2:
                    errors.append(f"{where}: multi needs >= 2 correct, has {n_correct}")

    return errors


def summarize(bank: dict) -> None:
    for set_name in SETS:
        items = bank[set_name]
        types = Counter(item["type"] for item in items)
        positions = Counter(
            LETTERS[[o["correct"] for o in item["options"]].index(True)]
            for item in items if item["type"] == "single"
        )
        tf = Counter(
            item["options"][[o["correct"] for o in item["options"]].index(True)]["text"]
            for item in items if item["type"] == "tf"
        )
        type_str = ", ".join(f"{t}={types.get(t, 0)}" for t in TYPES)
        pos_str = " ".join(f"{k}:{positions[k]}" for k in sorted(positions))
        tf_str = f"True:{tf.get('True', 0)} False:{tf.get('False', 0)}"
        print(f"  {set_name:<8} {len(items)} items | {type_str}")
        print(f"  {'':<8} single correct positions -> {pos_str or '-'} | tf answers -> {tf_str}")


def chapter_number(chapter: str) -> str:
    stripped = str(chapter).lstrip("0")
    return stripped or "0"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a quiz bank and build the quiz page.")
    parser.add_argument("chapter", help="chapter id, e.g. ch01")
    parser.add_argument("--bank", type=Path, help="bank JSON (default quizzes/banks/<chapter>.json)")
    parser.add_argument("--out", type=Path, help="output HTML (default quizzes/<chapter>.html)")
    args = parser.parse_args()

    chapter = args.chapter.lower()
    if not re.fullmatch(r"ch\d{2}", chapter):
        parser.error("chapter must look like ch01")
    bank_path = args.bank or QUIZ_DIR / "banks" / f"{chapter}.json"
    out_path = args.out or QUIZ_DIR / f"{chapter}.html"

    try:
        bank = json.loads(bank_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read bank {bank_path}: {exc}", file=sys.stderr)
        return 1

    errors = validate(bank)
    if errors:
        print(f"ERROR: {bank_path} failed validation ({len(errors)} problem(s)):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"Bank OK: {bank_path}")
    summarize(bank)

    payload = json.dumps(bank, ensure_ascii=False, separators=(",", ":"))
    bank_b64 = base64.b64encode(payload.encode("utf-8")).decode("ascii")
    title = f"Chapter {chapter_number(bank['meta']['chapter'])} Quiz · metricsAI"

    template = TEMPLATE.read_text(encoding="utf-8")
    for placeholder in ("{{BANK_B64}}", "{{TITLE}}"):
        if placeholder not in template:
            print(f"ERROR: template is missing {placeholder}", file=sys.stderr)
            return 1
    html = template.replace("{{BANK_B64}}", bank_b64).replace("{{TITLE}}", title)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
