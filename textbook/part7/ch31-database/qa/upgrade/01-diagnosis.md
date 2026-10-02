# 01절 진단 — SQLAlchemy 비동기 PostgreSQL (experiment)

- 작업일 2026-09-29 · 생성기 `qa/upgrade/author_01.py`(`3d310dcd…`) · 노트북 `labs/part7/ch31-database/notebooks/01-SQLAlchemy-비동기-PostgreSQL.ipynb` · 본문 `_src/01-SQLAlchemy-비동기-PostgreSQL.html` · DB 준비 훅 `qa/upgrade/pre_exec.sh`(`8a9529f1…`, 이 절이 새로 만듦 — 다섯 절 공통).
- 읽은 것: 준비 노트 `chapter-lead-notes.md`(전부) · `AGENT-BRIEF.md`·`PLAYBOOK.md` · 규격 `QUALITY-UPGRADE.md`(전부) · 과정 요약(§0~§9) · 계약 §3 Ch 30 줄·§5 Part 7 묶음·§6 pgvector · Ch 30 `chapter-summary.md`(전부)·`handoff.md` 챕터 공통 · 본 Ch 12·Ch 23 `pre_exec.sh` · Ch 30 `author_01.py`·`author_04.py`(머리) · Ch 25 `author_03.py`(시간 처리) · Ch 2 12 노트북(`perf_counter`·`gather` 모양) · Ch 4 03·Ch 23 02 `_src`(말). `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전(`gates-before.json`) | 5 | 84 | 3 | 1 | 3 | 0 | 7 | 20 | 3 | 37 |
| 첫 실행 전(`gates-wip-01-01.json`, G1·G2 먼저) | 21 | — | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 3(그림 없음) |
| 후(`gates-wip-01.json`, `--no-exec`) | **21** | **387** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

- AST 따로(`.cache/ch31-01/tools/extra_check.py`(Ch 30 판을 옮김)): 걸린 것은 셀 맨 위 `await`·`async def` 하나(`read_question`)뿐 — 챕터 허용 범위. 호출 깊이 최대 2 · 준비 셀 밖 셀 최대 9줄 · 코드 줄 108(주석·빈 줄 뺌, 옛 판 47).
- 금지어(`.cache/ch31-01/tools/ban31.py` = Ch 30 `ban30.py` 목록 + 「순차」·「동시성」·「식당」·「은행」·「창고」·「요청 함수」·「경로 함수」·「레코드」·「되돌려」·「되돌립」·「돌려」·「롤백」·「스키마」·「세션」·「쿼리」): `_src`·노트북 마크다운·코드 주석·`.mmd` 넷·캡션 다섯 모두 0 — 걸린 것은 「이벤트 루프」(Ch 2 12 말, 허용) 넷뿐. 사용자가 금지한 표현(과정 규칙) 0.
- 인용 대조(`.cache/ch31-01/tools/quotes.py`): 노트북 백틱 101개·`_src` `<code>` 63개 가운데 출력·코드에 없는 것은 명령·파일 이름·API 이름뿐(`uv sync --locked`·`kdt-ch31-postgres`·`.env`·`commit()`·`asyncio.gather()` 등).

## 수정 전 주요 문제 (옛 판 — `before/notebooks/01-…ipynb`·`before/_src/01-*.html`)

1. **걸린 초에 건 `assert`** — `assert sequential == concurrent and concurrent_s < sequential_s`(규격 §3 — 매번 같은 값에만) · 초 값을 b6·b8 결론·복습에 씀(「순차 약 0.46초, 동시 약 0.20초」).
2. 문법: `[await read_question(i) for i in range(1, 4)]`(내포식) · `asyncio.gather(*(delayed_read(i) for …))`(별표 풀기 + 제너레이터 식) · `item_id: int`·`-> str`(힌트·반환 힌트) · f-string 형식 지정 · `import asyncio`를 본 셀에서 · 한 셀 15줄 넘음([13] 16줄).
3. 접속 글: `os.getenv("CH31_DATABASE_URL", …localhost…)` — 노트북은 `.env`를 읽지 않음(README 문장은 거짓, 마감 몫) · `SYNC_URL`·`NATIVE_URL`을 01에서 만들고 쓰지 않음.
4. 설명 셀: 첫 줄 주석 0 · 결과 읽기 0 · 제목 셀 「운영 데이터베이스의 한 가지 문제를 재현하고 해결합니다」(다섯 절 같은 틀 문장 — experiment인데 「해결」) · 「이 준비 셀이 하는 일」 틀 단락.
5. 말: 「세션」 21·「쿼리」·「순차」·「반환」·「측정」·「지연」·「팩터리」·「체크아웃」 · b2 「Ch30에서 FastAPI 요청 함수」·b3 「경로 함수」(Ch 30 말은 「처리 함수」, 「경로」는 금지어) · 비유 「식당 주문 담당자」(Ch 19 「식당 주문 전표」 계열과 겹침).
6. b6 「Docker의 독립 PostgreSQL 17.8 컨테이너와 작은 데이터에서 측정」(다섯 절 공통 틀 문장) · b4 「운영에서 경계를 정하는 방법」(실행하지 않은 운영 설명 긴 단락) · b7 「동기 드라이버가 이벤트 루프를 멈춤」(실행 안 한 설명 — 한정 없음).
7. 그림: `{{svg:01-흐름}}` 한 장(푸른·붉은·초록·보라 상자를 처리 단계로 — 실패 아닌 요소에 빨강), Mermaid·삽화 0.
8. 옛 README Docker 명령 `-p 55431:5432` — 모든 주소에 열림(Docker 문서 「Publishing container ports is insecure by default」).

## 바꾼 것

- **experiment 구성**: 가설(5절) → 실행 1(6절 — `engine.dispose()`로 빈 풀 → await 줄 셋으로 차례로) → 실행 2(7절 — 같은 준비 → **바꾼 값 하나: 기다리는 방법**, 코루틴 셋을 만들기만 한 뒤 `asyncio.gather(first_waiting, second_waiting, third_waiting)` — 별표 풀기 없이 Ch 2 12 모양) → 결과 표(8절) → 참·거짓 비교 → 9절 정리(이름 공간 지우기·풀 비우기).
- **결론 = 매번 같은 값 + 부등식**: 받은 값 목록 `['환불', '배송', '결제']` 같음 · 기록 앞 세 개 `시작 1·끝 1·시작 2` ↔ `시작 1·시작 2·시작 3` · 끝난 뒤 풀에 쉬고 있는 연결 수 `1` ↔ `3` · `함께 기다린 시간이 더 짧은가: True`. **초 값은 결과 읽기 둘째 단락·b6 표·「확인할 점」·b7에만**(규격 §2-7 9번 끝·Ch 25 03 선례) — 그림 라벨·캡션·alt·b8·복습에 초 없음. 시간 `assert` 0.
- 첫 풀이(뜻 → 일상 예 → 코드): 비동기 엔진·드라이버·연결·연결 풀·SQL 글 객체(새 용어 5 — meta 4 → 5) · 풀이만: `engine.begin()`(Ch 4 03 커밋 이음)·값 자리 `:id`(Ch 4 03 물음표 자리)·`pg_sleep`·`fetchone`·`fetchall`·`scalar_one`·`rowcount`·`dispose()`·`to_regnamespace`·`pool.size()`/`checkedin()`/`checkedout()`.
- 이름 공간(Ch 23 02 말) `ch31_async`: 3절 `DROP SCHEMA IF EXISTS … CASCADE` → `CREATE SCHEMA` → `CREATE TABLE` → `INSERT` 세 줄(한 `begin` 블록) · 9절 `DROP SCHEMA` + `to_regnamespace` → `None`. 다시 실행해도 같은 출력(같은 커널 세 번 확인).
- 접속 글은 2절 설정 셀에 한 번, 연습용 값 그대로: `postgresql+asyncpg://postgres:postgres@127.0.0.1:55431/ch31_lab`(`localhost` → `127.0.0.1` — Docker 명령을 127.0.0.1에만 묶었기 때문) · 출력은 드라이버 부분과 `@` 뒤만(비밀번호 안 찍음).
- 학생 DB 명령(제목 셀 준비물): `docker run --name kdt-ch31-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=ch31_lab -p 127.0.0.1:55431:5432 -d pgvector/pgvector:0.8.1-pg17`(계정 줄은 이미지 기본값과 같은 값을 드러낸 것) · `docker start kdt-ch31-postgres` · 판 가름 「교재 출력은 … PostgreSQL 17.11 서버로 만들었습니다. 그 서버는 Docker 컨테이너가 아니라, 같은 접속 글로 켠 서버입니다」·「Docker 이미지로 켜면 서버 판 번호의 끝자리가 다를 수 있습니다」.
- b2 「처리 함수를 `async def`로 적었습니다」(Ch 30 01 링크 — 「요청 함수」·「경로 함수」 뺌) · b2에 챕터 제목(DB·상태 영속화 = Ch 23 상태 저장)·절 제목(SQLAlchemy·PostgreSQL) 풀이 · b3 Ch 2 12·Ch 4 03·Ch 12 02·Ch 23 02·Ch 28 01·Ch 30 03 링크 · b10 새로(SQLAlchemy asyncio·Engines and Connections·Connection Pooling·PostgreSQL 17 Delaying Execution·Docker Port publishing, 확인 2026-09-29).
- 비유 계열 **「전화 교환대」**를 엶(판 = 연결 풀, 꽂는 자리 셋 = `pool_size=3`, 꽂힌 선 = 연결, 켜진 불 수 = 끝난 뒤 쉬고 있는 연결 수) — b4 「비유와 다른 점」(실제 연결은 쓰지 않는 동안에도 풀에 남음).
- ORM(`DeclarativeBase`·`Mapped`·`AsyncSession`·`async_sessionmaker`)은 이 절에서 쓰지 않음(Core `text()`로 충분 — handoff 「문법 범위」).

## DB 준비 — `qa/upgrade/pre_exec.sh` (챕터 리드 결정 1)

- **요지**: `.cache/vm/pgenv/bin`(Ch 12가 둔 conda-forge PostgreSQL 17.11 + pgvector 0.8.1)로 챕터 전용 클러스터를 **연결 폴더 밖 `/tmp/ch31-pg/data`**에 둠. `PG_VERSION`이 없을 때만 `initdb -U postgres --pwfile`(연습용 비밀번호 `postgres`, `--auth-local=trust --auth-host=scram-sha-256 --encoding=UTF8 --locale=C`) → `pg_ctl … -o "-p 55431 -c listen_addresses=127.0.0.1 -k /tmp/ch31-pg" -w start` → `trap … pg_ctl -m fast -w stop … EXIT` → `ch31_lab`이 없을 때만 `createdb` → 학생 글과 같은 TCP 접속 글로 `SELECT 1`이 될 때까지 열 번까지 기다림. **다섯 절 모두**(`N` 조건 없음).
- **데이터 폴더 자리**: 연결 폴더(`.cache/vm/pgdata-ch31`)는 시험하지 않고 `/tmp`를 골랐습니다. PostgreSQL은 끌 때 `postmaster.pid`를, 05의 `dropdb` 때 DB 폴더를 스스로 지우는데, 연결 폴더는 지우기가 막힌 자리이고 지울 수 없는 40MB 남짓을 사용자 디스크에 남기게 됩니다. `/tmp`는 준비 담당이 이미 돌린 자리(Ch 23 선례)이고 이번에도 돌았습니다. 기기가 다시 만들어지면 훅이 `initdb`부터 다시 합니다. 크기 46MB(기기 루트 디스크).
- **두 번 불러도 안전한지(확인함)**: 같은 셸에서 두 번 source → 둘째는 「Ch 31 클러스터가 이미 켜져 있어 그대로 씁니다」(잠금 파일의 PID가 postgres이고 55431이 받을 때) · `initdb`·`createdb`는 없을 때만 · 55431에서 다른 서버가 받으면 켜지 않고 `return 1`(run_section.sh `set -e`로 끝남 — Ch 23 선례).
- **기기 셸의 성질(확인함)**: 호출이 `bwrap --unshare-pid --die-with-parent`로 돌아, **셸 호출이 끝나면 postgres도 끝남**(trap 없이 켠 서버가 다음 호출에서 프로세스 0·포트 0). 다만 이때는 깨끗이 끄지 못해 `postmaster.pid`와 소켓 잠금 파일 `.s.PGSQL.55431.lock`이 남고, **다음 호출이 PID를 1부터 다시 쓰므로 그 PID를 다른 프로세스가 쓰면 PostgreSQL이 켜지지 않음**(`sleep`으로 PID를 채워 재현 — `lock file … already exists`). 훅은 두 잠금 파일의 PID 프로세스 이름이 `postgres`가 아니면 파일을 **지우지 않고 이름만 바꿈**(`….stale-<초>`), PID가 비어 있으면 PostgreSQL이 스스로 처리(`pg_ctl: another server might be running; trying to start server anyway` 뒤 켜짐). 두 경우 모두 재현해 켜짐을 확인.
- **끄기와 남은 프로세스**: 정상 경로는 trap이 `pg_ctl -m fast -w stop`(로그 `database system is shut down`). 모든 호출 뒤 `ps -eo comm | grep -c '^postgres$'` = **0**, `ss -ltn | grep 55431` = **0**. 시험으로 생긴 이름 바꾼 잠금 파일 둘(`/tmp/ch31-pg/postmaster.pid.stale-1790696180`·`/tmp/ch31-pg/.s.PGSQL.55431.lock.stale-1790696204`)은 지우지 않음.
- `--no-exec`도 훅을 source 하므로 서버를 켰다 끕니다(빌드에는 필요 없으나 해 없음 — Ch 23과 같음).

## 설치판 동작 확인 (모델 없이 — `.cache/ch31-01/exp/e1_shape.py`, 가상환경 `.cache/vm/venv-ch31-database`)

- 판: sqlalchemy 2.0.43 · asyncpg 0.30.0(잠금 그대로) · 서버 `17.11` · 엔진 `AsyncEngine`·풀 `AsyncAdaptedQueuePool`·연결 `AsyncConnection`·결과 `CursorResult`·줄 `Row`·SQL 글 `TextClause`.
- 여섯 번 실행: 실행 1 `['환불', '배송', '결제']`·`[('시작', 1), ('끝', 1), ('시작', 2)]`·연결 1 · 실행 2 같은 목록·`list`·`[('시작', 1), ('시작', 2), ('시작', 3)]`·연결 3 · 같은가 `True`·짧은가 `True` · 정리 `None`·`0` — **여섯 번 모두 같음**. 걸린 초 실행 1 0.47~0.48 · 실행 2 0.19~0.20. **실행 2의 끝 차례는 실행마다 달랐음**(`끝 2·3·1`·`2·3·1`·`1·3·2`·`2·1·3`·`1·3·2`·`2·3·1`) → 노트북은 기록 앞 세 개만 출력.
- 같은 커널 세 번 이어 실행(`/tmp/ch31-01/try/samekernel-x3.ipynb` — 코드 셀을 세 번 이어 붙인 사본, PASS 63셀): 세 번 모두 연결 1 ↔ 3·기록 앞 세 개·`True`·`True`·`None`, 걸린 초 0.48 ↔ 0.19.
- `pg_sleep(:seconds)`에 파이썬 `0`·`0.15`를 넘겨도 됨(asyncpg가 서버에 자리 자료형을 물어 맞춤) · `DROP SCHEMA IF EXISTS`의 알림(NOTICE)은 출력에 나오지 않음.
- 문서 대조(WebFetch 2026-09-29): SQLAlchemy asyncio — 「The AsyncEngine delivers an AsyncConnection via its AsyncEngine.connect() and AsyncEngine.begin() methods」·「A single instance of AsyncSession is not safe for use in multiple, concurrent tasks」·`dispose()` 팁 / Engines and Connections — 블록이 끝나면 「released to the connection pool」·`begin()`은 끝에서 커밋, 예외면 롤백 / Pooling — `pool_size`·`max_overflow` 뜻·「AsyncAdaptedQueuePool … used automatically when using create_async_engine()」 / PostgreSQL 17 9.9.6 — 「The sleep delay will be at least as long as specified」 / Docker — 「Publishing container ports is insecure by default」·`-p 127.0.0.1:8080:80`.
- **문서와 설치판이 다를 수 있는 곳**: 준비 노트 e2 — `AsyncSession` 하나를 `gather` 두 작업이 함께 써도 이 설치판에서는 오류가 나지 않았음. 이 절은 그 장면을 실행하지 않고 b7에 「문서는 안전하지 않다고 적음·작업마다 따로 쓰라고 함 — 이 절은 작업마다 연결을 따로 빌렸음」으로만 적음.

## 실행 (새 커널)

- 첫 실행 전 `/tmp/ch31-01/try` 사본으로 `execute.py`(PASS 21셀) — 실습 폴더에 `.failure.json`이 남지 않게.
- **A**: `env -u OPENAI_API_KEY PYTHONDONTWRITEBYTECODE=1 bash run_section.sh textbook/part7/ch31-database 01` — 프로젝트 맨 위 커널, **2026-09-29T15:54:38Z**, PASS 21셀(그림 첨부 단계에서 멈춤 — 01-1 PNG가 아직 없어서, 실행·저장은 끝난 뒤) · `code_sha256` **`addb4391b06f908698e09fd0583ce97d8074c5a4d2f8ae93fdd6a62d1f505a53`** · `outputs_sha256` `145e0cf355cd5daf0ae271dc8e51bb7d538628d4c2c6f0f3668eee8368d69c91`.
- **B**(그림 전): 저장 노트북 사본 `/tmp/ch31-01/runB/`를 `execute.py --cwd labs/part7/ch31-database/notebooks`(학생 커널 자리), 15:54:53Z, PASS 21셀 · `code_sha256` 같음 · `outputs_sha256` `c63727fa…`.
- **셀별 출력 대조: 21개 가운데 19개 같음.** 다른 둘은 걸린 초가 찍힌 셀 — [13] `걸린 시간(초): 0.48`(A) ↔ `0.47`(B) · [19] 표의 차례로 줄 `0.48` ↔ `0.47`. 실행 2 [17] `0.19`는 두 번 같음. **부등식 `함께 기다린 시간이 더 짧은가: True`는 두 커널 모두 참.**
- 결과 읽기 둘째 단락·b6 표·확인할 점의 초는 A 출력(`0.48`·`0.19`)을 `mdpatch.py`로 채움(`[[T1]]`·`[[T2]]` — 재실행 없이 마크다운만, 노트북 해시 그대로).
- 실습 폴더에 새로 생긴 파일 0(노트북 01 말고) · `__pycache__` 0 · 커널 작업 폴더에 파일 쓰기 0.

## 걸린 시간 처리 (챕터 리드 결정 4 · Ch 25 03 선례)

- 결론(b6 셋째 단락·b8·노트북 정리·복습·그림)은 **부등식 `True`와 매번 같은 값**만. 초는 6·7절 결과 읽기 둘째 단락(「이번 실행에서는 `걸린 시간(초): 0.48`이었습니다」)·8절 둘째 단락·b6 표 「걸린 시간(초, 교재 출력 — 다시 실행하면 달라짐)」 줄·「확인할 점」·b7(노트북 밖 범위)에만.
- 결정적 예상값 `차례로 기다리면 적어도 걸릴 초: 0.45`(0.15 × 3, `round` — PostgreSQL 문서 「at least as long as specified」)는 결과 읽기 첫 단락에 둠(셈한 값이라 매번 같음).

## 옛 생성기 막기 (챕터 리드 결정 9)

| 파일 | 전 sha256 | 후 sha256 | 한 일 |
|---|---|---|---|
| `qa/author_ch31.py` | `1755fcec…` | `79bf670c…` | `from __future__` 줄 뒤에 설명 주석 셋 + `raise SystemExit(…)`(실행하면 종료 코드 1·안내 글 — 확인) |
| `figures/_gen_figures.py` | `dc2d8216…` | `34448715…` | 같음 |
- 사본 `/tmp/ch31-01/gen-before/`와 `diff` — 더한 네 줄뿐. `before/generators/`의 사본(준비 담당)과 전 해시 같음. 챕터·실습 폴더에 `_generate.py` 없음. `.moai` part7 셋은 Ch 30 01이 막은 판 그대로(`f60d7287…`·`8cb946ea…`·`b171658f…`). 옮기기는 마감 몫(Part 7 `check_figures.py` 20행이 `_gen_figures.py` 존재를 봄).

## 고친 틀린 사실

1. 시간 `assert`와 초 값을 결론·정리·복습에 쓴 것 → 부등식·매번 같은 값으로.
2. b2·b3 「Ch30 요청 함수·경로 함수」 → 「처리 함수」(Ch 30 요약 §19).
3. b6 「Docker의 독립 PostgreSQL 17.8 컨테이너에서 측정」 → 교재 출력 판(17.11, Docker 없이 같은 접속 글) · 학생 이미지 판 가름.
4. `os.getenv("CH31_DATABASE_URL")` — 노트북은 `.env`를 읽지 않으므로 환경 변수 기본값 글이 사실상 늘 쓰였음 → 셀에 연습용 값 한 번(README 「`.env`의 `CH31_DATABASE_URL`」 문장은 마감 몫).
5. b7 「동기 드라이버가 이벤트 루프를 멈출 수 있습니다」(한정 없음) → 「Ch 30 01절이 노트북 밖에서 본 차단 호출과 같은 까닭이고, 이 절에서는 실행하지 않았습니다」.
6. b7·복습 2 「세션을 공유하면 트랜잭션 상태가 섞일 수 있습니다」(실행 안 한 단정) → 문서 근거로만(「AsyncSession 하나를 여러 작업이 함께 쓰면 안전하지 않다고 적음」) + 이 절은 작업마다 연결을 따로 빌렸다고 한정.
7. Docker 명령이 모든 주소에 포트를 엶 → `-p 127.0.0.1:55431:5432`(노트북 준비물 — README는 마감 몫).

## 그림

- Mermaid **4장**(설계표 `01-figures.md`를 렌더 전에 씀): 01-1 엔진과 연결 풀(b4·노트북 오늘 볼 그림, viewBox 폭 **521**) · 01-2 이름 공간 준비와 확정(b5, 318 × 928) · 01-3 연결 하나로 차례로 기다린 실행 1(b5, 246) · 01-4 차례로와 함께 견주기(b6, **597**). 모두 868 이하 · `flowchart TB` · subgraph 제목 `<br>` 없음 · 라벨 대괄호·따옴표 없음 · 개수는 한글 · 노드 7개 이하 · `%% classes`. 첫 렌더에서 자동 줄바꿈이 생긴 네 라벨을 `<br>`로 미리 나눠 다시 렌더(PNG를 직접 열어 확인). **보라 0 · 빨강 0**. 라벨·캡션·alt에 걸린 초 없음(부등식은 `True`로만).
- 삽화 1장 **01-5 불이 하나 켜진 판과 셋 켜진 판**(b4 비유 뒤, 본문만): 1차 job `3d304f8c-ae4f-4151-9dd1-9f8356fe351f` 탈락(판 아래 선 고리가 여럿 늘어져 「꽂힌 선 하나」를 세기 어려움) → **2차 job `55814eca-21ec-4435-9945-4f45614baf2a` 채택**(재생성 1회). 거래 15:57:33Z·15:58:41Z 「Nano Banana Pro −2」 두 줄 = **이 절 몫 4크레딧**(잔액 2265 → 2261, 바로 앞 거래 12:29:22Z는 Ch 30 10). 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만). 저장 PNG 1100 × 614 `98fad365…`, 결과를 다시 받아 같은 폭으로 줄인 그림과 **픽셀 차이 0**. 그림에서 센 것: 판 둘 · 판마다 불 셋·자리 셋 · 왼쪽 선 하나·켜진 불 하나 · 오른쪽 선 셋·켜진 불 셋 · 선 모두 넷. 거의 흰 가로줄 172/614(위아래 여백 약 4분의 1 — 강사 확인) · 두 판 바깥 모서리가 가장자리에서 조금 잘림. 세부 `figures/01-5-…prompt.md`.

## 검사

- 게이트 G1~G7 0(`gates-wip-01.json`) · `verify.py --chapter` **PASS 5 sections / 43 code cells (max 25 lines)**(최대 25줄은 손대지 않은 05 옛 셀) · 빌드 HTML `01-SQLAlchemy-비동기-PostgreSQL.html` `{{`·`[[` 0 · review-pack `qa/upgrade/review-pack/01-SQLAlchemy-비동기-PostgreSQL.md`.
- 화면 검사 `visual.cjs`는 이 절에서 돌리지 않음(마감 몫).

## 완료 챕터 문장 참·거짓 (이 절 쪽 조건 — 고치지 않음)

- **Ch 30 10 b8**(`_src`·HTML·노트북 [44]) 「Ch 31 ↗은 PostgreSQL 데이터베이스에 표를 만들어 쓰는 방법과 체크포인터를 다룹니다」 — 링크 `ch31-database/01-SQLAlchemy-비동기-PostgreSQL.html` **그대로 있음**(슬러그 고정) · 01이 표를 만들어 씀 **참** · 체크포인터 부분은 05 몫(05에 체크포인터 저장 유지 — handoff).
- Ch 30 06 b7·10 b8 「보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다」 — 01에 SSE 0 **참**.
- Ch 30 `author_09.py` 688행 링크 상수 `L_CH31_01` — 슬러그 같음 **참**.
- Part 7 목차(`textbook/part7/index.html`) 01 링크 — 슬러그 같음.

## 챕터 밖 수정

- 없음. (공용 도구·Part 7 파일·다른 챕터 파일 0. `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json`은 `verify.py --chapter`가 다시 쓴 챕터 계약 파일.)

## 강사 확인 대상

1. **pgembed·SQLite 대체를 쓰지 않음**(챕터 리드 결정 1 — pgembed는 딸린 `psql` 세그폴트·맥 휠 제한(Apple Silicon·macOS 15 이상)·AGPL 확장 동봉, SQLite로는 비동기 드라이버·연결 풀·Alembic·pgvector를 보일 수 없음). 학생은 Docker 컨테이너 하나.
2. 제목의 영어 「SQLAlchemy」·「PostgreSQL」과 챕터 제목 「DB & 상태 영속화」(`&`)는 제목에 두고 본문 첫 자리(1절·b2)에서 풂.
3. **코드 양**: 코드 셀 5 → 21, 코드 줄 47 → 108(experiment 한 절 — 가설·실행 둘·표·정리를 셀로 나눔).
4. 걸린 시간을 실제로 잰 절(주제 절 예외)이고, 결론은 부등식 `True`와 매번 같은 값만(Ch 25 03 선례).
5. 삽화 위아래 흰 여백 약 4분의 1(재생성 한도를 써 선 개수가 맞는 2차 채택).
6. 학생 Docker 명령에 `-e POSTGRES_USER=postgres`를 드러내 적음(이미지 기본값과 같은 값).

## 남은 것 (마감 몫)

- README 다시 쓰기(`docker run -p 127.0.0.1:55431:5432 …`·`.env` 문장 빼기·`uv sync --locked`·`notebooks/`에서 열기·절마다 이름 공간·모델 요청 0) · `app/db.py`·`migrations/env.py`의 기본 접속 글 `localhost`(노트북이 열지 않음 — 마감 판단).
- 옛 생성기 둘 `mv -n` → `qa/upgrade/before/generators/blocked/`(Part 7 `check_figures.py` 20행 충돌) · 옛 그림 `figures/01-흐름.{svg,excalidraw,caption.md}` 삭제 승인 목록.
- `qa/verification.md`·`집필점검표.md` 머리에 「개선 전 판」 표시(이번에는 끝에 「품질 개선」 절만 더함).
- 06 실습 절·묶음·공개 목록 — 01은 공개 목록 줄 변화 없음(노트북 파일 이름 같음, 도구 파일 없음).

## 지우지 않은 것 (삭제 승인 대상 — 이 절이 만든 것)

- **기기 VM이 작업 끝 무렵(16:07Z 안팎) 다시 시작되어 `/tmp` 전체가 비었습니다**(`uptime` 2분 — 이 절이 지운 것 아님). 그래서 기기 `/tmp/ch31-01/`(탐색·사본 실행·삽화 원본·옛 생성기 사본, 약 12MB)와 준비 담당의 `/tmp/ch31-prep`, 공용 `/tmp/mmd`·`/tmp/libs`·`/tmp/pptr-cache`·`/tmp/uv-cache`가 없어졌습니다. 도구 스크립트(`ban31.py`·`extra_check.py`·`pregate.py`·`cmpout.py`·`quotes.py`·`dump.py`·`runcopy.sh`)와 노트북 밖 확인 파일(`exp/e1_shape.py`)은 같은 내용으로 연결 폴더 **`.cache/ch31-01/`**에 다시 두었습니다. `/tmp/ch31-pg/`는 재시작 뒤 훅이 `initdb`부터 다시 만들어 켜짐을 확인(서버 17.11·`ch31_lab`, 끈 뒤 프로세스 0·포트 0, 46MB — **02~05가 계속 씀**). 지우지 않은 것(삭제 승인 대상): 연결 폴더 `.cache/ch31-01-view/`(PNG 여섯, 약 2MB — 그림 확인 사본)·`.cache/ch31-01/`(도구·확인 파일) · `qa/upgrade/gates-wip-01-01.json`·`gates-wip-01.json` · 기기 `/tmp/ch31-pg/`.
- 준비 담당이 남긴 `/tmp/ch31-prep`(데이터 폴더 둘 포함)·`.cache/vm/pgembed-try`는 건드리지 않음.

## 디스크

- 기기 루트 여유: 작업 전 1.3G → 그림 작업 뒤 **1.2G**(`/tmp/ch31-pg` 46M·`/tmp/ch31-01` 12M 몫) → 마지막 확인 3.6G(VM 재시작으로 `/tmp`가 비어서 — 이 절은 아무것도 지우지 않음) · 사용자 디스크(연결 폴더) 여유 약 69G.

## 보호 파일 (`before-manifest.json` 209개)

- 01절 뒤 **같음 201 · 바뀜 8 · 없어짐 0** — 절 HTML·`_src`·노트북 01 · 옛 생성기 둘(막기) · `verify.py`가 다시 쓴 챕터 계약 파일 · `집필점검표.md`·`qa/verification.md`(끝에 01 절 더함). 표는 `manifest-changes.md`. 앞 챕터·Part 7·완료 챕터·과정 문서·pgenv 바이너리는 모두 같음.
