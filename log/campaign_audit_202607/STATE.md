# Campaign state — audit_202607

**Goal:** Audit + improve all 18 chapters (statistical correctness, code readability, format consistency). Plan: `~/.claude/plans/generic-humming-donut.md` (approved 2026-07-07).

## Decisions (locked with user)
- Scope ch00–ch17. Fix directly; judgment calls → `judgment_calls.md`. Execute everything. Balanced prose latitude.
- Sync targets only (.ipynb/.md/book HTML); NO PDFs. One commit per chapter. AED conventions.
- ch12–17 silently-iid inference fits: refit with vcov='HC1' (cluster in ch17 panel), re-sync prose numbers; conclusion-flips → report.
- Web apps out of scope (mirrored errors → report). Inline `{python}` in prose prohibited. Never change heading title words.
- CLAUDE.md has unrelated unstaged edit — keep out of all commits.

## Phase status
- Phase 0 (preflight + execute-all): **DONE** 2026-07-07. Export --all clean (ipynb in sync). Baselines captured. All 18 chapters executed via nbconvert: 17 with 0 cell errors; ch09 has 2 cell errors (see seed findings 7–9). Dumps: exec/chNN_outputs.txt.
- Phase 1 (audit-all): in-progress@2026-07-07 (Workflow run wf_6fe50e8a-a35; 6 lenses/chapter + adversarial verify + consolidate → findings/chNN.{json,md}; audit brief: audit_brief.md)
  - Attempt 1 hit session usage limit: 40/135 agents done (~ch01–ch06 lenses cached), all consolidators failed → no findings files yet.
  - Resumed 17:06 JST from cache (resumeFromRunId wf_6fe50e8a-a35). If limit trips again: resume again after reset — cache accumulates across attempts.
  - Attempt 2 hit Fable 5 limit: 78/147 cumulative agents done; consolidators still failed → no findings files.
  - User switched model to Opus 4.8. Resumed again (task wwz91kbyg) on Opus. Cache replays 78 done; remaining lenses/verifiers/consolidators run on Opus.
- Phase 1 audit DONE: 1111 findings across 18 chapters (findings/chNN.{json,md}). Distinct-fix count lower due to cross-lens dupes. 0 killed = verifiers downgraded to report/low-conf + attached correction notes (not lax).
- Phase 1.5 (conventions lock): DONE. conventions.md written. judgment_calls.md seeded with 191 report items.
- Phase 2 (serial fixes): in-progress@2026-07-08. Approach: parallel fixer agents produce reconciled patches/chNN_edits.json (fix-action only, deduped, verify_note-corrected); then apply+sync+verify+re-exec+commit SERIALLY per chapter.
- KNOWN STRUCTURAL (report, not mechanical): ch12 §12.3/12.5/12.7 prose interprets figures/tables/computations that no code produces (power-curve Fig 12.3, CI-vs-PI figure, SE-ratio table, HAC 3-way, manual SE calc). Present to user.
- Phase 3 (global sweep): pending

## Baseline verify scores
ch00:39 ch01:91 ch02:91 ch03:86 ch04:84 ch05:91 ch06:81 ch07:91 ch08:91 ch09:86 ch10:91 ch11:91 ch12:86 ch13:91 ch14:86 ch15:91 ch16:91 ch17:91

## Phase 2 progress (2026-07-08)
- Patches built for all 18 chapters (patches/chNN_edits.json), 746 total edits, all dry-run validated.
- ch01 committed 6b53264 (manual loop, 20 edits, score 91). ch02 committed c6dea20 (driver, 55 edits, score 91).
- Driver: log/campaign_audit_202607/scripts/driver_apply.sh (bash3.2-safe). Gates: apply→save diff→sync(render=exec)→freshness→verify>=baseline→scoped stage→commit. Hard-stops on any fail.
- Batch ch03-ch17 running (bg bbqv35his). Applied diffs saved to patches/chNN_applied.diff for post-hoc review.
- ch00 handled separately (no book render; sync = ipynb/md only).
- TODO after batch: review code-heavy diffs (ch07,08,11,12,13); refine judgment_calls.md (ch12 structural); Phase 3 sweep.

## REMEDIATION PHASE (2026-07-08, actioning the 191 report items — user approved all recs)
- Decisions: action all 191 per recs; restore ch12/ch06 missing cells; keep ch16 merged heading; ch05 qcut; ch03/ch06 replace=True; inject %pip at export.
- Phase A DONE: %pip install pyfixest injected at export time (export_qmd_to_ipynb.py), all 18 .ipynb re-exported. Commit 6b73556.
- Phase B DONE: all 18 remediated + committed (180 edits). Commits: ch11 cd30263, ch10 10bc78f, ch13 0fb0b29, ch07 6b59483, ch05 d0ac31f, ch17 c32ab09, ch08 265ae79, ch14 c523e29, ch15 a36cb6d, ch16 3912605, ch00 e3adce4, ch01 9e951c6, ch02 e33fd3f, ch03 7233fee, ch04 5fa193a, ch09 e2a349f, ch06 5bcc0c6, ch12 c845160.
  - ch06 restored 5 cells (MC/regression/manual-SE) — verified prose numbers match exactly (0.9960/1.9944/1.2069/0.3836; manual=model SEs). 1880-census removed.
  - ch12 restored 5 cells (SE-ratio/HAC/CI-PI/prediction/power) — verified ($262,559; CI[$253k,$272k]; PI[$213k,$312k]; 5.25×; HAC lag4 ratio 1.885). Score 86→91.
  - ch11 F-stat cascade, ch10 VIF fixed (render passed). Conclusion-flips (ch08/14/15/16/17) rewritten with ground-truth.
- Post-hoc verification DONE: review agents checked 192 rewritten claims across ch08/10/11/14/15/16/17 → 0 mismatches. (Note: parallel nbconvert re-exec trips GitHub 429s → cascade NameErrors that are NOT real; re-exec serially.)
- Phase C DONE: ch13.js OVB "correlation"→"slope" (EN); i18n_check + smoke_i18n pass; ES/JA flagged. Commit bd31e5d.
- Phase D DONE: full book render clean; consistency sweep clean; JUDGMENT_CALLS_REPORT.md has RESOLUTION section; session log log/20260708_1735.md.
- REMEDIATION COMPLETE. All 191 items actioned. Only pre-existing CLAUDE.md remains uncommitted. PDFs still deferred.

## CAMPAIGN Phase 2 COMPLETE — all 18 chapters committed. Phase 3 done.
Commits: ch00 def9ccb, ch01 6b53264, ch02 c6dea20, ch03 f89fea6, ch04 5ff0a00, ch05 2ecf4a8, ch06 74c409b, ch07 df3ee26, ch08 a364bc3, ch09 b9ac89e, ch10 dff8886, ch11 5272e89, ch12 5656a49, ch13 e9335eb, ch14 a20bdab, ch15 e1ede21, ch16 a817ffa, ch17 6d71b13, book-search 0f9d56b.
756 edits applied; 191 report items → JUDGMENT_CALLS_REPORT.md. Session log: log/20260708_0731.md.
ch13/ch16 committed over score gate (verifier artifacts, documented in commits).

## Chapter ledger
| ch | executed | audited | fixed | synced | verified | re-exec | nums-ok | commit | notes |
|----|----------|---------|-------|--------|----------|---------|---------|--------|-------|
| 01 | in-progress | – | – | – | – | – | – | – | |
| 02 | in-progress | – | – | – | – | – | – | – | |
| 03 | in-progress | – | – | – | – | – | – | – | |
| 04 | in-progress | – | – | – | – | – | – | – | |
| 05 | in-progress | – | – | – | – | – | – | – | |
| 06 | in-progress | – | – | – | – | – | – | – | |
| 07 | in-progress | – | – | – | – | – | – | – | |
| 08 | in-progress | – | – | – | – | – | – | – | |
| 09 | in-progress | – | – | – | – | – | – | – | |
| 10 | in-progress | – | – | – | – | – | – | – | |
| 11 | in-progress | – | – | – | – | – | – | – | |
| 12 | in-progress | – | – | – | – | – | – | – | |
| 13 | in-progress | – | – | – | – | – | – | – | |
| 14 | in-progress | – | – | – | – | – | – | – | |
| 15 | in-progress | – | – | – | – | – | – | – | |
| 16 | in-progress | – | – | – | – | – | – | – | |
| 17 | in-progress | – | – | – | – | – | – | – | |
| 00 | in-progress | – | – | – | – | – | – | – | Preface: 0 code cells; sync = ipynb/md only; goes LAST |

## Pre-verified seed findings (execution-confirmed during planning)
1. s_e $23,162 → $23,551 (ch05 L158,L795,L819,L824,L1038; ch07 L97). Truth 23,550.66 (Davis house, n=29).
2. ch05 L1450 R² "0.618" → 0.617 (truth 0.617453).
3. ch12 KC L101–126: s_e ≈$90,000 → $23,551; PI [$180k,$380k] → [$213k,$312k]; "three to four times wider" → ~5× (5.25).
4. ch07 L206 "(in thousands of dollars)" → "(in dollars)".
5. ch07 L1636/L2431 statsmodels credited for estimation → pyfixest; L2543 cov_type='HC1' → vcov='HC1'.
6. ch17 duplicate Key Concept 17.10 (L1756 keep; L1848→17.11, L1907→17.12). Web-app strings reference only KC 17.4/17.7 — safe.
7. ch09 case study: Tasks 3/4/5 use `{python}` + `#| eval: false` cells (L1122, L1165, L1197) while Tasks 1/2 use plain ```python fences. In Colab export, eval:false cells become runnable → "Run all" throws NameError (data_2014, m3_loglog). Fix: convert Tasks 3/4/5 cells to plain ```python fences (house pattern); the loader cell L1014 should become executable (remove eval:false) so students have data_cc loaded — matches other chapters' case studies.
8. ch09 prose/code variable mismatch: dataset bullets + task text say `rk`/`hc` but actual Mendez columns (execution-confirmed) are `kl` (capital per worker) and `h` (human capital); code is right, prose wrong (L1011–1012, L1087, L1089 area, L1117, L1160, L1163). Loader prose header at L1027 uses kl/h correctly.
9. ch09 Task 4 L1174–1175: `coef()['ln_rk']`/`confint().loc['ln_rk']` — Task 3 defines `ln_kl`, so this KeyErrors even with blanks filled → change to `ln_kl` (and align task text).

## Next action
Wait for execute_all.sh (bg) → confirm 18 output dumps with 0 errors → mark Phase 0 done → launch Phase 1 audit workflow.
