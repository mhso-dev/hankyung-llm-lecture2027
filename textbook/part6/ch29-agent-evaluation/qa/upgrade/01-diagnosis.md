# 01절 진단과 개선 기록 — 에이전트 평가 세 전략 (experiment)

- 작업일 2026-09-29 · 작업자: 01절 담당(모델 요청 **0**) · 생성기 `qa/upgrade/author_01.py`(`306b1316…`) · 슬러그 그대로(Ch 28 06 b8 링크).
- 읽은 것: 준비 노트(`chapter-lead-notes.md` 전부) · `AGENT-BRIEF.md`·`PLAYBOOK.md` · 규격 전부 · 과정 요약(§0~§9) · 계약(목차·Ch 18 06·Ch 21 06 → Ch 29 04 줄·Ch 28 줄·§4 도구 파일·§5 묶음 Ch 21~28 줄) · Ch 28 `chapter-summary.md`(전부)·`handoff.md`(챕터 공통·§01 → §02) · 본 생성기 Ch 28 `author_01.py`(전부)·Ch 27 `author_02.py`(머리·도구 파일 판·대조 함수·쓰기 가드). `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.

## 1. 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전(`gates-before.json`) | 5 | 61 | 3 | 2 | 0(실제로는 틀 문장) | 0 | 6 | 13 | 3 | **27** |
| 첫 실행 전(`gates-wip-01-01.json`) | 23 | — | 0 | 0 | 0 | 0 | 0 | 0 | 17(그림 전) | — |
| 후(`gates-wip-01.json`, `--no-exec`) | **23** | **358** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전에 기기 사본(`/tmp/ch29-01/try/`)으로 게이트 함수를 먼저 돌려(`/tmp/ch29-01/tools/pregate.py`) G6 긴 문장 둘(b3 Ch 19 04 문장 77자·b7 결과 딕셔너리 문장 72자)과 금지어 하나(b2 「돌려 만든」)를 고친 뒤, 실습 폴더에 쓰고 `upgrade_gates.py … --label wip-01 --section 01`(G1~G6 0)을 거쳐 실행했습니다. 삽화 뒤 「그림 읽기」 첫 문장이 70자를 넘어 한 번 줄였습니다.
- 코드 줄(`count_code.py`, 주석·빈 줄 뺌) **28 → 120**(도구 파일 36줄 따로). 옛 판은 셀 다섯에 내포식·`getattr`·`*args`를 몰아 적었고, 새 판은 셀 23개로 나눔(규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」 — 강사 확인 대상).
- AST 따로(`/tmp/ch29-01/tools/extra_check.py`): 노트북·도구 파일 금지 문법 0건(f-string·내포식·제너레이터 식·`lambda`·조건 표현식·별표 풀기·`+=`·`while`·`try`·클래스·데코레이터·힌트·기본값 매개변수·대입 풀기·`for` 풀기·`enumerate`·`getattr`·`sum`·`max`·`min`·`all`·`any`·`zip`·`next`·`isinstance`·`set`·`sorted`·`.get`·`.items`·`key=`·`reverse=`·`elif`·`await`), 호출 깊이 최대 **2**, 준비 셀 밖 셀 최대 **10줄**(`WASTEFUL`), 함수 본문 최대 **6줄**(`make_trajectory`·`called_tool_names`·`three_results`), 셀당 정의 하나. 쓴 내장 이름: `print`·`len`·`list`·`type`.
- 금지어(`/tmp/ch29-01/tools/ban29.py` — 준비 노트 `ban.py` 목록 + Ch 28 목록 + 과정 목록 + 「한 겹 더」 + 「결정적」·「알 수 있습니다」·「매칭」·「판정 모델」·영어 세 이름, `궤적`은 이 챕터 말이라 뺌): `_src` 본문·alt·캡션·노트북 마크다운·코드 주석·`.mmd` 라벨·캡션 파일·도구 파일 **0건**(참고 자료 제목 「LangSmith Trajectory evals」 거짓 양성 하나 말고).

## 2. 수정 전 주요 문제 (옛 판 — `qa/upgrade/before/`)

1. **b3 「Ch11 평가셋과 Ch21 에이전트를 사용합니다」 — 틀림**: 옛 01은 둘 다 쓰지 않았음(코드로 만든 궤적만). b3 둘째 문장 「필요한 자료와 객체는 노트북에서 다시 선언하므로…」는 네 절 같은 틀 문장.
2. **평가 셋 가운데 궤적 평가를 실제로 하지 않음**: 궤적은 도구 이름 목록을 뽑아 출력만(`[call["name"] for m in actual for call in getattr(m,"tool_calls",[])]`), 기준과 견준 판정 없음. 낭비 궤적은 「호출 2 ↔ 4」만 보이고 어느 평가가 그것을 잡는지 판정으로 보이지 않음. 최종 답은 `"14일" in …`(부분 글 포함) — b4 정의 「마지막 답을 채점」과 달리 같은 말이 든 틀린 답도 참이 되는 규칙.
3. **만든 대로 늘 참인 `assert`**: `"14일" in wasteful[-1].text and len(wasteful)>len(reference)`.
4. 코드: `trace(*tools: str) -> list`(`*args` 정의·힌트) · `enumerate(tools,1)`·`messages +=`·f-string `f"c{i}"` · 내포식 · `getattr` · `sum(… for …)` · 한 글자 변수 `m` · 인자 `{"topic":"대출"}`가 두 도구 모두 같음 · 도구 결과 「확인」 · 준비 셀의 별표 풀기 `[Path.cwd(), *Path.cwd().parents]`·`dotenv`(모델을 부르지 않는데 키 파일을 찾음, 주석 「공개하지 않은 API 키는 존재 여부만 확인하고…」는 틀 문장) · 설치 셀에 쓰지 않는 `langchain-openai`·`langgraph`·`python-dotenv`.
5. 문장: 영어 세 이름(Final Response·Single step·Trajectory)을 풀지 않음 · 「블랙박스」·「반환」 3·「측정」 3·「지연」·「보장」 2·「경로」(b4 「나쁜 경로」) · b5 확인할 점 = b6 첫 단락 = b8 둘째 항목(같은 글) · b8 「02-궤적-매칭-네-모드에서 이 결과를 다시 사용합니다」(틀 문장) · b10 참고 자료 둘(확인 2026-09-11)이 네 절 같음 · 복습 해설 한 줄.
6. 노트북 설명: 결과 읽기 0 · 준비물(요청 수·비용·시간) 없음 · 셀 첨부 그림 0 · 마크다운 「코드 읽기와 비교 경계」는 09-14 옛 보조 스크립트가 끼운 단락.

## 3. 바꾼 것 — 노트북 차례 (코드 셀 23, 마크다운 25)

| 절 | 셀 | 하는 일 |
|---|---|---|
| 준비 | 1 설치(setup) · 2 가져오기(setup) | `agentevals==0.0.9`·`langchain==1.4.0`만(이 절이 쓰는 패키지, 잠금 판). **키 셀·모델·`dotenv` 없음**. 가져오기 `create_trajectory_match_evaluator`·`AIMessage`·`HumanMessage`·`ToolMessage` + 도구 파일 `show_messages`·`tool_call_names`(고정 세 문장 + 실행 도구 가져오기 자리 한 문장) |
| 2 기준 궤적 | 3 글 정하기 · 4 `make_trajectory` 정의 · 5 기준 궤적 · 6 `show_messages`+최종 답 · 7 `called_tool_names` 정의 · 8 도구 차례 | 질문 「일반 도서는 며칠 동안 빌릴 수 있나요?」 · 기준 답 「일반 도서는 14일 동안 빌릴 수 있습니다.」 · 결과 글(Ch 14 LIB-001 글 + `[문서 ID]` — Ch 21 05 도구 메시지 모양) · 도구 요청 칸 넷(Ch 19 04·Ch 20 01 모양) · `기준 궤적의 메시지 수: 6` · `기준 궤적의 도구 차례: ['search_documents', 'check_source']`·`도구 요청 수: 2` · 음수 번호 `-1` 첫 풀이(Ch 16 03 음수 슬라이스) |
| 3 세 평가 함수 | 9 `final_answer_pass` · 10 `first_step_pass` · 11 `strict_match` 만들기 + 자기 자신과 견준 결과 딕셔너리 · 12 `trajectory_pass` · 13 `three_results` | 세 함수 모두 (실제 궤적, 기준 궤적)을 받음 · 최종 답 = 마지막 글 글자 비교(Ch 18 05 코드 검사처럼) · 한 단계 = 메시지 1번 자리의 도구 이름 목록 · 궤적 = 평가 함수의 칸 `score` · `평가 함수의 종류: function` · `{'key': 'trajectory_strict_match', 'score': True, 'comment': None, 'metadata': None}` |
| 4 견줄 궤적 넷 | 14 기준과 같음 · 15 검색 세 번 · 16 답만 틀림 · 17 차례 바꿈 | `도구 요청 수: 4 \| 메시지 수: 10` · `최종 답: 일반 도서는 7일 동안 빌릴 수 있습니다.` · `도구 차례: ['check_source', 'search_documents']` |
| 5 세 평가로 견주기 | 18 표(예상 → 실행) · 19 거짓을 낸 평가 · 20 첫 응답의 도구 요청 · 21 답만 틀림 뜯어보기 | 네 줄 표 · `['궤적']`·`['최종 답']`·`['한 단계', '궤적']` · 첫 응답은 차례 바꿈만 `['check_source']` · `메시지 수가 같은가: True`·`도구 차례가 같은가: True`·`최종 답이 같은가: False` |
| 6 값 바꿔 보기 | 22 답 글만 바꾼 궤적 · 23 나란히 견주기 | 바꾼 값 = 답만 틀린 궤적의 답 글 하나(「14일 동안 빌릴 수 있습니다.」, 도구 요청 그대로) · `두 줄이 같은가: True`(최종 답 평가는 뜻이 맞는 다른 글도 거짓) |
| 정리 | 세 줄 + 02절 | — |

- 노트북 첫 셀: 할 일 셋 · 준비물(모델 요청 0·API 키 없음·비용 0달러·읽는 파일은 도구 파일 하나·쓰는 파일 없음·걸린 시간 재지 않음) · 기준 버전(agentevals 0.0.9·langchain 1.4.0·Linux Python 3.12.13, 다른 판·Windows·macOS 실행 안 함) · 강의(2·3절)/실습(4~6절) 범위 · `uv sync --locked` → `notebooks/`에서 열기. 「오늘 볼 그림」에 01-1 첨부.
- `assert` **0개**(만든 대로 늘 참인 옛 `assert`를 뺌. 라이브러리 점수는 결정적이지만 01은 출력으로만 보임 — 02가 허용 여부를 판단, 인계 7번).

## 4. 챕터 리드 결정 적용

| 결정 | 적용 |
|---|---|
| 1 모델 M2(01 모델 없음) | 모델·키 셀·`dotenv` 0, 요청 0. 궤적은 손으로 만든 `AIMessage(tool_calls=…)`·`ToolMessage`(Ch 20 01 선례) |
| 2 01 설계 | 세 전략을 같은 기준 궤적과 견줌 · 설치판 사실 「모드가 답 글을 보지 않아 답만 틀린 궤적도 참」을 `strict` 하나로(네 모드 모두는 02 몫) · 낭비(검색 세 번) · 차례 바꿈 · 짝짓기 횟수·인자 비교·다른 세 모드는 쓰지 않음 · 만든 대로 늘 참인 `assert` 뺌 · b3 고침 |
| 3 04 계약 | 01은 계약 파일을 읽지 않음 — 인계 「챕터 공통」에 대조표를 옮김. **01·04 슬러그 그대로** |
| 4 용어 | 「궤적」 첫 자리 「에이전트가 도구를 부른 차례(궤적)」 + Ch 17 04 「단계 차례(궤적)」 이음 · 평가 모델은 Ch 15 말 「평가 모델(judge)」(과정 요약 §5 Ch 15 — **「판정 모델」은 과정 말이 아님**, 인계에 적음) · 「실행 경로」 본문 0 · 모드 이름은 `strict`만 첫 정의 · 「딕셔너리」·「내놓다」·「검사」·「재다」 · 「집합」·「루브릭」·「프롬프트」 본문 0 · b3·b10 새로 |
| 5 도구 파일 | **`eval_tools.py` 첫 판** — 이 노트북이 쓰는 앞 챕터 함수 둘만(§9) |
| 6 옛 생성기 | 공용·챕터 둘 막음(§10), `.moai` 둘은 기록만 |
| 7 슬러그 | 넷 모두 그대로, 제목 그대로 |
| 8 문법 범위 | §1 AST |
| 9 비유 | 「오르골 종이띠」를 엶(§12) |
| 10 준비 셀 | 설치(잠금 판·쓰는 패키지만)·가져오기, 키 셀 없음 |

## 5. 설치판·문서 확인 (2026-09-29, 모델 없음)

- 탐색 스크립트 `/tmp/ch29-01/exp/x1.py`(`env -u OPENAI_API_KEY`, 챕터 가상환경): 이 절 궤적과 같은 모양으로 세 평가를 돌려 표 네 줄 + 값 바꿔 보기 줄이 노트북 출력과 같음. 추가로 **질문 글만 다른 궤적·도구 결과 글만 다른 궤적·호출 ID만 다른 궤적·답 글이 빈 궤적도 `strict` 참**, 같은 판정 다섯 번 같음 — b7 「노트북 밖」으로만 적음(질문·결과 글·호출 ID 셋).
- 설치판 소스: agentevals 0.0.9 `trajectory/match.py` 24~109(만들기 함수, 26행 기본 `"strict"`, 81행 모드 이름 검사 `ValueError`) · `trajectory/strict.py` 20~76(34행 메시지 수 · 37행 역할 · 39~44행 도구 요청 유무 · 45~75행 이름·인자 짝 — 글 비교 줄 없음) · openevals 0.2.0 `utils.py` 203행 `@traceable`. 결과 딕셔너리 칸 넷(`key`·`score`·`comment`·`metadata`).
- 공식 문서(WebFetch 2026-09-29): LangSmith `evaluation-approaches`(세 방법 정의·입력/출력·장단점 — 최종 답은 「not evaluating anything that happens inside the agent, so it can be hard to debug」·「hard to define appropriate evaluation metrics」, 한 단계는 「relatively fast」·「only one particular step」) · LangChain `test/evals`(네 모드 — Strict 「message content can differ」, 결과 예시 칸 셋 `key`·`score`·`comment`) · LangSmith `trajectory-evals`(「allows for differences in message content」·「By default, only tool calls with the same arguments to the same tool are considered equal」) · PyPI agentevals(최신 0.0.9, 2025-07-24). **문서 예시(칸 셋)와 설치판 출력(칸 넷 — `metadata`)이 달라 출력 기준으로 적고 b7에 차이를 밝힘.**
- 환경 변수: 기기 셸에 LangSmith·LangChain 이름 없음, 루트 `.env` 키 이름은 `OPENAI_API_KEY` 하나(값 안 봄) — b7 「교재 출력을 만든 환경에는 LangSmith 설정 환경 변수가 없었습니다」의 근거.

## 6. 새 커널 두 번

- 시험 실행(기기 사본 `/tmp/ch29-01/try/`, 도구 파일 사본·`PYTHONPATH`) PASS 23셀 → 실습 폴더에 쓴 뒤 **A**(`run_section.sh`, 01:18:40Z, `code_sha256` `b7a67c68540b…`, `outputs_sha256` `8a4db6c2…`) → **B**(사본 `/tmp/ch29-01/B/`, 그림·삽화 전, `author_01.py --tools-copy`로 디스크 도구 파일 복사 — `cmp` 같음, 01:18:56Z) → 셀별 출력 글 **23/23 같음**(`/tmp/ch29-01/tools/cmpout.py`, 출력 글 연결 해시 `794d94020738a11a` 둘 같음, 시험 실행도 같음). `outputs_sha256`만 `8a4db6c2…` ↔ `dc1e6ec9…`로 다름 — 설치 셀 표준 출력이 A는 두 조각·B는 한 조각으로 나뉜 차이(글은 같음).
- A 첫 호출은 그림 파일이 없어 `attach_figures.py`에서 멈춤(`set -e`, 실행·저장은 끝난 뒤) → B → `.mmd`·캡션 → `run_section.sh … --no-exec`(렌더·첨부·빌드·verify·게이트). 그 뒤 코드는 바꾸지 않음(설명만 — `--src-only` 넷, 노트북 마크다운 한 셀(「오늘 볼 그림」 alt)을 `/tmp/ch29-01/tools/mdsync.py`로 옮김 — 코드 셀이 다르면 멈추는 스크립트, 코드·출력·`code_sha256` 그대로 확인).
- 모든 실행 `PYTHONDONTWRITEBYTECODE=1` — 실습 폴더 `notebooks/__pycache__` 생기지 않음(도구 파일 가져오기 pyc 0). `.failure.json` 0.
- **모델 요청 0**(노트북·탐색·B 모두), 예상 비용 0달러. 걸린 시간은 재지 않았습니다.

## 7. 용어 (새 용어 meta 5)

| 말 | 뜻(이 절) | 코드 | 비고 |
|---|---|---|---|
| 궤적(trajectory) — **이어 씀** | 에이전트가 도구를 부른 차례 · 이 절은 질문 → 최종 답 메시지 목록 | `called_tool_names(…)` | Ch 17 04 「단계 차례(궤적)」 이음(첫 자리에서 밝힘). 「궤적」은 Ch 28 금지어였으나 이 챕터 본문 말 |
| 기준 궤적(reference trajectory) | 좋은 에이전트라면 밟을 것이라고 사람이 미리 적어 둔 궤적 | `reference` | 「흐름을 보여 주려고 정한 예」 |
| 최종 답 평가(final response) | 안쪽은 보지 않고 마지막 답만 판정 | `final_answer_pass` | 이 절은 글자 비교(평가 모델은 03) |
| 한 단계 평가(single step) | 한 단계만 떼어 판정 | `first_step_pass` | 이 절은 첫 모델 응답의 도구 이름만 |
| 궤적 평가(trajectory) | 모든 단계를 판정 | `trajectory_pass` | — |
| 궤적 맞춰 보기(trajectory match) · 모드 `strict` | 실제 궤적을 기준 궤적과 코드 규칙으로 맞춰 봄 · `strict` = 메시지 수·역할·차례 + 도구 요청 이름·인자, 글은 안 봄 | `create_trajectory_match_evaluator(trajectory_match_mode="strict")` | 다른 세 모드는 02 첫 정의 |

- 이어 쓴 말: 평가 모델(judge)(Ch 15 01) · 코드 검사(Ch 18 05) · 도구 호출 요청·칸 넷(Ch 19 04) · 도구 메시지·호출 ID(Ch 19 05) · 딕셔너리 · 칸 · 참·거짓 값.
- 쓰지 않은 말: 「실행 경로」(제목에만) · 「judge」 단독(03 제목에만 — 본문은 「평가 모델(judge)」 한 번) · 「매칭」(02 제목에만 — 본문 「맞춰 보기」) · 「판정 모델」 · 영어 세 이름(괄호 원어 소문자 한 번씩만).

## 8. 옛 원고의 틀린 사실과 고친 방식

| 옛 글 | 사실 | 고친 방식 |
|---|---|---|
| b3 「Ch11 평가셋과 Ch21 에이전트를 사용합니다」 | 둘 다 쓰지 않음 | 실제로 잇는 것(Ch 17 04·Ch 19 04·06·Ch 20 01·Ch 15 01·Ch 18 05·Ch 21 05·06)으로 다시 씀. Ch 21 06은 「판정 여섯 모두 1 → 판정으로 두 흐름을 가를 수 없었다」를 동기로만 인용 |
| b4 「Trajectory는 … AIMessage와 ToolMessage 순서를 평가」·b6 「Trajectory 통과는 최종 문장의 사실 정확성을 보장하지 않습니다」(출력 근거 없음) | 설치판 `strict`는 글을 보지 않음 — 옛 판은 이를 실행하지 않았음 | 5절 출력(답만 틀림 → 궤적 `True`)과 소스 행으로 보임 |
| 최종 답 판정 `"14일" in …` | 부분 글 포함 규칙 — 틀린 답도 참이 될 수 있음 | 기준 답과 글자까지 같은지로 바꾸고, 뜻을 못 가르는 한계를 값 바꿔 보기로 보임 |
| 「낭비 궤적은 … 도구 호출이 2회에서 4회로」(판정 없음) | 어느 평가가 잡는지 보이지 않았음 | 표로 궤적 평가만 `False`임을 보임 |
| b7 「실제 모델 선택률이나 지연 시간을 보여 주지 않습니다」 | 뜻은 맞음, 금지어 「지연」 | 「실제 에이전트가 이런 궤적을 얼마나 자주 만드는지는 보여 주지 않습니다」·「걸린 시간은 재지 않았습니다」 |
| README 「01·02·04절은 저장된 실제 궤적과 결정적 평가」 | 01은 코드로 만든 궤적 | README는 고치지 않음(마감 몫 — 인계·§16) |

## 9. 도구 파일 `notebooks/eval_tools.py` — 첫 판

- 이름: 과정의 도구 파일 스물넷(`find labs -name '*_tools.py'`)·`eval_tools` 글자 검색과 겹치지 않음(2026-09-29 확인). 파이썬 내장 `eval`과 글자가 닮은 점은 머리 설명으로 뜻을 밝힘(「앞 챕터와 이 챕터에서 배운 평범한 함수」).
- 담은 함수 **둘**(이 노트북이 실제로 쓰는 앞 챕터 함수만): `tool_call_names(response)`(Ch 19 04) · `show_messages(messages)`(Ch 19 06, 안에서 `tool_call_names`를 부름). 설명 주석·본문을 **Ch 21 `runner_tools.py`(`f4113158…`)에서 글자 그대로** 옮김(주석 첫 줄만 「Ch 21 도구 파일 runner_tools.py의 같은 이름 함수를 옮겼습니다」). 가져오기 0 · 금지 문법 0 · 노트북 전역 이름 기대기 0.
- 해시 **`dab0888f0305d9c0fe5137a25666031b5a62b298034efebeeb13a757d85aafdf`**(36줄). 가져오는 절: 01(지금). 01 설치 셀에 더할 패키지 없음(가져오기 0).
- **생성기 대조 사슬(첫 판)**: `TOOLS_HEAD`(머리 설명 — 「이 챕터 앞 절 노트북에서 처음 적은 함수를 옮길 때는, 그 셀의 주석과 본문을 글자 그대로 옮깁니다」를 미리 둬 02가 머리를 바꾸지 않아도 되게) + `tools_text()`(원본 해시 고정 확인) + `strip_later_imports` + `check_tools()`(원본과 글자·AST 같음 + **Ch 27 `harness_tools.py`(`7a40d994…`)·Ch 28 `connect_tools.py`(`570ed3cc…`) 판과도 본문 같음**) + 쓰기 가드(없거나 이 판일 때만 쓰고, 뒤 절 판이면 `skip`) + `--tools-copy DIR`(B 사본용). 실행 결과 디스크 = `author_01.TOOLS`(확인).
- 01이 처음 가르친 함수 여섯(`make_trajectory`·`called_tool_names`·`final_answer_pass`·`first_step_pass`·`trajectory_pass`·`three_results`)은 **01 노트북에만**. 02·03이 다시 쓰면 그 절이 셀 글 그대로 도구 파일에 더함(인계 11번).
- 묶음 목록: 챕터 `qa/public-files.json`에 한 줄 + `collect_public_files.py`로 Part 목록 다시 모음(92 → 93, 선행 목록 바이트 같음). **zip은 다시 만들지 않음(마감)**.

## 10. 옛 생성기

- **공용 `textbook/part6/_author_ch21_ch29.py`**: `650f6506…` → **`391be055548853cce07c7f79cebc2c071751cbe37efb9e403c5df07ba53c5edf`**. 첫 줄 `from __future__ import annotations`와 Ch 21 설명 주석 셋 뒤에 설명 주석 셋 + `raise SystemExit("옛 Ch 21·Ch 29 원고·노트북·chapter.json 생성기입니다. …")`. Ch 21 건너뛰기 조건(551행 `if chapter == 21:`)은 그대로. 원본 사본(`before/generators/`)·작업 사본(`/tmp/ch29-01/gen/author_before.py`)과 `diff` — 더한 줄 넷뿐.
- **`figures/_gen_figures.py`**: `65b435f8…` → **`3577112dba8d97f8e1a65f7dd7219eaa6a3bf6fe70d4c9e43ad7ba470bcf8095`**(설명 주석 셋 + 독스트링 뒤 `raise SystemExit`).
- 확인: 두 파일을 기기 임시 폴더에서 실행 → 둘 다 막는 글을 찍고 종료 코드 1, Ch 29 `chapter.json`·`_src` 넷·노트북 넷·`figures/`·Ch 21 `_src` 목록의 해시 묶음이 실행 전후 같음, `__pycache__` 0.
- `$CH/qa/author_*.py`: 없음. **`.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part6b_enrich.py`(`8528cb33…`)·`part6b_review_fixes.py`(`a0299166…` — `ch29` 글자 넷)는 고치지 않고 실행하지 않음**(챕터 밖 옛 계획 폴더, 부르는 곳 0 — 지금 돌리면 개선한 Ch 25~29 `_src`·노트북 마크다운에 옛 단락을 끼움). 옮기기(`mv -n` → `before/generators/blocked/`)는 마감 몫.

## 11. 그림 (Mermaid 4)

- 설계표 `01-figures.md`를 **`.mmd`를 만들기 전·새 커널 A 전(01:18:15Z)**에 적음. 라벨 값은 시험 실행 출력 → A·B 출력과 다시 대조해 모두 맞음(바꾼 라벨 값 0). 렌더 뒤 줄 나눔만 고침(01-1 셋째 상자·01-2 도구 차례·01-3 넷 — 단어 가운데·가운뎃점 끊김) → 다시 렌더.
- 원본 viewBox 폭(868 이하): 01-1 **534** · 01-2 **563** · 01-3 **328** · 01-4 **305**. PNG 넷 직접 열어 확인(스테이징 사본): 01-1은 칸 위에 궤적 평가, 칸 오른쪽에 한 단계·최종 답 평가 — alt·도식 읽기를 그 자리로 고침.
- 색: 초록(궤적 메시지·입력 글·틀린 답 글) · 파랑(평가 함수·`make_trajectory`·`called_tool_names`·바꾼 답 글) · 노랑(출력 값) · 회색(네 줄 공통 기준·두 칸 공통 값) · **보라 0 · 빨강 0**. 갈래(보는 자리)는 점선, 나란한 조건은 `~~~`.
- 라벨 숫자 `6`·`2`·`14`(`7`은 한 자리)는 출력에 있음(G7). 라벨에 대괄호·따옴표 없음, subgraph 제목 `<br>` 없음, 노드 id `call`·`end` 없음.

## 12. 삽화 — 「오르골 종이띠」 계열을 엶

- `generate_image` 한 번(`nano_banana_pro`·16:9·2k·`use_unlim:false`·`count:1`) → **job `0defeb4c-9d52-4c66-ab90-98cc098bae03` 1차 채택, 재생성 0**. 작업 조회 모델 표시 `nano_banana_2`(요청 `nano_banana_pro`와 다름 — 기록만). 거래 **2026-09-29T01:21:13.439075Z 「Nano Banana Pro −2」** 한 줄이 이 절 몫(잔액 2305 → 2303, 바로 앞 거래 09-28T22:48:17Z는 다른 세션). **2크레딧**.
- 원본 `fd1a5fdb…`(2752 × 1536) → 폭 1100 `figures/01-5-오르골-종이띠.png`(`dcbd2609…`, 1100 × 614). 결과 URL을 다시 받아 같은 폭으로 줄인 그림과 픽셀 대조 bbox `None`·최대 차이 0. 저장 PNG와 같은 사본을 직접 열어 셈: 오르골 상자 **하나**(옆면 손잡이) · 상자에서 나온 구멍 띠 **하나** · 그 띠 첫 구멍·끝 위 돋보기 **둘** · 아래 떨어진 띠 **하나**. 글자·숫자·음표·사람·손·화살표 0. 구멍 수·띠 길이·아래 띠 기울기는 그림 읽기에서 짝짓지 않는다고 밝힘.
- 세부는 `figures/01-5-오르골-종이띠.prompt.md` 상태 줄.

## 13. 완료·대기 챕터 문장 (참·거짓)

- **Ch 28 06** 「Ch 29에서는 에이전트를 평가하는 방법을 배웁니다」 — 참 · 「Ch 29 01절은 평가 방법 세 가지를 견줍니다」 + 01 슬러그 링크 — **참**(슬러그 그대로, 01 b2가 세 방법 비교를 받음).
- **Ch 17 04** 「에이전트의 단계 차례를 맞춰 보며 평가하는 방법은 Ch 29 02절에서 다룹니다」(두 곳) — 지금 참(02가 네 모드로 다룰 예정, 01은 `strict` 하나만 쓰고 네 모드는 02로 넘김 — 01 b3가 이 예고를 되짚음). 02가 차례 맞추기를 다루는 한 참.
- **Ch 21 06** 「Ch 29 04절이 다시 읽습니다」(04 슬러그 링크)·「12~18번 셀」 등 — 01은 04를 건드리지 않아 그대로 참(셀 번호 문장은 04 몫 — 인계).
- Ch 18 06 「Ch 29 04절이 저장된 출력에서 읽습니다」 — 그대로 참(04 몫).
- Ch 33 02 「Ch29에서 최종 답뿐 아니라 도구 호출 궤적을 확인했습니다」 — 01이 궤적 평가를 보여 참에 가까워짐(Ch 33 파일 안 고침). Ch 30 03·09 「Ch29 평가셋」 — 01은 평가셋을 만들지 않음(느슨함 그대로, Ch 30 몫).

## 14. 챕터 밖 수정

- `textbook/part6/_author_ch21_ch29.py`(공용 옛 생성기 막기 — §10) · `textbook/part6/public-files.json`(도구 파일 한 줄 — §9) · `textbook/_notebook/checks/notebook-contracts-part6-ch29-agent-evaluation.json`(`verify.py`가 다시 씀). 실습 폴더 `notebooks/eval_tools.py`(새 파일)·01 노트북은 챕터 몫.
- 고치지 않은 것: 공용 도구(`nbkit.py`·`run_section.sh`·게이트·`verify.py`·`execute.py`·렌더·첨부) · 규격·PLAYBOOK·과정 요약 · Ch 17·18·21·28 원고 · 실습 폴더 README·잠금 · `part6-practice.zip` · `.moai` 보조 스크립트 · claude.ai 프로젝트 문서.

## 15. 보호 파일

- `before-manifest.json` 217개 대조: 바뀐 것 **10**(모두 예정 — `manifest-changes.md` 「01절 뒤」), 없어진 것 0, 나머지 207 같음. 계약 두 파일(`25cfe5df…`·`5ba7f5a0…`) 그대로.

## 16. 남은 것 · 지우지 않은 것 · 강사 확인

- **지워야 하지만 지우지 않은 것(삭제 승인 대상)**: `qa/upgrade/gates-wip-01-01.json`·`gates-wip-01.json` · 사용자 디스크 `.cache/ch29-01-view/`(삽화 확인 사본 596KB) · 기기 `/tmp/ch29-01/`(탐색 `exp/`·시험 실행 `try/`·사본 `B/`·`A.ipynb`·삽화 원본 `illu/`·검사 도구 `tools/`·생성기 조각 `gen/`, 약 6.6MB) · 옛 그림 `figures/01-흐름.{svg,excalidraw,caption.md}`(본문 참조 0, 공개 목록에 줄 없음).
- 마감 몫: 옛 생성기 둘 `mv -n` · `part6-practice.zip` 다시 만들기(도구 파일·01 새 판) · 실습 폴더 README(「01·02·04절은 저장된 실제 궤적」 틀림, 도구 파일 단락) · `chapter.json` `objectives`(「코드와 궤적」·「같은 평가셋과 명시적 기준」 — 「명시적」 금지어) · 옛 기록 파일 「개선 전 판」 표시.
- **강사 확인 대상**: ① 코드 줄 28 → 120(셀 5 → 23) ② 최종 답 평가를 글자 비교로 둔 설계(뜻을 못 가르는 한계를 값 바꿔 보기로 보임 — 옛 판 부분 글 포함 규칙에서 바꿈) ③ 도구 이름 `search_documents`(Ch 21 05 이름 빌림)·`check_source`와 결과 글은 교재용(도구 함수 없음) ④ 새 용어 다섯 ⑤ 도구 파일 이름 `eval_tools.py`(내장 `eval`과 글자가 닮음) ⑥ 삽화의 구멍 수·띠 길이 차이·아래 띠 기울기·상자 손잡이 ⑦ 제목 「Agent 평가 — 답과 실행 경로를 함께 보기」(「경로」 — 제목에만)·03 「LLM judge」·04 「Ch18 궤적」 ⑧ 「판정 모델」이 아니라 Ch 15 말 「평가 모델(judge)」로 둠.
- 기기 디스크: 작업 전 루트 **2.1G**·`/sessions` **831M** → 작업 뒤 루트 2.1G·`/sessions` 831M(같음).

## 마감 반영 (2026-09-29)

검토 1차(`review-round1-A.md`) 반영. **노트북은 다시 실행하지 않음** — `code_sha256` `b7a67c68540b…`·`outputs_sha256` `8a4db6c2b86e…`·`executed_at` 01:18:40Z 그대로(마크다운 셀 0·6·18만 바뀜, 파일 `debd4640` → `a693de5c`). 고친 방법: 생성기 문자열 치환(`.cache/ch29-close/tools/gapply29.py` — 치환 수가 다르면 멈춤, 코드 셀이 한 글자라도 다르면 멈춤) → 달라진 마크다운 셀만 노트북에 옮김 → `src_html()`로 `_src` → `run_section.sh … 01 --no-exec`(게이트 0).

- **A-1 「궤적」 정의 넓힘**: b4 「궤적과 기준 궤적」 첫 단락(질문·모델 응답·도구 결과·마지막 답을 차례대로 담은 메시지 목록 · 도구 이름만 모은 「도구 차례」 · 모드는 그 가운데 도구 호출 요청을 견줌) · 용어 표 「궤적」·「궤적 맞춰 보기」 칸 · 비유 「구멍을 차례대로 읽어 끝 소리까지 내는 띠 한 줄이 궤적」 · 노트북 [0] 할 일 1·[6] 2절 첫 단락·[18] 결과 읽기(「이 목록은 도구 이름만 모은 도구 차례이고, 궤적은 … 메시지 목록 전체」).
- **A-5**: 모드 `strict` 정의 「메시지 수·역할·차례」 → 「메시지의 수·역할·차례」(용어 표·「세 평가가 보는 자리」 두 곳).
- **A-2(삽화 01-5 — 다시 만들지 않음)**: 그림 읽기 끝 문장을 「구멍의 수, 띠의 길이와 기울기, 상자의 손잡이는 어떤 값과도 짝짓지 않고, 두 띠가 같은 궤적인지도 나타내지 않습니다」로(문장 수 다섯 그대로). 재생성은 강사 확인.
- **A-10**: 커널 폴더 문장(검토 A-10): 가져오기 결과 읽기의 「교재 출력은 실행 도구가 `notebooks/` 폴더를 가져오기 자리에 더해 준 실행입니다」를 빼고, 고정 문장 「노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다」 뒤에 Part 6(Ch 24~28) 두 문장 「커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다」·「교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다」를 둠(단락을 나눠 다섯 문장 안).
- **A-7(01 셀 37 `trajectories` 딕셔너리 한 줄 116칸) — 미반영**: 01은 이번 마감에서 다시 실행하지 않는 노트북이라 코드 셀을 바꾸지 않음(다음 재실행 몫 — 최종 점검표 §2-17).
- 그림·캡션·`.mmd` 바뀐 것 0. 금지어 0(참고 자료 원제목 「LangSmith Trajectory evals」 거짓 양성 말고), 검사 문장 358 → 360.
