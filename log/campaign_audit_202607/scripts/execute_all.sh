#!/bin/bash
# Phase 0 driver: execute all chapter notebooks (cap 6 parallel), dump outputs.
set -u
cd /Users/carlosmendez/Documents/GitHub/metricsai
source .venv/bin/activate
WORK=log/campaign_audit_202607

run_one() {
  nb="$1"
  base=$(basename "$nb" .ipynb)
  ch=${base%%_*}
  jupyter nbconvert --to notebook --execute --allow-errors \
    --ExecutePreprocessor.timeout=600 \
    --output-dir "$WORK/exec" --output "${ch}_executed.ipynb" "$nb" \
    > "$WORK/exec/${ch}_nbconvert.log" 2>&1
  rc=$?
  if [ $rc -eq 0 ]; then
    python3 "$WORK/scripts/extract_outputs.py" "$WORK/exec/${ch}_executed.ipynb" \
      > "$WORK/exec/${ch}_outputs.txt" 2>&1
    nerr=$(grep -c '!! ERROR' "$WORK/exec/${ch}_outputs.txt" || true)
    echo "${ch}: nbconvert=OK cell_errors=${nerr}"
  else
    echo "${ch}: nbconvert=FAILED rc=${rc} (see exec/${ch}_nbconvert.log)"
  fi
}
export -f run_one
export WORK

ls notebooks_colab/ch*_*.ipynb | xargs -P 6 -I {} bash -c 'run_one "$@"' _ {}
echo "=== ALL DONE ==="
