# 01절 진단과 개선 기록 — ToolNode와 tools_condition (experiment)

- 작업일 2026-09-24 · 생성기 `qa/upgrade/author_01.py` · 흔들림 확인 `qa/upgrade/01-probe.md`(+ `probe/probe01.py`·`probe/probe-{L,G,T}.jsonl`) · 그림 설계표 `qa/upgrade/01-figures.md` · 검토 묶음 `qa/upgrade/review-pack/01-ToolNode와-tools-condition.md`.
- 원본 사본은 준비 담당이 `qa/upgrade/before/`에 둔 것 그대로입니다(`_src`·노트북·그림·생성기).

## 1. 게이트 전후

| 시점 | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 수정 전(`gates-before.json`) | 8 | 97 | 7 | 5 | 0 | 2 | 7 | 28 | 3 | 52 |
| 첫 실행 전(`gates-wip-01-01.json` 첫 판) | 28 | — | 0 | 0 | 0 | 0 | 0 | 6 | 17 | — |
| **끝(`gates-wip-01.json`·`gates-wip-01-01.json`)** | **28** | **392** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G6 6건(b10 참고 자료 한 문장 70자 넘음 · 노트북 마크다운 표 한 덩어리가 한 문장으로 셈 · 영문으로 시작한 문장 둘 · 도식 읽기 단락 6문장)은 실행 전에 고쳤습니다. 마크다운 표는 목록 다섯 줄로 바꿨습니다(`_src`에는 HTML 표로 둠). G7 17건은 그림을 만들기 전이라 난 것입니다.
- G7 마지막 1건: `01-2` sequenceDiagram의 `box rgba(208, 191, 255, 0.45)` 숫자를 G7이 라벨 숫자로 읽음 → 이름 있는 색 `box Lavender`로 바꿔 0.
- 게이트 밖 AST 검사(`/tmp/ch20-01/extra_check.py` — Ch 19 06 판을 복사해 필드만 적은 `TypedDict` 클래스를 허용하고 `'__end__'` 글자·`elif`를 더 셈): 노트북 28셀 **0건**, 도구 파일 `graph_tools.py` **0건**. 금지어 검사(`/tmp/ch20-01/ban_check.py` — 「분기·경로·반환·검증·전파·필드·측정·지연·추정·프롬프트·레코드·병렬·사전·캐시·trace·택배·송장·스키마·MessagesState·super-step·한 겹 더·돌려」 등, 코드 백틱 밖): 노트북 마크다운·코드 주석·`_src`·캡션 다섯·`.mmd` 넷 **0건**(옛 그림 캡션 `01-흐름.caption.md`의 「분기」 1건은 이 절이 쓰지 않는 옛 파일).
- `verify.py --chapter`: `PASS 4 sections / 52 code cells (max 23 lines)`(23줄은 아직 고치지 않은 02~04절, 01절은 준비 셀이 아닌 셀 주석 뺀 코드 최대 9줄 · 준비 셀 최대 11줄 · 함수 본문 최대 8줄 `call_id_lists`). 빌드 HTML `01-ToolNode와-tools-condition.html` `{{` **0건**.
- 코드 줄(`count_code.py`, 주석·빈 줄 제외): 01 **88 → 153줄**(코드 셀 8 → 28) + 도구 파일 `graph_tools.py` 14줄. 옛 판은 셀 하나에 함수 둘·19줄 셀·내포식이 몰려 줄 수가 적었습니다(규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘 강사 확인 대상).

## 2. 수정 전 주요 문제 (준비 노트 §1·§2 01·§4-3·§7)

1. **핵심 관찰 셋이 모델 답에 건 `assert`**: `any ToolMessage`·`trace == ['model', 'model']`·인사 흐름 ToolMessage 없음 + 잰 비용 `< 1`. 모델이 다르게 답하면 셀이 멈춤(규격 §3).
2. **틀린 사실**: b3 「Ch13에서 StateGraph, **MessagesState**와 add_messages 리듀서」(Ch 13은 `MessagesState`를 가르치지 않음) · b4 비유 「도서관 상담 직원」 ↔ 도구 설명 「교육센터 자료실」 장소 어긋남.
3. **실행 흔적 칸이 Ch 13 01절 판 모양**: `trace: list[str]`(규칙 없음) + 노드가 `state['trace'] + ['model']`로 이어 붙임 — Ch 13 02가 하지 말라고 한 모양.
4. **Ch 19 05와의 대응 없음**: b2가 「`tool_calls`를 해석해 도구 함수를 호출」까지만. 바퀴 한도 `turn_limit`와 그래프 되풀이의 차이, 되돌아가는 엣지(과정 처음)의 풀이 없음.
5. **금지·미교육 문법**: 별표 풀기 `[Path.cwd(), *…parents]` · f-string 둘(`f'openai:{MODEL_NAME}'`·오류 글) · 타입힌트 전부(`-> BaseChatModel`·`state: AgentState` 등) · 한 셀에 함수 둘(`usage_of`+`make_model`) · 클래스+모델+노드 한 셀 · `enumerate`·`getattr`·`sum(생성기)`·`any`·딕셔너리 내포식 셋·`{**total, …}` · 한 글자 `m` · `from typing import Any`(안 씀) · `BaseChatModel` import(G4 착시).
6. **모델 설정**: `temperature=0` 없음(G4 진짜 결함) · 비용 셈이 캐시 입력 칸 없는 이 챕터만의 `usage_of`(인사 요청 비용은 안 셈) · 「추정 비용」·「지연」(Ch 18 금지어)과 잰 걸린 초 `1.963`을 결론에 씀(주제 아님).
7. **첫 줄 주석이 틀 문장**(「…에 필요한 연산을 실행합니다」 8셀 전부) · 결과 읽기 셀 0 · 금지어 「분기·병렬·필드·반환·추정·지연·측정·캐시·경로·trace」 · 영문으로 시작하는 문장 다수 · Mermaid 0 · 삽화 0.

## 3. 바꾼 것

- **상태 형식**: Ch 13 04절 모양 `AgentState(TypedDict)` — 메시지 칸 `Annotated[list[AnyMessage], add_messages]` + 흔적 칸 `Annotated[list[str], operator.add]`(Ch 13 02). 노드는 자기 몫 `{"messages": [응답], "trace": ["model"]}`만. 게이트 G1은 필드만 적은 `TypedDict`를 허용(Ch 13 선례, `upgrade_allow` 없음). `MessagesState` 0건.
- **조건 함수와 이름표 표**: 라이브러리 `tools_condition` + `path_map = {"tools": "tools", END: END}`(Ch 13 03 모양, `'__end__'` 글자 대신 상수). 그래프 없이 `tools_condition`을 **손으로 만든 `AIMessage` 둘**(요청 없음 / Ch 19 04 칸 넷을 담은 요청 하나)에 직접 불러 `__end__`·`tools`·`END와 같은가: True`를 출력 — Ch 13 03 「조건 함수만 직접 불러」 모양, 모델 없이 결정적.
- **되돌아가는 엣지**를 과정 처음으로 풀고(노트북 6절·b4 용어 표), 구조 문자열의 `tools --> model`로 확인.
- **도구 실행 노드**: `ToolNode(tools)`를 따로 만들어 속성 `tools_by_name`의 키 `['lookup_policy']`를 출력 — Ch 19 05 도구 찾기 표와 이음. 그래프 밖에서 바로 부르면 설치판에서 설정 오류가 나 노트북에서는 부르지 않았습니다(노트북 밖 `/tmp/ch20-01/offline01.py`로만 확인, 본문에 쓰지 않음).
- **모델 셀**: `nbkit.key_and_model_cells("openai:gpt-5.4-mini")`(`temperature=0`·`reasoning_effort="none"`). `bind_tools(tools, parallel_tool_calls=False)`(Ch 19 06과 같은 값 — 한 응답의 요청 여럿을 `ToolNode`가 한꺼번에 실행하는 장면을 01에서 피함, b7에 소스로만 적음).
- **걸린 시간·토큰·비용 재기 뺌**(챕터 리드 결정 5). 모델 요청 수 = 실행 흔적 칸의 길이. 준비물의 「10초 안에」는 셀 실행 기록(첫 셀 입력 06:15:36.05 → 마지막 셀 응답 06:15:43.65 UTC).
- **`assert`**: 호출 ID 짝(도구 실행 노드가 옮겨 적는 값) 하나만. 모델이 정하는 값(도구를 부를지·인자·흔적 길이·답 글)에는 0.
- **도구 파일 B안**: 새 `labs/part5/ch20-tool-node/notebooks/graph_tools.py`(§5).
- **소재**: 자료실 규정 `POLICIES` 셋(옛 판 글 그대로) + `@tool lookup_policy(topic: str)`(독스트링 「교육센터 자료실 규정 하나를 주제어로 찾습니다. topic에는 대출, 운영, 연체 가운데 하나를 넣습니다.」, 없는 주제면 `raise ValueError("지원하지 않는 주제: " + topic)` — 02가 쓸 자리, 01에서는 실행되지 않음). 반환 힌트 뺌.
- **질문 셋**: 대출(옛 판) · 인사(옛 판) · 값 바꿔 보기 「자료실 운영 시간과 연체 규정을 함께 알려 주세요.」(이 절이 정함 — 규정 둘이 필요해 되돌아가는 엣지를 두 번 지나는 장면).
- **본문**: 10블록 다시 씀. b2에 Ch 19 05 `ask_until_answer`·Ch 13(앞에서 뒤로만)·Ch 18(코드가 고름)·Ch 21 `create_agent`(Ch 21 01 b2 문장 확인). b3에 Ch 13 01~04·Ch 17 03(루프·바퀴·정지 조건 「모델의 끝 선택」)·Ch 19 01·04·05·06. b4 비유 「자료실 승강 상자」·용어 표 넷·대응 표(`ask_until_answer` 줄 ↔ 그래프). b8 다음 절에 Ch 19 06 `handle_tool_error`(도구 속성)를 잇는 문장. b10 확인일 2026-09-24.
- **새 용어 넷**(meta 「새 용어 5」 → **4**): 모델 노드 · 도구 실행 노드(ToolNode) · 도구 조건 함수(tools_condition) · 되돌아가는 엣지. 절 meta 시수 강의 1h · 실습 1.5h 그대로.

## 4. 흔들림 확인과 새 커널 두 번 (규격 §2-7 9·10번 끝)

- 노트북 밖 다섯 번(`01-probe.md`, 06:02:38~06:03:16 UTC, **30요청**): L 대출 · G 인사 · T 운영+연체 모두 **실행 흔적·메시지 종류·도구 이름과 인자·도구 메시지 내용과 결과 상태·호출 ID 짝·입력 토큰이 5/5 같음**. 흔들린 것은 답 글(문장부호·굵은 글씨 자리)과 마지막 응답의 출력 토큰(L 25/28 · T 62/77/78)뿐. 입력은 판단 규칙(§0, 첫 요청 전 기록)대로 그대로 씀, 후보 바꾸기 없음.
- **새 커널 A**(`run_section.sh`, 06:15:36~43 UTC, `code_sha256` `836cc6492589…` · `outputs_sha256` `8b2c88251b19…`)와 **B**(사본 `/tmp/ch20-01/B.ipynb`, 06:16:07~15 UTC, 같은 두 해시): 코드 셀 28개의 셀별 출력 글자 해시 **28/28 같음**(답 글까지 같음). 교재 출력 = A. 그림은 A·B 대조 뒤 그렸습니다.
- 결론·그림·정리에 쓴 값(A·B·밖 다섯 번 모두 같음): 흔적 `['model', 'model']`·`['model']`·`['model', 'model', 'model']` · 모델 요청 2·1·3 · 도구 메시지 1·0·2 · 인자 `{'topic': '대출'}` / `{'topic': '운영'}` → `{'topic': '연체'}` · 결과 상태 `success` · 호출 ID 짝 `True` · 구조 문자열 · `tools_condition` 이름표.
- 둘째 단락·「확인할 점」에만 둔 값: 답 글(대출 답 글의 `5권`·`14일`, 인사 답 글 `안녕하세요, 반갑습니다!`). 토큰은 노트북에서 세지 않음.
- 마크다운만 고친 뒤(`mdpatch.py` 두 번 — 결과 읽기 둘째 단락 셋과 「10초 안에」, 9절 「바퀴가 세 번」) 노트북 `code_sha256`·`outputs_sha256`·`executed_at` 그대로(다시 실행하지 않음).

## 5. 도구 파일 `notebooks/graph_tools.py` (챕터 리드 결정 1 B안)

- 함수 둘: `tool_call_names(response)`(Ch 19 04) · `show_messages(messages)`(Ch 19 06, 안에서 `tool_call_names`를 부름). Ch 19 `order_tools.py`(`fa5975b5…`)의 두 함수 소스 조각과 **AST 소스 문자열이 같음**(`ast.get_source_segment` 대조), 설명 주석 두세 줄도 같은 글 + 「# Ch 19 0N절에서 배웠습니다 — Ch 19 도구 파일 order_tools.py의 같은 이름 함수를 옮겼습니다」. import 0(`pandas` 없음 — 잠금 그대로), 전역 이름 기대기 0, 타입힌트·독스트링(함수) 0, 모듈 독스트링만.
- 해시 **`dd2dd4f8cfb91c1f0a7acf0ee59a41f21b802e71623f78e02b0b441210ed2150`**(코드 줄 14).
- `sum_usage`·`estimate_cost`는 01이 쓰지 않아 넣지 않았습니다(처음 쓰는 절이 더함 — handoff). 노드 함수 `call_model`·도움 함수 `call_id_lists`·`run_row`는 노트북에(`call_id_lists`는 이 절에서 처음 가르친 함수 — 02 이후 쓰면 도구 파일로 옮김).
- 묶음 목록: 챕터 `qa/public-files.json` `include`에 `notebooks/graph_tools.py`(`c43b2a80…` → `5f637756…`), Part 5 목록 `textbook/part5/public-files.json`에 `labs/part5/ch20-tool-node/notebooks/graph_tools.py`(보호 파일 — `manifest-changes.md`). 묶음 zip은 다시 만들지 않음(마감 몫).
- 가져오기 셀 결과 읽기에 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다」 + Ch 19 `order_tools.py`와 다른 파일이라는 문장. 교재 출력은 `run_section.sh`가 `PYTHONPATH`에 `notebooks/`를 더한 실행(01은 자리 찾기 셀이 없어 출력에는 드러나지 않음).
- `labs/part5/continuity-guide.md` 9행 「예제 데이터는 각 절에서 다시 준비」는 도구 파일이 생겨 어긋남 — Part 5 마감 몫(고치지 않음).

## 6. 그림

- Mermaid 4장: `01-1`(구조, 폭 554) · `01-2`(대출 차례 sequenceDiagram, 805) · `01-3`(세 질문, 859) · `01-4`(for 루프 ↔ 그래프, 651). 모두 868 이하, 빨강 0, 보라는 `01-2`의 모델 노드 띠(`Lavender`) 하나, 조건 함수는 상자 없이 점선 갈래 라벨로만. PNG 네 장을 직접 열어 확인.
- 삽화 `01-5-쪽지가-든-승강-상자`: `nano_banana_pro`(응답 모델 이름 `nano_banana_2`) 16:9 2k, **1차 job `096ba353-4ab4-42cb-8745-cbb044dad5af` 채택**(재생성 0). 거래 기록 **06:18:31Z 「Nano Banana Pro −2」** 한 줄이 이 절 몫(생성 전 잔액 2547.25). 원본 `fa50b4ea…`(2752 × 1536, 기기 `/tmp/ch20-01/illu-1-orig.png`), 저장 `figures/01-5-쪽지가-든-승강-상자.png` 1100 × 614 `5490ab2d…`, 원본을 같은 폭으로 줄인 그림과 픽셀 차이 0.
- 옛 그림 `figures/01-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 토큰만 바꿈).

## 7. 옛 생성기 막기 (규격 §8)

- `qa/author_ch20.py`(`336c0309…` → `59800f42…`)와 `figures/_gen_figures.py`(`4bd06a70…` → `d5b3347f…`) 맨 위에 설명 주석 세 줄 + `raise SystemExit("개선 전 생성기입니다. textbook/part5/ch20-tool-node/qa/upgrade/author_NN.py를 쓰세요.")`. 두 파일을 실행해 종료 코드 1과 안내 글만 나오는 것을 확인. 원본 사본은 `before/generators/`. 옮기기(`mv -n` → `before/generators/blocked/`)는 챕터 마감 몫.

## 8. 서비스 요청과 비용

- 노트북 밖 30 + 새 커널 A 6 + B 6 = **42요청**(모두 `gpt-5.4-mini`, 임베딩 0). 요금표(2026-09-17)로 어림한 예상 비용: 밖 0.0081 + 노트북 한 번 약 0.0016 × 2 ≈ **0.011달러**(청구 금액 아님, 노트북 실행은 토큰을 세지 않아 밖 확인의 같은 입력 토큰으로 어림).
- 노트북 한 번 요청 6(7절 2 · 8절 1 · 9절 3).

## 9. 챕터 밖 수정

- `textbook/part5/public-files.json` 한 줄 더함(§5, 보호 파일). 그 밖의 챕터 밖 파일은 고치지 않았습니다. `verify.py`가 `textbook/_notebook/checks/notebook-contracts-part5-ch20-tool-node.json`을 다시 씀(도구 동작).

## 10. 강사 확인 대상

1. 제목 「ToolNode와 tools_condition」의 영어 두 이름(본문 첫 자리 「도구 실행 노드(`ToolNode`)」·「도구 조건 함수(`tools_condition`)」로 풂).
2. 손으로 만든 `AIMessage(content="", tool_calls=[…])`(Ch 13 04 직접 만들기 + Ch 19 04 칸 넷) — 과정에서 처음 합친 모양. 가짜 모델이 아니라 조건 함수에 넣어 보는 값이라고 노트북에 밝힘.
3. 새 용어 5 → 4(meta).
4. 코드 줄 88 → 153(+ 도구 파일 14).
5. 삽화 판독: 오른쪽 통로가 아래층 바닥 밑으로 조금 더 그려짐(관계 판독에는 영향 없다고 봄).
6. `parallel_tool_calls=False`로 둔 설계(한 응답 요청 여럿의 `ToolNode` 한꺼번에 실행은 소스로만).

## 11. 남은 것

- 한국어 감사 3단·그림 판독은 별도 세션 검토. `visual.cjs`(1280·390px)는 이번에 돌리지 않았습니다(챕터 마감 몫).
- 지워야 하지만 지우지 않은 것(삭제 승인 대상): 기기 `/tmp/ch20-01/`(A·B 노트북 사본, 삽화 원본·축소본, 확인 스크립트, probe 기록 원본) · `.cache/ch20-01-view/illu-1-1100.png` · `qa/upgrade/gates-wip-01-01.json`·`gates-wip-01.json`(첫 판은 덮어씀) · `qa/upgrade/__pycache__/`(`author_01.py`를 불러 읽을 때 생김) · `qa/upgrade/probe/`의 `.jsonl` 셋(기록으로 둠).

## 마감 반영 (2026-09-24, 검토 1차 A — 노트북 다시 실행하지 않음)

- **A-1 [중]**: b6 결과 해석에서 「모델 요청 수 = 도구 메시지 수 + 1」의 까닭에 「여럿 담기를 꺼서 요청이 있는 응답마다 도구 메시지가 하나」를 더하고 단락을 둘로 나눔. b7 여럿 담기 항목 끝에 「요청 여럿이 한 응답에 오면 이 셈은 달라질 수 있다」. 노트북 [60]도 같은 뜻으로(단락 셋으로 나눔).
- **A-2**: b7 「이 절이 도구 파일에서 가져오는 두 함수」로 좁힘 · 노트북 [6]에 「이 절에서 만드는 `call_id_lists`·`run_row`도 뒤 절이 쓰도록 본문을 글자 그대로 이 파일에 옮겨 두었다」 한 문장.
- **A-3**: 노트북 [60]과 01-3 「도식 읽기」에 「인사 질문의 짝 `True`는 두 목록이 모두 비어 나온 값」(그림은 그대로).
- **A-4**: 01-4 「도식 읽기」 → 「그래프가 되풀이하는 횟수의 한도는 바퀴 한도 `turn_limit`과 세는 것이 달라, 아래 칸에 그리지 않고 03절에서 봅니다」.
- **A-5**: b4 「다른 상황에 적용」 → 「도구 목록을 바꿔 모델에게 다시 알리고 도구 실행 노드를 새로 만들면 되고, 그래프 모양은 그대로」.
- **A-6**: b4 비유의 「규정 카드」 셋 → 「규정 책」(삽화·그림 읽기의 파란 책과 맞춤, 02의 빈 카드와 대조). handoff 비유 계열 줄도 하나로.
- 방법: `.cache/ch20-close/cpatch.py`(생성기·노트북 마크다운·`_src`에 같이 적용, 코드 셀에 옛 글이 있으면 멈춤 — 0회) → `run_section.sh … 01 --no-exec`. `.mmd` 다시 렌더 0장. 노트북 `code_sha256` `836cc6492589…`·`outputs_sha256` `8b2c88251b19…`·`executed_at` 그대로, 파일 `0f8480299d05…` → `f65156b67d9c…`. `_src` `e3b0f102e5a8…` → `475dbfc6571d…`, 생성기 `575c56b60dc4…` → `2cd1844ac302…`(생성기 `src_html()`·`cells()`가 `_src`·노트북과 글자까지 같음). 게이트 G1~G7 0(검사 문장 399).
