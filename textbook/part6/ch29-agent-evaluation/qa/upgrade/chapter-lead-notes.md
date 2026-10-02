# Ch 29 Agent 평가 — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part6/ch29-agent-evaluation`(절 넷, 모두 experiment) · `labs/part6/ch29-agent-evaluation`. 바로 앞 Ch 28(완료, 모델 결정 M2)을 잇는 Part 6 아홉째 챕터이자 Part 6 마지막 챕터입니다.
- 준비 산출물: `qa/upgrade/before/`(원본 사본 39개, 549,256바이트 — 원본과 바이트 대조 39/39 같음) · `gates-before.json`(`fb2f153e…`) · `before-manifest.json`(217개, `4aa29f63…`) · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch29-agent-evaluation`(262MB, 사용자 디스크).
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(전부) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · 과정 요약(§0~§9 전부) · 계약 파일(`grep -n '^#'` 뒤 §3 Ch18·Ch21·Ch28 줄, §4 도구 파일 줄, §5 묶음 줄, §8 기준 버전) · Ch 28 `chapter-summary.md`(전부)·`chapter-lead-notes.md`·`before-manifest.json`(모양) · Ch 21 요약 §9·§15 · Ch 18 요약 §8·§12·§13 · Ch 15·17 요약(용어·비유·함수) · Part 6 목록·묶음·검사 스크립트 · 챕터 `qa/` 기록·`집필점검표.md`. `textbook/qa/upgrade-progress.md`는 읽지 않았습니다.
- **원고·노트북·그림은 하나도 고치지 않았습니다.** 연결 폴더 안 파일 삭제 0건, 노트북 실행 0건, 서비스 모델 요청 0건, `uv cache prune` 안 함. 확인은 기기 `/tmp/ch29-prep/exp/`의 작은 스크립트(`e1`~`e4`)와 설치판 소스·공식 문서로 했습니다. 모델 객체는 가짜 키 글로 **만들기만** 했습니다(요청 0). 모든 파이썬 호출은 `PYTHONDONTWRITEBYTECODE=1`, 확인 스크립트는 `OPENAI_API_KEY`를 지운 환경.
- `chapter.json` `hours` = 「총 8h · 강의 3h · 실습 5h」. 절 meta 강의 0.75h × 4 = **3h**, 실습 1.25h × 4 = **5h** — 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part6/_build_index.py` 27행 (3, 5)·`qa/check_scope.py` `EXPECTED` (3,5)·`SECTION_COUNTS` 4도 같습니다. 새 용어 meta 5·5·5·5(옛 생성기 틀 값 — 실제 새 말 목록 없음).

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-29)

| 절 | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 에이전트 평가 세 전략 | 5 | 61 | 3 | 2 | 0 | 0 | 6 | 13 | 3 | 27 |
| 02 궤적 매칭 네 모드 | 5 | 62 | 2 | 2 | 0 | 0 | 7 | 27 | 3 | 41 |
| 03 LLM judge로 궤적 평가 | 5 | 61 | 1 | 0 | 0 | 0 | 6 | 12 | 3 | 22 |
| 04 운영 지표와 Ch18 궤적 비교 | 9 | 70 | 14 | 0 | 0 | 0 | 10 | 14 | 3 | 41 |
| **합계** | **24** | **254** | **20** | **4** | **0** | **0** | **29** | **66** | **12** | **131** |

- 통과 절 **0/4**. 코드 줄(주석·빈 줄·`%pip` 뺌) 01 27 · 02 36 · 03 30 · 04 59 = **152줄**(`/tmp/ch29-prep/ast_scan.py`).
- G1 20 = `*args` 정의 3(01·02·03의 같은 `trace(*tools: str)`) · 리스트 내포식 8 · 제너레이터 식 9(04 c16 하나에 다섯).
- G2 4 = 한 글자 변수 `m`·`c`(01 c8·c10, 02 c6).
- **G3 0이지만 주석 틀 문제 있음** — 설치 셀·환경 셀 주석이 네 절 같은 글(「공개하지 않은 API 키는 존재 여부만 확인하고…」인데 01·02·04는 키를 확인하지 않음).
- **G4 0이지만 규격 §3을 어김** — 03 judge가 `create_trajectory_llm_as_judge(model="openai:gpt-5.4-mini", …)` 문자열이라 `init_chat_model` 셀이 없어 게이트가 못 봄. `temperature=0`·`reasoning_effort="none"` 둘 다 없음(설치판은 문자열이면 `init_chat_model(model=model)`만 부름 — openevals 0.2.0 `llm.py` 254행).
- G5 29 = 제목 셀·핵심 그림 첨부 없음 8 + 결과 읽기 인용 없음 17 + 마지막 셀 뒤 결과 읽기 없음 4.
- G6 66 = 70자 넘는 문장·영문 시작 조사(「strict는」·「`trace()`는」·「p95는」·「Ch18의」 등). §4 금지어는 G6가 대부분 세지 않음(§1 표).
- G7 12 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 것 (AST로 따로 셈)

- **별표 풀기 `[Path.cwd(), *Path.cwd().parents]`**: 네 절 환경 셀(`.env` 찾기) + 04 c6 `find_project_root`(과정 요약 2-2 금지 모양).
- **f-string**: 01·02·03 `trace()` 안 `f"c{i}"` 둘씩 · 04 c10 `f"Ch18:{pattern}"`·c14 `f"Ch21:{record['qid']}"`.
- **타입힌트**: `-> list`(01·02·03) · 04 `find_project_root(start: Path) -> Path`·`nearest_rank_p95(values: list[float]) -> float`·변수 힌트 `workflow_rows: list[dict]`·`agent_rows: list[dict]`.
- **그 밖**: `enumerate(tools, 1)`·`+=`(`messages += [...]`)·`getattr(m, "tool_calls", [])`(01·02)·`sum(…)`(01) · 04 `all(…)`·`max(…)`·`statistics.mean`(과정 처음 — Ch 15 06은 손으로 만든 `average`)·`round(…, 3)` 다섯 번 한 줄·`.get(...)` 셋(c8)·튜플 대입 여섯 칸(c10)·`raise FileNotFoundError`·독스트링 둘 · 03 `assert os.getenv(...)`(키 셀이 준비 셀과 한 셀).

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 요청(한 번) | 파일 읽기·쓰기 | 손 값 | 금지어(`_src` / 노트북 md / 주석) | `assert`(무엇에) |
|---|---|---|---|---|---|---|
| 01 | 코드로 만든 궤적 `trace("search_rules","check_source")`(인자 `{"topic":"대출"}`·도구 결과 「확인」·답 「일반 도서는 14일입니다.」)에서 ① 최종 답 `"14일" in actual[-1].text` ② 첫 도구 이름 ③ 도구 이름 목록을 뽑고, 같은 답에 검색 세 번인 낭비 궤적과 견줌(호출 2 ↔ 4). 평가 **라이브러리를 쓰지 않음**(손으로 쓴 세 줄) | **0**(평가 대상 에이전트 0 · judge 0) | 읽기: `.env`(쓰지 않음). 쓰기 0 | 궤적 전체(도구 이름·인자·결과·답) · 출력 `reference calls: 2`(손으로 적은 2) | 반환 3/0 · 측정 3/1 · 지연 1 · 경로 0/2 · 보장 2 · 블랙박스 2 · 궤적 14/4/2 · 영어 용어 Final Response·Single step·Trajectory | `"14일" in … and len(wasteful) > len(reference)`(**만든 대로 늘 참**) |
| 02 | `create_trajectory_match_evaluator(trajectory_match_mode=…)` 네 모드: 뒤집은 궤적 strict `False`·unordered `True`, 짧은 궤적(search만) subset `True`·superset `False`, 덤 궤적(`audit_log` 더함) subset `False`·superset `True` | **0** | 읽기 `.env`만. 쓰기 0 | 궤적(01과 같은 `trace`) | 반환 1/1 · 경로 3/1 · 사전 1/1 · 필드 1 · 옵션 1 · 집합 2/2 · 보장 1 · 검증 0/0/1 · 궤적 16/5/3 · 모드 이름 영어 넷 | 라이브러리 점수 넷(**결정적 — 허용**) |
| 03 | `create_trajectory_llm_as_judge(model="openai:gpt-5.4-mini", prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE)`로 **실제 궤적 = 기준 궤적**(같은 `trace`)을 판정 → `score True`·영어 `comment`, strict `True`와 나란히 출력 | **1**(judge 1 · 평가 대상 에이전트 0) · 저장 기록 셀 2.13초 | 읽기 `.env`(키 필요). 쓰기 0 | 궤적 · 모델 이름 문자열 | 반환 3/2 · 측정 3 · 지연 3 · 경로 4/2 · 사전 1/2 · **프롬프트 7/2** · **루브릭 6/2** · 재실행 1 · 피평가 1/1 · 궤적 18/4/1 · 제목 영어 「LLM judge」 | 키 있음 · `evaluation["score"] in [True, False]`(자료형) · strict `True`(결정적) |
| 04 | Ch 18 06 노트북 **저장 출력**의 `" | "` 줄 마지막 다섯과 Ch 21 06 `data/rag-comparison.json` 세 줄을 공통 칸 `final_score`·`model_calls`·`tool_calls`·`tokens`·`latency_s`로 바꿔 평균·가장 가까운 자리 방식 95 백분위수 | **0** | **읽기**: Ch 18 06 노트북 파일(JSON, 저장 출력) · Ch 21 06 계약 파일 · `커리큘럼_v6.html` 있는지(`assert`). 쓰기 0 | Ch 18 `tool_calls: 0`(손으로 넣은 상수) · `quality/5`로 나눔 · `0.95` · `_src` 옛 평균(§3) | 측정 4 · 추정 1/1 · **지연 8/1/2** · 스텝 2 · 불리언 1/1 · 필드 1/2 · **Agentic 3/1** · 판정식 1/1 · 열(→칸) 12/3/2 · 수치 1 · 운영 화면 1 · trace 0/0/1 · 경로 0/0/1 · 제목 「Ch18 궤적」 | 표 줄 ≥ 5 · `status` 모두 `ok` · 줄 3 · `tool_calls ≥ 1` · 두 목록 있음 · p95 ≥ 최댓값 · **`커리큘럼_v6.html` 있음(학생 묶음에서 멈춤 — §4)** |

- **서비스 요청 합계(한 번 실행)**: 01 0 · 02 0 · **03 1** · 04 0 = **1번**. 평가 대상 에이전트를 실제로 돌리는 절 0(01~03 궤적은 모두 코드로 만든 메시지, 04는 저장 기록). 임베딩 0.
- **`temperature=0`·`reasoning_effort="none"`**: 0곳(03 judge에 둘 다 없음).
- **흔들리는 값**: 03 judge 점수와 `comment` — 같은 입력에 대해 **옛 기록끼리 결과가 다름**: 저장 노트북(2026-09-10 16:29 실행)은 `True`, `qa/verification.md`·옛 생성기 `DETAILS`·`집필점검표.md`(2026-09-11)는 `False`(「질문이 모호한데 대출 주제를 임의로 골랐다」). 04 값은 파일을 읽는 한 결정적이지만, 원래 한 번 잰 값(걸린 초·토큰)이라 앞 챕터를 다시 실행하면 바뀜(§3).
- **걸린 시간**: 04만 앞 챕터가 잰 값을 읽음. 저장된 셀 기록(참고만): 01·02·04 1초 안, 03 judge 셀 2.13초.
- **옛 그림 토큰**: 절마다 b4 「도식 읽기」의 `{{svg:NN-흐름}}` 하나(`figures/_gen_figures.py` → `textbook/part5/_figure.py`) · 노트북 토큰 `{{notebook:slug}}`. Mermaid·삽화 0장. **챕터 공개 목록에 옛 SVG 줄 없음**(Ch 28과 다름).
- 노트북 `metadata.verification`: 넷 모두 `passed`, 실행일 **2026-09-10**(01 16:11 · 02 16:11 · 03 16:29 · 04 16:37 UTC). `code_sha256` 앞 12자 01 `6ed13ca33e52` · 02 `c2807667e2b7` · 03 `0bc0530051bb` · 04 `0c6de54fd899`. 셀 수 11·11·11·19. 파일은 `part6-practice.zip` 안 판과 바이트 같음. **마크다운은 09-14에 옛 보조 스크립트가 끼움**(`.moai/…/part6b_enrich.py` — 「코드 읽기와 비교 경계」 두 단락, 코드·출력 그대로).
- 노트북 설명 셀: 제목 한 줄 · 「패키지 설치」·「환경 준비」 · `_src` b4 「코드 읽기와 비교 경계」와 같은 글 · 소제목 한두 문장 · **결과 읽기 셀 0**, 「이 노트북에서 할 일」·준비물(요청 수·비용·시간)·실행일 문장 없음, 셀 첨부 그림 0.
- `_src` 틀(옛 생성기 `textbook/part6/_author_ch21_ch29.py` + 보조 스크립트): b3 「필요한 자료와 객체는 노트북에서 다시 선언하므로…」 네 절 같음 · b5 「확인할 점」 = b6 첫 단락 = b8 둘째 항목(글자까지 같음) · b8 첫 항목 = b4 정의 단락 · b10 참고 자료 둘이 네 절 같음(확인 2026-09-11) · 03 b7 「절당 1달러 미만으로 예상」(옛 틀) · 04 b5 첫 문장 「데이터·함수·객체 생성·invoke·관찰을 짧은 셀로」(04에 `invoke` 없음 — 틀 문장) · 복습 셋씩.

## 2. 절별로 더 봐야 할 것

### 01 에이전트 평가 세 전략
- **b3 「Ch11 평가셋과 Ch21 에이전트를 사용합니다」는 틀림** — 01은 둘 다 쓰지 않음(코드로 만든 궤적만). Ch 21 인계(요약 §15 222행)도 「느슨함」. Ch 28 06 b8(01 슬러그 링크 「Ch 29 01절은 평가 방법 세 가지를 견줍니다」)과 맞으려면 **01 슬러그 `01-에이전트-평가-세-전략` 고정**, 01 b2가 세 방법 비교를 받아야 함(지금 b2 질문 「Final Response·Single step·Trajectory는 각각 어떤 실패를 발견하는가?」 — 뜻은 맞음, 말은 영어).
- 공식 문서(LangSmith evaluation-approaches, 2026-09-29 확인): 최종 답(속을 보지 않고 마지막 글, 평가 모델이 판정 — 느리고 원인 찾기 어려움) · 한 단계(도구를 맞게 골랐는지, 참·거짓·규칙 검사 — 빠르지만 한 순간만) · 단계 차례(기대한 도구 호출 차례로 답에 닿았는지 — 정확한 차례 맞추기·단계 수·평가 모델). 지금 b4 정의와 뜻이 맞음.
- **결정적 값 후보(모델 없음, 설치판에서 확인)**: 같은 궤적 · 낭비 궤적(검색 셋) · **답만 틀린 궤적**(도구 차례 같고 답 「7일」) — 세 방법에 넣으면 최종 답 평가만 답 틀림을 잡고, 단계 차례 평가(네 모드 모두 `True`)는 못 잡음(§6-1 — strict도 메시지 내용을 보지 않음). 01이 「셋이 서로를 대신하지 않는다」를 결정적으로 보일 수 있는 가장 짧은 장면.
- 한 단계 평가를 실제 모델로 보이려면 Ch 19 04 모양(`bind_tools` + `tool_call_names`, Ch 19 요약 — 04 45/45 같음)이 선례. 쓰면 요청이 생김(§8).
- 01은 지금 평가 라이브러리를 부르지 않음 — 「세 전략」을 라이브러리 함수로 보일지(최종 답 = openevals `create_llm_as_judge`+`CORRECTNESS_PROMPT`(모델 요청) 또는 문자열 비교, 단계 차례 = 02의 함수 앞당김) 손으로 쓴 세 줄로 둘지 결정.

### 02 궤적 매칭 네 모드
- **모델 없이 네 모드 결과를 결정적으로 출력할 수 있음**(§6-1 표, 다섯 번 같음). 지금 판 세 궤적 외에 쓸 만한 대조: 낭비 궤적(strict·unordered·subset `False`, superset `True` — **같은 도구를 여러 번 부르면 subset·unordered가 떨어짐 = 횟수도 셈**) · 인자만 다른 궤적(네 모드 모두 `False` → `tool_args_match_mode="ignore"`면 `True`) · 한 응답에 도구 요청 둘(strict `False`, 나머지 `True` — strict는 메시지 모양까지 봄) · 답만 틀린 궤적(네 모드 모두 `True`).
- b4 「`subset`은 실제 호출이 기준에 나온 도구 안에서만」 — 이름만이 아니라 **인자·횟수까지** 맞춰 짝지음(설치판 `trajectory/utils.py` 90~134행). b6 「기본 매칭은 도구 이름과 인자까지 비교」 참(`exact`). 인자 비교 방식 넷(`exact`·`ignore`·`subset`·`superset`)과 도구별 덮어쓰기(`tool_args_match_overrides` — 모드 글·함수·키 목록)는 설치판·PyPI 설명과 맞음. 「인자 무시 옵션」은 `tool_args_match_mode="ignore"` 또는 덮어쓰기.
- Ch 17 04 `_src`·HTML이 「에이전트의 단계 차례를 맞춰 보며 평가하는 방법은 Ch 29 02절에서 다룹니다」(링크 없음, 두 곳) — 02가 차례 맞추기를 다루는 한 참.
- 결과 딕셔너리 `{'key': 'trajectory_strict_match', 'score': …, 'comment': None, 'metadata': None}` — 결과 읽기는 `score`만 인용하는 편이 G5에 안전.

### 03 LLM judge로 궤적 평가
- 지금 판은 **실제 = 기준**(같은 궤적)이라 strict와 judge가 같은 답을 내는 장면만 보임(b4가 스스로 「기본 동작만 확인」). judge가 보태는 것(구조는 같아도 뜻이 다른 궤적, 또는 구조는 달라도 뜻이 같은 궤적)을 보이려면 대조 궤적이 필요.
- **judge 입력·출력 모양(설치판)**: 평가 함수 인자 `outputs`·`reference_outputs`(메시지 목록 또는 `{"messages": …}`) → 메시지를 `<user>…</user>`·`<assistant><tool_call><name>…</name><arguments>…</arguments></tool_call></assistant>`·`<tool><tool_result>…</tool_result></tool>` 모양 글로 바꿔 머리글(판정 기준 네 줄: 단계 사이 논리·진행·상대적 효율·기준과 뜻이 같음)에 끼움 → **모델 요청 1번**(`with_structured_output` — 이 판은 `json_schema`, 칸 `reasoning`(글)·`score`) → `{'key': 'trajectory_accuracy', 'score': True/False, 'comment': reasoning, 'metadata': None}`. `continuous=True`면 0~1 소수, `choices=[…]`면 고른 값 하나. 네 메시지 궤적 하나의 요청 글은 머리글 포함 약 1,075자(기준을 함께 넣을 때, `e2_judge.py`).
- **`judge=` 인자에 모델 객체를 넘길 수 있음** → `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(규격 §3 모양 그대로)를 만들어 `create_trajectory_llm_as_judge(judge=model, …)`. 가짜 키로 만들기까지 확인(요청 0).
- 머리글이 영어·`comment`도 영어로 옴(저장 출력 「The actual trajectory matches…」) — 결과 읽기는 `score`만 결론에, `comment`는 둘째 단락에(흔들림, §8).
- Ch 15와 잇기: Ch 15 01 「평가 모델(judge)」·02 「판정 머리글·판정 요청 글」·03 「치우침(위치 치우침)·차례 바꾸기 검사」·04 「제시 라벨·일치율」. Ch 15는 `init_chat_model` + 손으로 쓴 머리글 + `json.loads`(도구 파일 `build_judge_prompt`·`judge_once`), 여기는 라이브러리가 머리글·출력 형식을 정함 — 차이를 한 문장으로.
- 요청 수 셈(Ch 26~28): judge는 평가 한 번에 요청 1번(평가 대상 에이전트의 요청과 따로 셈).

### 04 운영 지표와 Ch18 궤적 비교
- **계약 둘을 읽기만 함**(§3). 04가 파일을 쓰지 않음(다시 만들지 않음).
- **학생 묶음에서 지금 멈춤**: c6 `find_project_root`가 위로 올라가며 `textbook/`과 `labs/`가 함께 있는 폴더를 찾고 `커리큘럼_v6.html`을 `assert` — `part6-practice.zip`에는 `textbook/`·`커리큘럼_v6.html`이 없음(맨 위 `labs/`·`시작하기.md`·`env.example`·`manifest.json`뿐). `/tmp/ch29-prep/bundle`에 풀어 확인: 찾기 결과 `None` → `FileNotFoundError`. 묶음 안 상대 위치는 `notebooks/`에서 `../../ch21-create-agent/data/rag-comparison.json`·`../../../part5/ch18-workflow-patterns/notebooks/06-같은-과제로-다섯-패턴-비교.ipynb`(둘 다 있음). → 과정 경로 셀(`candidates` + `for`·`break`, 묶음 맨 위·실습 폴더 맨 위·`notebooks` 세 자리)로 바꿔야 함.
- 「Ch18 궤적」은 사실과 다름 — Ch 18 06 표는 도구 호출 없는 워크플로우의 요청 수·토큰 수·걸린 초·품질 칸(코드 검사 0~5)이고 도구 궤적이 없음(`tool_calls: 0`은 04가 손으로 넣은 값). 제목 슬러그는 Ch 21 06 b2가 링크(`../ch29-agent-evaluation/04-운영-지표와-Ch18-궤적-비교.html` — `_src` 8행·HTML 146행)해 **고정**.
- **품질 칸 뜻**(Ch 18 인계): Ch 18 `quality/5` = 코드 검사 다섯 항목(120~180자 + 꼭 담을 말 넷) ↔ Ch 21 `agent_supported` = 평가 모델 판정(참·거짓). 한 칸 `final_score`에 넣어도 척도가 다름(지금 b4·b6이 이미 한정 — 「최종 품질」 말만 넓음).
- 모델 없이 할 수 있는 확장(확인함, `e4_ch21.py`): Ch 21 기록의 `agent_trace`(검색어·문서 ID)를 메시지로 바꿔 기준 궤적(`search_documents` 한 번)과 네 모드로 견주면 인자 `exact`는 세 줄 모두 `False`(검색어가 다름), `ignore`는 모두 `True`. 첫 검색 결과 맨 앞 문서 = 정답 문서 ID(세 줄 모두). 도구 이름 `search_documents`는 Ch 21 06 노트북 셀의 이름(기록 파일에는 없음 — 손으로 넣는 값).
- 95 백분위수: Ch 15 06 `nearest_rank(values, percent)`(노트북 셀 — Ch 15 도구 파일에는 없음)와 같은 계산. 지금 04는 이름·인자가 다른 `nearest_rank_p95(values)`를 새로 적음(§2-7 3번과 충돌). 세 값이면 늘 최댓값(b4가 이미 밝힘).
- b8 「Ch30 최종 프로젝트 평가 설계」 — Ch 30은 FastAPI 서빙(Ch 30 09 b7 「Ch29 평가셋으로 … 반복 평가」). 실습 절을 붙이면 05로 옮김.

## 3. 계약 대조표 — Ch 21 06·Ch 18 06 → Ch 29 04 (가장 중요)

### 3-1. 파일

| 파일 | 해시(지금) | 모양 | 04가 읽는 것 | 만든 쪽 |
|---|---|---|---|---|
| `labs/part6/ch21-create-agent/data/rag-comparison.json` | **`25cfe5df3cfd729c130bce4af26c716cfcc3bcd4b4ff6e4a9d0a725816b02f51`**(계약과 같음) | 줄 3(`C01`·`C05`·`C07`) · 칸 12(`qid`·`gold_doc_id`·`fixed_answer`·`agent_answer`·`fixed_doc_ids`·`agent_trace`·`tool_calls`·`fixed_usage`·`agent_usage`·`agent_latency_s`·`fixed_supported`·`agent_supported`) | `qid` · `agent_usage`{`model_calls`·`input_tokens`·`output_tokens`} · `agent_supported` · `tool_calls` · `agent_latency_s` · `agent_trace` | Ch 21 06(**다시 실행 금지**) |
| `labs/part5/ch18-workflow-patterns/notebooks/06-같은-과제로-다섯-패턴-비교.ipynb` | **`5ba7f5a01fa8a8625a4673e6f6a007691907078b20c41ee828aa266252ba0b20`**(`code_sha256` `f37b5df47a1a…`, 실행 2026-09-23 22:07:51Z) | 셀 49(0부터 셈)의 저장 출력: 머리 `pattern | calls | tokens | latency_s | quality/5 | status` + 다섯 줄 + `상태가 ok인 줄 수: 5` | `" | "`가 든 줄 가운데 `pattern`으로 시작하지 않는 줄의 **마지막 다섯**, 여섯 칸 | Ch 18 06(**다시 실행 금지**) |

- 흉내 검사(지금 04 셀 8·10·12·14·16·18의 읽기 코드와 `assert` 그대로, `/tmp` 파이썬): **PASS** — 표 줄 **5**(옛 저장 출력은 6) · `ok` 다섯 · 줄 3 · `tool_calls ≥ 1` · p95 ≥ 최댓값.
- **Ch 29가 이 두 파일을 다시 만들지 않음**(04는 읽기만, 쓰기 0). 옛 생성기 `_author_ch21_ch29.py`의 Ch 21 쪽(파일을 쓰는 셀)은 막혀 있음.
- **학생 묶음**: 두 파일 모두 Part 6 선행 목록(`textbook/part6/prerequisite-files.json` 13줄 가운데 셋 — Ch 18 06 노트북·`workflow_tools.py`·계약 파일)과 Ch 29 `qa/prerequisite-files.json`(같은 셋)에 있고, `part6-practice.zip`(`5002dce3…`, 111항목) 안 판이 디스크와 바이트 같음. Ch 14 `documents.json`·`queries.json`도 묶음에 있음.

### 3-2. 옛 인용값 ↔ 새 값

| 자리 | 옛 값(지금 글) | 지금 파일로 셈한 값 | 성격 |
|---|---|---|---|
| `_src/04-…html` **6행**(b5 확인할 점)·**7행**(b6 첫 단락)·**9행**(b8 둘째 항목) — 같은 문장 셋 | Ch 18 다섯 패턴 평균 final_score **0.88**, 모델 **2.8**회, **610.2**토큰, **4.145**초 | **0.96 · 2.8 · 862.2 · 4.206** | 결정적 읽기 · 걸린 초·토큰은 Ch 18이 한 번 잰 값 |
| 같은 세 줄 | Ch 21 세 행 평균 final_score **1.0**, 모델 **2**회, 도구 **1**회, **519.7**토큰, **1.880**초 | **1.0 · 2 · 1 · 688 · 1.731** | 1.0·2·1은 Ch 21 06이 세 질문·다섯 번 확인에서 같았던 값 · 688·1.731은 한 번 잰 값 |
| 같은 세 줄 | Agent 세 건 p95 지연 **2.094**초, 토큰 **541** | **2.003 · 699** | 셋이면 최댓값(C07) |
| 같은 파일 **10행** 복습 3 해설 | 「**2.094초**였습니다」 | **2.003** | 걸린 초 |
| 노트북 04 저장 출력 셀 8 | `Ch18 실제 표 행: 6` + 옛 다섯 줄(`chaining | 2 | 428 | 3.513 | 5 | ok` …) | `5` + `chaining | 2 | 712 | 3.756 | 5 | ok` · `routing | 2 | 503 | 2.746 | 5 | ok` · `parallel | 3 | 676 | 1.043 | 4 | ok` · `orchestrator_worker | 5 | 1790 | 6.519 | 5 | ok` · `generator_evaluator | 2 | 630 | 6.966 | 5 | ok` | 다시 실행하면 바뀜(모델 없음) |
| 셀 14 | 토큰 526·492·541 · 초 2.007·1.538·2.094 · 검색어 옛 셋 | **684(632+52)·681(638+43)·699(638+61)** · **1.829·1.36·2.003** · 검색어 「책 대출 기간」·「토요일 자료실 폐관 시각」·「휴학 원격 전자자료」, 문서 첫 자리 `LIB-001`·`FAC-003`·`ACC-002`(= 정답 문서 ID) | 〃 |
| 셀 16·18 | 평균 둘 · p95 | 위 두 줄 | 〃 |
| 기록만(고치지 않는 옛 문서) | `집필점검표.md`·`qa/verification.md`·옛 생성기 `DETAILS` 「518.3토큰, 1.885초 · p95 2.037초·544」 | — | 더 옛 실행 값 — 챕터 마감 때 「개선 전 판」 표시 |

- Ch 18 쪽 값 뜻: `calls` = 모델 요청 수, `tokens` = 요청마다 입력+출력 합, `latency_s` = 흐름 하나 걸린 초, `quality/5` = 코드 검사, `status` = 흐름이 끝난 상태. **평가 모델 점수가 아님.**
- **걸린 초를 본문 숫자로 둘지부터 01 작업자가 정할 것**(Ch 21 인계). 파일을 읽는 한 새 커널 두 번에서 같음(규격 §2-7 9번의 「두 번 같은 값」 조건은 만족) — 그러나 값 자체는 앞 챕터가 한 번 잰 것이라 앞 챕터를 다시 실행하면 바뀜. 선택지는 §8-3.
- **말**: 옛 글의 「Agentic RAG」·「지연」·「스텝」·「불리언」·「열」·「필드」는 과정 금지어 → Ch 21 06 말(「에이전트 흐름」·「걸린 초」)·「칸」·「참·거짓 값」.

## 4. 실습 폴더 구조와 읽는 곳

```
labs/part6/ch29-agent-evaluation/
  README.md (3줄 — 「01·02·04절은 저장된 실제 궤적과 결정적 평가」: 01·02는 코드로 만든 궤적이라 틀림)
  pyproject.toml   uv.lock (package 94, export 93줄)
  notebooks/01~04-*.ipynb
  .venv/ (macOS 판 187MB, uv 0.11.6)
  (없음: data/ · runs/ · tests/ · 도구 파일 · 노트북 생성기 · __pycache__)
```

- **판**: `requires-python = ">=3.12,<3.13"`, `dependencies = ["agentevals==0.0.9", "langchain==1.4.0", "langchain-openai==1.6.0", "langgraph==1.2.11", "python-dotenv==1.2.3", "pillow>=11.0"]`(**`pillow`는 import 0** — Ch 21 B-16과 같은 줄), dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`, `[tool.uv] package = false`. 잠금 주요 판: **`agentevals 0.0.9`(PyPI 최신, 2025-07-24)·`openevals 0.2.0`·`langsmith 0.12.4`**·`langchain 1.4.0`·`langchain-core 1.6.2`·`langchain-openai 1.6.0`·`langgraph 1.2.11`·`langgraph-prebuilt 1.1.0`·`langgraph-checkpoint 4.2.0`·`openai 3.11.0`·`pydantic 2.13.5`·`pillow 12.3.0`·`tiktoken 0.14.0`. **`numpy`·`pandas` 없음.** `pyproject.toml`·`uv.lock` 수정 시각 09-10 그대로.
- **Ch 28 잠금과 견줌**: 겹치는 90개 **판 모두 같음**. Ch 29에만 `agentevals`·`openevals`·`pillow`(+ 프로젝트 이름). **Ch 21 잠금과 견줌**: 겹치는 판 모두 같음, Ch 21에만 `numpy 2.5.3` → Ch 21 `runner_tools.py`는 맨 위 `import numpy`라 이 잠금에서 가져오기 자체가 멈춤. Ch 28 `connect_tools.py`는 `fastmcp`가 없어 멈춤.
- **노트북이 코드로 읽는 파일**: 네 절 `.env`(01·02·04는 읽기만 하고 쓰지 않음) · 04만 Ch 18 06 노트북·Ch 21 계약 파일·`커리큘럼_v6.html`(있는지). **쓰는 파일 0**. SQLite 0(Ch 23 연결 폴더 멈춤 문제 해당 없음).
- **Ch 29 파일을 코드로 읽는 곳**(`grep -rn`, `textbook`·`labs`, `.venv`·`before` 제외):

| 자리 | 무엇을 | 성격 |
|---|---|---|
| `textbook/part6/public-files.json` 86~92행 | README·노트북 넷·잠금 둘 | 묶음 허용 목록 |
| 챕터 `qa/public-files.json` | HTML 다섯(목차 포함)·실습 파일 일곱 = 12줄(**옛 SVG 줄 없음**) | `collect_public_files.py`가 Part 목록으로 모음 |
| 챕터 `qa/prerequisite-files.json` | Ch 18 06 노트북·`workflow_tools.py`·Ch 21 계약 파일 | 선행 묶음(§3-1) |
| `textbook/downloads/part6-practice.zip`(111항목)·`llm-practice.zip` | Ch 29 7파일이 디스크와 같음(part6) | 묶음 |
| Part 6 `qa/check_bundle_execution.py` | Ch 24 01·Ch 28 01만 — **Ch 29 없음** | 계약 없음 |
| `textbook/part6/_build_index.py` 27행 · `_notebook/build_index.py` 62~63행 · `build_bundle.py` 27행 | (3, 5, 「최종 답변·한 단계의 선택·전체 궤적을 평가하고 운영 지표를 비교합니다.」) · (절 수 4, 같은 설명) · 공개 챕터 목록 | 실습 절을 붙이면 Part 목차 절 다섯(`build_index.py`는 실습 절을 빼고 세는 약속 — 4 그대로) |
| **Part 7 Ch 33 `labs/part7/ch33-cicd/data/regression-baseline.json`** | `source_files`에 **Ch 29 04 노트북 옛 해시 `71fa56ef…`**(지금 파일 `b8c1b9d2…` — 이미 다름) | **출처 기록만** — `scripts/evaluate_regression.py`·`tests/`가 해시를 확인하지 않음(`grep`), README가 「Ch29 개념을 다시 쓴 교육용 기준선, 원본 발췌 아님」. 04를 바꿔도 코드는 깨지지 않음 — 인계 기록 |
| 옛 검사(고치지 않음, 기록만) | `check_scope.py` `EXPECTED` (3,5)·`SECTION_COUNTS` 4(실습 절을 붙이면 4 ≠ 5, 이미 Ch 21 07에서 멈춤) · `check_notebook_readiness.py`(노트북 47 단언 — 결과 파일을 먼저 씀 → 되돌림 선례) · `check_figures.py`(SVG마다 `.excalidraw` 짝 — Ch 29 옛 넷은 짝 있음) · `check_visual_reports.py` · `check_delivery.py`(`llm-practice.zip` Part 1 Stale) · `textbook/qa/check_course_continuity.py`(Ch 29 줄 0) | Ch 21~28 선례대로 이미 어긋난 상태 |
| 기록만 | `final-artifact-hashes.json` Ch 29 줄 30 — **12줄 이미 옛 해시**(HTML 4·`_src` 4·노트북 4), 계약 파일 줄도 옛 `122cfce2…`, Ch 18 06·`workflow_tools.py` 줄은 지금과 같음 · `notebook-executions.json`·`notebook-readiness.json`·`figure-consistency.json`(각 4) · `visual-results.json`(10) · `lesson-scope.json`·`final-formatting.json`·`prose-repetition-initial.json` · `language/ch21-ch29-final.*`·`language/baseline/ch29-agent-evaluation/` · Part 7 `existing-artifacts-before.json` · `_notebook/checks/notebook-contracts-part6-ch29-agent-evaluation.json` | — |

- **옛 생성기·옛 보조 스크립트**:

| 파일 | 무엇을 씀 | 비고 |
|---|---|---|
| **`textbook/part6/_author_ch21_ch29.py`**(569줄, **`650f6506…`**, 공용) | 569행 `write_chapter(29, …)`가 **Ch 29 `chapter.json`(목표 둘)·노트북 넷(출력 없이, `SOURCES_ONLY` 없으면)·`_src` 넷을 덮어씀** | 551행 `if chapter == 21:` Ch 21 쪽만 건너뜀 — **Ch 29 쪽 동작은 살아 있음**. 게다가 지금 원고보다 옛 글(03 결과 「judge False」, 04 「518.3·1.885·2.037·544」, 「코드 읽기와 비교 경계」 없음). 부르는 스크립트 0(`grep` — 기록 문서·`before-manifest.json`뿐). 규격 §8대로 01절에서 첫머리 `raise SystemExit(...)` → 마감에서 `mv -n` → `ch29-…/qa/upgrade/before/generators/blocked/`(Ch 21 요약·계약 §5·체크리스트가 「Ch 29 작업 뒤 이동」으로 약속) |
| `figures/_gen_figures.py`(`65b435f8…`) | `NN-흐름.{svg,excalidraw,caption.md}` 12개(`textbook/part5/_figure.py`) | 사본 `before/generators/`·`before/figures/` |
| `$CH/qa/author_*.py` | **없음** | — |
| `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part6b_enrich.py`(`8528cb33…`)·`part6b_review_fixes.py`(`a0299166…`) | Ch 25~29 `_src`·노트북 마크다운에 단락을 끼움(Ch 29 넷 포함) | 옛 계획 폴더의 보조 스크립트, 부르는 곳 0. 지금 돌리면 개선한 Ch 25~28에도 씀 — 실행 금지(기록만, 매니페스트에 해시) |

## 5. 앞뒤 챕터 이음새

### 5-1. Ch 28 인계(요약 §16·§17, 계약 §3 Ch28 줄) 항목별 지금 상태

| 인계 항목 | 지금 Ch 29 원고·설치판 | 상태 |
|---|---|---|
| 06 b8 「Ch 29 01절은 평가 방법 세 가지를 견줍니다」(+ 01 슬러그 링크, `_src` 40행·HTML 594행) | 01 b2 세 방법(영어 이름) | 참 — **01 슬러그 유지**, 01이 세 방법을 견주는 장면을 남길 것 |
| 06 b8 「Ch 29에서는 에이전트를 평가하는 방법을 배웁니다」(HTML 577행) | 챕터 전체 | 참 |
| Ch 29 01 b3은 Ch 11·21만 전제 | 「Ch11 평가셋과 Ch21 에이전트를 사용합니다」 | **고칠 자리** — 01이 실제로 쓰는 것(코드로 만든 궤적, Ch 17 04 「단계 차례」, Ch 19 04 한 단계 선택)으로 |
| 말: 도구 명세·입력/출력 토큰·요청 수 셈(「요청 수 = 도구를 요청한 응답 수 + 1」)·호출 한도(Ch 22 04 — invoke마다) | Ch 29 원고에 없음 | 실제 에이전트를 돌리면(§8 M2) 호출 한도·요청 수 셈을 이어 씀 |
| ① Ch 28 산출 파일 없음 | Ch 29 코드가 Ch 28 파일을 읽는 곳 0(`grep` — `Ch 28`·`MCP` 0건) | 어긋남 없음 |
| ② `connect_tools.py`는 Ch 28에만 | 잠금에 `fastmcp` 없음 → 가져오면 멈춤 | 가져오지 말 것 |
| ③ MCP는 `MCPAdapter`만, 넘어간 것은 도구뿐 | Ch 29에 MCP 0 | 해당 없음 |
| ④ 에이전트 실행은 도구 한 번·요청 2번짜리뿐 | Ch 29도 실제 에이전트 실행 0 | 여러 도구·여러 번 부르는 실행을 전제하지 말 것(에이전트를 새로 돌리면 그 절이 처음) |
| ⑤ 입력 토큰 값은 그날·그 판의 값 | 해당 없음 | — |
| ⑥ 평가·궤적은 Ch 28에서 다루지 않음(「궤적」은 Ch 28 금지어) | Ch 29가 처음 | 「궤적」을 어떻게 부를지 결정(§9-2) |
| ⑦ 접근 토큰 · ⑧ Deep Agents 권한 규칙 | 해당 없음 | — |
| ⑨ 말(「프로토콜」·「스키마」·「반환」·「측정」 본문 0 등) | 「반환」·「측정」 01~04 · 「프롬프트」·「루브릭」 03 · 「지연」 01·03·04 등(§1) | **고칠 자리**(§9-2) |

### 5-2. 앞 챕터에서 가르친 것 (Ch 29가 전제할 수 있는 것)

| 챕터·절 | 가르친 것 | Ch 29와의 관계 |
|---|---|---|
| Ch 11 01~05 | 평가셋·정답 문서 ID·지표 함수(재현율·정밀도·nDCG) | 01 b3 말(평가셋) — 지금 01은 쓰지 않음 |
| Ch 15 01~04·06·07 | 평가 모델(judge)·판정 머리글·판정 요청 글·치우침·차례 바꾸기 검사·제시 라벨·일치율 · 백분위수·가장 가까운 자리 방식(`nearest_rank`, 06 노트북) · 회귀·기준선·통과 조건 | 03 judge의 선례 · 04 95 백분위수 · Ch 33 회귀(뒤) |
| Ch 17 04 | 「단계 차례(궤적, trajectory)」·자율성의 대가 | 01·02의 말 — **Ch 17 04가 「Ch 29 02절」을 가리킴** |
| Ch 18 06 | 같은 조건 비교·품질 칸(코드 검사) | 04 계약 |
| Ch 19 03·04·05 | 도구 명세·`bind_tools`·`tool_calls`·`tool_call_names`(응답 하나의 도구 이름 목록)·`sum_usage` | 01 한 단계 평가 · 요청 셈 |
| Ch 20 01 | 손으로 만든 `AIMessage(tool_calls=…)` + `ToolMessage` | 01~03 코드로 만든 궤적의 선례(Ch 20은 `ToolNode` 입력으로) |
| Ch 21 01·06 | `create_agent`(모델 객체) · 고정 흐름/에이전트 흐름·비교 기록·판정 여섯 모두 1(「판정으로 두 흐름을 가를 수 없다」) | 04 계약 · 실제 에이전트를 돌리면 01 모양 |
| Ch 22 04 | `ModelCallLimitMiddleware(run_limit=N, exit_behavior="end")` | 에이전트를 돌리면 안전 규칙 |
| Ch 26~28 | 요청 수 셈 · 도구 명세 몫 | judge 요청 셈과 나란히 |

### 5-3. 완료 챕터가 Ch 29에 기대는 문장 — 개선 뒤에도 참이어야 함

| 자리 | 문장 | 조건 |
|---|---|---|
| **Ch 28 06 `_src` b8 40행 · HTML 577·594행 · `author_06.py`** | 「Ch 29에서는 에이전트를 평가하는 방법을 배웁니다」 · 「Ch 29 01절은 평가 방법 세 가지를 견줍니다」 + **01 슬러그 링크** | 01 슬러그 유지 · 01이 세 방법을 견줌 |
| **Ch 21 06 `_src` 8행(b2 링크) · HTML 146·438·683~757행 · 노트북 셀 여럿 · README 55행** | 「Ch 29 04절이 다시 읽습니다」(**04 슬러그 링크**) · 「Ch 29 04절은 이 흐름의 invoke 한 번에 걸린 초를 칸 하나로 읽습니다」 · 「줄 수와 도구 호출 수를 assert로 확인」 · 「12~18번 셀이 이 절의 비교 기록 파일을 읽고」 · 「`model_calls`라는 이름으로 읽으므로」 | **04 슬러그 유지** · 04가 계약 파일의 줄 수·`tool_calls ≥ 1`·칸 이름 `model_calls`·걸린 초 칸을 계속 읽음. 「12~18번 셀」은 셀 번호 — 04 노트북을 다시 쓰면 번호가 바뀌어 **Ch 21 06 b7 문장이 옛 번호가 됨**(인계 기록 후보) |
| **Ch 18 06 `_src` b7 · HTML 632행 · 노트북 셀 · README 45행** | 「이 절의 표는 Ch 29 04절이 저장된 출력에서 읽습니다」 · 「06절 노트북을 다시 실행해 저장하면 … Ch 29 04절이 셈하는 평균도 바뀝니다」 | 04가 Ch 18 06 **저장 출력**을 계속 읽음(파일이 아니라 출력이라는 모양 유지 — 바꾸면 Ch 18 문장이 틀림) |
| **Ch 17 04 `_src`·HTML(두 곳)** | 「에이전트의 단계 차례를 맞춰 보며 평가하는 방법은 Ch 29 02절에서 다룹니다」 | 02가 차례 맞추기를 다룸(링크 없음) |
| Part 6 `_src/index.html` 7행 · `practice-start.md` · `continuity-guide.md` 15행 | 「Ch 18의 워크플로우 실행 기록은 Ch 29의 평가에 사용합니다」 · 「Ch15의 평가 항목과 Ch18의 실행 기록 \| Ch29 답변·선택·궤적 평가 \| 최종 프로젝트의 평가 설계」 | 참(04가 Ch 18 기록을 읽는 한). continuity 셋째 칸 「최종 프로젝트의 평가 설계」는 마감 때 대조(보호 파일, 묶음에 들어감) |

### 5-4. 뒤 챕터(대기)·Part 7이 Ch 29에 기대는 것 — 고치지 않음

- **코드·노트북이 Ch 29 노트북·출력·파일을 읽는 곳: 0**(`grep` — Ch 30·31·34 0건). Ch 33만 **옛 해시를 출처로 적은 자료 파일**(§4 표) — 확인 코드 없음. → **산출 파일 계약 없음.**
- 문장: Ch 33 02 `_src` 「Ch15의 Groundedness와 Ch29의 궤적 기준을 … 적용」·「Ch29에서 최종 답뿐 아니라 도구 호출 궤적을 확인했습니다」·「Ch29의 궤적 효율」(참 — 01·02가 남는 한) · Ch 33 04 「Ch29에서 운영 지표를 정의했고 Ch34에서 p95 계산을 더 자세히 다룹니다」(04 「운영 지표」 말이 남아야 참) · **Ch 30 03 「실제 모델 품질은 Ch29 평가셋으로 확인」·09 「Ch29 평가셋으로 도구 선택과 최종 답을 반복 평가」**(Ch 29에는 평가셋이 없음 — 느슨함, Ch 30 몫 인계) · Ch 30 `_src/_generate.py` 같은 문장.
- `textbook/_notebook/build_index.py` 62~63행 · Part 6 `_build_index.py` 27행 · `chapter.json` `objectives` 둘(「코드와 궤적」·「같은 평가셋과 명시적 기준」 — 「명시적」·「평가셋」) — 마감 때 새 본문과 대조.

### 5-5. Part 6 묶음·목록·기록·검사

- Part 6 선행 목록 13줄 가운데 Ch 29 몫 셋(§3-1) · `existing-artifact-hashes.json` Ch 29 줄 0(Ch 18 06 줄 셋) · `final-artifact-hashes.json` 30줄(12줄 옛 해시, 기록만).
- 공개 목록 두 곳 + zip(§4). **묶음 실행 검사 계약 없음**(Ch 29는 목록 밖). 모델 없는 절(01·02·04)을 목록에 넣을지는 전체 마감 후보 — **04는 지금 묶음에서 멈추므로 고친 뒤에야 후보**.
- 도구 파일·05 실습 절이 생기면 두 목록·zip을 함께(Ch 28 마감 모양 — `python3 textbook/part6/_build_index.py`를 마지막에 한 번 → `check_bundle_execution.py`로 Ch 24 01·Ch 28 01이 여전히 PASS인지).
- 옛 검사 스크립트(기록만): 넷 모두 Ch 29에 닿기 전에 멈춤(Ch 28 마감 기록). 실습 절을 붙이면 `check_scope.py` `SECTION_COUNTS` 4 ≠ 5.

## 6. 설치판 동작 — 소스와 모델 없는 확인 (2026-09-29, `agentevals 0.0.9`·`openevals 0.2.0`·`langsmith 0.12.4`·`langchain 1.4.0`·`langchain-core 1.6.2`·`langchain-openai 1.6.0`)

### 6-1. 궤적 매칭 네 모드 — 결정적 (`e1_modes.py`, 다섯 번 같음)

기준 궤적 = 질문 → `search_rules({"topic":"대출"})` → 결과 → `check_source({"doc_id":"R-14"})` → 결과 → 답 「일반 도서는 14일입니다.」

| 실제 궤적 | strict | unordered | subset | superset |
|---|---|---|---|---|
| 같음 | True | True | True | True |
| 차례 뒤집음(check → search) | False | True | True | True |
| 짧음(search만) | False | False | True | False |
| 덤(search, check, `audit_log`) | False | False | False | True |
| 낭비(search 셋 + check) | False | False | False | True |
| 다른 도구 둘(check, `audit_log`) | False | False | False | False |
| 인자만 다름(`{"topic":"대출 기간"}`) | False | False | False | False |
| **답만 틀림(도구 같고 답 「7일」)** | **True** | **True** | **True** | **True** |
| 한 응답에 도구 요청 둘 | False | True | True | True |

- 인자만 다른 궤적 + `tool_args_match_mode`: `exact` False · **`ignore` True** · `subset` False · `superset` False · `tool_args_match_overrides={"search_rules": "ignore"}` True.
- **소스 사실**(설치판 `agentevals/trajectory/`): strict(`strict.py` 20~75행)는 메시지 수·차례·역할과 도구 요청(이름 + 인자 비교기)을 보고 **메시지 내용(답 글)은 보지 않음**(LangSmith trajectory-evals 문서도 「allows for differences in message content」) · unordered = 두 방향 superset(`unordered.py`) · subset·superset = 기준 도구 요청마다 실제 요청 하나씩 짝(이름 같고 인자 비교기 참, **한 번 쓴 실제 요청은 다시 못 씀 → 횟수도 셈**, `utils.py` 90~134행) · 인자 비교기: `exact`(딕셔너리 같음)·`ignore`(늘 참)·`subset`(실제 인자가 기준 인자 안)·`superset`(기준 인자를 실제가 다 가짐), 덮어쓰기는 모드 글·함수·키 목록(`utils.py` 137~212행) · 모드 이름이 틀리면 `ValueError`.
- 결과: `{'key': 'trajectory_<mode>_match', 'score': bool, 'comment': None, 'metadata': None}`. 입력은 LangChain 메시지 목록·OpenAI 모양 딕셔너리 목록·`{"messages": …}` 모두 됨.
- 평가 함수는 langsmith `@traceable`로 감싸져 있음(openevals `utils.py` 203행) — 환경 변수 `LANGSMITH_TRACING`이 없으면 기록을 보내지 않음. 루트 `.env` 키 이름은 `OPENAI_API_KEY` 하나(값은 보지 않음).
- 비동기 판 `create_async_trajectory_match_evaluator`·`create_async_trajectory_llm_as_judge`도 있음(이번 챕터에 필요 없음).
- **02의 결정적 값 후보**: 위 표 전부. 01의 「답만 틀림」 장면도 같은 함수로.

### 6-2. LLM judge (`e2_judge.py`·`e3_struct.py`, 요청 0)
- `create_trajectory_llm_as_judge(*, prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE, model=None, feedback_key="trajectory_accuracy", judge=None, continuous=False, choices=None, use_reasoning=True, few_shot_examples=None)`. 머리글 둘: 기준을 넣는 판(기준 네 줄 — 단계 사이 논리·진행·상대적 효율·기준과 뜻이 같음)과 기준 없는 판(셋째 줄까지 + 「첫 메시지로 목표를 짐작」).
- `model="openai:…"` 글이면 설치판이 `init_chat_model(model=model)`만(온도·추론 설정 없음) · **`judge=` 모델 객체**면 그 객체를 그대로 씀 → `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")` 객체를 넘기면 규격 §3 모양. 모델 객체의 `with_structured_output(형식)`은 이 판에서 **`json_schema`**(요청 형식 `response_format`, 도구 요청 아님) — 평가 한 번에 요청 1번.
- 출력 형식(`openevals/llm.py` 70~117행): `reasoning`(글, 「Thus, the score should be: …」로 끝내라는 설명) + `score`(기본 참·거짓 / `continuous` 0~1 / `choices` 고른 값) → 결과 `{'key', 'score', 'comment'=reasoning, 'metadata'}`.
- 공식 문서(2026-09-29): `model="openai:o3-mini"` 예 · 결과 딕셔너리 `score` 참·거짓·`comment` — 설치판과 맞음. openevals에는 최종 답용 머리글도 있음(`CORRECTNESS_PROMPT`·`TOOL_SELECTION_PROMPT`·`TASK_COMPLETION_PROMPT` 등) — 01 최종 답 평가를 라이브러리로 보일 때 후보(모델 요청).

### 6-3. 공식 문서와 원고의 차이
- 원고 b10 참고 자료 둘(`…/langchain/test/evals` · `…/langsmith/trajectory-evals`, 확인 2026-09-11)은 지금도 열림. 세 방법 정의는 `…/langsmith/evaluation-approaches`에 있음(원고 b10에 없음 — `qa/research.md`에만).
- `langchain/test/evals` 문서는 네 모드와 인자 비교 설정·judge만 다루고 「최종 답·한 단계」 구분은 LangSmith 쪽 문서.
- `agentevals` 새 판 없음(0.0.9가 최신).

## 7. §2-7 판단 근거 — 도구 파일

### 사실
- 지금 되풀이: **`trace()` 정의가 01·02·03에 세 번**(같은 본문) · 도구 이름 목록 뽑기(01 c8·02 c6 — 내포식) · `.env` 찾기 셀 네 번.
- 개선하면 절 사이에 되풀이될 후보: **궤적 만들기**(01·02·03·05) · **궤적의 도구 이름 목록**(01·02·04·05) · **네 모드를 한 번에 돌려 점수 모으기**(02·03·05) · judge 한 번 부르고 점수·설명 꺼내기(03·05) · 04 Ch 18 표 줄 읽기·Ch 21 기록 읽기·공통 칸 만들기.
- **앞 챕터에서 가르친 함수**: Ch 15 06 `nearest_rank(values, percent)`(노트북 셀 — Ch 15 도구 파일에 없음, 04가 다시 적는 중) · Ch 15 06 `average(values)`(Ch 15 `rag_tools.py`, `json`·`math`) · Ch 19 04 `tool_call_names(response)`(응답 **하나**의 이름 — 궤적 전체와 다름) · Ch 19 05 `sum_usage(messages)` · Ch 6 06 `estimate_cost`(에이전트·judge 요청 비용을 셀 때) · Ch 15 02 `build_judge_prompt`·`judge_once`(Ch 15 판정 모양 — 라이브러리 judge와 다름). 모두 Ch 21 `runner_tools.py`에도 있으나 그 파일은 `numpy`로 멈춤 → 파일째 가져오지 말고 함수만 같은 본문으로 옮김(`# Ch N MM절에서 배웠습니다`).
- **이름 겹침 주의**: `tool_names`는 이미 두 모양(Ch 17 `agent_tools.py` = 단계 딕셔너리 목록 · Ch 27 `harness_tools.py` = 에이전트 그래프의 도구 이름). 궤적용 새 함수는 다른 이름(예: `called_tool_names`·`trajectory_names`).
- 과정의 도구 파일 이름(`find labs -name '*_tools.py'` + `guardrails.py`): `git_tools`·`data_tools`·`llm_tools`·`rag_tools`·`guardrails`·`agent_tools`·`workflow_tools`·`order_tools`·`graph_tools`·`runner_tools`·`checkpoint_tools`·`approval_tools`·`stream_tools`·`delegation_tools`·`harness_tools`·`connect_tools`. **안 겹치는 후보**: `eval_tools.py`(짧음, 파이썬 내장 `eval`과 글자가 닮음) · `evaluation_tools.py`(뜻이 분명, 길다) · `grading_tools.py`(「채점」 — 판정·점수와 이어짐) · `trajectory_tools.py`(「궤적」 말 결정과 얽힘).
- 교훈(Ch 24 A-10·Ch 25~28 첫 판부터): 앞 절 생성기가 뒤 절이 함수를 더한 도구 파일을 덮어쓰지 않게 `strip_later_imports`·판마다 해시 대조·쓰기 가드 · 머리 설명 첫 줄 「앞 챕터와 이 챕터에서 배운 평범한 함수」.

### 선택지 (결정하지 않음 — 장단점만)

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| A. 도구 파일 없음 | 절마다 노트북에 | 목록·zip 변경 없음 | 궤적 만들기를 세 절에 되풀이, 04가 Ch 15 06 `nearest_rank`를 다시 적음(§2-7 3번 충돌) |
| B. 앞 챕터 함수만 | Ch 15 06 `nearest_rank`·`average`(+ 요청을 세면 Ch 19 `sum_usage`·Ch 6 `estimate_cost`) — 본문 그대로, 가져오기 `math`만 | §2-7 3번을 지킴 · 파일이 작음 | 01~03 되풀이(궤적 만들기)는 남음 |
| C. B + 이 챕터 함수 | 01에서 가르친 궤적 만들기·도구 이름 목록 + 02 네 모드 한 번에 + (03 judge 한 번) | 02~05 코드가 가장 짧음 | 처음 가르친 절은 노트북에 남아 판이 둘 · `agentevals`를 가져오는 도구 파일이면 가져오는 모든 절 설치 셀에 `agentevals` 필요(규격 §2-7 6번 — 지금 네 절 모두 설치하므로 문제 적음) |

## 8. 모델·비용 선택지와 흔들림 처리 (결정하지 않음 — 장단점만)

### 8-1. 모델 없이 결정적으로 보일 수 있는 것
- 01: 세 방법(최종 답 글 비교·첫 도구 이름·도구 이름 차례)과 낭비 궤적·답만 틀린 궤적 — §6-1.
- 02: 네 모드 표 전부 + 인자 비교 방식.
- 03: judge에 들어가는 요청 글 모양(`_format_inputs` — 태그 모양 글)·결과 딕셔너리의 칸 이름·strict 점수. judge **점수 자체는 모델이 있어야** 보임.
- 04: 두 계약 파일 읽기·공통 칸·평균·95 백분위수·Ch 21 기록을 궤적으로 바꾼 네 모드 비교(인자 `ignore`) — 모두 결정적.
- 모델이 있어야 보이는 것: judge 점수·설명(03 핵심), 실제 에이전트가 만든 궤적(평가 대상 실행 — 지금 챕터 전체 0), 한 단계 평가의 실제 도구 선택.

| 선택 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **M1 지금 모양 유지** | 01·02·04 모델 0, 03만 judge 요청(평가 대상 궤적은 코드로 만듦) | 결정적 값이 거의 전부 · 요청 최소 · 키 셀은 03만 | 「에이전트 평가」인데 평가받는 에이전트 실행이 챕터에 없음(Ch 21 기록만 읽음) |
| **M2 03 뒤 절반에 실제 에이전트 한 번** | 03 앞 절반 judge(코드로 만든 궤적 둘~셋), 뒤 절반 `create_agent`(도구 둘, 호출 한도 — Ch 21 01·Ch 22 04 모양)로 궤적을 만들어 네 모드·judge로 평가 | 실제 궤적을 평가하는 장면이 생김 · Ch 26~28 요청 셈을 이어 씀 | 모델이 고른 도구 차례가 흔들릴 수 있음(노트북 밖 5번 필요) · 셀·요청 늘어남 |
| **M2′ 01에 한 단계 평가만 실제 모델** | 01 뒤 절반 Ch 19 04 모양 `bind_tools` → 첫 응답의 도구 이름(요청 한두 번) | 「한 단계 평가」가 실제 선택을 봄 · Ch 19 04 선례(45/45 같음) | 01이 키 셀을 갖게 됨(지금 01은 묶음 실행 검사 후보가 될 수 있는 절) |
| **M3 모든 절 실제 에이전트** | 01~03 모두 실제 궤적 | 문서 예와 가까움 | 흔들림 최대 · 결정적 매칭 장면이 모델 판단에 기대게 됨 |
| (금지) 04에서 앞 챕터 다시 돌리기 | — | — | 계약 파일·저장 출력 해시가 바뀜(두 챕터 「다시 실행 금지」) |

### 8-2. judge 점수 흔들림 처리 (규격 §2-7 9번 끝·10번 끝)
- **옛 기록이 이미 흔들림을 보임**: 같은 입력(실제 = 기준 궤적)에 저장 노트북 `True`, 옛 검증 기록 `False`. 새로 고르는 대조 궤적(답만 틀림·인자만 다름·낭비 등)에서 judge 점수가 흔들릴 가능성이 있음.
- 절차: `03-probe.md` §0에 판단 규칙·그림 라벨 규칙을 **첫 요청 전에** 적음 → 노트북에 넣을 궤적마다 **노트북 밖 같은 요청 5번** → 새 커널 두 번. 결론·그림·정리·복습에는 **결정적 값(네 모드 점수·요청 수 셈)**과 「5/5·두 커널 같음」인 judge 점수만(한정어와 함께), `comment` 글·흔들린 점수·토큰·비용은 결과 읽기 둘째 단락·b6 표·b7에만. 원래 관찰이 5번 중 일부만 나오면 입력 그대로 두고 b7 「같은 요청도 실행한 때에 따라 판정이 달라질 수 있다」 + 「…이면 …이 됩니다」 셈 한 문장(Ch 15 결정 A 선례). 원하는 점수가 나올 때까지 다시 돌리지 않음.
- **흔들림을 구조로 줄이는 방법**: judge에 `judge=` 모델 객체(온도 0·추론 none) · 점수는 참·거짓(기본) · 판정할 차이를 뚜렷하게(답이 틀린 궤적처럼 판정 기준 넷 가운데 하나만 어긋나게) · 머리글 원문을 결과 읽기에 인용하지 않고 기준 네 줄만 한국어로 풂.
- **judge와 결정적 매칭의 결론 자리**: 「차례·도구·인자」처럼 코드로 적을 수 있는 규칙은 네 모드(결정적)로 결론, judge는 「뜻」 판단의 예로만 — 지금 b4 방향과 같음.

### 8-3. 04 값(걸린 초·토큰)을 어디에 둘지
| 선택 | 장점 | 단점 |
|---|---|---|
| (가) 새 값 그대로 본문·그림에(파일 읽기는 결정적) | 결과 읽기·표·그림이 단순 | 앞 챕터가 한 번 잰 값이라 Ch 21·18을 다시 돌리면 틀림 · Ch 21 인계 「걸린 초는 흔들리는 값」과 어긋남 |
| (나) 요청 수·도구 수·줄 수·`final_score`(두 챕터가 확인한 값)만 결론·그림에, 걸린 초·토큰은 둘째 단락·표·b7에 「교재 출력에서는」 | 규격 §2-7 9번 끝·Ch 25·26 선례와 맞음 | 「운영 지표」 절에서 걸린 초가 결론에 없음 — 95 백분위수의 뜻은 셈 방법(셋이면 최댓값)으로만 |
| (다) 값 대신 부등식·자리(예: 「95 백분위수 = 가장 큰 값 = C07 줄」)만 결론에 | 앞 챕터가 바뀌어도 대체로 참 | 자리(C07)도 다시 실행하면 바뀔 수 있음 |

### 8-4. 서비스 요청·비용 어림 (요금표 2026-09-17 mini 입력 0.75·캐시 입력 0.075·출력 4.50달러/100만 토큰 — 청구 금액 아님)
- **judge 한 번**: 요청 글 약 1,000~1,500자(네~여섯 메시지 궤적 둘 + 머리글) + 출력 형식 → 입력 약 400~600토큰, 출력 `reasoning` 약 60~120토큰 → **약 0.0006~0.0010달러**. 저장 기록 셀 2.13초.
- **에이전트 실행 한 번**(M2, 도구 둘·한 번씩): 요청 2~3번 × 입력 300~700토큰 → 약 0.001달러.
- **노트북 한 번**: M1 1번 · M2 3번에서 약 6번(judge 궤적 셋 + 에이전트 한 번) · **05 실습 절** 3~5번(규격 §7-2).
- **절별 누적(새 커널 두 번 + 노트북 밖 흔들림 확인 다섯 번 + 개발 시도)**: 03(M1, 궤적 셋) ≈ 3 × 7 + 10 = 약 30요청 ≈ **0.03달러** · 03(M2) ≈ 약 50요청 ≈ 0.05달러 · 01(M2′) ≈ 약 15요청 ≈ 0.005달러 · 05 ≈ 약 40요청 ≈ 0.04달러. **절마다 1달러 안**, 챕터 전체 **약 50~120요청 · 0.05~0.12달러**. 임베딩 0. 삽화 약 10크레딧(다섯 장, 재생성 1회씩이면 최대 20).
- **실행 시간**: 01·02·04 1초 안(모델 없음), 03 judge 한 번 2초 안팎 — 셸 180초 안에 여유.

## 9. 과정 규칙과 부딪히는 것 (선택지와 장단점만)

### 9-1. 제목·슬러그
- **챕터 제목 「Agent 평가 — 답과 실행 경로를 함께 보기」**: 「경로」는 Ch 13부터 금지어(→ 차례·흐름, 파일 뜻이면 파일 위치). (가) 제목에만 남기고 강사 확인(Ch 15~28 「제목에만 남음」 선례, 변경 최소) · (나) 「답과 단계 차례를 함께 보기」/「답과 실행 흐름을 함께 보기」로 바꿈 — `chapter.json`·Part 6 목차·`textbook/index.html`·옛 기록 파일의 제목이 함께 바뀜, 슬러그(`ch29-agent-evaluation`)는 그대로.
- **03 「LLM judge로 궤적 평가」**: 「judge」는 Ch 15 제목(「평가 심화 — judge · 트레이싱 · 회귀」·「judge 프롬프트와 편향」)에 남은 선례가 있고 본문 말은 Ch 15 01 「평가 모델(judge)」. (가) 제목 그대로 + 본문 「평가 모델(judge)」 · (나) 「평가 모델로 궤적 판정」 — 03 슬러그를 링크하는 완료 챕터 파일 0(Part 6 목차만)이라 슬러그도 바꿀 수 있음(강사 확인).
- **04 「운영 지표와 Ch18 궤적 비교」**: Ch 18 기록에 도구 궤적이 없음 · 「궤적」 말 결정과 얽힘. **슬러그는 Ch 21 06 b2 링크로 고정** → 제목만 바꾸면 제목·슬러그가 어긋남. (가) 제목 그대로 + b2·b3에서 「Ch 18 기록은 요청 수·토큰·걸린 초·품질 칸이고 도구 차례는 없다」를 밝힘 · (나) 제목만 「운영 지표와 Ch 18·Ch 21 기록 비교」 등으로(슬러그 그대로).
- 01·02 제목: 금지어 없음(「궤적」 결정만). **01 슬러그는 Ch 28 06 b8 링크로 고정.**

### 9-2. 용어
- **「궤적」**: Ch 17 04가 「단계 차례(궤적, trajectory)」로 정의(Ch 17 본문은 「궤적」을 그 한 번만) · Ch 28은 주제가 아니라서 금지어로 둠 · 라이브러리 이름 `trajectory_match_mode`·`TRAJECTORY_…`·결과 키 `trajectory_strict_match`. (가) Ch 29 첫 자리에서 「Ch 17 04의 단계 차례(궤적)」를 다시 풀고 이 챕터 본문 말로 「궤적」을 씀(제목 말과 맞음, 과정 요약 §5에 새로 올릴 말) · (나) 본문은 「단계 차례」, 「궤적」은 제목·첫 풀이·코드 이름에만(Ch 17 말 그대로 — 제목 넷과 본문 말이 갈림).
- **모드 이름**(strict·unordered·subset·superset — 코드 값): 첫 자리에서 한국어 풀이 한 번씩(예: 차례까지 같음·차례 무관·기준 안에서만·기준을 모두 담음) + 본문은 코드 값을 백틱으로(「`strict` 모드는」 — 영문 시작 조사 금지 규칙). 「집합」(Ch 14 금지어) 대신 「기준 도구 요청을 모두 담음」 같은 풀이. 「포함」은 금지어 아님.
- 세 방법 이름(Final Response·Single step·Trajectory): 「최종 답 평가·한 단계 평가·단계 차례(궤적) 평가」 + 원어 한 번. 「블랙박스」 → 「속을 보지 않고」.
- 03: 「LLM-as-judge」 → 평가 모델이 판정하는 방식 · 「루브릭」 → 판정 기준(Ch 15 「판정 머리글」 안의 기준) · 「프롬프트」 → 판정 머리글(코드 이름 `TRAJECTORY_ACCURACY_PROMPT…`는 백틱) · 「피평가 에이전트」 → 평가받는 에이전트 · 「comment」 → 판정 까닭(Ch 21 06 결과 읽기 「까닭:」 줄과 같은 말).
- 04: 「nearest-rank p95」 → 가장 가까운 자리 방식의 95 백분위수(Ch 15 06 말) · 「지연」 → 걸린 초 · 「스텝」 → 단계 · 「불리언」 → 참·거짓 값 · 「열」·「필드」 → 칸 · 「Agentic RAG」 → 에이전트 흐름(Ch 21 06) · 「운영 화면」·「판정식」·「수치」 → 뺌 · 「추정」 → 어림 · 「공통 열 변환」 → 같은 칸 이름으로 옮겨 담기.
- 공통: 반환 → 내놓다 · 측정 → 재다·세다 · 검증 → 검사 · 사전 → 딕셔너리 · 옵션 → 설정·인자 · 경로 → 차례·흐름 · 보장 → 「늘 … 라고 할 수 없다」 · 재실행 → 다시 실행 · 사용자가 금지한 표현(규격 §4)·「쉽게·간단히·당연히」 금지.
- **「품질」**: Ch 18 품질 칸 = 코드 검사 · Ch 21 판정 = 평가 모델 · Ch 15 평가 넷 — 04에서 한 칸에 담을 때 세 뜻을 섞지 않음(Ch 18 인계).
- **한도 말 셋**(Ch 26 요약): 실제 에이전트를 돌리면 실행 한도·호출 한도·바퀴 한도를 섞지 않음.
- 새 말 후보(절 meta와 맞출 것): 최종 답 평가·한 단계 평가·단계 차례(궤적) 평가·기준 궤적·네 모드(풀이)·인자 비교 방식·판정 기준·판정 까닭·운영 지표·95 백분위수(이어 씀).

### 9-3. 문법·셀 모양
- `trace(*tools: str)` → `*args` 정의·타입힌트·f-string·`enumerate`·`+=` 없이: 목록을 인자로 받는 함수(`make_trace(calls, answer)` 모양 — 호출 ID는 `"c" + str(n)`), 본문 10줄 이하.
- 04 `find_project_root`·`커리큘럼_v6.html` 대신 과정 경로 셀(`candidates` + `for`·`break`, 세 자리 확인) · 내포식·제너레이터 식 16개를 `for`·`append`로 · `statistics.mean` 대신 Ch 15 `average`(도구 파일) 또는 손셈 · `nearest_rank_p95` 대신 Ch 15 06 `nearest_rank(values, percent)`(이름·인자 그대로).
- `assert`: 만든 대로 늘 참인 것(01 c10) 빼기 · judge 점수에 걸지 않음(자료형만이면 허용 — 흔들림 확인 전) · 네 모드 점수(결정적)·줄 수·`tool_calls ≥ 1`·`status`에만.
- 설치 셀 네 절 같음(`agentevals`·`langchain`·`langchain-openai`·`langgraph`·`python-dotenv`) — 01·02·04가 모델을 안 부르면 `langchain-openai`·`python-dotenv`는 필요 없음(Ch 24 01 선례처럼 키·`dotenv` 없는 절로 둘지 결정 — 묶음 실행 검사 후보와 이어짐).

## 10. 삽화 비유 계열 후보

**이미 쓴 계열**(계약 20행·과정 요약 §5·Ch 9~28 요약): Ch 3 창고 선반 · Ch 4 쟁반·카드 상자·서류철 · Ch 5 나무 쟁반·블록 · Ch 6 도서관 상담 창구·우편함·구슬·나무 레일·저울 · Ch 7·8 한 책상 색 약속 · Ch 9 두 책상·카드 상자·흰 카드 · Ch 10 도막 · Ch 11 흰 카드/색 딱지 · Ch 12 쪽지·끈·빈 쟁반·단추·연습 자물쇠 등 · Ch 13 작업대·갈림길 나무 길 · Ch 14 나무판·마개 · Ch 15 사과·저울·바구니·모래시계 · Ch 16 쪽지·도장·개찰구·체 · **Ch 17 눈 위 발자국(04 「같은 말뚝에 닿은 두 줄」 = 같은 도착점·다른 길 — Ch 29 주제와 가장 가까움, 피할 것)** · Ch 18 도자기 가마·물레 · Ch 19 식당 주문 전표와 내주는 창 · Ch 20 자료실 승강 상자 · Ch 21 세탁기 · Ch 22 공항 검사·우편 가림막·전화 연결·방문자 명부·두 겹 봉투·서류함·메모 정리 책상 · Ch 23 체스판·즉석사진 · Ch 24 도미노 줄·비워 둔 자리 · Ch 25 대나무 홈통·물방울 · Ch 26 항구 예인선·바지선 · Ch 27 온실·모종판 · Ch 28 우주 정거장 도킹 포트.

| 후보 | 그림 요소(절별) | 장점 | 겹침·위험 |
|---|---|---|---|
| **A. 오르골 종이띠(구멍 뚫린 악보 띠)** | 01 오르골 상자에서 나온 종이띠의 끝 구멍 하나만 가리키는 작은 추(최종 답) ↔ 첫 구멍만(한 단계) ↔ 띠 전체를 기준 띠와 나란히 펼침(단계 차례) · 02 기준 띠와 실제 띠 넷 — 같은 구멍 같은 차례 / 같은 구멍 뒤섞임 / 구멍이 빠진 띠 / 구멍이 더 있는 띠 · 03 돋보기 달린 검사대 위에 두 띠를 겹쳐 놓음(판정) · 04 길이가 다른 띠 여러 줄이 한 받침대에 걸림(운영 기록) | 과정에 쓰지 않은 소재 · 「끝 소리만 듣기 ↔ 곡 전체 차례」가 선명 · 구멍 모양으로 차례·빠짐·덤을 글자 없이 보임 | 구멍 줄이 숫자·글자처럼 보이지 않게 · 기계 안쪽을 그리면 복잡해짐(상자는 닫고 띠만) |
| **B. 요리 순서 카드와 완성 접시** | 01 완성 접시만 보는 쪽 ↔ 첫 재료 그릇만 ↔ 순서 카드 줄 전체 · 02 재료 그릇 줄의 차례·빠짐·덤 · 03 두 줄을 나란히 놓은 검사 쟁반 · 04 접시 여러 개와 쌓인 그릇 수 | 누구나 아는 장면 · 「결과가 같아도 과정이 다를 수 있다」 | Ch 19 식당 전표·Ch 4·5·12 쟁반과 부엌 계열이 가까움 · 음식·그릇이 많아 무관 요소가 늘기 쉬움 |
| **C. 오리엔티어링 지도와 확인 깃발 펀치 카드** | 01 결승 깃발만 ↔ 첫 확인 깃발 ↔ 카드의 펀치 자국 줄 전체 · 02 정해진 차례로 찍은 카드 / 차례 무관 카드 / 빠진 칸 / 덤 자국 · 03 카드 두 장을 겹쳐 비추는 판 · 04 카드 여러 장의 자국 수 | 네 모드와 짝이 가장 잘 맞음(차례 있는 코스·차례 없는 코스가 실제 경기 방식) | **Ch 17 눈밭·말뚝, Ch 13 갈림길 나무 길과 야외 길 소재가 겹침** · 사람·발자국 없이 그려야 함 · 펀치 자국이 Ch 16 도장과 닮을 수 있음 |
| **D. 필름 띠(연속 사진)와 마지막 컷** | 01 마지막 컷 한 장 ↔ 첫 컷 ↔ 필름 띠 전체 · 02 컷 차례가 뒤바뀐 띠 / 빠진 컷 / 덤 컷 · 03 빛 상자 위 두 띠 · 04 감긴 필름 통 여러 개 | 「마지막 장면만 ↔ 지나온 장면 전부」가 직관적 | Ch 23 즉석사진과 사진 계열이 겹침 · 컷 안 그림이 글자·화면처럼 읽힐 위험 |

- 스타일 문구는 규격 §5-4 그대로. 판정(03)은 사람 없이 돋보기·검사대로(Ch 15 저울은 피함). 크레딧: 절마다 1장(01~05) 약 10크레딧.

## 11. 위험과 깨진 것

1. **04가 학생 묶음에서 멈춤**(§2 04) — `find_project_root`가 `textbook/`을 찾고 `커리큘럼_v6.html`을 `assert`. 묶음을 풀어 확인(`None`). 교재 출력은 저장소 맨 위에서만 돌아감.
2. **계약 값 어긋남** — 04 `_src` 6·7·9·10행과 노트북 저장 출력(셀 8·10·14·16·18)이 옛 값(§3-2). 파일 해시·모양은 계약과 같고 읽기 코드 흉내 PASS.
3. **옛 생성기가 Ch 29 쪽으로 살아 있음** — `textbook/part6/_author_ch21_ch29.py`를 돌리면 Ch 29 `chapter.json`·노트북(출력 없이)·`_src`를 지금보다 옛 글로 덮어씀. `.moai/…/part6b_enrich.py`·`part6b_review_fixes.py`는 Ch 25~29를 씀. 부르는 곳은 없음.
4. **judge 흔들림** — 같은 입력에 옛 기록 `False`·저장 출력 `True`. judge에 온도·추론 설정 없음(G4가 못 봄).
5. **사실과 다른 글** — 01 b3 「Ch11 평가셋과 Ch21 에이전트」 · README 「01·02·04절은 저장된 실제 궤적」 · 04 제목 「Ch18 궤적」 · 04 b5 「invoke·관찰」 · 03 b7 「절당 1달러 미만」(옛 틀) · 04 b8 「Ch30 최종 프로젝트 평가 설계」 · `집필점검표.md` 「모든 함수에 타입 힌트」(옛 규칙).
6. **Ch 21 06 셀 번호 문장** — Ch 21 06 b7 「Ch 29 04절 노트북 12~18번 셀이 …」: 04를 다시 쓰면 셀 번호가 바뀜(Ch 21 파일은 고치지 않음 — 인계에 적을 것).
7. **모델 의존** — 03 결론이 judge 점수에 기대면 흔들림 확인 전에는 결론·그림에 못 씀. 에이전트를 새로 돌리면(M2) 도구 선택도 흔들릴 수 있음.
8. **파일 쓰기 자리** — 지금 쓰기 0. 04가 파일을 쓰지 않도록 유지(계약 파일을 다시 만들지 않음).
9. **서비스 요청·비용** — 작음(§8-4). 에이전트를 쓰면 호출 한도(Ch 22 04)를 붙이고 invoke마다 셈.
10. **긴 실행 시간** — 없음(모델 없는 절 1초 안, judge 2초 안팎).
11. **용어·제목** — 「경로」(챕터 제목)·「judge」(03 제목)·「궤적」 결정·「프롬프트」·「루브릭」·「반환」·「측정」·「지연」·「Agentic」·「열」·「집합」 등(§9).
12. **뒤 챕터 문장** — Ch 30 03·09 「Ch29 평가셋」(Ch 29에 평가셋 없음) · Ch 33 기준선 파일의 Ch 29 04 옛 해시(이미 다름, 확인 코드 없음) · Ch 33 04 「Ch29에서 운영 지표를 정의」.
13. **기기 디스크** — 루트 여유 **2.1G(작업 전후 같음)**, `/sessions` **831~832M(전후 같음)**. 가상환경 262MB는 사용자 디스크(`$ROOT/.cache/vm`, 여유 64G), 기기 `/tmp/ch29-prep` 632KB(확인 스크립트·묶음 일부 풀기). uv 캐시 `/tmp/uv-cache` 53MB(공용, 이번에 쓴 것은 `uv venv`·`pip==26.2`뿐 — 나머지는 `pip --no-cache-dir`).

## 12. 01절 작업자가 먼저 결정해야 할 것

1. **모델 결정(§8-1)** — M1(03 judge만) / M2(03 뒤 절반에 실제 에이전트) / M2′(01 한 단계 평가만 실제 모델) / M3. 결정적 값(네 모드·세 방법·04 셈)을 결론의 중심에 두고, judge 점수는 `03-probe.md` §0 규칙(첫 요청 전)과 노트북 밖 5번 뒤에만 한정어와 함께. judge는 `judge=` 모델 객체(`temperature=0`·`reasoning_effort="none"`)로.
2. **04 계약 값 처리(§3·§8-3)** — 옛 값(519.7·1.880·2.094·541 / 0.88·610.2·4.145)을 새 값(688·1.731·2.003·699 / 0.96·862.2·4.206)으로 고치되, 걸린 초·토큰을 결론·그림에 둘지((가)·(나)·(다)). 04 파일 찾기를 과정 경로 셀로 바꿔 **학생 묶음에서 돌게** 하고, 두 계약 파일은 읽기만(Ch 21 06·Ch 18 06 다시 실행 금지). 「Ch 18 궤적」·품질 칸 뜻을 b2·b3에서 바로잡기.
3. **말과 제목(§9)** — 「궤적」을 본문 말로 쓸지(Ch 17 04 「단계 차례(궤적)」과의 관계) · 챕터 제목 「실행 경로」·03 제목 「judge」·04 제목 「Ch18 궤적」을 「제목에만 남음(강사 확인)」으로 둘지 바꿀지 · 모드 이름·세 방법 이름의 한국어 풀이. **01·04 슬러그는 링크로 고정.**
4. **01~03 궤적 설계와 도구 파일(§2·§7)** — 코드로 만든 궤적의 대조 장면 고르기(답만 틀림·낭비·인자만 다름·한 응답 두 요청 — §6-1 표) · `trace` 되풀이를 도구 파일로 뺄지(A/B/C)와 이름(`eval_tools.py`·`evaluation_tools.py`·`grading_tools.py`) · Ch 15 06 `nearest_rank`·`average`를 같은 본문으로 옮길지 · 01·02·04를 키·`dotenv` 없는 절로 둘지(묶음 실행 검사 후보).
5. **옛 생성기 막기** — `textbook/part6/_author_ch21_ch29.py` 첫머리에 설명 주석 + `raise SystemExit(...)`(Ch 29 쪽까지 막힘 — Ch 21 멈춤 줄은 그대로 두고 첫머리에) · `figures/_gen_figures.py`도 같게. `.moai` 보조 스크립트 둘은 실행 금지 기록만.

## 13. 챕터 마감으로 미룰 것

- **05 실습 절 신설**(규격 §7-2): 슬러그 후보 **`05-Agent-평가-실습`**(챕터 짧은 이름 「Agent 평가」 — `_notebook/build_index.py` 62행과 같음, 선례 `06-Agent-개요-실습`·`06-MCP-실습`·`09-DeepAgents-실습`) · 다른 후보 `05-에이전트-평가-실습`(본문 말 「에이전트」와 맞춤). 제목 「Agent 평가 실습: …」, `format: experiment`, meta 「실습 30분 · 새 용어 0」(**챕터 시수 3·5h에 더하지 않음**). 새 문법·API 0, 요청 3~5번. 주제 예 — 01~04 기능(세 방법·네 모드·judge·셈)을 한 평가 표에 모으고, 실행 2는 값 하나만(예: 모드 하나·인자 비교 방식 하나·기준 궤적의 도구 하나) 바꿔 통과·실패 줄 수를 견줌.
- **공용 옛 생성기 이동**: `textbook/part6/_author_ch21_ch29.py`(`650f6506…` → 01절이 막은 뒤 새 해시) → `ch29-agent-evaluation/qa/upgrade/before/generators/blocked/`(`mv -n`, 해시 기록 — Ch 21 요약·계약 §5·체크리스트 약속) · `figures/_gen_figures.py`(`65b435f8…`)도 같은 자리로.
- 옛 그림 12개(`figures/0N-흐름.{svg,excalidraw,caption.md}`, N=1~4) 삭제 승인 목록(사본 `before/figures/`) — 챕터 공개 목록에 SVG 줄 없음.
- `chapter.json` `objectives`(「코드와 궤적」·「같은 평가셋과 명시적 기준」) · 절 제목 · `textbook/part6/_build_index.py` 27행 · `_notebook/build_index.py` 62~63행(절 수 4 그대로) · 목차를 개선 본문과 대조 → `_build.py`·`_build_index.py`.
- 실습 폴더 README 다시 쓰기(노트북 다섯, `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 절마다 요청 수·키 필요 여부, 04가 읽는 앞 챕터 파일 둘과 「다시 만들지 않음」, 예상 비용, 도구 파일 단락) · `labs/part6/continuity-guide.md` 15행 · `pyproject.toml` `pillow`(import 0 — Ch 21 B-16처럼 강사 확인) · `qa/research.md`·`technical-notes.md`·`verification.md`·`집필점검표.md`에 「개선 전 판」 표시.
- 공개 목록 두 곳에 05·(도구 파일) 줄 → `part6-practice.zip` 다시 만들기(마지막에 한 번) → `check_bundle_execution.py`(Ch 24 01·Ch 28 01 PASS 그대로인지) → `check_delivery.py`(`llm-practice.zip` Stale 예상) · 묶음을 풀어 04·05 첫 셀과 파일 찾기 셀 확인 · 옛 검사 넷 돌려 기록(`check_notebook_readiness.py` 결과 파일 되돌림).
- **뒤 챕터 인계**(고치지 않음): Ch 21 06 b7 「12~18번 셀」(04 셀 번호가 바뀌면) · Ch 30 03·09 「Ch29 평가셋」 · Ch 33 기준선 파일의 Ch 29 04 옛 해시(출처 기록) · Ch 33 02·04 문장(참인지) · 과정 요약에 Ch 29 줄(용어·도구 파일·judge 흔들림 처리) · 계약 §3의 Ch 21 06·Ch 18 06 줄에 「Ch 29가 새 값으로 고침」.
- Part 6 마지막 챕터이므로 **Part 6 마감(누적 문서 세 파일 갱신)**이 이어짐 — 오케스트레이터 몫.
- 삭제 승인 대상: 실습 폴더 `.venv`(macOS 187MB) · `qa/upgrade/gates-wip-*.json` · `.cache/vm/venv-ch29-agent-evaluation`(262MB) · 기기 `/tmp/ch29-prep`(632KB — 확인 스크립트·묶음 일부 풀기).

## 14. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 4 · `notebooks` 4 · `figures` 13(SVG·excalidraw·caption 각 4 + `_gen_figures.py`) · `generators` 2(`_author_ch21_ch29.py`·`_gen_figures.py`) · `qa` 5(`public-files.json`·`prerequisite-files.json`·`research.md`·`technical-notes.md`·`verification.md`) · `lab` 3(`README.md`·`pyproject.toml`·`uv.lock`) · **`html` 4**(빌드한 절 HTML — Ch 28은 해시만 적었으나 이번에는 사본도 둠) · `chapter.json`·`_build.py`·`index.html`·`집필점검표.md` = **39개, 549,256바이트**. 원본과 바이트 대조 모두 같음 |
| `qa/upgrade/gates-before.json` | §0 표(절별 G1~G7 · 합계 131, 통과 0/4), `fb2f153e…` |
| `qa/upgrade/before-manifest.json` | sha256 **217개**(`4aa29f63…`) — ① 이 챕터 원고·실습 폴더(`_src`·HTML·목차·`chapter.json`·`_build.py`·점검표·그림 13·`qa/` 다섯·README·잠금 둘·노트북 넷·`.venv/pyvenv.cfg`·노트북 계약 JSON) ② **이 챕터가 읽는 보호 파일**: Ch 21 계약 파일·Ch 18 06 노트북·`workflow_tools.py` + 만든 쪽(Ch 21 06 노트북·`_src`·HTML·`author_06.py`·README·잠금·`runner_tools.py`, Ch 18 06 `_src`·HTML·README, Ch 14 자료 둘) + 이어 쓸 앞 챕터(Ch 15 도구 파일·01~07 노트북·`_src`, Ch 11 평가셋, Ch 17 04·`agent_tools.py`, Ch 19 `order_tools.py`·04, Ch 20 `graph_tools.py`, Ch 22 04, Ch 26·27·28 도구 파일, Ch 28 06 노트북·`_src`·HTML·`author_05/06.py`·잠금) ③ 챕터 요약 전부 ④ Part 6 목록·목차·소개·`practice-start.md`·`qa/` 스크립트·JSON·MD 전부·`language/` 기록·`continuity-guide.md`·`build_index.py`·`build_bundle.py`·`textbook/index.html`·zip 둘 ⑤ **뒤 챕터·Part 7이 Ch 29를 가리키는 파일**(Ch 33 기준선·02 노트북·README·`evaluate_regression.py`·02·04 `_src`·HTML, Ch 30 03·09 `_src`·HTML·`_generate.py`, Part 7 기록·목록 둘) ⑥ **옛 생성기**(`_author_ch21_ch29.py`·`_figure.py`·`.moai` 보조 스크립트 둘·`part6a-author.md`) ⑦ 과정 문서·공용 도구(규격·PLAYBOOK·누적 문서 셋·게이트·`verify.py`·`execute.py`·빌더·렌더 도구 등) |
| `qa/upgrade/chapter-lead-notes.md` | 이 파일 |
| `$ROOT/.cache/vm/venv-ch29-agent-evaluation` | Python 3.12.13 · 262MB |

### 가상환경 만든 방법과 결과
- Ch 28 준비와 같은 방법: `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy uv venv --python 3.12.13 …/venv-ch29-agent-evaluation` → `uv pip install --python …/bin/python pip==26.2` → 잠금 목록 `uv export --project labs/part6/ch29-agent-evaluation --frozen --no-hashes --all-groups --no-emit-project`(실습 폴더 파일 그대로 — 수정 시각 09-10 그대로), 주석·들여 쓴 `# via` 줄을 뺀 93줄(`/tmp/ch29-prep/req-clean.txt`, 환경 표시 유지) → **`bin/python -m pip install --no-cache-dir -q -r`**(한 호출, 170초 안에 끝남). 설치 오류 0, **`uv cache prune` 안 함**.
- 크기 어림(만들기 전): Ch 28 환경 302MB에서 FastMCP 계열이 빠지고 `agentevals`·`openevals`·`pillow`가 더해져 조금 작을 것, 사용자 디스크(여유 64G)라 기기 루트(2.1G)·`/sessions`(832M)는 거의 그대로일 것 → 만듦. **전후 루트 2.1G · `/sessions` 831M.**
- 결과: `pip freeze --all`과 잠금 대조 **판 차이 0**(설치 88 = 잠금 93 − 이 기기에 해당하지 않는 다섯: `appnope`(darwin)·`colorama`(win32)·`cffi`·`pycparser`(pypy)·`httpx2-jsfetch`(emscripten)). `agentevals 0.0.9`·`openevals 0.2.0`·`langsmith 0.12.4`·`langchain 1.4.0`·`langchain-core 1.6.2`·`langchain-openai 1.6.0`·`langgraph 1.2.11`·`openai 3.11.0`·`pydantic 2.13.5`·`pillow 12.3.0`·`python-dotenv 1.2.3`·`ipykernel 7.3.0`·`nbclient 0.11.0`·`pip 26.2`. `pip check` 이상 없음. 커널 스펙 `share/jupyter/kernels/python3` 있음. `run_section.sh`는 `$ROOT/.cache/vm/venv-<챕터 폴더 이름>`을 자동으로 씀.
- import 확인(`env -u OPENAI_API_KEY`): `langchain.messages`·`langchain.agents.create_agent`·`langchain.chat_models.init_chat_model` · `agentevals.trajectory.match`(`create_trajectory_match_evaluator`)·`agentevals.trajectory.llm`(`create_trajectory_llm_as_judge`·머리글 둘·`_format_inputs`) · `openevals.llm`(`create_llm_as_judge`)·`openevals.prompts`·`openevals.exact` · `dotenv`·`langgraph`·`langchain_openai` 모두 됨. **`numpy`·`pandas` 없음.** judge 평가 함수는 가짜 키 모델 객체로 만들기만(요청 0).

### 참고 자료 (2026-09-29 확인)
- LangSmith Evaluation approaches `https://docs.langchain.com/langsmith/evaluation-approaches` — Final response(「Evaluate the agent's final response」, 속을 보지 않음·느리고 원인 찾기 어려움) · Single step(「Evaluate any agent step in isolation (e.g., whether it selects the appropriate tool)」) · Trajectory(「Evaluate whether the agent took the expected path (e.g., of tool calls) to arrive at the final answer」).
- LangChain Agent evals `https://docs.langchain.com/oss/python/langchain/test/evals` — 네 모드 정의(Strict 「Exact match of message structure and tool calls in the same order」 · Unordered · Subset 「Agent calls only tools from reference (no extras)」 · Superset 「at least the reference tools (extras allowed)」) · `tool_args_match_mode`·`tool_args_match_overrides` · `create_trajectory_llm_as_judge(model=…, prompt=TRAJECTORY_ACCURACY_PROMPT…)` · 결과 `key`·`score`(참·거짓)·`comment` · 비동기 판 · `pip install -U agentevals`.
- LangSmith Trajectory evals `https://docs.langchain.com/langsmith/trajectory-evals` — strict는 「allows for differences in message content」 · 「By default, only tool calls with the same arguments to the same tool are considered equal」.
- PyPI agentevals `https://pypi.org/project/agentevals/` — 최신 0.0.9(2025-07-24) · 인자 비교 `exact`·`ignore`·`subset`·`superset`.
- 설치판 소스: `agentevals/trajectory/match.py` 24~109(만들기 함수·모드·인자 비교 방식 검사) · `strict.py` 20~75 · `unordered.py` 21~33 · `subset.py`·`superset.py` 16~31 · `utils.py` 22~65(메시지 모양 맞추기)·90~134(짝짓기)·137~212(인자 비교기·덮어쓰기) · `trajectory/llm.py` 27~71(머리글 둘)·77~95(`_format_inputs`)·98~150(judge 만들기) · `openevals/llm.py` 70~117(출력 형식)·145~295(모델 객체·문자열·OpenAI 클라이언트 갈래, 254행 `init_chat_model(model=model)`) · `openevals/utils.py` 176~234(`@traceable`)·427~454(메시지 → 태그 글) · `langchain_openai` `with_structured_output` → `json_schema`(`e3_struct.py`).
- 모델 없는 확인 파일(기기 `/tmp/ch29-prep/exp/`): `e1_modes.py`(네 모드 표·인자 비교·다섯 번 같음) · `e2_judge.py`(judge 인자·요청 글 모양·openevals 머리글 목록) · `e3_struct.py`(출력 형식 요청 모양) · `e4_ch21.py`(Ch 21 기록을 궤적으로 바꿔 네 모드). AST·금지어 세기 `ast_scan.py`·`ban.py`, 매니페스트 `manifest.py`, 묶음 일부 풀기 `/tmp/ch29-prep/bundle/`.
