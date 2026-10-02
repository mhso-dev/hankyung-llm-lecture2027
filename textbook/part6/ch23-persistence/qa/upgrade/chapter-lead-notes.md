# Ch 23 Persistence와 Durable Execution — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part6/ch23-persistence`(절 여섯 — 01·03·04·05 experiment, 02·06 paired) · `labs/part6/ch23-persistence`. Part 6의 세 번째 챕터이고 완료 Ch 21·Ch 22 바로 뒤입니다.
- 준비 산출물: `qa/upgrade/before/`(원본 사본 45개) · `gates-before.json` · `before-manifest.json`(123개) · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch23-persistence`.
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(전부) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 과정 요약(전부) · 계약 파일(§3 Ch 20·21 줄, §4 Ch 16~21 줄, §5 Ch 16~21 줄, §8) · Ch 21 `chapter-summary.md`(§1·§2·§13~17)·`chapter-lead-notes.md`·`before-manifest.json` · Ch 20 02·03 `_src` 링크 문장 · Ch 21 03·07·Ch 22 09 `_src`의 Ch 23 문장 · 뒤 챕터(Ch 24~27·30·31) `_src`의 Ch 23 문장 · Ch 4 03·Ch 12 02·Ch 16 05·Ch 31 05 노트북 코드 · 옛 생성기 둘 · Part 6 목록·묶음·검사 스크립트 · `ch23-technical-review.md`·챕터 `qa/research.md`·`verification.md`·`집필점검표.md`.
- **원고·노트북·그림은 하나도 고치지 않았습니다.** 연결 폴더 안 파일 삭제 0건. 모델·임베딩 호출 0건(이 챕터는 원래 모델을 부르지 않음). 노트북 실행 0건. 한 확인은 모두 모델 없이 했습니다: import, 설치판 소스 읽기, `/tmp/ch23-prep/exp/`의 작은 그래프, 옛 worker 둘을 `/tmp` 경로로 되풀이 실행(04 worker 60번, 06 worker 20번), `/tmp`의 임시 PostgreSQL 클러스터로 옛 02 흐름 한 번(§5-4). 키는 `env -u OPENAI_API_KEY`로 뺀 채 돌렸습니다.
- `chapter.json` `hours` = 「총 16h · 강의 6h · 실습 10h」. 절 meta 합 강의 1 × 6 = **6h**, 실습 1.5 + 1.5 + 1.5 + 2 + 1.5 + 2 = **10h** → 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part6/_build_index.py` 21행 (6, 10)·`qa/check_scope.py` `EXPECTED` (6, 10)도 같습니다. 새 용어 meta 3 + 3 + 3 + 4 + 3 + 3 = **19**(용어 목록은 원고에 없음).

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-25)

| 절 | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 체크포인터와 스레드 | 4 | 75 | 0 | 1 | 0 | 0 | 6 | 22 | 3 | 32 |
| 02 PostgresSaver 준비와 스키마 | 4 | 77 | 2 | 1 | 0 | 0 | 6 | 28 | 3 | 40 |
| 03 스레드 재개와 대화 이어가기 | 5 | 76 | 2 | 2 | 0 | 0 | 6 | 12 | 3 | 25 |
| 04 내구 실행 모드 비교 | 6 | 83 | 7 | 3 | 0 | 0 | 4 | 27 | 3 | 44 |
| 05 pending writes와 장애 복구 | 5 | 83 | 5 | 4 | 0 | 0 | 5 | 19 | 3 | 36 |
| 06 노드 재시작과 멱등성 | 5 | 79 | 3 | 3 | 0 | 0 | 5 | 14 | 3 | 28 |
| **합계** | **29** | **473** | **19** | **14** | **0** | **0** | **32** | **122** | **18** | **205** |

- 통과 절 **0/6**. 코드 줄(`count_code.py labs/part6/ch23-persistence/notebooks`) 32·41·36·48·53·38 = **248줄**. 설치 셀(1줄)은 여섯 절이 같은 주석이고, 03~06 경로 셀(`candidates = [Path.cwd(), *Path.cwd().parents]` + `next(… for p in …)` 네 줄)이 글자까지 같게 되풀이됩니다.
- G1 19 = 제너레이터 식 9(03·05·06 경로 셀 2씩 · 04 경로 셀 2 + c10 `all(…)` 1) · `lambda` 2(02 c4 노드 `lambda state:` · 05 c4 리듀서 `lambda left, right:`) · 내포식 3(02 c8 표 이름 · 04 c10 `observations` · 05 c8 `tasks` 출력) · 조건 표현식 2(04 c6 `read_saved`·c12) · 긴 함수 2(04 `kill_and_resume` · 06 `interrupt_then_resume`, 둘 다 17줄) · 셀당 함수 셋 1(05 c6 `record`·`good`·`flaky`).
- G2 14 = 15줄 넘는 셀 6(01 c4 · 02 c4 · 04 c8 · 05 c4 · 05 c6 · 06 c6) · 한 글자 이름 `p` 8(경로 셀 넷 × 2).
- G3 0 — 그러나 **29셀 모두 주석이 첫 줄 한 줄뿐**입니다(옛 생성기 `CODE_COMMENTS`가 끼운 글, 이유 주석 0).
- **G4 0은 모델 셀이 없어서입니다**(여섯 절 모두 모델·임베딩 요청 0, 키 셀 0).
- G5 32 = 절마다 `title_cell_missing`·`core_figure_attachment_missing` 12 + 결과 읽기 인용 없음 14 + 마지막 코드 셀 뒤 결과 읽기 없음 6(결과 읽기 셀 자체가 0).
- G6 122 = 70자 초과 44 · 영문으로 시작해 조사가 붙은 문장 78. 금지어는 G6가 대부분 세지 않습니다(§1 표 금지어 열).
- G7 18 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 것 (AST로 따로 셈, 스크립트 `/tmp/ch23-prep/ast_scan.py`)

- **f-string**: 계산이 든 것 3(02 c6 `f"{type(exc).__name__}: {exc}"` · 03 c6 `f"답변 {len(state['turns'])}"` · 04 c12 `f"{row['mode']:5} -> …"` — **형식 지정 `:5`**) · 변수만 7(04 c8 `f"{mode}.sqlite"` 등 · 06 c6 셋).
- **타입힌트**: 노드·도움 함수 모두 매개변수 힌트 + 반환 힌트(01 `add(state: State) -> dict` · 03 `respond` · 04 `read_saved(db_path: Path, mode: str) -> dict | None`·`kill_and_resume(mode: str) -> dict` · 05 `record(name: str) -> None`·`good`·`flaky` · 06 `interrupt_then_resume(strategy: str) -> list[str]`). **Ch 13 노드 46개·Ch 20 노드는 힌트 0**(Ch 20·21은 `@tool` 매개변수 `: str`만).
- **클래스**: 상태 형식 `class State(TypedDict)` 넷(01·02·03·05) — Ch 13 L5 범위(칸만). 04·06은 worker 파일 안에 있음.
- **`with`**: `with sqlite3.connect(…) as conn:`(03 c8·c10 · 04 c6) · `with psycopg.connect(…)`(02 c4·c8) · `with PostgresSaver.from_conn_string(…) as saver:`(02 c6·c8) · `with trace_path.open("a")`(05 c6). 과정은 `with open(…)`(Ch 2 05)과 Ch 21 04 `warnings.catch_warnings`만 가르쳤고 Ch 4 03·Ch 12 02는 연결을 `connect()` → `close()`로 열고 닫았습니다.
- **예외**: 02 c6 `except Exception as exc`(너무 넓음 — 과정은 이름 하나를 받음) · 05 c8 `except RuntimeError as exc`.
- **처음 쓰면 풀어야 하거나 과정이 안 쓴 이름**: `[Path.cwd(), *Path.cwd().parents]`(별표 풀기)·`next(…)`(규격 §2-3 금지 모양) · `subprocess.Popen`(과정에서는 Ch 4 준비 셀 예외에서만)·`process.kill()`·`process.wait(timeout=5)`·`subprocess.run(…, check=True, capture_output=True, text=True, timeout=20)`·`sys.executable` · `time.time()` 기한 루프·`time.sleep(0.02)` · `Path.unlink(missing_ok=True)`·`mkdir(parents=True, exist_ok=True)`·`stat().st_size`·`with_suffix`·`read_text().splitlines()`·`write_text` · `os.getenv("CH23_POSTGRES_URI", …)` · `dict.get("completed", [])` · `all(…)` · `sorted(…)`·`bool(…)` · `is None` 비교.
- **worker 파일 둘**(학생이 여는 모듈): `from __future__ import annotations` · 한 줄 다중 대입 `db_path, ready_path, mode = Path(…), Path(…), sys.argv[3]` · 조건 표현식 둘씩 · 반환 힌트(durability 둘) · `class State(TypedDict)` · 모듈 독스트링 영어. 코드 줄 36·31.

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 요청 | 외부 서비스 | 파일 쓰기(옛 판) | 손 값 | 금지 문법(셀) | 금지어(`_src` 본문 / 노트북 md / 코드 주석) | `assert`(무엇에) |
|---|---|---|---|---|---|---|---|---|
| 01 | `InMemorySaver`를 붙인 한 노드 그래프(`total`에 `events[-1]`을 더함, 리듀서 없음) · `thread_id` `customer-a`에 3 → 4를 넣어 `total` 3 → 7 · `get_state`의 `values`·`next ()` · `customer-b`에 4 → 4 · 기록 수 6 ↔ 3 | 0 | 없음 | 없음(메모리) | 입력 3·4 · 스레드 이름 둘 | c4 15줄 넘음·힌트 | 반환 3/2/0 · 식별자 3/2/0 · 스냅샷 4/1/0 · 채널 1 · 경로 1 · Store 1/1(실행 안 함) · 스키마 1/1 | 1 — `second['total'] == 7 and other['total'] == 4`(결정적) |
| 02 | 새 스키마 `ch23_lab`(`DROP SCHEMA … CASCADE` 뒤 새로) · Before `setup()` 없이 `PostgresSaver.from_conn_string(uri)` → `UndefinedTable: relation "checkpoints" does not exist` · After `setup()` 뒤 `{'value': 12}`와 표 넷(`checkpoint_blobs`·`checkpoint_migrations`·`checkpoint_writes`·`checkpoints`) | 0 | **PostgreSQL 필수**(Docker `postgres:17`, `postgres:postgres@localhost:55432/postgres`, 환경 변수 `CH23_POSTGRES_URI`로 바꿀 수 있음) | DB 스키마 `ch23_lab` | 값 6 · 스키마 이름 · 접속 글 | c4 `lambda` 노드·15줄 넘음 · c6 f-string 계산·`except Exception` · c8 내포식 | 스키마 15/7/1 · 마이그레이션 6/2 · 검증 2/1 · 반환 2 · 경로 2 · 트랜잭션 1 · 로그 1/1 · 원문 1/1 · **제목 「PostgresSaver」·「스키마」** | 2 — `'UndefinedTable' in before_error`(서버가 있을 때만 결정적) · 값 12·표 이름(결정적) |
| 03 | `SqliteSaver` + 리듀서 `operator.add`(`turns`) · 첫 `with sqlite3.connect` 블록에서 질문 1 → `['질문 1', '답변 1']` · 파일 크기 `4096` · 둘째 블록(새 연결·새 그래프 객체)에서 질문 2 → `['질문 1', '답변 1', '질문 2', '답변 3']` | 0(「답변 N」은 노드 함수가 만든 글) | 없음 | `labs/…/data/thread-resume.sqlite`(+ `-wal`·`-shm`), 매번 `unlink` | 질문 글 둘 · 스레드 이름 | c4 제너레이터 둘·`p` 둘 · c6 f-string 계산·힌트 | 리듀서 6/4/1 · 로그 1/4 · 반환 2/1 · 채널 3 · 경로 2 · 인터페이스 1/1 · 모사 1 · 「SQLiteSaver」(틀린 이름) 1 · 「설치 부담」 1 | 1 — 목록 전체 같음(결정적) |
| 04 | `durability_worker.py`(first → second, second에 들어가면 ready 파일을 쓰고 30초 잠) · 부모가 ready를 보면 `kill()` → SQLite `get_tuple`로 저장값 → 같은 worker를 `resume`으로 다시 실행 · 모드 셋 `exit`·`async`·`sync` | 0 | 없음(자식 프로세스) | `data/durability/{모드}.{sqlite,ready,trace}` + worker가 쓴 SQLite | 30초 · 기한 20초 · 확인 간격 0.02초 | c4 제너레이터 둘·`p` 둘 · c6 조건 표현식·힌트 · c8 긴 함수(17줄)·15줄 넘음·f-string · c10 내포식·제너레이터 · c12 조건 표현식·f-string 형식 지정 | 지연 3/2 · 경합 1/1 · 측정 1 · 보장 2/1 · 내부 2 · 「정확히 한 번」 2 · 「SQLiteSaver」 1 · 병렬 1 · durability 3 | 4 — `ready.exists()` · exit `before is None`(결정적) · sync `before`에 first(결정적 — 코드 주석은 `observations[2]` = sync) · 셋 모두 재개 뒤 `['first', 'second']`(결정적) |
| 05 | `InMemorySaver` · START에서 `good`·`flaky`가 같은 단계로 갈라짐 · 리듀서 `lambda left, right: left + right` · `flaky`가 허용 파일이 없으면 `RuntimeError` · `snapshot.tasks` 출력 → 허용 파일을 쓰고 `invoke(None, config)` → 호출 `good` 1·`flaky` 2 | 0 | 없음 | `data/pending-trace.txt`·`data/allow-flaky`, 매번 `unlink` | 이름 둘 · 오류 글 | c4 제너레이터 둘·`lambda`·`p` 둘·15줄 넘음 · c6 함수 셋·15줄 넘음·힌트 · c8 내포식 | superstep 8/2/1 · 병렬 5/6/1 · 반환 3/1 · 로그 4/4 · 런타임 3 · 트랜잭션 1/1 · 채널 1/1 · **제목 「pending writes」** | 3 — 호출 수 둘·결과 목록(모두 결정적) |
| 06 | `idempotency_worker.py`(`charge` 노드가 로그 파일에 `order-2306`을 쓰고 ready를 쓴 뒤 30초 잠, `durability="sync"`) · 부모가 `kill()` → `resume` 실행 · Before `naive`(검사 없이 추가) 2줄 · After `idempotent`(이미 있으면 건너뜀) 1줄 | 0 | 없음(자식 프로세스) | `data/idempotency/{전략}.{sqlite,log,ready}` | `order-2306` · 30초·20초 | c4 제너레이터 둘·`p` 둘 · c6 긴 함수(17줄)·15줄 넘음·힌트 | 원자적 5/1 · 반환 6 · 경로 6/0/1 · 로그 8/1/1 · 재시작 6/1 · interrupt 1(Ch 24 말) · 보장 1/1 | 3 — `ready.exists()` · 줄 수 2 · 줄 수 1(결정적) |

- **서비스 요청 합계 0**(모델 0 · 임베딩 0). 노트북 `%pip` 셀: 01 `langgraph==1.2.11` · 02 `+ langgraph-checkpoint-postgres==3.0.5 'psycopg[binary,pool]==3.3.3'` · 03~06 `+ langgraph-checkpoint-sqlite==3.0.3`. 실습 폴더 dev에 `pip==26.2`, 잠금에 `pip 26.2` 있음(규격 §7-2 조건 충족).
- **`temperature=0`·`reasoning_effort="none"`**: 모델 셀이 없어 해당 없음.
- **걸린 시간**: 어느 절도 재지 않습니다(04·06의 `time.time()`은 20초 기한 루프). 그런데 04 b2·b4·b5 둘째 단락이 「다음 노드가 기다리는 시간이 늘어날 수 있습니다」·「지연을 줄일 수 있지만」·「비동기 저장의 지연 이점」을 씁니다 → 규격 §3 「재지 않은 시간 단정 금지」와 부딪힘(§9-7).
- **옛 그림 토큰**: 절마다 b4 「도식 읽기」의 `{{svg:NN-흐름}}` 하나(`figures/_gen_figures.py`가 `textbook/part5/_figure.py`로 만든 상자 네다섯 줄 흐름도). 노트북 토큰은 01·03·04·05 `{{notebook:slug}}` · 02·06 `{{notebook:slug|example}}`+`{{notebook:slug|failure}}`. Mermaid·삽화 0장.
- 노트북 `metadata.verification`: 여섯 모두 `passed`, 실행일 **2026-09-10**(16:18:27~16:18:35 UTC, macOS 판 `.venv`로 보임 — 03 출력 `<langgraph.graph.state.StateGraph at 0x109c9e150>`). `code_sha256` 앞 12자 01 `df01e4e474e1` · 02 `f7073854c242` · 03 `1ca6b5d44021` · 04 `c7e6ff55b8c4` · 05 `b19b09a2fb81` · 06 `02b6cf506a77`. 노트북 파일 해시 `3e3ac6c1…`·`17b9af07…`·`7a23d759…`·`b76842ea…`·`8ee4cd8c…`·`767959df…`(`part6-practice.zip` 안 판과 같음).
- 노트북 설명 셀: 제목 + 한 줄 · 「실행 환경 준비」 · 소제목 한 줄 + `_src` b4·b5 둘째 단락과 같은 글(옛 도구 `part6a_enrich.py`가 끼움) · **결과 읽기 셀 0**, 「이 노트북에서 할 일」·준비물·실행일 문장 없음, 셀 첨부 그림 0.
- `_src` 틀(옛 생성기 `author_ch23_ch24.py` 한 틀): b5 「확인할 점」 = b6 둘째 단락(같은 글 두 번) · b8 「다음 학습과 이어지는 지점」 · b9 복습 넷, 해설 한 줄 · **b10 참고 자료 넷이 여섯 절 모두 같음**(Persistence · Interrupts · Time Travel · LICENSE, 확인일 2026-09-14) — Interrupts·Time Travel은 Ch 24 주제이고 durability 정의 문서(`reference.langchain.com/…/Durability`)는 빠짐.

## 2. 절별로 더 봐야 할 것

### 01 체크포인터와 스레드
- 결과는 모두 결정적입니다(설치판에서 다시 돌림). `get_state_history`는 최신 것부터 단계 `4 loop ()`·`3 loop ('add',)`·`2 input ('__start__',)`·`1 loop ()`·`0 loop ('add',)`·`-1 input ('__start__',)` — 기록 수 6 = 실행 둘 × 셋. 없는 스레드의 `get_state(…).values`는 `{}`, `next`는 `()`(다른 스레드 장면을 코드 쪽 사실로 보일 수 있음).
- 상태 칸 `events`는 리듀서가 없어 덮어씁니다. 둘째 실행에 `{"events": ["4"]}`만 넣어도 `total`은 저장된 3에서 이어집니다 — 「체크포인터가 칸을 합치지 않는다」는 Ch 13 02 리듀서(덮어쓰기)로 풀 수 있음.
- 설정 딕셔너리 `{"configurable": {"thread_id": …}}`는 Ch 20 03 설정 딕셔너리(`{"recursion_limit": N}`)와 같은 자리입니다. 과정에서 `configurable`은 처음.
- b5 둘째 단락 「Store는 여러 스레드가 공유할 사용자 선호 …」 — Store는 과정·이 챕터 모두 실행하지 않음(「이번에 실행하지 않았습니다」 대상).
- **이 절을 링크하는 완료 문장**: Ch 20 03 b7 「실행 중 상태를 저장해 두는 체크포인터는 Ch 23 01절에서 다룹니다」 → 01이 체크포인터를 처음 가르치는 한 참. Ch 21 03 b4·b7·07 b7 「결과 상태를 저장해 다음 실행에 이어 쓰는 방법은 Ch 23에서 배웁니다」 → 3 → 7 장면으로 참.

### 02 PostgresSaver 준비와 스키마
- **옛 판은 실제 PostgreSQL에 접속합니다**: `base_uri = os.getenv("CH23_POSTGRES_URI", "postgresql://postgres:postgres@localhost:55432/postgres")`, 스키마는 URI 뒤 `?options=-csearch_path%3Dch23_lab`. 서버는 실습 폴더 README의 Docker(`docker run --name kdt-ch23-postgres -e POSTGRES_PASSWORD=postgres -p 55432:5432 -d postgres:17`). 잠금에 `langgraph-checkpoint-postgres 3.0.5`·`psycopg 3.3.3`·`psycopg-binary 3.3.3`·`psycopg-pool 3.3.1` 있음(이 기기 aarch64에 설치됨, libpq 18).
- **b3 「Ch4에서 PostgreSQL 스키마와 information_schema.tables를 조회했습니다」는 틀림.** Ch 4 03은 SQLite(`sqlite3.connect`·`CREATE TABLE`·`SELECT … JOIN … WHERE ? … ORDER BY`·`fetchall`·`close`)이고 `information_schema`는 과정 전체에서 Ch 23 02·Ch 31 05에만 있습니다. PostgreSQL·psycopg는 **Ch 12 02**(`psycopg.connect(database_url, autocommit=True)`·`cur.execute`·`fetchone`·`except psycopg.Error as error`·`error.diag.message_primary`, Docker `pgvector/pgvector:0.8.2-pg17`, **같은 호스트 포트 55432**).
- **포트 충돌**: Ch 12 컨테이너(`hankyung-part3-pgvector`)와 Ch 23 컨테이너가 모두 55432를 씁니다. Ch 12 컨테이너를 켜 둔 학생은 `port is already allocated`로 막힘. Ch 31은 55431. 판도 셋(Ch 12 psycopg 3.3.5 ↔ Ch 23 3.3.3, 이미지 `pgvector…pg17` ↔ `postgres:17`).
- Before 결함(`setup()` 누락 → `UndefinedTable`, 오류 종류 `psycopg.errors.UndefinedTable` → `ProgrammingError` → `DatabaseError` → `Error`, sqlstate `42P01`)은 **서버가 있으면 실제로 일어나는 결정적 결함**입니다(§5-4 재현). 서버가 없으면 같은 셀이 `OperationalError … Connection refused`로 멈춤 — 다른 결함.
- b4 「setup()은 … 표를 생성하거나 필요한 마이그레이션을 적용」·b7 「CREATE INDEX CONCURRENTLY」·「autocommit=True와 row_factory=dict_row」는 설치판과 맞음(§5-4). b6 「PostgreSQL이 … 반환한 오류」(금지어), b5 「로컬 postgres:17 컨테이너」.
- 소스 사실: `PostgresSaver.setup()` 독스트링 「It MUST be called directly by the user the first time」 ↔ `SqliteSaver.setup()` 「It is called automatically when needed and should not be called directly by the user」. **표 구조가 다름**: SQLite는 `checkpoints`·`writes` 둘(값을 체크포인트 칸 안에 담음), PostgreSQL은 넷(`checkpoint_writes`·`checkpoint_blobs`·`checkpoint_migrations` 따로). 「SQLite로 같은 표 구조를 보인다」는 쓸 수 없고 「이름이 다른 짝(`writes` ↔ `checkpoint_writes`)」까지만 참.
- **Ch 31 05(대기)** b3 「Ch23에서는 PostgresSaver의 `setup()`이 체크포인터 표를 만든다는 점을 확인했습니다」 → 02가 PostgreSQL을 실행하지 않으면 「소스로 봤다」 수준이 됨(인계). Ch 31 05 노트북은 Docker(55431)로 같은 `setup()`·표 조회를 다시 함.

### 03 스레드 재개와 대화 이어가기
- **모델이 없습니다.** 「답변 N」은 노드 `respond`가 `f"답변 {len(state['turns'])}"`로 만든 글입니다(가짜 모델 클래스는 아님 — 일반 노드 함수). 결과 목록은 결정적.
- **`with sqlite3.connect(…) as conn:`은 연결을 닫지 않습니다**(블록 뒤 `conn.execute("SELECT 1")`이 됨 — 확인). 파이썬 `sqlite3` 연결의 `with`는 확정(commit)·되돌리기만 합니다. 그래서 b5 「첫 with 블록에서 … 연결을 닫습니다」·노트북 c8 주석 「연결을 닫습니다」·b8 「정상 종료한 연결을 바꾼 경우」·복습 1은 사실과 다릅니다. 닫는 방법: `conn.close()`(Ch 4 03·Ch 12 02 모양) 또는 `SqliteSaver.from_conn_string(경로)`(설치판 `contextlib.closing`으로 닫음 — 확인).
- **`database bytes: 4096`은 오해를 부르는 값**입니다. `SqliteSaver`가 `PRAGMA journal_mode=WAL`을 켜서 저장 내용은 `-wal` 파일(이번 확인 65,952바이트)에 있고, 닫은 뒤에야 본 파일이 20,480바이트가 됩니다.
- **이 기기에서는 옛 판 그대로 실행되지 않습니다**(§9-2): 연결 폴더 안에서 SQLite 쓰기가 `sqlite3.OperationalError: disk I/O error`로 멈춤(확인 — 삭제가 막힌 폴더라 저널 파일을 지우지 못함). `db_path.unlink(…)`도 두 번째 실행부터 막힘.
- b3 「SQLiteSaver」(틀린 이름)·「모사」·「설치 부담을 줄이기 위해」 · b4 「리듀서가 없으면 새 turns 값이 이전 목록을 덮어씁니다」(Ch 13 02 덮어쓰기와 같음 — 참).
- **Ch 22 09(완료) b8** 「Ch23에서는 대화 기록을 프로그램 밖에 저장하고 다시 이어 가는 방법을 다룹니다. 이번 실습에서 종류별로 출력한 대화 기록이 그 대상입니다.」 — 「종류별로 출력한 대화 기록」은 메시지 목록(Human·AI·Tool)입니다. 지금 03은 글 목록 `turns`만 저장합니다. 메시지 칸(`add_messages`·`HumanMessage`·`AIMessage`, Ch 13 04)으로 바꾸면 그대로 참이 되고, 글 목록으로 두면 「대화 기록을 저장해 이어 간다」까지만 참.

### 04 내구 실행 모드 비교
- 모드 정의(설치판 `langgraph/types.py` 89~95행): `sync` 「persisted synchronously before the next step starts」 · `async` 「asynchronously while the next step executes」 · `exit` 「only when the graph exits」. **기본값은 `async`**(`pregel/main.py` 2602~2603행). 옛 판은 기본값을 말하지 않음.
- **옛 worker를 `/tmp` 경로로 60번 돌린 결과(§7-1)**: `exit` 20/20 `before=None`·호출 `first, second, first, second` · `sync` 20/20 `before=['first']`·호출 `first, second, second` · **`async` 56/60 `['first']`, 4/60 `first` 결과를 잃음**(호출 `first, second, first, second`). 옛 교재 출력(async = sync)은 흔한 쪽이지만 매번 같지 않습니다 → 규격 §2-7 9번 끝: async 값은 둘째 단락·「이번 실행에서는」에만.
- `exit` 모드는 **노드 안 예외로 멈출 때도 끝나며 저장합니다**(`pregel/_loop.py` 1324~1333행 `__exit__` — 오류가 있어도 `_put_checkpoint`·`_put_pending_writes`). 그래서 「실패 흉내」(예외)로는 `exit`의 손실이 안 보이고, **프로세스를 강제로 끝내야** 차이가 보입니다(§7-2 확인).
- **Ch 20 02(완료) b7이 「Ch 23 04절(강제 종료 뒤)」을 링크**합니다 → 04는 실제 강제 종료 장면을 지켜야 링크 설명이 참.
- 걸린 시간: 이 절 주제에 「느리고 빠름」이 들어 있지만 로컬 SQLite에서 20노드 그래프를 재면 `exit` 약 0.005초 · `async` 약 0.023초 · `sync` 약 0.024초(5번)로 async·sync 차이가 보이지 않았습니다(§7-3). 시간 비교를 결론으로 쓸 재료가 아님.
- worker가 30초를 자므로 부모가 `kill()`을 못 하면(기한 20초 초과) 셀이 `AssertionError`로 멈추고 자식이 30초 남음. 한 모드당 약 1.05~1.1초(자식 파이썬 시작 약 0.5초).
- b7 「정확히 한 번 실행을 보장하지 않습니다」·b6 「async 결과는 저장 장치와 kill 시점이 달라지면」 — 방향은 참(§7-1이 근거).

### 05 pending writes와 장애 복구
- 호출 **차례는 흔들림**(이번 확인 `['flaky', 'good']` ↔ 옛 출력 `['good', 'flaky']`) → 옛 b5 둘째 단락대로 횟수·결과만 결정적. 결과 목록은 `sorted`로 결정적.
- `SqliteSaver`로 바꾸면 **남은 쓰기를 SQL로 볼 수 있습니다**(§5-3): 실패 뒤 `writes` 표에 `flaky` 작업의 `__error__` 줄 1 + `good` 작업의 `results` 줄 1(`exit`) — async·sync는 입력 단계의 `branch:to:…` 줄이 더 있음. 세 모드 모두 재개 뒤 `good` 1·`flaky` 2. Ch 4 03 `SELECT`로 이을 수 있고, 02의 `checkpoint_writes`와 짝.
- `snapshot.tasks`는 `PregelTask(id, name, path, error, interrupts, state, result)`(`types.py` 637~646행) — `good`의 `result`는 `{'results': ['good-result']}`(딕셔너리), 옛 출력 `len(task.result or [])` = 1은 키 수.
- 같은 칸에 두 노드가 한꺼번에 쓰는 장면은 **Ch 13 05**(팬아웃·한꺼번에 낸 갱신·`InvalidUpdateError`)가 가르침 → 리듀서는 `operator.add`(Ch 13 02)로, `lambda`는 뺄 수 있음.
- 말: 「superstep」(Ch 20 금지어 super-step → Ch 20 03 「단계」) · 「병렬」(Ch 13·18 금지어 → 팬아웃·함께 실행) · 「런타임」(Ch 21 금지어) · 「트랜잭션」 · 「pending write(s)」(제목). Ch 20 02 b7 링크 설명 「05절(실패한 단계)」 → 05는 실패 원인을 없앤 뒤 재개하는 장면을 지켜야 참.

### 06 노드 재시작과 멱등성
- 옛 worker를 20번 돌린 결과 `naive` 10/10 두 줄 · `idempotent` 10/10 한 줄(§7-4) — Before 결함(같은 쓰기 두 번)은 **실제로 일어나는 결정적 결함**입니다.
- 같은 장면을 자식 프로세스 없이도 보일 수 있습니다(§7-4): 노드가 파일에 쓴 뒤 `raise ConnectionError(…)`(Ch 16 05 「실패 흉내」 모양) → `invoke(None, config)`로 재개 → naive 두 줄 · idempotent 한 줄, 실패 뒤 `next` `('charge',)`.
- 함수 이름 `interrupt_then_resume`의 `interrupt`는 Ch 24 API 이름과 같아 헷갈림. b7 「interrupt 승인과 보상 작업」도 Ch 24 말을 먼저 씀.
- **뒤 챕터가 기대는 문장**: Ch 24 01 b3 「Ch23에서 노드는 장애 뒤 처음부터 재시작될 수 있고 외부 쓰기에는 멱등성이 필요하다는 점을 확인했습니다」 · Ch 31 02 b3 「Ch23에서는 중단 뒤 재개와 멱등성을 배웠습니다」 · Ch 20 02 b7 「같은 쓰기를 한 번만 반영하는 방법은 Ch 23 06절」 → 재시작·중복 쓰기·멱등 키 세 장면을 지켜야 참.
- b8 「Ch24에서는 노드 실행 전에 사람의 승인 값을 받아 부작용 여부를 결정합니다」 — Ch 24 01 제목(interrupt 승인 게이트)과 맞음(Ch 24 대기).

## 3. 실습 폴더 구조와 읽는 곳

```
labs/part6/ch23-persistence/
  README.md (한 문단 + Docker 명령 셋 — postgres:17, 포트 55432)
  pyproject.toml   uv.lock (89항목)
  durability_worker.py (04가 자식 프로세스로 실행)
  idempotency_worker.py (06이 자식 프로세스로 실행)
  notebooks/01~06-*.ipynb
  .venv/ (macOS 판 142MB — home = /Users/…/cpython-3.12-macos-aarch64-none, uv 0.11.6)
  (없음: data/ · runs/ · tests/ · 도구 파일 · 노트북 생성기)
```

- **노트북이 쓰는 파일(옛 판)**: 03 `data/thread-resume.sqlite` · 04 `data/durability/{exit,async,sync}.{sqlite,ready,trace}` · 05 `data/pending-trace.txt`·`data/allow-flaky` · 06 `data/idempotency/{naive,idempotent}.{sqlite,log,ready}` · 02 PostgreSQL 스키마 `ch23_lab`. 모두 실습 폴더 안이고 묶음 목록에 없음 → **학생 폴더에 `data/`(SQLite 본 파일 + `-wal`·`-shm`)가 남습니다.** 지금 디스크에는 `data/`가 없습니다(옛 실행은 다른 기기).
- **Ch 23 파일을 코드로 읽는 곳**(`grep -rl`, `textbook`·`labs`, `.venv`·`before`·zip 제외): **챕터 밖에서 Ch 23 노트북·worker·출력·체크포인트 파일을 읽는 코드는 0** → 산출 파일 계약 없음.

| 자리 | 무엇을 | 성격 |
|---|---|---|
| `textbook/part6/public-files.json` 26~36행 | 실습 파일 11(README·worker 둘·노트북 여섯·`pyproject.toml`·`uv.lock`) | 묶음 허용 목록 |
| 챕터 `qa/public-files.json` | HTML 7 + 옛 SVG 6 + 실습 파일 11 = 24(경로 배열) | `collect_public_files.py`가 Part 목록으로 모음 |
| 챕터 `qa/prerequisite-files.json` | **없음**(Part 6 `prerequisite-files.json`에도 Ch 23 줄 0) | — |
| `textbook/downloads/part6-practice.zip` | `3755de3d…`(97항목) 안 Ch 23 11개가 디스크와 같음 | 묶음 |
| `textbook/part6/_build_index.py` 21행 · `textbook/_notebook/build_index.py` 50행 · `build_bundle.py` 24행 | (6, 10, 설명) · (절 수 **6**, 설명) · 공개 챕터 목록 | 실습 절을 더하면 6 ≠ 7(Ch 21 선례: `_notebook/build_index.py`는 전체 마감 몫) |
| `textbook/part6/qa/check_bundle_execution.py` 30·31행 | **Ch 24 01·Ch 28 01만** 키 없이 실행 | Ch 23은 실행하지 않음 |
| `textbook/_notebook/verify.py` | import 금지 첫 이름 목록 | worker는 import하지 않고 자식 프로세스로 부름 |
| 옛 검사(고치지 않음, 기록만) | `check_scope.py`(`EXPECTED` (6,10)·`SECTION_COUNTS` 6 — 실습 절을 붙이면 멈춤) · `check_notebook_readiness.py`(함수 힌트 필수 — 과정 규칙과 반대, 결과 파일을 먼저 씀) · `check_figures.py`(SVG마다 `.excalidraw` 짝) · `check_visual_reports.py` · `check_delivery.py`(`llm-practice.zip` 신선도) | Ch 21·22 선례대로 이미 어긋난 상태 |
| 기록만 | `textbook/part6/qa/final-artifact-hashes.json`(Ch 23 줄 **44**) · `notebook-executions.json`·`visual-results.json`·`lesson-scope.json`·`figure-consistency.json`·`notebook-readiness.json`·`prose-repetition-initial.json` · `language/ch23-final.json`·`ch23-source-{before,after}.sha256`·`originals/ch23/` · `diagram-color-{before,after}.sha256` · `language/ch22-ch24-code-output-figure-*.sha256` · `ch23-technical-review.md` · `textbook/part7/qa/existing-artifacts-before.json`·`before-integration/build_*.py` · `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json`(verify가 다시 씀)·`checks/ch23-persistence/`(옛 화면 검사) · `existing-artifact-hashes.json`에는 Ch 23 줄 0 | — |

- **옛 생성기**:

| 파일 | 무엇을 씀 | 비고 |
|---|---|---|
| **`textbook/part6/ch23-persistence/qa/author_ch23_ch24.py`**(703줄, `8635d292…`, **Ch 23·Ch 24 공용**) | `write_all()` — **Ch 23 노트북 여섯 + Ch 24 노트북 셋**(`labs/part6/<챕터>/notebooks/`) · 두 챕터 `_src` 전부 · 두 챕터 `figures/_gen_figures.py` | 실행하면 Ch 23 개선본과 **대기 챕터 Ch 24(01~03)**를 함께 옛 판으로 덮어씀. 부르는 스크립트 0(`grep`). `_src` 수정 시각(09-14 03:23)이 생성기(03:44)보다 앞 — 다시 돌리면 `_src`가 지금 판과 같게 나오는지는 확인하지 않음 |
| `figures/_gen_figures.py`(Ch 23) | `NN-흐름.{svg,excalidraw,caption.md}` 18개(`textbook/part5/_figure.py`) | 옛 그림 여섯 벌. Ch 24 `figures/_gen_figures.py`도 같은 공용 생성기가 씀 |
| (챕터 밖) `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part6a_enrich.py` 139~190행 | Ch 23 여섯 절 `_src` b4 「코드를 읽는 순서」·b5 「다른 상황과 적용 경계」와 노트북 설명 셀 | 기록만(Ch 21 선례) |

→ 규격 §8 1번: **01절 작업 때 `figures/_gen_figures.py` 첫머리에 설명 주석 + `raise SystemExit(...)`**. **공용 생성기는 막으면 Ch 24 쪽 생성도 함께 막힙니다** — Ch 21 `_author_ch21_ch29.py`와 같은 처지. 선택지: (가) 첫머리에서 막고 「Ch 23 개선 뒤 이 파일은 Ch 23을 덮어씀. Ch 24를 다시 만들려면 Ch 23 줄을 빼고 쓸 것」을 적음(Ch 24는 개선 때 자기 생성기를 새로 쓰는 것이 과정 흐름) · (나) Ch 23 몫만 막는 한 줄 수정(파일 고치기가 두 챕터에 걸침) · (다) 막지 않고 인계에만 적음. 사본은 이미 `before/generators/`. 파일이 **Ch 23 `qa/` 안**에 있어 챕터 마감 때 `mv -n` → `qa/upgrade/before/generators/blocked/`로 옮기면 Ch 24가 그 파일을 찾는 자리가 바뀜(Ch 24 몫 인계).

- **판**: `requires-python = ">=3.12,<3.13"`, `dependencies = ["langgraph==1.2.11", "langgraph-checkpoint-sqlite==3.0.3", "langgraph-checkpoint-postgres==3.0.5", "psycopg[binary,pool]==3.3.3"]`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`, `[tool.uv] package = false`. 잠금 주요 판: `langgraph-checkpoint 4.2.0`·`langgraph-prebuilt 1.1.0`·`langchain-core 1.6.2`·`pydantic 2.13.5`·`aiosqlite 0.22.1`·`sqlite-vec 0.1.9`·`psycopg-pool 3.3.1`·`orjson 3.12.0`·`ormsgpack 1.12.2`·`langsmith 0.12.4`. **`langchain`·`langchain-openai`·`openai`·`python-dotenv`·`numpy`는 잠금에 없습니다** → 모델을 부르려면 `uv lock`으로 잠금을 다시 만들어야 함(§9-1). `pytest` 없음.
- **Ch 21 잠금과 견줌**: 겹치는 런타임 판은 **모두 같음**(`langgraph 1.2.11`·`langgraph-checkpoint 4.2.0`·`langgraph-prebuilt 1.1.0`·`langchain-core 1.6.2`·`pydantic 2.13.5`, dev 넷). Ch 21에만 `langchain 1.4.0`·`langchain-openai 1.6.0`·`openai 3.11.0`·`python-dotenv 1.2.3`·`numpy 2.5.3`·`pillow 12.3.0`, Ch 23에만 checkpoint 두 패키지·psycopg 셋·`aiosqlite`·`sqlite-vec`. Ch 24 잠금은 `langgraph==1.2.11` 하나(체크포인터는 `InMemorySaver`).

## 4. 앞뒤 챕터 이음새

### 4-1. Ch 21 인계(요약 §13 「Ch 22·23이 이어받을 것과 전제하면 안 되는 것」·§14) 항목별 지금 상태

| # | Ch 21이 넘긴 것 | Ch 23 지금 자리 | 상태 |
|---|---|---|---|
| 1 | Ch 21은 미들웨어·체크포인터·`thread_id`·`interrupt`·스트리밍·`model_settings`·호출 한도를 쓰지 않음 | 01이 체크포인터·스레드를 처음부터 정의(b4) · 06 b7·01 b10이 `interrupt`(Ch 24)를 먼저 씀 | 체크포인터 쪽 **맞음** · `interrupt`를 앞당겨 쓰는 두 자리는 고칠 자리 |
| 2 | 상태 넓히기는 `state_schema=`만, 노드용 `Runtime`은 안 가르침 | Ch 23은 우리 상태 형식 `class State(TypedDict)`만 씀(Ch 13 모양) | 해당 없음 |
| 3 | 결과 상태는 실행 한 번 안에서만 — 저장해 다음 실행에 이어 쓰는 것은 Ch 23 몫. 「Ch 23 `_src`·노트북은 Ch 21·`create_agent`를 가리키지 않음」 | 지금도 **0건**(`grep` — Ch 23 `_src`가 가리키는 챕터는 Ch 13·20(01)·Ch 4(02 셋)·Ch 24(06)) · Ch 21 03 b4·b7·07 b7 「결과 상태를 저장하는 방법은 Ch 23에서」 | **참**(01의 3 → 7). `create_agent(…, checkpointer=…)` 인자는 설치판에 있음(`langchain 1.4.0` 서명 확인) — 쓰면 Ch 21과 곧바로 이어지지만 잠금에 `langchain`이 없음(§9-1) |
| 4 | 실행하지 않은 것을 전제하지 말 것(도구 오류·양식 재요청 등) | Ch 23은 에이전트·도구를 안 씀 | 해당 없음 |
| 5 | 모델이 채운 값은 「항상」이 아님 | 모델 없음 — 대신 **async 저장 여부가 흔들림**(4/60) | 같은 태도로 04 async 값을 한정해야 함 |
| 6 | `ProviderStrategy`의 `strict` | — | 해당 없음 |
| 7 | 이름 `AgentState` 셋 | Ch 23은 `State` | 해당 없음(`create_agent`를 쓰면 라이브러리 상태 형식) |
| 8 | 「컨텍스트」 = Ch 8 뜻 | Ch 23 0건 | 해당 없음 |
| §14 | 「Ch 23은 Ch 21에 기대지 않습니다」 | 맞음 | — |
| 도구 파일 | `runner_tools.py`(메시지·사용량·검색·판정 함수 15) | 모델·메시지가 없어 쓸 함수 0 | 가져올 것 없음(§8) |
| Ch 20 `graph_tools.py` · Ch 6 06 `estimate_cost` | 메시지·비용 함수 | 모델이 없으면 쓸 곳 0 | 모델을 넣는 선택(§9-1 M2)에서만 후보 |

### 4-2. 앞 챕터 부품과 대조 (다시 쓸 후보)

| 부품 | 앞 챕터 | Ch 23 지금 | 이을 때 |
|---|---|---|---|
| 상태 형식·리듀서 | Ch 13 01 `TypedDict`·02 `Annotated`+`operator.add`(덮어쓰기 ↔ 이어 붙이기)·04 `add_messages`·05 팬아웃·`InvalidUpdateError` · 노드 힌트 0 | 01 리듀서 없음 · 03 `operator.add` · 05 `lambda` 리듀서 · 노드 힌트 있음 | 05 `operator.add` · 힌트 빼기 · 03을 메시지 칸으로 바꾸면 Ch 13 04·Ch 22 09 b8과 이어짐 |
| 구조 문자열 | Ch 13 01 `get_graph().draw_mermaid()` 글자 | 없음 | 그래프 모양을 보여 줄 때 |
| 설정 딕셔너리 | Ch 20 03 `{"recursion_limit": N}`·「단계」 | `{"configurable": {"thread_id": …}}` | 「Ch 20 03 설정 딕셔너리에 칸 하나」로, super-step은 「단계」 |
| SQLite | Ch 4 03 `sqlite3.connect("shop.db")`(임시 폴더에서)·`execute`·`fetchall`·`commit`·`close` | 03·04 `with sqlite3.connect` | 표 조회(`sqlite_master`·`SELECT … FROM writes`)를 Ch 4 03 말로 |
| PostgreSQL | Ch 12 02 psycopg·Docker·55432 | 02 | b3 링크를 Ch 4 → Ch 12 02로 |
| 임시 폴더 | Ch 1~4 준비 셀 `mkdtemp(prefix="chNN-MM-")` → `os.chdir()` → `os.listdir()` · Ch 4 03이 SQLite 파일을 임시 폴더에 | 실습 폴더 `data/`에 씀 | **이 기기에서는 임시 폴더만 됨**(§9-2) |
| 실패 흉내·감사 기록 | Ch 16 05 `raise TimeoutError("이 절에서 만든 실패 흉내입니다.")`·감사 기록 파일(여는 방식 `"w"`) | 05 허용 파일로 `RuntimeError` · 06 로그 파일 | 05·06의 실패를 「실패 흉내」로 부르고, 06 로그를 「기록 파일」로 |
| 자식 프로세스 | 과정 §3 `subprocess.run([sys.executable, "-m", 모듈, …])`(Ch 2) · `subprocess.Popen`은 Ch 4 준비 셀 예외에서만 | 04·06 `Popen`+`kill`+`run` | 04는 강제 종료가 주제라 필요(§7) — 처음 쓰는 자리에서 세 문장 |
| 멈춘 흐름 | Ch 16 05 재시도·예비 흐름 · Ch 20 03 실행 한도에서 멈춘 `invoke`(「체크포인터로 읽는 일은 하지 않았습니다」) | — | 01 또는 05에서 「Ch 20 03이 넘긴 장면」으로 이을 수 있음 |

### 4-3. 완료 챕터가 Ch 23에 기대는 문장 — 개선 뒤에도 참이어야 함

| 자리 | 지금 문장 | 판정 기준 |
|---|---|---|
| **Ch 20 02 `_src` b7(33행)·HTML** | 「멈춘 실행을 다시 이어 가는 방법은 **Ch 23 04절**(강제 종료 뒤)과 **05절**(실패한 단계)에서 다룹니다. 같은 쓰기를 한 번만 반영하는 방법은 **Ch 23 06절**에서 다룹니다.」 — 링크 `../../part6/ch23-persistence/04-내구-실행-모드-비교.html`·`05-pending-writes와-장애-복구.html`·`06-노드-재시작과-멱등성.html`(생성기 `author_02.py` 568·569행 상수) | **슬러그 04·05·06을 바꾸면 끊김.** 04 = 강제 종료 뒤 재개, 05 = 실패 원인을 없앤 뒤 재개, 06 = 한 번만 반영하는 장면을 지켜야 참 |
| **Ch 20 03 `_src` b7·HTML** | 「실행 중 상태를 저장해 두는 체크포인터는 **Ch 23 01절**에서 다룹니다」 — 링크 `01-체크포인터와-스레드.html`(생성기 `author_03.py` 587행) | **슬러그 01도 바꾸면 끊김** |
| Ch 21 03 `_src` b4·b7 · 07 b7(HTML 둘) | 「결과 상태를 저장해 다음 실행에 이어 쓰는 방법은 Ch 23에서 배웁니다」 | 01의 3 → 7로 참(링크 없음) |
| **Ch 22 09 `_src` b8(55행)·HTML** | 「Ch23에서는 대화 기록을 프로그램 밖에 저장하고 다시 이어 가는 방법을 다룹니다. 이번 실습에서 종류별로 출력한 대화 기록이 그 대상입니다.」 | 03이 메시지 칸을 저장하면 그대로 참, 글 목록이면 앞 문장까지만 참(§2 03) |

- 슬러그 02·03은 링크하는 완료 파일이 없습니다(`grep`) → 02를 바꾸는 선택(§6)에서도 링크는 안 끊김. `textbook/part6/index.html`·`textbook/index.html`은 빌드로 다시 만듦.

### 4-4. 뒤 챕터(대기)가 Ch 23에 기대는 문장 — 고치지 않음

| 자리 | 지금 문장 | 판정 기준 |
|---|---|---|
| Ch 24 01 `_src` b3 | 「Ch23에서 노드는 장애 뒤 처음부터 재시작될 수 있고 외부 쓰기에는 멱등성이 필요하다는 점을 확인했습니다. … 체크포인터는 InMemorySaver …」 | 06 |
| Ch 25 01~03 `_src` b3 | 「Ch23에서 체크포인터와 thread_id가 상태를 저장하는 방법을 배웠고」 | 01 |
| Ch 26 01~04 `_src` b3 · `_generate_ch25_ch26.py` 470·478행 | 「Ch23에서 thread_id와 체크포인터를 배웠습니다」 | 01 |
| Ch 27 01 b3 · 04 b3 | 「Ch 23의 체크포인터는 실행 상태를 이어 주었고」 · 「Ch 23에서 상태 저장 범위를 구분했습니다. FilesystemBackend의 파일은 **체크포인터 메시지**와 다른 저장 표면」 | 01·03 — 「메시지」는 03을 메시지 칸으로 바꿀 때만 참 |
| Ch 30 02 b3·06 b3 · `_generate.py` 24·76행 | 「Ch21의 Agent와 Ch23의 체크포인터처럼 생성 비용과 수명주기가 다른 객체」 · 「Ch23의 thread 분리와 Ch24의 중복 실행 방지 원칙」 | 03(연결과 그래프 객체의 수명 구분)·01 |
| **Ch 31 05 b3 · 노트북** | 「Ch23에서는 PostgresSaver의 `setup()`이 체크포인터 표를 만든다는 점을 확인했습니다」 · 노트북이 Docker(55431)로 `setup()`·`information_schema` 조회를 다시 함 | **02가 PostgreSQL을 실행하느냐에 달림**(§6) |
| Ch 31 02 b3 | 「Ch23에서는 중단 뒤 재개와 멱등성을 배웠습니다」 | 04~06 |
| Part 6 소개 `_src/index.html` 8행 · `practice-start.md` 15행 · `labs/part6/continuity-guide.md` 9·10행 · `labs/part7/continuity-guide.md` 8행 | 「저장한 상태로 실행을 이어 가는 방법」 · 「저장·재개·승인을 실습」 · 「Ch4의 데이터베이스, Ch13의 상태와 노드 → Ch23 체크포인터와 프로세스 중단 후 복구」·「Ch23의 스레드와 저장 상태 → Ch24」 · 「Ch23의 저장 상태 → Ch30·31」 | 참(continuity-guide 9행 「Ch4의 데이터베이스」는 SQLite로 참) |

### 4-5. Part 6 묶음·목록·계약·검사

- **계약 0**: 뒤 챕터 코드·테스트·검사 스크립트가 Ch 23 파일을 읽지 않고, Ch 23도 앞 챕터 산출 파일을 읽지 않습니다. 묶음 실행 검사도 Ch 23을 돌리지 않습니다.
- **묶음을 다시 만들 때**: `python3 textbook/part6/_build_index.py` → `part6-practice.zip`(Ch 21 선례 — `Part 6: N verified sections; M bundled files`) · 도구 파일·worker 이름이 바뀌거나 늘면 챕터 `qa/public-files.json` + `textbook/part6/public-files.json`(`collect_public_files.py`는 Part 목록 전체를 다시 씀 — 돌리기 전 차이 확인).
- **옛 검사 스크립트가 Ch 23을 보는 법(기록)**: `check_scope.py` 절 수 6·(6, 10)·meta 정규식(「실습 30분」 불통) · `check_notebook_readiness.py` 함수 힌트 필수·Part 6 노트북 수 고정 · `check_figures.py` SVG마다 `.excalidraw` · `check_visual_reports.py` 개수 고정 · `check_delivery.py` 묶음 신선도(`llm-practice.zip`에서 멈추는 것이 과정 공통) · `check_bundle_execution.py` Ch 23 안 돌림. **모두 이미 Ch 21·22 개선으로 어긋난 상태** → 선례대로 고치지 않고 돌린 결과만 적음(`check_notebook_readiness.py`는 결과 파일 되돌림).

## 5. 라이브러리 동작 — 설치판 소스와 모델 없는 확인 (2026-09-25)

설치판: `langgraph 1.2.11`·`langgraph-checkpoint 4.2.0`·`langgraph-checkpoint-sqlite 3.0.3`·`langgraph-checkpoint-postgres 3.0.5`·`psycopg 3.3.3`(binary, libpq 18)·SQLite 3.53.1. 확인 스크립트는 기기 `/tmp/ch23-prep/exp/`(`exc_modes.py`·`kill_modes.py`·`kill_async.py`·`async_runs.txt`·`pending.py`·`sq.py`·`idem.py`·`idem_exc.py`·`timing.py`·`pg02.py`). **노트북 셀이 아니라 준비 조사용 확인입니다.**

### 5-1. durability
- 정의·기본값 §2 04. `durability`를 주고 체크포인터가 없으면 「`durability` has no effect when no checkpointer is present.」 경고(`main.py` 2802~2804행).
- `exit`가 아닌 모드는 작업이 끝날 때마다 쓰기(`put_writes`)를 저장하고(`_loop.py` 466행), `exit`는 그래프가 끝날 때(오류·중단 포함) 체크포인트와 남은 쓰기를 한꺼번에 저장(`_loop.py` 1324~1333행). `sync`는 매 단계 뒤 저장 완료를 기다림(`main.py` 2987~2988행 `loop._put_checkpoint_fut.result()`).

### 5-2. 체크포인트 수
- 한 노드 그래프 두 번 실행(01): 단계 −1(입력)·0·1 → 2(입력)·3·4 = 6. 공식 문서 「START → A → B → END에는 정확히 4개」와 같은 규칙.
- 두 노드 그래프 성공: 기록 수 `exit` **1** ↔ `async`·`sync` **4**(결정적, 세 번 같음). 20노드 그래프 SQLite `checkpoints` 표 줄 수: `sync` 22 ↔ `exit` 1.

### 5-3. 남은 쓰기(pending writes)
- `SqliteSaver.setup()`이 만드는 표 둘: `checkpoints`(thread_id·checkpoint_ns·checkpoint_id·parent_checkpoint_id·type·checkpoint·metadata) · `writes`(thread_id·checkpoint_ns·checkpoint_id·task_id·idx·channel·type·value), 그리고 `PRAGMA journal_mode=WAL`(`sqlite/__init__.py` 122~159행).
- 05 그래프를 `SqliteSaver`로: 실패 뒤 `writes` 표 `('…', '__error__', -1)`·`('…', 'results', 0)`(exit) / async·sync는 `branch:to:flaky`·`branch:to:good`·`results` 줄이 더 있음 · `checkpoints` 줄 exit 1 ↔ async·sync 2 · `get_state().next` `('flaky',)` · `tasks` `[('good', False, {'results': ['good-result']}), ('flaky', True, None)]` · 재개 뒤 세 모드 모두 good 1·flaky 2, 결과 `['flaky-result', 'good-result']`.
- 공식 문서(checkpointers): 「When a graph node fails mid-execution at a given super-step, LangGraph stores pending checkpoint writes from any other nodes that completed successfully at that super-step.」 · 「you don't re-run the successful nodes」.

### 5-4. PostgresSaver와 임시 PostgreSQL로 한 번 (옛 02 흐름)
- 서버: **Ch 12가 둔 conda-forge PostgreSQL 바이너리 `$ROOT/.cache/vm/pgenv`(`postgres (PostgreSQL) 17.11`)**로 `/tmp/ch23-prep/pgtest`에 새 클러스터(`initdb -U postgres`, 암호 `postgres`, 39MB)를 만들고 포트 **55439**에서 켠 뒤 같은 호출 안에서 끔. **Ch 12 `pgdata`는 건드리지 않음.**
- 결과: `server: 17.11` · Before `UndefinedTable | relation "checkpoints" does not exist | sqlstate 42P01` · After `{'value': 12}` · 표 `['checkpoint_blobs', 'checkpoint_migrations', 'checkpoint_writes', 'checkpoints']` · `checkpoint_migrations` 10줄(최대 v 9) · 스레드 `after` 체크포인트 3 · 쓰기 3 · 값 1 · 색인 7(기본 키 넷 + `thread_id` 색인 셋) · `setup()` 두 번째 부름은 오류 없음 · 서버 없는 포트는 `OperationalError … Connection refused`.
- `setup()`이 도는 문장(`postgres/base.py` 37~85행 `MIGRATIONS` 10개): 표 넷 `CREATE TABLE IF NOT EXISTS` · `ALTER TABLE checkpoint_blobs ALTER COLUMN blob DROP not null` · `SELECT 1`(판 번호 맞추기용) · `CREATE INDEX CONCURRENTLY` 셋 · `ALTER TABLE checkpoint_writes ADD COLUMN IF NOT EXISTS task_path …`. `setup()`은 `checkpoint_migrations`의 마지막 판 번호 다음부터만 돎(`postgres/__init__.py` 77~102행). **서버 없이도 `PostgresSaver.MIGRATIONS`를 import만으로 출력할 수 있음**(확인).
- `from_conn_string`은 `Connection.connect(conn_string, autocommit=True, prepare_threshold=0, row_factory=dict_row)`(`postgres/__init__.py` 56~75행).

### 5-5. SQLite 연결과 파일
- `with sqlite3.connect(…) as conn:` 뒤에도 연결이 열려 있음 · `-wal` 65,952바이트·본 파일 4,096 → 닫은 뒤 본 파일 20,480 · `SqliteSaver.from_conn_string(경로)`은 닫음 · 새 연결로 같은 스레드 `['질문 1', '답변 1', '질문 2', '답변 3']`, 체크포인트 6·쓰기 6.
- **연결 폴더(마운트) 안에서는 SQLite 쓰기가 안 됨**: `$ROOT/.cache/ch23-prep/`에서 `SqliteSaver` → `sqlite3.OperationalError: disk I/O error`(setup의 WAL 전환) · 일반 SQLite(`journal_mode` `delete`)도 첫 `commit`에서 `disk I/O error`. 저널 파일을 지우지 못해서로 보임(이 폴더는 삭제가 막힘). 시험 파일 넷(4.6KB)이 남음(§14 삭제 승인 대상).

## 6. Postgres 없이 02를 다루는 선택지 (장단점만)

**사실 먼저**: (1) 작업 기기에 Docker는 없지만 **PostgreSQL 17.11 서버 바이너리는 있음**(Ch 12 02 `pre_exec.sh` 선례 — `run_section.sh` 32행이 `qa/upgrade/pre_exec.sh`를 절 실행 직전에 source). §5-4처럼 새 클러스터로 옛 02 흐름이 그대로 돌았음. (2) 학생 기준은 Docker(README). (3) Before 결함(`setup()` 누락)은 서버가 있으면 실제·결정적. (4) Ch 31 05(대기)가 이 절의 「`setup()`이 표를 만든다는 확인」에 기댐. (5) 슬러그 02는 링크 0.

| 선택지 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **A. Ch 12 방식 — 작업 기기는 pgenv, 교재는 Docker** | 02용 클러스터를 새로(`.cache/vm/pgdata-ch23` 또는 `/tmp`) 만들고 `qa/upgrade/pre_exec.sh`가 교재와 같은 접속 정보로 켬. 노트북은 옛 판처럼 실제 접속 · paired 유지 | Before/After가 실제 결함·실제 표 · Ch 31 05 b3 그대로 참 · Ch 12 선례·도구(`run_section.sh`)가 이미 있음 · 모델 요청 0 | 작업 환경(PostgreSQL 17.11 바이너리) ↔ 학생 환경(Docker `postgres:17`)이 달라 진단에 적어야 함 · 새 클러스터 약 39MB(마운트면 사용자 디스크, `/tmp`면 기기 VM을 다시 만들 때 사라짐) · Ch 12 `pgdata`와 **같은 포트 55432**를 쓰면 두 챕터가 동시에 못 켬(호출이 끝나면 꺼지므로 실행 때는 문제 없음) · 학생 쪽 포트 충돌(§2 02)과 Docker 없는 학생은 여전히 이 절을 못 돌림 |
| **B. 서버 없이 — 설치판의 `setup()` 문장을 출력** | `PostgresSaver.MIGRATIONS`(10개)를 import만으로 출력해 「`setup()`이 만들 표 넷」을 보이고, 실제 표는 `SqliteSaver` 파일에서 `sqlite_master`로 조회(Ch 4 03 `SELECT`) | 누구나 실행 · 결정적 · 모델·서버 0 · 이 기기에서 바로 됨 | **PostgreSQL을 실행하지 않음**(「이번에 실행하지 않았습니다」) · SQLite 표는 둘이고 이름이 달라(`writes` ↔ `checkpoint_writes`, 값 표·판 기록 표 없음) 「같은 구조」로 쓸 수 없음 · paired Before를 새로 세워야 함 · 제목·`objectives` 둘째 줄(「PostgresSaver를 준비」)·Ch 31 05 b3 인계 |
| **C. B + Before를 「메모리 체크포인터는 프로세스가 끝나면 사라짐」으로** | Before = `InMemorySaver`로 저장한 자식 프로세스가 끝난 뒤 새 프로세스에서 `get_state().values` `{}`(결정적) · After = SQLite 파일은 남음. `setup()`·표 이야기는 소스 출력으로 | paired를 실제 결함으로 유지 · 03 「새 연결에서 이어 가기」와 겹치지만 「왜 파일·DB가 필요한가」가 선명 · 서버 0 | 절 주제가 「PostgresSaver 준비」에서 「프로세스 밖 저장소가 필요한 이유」로 바뀜(슬러그·제목 변경 가능 — 링크 0) · 03과 장면이 겹침 · PostgreSQL 실행 0 |
| D. 접속 실패를 Before 결함으로 | 서버 없는 환경의 `OperationalError`를 Before로 | 서버 0 | 학습 질문(`setup()` 누락)과 다른 결함 · **학생 환경에 따라 Before가 안 일어남**(Docker를 켠 학생) → 같은 셀 출력이 환경마다 다름. 규격 §3 「실패 장면은 실제로 일어나는 조건」은 만족하나 교재 출력으로 고정할 수 없음 — 권하지 않음 |
| E. 서버가 있으면 실행, 없으면 건너뜀 | `try`로 접속을 시험하고 분기 | 어디서나 셀이 끝까지 감 | 교재 출력이 환경마다 달라짐 · 새 커널 두 번 비교·G5 인용이 흔들림 · 코드가 길어짐 — 권하지 않음 |

- A·B는 섞을 수 있습니다(A로 실행하면서 `MIGRATIONS` 출력으로 「`setup()`이 도는 문장」을 한 셀 더 — 표 넷·색인 셋·판 기록이 한 번에 설명됨).
- 어느 쪽이든 b3 「Ch4 … PostgreSQL」 → Ch 12 02, `except Exception` → `except psycopg.Error`(Ch 12 02 모양) 또는 `psycopg.errors.UndefinedTable`, `lambda` 노드 → 이름 있는 함수.

## 7. 04~06 결정적 장면 가능성

### 7-1. 04 강제 종료(옛 방식)
- `exit`·`sync`는 강제 종료 시점과 상관없이 결정적(20/20). `sync`는 second가 시작되기 전에 first 저장이 끝나 있고, `exit`는 끝날 때까지 아무것도 쓰지 않기 때문. **async만 흔들림**(56/60 ↔ 4/60).
- → 결론·그림 라벨·정리는 exit ↔ sync 두 모드로, async는 「이번 실행에서는」 둘째 단락·표·「확인할 점」에만(규격 §2-7 9번 끝). 노트북 밖 확인 기록(60번)은 진단 b7에.

### 7-2. 04를 한 프로세스 안에서 (보조 장면 후보)
- (a) second 노드 안에서 그 순간 저장된 체크포인트 수를 셈: `exit` **0**(늘 같음) · `sync` **3**(늘 같음) · `async` 2 또는 3(흔들림). 자식 프로세스 없이 「저장이 끝났는가」를 출력으로 보임.
- (b) 노드 안 예외(실패 흉내)로 멈춤: **세 모드 모두 `completed ['first']`·`next ('second',)`** — `exit`도 끝나며 저장하므로 차이가 안 보임. 차이는 기록 수(exit 1 ↔ async·sync 3)에만.
- (c) 성공한 실행의 기록 수 exit 1 ↔ async·sync 4(결정적).
- **Ch 20 02 b7 「04절(강제 종료 뒤)」 때문에 (a)~(c)는 보조로만** — 강제 종료 장면을 빼면 링크 설명이 틀림.

### 7-3. 걸린 시간은 주제인가
- 공식 문서는 `exit` 「best performance」·`async` 「good balance」·`sync` 「highest durability」로 성능을 말합니다. 그러나 로컬 SQLite 20노드에서 exit 약 0.005초 ↔ async·sync 약 0.023~0.025초, async·sync 차이는 보이지 않았습니다(5번). **시간 비교를 주제 절 예외(Ch 15 05·06·Ch 17 04·Ch 18 03 선례)로 둘 재료가 약함** → 구조(「sync는 저장이 끝날 때까지 기다린다」)만 쓰고 「걸린 시간은 이번에 재지 않았습니다」가 과정 규칙과 맞음. 잰다면 결론에서는 빼고 둘째 단락에만.

### 7-4. 06 멱등성
- 강제 종료 방식(옛 worker) naive 2 · idempotent 1 **10/10씩** 결정적(한 전략 약 1.1초).
- 한 프로세스 안 방식: 노드가 기록 파일에 쓴 뒤 `raise ConnectionError(…)` → `invoke(None, config)` → naive 두 줄 · idempotent 한 줄(결정적). Ch 16 05 「실패 흉내」 선례와 같은 모양이라 자식 프로세스·`kill`이 필요 없음.
- 선택: 04에서 이미 강제 종료를 가르치면 06은 같은 도구를 다시 써도 되고(도구 파일 후보 §8), 실패 흉내로 바꿔 코드를 줄여도 됨. Ch 24 01 b3 「장애 뒤 처음부터 재시작」은 둘 다 참.

### 7-5. 05 남은 쓰기
- 호출 수·결과 목록·`writes` 표의 채널 이름(`__error__`·`results`)·`next`는 결정적, 호출 차례와 작업 ID는 흔들림/무작위.

## 8. §2-7 판단 근거 — 도구 파일

### 사실
1. **챕터 안 되풀이**: 경로 셀(03~06 같은 네 줄) · 강제 종료 뒤 재개 함수(04 `kill_and_resume`·06 `interrupt_then_resume` — `Popen` → ready 기다리기 → `kill` → `wait` → `run(…, "resume")` 모양이 같음, 각 17줄) · 저장값 읽기(04 `read_saved`, 03·06에서도 쓸 수 있음) · 기록 파일 한 줄 쓰기(05 `record`·worker 둘). 07 실습 절도 같은 함수를 다시 쓸 가능성이 큼.
2. **앞 챕터 함수로 바꿀 수 있는 것은 거의 없음**: Ch 20 `graph_tools.py`·Ch 21 `runner_tools.py`는 메시지·사용량·검색·판정 함수(모델이 없으면 0) · Ch 13 `print_state`는 칸(질문·검색어·실행 흔적)이 달라 못 씀 · Ch 16 `guardrails.py` `make_audit_log`·`write_audit_rows`는 감사 기록 모양이 06 로그와 다름.
3. **worker 둘은 이미 모듈 파일**(실습 폴더 맨 위, 자식 프로세스로만 실행 — import 안 함). 학생이 여는 파일이라 도구 파일 규칙(§2-7 4항 — 금지 문법 금지)을 따르게 할지 정해야 함(조건 표현식 둘씩·한 줄 다중 대입·반환 힌트·영어 독스트링).
4. **이미 쓴 도구 파일 이름**: `llm_tools.py`(Ch 5·7·8) · `rag_tools.py`(Ch 9~15) · `git_tools.py`(Ch 3) · `guardrails.py`(Ch 16) · `agent_tools.py`(Ch 17) · `workflow_tools.py`(Ch 18) · `order_tools.py`(Ch 19) · `graph_tools.py`(Ch 20) · `runner_tools.py`(Ch 21). Part 6·7 실습 폴더 모듈 `durability_worker.py`·`idempotency_worker.py`(Ch 23)·`course_server.py`(Ch 28)·`agent_service/`(Ch 30). `verify.py` 금지 첫 이름 `rag`·`prompts` 등. 실습 폴더 `tests/` 없음 → §2-7 7항 해당 없음.
5. 새 이름 후보(겹치지 않음): `checkpoint_tools.py` · `resume_tools.py` · `saver_tools.py` · `persist_tools.py`.

### 선택지 (결정하지 않음 — 장단점만)

**A. 도구 파일을 만들지 않는다**(worker 둘만)
- 장점: 묶음 목록·README 그대로 · 노트북 여섯이 짧아(248줄) 줄일 몫이 작음 · Ch 2·4·6·22 선례 「만들어도 챕터 전체가 줄지 않으면 만들지 않음」.
- 단점: 06·07이 04의 강제 종료 함수를 다시 적음(§2-7 3항과 부딪힘) — 06을 실패 흉내로 바꾸면 이 단점은 거의 사라짐.

**B. 새 도구 파일 하나**(`notebooks/checkpoint_tools.py` 등 — 04 강제 종료 뒤 재개 함수 · 저장값 읽기 · SQLite 표 줄 세기 · 기록 파일 한 줄 쓰기)
- 장점: 06·07이 한 줄로 가져옴 · 04에서 한 번 가르친 자식 프로세스 코드가 되풀이되지 않음.
- 단점: `subprocess`·`sys`·`time`·`sqlite3` import가 든 파일이 새로 생김 · 묶음 목록 둘·README 손질 · 함수 인자(worker 경로·ready 경로·임시 폴더)를 노트북 전역 대신 인자로 받게 설계해야 함.

**C. worker 파일과 도구 파일을 합침**(worker 둘을 `notebooks/`로 옮기고 그래프 만들기·강제 종료 함수를 한 파일에)
- 장점: 「학생이 여는 파일」이 한 자리 · 경로 찾기가 `notebooks/` 한 곳.
- 단점: 자식 프로세스로 부를 스크립트와 가져올 함수 파일이 섞여 읽기 어려움 · 묶음 목록 경로가 바뀜(`public-files.json` 둘) · Ch 20 02 링크와는 무관.

**D. 도구 파일 없이 06을 실패 흉내로 바꿔 강제 종료 코드를 04에만 둠**
- 장점: 되풀이 자체가 사라짐 · 06 코드가 짧아짐 · 06 Before·After가 한 프로세스라 설명이 쉬움.
- 단점: 06의 「프로세스가 죽은 뒤」 장면이 빠짐(실패 흉내는 예외로 멈춘 장면) — Ch 24 01 b3·Ch 31 02 b3은 여전히 참이지만 06 b2 「외부 쓰기 뒤 상태 반환 전에 프로세스가 끝나면」은 고쳐야 함.

공통: 도구 파일을 만들면 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 …」(과정 요약 §3) · `run_section.sh`가 `notebooks/`를 `PYTHONPATH`에 더함 · 함수마다 `# 04절에서 배웠습니다`.

## 9. 과정 규칙과 부딪히는 것 (선택지와 장단점만)

### 9-1. 모델 없는 챕터와 규격 §3
- **사실**: 여섯 절 모두 모델 요청 0, 잠금에 `langchain`·`openai` 없음. 규격 §3은 가짜 모델을 금지할 뿐 「모델 없는 그래프 절」은 선례가 있음(Ch 13 01~06·Ch 20 03). §7-2 실습 절 「모델 호출 3~5번」은 Part 1 실습 절(Ch 1·3·4)이 0번인 선례가 있음. Ch 22 09 b8·Ch 27 04 b3이 「대화 기록(메시지)을 저장」을 전제.
- (M1) **모델 없이 그대로** — 장점: 결정적·키 0·비용 0·잠금 그대로·Ch 24(모델 없음)와 이어짐. 단점: 03 「대화」가 글 목록뿐 · Ch 22 09 b8 「그 대상」이 반만 참 · 07 실습 절이 모델 0번(§7-2 분량 설명과 다름 — 챕터 요약·강사 확인).
- (M2) **03(또는 03·07)에 실제 모델** — `create_agent(model, …, checkpointer=…)`(Ch 21과 바로 이어짐) 또는 모델 노드 + `add_messages`. 앞 대화가 있어야만 답할 수 있는 질문(Ch 7 04 선례). 장점: Ch 21 → Ch 23 → Ch 22 09 b8·Ch 27 04와 모두 이어짐 · 「저장한 대화를 새 연결에서 이어 간다」가 실제 에이전트 장면. 단점: **`uv lock`으로 잠금을 다시 만들어야 함**(`langchain 1.4.0`·`langchain-openai 1.6.0`·`python-dotenv 1.2.3` — Ch 21 판, 보호 파일) · 키 셀·노트북 밖 다섯 번 흔들림 확인 · 모델 답에 `assert` 금지라 핵심 관찰(「앞 대화의 번호를 이어 받음」)이 흔들릴 수 있음.
- (M3) **모델 없이 메시지 칸만** — 03 상태를 `messages: Annotated[list[AnyMessage], add_messages]`로 하고 `HumanMessage`와 노드가 만든 `AIMessage`를 저장(Ch 13 04·Ch 20 01 「손으로 만든 `AIMessage`」 선례). 장점: Ch 22 09 b8 「종류별 대화 기록」이 참 · 결정적 · 잠금에 `langchain-core`가 이미 있음(메시지 클래스). 단점: 「답」이 모델 글이 아님을 한 문장으로 밝혀야 함 · 가짜 모델로 읽히지 않게(클래스가 아니라 노드 함수) 설명 필요.

### 9-2. 파일 쓰기 자리 — **이 기기에서는 실습 폴더에 SQLite를 쓸 수 없음**
- **사실**: §5-5 — 연결 폴더 안 SQLite는 `disk I/O error`. 옛 판 03·04·06(worker 포함)은 실습 폴더 `data/`에 씀 → **이 기기에서 그대로는 실행 실패**. 옛 판 `Path.unlink(missing_ok=True)`는 두 번째 실행부터 삭제가 막힘. 학생 폴더에는 `data/`가 계속 쌓임.
- (가) **임시 폴더**(`tempfile.mkdtemp(prefix="ch23-03-")` → `os.chdir()` → `os.listdir()` — Ch 1~4 준비 셀·Ch 4 03이 SQLite를 임시 폴더에 둔 선례) — 장점: 이 기기에서 돌아감 · 학생 폴더에 파일이 안 남음 · 매 실행 빈 폴더라 지우기 코드 불필요. 단점: 준비 셀 예외(`upgrade_allow=["stdlib-import"]` 선례는 Ch 1~4)를 Part 6에서 다시 쓰는 까닭 한 문장 · worker에 임시 경로를 넘겨야 함 · 출력에 임시 경로가 찍히면 인용 금지(과정 §3).
- (나) 실습 폴더 `data/` 유지 + 작업 기기만 다른 자리 — 단점: 교재 코드와 작업 실행이 달라짐 · 삭제 막힘 · 권하지 않음.
- 02(PostgreSQL)는 서버 쪽 스키마라 이 문제와 무관(§6).

### 9-3. 자식 프로세스·강제 종료 (04·06)
- **사실**: `subprocess.Popen`은 과정 기본 경로 0건(Ch 4 준비 셀 예외만), `process.kill()`·`wait(timeout=)`·`time.time()` 기한 루프는 처음. 04는 Ch 20 02 링크 때문에 강제 종료 장면이 필요(§7-2).
- (가) 04에서 세 문장으로 가르치고 06·07은 도구 파일에서 가져옴(§8 B) · (나) 04에서만 쓰고 06은 실패 흉내(§8 D) · (다) 지금처럼 04·06 모두 노트북에 — 긴 함수(17줄 > 10줄)를 나눠야 함.

### 9-4. 힌트·클래스·`with`
- 노드 힌트(`state: State`·`-> dict`)는 Ch 13·20·21이 0 → 빼는 쪽이 과정 모양(Ch 22는 시범이라 있음). 상태 형식 `class State(TypedDict)`는 Ch 13 L5 그대로.
- `with sqlite3.connect(…)`는 닫지 않음(§5-5) → `conn.close()`(Ch 4 03·Ch 12 02) 또는 `SqliteSaver.from_conn_string`·`PostgresSaver.from_conn_string`(`with` + 닫힘 — Ch 21 04 `with warnings.catch_warnings` 선례처럼 처음 쓰는 자리에서 한 문장).
- worker 파일의 금지 문법(§0)을 도구 파일 규칙으로 고칠지(학생이 여는 파일 — §8 사실 3).

### 9-5. 제목·`objectives`·용어

| 자리 | 말 | 과정 말·선례 |
|---|---|---|
| 챕터 제목 「Persistence와 Durable Execution」 | 영어 둘 | Ch 19~21 선례: 영어·API 이름은 제목에만 두고 강사 확인, 본문 첫 자리에서 풂(예: 저장과 이어 실행) |
| 02 「PostgresSaver 준비와 스키마」 | API 이름 · 「스키마」(Ch 20·21 금지어 — 거기서는 양식 뜻) | DB의 「스키마」는 이름 공간 뜻이라 다른 말(「이름 공간」·「표 묶음」) 또는 제목에만(강사 확인). §6 선택에 따라 제목 자체가 바뀔 수 있음 |
| 05 「pending writes와 장애 복구」 | 영어 | 본문은 「남은 쓰기」류로 풀고 제목에만(강사 확인) |
| 06 「노드 재시작과 멱등성」 | 「멱등성」 | 한자어 — 세 문장(뜻 → 일상 예 → 코드)으로 |
| 04 「내구 실행 모드 비교」 | 「내구」 | 한자어 — `durability`와 짝지어 풂 |
| `objectives` 셋 | 「PostgresSaver를 준비하고 내구 실행 모드별 장애 복구 범위를 비교」·「pending writes와 멱등 키」 | 마감 때 절별로(Ch 20·21 선례) |
| `_build_index.py` 21행 · `_notebook/build_index.py` 50행 | 「실행 상태를 저장하고 프로세스 중단 뒤 복구되는 범위를 확인합니다」 | 마감 때 21행만(50행은 선례대로) |
| 본문 공통 | 반환(Ch 13)·경로(Ch 13)·로그(Ch 17 → 기록)·스키마·검증(Ch 16 → 검사)·측정(Ch 17)·지연(Ch 18 → 걸린 초)·병렬(Ch 13·18)·superstep(Ch 20 → 단계)·식별자(Ch 19)·런타임·마이그레이션·인터페이스(Ch 21)·채널(Ch 13 → 칸)·스냅샷·트랜잭션·원자적·경합·모사·보장·「정확히 한 번」 | 내놓다·흐름/차례·기록·칸·단계·팬아웃/함께 실행·걸린 초. **「마이그레이션」은 Ch 21 04 「옮기기」(코드 옮기기)와 다른 뜻** — 과정 마감 목록이 「옮기기 ≠ Ch 23·31 DB 마이그레이션」으로 적어 둠 |

### 9-6. 참고 자료 b10
- 여섯 절이 같은 넷(Interrupts·Time Travel 포함) → 절마다 맞는 문서로: Persistence·Checkpointers(`docs.langchain.com/oss/python/langgraph/checkpointers`)·Durability 정의(`reference.langchain.com/python/langgraph/types/Durability`)·Postgres 체크포인터 README. 공식 durable execution 문서는 지금 주소(`…/langgraph/durable-execution`)가 개요 쪽으로 보이고 옛 GitHub 문서는 404 — 확인 필요(§14).

### 9-7. 걸린 시간·async 결론
- 04 b2·b4·b5의 「지연」 문장은 재지 않은 시간 단정(규격 §3) → 구조만 + 「걸린 시간은 이번에 재지 않았습니다」. async 저장 여부는 결론에서 빼고 「이번 실행에서는」(§7-1).

## 10. 삽화 비유 계열 후보

**이미 쓴 계열**(과정 요약·Ch 21 준비 조사·`figures/*.prompt.md` 174개 grep): 카드·봉투·서랍·쟁반·끈·단추·관·깔때기·그릇·클립보드·도장(stamp)·저울·나무 길·갈림길·레일·작업대(Ch 13·18)·나무판·구멍·마개(Ch 14)·사과·바구니·모래시계·궤짝·선반(Ch 15)·쪽지·덮개 천·두루마리·개찰구·체(Ch 16)·발자국·말뚝·울타리(Ch 17)·점토·물레·가마(Ch 18)·**식당 주문 전표와 내주는 창·같은 색 집게(Ch 19)**·**자료실 승강 상자·파란 책·빈 회색 카드(Ch 20)**·**세탁기(Ch 21)**·공항 검사·우편 가림막·전화 연결·방문자 명부·안내 데스크(Ch 22). grep에 이미 있는 말: `puzzle`·`jigsaw`·`brick`·`block`·`tape`·`sticky`·`shelf`·`bookshelf`·`envelope`·`clipboard`·`coin`·`key`·`padlock`·`plug`·`tent`·`rope`(5)·`hook`(2)·`camera`·`photo`(1씩). **0건**: `bookmark`·`ribbon`·`polaroid`·`chess`·`knitting`·`yarn`·`stitch`·`anchor`·`climb`·`cairn`·`lantern`·`candle`·`album`·`domino`·`abacus`·`punch card`.

| 후보 | 그림 요소(절별) | 장점 | 겹침·위험 |
|---|---|---|---|
| **A. 체스판과 즉석사진(폴라로이드)** — 한 수마다 판을 찍어 둔 사진 | 01 두 탁자에 각자 판과 사진 줄(스레드마다 따로) · 02 사진첩을 꽂을 선반을 벽에 먼저 다는 모습(`setup()`) · 03 다음 날 빈 판 옆 사진 한 장을 보고 말을 다시 놓음 · 04 사진이 다 나올 때까지 기다린 줄(sync) / **사진이 아직 하얗게 나오는 중인 줄**(async) / 끝날 때만 한 장인 줄(exit) + 쓰러진 말 · 05 나란한 두 판 중 한 판만 쓰러짐 · 06 같은 자리에 두 번 꽂힌 깃발 ↔ 한 번만 꽂히는 받침 | **async = 「아직 현상되는 사진」이 그대로 읽힘** · 0건 계열 · 글자 없이 판·사진·말로만 | 사진 속 작은 판이 판독 어렵고 생성 모델이 체스판 칸 수를 틀리기 쉬움 · 사람 손 없이 「찍는다」가 약함 |
| **B. 책갈피와 열람석 책**(자료실 계열 잇기) | 01 책마다 다른 색 책갈피(스레드) · 02 책갈피 보관 서랍장을 먼저 설치 · 03 다음 날 책갈피 자리에서 다시 펼침 · 04 장마다 책갈피를 옮긴 책(sync) / 넘기며 옮기는 중인 책(async) / 덮을 때만 꽂는 책(exit) + 바람에 덮인 책 · 05 나란히 펼친 두 권 중 한 권만 떨어짐 · 06 반납함에 같은 책 두 번 ↔ 한 칸짜리 반납 선반 | Ch 20·21·22의 자료실 소재와 이어짐 · 일상 물건 · 0건 | Ch 20 「자료실 승강 상자」와 장소가 같아 계열이 흐려짐 · 책갈피 위치 차이가 작게 보임 · 바람을 그리기 어려움 |
| **C. 뜨개질 바구니와 코 표시 고리** | 01 바구니마다 다른 색 실(스레드) · 03 다음 날 이어 뜨기 · 04 단마다 고리를 건 목도리(sync) / 걸고 있는 중(async) / 다 뜬 뒤에만 건 것(exit) + 바늘에서 빠져 풀린 코 — 고리에서 멈춤 ↔ 처음까지 풀림 · 05 두 소매 중 하나만 풀림 · 06 단추를 두 번 단 자리 ↔ 이미 달린 자리 | **「풀려도 마지막 고리에서 멈춘다」가 복구 범위를 그대로 보여 줌** · 0건 | 코·고리가 작아 판독 어려움 · 뜨개 무늬를 생성 모델이 뭉개기 쉬움 · 02 비유가 약함 |
| **D. 암벽의 확보 고리와 로프**(사람 없이) | 01 두 줄의 로프(스레드) · 02 벽에 고리를 먼저 박아 둔 모습(`setup()`) · 04 고리마다 건 로프(sync) / 거는 중(async) / 꼭대기에서만 건 로프(exit) — 떨어진 배낭이 마지막 고리에 걸림 ↔ 바닥까지 · 05 나란한 두 줄 중 한 줄만 풀림 · 06 같은 고리에 두 번 건 줄 | 「어디까지 떨어지는가」가 가장 선명 · 02 준비 단계와도 맞음 | 사람 없이 그리기 어려움(Ch 19·20 선례는 사람·손 없음) · 위험 느낌 · 06 비유 약함 · `rope`·`hook` 조금 씀 |

- 한 챕터 한 계열(Ch 19·20·21 선례). 사람·손·동물·화면·글자·숫자·화살표 없음이 선례. A·C는 「저장 시점의 차이(특히 async)」가, B는 앞 챕터와의 이음이, D는 「복구 범위」가 가장 잘 읽힘.

## 11. 위험과 깨진 것

1. **이 기기에서 옛 03·04·06이 실행되지 않음**(SQLite `disk I/O error` — §5-5) → 임시 폴더로 옮기지 않으면 새 커널 실행 자체가 안 됨.
2. **02는 PostgreSQL 서버가 필요**(§6) — Docker 없음, pgenv 바이너리는 있음. 선택을 먼저 정해야 02 작업이 시작됨.
3. **Ch 20 02·03 링크**: 슬러그 01·04·05·06은 바꾸면 끊김, 04는 강제 종료 장면·05는 실패 뒤 재개·06은 한 번만 반영 장면을 지켜야 링크 설명이 참.
4. **async 흔들림**(4/60) — 옛 결론 「async와 sync에는 first가 남았다」를 결론·정리·복습에 쓰면 규격 §2-7 9번 끝과 부딪힘.
5. **틀린 사실·실행하지 않은 사실**: 02 b3 「Ch4 … PostgreSQL·information_schema」 · 03 「연결을 닫습니다」(`with`는 안 닫음)·「database bytes 4096」 · 03·04 「SQLiteSaver」 · 01 Store · 04 「지연을 줄일 수 있지만」(안 잼) · 06 b7 interrupt(Ch 24) · b10 참고 자료가 절과 안 맞음.
6. **공용 옛 생성기**가 Ch 24 파일(노트북 셋·`_src` 셋·그림 생성기)을 함께 씀(§3).
7. **학생 쪽**: 포트 55432 충돌(Ch 12 컨테이너) · 실습 폴더에 `data/` 누적(임시 폴더로 풀림) · worker 30초 잠(실패하면 셀이 20초 기한에서 `AssertionError`) · Windows·macOS에서 `kill()`·SQLite 동작은 실행하지 않음(교재 출력은 Linux).
8. **뒤 챕터 인계**: Ch 31 05 b3(02 선택에 따라) · Ch 27 04 b3 「체크포인터 메시지」(03 선택에 따라) · Ch 22 09 b8(완료 — 03 선택에 따라 참/반참).
9. **서비스 요청 어림**: **M1(모델 없음)이면 0번**(비용 0, 키 셀 없음). M2로 03·07에 모델을 넣으면 03 2번 × (새 커널 2 + 노트북 밖 5) = 14 + 07 3~5번 × 7 = 21~35 → **약 35~50번**, 요금표 어림 0.05달러 아래(Ch 21 판 요금 mini 입력 0.75·출력 4.50달러/100만 토큰, 요청당 입력 약 500토큰 가정 — 청구 금액 아님). 삽화 7장(07 포함) 약 14크레딧(재생성 포함 최대 28).
10. **실행 시간**: 04 한 번 약 3.3초(모드당 약 1.1초), 06 약 2.2초, 02(A 선택) 서버 켜기 약 1~3초 — 셸 180초 안.

## 12. 01절 작업자가 먼저 결정해야 할 것

1. **파일 쓰기 자리** — 이 기기에서 SQLite는 연결 폴더에 쓸 수 없으므로 03·04·05·06·07의 파일(SQLite·ready·기록 파일)을 **임시 폴더**(`mkdtemp` → `os.chdir`, Ch 4 03 선례)로 옮길지, worker에 넘길 경로 모양, `upgrade_allow` 예외를 Part 6에서 어떻게 적을지. 01(`InMemorySaver`)부터 같은 준비 셀 모양을 쓸지.
2. **02 처리(§6)** — A(pgenv + `pre_exec.sh`, 교재는 Docker) / B·C(서버 없이, 제목·슬러그 변경 가능 — 링크 0) 가운데 무엇으로. A면 새 클러스터 자리(`.cache/vm/pgdata-ch23` ↔ `/tmp`)와 포트(55432 그대로 ↔ 다른 포트, 학생 쪽 Ch 12 충돌 안내), B·C면 Ch 31 05 인계 문장. b3 Ch 4 → Ch 12 02는 어느 쪽이든.
3. **모델을 넣을지(§9-1)** — M1(없음) / M2(03·07에 실제 모델, `uv lock` 필요) / M3(모델 없이 메시지 칸). Ch 22 09 b8·Ch 27 04 b3과의 관계가 여기서 정해짐. 01의 상태·출력 모양(글 목록 ↔ 메시지)을 챕터 전체에 맞출지.
4. **강제 종료와 도구 파일(§7·§8)** — 04 강제 종료 유지(Ch 20 링크) + 06을 강제 종료로 둘지 실패 흉내로 바꿀지, 도구 파일 A/B/C/D, worker 파일을 도구 파일 규칙(금지 문법 0·한국어 주석)으로 고칠지.
5. **결론 기준과 `assert` 대상** — 04는 exit ↔ sync(결정적)만 결론, async는 둘째 단락(60번 확인 기록은 진단 b7) · 05는 호출 수·채널 이름(차례 아님) · 걸린 시간은 재지 않음 · 노드 힌트 빼기 · 용어 표(단계·남은 쓰기·재개·멱등·「스키마」·「마이그레이션」 대체 말)를 01에서 정해 `handoff.md`에.

## 13. 챕터 마감으로 미룰 것

- **07 실습 절 신설**(규격 §7-2): 슬러그 후보 **`07-Persistence-실습`**(선례 `09-Middleware-실습`·`07-create-agent-실습`·`05-ToolNode-실습`·`08-LangGraph-실습`·`06-Agent-개요-실습`·`07-모델과-도구-실습` — 챕터 제목의 앞말), 제목 「Persistence 실습: …」, `format: experiment`, meta 「실습 30분 · 새 용어 0」(**챕터 시수 6·10h에 더하지 않음**). 새 문법·API 0. 주제 예 — 자료실 대출 신청 흐름(Ch 20~22 자료실 소재): 대출 기록 노드(멱등 키로 기록 파일에 한 줄) → 알림 노드(실패 흉내) · 이용자별 스레드 · 실패 뒤 `invoke(None, config)`로 재개 · 실행 1(`sync`·멱등 키) ↔ 실행 2(값 하나만 — 전략 naive 또는 모드 exit). 모델 요청은 §9-1 선택에 따라 0 또는 3~5(0이면 §7-2 분량 설명과 다름을 챕터 요약·강사 확인에). 파일은 임시 폴더에만(Part 3 실습 절 「파일을 쓰지 않습니다」 선례와 다름을 적음). 따라오는 것: `chapter.json` 절 추가 · `textbook/part6/_build_index.py` 21행(시수 6·10 그대로, 설명) · 챕터 `qa/public-files.json`(경로 배열 — 노트북·HTML 줄 직접) + `textbook/part6/public-files.json` · `textbook/_notebook/build_index.py` 50행(절 수 6, 선례대로 둘지) · `check_scope.py`(기록만) · 06 「다음 학습과 이어지는 지점」을 07로.
- 옛 생성기 `figures/_gen_figures.py` `mv -n` → `qa/upgrade/before/generators/blocked/` · **공용 `qa/author_ch23_ch24.py`는 Ch 24 몫과 함께 정함**(§3).
- 옛 그림 18개(`figures/0N-흐름.{svg,excalidraw,caption.md}`) 삭제 승인 목록(사본 `before/figures/`, `final-artifact-hashes.json`이 해시를 적어 둔 기록 파일).
- `chapter.json` `objectives`·절 제목, `textbook/part6/_build_index.py` 21행 설명을 개선 본문과 대조 → `_build.py`·`_build_index.py`.
- 실습 폴더 README 다시 쓰기(노트북 일곱, `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 02 서버 안내·포트, 파일이 임시 폴더에 생긴다는 문장, 요청 수) · `labs/part6/continuity-guide.md`(worker·도구 파일이 바뀌면) · `qa/research.md`·`verification.md`·`집필점검표.md`(「개선 전 판」 표시 — 학생 묶음 밖).
- `part6-practice.zip` 재생성(`python3 textbook/part6/_build_index.py`) → `check_delivery.py`(`llm-practice.zip` Stale 예상) · 옛 검사 넷 돌려 기록(`check_notebook_readiness.py`는 결과 파일 되돌림) · `check_bundle_execution.py`(Ch 23 안 돌림 — Ch 24·28 PASS만 확인).
- **뒤 챕터 인계**: Ch 24 01 b3 · Ch 25 01~03 b3 · Ch 26 01~04 b3 · Ch 27 01·04 b3 · Ch 30 02·06 b3 · **Ch 31 02·05 b3(02 선택)** · Part 6 소개·`practice-start.md`·continuity-guide 둘 · Ch 20(완료) 02·03 b7 링크와 Ch 21 03·07·Ch 22 09 문장 대조 · 공용 생성기의 Ch 24 쪽.
- 삭제 승인 대상: 실습 폴더 `.venv`(macOS 142MB) · `qa/upgrade/gates-wip-*.json` · `qa/upgrade/__pycache__` · `.cache/vm/venv-ch23-persistence`(233MB) · **`$ROOT/.cache/ch23-prep/`(SQLite 시험 파일 넷, 4.6KB)** · 기기 `/tmp/ch23-prep`(44MB — 임시 PostgreSQL 클러스터 `pgtest` 39MB 포함, 서버는 꺼 둠) · 02를 A로 하면 새 클러스터.

## 14. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 6 · `notebooks` 6 · `figures` 19(SVG·excalidraw·caption 각 6 + `_gen_figures.py`) · `generators` 2(**공용 `author_ch23_ch24.py` 사본**·`_gen_figures.py`) · `qa` 3(`public-files.json`·`research.md`·`verification.md`) · 실습 폴더 5(`pyproject.toml`·`uv.lock`·`README.md`·`durability_worker.py`·`idempotency_worker.py`) · `chapter.json`·`집필점검표.md`·`_build.py`·`index.html`(목차, objectives 대조용) = **45개, 544KB**. 원본과 `cmp` 모두 같음(원본은 그대로). `runs/`·`tests/`·`data/`는 실습 폴더에 없어 없음 |
| `qa/upgrade/gates-before.json` | §0 표(절별 G1~G7 · 합계 205, 통과 0/6), `a6f875a1…` |
| `qa/upgrade/before-manifest.json` | sha256 **123개**(`c50e96c8…`) — ① 이 챕터가 읽거나 가져올 수 있는 파일: 실습 폴더 11 · Ch 4 03·Ch 12 02 노트북 · Ch 12 `pre_exec.sh` · 도구 파일 일곱(Ch 13·16~21, 이름 피하기용) · Ch 21 `pyproject.toml`·`uv.lock` · Ch 22 `pyproject.toml` ② Ch 23을 링크·언급하는 완료 챕터 파일: Ch 20 02·03 `_src`·HTML·`author_02.py`·`author_03.py` · Ch 21 03·07 `_src`·HTML · Ch 22 09 `_src`·HTML ③ Ch 23에 기대는 대기 챕터 파일: Ch 24 01 · Ch 25 01~03 · Ch 26 01~04 · Ch 27 01·04 · Ch 30 02·06·`_generate.py` · Ch 31 02·05 `_src`·05 노트북·README · Part 6 소개·`practice-start.md`·continuity-guide 둘·`_generate_ch25_ch26.py` ④ 공용 생성기가 함께 쓰는 Ch 24 파일: 생성기·Ch 23/24 `_gen_figures.py`·Ch 24 `_src` 셋·노트북 셋·`chapter.json`·`pyproject.toml` · `part6a_enrich.py` ⑤ 묶음·목록·기록: `part6`·`part7`·`llm-practice.zip` · Part 6 목록 둘 · 챕터 `qa/` 셋 · Part 6 `qa/*.json` 열둘·`ch23-technical-review.md`·색·언어 기록 · Part 7 기록 셋 · `notebook-contracts-part6-ch23-persistence.json`·`checks/ch23-persistence/visual-results.json` · `textbook/index.html`·`part6/index.html` ⑥ 규칙·검사·빌드: `part6/_build_index.py` · `_notebook/build_index.py`·`build_bundle.py`·`verify.py`·`execute.py` · Part 6 검사 일곱 · `_template/builder.py` · 챕터 `_build.py`·`chapter.json` · `run_section.sh`·`nbkit.py`·`upgrade_gates.py` · `check_course_continuity.py` |
| `$ROOT/.cache/vm/venv-ch23-persistence` | Python 3.12.13 · 233MB |

### 가상환경 만든 방법과 결과

- `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy uv venv --python 3.12.13 …/venv-ch23-persistence`. 잠금 목록은 `uv export --project labs/part6/ch23-persistence --frozen --no-hashes --all-groups --no-emit-project`(실습 폴더 파일은 그대로 — `pyproject.toml`·`uv.lock` 수정 시각 09-10 그대로), 주석·빈 줄만 빼고 환경 표시는 남김(88줄, `/tmp/ch23-prep/req-clean.txt`).
- Ch 21 준비 선례대로 `uv pip install pip==26.2` → **`bin/python -m pip install --no-cache-dir -r`**. 설치 오류 0, **uv 캐시 정리(`uv cache prune`) 안 함**. 기기 루트 디스크 여유 **1.7G**(작업 전후 같음), `/tmp/uv-cache` 387MB 그대로.
- 결과: `pip freeze`와 잠금 대조 **판 차이 0**(설치 82 = 잠금 88 − 이 기기에 해당하지 않는 여섯: `appnope`(darwin)·`colorama`·`tzdata`(win32)·`cffi`·`pycparser`(PyPy)·`httpx2-jsfetch`(emscripten)). **`psycopg-binary 3.3.3`은 aarch64 바퀴 파일로 설치됨**(`psycopg.pq.__impl__` = `binary`, libpq 180000). `pip check` 이상 없음. 커널 스펙 `share/jupyter/kernels/python3` 있음.
- import 확인만: `InMemorySaver` · `SqliteSaver`·`AsyncSqliteSaver` · `PostgresSaver`·`AsyncPostgresSaver` · `StateGraph`·`START`·`END` · `Command`·`interrupt`·`Durability`(= `Literal['sync', 'async', 'exit']`) · `psycopg`·`psycopg_pool`·`sqlite3`(3.53.1). `langchain`·`openai`·`dotenv`은 없음(잠금대로). `run_section.sh`는 `$ROOT/.cache/vm/venv-<챕터 폴더 이름>`을 자동으로 씁니다.

### 참고 자료 (2026-09-25 확인)
- Checkpointers `https://docs.langchain.com/oss/python/langgraph/checkpointers`(남은 쓰기 두 문장 · START → A → B → END 네 체크포인트 · 기록은 최신 것부터 · `StateSnapshot` 칸 · SQLite 「experimentation and local workflows」·Postgres 「production」 · durability 셋).
- Persistence `https://docs.langchain.com/oss/python/langgraph/persistence`(`thread_id` 설정 · PostgreSQL 체크포인터의 `thread_id` 255자 안 · `setup()` 필요).
- Durability 정의 `https://reference.langchain.com/python/langgraph/types/Durability`(설치판 `types.py` 89~95행과 같은 글).
- Durable execution 문서: 공식 주소 `https://docs.langchain.com/oss/python/langgraph/durable-execution`는 이번에 개요 글만 받음 · 옛 GitHub 문서 `docs/docs/concepts/durable_execution.md`는 404 · 미러(비공식)에 「exit … only when graph execution exits either successfully, with an error, or due to a human in the loop interrupt」·「replay all steps from the starting point」·「ensure that side effects … are idempotent」 — **01절 작업 때 공식 주소를 다시 확인할 것**.
- 설치판 소스: `langgraph/types.py` 89~95·637~646행 · `langgraph/pregel/main.py` 2602~2603·2700~2712·2802~2804·2987~2988행 · `langgraph/pregel/_loop.py` 466·1132~1134·1324~1333행 · `langgraph/checkpoint/sqlite/__init__.py` 92~159행 · `langgraph/checkpoint/postgres/base.py` 37~85행 · `langgraph/checkpoint/postgres/__init__.py` 37~102행 · `langgraph/checkpoint/memory/__init__.py` 625행(`MemorySaver = InMemorySaver`).
