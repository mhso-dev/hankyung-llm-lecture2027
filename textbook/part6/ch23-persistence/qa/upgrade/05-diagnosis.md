# 05절 진단과 개선 기록 — pending writes와 장애 복구 (experiment)

- 대상: `_src/05-pending-writes와-장애-복구.html` · `labs/part6/ch23-persistence/notebooks/05-pending-writes와-장애-복구.ipynb` · 그림 `figures/05-1`~`05-5`.
- 생성기: `qa/upgrade/author_05.py`(노트북 + `_src`, 01 생성기에서 `html_text`·`table_html`·임시 폴더 셀을 가져오고 폴더 셀은 앞머리만 다른지 `assert`, `ca8264b913c98aab479070f7ba378346b2b15cfab33df5a579cf29785d28a9b4`) · `_src` `174bd51813e2…` · 빌드 HTML `df15083f595c…` · 노트북 파일 `d544089a5e04…`. 그림 설계표 `qa/upgrade/05-figures.md`. 흔들림 확인 `qa/upgrade/05-probe.md`(규칙을 먼저 적고 실행 — 판 A1·A2·B·C·D). 검토 묶음 `qa/upgrade/review-pack/05-pending-writes와-장애-복구.md`.
- 작업일 2026-09-25(UTC 10:0x~10:3x). 형식 **experiment 유지**, **슬러그·제목 그대로**(Ch 20 02 b7 링크 「05절(실패한 단계)」). meta 「강의 1h · 실습 1.5h · 새 용어 3」 그대로(말은 바뀜: 남은 쓰기·작업·장애 복구).
- **모델 요청 0번**(노트북·노트북 밖 모두, 챕터 리드 결정 1). 키 셀 없음. 자식 프로세스 없음.

## 1. 게이트 전후

| | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전 (`gates-before.json`) | 5 | 83 | 5 | 4 | 0 | 0 | 5 | 19 | 3 | **36** |
| 첫 실행 전 (`gates-wip-05-05.json` 첫 판, 노트북·`_src`만 쓴 판) | 21 | 293 | 0 | 0 | 0 | 0 | 0 | 3 → 0 | 18 | — |
| 후 (`gates-wip-05.json`) | **21** | **301** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 첫 검사: G1 **0**, G2 **0** · G6 **3**(70자 넘는 문장 셋 — b4 소스 행 문장·b7 기준 판 문장·b10 소스 행) → 나눈 뒤 **0**으로 만들고 첫 실행. G7 18은 그림 파일·설계표가 없던 때.
- 그림을 넣은 뒤 `--no-exec`: **G1~G7 0**, `verify.py --chapter` **`PASS 6 sections / 139 code cells (max 19 lines)`**(최대 19줄은 개선 전 06). 빌드 HTML `{{`·`[[` 0건, SVG 넷·삽화 JPEG 하나 인라인.
- AST 따로(`/tmp/ch23-05/extra_check.py` — 04 판 복사): **금지 문법 0건**. 허용 표시로 따로 나온 것 3 = `sorted(…)`(키워드 없음 — 5·6절 결과 목록, 마지막 셀 파일 목록; 03·04 판과 같은 모양). 클래스는 칸만 적은 `ResultState(TypedDict)` 하나, 함수 힌트·반환 힌트·데코레이터·f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`.get`·`+=`·기본값·튜플 풀기·한 줄 다중 대입·별표 풀기·`is`·`with`·`subprocess`·세미콜론 0. 셀 모양(`/tmp/ch23-05/shape.py`): 준비 셀이 아닌 셀 주석 뺀 코드 최대 **9줄**(설계 객체·6절 첫 셀), 함수 본문 최대 **6줄**(`saved_channels`), 셀당 정의 하나(정의 셋 — `good`·`flaky`·`saved_channels`), 첫 줄 주석 100%.
- 금지어(`/tmp/ch23-05/ban_check.py` — 04 판 그대로): 노트북·`_src`·캡션 넷·`.mmd` 넷에서 **0건**(걸린 것은 옛 그림 `figures/05-흐름.caption.md`의 「병렬」 하나 — 본문 참조 0, 그대로 둠). 「pending writes」는 제목·슬러그·파일 이름에만(본문 b2는 「제목의 영어 말」로 가리킴), 「superstep」·「병렬」·「채널」·「트랜잭션」·「런타임」·「재시작」 0.
- 코드 줄(`count_code.py`) 53 → **113**(셀 5 → 21, 준비 셀 셋).

## 2. 수정 전 주요 문제 (준비 노트 §1·§2 05·§5-3·§7-5, 인계 §04 → §05)

1. **셀 다섯**: 경로 셀(`[Path.cwd(), *…parents]`·`next(…)` 제너레이터 둘·한 글자 `p` 둘) · **리듀서 `lambda left, right: left + right`** · 한 셀에 함수 셋(`record`·`good`·`flaky`, 힌트 `name: str`·`state: State`·`-> dict`) · 15줄 넘는 셀 둘 · `snapshot.tasks` 내포식(`len(task.result or [])` — 결과가 딕셔너리라 키 수 1을 「결과 하나」로 읽게 함) · `except RuntimeError as exc`.
2. **파일 쓰기**: 실습 폴더 `data/pending-trace.txt`·`data/allow-flaky`(`unlink`·`mkdir`) — 학생 폴더에 남고, 두 번째 실행부터 삭제가 막히는 이 기기에서는 되풀이가 어려움.
3. **호출 차례를 출력**: `calls before resume: ['good', 'flaky']` — 차례는 스레드에 맡겨져 결정적이지 않음(준비 확인 `['flaky', 'good']`).
4. **말**: 「superstep」 8/2/1 · 「병렬」 5/6/1 · 「런타임」 3 · 「트랜잭션」 1/1 · 「채널」 · 「반환」 · 「로그」 · 「pending write(s)」 본문 다수 · 「StateSnapshot.tasks」 영문 시작 문장 · b7 「재시도 한도와 운영 알림」(실행 안 함) · b10 여섯 절 공통 참고 자료(Interrupts·Time Travel).
5. **노트북 설명**: 제목 셀·「이 노트북에서 할 일」·준비물·그림 첨부·결과 읽기 0, 설명 셀은 `_src` 문장 복사. 그림은 옛 `{{svg:05-흐름}}` 한 장. `InMemorySaver`라 「체크포인터에 남은 쓰기」를 눈으로 볼 수 없음.

## 3. 바꾼 것

- **실패 흉내로 만든 결정적 장면(챕터 리드 결정, Ch 16 05 모양)**: 가상 시작점에서 고정 엣지 둘로 `good`·`flaky`를 같은 단계에 둠(Ch 13 05 팬아웃을 고정 엣지로, Ch 20 03 「함께 실행되는 노드는 한 단계」). 상태 형식 `ResultState`(칸 `results`, `operator.add` — 04 `StepState`와 칸이 달라 새 이름). 부른 횟수 딕셔너리 `call_count`와 실패 흉내 딕셔너리 `failure_plan = {"fail": True, "wait_seconds": 0.1}`(Ch 16 05 `failure_plan` 이름을 이음). `flaky`는 `fail`이 `True`인 동안 0.1초 쉰 뒤 `raise TimeoutError("이 절에서 만든 실패 흉내입니다.")`(Ch 16 05 글 그대로) — 0.1초는 `good`이 먼저 끝나게 하려고 실행 전에 정한 값(`05-probe.md` 규칙 4, b7에 까닭과 판 C 결과). 받기는 `except TimeoutError as error`.
- **SQLite 체크포인터 + 임시 폴더(챕터 결정 2)**: 준비 셀 셋 = 설치(`langgraph==1.2.11`·`langgraph-checkpoint-sqlite==3.0.3`, 잠금 판) → 가져오기(`time` 더함) → 임시 폴더(01 셀 앞머리만 `ch23-05-`, 생성기 `assert`). 파일 `pending.sqlite` 하나에 스레드 둘(`pending-a` 기본값 · `exit-run`). 실습 폴더 `data/` 만들지 않음.
- **남은 것을 세 자리에서 봄**: 3절 `get_state` → `칸 값: {'results': ['good-result']}`·`다음 노드: ('flaky',)`·`체크포인트 수: 2` · `tasks`를 작업마다 한 줄(`good | None | {'results': ['good-result']}` / `flaky | TimeoutError('이 절에서 만든 실패 흉내입니다.') | None`) · 4절 함수 `saved_channels(connection, thread_name, task_id)`(03 `sqlite_tables` 모양, Ch 4 03 자리표시자 `?`)로 **표 `writes`의 작업별 칸 `channel`** → `good | ['results']`·`flaky | ['__error__']`. 작업의 `id`는 조건으로만 쓰고 출력하지 않음. `get_state`가 남은 쓰기를 칸 값에 더하고(설치판 `main.py` 1239~1248행) 쓰기가 남은 작업을 다음 노드에서 뺀다(1259행)는 것을 결과 읽기 둘째 단락·b4에.
- **노트북 셀에서 `invoke(None, config)`를 처음 부름**: 5절 `failure_plan["fail"] = False`(원인을 없앰) → `graph.invoke(None, config)` → `결과 목록(정렬): ['flaky-result', 'good-result']`·`부른 횟수: {'good': 1, 'flaky': 2}`(`assert` 둘 — 우리 코드가 센 값) → `다음 노드: ()`·`체크포인트 수: 3`·`남은 작업 수: 0`. 04절 4절 설명 셀 「입력 자리에 `None`을 넣으면 …」을 「04절 스크립트의 다시 실행 단계처럼」으로 이음.
- **6절 `exit`로 같은 실패(04 b7 약속)**: 부른 횟수 0·실패 흉내 켬 → `durability="exit"`로 `exit-run` → `체크포인트 수: 1`·`다음 노드: ('flaky',)`·같은 작업별 칸 이름 → 원인을 없애고 `exit`로 이어 감 → 같은 부른 횟수·결과, `체크포인트 수: 2`. 「04절 강제 종료에서는 아무것도 남지 않았지만, 오류로 멈출 때는 나가면서 저장」을 출력으로 세움.
- **결론은 결정적 값만**: 부른 횟수·칸 값·`next`·`tasks`의 이름·오류·결과·작업별 칸 이름·체크포인트 수·정렬한 결과. **호출 차례와 작업 `id`는 출력하지 않음**(차례는 b7에 소스 근거와 함께 「출력하지 않았다」만). 흔들린 값이 없어 결과 읽기 둘째 단락에 「이번 실행에서는」 값을 둔 곳도 없음.
- **새 말 셋**(meta 「새 용어 3」 그대로): 남은 쓰기(제목의 영어 말은 제목에만) · 작업(task) · 장애 복구 — 세 문장(뜻 → 비유 → 이 절 코드). 처음 쓰는 이름 한 문장씩: 고정 엣지 둘로 같은 단계 · `tasks`(칸 `name`·`error`·`result`) · 표 `writes`의 칸 `task_id`·`channel` · `__error__` · `invoke(None, config)`.
- **본문 10블록 다시 씀**: b3 Ch 13 02·05·Ch 20 03·Ch 16 05·Ch 4 03·01·03·04 링크 · b4 비유(한 탁자의 판 둘, 한 판만 엎어짐) + 삽화 + 용어 표 + 「새 말을 코드에서」 + 05-1 + 「이어 갈 때 다시 실행할 작업을 고르는 법」(소스 행 넷) + 「다른 상황에 적용」 + 「비교와 경계」(04 ↔ 05, 06 링크) · b6 표·05-4 · b7 일곱 줄 · b10 문서 하나·소스 행 일곱.

## 4. 새 커널 두 번 (규격 §2-7 9번 끝)

- A `run_section.sh`(셀 실행 기록 10:21:44.014~10:21:45.317Z, 약 1.3초 → 준비물 「5초 안에」) — **`PASS 05-pending-writes와-장애-복구.ipynb: 21 cells`**. 그림 파일이 아직 없어 `attach_figures.py`에서 멈춤(과제 차례대로 그림 전에 두 번 실행).
- B 사본 `/tmp/ch23-05/B.ipynb`를 `execute.py`로(`UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch23-persistence UV_NO_SYNC=1 PYTHONPATH=…/notebooks`, 10:22:03Z) — `PASS`. 두 실행 모두 빈 임시 폴더에서 시작(폴더 이름은 출력하지 않음).
- 셀별 출력 글자 대조(`/tmp/ch23-05/cmpout.py`) **21/21 같음**. 셀별 출력 글자 해시(`texthash.py`) A·B 모두 `35c0e884b421…`. `code_sha256` **`06cd28c63aff22b514efdc7a4a453a011ae4ac5017dba9a5274a744b7959edfe`**, `outputs_sha256` A·B 모두 **`b39f9ee7fbdf…`**. 교재 노트북은 A.
- 뒤이은 `author_05.py --src-only`(FIG1 alt·삽화 alt·캡션·그림 읽기)와 `--no-exec`의 `attach_figures.py`는 `_src`·노트북 마크다운 첨부만 바꿈 — 노트북의 `code_sha256`·`outputs_sha256`·`executed_at`(10:21:45Z) 그대로, A 사본과 셀별 출력 21/21 같음.

## 5. 도구 파일 — 만들지 않음 (인계 §04 → §05 8항·과제 결정)

- 이 절은 04가 가르친 강제 종료 함수(`start_worker`·`wait_for_signal`·`stop_worker`·`read_saved`·`read_record`·`kill_at_second`)를 쓰지 않음 — 자식 프로세스가 없고, 부른 횟수는 딕셔너리로 셈(기록 파일을 쓰지 않아 `read_record`도 불필요). 그래서 `labs/part6/ch23-persistence/notebooks/checkpoint_tools.py`는 **06이 처음 가져오며 만듦**(아래 인계). 묶음 목록(`textbook/part6/public-files.json`·챕터 `qa/public-files.json`) 변경 0.
- 01 `print_history`·`thread_row`, 03 `print_conversation`·`sqlite_tables`는 쓰지 않음. 4절 `saved_channels`는 이 절이 처음 가르친 함수(03 `sqlite_tables`와 모양이 같고 표·조건이 다름) — 06·07이 표 `writes`를 다시 보면 옮길 후보.

## 6. 설치판 동작과 문서 (모델 없는 확인, 2026-09-25)

- **노트북 밖 확인**(`05-probe.md`, 규칙 먼저): 판 A2(노트북과 같음) 저장 시점마다 100/100 같은 값 · A1(바로 실패) 100/100 같음(`good`의 쓰기가 빠진 회 0) · B(`good` 0.3초·`flaky` 바로) 10/10 · **C(`good` 0.3초·`flaky` 0.1초 뒤) — `exit`만 `good`의 쓰기를 남기지 않아 이어 갈 때 `good` 2번(10/10), 기본값·`sync`는 남음(10/10)** · D(원인을 두고 한 번 더 이어 감) 세 값 20/20 — 둘째 이어 가기도 `TimeoutError`, `good` 1·`flaky` 2 → 원인을 없앤 뒤 `good` 1·`flaky` 3. 두 노드가 **시작한** 차례는 이번 확인 모두 `flaky` → `good`(설치판 `_algo.py` 481~482행 — 이름 차례로 정렬해 띄움, 옛 macOS 출력은 `good` → `flaky`), 끝나는 차례는 소스가 정하지 않음 → 출력하지 않음.
- **계측 한 번**(`/tmp/ch23-05/why2.py`): 판 B에서 그래프는 `_runner.py` 337행 `futures.event.wait`에서 `good`을 기다렸음. 같은 파일 104~114행에서 작업을 새로 등록하면 기다림 표시를 지우므로, `flaky`가 `good`의 등록보다 먼저 실패한 경우로 읽힘(차례에 기대는 동작 — 노트북은 0.1초로 이 틈을 피함).
- **출력으로 본 것**: §3의 값 모두.
- **소스로만 본 것**(본문에 「설치판 소스」로 표시): `langgraph/pregel/_loop.py` 856·861~865행(입력 `None` = 이어 가기) · 661~663·736~749행(남은 쓰기를 작업에 다시 붙임, 오류·`INTERRUPT`·`RESUME` 줄은 건너뜀) · 1324~1333행(`exit`는 나갈 때 체크포인트와 남은 쓰기 저장 — **이번에 출력으로도 확인**) · `langgraph/pregel/main.py` 1239~1248행(`get_state`가 남은 쓰기를 칸 값에 더함)·1259행(쓰기가 없는 작업만 다음 노드)·2967~2968행(쓰기가 없는 작업만 실행) · `langgraph/types.py` 637~646행(`PregelTask`) · `langgraph/checkpoint/sqlite/__init__.py` 145~155행(표 `writes`의 칸) · `langgraph/_internal/_constants.py` 13행(`ERROR = "__error__"` — 본문은 「라이브러리가 받은 오류를 적어 두는 이름」으로만).
- **공식 문서**(WebFetch 2026-09-25): Checkpointers 「Pending writes」 — 「When a graph node fails mid-execution at a given super-step, LangGraph stores pending checkpoint writes from any other nodes that completed successfully at that super-step.」·「When you resume graph execution from that super-step you don't re-run the successful nodes.」(본문 b7·b10은 한국어로 옮김, 영어 원문·「super-step」은 본문에 쓰지 않음). Durable execution 문서는 `None` 입력으로 이어 가는 문장이 없어 인용하지 않음(이 모양은 소스로만).
- **이번에 실행하지 않은 것**(본문에 그렇게 적음): 노트북에서 `sync` · 노드가 파일·다른 서비스에 쓰는 일(06) · 원인을 두고 이어 가기(노트북 밖 D만) · `good`이 늦게 끝나는 경우(노트북 밖 C만) · 걸린 시간 · Windows·macOS.

## 7. 그림

| 그림 | 종류 | 원본 폭(viewBox) | 확인 |
|---|---|---|---|
| 05-1 같은 단계의 두 노드와 남은 쓰기 | `flowchart TB`, 회색 시작 → subgraph 안 파란 노드 둘(나란히) → 노란 표 줄 둘 → 노란 읽은 체크포인트 | 496(첫 렌더 472 — 칸 안 `~~~`가 두 노드를 비스듬히 놓아 빼고 다시 렌더) | PNG를 보고 도식 읽기와 맞춤 |
| 05-2 실패에서 이어 가기까지의 차례 | `flowchart TB` 한 줄 상자 여섯 | 244(세로 741) | 노트북 「오늘 볼 그림」 |
| 05-3 이어 갈 때 작업마다 고르는 두 갈래 | `flowchart TB`, 점선 두 갈래(라벨 있음) | 428 | 첫 상자 낱말 꺾임을 `<br>`로 미리 나눠 다시 렌더 |
| 05-4 기본값과 exit의 실패 뒤와 이어 간 뒤 | `flowchart TB` subgraph 둘 + `~~~` 회색 | 601 | 개수는 한글 |
| 05-5 쓰러진 판과 사진이 남은 판 | Higgsfield 삽화 | 1100 × 614 | 아래 |

- 색: 우리 코드(노드·호출) 파랑 · 출력(받아 출력한 `TimeoutError` 포함) 노랑 · 소스로 읽은 동작·가상 시작점·두 칸 공통 사실 회색 · **빨강 0**(experiment) · **보라 0**(모델 없음) · 초록 0(따로 상자로 둘 값 없음). 라벨 숫자는 `0.1`만.
- 삽화: **1차 job `c7b590e1-63af-4046-8b1e-246fba15464f` 채택**(재생성 0회) — 나무 탁자 하나·체스판 둘 나란히, 왼쪽 판 반듯(말 모두 섬)·앞에 즉석사진 한 장, 오른쪽 판 쓰러짐(말 흩어짐)·사진 없음, 카메라·사람·글자·숫자 없음. 거래 **10:23:49Z 「Nano Banana Pro −2」 한 줄 = 이 절 2크레딧**(잔액 2437.75 → 2435.75, 바로 앞 09:48:29Z는 04절 몫). 원본 `ebc7ac6e…`(2752 × 1536) → 저장 PNG `31b6177e…`, 결과 URL을 한 번 더 받아 같은 폭으로 줄인 그림과 픽셀 대조 bbox `None`·최대 차이 0. 세부 `figures/05-5-…prompt.md` 「상태」.
- 옛 그림 `figures/05-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 참조 0, 사본 `before/figures/`).

## 8. 서비스 요청과 비용

- 모델·임베딩 요청 **0번**(노트북 A·B, 노트북 밖 확인 모두). 키는 읽지 않음(노트북 밖 확인은 `env -u OPENAI_API_KEY`).
- Higgsfield 1회 생성, 2크레딧(§7).

## 9. 챕터 밖 수정

- **없음.** `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json`은 `verify.py --chapter`가 다시 씀(보호 목록 안, `manifest-changes.md`). 공용 도구·규격·과정 요약·계약 파일·Part 목록·묶음·실습 폴더 README·`pyproject.toml`·`uv.lock`·worker 둘 그대로. 새 패키지 설치 0.
- `_build.py`가 01~04·06 HTML·`index.html`도 다시 씀 — `_src`·노트북이 그대로라 내용 변화 없음(01 `d2581c77…`·03 `7e2c3dc1…`·04 `7c175686…` 앞 절 기록과 같음, `index.html`은 `before/index.html`과 바이트까지 같음).

## 10. 완료·뒤 챕터가 05에 기대는 문장 (고치지 않음, 참·거짓만)

| 자리 | 문장 | 판정 |
|---|---|---|
| **Ch 20 02 `_src` b7(완료)** | 「멈춘 실행을 다시 이어 가는 방법은 Ch 23 04절(강제 종료 뒤)과 05절(실패한 단계)에서 다룹니다」 | **05 쪽 참** — 노드 안의 실패 흉내로 멈춘 단계를, 원인을 없앤 뒤 `invoke(None, config)`로 이어 가 끝냄(5·6절 출력). 슬러그 그대로 |
| 04 `_src` b7 | 「다시 실행 단계의 `invoke(None, config)`는 … 스크립트 안에서만 썼고, 노트북 셀에서 부르지는 않았습니다」 | **참** — 05가 노트북 셀에서 처음 부름(5절). 04 문장은 04 안의 사실이라 그대로 참 |
| 04 `_src` b7 | 「`exit`는 노드 안 오류로 멈출 때도 나가면서 체크포인트를 씁니다. 오류로 멈추는 장면은 이 절에서 실행하지 않았고, 05절에서 봅니다」 | **참** — 6절 `exit` `체크포인트 수: 1`·남은 쓰기 |
| 04 `_src` b4·b8·노트북 정리 | 「05절은 강제 종료가 아니라 노드 안 오류로 멈춘 단계를 다룹니다」·「05절에서는 같은 단계의 두 노드 가운데 하나만 실패할 때를 봅니다」(노트북: 「성공한 노드의 쓰기가 남는지」) | **참** |
| 01 `_src` b3·b7 | 「멈춘 실행을 저장된 자리부터 이어 가는 일은 04절과 05절」 | **참** |
| 01 인계 | 「실패한 스레드도 체크포인트 둘·`next`가 남음 — 05가 출력으로」 | **참** — 3절 `체크포인트 수: 2`·`다음 노드: ('flaky',)` |
| Ch 24 01 b3(대기) | 「Ch23에서 노드는 장애 뒤 처음부터 재시작될 수 있고 외부 쓰기에는 멱등성이 필요하다는 점을 확인했습니다」 | 앞 반쪽을 05가 뒷받침(실패한 `flaky`는 이어 갈 때 처음부터 다시 실행, 부른 횟수가 체크포인트 밖에서 늘어남) — 본 판정·멱등성은 06 몫 |
| Ch 31 02 b3(대기) | 「Ch23에서는 중단 뒤 재개와 멱등성을 배웠습니다」 | 재개는 04·05로 참(멱등성은 06 몫) |
| `grep -rn 'pending\|남은 쓰기\|장애 복구' textbook/part6 textbook/part7`(Ch 23 밖) | `part6/index.html` 목차 제목 · `part6/public-files.json`(노트북 경로) · `part6/qa/` 옛 기록 · Ch 21 02 `Literal["paid", "pending", …]`(무관) · Ch 22 `before/` 사본 · Part 7 `qa/existing-artifacts-before.json` | 문장 기대 없음 — 목차 제목·경로는 그대로 참, 옛 기록은 고치지 않음 |

## 11. 강사 확인 대상

1. **실패 흉내 앞 0.1초 쉼**(`failure_plan["wait_seconds"]`) — `good`이 먼저 끝나게 하려는 설계. 노트북 밖 판 C에서 `good`이 늦게 끝나면 `exit`는 `good`의 쓰기를 남기지 않았음(기본값·`sync`는 남음) — b7에 한 줄.
2. 노드가 노트북 전역 딕셔너리(`call_count`·`failure_plan`)를 읽고 고침(Ch 16 05 `failure_plan` 선례) — 두 노드가 서로 다른 스레드에서 돌지만 각자 다른 키만 고침.
3. 호출 차례를 출력하지 않고 횟수만 셈(옛 판은 차례 출력) · 결과 목록은 `sorted`로.
4. `sync`는 노트북에서 실행하지 않음(노트북 밖 100/100 기본값과 같음).
5. 코드 줄 53 → 113(셀 5 → 21) · meta 시수(강의 1h · 실습 1.5h)·새 용어 3 그대로(말은 바뀜).
6. 제목의 「pending writes」는 제목에만(본문 「남은 쓰기」) — 챕터 마감 때 제목을 한국어로 바꿀지(슬러그는 Ch 20 02 링크 때문에 그대로).

## 12. 남은 것 · 지워야 하지만 지우지 않은 것

- 마감 몫: `part6-practice.zip` 재생성(05 노트북 새 판) · 실습 폴더 README(05 문장 — 파일이 임시 폴더에 생긴다는 문장) · 옛 그림 셋(`figures/05-흐름.*`) 삭제 승인 · `visual.cjs` · `chapter.json` `objectives` 셋째 줄 「pending writes와 멱등 키」 대조.
- 삭제 승인 대상(만들었지만 지우지 않음): 기기 **`/tmp/ch23-05/`**(`A.ipynb`·`B.ipynb`·`probe.py`·`probe_d.py`·`why.py`·`why2.py`·`why.sqlite`·`dry.py`·`dry/`(빈 폴더)·`probe-A1.txt`·`probe-A2.txt`·`probe-B.txt`·`probe-C.txt`·`probe-D.txt`·`probe-A1/`·`probe-A2/`(SQLite 300개씩 + 옆 파일)·`probe-B/`·`probe-C/`(30개씩)·`probe-D/`(60개)·`cmpout.py`·`texthash.py`·`extra_check.py`·`ban_check.py`·`shape.py`·`pixcmp.py`·`resize.py`·`figtext.py`·`illu-1-orig.png`·`illu-1-again.png`·`illu-1-1100.png`) · 기기 세션 임시 폴더 **`$TMPDIR/ch23-05-*`** 셋(노트북 A·B와 `dry.py`가 만든 폴더, 각 `pending.sqlite` 하나, 연결 폴더 밖) · `.cache/ch23-05-view/`(PNG 열 — Mermaid 넷 사본·다시 렌더한 둘·`m1`~`m4`·`illu-1-1100.png`) · `qa/upgrade/gates-wip-05-05.json`·`gates-wip-05.json` · `qa/upgrade/__pycache__/author_05.cpython-310.pyc`.

## 마감 반영 (2026-09-25, 검토 1차 `review-round1-A.md`·`review-round1-B.md`)

- **B-7 [중]** b7 첫 항목 끝의 공식 문서 문장을 떼어 새 항목으로: 「공식 문서는 같은 단계에서 성공한 노드의 쓰기를 저장한다고 적습니다. 그러나 위 확인에서 `good`은 실패 뒤에도 끝까지 실행되었는데, `exit`만 그 쓰기를 남기지 않았습니다.」 + 설치판 `_loop.py` 1324~1333행(`exit`는 나가는 자리에서 그때까지 모인 쓰기만 저장)·466행(다른 두 값은 작업이 끝날 때마다 저장) — 문서 문장은 이 관찰의 근거가 되지 않으므로 소스 자리를 근거로 둠. `05-probe.md` 판 C 끝 문장도 같은 방향으로 정정.
- **B-8 [중]** 노트북 셀 14(둘째 노드 설명)에 새 단락: 「기다리는 0.1초는 `good`이 먼저 끝나게 하려고 실행 전에 정한 값입니다. 노트북 밖 확인에서 `good`이 더 늦게 끝나게 하자, 저장 시점 `exit`는 `good`의 쓰기를 남기지 않았습니다. 그 장면은 이 노트북에서 실행하지 않았고, 교재 본문의 주의할 점에 적었습니다.」 — 07 노트북 셀 10(「같은 단계에서 함께 실행되는 노드가 없기 때문」)과 맞음. b6 셋째 단락을 「`flaky`가 0.1초를 기다려 `good`이 먼저 끝나는 한」으로 한정.
- **B-9** 셀 8 「Ch 13 05절의 팬아웃을 고정 엣지 둘로 적은 모양」 → 「Ch 13 05절에서 한 흐름을 여러 갈래로 펼친 것처럼, 이번에는 고정 엣지 둘로 두 갈래를 냅니다」. **B-5** meta `강의 1h | 실습 1.5h`.
- **다시 실행하지 않음** — `code_sha256` `06cd28c63aff…`·`outputs_sha256` `b39f9ee7fbdf…`·`executed_at` 10:21:45Z 그대로(파일 `d544089a5e04…` → `feca728999f7…`). 생성기 `ca8264b913c9…` → `998d378efacd…`(45/45·`_src` 같음). 게이트 0(검사 문장 301 → 307).
