#!/bin/bash
LOG=$HOME/del_run2.log
while IFS= read -r p; do
  [ -z "$p" ] && continue
  if [ -e "$p" ] || [ -L "$p" ]; then
    rm -rf -- "$p" 2>>$HOME/del_err.log
    if [ -e "$p" ] || [ -L "$p" ]; then echo "STILL $p" >> $LOG; else echo "OK $p" >> $LOG; fi
  fi
done < $HOME/plan_copy.txt
echo DONE >> $LOG
