# 03절 진단 — 상태 기록과 다른 분기 재실행 (experiment, 본문 마지막 절)

- 작업일 2026-09-25 · 생성기 `qa/upgrade/author_03.py`(`6ec79811…`) · 노트북 `labs/part6/ch24-human-in-the-loop/notebooks/03-상태-기록과-다른-분기-재실행.ipynb`(`e7649d5a…`) · 본문 `_src/03-상태-기록과-다른-분기-재실행.html`(`a6eabd0d…`) · 빌드 HTML `03-상태-기록과-다른-분기-재실행.html`(`d1d9e365…`) · 도구 파일 `notebooks/approval_tools.py`(`b40aab98…` → **`d562c9e67c56cab1a6e8435e7f926a7c1858a621faf5f3a9fdaa51a632f1b31f`**).
- 형식 **experiment 유지**, 슬러그·제목 그대로(들어오는 링크 0 — Part 목차는 `_build_index.py`가 다시 만듦), 절 meta 「강의 1h | 실습 2h | 새 용어 3」(시수 그대로 — 챕터 합 강의 1+1+1 = 3h · 실습 1.5+1.5+2 = 5h 유지).
- **모델 요청 0번 · API 키 셀 없음**(챕터 리드 결정 1, M1). 사람의 답은 셀에 적은 값(`"approve"`)을 `Command(resume=…)`에 넣습니다 — 준비물·b5에 그 문장.

## 1. 게이트 전후

| 구분 | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 수정 전(`gates-before.json`) | 5 | 81 | 3 | 0 | 0 | 0 | 5 | 22 | 3 | **33** |
| 첫 실행 전(`gates-wip-03-03.json` 첫 판) | 28 | — | 0 | 0 | 0 | 0 | 0 | 3 | 18 | 21(G6 3은 실행 전 고침, G7은 그림 전) |
| 마지막(`gates-wip-03.json`, `--no-exec`) | **28** | **412** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G6 셋: 70자 넘는 문장 셋(b4 「다른 상황에 적용」 모델 노드 문장 · b8 다음 학습 문장 · b10 `_loop.py` 줄) → 실행 전에 둘로 나누거나 줄임(`gates-wip-03-03.json`은 고친 뒤 다시 잰 판으로 덮임 — G1 0 · G2 0 · G6 0 · G7 18).
- 게이트 밖 확인(과제 기준): 준비 셀이 아닌 셀 최대 **9줄**(≤10, `shape.py`) · 함수 본문 최대 **6줄**(`find_before`, ≤8) · 셀당 정의 하나 · 정의 넷(`quote`·`discount`·`ask_price`·`find_before`) + 상태 형식 하나(`PriceState`).
- AST 따로(`/tmp/ch24-03/tools/extra_check.py` — 02 판 그대로, 노트북·도구 파일): 금지 문법 **0건**, 허용 표시 하나(마지막 셀 키워드 없는 `sorted` — Ch 23 선례). f-string·내포식·제너레이터 식·조건 표현식·`lambda`·`elif`·`next`·`set`·`.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·튜플 풀기·별표 풀기·`{**…}`·`while`·`try`·숫자 밑줄·`Path`·`unlink`·데코레이터·세미콜론 0. 호출 두 겹은 `print(len(x))`·`print_history([x])`·`print("…", price_calls.count(…))`까지(세 겹 0). 식 안 숫자는 `unit_price = 2500`·`full_percent = 100`처럼 이름을 붙임(`1 - sample_rate`의 1만 그대로).
- 금지어(`/tmp/ch24-03/tools/ban24.py` — 01·02 판 그대로, 노트북 설명·주석·`_src`·캡션·`.mmd`·도구 파일): 참 금지어 **0건**. 남은 걸림 27은 모두 거짓 양성 — 제목·슬러그의 「분기」·「재실행」 · 「체크포인터」 안 「포인터」 · 용어 표와 노트북 5절 「새 가지(fork)」(원어 풀이) · 03-3·03-4 `.mmd` 라벨과 alt의 「만든 자리 fork」(라이브러리가 적는 값 `fork` — Mermaid 라벨은 백틱을 못 씀) · 도구 파일 코드 변수 `snapshot`(Ch 23 01 코드 그대로) · 옛 그림 `figures/03-흐름.caption.md`의 「분기」(본문 참조 0, 마감 몫).
- 코드 줄(`count_code.py`) **43 → 137**(+94), 코드 셀 **5 → 28**. 도구 파일 코드 줄 30(01 판 + 함수 둘). 챕터 합계 125 → 441 — 강사 확인 대상(§8).

## 2. 수정 전 주요 문제 (옛 판 `before/notebooks/03-…ipynb`·`before/_src/03-*.html`)

1. 한 셀에 노드 함수 둘(`quote`·`discount`) · 노드 힌트·반환 힌트 · 칸 `trace: list[str]` · f-string 안 계산 `f"discount:{state['rate']}"` · 숫자 밑줄 `10_000` · 식 안 숫자 `(1 - state["rate"])` · `State` 한 이름(01·02와 칸이 다름).
2. 기록에서 고르기가 `next(item for item in history if item.next == ("discount",))`(제너레이터 식 + `next`) · 기록 출력이 내포식 + `.get("step")` + `reversed` · 설정 딕셔너리 비교 출력 `checkpoint ids differ: True`.
3. **소수 잘라 내기 함정**: `int(10000 * (1 - rate))` — 0.33이면 **6699**(기기 Python 3.12.13: `10000 * (1 - 0.33)` = `6699.999999999999`). 학생이 값을 바꿔 보면 틀린 가격이 나옴.
4. 값을 바꾸지 않은 다시 실행(`fork`)·고른 자리 뒤 멈춤 표시 다시 멈춤 — 옛 판에 없음(b7 「interrupt는 다시 실행」은 실행하지 않은 문장).
5. 결과 읽기 0 · 제목 셀·준비물·그림 첨부 없음 · b5 「확인할 점」 = b6 둘째 단락(같은 글 두 번) · b4 「정의」·「코드를 읽는 순서」가 같은 말 두 번.
6. 금지어·어려운 말: 「분기」 본문 20·노트북 8·주석 1 · 반환 · snapshot · trace · time travel · fork · 경로 · 보상 작업·격리(Ch 31 몫, 실행 안 함) · reducer · 파라미터 · 프롬프트 · 임계값 · 시나리오. b7 「LLM 호출 … 다시 실행」은 모델 없는 절에서 실행하지 않은 문장.
7. 그림: `{{svg:03-흐름}}` 한 장(옛 `_gen_figures.py` 상자 넷), Mermaid·삽화 0. 참고 자료 넷이 세 절 모두 같음(확인일 09-14).

## 3. 바꾼 것 (결정)

- **가격 그래프(상태 형식 `PriceState` — 칸 `quantity`·`base_price`·`percent`·`final_price`·`answer`, 규칙 없음)**: 노드 셋 `quote`(한 개 값 2500 × 수량) → `discount`(정수 백분율 `base_price * (100 - percent) // 100`) → `ask_price`(01 모양 멈춤 표시, 질문 값 `{'final_price': …, 'question': '이 가격으로 결제할까요?'}`). 노드는 02처럼 목록 `price_calls`에 이름을 적어 실행 횟수를 셈. 스레드 `price-2403`(01 `order-2401`·02 `order-2402`에 이어 절 번호).
- **정수 백분율의 까닭을 출력으로(2절 처음 셀)**: `소수 할인율로 계산한 값: 6699.999999999999` · `int로 소수점 아래를 버린 값: 6699` · `정수 백분율로 계산한 값: 6700`. `//`를 처음 쓰는 자리에서 한 문장.
- **결정적 장면(챕터 리드 결정)**: 첫 실행(할인 10 → 질문 값 9000 → `approve`) → `get_state_history` 다섯 줄을 도구 파일의 `print_history`로 출력 → **이 절이 처음 가르치는 함수 `find_before(history, node_name)`**(`for` + `in` + `break`, 없으면 `None`)로 다음 노드가 `discount`인 단계 1 체크포인트를 고름 → `update_state(chosen.config, {"percent": 20})` → **만든 자리 `update`·단계 2·다음 노드 `('discount',)`·부모 = 고른 체크포인트(`True`)** → `invoke(None, branch_config)` → **`['discount', 'ask_price']`만 실행, 질문 값 8000에서 다시 멈춤** → 스레드 설정으로 `approve` → 목록 8줄에 두 가지가 섞여 남음 → 스레드 설정 `8000` ↔ 따로 담아 둔 설정 `9000`(`assert`).
- **값을 바꾸지 않고 다시 실행(7절, 노트북에서 실행)**: `invoke(None, chosen.config)` → `['discount', 'ask_price']` 다시 실행, 질문 값 9000에서 다시 멈춤, 목록 맨 앞 둘 `3 | loop | ('ask_price',)`·`2 | fork | ('discount',)`(`assert` 만든 자리 `fork`) — 설치판 `pregel/_loop.py` 952~971행과 같음. 이 가지는 멈춘 채 둠.
- **멈춤 표시 다시 멈춤(01·02와 이음)**: 5·7·8절 세 번 모두 확인 노드가 새로 계산한 가격을 질문 값에 담아 다시 멈춤 — 공식 문서 「interrupts are always re-triggered during time travel」과 같음.
- **값 바꿔 보기(8절)**: 같은 체크포인트에 할인 33 → 질문 값 **6700** → `approve`(스레드 설정 — 7절에 멈춘 채 둔 가지가 아니라 가장 최근 가지가 답을 받음).
- **9절 견주기**: 다 끝난 체크포인트만 `33 | 6700 | approve`·`20 | 8000 | approve`·`10 | 9000 | approve`(최신 것부터) · `quote 실행 횟수: 1`(`assert`)·`discount 4`·`ask_price 7` · 체크포인트 13 · `find_before`로 다시 고르면 8절의 `2 | update | ('discount',)`(할인 33)이 나옴 → 「돌아갈 체크포인트는 고른 때 변수에 담아 둔다」(b7).
- **새 말 셋(meta 3)**: **지난 체크포인트에서 다시 실행(Time Travel)**(지난 체크포인트 하나를 골라 그 자리부터 다시 실행 · 찍어 둔 사진을 보고 줄의 한 자리로 돌아가 다시 세움 · `invoke(고른 설정)`+`None`) · **값 고쳐 넣기**(고른 체크포인트의 칸 값 일부를 바꾼 체크포인트를 새로 만듦 · 다시 세울 자리의 도미노 하나를 다른 색으로 · `update_state`, 만든 자리 `update`) · **새 가지(fork)**(지난 체크포인트 하나에서 이어 붙여 새로 쌓은 체크포인트 줄 · 넘어진 원래 줄 옆에 세운 새 줄 · 만든 자리 `update`·`fork`에서 시작, 원래 가지와 한 목록에 섞임). 「분기」·「갈래」·「재실행」 본문 0(제목·슬러그에만), 제목 풀이는 「절 제목은 지난 체크포인트로 돌아가 값을 바꾸고, 그 자리부터 새 가지로 다시 실행하는 일을 가리킵니다」(두 글자 없이). `source`는 Ch 23 01 말 **「만든 자리」**(`print_history` 라벨 그대로) — 과제 지시의 「원천」은 본문에 쓰지 않음.
- **ID·시각 출력 0**: 설정 딕셔너리째 출력하지 않고 `print_history`(단계 번호·만든 자리·다음 노드·칸 값)와 칸 값·`True`만. 첫 실행의 끝 설정은 변수에만 담음.
- **도구 파일(결정 4, 과제 예외)**: `approval_tools.py` = `author_01.TOOLS`(01 함수 셋, 글자 그대로 — `startswith` 대조) + `print_history`(`# Ch 23 01절에서 배웠습니다 — 01절 노트북 8절의 같은 이름 함수를 옮겼습니다`, Ch 23 01 노트북 셀 글과 **문자열·AST 모두 같음** — 생성기 `checks()`) + `find_before`(`# Ch 24 03절에서 배웠습니다 — 03절 노트북 4절의 같은 이름 함수를 옮겼습니다`, 노트북 셀과 같은 문자열 `DEF_FIND`). import 새로 0. 이 절 노트북은 `print_history`만 가져오고 준비 셀에 고정 세 문장 + 커널 폴더 문장 + 실행 도구 문장. `find_before`는 처음 가르치는 절이라 노트북에 적음(§2-7 3번), 도구 파일 판은 04가 가져올 몫.
- **01 영향 확인**: 새 도구 파일로 01 노트북 사본을 `PYTHONPATH` 없이 `--cwd`(도구 파일 폴더)로 새 커널 실행 → `PASS 28 cells`, 셀별 출력 **28/28 같음**, `code_sha256` `7187f7a39f3f…` 그대로(01이 가져오는 이름 셋 그대로). 01 노트북 파일은 다시 실행하지 않음(`9f25361b…` 그대로).
- **파일 쓰기 0**: 준비 셀 셋 모양은 01 그대로(설치 셀 `author_01.INSTALL`과 같음, 임시 폴더 셀은 `author_01.FOLDER`에서 `ch24-01-` → `ch24-03-`만 — `checks()`), 마지막 셀 `작업 폴더의 파일: []`·`파일 수: 0`. 지우는 줄 0.
- **재지 않은 것**: 걸린 시간 0 — 준비물의 「2초 안에」는 셀 실행 기록(A 14:52:28.14~29.17Z)으로 적은 값.
- **다음 절(과제 지시·Ch 23 06 선례)**: 본문 마지막 절이라 b8·노트북 정리 끝을 「04절 실습에서는 이 챕터에서 배운 것을 작은 흐름 하나에 모아 실행합니다.」로 — **링크 없음**(04 파일이 아직 없음, Ch 23 06·Ch 21 06 선례). 옛 판·첫 판의 Ch 25 문장은 뺌(04가 Ch 25로 이음). 그림·A/B 실행 뒤 설명만 고친 것이라 `mdpatch.py`(노트북·생성기) + `--src-only` → `--no-exec`, 코드·출력 그대로(셀별 28/28 B와 같음).

## 4. 새 커널 실행

- 노트북 밖 먼저: `/tmp/ch24-03/probe/probe.py`(같은 그래프·같은 차례) **두 번 출력 같음** · `probe2.py`(이어 붙이기 규칙 칸에 값 고쳐 넣기 → `['a', 'edited']` · `as_node="b"` → 다음 노드 `()`·만든 자리 `update`) **두 번 같음**.
- 사본 T(`/tmp/ch24-03/T/T.ipynb` + 도구 파일 사본, `execute.py`) `PASS T.ipynb: 28 cells`(14:52:21Z) — 실습 폴더에 `.failure.json`이 남지 않게 먼저.
- **A** `PYTHONDONTWRITEBYTECODE=1 env -u OPENAI_API_KEY bash run_section.sh … 03` → `PASS 03-상태-기록과-다른-분기-재실행.ipynb: 28 cells`, 셀 실행 14:52:28.14~29.17Z(UTC), `code_sha256` **`12b29f1517d5f8b90c041487a6c8ae0c14a1c6a1710cbc3d28129f7c5e74cdbd`**, `outputs_sha256` `aab2462d34f9…`. (그림이 아직 없어 첨부 단계에서 멈춘 것은 예정대로.)
- **B**(그림 그리기 전) 사본 `/tmp/ch24-03/B/B.ipynb`(A에서 출력만 지운 사본 + 도구 파일 사본, `execute.py`, 같은 환경 변수, 14:52:40Z) → PASS. **셀별 출력 28/28 같음**(`cmpout.py`, T도 28/28). `outputs_sha256`은 B `0482bf847552…` ↔ A·T `aab2462d34f9…` — 설치 셀 출력이 B에서 스트림 둘로 나뉘어 온 차이뿐(글은 같음, 01·02와 같은 현상).
- 그 뒤 코드·출력은 고치지 않음(본문·그림만 `--src-only`·`--figures` + `run_section.sh … --no-exec`). 노트북 `metadata.verification` 그대로(`executed_at` 14:52:29Z), 첨부만 바뀜(`03-1` PNG).
- `verify.py --chapter`(`run_section.sh` 안): `PASS 3 sections / 84 code cells (max 11 lines)`. 빌드 HTML `{{` **0건**. 01·02 HTML은 다시 빌드했지만 바이트 같음(`09f46b30…`·`8f502dfb…`).
- 실습 폴더 `notebooks/__pycache__`·`qa/upgrade/__pycache__` 만들지 않음(`PYTHONDONTWRITEBYTECODE=1`, 생성기 첫머리 `sys.dont_write_bytecode = True`, 손으로 부를 때 `python3 -B`). `uv run --project labs/…`는 늘 `UV_CACHE_DIR`·`UV_PROJECT_ENVIRONMENT`·`UV_NO_SYNC` 셋과 함께.

## 5. 설치판 확인 (`langgraph 1.2.11`, 노트북 밖)

- `langgraph/pregel/_loop.py` **952~971행**(02 인계 행 번호 그대로 확인): 952~954 주석 「When time-traveling (replaying from a specific checkpoint), save a fork checkpoint so the replayed execution creates a new branch」 · 958~959 `update_state`로 만든 `update`·`fork` 원천에서는 건너뜀 · 971 `self._put_checkpoint({"source": "fork"})`.
- `langgraph/pregel/main.py` ~~1733~1734행~~ **→ 마감에서 바로잡음(검토 B-1): 1733~1734행은 `values is None and as_node == END` 갈래라 노트북이 지나지 않음. 노트북의 `update_state`는 `main.py` 2019행(`step=step + 1`)이 `pregel/_checkpoint.py` 117행 함수를 부르고, 그 128행이 `"source": "update"`를 적음** · **2522~2524행**(`update_state` 독스트링 — `as_node`를 주지 않으면 마지막으로 갱신한 노드) · 1480행 `get_state_history`.
- 공식 문서 Time Travel `https://docs.langchain.com/oss/python/langgraph/use-time-travel` — 2026-09-25 `WebFetch`: 「Replay re-executes nodes—it doesn't just read from cache. LLM calls, API requests, and interrupts fire again and may return different results.」 · 「History is in reverse chronological order」 · 「`update_state` does not roll back a thread. It creates a new checkpoint that branches from the specified point. The original execution history remains intact.」 · 「interrupts are always re-triggered during time travel. The node containing the interrupt re-executes, and `interrupt()` pauses for a new `Command(resume=...)`.」 · 개요 「Replay: Retry from a prior checkpoint. Fork: Branch from a prior checkpoint with modified state」 — **문서는 값을 바꾸지 않은 다시 실행을 새 가지와 나눠 설명하지만 설치판은 `fork` 체크포인트를 만듦** → 본문은 출력 기준(b6 한 단락), 문서는 「노드를 다시 실행한다」까지만.

## 6. 그림

- Mermaid **4장**(설계표 `03-figures.md`): 03-1 고른 체크포인트에서 이어 붙인 새 가지(폭 657, 공통 회색 상자 + 칸 둘 — Ch 13 갈림길로 보이지 않게, 점선 없음) · 03-2 첫 실행의 체크포인트 목록과 고른 자리(497, 함수 상자에서 점선) · 03-3 값을 고쳐 넣은 가지와 그대로 다시 실행한 가지(630) · 03-4 다 끝난 가지 셋과 노드 실행 횟수(561) — 모두 868 이하, PNG 네 장 직접 열어 확인. **빨강 0**(experiment, 오류 장면 없음), **보라 0**, 고쳐 넣은 값·`None` 초록, `find_before` 파랑, 출력 노랑, 공통 체크포인트 회색. 라벨 숫자는 모두 출력에 있음(단계 -1~4·`10000`·`10`/`20`/`33`·`9000`/`8000`/`6700`), 개수·횟수는 한글. 첫 렌더에서 저절로 꺾인 라벨(03-1·03-3 공통 상자)을 `<br>`로 미리 나눠 다시 렌더.
- 삽화 **1장** `03-5-넘어진-줄-옆에-새로-세운-줄`: job **`b6d66b2b-9e64-4f57-88fb-e4f905ccbb7e`**, **1차 채택(재생성 0)**, 거래 2026-09-25T14:53:44Z 「Nano Banana Pro −2」(이 절 몫 **2크레딧**, 생성 전 잔액 2427.75 · 바로 앞 거래 14:26:19Z는 02 몫). 원본 `ee42eb50…`(2752×1536) → 1100×614 `b8427c9a…`, 다시 받은 결과와 **픽셀 대조 차이 0**(bbox `None`). 저장 PNG와 같은 사본·원본 잘라 낸 사본을 열어 셈: 나무 도미노 한 줄(열다섯) 모두 넘어짐 · 가운데쯤에서 주황 줄이 오른쪽 위로 · 주황 넷 넘어짐 → 빈 탁자 자리 → 맨 끝 둘 서 있음 · 글자·숫자·사람·손·컵·구슬 없음. 빈자리가 도미노 한 폭보다 좁아 그림 읽기에 「빈자리를 조금 둔 뒤」로 적음(자세히는 `.prompt.md`). 비유 계열 「도미노 줄과 비워 둔 자리」 03 후보 그대로, 「조각」 0.
- 옛 그림 `figures/03-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 참조 0, 캡션에 「분기」 — 마감 몫).

## 7. 공식 문서·참고 자료 (b10에 날짜·URL·문장)

- Time Travel(위 §5) · 설치판 `_loop.py` 952~971행 · `main.py` ~~1733~1734행~~ 2019행·`_checkpoint.py` 128행(마감 B-1)·`main.py` 2522~2524행 · Ch 23 01절(`print_history`·체크포인트 목록). 01·02의 Interrupts 문서는 이 절 b10에 되풀이하지 않음.

## 8. 강사 확인 대상

1. 제목 말 「분기」·「재실행」(본문은 새 가지·다시 실행, 제목 풀이 한 문장 — 두 글자 없이).
2. 새 말 셋 「지난 체크포인트에서 다시 실행(Time Travel)」·「값 고쳐 넣기」·「새 가지(fork)」 — 실습 04가 이어 씀. `source`는 Ch 23 말 「만든 자리」.
3. 가격 소재를 정수 백분율로(옛 소수 할인율 → 정수 칸 `percent`), 2절에 소수 계산 견줌 셀 하나를 더함(6699 ↔ 6700).
4. 값을 바꾸지 않은 다시 실행(`fork`)을 노트북에서 실행해 보임 — 공식 문서 개요 「Replay … / Fork: Branch …」와 설치판 동작의 표현 차이를 b6에 적음.
5. 모델 없는 절(M1) · 코드 줄 43 → 137(셀 5 → 28) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘.
6. 도구 파일에 함수 둘(`print_history`·`find_before`)을 더함 — `author_02.py` `checks()`의 도구 파일 대조가 이제 맞지 않음(§10·인계).

## 9. 완료·대기 챕터 문장 대조 (`grep -rn 'time travel\|update_state\|시간 여행\|Ch *24' …/ch2[5-9]-*/_src …/ch3*/_src textbook/part7` — 고치지 않음)

- **time travel·update_state·시간 여행을 말하는 뒤 챕터 문장 0**(Part 6 Ch 25~29 `_src`·Part 7 전체). 03 슬러그를 링크하는 뒤 챕터 파일 0.
- **Ch 25 01·02·03 b3** 「Ch24에서 interrupt와 재개 사건을 확인했습니다」 → `interrupt`와 이어 가기는 01·02로 참, 「사건」(스트림 사건)은 Ch 25 몫 — **부분 참** 그대로(01·02 판단과 같음). 03 b8은 04 실습을 가리킴(04가 Ch 25로 이을 몫).
- **Ch 27 01 b3** 「Ch 24는 사람 승인을」 → 참. **Ch 27 08 b3** 「도구 실행 경계」 → 03도 도구 호출 승인 없음 — **부분 참** 그대로.
- **Ch 28 03 b3** 「사람이 승인해야 하는 작업 경계」 → 참. **Ch 30 06 b3**(+ `_src/_generate.py` 76행) 「Ch24의 중복 실행 방지 원칙」 → 01로 참(03은 바꾸지 않음, b7에 「고른 자리 뒤 노드가 파일에 쓰면 다시 실행할 때 한 번 더 적음 — 01절 Before처럼」 한 줄).
- **Part 6** `labs/part6/continuity-guide.md` 10행 「Ch24 중단·재개, 과거 상태에서 분기」 → 뜻은 참(03이 지난 체크포인트에서 새 가지), 말 「분기」는 마감 때 볼지 · `textbook/part6/_build_index.py` 22행 설명 「과거 상태에서 다른 분기를 실행합니다」 → 뜻 참, 말 「분기」(마감 몫) · Part 7 `qa/before-integration/build_index.py` 52행(절 수 3, 기록만).
- 챕터 안: 01 b2 「Time Travel은 지난 체크포인트로 돌아가 다시 실행하는 일이고, 03절에서 다룹니다」 → **참** · 02 b4·b8·노트북 정리 「03절에서는 지난 체크포인트를 골라 값을 바꾸고, 그 자리부터 다시 실행해 봅니다」 → **참**(4·5절).

## 10. 챕터 밖 수정

- `textbook/_notebook/checks/notebook-contracts-part6-ch24-human-in-the-loop.json`(`verify.py`가 다시 씀, `a9436d1f…` → `cfbce0b9…`).
- 챕터 실습 폴더 도구 파일 `approval_tools.py`(과제 예외 — 함수 둘 더함). 챕터·Part 공개 목록은 경로 배열이라 그대로(`c629078f…`·`a7741594…`), zip 둘·`bundle-execution.json`은 고치지 않음(마감 몫 — zip 안 도구 파일은 옛 판, 01 새 `code_sha256`도 마감이 적음).
- **알려진 어긋남(고치지 않음)**: `qa/upgrade/author_02.py` `checks()` 셋째 `assert author_01.TOOLS_PATH.read_text() == author_01.TOOLS`가 이제 거짓 → 02 생성기를 다시 돌리려면 그 줄을 `startswith(author_01.TOOLS)`로(또는 `author_03.TOOLS`와 대조) 고쳐야 함. `author_01.py`를 `--src-only` 없이 돌리면 도구 파일을 01 판(함수 셋)으로 덮어써 03 노트북 가져오기가 멈춤 → `--src-only`로만 부르거나, 마감이 함수 둘을 `author_01.TOOL_PARTS`로 옮김(Ch 23 07 선례 — 마감이 `author_06.TOOLS`에 `new_prefix`를 넣음). `author_03.py`는 디스크 파일이 03 판 뒤에 더 붙은 판이면 덮어쓰지 않음(04가 함수를 더해도 안전).
- 그 밖 0: `chapter.json`·`_build_index.py`·실습 폴더 README·`pyproject.toml`·`uv.lock`·공용 도구·Ch 23 파일 그대로. 기기 임시 `/tmp/ch24-03/tools/`는 02 판 복사.

## 11. 남은 것과 지우지 않은 것

- **마감 몫**: 03 b8의 「04절」에 링크 `<a href="04-…-실습.html">`(04를 만든 뒤 `author_03.py`의 `_src` 문장 → `--src-only` → `run_section.sh … 03 --no-exec`, 노트북은 링크 없이 그대로 둘 수 있음) · 옛 그림 `figures/03-흐름.*` 삭제 승인·챕터 공개 목록 옛 SVG 줄 빼기 · `chapter.json` `objectives` 셋째 줄 「새 분기를 실행」 → 새 가지 말 · `_build_index.py` 22행 설명 「다른 분기」 · 실습 폴더 README(「승인 결과는 실습 폴더의 로컬 파일에만 기록」 — 01부터 거짓) · zip·`bundle-execution.json`(도구 파일 새 판 + 01 새 `code_sha256` `7187f7a39f3f…`) · §10의 생성기 대조 줄.
- **지워야 하지만 지우지 않은 것(삭제 승인 대상)**: `qa/upgrade/gates-wip-03-03.json`·`gates-wip-03.json` · `$ROOT/.cache/ch24-03-view/`(`illu-1-1100.png`·`crop-gap.png`·`crop-row.png`) · 기기 `/tmp/ch24-03/`(probe·T·A·B·one·illu·tools·`manifest-now.txt`) · 기기 세션 임시 폴더 `$TMPDIR/ch24-03-*` 셋(노트북 실행 T·A·B가 만든 빈 폴더)과 01 사본 확인이 만든 `$TMPDIR/ch24-01-*` 하나(`ch24-01-n3j5gejg` — 기록 파일이 든 임시 폴더) · `.cache/vm/venv-ch24-human-in-the-loop`(챕터 끝까지 씀).

## 마감 반영 (2026-09-25, 검토 1차)

노트북은 다시 실행하지 않았습니다(`code_sha256` `12b29f1517d5…`·`outputs_sha256` `aab2462d34f9…`·`executed_at` 14:52:29Z 그대로). 고친 방법은 01과 같고, `author_03.py --figures`로 03-3 `.mmd`와 03-4·03-5 캡션 파일이 바뀜 → **03-3만 `render_mermaid.py --only 03-3- --force`로 다시 렌더**(노트북 첨부는 03-1뿐이라 첨부 그대로).

- **B-1 [중] 설치판 행 번호**: b4 「고른 자리부터 실행하면 일어나는 일」 셋째 단락과 b10 다섯째 항목을 `main.py` 2019행(단계 번호 +1)·`_checkpoint.py` 128행(만든 자리 `update`)으로. 챕터 가상환경 설치판에서 두 행을 다시 읽어 확인(2016~2019행 `create_checkpoint_plan_for_update_state_api(…, step=step + 1, …)`, `_checkpoint.py` 117행 함수·128행 `"source": "update"`). 위 §5·§7도 바로잡음.
- **B-2 [하]**: b6 새 단락 — 문서 「Fork」 절(`update_state`)은 만든 자리 `update`, 「Replay」 절(그대로 다시 실행)은 만든 자리 `fork`를 남김(엇갈려 짝지어짐).
- **B-3 [하]**: 03-4 캡션 → 「다 끝난 가지 셋(원래 가지 포함)과 멈춘 채 둔 가지 하나가 한 목록에 남았고, 견적 노드는 한 번만 실행되었습니다.」
- **B-4 [하] 03-3**: 결과가 든 회색 공통 상자에서 두 칸으로 가던 실선을 없앰 — 출발 자리 「단계 1에서」는 두 칸 제목에, 두 장면 공통 결과(`quote` 다시 실행 없음 · `ask_price`에서 다시 멈춤)는 **두 칸 아래 회색 상자**(`~~~`)로. 상자 일곱 그대로, 폭 630 → **674**, alt·도식 읽기를 새 판대로. PNG를 직접 열어 칸 둘이 나란하고 회색 상자가 화살표 없이 아래에 있음을 확인.
- **B-5 [하] 2절 견줌 셀(셀 9)**: `print` 인자 안 계산·식 안 숫자 `1` — 코드 셀이라 **고치지 않음**. 결과 읽기에 바로잡을 사실 오류는 없음(출력 값과 설명이 맞음). **다음 재실행 때** `int_price = …` 한 줄과 `one = 1`류 이름을 두고 출력(`textbook/qa/upgrade-final-checklist.md` Ch 24 몫).
- **B-6 [하] 03-5 삽화**: 저장 PNG를 직접 열어 봄 — 주황 넷과 서 있는 둘 사이의 틈이 도미노 한 개 폭보다 좁음. **다시 만들지 않고**(Higgsfield 0) alt·캡션·그림 읽기를 보이는 대로(「좁은 틈」, 틈의 폭은 짝짓지 않음) 고침. `.prompt.md` 상태 끝에 마감 줄. 다시 만들지는 강사 확인 대상.
- 준비물 「2초 안에」 → 「걸린 시간은 재지 않았습니다.」 · 생성기 머리 설명의 `author_02` 대조 줄 주의 문장을 마감 판으로.
- 게이트 G1~G7 0(검사 문장 412 → 417), 과정 금지어 새 걸림 0.
