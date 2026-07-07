# Locked conventions (Phase 1.5) — governs all Phase 2 fixes

Derived from all 18 findings files + the audit brief. Fixer agents MUST follow these.

## Reconciliation rules (findings → edits)
The findings contain cross-lens duplicates and alternatives. Before emitting edits:
1. **Dedupe:** the methods and interpretation lenses often report the SAME defect (e.g. ch05 F01≡F37, F02≡F34, F03≡F40). Emit ONE edit per distinct (old-text) span.
2. **Mutually-exclusive alternatives:** some findings fix the same line two different ways (e.g. ch05 F14 code-fix vs F30 comment-fix for the residual table; F04 full-roadmap vs F42 partial). Pick the more complete/correct one; never emit both (apply_edits.py would fail the exactly-once match or double-edit).
3. **Honor verify_note corrections:** when a finding's `verify_note` says the proposed `new` is wrong/incomplete or should be merged (e.g. ch05 F07 must also carry the units fix from F38; use the verify_note's corrected replacement text), emit the CORRECTED edit, not the raw `new`.
4. **Only action=fix findings become edits.** action=report findings go to judgment_calls.md, NOT the patch.
5. Each edit's `old` must match the current .qmd exactly once — include enough surrounding context. Apply order matters if two edits touch nearby text; keep them non-overlapping.

## Number precision (canonical)
- R²: 3 dp (0.617453 → "0.617"; "0.62" acceptable only in loose prose). Money: whole dollars with commas ($23,551). Coefficients/SE/t: 2 dp unless the displayed cell shows more.
- A prose number is correct iff it equals the executed value rounded (not truncated) to the precision shown. Every occurrence of one quantity agrees at the coarsest shared precision.
- Ground truth for the Davis house regression (n=29): slope 73.77, se(slope) 11.17, R² 0.617, s_e $23,551, ŷ@2000 sqft $262,559, 95% CI for mean [$253k,$272k], 95% PI [$213k,$312k], PI/CI width ratio 5.26×.

## Format conventions (targets)
- Section headers: `## N.M Title` (space, no colon). Applies ch08,10,11,12,14,15,16,17. **Heading WORDS verbatim** — only remove the colon.
- KEEP ch16 merged `16.2-16.4` and ch17 starting at 17.2 (deliberate AED alignment); colon→space only.
- ch17 duplicate Key Concept 17.10 → renumber later ones 17.11/17.12 (web-app strings reference only 17.4/17.7 — safe).
- ch04 `### Exercise N:` → `**Exercise N: Title**` bold.
- Case-study wrap-up "What You've Learned..." → H4 `####`.
- ch13 `### **Bold Title**` → strip bold, words verbatim.
- Redundant `**Key Takeaways:**` bold line under `## Key Takeaways` → delete (ch07, ch09).
- Missing `**Next Steps:**` (3–5 bullets, ch01 style) → add (ch04,05,06,10,11,12,16,17). Verify any chapter cross-refs in the new bullets are correct (ch12's existing one misattributes dummies to ch13 — they're ch14).
- "Dataset(s) used": singular iff one dataset (ch01/10/11 already correct).
- ch00 `title: Untitled` → "Preface".
- Blank line before every markdown list (Pandoc requirement).

## SE convention (per chapter stage; AED: robust taught ch07, default from §12.2)
- ch01–06, ch10: classical fine; if prose draws a significance conclusion from an iid fit, add ONE labeling sentence (no refit).
- ch09, ch11: add ONE sentence at first inference discussion (classical as AED pre-Ch12; §12.2 introduces robust, preferred). No refits.
- ch12–17: silently-iid inference fit that prose draws inference from → refit `vcov='HC1'` (ch17 panel: cluster by unit) + re-sync numbers. Mechanics-only iid fits → leave. Conclusion-flip → report.

## Code readability
- Split a cell only if >45 lines AND ≥2 independently interpretable outputs. Cohesive multi-panel figure = one output, don't split (add per-panel banner comments).
- Non-Setup cells get a ≥1-sentence markdown lead-in + interpretation after notable output where missing.
- House comment style: banner first line (`# 12.2 Inference with robust standard errors`), stanza comments, sparing inline arg comments.
- Never touch `#| code-fold: true` Setup cells. Net cell-count delta ≤ ±4/chapter. No new imports.
- Mid-cell bare DataFrame expressions that are meant to display → wrap in `display(...)` (recurring bug: ch05 F13, ch12 F12/13/14/70/71/72). Colab-pip hint must sit ABOVE the import it guards (ch05 F17/F18).

## Structural issues that are REPORT, not fix (do not attempt mechanically)
- ch12 §12.3/§12.5/§12.7: prose interprets a power-curve "Figure 12.3", a CI-vs-PI two-panel figure, an SE-ratio comparison table, a HAC three-way comparison, and manual-SE calculations that NO code cell produces; two section stubs ("Prediction at Specific Values", "Manual Calculation of Standard Errors", "Illustration: Power of a Test") have no code. Requires add-code-vs-delete-prose author decision.
- Any fix that would flip a stated significance/qualitative conclusion.
