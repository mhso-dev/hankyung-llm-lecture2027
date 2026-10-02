# 02절 진단 — 트랜잭션과 원자성 (paired)

- 작업일 2026-09-29 · 생성기 `qa/upgrade/author_02.py`(`db71734c…`) · 노트북 `labs/part7/ch31-database/notebooks/02-트랜잭션과-원자성.ipynb` · 본문 `_src/02-트랜잭션과-원자성.html` · 슬러그 그대로 · DB 준비 훅 `qa/upgrade/pre_exec.sh`(01이 만든 판 `8a9529f1…` 그대로 씀).
- 읽은 것: `handoff.md`(챕터 공통·§01 → §02 전부) · 준비 노트 `chapter-lead-notes.md`(02·§3·§7·§8 부분) · `01-diagnosis.md` · 본 생성기 `author_01.py`(전부)·Ch 30 `author_02.py`(paired 구조·`__main__` 대조)·`author_06.py`(머리 — 실제 조건 Before·빨강) · `AGENT-BRIEF.md`·`PLAYBOOK.md` · 규격 `QUALITY-UPGRADE.md`(전부) · 과정 요약(Ch 2 예외 처리·SQL `UPDATE`·Ch 23 줄) · Ch 4 03 `_src`·노트북(제약·`sqlite3.IntegrityError`·커밋) · Ch 23 04~06·Ch 2 05 `_src`(b1·b8) · Ch 30 요약 §18. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전(`gates-before.json`) | 5 | 84 | 4 | 0 | 3 | 0 | 7 | 15 | 3 | 32 |
| 첫 실행 전(`gates-wip-02-02.json`, G1·G2 먼저) | 23 | — | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 3(그림 없음) |
| 후(`gates-wip-02.json`, `--no-exec`) | **23** | **376** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

- AST 따로(`/tmp/ch31-02/tools/extra_check.py` — 01 판 그대로): 걸린 것은 셀 맨 위 `await`·`async def` 셋·`try` 셋뿐 — 챕터 허용 범위(`try`는 `except IntegrityError as error`, Ch 2 05·Ch 4 03 모양). 호출 깊이 최대 2 · 준비 셀 밖 셀 최대 9줄 · 함수 본문 최대 4줄 · 코드 줄 112(주석·빈 줄 뺌, 옛 판 48) · 클래스·데코레이터·ORM·`AsyncSession`·힌트 0.
- 금지어(`/tmp/ch31-02/tools/ban32.py` = 01 `ban31.py`에서 「트랜잭션」·「롤백」만 목록에서 빼고, 두 말은 `twoword.py`로 나온 자리를 모두 봄): `_src`·노트북 마크다운·코드 주석·`.mmd` 넷·캡션 다섯 모두 0. 「트랜잭션」은 절 제목·제목 풀이(「절 제목의 트랜잭션(transaction)은」)·괄호 원어(「한 묶음 작업(트랜잭션)」) 자리만, 「롤백」은 괄호 원어(「취소(롤백)」)·03 제목 인용(「03절 제목의 롤백은」, b4 소제목) 자리만. 「되돌」·「돌려」와 과정 금지 문구 0.
- 인용 대조(`quotes.py`): 노트북 백틱 71개·`_src` `<code>` 42개 가운데 출력·코드에 없는 것은 명령·파일·API 이름뿐(`docker start kdt-ch31-postgres`·`uv sync --locked`·`sqlite3.IntegrityError`·`commit()`·`check_violation`·설치판 소스 파일 이름 등).

## 수정 전 주요 문제 (옛 판 — `before/notebooks/02-…ipynb`·`before/_src/02-*.html`)

1. **Before가 실제 결함이 아님** — 출금 블록을 확정한 뒤 **코드가 직접 `raise RuntimeError("입금 직전 장애")`**를 던져 900(규격 §3 「실패 장면은 실제 조건으로」, Ch 30 판정 기준). After도 `raise` 뒤에 닿지 않는 입금 줄 하나.
2. 문법: `[row.balance for …]` 내포식 둘·`sum(row.balance for …)` 제너레이터 식 둘 · `except RuntimeError: pass` · `(await conn.execute(…)).all()` 호출 사슬 · 셀 첫 줄 주석 0 · 결과 읽기 0 · 준비 셀 `%pip` 세 줄(이 절이 쓰지 않는 alembic·psycopg·pgvector·langgraph 설치) · `os.getenv` 주소 셋(`SYNC_URL`·`NATIVE_URL`은 쓰지 않음, `localhost`).
3. 말: 「트랜잭션」 22·「롤백」 12·**「되돌립니다」(게이트 금지어 「돌립니다」)**·「장애」·「격리」·「보장」·「멱등」·「세션」 · 비유 「은행 창구」(Ch 6 01-5 「상담 창구」 겹침) · 제목 셀 「운영 데이터베이스의 한 가지 문제를 재현하고 해결합니다」(다섯 절 틀 문장) · 「이 준비 셀이 하는 일」 틀 단락.
4. b3 「앞 절에서 작업마다 비동기 세션을 만들었습니다」(개선된 01은 `AsyncSession`을 쓰지 않음 — 거짓) · b4 「운영에서 경계를 정하는 방법」 긴 단락(실행하지 않은 격리 수준·재시도 설명, 한정 없음) · b6 「Docker의 독립 PostgreSQL 17.8 컨테이너와 작은 데이터에서 측정했습니다 … 시간과 실행 계획」(이 절은 시간·계획을 재지 않음) · b7 「보상 작업이 필요합니다」(Ch 23이 다루지 않음 — Ch 23 요약 210행) · b10 제목이 모두 「트랜잭션과 원자성 공식 문서」·확인 2026-09-11·PostgreSQL `current`(18) 문서.
5. 그림: `{{svg:02-흐름}}` 한 장(「붉은 트랜잭션 경계」·「초록색 오류」·「보라색 전체 롤백」 — 실패 아닌 요소에 빨강, 보라 뜻 어긋남), Mermaid·삽화 0.

## 바꾼 것

- **paired 설계(handoff §01 → §02 2)**: 표 `ch31_tx.accounts(id int PRIMARY KEY, balance int CHECK (balance >= 0))` 500·500 → 예시 부분에서 한 블록 이체 함수 `transfer_one_block`(받는 계좌에 더하기 → 보내는 계좌에서 빼기)으로 100 → `[(1, 400), (2, 600)]`·합계 1000. **Before** = 함수 `transfer_two_blocks`(같은 두 줄을 begin 블록 둘에 하나씩 — 둘째 `async with engine.begin() as conn:` 줄 하나만 다름)로 600 → 첫 블록(2번 +600) 확정 → 둘째 블록(1번 −600)이 **`IntegrityError`·SQLSTATE `23514`·`accounts_balance_check`·`Failing row contains (1, -100).`**로 막힘(받은 오류 노랑) → **`[(1, 500), (2, 1100)]`·합계 `1600`**(받은 결함 결과 — 빨강). **After** = 같은 600을 `transfer_one_block`으로 → 같은 오류 → `[(1, 500), (2, 500)]`·합계 1000(노랑) → 블록 안에서 더하기 뒤 2번 잔액을 읽는 판(`블록 안에서 읽은 2번 잔액: 1100`) → 블록 밖 `[(1, 500), (2, 500)]`(**취소를 처음 보임 — 01 3절 결과 읽기 약속 참**) → 합계 비교 `Before 뒤 합계가 처음과 같은가: False`·`After …: True`. **값 바꿔 보기** = 보낼 돈만 500 → `[(1, 0), (2, 1000)]`(CHECK가 0을 허용, 오류 없음).
- 옛 판 `RuntimeError` 장면·닿지 않는 줄은 쓰지 않음. 받는 계좌에 먼저 더하는 차례는 결함이 잔액에 보이게 정한 예라고 노트북 5절 끝·b7에 밝힘(규격 §3 — 노트북 밖 확인: 빼기를 먼저 하는 블록 둘은 첫 블록에서 막혀 500·500 그대로).
- **말(handoff 「뒤 절이 정할 말」)**: 트랜잭션 → **「한 묶음 작업(트랜잭션, transaction)」**(절 제목에만 원어 — 노트북 1절·b2 「절 제목의 트랜잭션(transaction)은 … 본문에서는 「한 묶음 작업」이라고 부릅니다」) · 커밋 → **「확정(커밋)」**(Ch 4 03 커밋 이음) · 롤백 → **「취소(롤백, rollback)」** + 「03절 제목의 롤백은 표 구조의 판을 내리는 일이라, 이 절의 취소와 뜻이 다릅니다」 · 원자성(제목 말) = 뜻 → 계약서 예 → 6절 잔액 · CHECK 제약(Ch 4 03 「제약(constraint)」 이음)·오류 코드 SQLSTATE는 풀이만. 새 용어 meta **3**(한 묶음 작업·원자성·취소).
- 첫 풀이(뜻 → 일상 예 → 코드): 한 묶음 작업(장바구니 한꺼번에 계산)·원자성(두 사람 서명 계약서)·취소(볼펜으로 옮겨 적기 전 지우개) · 풀이만: SQL `UPDATE … SET … WHERE`(과정 요약 「처음 쓰면 한 문장」)·`WHERE` 없는 `UPDATE`·CHECK 제약·SQLSTATE·`IntegrityError`(Ch 4 03과 같은 이름, 패키지 sqlalchemy의 모듈 `exc`)·`error.orig`·`row.balance`·SQLAlchemy 기본 풀 크기 5.
- 접속 글: 설정 셀 = **`author_01.SETTINGS` 글자 그대로**(`__main__`에서 `assert SETTINGS in author_01.py 글` — 노트북 2절 「01절 2절의 설정 셀과 글자까지 같은 셀」의 근거). 엔진은 풀 인자 없이(`풀에 둘 연결 수: 5` — 한 문장, 이 절은 연결을 한 번에 하나씩만 빌림).
- 오류 출력은 매번 같은 것만: `type(error).__name__` · `error.orig.sqlstate` · 라벨 줄 뒤 `print(error.orig)`(드라이버 오류 글 두 줄 — 서버 주소·PID·시각 없음 확인). `print(error)` 전체(SQL 글·값·오류 설명 주소 여러 줄)는 쓰지 않고 b7에 밝힘.
- 이름 공간 `ch31_tx`: 3절 `DROP SCHEMA IF EXISTS … CASCADE` → `CREATE SCHEMA` → 표 → 두 줄(한 `begin` 블록) · 8절 `DROP SCHEMA` + `to_regnamespace` → `None` + `dispose()`. 두 번 실행해도 같은 출력(사본 시험 뒤 A·B를 이어 실행 — 셋 모두 같은 출력).
- b2 「대화 기록 한 줄 저장 + 남은 횟수 하나 줄이기」(옛 「메시지 저장·사용량 차감」을 한 예로) · b3 01절·Ch 4 03·Ch 2 05·Ch 23 04~06 링크(**Ch 23 요약 §15 209행 「02 b3 Ch23 중단 뒤 재개와 멱등성」 참 — 유지**, 말은 「멈춘 그래프를 이어 실행」·「멱등 키」) · b7 보상 작업 풀이 + 「이 챕터에서는 실행하지 않았습니다」(Ch 23 §15 210행 몫 처리) · b10 새로(SQLAlchemy Connections·Core Exceptions·PostgreSQL 17 Transactions·Constraints·Error Codes, 확인 2026-09-29 + 설치판 소스 행 둘).
- 비유 계열 「전화 교환대」 이어 씀: 넓은 금속 판 하나·꽂는 자리 짝 셋(짝 = 이체의 두 변경, 선 한 가닥 = 한 묶음 작업) — 양 끝 꽂힘(이체 100) · 한 끝만(Before) · 둘 다 빔(After). b4 「비유와 다른 점」(실제 블록은 변경을 먼저 적용해 두고 끝에서 한꺼번에 확정·취소).
- 도구 파일: **만들지 않음**(handoff 챕터 공통 8 S1 유지) — 이 절의 함수 넷(`read_balances`·`add_balances`·`transfer_one_block`·`transfer_two_blocks`)은 표 `ch31_tx.accounts`와 전역 `engine`·`deposit_sql`·`withdraw_sql`에 기대는 이 절 전용이고, 03(Alembic·동기 드라이버)·04(풀 고갈)·05(pgvector·체크포인터)가 그대로 쓸 일이 없음. 01 `read_question`과도 겹치지 않음.

## 설치판 동작 확인 (모델 없이 — `/tmp/ch31-02/exp/`, 가상환경 `.cache/vm/venv-ch31-database`)

- `p0_attrs.py`: 기본 풀 `AsyncAdaptedQueuePool`·크기 5 · 받은 오류 `sqlalchemy.exc.IntegrityError`(MRO `IntegrityError → DatabaseError → DBAPIError → StatementError → SQLAlchemyError → …`) · `error.orig` = `sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.IntegrityError`(속성 `pgcode`·`sqlstate` = `23514`) · `error.orig.__cause__` = `asyncpg.exceptions.CheckViolationError`(`constraint_name` `accounts_balance_check`·`table_name` `accounts`·`detail` `Failing row contains (1, -100).`) · `str(error.orig)` = 두 줄(`<class 'asyncpg.exceptions.CheckViolationError'>: new row for relation "accounts" violates check constraint "accounts_balance_check"` / `DETAIL:  Failing row contains (1, -100).`) · `str(error)`은 그 뒤에 `[SQL: …]`·`[parameters: (600, 1)]`·`(Background on this error at: https://sqlalche.me/e/20/gkpj)`.
- `p1_scene.py`(노트북 장면 그대로 `asyncio.run`, **5번**): 출력 sha256 앞 16자리 다섯 번 모두 `a669ce6a6771496a` — 처음 500·500·1000 · 이체 100 → 400·600 · Before 23514 → 500·1100·1600 · After 23514 → 500·500·1000 · 블록 안 2번 1100 → 밖 500 · 500 이체 → 0·1000 · (b7 확인) 빼기 먼저 두 블록 → 첫 블록에서 `IntegrityError`, 500·500 · 정리 `None`·쉬는 연결 0.
- 설치판 소스(sqlalchemy 2.0.43): `ext/asyncio/engine.py` 1050~1068행(`begin()` = `connect()` + `conn.begin()` 블록) · 1419~1420행(`AsyncTransaction.__aexit__` → 동기 `__exit__`) · `engine/util.py` 143~162행(오류 없음 → `commit()`, 오류 → `rollback()`) · `dialects/postgresql/asyncpg.py` 786~791행(`"%s: %s" % (type(error), error)`로 글을 만들고 `pgcode`·`sqlstate`를 채움 — 오류 글이 `<class …CheckViolationError'>`로 시작하는 까닭).
- 문서 대조(WebFetch 2026-09-29): SQLAlchemy Connections — 「will commit itself when the block ends normally and emit a rollback if an exception is raised, before propagating the exception outwards」·`Engine.begin()`은 begin once 줄임 / Core Exceptions — 「The wrapped exception object is available in the StatementError.orig attribute」·IntegrityError 「Wraps a DB-API IntegrityError」 / PostgreSQL 17 3.4 — 「bundles multiple steps into a single, all-or-nothing operation」·Alice → Bob 100달러 이체 예·ROLLBACK은 「all our updates so far will be canceled」 / 5.5.1 — 「an error is raised」·「the system chooses a name for you」 / Appendix A — 다섯 글자·앞 두 글자 갈래·「should usually test the error code, rather than looking at the textual error message」·`23514` `check_violation`. 문서와 설치판 출력이 어긋난 곳 없음.

## 실행 (새 커널)

- 첫 실행 전 `/tmp/ch31-02/try` 사본으로 `runcopy.sh`(훅 source + `execute.py --cwd`) PASS 23셀 — 실습 폴더에 `.failure.json`이 남지 않게.
- **A**: `env -u OPENAI_API_KEY PYTHONDONTWRITEBYTECODE=1 bash run_section.sh textbook/part7/ch31-database 02` — 프로젝트 맨 위 커널, **`executed_at` 2026-09-29T16:31:16Z**, PASS 23셀(그림 첨부 단계에서 멈춤 — 02-1 PNG가 아직 없어서, 실행·저장은 끝난 뒤) · `code_sha256` **`39d29f86a1f263265d7aed6a7343da598e523d597cd8de4985203d09af600dc1`** · `outputs_sha256` `a44f100e391036ae6a3314822ca8c3e17a0d4b0e6fb44671612de12d418801ad`.
- **B**(그림 전): 저장 노트북 사본 `/tmp/ch31-02/runB/`를 `execute.py --cwd labs/part7/ch31-database/notebooks`(학생 커널 자리), 16:31Z, PASS 23셀 · `code_sha256` 같음 · `outputs_sha256` `22e565f5f601bd0c…`.
- **셀별 출력 글자 대조(`cmpout.py`): 23개 모두 같음.** `outputs_sha256`이 다른 것은 설치 셀 [1]의 출력 조각 나눔뿐(A는 `Note: …` 조각과 `\nsqlalchemy …` 조각 둘, B는 한 조각 — 이어 붙인 글은 같음, Ch 30 01·10 마감과 같은 현상). 흔들리는 값 없음 → 결과 읽기에 `[[…]]` 자리·`mdpatch.py` 없음.
- 실습 폴더에 새로 생긴 파일 0(노트북 02 말고) · `__pycache__` 0 · `.failure.json` 0 · 커널 작업 폴더에 파일 쓰기 0 · 모든 셸 호출 뒤 postgres 프로세스 0·55431 포트 0.

## 고친 틀린 사실

1. Before 「장애」가 코드가 직접 던진 `RuntimeError` → 실제 CHECK 제약 위반(SQLSTATE `23514`)으로 막힌 뒤 남은 잔액(1600).
2. b3 「앞 절에서 작업마다 비동기 세션을 만들었습니다」 → 01은 연결을 빌려 SQL 글을 보냄(`AsyncSession` 0).
3. b6 「Docker의 독립 PostgreSQL 17.8 컨테이너 … 시간과 실행 계획도 달라집니다」 → 이 절은 시간·계획을 재지 않음, 교재 출력 판 17.11(Docker 없이 같은 접속 글) · 학생 이미지 판 가름.
4. b7 「보상 작업이 필요합니다」(Ch 23이 다룬 것처럼 읽힘) → 뜻 풀이 + 「이 챕터에서는 실행하지 않았습니다」, 멱등 키는 Ch 23 06 링크.
5. b4·b6 격리 수준·READ COMMITTED·동시 이체·SERIALIZABLE 재시도 단정 → 뺌, 「여러 연결이 같은 계좌를 함께 바꾸는 장면은 실행하지 않았습니다」(b7).
6. b10 PostgreSQL `current`(18) 문서·제목 없는 링크 → 17 문서 다섯 + 설치판 소스 행, 확인 2026-09-29.
7. 옛 그림의 빨강·보라가 실패·모델이 아닌 요소 → 빨강은 Before 결함 결과 두 상자만, 보라 0.

## 그림

- Mermaid **4장**(설계표 `02-figures.md`를 렌더 전에 씀): 02-1 한 묶음 작업의 두 갈래(b4·노트북 오늘 볼 그림, viewBox 폭 **442**) · 02-2 계좌 표 준비와 이체 100(b5, 222 × 688) · 02-3 블록 둘로 따로 확정한 Before(b6, 262 × 779) · 02-4 블록 둘과 블록 하나 견주기(b6, **553**). 모두 868 이하 · `flowchart TB` · 갈래는 점선(02-1) · subgraph 제목 `<br>` 없음 · 라벨 대괄호·따옴표 없음 · 개수는 한글 · 노드 7개 이하 · 노드 id `call`·`end` 없음 · `%% classes`. 첫 렌더에서 자동 줄바꿈 0(라벨을 `<br>`로 미리 나눔, PNG 넷을 직접 열어 확인 — 02-4는 Before 칸이 왼쪽). **보라 0 · 빨강 2상자(02-3 남은 잔액·02-4 Before 결과 — 둘 다 Before 결함 결과)**. 02-4 맨 위 회색 공통 상자는 두 판 출력에서 모두 확인한 값만(처음 500·500·이체 600·`23514`).
- 삽화 1장 **02-5 양 끝이 꽂힌 선과 한 끝만 꽂힌 선**(b4 비유 뒤, 본문만): 1차 job `7669c5cd-59e6-41c5-891b-a624c02dcbba` 탈락(자리가 두 구멍 벽 콘센트·늘어진 끝이 두 핀 전원 플러그 — 멀티탭으로 읽힘, handoff 금지 소품 「콘센트 플러그」) → **2차 job `e184fcf0-e311-4103-8f35-e19132adb75b` 채택**(재생성 1회). 거래 16:33:11Z·16:34:28Z 「Nano Banana Pro −2」 두 줄 = **이 절 몫 4크레딧**(잔액 2261 → 2257, 바로 앞 거래 15:58:41Z는 01). 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만). 저장 PNG 1100 × 614 `b22a0bfa…`, 결과를 다시 받아 같은 폭으로 줄인 그림과 **픽셀 차이 0**(bbox `None`). 그림에서 센 것: 판 하나 · 자리 여섯(짝 셋) · 불 여섯 · 선 셋 · 켜진 불 둘·하나·0 · 전원 플러그 0. 거의 흰 가로줄 106/614 · 판 좌우 끝이 조금 잘림. 세부 `figures/02-5-…prompt.md`.

## 검사

- 게이트 G1~G7 0(`gates-wip-02.json`) · `verify.py --chapter` **PASS 5 sections / 61 code cells (max 25 lines)**(최대 25줄은 손대지 않은 05 옛 셀) · 빌드 HTML `02-트랜잭션과-원자성.html` `{{`·`[[` 0 · 오류 글의 `<class …>`는 HTML에서 `&lt;class …&gt;`로 이스케이프됨 · review-pack `qa/upgrade/review-pack/02-트랜잭션과-원자성.md`.
- 화면 검사 `visual.cjs`는 돌리지 않음(마감 몫).
- 실수 한 번(기록): 마지막 `verify.py`를 환경 변수 없이 `uv run --project labs/part7/ch31-database`로 불러, uv가 실습 폴더의 맥 `.venv`를 다시 만들려다 `.venv/.lock` 지우기에서 `Operation not permitted`로 멈춤. `.venv` 안 파일은 모두 2026-09-11 판 그대로(최근 10분 안에 바뀐 파일 0, 보호 파일 `.venv/pyvenv.cfg` `facfac63…` 같음). 같은 검사를 `run_section.sh`와 같은 환경 변수(`UV_PROJECT_ENVIRONMENT=.cache/vm/venv-ch31-database`·`UV_NO_SYNC=1`)로 다시 불러 PASS.

## 완료 챕터·뒤 챕터 문장 참·거짓 (고치지 않음)

- **01 b8·노트북 정리 끝** 「02절에서는 두 계좌의 잔액을 바꾸는 이체를 봅니다. 바꾼 내용을 따로 확정할 때와 한 블록으로 확정할 때를 견줍니다」 — **참**(Before 블록 둘 ↔ After 블록 하나). **01 3절 결과 읽기·b4** 「블록 안에서 오류가 나면 확정하지 않는데, 그 모양은 02절에서 봅니다」 — **참**(6절 블록 안 1100 → 밖 500).
- **Ch 30 10 b8**(`_src`·HTML·노트북) 「Ch 31에서는 PostgreSQL 데이터베이스에 표를 만들어 쓰는 방법과 체크포인터를 다룹니다」 — 02도 표를 만들어 씀 **참**(체크포인터는 05 몫). 「보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다」(Ch 30 06 b7·10 b8) — 02에 SSE 0 **참**.
- **Part 7 목차** 「Ch31의 데이터 저장」 — 참.
- **Ch 32 04 b3**(대기 챕터) 「Ch31에서는 PostgreSQL, 트랜잭션, 인덱스와 pgvector를 배웁니다」 — **트랜잭션 부분 참**(02가 한 묶음 작업(트랜잭션)을 가르침 — 말은 바뀌었지만 내용 유지, 원어는 괄호로 남음). 인덱스·pgvector는 05 몫.
- **`labs/part7/continuity-guide.md` 9행** 「Ch31의 트랜잭션·연결 풀·인덱스」 — 트랜잭션 부분 참(마감 대조).
- **Ch 23 요약 §15 209행** 「02 b3 Ch23 중단 뒤 재개와 멱등성」 — 참, 유지. **210행** 「02 b7 보상 작업」 — 02가 풀어 쓰고 「실행하지 않았습니다」로 처리.
- Part 1~6 HTML에 「Ch 31」 문장 0(`grep`).

## 챕터 밖 수정

- 없음. (공용 도구·Part 7 파일·다른 챕터 파일 0. `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json`은 `verify.py --chapter`가 다시 쓴 챕터 계약 파일.)
- 실습 폴더 파일(`app/`·`migrations/`·`alembic.ini`·`README.md`·`pyproject.toml`·`uv.lock`) 고침 0 — 노트북은 실습 폴더 파일을 읽지 않음.

## 강사 확인 대상

1. **말**: 「트랜잭션」 → 「한 묶음 작업(트랜잭션)」, 「롤백」 → 「취소(롤백)」, 「커밋」 → 「확정(커밋)」. 절 제목 「트랜잭션과 원자성」은 제목에 두고 본문 첫 자리에서 풂(Ch 23 금지어 「트랜잭션」).
2. **받는 계좌에 먼저 더하는 차례**는 Before 결함이 잔액에 보이게 정한 예(노트북 5절 끝·b7에 밝힘).
3. 오류 글 `print(error.orig)`의 둘째 줄 `DETAIL:  Failing row contains (1, -100).`은 서버의 영어 글(학생 Docker 이미지도 같은 글일 것으로 보나 이미지로는 실행하지 않음).
4. 코드 양: 코드 셀 5 → 23, 코드 줄 48 → 112(paired 한 절 — 예시·Before·After·블록 안 확인·값 바꿔 보기).
5. 삽화 판 좌우 끝이 조금 잘림(재생성 한도를 써 전원 플러그를 없앤 2차 채택).

## 남은 것 (마감 몫)

- 옛 그림 `figures/02-흐름.{svg,excalidraw,caption.md}` 삭제 승인 목록(본문은 더 쓰지 않음) · `qa/verification.md`·`집필점검표.md` 머리 「개선 전 판」 표시(끝에 행만 더함).
- README의 02 설명·「`.env`의 `CH31_DATABASE_URL`」 문장(마감 — 01 진단과 같음).

## 지우지 않은 것 (삭제 승인 대상 — 이 절이 만든 것)

- 기기 `/tmp/ch31-02/`(약 12MB — `exp/` 확인 스크립트 둘과 출력·`try/`·`runB/` 사본·`illu/` 삽화 원본 넷(탈락 원본 `r1.png` 포함)·`tools/`) · **기기 VM 재시작(작업 시작 전, `uptime` 8분)으로 `/tmp`가 비어 다시 설치한 Mermaid 렌더 도구 `/tmp/mmd`(470MB)·`/tmp/pptr-cache`(662MB)·`/tmp/libs`(60KB)와 설치 부산물 `/tmp/npm-cache`(241MB — README는 지우라고 적지만 이 작업은 지우지 않음)** · `uv`가 만든 `/tmp/uv-cache`(235MB) · 훅이 재시작 뒤 `initdb`부터 다시 만든 `/tmp/ch31-pg/`(46MB — 03~05가 계속 씀) · 연결 폴더 `.cache/ch31-02-view/`(PNG 둘, 약 1.2MB) · `qa/upgrade/gates-wip-02-02.json`·`gates-wip-02.json` · 도구·확인 파일 사본 `.cache/ch31-02/tools/`(열 개)·`.cache/ch31-02/exp/`(확인 스크립트 셋과 출력 둘) — 기기 `/tmp`가 재시작으로 비어도 03이 쓸 수 있게.
- 01이 남긴 `.cache/ch31-01/`·`.cache/ch31-01-view/`, 준비 담당의 `.cache/vm/pgembed-try`는 건드리지 않음.

## 디스크

- 기기 루트 여유: 작업 전 **3.6G** → Mermaid 도구 다시 설치 뒤 2.2G → 끝 **2.0G**(`/tmp/mmd`·`pptr-cache`·`npm-cache` 약 1.37GB · `uv-cache` 235MB 몫) · 사용자 디스크(연결 폴더) 여유 79G → 76G(다른 세션 몫 포함, 이 절이 연결 폴더에 더한 것은 1.3MB 남짓).

## 보호 파일 (`before-manifest.json` 209개)

- 02절 뒤 **같음 198 · 바뀜 11 · 없어짐 0** — 01이 바꾼 8개 가운데 7개는 01 기록 값 그대로, 챕터 계약 파일은 `verify.py`가 다시 씀(`ec9e7cd6…` → 새 값), 02가 처음 바꾼 셋(절 HTML·`_src`·노트북 02) + 기록 둘(`집필점검표.md`·`qa/verification.md` 끝에 02 행). 표는 `manifest-changes.md`.
