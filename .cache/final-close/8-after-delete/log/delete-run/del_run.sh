#!/bin/bash
ROOT=$HOME/mnt/한국경제신문
D=$ROOT/.cache/final-close/7-delete
LOG=$HOME/del_run.log
: > $LOG
n=0; fail=0
while IFS= read -r p; do
  [ -z "$p" ] && continue
  n=$((n+1))
  if rm -rf -- "$p" 2>>$HOME/del_err.log; then
    if [ -e "$p" ] || [ -L "$p" ]; then echo "STILL $p" >> $LOG; fail=$((fail+1)); else echo "OK $p" >> $LOG; fi
  else
    echo "FAIL $p" >> $LOG; fail=$((fail+1))
  fi
done < $D/plan.txt
echo "DONE n=$n fail=$fail" >> $LOG
