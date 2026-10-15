"""Validate a chapter quiz bank and build the self-contained quiz page.

Reads quizzes/banks/chNN.json, checks it against the bank schema, prints a
summary (type mix, answer-position balance) plus cue warnings (patterns that
let test-wise students guess), and writes quizzes/chNN.html by inlining the
bank (base64) into quizzes/_template.html.

Usage:
    python3 scripts/build_quiz.py ch01
    python3 scripts/build_quiz.py ch01 --bank path/to/bank.json --out path/to/out.html
    python3 scripts/build_quiz.py ch01 --check     # validate + warnings only, no HTML written
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import re
import sys
from collections import Counter
from itertools import groupby
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUIZ_DIR = ROOT / "quizzes"
TEMPLATE = QUIZ_DIR / "_template.html"

META_KEYS = ("chapter", "chapter_title", "book_title", "minutes", "pass_pct", "n_items")
SETS = ("practice", "exam")
TYPES = ("single", "multi", "tf")
LETTERS = "ABCDEFGH"

# Book-wide quiz policy (see .claude/skills/write-quiz/SKILL.md)
MIN_ITEMS, MAX_ITEMS = 20, 40
PASS_PCT = 80
MIN_PER_ITEM = 1.5


def expected_minutes(n_items: int) -> int:
    """1.5 minutes per question, rounded up to a multiple of 5."""
    return int(math.ceil(n_items * MIN_PER_ITEM / 5.0) * 5)


def plain(text: str) -> str:
    """Visible text without tags or math markup (for length comparisons)."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\\\(|\\\)|\\\[|\\\]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def string_fields(item: dict):
    """Yield (label, text) for every authored string in an item."""
    for field in ("concept", "stem", "explanation"):
        if isinstance(item.get(field), str):
            yield field, item[field]
    for o_idx, opt in enumerate(item.get("options") or []):
        if isinstance(opt, dict):
            label = LETTERS[o_idx] if o_idx < len(LETTERS) else str(o_idx)
            for field in ("text", "feedback"):
                if isinstance(opt.get(field), str):
                    yield f"option {label} {field}", opt[field]


def markup_errors(where: str, label: str, text: str) -> list[str]:
    """Math delimiters must balance; '$' is currency only; a bare '<' must be '&lt;'."""
    errs = []
    if text.count("\\(") != text.count("\\)"):
        errs.append(f"{where} {label}: unbalanced \\( … \\) math delimiters")
    if text.count("\\[") != text.count("\\]"):
        errs.append(f"{where} {label}: unbalanced \\[ … \\] math delimiters")
    if re.search(r"\$(?![\d])", text):
        errs.append(f"{where} {label}: '$' not followed by a digit — '$' is for currency only; write math as \\( … \\)")
    if re.search(r"<(?![a-zA-Z/!])", text):
        errs.append(f"{where} {label}: bare '<' — write '&lt;'")
    return errs


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
    if n_items is not None:
        if not (MIN_ITEMS <= n_items <= MAX_ITEMS and n_items % 5 == 0):
            errors.append(f"meta.n_items must be a multiple of 5 in [{MIN_ITEMS}, {MAX_ITEMS}], got {n_items}")
        if meta.get("minutes") != expected_minutes(n_items):
            errors.append(f"meta.minutes must be {expected_minutes(n_items)} for {n_items} items (1.5 min each, rounded up to 5), got {meta.get('minutes')}")
    if meta.get("pass_pct") != PASS_PCT:
        errors.append(f"meta.pass_pct must be {PASS_PCT}, got {meta.get('pass_pct')}")

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
            for label, text in string_fields(item):
                errors.extend(markup_errors(where, label, text))

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


def cue_warnings(bank: dict) -> list[str]:
    """Patterns that let a test-wise student score without the concept (lessons from ch01 reviews)."""
    warns: list[str] = []
    for set_name in SETS:
        items = bank[set_name]
        singles = [it for it in items if it["type"] == "single"]
        multis = [it for it in items if it["type"] == "multi"]
        tfs = [it for it in items if it["type"] == "tf"]
        n = len(items)

        # Type mix (ch01: ~63% single, ~17% multi, ~20% tf)
        for label, group, lo, hi in (("single", singles, .50, .75), ("multi", multis, .10, .25), ("tf", tfs, .12, .28)):
            share = len(group) / n if n else 0
            if not lo <= share <= hi:
                warns.append(f"{set_name}: {label} share {share:.0%} outside {lo:.0%}-{hi:.0%}")

        # Single-answer key position balance (4-option items)
        pos = Counter(LETTERS[[o["correct"] for o in it["options"]].index(True)] for it in singles if len(it["options"]) == 4)
        if pos:
            counts = [pos.get(k, 0) for k in "ABCD"]
            if max(counts) - min(counts) > 2:
                warns.append(f"{set_name}: single key positions unbalanced {dict(zip('ABCD', counts))}")

        # Key sequence: cycling through A-D (no letter ever repeats back to back) lets students rule out
        # the previous letter; long runs of one letter are a cue too. ~1 in 4 transitions should repeat.
        seq = [[o["correct"] for o in it["options"]].index(True) for it in singles]
        if len(seq) >= 10:
            repeats = sum(1 for a, c in zip(seq, seq[1:]) if a == c)
            longest_run = max(len(list(g)) for _, g in groupby(seq))
            if repeats == 0:
                warns.append(f"{set_name}: single keys never repeat back to back ({''.join(LETTERS[k] for k in seq)}); let some consecutive items share a letter")
            if longest_run >= 3:
                warns.append(f"{set_name}: {longest_run} consecutive single items share the same key letter ({''.join(LETTERS[k] for k in seq)})")

        # Correct option is clearly the longest (>= 15% and >= 8 characters longer than any distractor)
        longest = []
        for it in singles:
            lens = [len(plain(o["text"])) for o in it["options"]]
            k = [o["correct"] for o in it["options"]].index(True)
            rival = max(l for i, l in enumerate(lens) if i != k)
            if lens[k] >= 1.15 * rival and lens[k] - rival >= 8:
                longest.append(it["id"])
        if singles and len(longest) / len(singles) > 0.25:
            warns.append(f"{set_name}: key is clearly the longest option in {len(longest)}/{len(singles)} single items ({', '.join(longest)})")

        # Multi-select patterns
        if len(multis) >= 2:
            keys = [tuple(i for i, o in enumerate(it["options"]) if o["correct"]) for it in multis]
            alternating = [k for k in keys if all(i % 2 == 0 for i in k) or all(i % 2 == 1 for i in k)]
            if len(alternating) == len(keys):
                warns.append(f"{set_name}: every multi key uses only odd or only even positions {['/'.join(LETTERS[i] for i in k) for k in keys]}")
            if len(multis) >= 3 and len({len(k) for k in keys}) == 1:
                warns.append(f"{set_name}: every multi item has exactly {len(keys[0])} correct options")
            wrong_counts = {len(it["options"]) - len(k) for it, k in zip(multis, keys)}
            if len(multis) >= 3 and len(wrong_counts) == 1:
                warns.append(f"{set_name}: every multi item has exactly {wrong_counts.pop()} wrong options, so the option count gives away how many to tick")

        # True/False balance
        tf_true = sum(1 for it in tfs if it["options"][0]["correct"])
        if abs(tf_true - (len(tfs) - tf_true)) > 1:
            warns.append(f"{set_name}: true/false answers unbalanced (True {tf_true}, False {len(tfs) - tf_true})")

        # Exam: wrong-option feedback quoting a correct option verbatim (shown below 80% where the key is hidden)
        if set_name == "exam":
            for it in items:
                if it["type"] == "tf":
                    continue
                keys_txt = [plain(o["text"]).lower().rstrip(".") for o in it["options"] if o["correct"]]
                for o_idx, o in enumerate(it["options"]):
                    if o["correct"]:
                        continue
                    fb = plain(o["feedback"]).lower()
                    for kt in keys_txt:
                        if len(kt) >= 12 and kt in fb:
                            warns.append(f"exam {it['id']} option {LETTERS[o_idx]}: feedback quotes the correct option text")
    return warns


CORRECTION_RE = re.compile(
    r"\b(forgot|forgetting|you (?:divided|multiplied|used|swapped|subtracted|added|reversed)|square root|upside down|"
    r"the other way around|check (?:which|whether|the sign|the last step|the order)|direction is wrong)\b", re.I)
LEAK_NUM_RE = re.compile(r"\d[\d,]*\.\d+|\d{1,3}(?:,\d{3})+|\d{3,}")
STOPWORDS = {"the", "a", "an", "of", "is", "are", "to", "in", "and", "or", "that", "it", "its", "be", "by", "for", "on",
             "with", "as", "this", "not", "so", "at", "from", "than", "which", "would", "can", "has", "have"}


def cue_hints(bank: dict) -> list[str]:
    """Heuristic leak detectors (ch03-ch07 reviews). Not counted as warnings: read each one and fix it or
    justify it in the log. False positives are expected (e.g., a scenario number shared by several items)."""
    hints: list[str] = []
    for set_name in SETS:
        singles = [it for it in bank[set_name] if it["type"] == "single"]
        strict = []
        for it in singles:
            lens = [len(plain(o["text"])) for o in it["options"]]
            k = [o["correct"] for o in it["options"]].index(True)
            if lens[k] > max(l for i, l in enumerate(lens) if i != k):
                strict.append(it["id"])
        if singles and len(strict) / len(singles) > 0.40:
            hints.append(f"{set_name}: key is strictly the longest option in {len(strict)}/{len(singles)} single items ({', '.join(strict)})")
        # Reverse cue (ch12): distractors padded until "never pick the longest" works
        wordy = [it for it in singles if max(len(plain(o["text"])) for o in it["options"]) >= 40]
        if len(wordy) >= 8 and sum(it["id"] in strict for it in wordy) / len(wordy) < 0.10:
            hints.append(f"{set_name}: key is almost never the longest option in wordy single items "
                         f"({sum(it['id'] in strict for it in wordy)}/{len(wordy)}); 'avoid the longest' would work")
        # Multi: every correct option longer than every wrong option
        for it in bank[set_name]:
            if it["type"] != "multi":
                continue
            ks = [len(plain(o["text"])) for o in it["options"] if o["correct"]]
            ws = [len(plain(o["text"])) for o in it["options"] if not o["correct"]]
            if ws and min(ks) > max(ws):
                hints.append(f"{set_name} {it['id']}: every correct option is longer than every wrong option")

    exam = [it for it in bank["exam"] if it["type"] != "tf"]
    # 1. Exam wrong-option feedback that reads like a one-step correction (shown without the key below 80%)
    for it in exam:
        for o_idx, o in enumerate(it["options"]):
            m = CORRECTION_RE.search(plain(o["feedback"]))
            if not o["correct"] and m:
                hints.append(f"exam {it['id']} option {LETTERS[o_idx]}: feedback may be a one-step correction (\"{m.group(0)}\")")
    # 2. A number computed in one exam key (absent from its own stem) printed in another exam item's stem/options
    visible = {it["id"]: plain(it["stem"]) + " " + " ".join(plain(o["text"]) for o in it["options"]) for it in bank["exam"]}
    for it in exam:
        own = plain(it["stem"])
        nums = {n for o in it["options"] if o["correct"] for n in LEAK_NUM_RE.findall(plain(o["text"]))}
        opt_txt = [plain(o["text"]) for o in it["options"]]
        # skip numbers given in the stem, years, and unit-like numbers shared by several of the item's options
        nums = {n for n in nums if n not in own and not re.fullmatch(r"(19|20)\d\d", n)
                and sum(n in t for t in opt_txt) < 2}
        for num in sorted(nums):
            pat = r"(?<![\d.,])" + re.escape(num) + r"(?![\d]|[.,]\d)"
            others = [j for j, txt in visible.items() if j != it["id"] and re.search(pat, txt)]
            if others:
                hints.append(f"exam {it['id']}: computed key value {num} is printed in {', '.join(others)}")
    # 3. Practice key worded like an exam key (pre-teaches the exam answer)
    def words(t: str) -> set[str]:
        return set(re.findall(r"[a-z0-9]+", plain(t).lower())) - STOPWORDS
    p_keys = [(it["id"], words(o["text"])) for it in bank["practice"] if it["type"] != "tf" for o in it["options"] if o["correct"]]
    for it in exam:
        for o in it["options"]:
            ew = words(o["text"])
            if not o["correct"] or len(ew) < 5:
                continue
            for pid, pw in p_keys:
                if len(pw) >= 5 and len(ew & pw) / len(ew | pw) >= 0.5:
                    hints.append(f"exam {it['id']} key is worded like practice {pid} key (mirror, don't clone)")
    # 4. Practice explanation or feedback that restates an exam key (ch08 P19 -> E19, ch10 P09 -> E09)
    p_texts = [(it["id"], words(it.get("explanation", "")) | set().union(*(words(o["feedback"]) for o in it["options"])))
               for it in bank["practice"]]
    for it in exam:
        for o in it["options"]:
            ew = words(o["text"])
            if not o["correct"] or len(ew) < 7:
                continue
            for pid, pw in p_texts:
                if len(ew & pw) / len(ew) >= 0.85:
                    hints.append(f"exam {it['id']} key is nearly restated in practice {pid} feedback/explanation")
    # 5. Plain-text subscripts render with a literal underscore (ch15: s_e, β_age); use <sub> or KaTeX
    for set_name in SETS:
        for it in bank[set_name]:
            texts = [it["stem"], it.get("explanation", ""), it.get("concept", "")]
            texts += [t for o in it["options"] for t in (o["text"], o["feedback"])]
            for t in texts:
                t = re.sub(r"<code>.*?</code>|\\\(.*?\\\)|\\\[.*?\\\]", "", t)
                for tok in re.findall(r"[^\s(]*[^\W\d_]_[^\s,.;:)]+", t):
                    if not re.fullmatch(r"[A-Z0-9_]+", tok.strip("()")):
                        hints.append(f"{set_name} {it['id']}: raw underscore in visible text ({tok}); use <sub> or KaTeX")
    return list(dict.fromkeys(hints))


def chapter_number(chapter: str) -> str:
    stripped = str(chapter).lstrip("0")
    return stripped or "0"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a quiz bank and build the quiz page.")
    parser.add_argument("chapter", help="chapter id, e.g. ch01")
    parser.add_argument("--bank", type=Path, help="bank JSON (default quizzes/banks/<chapter>.json)")
    parser.add_argument("--out", type=Path, help="output HTML (default quizzes/<chapter>.html)")
    parser.add_argument("--check", action="store_true", help="validate and print warnings only; do not write HTML")
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
    warns = cue_warnings(bank)
    for w in warns:
        print(f"  WARN {w}")
    print(f"  cue warnings: {len(warns)}")
    hints = cue_hints(bank)
    for h in hints:
        print(f"  HINT {h}")
    print(f"  leak hints: {len(hints)} (review each; not blocking)")
    if args.check:
        return 0

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
