# 03절 진단과 개선 기록 — AgentState와 context_schema (experiment)

- 대상: `_src/03-AgentState와-context-schema.html` · `labs/part6/ch21-create-agent/notebooks/03-AgentState와-context-schema.ipynb` · 도구 파일 `notebooks/runner_tools.py`(함수 하나 더함) · 그림 `figures/03-1`~`03-5`.
- 생성기: `qa/upgrade/author_03.py`(노트북 + `_src`, `06965cff…`). 흔들림 확인: `qa/upgrade/03-probe.md`·`probe/probe03.py`·`probe/probe-{R0,R3}.jsonl`, 모델 없는 확인 `probe/check03_*.py`. 그림 설계표: `qa/upgrade/03-figures.md`. 검토 묶음: `qa/upgrade/review-pack/03-AgentState와-context-schema.md`.
- 작업일 2026-09-25(UTC 03:0x~03:4x). 형식 **experiment 유지**(`chapter.json`), 슬러그 그대로(02 b8·02 생성기 `L_03`이 링크).

## 1. 게이트 전후

| | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전 (`gates-before.json`) | 5 | 71 | 2 | 1 | 0 | 0 | 5 | 30 | 3 | **41** |
| 첫 실행 전 (`gates-wip-03-03.json`의 첫 판, 노트북만 쓴 판) | 24 | 346 | 0 | 0 | 0 | 0 | 0 | 1 | 6 | — |
| 후 (`gates-wip-03.json`) | **24** | **354** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G1·G2는 **0**(과제 지시대로 첫 실행 전에 먼저 검사). G6 1 = 복습 해설 한 곳의 괄호 뒤 마침표(`({}).`)가 두 문장을 한 문장으로 셈 → 문장을 고쳐 씀. G7 6 = 설계표·캡션 넷·삽화 prompt가 아직 없던 때의 값. 고친 뒤 같은 이름으로 다시 검사해 `gates-wip-03-03.json`은 지금 0 판입니다(첫 판 수치는 이 표와 기기 `/tmp/ch21-03/gates-wip-03-03.first.json`에만 남음).
- **클래스 게이트 허용 방법**: 상태 형식 확장 셀 하나(`class LibraryState(AgentState)`)에만 셀 메타데이터 **`upgrade_allow=["class_def"]`**(Ch 13 08절 `upgrade_allow=["multiple_defs_in_cell"]`와 같은 셀 메타데이터 허용 방법 — Ch 20은 허용 0, Ch 22 노트북은 지금 클래스 0). G1은 `SCHEMA_BASES = {"BaseModel", "TypedDict"}` 밖 상속을 `class_def`로 잡기 때문입니다. 실행 정보 형식 `class MemberContext(TypedDict)`는 칸만 적어 G1이 허용 모양으로 봄(허용 표시 없음). 두 클래스 모두 칸만 있고 메서드·기본값·데코레이터 0.
- AST 따로(`/tmp/ch21-03/extra_check.py` — 02 판에 **칸만 적은 `AgentState` 확장 클래스**와 **`@tool` 매개변수 `runtime: ToolRuntime[MemberContext]`** 허용을 더함, 허용한 두 곳은 `ALLOWED_03_…`으로 따로 출력): 노트북 **위반 0건**(허용 표시 2줄 — `cell19 LibraryState`·`cell23 ToolRuntime[MemberContext]`), 도구 파일 2건 = `estimate_cost`의 `.get` 둘(Ch 6 06 원본 예외, 01·02와 같음). 금지어(`/tmp/ch21-03/ban_check.py` — 02 판 + 「주입」·「의존」·「채널」·「컨텍스트」·「런타임」): 노트북·`_src`·캡션 다섯·`.mmd` 넷에서 **3건 = 「컨텍스트」 2(노트북·`_src` 각 한 번 — 「Ch 8 01절의 컨텍스트(모델이 받은 글 전체)와는 다른 값」, 과정 말을 가리키는 자리) · 「캐시 입력」 1(허용 말)**. 「한 겹 더」 0건. 「MessagesState」 0건.
- 코드 줄(`count_code.py`) 35 → **129**(셀 5 → 24), 도구 파일 코드 줄 50 → **57**. 준비 셀이 아닌 셀의 주석 뺀 코드 최대 **9줄**(`AGENT`), 함수 본문 최대 **5문**(`check_my_loan` — 독스트링 빼고), 셀당 정의 하나, 첫 줄 주석 100%. f-string·제네릭 없는 복합 힌트·기본값·`@dataclass` 0.

## 2. 수정 전 주요 문제 (준비 노트 §1·§2 03·§7-2·§7-3, 인계 §02 → §03)

1. **클래스 둘 + 도구 하나가 한 셀**: `from dataclasses import dataclass` · `class SupportState(AgentState)` · `@dataclass class UserContext` · `@tool current_access(runtime: ToolRuntime[UserContext]) -> str`(G1 `class_def` 2) — `@dataclass`(과정 0건)·위치 인자로 만들기 `UserContext("student-7", "read-only")`·반환 힌트·f-string 안 속성 계산.
2. **모델 이름 글자**: `create_agent("openai:gpt-5.4-mini", …)`(temperature·reasoning_effort 없음) · 한 줄 두 겹 호출(G2 `nested_call_2plus`)·`sorted(result.keys())`.
3. **모델 글에 건 `assert`**: `"read-only" in 답 글` · `"context" not in result`(원래 없는 키 — 증거로 약함).
4. **틀린 전제**: b3 「MessagesState와 TypedDict 상태를 사용합니다」(Ch 13·20은 `MessagesState`를 가르치지 않음) · b4 「상태 … 체크포인터가 저장할 수 있는 실행 데이터」(Ch 23 전제).
5. **이름 충돌**: Ch 20 01의 우리 상태 형식 `AgentState`와 라이브러리 `AgentState`를 가르는 문장 없음.
6. **금지어·말**: 「로그」 4 · 「식별자」 · 「주입」 3 · 「의존」 · 「채널」 · 「필드」 · 「스키마」 · 「지연」 · 「실행기」 · 「컨텍스트」를 모델에게 보내지 않는 값에 씀(과정의 「컨텍스트」는 Ch 8 01 뜻).
7. **틀 문장**: b3 「필요한 자료와 객체는 노트북에서 다시 선언하므로 …」 · b6 = 확인할 점 = b8 · b7 「절당 1달러 미만」·「모델 문장과 지연」 · b8 「04-0x에서-1x로-마이그레이션에서 이 결과를 다시 사용합니다」(04가 03 결과를 쓰지 않음) · 복습 해설 한 줄 · 결과 읽기 셀 0 · 옛 그림 `{{svg:03-흐름}}` 한 장 · 소재가 01·02 자료실과 끊김(`student-7`·`read-only`·`lesson-03` 지어낸 값).

## 3. 바꾼 것

- **소재를 01·02 자료실로 이음**: 01과 같은 모델 객체·`POLICY_DATA`·`DEF_TOOL`(생성기 `check_same_as_before()`가 01 생성기 상수와 문자열 대조). 새 도구 `check_my_loan(runtime: ToolRuntime[MemberContext])`는 실행 정보의 이용자 번호·연체 일수를 읽고, 연체가 있으면 01 자료의 연체 규정 글(`POLICIES["연체"]`)을 붙임. 시스템 메시지 글은 01 글과 **앞 문장이 같고** 뒤 문장만 이 도구에 맞게(대조). 에이전트에는 **도구 하나만**(모델이 도구를 부르는지를 한 가지로 보기 위해 — `lookup_policy`는 5절 명세 비교에만). 질문 「제가 지금 새 책을 빌릴 수 있나요?」, 상태 칸 `ticket_no`(문의 번호) `Q-017`, 실행 정보 `{"member_id": "M-0317", "overdue_days": 0}` — 모두 노트북 밖 확인 전에 정함(b7).
- **`AgentState` 확장(챕터 리드 결정)**: `class LibraryState(AgentState): ticket_no: str`(칸만, 게이트는 `upgrade_allow=["class_def"]`). 노트북 4절에 세 문장(뜻 → 창구 문의 번호 예 → 코드) + 「클래스 이름 뒤 괄호 = 그 틀의 칸 셋을 물려받음, Ch 6 03절 `BaseModel`과 같은 모양」 + Ch 13 02·04 잇기. **이름 충돌 한 문장**(「Ch 20 01절에서는 우리가 만든 상태 형식에 `AgentState`라는 이름을 붙였습니다. 이 절에서 가져온 `AgentState`는 이름만 같고, 라이브러리가 주는 다른 상태 형식입니다」 — 노트북 4절·`_src` b3).
- **Ch 22 이음새를 출력으로**: `AgentState is middleware.AgentState` → `두 자리의 AgentState가 같은 클래스인가: True`(Ch 22 노트북이 `from langchain.agents.middleware import AgentState`로 훅 표시에 씀).
- **상태 칸 비교를 결정적으로**: 두 형식을 넘기지 않은 그래프(같은 도구·시스템 메시지)와 넘긴 그래프의 `builder.channels` → `['messages', 'jump_to', 'structured_response']` ↔ `[…, 'ticket_no']`. 노드·조건 함수(`print_branches`)는 01과 같음. 실행 정보 칸은 상태 칸 목록에 없음(소스 `factory.py` 1174~1192행 — `StateGraph(state_schema=…, context_schema=…)`).
- **실행 정보는 `@dataclass` 대신 칸만 적은 `TypedDict`**(챕터 리드 결정): `class MemberContext(TypedDict)`, 도구 안에서 `runtime.context["member_id"]`(딕셔너리 꺼내기를 첫 자리 5절에서 풂), `invoke(first_state, context=first_context)`(딕셔너리). **말은 「실행 정보」**: 과정의 「컨텍스트」는 Ch 8 01 「모델이 이번 답을 만들 때 받은 글 전체」라, 모델 요청에 실리지 않는 이 값에 쓰면 뜻이 뒤집힘 → 「인자 이름은 context이지만 Ch 8 01절의 컨텍스트와 다른 값」 한 문장(노트북 5절·`_src` b4). 실행 정보가 모델 요청에 실리지 않는 것은 소스(`factory.py` 1450~1454행)로만, 도구가 만든 도구 메시지 글은 다음 요청에 실린다는 것도 함께 적음.
- **주입 확인을 첫 실행 전에 모델 없이**(03-probe.md §0-1): ① `create_agent`가 만든 `ToolNode`를 작은 그래프에 넣어 손으로 만든 요청 + `context` → 도구 메시지에 값이 들어감 ② **`create_agent` 흐름 전체**를 노트북 밖 확인용 대본 모델(`GenericFakeChatModel` + `bind_tools`만 더함)로 → 0일·3일 모두 도구 메시지에 값, 결과 키 `['messages', 'ticket_no']`. 두 확인 모두 가짜 키·키 뺌·요청 0. 대본 모델은 노트북에 쓰지 않음(규격 §3은 노트북 기본 경로 규칙).
- **`ToolRuntime` 표시(과정 처음)**: 「도구 매개변수에 표시 `ToolRuntime`을 붙이면, 라이브러리가 실행 정보를 담은 객체를 넣어 줍니다. 이 매개변수는 모델이 채우는 인자가 아니고 …」 + Ch 20 02 받을 오류 표시와 같은 성격 한 문장. **도구 명세에서 빠지는 것을 출력으로**(Ch 19 01 `args`·`convert_to_openai_tool` 모양): `lookup_policy | 입력 형식의 인자: ['topic'] | 명세의 인자: ['topic']` ↔ `check_my_loan | 입력 형식의 인자: [] | 명세의 인자: []` + 7절 `도구 이름: check_my_loan | 인자: {}`. 빼는 자리(`langchain_core/tools/base.py` 331~340행)·넣는 자리(`tool_node.py` 802~817행)는 소스로만.
- **제네릭 힌트 — 챕터 리드 결정의 예외(강사 확인 대상 1)**: 결정은 「`ToolRuntime[…]`은 빼기, 꼭 필요하면 까닭과 함께 진단·강사 확인」. 모델 없는 확인에서 **대괄호 없이 `ToolRuntime`만 적으면 컨텍스트 모양 셋(`TypedDict`·데이터 클래스·`BaseModel`) 모두 흐름 한 번에 Pydantic 직렬화 `UserWarning` 2건**(`field_name='context'`·`Expected none` — 라이브러리가 형식을 모를 때 `None`으로 봄), **대괄호로 적으면 셋 모두 0건**, 값이 들어가는 것·입력 형식 `{}`는 두 적기에서 같음(`probe/check03_warn_variants.py`). 대괄호 없이 가면 7·8절 두 셀에 Pydantic 내부 글 경고가 stderr로 찍혀 학생이 오류로 읽기 쉽고, 그 경고를 풀려면 결국 대괄호 뜻을 설명해야 함 → **`ToolRuntime[MemberContext]`로 적고** 노트북 5절에 「대괄호 안은 Ch 13 04 `list[AnyMessage]`처럼 안에 든 값의 형식」·「대괄호를 빼도 값은 들어가지만 이 판에서는 경고 두 줄 — 노트북 밖에서 모델 없이 확인, 이번 노트북에서 실행하지 않음」. 공식 문서 Tools도 실행 정보를 읽는 도구는 `ToolRuntime[UserContext]`로 적음(WebFetch 2026-09-25). 되돌리려면 표시 한 줄을 고치고 새 커널 두 번(7·8절에 경고 출력이 생김 — 결과 읽기 한 단락 더).
- **`assert`**: 칸 `ticket_no` 값(그래프가 옮김) · 도구 메시지 속 이용자 번호(**도구 메시지가 있을 때만** — `for`/`if` 안) · 호출 ID 짝. 모델 답 글·도구를 부를지에 건 `assert` 0. 옛 `"context" not in result` 대신 실행 정보 키마다 `결과 딕셔너리에 있는가: False` 출력 + 결과 키 목록.
- **값 바꿔 보기** = 실행 정보의 `overdue_days` 0 → 3(질문·`ticket_no`·그래프 그대로): 도구 메시지 `이용자 M-0317: 연체 3일. 연체한 일수만큼 새 대출이 제한됩니다.`(도구 몸통 `if` 갈래), 메시지 넷·요청 2·도구 메시지 1 같음, 입력 토큰 426 → 434.
- **`MessagesState` 전제 뺌**: b3을 Ch 13 01·02·04(칸만 적은 `TypedDict`·덮어쓰는 칸·메시지 리듀서)·Ch 6 03(괄호 상속 모양)·Ch 19 01(입력 형식·명세)·Ch 20 01(이름 충돌)·Ch 20 02(받을 오류 표시)·01·02로 다시 씀. 체크포인터·미들웨어는 「Ch 23에서」·「Ch 22에서」로만.
- **새 용어 3**(라이브러리 상태 형식(AgentState) · 실행 정보(context — 칸은 실행 정보 형식 `context_schema`) · 실행 객체 표시(ToolRuntime)) — meta 「새 용어 5」 → 3. 「문의 번호」·「이용자 번호」·「연체 일수」는 일반 말.
- 본문 10블록을 새 출력으로 다시 씀(비유 「세탁기」 03 — 셔츠 깃 이름표 ↔ 윗면 틈 카드, 용어 표, 그림 넷 + 삽화, 결과 표, b7 열한 줄, 복습 넷·해설 셋 문장, 참고 자료 열한 줄). 제작 이력 문장 0. 옛 그림 `figures/03-흐름.*`은 그대로(본문 참조 0).

## 4. 흔들림 확인과 새 커널 두 번 (규격 §2-7 9·10번 끝)

- **노트북 밖 다섯 번씩**(`03-probe.md`, 규칙 §0을 첫 요청 전 03:13Z에 적음 → 요청 03:14:13~36Z): R0 5/5 · R3 5/5 **모두 같음** — 결과 키 · `ticket_no` · 메시지 종류(Human·AI·Tool·AI) · 첫 응답 `check_my_loan {}` · 도구 메시지 글 · 호출 ID 짝 · 입력 토큰(R0 189·237 · R3 189·245) · 경고 0. 출력 토큰(R0 24/29/23/24/24, R3 64/64/61/64/61)과 답 글은 **글자까지 같지 않음**. 모델 `gpt-5.4-mini-2026-03-17`, 캐시 입력 0, 오류 0. → 입력을 그대로 씀.
- **새 커널 두 번**: A `run_section.sh`(셀 실행 기록 03:26:51~57Z, 약 6초) · B 사본 `/tmp/ch21-03/B.ipynb`를 `execute.py`로(03:27:14~21Z, `UV_…`·`PYTHONPATH=…/notebooks`). `code_sha256` `0f23718b4749…` 둘 다. **셀별 출력 글자 24셀 가운데 20셀 같음, 4셀 다름** — 모두 흔들리는 값으로 미리 정해 둔 셀: 19(7절 답 글 — A 「확인 결과, 연체가 …」 ↔ B 「확인 결과 연체가 …」 쉼표 하나) · 21(8절 답 글 — 쉼표 자리) · 23(연체 0일 출력 토큰 `45` ↔ `44`, 입력 토큰·요청 수·연체 3일은 같음) · 24(연체 0일 예상 비용 `0.000522` ↔ `0.000517`). `outputs_sha256` A `8854500f33cc…` ↔ B `108a34f71670…`. 교재 출력 = A.
- **두 번 같은 값만 결론·그림에**: 상태 칸 넷 · 명세 인자 · 결과 키 · `Q-017` · 메시지 칸 네 줄 · 빈 인자 · 도구 메시지 두 글 · `False`/`True` · 표 `연체 0일 | 2 | 1 | True`·`연체 3일 | 2 | 1 | True` · 입력 토큰 `426`·`434`. **흔들린 값(결과 읽기 둘째 단락에만)**: 답 글 · 출력 토큰 `45`·`79` · 예상 비용 `0.000522`·`0.000681` · R3 답 끝 「3일 후 … 가능」(모델이 규정 글에서 끌어낸 말 — 도구 메시지에 없는 말이라고 둘째 단락에 적음). 그림 라벨·캡션·정리·복습에는 넣지 않음.
- 그림은 `.mmd`를 노트북 밖 값으로 먼저 써 두고 A·B 출력과 대조(달라진 라벨 0 — 라벨·폭 때문에만 고침).
- 설명만 고친 세 번(`mdpatch.py` — 둘째 단락 A 값 맞추기·「모델 요청에 싣는 메시지」 문장·복습 조사)은 `--no-exec`로, 노트북 출력은 A 그대로(셀별 대조 24/24, `outputs_sha256` 같음).

## 5. 도구 파일 `notebooks/runner_tools.py`

- **더한 함수** `print_branches(graph_agent)` — `# Ch 21 02절에서 배웠습니다 — 02절 노트북 6절의 같은 이름 함수를 옮겼습니다` + 설명 한 줄(「에이전트 그래프 하나를 받아, 조건부 엣지마다 … 한 줄씩 출력합니다(내놓는 값 없음)」). 본문은 02 생성기 `DEF_BRANCHES`와 **AST가 같음**(`check_same_as_before()`가 실행마다 대조, 안쪽 주석 한 줄도 그대로). 02 셀의 첫 줄 주석 「(01절 5절 반복을 함수로 묶음)」은 옮기지 않고 도구 파일 설명 주석으로 바꿈. 머리 독스트링에 「02절 노트북에서 처음 적은 함수(print_branches)도 03절부터 쓰므로 …」 한 줄.
- 해시 **`ab31d0c1…` → `6ce7a8d29a2f96a9aa48d61ace68811932920f0d69fa3b758962809c39770471`**, 89 → 103줄(코드 줄 50 → 57), import 0. 사본 `/tmp/ch21-03/runner_tools.before.py`.
- **02 노트북 영향 없음**: 02는 `agent_row, estimate_cost, show_messages, sum_usage`만 가져오고 `print_branches`는 노트북 6절에 스스로 정의(처음 가르친 절) — 가져오는 이름·코드 그대로, 다시 실행하지 않음. 01도 가져오는 넷 그대로.
- 03이 가져오는 것: `agent_row, estimate_cost, print_branches, show_messages, sum_usage`(알파벳 순). 준비 셀 결과 읽기에 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다」 + 함수마다 배운 곳 + 「이 절부터 다시 쓰므로, 본문을 글자 그대로 도구 파일에 옮겼습니다」.
- 도구 파일에 이미 있던 함수는 고치지 않음. 묶음 목록 두 곳은 01이 이미 올림 — 고치지 않음.

## 6. 상태 칸 ↔ 실행 정보 요약 (보고용)

| 항목 | 상태에 더한 칸 `ticket_no` | 실행 정보 `context` | 근거 |
|---|---|---|---|
| 적는 곳 | `class LibraryState(AgentState)` → `state_schema=` | `class MemberContext(TypedDict)` → `context_schema=` | 코드 |
| 넘기는 곳 | `invoke`의 첫 인자(입력 상태) | `invoke(…, context=딕셔너리)` | 코드 |
| 설계 객체 상태 칸 | 넷째 칸으로 더해짐 | 칸 아님(목록에 없음) | 출력 · 소스 1174~1192행 |
| 결과 딕셔너리 | 키 `ticket_no`, 값 `Q-017` 그대로 | 키 `member_id`·`overdue_days` 없음(`False`) | 출력 |
| 도구가 읽는 법 | (이번에 안 읽음 — `runtime.state`는 실행하지 않음) | `runtime.context["member_id"]` | 출력(도구 메시지) · 소스 802~817행 |
| 모델 요청 | 실리지 않음 | 실리지 않음(도구 메시지 글은 실림) | **소스로만** 1450~1454행 |
| 도구 명세 | — | 매개변수 `runtime` 빠짐(`[]`) | 출력 · 소스 base.py 331~340행 |
| 값 바꿔 보기 | 그대로 `Q-017` | `overdue_days` 3 → 도구 메시지 글 바뀜 | 출력 |

- **실행하지 않은 것**(b7): 대괄호 없는 `ToolRuntime`(경고 2건 — 모델 없는 확인만) · `context` 없이 부르기(도구 안 `TypeError` — 모델 없는 확인만) · `runtime.state`로 상태 칸 읽기 · 미들웨어가 실행 정보를 읽기(Ch 22) · 체크포인터로 상태 저장(Ch 23) · 도구를 부르지 않는 경우(밖 10/10 모두 부름) · 데이터 클래스·`BaseModel` 실행 정보(모델 없는 확인만).

## 7. 그림

- Mermaid **4장**(`03-1` flowchart TB + subgraph 둘 677 · `03-2` flowchart TB + subgraph 둘(위아래) 326 · `03-3` sequenceDiagram 821.5 · `03-4` flowchart TB + subgraph 둘 + 공통 상자 642, 모두 868 이하), **빨강 0**, 보라는 `03-3` 모델 노드 띠 하나, 초록은 넣은 값(입력 상태·context·같은 조건), 파랑은 우리 코드(invoke 한 줄·매개변수), 회색은 라이브러리가 하는 일(소스)·두 칸 공통. 설계표 `03-figures.md`, PNG 넷을 직접 열어 봄(`.cache/ch21-03-view/`). `03-3`은 첫 렌더 957.5 → 메모를 세 줄로·첫 화살표 라벨을 줄여 821.5(렌더 넷), `03-1`·`03-2`·`03-4`는 저절로 꺾인 라벨을 `<br>`로 미리 나눔.
- 삽화 **1장** `03-5-옷에-남는-이름표와-기계에-남는-카드`(비유 계열 **「세탁기」** 03 — 셔츠 깃 이름표 ↔ 윗면 틈 주황 카드) — **1차 job `b8f3d50e-d979-4b15-8260-542d11bc7072` 채택**, 재생성 0, **2크레딧**(거래 2026-09-25T03:28:19Z 「Nano Banana Pro −2」, 생성 전 잔액 2459.75, 바로 앞 거래 02:54:19Z는 02절 몫). 응답 모델 이름 표시 `nano_banana_2`(01·02와 같음). 원본 `169bba7e…`(2752 × 1536) → 저장 `71e87781…`(1100 × 614), 픽셀 대조 bbox `None`·최대 차이 0. 벽이 흰 바탕이 아니라 회갈색으로 나왔지만 관계와 무관한 배경이라 채택(그림 읽기·alt에 「회갈색 벽」). 카드는 윗면 **왼쪽** 틈, 이름표는 깃 **안쪽** — 그림 읽기에 보이는 대로 적음.

## 8. 옛 생성기

- 01이 막아 둔 것 그대로(`figures/_gen_figures.py` `raise SystemExit` · 공용 `_author_ch21_ch29.py` Ch 21 쪽 건너뛰기). 이 절에서 새로 막은 것 없음.

## 9. 서비스 요청과 비용

- 노트북 한 번 **4번**(7절 2 · 8절 2), 임베딩 0, 바깥 그림 서비스 0.
- 이 절 작업 전체 **28번** = 노트북 밖 흔들림 확인 20(R0 10 · R3 10) + 새 커널 두 번 8. 모델 없는 확인(`check03_*.py` 넷 — 주입 둘·경고 비교·04 인계용 옛 함수 그래프)은 가짜 키 글자·키 뺌·요청 0.
- 요금표(2026-09-17, 100만 토큰당 입력 0.75 · 캐시 입력 0.075 · 출력 4.50달러)로 어림한 예상 비용: 노트북 한 번 약 0.0012달러(A `0.000522` + `0.000681`), 작업 전체 약 **0.0083달러**(밖 0.005871 + A 0.001203 + B 0.001198 — 청구 금액 아님). 삽화 2크레딧.
- 참고 자료 확인(WebFetch 2026-09-25): LangChain Agents(「subclass `AgentState` and pass the subclass to `create_agent` via `state_schema=`」·「pass it as `context`」) · LangChain Tools(「The `runtime` parameter is hidden from the model」, 실행 정보를 읽는 도구 예는 `ToolRuntime[UserContext]`).

## 10. 챕터 밖 수정

| 파일 | 무엇을 |
|---|---|
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | `verify.py --chapter`가 다시 씀(`4fa11281…` → `4d673fe9a4f2758db57a496037602bc9fb5f5dc4614a44818d98cffe3a390ec0`) |

- 챕터 안(실습 폴더 포함): `labs/…/notebooks/03-*.ipynb`(새 판, `890665f1…`) · `runner_tools.py`(`6ce7a8d2…`) · `_src/03-*.html`(`1d3df126…`) · 빌드 HTML `03-*.html`(`b237631c…`, `{{` 0건)·`index.html`(`13eb7a75…`) · `figures/03-1`~`03-5` 새 파일(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`·`.prompt.md`) · `qa/upgrade/` 새 파일(`author_03.py`·`03-probe.md`·`probe/probe03.py`·`probe/probe-{R0,R3}.jsonl`·`probe/check03_{inject_check,inject_flow,warn_variants,old_api_peek}.py`·`03-figures.md`·`03-diagnosis.md`·`gates-wip-03*.json`·`review-pack/03-*.md`) · `handoff.md`·`manifest-changes.md`·`집필점검표.md`·`qa/verification.md` 03 행.
- **고치지 않은 것**: `chapter.json`(절 제목 「AgentState와 context schema」는 밑줄이 공백 — 마감 몫, `objectives`도 마감) · 실습 폴더 `pyproject.toml`·`uv.lock`·README · 01·02 파일(노트북·`_src`·생성기) · Ch 22·Ch 29·Ch 30 파일 · 공용 도구·게이트·`verify.py` · 옛 그림.
- **파일 삭제 0건**.

## 11. 뒤 챕터가 Ch 21 03·`AgentState`·`context_schema`·`ToolRuntime`에 기대는 문장 (고치지 않음, 참·거짓만)

`grep -rn 'AgentState\|context_schema\|ToolRuntime\|Ch *21' textbook/part6/*/_src` + 실습 폴더·Part 7 grep.

| 자리 | 문장·코드 | 판정 |
|---|---|---|
| Ch 22 01 `_src` 4행 b3 | 「Ch21에서는 create_agent() 함수로 에이전트를 만들었습니다.」 | 참(03도 `create_agent`) |
| Ch 22 01 `_src` 9행 b4 | 「Ch21 01절에서 … 다시 모델을 부릅니다.」 | 참(01 몫, 03도 모델 → 도구 → 모델) |
| Ch 22 노트북 01·05·06·07·09 | `from langchain.agents.middleware import AgentState, Runtime` · 훅 `state: AgentState, runtime: Runtime` | **같은 클래스**(03 출력 `두 자리의 AgentState가 같은 클래스인가: True`) — 이음새 결정적. 03은 `Runtime`(노드·미들웨어용)을 가르치지 않음 — `ToolRuntime` 설명(설치판 1663행 「distinct from `Runtime`」)은 Ch 22 몫 |
| Ch 22 01 노트북 설명 셀(셀 4) | 「`Callable`, `AgentState`, `Runtime`은 타입 힌트에 쓰는 이름입니다. … 실행 결과는 바꾸지 않습니다.」 | **훅 함수 힌트에 한정하면 참**(설치판 `middleware/types.py`에 `get_type_hints`·`signature` 호출 0 — 훅은 힌트를 읽지 않음). 03은 **도구 매개변수**의 `ToolRuntime` 표시가 값을 넣게 한다고 가르침(Ch 20 02 받을 오류 표시도 동작을 바꿈) → 일반 문장으로 읽히면 어긋날 수 있음. Ch 22 완료라 고치지 않고 기록(강사 확인 대상 3) |
| Ch 27 01·02 `_src` b3 | 「Ch 21의 create_agent는 모델과 도구의 반복을 만들었습니다」·「Ch 21에서 create_agent에 도구를 전달했습니다」 | 참 |
| Ch 29 01·04 `_src` | 「Ch21 에이전트」·`rag-comparison.json` 인용 값 | 03과 무관(06 몫) |
| Ch 30 03 `_src` b3 | 「Ch21에서 Agent의 입력과 결과가 상태 사전임을 확인했습니다」 | 뜻은 참(03 입력 상태 딕셔너리·결과 키 `['messages', 'ticket_no']`) — 「사전」은 Ch 30 몫 |
| Ch 30 `agent_service/agent.py` 11행 | `class AgentState(TypedDict)`(서비스 코드의 우리 상태 형식) | **세 번째 같은 이름**(Ch 20 01 · 라이브러리 · Ch 30) — 기록만, Part 7 몫 |
| Ch 23~26·28 `_src` · Part 7 `_src` | `AgentState`·`context_schema`·`ToolRuntime` 0건 | — |

## 12. 강사 확인 대상

1. **`ToolRuntime[MemberContext]` 대괄호(챕터 리드 결정의 예외)** — 까닭 §3(대괄호 없으면 Pydantic 직렬화 `UserWarning` 2건이 7·8절 셀에 찍힘, 값은 같음, 공식 문서 예와 같은 모양). 대괄호 모양은 Ch 13 04 `list[AnyMessage]`로 이음. 되돌리면 경고 출력 설명 한 단락이 더 필요.
2. **라이브러리 클래스 상속 `LibraryState(AgentState)`** — 규격 「조건부 — 상속이 그 절의 학습 목표일 때」, 게이트는 셀 하나 `upgrade_allow=["class_def"]`. 설치판 설명(`factory.py` 916~922행)은 상태를 넓힐 때 미들웨어 쪽을 먼저 권함(Ch 22 몫이라 본문에 한 문장만).
3. Ch 22 01 노트북 「타입 힌트는 … 실행 결과는 바꾸지 않습니다」와 03 「도구 매개변수 표시가 값을 넣게 한다」의 관계(§11) — 훅 힌트에는 참이라 고치지 않음.
4. 말 「실행 정보」(context)·「실행 객체 표시」(ToolRuntime)·「라이브러리 상태 형식」(AgentState) — 「컨텍스트」를 Ch 8 뜻으로 지키려고 새로 정한 말. 제목 「AgentState와 context schema」는 API 이름 그대로(밑줄이 공백 — 마감 몫).
5. 코드 줄 35 → 129(셀 5 → 24) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘. 늘어난 몫은 01 자료·도구 두 셀(명세 비교용), 형식 둘·도구를 셀마다 나눈 것, 상태 칸·갈래·명세·인자·키를 출력으로 보이는 셀, 값 바꿔 보기.

## 13. 남은 것 · 지워야 하지만 지우지 않은 것

- 마감 몫: 옛 그림 `03-흐름.{svg,excalidraw,caption.md}` 삭제 승인 · `chapter.json` 절 제목 표기·`objectives` · 실습 폴더 README(도구 파일 함수 일곱·요청 수) · `part6-practice.zip` 재생성(도구 파일 새 해시 포함).
- 삭제 승인 대상(만들었지만 지우지 않음): 기기 `/tmp/ch21-03/`(probe 원본 JSONL·A/B 사본·`inject_check.py`·`inject_flow.py`·`warn_variants.py`·`old_api_peek.py`·`resize.py`·`pixcmp.py`·`cmp.py`·원본 삽화 3.3MB `illu-1-orig.png`·`illu-1-1100.png`·`runner_tools.before.py`·`extra_check.py`·`ban_check.py`·`reps{1,2,3}.json`·`gates-wip-03-03.first.json`) · `.cache/ch21-03-view/`(그림 확인 사본 다섯) · `labs/…/notebooks/__pycache__/`·`qa/upgrade/__pycache__/`(있으면).

## 마감 반영 (2026-09-25, 챕터 마감 담당)

검토 1차(`review-round1-A.md`·`review-round1-B.md`) 반영과 챕터 마감에서 이 절에 한 일입니다. 전체 기록은 `chapter-summary.md`, 절 사이 기록은 `handoff.md` 「검토 반영과 챕터 마감 (2026-09-25)」입니다.

- **A-12 NumPy(다시 실행)**: 설치 셀 `"numpy==2.5.3"` · 준비물 「패키지 여섯」 · 1절 한 문장 · 결과 읽기 첫 단락. `run_section.sh … 03`으로 새 커널 한 번(06:41:59~42:05Z, 약 5.7초), **모델 요청 4번**, 어림 약 0.0012달러(`0.000495` + `0.000668`).
- **앞 교재 출력과 셀별 대조: 24셀 가운데 19셀 같음, 5셀 다름** — 설치 셀 [3](`numpy` 한 줄) + **앞 A/B에서도 갈렸던 네 셀**: 7절 답 글 [41](「네, 가능합니다. 현재 연체가 없어 …」) · 8절 답 글 [45](끝 문장 「3일 후에 새 책 대출이 가능합니다」 — 「3일 후」 그대로) · 사용량 [49] 출력 토큰 `45`·`79` → **`39`·`76`** · 예상 비용 [51] `0.000522`·`0.000681` → **`0.000495`·`0.000668`**. 결과 읽기 첫 단락·결론·그림·정리·복습에 인용한 값(상태 칸·명세 인자·결과 키·`Q-017`·메시지 네 줄·빈 인자·도구 메시지 두 글·표 두 줄·입력 토큰 `426`·`434`)은 모두 같음 → 글 고침은 **둘째 단락 「이번 실행에서는」 두 곳만**(`mdpatch` 모양, 생성기 기본값 `OUT_ZERO`·`OUT_THREE`·`COST_ZERO`·`COST_THREE`와 조사 「이었습니다」를 같게). 답 글 둘을 가리키는 문장(「새 책을 빌릴 수 있다는 뜻」·「지금은 빌릴 수 없다는 뜻 … 끝 문장의 「3일 후」」)은 새 출력에도 참. `code_sha256` `0f23718b…` → **`fdda5d72aa86d9554498d7fd23635105776661ba17853762f6368f0a5f872fe2`**, `outputs_sha256` `8854500f…` → **`ef1392a510bbb41e690212ddb14ecf51d476231deaa924aa2b93ce8c8982468c`**.
- **A-9**: 노트북 5절·b7의 「Pydantic 경고 두 줄」 → 「두 건」(한 건이 여러 줄로 찍힘), 「노트북 밖에서 모델 없이 확인」 → 「모델을 부르지 않고 확인」(세 자리 — 확인 대본은 대본 모델 `GenericFakeChatModel` 상속이었으므로 규격 §3 「가짜 모델」과 섞이지 않게). **더한 근거(검토 A 재현, 모델·대본 모델 없이 `ToolNode`만 넣은 `StateGraph(LibraryState, context_schema=MemberContext)`, 사본 `.cache/ch21-close/warn_repro.py`·`noctx.py`)**: 대괄호 없는 `ToolRuntime` → `warnings: 2`(둘 다 `PydanticSerializationUnexpectedValue … field_name='context'`)·`args: {}` · 대괄호 있음 → `warnings: 0` · 실행 정보를 빼면 `TypeError 'NoneType' object is not subscriptable`. 위 §3·`03-probe.md` §0-1의 대본 모델 확인과 같은 결론.
- **A-2 제목**: `chapter.json` 「AgentState와 context schema」 → **「AgentState와 context_schema」**(슬러그 그대로).
- **A-10(위 §11·§12-3)**: Ch 22 01 노트북 설명 셀 「실행 결과는 바꾸지 않습니다」를 **「이 절의 훅 함수에 붙인 타입 힌트는 실행 결과를 바꾸지 않습니다」**로 고침(마크다운만, 챕터 리드 결정 — 요약 §10). 설치판 `middleware/types.py`에 `get_type_hints`·`signature` 호출 0(훅은 힌트를 읽지 않음)을 다시 확인.
- **A-11(Ch 30 몫)**: Ch 30 01 b3 「Ch21에서 Agent 실행 객체를 만들었습니다」의 「실행 객체」가 이 절 일반 말(도구 매개변수 `runtime`에 들어오는 객체)과 뜻이 다름 — 요약 §15 뒤 챕터 인계에 적음(Ch 30 파일은 고치지 않음). 위 §11 표에 이 줄을 더한 셈.
- 게이트 0(검사 문장 355), 금지어 전후 같음, 생성기 = 노트북·`_src`.
