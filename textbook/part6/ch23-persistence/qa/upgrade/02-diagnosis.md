# 02절 진단과 개선 기록 — PostgresSaver 준비와 스키마 (paired)

- 대상: `_src/02-PostgresSaver-준비와-스키마.html` · `labs/part6/ch23-persistence/notebooks/02-PostgresSaver-준비와-스키마.ipynb` · 그림 `figures/02-1`~`02-5`.
- 생성기: `qa/upgrade/author_02.py`(노트북 + `_src`, 01 생성기를 가져와 같은 셀은 글자 그대로 쓰고 `assert`로 대조, `8a6fb7352dd71fafba501f3adc0258d53a1fc8ce0a8e58ecb97100d1022b1fc0`) · `_src` `8009051ac676…` · 빌드 HTML `03bde627d942…` · 실행 전 준비 `qa/upgrade/pre_exec.sh`(새 파일 — PostgreSQL 켜고 끄기, `8f078591f4803ef9525c29ae04d2001980e0c40524df42aed8f03c5473f55c0b`). 그림 설계표 `qa/upgrade/02-figures.md`. 검토 묶음 `qa/upgrade/review-pack/02-PostgresSaver-준비와-스키마.md`.
- 작업일 2026-09-25(UTC 08:2x~09:0x). 형식 **paired 유지**, **슬러그·제목 그대로**(제목의 「스키마」는 강사 확인 — §12).
- **모델 요청 0번**(노트북·노트북 밖 모두, 챕터 리드 결정 1). 키 셀 없음. 흔들림 확인 대상이 없어 `02-probe.md`는 만들지 않았습니다.

## 1. 게이트 전후

| | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전 (`gates-before.json`) | 4 | 77 | 2 | 1 | 0 | 0 | 6 | 28 | 3 | **40** |
| 첫 실행 전 (`gates-wip-02-02.json`, 노트북·`_src`만 쓴 판) | 28 | 356 → 361 | 0 | 0 | 0 | 0 | 0 | 5 → 0 | 18 | — |
| 후 (`gates-wip-02.json`) | **28** | **366** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G1·G2 **0**(과제 지시대로 첫 실행 전에 먼저 검사). 첫 검사 G6 5 = 70자 넘는 문장 넷(참고 자료 셋·기준 버전 한 줄) + 영문 시작 하나(「PostgreSQL의 …」) → 고친 뒤 다시 검사해 G6 0, 이 파일은 둘째 검사 값입니다. 고치며 기준 버전 단락이 여섯 문장이 되어 둘로 나눴습니다. G7 18 = 그림 파일·설계표가 아직 없던 때의 값.
- 그림을 넣은 뒤 첫 `--no-exec`에서 G5 1(8절 앞 결과 읽기 첫 단락의 백틱 `ch23_lab`이 그 셀 출력에 없음) → 「2절에서 만든 이름 공간」으로 바꿔 0.
- AST 따로(`/tmp/ch23-02/extra_check.py` — 01 판 복사, 허용 목록 그대로): 노트북 **0건**. 클래스는 01과 같은 `CountState(TypedDict)` 하나, 함수 힌트·반환 힌트·데코레이터·f-string·내포식·`lambda`·조건 표현식·`elif`·`next`·`.get`·`+=`·기본값·튜플 풀기·별표 풀기·**`with`**·`is`·**`except Exception`** 0.
- 금지어(`/tmp/ch23-02/ban_check.py` — 01 판): 노트북·`_src`·캡션 다섯·`.mmd` 넷에서 참 금지어 **0건**. 걸린 것은 제목(노트북 첫 줄·`_src` meta 줄의 슬러그)의 「스키마」와 「프로그램」 안 「로그」뿐입니다.
- 코드 줄(`count_code.py`) 41 → **123**(셀 4 → 28). 준비 셀이 아닌 셀의 주석 뺀 코드 최대 **9줄**(`column_names` 정의 셀), 함수 본문 최대 **8줄**(`column_names`), 셀당 정의 하나, 첫 줄 주석 100%.

## 2. 수정 전 주요 문제 (준비 노트 §1·§2 02)

1. **셀 넷**: c4 15줄 넘음(이름 공간 만들기 + 상태 형식 + `lambda state:` 노드 + 설계 객체) · c6 `except Exception as exc`(너무 넓음)·f-string 계산 · c8 내포식 `[row[0] for row in rows]`·`with psycopg.connect` 두 번·`assert … and …` 세 조건.
2. **접속**: 옛 접속 글 `postgres:postgres@localhost:55432/postgres`와 실습 README의 Docker `postgres:17` — **Ch 12 02 컨테이너와 같은 포트 55432**라 둘을 함께 켤 수 없음. 환경 변수 `CH23_POSTGRES_URI`와 `?options=-csearch_path%3Dch23_lab`(URL 인코딩)도 설명 없이 씀.
3. **틀린 문장**: b3 「Ch4에서 PostgreSQL 스키마와 information_schema.tables를 조회했습니다」(Ch 4 03은 SQLite, PostgreSQL·psycopg는 Ch 12 02, `information_schema`는 과정 처음) · b6 「PostgreSQL이 … 반환한 오류」 · 금지어 「스키마」 15/7/1·「마이그레이션」·「검증」·「반환」·「경로」·「트랜잭션」·「로그」·「원문」.
4. **노트북 설명**: 제목 셀·「이 노트북에서 할 일」·준비물·그림 첨부·결과 읽기 0. After 앞 설명 셀이 b5 둘째 단락 글 그대로.
5. **관찰 범위**: 표 이름 넷과 값 12만 보고, 표 만들기 기록·표의 칸·체크포인트가 표에 몇 줄로 쌓였는지는 없음. 01과 다른 그래프(값 6 → 12)라 01의 이어 실행과 견줄 수 없음.
6. **그림**: 옛 `{{svg:02-흐름}}` 한 장(상자 넷 한 줄, 값 없음), Mermaid·삽화 0.

## 3. 바꾼 것

- **그래프**: 01 상태 형식 `CountState`·노드 `add_amount`를 **글자 그대로** 가져오고(생성기 `assert STATE == author_01.STATE` 등), 설계 객체 셀은 01과 같은 줄에 `compile(checkpointer=saver)`만 다름. 설정 딕셔너리 셀 `CONFIG_A`·값 바꿔 보기 셀 `CONFIG_B`·작업 폴더 셀 `FILES`도 01 셀과 글자까지 같음(assert). 임시 폴더 셀은 앞머리만 `ch23-02-`(assert).
- **paired Before = 실제 결함**: 같은 그래프·같은 체크포인터·같은 입력(01 첫 실행 `total 0·amount 3`, 스레드 `customer-a`)에서 **`setup()` 한 줄만 다름**. Before는 `except psycopg.Error as error`(Ch 12 02 모양)로 받아 `type(error).__name__`·`error.diag.message_primary`·`error.sqlstate` 출력 → `UndefinedTable` · `relation "checkpoints" does not exist` · `42P01`(두 번 같음). 이어서 이름 공간에 표가 여전히 `[]`인 것을 봄(체크포인터가 표를 스스로 만들지 않음). 서버가 없을 때의 `OperationalError`와 구별하는 문장을 결과 읽기와 b7에(§7).
- **After**: `saver.setup()` → 표 넷(`checkpoint_blobs`·`checkpoint_migrations`·`checkpoint_writes`·`checkpoints`, `assert` 표 수 4) → 표 만들기 기록 `checkpoint_migrations` 열 줄 판 번호 `[0, …, 9]` → 01과 같은 두 입력으로 합계 3 → 7(`assert`) → 표 `checkpoints`의 칸 일곱 → `get_state_history` 6 = 표 줄 수 6(`assert` 같음) → 값 바꿔 보기 둘(`setup()` 한 번 더 — 기록 10·`customer-a` 6 그대로 / 스레드 `customer-b` — 합계 4·표 3줄) → 체크포인터 연결을 먼저 닫고 조회 연결로 센 `customer-a` 6줄 그대로 → 두 연결 닫힘 `True` → 작업 폴더 `[]`.
- **연결 모양**: Ch 12 02처럼 `psycopg.connect(…, autocommit=True)` → `cursor()` → `execute`/`fetchone`/`fetchall` → `close()`. 체크포인터에는 따로 연 연결(`row_factory=dict_row` — 설치판 패키지 설명이 직접 만든 연결에 요구)과 `SET search_path TO ch23_lab`을 넘김. **`with`는 쓰지 않음**(`with PostgresSaver.from_conn_string(…)`은 b7 한 줄 — 설치판 소스로 「블록이 끝나면 연결을 닫음」 확인, 노트북에서 실행 안 함). 옛 URL `?options=-csearch_path%3D…`와 환경 변수 `CH23_POSTGRES_URI`는 뺌.
- **표 만들기 문장 목록**: 서버에 보내지 않고 `PostgresSaver.MIGRATIONS` 열 문장의 첫 줄을 출력(3절) → 6절 기록 열 줄과 판 번호로 짝지음.
- **SQL 조회 함수 셋**(인자로만 받음): `table_names(cursor)`(`information_schema.tables`, 본문 7줄) · `column_names(cursor, table_name)`(`information_schema.columns`, 자리표시자 `%s`, 본문 8줄) · `count_checkpoints(cursor, thread_name)`(`count(*)`·`WHERE thread_id = %s`, 본문 3줄). 표 이름 목록은 내포식 대신 `for`+`append`, 정렬은 SQL `ORDER BY`(Ch 4 03).
- **새 말 셋**(meta 「새 용어 3」 그대로): 이름 공간(SQL 낱말 `SCHEMA`) · 표 만들기(`setup()`) · 표 만들기 기록(표 `checkpoint_migrations`) — 세 문장(뜻 → 일상 예 → 코드). 「마이그레이션」은 속성 이름 `MIGRATIONS`에서 「Ch 21 04절의 「옮기기」와 같은 영어 낱말이지만 여기서는 표를 만들고 고치는 문장의 차례」로 한 번. 제목의 「스키마」는 본문에서 「제목의 마지막 말은 체크포인터가 쓰는 표들의 구조, 곧 표 이름과 표의 칸」으로만 가리키고 낱말은 쓰지 않음.
- **b3 고침**: Ch 4 → **Ch 12 02**(링크 `../../part3/ch12-retrieval-tuning/02-pgvector와-HNSW.html`) + Ch 4 03 `SELECT … WHERE … ORDER BY` 모양 + Ch 2 05 `try`·`except` + 01절.
- **본문 10블록 다시 씀**: b4 비유(사진첩과 속지) + 용어 표 + 「표를 먼저 만들어야 하는 까닭」·「다른 상황에 적용」·「비교와 경계」 · b6 Before/After 표 · b7 열 줄(교재 출력 환경·`OperationalError`·암호·이름 공간 지우기·연결 인자·`with` 모양·쓰기 표·ID 값·실행 안 한 것·시간) · b10 절에 맞는 참고 자료(문서 둘·패키지 설명·소스 행).
- 옛 판의 운영 조언(「배포 마이그레이션과 실행 계정의 권한을 분리」·「일반 요청마다 반복하지 않음」·「CREATE INDEX CONCURRENTLY라 명시적 트랜잭션 안에서 부르지 않음」)은 실행하지 않은 조언이라 뺐습니다. b7에 「권한 나누기·백업·연결 묶음은 이번에 실행하지 않았습니다」만.

## 4. 작업 환경 — PostgreSQL (챕터 리드 결정 3, 선택지 A)

- **학생 쪽 안내(본문·노트북)**: **Ch 12 02절 Docker 컨테이너 `hankyung-part3-pgvector`를 그대로 씀** — 접속 글 `postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab`(Ch 12 02와 글자 같음). 꺼져 있으면 `docker start …`, 없으면 노트북 첫 셀에 적은 Ch 12 README와 같은 `docker run` 명령. 노트북은 그 데이터베이스 안 **이름 공간 `ch23_lab`만** `DROP SCHEMA IF EXISTS … CASCADE` → `CREATE SCHEMA`(다른 이름 공간의 표는 지우지 않음 — Ch 12 표는 기본 이름 공간 `public`에 있음, Ch 12 컨테이너로는 실행하지 않았음). **포트 충돌이 사라짐**(옛 판 `postgres:17` 컨테이너와 Ch 12 컨테이너가 모두 55432).
- **작업 기기**: Docker 없음 → 새 `qa/upgrade/pre_exec.sh`(Ch 12 판을 본으로). `run_section.sh`가 절 실행 직전 source 하며 **`N=02`일 때만** 동작: ① 127.0.0.1:55432에서 이미 받는 서버가 있으면(예: Ch 12 서버) 멈춤(`return 1` → `set -e`) — Ch 12 데이터 폴더에 이름 공간이 생기지 않게 ② 클러스터 `/tmp/ch23-02/pgdata`가 없으면 Ch 12가 둔 conda-forge PostgreSQL 17.11(`$ROOT/.cache/vm/pgenv/bin`)로 `initdb -U student`(암호 파일 = 교재에 이미 있는 수업 전용 암호, 로컬 소켓 trust·TCP scram-sha-256) ③ `pg_ctl … -p 55432 -c listen_addresses=127.0.0.1 -k /tmp/ch23-02 -w start` ④ **`trap … EXIT`로 부른 셸이 끝날 때 `pg_ctl -m fast -w stop`** ⑤ 데이터베이스 `rag_lab`이 없으면 `createdb`. **Ch 12 `.cache/vm/pgdata`는 건드리지 않음**(읽지도 켜지도 않음).
- 확인: 첫 켜기(08:23:28Z) 뒤 다음 호출에서 `pg_isready` → `no response`, `postmaster.pid` 없음, postgres 프로세스 0(로그 `database system is shut down`). 이후 모든 호출(A·B·`--no-exec` 셋·탐색 둘) 뒤에도 `no response`. 클러스터 41MB.
- **교재 출력과 학생 환경의 차이**(b7·준비물에 한 문장씩 — Ch 12 02 문장 「이번 교재 출력은 그 환경에서 만들지 않았습니다」 그대로): 교재 출력은 Docker 이미지 `pgvector/pgvector:0.8.2-pg17`이 아니라 같은 접속 글로 켠 conda-forge PostgreSQL **17.11**. 출력 줄 `PostgreSQL 판: 17.11`만 서버에 따라 달라질 수 있음. psycopg는 Ch 23 잠금 **3.3.3**(Ch 12 잠금은 3.3.5 — 실습 폴더가 달라 충돌 없음).
- 판: langgraph 1.2.11 · langgraph-checkpoint-postgres 3.0.5 · psycopg 3.3.3(binary, libpq 18) · psycopg-pool 3.3.1(가져오기 때 필요 — `postgres/__init__.py`가 `psycopg_pool`을 가져옴, 그래서 설치 셀은 `psycopg[binary,pool]`). 설치 셀은 셋(이 절이 가져오는 패키지만 — 01과 달리 `langgraph-checkpoint`는 직접 가져오지 않음). `pip==26.2`는 잠금 dev에 있음(규격 §7-2 확인만). 가상환경 `$ROOT/.cache/vm/venv-ch23-persistence` 그대로(새로 넣은 패키지 0).

## 5. 새 커널 두 번 (규격 §2-7 9번 끝)

- A `run_section.sh`(셀 실행 기록 08:37:25.16~08:37:26.36Z, 약 1.2초) — 새 커널 **`PASS 02-…ipynb: 28 cells`**. 이 실행은 그림 파일이 아직 없어 `attach_figures.py`에서 멈췄고(과제 차례대로 그림을 그리기 전에 두 번 실행), 서버는 trap으로 꺼짐. A는 **새 클러스터**(이름 공간 없음)에서 시작.
- B 사본 `/tmp/ch23-02/B.ipynb`를 같은 호출 안에서 `pre_exec.sh`로 서버를 켜고, **`DROP SCHEMA IF EXISTS ch23_lab CASCADE`로 A가 남긴 표 넷을 지운 뒤**(psql, 이름 공간 0 확인) `execute.py`로 실행(08:37:47.48~48.57Z, `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch23-persistence UV_NO_SYNC=1 PYTHONPATH=…/notebooks`). 두 실행 모두 이름 공간 `ch23_lab`이 없는 데이터베이스에서 시작.
- 셀별 출력 글자 대조(`/tmp/ch23-02/cmpout.py`) **28/28 같음**. `code_sha256` **`5b4fa7cf7d928a76570c80ce762c242d76c476f77f6dacd341beab251cebf767`**, `outputs_sha256` A·B 모두 **`abb4f3d737b322ceb3feecabfb4bd96bf48bfec271702d79c7e88213a311c45d`**. 흔들린 값 없음. b6 「새 커널로 두 번 실행했을 때 코드 셀 28개의 출력이 모두 같았습니다」.
- 그 뒤 `mdpatch.py` 셋(그림 alt·도식 읽기, 결과 읽기 두 문장, `information_schema` 두 문장)과 `attach_figures.py`는 마크다운만 바꿈 — `code_sha256`·`outputs_sha256`·`executed_at`(08:37:26Z) 그대로, 교재 노트북과 A 사본 셀별 출력 28/28 같음.
- 준비물 「5초 안에」는 A 셀 실행 기록(약 1.2초)을 넉넉히 둔 값(설치 셀은 네트워크에 따라 다름).

## 6. 도구 파일 — 만들지 않음 (챕터 공통 5)

- 02는 01 함수 `print_history`·`thread_row`를 **쓰지 않음**. 체크포인트 수는 `len(list(graph.get_state_history(…)))`를 변수에 담아 표 줄 수와 견주는 데만 썼고(한 줄씩 출력은 01과 같은 여섯 줄이라 되풀이하지 않음), `thread_row`는 01 칸 전용 기록 줄이라 이 절의 비교(표 줄 수)와 다름.
- 02가 처음 가르친 함수 셋(`table_names`·`column_names`·`count_checkpoints`)은 PostgreSQL `information_schema`·이름 공간 `ch23_lab`·표 `checkpoints` 전용이라, SQLite를 쓰는 03~06이 그대로 쓸 수 없음(SQLite는 `sqlite_master`·`?` 자리표시자). 노트북에 둠.
- 그래서 `notebooks/checkpoint_tools.py`를 만들지 않았고 묶음 목록(`textbook/part6/public-files.json`·챕터 `qa/public-files.json`) 변경 0. 01 노트북이 가져오는 이름도 그대로(01 다시 실행 없음).

## 7. 설치판 동작과 문서 (모델 없는 확인, 2026-09-25)

- **노트북 밖 확인**: `/tmp/ch23-02/probe1.py`(노트북 흐름 그대로 + 표 줄 직접 읽기, 출력 `probe1.out`) · `probe2.py`(서버를 끈 뒤 같은 접속 글 → `OperationalError`, 종류 사다리 `OperationalError → DatabaseError → Error`, 출력 `probe2.out`). probe1에서 본 것: 오류 뒤 연결 상태 IDLE(같은 연결로 `setup()`이 됨) · `setup()` 전 `get_state`도 `UndefinedTable` · 두 번 실행 뒤 `checkpoint_writes` 10줄·`checkpoint_blobs` 5줄(칸 `__start__`·`trace`만 — 수·글 값은 `checkpoints` 안) · `metadata`의 단계 −1~4·만든 자리 `input`/`loop`. **본문에는 줄 수 10·5를 넣지 않음**(05 몫 — 표 이름과 쓰임만, 「설치판 소스로만 보았고 줄은 읽지 않았습니다」).
- **출력으로 본 것**(결과 읽기·본문 근거): §3의 값 모두.
- **소스로만 본 것**(본문에 「설치판 소스」로 표시): `PostgresSaver.setup()` 설명 「It MUST be called directly by the user the first time」·기록 다음 문장부터 실행(`langgraph/checkpoint/postgres/__init__.py` 77~102행) · `from_conn_string`이 `autocommit=True`·`prepare_threshold=0`·`row_factory=dict_row`로 열고 `with`로 닫음(54~75행 + psycopg `connection.py` 155~176행 `__exit__` → `close()`) · 수·글·`None`이 아닌 칸 값은 `checkpoint_blobs`로(301~308행) · 쓰기 저장(336~351행) · `MIGRATIONS` 열 문장(`base.py` 37~85행) · 체크포인터를 만들 때는 데이터베이스에 문장을 보내지 않음(`__init__` 37~51행) · 실행 시작 때 마지막 체크포인트를 찾음(`langgraph/pregel/_loop.py` 1651~1654행) · SQLite `setup()` 「called automatically … should not be called directly」(`sqlite/__init__.py` 122~128행).
- **패키지 설명**(`langgraph_checkpoint_postgres-3.0.5.dist-info/METADATA`): 처음 쓸 때 `.setup()` · 직접 만든 연결에 `autocommit=True`·`row_factory=dict_row`. PostgreSQL 필수 최소 판은 적혀 있지 않음(준비물에 그대로 적음).
- **공식 문서**(WebFetch 2026-09-25): Checkpointers — Postgres 체크포인터 「Ideal for using in production」와 `checkpointer.setup()` 예 · Persistence — 프로덕션용 체크포인터 목록의 `PostgresSaver`, `checkpointer.setup()  # Creates tables with indexes`.
- **이번에 실행하지 않은 것**(본문에 그렇게 적음): `with PostgresSaver.from_conn_string(…)` 모양 · 연결 인자 하나를 빠뜨린 장면 · 서버가 꺼진 셀(노트북 밖만) · 여러 프로그램이 같은 표를 쓰는 모습·연결 묶음·권한·백업 · 쓰기 표·값 표의 줄 · 새 연결·새 그래프 객체로 이어 가기(03 몫) · 걸린 시간 · Docker 이미지 서버 · Windows·macOS.

## 8. 그림

| 그림 | 종류 | 원본 폭(viewBox) | 확인 |
|---|---|---|---|
| 02-1 연결 둘과 이름 공간 하나 | `flowchart TB` 상자 다섯 + subgraph 하나 | 501 | 첫 판 연결·표 넷 라벨이 저절로 꺾여 `<br>`로 미리 나눔. PNG에서 체크포인터 연결이 왼쪽, 조회 연결이 오른쪽 — 도식 읽기를 그 방향으로 |
| 02-2 표 만들기 문장 열과 기록 열 줄 | `flowchart TB`(넷 이상 한 줄) + subgraph 안 `LR` 둘 | 463 | 첫 판 `PostgresSaver.MIGRATIONS`가 낱말 가운데서 꺾여 「속성 MIGRATIONS」로. 설계 때 「왼쪽에서 오른쪽」으로 적은 도식 읽기를 「위에서 아래」로 고침 |
| 02-3 표를 만들기 전과 뒤 | `flowchart TB` + subgraph 둘 + 공통 파란 상자 | 679 | Before 왼쪽·After 오른쪽, **빨강 두 상자는 Before 결함 결과만** |
| 02-4 스레드마다 표에 쌓인 줄 | `flowchart TB` + subgraph 둘 + `~~~` 회색·노랑 | 535 | 회색은 두 칸 공통(같은 표·칸 `thread_id`로 가름), 맨 아래 노랑은 9절 출력 |
| 02-5 속지를 끼운 사진첩과 빈 사진첩 | Higgsfield 삽화 | 1100 × 614 | 아래 |

- 색: 접속 글·연결·입력 초록 · 그래프·부른 메서드 파랑 · 출력 값 노랑 · 체크포인터·설치판 문장 목록·공통 사실 회색 · **빨강은 02-3 Before 두 상자만**(셀에서 받아 출력했어도 paired Before 결함 결과 — 규격 §5-3, Ch 19 01·Ch 20 02 선례) · **보라 0**. 라벨 숫자 대조: 두 자리 이상(`55432`·`127.0.0.1`·`42P01`·`23`)은 G7이 출력·본문과 대조해 통과, 한 자리(`0`·`3`·`4`·`7`·`9`)는 손으로 대조(3·6·8절 출력).
- 삽화: 1차 job `a9632856-4ca1-4d66-90b4-956ca02806a1` **탈락**(오른쪽 맨 위 속지 사진 **아홉 장**, 겹친 속지 수를 셀 수 없음) → 2차 job **`21f990d2-0483-48b0-ac22-14fdae21a1f5` 채택**(왼쪽 빈 고리 + 밖의 사진 한 장 · 오른쪽 속지 한 장에 사진 여섯 장 두 장씩 세 줄 · 카메라 하나). 거래 08:39:59Z·08:42:00Z 「Nano Banana Pro −2」 두 줄 = **이 절 4크레딧**(잔액 2445.75 → 2441.75). 저장 PNG `02f1edef…`와 채택 job 결과를 같은 폭으로 줄인 그림의 픽셀 대조 bbox `None`·최대 차이 0, 1차와는 다름. 세부 `figures/02-5-…prompt.md` 「상태」.
- 삽화가 「속지 넷」을 그리지 못해(1차), 비유 단락의 「속지 네 장을 끼우는 일」을 「속지를 끼우는 일이고, 이 절에서는 표 넷을 한꺼번에 만듭니다」로 바꾸고, 그림 읽기에 「속지는 표 `checkpoints` … 나머지 표 셋은 그림에 없고」를 적음.
- 옛 그림 `figures/02-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 참조 0, 사본 `before/figures/`).

## 9. 서비스 요청과 비용

- 모델·임베딩 요청 **0번**(노트북 A·B, 노트북 밖 확인 모두). 키는 읽지 않음(`env -u OPENAI_API_KEY`로 탐색).
- Higgsfield 2회 생성, 4크레딧(§8).

## 10. 챕터 밖 수정

- **없음.** 새 파일 `qa/upgrade/pre_exec.sh`는 챕터 안(공용 `run_section.sh`는 고치지 않음 — 이미 `pre_exec.sh`를 source 함). `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json`은 `verify.py --chapter`가 다시 씀(보호 목록 안, `manifest-changes.md`). 공용 도구·규격·과정 요약·계약 파일·Part 목록·묶음·실습 폴더 README·`pyproject.toml`·`uv.lock` 그대로.
- `_build.py`가 01·03~06 HTML·`index.html`도 다시 씀 — `_src`·노트북이 그대로라 내용 변화 없음.

## 11. 뒤 챕터·완료 챕터가 02에 기대는 문장 (고치지 않음, 참·거짓만)

| 자리 | 문장 | 판정 |
|---|---|---|
| **Ch 31 05 `_src` b3(대기)** | 「Ch23에서는 PostgresSaver의 `setup()`이 체크포인터 표를 만든다는 점을 확인했습니다」 | **참** — 02 6절 출력 `setup() 뒤 표 수: 4`와 표 이름 넷(Before에서는 표 `[]`). Ch 31 05 노트북은 자기 Docker(55431)·자기 그래프(값 6 → 12)로 다시 함 — 고치지 않음 |
| Ch 30 02 b3(대기) | 「Ch21의 Agent와 Ch23의 체크포인터처럼 생성 비용과 수명주기가 다른 객체」 | 02는 연결을 열고 닫았지만 객체 수명을 견주지 않음 → **03 몫**(연결과 그래프 객체를 새로 만드는 장면) |
| Ch 25·26 b3 「Ch23에서 체크포인터와 thread_id」 | — | 01로 참(02도 같은 스레드 이름 씀) |
| 01 `_src` b4 「프로그램 밖에 남기는 체크포인터는 02절과 03절에서 씁니다」 · b8 「02절에서는 체크포인트를 PostgreSQL 데이터베이스에 저장합니다. 그 전에 체크포인트를 담을 표를 만드는 일부터 봅니다」 | — | **참** — 02가 표를 만들고(`setup()`) 그 표에 체크포인트 여섯·셋이 쌓이는 것을 셈, 연결을 닫은 뒤에도 줄 수 그대로 |
| 슬러그 02 | 링크하는 완료 파일 0 | 그대로 |

## 12. 강사 확인 대상

1. **제목의 「스키마」 유지** — 본문은 이 낱말을 쓰지 않고 「제목의 마지막 말은 체크포인터가 쓰는 표들의 구조, 곧 표 이름과 표의 칸」으로 가리킴. SQL `SCHEMA`는 「이름 공간」으로 풂(한 낱말이 두 뜻 — 표 구조 ↔ 이름 공간). 「마이그레이션」은 속성 이름 `MIGRATIONS`만.
2. **학생은 Ch 12 02 컨테이너를 다시 씀** — 실습 폴더 README의 Docker 명령(`postgres:17`·`kdt-ch23-postgres`·postgres/postgres·55432)은 **02 노트북과 어긋난 채**(마감 때 README를 02 준비물과 같게 다시 씀 — 준비 노트 §13). Docker로 교재 출력을 만들지 않음(b7).
3. **Before의 받은 오류를 빨강으로** — 셀에서 받아 출력했지만 paired Before 결함 결과(규격 §5-3 문장, Ch 19 01·Ch 20 02 선례).
4. **코드 줄 41 → 123(셀 4 → 28)** — 늘어난 몫은 표 만들기 문장 목록(3절)·표 만들기 기록(6절)·표의 칸과 줄 세기(7절)·값 바꿔 보기 둘(8절)·연결 닫기(9절).
5. **삽화에서 「속지 넷」을 뺌** — 1차가 사진 수·속지 수를 틀려, 2차는 속지 한 장(= 표 `checkpoints`)만. 사진 여섯 장은 「두 장씩 세 줄」로 나옴(프롬프트 「세 장씩 두 줄」과 방향만 다름).
6. meta 시수(강의 1h · 실습 1.5h)·새 용어 3 그대로.

## 13. 남은 것 · 지워야 하지만 지우지 않은 것

- 마감 몫: 실습 폴더 README Docker 안내(위 2) · `chapter.json` `objectives` 둘째 줄 「PostgresSaver를 준비하고 …」 대조 · 옛 그림 셋 삭제 승인 · `visual.cjs`·묶음 재생성(Ch 21 선례대로 마감).
- 삭제 승인 대상(만들었지만 지우지 않음): 기기 **`/tmp/ch23-02/`**(PostgreSQL 클러스터 `pgdata` 41MB — **서버는 꺼져 있음**, `pg.log`·`initdb.log`·`pwfile`(교재에 이미 있는 수업 전용 암호 한 줄) · `probe1.py`·`probe1.out`·`probe2.py`·`probe2.out` · `A.ipynb`·`B.ipynb` · `cmpout.py`·`extra_check.py`·`ban_check.py`·`resize.py`·`crop.py`·`pixcmp.py` · `reps1.json`~`reps3.json` · `illu-1-orig.png` 5MB급·`illu-2-orig.png`·`illu-2-again.png`) · `.cache/ch23-02-view/`(`illu-1-1100.png`·`illu-1-crop-right.png`·`illu-1-crop-left.png`·`illu-2-1100.png`) · `qa/upgrade/gates-wip-02-02.json`·`gates-wip-02.json`(마감 `gates-after.json`으로 갈음) · `qa/upgrade/__pycache__/`(생성기를 모듈로 읽어 생김).
- `pre_exec.sh`는 지우지 않음 — 02를 다시 실행할 때(마감) 필요. 클러스터가 없어지면(기기 VM을 다시 만들면) `pre_exec.sh`가 새로 만듦.

## 마감 반영 (2026-09-25, 검토 1차 `review-round1-A.md`·`review-round1-B.md`)

- **A-5** `setup()` 문장(노트북 6절 결과 읽기·b4 「표를 먼저 만들어야 하는 까닭」·복습 4 해설)을 설치판 소스대로 — 먼저 기록 표를 만드는 0번 문장(`CREATE TABLE IF NOT EXISTS`, 이미 있으면 아무 일도 하지 않음)을 실행하고, 그다음 마지막 판 번호 뒤 문장만.
- **A-6** 노트북 2절 결과 읽기에 「이 장면은 노트북 밖에서 확인했고, 이 노트북에서는 실행하지 않았습니다」 · 5절 결과 읽기의 `OperationalError` 문장을 「노트북 밖에서 본 …」으로.
- **A-7** b7 `from_conn_string` 문장에 `prepare_threshold=0`(설치판 68~69행). **A-8** b4 「같은 판 소스」 → 「설치한 langgraph-checkpoint-sqlite 3.0.3 소스」(G6 때문에 두 문장으로). **A-9** b5 — 컨테이너가 없을 때의 `docker run` 명령은 이 챕터 실습 폴더 `README.md`(마감에서 다시 씀)와 노트북 첫 셀에 있다고 가리키고, 모델을 부르지 않는 까닭 한 구절을 더함. **A-10** b2 끝과 노트북 7절 머리에 「SQL 낱말 `SCHEMA`는 같은 영어 낱말이지만, 이 절은 그것을 이름 공간이라고 부르고 …」. **A-17(선택)** b4 비유 끝에 「01절의 메모리 체크포인터는 사진첩까지 카메라가 들고 있었다면, 이 절은 사진첩을 카메라 밖에 둡니다.」 **A-1** 셀 44 「이어 실행의 결과」 → 「같은 스레드로 다시 실행한 결과」.
- **A-11(02가 01 노드 함수 `add_amount`를 다시 적음) — 그대로 둠**(챕터 리드 결정: 그래프의 상태 형식·노드는 노트북에 남긴다는 과정 선례 — Ch 20·21 도구 파일에는 평범한 도움 함수만 두고 노드·도구·그래프 조립은 노트북에 둠). 까닭: 노드는 그 절의 그래프를 이루는 부분이라 노트북에서 보여야 하고, 3줄 노드 하나 때문에 02가 도구 파일 가져오기(작업 위치 문장 포함)를 새로 열면 준비가 더 길어짐. 「글자까지 같다」는 01 생성기 상수와 대조한 문장이라 참. 규격 §2-7 3·5번과 다른 예외로 챕터 요약 「강사 확인 대상」에 올림.
- **PostgreSQL은 켜지 않음**: `run_section.sh … 02 --no-exec`는 `pre_exec.sh`를 불러 서버를 켜므로, 같은 단계를 `pre_exec.sh` 없이 부르는 마감 전용 `.cache/ch23-close/tools/nx.sh 02`로 렌더·첨부·빌드·verify·게이트만 함(서버 프로세스 0 확인). **다시 실행하지 않음** — `code_sha256` `5b4fa7cf7d92…`·`outputs_sha256` `abb4f3d737b3…`·`executed_at` 08:37:26Z 그대로(파일 `c3b15aefd635…` → `8722ced25c56…`). 생성기 `8a6fb7352dd7…` → `6e709e215b8e…`(63/63·`_src` 같음). 게이트 0(검사 문장 366 → 377).
