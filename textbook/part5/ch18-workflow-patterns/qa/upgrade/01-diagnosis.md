# 01절 진단과 개선 기록 — 게이트가 있는 프롬프트 체이닝 (paired)

- 작업 2026-09-23 · 규격 `textbook/QUALITY-UPGRADE.md`(§2·§2-7·§3·§4·§5-3·§5-4·§6·§7-2·§8) · 생성기 `qa/upgrade/author_01.py`(노트북 + `_src` 함께).
- 1차 자료: `qa/upgrade/chapter-lead-notes.md`(준비 담당 조사) + 챕터 리드 결정 9개(`handoff.md` 「챕터 공통」).
- Part 5 둘째 챕터의 첫 절입니다. **모델 요청 노트북 한 번에 6번**(4절 1 · 9절 2 · 10절 1 + 2), 임베딩 0, 파일 읽기·쓰기 0.

## 1. 게이트 전후

| | 코드 셀 | 검사 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 수정 전(`gates-before.json`) | 8 | 95 | 4 | 1 | 0 | 0 | 7 | 22 | 3 | **37** |
| 수정 뒤(`gates-wip-01.json`, `--no-exec`) | **28** | **380** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 `upgrade_gates.py … --label wip-01 --section 01` → `gates-wip-01-01.json`: **G1 0 · G2 0**(G6 7건 — 참고 자료 긴 문장 넷·다음 절 문장·「temperature를」 영문 시작 둘 — 은 실행 전에 고침, G7 18은 그림 전).
- **G4 0은 수정 전에도 착시였습니다**(준비 조사 §0 — 게이트는 `init_chat_model(`만 봄). 새 판은 SDK 요청 두 곳(4절 직접 요청·`ask_json`) 모두 `temperature=0`·`reasoning={"effort": "none"}`이고, 4절이 응답 객체의 `temperature: 0.0`·`추론 설정: none`을 출력합니다.
- `verify.py --chapter` → `PASS 6 sections / 71 code cells (max 24 lines)`(24줄은 아직 고치지 않은 02~06절 몫, 01절 셀은 주석 포함 최대 11줄). 빌드 HTML 일곱 개 `{{` 잔존 **0건**.
- 코드 줄(주석·빈 줄 뺌, `count_code.py`) 85 → **150**, 도구 파일 40줄. 비준비 셀 최대 **10줄**, 함수 본문 최대 **7줄**(`ask_json`·`check_plan`·`run_gated_chain`).

## 2. 수정 전 주요 문제

1. **paired Before가 결함 코드가 아니었습니다.** Before도 After와 같은 게이트 코드였고 다른 것은 요청 글(「title만」)뿐이었습니다. b6이 말한 잘못된 방식(빠진 키가 있어도 다음 요청에 넣기)은 실행하지 않았습니다.
2. 모델 출력에 건 `assert` 둘(Before 게이트 실패 · After 통과와 답이 비지 않음). 모델이 칸을 더 붙이면 Before가 멈추는 구조.
3. 금지·미교육 문법: 타입힌트 전부(`tuple[bool, list[str]]` 등)·기본값 매개변수(`limit: int = 240`)·제너레이터 식 둘·한 셀 함수 둘(`cost_usd`·`score_of`)·집합 빼기 `required - data.keys()`·`isinstance`·`sorted`·조건 표현식 `0 if not passed else 1`·f-string에 딕셔너리 통째로(모델이 받는 글이 파이썬 표기)·식 안 숫자 `0.75`·`1_000_000`·쓰지 않는 `Path` import.
4. **`temperature` 없음**(기본값) · `OpenAI(timeout=45.0, max_retries=0)` · 이 절에서 쓰지 않는 `call_answer`·`score_of`가 준비 셀에 있음(여섯 노트북 공통 54줄 준비 셀).
5. 금지어: 제목 밖 「프롬프트」 b2×2·b4·b5·b6×3 · 「반환」 · 「사전」 · 「경로」 · 「검증」 · 「직렬화」 · 「추정 비용」. 영문 시작 문장 다수. b3이 Ch 17을 되짚지 않고, 왜 SDK를 직접 쓰는지 한 문장이 없음.
6. 옛 그림 `{{svg:01-흐름}}` 한 장, Mermaid·삽화 0. 제목 셀·핵심 그림 첨부·결과 읽기 없음(G5 7). 복습 해설 넷이 「오답 시 다시 볼 곳: 핵심 개념과 실행 결과」 틀.

## 3. 챕터 리드 결정의 반영

| 결정 | 이 절에서 한 일 |
|---|---|
| 1. SDK 직접 · `temperature=0` 새로 · 잠금 그대로 | `client.responses.create(model="gpt-5.4-mini", temperature=0, reasoning={"effort": "none"}, instructions=…, input=…, text={"format": {"type": "json_object"}})`. **노트북 밖에서 먼저 확인**(`01-probe.md` §1 — `temperature` 0.0·`effort` none·`status` completed). 잠금 `openai==2.29.0`·`python-dotenv==1.2.3` 그대로(`pyproject.toml`·`uv.lock` 손대지 않음). b7에 「다른 챕터 실습 폴더에는 다른 판이 설치될 수 있고, 이 절은 2.29.0으로만 실행」 |
| 2. 병렬 수단 (나) | 01은 병렬을 쓰지 않음. 요청 도움 함수는 **동기 한 벌 `ask_json`** 으로 만들어 03이 `asyncio.to_thread(ask_json, client, records, …)`로 감쌀 수 있게 했습니다(인자로 `client`·`records`를 받고 전역에 기대지 않음). `AsyncOpenAI` 0. 동기 클라이언트를 여러 스레드에서 함께 쓰는지·기록 목록 `append`는 03 확인 몫(인계) |
| 3. 도구 파일 | `notebooks/workflow_tools.py` 새로(§8) |
| 4. 06·Ch 29 계약 | 기록 칸을 06이 표를 만들 수 있게 설계(`handoff.md` 「기록 한 줄」) — 01은 Ch 29 04가 읽는 06 출력에 닿지 않음 |
| 5. 용어 | `handoff.md` 용어 표. 「단계 잇기(prompt chaining)」·「라우팅(routing)」(Ch 17 01 말 그대로) · `instructions` = **「지시 글」** · `input` = 「요청 글」 · 「머리글」은 Ch 15·17 뜻(요청 글의 첫머리). 제목의 「프롬프트」는 두고 노트북 1절과 `_src` b2에서 한 번씩 풂(강사 확인) |
| 6. 문법 | 클래스·`@dataclass`·타입힌트·기본값 매개변수·f-string·셀 맨 위 `await`·`Counter`·`re.S`·`**` 풀기 0. 모델 출력 `assert` 0(손으로 적은 기획 둘에만) |
| 7. 시간·비용 | 걸린 시간을 재지 않음(b7). 준비물 「20초 안에」는 셀 실행 기록(A2 18.0초 · B2 16.1초). 비용은 노트북에서 셈하지 않고 준비물·b7에 「요금표로 어림한 예상 비용 0.01달러 아래」(Ch 6 06 뜻) |
| 8. 비유 「도예」 | 삽화 `01-5-가마-앞에서-골라낸-그릇`으로 엶(§7) |
| 9. 옛 생성기 막기 | §10 |

## 4. 설계 — paired

**학습 질문**: 두 모델 요청을 이을 때, 첫 요청의 답이 약속한 모양이 아니면 어떻게 둘째 요청 전에 멈출까요?

- **Before**(`lesson_part="before"`) = **게이트 없이 두 단계를 잇는 함수** `run_chain_without_gate(client, records, setup, plan_request)` — 기획 → 곧바로 작성. 상태는 늘 `완료`, 칸 「문제」는 빈 목록(아무도 보지 않았으므로).
- **After**(`lesson_part="after"`) = `run_gated_chain` — Before 함수의 두 요청 사이에 **게이트 세 줄**(`check_plan` → `if` → `return`)만 더함.
- **두 흐름에 넣는 요청 글은 같습니다**: 칸 이름을 적지 않은 기획 요청(실제 모델 요청 — 만든 값 아님, 노트북 밖 다섯 번 모두 칸 셋 없음). Before 결과: `상태: 완료`·`요청 수(기록 줄 수): 2`·뒤늦게 검사한 `넘어간 기획의 문제: ['제목 칸 없음', '독자 칸 없음', '절차 칸 없음']`(결함 — 그림 01-3 빨강 둘). After 결과: `상태: 멈춤`·같은 문제 셋·`요청 수(기록 줄 수): 1`.
- **After 둘째 실행**: 칸 셋을 약속한 3절 요청 글 → `상태: 완료`·요청 2. **값 바꿔 보기**: 필수 칸에 「문의처」 → 같은 기획이 `['문의처 칸 없음']`(모델 요청 0).
- 예제 부분(b5): SDK 직접 요청 한 번(응답 객체의 모델 이름·temperature·추론 설정·글·토큰) → `json.loads` → 기록 한 줄 `add_record`·`print_records` → `ask_json` → 게이트 `check_plan`(손 확인 `assert` 둘) → `build_write_request` → 흐름 설정 딕셔너리 `chain_setup`.
- 「중간 결과를 만든 값으로 넣는 방법」(챕터 리드 §3 대안)은 쓰지 않았습니다 — 실제 요청이 다섯 번 모두 같은 관찰을 내서 필요가 없었습니다.
- 칸 이름: 기획 칸 `제목`·`독자`·`절차`(흐름의 「단계」와 헷갈리지 않게 「절차」), 작성 답 칸 `안내문`. 기록 칸 `단계`·`입력 토큰`·`출력 토큰`.
- 처음 쓴 모양(한 문장씩 풂): `client.responses.create` 인자 여섯 · 응답 속성 `model`·`temperature`·`reasoning.effort`·`output_text`·`usage.input_tokens`·`usage.output_tokens` · `client.max_retries` · `type(…).__name__` · `list(딕셔너리.keys())` · `type(값) != list` · `and`/`or` 조건(`or`는 앞이 참이면 뒤를 보지 않음) · 함수 안 `return` 두 개 · `records[-1]`(Ch 17 03 `steps[-1]`) · 딕셔너리로 설정 한 벌 넘기기 · `json.dumps(…, ensure_ascii=False)`(Ch 16 02).

## 5. 흔들림 확인

`qa/upgrade/01-probe.md` — 노트북 밖 41번. 칸 이름을 적지 않은 요청은 다섯 번 모두 칸 셋이 없었고(원래 관찰 재현 → 입력 그대로, b7 문장), 칸을 약속한 요청은 다섯 번 모두 게이트를 지났습니다. 절차 수는 4·5로 흔들려 결과 읽기 둘째 단락에만 둡니다.

## 6. 실행값 (새 커널 네 번)

- **첫 코드 판**(A1 19:24:31~48 · B1 19:25:01~18 UTC, `code_sha256` `0127b009…`): 셀별 출력 20/28 같음. 실행 뒤 `check_plan` 본문이 **9줄**(과제 기준 8줄 넘음 — 「목록 아님」·「개수 모자람」 두 `if`)인 것을 찾아 조건 하나로 합치고(`… != list or len(…) < min_count`, 본문 7줄, 문제 글 「절차가 3개 이상인 목록이 아님」) 다시 실행했습니다. 이 다시 실행은 코드를 고쳐서이고 출력을 고르려는 것이 아닙니다.
- **교재 출력 판**(A2 = `run_section.sh` 19:32:27~45 UTC, B2 = 사본 19:32:57~33:13 UTC, `code_sha256` `59dc63e1ad01…`, `outputs_sha256` A2 `0648caf5eda2…`·B2 `910d93f069cb…`): 셀별 출력 **19/28 같음**. 다른 아홉 셀은 모두 모델이 쓴 글·토큰에 기대는 셀입니다 — 4절 기획 글과 `출력 토큰` 144↔125, `절차 수` 5↔4, 5절 기록 줄의 출력 토큰, 8절 작성 요청 글(기획이 들어감), 9절 기록 둘째 줄 `356 | 164`↔`398 | 169`·출력 토큰, 9절 넘어간 기획의 칸 이름·안내문, 10절 기록 출력 토큰, 10절 안내문.
- **네 번 모두 같은 값(본문·그림·정리에 쓴 값)**: `응답한 모델: gpt-5.4-mini-2026-03-17` · `temperature: 0.0` · `추론 설정: none` · `입력 토큰: 108` · `칸 이름: ['제목', '독자', '절차']` · `1 | 기획 | 57` · 9절 `상태: 완료`·`흐름이 알린 문제: []`·`요청 수(기록 줄 수): 2`·`넘어간 기획의 문제: ['제목 칸 없음', '독자 칸 없음', '절차 칸 없음']` · 10절 `상태: 멈춤`·같은 문제·`요청 수(기록 줄 수): 1` · 비교 표 두 줄 · 둘째 실행 `상태: 완료`·`게이트가 찾은 문제: []`·요청 2 · 값 바꿔 보기 `['문의처 칸 없음']`.
- 흔들린 값의 자리: 결과 읽기 둘째 단락에 「교재 출력에서는」으로만(`출력 토큰: 144`·`절차 수: 5`·`2 | 작성 | 356 | 164`·칸 「목적」·「대상」·「구성」). b6·b8·그림·복습에는 없음.
- 준비물 「20초 안에」 = 셀 실행 기록 A2 18.0초 · B2 16.1초(첫 판 A1 16.7 · B1 17.1).
- 서비스 요청: 노트북 한 번 6번 · 이 절 작업 전체 **65번**(노트북 밖 41 + 새 커널 네 번 24), 모두 `gpt-5.4-mini`, 임베딩 0. 요금표(2026-09-17 Ch 6 06: 100만 토큰당 입력 0.75 · 출력 4.50달러, 캐시 할인 없이)로 어림한 예상 비용 **약 0.07달러**(노트북 한 번 약 0.006달러, 청구 금액 아님).
- `run_section.sh 01` 첫 호출(A1)은 실행 뒤 그림 첨부 단계에서 `FileNotFoundError: 01-1-….png`로 멈췄습니다(그림을 A·B 대조 뒤에 그리려고 일부러 순서를 둠). A2 호출은 그림이 있어 끝까지 통과했습니다.
- 한 번은 생성기 설명 셀의 `lesson_part`를 고치려고(9절 결과 읽기 뒤 「## 10」 소제목이 Before 칸에 들어감) 노트북을 다시 실행하지 않고 **생성기 `cells()`로 다시 만든 셀에 실행 출력을 그대로 옮겨** 썼습니다(코드 셀 소스 28개 같음 확인, `code_sha256`·`outputs_sha256` 다시 셈해 `metadata.verification`과 같음). 이 일은 A1 판에서 했고, A2 판은 고친 생성기로 새로 실행했습니다.

## 7. 그림

- Mermaid 4장(`01-1`~`01-4`), 원본 viewBox 폭 **371 · 539 · 627 · 521**, 노드 7 · 7 · 7 · 7. PNG를 모두 다른 이름으로 복사해(`.cache/ch18-01-view/`) 직접 열어 확인. `01-2` 첫 렌더는 노드 id `call`(예약어)로 멈춰 `sdk`로 바꿈, `01-3` 회색 상자 줄 꺾임을 두 번 고침(설계표 `01-figures.md`). **빨강은 `01-3` 왼쪽 칸 Before 결함 결과 둘뿐**, 보라는 실제로 부른 모델 요청만.
- 삽화 `01-5-가마-앞에서-골라낸-그릇`: `nano_banana_pro`(응답 모델 이름 `nano_banana_2`) · 16:9 · 2k · `use_unlim:false` · count 1. **1차 job `c0aafb11-5ec7-48fe-b5ab-1c7a494acda4` 채택**(재생성 없음). 생성 전 잔액 2581.25, 거래 기록 2026-09-23T19:26:08Z 「Nano Banana Pro −2」 한 줄이 이 절 몫(그 앞 줄은 17:17 다른 세션). 원본 `b0b89d32…`(2752 × 1536) → 1100 × 614 `7c60d301…`. 결과 URL을 다시 받아 같은 폭으로 줄여 저장 PNG와 픽셀 대조 bbox `None`·extrema 모두 `(0, 0)`. 저장 PNG 사본을 직접 열어 그림 읽기(판 위 그릇 둘 · 접시 위 금 간 그릇 하나 · 가마 문으로 이어진 판)를 씀.
- 옛 그림 `figures/01-흐름.{svg,excalidraw,caption.md}`는 그대로 둠(본문 참조 0, 마감 삭제 승인 목록).

## 8. 도구 파일과 묶음 목록

- `labs/part5/ch18-workflow-patterns/notebooks/workflow_tools.py` **새로**, 함수 여섯(`json`만): `add_record(records, step_name, usage)` · `print_records(records)` · `ask_json(client, records, step_name, instructions_text, request_text)` · `check_plan(plan, required_keys, min_count)` · `build_write_request(write_head, plan)` · `run_gated_chain(client, records, setup, plan_request)`. 함수마다 `# Ch 18 01절에서 배웠습니다 — …`. **노트북 셀 판과 AST 같음**(여섯 모두 확인; `ask_json` 안 주석 한 줄만 「4절 직접 요청」 ↔ 「01절 직접 요청」으로 다름). 금지 문법 0, 전역 이름 기대기 0. Before 함수 `run_chain_without_gate`는 결함 판이라 옮기지 않음.
- 해시 **`a024ed897b3f1b70bbfbd18f1fc6dd422c448469c249207117084691b60527c3`**(최종). 첫 판 `f118bce4…`(`check_plan` 본문 9줄)을 노트북과 함께 고쳐 바꿈. 모델 요청 없이 흉내 객체로 여섯 함수를 불러 봄(멈춤 1 · 완료 2 · 목록 아닌 절차).
- 이름 확인: `verify.py` 금지 모듈(`rag`·`context_lab`·`document_processing`·`experiment`·`harness`·`prompts`·`langchain*`·`langgraph*`)과 겹치지 않음. 01 노트북은 도구 파일을 가져오지 않음(처음 가르치는 절).
- 묶음 목록: `textbook/part5/public-files.json`에 `labs/part5/ch18-workflow-patterns/notebooks/workflow_tools.py` 한 줄(Ch 17 `agent_tools.py`와 같은 방식 — 노트북은 슬러그로 자동이라 적지 않음, `8919f21f…` → `8b9d1aca…`) · 챕터 `qa/public-files.json` `include`에 `notebooks/workflow_tools.py`(`54132b5d…` → `5b23e044…`). `part5-practice.zip`은 다시 만들지 않음(마감 몫).

## 9. 용어·금지어 확인 (`_src`·노트북 설명·코드·출력·도구 파일 `grep`)

- 「분기」·「경로」·「반환」·「임계」·「재정렬」·「쿼리」·「인덱스」·「융합」·「RRF」·「조각」·「노드」·「한 겹 더」·「돌려줍」·「돌려 보」·「폴백」·「레코드」·「캐시」·「검증」·「범주」·「사전」·「거부」·「병렬」·「측정」·「최대 단계」·「중간 프로젝트」·「페이지」·「옵션」·「집합」·「정규화」·「강사 시연」·「개선 전」·「쉽게·간단히·당연히」·「추정 비용」 **0건**. 「프롬프트」·「체이닝」은 제목·슬러그와 풀이 문장(`_src` b2·노트북 1절)에만. 출력의 「로그」 넷은 모델 안내문의 「로그인」.
- 본문 `<code>`·노트북 백틱 인용 가운데 출력·코드에 없는 것은 경로·명령(`uv sync --locked`·`.venv`)과 다른 이름(`init_chat_model`·`json_schema`·`json.dumps(…, ensure_ascii=False)`)뿐.

## 10. 옛 생성기 막기 · 보호 파일 · 챕터 밖 수정

- 옛 생성기 셋 첫머리(`from __future__` 다음, `_gen_figures.py`는 docstring 다음)에 설명 주석 세 줄 + `raise SystemExit("개선 전 생성기입니다. textbook/part5/ch18-workflow-patterns/qa/upgrade/author_NN.py를 쓰세요.")`. 셋 다 실행해 종료 코드 1. 해시 `_author.py` `510b68b7…` → `69d4c684…` · `labs/…/author_notebooks.py` `5d84f3e9…` → `f9019b10…` · `figures/_gen_figures.py` `146d5d67…` → `29aa1214…`(원본 사본은 `before/generators/`). 옮기기는 마감 몫.
- 보호 파일 15개(`before-manifest.json`) **모두 같음**.
- 챕터 밖 수정: `textbook/part5/public-files.json`(도구 파일 한 줄) · `textbook/_notebook/checks/notebook-contracts-part5-ch18-workflow-patterns.json`(`verify.py --chapter`가 다시 씀). 공용 도구·규격·과정 요약·계약 파일·뒤 챕터 파일은 고치지 않음.

## 11. 참고 자료 확인 (WebFetch, 2026-09-23)

- Anthropic 「Building effective agents」(`https://www.anthropic.com/engineering/building-effective-agents`) — prompt chaining 정의, 중간 단계의 programmatic checks(「gate」), 예 「문서 개요를 쓰고 기준에 맞는지 본 뒤 본문을 쓰기」, 다섯 패턴 차례(Prompt chaining · Routing · Parallelization · Orchestrator-workers · Evaluator-optimizer).
- OpenAI 모델 문서 `https://developers.openai.com/api/docs/models/gpt-5.4-mini` — 요금 100만 토큰당 입력 0.75 · 캐시 입력 0.075 · 출력 4.50달러, 추론 설정 none(기본값). temperature는 이 문서에 없음 → 서비스 확인(`01-probe.md` §1)으로 대신함.
- OpenAI API 레퍼런스(`developers.openai.com/api/reference/…/responses/methods/create`)는 가져온 요약에 인자 설명이 없어, `instructions`(「A system (or developer) message inserted into the model's context.」)·`json_object`(「the model will not generate JSON without a system or user message instructing it to do so」, 「An older method … Using `json_schema` is recommended」)·다시 보내기 기본값(`DEFAULT_MAX_RETRIES = 2`)은 **설치한 openai 2.29.0 소스**에서 읽었습니다.

## 12. 강사 확인 대상

1. 제목의 「프롬프트」·「체이닝」을 두고 본문에서 「단계 잇기(prompt chaining)」로 풂(Ch 15·16 선례).
2. `instructions`를 「지시 글」로 부름(Ch 16 「시스템 메시지」·Ch 15/17 「머리글」과 가름 — SDK 설명의 system(또는 developer) 메시지 자리).
3. Before 요청 글을 「칸 이름을 적지 않은 기획 요청」으로 정함(실제 요청, 노트북 밖 다섯 번 재현) · After에 요청 글을 고친 둘째 실행을 더해 요청 6번.
4. 기본 클라이언트(다시 보내기 2번)로 바꿈 — 옛 판 `max_retries=0`과 달리 기록 줄 수는 받은 응답 수이고 다시 보낸 요청은 세지 않음(b7).
5. `json_object`(SDK 설명상 옛 방법)를 쓰고 `json_schema`는 쓰지 않음(b4 「비교와 경계」).
6. 실습 폴더 잠금 `openai 2.29.0`이 Ch 17(3.11.0)과 다름(챕터 리드 결정 1, b7 한 문장).
7. 코드 줄 85 → 150(+ 도구 파일 40) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘(02~06이 도구 파일을 가져오면 챕터 합계는 줄 예정).
8. 비유 계열 「도예」 · 삽화 한 장.

## 13. 남은 것 · 지우지 않은 것

- 마감 몫: 옛 생성기 셋 `mv -n` → `before/generators/blocked/` · 옛 그림 `figures/01-흐름.*` 셋 삭제 승인 · 실습 폴더 README(도구 파일·`notebooks/`에서 열기·요청 수) · `part5-practice.zip`·`part6-practice.zip` 재생성 · `chapter.json` objectives 대조 · `qa/research.md` 비용 표.
- 지워야 하지만 지우지 않은 임시 파일: 기기 `/tmp/ch18-01/`(확인 스크립트·실행 사본 A·B·A2·B2·다시 만든 노트북·삽화 원본 둘 약 7MB) · `$ROOT/.cache/ch18-01-view/`(그림 확인 사본 일곱) · `qa/upgrade/gates-wip-01.json`·`gates-wip-01-01.json`.

## 마감 반영 (2026-09-23)

검토 1차(`review-round1-A.md`·`review-round1-B.md`)를 반영했습니다. **노트북은 다시 실행하지 않았습니다** — `mdpatch.py`(생성기·노트북 마크다운·`_src`) → `run_section.sh … 01 --no-exec`. 노트북 `code_sha256` `59dc63e1…` · `outputs_sha256` `0648caf5…` · `executed_at` 그대로, 게이트 G1~G7 0(검사 문장 398), 생성기 `cells()`·`SRC_HTML`이 노트북·`_src`와 글자까지 같음. 전체는 챕터 요약 §15.

- **A-1 [중]** 7절 결과 읽기에 `and`가 칸 「절차」가 없을 때 `plan["절차"]`를 읽지 않게 막는다는 풀이 넷 문장(02절 `KeyError`와 이음), `_src` b4 「게이트는 코드로 검사합니다」 뒤에 두 문장 단락.
- **A-2** 10절 정의 셀 결과 읽기에 「마지막 줄의 칸 「문제」에는 빈 목록 대신 검사 결과를 넣습니다」, 비교 표 결과 읽기 「코드에서 다른 것은 게이트 세 줄과 마지막 줄의 칸 「문제」뿐」, b6 「게이트만 더합니다」 → 「게이트를 더합니다」, 그림 `01-3` 회색 상자·alt(다시 렌더).
- **A-3** 노트북 1절에 SDK 풀이 세 문장(`_src` b3과 같은 뜻). **A-4** 3절 결과 읽기에 「서비스가 이 말을 지시 글이 아니라 요청 글에서 찾는다는 것은 02절에서 봅니다」. **A-13** 5절에 「Ch 17의 실행 기록은 도구 단계와 멈춤까지 단계 하나를 한 줄로 적었습니다 · 이 챕터의 기록 한 줄은 모델 요청 한 번」.
- **A-12** 준비물·b7 비용 문장: 토큰 수를 출력하는 요청은 여섯 번 가운데 네 번(4절 1 · 9절 2 · 10절 After 1), 나머지도 같은 크기로 어림 — 결론 「0.01달러 아래」 그대로. 준비물 단락이 여섯 문장이 되어 두 단락으로 나눔(G6).
- **A-14** `pack.py … 01` 다시(교재 출력 판 — `출력 토큰: 144` 2건·`127` 0건).

