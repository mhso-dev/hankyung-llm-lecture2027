# Ch 23 Persistence와 Durable Execution — 절 사이 인계 (handoff)

- 챕터: `textbook/part6/ch23-persistence`(01·03·04·05 experiment, 02·06 paired) · 실습 폴더 `labs/part6/ch23-persistence`.
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md`(§2-12 Ch 20·§2-13 Ch 21) → Ch 21 요약 `textbook/part6/ch21-create-agent/qa/upgrade/chapter-summary.md`(§13·§14) → 준비 노트 `qa/upgrade/chapter-lead-notes.md`(§2 절별·§5 설치판 동작·§6 02 선택지·§7 결정적 장면·§8 도구 파일·§9 과정 규칙·§10 비유) → **이 파일** → 앞 절 `NN-diagnosis.md`·`_src`(특히 b8).
- 이 파일은 `## 챕터 공통`(01절이 정한 것)과 절마다 `## §NN → §MM`을 이어 붙입니다.

## 챕터 공통 (01절에서 정한 것)

### 챕터 리드 결정 (그대로 이어 지키세요)

1. **모델은 부르지 않습니다(M1·M3)**. 키 셀·모델 셀 없음, 준비물에 「모델 요청 0번」과 까닭 한 문장(01 판: 「이 챕터는 상태를 저장하고 이어 가는 일이 주제입니다. 매번 같은 값을 내는 우리 노드로 그래프를 만들어야, 저장된 값이 맞는지 출력으로 가를 수 있습니다.」). 대화가 필요한 절(03·07)은 **메시지 칸(`add_messages`)에 코드가 만든 `HumanMessage`·`AIMessage`**(Ch 13 04·Ch 20 01 모양)를 쌓고, 「답」은 모델 글이 아니라 노드 함수가 만든 글이라는 것을 한 문장으로 — Ch 22 09 b8 「종류별로 출력한 대화 기록(메시지)」이 참이 되게. 잠금(`pyproject.toml`·`uv.lock`)은 바꾸지 않음(`langchain-core 1.6.2`가 잠금에 있어 메시지 클래스는 설치 셀에 `langchain-core==1.6.2`만 더하면 됨).
2. **파일 쓰기 자리는 임시 폴더**(Ch 4 03 선례). 모든 절이 같은 준비 셀 모양(아래 「준비 셀」). 까닭: 이 작업 기기에서 연결 폴더 안 SQLite 쓰기가 `disk I/O error`로 멈추고(준비 노트 §5-5 — 진단에만 적고 학생 본문에는 「실습 폴더에 파일을 남기지 않으려고」), 학생 폴더에 `.db`·`-wal`·`-shm`을 남기지 않기 위해. **worker 스크립트에 넘기는 경로도 이 임시 폴더**(04·06).
3. **02 PostgresSaver는 선택지 A**(Ch 12 02 방식 — 작업 기기의 `.cache/vm/pgenv` PostgreSQL을 절 실행 전에 켜는 `qa/upgrade/pre_exec.sh`) — 실제 결함(`setup()` 없이 `UndefinedTable`)과 표 넷을 출력으로. 학생 쪽 안내는 Ch 12와 같은 접속 방식. 02 몫(아래 §01 → §02).
4. **강제 종료 장면(04·06)은 유지**(`subprocess`로 worker를 실행하고 끊기 — Ch 20 02 b7이 04·05·06을 링크, 04는 「강제 종료 뒤」 장면을 지켜야 참). **결론은 결정적 값만**: exit ↔ sync(20/20·20/20), 체크포인트 수(exit 0·sync 3 등). **async는 흔들림**(준비 확인 60번 중 56 first · 4 잃음) — 결과 읽기 둘째 단락과 b7에만, 셈은 「이번 확인에서는」. 그림 라벨·캡션·정리·복습에는 async 값 금지.
5. **도구 파일 B안**: 새 파일 `labs/part6/ch23-persistence/notebooks/checkpoint_tools.py`(과정의 다른 도구 파일 이름과 겹치지 않음). **01은 만들지 않았습니다**(아래 「도구 파일」). 04·06·07이 되풀이할 강제 종료·기록 출력 같은 평범한 함수를 **처음 가르친 절은 노트북에**, **처음 가져오는 절이 파일을 만들고** 묶음 목록 둘(`textbook/part6/public-files.json`·챕터 `qa/public-files.json`)에 더함. worker 스크립트 자리·이름은 04 몫.
6. **슬러그 01·04·05·06은 바꾸지 않음**(Ch 20 02·03 b7 링크). 02·03도 바꾸지 않는 쪽으로.
7. **공용 옛 생성기 `qa/author_ch23_ch24.py`는 01이 Ch 23 쪽만 막음**(아래 「옛 생성기」). `figures/_gen_figures.py`는 맨 위 `raise SystemExit(...)`. 옮기기는 마감 몫.
8. **문법 범위**: 노드·도움 함수 타입힌트 없음(Ch 13·20·21) · 상태 형식은 Ch 13 모양(칸만 적은 `TypedDict`, 칸 구성이 바뀌면 새 이름) · 리듀서는 `operator.add`·`add_messages`(`lambda` 금지) · `with`(파일 `open` 밖)·`try/finally`·`subprocess.Popen`은 처음 쓰는 자리에서 한 문장씩(아래 「허용 문법 범위」).
9. **용어**: Ch 13·20·21 말 이어 쓰기(아래 표). 새 말은 쓰는 절만 정의(01은 체크포인터·체크포인트·스레드 셋).
10. **06 함수 이름에 Ch 24 API 이름 `interrupt`를 쓰지 않기**(옛 `interrupt_then_resume` → 다른 이름). Ch 24 API(`interrupt`·`Command(resume=)`·`update_state`·타임 트래블) 앞당겨 쓰지 않기.
11. **비유 계열 「체스판과 즉석사진」**(01이 엶, 아래).
12. **준비 셀은 과정 표준**(설치 `%pip` 줄은 잠금 판 번호까지, 그 절이 실제로 가져오는 패키지만).

### 준비 셀 (01 판 — 뒤 절은 이 모양을 그대로)

1. 설치 셀 `nbkit.install_source([...])` — 01: `"langgraph==1.2.11", "langgraph-checkpoint==4.2.0"`. 뒤 절 판(잠금): `langgraph-checkpoint-sqlite==3.0.3`(03~06, `aiosqlite`·`sqlite-vec`는 옮겨 오는 의존) · `langgraph-checkpoint-postgres==3.0.5`·`"psycopg[binary,pool]==3.3.3"`(02) · `langchain-core==1.6.2`(03·07 메시지 클래스). **`pip==26.2`는 잠금 dev에 있음**(규격 §7-2 조건 충족, 확인만).
2. 가져오기 셀 — **도구 파일 가져오기는 여기서(임시 폴더로 옮기기 전)**. 규격 §2-7 5번: 커널은 가져올 파일을 현재 작업 폴더에서 찾음.
3. 임시 폴더 셀(`lesson_role="setup"`):
   ```python
   # 파일이 생기는지 볼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다(Ch 4 03절과 같은 모양)
   import os
   import tempfile

   # mkdtemp()는 운영체제 임시 폴더 안에 새 폴더를 만들고, 그 폴더의 위치를 글로 내놓습니다
   practice_folder = tempfile.mkdtemp(prefix="ch23-NN-")
   # chdir()는 터미널의 cd처럼 현재 작업 폴더를 옮깁니다
   os.chdir(practice_folder)
   print("임시 폴더 이름에 ch23-NN-이 들어 있는가:", "ch23-NN-" in practice_folder)
   print("현재 작업 폴더의 파일:", os.listdir())
   ```
   **폴더 위치는 출력하지 않음**(실행마다 달라 새 커널 두 번 대조가 깨짐 — 과정 §3 「임시 경로는 인용하지 않음」). 결과 읽기 `True`·`[]`. 01 설명 문장: 「이 챕터의 뒤 절들은 체크포인트를 파일에 씁니다. 실습 폴더에 파일을 남기지 않으려고, 모든 절이 이 모양으로 빈 임시 폴더에서 시작합니다.」·「모듈 `os`와 `tempfile`은 Python에 들어 있는 기능 묶음입니다.」 — 뒤 절은 「01절처럼」 한 문장이면 됨.
4. **04·06 worker 경로**: `execute.py`는 저장소 루트에서 커널을 띄우고 학생은 `notebooks/`에서 엶 → worker 파일 자리를 **임시 폴더로 옮기기 전에** 과정 모양 자리 찾기 셀(`candidates = [".", "../../..", "../../../.."]` + `for`·`break`, 옛 `[Path.cwd(), *…parents]`·`next(…)` 금지)로 찾거나, 도구 파일 폴더 기준으로 정할 것(04 몫). 준비 셀 차례는 **설치 → 가져오기 → (자리 찾기) → 임시 폴더**.

### 01이 푼 문장 (뒤 절은 되풀이하지 말고 「01절에서 본 것처럼」으로)

- 제목 말: **Persistence = 실행이 끝난 뒤에도 상태를 남겨 두는 일(상태 저장)** · **Durable Execution = 멈춘 실행을 저장된 자리부터 다시 이어 가는 일(이어 실행)**(노트북 1절·`_src` b2).
- `builder.compile(checkpointer=memory)` — 같은 설계 객체를 `compile()`과 `compile(checkpointer=…)`로 둘 만들 수 있음. 속성 `checkpointer`(없으면 `None`).
- 설정 딕셔너리(Ch 20 03)의 키 `configurable` 아래 `thread_id` = 스레드 이름. 설정 딕셔너리는 상태에 들어가지 않음. **설정 없이 부르면 `ValueError`**(`Checkpointer requires one or more of the following 'configurable' keys: thread_id, checkpoint_ns, checkpoint_id` — `pregel/main.py` 2589~2593행).
- `get_state(config)` → `StateSnapshot`(「그 스레드의 마지막 체크포인트를 담은 객체」): `values`(저장된 칸 값)·`next`(다음에 실행할 노드 이름들, 끝났으면 `()`)·`metadata["step"]`(단계 번호)·`metadata["source"]`(만든 자리 `input`/`loop`). **없는 스레드 이름은 오류 없이 `{}`·`()`**.
- `get_state_history(config)` → 최신 것부터. `list(...)`로 담아 셈. **노드 하나 그래프는 실행 한 번에 체크포인트 셋**: 입력을 받은 때(`input`, 다음 `('__start__',)` — 가상 시작점이 입력을 칸에 넣을 차례) · 입력을 칸에 넣은 뒤(`loop`, 다음 `('add',)`) · 노드를 마친 뒤(`loop`, 다음 `()`). 첫 입력은 단계 -1부터. 체크포인트 ID·만든 시각(`created_at`)은 실행마다 다름 → 출력하지 않음.
- **이어 실행 규칙**: 같은 스레드로 다시 부르면 마지막 체크포인트에서 시작 → 새 입력을 칸의 규칙대로 넣음 → 노드 실행. 입력에 넣지 않은 칸은 저장값 그대로, **규칙 없는 칸에 넣은 값은 저장값을 덮어씀**(01 10절 `customer-c` 합계 4), 규칙을 적은 칸은 노드 갱신이 뒤에 붙음. **03의 메시지 칸(`add_messages`)은 입력 메시지가 저장된 목록 뒤에 붙는 쪽**(01은 규칙 칸에 입력을 넣어 보지 않음 — 03이 출력으로 보일 것).
- 체크포인터 없는 그래프에 둘째 입력만 넣으면 `KeyError: 'total'`(상태가 남지 않음). 새 `InMemorySaver` 객체로는 같은 스레드를 못 읽음(`{}`) — 「체크포인트는 그래프가 아니라 체크포인터 객체 안」. 커널 다시 시작은 **실행 안 함**(공식 문서 「When the process restarts, all checkpoints are lost」만). `InMemorySaver`는 파일을 쓰지 않음(임시 폴더 `[]`).
- 01이 실행하지 않은 것: Store(b7 한 줄) · 에이전트 그래프에 체크포인터 · 노드 여럿 그래프의 체크포인트 수 · 실패로 멈춘 실행의 체크포인트(준비 확인에서는 실패한 스레드도 체크포인트 둘·`next ('add',)`이 남음 — 05가 출력으로) · 저장 시점(durability) · 걸린 시간.

### 도구 파일 — 01은 만들지 않음 (결정 5 「01이 쓸 일이 없으면 만들지 말기」)

- 01은 앞 챕터 함수를 가져오지 않음(Ch 20 `graph_tools.py`·Ch 21 `runner_tools.py`는 메시지·사용량 함수 — 모델 없는 챕터라 쓸 곳이 적음. 03이 메시지 칸을 출력할 때 Ch 19 06 `show_messages`(Ch 21 `runner_tools.py` 판, 종류·도구 호출 요청·도구 메시지만 찍음)를 쓸지 판단 — 쓰면 그 절이 `checkpoint_tools.py`를 만들고 옮김).
- **01이 처음 가르친 함수(노트북에 있음, 뒤 절이 쓰면 옮길 후보)**: `print_history(history)` — 라벨 줄 `단계 번호 | 만든 자리 | 다음 노드 | 칸 값` + 체크포인트마다 한 줄(내놓는 값 없음, 본문 5줄) · `thread_row(compiled_graph, thread_name)` — `{"스레드", "합계", "실행 흔적", "체크포인트 수"}`(칸 `total`·`trace`를 읽음 — 01 상태 형식 전용, 다른 칸이면 새 함수). 옮길 때 `# Ch 23 01절에서 배웠습니다 — …`, 본문 글자·AST 같게(생성기에서 01 판과 대조 — Ch 21 `check_same_as_before()` 모양), 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 …」, `run_section.sh`가 `notebooks/`를 `PYTHONPATH`에 더함(자리 찾기 셀 결과 읽기에 그 한 문장 — 과정 §9).
- 함수 파일 규칙: 금지 문법 0(규격 §2-7 4번), 인자로만 받기, `subprocess`·`sys`·`time`을 쓰면 import 셋 — 처음 가르친 절 노트북에서 한 문장씩.

### 용어 (01절에서 정한 것 — 뒤 절은 그대로 이어 씁니다)

| 절 | 말 | 뜻 | 코드에서 |
|---|---|---|---|
| 01 | 체크포인터(checkpointer) | 그래프가 단계를 하나 마칠 때마다 그때의 상태를 저장해 두는 부품 | `InMemorySaver()` → `builder.compile(checkpointer=memory)` |
| 01 | 체크포인트(checkpoint) | 체크포인터가 한 번 저장한 상태 하나 | `get_state_history` 목록의 항목(`customer-a` 여섯) |
| 01 | 스레드(thread) | 한 이름으로 묶인 체크포인트들의 줄(이름은 설정 딕셔너리의 `thread_id`) | `{"configurable": {"thread_id": "customer-a"}}` |

- 01 meta 「새 용어」 3(옛 판 3 그대로).
- **일반 말(새 말 아님)**: 상태 저장(Persistence 풀이)·이어 실행(Durable Execution 풀이)·스레드 이름·마지막 체크포인트·체크포인트 목록·단계 번호(`step`)·만든 자리(`source`)·다음 노드(`next`)·저장된 칸 값(`values`)·읽은 것의 종류·임시 폴더·합계·이번 수.
- **이어 쓰는 말**: Ch 13 상태·상태 형식·노드·엣지·설계 객체·컴파일·실행 흔적·가상 시작점/끝점·리듀서·덮어쓰기·이어 붙이기·표시 `Annotated`·메시지 리듀서·갱신 · Ch 20 단계·실행 한도·설정 딕셔너리 · Ch 16 05 실패 흉내(05·06이 쓸 때) · Ch 2 05 `try`·`except 이름 as error`.
- **뒤 절 새 말 후보(그 절이 정의 — 01은 쓰지 않음)**: 저장 시점(durability, 04 — 「내구」 한자어는 제목에만, 본문은 「저장 시점」) · 강제 종료·자식 프로세스(04) · 남은 쓰기(pending writes, 05 — 제목 말) · 멱등성(06 — 뜻 → 일상 예 → 코드 세 문장)·멱등 키 · 표 만들기(`setup()`, 02 — DB 「마이그레이션」 대신, Ch 21 04 「옮기기」와 다른 뜻) · DB 「스키마」는 「이름 공간」 등(02 — 제목에만, 강사 확인).
- **금지어(01 설명·주석·캡션·`.mmd` 0건 — 제목·슬러그·코드 백틱 말고)**: 「지시」·「반환」(→내놓다)·「추정」(→예상)·「지연」(→걸린 시간)·「분기」(→갈래)·「경로」(→자리·위치·차례)·「trace」(→실행 흔적)·「스키마」·「superstep」·「super-step」(→단계)·「병렬」(제목 밖 — →함께 실행·같은 단계)·「노드」(Ch 13 뜻 밖)·「스냅샷」(→읽은 체크포인트·저장된 상태)·「채널」(→칸)·「식별자」(→이름)·「레코드」·「로그」(→기록)·「마이그레이션」(DB 뜻 — →표 만들기)·「런타임」·「트랜잭션」·「원자적」·「경합」·「보장」·「정확히 한 번」·「측정」·「검증」(→검사)·「필드」(→칸)·「인터페이스」·「사전」(「사전에」 포함)·「동시」(「동시에」 포함)·「순차」·「돌려줍니다」류·규격 §4 「쓰지 않는 말」 전부·「쉽게·간단히·당연히」·「개선 전」·「강사 시연」. 금지어 검사 `/tmp/ch23-01/ban_check.py`(Ch 21 판 + 「스냅샷」·「superstep」·「Store」 — 「로그」는 「프로그램」 안 글자가 걸리니 눈으로 거를 것).

### 허용 문법 범위 (01절 AST 확인 — `/tmp/ch23-01/extra_check.py`, Ch 21 마감 판 복사)

- 01이 쓴 이름: `StateGraph`·`add_node`·`add_edge`·`START`·`END`·`compile(checkpointer=…)` · `InMemorySaver()` · `graph.invoke(입력, 설정)` · `graph.get_state(설정)`·`.values`·`.next`·`.metadata["step"]`·`["source"]` · `list(graph.get_state_history(설정))` · `type(x).__name__` · `"글" in 글` · `try`·`except KeyError as error`·`except ValueError as error` · `tempfile.mkdtemp(prefix=…)`·`os.chdir`·`os.listdir()` · `assert`(코드로 정해지는 값 둘).
- 01이 안 쓴 것(0건): f-string · 내포식 · 제너레이터 식 · `lambda` · 조건 표현식 · `elif` · `next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`sorted` · `key=`·`reverse=` · `set` · `setdefault` · 노트북 `.get` · `+=` · 기본값 매개변수 · 타입힌트(상태 형식 칸 말고)·반환 힌트 · 튜플 풀기 · 별표 풀기 · `with` · `is` · 데코레이터 · 클래스(상태 형식 말고) · `Path`.
- **과정에서 처음이라 쓰는 절이 한 문장씩 풀 것**: `with`로 `open` 밖의 것 열기(`SqliteSaver.from_conn_string(…)`·`PostgresSaver.from_conn_string(…)` — Ch 21 04 `warnings.catch_warnings`가 첫 선례, 「블록이 끝나면 연결을 닫습니다」는 소스 확인 뒤에만 — **`with sqlite3.connect(…)`는 연결을 닫지 않음**, 준비 노트 §5-5) · `try`/`finally`(Ch 2 B만) · `subprocess.Popen`·`.kill()`·`.wait(timeout=)`(과정은 Ch 2 `subprocess.run([sys.executable, …])`까지, `Popen`은 Ch 4 준비 셀 예외뿐) · `time.time()` 기한 루프·`time.sleep`(Ch 16 05에서 `sleep`) · `sys.executable`(Ch 2 `subprocess.run` 모양에서 봄).
- 게이트 G2: **호출 안 호출 안 호출**(`len(list(graph.get_state_history(c)))`)은 `nested_call_2plus` — 변수에 먼저 담기(01 8절 모양). 셀 모양: 01 코드 셀 **28개**(준비 셀 셋), 준비 셀이 아닌 셀 주석 뺀 코드 최대 8줄, 함수 본문 최대 7줄, 셀당 정의 하나. 여러 줄 출력은 라벨 줄 따로(`print_history` 첫 줄).
- **괄호 뒤 마침표 `).`는 G6가 문장 끝으로 세지 않음** — 절 번호·행 번호 괄호는 문장 가운데로(「Ch 13 01절처럼 다음 셀은 …」).

### 색 (01절 Mermaid 4장, 빨강 0, 보라 0)

- 넘긴 값·입력·설정 딕셔너리 초록 · 우리가 적은 설계 객체·노드 함수·상태 형식 파랑 · 출력으로 확인한 값·**셀에서 받아 출력한 오류(experiment)** 노랑 · 라이브러리가 만든 그래프·체크포인터·공통 사실 회색 · **모델 없음 → 보라 0 장**(모든 절) · **experiment 절 빨강 0**, **paired 절(02·06)의 Before 결함 결과만 빨강**.
- 스레드를 고르는 갈래(체크포인터 → 스레드별 줄)는 점선. 체크포인트 목록은 오래된 것부터 그리고 「출력은 최신 것부터」를 도식 읽기에. 원본 폭 01: 493·669·552·808(모두 868 이하). 칸 셋을 가로로 둘 때 공통 회색 상자는 `~~~`로 아래에(01-4). 칸 둘을 `TB`로 쌓으면 세로가 950을 넘어 `LR`로 바꿈(01-3).
- 렌더를 직접 부를 때 `PUPPETEER_CACHE_DIR=/tmp/pptr-cache LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu`를 줄 것(`run_section.sh`는 자동).

### 비유 계열 — 「체스판과 즉석사진」 (01절이 엶, 챕터 리드 결정 11)

- 뜻 짝: **체스판 = 스레드의 상태** · **즉석사진 한 장 = 체크포인트** · **카메라(와 사진을 모아 두는 일) = 체크포인터** · **판 하나와 그 판 앞의 사진 묶음 = 스레드** · 한 번 둘 때(실행 한 번) 사진 셋.
- 01: 나무 탁자 둘·체스판 둘, 왼쪽 판 앞 사진 **여섯 장(세 장씩 두 줄)**, 오른쪽 판 앞 **세 장(한 줄)**, 두 탁자 사이 바닥 카메라 하나. 삽화 `01-5-판마다-따로-쌓이는-즉석사진`, 2차 job `547c15e2-02f2-43a4-be28-24aa6a51fbde` 채택(1차 `a6d9c270-…` 왼쪽 다섯 장이라 탈락), 4크레딧(거래 08:05:01Z·08:05:55Z).
- **뒤 절 후보**: 02 빈 사진첩에 칸(비닐 주머니) 넷을 먼저 붙여 두어야 사진을 꽂을 수 있음(`setup()`이 표 넷을 만듦) ↔ 사진첩 없이 쌓인 사진(Before) — **「선반」은 Ch 15 소품이라 쓰지 않기**(준비 노트 후보 A의 선반을 사진첩으로) · 03 다음 날 빈 판 옆 마지막 사진 한 장을 보고 말을 다시 놓음(새 연결·새 그래프 객체) · **04 sync = 사진이 다 나온 뒤 다음 수 / async = 사진이 아직 하얗게 나오는 중에 다음 수 / exit = 판이 끝날 때만 한 장, 그리고 엎어진 판** — async 흔들림은 「아직 하얗게 나오는 사진」으로 읽힘(그림 라벨에 async 결과 값 금지) · 05 나란한 두 판 중 한 판만 쓰러지고 다른 판의 마지막 사진은 남음(남은 쓰기) · 06 같은 수를 두 번 적은 기보 ↔ 이미 적힌 수는 건너뜀(멱등 — 06이 정함).
- 규칙: 사람·손·화살표·화면·글자·숫자·시계 없음, 물건은 크게, 개수·자리·상태를 이름으로. **여섯처럼 큰 수는 한 줄에 늘어놓으면 틀리게 나옴(01 1차 다섯 장) → 「two rows of three」처럼 세기 쉬운 배열로**. 앞 챕터 소품(쟁반·서랍·바구니·저울·울타리·발자국·공구판·승강 상자·식당 전표·집게·세탁기·선반·도장·카드·봉투) 금지. 스타일 첫 문장은 규격 §5-4 그대로.
- 저장: 기기 셸 `curl` → `UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pillow`로 폭 1100(LANCZOS) → `figures/`, 결과 URL을 한 번 더 받아 같은 폭으로 줄여 픽셀 대조, 사본 `.cache/ch23-NN-view/`를 `device_stage_files` → `Read`로 보고 개수를 셈. 크레딧은 **거래 기록으로 이 절 몫**을 가릴 것(다른 세션이 씀).

### 옛 생성기 (결정 7)

- **공용 `qa/author_ch23_ch24.py`**: 머리 주석 세 줄 + `write_all()` 노트북 고리·`_src`/그림 생성기 고리에서 `chapter == "ch23-persistence"`면 건너뜀(`44c9d593…`). Ch 24 쪽 산출은 막기 전후 같음(사본 `/tmp/ch23-01/gen/A`·`B` `diff -r`). **옮기지 않음** — Ch 24가 개선 때 이 파일을 어떻게 할지 정하고, 마감 때 `before/generators/blocked/`로 옮기면 Ch 24 쪽이 찾는 자리가 바뀜(Ch 24 몫 인계).
- `figures/_gen_figures.py`: 맨 위 `raise SystemExit(…)`(`6d95031c…`, 실행하면 종료 코드 1). 옮기기는 마감 몫.

### 파일 쓰기·슬러그·시간·비용

- 파일 쓰기: 임시 폴더에만(위). 01은 파일 0. 실습 폴더 `data/`는 만들지 않음.
- 슬러그: 01·04·05·06 고정(Ch 20 링크), 02·03도 그대로.
- 걸린 시간: 재지 않음(준비물의 「N초 안에」는 셀 실행 기록 — 01 A 약 1.4초 → 「5초 안에」). 04의 「느리고 빠름」 문장은 재지 않았으면 쓰지 않음(규격 §3, 준비 노트 §7-3).
- 모델·임베딩 요청 0, Higgsfield는 절당 1장(재생성 1회까지).
- 새 커널 두 번: A `run_section.sh` · B 사본 `/tmp/ch23-NN/B.ipynb`를 `execute.py`로(`UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch23-persistence UV_NO_SYNC=1 PYTHONPATH=$ROOT/labs/part6/ch23-persistence/notebooks`) → `/tmp/ch23-01/cmpout.py`로 셀별 대조. **환경 변수 없이 `uv run --project labs/part6/ch23-persistence`를 부르면 실습 폴더의 macOS `.venv`를 건드리려다 `Operation not permitted`로 멈춤**(01에서 한 번 — `.venv` 안 파일 변화 없음 확인). 04·06은 자식 프로세스라 **실행마다 달라지는 값(프로세스 번호·시각·임시 위치)을 출력하지 않을 것**.

### 완료·대기 챕터 문장 (01에서 확인)

- Ch 20 03 b7 「체크포인터는 Ch 23 01절에서」 — **참**(01). Ch 21 03 b4·b7·07 b7 「결과 상태를 저장해 다음 실행에 이어 쓰는 방법은 Ch 23에서」 — **참**(01 6절 3 → 7). Ch 20 02 b7(04·05·06) — 그 절 몫. **Ch 22 09 b8 「종류별로 출력한 대화 기록」 — 03이 메시지 칸으로 참이 되게**(결정 1). Ch 25·26 b3 「Ch23에서 체크포인터와 thread_id」 — 01로 참(대기 챕터, 고치지 않음). Ch 27 04 b3 「체크포인터 메시지」 — 03 몫.

## §01 → §02

**02절 주제**: 「PostgresSaver 준비와 스키마」(**paired**). 옛 판(`before/notebooks/02-…ipynb`·`before/_src/02-*.html`): `base_uri = os.getenv("CH23_POSTGRES_URI", "postgresql://postgres:postgres@localhost:55432/postgres")` · `DROP SCHEMA IF EXISTS ch23_lab CASCADE` → `CREATE SCHEMA ch23_lab` · `?options=-csearch_path%3Dch23_lab` · `lambda state:` 노드(값 6 → 12) · Before `setup()` 없이 `with PostgresSaver.from_conn_string(…) as saver:` → `except Exception as exc` + f-string · After `setup()` → `{'value': 12}` · `information_schema.tables` 내포식으로 표 넷.

1. **01절이 남긴 자리**: `_src` b8 「02절에서는 체크포인트를 PostgreSQL 데이터베이스에 저장합니다. 그 전에 체크포인트를 담을 표를 만드는 일부터 봅니다.」 · 노트북 정리 끝 같은 뜻 · b4 「비교와 경계」·노트북 11절 「프로그램 밖에 남기는 체크포인터는 02절과 03절에서 씁니다」 — 02가 **표를 만들고 거기에 체크포인트가 쌓이는 장면**을 보여야 참.
2. **이어 쓸 이름과 값**: 01 준비 셀 모양(설치 → 가져오기 → 임시 폴더 — 02는 파일을 쓰지 않지만 챕터 모양대로, 쓰지 않는다면 11절처럼 `[]`로 확인할 수 있음) · 01 상태 형식 `CountState`·노드 `add_amount`·설계 객체 셀(**01 판을 글자 그대로 복사하면 생성기에서 문자열 대조** — Ch 21 `check_same_as_before()` 모양) 또는 옛 판 값 6 → 12를 이름 있는 노드 함수로 · `print_history`(01 8절 — 02가 쓰면 도구 파일 `checkpoint_tools.py`를 만들 첫 절) · 스레드 이름은 옛 판 `before`·`after` 또는 01 모양. `get_state`·`get_state_history`는 「01절에서 본 것처럼」.
3. **선택지 A 실행 환경(결정 3)**: `qa/upgrade/pre_exec.sh`를 **Ch 12 판(`textbook/part3/ch12-retrieval-tuning/qa/upgrade/pre_exec.sh`)을 본으로** 새로 만듦 — `run_section.sh`가 절 실행 직전 source, 기기 셸 호출이 끝나면 서버도 꺼짐(절 실행마다 켬). 작업 기기 서버 `$ROOT/.cache/vm/pgenv/bin/{pg_ctl,initdb,postgres,psql}`(PostgreSQL 17.11). **학생 쪽 안내는 Ch 12 02와 같은 접속 방식**: Ch 12 02 셀 모양 `database_url = "postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab"` → `psycopg.connect(database_url, autocommit=True)` · `cur.execute`·`fetchone` · `except psycopg.Error as error` · `error.diag.message_primary`(Docker `pgvector/pgvector:0.8.2-pg17`, 컨테이너 `hankyung-part3-pgvector`, 호스트 포트 55432). 정할 것: (가) Ch 12 컨테이너·데이터(`.cache/vm/pgdata`)를 그대로 쓰고 이름 공간 `ch23_lab`만 따로 — 학생은 Ch 12에서 켠 컨테이너를 다시 쓰면 되고 포트 충돌(준비 노트 §2 02: Ch 12 ↔ 옛 Ch 23 둘 다 55432)이 사라짐, 대신 Ch 12 데이터 폴더에 이름 공간이 하나 늘어남(Ch 12 표와 겹치지 않는지 확인, `DROP SCHEMA ch23_lab CASCADE`는 그 이름 공간만) · (나) 02용 새 클러스터(`.cache/vm/pgdata-ch23`, 약 39MB — 준비 확인은 `/tmp/ch23-prep/pgtest` 포트 55439)에 Ch 12와 같은 접속 정보. 어느 쪽이든 **교재 본문은 학생 기준(Docker), 작업 환경 차이(conda-forge PostgreSQL 17.11 ↔ Docker 이미지 판)는 진단에만**. `psycopg` 판: Ch 12 잠금 3.3.5 ↔ Ch 23 잠금 3.3.3(설치 셀은 Ch 23 잠금 판).
4. **Before 실제 결함(paired)**: 서버가 있으면 `setup()` 없이 부를 때 `psycopg.errors.UndefinedTable`(`relation "checkpoints" does not exist`, sqlstate `42P01`, 종류 사다리 `UndefinedTable` → `ProgrammingError` → `DatabaseError` → `Error`)가 **결정적으로** 남(준비 노트 §5-4). 받기는 **`except psycopg.Error as error`**(Ch 12 02 모양) — 옛 `except Exception`·f-string 금지, 출력은 `type(error).__name__`·`error.diag.message_primary`·`error.sqlstate`(있는지 설치판 확인). 서버가 없으면 같은 셀이 `OperationalError … Connection refused`로 **다른 결함** → 서버 준비를 첫 셀들에서 확인(Ch 12 02처럼 `SELECT current_setting('server_version')` 출력)하고 진단에 적음. Before 결과는 **빨강**(paired).
5. **b3 고치기**: 옛 「Ch4에서 PostgreSQL 스키마와 information_schema.tables를 조회했습니다」는 **틀림** — Ch 4 03은 SQLite, PostgreSQL·psycopg는 **Ch 12 02**(링크 `../../part3/ch12-retrieval-tuning/02-pgvector와-HNSW.html`), `information_schema`는 과정 처음(한 문장). Ch 4 03 `SELECT` 모양은 표 조회 문장으로 이을 수 있음.
6. **After에서 보일 결정적 값(준비 노트 §5-4)**: 표 넷 `checkpoint_blobs`·`checkpoint_migrations`·`checkpoint_writes`·`checkpoints` · `checkpoint_migrations` 10줄(최대 v 9) · `setup()` 두 번째 부름은 오류 없음 · 한 스레드 실행 뒤 체크포인트·쓰기 줄 수(노드 수에 따라 — 02가 출력으로) · `PostgresSaver.MIGRATIONS`는 서버 없이 import만으로 출력 가능(10개 — `postgres/base.py` 37~85행). 표 이름 목록은 **내포식 대신 `for`+`append`**, 정렬은 SQL `ORDER BY`(Ch 4 03)로. `setup()` 독스트링 「It MUST be called directly by the user the first time」 ↔ `SqliteSaver.setup()` 「called automatically」(03과 대비 — 소스로만이면 「설치판 소스」로 표시).
7. **말**: 제목 「PostgresSaver」·「스키마」는 제목에만(강사 확인) — 본문 DB 「스키마」는 「이름 공간」 또는 「표 묶음」으로 한 번 풀고 되풀이, 「마이그레이션」(DB 뜻)은 「표 만들기」·「판 기록 표」 등(Ch 21 04 「옮기기」와 다른 뜻을 한 문장으로), 「반환」·「검증」·「로그」·「원문」·「트랜잭션」 금지. `autocommit=True`·`row_factory=dict_row`(준비 노트 §2 02 — `from_conn_string` 소스 56~75행)는 쓰면 한 문장씩.
8. **`with`**: `with PostgresSaver.from_conn_string(uri) as saver:`는 **과정에서 `open` 밖 두 번째 `with`**(Ch 21 04 `warnings.catch_warnings`가 첫째) 〔마감 정정 2026-09-25, 검토 A-13: 과정의 첫째·둘째가 아님 — 앞선 선례는 Ch 2 05 `with open`(A 트랙)·Ch 2 09·11(B 트랙)·**Ch 10 02 `with pdfplumber.open`**(라이브러리 객체, 기본 경로)·Ch 10 04·09 `zipfile.ZipFile`·Ch 21 04 `warnings.catch_warnings`. 03 b3·9절 설명은 Ch 10 02로 고침〕 — 「블록이 끝나면 연결을 닫습니다」는 설치판 소스로 확인한 뒤(`postgres/__init__.py` 56~75행)에만. 또는 Ch 12 02처럼 `psycopg.connect` → `PostgresSaver(conn)` → `conn.close()`로 `with` 없이(설치판 서명 확인).
9. **셀 모양과 그림**: 01 코드 셀 28(준비 셋), 비준비 셀 최대 8줄, 함수 본문 최대 7줄. 옛 c4 15줄 넘음·`lambda`·c8 내포식 고침. 그림 번호 `02-1`부터, 설계표 `qa/upgrade/02-figures.md` 먼저. paired라 **Before 결함 결과만 빨강**, 표 넷·판 기록은 노랑(출력), `setup()`·`PostgresSaver`는 라이브러리가 준 것이라 회색, 우리가 적은 노드·호출 줄은 파랑, 접속 정보·입력은 초록. 옛 `figures/02-흐름.*` 그대로.
10. **비유와 삽화**: 위 「비유 계열」 02 후보(빈 사진첩에 칸을 먼저 붙이기 ↔ 사진첩 없이 쌓인 사진 — 「선반」 금지). 01은 2차 채택(1차 개수 틀림) — 개수는 세기 쉬운 배열로.
11. **아직 가르치지 않은 것**(02가 설명 없이 전제하면 안 되는 것): `SqliteSaver`·파일 체크포인터(03) · 저장 시점 `durability`(04) · 강제 종료·자식 프로세스(04) · 남은 쓰기·`writes` 표 읽기(05 — 02는 `checkpoint_writes` 표 이름까지만) · 멱등(06) · 메시지 칸 저장(03) · 실패로 멈춘 실행의 체크포인트(05) · Store · Ch 24 `interrupt`·`update_state`. 01은 **체크포인트 ID·시각을 출력하지 않았음** — 02도 표 줄을 출력할 때 ID 칸(`checkpoint_id`)·시각은 빼고 수·이름만.
12. **02절 작업 순서와 챕터 밖 확인**: `before/`에 02 사본이 이미 있음 → `qa/upgrade/pre_exec.sh`(Ch 12 판 본) → `qa/upgrade/author_02.py`(01 판을 본으로 — `illustration_block()`·`html_text()`·`table_html()`·준비 셀 셋 그대로, paired라 `lesson_part` example/failure와 `{{notebook:slug|example}}`·`{{notebook:slug|failure}}` — Ch 21에는 paired가 없으니 Ch 20 03·Ch 22 paired 생성기를 볼 것) → 첫 실행 전 `upgrade_gates.py … --label wip-02 --section 02`(G1·G2) → `run_section.sh … 02`(A, 서버는 `pre_exec.sh`가 켬 — B 사본 실행 때도 같은 호출 안에서 서버를 켤 것) → 사본으로 B → 셀별 대조 → `.mmd`·삽화 → `--no-exec` 게이트 0 → AST·금지어 → `pack.py` → `02-diagnosis.md` → 이 파일 `§02 → §03` → 점검표·검증 행 → 보호 파일 해시(`manifest-changes.md`에 이어 적기). **뒤 챕터가 02에 기대는 문장**: Ch 31 05(대기) b3 「Ch23에서는 PostgresSaver의 `setup()`이 체크포인터 표를 만든다는 점을 확인했습니다」 — A로 실행하면 참(Ch 31 05 노트북은 Docker 55431로 다시 함, 고치지 않음). 슬러그 02는 링크 0. 실습 폴더 README의 Docker 명령(`postgres:17`·55432)은 마감 때 02 선택에 맞춰 다시 씀(02가 진단에 적을 것).

## §02 → §03

**03절 주제**: 「스레드 재개와 대화 이어가기」(**experiment**). 옛 판(`before/notebooks/03-…ipynb`·`before/_src/03-*.html`): `SqliteSaver` + 칸 `turns`(`operator.add`) · 경로 셀(`[Path.cwd(), *…parents]`·`next(…)`) · `with sqlite3.connect(…)` 블록 둘(둘째 블록에서 새 연결·새 그래프 객체) · 노드 `respond`가 `f"답변 {len(…)}"` · 출력 `database bytes: 4096` · `['질문 1', '답변 1', '질문 2', '답변 3']`.

1. **02절이 남긴 자리**: `_src` b8·노트북 정리 끝 「03절에서는 연결과 그래프 객체를 새로 만들어도, 같은 스레드의 대화를 이어 가는지 봅니다」 · b4 「비교와 경계」 「03절에서 쓸 SQLite 체크포인터는 필요할 때 표를 스스로 만든다고, 같은 판 소스가 적습니다」(`langgraph/checkpoint/sqlite/__init__.py` 122~128행 — 03이 `setup()`을 부르지 않고도 표가 생기는 것을 출력으로 보이면 더 단단해짐) · 01 b4 「프로그램 밖에 남기는 체크포인터는 02절과 03절에서」. **02는 새 연결·새 그래프 객체로 스레드를 이어 가는 장면을 하지 않았음** — 체크포인터 연결을 닫은 뒤 다른 연결로 표 줄 수만 셈(`customer-a` 6 그대로). 이어 가는 결정적 장면은 03 몫.
2. **SQLite 파일은 임시 폴더에**(챕터 결정 2): 준비 셀 셋은 01·02와 같은 모양(앞머리 `ch23-03-`), SQLite 파일(본 파일·`-wal`·`-shm`)을 **이 임시 폴더**에 씀. 이 작업 기기에서 연결 폴더(실습 폴더 `data/`) 안 SQLite 쓰기는 `sqlite3.OperationalError: disk I/O error`로 멈춤(준비 노트 §5-5 — 진단에만, 학생 본문은 「실습 폴더에 파일을 남기지 않으려고」). 옛 경로 셀·`Path.unlink`는 필요 없어짐. 02의 9절처럼 끝에 `os.listdir()`로 생긴 파일 이름을 볼 수 있음(임시 경로는 출력하지 않음).
3. **`with sqlite3.connect(…)`는 연결을 닫지 않음**(준비 노트 §5-5 확인 — 블록 뒤에도 `conn.execute("SELECT 1")`이 됨, 파이썬 `sqlite3`의 `with`는 확정·되돌리기만). 옛 판 「첫 with 블록에서 … 연결을 닫습니다」·복습 1은 틀림. 닫으려면 `conn.close()`(Ch 4 03·Ch 12 02·**Ch 23 02** 모양 — 02는 `connect` → `close`, `with` 0) 또는 `SqliteSaver.from_conn_string(경로)`(설치판 `contextlib.closing`으로 닫음 — 03이 행 번호 확인). **`with`(open 밖)를 실행하면 과정 두 번째**(첫째 Ch 21 04 `warnings.catch_warnings`) 〔마감 정정 2026-09-25, 검토 A-13: 과정의 첫째·둘째가 아님 — 앞선 선례는 Ch 2 05 `with open`(A 트랙)·Ch 2 09·11(B 트랙)·**Ch 10 02 `with pdfplumber.open`**(라이브러리 객체, 기본 경로)·Ch 10 04·09 `zipfile.ZipFile`·Ch 21 04 `warnings.catch_warnings`. 03 b3·9절 설명은 Ch 10 02로 고침〕 — 처음 쓰는 자리에서 한 문장. 02는 b7에 「공식 문서 예시 `with PostgresSaver.from_conn_string(…) as saver:` — 설치판 소스에서 블록이 끝나면 연결을 닫음(psycopg `connection.py` 155~176행), 노트북에서 실행 안 함」 한 줄만 둠.
4. **「4096바이트」는 틀린 값**: 옛 출력 `database bytes: 4096`은 `SqliteSaver.setup()`이 `PRAGMA journal_mode=WAL`을 켜서 내용이 `-wal` 파일(준비 확인 65,952바이트)에 있기 때문 — 닫은 뒤에야 본 파일이 20,480바이트. 파일 크기를 결론으로 쓰지 말 것. 파일 이름 목록(본 파일·`-wal`·`-shm`)은 새 커널 두 번에서 같은지 확인한 뒤에만.
5. **메시지 칸(M3, 챕터 결정 1)**: 상태 칸 `messages: Annotated[list[AnyMessage], add_messages]`(Ch 13 04·Ch 20 01), 입력은 `HumanMessage`, 「답」은 노드 함수가 만든 `AIMessage`(모델 글이 아님을 한 문장 — 가짜 모델 클래스가 아니라 노드 함수). 설치 셀에 `langchain-core==1.6.2`(잠금에 있음). 옛 f-string `f"답변 {len(…)}"` 금지 → 변수에 담고 `str()`·`+`. **Ch 22 09 b8 「이번 실습에서 종류별로 출력한 대화 기록이 그 대상입니다」가 참이 되려면 메시지 종류(`type(message).__name__`)를 출력**. Ch 19 06 `show_messages`(Ch 21 `runner_tools.py` 판)를 가져다 쓰면 03이 `notebooks/checkpoint_tools.py`를 처음 만들고 묶음 목록 둘에 더함(02는 만들지 않음 — 02 진단 §6). 01 `print_history`를 쓰는 절도 같은 규칙.
6. **새 연결에서 대화를 이어 가는 결정적 장면**: 준비 확인(글 목록 판) — 새 연결·새 그래프 객체로 같은 스레드 `['질문 1', '답변 1', '질문 2', '답변 3']`, 체크포인트 6·쓰기 6. 메시지 칸 판의 값은 03이 출력으로 정함. 대비: 01 11절(새 `InMemorySaver`는 `{}`) ↔ 03(새 연결·새 `SqliteSaver`·새 그래프 객체는 이어 감). 02가 쓴 말 「체크포인터 연결」·「조회 연결」을 이어 쓸 수 있음. 「답변 3」처럼 노드가 메시지 수로 글을 만들면 수가 튀는 까닭(메시지 칸 길이)을 결과 읽기에.
7. **표 구조 대비는 소스로만**: SQLite 체크포인터 표 둘(`checkpoints`·`writes` — 값을 체크포인트 칸 안에 담음, `sqlite_master`로 조회 가능 — Ch 4 03 `SELECT` 모양·자리표시자 `?`) ↔ PostgreSQL 넷(02 출력). 「02와 같은 표 구조」라고 쓰면 틀림 — `writes` ↔ `checkpoint_writes`는 이름이 다른 짝, 값 표·표 만들기 기록은 SQLite에 없음(준비 노트 §2 02). 02의 조회 함수 셋(`table_names`·`column_names`·`count_checkpoints`)은 PostgreSQL `information_schema`·이름 공간 `ch23_lab` 전용이라 03에서 그대로 못 씀.
8. **02에서 정한 말**(03이 이어 씀): **이름 공간**(SQL 낱말 `SCHEMA`) · **표 만들기**(`setup()`) · **표 만들기 기록**(표 `checkpoint_migrations`) · 판 번호 · 체크포인터 연결 / 조회 연결 · 표의 칸 · **줄**(표의 한 줄 — 「행」·「레코드」 대신). 제목의 「스키마」는 본문에서 「제목의 마지막 말은 … 표들의 구조」로만 가리킴(낱말 0), 「마이그레이션」은 속성 이름 `MIGRATIONS`에서 「Ch 21 04절의 「옮기기」와 같은 영어 낱말이지만 … 표를 만들고 고치는 문장의 차례」로 한 번 — **03은 둘 다 쓰지 않음**. 02 meta 「새 용어 3」.
9. **02 셀 모양·색**: 코드 셀 **28**(준비 셋), 비준비 셀 최대 9줄, 함수 본문 최대 8줄, 셀당 정의 하나, 모델 요청 0. Mermaid 4장(원본 폭 501·463·679·535), **빨강은 02-3 Before 두 상자만**(paired), 보라 0, 연결·접속 글 초록. 03은 experiment → 빨강 0, 받아 출력한 오류 노랑.
10. **비유**: 02 삽화 `02-5-속지를-끼운-사진첩과-빈-사진첩`(2차 job `21f990d2-…` 채택 — 왼쪽 빈 고리·사진첩 밖 사진 한 장 / 오른쪽 속지 한 장에 사진 여섯 장 두 장씩 세 줄 / 카메라 하나). 1차는 「속지 넷·사진 여섯」을 그리지 못함(사진 아홉·속지 수 셀 수 없음) → **겹친 종이·여러 장 속지처럼 셀 수 없는 배치는 피할 것**. 03 후보(준비: 다음 날 빈 판 옆 마지막 사진 한 장을 보고 말을 다시 놓음 — 새 연결·새 그래프 객체)는 물건 수를 작게. 금지 소품 목록 그대로(+ 사진첩은 02가 씀).
11. **작업 환경**: `qa/upgrade/pre_exec.sh`는 **`N=02`일 때만** PostgreSQL을 켬(03~06 `run_section.sh`에는 아무 일도 하지 않음). 02를 다시 실행할 때(마감)는 같은 호출 안에서 켜고 `trap EXIT`로 끔 · 127.0.0.1:55432에서 이미 받는 서버가 있으면 멈춤 · 클러스터 `/tmp/ch23-02/pgdata`(없으면 새로 만듦). Ch 12 `.cache/vm/pgdata`는 건드리지 않음. 새 커널 두 번은 01·02와 같은 방법(A `run_section.sh` · B 사본 `execute.py` + 환경 변수 넷, `/tmp/ch23-02/cmpout.py`).
12. **아직 가르치지 않은 것**(03이 설명 없이 전제하면 안 됨): 저장 시점 `durability`(04) · 강제 종료·자식 프로세스(04) · 남은 쓰기·쓰기 표 줄 읽기(05 — 02는 표 이름·「체크포인트에 딸린 쓰기」까지만) · 실패로 멈춘 실행(05) · 멱등(06) · Store · Ch 24 `interrupt`·`update_state` · 연결 묶음(`psycopg_pool`, 설치만 됨). **뒤 챕터**: Ch 30 02 b3 「Ch23의 체크포인터처럼 생성 비용과 수명주기가 다른 객체」 — 02는 객체 수명을 견주지 않음 → 03(연결·그래프 객체를 새로 만드는 장면)으로 참이 될 수 있음. Ch 27 04 b3 「체크포인터 메시지」 — 03 메시지 칸으로. Ch 31 05 b3(`setup()`이 표를 만든다) — **02로 참**. 실습 폴더 README의 옛 Docker 명령(`postgres:17`)은 02 노트북과 어긋난 채(마감 몫).

## §03 → §04

**04절 주제**: 「내구 실행 모드 비교」(**experiment**, 슬러그 고정 — Ch 20 02 b7이 「Ch 23 04절(강제 종료 뒤)」로 링크). 옛 판(`before/notebooks/04-…ipynb`·`before/_src/04-*.html`·실습 폴더 맨 위 `durability_worker.py`): 경로 셀(`[Path.cwd(), *…parents]`·`next(…)`) · `read_saved(db_path: Path, mode: str) -> dict | None`(조건 표현식·`with sqlite3.connect`) · `kill_and_resume(mode)`(17줄 — `Popen` → ready 파일 기다리기 `time.time()`·`time.sleep(0.02)` → `kill()` → `wait(timeout=5)` → `subprocess.run(…, "resume", check=True, timeout=20)`) · 내포식 `observations = [… for mode in …]` · `all(…)` · f-string 형식 지정 `{row['mode']:5}` · 파일은 실습 폴더 `data/durability/`.

1. **03절이 남긴 자리**: `_src` b8·노트북 정리 끝 「04절에서는 저장하는 때를 바꿔 가며, 프로그램을 강제로 끝낸 뒤 무엇이 남는지 봅니다」 · b4 「새로 시작한 프로그램에서 이어 가는 모습은 04절에서 봅니다」 · b7 「프로그램(커널)을 다시 시작해 이어 가 보지는 않았습니다」 → **04가 강제 종료 뒤 새 프로세스(worker `resume` 단계)에서 같은 SQLite 파일·같은 스레드로 이어 가는 장면을 출력으로 보여야 참**. 01 b3·b7 「멈춘 실행을 저장된 자리부터 이어 가는 일은 04절과 05절」·「저장 시점을 고르는 일은 04절」도 04 몫.
2. **강제 종료 장면 유지(챕터 리드 결정 4)**: `subprocess`로 worker를 실행하고 둘째 노드에서 끊기 → 모드마다 끊기 전 저장값·다시 실행한 뒤 값·노드 호출 기록. 예외(실패 흉내)로는 `exit`도 끝나며 저장해 차이가 안 보임(준비 노트 §7-2 (b), `_loop.py` 1324~1333행) — 강제 종료가 이 절의 까닭이라는 것을 한 문장으로. 실패 흉내 장면은 05 몫.
3. **worker 스크립트 자리와 임시 폴더 경로 넘기기(챕터 결정 2)**: 노트북은 준비 셀에서 임시 폴더로 `os.chdir()` → worker 파일 자리는 **옮기기 전에** 과정 모양 자리 찾기 셀(`candidates = [".", "../../..", "../../../.."]` + `for`·`break`, 옛 `[Path.cwd(), *…]`·`next(…)` 금지 — 인계 「준비 셀」 4) 또는 `notebooks/` 기준으로 정하고, **SQLite·ready·기록 파일 경로는 임시 폴더 안 이름으로 worker 인자에 넘김**(`sys.executable`로 부름). 준비 셀 차례: 설치 → 가져오기 → 자리 찾기 → 임시 폴더. 실습 폴더 `data/`는 만들지 않음. worker 파일(학생이 여는 모듈, 묶음 목록 두 곳에 실습 폴더 맨 위 경로로 있음)은 금지 문법(한 줄 다중 대입·조건 표현식 둘·반환 힌트·`from __future__`·영어 독스트링·`with sqlite3.connect` — **03에서 본 대로 이 `with`는 연결을 닫지 않음**)을 고칠지 04가 정하고, 자리·이름을 바꾸면 `textbook/part6/public-files.json`·챕터 `qa/public-files.json`을 함께. 출력에 **프로세스 번호·시각·임시 폴더 위치를 찍지 않음**(새 커널 두 번 대조).
4. **결론은 결정적 값만**: 준비 확인(60번) `exit` **20/20** 끊기 전 저장값 없음(`None`)·호출 `first, second, first, second` ↔ `sync` **20/20** 끊기 전 `['first']`·호출 `first, second, second`. 보조 장면(한 프로세스 안) 둘째 노드에서 센 체크포인트 수 **`exit` 0 · `sync` 3**(늘 같음 — 준비 노트 §7-2 (a)), 성공한 실행의 기록 수 `exit` 1 ↔ `sync` 4. 결론·그림 라벨·캡션·정리·복습에는 이 값만.
5. **async는 흔들림**(준비 확인 60번 중 **56 `['first']` / 4 잃음**, 보조 장면 체크포인트 수 2 또는 3) → 결과 읽기 **둘째 단락**과 b7에만 「이번 확인에서는」·「이번 실행에서는」으로, 60번 기록은 진단 b7. 새 커널 두 번에서 async 줄만 다르면 그 사실을 적고 둘째 단락 한정(규격 §2-7 9번 끝). 기본값이 `async`라는 것은 설치판 소스(`pregel/main.py` 2602~2603행)로 한 문장. 03이 기본값(`async`)으로 실행해도 매번 같았던 까닭 — 그래프는 저장을 뒤에서 도는 실행 흐름에 맡기고(`_loop.py` 1199~1202행 「save it, without blocking」) 실행이 끝날 때 맡긴 일을 모두 기다림(`_executor.py` 105~107행) — 은 03 b7에 있음. 04는 「끝나기 전에 강제로 끊으면 그 기다림이 없다」로 이을 수 있음(소스로 확인 후, `sync`는 매 단계 뒤 기다림 `main.py` 2987~2988행).
6. **걸린 시간 비교는 재료가 약함 → 주제로 삼지 않는 쪽**(준비 노트 §7-3: 로컬 SQLite 20노드 `exit` 약 0.005초 ↔ `async`·`sync` 약 0.023~0.025초, async·sync 차이 안 보임). 구조(「sync는 저장이 끝날 때까지 기다린다」)만 쓰고 「걸린 시간은 이번에 재지 않았습니다」. **옛 b2·b4·b5 「지연」 문장(「기다리는 시간이 늘어날 수 있습니다」·「지연을 줄일 수 있지만」·「지연 이점」)은 잰 적 없음** → 뺄 것(규격 §3). 공식 문서의 「best performance」·「highest durability」는 문서 문장으로만 인용 가능.
7. **처음 쓰는 이름 — 한 문장씩**: `subprocess.Popen`(과정은 Ch 2 `subprocess.run([sys.executable, …])`까지, `Popen`은 Ch 4 준비 셀 예외뿐 — 「끝나기를 기다리지 않고 자식 프로세스를 띄움」) · `.kill()` · `.wait(timeout=)` · `time.time()` 기한 루프(Ch 16 05는 `time.sleep`까지) · `sys.executable` · `try`/`finally`(쓰면 — Ch 2 B만). 새 말 **저장 시점**(`durability`, 「내구」 한자어는 제목에만)·**강제 종료**·**자식 프로세스**는 04가 세 문장으로 정의(인계 「용어」 후보).
8. **강제 종료 함수는 06·07이 되풀이**: 04는 **처음 가르친 절이라 노트북에 두되**, 노트북 전역 이름에 기대지 않게 **인자로만**(worker 자리·SQLite 경로·ready 경로·모드) 받고 **본문 8줄 이하 여러 함수로** 나눌 것(옛 17줄 → 띄우기·ready 기다리기·끊기·다시 실행 등). **06(또는 07)이 처음 가져오며 `notebooks/checkpoint_tools.py`를 만들고** `# Ch 23 04절에서 배웠습니다 — …`로 옮김(본문 글자·AST 같게, 묶음 목록 둘, 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 …」, `run_section.sh`가 `notebooks/`를 `PYTHONPATH`에 더함). `subprocess`·`sys`·`time` import는 그 파일에도. **03이 처음 가르친 함수** `print_conversation(messages)`(메시지 종류·글 — 07이 대화를 쓰면 후보) · `sqlite_tables(connection)`(`sqlite_master` 이름 차례 — 04·05가 SQLite 표를 보면 후보)도 같은 규칙.
9. **03에서 정한 이름·말(이어 쓰기)**: 새 말 **SQLite 체크포인터**(`SqliteSaver(연결)`) · **객체의 수명**(만든 때부터 닫혀 못 쓰게 된 때까지) · **스레드 재개(resume)**(객체를 새로 만든 뒤 같은 스레드 이름으로 마지막 체크포인트부터 이어 가기) — 04의 「프로세스가 끝나면 그 프로세스의 객체는 모두 사라지고 파일의 체크포인트만 남는다」에 그대로 씀. 연결은 `sqlite3.connect(파일, check_same_thread=False)` + `close()`, 또는 `with SqliteSaver.from_conn_string(파일) as 이름:`(03 9절에서 실행 — 블록이 끝나면 닫힘을 `ProgrammingError`로 확인, 설치판 `sqlite/__init__.py` 113~120행). `check_same_thread=False`를 빼면 그래프 실행 중 `ProgrammingError`(노트북 밖 5/5). 파일 목록은 `sorted(os.listdir())`를 변수에 담아 출력(**파일 크기는 WAL 때문에 결론에 쓰지 않음**, 연결을 모두 닫으면 `-wal`·`-shm`이 없어짐). 03 스레드 이름 `conversation-a`·`-b`, 04는 모드 이름을 스레드 이름으로 써도 됨(옛 판).
10. **03 셀 모양·색**: 코드 셀 **29**(준비 셋), 비준비 셀 최대 7줄, 함수 본문 최대 6줄, 셀당 정의 하나, 모델 요청 0. Mermaid 4장(원본 폭 311·256·791·578 — **셋을 가로로 둘 때 칸 제목이 길면 868을 넘음**, 03-3은 칸 제목을 줄이고 이름을 상자 안으로 옮겨 899 → 791), **빨강 0**(받아 출력한 `ProgrammingError`도 노랑), 보라 0. 04도 experiment → **빨강 0**(강제 종료로 잃은 값은 출력으로 확인한 값이라 노랑), async 흔들린 값은 그림에 넣지 않음.
11. **비유와 삽화**: 04 후보(인계 「비유 계열」) sync = 사진이 다 나온 뒤 다음 수 / async = 사진이 아직 하얗게 나오는 중에 다음 수 / exit = 판이 끝날 때만 한 장 + 엎어진 판 — **그림 라벨·캡션에 async 결과 값 금지**, 줄 셋처럼 물건이 많으면 줄마다 사진 수를 작게(03은 사진 한 장·말 넷·사진첩 하나·상자 하나로 1차 채택). 03이 쓴 소품: 닫힌 사진첩(= SQLite 파일)·빈 나무 상자(= 닫은 첫 객체)·판 앞 사진 한 장(= 마지막 체크포인트). 금지 소품 목록 그대로.
12. **아직 가르치지 않은 것**(04가 설명 없이 전제하면 안 됨): 남은 쓰기·표 `writes`의 줄 읽기(05 — 03은 표 이름까지만, 준비 확인 `writes` 6줄은 본문에 없음) · 실패로 멈춘 실행·`invoke(None, config)`로 다시 부르기(05 — 옛 worker의 `resume` 단계가 `None`을 넣으므로 04가 쓰면 한 문장, 05와 겹치지 않게) · 멱등(06) · Store · Ch 24 `interrupt`·`update_state` · 모델 답·도구 메시지 저장. **뒤 챕터**: Ch 20 02 b7 「04절(강제 종료 뒤)」 — 강제 종료 장면이 있어야 참 · Ch 31 02 b3 「중단 뒤 재개」(04~06) · Ch 30 02 b3 「체크포인터처럼 생성 비용과 수명주기가 다른 객체」 — **03으로 수명 쪽만 참, 생성 비용은 아무 절도 재지 않음**(04도 시간을 재지 않으면 그대로, 기록만). 작업 환경: 03은 기기 세션 임시 폴더(`$TMPDIR` = `/sessions/…/tmp`)에서 SQLite가 잘 됨, 새 커널 두 번은 01~03과 같은 방법(A `run_section.sh` · B 사본 `execute.py` + 환경 변수 넷, `/tmp/ch23-03/cmpout.py`·`texthash.py` — 설치 셀 stdout 조각 수 때문에 `outputs_sha256`은 달라질 수 있어 셀별 글자로 대조). worker가 30초 자므로 끊기에 실패하면 자식이 남음 — 셸 180초 안에서 모드마다 약 1.1초.


## §04 → §05

**05절 주제**: 「pending writes와 장애 복구」(**experiment**, 슬러그 고정 — Ch 20 02 b7이 「05절(실패한 단계)」로 링크). 옛 판(`before/notebooks/05-…ipynb`·`before/_src/05-*.html`): 경로 셀(`[Path.cwd(), *…parents]`·`next(…)` 둘) · 실습 폴더 `data/pending-trace.txt`·`data/allow-flaky`(`unlink`·`mkdir`) · 리듀서 **`lambda left, right: left + right`** · `record(name: str) -> None`·`good`·`flaky` 한 셀에 함수 셋(힌트) · `START`에서 `good`·`flaky` 두 갈래 → 같은 단계 · `flaky`가 허용 파일이 없으면 `raise RuntimeError("temporary failure")` · `except RuntimeError as exc` · `snapshot.tasks` 내포식 `[(task.name, bool(task.error), len(task.result or [])) …]` · 허용 파일을 쓰고 `graph.invoke(None, config)` → 호출 `['good', 'flaky', 'flaky']` · `sorted(resumed["results"])` · `InMemorySaver`.

1. **04절이 남긴 자리**: `_src` b8·노트북 정리 끝 「05절에서는 같은 단계의 두 노드 가운데 하나만 실패할 때(노트북: 실패했을 때, 성공한 노드의 쓰기가 남는지)를 봅니다」 · b4 「비교와 경계」 「05절은 강제 종료가 아니라 노드 안 오류로 멈춘 단계를 다룹니다. 설치판 소스에서 `exit`는 오류로 멈출 때도 나가면서 저장하므로, 이 절은 강제 종료로 차이를 보았습니다」 · b7 「설치판 소스 `_loop.py` 1324~1333행에서 `exit`는 노드 안 오류로 멈출 때도 나가면서 체크포인트를 씁니다. 오류로 멈추는 장면은 이 절에서 실행하지 않았고, 05절에서 봅니다」·「다시 실행 단계의 `invoke(None, config)`는 … 스크립트 안에서만 썼고, 노트북 셀에서 부르지는 않았습니다」 → **05가 노트북 셀에서 `invoke(None, config)`를 처음 부르고**(04 4절 설명 셀 「입력 자리에 `None`을 넣으면 새 입력 없이 마지막 체크포인트부터 이어 갑니다」를 「04절 스크립트처럼」으로 이음), 실패 흉내로 멈춘 단계를 이어 가야 위 문장들이 참. `exit`를 함께 실행하면 「오류로 멈출 때도 나가며 저장」이 출력으로 참이 됨(준비 노트 §5-3 — 세 값 모두 재개 뒤 `good` 1·`flaky` 2). Ch 20 02 b7 「05절(실패한 단계)」 — **실패 원인을 없앤 뒤 이어 가는 장면**이 있어야 참.
2. **결정적 값과 흔들리는 값(준비 노트 §5-3·§7-5)**: 결정적 — 호출 **수**(`good` 1·`flaky` 2), 결과 목록(`sorted` 뒤 `['flaky-result', 'good-result']`), 실패 뒤 `next` `('flaky',)`, `tasks`의 이름·오류 여부·`good`의 `result` `{'results': ['good-result']}`, **SQLite `writes` 표의 칸 `channel` 값**(`exit`: `__error__`·`results` / `async`·`sync`: `branch:to:flaky`·`branch:to:good` 줄이 더 있음), `checkpoints` 줄 수(`exit` 1 ↔ `async`·`sync` 2). 흔들림·무작위 — **호출 차례**(준비 확인 `['flaky', 'good']` ↔ 옛 출력 `['good', 'flaky']`), `task_id`·체크포인트 ID. → 차례는 출력하지 않거나(`count`로 수만) 출력하면 결과 읽기 둘째 단락·「이번 실행에서는」. 흔들림을 따로 확인하면 **`05-probe.md`에 규칙을 먼저**(04 판 모양 — 무엇·몇 번·판정·환경을 실행 전에). 새 커널 두 번은 04와 같은 방법(A `run_section.sh` · B 사본 `execute.py` + 환경 변수 넷, `/tmp/ch23-04/cmpout.py`·`texthash.py` 복사).
3. **리듀서·상태 형식**: `lambda` 리듀서 → **`operator.add`(Ch 13 02 모양, 04 `StepState`와 같은 칸 규칙)**. 칸 이름이 `results`면 04 `StepState`(칸 `completed`)와 달라 새 이름(Ch 13 약속 — 예: `ResultState`). 같은 칸에 두 노드가 한꺼번에 쓰는 장면은 **Ch 13 05**(팬아웃·한꺼번에 낸 갱신·규칙 없으면 `InvalidUpdateError`)가 가르침 → 「같은 단계」·「팬아웃」으로 이어 쓰고, 규칙이 있어 두 갱신이 목록에 함께 붙는다는 것을 한 문장. 노드·도움 함수 힌트 0, 셀당 정의 하나(옛 c6 함수 셋 → 셀 셋).
4. **실패 흉내(Ch 16 05)**: 옛 `RuntimeError("temporary failure")`·허용 파일 대신 Ch 16 05 모양(`raise TimeoutError("이 절에서 만든 실패 흉내입니다.")`·`except TimeoutError as error` — 과정 요약 §2-8)으로 이름을 잇는 쪽을 권함. 실패를 끄는 스위치는 (가) 임시 폴더의 파일(04 신호 파일처럼 `os.path.exists` — 노드가 전역 값에 기대지 않음) 또는 (나) Ch 16 05 `failure_plan` 딕셔너리(노드가 노트북 전역을 읽음) 가운데 05가 정할 것. **받아 출력한 오류는 노랑**(experiment, 규격 §5-3 — 다음 셀에서 고쳐도 노랑). 「남은 쓰기」 장면: 같은 단계의 `good`이 성공해 쓴 갱신이 체크포인트에 딸린 쓰기로 남아, 재개할 때 `good`을 **다시 실행하지 않음**(호출 수 1) — 공식 문서 Checkpointers 「you don't re-run the successful nodes」(준비 노트 §5-3). 04 기록 파일 모양(`with open(이름, "a")`로 노드 이름 한 줄 — worker `write_record`)을 노트북에 쓰면 이름 수를 셀 수 있음.
5. **금지어**(인계 「용어」 표 그대로 + 05 특히): 「superstep」·「super-step」 → **단계**(Ch 20 03) · 「병렬」 → **같은 단계·함께 실행·팬아웃**(Ch 13 05) · 「채널」 → 칸(코드 칸 이름 `channel`은 백틱 안에서만, 풀이는 「칸 `channel`에 적힌 칸 이름」) · 「런타임」·「트랜잭션」·「원자적」·「로그」(→ 기록)·「반환」·「경로」·「지연」·「보장」·「정확히 한 번」·「측정」·「검증」 · 「pending writes」·「pending write」는 제목에만, 본문은 새 말 **남은 쓰기**(뜻 → 비유 → 코드 세 문장, 인계 「용어」 후보). 「재시작」은 06 제목 말 — 05 본문은 「다시 실행」.
6. **임시 폴더(챕터 결정 2)**: 준비 셀은 01 판 폴더 셀 앞머리만 `ch23-05-`(생성기 `assert` — 04 `author_04.py` 끝 모양). `SqliteSaver`를 쓰면 03·04 모양(`sqlite3.connect(이름, check_same_thread=False)` → `SqliteSaver(연결)` → 끝에 `close()`), `writes` 표 조회는 03 `sqlite_tables`(`sqlite_master`)·Ch 4 03 `SELECT … WHERE thread_id = ? ORDER BY …` 모양(자리표시자 `?`), 파일 이름 목록은 `sorted(os.listdir())`를 변수에 담아 출력. 실습 폴더 `data/` 만들지 않음. `InMemorySaver`로 두면 파일은 0이지만 `writes` 표를 SQL로 볼 수 없음(준비 노트 §5-3은 SQLite 판을 권함).
7. **04에서 정한 말(이어 쓰기)**: 새 말 **저장 시점(durability)**(그래프가 체크포인트 저장을 언제 끝내는지 정하는 값 — `exit`·`async`·`sync`, 기본값 `async`, 「내구」는 제목에만) · **자식 프로세스** · **강제 종료** · **신호 파일**. 일반 말: 첫 실행 단계·다시 실행 단계(worker `first-run`·`resume`) · 기록 파일 · 끊다·끊긴 뒤 · 끝까지 실행. 04 결론(결정적): 끝까지 실행 체크포인트 `exit` 1 · `async` 4 · `sync` 4(노드 둘 — 입력을 받은 때·입력을 칸에 넣은 뒤·노드마다 마친 뒤) · 둘째 노드에서 강제 종료 뒤 `exit` `{}`·`()`·0 ↔ `sync` `{'completed': ['first']}`·`('second',)`·3 · 다시 실행 기록 `first, second, first, second` ↔ `first, second, second` · 되풀이 다섯 번 0 ↔ 5. **`async` 강제 종료는 흔들림**(교재 출력 4/5, B 5/5, 준비 확인 60 중 4 잃음·고친 worker 40/40 남음) — 05가 인용하면 「04절 준비 확인에서는」·둘째 단락만.
8. **강제 종료 함수(04가 처음 가르침 — 노트북에 있음, `checkpoint_tools.py`는 아직 없음)**: 06·07이 처음 가져올 때 `labs/part6/ch23-persistence/notebooks/checkpoint_tools.py`를 만들고 `# Ch 23 04절에서 배웠습니다 — …` 주석으로 **아래 본문을 글자·AST 그대로** 옮김(생성기에서 `author_04.DEF_*`와 문자열 대조 — Ch 21 `check_same_as_before()` 모양). 파일 맨 위 import는 `os`·`sqlite3`·`subprocess`·`sys`·`time` + `from langgraph.checkpoint.sqlite import SqliteSaver`(`read_saved`가 씀). 묶음 목록 둘(`textbook/part6/public-files.json` 26~36행 근처 · 챕터 `qa/public-files.json`)에 더하고, 처음 가져오는 절에 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다」(`run_section.sh`가 `notebooks/`를 `PYTHONPATH`에 더함), 가져오기는 **임시 폴더로 옮기기 전** 준비 셀에서 알파벳 순. 05가 이 함수들을 쓰지 않으면 만들지 않음(쓰면 05가 처음 가져오는 절).

```python
# 스크립트를 자식 프로세스로 띄우고, 끝나기를 기다리지 않고 그 프로세스 객체를 내놓습니다
def start_worker(worker_path, files, mode, phase):
    # 명령 목록: 지금 커널의 Python · 스크립트 자리 · 스크립트가 받을 글 다섯
    command = [sys.executable, worker_path, files["sqlite"], files["signal"], files["record"], mode, phase]
    process = subprocess.Popen(command)
    return process

# 신호 파일이 생길 때까지 짧게 쉬며 보고, 기한 안에 생겼는지를 True·False로 내놓습니다
def wait_for_signal(signal_name, limit_seconds):
    check_interval = 0.05
    deadline = time.perf_counter() + limit_seconds
    while time.perf_counter() < deadline:
        if os.path.exists(signal_name):
            return True
        time.sleep(check_interval)
    return False

# 자식 프로세스를 강제로 끝내고, 끝날 때까지 기다려 종료 코드를 내놓습니다
def stop_worker(process):
    process.kill()
    # 5초 안에 끝나지 않으면 오류가 납니다
    return_code = process.wait(timeout=5)
    return return_code

# 새 연결로 SQLite 파일을 열어 한 스레드의 칸 값·다음 노드·체크포인트 수를 읽고, 연결을 닫습니다
def read_saved(graph_builder, sqlite_name, thread_name):
    connection = sqlite3.connect(sqlite_name, check_same_thread=False)
    saver = SqliteSaver(connection)
    reader = graph_builder.compile(checkpointer=saver)
    config = {"configurable": {"thread_id": thread_name}}
    saved = reader.get_state(config)
    history = list(reader.get_state_history(config))
    connection.close()
    return {"칸 값": saved.values, "다음 노드": saved.next, "체크포인트 수": len(history)}

# 기록 파일을 읽어, 줄마다 적힌 노드 이름을 목록으로 내놓습니다
def read_record(record_name):
    with open(record_name, encoding="utf-8") as record_file:
        text = record_file.read()
    return text.split()

# 스크립트를 띄워 둘째 노드에서 강제로 끝내고, 끊긴 뒤 파일에 남은 것을 읽어 내놓습니다
def kill_at_second(worker_path, graph_builder, name_prefix, mode):
    files = {"sqlite": name_prefix + ".sqlite", "signal": name_prefix + ".signal",
             "record": name_prefix + ".record"}
    process = start_worker(worker_path, files, mode, "first-run")
    signal_limit = 20
    arrived = wait_for_signal(files["signal"], signal_limit)
    # 신호를 기다린 결과와 상관없이 먼저 끊어, 자식 프로세스가 남지 않게 합니다
    stop_worker(process)
    assert arrived, "기한 안에 신호 파일이 생기지 않았습니다"
    return read_saved(graph_builder, files["sqlite"], mode)
```

   - 인자: `worker_path`(자리 찾기 셀의 절대 자리 — `os.path.abspath`) · `files`(키 `"sqlite"`·`"signal"`·`"record"`, 값은 임시 폴더 안 파일 이름) · `mode`(`"exit"`·`"async"`·`"sync"`, 스레드 이름으로도 씀) · `phase`(`"first-run"`·`"resume"`) · `graph_builder`(worker와 노드 이름·칸이 같은 설계 객체). `read_saved`는 `{"칸 값", "다음 노드", "체크포인트 수"}` 딕셔너리, `stop_worker`는 종료 코드(Linux `-9`).
   - 06(`idempotency_worker.py`, 옛 `interrupt_then_resume` 17줄 — 이름에 Ch 24 `interrupt` 금지)은 이 함수들로 쓸 수 있게 worker 인자 모양을 04와 맞추면 좋음(인자 다섯·`first-run`/`resume`·신호 파일). 06 worker는 04가 건드리지 않음(금지 문법 그대로 — 06 몫).
9. **worker 스크립트(04가 다시 씀)**: `labs/part6/ch23-persistence/durability_worker.py` `c60467bd…` — 인자 다섯(SQLite·신호·기록 파일 이름, 저장 시점, 단계), 상태 형식 `StepState`(칸 `completed`, `operator.add`), 노드 `first`·`second`(기록 파일 `"a"`로 이름 한 줄, 둘째 노드는 신호 파일을 만들고 `first-run`에서만 30초 쉼), 연결 `connect(…, check_same_thread=False)` + `close()`, 다시 실행 단계는 `get_state(config).next`가 있으면 `invoke(None, config, durability=mode)`, 없으면 처음 입력. 금지 문법 0·한국어 주석. 생성기 `author_04.py`의 `WORKER` 글이 이 파일을 씀(`--src-only`는 건드리지 않음). **`part6-practice.zip` 안 worker·04 노트북은 옛 판** — 마감에서 짝으로 다시 묶을 것.
10. **04 셀 모양·색**: 코드 셀 **28**(준비 넷 — 설치·가져오기·자리 찾기·임시 폴더), 비준비 셀 최대 9줄, 함수 본문 최대 8줄, 셀당 정의 하나, 모델 요청 0, 검사 문장 372(〔마감 정정, 검토 B-6: `gates-wip-04.json`은 373〕). Mermaid 4장(원본 폭 836·274·478·547 — **칸 셋을 가로로 두면 라벨이 길 때 868을 넘음**, 04-1 첫 렌더 934 → 라벨을 `<br>`로 한 줄 더 나눠 836), **빨강 0**(강제 종료·잃은 체크포인트도 출력으로 본 값이라 노랑), 보라 0, 초록 0. 갈래는 점선 + 라벨(04-3), 칸 안 나란한 상자는 `~~~`(04-4). 05도 experiment → 빨강 0, 받아 출력한 오류 노랑.
11. **비유와 삽화**: 04 삽화 `04-5-엎어진-두-판과-남은-사진`(1차 job `ec7db33b-…` 채택 — 나무 탁자 둘·쓰러진 판 둘·왼쪽 판 앞 사진 셋 한 줄·오른쪽 사진 없음·탁자마다 카메라 하나, 2크레딧). 05 후보(인계 「비유 계열」): **나란한 두 판 중 한 판만 쓰러지고, 다른 판의 마지막 사진은 남음**(남은 쓰기) — 04가 「탁자 둘·쓰러진 판」을 썼으니 구도를 바꿀 것(예: 한 탁자 위 판 둘, 한 판만 쓰러짐, 서 있는 판 앞 사진 한 장). 물건 수 작게, 사진첩(02·03)·카메라 둘(04) 되풀이는 피하는 쪽. 금지 소품 목록 그대로.
12. **아직 가르치지 않은 것**(05가 설명 없이 전제하면 안 됨): 노트북 셀의 `invoke(None, config)`(05가 처음 — 04는 스크립트 안에서만) · `snapshot.tasks`·`PregelTask`(칸 `name`·`error`·`result` — 설치판 `types.py` 637~646행) · `writes` 표 줄 읽기(03은 표 이름까지만) · 실패 흉내로 멈춘 실행의 체크포인트(준비 확인: 실패한 스레드도 체크포인트가 남고 `next` `('flaky',)`) · 멱등·멱등 키(06) · Store · Ch 24 `interrupt`·`Command(resume=)`·`update_state`. **뒤 챕터**: Ch 20 02 b7 「05절(실패한 단계)」 — 실패 뒤 원인을 없애고 이어 가는 장면이 있어야 참 · Ch 31 02 b3 「중단 뒤 재개와 멱등성」(04~06) · Ch 24 01 b3 「노드는 장애 뒤 처음부터 재시작될 수 있고」(06). **작업 환경**: 04는 자식 프로세스가 남지 않았는지 `ps -eo pid,args | awk '$2 ~ /python/ && /durability_worker/'`로 봄(`pgrep -f`는 셸 명령 자체가 걸려 거짓 양성). 기기 세션 임시 폴더(`$TMPDIR`)에서 SQLite·자식 프로세스 모두 잘 됨.

## §05 → §06

**06절 주제**: 「노드 재시작과 멱등성」(**paired**, 본문 마지막 절 — 07 실습 절은 챕터 끝에 따로). 슬러그 고정(Ch 20 02 b7 「같은 쓰기를 한 번만 반영하는 방법은 Ch 23 06절」). 옛 판(`before/notebooks/06-…ipynb`·`before/_src/06-*.html`·실습 폴더 맨 위 `idempotency_worker.py` `f668aa02…`): 경로 셀(`[Path.cwd(), *…parents]`·`next(…)`) · 실습 폴더 `data/idempotency/{전략}.{sqlite,log,ready}` · `interrupt_then_resume(strategy: str) -> list[str]` **17줄**(f-string·`unlink`·`time.time()` 기한 루프·`Popen`·`kill`·`wait`·`subprocess.run(…, check=True, capture_output=True, text=True, timeout=20)`) · worker: `from __future__`·한 줄 다중 대입 다섯·조건 표현식(`existing = … if … else []`·`graph_input = … if … else None`)·힌트·`with sqlite3.connect`(닫지 않음)·영어 독스트링·노드 `charge`가 로그에 `order-2306`을 쓰고 ready를 쓴 뒤 `first`에서 30초·`durability="sync"` · Before `naive` 2줄 / After `idempotent` 1줄(`assert` 둘).

1. **05절이 남긴 자리**: `_src` b8·노트북 정리 끝 「06절에서는 다시 실행된 노드가 체크포인트 밖에 한 쓰기를, 한 번만 반영하는 방법을 봅니다」 · b4 「비교와 경계」 「다시 실행한 노드가 체크포인트 밖에 쓴 것은, 다시 실행한 만큼 되풀이됩니다. 같은 쓰기를 한 번만 반영하는 방법은 06절에서 봅니다」 · b4 「다른 상황에 적용」 「남은 쓰기는 칸에 낸 갱신만 담습니다 … 다시 실행한 `flaky`의 횟수는 그대로 늘었습니다」 · b7 「노드가 파일이나 다른 서비스에 쓰는 일도 같고, 06절에서 봅니다」 → **06이 노드의 바깥 쓰기(기록 파일 한 줄)가 다시 실행으로 두 번 남는 장면(Before)과, 이미 적힌 키를 건너뛰어 한 번만 남는 장면(After)을 출력으로** 보여야 참. 04 b4 「기록 파일에는 `sync`에서도 `second`가 두 번 적혔습니다 … 06절에서 봅니다」도 같은 장면.
2. **결정적 장면 두 가지(챕터 리드 결정 — 둘 다 결정적)**: (가) **강제 종료**(04 방식 — 준비 확인 옛 worker 20번: `naive` 10/10 두 줄 · `idempotent` 10/10 한 줄, 준비 노트 §7-4) · (나) **실패 흉내**(05 방식 — 노드가 기록 파일에 쓴 뒤 `raise`, `invoke(None, config)`로 이어 감 → naive 두 줄 · idempotent 한 줄, 실패 뒤 `next` `('charge',)`, 준비 노트 §7-4 `/tmp/ch23-prep/exp/idem_exc.py`). 과제 결정은 **「강제 종료 20번과 실패 흉내 모두 결정적」** — 06이 한 장면만 쓰든 둘 다 쓰든, 결론·그림 라벨에는 새 커널 두 번과 노트북 밖 확인에서 같았던 값만. 강제 종료를 쓰면 **06 worker를 고친 판으로 20번**(전략마다 10번 이상) 노트북 밖에서 먼저 확인하고 `06-probe.md`에 규칙을 먼저 적을 것(04·05 판 모양). 실패 흉내를 쓰면 05처럼 실패 앞에 짧게 쉬어 차례 틈을 없앨지 판단(05 판 C: 쓰기를 마친 노드가 실패보다 늦게 끝나면 `exit`는 그 쓰기를 남기지 않음 — 06은 노드 하나라 해당 없을 가능성이 큼, 확인해서 적을 것).
3. **Before/After(paired)와 색**: Before = 검사 없이 기록 파일에 덧붙이는 노드(naive) → 같은 키 **두 줄**(실제 결함, 결정적) · After = 기록 파일에 이미 있는 키면 건너뛰는 노드(idempotent, 멱등 키 `order-2306` 등) → **한 줄**. **Before 결함 결과만 빨강**(paired 규격 §5-3), After 결과·출력 노랑, 우리 코드 파랑, 라이브러리·공통 사실 회색, 보라 0. `lesson_part` example/failure와 `{{notebook:slug|example}}`·`{{notebook:slug|failure}}`(02 `author_02.py`·Ch 22 paired 생성기 모양, `write_notebook()`이 경계를 나눔).
4. **함수 이름에 Ch 24 API 이름 `interrupt`를 쓰지 않기**(챕터 공통 결정 10): 옛 `interrupt_then_resume` → 예: `kill_then_resume`·`fail_then_resume`. b7 「interrupt 승인과 보상 작업」 같은 Ch 24 말도 앞당기지 않음(`interrupt`·`Command(resume=)`·`update_state`·타임 트래블 0). 「재시작」은 06 제목 말 — 본문은 「다시 실행」과 짝지어 한 번 풀 것(05는 금지어 목록에 「재시작」을 두고 0건).
5. **강제 종료 함수를 `checkpoint_tools.py`로(04 인계 8항 — 05는 만들지 않음)**: 06이 04 함수를 쓰면 **06이 처음 가져오는 절**이라 `labs/part6/ch23-persistence/notebooks/checkpoint_tools.py`를 새로 만들고, `# Ch 23 04절에서 배웠습니다 — …` 주석으로 `author_04.DEF_START`·`DEF_WAIT`·`DEF_STOP`·`DEF_READ`·`DEF_RECORD`·`DEF_KILL` 본문을 **글자·AST 그대로** 옮김(생성기에서 `author_04`를 import해 문자열 대조 — Ch 21 `check_same_as_before()` 모양). 파일 맨 위 import `os`·`sqlite3`·`subprocess`·`sys`·`time` + `from langgraph.checkpoint.sqlite import SqliteSaver`. 04 노트북은 함수를 셀에 적어 둔 채 그대로(다시 실행 안 함). 묶음 목록 둘(`textbook/part6/public-files.json` 27~34행 — worker 둘·노트북 여섯 사이 · 챕터 `qa/public-files.json`)에 더하고, 06 준비 셀에서 **임시 폴더로 옮기기 전** 알파벳 순 가져오기 + 고정 세 문장(과정 요약 §3 — 「앞에서 배운 함수는 `checkpoint_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.」, 규격 §2-7 5번) + 「커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다」(`run_section.sh`가 `notebooks/`를 `PYTHONPATH`에 더함). **`kill_at_second`·`start_worker`는 worker 인자가 04 모양(SQLite·신호·기록 파일 이름, 모드, `first-run`/`resume`)이라** 06 worker를 이 모양에 맞추면 그대로 쓸 수 있음 — 인자 모양이 다르면 처음 가져오는 절에서 한 문장으로 알림(§2-7 4번). 05가 처음 가르친 `saved_channels(connection, thread_name, task_id)`(표 `writes`의 작업별 칸 이름)는 06이 쓰면 같은 파일로 옮길 후보.
6. **임시 폴더(챕터 결정 2)**: 준비 셀 차례 설치 → 가져오기(도구 파일 포함) → (자리 찾기 — worker를 쓰면 04 `LOCATE` 모양, `idempotency_worker.py` 자리) → 임시 폴더(01 셀 앞머리만 `ch23-06-`, 생성기 `assert`). worker에 넘기는 SQLite·신호·기록 파일은 모두 임시 폴더 안 이름. 실습 폴더 `data/` 만들지 않음. 출력에 프로세스 번호·시각·임시 위치를 찍지 않음. 자식 프로세스가 남았는지는 `ps -eo pid,args | awk '$2 ~ /python/ && /idempotency_worker/'`(`pgrep -f`는 거짓 양성).
7. **06 worker(06 몫 — 04·05는 건드리지 않음)**: 금지 문법(위)을 고치고 한국어 주석으로 다시 쓸지 06이 정함(04가 `durability_worker.py`를 `author_04.WORKER` 글로 다시 쓴 선례, 묶음 목록에는 이미 실습 폴더 맨 위 경로로 있음). `with sqlite3.connect`는 연결을 닫지 않음(03) → `connect(…, check_same_thread=False)` + `close()`. 다시 실행 단계는 04 worker처럼 **저장된 다음 노드가 있으면 `invoke(None, …)`**. 옛 판 `durability="sync"` 유지 여부와 까닭(강제 종료 뒤 노드 앞 체크포인트가 남아야 `charge`부터 이어 감 — 04 결론)을 한 문장.
8. **05에서 정한 말(이어 쓰기)**: 새 말 **남은 쓰기**(같은 단계에서 먼저 끝난 노드가 낸 갱신 가운데, 단계가 끝나지 못해 칸 값에 합쳐지지 않은 채 체크포인트에 딸려 저장된 것 — 「pending writes」는 05 제목에만) · **작업(task)**(한 단계에서 노드 하나를 한 번 실행하는 일, `tasks`의 항목 — 칸 `name`·`error`·`result`) · **장애 복구**(멈춘 실행의 원인을 없앤 뒤 저장된 자리부터 이어 가 끝내는 일). 일반 말: 실패 흉내(Ch 16 05 — `TimeoutError("이 절에서 만든 실패 흉내입니다.")`·`failure_plan`) · 부른 횟수 · 원인을 없앰 · 이어 가다 · 같은 단계에서 함께 실행 · 팬아웃(Ch 13 05) · 표 `writes`의 칸 `task_id`·`channel` · `__error__`(라이브러리가 받은 오류를 적어 두는 이름). 06 새 말 후보: **멱등성**(뜻 → 일상 예 → 코드 세 문장) · **멱등 키**. 「원자적」·「트랜잭션」·「정확히 한 번」·「보장」은 금지어(인계 「용어」).
9. **05 결론(결정적 — 06이 인용할 수 있는 값)**: 같은 단계에서 `flaky`만 실패 → 부른 횟수 `{'good': 1, 'flaky': 1}` · `칸 값: {'results': ['good-result']}` · `다음 노드: ('flaky',)` · 체크포인트 기본값 2 / `exit` 1 · 표 `writes` `good | ['results']`·`flaky | ['__error__']` → 원인을 없애고 `invoke(None, config)` → `{'good': 1, 'flaky': 2}`·`['flaky-result', 'good-result']`(정렬)·`다음 노드: ()`·체크포인트 기본값 3 / `exit` 2. **노트북 밖(05-probe.md)**: 원인을 두고 이어 가면 같은 `TimeoutError`(20/20, `good` 여전히 1) · `good`이 실패보다 늦게 끝나면 `exit`는 그 쓰기를 남기지 않음(10/10). **05는 노트북 셀에서 `invoke(None, config)`를 처음 부른 절** — 06은 「05절처럼」으로 이음.
10. **05 셀 모양·색**: 코드 셀 **21**(준비 셋), 비준비 셀 최대 9줄, 함수 본문 최대 6줄, 셀당 정의 하나, 모델 요청 0, 검사 문장 301. Mermaid 4장(원본 폭 496·244·428·601 — 칸 안 두 노드를 `~~~`로 이으면 `TB`에서 비스듬히 놓여 뺌), **빨강 0**(받은 `TimeoutError`도 노랑), 보라 0, 초록 0. 06은 paired → **Before 결함 결과(같은 키 두 줄)만 빨강**.
11. **비유와 삽화**: 05 삽화 `05-5-쓰러진-판과-사진이-남은-판`(1차 job `c7b590e1-…` 채택 — 한 탁자·판 둘 나란히·왼쪽 반듯하고 앞에 사진 한 장·오른쪽 쓰러짐·사진 없음·카메라 없음, 2크레딧). 06 후보(인계 「비유 계열」): **같은 수를 두 번 적은 기보 ↔ 이미 적힌 수는 건너뜀**(멱등) — 04·05가 판·사진·카메라를 썼으니 기보(종이 한 장, 줄 둘 ↔ 줄 하나)처럼 셀 수 있는 물건으로, **글자·숫자 없이** 「같은 표시가 두 번」을 보이게(예: 같은 모양 말 스티커 둘 ↔ 하나). 금지 소품 목록 그대로 + 사진첩(02·03).
12. **아직 가르치지 않은 것·뒤 챕터**: Store · Ch 24 `interrupt`·`Command(resume=)`·`update_state`·타임 트래블 · 모델 답·도구 메시지 저장 · 외부 서비스 결제 API(06은 기록 파일로 흉내만 — 「실제 결제 서비스는 실행하지 않았습니다」). **뒤 챕터**: Ch 24 01 b3(대기) 「Ch23에서 노드는 장애 뒤 처음부터 재시작될 수 있고 외부 쓰기에는 멱등성이 필요하다는 점을 확인했습니다」 — **06 몫**(05는 앞 반쪽만 뒷받침: 실패한 노드는 이어 갈 때 처음부터 다시 실행) · Ch 31 02 b3 「중단 뒤 재개와 멱등성」 — 멱등성 06 몫 · Ch 20 02 b7 「같은 쓰기를 한 번만 반영하는 방법은 Ch 23 06절」 — 06 몫. 작업 환경: 01~05와 같은 새 커널 두 번(A `run_section.sh` · B 사본 `execute.py` + 환경 변수 넷, `/tmp/ch23-05/cmpout.py`·`texthash.py` 복사). 05 노트북·`_src`는 06이 건드리지 않음.

## §06 → 실습(07)

**07절 주제**: 챕터 끝 실습 절 신설(규격 §7-2 · PLAYBOOK §3 — 슬러그 후보 **`07-Persistence-실습`**(선례 `09-Middleware-실습`·`07-create-agent-실습`·`05-ToolNode-실습`·`08-LangGraph-실습`·`06-Agent-개요-실습` — 챕터 제목의 앞말, 준비 노트 §13), 제목 「Persistence 실습: {주제}」, `chapter.json`에 `format: experiment`로 추가, meta 「실습 30분 · 새 용어 0」, **챕터 시수(6·10h)에 더하지 않음**). **06이 본문 마지막 절**이었습니다. 01~06의 이름·API만 쓰고 새 문법·새 API·새 말 0.

1. **06절이 남긴 자리(07이 생겨야 참)**: `_src` b8 「다음 학습과 이어지는 지점 — 07절 실습에서는 이 챕터에서 배운 것을 작은 흐름 하나에 모아 실행합니다.」 · 노트북 정리 끝 같은 문장(**링크 없음** — 07 파일이 아직 없음, Ch 21 06 선례). 07이 「이 챕터에서 배운 것(체크포인터·스레드·SQLite 파일·저장 시점·이어 가기·멱등 키 가운데 2~3개)을 한 흐름에」 모으면 그대로 참. 07이 생기면 06 b8에 `<a href="07-Persistence-실습.html">`을 넣을지 그때 정함(`author_06.py`의 `_src` 문장 → `--src-only` → `run_section.sh … 06 --no-exec`, 노트북 문장은 `mdpatch.py`로만 — 06은 다시 실행하지 않아도 됨). 06 b7이 남긴 「실행하지 않음」: 여러 프로그램이 한 기록 파일을 함께 쓰기 · 저장 시점 `exit`로 끊기 · 기록을 적기 전에 끊기 · 노트북에서 실패 흉내로 멈추기(노트북 밖 판 B만) · 실제 결제 서비스 — 07이 새로 풀면 새 설계가 되므로 **다루지 않는 쪽**을 권합니다.

2. **이어 쓸 이름 — 도구 파일 `labs/part6/ch23-persistence/notebooks/checkpoint_tools.py`(06이 만듦, `71280dd9fdd748bb9ae98388990a7ed0d33d07e3fb1246abfba95c64c4437c29`, import `os`·`sqlite3`·`subprocess`·`sys`·`time` + `from langgraph.checkpoint.sqlite import SqliteSaver`, 묶음 목록 둘에 올림)**:

   | 함수(인자) | 배운 곳 | 06에서 | 하는 일 |
   |---|---|---|---|
   | `start_worker(worker_path, files, mode, phase)` | 04 노트북 3절 | 가져옴 | `subprocess.Popen([sys.executable, worker_path, files["sqlite"], files["signal"], files["record"], mode, phase])` → 프로세스 객체 |
   | `wait_for_signal(signal_name, limit_seconds)` | 04 노트북 3절 | (`kill_at_second` 안) | 신호 파일을 0.05초 간격으로 기다려 `True`/`False` |
   | `stop_worker(process)` | 04 노트북 3절 | (`kill_at_second` 안) | `kill()` → `wait(timeout=5)` → 종료 코드(Linux `-9`) |
   | `read_saved(graph_builder, sqlite_name, thread_name)` | 04 노트북 3절 | 가져옴 | 새 연결·새 `SqliteSaver`로 읽은 `{"칸 값", "다음 노드", "체크포인트 수"}`, 연결 닫음 |
   | `read_record(record_name)` | 04 노트북 3절 | 가져옴 | 기록 파일의 줄 → 목록(`split()`) |
   | `kill_at_second(worker_path, graph_builder, name_prefix, mode)` | 04 노트북 6절 | 가져옴 | 파일 이름 셋 = 앞머리 + `.sqlite`·`.signal`·`.record`, 띄우기 → 신호(20초) → 끊기 → `assert` → `read_saved(…, mode)` |
   | `append_key(record_name, order_key)` | **06 노트북 2절** | 노트북에 정의 | 기록 파일 끝에 키 한 줄(`"a"`), `"적음"` |
   | `append_key_once(record_name, order_key)` | **06 노트북 2절** | 노트북에 정의 | 파일이 있으면 읽어 키가 있으면 `"건너뜀"`, 없으면 `append_key` |
   | `kill_then_resume(worker_path, graph_builder, name_prefix, strategy)` | **06 노트북 6절** | 노트북에 정의 | `kill_at_second` → `start_worker(…, "resume")`·`wait(timeout=30)` → `read_record` |

   - 04 함수 여섯은 `author_04.DEF_*`와, 06 함수 셋은 `author_06.DEF_APPEND`·`DEF_ONCE`·`DEF_KILL_RESUME`과 **문자열·AST 같음**(`author_06.check_same_as_before()`). 07은 **처음 가져오는 절이 아니므로** 고정 세 문장은 한 번 더 적어도 되고(과정 선례는 절마다 가져올 때 한 번), 「커널이 `notebooks/` 폴더에서 시작해야 …」 한 문장과 가져오기를 **임시 폴더로 옮기기 전** 준비 셀에서 알파벳 순으로.
   - **노트북에만 있는 함수(처음 가르친 절)** — 07이 쓰면 `# Ch 23 NN절에서 배웠습니다 — …`로 도구 파일에 **글자 그대로** 옮기고(생성기에서 `author_NN` 상수와 대조) 해시·묶음 목록 확인: 01 `print_history(history)`·`thread_row(compiled_graph, thread_name)`(칸 `total`·`trace` 전용) · 03 `print_conversation(messages)`·`sqlite_tables(connection)` · 05 `saved_channels(connection, thread_name, task_id)`. 셀 상수(상태 형식·노드)는 생성기 상수를 import해 문자열 대조(「글자까지 같다」는 대조한 것만).
   - worker 둘: `durability_worker.py`(04 — 저장 시점을 넷째 글로) · `idempotency_worker.py`(06 — 쓰기 방식 `naive`/`idempotent`를 넷째 글로, 노드 `receive_order` → `charge`, 저장 시점 `sync`, 주문 키 `order-2306`). 07이 자식 프로세스를 쓰면 이 둘 가운데 하나를 그대로(새 worker를 만들면 새 파일·묶음 목록 둘).

3. **허용 문법 범위(01~06 끝 — 07은 이 안에서만)**: 상태 형식은 칸만 적은 `TypedDict`(칸 구성이 바뀌면 새 이름 — `CountState`·`StepState`·`ResultState`·`OrderState` 선례) · 리듀서 `operator.add`·`add_messages` · `StateGraph`·`add_node`·`add_edge`(고정 엣지 둘로 같은 단계 — 05)·`START`·`END`·`compile(checkpointer=…)` · `InMemorySaver()`(01) · `sqlite3.connect(이름, check_same_thread=False)` → `SqliteSaver(연결)` → `close()`(03) · `with SqliteSaver.from_conn_string(이름) as 이름:`(03 — `open` 밖 `with`는 이것만) · `psycopg.connect(…, autocommit=True, row_factory=dict_row)`·`PostgresSaver(연결)`·`setup()`(02 — 서버 필요, 07은 권하지 않음) · 설정 딕셔너리 `{"configurable": {"thread_id": …}}` · `invoke(입력, 설정)`·`invoke(입력, 설정, durability="exit"|"async"|"sync")`·**`invoke(None, 설정)`(05)** · `get_state(설정)`의 `.values`·`.next`·`.tasks`(칸 `name`·`error`·`result` — 05)·`.metadata["step"]`·`["source"]` · `list(get_state_history(설정))`를 변수에 담은 뒤 `len` · `HumanMessage`·`AIMessage`(코드가 만든 메시지 — 03) · `type(x).__name__` · `try`/`except KeyError`·`ValueError`·`TimeoutError`·`psycopg.Error` `as error`(셀이 받아 출력) · `raise TimeoutError("이 절에서 만든 실패 흉내입니다.")`·딕셔너리 `failure_plan`·`call_count`(05, Ch 16 05 모양) · `time.sleep`·`time.perf_counter()` 기한 루프(04 — 걸린 시간 재기 아님) · `subprocess.Popen`·`kill()`·`wait(timeout=)`·`sys.executable`(04 — 도구 파일 안) · `os.path.exists`·`os.path.abspath`·`os.listdir`·`tempfile.mkdtemp`·`os.chdir`(준비 셀) · 자리 찾기 셀(`candidates` + `for`·`break`, 준비 셀의 `assert … is not None`) · `with open(…, encoding="utf-8")`·여는 방식 `"a"`·`read().split()` · 목록 `count`·`append`·`in` · SQL `SELECT … FROM writes WHERE thread_id = ? … ORDER BY …`·`sqlite_master`(03·05) · `sorted(목록)`(키워드 없이 — 결과 목록·파일 목록) · `range`·`str`·글 `+` · `assert`(우리 코드가 정하는 값에만). **01~06 모두 안 쓴 것**: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·튜플 풀기·별표 풀기·세미콜론·`isinstance`·데코레이터·클래스(상태 형식 말고)·`try`/`finally`·`with sqlite3.connect`(연결을 닫지 않음 — 03)·`Path`·`is`(준비 셀 `assert` 말고)·`AsyncSqliteSaver`·`psycopg_pool`·모델.

4. **결정적 값·흔들린 값(01~06, 새 커널 두 번 + 노트북 밖 확인)**. **안 흔들림**: 01 체크포인트 실행 한 번에 셋(`input`·`loop`·`loop`)·합계 3 → 7·없는 스레드 `{}`/`()` · 02 `UndefinedTable`·`42P01`·표 넷·기록 열 줄·줄 수 6/3 · 03 새 연결·새 그래프로 이어 가기(`3번째 질문`)·체크포인트 9/3·닫힌 연결 `ProgrammingError` · 04 끝까지 실행 `exit` 1·`async` 4·`sync` 4 · 둘째 노드에서 강제 종료 뒤 `exit` `{}`·`()`·0 ↔ `sync` `{'completed': ['first']}`·`('second',)`·3 · 다시 실행 기록 `first, second, first, second` ↔ `first, second, second` · 05 부른 횟수 `{'good': 1, 'flaky': 1}` → `{'good': 1, 'flaky': 2}`·`다음 노드: ('flaky',)`·작업별 칸 이름 `results`/`__error__`·체크포인트 기본값 2 → 3 / `exit` 1 → 2 · **06 끊긴 뒤 `{'order_key': 'order-2306', 'notes': ['주문 받음']}`·`('charge',)`·3 · 끊기 전 키 한 줄 · 다시 실행한 뒤 4 · `naive` `['주문 받음', '적음']`·두 줄 ↔ `idempotent` `['주문 받음', '건너뜀']`·한 줄 · 되풀이 `naive | 0 | 5`·`idempotent | 5 | 5`(밖 판 A 20/20씩, 판 B 실패 흉내 10/10씩)**. **흔들림(결론 밖)**: **04 `async` 강제 종료**(교재 출력 5번 중 4번 남음·B 5/5·준비 확인 60 중 4 잃음·고친 worker 40/40 남음 — 결과 읽기 둘째 단락·b7에만, 「이번 실행에서는」) · 05 두 노드가 끝나는 차례(출력하지 않음, 횟수만) · 체크포인트 ID·작업 id·시각·프로세스 번호·임시 폴더 위치(출력하지 않음). 07도 `async` 강제 종료 값을 결론·그림·정리·복습에 쓰지 말 것.

5. **요청 수 선례와 07**: 01~06 모두 **모델 요청 0번**(챕터 리드 결정 1 — 키 셀·모델 셀 없음). 규격 §7-2 실습 절 「모델 호출 3~5번」과 다름 → 07도 0번이면 **까닭을 07 진단·챕터 요약에 적고 강사 확인 대상**(준비 노트 §13·§9-1 — Part 1 실습 절 0번 선례). 대화가 필요하면 03처럼 메시지 칸에 코드가 만든 `HumanMessage`·`AIMessage`(모델 글이 아니라는 한 문장). 잠금(`pyproject.toml`·`uv.lock`)에는 `langchain`·`openai`가 없음 — 모델을 넣으려면 `uv lock`이 필요(보호 파일, 챕터 리드 결정 없이 하지 말 것).

6. **07 설계 권고(규격 §7-2, 준비 노트 §13)**: 실행 1(기본) → 실행 2(값 하나만 바꿈), 각각 예상 → 실행 → 출력 확인 → 비교, 본문 「앞에서 배운 내용」에 「절 | 배운 것 | 실습에서 쓰는 곳」 표, 그림 조립도·실행 1 순서·실행 1·2 비교 + 삽화. 「앞 절 기능 2~3개」 후보 — 자료실 대출 신청 흐름(Ch 20~22 자료실 소재): **03 SQLite 체크포인터(임시 폴더 파일)·스레드 이름(이용자별) + 05 실패 흉내로 멈춘 뒤 원인을 없애고 `invoke(None, config)`로 이어 가기 + 06 `append_key_once`(멱등 키 = 대출 번호)로 대출 기록 파일에 한 줄**. 노드 예: 대출 기록(`append_key_once`) → 알림(실패 흉내). 실행 2는 값 하나만 — 쓰기 함수를 `append_key`로(기록 두 줄) 또는 `durability="exit"`(체크포인트 수) 가운데 하나. 한 커널 안에서 끝나 자식 프로세스가 필요 없음(04·06 강제 종료를 되풀이하면 코드가 길어짐 — 쓰려면 `kill_then_resume`·`idempotency_worker.py`를 그대로). 결과를 볼 기록은 도구 파일 `read_saved`·`read_record`(또는 01 `print_history`를 옮겨서). 파일은 임시 폴더에만(Part 3 실습 절 「파일을 쓰지 않습니다」 선례와 다름을 진단에 한 줄). 결과는 코드가 정하는 값이라 `assert` 가능(부른 횟수·줄 수·체크포인트 수).

7. **아직 가르치지 않은 것(07이 설명 없이 전제하면 안 되는 것)**: Ch 24 `interrupt`·`Command(resume=)`·`update_state`·시간 여행(`checkpoint_id`로 되돌려 다시 실행 — 공식 문서 「Replay」) · Ch 25 스트리밍(`stream`) · Store(01 b7 한 줄뿐) · 모델 답·도구 메시지 저장·에이전트 그래프에 체크포인터(`create_agent(…, checkpointer=…)`) · `AsyncSqliteSaver`·비동기 실행 · 연결 묶음(`psycopg_pool`, 설치만 됨) · 여러 프로그램이 한 파일·한 표를 함께 쓰기 · 실제 결제·메일 서비스 · 06 조합(저장 시점 `exit`로 끊기·기록을 적기 전에 끊기) · 걸린 시간 재기(모든 절 재지 않음) · Windows·macOS 출력 · 01 `thread_row`를 다른 칸 이름에 그대로 쓰기(칸 `total`·`trace` 전용). 「재시작」은 06 제목 말 — 07 본문은 「다시 실행」.

8. **비유 계열 「체스판과 즉석사진」과 삽화 소품**: 01 나무 탁자 둘·판 둘·왼쪽 사진 여섯(세 장씩 두 줄)·오른쪽 셋·바닥 카메라 하나 · 02 속지를 끼운 사진첩(여섯 장)과 빈 사진첩·카메라 · 03 판 앞 사진 한 장·말 넷·닫힌 사진첩·빈 나무 상자 · 04 탁자 둘에 쓰러진 판 둘·왼쪽 사진 셋 한 줄·탁자마다 카메라 · 05 한 탁자에 판 둘, 오른쪽만 쓰러짐, 왼쪽 앞 사진 한 장, 카메라 없음 · **06 한 탁자 가운데 서 있는 판, 왼쪽 흰 종이에 같은 모양 검은 나이트 실루엣 둘(위아래), 오른쪽 종이에 하나(기보 — 1차 job `db7ef025-73f3-4dde-82f6-5943c262272f`, 2크레딧, 거래 10:57:21Z)**. 07 후보: 한 흐름에 기능을 모은 모습을 **새 소품으로**(앞 소품 되풀이 피함) — 예: 판 하나 앞에 사진 한 장과 기보 한 장이 함께 놓이고 말 상자가 곁에 있는 모습처럼 물건 수를 작게. 규칙: 사람·손·화살표·화면·글자·숫자·시계 없음, 물건은 크게, 개수·자리·상태를 이름으로(「exactly N」·「two rows of three」), 앞 챕터 소품(쟁반·서랍·바구니·저울·울타리·발자국·공구판·승강 상자·식당 전표·집게·세탁기·선반·도장·카드·봉투) 금지, 스타일 첫 문장은 규격 §5-4 그대로. 크레딧은 거래 기록으로 그 절 몫을 가릴 것.

9. **06 노트북은 다시 실행해도 값이 같음**(모델 0·결정적, 계약 파일 없음) — 그래도 설명만 고칠 때는 `mdpatch.py` → `run_section.sh … 06 --no-exec`(`executed_at`·해시를 지키려고). 다시 실행하면 `PYTHONDONTWRITEBYTECODE=1`을 주어 실습 폴더 `notebooks/__pycache__/`를 만들지 않게(06은 그렇게 실행함). 새 커널 두 번 방법은 01~06과 같음(A `run_section.sh` · B 사본 `execute.py` + 환경 변수 넷, `/tmp/ch23-06/cmpout.py`·`texthash.py`). 자식 프로세스를 쓰면 `ps -eo pid,args | awk '$2 ~ /python/ && /…_worker/'`로 남은 것 확인(`pgrep -f`는 거짓 양성).

10. **셀 모양과 문장 선례**: 06 코드 셀 **23**(준비 넷: 설치·가져오기·자리 찾기·임시 폴더), 준비 셀이 아닌 셀 주석 뺀 코드 최대 9줄, 함수 본문 최대 7줄(도구 파일 최대 8줄), 셀당 정의 하나, 검사 문장 348. 실습 절은 19~25셀 선례(Ch 22 09 19셀·Ch 21 07 24셀). **G6 주의**: 괄호 뒤 `).`는 문장 끝으로 세지 않아 괄호 설명은 문장 가운데로(06 첫 검사 1건). **G5**: 결과 읽기 첫 단락의 숫자 든 백틱은 바로 앞 셀 출력에 글자 그대로. 「스크립트와 글자까지 같다」 같은 문장은 생성기 `assert`로 대조한 것만(06 선례).

11. **그림·색 선례(06)**: 두 결과 나란히 = 회색 공통 상자 → subgraph 둘(06-4, 폭 658), 차례 = 한 줄 상자(06-2, 273), 함수 갈래 = 점선 두 갈래 + 라벨(06-3, 495), 끊긴 자리 = subgraph + 점선 두 갈래(06-1, 390). 가운뎃점(`·`)이 든 긴 줄은 저절로 꺾이니 `<br>`로 미리 나눌 것(06-2·06-4 첫 렌더). 06은 paired라 **Before 결과 한 상자만 빨강** — 07은 experiment라 **빨강 0**(받아 출력한 오류도 노랑), 보라 0(모델 없음), 우리 코드 파랑·출력 노랑·공통 회색, 원본 폭 868 이하.

12. **마감 몫(01~06 진단의 남은 것 전부 — 07 뒤 챕터 마감 담당)**:
    - **02 `qa/upgrade/pre_exec.sh`**(`8f078591…` — `N=02`일 때만 PostgreSQL을 켜고 `trap EXIT`로 끔, 02를 다시 실행하려면 같은 호출 안에서) 지우지 말 것 · **실습 폴더 README의 옛 Docker 명령**(`postgres:17`·`kdt-ch23-postgres`·55432)을 02 준비물(Ch 12 02 컨테이너 `hankyung-part3-pgvector`·같은 접속 글·이름 공간 `ch23_lab`)과 같게 다시 씀.
    - **README 다시 쓰기 전체**: 노트북 일곱 · `uv sync --locked` → `.venv` → `notebooks/`에서 열기 · **도구 파일 단락(`checkpoint_tools.py` 함수 아홉·import)** · worker 둘(04 저장 시점·06 쓰기 방식, 인자 다섯) · 파일은 노트북 임시 폴더에 생김 · 절별 모델 요청 0 · 02 서버 안내 · `labs/part6/continuity-guide.md` 문장 확인.
    - **`part6-practice.zip` 재생성**(`python3 textbook/part6/_build_index.py`) — 지금 묶음(`3755de3d…`) 안의 01~06 노트북·worker 둘은 옛 판이고 **도구 파일이 없음**. 04 노트북·`durability_worker.py`, 06 노트북·`idempotency_worker.py`·`checkpoint_tools.py`는 짝이라 반드시 함께. 뒤이어 `check_delivery.py`(`llm-practice.zip` Stale 예상 — 과정 공통)·옛 검사 넷 돌려 기록(`check_notebook_readiness.py`는 결과 파일 되돌림)·`check_bundle_execution.py`(Ch 23 안 돌림).
    - **`chapter.json`**: 07 절 추가 · `objectives` 셋을 절 본문 말과 대조(「체크포인터와 thread_id로 … 저장하고 재개」 — 01·03 · 「PostgresSaver를 준비하고 내구 실행 모드별 장애 복구 범위를 비교」 — 02·04 · 「pending writes와 멱등 키」 — 05·06, 본문은 「남은 쓰기」·「저장 시점」) → `_build.py`.
    - **Part 6 목차·묶음 목록**: `textbook/part6/_build_index.py` 21행(시수 6·10 그대로, 설명 대조) · `textbook/_notebook/build_index.py` 50행(절 수 6 — 선례대로 둘지) · 챕터 `qa/public-files.json`·`textbook/part6/public-files.json`에 07 노트북·HTML 줄(경로 배열 직접 한 줄, Part 목록은 이름 차례) · 챕터 목록의 **옛 SVG 여섯 줄**(`figures/0N-흐름.svg`)을 옛 그림 삭제와 함께 정리 · `check_scope.py`(기록만).
    - **옛 생성기**: `figures/_gen_figures.py`(`6d95031c…`, 맨 위 `raise SystemExit`) `mv -n` → `qa/upgrade/before/generators/blocked/` · **공용 `qa/author_ch23_ch24.py`**(`44c9d593…`, Ch 23 쪽만 막음)는 옮기지 않음 — Ch 24 개선 때 함께 정함(옮기면 Ch 24 쪽 찾는 자리가 바뀜).
    - **옛 그림 18개** 삭제 승인 목록(`figures/0N-흐름.{svg,excalidraw,caption.md}`, N=1~6 — 본문 참조 0, 사본 `before/figures/`, `final-artifact-hashes.json`이 해시를 적어 둔 기록 파일) · `visual.cjs`(1280px·390px).
    - `qa/research.md`·`qa/verification.md`·`집필점검표.md` 위쪽 옛 기록에 「개선 전 판」 표시 · 챕터 요약 `qa/upgrade/chapter-summary.md`(새 말 합 — meta 3·3·3·4·3·3 = 19, 말은 바뀜 · 도구 파일 해시 · worker 둘 해시 · 요청 0 · `gates-after.json`).
    - **제목의 영어·한자어(강사 확인)**: 챕터 「Persistence와 Durable Execution」 · 02 「PostgresSaver」·「스키마」 · 04 「내구」 · 05 「pending writes」 · 06 「재시작」·「멱등성」(본문에서 풂) — 슬러그는 01·04·05·06 고정(Ch 20 02·03 b7 링크).
    - **강사 확인 대상 모음**: 01~06 진단 §강사 확인(02 PostgreSQL 선택 A·작업 환경 17.11 · 04 `async` 흔들림·worker 다시 씀 · 05 0.1초 쉼·전역 딕셔너리 · 06 worker 다시 씀·도구 파일에 06 함수 셋·읽기용 `charge`) + 07 요청 0번.
    - **뒤 챕터 인계**(고치지 않음, 챕터 요약에): Ch 24 01 b3 「노드는 장애 뒤 처음부터 재시작될 수 있고 외부 쓰기에는 멱등성이 필요」 — **06으로 참** · Ch 31 02 b3 「중단 뒤 재개와 멱등성」 — **참** · Ch 31 05 b3 「`setup()`이 표를 만든다」 — 02로 참 · Ch 30 02 b3 「생성 비용과 수명주기」 — 수명만 참(03) · Ch 27 04 b3 「체크포인터 메시지」 — 03으로 참 · Ch 25·26 b3 — 01로 참 · Ch 20 02·03 b7 링크 슬러그 그대로 · Ch 22 09 b8 — 03으로 참.
    - **삭제 승인 대상**: 실습 폴더 `.venv`(macOS 142MB) · `.cache/vm/venv-ch23-persistence`(233MB) · 기기 `/tmp/ch23-prep`·`/tmp/ch23-01`~`/tmp/ch23-06`(02의 PostgreSQL 클러스터 `/tmp/ch23-02/pgdata` 포함 — 서버는 꺼져 있음) · 기기 세션 임시 폴더 `$TMPDIR/ch23-0N-*` · `$ROOT/.cache/ch23-prep/`(SQLite 시험 파일 넷) · `.cache/ch23-0N-view/` · `qa/upgrade/gates-wip-*.json` · `qa/upgrade/__pycache__/`.

## 실습 → 챕터 검토

**07절 `07-Persistence-실습`을 새로 만들었습니다**(2026-09-25). 제목은 「Persistence 실습: 멈춘 대출 처리를 이어 가고 기록은 한 번만 남기기」이고 `chapter.json`에 `format: experiment`로 더했습니다. 기록은 `qa/upgrade/07-diagnosis.md`, 그림 설계표는 `qa/upgrade/07-figures.md`, 검토 묶음은 `qa/upgrade/review-pack/07-Persistence-실습.md`입니다. 위 「챕터 공통」의 준비 셀·용어·색·비유 약속은 그대로 삽니다. 슬러그는 위 「§06 → 실습(07)」 후보 그대로.

### 1. 이 절이 한 것

- **주제**: 자료실 창구의 대출 신청 한 건 — 이용자 번호 `M-0317`(Ch 21 03절 실행 정보 값 그대로, 스레드 이름으로 씀)·대출 키 `loan-2307`(이 절에서 실행 전에 정함, 06 `order-2306` 모양 — 멱등 키). 그래프는 노드 `receive_request`(칸 `notes`에 `신청 받음`) → `record_loan`(쓰기 방식대로 대출 기록 파일에 키 한 줄 → **그 뒤에** 실패 흉내가 켜져 있으면 알림을 보내다 `TimeoutError`). 실행 1 = 쓰기 방식 `idempotent`, 실행 2 = **쓰기 방식 하나만 `naive`**(06 Before/After와 같은 값 — b2·노트북 6절 앞 「새로 볼 것」 한 문장: 강제 종료가 아니라 같은 커널 안의 실패 흉내로 멈추고 새 연결에서 이어 갈 때도 같은 차이인지). 파일 이름은 쓰기 방식 이름을 앞머리로(`idempotent.sqlite`·`.record` / `naive.…`), 스레드 이름은 두 실행 같음.
- **붙인 앞 절 기능 셋 — 모두 흐름 안에서 쓰임**(두 실행 모두, 코드로 셈): **03** SQLite 체크포인터(임시 폴더 파일) + 멈춘 뒤 `close()` → **새 연결·새 `SqliteSaver`·새 그래프**가 같은 자리(`('record_loan',)`)를 읽고 **이어 가기도 그 새 그래프로** · **05** 실패 흉내(`failure_plan`·`call_count`, 05 `flaky`와 같은 오류 글)와 원인을 없앤 뒤 `invoke(None, config)` → 부른 횟수 1·1 → 1·2 · **06** `append_key_once`(도구 파일) → 다시 실행된 `record_loan`이 `건너뜀`, 기록 한 줄(실행 2 `append_key` → `적음`·두 줄). 04 `read_saved`·`read_record`(도구 파일)는 결과 읽기에만.
- **설계의 까닭(강사 확인)**: 멱등 키 확인이 흐름에서 실제로 「건너뛰려면」 기록을 적은 노드가 다시 실행되어야 하고, 자식 프로세스 없이 한 커널 안에서 그렇게 되는 모양은 「기록을 적는 노드 안, 기록 뒤의 실패 흉내」뿐(기록 노드와 실패 노드를 나누거나 같은 단계에 두면 기록 노드는 다시 실행되지 않아 쓰기 방식을 바꿔도 결과가 같음 — Ch 20 05 B-8 교훈). 그래서 **06 b7이 「노트북 밖 판 B만」으로 적은 장면을 07이 노트북에서 실행**(인계 1항은 「다루지 않는 쪽」 권고였음). 결과(두 줄/한 줄)는 06 b7 문장과 같고, 06 b7은 06 노트북에 대해 여전히 참.
- **뺀 것**(b3 둘째 단락): 02 PostgreSQL(서버) · 04 저장 시점 비교·강제 종료(04·06 되풀이·자식 프로세스) · 05 같은 단계 두 노드·남은 쓰기·표 `writes`(이번 흐름에 없음) · 03 메시지 칸(대화 아님) · 01 `InMemorySaver`(다시 열 파일 필요).
- **새 문법·새 API·새 말 0개**(07 코드 셀의 이름·속성·키워드 인자를 01~06과 AST 대조 — 내장 이름·속성·키워드 0, import 둘은 06 함수를 도구 파일에서 가져오는 줄). 이 절이 정의한 것은 노드 둘과 상태 형식 `LoanState`(06 `OrderState`와 칸 이름만 다름 — 생성기 대조). **도구 파일 그대로**(`71280dd9…`). 모델 요청 0 · 키 셀 없음 · 자식 프로세스 0 · 걸린 시간 재지 않음. `assert`는 같은 키 줄 수(1·2)에만.
- 코드 셀 **22개**(준비 셋: 설치·가져오기·임시 폴더), 준비 셀이 아닌 셀 최대 9줄, 함수 본문 최대 8줄(`record_loan`), 검사 문장 333, 게이트 G1~G7 **0**(챕터 전체 7/7 PASS). meta 「실습 30분 · 새 용어 0」, **챕터 시수에 더하지 않음**(`hours` 그대로). Mermaid 3 + 삽화 1.

### 2. 실행으로 확인한 값 (새 커널 A 11:27:23~25 · B 11:27:49~51 UTC 두 번 22/22 같음 + 노트북 밖 준비 확인 10회 같음 — 챕터 요약이 인용할 수 있는 값)

- 준비: `도구 파일에서 가져온 함수: append_key, append_key_once, read_record, read_saved` · `임시 폴더 이름에 ch23-07-이 들어 있는가: True`·`현재 작업 폴더의 파일: []` · `이용자 번호: M-0317`·`대출 키: loan-2307`(출처 줄 둘) · `등록한 노드: ['receive_request', 'record_loan']`.
- 실행 1(`idempotent`): `오류 종류: TimeoutError`·`오류 메시지: 이 절에서 만든 실패 흉내입니다.`·`부른 횟수: {'receive_request': 1, 'record_loan': 1}` → `남은 칸 값: {'loan_key': 'loan-2307', 'notes': ['신청 받음']}`·`다음 노드: ('record_loan',)`·`체크포인트 수: 3`·`멈추기 전에 적힌 키: ['loan-2307']` → 연결을 닫고 새 그래프 `새 그래프가 읽은 다음 노드: ('record_loan',)`·`새 그래프가 읽은 칸 notes: ['신청 받음']` → 원인을 없애고 `None` `칸 notes: ['신청 받음', '건너뜀']`·`부른 횟수: {'receive_request': 1, 'record_loan': 2}` → `다음 노드: ()`·`체크포인트 수: 4`·`대출 기록 파일의 키: ['loan-2307']`·`같은 키가 적힌 줄 수: 1`.
- 실행 2(`naive`): 멈춘 뒤 `('record_loan',)`·3·`['loan-2307']`(같음) → `칸 notes: ['신청 받음', '적음']`·부른 횟수 1·2(같음) → `()`·4·`['loan-2307', 'loan-2307']`·`같은 키가 적힌 줄 수: 2`.
- 견주기: `idempotent | ['신청 받음', '건너뜀'] | 4 | 1`·`naive | ['신청 받음', '적음'] | 4 | 2` · 끝 `현재 작업 폴더의 파일: ['idempotent.record', 'idempotent.sqlite', 'naive.record', 'naive.sqlite']`(연결을 모두 닫아 `-wal`·`-shm` 없음).
- 흔들린 값 없음. `code_sha256` `c950067c72cc…` · `outputs_sha256` `5db80578cc6b…`(A·B 같음) · 노트북 파일 `0fe06118afcf…`.

### 3. 함께 고친 파일 (검토자가 볼 곳)

**챕터 안**
- `chapter.json` — 07절 추가(`d45772cc…` → `36267fb51acb…`). **`hours`·`objectives` 그대로**(objectives는 마감 몫, 아래 5번).
- **06절 마지막 문장**: b8·노트북 정리 끝 「07절 실습에서는 이 챕터에서 배운 것을 작은 흐름 하나에 모아 실행합니다」가 07 내용과 맞아 **글은 그대로**, 01~05 b8처럼 **`_src` b8에 07 링크만** 더함 — `author_06.py`(`912c8dc7…` → `f620b444e385…`, 고치기 전 생성기 `src_html()`이 그때 `_src`와 같음 확인) → `--src-only`(`_src/06` `302faf19…` → `000920725beb…`) → `run_section.sh … 06 --no-exec`(06 게이트 0). 노트북 끝 줄은 링크 없는 선례대로 두어 `mdpatch.py`를 쓰지 않음. **06 노트북 `869b6ae460f4…` · `code_sha256` `52c92b7d3410…` · `outputs_sha256` `8cf67c492cc6…` · `executed_at` 10:54:54Z 그대로.** 06 빌드 HTML만 `2b2a9a45…` → `818b6b402240…`(다음 절 링크 + b8 링크), 챕터 `index.html` `45f0847c…` → `822f099e9e8f…`.
- 챕터 `qa/public-files.json` — **07 HTML·07 노트북 두 줄**(06 줄 다음, `8aa1f73d…` → `d16b71f330f8…`, 보호 파일 — Ch 21 마감 선례).
- 새 파일: 노트북 07 · `_src/07`(`d0c586bd8191…`) · 빌드 `07-Persistence-실습.html`(`164f1f6ad01c…`, `{{` 0건) · `figures/07-1`~`07-3`(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`) · `figures/07-4-리본으로-이은-사진과-기보.{png,prompt.md,caption.md}` · `qa/upgrade/author_07.py`(`21e1e5e9533a…`) · `07-figures.md`·`07-diagnosis.md` · `gates-wip-07.json`·`gates-wip-07-07.json`·`gates-wip-ch23-after07.json` · `review-pack/07-Persistence-실습.md`.
- `집필점검표.md` 품질 개선 표 07 행 · `qa/verification.md` 품질 개선 검증 표 07 행 · `qa/upgrade/manifest-changes.md` 「07절 끝」 · 이 파일 이 절.

**챕터 밖**
- `labs/part6/ch23-persistence/README.md` — 맨 아래 **07절 한 단락만**(`a876fed0efab…`). 옛 첫 단락·Docker 명령은 마감 몫.
- `textbook/part6/public-files.json` — `python3 textbook/part6/qa/collect_public_files.py`로 다시 모음 → **07 노트북 한 줄만** 늘어남(`9beba972…` → `8ed6852b524f…`, 보호 파일). `prerequisite-files.json` 바이트까지 같음.
- `textbook/part6/index.html`(`ec2588c0fded…`) · `textbook/downloads/part6-practice.zip`(`43b1923fa3e3…`) · `textbook/part6/qa/integration-results.json`(`2ff2be9f8cd6…`) — `python3 textbook/part6/_build_index.py` 한 번(**`Part 6: 50 verified sections; 96 bundled files`**). 목차에 Ch 23 「7절」·07 링크, **zip 안 Ch 23 항목 13개가 모두 디스크와 같아짐**(04~06 노트북·worker 둘·도구 파일이 처음 새 판으로 — 06 인계의 「짝으로 다시 묶기」가 이 판에서는 맞음, README를 마감에서 다시 쓰면 한 번 더). `_build_index.py`는 고치지 않음(21행 설명은 마감 몫).
- `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json` — `verify.py --chapter`가 다시 씀(`8d2cedf1b8e2…`).
- **고치지 않음**: 01~05 파일 · 06 노트북 · 도구 파일 · worker 둘 · `pyproject.toml`·`uv.lock` · 공용 옛 생성기 `qa/author_ch23_ch24.py`·`figures/_gen_figures.py` · 옛 그림 · Ch 24~31 파일 · `textbook/index.html` · 공용 도구·규격·과정 요약·`build_index.py`.

### 4. 검사 결과

- `run_section.sh … 07 --no-exec`: 게이트 G1~G7 **0**, `verify.py --chapter` **`PASS 7 sections / 179 code cells (max 14 lines)`**, 빌드 HTML `{{`·`[[` 0건, SVG 셋·삽화 하나. 챕터 전체 `gates-wip-ch23-after07.json` **7/7 PASS**. 07·06·목차 상대 링크 59개 모두 있음(`check_delivery.py` 링크 규칙으로 따로), 07 복습 4·해설 4·b1~b10 있음.
- `check_delivery.py` — **117행 `llm-practice.zip`의 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`에서 멈춤**(알려진 일, 전체 마감 몫). 그 앞(절 검사 50·비밀값·개인 경로·`part6-practice.zip` 매니페스트 신선도)은 지나감. `delivery-results.json` 안 바뀜(`3cc2d143…`).
- `check_bundle_execution.py`·`check_scope.py`·`visual.cjs`·옛 검사 넷은 돌리지 않음(마감 몫).
- 보호 파일 123개: **104개 같음·19개 바뀜·없어진 파일 0** = 06절 끝까지의 14개(이 절이 값을 다시 바꾼 것: 묶음 목록 둘·`verification.md`·notebook-contracts) + **이 절이 지시대로 바꾼 다섯**(`chapter.json`·실습 폴더 `README.md`·`part6/index.html`·`part6-practice.zip`·`integration-results.json`) — `manifest-changes.md` 「07절 끝」.
- 삽화 `07-4` 1차 채택(job `a6c8200a-a747-4590-824a-e3c904038749`), 2크레딧(거래 11:32:55Z), 저장 PNG ↔ 채택 job 픽셀 차이 0. 리본은 「두 물건을 묶음」이 아니라 「판에서 두 물건 사이로 이어짐」으로 그려져 본문을 보이는 대로 고침(재생성 0).

### 5. 챕터 마감 담당이 이어서 할 것 (「§06 → 실습(07)」 12번 마감 몫 전부 + 01~06 진단의 마감 몫 + 07이 더한 것)

1. **`chapter.json` `objectives`** 셋을 절 본문 말과 대조(「체크포인터와 thread_id로 … 저장하고 재개」 — 01·03 · 「PostgresSaver를 준비하고 내구 실행 모드별 장애 복구 범위를 비교」 — 02·04, 본문은 「저장 시점」 · 「pending writes와 멱등 키」 — 05·06, 본문은 「남은 쓰기」) + **07 실습 줄을 넣을지**(예: 「실습에서 SQLite 체크포인터를 붙인 대출 처리 그래프를 실패 흉내로 멈췄다 새 연결로 이어 가고, 쓰기 방식 하나를 바꿔 대출 기록 파일의 줄 수를 견줄 수 있습니다」) → `_build.py`. **제목의 영어·한자어(강사 확인)**: 챕터 「Persistence와 Durable Execution」 · 02 「PostgresSaver」·「스키마」 · 04 「내구」 · 05 「pending writes」 · 06 「재시작」·「멱등성」 · **07 「Persistence 실습」**(슬러그 01·04·05·06 고정 — Ch 20 02·03 b7 링크).
2. **Part 6 목차·묶음**: `textbook/part6/_build_index.py` 21행(시수 6·10 그대로, 설명 문장 대조 — 실습 절 문구를 더할지, Ch 21 19행 선례) → 다시 돌려 `part6-practice.zip` 재생성(README·objectives 고친 뒤 한 번 더) · `textbook/_notebook/build_index.py` 50행(절 수 6 — Ch 20·22 선례는 실습 절을 뺀 수, 그대로 둘지) · `check_scope.py` `SECTION_COUNTS`(기록만) · 챕터 `qa/public-files.json`의 **옛 SVG 여섯 줄**(`figures/0N-흐름.svg`)을 옛 그림 삭제와 함께 정리 → `collect_public_files.py` → `check_delivery.py`(`llm-practice.zip` Stale 예상 — 과정 공통) · 옛 검사 넷(`check_notebook_readiness.py`는 결과 파일 되돌림) · `check_bundle_execution.py`(Ch 23은 모델 없는 절이라 묶음 실행 대상인지 확인 — 02는 PostgreSQL 서버, 04·06은 자식 프로세스).
3. **실습 폴더 README 다시 쓰기 전체**(지금은 옛 첫 단락 + 07 한 단락): 노트북 일곱 · `uv sync --locked` → `.venv` → `notebooks/`에서 열기 · **옛 Docker 명령**(`postgres:17`·`kdt-ch23-postgres`·55432)을 02 준비물(Ch 12 02 컨테이너 `hankyung-part3-pgvector`·같은 접속 글·이름 공간 `ch23_lab`)과 같게 · 도구 파일 단락(`checkpoint_tools.py` 함수 아홉·import — 07은 넷을 가져옴) · worker 둘(04 저장 시점·06 쓰기 방식, 인자 다섯) · 파일은 노트북 임시 폴더에 생김 · 절별 모델 요청 0 · `labs/part6/continuity-guide.md` 문장 확인. **02 `qa/upgrade/pre_exec.sh`**(`N=02`일 때만 PostgreSQL을 켜고 끔) 지우지 말 것.
4. **옛 생성기·옛 그림**: `figures/_gen_figures.py`(`6d95031c…`) `mv -n` → `qa/upgrade/before/generators/blocked/` · **공용 `qa/author_ch23_ch24.py`**(`44c9d593…`)는 옮기지 않음 — Ch 24 개선 때 함께 정함 · 옛 그림 18개(`figures/0N-흐름.{svg,excalidraw,caption.md}`, N=1~6) 삭제 승인 목록(사본 `before/figures/`, `final-artifact-hashes.json`이 해시를 적은 기록 파일) · `visual.cjs` 1280px·390px(HTML 일곱).
5. **기록**: `qa/research.md`·`qa/verification.md`·`집필점검표.md` 위쪽 옛 표에 「개선 전 판」 표시 · **`chapter-summary.md`**(PLAYBOOK §6): 새 말 합(meta 3·3·3·4·3·3·**0** = 19) · 도구 파일 해시·함수 아홉(07이 쓰는 넷, `kill_then_resume`은 07도 쓰지 않음) · worker 둘 해시 · 요청 0(07 포함 — 규격 §7-2와 다름) · **실습 30분은 챕터 시수에 더하지 않음** · 07 주제와 결과(위 2번) · 비유 「체스판과 즉석사진」 일곱 장 · `gates-after.json`(`upgrade_gates.py … --label after`) · 한국어 감사 3단·그림 판독 별도 세션(01~07).
6. **강사 확인 대상 모음**: 01~06 진단 §강사 확인(02 PostgreSQL 선택 A·작업 환경 17.11 · 04 `async` 흔들림·worker 다시 씀 · 05 0.1초 쉼·전역 딕셔너리 · 06 worker 다시 씀·도구 파일에 06 함수 셋·읽기용 `charge`) + **07 진단 §12**(모델 요청 0 · 06 b7 판 B를 노트북에서 · 실행 2가 06과 같은 값 · 대출 키를 새로 정함 · 삽화 리본 모양).
7. **뒤 챕터 인계**(고치지 않음, 챕터 요약에): Ch 24 01 b3 「노드는 장애 뒤 처음부터 재시작될 수 있고 외부 쓰기에는 멱등성이 필요」 — 06으로 참(07도 같은 방향: 실패 흉내로 멈춘 노드가 처음부터 다시 실행, 멱등 키로 한 줄) · Ch 31 02 b3 「중단 뒤 재개와 멱등성」 — 참 · Ch 31 05 b3 — 02로 참 · Ch 30 02 b3 「생성 비용과 수명주기」 — 수명만 참(03) · Ch 27 04 b3 — 03으로 참 · Ch 25·26 b3 — 01로 참 · Ch 20 02·03 b7 링크 슬러그 그대로 · Ch 22 09 b8 — 03으로 참. 07을 가리키는 뒤 챕터 문장은 없음(`grep` — Part 6 목차·목록 말고 0).
8. **삭제 승인 대상**: 실습 폴더 `.venv`(macOS 142MB) · `.cache/vm/venv-ch23-persistence`(233MB) · 기기 `/tmp/ch23-prep`·`/tmp/ch23-01`~`/tmp/ch23-07`(02의 PostgreSQL 클러스터 `/tmp/ch23-02/pgdata` 포함 — 서버는 꺼져 있음) · 기기 세션 임시 폴더 `$TMPDIR/ch23-0N-*`(07은 노트북 둘 + 준비 확인 열하나) · `$ROOT/.cache/ch23-prep/` · `.cache/ch23-0N-view/`(N=1~7) · `qa/upgrade/gates-wip-*.json` · `qa/upgrade/__pycache__/` · 각 절 진단 「지우지 않은 것」(07은 진단 §13).

### 6. Ch 24 작업자가 전제하면 안 되는 것

- **Ch 23은 모델을 부르지 않았습니다(01~07).** 모델 답·도구 메시지를 저장한 적이 없고, 에이전트 그래프(`create_agent(…, checkpointer=…)`)에 체크포인터를 붙인 적도 없습니다. 「대화」는 03의 코드가 만든 `HumanMessage`·`AIMessage`뿐입니다.
- **`interrupt`·`Command(resume=)`·`update_state`·시간 여행(`checkpoint_id`로 되돌려 다시 실행)·`stream`은 0건**입니다. 07의 「이어 가기」는 오류(실패 흉내)로 멈춘 뒤 원인을 없애고 `invoke(None, config)` — 사람의 승인 값을 넣어 이어 가는 장면은 없습니다. 06·07 함수 이름에도 `interrupt`를 쓰지 않았습니다(`kill_then_resume`).
- **07의 멱등 키 확인은 기록 파일을 읽은 뒤 적는 방식**이고, 한 프로그램·한 커널 안에서만 보았습니다. 여러 프로그램이 한 파일을 함께 쓰는 틈·「보상 작업」·실제 결제·메일 서비스는 실행하지 않았습니다(06·07 b7). Ch 24 01 b8 「interrupt 앞의 필요한 쓰기를 안전하게 … 멱등 처리」는 Ch 24 몫입니다.
- **07은 기록을 적은 뒤의 실패만 보았습니다.** 기록 전에 멈추기·원인을 두고 이어 가기·저장 시점 `exit`/`sync`로 멈추기·강제 종료는 07에서 실행하지 않았습니다(04·06이 강제 종료, 05가 `exit`·원인을 두고 이어 가기(노트북 밖)를 봄). 07은 저장 시점을 적지 않은 기본값(`async`)만 썼습니다.
- **체크포인트 수는 노드 둘인 우리 그래프의 값**(멈춘 뒤 3, 끝난 뒤 4 — 04 끝까지 실행·06과 같은 수)입니다. Ch 24가 노드 수가 다른 그래프에서 이 수를 그대로 쓰면 안 됩니다. Ch 24 01의 「체크포인터는 InMemorySaver」는 01로 이어집니다(Ch 23 03~07은 SQLite).
- **말**: 07은 새 말 0 — 01~06 말(체크포인터·체크포인트·스레드·SQLite 체크포인터·스레드 재개·저장 시점·남은 쓰기·작업·장애 복구·노드 재시작·멱등성·멱등 키)만 씀. 「재시작」은 06 제목 말(본문은 「다시 실행」), 「pending writes」는 05 제목에만. 금지어는 위 「챕터 공통」 표.
- 공용 옛 생성기 `qa/author_ch23_ch24.py`(`44c9d593…`)는 Ch 23 쪽만 막혀 있고 **옮기지 않았습니다** — Ch 24 개선 때 이 파일을 어떻게 할지 정할 것.

## 검토 반영과 챕터 마감 (2026-09-25)

별도 세션 검토 둘(`review-round1-A.md` 01~03·공통 중 2 · 하 17, `review-round1-B.md` 04~07 상 1 · 중 2 · 하 12)을 반영하고 챕터를 마감했습니다. 전체 기록은 `chapter-summary.md`, 절별 마감 기록은 각 `NN-diagnosis.md` 끝 「마감 반영」과 `01·04·07-figures.md` 끝 「마감 반영」입니다. **[상] 1 · [중] 4 · [하] 29를 모두 반영**했고(뒤 챕터 몫 — Ch 30 02 b3 「생성 비용」·Ch 31 02 b7 「보상 작업」·Ch 22 09 b8·Ch 24 `resume` 말 — 은 그 챕터 파일을 고치지 않고 요약 §15에 기록), 게이트를 깨뜨려 반영하지 못한 것은 없습니다. **다시 실행한 노트북은 04·06·07**(모델 요청 0)이고 01·02·03·05는 코드·출력 그대로입니다. 이 파일 위 기록 가운데 마감으로 사실이 바뀐 자리만 적습니다.

1. **「이어 실행」은 Durable Execution 풀이 한 뜻**(검토 A-1, 챕터 리드 결정): 위 「챕터 공통」 「01이 푼 문장」의 **「이어 실행 규칙」 항목은 이름이 바뀜** — 같은 스레드로 다시 부를 때의 규칙(마지막 체크포인트에서 시작 → 새 입력을 칸의 규칙대로 → 노드 실행)은 「같은 스레드로 다시 실행」으로 부릅니다. 01 b4 소제목·노트북 6절 제목·b6 결론·결과 읽기 두 곳, 02 셀 44, 07 b3 표를 고침. 뒤 챕터도 「이어 실행」을 멈춘 실행을 저장된 자리부터 이어 가는 일로만 쓸 것.
2. **위 「§04 → §05」·「§06 → 실습(07)」 2항의 도구 파일 표 — 함수 아홉 → 열**: `new_prefix(name)`(04절 노트북 3절 — 작업 폴더에 `이름-번호.sqlite`가 있으면 번호를 올려 아직 쓰지 않은 앞머리를 내놓음)를 `read_record` 뒤에 더함. 가져오는 절: 06(`kill_at_second, new_prefix, read_record, read_saved, start_worker`)·07(`append_key, append_key_once, new_prefix, read_record, read_saved`). 해시 `71280dd9…` → **`a850b2cdccbd8ff6f3dd8364e5ab58a8f2845eb6c8607ef7250315c5eee26b37`**. `kill_then_resume`은 가져오는 절 없이 남김(B-11, 강사 확인) — 머리 독스트링을 그 사실대로 고침.
3. **04 4·5절은 띄우기·기다리기·끊기가 한 셀**(검토 B-1 [상]): 위 「§04 → §05」의 「4절 `exit`·5절 `sync` 장면은 같은 모양 다섯 셀」 → **네 셀**(끊는 셀 · 새 연결로 읽기 · 다시 실행 · 다시 읽기), 끊는 셀 끝 `assert` 둘(신호 · 종료 코드가 0이 아님). 04 코드 셀 28 → **27**, 파일 이름은 `exit.*`·`sync.*` → **`exit-1.*`·`sync-1.*`**(6절 `exit-2~6`·`sync-2~6`·`async-1~5`). 04-2 그림을 다시 렌더(회색 테두리 칸 「4·5절 셀 하나」).
4. **06·07 파일 이름도 앞머리를 따름**(검토 B-2): 06 `naive-1.*`·`idempotent-1.*`(6절 `-2~6`), 07 `idempotent-1.*`·`naive-1.*`(`write_plan["prefix"]`). 위 「실습 → 챕터 검토」 §2의 07 값 가운데 `쓰기 방식: {'mode': 'idempotent'}` → `{'mode': 'idempotent', 'prefix': 'idempotent-1'}`, 견주기 줄 `idempotent | …`·`naive | …` → **`idempotent-1 | … | 4 | 1`·`naive-1 | … | 4 | 2`**, 파일 목록 → `['idempotent-1.record', 'idempotent-1.sqlite', 'naive-1.record', 'naive-1.sqlite']`, 실행 1 연결 셀에 `SQLite 파일 이름: idempotent-1.sqlite` 한 줄. 나머지 값(부른 횟수·다음 노드·체크포인트 수·줄 수)은 같음.
5. **04 `async` 흔들린 값**: 교재 출력이 **5/5**(다시 실행 4/5)로 바뀌어 결과 읽기 둘째 단락·b7만 고침. 위 「§06 → 실습(07)」 4항 「교재 출력 5번 중 4번 남음·B 5/5」는 **앞 판 기록**입니다.
6. **새 해시**(`code_sha256`/`outputs_sha256`): 04 `490b1737…`/`341f57f4…` · 06 `8d7467af…`/`8bf64357…` · 07 `166e293b…`/`46338827…`. 01 `9d71f6f9…`/`4315f7f9…` · 02 `5b4fa7cf…`/`abb4f3d7…` · 03 `fe89a30a…`/`952dc366…` · 05 `06cd28c6…`/`b39f9ee7…`는 그대로. worker 둘 그대로.
7. **위 「§06 → 실습(07)」 12번·「실습 → 챕터 검토」 §5의 마감 목록은 끝났습니다**: 실습 폴더 README 전체(`7eae43a5…`) · `chapter.json` `objectives` 일곱 줄(`hours` 그대로) · `textbook/part6/_build_index.py` ch23 설명 줄 · 챕터 공개 목록 옛 SVG 여섯 줄 뺌(Part 목록 바이트 같음) · `part6-practice.zip` `aa82b386…`(Ch 23 13파일 디스크와 같음) · `check_bundle_execution.py` PASS · `gates-after.json` 7/7 · `verify.py --chapter` PASS 7/178 · `visual.cjs` 16행 PASS · 옛 생성기 `figures/_gen_figures.py` → `qa/upgrade/before/generators/blocked/`(`mv -n`, 해시 같음) · 옛 기록 파일 셋에 「개선 전 판」 표시 · `chapter-summary.md`. **공용 옛 생성기 `qa/author_ch23_ch24.py`는 옮기지 않음**(Ch 24가 씀 — 01절이 넣은 Ch 23 건너뛰기 그대로). 옛 그림 열여덟·`gates-wip-*.json`·캐시·임시 폴더·`llm-practice.zip`·`pre_exec.sh`와 `/tmp/ch23-02/pgdata` 등은 `textbook/qa/upgrade-final-checklist.md` §2-11.
8. **02는 다시 실행하지 않았고 PostgreSQL도 켜지 않았습니다**: `run_section.sh … 02 --no-exec`가 `pre_exec.sh`로 서버를 켜므로, 같은 단계를 `pre_exec.sh` 없이 부르는 `.cache/ch23-close/tools/nx.sh`로 빌드했습니다. 뒤에 02를 다시 실행할 사람은 위 「§01 → §02」의 `pre_exec.sh` 방식을 그대로 쓰면 됩니다.
9. **Ch 24 작업자에게**: 위 「실습 → 챕터 검토」 §6과 요약 §13 — 특히 **03 「스레드 재개」는 Ch 24 `Command(resume=…)`와 다른 장면**(03 용어 표에 한 문장), 04·06 worker의 단계 이름 `resume`도 강제 종료 뒤 다시 실행일 뿐입니다. 공용 옛 생성기는 Ch 24 개선 때 옮길지 정할 것.
