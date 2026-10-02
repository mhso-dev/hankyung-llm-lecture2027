#!/bin/bash
# runverify.sh textbook/partN/chXX-slug — run_section.sh와 같은 환경 변수로 verify.py --chapter
ROOT="$HOME/mnt/한국경제신문"; cd "$ROOT"
C="${1%/}"; CH=$(basename "$C")
L=$(python3 -c "import json;print(json.load(open('$C/chapter.json'))['lab_path'])")
VM="$ROOT/.cache/vm"
export UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT="$VM/venv-$CH" HF_HOME="$VM/hf" UV_NO_SYNC=1 PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT/$L/notebooks"
env -u OPENAI_API_KEY timeout 160 uv run --project "$L" python textbook/_notebook/verify.py --chapter "$C" 2>&1 | tail -2
