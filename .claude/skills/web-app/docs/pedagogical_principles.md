# Pedagogical Principles

The ten rules this skill is built around. Read before starting any chapter. If a new requirement conflicts with one of these rules, flag it explicitly in the plan — don't quietly drift.

## 1. Start from the chapter's Key Concepts

Every widget targets exactly one Key Concept. The concept drives the interaction, not the other way around. If you can't state which concept a proposed widget teaches, don't build it.

## 2. Use the book's own datasets

The student is toggling between the chapter and the app. Matching datasets keeps that transition seamless. Supplementary data (e.g., Maddison Project long series in Chapter 2) is allowed only when a concept can't be illustrated with book data — and it must be attributed in the footer and in `PLAN.md`.

## 3. Fewer, sharper widgets beat more, shallower ones

A chapter typically has 7–11 Key Concepts. Not all of them benefit from interactivity. Aim for 6–10 widgets, never more. If two Key Concepts collapse naturally into one interaction, build one widget and document the concept pairing.

## 4. Every widget gets a "Try this" block

Two to four numbered imperative experiments, each specific to the chapter's dataset. Not generic ("drag the slider"). Specific ("drag to $500k — which moves further, mean or median?"). This is the single highest-leverage pedagogical feature the skill produces.

## 5. Every widget gets a Reset button

Students explore. They get stuck. One click returns the widget to the canonical view the chapter describes. Low friction matters.

## 6. Numbers must match the chapter

If the chapter quotes mean = $41,412.69, the app's stats grid must show $41,412.69 within rounding. Any discrepancy ≥ 1% is flagged in `PLAN.md` with an explanation (different formula convention, different sample, etc.).

## 7. Make the punchline impossible to miss

A Δ readout ("mean moved 12× more than median") is more effective than "compare the current values." When a widget has a clear lesson, surface it numerically and visually, don't rely on the student noticing.

## 8. Progressive disclosure

Controls are obvious, chart behavior reacts live, the lesson is in the callout. Students shouldn't need to read documentation. If a widget needs explaining beyond its lede and its callout, it's too complicated.

## 9. Respect the reader's attention

One chapter, one HTML file. No multi-page apps. No sign-up. No tracking. No cookies beyond `localStorage` for the theme preference. Fast-loading (< 200 KB). Works offline after first CDN cache.

## 10. Teach the instructor, not just the student

Include features that let instructors teach with the app: shareable URL-hash state ("open this link to see what I mean"), Reset buttons for lab sections, on-theme printing (light mode prints fine). The app should be usable in front of a class, not just at a desk.

## What this principle set rules out

- Gimmicks: 3D rotations, parallax scroll, splash animations. Nothing that doesn't teach.
- Generic chart types that don't pay rent on a Key Concept.
- Content the chapter doesn't cover. (The app is a supplement, not an expansion.)
- Synthetic data as illustration when real data works. Real data anchors the concept in a recognizable example.
