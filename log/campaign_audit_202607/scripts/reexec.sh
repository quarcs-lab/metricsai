#!/bin/bash
set -u
cd /Users/carlosmendez/Documents/GitHub/metricsai
source .venv/bin/activate
W=log/campaign_audit_202607
run_one(){
  ch="$1"; nb=$(ls notebooks_colab/${ch}_*.ipynb)
  jupyter nbconvert --to notebook --execute --allow-errors --ExecutePreprocessor.timeout=600 \
    --output-dir "$W/exec" --output "${ch}_rem.ipynb" "$nb" > "$W/exec/${ch}_rem_nbc.log" 2>&1
  python3 "$W/scripts/extract_outputs.py" "$W/exec/${ch}_rem.ipynb" > "$W/exec/${ch}_rem.txt" 2>&1
  echo "${ch}: errors=$(grep -c '!! ERROR' $W/exec/${ch}_rem.txt)"
}
export -f run_one; export W
echo "$@" | tr ' ' '\n' | xargs -P 6 -I{} bash -c 'run_one "$@"' _ {}
echo "=== reexec done ==="
