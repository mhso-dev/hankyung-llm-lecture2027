# 04절 진단 — 커넥션 풀 고갈과 대응 (paired)

- 작업일 2026-09-29 · 생성기 `qa/upgrade/author_04.py`(`f5a282a8…`) · 노트북 `labs/part7/ch31-database/notebooks/04-커넥션-풀-고갈과-대응.ipynb` · 본문 `_src/04-커넥션-풀-고갈과-대응.html` · 슬러그 그대로 · DB 준비 훅 `qa/upgrade/pre_exec.sh`(01이 만든 판 `8a9529f1…` 그대로 씀).
- **재개 작업**: 앞 04 작업자가 설계·노트북 밖 확인(5/5)·문서 확인을 끝낸 뒤, `author_04.py`를 기기에 쓰려던 순간 사용자 컴퓨터 연결이 끊겨 멈춤(기기에 `author_04.py` 없음 · 교재·노트북·보호 파일 고침 0 · 크레딧 0). 재개 자료 `.cache/ch31-04/resume/ch31-04-resume-notes.md`(확정 설계·출력 값·그림 계획·문서 확인·설치판 소스 행)·`author_04_draft.py`(코드 셀 상수 전부)·`.cache/ch31-04/exp/`(= 기기 `/tmp/ch31-04/exp/`)를 통째로 읽고 설계는 다시 하지 않음. **재개 작업자가 새로 쓴 것**: 제목 셀·`cells()`(설명·결과 읽기 전부)·`_src` 10블록·그림 넷과 삽화·기록 파일 전부. 초안 상수와의 차이는 값 바꿔 보기 셀(`VARY`)의 둘째 주석 줄 하나(「대기 제한은 엔진을 만들 때 정하므로, 지금 엔진의 풀을 먼저 비웁니다」 — 셀 첫 줄 주석이 `dispose()` 줄을 설명하지 않아 더함)뿐(`diff`로 확인).
- **앞 작업자 확인 기록(재개 메모 그대로)**: 노트북 장면 `e1_scene.py`를 `asyncio.run`으로 5번 — stdout sha256 앞 16자리 `91c726007280fa11` 5/5·stderr 0바이트 · `e2_extras.py`(b7 근거, 노트북 밖) — [a] 풀 크기 2에 닫지 않은 연결 하나 → 다음 요청 ok·하나 더 닫지 않으면 `QueuePool limit of size 2 …` · [b] Before 셀 두 번 → 둘째 `await engine.connect()`가 `TimeoutError` · [c] 함수 안 지역 변수로 잃은 연결 → 반환 직후 빌려 간 1, `gc.collect()` 뒤 SAWarning(stderr, 주소 포함)·0, 다음 요청 ok · [d] `create_task` 타이밍 — 대기 1.0·쥔 0.3초 ok 5/5 / 대기 0.2·쥔 0.6초 `TimeoutError` 5/5 · [e] 닫지 않은 연결 `pg_stat_activity` `idle in transaction` → 닫은 뒤 `idle` · [g] `max_connections` 100 · [h] `max_overflow=1` 겹쳐 빌리기 ok·`Current Overflow: 1 Current Checked out connections: 2` → 반납 뒤 in pool 1 · [f] `from sqlalchemy.exc import TimeoutError` 뒤 이름이 가리키는 것은 `builtins.TimeoutError`가 아님(module `sqlalchemy.exc`). 문서 확인(WebFetch 2026-09-29, 문서 2.0.54 / 설치 2.0.43)과 설치판 소스 행.
- **재개 뒤 다시 확인**: 훅으로 DB를 켠 같은 셸에서 `e1_scene.py`를 2번 더 — stdout 앞 16자리 `91c726007280fa11` 2/2, stderr 0바이트, 기록 `e1_1.out`과 바이트까지 같음(`cmp`) → 설계 그대로 확정. 문서 여섯은 재개 작업자가 같은 날 다시 WebFetch(아래 「문서 대조」).
- 읽은 것: `handoff.md`(챕터 공통·§03 → §04 전부) · 준비 노트 `chapter-lead-notes.md`(§1·§2 04·§3·§6-4·§7) · `03-diagnosis.md`·`03-figures.md` · 본 생성기 `author_02.py`(전부)·`author_03.py`(제목 셀·b3·b8)·`author_01.py`(`SETTINGS`·풀 인자 풀이) · Ch 30 `author_02.py`(재정의 누수 Before·비우기 After·끝 정리)·Ch 30 02 `_src` b1·b2·b8 · Ch 16 05 노트북(`except TimeoutError` 셀 셋)·`_src` · `AGENT-BRIEF.md`·`PLAYBOOK.md` · 규격 `QUALITY-UPGRADE.md`(§2·§2-7·§3·§4·§5·§6·§7·§8) · 과정 요약(「처음 쓰면 한 문장」 표 — `create_task`) · 옛 판 `_src`. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전(`gates-before.json`) | 4 | 83 | 0 | 1 | 2 | 0 | 6 | 14 | 3 | 26 |
| 첫 실행 전(`gates-wip-04-04.json`, G1·G2 먼저) | 21 | 379 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 3(그림 없음) |
| 후(`gates-wip-04.json`, `--no-exec`) | **21** | **400** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

- 첫 실행 전 생성기 대조(`/tmp/ch31-04/tools/pregate.py` — `cells()`·`src_html()`을 임시 노트북으로): G1~G5 0, `_src` 70자 넘는 문장 셋(b7 `create_task` 문장·b8 다음 절 문장(굵은 라벨 포함 81자)·b10 소스 행)·영어로 시작해 조사가 붙은 문장 하나(「SQLAlchemy는」) → 고침(b8은 문장 둘로 — 아래 §04 → §05 1). 금지어 검사(`ban33.py` — 02·03 판 그대로)에서 「요청 함수」 하나(b5 「다음 요청 함수」 — Ch 30 금지어) → 「다음 요청이 할 일을 함수로」. 첫 실행 뒤 G5(결과 읽기 첫 단락 인용이 출력에 있는지) 0 — `[[…]]` 자리 없이 한 번에 맞음(모델 없음·흔들리는 값 없음).
- AST 따로(`extra_check.py` — 01~03 판 그대로): 걸린 것은 `await`(셀 맨 위 — 01·02 이어 씀)·`async def` 하나(`ask_database`, 본문 4줄)·`try` 넷(`except sqlalchemy.exc.TimeoutError as error` — Ch 2 05·02절 모양, 첫째 연결 블록 셀 하나 + 다음 요청 셀 세 곳) · 호출 깊이 최대 2 · 준비 셀 밖 셀 최대 9줄 · 코드 줄 98(주석·빈 줄 뺌, 옛 판 39) · 클래스·데코레이터·힌트·f-string·내포식·조건 표현식·`next`·`create_task`·`gather`·`time`·세미콜론·별표 풀기·대입 풀기·기본값 매개변수 0.
- 금지어(`ban33.py`): `_src`·노트북 마크다운·코드 주석·`.mmd` 넷·캡션 다섯 모두 0. 「커넥션」·「고갈」은 절 제목과 제목 풀이(노트북 1절·b2 「절 제목의 커넥션 풀(connection pool)은 01절에서 본 연결 풀입니다. 제목의 고갈은 …」)에만. 「반환」 0(「반납」·「풀에 다시 넣음」) · 사용자 금지 표현 0(생성기·노트북·`_src` `grep`).
- 인용 대조(`quotes.py`): 노트북 백틱 72개·`_src` `<code>` 61개 가운데 출력·코드에 없는 것은 명령·파일·API 이름(`docker run`·`uv sync --locked`·`except TimeoutError`·`from sqlalchemy.exc import TimeoutError`·`IntegrityError`(02 이름)·설치판 소스 파일 이름·`asyncio.create_task`·`pg_stat_activity`·`max_connections`)과 b7의 **노트북 밖 확인 값**(`QueuePool limit of size 2`·`Current Overflow: 1 Current Checked out connections: 2`·`idle in transaction`·`idle`·`100` — 본문에 「노트북 밖에서」로 밝힘)·b4의 02 출력 `풀에 둘 연결 수: 5`(02 노트북 출력)뿐.

## 수정 전 주요 문제 (옛 판 — `before/notebooks/04-…ipynb`·`before/_src/04-*.html`)

1. **Before가 타이밍에 기댐** — `asyncio.create_task(hold(0.6))` + `asyncio.sleep(0.05)` 뒤 둘째 연결(첫 연결에 걸린 초가 0.05초와 비슷 — 준비 노트 §2 04). 결과는 5/5 같았지만 까닭이 시간에 달림. **After는 설정값 바꾸기**(대기 제한 1.0초·첫 작업 0.25초) — 결함 코드를 고친 것이 아님.
2. **이름 가림** — `from sqlalchemy.exc import TimeoutError`가 파이썬의 `TimeoutError`(Ch 16 05에서 배운 것)를 가림. `sqlalchemy.exc.TimeoutError`는 파이썬의 `TimeoutError`를 이어받지 않음(`False`).
3. `create_task` 첫 풀이 없음(Ch 2 12 전제 금지 — 과정 요약 「처음 쓰면 한 문장」) · 힌트(`delay: float`·`-> None`·`-> int`) · 코드 셀 4·최대 18줄 · 첫 줄 주석·결과 읽기 0.
4. 말: 「커넥션 풀」 25·「반환」 11·「쿼리」 10·「체크아웃」 5·「최대」 5·「지연」·「백프레셔」·「상위 백분위수」·「인스턴스」 · 비유 「도서관 태블릿」(과정 금지 소품) · b4 `pool_pre_ping`·`pool_recycle`·백프레셔(실행 안 함) · b6 「Docker PostgreSQL 17.8에서 측정」(시간을 재지 않음) · b7 「상위 백분위수」·「체크아웃과 체크인 이벤트 추적」(실행 안 함) · b8 「마지막 절에서는 … 인스턴스」.
5. 그림: `{{svg:04-흐름}}` 한 장 — 「푸른·붉은·초록·보라」 틀 문장, 보라가 모델 아닌 요소, 빨강이 결함 결과 아닌 풀.

## 바꾼 것

- **paired 설계(handoff §03 → §04 2 권장안 — 반납 누락)**: 엔진 `create_async_engine(database_url, pool_size=1, max_overflow=0, pool_timeout=0.2)`, 조회는 표 없이 `SELECT current_database()`(이름 공간·표를 만들지 않음 — 서버에 남기는 것 0). **예시**(3·4절) = `async with` 블록 안 `빌려 간 연결 수: 1` → 밖 0·쉬고 있는 1 · `status()` 글 · 함수 `ask_database`(다음 요청이 할 일) · 첫째 연결을 빌린 채 둘째 → `TimeoutError`(예시 부분에서 받은 오류 — 노랑) · 이름 가르기(`__module__` `sqlalchemy.exc`·`SQLAlchemyError` `True`·파이썬 `TimeoutError` `False`). **Before**(5절) = `conn = await engine.connect()` → 조회 → 닫지 않음 → `빌려 간 연결 수: 1`·`풀에 쉬고 있는 연결 수: 0` → 다음 요청 셀 → `받은 오류: TimeoutError`·`… timeout 0.20`(받은 오류 노랑) → **다음 요청이 연결을 받지 못함(빨강 — Before 결함 결과)** → 닫지 않은 연결로는 `ch31_lab`·`Current Checked out connections: 1`(연결은 멀쩡함). **After**(6절) = `await conn.close()` → 0·1 → 같은 조회를 `async with` 블록으로 → 0·1 → **같은 다음 요청 셀** → `받은 데이터베이스 이름: ch31_lab` → 모아 보기 `1` ↔ `0`. **값 바꿔 보기**(7절) = `dispose()` 뒤 대기 제한만 1.0초인 새 엔진에서 다시 닫지 않고 둠 → 같은 다음 요청 셀 → `timeout 1.00`(대기 제한은 기다리는 시간만 바꿈). **정리**(8절) = 닫고 `dispose()` → 0·0(다시 실행해도 같은 출력 — 닫지 않은 연결은 뒤 셀에서 모두 닫음, handoff 4).
- 다음 요청 셀은 5·6·7절 세 곳이 같은 상수(`__main__`에서 셋인지 대조 — 「글자까지 같습니다」 문장의 근거) · 설정 셀 = `author_01.SETTINGS` 글자 그대로(`__main__`에서 문자열 대조 — 03은 `psycopg` 판, 04는 01 판).
- **이름 가르기(handoff §03 → §04 3)**: `import sqlalchemy.exc` · `except sqlalchemy.exc.TimeoutError as error:` · 「이름 가림」(뜻 → 게시판 공지 예 → 이 절의 `from … import TimeoutError`) · Ch 16 05의 `except TimeoutError`로는 이 절의 오류를 받지 못한다는 것은 **출력 `False` + 파이썬 문서의 `except` 규칙으로 판단**(그 줄로 받아 보는 셀은 두지 않음 — 노트북 4절·b4·복습 5에 「실행하지 않았습니다」). `issubclass`·`__module__` 첫 풀이 한 문장씩.
- **출력 차례(handoff §03 → §04 6)**: 모든 셀 stderr 0(노트북 밖 5+2번·새 커널 A·B·사본 모두) — 닫지 않은 연결을 뒤 셀에서 반드시 닫아 쓰레기 수거 경고(주소 포함)가 나지 않게 함. 그 경고 장면(노트북 밖 [c])은 노트북에 넣지 않고 b7에 결정적인 부분(빌려 간 1 → 수거 뒤 0, 경고 글이 「끊는다」고 적음)만.
- **걸린 초**: 출력하지 않음(`time` 0) · 결론·그림 라벨에 초 없음 · 대기 제한 `0.2`·`1.0`과 오류 글의 `0.20`·`1.00`은 설정값(흔들리지 않음) · 제목 셀 「오류를 받는 셀은 대기 제한만큼 기다린 뒤 끝나지만, 걸린 시간은 재지 않습니다」 · `create_task` 타이밍 장면은 노트북 밖 확인으로 b7에만(「기다린 시간에 기대는 장면이라, 노트북에서는 실행하지 않았습니다」 + 한 문장 풀이).
- **말(handoff 「뒤 절이 정할 말」 04)**: 커넥션 풀 → 본문 「연결 풀」(01) · 고갈 → 「빌려 줄 연결이 없다」(제목 풀이 한 곳 — 03이 쓴 「연결 풀에 빈 연결이 없을 때」와 같은 뜻) · `pool_timeout` → **「대기 제한」** · 빌린 연결을 닫아 풀에 다시 넣기 → **「반납」**(01 「풀에 다시 넣음」 이어 씀) · 반납 누락 → 「닫지 않고 둔 연결」 · **「이름 가림」** · 새 용어 meta **3**(대기 제한·반납·이름 가림 — 옛 4). **패키지·서버 번호는 「버전」**(03 모양 — 이 절은 교환대 「판」을 비유에 써서, 01·02의 「판은 sqlalchemy …」 모양을 쓰지 않음) · Before/After 앞에 영어로 문장을 시작하지 않게 「After 쪽」.
- b3: 01(풀 인자·`async with`·`checkedin/out`·함께 기다린 실행이 셋을 빌림 — 「처음으로 겹쳐 빌림」은 01 실행 2 때문에 거짓이라 「풀에 둘 연결 수보다 많이 빌리려 할 때」로) · 02(한 묶음 작업·`try`로 이름과 코드) · 03(예고 문장) · Ch 2 05(`try`/`except`) · **Ch 30 02(재정의 누수 → 다음 테스트 504 → 딕셔너리 비우기 → 200 — 같은 모양의 Before)** · Ch 16 05(`except TimeoutError`).
- b7: 대기 제한·풀 키우기로는 반납 누락이 결국 같은 오류(노트북 밖 [a]) · Before 셀 두 번(밖 [b]) · 함수 안에서 잃은 연결과 쓰레기 수거(밖 [c] + 문서 「비동기 드라이버에서 지원하지 않음」) · 닫지 않은 연결 = 열린 한 묶음 작업 `idle in transaction`(밖 [e] + 문서 autobegin·reset on return — 02 「한 묶음 작업·취소」와 이음) · 프로세스 여럿 × 풀 합 ≤ `max_connections` 100(밖 [g] + PG 문서, 여러 프로세스는 실행 안 함) · `max_overflow=1`(밖 [h]) · `create_task` 타이밍(밖 [d]) · 노트북 밖 다섯 번 · 버전(문서 2.0.54 ↔ 설치 2.0.43). 옛 b4의 `pool_pre_ping`·`pool_recycle`·백프레셔·상위 백분위수는 실행하지 않아 뺌.
- 비유 계열 「전화 교환대」 이어 씀: 교환대 한 대 = 풀 크기 1인 연결 풀, 선 한 가닥 = 연결, 선반 받침 구멍에 세운 선 = 쉬고 있는 연결, 판 자리에 꽂힌 선 = 빌려 간 연결 · 왼쪽(꽂힌 채·받침 빔) = Before, 오른쪽(받침에 섬·판 빔) = After · 「비유와 다른 점」: 01의 불(서버와 이어진 연결)은 그리지 않음 — 실제 연결은 어디에 있든 서버와 이어져 있음.
- 도구 파일: 만들지 않음(챕터 공통 8 S1 — `ask_database`는 전역 `engine`·`ask_sql`에 기대는 이 절 전용).

## 문서 대조 (재개 작업자 WebFetch 2026-09-29 — 문서 SQLAlchemy **2.0.54** · Python **3.14.7** · PostgreSQL 17, 설치는 sqlalchemy 2.0.43·Python 3.12.13·서버 17.11)

- SQLAlchemy Connection Pooling — 기본값 `pool_size` 5·`max_overflow` 10·`pool_timeout` 30.0 · `pool_timeout` 「The number of seconds to wait before giving up on returning a connection」 · `close()` 「Instead of the DBAPI connection being closed, it is returned to the pool」 · `create_async_engine()` → `AsyncAdaptedQueuePool` · 쓰레기 수거 반납 「not supported with asyncio DBAPI drivers」 · `status()` 「a brief description of the state of this pool」.
- Error Messages `3o7r` — 흔한 까닭 「failing to release these connections and is instead leaving them open」 · 쓰레기 수거 반납은 「cannot be relied upon」 · 고치는 법 `.close()`·context manager.
- Core Exceptions — `TimeoutError` 「Raised when a connection pool times out on getting a connection」, bases `SQLAlchemyError`.
- Working with Engines and Connections — autobegin(첫 `execute`에서 한 묶음 작업 시작) · Reset On Return(반납 때 `rollback()`).
- Python Tutorial 8.3 — 「matches exceptions which are instances of the class itself or one of its derived classes (but not the other way around …)」 · Built-in Exceptions — `TimeoutError` 「timed out at the system level」, `OSError` 하위.
- PostgreSQL 17 `max_connections` — 「The default is typically 100 connections」·서버를 켤 때만 정함.
- 설치판 소스(sqlalchemy 2.0.43 — `.cache/vm/venv-ch31-database`): `pool/impl.py` 74~76행(기본값 5·10·30.0)·151~171행(`_do_get` — 대기 제한 동안 기다리고 오류 글·코드 `3o7r`)·230~256행(`status`·`size`·`timeout`·`checkedin`·`overflow`·`checkedout` = `maxsize - qsize + overflow`)·259행(`AsyncAdaptedQueuePool`) · `exc.py` 287~288행 · `ext/asyncio/engine.py` 475~482행(`close()`가 열린 한 묶음 작업도 취소)·894~896행(`__aexit__` → `close()`) · `pool/base.py` 1016~1025행(쓰레기 수거 경고 글). 재개 메모의 「892~896」은 891행 `__await__`까지 걸친 범위라 본문에는 **894~896**으로 적음. 문서와 설치판 출력이 어긋난 곳은 찾지 못함(기본값·오류 글 모양 같음).

## 실행 (새 커널)

- 첫 실행 전 `/tmp/ch31-04/try/copy1.ipynb` 사본을 `runcopy.sh`(훅 source + `execute.py --cwd` 프로젝트 맨 위)로 PASS 21셀 — 실습 폴더에 `.failure.json`이 남지 않게. 출력은 설계(재개 메모)와 같음.
- **A**: `env -u OPENAI_API_KEY PYTHONDONTWRITEBYTECODE=1 timeout 170 bash run_section.sh textbook/part7/ch31-database 04` — 프로젝트 맨 위 커널, **`executed_at` 2026-09-29T18:54:00Z**, PASS 21셀(그림 첨부 단계에서 멈춤 — 04-1 PNG가 아직 없어서, 실행·저장은 끝난 뒤) · `code_sha256` **`d919bdcdd61a9254a90dbe2b5fbb60a80458210c94df0899dc61e0a6f1f4572c`** · `outputs_sha256` **`1673bbd94b671b0e41a5d6e5193a246c806efb9a3a4851a223e6975d525125f8`**.
- **B**(그림 전): 저장 노트북 사본 `/tmp/ch31-04/runB/04B.ipynb`를 `--cwd labs/part7/ch31-database/notebooks`(학생 커널 자리) · `executed_at` 18:54:09Z · PASS 21셀 · `code_sha256` 같음 · **`outputs_sha256`도 A와 같음**.
- **셀별 출력 글자 대조(`cmpout.py`): 21개 모두 같음.** 흔들리는 값 없음 → 결과 읽기에 `[[…]]` 자리 없음. 그림 첨부 뒤 저장 노트북도 A와 셀별 21개·해시 같음. 생성기 `cells()`(`split_part_boundaries` 뒤 47셀)와 저장 노트북 셀 소스 47개 모두 같음.
- 모든 셸 호출 뒤 postgres 프로세스 0·55431 포트 0 · 서버에 남긴 것 0(끝에 확인: 이름 공간 `public`만, 확장 `plpgsql`만, 데이터베이스 `ch31_lab`·`postgres`).
- 실습 폴더 파일 고침 **0**: `app/`·`migrations/`(맥 pyc 포함)·`alembic.ini`·README·`pyproject.toml`·`uv.lock` 17개 sha256을 03의 기록 `/tmp/ch31-03/lab-before.sha`와 대조 — 17/17 같음 · 실습 폴더에서 바뀐 파일은 노트북 04뿐 · pyc 0 · `.failure.json` 0.

## 고친 틀린 사실

1. After 「연결을 일찍 반환하고 대기 제한을 조정한 뒤 두 작업의 성공」(설정값을 바꾼 것 — 결함 코드를 고친 것 아님) → 같은 설정에서 닫지 않은 연결을 닫고 `async with`로 빌려 같은 다음 요청이 이름을 받음 · 대기 제한만 늘리면 같은 오류(`timeout 1.00`).
2. `from sqlalchemy.exc import TimeoutError`(이름 가림) → `sqlalchemy.exc.TimeoutError`, 파이썬 `TimeoutError`와 다른 종류임을 출력으로.
3. b6 「Docker의 독립 PostgreSQL 17.8 … 시간과 실행 계획」 → 이 절은 시간·계획을 재지 않음, 교재 출력 버전 17.11(Docker 없이 같은 접속 글).
4. b4·b7의 `pool_pre_ping`·`pool_recycle`·백프레셔·상위 백분위수·「체크아웃 대기 시간 관찰」(실행 안 함) → 뺌. 풀 합과 `max_connections`는 노트북 밖에서 본 값·문서로 한정.
5. b8 「마지막 절에서는 … 인스턴스」 → 05절 제목과 맞게(검색 문서 표·체크포인터 표·백업과 복원).
6. 옛 그림의 보라(모델 아님)·빨강(풀 — 결함 결과 아님) → 보라 0, 빨강은 Before 결함 결과 두 상자만.

## 그림

- Mermaid **4장**(설계표 `04-figures.md`를 렌더 전에 씀): 04-1 연결을 빌리고 풀에 다시 넣기(b4·노트북 오늘 볼 그림, viewBox 폭 **266**) · 04-2 연결 하나를 빌린 채 둘째 빌리기(b5, **259**) · 04-3 닫지 않고 둔 연결의 Before(b6, **271**) · 04-4 닫지 않은 셀과 async with 셀 견주기(b6, **606**). 모두 868 이하 · `flowchart TB` · subgraph 제목 `<br>` 없음 · 라벨 대괄호·따옴표 없음 · 개수는 한글 · 노드 7개 이하(04-4가 7) · 노드 id `call`·`end` 없음 · `%% classes`. **첫 렌더에서 넷 모두 자동 줄바꿈**(`pool_size=1 · max_overflow=0`·`async with engine.connect()`·`SELECT current_database()`·`conn = await engine.connect()`·`풀 크기 하나 · 더 만들 연결 없음`) → `<br>`로 미리 나눠 다시 렌더, 04-2 `오류가 든 모듈 sqlalchemy.exc`도 한 번 더 나눔 · PNG 넷을 직접 열어 확인(다른 이름 사본 `.cache/ch31-04-view/` — 04-4는 Before 칸이 왼쪽). **보라 0 · 빨강 2상자(04-3 「다음 요청은 연결을 받지 못함 · 빌려 간 연결 하나 · 쉬고 있는 연결 없음」·04-4 Before 칸 「셀 뒤 빌려 간 연결 하나 · 쉬고 있는 연결 없음」 — 둘 다 Before 결함 결과)** · 받아 출력한 `TimeoutError`는 모든 그림에서 노랑 · 04-2의 「대기 제한 0.2초 동안 반납을 기다림」은 설치판 소스로 본 동작이라 회색(도식 읽기에 근거 적음) · 04-4 맨 위 회색 공통 상자는 두 셀 출력에서 모두 확인한 값만(같은 엔진·같은 SQL 글·`ch31_lab`).
- 삽화 1장 **04-5 판에 꽂힌 채인 선과 받침에 놓인 선**(b4 비유 뒤, 본문만): **1차 job `052be948-407a-46ae-86df-3eac09cf1869` 채택**(재생성 0회). 거래 2026-09-29T18:56:18.327904Z 「Nano Banana Pro −2」 한 줄 = **이 절 몫 2크레딧**(잔액 2253 → 2251, 바로 앞 거래 17:14:39Z는 03 — 앞 04 작업자 0). 작업 조회 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만). 원본 2752 × 1536 `e2d20dbe…` · 저장 PNG 1100 × 614 `7cdb516d…`, 결과를 다시 받아 같은 폭으로 줄인 그림과 **픽셀 차이 0**(bbox `None`). 그림에서 센 것: 짙은 남색 교환대 둘 · 판마다 흰 테두리 자리 하나 · 선반마다 받침 구멍 하나 · 겨자색 선 둘 · 왼쪽 선 끝은 판 자리에 꽂힘·받침 구멍 빔 · 오른쪽 선 끝은 받침 구멍에 섬·판 자리 빔 · 불·사람·손·글자·숫자·화살표·콘센트·전원 플러그 0. 거의 흰 가로줄 3/614. 세부 `figures/04-5-…prompt.md`.

## 검사

- 게이트 G1~G7 0(`gates-wip-04.json`, 검사 문장 400) · `verify.py --chapter` **PASS 5 sections / 103 code cells (max 25 lines)**(최대 25줄은 손대지 않은 05 옛 셀) · 빌드 HTML `04-커넥션-풀-고갈과-대응.html`의 `{{`·`[[` 0, `_src`의 `[[` 0(`{{`는 토큰 일곱뿐) · review-pack `qa/upgrade/review-pack/04-커넥션-풀-고갈과-대응.md`.
- 화면 검사 `visual.cjs`는 돌리지 않음(마감 몫).

## 완료 챕터·앞 절·뒤 챕터 문장 참·거짓 (고치지 않음)

- **03 노트북 정리 끝·b8** 「04절에서는 연결 풀에 빈 연결이 없을 때 무슨 일이 생기는지 봅니다」 — **참**(4절 첫째를 빌린 채 둘째 → `TimeoutError`, 5절 닫지 않은 연결 뒤 다음 요청 → `TimeoutError`).
- **01 설정 셀** — 04는 글자 그대로(생성기 대조). **02 b4** 「02절의 `풀에 둘 연결 수: 5`가 기본값」 — 04 b4가 인용(02 출력 그대로).
- **Ch 30 10 b8**(`_src`·HTML·노트북) 「Ch 31에서는 PostgreSQL 데이터베이스에 표를 만들어 쓰는 방법과 체크포인터를 다룹니다」·「05절은 체크포인터로 …」·「보낸 SSE 사건을 저장하는 방법은 Ch 31에서도 다루지 않습니다」 — 04에 SSE 0 **참**(체크포인터는 05 몫). **Ch 30 06 b7** SSE — 참.
- **Ch 16 05** — 04가 「재시도 함수는 `except TimeoutError`로 파이썬의 오류를 받았습니다」라고 기댐: Ch 16 05 노트북 `retry_with_fallback`의 `except TimeoutError:`·실패 흉내 `raise TimeoutError(…)` **참**.
- **Ch 30 02** — 04 b3 「첫 테스트가 적은 재정의를 지우지 않아, 다음 테스트까지 504 … 비우자 200」: Ch 30 02 b8 「첫 테스트가 남긴 재정의로 다음 테스트도 504를 받았고, 딕셔너리를 비우자 200이 왔습니다」 **참**.
- **Part 7 목차** 「Ch31의 데이터 저장」 참 · **Ch 32 04 b3**(대기) 「Ch31에서는 PostgreSQL, 트랜잭션, 인덱스와 pgvector」 — 04 무관 · `grep -rn 'Ch *31'`(Part 1·2·3·5·6·7 HTML, ch31 밖): Part 7 목차 둘·Ch 30 06·10·Ch 32 04와 옛 판 사본(`before/`)뿐 — **04에 기대는 문장 없음**. `labs/part7/continuity-guide.md`의 「연결 풀」은 마감 대조.

## 챕터 밖 수정

- 없음. (공용 도구·Part 7 파일·다른 챕터 파일 0. `textbook/_notebook/checks/notebook-contracts-part7-ch31-database.json`은 `verify.py --chapter`가 다시 쓴 챕터 계약 파일.)
- 실습 폴더 파일(`app/`·`migrations/`·`alembic.ini`·`README.md`·`pyproject.toml`·`uv.lock`) 고침 0.

## 강사 확인 대상

1. **말**: 절 제목의 「커넥션 풀」·「고갈」은 제목에 두고 본문 첫 자리에서 풂(「01절에서 본 연결 풀」·「빌려 줄 연결이 없다」) · `pool_timeout` = 「대기 제한」 · 「반납」 · 「이름 가림」 · 이 절도 패키지·서버 번호를 「버전」으로(03과 같게, 01·02는 「판」).
2. **After가 설정을 바꾸지 않음**: 옛 판은 대기 제한을 늘려 성공시켰으나, 개선본은 같은 설정에서 반납으로 고치고 대기 제한 늘리기는 값 바꿔 보기(여전히 실패)로 보임 — 절의 결론이 「대기 제한을 늘리는 것은 대응이 아니다」 쪽으로 바뀜.
3. `create_task`로 두 작업을 함께 돌리는 옛 장면은 노트북에서 빼고 b7에 노트북 밖 확인으로만 둠(타이밍에 기댐) — Ch 2 12 전제 금지 목록의 `create_task` 첫 풀이는 b7 한 문장.
4. 코드 양: 코드 셀 4 → 21, 코드 줄 39 → 98(paired 한 절 — 예시·Before·After·값 바꿔 보기·정리, 다음 요청 셀 세 곳 같은 코드).

## 남은 것 (마감 몫)

- 옛 그림 `figures/04-흐름.{svg,excalidraw,caption.md}` 삭제 승인 목록(본문은 더 쓰지 않음) · README의 04 설명(마감 — 01 진단과 같음) · `labs/part7/continuity-guide.md` 연결 풀 줄 대조.

## 지우지 않은 것 (삭제 승인 대상 — 이 절이 만든 것)

- 기기 `/tmp/ch31-04/`(약 7.7MB — `exp/`(앞 작업자 확인 스크립트 둘·출력, 재개 확인 출력 `r_1`·`r_2`)·`tools/`(03 도구 사본 열셋)·`gen/`(생성기 조각 넷·`all.py`·`edit.py`·치환 JSON 셋·설계표·진단·그림 초안)·`pre/`(pregate 임시 노트북·`src.html`)·`try/copy1.ipynb`·`runA/`·`runB/`·`illu/`(`r1.png` 원본·`r1-again.png`·`r1-1100.png`)) · 연결 폴더 `.cache/ch31-04-view/`(PNG 열둘 — 첫 렌더 넷·다시 렌더 둘·최종 둘·삽화 둘 등, 약 2.1MB) · `.cache/ch31-04/resume/`·`.cache/ch31-04/exp/`(앞 작업자 재개 자료 — 그대로 둠) · `qa/upgrade/gates-wip-04-04.json`·`gates-wip-04.json`.
- 앞 절이 남긴 `/tmp/ch31-02/`·`/tmp/ch31-03/`·`.cache/ch31-0[123]*`, 공용 `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/libs`·`/tmp/npm-cache`·`/tmp/uv-cache`·`/tmp/ch31-pg/`는 건드리지 않음.

## 디스크

- 기기 루트 여유: 작업 전 **2.0G** → 끝 **2.0G**(`/tmp/ch31-04` 7.7MB) · 세션 디스크(`/sessions`) 831M → 830M · 사용자 디스크(연결 폴더) 여유 74G → 74G(이 절이 연결 폴더에 더한 것은 3MB 남짓).

## 보호 파일 (`before-manifest.json` 209개)

- 04절 뒤 대조 결과는 `manifest-changes.md` 「04절 뒤」.
