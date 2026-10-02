# Ch 23 02절 PostgreSQL 준비 — run_section.sh가 절 실행 직전에 source 한다(본: Ch 12 qa/upgrade/pre_exec.sh).
# 교재 02절은 학생에게 Ch 12 02절의 Docker 컨테이너(hankyung-part3-pgvector)를 다시 켜라고 안내하고,
# 같은 접속 글 postgresql://student:…@127.0.0.1:55432/rag_lab 안의 이름 공간 ch23_lab만 쓴다.
# 작업 기기에는 Docker가 없어, Ch 12가 둔 conda-forge PostgreSQL 17.11(.cache/vm/pgenv/bin)로 이 챕터 전용 새 클러스터를
# /tmp/ch23-02/pgdata 에 만들고(없을 때만 initdb·createdb) 교재와 같은 접속 글로 켠다.
# Ch 12 데이터 폴더(.cache/vm/pgdata)는 건드리지 않는다. 55432에서 이미 받는 서버가 있으면(예: Ch 12 서버)
# 그 데이터에 이름 공간을 만들지 않도록 켜지 않고 멈춘다(return 1 → run_section.sh의 set -e로 끝남).
# 서버는 부른 셸이 끝날 때(trap EXIT) 같은 호출 안에서 끈다. 02절이 아닌 절에서는 아무 일도 하지 않는다.
# 직접 부를 때: N=02 . textbook/part6/ch23-persistence/qa/upgrade/pre_exec.sh
if [ "${N:-}" = "02" ]; then
  CH23_PGBIN="$HOME/mnt/한국경제신문/.cache/vm/pgenv/bin"
  CH23_PGDIR=/tmp/ch23-02
  CH23_PGDATA="$CH23_PGDIR/pgdata"
  mkdir -p "$CH23_PGDIR"
  if "$CH23_PGBIN/pg_isready" -h 127.0.0.1 -p 55432 -t 2 >/dev/null 2>&1; then
    echo "pre_exec: 127.0.0.1:55432에서 이미 받는 서버가 있어 멈춥니다(Ch 12 서버일 수 있음)." >&2
    return 1
  fi
  if [ ! -f "$CH23_PGDATA/PG_VERSION" ]; then
    # 암호는 Ch 12 02절 교재·실습 README에 이미 적힌 수업 전용 값이다
    printf '%s\n' 'local-practice-only' > "$CH23_PGDIR/pwfile"
    "$CH23_PGBIN/initdb" -D "$CH23_PGDATA" -U student --pwfile="$CH23_PGDIR/pwfile" \
      --auth-local=trust --auth-host=scram-sha-256 >"$CH23_PGDIR/initdb.log" 2>&1
  fi
  "$CH23_PGBIN/pg_ctl" -D "$CH23_PGDATA" -o "-p 55432 -c listen_addresses=127.0.0.1 -k $CH23_PGDIR" \
    -l "$CH23_PGDIR/pg.log" -w start >/dev/null
  trap '"$CH23_PGBIN/pg_ctl" -D "$CH23_PGDATA" -m fast -w stop >/dev/null 2>&1' EXIT
  if ! "$CH23_PGBIN/psql" -h "$CH23_PGDIR" -p 55432 -U student -d postgres -tAc \
      "SELECT 1 FROM pg_database WHERE datname = 'rag_lab'" | grep -q 1; then
    "$CH23_PGBIN/createdb" -h "$CH23_PGDIR" -p 55432 -U student rag_lab
  fi
fi
