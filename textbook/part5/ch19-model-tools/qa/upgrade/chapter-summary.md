# Ch 19 모델과 도구 — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part5/ch19-model-tools` 01~06절(품질 개선) + **07절 챕터 끝 실습 절 신설**(`07-모델과-도구-실습`), 노트북 `labs/part5/ch19-model-tools/notebooks/01~07-*.ipynb`, 도구 파일 `notebooks/order_tools.py`.
- 기간: 2026-09-24(준비 조사 · 01~06절 개선 · 07절 신설 · 검토 1차 반영 · 챕터 마감). 상태: **완료(강사 확인 대기)**.
- 게이트: 수정 전 여섯 절 합계 **190**(01 31·02 27·03 29·04 40·05 38·06 25, `gates-before.json`) → 마감 뒤 **7/7 PASS, G1~G7 모두 0**(`gates-after.json`, 검사 문장 359·349·366·369·369·406·363 = **2,581**).
- 코드 셀 21·21·27·27·26·26·23 = **171**(`verify.py --chapter` → `PASS 7 sections / 171 code cells (max 13 lines)`). Mermaid **27장**(01~06 넷씩 · 07 셋), 삽화 **7장**(절마다 하나, Higgsfield `nano_banana_pro` 20크레딧, 마감 0), 복습 문제는 HTML에만.
- 모델 요청(노트북 한 번씩, 교재 출력 기준): 01 0 · 02 0 · 03 0 · 04 28 · 05 5 · 06 8 · 07 5 = **46번**(모두 `gpt-5.4-mini`, 임베딩 0). 06은 8~9번, 07은 4~5번(모델이 요청한 도구 수에 따름, 바퀴 한도 5). 노트북마다 요금표로 어림한 예상 비용은 0.01달러 아래(청구 금액 아님). **01~03은 API 키 없이 돕니다**(01은 `check_bundle_execution.py`가 키 없는 학생 묶음에서 실행).
- 화면 검사 `visual.cjs`: HTML **여덟 개**(일곱 절 + `index.html`) × 1280px·390px = **16행 PASS**(`textbook/_notebook/checks/ch19-model-tools/visual-results.json`).
- **마감에서 다시 실행한 노트북은 없습니다.** 일곱 노트북 모두 `code_sha256`·`outputs_sha256`·`executed_at`이 마감 전후 같습니다(마크다운만 바뀜, §15).
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 18 요약 → **이 문서** → `handoff.md`(절 사이 세부, 끝의 「검토 반영과 챕터 마감」) → 절별 `NN-diagnosis.md`(끝 「마감 반영」) → 검토 `review-round1-A.md`(01~03·공통)·`review-round1-B.md`(04~07) → 흔들림 확인 `04~07-probe.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 문법·API | 새로 만든 함수 (도구 파일에 둔 것은 굵게) | 새 용어 |
|---|---|---|---|
| 01 tool과 Ch 4 함수 재사용 (paired) | `from langchain.tools import tool` · 맨 **`@tool`**(데코레이터 줄, Ch 2 09 세 문장 + 링크) · **독스트링**(도구 설명이 됨) · `@tool` 함수 매개변수에만 **타입힌트 `: str`**(Ch 2 07) · 속성 `.func`·`.name`·`.description`·`.args` · **`.invoke(인자 딕셔너리)`** · `convert_to_openai_tool`(도구 명세) · 내장 `callable` · 실제 `TypeError: 'StructuredTool' object is not callable`과 `try/except TypeError as error`(Ch 2 05) · 도구 파일 시그니처의 키워드 전용 `*`·`status=None` 풀이 · `dtype` 딕셔너리 | (노트북) `list_orders_by_status` · **`fetch_orders`는 Ch 4 실습 폴더 판을 옮김** | 도구 · 도구 설명 · 독스트링 · 입력 형식 · 도구 명세 (5) |
| 02 Pydantic 인자와 반환 스키마 (paired) | `from typing import Literal` · 양식 클래스 칸의 `Literal[…]` · 인자 있는 **`@tool(args_schema=…)`** · 슬라이싱 `[:limit]` · `.model_validate(딕셔너리)` · `model_json_schema()["required"]` · Ch 6 03에서 이은 `BaseModel`·`Field(ge=, le=, description=)`·`ValidationError` | (노트북) `OrderQuery` · `search_orders` · `OrderRecord` | 양식 클래스 · 고를 수 있는 값 · 입력 형식 클래스 · 입력 검사 · 내놓는 값 검사 틀 (5) |
| 03 좋은 도구 이름과 설명 (experiment) | `json.dumps(…, ensure_ascii=False)` · `split("_")` · `range(len(목록))`로 두 목록 짝짓기 · 같은 함수 이름으로 도구 다시 정의 · 슬라이싱 `[:count]` | **`find_order`** · **`sum_orders`** · (노트북) `check_tool` · `count_met` · `spec_length` | 몸통 함수 · 동사로 시작하는 이름 · 사용 조건 · 설명 기준 · 명세 글자 수 (5) |
| 04 설명만으로 도구 선택하기 (experiment) | **이 챕터 첫 모델 요청** · 인자 있는 `@tool("이름")`(공개 이름) · **`model.bind_tools(도구 목록, parallel_tool_calls=False)`** · 속성 `.kwargs["tools"]` · 응답 **`.tool_calls`**(Ch 7 05 「도구 호출 목록」)와 한 건 = 도구 호출 요청(칸 `name`·`args`·`id`·`type`) · `len(response.content)` · 이중 `for` · Ch 6 06 `estimate_cost` 가져오기 | **`tool_call_names`** · **`ask_questions`** · **`count_expected`** · **`estimate_cost`**(Ch 6 06 판을 옮김) · (노트북) `records_cost` | 공개 이름 · 도구 알려 주기 · 도구 호출 요청 · 기대 도구 · 선택 채점 (5) |
| 05 bind_tools와 병렬 호출 (experiment) | **이 챕터 첫 도구 실행** · `parallel_tool_calls=True`(여럿 담기) · **`도구.invoke(도구 호출 요청)` → `ToolMessage`**(칸 `tool_call_id`·`content`, 내용은 JSON 글) · 도구 찾기 표 · `HumanMessage(content=…)`(Ch 13 04) · 메시지 목록에 `append` 뒤 다시 `invoke` · `type(x).__name__ == "AIMessage"` · `json.loads`(Ch 17 03) · `for … range(turn_limit)` + `break`(바퀴 한도, Ch 17 03) · `str(수) in 글` | **`run_tool_calls`** · **`ask_until_answer`**(받은 목록에 바로 이어 붙임 — 마감 B-3) · **`sum_usage`** · (노트북) `check_amounts` | 도구 실행 · 도구 메시지 · 호출 ID · 여럿 담기 · 도구 찾기 표 (5) |
| 06 오류와 읽기 쓰기 분리 (paired) | **`raise ToolException(글)`** · 도구 속성 **`handle_tool_error = True`**(`@tool(handle_tool_error=True)`는 설치판에서 `TypeError` — 노트북 밖 확인) · 도구 메시지 칸 **`status`**(`success`/`error`) · 실제 `ToolException`과 `try/except ToolException as error` · `list(목록)`·목록 `+` | **`pick_tools`** · **`make_tools_table`** · **`spec_names`** · **`show_messages`** · (노트북) `get_order_by_id`·`cancel_order`(흉내) | 읽기 도구 · 쓰기 도구 · 도구 오류 · 오류 담기 설정 · 결과 상태 (5) |
| 07 모델과 도구 실습 | **새 문법·API·말 0개** | 노트북에만 `CancelForm`·`request_cancel`(02 모양 쓰기 도구) · `handle_inquiry`(조립 함수) · `summarize_run` · `print_summaries` | 0 |

- 새 용어 합계 **30개**(절 meta 「새 용어」 5·5·5·5·5·5·0과 같음).
- **이 챕터 주제라서 허용한 문법**(챕터 리드 결정 3): 맨 `@tool`·`@tool("이름")`(04)·`@tool(args_schema=…)`(02) · `@tool` 함수 매개변수의 간단한 타입힌트(`str`) · 독스트링 · 02·07 양식 클래스(칸만). 그 밖의 자리(도구 파일 포함)는 타입힌트·데코레이터·클래스·반환 힌트 0.
- **쓰지 않은 Python 이름(일곱 절 모두 0건, AST 확인)**: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`:=`·`global`·함수 안 함수·`next`·`all`·`any`·`sum`·`max`·`min`·`sorted`·`enumerate`·`zip`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`+=`·기본값 매개변수·반환 힌트·튜플 풀기·별표 풀기·`isinstance`·`TypeAdapter`·`tool_choice`·시스템 메시지·**`ToolNode`·`tools_condition`·`create_agent`·`StateGraph`·미들웨어**·`ToolMessage(…)` 직접 만들기·`handle_validation_error`. 도구 파일의 예외는 `fetch_orders`의 `status=None`(Ch 4 약속 시그니처)과 `estimate_cost`의 `.get`(Ch 6 06 원본)뿐.
- 셀 모양: 코드 셀 최대 13줄(verify), 함수 본문 최대 8줄(07 `summarize_run`), 셀당 함수 하나, 첫 줄 주석 100%. **모델이 정하는 값(도구 호출 요청·답 글)에 건 `assert`는 0건** — CSV에서 정해지는 값·호출 ID 짝에만.

## 2. 앞 챕터에서 이어 쓴 부품과 값

- **Ch 4 01 `fetch_orders(csv_path, *, status=None)`**(실습 폴더 `data_tools.py` 판 — Ch 4 약속 네 곳): `data_tools.py`는 `bs4`·`httpx`를 import해 가져올 수 없어 **이 챕터 도구 파일로 옮겼습니다**(몸통 AST 같음, 자료형 표시와 독스트링을 빼고 주석을 담). `data/orders.csv`는 Ch 4 `data/orders.csv`와 바이트 단위로 같음(`f2d1e3ee…`, 네 줄 `O101`~`O104`). Part 5 묶음에 Ch 4 실습 폴더가 함께 들어 있어 01 b3 「두 파일을 나란히 열어 볼 수 있습니다」가 참.
- **Ch 6 06 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`**와 요금표(2026-09-17, 100만 토큰당 입력 0.75 · 캐시 입력 0.075 · 출력 4.50달러) · 「예상 비용」 = 사용량 × 요금표(청구 금액 아님). 04가 처음 옮김(Ch 17 `agent_tools.py`와 함수 AST 같음).
- **Ch 6 03** 양식 클래스(`StudyCard`·`Field` 범위·`ValidationError`·`model_json_schema`)와 Before(설명에만 범위를 적은 양식이 9를 받음) → 02 · **Ch 4 03** Before(오류 없이 다른 고객 주문) → 02 Before 「오류 없이 빈 목록」.
- **Ch 2**: 05 `try/except 오류이름 as error` · 07 타입힌트(값을 검사하지 않음)·모듈 가져오기(현재 작업 폴더에서 찾음) · 09 `@` 줄 · 10 `BaseModel`·`Field()` — **Ch 2 09 b2·b8 · 10 b2·b8 · Ch 22 01 b3의 「Ch 19 `@tool` 줄」·「Ch 19 도구 입력 규칙에서 `BaseModel`·`Field()`」 약속을 01·02가 지켰습니다.** Ch 2 07의 `order_tools.py`(임시 폴더 예제 모듈)와 **이름이 같은 다른 파일**이라는 문장을 01(노트북·b3)·README에 둠(마감 A-12).
- **Ch 7 05** 「도구 호출 목록(`tool_calls`)」 · **Ch 13 04** 메시지 목록·`HumanMessage` · **Ch 16 01** `raise`로 오류 내기 · **Ch 17** 02·03 부작용·사람 확인·루프·**바퀴 한도**·`json.loads` · **Ch 18 03** 「함께 보내기」(05 「한 응답 안 도구 호출 요청 여럿」과 다르다고 가름).
- **Ch 16 01 「입력 검사」와 뜻이 다릅니다**(마감 A-4): Ch 16 = 모델을 부르기 전에 우리 코드가 사용자 질문을 봄 / Ch 19 02 = 도구가 몸통을 실행하기 전에 인자 딕셔너리를 입력 형식 규칙에 맞춰 봄. 02 용어 표에 한 문장으로 가름(§4).
- **Ch 17 `agent_tools.py`·Ch 18 `workflow_tools.py`는 가져오지 않습니다.**

## 3. 절별 사례·값 (새 커널 두 번과 노트북 밖 확인에서 같았던 값)

| 절 | 과제·입력 | 결정적 값(결론·그림에 쓴 값) | 요청 |
|---|---|---|---|
| 01 | Ch 4 함수를 도구로 감싸기 · CSV 네 줄 | `list_orders_by_status의 종류: StructuredTool` · `입력 형식: {'status': {'title': 'Status', 'type': 'string'}}` · `꼭 채울 인자: ['status']` · `명세에 csv 글자가 있는가: False` · Before `받은 오류: TypeError`·`'StructuredTool' object is not callable` · After `받은 주문 수: 2`(`O101`·`O103`) · 타입힌트를 빼면 `{'status': {'title': 'Status'}}`·명세 `{'status': {}}`, 결과 같음 | 0 |
| 02 | 상태 셋 `Literal` + `limit` 1~10 · Before 01 도구에 `shipped` | `꼭 채울 칸: ['status', 'limit']` · 명세 `limit` 칸 `maximum 10·minimum 1` · Before `받은 주문 수: 0`·`받은 값: []`(오류 없음) · After `1 validation error for OrderQuery`·`literal_error`·몸통 실행 줄 없음 · limit 0 → `greater_than_equal` · 내놓은 값 검사 `OrderRecord`(만든 줄 −9000 → 걸림, 도구 명세에 `amount` 없음) | 0 |
| 03 | 같은 몸통에 설명만 다른 두 판 · 기준 넷(이 절이 정함) | `이름 같음: True`·`입력 형식 같음: True` · 짧은 판 `채운 기준 수: 1`(이름만) · 자세한 판 `4` — **자세한 판은 이 절의 낱말 표·인자 이름에 맞춰 쓴 예라 1 ↔ 4는 실행 전에 정해진 값**(마감 A-5) · 코드로 새로 알게 된 값 = 명세 글자 수 `599`·`923`(+`324`), 도구 1·2·3개 `309`·`610`·`923` · 이름만 `order_info` → `3` | 0 |
| 04 | 공개 이름을 `tool_a`·`tool_b`·`tool_c`로 가린 짧은 판/자세한 판 × 질문 셋(목록·한 건·건수) × 세 번 · 값 바꿔 보기 = 합계 도구 설명만 자세한 판 네 문장 | 건수 질문 **짧은 판 `['tool_a']` 세 번 · 자세한 판 `['tool_c']` 세 번**, 나머지 질문은 두 판 같음 · `6 / 9` ↔ `9 / 9`(이 절이 정한 역할 나눔과 맞은 수 — 마감 B-2) · 목록 질문 입력 토큰 `177` → `330`(+`153`) · 예상 비용 `0.001906` ↔ `0.002938` · 합계 도구만 바꾼 판 `['tool_c']`·`9 / 9` — **네 문장 가운데 어느 문장이 선택을 바꿨는지는 가르지 않음**(마감 B-1) | 28 |
| 05 | 「O101 주문과 O103 주문의 금액을 알려 줘.」 · 도구 하나(`get_order_by_id`) | `도구 호출 요청 수: 2` · `ToolMessage`·`tool_call_id가 요청 id와 같은가: True` · 여럿 담기 `{'requests': 2, 'input_tokens': 515, 'output_tokens': 84}` · 하나씩 `{'requests': 3, 'input_tokens': 771, 'output_tokens': 71}` · 예상 비용 `0.000764`·`0.000898` · 답 글에 두 금액 `True` | 5 |
| 06 | 읽기 도구 `get_order_by_id`(없는 번호면 `ToolException`) + 쓰기 도구 흉내 `cancel_order` · 질문 「O101 주문을 취소해 줘.」·「O999 주문의 금액을 알려 줘.」 | Before 한 목록 `['get_order_by_id', 'cancel_order']` · O999 흐름 `ToolException`으로 멈춤·`메시지 수: 2` · After `status: error` 도구 메시지·확인 전 명세 `['get_order_by_id']`·쓰기 도구 요청 0 · 값 바꿔 보기(확인 뒤) `cancel_order` 실행·`CSV의 O101 상태: paid` | 8 |
| 07 | 「O102 주문이 아직 결제 대기 중이면 취소해 주세요. 다른 상품을 잘못 주문했어요.」 · 사람 확인 값 `False`/`True` | §7 | 5 |

## 4. 용어 (챕터 안에서 한 번만 정의하고 이어 씀)

| 절 | 말 | 뜻 | 코드에서 |
|---|---|---|---|
| 01 | 도구(tool) | 모델이 고를 수 있게 이름·설명·입력 형식을 붙여 감싼 함수 | `@tool` 아래 함수, 종류 `StructuredTool` |
| 01 | 도구 설명(description) | 도구가 하는 일을 적은 글, 독스트링이 들어감 | `.description` |
| 01 | 독스트링(docstring) | 함수 첫 줄에 큰따옴표 세 개로 감싸 적는 설명 글 | `"""…"""` |
| 01 | 입력 형식(스키마, schema) | 도구가 받는 인자의 이름과 자료형을 적은 틀 (비유: 메뉴판 한 줄의 「주문할 때 적는 칸」 — 마감 A-1) | `.args` |
| 01 | 도구 명세(tool definition) | 이름·설명·입력 형식을 모델 요청에 실을 모양으로 한 딕셔너리에 모은 것 | `convert_to_openai_tool(…)` |
| 02 | 양식 클래스(BaseModel) | 칸마다 자료형과 규칙을 적어 값을 검사하는 클래스(Ch 6 03 말) | `OrderQuery`·`OrderRecord` |
| 02 | 고를 수 있는 값(Literal) | 칸에 적을 수 있는 값을 몇 개로 정해 두는 표시 | `Literal["paid", "pending", "cancelled"]` |
| 02 | 입력 형식 클래스(args_schema) | 도구의 입력 형식을 매개변수 대신 정하는 양식 클래스 | `@tool(args_schema=OrderQuery)` |
| 02 | **입력 검사** | 도구가 몸통을 실행하기 전에 인자 딕셔너리를 입력 형식의 규칙에 맞춰 보는 일. **Ch 16 01 「입력 검사」(모델을 부르기 전에 사용자 질문을 우리 코드가 보는 일)와 보는 값·자리가 다름** | 걸리면 값 검사 오류 `ValidationError` |
| 02 | 내놓는 값 검사 틀(반환 스키마) | 도구가 내놓은 값의 칸을 코드가 따로 검사하는 양식 클래스, 도구 명세에 없음 | `OrderRecord.model_validate(row)` |
| 03 | 몸통 함수 | 도구로 감싸기 전에 실제 일을 하는 평범한 함수 | `find_order`·`sum_orders` |
| 03 | 동사로 시작하는 이름 | 하는 일을 뜻하는 동사를 앞에, 대상을 뒤에 밑줄로 이은 도구 이름(이 챕터에서만 쓰는 기준 — 마감 A-6) | `get_order_by_id` |
| 03 | 사용 조건 | 그 도구를 언제 쓰는지 적은 설명 문장 | 「… 때 씁니다」 |
| 03 | 설명 기준 | 이름·설명을 코드로 확인하려고 이 절에서 정한 네 가지 물음 | `check_tool` |
| 03 | 명세 글자 수 | 도구 명세를 JSON 글로 바꿔 센 글자 수, 토큰 수와 다름 | `spec_length` |
| 04 | 공개 이름 | 모델에게 보이는 도구 이름 | `@tool("tool_a")` |
| 04 | 도구 알려 주기(bind_tools) | 모델 객체에 도구 명세 목록을 붙여 요청마다 함께 싣게 하는 일 | `model.bind_tools(…)` |
| 04 | 도구 호출 요청 | 모델이 응답에 적어 보낸 「이 도구를 이 인자로 불러 달라」는 한 건 | `response.tool_calls`의 딕셔너리 |
| 04 | 기대 도구 | 질문마다 실행 전에 사람이 정해 둔, 골라야 할 도구 | `expected_tools` |
| 04 | 선택 채점 | 고른 도구 이름이 기대 도구와 같은지 세는 일(인자는 보지 않음) | `count_expected` |
| 05 | 도구 실행 | 프로그램이 도구 호출 요청을 받아 그 도구를 부르는 일 | `run_tool_calls` |
| 05 | 도구 메시지(ToolMessage) | 도구 실행 결과를 모델에게 보낼 메시지로 담은 것 | `ToolMessage` |
| 05 | 호출 ID(tool_call_id) | 도구 메시지가 어느 도구 호출 요청의 결과인지 알리는 번호, 요청의 칸 `id`를 옮겨 적음 (비유: **같은 색 집게**) | `.tool_call_id` |
| 05 | 여럿 담기(parallel_tool_calls) | 한 응답에 도구 호출 요청을 여럿 담아도 되는지 정하는 인자 | `parallel_tool_calls=True` |
| 05 | 도구 찾기 표 | 공개 이름을 키, 도구를 값으로 둔 딕셔너리 | `tools_by_name` |
| 06 | 읽기 도구 | 자료를 찾아 읽기만 하고 아무것도 바꾸지 않는 도구 | `get_order_by_id` |
| 06 | 쓰기 도구 | 주문 상태처럼 무언가를 바꾸는 도구, 부작용이 있음 | `cancel_order`(흉내) |
| 06 | 도구 오류(ToolException) | 도구가 일을 끝내지 못했다고 알리려고 몸통에서 내는 오류 | `raise ToolException(…)` |
| 06 | 오류 담기 설정(handle_tool_error) | 도구 오류를 받아 도구 메시지에 담을지 정하는 **도구의 속성**, 기본값 `False`, `ToolException`만 받음 | `도구.handle_tool_error = True` |
| 06 | 결과 상태(status) | 도구 메시지의 칸, 결과면 `success`, 도구 오류면 `error` | `.status` |

- **일반 말(새 말 아님)**: 도구 이름(= 함수 이름) · 데코레이터 줄(Ch 2 09) · 인자 딕셔너리 · 꼭 채울 인자/칸(`required`) · **CSV 파일 위치**(「경로」 대신) · 칸(「필드」 대신) · 값 검사 오류(Ch 6 01) · 몸통 실행 줄 · 짧은 판·자세한 판 · 목록/한 건/합계 도구 · **도구 호출 목록**(Ch 7 05) · 응답 글(`.content`) · 최종 답 · 메시지 목록(Ch 13 04) · **바퀴 한도**(Ch 17 03, `turn_limit`) · 함께 보내기(Ch 18 03) · 사람 확인 값(`person_confirmed`) · 확인 전/뒤 목록 · 한 목록/나눈 목록 · 흉내 · 조립 함수·기록 장치·실행 요약·취소 까닭(07). **「흐름 끝 표지」는 마감에서 풀어 쓴 말(「마지막 응답에 도구 호출 요청이 없음」)로 바꿔 이제 0건**(B-6).
- **제목의 영어·「병렬」**: 「tool」·「Pydantic」·「반환 스키마」·「bind_tools」·「병렬」은 제목과 본문 풀이 한 번에만(05 「병렬 호출」 = 한 응답 안에 도구 호출 요청이 여럿 — Ch 18 03 「함께 보내기」와 다름). 「동시」는 05 구분 문장에만.
- **금지어(일곱 절 설명·코드·주석·캡션·`.mmd`·도구 파일 0건 — 제목·풀이·링크 파일 이름 말고)**: 「분기」·「경로」·「반환」·「임계값」·「재정렬」·「쿼리」·「인덱스」·「융합」·「조각」·「노드」·「돌려줍니다」·「프롬프트」·「폴백」·「레코드」·「캐시」 단독·「병렬」(제목 밖)·「검증」·「범주」·「사전」·「거부」·「측정」·「집합」·「정규화」·「추정 비용」·「필드」·「인터페이스」·「인라인」·「장식」·「로직」·「포장」·「직렬화」·「식별자」·「문맥」·「동시」(05 구분 문장 밖)·「순차」·「지연」·「강사 시연」·「개선 전」·「쉽게·간단히·당연히」. 마감이 더한 문장 43줄(노트북)·`_src` 문장도 같은 목록으로 셈(링크 파일 이름의 「검증」·「반환」·「병렬」·「지연」 말고 0).

## 5. 색 규칙 (Mermaid 27장, 빨강은 paired Before 결함만)

- **우리가 코드로 적은 함수·부르는 줄 파랑(flow)** · **자료·손으로 정한 값(CSV 파일 위치·요청 글·질문·바꾼 값) 초록(tool)** · **출력으로 확인한 값 노랑(measure)** · **LangChain이 준 것(`@tool` 줄·도구 객체·`convert_to_openai_tool`·`bind_tools`)과 두 칸 공통 사실 회색** · **보라는 그 절에서 실제로 부른 모델만**(01~03 0장, `04-1`·`04-2`·`05-3`·`06-1`·`06-4`·`07-1`) · **빨강은 paired Before 결함 결과만**(`01-3` 왼쪽 하나 · `02-3` · `06-3` `b1`·`b2`). experiment 03·04·05·07은 빨강 0, 받아 출력한 오류는 노랑.
- 원본 viewBox 폭 모두 868 이하(최대 815). 넷 이상 한 줄이면 `flowchart TB`, 칸 비교는 subgraph 둘 + `~~~` 회색 공통 상자, 저절로 꺾이는 라벨은 `<br>`로 미리, 노드 id `call`·`end` 금지. **마감에서 다시 렌더한 `.mmd`는 없습니다**(캡션 `03-3`·`06-3`과 삽화 캡션 `01-5`·`07-4`만 글로 고침).
- 비유 계열 「식당 주문 전표와 내주는 창」: 01 메뉴판 카드와 창턱 전표(주방 요리법 = 몸통) · 02 빈칸 전표/동그라미 셋 전표와 열린 창·닫힌 덧문 · 03 흐린 카드/뚜렷한 카드 메뉴판 둘 · 04 이름표가 비어 있는 카드 셋과 칠한 칸 하나 · 05 주문 둘을 적은 전표와 **같은 색 집게** 짝 · 06 열린 창과 걸쇠 건 서랍 · 07 도장 받은 전표와 취소 상자. 사람·손·동물·화면·쟁반·화살표·글자는 쓰지 않았습니다.

## 6. 서비스 요청과 흔들린 값

- 노트북 한 번 요청: §머리(46번). 작업 전체 서비스 요청(노트북 밖 확인 + 새 커널 두 번): 04 102 · 05 36 · 06 63 · 07 36 = **237번**(01~03 0), **마감 0번**. 요금표로 어림한 예상 비용 합 약 0.073달러(04 0.027 · 05 0.012 · 06 0.019 · 07 0.015, 청구 금액 아님). 삽화 7장 20크레딧(02·06·07은 1차 탈락 뒤 2차 채택).
- **흔들림 확인(노트북 밖 다섯 번, 규격 §2-7 10번 끝)**: 04(세 판 × 다섯 번 45/45 같음 — 후보 입력 C1·C2는 쓰지 않음) · 05(두 흐름 다섯 번, 토큰 515/84·771/71 같음) · 06(판단 규칙을 첫 요청 전에 적음 · **한 목록 + 취소 질문의 첫 응답 도구 이름은 11번 중 1번이 읽기 도구 먼저** → Before 결함을 「명세에 쓰기 도구가 실림」이라는 코드 쪽 사실로 세움) · 07(후보 A만, 다섯 번 같음).
- **04의 도구 선택은 흔들린 값이 없었습니다**(A·B·밖 다섯 번 모두 같음, 다른 것은 칸 `id`뿐).
- **탐색·설계로 정한 입력(b7에 「흐름을 보여 주려고 정한 예」)**: 03 기준 넷·동사 표·낱말 표와 그에 맞춰 쓴 자세한 판(마감 A-5) · 04 질문 셋·기대 도구·가린 공개 이름 · 05 질문과 도구 하나 · 06 질문 둘·도구 둘·`parallel_tool_calls=False` · 07 문의 글·O102·취소 까닭 셋·막히는 예 `too_expensive`.
- **흔들린 값의 자리**: 06 첫 응답 도구 이름·확인 뒤 흐름 요청 수(「…이면 9가 됩니다」 셈) · 06·07 출력 토큰과 예상 비용 · 모든 답 글(07 B 실행 1 답 글이 도구 없이 「취소 처리해 드릴게요」) — 결과 읽기 둘째 단락·「확인할 점」·b7에만 「이번 실행에서는」·「교재 출력에서는」으로. **그림 라벨·캡션·정리·복습·본문 결론에서 흔들린 값에서 끌어낸 비교 0건**(마감 확인, 규격 §2-7 9번 끝).
- **재지 않은 것**: 걸린 시간(일곱 절 모두) · 청구 금액 · 서비스 오류(429·5xx·시간 제한) · 흐름 안 입력 검사 오류(07 — 소스로만, 마감 B-9) · `ValueError`를 설정을 켠 도구에서 본 장면(06 — 노트북 밖 확인만).

## 7. 07절 실습 절 주제와 결과

- 제목 「**모델과 도구 실습: 주문 취소 문의를 도구 둘로 처리하고 사람 확인 값 바꾸기**」, 슬러그 `07-모델과-도구-실습`, `format: experiment`, meta 「실습 30분 · 새 용어 0」. **챕터 시수에 더하지 않습니다**(규격 §7-2). 01~06 meta 합 강의 1h × 6 = **6h** · 실습 2+2+1+2+2+1 = **10h** = `chapter.json` 「총 16h · 강의 6h · 실습 10h」(`_build_index.py`도 6·10).
- 붙인 앞 절 기능 셋: **02 입력 검사**(새 쓰기 도구 `request_cancel(order_id, reason)` — `CancelForm`의 취소 까닭 `Literal["changed_mind", "wrong_order", "late_delivery"]`) + **05 도구 실행 반복**(`ask_until_answer`) + **06 읽기·쓰기 분리**(`pick_tools`의 사람 확인 값 = 바꾸는 값). 읽기 도구는 06 3절 셀 그대로(오류 담기 설정 켬 — 흐름에서는 쓰이지 않음). 뺀 것: 04 선택 채점 · 05 여럿 담기 · 06 오류 장면 · 06 한 목록/나눈 목록 견주기. **바꾸는 값은 06 값 바꿔 보기와 같고, 새로 볼 것은 입력 검사를 붙인 쓰기 도구가 읽기 결과 뒤에 이어 불리는 차례**(마감 B-11).
- 결과(새 커널 두 번 + 노트북 밖 다섯 번 모두 같음): 정해 둔 셋 밖의 까닭 `too_expensive` → 몸통 전 `ValidationError`(모델 요청 0) · 실행 1(`False`) 명세 `['get_order_by_id']`·요청한 도구 `['get_order_by_id']`·`success`·요청 2 · 실행 2(`True`) 명세 둘·`['get_order_by_id', 'request_cancel']`·`success, success`·요청 3·`{"order_id": "O102", "reason": "wrong_order", "cancel_requested": true}` · 첫 요청 입력 토큰 `203` ↔ `319` · `CSV의 O102 상태: pending`(흉내라 파일 그대로). 파일 쓰기 0, 걸린 시간 재지 않음.
- **흐름 안 입력 검사 오류는 오류 담기 설정으로 받지 못해 흐름이 멈춥니다**(설치판 langchain-core 1.6.2 `tools/base.py` 542~544·1088~1092·1109~1117행, 이번에 실행하지 않음 — 마감 B-9, b7). 교재 흐름에서 모델이 셋 밖의 까닭을 보낸 적은 없습니다.

## 8. 도구 파일 `notebooks/order_tools.py` — 함수 표와 해시 변천

| 함수(인자) | 배운 곳(= 옮긴 절) | 가져오는 절 |
|---|---|---|
| `fetch_orders(csv_path, *, status=None)` | Ch 4 01(실습 폴더 판) | 01·02·03·04(이름만)·07 |
| `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` | Ch 6 06(04가 옮김) | 04·05·06·07 |
| `find_order(csv_path, order_id)` · `sum_orders(csv_path, status)` | 03 | 04·05·06·07(`find_order`) |
| `tool_call_names(response)` · `ask_questions(bound_model, expected_tools, repeats)` · `count_expected(records, expected_tools)` | 04 | 05·06·07(`tool_call_names`) |
| `run_tool_calls(response, tools_by_name)` · `ask_until_answer(bound_model, messages, tools_by_name, turn_limit)` · `sum_usage(messages)` | 05 | 06·07 |
| `pick_tools(read_tools, write_tools, person_confirmed)` · `make_tools_table(tools)` · `spec_names(bound_model)` · `show_messages(messages)` | 06 | 07 |

- 함수 **열넷**, 함수마다 `# Ch N NN절에서 배웠습니다`, import `pandas`뿐, 전역 이름 기대기 0(CSV 파일 위치는 인자), `@tool` 감싸기와 도구 객체는 노트북에(챕터 리드 결정 2). 이 챕터가 가르친 12개는 처음 가르친 셀과 함수 AST 같음, `estimate_cost`는 Ch 6 06·Ch 17 `agent_tools.py`와 AST 같음. **`ask_until_answer`는 받은 목록에 바로 이어 붙입니다**(06 Before가 그 성질로 멈춘 뒤에도 목록에 남은 응답을 봄 — 05·06에 풀이, 마감 B-3).
- **해시 변천**: 없음 → 01 `ade40a31…` → 03 `a7106e48…` → 04 `28c4010d…` → 05 `f444d5a3…` → 06 `f2f48a15…` → 07 그대로 → **마감 `fa5975b5e2466cf205d84a235f4ace2e0655d28f28f276f4fc1e72da5c597062`**(12행 `fetch_orders` 주석만 「(자료형 표시와 설명 글을 빼고 주석을 달았습니다)」 — 검토 A-10, AST 같음).
- 가져오는 절(01~07)마다 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다」가 준비 셀 결과 읽기에 한 번씩(01은 뒤에 Ch 2 07 모듈과 다르다는 문장 — A-12). 묶음 목록 두 곳(`textbook/part5/public-files.json`·챕터 `qa/public-files.json` `labs`)에 있고, 마감 zip에 들어간 판이 디스크와 같음(§10). **마감에서 Part 6 선행 목록 둘에 더했습니다**(§10).
- **Ch 19 실습 폴더 전용**입니다. Ch 20 실습 폴더(`labs/part5/ch20-tool-node`)에는 없습니다.

## 9. 의존성 (`pyproject.toml`·`uv.lock`, 바꾸지 않음)

- `dependencies = ["langchain==1.4.0", "langchain-openai==1.6.0", "pandas==3.0.5", "pydantic==2.12.5", "python-dotenv==1.2.3"]`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`pytest==9.1.1`·`ruff==0.15.6`. 잠금에 `langchain-core 1.6.2`·`langgraph 1.2.11`·`openai 3.11.0`·`tiktoken 0.14.0`·`httpx 0.28.1`·`pip 26.2`. 노트북 `%pip`은 그 절이 쓰는 패키지만(01·03 셋, 02 넷, 04~06 다섯, 07 여섯, 모두 잠금 판).
- 교재 출력 환경 `.cache/vm/venv-ch19-model-tools`(Python 3.12.13, 잠금과 판 차이 0). 실습 폴더에 `tests/` 없음.

## 10. 챕터 밖 수정 (전부 목록)

| 파일 | 언제 | 무엇을 |
|---|---|---|
| `labs/part5/ch19-model-tools/notebooks/01~07-*.ipynb` · `notebooks/order_tools.py` | 01~07절 · **마감**(노트북 마크다운만 · 도구 파일 주석 한 줄) | 실습 폴더(챕터 몫) — §1·§8·§15. 마감은 코드·출력 0 변경. 노트북 파일 `5d376140`→`ff44fdea` · `1244ce6f`→`e5a8b5e3` · `dae5411e`→`f0d83063` · `8eb70c7c`→`ac27b966` · `0010c4f3`→`c4d4204f` · **`f3d5351a`→`9c14c372`** · `79d5b0d9`→`4f8f9ed5`, 도구 파일 `f2f48a15`→`fa5975b5` |
| `labs/part5/ch19-model-tools/README.md` | 07절(07 단락) · **마감(전체)** | `917725f6…` → **`ecca288b…`**: 노트북 일곱(01~03 키 없이 · 04~07 API 키), `uv sync --locked` → `.venv` → `notebooks/`에서 열기(다른 폴더면 `ModuleNotFoundError`), 키는 커널 폴더에서 위로 찾은 첫 `.env`, 패키지 판, `data/orders.csv` = Ch 4 자료, 모델 설정(`gpt-5.4-mini`·`temperature=0`·`reasoning_effort="none"`·`bind_tools`), 도구 파일 단락(고정 문장 뜻 · Ch 2 07 모듈과 다름 · 함수 열넷·배운 절 · `pandas`만), 절마다 하는 일, 요청 46번(절별)·예상 비용(청구 아님), 07 단락. 「노트북은 서로 독립적」·「프로젝트 루트부터 상위 폴더」·「1달러 미만으로 제한」 뺌 |
| `textbook/part2/ch07-prompt-engineering/_src/05-CoT와-ReAct의-경계.html` · `05-CoT와-ReAct의-경계.html` | **마감** | b4 「도구를 모델에 알려 주고 호출 요청을 받는 방법은 Ch 19 **05절에서** 다룹니다」 → 「Ch 19 **04절부터** 다룹니다」(`_src` `e94639b0`→`3aea35b6`, HTML `f52b5cf7`→`9cc71a47`, 다른 Ch 7 HTML 그대로). 생성기 `author_05.py`에는 이 문장이 없음(노트북 문장 「Ch 19에서 배웁니다」는 참이라 그대로) · `verify.py --chapter` **PASS 9 sections / 179 code cells (max 15 lines)**, 05 게이트 0. `{{` 1건은 04 HTML의 기존 LangChain 오류 글(`{{history}}`)로 이번 변경과 무관 |
| `textbook/part5/ch17-agent-overview/_src/03-모델-도구-루프와-정지-조건.html` · `qa/upgrade/author_03.py` · `03-모델-도구-루프와-정지-조건.html` | **마감** | b4 「(`bind_tools`)은 Ch 19 **05절에서** 다룹니다」 → 「Ch 19 **04절부터** 다룹니다」(`mdpatch.py`로 생성기·`_src` 같이, 노트북에는 없는 문장 — 03 노트북 해시 그대로. `_src` `4adca8ae`→`5e1525c9`, 생성기 `4ae893c9`→`d4f35abc`, HTML `753f6790`→`5619596f`, 다른 Ch 17 HTML 그대로) · `verify.py --chapter` **PASS 6 sections / 147 code cells (max 13 lines)**, 03 게이트 0, `{{` 0 |
| `labs/part5/continuity-guide.md` | **마감** | 7행 「첫 번째 노트북에는 Ch 4의 `fetch_orders()` 본문과 원본 SHA-256이 함께 적혀 있습니다」(사실과 다름) → 「이 파일은 Ch 4의 `orders.csv`와 바이트 단위로 같습니다. Ch 4 실습 폴더 판 `fetch_orders()`는 도구 파일 `notebooks/order_tools.py`로 옮겨 두었고, 노트북이 이 파일에서 가져옵니다」(`59295755`→`0d0237e1`). 9행은 대조해 틀린 사실이 없어 그대로. 7행의 「입력·반환 형식」(「반환」)은 사실 문제가 아니라 그대로(Part 5 마감 몫) |
| `textbook/part5/_build_index.py` | **마감** | ch19 설명 「조회 함수를 도구로 감싸고 입력 **검증**·설명문·호출 결과를 연결합니다」 → 「조회 함수를 도구로 감싸 입력 형식과 설명을 적고, 모델이 고른 도구를 실행해 도구 메시지로 잇고, 읽기·쓰기 도구를 나눠 주문 취소 문의를 처리하는 실습을 합니다」(시수 6·10 그대로, 절 수 칸 없음, `9e1e823a`→`246d7dcc`) |
| `textbook/part5/index.html` · `textbook/downloads/part5-practice.zip` · `textbook/part5/qa/integration-results.json` | 07절 + **마감** | `python3 textbook/part5/_build_index.py` → **`Part 5: 24 verified sections; 63 bundled files`**, zip `40c10aec…` → **`72d3e3e786834387717e2d4bc7339c3219b9e920f0582bc74563b92c0f09f5a0`**(66항목, Ch 19 열둘 모두 디스크와 같음, `__pycache__` 0), `index.html` `29775f04`→`8bcdb27a`, `integration-results.json` `f0038083`→`d4b45da6` |
| `textbook/part5/qa/ch19-visual-summary.json` · `textbook/part5/qa/visual-summary.json` | **마감** | ch19 행 14 → **16**(새 결과로, `c354645b`→`9dd24120`), 합 `checks`·`passed` 58 → **60**(`134cdec3`→`b071ea4a`, 다른 챕터 파일 그대로) |
| `textbook/part5/qa/bundle-execution.json` | **마감** | `check_bundle_execution.py`가 다시 씀(`617aa4c6`→`1d109972` — 새 zip 해시, Ch 17 05·**Ch 19 01**·Ch 20 03 PASS) |
| `textbook/part5/qa/notebook-readiness.json` | **마감(되돌림)** | 옛 `check_notebook_readiness.py`가 멈추기 전에 이 파일을 다시 써서, 실행 전 사본으로 되돌렸습니다(내용 변경 0) |
| `textbook/part6/prerequisite-files.json` · `textbook/part6/ch28-mcp/qa/prerequisite-files.json` | **마감** | Ch 18 선례 모양으로 **`labs/part5/ch19-model-tools/data/orders.csv` · `notebooks/04-설명만으로-도구-선택하기.ipynb` · `notebooks/order_tools.py`**를 더함(Part 6 목록은 정렬 — `collect_public_files.py`를 쓰지 않고 흉내 낸 결과와 같음 확인). Ch 28 목록은 HTML에 **04 HTML**도 더함(03·05·06 HTML이 있던 모양). `e6605958`→`4c7f5a4b` · `e3369dfd`→`8148077e`. 잠금(`pyproject.toml`·`uv.lock`)은 더하지 않음(지시 범위) |
| `textbook/part6/qa/final-artifact-hashes.json` | **마감** | 만드는 스크립트가 없어(`grep` 0) Ch 19 줄만: 03·05·06 노트북 옛 값(`7dcb5963`·`c0888cbd`·`928d47ca`) → 지금 값(`f0d83063`·`c4d4204f`·`9c14c372`), 새 줄 셋(`data/orders.csv` `f2d1e3ee` · 04 노트북 `ac27b966` · `order_tools.py` `fa5975b5`). 356 → 359키, 다른 키 값 그대로(`74379765`→`76d3f169`). 같은 파일의 `part6-practice.zip` 줄(`bd09ba55…`, 이미 낡음)은 Ch 18 선례대로 고치지 않음 |
| `textbook/downloads/part6-practice.zip` · `textbook/part6/qa/integration-results.json` | **마감** | `python3 textbook/part6/_build_index.py` 한 번 → **`Part 6: 48 verified sections; 92 bundled files`**, zip `dacb688e…` → **`0543ea632df030bdddfb5613eb908230a1508c34c67263292f302482aa79780f`**(95항목 — 바뀐 것은 Ch 19 03·05·06 새 판과 새 항목 셋(04·`order_tools.py`·`orders.csv`), `manifest.json`뿐 — 나머지 항목의 디스크 파일은 옛 zip보다 오래됨), `integration-results.json` `764e0f99`→`8be394e0`. **`textbook/part6/index.html` 그대로** |
| `textbook/part6/qa/bundle-execution.json` | **마감** | Part 6 `check_bundle_execution.py`가 다시 씀(`27a85dc1`→`d6e1ba96` — Ch 24 01·Ch 28 01 PASS, Ch 19는 대상 아님) |
| `textbook/_notebook/checks/notebook-contracts-part5-ch19-model-tools.json` | 절마다·마감 | `verify.py --chapter`가 다시 씀(Ch 7·Ch 17 계약 파일은 같은 내용으로 다시 써져 해시 그대로) |
| `textbook/_notebook/checks/ch19-model-tools/visual-results.json`(+ 스크린숏 넷) | **마감** | `visual.cjs` 16행(`NODE_PATH=/tmp/pw/node_modules`) |
| `textbook/qa/upgrade-progress.md` · `textbook/qa/upgrade-final-checklist.md` | **마감** | Ch 19 행 한 줄 · §2-8 Ch 19 항목과 §3·§4 Ch 19 줄 |

- **고치지 않은 것**: `textbook/QUALITY-UPGRADE.md`·`PLAYBOOK.md`·과정 요약·계약 파일, 공용 도구 코드(`nbkit.py`·`mdpatch.py`·`run_section.sh`·게이트·`verify.py`·`visual.cjs`·`execute.py`·`build_bundle.py`·`render_mermaid.py`·`attach_figures.py`), Part 5·6 옛 검사 스크립트와 `check_*` 스크립트, **`textbook/_notebook/build_index.py` 42행**(Ch 19 절 수 6·제목 「LangChain Model과 Tool」 — Ch 17(5)·Ch 18(6, 「지연」)도 실습 절을 더할 때 이 파일을 고치지 않은 선례(파일 날짜 2026-09-11)라 그대로), `textbook/part5/practice-start.md`·Part 5 소개 `_src/index.html`(Ch 19 문장이 사실과 맞음), **Ch 20 이후 파일 전부**(Part 6 선행 목록 둘과 `final-artifact-hashes.json`·`part6-practice.zip` 말고 — Ch 20·22·28 `_src`·노트북·`labs/part6/continuity-guide.md`), 보호 파일 가운데 위 표 밖의 25개.
- **파일을 지운 것은 없습니다.** 옛 생성기 둘만 `mv -n`으로 옮겼습니다(§14 1번). 마감이 새로 만든 파일: `chapter-summary.md`(이 파일) · `gates-after.json` · `before/generators/blocked/` 둘(옮긴 것) · `.cache/ch19-close/`(마감 전 사본·확인 스크립트·그림 확인 사본·로그).

## 11. 기준 버전·확인 날짜

- 실습 폴더 잠금: §9. **교재 출력 환경 = 잠금 판**.
- 교재 출력: Linux aarch64 · Python **3.12.13** · 모델 `gpt-5.4-mini`(`temperature=0`·`reasoning_effort="none"`, `init_chat_model("openai:gpt-5.4-mini", …)`). 실행일 모두 2026-09-24(01 00:55 · 02 01:24 · 03 01:48 · 04 02:15 · 05 02:48 · 06 03:20 · 07 03:57 UTC).
- 참고 자료(2026-09-24 확인): LangChain Tools(독스트링 = 설명, 「Type hints are required」, `snake_case`, 권한별 도구 거르기·도구 오류 예는 **둘 다 미들웨어** — 06 b10 마감 B-7) · LangChain Models · Tool calling(`bind_tools`·`tool_call_id` 짝·`parallel_tool_calls=False`) · OpenAI Function calling(목적·매개변수·출력의 뜻, 언제 쓰는지는 시스템 메시지에) · Anthropic Define tools(하는 일·언제·매개변수·한계, 3~4문장, 서비스 이름 앞붙이기 — 03 b4 마감 A-6) · Pydantic Models · 설치판 소스 langchain-core 1.6.2(`structured.py` 289행 · `tools/base.py` 527·542~544·1088~1092·1109~1127·1269·1352·1369~1371·1390·1471·1481행) · langchain-openai 1.6.0(`chat_models/base.py` 2394·2427~2428·2435~2436행).

## 12. 강사 확인 대상

1. **제목 말**: 01 「tool」·02 「Pydantic」·「반환 스키마」·05 「bind_tools」·「병렬 호출」을 두고 본문에서 한 번씩 풂. 제목에 「병렬」을 남길지(05).
2. **도구 정의 문법을 이 챕터 주제로 허용한 범위**(맨 `@tool`·`@tool("이름")`·`@tool(args_schema=…)`·매개변수 `str` 힌트·독스트링·양식 클래스, 반환 힌트 없음) · 01 `convert_to_openai_tool`(과제 범위보다 한 걸음 더) · 도구 파일 `fetch_orders`의 `*`·`status=None`.
3. **01 삽화 `01-5`(검토 A-1)**: 다시 만들지 않고 글만 고침 — 전표의 동그라미 셋은 「설명 글의 안내」, 칠한 하나는 「고른 값」, 입력 형식은 글 한 칸(02 「빈칸 전표 = 01 도구의 입력 형식」과 이어짐). 그림(동그라미 전표)과 02의 빈칸 전표가 한눈에는 달라 보이는 점 — 01 전표를 빈 칸으로 다시 만들지(2크레딧).
4. **03 실험의 모양(검토 A-5)**: 코드는 그대로 두고 「자세한 판은 기준 낱말에 맞춰 쓴 예라 1 ↔ 4는 실행 전에 정해진 값 · 흐름을 보여 주려고 정한 예」를 b6·b7·노트북 5절 끝·정리·복습·캡션에 밝히고 표를 한 줄로 줄임. 이 절 문체가 아닌 설명 하나를 값 바꿔 보기에 넣어 낱말 검사의 한계를 출력으로 보이려면 03 재실행(모델 0).
5. **「입력 검사」 두 뜻(검토 A-4)**: 말은 그대로, 02 용어 표에 Ch 16 01과 한 문장으로 가름 · 07은 b3 표 「몸통 전 입력 검사」로 충분하다고 보고 더하지 않음.
6. **04 설계**: 공개 이름 가림·기대 도구를 이 절이 정함(B-2 문장) · 두 판이 건수 질문 하나에서만 갈림 · 값 바꿔 보기 결론을 「네 문장 전체」로 넓힘(B-1 — 사용 조건 문장만 더한 판으로 원인을 가르려면 04 재실행·요청 증가).
7. **05**: 도구 하나만 알려 준 설계 · 하나씩 흐름의 출력 토큰 합이 적은 까닭 미확인 · `ask_until_answer`가 받은 목록을 고쳐 쓰는 설계(B-3 — 풀이만 더함).
8. **06**: Before 쓰기 결함을 코드 쪽 사실로 세움(첫 응답 11번 중 1번 다름) · 쓰기 도구 흉내 · 사람 확인 값 참/거짓 하나 · **도구 속성 `handle_tool_error`(단수) ↔ Ch 20 02 `ToolNode(handle_tool_errors=…)`(복수)** · 06 노트북 파일 해시가 마감 마크다운으로 바뀜(출력·코드 그대로).
9. **07**: 붙인 조합과 뺀 것 · **모델 요청 5번**(3~5번 위 끝, 준비물 「4~5번」) · **B 실행 답 글 어긋남**(도구 없이 「취소 처리해 드릴게요」 — 지금처럼 둘째 단락·b7에 둠, 배울 점으로 올릴지) · 오류 담기 설정을 켜 두기만 함(06 셀과 글자 같게, B-9 문장으로 범위 한정) · 06 값 바꿔 보기와 같은 값을 바꾸는 설계(B-11 초점 문장만).
10. **07 삽화 `07-4`(검토 B-12)**: 다시 만들지 않고 보이는 대로 「꽂힌 전표의 아래쪽이 상자 앞면으로 비쳐 보이고 거기에 도장 자국」 한 전표로 적음 — 「그림만 보고 관계가 읽히는가」 판독과 **창의 열린 문짝이 02 덧문 소품과 가까운 점**.
11. **Part 6 묶음**: 선행 목록에 도구 파일·`orders.csv`·04를 더해 Part 6 묶음의 03은 Ch 19 가상환경으로 `notebooks/`에서 끝까지 돎(마감 확인, 27셀 PASS) — **잠금(`pyproject.toml`·`uv.lock`)은 넣지 않아** Part 6 묶음만으로는 Ch 19 패키지를 설치할 방법이 없음. 04~06은 API 키 필요. 넣을지.
12. **`chapter.json` 학습 목표 넷 → 여섯**(「반환」·「경로」·「tool_calls를 기록하고 평가」 뺌, 07 실습 줄), `hours` 그대로 16h(01~06 meta 합) · 실습 폴더 README 다시 쓴 범위.
13. **코드 줄 증가**(01 38 → 90 · 02 55 → 109 · 03 44 → 130 · 04 92 → 144 · 05 65 → 148 · 06 코드 셀 6 → 26 · 07 새 절, + 도구 파일 97줄) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘.
14. 삽화 일곱 장의 「그림만 보고 관계가 읽히는가」(01 전표 크기 · 02 별 위치 · 03 금화 = 합계 · 04 칠한 칸 · 05 걸린 전표 · 06 덧판 없는 창 · 07 위 10번) · 한국어 감사 3단(별도 세션).

## 13. 뒤 챕터 인계

### Ch 20 ToolNode가 이어받을 것

- 말: 도구·도구 설명·입력 형식·도구 명세(01) · 입력 검사(02 — Ch 16 01 뜻과 다름) · **도구 호출 요청**(04, `tool_calls` 한 건) · **도구 메시지·호출 ID·여럿 담기·도구 찾기 표**(05) · **읽기 도구·쓰기 도구·도구 오류·오류 담기 설정·결과 상태**(06) · 사람 확인 값 · 바퀴 한도(Ch 17 03) · 예상 비용(Ch 6 06 뜻).
- 사실: Ch 20 01 b2·b3 「Ch19에서는 `@tool`과 `bind_tools`로 … `tool_calls`를 해석해 도구 함수를 호출」·「`bind_tools`가 도구 스키마를 모델 요청에 포함」은 04·05로 **참** · Ch 20 02 b3 「Ch19에서는 지원 범위를 도구 docstring과 Pydantic 스키마에 적었습니다」는 02·03으로 **참** · Ch 20 04 b3 「Ch19에서는 모델 응답에 포함된 `tool_calls`를 해석했습니다」 **참** · Ch 20 01 b7 「쓰기 도구에는 별도의 권한 확인」은 06 「사람 확인 값」과 뜻이 맞음 · Ch 19 07 b8 「Ch 20에서는 도구를 실행하고 다시 묻는 반복을, Ch 13의 상태 그래프로 조립합니다」·05 b2 「Ch 20에서는 `ToolNode`가 이 실행을 맡습니다」가 Ch 20 01 b2와 맞음.

### Ch 20이 전제하면 안 되는 것 (검토 B-16 — Ch 20 파일은 고치지 않았습니다)

1. **호출 ID를 처음 가르치는 것처럼 쓰지 않기**: Ch 20 `_src/02-도구-오류와-ToolMessage.html` 2행 b1 학습 목표 「ToolMessage의 tool_call_id가 요청과 결과를 연결하는 방식을 설명할 수 있습니다」 — Ch 19 05가 이미 가르쳤습니다(용어 「호출 ID」, `tool_call_id가 요청 id와 같은가: True`, 비유 **「같은 색 집게」**, 삽화 `05-5`). Ch 20 02 5행 b4 「택배 송장 번호가 발송 요청과 배송 결과를 연결하듯 tool_call_id는 …」은 **둘째 비유**입니다 — 「Ch 19 05절에서 본 호출 ID를」로 잇고 비유를 하나로 맞추거나 한 문장으로 이어 주세요.
2. **도구 오류를 도구 메시지로 바꾸는 일을 처음처럼 쓰지 않기**: Ch 20 02 b2·b4는 처음 보이는 것처럼 적지만 Ch 19 06이 **도구 속성 `handle_tool_error = True`(단수) + `raise ToolException(…)`**으로 먼저 보였고(결과 상태 `error` 도구 메시지), 06 b4·b7은 **「`ValueError` 같은 다른 오류는 설정을 켜도 그대로 올라온다」**고 가르쳤습니다(노트북 밖 확인). Ch 20 02는 **`ToolNode(handle_tool_errors=…)`(복수)**에 오류 처리 함수를 주어 **`ValueError`를 도구 메시지로 바꿉니다**(6행 b5 「After에는 ValueError만 처리하는 handle_policy_error」·9행 b8). 학생이 어긋난 설명으로 읽지 않게 Ch 20 02 b3이나 b4에 「Ch 19 06절의 도구 속성 `handle_tool_error`는 `ToolException`만 받았다. 이 절의 `ToolNode` 인자 `handle_tool_errors`(복수)는 노드가 도구를 실행할 때 받을 오류와 처리 함수를 정한다」 뜻의 한 문장이 필요합니다(Ch 20 02 8행 b7 「`handle_tool_errors=True`처럼 모든 예외를 같은 방식으로」도 같은 자리에서 가르기).
3. **Ch 20 01 b8(9행, 다음 절 예고)**: 「다음 절에서는 ToolNode가 실행한 도구에서 오류가 발생했을 때 예외를 숨기지 않고 ToolMessage로 어떻게 전달할지」 — Ch 19 06을 잇는 말이 없습니다(「Ch 19 06절에서 도구 속성으로 한 일을 노드 쪽에서」 정도).
4. **Ch 18 금지어 「추정 비용」·「지연」**: Ch 20 02 7행 b6 「추정 비용 0.00049125달러, 지연 1.356초」 · 01 7행 b6 「추정 비용은 0.000503달러, 전체 지연은 1.963초」 · 04 2행 b1·7행 b6·5~6행 b4·9~10행 b8·b9 「추정 비용」·「지연」 · 03 3행 b2·9행 b8 「지연」 → 「예상 비용」(Ch 6 06 뜻, 청구 금액 아님)·「걸린 시간/걸린 초」. Ch 19는 걸린 시간을 재지 않았습니다.
5. **`recursion_limit` ≠ 바퀴 한도**: Ch 19의 멈춤은 평범한 Python 함수 `ask_until_answer`의 **바퀴 한도 `turn_limit`**(Ch 17 03 말, 바퀴 한 번 = 모델 요청 한 번)와 「도구 호출 요청이 없는 응답」입니다. Ch 20 03(2·4~6·8~10행) `recursion_limit`은 그래프 super-step 한도라 다른 것이라고 한 문장.
6. **Ch 19가 하지 않은 것**: `ToolNode`·그래프·`tools_condition`·`create_agent`·미들웨어·`tool_choice`·시스템 메시지·서비스 오류(429·5xx·시간 제한)·다시 보내기·걸린 시간 재기 · `ToolMessage(…)`를 직접 만들기·`handle_validation_error` · **흐름 안에서 입력 검사 `ValidationError`가 난 장면**(07은 모델 없이 직접 `invoke`로만 — 흐름 안이면 오류 담기 설정으로 받지 못해 멈춘다는 것은 소스로만, 07 b7) · 한 응답의 여러 요청을 한꺼번에 실행(05는 `for`로 차례로, 06·07은 `parallel_tool_calls=False`).
7. **도구 파일 `order_tools.py`는 Ch 19 실습 폴더 전용**입니다(Ch 20 실습 폴더에 없음, Ch 20 노트북은 자기 자료·도구를 다시 선언 — 가져오려면 Ch 20이 정함).
8. **모델 답의 흔들림**: 07의 두 흐름은 밖 5/5·새 커널 2/2 같았지만 「항상」이라 쓰지 마세요(06은 같은 첫 요청 11번 중 1번이 다름). 답 글은 흐름과 어긋나게 적을 수 있습니다(07 B).

### Ch 22 Middleware (완료 챕터 — 고치지 않음, 기록만)

- Ch 22 `_src/01-미들웨어와-6개-훅.html` 10행 b3 「Ch19에서는 함수 위에 @tool 줄을 붙여 도구로 만들었습니다」 **참**(01). Ch 22 노트북 01·04·09의 도구 `lookup_hours(day: str) -> str`은 **반환 힌트**를 씁니다 — Ch 19는 반환 힌트를 가르치지 않았습니다(01 결정: `@tool`의 반환 힌트는 입력 형식·도구 명세에 들어가지 않음 — 02 b7). Ch 22 01 「Ch16에서는 모델을 부르기 전후에 검사 함수를 직접 호출」의 검사는 Ch 16 뜻(Ch 19 02 「입력 검사」와 다름).
- Ch 22 미들웨어의 도구 오류 처리(`@wrap_tool_call` 등)는 Ch 19 06의 도구 속성 방식과 다른 자리입니다 — Ch 19 06 b10이 「LangChain Tools 문서의 권한별 도구 거르기·도구 오류 예는 모두 미들웨어, 이 절은 미들웨어 없이 `bind_tools` 앞에서 목록을 고름」으로 가름(마감 B-7).

### Ch 28 MCP (대기 챕터 — 고치지 않음, 검토 B-17·A 뒤 챕터 표)

| 자리 | 지금 문장 | Ch 19 쪽 사실 | 판정 |
|---|---|---|---|
| `textbook/part6/ch28-mcp/_src/01-MCP-구조와-capability-협상.html` 3행 b2 | 「Ch19에서는 Python 함수를 모델이 읽을 도구 스키마로 바꾸었습니다」 | 01~03 `@tool` → `convert_to_openai_tool` | 참 |
| 같은 파일 4행 b3 | 「Ch19에서 도구 이름·설명·입력 스키마가 모델 선택에 영향을 준다는 사실을 확인했습니다」 | 04는 **설명만** 바꿨고(공개 이름은 두 판 모두 `tool_a`… 로 가림, 입력 형식은 같게 둔 통제 변수) 건수 질문 하나에서 선택이 갈림. 03은 모델 없음 | **부분 참** — 「도구 설명이 모델의 선택을 바꿀 수 있다는 것을 확인」으로 좁힐 것 |
| `02-FastMCP-로컬-서버-제작.html` 4행 b3 | 「Ch4에서 함수와 타입 힌트를, Ch19에서 @tool 장식자와 입력 스키마를 배웠습니다」 | 타입힌트는 Ch 2 07이 가르침(Ch 4 아님). Ch 19 말은 「데코레이터 줄」(01)·「입력 형식」 — 「장식자」 0건 | Ch 28 몫(말·출처) |
| `04-LangChain-MCP-클라이언트-연동.html` 4행 b3 | 「Ch19에서 @tool로 만든 BaseTool의 name, description, args_schema를 모델에 연결했습니다」 | 뜻은 04로 참. Ch 19는 `BaseTool`이라는 이름을 쓰지 않음(종류 `StructuredTool`, `_src` 0건), `args_schema`는 02 | 참(말 한 곳) |
| `05-도구-정의와-첫-호출-토큰.html` 3행 b2 | 「Ch19에서 도구 개수가 늘면 선택 정보가 커진다는 사실을 배웠습니다」 | 03 6절 **명세 글자 수**로만(`309`→`610`→`923`, 토큰이라 하지 않음) | 글자 수로 참 — 「토큰」으로 읽히지 않게 |
| 같은 파일 4행 b3 | 「Ch19에서 bind_tools가 도구 설명을 모델 요청에 포함시키고 usage_metadata가 입력·출력 토큰을 제공한다는 사실을 확인」 | 04(첫 `bind_tools`, 설명 길이에 따른 입력 토큰 `177` → `330`)·05(`sum_usage`) | 참 — **이 장면이 04에 있어 Part 6 선행 목록에 04를 더함**(B-15) |

- Part 6 묶음: 마감에서 Ch 19 03·04·05·06 노트북 + `order_tools.py` + `data/orders.csv`가 들어갔습니다(§10). 잠금은 없습니다. `labs/part6/continuity-guide.md` 14행 「Ch19의 도구 정의와 호출 비용 → Ch28」은 참.

## 14. 남은 것 (전체 마감 몫 — `textbook/qa/upgrade-final-checklist.md` §2-8)

1. **옛 생성기 둘은 옮겼습니다(삭제 아님, 2026-09-24 완료)**: `textbook/part5/ch19-model-tools/_make_sources.py`(`8fcb94d3…`)·`figures/_gen_figures.py`(`348b928d…`, 모두 01절이 `raise SystemExit`로 막은 판) → `qa/upgrade/before/generators/blocked/`(원본 사본 `before/generators/`, 옮기기 전후 해시 같음). 부르는 스크립트 없음(`grep` 0), 옮긴 뒤 `_build.py` HTML 여덟 개 해시 같음.
2. **옛 그림 열여덟 삭제 승인**: `figures/0N-…-flow.{svg,excalidraw,caption.md}`(01~06절 각 셋, 본문 참조 0, `05-…-flow.caption.md`에 「순차」·「반환」 남음, 사본 `qa/upgrade/before/figures/`).
3. **`gates-wip-*.json` 열넷 삭제 승인**(`gates-after.json` 7/7로 갈음 — 마감의 `run_section.sh --no-exec` 일곱 번이 `gates-wip-01~07.json`을 끝 값으로 다시 씀).
4. **자리 찾기 셀 `assert` 안내 글(01~07 코드 셀, 검토 A-11·B-14)**: 「notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요」 → 다음 재실행 때 `author_01~07.py`에서 「notebooks 폴더에서」로(지금은 결과 읽기 한 문장이 바로잡음, 생성기 코드는 노트북과 같게 그대로).
5. **Part 5 옛 검사 스크립트 넷(고치지 않음, 마감에서 돌려 본 결과)**: `check_scope.py` — Ch 17 `06-Agent-개요-실습.html` meta 「실습 30분」에서 `Missing scope`(Ch 19 07도 같은 모양, `SECTION_COUNTS` ch19 = 6 ≠ 7) · `check_figures.py` — Ch 17 `01-1-고른-쪽으로-가르기.svg`의 `.excalidraw` 짝 요구에서 멈춤 · `check_notebook_readiness.py` — `assert len(reports) == 21`(지금 Part 5 노트북 24)에서 멈춤, **결과 파일을 먼저 씀 → 되돌림**(함수 타입힌트 필수 규칙도 Ch 19와 맞지 않음) · `finalize_evidence.py` — Ch 18 `_src/01-게이트가-있는-프롬프트-체이닝.html` 감사 해시에서 멈춤. 모두 Ch 19에 닿기 전에 멈춥니다.
6. **`llm-practice.zip`**: Part 5·6 `check_delivery.py`가 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`(Part 5 115행 · Part 6 117행)에서 멈춤(결과 파일 안 바뀜). 사본에서 `llm-practice.zip`만 빼고 결과 파일 없이 돌리면 **Part 5**: HTML 30 · 링크 503 · 누락 0 · 복습 97문항 오류 0 · 비밀값 0 · `part5-practice.zip` 66항목(part5 노트북 24) 통과 / **Part 6**: HTML 59 · 링크 877 · 누락 0 · 복습 175문항 오류 0 · 비밀값 0 · `part6-practice.zip` 95항목(part6 노트북 48) 통과.
7. **`textbook/_notebook/build_index.py` 42행**(Ch 19 절 수 6·제목 「LangChain Model과 Tool」·설명) — 전체 목차 마감 때 `chapter.json` 「모델과 도구」·`textbook/part5/_build_index.py` 새 설명과 맞출 것(Ch 17·18 선례대로 이번에는 고치지 않음).
8. **Ch 28 문장 다섯**(§13 표) · **Ch 20 문장**(§13 1~5번) — 그 챕터 개선 때.
9. **Part 6 묶음 잠금**(§12 11번) · `final-artifact-hashes.json`의 `part6-practice.zip` 줄(이미 낡음, Ch 18도 그대로 둠).
10. **`qa/research.md`**(2026-09-10 조사)와 `qa/verification.md`·`집필점검표.md` 위쪽 옛 줄: 학생 묶음 밖 기록이라 그대로(「개선 전 판」 표시). `qa/upgrade/review-pack/`은 마감 전 판(검토에 쓴 묶음 — 다시 만들지 않음).
11. **과정 요약·계약 파일(누적 문서 몫)**: Ch 19 용어(§4, 특히 「입력 검사」 두 뜻 · 「호출 ID」 비유 「같은 색 집게」 · 「오류 담기 설정」 = 도구 속성 단수) · 도구 파일 `order_tools.py` 줄 · Part 6 선행 목록 추가는 과정 요약·`upgrade-contracts.md`에 아직 넣지 않았습니다(Part 5 마감 오케스트레이터 몫).
12. **삭제 승인 대상(캐시·임시)**: `labs/part5/ch19-model-tools/.venv`(macOS 판 243MB)·`.ruff_cache` · `__pycache__` 셋(`labs/…/notebooks/`·`textbook/…/qa/upgrade/`·`qa/upgrade/probe/`) · `.cache/ch19-01-view`~`ch19-07-view` · `.cache/ch19-close`(마감 전 사본·확인 스크립트·그림 확인 사본·로그) · `.cache/vm/venv-ch19-model-tools`(382MB) · 기기 `/tmp/ch19-prep`·`/tmp/ch19-01`~`/tmp/ch19-07`·`/tmp/ch19-close-p6.*`(마감의 Part 6 묶음 풀기)·`/tmp/reviewA19`·`/tmp/reviewB19`.
13. **2차 검토**: 검토 둘의 「확인하지 못한 것」(삽화 판독, 한국어 감사 3단)과 §12.

## 15. 검토 1차와 반영 (2026-09-24 마감)

- 판정: **A(01~03·공통) 중 4 · 하 8**, **B(04~07) 중 4 · 하 13**(모두 accept with fixes/작은 고침 뒤 통과, 상 0).
- **[중] 8건 반영**: A-1(01 삽화 글 — 다시 만들지 않음, 02 짝 문장) · A-4(02 용어 표 한 문장) · A-5(03 「실행 전에 정해진 값」·「흐름을 보여 주려고 정한 예」, 표 한 줄, 코드 그대로) · A-9·B-13(실습 폴더 README 전체) · B-1(04 결론 「네 문장 전체」, 04 재실행 안 함) · B-3(05·06 `ask_until_answer` 풀이) · B-9(07 b7 흐름 안 입력 검사 오류, [22] 읽기 도구 한정).
- **[하] 반영**: A-2(01 b3 Ch 17 `run_tool`) · A-3(01 `dtype` 차이 조건) · A-6(03 b2 「모으면 넷」·서비스 이름 앞붙이기) · A-7(03 비유 대응) · A-8(03·04·05·06·07 복습 해설의 「b숫자」 → 화면 이름, 03 「이 절 2절」) · A-10(도구 파일 주석 — 해시 `fa5975b5…`) · A-11·B-14(01~07 자리 찾기 결과 읽기 두 문장) · A-12(01 노트북·b3·README 「Ch 2 07 모듈과 다른 파일」) · B-2(04 b7 한 문장) · B-4(05 b10 행 번호) · B-5(06 소제목 5) · B-6(06 「흐름 끝 표지」 풀어 씀) · B-7(06 b10 미들웨어) · B-8(06-3 캡션·[38] 「이번에는 실행하지 않았습니다」) · B-10(07 b3 「범위로 어림」) · B-11(07 b2 초점 문장) · B-12(07 삽화 글 — 다시 만들지 않음) · B-15(Part 6 선행 목록 둘에 도구 파일·CSV·04, `final-artifact-hashes.json`, `part6-practice.zip`) · **B-16(Ch 20 몫)·B-17(Ch 28 몫)은 그 챕터 파일을 고치지 않고 §13에 자리·문장·Ch 19 쪽 사실로 기록**. 알려진 마감 몫(Ch 7 05·Ch 17 03 문장 · `chapter.json` objectives · Part 5 목차 설명 · `continuity-guide.md` 7행)도 반영.
- **미반영(부분)과 까닭**: **A-11·B-14의 `assert` 안내 글 자체** — 코드 셀이라 고치면 `code_sha256`이 실행 기록과 어긋남 → 결과 읽기 한 문장으로 바로잡고 다음 재실행 몫(§14 4번). **A-1·B-12의 삽화 다시 만들기** — 챕터 리드 결정으로 글만(강사 확인 §12 3·10번). **A-5의 코드 갈래(다른 문체 설명을 값 바꿔 보기에)** — 03 재실행이 필요해 글 갈래로(§12 4번). **B-1의 「사용 조건 문장만 더한 판을 새로 돌려 원인 가르기」 갈래** — 04 재실행·요청 증가라 문장만(§12 6번). **A-4의 07 한 구절** — 07 b3 표·b4가 이미 자리를 밝혀 더하지 않음. **07 B 실행 답 글 어긋남·07 요청 5번** — 챕터 리드 결정대로 그대로(강사 확인). **07 오류 담기 설정 셀** — 06 셀과 글자 같게 유지(B-9 문장으로 범위 한정).
- **노트북 해시 전후**(`code_sha256` / `outputs_sha256`, 앞 12자, **모두 그대로**): 01 `acf002bdaf50`/`990530ef6fb2` · 02 `a00c3c75f4a3`/`0ba214225b49` · 03 `9cfb2f16c41e`/`d96e6d3d3bc8` · 04 `da619d3726ab`/`ad532a44b091` · 05 `211aeaae50c9`/`59c3b9f17d0a` · 06 `87a30720b3e2`/`0271e22d7387` · 07 `5cbee6c49167`/`5d08a908edf7`. 일곱 노트북 모두 `metadata.verification`과 다시 계산한 값이 같고 `executed_at` 그대로, 셀 수 그대로(50·50·57·59·57·61·51), 바뀐 것은 마크다운뿐. 노트북 파일 해시는 마크다운 때문에 바뀜(§10 첫 줄, **06 `f3d5351a…` → `9c14c372e2e298bc118d668486fab813371129da228ff34a5abe95daedde43c2`**).
- 고친 방법: `mdpatch.py`로 생성기·노트북 마크다운·`_src`를 같이(적용 전 대조 스크립트로 **코드 셀 0회**·생성기 횟수 확인, 두 번째 묶음은 G6 「5문장 넘는 단락」 다섯 곳을 빈 줄로 나눔) → `run_section.sh … NN --no-exec` 일곱 번 → 캡션 파일 넷(`01-5`·`03-3`·`06-3`·`07-4`)을 `_src`와 같게 → 도구 파일 주석 한 줄. **`.mmd` 다시 렌더 0장**(글·캡션만 바뀜), 노트북 첨부 PNG 그대로. 삽화 두 장(`01-5`·`07-4`)과 `02-5`는 PNG를 다른 이름으로 복사해 직접 보고 그림 읽기를 고침. 마감 뒤 생성기 `author_01~07.py`의 `cells()`·`SRC_HTML`/`src_html()`이 노트북·`_src`와 글자까지 같음(7/7). 새로 더한 노트북 문장 43줄·`_src` 문장의 금지어 0(링크 파일 이름 말고).
- **보호 파일 39개**(`before-manifest.json`): **25개 같음 · 14개 바뀜** — 모두 의도한 것: Ch 7 05 `_src` · Ch 17 03 `_src` · `labs/part5/continuity-guide.md` · Ch 19 03·05·06 노트북과 빌드 HTML(여섯) · Part 6 선행 목록 둘 · `final-artifact-hashes.json` · `part5-practice.zip` · `part6-practice.zip`. Ch 28 `_src` 넷·`labs/part6/continuity-guide.md`·Ch 22 01·Ch 18 07·Ch 2·4·8 파일·`verify.py`·테스트·`check_bundle_execution.py`는 그대로.
- 검사: `upgrade_gates.py … --label after` **7/7 PASS, G1~G7 0** · AST 따로(06 판 `extra_check.py`) — 걸린 것은 허용 예외뿐(02·07 양식 클래스·`@tool(args_schema=…)`, 04 `@tool("tool_a")` 모양, 도구 파일 `status=None`·`.get`) · `verify.py --chapter` **PASS 7 sections / 171 code cells (max 13 lines)**(Ch 7 PASS 9/179 · Ch 17 PASS 6/147) · 빌드 HTML 여덟 개 `{{` **0건** · `visual.cjs` **16행 PASS** · Part 5 `check_bundle_execution.py` **PASS**(Ch 17 05 · **Ch 19 01 21셀, `code_sha256` 같음, `notebooks/`에서** · Ch 20 03) · Part 6 `check_bundle_execution.py` **PASS**(Ch 24 01 · Ch 28 01) · Part 6 묶음의 Ch 19 03을 Ch 19 가상환경으로 `notebooks/`에서 새 커널 실행 **PASS 27셀**(`찾은 프로젝트 맨 위: ../../../..`, 추가 확인).
