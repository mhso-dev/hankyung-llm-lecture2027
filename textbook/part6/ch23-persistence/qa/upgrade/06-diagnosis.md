# 06절 진단과 개선 기록 — 노드 재시작과 멱등성 (paired)

- 대상: `_src/06-노드-재시작과-멱등성.html` · `labs/part6/ch23-persistence/notebooks/06-노드-재시작과-멱등성.ipynb` · **worker 스크립트 `labs/part6/ch23-persistence/idempotency_worker.py`(다시 씀)** · **도구 파일 `labs/part6/ch23-persistence/notebooks/checkpoint_tools.py`(새로 만듦)** · 그림 `figures/06-1`~`06-5`.
- 생성기: `qa/upgrade/author_06.py`(worker 글 `WORKER` + 도구 파일 글 `TOOLS` + 노트북 + `_src`, 01 생성기에서 `html_text`·`table_html`·임시 폴더 셀, 04 생성기에서 `DEF_*` 여섯·`LOCATE`·`scene_cells`를 가져오고 `check_same_as_before()`·`assert`로 대조, `912c8dc7c65f9cb0b9632070fd34abcb0dbb5f4449ae198976fddf6e129e3c10`) · `_src` `302faf19f4dc…` · 빌드 HTML `2b2a9a459c97…` · 노트북 파일 `869b6ae460f4…` · worker `b0201de72d4534a7238d0bd5b2ad8b4d85e2ca0eeb6f307ac7d6897207430b72` · 도구 파일 `71280dd9fdd748bb9ae98388990a7ed0d33d07e3fb1246abfba95c64c4437c29`(둘 다 노트북 밖 확인 사본 `/tmp/ch23-06/probe/`와 해시 같음). 그림 설계표 `qa/upgrade/06-figures.md`. 흔들림 확인 `qa/upgrade/06-probe.md`(규칙을 먼저 적고 실행). 검토 묶음 `qa/upgrade/review-pack/06-노드-재시작과-멱등성.md`.
- 작업일 2026-09-25(UTC 10:3x~11:0x). 형식 **paired 유지**, **슬러그·제목 그대로**(Ch 20 02 b7 링크 「같은 쓰기를 한 번만 반영하는 방법은 Ch 23 06절」). meta 「강의 1h · 실습 2h · 새 용어 3」 그대로(말은 바뀜: 노드 재시작·멱등성·멱등 키). **본문 마지막 절**.
- **모델 요청 0번**(노트북·노트북 밖 모두, 챕터 리드 결정 1). 키 셀 없음. 자식 프로세스는 노트북 한 번에 24번 띄우고 12번 강제 종료(노트북 밖 판 A 40회 — 회마다 첫 실행·다시 실행 두 번, 자식 프로세스 80번).

## 1. 게이트 전후

| | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전 (`gates-before.json`) | 5 | 79 | 3 | 3 | 0 | 0 | 5 | 14 | 3 | **28** |
| 첫 실행 전 (`--section 06` 첫 검사, 노트북·`_src`만 쓴 판 — `gates-wip-06-06.json`은 마지막 확인에서 다시 써 지금은 0) | 23 | — | 0 | 0 | 0 | 0 | 0 | 2 → 0 | 18 | — |
| 후 (`gates-wip-06.json`) | **23** | **348** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 첫 검사: G1 **0**, G2 **0** · G6 **2**(70자 넘는 문장 둘 — b4 Stripe 문장·b7 판 B 문장의 괄호 뒤 `).`로 두 문장이 붙음) → 나눠 **0**으로 만든 뒤 첫 실행. G7 18은 그림 파일·설계표가 없던 때.
- 그림을 넣은 뒤 `--no-exec`: **G1~G7 0**, `verify.py --chapter` **`PASS 6 sections / 157 code cells (max 14 lines)`**(개선 전 절이 모두 없어져 최대 줄 수가 14로 내려감). 빌드 HTML `{{`·`[[` 0건, SVG 넷·삽화 JPEG 하나 인라인, Before/After 칸 표시(`data-lesson-stage`) 있음.
- AST 따로(`/tmp/ch23-06/extra_check.py` — 05 판 복사): **노트북·worker·도구 파일 모두 금지 문법 0건**. 허용 표시로 따로 나온 것 1 = 마지막 셀 `sorted(os.listdir())`(키워드 없음 — 03~05 판과 같은 모양). 클래스는 칸만 적은 `OrderState(TypedDict)`(노트북 1·worker 1), 함수 힌트·반환 힌트·데코레이터·f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`.get`·`+=`·기본값·튜플 풀기·한 줄 다중 대입·별표 풀기·`try`·`with`(open 밖)·`from __future__`·독스트링(함수)·세미콜론 0. 셀 모양(`/tmp/ch23-06/shape.py`): 준비 셀이 아닌 셀 주석 뺀 코드 최대 **9줄**(4·5절 마지막 셀·6절 되풀이), 함수 본문 최대 **7줄**(`append_key_once`·`kill_then_resume`), 셀당 정의 하나(정의 다섯 — `append_key`·`append_key_once`·`receive_order`·읽기용 `charge`·`kill_then_resume`, 상태 형식 하나 따로), 첫 줄 주석 100%. worker 함수 본문 3·7·2·1·8줄(`charge` 8), 도구 파일 최대 8줄(`read_saved`·`kill_at_second` — 04 판 그대로).
- 금지어(`/tmp/ch23-06/ban_check06.py` — 05 판에서 「재시작」만 뺀 판): 노트북·`_src`·캡션 다섯·`.mmd` 넷·worker·도구 파일에서 참 금지어 **0건**(걸린 5건은 모두 「프로그램」 안 「로그」). 「재시작」은 제목·파일 이름·b2 제목 풀이·용어 표·「새 말을 코드에서」·노트북 4절 정의 문장에만(본문은 「다시 실행」). `interrupt`·`Command`·`update_state`·타임 트래블 0(생성기 `assert "interrupt" not in TOOLS/WORKER`).
- 코드 줄(`count_code.py`) 38 → **123**(셀 5 → 23, 준비 셀 넷). 04 강제 종료 함수 여섯을 도구 파일에서 가져와 04절(147줄)보다 짧음.

## 2. 수정 전 주요 문제 (준비 노트 §1·§2 06·§7-4, 인계 §05 → §06)

1. **셀 다섯**: 경로 셀(`[Path.cwd(), *…parents]`·`next(…)` 제너레이터 둘·한 글자 `p` 둘·`mkdir`) · **`interrupt_then_resume(strategy: str) -> list[str]` 17줄**(함수 이름이 Ch 24 API `interrupt`와 같음 · f-string 셋 · `unlink(missing_ok=True)` · `time.time()` 기한 루프 · `subprocess.run(…, check=True, capture_output=True, text=True, timeout=20)` · 힌트) · 15줄 넘는 셀.
2. **파일 쓰기**: 실습 폴더 `data/idempotency/{naive,idempotent}.{sqlite,log,ready}` — 학생 폴더에 남고, 이 작업 기기의 연결 폴더에서는 SQLite 쓰기가 `disk I/O error`(준비 노트 §5-5).
3. **worker 스크립트**(학생이 여는 파일): `from __future__` · 한 줄 다중 대입 다섯 · 조건 표현식 둘 · `class State` 칸 · 힌트 · 영어 독스트링 · `with sqlite3.connect`(연결을 닫지 않음 — 03) · 인자 차례와 단계 이름(`first`/그 밖)이 04 worker와 달라 04 함수로 부를 수 없음.
4. **말**: 「원자적」 5/1 · 「반환」 6 · 「경로」 6/0/1 · 「로그」 8/1/1 · 「보장」 1/1 · b7 「interrupt 승인과 보상 작업」(Ch 24 말을 먼저 씀) · 「operation_id」·「idempotent 전략」 영문 시작 문장 · b3 「pending write」 · b10 여섯 절 공통 참고 자료(Interrupts·Time Travel).
5. **노트북 설명**: 제목 셀·「이 노트북에서 할 일」·준비물·그림 첨부·결과 읽기 0, 멱등성 정의가 설명 셀과 `_src` b4에 같은 글로 두 번. 그림은 옛 `{{svg:06-흐름}}` 한 장. 노드가 다시 실행되었다는 증거(After에서도 `charge`가 불렸는지)가 출력에 없음.

## 3. 바꾼 것

- **강제 종료 장면 유지(챕터 공통 결정 4)와 paired Before = 실제 결함**: worker를 04 인자 모양(SQLite·신호·결제 기록 파일 이름, 쓰기 방식, `first-run`/`resume`)으로 다시 씀 — 노드 `receive_order`(칸 `notes`에 `주문 받음`) → `charge`(쓰기 방식에 따라 `append_key`/`append_key_once`로 결제 기록 파일에 `order-2306` 한 줄, 신호 파일, 첫 실행 단계에서 30초 쉼, 칸 `notes`에 `적음`/`건너뜀`), 저장 시점 `sync`(04 결론 — 둘째 노드에서 끊겨도 첫째 노드까지의 체크포인트 셋이 남아 `charge`부터 이어 감), 다시 실행 단계는 저장된 다음 노드가 있으면 `invoke(None, …)`. Before 쓰기 방식 `naive` → 같은 키 **두 줄**(빨강) / After `idempotent` → **한 줄**, 두 절은 쓰기 방식 이름만 다른 같은 네 셀(끊기 → 끊기 전 키 → 다시 실행 → 다시 읽기). **칸 `notes`의 `건너뜀`으로 After에서도 `charge`가 다시 실행되었음을 출력으로 보임**(옛 판에 없던 증거).
- **멱등성을 코드로 먼저(2절)**: 노트북 함수 `append_key`(여는 방식 `"a"`로 덧붙이고 `적음`)·`append_key_once`(기록 파일을 읽어 키가 있으면 `건너뜀`, 없으면 `append_key`)를 같은 키로 두 번씩 불러 `적음 적음`·두 줄 ↔ `적음 건너뜀`·한 줄. worker 안의 두 함수는 이 셀들과 **글자까지 같음**(생성기 `assert DEF_APPEND in WORKER` 등 — 본문 3절 문장의 근거).
- **도구 파일 `notebooks/checkpoint_tools.py`를 이 절이 처음 만듦(인계 §04 → §05 8항·§05 → §06 5항)**: 04 함수 여섯(`start_worker`·`wait_for_signal`·`stop_worker`·`read_saved`·`read_record`·`kill_at_second`)을 `# Ch 23 04절에서 배웠습니다 — 04절 노트북 3절(6절)의 같은 이름 함수를 옮겼습니다`로 옮김 — **`author_04.DEF_*`와 문자열 포함·함수별 `ast.dump` 모두 같음**(`check_same_as_before()`), 04 노트북 코드 셀과도 문자열 같음(따로 확인). 이 절이 처음 적은 평범한 함수 셋(`append_key`·`append_key_once`·`kill_then_resume`)도 `# Ch 23 06절에서 배웠습니다 — …`로 같은 파일에 둠(과제 「07이 쓸 평범한 함수가 이 절에서 생기면 같은 파일로」). import `os`·`sqlite3`·`subprocess`·`sys`·`time` + `SqliteSaver`, 모듈 독스트링 한국어, 함수는 모두 인자로만 받음. 노트북은 가져오기 셀(준비 셀, **임시 폴더로 옮기기 전**)에서 알파벳 순 `from checkpoint_tools import kill_at_second, read_record, read_saved, start_worker`, 결과 읽기에 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다」 + 인자 `mode` 자리에 이번에는 쓰기 방식을 넘긴다는 한 문장(§2-7 4번). 04 노트북은 바꾸지 않음(다시 실행 안 함).
- **함수 이름**: 옛 `interrupt_then_resume` → **`kill_then_resume`**(결과 읽기에 이름 뜻 한 문장). Ch 24 API 0.
- **준비 셀 넷(챕터 결정 2)**: 설치(`langgraph==1.2.11`·`langgraph-checkpoint-sqlite==3.0.3`, 잠금 판) → 가져오기(도구 파일 포함) → 자리 찾기(04 `LOCATE`에서 스크립트 이름만 — 생성기 `assert`) → 임시 폴더(01 셀 앞머리만 `ch23-06-` — 생성기 `assert`). 결제 기록·SQLite·신호 파일은 모두 임시 폴더 안 이름. 자리 찾기 결과 읽기에 「교재 출력은 실행 도구가 도구 파일 폴더를 따로 알려 준 실행」 한 문장(과정 §9). 실습 폴더 `data/` 만들지 않음.
- **결론은 결정적 값만**(`06-probe.md` 판 A 쓰기 방식마다 20/20 · 새 커널 두 번 23/23): 끊긴 뒤 `{'order_key': 'order-2306', 'notes': ['주문 받음']}`·`('charge',)`·3 · 끊기 전 키 한 줄 · 다시 실행 종료 코드 0 · 다시 실행한 뒤 체크포인트 4 · `naive` `['주문 받음', '적음']`·두 줄 ↔ `idempotent` `['주문 받음', '건너뜀']`·한 줄 · 되풀이 `naive | 0 | 5`·`idempotent | 5 | 5`. 흔들린 값 없음 → 결과 읽기 둘째 단락에 「이번 실행에서는」 값을 둔 곳 없음. `assert` 둘은 우리 코드와 `sync`가 정하는 줄 수에만.
- **새 말 셋**(meta 「새 용어 3」 그대로): 노드 재시작(제목 말 — 본문은 「다시 실행」, 노트북 4절 결과 읽기에서 뜻 → 비유 → 코드) · 멱등성(2절 — 뜻 → 엘리베이터 호출 버튼 → `append_key`) · 멱등 키(2절 — 뜻 → 기보의 차례 번호 → `order-2306`). 이어 쓴 말: 부작용(Ch 17 02 정의 그대로 인용) · 저장 시점·자식 프로세스·강제 종료·신호 파일(04) · 남은 쓰기(05) · 기록 파일(04). 새 일반 말: 결제 기록 파일·주문 키·쓰기 방식(`naive`/`idempotent`)·읽기용 판.
- **본문 10블록 다시 씀**: b3 Ch 17 02·Ch 2 05·Ch 13 02·04·05 링크 · b4 비유(체스판 옆 기보 — 사진을 찍기 전에 판이 엎어져 같은 수를 다시 둠) + 삽화 + 용어 표 + 「새 말을 코드에서」 + 06-1 + 「끊긴 노드를 처음부터 다시 실행하는 까닭」(소스 행 둘·공식 문서) + 「다른 상황에 적용」(Stripe 설명서 — 부르지 않음) + 「비교와 경계」(05 남은 쓰기 ↔ 06) · b5 예시 부분 · b6 06-4·비교 표·세 단락 · b7 여덟 줄 · b10 문서 셋·소스 행 셋. **b8 다음 절은 07 실습을 가리킴**(링크 없음 — 07이 아직 없음, Ch 21 06 선례).

## 4. 새 커널 두 번 (규격 §2-7 9번 끝)

- A `run_section.sh`(셀 실행 기록 10:54:39.70~10:54:53.98Z, 약 14.3초 → 준비물 「30초 안에」, 04와 같은 여유) — **`PASS 06-노드-재시작과-멱등성.ipynb: 23 cells`**. 그림 파일이 아직 없어 `attach_figures.py`에서 멈춤(과제 차례대로 그림 전에 두 번 실행).
- B 사본 `/tmp/ch23-06/B.ipynb`를 `execute.py`로(`UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch23-persistence UV_NO_SYNC=1 PYTHONPATH=…/notebooks`, 10:55:31Z) — `PASS`. 두 실행 모두 빈 임시 폴더에서 시작(폴더 이름은 출력하지 않음). 두 실행 모두 `PYTHONDONTWRITEBYTECODE=1`로 실습 폴더에 `__pycache__`를 만들지 않음.
- 셀별 출력 글자 대조(`/tmp/ch23-06/cmpout.py`) **23/23 같음**. 셀별 출력 글자 해시(`texthash.py`) A·B 모두 `898ec83a882c…`. `code_sha256` **`52c92b7d341090c2c5205b8f9a8250d64ab6a7ddf1c42a79b5db81b5a92f3c47`**, `outputs_sha256` A·B 모두 **`8cf67c492cc6…`**. 교재 노트북은 A.
- 뒤이은 `author_06.py --src-only`(삽화 alt·캡션·그림 읽기)와 `--no-exec`의 `attach_figures.py`는 `_src`·노트북 마크다운 첨부만 바꿈 — 노트북의 `code_sha256`·`outputs_sha256`·`executed_at`(10:54:54Z) 그대로, A 사본과 셀별 출력 23/23 같음.
- 남은 자식 프로세스: A·B 실행 뒤와 노트북 밖 확인 묶음마다 `ps -eo pid,args`에서 `python … idempotency_worker` 줄 **0**.

## 5. 도구 파일과 묶음 목록

| 함수(인자) | 배운 곳 | 06이 가져옴 | 하는 일 |
|---|---|---|---|
| `start_worker(worker_path, files, mode, phase)` | 04 노트북 3절 | ○ | 스크립트를 자식 프로세스로 띄워 프로세스 객체를 내놓음(글 다섯을 넘김) |
| `wait_for_signal(signal_name, limit_seconds)` | 04 노트북 3절 | (`kill_at_second` 안) | 신호 파일을 0.05초 간격으로 기다려 `True`/`False` |
| `stop_worker(process)` | 04 노트북 3절 | (`kill_at_second` 안) | `kill()` → `wait(timeout=5)` → 종료 코드 |
| `read_saved(graph_builder, sqlite_name, thread_name)` | 04 노트북 3절 | ○ | 새 연결로 읽은 `{"칸 값", "다음 노드", "체크포인트 수"}`, 연결 닫음 |
| `read_record(record_name)` | 04 노트북 3절 | ○ | 기록 파일의 줄을 목록으로 |
| `kill_at_second(worker_path, graph_builder, name_prefix, mode)` | 04 노트북 6절 | ○ | 띄우기 → 신호 → 끊기 → `assert` → `read_saved` |
| `append_key(record_name, order_key)` | **06 노트북 2절** | (노트북에 정의) | 기록 파일 끝에 키 한 줄, `"적음"` |
| `append_key_once(record_name, order_key)` | **06 노트북 2절** | (노트북에 정의) | 키가 이미 있으면 `"건너뜀"`, 없으면 `append_key` |
| `kill_then_resume(worker_path, graph_builder, name_prefix, strategy)` | **06 노트북 6절** | (노트북에 정의) | `kill_at_second` → `start_worker(…, "resume")`·`wait(timeout=30)` → 기록 파일의 키 목록 |

- 묶음 목록 둘에 `labs/part6/ch23-persistence/notebooks/checkpoint_tools.py` 한 줄씩(Part 목록은 `collect_public_files.py`의 `sorted` 결과와 같은 자리, 79줄 — 이름 차례 확인). `part6-practice.zip`은 다시 만들지 않음(마감 몫 — 안에 도구 파일이 없고 04~06 노트북·worker 둘이 옛 판). `check_delivery.py`는 돌리지 않음(Part 6 `qa/delivery-results.json`을 다시 쓰고, 묶음 신선도에서 멈추는 것이 과정 공통 — 마감 몫).
- 01 `print_history`·`thread_row`, 03 `print_conversation`·`sqlite_tables`, 05 `saved_channels`는 쓰지 않아 옮기지 않음(07이 쓰면 07이 옮김 — 인계).

## 6. 설치판 동작과 문서 (모델 없는 확인, 2026-09-25)

- **노트북 밖 확인**(`06-probe.md`, 규칙 먼저): 판 A(노트북 장면) 쓰기 방식마다 **20/20 같음**(끊긴 뒤 칸 값·`('charge',)`·3 · 끊기 전 키 한 줄 · 종료 코드 0 · 다시 실행한 뒤 `적음`/`건너뜀`·4 · 키 두 줄/한 줄, 파일 셋·`-wal` 없음) · 판 B(한 프로세스 안, `charge`가 적은 뒤 실패 흉내 → 원인을 없애고 `invoke(None, config)`) 쓰기 방식마다 **10/10 같음**(두 줄/한 줄 — b7 한 줄).
- **출력으로 본 것**: §3의 값 모두.
- **소스로만 본 것**(본문에 「설치판 소스」로 표시): `langgraph/pregel/_runner.py` 574~613행(`commit` — 작업이 끝나면(성공·오류) 그 작업의 쓰기를 `put_writes`로 넘김, 강제로 끊긴 작업은 이 자리에 오지 않음) · `langgraph/pregel/main.py` 2968행(`[t for t in loop.tasks.values() if not t.writes]` — 쓰기가 없는 작업만 실행)·2987~2988행(`sync`가 단계마다 저장을 기다림).
- **공식 문서**(WebFetch 2026-09-25): LangGraph Checkpointers — 「Checkpointing provides fault-tolerance and error recovery: if one or more nodes fail at a given superstep, you can restart your graph from the last successful step.」·「When you resume graph execution from that super-step you don't re-run the successful nodes.」(본문 b4·b10은 한국어로 옮김, 「super-step」은 쓰지 않음). 같은 문서의 「Nodes after the checkpoint re-execute, including any LLM calls, API requests …」는 되돌려 다시 실행(replay — Ch 24 시간 여행 쪽) 문맥이라 인용하지 않음. Durable execution 문서 주소는 이번에도 Persistence 개요 글만 받음(멱등·부작용 문장 없음 — 인용 안 함). Stripe Idempotent requests — 「Subsequent requests with the same key return the same result」·「You can remove keys from the system automatically after they're at least 24 hours old」(b4·b7, 부르지 않았다고 적음). Python 3.12 subprocess — Windows `kill()` = `terminate()`(04와 같음).
- **이번에 실행하지 않은 것**(본문에 그렇게 적음): 실제 결제 서비스 · 여러 프로그램이 한 기록 파일을 함께 쓰기 · 저장 시점 `exit`·`async`로 끊기 · 기록을 적기 전에 끊기 · 노트북에서 실패 흉내로 멈추기(노트북 밖 판 B만) · 걸린 시간 · Windows·macOS.

## 7. 그림

| 그림 | 종류 | 원본 폭(viewBox) | 확인 |
|---|---|---|---|
| 06-1 끊긴 노드의 갱신과 바깥 기록 | `flowchart TB`, subgraph(칸 안 실제 차례) + 점선 두 갈래(라벨) | 390 | PNG를 보고 도식 읽기와 맞춤 |
| 06-2 끊고 다시 실행하는 차례 | `flowchart TB` 한 줄 상자 다섯 | 273(세로 607) | 노트북 「오늘 볼 그림」. 첫 렌더에서 가운뎃점 뒤 저절로 꺾인 줄을 `<br>`로 미리 나눠 다시 렌더 |
| 06-3 이미 적힌 키면 건너뛰는 두 갈래 | `flowchart TB`, 점선 두 갈래(라벨 있음) | 495 | 노란 상자는 2절·5절 출력에서 확인한 값만(5절 첫 실행이 낸 `적음`은 체크포인트에 없어 넣지 않고 「끊기 전 키 한 줄」로) |
| 06-4 검사 없이 적기와 건너뛰기의 결과 | `flowchart TB` 회색 공통 → subgraph 둘 | 658 | **빨강은 Before 결과 한 상자만**, 공통 회색은 두 칸 출력에서 모두 확인한 값. 06-2와 같은 줄 꺾임을 고쳐 다시 렌더 |
| 06-5 같은 수를 두 번 적은 기보와 한 번 적은 기보 | Higgsfield 삽화 | 1100 × 614 | 아래 |

- 색: 우리 코드(노트북 함수·스크립트 노드) 파랑 · 출력 노랑 · 두 방식 공통 사실 회색 · **Before 결함 결과만 빨강**(paired) · **보라 0**(모델 없음) · 초록 0. 라벨 숫자 `2306`·`0`·절 번호만.
- 삽화: **1차 job `db7ef025-73f3-4dde-82f6-5943c262272f` 채택**(재생성 0회) — 나무 탁자 하나·가운데 체스판(말이 서 있음)·왼쪽 흰 종이에 같은 모양 검은 나이트 실루엣 둘(위아래)·오른쪽 흰 종이에 하나, 글자·숫자·사람·카메라·사진 없음. 거래 **10:57:21Z 「Nano Banana Pro −2」 한 줄 = 이 절 2크레딧**(생성 전 잔액 2435.75, 바로 앞 10:23:49Z는 05절 몫). 원본 `ae1e5fda…`(2752 × 1536) → 저장 PNG `47b1001a…`, 결과 URL을 한 번 더 받아 같은 폭으로 줄인 그림과 픽셀 대조 bbox `None`·최대 차이 0. 세부 `figures/06-5-…prompt.md` 「상태」.
- 옛 그림 `figures/06-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 참조 0, 사본 `before/figures/`).

## 8. 서비스 요청과 비용

- 모델·임베딩 요청 **0번**(노트북 A·B, 노트북 밖 확인 모두). 키는 읽지 않음(노트북 밖 확인·새 커널 실행 모두 `env -u OPENAI_API_KEY`).
- Higgsfield 1회 생성, 2크레딧(§7).

## 9. 챕터 밖 수정

- **`textbook/part6/public-files.json`**(Part 6 묶음 허용 목록) — 도구 파일 한 줄 더함(과제·인계 결정, 규격 §2-7 6번). 그 밖에는 없음. `textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json`은 `verify.py --chapter`가 다시 씀(보호 목록 안, `manifest-changes.md`). 공용 도구·규격·과정 요약·계약 파일·묶음 zip·실습 폴더 README·`pyproject.toml`·`uv.lock` 그대로. 새 패키지 설치 0.
- 챕터 안 보호 파일 중 새로 바꾼 것: `labs/part6/ch23-persistence/idempotency_worker.py`(`f668aa02…` → `b0201de7…`) · 06 노트북 · 챕터 `qa/public-files.json` · `qa/verification.md`(06 행). 새 파일: `labs/part6/ch23-persistence/notebooks/checkpoint_tools.py`.
- `_build.py`가 01~05 HTML·`index.html`도 다시 씀 — `_src`·노트북이 그대로라 내용 변화 없음(01 `d2581c77…`·02 `03bde627…`·03 `7e2c3dc1…`·04 `7c175686…`·05 `df15083f…` 앞 절 기록과 같음, `index.html`은 `before/index.html`과 바이트까지 같음).

## 10. 완료·뒤 챕터가 06에 기대는 문장 (고치지 않음, 참·거짓만)

| 자리 | 문장 | 판정 |
|---|---|---|
| **Ch 20 02 `_src` b7(완료)** | 「같은 쓰기를 한 번만 반영하는 방법은 Ch 23 06절에서 다룹니다」(링크 `06-노드-재시작과-멱등성.html`) | **참** — 멱등 키가 이미 적혀 있으면 건너뛰는 `append_key_once`로, 끊고 다시 실행해도 결제 기록 한 줄(5절·6절 출력). 슬러그 그대로 |
| 05 `_src` b4·b7·b8·노트북 정리 | 「다시 실행한 노드가 체크포인트 밖에 쓴 것은, 다시 실행한 만큼 되풀이됩니다. 같은 쓰기를 한 번만 반영하는 방법은 06절」·「노드가 파일이나 다른 서비스에 쓰는 일도 같고, 06절에서 봅니다」·「06절에서는 다시 실행된 노드가 체크포인트 밖에 한 쓰기를, 한 번만 반영하는 방법을 봅니다」 | **참** — 4절 두 줄(되풀이) · 5절 한 줄(한 번만 반영) |
| 04 `_src` b4 | 「기록 파일에는 `sync`에서도 `second`가 두 번 적혔습니다 … 같은 쓰기를 한 번만 반영하는 방법은 06절에서 봅니다」 | **참** — 같은 `sync`·둘째 노드 장면에서 결제 기록으로 되풀이와 한 번만 반영을 보임 |
| **Ch 24 01 `_src` b3(대기)** | 「Ch23에서 노드는 장애 뒤 처음부터 재시작될 수 있고 외부 쓰기에는 멱등성이 필요하다는 점을 확인했습니다」 | **참** — 강제 종료 뒤 `charge`가 처음부터 다시 실행(`건너뜀`까지 출력), 검사 없는 바깥 쓰기는 두 줄·멱등 키 확인은 한 줄. 「멱등성」·「재시작」 말도 06이 정의 |
| **Ch 31 02 `_src` b3(대기)** | 「Ch23에서는 중단 뒤 재개와 멱등성을 배웠습니다」 | **참** — 재개는 04·05·06, 멱등성은 06 |
| Ch 31 02 b7(대기) | 「외부 결제 API 호출은 데이터베이스 롤백으로 취소되지 않으므로 멱등성 키와 보상 작업이 필요합니다」 | Ch 23과 이어지는 말(멱등 키)은 참, 「보상 작업」은 06이 다루지 않음(기록만) |
| Ch 30 06 b3(대기) | 「Ch23의 thread 분리와 Ch24의 중복 실행 방지 원칙」 | Ch 23 쪽(스레드)은 01로 참 — 06과 무관 |
| Ch 24 01 b8(대기) | 「승인 게이트만으로는 interrupt 앞의 필요한 쓰기를 안전하게 만들 수 없으므로 멱등 처리가 필요합니다」 | 06의 「멱등 키 확인」과 같은 방향(Ch 24 몫, 고치지 않음) |
| Ch 34 04 b7(대기) | 「응답을 이미 일부 처리한 비멱등 작업은 …」 | Ch 23을 가리키지 않음(기록만) |
| `grep -rn '멱등\|idempot' textbook/part6 textbook/part7`(Ch 23 밖, `_src`) | 위 다섯 자리뿐 | — |

## 11. 강사 확인 대상

1. **worker 스크립트를 다시 씀**(04 인자 모양·노드 둘·저장 시점 `sync`·쓰기 방식 이름 `naive`/`idempotent`·한국어 주석) — 학생 묶음에 들어가는 파일이라 마감 때 묶음 재생성 필요.
2. **도구 파일 `checkpoint_tools.py`를 새로 만들고, 이 절이 처음 적은 함수 셋까지 넣음**(과제 「07이 쓸 평범한 함수가 이 절에서 생기면 같은 파일로」) — 07이 그 셋을 쓰지 않으면 06 함수 셋은 도구 파일에만 남음(07·마감에서 확인).
3. **읽기용 `charge` 셀**(파일에 쓰지 않고 칸 모양만 같은 노드 — 04절 읽기용 설계 객체 선례). 스크립트와 노드 이름·칸이 같아야 `read_saved`로 읽을 수 있기 때문이라고 3절에 적음.
4. 결제는 파일 한 줄 흉내, Stripe 설명서 인용(부르지 않음) · 여러 프로그램이 함께 쓸 때의 틈은 실행하지 않고 b7에 적음.
5. 코드 줄 38 → 123(셀 5 → 23) · 자식 프로세스 24번(노트북 약 14초) · meta 시수(강의 1h · 실습 2h)·새 용어 3 그대로(말은 바뀜).
6. `kill()`·종료 코드는 Linux 출력 — Windows·macOS는 실행하지 않음.

## 12. 남은 것 · 지워야 하지만 지우지 않은 것

- 마감 몫: 07 실습 절 신설(인계 `§06 → 실습(07)`) · `part6-practice.zip` 재생성(도구 파일·worker 둘·04~06 노트북 짝) · `check_delivery.py` · 실습 폴더 README(도구 파일 단락·worker 둘·파일이 임시 폴더에 생긴다는 문장·옛 Docker 명령) · 옛 그림 셋(`figures/06-흐름.*`) 삭제 승인 · `visual.cjs` · `chapter.json` `objectives` 셋째 줄 「pending writes와 멱등 키」 대조 · 06 b8에 07 링크를 더할지(07이 생긴 뒤).
- 삭제 승인 대상(만들었지만 지우지 않음): 기기 **`/tmp/ch23-06/`**(`A.ipynb`·`B.ipynb`·`probe/`(worker·도구 파일 사본)·`probe_a.py`·`probe_b.py`·`probe-A/`(폴더 40개 — 각 SQLite·신호·기록 파일 셋, `naive.jsonl`·`idempotent.jsonl`)·`probe-B/`(폴더 20개)·`probe-A-naive.txt`·`probe-A-idempotent.txt`·`probe-B.txt`·`cmpout.py`·`texthash.py`·`extra_check.py`·`ban_check.py`·`ban_check06.py`·`shape.py`·`pixcmp.py`·`resize.py`·`figtext.py`·`illu-1-orig.png`·`illu-1-again.png`·`illu-1-1100.png`) · 기기 세션 임시 폴더 **`$TMPDIR/ch23-06-*` 둘**(노트북 A·B가 만든 폴더, 각 파일 38, 연결 폴더 밖) · `.cache/ch23-06-view/`(PNG 셋 — 다시 렌더한 06-2·06-4 사본 `m2`·`m4`·`illu-1-1100.png`) · `qa/upgrade/gates-wip-06-06.json`·`gates-wip-06.json`.

## 마감 반영 (2026-09-25, 검토 1차 `review-round1-A.md`·`review-round1-B.md`)

- **B-2(06 몫)**: 4·5절 끊는 셀이 04절 함수 `new_prefix`로 새 앞머리(`naive-1`·`idempotent-1`)를 고르고 `kill_at_second`에 넘김, 기록 셀의 `naive_files`는 그 앞머리로 만듦, 6절 되풀이는 회차마다 `new_prefix`(`naive-2~6`·`idempotent-2~6`), 마지막 셀은 `4절 기록 파일 이름: naive-1.record`·옆 파일 `-wal` 없음. 가져오기 셀에 `new_prefix`(함수 다섯, 알파벳 순). 다시 실행 셀은 04절 5절 셀과 이름만 다름(생성기 `assert` 그대로). 셀을 다시 실행해도 4/4·4/4·1/1 같음(04 진단 마감 반영).
- **도구 파일** `notebooks/checkpoint_tools.py`: `new_prefix`를 `read_record` 뒤에 `# Ch 23 04절에서 배웠습니다 — 04절 노트북 3절의 같은 이름 함수를 옮겼습니다`로 더함(함수 아홉 → **열**) · 머리 독스트링 「강제 종료 함수 여섯」 → 「함수 일곱(강제 종료 함수와 앞머리 글 함수)」, 「06절 … 뒤 절이 가져다 쓸 수 있게」 → 「(07절은 그 가운데 append_key와 append_key_once를 가져옵니다)」(**B-11**: `kill_then_resume`은 남김 — 가르친 함수를 모은다는 규칙, 빼도 얻는 것이 없음, 강사 확인). `check_same_as_before()` 문자열·AST 대조 통과. 해시 `71280dd9fdd7…` → **`a850b2cdccbd8ff6f3dd8364e5ab58a8f2845eb6c8607ef7250315c5eee26b37`**.
- **B-10** b4 「그 단계 안의 노드는 처음부터 다시 실행되므로」 → 「끝나지 못한 노드는 …」. **B-12** 노트북 셀 10 「체크포인트는 그래프의 칸 값을 저장할 뿐」 → 「칸 값과 칸에 낸 갱신을 담을 뿐」. **B-5** meta `강의 1h | 실습 2h`. b7에 다시 실행 안내 항목과 Windows 종료 코드 1 문장, 준비물에 다시 실행 안내.
- **새 커널 두 번**: A `run_section.sh`(12:36:11.46~12:36:25.59Z, 약 14.1초 → 「30초 안에」 그대로) `PASS … 23 cells` · B 사본 `execute.py` PASS · 셀별 출력 **23/23 같음**. 값은 앞 판과 같음(끊긴 뒤 `('charge',)`·3·키 한 줄, Before 두 줄·After 한 줄, `naive | 0 | 5`·`idempotent | 5 | 5`, 파일 38, 자식 프로세스 24번·강제 종료 12번). `code_sha256` `52c92b7d3410…` → **`8d7467afba42dd96c45fc3a54c80f02237f5c96da3d5faf030bcb3f6f258504f`** · `outputs_sha256` `8cf67c492cc6…` → **`8bf6435755e79a4de2ea1fd5359ab0426211be9ee684c049fbbde79ac1fbc0d7`**(A·B 같음) · 파일 `869b6ae460f4…` → `589badaba914…` · worker `b0201de7…` 그대로 · 생성기 `f620b444e385…` → `4abfe18b7928…`. 게이트 0(검사 문장 348 → 356).
