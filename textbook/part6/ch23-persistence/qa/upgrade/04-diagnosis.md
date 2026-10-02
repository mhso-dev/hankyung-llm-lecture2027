# 04절 진단과 개선 기록 — 내구 실행 모드 비교 (experiment)

- 대상: `_src/04-내구-실행-모드-비교.html` · `labs/part6/ch23-persistence/notebooks/04-내구-실행-모드-비교.ipynb` · **worker 스크립트 `labs/part6/ch23-persistence/durability_worker.py`(다시 씀)** · 그림 `figures/04-1`~`04-5`.
- 생성기: `qa/upgrade/author_04.py`(worker 글 `WORKER` + 노트북 + `_src`, 01 생성기에서 `html_text`·`table_html`·임시 폴더 셀을 가져오고 폴더 셀은 앞머리만 다른지 `assert`, `11e5dba8f69c2eb8eb12218ab921aa1802580361923d0a3ac7d30127a21d8830`) · `_src` `ab869ad4c20e…` · 빌드 HTML `7c17568644ee…` · 노트북 파일 `be38374b8616…` · worker `c60467bdd82d40792148b2afad0471a98a8219ac6de48f10b104578be14491de`(노트북 밖 확인에 쓴 사본 `/tmp/ch23-04/durability_worker.py`와 `cmp` 같음). 그림 설계표 `qa/upgrade/04-figures.md`. 흔들림 확인 `qa/upgrade/04-probe.md`(규칙을 먼저 적고 실행). 검토 묶음 `qa/upgrade/review-pack/04-내구-실행-모드-비교.md`.
- 작업일 2026-09-25(UTC 09:2x~10:0x). 형식 **experiment 유지**, **슬러그·제목 그대로**(Ch 20 02 b7 링크). meta 「강의 1h · 실습 2h · 새 용어 4」 그대로(말은 바뀜: 저장 시점·자식 프로세스·강제 종료·신호 파일).
- **모델 요청 0번**(노트북·노트북 밖 모두, 챕터 리드 결정 1). 키 셀 없음. 자식 프로세스는 노트북 한 번에 19번 띄우고 17번 강제 종료(노트북 밖 확인 85회 — 회마다 첫 실행·다시 실행 두 번, 자식 프로세스 170번).

## 1. 게이트 전후

| | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전 (`gates-before.json`) | 6 | 83 | 7 | 3 | 0 | 0 | 4 | 27 | 3 | **44** |
| 첫 실행 전 (`gates-wip-04-04.json` 첫 판, 노트북·`_src`만 쓴 판) | 28 | — | 0 | 0 | 0 | 0 | 0 | 4 → 1 → 0 | 18 | — |
| 후 (`gates-wip-04.json`) | **28** | **372**(〔마감 정정, 검토 B-6: 기록 파일은 373〕) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 첫 검사: G1 **0**, G2 **0** · G6 **4**(70자 넘는 문장 넷 — b8 다음 절 문장·복습 3 해설·b10 참고 자료 둘) → 나누거나 줄인 뒤 G6 1(`async`로 시작해 조사가 붙은 문장 — 「값 `async`의」로 고침) → **0**으로 만든 뒤 첫 실행. G7 18은 그림 파일·설계표가 없던 때.
- 그림을 넣은 뒤 `--no-exec` 두 번(그림·삽화 반영 · b7 두 줄 손질 뒤) 모두 **G1~G7 0**, `verify.py --chapter` **`PASS 6 sections / 123 code cells (max 23 lines)`**(최대 23줄은 개선 전 05·06). 빌드 HTML `{{`·`[[` 0건, SVG 넷·삽화 JPEG 하나 인라인.
- AST 따로(`/tmp/ch23-04/extra_check.py` — 03 판 복사): **노트북·worker 모두 금지 문법 0건**. 허용 표시로 따로 나온 것 1 = 마지막 셀 `sorted(os.listdir())`(키워드 없음 — 03 판과 같은 모양). 클래스는 칸만 적은 `StepState(TypedDict)`(노트북 1·worker 1), 함수 힌트·반환 힌트·데코레이터·f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`.get`·`+=`·기본값·튜플 풀기·한 줄 다중 대입·별표 풀기·`is`·`try`·`with`(open 밖)·`from __future__`·세미콜론 0. 셀 모양(`/tmp/ch23-04/shape.py`): 준비 셀이 아닌 셀 주석 뺀 코드 최대 **9줄**, 함수 본문 최대 **8줄**(`read_saved`·`kill_at_second`), 셀당 정의 하나, 첫 줄 주석 100%. worker 함수 본문 2·2·6줄.
- 금지어(`/tmp/ch23-04/ban_check.py` — 03 판 그대로): 노트북·`_src`·캡션 다섯·`.mmd` 넷·worker에서 참 금지어 **0건**(걸린 16건은 모두 「프로그램」 안 「로그」). 「모드」·「내구」·「지연」은 제목·슬러그·링크 주소(`05-로컬-트레이싱과-지연.html`)에만.
- 코드 줄(`count_code.py`) 48 → **147**(셀 6 → 28, 준비 셀 넷). 늘어난 몫은 2절 끝까지 실행 장면(상태 형식·노드 둘·설계 객체·체크포인터·세 값 실행)·3절 함수 다섯·4·5절 장면 다섯 셀씩·6절 되풀이.

## 2. 수정 전 주요 문제 (준비 노트 §1·§2 04·§7, 인계 §03 → §04)

1. **셀 여섯**: 경로 셀 `[Path.cwd(), *…parents]`·`next(…)` 제너레이터 둘·한 글자 `p` 둘 · `read_saved(db_path: Path, mode: str) -> dict | None`(힌트·조건 표현식 둘·`with sqlite3.connect` — **연결을 닫지 않음**, 03에서 확인) · `kill_and_resume(mode)` **17줄**(f-string·`unlink`·`time.time()` 기한 루프·`Popen`·`kill`·`wait`·`subprocess.run(…, check=True)`) · 내포식 `observations = [… for mode in …]`·`all(…)`·`.get` · f-string 형식 지정 `{row['mode']:5}`.
2. **파일 쓰기**: 실습 폴더 `data/durability/{모드}.{sqlite,ready,trace}` — 학생 폴더에 남고, 이 작업 기기의 연결 폴더에서는 SQLite 쓰기가 `disk I/O error`(준비 노트 §5-5).
3. **worker 스크립트**(학생이 여는 파일): `from __future__ import annotations` · 한 줄 다중 대입 `db_path, ready_path, mode = …` · 조건 표현식 둘(`phase = … if … else …`·`graph_input = … if … else None`) · 반환 힌트 · 영어 독스트링 · `with sqlite3.connect` · `resume` 단계에서 `exit`만 입력을 다시 넣는 조건(저장 여부가 아니라 모드 이름으로 가름).
4. **결론이 흔들린 값에 기댐**: 옛 출력 「이번 실행의 `async`와 `sync`는 `completed=['first']`를 보존」 — 준비 확인 60번 중 4번은 `async`가 `first`를 잃음(준비 노트 §7-1). b8 정리 둘째 줄이 async 값을 결론으로 씀.
5. **재지 않은 시간**: b2 「다음 노드가 기다리는 시간이 늘어날 수 있습니다」 · b4 「지연을 줄일 수 있지만」 · b5 「비동기 저장의 지연 이점」·「저장소 지연」 — 시간을 재는 코드 없음(규격 §3). 로컬 SQLite에서 재 보면 `async`·`sync` 차이가 보이지 않음(준비 노트 §7-3).
6. **말**: 「SQLiteSaver」(틀린 이름) · 「내구성(durability)」 · 「경합」·「보장」·「정확히 한 번」·「병렬」·「측정」·「로그」·「내부」·「운영체제 수준」 · 영문 시작 문장 다수(`sync는`·`first 노드가`) · 기본값 `async`를 말하지 않음 · b10 여섯 절 공통 참고 자료(Interrupts·Time Travel), durability 문서 빠짐.
7. **노트북 설명**: 제목 셀·「이 노트북에서 할 일」·준비물·그림 첨부·결과 읽기 0, 설명 셀은 `_src` 문장 복사. 그림은 옛 `{{svg:04-흐름}}` 한 장.

## 3. 바꾼 것

- **강제 종료 장면 유지(챕터 리드 결정 4)**: 3절 함수 넷 — `start_worker(worker_path, files, mode, phase)`(`subprocess.Popen([sys.executable, worker_path, 파일 이름 셋, mode, phase])`) · `wait_for_signal(signal_name, limit_seconds)`(`time.perf_counter()` 기한 루프 + `os.path.exists` + `time.sleep(0.05)`) · `stop_worker(process)`(`kill()` → `wait(timeout=5)` → 종료 코드) · `read_saved(graph_builder, sqlite_name, thread_name)`(새 연결·새 `SqliteSaver`·설계 객체로 컴파일 → `get_state`·`get_state_history` → `close()` → 한국어 키 딕셔너리) · `read_record(record_name)`(`with open` → `split()`) — 모두 **인자로만** 받음(노트북 전역 값에 기대지 않음). 4절 `exit`·5절 `sync` 장면은 같은 모양 다섯 셀(띄우기·신호 → 끊기·종료 코드·기록 → 새 연결로 읽기 → 다시 실행(`resume` 단계, `wait(timeout=30)`) → 다시 읽기·기록). 6절 `kill_at_second(worker_path, graph_builder, name_prefix, mode)`(앞 넷을 부름, 신호 결과와 상관없이 먼저 끊고 `assert`)로 세 값 × 다섯 번.
- **worker 스크립트 다시 씀**(도구 파일 규칙 — 금지 문법 0·한국어 주석): 인자 다섯(SQLite·신호·기록 파일 이름 — **모두 임시 폴더 안 이름**, 저장 시점, 단계 `first-run`/`resume`), 상태 형식 `StepState`(칸 `completed`, `operator.add`) · 노드 `first`·`second`(기록 파일에 이름 한 줄 — 여는 방식 `"a"`, 둘째 노드는 신호 파일을 만들고 첫 실행 단계에서만 30초 쉼) · 연결 `sqlite3.connect(…, check_same_thread=False)` + `close()`(03 모양) · **다시 실행 단계는 저장된 다음 노드가 있으면 `invoke(None, config, durability=mode)`, 없으면 처음 입력** — 옛 판의 「`exit`만 입력을 다시 넣는」 조건 대신 저장 여부로 가름. 자리·이름 그대로라 묶음 목록 두 곳 변경 0(`textbook/part6/public-files.json` 27행·챕터 `qa/public-files.json`에 이미 있음).
- **자리 찾기와 임시 폴더(챕터 결정 2)**: 준비 셀 넷 = 설치(`langgraph==1.2.11`·`langgraph-checkpoint-sqlite==3.0.3`, 잠금 판) → 가져오기(`subprocess`·`sys`·`time` — 이 챕터 처음, 과정은 Ch 2 08·Ch 15 05·Ch 16 05) → **자리 찾기**(Ch 17 05 모양 `candidates = [".", "../../..", "../../../.."]` + `for`·`break`, `os.path.abspath`로 절대 자리 — 자리 글은 출력하지 않음) → 임시 폴더(01 셀 앞머리만 `ch23-04-`, 생성기 `assert`). 자식 프로세스는 부모의 작업 폴더를 물려받아 같은 임시 폴더에 씀(마지막 셀 파일 수 52로 확인). 실습 폴더 `data/`는 만들지 않음.
- **2절 끝까지 실행 장면(보조, 결정적)**: 같은 두 노드 그래프를 `steps.sqlite`에 붙여 `exit`·`async`·`sync`로 끝까지 → 체크포인트 **1·4·4**. 옛 판에 없던 장면 — 「끝까지 가면 `async`=`sync`, 차이는 끊길 때만」을 출력으로 세움. 준비 노트 §7-2 (a)의 「둘째 노드 안에서 센 체크포인트 수(exit 0·sync 3)」는 **끊긴 뒤 새 연결로 센 수(exit 0·sync 3)**로 보였습니다 — 둘째 노드가 쉬는 동안에는 더 쓰는 것이 없어 같은 값이고(노트북 밖 20/20씩), 노드 함수가 전역 체크포인터나 닫힌 함수에 기대지 않아도 됩니다.
- **결론은 결정적 값만**: 정리·그림 라벨·캡션·복습·b6 표에 `exit`·`sync`(끝까지 1·4, 끊긴 뒤 0·3, 다음 노드 `()`·`('second',)`, 다시 실행한 노드 차례, 되풀이 0/5·5/5)와 끝까지 실행한 `async` 4만. **`async` 강제 종료 결과는 6절 결과 읽기 둘째 단락과 b7에만**(아래 §4).
- **걸린 시간**: 재지 않음. 옛 「지연」 문장 셋 뺌. b4 「다른 상황에 적용」은 공식 문서 문장(`exit` 「best performance for long-running graphs」·`sync` 「at the cost of some performance overhead」)만 옮기고 「걸린 시간은 이번에 재지 않았습니다」. 준비물 「30초 안에」는 A 셀 실행 기록(09:44:13.41 → 09:44:24.63, 약 11.2초)을 넉넉히 둔 값.
- **새 말 넷**(meta 「새 용어 4」 그대로): 저장 시점(durability) · 자식 프로세스 · 강제 종료 · 신호 파일 — 세 문장(뜻 → 비유 → 이 절 코드). 「내구」는 제목에만, 본문은 「저장 시점」(b2 「이 절의 제목이 가리키는 것은 … `durability`의 값 셋」). 처음 쓰는 이름 한 문장씩: `subprocess.Popen`(Ch 2 08 `subprocess.run`과 견줌) · `kill()`(Python 설명서 — POSIX는 신호 9) · `wait(timeout=)`(종료 코드, 음수 `-N` = 신호 N) · `time.perf_counter()` 기한(Ch 15 05) · `os.path.abspath` · 여는 방식 `"a"`(worker 주석) · `sys.argv`(worker 주석) · `invoke(None, …)`(4절 설명 셀 한 문장 — 노트북 셀에서는 부르지 않음, b7).
- **본문 10블록 다시 씀**: b3 Ch 2 08·Ch 15 05·Ch 16 05·Ch 17 05·Ch 13 02·01·03 링크 · b4 비유(사진을 찍는 때가 다른 세 사람 + 엎어진 판) + 삽화 + 용어 표 + 「저장 시점마다 저장하는 때」(소스 행 넷)·「다른 상황에 적용」·「비교와 경계」(03 ↔ 04, 05·06 몫) · b6 표 · b7 여덟 줄 · b10 문서 둘·소스 행.

## 4. 새 커널 두 번 (규격 §2-7 9번 끝)

- A `run_section.sh`(셀 실행 기록 09:44:13.41~09:44:24.63Z) — **`PASS 04-내구-실행-모드-비교.ipynb: 28 cells`**. 그림 파일이 아직 없어 `attach_figures.py`에서 멈춤(과제 차례대로 그림 전에 두 번 실행).
- B 사본 `/tmp/ch23-04/B.ipynb`를 `execute.py`로(`UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch23-persistence UV_NO_SYNC=1 PYTHONPATH=…/notebooks`) — `PASS`. 두 실행 모두 빈 임시 폴더에서 시작(폴더 이름은 실행마다 다르고 출력하지 않음).
- 셀별 출력 글자 대조(`/tmp/ch23-04/cmpout.py`) **27/28 같음**. 다른 한 셀은 **6절 되풀이 셀의 `async` 줄뿐** — A `async | 4 | 5` ↔ B `async | 5 | 5`(같은 셀의 `exit | 0 | 5`·`sync | 5 | 5`와 라벨 줄은 같음). 셀별 출력 글자 해시(`/tmp/ch23-04/texthash.py`) A `e6dea0cc185d…` · B `04d21e195c37…`(그 한 줄 때문). `code_sha256` **`ff4e48c4a73168dd088340e6d324768a1aec03a145c7fda4f8c13b0f966a641e`**, 교재 노트북은 A(`outputs_sha256` `845cda331722…`).
- 처리: `async` 값은 6절 결과 읽기 **둘째 단락**(「이번 실행에서는 다섯 번 가운데 4번 … 새 커널로 한 번 더 실행했을 때는 다섯 번 모두」)과 b7에만. 첫 단락·정리·그림·캡션·복습·b6 표에는 없음. b6 셋째 단락은 「두 실행에서 달랐던 것은 6절 되풀이 셀의 `async` 줄 하나뿐」(값 없이). 흔들림은 입력을 고칠 일이 아니라 이 절이 보이려는 성질(공식 문서 「small risk … if the process crashes」)이라 다시 돌려 고르지 않았습니다(규격 §2-7 10번 — 원하는 값이 나올 때까지 돌리지 않음).
- 뒤이은 `mdpatch.py`(`[[READ_ASYNC]]` 두 곳, `/tmp/ch23-04/reps1.json`)·오늘 볼 그림 셀 alt·읽기 채우기·`author_04.py --src-only`·`attach_figures.py`는 마크다운만 바꿈 — 노트북의 `code_sha256`·`outputs_sha256`·`executed_at`(09:44:24Z) 그대로, A 사본과 셀별 출력 28/28 같음, 생성기 `cells()`와 노트북 셀 원본 59/59 같음.
- 남은 자식 프로세스: A·B 실행 뒤와 노트북 밖 확인 묶음마다 `ps -eo pid,args`에서 `python … durability_worker` 줄 **0**(`pgrep -f`는 이 셸 명령 자체가 걸려 거짓 양성 — `ps`+`awk`로 바꿈).

## 5. 도구 파일 — 만들지 않음 (챕터 공통 5·과제 결정)

- 04는 강제 종료 함수를 **처음 가르친 절**이라 노트북에 둠: `start_worker`·`wait_for_signal`·`stop_worker`·`read_saved`·`read_record`·`kill_at_second`(본문은 인계 `§04 → §05` 8항에 글자 그대로). 06·07이 처음 가져올 때 `notebooks/checkpoint_tools.py`를 만들고 묶음 목록 둘에 더함.
- 01 `print_history`·`thread_row`, 03 `print_conversation`·`sqlite_tables`는 쓰지 않음(칸·출력 모양이 다름). 그래서 묶음 목록(`textbook/part6/public-files.json`·챕터 `qa/public-files.json`) 변경 0.

## 6. 설치판 동작과 문서 (모델 없는 확인, 2026-09-25)

- **노트북 밖 확인**(`04-probe.md`, 규칙 먼저): 고친 worker로 강제 종료 `exit` 20 · `sync` 20 · `async` 40, 끝까지 실행 세 값 × 20. **`exit`·`sync`는 모두 20/20 같음**(끊긴 뒤 `{}`·`()`·0 ↔ `{'completed': ['first']}`·`('second',)`·3, 다시 실행 기록 `first, second, first, second` ↔ `first, second, second`, 체크포인트 1 ↔ 4, 종료 코드 `-9`) · 끝까지 실행 1·4·4 20/20 · **`async` 강제 종료 40/40 `first` 남음**(준비 조사 옛 worker 60번 중 4번 잃음). 노트북 A에서는 `async` 다섯 번 중 한 번 잃음 — 셋을 합쳐 「끊는 때에 따라 남기도 하고 잃기도 한다」로만 씀.
- **출력으로 본 것**: §3의 값 모두.
- **소스로만 본 것**(본문에 「설치판 소스」로 표시): `langgraph/types.py` 89~95행(세 값 설명) · `langgraph/pregel/main.py` 2602~2603행(기본값 `async`)·3866행(`invoke` 설명 「defaults to "async"」)·2987~2988행(`sync`가 단계마다 `_put_checkpoint_fut.result()`) · `langgraph/pregel/_loop.py` 1132~1135행(`exit`는 나갈 때만 체크포인트)·1199~1202행(저장을 뒤에 맡김)·1324~1333행(`exit`는 오류·중단으로 나갈 때도 저장 — **노트북에서 실행하지 않음, 05절 몫**)·466행(`exit` 밖은 작업마다 쓰기 저장) · `langgraph/pregel/_executor.py` 105~107행(끝날 때 맡긴 일을 모두 기다림).
- **공식 문서**(WebFetch 2026-09-25): Checkpointers 「Durability modes」 — 「from least to most durable」·`exit` 「persists changes only when graph execution exits — successfully, with an error, or due to a human-in-the-loop interrupt」·「best performance for long-running graphs but … you cannot recover from system failures (like process crashes) mid-execution」·`async` 「there is a small risk that LangGraph does not write checkpoints if the process crashes during execution」·`sync` 「high durability at the cost of some performance overhead」(기본값은 이 문서에 적혀 있지 않음 — 본문은 소스로만). Durability reference 페이지는 형식 정의(`Literal['sync', 'async', 'exit']`)뿐이라 b10에서 뺌. Durable execution 문서(`…/durable-execution`)는 이번에도 저장 시점 절이 없어 인용하지 않음. Python 3.12 subprocess — `Popen` 「Execute a child program in a new process」·`kill()` 「On POSIX OSs the function sends SIGKILL … On Windows kill() is an alias for terminate()」·`wait` 「If the process does not terminate after timeout seconds, raise a TimeoutExpired」·`returncode` 「A negative value -N indicates that the child was terminated by signal N (POSIX only)」.
- **이번에 실행하지 않은 것**(본문에 그렇게 적음): 노드 안 오류로 멈춘 실행(05) · 노트북 셀의 `invoke(None, config)`(스크립트 안에서만) · 셀을 도중에 멈춘 경우 · 걸린 시간 · Windows·macOS · 여러 프로그램이 한 파일을 함께 쓰기 · 다시 실행한 노드의 바깥 쓰기를 한 번만 반영(06).

## 7. 그림

| 그림 | 종류 | 원본 폭(viewBox) | 확인 |
|---|---|---|---|
| 04-1 저장 시점 셋과 체크포인트 수 | `flowchart TB` subgraph 셋 + `~~~` 회색 | 836(첫 렌더 934) | PNG를 보고 도식 읽기와 맞춤(회색 저장하는 때 → 노란 체크포인트 수, 공통 회색은 2절 세 줄에서 확인) |
| 04-2 둘째 노드에서 끊고 다시 실행하는 차례 | `flowchart TB` 한 줄 상자 여섯 | 274(세로 723) | 둘째 상자 낱말 꺾임을 `<br>`로 미리 나눔. 노트북 「오늘 볼 그림」 |
| 04-3 다시 실행 단계가 고르는 두 갈래 | `flowchart TB`, 점선 두 갈래(라벨 있음) | 478 | 도식 읽기는 좌우 대신 갈래 라벨로 가리킴 |
| 04-4 끊긴 뒤 남은 것 exit와 sync | `flowchart TB` subgraph 둘(칸 안 `~~~`) + `~~~` 회색 | 547 | 개수는 한글(「체크포인트 없음」·「모두 first를 잃음/가 남음」) |
| 04-5 엎어진 두 판과 남은 사진 | Higgsfield 삽화 | 1100 × 614 | 아래 |

- 색: 우리 코드(노트북 함수·worker) 파랑 · 출력 노랑 · 설치판 소스 사실·칸 공통 사실 회색 · **빨강 0**(experiment — 강제 종료는 우리가 일부러 만든 장면, 잃은 체크포인트도 출력으로 본 값) · **보라 0**(모델 없음) · 초록 0(파일·값을 따로 상자로 두지 않음). **`async` 강제 종료 값은 그림에 없음.** 라벨 숫자 `30`·`-9`만(모두 출력·본문에 있음).
- 삽화: **1차 job `ec7db33b-866a-4529-b5d8-e5487a00baad` 채택**(재생성 0회) — 나무 탁자 둘에 쓰러진 체스판 둘·옆으로 누운 말 · 왼쪽 판 앞 즉석사진 **세 장 한 줄**(사진마다 작은 판) · 오른쪽 사진 없음 · 탁자마다 즉석카메라 하나 · 글자·숫자·사람·손·사진첩 없음. 거래 **09:48:29Z 「Nano Banana Pro −2」 한 줄 = 이 절 2크레딧**(잔액 2439.75 → 2437.75, 바로 앞 09:11:18Z는 03절 몫). 원본 `8f129a0c…`(2752 × 1536) → 저장 PNG `29a24868…`, 결과 URL을 한 번 더 받아 같은 폭으로 줄인 그림과 픽셀 대조 bbox `None`·최대 차이 0. 세부 `figures/04-5-…prompt.md` 「상태」.
- 옛 그림 `figures/04-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 참조 0, 사본 `before/figures/`).

## 8. 서비스 요청과 비용

- 모델·임베딩 요청 **0번**(노트북 A·B, 노트북 밖 확인 모두). 키는 읽지 않음(노트북 밖 확인은 `env -u OPENAI_API_KEY`).
- Higgsfield 1회 생성, 2크레딧(§7).

## 9. 챕터 밖 수정

- **없음.** `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json`은 `verify.py --chapter`가 다시 씀(보호 목록 안, `manifest-changes.md`). 공용 도구·규격·과정 요약·계약 파일·Part 목록·묶음·실습 폴더 README·`pyproject.toml`·`uv.lock`·`idempotency_worker.py` 그대로. 새 패키지 설치 0.
- 챕터 안 보호 파일 중 새로 바꾼 것: **`labs/part6/ch23-persistence/durability_worker.py`**(`ce6fb8c56770…` → `c60467bd…` — 이 절이 쓰는 스크립트, 인계 §03 → §04 3항 「04가 정함」) · 04 노트북 · `qa/verification.md`(04 행).
- **`part6-practice.zip`은 다시 만들지 않음**(마감 몫) — 지금 묶음 안 worker·04 노트북은 옛 판(`3755de3d…` 그대로). 노트북과 worker는 짝이라(인자 다섯·`first-run`/`resume`) 마감에서 반드시 함께 다시 묶어야 함.
- `_build.py`가 01~03·05·06 HTML·`index.html`도 다시 씀 — `_src`·노트북이 그대로라 내용 변화 없음(01 `d2581c77…`·03 `7e2c3dc1…` 앞 절 기록과 같음, `index.html`은 `before/index.html`과 바이트까지 같음).

## 10. 완료·뒤 챕터가 04에 기대는 문장 (고치지 않음, 참·거짓만)

| 자리 | 문장 | 판정 |
|---|---|---|
| **Ch 20 02 `_src` b7(완료)** | 「멈춘 실행을 다시 이어 가는 방법은 Ch 23 04절(강제 종료 뒤)과 05절(실패한 단계)에서 다룹니다」 | **04 쪽 참** — 자식 프로세스를 강제로 끝낸 뒤 새 프로세스가 같은 파일·스레드에서 `sync`는 둘째 노드부터 이어 감(4·5절 출력). 슬러그 그대로 |
| 01 `_src` b3·b7 | 「멈춘 실행을 저장된 자리부터 이어 가는 일은 04절과 05절」·「저장 시점을 고르는 일은 04절」 | **참** |
| 03 `_src` b4·b8·노트북 정리 | 「새로 시작한 프로그램에서 이어 가는 모습은 04절에서 봅니다」·「04절에서는 저장하는 때를 바꿔 가며, 프로그램을 강제로 끝낸 뒤 무엇이 남는지 봅니다」 | **참** |
| Ch 31 02 b3(대기) | 「Ch23에서는 중단 뒤 재개와 멱등성을 배웠습니다」 | 중단 뒤 재개는 04로 참(멱등성은 06 몫) |
| Ch 30 02 b3(대기) | 「Ch23의 체크포인터처럼 생성 비용과 수명주기가 다른 객체」 | 03 판정 그대로 **반만 참** — 04도 걸린 시간·생성 비용을 재지 않음 |
| Ch 24 01 b3(대기) | 「노드는 장애 뒤 처음부터 재시작될 수 있고 외부 쓰기에는 멱등성이 필요」 | 04가 뒷받침(`exit`는 첫째 노드부터 다시, `sync`도 끊긴 `second`의 기록 쓰기가 두 번) — 본 판정은 06 몫 |
| Part 6 소개·continuity-guide(대기·기록) | 「Ch23 체크포인터와 프로세스 중단 후 복구」 | 참(04) |
| `grep -rn 'durability\|내구 실행' textbook/part6 textbook/part7`(Ch 23 밖) | `part6/index.html` 목차 제목 · `part6/qa/` 옛 기록(`ch23-technical-review.md`·`language/originals`·`ch23-final.md`) | 문장 기대 없음 — 목차 제목은 그대로 참, 옛 기록은 기록물이라 고치지 않음 |

## 11. 강사 확인 대상

1. **worker 스크립트를 다시 씀**(인자 다섯·다시 실행 단계가 저장 여부로 가름·기록 파일·한국어 주석). 학생 묶음에 들어가는 파일이라 마감 때 묶음 재생성 필요.
2. **`async` 강제 종료 결과가 교재 출력에서 다섯 번 중 한 번 잃음**(B는 다섯 번 모두 남음) — 결론에서 빼고 둘째 단락·b7에만. 이 흔들림 자체가 공식 문서 문장과 맞는 관찰.
3. 코드 줄 48 → 147(셀 6 → 28) · 자식 프로세스 19번(노트북 약 11초).
4. 옛 「지연」 문장 셋·「보장」류를 뺌 — 걸린 시간은 재지 않음(공식 문서 문장만 인용).
5. meta 시수(강의 1h · 실습 2h)·새 용어 4 그대로(말은 바뀜).
6. `kill()`·종료 코드 `-9`는 Linux 출력 — Windows·macOS는 실행하지 않음(Windows에서 `kill()` = `terminate()`).

## 12. 남은 것 · 지워야 하지만 지우지 않은 것

- 마감 몫: `part6-practice.zip` 재생성(worker·04 노트북 짝) · 실습 폴더 README(04 문장 「제공된 자식 프로세스를 실제로 종료」는 참, 파일이 임시 폴더에 생긴다는 문장 추가) · 옛 그림 셋(`figures/04-흐름.*`) 삭제 승인 · `visual.cjs` · `chapter.json` `objectives` 둘째 줄 「내구 실행 모드별 장애 복구 범위를 비교」 대조(맞음).
- 삭제 승인 대상(만들었지만 지우지 않음): 기기 **`/tmp/ch23-04/`**(11MB — `A.ipynb`·`B.ipynb`·`durability_worker.py` 사본·`probe_kill.py`·`probe_run.py`·`probe-exit-sync.txt`·`probe-async.txt`·`probe-exit/`·`probe-sync/`·`probe-async/`(SQLite·신호·기록 파일 85벌 — 연기 확인 5 + 규칙 확인 80)·`probe-run/`(SQLite 20)·`cmpout.py`·`texthash.py`·`extra_check.py`·`ban_check.py`·`shape.py`·`pixcmp.py`·`resize.py`·`figtext.py`·`reps1.json`·`illu-1-orig.png`·`illu-1-again.png`·`__pycache__/`) · 기기 세션 임시 폴더 **`$TMPDIR/ch23-04-*` 둘**(각 508KB·파일 52 — 노트북 A·B가 만든 폴더, 연결 폴더 밖) · `.cache/ch23-04-view/`(PNG 다섯 — Mermaid 넷 사본·`illu-1-1100.png`) · `qa/upgrade/gates-wip-04-04.json`·`gates-wip-04.json`·**`gates-wip.json`**(챕터 전체 검사 한 번 — 이 절 작업 중 새로 생김) · `qa/upgrade/__pycache__/`(`author_04` 캐시).

## 마감 반영 (2026-09-25, 검토 1차 `review-round1-A.md`·`review-round1-B.md`)

- **B-1 [상] 고침(챕터 리드 결정)**: 4·5절의 띄우기 셀과 끊기 셀을 **한 셀**로 합침(`start_worker` → `wait_for_signal` → `stop_worker` → 출력 셋 → `assert` 둘: 신호가 왔는지·종료 코드가 0이 아닌지 — Linux `-9`, Windows `1` 모두 통과). 도구 파일의 `kill_then_resume`은 06절 함수라 04가 쓸 수 없고, 04가 가르친 함수를 한 셀에서 조합함. 코드 줄 12(주석 뺌).
- **B-2(04 몫)**: 3절 끝에 새 함수 **`new_prefix(name)`**(이름 뒤에 번호 — 작업 폴더에 `이름-번호.sqlite`가 있으면 번호를 올림, `while`·`os.path.exists`·`str`·`+`만, 본문 4줄)를 가르치고, 4·5절 끊는 셀과 6절 되풀이 셀이 실행마다 새 앞머리를 고름(`exit-1`·`sync-1`, 6절은 `exit-2~6`·`sync-2~6`·`async-1~5`). 마지막 셀은 `exit.sqlite` 대신 `exit_files`의 이름(`4절 SQLite 파일 이름: exit-1.sqlite`)을 봄. 도구 파일에 옮김(06 생성기 `TOOL_PARTS`).
- **셀을 다시 실행해도 같은지(노트북 밖 확인 `/tmp/ch23-close/rerun_probe.py`)**: 새 커널로 끝까지 실행한 뒤 4절 네 셀·5절 네 셀·6절 되풀이 셀을 한 번 더 실행 → **4/4 · 4/4 · 1/1 출력 같음**(06: 4/4·4/4·1/1, 07: 설정 셀부터 다시 — 앞머리 번호 줄 말고 같음).
- **B-3** 4절 결과 읽기 둘째 단락과 b7에 「설치판 Python 소스에서 Windows의 `kill()`(`terminate()`)은 종료 코드 1로 끝냄 — Windows에서는 1, 실행하지 않음」(`subprocess.py` 1667~1682행). **B-4** b2 「프로세스(실행 중인 프로그램)」·용어 표 자식 프로세스 「실행 중인 프로그램(프로세스)이 띄운 …」·노트북 3절 같은 풀이. **B-5** meta `강의 1h | 실습 2h`. **B-6** 이 진단 §1 검사 문장 372에 정정 표시(기록 파일 373).
- 그림: **04-2 `.mmd`를 고쳐 `--force` 다시 렌더** — 위 네 상자(start_worker·자식 프로세스·wait_for_signal·stop_worker)를 회색 테두리 칸 「4·5절 셀 하나」로 묶음(원본 폭 274 → 318, 세로 874). alt·캡션(「한 셀에서」)·도식 읽기(「회색 테두리 칸 안의 네 상자는 4·5절에서 한 셀로 실행하고, 신호 파일이 생기면 바로 끊습니다. 그래서 끊는 자리는 늘 둘째 노드가 쉬는 동안입니다.」)·`04-2-….caption.md`를 맞춤. PNG를 직접 보고 확인(`.cache/ch23-close/view/04-2.png`). 노트북 「오늘 볼 그림」 첨부도 새 PNG.
- 준비물(노트북)·b7에 다시 실행 안내(「4~6절의 끊는 셀은 실행할 때마다 새 파일을 써서, 다시 실행해도 같은 결과」·「노트북 전체를 처음 값으로 보려면 1절 임시 폴더 셀부터」 — 2절 셀은 같은 스레드에 이어 붙어 수가 달라짐).
- **새 커널 두 번**: A `run_section.sh`(셀 실행 기록 12:35:50.59~12:36:01.66Z, 약 11.1초 → 준비물 「30초 안에」 그대로) `PASS 04-내구-실행-모드-비교.ipynb: 27 cells` · B 사본 `/tmp/ch23-close/B04.ipynb` `execute.py` PASS · 셀별 출력 **26/27 같음** — 다른 한 셀은 6절 되풀이 셀의 **`async` 줄뿐**(A `async | 5 | 5` ↔ B `async | 4 | 5`). **교재 출력(A)이 5/5가 되어** 결과 읽기 둘째 단락·b7 첫 항목의 값을 `mdpatch.py`로 바꿈(「이번 실행에서는 다섯 번 모두 … 새 커널로 한 번 더 실행했을 때는 다섯 번 가운데 4번」). 첫 단락·정리·그림·캡션·복습·b6 표·「확인할 점」의 `exit`·`sync` 값은 모두 앞 판과 같음(끝까지 1·4·4, 끊긴 뒤 `{}`·`()`·0 ↔ `{'completed': ['first']}`·`('second',)`·3, 다시 실행 기록, 되풀이 0/5·5/5, 파일 52, 자식 프로세스 19번·강제 종료 17번).
- 해시: 코드 셀 28 → **27**(셀 59 → 57) · `code_sha256` `ff4e48c4a731…` → **`490b1737b666c0f03c162ae3a7f09327054f640a550f5d187b86fbd64acd5d5e`** · `outputs_sha256` `845cda331722…` → **`341f57f44e6668590d4bbc99968cefb870d078f5d62daf770296af54b5a93f49`**(B `718d35cefb1d…`) · 노트북 파일 `be38374b8616…` → `b81d248ba6e1…` · worker `c60467bd…` 그대로 · 생성기 `11e5dba8f69c…` → `3bbd5e68281e…`. 게이트 0(검사 문장 373 → 393). 남은 자식 프로세스 0(`ps -eo pid,args` + `awk`).
