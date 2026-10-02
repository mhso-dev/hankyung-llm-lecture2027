# Ch 26 위임 구조 — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part6/ch26-delegation`(절 넷 — 01·02·03·04 모두 experiment) · `labs/part6/ch26-delegation`. 바로 앞 Ch 25(완료, 모델 결정 M2)를 잇는 Part 6 여섯째 챕터입니다.
- 준비 산출물: `qa/upgrade/before/`(원본 사본 38개, 464KB — 원본과 `cmp` 모두 같음) · `gates-before.json`(`6113c82e…`) · `before-manifest.json`(190개, `ea09b677…`) · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch26-delegation`.
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(전부) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 과정 요약(전부) · 계약 파일(§3 Ch 16~25 줄 · §4 Ch 15~25 줄 · §5 · §8) · Ch 25 `chapter-summary.md`(전부)·`chapter-lead-notes.md`·`before-manifest.json` · Ch 21 `chapter-lead-notes.md`(목차)·`chapter-summary.md`(§1·§6~8) · Ch 20·23 요약의 Ch 26 줄 · Ch 8 요약·03 `_src` · Ch 13 05·06 · Ch 18 요약(§1·용어) · Ch 22 04·08 `_src` · Ch 25 04 b8·`author_04.py` · Ch 27·34의 위임·라우터 문장 · 공용 옛 생성기 · Part 6 목록·묶음·검사 스크립트 · 챕터 `qa/` 기록 일곱. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다. `upgrade-final-checklist.md`는 `grep -n 'Ch *26'` 네 줄만 봤습니다.
- **원고·노트북·그림은 하나도 고치지 않았습니다.** 연결 폴더 안 파일 삭제 0건, 노트북 실행 0건, 서비스 모델·임베딩 요청 0건, `uv cache prune` 안 함. 확인은 기기 `/tmp/ch26-prep/exp/`의 작은 그래프(`e1_send.py`~`e6_imports.py`, `env -u OPENAI_API_KEY` — `e4`만 모델 객체를 만들려고 가짜 키 글을 넣음, 요청 0)와 설치판 소스·공식 문서로 했습니다. 가짜 모델은 쓰지 않았습니다.
- `chapter.json` `hours` = 「총 8h · 강의 4h · 실습 4h」. 절 meta 합 강의 1×4 = **4h**, 실습 1×4 = **4h** → 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part6/_build_index.py` 24행 (4, 4)·`qa/check_scope.py` `EXPECTED` (4,4)·`SECTION_COUNTS` 4도 같습니다. 새 용어 meta 5×4 = **20**(옛 생성기 `page()`가 모든 절에 「5」로 찍은 틀 값 — 실제 새 말 목록 없음).

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-28)

| 절 | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 Subagent 도구 위임 | 4 | 87 | 1 | 1 | 0 | 1 | 5 | 17 | 3 | 28 |
| 02 Handoff 상태 전환 | 6 | 77 | 2 | 0 | 0 | 0 | 5 | 21 | 3 | 31 |
| 03 Router 분류와 병렬 실행 | 4 | 82 | 1 | 1 | 0 | 1 | 6 | 19 | 3 | 31 |
| 04 호출 수·비용·종료 조건 비교 | 9 | 83 | 4 | 2 | 0 | 1 | 8 | 20 | 3 | 38 |
| **합계** | **23** | **329** | **8** | **4** | **0** | **3** | **24** | **77** | **12** | **128** |

- 통과 절 **0/4**. 코드 줄(`count_code.py labs/part6/ch26-delegation/notebooks`) 42·37·37·109 = **225줄**.
- G1 8 = 리스트 내포식 2(01 c6 `[call["name"] for message in … for call in getattr(…)]`(**이중 `for`**) · 04 c8 같은 모양) · 셀당 함수 둘 3(02 c6 `dispatch`·`respond` · 04 c6 `record_usage`·`measured_call` · 04 c10 `shipping_node`·`refund_node`·`route_active` **셋**) · 조건 표현식 1(02 c12 `"END" if completed else "refund_agent"`) · 제너레이터 식 2(03 c8 `"\n".join(f"[{name}] {value}" for …)` · 04 c16 `all(item["cost_usd"] < 1 for …)`).
- G2 4 = 15줄 넘는 셀 3(01 c4 17줄 · 04 c10 16줄 · 04 c14 19줄 — 주석·빈 줄 뺌) · 호출 두 겹 1(03 c6 `dict(zip(…, pool.map(…)))`).
- G3 0 — 셀마다 첫 줄 주석 한 줄뿐, 이유 주석 0.
- **G4 3 = 01 c4·03 c4·04 c4 `init_chat_model(f"openai:{MODEL}", reasoning_effort="none")`에 `temperature` 없음.** 가짜 모델 0. 02는 모델 셀이 없어 0.
- G5 24 = 절마다 제목 셀 없음·핵심 그림 첨부 없음 8 + 결과 읽기 인용 없음 12 + 마지막 코드 셀 뒤 결과 읽기 없음 4(결과 읽기 셀 자체가 0).
- G6 77 = 70자 초과 28(10·6·2·10) · 영문으로 시작해 조사가 붙은 문장 49(7·15·17·10). 금지어는 G6가 대부분 세지 않습니다(§1 표).
- G7 12 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 것 (AST로 따로 셈, `/tmp/ch26-prep/ast_scan.py`)

- **f-string**: 01 c4 `f"openai:{MODEL}"`·`f"{TRAINING_POLICY}\n\n[고객 질문]\n{question}"` · 02 c6 `f"{state['active_agent']}가 답변합니다: {state['message']}"`(**계산 — 딕셔너리 읽기**) · 03 c4·04 c4 `f"openai:{MODEL}"` · 03 c8 f-string(제너레이터 안) · 04 c14 `f"{destination} 담당자로 답하세요: "`. Ch 13~25는 f-string 0건.
- **타입힌트**: 함수 모두 `(… : str) -> str`·`(state: State) -> dict[str, str]`·`-> dict[str, object]`·`-> None`·`response: object` · 변수 힌트 `calls: list[str]`(01 c4)·`records: list[dict[str, object]]`(04 c4)·`router_results: list[str]`(04 c14)·`summary: dict[str, dict[str, float]]`(04 c16). Ch 13·20·23·24·25 노드는 힌트 0(상태 형식 칸 말고).
- **클래스**: `class State(TypedDict)`(02 — Ch 13~25 규칙 「칸 구성이 바뀌면 새 이름」과 다른 막연한 이름) · `class HandoffState(TypedDict)`(04, 칸 다섯) · `class Route(BaseModel)`(03)·`class CompareRoute(BaseModel)`(04, 칸 `destinations: list[Literal["policy", "shipping"]]` — 양식 클래스, Ch 19 02·Ch 21 02 선례).
- **데코레이터**: `@tool`(01 c4 `policy_specialist` · 04 c8 `policy_tool`) — 규격 L6 「이 줄은 아래 함수를 도구로 등록합니다」 설명 0.
- **그 밖**: `[Path.cwd(), *Path.cwd().parents]` 별표 풀기(01·03·04 c2 — 과정 요약 2-2 금지 모양) · 설치 셀에 `%pip`·import·키 확인·`MODEL`·출력이 한 셀(규격 §2-4 준비 네 셀과 다름) · `getattr(message, "tool_calls", [])`(01 c6·04 c8)·`getattr(response, "usage_metadata", None) or {}`(04 c6 — `or` 기본값 모양) · `.get` 다섯(02 c6 `state.get("active_agent")`·04 c6 넷) · `.setdefault`·`+=` 다섯(04 c16) · `set(…)` 비교(03 c6·04 c14)·집합 리터럴 `{"policy", "shipping"}`(04 c14) · `dict(zip(…))`(03 c6) · `bool(…)` 셋(04) · 튜플 풀기 `for name, result in results.items()`(03)·`for pattern, done in …`(04) · `raise ValueError(…)`(04 c14 — Ch 16 01에서 연 이름) · 식 안 요금 숫자 `0.75`·`0.075`·`4.50`·숫자 밑줄 `1_000_000`(04) · `"내부 기록 " * 100`(01 c8 — 글 곱하기, 숫자를 식 안에) · `with ThreadPoolExecutor(max_workers=2) as pool:`·`pool.map`(03 c6 — **`concurrent.futures`는 과정에서 처음**) · `with_structured_output(…, include_raw=True)`·`["parsing_error"]`·`["parsed"]`·`["raw"]`(04 c14) · 함수 본문 8줄(`dispatch`·`record_usage`) · 노드가 노트북 전역 `model`·`measured_call`·`records`를 읽고 씀(04 c10).

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 요청(한 번 실행) | 파일 쓰기 | 손 값 | 금지 문법(셀) | 금지어(`_src` b1~b9 / 노트북 md / 코드 주석) | `assert`(무엇에) |
|---|---|---|---|---|---|---|---|
| 01 | `create_agent(model, tools=[], system_prompt=…)`로 만든 전문 에이전트를 `@tool` 함수 `policy_specialist` 안에서 `specialist.invoke`로 부르고 마지막 메시지 `.text`를 내놓음 → 중앙 에이전트 `supervisor = create_agent(model, tools=[policy_specialist], …)`가 그 도구를 골라 부른 뒤 답 · 도구 함수가 노트북 전역 `calls`에 이름을 붙임 · 「전체 기록 639자 ↔ 전달 38자」 글자 수 비교 | **실제 3**(중앙 2 + 전문 1 — 저장 출력 기준, 사용량 출력 없음) | 없음 | `TRAINING_POLICY` 규정 글(교재용) · **`"내부 기록 " * 100`로 만든 「전체 기록」 639자**(실제 대화 기록이 아닌 손으로 만든 글) · `cost_limit_usd` 1.0 출력 · b5 「예상 API 비용은 1달러 미만」 | c2 별표 풀기·네 일 한 셀 · c4 17줄·힌트·f-string·데코레이터 설명 없음·전역 `calls` · c6 이중 내포식·`getattr`·`assert A and B` · c8 식 안 숫자 100 | 반환 7/2/0 · 문맥 10/1(**Part 3 금지어, Ch 8 「컨텍스트」·「나누기(Isolate)」로**) · 격리 3 · 측정 7/1 · 지연 2 · 스키마 1/1 · 검증 0/1 · 프롬프트 2/1 · docstring 1/1 · 명시 1 · 병렬 1 · supervisor 3/0/1 · 제목·본문 「Subagent」 5 | 4 — `tool_names == ["policy_specialist"] and calls == [...]`(**모델의 도구 선택 — 흔들리는 값**) · **`"3일 이상" in answer and "주문 번호" in answer`(모델 글 속 단어 — 규격 §3 위반)** · 글자 수 비교(손 값끼리) · 키 셀 |
| 02 | **모델 없음** — 상태 `State`(칸 `message`·`active_agent`·`reply`) + 노드 `dispatch`(글에 「환불」이 있으면 `refund_agent`, 없으면 저장된 담당 유지, 없으면 `general_agent`)·`respond` + `InMemorySaver`, 같은 `thread_id` 두 차례로 담당 유지 · 끝 판정은 노트북 셀이 조건 표현식으로 `"END"`를 출력(그래프와 무관) | **0**(API 키 셀·`dotenv` 없음, `%pip`은 `langgraph` 하나) | 없음(메모리 체크포인터) | 입력 글 둘·`A-102` · 스레드 `handoff-demo` | c6 함수 둘·f-string 계산·`.get`·힌트 · c12 조건 표현식·`and` | 반환 1/2 · 런타임 1/1 · 검증 3/1 · 재시작 2 · 필드 1/1/1 · 명시 3/1 · 병렬 1 · 영속 3 · 전환 11/3 · 제목·본문 「Handoff」 6/1 | 2 — `turn2["active_agent"] == "refund_agent"`·`completed`(모두 결정적) |
| 03 | `model.with_structured_output(Route)`(칸 `destinations: list[Literal["policy","shipping"]]`)로 분야를 고름 → `ThreadPoolExecutor(max_workers=2)`·`pool.map(run_specialist, …)`로 고른 분야마다 `model.invoke` → `dict(zip(…))` → 이름을 붙여 `"\n".join(…)` · **`Send`·`Command`·그래프 0건**(b4는 「Command는 한 경로, Send는 여러 경로」라고 적지만 코드는 스레드 풀) | **실제 3**(분류 1 + 전문 2) | 없음 | 요청 글 한 줄·분야 글 둘 · `max_workers=2` | c2 별표 풀기 · c4 힌트·f-string · c6 힌트·`dict(zip(…))` 두 겹·`set`·스레드 풀 · c8 제너레이터·f-string | 반환 4/2/1 · **경로 10/1** · 스키마 2/2 · **지연 5/1** · **병렬 12/7** · 측정 4 · 동시 1/0/1 · 동적 1 · fan-out 2 · 순차 0/1 · 스레드 1/1 · 최대 0/0/1 · 제목·본문 「Router」 10/1 | 1 — `set(results) == set(route.destinations)`(구조 — 고른 이름만큼 실행됐는가) |
| 04 | 세 구조를 한 노트북에서: **Subagent** = `create_agent` 중앙 + `@tool policy_tool`(안에서 `measured_call` — **에이전트가 아닌 모델 요청 하나**) · **Handoff** = `HandoffState` + 조건부 엣지 `route_active`가 `active_agent`를 읽어 `shipping → refund`(**차례를 노드 코드가 미리 정함 — 모델이 넘기지 않음**) · **Router** = `with_structured_output(CompareRoute, include_raw=True)` 분류 + 고른 분야를 `for`로 **차례대로** 요청 + 종합 요청 · `records`에 사용량·손 요금 비용 → `setdefault`로 합계 · 완료 값 셋 | **실제 9**(Subagent 3 · Handoff 2 · Router 4) | 없음 | **요금 0.75·0.075·4.50을 식 안에** · `1_000_000` · b6 호출 수·토큰·비용 전부 한 번 실행 값(3회·0.005498 · 2회·0.000785 · 4회·0.001574) · 「2026-09-11 공식 단가」 | c2 별표 풀기 · c4 힌트 · c6 함수 둘·`.get` 넷·`or {}`·숫자 밑줄 · c8 데코레이터·이중 내포식·`bool` · c10 16줄·함수 셋·힌트·전역 기대 · c12 `bool`·`and` · c14 19줄·`raise`·집합 리터럴·`include_raw` · c16 제너레이터·`setdefault`·`+=` · c18 `all` | 반환 3/2 · 경로 4/0/1 · 검증 2/1 · 지연 2 · **추정 4/1/1** · 측정 5 · 계측 0/1 · **최대 1/1 · 비상 1** · 분기 0/1 · 병렬 1/1 · 관찰 장부 1/1 · trace 0/0/1 · supervisor 2/0/1 · 「Subagent·Handoff·Router」 11/6 | 6 — `sub_done`(**모델 도구 선택 포함**) · `handoff_done and trace == [...]`(코드가 정한 차례) · **`set(destinations) == {"policy","shipping"}`(모델 분류 — 흔들리는 값)** · `all(cost < 1)` · `all(completion)` · 키 셀 |

- **서비스 요청 합계 15번**(01 3 · 02 0 · 03 3 · 04 9). 임베딩 0. 노트북 `%pip`은 01·03·04가 `langchain==1.4.0 langchain-openai==1.6.0 langgraph==1.2.11 python-dotenv==1.2.3`, 02가 `langgraph==1.2.11` 하나. 실습 폴더 dev에 `pip==26.2`, 잠금에 `pip 26.2` 있음(규격 §7-2 조건 충족).
- **`temperature=0`**: 0곳(G4 3). **`reasoning_effort="none"`**: 01·03·04 세 곳. 모델 이름은 `MODEL = "gpt-5.4-mini"`를 f-string으로 이어 붙임(규격 §3 기본 모양과 다름).
- **걸린 시간**: 어느 절도 재지 않음. 그런데 03 b2 「순서대로 호출하면 서로 기다릴 필요가 없는 작업까지 지연됩니다」·b4 「전체 지연만 바꿀 수 있습니다」·b6 「실제 완료 시각은 다를 수 있습니다」, 04 b4 「라우터는 … 병렬로 실행」(04 코드는 `for`로 차례대로) → **재지 않은 시간·속도 단정**(규격 §3, Ch 12 A 07-1).
- **흔들리는 값 처리**: 01·04가 모델의 도구 선택·분류 결과에 `assert`를 걸고, 01은 모델 글 속 단어에 `assert`. 노트북 밖 되풀이 확인 기록 없음. 04 b6·b8·복습 2가 한 번 실행한 호출 수·토큰·비용을 결론처럼 적음.
- **옛 그림 토큰**: 절마다 b4 「도식 읽기」의 `{{svg:NN-흐름}}` 하나(`figures/_gen_figures.py`가 `textbook/part5/_figure.py`의 `linear()`로 만든 상자 넷 세로 흐름도). 노트북 토큰 `{{notebook:slug}}` 넷. Mermaid·삽화 0장.
- 노트북 `metadata.verification`: 넷 모두 `passed`. 실행일 01·02 **2026-09-14**(옛 덧붙임 도구 `part6b_review_fixes.py`가 다시 돌림), 03·04 **2026-09-10**. `code_sha256` 앞 12자 01 `791fcd0bb64f` · 02 `da52d109644a` · 03 `ebd4942f5346` · 04 `0f15ddbd7cb8`. 파일 해시 `d9e73dbb…`·`bfa71019…`·`a0e27cfe…`·`cb8a579c…`(`part6-practice.zip`·`llm-practice.zip` 안 판과 같음). 셀 수 9·13·9·19.
- 노트북 설명 셀: 제목(질문 한 줄) · 「실행 환경 준비」 · 소제목 + `_src` b4 「코드 읽기와 비교 경계」와 같은 글(옛 도구 `part6b_enrich.py`가 끼움) · 소제목 뒤 한두 문장 · **결과 읽기 셀 0**, 「이 노트북에서 할 일」·준비물(요청 수·비용·시간)·실행일 문장 없음, 셀 첨부 그림 0.
- `_src` 틀(옛 생성기 한 틀): b1 셋이 네 절 모두 같은 모양(「{제목}의 핵심 구성 요소를 실제 출력에서 구분할 수 있습니다」…) · **b3 네 절이 글자까지 같음**(「Ch20에서 ToolNode와 명시적 END 조건을, Ch23에서 thread_id와 체크포인터를 배웠습니다. Ch25에서는 실행 사건을 스트리밍했습니다. …」) · b6 둘째 단락 01·03·04 같음 · b7 「비밀 키…」·「외부 모델 호출의 응답과 지연…」 01·03·04 같음 · **b10 참고 자료 다섯이 네 절 모두 같음**(Subagents·Handoffs·Router 문서·langgraph-supervisor·langgraph-swarm, 확인 2026-09-11) · b9 복습 넷.

## 2. 절별로 더 봐야 할 것

### 01 Subagent 도구 위임
- **슬러그 고정**: Ch 25 04 b8(완료, `_src`·HTML·`author_04.py` 533행 `L_CH26_01`)이 `../ch26-delegation/01-Subagent-도구-위임.html`을 링크하고 「전문 에이전트를 도구로 감싸 일을 맡기는 위임 구조를 다룹니다」라고 소개합니다. Ch 8 03 b4·b8·목차 본문(완료, 글만 — 링크 없음)은 「서브에이전트가 따로 받은 컨텍스트로 일하는 모양은 Ch 26 01절」·「서브에이전트로 나누는 방법은 Ch 26 01절」이라고 적습니다 → **01은 ① 전문 에이전트를 도구로 감싸 부르고 ② 전문 에이전트가 따로 받은 컨텍스트(메시지 목록)로 일하는 모양을 보여야** 두 완료 챕터 문장이 참으로 남습니다.
- **모델이 있어야 보이는 절**: 중앙 에이전트가 도구를 고르는 것 자체가 관찰 대상. 설치판 `create_agent`는 도구 여러 개 요청을 한 응답에 담는 것을 막지 않고(`parallel_tool_calls` 인자 없음 — Ch 21 01 「한 응답 요청 둘」 선례), 도구 실행 노드는 한 응답의 도구 요청 여럿을 스레드로 함께 실행합니다(`langgraph/prebuilt/tool_node.py` 821~823행 `executor.map`). → 「전문 에이전트를 한 번 불렀다」는 흔들리는 값(§6).
- **요청 수 세기의 함정**: 중앙 에이전트 결과의 메시지 목록에는 **중앙 에이전트 응답만** 들어 있습니다. 전문 에이전트의 요청은 도구 함수 안 `specialist.invoke` 결과에만 있고 바깥 목록에는 도구 메시지(글) 하나로만 남습니다(e5 — 안쪽 메시지 2개, 바깥에는 `ToolMessage` 하나). Ch 19·20·21 `sum_usage(messages)`를 바깥 목록에 쓰면 전문 에이전트 요청이 빠집니다 → 도구 함수 안에서 `sum_usage(result["messages"])`를 기록 목록에 붙이거나(옛 04 `measured_call` 모양), `langchain_core.callbacks.get_usage_metadata_callback()`(요청 수는 안 셈, 과정에서 안 가르침)을 써야 합니다.
- **「전체 기록 639자 ↔ 전달 38자」는 손으로 만든 비교**: 「전체 기록」 = 요청 글 + `"내부 기록 " * 100`. 실제 대화 기록이 아니고 모델에 보내지도 않음. b6이 「토큰 절감이나 품질 향상을 직접 증명하지 않는다」고 스스로 한정했지만 b5·b8·복습 3이 이 수를 핵심 관찰로 씀. Ch 8 03(완료)이 「나누기가 토큰을 줄이지 않은 해석」을 이미 둠(Ch 8 요약 129행) → 나누기(Isolate)를 보이려면 **전문 에이전트가 실제로 받은 메시지 목록**(안쪽 결과의 `messages` 수·첫 메시지 글)과 **중앙 에이전트 목록**을 나란히 출력하는 편이 출력 근거가 됨(모두 결정적 — 모델 글이 아닌 목록 모양).
- 규정 글 `TRAINING_POLICY`는 「교재용」 표시가 있어 좋음. 소재(배송 지연·환불)는 Ch 21~25의 도서관 자료실 소재와 다름(Ch 19 `orders.csv` 주문 소재와는 가까움) — §11-5.
- b4 「공식 문서는 이를 중앙 집중 제어와 문맥 격리로 설명합니다」 → 공식 문서(2026-09-28 확인): 「By default, subagents are stateless … all conversation memory maintained by the main agent」, 입력 방식 「isolated(과제 글만)」↔「forked(`runtime.state["messages"]`로 부모 기록을 넘김)」, 동기(기다림)↔비동기(작업 시작·상태 확인·결과 받기 세 도구). b7 「병렬 위임은 작업 사이에 선후 관계가 없을 때」는 실행하지 않은 권고.
- `create_agent(…, name="…")`(설치판 인자)는 실행 설정의 `metadata["lc_agent_name"]`에 이름을 적고, 설치판 `langchain/agents/_subagent_transformer.py`가 도구에서 부른 이름 있는 에이전트를 「서브에이전트」로 가려 스트림 쪽에 드러냄(새 스트리밍 규약용 — 이번에 실행하지 않음). 01에서 쓸 필요는 없으나 쓰면 한 문장.

### 02 Handoff 상태 전환
- **지금 판은 핸드오프가 아님(모델·`Command`·도구 0)**: 담당을 바꾸는 쪽은 노드 코드의 `if "환불" in text`(글자 규칙). 공식 핸드오프 두 모양(2026-09-28 확인) — ① **한 에이전트 + 미들웨어**: 도구가 `Command(update={"messages": [ToolMessage(…, tool_call_id=runtime.tool_call_id)], "current_step": "specialist"})`를 내놓고 `@wrap_model_call`이 단계마다 시스템 메시지·도구를 바꿈 ② **여러 에이전트 하위 그래프**: 에이전트마다 바깥 그래프의 노드, 넘기기 도구가 `Command(goto="sales_agent", update={"active_agent": "sales_agent", "messages": [last_ai_message, transfer_message]}, graph=Command.PARENT)`, 바깥 그래프는 `MultiAgentState(AgentState)`(칸 `active_agent: NotRequired[str]`) + `START`의 조건 함수가 저장된 `active_agent`로 첫 노드를 고름 + 체크포인터. 문서: 「A `ToolMessage` must be included … without it, the conversation history becomes malformed」·「assumes only the handoff tool was called (no parallel tool calls)」.
- **지금 판에서 살릴 수 있는 것(결정적)**: 체크포인터 + 같은 `thread_id`로 둘째 차례가 저장된 `active_agent`를 이어받음 — Ch 23 01과 이어짐. 설치판 확인 e2: `START` 조건부 엣지로 저장된 담당에서 시작, `Command(goto="refund_desk", update={"active_agent": …})`로 담당 바꾸기, 둘째 차례 `{'message': '주문 번호는 A-102입니다', 'active_agent': 'refund_desk', …}`, 새 스레드면 첫 담당, 체크포인트 7개(두 차례).
- b4 「런타임이 직전 상태를 읽고 누락된 active_agent를 이어 줍니다」 — 참(체크포인터 값 위에 새 입력 칸만 덮어씀)이지만 「런타임」 금지어. b6 「다음 상태를 END로 표시했습니다」 — 그래프가 아니라 노트북 셀의 조건 표현식이 글자 `"END"`를 출력한 것(과장). b7 「재시작 후에도 상태를 유지하려면 영속 저장소」 — Ch 23 03(SQLite)·02(PostgreSQL)로 이을 수 있음.
- 「Handoff는 함수를 한 번 호출하고 결과를 반환받는 서브에이전트 위임과 다릅니다. … 선택된 담당자가 다음 턴의 제어권을 가집니다」(b4) — 개념 대조로 좋음. 지금 코드에는 「다음 턴의 제어권」이 모델에 넘어가는 장면이 없음.

### 03 Router 분류와 병렬 실행
- **Ch 18 02·03과 겹침(완료)**: Ch 18 02 「라우팅(routing) — 모델이 쓴 종류를 보고 코드가 준비한 갈래로」(허용 목록·신뢰도·기준값·되묻기) · 03 「함께 보내기(parallelization) — 나눠 쓰기·투표」(OpenAI SDK + `asyncio.to_thread`·`gather`, **03은 걸린 초를 잰 주제 절 예외지만 걸린 초·도착 차례 비교는 결론·그림·정리에서 뺌**). Ch 26 03이 새로 보일 것은 **LangGraph로 같은 모양을 만드는 방법 — 구조화 출력 분류 + `Send`로 고른 분야마다 노드 실행 + 리듀서로 결과 모으기 + (종합)**. 공식 Router 문서도 「병렬은 `Send`, 한 갈래는 `Command(goto=…)`」.
- **지금 판은 `Send`·그래프 0건, `concurrent.futures.ThreadPoolExecutor`(과정 처음)**. Ch 13 05(완료)가 `Send`·팬아웃·「결과가 모이는 차례는 우리가 정하지 않습니다 → 자리 번호를 함께 보내 맞춤」을, 06이 `Command(update=, goto=)`·`destinations=`를 가르침 → 03은 Ch 13 05·06을 이어 쓰는 편이 새 API가 적음.
- **설치판 확인(e1, 모델 없음)**: `Send` 두 갈래가 같은 단계에서 **동시에 실행**(0.5초·0.2초 잠드는 노드 → `invoke` 0.51초, 세 번 같음) · 모드 `updates` 사건은 **끝난 차례**(0.2초 쪽 `shipping`이 먼저) · 리듀서 칸(`Annotated[list, operator.add]`)에 모인 차례는 **`Send`를 만든 차례**(`['policy 답', 'shipping 답']` 세 번 같음 — 설치판 `pregel/_algo.py` 253~256행 「sort tasks on path, to ensure deterministic order」). 리듀서 없는 칸이면 `InvalidUpdateError`(Ch 13 05 오류 장면과 같음). **Ch 13 05 「결과가 모이는 차례는 우리가 정하지 않습니다」와 부딪힘** — 소스로는 정해진 차례이나 Ch 13은 자리 번호로 맞추라고 가르침(§8-4).
- **고른 분야가 0개면**(e5) 조건 함수가 빈 목록을 내놓고 **종합 노드가 실행되지 않은 채 그래프가 조용히 끝남**(오류 없음, `final` 빈 글). 같은 분야 둘이면 둘 다 실행. b7 「분류 결과가 비어 있을 때의 기본 경로도 정해야 합니다」·복습 3이 이 장면을 말로만 다룸 → 실제 조건으로 보일 수 있음(모델 없이).
- `with_structured_output(Route)` 분류는 Ch 6 03(구조화 출력) 이름. 칸 `list[Literal[…]]`는 Ch 19 02·Ch 21 02 양식 클래스 칸 선례. 분류 결과(고른 분야 목록)는 **흔들리는 값**(옛 04 `assert set(destinations) == {"policy","shipping"}`).
- b2 「순서대로 호출하면 … 지연됩니다」·b4 「전체 지연만 바꿀 수 있습니다」·b6 「실제 완료 시각은 다를 수 있습니다」는 재지 않은 시간 단정. `updates` 사건 차례(끝난 차례)로 「동시에 돌았다」를 보이면 시간을 재지 않고도 구조를 보일 수 있으나 그 차례는 흔들리는 값(모델 요청이면 도착 차례가 바뀜 — Ch 18 03 선례).

### 04 호출 수·비용·종료 조건 비교
- **세 구조가 같은 일을 하지 않음(비교 설계의 결함, 가장 큼)**: Subagent 쪽 도구 안은 에이전트가 아닌 모델 요청 하나 · Handoff 쪽은 모델이 넘기지 않고 노드 코드가 `shipping → refund` 차례를 정함(`route_active`는 코드가 적은 값을 읽을 뿐) · Router 쪽은 고른 분야를 `for`로 차례대로 요청(`Send`·동시 실행 없음)하고 **종합 요청을 하나 더** 함 → 「Subagent 3회 · Handoff 2회 · Router 4회」는 구조 차이가 아니라 코드에 적은 요청 수. b4 「이름만 바꾼 고정 호출 목록으로는 차이를 검증할 수 없으므로」(옛 검토 `integration-review.md` 11행이 고친 결함)라고 적었지만 Handoff는 여전히 고정 차례.
- **공식 문서의 요청 수 표(2026-09-28 확인, multi-agent 개요)**: 한 번 요청 「Buy coffee」 Subagents 4 · Handoffs 3 · Skills 3 · Router 3(「Subagents adds one extra call because results flow back through the main agent」) · 같은 요청 되풀이(두 차례) Subagents 8 · Handoffs 5 · Skills 5 · Router 6 · 여러 분야 Subagents 5(~9K 토큰) · Handoffs 7+(~14K+) · Skills 3(~15K) · Router 5(~9K). → **구조가 정하는 요청 수**(가장 적게 부른 경우)를 결론으로, 실제 요청·토큰·비용은 둘째 단락으로 두는 설계 근거(§6-2).
- **종료 조건**: b4 「recursion_limit 같은 실행 한도는 비상 경계」 + 「‘최대 세 번 호출’ 같은 실행 한도」 — Ch 20 03(완료)이 「실행 한도 = 그래프 단계 수」로 정한 말을 호출 수 상한 뜻으로 씀(Ch 20 요약 §13·계약 §3 Ch20 줄) → 「바퀴 한도(Ch 17 03)」 또는 「호출 한도(Ch 16 04·Ch 22 04 `ModelCallLimitMiddleware`)」로. 「비상 경계」·「최대」 금지어. 코드의 완료 값 셋(`sub_done` 등)은 `bool(글 and …)` — 한도·실패 장면은 실행하지 않음.
- 비용: `record_usage`가 손 요금을 식 안에 적음 → Ch 6 06 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`(Ch 21 `runner_tools.py`·Ch 25 `stream_tools.py`와 같은 본문)로. 「추정 비용」 → 「예상 비용」(Ch 6 06 뜻), 요금표 날짜는 과정 요금표(2026-09-17, Ch 25 검토 B가 2026-09-25 다시 확인).
- b7 langgraph-supervisor 문장 — 2026-09-28 다시 확인 참(README 「We now recommend using the supervisor pattern directly via tools rather than this library for most use cases」, 최신 0.0.31·2025-11-19). 설치 잠금에 `langgraph-supervisor`·`langgraph-swarm` 없음(실행하지 않은 라이브러리).
- **b8 「Ch39에서는 종료 조건을 평가 지표와 실패 예산으로 다시 다룹니다」 — 과정에 Ch 39가 없음(Ch 34까지)**. `labs/part6/continuity-guide.md` 12행 「Ch27의 서브에이전트, Ch39의 정지 조건」도 같은 끊긴 가리킴. Ch 27 쪽 문장(「파일시스템·Subagent·문맥 관리를 미리 조립한 DeepAgents 하네스로 이 위임 구조를 확장합니다」)은 Ch 27 01·06과 맞음.

## 3. 실습 폴더 구조와 읽는 곳

```
labs/part6/ch26-delegation/
  README.md (한 문단 — 「번호 순서대로 새 Python 3.12 커널 · .env의 OPENAI_API_KEY 값은 출력하지 않음 · 절별 예상 API 비용 1달러 미만」, uv sync 안내 없음, 02가 키 불필요라는 말 없음)
  pyproject.toml   uv.lock (88 package 항목, export 87줄)
  notebooks/01~04-*.ipynb
  .venv/ (macOS 판 174MB — home = /Users/…/cpython-3.12-macos-aarch64-none, uv 0.11.6, prompt kdt-ch26-delegation)
  (없음: data/ · runs/ · tests/ · 도구 파일 · worker · 노트북 생성기)
```

- **노트북이 쓰는 파일: 0**(네 절 모두 `open`·쓰기 없음, 02만 `InMemorySaver`). 노트북이 읽는 파일은 01·03·04의 `.env`뿐(`Path.cwd()`와 부모 폴더를 거슬러 찾음). 연결 폴더 SQLite 멈춤(Ch 23 발견)은 지금 판에는 해당 없음.
- **Ch 26 파일을 코드로 읽는 곳**(`grep -rIl`, `textbook`·`labs`·`.moai`, `.venv`·`.cache`·zip 제외):

| 자리 | 무엇을 | 성격 |
|---|---|---|
| `textbook/part6/public-files.json` 53~57행 | README·노트북 넷(**`pyproject.toml`·`uv.lock` 줄 없음**) | 묶음 허용 목록. zip에는 잠금 둘이 들어감(`build_bundle.py`가 실습 폴더 잠금을 함께 넣음 — Ch 25와 같음) |
| 챕터 `qa/public-files.json` | HTML 5 + 실습 파일 5 = 10(옛 SVG 줄 없음) | `collect_public_files.py`가 Part 목록으로 모음 |
| `textbook/downloads/part6-practice.zip`(`71683e44…`)·`llm-practice.zip` | Ch 26 일곱 파일(노트북 넷·README·`pyproject.toml`·`uv.lock`)이 **디스크와 같음** | 묶음 |
| `textbook/part6/_build_index.py` 24행 · `textbook/_notebook/build_index.py` 56~57행 · `build_bundle.py` 25행 | (4, 4, 「세 가지 위임 구조를 구현하고 호출 수·비용·종료 조건을 비교합니다.」) · (절 수 4, 「Subagent·Handoff·Router를 구현하고 같은 과제의 호출 수·비용을 비교합니다.」) · 공개 챕터 목록 | 실습 절을 붙이면 Part 목차는 절 다섯(`_notebook/build_index.py`는 실습 절을 빼고 세는 과정 전체 약속 — 4 그대로) |
| Part 6·7 선행 목록(`prerequisite-files.json`) · `existing-artifact-hashes.json` · 챕터 `qa/prerequisite-files.json`(`[]`) | **Ch 26 줄 0** | 뒤 챕터가 Ch 26 파일을 읽지 않음 |
| Part 6 `check_bundle_execution.py` 30~31행 | Ch 24 01·Ch 28 01만(**Ch 26 안 봄**) | 묶음 실행 계약 없음 |
| Part 7 `check_bundle_execution.py` | Part 7 챕터만 | — |
| 옛 검사(고치지 않음, 기록만) | `check_scope.py` 12행 `EXPECTED` (4,4)·`SECTION_COUNTS` 4(실습 절을 붙이면 어긋남, 이미 Ch 21에서 멈춤) · `check_notebook_readiness.py`(노트북 수 단언 — 결과 파일을 먼저 씀 → 되돌림 선례) · `check_figures.py`(SVG마다 `.excalidraw` 짝) · `check_visual_reports.py` · `check_delivery.py`(`llm-practice.zip` 신선도) | Ch 21~25 선례대로 이미 어긋난 상태 |
| 기록만 | `final-artifact-hashes.json`(Ch 26 줄 30 — **노트북 넷·`_src` 넷·HTML 넷 = 12줄은 이미 옛 해시**, 그림·README·잠금 등 18줄은 같음) · `notebook-executions.json`·`notebook-readiness.json`·`figure-consistency.json`(각 4) · `visual-results.json`(10) · `lesson-scope.json`·`prose-repetition-initial.json`(1) · `integration-review.md` 11·12행 · `verification.md` 16행 · `language/ch26-final.{json,md}`·`ch25-ch26-original-prose.sha256`·`ch26-original/` · Part 7 `existing-artifacts-before.json`(8)·`before-integration/build_*.py` · `_notebook/checks/notebook-contracts-part6-ch26-delegation.json`(verify가 다시 씀)·`checks/ch26-delegation/`(옛 화면 검사 PNG 넷) · 챕터 `qa/ch26-code-output-preservation.sha256`(13줄 — 노트북 넷은 이미 옛 해시) · `.moai/…/ch26-delegation-visual-state.json` 등 | — |

- **옛 생성기**:

| 파일 | 무엇을 씀 | 비고 |
|---|---|---|
| **`textbook/part6/_generate_ch25_ch26.py`**(565줄, `0767052613d9…`, **Ch 25·26 공용**) | `write()` — **Ch 26 노트북 넷(출력 없이 — 지금 출력이 모두 지워짐)** · `chapter.json`(**`part_title` 「Part 6 · Agent 심화」 — 지금 파일은 「Agent 개발」**) · 실습 폴더 `pyproject.toml`·`README.md` · `_src`(`page()` 틀 — 옛 「calls에는 policy_specialist와 main_agent가 순서대로」·「policy_tool.invoke」 같은 옛 검토 전 글) · `research.md`·`qa/authoring-checklist.md`·`집필점검표.md` · 챕터 `qa/public-files.json`. `--pages-only`는 `_src`만 | Ch 25 01절이 Ch 25 쪽만 건너뛰게 함(머리 주석 넷 + `continue` 셋, 515·520·555행). **Ch 26 쪽은 그대로 — 지금 돌리면 Ch 26 개선본을 옛 판으로 덮어씀.** 부르는 스크립트 0(`grep` — 기록 문서만). 사본 `before/generators/_generate_ch25_ch26.py`(지금 판) · Ch 25 `before/generators/`(원본 `545db83c…`) |
| `figures/_gen_figures.py`(Ch 26, `af127dca…`) | `NN-흐름.{svg,excalidraw,caption.md}` 12개(`textbook/part5/_figure.py`) | 옛 그림 네 벌. 사본 `before/generators/`·`before/figures/` |
| (챕터 밖) `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part6b_enrich.py`·`part6b_review_fixes.py`(43·86·113·125행) | Ch 26 01·02 노트북 설명 셀·`_src` 단락 덧붙임·다시 실행 | 기록만(Ch 21·23·24·25 선례) |
| `textbook/part6/_author_ch21_ch29.py` | **Ch 26 안 씀**(`grep` 0) | — |

→ **Ch 25 요약 §13-7·체크리스트 222행 약속**: Ch 26 01절이 `_generate_ch25_ch26.py` 첫머리를 막고(설명 주석 + `raise SystemExit(...)`), **Ch 26 마감에 `mv -n`**으로 `ch26-delegation/qa/upgrade/before/generators/blocked/`에 옮김(Ch 23·24 공용 생성기 선례 — 옮긴 자리와 부르는 스크립트 0을 `grep`으로 확인하고 Ch 25 요약·체크리스트 §2-13에 한 줄). 파일 자리가 Part 6 맨 위라 챕터 밖 수정 — 진단·요약에 한 줄. Ch 26 `figures/_gen_figures.py`는 01절에서 막고 마감 때 `mv -n` → `qa/upgrade/before/generators/blocked/`(Ch 25 선례).

- **판**: `requires-python = ">=3.12,<3.13"`, `dependencies = ["langchain==1.4.0", "langchain-openai==1.6.0", "langgraph==1.2.11", "python-dotenv==1.2.3"]`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`, `[tool.uv] package = false`. 잠금 주요 판: `langchain-core 1.6.2`·`openai 3.11.0`·`langgraph-checkpoint 4.2.0`·`langgraph-prebuilt 1.1.0`·`langgraph-sdk 0.4.4`·`langsmith 0.12.4`·`pydantic 2.13.5`. **`numpy`·`pillow`·`langgraph-checkpoint-sqlite`·`langgraph-supervisor`·`langgraph-swarm` 없음.** `pyproject.toml`·`uv.lock` 수정 시각 09-10 그대로.
- **Ch 25 잠금과 견줌**: `diff` 결과 **프로젝트 이름 두 줄(`kdt-ch25-streaming` ↔ `kdt-ch26-delegation`)만 다름** — 판 모두 같음. 따라서 Ch 21 잠금과는 `numpy 2.5.3`·`pillow 12.3.0` 둘만 다름. **Ch 21 `runner_tools.py`는 맨 위에서 `numpy`를 가져와 Ch 26 잠금에서는 import 자체가 멈춤**(파일째 가져오기 불가 — §7). Ch 23 `checkpoint_tools.py`(SQLite)도 같음.
- `pytest`·`tests/` 없음. 실습 폴더 `.venv`는 macOS 판(삭제 승인 대상).

## 4. 앞뒤 챕터 이음새

### 4-1. Ch 25 인계(요약 §13·§14·§15, 계약 §3 Ch25 줄) 항목별 지금 상태

| 인계 항목 | 지금 Ch 26 원고 | 상태 |
|---|---|---|
| 01~04 b3 「Ch25에서는 실행 사건을 스트리밍했습니다」는 참 | 네 절 글자까지 같음 | **참** — 다만 b3 전체가 틀 문장(Ch 20·23·25 한 줄씩)이라 절마다 이 절에 맞는 앞 내용(Ch 8 03·Ch 13 05·06·Ch 18 02·03·Ch 19~21·Ch 22 04·08)으로 다시 쓸 자리 |
| ① 동기 `stream`만 · `astream`·`stream_events`·`subgraphs=True` 0건 | Ch 26은 스트리밍 0건(`stream` 호출 없음) | 어긋남 없음. 위임 구조를 스트리밍하면 Ch 26이 처음(하위 그래프 사건은 `subgraphs=True`로 `(ns, 모드, 자료)` 짝 — Ch 25 준비 조사 e2) |
| ② 노드 하나짜리 작은 그래프만 · 여러 노드·에이전트 그래프·노드 이름 거르기·`ToolMessage` 사건 0건 | Ch 26도 안 씀 | 어긋남 없음(쓰면 첫 자리에서 가르침) |
| ③ 초는 조건마다 한 번 · 초 비교는 결론 아님 | Ch 26은 초를 안 잼. 그런데 03 b2·b4·b6 「지연」·「완료 시각」 단정 | **Ch 25 근거와 무관한 규격 §3 문제** — 고칠 자리(§2 03) |
| ④ 예상 비용은 Ch 25 도구 파일 `estimate_cost`(Ch 21 판 글자 그대로) · Ch 25 도구 파일은 파일째 가져오지 말 것 | 04 `record_usage`가 손 요금을 식 안에 | `estimate_cost` 본문을 Ch 26 도구 파일로 옮겨 오거나 노트북에 다시 적음(§7) |
| ⑤ 모델 요청 수는 Ch 25 그래프의 값 — Ch 26 「호출 수」 비교에 쓰지 않음 | Ch 26은 Ch 25 수를 안 씀 | 어긋남 없음 |
| ⑥ 말: 「이벤트」·「조각」·「지연」·「측정」·「추정」·「구독」 0 | 「지연」 01 2·03 5+1·04 2 · 「측정」 01 7+1·02 2·03 4·04 5 · 「추정」 04 4+1+1 · 「계측」 04 md 1 | **고칠 자리**(§1 표) |
| ⑦ 공용 옛 생성기 `_generate_ch25_ch26.py` — Ch 26 01절이 막고 Ch 26 마감에 `mv -n` | Ch 26 쪽 그대로 | **Ch 26 몫**(§3) |

- **Ch 20 인계**(Ch 20 요약 §13 「Ch 26 delegation」·계약 §3 Ch20 줄): b3 「Ch20에서 ToolNode와 명시적 END 조건을 … 배웠습니다」는 참(Ch 20 01·03·05) · **04 b4 「실행 한도」를 호출 수 상한 뜻으로 씀 → 바퀴 한도·호출 한도** · 「비상 경계」·「추정 비용」(→ 예상 비용)·「최대」. 모두 미해결.
- **Ch 23 인계**(Ch 23 요약 204행): b3 「Ch23에서 thread_id와 체크포인터를 배웠습니다」는 참(01). 02가 체크포인터를 쓰면 `InMemorySaver`·`thread_id`·`get_state`는 이어 쓰기(Ch 23 01).
- **Ch 8 인계**(Ch 8 요약 137행·체크리스트 36행): **「Ch 26 01 「문맥 격리」·03 「나누기(Isolate)」 말 맞추기(Ch 26 개선 때)」** — 지금 01 b4·b8 「문맥 격리」 3회·「문맥」 10회, Ch 8 03 말은 「나누기(Isolate)」(업무마다 메시지 목록을 따로 만들어 요청 하나에 한 업무 자료만). Ch 22 08(완료, 시범)은 같은 Isolate를 「컨텍스트 분리(Isolate)」라고 부름 → 두 이름 중 무엇을 이을지 정할 자리(§8-2).

### 4-2. 앞 챕터에서 가르친 것 (Ch 26이 전제할 수 있는 것)

| 챕터·절 | 가르친 것 | Ch 26과의 관계 |
|---|---|---|
| Ch 6 03·06 | `with_structured_output`·구조화 출력 · 요금표·`estimate_cost`·「예상 비용」(청구 금액 아님) | 03 분류 · 04 비용 |
| Ch 8 03 | **나누기(Isolate)** — 업무마다 메시지 목록을 따로(`build_messages`) · 「이 절에는 에이전트가 없습니다 … Ch 26 01절에서」 | 01의 개념 뿌리(§4-3) |
| Ch 13 02·03·05·06 | 리듀서 `Annotated[list, operator.add]` · 조건부 엣지·`path_map` · **`Send`·팬아웃·갈래별 상태·`InvalidUpdateError`**·「결과 차례는 자리 번호로 맞춤」 · **`Command(update=, goto=)`·`add_node(…, destinations=(…))`** | 02 담당 넘기기·03 팬아웃의 직접 선례 |
| Ch 16 04 | 호출 한도(예산의 요청 수 상한, `make_budget`·`reserve`) | 04 종료 조건 말 |
| Ch 17 03 | 루프·바퀴·**정지 조건 넷**(모델의 끝 선택·사람 확인·같은 도구 다시 고름·바퀴 한도)·바퀴 한도 ≠ 호출 한도 | 04 「종료 조건」은 Ch 17 「정지 조건」과 같은 뜻인지 정할 자리 |
| Ch 18 02·03·04·06 | **라우팅**(모델이 쓴 종류 → 코드가 준비한 갈래)·갈래·허용 목록·되묻기 · **함께 보내기(parallelization)**·나눠 쓰기·도착 차례 · **작업 나눠 맡기기(orchestrator-workers)**·계획 모델·작업 모델·종합 · 같은 조건 비교·요청 수(`calls`) — 모두 OpenAI SDK, 다음 단계는 코드가 고름 | 03 라우터가 Ch 18 02·03과 겹침 · 01 서브에이전트가 Ch 18 04(계획 모델이 작업 모델에 맡김)와 겹침 — 차이는 「모델이 도구를 골라 맡기는가」 |
| Ch 19 01·02·04·05·06 | `@tool`(세 문장 + Ch 2 09 링크)·독스트링·양식 클래스 칸 `Literal` · `tool_calls` · `ToolMessage`·호출 ID · `sum_usage`·`show_messages`·`tool_call_names` | 01 도구로 감싸기 · 요청 수 세기 |
| Ch 20 01·03 | `ToolNode`·되돌아가는 엣지 · **실행 한도 `{"recursion_limit": N}`·`GraphRecursionError`(03, 모델 없음)** · 명시적 종료 | 04 종료 조건 |
| Ch 21 01·03·07 | `create_agent(model, tools=…, system_prompt=…)`·에이전트 그래프 · `AgentState` 확장(칸만)·`context_schema`·**`ToolRuntime[…]`(대괄호 예외, `runtime.context`)** | 01 전문·중앙 에이전트 · 02 넘기기 도구의 `runtime.tool_call_id`·`runtime.state`는 새 속성 |
| Ch 22 04·07·08 | **`ModelCallLimitMiddleware(run_limit=…, exit_behavior="end")`(호출 한도)** · 감싸기형 훅 `@wrap_model_call`·`request.override(messages=…)`로 요청만 바꾸기(08 컨텍스트 분리) | 04 한도 장면 · 02 「한 에이전트 + 미들웨어」 핸드오프 모양의 선례 |
| Ch 23 01 | `InMemorySaver`·`thread_id`·`get_state`·`get_state_history` | 02 다음 차례 이어 가기 |
| Ch 24 01 | `Command(resume=…)` — `Command`의 다른 쓰임 | 02 `Command(goto=…)`와 가를 한 문장(Ch 13 06 `goto`·Ch 24 `resume`·Ch 26 `graph=Command.PARENT`) |
| Ch 25 01~03 | 스트림 모드·모드 `updates`·`tasks` 사건 | 03 「같은 단계에서 동시에 실행」을 사건 차례로 보이는 도구(쓰면) |

### 4-3. 완료 챕터가 Ch 26에 기대는 문장 — 개선 뒤에도 참이어야 함

| 자리 | 문장 | 조건 |
|---|---|---|
| **Ch 25 04 `_src` b8(+ HTML·`author_04.py` 533·612행)** | 「이 절로 Ch 25가 끝납니다. Ch 26 01절에서는 전문 에이전트를 도구로 감싸 일을 맡기는 위임 구조를 다룹니다」 + **01 슬러그 링크** | **01 슬러그 `01-Subagent-도구-위임` 유지** · 01이 전문 에이전트를 도구로 감쌈 |
| **Ch 8 03 `_src` 39행(b4)·83행(b8)·`index-body.html` 34행(+ HTML 둘·`집필점검표.md`)** | 「서브에이전트가 따로 받은 컨텍스트로 일하는 모양은 Ch 26 01절에서 다룹니다」 · 「서브에이전트로 나누는 방법은 Ch 26 01절에서 다룹니다」 · 「서브에이전트로 나누기는 Ch 26 01절」 | 01이 전문 에이전트가 **따로 받은 메시지 목록**으로 일하는 모양을 보임(글자 수 비교만으로는 약함) |
| Ch 20 요약 §13 · Ch 23 요약 204행 | b3 Ch 20·23 문장 참 | b3를 고쳐도 Ch 20·23 이음이 남으면 참 |
| Ch 18·19·21·22 `_src` | Ch 26 언급 0(`grep`) | — |

### 4-4. 뒤 챕터(대기)가 Ch 26에 기대는 문장 — 고치지 않음

| 자리 | 문장 | Ch 26 쪽 사실(지금 판) |
|---|---|---|
| Ch 27 01 `_src` b3(+ HTML·`qa/author_ch27.py` 38행) | 「Ch 24는 사람 승인을, Ch 26은 위임 구조를 다뤘습니다」 | 참 |
| Ch 27 03 `_src` b3(+ `author_ch27.py` 54행) | 「Ch 26에서 위임 완료 조건을 **문장으로 적었습니다**」 | **부분 참** — 04가 완료 값(`sub_done` 등)을 코드로 셈. 「문장으로」는 04 b2 「‘무엇이 생기면 끝인가’를 각 구조의 상태로 적습니다」와 가까움. 04에서 완료 조건을 말로 적는 자리가 남으면 참 |
| Ch 27 06 `_src` b3(+ `author_ch27.py` 78행) | 「Ch 26에서 **서브에이전트의 완료 조건**을 적었습니다」 | **부분 참** — 04 `sub_done`(도구 이름 차례 + 답 글 있음). 서브에이전트 쪽 완료 조건이 04(또는 01)에 남아야 참 |
| Ch 27 01~08 | 「서브에이전트」·「위임 도구」·「task ToolMessage」(DeepAgents) | Ch 26 말(서브에이전트·위임)과 같은 말을 씀 → Ch 26이 용어를 바꾸면(예: 「전문 에이전트」) Ch 27과 이름이 갈림 |
| Ch 34 03 `_src`(모델 라우팅) | b3 「Ch 18에서는 코드가 분기를 고르는 라우팅 패턴」 — Ch 26 언급 0 | 계약 아님. 「라우터」 = 모델을 고르는 함수(다른 뜻) |
| `labs/part6/continuity-guide.md` 12행 | 「Ch18의 패턴과 Ch21의 에이전트 \| Ch26 도구로 위임·활성 담당 변경·라우팅 \| Ch27의 서브에이전트, **Ch39의 정지 조건**」 | 둘째 칸 참 · **「Ch39」는 없는 챕터**(과정은 Ch 34까지) — 마감 때 고칠 자리(보호 파일, 묶음에 들어감) |
| Part 6 `_src/index.html` 8행 · `practice-start.md` 15행 | 「Ch 26–28은 다른 에이전트·파일·외부 도구를 연결하는 범위를 넓힙니다」 · 「Ch 25에서 스트리밍을 관찰한 뒤 Ch 26의 위임」 | 참 |
| `textbook/part6/_build_index.py` 24행 · `_notebook/build_index.py` 56~57행 | 「세 가지 위임 구조를 구현하고 호출 수·비용·종료 조건을 비교합니다」 · 「Subagent·Handoff·Router를 구현하고 같은 과제의 호출 수·비용을 비교합니다」 | 마감 때 새 본문과 대조(`objectives`도) |
| Ch 27~29·Part 7 노트북·코드 | Ch 26 파일을 읽는 코드 0 | **산출 파일 계약 없음** |

### 4-5. Part 6 묶음·목록·기록·검사

- Part 6 선행 목록(`prerequisite-files.json` 13줄)·`existing-artifact-hashes.json`·Part 7 선행 목록에 Ch 26 줄 **0**. `final-artifact-hashes.json` Ch 26 줄 30개 중 12개가 이미 옛 판(만드는 스크립트 없음, Ch 21·23·24·25 선례대로 기록만).
- 공개 목록 두 곳 + zip 두 개(§3). **묶음 실행 검사 계약 없음**(`check_bundle_execution.py` 목록은 Ch 24 01·Ch 28 01). 모델 없는 절(지금 02)을 넣을지는 Ch 25 01과 같은 전체 마감 후보.
- 도구 파일을 만들면 `notebooks/…_tools.py` 줄을 두 목록(`textbook/part6/public-files.json`·챕터 `qa/public-files.json`)에 더하고 zip 다시 만들기(Ch 25 마감 모양 — `python3 textbook/part6/_build_index.py`를 마지막에 한 번).
- 뒤 챕터가 Ch 26 노트북·출력·파일을 읽는 코드: **0**(Ch 27~29·30·31·34 모두 — Ch 29 04는 Ch 18 06·Ch 21 06만 읽음). Ch 26은 산출 파일을 쓰지 않음 → **파일 계약 없음**.
- 옛 검사 스크립트(기록만, 고치지 않음): Ch 25 마감 기록대로 넷 모두 Ch 26에 닿기 전에 멈춤(`check_scope.py` Ch 21 07 「실습 30분」 · `check_figures.py` Ch 21 SVG 짝 · `check_notebook_readiness.py` 노트북 수 단언 — 결과 파일을 먼저 씀 → 실행 전 사본으로 되돌림 · `check_visual_reports.py` `ch22-middleware`). Ch 26에 실습 절을 붙이면 `check_scope.py` `SECTION_COUNTS` 4 ≠ 5도 더해짐. `check_delivery.py`는 `llm-practice.zip` Part 1 Stale에서 멈춤(Ch 25 마감 기록).

## 5. 라이브러리 동작 — 설치판 소스와 모델 없는 확인 (2026-09-28, `langgraph 1.2.11`·`langchain 1.4.0`·`langchain-core 1.6.2`)

### 5-1. 에이전트를 도구로 감싸기 (서브에이전트)
- 설치판에 「에이전트를 도구로」 만드는 전용 함수는 없음. 공식 모양 = `@tool` 함수 안에서 `subagent.invoke({"messages": [{"role": "user", "content": query}]})` → `result["messages"][-1].content`(문서) — 지금 01과 같은 모양(`.text`).
- `create_agent` 서명(`langchain/agents/factory.py` 772~789행): `model, tools, *, system_prompt, middleware, response_format, state_schema, context_schema, checkpointer, store, interrupt_before, interrupt_after, debug, name, cache, transformers`. **`parallel_tool_calls`·`max_iterations` 인자 없음.** `name=`은 설정 `metadata["lc_agent_name"]`(1831~1834행).
- `create_agent`가 컴파일한 그래프에 **`with_config({"recursion_limit": 9_999})`**(1831행 설정 딕셔너리 · 1857행 `.with_config(config)` — langgraph 이슈 7313 주석) → 에이전트 그래프의 실행 한도 기본값은 9999(e4 `spec.config` 출력). 그냥 `StateGraph.compile()`은 `config` 없음 → `DEFAULT_RECURSION_LIMIT = 10007`(`langgraph/_internal/_config.py` 32행, Ch 20 03 기록과 같음).
- 도구 없는 에이전트(`tools=[]`)의 노드는 `['__start__', 'model', '__end__']`, 도구가 있으면 `['__start__', 'model', 'tools', '__end__']`(e4). `@tool` 함수는 `StructuredTool`, 인자 `{'question': {'title': 'Question', 'type': 'string'}}`. 에이전트 그래프에도 `as_tool` 메서드가 있으나(e4 `True`, 과정에서 안 씀) 공식 문서 모양은 `@tool`.
- 도구 실행 노드는 한 응답의 도구 요청 여럿을 함께 실행(`tool_node.py` 821~823행 `get_executor_for_config`·`executor.map`) — 전문 에이전트 두 번 요청이 오면 두 `invoke`가 스레드로 함께 돔.
- **안쪽 메시지는 바깥에 섞이지 않음**(e5, 모델 없는 안쪽 그래프): 도구 안 그래프의 메시지 2개는 바깥 목록에 안 들어가고, 바깥에는 도구 메시지(`name='ask_specialist'`·`tool_call_id`)만 붙음 → 나누기(Isolate)의 출력 근거.
- `ToolRuntime` 칸(e6): `state`·`context`·`config`·`stream_writer`·`tool_call_id`·`store`·`tools`·`execution_info`·`server_info`. Ch 21 03은 `runtime.context`만 가르침.

### 5-2. 핸드오프 — `Command(goto=…, update=…, graph=Command.PARENT)`
- `Command` 칸(`langgraph/types.py` 799~848행): `graph`(`None` = 지금 그래프, **`Command.PARENT` = `"__parent__"` = 가장 가까운 바깥 그래프**)·`update`·`resume`·`goto`(노드 이름·이름 목록·`Send`·`Send` 목록).
- **노드가 내놓는 `Command(goto=, update=)`**(Ch 13 06): e2 — `add_node("front_desk", front_desk, destinations=("refund_desk", END))`, 그림 문자열에 점선 `front_desk -.-> refund_desk`. `goto` 목록이면 여러 노드로(e2 `multi goto`).
- **`goto`에 없는 노드 이름을 적으면 오류 없이 경고만 남기고 조용히 끝남**(e2 — 「Task bad … wrote to unknown channel branch:to:nowhere, ignoring it.」, 설치판 `pregel/_algo.py` 312행). 이름 오타가 멈춤으로 드러나지 않는 위험.
- **도구가 내놓는 `Command`와 `ToolMessage`**(`langgraph/prebuilt/tool_node.py` 1503~1578행 `_validate_tool_command`): 지금 그래프(`graph=None`)로 가는 `Command`의 `update["messages"]`에 **같은 호출 ID의 `ToolMessage`가 없으면 `ValueError`**(e3 — 「Expected to have a matching ToolMessage in Command.update for tool 'transfer_no_msg' … MUST have a corresponding ToolMessage」) · 있으면 통과(메시지 `['AIMessage', 'ToolMessage']`) · **`graph=Command.PARENT`이면 이 검사를 하지 않음**(1559~1562행 `require_terminator and updated_command.graph is None`). 도구 실행 노드가 바깥 그래프 없이 돌면 `ParentCommand` 예외가 올라옴(e3). 하위 그래프 안에서 `graph=Command.PARENT`로 넘기면 바깥 그래프의 다른 노드로 감(e3 `outer -> refund`) — **이때 `ToolMessage`를 넣지 않으면 바깥 기록에 도구 요청만 있고 답이 없는 응답이 남음**(e3 메시지 `Human·AI(도구 요청)·AI`) → 다음 모델 요청에서 문서가 말하는 「malformed」 기록(서비스 모델에서는 실행하지 않음). 공식 넘기기 도구는 `update`에 `last_ai_message`와 `ToolMessage`를 함께 넣음.
- 도구 실행 노드는 한 응답의 부모행 `Command` 여럿이 모두 `Send` 목록일 때만 하나로 합침(868~915행) — 이름 `goto`가 둘이면 따로 둘(두 넘기기 도구를 한 응답에 부르는 장면은 문서가 「no parallel tool calls」로 전제).
- 다음 차례 이어 가기(e2): 체크포인터 + `START` 조건부 엣지(저장된 `active_agent`로 첫 노드 고름) → 둘째 차례는 첫 담당을 건너뜀, 새 스레드는 처음부터.

### 5-3. 라우터 — `Send`로 함께 실행하고 리듀서로 모으기
- `Send(node, arg, *, timeout=None)`(`types.py` 704~790행). 조건 함수가 `Send` 목록을 내놓거나(Ch 13 05), 노드가 `Command(goto=[Send…])`를 내놓아도 같음(e5 `Command(goto=[Send]) -> … ['policy', 'shipping']`).
- **같은 단계의 `Send` 작업은 `invoke`(동기)에서도 스레드로 함께 실행**(`pregel/_runner.py` 135행 `PregelRunner`·`_executor.py` 40행 `BackgroundExecutor`, 설정 `max_concurrency`로 줄일 수 있음 — `_executor.py` 135행). e1: 0.5초·0.2초 노드 두 갈래 → 0.51초(세 번).
- **리듀서 칸에 모인 차례 = `Send` 목록 차례**(`_algo.py` 253~256행, e1 세 번 같음) ↔ **모드 `updates` 사건 차례 = 끝난 차례**(e1 `shipping`이 먼저). 리듀서 없는 칸 → `InvalidUpdateError`(「At key 'answers': Can receive only one value per step」).
- 빈 `Send` 목록 → 뒤 노드가 실행되지 않고 조용히 끝남(e5). 같은 분야 둘 → 둘 다 실행.
- 라우터 한 갈래는 `Command(goto=active_agent)`(문서).

### 5-4. 종료 조건 — 실행 한도·호출 한도
- `{"recursion_limit": N}` 넘으면 `GraphRecursionError`(`langgraph/errors.py` 67행, 「Recursion limit of N reached without hitting a stop condition」). 두 담당이 서로 `Command(goto=)`로 넘기는 모델 없는 그래프(e4)에서 한도 4 → 사건 넷(`desk_a·desk_b·desk_a·desk_b`) 뒤 오류, 한도 5·10도 오류(끝나지 않는 그래프). 한도 계산은 `pregel/_loop.py` 1701행 `stop = step + recursion_limit + 1`(Ch 20 03 「노드 K번 흐름은 한도 K+1부터 통과」와 같음).
- `ModelCallLimitMiddleware(*, thread_limit=None, run_limit=None, exit_behavior='end')`·`ToolCallLimitMiddleware(*, tool_name=None, thread_limit=None, run_limit=None, exit_behavior='continue')`(e4 서명) — Ch 22 04가 `run_limit=1, exit_behavior="end"`로 가르침. 도구 이름마다 호출 한도(`tool_name=`)는 과정에서 안 씀.
- `max_iterations`류 인자는 설치판 `create_agent`에 없음(옛 `AgentExecutor` 말).

### 5-5. 모델 객체(가짜 키, 요청 0)
- `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` → `temperature 0.0`·`reasoning_effort 'none'`·`stream_usage True`·`model_name gpt-5.4-mini`(e4). ChatOpenAI 설명(`chat_models/base.py` 3094~3096행): `parallel_tool_calls`는 `model.bind(parallel_tool_calls=False)`나 만들 때 `model_kwargs`로 줄 수 있음 — `create_agent`는 도구를 묶을 때 `request.model_settings`를 넘김(`factory.py` 1396~1402행) → 미들웨어로 끌 수 있으나 **실행하지 않음**(도구 없는 전문 에이전트에 이 값을 보내면 서비스가 받는지도 확인 안 함).

## 6. 모델을 부를지와 04 비교의 흔들림 처리 (결정하지 않음 — 장단점만)

### 6-1. 모델
- **위임의 핵심 관찰 가운데 모델이 있어야 보이는 것**: 01 중앙 에이전트가 전문 에이전트 도구를 **고르는** 장면 · 02 담당 에이전트가 넘기기 도구를 **골라** 다음 차례의 담당이 바뀌는 장면(문서 모양) · 03 분류 모델이 분야를 **고르는** 장면 · 04 구조마다 실제로 생긴 요청·토큰. 규격 §3은 기본 경로에서 가짜 모델을 금지 → 이 장면들은 실제 모델 없이는 못 보임.
- **모델 없이 결정적으로 보일 수 있는 것**(§5, e1~e5): `Command(goto=, update=)`로 담당 바꾸기와 체크포인터로 다음 차례 이어 가기 · `graph=Command.PARENT`로 바깥 그래프 노드로 넘기기 · 도구가 내놓는 `Command`의 `ToolMessage` 검사 오류(손으로 만든 `AIMessage(tool_calls=…)` — Ch 20 01 선례) · `Send` 팬아웃이 같은 단계에서 함께 돌고 리듀서로 모임 · 빈 분류면 조용히 끝남 · `goto` 이름 오타가 조용히 끝남 · `recursion_limit` 초과 `GraphRecursionError`(Ch 20 03 선례) · 안쪽 그래프 메시지가 바깥에 안 섞임.

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **M1 모델 없음** | 네 절 모두 노드·도구가 정한 값 | 결정적 · 키 셀·비용 0 · 흔들림 0 | 「모델이 골라 맡긴다」는 챕터 목표를 못 보임 · 01은 Ch 25 04 b8 「전문 에이전트를 도구로 감싸」·Ch 8 03 「서브에이전트가 따로 받은 컨텍스트」가 에이전트 없이 약해짐 · 04 비용 비교 불가 |
| **M2 절마다 다르게** | 01·04 실제 모델 · 02·03은 **앞 절반 모델 없음**(`Command`·`Send` 구조 — 결정적) + **뒤 절반 실제 모델**(02 넘기기 도구 / 03 분류 모델) | 구조는 흔들림 0으로, 모델 판단은 실제로 · 02·03 앞 절반은 묶음 실행 검사 후보 모양 · Ch 25 M2와 같은 틀 | 한 노트북에 두 조건(키 셀 위치·「앞 절반은 요청 0」 설명) · 셀 수 늘어남(§2-7 「코드를 늘려 가면서 개선할 필요는 없다」) |
| **M2′ 02만 모델 없음** | 02를 지금처럼 모델 없는 담당 넘기기(글자 규칙 대신 `Command`)로, 01·03·04 실제 모델 | 02 결정적 · 요청 적음 | 02에 「모델이 넘긴다」가 없어 공식 핸드오프(넘기기 도구 + `ToolMessage` + `graph=Command.PARENT`)를 04에서 처음 보임 → 04가 무거워짐 |
| **M3 모든 절 실제 모델** | 02도 넘기기 도구, 03 `Send` 부분도 모델 | 네 절 모두 문서 모양 | 흔들림이 가장 큼(담당 넘기기 여부·분류) · 요청 가장 많음 |

- 모델 설정은 과정 표준(`nbkit.key_and_model_cells()` — `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`). 지금 01·03·04의 `temperature` 없음·f-string 모델 이름·별표 풀기 키 찾기는 표준 셀로 바꿀 자리.
- 에이전트 답 글이 길면(옛 01 답은 제목·목록·「원하시면 …」까지) 토큰·비용이 흔들림 → 시스템 메시지 글에 「두 문장」처럼 길이를 정하는 것이 흔들림을 줄임(값은 여전히 흔들림).

### 6-2. 흔들리는 값과 04 비교
- **흔들리는 값**(서비스 모델): 중앙 에이전트가 도구를 부른 횟수(0·1·2 — 한 응답에 둘도 가능) · 넘기기 도구를 부를지 · 분류가 고른 분야 목록 · 답 글 · 입력 토큰(도구 결과 글 길이에 따라)·출력 토큰·예상 비용.
- **구조가 정하는 값**(흔들리지 않음 — 모델 판단이 정해지면 코드로 정해짐): 요청 수 셈 공식 — 서브에이전트 「중앙 = 도구 요청 응답 수 + 1(마지막 답) · 전문 = 부른 횟수 × 전문 안 요청 수(도구 없으면 1)」 → 한 번 맡기면 **2 + 1 = 3** · 핸드오프 「넘긴 차례 = 첫 담당 1(넘기기 요청) + 받은 담당 1(답) = 2, 다음 차례 = 받은 담당 1」 · 라우터 「분류 1 + 고른 분야 수 N (+ 종합 1)」 → 두 분야면 **3 또는 4** · 리듀서 칸 줄 수 = 고른 분야 수 · 종료가 완료 조건 때문인지 한도 때문인지(한도 장면을 실제 조건으로 만들면 결정적 — Ch 22 04 `run_limit=1`은 「모델 호출 횟수 1」이 결정적이었음).
- **규격 §2-7 9번 끝**: 결론·그림 라벨·캡션·정리·복습에는 두 번(새 커널) 모두 같았던 값과 구조가 정하는 값만. 실제 요청 수·토큰·비용은 결과 읽기 둘째 단락·본문 표(「교재 출력」 표시)·「확인할 점」·b7에만 「이번 실행에서는」. **본문 해석·결론에서 그 값으로 구조 순위를 매기지 않음**(Ch 6·12 「비용·시간 순위」 금지 태도).
- **규격 §2-7 10번 끝**: 결론에 쓸 모델 판단(「중앙 에이전트가 전문 도구를 한 번 부름」·「담당이 넘기기 도구를 부름」·「분류가 두 분야를 고름」)은 **입력을 확정하기 전에 노트북 밖에서 같은 요청 5번**으로 확인하고 `NN-probe.md` §0에 판단 규칙·그림 라벨 규칙을 먼저 적음(Ch 21·25 선례). 원래 관찰이 5/5가 아니면: 입력을 고치기 전에 흔들림 확인 → 원래 관찰이 다시 나오면 입력 그대로 + b7 「같은 요청도 실행한 때에 따라 … 달라질 수 있다」 + 다른 결과는 사실대로 + 「…이면 …이 됩니다」 셈 한 문장.

| 04 처리 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **R1 구조 공식 결론 + 실제 값 둘째 단락** | 세 구조를 **같은 과제**로(01~03에서 만든 부품 그대로) 한 번씩 실행 → 결론 = 「구조가 정하는 요청 수 공식과 이번 판단에서의 값(3·2(또는 3)·4)」·종료 까닭 · 표에 실제 토큰·예상 비용(「교재 출력」) | §2-7 9번 끝과 맞음 · 공식 문서 요청 수 표와 대조 가능(「Subagents adds one extra call」) · 요청 최소(구조당 1번) | 「어느 구조가 싸다」는 결론을 못 냄(원래 절 제목의 기대와 다름 — 강사 확인) |
| **R2 R1 + 같은 과제를 구조마다 N번(예 3번)** | 셀 안 `for`로 되풀이, 요청 수·토큰의 범위 | 흔들림 자체를 보여 줌 | 요청 ×N · 범위도 두 커널에서 흔들림(그림·결론 불가) · 셀·함수 늘어남 |
| **R3 두 차례 대화(되풀이 요청)까지** | 문서의 「Repeat request」처럼 둘째 차례를 더해 핸드오프가 첫 담당을 건너뛰는 구조 차이(체크포인터)를 보임 | 핸드오프의 장점(다음 차례 요청 1)이 구조로 드러남 · 02와 이어짐 | 요청 늘어남 · 서브에이전트·라우터 둘째 차례 모양을 정해야 함 |
| **R4 모델 없는 구조 비교만** | 세 구조를 모델 없는 노드로, 요청 수 = 노드 수 | 완전 결정적 | 「호출 수·비용」 절이 실제 요청 0 — 비용 비교 불가, 규격 §3 「실제 모델」 취지와 어긋남 |

- **종료 조건 장면(결정적 후보)**: ① 모델 없는 두 담당 핑퐁 그래프 + `{"recursion_limit": 4}` → `GraphRecursionError`, 사건 넷(e4 — Ch 20 03 선례, 키 셀 없이) ② 중앙 에이전트에 `ModelCallLimitMiddleware(run_limit=1, exit_behavior="end")` → 도구를 부르려면 요청 2번이 필요해 1번에서 끝남(Ch 22 04 선례, 요청 1) ③ 완료 조건 함수(필요한 결과 칸이 모두 찼는가 — 모델 글이 아닌 칸 있음·줄 수) ④ 빈 분류 → 종합 없이 끝남(e5, 모델 없음) → 「한도로 끝남 ≠ 일이 끝남」을 실제 조건으로.
- **서비스 요청 어림**은 §10-11.

## 7. §2-7 판단 근거 — 도구 파일

### 사실
- 지금 네 노트북은 서로 함수를 다시 쓰지 않음(01 `policy_specialist` · 02 `dispatch`·`respond` · 03 `run_specialist` · 04 `record_usage`·`measured_call`·`policy_tool`·노드 셋). 04가 01~03을 **다른 코드로 다시 만듦**(같은 이름 없음).
- 개선하면 절 사이에 되풀이될 자리: 메시지 목록 출력(Ch 19 06 `show_messages` — 01·02·04·05) · 요청 수·토큰 합(Ch 19 05 `sum_usage` — 01·04·05, **도구 안 전문 에이전트 결과에도 부름**) · 예상 비용(Ch 6 06 `estimate_cost` — 04·05, 01이 비용을 보이면 01부터) · 도구 요청 이름(Ch 19 04 `tool_call_names` — `show_messages` 안) · 호출 ID 짝(Ch 20 01 `call_id_lists` — 02 넘기기 도구의 `ToolMessage` 짝을 보이면) · 이 챕터 새 함수(01 전문 에이전트 요청을 기록 목록에 모으는 함수 · 04 구조마다 한 줄 기록 · 완료 조건 판정).
- 노드·넘기기 도구·전문 에이전트 도구는 노트북 전역 `model`·에이전트 객체를 읽음 → 도구 파일에 두려면 인자로 받아야 함(Ch 25는 노드를 노트북에 두고 03·04가 다시 적음 — 02 셀과 글자 같음, 생성기 대조).
- **앞 챕터 도구 파일은 파일째 못 가져옴**: Ch 21 `runner_tools.py`(맨 위 `import numpy as np` — Ch 26 잠금에 없음) · Ch 25 `stream_tools.py`(`time`만 — 가져올 수는 있으나 계약·해시가 Ch 25 폴더에 묶임, Ch 25 요약 §13-4 「파일째 가져오지 말 것」) · Ch 23 `checkpoint_tools.py`(SQLite). 규격 §2-7 3번대로 쓸 함수만 **같은 본문으로 옮기고 `# Ch N MM절에서 배웠습니다`**.
- 과정의 도구 파일 이름(`find labs -name '*_tools.py'` + `guardrails.py`): `git_tools`(Ch 3)·`data_tools`(Ch 4, 실습 폴더 맨 위)·`llm_tools`(Ch 5·7·8)·`rag_tools`(Ch 9~15)·`guardrails`(Ch 16)·`agent_tools`(Ch 17)·`workflow_tools`(Ch 18)·`order_tools`(Ch 19)·`graph_tools`(Ch 20)·`runner_tools`(Ch 21)·`checkpoint_tools`(Ch 23)·`approval_tools`(Ch 24)·`stream_tools`(Ch 25). **안 겹치는 후보**: **`delegation_tools.py`**(챕터 폴더 이름과 같은 말, `labs/` 전체에 0) · `team_tools.py` · `desk_tools.py`(창구 소재를 쓰면).
- 교훈(Ch 24 A-10·Ch 25 02~04): 앞 절 생성기가 뒤 절이 함수를 더한 도구 파일을 덮어쓰지 않게 **첫 판부터** `strip_later_imports`·판마다 해시 대조·쓰기 가드.

### 선택지 (결정하지 않음 — 장단점만)

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| A. 도구 파일 없음(Ch 2·4·6·22 선례) | 절마다 노트북에 | 목록·zip 변경 없음 | 01·04·05가 `show_messages`·`sum_usage`·`estimate_cost`(Ch 19·6 함수)를 다시 적으면 §2-7 3번과 충돌 |
| B. `delegation_tools.py`에 앞 챕터 함수만 | `tool_call_names`·`show_messages`·`sum_usage`(Ch 19)·`estimate_cost`(Ch 6)(+ `call_id_lists` Ch 20) — Ch 21 `runner_tools.py` 판과 글자 같은 본문, import 0 | §2-7 3번을 지킴 · 01부터 가져옴(첫 가져오기 고정 세 문장) · numpy 없음 | 함수 넷~다섯짜리 파일 — 절마다 쓰는 것이 달라 「이 절이 쓰는 함수는 …」 한정 문장 필요(Ch 21 01 A-1 선례) |
| C. B + 이 챕터 도움 함수 | 01 전문 에이전트 요청 기록(인자로 결과 메시지·기록 목록) · 04 구조 한 줄 기록·완료 조건 판정 · (03 분야 목록 → `Send` 목록 — 모델을 안 읽으므로 옮길 수 있음) | 04·05 실습 절 코드가 가장 짧음 | 처음 가르친 절은 노트북에 남겨 판이 둘 · 생성기 대조 사슬이 길어짐 · 함수 본문 10줄(L2) 넘기 쉬운 기록 함수 |

## 8. 과정 규칙과 부딪히는 것 (선택지와 장단점만)

### 8-1. 모델과 규격 §3 — §6 표.

### 8-2. 용어
- **세 구조 이름**: 「서브에이전트」·「핸드오프」·「라우터」(본문 3·3·2회, 영어 「Subagent」·「Handoff」·「Router」 제목·본문 11·10·16회). (가) 한국어 음차를 새 용어로 한 번 정의(뜻 → 일상 예 → 코드 모습)하고 이어 씀 — **Ch 27(대기)이 「서브에이전트」·「위임 도구」를 그대로 씀**(이름이 이어짐), 「라우팅」은 Ch 18 02 말이라 「라우터 = 라우팅을 하는 쪽」으로 이음 / (나) 풀어 쓴 말(「일을 맡는 에이전트」·「담당 넘기기」·「분류해 보내는 쪽」) — 일상어지만 Ch 27·공식 문서와 이름이 갈리고 새 말이 늘어남. 「핸드오프」는 Ch 24 금지어 「재개」·「중단」과 달리 금지 목록에 없음.
- **「문맥」(Part 3 금지어)·「문맥 격리」** → Ch 8 03 **「나누기(Isolate)」**(Ch 8 요약 137행이 Ch 26에 넘긴 약속) / Ch 22 08(시범 챕터) **「컨텍스트 분리(Isolate)」** — 두 이름이 과정 안에 이미 갈려 있음. (가) Ch 8 말 「나누기」 — 과정 요약 §5 Ch6~8 용어, 체크리스트 36행과 맞음 / (나) Ch 22 말 — 바로 앞 Part 6 챕터 말이지만 Ch 8 약속과 다름. 어느 쪽이든 01 b3에서 다른 쪽 이름을 한 문장으로 가름.
- **「병렬」(Ch 13·18 금지어)** → Ch 18 03 **「함께 보내기(parallelization)」** 또는 Ch 13 05 **「팬아웃」**. 03 제목 「병렬 실행」은 Ch 18 03 「병렬 섹셔닝」처럼 제목에만 두고 본문에서 한 번 풀기(강사 확인).
- **「종료 조건」 ↔ Ch 17 03 「정지 조건」**(정지 조건 넷 = 모델의 끝 선택·사람 확인·같은 도구 다시 고름·바퀴 한도): 같은 뜻이면 Ch 17 말을 이어 쓰고, 04가 새로 보이는 「완료 조건(필요한 결과가 다 모였는가)」을 정지 조건과 가름. **한도 말**: 「실행 한도」 = Ch 20 03 그래프 단계 수(`recursion_limit`) · 「호출 한도」 = Ch 16 04·Ch 22 04 모델 요청 수 상한(`ModelCallLimitMiddleware`) · 「바퀴 한도」 = Ch 17 루프 바퀴 수 — 04 b4 「최대 세 번 호출 같은 실행 한도」는 호출 한도.
- 「제어권」(01·02·03·04 합 10회) — 새 말. (가) 「다음에 누가 답하는가」·「담당」으로 풀기 / (나) 새 용어로 정의. 「맥락」(합 5, `objectives` 「맥락 소유자」)도 같은 처리.
- 그 밖 금지어 → 대체어: 반환 → 내놓다 · 스키마 → 양식(Ch 21)·입력 형식(Ch 19) · 필드 → 칸 · 런타임 → 실행 객체 표시(`ToolRuntime`, Ch 21 03) · 검증 → 검사 · 측정·계측 → 재기·세기 · 추정 비용 → 예상 비용 · 지연 → 걸린 초 · 경로 → 갈래·차례 · 영속 → 상태 저장(Ch 23) · 재시작 → 다시 실행(Ch 23 06 제목 말고) · docstring → 독스트링(Ch 19) · supervisor → 중앙 에이전트(코드 이름은 그대로) · 명시 → 적어 둔 · 최대·비상 경계 → 뺌 · 동적 → 입력을 보고 정하는(Ch 18 04 풀이) · fan-out → 팬아웃(Ch 13 05).
- `Command` 세 쓰임을 한 문장으로 가를 자리: Ch 13 06 `Command(update=, goto=)` · Ch 24 `Command(resume=…)` · Ch 26 `Command(…, graph=Command.PARENT)`(바깥 그래프로).

### 8-3. 제목·슬러그
- 챕터 제목 「위임 구조 — Subagents · Handoffs · Router」·절 제목의 영어 셋. **01 슬러그 `01-Subagent-도구-위임`은 Ch 25 04 b8 링크로 고정**(제목 글만 바꾸면 슬러그와 제목이 달라짐 — Ch 25 01 선례 「슬러그 고정·제목 말 강사 확인」). 02·03·04 슬러그는 Part 6 목차만 링크(다시 만들어짐)·옛 기록 파일(`prose-repetition-initial.json` 등)만 적음 → 바꿀 수 있음(강사 확인). 제목 말은 선례대로 「제목에만 남음(강사 확인)」 + 본문 첫 자리 풀이가 가장 작은 변경.

### 8-4. Ch 13 05 「결과가 모이는 차례는 우리가 정하지 않습니다」와 설치판 사실
- 설치판은 같은 단계 작업의 갱신을 작업 자리(path) 차례로 적용(`_algo.py` 253~256행) → 리듀서 칸 차례 = `Send` 목록 차례(e1 세 번). (가) Ch 13 05 가르침 그대로 — 결과마다 분야 이름을 함께 담아 차례에 기대지 않음(가장 안전, 새 사실 0) / (나) 「설치판은 `Send` 차례대로 모읍니다(소스 확인)」를 b7에 — 사실이지만 Ch 13 05(완료)의 조심스러운 말과 어긋나 보임 / (다) 모드 `updates` 사건 차례(끝난 차례)만 흔들리는 값으로 보이고 리듀서 차례는 말하지 않음.

### 8-5. 문법·셀 모양
- 함수 힌트 빼기(Ch 13·20·23·24·25) — 단 `@tool` 함수 매개변수 `: str`은 Ch 19 01 선례로 허용, 반환 힌트 `-> str`은 Ch 19 「반환 힌트 0」 · 변수 힌트(`calls: list[str]`) 빼기 · 상태 형식 이름을 칸 구성마다(`State` → 예 `DeskState`) · f-string·별표 풀기·이중 내포식·`getattr`·`dict(zip(…))`·`set` 비교·`setdefault`·`+=`·`1_000_000`·식 안 요금 없이 · 15줄 넘는 셀 셋 나누기 · 셀당 함수 하나 · 노드가 노트북 전역 기록 목록에 붙이기(04 c10)는 칸으로.
- 새로 쓰게 될 이름(쓰면 첫 자리 풀이): `Command.PARENT`·`graph=` · `ToolRuntime`의 `tool_call_id`·`state`(Ch 21 03은 `context`만) · `ToolMessage(content=…, tool_call_id=…)` 직접 만들기(Ch 19 05는 도구가 만든 것을 읽음) · `AgentState` 확장 칸(Ch 21 03 선례, `upgrade_allow`) · 문서의 `NotRequired`(과정 0건 — 입력에 빈 글을 넣어 피할 수 있음) · `include_raw=True`·`parsing_error`(과정 요약 2-2 「처음 쓰면 풀기」) · `ModelCallLimitMiddleware`(Ch 22 04 이름 그대로) · `concurrent.futures`는 `Send`로 바꾸면 불필요.
- `assert`: 모델 글 속 단어(01 c6)는 빼기(규격 §3) · 모델 판단(도구 이름·분류)은 흔들리는 값 → `assert` 대신 출력·probe로(Ch 21·25 선례 — 키 셀·구조 값에만).

### 8-6. 걸린 시간(03)
- 지금 03은 재지 않은 시간을 단정. (가) 재지 않고 구조만 — `Send` 두 작업이 같은 단계라는 것은 모드 `tasks`·`updates` 사건(Ch 25 말)이나 체크포인트 단계 번호로 결정적으로 보임 + 「걸린 시간은 이번에 재지 않았습니다」(Ch 12 A 07-1) / (나) Ch 18 03처럼 `time.perf_counter`로 재기 — 03이 「시간이 주제인 절」 예외에 드는지 먼저 정해야 함(제목은 「병렬 실행」 — Ch 18 03은 주제 절로 인정, 초·도착 차례 비교는 결론·그림·정리에서 뺌) / (다) 모델 없는 `time.sleep` 노드로 함께 도는 것을 보임(e1 모양) — 가짜 모델은 아니지만 「실제 처리를 미리 계산한 값으로 바꾸지 않는다」(§2-6) 취지와 부딪힐 수 있음.

### 8-7. 01 「전체 기록」 손 글
- `"내부 기록 " * 100`(639자)은 실제 기록이 아닌 글. (가) 빼고 안쪽·바깥 메시지 목록 모양으로 나누기를 보임 / (나) 남기되 「흐름을 보여 주려고 만든 글」임을 본문 주의 메모에(규격 §3 기준 값 밝히기) — 결론에는 안 씀.

### 8-8. 참고 자료 b10
- 네 절이 같은 다섯 → 절마다: 01 Subagents 문서 · 02 Handoffs 문서 · 03 Router 문서(+ Ch 13 05·Ch 18 02·03 링크) · 04 multi-agent 개요(요청 수 표)·langgraph-supervisor README. 확인일 새로(이 조사 2026-09-28).

### 8-9. 실습 절 요청 수
- 위임 구조 한 번 실행에 요청이 여럿(서브에이전트 3 · 라우터 3~4) → 실습 절 실행 1·실행 2만으로 6~8번 → 규격 §7-2 「3~5번을 넘으면 까닭을 진단에 적고 강사 확인」 대상이 될 가능성이 큼(Ch 14 10절 선례). 줄이려면 실습 절을 핸드오프 한 구조(차례당 1~2번)로 잡거나, 서브에이전트 한 번 + 값 하나 바꾼 한 번.

## 9. 삽화 비유 계열 후보

**이미 쓴 계열**(`figures/*.prompt.md` 이름 대조): Ch 13 작업대·갈림길 나무 길 · Ch 14 나무판·마개 · Ch 15 사과·저울·바구니·모래시계 · Ch 16 쪽지·도장·개찰구·체 · Ch 17 눈 위 발자국 · **Ch 18 도자기 가마·물레(작업 나눠 맡기기 = 큰 덩이를 나눠 빚은 그릇)** · **Ch 19 식당 메뉴판·주문 전표·집게** · **Ch 20 자료실 승강 상자(쪽지를 싣고 오가는 상자)** · **Ch 21 세탁기** · Ch 22 공항 검사·우편 가림막·전화 연결·개찰구·방문자 명부·두 겹 봉투·서류함·안내 데스크 · **Ch 23 체스판·즉석사진** · **Ch 24 도미노 줄·비워 둔 자리** · **Ch 25 대나무 홈통·물방울** · 그 밖 Ch 1~12 상자·쟁반·카드·우편함·구슬·택배 상자·서랍·사물함. 선례: 사람·손·동물·화면·글자·숫자·시계·화살표 없음(Ch 22만 사람이 나옴).

| 후보 | 그림 요소(절별) | 장점 | 겹침·위험 |
|---|---|---|---|
| **A. 항구의 예인선과 바지선** | 01 큰 배(중앙)가 작은 보트(전문)를 내려 부두에서 상자 하나만 싣고 돌아오게 함 — 큰 배는 제자리 · 02 바지선을 끌던 밧줄이 다음 예인선에 걸려 있음(끄는 배가 바뀜 = 다음 차례의 담당) · 03 분류 부두에서 짐배 세 척이 세 물길로 한꺼번에 떠나고 끝의 모음 부두에 짐이 모임 · 04 세 장면을 한 항구에 나란히 · 05 실습 장면 | 「맡기고 돌려받기 / 밧줄이 넘어감 / 나눠 한꺼번에 보냄」이 사람 없이 읽힘 · 배 계열 0건 | 물 장면이 Ch 25 홈통(물)과 색감이 겹칠 수 있음 · 밧줄이 어느 배에 걸렸는지 판독이 어려울 수 있음(「clearly tied to」 같은 보이는 모양으로) · 물길 셋이 Ch 13 「세 갈래 길」과 비슷해 보일 위험 |
| **B. 공사장 크레인과 갈고리** | 01 큰 크레인이 옆 작은 크레인에게 벽돌 한 판을 올려 달라고 맡기고 받은 판을 쌓음 · 02 짐이 한 크레인 갈고리에서 옆 크레인 갈고리로 옮겨 걸림(누가 들고 있는가) · 03 분류대의 벽돌 세 무더기가 트럭 세 대에 한꺼번에 실림 | 「누가 짐을 들고 있는가」가 갈고리로 분명 · 0건 계열 | 공사장 소품이 많아 관계와 무관한 색 요소(안전 표지·화면)가 끼기 쉬움(프롬프트에 「no signs」) · 01 「맡기고 돌려받기」가 약하게 읽힐 수 있음 |
| **C. 이어달리기 바통과 받침대(사람 없이)** | 02 두 받침대 사이 선에서 바통이 뒤 받침대에 놓여 있고 앞 받침대는 빔 · 03 출발선에 바통 셋이 세 레인 받침대에 동시에 · 01 트랙 가운데 중앙 받침대 옆 작은 바구니가 옆 레인에 다녀옴 | 「바통 = 다음에 누가 달리나」가 핸드오프와 가장 가까움(「바통 넘기기」는 과제 설명의 말) | 사람 없이는 움직임이 안 읽힘(화살표·움직임 선 금지 선례) · 01·04 장면이 억지 · 「바통」이 지휘봉으로 그려질 위험 |
| **D. 공기 수송관(기송관)과 캡슐** | 01 캡슐이 관으로 전문 창구에 갔다가 같은 관으로 되돌아옴 · 02 캡슐이 다음 창구로 넘어가 그 창구 표시등이 켜짐 · 03 분배판이 캡슐 셋을 세 관으로 한꺼번에 보내고 모음 통에 모임 | 기계 동작이 분명 | **Ch 20 「쪽지를 싣고 오가는 승강 상자」·Ch 25 「홈통」과 겹침이 큼** — 쓰면 그림 읽기에 비유 뜻 차이를 적어야 함 · 표시등 색이 뜻을 얻을 위험 |

- 스타일 문구는 규격 §5-4 그대로. 크레딧: 절마다 1장(01~05) 약 10크레딧, 재생성 1회씩이면 최대 20.

## 10. 위험과 깨진 것

1. **04 비교 설계** — 세 구조가 같은 일을 하지 않음(서브에이전트 도구 안은 모델 요청 하나, 핸드오프는 코드가 정한 차례, 라우터는 차례대로 요청 + 종합) → 「3·2·4회」는 코드에 적은 요청 수. 같은 과제·같은 부품으로 다시 짜면 출력·본문·복습 숫자가 모두 바뀜.
2. **02는 핸드오프가 아님** — 모델·`Command`·넘기기 도구 0, 글자 규칙 `if "환불" in text`. 03은 `Send` 0(스레드 풀).
3. **흔들림** — 도구 부른 횟수(한 응답에 둘도 가능, 도구 실행 노드는 함께 실행)·넘기기 여부·분류 목록·답 글·토큰·비용. 옛 01·04가 이 값에 `assert`. 01은 모델 글 속 단어에 `assert`(규격 §3 위반).
4. **요청 수 세기 누락** — 바깥 메시지 목록만 세면 전문 에이전트 요청이 빠짐(§2 01).
5. **`ToolMessage` 빠진 기록** — `graph=Command.PARENT`로 넘길 때는 도구 실행 노드가 `ToolMessage`를 검사하지 않음 → 넣지 않으면 바깥 기록이 「도구 요청 뒤 답 없음」 상태로 남고 다음 모델 요청에서 서비스 오류가 날 수 있음(문서 「malformed」, 실행하지 않음). 넘기기 도구 둘을 한 응답에 부르면 `goto`가 둘(문서는 그 경우를 전제하지 않음).
6. **조용히 끝나는 두 경우** — `goto` 이름 오타(경고만)·빈 분류(`Send` 0개 → 종합 없음). 오류로 드러나지 않아 절이 이를 보이지 않으면 학생이 놓침.
7. **실행 한도·무한 반복** — 두 담당이 서로 넘기면 끝나지 않음 → `GraphRecursionError`(그래프 기본 10007 · `create_agent` 9999라 기본값이면 한참 돈 뒤 멈춤 — 모델 그래프에서 무한 넘기기가 나면 요청이 수천 번 나갈 수 있음). 모델 절에는 작은 `recursion_limit`이나 `ModelCallLimitMiddleware`를 함께 두는 편이 안전(요금 사고 방지 — 규격 §3 누적 비용 1달러).
8. **용어** — 「문맥」(Part 3 금지어)·「병렬」·「지연」·「측정」·「추정」·「반환」·「스키마」·「필드」·「런타임」·「최대」·「비상 경계」 · 「실행 한도」 뜻 오용 · Isolate 이름 둘(Ch 8 나누기 ↔ Ch 22 컨텍스트 분리) · 제목 영어 셋.
9. **끊긴 가리킴** — 04 b8·`continuity-guide.md` 12행 「Ch39」(과정은 Ch 34까지).
10. **공용 옛 생성기** — `_generate_ch25_ch26.py`를 돌리면 Ch 26 노트북(출력 삭제)·`chapter.json`(`part_title` 옛 값)·`_src`(옛 검토 전 글)·`pyproject.toml`·README·목록을 덮어씀. 01절 작업 때 막기.
11. **서비스 요청 어림**(M2·R1·도구 파일 B 기준, 요금표 2026-09-17 mini 입력 0.75·캐시 입력 0.075·출력 4.50달러/100만 토큰, 요청당 입력 약 200~800·출력 약 60~300토큰 가정 — 청구 금액 아님):
    - 노트북 한 번: 01 **약 3~6**(기본 3 + 값 바꿔 보기 3) · 02 **0~5**(앞 절반 0 + 넘기기 두 차례 3 + 값 바꿔 보기) · 03 **약 4~7**(분류 1 + 전문 2 + 종합 1, 값 바꿔 보기 한 분야 3) · 04 **약 11~12**(3 + 3 + 4 + 호출 한도 장면 1) · 05 실습 **약 6~8** → **약 25~38번**.
    - 새 커널 두 번 → 약 50~76 · 노트북 밖 흔들림 확인 다섯 번(01 30 · 02 25 · 03 35 · 04 60 · 05 40) → 약 190.
    - **합계 약 240~270번**, 요청당 약 0.0005~0.002달러 → **약 0.15~0.5달러**(옛 01 답처럼 길면 위쪽). 절 하나 누적 1달러를 넘지 않음(04가 가장 많아 약 0.1달러). 임베딩 0. 삽화 약 10크레딧(최대 20).
12. **실행 시간**: e1~e6 모두 몇 초(모델 없음, e1은 잠드는 노드 0.5초 × 여러 번). 옛 노트북 셀 실행 기록으로 01 4.3초 · 02 0.6초 · 03 3.0초 · 04 17.7초 — 셸 180초 안에 여유(새 판은 요청이 늘어 더 걸림). 흔들림 확인 04(60번)는 호출 여러 번으로 나눠야 할 수 있음.
13. **파일 쓰기 자리** — 지금 0. 04·05가 기록을 파일로 쓰면 임시 폴더(`mkdtemp`, Ch 23·24 선례). SQLite 체크포인터는 연결 폴더에서 멈춤(Ch 23 발견) — 02는 `InMemorySaver`로 충분.
14. **뒤 챕터 계약** — 파일 계약 없음. 문장만: Ch 27 03·06 b3(완료 조건 — 부분 참) · Ch 25 04 b8(01 슬러그) · Ch 8 03(01 내용).

## 11. 01절 작업자가 먼저 결정해야 할 것

1. **모델을 부를지(§6-1)** — M1 / **M2(01·04 실제 모델, 02·03은 모델 없는 구조 + 실제 모델 판단)** / M2′ / M3. 모델 없는 부분을 두면 키 셀 자리와 「앞 절반 요청 0」 설명 · 묶음 실행 검사 후보 여부까지 함께.
2. **용어와 제목(§8-2·8-3)** — 서브에이전트·핸드오프·라우터를 음차 새 용어로 둘지(Ch 27과 이어짐) · Isolate 이름(Ch 8 「나누기」 ↔ Ch 22 「컨텍스트 분리」) · 「종료 조건」 ↔ Ch 17 「정지 조건」·한도 말 셋 · 「병렬」 → 「함께 보내기」/「팬아웃」 · 「제어권」·「맥락」 · 01 슬러그 고정(제목 글만 바꿀지) · 네 절 b3를 절마다 새로. `handoff.md`에 용어 표로 먼저.
3. **01 설계(§2 01)** — 전문 에이전트 하나/둘 · 나누기를 보이는 출력(안쪽 목록 ↔ 바깥 목록, 손으로 만든 「전체 기록」 뺄지) · **전문 에이전트 요청까지 세는 방법**(도구 안에서 결과 메시지로 기록 / 콜백) · 흔들림 확인 규칙을 `01-probe.md` §0에 먼저(도구 부른 횟수·답 길이) · `assert` 대상(키 셀·구조 값만).
4. **도구 파일(§7)** — A/B/C와 이름(`delegation_tools.py` 후보), 첫 판부터 생성기 대조 사슬(`strip_later_imports`·해시 대조·쓰기 가드) · **공용 옛 생성기 `_generate_ch25_ch26.py`와 Ch 26 `figures/_gen_figures.py` 첫머리 막기**(설명 주석 + `raise SystemExit(...)`, 챕터 밖 한 줄 — 진단에).
5. **소재와 04 비교 틀(§6-2·§2 04)** — 배송 지연·환불(지금 판, Ch 19 주문 소재와 가까움) ↔ Ch 20~25 도서관 자료실 소재 중 무엇을 01~05에 이어 쓸지 · 04를 **같은 과제·01~03 부품 그대로 + 구조가 정하는 요청 수 결론(R1)**으로 할지 · 종료 조건 장면(실행 한도·호출 한도·빈 분류) 어느 것을 실제 조건으로 보일지.

## 12. 챕터 마감으로 미룰 것

- **05 실습 절 신설**(규격 §7-2): 슬러그 후보 **`05-위임-구조-실습`**(챕터 제목의 한국어 머리말 — `_notebook/build_index.py`의 짧은 이름 「위임 구조」와 같음; 선례 `07-워크플로우-패턴-실습`·`06-Agent-개요-실습`·`04-Streaming-실습`·`07-create-agent-실습` — 모두 챕터 제목 말 그대로) · 다른 후보 `05-Delegation-실습`(폴더 이름 말)·`05-위임-실습`. 제목 「위임 구조 실습: …」, `format: experiment`, meta 「실습 30분 · 새 용어 0」(**챕터 시수 4·4h에 더하지 않음**). 새 문법·API 0, 요청 3~5번이 넘을 가능성(§8-9 — 강사 확인). 주제 예 — 01~04 소재를 이어 문의 창구 하나에 「라우터로 분야를 고르고 → 고른 전문 에이전트를 도구로 부르는」 조립 + 실행 2는 값 하나(예: 분류가 고를 수 있는 분야 목록에서 하나 빼기 · 호출 한도 1)만 바꿈.
- 공용 옛 생성기 `_generate_ch25_ch26.py` → `ch26-delegation/qa/upgrade/before/generators/blocked/`(`mv -n`, 해시 기록, Ch 25 요약 §13-7·체크리스트 §2-13에 한 줄) · Ch 26 `figures/_gen_figures.py` → 같은 자리(`mv -n`).
- 옛 그림 12개(`figures/0N-흐름.{svg,excalidraw,caption.md}`, N=1~4) 삭제 승인 목록(사본 `before/figures/`, `final-artifact-hashes.json`·`ch26-code-output-preservation.sha256`이 해시를 적은 기록 파일). 챕터 공개 목록에 옛 SVG 줄은 **원래 없음**.
- `chapter.json` `objectives`(「맥락 소유자」·「계측」·「추정 비용」) · 절 제목 · `textbook/part6/_build_index.py` 24행 설명 · `_notebook/build_index.py` 56~57행 설명(절 수 4 그대로 — 실습 절 빼고 세는 약속) · 챕터 목차를 개선 본문과 대조 → `_build.py`·`_build_index.py`.
- 실습 폴더 README 다시 쓰기(노트북 다섯, `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 절마다 요청 수·키 필요 여부, 「예상 비용」, 도구 파일 단락) · `labs/part6/continuity-guide.md` 12행(「Ch39」 → 없는 챕터 — 참이 되게) · `qa/research.md`·`verification.md`·`authoring-checklist.md`·`ch26-technical-review.md`·`집필점검표.md`·`research.md`(Ch 25 조사 섞임)에 「개선 전 판」 표시.
- Part 6 공개 목록에 05·(도구 파일) 줄 → `part6-practice.zip` 다시 만들기(마지막에 한 번) → `check_delivery.py`(`llm-practice.zip` Stale 예상) · 묶음을 풀어 05 경로 셀 확인 · 옛 검사 넷 돌려 기록(`check_notebook_readiness.py` 결과 파일 되돌림). 묶음 실행 검사에 모델 없는 절을 넣을지는 전체 마감 후보(강사 확인).
- **뒤 챕터 인계**(고치지 않음): Ch 27 01(참)·03·06 b3(완료 조건 — 부분 참) · `continuity-guide.md` 12행 · Part 6 소개·`practice-start.md`(참) · Ch 25 04 b8(01 슬러그·내용) · Ch 8 03(01 내용).
- 삭제 승인 대상: 실습 폴더 `.venv`(macOS 174MB) · `qa/upgrade/gates-wip-*.json` · `qa/upgrade/__pycache__`(생기면) · `.cache/vm/venv-ch26-delegation`(238MB) · 기기 `/tmp/ch26-prep`·`/tmp/uv-cache`(6.9MB — 이번에 새로 만듦, 공용).

## 13. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 4 · `notebooks` 4 · `figures` 13(SVG·excalidraw·caption 각 4 + `_gen_figures.py`) · `generators` 2(**공용 `_generate_ch25_ch26.py` 지금 판**·`_gen_figures.py`) · `qa` 7(`public-files.json`·`prerequisite-files.json`·`research.md`·`verification.md`·`authoring-checklist.md`·`ch26-technical-review.md`·`ch26-code-output-preservation.sha256`) · 실습 폴더 3(`pyproject.toml`·`uv.lock`·`README.md`) · `chapter.json`·`집필점검표.md`·`_build.py`·`index.html`·`research.md` = **38개, 464KB**. 원본과 `cmp` 모두 같음 |
| `qa/upgrade/gates-before.json` | §0 표(절별 G1~G7 · 합계 128, 통과 0/4), `6113c82e…` |
| `qa/upgrade/before-manifest.json` | sha256 **190개**(`ea09b677…`) — ① 이 챕터 실습 폴더 7·원고(`_src`·HTML·목차·`chapter.json`·`_build.py`·기록·그림·`qa/`) · 앞 챕터에서 가져오거나 이어 쓸 파일: Ch 25 도구 파일·04 노트북·잠금 둘 · Ch 24·23 도구 파일·Ch 23 01 · Ch 21 `runner_tools.py`·01·03·07·잠금 둘 · Ch 22 04·08·잠금 둘 · Ch 20 도구 파일·01·03 · Ch 19 도구 파일·05 · Ch 18 도구 파일·02·03·04·06 · Ch 17 도구 파일·03 · Ch 16·15·13 도구 파일 · Ch 13 05·06 · Ch 6 03·06 · Ch 8 03 노트북과 해당 `_src` ② Ch 26을 가리키는 완료 챕터 파일: Ch 8 03 `_src`·HTML·`index-body.html`·`index.html`·`집필점검표.md`·요약 · Ch 25 04 `_src`·HTML·`author_04.py`·요약·`handoff.md`·`research.md` · Ch 20·21·23 요약 ③ Ch 26에 기대는 뒤 챕터·Part·과정 파일: Ch 27 01·03·06 `_src`·HTML·`author_ch27.py`·06 노트북 · Ch 34 03 `_src` · 연속성 안내 둘 · Part 6 소개·목차·`practice-start.md` · 목차 스크립트 둘·`build_bundle.py`·`textbook/index.html` · 목록 셋 · zip 셋 · Part 6 `qa/` 기록 열넷·언어 기록·Part 7 기록 셋·검사 기록 ④ 옛 생성기와 부품(`_generate_ch25_ch26.py`·`_author_ch21_ch29.py`·`figures/_gen_figures.py`·`part5/_figure.py`·Ch 25 쪽 생성기 사본·`part6b_*.py` 둘) · 검사·빌드 스크립트 열다섯 |
| `qa/upgrade/chapter-lead-notes.md` | 이 파일 |
| `$ROOT/.cache/vm/venv-ch26-delegation` | Python 3.12.13 · 238MB |

### 가상환경 만든 방법과 결과
- Ch 25 준비와 같은 방법: `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy uv venv --python 3.12.13 …/venv-ch26-delegation` → `uv pip install --python …/bin/python pip==26.2` → 잠금 목록 `uv export --project labs/part6/ch26-delegation --frozen --no-hashes --all-groups --no-emit-project`(실습 폴더 파일 그대로 — 수정 시각 09-10 그대로), 주석 줄만 뺀 87줄(`/tmp/ch26-prep/req-clean.txt`, 환경 표시 `; sys_platform == …` 유지) → **`bin/python -m pip install --no-cache-dir -r`**. 설치 오류 0, **`uv cache prune` 안 함**. `/tmp/uv-cache`는 기기가 새로 만들어져 없어서 이번에 새로 만듦(6.9MB). 기기 루트 디스크 여유 **3.9G**(작업 전후 같음 — 가상환경은 사용자 디스크 `$ROOT/.cache/vm`, 여유 73G), `/sessions` 830M.
- 결과: `pip freeze --all`과 잠금 대조 **판 차이 0**(설치 82 = 잠금 87 − 이 기기에 해당하지 않는 다섯: `appnope`(darwin)·`colorama`(win32)·`cffi`·`pycparser`(PyPy)·`httpx2-jsfetch`(emscripten)) — Ch 25 가상환경과 같은 모양. `langchain 1.4.0`·`langchain-core 1.6.2`·`langchain-openai 1.6.0`·`langgraph 1.2.11`·`langgraph-checkpoint 4.2.0`·`langgraph-prebuilt 1.1.0`·`openai 3.11.0`·`python-dotenv 1.2.3`·`pydantic 2.13.5`·`ipykernel 7.3.0`·`nbclient 0.11.0`·`pip 26.2`. `pip check` 이상 없음. 커널 스펙 `share/jupyter/kernels/python3` 있음.
- import 확인만(`env -u OPENAI_API_KEY`, e6): `create_agent`·`init_chat_model`·`tool`·`ToolRuntime`·`ModelCallLimitMiddleware`·`ToolCallLimitMiddleware`·`wrap_model_call`·`AIMessage`·`ToolMessage`·`HumanMessage`·`get_usage_metadata_callback`·`StateGraph`·`START`·`END`·`MessagesState`·`Command`·`Send`·`GraphRecursionError`·`InvalidUpdateError`·`ParentCommand`·`InMemorySaver`·`ToolNode`·`ChatOpenAI`·`dotenv`·`ipykernel`·`nbclient`·`pip`. `numpy`·`pillow`·`langgraph-checkpoint-sqlite`·`langgraph-supervisor`·`langgraph-swarm`은 없음(잠금대로). 모델 객체는 가짜 키 글로 만들기만 확인(요청 0). 루트 `.env`에 `OPENAI_API_KEY` 이름 한 줄 있음(값은 보지 않음). `run_section.sh`는 `$ROOT/.cache/vm/venv-<챕터 폴더 이름>`을 자동으로 씁니다.

### 참고 자료 (2026-09-28 확인)
- LangChain Subagents `https://docs.langchain.com/oss/python/langchain/multi-agent/subagents` — `@tool("research", …)` 함수 안 `subagent.invoke({"messages": [{"role": "user", "content": query}]})` → `result["messages"][-1].content` · 「By default, subagents are stateless … all conversation memory maintained by the main agent」 · isolated ↔ forked(`runtime.state["messages"]`) · 동기 ↔ 비동기(세 도구) · 「The main agent can invoke multiple subagents in a single turn」 · 도구마다 에이전트 ↔ 도구 하나로 나눠 보내기 표.
- LangChain Handoffs `https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs` — 넘기기 도구 `transfer_to_sales(runtime: ToolRuntime) -> Command` · `Command(goto="sales_agent", update={"active_agent": …, "messages": [last_ai_message, transfer_message]}, graph=Command.PARENT)` · 「A `ToolMessage` must be included … without it, the conversation history becomes malformed」 · `MultiAgentState(AgentState)`·`active_agent: NotRequired[str]` · 한 에이전트 + 미들웨어 모양(`current_step`·`@wrap_model_call`·`Command(update={"messages": [ToolMessage(…)], …})`) · 「assumes only the handoff tool was called (no parallel tool calls)」.
- LangChain Router `https://docs.langchain.com/oss/python/langchain/multi-agent/router` — `route_query`가 `[Send(c["agent"], {"query": c["query"]}) for c in classifications]` · 한 갈래 `Command(goto=active_agent)` · 리듀서 `Annotated[list, operator.add]` · 여러 차례 대화는 라우터를 도구로 감싸 대화 에이전트가 기록을 맡음. 요청 수·비용 설명 없음.
- LangChain Multi-agent 개요 `https://docs.langchain.com/oss/python/langchain/multi-agent` — 다섯 모양(Subagents·Handoffs·Skills·Router·Custom workflow) · 「not every complex task requires this approach」 · **요청 수 표**(한 번 요청 4·3·3·3 / 되풀이 두 차례 8·5·5·6 / 여러 분야 5·7+·3·5와 토큰 ~9K·~14K+·~15K·~9K) · 「Subagents adds one extra call because results flow back through the main agent」. 쪽에 판·날짜 표시 없음.
- langgraph-supervisor README `https://github.com/langchain-ai/langgraph-supervisor-py` — 「We now recommend using the supervisor pattern directly via tools rather than this library for most use cases」 · 최신 0.0.31(2025-11-19).
- 설치판 소스(`langgraph 1.2.11`): `types.py` 704~790행(`Send`)·799~848행(`Command`·`PARENT`) · `prebuilt/tool_node.py` 821~823행(도구 요청 함께 실행)·862~915행(부모행 `Command` 합치기)·1455~1501행(목록 검사)·1503~1578행(`_validate_tool_command` — `ToolMessage` 검사, 1559~1562행 `graph is None`일 때만) · `pregel/_algo.py` 253~256행(작업 자리 차례로 갱신 적용)·312행(없는 노드로 가는 쓰기 무시 경고) · `pregel/_runner.py` 135행·`_executor.py` 40·135행(같은 단계 작업을 스레드로, `max_concurrency`) · `pregel/_loop.py` 1701행(`stop = step + recursion_limit + 1`) · `_internal/_config.py` 32행(`DEFAULT_RECURSION_LIMIT` 10007) · `errors.py` 67·90·129행(`GraphRecursionError`·`InvalidUpdateError`·`ParentCommand`). (`langchain 1.4.0`) `agents/factory.py` 772~789행(`create_agent` 인자)·1396~1402행(`model_settings`를 도구 묶기에 넘김)·1831~1834·1857행(`recursion_limit` 9999·`lc_agent_name`) · `agents/_subagent_transformer.py` 1~60·120행(이름 있는 에이전트를 서브에이전트로 드러냄). (`langchain-openai 1.6.0`) `chat_models/base.py` 3094~3096행(`parallel_tool_calls`는 `bind`나 `model_kwargs`로). (`langchain-core 1.6.2`) `callbacks/usage.py` 18·81행(`UsageMetadataCallbackHandler`·`get_usage_metadata_callback` — 모델 이름별 토큰 합, 요청 수는 안 셈).
- 모델 없는 확인 파일: `/tmp/ch26-prep/exp/e1_send.py`(팬아웃·리듀서·동시 실행·`InvalidUpdateError`) · `e2_command.py`(`Command` 담당 넘기기·체크포인터 다음 차례·없는 노드 이름) · `e3_parent.py`(`graph=Command.PARENT`·`ToolMessage` 검사·`ParentCommand`) · `e4_limits.py`(`GraphRecursionError`·`create_agent` 설정·`@tool` 모양·한도 미들웨어 서명) · `e5_misc.py`(도구 안 그래프 메시지 나누기·빈 분류·`Command(goto=[Send])`) · `e6_imports.py`(판·import).
- 앞 챕터: Ch 8 03 `_src` 6·33~36·39·83행 · Ch 13 05 `_src`(결과 차례와 자리 번호) · Ch 18 요약 16~22·53~58행 · Ch 20 요약 §13 「Ch 26 delegation」 · Ch 21 요약 §1·§6~8 · Ch 22 04·08 `_src` · Ch 25 요약 §13·§15 · Ch 25 04 `author_04.py` 533·612행.
