#!/bin/bash
# genmatch_all.sh TEXTBOOK_CH LAB NN... — 절마다 노트북의 실행 날짜 줄을 읽어 UPGRADE_RUN_DATE로 주고 genmatch.py를 따로 돌린다.
ROOT="$HOME/mnt/한국경제신문"; cd "$ROOT"; W="$ROOT/.cache/final-close/2-tools-head"
T="$1"; L="$2"; shift 2
for n in "$@"; do
  nb=$(ls $L/notebooks/$n-*.ipynb | head -1)
  d=$(python3 -c "
import json,re,sys
nb=json.load(open(sys.argv[1],encoding='utf-8'))
for c in nb['cells']:
    s=c['source'] if isinstance(c['source'],str) else ''.join(c['source'])
    m=re.search(r'이 노트북의 출력은 (\d{4}-\d{2}-\d{2})에', s)
    if m: print(m.group(1)); break
" "$nb")
  echo -n "[date ${d:-none}] "
  UPGRADE_RUN_DATE=${d:-} PYTHONDONTWRITEBYTECODE=1 python3 $W/tools/genmatch.py "$T" "$L" "$n" 2>&1 | tail -8
done
