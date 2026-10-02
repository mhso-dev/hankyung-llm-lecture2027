# 02절 진단 — Command resume으로 실행 재개 (experiment)

- 작업일 2026-09-25 · 생성기 `qa/upgrade/author_02.py`(`e3699a92…`) · 노트북 `labs/part6/ch24-human-in-the-loop/notebooks/02-Command-resume으로-실행-재개.ipynb`(`5391d97b…`) · 본문 `_src/02-Command-resume으로-실행-재개.html`(`156ccab7…`) · 빌드 HTML `02-Command-resume으로-실행-재개.html`(`8f502dfb…`).
- 형식 **experiment 유지**, 슬러그·제목 그대로(들어오는 링크 0 — Part 목차는 `_build_index.py`가 다시 만듦), 절 meta 「강의 1h | 실습 1.5h | 새 용어 3」(시수 그대로 — 챕터 합 3h·5h 유지).
- **모델 요청 0번 · API 키 셀 없음**(챕터 리드 결정 1, M1). 사람의 답은 셀에 적은 값(`"maybe"`·`"yes"`·`"approve"`)을 `Command(resume=…)`에 넣습니다 — 준비물·b5에 그 문장.
- **도구 파일 변경 없음**: 이 절은 파일을 쓰지 않아 `approval_tools.py`에서 가져오지 않습니다(가져오기 줄·고정 세 문장 없음). 도구 파일 해시 `b40aab98ae6d…` 그대로(생성기 `checks()`가 `author_01.TOOLS`와 디스크 글이 같은지 `assert`). 01 노트북이 가져오는 이름도 그대로, 01은 다시 실행하지 않음(`9f25361b…` 그대로).

## 1. 게이트 전후

| 구분 | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 수정 전(`gates-before.json`) | 4 | 79 | 0 | 3 | 0 | 0 | 5 | 16 | 3 | **27** |
| 첫 실행 전(`gates-wip-02-02.json` 첫 판) | 28 | — | 0 | 0 | 0 | 0 | 0 | 4 | 22 | 26(G6 4는 실행 전 고침, G7은 그림 전) |
| 마지막(`gates-wip-02.json`, `--no-exec`) | **28** | **396** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G6 넷: 70자 넘는 문장 셋(02-3 도식 읽기 · b10 둘) + 코드 이름으로 시작해 조사가 붙은 문장 하나(b4 「`while True`로 …」) → 실행 전에 나눔·어순 바꿈. 그림 뒤 G6 하나(b4 비교와 경계 한 문장 72자) → 둘로 나눔.
- 게이트 밖 확인(과제 기준): 준비 셀이 아닌 셀 최대 **9줄**(≤10) · 함수 본문 최대 **8줄**(`ask_in_loop`, ≤8) · 셀당 정의 하나 · 정의 다섯(`make_question`·`record_counts`·`ask_once`·`after_answer`·`ask_in_loop`) + 상태 형식 하나.
- AST 따로(`/tmp/ch24-02/tools/extra_check.py` — 01 판에 `while`·`try` 허용 표시를 더함): 금지 문법 **0건**. 허용 표시 넷 — `while True` 하나(4절 권하지 않는 모양 셀, 셀 제목·주석·본문에 「권하지 않는 모양」), `try`/`except RuntimeError`·`except KeyError` 둘(6절 오류 받기, 노드 밖 `invoke`를 감쌈), 키워드 없는 `sorted` 하나(마지막 셀, Ch 23 선례). f-string·내포식·제너레이터 식·조건 표현식·`lambda`·`elif`·`next`·`set`·`.get`·`+=`·기본값 매개변수·타입힌트(상태 형식 칸 말고)·반환 힌트·튜플 풀기·별표 풀기·`{**…}`·숫자 밑줄·`Path`·`unlink`·데코레이터·세미콜론 0. 호출 두 겹은 `print(len(x))`·`rows.append(counts)`까지(세 겹 0).
- **게이트는 `while True`를 막지 않습니다**(`upgrade_gates.py` G1·G2는 `ast.While`을 세지 않음, 2026-09-25 확인) → 과제 지시대로 옛 모양을 노트북에서 실행하고 「권하지 않는 모양」을 셀 첫 줄 주석·소제목·본문 b7에 밝힘.
- 금지어(`/tmp/ch24-02/tools/ban24.py` — 01 판 그대로): 노트북 설명·주석·`_src`·캡션·`.mmd`에서 참 금지어 **0건**. 남은 걸림은 모두 거짓 양성 — 「체크포인터」 안 「포인터」, 노트북 제목 셀 「실행 재개」·meta 줄의 슬러그 「재개」.
- 코드 줄(`count_code.py` 세는 법 — 주석·빈 줄 뺌) **32 → 146**(+114), 코드 셀 **4 → 28**. 01(50 → 158)·Ch 23 01(32 → 113)과 같은 늘어남 — 강사 확인 대상(§8).

## 2. 수정 전 주요 문제 (옛 판 `before/notebooks/02-…ipynb`·`before/_src/02-*.html`)

1. **공식 문서 규칙과 반대 모양**: 노드 `review` 안 `while True` + `interrupt` 되풀이(LangGraph Interrupts 「Rules of interrupts」 — 아래 §7). 20줄 셀·집합 `{"approve", "reject"}`·`{**prompt, "error": …}`·f-string `f"허용하지 않는 값: {decision}"`·노드 힌트·반환 힌트·`State` 한 이름.
2. `history count: 3`을 `len(list(graph.get_state_history(config)))`(호출 세 겹)로 출력, 결과 읽기 0 · 제목 셀·준비물·그림 첨부 없음 · b5 「확인할 점」 = b6 둘째 단락(같은 글 두 번).
3. b5 「새 ID로 resume을 보내면 기존 interrupt에 값이 전달되지 않습니다」는 실행하지 않은 문장 → 설치판에서는 **오류 글이 스레드를 알려 주지 않는 `KeyError`**(§5).
4. b3 「앞 절에서 … `Command(resume=False)`가 거절 값을 반환」 — 개선된 01은 `"reject"` 글을 넣음(옛 01 기준 문장).
5. 금지어·어려운 말: 반환 9 · 검증 8 · payload 5 · 런타임 2 · 스키마 2 · 포인터(단독 — 「기다리던 실행을 찾는 포인터」) · 정확히 · 소비 · 분기 · 경로. b7 「감사 기록은 … 별도로 보존」은 실행하지 않은 운영 조언.
6. 그림: `{{svg:02-흐름}}` 한 장(옛 `_gen_figures.py` 상자 넷), Mermaid·삽화 0. 참고 자료 넷이 세 절 모두 같음(확인일 09-14).

## 3. 바꾼 것 (결정)

- **다시 묻기는 조건부 엣지로(챕터 리드 결정 — 공식 문서 규칙)**: 3절 권하는 모양 `ask_once` = 질문 값을 만들어 `interrupt` **한 번** → 목록에 있으면 `{"answer": 답, "error": ""}`, 없으면 `{"error": "허용하지 않는 값: " + 답}` → 조건 함수 `after_answer`(여러 줄 `if`, 오류 글이 빈 글이면 `END`, 아니면 이름표 `"ask_again"`) + 이름표 표 `{"ask_again": "ask_once", END: END}`(Ch 13 03 · Ch 20 03 모양) → `add_conditional_edges`로 같은 노드에 되돌아감(Ch 20 01 되돌아가는 엣지와 견주는 한 문장). 조건 함수는 그래프 없이 직접 불러 `__end__`·`ask_again`을 봄(Ch 20 03 선례).
- **옛 모양을 권하지 않는 모양으로 견주기(experiment)**: 4절 `ask_in_loop` = 노드 안 `while True`에서 `interrupt`를 되풀이(옛 판 구조, 금지 문법만 뺌 — 집합 → 목록 `in`, `{**…}`·f-string → `make_question` 함수). **같은 답 차례 `maybe` → `yes` → `approve`**를 두 모양에 넣고, 노드가 목록에 적는 글 `시작`·`질문`으로 노드 시작 수와 `interrupt` 부른 수를 셈(01의 노드 안 `print`를 셀 수 있게 바꿈 — `record_counts(calls, graph, config, rows)`가 체크포인트 수와 함께 출력하고 한 줄로 모음).
- **결정적 값(두 번 같음, §4)**: 조건부 엣지 모양 시작·부름·체크포인트 `1·1·2 → 3·3·3 → 5·5·4 → 6·6·5` ↔ while True 모양 `1·1·2 → 2·3·2 → 3·6·2 → 4·9·3`. 사람에게 보인 질문 값 넷과 마지막 결과(`{'order_key': 'order-2402', 'answer': 'approve', 'error': ''}`)는 두 모양이 같음. 두 `approve` 셀 끝에 `assert edge_rows[3] == [6, 6, 5]`·`assert loop_rows[3] == [4, 9, 3]`(우리 노드와 라이브러리가 정하는 값).
- **01이 약속한 「허용하지 않는 답이면 다시 묻기」를 이 절이 보임**: 01 `_src` b4 「비교와 경계」·b7·b8·노트북 정리 끝의 02 약속 → 3절 `maybe`·`yes`로 참.
- **실패 장면 둘(받은 오류, 노랑)** — 6절: (가) 3절 설계 객체 `edge_builder`를 **체크포인터 없이 다시 컴파일** → 첫 실행은 오류 없이 `멈춤 표시 수: 1` → `Command(resume="approve")`에서 `RuntimeError: Cannot use Command(resume=...) without checkpointer`(설치판 `pregel/_loop.py` 904~908행). 01이 문서·소스로만 말한 「멈춤 표시를 쓰려면 체크포인터」의 실행 근거. (나) 멈춘 적 없는 스레드 `other`로 `Command(resume="approve")` → `KeyError: 'order_key'`, 스레드 `other`의 칸 값 `{}`·다음 노드 `('ask_once',)`·작업 오류 `KeyError('order_key')`(Ch 23 05 `tasks` 모양), 3절 스레드 `edge` 칸 값 그대로. `try`/`except 오류이름 as error`(Ch 2 05 모양)로 받아 이름·오류 글만 출력 — 노드 밖 `invoke`를 감싼 것이라 01 b7의 「노드 안 `interrupt`를 `try`로 감싸지 않기」와 다르다는 한 문장. 옛 후보 (라) 여러 멈춤 표시·아이디 딕셔너리는 아직 가르치지 않은 것이라 넣지 않음.
- **상태 형식 `ReviewState`**(칸 `order_key`·`answer`·`error`, 규칙 없음 — 01 `ApprovalState`와 칸이 달라 새 이름). 질문 값 = 01 모양 `{"order_key", "question": "결제할까요?"}` + `"allowed"`(허용 답 목록) + `"error"`(오류 글) — `make_question(order_key, error_text)`. 주문 키 **`order-2402`**(01 `order-2401`에 이어 절 번호), 스레드 `edge`·`loop`·`plain`·`other`. 옛 `publish-local`·`review-2402`는 쓰지 않음.
- **파일 쓰기 0**: 준비 셀 셋 모양은 01 그대로(설치 셀 `author_01.INSTALL`과 같음 `assert`, 임시 폴더 셀은 `author_01.FOLDER`에서 `ch24-01-` → `ch24-02-`만 — `assert`), 마지막 셀 `작업 폴더의 파일: []`·`파일 수: 0`. 지우는 줄 0.
- **새 말 셋**(meta 3): **허용 답 목록**(받아들일 값만 적은 목록 · 빈자리에 맞는 도미노 모양 · `allowed_answers`·`in`) · **다시 묻기**(받아들이지 않는 답이면 까닭을 질문 값에 담아 같은 자리에서 한 번 더 멈춤 · 구슬을 치우고 맞는 도미노를 다시 기다림 · 칸 `error` + 조건부 엣지) · **차례 맞추기**(한 노드 안 여러 `interrupt`에 받은 답을 부른 차례대로 맞춤 · 줄을 다시 세우며 전에 놓은 물건을 차례대로 다시 놓음 · `ask_in_loop`, 설치판 `types.py` 866~868행 — 인계 11 「한 노드 안 `interrupt` 여러 번」을 이 절이 처음 가르침). 01 용어(멈춤 표시·질문 값·사람의 답으로 이어 가기·승인 지점) 그대로. 본문 「재개」 0(제목에만), 제목 풀이는 「절 제목은 01절의 `Command(resume=…)`로 멈춘 실행을 이어 가는 일을 가리킵니다」로 「재개」 글자 없이.
- **결과 읽기의 정직성**: 4절 `yes` 셀 — 둘째 부름이 `yes`를 받은 것은 셋째 질문의 오류 글로 보이지만, 첫 부름이 `maybe`를 다시 받은 것은 **셀 출력에 따로 찍지 않았다**고 적고 설치판 소스 행으로 근거를 댐. 02-3 그림도 그 두 상자를 회색 「소스 확인」으로.
- **재지 않은 것**: 걸린 시간 0 — 준비물의 「2초 안에」는 셀 실행 기록(A 14:23:56.50~57.44Z)으로 적은 값(01과 같은 방식).

## 4. 새 커널 실행

- 노트북 밖 먼저: `/tmp/ch24-02/probe/probe.py`(같은 코드 + 끝난 스레드 다시 보내기) **두 번 출력 같음** · 사본 `/tmp/ch24-02/T/T.ipynb`로 `execute.py` `PASS T.ipynb: 28 cells`(14:23:30~31Z) — 실습 폴더에 `.failure.json`이 남지 않게 먼저.
- **A** `PYTHONDONTWRITEBYTECODE=1 env -u OPENAI_API_KEY bash run_section.sh … 02` → `PASS 02-Command-resume으로-실행-재개.ipynb: 28 cells`, 셀 실행 14:23:56.50~57.44Z(UTC), `code_sha256` **`ead91c80882f194d6d58a329197d2637cba1cf77eb8595387dfd832354fd0441`**, `outputs_sha256` `b3385367b194…`. (그림이 아직 없어 첨부 단계에서 멈춘 것은 예정대로 — 그림 뒤 `--no-exec`로 이음.)
- **B** 사본 `/tmp/ch24-02/B/B.ipynb`(`execute.py`, 같은 환경 변수, 14:24:08~09Z) → PASS. **셀별 출력 28/28 같음**(`cmpout.py`, A·T도 28/28). `outputs_sha256`은 B·T `d6b3bdf6ba2e…` ↔ A `b3385367b194…` — 설치 셀 출력이 A에서만 스트림 둘로 나뉘어 온 차이뿐(글은 같음, 01과 같은 현상).
- 그 뒤 코드·출력은 고치지 않음(설명·본문·그림만 `--src-only` + `run_section.sh … --no-exec` 세 번). 노트북 `metadata.verification` 그대로(`executed_at` 14:23:57Z), 첨부만 바뀜.
- `verify.py --chapter`(`run_section.sh` 안): `PASS 3 sections / 61 code cells (max 19 lines)`(19줄은 개선 전 03). 빌드 HTML `{{` **0건**.
- 실습 폴더 `notebooks/__pycache__`·`qa/upgrade/__pycache__` 만들지 않음(`PYTHONDONTWRITEBYTECODE=1`, 생성기 첫머리 `sys.dont_write_bytecode = True` — `run_section.sh`가 `-B` 없이 부르므로). `uv run --project labs/…`는 늘 `UV_CACHE_DIR`·`UV_PROJECT_ENVIRONMENT`·`UV_NO_SYNC` 셋과 함께.

## 5. 설치판 확인 (노트북 밖, `langgraph 1.2.11`)

- `probe.py` 두 번 같음: 위 결정적 값 전부 · 조건부 엣지 모양 체크포인트 기록 단계 -1 `input` → 0 `loop`(`error ''`) → 1 `loop`(`error '허용하지 않는 값: maybe'`) → 2 `loop`(`… yes`) → 3 `loop`(`answer 'approve'`, 다음 `()`) — 노드가 오류 글을 내고 마칠 때마다 한 줄. while True 모양은 -1·0·1 세 줄(멈춘 동안 0에서 `tasks` 멈춤 표시 하나).
- 체크포인터 없는 그래프의 `get_state`는 `ValueError: No checkpointer set`(노트북에서는 부르지 않음).
- **끝난 스레드 `edge`에 `Command(resume="reject")`를 한 번 더** → 오류 없이 칸 값 그대로, 체크포인트 5 그대로, 노드 시작 0 → b7에 「노트북 밖 확인 · 노트북에서 실행하지 않았습니다」.
- 설치판 소스: `langgraph/types.py` 864행(처음부터 다시 실행)·866~868행(여러 `interrupt`는 노드 안 차례로 맞춤, 작업마다 따로)·870~871행(체크포인터 필요) · `langgraph/pregel/_loop.py` 904~908행(`RuntimeError`)·916~920행(여러 멈춤 표시에 값 하나면 `RuntimeError` — 넣지 않음).

## 6. 그림

- Mermaid **5장**(설계표 `02-figures.md`): 02-1 조건부 엣지로 다시 묻는 그래프(폭 657, 조건 함수는 회색 마름모 — Ch 13 03-1 규칙) · 02-2 답마다 본 질문 값과 체크포인트(272) · 02-3 while True 노드가 앞선 답을 다시 받는 차례(262, 소스로만 확인한 두 부름 회색 「소스 확인」) · 02-4 두 모양의 부른 횟수와 체크포인트(665) · 02-5 사람의 답이 질문에 닿지 않은 두 장면(621) — 모두 868 이하, PNG 다섯 장 직접 열어 확인. **빨강 0**(experiment — 권하지 않는 모양도 결과를 냈고, 받은 오류는 노랑), **보라 0**, 넣은 값·사람의 답 초록, 노드·부른 줄 파랑, 출력·받은 오류 노랑, START/END·공통 사실·조건 함수·소스 확인 회색. 라벨 숫자는 `2402` 하나(출력에 있음), 개수는 한글. 첫 렌더에서 02-1 자기 자신으로 돌아오는 점선 라벨이 선과 겹쳐 조건 함수 마름모를 따로 그림 · 저절로 꺾인 라벨을 `<br>`로 미리 나눠 다시 렌더.
- 삽화 **1장** `02-6-빈자리에-놓인-구슬과-도미노`: job **`1939b15e-9adb-4dfb-affd-cbde22c5aca2`**, **1차 채택(재생성 0)**, 거래 2026-09-25T14:26:19Z 「Nano Banana Pro −2」(이 절 몫 **2크레딧**, 생성 전 잔액 2429.75 · 바로 앞 거래 13:52:58Z는 01 몫). 원본 `5bba5d1b…`(2752×1536) → 1100×614 `8bffb4be…`, 다시 받은 결과와 **픽셀 대조 차이 0**(bbox `None`). 저장 PNG와 같은 사본을 열어 셈: 도미노 두 줄 · 위 줄 넘어진 다섯 → 빈자리의 파란 구슬 하나 → 서 있는 일곱 · 아래 줄 가운데 연두색 도미노 하나 → 줄 전체가 오른쪽 끝까지 넘어짐 · 글자·숫자·사람·손·컵 없음(자세히는 `.prompt.md`). 비유 계열 「도미노 줄과 비워 둔 자리」 02 후보 그대로, 「조각」 0.
- 옛 그림 `figures/02-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 참조 0, 캡션에 「반환값」 — 마감 몫).

## 7. 공식 문서 규칙 (b10에 날짜·URL·문장)

- LangGraph Interrupts `https://docs.langchain.com/oss/python/langgraph/interrupts` — 2026-09-25 `WebFetch`:
  - 「Rules of interrupts」: "Do not loop `interrupt` calls using logic that isn't deterministic across executions, including `while True` validation loops. Use a conditional edge instead (see Validating human input)" — b10에 이 문장을 코드 글꼴로 그대로.
  - 「Validating human input」: "Avoid `while True` + `interrupt()` loops inside a single node. Because the node re-runs from the beginning on every resume …, a loop that calls `interrupt()` multiple times causes each resume to replay all previous iterations: the first resume replays 1 iteration, the second replays 2, and so on." · 권장 "call `interrupt()` exactly once, return from the node with the error message stored in state, and use a conditional edge to loop back to the node."
  - 「Do not reorder `interrupt` calls within a node」: "Matching is strictly index-based, so the order of interrupt calls within a node is important."
  - 「Resuming interrupts」: "You must use the same thread ID when resuming that was used when the interrupt occurred." · 「Pause using `interrupt`」: 체크포인터와 스레드 ID.
- 노트북 결과(셀마다 늘어난 부름 둘·셋·셋, 다시 실행된 바퀴 하나·둘·셋)는 문서의 「first resume replays 1 iteration, the second replays 2」와 같음 → 5절 결과 읽기·b4·b6.

## 8. 강사 확인 대상

1. 제목 말 「Command」·「resume」·「재개」(본문은 01 용어 「사람의 답으로 이어 가기」, 제목 풀이 한 문장).
2. **권하지 않는 `while True` 모양을 노트북에서 한 번 실행**(experiment 견주기, 공식 문서가 쓰지 말라는 모양 — 셀·소제목·b7에 밝힘). 게이트는 막지 않음.
3. 모델 없는 절(M1) — 사람의 답은 셀에 적은 값. 실패 장면 둘(받은 오류)을 더함.
4. 코드 줄 32 → 146(셀 4 → 28) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘.
5. Mermaid 5장(상한) — 차례 맞추기 그림(02-3)을 따로 둠.
6. 새 말 셋 「허용 답 목록」·「다시 묻기」·「차례 맞추기」(03이 이어 쓸지).

## 9. 완료·대기 챕터 문장 대조 (`grep -rn 'Command\|resume\|Ch *24' …/ch2[5-9]-*/_src …/ch3*/_src textbook/part7` — 고치지 않음)

- **Ch 25 01·02·03 b3** 「Ch24에서 interrupt와 재개 사건을 확인했습니다」 → `interrupt`와 사람의 답으로 이어 가기는 01·02로 **참**, 「사건」(스트림 사건)은 Ch 25 몫이라 **부분 참** 그대로(01 판단과 같음).
- **Ch 27 01 b3** 「Ch 24는 사람 승인을」 → 참. **Ch 27 08 b3** 「Ch 24의 사람 승인과 이 장의 permissions는 도구 실행 경계를 다룹니다」 → 02도 도구 호출 승인 장면 없음(쓰기 노드 승인·답 검사) — **부분 참** 그대로.
- **Ch 28 03 b3** 「Ch24에서 사람이 승인해야 하는 작업 경계를 확인했습니다」 → 참.
- **Ch 30 06 b3**(+ `_src/_generate.py` 76행) 「Ch23의 thread 분리와 Ch24의 중복 실행 방지 원칙」 → 01 b4·b6·6절로 참(02는 바꾸지 않음). 02의 「사람의 답은 멈춘 스레드 이름으로」(6절)는 「thread 분리」 쪽과도 맞음.
- Ch 26 03 b4의 걸림은 「지연」 글자(관계없음). Part 7 Ch 30 06 `resume-1:0`은 SSE 이벤트 ID(관계없음). 02 슬러그를 링크하는 뒤 챕터 파일 0.
- 챕터 안: 01 `_src` b4·b7·b8·노트북 정리의 「02절에서는 사람의 답을 검사해, 허용하지 않는 값이면 다시 묻는 방법」 → **참**(3절).

## 10. 챕터 밖 수정

- `textbook/_notebook/checks/notebook-contracts-part6-ch24-human-in-the-loop.json`(`verify.py`가 다시 씀, `6e540bbc…` → `a9436d1f…`).
- 그 밖 0: 도구 파일·공개 목록·zip·`bundle-execution.json`·`_build_index.py`·`chapter.json`·실습 폴더 README·`pyproject.toml`·`uv.lock`·공용 도구·Ch 23 파일 그대로. `/tmp/ch24-02/tools/extra_check.py`(기기 임시 사본)만 고침.

## 11. 남은 것과 지우지 않은 것

- **마감 몫**: 옛 그림 `figures/02-흐름.*` 삭제 승인·챕터 공개 목록 옛 SVG 줄 빼기 · `chapter.json` `objectives` 둘째 줄 「승인 입력을 검증하고 … 재개」(「검증」·「재개」 → 이 절 말) · 실습 폴더 README.
- **지워야 하지만 지우지 않은 것(삭제 승인 대상)**: `qa/upgrade/gates-wip-02-02.json`·`gates-wip-02.json` · `$ROOT/.cache/ch24-02-view/`(삽화 확인 사본 `illu-1-1100.png`) · 기기 `/tmp/ch24-02/`(probe·T·A·B·illu·tools·`manifest-now.txt`) · 기기 세션 임시 폴더 `$TMPDIR/ch24-02-*` 셋(노트북 실행 T·A·B가 만든 빈 폴더) · `.cache/vm/venv-ch24-human-in-the-loop`(챕터 끝까지 씀).

## 마감 반영 (2026-09-25, 검토 1차)

노트북은 다시 실행하지 않았습니다(`code_sha256` `ead91c80882f…`·`outputs_sha256` `b3385367b194…`·`executed_at` 14:23:57Z 그대로). 고친 방법은 01과 같고(`gpatch.py` → `--src-only` → `--no-exec`), `author_02.py --figures`로 02-3 캡션 파일만 바뀜(`.mmd` 다섯 그대로 — 다시 렌더 없음).

- **A-4 [중] 「오늘 볼 그림」**: 노트북 셀 1을 생성기 `FIG1_ALT`·`FIG1_READ`(회색 마름모 조건 함수 `after_answer` · 마름모에서 나가는 점선 둘)와 같게(`syncmd.py 02 1`, 첨부 그대로). 마감 전 생성기와 노트북이 다르던 셀은 이 하나뿐이었습니다(`genmatch.py` 58/59 → 59/59).
- **A-5 [중] 실험 해석**: b6에 두 단락 — 노드 시작 수 `6` ↔ `4`의 뜻(목록 밖 답마다 노드를 마치고 새로 시작 · 답 하나에 둘씩) · 권하는 까닭은 부른 수(`1·3·5·6` ↔ `1·3·6·9`, 반복문 쪽이 더 빨리 늚) · 셈 줄은 `interrupt` 바로 앞 줄이라 01절처럼 쓰기가 있으면 두 모양 모두 되풀이되고 반복문 쪽이 더 많음. 노트북 5절 결과 읽기에 같은 뜻 네 문장(둘째 단락 뒤 — 첫 단락 숫자 인용 그대로). **노트북 밖 확인**(`/tmp/ch24-close/probe/p02five.py`, 챕터 가상환경 파이썬, 모델 없음, 두 번 같음): 목록 밖 답 다섯 + `approve`면 시작·부름·체크포인트 조건부 엣지 `12·12·8` ↔ 반복문 `7·27·3`(반복문 누적 부름 1·3·6·10·15·21·27) — **b7에만** 「노트북 밖에서 … 이 장면은 노트북에서 실행하지 않았습니다」로 적음(정리·그림·복습에 없음).
- **A-6 [중] Ch 16 01 「허용 목록」·Ch 18 02 「되묻기」**: 과정 요약·두 절 `_src`로 뜻을 확인 — 「허용 답 목록」은 같은 뜻(허용하는 값의 목록을 `in`으로 검사, Ch 18 02가 「이 절의 허용 목록은 …」으로 이어 쓴 선례) → **이어 쓰는 말로 두고 새 말에서 뺌(meta 새 용어 3 → 2)**, 말은 「허용 답 목록」 그대로(코드 주석·02-1·04-1 라벨에 있음). 「다시 묻기」는 뜻이 다름(Ch 18 되묻기는 흐름을 끝내고 되묻는 쪽 · 이 절은 멈춘 그래프가 같은 자리에서 다시 멈춤) → 새 말 그대로, 가르는 문장을 b3 새 단락·용어 표 두 줄·노트북 2절·3절 첫 자리에.
- **A-7 [하]**: b6 둘째 해석 단락(「설치판 설명(`types.py` 866~868행)대로라면 … 다시 내놓습니다」·「부름마다 받은 값은 셀에 찍지 않았습니다」) · 02-3 캡션(「소스 설명대로라면 … 다시 받습니다」) · 복습 2 해설(둘째 부름은 셋째 질문의 오류 글로 보임, 첫째 부름의 `maybe`는 설치판 설명으로 앎).
- **A-8 [하]**: 노트북 6절 앞(셀 48)에 「감싸는 `try`가 없으면 이 셀은 오류에서 멈춥니다. 셀에서는 그 오류 이름만 받아 끝까지 실행하지만, 실제 프로그램이라면 여기서 멈춥니다.」
- **A-9 [하]**: 02-4 도식 읽기에 「칸 맨 위 파란 상자는 두 노드가 다시 묻는 방법입니다」.
- **`while True` 셀(4절)**: 기본 경로에 그대로 둠(챕터 리드 결정) — 셀 첫 줄 주석·소제목·b7 「권하지 않는 모양」 그대로, handoff 허용 문법 목록에 이 한 자리 예외를 적음(강사 확인 대상).
- 준비물 「2초 안에」 → 「걸린 시간은 재지 않았습니다.」
- **B-17·A-10 생성기**: `checks()` 셋째 줄 `== author_01.TOOLS` → `.startswith(author_01.TOOLS)` — 이제 `--src-only`·`--figures`로 돌아감.
- 게이트 G1~G7 0(검사 문장 396 → 421), 과정 금지어 새 걸림 0(meta 줄 슬러그의 「재개」·「프로그램」 속 「로그」는 거짓 양성).
