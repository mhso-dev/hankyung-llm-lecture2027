# Ch 31 DB & 상태 영속화 — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part7/ch31-database` 01~05절(품질 개선) + **06절 챕터 끝 실습 절 신설**(`06-DB와-상태-영속화-실습`), 노트북 `labs/part7/ch31-database/notebooks/01~06-*.ipynb`. 도구 파일 없음(§13). 실습 폴더의 `app/`·`migrations/`는 노트북이 가르치는 파일이 아님(03만 `alembic.ini`·`migrations/`를 임시 폴더 사본으로 씀). **뒤 챕터가 읽는 계약 파일(산출 파일)은 없습니다**(노트북이 작업 폴더에 파일을 쓰지 않음 — 03 판 파일 사본·05 덤프 파일은 운영체제 임시 폴더).
- 기간: 2026-09-29(준비 조사 · 01~05절 개선 · 06절 신설 · 검토 1차 · 챕터 마감). 상태: **완료(강사 확인 대기)**. Part 7 둘째 챕터(Ch 32·33은 이번 품질 개선에서만 제외 — 다음 개선 대상은 Ch 34).
- 게이트: 수정 전 다섯 절 합계 **175**(01 37 · 02 32 · 03 35 · 04 26 · 05 45, `gates-before.json`) → 마감 뒤 **6/6 PASS, G1~G7 모두 0**(`gates-after.json` `aa553e4c…`, 검사 문장 394·381·469·403·523·390 = **2,560**).
- 코드 셀 5·5·6·4·7 = 27 → **21·23·31·21·31 + 06 새 절 23 = 150**(`verify.py --chapter` → `PASS 6 sections / 150 code cells (max 14 lines)`). 코드 줄(`count_code.py`, 주석·빈 줄 뺌) 47·48·42·42·94 = 273 → **109·113·136·99·179 + 06 131 = 767**. Mermaid **24장**(01 넷 · 02 넷 · 03 다섯 · 04 넷 · 05 넷 · 06 셋), 삽화 **6장**(절마다 하나, Higgsfield — 재생성 3회, 18크레딧, 마감 0), 복습 문제는 HTML에만.
- **모델 요청: 01~06 모두 0**(키 셀 없음, 실제 모델 비용·토큰 기록 없음). 작업 전체 0, 마감 0.
- 화면 검사 `visual.cjs`: HTML **일곱 개**(여섯 절 + `index.html`) × 1280px·390px = **14행 PASS**(기기 `/tmp/pw` playwright 1.63.0·`/tmp/pw-browsers` chromium-headless-shell 1243 — VM 재시작으로 없어져 마감이 `/tmp`에만 다시 설치, 환경 변수 `NODE_PATH`·`PLAYWRIGHT_BROWSERS_PATH`·`LD_LIBRARY_PATH`만 주고 원본 그대로).
- **마감에서 다시 실행한 노트북: 01 하나**(모델 없음 — 코드 주석 [11] 「닫힘」(검토 A-1)과 출력 라벨 `데이터베이스와 서버 판:` → `버전:`(A-15)). 새 커널 두 번(A 루트 커널 21:08:37Z · B `notebooks/` 커널 사본) 셀별 21개 가운데 19개 같음 — 다른 둘은 걸린 초 셀(A 0.48·0.19 ↔ B 0.47·0.19), 두 비교 `True`는 두 번 모두. **교재 값 0.48·0.19는 새 A 출력과 같아 고칠 곳 없음.** 02~06은 코드·출력·`executed_at` 전후 같음(§21).
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 30 요약 → **이 문서** → `handoff.md`(절 사이 세부, 끝 「검토 반영과 챕터 마감 (2026-09-29)」) → 절별 `NN-diagnosis.md`·`06-design.md` → 검토 `review-round1-A.md`(01~03·공통)·`review-round1-B.md`(04~06) → 준비 조사 `chapter-lead-notes.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 문법·API | 조건 |
|---|---|---|
| 01 | `create_async_engine(url, pool_size=3, max_overflow=0)`(비동기 엔진·`AsyncAdaptedQueuePool`) · `async with engine.connect()` · `await conn.execute(text("… :id …"), 딕셔너리)` · `fetchone`·`fetchall`·`scalar_one`·`rowcount` · **`async with engine.begin()`**(블록 끝 확정) · `engine.pool.size()`·`checkedin()`·`checkedout()` · `await engine.dispose()` · **`asyncio.gather`**(코루틴을 인자로 하나씩 — Ch 2 12 이음) · `time.perf_counter()` | 셀 맨 위 `await`·`async with`(Ch 28·30 이음) · `async def` 하나 · ORM·`AsyncSession` 쓰지 않음 |
| 02 | **한 묶음 작업**(`begin()` 블록 하나)·확정·취소 · `CHECK (balance >= 0)` · `UPDATE` · `except IntegrityError as error:` · `error.orig.sqlstate`(**SQLSTATE** `23514`) · `print(error.orig)` | `error.orig` = SQLAlchemy asyncpg 방언이 드라이버 오류를 DB-API 모양으로 바꾼 오류(드라이버 오류는 `__cause__` — 검토 A-6) |
| 03 | Alembic 파이썬 API **`command.upgrade(cfg, "head")`·`command.downgrade(cfg, "-1")`** · `Config` · 판 파일(`revision`·`down_revision`·`op.add_column`·`op.drop_column`) · **`server_default`** · `nullable` · 환경 변수 `os.environ["CH31_SYNC_URL"]` · `tempfile.mkdtemp` 사본 · 동기 엔진 `create_engine`(psycopg) · `replace` | 새 판 파일은 임시 폴더 사본에만 · 자식 프로세스 없음 |
| 04 | **`pool_timeout`**(대기 제한) · **반납**(`await conn.close()`·`async with` 블록 끝) · **`sqlalchemy.exc.TimeoutError`**(내장 `TimeoutError`와 이름 가림 — `import sqlalchemy.exc`) · `engine.pool.status()` · `engine.pool.timeout()` · `issubclass` · `__module__` | `create_task`는 노트북에서 쓰지 않음(b7 노트북 밖 확인과 첫 풀이 한 문장 — 검토 B-2) |
| 05 | psycopg 동기 연결(`autocommit=True`·`dict_row`) · pgvector `vector(3)`·**HNSW**(`vector_cosine_ops`)·`<=>` · **`EXPLAIN (COSTS OFF)`**·`SET enable_seqscan = off` · **`PostgresSaver`**+`setup()`+**`SET search_path TO ch31_shared`** · 모델을 쓰지 않는 그래프(`double_value`)·`get_state` · `shutil.which`·`subprocess.run(…, input=, capture_output=True, env=)` · **`pg_dump --format=custom --schema=…`**·`pg_restore --list`·**`pg_restore --dbname=…`** · 복원 전 `CREATE EXTENSION vector` | `PGPASSWORD`로 연습용 비밀번호(값 출력 없음) · Docker 갈래(`docker exec -i`)는 실행하지 않음 |
| 06 | 새 문법·새 API 0(01~05 이름만 — `astdiff.py`) | 동기 엔진 `begin()` 블록 하나 + 작은 풀(`pool_size=1, max_overflow=0, pool_timeout=0.2`) + `PostgresSaver` |

- 쓰지 않은 것(전 절 0): ORM(`DeclarativeBase`·`Mapped`)·`AsyncSession`·`async_sessionmaker`·`AsyncPostgresSaver`·노트북 `create_task`·f-string·내포식·제너레이터 식·`lambda`·조건 표현식·기본값 매개변수·힌트(상태 형식 `TypedDict` 칸 말고)·가짜 모델. 호출 깊이 최대 2, 준비 셀 밖 셀 최대 10줄.

## 2. 앞 챕터에서 이어 쓴 부품과 값

| 챕터 | 이어 쓴 것 | 자리 |
|---|---|---|
| Ch 2 12 | `async def`·await·`gather()`·`time.perf_counter()` · `create_task`는 전제 금지 목록 | 01 7절 · 04 b7 첫 풀이 |
| Ch 2 05·08 | `try`·`with open` · `subprocess.run(…, capture_output=True)` | 02·03·05 |
| Ch 4 03 | SQL·커밋(→ 「확정(커밋)」)·물음표 자리(→ `:id`)·제약·`sqlite3.IntegrityError` | 01·02·03 |
| Ch 12 02 | PostgreSQL 컨테이너·pgvector·HNSW·`enable_seqscan` 실험(05는 겹치지 않게 「확장 만들기」를 변수로) · 말 「색인」 | 05 |
| Ch 16 05 | `retry_with_fallback`의 `except TimeoutError` — 04가 이름 가르기 | 04 b3·[24] |
| Ch 21 04 | 「옮기기(마이그레이션)」 — 03 「표 구조 바꾸기(마이그레이션)」와 다른 뜻 문장 | 03 2절·b3 |
| Ch 23 01·02·06 | 체크포인터·스레드·`PostgresSaver`·`setup()`·표 만들기 기록·이름 공간(SQL `SCHEMA`)·`search_path` · 멱등 키 | 01 3절 · 05 · 06 · 02 b7 |
| Ch 25 03 | 걸린 시간 처리 선례(결론은 부등식과 매번 같은 값, 초는 결과 읽기 둘째 단락·b6 표·확인할 점·b7) | 01 |
| Ch 28 01·03 | 셀 맨 위 await(노트북 도구 기능) · 환경 변수 · `dict(os.environ)` 복사 | 01·03·05 |
| Ch 30 01·03 | 처리 함수 `async def`(Ch 30 말 「처리 함수」) · 파일 위치 셀(후보 셋·`assert` 한 줄) · 셀 맨 위 `ainvoke` | 01 b2·b3 · 03 · 01 b3 |

## 3. 절별 과제·값 (새 커널 두 번에서 같았던 값 — 결론·그림에 쓴 값)

| 절 | 과제 | 값 |
|---|---|---|
| 01 | 같은 `read_question`(0.15초) 셋을 await 줄 셋 ↔ `gather()` | 받은 값 `['환불', '배송', '결제']` 같음 `True` · 기록 앞 셋 시작 1·끝 1·시작 2 ↔ 시작 1·2·3 · 쉬는 연결 1 ↔ 3 · `함께 기다린 시간이 더 짧은가: True` · (흔들린 값) 0.48 ↔ 0.19초 |
| 02 | 잔액 500·500에서 600 이체 — 블록 둘(Before) ↔ 블록 하나(After) | 둘 다 `23514`·`accounts_balance_check` · Before `[(1, 500), (2, 1100)]` 합 1600(빨강) ↔ After `[(1, 500), (2, 500)]` 합 1000 · 블록 안 1100 ↔ 밖 500 · 값 바꿔 보기 500 이체 `[(1, 0), (2, 1000)]` |
| 03 | 줄 셋이 든 `tickets`에 NOT NULL 칸 `owner` — 기본값 없음(Before) ↔ `server_default="미정"`(After) | Before `IntegrityError`·`NotNullViolation`·`23502` → `판 번호: 20260911_01`·`칸: ['id', 'question']`(빨강) ↔ After `20260929_02`·세 줄 `'미정'` · 판 내리기 뒤 다시 올리면 1번 줄 `'민지'` → `'미정'` · `nullable=True` → `None` 셋 |
| 04 | 풀 크기 1·대기 제한 0.2초 — 닫지 않은 연결(Before) ↔ 반납(After) | Before `빌려 간 연결 수: 1`·`풀에 쉬고 있는 연결 수: 0` → `TimeoutError`(`… timeout 0.20`, 빨강) ↔ After 0·1 → `받은 데이터베이스 이름: ch31_lab` · 값 바꿔 보기 1.0초 → `timeout 1.00` · `파이썬의 TimeoutError를 이어받는가: False` |
| 05 | 이름 공간 `ch31_shared`(문서 표·HNSW·체크포인터 표 넷) 덤프 → 새 DB 복원 — 확장 만들기 False ↔ True | 3절 `Seq Scan on documents` · 표 다섯·`{'value': 12}` · `pg_dump 버전: pg_dump (PostgreSQL) 17.11` · 목차 문서 표 `True`·체크포인트 표 `True`·확장 `False` · 실행 1 `pg_restore 종료 코드: 1`·`type "public.vector" does not exist`·`errors ignored on restore: 5`·표 넷 ↔ 실행 2 `0`·표 다섯(`'documents': 3`) · 두 실행 `{'value': 12}` · 복원 DB `Index Scan using documents_embedding_hnsw on documents` |
| 06 | 상담 예약 그래프(문의 셋 10·30·10분) — 처음 상담 시간 50 ↔ 30 | 실행 1 `[1, 1, 1]`·남은 0·`[1, 2, 3]`·`booked 1` ↔ 실행 2 `문의 2 받은 오류: IntegrityError 23514`·`[1, 0, 1]`·남은 10·`[1, 3]`·`booked 0` · 두 실행 체크포인트 9·빌려 간 0 · 새 연결로도 `{'no': 2, 'minutes': 30, 'booked': 0}` |

## 4. 용어 (챕터 안에서 한 번만 정의하고 이어 씀 — 세부는 handoff 「용어 표」)

| 말 | 뜻 | 첫 자리 |
|---|---|---|
| 비동기 엔진 · 드라이버 · 연결 · 연결 풀 · SQL 글 객체 | 01 새 용어 다섯. **연결 풀 = 한 번 연 연결을 서버와 끊지 않고 모아 두었다가 다시 빌려 주는 곳**(마감 검토 A-1 — 「닫지 않고」를 고침) | 01 |
| 한 묶음 작업(트랜잭션) · 원자성 · 취소(롤백) · 확정(커밋) | 「취소」는 블록 안 변경을 없던 일로 하는 것만 — 03 제목의 롤백(판 내리기)과 다름 | 02 |
| 표 구조 바꾸기(마이그레이션) · 판(리비전) · 판 올리기·판 내리기 | Ch 21 04 「옮기기(마이그레이션)」와 다른 뜻 | 03 |
| 대기 제한(`pool_timeout`) · **반납**(빌린 연결을 닫아 풀에 다시 넣는 일 — 서버와의 통로는 끊지 않음) · 이름 가림 | 01의 「블록이 끝나면 풀에 다시 들어간다」에 붙인 이름 — 01에 「04절은 이 일을 반납이라고 부릅니다」(마감) | 04 |
| 백업 · 복원 · 덤프 파일 | 목차 원문은 실행마다 번호가 바뀌어 출력하지 않음 | 05 |
| (이어 씀) 이름 공간·체크포인터·색인·계획 줄·스레드 | Ch 23·Ch 12 말 | — |
| **「버전」 ↔ 「판」** | **패키지·서버 번호는 챕터 전체에서 「버전」, 「판」은 표 구조의 판(리비전)에만**(마감 검토 A-15 — 01·02 고침). 교환대 비유의 「판」(나무·금속 판)과 02의 「Before 판·After 판」(두 가지 코드)은 그대로 — 강사 확인 | 03(정함)·마감 |

- 금지어·대체어: 트랜잭션·롤백·마이그레이션은 제목·제목 풀이·괄호 원어만 · 인덱스 → 색인 · 스키마 → 표 구조 / 이름 공간 · 쿼리 → 조회 · 세션 → 연결 또는 코드 이름 · 반환 → 내놓다 / 반납 · 보장 → 장담(마감에서 05에 새로 쓴 「보장」 넷을 고침) · 「순차」(Ch 12 「순차 스캔」도 인용하지 않음).

## 5. DB 준비

- **학생**: 챕터 전용 Docker 컨테이너 하나를 여섯 절이 함께 씀(01 제목 셀·실습 폴더 README 글자 그대로).
  ```bash
  docker run --name kdt-ch31-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=ch31_lab -p 127.0.0.1:55431:5432 -d pgvector/pgvector:0.8.1-pg17
  ```
  연습용 비밀번호 `postgres` · `127.0.0.1`에만 묶음(Docker 기본은 바깥에서도 붙음) · 접속 글 `postgresql+asyncpg://…`(01·02·04) / `postgresql+psycopg://…`(03·06) / `postgresql://…`(05·06 체크포인터) — 서버·계정·DB는 같고 드라이버 부분만 다름 · 노트북은 `.env`를 읽지 않음.
- **작업 기기**: `qa/upgrade/pre_exec.sh`(**최종 `3a838c9204b9b8d8be487e2f0460bd3bd3f394fe891161efa2b88c54cb35a435`** — 01 `8a9529f1…` → 05 `dd564645…` → 마감 주석 두 줄만 「여섯 절」로, 주석 밖 줄은 같음을 `diff`로 확인) · `.cache/vm/pgenv/bin`(conda-forge PostgreSQL 17.11 + pgvector 0.8.1)으로 **`/tmp/ch31-pg/data`**에 클러스터(없을 때만 `initdb`) · `127.0.0.1:55431`만 · 부른 셸이 끝날 때 `trap EXIT`로 끔 · 05가 **pgenv `bin`을 `PATH` 끝에 한 줄** 더함(`pg_dump`·`pg_restore` 17.11, 시스템 명령을 가리지 않게). `run_section.sh` 32행이 source(`--no-exec`도). 끝낸 뒤 `ps -eo comm | grep -c '^postgres$'` 0 · `ss -ltn | grep -c 55431` 0.
- **교재 출력 버전 가름**: 교재 출력은 Linux의 Python 3.12.13 + PostgreSQL **17.11** 서버(Docker 컨테이너가 아님) + pgvector **0.8.1**. 학생 이미지 `pgvector/pgvector:0.8.1-pg17`은 PG 17·pgvector 0.8.1이지만 서버 버전 끝자리는 다를 수 있음(각 절 제목 셀·b7). Docker·Windows·macOS로는 교재 출력을 만들지 않음.
- 서버에 남기는 것: 05의 확장 `vector`(`ch31_lab`의 `public`)뿐 — 절마다 제 이름 공간(`ch31_async`·`ch31_tx`·`ch31_migration`·`ch31_shared`·`ch31_practice`)과 복원 DB `ch31_restore`를 지움.

## 6. 비동기·동기 드라이버 범위

- 비동기(asyncpg — 셀 맨 위 `await`): 01·02·04. 동기(psycopg): 03(Alembic 동기 엔진)·05(`PostgresSaver`)·06(그래프 `invoke` + `PostgresSaver`라 노드의 한 묶음 작업도 동기 `begin()` — 06 b3 문장). `AsyncPostgresSaver`·`await` 노드는 어느 절도 실행하지 않음.
- 01 b7: 연결 하나나 `AsyncSession` 하나를 여러 작업이 함께 쓰는 장면은 실행하지 않음(문서 「안전하지 않다」만 인용).

## 7. 파일 위치 셀과 묶음 계약 (03)

- 03만 실습 폴더 파일(`alembic.ini`·`migrations/`)을 읽음 → Ch 30 과정 표준 파일 위치 셀(후보 `..`·`.`·`labs/part7/ch31-database`, 찾을 파일 `/alembic.ini`, 고른 후보 출력 없음, `assert` 한 줄).
- **묶음 계약**: Part 7 `qa/check_bundle_execution.py` 27행 `smoke_sections`가 **Ch 31 03**을 풀린 묶음 `notebooks/`에서 실행 — 03은 키·모델·도구 파일 없이 DB만 있으면 돎. 03 `code_sha256` `f97cba07f5bc…`(마감 전후 같음, `bundle-execution.json`의 Ch 31 줄 `b0594f2d…`는 옛 판 — 전체 마감).
- 03은 새 판 파일을 임시 폴더 사본에만 씀 → 실습 폴더 `migrations/versions/`와 학생 판 사슬은 그대로. 첫 판 파일 설명 글 「상담 티켓 표 구조를 변경합니다」(실제로는 표를 만듦)는 **03 출력 [27]의 Alembic 진행 기록에 찍혀** 고치지 않음(검토 A-17 — §21).

## 8. 비유 가족 「전화 교환대」 (삽화 열)

- 사람 없이 판·꽂는 자리·선·불·덮개만. 짝: 판 = 연결 풀 · 꽂는 자리 수 = `pool_size` · 꽂힌 선 = 연결.
- 01-5 갈색 나무 판 둘(선 하나·불 하나 ↔ 선 셋·불 셋) · 02-5 초록 금속 판 하나에 짝 셋(양 끝 꽂힘·한 끝만·둘 다 빔) · 03-6 크림색 판 둘(빈 자리 새 판이 탁자에 남음 ↔ 회색 마개 셋) · 04-5 판에 꽂힌 채인 선 ↔ 받침에 세운 선 · 05-5 자리를 단 판 ↔ 달지 않은 판(선 넷 ↔ 다섯) · 06-4 검은 틀 하나에 청록·테라코타·옅은 노랑 판 셋(가운데 칸만 빔 ↔ 덮개 셋).
- **「꽂힌 선」 뜻**: 04는 「판에 꽂힌 선 = 빌려 간 연결, 받침에 세운 선 = 쉬고 있는 연결」. 06은 「풀에 있는 연결 하나」 — 06 비유 다른 점에 「04절 비유와 달리 … 실행 2 뒤 빌려 간 연결은 0」을 둠(마감 검토 B-6).
- 작업 조회 결과의 모델 표시 `nano_banana_2`와 요청 `nano_banana_pro`가 다름(기록만). 금지 소품 목록은 handoff 「비유 계열」.

## 9. 색 규칙 (Mermaid 24장)

- 셀에 적은 자료·값 초록(tool) · 우리가 적은 코드와 **실험·값 바꿔 보기에서 바꾼 값 파랑(flow)** · 출력으로 확인한 값·받아 출력한 오류 노랑(measure) · 라이브러리·서버·두 조건 공통·설치판 소스로만 본 것 회색 · 보라 0(모델 없음) · **빨강은 paired Before 결함 결과만**(02-3·02-4·03-3·03-4·04-3·04-4).
- **06-3을 마감에서 바꿈**(검토 B-8): 실행 2의 처음 상담 시간 30분 상자를 파랑으로(실행 1의 50분은 셀에 적은 값이라 초록) — Ch 29·30 마감 결정(10-3)과 같게. 도식 읽기·alt·설계표 함께.
- 03-2 결과 상자에서 판 올리기 뒤 셀이 아닌 「넣은 줄 수 3」을 뺌(A-12) · 03-3 회색 상자 「한 묶음 작업 전체가 취소됨」 → 「판 함수가 끝나지 않아 판 번호를 적지 않음」(A-8, 설치판 소스 근거 — 도식 읽기에 갈래). 다시 렌더한 셋은 PNG를 열어 확인.

## 10. 결정적 값과 흔들린 값

- 모델이 없어 01의 걸린 초 말고는 모두 매번 같은 값(각 절 새 커널 두 번 셀별 출력 같음 — `outputs_sha256`이 갈린 절은 설치 셀 출력이 나뉜 모양 차이뿐).
- **01 초 값**: 결과 읽기 둘째 단락·b6 표·「확인할 점」·b7에만(교재 출력 A 0.48·0.19). 결론·그림·캡션·alt·정리·복습에는 `함께 기다린 시간이 더 짧은가: True`와 매번 같은 값만. 마감 재실행 A 0.48·0.19(값 그대로) · B 0.47·0.19 · 두 번 모두 부등식 `True`. 시간 `assert` 0.
- 04는 걸린 시간을 재지 않음 — 7절 결과 읽기의 「대기 제한은 기다리는 시간만 바꿨다」 단정을 「걸린 시간은 재지 않았고, 출력에서 달라진 것은 오류 글 끝의 대기 제한 값뿐」으로(검토 B-1).

## 11. 모델 요청 수와 예상 비용

| 절 | 노트북 한 번 | 작업 전체 |
|---|---|---|
| 01~06 | 0 | 0(노트북 밖 확인·새 커널 두 번·묶음 실행 모두 모델 없음) |
| 마감 | — | 0(01 재실행·묶음 손 실행 03·06·노트북 밖 확인 B-3 모두 모델 없음) |

- 06 실습 절 모델 요청 0은 규격 §7-2 「3~5번」과 다름(Ch 23·24·30 선례 — 강사 확인). 예상 비용 0달러.

## 12. 06절 실습 절 — 상담 예약 그래프에서 처음 상담 시간 하나만 바꾸기

- 붙인 기능 셋(모두 실행 1·2 흐름 안): **02 한 묶음 작업**(노드 `book_inquiry`의 `begin()` 블록 하나 — 예약 줄 `INSERT` + 상담 시간 `UPDATE`, `CHECK (minutes >= 0)` 위반을 받아 `{"booked": 0}`) · **04 작은 연결 풀과 반납**(풀 크기 1인데 배송 뒤 결제 문의가 연결을 받음·빌려 간 0) · **05 체크포인터**(`search_path TO ch31_practice`·`get_state`·새 연결로 다시 읽기). 뺀 것: 01 `gather`(노드가 문의를 차례로 받으므로) · 03 Alembic · 05 색인·백업·복원.
- **취소된 문의의 상태가 남는 까닭(마감 검토 B-5 [상] 정정)**: 배송 문의의 한 묶음 작업은 **노드 함수 안에서 이미 취소**되었고, 노드는 그 오류를 받아 `{"booked": 0}`을 내고 끝남. 체크포인터는 **노드가 끝난 뒤** 그 상태를 적음(설치판 langgraph 1.2.11 `pregel/_runner.py` 207~221행 — 노드 작업을 끝까지 실행한 뒤 `commit` · `pregel/_loop.py` 683~718행 — `after_tick`에서 `_put_checkpoint`, 행 번호 마감 확인). 옛 글 「체크포인터가 다른 연결로 적기 때문」·「실행 2는 이 차이를 보여 줍니다」를 본문 b4·b6·셀 [40]·복습 4·b7·학습 목표 3·정리에서 고침. **두 표를 한 묶음 작업으로 함께 확정/취소하는 장면은 실행하지 않음**(b4·b7).
- 말(검토 B-7): 「배송 문의만 취소」 → 「배송 문의만 예약되지 않음」(목표 2·정리·캡션) · 「취소」는 02 뜻(한 묶음 작업)으로만.
- 코드 셀 23 · 코드 줄 131 · 검사 문장 390 · Mermaid 3 + 삽화 1 · meta 「실습 30분 · 새 용어 0」(**챕터 시수 16h에 더하지 않음** — 01~05 meta 합 강의 1·1·1·1·1 = 5h · 실습 2·2·2·2·3 = 11h = `chapter.json` `hours`) · `code_sha256` `bb245f74…`·`outputs_sha256` `139e24d3…`(마감 전후 같음).

## 13. 도구 파일 — 없음 (까닭)

- 규격 §2-7 3의 대상(두 절 이상이 같은 평범한 함수를 다시 적는 경우)이 없음: 01 `read_question`은 전역 `engine`·`read_sql`·`step_log`에 기대는 실험용 · 02~05 함수는 모두 그 절의 이름 공간·전역에 묶임 · 06 함수 넷(`book_inquiry`·`open_day`·`read_tables`·`send_inquiry`)은 흐름을 잇는 새 함수 · 06 셀 [45]가 05 `restored_state` 본문 다섯 줄을 다른 이름 공간으로 한 번 풀어 쓰는 것은 파일을 더해도 코드가 줄지 않는 예외(검토 B 확인). 03은 묶음 실행 검사 절이라 도구 파일을 가져오지 않는 편이 안전(Ch 28 01 선례).

## 14. 묶음·검사

- **묶음**: `python3 -B textbook/part7/_build_index.py`(README·`chapter.json`·목차 줄·continuity-guide·노트북을 모두 고친 뒤 마지막에 한 번) → **`Part 7: 31 verified sections; 111 bundled files`**, `part7-practice.zip` `b5dac376…`(06절 작업 중간 판) → **`6711c32aaad9550e19c1638e2d3de912a7b67c944ae687ba9fdd54807b3bedd9`**(114항목·파일 114, **Ch 31 17파일이 디스크와 모두 같음**, 디스크에만 있는 Ch 31 파일 0, `continuity-guide.md` 같음, `__pycache__`·`.pyc`·`.venv`·`.pytest_cache`·`.env`·`.failure.json` 0) · `textbook/part7/index.html` `bfea1c9a` → `9c566329`(Ch 31 설명 한 줄만) · `qa/integration-results.json` `e231a76c` → `89f684f2`(`bundle_sha256`만). 공개 목록: 챕터 `qa/public-files.json` 24줄(06 HTML·노트북 있음, 옛 그림·옛 생성기 줄 없음 — 그대로 `51fc1808`) · Part 목록 `collect_public_files.py`로 다시 모아 **바이트 같음**(`d822ee88`, `Explicit public files: 110; prerequisites: 1`).
- **묶음 실행 검사는 손으로**: `check_bundle_execution.py`는 노트북 실행기를 `labs/part7/ch31-database/.venv/bin/python`(맥 `.venv` — `/Users/…` 링크)으로 박아 두어 스크립트를 고치지 않고는 이 기기에서 못 돎(32행). 그래서 새 zip을 `/tmp/ch31-close/bundle`에 풀고 Ch 31 가상환경으로 **03·06을 키 없이·훅으로 DB를 켜고** 실행(`execute.py --cwd <풀린 notebooks>`, `OPENAI_API_KEY` 없음, `PYTHONDONTWRITEBYTECODE=1`) → **03 PASS 31셀·06 PASS 23셀, 저장 노트북과 셀별 출력 글자 31/31·23/23 같음**(03 `outputs_sha256`까지 같음 · 06은 설치 셀 출력이 한 조각으로 온 모양만 달라 `9c4cfe67…`), `code_sha256` 같음, 풀린 폴더에 `__pycache__`·`.failure.json` 0. **`bundle-execution.json`은 옛 zip 기준 그대로**(Ch 31 03 옛 `b0594f2d…` → 지금 `f97cba07…`) — 전체 마감 몫.
- **전달 검사**(Part 7 `check_delivery.py`, 고치지 않음): 절·링크 검사 뒤 **`existing-artifacts-before.json`의 없는 파일(`textbook/part2/ch07-prompt-engineering/_src/index-body.html`)에서 `FileNotFoundError`**(알려진 일, 결과 파일 안 바뀜). 그 대조와 `llm-practice.zip`을 뺀 사본(`.cache/ch31-close/dx/check_delivery_noprior.py` — Ch 30 사본과 같은 네 줄, 결과 자리만 ch31)은 **절 31 · 코드 셀 448 · 깨진 링크 0 · `part7-practice.zip` 111파일 모두 디스크와 같음** 통과.
- **화면 검사** `visual.cjs`: **14행 PASS**(`textbook/_notebook/checks/ch31-database/visual-results.json` `964cfbb2…` + 스크린숏 넷 새로). Part 7 공용 `qa/visual-results.json`은 **Ch 31 줄만 12 → 14**(`b73d3e84` → `85ca91f8`, 다른 줄 62 그대로 — 파이썬으로 객체 대조).
- **옛 검사 스크립트(고치지 않음)**: `check_figures.py` — **20행 `assert (figures / '_gen_figures.py').is_file()`에서 Ch 30 폴더로 멈춤**(Ch 30 마감이 옮긴 알려진 충돌 — Ch 31까지 가지 않음, 결과 파일 안 바뀜). Ch 31만 도는 사본(`.cache/ch31-close/dx/check_figures_ch31only.py`)으로 옮기기 전 **PASS 5쌍**(옛 그림 다섯 쌍) — **이 사본이 첫 실행에서 결과 파일 `figure-consistency.json`을 써서 실행 전 사본으로 되돌림(바이트 같음 확인)**, 사본은 그 줄을 막음 · `check_secrets.py` — **PASS 178파일·묶음 둘**, 결과 파일 `secret-scan.json`을 새로 써서(`source_files` 171 → 178) **실행 전 사본으로 되돌림** · `check_special_secret.py` — Ch 32 도커 PostgreSQL 검사라 돌리지 않음 · `collect_public_files.py` — 바이트 같음 · `check_bundle_execution.py` — 위.
- 게이트 `upgrade_gates.py … --label after` **6/6 PASS · G1~G7 0** · AST 따로(`.cache/ch31-06/tools/extra_check.py`) 챕터 예외만(셀 맨 위 `await`·`async with`·`try`·`async def`·`TypedDict` 칸)·깊이 2 · `verify.py --chapter` **PASS 6 sections / 150 code cells (max 14 lines)**(계약 파일 `089e8b84` → `a386e822` — 01 새 해시) · 빌드 HTML 일곱 `{{`·`[[` **0건** · 인용 대조(§21).

## 15. 챕터 밖 수정 (전부 목록)

| 파일 | 언제 | 무엇을 |
|---|---|---|
| `labs/part7/ch31-database/notebooks/01~06-*.ipynb` | 01~06절 · **마감** | 실습 폴더(챕터 몫). 마감: **01 다시 실행**(`code_sha256` `addb4391…` → `1566ad038be4…` · `outputs_sha256` `145e0cf3…` → `f8a551e4d649…` · 파일 `0b743f06` → `325b22d7`) · 02~06 마크다운만(코드·출력·`executed_at` 그대로) — 파일 02 `b427398a`→`9e011482` · 03 `28595499`→`8870859a` · 04 `3d9bf01c`→`d2f2ce27` · 05 `09471344`→`07371777` · 06 `2bdbfbd1`→`4de8d9f9` |
| `labs/part7/ch31-database/README.md` | 06절(한 단락) · **마감(전체)** | `a54f0fd5`(원본) → `bd99e26b` → **`e6eba05a3b7cc854818114c61dd0924c63e57b7e63dad21c01befcd102c839fe`**: 노트북 여섯·절별 설치 버전·**모델 요청 01~06 모두 0**·API 키 없음·**노트북은 `.env`를 읽지 않음**·DB 준비(01 Docker 명령 글자 그대로·연습용 비밀번호·`127.0.0.1`에 묶는 까닭·끄는 명령)·접속 글 셋·교재 출력 버전(17.11·0.8.1)과 이미지 버전 가름·`uv sync --locked` → `.venv` → `notebooks/`·절별 이름 공간·05 백업 명령 두 갈래와 **주 버전 조건**(`pg_dump_found = None` 한 줄로 컨테이너 쪽)·종료 코드 확인·`app/`와 `migrations/` 설명·**실습 폴더 맨 위에서 도는 명령**(`uv run alembic upgrade head` → `uv run python -m app.service` → `uv run alembic downgrade base`, 프로젝트 맨 위에서는 `ModuleNotFoundError` — 마감이 Linux에서 실습 폴더 사본으로 확인, `[]`)·03이 이름 공간을 지우고 시작한다는 것·06 단락. 옛 `.env`의 `CH31_DATABASE_URL`·`-p 55431:5432`·`uv sync --project`·프로젝트 맨 위 `python -m app.service`·「스키마」·「롤백」·「트랜잭션」·「다섯 노트북」 뺌, 묶음 밖 파일을 가리키지 않음, 금지어 0 · **덮어쓸 때 임시 파일을 `mv -f`로 옮겨 씀(옛 판은 `.cache/ch31-close/pre/`·`README.old.md`에 사본)** |
| `labs/part7/continuity-guide.md` | **마감** | 9행 「Ch4의 SQL, Ch12의 pgvector \| Ch31의 트랜잭션·연결 풀·인덱스 \| …」 → 「Ch2의 gather, Ch4의 SQL과 커밋, Ch12의 pgvector와 HNSW, Ch23의 체크포인터 \| Ch31의 비동기 엔진과 연결 풀, 한 묶음 작업과 취소, Alembic 판 올리기·내리기, 반납과 대기 제한, 색인·체크포인터 표·백업과 복원 \| Ch32의 데이터베이스 컨테이너」(`17b07239` → `b9aa0766`, 보호 파일, 묶음에 들어감). 8행(Ch 30 줄의 「Ch31의 데이터·체크포인트 저장」)은 참이라 그대로 |
| `textbook/part7/_build_index.py` | **마감** | 20행 ch31 설명 → 「비동기 엔진과 연결 풀, 한 묶음 작업과 취소, Alembic 판 올리기·내리기, 반납과 대기 제한을 보고, pgvector 색인·체크포인터 표의 백업과 복원을 확인한 뒤, 세 기능을 상담 예약 그래프 하나로 잇는 실습을 합니다.」(시수 5·11 그대로, `43525ed4` → `750baec3`, 보호 파일) |
| `textbook/_notebook/build_index.py` · `textbook/index.html` | **마감** | 66~67행 Ch 31 설명 → 「비동기 엔진과 연결 풀, 한 묶음 작업과 취소, Alembic 판 올리기·내리기, 반납과 대기 제한을 보고, pgvector 색인·체크포인터 표의 백업과 복원을 확인합니다.」 **절 수 5 그대로**. 스크립트를 돌리기 전 옛 스크립트 출력이 지금 `index.html`과 바이트까지 같았고, 다시 만든 뒤 바뀐 것은 Ch 31 설명 하나(파이썬으로 되돌려 대조)(`db6ad12f` → `8457fd7d` · `80aad0d4` → `2159e001`, 보호 파일) |
| `textbook/part7/index.html` · `textbook/downloads/part7-practice.zip` · `textbook/part7/qa/integration-results.json` | 06절 + **마감** | §14 |
| `textbook/part7/qa/visual-results.json` · `textbook/_notebook/checks/ch31-database/visual-results.json`(+ 스크린숏 넷) | **마감** | §14 |
| `textbook/part7/qa/secret-scan.json` · `textbook/part7/qa/figure-consistency.json` | **마감(되돌림)** | `check_secrets.py`·`check_figures.py` 사본이 새로 써서 실행 전 사본으로 되돌림(내용 변경 0) |
| `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json` | 절마다·마감 | `verify.py --chapter`가 다시 씀 — 마감 뒤 `a386e822` |
| `textbook/qa/upgrade-progress.md` · `textbook/qa/upgrade-final-checklist.md` | **마감** | Ch 31 행 한 줄 · §2-19 Ch 31 항목·§3·§4 Ch 31 줄·§2-18 11번 끝에 한 줄 |

- **고치지 않은 것**: `textbook/QUALITY-UPGRADE.md`·`PLAYBOOK.md`·과정 요약·`upgrade-contracts.md`(오케스트레이터 몫) · 공용 도구 코드(`nbkit.py`·`mdpatch.py`·`run_section.sh`·게이트·`verify.py`·`visual.cjs`·`execute.py`·`render_mermaid.py`·`attach_figures.py`·`count_code.py`) · Part 7 검사 스크립트 전부 · `bundle-execution.json`·`delivery-results.json`·`existing-artifacts-before.json`·`final-artifact-hashes.json` · 공개 목록 두 곳(바이트 같음) · 실습 폴더 `app/`·`migrations/`(첫 판 파일·`env.py`)·`alembic.ini`·`pyproject.toml`·`uv.lock`(해시 같음) · 삽화(Higgsfield 0) · `.moai` part7 스크립트 셋 · **Ch 32 이후 파일 전부**(Part 7 목차·묶음·공개 목록·기록·`continuity-guide.md` Ch 31 줄 말고 — Ch 32 04 `_src`는 읽기만) · `llm-practice.zip` · claude.ai 프로젝트 문서.
- **파일을 지운 것은 없습니다.** 옮긴 것은 옛 생성기 둘(`mv -n`, 해시 같음 — §20). 부르는 스크립트는 Part 7 `check_figures.py` 20행뿐(`grep`) — 이미 Ch 30에서 멈추는 알려진 충돌. 마감 README는 임시 파일을 `mv -f`로 덮어 씀(위 표).
- **보호 파일 209개(`before-manifest.json`)**: §21.

## 16. 기준 버전·확인 날짜

- 실습 폴더 잠금(`pyproject.toml` 직접 의존 `alembic==1.16.5`·`asyncpg==0.30.0`·`langgraph==1.2.11`·`langgraph-checkpoint-postgres==3.0.5`·`pgvector==0.4.1`(파이썬 패키지 — 노트북은 쓰지 않음)·`psycopg[binary,pool]==3.3.3`·`python-dotenv==1.2.1`(노트북은 쓰지 않음)·`sqlalchemy[asyncio]==2.0.43`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·**`pip==25.2`**(과정 기준 26.2와 다름 — 고치지 않음, §20)·`ruff==0.12.11`). 노트북 `%pip`: 01·02·04 둘 · 03 셋 · 05 셋 · 06 넷(README 표).
- 서버: PostgreSQL **17.11**(conda-forge pgenv)·pgvector 확장 **0.8.1** · 명령 `pg_dump`·`pg_restore` 17.11.
- 교재 출력: Linux aarch64 · Python **3.12.13** · 환경 `.cache/vm/venv-ch31-database`(잠금 판 + pip 26.2). 실행일 2026-09-29(01 **21:08:37(마감 재실행)** · 02 16:31:16 · 03 17:09:43 · 04 18:54:00 · 05 19:32:40 · 06 20:10:04 UTC).
- 참고 자료(절 작업·검토 2026-09-29 확인): SQLAlchemy asyncio·Connections·Pooling·Core Exceptions·Error 3o7r(문서 2.0.54 ↔ 설치 2.0.43) · Alembic Tutorial·Commands·Runtime·Autogenerate(문서 1.20 ↔ 설치 1.16.5) · PostgreSQL 17 pg_sleep·Transactions·ALTER TABLE·Constraints·Error Codes·EXPLAIN·pg_dump(`-n`·`-e`·주 버전)·pg_restore·libpq `PGPASSWORD` · Docker Port publishing · Docker Hub postgres·pgvector 이미지 · langgraph-checkpoint-postgres(PyPI 3.1.2 ↔ 설치 3.0.5) · Python asyncio `create_task`.
- 설치판 소스 행(마감 확인): sqlalchemy `dialects/postgresql/asyncpg.py` 776~791(드라이버 오류 바꾸기 `raise translated_error from error`) · alembic `runtime/migration.py` 620~632(판 함수 뒤 판 번호) · langgraph `pregel/_runner.py` 207~221·`pregel/_loop.py` 683~718.

## 17. 강사 확인 대상

1. **제목의 영어와 말**: 챕터 「DB & 상태 영속화」(`&`) · 01 「SQLAlchemy」·「PostgreSQL」 · 02 「트랜잭션」 · 03 「Alembic」·「롤백」 · 04 「커넥션 풀」·「고갈」 · 05 「pgvector」·「체크포인터」·「공존」 · **06 긴 제목**·슬러그 `06-DB와-상태-영속화-실습`(준비 노트 후보 `06-DB-실습`을 쓰지 않음). 본문 첫 자리에서 한 번씩 풂. 01 슬러그는 Ch 30 10 b8·Part 7 목차가 링크해 고정.
2. **코드 양**(규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」): 코드 줄 273 → 767(01 109·02 113·03 136·04 99·05 179·06 131) · 코드 셀 27 → 150.
3. **03 짧은 셀 열둘**(검토 A-14 — 코드 줄 1~2줄 셀, 판을 올리고 내리는 셀과 결과 셀을 나눈 까닭은 stderr·stdout 차례): 합치면 03 재실행·묶음 검사 해시 — 마감은 그대로.
4. **새 용어 17**(01 5·02 3·03 3·04 3·05 3·06 0)과 말: 「한 묶음 작업」·「취소」 ↔ 「판 내리기」 · 「판」 ↔ 「버전」(마감에서 01·02 고침 — 02의 「Before 판·After 판」과 비유의 「판」은 그대로) · 「반납」(01에 이름을 이음) · 「색인」 · 「노드」(허용).
5. **pgembed·SQLite 대체를 쓰지 않은 결정**(준비 노트 §4·§10-1) — 학생은 Docker 컨테이너 하나, 작업 기기는 pgenv 훅.
6. **05 판단**: 실험 변수 「복원 전에 확장 만들기」(Ch 12 02와 겹치지 않게) · `PGPASSWORD`(문서는 비밀번호 파일 권고) · **Docker 갈래(`docker exec -i … pg_dump`/`pg_restore`에 표준 입력) 교재 출력에서 미실행 — 학생 컨테이너에서 한 번 확인할 사람** · **주 버전 조건(검토 B-4)을 글로만** — 코드는 `shutil.which` 결과로만 갈래를 고르고 종료 코드를 확인하지 않음(학생이 `pg_dump_found = None` 한 줄을 더하는 방법을 제목 셀·[40]·b7·README에) · 덤프에 확장이 빠지는 까닭(검토 B-3)을 「`--schema`를 주면 확장을 넣지 않음」으로 고침 — 마감이 노트북 밖에서 재현(`.cache/ch31-close/exp/b3_ext.out`: 확장을 이름 공간 안에 만들어 `--schema`로 덤프 0 · `--extension=vector` 더하면 들어감 · DB 전체 들어감 · `--schema=public` 0).
7. **03 원자성 설명**(검토 A-8): 문장 하나짜리 판이라 원자성 덕분인지 가를 수 없다는 사실대로 고침(「판 함수가 실패해 판 번호를 적는 데까지 가지 않았다」 + 문서대로라면 여러 문장 판은 함께 취소 — 실행하지 않음). **문장 둘짜리 판 장면을 03에 더할지**(더하면 03 재실행·묶음 검사 해시).
8. **06 판단**: **모델 요청 0**(규격 §7-2 「3~5번」과 다름) · 비동기 절 기능을 동기 엔진으로 · 붙인 셋·뺀 것 · 바꾼 값 처음 상담 시간 · 두 표를 함께 확정하는 설계는 다루지 않음(B-5 — 장면을 더하면 새 API라 실습 절 규칙과 부딪힘) · 코드 셀 23·함수 넷이 30분 분량인지.
9. **04 재개 작업**(앞 작업자가 설계·노트북 밖 확인 뒤 연결이 끊겨 멈춘 자리부터) · After가 설정을 바꾸지 않음(대기 제한 늘리기는 값 바꿔 보기에서 여전히 실패).
10. **삽화 여섯**: 01-5 위아래 흰 여백 약 4분의 1 · 02-5 판 좌우 끝이 조금 잘림 · 06-4 덮개가 프롬프트와 달리 닫힌 모양·위쪽 흰 여백 약 5분의 1 · 작업 조회 결과의 모델 표시 `nano_banana_2`(기록만).
11. **01 `AsyncSession` 공유**(검토 A 사람이 정할 것 4): 준비 노트 e2에서 설치판이 두 작업의 `AsyncSession` 공유에 오류를 내지 않았다는 사실을 학생 글에 밝힐지 — 지금은 문서 말과 「실행하지 않았습니다」만.
12. **실습 폴더 파일**: 첫 판 파일 설명 글(03 출력에 찍혀 고치지 않음)·`env.py` 35행 조건 표현식·반환 힌트·기본 접속 글 `localhost`·`app/db.py` 기본 글 `localhost`(README는 `127.0.0.1` 환경 변수를 권함) — 고치면 03 재실행·글·묶음 검사.
13. **`chapter.json` 학습 목표 셋 → 여섯**(「작업 경계를 설계」·「실제 환경에서 재현하고 대응」·「논리 백업 범위」·「트랜잭션」·「롤백」·「커넥션 풀 고갈」을 뺌, 06 실습 줄 더함, `hours` 그대로 16h = 강의 5h + 실습 11h = 01~05 meta 합) · `_build_index.py`·`build_index.py`·`continuity-guide.md` Ch 31 문구 · README 다시 쓴 범위.
14. **Ch 32·33 문장**: Ch 32·33은 이번 품질 개선에서만 제외(Docker 실행 환경 없음)이고 과정에는 남아 있음 — 06 b8의 「다음 챕터 Ch 32 … 04절은 Compose로 서비스와 PostgreSQL·pgvector」는 그대로(검토 B 사람이 정할 것 5).
15. 한국어 감사 3단·그림 판독 2차(별도 세션 — 두 검토의 「확인하지 못한 것」: 삽화 PNG 눈 판독, 학생 Docker 컨테이너로 실제 실행, Windows·macOS, 학생 `uv sync --locked` `.venv` 첫 셀, 03을 바이트코드 캐시 켠 채 실행).

## 18. Ch 34가 이어받을 것과 전제하면 안 되는 것

### 이어받을 것

- 말: 한 묶음 작업(트랜잭션)·확정(커밋)·취소(롤백 — 02) ↔ 판 내리기(03 제목의 롤백) · 표 구조 바꾸기·판(리비전) · 연결 풀·빌려 간/쉬고 있는 연결·반납·대기 제한·이름 가림 · 백업·복원·덤프 파일 · 색인 · **패키지·서버 번호는 「버전」**.
- Ch 34 `_src`·`chapter.json`에는 Ch 31 언급이 없음(2026-09-29 `grep`) — 이어 쓸 문장 없음. Ch 34가 Ch 31을 가리키려면 위 말과 §3 값으로.

### 전제하면 안 되는 것 (Ch 34 파일은 고치지 않았습니다)

1. **Ch 31은 모델 요청 0**(01~06 모두 — 키 셀 없음). 실제 모델 비용·토큰·지연 기록이 없고, `runs/`·계약 파일도 없음 — Ch 34가 비용·예산 계산에 Ch 31 값을 가져올 수 없음.
2. **작업 기기 DB는 훅**(`qa/upgrade/pre_exec.sh` — pgenv PostgreSQL 17.11 + pgvector 0.8.1, 데이터 `/tmp/ch31-pg/data`, `127.0.0.1:55431`, 셸 호출이 끝나면 꺼짐), **학생은 Docker 컨테이너 `kdt-ch31-postgres`**(`pgvector/pgvector:0.8.1-pg17`, `-p 127.0.0.1:55431:5432`, 연습용 비밀번호). 교재 출력은 Docker로 만들지 않았고, 05의 Docker 쪽 백업 갈래도 실행하지 않음.
3. **Ch 32·33은 이번 품질 개선에서만 제외**(과정에는 남음) — Ch 31 06 b8은 Ch 32 04를 가리킴. Ch 34가 Ch 32·33의 개선본을 전제하지 말 것.
4. Ch 31은 **Ch 30 앱에 DB·체크포인터를 붙이지 않음**(SSE 사건 저장 0) · 실습 폴더 `app/`은 노트북이 쓰지 않는 짧은 예제(ORM·`AsyncSession`, 기본 글 `localhost`).
5. **ORM(`Mapped`)·`AsyncSession`·`async_sessionmaker`·`AsyncPostgresSaver`·노트북 `create_task`는 가르치지 않음**(`gather`는 01만). 연결 재시도·마이그레이션 동시 실행·운영 백업 일정도 다루지 않음. 도구 파일 없음.
6. 06: 예약 표와 체크포인터 표는 다른 연결로 확정된다는 사실만 적었고, 함께 취소되는지 가르는 장면은 실행하지 않음. 취소된 문의의 상태가 남은 까닭은 「노드가 오류를 받아 값을 내고 끝났고, 체크포인터는 노드가 끝난 뒤 적음」.

## 19. 뒤 챕터 인계 (그 챕터 파일은 고치지 않음)

| 챕터 | 자리 | 지금 글 | Ch 31 쪽 사실 | 할 일 |
|---|---|---|---|---|
| Ch 32(제외 — 다음 개선 때) | 04 b3 「Ch31에서는 PostgreSQL, 트랜잭션, 인덱스와 pgvector를 배웁니다」 | **참** · 말만 다름 | 02 한 묶음 작업(트랜잭션)·05 색인(인덱스)·pgvector | Ch 32 개선 때 「한 묶음 작업」·「색인」 말로 |
| Ch 32(제외) | **04 b7 「연결 재시도, 트랜잭션 경계, 마이그레이션 동시 실행은 Ch31의 운영 설계와 함께 결정해야 합니다」**(검토 B-9) | 일부 거짓 | 트랜잭션 경계는 02가 다룸 · **연결 재시도·마이그레이션 동시 실행은 Ch 31 01~06이 다루지 않음**(`_src`의 「재시도」는 04 b3의 Ch 16 05 인용뿐, 「동시」 0) | Ch 32 개선 때 대조·고침 |
| Ch 32(제외) | 04 b3 「이 챕터는 Ch31 파일을 복사하지 않고 init.sql에 …」 | 참 | Ch 31 파일을 복사해 쓸 일 없음 | 없음 |
| Ch 33(제외) | Ch 31 언급 없음 | — | — | 없음 |
| Ch 34 | Ch 31 언급 없음(04 b3은 Ch 30만) | — | — | 없음 |
| Ch 30(완료) | 10 b8 「Ch 31 05절은 체크포인터로 그래프의 실행 상태를 PostgreSQL 표에 저장합니다」·06 b7 「보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다」 | 참 | 05·06 그대로 | 없음 |
| Ch 23(완료) | 요약 209행(02 b3 멱등)·210행(02 b7 보상 작업 — 「실행하지 않았습니다」) · 211행(05 체크포인터 새 용어로 세지 않음) | 참 | 02·05 그대로 | 없음 |
| Ch 21(완료) | 요약 64행(03 「마이그레이션」 가르기) | 참 | 03 2절·b3 | 없음 |
| 과정 요약(오케스트레이터) | Ch 31 줄 없음 | — | §4 용어(「버전」↔「판」 가름 포함) · §5 DB 준비(학생 Docker ↔ 작업 기기 훅) · §6 동기·비동기 범위 · 06 모델 0 실습 | Part 7 누적 문서 |
| `upgrade-contracts.md` | §5 묶음 | 옛 zip | 새 zip `6711c32a…` · `bundle-execution.json` 옛 값(Ch 31 03 `b0594f2d…` → 지금 `f97cba07…`) | 전체 마감 |

## 20. 남은 것 (전체 마감 몫 — `textbook/qa/upgrade-final-checklist.md` §2-19)

1. **옛 그림 열다섯 삭제 승인**: `figures/0N-흐름.{svg,excalidraw,caption.md}`(N=1~5 — 세어 15개·25,891바이트, 본문 참조 0, 공개 목록 줄 없음, 사본 `qa/upgrade/before/figures/`). Part 7 `check_figures.py`가 `.excalidraw` 짝과 `_gen_figures.py`를 요구하는 것과 함께 정할 것(옮기기 전 사본 검사 PASS 5쌍).
2. **옛 생성기 둘 옮김(끝남)**: `qa/author_ch31.py`(`79bf670c…`)·`figures/_gen_figures.py`(`34448715…`) → `qa/upgrade/before/generators/blocked/`(`mv -n`, 해시 같음). 막기 전 원본 사본은 `before/generators/`에 그대로. 부르는 스크립트는 `check_figures.py` 20행뿐(Ch 30에서 이미 멈춤).
3. **`gates-wip-*.json` 열셋 삭제 승인**(`gates-wip-01-01`~`06-06`·`01`~`06`·`ch31-after06` — `gates-after.json` 6/6으로 갈음, 절 번호 여섯은 마감 `run_section.sh`가 다시 씀). 챕터 `qa/upgrade/__pycache__/`는 없음.
4. **캐시·임시 삭제 승인**: 실습 폴더 `labs/part7/ch31-database/.venv`(macOS 판 — **`check_bundle_execution.py` 실행기와 묶임**)·`app/__pycache__/`(pyc 넷)·`migrations/__pycache__/`·`migrations/versions/__pycache__/`(pyc 둘 — 모두 2026-09-11 macOS 판, 마감이 만든 pyc 0) · `.cache/vm/venv-ch31-database`(약 349MB)·**`.cache/vm/pgembed-try`(약 204MB — 준비 시험 환경)** · `.cache/ch31-01`~`.cache/ch31-06`·`.cache/ch31-01-view`~`.cache/ch31-06-view` · `.cache/ch31-04/resume` · **`.cache/ch31-close/`**(마감 전 사본 `pre/`·확인 스크립트 `tools/`·치환 목록 `reps/`·B-3 재현 `exp/`·검사 사본 `dx/`·로그 `log/`·그림 보기 사본 `view/`·README 옛/새 사본) · 기기 `/tmp/ch31-prep`·`/tmp/ch31-02`~`/tmp/ch31-06`·**`/tmp/ch31-close`**(B 사본·실습 폴더 사본·묶음 풀기)·**`/tmp/ch31-pg`(DB 데이터 폴더 — 지우면 다음 훅이 `initdb`부터)** · `/tmp/reviewA31`·`/tmp/reviewB31` · 기기 셸 `TMPDIR`의 `ch31-03-*`·`ch31-05-*`(Alembic 사본·덤프 폴더)·`ch31-close-b3`(B-3 재현 덤프) · 마감이 설치한 `visual.cjs` 도구 `/tmp/pw`(19MB)·`/tmp/pw-browsers`(269MB)·`/tmp/npm-cache-ch31close`.
5. **묶음 실행 검사 상태**: `check_bundle_execution.py` 실행기(`labs/part7/ch31-database/.venv/bin/python` — 맥 링크)를 고치거나 기기 판으로 바꾼 뒤 새 zip(`6711c32a…`)으로 다시 돌려 `bundle-execution.json`(옛 zip·Ch 31 03 `b0594f2d…` 기준)을 갱신. **06을 목록에 넣을지**(키·모델 없음, DB만 — 넣으면 계약이 생김).
6. **Part 7 옛 검사 스크립트(고치지 않음)**: `check_figures.py` 20행(Ch 30에서 멈춤 — 1번과 함께) · `check_delivery.py`(`existing-artifacts-before.json`의 없는 Part 2 파일에서 멈춤, `llm-practice.zip`도 대조 대상) · `check_secrets.py`(통과하나 결과 파일을 새로 씀 — 되돌림).
7. **실습 폴더 파일**: `migrations/env.py`(35행 조건 표현식·반환 힌트·`from __future__`·기본 접속 글 `localhost`) — **고치면 03 새 커널 실행 + 3절 글·b4·복습 2·03-2 라벨 대조 + 묶음 실행 검사**(검토 A-17) · 첫 판 파일 설명 글 「상담 티켓 표 구조를 변경합니다」(실제로는 표를 만듦 — 03 출력 [27]에 찍혀 고치지 않음) · `app/db.py` 기본 글 `localhost`.
8. **dev 그룹 `pip==25.2`**(과정 기준 26.2와 다름): `%pip` 셀은 이 잠금으로 돎 — `pyproject.toml`·`uv.lock`을 고치지 않음. 26.2로 맞추려면 `uv lock` → `uv sync --locked` → 묶음.
9. **05 Docker 갈래 확인**: 학생 컨테이너에서 `pg_dump_found = None` 갈래(`docker exec -i kdt-ch31-postgres pg_dump …`/`pg_restore`에 표준 입력)를 한 번 돌려 볼 사람 — 교재 출력에서 한 번도 돌지 않음(검토 B-4).
10. **03 원자성 장면**: 문장 둘짜리 판(성공하는 칸 더하기 + 막히는 NOT NULL 칸)을 03에 더할지(검토 A-8 — 더하면 03 재실행·묶음 검사 해시·`bundle-execution.json`).
11. **`.moai` part7 스크립트 셋**: Ch 30 01이 막은 판 그대로 — Ch 31 작업은 기대지 않음. 처분은 사용자·강사.
12. **옛 기록 파일**: `qa/research.md`·`qa/verification.md`·`집필점검표.md` 머리에 「개선 전 판」 표시(내용 그대로 — 뒤 둘은 끝 「마감」 절) · `qa/upgrade/review-pack/`(검토에 쓴 마감 전 묶음 — 다시 만들지 않음) · `qa/technical-review.md`는 없음.
13. **과정 요약·계약(누적 문서 몫 — 오케스트레이터)**: 과정 요약에 Ch 31 줄(용어 표·**「버전」↔「판」 가름**·DB 준비 방식·동기·비동기 범위·실습 절 모델 0·도구 파일 없음) · `upgrade-contracts.md` §5 새 zip `6711c32a…`·`bundle-execution.json` 옛 값.
14. **`llm-practice.zip` 안 Ch 31은 옛 판** — 전체 묶음 재생성 때 Ch 31 17파일 대조.
15. **뒤 챕터 문장**(§19): Ch 32 04 b3·b7(Ch 32 개선 때).
16. **2차 검토**: 두 검토의 「확인하지 못한 것」과 §17-15.

## 21. 검토 1차와 반영 (2026-09-29 마감)

- 판정: **A(01~03·공통) 상 0 · 중 3 · 하 14**, **B(04~06) 상 1 · 중 2 · 하 6**. 합 **[상] 1 · [중] 5 · [하] 20 = 26건**.
- **반영 25건 · 미반영 1건(A-14)**. 선택지 가운데 반영하지 않은 것(검토가 둘 이상의 안을 준 곳): A-8 문장 둘짜리 판 장면 · A-17 실습 폴더 파일 고치기 · B-4 코드 고치기 · B-5 두 표를 묶는 장면 — 모두 §1(03~06 재실행 안 함)과 실습 절 규칙 때문, 강사 확인(§17).
- **[상] B-5 반영**(06 취소된 문의의 상태가 남는 까닭 — §12): b4 「실습 조립의 구성」(노드 함수가 끝나 상태를 내면 체크포인터가 적음 · 「두 표를 한 묶음 작업으로 함께 확정하는 설계는 이 절에서 실행하지 않았습니다」) · b6 넷째 단락 · 셀 [40] · 복습 4(물음 「배송 문의의 한 묶음 작업은 취소되었는데」·해설) · b7 둘째 항목(「함께 취소되는지 가르는 장면은 실행하지 않았습니다」) + 새 항목(설치판 소스 두 자리) · 학습 목표 3(「예약되지 않은 문의의 상태도 … 남는 까닭」) · 정리(b8·노트북) · handoff §6. 코드 그대로(06 `code_sha256`·`outputs_sha256` 같음). 캡션 06-1 「그 상태는 체크포인터가 따로 연 연결로 적힙니다」는 사실이라 그대로.
- **[중] 5건 모두 반영**: **A-1**(01 「닫히지 않고」 → 「서버와 끊기지 않은 채」 — b4 비유 다른 점·b4 엔진 단락(「라이브러리가 빌린 연결을 닫아 풀에 다시 넣지만 통로는 끊지 않음 · 04절은 반납」)·01-1 캡션·복습 1·노트북 [12]·정리 1·용어 표 「연결 풀」(「서버와 끊지 않고」)·**코드 주석 [11]**(01 재실행) — b10 「블록이 끝나 연결을 닫으면 풀에 놓인다」와 04 반납 정의와 맞음) · **A-15**(01 다섯 곳 + 출력 라벨 `데이터베이스와 서버 버전:`(01 재실행)·LOOK·b7 · 02 제목 셀 셋·[2]·[4]·b7 둘 · handoff 용어 표에 가름 한 줄) · **A-8**(03 [43]·b4 비유 다른 점·b4 한 묶음 작업 단락·b6·복습 3·03-3 캡션·alt·도식 읽기·`.mmd` 라벨 — 「판 함수가 실패해 판 번호를 적는 데까지 가지 않았다」 + 「문서대로라면 여러 문장 판은 함께 취소 — 이번에 실행하지 않음」, [44] 「취소되어」 → 「막혀」) · **B-3**(05 [44] 새 단락 · 복습 2 · b7 첫 항목(`--extension=vector`·DB 전체 — 노트북 밖에서) · b10(`-e`) · 05-2 캡션 「이름 공간을 골라 받은 … 확장은 들지 않았습니다」 · handoff §04 → §05 6 정정 — 마감이 노트북 밖에서 재현(§17-6)) · **B-4**(05 제목 셀 「앞자리(주 버전)가 서버와 같은 17인 명령이 안전」·[40](주 버전 두 문장 + `pg_dump_found = None` 한 줄 + 종료 코드 확인)·b7 두 항목(빈 파일인데 `덤프 파일이 생겼는가: True`가 찍힐 수 있음 — 셀이 종료 코드를 보지 않음)·b5 확인할 점·b10 · README — 코드 그대로).
- **[하] 20건 가운데 19건 반영**: A-2(01 [1] alt — 01 재실행이 생성기 글로 다시 씀) · A-3(「기다릴 초로 0을 넣으면」) · A-4(01-3 도식 읽기 — 「같은 연결」은 출력과 문서를 함께 읽은 것, b10 Pooling에 「풀은 연 연결을 메모리에 두었다가 다시 쓴다」) · A-5(01 [8] 엔진 「차단기·스위치」·[16] SQL 글 객체 「빈칸이 있는 신청서」 · 03 [6] 「계단」) · A-6(02 b4 새 단락·b10·[31] 새 단락 — `orig`은 SQLAlchemy가 DB-API 모양으로 바꾼 오류, 설치판 776~791행) · A-7(02 b7 「노트북 밖에서 … 찍어 보니」) · A-9(03 [64]·b6 끝 — NOT NULL이 막은 것은 새 칸의 빈 값, 빈 표는 노트북 밖) · A-10(03 [60] 「이 판의 판 내리기는 칸을 빼는 함수라」·b7 「백업이 있습니다」) · A-11(03 b7 제작 이력 문장 뺌) · A-12(03-2 결과 상자·alt·설계표) · A-13(03 [10] `replace` 첫 풀이·[44] 「3절에서 쓴」) · A-16(01 제목 셀·[12] 「여섯 절」·`pre_exec.sh` 주석 둘·README) · **A-17**(실습 폴더 파일은 고치지 않음 — 첫 판 설명 글이 03 출력 [27]에 찍혀 조건 불충족, `env.py`도 그대로 — 권고대로 마감 목록·최종 점검표에 「고치면 03 재실행·글 대조·묶음 검사」 기록) · B-1(04 [44]) · B-2(04 b7 `create_task` 풀이·「쓰레기 수거(garbage collection)」 풀이·「오류 출력(stderr)」 — 항목을 둘씩으로 나눔) · B-6(06 비유 다른 점) · B-7(06 b3 「노드가 문의를 차례로 받으므로 … 쓰지 않았습니다」·「배송 문의만 예약되지 않았고」·비유 「한 묶음 작업이 취소된 배송 문의」) · B-8(06-3 파랑 — §9) · B-9(§19·최종 점검표).
- **미반영 A-14**(03 1~2줄 셀 열둘 — 합치면 03 재실행·묶음 검사 해시, 강사 확인 §17-3).
- **마감이 더 고친 것(검토 밖)**: 05에 새로 쓴 「보장」 넷을 「장담」으로(챕터 금지어) · 01 b10 Pooling 한 문장(A-4 근거) · 06 b2 「예약되지 않은 문의의 상태가 저장되는지」 · **사용자가 금지한 표현(과정 규칙) 바꿈**: 챕터·실습 폴더 전체 `grep`에서 글자 그대로 나온 네 곳 — `qa/upgrade/01-diagnosis.md` 15행·`05-diagnosis.md` 16행·`handoff.md` 130행·273행(금지어 목록 줄) → 「사용자가 금지한 표현(과정 규칙)」(원고·노트북·생성기에는 없었음, `before/`·`review-pack/`에도 없음 — 기기 `.cache/ch31-0N/tools/ban3*.py`의 금지어 목록 문자열은 챕터 밖 도구라 그대로).
- **노트북 해시 전후**(`code_sha256` / `outputs_sha256`, 앞 12자 — `metadata.verification`과 다시 셈한 값 같음): **01 `addb4391b06f`/`145e0cf355cd` → `1566ad038be4`/`f8a551e4d649`(마감 재실행, `executed_at` 21:08:37Z)** · 02 `39d29f86a1f2`/`a44f100e3910` · 03 `f97cba07f5bc`/`875e6c2e50d4` · 04 `d919bdcdd61a`/`1673bbd94b67` · **05 `6269536315f3`/`8bac96cd5e64`** · 06 `bb245f74e657`/`139e24d3c384` — 02~06 전후 같음, `executed_at` 같음.
- **01 재실행 두 커널 대조**: A(루트 커널, `run_section.sh`) ↔ B(생성기 사본 `/tmp/ch31-close/B01`, `notebooks/` 커널 — A보다 먼저) 셀별 21개 가운데 19개 같음(다른 둘 = 실행 1 걸린 초 셀·두 실행 표) · `code_sha256` 같음 · 두 비교 `True` 둘 다 · 인용 값(01 결과 읽기·b6 표·확인할 점·RUNS_SENTENCE)은 새 A 출력과 같아 고칠 곳 없음 · G5 0.
- **생성기 대조**: 여섯 생성기를 메모리에서 실행해 셀·`src_html()`이 노트북·`_src`와 글자까지 같음(45/51/67/47/65/49, `_src` 6/6 — `.cache/ch31-close/tools/genmatch31.py`) · 캡션 파일이 생성기 `FIGn_CAP`과 모두 같음(`capsync31.py` — 01-1·03-3·05-2·06-3 새로 씀).
- **인용 대조**(숫자 없는 백틱 인용 포함, 여섯 절 노트북 마크다운 786·`_src` 614 — `quotes31.py`): 출력 값을 인용했는데 출력에 없는 것 0건. 남은 79건은 파일 이름·설치판 파일·API 이름·옵션·노트북 밖 확인 값(04 `QueuePool limit of size 2`·05 `--extension=vector` 등, 본문이 「노트북 밖에서」로 한정)·다른 절 출력 인용(04 b3 `풀에 둘 연결 수: 5`)·01 제목 셀 코드 블록 안 백틱의 거짓 양성. 마감에서 새로 생긴 것은 `--extension`·`--extension=vector`·`pregel/_runner.py`·`pregel/_loop.py`(옵션·파일 이름)뿐.
- **다시 렌더한 `.mmd`**: 03-2(A-12) · 03-3(A-8) · 06-3(B-8) — 모두 본문에만 있는 그림(노트북 첨부 아님), PNG를 열어 확인, viewBox 폭 481·274·625.
- **보호 파일 209개**: **같음 169 · 바뀜 38 · 옮김 2**(06절 뒤 181 · 28 · 0) — 옮김은 옛 생성기 둘, 바뀜 38 가운데 36이 마감에서 바뀜(둘은 06절 뒤 값 그대로인 공개 목록 두 곳), 모두 의도한 변경(파일별은 `manifest-changes.md` 「마감 뒤」).
- 고친 방법: `.cache/ch31-close/tools/gapply31.py`(Ch 30 `gapply30.py` 판 — 생성기 문자열 치환 수를 확인하고, 바뀐 생성기를 메모리에서 실행해 **코드 셀이 노트북과 한 글자라도 다르면 멈추고**, 달라진 마크다운 셀만 노트북에 옮긴 뒤 `src_html()`로 `_src`; 01은 `--gen-only`로 생성기·`_src`만 쓰고 `run_section.sh … 01`로 다시 실행) · `pregate31.py`(쓰기 전 G1~G6를 `/tmp` 임시 노트북으로) · `mkcopy.py`(01 B 사본) → `run_section.sh … NN --no-exec`(02~06) · `genmatch31.py`·`capsync31.py`·`bandiff31.py`(금지어 수 전후 — 늘어난 것은 「이벤트 루프」·「노드」 허용 말뿐)·`quotes31.py`·`nbhash31.py`·`manifest_check31.py`. 치환 목록 `.cache/ch31-close/reps/`.

## 22. 절차 메모

- 마감은 기기 셸 한 곳에서만 작업(`mcp__remote-devices__device_bash`, 셸 호출마다 `timeout` 170 안팎). 모델 요청 0 · 삽화 생성 0 · 파일 삭제 0(`rm` 0 — README 덮어쓰기에 `mv -f` 한 번) · 모든 파이썬 호출 `PYTHONDONTWRITEBYTECODE=1`(실습 폴더·챕터 pyc 새로 0) · 키 값 출력 0(`.env`를 열지 않음, 실행은 `OPENAI_API_KEY`를 지우고) · DB는 `pre_exec.sh`로만(같은 셸 호출 안에서 source) · 끝낸 뒤 postgres 프로세스 0·55431 포트 0.
- **기기 VM 재시작으로 `/tmp/pw`·`/tmp/pw-browsers`가 없어져 있었음** — 마감이 `/tmp`에만 다시 설치(`npm install playwright@1.63.0` → `npx playwright install chromium-headless-shell`, 캐시 `/tmp/npm-cache-ch31close`). Mermaid 도구 `/tmp/mmd`·`/tmp/libs`·`/tmp/pptr-cache`는 있었음.
- 옛 검사 스크립트의 사본을 만들 때는 결과 파일을 쓰는 줄을 먼저 막을 것(마감의 `check_figures` 사본이 한 번 써서 되돌림).
- 01 재실행은 **B를 먼저**(생성기 사본을 `/tmp`에 만들어 `notebooks/` 커널로 — 실습 폴더에 쓰지 않음) → A(`run_section.sh`) 차례가 안전.
