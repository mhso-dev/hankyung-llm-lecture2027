# 04절 진단과 개선 기록 — 0.x에서 1.x로 마이그레이션 (experiment)

- 대상: `_src/04-0x에서-1x로-마이그레이션.html` · `labs/part6/ch21-create-agent/notebooks/04-0x에서-1x로-마이그레이션.ipynb` · 그림 `figures/04-1`~`04-5` · `chapter.json` 절 제목 글자.
- 생성기: `qa/upgrade/author_04.py`(노트북 + `_src`, `20c1b6a5…`). 모델 없는 확인: `probe/check04_graph_shapes.py`·`probe/check04_warning_stderr.py`(요청 0). 그림 설계표: `qa/upgrade/04-figures.md`. 검토 묶음: `qa/upgrade/review-pack/04-0x에서-1x로-마이그레이션.md`.
- 작업일 2026-09-25(UTC 03:4x~04:1x). 형식 **experiment 유지**, **슬러그 그대로**(01·02·03 b8·생성기 `L_04`가 링크), 제목 글자만 고침(§3).
- **모델 요청 0번**(노트북·노트북 밖 모두). 흔들림 확인 대상이 없어 `04-probe.md`는 만들지 않았습니다.

## 1. 게이트 전후

| | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전 (`gates-before.json`) | 5 | 64 | 0 | 1 | 0 | 0 | 7 | 20 | 3 | **31** |
| 첫 실행 전 (`/tmp/ch21-04/gates-wip-04-04.first.json`, 노트북만 쓴 판) | 24 | 348 | 0 | 0 | 0 | 0 | 0 | 1 | 18 | — |
| 후 (`gates-wip-04.json`·`gates-wip-04-04.json`) | **24** | **354** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G1·G2는 **0**(과제 지시대로 첫 실행 전에 먼저 검사). G6 1 = b4 「비교와 경계」 한 문장 70자 초과 → 둘로 나눔. G7 18 = 그림 파일·설계표가 아직 없던 때의 값. `gates-wip-04-04.json`은 고친 뒤 같은 이름으로 다시 검사한 0 판입니다.
- AST 따로(`/tmp/ch21-04/extra_check.py` — 03 판에 `with warnings.catch_warnings(…)` 블록·`issubclass`·`inspect.signature`를 **허용 표시로 따로 출력**하게 더함): 노트북 **위반 0건**(허용 표시 6줄 — `cell17` `inspect.signature` 둘 · `cell21`·`cell25`·`cell39` `with warnings.catch_warnings(record=True)` · `cell23` `issubclass`), 도구 파일 2건 = `estimate_cost`의 `.get` 둘(Ch 6 06 원본 예외, 01~03과 같음). 클래스는 `PolicyAnswer(BaseModel)` 하나(02 셀 그대로, G1 허용 모양), 데코레이터는 맨 `@tool` 하나, f-string·내포식·`lambda`·조건 표현식·기본값·반환 힌트·튜플 풀기·`elif`·`+=` 0.
- 금지어(`/tmp/ch21-04/ban_check.py` — 03 판 + 「마이그레이션」·「v1」·「이주」·「로그인」): 노트북·`_src`·캡션 다섯·`.mmd` 넷에서 **6건 = 「마이그레이션」 5**(노트북 제목 셀 · 노트북 1절 풀이 한 곳 · `_src` 머리 meta의 슬러그 · `_src` b2 풀이 한 곳 · b4 용어 표 「옮기기(마이그레이션, migration)」) **· 「v1」 1**(b10 참고 자료 영문 원제목 「LangChain v1 migration guide」). 모두 제목 말 풀이·원제목 자리. 첫 판의 「임시 파일 경로」 2건은 「임시 파일 위치」로 고침(`mdpatch.py`). 「한 겹 더」 0건.
- 코드 줄(`count_code.py`) 30 → **142**(셀 5 → 24). 준비 셀이 아닌 셀의 주석 뺀 코드 최대 **9줄**(`OLD_FORM`), 함수 본문 최대 **4줄**(`print_arrow_lines`), 셀당 정의 하나, 첫 줄 주석 100%.

## 2. 수정 전 주요 문제 (준비 노트 §2 04·§7-6, 인계 §03 → §04)

1. **옛 API를 실행하지 않고 표 글자만**: 대응표 네 줄을 코드에 적어 출력(f-string 형식 지정 `f"{old:28} -> …"` · 한 줄 복합문 `for …: print(…)`(G2) · 튜플 풀기). 출력이 확인한 것이 아니라 우리가 적은 글.
2. **대응표 셋째 줄 사실과 다름**: 「response_format 별도 후처리 → response_format」 — 옛 함수도 `response_format`을 받았고, 루프가 끝난 뒤 노드 `generate_structured_response`에서 모델 요청을 한 번 더 함(설치판 소스 744~767행·그래프 출력). 넷째 줄 「Pydantic 사용자 상태 → TypedDict」는 공식 안내에만 있는 사실(노트북에서 확인 안 함).
3. **`inspect.signature(create_agent)` 약 900자 한 줄 출력** + 「글자 안에 이름이 있는가」 `assert` 여섯 — `inspect`는 과정 처음, 긴 출력은 읽기 어려움.
4. **모델 이름 글자·일반 질문**: `create_agent("openai:gpt-5.4-mini", [], …)`(temperature·reasoning_effort 없음) · 질문 「마이그레이션에서 먼저 고정할 것은 무엇인가요?」는 이 절 관찰과 무관 · 답 글 `assert`(모델 글).
5. **틀린 전제·틀 문장**: b3 「Ch20의 직접 조립 그래프를 사용합니다」(사용 안 함) · b3 「필요한 자료와 객체는 노트북에서 다시 선언하므로 …」 · b6 = 확인할 점 = b8(같은 글 세 번) · b7 「절당 1달러 미만」·「모델 문장과 지연」 · b8 「05-retriever를-도구로-전환에서 이 결과를 다시 사용합니다」(05가 04 결과를 쓰지 않음) · 결과 읽기 셀 0 · 옛 그림 `{{svg:04-흐름}}` 한 장.
6. **금지어·말**(옛 `_src`·노트북, `ban_check.py`): 「v1」 13 · 「마이그레이션」 6(제목 말을 본문에 되풀이) · 「반환」 3 · 「경로」 3 · 「지시」 2 · 「프롬프트」 2 · 「필드」 2 · 「지연」 1 · 영문으로 시작해 조사가 붙은 문장·70자 넘는 문장(G6 20).
7. **제목 표기**: `chapter.json` 「0x에서 1x로 마이그레이션」(점 빠짐 — 옛 생성기 `_author_ch21_ch29.py` 435행은 「0.x에서 1.x로 마이그레이션」이었음).

## 3. 바꾼 것

- **0.x는 실행하지 않고, 1.x에 남은 옛 함수로 그래프 모양만 견줌(챕터 리드 결정)**: 잠금(`uv.lock`)에 langgraph 0.x가 없어 0.x 판은 실행 불가 → 준비물·b4 「비교와 경계」·b7 첫 줄에 「0.x 판은 실행하지 않았습니다」, 「0.x 판에서도 모양이 같았는지는 확인하지 않았습니다」. 설치판 langgraph-prebuilt 1.1.0의 `from langgraph.prebuilt import create_react_agent`로 **01절과 같은 모델 객체·`lookup_policy`·01 시스템 메시지 글**(생성기 `check_same_as_before()`가 01 `AGENT`의 `system_text` 줄과 한 줄 통째로 대조)을 넘겨 그래프를 만들고, 새 함수 `create_agent`와 같은 셀 모양으로 출력.
- **모델 요청 0**: 그래프를 만들기만 하고 `invoke`하지 않음(새 API 실행은 01~03이 보임). 모델 객체는 키가 있어야 만들어져(`env -u OPENAI_API_KEY`로 가짜 키 없이 `init_chat_model(…)` → `OpenAIError: Missing credentials` — `check04_graph_shapes.py`) 키 셀·모델 셀은 둠. 모델 셀은 `nbkit.model_source()` 그대로, 결과 읽기만 「이 모델에게 보낸 요청은 없습니다」로(과정 표준 `key_and_model_cells()`의 「이 모델로 실행한 결과」 문장이 이 절에 맞지 않아 셀을 직접 조립 — 코드 셀 글자는 같음).
- **인자 이름은 해당 이름만 출력**: `inspect.signature(…).parameters`를 목록으로 모아 앞 두 자리 `['model', 'tools']`(두 함수 같음)와 견줄 이름 여덟(`prompt`·`system_prompt`·`pre_model_hook`·`post_model_hook`·`middleware`·`response_format`·`state_schema`·`context_schema`)이 있는지 `True/False`로. `inspect`·`warnings`는 가져오기 셀 설명에 「Python에 들어 있는 기능 묶음」 한 문장, `inspect.signature`·`parameters`는 쓰는 자리에 한 문장씩.
- **사용 중단 경고를 출력으로**: 경고를 그대로 두면 셀 stderr에 `…/tmp/ipykernel_6/3132417751.py:1: LangGraphDeprecatedSinceV10: …`처럼 **실행한 컴퓨터의 임시 파일 위치**가 찍힘(노트북 밖 nbclient 확인 — `check04_warning_stderr.py`, 같은 셀 두 번에 두 번) → 새 커널 두 번의 출력이 같도록 `with warnings.catch_warnings(record=True)` + `warnings.simplefilter("always")`로 모아 `받은 경고 수: 1`·`경고 종류: LangGraphDeprecatedSinceV10`·`사용 중단 경고의 한 종류인가: True`(`issubclass(…, DeprecationWarning)`)·경고 글을 출력. 블록 `with`는 Ch 2 05절(`with open`)로 이음. 새 함수도 같은 블록으로 `받은 경고 수: 0`. 경고 글은 영어라 결과 읽기에서 풀어 씀(「옮겨졌다」·「`langchain.agents`에서 `create_agent`를 가져오라」·「1.0에서 사용을 멈췄고 경고 글에 따르면 2.0에서 없어질 예정」).
- **그래프 모양 비교(03이 요청 0으로 미리 본 값을 노트북 출력으로 다시 확인 — 모두 같음)**: 노드 `['agent', 'tools']` ↔ `['model', 'tools']` · 화살표 줄(새 함수 `print_arrow_lines` — 구조 문자열에서 `-->`·`-.->`가 든 줄만) 되돌아가는 엣지 `tools --> agent;`(실선) ↔ `tools -.-> model;`(점선) · 고정 엣지 수 `2` ↔ `1` · 조건 함수 `should_continue`(갈 곳 `['tools', '__end__']`) ↔ `tools_to_model`·`model_to_tools`(01과 같음) · 상태 칸 `['messages']` ↔ `['messages', 'jump_to', 'structured_response']` · 그래프가 채우는 값(속성 `managed`) `['remaining_steps']` ↔ `[]` · 입력 칸(`get_input_jsonschema()["properties"]`) `['messages', 'remaining_steps']` ↔ `['messages']`. 옛 그래프의 화살표 네 줄은 `agent`를 `model`로 바꾸면 **Ch 20 01절 노트북 출력의 화살표 네 줄과 글자까지 같음**(문자열 대조).
- **값 바꿔 보기 = 두 함수에 02절 양식 클래스 `PolicyAnswer`를 `response_format`으로 더 넘김**(02 `DEF_FORM` 셀 문자열 대조): 옛 그래프만 노드 `generate_structured_response` 더해짐, `should_continue` 갈 곳 `['tools', 'generate_structured_response']`(끝으로 바로 가지 않음), 화살표 `generate_structured_response --> __end__;`(실선이지만 고정 엣지 수는 `2` 그대로 — 소스 900~915행에 이 노드에서 나가는 엣지를 적는 줄이 없음, 「흐름이 끝나는 자리를 그린 것으로 보입니다」로 한정), 상태 칸 `['messages', 'structured_response']`·입력 칸 `[…, 'remaining_steps', 'structured_response']`. 새 그래프는 노드 그대로, `tools -.-> __end__;`·`model -.-> model;`이 더해짐 — 조건 함수 출력이 **02절 11절(`auto_agent`) 출력과 같음**. `assert`는 노드 목록(함수가 정하는 값)에만 둘.
- **대응표는 출력으로 확인한 줄만(챕터 리드 결정)** — 노트북 9절 목록과 b6 표 일곱 줄: 가져오는 줄(5절 경고 글) · `prompt` → `system_prompt`(4절·5절) · 훅 인자 둘 → 없음/`middleware`(4절, 옮기는 법은 Ch 22) · 양식 — 이름 같음, 옛 함수만 노드를 더함(8절) · 모델 노드 이름 `agent` → `model`(6절) · 되돌아가는 엣지 고정 → 조건부(6절) · 입력 칸 `remaining_steps` 옛 그래프에만(7절).
  - **옛 셋째 줄 고침**: 「response_format 별도 후처리」 → 「옛 함수는 루프 뒤 노드 `generate_structured_response`를 더함(8절 출력) · 그 노드가 모델에게 한 번 더 요청하는 것은 소스(744~767행)로만」.
  - **옛 넷째 줄 뺌**: 「Pydantic 사용자 상태 → TypedDict」는 공식 옮기기 안내(「`create_agent` only supports `TypedDict` for state schemas」)에만 있고 노트북에서 실행하지 않아 대응표에서 빼고 b7 한 줄로.
  - 옛 첫째·둘째 줄은 출력(경고 글·인자 줄)으로 확인해 남김.
- **제목**: `chapter.json` 절 제목 **글자만** 「0x에서 1x로 마이그레이션」 → **「0.x에서 1.x로 마이그레이션」**, 슬러그 `04-0x에서-1x로-마이그레이션` 그대로. 노트북 제목 셀·빌드 HTML `<title>`·챕터 목차·03/05 이웃 절 링크 글자가 새 글자(빌드 확인, 옛 글자 0건). 「마이그레이션」은 제목 말 — 노트북 1절·`_src` b2 첫 자리에서 「옛 판에서 쓴 코드를 새 판에서 돌도록 옮겨 쓰는 일」로 풀고 본문은 「옮기기」(용어 표). **`textbook/part6/index.html`(Part 목차)은 다시 만들지 않음** — `_build_index.py`는 묶음 zip도 다시 쓰므로 마감 몫(지금 Part 목차에는 옛 글자 「0x에서 1x로」).
- **용어 셋**(meta 「새 용어 5」 → 3): 옮기기(마이그레이션, migration) · 옛 함수(create_react_agent) · 사용 중단 경고(DeprecationWarning). 일반 말: 그래프가 채우는 값(`managed`)·화살표 줄·입력 칸·인자 이름·경고 글.
- **본문 10블록 다시 씀**: 비유 「세탁기」 04(같은 수건을 빠는 옛 세탁기와 새 세탁기, 옛 기계에만 관으로 이어진 칸) · 용어 표 · 그림 넷 + 삽화 · b6 표 둘(그래프 넷의 모양 · 옛 코드 → 새 코드) · b7 열한 줄 · 복습 넷 · 참고 자료 열한 줄(공식 옮기기 안내 둘 2026-09-25 확인 + 설치판 소스 행 번호). 제작 이력 문장 0. 옛 그림 `figures/04-흐름.*`은 그대로(본문 참조 0).
- **b8 다음 절 문장**: 「05절에서는 문서를 찾는 검색을 도구로 바꿔 에이전트 그래프에 넣습니다.」(05 설계를 묶지 않게 제목 뜻만 — 인계 §04 → §05 1항).

## 4. 새 커널 두 번 (규격 §2-7 9번 끝)

- A `run_section.sh`(셀 실행 기록 03:58:09.28~03:58:11.51Z, 약 2.2초 — 설치 셀이 이미 설치된 판이라 0.7초) · B 사본 `/tmp/ch21-04/B.ipynb`를 `execute.py`로(03:58:38.49~03:58:40.50Z, `UV_…`·`PYTHONPATH=…/notebooks`). **그림 그리기 전에 두 번 모두 실행**.
- `code_sha256` `ba1d0a4506cf…` 둘 다 · **셀별 출력 글자 24/24 같음** · `outputs_sha256` 둘 다 **`ad1cedfe20eb…`**(교재 출력 = A). 모델 요청이 없어 모든 값이 결론·그림·정리·복습에 쓸 수 있는 값입니다. 출력에 stderr 0(경고를 모았기 때문).
- 설명만 고친 세 번(`mdpatch.py` — 준비물 시간 「10초 안에」 → 「5초 안에」, 「임시 파일 경로」 → 「위치」, 준비물 파일 문장)은 `--no-exec`로, 노트북 출력은 A 그대로(대조 24/24, `outputs_sha256` 같음).
- 모델 없는 확인 `check04_graph_shapes.py`는 `PYTHONHASHSEED` 1·2·3·4·5·99에서 출력 md5가 같음(구조 문자열 줄 차례가 해시 씨앗에 흔들리지 않음).

## 5. 도구 파일 `notebooks/runner_tools.py`

- **바꾸지 않음**(`6ce7a8d29a2f96a9aa48d61ace68811932920f0d69fa3b758962809c39770471` 그대로). 04가 가져오는 것은 `print_branches` 하나(02 `DEF_BRANCHES`와 AST 같음을 `check_same_as_before()`가 실행마다 대조). 준비 셀 결과 읽기에 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 …」 + 배운 곳.
- 이 절 노트북에서 처음 적은 함수 `print_arrow_lines(graph_agent)`(구조 문자열에서 화살표 줄만 출력) — 뒤 절이 쓰면 `# Ch 21 04절에서 배웠습니다`로 옮길 것(인계).

## 6. 옛 함수 ↔ 새 함수 비교 요약 (보고용, 모두 노트북 출력 — 소스로만 본 것은 표시)

| 항목 | 옛 함수 `create_react_agent` | 새 함수 `create_agent` |
|---|---|---|
| 경고 | `받은 경고 수: 1`(부를 때마다 — 8절에서도 1) · `LangGraphDeprecatedSinceV10`(`DeprecationWarning` 자식 `True`) | `0` |
| 시스템 메시지 글 인자 | `prompt`(새 함수에 없음) | `system_prompt`(옛 함수에 없음) |
| 훅 인자 | `pre_model_hook`·`post_model_hook` | 없음 · `middleware` |
| 노드 | `['agent', 'tools']` | `['model', 'tools']` |
| 되돌아가는 엣지 | `tools --> agent;` 실선 · 고정 엣지 수 `2` | `tools -.-> model;` 점선 · 고정 엣지 수 `1` |
| 조건 함수 | `agent | should_continue | ['tools', '__end__']` | `tools_to_model` `['model']` · `model_to_tools` `['tools', '__end__']` |
| 상태 칸 / 채우는 값 | `['messages']` / `['remaining_steps']` | `['messages', 'jump_to', 'structured_response']` / `[]` |
| 입력 칸 | `['messages', 'remaining_steps']` | `['messages']` |
| 양식을 넘기면 노드 | `+ generate_structured_response`(루프 뒤 모델 요청 한 번 더 — **소스로만** 744~767행) | 그대로 `['model', 'tools']` |
| 양식을 넘기면 갈래 | `should_continue` → `['tools', 'generate_structured_response']` · `generate_structured_response --> __end__;`(실선, 고정 엣지 수 그대로 `2`) | `tools_to_model` `['model', '__end__']` · `model_to_tools` `['tools', '__end__', 'model']`(02 11절과 같음) |
| 양식을 넘기면 칸 | 상태 `['messages', 'structured_response']` · 입력 `[…, 'remaining_steps', 'structured_response']` | 상태 그대로 · 입력 `['messages']` |
| `remaining_steps`로 멈추는 동작 | 남은 단계가 둘보다 적고 도구 요청이 오면 멈추는 글(**소스로만** 620~633·684~692행) | 없음(칸이 없음) |

- **실행하지 않은 것**(b7): 0.x 판 · 두 그래프의 `invoke`(모델 요청) · `generate_structured_response`의 요청 · `remaining_steps`로 멈추기 · 옛 함수의 Pydantic 상태 형식 · 스트리밍 노드 이름(Ch 25) · `ToolNode`를 도구 목록에 넘기기 · 훅 → 미들웨어(Ch 22) · 다른 예제를 옮겨 보기.

## 7. 그림

- Mermaid **4장**(`04-1` flowchart TB + subgraph 둘(위아래) 699.8 · `04-2` flowchart TB + subgraph 둘 + 공통 상자 588.5 · `04-3` flowchart TB + subgraph 둘(위아래) 518.8 · `04-4` flowchart TB + subgraph 둘(위아래) 639.8, 모두 868 이하), **빨강 0 · 보라 0**(모델을 부르지 않음), 초록 `system_text` 하나, 파랑은 우리가 적은 인자 둘, 노랑은 출력 값, 회색은 라이브러리 노드·두 칸 공통·소스로만 본 동작(「소스 확인 ·」). PNG 넷을 직접 열어 봄(`.cache/ch21-04-view/`). 첫 렌더에서 저절로 꺾인 라벨(`04-2` 「system_prompt=system_t / ext」·`04-3` 회색 상자 「오면」 한 줄·`04-4` 「generate_structured_resp / onse」)을 `<br>`로 미리 나누고, `04-4`는 첫 줄 `%%{init: {"flowchart": {"wrappingWidth": 320}}}%%`로 노드 이름이 꺾이지 않게 함(렌더 둘째 판). 조건 함수는 상자로 그리지 않고 점선 라벨로만, 가상 시작점은 그리지 않음(01-2 선례, 도식 읽기에 한 문장).
- 삽화 **1장** `04-5-같은-빨래를-하는-옛-세탁기와-새-세탁기`(비유 계열 **「세탁기」** 04 — 옛 기계에만 관으로 이어진 회색 칸) — **1차 job `99f146c5-960e-4444-b4c8-4836dcbce80d` 채택**, 재생성 0, **2크레딧**(거래 2026-09-25T04:00:15Z 「Nano Banana Pro −2」, 생성 전 잔액 2457.75, 바로 앞 거래 03:28:19Z는 03절 몫). 응답 모델 이름 표시 `nano_banana_2`(01~03과 같음). 원본 `74eeeab6…`(2752 × 1536) → 저장 `ecceb5a3…`(1100 × 614), 픽셀 대조 bbox `None`·최대 차이 0. 벽이 흰 바탕이 아니라 옅은 베이지, 흰 세탁기 윗면 왼쪽에 세제 칸처럼 보이는 가로 칸(프롬프트 「no drawers」와 다름) — 관계와 무관해 채택하고 그림 읽기에 「코드의 무엇과도 짝짓지 않습니다」로 적음.

## 8. 옛 생성기

- 01이 막아 둔 것 그대로(`figures/_gen_figures.py` `raise SystemExit` · 공용 `_author_ch21_ch29.py` Ch 21 쪽 건너뛰기). 이 절에서 새로 막은 것 없음.

## 9. 서비스 요청과 비용

- 모델 요청 **0번**(노트북 A·B, 노트북 밖 확인 셋 모두 가짜 키 글자 또는 그래프 만들기만). 임베딩 0, 바깥 그림 서비스 0. 예상 비용 0달러.
- 삽화 2크레딧(거래 04:00:15Z).
- 참고 자료 확인(WebFetch 2026-09-25): LangChain v1 migration guide `https://docs.langchain.com/oss/python/migrate/langchain-v1`(「The import path for the agent prebuilt has changed from `langgraph.prebuilt` to `langchain.agents`」 · 「The `prompt` parameter has been renamed to `system_prompt`」 · 훅 → `before_model`/`after_model` 미들웨어 · 「`create_agent` only supports `TypedDict` for state schemas」 · 「We generate structured output in the main loop, reducing cost and latency」 · 스트림 노드 이름 `"agent"` → `"model"` · `ToolNode` 받지 않음 — `remaining_steps`는 적지 않음) · LangGraph v1 migration guide `https://docs.langchain.com/oss/python/migrate/langgraph-v1`(「deprecates the `create_react_agent` prebuilt」, 없애는 시기는 적지 않음 — 「2.0에서 없앰」은 설치판 경고 글에만).

## 10. 챕터 밖 수정

| 파일 | 무엇을 |
|---|---|
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | `verify.py --chapter`가 다시 씀(`4d673fe9…` → `8bd0846580a08d41de2306854a850c99844442161160df986b10da030552a677`) |

- 챕터 안(실습 폴더 포함): `labs/…/notebooks/04-*.ipynb`(새 판, `cbba4573…`) · `_src/04-*.html`(`bba748b7…`) · 빌드 HTML `04-*.html`(`6db1dc62…`, `{{` 0건)·`index.html`(`9112e268…`)·01~06 HTML(이웃 절 링크 제목 글자) · `chapter.json`(`f163836b…`, 04 제목 글자 하나) · `figures/04-1`~`04-5` 새 파일(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`·`.prompt.md`) · `qa/upgrade/` 새 파일(`author_04.py`·`probe/check04_graph_shapes.py`·`probe/check04_warning_stderr.py`·`04-figures.md`·`04-diagnosis.md`·`gates-wip-04*.json`·`review-pack/04-*.md`) · `handoff.md`·`manifest-changes.md`·`집필점검표.md`·`qa/verification.md` 04 행.
- **고치지 않은 것**: 도구 파일 · 실습 폴더 `pyproject.toml`·`uv.lock`·README · 01~03 파일(노트북·`_src`·생성기) · `textbook/part6/index.html`(Part 목차 — 마감 몫) · Ch 22·Ch 29·Ch 30 파일 · 공용 도구·게이트·`verify.py` · 옛 그림.
- **파일 삭제 0건**.

## 11. 뒤 챕터가 04·`create_react_agent`·옮기기에 기대는 문장 (고치지 않음, 참·거짓만)

`grep -rn 'create_react_agent\|마이그레이션\|0\.x\|1\.x' textbook/part6/*/_src textbook/part7` + 슬러그·옛 제목 글자 grep.

| 자리 | 문장·코드 | 판정 |
|---|---|---|
| Part 6·7 `_src`(Ch 22~34) | `create_react_agent`·「0.x」·「1.x」 0건 · Ch 21 04절을 가리키는 문장 0건 | 기댈 문장 없음 |
| Ch 23 02 `_src` 4·5·8·10행 | 「setup()을 호출해야 필요한 표와 마이그레이션 기록이 생성됩니다」 등 | **다른 뜻**(체크포인터 DB 표의 스키마 옮기기) — Ch 21 04와 무관, 참·거짓 대상 아님 |
| Ch 31 03 `_src` 4~10행 · Ch 31·32·33 `_src`·`part7/_build_index.py` 20행 | 「마이그레이션(migration)은 데이터베이스 구조 변경을 순서가 있는 코드로 기록하는 작업」(Ch 31 03 새 용어) | **다른 뜻**(DB 스키마). Ch 21 04는 「옛 판 코드를 새 판에서 돌도록 옮겨 쓰는 일」로 풀고 본문은 「옮기기」라 뒤 챕터 정의와 겹치지 않음 — 강사 확인 대상 3 |
| Ch 22 01 `_src` b3·b4 | 「Ch21에서는 create_agent() 함수로 에이전트를 만들었습니다」·「Ch21 01절에서 …」 | 참(04도 `create_agent`, 모델을 부르는 장면은 01 몫) |
| Ch 22 노트북 | `create_agent(model, tools=[lookup_hours], middleware=hooks)` | 04가 출력한 `middleware | 옛 함수: False | 새 함수: True`와 맞음 |
| `textbook/part6/qa/ch21-ch29-technical-review.md` 15행 | 「LangChain v1 migration guide — create_react_agent에서 create_agent로의 이식, system_prompt, TypedDict 상태, context 사용을 확인」 | 기록 파일(뒤 챕터 아님) — TypedDict 상태는 04가 실행하지 않음(b7) |
| `textbook/part6/index.html` · `qa/language/baseline/…` · Part 6 기록 JSON 여럿 · `textbook/part7/qa/existing-artifacts-before.json` 361행 | 옛 제목 글자 「0x에서 1x로」 · 옛 노트북 해시 `c6f65e65…` | Part 목차는 마감 때 `_build_index.py`로 새 글자 · 나머지는 기록(고치지 않음) |

## 12. 강사 확인 대상

1. **제목 「0.x에서 1.x로 마이그레이션」** — 점을 살린 글자로 고침(옛 생성기 글자와 같음), 슬러그는 그대로. 「마이그레이션」을 제목에 둘지, 「옛 판 코드 옮기기」 류로 바꿀지(과정 금지어 목록 §7-5 「마이그레이션」 → 풀어 씀).
2. **모델 요청 0인 절에 키 셀·모델 셀을 둠** — 모델 객체를 만들 때 키가 있어야 해서(가짜 키 글자는 과정 모양이 아님). 준비물·2절에 까닭 한 문장.
3. 말 「옮기기」(마이그레이션)와 Ch 31 03 「마이그레이션(DB 구조 변경 기록)」이 다른 뜻 — 04는 본문에서 「옮기기」만 써 겹치지 않게 함.
4. `with warnings.catch_warnings(record=True)`·`warnings.simplefilter`·`issubclass`·`inspect.signature` — 과정 처음 쓰는 이름 넷(각 한 문장 풀이). 경고를 그대로 두면 셀 출력에 실행한 컴퓨터의 임시 파일 위치가 찍혀 새 커널 두 번 출력이 달라지는 것이 까닭.
5. 코드 줄 30 → 142(셀 5 → 24) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘. 늘어난 몫은 01·02 자료·도구·양식 셀(두 함수에 같은 재료), 그래프 넷(옛·새 × 양식 없음·있음)의 노드·화살표·조건 함수·칸을 출력으로 보이는 셀.

## 13. 남은 것 · 지워야 하지만 지우지 않은 것

- 마감 몫: `textbook/part6/index.html` Part 목차 다시 만들기(옛 글자 「0x에서 1x로」 — `_build_index.py`, 묶음 zip도 다시 씀) · 옛 그림 `04-흐름.{svg,excalidraw,caption.md}` 삭제 승인 · `chapter.json` `objectives`·다른 절 제목 밑줄 표기 · 실습 폴더 README.
- 삭제 승인 대상(만들었지만 지우지 않음): 기기 `/tmp/ch21-04/`(`explore04.py`·`explore04b.py`·`warn_nb.py`·`A.ipynb`·`B.ipynb`·`cmp.py`·`resize.py`·`pixcmp.py`·`illu-1-orig.png` 3.3MB·`illu-1-1100.png`·`extra_check.py`·`ban_check.py`·`reps{1,2,3}.json`·`gates-wip-04-04.first.json`·`cnt-new/`·`cnt-old/`) · `.cache/ch21-04-view/`(그림 확인 사본 다섯) · `labs/…/notebooks/__pycache__/`·`qa/upgrade/__pycache__/`(있으면).

## 마감 반영 (2026-09-25, 챕터 마감 담당)

검토 1차(`review-round1-A.md`·`review-round1-B.md`) 반영과 챕터 마감에서 이 절에 한 일입니다. 전체 기록은 `chapter-summary.md`, 절 사이 기록은 `handoff.md` 「검토 반영과 챕터 마감 (2026-09-25)」입니다.

- **A-12·B-1 [중] NumPy(다시 실행, 모델 요청 0)**: 설치 셀 `"numpy==2.5.3"`(`langgraph-prebuilt` 뒤) · 준비물 「패키지 여덟」 · 1절 「도구 파일이 NumPy를 쓰므로, 01절처럼 numpy도 함께 설치합니다」 · 결과 읽기 `numpy: 2.5.3`. **새 커널 두 번**: A `run_section.sh … 04`(06:40:41~44Z, 약 2.6초 — 준비물 「5초 안에」 그대로) · B 사본 `/tmp/ch21-close/B04.ipynb`를 `execute.py`로(`UV_…`·`PYTHONPATH=…/notebooks`) → **24/24 같음**(`outputs_sha256` A·B 모두 `4a8d08c4…`). 앞 교재 출력과는 23/24 같음(설치 셀만). `code_sha256` `55f6505b…` → **`a83c7aaaa72d5f5cb21224e24eff738d9c13eb68bff217670373a7aa0db5d4ee`**, `outputs_sha256` `39d8c0c2…` → **`4a8d08c4283c9ba27f04ef519927c9efdfa48e90cc0154c3ddaa74d32e169112`**. b6 「새 커널로 두 번 실행했을 때 모든 셀의 출력이 같았습니다」 그대로 참.
- **B-2**: `04-2` 노란 상자 둘과 회색 공통 상자 머리에 「견준 여덟 가운데」(설치판 서명으로 옛 함수에만 `version`·`deprecated_kwargs`, 새 함수에만 `cache`·`transformers`도 있음 — 검토 B 확인), alt·도식 읽기(「노란 상자는 노트북 4절에서 견준 이름 여덟 가운데 한쪽에만 있던 것」) 같게, 다시 렌더·PNG 확인. 이 그림은 노트북에 첨부하지 않음(첨부는 04-1).
- **B-3**: b6 대응표 둘째 줄 근거 「4절 인자 줄 · 5절 두 셀(짝은 공식 옮기기 안내)」 · 노트북 9절 목록 같은 줄에 「두 인자를 짝지은 것은 공식 옮기기 안내입니다」.
- **B-4**: (1) 용어 표 「사용 중단 경고」에 일상 예 「가게에서 곧 팔지 않을 물건에 붙이는 「단종 예정」 안내처럼, 지금은 쓸 수 있지만 곧 없앤다는 표시」 · (2) 5절 결과 읽기 「LangGraph 1.0에서 사용을 멈췄다는 뜻」 → 「1.0부터 쓰지 말라고 알린(사용 중단을 예고한) 기능이라는 뜻」 · (3) 「마이그레이션」 풀이를 용어 표 「고쳐 쓰는 일」로 맞춤(b2·노트북 1절의 「옮겨 쓰는 일」 → 「고쳐 쓰는 일」).
- 위 §13 마감 몫: Part 목차 `textbook/part6/index.html` 새 글자(`_build_index.py`, 요약 §10) · `objectives`·다른 절 제목 밑줄 · README 끝남. 게이트 0(검사 문장 355).
