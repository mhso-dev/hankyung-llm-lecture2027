# 05절 진단 — pgvector 체크포인터 공존과 백업 (experiment)

- 작업일 2026-09-29 · 생성기 `qa/upgrade/author_05.py`(`42cd35c9…`) · 노트북 `labs/part7/ch31-database/notebooks/05-pgvector-체크포인터-공존과-백업.ipynb` · 본문 `_src/05-pgvector-체크포인터-공존과-백업.html` · 슬러그 그대로 · DB 준비 훅 `qa/upgrade/pre_exec.sh`(**한 줄 더함** — 아래 「백업 명령 자리」).
- 읽은 것: `handoff.md`(챕터 공통 전부·§04 → §05 전부) · 준비 노트 `chapter-lead-notes.md`(머리·§0·§1·§2 05·§3·§4·§6-4·§7·§8·§9·§10·§12·§14·§15) · `04-diagnosis.md` · 본 생성기 `author_01.py`(전부 — `SETTINGS`·experiment 틀)·`author_04.py`(전부)·`author_03.py`(설정·가져오기·임시 폴더 셀·b7) · Ch 23 02·Ch 12 02·Ch 28 03·Ch 2 08 노트북 코드 셀 · Ch 23 `chapter-summary.md`(§1·용어·§15) · Ch 12 요약(02 줄) · Ch 30 요약(「노드」 허용·금지어) · 과정 요약(Ch 23·처음 쓰면 한 문장) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 규격 `QUALITY-UPGRADE.md`(전부) · 옛 판 노트북·`_src`. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전(`gates-before.json`) | 7 | 101 | 4 | 3 | 5 | 0 | 9 | 21 | 3 | 45 |
| 첫 실행 전(`gates-wip-05-05.json`, G1·G2 먼저) | 31 | 482 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 3(그림 없음) |
| 후(`gates-wip-05.json`, `--no-exec`) | **31** | **509** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

- 첫 실행 전 생성기 대조(`/tmp/ch31-05/tools/pregate.py` — `cells()`·`src_html()`을 임시 노트북으로): G1~G5 0 · 70자 넘는 문장 다섯(버전 문장 둘·노트북 밖 다섯 번 문장·psycopg 참고 자료·설치판 소스 행) · 영어로 시작해 조사가 붙은 문장 하나(b3 「`EXPLAIN`의」) · 5문장 넘는 단락 둘(b4 비유·제목 셀 기준 버전) → 모두 고침. 첫 `--no-exec` 뒤 G5 다섯(결과 읽기 첫 단락의 숫자 든 인용 `pgvector/pgvector:0.8.1-pg17`·`ch31_lab`·`ch23_lab`·`ch31_shared` 둘이 그 셀 출력에 없음) → 둘째 단락으로 옮기거나 말로 바꿔 `mdpatch.py`로 노트북까지(재실행 없음).
- AST 따로(`extra_check.py` — 01~04 판 그대로): 걸린 것은 상태 형식 클래스 `ValueState(TypedDict)` 하나(`ClassDef`·`AnnAssign` — 규격 §2-2 L5·Ch 23 모양, 셀 하나) · 호출 깊이 최대 2 · 준비 셀 밖 셀 최대 9줄 · 함수 본문 최대 7줄(`restore_copy`·`read_restored`·`shared_tables`) · 코드 줄 178(주석·빈 줄 뺌, 옛 판 94) · f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`next`·`try`·`await`·`async def`·데코레이터·힌트·기본값 매개변수·대입 풀기·별표 풀기·세미콜론·한 글자 이름·메서드 셋 이어 부르기 0.
- 금지어(`ban33.py` — 04 판 그대로): `_src`·노트북 마크다운·코드 주석·`.mmd` 넷·캡션 다섯에서 남은 것은 거짓 양성과 허용 말뿐 — 「이벤트」(← 「이벤트 루프」 둘) · 「로그」(← 「프로그램」 둘) · **「노드」 7(마크다운 5·주석 2 — Ch 13 말, Ch 30 선례대로 씀)**. 「인덱스」·「순차」·「스냅샷」·「재개」·「스키마」·「쿼리」·「경로」·「반환」 0 · 사용자가 금지한 표현(과정 규칙) 0(생성기·노트북·`_src` `grep`).
- 인용 대조(`quotes.py`): 노트북 백틱 136개·`_src` `<code>` 61개 가운데 출력·코드에 없는 것은 명령·이름(`docker run`·`docker start …`·`uv sync --locked`·`docker exec -i`·`pg_dump --version`·`text=True`·`table_names`(Ch 23 02 함수)·`InMemorySaver`·`AsyncPostgresSaver`·`from_conn_string`·`--single-transaction`·`-n`·`student`·`ch23_lab`·`postgresql+asyncpg`·이미지 태그·설치판 소스 파일 이름)뿐.

## 수정 전 주요 문제 (옛 판 — `before/notebooks/05-…ipynb`·`before/_src/05-*.html`)

1. **Docker에 묶인 백업**: `docker exec kdt-ch31-postgres pg_dump/dropdb/createdb/psql` — Docker가 없는 곳(작업 기기·Docker 없는 학생)에서는 돌지 않음. 비밀번호·연결 폴더 개념 없이 컨테이너 안 명령만.
2. **`lambda` 노드**, 상태 형식 클래스를 `with` 블록 안에서 정의, `from typing_extensions import TypedDict`도 블록 안 · **코드 셀 25줄**(verify 「max 25 lines」가 이 셀) · 17·18줄 셀 · `import os, subprocess` 한 줄 · `[row[0] for …]` 내포식 둘 · `"\n".join(… for …)` 제너레이터 식 · `assert … and …`.
3. **`EXPLAIN (ANALYZE, BUFFERS, …)`** — 시간·버퍼 줄이 실행마다 흔들림(`actual time`·`Planning Time`) · 「uses hnsw: False」만 보고 색인이 쓰이는 계획은 보이지 않음.
4. 복원한 DB를 지우지 않고 남김 · 확장을 먼저 만드는 까닭(덤프에 확장이 없음)을 설명하지 않음 — 확장 없이 복원하면 무엇이 되는지 보이지 않음 · 체크포인터 표가 `search_path` 연결 주소 옵션으로 이름 공간에 생기는 까닭 설명 없음.
5. 말: 「인덱스」·「스키마」·「쿼리」·「스냅샷」 류 · 새 용어에 「체크포인터」(Ch 23 01 말 — Ch 23 요약 §15 211행) · 비유 「창고와 배송 장부」(Ch 3 가족 겹침) · b6 「Docker PostgreSQL 17.8」 틀 문장 · b7 「Ch11 평가셋으로 변경 전후 측정」(실행 안 함) · b8 「Ch32에서 Compose 서비스로 묶고 헬스체크와 시크릿」.
6. 첫 줄 주석·결과 읽기 0 · 옛 그림 `{{svg:05-흐름}}` 한 장(보라·빨강이 모델·실패 아닌 요소).

## 바꾼 것

- **experiment 설계(챕터 리드 결정 + 이 절이 고른 변수)**: 가설 → 실행 1(확장을 만들지 않은 새 데이터베이스에 복원) → 실행 2(**바꾼 값 하나: 복원 전에 `CREATE EXTENSION vector`**) → 결과 표 → 결론(매번 같은 값). 준비 노트가 적은 변수 후보 `enable_seqscan`은 **Ch 12 02절 실행 3이 이미 한 실험**이라, 이 절은 3절 계획 줄(`Seq Scan on documents`)과 9절 복원 DB 계획 줄(`Index Scan using documents_embedding_hnsw on documents` — 복원한 색인이 쓰이는지)에 설정으로만 씀. 절의 새 내용인 백업·복원에서 변수를 고름 — 준비 노트 「확장 없이 복원 → 실제 조건 실패 장면 후보(노랑)」.
- **공존**: 조회 연결 `conn`(psycopg, `autocommit=True` — Ch 12 02) + 체크포인터 연결 `saver_conn`(`autocommit=True`·`row_factory=dict_row`·`SET search_path TO ch31_shared` — Ch 23 02 모양 그대로) → `PostgresSaver(saver_conn)`·`setup()` → 이름 공간 `ch31_shared`에 표 다섯(`documents` + 체크포인터 넷). **체크포인터 표를 `public`이 아니라 `ch31_shared`에 둔 까닭(노트북 4절 한 문장)**: 이름 공간 하나로 함께 백업하고, 3절 `DROP SCHEMA … CASCADE`가 체크포인터 표도 지워 다시 실행해도 줄 수가 같게. `search_path` 없이 `setup()`을 부르면 `public`에 생김 — 노트북 밖 `e2_public.py`로 따로 만든 DB에서 확인(b7·복습 1).
- **모델 없음**: 이름 있는 노드 함수 `double_value`(값 두 배 — 「모델을 쓰지 않는 그래프」로 공개, Ch 23 01 선례) · 가짜 채팅 모델 0 · 벡터는 손으로 정한 3차원 값(배송·환불·결제 쪽)과 질문 벡터 `[0.9,0.1,0]` — **실행 전에 정했다는 것과 뜻을 셀 주석·설명에**, 임베딩 모델이 만든 값이 아님을 밝힘.
- **백업 명령 자리(챕터 리드 결정)**: 노트북 5절 `shutil.which("pg_dump")` → 있으면 `command_start = []`·`server_args = ["--host=127.0.0.1", "--port=55431", "--username=postgres"]`, 없으면 `["docker", "exec", "-i", "kdt-ch31-postgres"]`·`["--username=postgres"]`(공식 이미지는 컨테이너 안 접속을 trust — Docker Hub 문서) — **조건 표현식 없이 `if`/`else`**, 출력은 `명령을 부를 자리: 이 컴퓨터` 한 줄(찾은 위치는 출력하지 않음). 비밀번호는 `dict(os.environ)` 복사(Ch 28 03 모양)에 `PGPASSWORD`로(명령 목록·출력에 없음 — b7에 문서의 보안 권고). 함수 `run_tool(tool_args, input_bytes)`가 `subprocess.run(command, input=…, capture_output=True, env=tool_env)`(Ch 2 08 이음 — `text=True` 없이 바이트) · 덤프는 표준 출력 바이트를 `tempfile.mkdtemp(prefix="ch31-05-")` 폴더의 파일에 `"wb"`로 쓰고(03 b7 「데이터베이스를 파일로 남겨야」를 참으로), 복원·목차는 그 파일을 입력으로 보냄 → **컨테이너 쪽도 같은 셀로 됨**(교재 출력에서는 실행하지 않았다고 제목 셀·5절·b7·그림 05-2 회색에 한정). 출력에 위치·바이트 수 없음.
- **pgvector·색인**: `CREATE EXTENSION IF NOT EXISTS vector`(확장은 `public` — 7절 오류 글 `public.vector`로 이음) · `vector(3)` 표 · HNSW(`vector_cosine_ops`) · `<=>` 가까운 둘 `[('배송', 0.0061), ('환불', 0.8896)]` · `EXPLAIN (COSTS OFF)`(ANALYZE 없이 — 시간 줄 없음, 매번 같음) → `Seq Scan on documents`.
- **체크포인터 저장(Ch 30 10 b8 유지)**: `graph.invoke({"value": 6}, …)` → `{'value': 12}` · `get_state` 같음 · 표 줄 수 `checkpoints 3 · checkpoint_blobs 1 · checkpoint_writes 3 · checkpoint_migrations 10`(준비 노트 `(3, 1, 3, 10)`과 같음).
- **덤프 목차**: `pg_restore --list` 원문 줄은 항목 번호(OID)가 실행마다 바뀌어(노트북 밖 5번) 출력하지 않고, 목차 글에 ` TABLE ch31_shared documents `·` TABLE ch31_shared checkpoints `·` EXTENSION `이 있는지만 → `True`·`True`·`False`.
- **복원 결과(결정적)**: 실행 1 `pg_restore 종료 코드: 1` · 오류 첫 줄 `pg_restore: error: could not execute query: ERROR:  type "public.vector" does not exist` · 끝 줄 `pg_restore: warning: errors ignored on restore: 5` · 표 넷(`documents` 없음, 체크포인터 줄 수 원래와 같음) · `저장된 값: {'value': 12}` ↔ 실행 2 `0`·오류 0줄·표 다섯(`'documents': 3`)·`{'value': 12}` · 복원 DB `SET enable_seqscan = off` 계획 `Index Scan using documents_embedding_hnsw on documents`. **오류 수**: 노트북 밖 첫 판(`e1_scene.py` — `pg_restore --no-owner`)은 넷, 노트북은 `--no-owner`를 주지 않아 표 주인 정하기(`ALTER TABLE … OWNER TO postgres`)까지 **다섯** — 모두 `ch31_shared.documents`에 걸림(노트북 밖 `e3_scene.py` 전체 오류 출력, b7에 「노트북 밖에서」로). 사본 시험에서 이 차이를 보고 글을 다섯으로 고침(설계는 그대로).
- **동기·비동기**: 1절·b3 「01·02·04절은 asyncpg 비동기 엔진, 이 절은 03절처럼 동기 psycopg — `PostgresSaver`가 psycopg 동기 연결을 쓰기 때문」 · b7 「비동기 체크포인터 `AsyncPostgresSaver`도 있다(LangGraph 문서), Windows에서 psycopg 비동기와 기본 이벤트 루프가 맞지 않는다(psycopg 문서), 실행하지 않았다」.
- **접속 글**: `postgresql://postgres:postgres@127.0.0.1:55431/ch31_lab` — 01 설정 셀에서 드라이버 부분만 다름(생성기 `__main__`에서 `replace` 대조, 「글자까지 같다」 쓰지 않음) · 복원 DB 글은 `replace("/ch31_lab", "/ch31_restore")`.
- **다시 실행해도 같게**: 3절 첫 셀이 `DROP DATABASE IF EXISTS ch31_restore` → `DROP SCHEMA IF EXISTS ch31_shared CASCADE` → `CREATE SCHEMA` · 끝 셀이 체크포인터 연결을 닫고 `DROP DATABASE ch31_restore`·`DROP SCHEMA ch31_shared CASCADE` → `남은 이름 공간: None`·`남은 복원 데이터베이스 수: 0` · 복원 DB에 붙는 연결은 함수마다 닫음(누가 붙어 있으면 지울 수 없음 — PostgreSQL 문서). **확장 `vector`는 `ch31_lab`의 `public`에 남김**(노트북 10절에 밝힘 — 다시 실행하면 `IF NOT EXISTS`) · 덤프 파일은 운영체제 임시 폴더에 남김(노트북 밖, 지우지 않음).
- **말**: pgvector·체크포인터·공존(제목 말 — 1절·b2 첫 자리 풂) · 새 용어 meta **3**(백업·복원·덤프 파일 — 옛 5) · 체크포인터·체크포인트·스레드(Ch 23 01)·표 만들기 `setup()`·표 만들기 기록·이름 공간(Ch 23 02)은 새 용어로 세지 않음 · 색인·HNSW·계획 줄·색인 스캔(Ch 12 02 이어 씀) · `Seq Scan`은 「표의 줄을 처음부터 모두 읽는 계획」(Ch 12 말 「순차 스캔」은 Ch 31 금지어 「순차」 때문에 인용하지 않음) · 확장(풀이만 — 「PostgreSQL에 새 자료형과 함수를 더하는 꾸러미」) · 패키지·서버 번호는 「버전」(03·04 모양 — 교환대 비유와 겹치지 않게) · 한 묶음 작업(02 — `CREATE DATABASE`는 한 묶음 작업 안에서 돌지 않음·`--single-transaction`).
- **비유 「전화 교환대」 이어 씀**: 배선표 = 덤프 파일 · 새 판에 다시 꽂기 = 복원 · 판에 따로 다는 자리 = 확장 vector · 회색 선 넷 = 체크포인터 표 넷 · 노란 초록 선 = 검색 문서 표 · 왼쪽(자리 없음) = 실행 1, 오른쪽 = 실행 2 · 「비유와 다른 점」: 실제 복원은 파일의 SQL 글로 표를 새로 만들고 줄을 넣는 일.
- 도구 파일: 만들지 않음(챕터 공통 8 S1 — `shared_tables`·`run_tool`·`restore_copy`·`read_restored`·`restored_state`는 이 절의 전역 `cur`·`command_start`·`dump_bytes`·`builder`에 기댐).

## 백업 명령 자리 — 훅 한 줄 (다섯 절 공통 파일)

- `qa/upgrade/pre_exec.sh` **`8a9529f101ef38bdbf57ae31118c70fd53736df65ca884038fe1096aae009b9e` → `dd564645cc2a7a625ede2d7040c31dfa387ae7155fee82c5ef1355c4a6d846d6`**. `CH31_PGURL` 정의 뒤에 설명 주석 셋 + `case ":$PATH:" in *":$CH31_PGBIN:"*) ;; *) export PATH="$PATH:$CH31_PGBIN" ;; esac` 한 줄(두 번 source해도 한 번만 더함 — 확인).
- **PATH 앞이 아니라 끝에 더함(챕터 리드 결정은 「앞에 더해도 됨」)**: pgenv `bin`에 명령 107개가 있고 그 가운데 `openssl`·`clear`·`tput`·`zstd` 등이 시스템 명령을 가림 → 끝에 두면 시스템에 없는 `pg_dump`·`pg_restore`·`psql` 등만 채움. 이 기기 시스템에는 `pg_dump`가 없음(`command -v` 빈 값 — 04 확인, 다시 확인). 훅을 부른 셸에서 `command -v openssl` → `/usr/bin/openssl`(가리지 않음), `uv run` 가상환경 파이썬의 `shutil.which('pg_dump') is not None` → `True`.
- **01~04 영향**: 01~04 노트북의 코드·출력에 `PATH` 0건(`grep`) · 03 Alembic은 파이썬 API(PATH에 기대지 않음) · 01~04는 다시 실행하지 않음 · 01~04 진단의 훅 해시 `8a9529f1…`는 01~04 때의 값(바뀐 값은 이 진단·`manifest-changes.md`에).

## 문서 대조 (WebFetch 2026-09-29)

- pgvector README **v0.8.1**(설치 확장 0.8.1과 같음) — HNSW 「creates a multilayer graph」 · `<=>` cosine distance · `vector_cosine_ops` · Troubleshooting 「if the table is small, a table scan may be faster」·`SET LOCAL enable_seqscan = off`.
- PostgreSQL 17 pg_dump — `-n` 「makes no attempt to dump any other database objects that the selected schema(s) might depend upon … no guarantee that the results of a specific-schema dump can be successfully restored by themselves into a clean database」 · `custom` 「suitable for input into pg_restore」 · 「cannot dump from PostgreSQL servers newer than its own major version」.
- PostgreSQL 17 pg_restore(문서 17.11) — 파일 없으면 표준 입력 · `--exit-on-error` 「The default is to continue and to display a count of errors」 · `--list` · `--single-transaction` 「either all the commands complete successfully, or no changes are applied」.
- PostgreSQL 17 EXPLAIN(`COSTS` 기본 TRUE·계획은 표를 어떻게 읽는지) · Planner Method Configuration(`enable_seqscan` — 「crude method」·「temporary solution」) · CREATE DATABASE(「cannot be executed inside a transaction block」) · DROP DATABASE(「if anyone else is connected … will fail unless … FORCE」·`IF EXISTS`) · libpq Environment Variables(`PGPASSWORD` 「not recommended for security reasons … consider using a password file」).
- LangGraph Memory(`setup()` 처음 한 번·`from_conn_string`·`AsyncPostgresSaver`) · PyPI langgraph-checkpoint-postgres **3.1.2**(설치 3.0.5) — 연결을 직접 만들면 `autocommit=True`·`row_factory=dict_row` · psycopg async(문서 **3.3.7.dev1**, 설치 3.3.3) — 「On Windows, Psycopg is not compatible with the default ProactorEventLoop」 · Docker Hub postgres — 「sets up trust authentication locally … inside the same container」.
- 설치판 소스(langgraph-checkpoint-postgres 3.0.5 — `.cache/vm/venv-ch31-database`): `langgraph/checkpoint/postgres/__init__.py` 56~75행(`from_conn_string` — `autocommit=True, prepare_threshold=0, row_factory=dict_row`)·77~102행(`setup()` — `MIGRATIONS[0]` 뒤 판 번호를 기록 표에) · `base.py` 37~85행(`MIGRATIONS` 열 문장 — 표 넷·색인 셋). 문서와 설치판 출력이 어긋난 곳은 찾지 못함.

## 실행 (새 커널)

- **노트북 밖 확인**(`/tmp/ch31-05/exp/`, 가상환경 파이썬 · 훅으로 켠 서버): `e1_scene.py`(첫 설계, `pg_restore --no-owner`) 5/5 같음(목차 원문 줄 뺀 stdout sha256 앞 16자리 `040b9a8165498278`, 원문 줄 포함은 5번 모두 다름 — OID) · `e3_scene.py`(노트북과 같은 인자) **5/5 같음 `a10ce6dbc04c5c4a`**, stderr 0바이트 · `e2_public.py`(따로 만든 DB `ch31_probe05`에서 `search_path` 없이 `setup()` → 표 넷 모두 `public`, 끝에서 DB 지움 → 남은 0).
- 첫 실행 전 `/tmp/ch31-05/try/copy1.ipynb` 사본을 `runcopy.sh`(훅 source + `execute.py --cwd` 프로젝트 맨 위)로 PASS 31셀 — 오류 수 5를 여기서 보고 설명 글을 고침. 실습 폴더에 `.failure.json` 0.
- **A**: `env -u OPENAI_API_KEY PYTHONDONTWRITEBYTECODE=1 timeout 170 bash run_section.sh textbook/part7/ch31-database 05` — 프로젝트 맨 위 커널, **`executed_at` 2026-09-29T19:32:40Z**, PASS 31셀(그림 첨부 단계에서 멈춤 — 05-1 PNG가 아직 없어서, 실행·저장은 끝난 뒤) · `code_sha256` **`6269536315f374f65e1e859232ac9f21a07e56b8798a3064eacec17f2857a4ac`** · `outputs_sha256` **`8bac96cd5e64e0f1d40a8c19885363fdf47b51c02d16bc18f2b1a93baa3e6e39`**.
- **B**(그림 전): 저장 노트북 사본 `/tmp/ch31-05/runB/05B.ipynb`를 `--cwd labs/part7/ch31-database/notebooks`(학생 커널 자리) · `executed_at` 19:32:50Z · PASS 31셀 · `code_sha256` 같음 · `outputs_sha256` `930cc17a…`(다름 — **설치 셀의 stdout 조각 나눔만 다름**: A `1+3`자 조각 ↔ B `4`자 한 조각, 글자는 같음, 03 선례).
- **셀별 출력 글자 대조(`cmpout.py`): A·B 31개 모두 같음**, 사본 시험(copy1)과 A도 31개 모두 같음·`outputs_sha256` 같음 → 같은 서버에서 세 번 연달아 실행해도 같은 출력(다시 실행해도 같음). 흔들리는 값 없음 → 결과 읽기에 `[[…]]` 자리 없음. 모든 셀 stderr 0.
- 설명만 고친 뒤(`mdpatch.py` — G5 다섯) 저장 노트북과 A 셀별 31개·`outputs_sha256`·`code_sha256`·`executed_at` 같음 · 생성기 `cells()` 65셀과 저장 노트북 셀 소스 65개 모두 같음 · `src_html()`과 `_src` 같음.
- 한 셸 호출 시간: 사본 3초 안팎·A 약 10초(설치 셀 포함) — 180초 제한과 멂.
- 모든 셸 호출 뒤 postgres 프로세스 0·55431 포트 0. 끝의 서버 상태: 이름 공간 `public`만 · 확장 `plpgsql`·**`vector 0.8.1`(`public` — 노트북이 남김)** · 데이터베이스 `ch31_lab`·`postgres`(`ch31_restore`·`ch31_probe05` 없음) · `public` 표 0.
- 실습 폴더 파일 고침 **0**: `app/`·`migrations/`(맥 pyc 포함)·`alembic.ini`·README·`pyproject.toml`·`uv.lock` 17개 sha256을 03의 기록 `/tmp/ch31-03/lab-before.sha`와 대조 — 17/17 같음 · 실습 폴더에서 바뀐 파일은 노트북 05뿐.

## 고친 틀린 사실

1. 백업·복원이 Docker 안에서만 되던 것 → 이 컴퓨터의 `pg_dump`를 먼저 찾고 없으면 컨테이너 안 명령(두 갈래 같은 셀) · 교재 출력은 이 컴퓨터 쪽만 실행했다고 한정.
2. 「확장을 만든 뒤 복원」의 까닭이 없던 것 → 덤프 목차에 확장 없음(`False`) + 확장 없이 복원하면 문서 표만 빠지고 종료 코드 1(실행 1)로 보임.
3. `EXPLAIN ANALYZE` 시간 줄(흔들림)·「uses hnsw: False」만 → `COSTS OFF` 계획 줄(매번 같음) + 복원 DB에서 `enable_seqscan` off일 때 색인 스캔.
4. 「체크포인터」를 새 용어로 셈 → Ch 23 01 말로 잇고 새 용어는 백업·복원·덤프 파일 셋.
5. b6 「Docker PostgreSQL 17.8」 → 교재 출력 17.11(Docker 없이 같은 접속 글) · b7 「Ch11 평가셋으로 측정」·b8 「Ch32 Compose·헬스체크·시크릿」(실행·확인 안 함) → 뺌.
6. 옛 그림의 보라·빨강(모델·실패 아닌 요소) → 보라 0·빨강 0(experiment).

## 그림

- Mermaid **4장**(설계표 `05-figures.md`를 렌더 전에 씀): 05-1 한 이름 공간에 두 가지 표(b4·노트북 오늘 볼 그림, viewBox 폭 **721**) · 05-2 백업 명령 자리와 덤프 파일(b5, **468**) · 05-3 확장 없이 복원한 실행 1(b6, **255**) · 05-4 확장 만들기 하나를 바꾼 두 실행(b6, **606**). 모두 868 이하 · `flowchart TB` · 갈래는 점선(05-2) · subgraph 제목 `<br>` 없음 · 라벨 대괄호·따옴표·중괄호 없음 · 개수는 한글 · 노드 7개 이하 · 노드 id `call`·`end` 없음 · `%% classes`. **첫 렌더에서 자동 줄바꿈 다섯**(`documents_embedding_hnsw` 둘·Docker 갈래 상자·목차 상자·`errors ignored on restore: 5`) → `<br>`로 미리 나눠 다시 렌더 · PNG 넷을 다른 이름 사본(`.cache/ch31-05-view/r1-*`·`r2-*`)으로 직접 열어 확인(05-4는 실행 1 칸이 왼쪽). **보라 0 · 빨강 0**(받아 출력한 `pg_restore` 오류·빠진 문서 표도 노랑) · 05-2 Docker 갈래는 실행하지 않아 회색 · 05-4 맨 아래 노랑 공통 상자는 두 칸 출력에서 모두 확인한 값만(`checkpoints` 줄 셋·`value 12`), 계획 줄은 실행 2 칸에만.
- 삽화 1장 **05-5 자리를 단 판과 달지 않은 판**(b4 비유 뒤, 본문만): **1차 job `b542e23e-c519-4e0c-b72d-d5bc0e1d73e4` 채택**(재생성 0회). 거래 2026-09-29T19:35:55.970604Z 「Nano Banana Pro −2」 한 줄 = **이 절 몫 2크레딧**(잔액 2251 → 2249, 바로 앞 거래 18:56:18Z는 04). 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만). 원본 2752 × 1536 `d40b1da8…` · 저장 PNG 1100 × 614 `5ee9db5b…`, 결과를 다시 받아 같은 폭으로 줄인 그림과 **픽셀 차이 0**(bbox `None`). 그림에서 센 것: 옅은 회색 금속 판 둘 · 왼쪽 구리색 자리 넷 + 구멍 없는 자리 하나 · 짙은 회색 선 넷 꽂힘 · 노란 초록 선 하나 턱 위에 누움 · 오른쪽 구리색 자리 다섯 · 짙은 회색 선 넷 + 노란 초록 선 하나 꽂힘 · 선 모두 열 · 불·사람·손·글자·숫자·화살표·콘센트·전원 플러그 0. 거의 흰 가로줄 0/614. 세부 `figures/05-5-…prompt.md`.

## 검사

- 게이트 G1~G7 0(`gates-wip-05.json`, 검사 문장 509) · `verify.py --chapter` **PASS 5 sections / 127 code cells (max 14 lines)**(옛 05의 25줄 셀이 없어져 최대가 14 — 01~04 준비 셀) · 빌드 HTML `05-pgvector-체크포인터-공존과-백업.html`의 `{{`·`[[` 0, `_src`의 `[[` 0(`{{`는 토큰 여섯뿐) · review-pack `qa/upgrade/review-pack/05-pgvector-체크포인터-공존과-백업.md`.
- 화면 검사 `visual.cjs`는 돌리지 않음(마감 몫).

## 완료 챕터·앞 절·뒤 챕터 문장 참·거짓 (고치지 않음)

- **04 노트북 정리 끝·b8** 「05절에서는 같은 PostgreSQL 서버에 검색 문서 표와 체크포인터 표를 함께 두고, 백업과 복원을 해 봅니다」 — **참**(같은 서버 `ch31_lab`의 한 이름 공간에 둘, `pg_dump`·`pg_restore`).
- **03 b7** 「값을 따로 남겨 두려면 판을 내리기 전에 데이터베이스를 파일로 남겨야 하고, 그 방법은 05절에서 봅니다」 — **참**(덤프 파일로 남김 — 표 구조의 판 내리기와 함께 쓰는 장면은 05에 없음, 「파일로 남기는 방법」까지만).
- **01 설정 셀** — 05는 드라이버 부분만 다름(생성기 대조, 「글자까지 같다」 안 씀).
- **Ch 30 10 b8**(`_src`·HTML·노트북) 「Ch 31에서는 PostgreSQL 데이터베이스에 표를 만들어 쓰는 방법과 체크포인터를 다룹니다」·「Ch 31 05절은 체크포인터로 그래프의 실행 상태를 PostgreSQL 표에 저장합니다」 — **참**(4절 `PostgresSaver`·`setup()`·`invoke` → 표 `checkpoints` 3줄·`{'value': 12}`) · 「이 챕터의 실습 앱에 붙이는 일은 다루지 않습니다」·「보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다」 — **참**(Ch 30 앱·SSE 0). **Ch 30 06 b7** SSE — 참.
- **Ch 32 04 b3**(대기) 「Ch31에서는 PostgreSQL, 트랜잭션, 인덱스와 pgvector를 배웁니다」 — **참**(02 한 묶음 작업·05 HNSW 색인·pgvector — 말은 「색인」) · 같은 b3 「Ch12에서 사용한 벡터 검색 개념은 vector(3) 열과 HNSW 인덱스로 다시 나타납니다」 — 05도 `vector(3)`·HNSW(이음 자연스러움).
- **Ch 23 §15 211행** 「05 새 용어 체크포인터」 — 고침(새 용어로 세지 않고 Ch 23 01 말로 이음). **Ch 23 02** `SET search_path`·`PostgresSaver(conn)`·표 넷·기록 10줄 — 05가 같은 모양·같은 값.
- **Ch 12 02** HNSW·`<=>`·`vector_cosine_ops`·`EXPLAIN`·`enable_seqscan` off → `Index Scan` — 05가 이어 씀(컨테이너·포트·계정 다름을 b3 한 문장).
- `grep -rn 'Ch *31'`(Part 1·2·3·5·6·7 HTML, ch31 밖): Part 7 목차 둘·Ch 30 06·10·Ch 32 04와 옛 판 사본(`before/`)뿐. `labs/part7/continuity-guide.md` 8~10행(체크포인트 저장·인덱스)은 마감 대조.

## 챕터 밖 수정

- 없음. (공용 도구·Part 7 파일·다른 챕터 파일 0. `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json`은 `verify.py --chapter`가 다시 쓴 챕터 계약 파일.) 훅 `pre_exec.sh`는 챕터 안 파일.
- 실습 폴더 파일(`app/`·`migrations/`·`alembic.ini`·`README.md`·`pyproject.toml`·`uv.lock`) 고침 0.

## 강사 확인 대상

1. **실험 변수**: 준비 노트 후보 `enable_seqscan` 대신 「복원 전에 확장 만들기」(Ch 12 02 실행 3과 겹치지 않게) — 색인 계획은 3절·9절에서 설정으로만.
2. **백업 명령 두 갈래**: 이 컴퓨터에 `pg_dump`가 있으면 그것을 씀 — 학생 컴퓨터의 `pg_dump`가 16 이하이면 5절이 실패(b7에 알림, 우회는 PATH에서 빼거나 컨테이너 쪽). Docker 쪽 갈래(`docker exec -i … pg_restore`에 표준 입력으로 파일 보내기)는 교재 출력에서 실행하지 않음 — **학생 컨테이너에서 한 번 확인 필요**.
3. 연습용 비밀번호를 `PGPASSWORD` 환경 변수로 넘김(문서는 권하지 않음 — b7에 비밀번호 파일 권고).
4. 노트북이 `ch31_lab`에 확장 `vector`를 남김(10절에 밝힘) · 덤프 파일을 운영체제 임시 폴더에 남김.
5. 말: 제목의 「pgvector」·「체크포인터」·「공존」은 제목에 두고 1절·b2에서 풂 · 새 용어 백업·복원·덤프 파일 · 「노드」(Ch 13 말 — 금지어 목록의 거짓 양성으로 둠).
6. 코드 양: 코드 셀 7 → 31, 코드 줄 94 → 178(experiment 한 절 — 공존·백업·두 복원·정리, 함수 다섯).
7. 훅 `pre_exec.sh`를 고침(PATH 끝에 pgenv `bin`) — 다섯 절 공통 파일.

## 남은 것 (마감 몫)

- 옛 그림 `figures/05-흐름.{svg,excalidraw,caption.md}` 삭제 승인 목록(본문은 더 쓰지 않음 — 캡션에 「스키마」) · README의 05 설명(`docker exec` 명령·`.env`) 다시 쓰기 · `chapter.json` `objectives` 셋째 줄 「논리 백업 범위」 대조 · `labs/part7/continuity-guide.md` 대조.
- 06 실습 절(다른 작업자) — handoff 「§05 → 실습 절」.

## 지우지 않은 것 (삭제 승인 대상 — 이 절이 만든 것)

- 기기 `/tmp/ch31-05/`(약 8.2MB — `exp/`(`e1_scene.py`·`e2_public.py`·`e3_scene.py`와 출력 `e1_0~5`·`e2.out`·`e3_1~5`)·`tools/`(04 도구 사본 열셋 + `edit.py`·`runcopy.sh.bak`)·`gen/`(생성기 조각 넷·`all.py`·치환 스크립트와 JSON `r1`~`r9`)·`pre/`(pregate 임시 노트북·`src.html`)·`try/copy1.ipynb`·`runA/`·`runB/`·`illu/`(`r1.png` 원본·`r1-again.png`·`r1-1100.png`)) · 연결 폴더 `.cache/ch31-05-view/`(PNG 아홉 — 첫 렌더 넷·다시 렌더 넷·삽화 하나, 약 1.4MB) · `qa/upgrade/gates-wip-05-05.json`·`gates-wip-05.json`.
- **운영체제 임시 폴더의 덤프 파일**: 기기 셸의 `TMPDIR`(`/sessions/…/tmp`)에 `ch31-05-*` 폴더 **14개**(각각 `ch31_shared.dump` 하나 — 노트북 밖 `e1` 6번·`e3` 5번 + 사본 시험·A·B, 합 224K). 노트북·확인 스크립트가 지우지 않음(설계대로 — 03의 `ch31-03-*` 사본 폴더와 같은 자리).
- 서버에 남긴 것: `ch31_lab`의 확장 `vector`(노트북 설계 — 다시 실행에 영향 없음).
- 앞 절이 남긴 `/tmp/ch31-02/`·`/tmp/ch31-03/`·`/tmp/ch31-04/`·`.cache/ch31-0[1234]*`, 공용 `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/libs`·`/tmp/npm-cache`·`/tmp/uv-cache`·`/tmp/ch31-pg/`는 건드리지 않음.

## 디스크

- 기기 루트 여유: 작업 전 **2.0G**(첫 `df`) → 끝 **1.9G**(`/tmp/ch31-05` 8.2MB) · 세션 디스크(`/sessions`, `TMPDIR`) 831M(덤프 폴더 224K) · 사용자 디스크(연결 폴더) 여유 74G → 74G(이 절이 연결 폴더에 더한 것은 3MB 남짓).

## 보호 파일 (`before-manifest.json` 209개)

- 05절 뒤 대조 결과는 `manifest-changes.md` 「05절 뒤」.
