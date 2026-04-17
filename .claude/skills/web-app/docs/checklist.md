# Pre-commit Checklist

Sign off every item before merging a chapter app. If an item fails, fix it rather than marking skipped.

## Build

- [ ] `python3 scripts/build_chNN_webapp.py` runs without errors.
- [ ] Output file size under 200 KB (soft cap; investigate if larger).
- [ ] Build script prints at least one sanity-check value that matches a number quoted in the chapter.

## Automated verification

- [ ] `python3 .claude/skills/web-app/scripts/verify_app.py web-apps/chNN/dashboard.html` passes.
- [ ] No `{{…}}` placeholders remain in the output.
- [ ] JSON data island parses.
- [ ] JS passes `node --check`.

## Fidelity to the chapter

- [ ] Every summary statistic the app displays matches the chapter's quoted value within rounding (flag ≥ 1% discrepancies in PLAN.md).
- [ ] Every dataset used in a widget appears in the chapter's prose or is a documented supplementary dataset.
- [ ] Any supplementary (non-book) dataset is:
    - [ ] Cited in the dashboard footer.
    - [ ] Attributed in `web-apps/chNN/PLAN.md`.
    - [ ] Acquired by a committed `scripts/fetch_<source>.py` with provenance documented.

## Pedagogy

- [ ] Every widget targets a specific Key Concept (listed in `PLAN.md`).
- [ ] Every widget has a `.try-this` block with 2–4 chapter-specific imperative prompts (not generic).
- [ ] Every widget has a Reset button that returns controls to a sensible chapter default.
- [ ] Chapter Key Concepts not covered by a widget are listed in `PLAN.md` with reasoning.

## Interaction

- [ ] All controls (selects, ranges, toggle groups) are keyboard operable.
- [ ] Each interactive control is registered in the `REG` registry at the end of the script.
- [ ] Hash state roundtrips: drag something, copy URL, reload, widget is in the same state.
- [ ] Clicking a Reset button restores the chapter default AND updates the URL hash.
- [ ] Theme toggle re-renders every chart (verify by switching dark ↔ light).

## Layout / responsive

- [ ] Page renders correctly at 1280 px (desktop) and 375 px (mobile).
- [ ] Sticky nav remains reachable at all breakpoints.
- [ ] No horizontal scroll on mobile.

## Chrome

- [ ] Page title: `Chapter N — <Chapter Title> · metricsAI`.
- [ ] Footer links: book, GitHub, attribution (if any), back-to-top.
- [ ] Header has chapter badge and short subtitle.

## Documentation

- [ ] `web-apps/chNN/PLAN.md` exists and includes:
    - [ ] Widgets built (with target Key Concept each).
    - [ ] Key Concepts deliberately not covered (with reasoning).
    - [ ] Supplementary datasets used (with attribution).
    - [ ] Known issues / future improvements.
- [ ] `web-apps/README.md` is updated if a new supplementary dataset was added.

## Final spot checks

- [ ] Open the dashboard, click through every widget once, try the Reset buttons.
- [ ] Toggle dark mode, reload page, confirm it persisted.
- [ ] Copy a hash URL, paste in a new tab, confirm state restored.
