# Ch 23 Persistence와 Durable Execution — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part6/ch23-persistence` 01~06절(품질 개선) + **07절 챕터 끝 실습 절 신설**(`07-Persistence-실습`), 노트북 `labs/part6/ch23-persistence/notebooks/01~07-*.ipynb`, 도구 파일 `notebooks/checkpoint_tools.py`, worker 스크립트 둘(`durability_worker.py`·`idempotency_worker.py`, 실습 폴더 맨 위). 계약 파일(뒤 챕터가 읽는 산출 파일)은 없습니다.
- 기간: 2026-09-25(준비 조사 · 01~06절 개선 · 07절 신설 · 검토 1차 반영 · 챕터 마감). 상태: **완료(강사 확인 대기)**.
- 게이트: 수정 전 여섯 절 합계 **205**(G1 19 · G2 14 · G5 32 · G6 122 · G7 18 — 01 32 · 02 40 · 03 25 · 04 44 · 05 36 · 06 28, `gates-before.json`) → 마감 뒤 **7/7 PASS, G1~G7 모두 0**(`gates-after.json`, 검사 문장 352·377·364·393·307·356·344 = **2,493**).
- 코드 셀 28·28·29·27·21·23·22 = **178**(`verify.py --chapter` → `PASS 7 sections / 178 code cells (max 14 lines)` — 14줄은 준비 셀). Mermaid **27장**(01~06 넷씩 · 07 셋), 삽화 **7장**(절마다 하나, Higgsfield 18크레딧 — 01·02는 2차 채택 4크레딧씩, 마감 0), 복습 문제는 HTML에만.
- **모델 요청 0번(일곱 절 모두)** — 챕터 리드 결정 1. API 키 셀·모델 셀 없음, 실습 폴더 잠금에 모델 패키지 없음. 대화가 필요한 03·07의 글은 노드 함수가 만든 글입니다.
- 화면 검사 `visual.cjs`: HTML **여덟 개**(일곱 절 + `index.html`) × 1280px·390px = **16행 PASS**.
- **마감에서 다시 실행한 노트북: 04·06·07**(검토 B-1 [상] 코드 고침 — 모두 모델 요청 0·결정적). 01·02·03·05는 `code_sha256`·`outputs_sha256`·`executed_at` 전후 같음(마크다운만 — 02는 PostgreSQL 서버를 켜지 않음).
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 21 요약 → **이 문서** → `handoff.md`(절 사이 세부, 끝 「검토 반영과 챕터 마감 (2026-09-25)」) → 절별 `NN-diagnosis.md`(끝 「마감 반영」) → 검토 `review-round1-A.md`(01~03·공통)·`review-round1-B.md`(04~07) → 노트북 밖 확인 `04·05·06-probe.md` → 준비 조사 `chapter-lead-notes.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 문법·API | 새로 만든 함수 (도구 파일에 둔 것은 굵게) | 새 용어 |
|---|---|---|---|
| 01 체크포인터와 스레드 (experiment) | **`InMemorySaver()`** · **`builder.compile(checkpointer=memory)`**(같은 설계 객체로 `compile()`과 둘 만듦, 속성 `checkpointer`) · 설정 딕셔너리 `{"configurable": {"thread_id": …}}` · **`get_state(config)`**(`values`·`next`·`metadata["step"]`·`["source"]`) · **`list(get_state_history(config))`**(최신 것부터) · 설정 없이 부르면 `ValueError` · 없는 스레드는 `{}`·`()` · 체크포인터 없는 그래프의 둘째 입력 `KeyError` | `print_history`·`thread_row`(노트북) | 체크포인터 · 체크포인트 · 스레드 (3) |
| 02 PostgresSaver 준비와 스키마 (paired) | `psycopg.connect(…, autocommit=True, row_factory=dict_row)`(Ch 12 02 접속 글) · `CREATE SCHEMA`·`SET search_path` · **`PostgresSaver(conn)`** · 속성 `MIGRATIONS`(표 만들기 문장 열) · **Before: `setup()` 없이 실행 → `UndefinedTable`(`42P01`)** · **After: `setup()`** → 표 넷·기록 `checkpoint_migrations` 열 줄 · `information_schema`로 표·칸 읽기 · `psycopg.Error`·`diag.sqlstate`·`diag.message_primary` | `table_names`·`column_names`·`count_checkpoints`(노트북) | 이름 공간(SQL `SCHEMA`) · 표 만들기(`setup()`) · 표 만들기 기록 (3) |
| 03 스레드 재개와 대화 이어가기 (experiment) | **`sqlite3.connect(…, check_same_thread=False)` → `SqliteSaver(conn)`** · `close()` 뒤 옛 그래프 `ProgrammingError` · 새 연결·새 체크포인터·새 그래프로 같은 스레드 이어 가기 · 메시지 칸 `add_messages`에 코드가 만든 `HumanMessage`·`AIMessage` · 표 `sqlite_master` · **`with SqliteSaver.from_conn_string(…) as …:`**(블록이 끝나면 연결을 닫음) | `print_conversation`·`sqlite_tables`(노트북) | SQLite 체크포인터 · 객체의 수명 · 스레드 재개 (3) |
| 04 내구 실행 모드 비교 (experiment) | **`invoke(…, durability="exit"/"async"/"sync")`** · **`subprocess.Popen([sys.executable, …])`·`kill()`·`wait(timeout=)`**(종료 코드 Linux `-9`) · `time.perf_counter()` 기한 루프·`time.sleep` · `os.path.exists`·`os.path.abspath` · 자리 찾기 셀 · worker의 `sys.argv`·`invoke(None, config, durability=…)`(스크립트 안에서만) · **마감: 띄우기·기다리기·끊기를 한 셀에서 + `assert` 둘(신호·종료 코드가 0이 아님)** | **`start_worker`·`wait_for_signal`·`stop_worker`·`read_saved`·`read_record`·`new_prefix`(마감)·`kill_at_second`**(06이 도구 파일로 옮김) | 저장 시점(durability) · 자식 프로세스 · 강제 종료 · 신호 파일 (4) |
| 05 pending writes와 장애 복구 (experiment) | 고정 엣지 둘로 같은 단계의 두 노드 `good`·`flaky` · 딕셔너리 `failure_plan`·`call_count`(Ch 16 05 모양, 0.1초 쉰 뒤 `TimeoutError`) · **`get_state(config).tasks`**(`name`·`error`·`result`) · 표 `writes` 조회 · **노트북 셀에서 처음 `invoke(None, config)`** · `durability="exit"`로 같은 실패 | `saved_channels`(노트북) | 남은 쓰기 · 작업(task) · 장애 복구 (3) |
| 06 노드 재시작과 멱등성 (paired) | `with open(…, "a", encoding="utf-8")` · `read().split()` · 목록 `count` · 읽기용 노드(설계 객체를 읽기에만) · **Before `naive` 두 줄 ↔ After `idempotent` 한 줄** | **`append_key`·`append_key_once`·`kill_then_resume`**(이 절이 도구 파일을 처음 만듦) | 노드 재시작 · 멱등성 · 멱등 키 (3) |
| 07 Persistence 실습 | **새 문법·새 API 0**(01~06 이름만 — 01~06에 없는 내장 이름·속성·키워드 0) | 0(상태 형식 `LoanState`와 노드 둘만 노트북에) | 0 |

- 새 용어 합계 **19개**(절 meta 「새 용어」 3·3·3·4·3·3·0).
- **이 챕터 주제라서 허용한 문법**(챕터 리드 결정 8): 칸만 적은 `TypedDict` 상태 형식(칸 구성이 바뀌면 새 이름 — `CountState`·`ConversationState`·`StepState`·`ResultState`·`OrderState`·`LoanState`) · 리듀서 `operator.add`·`add_messages` · `with`(파일 `open` 밖은 03 `SqliteSaver.from_conn_string` 하나) · `subprocess.Popen`(04 — 과정은 Ch 2 08 `subprocess.run`까지) · 준비 셀 `assert root_path is not None`.
- **쓰지 않은 것(일곱 절 모두 0건, AST 확인)**: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·튜플 풀기·별표 풀기·세미콜론·`isinstance`·데코레이터·`try`/`finally`·`with sqlite3.connect`(연결을 닫지 않음)·`Path`·`AsyncSqliteSaver`·`psycopg_pool`·`interrupt`·`Command`·`update_state`·`stream`·모델. 마감 AST 따로(`extra_check.py`): 노트북 일곱·도구 파일·worker 둘 금지 문법 0, 허용 표시만(키워드 없는 `sorted` 열 곳·03 `with` 하나).
- 셀 모양: 준비 셀이 아닌 셀 최대 12줄(04 끊는 셀 — 마감), 함수 본문 최대 8줄(`read_saved`·`kill_at_second`·07 `record_loan`은 9줄 — 한도 10), 셀당 함수 하나, 첫 줄 주석 100%. `assert`는 우리 코드가 정하는 값(체크포인트 수·줄 수·합계·종료 코드)에만.

## 2. 앞 챕터에서 이어 쓴 부품과 값

- **Ch 4 03**: 임시 폴더 준비 셀(`tempfile.mkdtemp(prefix=…)`·`os.chdir`·`os.listdir()`) — 일곱 절이 앞머리 `ch23-NN-`만 다르고 글자까지 같은 셀(생성기 `assert`), SQLite `connect`/`close`·자리표시자 `?`·`SELECT … WHERE … ORDER BY`.
- **Ch 10 02**: `with pdfplumber.open(…)` — 03 `with SqliteSaver.from_conn_string` 설명의 선례(마감 A-13, 라이브러리 객체를 블록이 끝나면 닫음). Ch 2 05 `with open`도 함께.
- **Ch 12 02**: PostgreSQL 컨테이너 `hankyung-part3-pgvector`·접속 글 `postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab`·`%s`·`except psycopg.Error as error`·`diag.message_primary` — 02가 그대로(이름 공간 `ch23_lab`만 씀, Ch 12 표는 기본 이름 공간이라 겹치지 않음). 작업 기기는 Ch 12가 둔 conda-forge PostgreSQL 17.11(`.cache/vm/pgenv`)로 새 클러스터.
- **Ch 13**: 상태·상태 형식·노드·엣지·설계 객체·컴파일·가상 시작점/끝점·리듀서·이어 붙이기·메시지 리듀서(04 import 줄)·팬아웃(05 — 마감 B-9에서 「여러 갈래로 펼친 것처럼」으로 뜻을 맞춤).
- **Ch 16 05**: 실패 흉내 `failure_plan`·`call_count`·`time.sleep`(05·07). **Ch 15 05** `time.perf_counter()`(04 기한 루프 — 걸린 시간 재기 아님). **Ch 17 02** 부작용(06). **Ch 17 05** 자리 찾기 셀 모양(04·06).
- **Ch 20**: 단계(03 — 체크포인트가 쌓이는 차례)·설정 딕셔너리·실행 한도 · Ch 20 02·03 b7이 04·05·06 슬러그를 링크(슬러그 고정).
- **Ch 21**: 03 이용자 번호 `M-0317`(07 스레드 이름) · 03 b4·b7 「결과 상태를 저장해 다음 실행에 이어 쓰는 방법은 Ch 23에서」 → 01로 참. Ch 21 `runner_tools.py`는 쓰지 않음(모델 없는 챕터).

## 3. 절별 사례·값 (새 커널 두 번과 노트북 밖 확인에서 같았던 값)

| 절 | 과제·입력 | 결정적 값(결론·그림에 쓴 값) |
|---|---|---|
| 01 | 노드 `add_amount`(합계 += 이번 수) · 스레드 `customer-a` 3 → 4 · `customer-b` · `customer-c`(둘째 입력에 합계 0) | 체크포인터 없음 둘째 실행 `KeyError: 'total'` · `customer-a` 합계 3 → 7·체크포인트 6(실행 한 번에 셋 — `input`·`loop`·`loop`, 단계 -1~4) · `customer-a \| 7 \| ['add', 'add'] \| 6`·`customer-b \| 4 \| ['add'] \| 3`·`customer-c \| 4 \| ['add', 'add'] \| 6` · 없는 스레드 `{}`·`()` · `InMemorySaver`는 파일 0 |
| 02 | 01 상태 형식·노드(글자 그대로) · 이름 공간 `ch23_lab` | Before `받은 오류: UndefinedTable`·`42P01`·표 `[]` · After `setup() 뒤 표 수: 4`·기록 `[0, 1, …, 9]`·합계 3 → 7 · 표 `checkpoints` 칸 일곱·`customer-a` 6줄 · `setup()` 한 번 더 → 10줄 그대로 · `customer-b` 3줄 · 연결 닫은 뒤에도 6 |
| 03 | 메시지 칸, 노드 `reply`(「N번째 질문을 받았습니다」) · 스레드 `conversation-a`·`-b` · 파일 `chat.sqlite`·`other.sqlite` | 첫 실행 뒤 표 `['checkpoints', 'writes']`(`setup()`을 부르지 않아도) · 메시지 넷·체크포인트 6·열린 동안 파일 셋 → 닫은 뒤 하나 · 옛 그래프 `ProgrammingError` · 새 연결·새 그래프 `단계 번호: 4` → 셋째 질문 `3번째 질문을 받았습니다`·메시지 6·체크포인트 9 · `conversation-b \| 3` · 다른 파일 `{}` · `with` 블록 뒤 `ProgrammingError` |
| 04 | worker 노드 `first` → `second`(둘째 노드는 신호 파일을 만들고 첫 실행 단계에서 30초 쉼) · 저장 시점 셋 | 끝까지 실행 `exit 1`·`async 4`·`sync 4` · 둘째 노드에서 강제 종료(`-9`) 뒤 `exit` `{}`·`()`·0 ↔ `sync` `{'completed': ['first']}`·`('second',)`·3 · 다시 실행한 뒤 기록 `first, second, first, second` ↔ `first, second, second`·체크포인트 1 ↔ 4 · 되풀이 `exit \| 0 \| 5`·`sync \| 5 \| 5` · 파일 52(4절 `exit-1.sqlite`) · 자식 프로세스 19번·강제 종료 17번 |
| 05 | 같은 단계의 `good`·`flaky`(0.1초 뒤 `TimeoutError`) · 스레드 `pending-a`(기본값)·`exit-run` | `부른 횟수: {'good': 1, 'flaky': 1}` → 이어 간 뒤 `{'good': 1, 'flaky': 2}` · `다음 노드: ('flaky',)` · 표 `writes` `good \| ['results']`·`flaky \| ['__error__']` · 체크포인트 기본값 2 → 3 / `exit` 1 → 2 |
| 06 | worker 노드 `receive_order` → `charge`(결제 기록에 `order-2306`을 적은 뒤 신호·쉼), 저장 시점 `sync` · 쓰기 방식 `naive`/`idempotent` | 2절 `적음 적음`·두 줄 ↔ `적음 건너뜀`·한 줄 · 끊긴 뒤 `{'order_key': 'order-2306', 'notes': ['주문 받음']}`·`('charge',)`·3·키 한 줄 · 다시 실행 뒤 4 · Before `['주문 받음', '적음']`·두 줄 ↔ After `['주문 받음', '건너뜀']`·한 줄 · `naive \| 0 \| 5`·`idempotent \| 5 \| 5` · 파일 38(4절 `naive-1.record`) · 자식 프로세스 24번·강제 종료 12번 |
| 07 | §7 | §7 |

## 4. 용어 (챕터 안에서 한 번만 정의하고 이어 씀)

| 절 | 말 | 뜻 | 코드에서 |
|---|---|---|---|
| 01 | 체크포인터(checkpointer) | 그래프가 단계를 하나 마칠 때마다 그때의 상태를 저장해 두는 부품(입력을 받은 때의 체크포인트는 첫 단계 0보다 앞이라 번호 -1 — 마감 A-3) | `InMemorySaver()` → `compile(checkpointer=…)` |
| 01 | 체크포인트(checkpoint) | 체크포인터가 한 번 저장한 상태 하나 | `get_state_history`의 항목 |
| 01 | 스레드(thread) | 한 이름으로 묶인 체크포인트들의 줄(이름은 설정 딕셔너리의 `thread_id`) | `{"configurable": {"thread_id": "customer-a"}}` |
| 02 | 이름 공간(SQL 낱말 `SCHEMA`) | 한 데이터베이스 안에서 표들을 이름으로 묶어 두는 자리 — **제목의 「스키마」(표들의 구조)와 나눠 씀**(마감 A-10) | `CREATE SCHEMA ch23_lab` |
| 02 | 표 만들기(`setup()`) | 체크포인터가 쓸 표를 데이터베이스에 만드는 일(DB 「마이그레이션」 대신 — Ch 21 04 「옮기기」와 다른 뜻) | `saver.setup()` |
| 02 | 표 만들기 기록 | 표 만들기 문장 가운데 어디까지 실행했는지 판 번호로 적어 두는 표 | 표 `checkpoint_migrations` |
| 03 | SQLite 체크포인터 | 체크포인트를 SQLite 파일 하나의 표에 쓰는 체크포인터 | `SqliteSaver(conn)` |
| 03 | 객체의 수명 | 객체를 만든 때부터, 닫혀서 더 쓸 수 없게 된 때까지 | `close()` 뒤 `ProgrammingError` |
| 03 | 스레드 재개 | 객체를 새로 만든 뒤 같은 스레드 이름으로 마지막 체크포인트부터 대화를 이어 가는 일 — **영어 괄호 뺌, Ch 24 `Command(resume=…)`와 다른 장면**(마감 A-16) | `second_graph.invoke(…, config_a)` |
| 04 | 저장 시점(durability) | 그래프가 체크포인트 저장을 언제 끝내는지 정하는 값(「내구」는 제목에만) | `durability="exit"/"async"/"sync"` |
| 04 | 자식 프로세스 | 실행 중인 프로그램(프로세스)이 띄운 또 하나의 프로그램(마감 B-4) | `subprocess.Popen(command)` |
| 04 | 강제 종료 | 프로그램이 스스로 끝나기를 기다리지 않고 운영체제가 그 자리에서 끝내는 일 | `process.kill()` |
| 04 | 신호 파일 | 자식 프로세스가 어디까지 왔는지 알리려고 만드는 파일 | `wait_for_signal` |
| 05 | 남은 쓰기 | 같은 단계에서 먼저 끝난 노드가 낸 갱신 가운데, 단계가 끝나지 못해 칸 값에 합쳐지지 않은 채 체크포인트에 딸려 저장된 것(「pending writes」는 제목에만) | 표 `writes` |
| 05 | 작업(task) | 한 단계에서 노드 하나를 한 번 실행하는 일 | `get_state(config).tasks` |
| 05 | 장애 복구 | 멈춘 실행의 원인을 없앤 뒤 저장된 자리부터 이어 가 끝내는 일 | `invoke(None, config)` |
| 06 | 노드 재시작 | 끊긴 노드를 이어 갈 때 그 노드를 처음부터 다시 실행하는 일(「재시작」은 06 제목 말 — 다른 절 본문은 「다시 실행」) | worker 다시 실행 단계 |
| 06 | 멱등성(idempotency) | 몇 번 실행해도 결과가 한 번 실행한 것과 같은 성질 | `append_key_once` |
| 06 | 멱등 키(idempotency key) | 같은 일을 다시 해도 한 번만 반영하려고 일마다 붙여 두는 이름 | `order-2306`·07 `loan-2307` |

- **일반 말(새 말 아님)**: **상태 저장(Persistence 풀이) · 이어 실행(Durable Execution 풀이 — 「멈춘 실행을 저장된 자리부터 이어 가는 일」 한 뜻만, 마감 A-1)** · **같은 스레드로 다시 실행**(끝까지 간 실행 뒤 같은 스레드로 새 입력을 넣는 다음 실행 — 01 b4·6절·b6, 02, 07 b3) · 스레드 이름 · 마지막 체크포인트 · 단계 번호 · 만든 자리 · 다음 노드 · 저장된 칸 값 · 임시 폴더 · 파일 앞머리(마감 — `new_prefix`가 고르는 `이름-번호`) · 실행 흐름(03 — 한 프로그램 안에서 따로 도는 일의 줄, `check_same_thread`의 thread, **챕터의 스레드와 다름** — 마감 A-15) · 실패 흉내 · 쓰기 방식.
- **이어 쓰는 말**: Ch 13 상태·상태 형식·노드·엣지·설계 객체·컴파일·실행 흔적·가상 시작점/끝점·리듀서·덮어쓰기·이어 붙이기·메시지 리듀서·갱신 · Ch 20 단계·설정 딕셔너리 · Ch 16 05 실패 흉내 · Ch 17 02 부작용.
- **금지어(일곱 절 설명·주석·캡션·`.mmd`·README 0건 — 제목·슬러그·코드 백틱 말고)**: 「지시」·「반환」·「추정」·「지연」·「분기」·「경로」·「trace」·「스키마」·「superstep」·「병렬」·「스냅샷」·「채널」·「식별자」·「레코드」·「로그」(「프로그램」 안 글자 말고)·「마이그레이션」(DB 뜻)·「런타임」·「트랜잭션」·「원자적」·「경합」·「보장」·「정확히 한 번」·「측정」·「검증」·「필드」·「인터페이스」·「사전」·「동시」·「순차」·「돌려줍니다」류·「쉽게·간단히·당연히」·「개선 전」·「강사 시연」·「재시작」(06 제목·정의 자리 말고). 마감 전후 금지어 목록(`.cache/ch23-close/log/ban-pre.txt`) — 마감이 더한 문장의 참 금지어 0.
- 제목 말 「Persistence」·「Durable Execution」(챕터)·「PostgresSaver」·「스키마」(02)·「내구 실행 모드」(04)·「pending writes」(05)·「노드 재시작」·「멱등성」(06)·「Persistence 실습」(07)은 제목과 본문 첫 풀이에만(강사 확인).

## 5. 색 규칙 (Mermaid 27장)

- **넘긴 값·입력·설정 딕셔너리·바꾼 값 초록(tool)** · **우리가 적은 설계 객체·노드 함수·상태 형식·도움 함수·worker 코드 파랑(flow)** · **출력으로 확인한 값·셀에서 받아 출력한 오류(experiment) 노랑(measure)** · **라이브러리가 만든 그래프·체크포인터·공통 사실·테두리 칸 회색(클래스 없음)** · **모델 없음 → 보라 0장**.
- **빨강은 paired 절 Before 결함 결과만**: 02-3 Before 두 상자(`UndefinedTable` — 받아 출력했지만 paired Before 결함 결과, Ch 19 01 선례) · 06-4 Before 한 상자(같은 키 두 줄). experiment 절(01·03·04·05·07)은 빨강 0 — 03 `ProgrammingError`·01 `KeyError`·`ValueError`는 노랑.
- 나란한 칸은 subgraph + `~~~` 회색 공통 상자(공통 상자에는 모든 칸 출력에서 확인한 값만 — 01-4 둘째 줄은 a·c 칸만 해당함을 마감 A-2에서 도식 읽기에 밝힘). 스레드를 고르는 갈래·함수가 고르는 갈래는 점선. 체크포인트 목록은 오래된 것부터 그리고 「출력은 최신 것부터」를 도식 읽기에. 원본 viewBox 폭 모두 868 이하(최대 836).
- **마감에서 다시 렌더한 `.mmd`: `04-2` 하나**(검토 B-1 — 위 네 상자를 회색 테두리 칸 「4·5절 셀 하나」로 묶음, 폭 274 → 318, `--force`, 노트북 첨부 PNG 새 판, PNG 직접 확인). 01-4·07-4는 글만 고침.
- **비유 계열 「체스판과 즉석사진」**: 체스판 = 스레드의 상태 · 즉석사진 한 장 = 체크포인트 · 카메라(와 사진 모으기) = 체크포인터 · 판 하나와 그 앞 사진 묶음 = 스레드. 01 탁자 둘·사진 여섯/셋·카메라 하나 · 02 속지를 끼운 사진첩 ↔ 빈 사진첩(이름 공간 = 사진첩, 표 = 속지 — 마감 A-17: 01은 사진첩까지 카메라가 들고 있고 02는 카메라 밖에) · 03 판 앞 사진 한 장·닫힌 사진첩·빈 상자 · 04 쓰러진 판 둘, 왼쪽(`sync`) 사진 셋 · 05 한 탁자에 판 둘, 한 판만 쓰러짐 · 06 같은 수를 두 번 적은 기보 ↔ 한 번 · 07 판 앞 사진 한 장과 기보 한 장, 리본(판 가장자리에서 두 물건 사이로 — 두 물건이 한 판에 딸린 소품, 마감 B-13). 사람·손·화살표·글자·숫자·시계 없음.

## 6. 결정적 값과 흔들린 값

- **흔들린 값은 04 `async` 강제 종료 결과 하나**: 04 6절 되풀이 셀의 `async` 줄 — 개선 때 교재 출력 4/5(B 5/5) → **마감 교재 출력 `async | 5 | 5`(B `async | 4 | 5`)**. 준비 확인 60번 가운데 4번 잃음 · 고친 worker 40번 모두 남음. 결과 읽기 **둘째 단락과 b7에만** 「이번 실행에서는 …·새 커널로 한 번 더 실행했을 때는 …」, 첫 단락·정리·그림·캡션·복습·b6 표에는 값 없음(b6 셋째 단락은 값 없이 「async 줄 하나뿐」). 흔들림 자체가 공식 문서 「small risk … if the process crashes」와 맞는 관찰이라 입력을 고치지 않음(규격 §2-7 10번).
- **결정적 값**: §3 표 전부 + 05 두 노드가 끝나는 차례(출력하지 않고 횟수만) · 체크포인트 ID·작업 id·시각·프로세스 번호·임시 폴더 위치(출력하지 않음). 04·06은 **신호가 온 그 셀에서 바로 끊으므로**(마감 B-1) 끊는 자리가 늘 둘째 노드가 쉬는 동안.
- 새 커널 셀별 같음(마감): 04 **26/27**(다른 셀은 `async` 줄뿐) · 06 **23/23** · 07 **22/22**. 01·02·03·05는 개선 때 두 번(28/28·28/28·29/29·21/21)이고 마감에서 다시 실행하지 않음.
- **셀을 다시 실행해도 같은지(마감, 노트북 밖 확인 `/tmp/ch23-close/rerun_probe.py` — 새 커널로 끝까지 실행한 뒤 장면 셀을 한 번 더)**: 04 4절 네 셀 4/4 · 5절 4/4 · 6절 1/1 · 06 4절 4/4 · 5절 4/4 · 6절 1/1 · 07 설정 셀부터 실행 1·2 — 앞머리 번호 줄(`idempotent-2`·`naive-2`) 말고 모두 같음. 2절 셀(04 `steps.sqlite` 세 스레드·06 `twice.record`)은 다시 실행하면 같은 스레드·파일에 이어 붙어 값이 달라짐 → 노트북 준비물·b7에 「노트북 전체를 처음 값으로 보려면 1절 임시 폴더 셀부터」.
- **재지 않은 것**: 걸린 시간(준비물의 「N초 안에」는 셀 실행 기록 — 04 약 11.1초 · 06 약 14.1초 · 07 약 1.0초) · Windows·macOS 실행(종료 코드 Windows `1`은 설치판 Python 소스로만) · 여러 프로그램이 한 파일·한 표를 함께 쓰기 · 실제 결제·메일 서비스 · 에이전트 그래프·모델 답·도구 메시지 저장 · 커널 다시 시작.

## 7. 07절 실습 절 주제와 결과

- 제목 「**Persistence 실습: 멈춘 대출 처리를 이어 가고 기록은 한 번만 남기기**」, 슬러그 `07-Persistence-실습`, `format: experiment`, meta 「실습 30분 · 새 용어 0」. **챕터 시수에 더하지 않습니다**(규격 §7-2). 01~06 meta 합 강의 1×6 = **6h** · 실습 1.5+1.5+1.5+2+1.5+2 = **10h** = `chapter.json` 「총 16h · 강의 6h · 실습 10h」(`_build_index.py`도 6·10).
- 대출 신청 한 건 — 스레드 = 이용자 번호 `M-0317`(Ch 21 03 값), 멱등 키 = 대출 키 `loan-2307`(실행 전에 정함). 노드 `receive_request` → `record_loan`(쓰기 방식대로 대출 기록 파일에 키 한 줄 → **그 뒤에** 실패 흉내 `TimeoutError`). 실행 1 쓰기 방식 `idempotent`, **실행 2는 쓰기 방식 하나만 `naive`**(06 Before/After와 같은 값 — 「새로 볼 것」 = 강제 종료가 아니라 같은 커널 안의 실패 흉내로 멈추고 새 연결에서 이어 갈 때도 같은 차이인지). 파일 앞머리는 `write_plan["prefix"] = new_prefix(write_plan["mode"])`(마감 — 설정 셀을 다시 실행하면 번호가 올라 새 파일).
- 붙인 앞 절 기능 셋(두 실행 모두 흐름 안에서 쓰임): **03** SQLite 체크포인터 + 멈춘 뒤 `close()` → 새 연결·새 `SqliteSaver`·새 그래프가 같은 자리를 읽고 그 그래프로 이어 감 · **05** 실패 흉내와 원인을 없앤 뒤 `invoke(None, config)`(부른 횟수 1·1 → 1·2) · **06** `append_key_once`(도구 파일) → 다시 실행된 `record_loan`이 `건너뜀`. 04 `read_saved`·`read_record`·`new_prefix`는 결과 읽기·파일 이름에만. 뺀 것: 02(서버)·04 저장 시점 비교·강제 종료·05 같은 단계 두 노드·03 메시지 칸·01 `InMemorySaver`.
- 결과(마감 새 커널 두 번 22/22 같음): `쓰기 방식: {'mode': 'idempotent', 'prefix': 'idempotent-1'}` · `SQLite 파일 이름: idempotent-1.sqlite` · 실행 1 `오류 종류: TimeoutError`·`부른 횟수: {'receive_request': 1, 'record_loan': 1}` → `다음 노드: ('record_loan',)`·`체크포인트 수: 3`·`멈추기 전에 적힌 키: ['loan-2307']` → `새 그래프가 읽은 다음 노드: ('record_loan',)` → `칸 notes: ['신청 받음', '건너뜀']`·`부른 횟수: {'receive_request': 1, 'record_loan': 2}` → `다음 노드: ()`·`체크포인트 수: 4`·`같은 키가 적힌 줄 수: 1` · 실행 2 같은 차례 → `['신청 받음', '적음']`·`같은 키가 적힌 줄 수: 2` · 견주기 `idempotent-1 | ['신청 받음', '건너뜀'] | 4 | 1`·`naive-1 | ['신청 받음', '적음'] | 4 | 2` · 파일 `['idempotent-1.record', 'idempotent-1.sqlite', 'naive-1.record', 'naive-1.sqlite']`. 모델 요청 0 · 자식 프로세스 0 · `assert`는 같은 키 줄 수(1·2)에만.

## 8. 도구 파일 `notebooks/checkpoint_tools.py` — 함수 표와 해시 변천

| 함수(인자) | 배운 곳 | 가져오는 절 | 하는 일 |
|---|---|---|---|
| `start_worker(worker_path, files, mode, phase)` | 04 노트북 3절 | 06 | `subprocess.Popen([sys.executable, worker_path, 파일 이름 셋, mode, phase])` → 프로세스 객체 |
| `wait_for_signal(signal_name, limit_seconds)` | 04 노트북 3절 | (`kill_at_second` 안) | 신호 파일을 0.05초 간격으로 기다려 `True`/`False` |
| `stop_worker(process)` | 04 노트북 3절 | (`kill_at_second` 안) | `kill()` → `wait(timeout=5)` → 종료 코드 |
| `read_saved(graph_builder, sqlite_name, thread_name)` | 04 노트북 3절 | 06·07 | 새 연결·새 `SqliteSaver`로 `{"칸 값", "다음 노드", "체크포인트 수"}`, 연결 닫음 |
| `read_record(record_name)` | 04 노트북 3절 | 06·07 | 기록 파일의 줄 → 목록 |
| **`new_prefix(name)`(마감)** | 04 노트북 3절 | 06·07 | 작업 폴더에 `이름-번호.sqlite`가 있으면 번호를 올려, 아직 쓰지 않은 앞머리 `이름-번호`를 내놓음(`while`·`os.path.exists`·`str`·`+`, 본문 4줄) |
| `kill_at_second(worker_path, graph_builder, name_prefix, mode)` | 04 노트북 6절 | 06 | 띄우기 → 신호(20초) → 끊기 → `assert` → `read_saved` |
| `append_key(record_name, order_key)` | 06 노트북 2절 | 07 | 기록 파일 끝에 키 한 줄, `"적음"` |
| `append_key_once(record_name, order_key)` | 06 노트북 2절 | 07 | 키가 이미 있으면 `"건너뜀"`, 없으면 `append_key` |
| `kill_then_resume(worker_path, graph_builder, name_prefix, strategy)` | 06 노트북 6절 | **없음**(강사 확인 — B-11) | `kill_at_second` → `start_worker(…, "resume")`·`wait(timeout=30)` → `read_record` |

- 함수 **열**, 함수마다 `# Ch 23 NN절에서 배웠습니다 — NN절 노트북 N절의 같은 이름 함수를 옮겼습니다`, import `os`·`sqlite3`·`subprocess`·`sys`·`time` + `from langgraph.checkpoint.sqlite import SqliteSaver`, 전역 이름 기대기 0, 금지 문법 0. **파일을 쓰는 생성기는 `author_06.py`**(`TOOL_PARTS` — 04 생성기 `DEF_*`와 06 `DEF_*`를 글자 그대로, `check_same_as_before()`가 문자열·AST 대조). 07 생성기는 해시와 `author_06.TOOLS`를 대조.
- 머리 독스트링(마감 B-11): 「04절 노트북 3절과 6절에서 처음 적은 함수 일곱(강제 종료 함수와 앞머리 글 함수)」 · 「06절 노트북에서 처음 적은 함수 셋도 … (07절은 그 가운데 append_key와 append_key_once를 가져옵니다)」.
- **해시 변천**: 없음(01~05) → 06 `71280dd9fdd748bb9ae98388990a7ed0d33d07e3fb1246abfba95c64c4437c29`(04 함수 여섯 + 06 함수 셋) → 07 그대로 → **마감 `a850b2cdccbd8ff6f3dd8364e5ab58a8f2845eb6c8607ef7250315c5eee26b37`**(+ `new_prefix`, 독스트링 두 줄).
- 가져오는 절(06·07) 준비 셀 결과 읽기에 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 …」, 가져오기는 임시 폴더로 옮기기 전, 이름은 알파벳 순. 01~05는 가져오지 않음(01·03·05가 처음 적은 `print_history`·`thread_row`·`print_conversation`·`sqlite_tables`·`saved_channels`는 뒤 절이 되풀이하지 않아 옮기지 않음). 묶음 목록 두 곳에 있고 마감 zip에 든 판이 디스크와 같음. Part 6 선행 목록에는 없음(뒤 챕터가 쓰지 않음).

## 9. worker 스크립트 둘과 02 PostgreSQL 실행 방식

- **`durability_worker.py`**(04, `c60467bdd82d40792148b2afad0471a98a8219ac6de48f10b104578be14491de`, 생성기 `author_04.py` `WORKER`) — 인자 다섯(SQLite·신호·기록 파일 이름 — 모두 노트북 임시 폴더 안 이름, 저장 시점, 단계 `first-run`/`resume`), 상태 형식 `StepState`(칸 `completed`), 노드 `first`·`second`가 기록 파일에 이름 한 줄(`"a"`), 둘째 노드는 신호 파일을 만들고 `first-run`에서만 30초 쉼, 다시 실행 단계는 저장된 다음 노드가 있으면 `invoke(None, config, durability=mode)`·없으면 처음 입력, 연결은 `sqlite3.connect(…, check_same_thread=False)` + `close()`.
- **`idempotency_worker.py`**(06, `b0201de72d4534a7238d0bd5b2ad8b4d85e2ca0eeb6f307ac7d6897207430b72`, 생성기 `author_06.py` `WORKER`) — 04와 같은 인자 모양(넷째 글 = 쓰기 방식 `naive`/`idempotent`), 노드 `receive_order` → `charge`(결제 기록에 `order-2306` → 신호 → 쉼), 저장 시점 `sync`, 함수 `append_key`·`append_key_once`는 노트북 셀과 글자까지 같음.
- 두 worker는 마감에서 바뀌지 않음(생성기를 다시 돌려도 바이트 같음). 자식 프로세스가 남지 않게 `kill_at_second`는 신호 결과와 상관없이 먼저 끊음. 확인은 `ps -eo pid,args | awk '$2 ~ /python/ && /_worker/'`(`pgrep -f`는 거짓 양성).
- **02 PostgreSQL**: 학생은 Ch 12 02 컨테이너 `hankyung-part3-pgvector`를 같은 접속 글로(꺼져 있으면 `docker start`, 없으면 Ch 12와 같은 `docker run` — 노트북 첫 셀·실습 폴더 README), 이름 공간 `ch23_lab`만 지우고 만듦. **작업 기기(교재 출력)**: Docker가 없어 `qa/upgrade/pre_exec.sh`(`8f078591…`)가 `N=02`일 때만 Ch 12의 conda-forge PostgreSQL 17.11(`.cache/vm/pgenv/bin`)로 새 클러스터 `/tmp/ch23-02/pgdata`를 만들고(없을 때만 `initdb`) 같은 접속 글로 켠 뒤 `trap EXIT`로 끔 · 55432에서 이미 받는 서버가 있으면 켜지 않고 멈춤(`return 1`) · Ch 12 데이터 폴더(`.cache/vm/pgdata`)는 건드리지 않음. `run_section.sh`가 절 실행 전에 source 하므로 **02를 다시 실행하려면 같은 호출 안에서**. **`run_section.sh … 02 --no-exec`도 서버를 켬** — 마감은 `pre_exec.sh` 없이 같은 단계를 부르는 `.cache/ch23-close/tools/nx.sh`를 썼음.

## 10. 챕터 밖 수정 (전부 목록)

| 파일 | 언제 | 무엇을 |
|---|---|---|
| `labs/part6/ch23-persistence/notebooks/01~07-*.ipynb` · `notebooks/checkpoint_tools.py` · `durability_worker.py`·`idempotency_worker.py` | 01~07절 · **마감** | 실습 폴더(챕터 몫) — §1·§8·§9·§16. 마감: 04·06·07 다시 실행, 01·02·03·05 마크다운만(파일 `7189b35f`→`72e3e7ee` · `c3b15aef`→`8722ced2` · `ab7333da`→`bc54df7e` · `be38374b`→`b81d248b` · `d544089a`→`feca7289` · `869b6ae4`→`589badab` · `0fe06118`→`44613fb4`). 도구 파일 `71280dd9`→`a850b2cd`. worker 둘 그대로 |
| `labs/part6/ch23-persistence/README.md` | 07절(07 단락) · **마감(전체)** | `a876fed0…` → **`7eae43a5f6e63dc87413c9838e67a2fcac9e5077454ab650bea9a4395fa63426`**: 노트북 일곱(모두 모델 요청 0·API 키 불필요), `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 절별 패키지 판, 파일은 임시 폴더에만, **02 PostgreSQL은 Ch 12 02 컨테이너를 같은 접속 글로 다시 씀(옛 `kdt-ch23-postgres`·`postgres:17` 명령 뺌) + Ch 12와 같은 `docker run`**, 이름 공간 `ch23_lab`, 도구 파일 단락(고정 문장 뜻·함수 열·배운 절·가져오는 절), worker 둘의 자리와 역할·인자, 다시 실행 단계, **Windows 강제 종료·종료 코드 주의**, 절마다 하는 일, 07 단락(함수 다섯). 묶음에 없는 파일(Ch 12 README 등)을 가리키지 않음. 금지어 0 |
| `textbook/part6/ch23-persistence/chapter.json` | 07절 · **마감** | 07 절(07절) · `objectives` 셋 → **일곱**(절마다 한 줄 + 07 실습 줄, 「재개」·「내구 실행 모드」·「pending writes」·「멱등 키 … 재실행의 중복 부작용」 옛 말 뺌), `hours` 그대로(`36267fb5` → `e766b0ca`, 보호 파일) |
| `textbook/part6/ch23-persistence/qa/public-files.json` | 07절 · **마감** | 07 두 줄(07절) · **옛 SVG 여섯 줄(`figures/0N-흐름.svg`) 뺌**(본문 참조 0, 파일은 지우지 않음 — `d16b71f3` → `e34255f9`, 보호 파일). `collect_public_files.py`로 다시 모은 Part 목록 `textbook/part6/public-files.json`·`prerequisite-files.json`은 **바이트까지 같음**(`8ed6852b…`·`4c7f5a4b…` — 교재 쪽 줄은 Part 목록에 들어가지 않음) |
| `textbook/part6/_build_index.py` | **마감** | ch23 설명 「실행 상태를 저장하고 프로세스 중단 뒤 복구되는 범위를 확인합니다.」 → 「체크포인터로 실행 상태를 스레드마다 메모리·PostgreSQL·SQLite에 저장하고, 저장 시점에 따라 강제 종료 뒤 파일에 남는 것을 견주고, 멈춘 실행을 이어 갈 때의 남은 쓰기와 멱등 키를 확인한 뒤, 멈춘 대출 처리를 이어 가고 기록은 한 번만 남기는 실습을 합니다.」(시수 6·10 그대로, `9e130bd4` → `036fbdd2`, 보호 파일) |
| `textbook/part6/index.html` · `textbook/downloads/part6-practice.zip` · `textbook/part6/qa/integration-results.json` | 07절 + **마감** | `python3 textbook/part6/_build_index.py`(README·노트북·목록·`chapter.json`을 모두 고친 뒤 마지막 한 번) → **`Part 6: 50 verified sections; 96 bundled files`**, zip `43b1923f…` → **`aa82b386b154e5c634f7bf416e48b50525b1b2067deda65ddcfe6a7b1e381f04`**(99항목, **Ch 23 13파일이 모두 디스크와 같음**, `__pycache__` 0), `index.html` `ec2588c0` → `cfd0cd81`, `integration-results.json` `2ff2be9f` → `624a596e` |
| `textbook/part6/qa/bundle-execution.json` | **마감** | Part 6 `check_bundle_execution.py`가 다시 씀(`2a3bed10` → `f53987e8` — 새 zip, **Ch 24 01 4셀·Ch 28 01 4셀 PASS**, Ch 23은 실행 대상 아님). 환경 변수 `UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache`·`UV_LINK_MODE=symlink`만(스크립트 수정 0) |
| `textbook/part6/qa/visual-results.json` · `textbook/_notebook/checks/ch23-persistence/visual-results.json`(+ 스크린숏) | **마감** | `visual.cjs` 16행 PASS. 공용 파일은 **Ch 23 줄만** 14 → 16(07 두 줄, 새 HTML 해시), `screens` 118 → 120, 다른 챕터 줄 그대로(→ `367e23e3`, 보호 파일). 다른 챕터 줄 76개는 원래부터 옛 HTML 해시(Ch 22 등 — 기록만) |
| `textbook/part6/qa/notebook-readiness.json` | **마감(되돌림)** | 옛 `check_notebook_readiness.py`가 멈추기 전에 다시 써서 실행 전 사본으로 되돌림(내용 변경 0, `b3d69e9c…`) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json` | 절마다·마감 | `verify.py --chapter`가 다시 씀(마감 뒤 `1458e094…`) |
| `textbook/qa/upgrade-progress.md` · `textbook/qa/upgrade-final-checklist.md` | **마감** | Ch 23 행 한 줄 · §2-11 Ch 23 항목과 §3·§4 Ch 23 줄 |

- **고치지 않은 것**: `textbook/QUALITY-UPGRADE.md`·`PLAYBOOK.md`·과정 요약·`upgrade-contracts.md` · 공용 도구 코드(`nbkit.py`·`mdpatch.py`·`run_section.sh`·게이트·`verify.py`·`visual.cjs`·`execute.py`·`build_bundle.py`·`render_mermaid.py`·`attach_figures.py`·`builder.py`) · Part 6 옛 검사 스크립트와 `check_*`·`collect_public_files.py` · **`textbook/_notebook/build_index.py`**(Ch 23 절 수 6 — 선례대로) · **공용 옛 생성기 `qa/author_ch23_ch24.py`**(`44c9d593…`, Ch 24가 아직 씀 — 01절이 넣은 Ch 23 건너뛰기 그대로, 옮기지 않음, Ch 24 쪽 동작 그대로) · `textbook/part6/qa/final-artifact-hashes.json`(옛 판 기록 — `figures/_gen_figures.py` 옛 자리 줄 포함) · `textbook/part6/qa/ch23-technical-review.md`(Part 6 쪽 옛 검토 기록, 보호 파일) · 실습 폴더 `pyproject.toml`·`uv.lock` · `labs/part6/continuity-guide.md`(Ch 23 두 줄 「체크포인터와 프로세스 중단 후 복구」·「스레드와 저장 상태」는 참 — 확인만) · **Ch 24 이후 파일 전부**(Part 6 목차·묶음·공개 목록·기록 말고) · `pre_exec.sh`(지우지 않음).
- **파일을 지운 것은 없습니다.** 옛 생성기 `figures/_gen_figures.py` 하나만 `mv -n`으로 `qa/upgrade/before/generators/blocked/`에 옮겼습니다(해시 `6d95031c…` 같음, 부르는 빌드·검사 스크립트 없음 — `grep`으로 `before-manifest.json`·공용 옛 생성기의 Ch 23 건너뛰기 주석·`final-artifact-hashes.json` 기록뿐, 옮긴 뒤 `_build.py`·`verify.py` 통과). 마감이 새로 만든 파일: `chapter-summary.md`(이 파일) · `gates-after.json` · `before/generators/blocked/_gen_figures.py`(옮긴 것) · 기기 `/tmp/ch23-close/`(A·B 사본·`rerun_probe.py`) · `.cache/ch23-close/`(마감 전 사본 `pre/`·확인 스크립트 `tools/`(`cpatch.py`·`genmatch.py`·`nx.sh`·`patch04*.py`·`patch06.py`·`patch07*.py`·`cmpout.py`·`extra_check.py`·`ban_check.py`·`names_check.py`·`nbhash.py` 등)·치환 목록 `reps/`·그림 확인 사본 `view/`·옛 검사 결과 `oldcheck/`·`dx/`(`llm-practice.zip`을 뺀 전달 검사 사본과 결과)·로그 `log/`).
- **보호 파일 123개(`before-manifest.json`)**: **99개 같음 · 23개 바뀜 · 1개 옮김(없어짐)** — 모두 의도한 것: 01~07절이 바꾼 열아홉 가운데 18(README·worker 둘 — 개선 판·노트북 01~06·공용 옛 생성기 Ch 23 건너뛰기·zip·Part/챕터 공개 목록·`verification.md`·통합 기록·notebook-contracts·Part 6 목차·`chapter.json`) + 마감이 새로 바꾼 다섯(`_build_index.py`·`bundle-execution.json`·Part 6 `visual-results.json`·챕터 `visual-results.json`·`qa/research.md` 「개선 전 판」 표시) · **옮김 1 = `figures/_gen_figures.py`**(§4-5 결정). 정확한 목록은 §16 끝.

## 11. 기준 버전·확인 날짜

- 실습 폴더 잠금(`pyproject.toml` 직접 의존 `langgraph==1.2.11`·`langgraph-checkpoint-sqlite==3.0.3`·`langgraph-checkpoint-postgres==3.0.5`·`psycopg[binary,pool]==3.3.3`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`): `langgraph-checkpoint 4.2.0`·`psycopg-pool 3.3.1`·`langchain-core 1.6.2`·`typing-extensions 4.16.0`. 노트북 `%pip`은 모두 잠금 판(01 둘 · 02 셋 · 03 셋(+ `langchain-core`) · 04~07 둘).
- 교재 출력: Linux aarch64 · Python **3.12.13** · SQLite **3.53.1** · 02는 PostgreSQL **17.11**(같은 접속 글로 켠 서버 — Docker 이미지로는 실행하지 않음) · 환경 `.cache/vm/venv-ch23-persistence`(잠금 판). 실행일 모두 2026-09-25(01 08:04 · 02 08:37 · 03 09:08 · 05 10:21 UTC · **04 12:36 · 06 12:36 · 07 12:36 — 마감 새 실행**).
- 설치판 소스 행(검토 A·B가 다시 확인): `pregel/main.py` 2589~2593·2602~2603·2967~2968·2987~2988 · `pregel/_loop.py` 466·856·861~865·1132~1135·1199~1202·1324~1333·1651~1654 · `pregel/_executor.py` 105~107 · `pregel/_runner.py` 574~613 · `types.py` 89~95·637~646 · `checkpoint/memory/__init__.py` 36~42·334~354 · `graph/message.py` 202~208 · `checkpoint/postgres/__init__.py` 37~51·56~75·68~69·77~102·84~85·301~308·336~351 · `checkpoint/sqlite/__init__.py` 41~44·62~66·113~120·122~159·161~176 · CPython 3.12 `subprocess.py` 1667~1682(Windows `terminate()` = 종료 코드 1).
- 참고 자료(2026-09-25 확인): LangGraph Persistence · Checkpointers(Durability modes) · Python 3.12 `subprocess`·`sqlite3` · SQLite WAL · Stripe Idempotent requests.

## 12. 강사 확인 대상

1. **제목 말**: 챕터 「Persistence와 Durable Execution」 · 02 「PostgresSaver」·「스키마」(SQL `SCHEMA`는 「이름 공간」, 이음 문장 — 마감 A-10) · 04 「내구 실행 모드」(본문 「저장 시점」) · 05 「pending writes」(본문 「남은 쓰기」) · 06 「노드 재시작」·「멱등성」 · 07 「Persistence 실습」. 슬러그 01·04·05·06은 Ch 20 02·03 b7 링크 때문에 고정.
2. **모델 없는 챕터**(일곱 절 모델 요청 0, 키 셀 없음) — **07 실습 절도 0번**(규격 §7-2 「3~5번」과 다름, Part 1 실습 절 선례).
3. **07 실행 2가 06과 같은 값(쓰기 방식)** · **06 b7이 노트북 밖에서만 본 장면(실패 흉내로 멈춘 뒤 이어 가기)을 07이 노트북에서 실행** · 07 대출 키를 새로 정함·이용자 번호는 Ch 21 03 값.
4. **흔들린 값을 b7에 둔 과정 선례**(04 `async` — 규격 §2-7 9번 목록은 둘째 단락·본문 표·확인할 점만) — 과정 선례(Ch 20)와 인계 결정대로 둠.
5. **02 PostgreSQL 선택 A**(교재 출력은 작업 기기의 PostgreSQL 17.11 — 학생 안내는 Ch 12 Docker 컨테이너) · 02가 01 노드 함수 `add_amount`를 노트북에 다시 적음(마감 A-11 — 챕터 리드 결정대로 그대로: 노드는 노트북에 남김, 규격 §2-7 3·5번과 다른 예외).
6. **마감 코드 고침(B-1 [상])**: 04 4·5절 띄우기·끊기를 한 셀로 · **새 함수 `new_prefix`**(04가 가르침, 도구 파일 함수 열) · 04·06·07 파일 이름이 `이름-번호` 앞머리로(교재 출력 `exit-1`·`naive-1`·`idempotent-1` 등) · 04 끊는 셀 `assert` 둘(`!=` — Ch 2 문법) · 04 코드 셀 28 → 27.
7. **도구 파일 `kill_then_resume`을 가져오는 노트북이 없음**(B-11) — 남김(가르친 함수를 모은다는 규칙). 뺄지.
8. **05 0.1초 쉼과 전역 딕셔너리** — 마감에서 노트북에 실제 까닭(`good`이 먼저 끝나게)과 조건을 밝힘(B-8) · 05 b7 공식 문서 문장은 관찰의 근거가 아님을 밝히고 소스 자리를 근거로(B-7).
9. **worker 스크립트 둘을 다시 씀**(04·06 개선 때) · 06 읽기용 `charge` 셀 · 결제는 파일 한 줄 흉내.
10. **코드 줄 증가**(주석·빈 줄 뺌, `count_code.py`: 01 32→113 · 02 41→123 · 03 36→127 · 04 48→147→**161**(마감 +14 — `new_prefix` 셀·끊는 셀의 앞머리·`assert` 둘·마지막 셀 라벨, 셀은 28 → 27) · 05 53→113 · 06 38→123→**128**(마감 +5) · 07 새 절 135→**141**(마감 +6) · 도구 파일 69줄 — 챕터 합 881 → 906) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘.
11. **meta 구분자 `|` 통일**(04~06, B-5) · 시수 합 6h·10h 그대로.
12. **삽화(다시 만들지 않음, Higgsfield 0)**: 02-5 사진 배열이 「두 장씩 세 줄」(프롬프트는 세 장씩 두 줄) · 07-4 리본 모양(글만 고침 — B-13) · 07-4 판 위 흰 나이트 셋(「짝짓지 않습니다」로 막음).
13. **`chapter.json` 학습 목표 셋 → 일곱**(절마다 한 줄 + 07 실습 줄) · 실습 폴더 README 다시 쓴 범위.
14. 한국어 감사 3단·그림 판독 2차(별도 세션 — 두 검토의 「확인하지 못한 것」: Windows·macOS 실제 실행, 특히 Windows venv `python.exe` 실행기 아래 프로세스까지 `kill()`이 끝내는지 · 학생 `uv sync --locked` `.venv`에서 첫 셀).

## 13. Ch 24가 이어받을 것과 전제하면 안 되는 것

### 이어받을 것

- 말: 체크포인터·체크포인트·스레드(01) · 이름 공간·표 만들기·표 만들기 기록(02) · SQLite 체크포인터·객체의 수명·스레드 재개(03) · 저장 시점·자식 프로세스·강제 종료·신호 파일(04) · 남은 쓰기·작업·장애 복구(05) · 노드 재시작·멱등성·멱등 키(06). **「이어 실행」 = Durable Execution 풀이 한 뜻**(멈춘 실행을 저장된 자리부터 이어 가는 일), 끝까지 간 뒤의 다음 실행은 「같은 스레드로 다시 실행」.
- 사실(참, 출력 근거): Ch 24 01 b3 「Ch23에서 노드는 장애 뒤 처음부터 재시작될 수 있고 외부 쓰기에는 멱등성이 필요하다는 점을 확인했습니다」 — **06·07로 참**(끊긴·멈춘 노드가 처음부터 다시 실행, `append_key_once`로 한 줄). Ch 24 01 「체크포인터는 InMemorySaver」 — 01로 이어짐(Ch 23 03~07은 SQLite). 설정 딕셔너리의 `thread_id`, `get_state`의 `next`·`tasks`(05), `invoke(None, config)`(05·07).

### 전제하면 안 되는 것 (Ch 24 파일은 고치지 않았습니다)

1. **Ch 23은 모델을 부르지 않았습니다(01~07).** 모델 답·도구 메시지를 저장한 적이 없고, 에이전트 그래프(`create_agent(…, checkpointer=…)`)에 체크포인터를 붙인 적도 없습니다. 「대화」는 03의 코드가 만든 `HumanMessage`·`AIMessage`뿐입니다.
2. **`interrupt`·`Command(resume=)`·`update_state`·시간 여행(`checkpoint_id`로 되돌려 다시 실행)·`stream`은 0건**입니다. 07의 「이어 가기」는 실패 흉내로 멈춘 뒤 원인을 없애고 `invoke(None, config)` — 사람의 승인 값을 넣어 이어 가는 장면은 없습니다. 06·07 함수 이름에도 `interrupt`를 쓰지 않았습니다(`kill_then_resume`).
3. **`resume` 말 겹침**: 03 「스레드 재개」(객체를 새로 만든 뒤 같은 스레드로 이어 가기 — 마감에서 영어 괄호를 빼고 「Ch 24에서 사람의 확인을 받아 멈춘 실행을 다시 움직이는 일과는 다른 장면」 한 문장) · 04·06 worker의 단계 이름 `resume`(강제 종료 뒤 새 프로세스로 다시 실행) · Ch 24 `Command(resume=…)`(멈춰 기다리던 실행에 값을 넘겨 다시 움직이기)는 **셋 다 다른 장면**입니다. Ch 24는 첫 자리에서 03과 다르다는 문장을 두는 쪽을 권합니다.
4. **멱등 키 확인은 기록 파일을 읽은 뒤 적는 방식**이고, 한 프로그램·한 커널 안에서만 보았습니다. 여러 프로그램이 한 파일을 함께 쓰는 틈·「보상 작업」·실제 결제·메일 서비스는 실행하지 않았습니다(06·07 b7).
5. **체크포인트 수는 우리 그래프의 값**(노드 하나 01: 실행 한 번에 셋 · 노드 둘 04·06·07: 끝까지 넷, 둘째 노드에서 멈추면 셋 · 05 같은 단계 두 노드: 실패 뒤 둘(기본값)/하나(`exit`)). 노드 수가 다른 그래프에 그대로 쓰면 안 됩니다.
6. **공용 옛 생성기 `qa/author_ch23_ch24.py`**(`44c9d593…`)는 Ch 23 쪽만 막혀 있고(`write_all()`이 `ch23-persistence`를 건너뜀) **옮기지 않았습니다** — Ch 24 개선 때 이 파일을 어떻게 할지 정하고, Ch 24 작업 뒤 `qa/upgrade/before/generators/blocked/`로 `mv -n`(Ch 23 몫 인계).
7. **말**: 「재시작」은 06 제목 말(다른 절 본문은 「다시 실행」), 「pending writes」는 05 제목에만. Ch 24 01에 있는 「경로」(`unsafe 경로`)·「런타임」·「반환값」은 Ch 23 금지어 표의 말 — Ch 24 몫.
8. **파일 앞머리 `new_prefix`는 Ch 23 실습 폴더 도구 파일 함수**입니다(Ch 24 실습 폴더에는 없음).

## 14. 챕터 끝 인계 요약 (Ch 24 작업자용 한 줄)

Ch 24 01 b3(06·07로 참)·「InMemorySaver」(01)는 그대로 참입니다. Ch 24는 `interrupt`·`Command(resume=)`를 처음 가르치는 챕터이고, Ch 23 03 「스레드 재개」·04·06 worker `resume` 단계와 다른 장면임을 첫 자리에서 밝혀 주세요. 공용 옛 생성기의 이동도 Ch 24 몫입니다.

## 15. 뒤 챕터(Ch 24·25·26·27·30·31) 인계 (그 챕터 파일은 고치지 않음)

| 챕터 | 자리 | 지금 글 | Ch 23 쪽 사실 | 할 일 |
|---|---|---|---|---|
| Ch 24(대기) | 01 `_src` b3 | 「Ch23에서 노드는 장애 뒤 처음부터 재시작될 수 있고 외부 쓰기에는 멱등성이 필요하다는 점을 확인했습니다」 | 06·07로 참 | 없음 — 「재시작」은 Ch 23 06 제목 말(본문 「다시 실행」)임을 참고 |
| Ch 24(대기) | 01·02 `resume`·「재개」 | `Command(resume=value)`·「재개할 때 노드는 처음부터 실행」 | Ch 23 03 「스레드 재개」·04·06 worker `resume`과 다른 장면 | Ch 24 첫 자리에서 03과 다른 장면이라는 한 문장(§13-3) |
| Ch 24(대기) | 공용 옛 생성기 `textbook/part6/ch23-persistence/qa/author_ch23_ch24.py` | Ch 23 쪽 건너뜀 | Ch 23은 옮기지 않음 | Ch 24 작업 뒤 `mv -n`(체크리스트 §2-11) |
| Ch 25(대기) | 01~03 `_src` b3 | 「Ch23에서 체크포인터와 thread_id가 상태를 저장하는 방법을 배웠고」 | 01로 참 | 없음 |
| Ch 26(대기) | 01~04 `_src` b3 | 「Ch23에서 thread_id와 체크포인터를 배웠습니다」 | 01로 참 | 없음 |
| Ch 27(대기) | 01 `_src` | 「Ch 23의 체크포인터는 실행 상태를 이어 주었고」 | 01·03·05·07로 참 | 없음 |
| Ch 27(대기) | 04 `_src` b3 | 「Ch 23에서 상태 저장 범위를 구분했습니다」 · 「체크포인터 메시지와 다른 저장 표면」 | 01 b7(Store는 실행 안 함)·03(메시지 칸을 SQLite에)로 참 — 다만 Store는 한 줄뿐 | 없음(느슨함 — Ch 27 작업 때 확인) |
| Ch 30(대기) | 02 `_src` b3 | 「Ch21의 Agent와 **Ch23의 체크포인터처럼 생성 비용과 수명주기가 다른 객체**」 | **수명만 참**(03 「객체의 수명」) — 생성 비용은 Ch 23 어느 절도 재지 않음 | Ch 30 작업 때 「수명」만 남기거나 생성 비용 근거를 Ch 30이 보임 |
| Ch 30(대기) | 06 `_src` b3 | 「Ch23의 thread 분리」 | 01로 참 | 없음 |
| Ch 31(대기) | 02 `_src` b3 | 「Ch23에서는 중단 뒤 재개와 멱등성을 배웠습니다」 | 04·05·06·07로 참 | 없음 |
| Ch 31(대기) | 02 `_src` b7 | 「멱등성 키와 **보상 작업**」 | 보상 작업은 Ch 23이 다루지 않음(Ch 23을 가리키지 않는 문장 — 문제 아님) | Ch 31 몫 |
| Ch 31(대기) | 05 `_src` b3·새 용어 | 「Ch23에서는 PostgresSaver의 `setup()`이 체크포인터 표를 만든다는 점을 확인」 · 새 용어에 「체크포인터」 | `setup()`은 02로 참 · **「체크포인터」는 Ch 23 01이 이미 정의한 말** | Ch 31 작업 때 새 용어에서 빼고 「Ch 23 01에서 정의한」으로 이을지(Ch 31의 「스키마」·「마이그레이션」도 Ch 23 금지어 — Ch 31 몫) |
| Ch 20(완료) | 02·03 b7 링크 | 04·05·06 슬러그 | 슬러그 그대로 · 04 「강제 종료 뒤」·05 「실패한 단계」·06 「한 번만 반영」 참 | 없음 |
| Ch 21(완료) | 03 b4·b7·07 b7 | 「결과 상태를 저장해 다음 실행에 이어 쓰는 방법은 Ch 23에서」 | 01로 참 | 없음 |
| Ch 22(완료) | 09 b8 | 「이번 실습에서 종류별로 출력한 대화 기록이 그 대상입니다」 | 03(메시지 칸 저장)으로 메시지 기록 수준에서 참 — 도구 메시지는 저장해 보지 않음(03 b7 공개), 03 [14]에 「Ch 22 09는 `message.type`, 이 절은 클래스 이름」(마감 A-18) | 없음(완료 챕터 — 고치지 않음) |

## 16. 남은 것 (전체 마감 몫 — `textbook/qa/upgrade-final-checklist.md` §2-11)

1. **공용 옛 생성기 `qa/author_ch23_ch24.py`**(`44c9d593…`) — Ch 24가 쓰므로 옮기지 않음. **Ch 24 작업 뒤 `mv -n` → `qa/upgrade/before/generators/blocked/`.** Ch 23 `figures/_gen_figures.py`는 마감에서 옮김(완료). **→ Ch 24 마감(2026-09-25)에서 옮김(완료)**: 01절이 막은 판(`3fc72ded…`)을 `mv -n` → `qa/upgrade/before/generators/blocked/author_ch23_ch24.py`(해시 같음, 부르는 스크립트 0 — Ch 24 요약 §10).
2. **옛 그림 열여덟 삭제 승인**: `figures/0N-흐름.{svg,excalidraw,caption.md}`(N=1~6, 본문 참조 0, 챕터 공개 목록 줄은 마감에서 뺌, 사본 `qa/upgrade/before/figures/`, `final-artifact-hashes.json`이 해시를 적은 기록 파일) — Part 6 옛 검사 `check_figures.py`가 `.excalidraw` 짝을 요구하는 것과 함께 정할 것.
3. **02 PostgreSQL**: `qa/upgrade/pre_exec.sh`(`8f078591…`)는 지우지 말 것(02를 다시 실행할 때 씀) · 기기 `/tmp/ch23-02/pgdata`(PostgreSQL 클러스터, 서버는 꺼져 있음)·`/tmp/ch23-prep`(임시 클러스터 포함) 삭제 승인.
4. **`gates-wip-*.json` 열여섯 삭제 승인**(`gates-wip-01~07.json`·`gates-wip-0N-0N.json` 일곱·`gates-wip-ch23-after07.json`·`gates-wip.json` — `gates-after.json` 7/7로 갈음) · **`qa/upgrade/__pycache__/`**(생성기 대조 때 생김, 마감에서 새로 만들지 않음). 실습 폴더 `notebooks/__pycache__`는 없음.
5. **캐시·임시**: 실습 폴더 `labs/part6/ch23-persistence/.venv`(macOS 판 142MB) · `.cache/vm/venv-ch23-persistence`(233MB) · `$ROOT/.cache/ch23-prep/`(SQLite 시험 파일 넷) · `.cache/ch23-0N-view/`(N=1~7) · `.cache/ch23-close/`(마감 전 사본·확인 스크립트·로그) · 기기 `/tmp/ch23-prep`·`/tmp/ch23-01`~`/tmp/ch23-07`·`/tmp/ch23-close` · 기기 세션 임시 폴더 `$TMPDIR/ch23-0N-*`(노트북 실행·노트북 밖 확인이 만든 임시 폴더) · `/tmp/reviewA23`·`/tmp/reviewB23`(검토 재현 파일).
6. **코드 쪽 다음 재실행 몫**: 01·02·03·05는 마감에서 다시 실행하지 않았고, 코드를 고쳐야 맞는 자리는 없었음(모든 지적이 글로 해결). 다음에 다시 실행하면 02는 `pre_exec.sh` 방식으로 같은 호출 안에서.
7. **Part 6 옛 검사 스크립트 넷(고치지 않음, 마감에서 돌린 결과)** — 모두 Ch 23에 닿기 전에 멈춤: `check_scope.py` Ch 21 `_src/07-create-agent-실습.html` `Missing scope`(Ch 23 07 「실습 30분」도 같은 모양) · `check_figures.py` Ch 21 `01-1-….svg`의 `.excalidraw` 짝(Ch 23 새 SVG도 짝 없음) · `check_notebook_readiness.py` `assert len(reports) == 47`(Part 6 노트북 50) — **결과 파일 `notebook-readiness.json`을 먼저 씀 → 실행 전 사본으로 되돌림** · `check_visual_reports.py` `ch22-middleware`에서 멈춤(Part 6 `visual-results.json`은 쓰지 않음, Ch 23 줄은 16).
8. **`llm-practice.zip`**: Part 6 `check_delivery.py`가 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`(117행)에서 멈춤(결과 파일 안 바뀜). 사본에서 그 zip만 빼면 HTML 61 · 링크 1,091 · 누락 0 · 절 50 · 복습 189문항 오류 0 · 비밀값 0 · 개인 경로 0 · `part6-practice.zip` `aa82b386…` 99항목(part6 노트북 50) 통과. `llm-practice.zip` 안 Ch 23은 옛 판 — 전체 묶음 재생성 때.
9. **`textbook/_notebook/build_index.py`**(Ch 23 절 수 6 · 설명) — 선례대로 고치지 않음, 전체 목차 마감 때. **`textbook/part6/qa/final-artifact-hashes.json`**(Ch 23 줄이 옛 판 — 만드는 스크립트 없음) — 전체 마감 때 다시 모을지. **Part 6 공용 `visual-results.json`의 다른 챕터 줄 76개**가 옛 HTML 해시(Ch 22 등) — Part 6 마감 때 `visual.cjs`를 다시 돌려 모을 것.
10. **과정 요약·계약 문서(누적 문서 몫)**: Ch 23 용어(§4 — 「이어 실행」 한 뜻 · 「같은 스레드로 다시 실행」 · 「실행 흐름」 ≠ 스레드 · 「표 만들기」 ≠ Ch 21 「옮기기」 · 「스레드 재개」 ≠ Ch 24 `resume`)와 도구 파일 `checkpoint_tools.py`(`a850b2cd…`)는 과정 요약에 아직 넣지 않음(Part 6 마감 오케스트레이터). 계약 파일은 없음.
11. **옛 기록 파일**: `qa/research.md`·`qa/verification.md`·`집필점검표.md` 머리에 「개선 전 판」 표시(내용은 그대로) · `textbook/part6/qa/ch23-technical-review.md`(Part 6 쪽 옛 검토 기록 — 고치지 않음) · `qa/upgrade/review-pack/`(검토에 쓴 마감 전 묶음 — 다시 만들지 않음) · `textbook/part6/qa/language/ch23-*`(옛 감사 기록).
12. **2차 검토**: 두 검토의 「확인하지 못한 것」(한국어 감사 3단, Windows·macOS 실제 실행, 학생 `.venv` 첫 셀)과 §12.
13. **보호 파일 목록(마감 끝 대조)** — 바뀐 23: `labs/part6/ch23-persistence/README.md`·`durability_worker.py`·`idempotency_worker.py`·`notebooks/01~06`(여섯) · `textbook/part6/ch23-persistence/qa/author_ch23_ch24.py` · `textbook/downloads/part6-practice.zip` · `textbook/part6/public-files.json` · 챕터 `qa/public-files.json` · 챕터 `qa/verification.md` · 챕터 `qa/research.md` · `textbook/part6/qa/integration-results.json` · `bundle-execution.json` · Part 6 `visual-results.json` · `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json` · `textbook/_notebook/checks/ch23-persistence/visual-results.json` · `textbook/part6/index.html` · `textbook/part6/_build_index.py` · 챕터 `chapter.json` / 옮김 1: `figures/_gen_figures.py`.

## 17. 검토 1차와 반영 (2026-09-25 마감)

- 판정: **A(01~03·공통) 중 2 · 하 17**(01 중 1·하 3 · 02 하 7 · 03 하 7 · 공통 중 1), **B(04~07·공통) 상 1 · 중 2 · 하 12**(04 상 1·하 5 · 05 중 2·하 1 · 06 하 2 · 07 하 2 · 공통 하 2).
- **[상] 1건 반영 — B-1**: 04 4·5절 띄우기·끊기를 한 셀로(+ `assert` 둘), 실행마다 새 파일 이름(`new_prefix`, 04가 가르치고 도구 파일로), 04·06·07 새 커널 두 번(04 26/27 — `async` 줄만, 06 23/23, 07 22/22), 셀 다시 실행 확인(§6), 04-2 다시 렌더.
- **[중] 4건 모두 반영**: A-1(「이어 실행」 한 뜻 — 01 b4·6절·b6·결과 읽기 둘, 02 셀 44, 07 b3 표) · A-19(실습 폴더 README 전체 다시 씀 + `_build_index.py`로 묶음) · B-7(05 b7 공식 문서 문장을 관찰과 맞게 — 근거가 아님을 밝히고 소스 행으로, `05-probe.md` 정정) · B-8(05 노트북 셀 14에 0.1초의 까닭과 `exit` 조건, b6 한정 — 07 셀 10과 맞음).
- **[하] 29건 모두 반영**: A-2(01-4 도식 읽기) · A-3(-1 문장) · A-4(01-5 prompt 기록) · A-5(`setup()` 0번 문장) · A-6(`OperationalError` 한정) · A-7(`prepare_threshold=0`) · A-8(sqlite 3.0.3) · A-9(b5 명령 자리·까닭) · A-10(`SCHEMA` 이음) · **A-11(그대로 — 챕터 리드 결정, 02 진단·§12에 기록)** · A-12(`add_messages` 출처) · A-13(`with` 선례 Ch 10 02 + 「과정 두 번째」 기록 정정) · A-14(읽거나 쓸 때) · A-15(`check_same_thread`·실행 흐름) · A-16(「스레드 재개」 영어 괄호 뺌 + Ch 24와 다른 장면) · A-17(비유 이음 — 03 [18]·02 b4) · A-18(Ch 22 09 출력 모양) · B-2(다시 실행 — B-1과 함께 코드로) · B-3(Windows 종료 코드 1) · B-4(프로세스 풀이) · B-5(meta `|`) · B-6(검사 문장 373 기록 정정) · B-9(팬아웃 뜻) · B-10(06 b4 「끝나지 못한 노드」) · **B-11(`kill_then_resume` 남김 — 독스트링을 사실대로, §12 강사 확인)** · B-12(06·07 「칸 값과 칸에 낸 갱신」) · B-13(07 리본 풀이·prompt 기록) · B-14(README — A-19와 같음) · B-15(`objectives` 일곱 줄·`_build_index.py` 설명·공개 목록 옛 SVG 줄).
- **반영하지 않은 갈래와 까닭**: 없음(게이트를 깨뜨리는 지적 없음). 뒤 챕터 파일 수정(Ch 24·30·31 — §15 기록) · 완료 챕터 Ch 22 09 b8(A-18 권고대로 그대로) · 삽화 다시 만들기(글만) · 01·02·03·05 다시 실행(모든 지적이 글로 해결)은 과제 결정대로 하지 않음.
- **노트북 해시 전후**(`code_sha256` / `outputs_sha256`, 앞 12자): 01 `9d71f6f9522f`/`4315f7f9e3d3` 그대로 · 02 `5b4fa7cf7d92`/`abb4f3d737b3` 그대로 · 03 `fe89a30aec83`/`952dc36685ea` 그대로 · 04 `ff4e48c4a731`/`845cda331722` → **`490b1737b666`/`341f57f44e66`** · 05 `06cd28c63aff`/`b39f9ee7fbdf` 그대로 · 06 `52c92b7d3410`/`8cf67c492cc6` → **`8d7467afba42`/`8bf6435755e7`** · 07 `c950067c72cc`/`5db80578cc6b` → **`166e293b3b08`/`463388271dd6`**. 일곱 노트북 모두 `metadata.verification`과 다시 계산한 값이 같음. 셀 수 59·63·61·**57**·45·52·47(04만 59 → 57).
- **다시 실행한 셋의 바뀐 셀**: 04 — 끊는 셀 합침·`new_prefix` 셀·마지막 셀 라벨(`4절 SQLite 파일 이름: exit-1.sqlite`), 되풀이 셀 `async` 줄 5/5(둘째 단락·b7만 `mdpatch.py`로 고침) · 06 — 가져오기 줄(`new_prefix`)·마지막 셀 라벨(`4절 기록 파일 이름: naive-1.record`) · 07 — 가져오기 줄·설정 셀(`prefix`)·연결 셀 파일 이름 줄·견주기 줄 앞머리·파일 목록. **결과 읽기 첫 단락은 새 출력으로 생성기에서 먼저 씀**, 결론·그림·정리·복습의 값은 바뀌지 않음.
- 고친 방법: 01·02·03·05는 `.cache/ch23-close/tools/cpatch.py`(생성기·노트북 마크다운·`_src`에 함께 — 노트북 코드 셀에 옛 글이 있거나 생성기 코드 문자열에 걸리면 멈춤, 적용 전 대상별 횟수 확인, 03 b3는 링크 상수 때문에 생성기를 직접) → `run_section.sh … 0N --no-exec`(02는 `nx.sh`) · 04·06·07은 생성기(`patch04*.py`·`patch06.py`·`patch07*.py`, 모두 `assert` 한 번 맞음) → `run_section.sh … 0N`(A) + 사본 `execute.py`(B) → `async` 값만 `mdpatch.py` → `--no-exec`. 마감 뒤 생성기 `author_01~07.py`의 `cells()`·`src_html()`이 노트북·`_src`와 글자까지 같음(7/7). 마감이 더한 문장의 금지어 0, 게이트 G6 0.
- 검사: `upgrade_gates.py … --label after` **7/7 PASS, G1~G7 0** · AST 따로 금지 문법 0 · `verify.py --chapter` **PASS 7 sections / 178 code cells (max 14 lines)** · 빌드 HTML 여덟 `{{` **0건** · `visual.cjs` **16행 PASS** · Part 6 `check_bundle_execution.py` **PASS**(Ch 24 01·Ch 28 01) · Part 6 `check_delivery.py`는 `llm-practice.zip` Part 1 Stale에서 멈춤(그 zip을 뺀 대조 통과, §16 8번) · 보호 파일 123개 99 같음 · 23 의도한 변경 · 1 옮김 · 남은 자식 프로세스·켜진 PostgreSQL 서버 0.
