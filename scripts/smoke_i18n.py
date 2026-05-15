#!/usr/bin/env python3
"""Phase 5 smoke test for the shared i18n runtime.

Spins up a localhost HTTP server (so localStorage is shared across pages),
then runs Playwright assertions:

  5.3: For each of ch04, ch10, ch16:
       - load dashboard
       - snapshot EN: lang attr, label, document.title, 4 [data-i18n] elements,
         and one Plotly tick label
       - call window.toggleLanguage()
       - snapshot ES: same fields; assert all differ
       - assert no defined-i18n-key string leaks into rendered body text
       - toggle again, assert ES->EN round-trip equals snapshot 1

  5.4: Cross-page persistence:
       - load index.html, toggle once -> ES
       - load web-apps/ch08/dashboard.html, assert __lang === "es"
       - toggle once -> EN, navigate back to index.html, assert EN boot

Usage: python3 scripts/smoke_i18n.py
"""

from __future__ import annotations

import re
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ["ch04", "ch10", "ch16"]
PORT = 8123


def collect_defined_keys() -> set[str]:
    """Mirror i18n_check.py's parser; return every defined i18n key."""
    entry_re = re.compile(r'"([\w.\-]+)"\s*:\s*\{\s*[a-z]{2}\s*:', re.DOTALL)
    keys: set[str] = set()
    for path in (ROOT / "web-apps" / "_shared" / "strings").glob("*.js"):
        keys |= set(entry_re.findall(path.read_text(encoding="utf-8")))
    return keys


def start_server(port: int) -> subprocess.Popen:
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(40):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.25):
                return proc
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"http.server didn't come up on port {port}")


def wait_for_runtime(page) -> None:
    page.wait_for_function(
        "() => window.I18N && window.I18N.strings && "
        "Object.keys(window.I18N.strings).length > 50 && window.__lang"
    )


def snapshot_chapter(page, ch: str) -> dict:
    return page.evaluate(
        """(ch) => {
          const sel = (s) => document.querySelector(s);
          const txt = (k) => {
            const el = document.querySelector('[data-i18n="' + k + '"]');
            return el ? el.textContent.trim() : null;
          };
          let plotly_tick = null;
          const tick = sel('.xtick text') || sel('.x2tick text') || sel('text.xtick');
          if (tick) plotly_tick = tick.textContent.trim();
          return {
            lang: document.documentElement.lang,
            label: (sel('#siteLanguageLabel') || {}).textContent || null,
            title: document.title,
            'chapter.title': txt('chapter.' + ch + '.title'),
            'header.badge': txt('header.badge'),
            'nav.about': txt('nav.about'),
            'common.howtoTitle': txt('common.howtoTitle'),
            'code.heading': txt('code.heading'),
            plotly_tick: plotly_tick,
          };
        }""",
        ch,
    )


# Ignore tokens that are common in code / file extensions / domain text and
# never could be an i18n key — keeps the leak detector noise-free.
LEAK_IGNORE_RE = re.compile(
    r"\.(?:py|js|html|css|md|json|csv|ipynb|com|org|dev|edu|io)$|"
    r"^(?:np|pd|plt|sns|sm|tf|sk|st|os|sys|os|self|this|that)\."
)


def find_raw_key_leak(page, defined_keys: set[str]) -> list[str]:
    body_text = page.evaluate("() => document.body.innerText")
    leaks: set[str] = set()
    for m in re.finditer(r"\b([a-z][\w]*\.[a-z][\w.]*)\b", body_text):
        candidate = m.group(1)
        if candidate in defined_keys and not LEAK_IGNORE_RE.search(candidate):
            leaks.add(candidate)
    return sorted(leaks)


LANG_CYCLE = ["en", "es", "ja"]
SNAPSHOT_KEYS = ("chapter.title", "header.badge", "nav.about",
                 "common.howtoTitle", "code.heading")


def smoke_chapter(page, base_url: str, ch: str, defined_keys: set[str]) -> str:
    """Cycle through every language in LANG_CYCLE + back to start; assert each
    transition flips lang/label/title and per-key text, then assert the final
    snapshot equals the initial one (full round-trip).
    """
    page.goto(f"{base_url}/web-apps/{ch}/dashboard.html")
    wait_for_runtime(page)
    page.wait_for_timeout(500)

    snaps = [snapshot_chapter(page, ch)]
    diffs: list[str] = []
    if snaps[0]["lang"] != LANG_CYCLE[0]:
        return (f"[{ch}] FAIL: initial lang is {snaps[0]['lang']!r} "
                f"(expected {LANG_CYCLE[0]!r})")

    for step in range(len(LANG_CYCLE)):
        page.evaluate("window.toggleLanguage()")
        page.wait_for_timeout(400)
        snap = snapshot_chapter(page, ch)
        snaps.append(snap)
        expected = LANG_CYCLE[(step + 1) % len(LANG_CYCLE)]
        prev = snaps[step]

        if snap["lang"] != expected:
            diffs.append(f"step {step}: lang is {snap['lang']!r} "
                         f"(expected {expected!r})")
        if (snap["label"] or "").lower() != expected:
            diffs.append(f"step {step}: label is {snap['label']!r} "
                         f"(expected {expected.upper()!r})")
        # Title and per-key text must change between consecutive distinct langs
        # (but step len-1 returns to the start — same content as snaps[0]).
        if expected != prev["lang"]:
            if snap["title"] == prev["title"]:
                diffs.append(f"step {step} ({prev['lang']}->{expected}): "
                             f"document.title did not change ({prev['title']!r})")
            for k in SNAPSHOT_KEYS:
                v_prev = prev.get(k)
                v_now = snap.get(k)
                if v_prev is not None and v_now is not None and v_prev == v_now:
                    diffs.append(f"step {step} ({prev['lang']}->{expected}): "
                                 f"{k} did not change ({v_prev!r})")

    # After cycling through every language, we should be back at the start.
    final = snaps[-1]
    if final["lang"] != snaps[0]["lang"]:
        diffs.append(f"round-trip: ended on {final['lang']!r}, "
                     f"expected {snaps[0]['lang']!r}")
    if final["title"] != snaps[0]["title"]:
        diffs.append(f"round-trip: title diverged "
                     f"({snaps[0]['title']!r} -> {final['title']!r})")
    for k in SNAPSHOT_KEYS:
        if final.get(k) != snaps[0].get(k):
            diffs.append(f"round-trip: {k} diverged "
                         f"({snaps[0].get(k)!r} -> {final.get(k)!r})")

    leaks = find_raw_key_leak(page, defined_keys)
    if leaks:
        diffs.append(f"raw key leak in body text: {leaks[:5]}"
                     f"{'...' if len(leaks) > 5 else ''}")

    if diffs:
        return f"[{ch}] FAIL:\n  - " + "\n  - ".join(diffs)
    titles = " -> ".join(s["title"][:30] + "…" if len(s["title"]) > 30 else s["title"]
                         for s in snaps[:-1])
    plotly_seq = " -> ".join(repr(s.get("plotly_tick")) for s in snaps[:-1])
    return f"[{ch}] PASS  (titles: {titles}; plotly: {plotly_seq})"


def smoke_persistence(page, base_url: str) -> str:
    """Toggle index.html through every language; after each toggle, navigate
    to web-apps/ch08/dashboard.html and confirm it boots in the same language.
    """
    diffs: list[str] = []

    page.goto(f"{base_url}/index.html")
    page.wait_for_function("() => window.I18N && window.__lang")
    page.wait_for_timeout(200)
    boot0 = page.evaluate("() => window.__lang")
    if boot0 != LANG_CYCLE[0]:
        diffs.append(f"index initial lang was {boot0!r} "
                     f"(expected {LANG_CYCLE[0]!r} on a fresh context)")

    for step in range(len(LANG_CYCLE)):
        expected = LANG_CYCLE[(step + 1) % len(LANG_CYCLE)]

        page.evaluate("window.toggleLanguage()")
        page.wait_for_timeout(250)
        after = page.evaluate(
            "() => ({ lang: window.__lang, ls: localStorage.getItem('language') })"
        )
        if after["lang"] != expected or after["ls"] != expected:
            diffs.append(f"step {step}: index toggle to {expected!r} failed: {after}")

        page.goto(f"{base_url}/web-apps/ch08/dashboard.html")
        page.wait_for_function("() => window.I18N && window.__lang")
        page.wait_for_timeout(400)
        boot = page.evaluate(
            """() => ({
              lang: window.__lang,
              label: (document.querySelector('#siteLanguageLabel') || {}).textContent,
              title: (document.querySelector('[data-i18n="chapter.ch08.title"]') || {}).textContent,
              ls: localStorage.getItem('language'),
            })"""
        )
        if boot["lang"] != expected:
            diffs.append(f"step {step}: ch08 didn't boot in {expected!r}: {boot}")
        if (boot["label"] or "").lower() != expected:
            diffs.append(f"step {step}: ch08 label was {boot['label']!r} "
                         f"(expected {expected.upper()!r})")
        # Return to index.html for the next cycle iteration.
        page.goto(f"{base_url}/index.html")
        page.wait_for_function("() => window.I18N && window.__lang")
        page.wait_for_timeout(200)

    final = page.evaluate("() => window.__lang")
    if final != LANG_CYCLE[0]:
        diffs.append(f"after full cycle, index lang is {final!r} "
                     f"(expected back to {LANG_CYCLE[0]!r})")

    if diffs:
        return "[persistence] FAIL:\n  - " + "\n  - ".join(diffs)
    return "[persistence] PASS"


def main() -> int:
    defined_keys = collect_defined_keys()
    print(f"Defined i18n keys: {len(defined_keys)}")

    server = start_server(PORT)
    base_url = f"http://127.0.0.1:{PORT}"
    print(f"Server up at {base_url}\n")

    failures: list[str] = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            ctx = browser.new_context()
            page = ctx.new_page()

            for ch in CHAPTERS:
                result = smoke_chapter(page, base_url, ch, defined_keys)
                print(result + "\n")
                if "FAIL" in result:
                    failures.append(result)
                    try:
                        page.screenshot(path=str(ROOT / "log" / f"phase5_{ch}_fail.png"))
                    except Exception:
                        pass

            ctx.close()
            ctx = browser.new_context()
            page = ctx.new_page()
            r = smoke_persistence(page, base_url)
            print(r + "\n")
            if "FAIL" in r:
                failures.append(r)
                try:
                    page.screenshot(path=str(ROOT / "log" / "phase5_persistence_fail.png"))
                except Exception:
                    pass

            browser.close()
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()

    if failures:
        print(f"\n=== {len(failures)} failure(s) ===")
        return 1
    print("\nALL PHASE 5 TESTS PASSED ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
