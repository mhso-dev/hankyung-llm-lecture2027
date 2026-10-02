#!/bin/bash
# 사용: bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch02-python 03 [--no-exec]
#   생성기 실행 → 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트(wip)
# 준비물: /tmp/mmd(mermaid-cli), /tmp/libs(libXdamage) — textbook/_notebook/mermaid/README.md
set -e
ROOT="$HOME/mnt/한국경제신문"; cd "$ROOT"
C="${1%/}"; N="$2"; MODE="$3"
CH=$(basename "$C")
if [ -f "$C/chapter.json" ]; then
  L=$(python3 -c "import json;print(json.load(open('$C/chapter.json'))['lab_path'])")
else
  L="labs/${C#textbook/}"
fi
export UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=/tmp/venv-$CH
# 큰 챕터(torch·로컬 모델): 루트 디스크가 좁아 가상환경·uv 캐시·모델을 마운트 폴더의 .cache/vm(.gitignore의 .cache/)에 둔다
VM="$ROOT/.cache/vm"
if [ -d "$VM/venv-$CH" ]; then
  # uv 캐시는 /tmp에 둔다. 마운트 폴더에 두면 `--with` 임시 환경을 지울 때 Operation not permitted로 멈춘다(2026-09-18, Ch12 05절).
  export UV_PROJECT_ENVIRONMENT="$VM/venv-$CH" HF_HOME="$VM/hf"
  # 마운트 폴더는 삭제가 막혀 uv sync가 기존 파일을 지우려다 실패한다. 이미 만든 환경은 그대로 쓴다.
  # 의존성을 새로 넣어야 하면 직접: uv pip install --python "$VM/venv-$CH/bin/python" <패키지>
  export UV_NO_SYNC=1
fi
export PUPPETEER_CACHE_DIR=/tmp/pptr-cache
ARCH=$(uname -m); [ "$ARCH" = "aarch64" ] && LIBARCH=aarch64-linux-gnu || LIBARCH=x86_64-linux-gnu
export LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/$LIBARCH
NB=$(ls $L/notebooks/$N-*.ipynb 2>/dev/null | head -1 || true)
# §2-7 도구 파일(llm_tools.py·rag_tools.py)은 노트북 폴더에 둔다. 학생 커널은 노트북 폴더에서 시작해 바로 가져오지만,
# execute.py는 저장소 루트에서 커널을 띄우므로 노트북 폴더를 가져오기 경로에 더한다(2026-09-21, Ch 5 §2-7 리팩터).
export PYTHONPATH="$ROOT/$L/notebooks${PYTHONPATH:+:$PYTHONPATH}"
# 절 실행 전 준비 훅(예: Ch 12 pgvector 서버 띄우기). 기기 셸은 호출이 끝나면 백그라운드 프로세스도 끝나므로 같은 호출 안에서 켠다.
[ -f "$C/qa/upgrade/pre_exec.sh" ] && . "$C/qa/upgrade/pre_exec.sh"
if [ "$MODE" != "--no-exec" ]; then
  if [ -f "$C/qa/upgrade/author_$N.py" ]; then python3 "$C/qa/upgrade/author_$N.py"; else python3 "$C/qa/upgrade/author_upgrade.py" "$N"; fi
  NB=$(ls $L/notebooks/$N-*.ipynb | head -1)
  uv run --project "$L" --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip --with python-dotenv==1.2.3 \
    python textbook/_notebook/execute.py "$NB" 2>&1 | grep -E "PASS|FAIL|Error|Traceback" || true
fi
python3 textbook/_notebook/mermaid/render_mermaid.py "$C" --only "$N-"
uv run --project "$L" --with pillow python textbook/_notebook/mermaid/attach_figures.py "$NB" "$C/figures"
(cd "$C" && uv run --project "$ROOT/$L" --with pillow python _build.py >/dev/null)
if [ -f "$C/chapter.json" ]; then
  uv run --project "$L" python textbook/_notebook/verify.py --chapter "$C" 2>&1 | tail -1
fi
python3 textbook/_notebook/checks/upgrade_gates.py "$C" --label wip --section "$N" | tail -1
