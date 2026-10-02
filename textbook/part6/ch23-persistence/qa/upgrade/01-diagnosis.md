# 01절 진단과 개선 기록 — 체크포인터와 스레드 (experiment)

- 대상: `_src/01-체크포인터와-스레드.html` · `labs/part6/ch23-persistence/notebooks/01-체크포인터와-스레드.ipynb` · 그림 `figures/01-1`~`01-5`.
- 생성기: `qa/upgrade/author_01.py`(노트북 + `_src`, `534de7c35fd49980704cdcf0986961133bb7e61377769db2c6df5df7c3e423f2`) · `_src` `1df66ad5004c…` · 빌드 HTML `d2581c772adc…`. 모델 없는 확인: 기기 `/tmp/ch23-01/exp1.py`·`exp2.py`(설치판 langgraph 1.2.11 · langgraph-checkpoint 4.2.0, 요청 0). 그림 설계표: `qa/upgrade/01-figures.md`. 검토 묶음: `qa/upgrade/review-pack/01-체크포인터와-스레드.md`.
- 작업일 2026-09-25(UTC 07:3x~08:2x). 형식 **experiment 유지**, **슬러그 그대로**(Ch 20 03 b7이 링크 — 챕터 리드 결정 6), 제목 그대로.
- **모델 요청 0번**(노트북·노트북 밖 모두, 챕터 리드 결정 1). 키 셀 없음. 흔들림 확인 대상이 없어 `01-probe.md`는 만들지 않았습니다.

## 1. 게이트 전후

| | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전 (`gates-before.json`) | 4 | 75 | 0 | 1 | 0 | 0 | 6 | 22 | 3 | **32** |
| 첫 실행 전 (`gates-wip-01-01.json`, 노트북·`_src`만 쓴 판) | 28 | 344 | 0 | 0 | 0 | 0 | 0 | 1 | 6 | — |
| 후 (`gates-wip-01.json`) | **28** | **349** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G1·G2 **0**(과제 지시대로 첫 실행 전에 먼저 검사). G6 1 = 복습 1 해설이 코드 이름+조사(「`KeyError`를 받았습니다」)로 시작 → 「오류 `KeyError`를 받았습니다」. G7 6 = 캡션·설계표·삽화 prompt 파일이 아직 없던 때의 값.
- AST 따로(`/tmp/ch23-01/extra_check.py` — Ch 21 마감 판 `.cache/ch21-close/extra_check.py` 복사, 허용 목록 그대로): 노트북 **0건**. 클래스는 칸만 적은 `CountState(TypedDict)` 하나(Ch 13 L5 모양, `Annotated[list[str], operator.add]` 칸 하나), 함수 힌트·반환 힌트·데코레이터·f-string·내포식·`lambda`·조건 표현식·`elif`·`next`·`.get`·`+=`·기본값·튜플 풀기·별표 풀기·`with`·`is` 0.
- 금지어(`/tmp/ch23-01/ban_check.py` — Ch 21 마감 판 + 「스냅샷」·「superstep」·「Store」): 노트북·`_src`·캡션 다섯·`.mmd` 넷에서 **10건 = 「로그」 8(「프로그램」 안 글자) + 「Store」·「저장소(Store」 2**(b7 「여러 스레드가 함께 쓰는 저장소(Store)는 이 챕터에서 실행하지 않았습니다」 — 옛 판 문장을 실행하지 않았다고 적은 자리, 챕터 리드 지시대로). 참 금지어 0건(규격 §4 금지 말 포함).
- 코드 줄(`count_code.py`) 32 → **113**(셀 4 → 28). 준비 셀이 아닌 셀의 주석 뺀 코드 최대 **8줄**(`PLAIN_BUILD`), 준비 셀 최대 6줄, 함수 본문 최대 **7줄**(`thread_row`), 셀당 정의 하나, 첫 줄 주석 100%.

## 2. 수정 전 주요 문제 (준비 노트 §1·§2 01)

1. **셀 넷에 한 셀 15줄 넘음**(c4 상태 형식 + 노드 + 설계 객체 + 컴파일) · 노드 힌트 `add(state: State) -> dict`(Ch 13·20·21은 힌트 0) · 첫 줄 주석은 옛 생성기 `CODE_COMMENTS`가 끼운 한 줄뿐.
2. **노트북 설명**: 제목 셀·「이 노트북에서 할 일」·준비물·그림 첨부·결과 읽기 0. 설명 셀은 `_src` b4 둘째 단락과 같은 글(옛 도구 `part6a_enrich.py`).
3. **본문**: 영문 시작 문장(「customer-a가 …」·「StateSnapshot의 values는 …」) · 금지어 「반환」·「식별자」·「스냅샷」·「채널」·「경로」·「스키마」 · 70자 넘는 문장 · b5 「다른 상황과 적용 경계」 = b6 둘째 단락 · 「Store는 … 저장합니다」(과정·챕터 모두 실행하지 않은 기능을 사실처럼) · b8 「다음 절의 PostgreSQL 저장소와 용도가 다릅니다」(비교를 실행하지 않음) · b10 참고 자료 넷이 여섯 절 공통(Interrupts·Time Travel은 Ch 24 주제).
4. **관찰 범위**: 기록 수 6·3만 출력하고 「무엇이 몇 개 저장됐는지」는 보이지 않음 · 체크포인터가 없을 때와 견주지 않아 「이어 쓴다」의 근거가 결과 한 줄뿐 · 입력 칸이 저장된 값과 어떻게 합쳐지는지 없음.
5. **그림**: 옛 `{{svg:01-흐름}}` 한 장(상자 넷 한 줄, 값 없음), Mermaid·삽화 0.

## 3. 바꾼 것

- **그래프**: 옛 칸 `total`·`events`(글 목록 끝 값을 `int`로) → 칸 `total`·`amount`·`trace`(실행 흔적, Ch 13 02 `operator.add`)의 `CountState`, 노드 함수 `add_amount`(이름 `add`) — 옛 판 수치 모양 **customer-a 3 → 7 · customer-b 4** 그대로(챕터 리드 결정 「결정적」).
- **체크포인터 없는 그래프와 견줌(3절)**: 같은 설계 객체를 `compile()` / `compile(checkpointer=memory)`로 둘 만들어 **같은 두 입력**(`total 0·amount 3` → `amount 4`만)을 넣음 → 체크포인터 없음은 둘째 실행에서 `KeyError: 'total'`(셀에서 받아 출력, 결정적), 있음은 합계 7. Ch 21 03 「결과 상태는 실행 한 번 안에서만」과 잇는 문장.
- **저장된 것 세기(7·8절)**: `get_state` → `StateSnapshot`·`values`·`next ()`·`metadata["step"]` 4 · `get_state_history`를 `list`로 담아 **6**, 함수 `print_history(history)`로 단계 번호·만든 자리(`source`)·다음 노드·칸 값을 한 줄씩(최신 것부터) — 실행 한 번에 셋(입력을 받은 때 `input` · 입력을 칸에 넣은 뒤 `loop` · 노드를 마친 뒤 `loop`). 체크포인트 ID·만든 시각은 실행마다 달라 출력하지 않음.
- **값 바꿔 보기 둘**: 9절 스레드 이름만(`customer-b`, 새 스레드라 합계 0부터 — 결과 4, 체크포인트 3, `customer-a` 합계 7 그대로) · 10절 둘째 입력에 `total` 0을 더함(`customer-c` — 합계 4, 실행 흔적 두 칸, 단계 3에서 합계가 0으로 덮어써짐 — Ch 13 02 「덮어쓰기」로 설명).
- **경계 확인(9·11절)**: 한 번도 실행하지 않은 스레드 `customer-new` → `{}`·`()`(오류 없음) · 설정 없이 부르면 `ValueError`(글 그대로 인용) · 새 `InMemorySaver`로 컴파일한 그래프는 `customer-a`를 읽지 못함(`{}`) · 임시 폴더 파일 `[]`·`0`.
- **기록 표(12절)**: 함수 `thread_row(compiled_graph, thread_name)`(Ch 13 01 `run_row` 모양, 그래프를 인자로) → 세 줄 `customer-a | 7 | ['add', 'add'] | 6` · `customer-b | 4 | ['add'] | 3` · `customer-c | 4 | ['add', 'add'] | 6`.
- **`assert`**: 둘째 실행 합계 7 · `customer-a` 체크포인트 6 — 둘 다 코드로 정해지는 값.
- **준비 셀(챕터 표준)**: 설치 `"langgraph==1.2.11" "langgraph-checkpoint==4.2.0"`(이 절이 가져오는 두 패키지, 잠금 판 — `langgraph-checkpoint`는 잠금의 옮겨 오는 의존) → 가져오기(Ch 13 이름 + `InMemorySaver`) → **임시 폴더**(`tempfile.mkdtemp(prefix="ch23-01-")` → `os.chdir()` → `os.listdir()`, Ch 4 03 모양 — 폴더 위치는 출력하지 않고 앞머리가 들어 있는지 `True`만). 키 셀 없음.
- **본문 10블록 다시 씀**: 제목 말 Persistence(상태 저장)·Durable Execution(이어 실행)을 b2·노트북 1절에서 풂 · 새 말 셋(체크포인터·체크포인트·스레드) 세 문장 · b4 「이어 실행에서 칸 값이 정해지는 차례」 · b6 표(스레드별 넣은 값·합계·실행 흔적·체크포인트 수) · b7 여덟 줄(소스 행 번호·공식 문서·Store 실행 안 함·걸린 시간 안 잼) · b10 절에 맞는 참고 자료(Checkpointers·Persistence·설치판 소스 행).
- 옛 판 b5 「사용자 ID를 그대로 스레드 ID로 쓰면 …」·b7 「thread_id를 사용자 입력에서 그대로 받기보다 …」는 실행하지 않은 운영 조언이라 뺐습니다(b4 「다른 상황에 적용」은 「대화 하나에 스레드 이름 하나」까지만).

## 4. 새 커널 두 번 (규격 §2-7 9번 끝)

- A `run_section.sh`(셀 실행 기록 08:04:28.02~08:04:29.40Z, 약 1.4초 — 설치 셀이 이미 설치된 판이라 0.8초) · B 사본 `/tmp/ch23-01/B.ipynb`를 `execute.py`로(08:04:47.57~08:04:48.54Z, `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch23-persistence UV_NO_SYNC=1 PYTHONPATH=…/notebooks`). **그림 그리기 전에 두 번 모두 실행**.
- 셀별 출력 글자 대조(`/tmp/ch23-01/cmpout.py`) **28/28 같음**, `code_sha256` **`9d71f6f9522f33a65f5cf36368ec94913fcaf074a254a98e734af2661a4485c9`**, `outputs_sha256` A·B 모두 **`4315f7f9e3d39150cdf5bc4e2d387b4d4fdc00bac84d887e674accf55eaeb777`**. 흔들린 값 없음 → 본문·그림·정리의 값은 모두 두 번 같은 값. b6 「새 커널로 두 번 실행했을 때 코드 셀 28개의 출력이 모두 같았습니다」.
- 뒤이은 `mdpatch.py`(비유 말 여섯 곳 — §7)·`attach_figures.py`는 마크다운만 바꿈: 노트북 파일 `7189b35f…`, `code_sha256`·`outputs_sha256`·`executed_at`(08:04:29Z) 그대로(`/tmp/ch23-01/nbhash.py`).
- 준비물 「5초 안에」는 A 셀 실행 기록(약 1.4초)을 넉넉히 둔 값입니다(설치 셀은 네트워크에 따라 다름 — 준비물에 적음).

## 5. 도구 파일 — 만들지 않음 (챕터 리드 결정 5 「01이 쓸 일이 없으면 만들지 말기」)

- 01이 **가져오는** 앞 챕터 함수가 없습니다(Ch 20 `graph_tools.py`·Ch 21 `runner_tools.py`는 메시지·사용량 함수, 모델 없는 이 절에서 쓸 곳 0 — 준비 노트 §4-1). Ch 13 `print_state`는 칸이 달라 못 씀.
- 01이 **처음 가르친** 평범한 함수 둘은 노트북에 둡니다: `print_history(history)`(8절, 본문 5줄) · `thread_row(compiled_graph, thread_name)`(12절, 본문 7줄). 둘 다 인자로만 받고 노트북 전역 이름에 기대지 않음 — 뒤 절(03·05·07)이 되풀이하면 **처음 가져오는 절이** `notebooks/checkpoint_tools.py`를 만들어 옮기고(`# Ch 23 01절에서 배웠습니다`) 묶음 목록 둘을 고칩니다(인계 「챕터 공통」).
- 묶음 목록(`textbook/part6/public-files.json`·챕터 `qa/public-files.json`) 변경 0.

## 6. 설치판 동작과 문서 (모델 없는 확인 `/tmp/ch23-01/exp1.py`·`exp2.py`, 2026-09-25)

- 출력으로 본 것(노트북 결과 읽기 근거): 위 §3 값 모두. 옛 판 `get_state_history` 단계 `4 loop ()`·`3 loop ('add',)`·`2 input ('__start__',)`·`1 loop ()`·`0 loop ('add',)`·`-1 input ('__start__',)`(준비 노트 §2 01)과 같은 모양 — 단계 -1의 칸 값은 `{'trace': []}`(규칙을 적은 칸만 빈 목록으로 있음).
- 소스로만 본 것(본문에 「설치판 소스」로 표시): `InMemorySaver` 설명(`langgraph/checkpoint/memory/__init__.py` 36~42행 — `defaultdict`에 저장, 디버깅·시험용) · 목록을 최신 것부터 늘어놓는 자리(같은 파일 334~354행 `sorted(…, reverse=True)`) · 설정 없이 부를 때의 `ValueError`(`langgraph/pregel/main.py` 2589~2593행) · `compile`의 인자 `checkpointer`(`langgraph/graph/state.py` 1177~1179행).
- 공식 문서(WebFetch, 2026-09-25): `https://docs.langchain.com/oss/python/langgraph/checkpointers` — 「A checkpointer saves a snapshot of graph state at each super-step, organized into threads.」 · 「When invoking a graph with a checkpointer, you must specify a `thread_id` as part of the `configurable` portion.」 · START → A → B → END 「exactly 4 checkpoints」 · 「ordered chronologically with the most recent checkpoint being the first in the list」 · InMemorySaver 「for experimentation」. `https://docs.langchain.com/oss/python/langgraph/persistence` — 「MemorySaver and InMemorySaver store checkpoints in RAM. When the process restarts, all checkpoints are lost.」 · Store = 「long-term, cross-thread memory」(이 챕터 실행 안 함).
- **이번에 실행하지 않은 것**(본문에 그렇게 적음): 커널 다시 시작 뒤 사라짐(공식 문서 문장만) · Store · 에이전트 그래프에 체크포인터 붙이기 · 노드가 여럿인 그래프의 체크포인트 수 · 실패로 멈춘 실행의 체크포인트(준비 확인 `exp2.py`에서 실패한 스레드도 체크포인트 둘·`next ('add',)`이 남는 것을 봤지만 05 몫이라 본문에 넣지 않음) · 걸린 시간.
- 부수 효과(본문에 넣지 않음): 없는 스레드를 `get_state`로 읽으면 `InMemorySaver.storage`(defaultdict)에 그 이름의 빈 칸이 생김 — 공개 API 밖이라 결과에 드러나지 않음.

## 7. 그림

| 그림 | 종류 | 원본 폭(viewBox) | 확인 |
|---|---|---|---|
| 01-1 스레드마다 따로 쌓이는 체크포인트 | `flowchart TB` 상자 다섯, 점선 갈래 둘 | 493 | PNG를 보고 도식 읽기와 맞춤 |
| 01-2 체크포인터가 없을 때와 있을 때 | `flowchart TB` + subgraph 둘 + 공통 파란 상자 | 669 | 첫 판 파란 상자 라벨이 저절로 꺾여 `<br>`로 미리 나눔 |
| 01-3 같은 스레드의 체크포인트 여섯 | `flowchart LR` + subgraph 둘(칸 안 `TB`) | 552 | 첫 판 `TB`는 세로 952로 길어 `LR`로 바꿈 |
| 01-4 세 스레드의 마지막 상태 | `flowchart TB` + subgraph 셋(가로) + 회색 공통 상자 | 808 | 회색 상자 라벨을 네 줄로 미리 나눔 |
| 01-5 판마다 따로 쌓이는 즉석사진 | Higgsfield 삽화 | 1100 × 614 | 아래 |

- 색: 넘긴 값·입력 초록 · 설계 객체 파랑 · 출력 확인 값·받아 출력한 오류 노랑 · 라이브러리가 만든 그래프·체크포인터·공통 사실 회색 · **보라 0 · 빨강 0**(experiment). 라벨 숫자는 모두 노트북 출력에 있음(G7 통과, 한 자리 수는 손으로 대조 — `-1`·`0`~`4`·`3`·`4`·`7`).
- 삽화: 1차 job `a6d9c270-945b-4ede-b6b9-28691e3ec7ea` **탈락**(왼쪽 사진 다섯 장 — 여섯이어야 함) → 2차 job **`547c15e2-02f2-43a4-be28-24aa6a51fbde` 채택**(왼쪽 여섯 장 세 장씩 두 줄 · 오른쪽 세 장 한 줄 · 카메라 하나). 거래 기록 08:05:01Z·08:05:55Z 「Nano Banana Pro −2」 두 줄 = **이 절 4크레딧**(잔액 2449.75 → 2445.75). 저장 PNG `c99e8b0a…`와 채택 job 결과를 같은 폭으로 줄인 그림의 픽셀 대조 bbox `None`·최대 차이 0. 세부 `figures/01-5-…prompt.md` 「상태」.
- 삽화가 「세 장씩 두 줄」이라 비유 문장의 「옆에 차례로 늘어놓습니다」·「줄을 세웁니다」를 「앞에 모아 둡니다」·「따로 둡니다」로 고침(`mdpatch.py`, `/tmp/ch23-01/reps1.json` 여섯 곳 — 생성기·노트북 마크다운·`_src` 함께, 다시 실행 없음). 용어 뜻 「한 이름으로 묶인 체크포인트들의 줄」은 목록의 차례라 그대로.
- 옛 그림 `figures/01-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 참조 0, 사본 `before/figures/`).

## 8. 옛 생성기 (챕터 리드 결정 7)

- **공용 `qa/author_ch23_ch24.py`**(Ch 23·24 함께 씀): 머리 주석 세 줄 + `write_all()`의 노트북 고리와 `_src`·그림 생성기 고리에서 `chapter == "ch23-persistence"`면 건너뜀(`8635d292…` → **`44c9d593fcd061760fc2255453c20d3ccbe21a347ff5c0325e49ad91e12edcfb`**). **Ch 24 쪽 동작 그대로 — 사본에서 전후 대조**: `/tmp/ch23-01/gen/A`(원본)·`B`(고친 판)를 빈 뼈대에서 각각 실행 → Ch 24 노트북 셋·`_src` 셋·`figures/_gen_figures.py`가 `diff -r` 같음, Ch 23 파일은 A만 씀(노트북 여섯·`_src` 여섯·`_gen_figures.py`), B는 0. (참고: 옛 생성기는 원래도 지금 디스크의 Ch 24 파일과 다른 판을 씀 — 막기 전후 같음, Ch 24 몫.) 옮기지 않음(마감·Ch 24 몫).
- **`figures/_gen_figures.py`**: 맨 위 설명 주석 세 줄 + `raise SystemExit("개선 전 그림 생성기입니다. …author_NN.py를 쓰세요.")`(`e77d489f…` → **`6d95031c3aafa0486e01e473e8c90361d62a008511ee9a287d525ec4623371ae`**), 실행하면 종료 코드 1로 멈춤 확인. 옮기기(`mv -n` → `before/generators/blocked/`)는 마감 몫.

## 9. 서비스 요청과 비용

- 모델·임베딩 요청 **0번**(노트북 A·B, 노트북 밖 확인 모두). 예상 비용 0달러. 키는 읽지 않음.
- Higgsfield 2회 생성, 4크레딧(§7).

## 10. 챕터 밖 수정

- 없음. (`textbook/_notebook/checks/notebook-contracts-part6-ch23-persistence.json`은 `verify.py --chapter`가 다시 씀 — 보호 목록 안, `manifest-changes.md`.) 공용 도구·규격·과정 요약·계약 파일·Part 목록·묶음 모두 그대로.
- `_build.py`가 02~06 HTML·`index.html`도 다시 씀 — `_src`·노트북이 그대로라 내용 변화 없음(두 번 빌드 해시 같음, `index.html`은 `before/index.html`과 바이트까지 같음).

## 11. 완료 챕터가 01에 기대는 문장 (고치지 않음, 참·거짓만)

| 자리 | 문장 | 판정 |
|---|---|---|
| Ch 20 03 `_src` b7 · HTML | 「실행 중 상태를 저장해 두는 체크포인터는 Ch 23 01절에서 다룹니다」(링크 `01-체크포인터와-스레드.html`) | **참** — 01이 체크포인터를 처음 가르침, 슬러그 그대로 |
| Ch 20 03 `_src` b7 | 「한도에 닿은 실행의 상태를 체크포인터로 읽는 일은 이번에 하지 않았습니다」 | 참(01도 하지 않음 — b3에서 「04·05절에서 다룹니다」) |
| Ch 21 03 b4·b7 · 07 b7 | 「결과 상태를 저장해 다음 실행에 이어 쓰는 방법은 Ch 23에서 배웁니다」 | **참** — 01 6절 3 → 7(에이전트 그래프가 아닌 우리 그래프로 보임 — b4 「다른 상황에 적용」에 한 문장) |
| Ch 20 02 b7 | 04·05·06 링크 | 01 무관(슬러그 그대로) |
| Ch 22 09 b8 | 「종류별로 출력한 대화 기록이 그 대상」 | 03 몫(메시지 칸 — 챕터 리드 결정 1, 인계) |

## 12. 강사 확인 대상

1. 제목 말 「Persistence」·「Durable Execution」(챕터 제목) — 본문 첫 자리에서 「상태 저장」·「이어 실행」으로 풂.
2. 코드 줄 증가 32 → 113(셀 4 → 28) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘. 늘어난 몫은 체크포인터 없는 그래프(3절)·저장된 것 세기(7·8절)·값 바꿔 보기 둘·경계 확인(11절)·기록 표(12절).
3. 모델 없는 절(키 셀 없음) — 챕터 리드 결정 1. 옛 판 스레드 이름 `customer-a`·`customer-b`를 그대로 두고 `customer-c`·`customer-new`를 더함.
4. 모든 절 준비 셀에 임시 폴더(Ch 4 03 모양)를 Part 6에서 다시 씀 — 01은 파일을 쓰지 않지만 챕터 모양을 맞추고 11절 「파일이 생기지 않음」 관찰에 씀.
5. 옛 판의 운영 조언(스레드 이름을 사용자 입력에서 받지 않기 등)을 뺌.

## 13. 남은 것 · 지워야 하지만 지우지 않은 것

- 마감 몫: `figures/_gen_figures.py` `mv -n` · 공용 옛 생성기(Ch 24 작업과 함께) · 옛 그림 셋 삭제 승인 · `chapter.json` `objectives` 첫 줄 대조(「체크포인터와 thread_id로 실행 상태를 저장하고 재개할 수 있습니다」 — 01 범위는 「저장하고 같은 스레드에서 이어 쓴다」, 「재개」는 04·05 뜻과 겹치니 마감 때 절 본문 말과 대조).
- 삭제 승인 대상(만들었지만 지우지 않음): 기기 `/tmp/ch23-01/`(`exp1.py`·`exp2.py`·`a1.py`·`a2.py`·`a3.py`·`A.ipynb`·`B.ipynb`·`cmpout.py`·`nbhash.py`·`extra_check.py`·`ban_check.py`·`resize.py`·`pixcmp.py`·`reps1.json`·`reps2.json`(쓰지 않은 초안)·`html-a.txt`·`html-b.txt`·`illu-caption.old`·`illu-1-orig.png` 3.4MB·`illu-2-orig.png`·`illu-2-again.png`·`gen/`(옛 생성기 대조 사본 A·B)) · `.cache/ch23-01-view/`(`illu-1-1100.png`·`illu-2-1100.png`) · `qa/upgrade/gates-wip-01-01.json`·`gates-wip-01.json`(마감 `gates-after.json`으로 갈음) · `qa/upgrade/__pycache__/`(캡션을 쓸 때 생성기를 모듈로 읽어 생김).

## 14. 마지막 설명 손질 (다시 실행 없음)

- 비유 말 여섯 곳(`/tmp/ch23-01/reps1.json`, 삽화 배열에 맞춤 — §7)과 `_src` 두 곳(`/tmp/ch23-01/reps2.json` 뜻 — b3 「한도에 닿아 멈춘 실행을 이어 가는 일은」 → 「멈춘 실행을 저장된 자리부터 이어 가는 일은」(04·05는 실행 한도가 아닌 강제 종료·실패를 다룸), b7 「실패해 멈춘 실행의 체크포인트와 저장 시점 … 04절·05절」 → 「저장 시점은 04절, 실패해 멈춘 실행을 이어 가는 일은 05절」). 생성기·`_src`(·노트북 마크다운) 함께, `run_section.sh … --no-exec` → G1~G7 0, `pack.py` 다시. 노트북 `code_sha256`·`outputs_sha256`·`executed_at` 그대로.

## 마감 반영 (2026-09-25, 검토 1차 `review-round1-A.md`·`review-round1-B.md`)

- **A-1 [중] 「이어 실행」 한 뜻**(챕터 리드 결정 — Durable Execution 풀이 「멈춘 실행을 저장된 자리부터 이어 가는 일」 하나로): b4 소제목 「이어 실행에서 칸 값이 정해지는 차례」 → 「같은 스레드로 다시 부를 때 칸 값이 정해지는 차례」 · 노트북 6절 제목 → 「같은 스레드로 한 번 더 실행하기」 · b6 결론 → 「같은 스레드의 다음 실행은 저장된 상태를 그대로 쓰지 않습니다. 그 위에 새 입력을 칸의 규칙대로 넣은 뒤, 노드를 실행합니다.」 · 결과 읽기 셀 44 「이어 실행해도」 → 「다시 실행해도」 · 셀 58 「두 번 이어 실행한」 → 「두 번 실행한」. b2와 노트북 1절의 정의는 그대로.
- **A-2** 01-4 도식 읽기 「맨 아래 회색 상자는 세 칸에 모두 해당하는 사실입니다」 → 「맨 아래 회색 상자의 앞 두 줄은 세 칸 모두에 해당하는 사실입니다. 뒤 두 줄은 a와 c 칸에만 해당합니다.」(`.mmd` 그대로 — 다시 렌더 없음).
- **A-3** 8절 결과 읽기 둘째 단락에 「입력을 받은 때의 체크포인트는 첫 단계 0보다 앞이라, 번호가 -1입니다.」(용어 표 정의는 그대로).
- **A-4** `figures/01-5-….prompt.md` 「설명 대상 문장」을 지금 b4 글(「그 판 앞에 모아 둡니다」·「판마다 따로 둡니다」)로.
- 방법: 마감 전용 `.cache/ch23-close/tools/cpatch.py`(생성기·노트북 마크다운·`_src`에 함께, 노트북 코드 셀에 옛 글이 있거나 생성기 코드 문자열에도 걸리면 멈춤) → `run_section.sh … 01 --no-exec`. **다시 실행하지 않음** — `code_sha256` `9d71f6f9522f…`·`outputs_sha256` `4315f7f9e3d3…`·`executed_at` 08:04:29Z 그대로(노트북 파일 `7189b35fdcfc…` → `72e3e7ee8d7f…`, 마크다운만). 생성기 `author_01.py` `534de7c35fd4…` → `9d93a1e622b7…`, `cells()`·`src_html()`이 노트북 59/59·`_src`와 같음. 게이트 G1~G7 0(검사 문장 349 → 352).
