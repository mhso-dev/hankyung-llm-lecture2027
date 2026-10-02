#!/bin/bash
# runcopy.sh CH_SLUG LAB_DIR COPY_NOTEBOOKS_DIR NB_BASENAME... — 사본 노트북을 새 커널로 실행(키 없이). 사본만 바꾼다.
ROOT="$HOME/mnt/한국경제신문"; cd "$ROOT"
CH="$1"; L="$2"; C="$3"; shift 3
VM="$ROOT/.cache/vm"
export UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT="$VM/venv-$CH" HF_HOME="$VM/hf" UV_NO_SYNC=1 PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$C"
CWD="${COPY_CWD:-$C}"
for nb in "$@"; do
  env -u OPENAI_API_KEY timeout 160 uv run --project "$L" --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip --with python-dotenv==1.2.3 \
    python textbook/_notebook/execute.py "$C/$nb" --cwd "$CWD" 2>&1 | grep -E "PASS|FAIL|Error|Traceback|error" | head -5
done
