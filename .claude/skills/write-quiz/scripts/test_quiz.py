#!/usr/bin/env python3
"""End-to-end browser tests for a built chapter quiz (quizzes/chNN.html), any size.

Drives the page with Playwright (Chromium) and checks: start gating, Practice flow
(feedback, locking, keyboard, finish, full review), Exam pass (certificate, full key),
the exact 80% boundary, Exam fail (NO key leaks), timer warnings + auto-submit
(page.clock), attempt counter, blocked localStorage, KaTeX rendering, one-page
certificate/report PDFs, and no horizontal scroll in light/dark at 1280/375 px.
Screenshots and PDFs go to --out for visual inspection.

Usage:
    python3 .claude/skills/write-quiz/scripts/test_quiz.py ch02 --out <scratch-dir>
Exit code 0 only if every check passes and the console has no errors.
"""

import argparse
import base64
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[4]
NAME = "Ana María Rodríguez"

ap = argparse.ArgumentParser()
ap.add_argument("chapter")
ap.add_argument("--out", type=Path, required=True, help="directory for screenshots and PDFs (use the session scratchpad)")
ap.add_argument("--html", type=Path, help="quiz page (default quizzes/<chapter>.html)")
args = ap.parse_args()

HTML = (args.html or ROOT / "quizzes" / f"{args.chapter}.html").resolve()
OUT = args.out
OUT.mkdir(parents=True, exist_ok=True)
URL = HTML.as_uri()
bank = json.loads(base64.b64decode(re.search(r'id="quiz-bank" type="text/plain">([^<]+)<', HTML.read_text(encoding="utf-8")).group(1)).decode("utf-8"))
META = bank["meta"]
N = META["n_items"]
T = int(META["minutes"]) * 60
PASS_N = math.ceil(META["pass_pct"] / 100 * N)

results, console_errors = [], []


def check(cond, msg):
    results.append(("PASS" if cond else "FAIL", msg))
    print(("PASS " if cond else "FAIL ") + msg)


def key(item):
    return [i for i, o in enumerate(item["options"]) if o["correct"]]


def wrong(item):
    return [i for i in range(len(item["options"])) if i not in key(item)]


def mmss(sec):
    return f"{sec // 60:02d}:{sec % 60:02d}"


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def new_page(browser, width=1280, scheme="light", clock=False):
    ctx = browser.new_context(viewport={"width": width, "height": 900}, color_scheme=scheme, device_scale_factor=1)
    page = ctx.new_page()
    page.on("console", lambda m: console_errors.append(f"{m.type}: {m.text}") if m.type == "error" else None)
    page.on("pageerror", lambda e: console_errors.append(f"pageerror: {e}"))
    if clock:
        page.clock.install()
    page.goto(URL)
    page.wait_for_load_state("networkidle")
    return ctx, page


def start(page, mode):
    page.fill("#name", NAME)
    page.click(f"#mode-{mode}")
    page.click("#start")
    page.wait_for_selector("#screen-quiz:not([hidden])")


def pick(page, idxs):
    for i in idxs:
        page.click(f'#q-options .opt[data-index="{i}"]')


def answer_all(page, items, plan):
    for i, item in enumerate(items):
        picks = plan(i, item)
        if picks:
            pick(page, picks)
        if i < len(items) - 1:
            page.click("#next")


def submit(page):
    page.click("#submit")
    page.click("#modal-confirm")
    page.wait_for_selector("#screen-results:not([hidden])")


def no_hscroll(page, w, label):
    sw = page.evaluate("document.documentElement.scrollWidth")
    check(sw <= w, f"{label}: no horizontal scroll (scrollWidth={sw})")


def has_math(items, visible_only=False):
    """Indices of items with KaTeX math (visible_only: in the stem or option texts, i.e. shown before checking)."""
    def text(it):
        return it["stem"] + "".join(o["text"] for o in it["options"]) if visible_only else json.dumps(it, ensure_ascii=False)
    return [i for i, it in enumerate(items) if "\\(" in text(it) or "\\[" in text(it)]


# Deterministic ~50% plan for the failing exam: evens correct; first multi incomplete; last two odd unanswered.
exam = bank["exam"]
first_multi = next((i for i, it in enumerate(exam) if it["type"] == "multi"), None)
odd = [i for i in range(1, N, 2) if i != first_multi]
unanswered = set(odd[-2:])


def half(i, it):
    if i == first_multi:
        return key(it)[:1]
    if i in unanswered:
        return []
    if i % 2 == 0:
        return key(it)
    if it["type"] == "multi":
        return wrong(it)[:1] + key(it)[:1]
    return wrong(it)[:1]


with sync_playwright() as p:
    browser = p.chromium.launch()

    # ---------- Welcome ----------
    for scheme in ("light", "dark"):
        for w in (1280, 375):
            ctx, page = new_page(browser, w, scheme)
            page.fill("#name", NAME); page.click("#mode-exam"); page.mouse.move(2, 2); page.wait_for_timeout(300)
            page.screenshot(path=str(OUT / f"welcome_{scheme}_{w}.png"), full_page=True)
            no_hscroll(page, w, f"welcome {scheme} {w}")
            if scheme == "light" and w == 1280:
                body = page.inner_text("#screen-welcome")
                check(f"{N} " in body and f"{META['minutes']}-minute" in body, f"welcome shows {N} questions and {META['minutes']}-minute countdown")
                check(page.evaluate("typeof window.renderMathInElement === 'function' && typeof window.katex === 'object'"), "KaTeX + auto-render loaded")
            ctx.close()

    # ---------- Start gating ----------
    ctx, page = new_page(browser)
    check(page.is_disabled("#start"), "start disabled initially")
    page.fill("#name", "A"); page.click("#mode-practice")
    check(page.is_disabled("#start"), "start disabled with 1-char name")
    page.fill("#name", "  Al   Bo  ")
    check(page.is_enabled("#start"), "start enabled with valid name + mode")
    page.click("#start")
    check(page.evaluate("__quiz.getState()")["name"] == "Al Bo", "name whitespace cleaned")
    ctx.close()

    # ---------- Practice ----------
    practice = bank["practice"]
    # first multi after item 0 (item 0 is checked, hence locked, before the multi screenshot)
    p_multi = next(i for i, it in enumerate(practice) if it["type"] == "multi" and i > 0)
    for scheme in ("light", "dark"):
        for w in (1280, 375):
            ctx, page = new_page(browser, w, scheme)
            start(page, "practice")
            pick(page, wrong(practice[0])[:1]); page.click("#check")
            fb = page.locator("#feedback")
            check(fb.is_visible() and "key idea" in fb.inner_text().lower(), f"practice {scheme} {w}: feedback + key idea after check")
            check(page.locator("#q-options .opt.is-correct").count() == len(key(practice[0])), "practice: correct option(s) marked after check")
            check(page.locator("#q-options .opt-fb").count() == len(practice[0]["options"]), "practice: feedback on every option")
            check(page.is_disabled('#q-options input[value="0"]'), "practice: item locked after check")
            page.screenshot(path=str(OUT / f"practice_feedback_{scheme}_{w}.png"), full_page=True)
            page.click(f'#navigator .nav-cell[data-i="{p_multi}"]'); pick(page, [0])
            page.screenshot(path=str(OUT / f"practice_multi_{scheme}_{w}.png"))
            no_hscroll(page, w, f"practice {scheme} {w}")
            ctx.close()

    ctx, page = new_page(browser)
    start(page, "practice")
    for i in range(10):
        if i < 3 and practice[i]["type"] != "multi":
            page.keyboard.press("abcde"[key(practice[i])[0]]); page.keyboard.press("Enter"); page.keyboard.press("Enter")
        else:
            pick(page, key(practice[i])); page.click("#check"); page.click("#next")
    st = page.evaluate("__quiz.getState()")
    check(st["current"] == 10 and sum(st["checked"]) == 10, f"practice: keyboard + click flow checked 10 (current={st['current']})")
    pick(page, key(practice[10]))
    page.click("#finish")
    check(page.is_visible("#modal"), "practice: finish opens custom modal when items remain")
    page.click("#modal-confirm"); page.wait_for_selector("#screen-results:not([hidden])")
    st = page.evaluate("__quiz.getState()")
    check(st["results"]["score"] == 11, f"practice: selected-but-unchecked answer graded (score {st['results']['score']} == 11)")
    check(page.locator("#review .key-idea").count() == N, f"practice review: key idea on all {N} items")
    check(page.is_hidden("#print-row") and page.is_visible("#take-exam"), "practice: no print button; Take the exam shown")
    review_txt = page.inner_text("#review")
    check("\\(" not in review_txt and "\\[" not in review_txt, "practice review: no raw math delimiters left")
    if has_math(practice):
        check(page.locator("#review .katex").count() > 0, "practice review: KaTeX rendered")
    page.screenshot(path=str(OUT / "practice_results_light_1280.png"))
    page.click("#take-exam")
    check(page.is_visible("#screen-welcome") and page.input_value("#name") == NAME and page.get_attribute("#mode-exam", "aria-pressed") == "true", "take-exam returns to welcome with name kept + exam selected")
    ctx.close()

    # ---------- Math in the live question view ----------
    for set_name in ("practice", "exam"):
        idxs = has_math(bank[set_name], visible_only=True)
        if idxs:
            ctx, page = new_page(browser)
            start(page, set_name)
            page.click(f'#navigator .nav-cell[data-i="{idxs[0]}"]')
            txt = page.inner_text("#q-card")
            check(page.locator("#q-card .katex").count() > 0 and "\\(" not in txt, f"{set_name} Q{idxs[0] + 1}: KaTeX rendered in question view")
            page.screenshot(path=str(OUT / f"math_{set_name}.png"))
            ctx.close()

    # ---------- Exam: all correct ----------
    for scheme in ("light", "dark"):
        for w in (1280, 375):
            ctx, page = new_page(browser, w, scheme)
            start(page, "exam")
            pick(page, [0]); page.click("#flag")
            answer_all(page, exam, lambda i, it: key(it) if i != 0 else [])
            page.click('#navigator .nav-cell[data-i="0"]'); pick(page, key(exam[0]))
            page.mouse.move(2, 2); page.wait_for_timeout(300)
            page.screenshot(path=str(OUT / f"exam_question_{scheme}_{w}.png"), full_page=True)
            no_hscroll(page, w, f"exam {scheme} {w}")
            page.click("#submit")
            check("Flagged for review: 1" in page.inner_text("#modal-body"), "exam: submit modal shows flagged count")
            page.click("#modal-confirm"); page.wait_for_selector("#screen-results:not([hidden])")
            st = page.evaluate("__quiz.getState()")
            check(st["results"]["score"] == N and st["results"]["passed"], f"exam pass {scheme} {w}: {N}/{N} passed")
            check(page.is_visible("#cert-block") and page.locator("#cert-preview .cert-name").inner_text() == NAME, "exam pass: certificate preview with name")
            check(page.locator("#review .key-idea").count() == N, "exam pass: full key + explanations in review")
            page.wait_for_timeout(600)
            page.screenshot(path=str(OUT / f"exam_pass_{scheme}_{w}.png"))
            no_hscroll(page, w, f"exam pass results {scheme} {w}")
            if scheme == "dark" and w == 1280:
                page.emulate_media(media="print")
                page.pdf(path=str(OUT / "certificate.pdf"), prefer_css_page_size=True, print_background=True)
                page.emulate_media(media="screen")
            ctx.close()

    # ---------- Exam: the 80% boundary ----------
    for n_ok, should_pass in ((PASS_N, True), (PASS_N - 1, False)):
        ctx, page = new_page(browser)
        start(page, "exam")
        answer_all(page, exam, lambda i, it: key(it) if i < n_ok else wrong(it)[:1])
        submit(page)
        st = page.evaluate("__quiz.getState()")
        check(st["results"]["score"] == n_ok and st["results"]["passed"] == should_pass,
              f"exam {n_ok}/{N} ({100 * n_ok / N:.0f}%): passed={st['results']['passed']} (expected {should_pass})")
        ctx.close()

    # ---------- Exam: ~50%, key must stay hidden ----------
    ctx, page = new_page(browser)
    start(page, "exam")
    answer_all(page, exam, half)
    expected = sum(1 for i, it in enumerate(exam) if sorted(half(i, it)) == sorted(key(it)))
    submit(page)
    st = page.evaluate("__quiz.getState()")
    check(st["results"]["score"] == expected and not st["results"]["passed"], f"exam fail: score {st['results']['score']} == expected {expected}, not passed")
    sel_hidden = '#review .r-item[data-status="missed"], #review .r-item[data-status="unanswered"]'
    n_missed = page.locator('#review .r-item[data-status="missed"]').count()
    check(n_missed > 0 and page.locator(f'{sel_hidden.replace(", ", " .is-correct, ")} .is-correct').count() == 0, f"exam fail: no correct-option markers in {n_missed} missed items")
    check(page.locator(f'{sel_hidden.replace(", ", " .key-idea, ")} .key-idea').count() == 0, "exam fail: no explanations on missed/unanswered items")
    leaks = []
    for i, it in enumerate(exam):
        if st["results"]["statuses"][i] == "correct":
            continue
        card = page.locator("#review .r-item").nth(i).inner_text()
        if "(correct option)" in card:
            leaks.append((it["id"], "sr marker"))
        for oi in key(it):
            if oi not in st["answers"][i] and it["type"] != "tf" and plain(it["options"][oi]["text"]) in card:
                leaks.append((it["id"], f"unpicked correct option {oi}"))
    check(not leaks, f"exam fail: no key text in missed/unanswered cards {leaks[:5]}")
    check(page.locator(f'{sel_hidden.replace(", ", " .revisit, ")} .revisit').count() == page.locator(sel_hidden).count(), "exam fail: concept-to-revisit on every missed/unanswered item")
    check("At least one option that also applies was not selected." in page.inner_text("#review"), "exam fail: incomplete-multi message shown")
    check(page.is_visible("#report-block") and page.is_hidden("#cert-block"), "exam fail: report block, no certificate")
    page.screenshot(path=str(OUT / "fail_top_light_1280.png"))
    items_loc = page.locator("#review .r-item")
    items_loc.nth(0).scroll_into_view_if_needed()
    y0 = items_loc.nth(0).bounding_box()["y"] + page.evaluate("scrollY")
    b5 = items_loc.nth(min(5, N - 1)).bounding_box()
    y5 = b5["y"] + b5["height"] + page.evaluate("scrollY")
    page.screenshot(path=str(OUT / "fail_review_light_1280.png"), full_page=True, clip={"x": 0, "y": y0 - 10, "width": 1280, "height": min(2600, y5 - y0 + 20)})
    page.click("#filter-missed")
    check(page.locator('#review .r-item[data-status="correct"]').count() == 0, "review filter: missed only hides correct")
    page.emulate_media(media="print")
    page.pdf(path=str(OUT / "report.pdf"), prefer_css_page_size=True, print_background=True)
    pa = page.inner_text("#print-area")
    check(all(plain(it["stem"])[:40] not in pa for it in exam), "print area contains no questions")
    page.emulate_media(media="screen")
    ctx.close()

    ctx, page = new_page(browser, 375, "dark")
    start(page, "exam"); answer_all(page, exam, half); submit(page)
    page.screenshot(path=str(OUT / "exam_fail_dark_375.png"), full_page=True)
    no_hscroll(page, 375, "exam fail dark 375")
    ctx.close()

    # ---------- Timer ----------
    ctx, page = new_page(browser, clock=True)
    start(page, "exam")
    pick(page, key(exam[0]))
    page.clock.run_for(2000)
    t0 = page.inner_text("#timer-text")
    check(t0 in (mmss(T - 2), mmss(T - 1)), f"timer counts down from {mmss(T)} (shows {t0})")
    page.clock.fast_forward((T - 2 - 297) * 1000)             # ms -> about 4:57 left
    page.clock.run_for(500)
    check("warn" in page.get_attribute("#timer", "class") and "5 minutes" in page.inner_text("#toast"), f"timer: 5-minute warning (timer={page.inner_text('#timer-text')})")
    page.screenshot(path=str(OUT / "timer_warn.png"))
    page.clock.fast_forward(240 * 1000)                       # ms -> about 0:57 left
    page.clock.run_for(500)
    check("danger" in page.get_attribute("#timer", "class"), f"timer: 1-minute danger state (timer={page.inner_text('#timer-text')})")
    page.click("#submit")                                     # modal open while time runs out
    page.clock.fast_forward(65 * 1000)
    page.clock.run_for(500)
    st = page.evaluate("__quiz.getState()")
    check(st["phase"] == "results" and st["autoSubmitted"], "timer: auto-submit at 0 with modal open")
    check(page.is_visible("#timeout-note") and page.is_hidden("#modal"), "timer: time's-up notice shown, modal closed")
    check(st["results"]["timeUsedSec"] == T and st["results"]["score"] == 1, f"timer: time used {mmss(T)}, score 1 (got {st['results']['timeUsedSec']}, {st['results']['score']})")
    ctx.close()

    # ---------- Attempts ----------
    ctx, page = new_page(browser)
    start(page, "exam"); submit(page)
    page.click("#retake")
    check("Exam attempts in this browser: 1" in page.inner_text("#exam-attempts") and page.get_attribute("#mode-exam", "aria-pressed") == "true", "attempt counter 1; retake preselects exam")
    page.click("#start")
    check(page.evaluate("__quiz.getState()")["attempt"] == 2, "second exam is attempt 2")
    submit(page)
    check("2 (this browser)" in page.inner_text("#result-meta"), "results show Attempt 2 (this browser)")
    ctx.close()

    # ---------- Storage blocked ----------
    ctx = browser.new_context()
    ctx.add_init_script("Object.defineProperty(window, 'localStorage', { get() { throw new Error('blocked'); } });")
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.goto(URL); page.wait_for_load_state("networkidle")
    start(page, "exam"); submit(page)
    check(not errs and page.is_visible("#screen-results"), f"works with localStorage blocked (errors={errs})")
    ctx.close()

    browser.close()

# ---------- PDFs ----------
have_poppler = shutil.which("pdfinfo") and shutil.which("pdftoppm")
for pdf, size in (("certificate.pdf", "792 x 612"), ("report.pdf", "612 x 792")):
    if not have_poppler:
        print(f"SKIP {pdf} page checks (poppler not installed)")
        continue
    info = subprocess.run(["pdfinfo", str(OUT / pdf)], capture_output=True, text=True).stdout
    pages = re.search(r"Pages:\s+(\d+)", info).group(1)
    psize = re.search(r"Page size:\s+(.+)", info).group(1)
    check(pages == "1" and size in psize, f"{pdf}: one page, {psize}")
    subprocess.run(["pdftoppm", "-png", "-r", "70", str(OUT / pdf), str(OUT / pdf.replace(".pdf", "_render"))])

check(not console_errors, f"no console errors {console_errors[:3]}")
fails = [m for s, m in results if s == "FAIL"]
print(f"\n{len(results) - len(fails)}/{len(results)} checks passed   (screenshots + PDFs in {OUT})")
for f in fails:
    print("FAILED:", f)
sys.exit(1 if fails else 0)
