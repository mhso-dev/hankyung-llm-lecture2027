# 03절 진단과 개선 기록 — 스레드 재개와 대화 이어가기 (experiment)

- 대상: `_src/03-스레드-재개와-대화-이어가기.html` · `labs/part6/ch23-persistence/notebooks/03-스레드-재개와-대화-이어가기.ipynb` · 그림 `figures/03-1`~`03-5`.
- 생성기: `qa/upgrade/author_03.py`(노트북 + `_src`, 01 생성기에서 `html_text`·`table_html`·임시 폴더 셀을 가져오고 폴더 셀은 앞머리만 다른지 `assert`, `08789d9142387415241500bf045b48a9cb4fcbff9d5e2571be946f98554276d8`) · `_src` `59216563fb22…` · 빌드 HTML `7e2c3dc13fcd…` · 노트북 파일 `ab7333da9124…`. 그림 설계표 `qa/upgrade/03-figures.md`. 검토 묶음 `qa/upgrade/review-pack/03-스레드-재개와-대화-이어가기.md`.
- 작업일 2026-09-25(UTC 09:0x~09:2x). 형식 **experiment 유지**, **슬러그·제목 그대로**(링크하는 완료 파일 0).
- **모델 요청 0번**(노트북·노트북 밖 모두, 챕터 리드 결정 1). 키 셀 없음. 흔들림 확인 대상이 없어 `03-probe.md`는 만들지 않았습니다(노트북 밖 확인은 §6).

## 1. 게이트 전후

| | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전 (`gates-before.json`) | 5 | 76 | 2 | 2 | 0 | 0 | 6 | 12 | 3 | **25** |
| 첫 실행 전 (`gates-wip-03-03.json`, 노트북·`_src`만 쓴 판) | 29 | 352 → 355 | 0 | 4 → 0 | 0 | 0 | 0 | 5 → 0 | 18 | — |
| 후 (`gates-wip-03.json`) | **29** | **360** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 첫 검사: G1 **0**, G2 **4**(파일 목록 셀 넷의 `print(…, sorted(os.listdir()))` — 호출 안 호출 안 호출 `nested_call_2plus`) · G6 **5**(70자 넘는 문장 다섯 — b7 소스 행 두 괄호가 `).`로 이어져 한 문장으로 셈, 기준 버전·가져오기 설명 두 문장, b7 교재 출력 환경, b8 다음 절). G2는 `file_names = sorted(os.listdir())`로 변수에 먼저 담고, G6은 문장을 나누거나 괄호를 문장 가운데로 옮겨 **실행 전에 모두 0**으로 만든 뒤 첫 실행을 했습니다(`gates-wip-03-03.json`은 그 마지막 검사 값, G7 18은 그림 파일·설계표가 없던 때).
- 그림을 넣은 뒤 `--no-exec` 두 번(삽화 반영 · 설명 네 곳 손질 뒤) 모두 **G1~G7 0**, `verify.py --chapter` `PASS 6 sections / 101 code cells (max 23 lines)`(최대 23줄은 개선 전 04~06).
- AST 따로(`/tmp/ch23-03/extra_check.py` — 02 판 복사 + 허용 표시 둘): 노트북 금지 문법 **0건**. 허용 표시로 따로 나온 것 5 = `sorted(…)` 넷(키워드 없음 — Ch 4 02·Ch 10 01에서 쓴 모양, 과정 요약 §2-4 Ch 13 내장 이름 목록에 있음) + `with SqliteSaver.from_conn_string("chat.sqlite")` 하나(과정의 `open` 밖 `with` 두 번째 — 첫째 Ch 21 04 `warnings.catch_warnings` 〔마감 정정 2026-09-25, 검토 A-13: 과정의 첫째·둘째가 아님 — 앞선 선례는 Ch 2 05 `with open`(A 트랙)·Ch 2 09·11(B 트랙)·**Ch 10 02 `with pdfplumber.open`**(라이브러리 객체, 기본 경로)·Ch 10 04·09 `zipfile.ZipFile`·Ch 21 04 `warnings.catch_warnings`. 03 b3·9절 설명은 Ch 10 02로 고침〕, 9절 설명 셀에서 한 문장). 클래스는 칸만 적은 `ConversationState(TypedDict)` 하나, 함수 힌트·반환 힌트·데코레이터·f-string·내포식·`lambda`·조건 표현식·`elif`·`next`·`.get`·`+=`·기본값·튜플 풀기·별표 풀기·`is`·`except Exception`·`durability` 0.
- 금지어(`/tmp/ch23-03/ban_check.py` — 02 판 + 「트랜잭션」·「원자적」·「경합」·「보장」·「정확히 한 번」·「원문」·「모사」·「재시작」·「지시문」·「SQLiteSaver」): 노트북·`_src`·캡션 다섯·`.mmd` 넷에서 참 금지어 **0건**(걸린 12건은 모두 「프로그램」 안 「로그」). 「한 겹 더」 0.
- 코드 줄(`count_code.py`) 36 → **127**(셀 5 → 29, 준비 셀 셋). 준비 셀이 아닌 셀의 주석 뺀 코드 최대 **7줄**(`OTHER_FILE`), 함수 본문 최대 **6줄**(`reply`·`sqlite_tables`), 셀당 정의 하나, 첫 줄 주석 100%.

## 2. 수정 전 주요 문제 (준비 노트 §1·§2 03, 인계 §02 → §03)

1. **셀 다섯**: 경로 셀 `[Path.cwd(), *Path.cwd().parents]`·`next(… for …)` 제너레이터 둘·한 글자 `p` 둘 · 노드 힌트 `respond(state: State) -> dict`·f-string 계산 `f"답변 {len(state['turns'])}"` · `with sqlite3.connect(…) as conn:` 블록 둘(설명 「연결을 닫습니다」 — **사실과 다름**, Python `sqlite3`의 `with`는 연결을 닫지 않음) · `durability="sync"`(04절 말을 설명 없이 먼저 씀).
2. **파일 쓰기**: 실습 폴더 `data/thread-resume.sqlite`(+ `-wal`·`-shm`)에 씀 — 학생 폴더에 파일이 남고, 이 작업 기기의 연결 폴더에서는 SQLite 쓰기가 `disk I/O error`로 멈춤(준비 노트 §5-5). `Path.unlink`는 두 번째 실행부터 삭제가 막힘.
3. **틀린 값**: 출력 `database bytes: 4096`은 `SqliteSaver.setup()`이 켠 WAL 때문에 내용이 `-wal`에 있는 동안의 본 파일 크기(준비 확인 `-wal` 65,952바이트·닫은 뒤 본 파일 20,480바이트) — 저장된 양으로 읽으면 틀림.
4. **대화가 글 목록뿐**: 칸 `turns`(`operator.add`)에 글 `질문 1`·`답변 1` — Ch 22 09 b8 「종류별로 출력한 대화 기록이 그 대상」이 반만 참. 「답변 3」은 목록 길이라 숫자가 튀는 까닭 설명 없음.
5. **본문**: b3 「SQLiteSaver」(틀린 이름)·「설치 부담을 줄이기 위해」·「프로세스 경계를 모사」 · b4 「채널」·「인터페이스」·「반환」·「경로」·「로그」 · b5 「첫 with 블록에서 … 연결을 닫습니다」 · b8 「정상 종료한 연결을 바꾼 경우」 · 복습 3 경로 셀 · b10 여섯 절 공통 참고 자료(Interrupts·Time Travel).
6. **노트북 설명**: 제목 셀·「이 노트북에서 할 일」·준비물·그림 첨부·결과 읽기 0, 설명 셀은 `_src` 문장 복사. 그림은 옛 `{{svg:03-흐름}}` 한 장.

## 3. 바꾼 것

- **메시지 칸(M3, 챕터 리드 결정 1)**: 상태 형식 `ConversationState` = 칸 `messages: Annotated[list[AnyMessage], add_messages]` 하나(Ch 13 04 모양, 칸 구성이 Ch 13 04 `ChatState`와 달라 새 이름). 노드 `reply`는 메시지 칸의 `HumanMessage` 수를 세어 `AIMessage(content="N번째 질문을 받았습니다")` 하나를 냄 — **「답」은 모델 글이 아니라 코드가 센 수로 만든 글**(준비물·2절·b5·b7에 한 문장씩). 메시지 클래스는 `langchain_core.messages`에서(잠금에 `langchain` 없음 — langchain 1.4.0 `langchain/messages/__init__.py` 7행이 같은 클래스를 다시 내놓음, Ch 21 가상환경에서 `is` 대조 True). 설치 셀 `"langgraph==1.2.11" "langgraph-checkpoint-sqlite==3.0.3" "langchain-core==1.6.2"`(모두 잠금 판).
- **출력 함수** `print_conversation(messages)`(라벨 줄 `메시지 종류 | 글` + 메시지마다 `type(message).__name__ | message.text`, 본문 3줄) — Ch 22 09 「종류별로 출력한 대화 기록」 모양. 메시지 번호는 `add_messages`가 uuid4로 붙여(설치판 `langgraph/graph/message.py` 202~208행) 출력하지 않음. Ch 13 04 `print_messages(label, messages)`(번호까지 찍음)와 다른 모양이라 이름을 달리함.
- **결정적 장면(챕터 리드 결정)**: 3절 첫 연결 `sqlite3.connect("chat.sqlite", check_same_thread=False)` → `SqliteSaver(first_conn)` → `builder.compile(checkpointer=…)`(표 `[]`) → 4절 스레드 `conversation-a` 질문 둘(메시지 둘 → 넷, 첫 실행 뒤 표 `['checkpoints', 'writes']` — 02 b4 「SQLite 체크포인터는 표를 스스로 만든다」를 출력으로, 체크포인트 6·단계 4, 열린 동안 파일 셋) → **5절 `first_conn.close()`** → 닫은 연결·첫 그래프 모두 `ProgrammingError`·`Cannot operate on a closed database.`(셀에서 받아 출력 — 노랑), 파일 `['chat.sqlite']` → **6절 새 연결·새 `SqliteSaver`·새 그래프**(설계 객체만 그대로)가 `get_state`로 단계 4·`()`·메시지 넷을 읽고 셋째 질문 → **메시지 여섯, `AIMessage | 3번째 질문을 받았습니다`**(`assert` 둘 — 메시지 수·답 글, 코드가 정하는 값) → 체크포인트 9·단계 7.
- **값 바꿔 보기 둘**: 7절 스레드 이름만(`conversation-b`, 같은 글 → `1번째`·메시지 둘, 표 `checkpoints` 줄 `conversation-a | 9`·`conversation-b | 3` — 자리표시자 `?`, Ch 4 03) · 8절 파일 이름만(`other.sqlite`, 같은 스레드 → `{}`·`()` — 01 11절 새 `InMemorySaver`와 짝).
- **연결 닫는 둘째 모양(9절)**: `with SqliteSaver.from_conn_string("chat.sqlite") as block_saver:` 안에서 메시지 6을 읽고, 블록 뒤 같은 그래프가 `ProgrammingError` → 「블록이 끝나면 연결을 닫는다」를 **출력으로**(설치판 `sqlite/__init__.py` 113~120행 `contextlib.closing`). 끝 셀에서 남은 연결을 닫고 파일 `['chat.sqlite', 'other.sqlite']`(옆 파일 없음).
- **준비 셀(챕터 표준)**: 설치 → 가져오기(`sqlite3`·Ch 13 이름·메시지 이름 넷·`SqliteSaver`, `SQLite 판: 3.53.1` 출력) → 임시 폴더(01 셀에서 앞머리만 `ch23-03-`, 생성기 `assert`). 파일 이름 목록은 `sorted`로 출력(새 커널 두 번 같음), **파일 크기·임시 폴더 위치·메시지 번호·체크포인트 ID는 출력하지 않음**.
- **새 말 셋**(meta 「새 용어 3」 그대로): SQLite 체크포인터 · 객체의 수명 · 스레드 재개(resume) — 세 문장(뜻 → 비유 → 이 절 코드). 01 용어(체크포인터·체크포인트·스레드)·02 용어(표 만들기·줄·칸)는 그대로 이어 씀. 「이름 공간」·「표 만들기 기록」·「스키마」·「마이그레이션」 0.
- **본문 10블록 다시 씀**: b3 Ch 4 03·Ch 13 04·Ch 22 09·Ch 2 05·Ch 21 04·01·02 링크 · b4 비유(판을 치웠다가 마지막 사진을 보고 다시 놓기) + 용어 표 + 「닫아도 남는 것과 사라지는 것」(01 10절 덮어쓰기 ↔ 메시지 칸 이어 붙이기)·「다른 상황에 적용」(프로그램을 다시 시작하는 장면은 04절)·「비교와 경계」(SQLite 표 둘 ↔ PostgreSQL 넷, `writes` ↔ `checkpoint_writes` 이름이 다른 짝, `setup()` 스스로 ↔ 직접) · b6 표(파일·스레드별) · b7 아홉 줄 · b10 절에 맞는 참고 자료(문서 셋·소스 행).
- 옛 판의 운영 조언(「다중 서버 운영의 동시성 요구는 별도로 검토」·「보존 기간 정책」)은 실행하지 않은 조언이라 뺐고, b7에 「여러 프로그램이 한 파일을 함께 쓰는 모습은 실행하지 않았습니다」·「오래된 메시지를 줄이는 일은 하지 않았습니다」만.

## 4. 새 커널 두 번 (규격 §2-7 9번 끝)

- A `run_section.sh`(셀 실행 기록 09:08:54.95~09:08:56.09Z, 약 1.1초) — **`PASS 03-…ipynb: 29 cells`**. 그림 파일이 아직 없어 `attach_figures.py`에서 멈춤(과제 차례대로 그림 전에 두 번 실행).
- B 사본 `/tmp/ch23-03/B.ipynb`를 `execute.py`로(09:09:09.04~09:09:10.11Z, `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch23-persistence UV_NO_SYNC=1 PYTHONPATH=…/notebooks`). 두 실행 모두 빈 임시 폴더에서 시작(폴더 이름은 실행마다 다르고 출력하지 않음).
- 셀별 출력 글자 대조(`/tmp/ch23-03/cmpout.py`) **29/29 같음**. 셀별 출력 글자를 이은 해시(`/tmp/ch23-03/texthash.py`) A·B 모두 **`f75291e01abdebdfb9d334bb7aaa633e3059abb64f5c2d09a910734a57193933`**. `code_sha256` **`fe89a30aec83712eac02cd119379e4009e12f44727bdc4444552cae8937613dc`**.
- **`outputs_sha256`은 A `952dc36685ea…` ↔ B `c5bca6072631…`로 다름** — 설치 셀의 stdout이 A는 한 조각, B는 두 조각(`Note: …` 줄과 판 번호 세 줄)으로 나뉘어 저장된 차이뿐이고 글자는 같음(과정 요약 §9 「`outputs_sha256`은 흔들리므로 셀별 출력 글자 해시로 대조」). 흔들린 값 없음 → b6 「새 커널로 두 번 실행했을 때 코드 셀 29개의 출력이 모두 같았습니다」.
- 뒤이은 `author_03.py --src-only`·`mdpatch.py`(설명 네 곳, `/tmp/ch23-03/reps1.json`)·`attach_figures.py`는 마크다운만 바꿈 — 노트북의 `code_sha256`·`outputs_sha256`·`executed_at`(09:08:56Z) 그대로, A 사본과 셀별 출력 29/29 같음, 생성기 `cells()`와 노트북 셀 원본 61/61 같음.
- 준비물 「5초 안에」는 A 셀 실행 기록(약 1.1초)을 넉넉히 둔 값(설치 셀은 네트워크에 따라 다름).

## 5. 도구 파일 — 만들지 않음 (챕터 공통 5)

- 03은 01 함수 `print_history`·`thread_row`를 **쓰지 않음**: `print_history`는 칸 값을 통째로 찍어 메시지 번호(uuid)가 출력에 섞이고, `thread_row`는 01 칸(`total`·`trace`) 전용. 체크포인트 수·마지막 단계 번호는 `list(get_state_history(…))`를 변수에 담아 `len`·`[0].metadata["step"]`로 봄(01 7·8절 모양).
- 02 함수 셋(`table_names`·`column_names`·`count_checkpoints`)은 PostgreSQL `information_schema`·이름 공간 전용이라 쓰지 않음.
- 앞 챕터 함수(Ch 13 04 `print_messages`·Ch 21 `runner_tools.py` `show_messages`)도 가져오지 않음 — 둘 다 이 챕터 실습 폴더 밖이고, 모양이 다름(번호를 찍음 / 사람 메시지 글을 찍지 않음).
- 그래서 `notebooks/checkpoint_tools.py`를 만들지 않았고 묶음 목록(`textbook/part6/public-files.json`·챕터 `qa/public-files.json`) 변경 0. 01·02 노트북이 가져오는 이름도 그대로(다시 실행 없음).
- **03이 처음 가르친 함수(노트북에 있음, 뒤 절이 쓰면 옮길 후보)**: `print_conversation(messages)`(본문 3줄) · `sqlite_tables(connection)`(본문 6줄, `sqlite_master` 이름 차례) — 인계 `§03 → §04`.

## 6. 설치판 동작과 문서 (모델 없는 확인, 2026-09-25)

- **노트북 밖 확인**(기기 `/tmp/ch23-03/`): `probe1.py` — 노트북 흐름과 같은 차례(+ `get_state_history` 단계별 메시지 수 `-1:0 · 0:1 · 1:2 · 2:2 · 3:3 · 4:4`, `writes` 표 6줄, `PRAGMA journal_mode` `wal`)를 **20번** 돌려 메시지 번호를 뺀 출력 **20/20 같음**. `probe2.py` — `check_same_thread` 없이 같은 모양의 작은 그래프 → **5/5 `ProgrammingError: SQLite objects created in a thread can only be used in that same thread`**(스레드 번호는 실행마다 다름 — 노트북에 넣지 않고 b7에 「노트북 밖 다섯 번」). `with sqlite3.connect(…) as conn:` 블록 뒤 `conn.execute("SELECT 1")` → `[(1,)]`(닫히지 않음, b7). 모두 `env -u OPENAI_API_KEY`.
- **출력으로 본 것**(결과 읽기·본문 근거): §3의 값 모두.
- **소스로만 본 것**(본문에 「설치판 소스」로 표시): `SqliteSaver` 설명 「lightweight, synchronous use cases (demos and small projects)」(`langgraph/checkpoint/sqlite/__init__.py` 41~44행)·예시의 `check_same_thread=False`와 잠금(62~66행) · `from_conn_string`이 `contextlib.closing`으로 연결을 닫음(92~120행 — 노트북 9절 출력으로도 확인) · `setup()`이 `PRAGMA journal_mode=WAL`과 표 둘을 만듦(122~159행)·`cursor()`에서 스스로 부름(175행) · 그래프가 체크포인트 저장을 뒤에서 도는 실행 흐름에 맡김(`langgraph/pregel/_loop.py` 1199~1202행)·실행이 끝날 때 맡긴 일을 모두 기다림(`langgraph/pregel/_executor.py` 105~107행) · 메시지 번호(`langgraph/graph/message.py` 202~208행).
- **공식 문서**(WebFetch 2026-09-25): Checkpointers — SQLite 체크포인터 「Ideal for experimentation and local workflows」, 패키지 `langgraph-checkpoint-sqlite`(문서 예시는 `SqliteSaver(sqlite3.connect("checkpoint.db"), …)` — `check_same_thread` 없음, 본문에 인용하지 않음) · SQLite `wal.html` 「the changes are appended into a separate WAL file」·「When the last connection to a database closes, that connection does one last checkpoint and then deletes the WAL and its associated shared-memory file」 · Python 3.12 `sqlite3` 「The context manager neither implicitly opens a new transaction nor closes the connection」·`check_same_thread` 설명.
- **이번에 실행하지 않은 것**(본문에 그렇게 적음): 커널·프로그램을 다시 시작해 이어 가기(04절 몫) · 모델 답·도구 메시지가 든 대화 · `check_same_thread`를 뺀 셀(노트북 밖만) · 여러 프로그램이 한 파일을 함께 쓰기 · 오래된 메시지 줄이기 · 표 `writes`의 줄 읽기(05절 몫) · 저장 시점 `durability`(04절) · 걸린 시간 · Windows·macOS.

## 7. 그림

| 그림 | 종류 | 원본 폭(viewBox) | 확인 |
|---|---|---|---|
| 03-1 닫아도 파일에 남는 대화 | `flowchart TB` subgraph 둘 + 파일·결과 상자 | 311(세로 926) | PNG를 보고 도식 읽기와 맞춤(위 칸 첫 객체 → 파일 → 아래 칸 새 객체 → 노란 결과) |
| 03-2 질문마다 쌓인 메시지 | `flowchart TB` 한 줄 상자 다섯 | 256 | 첫 렌더에서 메시지 글이 낱말 가운데서 꺾여 `<br>`로 미리 나눔 |
| 03-3 스레드 이름과 파일 이름 바꿔 보기 | `flowchart TB` + subgraph 셋 + `~~~` 회색 | 791 | 첫 두 렌더 899(868 넘음) → 칸 제목을 「같은 파일 · 같은 스레드」 꼴로, 파일·스레드 이름을 초록 상자로, 답 글을 두 줄로 |
| 03-4 연결을 닫는 두 모양 | `flowchart TB` + subgraph 둘 + `~~~` 회색 | 578 | 회색 상자 라벨을 네 줄로 미리 나눔. 회색 두 사실은 5절 파일 목록·9절 끝 파일 목록에서 각각 확인 |
| 03-5 마지막 사진을 보고 다시 놓은 체스판 | Higgsfield 삽화 | 1100 × 614 | 아래 |

- 색: 연결·파일·입력 초록 · 부른 메서드 파랑 · 출력·받은 오류 노랑 · 체크포인터·그래프·공통 사실 회색 · **빨강 0 · 보라 0**(experiment, 모델 없음). 라벨 숫자(`1번째`·`2번째`·`3번째`·단계 번호 `4`)는 노트북 출력에 있음(G7 통과 + 손 대조), 개수는 한글.
- 삽화: **1차 job `33fe798b-3ff5-4698-9d41-c7f224ec12e2` 채택**(재생성 0회) — 판 위 말 네 개 · 판 앞 즉석사진 한 장(부분 확대로 사진 속 판에도 말 네 개가 같은 모양인 것을 셈) · 닫힌 파란 사진첩 하나(겉모습은 두꺼운 책과 비슷) · 빈 나무 상자 하나 · 카메라·다른 사진·글자 없음. 거래 **09:11:18Z 「Nano Banana Pro −2」 한 줄 = 이 절 2크레딧**(잔액 2441.75 → 2439.75, 바로 앞 08:42:00Z는 02절 몫). 저장 PNG `1a382674…`와 채택 job 결과를 다시 받아 같은 폭으로 줄인 그림의 픽셀 대조 bbox `None`·최대 차이 0. 세부 `figures/03-5-…prompt.md` 「상태」.
- 옛 그림 `figures/03-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 참조 0, 사본 `before/figures/`).

## 8. 서비스 요청과 비용

- 모델·임베딩 요청 **0번**(노트북 A·B, 노트북 밖 확인 모두). 키는 읽지 않음.
- Higgsfield 1회 생성, 2크레딧(§7).

## 9. 챕터 밖 수정

- **없음.** `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json`은 `verify.py --chapter`가 다시 씀(보호 목록 안, `manifest-changes.md`). 공용 도구·규격·과정 요약·계약 파일·Part 목록·묶음·실습 폴더 README·`pyproject.toml`·`uv.lock`·worker 둘 그대로. 새 패키지 설치 0(가상환경 그대로).
- `_build.py`가 01·02·04~06 HTML·`index.html`도 다시 씀 — `_src`·노트북이 그대로라 내용 변화 없음.

## 10. 완료·뒤 챕터가 03에 기대는 문장 (고치지 않음, 참·거짓만)

| 자리 | 문장 | 판정 |
|---|---|---|
| **Ch 22 09 `_src` b8(완료)** | 「Ch23에서는 대화 기록을 프로그램 밖에 저장하고 다시 이어 가는 방법을 다룹니다. 이번 실습에서 종류별로 출력한 대화 기록이 그 대상입니다.」 | **참** — 03이 메시지 칸(`HumanMessage`·`AIMessage`)을 SQLite 파일에 저장하고 새 연결·새 그래프로 이어 감, 메시지를 종류별로 출력. (Ch 22 09 기록에는 도구 메시지도 있었으나 03은 사람·AI 메시지만 — b7 「도구 메시지가 든 대화를 저장해 보지는 않았습니다」) |
| 01 `_src` b4 「대화 기록을 저장해 이어 가는 모습은 03절에서 봅니다」·「프로그램 밖에 남기는 체크포인터는 02절과 03절에서」 | — | **참** |
| 02 `_src` b8 「03절에서는 연결과 그래프 객체를 새로 만들어도, 같은 스레드의 대화를 이어 가는지 봅니다」 · b4 「03절에서 쓸 SQLite 체크포인터는 필요할 때 표를 스스로 만든다」 | — | **참** — 6절 · 4절 `['checkpoints', 'writes']`(`setup()` 부르지 않음) |
| Ch 20 02 b7(04·05·06) · Ch 20 03 b7(01) | 링크 | 03 무관, 슬러그 그대로 |
| Ch 25 01~03 · Ch 26 01~04 b3(대기) | 「Ch23에서 체크포인터와 thread_id가 상태를 저장하는 방법」 | 참(01·03) |
| Ch 27 01 b3(대기) | 「Ch 23의 체크포인터는 실행 상태를 이어 주었고」 | 참(03 6절) |
| **Ch 27 04 b3(대기)** | 「FilesystemBackend의 파일은 체크포인터 메시지와 다른 저장 표면」 | **참** — 03이 메시지를 체크포인터로 SQLite 파일에 저장 |
| **Ch 30 02 b3·`_generate.py` 24행(대기)** | 「Ch21의 Agent와 Ch23의 체크포인터처럼 생성 비용과 수명주기가 다른 객체가 있다는 점도 배웠습니다」 | **반만 참** — 수명은 03이 보임(용어 「객체의 수명」: 연결을 닫자 체크포인터·그래프는 못 쓰고 파일의 체크포인트는 남음, 새 객체로 이어 감). **생성 비용은 재지도 견주지도 않음**(걸린 시간 안 잼) · Agent(Ch 21)와 수명을 견주지 않음 |
| Ch 30 06 b3(대기) | 「Ch23의 thread 분리」 | 참(01·03 7절) |
| Ch 24 01 · Ch 31 02 b3(대기) | 재시작·멱등성·재개 | 04~06 몫 |
| Ch 31 05 b3(대기) | `setup()`이 표를 만든다 | 02로 참(03은 SQLite는 스스로 만든다는 대비만) |

## 11. 강사 확인 대상

1. **「답」 메시지가 코드가 만든 글**(「N번째 질문을 받았습니다」) — 챕터 리드 결정 1(M3). 모델 요청 0, 준비물·2절·b5·b7에 한 문장씩.
2. **코드 줄 36 → 127(셀 5 → 29)** — 늘어난 몫은 메시지 칸 출력·표 확인(3·4절)·닫은 뒤 옛 객체 오류(5절)·값 바꿔 보기 둘(7·8절)·`with` 모양(9절).
3. **`with SqliteSaver.from_conn_string(…)`을 노트북에서 실행**(과정 `open` 밖 `with` 두 번째 〔마감 정정 2026-09-25, 검토 A-13: 과정의 첫째·둘째가 아님 — 앞선 선례는 Ch 2 05 `with open`(A 트랙)·Ch 2 09·11(B 트랙)·**Ch 10 02 `with pdfplumber.open`**(라이브러리 객체, 기본 경로)·Ch 10 04·09 `zipfile.ZipFile`·Ch 21 04 `warnings.catch_warnings`. 03 b3·9절 설명은 Ch 10 02로 고침〕) — 02는 b7 한 줄만 두었음. 03은 「블록이 끝나면 닫는다」를 출력(오류)으로 보이려고 실행.
4. 파일 크기(옛 「4096」)를 결론에서 뺌 — WAL 때문에 연결이 열린 동안 본 파일 크기가 저장된 양과 맞지 않음(b7 한 줄).
5. 메시지 클래스를 `langchain_core.messages`에서 가져옴(Ch 13 04는 `langchain.messages`) — 잠금 그대로 두려고. 설치 셀에 `langchain-core==1.6.2`.
6. meta 시수(강의 1h · 실습 1.5h)·새 용어 3 그대로(말은 바뀜: SQLite 체크포인터·객체의 수명·스레드 재개).

## 12. 남은 것 · 지워야 하지만 지우지 않은 것

- 마감 몫: `chapter.json` `objectives` 첫 줄 「… 저장하고 재개할 수 있습니다」 — 03 「스레드 재개」 뜻과 맞음(대조만) · 옛 그림 셋(`figures/03-흐름.*`) 삭제 승인 · `visual.cjs`·묶음 재생성.
- 삭제 승인 대상(만들었지만 지우지 않음): 기기 **`/tmp/ch23-03/`**(6.8MB — `probe1.py`·`probe2.py`·`A.ipynb`·`B.ipynb`·`cmpout.py`·`texthash.py`·`extra_check.py`·`ban_check.py`·`pixcmp.py`·`reps1.json`·`illu-1-orig.png` 3.4MB·`illu-1-again.png`) · 기기 세션 임시 폴더 **`$TMPDIR/ch23-03-*` 29개**(1.6MB — 노트북 A·B가 만든 `ch23-03-…` 둘(각 `chat.sqlite`·`other.sqlite`), 탐색 `ch23-03-probe-…` 21·`ch23-03-probe2-…` 5·`ch23-03-with-…` 1; 연결 폴더 밖) · `.cache/ch23-03-view/`(PNG 여섯 — Mermaid 넷 사본·`illu-1-1100.png`·`illu-1-crop-photo.png`) · `qa/upgrade/gates-wip-03-03.json`·`gates-wip-03.json`(마감 `gates-after.json`으로 갈음) · `qa/upgrade/__pycache__/`(생성기를 모듈로 읽어 새로 생긴 `author_03` 캐시 포함).

## 마감 반영 (2026-09-25, 검토 1차 `review-round1-A.md`·`review-round1-B.md`)

- **A-12** 가져오기 설명 — 「메시지 클래스 셋은 Ch 13 04절과 같지만, 이 절은 클래스가 원래 들어 있는 langchain-core에서 가져옵니다」 + 「메시지 리듀서 `add_messages`는 그 절처럼 langgraph에서 가져옵니다」.
- **A-13** `with` 선례 — b3에 Ch 10 02절(라이브러리 객체 `pdfplumber.open`, 링크 `L_CH10_02` 상수를 생성기에 더함)·Ch 21 04절(경고 목록), 노트북 9절 설명은 「Ch 2 05절에서 파일을, Ch 10 02절에서 라이브러리 객체를」. 이 진단 18·112행과 `handoff.md` 두 곳의 「과정 두 번째」에는 정정 표시를 붙임(사실: Ch 2 05·09·11·Ch 10 02·04·09·Ch 21 04가 앞섬).
- **A-14** 「파일을 처음 쓸 때」 → 「처음 읽거나 쓸 때」. **A-15** 3절 설명에 「인자 이름의 thread는 이 챕터의 스레드(`thread_id`)가 아니라, 한 프로그램 안에서 따로 도는 일의 줄(실행 흐름)을 가리킵니다」(단락을 둘로 나눔) · b7에 실행 흐름 풀이와 같은 구분 한 문장. **A-16** 용어 표 「스레드 재개(resume)」에서 영어 괄호를 빼고 「Ch 24에서 사람의 확인을 받아 멈춘 실행을 다시 움직이는 일과는 다른 장면입니다」. **A-17** 3절 「02절의 비유를 이어 쓰면, …」. **A-18** 「Ch 22 09절에서는 `message.type`으로 종류를 찍었고, 이 절은 01절처럼 클래스 이름으로 …」(Ch 22 09 b8은 고치지 않음 — 챕터 요약 인계).
- **다시 실행하지 않음** — `code_sha256` `fe89a30aec83…`·`outputs_sha256` `952dc36685ea…`·`executed_at` 09:08:56Z 그대로(파일 `ab7333da9124…` → `bc54df7e3f36…`). 생성기 `08789d914238…` → `1af0c606f025…`(61/61·`_src` 같음). 게이트 0(검사 문장 360 → 364).
