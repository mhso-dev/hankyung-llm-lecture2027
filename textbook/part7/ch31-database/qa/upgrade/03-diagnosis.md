# 03절 진단 — Alembic 적용과 롤백 (paired)

- 작업일 2026-09-29 · 생성기 `qa/upgrade/author_03.py`(`c7946dcf…`) · 노트북 `labs/part7/ch31-database/notebooks/03-Alembic-적용과-롤백.ipynb` · 본문 `_src/03-Alembic-적용과-롤백.html` · 슬러그 그대로 · DB 준비 훅 `qa/upgrade/pre_exec.sh`(01이 만든 판 `8a9529f1…` 그대로 씀).
- 읽은 것: `handoff.md`(챕터 공통·§02 → §03 전부) · 준비 노트 `chapter-lead-notes.md`(§0·§1·§2 03·§3·§5·§6·§7) · `02-diagnosis.md` · 본 생성기 `author_02.py`(전부)·`author_01.py`(`SETTINGS`)·Ch 30 `author_01.py`(`FIND_LAB`·묶음 계약 결정) · `AGENT-BRIEF.md`·`PLAYBOOK.md` · 규격 `QUALITY-UPGRADE.md`(전부) · 과정 요약(Ch 21·Ch 23·Ch 30 줄, 「처음 쓰면 한 문장」 표) · 계약 파일 Ch 30 → Ch 31 줄 · Ch 23 02 `_src`(표 만들기 기록·판 번호) · Ch 21 04 `_src`·요약(옮기기) · Ch 28 03 용어 표(환경 변수) · 옛 판 노트북·`_src` · 실습 폴더 `alembic.ini`·`migrations/env.py`·첫 판 파일·`script.py.mako` · Part 7 `check_bundle_execution.py`. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전(`gates-before.json`) | 6 | 82 | 3 | 0 | 4 | 0 | 8 | 17 | 3 | 35 |
| 첫 실행 전(`gates-wip-03-03.json`, G1·G2 먼저) | 31 | — | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 3(그림 없음) |
| 첫 `--no-exec`(그림 뒤) | 31 | 457 | 0 | 0 | 0 | 0 | 3 | 1 | 0 | 4 |
| 후(`gates-wip-03.json`, `--no-exec`) | **31** | **457** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

- 첫 `--no-exec`의 넷: G5 셋 = 결과 읽기 첫 단락의 숫자 든 인용이 그 셀 출력에 없음(`ch31_migration`·`20260911_01`·`20260929_02` — 출력이 생긴 뒤에야 잡힘) · G6 하나 = b7 70자 넘는 문장. `mdpatch.py`로 생성기·노트북·`_src`를 함께 고침(재실행 없이 — 모델 없음, 출력 그대로).
- AST 따로(`/tmp/ch31-03/tools/extra_check.py` — 01·02 판 그대로): 걸린 것은 `try` 하나(함수 `try_upgrade`의 `except IntegrityError as error` — Ch 2 05·02절 모양). 호출 깊이 최대 2 · 준비 셀 밖 셀 최대 10줄(판 파일 글 셀) · 함수 본문 `show_state` 7줄·`try_upgrade` 5줄 · 코드 줄 135(주석·빈 줄 뺌, 옛 판 42) · 클래스·데코레이터·힌트·`async`·`await`·f-string·내포식·`sorted`·`next`·세미콜론 0. **거짓 양성 하나**: 도구가 판 파일 글 셀(`before_text`)을 「`def` 둘」로 셈 — 정규식 `^def `가 문자열 안의 `def upgrade():`·`def downgrade():`를 잡은 것(게이트 G1은 AST라 0).
- **판 파일 글(노트북이 문자열로 사본에 쓰는 파이썬 글)도 과정 문법 안**: `from alembic import op`·`import sqlalchemy as sa`·변수 둘·`def upgrade():`·`def downgrade():`(힌트 없음)·`owner = sa.Column("owner", sa.String(length=50), nullable=False)`(깊이 2 — `op.add_column(…, sa.Column(…, sa.String(…)))` 세 겹을 피하려고 변수로 나눔)·`op.add_column`·`op.drop_column`. 실습 폴더 첫 판 파일의 반환 힌트 `-> None`·`branch_labels`·`depends_on`·설명 글은 넣지 않음(Alembic은 `getattr(module, "branch_labels", None)`으로 읽어 없어도 됨 — 설치판 `script/base.py` 813~817행).
- 금지어(`/tmp/ch31-03/tools/ban33.py` = 02 `ban32.py`에서 「마이그레이션」도 빼고, 「마이그레이션」·「롤백」·「리비전」·「스키마」·「되돌」·「옮기」는 `twoword33.py`로 자리를 모두 봄): `_src`·노트북 마크다운·코드 주석·`.mmd` 다섯·캡션 여섯 모두 0(「로그」 한 건은 「프로그램」 거짓 양성). 「마이그레이션」은 괄호 원어 둘(「표 구조 바꾸기(마이그레이션, migration)」·「옮기기(마이그레이션)」)만, 「롤백」은 절 제목·제목 풀이(「제목의 롤백은」)·02 괄호 원어(「취소(롤백)」)만, 「리비전」은 괄호 원어 하나만, 「스키마」·「되돌」 0, 「옮기」는 Ch 21 인용 하나만. 복습 5번의 「둘 다 롤백이니」(동료 말 인용)는 「영어 이름이 같으니」로 고침. 사용자 금지 표현 0.
- 인용 대조(`quotes.py`): 노트북 백틱 122개·`_src` `<code>` 64개 가운데 출력·코드에 없는 것은 명령·파일·API·설정 글 이름뿐(`docker start kdt-ch31-postgres`·`uv sync --locked`·`alembic upgrade head`·`script_location = %(here)s/migrations`(실습 폴더 `alembic.ini` 2행 그대로)·`requests`(01 표 이름)·설치판 소스 파일 이름·`{id,question}`(첫 시험 실행 출력 — b7) 등).

## 수정 전 주요 문제 (옛 판 — `before/notebooks/03-…ipynb`·`before/_src/03-*.html`)

1. **Before가 실제 결함이 아님** — `downgrade base` 뒤 `to_regclass` → `None`은 판 내리기가 명령대로 한 것(규격 §3). After도 같은 판을 다시 올린 것뿐(고친 것 없음).
2. **`subprocess.run(["alembic", …])`** — 커널의 PATH에 가상환경 `bin`이 있어야 돎(준비 노트 §2 — 이 기기에서 `shutil.which('alembic')` = `None`) · 자식 프로세스에 `PYTHONDONTWRITEBYTECODE`를 넘기지 않아 실습 폴더 `migrations/__pycache__`에 pyc가 생길 수 있음.
3. 문법: `candidates = [… for parent in (Path.cwd(), *Path.cwd().parents)]` 내포식·별표 풀기 · `next(path for …)` 제너레이터 식 · `def alembic(*args: str) -> str` · `os.environ | {…}` 딕셔너리 합치기 · `import os, subprocess` 한 줄 · `.splitlines()[-1]` 사슬 · `fetchone()[0]` · 첫 줄 주석 0 · 결과 읽기 0 · 준비 셀 `%pip` 세 줄(이 절이 쓰지 않는 asyncpg·pgvector·langgraph 설치) · `os.getenv` 주소 셋(`localhost`).
4. 말: 「리비전」 16·「롤백」 9·「마이그레이션」 7·「스키마」 6·「되돌」 1 · 비유 「도면」 · 제목 셀 「운영 데이터베이스의 한 가지 문제를 재현하고 해결합니다」(다섯 절 틀 문장) · 「이 준비 셀이 하는 일」 틀 단락 · 「확장-이행-축소」·「백업 복구 시간을 측정」(실행 안 함).
5. b4·b7·복습 3의 자동 생성(`revision --autogenerate`) 설명 — `env.py`에 `target_metadata`가 없어 실행한 적 없음 · `alembic check` 종료 255 · b6 「Docker의 독립 PostgreSQL 17.8 컨테이너 … 시간과 실행 계획」(이 절은 시간·계획을 재지 않음) · b10 확인 2026-09-11·「확인 필요 항목」 틀.
6. 첫 판 파일 설명 글 「상담 티켓 표 구조를 변경합니다」(실제로는 표를 만듦) — Alembic 진행 기록에 찍힘. **실습 폴더 파일이라 고치지 않고**, 노트북 5절 결과 읽기에 「설명 글은 표 구조를 바꾼다고 적었지만, 이 판은 표 tickets를 새로 만듭니다」로 바로잡음.
7. 그림: `{{svg:03-흐름}}` 한 장(틀 문장 「푸른·붉은·초록·보라」), Mermaid·삽화 0.

## 바꾼 것

- **paired 설계(handoff §02 → §03 2 ① 권장안)**: 실습 폴더 `alembic.ini`·`migrations/`를 `tempfile.mkdtemp(prefix="ch31-03-")` 사본에 복사(`shutil.ignore_patterns("__pycache__")` — 맥 pyc를 가져오지 않음) → `Config(사본 ini)`(`%(here)s`가 사본 — 출력 `판 파일 폴더가 사본 안인가: True`, 사본 위치는 출력하지 않음) → 첫 판 `20260911_01`(실습 폴더 판 파일 그대로) → 표 `tickets(id, question)`에 01 문의 글과 같은 세 줄. **Before** = 노트북이 사본 `versions/`에 쓴 판 `20260929_02`(`owner VARCHAR(50)`, `nullable=False`, 기본값 없음) → `try_upgrade()`가 **`IntegrityError`**(`error.orig` = `psycopg.errors.NotNullViolation`, `sqlstate` `23502`, `statement` `ALTER TABLE ch31_migration.tickets ADD COLUMN owner VARCHAR(50) NOT NULL`, 글 `column "owner" of relation "tickets" contains null values`)를 내놓음(받은 오류 노랑) → **`판 번호: 20260911_01`·`칸: ['id', 'question']` 그대로**(받은 결함 결과 — 빨강). **After** = 같은 파일에 `server_default="미정"`만 더해 고쳐 씀(`replace` 한 곳) → `받은 오류: None`·`판 번호: 20260929_02`·세 줄 `'미정'`. **판 내리기** = 1번 줄 `'민지'` → `command.downgrade(…, "-1")` → 칸 둘·줄 셋 → 다시 올리기 → 1번 줄 `'미정'`(판 내리기에서 없어진 값). **값 바꿔 보기** = Before 글의 `nullable=False`만 `True` → `20260929_02`·세 줄 `None`.
- 판 번호 `20260929_02`는 노트북이 정한 글(출력이 매번 같게 — 명령 `alembic revision`의 자동 번호는 `uuid4().hex[-12:]`, 설치판 `util/langhelpers.py` 232~233행 — 실행하지 않음, b7). 둘째 판 파일 이름 `20260929_02_add_owner.py`.
- **Alembic은 파이썬 함수**(`alembic.command.upgrade`·`downgrade`, 같은 프로세스) — PATH·자식 프로세스·`PYTHONDONTWRITEBYTECODE` 넘기기 없음(handoff §02 → §03 4). Alembic이 가져오는 `env.py`·판 파일은 사본 것이라 pyc가 생겨도 사본에만 생김(이번 실행들은 `PYTHONDONTWRITEBYTECODE=1`이라 사본에도 0).
- **`env.py` 함정 처리(handoff §02 → §03 5)**: 노트북 3절이 실습 폴더 `env.py` 12~15행을 **비밀번호 자리만 `(비밀번호)`로 가려** 출력(`os.getenv("CH31_SYNC_URL", "postgresql+psycopg://postgres:(비밀번호)@localhost:55431/ch31_lab")`) → 「`alembic.ini`나 설정 객체에 무엇을 적든 접속 글을 새로 정합니다」 → `os.environ["CH31_SYNC_URL"] = database_url`(값은 출력하지 않고 같은지만 `True`). `os.environ`은 「처음 쓰면 한 문장」(과정 요약 §2) — Ch 28 03 환경 변수 풀이로 이음. **`env.py`·`alembic.ini`는 고치지 않음**(README·묶음 영향 없음).
- 접속 글: 설정 셀 = **`author_01.SETTINGS`에서 `asyncpg` → `psycopg` 한 곳만 다름**(`__main__`에서 `SETTINGS.replace("psycopg", "asyncpg") in author_01.py` 대조 — 「드라이버 이름 … 한 곳만 다릅니다」 문장의 근거). 「글자까지 같다」는 쓰지 않음.
- **파일 위치 셀** = Ch 30 01 `FIND_LAB`에서 후보 이름(`labs/part7/ch31-database`)·찾을 파일(`/alembic.ini`)만 다름(`__main__`에서 문자열 대조). 루트 커널(A)·`notebooks/`(B)·묶음을 푼 `notebooks/` 세 자리에서 `실습 폴더를 찾았는가: True`.
- **출력 차례(결정 3)**: Alembic 진행 기록은 `env.py`의 `fileConfig`로 stderr에 찍힘. ipykernel `OutStream`은 흐름마다 0.2초 타이머로 내보내(설치된 ipykernel 7.3.0 `iostream.py` 446·658~669행), stdout과 한 셀에 섞이면 셀 안 차례가 실행마다 바뀔 수 있음 → **판을 올리고 내리는 셀은 print 없이 기록만**, 결과는 다음 셀. 받은 오류는 함수 `try_upgrade`가 내놓음(except 블록 밖에서 이름 `error`가 지워지는 문제도 피함). 노트북 결과 읽기·b7에 「오류 출력(stderr) 쪽 — 편집기에 따라 바탕색이 다름, 오류 아님」.
- 진행 기록 `Will assume transactional DDL.`을 02의 한 묶음 작업·원자성과 잇는 근거로 씀(설치판 `runtime/migration.py` 211~218행·`ddl/postgresql.py` 84행 `transactional_ddl = True`) · `Running upgrade …`는 판 함수를 부르기 **전에** 찍힘(620~632행) → Before·After 모두 같은 기록이라 「기록만으로는 끝났는지 가를 수 없다」(7절).
- 칸 목록 SQL: `array_agg(column_name::text ORDER BY ordinal_position)`. **첫 사본 시험(copy1)에서 `::text` 없이 `칸: {id,question}`(글 하나)**이 나와 — `information_schema.columns.column_name`의 자료형이 `information_schema.sql_identifier`(`pg_typeof`)라 psycopg가 배열로 읽지 않음 — `::text`를 더함(b7에 밝힘).
- **말(handoff 「뒤 절이 정할 말」 03 권장 그대로)**: 마이그레이션 → **「표 구조 바꾸기(마이그레이션, migration)」**(뜻 → 출석부 칸 긋기 예 → 표 `tickets`에 `owner`) · 리비전 → **「판(리비전, revision)」**(개정판 예·앞 판 번호 `down_revision`) · `upgrade`/`downgrade` → **「판 올리기(upgrade)·판 내리기(downgrade)」**(계단 예) · 제목의 롤백 = 판 내리기, **02 취소(롤백)와 다른 뜻**(노트북 1절·8절·b2·b4 소제목 「이 절의 판 내리기와 02절의 취소」·복습 5) · **Ch 21 04 옮기기(마이그레이션) = 옛 버전 라이브러리 코드를 새 버전에 맞춰 고치는 일, 뜻이 다름**(노트북 2절·b3) · 판 사슬·판 기록 표(`alembic_version` — Ch 23 02 「표 만들기 기록」 판 번호와 같은 생각)는 풀이만 · NOT NULL 제약(Ch 4 03 제약 이음)·서버 기본값·`os.environ`·`tempfile`·`shutil`·`information_schema.columns`·`array_agg`·`::text`·`SELECT *`는 한 문장씩. 새 용어 meta **3**(옛 4). **이 절에서 「판」은 표 구조의 판만** — 패키지·서버는 「버전」(제목 셀·b4에 한 문장, 01·02의 「판은 sqlalchemy …」 모양을 이 절만 「버전은 …」으로).
- 동기 엔진 `create_engine`(01 `create_async_engine`과 같은 일, `with`·`await` 없음 — 한 문장) · 이름 공간 `ch31_migration`: 4절 `DROP SCHEMA IF EXISTS … CASCADE`·`to_regnamespace` → `None`, 10절 `DROP SCHEMA … CASCADE`(판 기록 표까지) → `None`·`engine.dispose()` · 임시 폴더 사본은 Ch 23처럼 지우지 않고 둠(노트북 10절 한 문장). 두 번 실행해도 같은 출력(사본 시험 둘·A·B·묶음 — 다섯 실행 모두 같은 서버에서 이어 실행, 셀별 출력 같음).
- 설치 셀은 이 절이 쓰는 셋만: `sqlalchemy==2.0.43`·`psycopg[binary]==3.3.3`·`alembic==1.16.5`(출력 `sqlalchemy: 2.0.43`·`psycopg: 3.3.3`·`alembic: 1.16.5` — 잠금 판; 잠금 extras는 `[binary,pool]`, 이 절은 pool을 쓰지 않아 `[binary]`만 적음). `%pip` 셀을 새로 넣은 것이 아니라 줄을 줄인 것이라 잠금·dev `pip`은 건드리지 않음.
- 비유 계열 「전화 교환대」 이어 씀: 가로 줄 = 표의 줄, 세로 줄 = 칸, 빈 자리 셋짜리 새 판 = 기본값 없는 새 칸(붙지 못함 = Before), 회색 마개 = 서버 기본값(After), 「모든 자리에 무언가 꽂혀 있어야 한다」 = NOT NULL. b4 「비유와 다른 점」(실제로는 한 묶음 작업이 취소되어 붙이다 만 판도 남지 않음).
- 도구 파일: **가져오지 않음**(묶음 계약 · 챕터 공통 8 S1) — 이 절의 함수 둘(`show_state`·`try_upgrade`)은 전역 `engine`·SQL 글 셋·`alembic_cfg`에 기대는 이 절 전용.

## 설치판 동작 확인 (모델 없이 — `/tmp/ch31-03/exp/`, 가상환경 `.cache/vm/venv-ch31-database`)

- `e1_scene.py`(노트북 장면을 같은 프로세스 API로, **5번**): stdout sha256 앞 16자리 다섯 번 모두 `52c40e17025221e2`, stderr 다섯 번 모두 `c959c8dbfd948b09` — 첫 판 `20260911_01`·칸 둘 · Before `IntegrityError`(MRO `IntegrityError → DatabaseError → DBAPIError → StatementError → SQLAlchemyError`)·`psycopg.errors.NotNullViolation`·`23502`·`statement`·`diag.column_name` `owner` → 판·칸 그대로 · After `20260929_02`·`'미정'` 셋 · `UPDATE` 민지 → `downgrade -1` → 칸 둘·줄 셋 → 다시 올리기 → `'미정'` · `command.current` `20260929_02 (head)` · `command.history` 두 줄 · 정리 `None` · 실습 폴더에 새 판 파일 없음 · 사본 `__pycache__` 없음 · **`sys.path` 앞에 `"."`이 명령마다 더해짐**(`prepend_sys_path = .` — 설치판 `script/base.py` 185~187행, 스크립트 끝 7개; 노트북 커널에서도 같을 것 — 커널 안에서만, 이 절의 판 파일은 `app`을 가져오지 않아 결과에 닿지 않음).
- `e3_empty.py`(2번): **빈 표**에 같은 Before 판 → 막히지 않고 `20260929_02`(b7 「줄이 든 표에서만 드러나는 결함」의 근거).
- 사본 시험 copy1: 칸 목록 `{id,question}`(글) → `::text` 더함 → copy2: `['id', 'question']`.
- 설치판 소스(alembic 1.16.5): `config.py` 241~245행(`here` = 설정 파일 폴더) · `script/base.py` 185~187행(`prepend_sys_path`)·813~817행(`branch_labels`·`depends_on`은 `getattr` 기본값) · `runtime/migration.py` 211~218행(진행 기록 둘)·620~632행(`Running …` → 판 함수 → 판 번호 적기) · `runtime/environment.py` 421·494행(`transaction_per_migration` 기본 `False`) · `ddl/postgresql.py` 84행 · `util/langhelpers.py` 232~233행 · `script/revision.py` 48행(판 번호에 `@`·`-`·`+` 금지 — `20260929_02`는 밑줄).
- 문서 대조(WebFetch 2026-09-29 — Alembic 문서는 **1.20 판**, 설치는 1.16.5): Tutorial — 「Alembic first checked if the database had a table called alembic_version, and if not, created it」·`alembic downgrade -1`·`base` / Commands — 「being sent the Config object as the first argument」·`upgrade(…"heads")`·`downgrade(…"base")` / Runtime — `transactional_ddl` 「defaults to whether or not the dialect in use supports it」·`transaction_per_migration` 「rather than the full series」 / Autogenerate — 「modify our env.py so that it gets access to a table metadata object」·「autogenerate is not intended to be perfect」 / Operation Reference — `add_column` 「ALTER TABLE… ADD COLUMN」·`server_default` / PostgreSQL 17 ALTER TABLE Notes — 「That value will be used for the column for all existing rows. If no DEFAULT is specified, NULL is used」 / Constraints 5.5.2 — 「must not assume the null value」 / Error Codes — `23502` `not_null_violation`. 문서와 설치판 출력이 어긋난 곳 없음.

## 실행 (새 커널)

- 첫 실행 전 `/tmp/ch31-03/try/copy1`·`copy2` 사본을 `runcopy.sh`(훅 source + `execute.py --cwd` 프로젝트 맨 위)로 PASS 31셀 — 실습 폴더에 `.failure.json`이 남지 않게.
- **A**: `env -u OPENAI_API_KEY PYTHONDONTWRITEBYTECODE=1 timeout 170 bash run_section.sh textbook/part7/ch31-database 03` — 프로젝트 맨 위 커널, **`executed_at` 2026-09-29T17:09:43Z**, PASS 31셀(그림 첨부 단계에서 멈춤 — 03-1 PNG가 아직 없어서, 실행·저장은 끝난 뒤) · `code_sha256` **`f97cba07f5bc40c161d04a77d7043d5ec1ea17ecd3e716ca2d2455817b04d252`** · `outputs_sha256` `875e6c2e50d4e2aa17243057e5951b2844f3d1f120b08a9a686a7f8e9da7c838`.
- **B**(그림 전): 저장 노트북 사본 `/tmp/ch31-03/runB/03B.ipynb`를 `--cwd labs/part7/ch31-database/notebooks`(학생 커널 자리) · PASS 31셀 · `code_sha256` 같음 · `outputs_sha256` `ddcf90d916da6e7c…`.
- **셀별 출력 글자 대조(`cmpout.py`): 31개 모두 같음.** `outputs_sha256`이 다른 것은 끝 셀 [31]의 stdout 조각 나눔뿐(A 한 조각, B 두 조각 — 이어 붙인 글은 같음). stderr 진행 기록 셀(판을 올리고 내리는 셀 여섯)은 줄마다 조각이고 두 실행에서 같음. 흔들리는 값 없음 → 결과 읽기에 `[[…]]` 자리 없음.
- **묶음 계약(handoff §02 → §03 7)**: `textbook/downloads/part7-practice.zip`(Ch 30 마감 판)을 `/tmp/ch31-03/bundle`에 풀고 03 노트북만 새 판으로 바꿈 → 훅으로 DB를 켠 같은 셸에서 `execute.py --cwd …/part7-practice/labs/part7/ch31-database/notebooks`, **`OPENAI_API_KEY` 없이·`.env` 0** → PASS 31셀, 셀별 31개 같음, **`outputs_sha256` A와 같음**(`875e6c2e…`), 묶음 `migrations/`에 새 파일·pyc 0. 키·모델·도구 파일 없이 DB만으로 돎. 실행기는 이 챕터 `.cache/vm` 가상환경(묶음 검사 스크립트 32행의 실습 폴더 맥 `.venv`는 이 기기에서 못 돎 — 마감 몫) · 묶음 zip 다시 만들기·`bundle-execution.json` 새 `code_sha256`(`f97cba07…`, 지금 기록 `b0594f2d…`는 옛 판)은 **마감 몫**.
- 실습 폴더 파일 고침 **0**: `app/`·`migrations/`(맥 pyc 포함)·`alembic.ini`·README·`pyproject.toml`·`uv.lock` 17개 sha256을 작업 전(`/tmp/ch31-03/lab-before.sha`)과 끝에 대조 — 모두 같음 · 실습 폴더에 새로 생긴 파일은 노트북 03뿐 · pyc 0 · `.failure.json` 0 · 모든 셸 호출 뒤 postgres 프로세스 0·55431 포트 0.

## 고친 틀린 사실

1. Before 「downgrade 뒤 이전 코드가 기대하던 표를 조회할 수 없다」(명령대로 한 것) → 실제 결함: 줄이 든 표에 기본값 없는 NOT NULL 칸 → `23502`, 판 번호·칸 그대로.
2. 「`subprocess.run(["alembic", …])`」(PATH 의존) → 파이썬 함수 `command.upgrade`·`downgrade`.
3. 옛 노트북의 접속 글 `localhost`·`os.getenv("CH31_DATABASE_URL", …)`·`replace` 셋 → 01 설정 셀과 드라이버만 다른 `127.0.0.1` 글 하나, Alembic에는 환경 변수로.
4. b4·b7·복습의 자동 생성 설명(실행한 적 없음) → 「`env.py`에 표 정의가 이어져 있지 않아 실행하지 않았습니다」 + 문서의 「늘 사람이 읽고 고쳐야 한다」.
5. b6 「Docker의 독립 PostgreSQL 17.8 … 시간과 실행 계획」 → 이 절은 시간·계획을 재지 않음, 교재 출력 버전 17.11(Docker 없이 같은 접속 글) · 학생 이미지 버전 가름.
6. 첫 판 설명 글 「표 구조를 변경합니다」 → 노트북 결과 읽기에서 「이 판은 표를 새로 만듭니다」(파일은 그대로).
7. 「확장-이행-축소 순서」·「백업 복구 시간을 측정」 단정 → 뺌. 판 내리기의 값 사라짐은 출력으로 보임, 값을 남기는 방법은 05절(백업)로.
8. 옛 그림의 빨강·보라가 실패·모델이 아닌 요소 → 빨강은 Before 결함 결과 두 상자만, 보라 0.

## 그림

- Mermaid **5장**(설계표 `03-figures.md`를 렌더 전에 씀): 03-1 판 사슬과 판 기록 표(b4·노트북 오늘 볼 그림, viewBox 폭 **271**) · 03-2 사본으로 첫 판 올리기(b5, **481**) · 03-3 기본값 없는 NOT NULL 칸의 Before(b6, 274 × 723) · 03-4 기본값 없는 판과 서버 기본값 판 견주기(b6, **614**) · 03-5 판 내리기와 다시 올리기(b6, 256). 모두 868 이하 · `flowchart TB` · subgraph 제목 `<br>` 없음 · 라벨 대괄호·따옴표 없음 · 개수는 한글 · 노드 7개 이하 · 노드 id `call`·`end` 없음 · `%% classes`. **첫 렌더에서 셋(03-2·03-3·03-4)이 자동 줄바꿈** → `<br>`로 더 나눠 다시 렌더(PNG 다섯을 직접 열어 확인 — 03-4는 Before 칸이 왼쪽, 03-1 점선은 둘째 판 → 첫 판). **보라 0 · 빨강 2상자(03-3 판 번호·칸 그대로·03-4 Before 결과 — 둘 다 Before 결함 결과)**. 03-4 맨 위 회색 공통 상자는 두 판 출력에서 모두 확인한 값만(시작 판·줄 셋·둘째 판 번호 — 두 판 모두 진행 기록 `Running upgrade 20260911_01 -> 20260929_02`). 03-3의 「서버가 SQL 문장을 막음 · 한 묶음 작업 전체가 취소됨」은 수동형(취소를 누가 보내는지는 출력으로 보지 않음 — 결과인 판 번호·칸만 출력).
- 삽화 1장 **03-6 빈 자리 판과 마개를 꽂은 판**(b4 비유 뒤, 본문만): 1차 job `3f28a43c-9acd-41f1-9909-c447a826efe2` 탈락(왼쪽 판이 세로 세 줄 — 빈 자리 한 줄이 판에 붙어 Before와 반대로 읽힘, 오른쪽 판 세로 네 줄) → **2차 job `1f2ce2ae-15dd-40f0-9127-7bb7fcca1fef` 채택**(재생성 1회). 거래 17:13:40Z·17:14:39Z 「Nano Banana Pro −2」 두 줄 = **이 절 몫 4크레딧**(잔액 2257 → 2253, 바로 앞 거래 16:34:28Z는 02). 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만). 저장 PNG 1100 × 614 `d0c61837…`, 결과를 다시 받아 같은 폭으로 줄인 그림과 **픽셀 차이 0**(bbox `None`). 그림에서 센 것: 판 둘 · 왼쪽 세로 두 줄·주황 꽂이 여섯·빈 자리 0 · 탁자 위 가는 판 하나·빈 구멍 셋 · 오른쪽 세로 세 줄·주황 여섯·회색 마개 셋 · 선·불·전원 플러그 0. 거의 흰 가로줄 64/614. 세부 `figures/03-6-…prompt.md`.
- 운영 메모: 기기 VM이 aarch64라 직접 렌더할 때 `LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu`(`run_section.sh`는 스스로 고름 — 첫 직접 렌더를 x86_64 경로로 불러 한 번 실패). 파일을 다시 렌더한 뒤 같은 이름으로 `device_stage_files`를 다시 부르면 옛 그림이 보였음 → `.cache/ch31-03-view/`에 다른 이름으로 복사해 확인.

## 검사

- 게이트 G1~G7 0(`gates-wip-03.json`) · `verify.py --chapter` **PASS 5 sections / 86 code cells (max 25 lines)**(최대 25줄은 손대지 않은 05 옛 셀) · 빌드 HTML `03-Alembic-적용과-롤백.html`·`_src` `{{`·`[[` 0 · 생성기 `cells()`(`split_part_boundaries` 뒤 67셀)와 저장 노트북 셀 소스 67개 모두 같음(`mdpatch.py` 뒤 대조) · review-pack `qa/upgrade/review-pack/03-Alembic-적용과-롤백.md`.
- 화면 검사 `visual.cjs`는 돌리지 않음(마감 몫).

## 완료 챕터·앞 절·뒤 챕터 문장 참·거짓 (고치지 않음)

- **02 노트북 6절·b4 소제목** 「03절 제목의 롤백은 표 구조의 판을 내리는 일이라, 이 절의 취소와 뜻이 다릅니다」 — **참**(03이 제목의 롤백 = 판 내리기 `downgrade`로 풀고, 02 취소와 다름을 노트북 1·8절·b2·b4·복습 5에 씀). **02 b8·노트북 정리 끝** 「03절에서는 Alembic으로 표 구조를 판마다 바꾸는 방법을 봅니다」 — **참**(판 사슬 `20260911_01` → `20260929_02`, 판 올리기·내리기). 02는 다시 실행·수정할 것 없음.
- **01 b8** 「02절에서는 …」 — 03과 무관(02가 참으로 처리). 01 설정 셀 글 → 03은 드라이버만 다름(생성기 대조).
- **Ch 21 요약 64행**(완료 기록) 「Ch 23 02·Ch 31 03의 DB 「마이그레이션」과 다른 뜻」 — **참**(03이 DB 표 구조 바꾸기(마이그레이션)를 다루고 Ch 21 04 옮기기와 다른 뜻 문장을 노트북 2절·b3에 둠).
- **Ch 30 10 b8**(`_src`·HTML·노트북) 「Ch 31에서는 PostgreSQL 데이터베이스에 표를 만들어 쓰는 방법과 체크포인터를 다룹니다」 — 03도 판 파일로 표를 만들고 칸을 더함 **참**(체크포인터는 05 몫) · 「보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다」(Ch 30 06 b7·10 b8) — 03에 SSE 0 **참**.
- **Part 7 목차** 「Ch31의 데이터 저장」 — 참. **Ch 32 04 b3**(대기) 「Ch31에서는 PostgreSQL, 트랜잭션, 인덱스와 pgvector를 배웁니다」 — 03 무관. **`labs/part7/continuity-guide.md` 9행**에 마이그레이션 없음 — 마감 대조.
- `grep -rn 'Ch *31'`(Part 1·2·3·5·6·7 HTML, ch31 밖): Part 7 목차 둘·Ch 30 06·10·Ch 32 04와 옛 판 사본(`before/`)뿐 — 03에 기대는 새 문장 없음.

## 챕터 밖 수정

- 없음. (공용 도구·Part 7 파일·다른 챕터 파일 0. `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json`은 `verify.py --chapter`가 다시 쓴 챕터 계약 파일.)
- 실습 폴더 파일(`app/`·`migrations/`·`alembic.ini`·`README.md`·`pyproject.toml`·`uv.lock`) 고침 0.

## 강사 확인 대상

1. **말**: 「마이그레이션」 → 「표 구조 바꾸기(마이그레이션)」, 「리비전」 → 「판(리비전)」, `upgrade`/`downgrade` → 「판 올리기/판 내리기」, 제목의 「롤백」 = 판 내리기. 절 제목 「Alembic 적용과 롤백」은 제목에 두고 본문 첫 자리에서 풂. 이 절에서만 패키지·서버 번호를 「버전」으로 적음(01·02는 「판」 — 「판」이 표 구조의 판과 겹쳐서).
2. **stderr 진행 기록**: Alembic 기록이 노트북에서 오류 출력 쪽(편집기에 따라 붉은 바탕)으로 찍힘 — 「오류 아님」 한 문장으로 안내.
3. 첫 판 파일 설명 글 「상담 티켓 표 구조를 변경합니다」(실제로는 표를 만듦)는 실습 폴더 파일이라 그대로 — 고칠지(묶음·README 영향)는 마감 판단.
4. 코드 양: 코드 셀 6 → 31, 코드 줄 42 → 135(paired 한 절 — 예시·Before·After·판 내리기·값 바꿔 보기, 판을 올리는 셀과 결과 셀을 나눈 몫 여섯).
5. `env.py` 35행 조건 표현식·반환 힌트·`from __future__`(앱 파일 문법)은 노트북이 12~15행만 출력해 보이고 파일은 고치지 않음 — 학생이 파일을 열면 보임(Ch 28 A-17 선례 대상 여부는 마감 판단).

## 남은 것 (마감 몫)

- 옛 그림 `figures/03-흐름.{svg,excalidraw,caption.md}` 삭제 승인 목록(본문은 더 쓰지 않음) · Part 7 묶음 zip 다시 만들기·`check_bundle_execution.py`(서버를 켠 곳)·`bundle-execution.json` Ch 31 줄 새 `code_sha256`.
- README의 03 설명·「`.env`의 `CH31_DATABASE_URL`」 문장·`alembic` 명령(마감 — 01 진단과 같음).

## 지우지 않은 것 (삭제 승인 대상 — 이 절이 만든 것)

- 기기 `/tmp/ch31-03/`(약 15MB — `exp/` 확인 스크립트 셋과 출력·`try/` 사본 둘·`runB/`·`bundle/`(풀어 둔 묶음 3.1MB)·`illu/` 삽화 원본 셋(탈락 `r1.png` 포함)·`draft/`·`tools/`·`lab-before.sha`·`reps1.json`) · **세션 임시 폴더 `$HOME/tmp/ch31-03-*` 12개**(각 약 32KB — `tempfile.mkdtemp`가 만든 판 파일 사본: 노트북 밖 e1 다섯·e3 둘·노트북 실행 다섯(copy1·copy2·A·B·묶음)) · 연결 폴더 `.cache/ch31-03-view/`(PNG 여섯, 약 2.3MB) · `.cache/ch31-03/tools/`(열셋)·`.cache/ch31-03/exp/`(스크립트 셋과 출력 셋) — 기기 `/tmp`가 비어도 04가 쓸 수 있게 · `qa/upgrade/gates-wip-03-03.json`·`gates-wip-03.json`.
- 앞 절이 남긴 `/tmp/ch31-02/`·`.cache/ch31-01*`·`.cache/ch31-02*`, 공용 `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/libs`·`/tmp/npm-cache`·`/tmp/uv-cache`·`/tmp/ch31-pg/`는 건드리지 않음.

## 디스크

- 기기 루트 여유: 작업 전 **2.0G** → 끝 **2.0G**(`/tmp/ch31-03` 15MB) · 세션 디스크(`/sessions`, `$HOME/tmp`) 831M → 830M · 사용자 디스크(연결 폴더) 여유 76G → 75G(다른 세션 몫 포함, 이 절이 연결 폴더에 더한 것은 3MB 남짓).

## 보호 파일 (`before-manifest.json` 209개)

- 03절 뒤 **같음 195 · 바뀜 14 · 없어짐 0** — 01·02가 바꾼 것은 01·02 기록 값 그대로(집필점검표·verification·계약 파일은 03이 다시 바꿈), 03이 처음 바꾼 셋(절 HTML·`_src`·노트북 03) + 기록 둘 + 계약 파일. 표는 `manifest-changes.md`.
