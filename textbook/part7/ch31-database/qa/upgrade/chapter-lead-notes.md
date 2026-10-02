# Ch 31 DB & 상태 영속화 — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part7/ch31-database`(절 다섯 — experiment 01·05, paired 02·03·04) · 실습 폴더 `labs/part7/ch31-database`(`chapter.json` `lab_path`와 같음). 바로 앞 Ch 30(완료, Part 7 첫 챕터)을 잇는 Part 7 둘째 챕터입니다. 뒤는 제외 챕터 Ch 32·33(Docker·CI/CD — 실습 절 없음)과 Ch 34입니다.
- 준비 산출물: `qa/upgrade/before/`(원본 사본 **55개, 714,599바이트** — 원본과 sha256 대조 55/55 같음) · `gates-before.json`(`63372b07…`) · `before-manifest.json`(**209개**, `b9bd5a88fc7d6bb40e506c393a116d5b39ea27b836b342facd9093a3b81fd168`) · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch31-database`(349MB, 사용자 디스크).
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(전부) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 과정 요약(§0~§9, 특히 §2-14·§2-19·§2-21·§5·§6·§7) · 계약 파일(`grep -n '^#'` 뒤 §3 Ch23·Ch30 줄·§5 Part 7 묶음 줄·§6 pgvector·§8 기준 버전) · Ch 30 `chapter-summary.md`(전부)·`chapter-lead-notes.md`(구조·§5-5·§6) · Ch 23 요약(§1·§4·§9·§15) · Ch 21 요약 64행 · Part 7 목록·목차·묶음·검사 스크립트 · 챕터 `qa/` 기록. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.
- **원고·노트북·그림·앱 파일은 하나도 고치지 않았습니다.** 연결 폴더 안 파일 삭제 0, 노트북 실행 0, 서비스 모델 요청 0, `uv cache prune` 안 함, 키 값 출력 0(`.env`에는 `OPENAI_API_KEY` 이름 하나만 있음 — `CH31_*` 이름 없음). 모든 파이썬 호출은 `PYTHONDONTWRITEBYTECODE=1`·`OPENAI_API_KEY`를 지운 환경. 실습 폴더에 새로 생긴 파일 0(`find -newer`).
- **삭제 한 가지(보고)**: 기기 `/tmp/ch31-prep/alem/`에 실습 폴더 `alembic.ini`·`migrations/`를 복사한 직후, 복사본에 딸려 온 `__pycache__` 두 폴더(맥 pyc)를 `rm -rf`로 지웠습니다. 제가 방금 만든 `/tmp` 복사본 안의 것이고 연결 폴더 원본은 그대로입니다(규칙상 `rm` 금지를 어긴 일이라 적어 둡니다).
- DB 서버는 `127.0.0.1:55431`·데이터 폴더 `/tmp/ch31-prep/pg/data`(39MB)에서 여러 번 켜고 끔(매번 `pg_ctl -m fast stop`), pgembed 서버는 `/tmp/ch31-prep/pgembed-data`(38MB, 유닉스 소켓만)에서 두 번 켜고 끔. **남은 postgres 프로세스 0, 5543x 포트 0.**
- `chapter.json` `hours` = 「총 16h · 강의 5h · 실습 11h」. 절 meta 강의 1·1·1·1·1 = **5h**, 실습 2·2·2·2·3 = **11h** — 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part7/_build_index.py` 20행 `(5, 11)`도 같습니다. 새 용어 meta 4·5·4·4·5 = 22.

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-29)

| 절 | 코드 셀 | 코드 줄 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 SQLAlchemy 비동기 PostgreSQL (experiment) | 5 | 47 | 84 | 3 | 1 | 3 | 0 | 7 | 20 | 3 | 37 |
| 02 트랜잭션과 원자성 (paired) | 5 | 48 | 84 | 4 | 0 | 3 | 0 | 7 | 15 | 3 | 32 |
| 03 Alembic 적용과 롤백 (paired) | 6 | 42 | 82 | 3 | 0 | 4 | 0 | 8 | 17 | 3 | 35 |
| 04 커넥션 풀 고갈과 대응 (paired) | 4 | 42 | 83 | 0 | 1 | 2 | 0 | 6 | 14 | 3 | 26 |
| 05 pgvector 체크포인터 공존과 백업 (experiment) | 7 | 94 | 101 | 4 | 3 | 5 | 0 | 9 | 21 | 3 | 45 |
| **합계** | **27** | **273** | **434** | **14** | **5** | **17** | **0** | **37** | **87** | **15** | **175** |

- 통과 절 **0/5**. 코드 줄은 주석·빈 줄 뺀 값(`%pip` 줄 포함, `/tmp/ch31-prep/ast_scan.py`), 셀 최대 16·14·13·18·**25**줄.
- G1 14 = 내포식 7(01 [10]·[13] `[await … for …]` · 02 [9]·[12] `[row.balance for …]` · 03 [7] `candidates` · 05 [10]·[14] `[row[0] for …]`) · 제너레이터 식 5(01 `gather(*(… for …))` · 02 `sum(row.balance for …)` 둘 · 03 `next(path for …)` · 05 `"\n".join(… for …)`) · `*args` 정의 1(03 `def alembic(*args: str)`) · **`lambda` 1(05 노드)**.
- G2 5 = 15줄 넘는 셀 01 [13]·04 [8]·05 [10]·[14]·[17].
- G3 17 = **첫 줄 주석 없는 코드 셀 17**(설치 셀·주소 셀만 주석 있음).
- G4 0 — **다섯 절 모두 모델을 부르지 않음**(키 셀·모델 셀 0).
- G5 37 = 제목 셀·핵심 그림 첨부 없음 10 + 결과 읽기 인용 없음·빠짐 27.
- G6 87 = 70자 넘는 문장 38 · 영문 시작 조사 39 · 5문장 넘는 단락 8 · 금지어 2(02 「되돌립니다」가 게이트 금지어 「돌립니다」에 걸림).
- G7 15 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 것 (AST로 따로 셈 — 노트북 27셀)

- **비동기**: 셀 맨 위 `await`(01·02·04 모든 본 셀) · 셀 맨 위 `async with engine.begin()`·`engine.connect()`(01·02·04) · 셀 안 `async def`(01 둘·04 둘 — 셀당 하나) · 셀 맨 위 목록 내포식 안 `await`(01 `[await read_question(i) for …]`) · **`asyncio.create_task`(04 둘 — Ch 2 요약 「처음 쓰면 한 문장」)** · `asyncio.gather(*…)`(01 — 별표 풀기, Ch 18 03 선례) · `asyncio.sleep(0.05)`(04).
- **힌트**: `item_id: int`·`-> str`·`delay: float`·`-> None`·`-> int`·`*args: str`(01·03·04 — 반환 힌트 포함, Ch 30은 노트북 반환 힌트 0) · 05 `class State(TypedDict)`를 **`with` 블록 안에서 정의**하고 `from typing_extensions import TypedDict`도 블록 안.
- **그 밖**: f-string 형식 지정 `f"sequential={sequential_s:.3f}s, …"`(01) · `try/except RuntimeError as exc`(02 두 셀 — **`raise RuntimeError("입금 직전 장애")`를 코드가 직접 던짐**, After 셀은 `raise` 뒤에 닿지 않는 줄 하나) · `except RuntimeError: pass`(02) · `try/except TimeoutError as exc`(04 — **`from sqlalchemy.exc import TimeoutError`가 내장 이름을 가림**, §7-1) · `os.environ | {…}` 딕셔너리 합치기(03) · `(Path.cwd(), *Path.cwd().parents)`(03) · `next(…)`(03) · `import os, subprocess`(03·05 한 줄 두 모듈) · `sum`(02) · `type(exc).__name__`(02·04) · `.all()`·`.fetchone()[0]`·`.fetchall()`·`.scalar_one()`·`row.balance`(행 속성) · `"\n".join`·`.splitlines()[-1]`(03 호출 사슬) · `assert … and …`(01·05 한 줄 두 조건).
- **시간 `assert`**: 01 `assert sequential == concurrent and concurrent_s < sequential_s` — 걸린 초를 `assert`로 봄(§6 흔들림).
- 실습 폴더 파일(학생이 여는 파일 — Ch 28 A-17 「서버 파일도 금지 문법 0」 선례 대상): `app/models.py` `class Base(DeclarativeBase)`·`class Ticket(Base)`·**`Mapped[int]`·`Mapped[str]` 힌트가 칸을 정함**·`__table_args__` · `app/db.py` `async def session_scope() -> AsyncSession`(쓰는 곳 0) · `app/service.py` `async with`·`await session.scalars`·`list(rows)`·`asyncio.run` · `migrations/env.py` **조건 표현식**(35행 `run_migrations_offline() if … else …`)·반환 힌트·`or {}` · 새 리비전 `20260911_01_create_tickets.py` 반환 힌트 둘 · 다섯 파일 모두 `from __future__ import annotations`(리비전 빼고).
- 코드 셀은 옛 생성기 `qa/author_ch31.py`의 `NBS`와 **글자까지 같고**, 마크다운 셀은 절마다 넷(05는 다섯) 더 있음 — 2026-09-14 `.moai` part7 보조 스크립트가 끼운 「이 준비 셀이 하는 일」·「바로 다음 코드를 읽는 방법」·「이 단계에서 구분할 범위」(Ch 30과 같은 모양).

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 요청 | DB 준비·정리 | 파일 쓰기 | 손 값 | `assert` 대상 |
|---|---|---|---|---|---|---|
| 01 | `create_async_engine(pool_size=3, max_overflow=0)`·`async_sessionmaker(expire_on_commit=False)` → 이름 공간 `ch31_async` 표 `requests` 세 줄(`환불·배송·결제`) → 세션마다 `text(…)` 조회 `['환불', '배송', '결제']` → `pg_sleep(0.15)` 조회 셋 순차 ↔ `asyncio.gather` 동시 `sequential=0.468s, concurrent=0.195s` → `engine.dispose()` | 0 | `DROP SCHEMA IF EXISTS ch31_async CASCADE` → 다시 만듦(노트북 첫머리, 끝에서 지우지 않음) | 0 | 0.15초 · 풀 크기 3 · 세 줄 | 목록 · **걸린 초 부등식** |
| 02 | 이름 공간 `ch31_tx` 표 `accounts`(`CHECK(balance>=0)`, 500·500) · Before 출금만 `engine.begin()`으로 확정 → **코드가 `raise RuntimeError`** → `[(1, 400), (2, 500)] total: 900` · After 출금·(닿지 않는) 입금을 한 블록 → `[(1, 500), (2, 500)] total: 1000` | 0 | 이름 공간 다시 만듦 · After 앞에서 `UPDATE … SET balance=500`으로 되돌림 | 0 | 100원·500원 | 잔액 목록 |
| 03 | 파일 위치(`alembic.ini`) → `subprocess.run(["alembic", …])` 함수 → 이름 공간 `ch31_migration` 지우고 `upgrade head`(`Running upgrade  -> 20260911_01`) → `to_regclass` `ch31_migration.tickets` · Before `downgrade base` → `None` · After `upgrade head` 다시 → 표 되살아남 | 0 | 이름 공간 지움(psycopg `autocommit`) · Alembic 버전 표는 `ch31_migration.alembic_version` | 0(단 Alembic 자식 프로세스가 `migrations/__pycache__`에 pyc를 쓸 수 있음 — 실습 폴더에 맥 pyc가 이미 있음) | 리비전 `20260911_01` | 표 이름 · `None` |
| 04 | `pool_size=1, max_overflow=0, pool_timeout=0.2` · `create_task(hold(0.6))` + `sleep(0.05)` 뒤 둘째 → `sqlalchemy.exc.TimeoutError`(Before) · After `pool_timeout=1.0`·첫 작업 0.25초 → `1 1`·`pool.status()` 글 | 0 | 표 없음(`SELECT pg_sleep`) · `dispose()` | 0 | 0.6·0.05·0.2·0.25·1.0초 | 오류 이름 글 · `second == 1` |
| 05 | `CREATE EXTENSION vector`(기본 이름 공간 `public`) · 이름 공간 `ch31_shared` 표 `documents`(`vector(3)` 세 줄)·HNSW(`vector_cosine_ops`) · `<=> '[0.9,0.1,0]'` → `['배송', '환불']` · `EXPLAIN (ANALYZE, BUFFERS, COSTS OFF)` → Seq Scan, `uses hnsw: False` · `PostgresSaver.from_conn_string(…)`+`setup()`+노드 하나(`lambda`) 그래프 `{'value': 12}`·체크포인트 3줄 · **`docker exec kdt-ch31-postgres pg_dump …`** → `dropdb`/`createdb ch31_restore` → `CREATE EXTENSION vector` → `psql`로 복원 → `(3, 3)`·HNSW `True` | 0 | 이름 공간·복원 DB 다시 만듦(지우지 않음) | 0(덤프는 문자열로 받음) | 벡터 셋·질의 벡터 | 가까운 문서 · `"Scan" in plan` · 값 12·체크포인트 > 0 · 복원 줄 수 |

- **서비스 요청 합계(한 번 실행)**: 다섯 절 **0**(API 키 셀도 없음). 05 체크포인터 절도 모델을 쓰지 않는 그래프(노드 하나가 값 두 배).
- **`temperature=0`·`reasoning_effort="none"`**: 해당 없음(모델 셀 0).
- **DB 연결 글(값은 로컬 수업 전용 기본값)**: 환경 변수 **`CH31_DATABASE_URL`**(없으면 `postgresql+asyncpg://…@localhost:55431/ch31_lab`) → 노트북이 `replace`로 `SYNC_URL`(`postgresql+psycopg`)·`NATIVE_URL`(`postgresql`)을 만듦 · Alembic `env.py`는 **`CH31_SYNC_URL`**(없으면 같은 서버의 psycopg 주소) · 05는 **`CH31_POSTGRES_CONTAINER`**(없으면 `kdt-ch31-postgres`). **노트북은 `.env`를 읽지 않음**(`dotenv` 가져오기 0 — README 「`.env`의 `CH31_DATABASE_URL`」은 사실과 다름, `python-dotenv`는 의존에만 있음).
- **파일 위치**: 03만 `alembic.ini`를 찾음(후보 = 지금 폴더와 모든 부모 + `labs/part7/ch31-database`·지금·부모) — 루트 커널(`execute.py`)·`notebooks/`·묶음 세 자리 모두 찾음.
- **흔들리는 값**: 01 걸린 초(교재 0.468·0.195 / 이 기기 0.468~0.472·0.157~0.190) · 04 둘째 작업이 기다린 초(0.204~0.211 — 출력 안 함) · 05 `EXPLAIN ANALYZE`의 `actual time`·`Buffers`·`Planning/Execution Time` 줄 · 덤프 줄 수·아카이브 바이트(판마다 다름). **결정적 값**은 §7.
- **옛 그림 토큰**: 절마다 b4 「도식 읽기」의 `{{svg:NN-흐름}}` 하나(`figures/_gen_figures.py` — SVG·excalidraw 다섯 쌍, `textbook/part5/_figure.py`는 안 씀) · 노트북 토큰 paired `{{notebook:slug|example}}`+`{{notebook:slug|failure}}`, experiment `{{notebook:slug}}`. 도식 읽기 틀 문장이 「푸른·**붉은**·초록·보라」 상자를 처리 단계로 씀(실패가 아닌 요소에 빨강 — 과정 색 규칙과 다름). Mermaid·삽화 0장. **챕터 공개 목록에 옛 SVG 줄 없음.**
- 노트북 `metadata.verification`: 다섯 모두 `passed`, 실행일 **2026-09-11**(사용자 맥 + Docker 컨테이너), 코드 셀 5·5·6·4·7 = 27, `code_sha256` 01 `de578491…`·02 `63d17b06…`·03 **`b0594f2d…`**(Part 7 묶음 실행 기록과 같음 — §5-4)·04 `d8f007b1…`·05 `e0c4d380…`.
- 노트북 설명 셀: 제목 한 줄 「실제 PostgreSQL 17에서 운영 데이터베이스의 한 가지 문제를 재현하고 해결합니다」(다섯 절 같은 글 — experiment 01·05에도) · 결과 읽기 셀 0 · 준비물(DB 준비·요청 수·시간)·실행일 문장 없음 · 첨부 그림 0.
- `_src` 틀(옛 생성기 `qa/author_ch31.py`): b4 「운영에서 경계를 정하는 방법」·「코드 읽기와 개념 경계」 긴 단락 · b6 끝 공통 문장 「이 결과는 Docker의 독립 PostgreSQL 17.8 컨테이너와 작은 데이터에서 측정했습니다 …」(다섯 절 같은 글 — 02·03·05는 시간을 재지 않음) · 복습 넷(05 다섯) · 참고 자료(확인 2026-09-11) · b10 공통 「확인 필요 항목」.

### 금지어·주의 말 (`_src` 산문 / 노트북 마크다운 / 코드 주석 — 코드 백틱·`<pre>` 뺌, `/tmp/ch31-prep/ban.py`)

| 절 | 걸린 말(수) |
|---|---|
| 01 | **세션 21/6** · SQL 11/7 · 풀 11/1 · 드라이버 6/2 · 쿼리 6/2 · 운영 5/1 · 트랜잭션 4/1 · 이벤트 4 · 주문 4 · **요청 함수 2·경로 함수 1(Ch 30 인계)** · 엔진 3/1 · 경로 3 · 반환 2/1 · 측정·보장·팩터리·배포 2 · 지연·체크아웃·백업·복구·동시성·부하·의존성·계획 1 · **식당 1(비유 — Ch 19 「식당 주문 전표」 겹침)** · Docker·컨테이너 1 |
| 02 | **트랜잭션 22/3** · 롤백 12/2 · 장애 8/1 · SQL 7/6 · 격리 6/1 · 원자 6/2 · 커밋 4/1 · 멱등 4 · 운영 4/1 · 보장 3/1 · 재시도 3 · 식별자 2 · 불변식·정합성 1/1 · 세션 2 · 마이그레이션·풀·검증·측정·로그·백업·복구·배포·계획 1 · **창구 1(비유 — Ch 6 01-5 「상담 창구」 겹침)** · 「실패 재현」 0/1 |
| 03 | **리비전 16/3** · 운영 10/1 · 롤백 9/2 · 마이그레이션 7/2(주석 1) · DDL 7 · 배포 7/1 · 스키마 6/2 · 복구 5/2 · 측정 4/1 · 백업·복원 4 · 경로 3 · SQL 3/6 · 인덱스·반환·보장·로그·확장 2 · 가역 1/1 · 필드·검증·식별자·인스턴스·트랜잭션·풀·장애 1 · 도면 2(비유) · 「되돌」 1/1 |
| 04 | **풀 25/6** · 반환 11/1 · 쿼리 10/3 · SQL 8/5 · 체크아웃 5 · 최대 5/2 · 운영 5/1 · 트랜잭션 3/1 · 마이그레이션 3 · 인스턴스 2/1 · 처리량 2 · 지연 2 · 백업 2 · 백프레셔·재시도·색인·이벤트·체크포인터·부하·배포 1 · 태블릿 1(비유 — 도서관) · 「실패 재현」 0/1 |
| 05 | **인덱스 24/5** · 백업 20/6 · HNSW 17/5 · 복원 14/2 · 체크포인터 13/5 · 복구 11/2 · 스키마 10/8 · SQL 8/9 · 운영 7/3 · 덤프 6/1 · 계획 6/3 · 스레드 6/1 · 확장 5/1 · 검증·측정·최적(화기)·쿼리·스캔 3 · 평가셋 2(「Ch11 평가셋」 — Ch 29·30 인계와 같은 느슨함) · 스냅샷·WAL·지연·명시 1 · **창고 2(비유 — Ch 3 「창고 선반」 겹침)** · Docker·컨테이너 1/1 |

- **과정 금지어와 챕터 주제가 부딪힘**: Ch 23 금지어 「트랜잭션」·「마이그레이션」(DB 뜻)·「스냅샷」·「보장」 · Ch 30 금지어 「스키마」·「반환」·「검증」·「경로」·「필드」 · Ch 25·18 「지연」·「측정」 · Ch 21 「런타임」 · Ch 15 「레코드」 · Ch 28 「세션」(→ 연결). 이 중 **트랜잭션·마이그레이션·세션·풀·스키마·롤백·커밋**은 이 챕터의 학습 대상입니다(§10-4).
- **앞 챕터가 정한 말**: Ch 23 02 SQL `SCHEMA` = **「이름 공간」**(제목의 「스키마」 = 표 구조와 나눔) · `setup()` = **「표 만들기」** · Ch 21 04 「옮기기(마이그레이션, migration)」 = 코드 판 옮기기 — **「Ch 23 02·Ch 31 03의 DB 「마이그레이션」과 다른 뜻」**(Ch 21 요약 64행) · 「체크포인터」·「스레드」는 Ch 23 01이 정의(05가 새 용어로 세면 겹침 — Ch 23 요약 §15 211행).
- 제목의 영어·약어·기호: 챕터 「DB & 상태 영속화」(`_notebook/build_index.py` 66행은 「DB와 상태 영속화」 — 두 이름) · 01 「SQLAlchemy」·「PostgreSQL」 · 02 「트랜잭션」 · 03 「Alembic」·「롤백」 · 04 「커넥션 풀」(`_build_index.py`·Ch 30 요약은 「연결 풀」) · 05 「pgvector」·「체크포인터」. 슬러그 01은 Ch 30 10 b8·Part 7 목차가 링크(§5-3) — 고정.

## 2. 절별로 더 봐야 할 것

### 01 SQLAlchemy 비동기 PostgreSQL (experiment)
- 학습 질문이 「비동기가 같은 대기 조회 셋의 걸린 시간을 어떻게 바꾸나」 — **시간이 주제인 절**(Ch 25 03·Ch 15 05 선례): 결론·그림·정리에는 결정적 부등식·차례만, 초는 결과 읽기 둘째 단락·표·b7에만(과정 요약 §7 「§2-7 9번 끝 적용 선례」). 지금 `assert concurrent_s < sequential_s`는 이 기기에서 3/3 참이었으나 시간 `assert`임.
- b2·b3 「Ch30에서 FastAPI 요청 함수/경로 함수를 비동기로 작성」 — 뜻은 참, 말은 Ch 30 「처리 함수」로(Ch 30 요약 §19).
- 세션 하나를 `gather` 두 작업이 함께 써도 **이 설치판에서는 오류가 나지 않았음**(asyncpg 어댑터가 한 연결의 실행을 차례로 세움 — `/tmp/ch31-prep/exp/e2_async.py`, 결과 `['환불', '배송']`). 공식 문서는 「A single instance of AsyncSession is not safe for use in multiple, concurrent tasks」라고 씀 → 「같이 쓰면 오류」로 쓰지 말고 문서 근거로만.
- 「비동기 함수 안 동기 드라이버가 이벤트 루프를 멈춤」(b7)은 실행하지 않은 설명(Ch 30 01이 같은 설명을 이미 둠).
- 비유 「식당 주문 담당자」는 Ch 19 가족과 겹침.

### 02 트랜잭션과 원자성 (paired)
- Before가 **코드가 직접 던진 `RuntimeError`** — Ch 30 판정 기준으로 실제 결함 장면이 아님. 표에 이미 `CHECK(balance>=0)`가 있어 **실제 제약 위반**으로 바꿀 수 있음(§3, 두 번 실행 같음).
- b2 「사용량 차감·메시지 저장·작업 상태 갱신」, b7 「멱등성 키와 보상 작업」(보상 작업은 Ch 23이 다루지 않음 — Ch 31 몫, Ch 23 요약 210행) · b3 「Ch23 중단 뒤 재개와 멱등성」 참(Ch 23 04~07).
- 격리 수준·`SERIALIZABLE`·재시도는 실행 안 함(본문이 한정함).
- 세션 판 `async with Session() as s: async with s.begin():`도 같은 결과(`IntegrityError` 뒤 줄 그대로 — e3).

### 03 Alembic 적용과 롤백 (paired)
- Before `downgrade base` → 표 없음은 **downgrade가 하라는 일을 한 것**(결함 아님), After는 다시 `upgrade`(고친 것 없음). 실제 조건 후보 셋을 확인함(§3).
- `subprocess.run(["alembic", …])`는 **`PATH`에 가상환경 `bin`이 있어야** 돎 — 이 기기에서 가상환경 파이썬만으로는 `shutil.which('alembic')` = `None`(학생이 VS Code에서 `.venv` 커널을 골라도 `PATH`는 보장되지 않음). 과정 관례 `subprocess.run([sys.executable, "-m", "alembic", …])`는 이 기기에서 돎(e4).
- `env.py`에 `target_metadata`가 없어 **자동 생성(`revision --autogenerate`)이 모델을 볼 수 없음** — b4·b7·복습 3이 자동 생성을 설명하지만 실행한 적 없음. `alembic check`은 `Target database is not up to date.`(종료 255)로 끝남(버전이 head가 아닐 때).
- 이름 공간 만들기가 `env.py`(`CREATE SCHEMA IF NOT EXISTS` + `commit`)와 리비전 `upgrade()` 두 곳에 있음 · 버전 표 이름 공간 `ch31_migration`.
- 리비전 설명 글 「상담 티켓 표 구조를 변경합니다」(실제로는 표를 **만듦**) — 출력 줄에 그대로 찍힘.
- Alembic 자식 프로세스는 `migrations/`의 `.py`를 가져오므로 `PYTHONDONTWRITEBYTECODE`를 넘기지 않으면 실습 폴더에 pyc가 생김(지금 있는 pyc 셋은 2026-09-11 맥 판).

### 04 커넥션 풀 고갈과 대응 (paired)
- Before는 **실제 조건**(풀 한도·짧은 대기 제한) — 이 기기 5/5 `TimeoutError`, `sleep(0)`으로 줄여도 3/3(QueuePool이 연결을 만들기 전에 자리를 먼저 셈). 첫 연결에 0.051초가 걸려 `sleep(0.05)`와 거의 같았지만 결과는 같았음.
- After는 **설정값 바꾸기**(대기 제한 1.0 > 점유 0.25) — 결함 코드를 고친 것은 아님. 「반납을 잊은 연결」(`conn = await small.connect()` 뒤 닫지 않음)이 타이밍 없이 결정적인 다른 후보(§3).
- **`from sqlalchemy.exc import TimeoutError`가 내장 `TimeoutError`를 가림** — `sqlalchemy.exc.TimeoutError`는 내장 `TimeoutError`의 하위 클래스가 **아님**(MRO `TimeoutError → SQLAlchemyError → HasDescriptionCode → Exception`). Ch 16 05에서 배운 `except TimeoutError`(내장)로는 이 오류를 못 받음 → 이름 가르기 필요.
- b1·b6 「연결을 일찍 반환」, b4 「`pool_pre_ping`·`pool_recycle`·백프레셔」(실행 안 함), b7 「상위 백분위수」.

### 05 pgvector 체크포인터 공존과 백업 (experiment)
- **Docker 전제**: `docker exec kdt-ch31-postgres pg_dump/dropdb/createdb/psql` — Docker 없는 곳(이 기기)에서는 그대로 못 돎. 로컬 `pg_dump`(서버 판 이상)로 바꾸면 이 기기에서 돎(§4).
- 노드가 `lambda` · 상태 형식 클래스를 `with` 안에서 정의 · 코드 셀 25줄.
- b3 「Ch12 pgvector 거리 연산과 HNSW」 참(Ch 12 02) · 「Ch23 PostgresSaver `setup()`」 참(Ch 23 02 — Ch 23은 `PostgresSaver(conn)`에 `psycopg.connect(…, autocommit=True, row_factory=dict_row)`로 만든 연결을 넘김, 05는 `from_conn_string`) · **새 용어 「체크포인터」는 Ch 23 01 말**.
- b6 「복원 뒤 스레드 재개는 범위 밖」 — 복원 DB에서 같은 그래프·같은 `thread_id`로 `get_state(...).values` = `{'value': 12}`를 이 기기에서 확인(e6) — 넣으면 「재개」 대신 「저장된 상태 읽기」까지 보일 수 있음.
- 확장 `vector`는 `public`에 있어 이름 공간 덤프에 `CREATE EXTENSION`이 **없음** → 복원 DB에 확장을 먼저 만들지 않으면 `ERROR: type "public.vector" does not exist`(종료 3) — 실제 조건 실패 장면 후보(experiment 절이라 노랑).
- b8 「Ch32에서 Compose 서비스로 묶고 헬스체크와 시크릿」 — Ch 32는 제외 챕터(개선 대상 아님, `ch32-docker/04`는 있음). b7 「Ch11 평가셋으로 변경 전후를 측정」은 실행 안 함.
- 비유 「창고와 배송 장부」는 Ch 3 가족과 겹침.

## 3. paired 절 Before 판정 (§5-3 빨강 = Before 결함 결과)

| 절 | 지금 Before | 실제 결함인가 | 모델 없이 결정적인가 | After가 결함을 고치는가 | 실제 조건 후보 (모두 설치판·이 기기 PostgreSQL 17.11에서 확인, 결정적) |
|---|---|---|---|---|---|
| 02 | 출금만 확정 → 코드가 `raise RuntimeError` → 900 | **아님**(일부러 던진 예외) | 예 | 예(한 블록 롤백) — 다만 After에 닿지 않는 줄 | **CHECK 위반**: 입금 +600을 따로 확정 → 출금 −600이 `IntegrityError`(`CheckViolationError`, SQLSTATE `23514`, `new row for relation "accounts" violates check constraint "accounts_balance_check"`) → **`[(1, 500), (2, 1100)]` 합 1600** ↔ 한 `engine.begin()` 블록 → 같은 오류 뒤 **`[(1, 500), (2, 500)]` 합 1000** (두 번 실행 같음, `e3_tx.py`) |
| 03 | `downgrade base` → 표 없음 | **아님**(명령대로 됨) | 예 | 아님(다시 올리기) | ① **NOT NULL 칸 추가 실패**: 줄 셋이 든 표에 기본값 없는 `nullable=False` 칸을 더하는 리비전 → `upgrade head` 종료 **1**, `psycopg.errors.NotNullViolation: column "owner" of relation "tickets" contains null values` · 버전 `20260911_01` 그대로 · 칸 없음(PostgreSQL DDL이 한 트랜잭션이라 반쯤 적용 없음) ↔ `server_default` 판 → 종료 0·버전 `20260929_02`·세 줄 모두 기본값 · ② **downgrade 뒤 데이터 사라짐**: 줄 3 → `downgrade base` → `upgrade head` → 줄 **0** · ③ **downgrade 없음**(`pass`): 표가 남고 버전 줄 0 → 다시 `upgrade head` 종료 1 `DuplicateTable: relation "tickets" already exists` (`e4_alembic.py`·`e4b_nodown.py` — 복사본 폴더에서, 실습 폴더 리비전은 그대로) |
| 04 | 크기 1 풀을 0.6초 점유 중 둘째 요청 대기 0.2초 → `TimeoutError` | **예**(실제 한도) | 예(5/5·`sleep(0)` 3/3) — 기다린 초만 흔들림 | 설정 바꾸기(1.0초) | 지금 장면 유지 가능. 타이밍 없는 후보 **반납 누락**: `conn = await small.connect()`로 빌리고 닫지 않음 → `pool.status()` `Current Checked out connections: 1` → 둘째 `async with small.connect()` → `TimeoutError`(`QueuePool limit of size 1 overflow 0 reached, connection timed out, timeout 0.20`) ↔ `async with`로 빌림 → 둘 다 `1`·`Checked out connections: 0` (3/3, `e5_pool.py`) |

- 빨강은 paired Before 결함 결과만(과정 요약 §8). experiment 01·05에서 받은 오류(예: 05 확장 없이 복원)는 노랑.

## 4. DB 준비 경로 — 이 기기 시험 결과 (가장 중요)

### 4-1. 옛 원고가 쓰는 방법
- **Docker**: README `docker run --name kdt-ch31-postgres -e POSTGRES_PASSWORD=… -e POSTGRES_DB=ch31_lab -p 55431:5432 -d pgvector/pgvector:0.8.1-pg17`(**`127.0.0.1`에 묶지 않음** — Ch 12는 `-p 127.0.0.1:55432:5432`) · 05가 `docker exec`로 `pg_dump`·`dropdb`·`createdb`·`psql` · 다섯 절 b6 「Docker의 독립 PostgreSQL 17.8 컨테이너」 · `qa/verification.md` 「`kdt-ch31-postgres`, `localhost:55431`, PostgreSQL 17.8, pgvector 0.8.1」.
- **과정의 앞선 학생 경로**: Ch 12 02 컨테이너 `hankyung-part3-pgvector`(`pgvector/pgvector:0.8.2-pg17`, `postgresql://student:…@127.0.0.1:55432/rag_lab`) → **Ch 23 02가 같은 컨테이너·접속 글을 다시 씀**(이름 공간 `ch23_lab`). Ch 31은 따로 컨테이너(포트 55431·다른 이미지 판·다른 계정)를 만듦 — 과정 안에서 PostgreSQL 컨테이너가 둘이 됨. Ch 32 04는 Ch 31 파일을 읽지 않고 제 `compose.yaml`(`pgvector/pgvector:0.8.6-pg17-bookworm`)·`init.sql`.
- SQLite 흉내·가짜 엔진: 없음.

### 4-2. 이 기기에서 실제로 돈 것
| 경로 | 결과 | 판 | pgvector | `pg_dump`·`pg_restore` | 바인딩·데이터 폴더·끄기 | 크기 |
|---|---|---|---|---|---|---|
| **A. conda-forge PostgreSQL**(Ch 12가 둔 `$ROOT/.cache/vm/pgenv`) | **돎** — `initdb` 0.5초 → `pg_ctl … -o "-p 55431 -c listen_addresses=127.0.0.1 -k /tmp/ch31-prep/pg"` → `createdb ch31_lab` → `CREATE EXTENSION vector` → 01~05 모든 후보 확인(§3·§7) → `pg_ctl -m fast stop` | PostgreSQL **17.11**(aarch64-conda-linux-gnu) | **0.8.1** | 있음(17.11) · `psql`·`createdb`·`dropdb`·`pg_isready` 있음 | `127.0.0.1:55431`만 · 데이터 `/tmp/ch31-prep/pg/data` · 셸이 끝나면 `trap EXIT`로 끔(`/tmp/ch31-prep/pgup.sh`) | 환경 173MB(이미 있음) · 새 클러스터 39MB |
| **B. `pgembed` 0.2.0**(pgserver 갈래, PyPI 2026-03-18) | **서버는 돎** — `pgembed.get_server("/tmp/…")` 0.42초 → psycopg·**SQLAlchemy+asyncpg**(`?host=/소켓 폴더`) 연결 됨 · **딸려 온 `psql`은 이 기기에서 `--version`부터 세그폴트(-11)** | PostgreSQL **17.9** | **0.8.2** 들어 있음(+ `vectorscale`·`pg_textsearch`·**`pg_search`(ParadeDB, AGPL-3.0)**) | `pg_dump`·`pg_restore` 17.9 됨 | **POSIX는 유닉스 소켓만**(`listen_addresses ''`, `-h ""`) · Windows는 `127.0.0.1` + 빈 포트 · 파이썬 프로세스가 끝나면(atexit) 또는 `cleanup()`으로 끔 · README의 `pgembed.POSTGRES_BIN_PATH`는 맨 위에 없음(`pgembed._commands.POSTGRES_BIN_PATH`) | 휠 68MB(맥 83MB·Win 14MB) · 설치 133MB · 시험 가상환경 `$ROOT/.cache/vm/pgembed-try` **204MB**(사용자 디스크) |
| C. `pgserver` 0.1.4(2024-06, 갱신 없음) | **이 기기 설치 불가** — 리눅스 aarch64 휠 없음(맥 x86·arm64·리눅스 x86_64·Win만, Python 3.9~3.12) | PostgreSQL 16.2 | 0.6.2(맥 휠 안 확인) | 있음(맥 휠) | pgembed와 같은 설계(소켓) | 휠 10~13MB |
| D. `postgresql-binaries` 18.6.0(2026-09-20) | 휠 목록만 원격으로 읽음(설치 안 함) | 16·17·18 판 | **없음**(05 불가) | 있음 | 직접 `initdb`·`pg_ctl` | 휠 12MB |
| E. `testing.postgresql`·`pytest-postgresql` | 시험 안 함 — 시스템 PostgreSQL을 **따로 설치해야** 씀(번들 아님) | — | — | — | — | — |
| F. `postgresql-wheel` 14.1.2(2021) | 시험 안 함 — Python 3.7~3.9·리눅스 x86만 | 14 | 없음 | — | — | — |
| G. Docker | 이 기기에 없음(과정 조건) — 선택지에서 뺌. 학생 경로로는 Ch 12·23 선례 | — | — | 컨테이너 안 | — | — |

- **학생 환경(맥·윈도·리눅스)에서 같은 방법인가**: Docker(Ch 12·23 선례)는 세 OS 같음(Docker Desktop 필요, 명령·`docker exec`까지 같음). `pgembed`는 **맥은 Apple Silicon·macOS 15 이상 휠만**(0.1.7~0.2.0 모두 `macosx_15_0_arm64` — 인텔 맥·macOS 14 이하 설치 불가), 리눅스 x86_64·arm64(glibc 2.28+), Windows x64 — POSIX(소켓)와 Windows(TCP 포트)의 연결 글 모양이 다름, 확장 번들 차이(윈도 휠엔 `pg_search` 없음), 0.x 판·문서와 코드 어긋남. conda-forge는 세 OS 모두 되지만 conda/mamba가 필요하고 173MB.
- **작업 기기 방식(교재 출력용)**: Ch 12·23 선례 그대로 `qa/upgrade/pre_exec.sh`로 절 실행 직전에 pgenv 클러스터를 `/tmp` 데이터 폴더에 켜고 `trap EXIT`로 끔. Ch 31은 **다섯 절 모두 DB가 필요**(Ch 23은 02만) → `N` 조건 없이 켜야 함. 접속 글·포트를 학생 글과 같게(55431 또는 Ch 12의 55432 — 55432를 고르면 Ch 12 서버와 겹치지 않게 Ch 23처럼 「이미 받는 서버가 있으면 멈춤」).
- **연결 폴더와 DB**: 이번에는 데이터 폴더를 모두 `/tmp`에 두어 연결 폴더 PostgreSQL은 시험하지 않았습니다. 참고로 Ch 12의 `pre_exec.sh`는 데이터 폴더를 연결 폴더(`.cache/vm/pgdata`, 64MB)에 두고 절마다 켜서 썼습니다(계약 §6) — Ch 23은 `/tmp/ch23-02/pgdata`로 옮겨 씀. SQLite는 이 챕터에 없음.

## 5. 실습 폴더 구조와 읽는 곳

```
labs/part7/ch31-database/
  README.md (a54f0fd5… — docker run / uv sync --project / uv run … python -m app.service / docker rm)
  pyproject.toml (449bed56…) · uv.lock (161,823바이트, 2026-09-11) · alembic.ini (2f069ae1…)
  app/ __init__.py · db.py(엔진 pool_size=5·max_overflow=5·pool_timeout=5, CH31_DATABASE_URL) · models.py(Ticket, Mapped) · service.py(list_tickets·main) · __pycache__/(맥 pyc 넷)
  migrations/ env.py(CH31_SYNC_URL·version_table_schema·조건 표현식) · script.py.mako · versions/20260911_01_create_tickets.py · __pycache__/·versions/__pycache__/(맥 pyc 둘)
  notebooks/ 01~05 .ipynb (옛 생성기 없음 — 생성기는 챕터 qa/author_ch31.py)
  .venv/ (macOS arm64 판 217MB, uv 0.11.6, /Users/mhso/... 로 가는 링크)
```

- **코드로 읽는 곳**(`grep -rn`, `.venv` 뺌): `alembic.ini`·`migrations/`는 **03 노트북만**(자식 프로세스 Alembic) · **`app/`은 노트북·검사 어디서도 가져오지 않음** — README 명령 `uv run --project labs/part7/ch31-database python -m app.service`뿐인데, **프로젝트 맨 위에서 실행하면 `ModuleNotFoundError: No module named 'app'`**(이 기기 확인), 실습 폴더 안에서 실행하면 `['환불', '배송', '결제']`(03이 남긴 표를 읽음) · `migrations/env.py`는 `app.models`를 가져오지 않음(`target_metadata` 없음) · 뒤 챕터가 읽는 Ch 31 파일 없음(§6-2).
- **공용 도구와의 관계**: `run_section.sh`는 `uv run --project <실습 폴더> --with … python textbook/_notebook/execute.py`로 **저장소 맨 위에서** 커널을 띄움(03 파일 위치 후보에 `labs/part7/ch31-database`가 있어 찾음) · `PYTHONPATH`에 `notebooks/` 더함(도구 파일을 두면 가져옴) · `--with python-dotenv==1.2.3`은 잠금 1.2.1과 다름(Ch 30과 같은 기록) · **`pre_exec.sh` 훅이 없으면 다섯 절 모두 연결 오류로 멈춤**.
- **옛 생성기와 부르는 곳**: 챕터 `qa/author_ch31.py`(50,995바이트 — `NBS`로 노트북 다섯, `chapter.json`, `_src` 다섯을 **출력 없이 덮어씀**, 맨 위 막는 줄 없음) · `figures/_gen_figures.py`(SVG·excalidraw 다섯 쌍) · **`.moai/…/part7_apply_depth.py`·`part7_review_fixes.py`·`part7_final_repairs.py`** — Ch 30 01이 맨 위 `raise SystemExit`로 이미 막음(Ch 31 노트북·`_src`도 다루는 스크립트 — 막힌 판 그대로라 Ch 31을 덮어쓰지 않음, 셋 중 둘은 `ch31`을 글로 가리킴 5·7곳). **부르는 빌드·검사 스크립트 0**, 단 Part 7 `qa/check_figures.py` 20행이 챕터마다 `figures/_gen_figures.py`가 있는지 `assert`(§6-3).
- **잠금 판**: `sqlalchemy[asyncio] 2.0.43`(`greenlet 3.5.5`) · `asyncpg 0.30.0` · `psycopg[binary,pool] 3.3.3`(`psycopg-pool 3.3.1`) · `alembic 1.16.5`(`mako 1.4.1`) · `pgvector 0.4.1`(+ **`numpy 2.5.3`**) · `langgraph 1.2.11`(`langgraph-checkpoint 4.2.0`·`langgraph-prebuilt 1.1.0`·`langgraph-sdk 0.4.4`) · `langgraph-checkpoint-postgres 3.0.5` · `langchain-core 1.6.2` · `pydantic 2.13.5` · `python-dotenv 1.2.1` · dev `ipykernel 7.3.0`·`nbclient 0.11.0`·**`pip 25.2`**·`ruff 0.12.11`. **Part 7 다른 챕터와 다른 것**: Ch 30은 `pydantic 2.12.5`·`openai 3.13.0`·`langchain 1.4.0`(Ch 31에는 langchain·openai·fastapi 없음) · Ch 23 `psycopg 3.3.3`·`langgraph-checkpoint-postgres 3.0.5`와 같음 · Ch 12 `psycopg 3.3.5`와 다름. **dev `pip==25.2`는 과정 규칙 `pip==26.2`와 다름**(규격 §7-2 `%pip` 줄 — 잠금을 바꾸려면 `uv lock`).
- `%pip` 셀(다섯 절 같은 글, 세 줄): `sqlalchemy[asyncio]==2.0.43 asyncpg==0.30.0 alembic==1.16.5` · `psycopg[binary,pool]==3.3.3 pgvector==0.4.1` · `langgraph==1.2.11 langgraph-checkpoint-postgres==3.0.5` — `numpy`·`python-dotenv` 줄 없음(pgvector가 numpy를 끌어옴).

## 6. 앞뒤 챕터 이음새

### 6-1. 앞 챕터 인계 — 항목별 지금 상태

| 넘긴 챕터 | 자리 | 지금 원고 | 판정 · 할 일 |
|---|---|---|---|
| Ch 30 §18-1·계약 115행 | 전체 | SSE 사건·실행 저장 0 | **참** — Ch 31 원고에 SSE·Ch 30 앱 이어 쓰기 0(`fastapi` 가져오기 0, `agent_service` 0) |
| Ch 30 §18-2 | 05 | `PostgresSaver`를 제 그래프(노드 하나)에 붙임 | **참** — Ch 30 앱과 안 이어짐. Ch 30 10 b8 「Ch 31은 PostgreSQL 데이터베이스에 표를 만들어 쓰는 방법과 체크포인터」·「Ch 31 05절은 체크포인터로 그래프의 실행 상태를 PostgreSQL 표에 저장」이 참이려면 **05에 체크포인터 저장을 남겨야 함** |
| Ch 30 §19 | 01 b2 「요청 함수」·b3 「경로 함수」 | 그대로 | 뜻은 참 · 「처리 함수」로(「경로」는 Ch 30 금지어) |
| Ch 30 §18-7 | 앱 파일 문법 예외 | Ch 31 `app/`·`migrations/` 파일에 클래스·`Mapped` 힌트·조건 표현식 | Ch 31이 따로 정할 것(§10-2) |
| Ch 30 §19 | 05 「검색 문서와 실행 상태를 같은 PostgreSQL에」 | 05 b2 | 참 — 유지 |
| Ch 30 06 b7 | 「보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다」 | Ch 31에 SSE 0 | 참 — SSE 저장을 넣으면 Ch 30 06·10 b8이 틀림 |
| Ch 23 §15 209행 | 02 b3 「Ch23 중단 뒤 재개와 멱등성」 | 그대로 | 참(Ch 23 04~07) |
| Ch 23 §15 210행 | 02 b7 「보상 작업」 | 그대로 | Ch 23이 다루지 않음 — Ch 31 몫(풀어 쓰거나 「이 챕터에서 실행하지 않음」) |
| Ch 23 §15 211행 | 05 b3·새 용어 「체크포인터」 | 새 용어로 셈 | 「Ch 23 01에서 정의한 체크포인터」로 잇고 새 용어에서 뺄지 · Ch 23 금지어 「스키마」·「마이그레이션」은 Ch 31 몫 |
| Ch 23 가르친 것 | 05 | `from_conn_string` | Ch 23 02는 `PostgresSaver(conn)`(연결 직접), 03은 `SqliteSaver.from_conn_string`+`with` — `from_conn_string`은 Ch 23 03 모양으로 설명 가능. 체크포인트 수 「노드 하나 3」은 Ch 23 값과 같음(e6 `checkpoints` 3·`checkpoint_blobs` 1·`checkpoint_writes` 3·`checkpoint_migrations` 10) |
| Ch 21 요약 64행 | 03 | 「마이그레이션」 | Ch 21 04 「옮기기(마이그레이션)」와 **다른 뜻** — 03 첫 자리에서 가를 것 |
| Ch 12 02 | 05 | HNSW·`<=>`·`vector_cosine_ops` | 참 · Ch 12 컨테이너·접속 글과 Ch 31 컨테이너가 다름(§4-1) |
| Ch 4 | 01 b3·03 b3 | 「관계형 표와 기본 SQL」·「CREATE TABLE」 | 참(Ch 4 sqlite3·SQL — `UPDATE`는 과정 요약 §2-1 「처음 쓰면 한 문장」) |
| Ch 2 12 | 01 | `async`·`await`·`gather` | 참 · `create_task`는 Ch 2 전제 금지 목록(「처음 쓰면 한 문장」) |
| Ch 16 05 | 04 | `except TimeoutError` | **이름 겹침** — 04의 `TimeoutError`는 SQLAlchemy 것(§2 04) |

### 6-2. Part 7 묶음·목록·기록·검사

- **목록**: Part 목록 `textbook/part7/public-files.json` Ch 31 **16줄**(44~59행 — README·`alembic.ini`·`app` 넷·`migrations` 셋·노트북 다섯·잠금 둘) · 챕터 `qa/public-files.json` **22줄**(HTML 여섯 + 위 16) · 선행 목록 `prerequisite-files.json`은 Ch 15 한 줄뿐 · `collect_public_files.py`가 챕터 목록 다섯 + `continuity-guide.md`로 Part 목록을 다시 만듦.
- **묶음** `textbook/downloads/part7-practice.zip`(`007f1387…`, Ch 30 마감 판) ← `python3 -B textbook/part7/_build_index.py`(Part 7 30절 `verify_lesson` → `index.html`·zip·`qa/integration-results.json`, **절 수 검사 없음**, Part 시수 「88시간」 손 글).
- **묶음 실행 검사**(`textbook/part7/qa/check_bundle_execution.py`): 27행 `smoke_sections = {"ch30-fastapi-serving": "01", "ch31-database": "03", "ch33-cicd": "02"}` → **Ch 31 03을 풀린 묶음 `notebooks/`에서 실행** · 실행기 32행 **`labs/part7/ch31-database/.venv/bin/python`(이 챕터의 맥 `.venv`)** — 이 기기에서는 링크가 `/Users/mhso/…`로 가서 못 돎(Ch 30 마감이 손으로 대신함) · **03은 DB가 켜져 있어야 통과**(2026-09-11 기록은 맥 Docker) · `bundle-execution.json`(`65daf4ac…`)의 Ch 31 줄 `code_sha256` `b0594f2d…` = 지금 03. → **03에 키·모델을 넣지 말고, DB 접속 글을 바꾸면 이 검사를 돌릴 곳(서버 켜기)도 함께 정해야 함.** 실행기를 이 챕터 `.venv`가 쥐고 있어 실습 폴더 `.venv` 삭제 승인도 이 검사와 묶임.
- **옛 검사 스크립트(고치지 않음 — 결과 파일을 쓰므로 돌리지 않고 읽어서 판정)**: `check_figures.py` — 20행 `_gen_figures.py` 존재 `assert` + SVG·excalidraw 짝 → 마감에서 옛 그림·생성기를 옮기면 Ch 30에서 이미 멈춤(Ch 30 마감 기록) · `check_delivery.py` — b1~b10·복습 3~5·링크 뒤 `existing-artifacts-before.json`(376개, **Ch 31 줄 0**)에서 멈춤(Part 2 Ch 7 파일 없음) · `check_special_secret.py` — Ch 32 Docker 검사 · `final-artifact-hashes.json` — Ch 31 실습 파일 14줄(기록 파일) · `figure-consistency.json`·`delivery-results.json`에 Ch 31 옛 줄.
- `textbook/_notebook/build_index.py` 66행 Ch 31 절 수 **5**(실습 절을 빼고 세는 과정 약속 — 그대로), 설명 「트랜잭션·마이그레이션·연결 풀과 벡터 검색 데이터의 저장을 확인합니다.」 · `build_bundle.py` 28행 Part 7 목록 · `check_course_continuity.py`는 Part 7을 보지 않음.

### 6-3. 뒤 챕터(대기·제외)가 Ch 31에 기대는 것 — 고치지 않음

| 파일 | 내용 | 계약 여부 |
|---|---|---|
| Ch 32 04 `_src` b3 | 「Ch31에서는 PostgreSQL, 트랜잭션, 인덱스와 pgvector를 배웁니다. 이 챕터는 Ch31 파일을 복사하지 않고 `init.sql`에 필요한 최소 스키마를 독립적으로 제공합니다.」 | 글만 — **인덱스(HNSW)·트랜잭션·pgvector를 남겨야 참** |
| Ch 32 `compose.yaml`·`init.sql` | 제 `pgvector/pgvector:0.8.6-pg17-bookworm` | **Ch 31 파일을 읽지 않음** |
| Ch 33 `.github/workflows/ci.yml` | 제 폴더만 | Ch 31 없음 |
| Ch 34 | `_src`에 Ch 31 문장 0 | 없음 |
| `labs/part7/continuity-guide.md` 8·9·10행 | 「Ch30…와 Ch31의 데이터·체크포인트 저장」·「Ch4의 SQL, Ch12의 pgvector → Ch31의 트랜잭션·연결 풀·인덱스 → Ch32의 데이터베이스 컨테이너」·「Ch30·31의 서비스와 데이터베이스」 | 글만(Ch 31 마감 때 대조, 9행에 마이그레이션·백업이 없음) |
| Part 7 `_src/index.html`·`index.html` 61·70행 | 「Ch31의 데이터 저장」 · 절 다섯 슬러그 링크 | 글·링크(슬러그) |
| `textbook/index.html` 55행 | `ch31-database/index.html` 링크 | 링크 |

### 6-4. 완료 챕터가 Ch 31에 기대는 문장 — 개선 뒤에도 참이어야 함

| 파일 | 문장·링크 | Ch 31 쪽 조건 |
|---|---|---|
| **Ch 30 10** `_src`·HTML·노트북 [44]·`author_10.py` 569~572·606·673행 | b8 「Ch 31 ↗(01 슬러그 링크)은 PostgreSQL 데이터베이스에 표를 만들어 쓰는 방법과 체크포인터를 다룹니다. Ch 31 05절은 체크포인터로 그래프의 실행 상태를 PostgreSQL 표에 저장합니다. 이 챕터의 실습 앱에 붙이는 일은 다루지 않습니다. 보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다.」 | **01 슬러그 고정 · 05 체크포인터 저장 · Ch 30 앱·SSE 저장 안 다룸** |
| Ch 30 `author_09.py` 688행 | 링크 상수 `L_CH31_01`(HTML 09에는 링크 없음 — 상수만) | 01 슬러그 |
| Ch 30 06 `_src` b7 | 「보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다」 | SSE 저장 안 다룸 |
| Ch 21 요약 64행(완료 기록) | 「Ch 23 02·Ch 31 03의 DB 「마이그레이션」과 다른 뜻」 | 03이 DB 「마이그레이션」을 다룸 |
| Ch 1 01(과정 지도) | 「Part 7 서비스화와 배포 · Ch 30~34」 | 참 |

- 완료 챕터 HTML에서 Ch 31을 링크하는 곳은 Ch 30 10 하나뿐(`grep -rno 'ch31-database/'`). Part 1~6에 「Ch 31」 문장 0(Ch 12·23의 PostgreSQL 문장은 Ch 31을 가리키지 않음).

## 7. 설치판 동작 — 모델 없는 확인 (2026-09-29, 가상환경 = 잠금 판 + pip 26.2, 서버 = pgenv 17.11 · pgvector 0.8.1)

### 7-1. 판과 이름 (`e1_versions.py`)
- 위 잠금 판 그대로 설치됨. `create_async_engine`의 기본 풀은 **`AsyncAdaptedQueuePool`**, 새 엔진 `pool.status()` = `Pool size: 5  Connections in pool: 0 Current Overflow: -5 Current Checked out connections: 0`.
- **`sqlalchemy.exc.TimeoutError`는 내장 `TimeoutError`의 하위 클래스가 아님**(`issubclass` = `False`).
- `PostgresSaver`·`AsyncPostgresSaver`(`langgraph.checkpoint.postgres.aio`)·`pgvector.sqlalchemy`·`pgvector.psycopg`·`alembic.command` 가져오기 됨. `python -m alembic` 됨(가상환경 `bin`이 `PATH`에 없어도).

### 7-2. 결정적으로 보일 수 있는 값 (두 번 이상 같음)
- 01: 세 줄 `['환불', '배송', '결제']` · 순차·동시 결과 같음 `True` · 동시 < 순차 `True`(3/3) · `dispose()` 뒤 `Connections in pool: 0`.
- 02: §3 표(`23514`·`accounts_balance_check`·1600 ↔ 1000) · 정상 이체 100 → `[(1, 400), (2, 600)]`.
- 03: `Running upgrade  -> 20260911_01, …` · 버전 `('20260911_01',)` · 표 `['alembic_version', 'tickets']` · downgrade 뒤 `to_regclass` `None`·버전 줄 0 · §3 후보 셋의 종료 코드·오류 첫 줄·버전·줄 수 · `alembic history` 두 줄.
- 04: `TimeoutError` 글 `QueuePool limit of size 1 overflow 0 reached, connection timed out, timeout 0.20 (Background on this error at: https://sqlalche.me/e/20/3o7r)` · 끝난 뒤 `pool.status()` 글 · 반납 누락 `Checked out connections: 1` → 닫은 뒤 0.
- 05: 가까운 문서 `배송`(거리 `0.0061`)·`환불`(`0.8896`) · **`EXPLAIN (COSTS OFF)`(ANALYZE 없이)** = `Limit / Sort / Seq Scan on documents` 네 줄(시간 줄 없음 → 결정적) · `SET enable_seqscan = off` 뒤 `Index Scan using documents_embedding_hnsw` · `setup()` 뒤 표 넷 + `documents` · `{'value': 12}`·기록 길이 3 · 체크포인트 표 줄 수 `(3, 1, 3, 10)` · 덤프에 `CREATE TABLE ch31_shared.documents`·`USING hnsw` 있음, `CREATE EXTENSION` 없음 · 확장 없이 복원 → 종료 3 `type "public.vector" does not exist` · 확장 뒤 복원 → `(3, 3, True)` · 복원 DB `get_state` → `{'value': 12}` · `pg_restore -l`의 TABLE 항목 5.
- 흔들리는 값: 걸린 초(01·04) · `EXPLAIN ANALYZE`의 시간·버퍼 줄 · 덤프 줄 수(이 판 232)·아카이브 바이트(이 판 8,494) — 판·기기마다 달라짐.

### 7-3. 노트북 셀 맨 위 `await`와 비동기 드라이버
- 옛 노트북이 2026-09-11 새 커널에서 셀 맨 위 `await`·`async with`로 asyncpg 엔진을 셀 여러 곳에서 쓰고 PASS(ipykernel이 셀 사이 같은 이벤트 루프를 씀 — Ch 28·30 선례와 같은 모양). 이번에는 노트북을 실행하지 않았고, 같은 코드를 `asyncio.run` 스크립트로 확인함.
- **Windows 주의(문서 근거, 실행 안 함)**: psycopg 비동기(`AsyncPostgresSaver`·`psycopg.AsyncConnection`)는 「On Windows, Psycopg is not compatible with the default ProactorEventLoop」(psycopg 문서). asyncpg(01~04)·동기 `PostgresSaver`(05 지금 판)는 해당 없음 → 05를 비동기 체크포인터로 바꾸면 Windows 학생이 막힐 수 있음.

## 8. §2-7 판단 근거 — 도구 파일·앱 파일

### 사실
- 절 사이에 되풀이되는 것: **주소 셀**(다섯 절 같은 셀 — `ASYNC_URL`·`SYNC_URL`·`NATIVE_URL`) · 이름 공간 지우고 다시 만들기(01·02·03·05 — 절마다 SQL이 다름) · 잔액 읽기(02 안에서 둘) · `to_regclass` 표 있는지(03 안에서 셋) · Alembic 부르기(03만) · 줄 수 세기(05 안에서). **절을 건너 되풀이되는 함수는 거의 없음** — 규격 §2-7 3번 「도구 파일을 더해도 챕터 전체 코드가 줄지 않으면 만들지 않음」(Ch 2·4·6·22 선례)에 걸릴 수 있음.
- 앞 챕터 도구 파일(Ch 30 `serve_tools.py`·Ch 23 `checkpoint_tools.py`·Ch 24 `approval_tools.py`·Ch 12 `rag_tools.py`)에 이 챕터가 쓸 함수 없음(worker·SQLite·SSE·검색 순위). 잠금도 다름.
- 도구 파일 이름 후보(과정의 `*_tools.py` 스물여섯과 안 겹침): **`db_tools.py`** · `store_tools.py` · `database_tools.py` (**`data_tools.py`는 Ch 4에 있음**).
- `app/`은 노트북이 쓰지 않는 따로 예제(README 명령뿐) — 도구 파일과 별개. `app/db.py` 풀 설정(5·5·5)은 04와 이을 수 있는 값.

### 선택지 (결정하지 않음 — 장단점만)
- **S1 도구 파일 없음**: 절마다 필요한 함수를 그 자리에서 가르침. 장점 — 절이 짧고 서로 독립, 해시 사슬·공개 목록 줄 0. 단점 — 주소 셀 다섯 번·06 실습 절에서 01~05 함수를 다시 적어야 함(실습 절 「새 문법·API 0」은 지켜짐).
- **S2 `db_tools.py`**(예: 주소 만들기·이름 공간 다시 만들기·표 있는지·줄 수·Alembic 부르기): 장점 — 06 실습 절이 짧아짐, 03 함수가 04·05·06에 이어짐. 단점 — 비동기 함수(`async def`)를 도구 파일에 둘지(Ch 30 `zero_timeout` 강사 확인 선례), 생성기 대조 사슬·공개 목록 두 곳·zip 해시가 늘어남, 파일을 가져오는 절의 설치 셀에 도구 파일 패키지.
- **S3 `app/`을 노트북에서 가져오기**(Ch 30 앱 방식): 장점 — 「서비스 코드가 쓰는 엔진·세션」을 그대로 보임, 04의 풀 설정과 이음. 단점 — `app/` 파일의 클래스·`Mapped` 힌트·`from __future__`·반환 힌트를 문법 예외로 정해야 함(§10-2), 파일 위치 셀 세 자리, 묶음 실행 검사 03의 조건이 늘어남.

## 9. 모델·비용 선택지와 흔들림 처리 (결정하지 않음 — 장단점만)

### 9-1. 모델 없이 결정적으로 보일 수 있는 것 (확인함)
- 다섯 절의 학습 질문 전부(§7-2) — 엔진·세션·트랜잭션·롤백·Alembic 판 번호·풀 상태·`setup()` 표 이름·체크포인트 줄 수·복원 뒤 줄 수. 05의 벡터는 손으로 적은 3차원 값.

### 9-2. 선택지
- **M0 모델 0(지금)**: 요청 0·비용 0, 키 셀 없음(Ch 23·24 선례), 모든 값 결정적 → 새 커널 두 번 비교가 쉬움, 06 실습 절 요청 0(Ch 23·24·30 선례 — 규격 §7-2 「3~5번」과 달라 강사 확인). 단점 — 「에이전트 서비스의 상태」가 코드가 만든 값뿐.
- **M1 05 문서를 실제 임베딩으로**(`OpenAIEmbeddings(dimensions=…)`, Ch 12·14 이음): 요청 2번 안팎(문서 한 번·질문 한 번, 1원 아래) · 단점 — 잠금에 langchain-openai·키 셀이 들어감(Part 7 묶음 실행 검사는 03만이라 직접 영향은 없음), 거리 넷째 자리가 흔들림(과정 요약 §6 「검색 점수 넷째 자리」).
- **M2 05 그래프에 실제 모델 노드**: 체크포인터에 대화 메시지가 쌓이는 장면 · 단점 — 요청 수·답 글 흔들림, Ch 23이 일부러 모델 0으로 가르친 체크포인터와 이음이 약해짐, 흔들림 확인(노트북 밖 5번 — 규격 §2-7 10번 끝)·`NN-probe.md` 필요.
- **흔들림 처리**: M0이면 흔들리는 값은 걸린 초(01·04)와 `EXPLAIN ANALYZE` 시간 줄뿐 → 01은 Ch 25 03 선례(결론·그림·정리에는 「동시 < 순차」 부등식만, 초는 둘째 단락·표·b7), 05는 `COSTS OFF`에 `ANALYZE`를 빼면 계획 글이 매번 같음(시간 줄을 보이려면 둘째 단락에 「이번 실행에서는」).
- **묶음 실행 검사 후보**: 다섯 절 모두 DB가 필요 → 키가 없어도 DB 없이는 못 돎. 지금 계약 03은 그대로 두고(스크립트 수정 금지), DB를 켠 상태에서 손으로 대조(Ch 30 마감 방식)할 절을 정하면 됨.

## 10. 과정 규칙과 부딪히는 것 (선택지와 장단점만)

### 10-1. DB 준비 방식
- **D1 학생 = Docker, 작업 기기 = pgenv + `pre_exec.sh`**(Ch 12·23 선례): 장점 — 실제 PostgreSQL·pgvector·`pg_dump`, 규격 §3 「가짜 금지」와 맞음, 과정 선례 그대로. 선택 — (a) Ch 23처럼 **Ch 12 컨테이너 재사용**(`student@127.0.0.1:55432/rag_lab`, 이름 공간 `ch31_*`) — 컨테이너 하나로 과정이 이어짐, 단 `pgvector 0.8.2`·계정 이름이 옛 원고와 다름, 복원용 DB(`ch31_restore`)를 만들 권한 확인 필요(`student`는 컨테이너 초기 계정이라 슈퍼유저) · (b) **챕터 전용 컨테이너 유지**(`kdt-ch31-postgres`, 55431) — 옛 원고와 가까움, 단 `127.0.0.1` 묶기·계정 글 정리 필요. 단점(공통) — Docker Desktop이 없는 학생은 막힘, 05 `docker exec`는 Docker에서만.
- **D2 `pgembed`(pip로 PostgreSQL)**: 장점 — Docker 없이 `uv sync`만으로 세 OS(조건부), pgvector 0.8.2·`pg_dump` 포함, 서버가 커널과 함께 꺼짐. 단점 — 인텔 맥·macOS 14 이하 휠 없음, POSIX 소켓 ↔ Windows TCP로 연결 글 모양이 갈림, 이 기기에서 딸려 온 `psql` 세그폴트, AGPL 확장(`pg_search`) 동봉, 0.x 판(문서·코드 어긋남), 휠 68~83MB·설치 130MB+, 풀·포트·`localhost`를 설명하는 04와 모양이 다름(소켓).
- **D3 SQLite로 대신**: 장점 — 설치 0. 단점 — asyncpg·풀 고갈·Alembic 트랜잭션 DDL·pgvector·`PostgresSaver`·`pg_dump`를 보일 수 없음(챕터 주제가 PostgreSQL), 연결 폴더 SQLite 멈춤(Ch 23), 규격 §3 「실제 조건」과 멀어짐. → 권하기 어려움.
- **D4 conda-forge 안내**: 장점 — 작업 기기와 같은 판. 단점 — 학생에게 conda/mamba가 새로 필요, 크기.

### 10-2. 클래스·`Mapped` 힌트·데코레이터 (Ch 30 앱 파일 예외와 이어)
- 지금 **노트북에는 ORM 클래스 0**(모두 `text()` SQL) — `Mapped[...]`는 `app/models.py`에만. 선택: (a) 노트북은 `text()`만, 앱 파일은 Ch 30 §6처럼 「가르치는 대상 파일의 예외」(`DeclarativeBase` 상속·`Mapped[...]` 칸만 적은 클래스 — L5 스키마 클래스와 같은 성격, 힌트가 칸 형식을 정함)로 둠 · (b) 노트북에서 ORM 모델을 가르침(01 또는 03 — `Mapped`가 Alembic 자동 생성과 이어짐) — 클래스·힌트 예외를 노트북까지 넓혀야 함 · (c) 앱 파일도 과정 문법으로 고침(Ch 28 A-17) — 조건 표현식(`env.py` 35행)·반환 힌트·`from __future__`는 고칠 수 있으나 `Mapped` 힌트는 빼면 모델이 안 됨.
- 데코레이터: 챕터 코드에 0(앱 파일 포함).

### 10-3. 비동기 문법
- Ch 28·30 허용 = 셀 맨 위 `async with`·`await`, `async def` 셀당 하나, `ainvoke`·`async for`·비동기 생성기. **Ch 31이 새로 쓰는 것**: `async_sessionmaker`로 만든 세션을 `async with Session() as session`(셀 안 함수 속) · `async with engine.begin()`(블록이 끝나면 확정·오류면 되돌림 — 트랜잭션의 핵심 모양) · `asyncio.create_task`(04 — 과정 첫 사용이면 한 문장) · `asyncio.gather(*…)`(Ch 18 03 선례) · `await engine.dispose()`. 03·05는 동기(psycopg·Alembic 자식 프로세스·`PostgresSaver`) — 비동기가 학습 목표인 01·02·04와 섞임(L7 「비동기가 학습 목표일 때만」).

### 10-4. SQL 글·파일 쓰기·말·제목
- **SQL 글**: `text("…")`·`conn.execute("…")` 안 SQL은 G2가 코드 줄로 셈(여러 줄 문자열이면 줄마다) · Ch 4·12·23이 문자열 SQL을 이미 씀. SQL 낱말 `CREATE SCHEMA`·`CHECK`·`UPDATE`·`EXPLAIN`·`CREATE EXTENSION`·`to_regclass`는 처음 쓰는 자리에서 한 문장씩(과정 요약 §2-1 「SQL `UPDATE` 처음 쓰면 한 문장」).
- **파일 쓰기**: 지금은 0. 03을 실제 조건(§3)으로 바꾸면 **새 리비전 파일**이 필요 → 실습 폴더 `migrations/versions/`에 두면 묶음·03 계약(`b0594f2d…`)·학생 폴더 리비전 사슬이 바뀜 / **임시 폴더에 `migrations` 복사본을 만들어 거기서**(Ch 23 「파일은 임시 폴더에만」 선례) · 05 덤프를 파일(`-Fc`)로 쓰면 임시 폴더.
- **말**: 챕터 주제 말(트랜잭션·커밋·롤백·마이그레이션·세션·풀·스키마)을 새 용어로 풀지, 한국어 대체어(예: 「한 묶음 처리」·「확정」·「되돌리기」·「표 구조 판」·「연결 풀」)를 쓸지 · Ch 23 「이름 공간」(SQL `SCHEMA`)·「표 만들기」(`setup()`) 이어 쓰기 · Ch 21 「옮기기」와 가르기 · 「쿼리」(Ch 14 금지 → 「조회」)·「반환」(→ 내놓다·풀에 돌려놓기 — 「돌려」는 게이트 금지어 조각이 걸리지 않게)·「레코드」(→ 줄)·「필드」(→ 칸)·「검증」(→ 검사)·「측정」(→ 재기).
- **제목**: 「DB & 상태 영속화」(`&`·두 이름)·「SQLAlchemy」·「PostgreSQL」·「Alembic」·「pgvector」·「커넥션 풀」 — Ch 23·30처럼 「제목에만 남음(강사 확인)」 + 본문 첫 자리 풀이. 슬러그는 01이 링크로 고정, 02~05는 Part 7 목차만 링크(목차는 `_build_index.py`가 다시 만듦).

## 11. 삽화 비유 계열 후보 (앞 챕터와 겹치지 않게)

앞 챕터가 쓴 계열: Ch 3 창고 선반 · Ch 4 쟁반·카드 상자·서류철 · Ch 5 나무 쟁반·블록 · Ch 6 도서관 상담 창구·소포 · Ch 7·8 책상 색 약속 · Ch 10 도막·공책과 장부 · Ch 11 쪽지·쟁반 · Ch 12 관·깔때기·구슬 · Ch 15 저울·사과·바구니 · Ch 16 쪽지·도장 대장·개찰구 · Ch 17 눈 위 발자국 · Ch 18 도예 · Ch 19 식당 주문 전표 · Ch 20 자료실 승강 상자 · Ch 21 세탁기 · Ch 23 체스판과 즉석사진 · Ch 24 도미노 · Ch 25 대나무 홈통 · Ch 26 항구 예인선 · Ch 27 온실과 모종판 · Ch 28 우주 정거장 도킹 포트 · Ch 29 오르골 종이띠 · Ch 30 화물 열차와 번호판 차량 · Ch 1 사물함 · Ch 2 동전 저울. **옛 Ch 31 비유**(식당·은행 창구·건물 도면·도서관 태블릿·창고)는 Ch 19·Ch 6·Ch 3과 겹침.

1. **「옛 전화 교환대」** — 구멍 수가 정해진 교환판(연결 풀, 04 — 모든 구멍에 선이 꽂힘 = 고갈, 뽑지 않은 선 = 반납 누락) · 두 선을 함께 꽂아야 통화가 이어짐(02 — 한 선만 꽂힌 판 = Before) · 교환원이 선 여러 개를 번갈아 잇기(01 대기 겹침) · 번호를 차례로 적은 교환 일지(03) · 일지와 선 배치를 함께 옮겨 적기(05). 겹침 없음(과정 삽화에 교환대·전화 0). 사람 손 없이 그리기 어려움(선만 보이게).
2. **「자판기와 동전」** — 동전을 넣었는데 음료가 안 나오면 동전이 전부 돌아옴(02 원자성) · 투입구 하나 앞 줄(04) · 칸마다 번호를 붙인 보충 기록표(03) · 음료 칸과 동전 통이 한 기계(05 공존). 겹침 없음. 01(비동기)은 그리기 약함. 「돌아옴」 말이 게이트 금지어 조각과 가까움(그림 읽기 말 조심).
3. **「대관람차와 번호 곤돌라」** — 곤돌라 수가 정해짐(풀) · 내리지 않은 손님(반납 누락) · 줄 선 손님이 기다리다 떠남(대기 제한) · 여러 곤돌라가 함께 돎(01) · 두 사람이 한 곤돌라에 함께 타거나 함께 못 탐(02). 03·05는 약함. 탈것이라 Ch 30 열차·차량과 결이 가까움.
4. **「번호를 새긴 사다리와 찬합 도시락」**(두 물건) — 가로대 번호 = 리비전, 한 칸씩 오르내리기 = upgrade/downgrade, 부러진 가로대 앞에서 제자리(03 실패 뒤 판 그대로) · 한 찬합의 층이 다른 반찬(05 공존)·찬합째 옮겨 담기(백업). 02·04는 다른 물건이 필요 → 한 가족으로 묶기 어려움.

## 12. 위험과 깨진 것

1. **DB 서버 없이는 다섯 절 모두 멈춤** — `run_section.sh`에 `pre_exec.sh` 훅이 꼭 필요(다섯 절 모두), 서버는 호출이 끝나면 꺼지므로 실행과 `--no-exec`(빌드만)도 그 호출 안에서 켜야 하는지 확인(`--no-exec`는 노트북을 안 돌리므로 서버 불필요 — Ch 23은 `--no-exec`에도 훅이 켬).
2. **프로세스·포트·데이터 폴더**: 기기 셸이 끝나면 postgres도 끝나지만, 한 호출 안에서 멈춘 채 남지 않게 `trap EXIT` 필수 · 55432는 Ch 12 서버 자리(겹치면 Ch 23처럼 멈춤) · 데이터 폴더는 `/tmp`(클러스터 하나 약 40MB) · pgembed는 커널이 살아 있는 동안 서버가 남음.
3. **05의 Docker 명령**은 이 기기·Docker 없는 학생에서 못 돎 — `pg_dump`를 어디서 부를지(컨테이너 안 ↔ 로컬 바이너리 ↔ pgembed 경로)를 절 첫머리에서 정해야 함. 로컬 `pg_dump`는 서버 판 이상이어야 함.
4. **03 Alembic `PATH`**: `["alembic", …]`는 가상환경 `bin`이 `PATH`에 없으면 `FileNotFoundError`(학생 VS Code 커널). `sys.executable -m alembic`이 안전. Alembic 자식 프로세스의 pyc가 실습 폴더에 쌓임(`PYTHONDONTWRITEBYTECODE` 넘기기).
5. **03이 묶음 실행 검사 계약** — 03 코드를 바꾸면 zip → (DB를 켠 곳에서) 검사 → 새 `code_sha256`. 실행기가 이 챕터 맥 `.venv`를 가리켜 이 기기에서 스크립트 그대로는 못 돎(Ch 30 마감과 같은 처지).
6. **04 이름 가림**: `sqlalchemy.exc.TimeoutError` ≠ 내장 `TimeoutError` — Ch 16 05와 부딪힘.
7. **01 시간 `assert`** — 이 기기 3/3 참이나 느린 학생 기기·원격 DB에서 흔들릴 수 있음(규격 §3 「`assert`는 매번 같아야 하는 값에만」).
8. **README 틀린 곳**: `.env` 읽기(노트북이 안 읽음) · 프로젝트 맨 위에서 `python -m app.service` 실패 · `uv sync --project`(`--locked` 아님) · `docker run -p 55431:5432`(모든 주소에 묶임).
9. **dev `pip==25.2`**(과정 `26.2`) — `%pip` 셀을 건드리면 `uv lock` 필요, 연결 폴더라 `uv sync`가 막힐 수 있음(`UV_NO_SYNC=1`).
10. **옛 생성기 `qa/author_ch31.py`가 막혀 있지 않음** — 실행하면 노트북 다섯(출력 없이)·`chapter.json`·`_src`를 덮어씀. 01 작업 첫머리에서 `raise SystemExit`.
11. **모델 의존·비용**: 지금 0. 넣으면 키 셀·흔들림 확인·잠금 변경이 따라옴(§9).
12. **학생 환경**: Docker Desktop(Windows는 WSL2)·포트 충돌(55431/55432)·Windows psycopg 비동기 루프·pgembed 휠 조건(§4-2).
13. **기기 디스크**: 루트 여유 1.5G → 1.4G(이번 준비 `/tmp/ch31-prep` 109MB — 서버 데이터 폴더 둘 77MB 포함) · `/sessions` 831M 그대로 · 가상환경·pgembed 시험 환경은 사용자 디스크(여유 약 70G). 절 작업마다 `/tmp`에 클러스터를 새로 만들면 약 40MB씩.
14. **뒤 챕터 계약**: 없음(Ch 32·33·34가 Ch 31 파일을 읽지 않음). 글 계약은 Ch 30 10 b8·Ch 32 04 b3·continuity-guide(§6-3·6-4).

## 13. 01절 작업자가 먼저 결정해야 할 것

1. **DB 준비 경로와 접속 글(§4·§10-1)** — 학생 경로(Ch 12 컨테이너 재사용 ↔ 챕터 전용 컨테이너 ↔ pgembed), 작업 기기 `pre_exec.sh`(pgenv, 다섯 절 모두, `/tmp` 데이터 폴더, 포트·계정을 학생 글과 같게), 환경 변수 이름(`CH31_DATABASE_URL`·`CH31_SYNC_URL`)과 `.env`를 읽을지, 05 `pg_dump`·`psql`을 어디서 부를지. 교재 본문 판 표기(학생 이미지 판 ↔ 교재 출력 17.11·0.8.1)를 Ch 12·23처럼 가름.
2. **paired 02·03·04 Before를 실제 조건으로 바꿀지(§3)** — 02 CHECK 위반(1600 ↔ 1000) · 03 NOT NULL 칸 추가 실패 / downgrade 데이터 사라짐 / downgrade 없음 중 하나 + 리비전 파일을 임시 폴더 복사본에 둘지 · 04 지금 장면 유지 ↔ 반납 누락. 03은 묶음 실행 검사 계약.
3. **문법 예외 범위(§10-2·10-3)** — `async with engine.begin()`·세션·`create_task`·`gather(*…)` 허용 범위, 노트북에서 ORM(`Mapped`)을 가르칠지, 앱 파일(`app/`·`migrations/env.py`)을 과정 문법으로 고칠지(Ch 28 A-17)·Ch 30 §6 예외로 둘지, 반환 힌트, 04 `TimeoutError` 이름 가르기.
4. **말과 제목(§1 금지어·§10-4)** — 트랜잭션·커밋·롤백·마이그레이션·세션·풀·스키마를 새 용어로 풀지·대체어로 쓸지, Ch 23 「이름 공간」·「표 만들기」와 Ch 21 「옮기기」 가르기, 「커넥션 풀」 ↔ 「연결 풀」, 제목 영어를 「제목에만 남음」으로 둘지.
5. **모델 결정과 도구 파일(§8·§9)** — M0(요청 0 유지) ↔ M1·M2, 01 시간은 부등식만 결론에, `db_tools.py`를 둘지(S1~S3), 05 체크포인터 저장은 Ch 30 10 b8 때문에 남김, 01 슬러그 고정.

## 14. 챕터 마감으로 미룰 것

- **06 실습 절 신설**(규격 §7-2): 슬러그 후보 **`06-DB-실습`**(가장 짧음 — 선례 `09-Middleware-실습`·`04-Streaming-실습`·`06-MCP-실습`처럼 챕터 짧은 이름 + 「실습」) · `06-상태-영속화-실습` · `06-DB와-상태-영속화-실습`(`_notebook/build_index.py` 제목 「DB와 상태 영속화」, Ch 30 `10-FastAPI-서빙-실습` 모양). 슬러그에 `&`는 못 씀. 제목 「DB와 상태 영속화 실습: …」 · `format: experiment` · meta 「실습 30분 · 새 용어 0」(**챕터 시수 5·11h에 더하지 않음**) · 새 문법·API 0 · 요청은 모델 결정에 따라(M0이면 0 — Ch 23·24·30 선례, 강사 확인). 주제 예: 도서관 상담 기록을 저장하는 한 흐름 — 02 한 묶음 저장(기록 줄 + 대출 횟수 차감) · 04 풀에서 빌리고 돌려놓기 · 05 체크포인트 저장·복원 확인 → 실행 2는 값 하나만(예: 보낼 금액이 CHECK를 넘게·`pool_timeout`·복원 DB에 확장 만들기 여부).
- **Part 7에서 다른 점**: `_build_index.py`에 절 수 검사 없음(자동 「31절」) · Part 시수 손 글 「88시간」 그대로 · `textbook/_notebook/build_index.py` 66행 절 수 5 그대로(과정 약속) · 챕터 설명 한 줄(`_build_index.py` 20행·`build_index.py` 67행)을 개선 본문과 대조 · Part 7 `check_bundle_execution.py`는 03 실행(스크립트 수정 금지 — DB를 켠 곳에서 손 대조, 실습 절을 넣으려면 수정 필요 → 후보로 기록) · `check_figures.py`는 옛 그림 짝·`_gen_figures.py`를 요구(옮기면 멈춤 — Ch 30에서 이미 멈춤).
- 옛 생성기 막기(01 첫머리 `raise SystemExit`) → 마감 때 `qa/upgrade/before/generators/blocked/`로 `mv -n`: `qa/author_ch31.py`(50,995바이트) · `figures/_gen_figures.py` · `.moai` part7 스크립트 셋은 Ch 30 01이 막은 판 그대로(처분은 사용자·강사).
- 옛 그림 15개(`figures/0N-흐름.{svg,excalidraw,caption.md}`) 삭제 승인 목록(사본 `before/figures/`, 공개 목록에 줄 없음) — `check_figures.py`와 함께.
- `chapter.json` `objectives`(「작업 경계를 설계」·「실제 환경에서 재현하고 대응」·「논리 백업 범위」)·제목(`&`)·챕터 `index.html` 대조 → `_build.py`·`_build_index.py`.
- 실습 폴더 README 다시 쓰기(DB 준비·`uv sync --locked`·`notebooks/`에서 열기·절마다 DB 이름 공간·요청 수 0·05 백업 명령·`app/` 실행 자리·끄는 명령) · `labs/part7/continuity-guide.md` 8~10행 · `qa/research.md`·`verification.md`·`집필점검표.md`에 「개선 전 판」 표시.
- 공개 목록 두 곳(06 노트북·도구 파일·바뀐 실습 파일) → `part7-practice.zip` 다시 만들기(마지막에 한 번) → 묶음을 풀어 03·06 준비 셀 확인(DB 켠 채).
- **뒤 챕터 인계**(고치지 않음): Ch 32 04 b3(인덱스·트랜잭션·pgvector가 남았는지) · continuity-guide · 과정 요약에 Ch 31 줄(DB 준비 방식·비동기 세션 허용·용어).
- 삭제 승인 대상: 실습 폴더 `.venv`(맥 217MB — 묶음 실행 검사 실행기와 묶임) · `app/__pycache__`·`migrations/**/__pycache__`(맥 pyc 여섯) · `.cache/vm/venv-ch31-database`(349MB) · **`.cache/vm/pgembed-try`(204MB — 이번 시험 환경)** · 기기 `/tmp/ch31-prep`(109MB — 클러스터 둘·Alembic 복사본·시험 스크립트) · `qa/upgrade/gates-wip-*.json`(생기면).

## 15. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 5 · `html` 5(빌드한 절 HTML) · `notebooks` 5 · `figures` 16(SVG·excalidraw·caption 각 5 + `_gen_figures.py`) · `generators` 6(`author_ch31.py`·`_gen_figures.py` + `moai/` part7 스크립트 셋·`part7-author.md`) · `qa` 3(`public-files.json`·`research.md`·`verification.md`) · `lab` 11(README·`pyproject.toml`·`uv.lock`·`alembic.ini`·`app` 넷·`migrations` 셋 — pyc·`.venv` 뺌) · `chapter.json`·`_build.py`·`index.html`·`집필점검표.md` = **55개, 714,599바이트**. 원본과 sha256 모두 같음 |
| `qa/upgrade/gates-before.json` | §0 표(절별 G1~G7 · 합계 175, 통과 0/5, 문장 434), `63372b07031c82f5b23e950e35449bd7f33d07e981ccc6d1a2c8aa82b5654b5a` |
| `qa/upgrade/before-manifest.json` | sha256 **209개**(`b9bd5a88…`) — ① 이 챕터 원고·실습 폴더 57(`qa/upgrade` 뺀 챕터 파일 전부·실습 폴더 파일 전부(`.venv`·pyc 뺌)·`.venv/pyvenv.cfg`·노트북 계약 JSON·화면 검사 결과) ② 앞 챕터 DB 선례·도구 27(Ch 12 README·02 `_src`·HTML·`pre_exec.sh`·잠금 / Ch 23 README·잠금·`checkpoint_tools.py`·01~03 노트북·01·02 `_src`·02 HTML·`pre_exec.sh` / Ch 30 `serve_tools.py`·잠금 / Ch 24 `approval_tools.py` / **pgenv 바이너리 여섯·`vector.control`**) ③ 챕터 요약 29 ④ Part 7 목록·목차·소개·`practice-start.md`·`qa/` 전부·continuity-guide 둘·`build_index.py`·`build_bundle.py`·`textbook/index.html`·zip 셋 48 ⑤ 뒤 챕터 10(Ch 32 04 `_src`·HTML·`compose.yaml`·`init.sql`·README, Ch 33 CI, Ch 30·32~34 `chapter.json`) ⑥ Ch 31을 가리키는 완료 챕터 10(Ch 30 10·06 `_src`·HTML·노트북·`author_06/09/10.py`, Ch 21 04 `_src`) ⑦ 옛 생성기(`.moai` part7 셋·`part7-author.md`·`review-part7.md` — 챕터 생성기 둘은 ①에) ⑧ 과정 문서·공용 도구 23 |
| `qa/upgrade/chapter-lead-notes.md` | 이 파일 |
| `$ROOT/.cache/vm/venv-ch31-database` | Python 3.12.13 · 349MB |
| (시험) `$ROOT/.cache/vm/pgembed-try` | pgembed 0.2.0 시험 가상환경 · 204MB — 챕터 작업에는 쓰지 않음 |

### 가상환경 만든 방법과 결과
- Ch 30 준비와 같은 방법: `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy uv venv --python 3.12.13 …/venv-ch31-database` → `uv pip install --python …/bin/python pip==26.2` → `uv export --project labs/part7/ch31-database --frozen --no-hashes --all-groups --no-emit-project`에서 주석·들여 쓴 줄을 뺀 94줄, **`pip==25.2`만 `pip==26.2`로 바꿈**(`/tmp/ch31-prep/req-clean.txt`) → `bin/python -m pip install --no-cache-dir -q -r`(한 호출, 170초 안). 설치 오류 0, `uv cache prune` 안 함.
- 크기 어림(만들기 전): Ch 30 254MB 안팎·사용자 디스크(여유 70G)라 기기 루트(1.5G)·`/sessions`(831M)는 그대로일 것 → 만듦. **전후 루트 1.5G → 1.4G(`/tmp` 시험 파일 몫) · `/sessions` 831M 그대로.**
- 결과: `pip freeze --all`과 잠금 대조 **판 차이 0**(설치 88 = 잠금 94 − 이 기기에 해당하지 않는 여섯: `appnope`(darwin)·`colorama`·`tzdata`(win32)·`cffi`·`pycparser`(pypy)·`httpx2-jsfetch`(emscripten)). `pip check` 이상 없음. 커널 스펙 `share/jupyter/kernels/python3` 있음. `run_section.sh`는 `$ROOT/.cache/vm/venv-ch31-database`를 자동으로 씀(`UV_NO_SYNC=1`).
- import 확인(`env -u OPENAI_API_KEY`): §7-1.

### 모델 없는 확인 파일 (기기 `/tmp/ch31-prep/`)
- `pgup.sh`(pgenv 클러스터 `127.0.0.1:55431` 켜기 + `trap EXIT` 끄기) · `exp/e1_versions.py`(판·풀 클래스·`TimeoutError` 계보) · `e2_async.py`(01 — 세션·`gather`·세션 함께 쓰기) · `e3_tx.py`(02 — CHECK 위반 Before/After·세션 판) · `e4_alembic.py`(03 — 적용·데이터 사라짐·NOT NULL 실패·기본값 판·`history`·`check`) · `e4b_nodown.py`(03 — downgrade 없음) · `e5_pool.py`(04 — 옛 장면 5회·`sleep(0)` 3회·반납 누락 3회) · `e6_shared.py`(05 — pgvector·계획·`setup()` 표·줄 수·로컬 `pg_dump`·확장 없이 복원 실패·복원·복원 DB `get_state`·아카이브) · `e7_pgembed.py`·`e7b_pgembed.py`(pgembed 서버·asyncpg·`pg_dump`·`psql` 세그폴트) · `rzip*.py`(휠 목록을 내려받지 않고 원격으로 읽음) · `ast_scan.py`·`ban.py`·`snapshot.py`·`manifest.py`.

### 참고 자료 (2026-09-29 확인)
- SQLAlchemy asyncio `https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html` — 「A single instance of AsyncSession is not safe for use in multiple, concurrent tasks」 · 「Using AsyncSession with Concurrent Tasks」(작업마다 세션) · `expire_on_commit=False` · `await engine.dispose()`.
- psycopg 3 async `https://www.psycopg.org/psycopg3/docs/advanced/async.html` — 「On Windows, Psycopg is not compatible with the default ProactorEventLoop. Please use a different loop, for instance the SelectorEventLoop.」
- LangChain/LangGraph 메모리 `https://docs.langchain.com/oss/python/langgraph/add-memory` — `pip install -U "psycopg[binary,pool]" langgraph langgraph-checkpoint-postgres` · `PostgresSaver.from_conn_string(DB_URI)` · 「You need to call checkpointer.setup() the first time you're using Postgres checkpointer」.
- PyPI JSON(기기 `curl`): `pgserver` 0.1.4(2024-06-08, 휠 태그 넷) · `pgembed` 0.1.7~0.2.0(휠 태그·크기) · `postgresql-binaries` 18.6.0 · `postgresql-wheel` 14.1.2 · `testing.postgresql` 1.3.0 · `pytest-postgresql` 9.1.0 · `py-pglite` 0.5.3. `pgembed` 저장소 `https://github.com/Ladybug-Memory/pgembed`(Apache-2.0, pgserver 갈래) · ParadeDB `https://github.com/paradedb/paradedb`(AGPL-3.0).
- 설치판 소스·동작: `sqlalchemy.exc.TimeoutError` 계보 · `AsyncAdaptedQueuePool` · Alembic 1.16.5 `Will assume transactional DDL.` · pgenv `vector.control` `default_version = '0.8.1'`.
