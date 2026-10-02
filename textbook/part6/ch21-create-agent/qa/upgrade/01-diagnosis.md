# 01절 진단과 개선 기록 — create_agent와 ReAct 루프 (experiment)

- 대상: `_src/01-create-agent와-ReAct-루프.html` · `labs/part6/ch21-create-agent/notebooks/01-create-agent와-ReAct-루프.ipynb` · 새 도구 파일 `notebooks/runner_tools.py` · 그림 `figures/01-1`~`01-5`.
- 생성기: `qa/upgrade/author_01.py`(노트북 + `_src`). 흔들림 확인: `qa/upgrade/01-probe.md`·`probe/probe01.py`·`probe/probe-{L,G,T}.jsonl`. 그림 설계표: `qa/upgrade/01-figures.md`. 검토 묶음: `qa/upgrade/review-pack/01-create-agent와-ReAct-루프.md`.
- 작업일 2026-09-25(UTC 01:5x~02:3x). 형식 **experiment 유지**(`chapter.json`), 슬러그 그대로(링크하는 완료 파일 0).

## 1. 게이트 전후

| | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전 (`gates-before.json`) | 6 | 72 | 4 | 4 | 0 | 0 | 7 | 28 | 3 | **46** |
| 첫 실행 전 (`gates-wip-01-01.json`, 노트북만 쓴 판) | 23 | 386 | 0 | 0 | 0 | 0 | 0 | 10 | 18 | — |
| 후 (`gates-wip-01.json`) | **23** | **392** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G6 10 = 괄호 뒤 마침표로 두 문장이 한 문장으로 세어진 9곳 + 영문 시작 1곳(「LangChain은」) → 괄호 설명을 문장 가운데로 옮기고 「라이브러리 LangChain은」으로 고친 뒤 실행. G7 18은 그림 파일이 아직 없던 때의 값.
- AST 따로(Ch 20 마감 `extra_check.py` 복사, `/tmp/ch21-01/extra_check.py`): 노트북 **0건**, 도구 파일 2건 = `estimate_cost`의 `.get` 둘(Ch 6 06 원본 예외, Ch 20과 같음). 금지어(`/tmp/ch21-01/ban_check.py` — Ch 20 목록 + 「지시」·「돌려줍니다」·「시스템 프롬프트」·「실행기」): 노트북·`_src`·캡션·`.mmd`에서 **1건 = 「캐시 입력」**(허용 말).
- 코드 줄(`count_code.py`) 39 → **124**(셀 6 → 23), 도구 파일 코드 줄 42. 준비 셀이 아닌 셀의 주석 뺀 코드 최대 8줄(설치 셀 포함 셀 최대 10줄), 함수 본문 최대 7줄(`agent_row`), 셀당 함수 하나, 첫 줄 주석 100%.

## 2. 수정 전 주요 문제 (준비 노트 §1·§2 01·§4·§9)

1. **모델 설정**: `create_agent("openai:gpt-5.4-mini", …)`에 이름 글자를 넘겨 `temperature`·`reasoning_effort`가 둘 다 없음(설치판 `factory.py` 995~996행 — 글자면 기본 설정 `init_chat_model(model)`). G4가 놓침.
2. **바깥 서비스 요청**: `draw_mermaid_png()`가 기본값으로 mermaid.ink에 그림을 요청(`langchain_core/runnables/graph.py` 639행, `graph_mermaid.py` 422~423행) → 오프라인·서비스 장애에서 셀이 멈추고 PNG 바이트 수(8,388)는 서비스 판에 따라 바뀔 수 있음. `display`·`Image` 셀과 PNG 서명 `assert`.
3. **소재 차이**: 규정 글이 Ch 20과 다름(「14일 동안 5권」·토요일 없음), 없는 주제는 딕셔너리 `KeyError`(Ch 20은 `raise ValueError`), 반환 힌트 `-> str`(Ch 19·20 규칙 밖), 한 줄 딕셔너리 찾기.
4. **모델 답에 건 `assert`**: `"14" in 답 글` · `ToolMessage`가 있는가(모델 선택) · 비용 < 1.
5. **Ch 20과의 대응 설명이 없음**: 되돌아가는 엣지가 점선 `tools -.-> model`인데 까닭 없음, `tools_condition`을 쓰지 않는 사실·노드 이름·상태 칸·요청 수 셈 조건(여럿 담기) 설명 없음(Ch 20 인계 1·2·7).
6. **금지어·말**: 「반환」 10·「지시」 3(시스템 메시지 뜻)·「추정」 3·「경로」 4·「지연」 1·「인터페이스」·「실행기」, b2 질문 「Ch20의 모델·도구·지시」(Ch 20은 시스템 메시지를 안 씀), 비용을 자체 식(튜플 한 줄 대입·식 안 숫자·캐시 입력 칸 없음)으로 「추정」.
7. **금지 문법**: 별표 풀기(`[Path.cwd(), *…parents]`)·`enumerate`·`getattr`·제너레이터 `any`·`sum`·내포식·한 글자 이름 `m`·`x`·튜플 한 줄 대입, 설치 셀 `pillow`(판 없음, import 0).
8. **틀 문장**: b3 「필요한 자료와 객체는 노트북에서 다시 선언하므로 …」, b6 = 확인할 점 = b8(같은 글 세 번), b7 「절당 1달러 미만」·「모델 문장과 지연」, b8 「02-구조화-출력-두-전략에서 이 결과를 다시 사용합니다」(02가 01 결과를 쓰지 않음), 복습 해설 한 줄, 결과 읽기 셀 0, 그림 1장(옛 `{{svg:01-흐름}}` — 「도구 선택」을 모델 상자 하나로 따로 그림).

## 3. 바꾼 것

- **모델 셀 과정 표준**(`nbkit.key_and_model_cells("openai:gpt-5.4-mini")`)으로 만든 **모델 객체**를 `create_agent(model, tools=[lookup_policy], system_prompt=system_text)`에 넘김(Ch 22 01~09 모양과 같음 — 모델 객체 + `tools=` 키워드). 4절 결과 읽기에 「이름 글자만 넘기면 기본 설정으로 모델을 새로 만든다」(소스).
- **`draw_mermaid_png` 뺌** → `get_graph().draw_mermaid()` 구조 문자열(Ch 13·20이 쓴 방법). b7에 바깥 서비스 요청 사실 한 줄(소스).
- **소재 = Ch 20 01 그대로**: `POLICY_DATA` 셀은 Ch 20 01 생성기의 같은 상수와 **문자열까지 같음**(생성기 `check_same_as_ch20()`가 실행마다 대조). `DEF_TOOL`은 **코드 줄이 같고 주석 한 줄만** 「(이 오류를 다루는 법은 02절에서 봅니다)」 → 「(이 오류를 그래프 안에서 다루는 법은 Ch 20 02절에서 보았습니다)」로 고침 — 이 챕터 02절은 구조화 출력이라 학생이 「02절」을 이 챕터 02절로 읽기 때문(노트북 3절 결과 읽기에 「셀 안 주석 한 줄만 이 챕터에 맞게 「Ch 20 02절」로 적었다」). `LOAN_ARGS`·`LOAN_IDS`·`LOAN_ANSWER`·`TWO_ARGS`도 Ch 20 01 셀과 문자열까지 같음(같은 대조). 질문 셋도 Ch 20 01과 같은 글.
- **Ch 20과 무엇이 같고 다른지를 출력으로**(챕터 리드 결정 4): 5절 구조 문자열(상자 넷·점선 셋) → 설계 객체 `agent.builder`로 `등록된 노드: ['model', 'tools']`·`고정 엣지로 적힌 수: 1`·`조건부 엣지를 적은 노드 수: 2`·`상태 칸: ['messages', 'jump_to', 'structured_response']`·`노드 tools의 종류: ToolNode` → `branches`로 조건 함수 이름·갈 곳(`tools | 조건 함수: tools_to_model | 갈 수 있는 곳: ['model']` · `model | 조건 함수: model_to_tools | 갈 수 있는 곳: ['tools', '__end__']`). 6절 결과 키 `['messages']`(흔적 칸 없음). 10절 Ch 20 표와 견주기 + 부품 대응 목록 여섯 줄. 본문 b4 대응 표(일곱 줄)·그림 01-2.
- **`tools_condition`을 쓰지 않는다는 사실**은 출력(조건 함수 이름)과 설치판 소스(`factory.py` 28행 — `ToolNode`만 가져옴)로 둘 다. 조건 함수가 하는 일(요청마다 `Send`, 끝으로 가는 두 경우)은 소스로만 확인했다고 밝힘.
- **여럿 담기(`parallel_tool_calls`) 조건**(Ch 20 인계 7): 설치판 `create_agent`는 그 값을 넣는 인자가 없고 미들웨어 없이 `bind_tools(도구, tool_choice=None, **{})`만 부름(`factory.py` 1431~1436·1474행, `middleware/types.py` 156행 `model_settings` 기본 `{}`) · langchain-openai 1.6.0은 값을 줄 때만 요청에 넣음(`chat_models/base.py` 2427~2428행, 같은 파일 3074행 설명 「defaults to True」). → **8절 값 바꿔 보기(운영·연체)에서 첫 응답에 요청 둘 → 모델 요청 2번**(Ch 20 01은 3번). 요청 수는 도구 메시지 수로 짐작하지 않고 **응답 수(`sum_usage`의 `requests`)로 셈**, 「모델 요청 수 = 도구 메시지 수 + 1」은 요청을 하나씩 받을 때만 맞는다고 적음. b6에 「시스템 메시지도 달라 한 가지만 바꾼 비교가 아니다」.
- **시스템 메시지**(챕터 리드 결정 5): 말은 Ch 16 「시스템 메시지(글)」(Ch 16 03 「모델이 따를 규칙을 담은 메시지」로 잇고 링크), 「Ch 20의 그래프는 시스템 메시지를 쓰지 않았다」 한 문장. 6절 새 셀로 `시스템 메시지 수: 0`(메시지 칸에 남지 않음, 코드로 셈) + 요청마다 앞에 붙인다는 것은 소스(`factory.py` 1451~1452행)로만. 시스템 메시지 글은 흔들림 확인 전에 정함(`01-probe.md` §0).
- **도구 파일 `runner_tools.py` 새로 만듦**(§5).
- **사용량·예상 비용**은 과정 표준 함수(Ch 19 05 `sum_usage` · Ch 6 06 `estimate_cost`)로 — 출력 토큰·비용은 결과 읽기 둘째 단락 「이번 실행에서는」. 걸린 시간은 재지 않음(챕터 리드 결정 1).
- **ReAct**는 제목 말로 두고 노트북 1절·b3·용어 표에서 Ch 7 05 말(「생각과 행동을 번갈아 하는 방식」, 관찰)로 풂. 새 용어 **3**(에이전트를 만드는 함수 · 에이전트 그래프 · ReAct 루프) — meta 「새 용어 5」 → 3.
- **`assert`는 호출 ID 짝 하나**(도구 실행 노드가 옮겨 적는 값). 모델 답·도구를 부를지·한 응답의 요청 수에 건 `assert` 0.
- 본문 10블록을 새 출력으로 다시 씀(비유 「세탁기」, 용어 표, 그림 넷 + 삽화, 대응 표, 결과 표, b7 열한 줄, 복습 넷·해설 셋 문장, 참고 자료 여덟 줄). 제작 이력 문장 0.

## 4. 흔들림 확인과 새 커널 두 번 (규격 §2-7 9·10번 끝)

- **노트북 밖 다섯 번**(`01-probe.md`, 규칙 §0을 첫 요청 전 02:01:04Z에 적음 → 요청 02:01:34~57Z): L 대출 5/5 · G 인사 5/5 · T 운영·연체 5/5 **모두 같음** — 결과 키 `['messages']` · 메시지 종류 · 도구 이름과 인자(`대출` / 없음 / `운영`·`연체`를 **한 응답에 둘**) · 결과 상태 `success` · 호출 ID 짝 `True` · 시스템 메시지 없음 · 입력 토큰(L 203·253 · G 199 · T 200·306) · 출력 토큰(L 18·26 · G 14 · T 49·78) · 답 글까지 15/15 같았음. 모델 `gpt-5.4-mini-2026-03-17`, 캐시 입력 0, 오류 0. → 입력을 그대로 씀.
- **새 커널 두 번**: A `run_section.sh`(02:19:51~58Z, 셀 실행 기록 약 7.5초) · B 사본 `/tmp/ch21-01/B.ipynb`를 `execute.py`로(02:20:2x Z). `code_sha256` `becd09fa7fbb…` 둘 다, **셀별 출력 글자 23/23 같음**, `outputs_sha256` 둘 다 `89e69f57f1cd…`. 교재 출력 = A. 그림은 A·B 대조 뒤 확정(`.mmd`는 노트북 밖 값으로 먼저 써 두고 A·B 출력과 대조 — 달라진 라벨 0).
- **흔들린 값(본문 결론·그림·정리·복습에 안 씀)**: 답 글(이번 두 번과 밖 다섯 번은 같았지만 모델 글이라 둘째 단락에만) · 출력 토큰 `'output_tokens': 44` · 예상 비용 `0.00054`. 입력 토큰 `456`은 결과 읽기 첫 단락에 둠(밖 다섯 번·새 커널 두 번 모두 같음).
- **탐색으로 고른 입력 없음**: 질문 셋은 Ch 20 01과 같은 글, 시스템 메시지 글은 첫 요청 전에 정함(b7 「흐름을 보여 주려고 정한 예」).

## 5. 도구 파일 `notebooks/runner_tools.py` (챕터 리드 결정 6)

| 함수(인자) | 배운 곳 | 이 절에서 |
|---|---|---|
| `tool_call_names(response)` | Ch 19 04 | `show_messages` 안에서만(노트북에서 직접 가져오지 않음) |
| `show_messages(messages)` | Ch 19 06 | 6·7·8절 |
| `sum_usage(messages)` — 키 `requests`·`input_tokens`·`output_tokens` | Ch 19 05 | 9절·10절 `agent_row` 안 |
| `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` | Ch 6 06(Ch 19 판) | 9절 |
| `call_id_lists(messages)` | Ch 20 01 | 6·8절·10절 `agent_row` 안 |

- 해시 **`eb408639084bd97ca4258ab67cdea7818c0b33d42cfe800130170856efe0ff08`**, 76줄(코드 줄 42), import 0, 함수마다 `# Ch NN MM절에서 배웠습니다 — Ch 20 도구 파일 graph_tools.py의 같은 이름 함수를 옮겼습니다`. 다섯 함수의 AST가 Ch 20 `graph_tools.py`(`34161a6f…`)와 같음(대조 스크립트 출력 5/5 `True`). 주석은 Ch 20 판 그대로(출처 문구만 「Ch 19 도구 파일 order_tools.py」→「Ch 20 도구 파일 graph_tools.py」, `call_id_lists`는 「01절 노트북 7절」→「Ch 20 도구 파일 graph_tools.py」).
- **옮기지 않은 것**: Ch 20 `run_row`(결과의 `trace` 칸을 읽음 — 에이전트 그래프 결과에 없음, 10절에서 까닭을 보이고 새 함수 `agent_row`를 노트북에 적음). `agent_row`는 이 절이 처음 가르친 함수라 노트북에 둠(뒤 절이 쓰면 그 절이 도구 파일로 옮김).
- 이름 `runner_tools.py`: 과정의 다른 도구 파일(`llm_tools`·`rag_tools`·`git_tools`·`guardrails`·`agent_tools`·`workflow_tools`·`order_tools`·`graph_tools`)과 겹치지 않고, `verify.py` 금지 첫 이름(`openai`·`rag`·`prompts` 등)과도 겹치지 않음. Ch 22 노트북 이름(`mask_pii`·`lookup_hours`·훅 이름)과 겹치는 함수 없음.
- 묶음 목록 두 곳에 한 줄씩(`textbook/part6/public-files.json` · 챕터 `qa/public-files.json`) — `manifest-changes.md`. 노트북 1절 결과 읽기에 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 …」.
- 실행 뒤 `labs/part6/ch21-create-agent/notebooks/__pycache__/`가 생겼을 수 있음(가져오기 부산물, 묶음 목록 밖 — 지우지 않음).

## 6. Ch 20 대응 요약 (보고용)

| 항목 | Ch 20 01(손으로 이음) | Ch 21 01(`create_agent`) | 근거 |
|---|---|---|---|
| 노드 이름 | `model`·`tools` | `model`·`tools`(같음), 도구 실행 노드 종류 `ToolNode` | 출력 |
| 고정 엣지 수 | 2(시작·되돌아가는 엣지) | 1(시작) | 출력 |
| 조건부 엣지를 적은 노드 | `model` 하나(`tools_condition`) | `model`(`model_to_tools`)·`tools`(`tools_to_model`) 둘 | 출력 · 동작은 소스 1923~1975·2004~2037행 |
| 되돌아가는 엣지 | 실선 `tools --> model` | 점선 `tools -.-> model`(갈 곳 `model` 하나) | 출력 |
| `tools_condition` | 씀 | 안 씀(`factory.py` 28행은 `ToolNode`만 가져옴) | 출력 + 소스 |
| 상태 칸 | `messages`·`trace` | `messages`·`jump_to`·`structured_response`, 결과 키 `['messages']` | 출력(`jump_to` 비공개는 소스) |
| 여럿 담기 | `parallel_tool_calls=False` | 인자 없음, 값 안 보냄 → 운영·연체 첫 응답에 요청 둘, 모델 요청 3 → 2 | 출력 + 소스 |
| 시스템 메시지 | 안 씀 | `system_prompt`, 메시지 칸에 없음(`0`), 요청 앞에 붙임은 소스만 | 출력 + 소스 |
| 단계 수·실행 한도 | 03절 | **세지 않음**(한 응답 요청 둘을 한 단계에서 함께 실행하는지 미확인) | — |

## 7. 그림

- Mermaid **4장**(`01-1` flowchart TB 645 · `01-2` flowchart TB + subgraph 둘 688 · `01-3` sequenceDiagram 851 · `01-4` flowchart TB + subgraph 셋 851, 모두 868 이하), **빨강 0**, 보라는 `01-3` 모델 노드 띠 하나. 설계표 `01-figures.md`, PNG 넷을 직접 열어 봄(`.cache/ch21-01-view/`). `01-4`는 902 → 851로 라벨을 미리 나눔(렌더 세 번).
- 삽화 **1장** `01-5-코스-버튼-하나인-세탁기`(비유 계열 **「세탁기(코스 버튼과 동그란 창)」** 개시) — **1차 job `5589dc15-3be6-4383-8d14-f1c6c44c7f27` 채택**, 재생성 0, **2크레딧**(거래 2026-09-25T02:22:03Z 「Nano Banana Pro −2」, 생성 전 잔액 2471.25, 바로 앞 거래는 다른 세션의 GPT Image). 응답 모델 이름 표시는 `nano_banana_2`(Ch 20과 같은 표시). 원본 `49c31ac5…`(2752 × 1536) → 저장 `29f497fe…`(1100 × 614), 픽셀 대조 bbox `None`·최대 차이 0. 그림 읽기는 저장 파일 사본을 직접 보고 씀(도구 셋·기계 한 대·버튼 하나·둥근 창 하나를 셈).
- 옛 그림 `figures/01-흐름.{svg,excalidraw,caption.md}`는 그대로(본문 참조 0).

## 8. 옛 생성기 (규격 §8, 챕터 리드 결정 9)

- `figures/_gen_figures.py`: 독스트링 뒤 설명 주석 세 줄 + `raise SystemExit("개선 전 그림 생성기입니다. …author_NN.py를 쓰세요.")`(`64c10c54…` → `77686b7d…`). 옮기기는 마감 몫.
- **공용 `textbook/part6/_author_ch21_ch29.py`**: 파일 전체를 막지 않고, 머리 주석 세 줄 + `write_chapter()` 첫머리 `if chapter == 21:` → 안내 한 줄 출력 후 `return`(Ch 21 쪽만 건너뜀, Ch 29 쪽 동작 그대로). 검증: `/tmp/ch21-01/gentest/{old,new}`에 두 챕터의 `chapter.json`과 빈 `_src`·`notebooks`를 두고 옛 판·새 판을 각각 실행 → **Ch 29 산출 `diff -r` 같음**, 새 판은 Ch 21 폴더에 아무것도 쓰지 않음(`chapter.json` 그대로). 해시 `1d3d1dc9…` → `650f6506…`. 옮기지 않음(Ch 29 몫 — Part 6 또는 Ch 29 마감).

## 9. 서비스 요청과 비용

- 노트북 한 번 **5번**(6절 2 · 7절 1 · 8절 2), 임베딩 0, 바깥 그림 서비스 0.
- 이 절 작업 전체 **35번** = 노트북 밖 흔들림 확인 25(L 10 · G 5 · T 10) + 새 커널 두 번 10. 구조 확인(`/tmp/ch21-01/graph_shape_check.py`)은 가짜 키 글자로 모델 객체만 만들고 `invoke`하지 않음(요청 0).
- 요금표(2026-09-17, 100만 토큰당 입력 0.75 · 캐시 입력 0.075 · 출력 4.50달러)로 어림한 예상 비용: 노트북 한 번 약 0.0017달러(대출 0.00054 · 인사 0.00021 · 운영·연체 0.00095), 작업 전체 약 0.012달러(청구 금액 아님).
- 참고 자료 확인: LangChain Agents `https://docs.langchain.com/oss/python/langchain/agents`(WebFetch 2026-09-25 — 「An agent is a model calling tools in a loop until a given task is complete.」, 모델 이름 글자 또는 모델 객체, 여럿 담기는 언급 없음).

## 10. 챕터 밖 수정

| 파일 | 무엇을 |
|---|---|
| `textbook/part6/_author_ch21_ch29.py` | §8 — Ch 21 쪽 건너뛰기(보호 파일) |
| `textbook/part6/public-files.json` | 도구 파일 한 줄(보호 파일) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | `verify.py`가 다시 씀 |

- 챕터 안(실습 폴더 포함): `labs/…/notebooks/01-*.ipynb`(새 판, `f5e6c60b…`) · `runner_tools.py`(새 파일) · `_src/01-*.html`(`c33000ea…`) · 빌드 HTML `01-*.html`(`00ce823f…`, `{{` 0건)·`index.html` · `figures/_gen_figures.py`·`01-1`~`01-5` 새 파일 · 챕터 `qa/public-files.json` · `qa/upgrade/` 새 파일(`author_01.py`·`01-probe.md`·`probe/`·`01-figures.md`·`01-diagnosis.md`·`handoff.md`·`manifest-changes.md`·`gates-wip-01*.json`·`review-pack/`) · `집필점검표.md`·`qa/verification.md` 01 행.
- **고치지 않은 것**: `chapter.json`(절 제목 「create agent와 ReAct 루프」·`objectives`는 마감 몫) · 실습 폴더 `pyproject.toml`·`uv.lock`·README(마감 몫) · Ch 22·Ch 29·Ch 20 파일 · 공용 도구·게이트·`verify.py` · 옛 그림.
- **파일 삭제 0건.**

## 11. 강사 확인 대상

1. 제목 말 「create_agent」·「ReAct」(제목에만, 본문 첫 자리에서 풂). `chapter.json` 절 제목은 옛 생성기가 밑줄을 뺀 「create agent와 ReAct 루프」 그대로(마감 때 표기 맞춤).
2. 코드 줄 39 → 124(셀 6 → 23) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘. 늘어난 몫은 Ch 20 대응을 출력으로 보이는 5절 셀 셋(구조 문자열·설계 객체·조건 함수)과 결과 읽기 셀 분리.
3. 새 API 모양: 컴파일한 그래프의 속성 `builder`와 설계 객체의 `channels`·`nodes["tools"].runnable`·`branches[…][…].ends`(공식 문서에 없는 속성 — Ch 20 03 `builder.branches` 선례). 쓰지 않으면 조건 함수 이름·도구 실행 노드 종류를 출력으로 보일 수 없음.
4. `DEF_TOOL` 주석 한 줄을 「Ch 20 02절」로 고친 것(코드 줄은 Ch 20과 같음 — 챕터 리드 결정 3 「글자까지 같게」와 어긋나는 한 줄).
5. 시스템 메시지 글을 넣어 Ch 20과 두 가지(여럿 담기·시스템 메시지)가 함께 다른 비교가 됨 — b6·b7에 밝힘. 한 가지만 바꾼 비교로 하려면 시스템 메시지 없는 에이전트를 더해 요청 +5.
6. 도구 파일 이름 `runner_tools.py`(챕터 리드 예시 그대로).
7. 새 용어 수 5 → 3.

## 12. 남은 것 · 지워야 하지만 지우지 않은 것

- 마감 몫: `figures/_gen_figures.py` `mv -n` → `qa/upgrade/before/generators/blocked/` · 옛 그림 `01-흐름.*` 삭제 승인 · `chapter.json` 절 제목·`objectives` · 실습 폴더 README(도구 파일 단락·요청 수) · `pyproject.toml`의 `pillow>=11.0`(노트북 import 0 — 01은 `%pip`에서 뺌)·`numpy>=2.0` 범위 표기 · `labs/part6/continuity-guide.md` 문장 확인 · `part6-practice.zip` 재생성(도구 파일 포함).
- 삭제 승인 대상(만들었지만 지우지 않음): 기기 `/tmp/ch21-01/`(probe 원본·A/B 사본·`gentest/`·원본 삽화 4MB·확인 스크립트) · `.cache/ch21-01-view/`(그림 확인 사본) · `qa/upgrade/gates-wip-01-01.json`(첫 실행 전 판) · `labs/…/notebooks/__pycache__/`·`qa/upgrade/__pycache__/`(있으면).

## 마감 반영 (2026-09-25, 챕터 마감 담당)

검토 1차(`review-round1-A.md`·`review-round1-B.md`) 반영과 챕터 마감에서 이 절에 한 일입니다. 전체 기록은 `chapter-summary.md`, 절 사이 기록은 `handoff.md` 「검토 반영과 챕터 마감 (2026-09-25)」입니다.

- **A-12 NumPy(다시 실행)**: 도구 파일 `runner_tools.py`가 맨 위에서 `import numpy as np`를 하므로 설치 셀에 `"numpy==2.5.3"`(잠금 판)을 더함 — `author_01.py` `INSTALL` · 준비물 「패키지 여섯」·판 줄 · 1절 「뒤에서 가져오는 도구 파일이 NumPy를 쓰므로, numpy도 함께 설치합니다」 · 결과 읽기 첫 단락 `numpy: 2.5.3`. `run_section.sh … 01`로 새 커널 한 번(셀 실행 기록 06:41:15~23Z, 약 8.2초 — 준비물 「10초 안에」 그대로), **모델 요청 5번**, 요금표 어림 약 0.002달러(청구 아님).
- **앞 교재 출력과 셀별 대조**(앞 출력을 둘째 실행으로 삼음): **23셀 가운데 22셀 글자까지 같음**, 다른 셀은 설치 셀 [3](`numpy: 2.5.3` 한 줄 더)뿐 — 답 글·출력 토큰 `44`·예상 비용 `0.00054`·인사 답 글까지 같아 결과 읽기·결론·그림·정리·복습 고침 0. `code_sha256` `becd09fa…` → **`80151070e4d72a1f52aeb2182e09094ce28f01eef5e0928ea545678d5659e306`**, `outputs_sha256` `89e69f57…` → **`f7670f571346a354e99b4ce63d203a0979ca9908bdf130c7b2d645b77b396093`**.
- **A-1**: 준비 셀 결과 읽기 [6] 「이 챕터 노트북이 쓰는 함수만 …」 → 「이 절이 쓰는 함수는 … 옮긴 것」 + 「같은 파일에는 뒤 절이 쓰는 함수도 함께」 + 「파일 맨 위에서 NumPy를 가져오므로 … `numpy`도 설치」(단락을 둘로 나눔, 다섯 문장 넘지 않게) · b7 「도구 파일의 함수 다섯은 …」 → 「이 절이 가져오는 함수 넷과 그 안에서 쓰는 `tool_call_names`는 … 같은 도구 파일에는 뒤 절이 쓰는 함수도 들어 있습니다」.
- **A-13 색(챕터 리드 결정 — 라이브러리가 준 `create_agent`는 회색)**: `01-1` `mk["create_agent 한 줄"]`의 `:::flow`를 빼 회색(07-1과 같음) → `--force`와 같은 효과로 다시 렌더(`run_section.sh`가 바뀐 도장을 보고 렌더), 노트북 첨부 PNG 새 판. alt 「회색 상자 create_agent 한 줄」 · 도식 읽기 「초록 상자는 우리가 넘긴 값 셋이고, 그 아래 회색 상자는 라이브러리가 준 함수 create_agent를 부르는 줄입니다」. PNG를 직접 열어 확인(`.cache/ch21-close/view/close-01-1.png`).
- **A-2 제목**: `chapter.json` 절 제목 「create agent와 ReAct 루프」 → **「create_agent와 ReAct 루프」**(슬러그 그대로) — 빌드 `<title>`·챕터 목차·이웃 절 링크·Part 6 목차에 반영. 위 §11-1의 「마감 때 표기 맞춤」은 끝남(제목 말 자체는 강사 확인 대상으로 남음).
- 위 §12 「마감 몫」 결과: `_gen_figures.py`는 `qa/upgrade/before/generators/blocked/`로 옮김 · `objectives`·README·`part6-practice.zip` 새 판 · `pyproject.toml`의 `pillow>=11.0`은 **그대로**(보호 파일·잠금을 다시 만들어야 함 — 요약 §16) · 옛 그림 `01-흐름.*` 삭제 승인은 `textbook/qa/upgrade-final-checklist.md` §2-10.
- 게이트 G1~G7 0(검사 문장 396), 금지어 마감 전후 같음, 생성기 `cells()`·`src_html()` = 노트북·`_src`(글자까지).
