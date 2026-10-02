# Ch 18 워크플로우 5패턴: 맨손 구현 — 챕터 준비 조사 (01절 작업자용)

- 대상: `textbook/part5/ch18-workflow-patterns`(절 여섯 — 01·02 paired, 03~06 experiment) · `labs/part5/ch18-workflow-patterns`. Part 5의 둘째 챕터이고 **Ch 17 바로 뒤**입니다.
- 준비 산출물: `qa/upgrade/before/`(원본 사본) · `gates-before.json` · `before-manifest.json` · 이 파일 · 가상환경 `$ROOT/.cache/vm/venv-ch18-workflow-patterns`.
- 읽은 것: 규격 `QUALITY-UPGRADE.md`(§2·§2-7·§3·§5-3·§5-4·§6·§7-2·§8) · `AGENT-BRIEF.md` · `PLAYBOOK.md` · `qa/upgrade-course-summary.md` · `qa/upgrade-contracts.md`(§1·§3 Ch17 줄·§4·§5·§8) · Ch 17 `chapter-summary.md` · Ch 17 `chapter-lead-notes.md`·`before-manifest.json`·`gates-before.json`(모양) · 커리큘럼 v6의 Ch 18·Ch 39 설명 · Ch 2 12절 `_src`·노트북.
- **원고·노트북·그림은 하나도 고치지 않았습니다.** 파일 삭제 0건. 모델 호출 0건. 노트북 실행 0건. 모델을 부르지 않는 확인만 했습니다(`test_verify.py`의 Ch 18 두 시험 통과 · Ch 29 04의 읽기 코드를 지금 06 노트북에 그대로 돌려 봄 · 06 `grade()`를 05 최종 초안에 대 봄).
- `chapter.json` `hours` = 「총 16h · 강의 4h · 실습 12h」. 절 meta 합은 강의 0.7×5 + 0.5 = **4h**, 실습 1.5+1.5+2+2.5+2+2.5 = **12h** → 규격 §7-2 「절 meta 시수 합」을 지금 만족합니다. `textbook/part5/_build_index.py`(4, 12)·`qa/check_scope.py` `EXPECTED`(4, 12)도 같습니다. 새 용어 meta 5·5·6·6·6·6 = 34.

## 0. 게이트 기준선 (`gates-before.json`, 2026-09-23)

| 절 | 형식 | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 게이트가 있는 프롬프트 체이닝 | paired | 8 | 95 | 4 | 1 | 0 | 0 | 7 | 22 | 3 | 37 |
| 02 실패를 처리하는 라우팅 | paired | 8 | 91 | 4 | 1 | 0 | 0 | 7 | 18 | 3 | 33 |
| 03 병렬 섹셔닝과 투표 | experiment | 8 | 95 | 11 | 10 | 0 | 0 | 7 | 18 | 3 | 49 |
| 04 동적 오케스트레이터와 워커 | experiment | 8 | 100 | 6 | 3 | 0 | 0 | 7 | 10 | 3 | 29 |
| 05 생성자 평가자와 정지 조건 | experiment | 8 | 99 | 4 | 4 | 0 | 0 | 6 | 10 | 3 | 27 |
| 06 같은 과제로 다섯 패턴 비교 | experiment | 11 | 99 | 17 | 14 | 0 | 0 | 10 | 14 | 3 | 58 |
| **합계** | | **51** | **579** | **46** | **33** | **0** | **0** | **44** | **92** | **18** | **233** |

- 통과 절 **0/6**. 코드 줄(`count_code.py`) 85·85·100·83·86·144 = **583줄**, 그중 **절마다 같은 준비·도움 셀 다섯 개가 54줄씩 = 324줄(56%)**.
- G1 46 = 제너레이터 식 23 · 한 셀에 함수 둘 7 · 조건 표현식 8 · 리스트 내포식 8.
- G2 33 = 두 겹 이상 호출 8 · 한 글자 이름 12(`r` 10 · `v` 1 · `x` 1) · 15줄 초과 5(03 cell13 19·cell15 23 · 05 cell15 20 · 06 cell13 16·cell23 18) · 세미콜론 8(05 `…; break` 둘 · 06 `start = len(calls); began = …` 등 여섯).
- G3 0 = 첫 줄 주석은 셀마다 구체적입니다(Ch 17의 틀 문장 착시와 다름). 다만 **2~3줄마다 이유 주석(§2-5)은 거의 없습니다**(06 cell23 18줄에 주석 한 줄).
- **G4 0은 착시입니다.** G4는 `init_chat_model(`만 봅니다. 이 챕터는 `client.responses.create(…)`를 쓰고 **`temperature`를 한 번도 주지 않습니다**(기본값). `reasoning={"effort": "none"}`은 모든 요청에 있습니다. 가짜 모델은 없습니다.
- G5 44 = 절마다 `title_cell_missing`·`core_figure_attachment_missing` + 결과 읽기 인용 없음 32.
- G6 92 = 70자 초과 19 · 영문으로 시작해 조사가 붙은 문장 **70** · 빽빽한 단락 3.
- G7 18 = 절마다 Mermaid 0 · 삽화 0 · 설계표 없음.

### G1이 잡지 않은 금지·미교육 문법 (AST로 따로 셈)

- **타입힌트**: 함수 32개 모두 인자·반환(`dict`·`tuple[bool, list[str]]`·`tuple[str | None, str]`·`dict[str, int]`), 변수 주석(`calls: list[dict[str, float | int | str]] = []` 여섯 노트북 · 05 `history: list[dict]`·`previous_score: int | None` · 06 `results: dict[str, dict]`). Ch 13~17은 0건입니다.
- **기본값 매개변수**: `call_json(…, limit: int = 240)`·`call_answer(…, limit: int = 400)` 여섯 노트북.
- **비동기**: `async def` 03 넷·04 셋·06 둘, **셀 맨 위 `await`** 03 3곳·04 3곳·06 11곳, `AsyncOpenAI`(03·04·06).
- **별표 풀기**: `asyncio.gather(*(…생성기…))`(03 ×2·04), `gather(*[…내포식…])`(03), `write_section(*item)`(03), `gather(*section_jobs)`·`gather(*worker_jobs)`(06), `{**checks, "score": …}`(06). 과정 요약 §2-1·마감 파일 35행이 **「Ch18 03 `gather(*jobs)` 첫 사용 때 한 문장」**을 이미 걸어 두었습니다.
- **f-string**: 여섯 노트북 모두(과정은 Ch 13~17 0건), 그 안 계산 03 `candidates[0]['answer']`·04 `item['instruction']`·06 `item['instruction']`, **딕셔너리·목록을 통째로 넣어 모델에 보냄**(01 `{outline}` · 04 `{worker_results}` · 06 `{outline}`·`{worker_outputs}` — 모델이 받는 글은 JSON이 아니라 파이썬 표기).
- **집합**: 01 `required - data.keys()`(집합 빼기) · 02 `ALLOWED = {…}` · 03 `{"A", "B"}` · 05 `assert … in {…}` · 06 `{"security", "hr", "finance"}`.
- **처음 쓰면 풀어야 하는 이름**: `Counter`·`most_common`(03) · `re.search(…, re.S)`(06 — Ch 16은 `findall`·`sub`만, 플래그 없음) · `enumerate`·`max`·`all`·`bool()`·`list()`(06) · `sum`·`isinstance`(전부) · `sorted`(01) · `dict()`(03) · `float()`(02·06) · 이어진 비교 `0 <= value <= 100`·`120 <= len(answer) <= 180` · 숫자 `1_000_000` · 요금 0.75·4.50을 식 안에 바로(§2-3) · 튜플 반환·풀기(01·02·06) · `is None`(02·05).
- **try 0건**: 모델 글 `json.loads` 실패·API 오류(시간 제한 45초·`max_retries=0`)가 나면 셀이 멈춥니다. 도움 함수 안 `raise ValueError` 넷 + 03 `write_section`·04 계획 검사.
- **쓰지 않는 import**(ruff F401, `textbook/part5/qa/ch18-lint-findings.json`): `Path`(01·02·05) · `re`(03·04) · `Counter`(04).
- **한 셀에 함수 정의와 호출**(규격 §2-2): 01 cell13 · 02 cell13·17 · 03 cell13·15 · 04 cell15. 06 cell13은 함수 둘(`grade`·`answer_of`)을 한 셀에 둠.

## 1. 절별 현황 표

| 절 | 지금 가르치는 것(요지) | 모델 요청(이번 출력 / 상한) | 손 값·가짜 기록 | 금지 문법(셀) | 금지어(`_src` 블록 / 노트북) | `assert`(무엇에 걸렸나) |
|---|---|---|---|---|---|---|
| 01 | 기획 JSON(`title`·`audience`·`steps`) → 안내문, 두 요청 사이에 코드 게이트 `outline_gate`(세 키 + `steps` 목록 3개 이상). 기본 실행은 손 예시로 `(True, [])` · Before는 모델에 title만 요청 → `{'title': '비밀번호 재설정 안내'}` → 부족 `['audience', 'steps', 'steps(3개 이상)']`·`다음 호출 수: 0` · After는 세 칸 요청 → 통과 → 4문장 안내문 | **3 / 3**(동기 `OpenAI`) | 완전한 예시 `sample`, 요금 0.75·4.50 | cell11 제너레이터 둘·함수 둘 · cell13 집합 빼기·`sorted`·`isinstance`·튜플 반환 · cell15 조건 표현식 `0 if not passed else 1` · cell17 f-string에 딕셔너리 통째로 · 타입힌트·기본값 | **제목 「프롬프트」**·「체이닝」 · 프롬프트 b2×2·b4·b5·b6×3 / md 2 · 반환 b3·b4×2·b5×2·b7 / md 5 · 사전 b4×2·b5·b6 / md 5 · 경로 b8 · 검증 b9 · 직렬화 b4 · 「추정 비용」 b5·b7·출력 · md 「계획 비용」 | 4 — 키 있음 · 손 예시 `(True, [])` · **Before 게이트 실패(모델 출력)** · **After 통과·답이 비지 않음(모델 출력)** |
| 02 | 분류 요청(`category`·`confidence` JSON) → `route()`가 허용 목록 `ALLOWED`(billing·account·technical)와 신뢰도 0.75를 검사 → 전문 머리글로 답하거나 `needs_clarification` 되묻기. 단일 의도 `billing 0.98` → 결제 답 · 혼합 `unknown 0.93` → 되묻기 | **3 / 4** | `ALLOWED`·0.75·`prompts` 세 역할·되묻기 문장 | cell13 상수+함수+호출 한 셀(14줄)·`float(….get(…, 0))`·`str \| None` · cell15 **조건 표현식으로 「KeyError 위험」 글만 찍음** · cell17 f-string·`is None` | 프롬프트 b1·b2 / md 1 · **경로 b1·b2·b4×3·b5×2·b7·b8·b9×2 / md 2·출력 「전문 경로 사용」** · 반환 b2×3·b4×4·b5·b6 / md 6 · 범주 b2×2·b3·b4×7·b5·b6·b9 / md 5 · 사전 b3·b4×2·b6·b9 / md 6 · 폴백 b4×2·b9 · 거부 b3·b9 · 분기 b4 / 제목 셀 · 임계 b7 · 측정 b7 | 1 — 키만 |
| 03 | `AsyncOpenAI` + `asyncio.gather`로 (가) 섹셔닝: 공통 사실 하나를 목적·절차·지원 세 요청으로 함께 → 입력 순서 `['목적', '절차', '지원']`, 벽시계 2.283초 · 개별 지연 합 5.644초 (나) 투표: 후보 A·B를 함께 만든 뒤 평가자 셋(인사·보안·신입 직원) → 원표 A·B·A, 유효표 A 2·B 1, 결과 A, 제외 0. `tie`·`refuse`·`undecided` 규칙은 코드에만(실행에서 안 나옴) | **8 / 8** | `brief`·세 부분·문체 둘·평가자 셋 | cell13 **19줄**·정의+호출·`*` 풀기·생성기·내포식·f-string·`r` · cell15 **23줄**·내포식 셋·`Counter`·f-string 계산·`v` · cell17 생성기 둘·`r` | **제목 「병렬」(Ch 13 금지어)·「섹셔닝」** · 병렬 b4×3·b5×2·b8 / md 5·출력 「병렬 벽시계 시간(초)」 · 반환 b4×3·b5×2·b6×2·b9 / md 5·출력 「입력 순서대로 반환」 · 분기 b3 · 프롬프트 b6 · 측정 b8×2 · awaitable·코루틴 b3·b4 | 1 — 키만 |
| 04 | 오케스트레이터 요청이 `tasks` 2~4개(`id`·`instruction`) → 코드가 딕셔너리·값 있는 항목만 앞 네 개 → 2개 미만이면 `raise` → 작업 수만큼 워커 `gather` → 종합 요청. 이번 작업 3 → 요청 5 = 1 + 3 + 1 | **5 / 6** | **`print("고정 목록 사용:", False)` — 계산이 아니라 손으로 적은 값** · 과제 글 | cell13 내포식·`isinstance`·`raise` · cell15 `async def`+호출 한 셀·f-string 계산·`*` 풀기 · cell17 f-string에 목록 통째로 | **제목 「오케스트레이터」·「워커」** · 병렬 b1·b3·b4×2·b9×2 · 분기 b2 · **b3 「얼마나」·「자율성」(Ch 17 어긋남)** · 검증 b4·b6 · 사전 b4 / md 4 · 반환 b5 / md 3 · 코루틴 b1·b4 | 2 — 키 · `assert final_answer`(모델 출력이 비지 않음) + 계획 2개 미만이면 `raise`(모델 출력에 달림) |
| 05 | 생성자(answer 스키마)·평가자(`score`·`feedback`)를 `for iteration in range(1, 4)`로 번갈아. 정지 조건 셋 — 품질 85 이상 · 개선 폭 3 미만 · 최대 3번. 이번 실행: **첫 바퀴 100점 → `quality_threshold`**, 기록 한 줄 | **2 / 6** | 85·3·3, 과제 글 | cell13 딕셔너리를 통째로 `print` · cell15 **20줄**·세미콜론 둘 `…; break`·조건 표현식 `None if … else …`·`int \| None`·f-string | 임계 b1·b4·b5·b6·b8 / md 1·출력 「품질 임계」 · 프롬프트 b1·b6·b9 · 호출 상한 b3 · 게이트 b4 · 검증 b4 · 경로 b6×2·b8 · 하한 b4·b9 · 반환 b4·b5×2 · 「얼마나」 b6 | 3 — 키 · 기록 줄 수 ≤ 3 · `stop_reason` ∈ 셋(구조 값 — 규격에 맞음) |
| 06 | 같은 과제 `TASK`(120~180자·날짜·전 직원·help@company.test·1)2)3))와 코드 채점 `grade()` 다섯 항목(각 1점)으로 다섯 패턴을 셀 안에서 **짧게 다시 적어** 실행 → `pattern \| calls \| tokens \| latency_s \| quality/5 \| status` 표. 이번 출력 chaining 2·428·3.513·5 / routing 2·270·2.33·4 / parallel 4·884·7.008·4 / orchestrator_worker 4·1049·5.11·5 / generator_evaluator 2·420·2.765·4 → 최고 품질 동점 둘, 예상 비용 0.006563 | **14 / 18** | 과제·채점 기준·분류 셋(security·hr·finance) | G1 17·G2 14 · `**` 풀기 · `re.S` · `enumerate`·`max`·`all` · cell23 18줄(`results`의 `from` 자리로 구간 셈) | 벽시계·지연 여러 곳 · 라우팅·병렬·오케스트레이터·워커·체이닝(영어 패턴 이름이 출력에 — **Ch 29 04가 읽음**) · 반환 b4×2 / md 4 · 측정 b4·b8·b9×2 · 경로·캐시·범주 b7 · 사전 b9 / md 3 · **「패턴 선택표」**(b4·md, 과정이 없앤 말) | 2 — 키 · `all(answer_of(item) …)`(모델 출력이 비지 않음) |

- **모델 요청 합계(노트북 한 번씩, 교재 출력 기준) 3 + 3 + 8 + 5 + 2 + 14 = 35번**(상한 3·4·8·6·6·18 = 45), 모두 `gpt-5.4-mini` Responses API, 임베딩 0. 예상 비용 출력 합 0.001007 + 0.000603 + 0.003395 + 0.002071 + 0.000916 + 0.006563 ≈ **0.0146달러**(할인 없는 요금표 어림, 청구 금액 아님).
- **걸린 시간**: 도움 함수가 요청마다 `time.perf_counter()`로 `latency_s`를 적지만 **출력하는 곳은 03(벽시계·개별 합)과 06(패턴별 걸린 초)뿐**. 03·06은 시간이 주제인 절이라 Ch 15 05·06·Ch 17 04처럼 「재지 않는다」 규칙의 예외 후보입니다(커리큘럼 v6이 「호출 수·토큰·지연·품질을 표로」를 요구). 01·02·04·05는 재기만 하고 보이지 않습니다.
- **비용**: 여섯 절 모두 `cost_usd(calls)` = 입력·출력 토큰 합 × 0.75·4.50(식 안 숫자)로 「사용량 기준 추정 비용($)」을 출력. 과정 말은 **「예상 비용」(Ch 6 06 = 사용량 × 요금표)**, 캐시 입력은 할인하지 않음(Ch 6 06 `estimate_cost`는 캐시 입력을 따로 셈).
- **준비 셀**: 여섯 노트북이 같은 모양 — `%pip install -q openai==2.29.0 python-dotenv==1.2.3` → import·키 `assert`·클라이언트(`OpenAI`/`AsyncOpenAI(timeout=45.0, max_retries=0)`)·`calls` → `call_json`(`text={"format": {"type": "json_object"}}`) → `call_answer`(`json_schema` strict, `answer` 한 칸) → `cost_usd`·`score_of`. `score_of`는 05·06만, `call_answer`는 02에서 안 씀. **모델 준비 셀 결과 읽기의 실행일 문장·temperature 없음.**
- **옛 그림 토큰**: 절마다 b4 「도식 읽기」의 `{{svg:0N-흐름}}` 하나. 노트북 토큰은 01·02 `{{notebook:slug|example}}`+`|failure}}`, 03~06 `{{notebook:slug}}`(`chapter.json` 형식과 같음). Mermaid·삽화 0장.
- 노트북 `metadata.verification`: 여섯 모두 `passed`, 실행일 01·02·04·06 **2026-09-10**, 03·05 **2026-09-14**(다시 실행). `code_sha256` 앞 12자 01 `42b63166aef9` · 02 `7eaa373566c8` · 03 `f27213b03702` · 04 `49a1b53ecb87` · 05 `b3b85654deba` · 06 `d2d502a83a79`.
- 노트북 설명 셀: 「실행 환경과 비용 상한」·「코드를 읽기 전에」(`_src` b4와 같은 글, `revision: 2026-09-14-first-use-depth`)·「다음 셀을 읽는 방법」 넷(`2026-09-14-direct-cell-reading`, 도움 셀 설명)·소제목·「다른 상황에 적용하기」. 결과 읽기 셀 0.
- 복습 문제 01~05 넷·06 다섯(`check_delivery.py` 3~5 안). 해설 끝이 「오답 시 다시 볼 곳: 핵심 개념과 실행 결과」 틀. b10 참고 자료 넷(OpenAI SDK 저장소·LICENSE·모델 페이지·Anthropic 글, 확인일 2026-09-10).

## 2. 절별로 더 봐야 할 것

### 01 게이트가 있는 프롬프트 체이닝 (paired)
- **Before가 결함 코드가 아닙니다.** Before도 After와 같은 게이트 코드이고, 다른 것은 요청 글(「title만」)입니다. b6가 말하는 「잘못된 방식」(빠진 키가 있어도 글로 바꿔 다음 요청에 넣기)은 **실행하지 않습니다**. paired 절의 Before로는 「게이트 없이 이어 부르면 빠진 칸이 있는 기획으로 둘째 요청이 나간다」를 실제로 보여야 합니다(규격 §3 「실패 장면은 실제로 일어나는 조건으로」).
- Before·After 결과가 모델 출력에 달린 `assert` 둘(cell15·17). 「title만」 요청에 모델이 칸을 더 붙이면 Before `assert`가 멈춥니다.
- b3 「Ch 4에서 … Ch 16에서 호출 전에 입력과 비용을 검사」 — Ch 16 말은 입력 검사·호출 한도·비용 상한·부르기 전 예약. **Ch 17을 되짚지 않습니다**(Ch 17 요약 §13 「이어받을 것」: 워크플로우·결정 주체·라우팅 = 워크플로우). 「LangChain이나 LangGraph는 사용하지 않습니다」 — Ch 6~17이 `init_chat_model`로 불렀으므로 **왜 SDK를 직접 쓰는지 한 문장**(커리큘럼 v6: 「사용 라이브러리는 openai 뿐」, `verify.py` 108~122행이 Ch 18 노트북의 `langchain`·`langgraph` import를 막음)이 필요합니다.
- 새 API가 한꺼번에 나옵니다: `OpenAI(timeout=, max_retries=)` · `client.responses.create(model=, instructions=, input=, max_output_tokens=, reasoning=, text=)` · `response.output_text` · `response.usage.input_tokens`·`output_tokens` · `text={"format": {"type": "json_object"}}` · `json_schema` + `strict`. 과정에서 이 SDK 모양은 처음입니다(Ch 6은 LangChain). `instructions` = Ch 17 「머리글」, `input` = 「요청 글」로 이으면 「프롬프트」를 피할 수 있습니다.

### 02 실패를 처리하는 라우팅 (paired)
- **Before가 실패를 흉내 냅니다**: `print("Before 결과:", "KeyError 위험" if bad_key not in prompts else prompts[bad_key])` — 실제 `KeyError`는 나지 않습니다. `try`/`except KeyError as error`(L3, 과정 관례 「그 오류 이름만 받아 셀은 끝까지」)로 진짜 오류를 받거나, 받지 않은 채 멈추는 장면을 보여야 합니다.
- **핵심 관찰이 모델 답에 달림**: 혼합 질문 「로그인도 안 되고 카드 청구도 이상해요」가 `unknown`으로 와야 되묻기 갈래가 보입니다. 모델이 `billing`·`account`를 높은 신뢰도로 내면 이 절의 After가 보여 줄 장면이 사라집니다 → **흔들림 먼저 확인 대상**. 신뢰도는 모델이 스스로 적은 값입니다(b7이 밝힘).
- `float(decision.get("confidence", 0))` — 숫자가 아닌 글이면 `ValueError`로 멈춥니다. 전문 답은 `call_json`(스키마 없음)으로 받습니다.
- Ch 17 01(개선 뒤)이 「라우팅(routing) = 모델이 쓴 종류 이름을 보고 코드가 준비한 갈래 가운데 하나로 가는 모양 · **이 규칙으로는 워크플로우** · Ch 18 02절에서 직접 만듭니다」라고 약속했습니다. 02는 이 정의를 그대로 이어받아야 합니다. Ch 17의 라우팅은 `if` 둘뿐이고 **실제 모델로 종류를 가른 적은 없습니다**(Ch 17 요약 §13).

### 03 병렬 섹셔닝과 투표 (experiment)
- **병렬 실행 수단**: `AsyncOpenAI` + `async def` 도움 함수 + **셀 맨 위 `await`**(IPython의 자동 await) + `asyncio.gather(*(…))`. 스레드·`asyncio.run`·LangChain `batch`/`RunnableParallel`은 쓰지 않습니다.
- **과정이 가르친 것(Ch 2 12, 개선 완료)**: `async def`·`await`·셀 맨 위 `await`(「노트북 도구의 기능」이라고 설명)·`asyncio.gather(a, b)`(**변수 둘을 직접 넣음 — 별표 풀기 없음**)·반환 목록은 넣은 순서·`time.perf_counter()`로 걸린 초 · `asyncio.to_thread()`로 동기 함수를 함께 기다리기 · 파일에서는 `asyncio.run(main())`. **안 가르친 것**: `AsyncOpenAI`, `gather(*목록)`, 생성기·내포식, `Counter`·`most_common`.
- **Ch 2 12 b8의 약속(완료 챕터)**: 「Ch 18 3절은 모델 호출 세 개를 `asyncio.gather()`로 함께 기다리고, 반환 목록이 입력 순서라고 적습니다.」 → 섹셔닝 세 요청과 「입력 순서」 문장은 남겨야 합니다.
- 「벽시계 2.283초 < 개별 지연 합 5.644초」는 한 번 잰 값입니다(b6이 일반화하지 않는다고 밝힘). `qa/verification.md`(2026-09-10)는 4.619·9.263초, 원표 **A·A·B** — 지금 노트북(09-14 재실행)은 **A·B·A**. **표는 이미 한 번 바뀌었습니다**(결과는 둘 다 A).
- 투표의 `tie`·`refuse`·`undecided` 갈래는 한 번도 실행되지 않았습니다(b6이 「작성했습니다」로 밝힘).
- 제목·본문의 「병렬」은 **Ch 13 금지어**(Ch 13은 팬아웃·`Send`로 말함), 「섹셔닝」은 영어 음역. 뒤 챕터(Ch 19 05 「병렬 호출」·Ch 20 「병렬 실행」·Ch 23)는 「병렬」을 그대로 씁니다.

### 04 동적 오케스트레이터와 워커 (experiment)
- **Ch 17 요약이 짚은 문장(그대로 있음)**: b3 「Ch 17에서는 모델이 흐름을 **얼마나** 결정하는지 자율성의 기준으로 살펴봤습니다. 이 절은 그 경계를 코드에서 확인합니다.」 → Ch 17은 **누가 다음 단계를 골랐는지(모델이 고른 단계가 있는지)**만 봤습니다. 「얼마나」는 전제하지 마세요.
- **Ch 17 01 규칙과의 긴장**: 커리큘럼 v6은 04를 「여기서 처음으로 모델이 흐름의 일부를 정합니다」로 소개합니다. Ch 17 01 규칙(기록에 모델이 고른 단계가 있으면 「에이전트 후보」)을 그대로 대면 오케스트레이터가 작업 목록을 정하는 흐름이 에이전트 후보로 읽힐 수 있습니다. Anthropic 글은 오케스트레이터-워커를 워크플로우로 둡니다. 「다음 단계의 차례(계획 → 워커들 → 종합)는 코드가 정하고, 워커 수와 맡을 일은 모델이 정한다」처럼 **어느 칸을 누가 정하는지** 한 번에 풀어야 Ch 17과 부딪히지 않습니다.
- `print("고정 목록 사용:", False)`는 계산값이 아니라 **손으로 적은 `False`**입니다.
- **종합 답에 과제에 없는 연락처를 모델이 지어냄**: 「IT헬프데스크(내선 1234, it-support@company.com)」. 과제 글에는 문의처가 없습니다. b6이 「지정하지 않은 문의처가 들어갈 수 있다」로 일반론만 적었습니다.
- 작업 수(이번 3)는 입력마다·실행마다 2~4로 흔들릴 수 있고, 2개 미만이면 `raise`로 셀이 멈춥니다 → **흔들림 확인 대상**. ID 중복·40자 제한은 검사하지 않습니다(b4가 밝힘).

### 05 생성자 평가자와 정지 조건 (experiment)
- **루프가 한 바퀴만 돕니다**: 첫 평가 100점 → `quality_threshold`. 개선 폭·최대 반복 갈래는 실행되지 않았습니다(b6이 밝힘). 이 절의 학습 질문(「품질이 충분하거나 개선이 멈췄을 때 어떻게 끝내는가」)의 절반이 출력에 없습니다.
- **평가자가 조건을 어긴 초안에 100점**: 최종 초안이 **117자**로 과제 「120~180자」를 어겼습니다. 06의 코드 채점 `grade()`에 그대로 대면 `length 0` → **4/5**입니다(모델 요청 없이 이번에 확인). 본문·노트북 어디에도 이 사실이 없습니다. 「모델 평가자 ≠ 코드 검사」를 보여 줄 수 있는 실제 장면이고, 입력을 고치는 근거(규격 §2-7 10번)도 됩니다.
- 이전 실행(`qa/verification.md`·`집필점검표.md`, 2026-09-10)은 96점 — 지금 노트북(09-14)은 100점. 점수는 흔들리지만 정지 이유는 두 번 모두 같았습니다.
- 준비물 md 「마지막 보고 1회 이하」 — 코드에 보고 요청이 없습니다.
- **Ch 17 이음새**: Ch 17 03이 「정지 조건」·「바퀴 한도」(바퀴 수 상한, `turn_limit`)·「정지 조건 넷」을 가르쳤습니다. 05의 `MAX_ITERATIONS`는 바퀴 한도와 같은 일을 하고, 품질 기준·개선 폭은 **모델이 낸 점수를 코드가 비교**하는 정지입니다. b3은 Ch 17을 부르지 않고 「Ch 16에서는 호출 상한」(→ 호출 한도)·**「Ch 39에서 … 다시 사용」(교재에 없는 챕터 — Part 8 미집필)**을 적었습니다.

### 06 같은 과제로 다섯 패턴 비교 (experiment)
- **01~05 코드를 다시 쓰지 않고 셀 안에서 짧게 새로 적습니다**: 체이닝에 게이트가 없고, 라우팅 종류가 02(billing·account·technical)와 달리 security·hr·finance, 오케스트레이터는 작업 2개 고정(04는 2~4), 생성자-평가자는 `range(2)`(05는 3번)·개선 폭 없음. b4 「다섯 함수는 …」이라 적었지만 **코드에 함수가 없습니다.** 「같은 과제로 다섯 패턴 비교」의 공정성 주장이 약합니다.
- **Ch 29 04가 이 노트북의 출력을 읽습니다**(§4-1 계약). 표 모양·영어 패턴 이름·`status`가 `ok`인지가 뒤 챕터 코드에 걸려 있습니다.
- 품질 4점인 패턴이 어느 항목을 놓쳤는지 출력하지 않습니다(b6이 「단정하지 않는다」로 밝힘) → 항목별 출력을 더하면 05와 같은 「길이」 탈락이 보일 가능성이 큽니다.
- 품질 점수·최고 품질 목록·라우팅 종류·작업 수·걸린 초가 모두 실행마다 흔들립니다 → **흔들림 확인 대상 1순위**. 라우팅이 세 종류 밖을 내면 `status`가 `invalid_category`가 아니라 **`no_answer`**가 되어 Ch 29 04 `assert all(status == "ok")`가 멈춥니다.
- b3 「Ch 15에서 배운 것처럼 채점 기준은 출력을 본 뒤 정하지 않고 호출 전에 공개」 — Ch 15(07 기준선·통과 조건) 또는 Ch 5 08(「측정 전에 기준을 정한다」) 가운데 어디인지 확인하지 않았습니다(**확인 필요**).
- 「패턴 선택표」(b4·md) — 과정이 없앤 말(「선택표」, Ch 6 01 고칠 것 목록).

## 3. 실습 폴더 구조와 읽는 곳

```
labs/part5/ch18-workflow-patterns/
  README.md (3줄 — `textbook/…/qa/research.md` 비용 상한을 보라고 적음: 학생 묶음에 없는 파일)
  pyproject.toml   uv.lock
  author_notebooks.py   (35KB 옛 생성기 — 노트북 여섯을 출력 없이 덮어씀)
  notebooks/01~06-*.ipynb
  __pycache__/author_notebooks.cpython-312.pyc · .ruff_cache/ · .venv/ (macOS 판, 2026-09-10)
  (없음: data/ · runs/ · tests/ · 모듈 · 도구 파일)
```

- **코드로 읽는 파일**: 노트북은 루트 `.env`(`load_dotenv(find_dotenv(usecwd=True))`)만 읽습니다. 자료·기록 파일 읽기·쓰기 0건.
- **옛 생성기 셋**(부르는 곳 0 — `qa/public-files.json` 제외 목록 글에만 이름이 나옴):

| 파일 | 무엇을 씀 | 비고 |
|---|---|---|
| `textbook/part5/ch18-workflow-patterns/_author.py`(39KB) | `chapter.json`(제목·hours·objectives) + `_src/*.html` 여섯 | 실행하면 개선한 `_src`를 옛 판으로 덮어씀 |
| `labs/part5/ch18-workflow-patterns/author_notebooks.py`(35KB) | `notebooks/*.ipynb` 여섯(출력 없이) | 〃 노트북 |
| `textbook/part5/ch18-workflow-patterns/figures/_gen_figures.py` | `0N-흐름.{svg,excalidraw,caption.md}` 18개(`textbook/part5/_figure.py` 사용) | 〃 옛 그림 |
| (챕터 밖) `.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part5_enrich.py`·`part5_review_repairs.py` | 「코드를 읽기 전에」·「다음 셀을 읽는 방법」 블록을 끼워 넣은 옛 도구 | 기록만(Ch 16·17 선례대로 막지 않음) |

→ 규격 §8 1번: **01절 작업 때 앞의 셋 첫머리에 설명 주석 + `raise SystemExit(...)`**, 마감 때 `mv -n` → `qa/upgrade/before/generators/blocked/`(사본은 이미 `before/generators/`).

- **판**: `requires-python = ">=3.12,<3.13"`, **`dependencies = ["openai==2.29.0", "python-dotenv==1.2.3"]`**, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`, `[tool.uv] package = false`. `uv.lock` 60항목.
- **Ch 17과 견줌**: dev 그룹·Python·공통 의존(httpx 0.28.1·pydantic 2.13.5·python-dotenv 1.2.3·ipykernel 7.3.0·pip 26.2)은 **같습니다**. 다른 것은 **`openai` 2.29.0(Ch 18) ↔ 3.11.0(Ch 17·19·20 잠금, LangChain이 끌어옴)** 하나와 Ch 18에만 있는 `tqdm`. Ch 18에는 `langchain`·`langchain-openai`가 없습니다(의도 — `verify.py` 규칙). 계약 파일 §3 「Ch18 잠금은 `openai==2.29.0`」과 맞습니다.
- `%pip` 셀(여섯 노트북 cell3) = `openai==2.29.0 python-dotenv==1.2.3` — 잠금과 같음. dev `pip==26.2` 있음.
- 실습 폴더 `.venv`: **macOS 판**(`home = /Users/mhso/.local/share/uv/python/cpython-3.12-macos-aarch64-none/bin`, uv 0.11.6) → 기기 VM에서 쓸 수 없음, 삭제 승인 대상(Ch 16·17과 같음).

## 4. 이음새 — 앞뒤 챕터와 검사 스크립트

### 4-1. Ch 18 파일을 **코드로** 읽는 곳

| 읽는 곳 | 무엇을 | 계약(바꾸면 깨짐) |
|---|---|---|
| **`labs/part6/ch29-agent-evaluation/notebooks/04-운영-지표와-Ch18-궤적-비교.ipynb`** cell 8·10·16(Ch 29 **대기**, 고치지 않음) | Ch 18 **06 노트북의 저장된 stream 출력**을 저장소 경로로 읽음 | ① 모든 stream 출력에서 `" \| "`가 든 줄 가운데 `pattern`으로 시작하지 않는 줄을 모아 **마지막 다섯 줄**을 씀(지금 여섯 줄 — 첫 줄은 준비 셀 `모델: gpt-5.4-mini \| API 키 존재: 예`) ② 줄마다 `\|`로 나눠 **정확히 여섯 칸** `pattern, calls, tokens, latency, quality, status` ③ `int(calls)`·`int(tokens)`·`float(latency)`·`int(quality) / 5` ④ `assert len(table_lines) >= 5` · **`assert all(status == "ok")`** ⑤ 이름은 `Ch18:{pattern}`으로 씀. **표 뒤에 `" \| "`가 든 줄을 하나라도 더 찍으면, 또는 칸 수·자료형·`ok`가 바뀌면 멈춥니다.** 지금 판으로 돌려 보면 통과(평균 품질 0.88 · 요청 2.8 · 토큰 610.2 · 걸린 초 4.145) |
| `textbook/part6/ch29-agent-evaluation/_src/04-운영-지표와-Ch18-궤적-비교.html` | 위 평균 넷을 b6·b8·(노트북) **세 번씩** 인용(`0.88`·`2.8회`·`610.2`·`4.145`) | 06을 다시 실행하면 값이 바뀝니다 → Ch 29가 대기이므로 **고치지 않고 챕터 요약 「뒤 챕터 인계」에 파일·행·현재 값·새 값**(규격 §7-2) |
| `textbook/part6/prerequisite-files.json` 6행 · `textbook/part6/ch29-agent-evaluation/qa/prerequisite-files.json` 2행 | 06 노트북을 **`part6-practice.zip`에 함께 넣음**(`textbook/part6/_build_index.py` 67행) | 06을 바꾸면 마감 때 `part6-practice.zip`도 다시 만들어야 함(Ch 16 선례) |
| `textbook/_notebook/verify.py` 105~122행 · `tests/test_verify.py` 49~64행 | Ch 18 노트북만 `openai` import 허용, **`langchain`·`langgraph` import는 `AssertionError`**. 모든 노트북에서 모듈 이름 `rag`·`context_lab`·`document_processing`·`experiment`·`harness`·`prompts` import 금지 | 도구 파일 이름을 **`prompts.py`·`experiment.py` 등으로 지으면 verify가 멈춤**. 이번에 두 시험 통과 확인 |
| `textbook/_notebook/build_bundle.py` 21행 · `build_index.py` 40행(절 수 **6**) · `textbook/part5/_build_index.py` 21행(4·12·설명 「호출 수·사용량·지연·품질을 비교」) | 묶음·목차 | 실습 절(07)을 붙이면 절 수·설명 대조 |
| `textbook/part5/qa/check_scope.py`(`EXPECTED` (4, 12) · **`SECTION_COUNTS` Ch 18 = 6**) · `check_notebook_readiness.py`(Part 5 노트북 21개·**함수 타입힌트 필수**·노트북마다 `assert`) · `check_figures.py`(SVG마다 `.excalidraw`) · `check_delivery.py`(챕터 4·복습 3~5) · `finalize_evidence.py`(`language/ch18-final.json` 해시 — **이미 Ch 18 `_src/01`에서 멈춤**, Ch 17 요약) | 옛 검사 넷 | Ch 17과 같이 **고치지 않고 기록**. 실습 절 meta 「실습 30분」은 `Missing scope` |
| 기록만(읽는 스크립트 없음) | `textbook/part6/qa/final-artifact-hashes.json` 353행·`existing-artifact-hashes.json` 124~129·407~419행 · `textbook/part7/qa/existing-artifacts-before.json` 242~268행 · `.moai/context.md` 77행 | 06 옛 해시 `7bd4a20d…` ≠ 지금 `b583e8b4…`(이미 다름) |

- `textbook/part5/qa/check_bundle_execution.py`는 Ch 17 05·Ch 19 01·Ch 20 03만 돌립니다(Ch 18 없음). `textbook/qa/check_course_continuity.py`의 노트북 목록에도 Part 5가 없습니다.

### 4-2. Ch 18이 앞 챕터 파일을 읽는가

- **0건.** 여섯 노트북 모두 `openai`·`dotenv`와 표준 라이브러리만 씁니다. Ch 17 `agent_tools.py`·자료 넷, Ch 16 `guardrails.py`를 부르지 않습니다. Ch 17 `agent_tools.py`의 모델 함수(`send_and_measure`·`choose_line`·`run_measured_loop`)는 LangChain `chat_model.invoke` 모양이라 **Ch 18이 가져올 수 없습니다**(verify 규칙).

### 4-3. 문장으로 기대는 곳 (확인한 것만)

| 자리 | 지금 문장 | Ch 18 개선 때 |
|---|---|---|
| **Ch 2 12 b8**(완료) | 「Ch 18 3절은 모델 호출 세 개를 `asyncio.gather()`로 함께 기다리고, 반환 목록이 입력 순서라고 적습니다.」 · Ch 2 index 「비동기 대기는 Ch 18의 API 호출 … 에서 다시 사용」 | 03이 지켜야 할 약속 |
| **Ch 17 01 b4·b7·b10**(완료) | 라우팅 = 모델이 쓴 종류 이름을 보고 코드가 준비한 갈래로 가는 모양, 이 규칙으로는 워크플로우, 「Ch 18 02절 — 라우팅을 직접 만드는 자리」 | 02가 이 정의로 시작 |
| **Ch 18 04 b3**(이 챕터 몫) | 「Ch 17에서는 모델이 흐름을 **얼마나** 결정하는지 자율성의 기준으로 살펴봤습니다.」 | → 「누가 다음 단계를 골랐는지(모델이 고른 단계가 있는지)」 |
| Ch 18 01·02·05 b3(이 챕터 몫) | Ch 16 옛 말(「거부」·「호출 상한」·「입력과 비용을 검사」)·「사전」·「Ch 39」 | Ch 16 말(입력 검사·허용 목록·호출 한도·부르기 전 예약)·딕셔너리, Ch 17 되짚기 더하기 |
| Ch 20 01 b3·04 b3(대기) | 「Ch18에서는 OpenAI SDK를 직접 호출하고 코드로 단계·분기·병렬 실행과 종료를 연결했습니다」 | 개선 뒤에도 참이 되게(SDK 직접 · 차례 · 갈래 · 함께 기다리기 · 멈춤) |
| Ch 34 03 b3(대기) | 「Ch 18에서는 코드가 분기를 고르는 라우팅 패턴을 구현했습니다」 | 02가 「모델이 종류를 쓰고 코드가 갈래를 고른다」로 남으면 참 |
| Ch 29 03 b8·04 b1~b9(대기) | 「저장된 Ch18 … 실행 기록」·평균 넷 | §4-1 |
| `textbook/part5/_src/index.html` 7·8행 | 「Ch 2의 함수·**타입 힌트**·비동기 실행은 Ch 18의 패턴 구현에 사용합니다」·「Ch 18은 OpenAI SDK를 직접 사용합니다. 모델이 작업 목록을 만드는 오케스트레이터도 이 챕터에서 다룹니다」 | 타입힌트를 빼면 7행이 틀림 → Part 5 마감 몫(`finalize_evidence.py` 해시 고정) |
| `labs/part5/continuity-guide.md` 5행 | 「Ch 18은 Ch 2의 함수·비동기 실행을 사용합니다. 다섯 가지 패턴으로 같은 과제의 결과를 비교하고, 동적 작업 분해와 생성·평가 반복의 정지 조건을 확인합니다. **Ch 39**에서는 이 정지 조건을 더 큰 반복 작업에 적용합니다.」 | Ch 39는 커리큘럼 v6에만 있고 교재 폴더에 없음(Part 8 미집필) |
| `textbook/part5/practice-start.md` 9·15행 | Ch 18 폴더 예시 · 「OpenAI SDK로 다섯 가지 패턴을 구현하고 같은 과제를 비교」 | 그대로 참 |
| 커리큘럼 v6 | 「사용 라이브러리는 openai 뿐 … ③ 병렬 `asyncio.gather`로 섹셔닝과 투표 — Ch 2의 async가 여기서 회수 · ④ 여기서 처음으로 모델이 흐름의 일부를 정함 · ⑤ 정지 조건 3요소(최대 반복·품질 임계·개선 폭 하한) — Ch 39 정지조건의 원형 · 실습: 호출 수·토큰·지연·품질을 표로, 「패턴이 화려할수록 좋은 게 아니다」를 수치로」 | 설계 기준 |

- Ch 19·21·22 `_src`는 Ch 18을 부르지 않습니다(0건). Ch 19 05 「병렬 호출」은 도구 호출 뜻으로 따로 씁니다.

## 5. §2-7 판단 근거 — 도구 파일

### 사실
1. **앞 챕터 함수를 다시 쓰는 곳 0.** 다만 Ch 6 06 `estimate_cost(usage, input_rate, cached_input_rate, output_rate)`(Ch 17 `agent_tools.py`에도 있음)는 딕셔너리 `usage["input_tokens"]`·`["output_tokens"]`만 있으면 SDK 응답에도 쓸 수 있습니다(캐시 키가 없으면 할인 없이 셈). 지금 `cost_usd`는 같은 일을 요금을 식 안에 박아 다시 만든 판입니다.
2. **챕터 안 되풀이가 큽니다**: 준비·도움 셀 다섯(`%pip`·import·`call_json`·`call_answer`·`cost_usd`+`score_of`)이 여섯 노트북에 **54줄씩, 합 324줄 = 코드의 56%**. 동기 판(01·02·05)과 비동기 판(03·04·06) 두 벌입니다.
3. **06이 01~05 함수를 다시 부르지 않고 짧은 새 판을 적습니다**(§2 06). 01~05 함수를 도구 파일에 두면 06은 「같은 과제에 같은 패턴 코드」를 가져와 조립만 하게 됩니다.
4. 벡터 계산이 없어 NumPy 대상은 없습니다.

### 선택지 (결정하지 않음 — 장단점만)

**A. 도구 파일을 만들지 않는다** — 장점: 묶음 목록·README·커널 시작 폴더 안내가 움직이지 않음. 단점: 준비 셀 324줄이 그대로이거나 절마다 다시 줄여 적어야 하고, 06이 01~05를 또 새로 적음. 규격 §2-7 3항(「앞 절에서 가르친 함수는 다시 적지 않는다」)과 부딪힘.

**B. `notebooks/workflow_tools.py`**(이름 후보: **`workflow_tools.py`** — 챕터 이름·과정 관례 `*_tools.py` / `pattern_tools.py` / `sdk_tools.py`. `agent_tools.py`는 Ch 17과 같은 이름·다른 내용이라 피함. `prompts.py`·`experiment.py`는 verify가 막음)
- 담을 후보: 01 요청 보내기 + JSON 읽기 + 기록 한 줄 남기기(예: `ask_json(client, records, head, request, limit)`·`ask_answer(…)` — **클라이언트와 기록 목록을 인자로**, 노트북 전역 `calls`에 기대지 않음) · Ch 6 06 `estimate_cost`(그대로 옮김) · 01 `outline_gate` · 02 `route` · 03 표 세기 · 04 작업 목록 거르기 · 05 정지 판정 · 06 `grade`. 가져가는 절 02~06(06이 가장 많이).
- 장점: 324줄 되풀이가 사라지고 06이 짧아짐. 06이 01~05와 **같은 코드**를 쓰게 되어 비교가 공정해짐. Ch 17과 같은 방식.
- 단점: 동기·비동기 두 벌이면 함수 수가 두 배(→ 아래 C의 수단 선택과 묶임). 인자가 길어짐(`client`·`records`). 묶음 목록 두 곳(`textbook/part5/public-files.json`·챕터 `qa/public-files.json`)·README·「커널이 `notebooks/`에서 시작해야」 문장. Ch 29 04는 출력만 읽으므로 영향 없음.

**C. 병렬 수단을 무엇으로 할지(B와 함께 정함)**
- (가) 지금처럼 `AsyncOpenAI` + `async def` 도움 함수 + `gather` — 커리큘럼·Part 5 소개 문장과 맞음. `AsyncOpenAI`·`gather(*목록)`이 새 이름. 도움 함수가 동기·비동기 두 벌.
- (나) **동기 `OpenAI` 도움 함수 하나 + `asyncio.to_thread(함수, …)` + `gather`** — **Ch 2 12 After가 가르친 모양 그대로**(`to_thread`로 동기 함수를 함께 기다림). 도움 함수 한 벌, `AsyncOpenAI` 불필요. 단점: 기록 목록에 여러 스레드가 `append`, 동기 클라이언트를 여러 스레드가 함께 쓰는지(SDK 설명) **확인 필요**, 「AsyncOpenAI」를 말한 README·Part 5 소개와 다름.
- (다) 스레드 풀·LangChain `batch` — 과정 미교육·verify 금지라 제외.

## 6. 삽화 비유 계열 후보

**이미 쓴 계열**(과정 요약·계약 §1·각 챕터 `figures/*.prompt.md` 이름): 카드·카드 상자·서류철·봉투·두 겹 봉투·서랍·쟁반·칸막이 쟁반·블록·끈·단추·관·깔때기·그릇(Ch 1 04 흰 그릇 넷)·빵 칼·**나무 길·갈림길·세 갈래 길·나무 레일·작업대·표지판(Ch 13)**·**나무판·마개(Ch 14)**·**바구니·사과·저울·동전·모래시계·선반·궤짝·눈금(Ch 15)**·**쪽지·도장·덮개 천·두루마리·개찰구·체·돌(Ch 16)**·**눈 위 발자국·바위·말뚝·울타리(Ch 17)**·공항 검사 지점·우편 가림막·전화 연결·교통카드 개찰구·방문자 명부·서류함·안내 데스크(Ch 22)·창고 선반·열쇠·깃발·명찰·클립보드·퍼즐 조각·돋보기. 프롬프트 파일에서 **점토·물레·가마, 화분·물뿌리개·모종, 냄비·국자·가스레인지, 종이접기, 장난감 기차 전환기는 0건**입니다.

| 후보 | 그림 요소 | 맞는 절 | 겹침 점검 |
|---|---|---|---|
| **도예(점토 덩이·물레·가마·말림판)** | 점토 → 물레 → 가마 차례, 가마 앞에서 금 간 그릇만 옆으로 빠짐 / 빚고 살피고 다시 빚은 그릇 셋이 나란히(마지막만 매끈) | 01(게이트) · 05(생성자-평가자·정지) · 06(같은 흙 다섯 덩이) | 겹침 없음. 「판」은 Ch 14 나무판과 가르려고 천 없이 둥근 받침으로 |
| **부엌 화구와 냄비(요리)** | 화구 셋 위 냄비 셋이 함께 끓음(섹셔닝) / 같은 냄비 곁 국자 셋(투표) / 간을 보고 소금을 더하는 차례(반복) | 03 · 05 | 겹침 없음(Ch 1 04 흰 그릇과 가르려고 그릇 대신 냄비·국자). 사람·손 없이 그리면 투표가 잘 안 읽힐 위험 |
| **원예(모종판·화분 셋·이름표 꽂이·물뿌리개)** | 모종마다 이름표 → 해·그늘·물가 화분 셋 가운데 하나로, 이름표 없는 모종은 따로 둔 작은 접시 / 넓은 밭을 모종 수만큼 나눈 구획 | 02(라우팅·되묻기) · 04(작업 수를 입력에 맞춰 나눔) | 겹침 없음. 「바구니」(Ch 15)는 쓰지 않음 |
| **종이접기(색종이 학·배)** | 접는 차례 넷, 모서리가 안 맞은 셋째 장에서 멈춤 / 접었다 펼친 자국이 남은 종이 | 01 · 05 | 겹침 적음(Ch 16 쪽지와 가르려고 글씨 없는 색종이). 관계가 작아 「그림만 보고 읽히는가」 위험 |
| (보조) 장난감 기차 선로 전환기 | 선로 셋 앞 전환 손잡이 | 02 | Ch 13 길·갈림길·나무 레일과 겹침 → 뒤로 |

- 한 계열로 챕터를 이을지(예: 도예 01·05·06 + 원예 02·04 + 부엌 03), 절마다 다를지는 01 작업자가 정합니다. 사람·동물·화면·글자는 넣지 않는 것이 앞 챕터 선례입니다.

## 7. 위험과 깨진 것

1. **Ch 29 04 출력 계약(§4-1)** — 06 표 모양·영어 패턴 이름·`status == "ok"`·「표 뒤에 `" | "` 줄 없음」. 06을 다시 쓰면 반드시 Ch 29 04 cell 8·10·16의 읽기 코드를 새 출력에 그대로 돌려 보고, Ch 29 `_src` 04의 평균 넷(0.88·2.8·610.2·4.145)이 바뀌는 것을 인계에 적어야 합니다. `part6-practice.zip`도 다시 만들어야 합니다.
2. **모델 답에 기대는 핵심 관찰(흔들림 먼저 확인 대상, 규격 §2-7 10번 끝)**:
   - 01 Before — 「title만」 요청에 모델이 칸을 더 붙이면 게이트가 통과해 Before `assert`가 멈춤.
   - **02 혼합 질문 → `unknown`** — 다른 종류가 오면 되묻기 장면이 사라짐(신뢰도는 모델 자기 보고).
   - **03 투표** — 원표가 이미 A·A·B(09-10) → A·B·A(09-14)로 바뀜. B나 동점이 되면 결론이 뒤집힘.
   - **04 작업 수** — 2~4로 흔들림, 2 미만이면 `raise`. 종합 답이 연락처를 지어냄.
   - **05 첫 바퀴 통과** — 96(09-10)·100(09-14) 모두 첫 바퀴 종료라 루프·개선 폭·최대 반복이 한 번도 보이지 않음. 평가자가 117자 초안(과제 위반)에 100점.
   - **06 전체** — 패턴별 품질 4·5, 최고 품질 목록, 라우팅 종류(밖이면 `no_answer` → Ch 29 멈춤), 작업 수, 걸린 초.
3. **모델 출력에 건 `assert`·`raise`**: 01 cell15·17 · 04 cell17(`assert final_answer`)·cell13(`raise`) · 06 cell17(`assert all(…)`). 규격 §3은 매번 같은 값에만 `assert`.
4. **`temperature` 없음** — 모든 요청이 기본 temperature. 규격 §3은 `temperature=0` + 추론 none. Responses API `create()`에 `temperature` 인자가 있음을 설치판 시그니처로 확인했지만(`openai 2.29.0`), `gpt-5.4-mini` + `reasoning={"effort": "none"}` + `temperature=0` 조합을 **이 SDK·이 API로 보낸 적은 없습니다**(Ch 22 시범은 LangChain `init_chat_model` 경로) → 01 첫 실행에서 확인.
5. **실패 흉내·손 값을 관찰처럼**: 02 Before 「KeyError 위험」(조건 표현식) · 04 `고정 목록 사용: False`(손으로 적은 값).
6. **paired Before 설계**: 01·02 모두 Before가 「결함 코드를 실행한 결과」가 아닙니다(01은 같은 게이트, 02는 흉내). paired 빨강 상자 규칙(규격 §5-3)을 쓰려면 실제 결함 장면이 필요합니다.
7. **06이 01~05와 다른 코드**(게이트 없는 체이닝·다른 분류 셋·2번 반복) — 「같은 과제·같은 패턴」 비교의 공정성.
8. **try 0건** — `json_object` 형식이 깨지거나 시간 제한 45초·`max_retries=0`에서 서비스 오류(429·5xx)가 나면 셀이 멈춤. 03·04·06은 요청 3~4개를 한꺼번에 보냄.
9. **주피터와 병렬 실행**: 셀 맨 위 `await`는 Jupyter·VS Code 노트북·`execute.py`(nbclient + ipykernel)에서 됩니다(09-10·09-14 실행 통과). 같은 코드를 `.py` 파일로 옮기면 `SyntaxError`, 셀 안에서 `asyncio.run()`을 부르면 이미 도는 이벤트 루프 때문에 `RuntimeError`입니다(Ch 2 12 복습 4가 앞쪽만 설명). Windows·macOS 커널에서 `AsyncOpenAI`는 **이번에 실행하지 않았습니다**. 한 셀에서 만든 `AsyncOpenAI`를 다른 셀에서 쓰는 것은 같은 커널 이벤트 루프라 지금까지 문제 없었습니다.
10. **오래된 기록 문서**: `qa/verification.md`·`집필점검표.md`(09-10 값 — 03 4.619·9.263·A·A·B, 05 96점)가 지금 노트북(09-14)과 다름. `qa/research.md` 비용 표와 노트북 md 「계획 비용」이 04(0.0229 ↔ 0.0183)·05(0.0205 ↔ 0.0217)에서 다름. README가 학생 묶음에 없는 `qa/research.md`를 가리킴.
11. **옛 생성기 셋이 개선본을 덮어씀**(§3) — 01 작업 첫머리에 `raise SystemExit`.
12. **Part 5 옛 검사 넷**(Ch 17과 같음) — `check_scope.py` 절 수 6·실습 절 meta · `check_notebook_readiness.py` 타입힌트·21개 · `check_figures.py` `.excalidraw` 짝 · `finalize_evidence.py`(이미 멈춤). 고치지 않고 기록.
13. **「Ch 39」** — 05 b3·`continuity-guide.md`가 교재에 없는 챕터를 가리킴(확인한 연결만 쓰는 규칙, 규격 §7-2).
14. **비용·요청 수**: 한 번씩 35번 ≈ 0.015달러, 06 한 번 14번(상한 18) ≈ 0.0066달러. 새 커널 두 번 + 흔들림 확인(02·03·04·05·06 × 5번)을 모두 해도 요청 약 300번·0.2달러 안팎으로 절당 1달러 상한과 거리가 멉니다. 요청 수가 많은 것은 06(한 번 14번)과 03(8번). 06 한 번의 모델 대기는 걸린 초 합 약 21초라 기기 셸 180초 안.
15. **디스크**: 기기 루트 여유 **2.1G**(`/tmp/uv-cache` 379M · `/tmp/mmd` 471M · `/tmp/pptr-cache` 658M 포함). 가상환경은 마운트 폴더(174M). Mermaid 도구(`/tmp/mmd`·`/tmp/libs`·`/tmp/pptr-cache`·`/tmp/pw`) 있음. 루트 `.env`에 `OPENAI_API_KEY` **이름** 있음(값은 보지 않음).

## 8. 01절 작업자가 먼저 결정해야 할 것

1. **요청 도움 함수의 모양과 병렬 수단(§5 C)** — SDK 직접 호출은 고정(커리큘럼 v6·`verify.py`). 정할 것: 도움 함수 이름·인자(클라이언트·기록 목록을 인자로), `temperature=0` 추가, 기록 한 줄 칸(한국어 키 딕셔너리, Ch 17 「기록 한 줄」 선례), 03의 병렬을 (가) `AsyncOpenAI` 두 벌로 둘지 (나) 동기 한 벌 + Ch 2 12 `asyncio.to_thread` + `gather`로 할지. 01이 만든 함수가 02~06과 도구 파일에 그대로 이어지므로 **01에서 정해 `handoff.md`에 적어야** 합니다.
2. **§2-7 도구 파일(§5)** — 만들지(B, 이름 `workflow_tools.py` 후보) / 만들지 않을지(A). 06이 01~05 함수를 가져와 조립하는 설계인지와 묶여 있습니다. Ch 6 06 `estimate_cost`를 옮겨 「예상 비용」(Ch 17 요약 §4 과정 뜻)으로 맞출지도 함께.
3. **용어 표와 금지어·제목** — 「프롬프트」(01 제목 — Ch 15·16처럼 제목만 남기고 b2에서 풀지), 「병렬」(03 제목·Ch 13 금지어 — 이 챕터 말로 다시 열지), 영어 음역 「체이닝·섹셔닝·오케스트레이터·워커」, 그리고 경로→차례·갈래 · 분기→갈래 · 반환→내놓다 · 사전→딕셔너리 · 범주→종류 · 폴백→예비 흐름 · 거부→막다 · 검증→검사 · 임계값→기준값 · 측정→재다 · 추정·계획 비용→예상 비용. `instructions` = 「머리글」, `input` = 「요청 글」(Ch 17). 05의 `MAX_ITERATIONS`를 Ch 17 「바퀴 한도」로 부를지. 04에서 「모델이 정하는 칸」을 Ch 17 01 규칙과 어떻게 가를지(§2 04).
4. **paired 두 절의 Before와 `assert`** — 01 Before를 「게이트 없이 이어 부르기」로(요청 3번 → 4번?), 02 Before를 실제 `KeyError`(받아서 출력 = 노랑? paired Before 결함 = 빨강, 규격 §5-3)로 바꿀지. 모델 출력에 건 `assert` 넷을 무엇으로 바꿀지(요청 수·키 있음 등 매번 같은 값).
5. **흔들림 확인 계획과 06 출력 계약** — 02·03·04·05·06의 핵심 관찰을 노트북 밖에서 5번 먼저 확인할지와 순서(규격 §2-7 10번 끝). 05는 한 바퀴 종료가 계속되면 「같은 학습 목표 안에서 입력을 고침」 후보(예: 코드 검사로 길이를 먼저 보고 평가자 점수와 견주기). 06은 Ch 29 04 계약(마지막 다섯 줄·여섯 칸·`ok`)을 지키는 출력 모양을 먼저 정해야 01~05 함수의 기록 칸이 맞습니다. 03·06은 시간이 주제라 「재는 절」 예외로 둘지(Ch 15 05·06·Ch 17 04 선례).

## 9. 챕터 마감으로 미룰 것

- **07 실습 절 신설**(규격 §7-2): 슬러그 후보 `07-워크플로우-5패턴-실습`, 요청 3~5번, 새 문법·API 0. 06이 이미 「다섯 패턴 비교」 실험이라 **주제가 겹치지 않게**(예: 01 게이트 + 02 라우팅 + 05 정지 조건을 새 문의 하나에 붙이고 값 하나만 바꿔 다시). 따라오는 것: `chapter.json` 절 추가·meta 「실습 30분」(시수에 더하지 않음) · `textbook/part5/_build_index.py` 재실행 · 챕터 `qa/public-files.json` · `textbook/_notebook/build_index.py` 40행 6 → 7 · `check_scope.py` `SECTION_COUNTS`(기록만).
- 옛 생성기 셋 `mv -n` → `qa/upgrade/before/generators/blocked/`.
- 옛 그림 18개(`figures/0N-흐름.{svg,excalidraw,caption.md}`) + `figures/_gen_figures.py` 삭제 승인 목록(사본 `before/figures/`).
- `chapter.json` `objectives` 셋(「지연·품질 비교」·「빈 응답」 등)과 `textbook/part5/_build_index.py` Ch 18 설명·`textbook/_notebook/build_index.py` 40행 설명을 개선 본문과 대조.
- `textbook/part5/_src/index.html` 7·8행(타입 힌트) · `labs/part5/continuity-guide.md` 5행(「Ch 39」) · `practice-start.md` — Part 5 마감 몫이면 기록만(`finalize_evidence.py` 해시).
- 실습 폴더 README 다시 쓰기(도구 파일·`notebooks/`에서 열기·`uv sync --locked`·요청 수·예상 비용), `qa/research.md`·`qa/verification.md`·`집필점검표.md` 새 값으로.
- `part5-practice.zip` + **`part6-practice.zip`**(06 노트북이 Part 6 선행 파일) 재생성, `check_bundle_execution.py`·`check_delivery.py` 실행(`llm-practice.zip` Stale 멈춤 예상).
- **뒤 챕터 인계**: Ch 29 04 읽기 코드 결과·`_src` 평균 넷의 현재 값/새 값 · Ch 20 01·04 b3 · Ch 34 03 b3 문장 대조.
- 삭제 승인 대상: 실습 폴더 `.venv`(macOS)·`__pycache__`·`.ruff_cache` · `qa/upgrade/gates-wip-*.json` · `.cache/vm/venv-ch18-workflow-patterns` · 기기 `/tmp/ch18-prep`.

## 10. 만든 것

| 파일 | 내용 |
|---|---|
| `qa/upgrade/before/` | `_src` 6 · `notebooks` 6 · `figures` 19(SVG·excalidraw·caption 각 6 + `_gen_figures.py`) · `generators` 3(`_author.py`·`author_notebooks.py`·`_gen_figures.py`) · `qa` 3(`research.md`·`verification.md`·`public-files.json` — `_author.py`가 만든 파일이라 함께) · `pyproject.toml`·`uv.lock`·`README.md`·`chapter.json` = **41개, 552KB**. 원본과 `cmp` 모두 같음(원본은 그대로). `data/`·`runs/`·`tests/`는 챕터에 없어 없음 |
| `qa/upgrade/gates-before.json` | §0 표(절별 G1~G7 · 합계 233, 통과 0/6) |
| `qa/upgrade/before-manifest.json` | 보호 파일 15개 sha256 — Ch 17 마감 판(`agent_tools.py` `18209add…` · 자료 넷 — Ch 17 요약·매니페스트와 같음) · Part 5 묶음 공유 `orders.csv` 둘(`f2d1e3ee…`) · **Ch 18을 읽는 Ch 29 04 노트북(`b8c1b9d2…`)·`_src`(`ec34bf6e…`)·Part 6 선행 목록 둘** · Ch 18 03의 약속을 적은 Ch 2 12 노트북·`_src` · Ch 18 규칙을 가진 `verify.py`·`test_verify.py`. (Ch 18 06 노트북 자체는 바뀔 파일이라 넣지 않음 — 지금 `b583e8b4…`, 사본 `before/notebooks/`) |
| `$ROOT/.cache/vm/venv-ch18-workflow-patterns` | Python 3.12.13 · 174MB |

### 가상환경 만든 방법과 걸린 것

- `UV_CACHE_DIR=/tmp/uv-cache UV_LINK_MODE=copy` → `uv venv --python 3.12`. 잠금 목록은 `uv export --project labs/part5/ch18-workflow-patterns --frozen --no-hashes --all-groups --no-emit-project`(실습 폴더 파일 그대로 — `cmp` 확인), 주석 줄만 빼고 환경 표시(`sys_platform` 등)는 남김.
- **`uv pip install -r`이 마운트 폴더에서 멈춤**: `failed to remove directory …/ipykernel-7.3.0.data: Operation not permitted`(Ch 16·17과 같은 원인). 우회: `uv pip install pip==26.2` → **`bin/python -m pip install --no-cache-dir -r`**(Ch 16·17 선례, 루트 디스크에 pip 캐시를 남기지 않음).
- 결과: `pip freeze`와 잠금 대조 **판 차이 0**(설치 55 = 잠금 59 − 이 기기에 해당하지 않는 넷: `appnope`(darwin)·`colorama`(win32)·`cffi`·`pycparser`(PyPy)). `openai 2.29.0` · `python-dotenv 1.2.3` · `ipykernel 7.3.0` · `nbclient 0.11.0` · `pip 26.2` · `ruff 0.15.6` · `ipython 9.17.1` · `httpx 0.28.1` · `pydantic 2.13.5`. `pip check` 이상 없음. import 확인만(`openai`·`OpenAI`·`AsyncOpenAI`·`dotenv`·`ipykernel`·`nbclient`·`nbformat`·`jupyter_client`·`IPython`·`zmq`) + `ruff --version`. `Responses.create` 시그니처에 `temperature`·`reasoning`·`max_output_tokens`·`text`·`instructions` 있음. 커널 스펙 `share/jupyter/kernels/python3` 있음.
- 남은 흔적(마운트 폴더라 지울 수 없음): `site-packages/ipykernel-7.3.0.data/`(빈 폴더 사슬 — uv가 멈춘 자리)·`ruff-0.15.6.data/scripts/ruff`(pip이 옮긴 뒤 못 지운 사본). 두 패키지는 정상 설치돼 있습니다.
- `run_section.sh`는 `$ROOT/.cache/vm/venv-ch18-workflow-patterns`가 있으면 자동으로 쓰고 `UV_NO_SYNC=1`을 줍니다. `--with python-dotenv==1.2.3`·`--with pillow`를 따로 붙입니다.
