# 02절 진단과 개선 기록 — 구조화 출력 두 전략 (experiment)

- 대상: `_src/02-구조화-출력-두-전략.html` · `labs/part6/ch21-create-agent/notebooks/02-구조화-출력-두-전략.ipynb` · 도구 파일 `notebooks/runner_tools.py`(함수 하나 더함) · 그림 `figures/02-1`~`02-5`.
- 생성기: `qa/upgrade/author_02.py`(노트북 + `_src`, `e149564f…`). 흔들림 확인: `qa/upgrade/02-probe.md`·`probe/probe02.py`·`probe/probe-{TS,PS,AS}.jsonl`. 그림 설계표: `qa/upgrade/02-figures.md`. 검토 묶음: `qa/upgrade/review-pack/02-구조화-출력-두-전략.md`.
- 작업일 2026-09-25(UTC 02:3x~03:0x). 형식 **experiment 유지**(`chapter.json`), 슬러그 그대로(01 b8·01 생성기 `L_02`가 링크).

## 1. 게이트 전후

| | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전 (`gates-before.json`) | 5 | 76 | 1 | 1 | 0 | 0 | 6 | 28 | 3 | **39** |
| 첫 실행 전 (`gates-wip-02-02.json`의 첫 판, 노트북만 쓴 판) | 28 | — | 0 | 2 | 0 | 0 | 0 | 4 | 18 | — |
| 후 (`gates-wip-02.json`) | **28** | **381** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G2 2 = `print("칸 이름:", list(x.keys()))`(호출 안 호출 안 호출, `nested_call_2plus`) 두 셀 → 변수에 먼저 담음. G6 4 = 70자 넘는 문장 넷(도식 읽기 첫 문장·b7 한 줄·b8 다음 절 문장·b10 한 줄) → 나눔. G7 18은 그림 파일이 아직 없던 때의 값. 고친 뒤 같은 이름으로 다시 검사해 `gates-wip-02-02.json`은 지금 G1~G6 0 판입니다(첫 판 수치는 이 표에만 남음).
- AST 따로(`/tmp/ch21-02/extra_check.py` — 01 판에 **칸만 적은 `BaseModel` 양식 클래스 허용**을 더함): 노트북 **0건**, 도구 파일 2건 = `estimate_cost`의 `.get` 둘(Ch 6 06 원본 예외, 01과 같음). 금지어(`/tmp/ch21-02/ban_check.py`, 01 판 복사): 노트북·`_src`·캡션 다섯·`.mmd` 넷에서 **1건 = 「캐시 입력」**(허용 말). 「스키마」 0건 — 원어는 「schema」로 노트북·`_src`에 한 번씩(「라이브러리 문서는 이 양식을 원어로 schema라고 부르고」).
- 코드 줄(`count_code.py`) 33 → **157**(셀 5 → 28), 도구 파일 코드 줄 42 → **50**. 준비 셀이 아닌 셀의 주석 뺀 코드 최대 **9줄**, 함수 본문 최대 **6줄**(`print_branches`), 셀당 정의 하나(양식 클래스 셀 하나·함수 셀 하나), 첫 줄 주석 100%.

## 2. 수정 전 주요 문제 (준비 노트 §1·§2 02·§9-3, 인계 §01 → §02)

1. **도구 없는 에이전트**: `create_agent("openai:gpt-5.4-mini", [], response_format=…)` — 모델 이름 글자(temperature·reasoning_effort 없음), 도구가 없어 01절 에이전트 그래프와 이어지지 않고 `tools_to_model`(01이 남긴 자리)이 생기지 않음.
2. **입력이 답을 담은 글**: 「자료 R-14에 따르면 일반 도서 대출 기간은 14일입니다. 구조화해 주세요.」 — 모델이 근거를 찾는 장면이 아니고, `R-14`는 지어낸 자료 번호.
3. **모델 글에 건 `assert`**: `'R-14' in source and '14' in answer`. 옛 출력에서 `source`가 `R-14` / `자료 R-14`로 두 전략에서 달랐음(흔들림 대상).
4. **금지어**: 「스키마」 15/7/1 · 「검증」 9/2/1 · 「필드」 6/3/1 · 「네이티브」 · 「프로필」 · 「분기」·「반환」·「측정」·「지연」. 「structured_response에서 Pydantic 스키마의 필드를 읽을 수 있습니다」 같은 영문 시작 문장.
5. **틀 문장**: b3 「필요한 자료와 객체는 노트북에서 다시 선언하므로 …」, b6 = 확인할 점 = b8(같은 글 세 번), b7 「절당 1달러 미만」·「모델 문장과 지연」, b8 「03-AgentState와-context-schema에서 이 결과를 다시 사용합니다」(03이 02 결과를 쓰지 않음), 복습 해설 한 줄, 결과 읽기 셀 0, 옛 그림 `{{svg:02-흐름}}`은 두 전략을 한 줄 차례로 그림.
6. **셀 모양**: 클래스 + 에이전트 둘 + 입력 글을 한 셀에(c6), 제너레이터 `sum`·한 글자 이름 `m`·튜플 풀기·딕셔너리 한 줄(c8), `%pip`에 판 없는 `pillow`.

## 3. 바꾼 것

- **01절 에이전트 그래프에 두 전략을 붙임**(챕터 리드 결정, 인계 6항 (가)): 01과 같은 모델 객체(`nbkit.key_and_model_cells`)·`POLICY_DATA`·`DEF_TOOL`·시스템 메시지 글(생성기 `check_same_as_01()`이 01 생성기 상수와 문자열 대조) + `response_format=ToolStrategy(PolicyAnswer)` / `ProviderStrategy(PolicyAnswer)`. 질문은 01절 대출 질문 그대로.
- **양식 클래스**(Ch 19 02 범위): `PolicyAnswer(BaseModel)` 칸 둘 `topic: Literal["대출", "운영", "연체"] = Field(description=…)`·`answer: str = Field(description=…)`, 메서드 없음. 옛 `source` 칸 뺌. `model_json_schema()`로 `꼭 채울 칸`·`주제어 칸의 고를 수 있는 값`(enum)·설명을 출력(Ch 19 02 모양). 말은 Ch 6 03·Ch 19 02 「양식 클래스」·「칸」·「고를 수 있는 값」, `model_dump`는 Ch 6 03 메서드로 이음(세 문장 + Ch 2 10 링크는 Ch 6 03이 마침 — 과정 요약 §1 A 순서 → `_src` b3에 Ch 2 10 링크 한 줄).
- **두 그래프의 모양을 출력으로**(01 5절 셀을 함수 `print_branches(graph_agent)`로 묶음): 도구 전략 `tools | 조건 함수: tools_to_model | 갈 수 있는 곳: ['model', '__end__']` ↔ 제공자 전략 `['model']` · 두 그래프 `model_to_tools` 갈 곳 `['tools', '__end__', 'model']`(양식이 있으면 모델 노드 자기 자신이 더해짐 — 소스 1703~1705행). **01 5절 결과 읽기 「구조화 출력용 도구가 있을 때 `tools_to_model`이 끝으로 간다」는 갈 곳 출력으로 참**, 실제로 그 갈래로 끝난 장면은 이번에도 없음(§6).
- **메시지 칸 비교**: 도구 전략 메시지 5(`['lookup_policy']` → 도구 메시지 → `['PolicyAnswer']` → 도구 메시지 「Returning structured response: …」) ↔ 제공자 전략 4(마지막 응답 요청 0건, 내용 글이 JSON). 양식 값이 온 자리를 셀로 보임(도구 전략 = 양식 도구 요청의 인자, `그 응답의 내용 글 길이: 0` · 제공자 전략 = 마지막 응답의 내용 글). 도구 전략의 마지막 도구 메시지는 **모델 노드가 만든다는 것**과 흐름을 끝으로 보낸 조건 함수(`model_to_tools`)는 소스로만(1255~1276·1953~1968행, 결과 읽기에 「소스로 보면」).
- **결과 칸**: 두 전략 모두 결과 키 `['messages', 'structured_response']`, `structured_response의 종류: PolicyAnswer`, `칸 이름: ['topic', 'answer']`, `주제어 칸 값이 정해 둔 셋 안인가: True`. 01 6절 「구조화 출력을 쓰지 않아 칸 `structured_response`에는 값이 생기지 않았습니다」·b8 「그 결과를 담는 자리」가 이 절로 이어짐.
- **값 바꿔 보기** = `response_format=PolicyAnswer`(양식 클래스 그대로): 기능 표 `model.profile["structured_output"]` → `True`, 그래프 갈 곳은 도구 전략과 같음(만들 때 양식 도구를 준비 — 소스 1024~1036행), 메시지 칸은 제공자 전략과 같음(요청할 때 전략을 고름 — 소스 1357~1367행). 「프로필」 대신 「기능 표(속성 `profile`)」.
- **도구 파일**: 01 노트북 함수 `agent_row`를 이 절이 다시 써서 `runner_tools.py`로 옮김(§5). 두 전략·바꾼 값의 기록 한 줄씩(`ToolStrategy | 2 | 2 | True` · `ProviderStrategy | 2 | 1 | True` · `양식 클래스 그대로 | 2 | 1 | True`). 모델 요청 수 = 응답 수(01 규칙), 도구 메시지 수로 짐작하지 않음.
- **사용량·예상 비용**: `sum_usage`·`estimate_cost`(도구 파일) — 입력 토큰 `572` ↔ `768`(흔들림 확인 5/5·A/B 같음 → 결과 읽기 첫 단락), 출력 토큰·예상 비용(`0.000699` ↔ `0.000824`)은 둘째 단락 「이번 실행에서는」, 「어느 전략이 싸다고 말하지 않습니다」. 입력 토큰 차이의 몫은 나눠 세지 않았다고 밝힘. 걸린 시간 재지 않음.
- **`assert`**: `structured_response`의 자료형(두 셀)과 호출 ID 짝(표 셀)에만. 모델이 채운 양식 칸 값에 건 `assert` 0.
- **새 용어 3**(도구 전략(ToolStrategy) · 제공자 전략(ProviderStrategy) · 양식 도구) — meta 「새 용어 5」 → 3. 「구조화 출력」·「양식 클래스」는 Ch 6·19 말(새 말 아님).
- 본문 10블록을 새 출력으로 다시 씀(비유 「세탁기」 02 — 따로 세운 판 ↔ 몸체에 붙은 틈, 용어 표, 그림 넷 + 삽화, 결과 표, b7 열한 줄, 복습 넷·해설 셋 문장, 참고 자료 아홉 줄). 제작 이력 문장 0. 옛 그림 `figures/02-흐름.*`은 그대로(본문 참조 0).

## 4. 흔들림 확인과 새 커널 두 번 (규격 §2-7 9·10번 끝)

- **노트북 밖 다섯 번씩**(`02-probe.md`, 규칙 §0을 첫 요청 전 02:37Z에 적음 → 요청 02:37:57~02:38:30Z): TS 5/5 · PS 5/5 · AS 5/5 **모두 같음** — 결과 키 · 메시지 종류 · 도구 요청 이름과 인자 · 도구 메시지 이름·상태·내용 · 호출 ID 짝 · `structured_response` 자료형·칸 · 입력 토큰(TS 261·311 · PS/AS 359·409) · 출력 토큰(TS 18·42 · PS/AS 18·37) · 양식 칸 값까지 15/15 같음. 모델 `gpt-5.4-mini-2026-03-17`, 캐시 입력 0, 오류 0, 양식 검사 실패 재요청 0, 한 응답에 두 요청을 함께 담은 회차 0. → 입력·양식을 그대로 씀.
- **새 커널 두 번**: A `run_section.sh`(02:51:30~37Z, 셀 실행 기록 약 7.5초) · B 사본 `/tmp/ch21-02/B.ipynb`를 `execute.py`로(02:52:03~11Z, 약 7.7초, `UV_…`·`PYTHONPATH=…/notebooks`). `code_sha256` `cc31fb4586c9…` 둘 다, **셀별 출력 글자 28/28 같음**, `outputs_sha256` 둘 다 `4c4b79dfa046…`. 교재 출력 = A. 그림은 `.mmd`를 노트북 밖 값으로 먼저 써 두고 A·B 출력과 대조(달라진 값 0 — 라벨·폭 때문에만 고침).
- **흔들린 값의 자리(본문 결론·그림·정리·복습에 안 씀)**: 양식 칸 값(`대출`·규정 글 — 이번 두 번과 밖 다섯 번은 같았지만 모델 글) · 제공자 전략 마지막 응답의 JSON 글 · 도구 메시지 내용의 뒤쪽 글 · 출력 토큰 `60`·`55` · 예상 비용 `0.000699`·`0.000824` → 결과 읽기 둘째 단락에만. 입력 토큰 `572`·`768`은 첫 단락·표·그림 02-4(밖 다섯 번·새 커널 두 번 모두 같음, 결론 문장은 「달랐다·몫은 세지 않음」까지).
- **탐색으로 고른 입력 없음**: 질문·시스템 메시지 글은 01과 같은 글, 양식 칸 둘과 설명은 첫 요청 전에 정함(b7 「흐름을 보여 주려고 정한 예」).

## 5. 도구 파일 `notebooks/runner_tools.py`

- **더한 함수** `agent_row(question_name, result)` — `# Ch 21 01절에서 배웠습니다 — 01절 노트북 10절의 같은 이름 함수를 옮겼습니다`. 본문은 01 생성기 `DEF_ROW`와 **AST가 같고 코드 줄이 같음**(`check_same_as_01()`이 실행마다 대조). 01 셀의 첫 줄 주석 「실행 결과 하나를 기록 한 줄로 만듭니다(모델 요청 수 = 응답 메시지 수)」은 도구 파일 주석 두 줄로 풀어 적음(첫 칸 이름표가 질문 이름이나 설정 이름을 받는다는 말을 더함). 머리 독스트링에 「앞 챕터와 앞 절에서」·「01절 노트북에서 처음 적은 함수(agent_row)도 02절부터 쓰므로」 한 줄씩.
- 해시 **`eb408639…` → `ab31d0c1ef7b4b89a63a8fcf843d21f3ee7feff311afe7ecbb86d6c007f32621`**, 76 → 89줄(코드 줄 42 → 50), import 0. 01 노트북은 이 파일에서 `call_id_lists, estimate_cost, show_messages, sum_usage`만 가져오므로 01의 출력·코드는 그대로(01 노트북에는 `agent_row` 정의가 남아 있음 — 처음 가르친 절).
- 02가 가져오는 것: `agent_row, estimate_cost, show_messages, sum_usage`(알파벳 순). 준비 셀 결과 읽기에 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다」.
- **옮기지 않은 것**: 이 절 함수 `print_branches(graph_agent)`(01 5절 반복 셀을 처음 함수로 묶은 것 — 처음 가르친 절이라 노트북). 03이 다시 쓰면 03이 옮김(인계).
- 묶음 목록 두 곳은 01이 이미 이 파일을 올려 둠 — 이번에 고치지 않음.

## 6. 두 전략 비교 요약 (보고용)

| 항목 | 도구 전략(`ToolStrategy`) | 제공자 전략(`ProviderStrategy`) | 양식 클래스 그대로(바꾼 값) | 근거 |
|---|---|---|---|---|
| 노드 | `model`·`tools` | 같음 | 같음 | 출력 |
| `tools_to_model` 갈 곳 | `['model', '__end__']` | `['model']` | `['model', '__end__']` | 출력(까닭은 소스 1678~1685행) |
| `model_to_tools` 갈 곳 | `['tools', '__end__', 'model']` | 같음 | 같음 | 출력(소스 1703~1705행) |
| 결과 키 | `messages`·`structured_response` | 같음 | (출력하지 않음) | 출력 |
| 메시지 | 5(Human·AI·Tool·AI·Tool) | 4 | 4(메시지 칸 네 줄) | 출력 |
| 응답 수(모델 요청) | 2 | 2 | 2 | 출력(`agent_row`) |
| 도구 메시지 수 | 2(규정 · 양식) | 1 | 1 | 출력 |
| 양식 값이 온 자리 | 둘째 응답의 양식 도구 요청 인자(내용 글 길이 0) | 마지막 응답의 내용 글(JSON), 요청 0건 | 마지막 응답이 요청 0건(메시지 칸) | 출력 |
| `structured_response` | `PolicyAnswer`·칸 둘·셋 안 `True` | 같음 | `PolicyAnswer` | 출력 |
| 입력 토큰 합 | 572 | 768 | (노트북에서 세지 않음, 밖 다섯 번은 768) | 출력 · 밖 기록 |
| 끝으로 보낸 조건 함수 | `model_to_tools`(양식 도구 요청은 도구 실행 노드로 보내지 않음, `structured_response`에 값) | `model_to_tools`(요청 0건) | 같음 | **소스로만**(1953~1968행) |
| 양식 도구 메시지를 만든 곳 | 모델 노드 | — | — | **소스로만**(1255~1276행) |

- **실행하지 않은 것**(b7): 한 응답에 규정 요청과 양식 도구 요청이 함께 오는 경우(그때만 `tools_to_model`이 끝으로 감, 2028~2030행 — 양식 값이 도구 메시지를 보기 전에 채워짐) · 양식 검사 실패 재요청(`handle_errors` 기본 참, 도구 전략만) · 도구가 필요 없는 질문을 도구 전략에 보냄(`tool_choice="any"`, 1423행) · 기능 표가 거짓인 모델 · 입력 토큰 차이의 몫.

## 7. 그림

- Mermaid **4장**(`02-1` flowchart TB + subgraph 둘 681 · `02-2` flowchart TB + subgraph 둘(위아래) 592 · `02-3` sequenceDiagram 852 · `02-4` flowchart TB + subgraph 셋 860, 모두 868 이하), **빨강 0**, 보라는 `02-3` 모델 노드 띠 하나, 초록은 양식 클래스(02-1)·같은 조건(02-4). 설계표 `02-figures.md`, PNG 넷을 직접 열어 봄(`.cache/ch21-02-view/`). 02-2는 칸 안 `LR`에서 라벨이 겹치고 1047로 넓어 칸 안 `TB`·위아래 칸으로 바꾸고 자기 자신 갈래 라벨을 뺌(렌더 세 번), 02-3은 메모를 세 줄로 나눠 915 → 852, 02-4는 회색 상자에서 결과 키 줄을 뺌(11절은 키를 출력하지 않아 세 칸 공통이 아님).
- 삽화 **1장** `02-5-개는-판을-세운-쪽과-틈이-붙은-쪽`(비유 계열 **「세탁기」** 02 — 앞에 따로 세운 빨래 개는 판 ↔ 몸체에 붙은 틈, 바구니 없음) — **1차 job `28a107c2-cfd5-46ac-b003-a8781baf71b6` 채택**, 재생성 0, **2크레딧**(거래 2026-09-25T02:54:19Z 「Nano Banana Pro −2」, 생성 전 잔액 2461.75, 바로 앞 거래 02:46:36Z 「GPT Image 2.5 Flare」 다섯 줄은 다른 세션). 응답 모델 이름 표시는 `nano_banana_2`(01과 같은 표시). 원본 `b062db3e…`(2752 × 1536) → 저장 `1b373506…`(1100 × 614), 픽셀 대조 bbox `None`·최대 차이 0. 오른쪽 셔츠는 반듯이 놓이지 않고 반쯤 나와 늘어져 있어 그림 읽기에 그대로 적음. 처음 저장 이름 「칸이-붙은-쪽」을 그림을 보고 「틈이-붙은-쪽」으로 `mv`(본문 비유 말도 「칸」→「틈」).

## 8. 옛 생성기

- 01이 막아 둔 것 그대로(`figures/_gen_figures.py` `raise SystemExit` · 공용 `_author_ch21_ch29.py` Ch 21 쪽 건너뛰기). 이 절에서 새로 막은 것 없음.

## 9. 서비스 요청과 비용

- 노트북 한 번 **6번**(7절 2 · 8절 2 · 11절 2), 임베딩 0, 바깥 그림 서비스 0.
- 이 절 작업 전체 **42번** = 노트북 밖 흔들림 확인 30(TS 10 · PS 10 · AS 10) + 새 커널 두 번 12. 구조 확인(`/tmp/ch21-02/shape_check.py`)은 가짜 키 글자로 모델 객체만 만들고 `invoke`하지 않음(요청 0).
- 요금표(2026-09-17, 100만 토큰당 입력 0.75 · 캐시 입력 0.075 · 출력 4.50달러)로 어림한 예상 비용: 노트북 한 번 약 0.0023달러(도구 전략 0.000699 · 제공자 전략 0.000824 · 양식 클래스 그대로 약 0.000824 — 밖 기록 사용량으로 셈), 작업 전체 약 0.016달러(청구 금액 아님). 삽화 2크레딧.
- 참고 자료 확인: LangChain Structured output `https://docs.langchain.com/oss/python/langchain/structured-output`(WebFetch 2026-09-25 — 「The structured response is returned in the `structured_response` key」, 기능 표(profile data)로 제공자 전략을 고름, 기본 도구 메시지 「Returning structured response: {data}」, `handle_errors` 기본 `True`, 지원 양식 넷).

## 10. 챕터 밖 수정

| 파일 | 무엇을 |
|---|---|
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | `verify.py --chapter`가 다시 씀(`1e0c83f3…` → `4fa11281…`) |

- 챕터 안(실습 폴더 포함): `labs/…/notebooks/02-*.ipynb`(새 판, `920244fc…`) · `runner_tools.py`(`ab31d0c1…`) · `_src/02-*.html`(`b7b19144…`) · 빌드 HTML `02-*.html`(`cc88e29e…`, `{{` 0건)·`index.html` · `figures/02-1`~`02-5` 새 파일(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`·`.prompt.md`) · `qa/upgrade/` 새 파일(`author_02.py`·`02-probe.md`·`probe/probe02.py`·`probe/probe-{TS,PS,AS}.jsonl`·`02-figures.md`·`02-diagnosis.md`·`gates-wip-02*.json`·`review-pack/02-*.md`) · `handoff.md`·`manifest-changes.md`·`집필점검표.md`·`qa/verification.md` 02 행.
- **고치지 않은 것**: `chapter.json`(절 제목 「구조화 출력 두 전략」은 옛 판과 같음 — 고칠 것 없음, `objectives`는 마감 몫) · 실습 폴더 `pyproject.toml`·`uv.lock`·README(마감 몫 — `pydantic`은 잠금 판 2.13.5로 `%pip`에만 적음) · 01 파일(노트북·`_src`·생성기) · Ch 22·Ch 26·Ch 29·Ch 30 파일 · 공용 도구·게이트·`verify.py` · 옛 그림.
- **파일 삭제 0건**(이름 바꾸기 한 번 — 이 절이 만든 삽화 PNG).

## 11. 뒤 챕터가 Ch 21 02·구조화 출력에 기대는 문장 (고치지 않음, 참·거짓만)

| 자리 | 문장 | 판정 |
|---|---|---|
| `labs/part6/continuity-guide.md` 7행 | 「Ch21 `create_agent`의 도구 호출 루프와 구조화 출력」 | **참**(01 루프 + 02 `response_format` 두 전략) |
| Ch 22 01 `_src` 4·9행 | 「Ch21에서는 create_agent() 함수로 …」·「Ch21 01절에서 … 다시 모델을 부릅니다」 | 참(02와 무관, 01 몫 그대로) |
| Ch 26 03·04 노트북 | `with_structured_output(Route)`·`with_structured_output(CompareRoute, include_raw=True)` | Ch 21 02에 기대지 않음(Ch 6 03 모양). Ch 26 03 설명 셀의 「스키마」·「반환」은 Ch 26 몫 |
| Ch 27 01·02 `_src` b3 | 「Ch 21의 create_agent는 모델과 도구의 반복을 만들었습니다」·「Ch 21에서 create_agent에 도구를 전달했습니다」 | 참(02도 `tools=[lookup_policy]`) |
| Ch 29 01·04 `_src` | 「Ch21 에이전트」·`rag-comparison.json` 인용 값 | 02와 무관(06 몫) |
| Ch 30 03 `_src` b3 | 「Ch21에서 Agent의 입력과 결과가 상태 사전임을 확인했습니다」 | 뜻은 참(02 결과 딕셔너리 키 `['messages', 'structured_response']`) — 「사전」은 Ch 30 몫 |
| Ch 30 09 `_src` b3 | 「Ch21에서는 init_chat_model과 create_agent로 도구 호출 Agent를 만들었습니다」 | 참(02도 모델 객체를 넘김) |
| Part 7 `ToolStrategy`·`ProviderStrategy`·`structured_response` | — | 0건(`grep`) |

## 12. 강사 확인 대상

1. 코드 줄 33 → 157(셀 5 → 28) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘. 늘어난 몫은 두 전략을 01 에이전트 그래프에 붙여 **그래프 모양·메시지 칸·양식 값 자리·결과 칸을 전략마다 출력으로 보이는 셀**(전략마다 넷)과 값 바꿔 보기(넷)·결과 읽기 셀 분리.
2. 새 API 모양: `response_format=`·`ToolStrategy(…)`·`ProviderStrategy(…)`(과정 처음, 절 주제) · 모델 객체 속성 `profile`(과정 처음 — 「기능 표」로 부름, 값 바꿔 보기의 근거 출력) · `model_json_schema()["properties"]["topic"]["enum"]`(Ch 19 02는 `["required"]`까지 — 이번에는 안쪽 칸까지 읽음).
3. 삽화 `02-5`: 오른쪽 셔츠가 반듯이 개어진 모양이 아니라 틈에서 반쯤 나와 늘어짐 — 「개어진 채 나온다」가 그림만으로 읽히는지(그림 읽기는 보이는 대로 적음). 다시 만들면 2크레딧.
4. 새 용어 수 5 → 3, 말 「도구 전략」·「제공자 전략」·「양식 도구」·「기능 표」(원어 병기).
5. 설치 셀에 `pydantic==2.13.5`를 더함(노트북이 `from pydantic import …`를 직접 씀, 잠금 판과 같음 — `pyproject.toml`에는 직접 의존으로 없음, 마감 때 README·pyproject 표기 판단).

## 13. 남은 것 · 지워야 하지만 지우지 않은 것

- 마감 몫: 옛 그림 `02-흐름.{svg,excalidraw,caption.md}` 삭제 승인 · `chapter.json` `objectives` · 실습 폴더 README(도구 파일 함수 여섯·요청 수) · `part6-practice.zip` 재생성(도구 파일 새 해시 포함).
- 삭제 승인 대상(만들었지만 지우지 않음): 기기 `/tmp/ch21-02/`(probe 원본 JSONL·A/B 사본·`shape_check.py`·`resize.py`·`cmp.py`·원본 삽화 3.6MB `illu-1-orig.png`·`illu-1-1100.png`·`runner_tools.before.py`·`extra_check.py`·`ban_check.py`) · `.cache/ch21-02-view/`(그림 확인 사본 다섯) · `labs/…/notebooks/__pycache__/`·`qa/upgrade/__pycache__/`(있으면).

## 마감 반영 (2026-09-25, 챕터 마감 담당)

검토 1차(`review-round1-A.md`·`review-round1-B.md`) 반영과 챕터 마감에서 이 절에 한 일입니다. 전체 기록은 `chapter-summary.md`, 절 사이 기록은 `handoff.md` 「검토 반영과 챕터 마감 (2026-09-25)」입니다.

- **A-12 NumPy(다시 실행)**: 설치 셀에 `"numpy==2.5.3"` · 준비물 「패키지 일곱」(기준 버전 단락이 여섯 문장이 되어 Linux 두 줄을 다음 단락으로 나눔 — G6) · 1절 「도구 파일이 NumPy를 쓰므로, 01절처럼 numpy도 함께 설치합니다」 · 결과 읽기 첫 단락 `numpy: 2.5.3`. `run_section.sh … 02`로 새 커널 한 번(06:41:33~40Z, 약 7.2초 — 준비물 「20초 안에」 그대로), **모델 요청 6번**, 어림 약 0.002달러. **앞 교재 출력과 28셀 가운데 27셀 같음**(다른 셀은 설치 셀 [3]뿐 — 입력 토큰 `572`·`768`, 출력 토큰 `60`·`55`, 예상 비용 `0.000699`·`0.000824`까지 같음). `code_sha256` `cc31fb45…` → **`5a3351792f90487c68cce185caa096a3bd9166595aa7e7e76c9f6301e003e030`**, `outputs_sha256` `4c4b79df…` → **`afecf4e50d24bb9677ef1fa2ef32a860fa46bae021f152006c25ff58dab10f50`**.
- **A-3 [중] `strict`**: 셀 [24] 「OpenAI 계열 모델이면 설정 `strict=True`를 더해, 양식을 꼭 지키게 요청합니다」 → 「함께 싣는 도구 명세에 설정 `strict=True`를 붙입니다 · 양식 쪽을 꼭 지키게 하는 설정은 `ProviderStrategy(…, strict=True)`이고 이 절은 주지 않았습니다 · 그래서 요청 글의 양식 쪽에는 `"strict": false`가 실립니다 · 모델을 부르지 않고 요청 글만 만들어 본 확인이고 이번 노트북에서는 출력하지 않았습니다」(다섯 문장 단락). 근거: `factory.py` 1391~1404행(주석 「Redundantly set strict=True on tools」·`bind_kwargs["strict"] = True`) · `structured_output.py` 284~308행(`strict=None` 기본, 줄 때만 `json_schema["strict"] = True`) · **모델을 부르지 않은 확인**(`.cache/ch21-close/strict_check.py` — 검토 A 대본 사본, 가짜 키 글자, `_get_request_payload`): `tools strict: [True]` · `response_format … "strict": false` · `parallel_tool_calls in payload: False`. 위 인계 「§01 → §02」 3항의 「ProviderStrategy는 OpenAI 계열이면 `strict=True`를 더 붙임」은 **도구 명세에 붙는 것**이 맞는 뜻(handoff 마감 절에 적음).
- **A-4 [중] 전략 고르기 규칙**: [54] 「이 값이 참이면 제공자 전략을, 아니면 도구 전략」 → 「소스(`factory.py` 583~596행)로 보면 참이면 제공자 전략 · 참이 아니면 정해 둔 모델 이름 목록(174~194행)과 한 번 더 견주고, 거기에도 없으면 도구 전략 · 이 절의 모델 이름도 그 목록에 들어 있습니다」(186행 `gpt-5\.4-(mini|nano)`; 첫 판은 모델 이름을 백틱으로 적어 G5가 잡음 → 백틱 없는 말로) · [60] 「표시가 거짓인 모델에서는 …」 → 「기능 표와 이름 목록 어디에도 없는 모델에서는 도구 전략이 골라지고 …」. b4·복습 4는 그대로 참.
- **A-5**: b6 표 셋째 줄 양식 값 자리 「마지막 응답의 내용 글」 → 「마지막 응답(요청 0건) · 글은 출력하지 않음」.
- **A-6**: `02-1` 노란 상자 「모델 노드가 붙인 도구 메시지」 → 「마지막 도구 메시지」(누가 붙였는지는 02-3의 「소스 확인 ·」 메모가 맡음), alt 같은 말, 다시 렌더·첨부 PNG 새 판, PNG를 열어 확인. 도식 읽기는 그 말을 쓰지 않아 그대로.
- **A-7**: [36]·b7 「`tools_to_model`이 끝으로 가는 것은 …」 앞에 「양식 도구 쪽에서」(01의 「둘뿐」 — `return_direct` 경우와 부딪히지 않게).
- **A-8**: b4 「비교와 경계」 끝에 「지원 여부는 모델 객체의 기능 표(속성 `profile`, 지원하는 기능을 적은 딕셔너리)로 봅니다」.
- 게이트 0(검사 문장 389), 금지어 전후 같음, 생성기 = 노트북·`_src`.
