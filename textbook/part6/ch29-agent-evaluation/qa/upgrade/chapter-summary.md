# Ch 29 Agent 평가 — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part6/ch29-agent-evaluation` 01~04절(품질 개선) + **05절 챕터 끝 실습 절 신설**(`05-Agent-평가-실습`), 노트북 `labs/part6/ch29-agent-evaluation/notebooks/01~05-*.ipynb`, 도구 파일 `notebooks/eval_tools.py`. **뒤 챕터가 읽는 계약 파일(산출 파일)은 없습니다**(노트북 파일 쓰기 0). 04는 앞 챕터 계약 파일 둘(Ch 21 06·Ch 18 06)을 읽기만 합니다.
- 기간: 2026-09-29(준비 조사 · 01~04절 개선 · 05절 신설 · 검토 1차 · 챕터 마감). 상태: **완료(강사 확인 대기)**. Part 6 마지막 챕터(다음은 Part 7 Ch 30).
- 게이트: 수정 전 네 절 합계 **131**(G1 20 · G2 4 · G3 0 · G4 0 · G5 29 · G6 66 · G7 12 — 01 27 · 02 41 · 03 22 · 04 41, `gates-before.json`) → 마감 뒤 **5/5 PASS, G1~G7 모두 0**(`gates-after.json`, 검사 문장 360·422·433·412·376 = **2,003**).
- 코드 셀 5·5·5·9 = 24 → **23·27·28·25 + 05 새 절 24 = 127**(`verify.py --chapter` → `PASS 5 sections / 127 code cells (max 14 lines)`). 코드 줄(`count_code.py`, 주석·빈 줄 뺌) 28·37·31·60 = 156 → **120·168·155·151 + 05 143 = 737**, 도구 파일 135줄(파일). Mermaid **19장**(01~04 넷씩 · 05 셋), 삽화 **5장**(절마다 하나, Higgsfield — 재생성 0, 10크레딧, 마감 0), 복습 문제는 HTML에만.
- **모델 요청**: 01·02·04는 모델 없음(코드로 적은 궤적·앞 챕터 기록 읽기). 03은 앞 절반이 모델 없는 구조, 4~6절만 실제 `gpt-5.4-mini`(`temperature=0`·`reasoning_effort="none"`). 05는 실습 절. 노트북 한 번 **0 · 0 · 5 · 0 · 5 = 10**번. 작업 전체(노트북 밖 흔들림 확인 + 시험 실행 + 새 커널 A·B — `probe/*.jsonl`과 노트북 출력으로 다시 셈, §9) **01 0 · 02 0 · 03 40 · 04 0 · 05 35 = 75번**, 마감 **0번**.
- 화면 검사 `visual.cjs`: HTML **여섯 개**(다섯 절 + `index.html`) × 1280px·390px = **12행 PASS**(기기 `/tmp/pw` playwright·`/tmp/pw-browsers` chromium — Ch 26 마감이 설치한 것을 환경 변수 `NODE_PATH`·`PLAYWRIGHT_BROWSERS_PATH`·`LD_LIBRARY_PATH`만 주고 원본 그대로). Ch 21 06 HTML(마감에서 문장 하나 고쳐 다시 빌드)도 두 줄 PASS.
- **마감에서 다시 실행한 노트북: 02·04 둘**(둘 다 모델 없음·요청 0 — 02는 긴 한 줄 코드, 04는 `executed_at` 출력 빼기, §19). 01·03·05는 `code_sha256`·`outputs_sha256`·`executed_at`이 전후 같습니다(마크다운만).
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 28 요약 → **이 문서** → `handoff.md`(절 사이 세부, 끝 「검토 반영과 챕터 마감 (2026-09-29)」) → 절별 `NN-diagnosis.md`(끝 「마감 반영」)·`03-probe.md`·`05-probe.md`(노트북 밖 흔들림 확인) → 검토 `review-round1-A.md`(01~02·공통)·`review-round1-B.md`(03~05) → 준비 조사 `chapter-lead-notes.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 문법·API | 새로 만든 함수 (도구 파일에 둔 것은 굵게) | 새 용어 |
|---|---|---|---|
| 01 에이전트 평가 세 전략 | 손으로 만든 궤적(`HumanMessage`·`AIMessage(content=…, tool_calls=[…])`·`ToolMessage(content=…, tool_call_id=…)` — Ch 20 01 모양) · 설치판 agentevals 0.0.9 `create_trajectory_match_evaluator(trajectory_match_mode="strict")` → 평가 함수(`outputs=`·`reference_outputs=`) → 결과 딕셔너리 `{'key': 'trajectory_strict_match', 'score': True, 'comment': None, 'metadata': None}` · 음수 번호 `[-1]` · `type(x).__name__` · 최종 답 평가(마지막 글 = 기준 답, 글자 비교)·한 단계 평가(첫 모델 응답의 도구 이름)·궤적 평가(모드 `strict`) · 값 바꿔 보기(답 글만) | **`make_trajectory`**·**`called_tool_names`**·**`trajectory_pass`**(02가 도구 파일로) · `final_answer_pass`·`first_step_pass`·`three_results`(노트북) | 기준 궤적 · 최종 답 평가 · 한 단계 평가 · 궤적 평가 · 궤적 맞춰 보기 (5) — 「궤적」은 Ch 17 04를 이어 씀 |
| 02 궤적 매칭 네 모드 | 모드 넷(`strict`·`unordered`·`subset`·`superset`)의 평가 함수를 딕셔너리에 모음 · 짝짓기(요청 횟수까지 셈 — 설치판 `utils.py` 90~134행) · 인자 비교 방식 `tool_args_match_mode`(`exact`·`ignore`·`subset`·`superset`) · 도구별 덮어쓰기 `tool_args_match_overrides={"search_documents": "ignore"}` · 목록 메서드 `count`·`remove`(처음 쓰는 자리에서 한 문장씩) · 목록 `copy()`(Ch 2 03) · **딕셔너리 `copy()`(Ch 18 05 — 마감 A-7에서 셀 47·55가 씀)** · 모드·인자 비교 방식에 따라 갈린 값에만 `assert`(다섯 셀 × 두 줄) | **`four_modes`**(03이 도구 파일로) · `unpaired_names`(이름만 보는 교재용 — 노트북) | 모드 `unordered`·`subset`·`superset` · 짝짓기 · 인자 비교 방식 · 도구별 덮어쓰기 (6) |
| 03 LLM judge로 궤적 평가 | 설치판 `_format_inputs`(평가 모델이 받는 궤적 글 — 밑줄 함수, 판 고정·공개) · 판정 머리글 `TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE`(글 메서드 `startswith`·`format`) · `create_trajectory_llm_as_judge(judge=모델 객체, prompt=…)`(문자열 `model=`이면 온도·추론 설정 없이 만듦 — openevals 0.2.0 `llm.py` 251~254행) → `{'key': 'trajectory_accuracy', 'score', 'comment', 'metadata'}` · `@tool` + 매개변수 `: str`(Ch 19 01) · `create_agent(model, tools=[…], system_prompt=…, middleware=[ModelCallLimitMiddleware(run_limit=4, exit_behavior="end")])` · `invoke(…, {"recursion_limit": 20})`(Ch 20 03) · 결과 목록에 시스템 메시지 없음(`assert` — `factory.py` 1451~1452행) · 요청 수 셈 「도구를 요청한 응답 수 + 1」 · 궤적 목록 `copy()` 뒤 `[-1]`에 새 `AIMessage` | 새 함수 0(도구 파일에 **`four_modes`·`sum_usage`·`estimate_cost`**를 더함) | 궤적 글 · 판정 까닭 · 평가받는 에이전트 (3) |
| 04 운영 지표와 Ch18 궤적 비교 | 파일 위치 셀(후보 셋 + `for`·`break` + `os.path.exists` — Ch 21 06 모양) · `with open(…) as file` + `json.loads(file.read())` · 노트북 파일의 저장된 출력(칸 `outputs`·`output_type` `stream`·`text`) · 글 메서드 `join`(Ch 16 01)·`splitlines`·`strip`·`split` · 음수 슬라이스 `[-5:]`(Ch 16 03) · `int(글)`·`float(글)`·**`float(참·거짓 값)`** · `round(…, 3)` · `sorted`·`math.ceil`(Ch 15 06) · 딕셔너리 두 겹 읽기 · 모르는 값 `None` · 95 백분위수(가장 가까운 자리 방식) | **`average`·`nearest_rank`**(Ch 15 06 노트북 셀 글자 그대로 — 04가 도구 파일로) · **`show_row`**(05가 도구 파일로) · `printed_lines_of`·`split_row`·`ch18_row`·`ch21_row`·`column_values`(노트북) | 운영 지표 · 공통 칸 (2) |
| 05 Agent 평가 실습 | **새 문법·새 API·새 말 0**(01~04 노트북·도구 파일 04판과 AST 대조 — 새 요소는 속성 `usage_metadata`·연산 `is`·`-`·슬라이스 `[:-1]`뿐이고 모두 도구 파일·Ch 26 04·05에 있음) | 조립 `run_agent(limit)` · `count_asked(messages)` · `model_part(messages)` · `run_row(name, messages, usage, score)`(노트북) | 0 |

- 새 용어 합계 **16개**(절 meta 「새 용어」 5·6·3·2·0).
- **이 챕터에서 허용한 문법**: 함수(셀당 하나, 본문 8줄 이하) · 여러 줄 `if`·`for` · 목록 `append`·`count`·`remove`·`copy()` · 딕셔너리 `copy()`(02 마감) · 딕셔너리 여러 줄(키마다 한 줄 — 마감 A-7로 02 셀 29·43을 맞춤) · `@tool` + `: str`(03·05) · `with open`·`json.loads` · 글 메서드 `join`·`splitlines`·`strip`·`split`·`startswith`·`format` · `sorted`·`math.ceil`(04) · `float(참·거짓 값)` · 도구 파일 `estimate_cost`의 `.get` 둘(Ch 6 06 본문 그대로). 마감 AST 따로(`extra_check.py`) 금지 문법 0.
- **쓰지 않은 것**(다섯 절·도구 파일 0건): f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·`statistics`·`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`.items`·`+=`·기본값 매개변수·반환 힌트·대입 풀기·별표 풀기·`while`·`try`·세미콜론·`isinstance`·클래스·`async`.
- 셀 모양: 준비 셀 밖 셀 **12줄 이하**(02 셀 47 — 마감 A-7로 10 → 12, 규격 §2-4 「3~12줄」 안), 함수 본문 8줄 이하, 셀당 정의 하나, 첫 줄 주석 100%, 호출 깊이 최대 2. `assert`는 키 셀(03·05)·파일 위치 셀(04)·02 모드 판정 열 줄·03 시스템 메시지 없음·04 기록 모양(줄 수·상태·도구 요청 수)에만 — 모델 판단·모델 글·걸린 초·토큰에 0.

## 2. 앞 챕터에서 이어 쓴 부품과 값

- **Ch 2 03**: 목록 `copy()`(02 `unpaired_names`·03 6절 — 마감 A-3·B-4에서 출처를 Ch 2 03으로 바로잡음).
- **Ch 6 06**: 「예상 비용」(요금표 어림, 청구 금액 아님)·`estimate_cost`(도구 파일 — Ch 21 판 본문).
- **Ch 13 02**: 리듀서의 「덮어쓰기」 — 02 「도구별 덮어쓰기」와 다른 말이라고 용어 표에 한 문장(마감 A-9).
- **Ch 15 01·02·03·06**: 평가 모델(judge)·판정 머리글·판정 요청 글·치우침(03) · `average`·`nearest_rank`·95 백분위수·가장 가까운 자리 방식(04 — 셀 글자 그대로 도구 파일로).
- **Ch 16 01·03**: 글 메서드 `join` · 음수 슬라이스(04).
- **Ch 17 04**: 「실행 기록의 단계를 차례대로 늘어놓은 것(단계 차례·궤적)」 — 01이 이어 씀(마감 A-1에서 정의를 이 말대로 넓힘), 「단계 차례를 맞춰 보며 평가하는 방법은 Ch 29 02절」 예고를 02가 받음.
- **Ch 18 05·06**: 코드 검사(01 b3) · 딕셔너리 `copy()`(02 마감) · 06 노트북 셀 49 저장 출력의 비교 표 다섯 줄(04 — 읽기만, 계약 §10).
- **Ch 19 01·04·05·06**: `@tool`·`: str`(03·05) · 도구 호출 요청 칸 넷·`tool_call_names` · 한 응답에 요청 여럿·`sum_usage` · 쓰기 도구·`show_messages`(모두 Ch 21 판 본문으로 도구 파일에).
- **Ch 20 01·03**: 모델 없이 손으로 만든 도구 호출 요청(01·02 궤적) · 실행 한도 설정 딕셔너리(03·05).
- **Ch 21 01·05·06 · `runner_tools.py`**: `create_agent`(모델 객체) · 검색 도구 이름 `search_documents`(빌림) · 06 비교 기록 파일 `data/rag-comparison.json`(04 — 읽기만) · 도구 파일 함수 넷의 원본(`f4113158…` — 파일째 가져오지 않음).
- **Ch 22 04**: `ModelCallLimitMiddleware(run_limit=N, exit_behavior="end")`(03 한도 4·05 한도 4와 2 — invoke 한 번마다 셈) · 한도에 닿으면 안내 메시지로 끝남(05).
- **Ch 26 04·05**: 한도가 끼운 끝 메시지(「호출 한도가 적어 넣은 글」)의 사용량 `None` · 자르기 `[:-1]` · 호출 한도를 하나 줄여 완료 조건이 `False`가 되는 실험(05 b2·b3·b6이 선례로 밝힘 — 마감 B-9·B-10).
- **Ch 27 02**: 요청 수 셈 「도구를 요청한 응답 수 + 1」(03 b3).
- **Ch 28 06**: b8이 01 슬러그로 이음(「평가 방법 세 가지를 견줍니다」 — 01 b2가 받음).
- 소재: **도서관 규정 질문 하나**(「일반 도서는 며칠 동안 빌릴 수 있나요?」, 기준 답 「일반 도서는 14일 동안 빌릴 수 있습니다.」)와 교재용 도구 둘(`search_documents(query)` — 어떤 검색어에도 LIB-001 글 · `check_source(doc_id)` — `LIB-001`만 있음). 04만 앞 챕터 기록 둘.

## 3. 절별 과제·값 (새 커널 두 번과 노트북 밖 흔들림 확인에서 같았던 값)

| 절 | 과제·입력 | 결정된 값·두 커널과 흔들림 확인 5/5가 같았던 값(결론·그림에 쓴 값) |
|---|---|---|
| 01 | 기준 궤적(검색 → 출처 확인 → 답, 메시지 6) · 견줄 궤적 넷(기준과 같음·검색 세 번·답만 틀림·차례 바꿈) · 값 바꿔 보기(답 글 「14일 동안 빌릴 수 있습니다.」) | `기준 궤적의 도구 차례: ['search_documents', 'check_source']`·`도구 요청 수: 2`·`메시지 수: 6` · 검색 세 번 → 궤적 평가만 거짓 · 답만 틀림 → 최종 답 평가만 거짓 · 차례 바꿈 → 한 단계·궤적 평가 거짓 · 답 글을 바꿔도 최종 답 평가 `False`·`두 줄이 같은가: True` · 요청 0 · 새 커널 23/23 |
| 02 | 궤적 다섯(차례 바꿈·한 응답에 요청 둘·검색만·예약을 더함·검색 세 번) × 네 모드 · 인자만 다른 궤적 셋 × 인자 비교 방식 넷 · 도구별 덮어쓰기 | 차례 바꿈·한 응답에 요청 둘 → `strict`만 `False` · 검색만 → `subset`만 `True` · 예약을 더함·검색 세 번 → `superset`만 `True` · `검색 요청 수 \| 실제: 3 \| 기준: 1` · 인자만 다름은 네 모드 모두 `False` → `검색어가 다름 \| exact: False \| ignore: True` · 인자 비교 표(exact 셋 모두 F · ignore 셋 모두 T · subset `F F T` · superset `F T F`) · 덮어쓰기 `검색어가 다름: True`·`출처 문서가 다름: False` · 요청 0 · **마감 새 커널 27/27**(출력 글 옛 판과 같음) |
| 03 | 01 답만 틀린 궤적의 궤적 글 · 평가 함수 만들기(요청 0) · 평가받는 에이전트 한 번(호출 한도 4·실행 한도 20) · 모드 넷(검색어 뺌)과 평가 모델 판정 · 답 글만 01의 틀린 답으로 | `답만 틀림: {'strict': True, 'unordered': True, 'subset': True, 'superset': True}` · 궤적 글에 답 글·검색 결과 글·호출 ID 모두 들어 있음 `True` · `요청 글의 글자 수: 1694` · (5/5 + 두 커널) 도구 차례 `search_documents` → `check_source`·`모델 요청 수: 3`·셈 `True`·시스템 메시지 없음 `False` · 네 모드 모두 `True` · 평가 모델 `칸 score: True` · 답 글만 바꾸면 `모드 strict: True`·`평가 모델 칸 score: False` · `모두 합한 모델 요청 수: 5` · 새 커널 26/28(갈린 둘은 판정 까닭 글만) |
| 04 | Ch 18 06 저장 출력(표 다섯 줄) · Ch 21 06 비교 기록(줄 셋·칸 12) → 공통 칸 여섯 · 요청 수 셈 · 평균·95 백분위수 · 값 바꿔 보기(백분위 50) | `셀 수: 58`·`표 줄 수: 5`·`옮겨 담은 줄 수: 5 \| 상태가 ok인 줄 수: 5` · `줄 수: 3 \| 한 줄의 칸 수: 12` · 공통 칸 표 여덟 줄(Ch 18 도구 요청 수 `None`) · `C01·C05·C07 \| 2 \| 1 \| True \| 1` · `Ch 18 상태가 ok인 줄: 5 \| 품질이 만점인 줄: 4 \| 전체: 5`·`Ch 21 평가 모델 판정이 참인 줄: 3 \| 전체: 3` · 평균 `요청 수 \| 2.8`·`점수 \| 0.96` / `2.0`·`1.0`·`1.0` · `95 백분위수 자리: 3 \| 줄 수: 3` · 줄 수 표(3·5·19 `True`, 20·100 `False`) · `50 백분위수 자리: 2` · 요청 0 · **마감 새 커널 25/25**(실행 시각 한 줄만 빠짐) |
| 05 | §10 | §10 |

## 4. 용어 (챕터 안에서 한 번만 정의하고 이어 씀)

| 절 | 말 | 뜻 | 코드에서 |
|---|---|---|---|
| 01 | **궤적(trajectory)** | **(마감 A-1에서 넓힘)** 에이전트가 질문에서 최종 답까지 밟은 단계의 차례. 이 챕터는 질문·모델 응답(안에 도구 호출 요청)·도구 결과·마지막 답을 일어난 차례대로 담은 **메시지 목록 전체**로 적음(Ch 17 04 「실행 기록의 단계를 차례대로 늘어놓은 것」을 이어 씀). 궤적 맞춰 보기의 모드는 그 가운데 **도구 호출 요청**을 견줌 | 메시지 목록(`make_trajectory`) |
| 01 | 도구 차례 | 모델 응답의 도구 호출 요청에서 도구 이름만 차례대로 모은 목록 — 「궤적」과 가름(옛 정의 「에이전트가 도구를 부른 차례」는 쓰지 않음) | `called_tool_names(messages)` · `['search_documents', 'check_source']` |
| 01 | 기준 궤적 | 좋은 에이전트라면 밟을 것이라고 사람이 미리 적어 둔 궤적(흐름을 보여 주려고 정한 예) | `reference` |
| 01 | 최종 답 평가 · 한 단계 평가 · 궤적 평가 | 마지막 답만 / 한 단계만 떼어 / 모든 단계를 판정(LangSmith evaluation-approaches, 원어는 괄호 소문자 한 번씩) | `final_answer_pass`·`first_step_pass`·`trajectory_pass` |
| 01 | 궤적 맞춰 보기 · 모드 `strict` | 실제 궤적을 기준 궤적과 코드 규칙으로 맞춰 봄 · 모드 `strict`는 **메시지의 수·역할·차례**와 도구 요청의 이름·인자가 모두 같아야 참, 메시지 글은 견주지 않음 — **보는 차례는 응답 사이의 차례이고 한 응답에 함께 담긴 요청끼리의 차례는 보지 않음**(마감 A-5, 설치판 `strict.py` 53~75행). 「매칭」은 02 제목에만 | `create_trajectory_match_evaluator(trajectory_match_mode="strict")` |
| 02 | 모드 `unordered`·`subset`·`superset` · 짝짓기 | 두 쪽 요청이 모두 짝을 찾으면 / 실제 요청이 모두 짝을 찾으면 / 기준 요청이 모두 짝을 찾으면 참 · 이름이 같고 인자가 맞는 요청끼리 하나씩 짝지음(횟수까지 셈) — 「집합」 금지 | `evaluators[모드]` · `unpaired_names`(이름만) |
| 02 | 인자 비교 방식 · 도구별 덮어쓰기 | `exact`·`ignore`·`subset`·`superset` — **`subset`·`superset`의 방향은 모드 `strict`·`superset` 기준**(모드 `subset`에서 거꾸로, `unordered`에서 두 방향 — 마감 A-4, 02는 `strict`에서만 견줌) · 도구마다 인자 비교 방식을 따로 정함 — **Ch 13 02 리듀서의 「덮어쓰기」와 다른 말**(마감 A-9) | `tool_args_match_mode` · `tool_args_match_overrides` |
| 03 | 평가 모델(judge) · 판정 머리글 · 판정 까닭 · 궤적 글 · 평가받는 에이전트 | Ch 15 말 그대로(원어 괄호는 03 b1 첫 자리 하나 — 마감 B-4) · 라이브러리가 적어 둔 영어 머리글 · 칸 `comment`의 글(영어, 결론에 쓰지 않음) · 역할 태그로 감싼 한 덩어리 글 · 평가할 궤적을 만드는 에이전트(「피평가」 금지) | `TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE` · `_format_inputs(…)[0]` · `library_agent` |
| 04 | 운영 지표 · 공통 칸 | 실행할 때마다 모으는 값(요청 수·도구 요청 수·토큰 수·걸린 초·성공 여부) · 서로 다른 기록의 값을 같은 이름의 칸으로 옮겨 담은 것(기록에 없는 칸은 `None`) — 「지연」·「열」·「필드」 금지 | `ch18_row`·`ch21_row`의 키 여섯 |
| (이어 씀) | 요청 수 셈 · 호출 한도 · 실행 한도 · 도구 호출 요청 · 95 백분위수 · 걸린 초 · 코드 검사 | Ch 27 02·Ch 22 04·Ch 20 03·Ch 19 04·Ch 15 06·Ch 18·21·Ch 18 05 — 한도 셋은 섞지 않음 | — |
| 05 | 한도가 끼운 끝 메시지 | 새 용어가 아니라 Ch 22 04 「안내 메시지」·Ch 26 04 「호출 한도가 적어 넣은 글」과 같은 것을 부르는 이 절의 말(b2 첫 자리에서 이음 — 마감 B-10) | `Model call limits exceeded: run limit (2/2)` |

- 대체어: 반환 → 내놓다 · 검증 → 검사 · 측정 → 재다·세다 · 사전 → 딕셔너리 · 경로 → 차례·흐름(파일이면 파일 위치) · 블랙박스 → 「안쪽을 보지 않고」 · 지연 → 걸린 초 · 옵션 → 설정·인자 · 루브릭 → 판정 기준 · 프롬프트 → 판정 머리글·요청 글 · 피평가 에이전트 → 평가받는 에이전트 · 지시 → 말(마감 03 [29]).
- **쓰지 않는 말**(다섯 절 설명·주석·캡션·`.mmd`·README·`objectives` 0 — 제목·슬러그·코드 백틱 말고): Ch 28 목록 + 「반환」·「검증」·「측정」·「추정」·「지연」·「경로」·「스키마」·「사전」·「프롬프트」·「루브릭」·「효율」·「결정적」·「명시」·「매칭」(02 제목 밖)·「판정 모델」·「평가셋」 · 사용자 금지 표현. 참고 자료 원제목 「LangSmith Trajectory evals」는 거짓 양성(`/tmp/ch29-04/tools/ban29.py` — 마감 전후 대조).

## 5. 비유 가족 「오르골 종이띠」 (삽화 다섯)

- 01-5 닫힌 나무 오르골 상자에서 나온 띠 하나와 첫 구멍·끝의 돋보기 둘, 아래 떨어진 기준 띠(상자 = 에이전트, 띠 = 궤적, 돋보기 = 한 단계·최종 답 평가, 나란히 둔 모습 = 궤적 평가 — **마감 A-1로 「구멍을 차례대로 읽어 끝 소리까지 내는 띠 한 줄이 궤적」**, 그림 읽기에 「두 띠가 같은 궤적인지도 나타내지 않습니다」를 더함 — A-2) · 02-5 가로로 쌓은 띠 다섯과 둥근·네모·세모 구멍(구멍 하나 = 도구 요청 하나, 구멍 차례 = **도구 차례**) · 03-5 비켜 겹친 띠 둘 ↔ 상자 없는 오르골 기계 둘(겹쳐 보기 = 모드, 울려 보기 = 평가 모델) · 04-5 나무 막대 하나에 걸린 띠 여덟(다섯·셋 두 무리 — 막대 = 공통 칸 표, 띠 = 기록 한 줄; **마감 B-5·B-7로 비유 글을 그림에 맞춤**: 두 가게가 서로 다른 막대에 걸던 띠를 한 막대에 옮겨 걺, 「걸어 둔 띠는 다시 세어도 같지만 곡을 다시 울리면 새 띠는 달라질 수 있음」, 기록표는 「비유와 다른 점」) · 05-4 나무판 둘에 붙인 같은 길이의 띠와 점 찍은 카드(끝이 구멍 무리 ↔ 회색 종이 = 모델이 쓴 답 ↔ 한도가 끼운 끝 메시지, 점 셋·둘 = 요청 수).
- 사람·손·글자·숫자·음표·화살표·화면 없음. 짝짓지 않는 요소(구멍 수·띠 길이·기울기·손잡이·빈 고리·핀·나뭇결)는 그림 읽기에 밝힘. 작업 조회 결과의 모델 표시 `nano_banana_2` ↔ 요청 `nano_banana_pro`(기록만). 마감은 삽화를 다시 만들지 않음(Higgsfield 0).

## 6. 색 규칙 (Mermaid 19장)

- 코드로 적은 자료·값(질문·답 글·도구 요청 목록·결과 글·궤적 메시지·앞 챕터 기록) **초록(tool)** · 우리 코드(정의한 함수·만든 평가 함수·조립 함수)와 값 바꿔 보기에서 **바꾼 값 파랑(flow)** · 출력으로 확인한 값 **노랑(measure)** · 라이브러리가 정한 것·설치판 소스로만 본 것·여러 조건 공통 값·기록에 없는 칸 **회색** · **보라 = 그 절에서 실제로 부른 모델만**(03-3 에이전트·평가 모델, 05-1·05-2 에이전트 모델 — 01·02·04와 03 앞 절반 보라 0) · **빨강 0**(다섯 절 모두 experiment).
- 원본 viewBox 폭 모두 868 이하. 라벨에 판정 까닭·토큰·초 값 없음. 평가 모델 점수 라벨은 흔들림 확인 5/5 **그리고** 새 커널 두 번 같을 때만(03-3·03-4 캡션에 한정어 — 마감 B-1).
- **마감에서 다시 렌더한 `.mmd` 하나**: `04-3-세는-값으로-읽기`(칸 제목 「Ch 18 기록 다섯 줄」·「Ch 21 기록 세 줄」 — B-5). 나머지 18장은 렌더 도장 같음(`skip`).

## 7. 결정적 값과 흔들린 값

- **결정된 값**(결론·그림·정리·복습에 쓴 값): §3 표 전부. 01·02는 코드로 적은 궤적과 라이브러리 규칙이라 모두 같고, 04는 저장된 기록을 읽어 같음(새 커널 두 번 셀별 출력 같음). 03·05의 모델 판단 값(도구 차례·요청 수·평가 모델 점수)은 노트북 밖 흔들림 확인 5/5와 두 커널에서 같을 때만 「노트북 밖 다섯 번과 두 커널에서 모두」로 한정해 씀. 결론의 중심은 셈 **요청 수 = 도구를 요청한 응답 수 + 1**(답까지 간 실행에서만 — 05 실행 2에서는 맞지 않음).
- **04 「세는 값」 분류(검토 B-5 — 챕터 리드 결정으로 마감에서 고침)**: 두 기록의 값은 **모두 앞 챕터를 한 번 실행해 남긴 값**. 노트북 출력은 기록을 읽기만 해 몇 번을 실행해도 같지만, 앞 챕터를 다시 실행하면 바뀜. Ch 18 요청 수 2·2·3은 코드가, 5·2는 모델 답이 정한 작업 수·바퀴 수에서 나옴 · Ch 21 도구 요청 수 1은 모델이 고른 값 · 평가 판정은 평가 모델이 한 번 내린 값. 다시 실행해도 그대로인 것은 짜임새가 정한 **셈**뿐 → 결론은 「이 기록에서 센 값」과 「셈이 기록과 맞는지」로, 두 짜임새의 일반 성질은 정하지 않음. 옛 판의 「세는 값은 흐름의 짜임새를 따름, 걸린 초·토큰만 한 번 실행한 값」은 쓰지 않음.
- **흔들린 값 — 결론·그림·정리·복습에 쓰지 않음**(결과 읽기 둘째 단락·b6 표·b7에만): 판정 까닭 글(영어) · 에이전트가 쓴 검색어·답 글 · 토큰 수·예상 비용(03 에이전트 933·63·0.000983달러, 평가 모델 판정 한 번 입력 679~682·출력 87~104 — 마감 B-3에서 노트북 [59]를 이 범위로) · 04 걸린 초·토큰 수(두 기록 한 번 실행 값) · 05 토큰 996·615.
- **노트북 밖에서만 본 값(b7에 「노트북 밖」 표시)**: 01 질문 글·도구 결과 글·호출 ID만 바꾼 궤적도 `strict` 참 · 02 모드 `subset`·`unordered`와 인자 비교 방식을 섞은 결과 · **마감 B-8로 「모델 대신 정해 둔 응답」 실행을 근거로 한 세 문장을 교재에서 뺌**(03 그래프 단계 12 → 「이번에 세지 않았습니다」 · 05 한도 1 → 02 네 모드 뜻으로 셈한 예상 + 「이번에 실행하지 않았습니다」 · 05 `sum_usage` `TypeError` → 도구 파일 88~96행 코드 사실).
- **재지 않은 것·실행하지 않은 것**: 걸린 시간(모든 절) · Windows·macOS 실행 · 다른 모델로 판정(03 자기 판정) · 한도 1 실행 · 01 최종 답 평가로 05 실행 2 판정 · `continuous`·`choices`·기준 없는 머리글 · 한 응답 안 요청 차례를 바꾼 궤적의 `strict` 판정(설치판 소스로만).

## 8. 파일 쓰기·읽기와 노트북 작업 폴더

- **노트북 파일 쓰기 0**(01~05 모두). 읽는 파일: 도구 파일(01~05) · `.env`(03·05) · Ch 18 06 노트북·Ch 21 06 비교 기록(04).
- 작업 폴더 `notebooks/` — 다섯 노트북 모두 도구 파일을 가져오므로 커널이 `notebooks/` 폴더에서 시작해야 함(마감 A-10으로 다섯 노트북 가져오기 결과 읽기에 Part 6 두 문장). 04 파일 위치 셀은 후보 셋(`.`·`../../..`·`../../../..`).

## 9. 모델 요청 수와 예상 비용

| 절 | 노트북 한 번 | 흔들림 확인(노트북 밖) | 시험 실행 | 새 커널 A + B | 작업 전체 | 예상 비용 어림(작업 전체) |
|---|---|---|---|---|---|---|
| 01 | 0 | 0 | 0 | 0 + 0 | **0** | 0 |
| 02 | 0 | 0 | 0 | 0 + 0(마감 재실행도 0) | **0** | 0 |
| 03 | 5(에이전트 3 + 평가 모델 2) | 25(5회 × (3 + 2)) | 5 | 5 + 5 | **40**(에이전트 24 + 평가 모델 16) | 약 0.023달러 |
| 04 | 0 | 0 | 0 | 0 + 0(마감 재실행도 0) | **0** | 0 |
| 05 | 5(실행 1 = 3 + 실행 2 = 2) | 25(5회 × (3 + 2)) | 0 | 5 + 5 | **35** | 약 0.0113달러 |
| 합 | 10 | 50 | 5 | 20 | **75**(마감 0) | **약 0.034달러** |

- 다시 센 방법(마감): `probe/probe-03-A.jsonl`(회차 다섯 — 칸 `requests` 3씩·`judge_agent`·`judge_wrong` 둘씩 = 에이전트 15 + 평가 모델 10) · `probe-05-R.jsonl`(회차 다섯 — `run1.requests` 3·`run2.requests` 2) · 기기 `/tmp/ch29-03/try-executed.ipynb`·`A.ipynb`·`B/…` 출력 `모두 합한 모델 요청 수: 5` 셋 · `/tmp/ch29-05/A.ipynb`·`B/…` 출력 `모델 요청 수: 3`·`2` 둘(05 시험 실행은 요청 0 — 05 진단 §11). 인계의 절별 값과 같음.
- 예상 비용은 과정 요금표(2026-09-17, mini 입력 0.75·캐시 입력 0.075·출력 4.50달러/100만 토큰)로 어림한 값이고 청구 금액이 아님. 절마다 1달러 안. 05는 실습 절 기준 3~5번 안(5번). 노트북 한 번 예상 비용: 03 약 0.003달러 · 05 0.002달러 아래.

## 10. 05절 실습 절 주제와 결과

- 제목 「**Agent 평가 실습: 호출 한도를 줄인 실행을 궤적과 운영 지표로 견주기**」, 슬러그 `05-Agent-평가-실습`, `format: experiment`, meta 「실습 30분 · 새 용어 0」. **챕터 시수에 더하지 않습니다**(규격 §7-2). 01~04 meta 합 강의 0.75h × 4 = **3h** · 실습 1.25h × 4 = **5h** = `chapter.json` 「총 8h · 강의 3h · 실습 5h」(`_build_index.py`도 3·5).
- 붙인 앞 절 기능 셋(두 실행 모두 흐름 안에서 쓰임): **03** 평가받는 에이전트(`@tool` 둘 03 셀 글 그대로·`create_agent`·요청 수 셈) · **02** 네 모드와 도구별 덮어쓰기(`four_modes` + `search_documents` `ignore`) · **04** 공통 칸(칸 여섯·`show_row`). 뺀 것: 03 평가 모델(요청 7이 됨) · 01 최종 답 평가(흔들리는 답 글 — 마감 B-12로 「실행 2의 끝 메시지 글이면 거짓이 될 것」 셈 한 문장) · 04 95 백분위수(줄 둘이면 늘 가장 큰 값).
- 실행 1(호출 한도 4) → 실행 2(**값 하나 호출 한도 2**). 모델 요청 **5번**(3 + 2). b2 「새로 볼 것」은 이 챕터의 평가(네 모드·공통 칸·요청 수 셈)가 한도에 닿은 실행을 어떻게 판정하는지(한도 끝 모양은 Ch 22 04, 사용량 `None`은 Ch 26 04, 한도를 하나 줄인 실험·완료 조건은 **Ch 26 05** — 마감 B-9로 선례를 밝힘).
- 결과(새 커널 두 번 24/24 같음·`outputs_sha256`까지 + 노트북 밖 5회차, 모든 칸 5/5): 두 실행 모두 도구 `search_documents` → `check_source`, 메시지를 차례대로 본 출력은 호출 한도 줄 말고 같음 · 실행 1 요청 3·도구를 요청한 응답 2·셈 `True` · 실행 2 끝 메시지 `Model call limits exceeded: run limit (2/2)`·사용량 없음 `True`·요청 2·응답 2·**셈 `False`** · **두 실행 모두 네 모드 `True`** · 공통 칸 두 줄 점수 1.0 · `점수가 1.0인 실행: 2 | 셈이 맞은 실행: 1 | 전체 실행: 2` → **「노트북 밖 다섯 번과 두 커널에서 모두, 도구를 모두 부른 뒤 한도에 닿은 실행은 답을 쓰지 못했어도 네 모드로는 통과했고, 요청 수 셈과 끝 메시지의 사용량 기록이 가려냈다」**.
- 코드 셀 24(실습 선례 19~28) · 코드 줄 143 · 함수 본문 최대 8줄(`run_row`). `assert`는 키 셀뿐. 셀 [22] `print("두 값의 출처: …")`는 손으로 적은 글이라 결과 읽기에 「코드가 견준 값은 아닙니다」(마감 B-11 — 코드 고침은 다음 재실행 몫).

## 11. 도구 파일 `notebooks/eval_tools.py` — 함수 표·해시 변천·생성기 대조 사슬

| 함수(인자) | 배운 곳 | 가져오는 절 | 하는 일 |
|---|---|---|---|
| `tool_call_names(response)` | Ch 19 04(Ch 21 판) | 01·03·05 | 응답 하나의 도구 호출 요청 이름 목록 |
| `show_messages(messages)` | Ch 19 06(Ch 21 판) | 01·03·05 | 메시지 목록을 한 줄씩 출력 |
| `make_trajectory(question, calls, results, answer)` | **Ch 29 01** | 02·03·05 | 질문·요청 목록·결과 글·답 글로 궤적(메시지 목록) |
| `called_tool_names(messages)` | **Ch 29 01** | 02·03·05 | 도구 차례 |
| `trajectory_pass(messages, reference, evaluator)` | **Ch 29 01** | 02·03 | 결과 딕셔너리에서 칸 `score`만 |
| `four_modes(messages, reference, evaluators)` | **Ch 29 02** | 03·05 | 네 모드의 점수 딕셔너리 |
| `sum_usage(messages)` | Ch 19 05(Ch 21 판) | 03·05 | 응답마다 요청 하나·토큰 합(사용량 `None`이면 `TypeError` — 88~96행) |
| `estimate_cost(usage, input_rate, cached_input_rate, output_rate)` | Ch 6 06(Ch 21 판) | 03 | 예상 비용(`.get` 둘 — 허용 표시, 본문 9줄 — 원본 그대로) |
| `average(values)` | Ch 15 06 노트북 셀 | 04 | 평균(소수 여섯째 자리까지) |
| `nearest_rank(values, percent)` | Ch 15 06 노트북 셀 | 04 | 가장 가까운 자리 방식 백분위수 |
| `show_row(row)` | **Ch 29 04** | 05 | 공통 칸 딕셔너리 한 줄을 표 한 줄로 |

- 가져오기 줄 `from langchain.messages import AIMessage, HumanMessage, ToolMessage`·`import math`(표준 라이브러리) → **이 파일을 가져오는 01~05 설치 셀 모두 `langchain==1.4.0`**(규격 §2-7 6번). 노트북 전역 이름 기대기 0, 금지 문법 0.
- **해시 변천**: 없음 → 01 `dab0888f…`(함수 둘) → 02 `4a3d8143…`(+ 01 셀 셋, 가져오기 줄) → 03 `617a82bc…`(+ `four_modes`·`sum_usage`·`estimate_cost`) → 04 `223881ec…`(+ `average`·`nearest_rank`, `import math`) → 05 **`d624b8f360c993e5f93d779dbf58f3ad41e60f6bd47dda2c3aecd9c5da6f0af9`**(+ `show_row`) → **마감 그대로**(챕터 리드 결정 — 02·04 마감 재실행도 이 05판, 02·04 생성기 가드 `skip`).
- **머리 설명**(검토 A-14·B-15): 「Ch 21 도구 파일에서 옮긴 함수」·「이 챕터 앞 절 노트북에서 옮긴 함수」 두 경우만 적고, **Ch 15 06 노트북 셀에서 옮긴 `average`·`nearest_rank` 출처가 머리에 없음**(함수 위 주석에는 있음) · 가져오기 줄 주석의 「N절에서 옮긴」이 두 뜻 · `average` 주석 「여섯째 자리에서 반올림」(Ch 15 원본 글자). 내용은 바꾸지 않고 Ch 24~27 「도구 파일 머리 설명」 전체 마감 항목에 덧붙임(최종 점검표 §2-13 6번). README가 함수 열하나의 배운 절·가져오는 절을 적음.
- **생성기 대조 사슬**(마감에서 다시 확인 — 모두 통과, 쓰기 없음, `.cache/ch29-close/tools/chain29.py`): `author_01.TOOLS_HEAD`·`TOOLS`·`strip_later_imports` → `author_02.TOOLS`(01판 + 가져오기 줄 + 01 셀 셋, 셀 글 해시 고정) → `author_03.TOOLS` → `author_04.TOOLS`(Ch 15 06 셀 글자 대조) → `author_05.TOOLS`(04 셀 `show_row`, 04 디스크 셀·AST 대조) = **디스크 파일**. 01 가드 「`strip` 뒤 01판으로 시작·같지 않음 → skip」, 02·03·04 `later_version` 참 → 다시 돌려도 덮어쓰지 않음(02·04 마감 재실행에서 `skip` 확인). 다섯 생성기 셀 글이 노트북과 49·57·60·53·52셀 차이 0, `src_html()` = `_src` 5/5, `check_tools`·`check_same_as_prev`·`check_same_as_probe`·`check_contracts` 통과. 설명만 고칠 때는 `.cache/ch29-close/tools/gapply29.py`(치환 수·코드 셀 대조) → `run_section.sh … NN --no-exec`.
- **전체 마감 2026-09-30: 머리 줄 고침, 새 해시 `b75636c4f0cb6bc2719d2f0bfa22a6840ac7acf2b28bc67e6f974c266bcc0a47`**(검토 A-14·B-15 · 체크리스트 §2-13 6번). 7행(Ch 21 줄) 뒤에 「Ch 15 06절 노트북 셀에서 옮긴 함수(average·nearest_rank)도 그 셀의 주석과 본문을 글자 그대로 옮겼습니다.」 한 줄만 더함(머리 설명 12 → 13줄). 1행(「앞 챕터와 이 챕터에서 배운 …」)·나머지 줄·가져오기 두 줄과 그 주석·함수 열하나 본문은 AST·글자 같음. **그대로 둔 것**: 가져오기 줄 주석 「01절에서 옮긴 함수 make_trajectory …」·「04절에서 옮긴 함수 nearest_rank(Ch 15 06절) …」의 두 뜻(A-14 둘째 — 머리 설명 밖, `author_02.TOOLS_IMPORTS`·`author_04.MATH_IMPORT` 상수) · `average` 위 주석 「여섯째 자리에서 반올림」(Ch 15 06 셀 글 그대로 — 규격 §2-7 글자 그대로, 과정 인계). 생성기 안 판: 01 `dab0888f…` → `7f32d8fb…` · 02 `4a3d8143…` → `10f26b96…` · 03 `617a82bc…` → `b1fd3492…` · 04 `223881ec…` → `14dc76c9…` · 05 = 디스크. 고친 생성기: `author_01.TOOLS_HEAD`(한 곳) · 판 해시 고정값 셋 — `author_03` `check_tools()`의 02판 줄 · `author_04` `check_tools()`의 03판 줄 · `author_05.TOOLS_04_SHA`(각각 설명 한 줄). 앞서 Ch 27 머리 줄 고침으로 `author_01.HARNESS_SHA`도 새 값. **뒤 챕터 고정값**: Ch 34 `author_01.EVAL_TOOLS_SHA`(`author_05`도 이 값을 씀)를 새 값으로 — Ch 34 여섯 생성기 `--src-only`·04·06 `--guard-check`를 쓰기 없이 돌려 통과(`cost_tools.py` `9fd98846…` 그대로, 05 `--guard-check`는 디스크가 05 판일 때만 도는 확인이라 전과 같이 멈춤). 조건 넷: (가) 노트북 다섯 마크다운·출력과 `_src`·HTML·README에 머리 글·판 해시 0 · (나) 다섯 생성기를 파일 쓰기를 가로챈 채(`.cache/final-close/2-tools-head/tools/dryrun.py`) `--src-only`와 인자 없는 모드로 돌림 → `_src` 다섯 바이트 같음, 01~04 가드 `skip`, 05 `same`, `check_tools` 다섯(판 흉내 `later_version` 포함) 통과, `cells()`가 노트북과 49·57·58/60·53·52셀 같음(03의 다른 둘은 모델 값 자리 표시를 `mdpatch`로 채운 셀 — 고치기 전과 같음) · (다) 모델 없는 01·02·04 사본(`.cache/final-close/2-tools-head/ch29/notebooks`, 키 없이, 커널 자리는 교재 출력 때와 같은 저장소 맨 위)을 새 커널로 돌려 셀별 23/23·27/27·25/25(01·04는 설치 셀 스트림 나뉨만), 모델 절 03·05는 가져오는 이름(8·7개)이 새 파일에 있고 함수 본문 AST가 옛 파일과 같음만 확인 · (라) 이 줄·handoff·계약 §4. 노트북 `code_sha256`·`outputs_sha256` 전후 같음.

## 12. 계약 (Ch 21 06·Ch 18 06 — 읽기만)과 묶음·검사

| 파일 | 해시(마감 전후 같음) | 04가 읽는 것 | 학생 묶음 안 자리(`part6-practice/`) |
|---|---|---|---|
| `labs/part6/ch21-create-agent/data/rag-comparison.json` | `25cfe5df3cfd729c130bce4af26c716cfcc3bcd4b4ff6e4a9d0a725816b02f51` | 줄 3(`C01`·`C05`·`C07`) · `qid`·`agent_usage`{`model_calls`·`input_tokens`·`output_tokens`}·`agent_supported`·`tool_calls`·`agent_latency_s`·`agent_trace` · 줄 수·도구 요청 수 `assert` | `labs/part6/ch21-create-agent/data/rag-comparison.json` |
| `labs/part5/ch18-workflow-patterns/notebooks/06-같은-과제로-다섯-패턴-비교.ipynb` | `5ba7f5a01fa8a8625a4673e6f6a007691907078b20c41ee828aa266252ba0b20` | 셀 49 저장 출력의 `" \| "` 줄(머리 `pattern` 뺌) 마지막 다섯 · 셀 수 — **`metadata.verification.executed_at`은 마감 B-6 (나)로 읽지 않음** | `labs/part5/ch18-workflow-patterns/notebooks/06-같은-과제로-다섯-패턴-비교.ipynb` |

- 새 인용값(04 절 작업에서 옛 값 → 새 값, 마감 그대로): Ch 18 평균 0.96·2.8·862.2·4.206 · Ch 21 평균 1.0·2.0·1.0·688.0·1.731 · p95 2.003·699 · 표 줄 5. **Ch 21 06 b10 문장**(마감에서 고침 — §13): 「Ch 29 04절 노트북의 코드 셀 13~25가 이 절의 비교 기록 파일을 읽어 씁니다. 코드 셀 13과 15는 줄 수와 도구 호출 수를 `assert`로 확인합니다」(실행 번호 [13]~[25], 0부터 센 셀 번호 27~51).
- **묶음**: `python3 -B textbook/part6/_build_index.py`(README·`chapter.json`·목차 줄·continuity-guide·노트북을 모두 고친 뒤 마지막에 한 번) → **`Part 6: 56 verified sections; 110 bundled files`**, `part6-practice.zip` `f5d87d66…` → **`6d746be1ac649c102ee93475d897ae87e52b9876d2b131389a766a58afabb487`**(113항목, **Ch 29 아홉 항목·앞 챕터 기록 둘·`continuity-guide.md`가 디스크와 같음**, `__pycache__`·`.pyc`·`.env`·`.venv` 0). 공개 목록: 챕터 목록에 옛 그림 줄 없음(그대로), Part 목록은 `collect_public_files.py`로 다시 모아 바이트 같음(`47429ce7`, `Explicit public files: 94; prerequisites: 13`) — 도구 파일·05 노트북 줄 있음.
- **04 묶음 실행**: 새 zip을 풀어 `notebooks/`에서 키 없이 **PASS 25셀**, 24/25 같음(셀 3 `고른 자리: ../../../..` — 노트북 [8]이 밝힌 차이).
- **묶음 실행 검사 계약**(Part 6 `check_bundle_execution.py` — 목록은 Ch 24 01·Ch 28 01, Ch 29 없음): `UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache UV_LINK_MODE=symlink` 환경 변수만(스크립트 수정 0, `TMPDIR`은 세션 홈 `/sessions/…/tmp` — 맥 마운트 밖, 키 환경 변수 지움) → **PASS**(Ch 24 01 `7187f7a39f3f…` 28셀 · Ch 28 01 `2407c4c57138…` 25셀). `bundle-execution.json` `fc4e1b78` → **`f858a5caa61f5252f3ead767ec6ee069f672f0ea4db8ded84ccda4c2aa0fa3c9`**(`archive_sha256` = 새 zip). **Ch 29 01·02·04는 모델·키 없이 도는 절이라 목록 후보**(검토 A-16·B-13 — 마감은 검사 스크립트를 고치지 않음, 최종 점검표 §2-17).
- **전달 검사**(Part 6 `check_delivery.py`): 117행 `llm-practice.zip`의 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`에서 멈춤(알려진 일, `delivery-results.json` `3cc2d143…` 안 바뀜). 그 zip을 뺀 사본(`.cache/ch29-close/dx/check_delivery_nollm.py` — 바꾼 줄 셋: 루트·zip 목록·결과 파일 자리)은 **HTML 67 · 로컬 링크 1,628 · 누락 0 · 절 56 · 코드 셀 1,369 · 복습 224문항 오류 0 · SVG 260 · 비밀값 0 · 개인 경로 0 · `part6-practice.zip` 113항목(part6 노트북 56)** 통과.
- **화면 검사** `visual.cjs`(1280px·390px): **12행 PASS**(`textbook/_notebook/checks/ch29-agent-evaluation/visual-results.json` + 스크린숏 넷 새로). Ch 21 06은 원본과 바이트 같은 사본(`/tmp/ch29-close/vis/visual.cjs`)으로 돌려 Ch 21 여덟 쪽 16행 PASS(결과는 `/tmp`에만 — Ch 21 챕터 결과 파일은 고치지 않음). Part 6 공용 `qa/visual-results.json`은 **Ch 29 줄만 10 → 12**(05 두 줄 더함, 새 HTML 해시) + **Ch 21 06 두 줄 새 해시**, `screens` 130 → 132, 다른 줄 118개 그대로(Part 6·전체 `index.html` 줄은 옛 해시 — Part 6 마감 때).
- **옛 검사 스크립트(고치지 않음, 돌려서 멈춘 자리만 기록)**: Part 6 `check_scope.py` — Ch 21 07 `Missing scope`에서 멈춤(Ch 29에 닿기 전, **`SECTION_COUNTS` ch29 4 ≠ 5**도 남음) · `check_figures.py` — Ch 21 `01-1-한-줄이-만든-에이전트-그래프.svg`의 `.excalidraw` 짝 · `check_notebook_readiness.py` — `assert len(reports) == 47`(Part 6 노트북 56), **결과 파일 `notebook-readiness.json`을 먼저 씀 → 실행 전 사본으로 되돌림**(`b3d69e9c…`, 사본과 바이트 같음) · `check_visual_reports.py` — **Ch 21 `01-create-agent와-ReAct-루프.html`에서 `Stale visual report`**(마감이 Ch 21 `_build.py`로 HTML 여덟을 다시 써 수정 시각이 바뀜 — 내용이 바뀐 것은 06 하나, Ch 28 마감 때는 `ch22-middleware`에서 멈췄음) · `textbook/qa/check_course_continuity.py`(챕터 가상환경 3.12로) — `llm-practice.zip` Part 1 Stale에서 멈춤(결과 파일 안 바뀜).

## 13. 챕터 밖 수정 (전부 목록)

| 파일 | 언제 | 무엇을 |
|---|---|---|
| `labs/part6/ch29-agent-evaluation/notebooks/01~05-*.ipynb` | 01~05절 · **마감** | 실습 폴더(챕터 몫) — §1·§19. 마감: **02·04만 다시 실행**(02 `8e80cc8d…` → `238911432b50…` · 04 `43163e6a…` → `4ed26b54f6ff…`), 01·03·05는 마크다운만(코드·출력·`executed_at` 그대로) — 파일 01 `debd4640`→`a693de5c` · 02 `abdd6dc3`→`934cc954` · 03 `41e79afe`→`36378027` · 04 `95dfbec8`→`76c112f6` · 05 `053ab017`→`18313379`. 도구 파일 그대로 `d624b8f3…` |
| `labs/part6/ch29-agent-evaluation/README.md` | 05절(05 단락) · **마감(전체)** | `e252d099…`(원본) → `8be9903b…` → **`b108b2d35b5f…`**: 노트북 다섯, `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 절별 설치 판, **모델 요청 01 0 · 02 0 · 03 5 · 04 0 · 05 5**, 01·02·04 키 없음·03·05 키 필요, 예상 비용(요금표 어림, 청구 금액 아님), 키는 프로젝트 맨 위(학생 묶음이면 `part6-practice/`) `.env`의 `OPENAI_API_KEY`에서만, **04가 읽는 앞 챕터 기록 둘의 묶음 안 자리와 「두 절을 다시 실행하지 않음」**, 도구 파일 단락(규격 §2-7 고정 문장 뜻·함수 열하나·배운 절·가져오는 절·`langchain`·`math`), 절마다 하는 일, 05 단락. 옛 「저장된 실제 궤적과 결정적 평가」·「LLM judge」 뺌, 묶음 밖 파일을 가리키지 않음, 금지어 0 |
| `textbook/part6/ch29-agent-evaluation/chapter.json` | 05절 · **마감** | 05 절(05절) · `objectives` 둘 → **다섯**(§15), `hours` 그대로(`4e565b61` → **`174ae411`**, 보호 파일) |
| `textbook/part6/ch29-agent-evaluation/index.html` | 05절 · **마감** | `_build.py`(목표 다섯, `2821043d` → `1b9b3fb0`) |
| `textbook/part6/_build_index.py` | **마감** | ch29 설명 「최종 답변·한 단계의 선택·전체 궤적을 평가하고 운영 지표를 비교합니다.」 → 「질문 하나와 기준 궤적으로 최종 답·한 단계·궤적 평가가 보는 자리를 견주고, 궤적 맞춰 보기 네 모드와 인자 비교 방식의 판정 차이를 본 뒤, 실제로 실행한 에이전트 궤적을 네 모드와 평가 모델로 함께 판정하고, 앞 챕터 실행 기록을 공통 칸으로 옮겨 요청 수 셈과 95 백분위수로 읽으며, 호출 한도만 바꾼 두 실행을 견주는 실습을 합니다.」(시수 3·5 그대로, `2020202a` → `66943bb4`, 보호 파일) |
| `textbook/_notebook/build_index.py` · `textbook/index.html` | **마감** | Ch 29 설명 → 「최종 답·한 단계·궤적 평가가 보는 자리와 궤적 맞춰 보기 네 모드의 판정 차이를 보고, 에이전트 궤적을 평가 모델로 판정하며 운영 지표를 셉니다.」. **절 수 4는 그대로**(실습 절을 빼고 세는 과정 약속). 다시 만든 `index.html`에서 바뀐 것은 Ch 29 설명 하나(Ch 21 설명 그대로 — `cde0dc13` → `b21bb749` · `64bfbb36` → `fc7fdde3`, 보호 파일) |
| `labs/part6/continuity-guide.md` | **마감** | Ch 29 줄 「Ch15의 평가 항목과 Ch18의 실행 기록 \| Ch29 답변·선택·궤적 평가 \| 최종 프로젝트의 평가 설계」 → 「Ch15의 평가 모델과 95 백분위수, Ch17의 단계 차례, Ch18·Ch21의 실행 기록, Ch22의 호출 한도 \| Ch29 최종 답·한 단계·궤적 평가, 궤적 맞춰 보기 네 모드와 인자 비교 방식, 실제 에이전트 궤적을 평가 모델로 판정, 앞 챕터 실행 기록을 공통 칸으로 옮겨 요청 수 셈과 95 백분위수로 읽기 \| Ch33 평가 회귀 검사의 궤적 기준과 모니터링 지표」(Ch 33 02 「Ch29의 궤적 기준」·04 「Ch29에서 운영 지표를 정의」를 확인, `f549f3ad` → `15b2dd3c`, 보호 파일, 묶음에 들어감) |
| `textbook/part6/index.html` · `textbook/downloads/part6-practice.zip` · `textbook/part6/qa/integration-results.json` | 05절 + **마감** | §12 — `index.html` `a8c95c20` → `d909e971`(Ch 29 섹션 설명 한 줄만), zip → `6d746be1`, `integration-results.json` `0526eb39` → `67c362bd` |
| `textbook/part6/qa/bundle-execution.json` | **마감** | §12(`fc4e1b78` → `f858a5ca`) |
| `textbook/part6/qa/visual-results.json` · `textbook/_notebook/checks/ch29-agent-evaluation/visual-results.json`(+ 스크린숏 넷) | **마감** | §12 — 공용 파일은 Ch 29 줄 10 → 12 + Ch 21 06 두 줄·`screens` 132(`24d74549` → `d8c16739`, 보호 파일), 챕터 결과·스크린숏 넷(index·01 × 1280·390) 새로 찍음 |
| `textbook/part6/qa/notebook-readiness.json` | **마감(되돌림)** | 옛 `check_notebook_readiness.py`가 멈추기 전에 다시 써서 실행 전 사본으로 되돌림(내용 변경 0, `b3d69e9c…`) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch29-agent-evaluation.json` · `…-ch21-create-agent.json` | 절마다·마감 | `verify.py --chapter`가 다시 씀(Ch 29 마감 뒤 `662d2a2f…` · Ch 21 `b8a4f912…` — Ch 21 요약 기록 값과 같음) |
| **Ch 21 06 b10 문장**: `textbook/part6/ch21-create-agent/_src/06-같은-평가셋으로-RAG-비교.html` · `qa/upgrade/author_06.py` · `06-같은-평가셋으로-RAG-비교.html` | **마감** | 「Ch 29 04절 노트북 12~18번 셀이 …」 → §12의 새 문장(`_src` `556759eb` → `f2cb4ac5` · 생성기 `137ddee4` → `c19c22f3` — `src_html()` = `_src` 전후 모두 참 · HTML `f1c735dc` → `73df1a27`). **Ch 21 06 노트북은 이 문장이 없어 손대지 않음 — 코드 `ca14949bb0f9…`·출력 `1ded374d9f64…`·파일 `8a6f9da7…`·`executed_at` 2026-09-25T05:11:56Z 그대로, `data/rag-comparison.json` 그대로, Ch 21 06을 실행하지 않음.** Ch 21 `_build.py`가 HTML 여덟을 다시 썼고 내용이 바뀐 것은 06 하나(나머지 일곱 해시 같음, 수정 시각만 바뀜). `verify.py --chapter` Ch 21 **PASS 7 sections / 180 code cells** |
| **`.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part6b_enrich.py`·`part6b_review_fixes.py`** | **마감(검토 A-13)** | `from __future__` 줄 뒤에 설명 주석 세 줄 + `raise SystemExit(…)` 한 줄만 더함(내용 그대로 — 사본 `.cache/ch29-close/pre/.moai/…`와 `diff` 네 줄 더함뿐). `8528cb33…` → **`11ffa9fa914ccd4bfdad7b2704961d5e0b80138a362d42bcdad3e5cde905504f`** · `a0299166…` → **`fea9f8c76c3ee2125ece8788801dc7d6661f6e497dd031580ec1adccdaebbe61`**. `/tmp` 사본 실행으로 둘 다 안내 글과 종료 코드 1로 멈춤 확인. 옮기지는 않음 |
| **`textbook/part6/_author_ch21_ch29.py` → `qa/upgrade/before/generators/blocked/_author_ch21_ch29.py`** | 01절(막음) · **마감(`mv -n`)** | `391be055548853cce07c7f79cebc2c071751cbe37efb9e403c5df07ba53c5edf` 같음(Ch 21·29 모두 마감 — 공용 옛 생성기). 부르는 빌드·검사 스크립트 0(`grep` — `textbook`·`labs`·`qa`·`.moai`의 `.py`·`.sh`·`.cjs`·`.js`) |
| **`figures/_gen_figures.py` → `qa/upgrade/before/generators/blocked/_gen_figures.py`** | 01절(막음) · **마감(`mv -n`)** | `3577112dba8d97f8e1a65f7dd7219eaa6a3bf6fe70d4c9e43ad7ba470bcf8095` 같음. 부르는 스크립트 0(Part 7 `check_figures.py`는 Part 7 챕터 자기 파일만). `before/generators/`의 두 원본 사본(막기 전)은 그대로 |
| `textbook/part6/ch21-create-agent/qa/upgrade/chapter-summary.md` · `textbook/qa/upgrade-final-checklist.md` | **마감** | Ch 21 요약 옛 생성기 항목(231행)에 「옮김」 한 줄 덧붙임 · 체크리스트 §2-10 2번에 「옮김」 한 줄 덧붙임, §2-13 6번에 Ch 29 줄, §2-17 Ch 29 항목, §3·§4 Ch 29 줄 |
| `textbook/qa/upgrade-progress.md` | **마감** | Ch 29 행 한 줄 |

- **고치지 않은 것**: `textbook/QUALITY-UPGRADE.md`·`PLAYBOOK.md`·과정 요약·`upgrade-contracts.md`(Ch 21 06 줄·Ch 18 06 줄·§5 — 오케스트레이터 몫, §17) · 공용 도구 코드(`nbkit.py`·`mdpatch.py`·`run_section.sh`·게이트·`verify.py`·`visual.cjs`·`execute.py`·`render_mermaid.py`·`attach_figures.py`·`count_code.py`) · Part 6 옛 검사 스크립트와 `check_*`·`collect_public_files.py` · `textbook/qa/check_course_continuity.py` · Part 6 `_src/index.html`·`practice-start.md` · `textbook/part6/qa/final-artifact-hashes.json`·`notebook-executions.json`·`ch21-ch29-technical-review.md`·`ch29-before-technical-repair/`(옛 기록) · 실습 폴더 `pyproject.toml`·`uv.lock` · 도구 파일(해시 고정) · 삽화 · Ch 21 06 노트북·계약 파일 · Ch 21 요약 §9의 「cell 12~18」·`assert` 셋(기록 — §18) · **Ch 30 이후 파일 전부**(Part 6 목차·묶음·공개 목록·기록·`continuity-guide.md` Ch 29 줄 말고 — Ch 30 03·09·Ch 33 02·04는 읽기만) · `llm-practice.zip`·`delivery-results.json` · claude.ai 프로젝트 문서.
- **파일을 지운 것은 없습니다.** 옮긴 것은 옛 생성기 둘(`mv -n`, 해시 같음). 옮긴 뒤 `verify.py --chapter`(PASS 5/127, 계약 파일 해시 같음)·게이트(`gates-after.json` 바이트 같음)·`_build_index.py`·묶음 실행 검사·`visual.cjs` 통과(`_build.py`는 옮기기 전에 돌렸고 옛 생성기를 부르지 않음). 마감이 만든 것: 사용자 디스크 `.cache/ch29-close/`(마감 전 사본 `pre/` 19MB·확인 스크립트 `tools/`·치환 목록 `reps/`·전달 검사 사본 `dx/`·로그 `log/`) · 기기 `/tmp/ch29-close/`(02·04 시험 실행 `02try`·`04try`·사본 `02B`·`04B`·묶음 일부 풀기 `zip/`·`.moai` 막기 확인 `moai/`·화면 검사 사본 `vis/`·문서 초안 `docs/`·게이트 임시 `pregate/`, 약 3.4MB).
- **보호 파일 217개(`before-manifest.json`)**: `manifest-changes.md` 「마감 뒤」 — **같음 177 · 바뀜 38 · 옮김 2**(바뀜 38 가운데 36은 마감에서 바뀐 것 — 파일별 목록 값 → 마감 전 → 마감 뒤 해시는 그 파일 표, 나머지 둘(Ch 29 `qa/public-files.json`·Part 6 `public-files.json`)은 05절 작업 값 그대로 — 마감에서 바꾸지 않음).

## 14. 기준 버전·확인 날짜

- 실습 폴더 잠금(`pyproject.toml` 직접 의존 `agentevals==0.0.9`·`langchain==1.4.0`·`langchain-openai==1.6.0`·`langgraph==1.2.11`·`python-dotenv==1.2.3`·`pillow>=11.0`(import 0 — 강사 확인), dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`): `openevals 0.2.0`·`langchain-core 1.6.2`·`langsmith 0.12.4`·`openai 3.11.0`·`pydantic 2.13.5`. 노트북 `%pip`: 01·02 둘 · 03·05 넷 · 04 하나(`langchain`).
- 교재 출력: Linux aarch64 · Python **3.12.13** · 환경 `.cache/vm/venv-ch29-agent-evaluation`(잠금 판). 실행일 2026-09-29(01 01:18 · 02 **04:43(마감 재실행)** · 03 02:26 · 04 **04:46(마감 재실행)** · 05 03:40 UTC). 모델 `gpt-5.4-mini`.
- 설치판 소스 행(검토 A·B와 마감이 다시 확인): agentevals 0.0.9 `trajectory/match.py` 24~109·72~88·80~83·85~88 · `strict.py` 20~76·34·**53~75(한 응답 안 요청은 `seen`으로 차례 없이 짝지음 — 마감 A-5)** · `unordered.py` 33~37 · `subset.py` 28~30 · `superset.py` 33~35 · `utils.py` 78~87·90~134·137~171·194~212 · `trajectory/llm.py` 27~49·77~95·98~173 · openevals 0.2.0 `llm.py` 70~117·**102~110(칸 reasoning 설명 — 마감 B-2)**·218~220·251~254·256~272 · `utils.py` 203·427~454 · langchain 1.4.0 `agents/factory.py` 1451~1452 · `agents/middleware/model_call_limit.py` 37~60·168~208·236~251 · langchain-openai 1.6.0 `chat_models/base.py` 3723.
- 참고 자료(2026-09-29 확인 — 절 작업·검토 WebFetch): LangSmith Evaluation approaches · LangChain Agent evals · LangSmith Trajectory evals · agentevals GitHub·PyPI(0.0.9, 2025-07-24) · openevals GitHub · LangSmith Dashboards · Wikipedia Percentile · Python `math.ceil`.

## 15. 강사 확인 대상

1. **제목 말**: 챕터 「Agent 평가 — 답과 실행 경로를 함께 보기」(「경로」 — 제목에만) · 02 「매칭」 · 03 「LLM judge」 · 04 「Ch18 궤적」(Ch 18 기록에는 도구 차례가 없음 — b2에서 밝힘) · **05 긴 제목**·슬러그. 슬러그 01·04는 Ch 28 06 b8·Ch 21 06 b2가 링크해 고정.
2. **「궤적」 정의를 넓힌 것**(검토 A-1 — 챕터 리드 결정): 「질문에서 최종 답까지 밟은 단계의 차례(메시지 목록 전체)」 + 이름 목록은 「도구 차례」. 01·02 문장·01 비유·handoff 용어 표를 고침.
3. **`chapter.json` 학습 목표 둘 → 다섯**(01 세 평가 · 02 네 모드와 인자 비교 방식 · 03 실제 에이전트 궤적을 모드와 평가 모델로 · 04 기록 두 개를 공통 칸으로 · 05 실습 — 「평가셋」·「명시」 뺌, `hours` 그대로 8h·강의 3h·실습 5h = 01~04 meta 합). `_build_index.py`·`build_index.py`·`continuity-guide.md` Ch 29 문구 · README 다시 쓴 범위.
4. **코드 양**(규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」): 코드 줄 156 → 737(01 120·02 168·03 155·04 151·05 143) + 도구 파일 · 코드 셀 24 → 127 · **02 마감 재실행으로 코드 줄 147 → 168**(A-7 — 딕셔너리 키마다 한 줄·평가 함수 여러 줄, 셀 47은 딕셔너리 `copy()`로 12줄).
5. **03 판단**: 평가 모델 점수 5/5·두 커널 같음을 결론에 둔 것 · 에이전트와 평가 모델이 같은 모델 객체(자기 판정) · `_format_inputs` 사용 · 평가 모델 요청 2를 손으로 더한 것 · 교재용 도구와 시스템 메시지 글에 도구 차례를 적은 설계 · 호출 한도 4·실행 한도 20.
6. **04 판단**: 「세는 값」 분류를 「세는 값도 한 번 실행한 값」으로 고친 것(B-5 — 비유·04-3 칸 제목 포함) · Ch 18 도구 요청 수 `None` · 한 칸 「점수」에 코드 검사와 평가 모델 판정 · `executed_at` 출력을 뺀 것(B-6 (나)).
7. **05 설계**: 평가 모델·최종 답 평가를 뺌 · 점수 칸에 모드 `strict`(검색어 뺌) 판정 · 결론을 「도구를 모두 부른 뒤 한도에 닿은 실행」으로 한정 · 새 함수 넷을 노트북에 · 셀 [22] 출처 줄(코드 고침은 다음 재실행 — B-11) · 실행 2가 Ch 26 05와 같은 모양(B-9 — 선례를 밝힘).
8. **「도구별 덮어쓰기」 말**(A-9): Ch 13 「덮어쓰기」와 가르는 한 문장만 넣음 — 말을 바꿀지.
9. **삽화 다섯**: 01-5 두 띠의 구멍 수·길이·기울기(**A-2 — 재생성하지 않고 그림 읽기에 「두 띠가 같은 궤적인지도 나타내지 않습니다」**, 01은 재생성 여유 1회) · 02-5 띠 오른쪽 빈 부분 · 03-5 두 띠 구멍이 겹치지 않고 나란히 · 04-5 빈 고리·다섯째 띠 길이(비유 글을 그림에 맞춤 — B-7) · 05-4 카드·구멍 · **작업 조회 결과의 모델 표시 `nano_banana_2`와 요청 `nano_banana_pro`가 다름**(기록만).
10. **그림에서 바꾼 값 색 파랑**(05 과제 지시의 초록 대신 챕터 규칙 — Ch 28 B-10과 같은 쪽).
11. **도구 파일 이름 `eval_tools.py`**(내장 `eval`과 글자가 닮음 — 모듈 이름이라 가리지 않음).
12. **`.moai` 보조 스크립트 둘 막음**(A-13): 옮길지·지울지는 사용자·강사(Ch 25~28도 대상).
13. **실습 폴더 `pyproject.toml` `pillow>=11.0`**(import 0 — Ch 21 B-16처럼, 잠금 재생성이 들어 그대로).
14. 한국어 감사 3단·그림 판독 2차(별도 세션 — 두 검토의 「확인하지 못한 것」: 삽화·Mermaid PNG 눈 판독, 요금표 값 공급사 문서 재확인, Windows·macOS 실제 실행, 학생 `uv sync --locked` `.venv` 첫 셀).

## 16. Ch 30이 이어받을 것과 전제하면 안 되는 것

### 이어받을 것

- 05 b8 「Part 7 Ch 30 01절에서는 웹 서비스가 받을 요청과 내놓을 응답의 모양을 정합니다」(Ch 30 01 b2·b3와 맞음 — 앞당겨 가르치지 않음).
- 말: 요청 수 셈(「요청 수 = 도구를 요청한 응답 수 + 1」 — 답까지 간 실행에서만) · 호출 한도(Ch 22 04 — invoke 한 번마다) · 운영 지표·공통 칸(Ch 29 04 — Ch 33 04가 이어 씀).

### 전제하면 안 되는 것 (Ch 30 파일은 고치지 않았습니다)

1. **Ch 29에는 평가셋이 없습니다.** 01~03·05는 질문 **하나**(「일반 도서는 며칠 동안 빌릴 수 있나요?」)와 기준 궤적 **하나**(`search_documents` → `check_source`)만 쓰고, 04는 Ch 21 06의 세 질문(`C01`·`C05`·`C07`) 기록과 Ch 18 06 저장 출력을 읽기만 합니다. **Ch 30 03 「실제 모델 품질은 Ch29 평가셋으로 확인합니다」·09 「Ch29 평가셋으로 도구 선택과 최종 답을 반복 평가하고」는 지금 판과 맞지 않습니다**(평가셋·반복 평가·평가 결과 파일 없음 — Ch 30 몫).
2. **Ch 29는 뒤 챕터가 읽는 산출 파일을 만들지 않았습니다**(노트북 파일 쓰기 0). Ch 29 파일을 Ch 30이 읽는다고 전제하지 말 것(파일 계약 없음). Ch 21 06·Ch 18 06 두 파일(`25cfe5df…`·`5ba7f5a0…`)은 그대로입니다.
3. **도구 파일 `eval_tools.py`(05판 `d624b8f3…`)는 Ch 29 실습 폴더에만** 있습니다(`langchain.messages`·`math`를 가져옴). Ch 30 실습 폴더와 잠금이 다르면 파일째 가져오지 말 것.
4. **에이전트는 `create_agent` + 교재용 도구 둘 + 호출 한도 + 실행 한도 20**, 모델은 `gpt-5.4-mini`(temperature 0, `reasoning_effort="none"`)만 썼습니다. 웹 서버·HTTP·비동기 실행(`ainvoke`)·스트리밍·체크포인터는 Ch 29에서 쓰지 않았습니다.
5. **평가 모델(judge)은 03에서만** 두 번 불렀고(같은 모델 객체 — 자기 판정), 05는 부르지 않았습니다. 평가 모델 점수는 「노트북 밖 다섯 번과 두 커널 같음」 한정어로만 결론에 썼습니다.
6. **요청 수 셈은 답까지 간 실행에서만 맞습니다.** 도구를 모두 부른 뒤 호출 한도에 닿은 실행(05 실행 2)은 요청 수 = 도구를 요청한 응답 수였고, 한도가 끼운 끝 메시지는 사용량 `None`이라 `sum_usage`에 그대로 넘기면 `TypeError`(도구 파일 88~96행 — 05는 `model_part`로 뺌).
7. **말**: 「궤적」(질문에서 최종 답까지의 메시지 목록 전체)·「도구 차례」·「기준 궤적」·「궤적 맞춰 보기」·모드 넷·「평가 모델(judge)」·「평가받는 에이전트」·「운영 지표」·「공통 칸」은 Ch 29 말입니다. 「매칭」·「LLM judge」·「실행 경로」는 제목에만. 「결정적」·「지연」·「측정」·「반환」·「프롬프트」는 본문 0.
8. 05 소재(호출 한도 4 → 2·공통 칸 두 줄)를 Ch 30이 이어 쓴다는 약속은 없습니다.

## 17. 뒤 챕터 인계 (그 챕터 파일은 고치지 않음)

| 챕터 | 자리 | 지금 글 | Ch 29 쪽 사실 | 할 일 |
|---|---|---|---|---|
| Ch 30(Part 7, 대기) | 03 `_src` 「실제 모델 품질은 Ch29 평가셋으로 확인합니다」 · 09 「Ch29 평가셋으로 도구 선택과 최종 답을 반복 평가하고」 · `_src/_generate.py` 같은 문장 | 「평가셋」·「반복 평가」 | Ch 29는 평가셋·반복 평가·평가 결과 파일이 없음(§16-1) | Ch 30 개선 때 「Ch 29의 궤적 맞춰 보기·평가 모델 판정으로 …」처럼 실제로 가르친 것으로 고칠 것 |
| Ch 30 | 01 b2·b3 | 요청·응답 모양 | 05 b8이 「요청과 응답의 모양을 정합니다」로만 이음 | 없음(참) |
| Ch 33(Part 7, 대기) | 02 「Ch29의 궤적 기준」·「Ch29의 궤적 효율」 | 「궤적 효율」(금지어 「효율」, 느슨함) | Ch 29는 참·거짓 판정과 요청 수 셈만 함(점수화한 효율 없음) | Ch 33 개선 때 「궤적 맞춰 보기 판정·요청 수」로 |
| Ch 33 | 04 「Ch29에서 운영 지표를 정의」 | 참 | 04 용어 「운영 지표」·「공통 칸」 | 없음 |
| Ch 33 | `data/regression-baseline.json` 출처 기록의 Ch 29 04 옛 해시 | 옛 해시 | 04 노트북 새 해시(`4ed26b54…`) | Ch 33 개선 때 출처 기록 확인 |
| Ch 21(완료) | 요약 §9 「Ch 29 04 노트북 cell 12~18」·「`assert` 셋(p95 포함)」 | 옛 번호·옛 `assert` | 새 04는 `assert` 둘(줄 수·도구 요청 수 — p95 `assert`는 뺌), 코드 셀 13·15 | 기록이라 고치지 않음(b10 교재 문장은 마감에서 고침) — Part 6 마감 누적 문서 |
| 과정 문서(오케스트레이터) | `upgrade-contracts.md` Ch 21 06 줄(없음)·Ch 18 06 줄(98행)·104행 「10행 복습 해설 2.094 → 2.003」·§5 | 옛 값 | 04가 새 값으로 고침·공통 칸·Ch 18 도구 요청 수 `None`·04 복습 3은 자리 문제로 바뀜 · 새 zip `6d746be1…`·`bundle-execution.json` `f858a5ca…`(Ch 24 01·Ch 28 01 값 그대로) | Part 6 마감 누적 문서 |
| 과정 요약 | §5 Ch 29 용어 · §7 실습 절 선례 | 없음 | §4 용어(넓힌 「궤적」·「도구 차례」 포함) · 05 「한도에 닿은 실행을 궤적 맞춰 보기와 운영 지표로 견줌」 | Part 6 마감 누적 문서 |
| 전체 마감 | `llm-practice.zip` 안 Ch 29 | 옛 판 | `part6-practice.zip`은 새 판 아홉 항목이 디스크와 같음 | 전체 묶음 재생성 때 대조 |

## 18. 남은 것 (전체 마감 몫 — `textbook/qa/upgrade-final-checklist.md` §2-17)

1. **옛 그림 열둘 삭제 승인**: `figures/0N-흐름.{svg,excalidraw,caption.md}`(N=1~4 — 세어 12개, 본문 참조 0, 공개 목록에 줄 없음, 사본 `qa/upgrade/before/figures/`, 03 캡션에 옛 금지어 「반환」·「루브릭」·「LLM judge」). Part 6 옛 검사 `check_figures.py`가 `.excalidraw` 짝을 요구하는 것과 함께 정할 것.
2. **`gates-wip-*.json` 열하나 삭제 승인**(`gates-wip-01-01`~`05-05`·`01`~`05`·`ch29-after05` — `gates-after.json` 5/5로 갈음, 절 번호 다섯은 마감 `run_section.sh`가 다시 씀).
3. **캐시·임시 삭제 승인**: 실습 폴더 `notebooks/__pycache__/`는 **없음**(모든 실행 `PYTHONDONTWRITEBYTECODE=1`) · 실습 폴더 `labs/part6/ch29-agent-evaluation/.venv`(macOS 판 187MB) · `.cache/vm/venv-ch29-agent-evaluation`(265MB) · `.cache/ch29-01-view`~`ch29-05-view`(약 3.4MB) · `.cache/ch29-close/`(약 19MB) · 기기 `/tmp/ch29-prep`·`/tmp/ch29-01`~`/tmp/ch29-05`(약 41MB)·`/tmp/ch29-close`(약 3.5MB) · `/tmp/reviewA29`·`/tmp/reviewB29`(검토 재현 파일) · 공용 `/tmp/mmd`·`/tmp/pptr-cache`·`/tmp/libs`·`/tmp/uv-cache`·`/tmp/pw`·`/tmp/pw-browsers`·`/tmp/npm-cache-ch26close`(Ch 26 마감이 설치, 그대로 씀).
4. **코드 쪽 다음 재실행 몫**: **01 셀 37** `trajectories = {…}` 한 줄 116칸(A-7 — 01은 이번에 다시 실행하지 않음, 01은 모델 0·결정적이라 재실행 비용 작음) · **05 셀 [22]** 출처 `print` 줄(B-11 — 05 재실행은 요청 10) · 02 셀 45 `print` 한 줄 105칸(딕셔너리·목록 아님 — 선택).
5. **도구 파일 머리 설명**: §2-13 6번 Ch 24~27 한 항목에 Ch 29 줄 덧붙임(§11).
6. **Part 6 묶음 실행 검사 후보**: Ch 29 01·02·04(모델·키 없이 결정적 — 04는 묶음에서 PASS 25셀 확인). 넣으면 `check_bundle_execution.py` 목록과 계약(모델·키 셀 금지)이 생김 — 마감은 검사 스크립트를 고치지 않음.
7. **`.moai` 보조 스크립트 둘**: 막음(§13). 옮길지·지울지 사용자·강사.
8. **Part 6 옛 검사 스크립트(고치지 않음)**: `check_scope.py` `SECTION_COUNTS` ch29 **4 ≠ 5**(Ch 21 07에서 먼저 멈춤) · `check_figures.py`·`check_notebook_readiness.py`(47 ≠ 56 — 결과 파일 되돌림)·`check_visual_reports.py`(**Ch 21 HTML 수정 시각이 바뀌어 Ch 21 01에서 멈춤** — Ch 21 `visual.cjs`를 다시 돌리면 풀림, `/tmp` 사본 실행 16행 PASS) · `textbook/qa/check_course_continuity.py`(`llm-practice.zip` Stale) — §12.
9. **`llm-practice.zip`**: §12 · 안 Ch 29는 옛 판(§17).
10. **기록 파일의 옛 해시(계약·검사 입력 아님 — 고치지 않음)**: `textbook/part6/qa/final-artifact-hashes.json`(Ch 29 줄, 옛 생성기 옛 자리 포함) · `notebook-executions.json`·`notebook-readiness.json`(Ch 29 넷 — 05 없음) · `ch21-ch29-technical-review.md`·`ch29-before-technical-repair/` · Part 6 공용 `visual-results.json`의 `index.html` 두 줄(Part 6·전체 목차 — 옛 해시) · `textbook/_notebook/build_index.py` 절 수(Ch 29 4 — 실습 절 뺀 수).
11. **과정 요약·계약(누적 문서 몫)**: §17 과정 문서 줄 · 도구 파일 `eval_tools.py`(`d624b8f3…`, 함수 열하나)는 과정 요약에 아직 넣지 않음(Part 6 마감 오케스트레이터).
12. **옛 기록 파일**: `qa/research.md`·`qa/technical-notes.md`·`qa/verification.md`·`집필점검표.md` 머리에 「개선 전 판」 표시(내용 그대로 — 뒤 둘은 끝 「마감」 절) · `qa/upgrade/review-pack/`(검토에 쓴 마감 전 묶음 — 다시 만들지 않음) · `figures/0N-…prompt.md`(생성 기록).
13. **2차 검토**: 두 검토의 「확인하지 못한 것」과 §15-14.

## 19. 검토 1차와 반영 (2026-09-29 마감)

- 판정: **A(01~02·공통) 중 6 · 하 10**, **B(03~05·마감 몫) 중 3 · 하 13**. 합 **[중] 9 · [하] 23**, [상] 0.
- **[중] 9건 모두 반영**:
  - **A-1** 「궤적」 정의 넓힘(01 b4·용어 표·비유·노트북 [0]·[6]·[18], 02 노트북 [6]·그림 읽기, handoff 용어 표) — 챕터 리드 결정.
  - **A-3** 목록 `copy()` 출처 → Ch 2 03절(02 b3·노트북 [38]·생성기 설명, 03 b3·노트북 [51]).
  - **A-10** 다섯 노트북 커널 폴더 문장 → Part 6 두 문장(01·03·05 마크다운만, 02·04는 재실행과 함께).
  - **A-11·B-13** 실습 폴더 README 전체 다시 씀(§13).
  - **A-12·B-13** `chapter.json` `objectives` 둘 → 다섯(§15-3), zip을 마지막에 한 번 다시 만들고 묶음 실행 검사 PASS(`bundle-execution.json`이 새 zip 기준 — §12).
  - **A-13** `.moai` 보조 스크립트 둘 막음(§13).
  - **B-5** 04 「세는 값」 분류(§7) — b1·b4 비유와 소제목 단락·b6·표·확인할 점·b7·b8·복습 2·노트북 [38]·[40]·정리·04-3 칸 제목·캡션(04 재실행과 함께).
  - **B-8** 03·05 b7의 노트북 밖 가짜 모델 근거 세 문장 → 코드 사실(`sum_usage` 88~96행)·02 네 모드 뜻으로 셈한 예상·「이번에 세지/실행하지 않았습니다」. 「모델 대신 정해 둔 응답」 교재 0건.
- **[하] 23건 처리**(고침 19 · 일부 반영 1 · 전체 마감 항목으로 넘김 2 · 기록 1): A-2(그림 읽기 한 문장 — 재생성 0, 강사 확인) · A-4(02 한정·b7 까닭) · A-5(01·02 정의·02 b7 새 항목) · A-6(02 [56]) · **A-7(02 여섯 셀 고침·재실행 — 01 셀 37은 미반영)** · A-8(설계표) · A-9(용어 표 한 문장 + 강사 확인) · **A-14·B-15(도구 파일 머리 설명 — 내용은 그대로, 전체 마감 항목에 덧붙임)** · A-15(Ch 21 06 b10 고침, Ch 30·33은 §17 인계) · **A-16(묶음 실행 검사 후보 — 스크립트를 고치지 않아 최종 점검표 기록)** · B-1(캡션 한정어·도식 읽기) · B-2(03-2 캡션·도식 읽기·노트북 [27]·[29]) · B-3(노트북 [59]·handoff) · B-4(03 b3·[51]·원어 괄호) · B-6 (나)(04 `executed_at` 출력 뺌 — 재실행) · B-7(04 비유 글) · B-9(05 b2·b3·b6) · B-10(05 b2·[29]) · B-11(설명만 — 코드는 다음 재실행) · B-12(05 b7 한 문장) · B-14(Ch 21 06 b10 고침 — Ch 21 요약 §9·계약 104행은 기록이라 §17) · B-16(handoff §6 첫 항목).
- **미반영과 까닭**: ① **A-7의 01 셀 37** — §1이 01을 다시 실행하지 않기로 정해 코드 셀을 바꾸지 않음(다음 재실행 몫) ② **A-14·B-15 도구 파일 머리 설명** — 챕터 리드 결정(도구 파일 해시 고정 `d624b8f3…`, 바꾸면 01~05 생성기 대조 사슬·zip·공개 목록 해시가 함께 바뀜) → Ch 24~28과 함께 전체 마감 한 항목 ③ **A-16 묶음 실행 검사 목록에 Ch 29 더하기** — 검사 스크립트 수정 금지, 후보로만 기록 ④ **B-11 셀 [22] 코드** — 05를 다시 실행하지 않음(요청 10), 권고대로 설명만 ⑤ **A-2 삽화 재생성** — 마감은 Higgsfield 0, 글로 막고 강사 확인 ⑥ Ch 30 03·09·Ch 33 02 문장 — 그 챕터 파일을 고치지 않음(§17).
- **노트북 해시 전후**(`code_sha256` / `outputs_sha256`, 앞 12자): 01 `b7a67c68540b`/`8a4db6c2b86e` 같음 · **02 `8e80cc8d5a27`/`ecc6f928477e` → `238911432b50`/`274931b425d1`**(A 04:43:56Z · B 04:44:07Z, 27/27 같음 — 출력 글을 이어 붙이면 옛 판과 같고, 설치 셀의 출력이 나뉜 모양만 달라 `outputs_sha256`이 바뀜) · 03 `c38454ecf35a`/`329537cf048c` 같음 · **04 `43163e6ac114`/`cccaacaa28da` → `4ed26b54f6ff`/`492d4e24d7f3`**(A 04:46:54Z · B 04:47:06Z, 25/25 같음) · 05 `7dba1d37a0bd`/`2793f969c4ac` 같음. 01·03·05 `executed_at` 같음, 다섯 모두 `metadata.verification`과 다시 계산한 값이 같음. **Ch 21 06 노트북 `ca14949bb0f9`/`1ded374d9f64` 같음(파일 해시도 같음).**
- 고친 방법: `.cache/ch29-close/tools/gapply29.py`(생성기 문자열 치환 — 치환 수가 다르면 멈춤, 바뀐 생성기를 실행해 **코드 셀이 노트북과 한 글자라도 다르면 멈추고**(02·04는 `--gen-only`), 달라진 마크다운 셀만 노트북에 옮긴 뒤(첨부·메타데이터 그대로) `src_html()`로 `_src`) · `pregate29.py`(쓰기 전 G1~G6를 `/tmp` 임시 노트북으로) → 01·03·05 `run_section.sh … NN --no-exec` · 02·04는 `author_NN.py --try`·`--tools-copy` 시험 실행 → `run_section.sh … NN`(A) → 사본 B → `cmpout.py` 셀별 대조 · `.mmd` 하나(04-3) `render_mermaid.py`(바뀐 것만) · `capsync29.py`(캡션 파일 = 생성기 `FIGn_CAP`, 03-2·03-3·03-4·04-3 맞춤) · `chain29.py`(생성기 대조 사슬).
- 검사: `upgrade_gates.py … --label after` **5/5 PASS, G1~G7 0** · AST 따로 금지 문법 0(다섯 노트북·도구 파일) · 호출 깊이 최대 2 · `verify.py --chapter` **PASS 5 sections / 127 code cells (max 14 lines)**(Ch 21도 PASS 7/180) · 빌드 HTML 여섯(과 Ch 21 06) `{{`·`[[` **0건** · `visual.cjs` **12행 PASS**(+ Ch 21 06 두 줄) · Part 6 `check_bundle_execution.py` **PASS** · Part 6 `check_delivery.py`는 `llm-practice.zip` Part 1 Stale에서 멈춤(그 zip을 뺀 대조 통과) · 옛 검사 넷·과정 연속성 검사는 Ch 29 전에 멈춤(§12) · 금지어 전후 대조(`ban29.py`) 새 걸림 0(거짓 양성만) · 보호 파일 217개 — `manifest-changes.md` 「마감 뒤」.

## 20. 절차 메모

- 마감은 기기 셸 한 곳에서만 작업(`mcp__remote-devices__device_bash`), 셸 호출마다 `timeout` 170 안팎. 모델 요청 0 · 삽화 생성 0 · 파일 삭제 0(기기 `/tmp/ch29-close/02try`를 만들기 전에 없는 폴더에 `rm -rf` 한 번을 부른 일이 있으나, 폴더가 없어 지워진 것은 없음 — 그 뒤로 `rm`을 쓰지 않음) · 모든 파이썬 호출 `PYTHONDONTWRITEBYTECODE=1`(실습 폴더·`qa/` pyc 새로 0). 키 값은 출력하지 않음(`.env`를 열지 않음, 02·04·묶음 검사는 키 환경 변수를 지우고).
- 날짜: 마감 검사는 모두 2026-09-29 UTC 안에 끝남 — `nbkit.RUN_DATE` = 실행일이라 03·05 키 셀 결과 읽기의 실행일 문장과 생성기가 그대로 같음.
- `grep -r`을 프로젝트 맨 위 전체에 걸면 `.cache/vm` 때문에 셸 시간 제한(120초)에 걸림 — 폴더를 좁혀 부름.
