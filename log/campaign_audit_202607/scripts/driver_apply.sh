#!/bin/bash
# Serial per-chapter apply -> sync -> gate -> commit driver (bash 3.2 compatible).
# Usage: driver_apply.sh ch02 ch03 ...
# Hard-stops the loop on the first gate failure (leaves that chapter uncommitted).
set -u
cd /Users/carlosmendez/Documents/GitHub/metricsai
source .venv/bin/activate
W=log/campaign_audit_202607

score_of () { python3 .claude/skills/chapter-standard/scripts/verify_chapter.py "$1" --json 2>/dev/null | python3 -c "import json,sys;cs=json.load(sys.stdin)['compliance_score'];print(cs['score'] if isinstance(cs,dict) else cs)"; }
baseline_of () { python3 -c "import json;cs=json.load(open('$W/baseline/verify_$1.json'))['compliance_score'];print(cs['score'] if isinstance(cs,dict) else cs)" 2>/dev/null || echo 0; }

for CH in "$@"; do
  QMD=$(ls notebooks_quarto/${CH}_*.qmd 2>/dev/null | head -1)
  if [ -z "$QMD" ]; then echo "!! $CH no qmd found — stopping"; exit 1; fi
  B=$(basename "$QMD" .qmd)
  BL=$(baseline_of "$CH")
  echo "========== $CH ($B) =========="

  # 1. apply
  if ! python3 $W/scripts/apply_edits.py "$QMD" "$W/patches/${CH}_edits.json"; then
    echo "!! $CH APPLY FAILED — stopping"; exit 1; fi
  git diff -- "$QMD" > "$W/patches/${CH}_applied.diff"
  echo "[$CH] diff saved ($(git diff --stat -- "$QMD" | tail -1))"

  # 2. sync (render executes Python; set -e inside aborts on error)
  if ! bash scripts/sync_chapter.sh "$QMD" > "$W/renders/${CH}_sync.log" 2>&1; then
    echo "!! $CH SYNC/RENDER FAILED — see renders/${CH}_sync.log — stopping"; tail -25 "$W/renders/${CH}_sync.log"; exit 1; fi
  if ! grep -q "\[sync\] Done" "$W/renders/${CH}_sync.log"; then
    echo "!! $CH sync did not reach Done — stopping"; tail -25 "$W/renders/${CH}_sync.log"; exit 1; fi

  # 3. freshness
  HJ="book/_freeze/notebooks_quarto/${B}/execute-results/html.json"
  if [ ! -f "$HJ" ] || [ $(( $(date +%s) - $(stat -f %m "$HJ") )) -gt 900 ]; then
    echo "!! $CH freeze not fresh — stopping"; exit 1; fi

  # 4. verify score gate (must not drop below baseline)
  S=$(score_of "$CH"); echo "[$CH] verify score: $S (baseline $BL)"
  if [ "${S:-0}" -lt "${BL:-0}" ]; then
    echo "!! $CH score $S < baseline $BL — stopping for review"; exit 1; fi

  # 5. stage exact paths (only those that exist)
  git add "$QMD" "notebooks_colab/${B}.ipynb" "notebooks_md/${B}.md" book/_book/search.json
  for p in "book/_freeze/notebooks_quarto/${B}" "book/_book/notebooks_quarto/${B}.html" "book/_book/notebooks_quarto/${B}_files"; do
    [ -e "$p" ] && git add "$p"; done
  # guard: nothing outside this chapter (+ search.json) staged
  BAD=$(git diff --cached --name-only | grep -vE "(${B}(\.|_files|/)|search\.json$)" || true)
  if [ -n "$BAD" ]; then echo "!! $CH staged unexpected paths:"; echo "$BAD"; echo "stopping"; exit 1; fi

  # 6. commit
  { echo "Audit $CH: statistical, code, and format corrections"; echo;
    cat "$W/commitmsg/${CH}.txt";
    echo; echo "Verified edits from campaign audit; report-only items in judgment_calls.md.";
    echo; echo "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>";
    echo "Claude-Session: https://claude.ai/code/session_01Bocu8XHCRxQ5z75AoPKCxh"; } > "$W/commitmsg/${CH}_full.txt"
  git commit -q -F "$W/commitmsg/${CH}_full.txt"
  echo "[$CH] COMMITTED $(git rev-parse --short HEAD)"
done
echo "########## DRIVER DONE for: $* ##########"
