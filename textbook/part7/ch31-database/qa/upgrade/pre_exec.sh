# Ch 31 PostgreSQL 준비 — run_section.sh가 절 실행 직전에 source 한다(본: Ch 12·Ch 23 qa/upgrade/pre_exec.sh).
# 교재는 학생에게 챕터 전용 Docker 컨테이너(kdt-ch31-postgres, 이미지 pgvector/pgvector:0.8.1-pg17)를
# 127.0.0.1:55431에만 묶어 켜라고 안내하고, 여섯 절 모두 같은 서버·계정·데이터베이스를 쓴다(연습용 비밀번호 — 03·05·06은 드라이버 부분만 다름).
#   postgresql+asyncpg://postgres:postgres@127.0.0.1:55431/ch31_lab
# 작업 기기에는 Docker가 없어, Ch 12가 둔 conda-forge PostgreSQL 17.11 + pgvector 0.8.1(.cache/vm/pgenv/bin)로
# 이 챕터 전용 클러스터를 연결 폴더 밖 /tmp/ch31-pg/data 에 만들고(없을 때만 initdb·createdb) 같은 접속 글로 켠다.
# 데이터 폴더를 연결 폴더 밖에 두는 까닭: PostgreSQL은 끌 때 postmaster.pid를, 05절 dropdb 때 DB 폴더를 스스로 지운다.
# 여섯 절 모두 DB가 필요해 N 조건 없이 켠다. 두 번 불러도 안전하다:
#   - 이 클러스터가 이미 켜져 있으면(잠금 파일의 PID가 postgres이고 55431이 받음) 다시 켜지 않고 그대로 쓴다(끄기는 처음 부른 셸의 trap이 맡음).
#   - 55431에서 다른 서버가 받고 있으면 그 데이터를 건드리지 않도록 켜지 않고 멈춘다(return 1 → run_section.sh의 set -e로 끝남).
#   - initdb는 PG_VERSION이 없을 때만, createdb는 ch31_lab이 없을 때만 한다.
# 서버는 이 스크립트를 source 한 셸이 끝날 때(trap EXIT) 같은 호출 안에서 끈다(pg_ctl -m fast stop).
# 끈 뒤 확인: pgrep -f "$HOME/mnt/한국경제신문/.cache/vm/pgenv/bin/postgres" 가 아무것도 내지 않아야 한다.
# 직접 부를 때: . textbook/part7/ch31-database/qa/upgrade/pre_exec.sh
CH31_PGBIN="$HOME/mnt/한국경제신문/.cache/vm/pgenv/bin"
CH31_PGDIR=/tmp/ch31-pg
CH31_PGDATA="$CH31_PGDIR/data"
CH31_PGURL="postgresql://postgres:postgres@127.0.0.1:55431/ch31_lab"
# 05절 노트북은 shutil.which("pg_dump")로 백업 명령을 찾는다(없으면 학생 Docker 컨테이너 안의 명령). 작업 기기는 pg_dump가
# PATH에 없어 pgenv bin(pg_dump·pg_restore 17.11 — 서버와 같은 버전)을 PATH 끝에 더한다. 앞에 더하지 않는 까닭: pgenv bin의
# 명령 107개 가운데 openssl·clear·tput·zstd 등이 시스템 명령을 가린다. 끝에 두면 시스템에 없는 명령만 채운다(2026-09-29 05절).
case ":$PATH:" in *":$CH31_PGBIN:"*) ;; *) export PATH="$PATH:$CH31_PGBIN" ;; esac
mkdir -p "$CH31_PGDIR"
# 기기 셸은 호출이 끝나면 그 안의 프로세스를 모두 끝낸다(bwrap --unshare-pid --die-with-parent — 2026-09-29 확인).
# trap이 돌지 못하고 끝난 호출(시간 제한 등)은 postmaster.pid를 남긴다. 호출마다 PID를 1부터 다시 쓰므로
# 남은 잠금 파일 둘(데이터 폴더 postmaster.pid·소켓 폴더 .s.PGSQL.55431.lock)의 PID를 다른 프로세스가 쓰고 있으면
# PostgreSQL이 켜지지 않는다 → 그 PID가 postgres가 아니면 잠금 파일을 지우지 않고 이름만 바꿔 둔다
# (PID가 비어 있으면 pg_ctl·postgres가 스스로 처리한다).
CH31_RUNNING=no
for CH31_LOCK in "$CH31_PGDATA/postmaster.pid" "$CH31_PGDIR/.s.PGSQL.55431.lock"; do
  if [ -f "$CH31_LOCK" ]; then
    CH31_PID=$(head -1 "$CH31_LOCK")
    CH31_COMM=$(cat "/proc/$CH31_PID/comm" 2>/dev/null || true)
    if [ "$CH31_COMM" = "postgres" ] && "$CH31_PGBIN/pg_isready" -h 127.0.0.1 -p 55431 -t 2 >/dev/null 2>&1; then
      CH31_RUNNING=yes
    elif [ -n "$CH31_COMM" ] && [ "$CH31_COMM" != "postgres" ]; then
      mv "$CH31_LOCK" "$CH31_LOCK.stale-$(date +%s)"
    fi
  fi
done
if [ "$CH31_RUNNING" = "yes" ]; then
  echo "pre_exec: Ch 31 클러스터가 이미 켜져 있어 그대로 씁니다." >&2
else
  if "$CH31_PGBIN/pg_isready" -h 127.0.0.1 -p 55431 -t 2 >/dev/null 2>&1; then
    echo "pre_exec: 127.0.0.1:55431에서 다른 서버가 받고 있어 멈춥니다." >&2
    return 1
  fi
  if [ ! -f "$CH31_PGDATA/PG_VERSION" ]; then
    # 비밀번호는 교재·옛 README에 적힌 연습용 값이다(수업 전용 — 다른 곳에 쓰지 않음)
    printf '%s\n' 'postgres' > "$CH31_PGDIR/pwfile"
    "$CH31_PGBIN/initdb" -D "$CH31_PGDATA" -U postgres --pwfile="$CH31_PGDIR/pwfile" \
      --auth-local=trust --auth-host=scram-sha-256 --encoding=UTF8 --locale=C >"$CH31_PGDIR/initdb.log" 2>&1
  fi
  "$CH31_PGBIN/pg_ctl" -D "$CH31_PGDATA" -o "-p 55431 -c listen_addresses=127.0.0.1 -k $CH31_PGDIR" \
    -l "$CH31_PGDIR/pg.log" -w start >/dev/null
  trap '"$CH31_PGBIN/pg_ctl" -D "$CH31_PGDATA" -m fast -w stop >/dev/null 2>&1' EXIT
fi
if ! "$CH31_PGBIN/psql" -h "$CH31_PGDIR" -p 55431 -U postgres -d postgres -tAc \
    "SELECT 1 FROM pg_database WHERE datname = 'ch31_lab'" | grep -q 1; then
  "$CH31_PGBIN/createdb" -h "$CH31_PGDIR" -p 55431 -U postgres ch31_lab
fi
# 학생 글과 같은 TCP 접속 글로 SELECT 1이 될 때까지 열 번까지 기다린다
for CH31_TRY in 1 2 3 4 5 6 7 8 9 10; do
  "$CH31_PGBIN/psql" "$CH31_PGURL" -tAc "SELECT 1" >/dev/null 2>&1 && break
  sleep 1
done
