# Ch 12 02절 pgvector 준비 — run_section.sh가 절 실행 직전에 source 한다.
# 교재는 Docker 데이터베이스를 쓰지만 이 작업 VM에는 Docker가 없어, conda-forge PostgreSQL 17.4 + pgvector 0.8.1을
# 사용자 디스크(.cache/vm/pgenv)에 두고 같은 접속 정보(127.0.0.1:55432 / student / rag_lab)로 띄운다.
# 기기 셸은 호출이 끝나면 프로세스도 끝나므로 절 실행마다 다시 켠다(자동으로 멈춤).
PGROOT="$HOME/mnt/한국경제신문/.cache/vm"
if [ -x "$PGROOT/pgenv/bin/pg_ctl" ]; then
  "$PGROOT/pgenv/bin/pg_ctl" -D "$PGROOT/pgdata" -o "-p 55432 -c listen_addresses=127.0.0.1" -l /tmp/pg-ch12.log start >/dev/null 2>&1 || true
  for i in 1 2 3 4 5 6 7 8 9 10; do
    "$PGROOT/pgenv/bin/psql" "postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab" -tAc "SELECT 1" >/dev/null 2>&1 && break
    sleep 1
  done
fi
