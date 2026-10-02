# Ch 18 워크플로우 5패턴: 맨손 구현 — 챕터 요약 (다음 챕터 작업자용)

- 대상: `textbook/part5/ch18-workflow-patterns` 01~06절(품질 개선) + **07절 챕터 끝 실습 절 신설**(`07-워크플로우-패턴-실습`), 노트북 `labs/part5/ch18-workflow-patterns/notebooks/01~07-*.ipynb`, 도구 파일 `notebooks/workflow_tools.py`.
- 기간: 2026-09-23(준비 조사 · 01~06절 개선 · 07절 신설 · 검토 1차 반영 · 챕터 마감). 상태: **완료(강사 확인 대기)**.
- 게이트: 수정 전 여섯 절 합계 **233**(01 37·02 33·03 49·04 29·05 27·06 58, `gates-before.json`) → 마감 뒤 **7/7 PASS, G1~G7 모두 0**(`gates-after.json`, 검사 문장 398·369·429·458·460·455·362 = **2,931**).
- 코드 셀 28·26·29·29·29·27·24 = **192**(`verify.py --chapter` → `PASS 7 sections / 192 code cells (max 11 lines)`), 코드 줄(주석·빈 줄 뺌) 148·149·187·175·183·202·128 = 1,172 + 도구 파일 207. Mermaid **27장**(01~06 넷씩 · 07 셋), 삽화 **7장**(절마다 하나), 복습 문제는 HTML에만.
- 서비스 요청(노트북 한 번씩, 교재 출력 기준): 01 6 · 02 8 · 03 12 · 04 11 · 05 10 · 06 14 · 07 4 = **65번**(모두 `gpt-5.4-mini`, 임베딩 0). 코드가 정한 상한 때문에 04는 12번, 05는 10번, 06은 19번, 07은 6번을 넘지 않습니다. 노트북마다 요금표로 어림한 예상 비용은 0.01달러 아래(청구 금액 아님).
- 화면 검사 `visual.cjs`: HTML **여덟 개**(일곱 절 + `index.html`) × 1280px·390px = **16행 PASS**(`textbook/_notebook/checks/ch18-workflow-patterns/visual-results.json`).
- **마감에서 다시 실행한 노트북은 없습니다.** 일곱 노트북 모두 `code_sha256`·`outputs_sha256`·`executed_at`이 마감 전후 같습니다(마크다운만 바뀜, §15). 06은 Ch 29 04 계약 때문에 처음부터 다시 실행하지 않는 노트북입니다.
- 읽는 순서: 과정 요약 `textbook/qa/upgrade-course-summary.md` → Ch 17 요약 → **이 문서** → `handoff.md`(절 사이 세부, 끝의 「검토 반영과 챕터 마감」) → 절별 `NN-diagnosis.md`(끝 절 「마감 반영」) → 검토 `review-round1-A.md`(01~03·공통)·`review-round1-B.md`(04~07) → 흔들림 확인 `0N-probe.md`.

## 1. 새로 가르친 것 (노트북에서 실행한 것만)

| 절 | 문법·API | 새로 만든 함수 (도구 파일에 둔 것은 굵게) | 새 용어 |
|---|---|---|---|
| 01 게이트가 있는 프롬프트 체이닝 (paired) | **OpenAI SDK 직접 호출** `client.responses.create`(인자 `model`·`temperature`·`reasoning`·`instructions`·`input`·`text={"format": {"type": "json_object"}}`) · 응답 `output_text`·`usage.input_tokens`·`usage.output_tokens`·`model`·`reasoning.effort` · `client.max_retries`(기본 2, 소스 확인) · `type(값) != list` · `and`/`or`가 뒤를 보지 않는 성질(마감 — `and`로 없는 칸을 읽지 않음) · 함수 안 `return` 둘 · `records[-1]` · 흐름 설정 딕셔너리 한 벌 · `json.dumps(…, ensure_ascii=False)`(Ch 16 02) | **`add_record`** · **`print_records`** · **`ask_json`** · **`check_plan`** · **`build_write_request`** · **`run_gated_chain`** · `run_chain_without_gate`(Before 결함 판, 옮기지 않음) | 단계 잇기 · 중간 결과 · 게이트 · 지시 글 · 클라이언트 (5) |
| 02 실패를 처리하는 라우팅 (paired) | 이 챕터 첫 **도구 파일 가져오기** · 실제 `KeyError`와 `try`/`except KeyError as error`(Ch 2 05 모양, 셀은 끝까지 · 실제 프로그램은 멈춤) · `type(error).__name__` · 딕셔너리 값으로 딕셔너리 찾기 · `list(딕셔너리.keys())`로 허용 목록 · 수 비교 `<` | **`check_route`** · **`route_question`** · `route_without_check`(Before) | 라우팅 · 갈래 · 신뢰도 · 기준값 · 되묻기 (5) |
| 03 병렬 섹셔닝과 투표 | `async def` · 셀 맨 위 `await`(IPython 기능) · **`asyncio.to_thread(함수, 인자들)`** · **`asyncio.gather`**(변수 셋 → **`gather(*waitings)` 별표 풀기, 과정 처음**) · 동기 `OpenAI()` 하나를 여러 스레드가 함께 씀(httpx 설명·밖 20/20 확인) · 목록 `append`가 스레드에서도 한 번에 끝남(Python FAQ, 마감) · 한 번 기다린 코루틴을 다시 기다리면 `RuntimeError`(마감 안내) · `time.perf_counter()`·`round(…, 3)`(Ch 2 12·Ch 15 05) | **`build_part_request`** · **`ask_all_together`**(async) · **`join_parts`** · **`write_sections`**(async) · **`count_votes`** · **`decide_vote`** · **`run_vote`**(async) | 함께 보내기 · 나눠 쓰기 · 투표 · 다수결 · 필요한 표 수 (5) |
| 04 동적 오케스트레이터와 워커 | 목록 자르기 `[:max_tasks]`(Ch 2 되짚기) · 정규식 `[a-z]`·`\.`·`\d+` + `re.findall`(Ch 16 02) · 한 기록 목록을 계획·작업·종합이 함께 씀 · `async def` 흐름 함수 안에서 동기 `ask_json`과 `await`를 섞어 부름 · 흐름 결과 「멈춤」을 `return`으로 | **`pick_tasks`** · **`build_task_requests`** · **`build_summary_request`** · **`find_new_contacts`** · **`plan_tasks`** · **`run_orchestrator`**(async) | 작업 나눠 맡기기 · 계획 모델 · 작업 모델 · 작업 목록 · 종합 (5) |
| 05 생성자 평가자와 정지 조건 | 함수가 내놓은 목록에 이어 `append` · `for turn in range(n)` + `break`(Ch 17 05) · 딕셔너리 `copy()` · `str(수)` · `len()`으로 글자 수(띄어쓰기·문장 부호 포함) | **`check_length`** · **`check_draft`** · **`decide_stop`** · **`build_notes`** · **`write_and_judge`** · **`finish_loop`** · **`run_write_judge_loop`** | 쓰고 평가하기 반복 · 쓰는 모델 · 평가 모델 · 고칠 점 · 코드 검사 (5) |
| 06 같은 과제로 다섯 패턴 비교 | 흐름 함수 다섯을 한 노트북에서 조립 · 흐름 앞뒤 `time.perf_counter()` 차 · 표 한 줄 딕셔너리 · `for` + `>`로 가장 큰 줄 찾기(`max` 대신) · `range(len(rows))` · 설정 `copy()`로 검사 값 한 칸만 바꿔 다시 셈 · `[:1]` | **`total_tokens`** · **`grade_notice`** · **`make_row`** | 같은 조건 비교 · 비교 표 한 줄 · 품질 칸 (3) |
| 07 워크플로우 패턴 실습 | **새 문법·API·말 0개** | 노트북에만 `summarize_run` · `print_summaries` · `serve_notice`(조립 함수, `async def`) | 0 |

- 새 용어 합계 **28개**(절 meta 「새 용어」 5·5·5·5·5·3·0과 같음).
- **쓰지 않은 Python 이름(일곱 절 모두 0건)**: f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`else`·`:=`·`global`·`next`·`all`·`any`·`sum`·`max`·`min`·`sorted`·`enumerate`·`zip`·`key=`·`reverse=`·`set`·`setdefault`·`.get`·`+=`·`float`·기본값 매개변수·**타입힌트**·튜플 풀기·클래스·`@dataclass`·`isinstance`·`Counter`·`while`·`raise`·`AsyncOpenAI`·`json_schema`·`re.S`·`**` 풀기·`threading`·**LangChain·LangGraph 전부**(`verify.py`가 Ch 18 노트북의 `langchain*`·`langgraph*` import를 막음) · 도구 호출 API(`bind_tools`·`tools=`·`tool_calls`). `try`는 02 Before의 `except KeyError` 한 번뿐.
- 셀 모양: 비준비 셀 최대 10줄, 함수 본문 최대 8줄, 셀당 함수 하나, 첫 줄 주석 100%. **모델이 쓴 글·잰 값에 건 `assert`는 0건** — 손으로 적은 기획·표·글·기록에만.

## 2. 앞 챕터에서 이어 쓴 부품과 값

- **Ch 2**: 03 `KeyError`(02에서 실제로 봄) · 05 `try/except … as error` · 12 코루틴·`await`·`asyncio.gather`(내놓는 목록은 넣은 차례)·`asyncio.to_thread`·`asyncio.run(main())`(03 b7에서 파일로 옮길 때만) — **Ch 2 12 b8 약속 「Ch 18 3절은 모델 호출 세 개를 `asyncio.gather()`로 함께 기다리고, 반환 목록이 입력 순서라고 적습니다」를 03 5절이 지켰습니다**(Ch 2 12 파일은 보호 파일, 고치지 않음).
- **Ch 6 06**: `temperature=0`·`reasoning` 설정의 뜻 · 요금표(2026-09-17, 100만 토큰당 입력 0.75 · 출력 4.50달러) · 「예상 비용」 = 사용량 × 요금표(청구 금액 아님). **`estimate_cost`는 이 챕터 어느 절도 도구 파일에 옮기지 않았습니다**(노트북에서 비용을 셈하지 않음).
- **Ch 13 03** 「기준값」 · **Ch 15** 01 평가 모델(judge)·02 JSON 판정 글과 `json.loads`·03 차례 바꾸기 검사(03 투표에서 「하지 않았다」로만)·05 걸린 시간 재기 예외 · **Ch 16** 01 입력 검사·허용 목록(02 「허용할 종류 목록」)·02 정규식·`re.findall`·`ensure_ascii=False`·04 「호출 한도」(05 「바퀴 한도」와 가름)·05 예비 흐름 · **Ch 17** 01 워크플로우/에이전트 후보 규칙·라우팅 정의·`count = count + 1`·03 바퀴·정지 조건·바퀴 한도·`steps[-1]`·05 `for`·`break`.
- **Ch 17 `agent_tools.py`는 가져오지 않습니다**(Ch 18은 LangChain 없이 SDK 직접 — 도구 파일도 따로).

## 3. 절별 사례·값 (새 커널 두 번과 노트북 밖 확인에서 같았던 값)

| 절 | 과제·입력 | 결정적 값(결론·그림에 쓴 값) | 요청 |
|---|---|---|---|
| 01 | 비밀번호 재설정 안내문 기획 → 작성. Before·After 요청 글 = 칸 이름을 적지 않은 기획 요청 | `입력 토큰: 108`(칸 셋 약속 요청) · `1 \| 기획 \| 57` · Before `상태: 완료`·요청 2·`['제목 칸 없음', '독자 칸 없음', '절차 칸 없음']` · After `상태: 멈춤`·요청 1 · 고친 요청 `완료`·요청 2 · 필수 칸 + 「문의처」 → `['문의처 칸 없음']` | 6 |
| 02 | 고객 문의 라우팅(종류 결제·계정·기술, 모름) · 섞인 문의 · 배송 문의(탐색 실행으로 고름) | `종류: 결제`·`1 \| 분류 \| 126 \| 22` · 허용 목록 `['결제', '계정', '기술']`·기준값 0.75 · Before `KeyError '모름'`·요청 1 / 배송 `완료`·요청 2·`['신뢰도가 기준값보다 낮음']` · After 두 문의 `되묻기`·요청 1씩 · 결제 `완료`·요청 2 · 허용 목록에서 결제를 빼면 `['허용 목록에 없는 종류']` | 8 |
| 03 | **2단계 인증 공통 사실(131자, `help@company.test`) — 03~07절이 이어 씀** · 부분 셋(목적·절차·문의) · 후보 글 A·B와 평가자 셋(손으로 정함) | 입력 토큰 196·195·194(하나씩·함께 같음) · `받은 답의 칸 「부분」 차례: ['목적', '절차', '문의']` · `요청 수(기록 줄 수): 3 3` · 나눠 쓰기 `완료`·요청 3 · 표 A·A·B · 셈 `{'A': 2, 'B': 1, '그 밖': 0}`·결과 A · 필요한 표 수 3 → `정하지 못함`. **「함께 기다린 쪽이 짧은가: True」는 두 번·밖 다섯 번 같았지만 흔들린 값(걸린 초)에서 끌어낸 비교라 마감에서 그림·결론·정리에서 뺌**(§6) | 12 |
| 04 | 과제 글 B2 「신입 직원 … 적용 날짜, 까닭, 등록 방법, 문의처를 따로따로」(4~7절) / B1 「등록 방법만 짧게」(10절) | `받은 작업 수: 4`·이름 넷 · `요청 수(기록 줄 수): 6`·`1 + 작업 수 + 1: 6`·`1 \| 계획 \| 232` · 손 확인 `['helpdesk@company.com', '1234']` · 종합 답 검사 `[]` · 10절 `완료`·`작업 수 4 3`·`요청 수 6 5`. **작업 넷은 과제 글의 네 항목과 짝이 맞아 과제 글이 작업 수를 사실상 정함**(마감 B-1) · **이 절 종합 요청 글에는 과제 글이 없음**(마감 B-2) | 11 |
| 05 | 과제 150~170자·꼭 담을 말 넷 · 기준값 85 · 바퀴 한도 3 / 1 | 손 확인 `['기준 통과', '계속', '계속', '바퀴 한도']` · 첫 바퀴 `평가 점수가 기준값 이상인가: True`·`코드 검사 문제: ['글자 수가 150자보다 적음']`·`정지 판정: 계속` · `설정 칸 수: 9` · `1 \| 쓰기 \| 221` · 11절(한도 1) `멈춤`·`바퀴 한도`·요청 2 | 10(많아야) |
| 06 | 같은 과제 글(120~180자, 적용 날짜·대상·등록 방법·문의처 주소) · 코드 검사 값 `grade_setup` | 다섯 흐름 `완료` · `calls` 2·2·3·5·2 · 02 분류 `보안 0.99` · parallel 104자 → 품질 4 · 04·05 품질 5 · 최소 글자 수 100이면 다섯 모두 5 · 표 여섯 칸·`ok` 다섯(Ch 29 계약, §8) | 14 |
| 07 | 공지 요청 글 한 문장(종류 이름 없음) · 허용 목록 셋 / 둘 | §7 | 4 |

## 4. 용어 (챕터 안에서 한 번만 정의하고 이어 씀)

**패턴 이름**(한국어를 먼저, 영문은 처음 한 번 괄호. 제목은 바꾸지 않고 본문에서 풂 — 강사 확인):

| 절 · 제목 | 이 챕터 말 | 제목 말 풀이 |
|---|---|---|
| 01 게이트가 있는 **프롬프트 체이닝** | **단계 잇기(prompt chaining)** · 게이트 · 중간 결과 | 「프롬프트」는 제목·풀이 한 번(`_src` b2·노트북 1절) |
| 02 실패를 처리하는 **라우팅** | **라우팅(routing)** — Ch 17 01 뜻 그대로(모델이 쓴 종류를 보고 코드가 준비한 갈래로) · 갈래 · 되묻기 · 허용 목록 · 기준값 · 신뢰도 | — |
| 03 **병렬 섹셔닝**과 투표 | **함께 보내기(parallelization)** — **나눠 쓰기(sectioning)** · **투표(voting)** · 다수결 · 필요한 표 수 · 부분 · 넣은 차례/도착 차례 | 「병렬」은 **마감에서** 노트북 1절·b4 용어 표에서 한 번씩 풂(Ch 13 금지어 — 제목·풀이 밖 0) · 「섹셔닝」 풀이 한 번 |
| 04 **동적 오케스트레이터와 워커** | **작업 나눠 맡기기(orchestrator-workers)** — 계획 모델(오케스트레이터 = 계획 요청 + 종합 요청) · 작업 모델(워커) · 작업 목록 · 종합 | 「동적」은 제목에만(「입력을 보고 모델이 정하는」으로 풂) |
| 05 **생성자 평가자**와 정지 조건 | **쓰고 평가하기 반복(evaluator-optimizer)** — 쓰는 모델(생성자) · 평가 모델(평가자, Ch 15 judge와 같은 뜻) · 고칠 점 · 코드 검사 · 바퀴 줄 · 정지 판정 · 멈춘 까닭(기준 통과/바퀴 한도) | 셋째 정지 조건(개선 폭)은 구현하지 않음 |
| 06 같은 과제로 다섯 패턴 비교 | 같은 조건 비교 · 비교 표 한 줄 · 품질 칸. **표의 칸·패턴 이름은 영어 그대로**(`pattern`·`calls`·…·`chaining`·`routing`·`parallel`·`orchestrator_worker`·`generator_evaluator` — Ch 29 계약) | 「패턴 선택표」 쓰지 않음 |

- **지시 글(instructions)** = 인자 `instructions`에 적는 역할·규칙 글(SDK 설명상 시스템/개발자 메시지 자리, 「Ch 16 01절의 시스템 메시지와 같은 구실」) ≠ Ch 16 06 「숨은 지시문」. **요청 글(input)** = Ch 15·17 뜻 그대로. **머리글** = 요청 글의 첫머리 글(Ch 15·17). **`json_object` 형식은 요청 글(input)에 「JSON」이라는 말이 있어야 합니다** — 지시 글에만 두면 서비스가 400으로 막음(02 밖 확인). 01 결과 읽기도 마감에서 이 사실을 02절로 이음(검토 A-4, handoff 47행 고침).
- **기록 한 줄 = 모델 요청 한 번**(`{"단계", "입력 토큰", "출력 토큰"}`), **요청 수 = 기록 줄 수**. **Ch 17의 「기록 한 줄 = 단계 하나」(칸 「단계」·「한 쪽」·「고른 쪽」)와 다릅니다** — 01 5절이 마감에서 한 문장으로 가름(A-13). 함께 보낸 요청의 칸 「단계」에는 부분·작업·평가자 이름을 적고, 기록 줄은 **도착 차례**로 쌓임(gather 목록은 넣은 차례).
- **Ch 17 판정 문장(검토 B-6, 01~07 같은 기준)**: 이 챕터 기록 줄에는 칸 「고른 쪽」이 없습니다. 판정은 「Ch 17 01절처럼 단계마다 다음 단계를 고른 쪽을 적어 보면 모두 코드 → 워크플로우」로 적습니다(04·05 b4·복습 3·노트북 9절). 다섯 흐름과 07 조립 모두 다음 단계를 고른 쪽은 코드입니다.
- **바퀴 한도**(05, Ch 17 03 말) ≠ **호출 한도**(Ch 16 04). 「최대 반복」 쓰지 않음. 품질 기준 85 = **기준값**(02 말). **품질 칸**(06) = 글자 수 범위 + 꼭 담을 말 넷을 세는 코드 검사 0~5 — 평가 모델 점수가 아님.
- **흐름 결과 칸 「상태」**: 01 완료/멈춤 · 02 완료/되묻기 · 03 늘 완료 · 04 완료/멈춤 · 05 완료/멈춤(멈춘 까닭 기준 통과/바퀴 한도) · 07 완료/되묻기. 결과 글 칸은 02만 「답」, 나머지 「안내문」.
- **금지어(일곱 절 설명 0건 — 제목·풀이 자리 말고)**: 「분기」·「경로」·「반환」·「임계값」·「재정렬」·「쿼리」·「인덱스」·「융합」·「조각」·「노드」·「한 겹 더」·「돌려줍니다」·「프롬프트」·「폴백」·「레코드」·「검증」·「범주」·「사전」·「거부」·「병렬」·「측정」·「최대 단계」·「중간 프로젝트」·「페이지」·「옵션」·「집합」·「정규화」·「강사 시연」·「개선 전」·「추정 비용」·「쉽게·간단히·당연히」·「지연」(→ 걸린 초)·「동적으로」·「최대 반복」·「Ch 39」·「호출 상한」·「패턴 선택표」·「awaitable」. 「코루틴」은 03(가르치는 절)과 06·07 되짚기에만. 모델이 쓴 출력의 「로그인」은 「로그」로 잡히니 가려 봄.

## 5. 색 규칙 (Mermaid 27장, 빨강 4상자)

- **손으로 적은 요청 글·과제 글·설정·바꾼 값·공통 사실 초록(tool)** · **우리가 코드로 적은 함수(게이트·검사·흐름 함수) 파랑(flow)** · **그 절에서 실제로 부른 모델 요청만 보라(model, `gpt-5.4-mini`)** · **출력으로 확인한 값 노랑(measure)** · **SDK·`asyncio` 같은 라이브러리, 두 칸 공통 사실, 이번에 나오지 않은 갈래 회색** · **빨강은 paired Before 결함 결과만**(01-3 왼쪽 둘 · 02-3 왼쪽 둘). experiment 03~07은 빨강 0.
- 마감에서 맞춘 것: `01-3` 회색 상자(게이트 세 줄 + 마지막 줄의 칸 문제) · `03-2` 노랑 「넣은 차례와 다를 수 있음」 · `03-3` 노랑 관찰 상자 뺌·회색 메모 · `04-3` 회색 공통 상자(같은 차례와 설정 · 4~7절은 셀 · 10절은 흐름 함수) · `05-1` 「기준 통과 · 상태 완료」 노랑 → 회색 「교재 출력의 흐름에는 없음」.
- 원본 viewBox 폭 모두 868 이하(최대 `02-3` 830 · `07-2` 780). 칸 비교는 subgraph 둘 + `~~~` 회색 공통 상자, 갈래는 점선, 넷 이상 한 줄이면 `flowchart TB`, 저절로 꺾이는 라벨은 `<br>`로 미리(마감 `03-3`·`04-3` 첫 렌더에서 꺾여 다시 나눔). 노드 id `call`·`end` 금지.
- 비유 계열 「도예(점토·물레·가마)」: 01 가마 앞에서 골라낸 그릇(금 간 그릇 = 게이트가 멈춘 기획) · 02 모양별 선반 셋과 작업대의 덩이(되묻기) · 03 가마 하나에 함께 넣은 그릇 셋 · 04 큰 덩이를 나눠 빚은 그릇 · 05 세 번 빚은 찻잔과 자 · 06 같은 흙으로 빚은 다섯 그릇 · 07 물레 둘의 그릇과 탁자 위 덩이. 사람·손·동물·화면·표지판·화살표·길·저울(Ch 15)·발자국(Ch 17)은 쓰지 않았습니다.

## 6. 서비스 요청과 흔들린 값

- 노트북 한 번 요청: §머리(65번). 작업 전체 서비스 요청: 01 65 · 02 52 · 03 89 · 04 103 · 05 80 · 06 98 · 07 28 = **515번**, **마감 0번**. 요금표로 어림한 예상 비용 합 약 0.26달러(청구 금액 아님). 삽화 7장 Higgsfield `nano_banana_pro` 장당 2크레딧 = 14크레딧(06 1차는 서비스 필터로 막혀 환불).
- **흔들림 확인(노트북 밖 다섯 번, 규격 §2-7 10번 끝)**: 01(칸 없는 요청 5/5 칸 셋 없음 · 약속한 요청 5/5 통과) · 02(섞인 문의 5/5 `모름` · 배송 10/10 허용 목록 안 + 신뢰도 0.18~0.34) · 03(받은 차례 5/5 · 도착 차례 5/5 넣은 차례와 다름 · 함께가 짧음 5/5 · 원표 5/5 A·A·B, 스레드 20/20) · 04(B2 작업 넷 5/5 · B1 셋 5/5 · 종합 답 지어낸 주소·숫자 15/15 0) · 05(150~170자 판 첫 바퀴 15/15 「점수 ≥ 85 + 150자보다 짧음」) · 06(다섯 흐름 25/25 완료) · 07(분류 10/10 보안 0.99).
- **탐색으로 고른 입력(b7에 「흐름을 보여 주려고 정한 예」)**: 02 배송 문의 · 04 과제 글 B2/B1 · 05 150~170자 · 06 120~180자 · 07 실행 2 허용 목록. 03 후보 글·평가자 기준은 손으로 정한 값(탐색 실행 없음).
- **흔들린 값의 자리**: 결과 읽기 둘째 단락·본문 표·「확인할 점」에만(「교재 출력에서는」·「한 번 더 실행했을 때는」). **마감에서 흔들린 값에서 끌어낸 비교를 결론·그림·정리에서 뺐습니다**(챕터 리드 결정, 규격 §2-7 9번 끝): 03 걸린 초 비교(그림 `03-3`·b6·b8·노트북 정리)와 도착 차례 ≠ 넣은 차례(그림 `03-2`·b6), 06 「토큰 수가 가장 많은 흐름은 두 번 모두 작업 나눠 맡기기」(b6 → 구조 문장). 결과 읽기 첫 단락의 출력 인용(03 `함께 기다린 쪽이 짧은가: True` · 06 `토큰 수가 가장 많은 패턴도 orchestrator_worker`)은 「이번 실행에서는」과 함께 그대로 두었습니다.
- **강사 확인으로 남긴 것**: 05 첫 바퀴 「평가 점수 ≥ 85 · 150자보다 짧음」(점수 96/92·글자 수 136/126이 두 번 달랐지만 판정은 두 번 × 세 흐름 + 밖 15/15 같음)은 검토 B 판정대로 결론·그림 `05-2`·`05-4`에 두었습니다. 규격 §2-7 9번을 글자 그대로 적용하면 이것도 「흔들린 값에서 끌어낸 비교」로 읽힐 수 있습니다(§12 3번).
- **재지 않은 것**: 걸린 초의 분포·백분위수(03·06 흐름마다 한 번, 순위 결론 0), 답 품질(06 품질 칸은 코드 검사), 청구 금액, 서비스 오류(429·5xx)·SDK 다시 보내기·`JSONDecodeError`를 실제로 본 장면(모두 0번).

## 7. 07절 실습 절 주제와 결과

- 제목 「**워크플로우 패턴 실습: 공지 요청을 라우팅 검사 뒤 나눠 쓰고 허용 목록 바꾸기**」, 슬러그 `07-워크플로우-패턴-실습`(강사 확인 — handoff 제안 `07-워크플로우-5패턴-실습`), `format: experiment`, meta 「실습 30분 · 새 용어 0」. **챕터 시수에 더하지 않습니다**(규격 §7-2). 01~06 meta 합 강의 0.7×5 + 0.5 = 4.0h · 실습 1.5+1.5+2+2.5+2+2.5 = 12h = `chapter.json` 「총 16h · 강의 4h · 실습 12h」(`_build_index.py`도 4·12).
- 붙인 앞 절 기능 셋: **01 게이트 자리**(앞 단계와 뒤 단계 사이 검사, `ask_json`·`print_records`, 요청 수 = 기록 줄 수) + **02 라우팅 검사**(분류 지시 글·요청 머리글·`check_route`·갈래 표·되묻기, 창구 설정 = 02 라우팅 설정과 같은 여섯 칸) + **03 나눠 쓰기**(`write_sections`·`build_part_request`, 갈래 표의 값 = 03 나눠 쓰기 설정). 뺀 것: 01 `run_gated_chain` 통째 · 04·05(요청 수를 모델 답이 정함) · 03 투표 · 06 비교 표·걸린 초·품질 칸.
- 결과(새 커널 두 번 + 노트북 밖 다섯 번 모두 같음): 실행 1(허용 목록 보안·인사·회계) `상태: 완료`·`분류: {'종류': '보안', '신뢰도': 0.99}`·`검사가 찾은 문제: []`·기록 세 줄(`1 | 분류 | 138 | 22`)·`받은 부분 차례: ['적용', '등록']` · 실행 2(보안 뺌) `상태: 되묻기`·`['허용 목록에 없는 종류']`·기록 한 줄 · `분류 요청 입력 토큰 | 실행 1 138 | 실행 2 138` · `줄어든 요청 수: 2` = 보안 갈래 부분 수. 파일 쓰기·자료 읽기 0, 걸린 시간 재지 않음.

## 8. 도구 파일 `notebooks/workflow_tools.py` — 함수 표와 해시 변천

| 함수 | 배운 곳(= 옮긴 절) | 가져오는 절 |
|---|---|---|
| `add_record` · `print_records` · `ask_json` · `check_plan` · `build_write_request` · `run_gated_chain` | 01 | 02·03·04·05·07(`ask_json`·`print_records`) · 06(`run_gated_chain`, 안에서 앞 넷) |
| `check_route` · `route_question` | 02 | 06(`route_question`) · 07(`check_route`) |
| `build_part_request` · `ask_all_together`(async) · `join_parts` · `write_sections`(async) · `count_votes` · `decide_vote` · `run_vote`(async) | 03 | 04(`ask_all_together`·`join_parts`) · 06(`write_sections`) · 07(`build_part_request`·`write_sections`) |
| `pick_tasks` · `build_task_requests` · `build_summary_request` · `find_new_contacts` · `plan_tasks` · `run_orchestrator`(async) | 04 | 06(`run_orchestrator`) |
| `check_length` · `check_draft` · `decide_stop` · `build_notes` · `write_and_judge` · `finish_loop` · `run_write_judge_loop` | 05 | 06(`check_draft`·`run_write_judge_loop`) |
| `total_tokens` · `grade_notice` · `make_row` | 06 | (없음 — 07은 재지 않아 쓰지 않음) |

- 함수 **서른하나**(`async def` 넷), 함수마다 `# Ch 18 NN절에서 배웠습니다 — …`, import `asyncio`·`json`·`re`, 전역 이름 기대기 0, 금지 문법은 03 `ask_all_together`의 `*` 풀기(03이 풂) 하나, 코드 줄 207. 모두 처음 가르친 노트북 셀과 AST 같음(첫 줄 주석만 다름, 01 `ask_json` 안 주석 「4절」↔「01절」 한 줄 — 검토 A·B 확인).
- **해시 변천**: 없음 → 01 `a024ed89…` → 02 `5a80b815…` → 03 `3fb4ed40…` → 04 `f9eade3f…` → 05 `67e9433b…` → 06 **`5a158a68d93a0ece889760e0cb716df5b1c7b54f5709f62a160845792fa92dae`** → 07·마감 그대로.
- 가져오는 절(02~07)마다 고정 세 문장 + 「커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다」가 준비 셀 결과 읽기 [4]에 **한 번씩**(마감 확인 — 한 절 안 두 번 0, A 「사람이 정해야 할 것」 3 → 과정 선례대로 절마다). 묶음 목록 두 곳(`textbook/part5/public-files.json` 7행·챕터 `qa/public-files.json` include)에 있고, 마감 zip을 `/tmp`에 풀어 `notebooks/`에서 가져오기 확인(함수 31, 02~07이 쓰는 이름 모두).
- **Ch 18 전용**입니다. 모양이 SDK 직접 호출이라 Ch 19·20(LangChain)이 가져올 수 없습니다. **Part 6 선행 목록에는 이 파일이 없습니다**(§13).

## 9. 의존성 (`pyproject.toml`·`uv.lock`, 바꾸지 않음)

- `dependencies = ["openai==2.29.0", "python-dotenv==1.2.3"]`, dev `ipykernel==7.3.0`·`nbclient==0.11.0`·`pip==26.2`·`ruff==0.15.6`. 잠금에 `pip 26.2`·`httpx 0.28.1`·`httpcore 1.0.9`. 노트북 `%pip`은 두 패키지(잠금 판). 교재 출력 환경 `.cache/vm/venv-ch18-workflow-patterns`(Python 3.12.13, 잠금과 판 차이 0).
- **Part 5 안 `openai` 판 차이**: Ch 18 **2.29.0**(SDK 직접) ↔ Ch 17·19·20 잠금 **3.11.0**(LangChain이 끌어옴). 잠금은 바꾸지 않았고 01 b7에 한 문장 — 강사 확인.

## 10. 챕터 밖 수정 (전부 목록)

| 파일 | 언제 | 무엇을 |
|---|---|---|
| `labs/part5/ch18-workflow-patterns/{notebooks/01~07-*.ipynb, notebooks/workflow_tools.py}` | 01~07절 · 마감(노트북 마크다운만) | 실습 폴더(챕터 몫) — §1·§8. 마감은 코드·출력 0 변경 |
| `labs/part5/ch18-workflow-patterns/README.md` | 07절(07 단락) · **마감(전체)** | `9a99b203…` → **`7f9ca42b…`**: 노트북 일곱(모두 API 키), `uv sync --locked` → `.venv` → `notebooks/`에서 열기, 모델 설정(`gpt-5.4-mini`·`temperature=0`·`reasoning` none·`json_object`와 요청 글의 「JSON」·기본 클라이언트 다시 보내기 2번), 도구 파일 단락(고정 문장 뜻 + 함수 서른하나·배운 절·`asyncio`·`json`·`re`), 절마다 하는 일, 요청 65번·절별 상한·예상 비용(청구 아님), 06 출력 = Ch 29 04 입력 주의, 07 단락. 묶음에 없는 `qa/research.md`·「`max_output_tokens`와 호출 수를 제한」·「독립적으로 실행」 뺌 |
| `labs/part5/ch18-workflow-patterns/author_notebooks.py` | **마감** | `mv -n` → `textbook/part5/ch18-workflow-patterns/qa/upgrade/before/generators/blocked/`(§14 1번) |
| `textbook/part5/_src/index.html` | **마감** | 7행 「Ch 2의 함수·**타입 힌트**·비동기 실행은 Ch 18의 패턴 구현에 사용합니다」 → 「Ch 2의 함수와 비동기 실행은 …」(Ch 18 노트북·도구 파일 타입힌트 0, 검토 A-15). Part 5 소개 첫 단락의 「분기」(Part 5 마감 몫)는 그대로 |
| `labs/part5/continuity-guide.md` | **마감** | 5행(Ch 18 단락) 끝 문장 「Ch 39에서는 이 정지 조건을 더 큰 반복 작업에 적용합니다」(교재에 없는 챕터) → 「Ch 19에서는 함수를 도구로 만들고, 모델이 도구 설명을 보고 고르게 합니다」(07 b8과 같은 문장, Ch 19 01·03·04 제목과 대조한 것). `5d37b331…` → `59295755…`. 같은 줄의 「동적 작업 분해」는 그대로 |
| `textbook/part5/_build_index.py` | **마감** | ch18 설명 「… 호출 수·사용량·**지연**·품질을 비교합니다」 → 「OpenAI SDK로 다섯 워크플로우 패턴을 직접 만들고, 같은 과제에서 요청 수·토큰 수·걸린 초·품질 칸을 견준 뒤 라우팅 검사와 나눠 쓰기를 잇는 실습을 합니다」(시수 4·12 그대로, 절 수 칸 없음) |
| `textbook/part5/index.html` · `textbook/downloads/part5-practice.zip` · `textbook/part5/qa/integration-results.json` | 07절 + **마감** | `python3 textbook/part5/_build_index.py` → **`Part 5: 23 verified sections; 61 bundled files`**, zip `85dc7299…` → **`fe860153…`**(64항목, Ch 18 열하나 모두 디스크와 같음), `index.html` `ee123cc4…` → `768a6790…`, `integration-results.json` `69cb8c73…` → `60df3c5d…` |
| `textbook/part5/qa/ch18-visual-summary.json` · `textbook/part5/qa/visual-summary.json` | **마감** | ch18 행 14 → **16**(새 결과로), 합 `checks`·`passed` 56 → **58**(다른 챕터 파일 그대로) |
| `textbook/part5/qa/notebook-readiness.json` | **마감(되돌림)** | 옛 `check_notebook_readiness.py`가 멈추기 전에 이 파일을 다시 써서, 실행 전 사본으로 되돌렸습니다(내용 변경 0, `b87e5028…`) |
| `textbook/downloads/part6-practice.zip` · `textbook/part6/qa/integration-results.json` | **마감** | `python3 textbook/part6/_build_index.py` 한 번 → **`Part 6: 48 verified sections; 88 bundled files`**. zip `ca012cae…` → **`696e75ea…`** — 91항목 가운데 바뀐 것은 **06 노트북(`b583e8b4…` 개선 전 → `5ba7f5a0…`)과 `manifest.json` 둘뿐**. `integration-results.json` `a9255457…` → `967ce8df…`(`bundle_sha256` 칸). `textbook/part6/index.html`(`a606f921…`)과 나머지 `textbook/part6/qa/*.json`은 그대로 |
| `textbook/part6/qa/final-artifact-hashes.json` | **마감** | 이 파일을 만드는 스크립트가 없어(`grep` 0) 353행 ch18 06 노트북 한 줄만 `7bd4a20d…` → `5ba7f5a0…`(파일 `5b946cc5…` → `19ac9457…`). 같은 파일의 Ch 29 04 줄은 고치지 않음 |
| `textbook/_notebook/checks/notebook-contracts-part5-ch18-workflow-patterns.json` | 절마다·마감 | `verify.py --chapter`가 다시 씀 |
| `textbook/_notebook/checks/ch18-workflow-patterns/visual-results.json`(+ 스크린숏 넷) | **마감** | `visual.cjs` 16행(`NODE_PATH=/tmp/pw/node_modules` shim) |
| `textbook/qa/upgrade-progress.md` · `textbook/qa/upgrade-final-checklist.md` | **마감** | Ch 18 행 한 줄 · §2-7 Ch 18 항목과 §3·§4 Ch 18 줄 |

- **고치지 않은 것**: `textbook/QUALITY-UPGRADE.md`·`PLAYBOOK.md`·과정 요약·계약 파일, 공용 도구 코드(`nbkit.py`·`mdpatch.py`·`run_section.sh`·게이트·`verify.py`·`visual.cjs`·`execute.py`·`build_bundle.py`·`render_mermaid.py`), Part 5·6 옛 검사 스크립트, `textbook/_notebook/build_index.py` 40~41행(Ch 18 설명 「… 호출 수·사용량·지연·품질」·절 수 6 — 전체 목차 마감 몫), **Ch 19 이후 파일 전부**(Ch 29 04 `_src`·노트북, Part 6 선행 목록 둘 포함), 보호 파일 15개.
- **파일을 지운 것은 없습니다.** 옛 생성기 셋만 `mv -n`으로 옮겼습니다. 마감이 새로 만든 파일: `chapter-summary.md`(이 파일) · `gates-after.json` · **`gates-closecheck.json`**(G6 확인 중 `--label closecheck`로 한 번 만든 중간 보고 — 삭제 승인 대상) · `before/generators/blocked/` 셋(옮긴 것).

## 11. 기준 버전·확인 날짜

- 실습 폴더 잠금: `openai 2.29.0` · `python-dotenv 1.2.3` · `httpx 0.28.1`, dev `ipykernel 7.3.0`·`nbclient 0.11.0`·`pip 26.2`·`ruff 0.15.6`. **교재 출력 환경 = 잠금 판**.
- 교재 출력: Linux aarch64 · Python **3.12.13** · 모델 `gpt-5.4-mini`(응답 모델 `gpt-5.4-mini-2026-03-17`, `temperature=0`·`reasoning={"effort": "none"}`). 실행일 모두 2026-09-23(01 19:32 · 02 19:57 · 03 20:28 · 04 20:58 · 05 21:29 · 06 22:07 · 07 22:41 UTC).
- 참고 자료(2026-09-23 확인): Anthropic 「Building effective agents」(워크플로우 다섯 모양·「maximum number of iterations」은 Agents 절) · openai-python 저장소(설치판 소스로 인자·다시 보내기 기본값) · GPT-5.4 mini 모델 문서(요금) · Python 3.12 문서 `asyncio`(gather 차례·to_thread)·`re`·`time.perf_counter`·**Library and Extension FAQ**(목록 `append`, 마감에서 03 b10에 더함) · httpx API 문서·Discussion #1633.

## 12. 강사 확인 대상

1. **제목 말**: 01 「프롬프트 체이닝」·03 「병렬 섹셔닝」·04 「동적 오케스트레이터와 워커」·05 「생성자 평가자」를 두고 본문에서 한 번씩 풂(03 「병렬」은 마감에서 풂).
2. **07 슬러그·제목**(검토 B 「사람이 정해야 할 것」 1): `07-워크플로우-패턴-실습` / 제안 `07-워크플로우-5패턴-실습`. 바꾸면 파일 넷·`chapter.json`·생성기 상수·목차·zip이 함께 바뀝니다.
3. **흔들린 값에서 끌어낸 비교의 적용 범위**(A 「사람이 정해야 할 것」 1 → 챕터 리드 결정): 03 걸린 초·도착 차례 비교와 06 토큰 수 차례는 결론·그림·정리에서 뺐습니다. 05 첫 바퀴 「점수 ≥ 85 · 150자보다 짧음」은 검토 B 판정대로 두었습니다(§6).
4. **04 과제 글(B-1)과 10절 종합 머리글(B-2)**: 문장만 덧붙이고 04는 다시 실행하지 않음(과제 글이 작업 수를 사실상 정함 · 종합 요청 글에 과제 글 없음을 사실대로). 과제 글을 바꾸거나 종합 머리글에 과제 글을 넣으려면 04 재실행.
5. **06 비교의 공정성·「품질 칸」 말**(B 「사람이 정해야 할 것」 4·5): 나눠 쓰기는 과제 글을 받지 않고 한 문장씩, 작업 나눠 맡기기는 종합 머리글에만 과제 글 — b7에 밝힘. 품질 칸 = 코드 검사, Ch 29 04 「최종 품질」 표현과 함께.
6. **탐색으로 고른 입력**(02 배송 문의 · 04 B2/B1 · 05 150~170자 · 06 120~180자 · 07 실행 2 허용 목록) — 모두 실행 전 후보 둘 안에서, b7에 밝힘.
7. **`openai` 판 차이**(Ch 18 2.29.0 ↔ Ch 17·19·20 3.11.0) · `json_object`(SDK 설명상 옛 방법)를 쓰고 `json_schema`는 쓰지 않은 것 · 기본 클라이언트(다시 보내기 2번).
8. **06·07 코드 셀 주석 「01~0N절과 같은 …」**(검토 B-7): 결과 읽기에서 한 문장으로 바로잡고 코드·생성기 주석은 그대로 — 다음 재실행 때 고칠 것.
9. **Part 6 묶음의 06 노트북**(B-15): 새 06을 넣었지만 `workflow_tools.py`는 Part 6 선행 목록(보호 파일)에 없어, Part 6 묶음에서 06을 실행하면 첫 가져오기 셀이 `ModuleNotFoundError`로 멈춥니다. Ch 29 04는 저장 출력만 읽어 계약에는 문제없음. 선행 목록에 넣을지, 「06은 Ch 29가 읽는 기록」으로만 둘지 결정.
10. **`chapter.json` 학습 목표 셋 → 다섯**(01·02 한 줄, 03, 04·05 한 줄, 06, 07 실습 — 「동점·빈 응답」·「지연」 뺌), `hours` 그대로 16h(01~06 meta 합) · 실습 폴더 README 다시 쓴 범위.
11. **코드 줄 증가**(01 85 → 148 · 02 85 → 149 · 03 100 → 187 · 04 83 → 175 · 05 86 → 183 · 06 144 → 202 · 07 새 128, + 도구 파일 207) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘(A 「사람이 정해야 할 것」 2).
12. 절별: 01 Before 요청 글·요청 6번 · 02 Before 셀의 `try`와 빨강·종류 이름 한국어 · 03 걸린 시간을 잰 절·후보 글 손으로·차례 바꾸기 검사 안 함·A를 먼저 보는 `decide_vote` · 04 흐름 함수 멈춤 갈래 실행 안 함·계획 모델 = 계획 + 종합 · 05 셋째 정지 조건(개선 폭) 뺌·10절 멈춘 까닭이 실행마다 다름 · 06 표의 영어 칸·05 품질 5는 구조 · 07 인사·회계 갈래가 같은 공통 사실을 받는 모양·요청 4번.
13. 삽화 일곱 장의 「그림만 보고 관계가 읽히는가」(07 물레가 받침대 없는 둥근 판) · 한국어 감사 3단(별도 세션).

## 13. 뒤 챕터 인계

### Ch 19 모델과 도구가 이어받을 것

- 말: 「라우팅」(모델이 쓴 종류 이름을 코드가 갈래 표에서 찾는 모양 — **Ch 17 01 규칙으로 워크플로우**) · 「갈래」(「분기」 대신) · 「되묻기」 · 「허용 목록」 · 「기준값」 · 「게이트」 · 「지시 글(instructions)」·「요청 글」·「머리글」 · 「함께 보내기」 · 「바퀴 한도」 · 「코드 검사」 · 「기록 줄」(요청 한 번 = 한 줄) · 「예상 비용」(Ch 6 06 뜻).
- 결론 방향: 다섯 흐름과 07 조립 모두 **다음 단계를 고른 쪽은 코드**입니다. 모델은 JSON 글(종류·작업 목록·초안·점수·표)만 썼습니다. 07 b8·노트북 정리 끝 줄 「Ch 19에서는 함수를 도구로 만들고, 모델이 도구 설명을 보고 고르게 합니다」가 Ch 19로 넘기는 문장입니다(Ch 19 01·03·04 제목과 대조).

### Ch 19가 전제하면 안 되는 것

- **도구 호출 API는 Ch 18에서 가르치지 않았습니다**: `bind_tools`·`@tool`·`ToolNode`·`tool_calls`·함수 스키마. Ch 18의 모델 요청은 모두 OpenAI SDK `client.responses.create` + `json_object`이고, 모델이 도구를 고른 적이 없습니다. 「라우팅」은 모델이 도구를 고르는 것이 아닙니다 — Ch 19 04 「설명만으로 도구 선택하기」와 가르세요.
- **Ch 18은 LangChain을 쓰지 않습니다**(잠금 `openai 2.29.0`, Ch 19는 3.11.0). `workflow_tools.py`는 Ch 19가 가져올 수 없습니다.
- **쓰지 않은 것**: `json_schema`·`AsyncOpenAI`·Pydantic 스키마(Ch 19 02가 처음 쓰면 풀어야 함) · 타입힌트 · `try`는 02 Before 한 번 · 서비스 오류·SDK 다시 보내기·`JSONDecodeError`를 본 장면 0 · 걸린 초는 03·06만(분포 없음) · 노트북에서 비용 셈 0(`estimate_cost` 안 옮김) · 답 품질 판정 0.
- **「병렬」**: Ch 18 본문 말은 「함께 보내기」(03 제목에만 「병렬」). Ch 19 05 「bind_tools와 병렬 호출」의 「병렬」은 도구 호출 뜻이라 Ch 18 03과 다르다고 한 문장 두면 이어집니다.
- **모델 답의 흔들림**: 07 분류는 밖 10/10·두 번 4/4 같았지만 「항상」이라 쓰지 마세요(02 배송 문의 종류는 밖 10번 중 결제 8·기술 2). 04 작업 수·05 바퀴 수는 과제 글에 따라 달라집니다.

### Ch 20·29·34 인계 (그 챕터 몫 — 이 마감은 고치지 않음)

- **Ch 29 04 (Part 6, 보호 파일 — 고치지 않음)**: 06 노트북 저장 출력을 cell 8·10·16 읽기 코드로 흉내 내 **통과**(표 행 5 · 여섯 칸 · `int`·`float` 변환 · `status` 다섯 `ok`). 평균 넷이 바뀝니다 — `textbook/part6/ch29-agent-evaluation/_src/04-운영-지표와-Ch18-궤적-비교.html` **6·7·9행**(같은 문장 세 곳) 「0.88, 모델 2.8회, 610.2토큰, 4.145초」 → 지금 06 출력으로는 **0.96 · 2.8 · 862.2 · 4.206**. 노트북 `labs/part6/ch29-agent-evaluation/notebooks/04-운영-지표와-Ch18-궤적-비교.ipynb` 저장 출력 cell 8(`Ch18 실제 표 행: 6` → 새 06으로는 5)·cell 10·16도 옛 표와 옛 평균입니다. **품질 칸 뜻이 바뀌었습니다**: 새 06의 `quality/5`는 코드 검사 다섯 항목(글자 수 120~180자 + 꼭 담을 말 넷) — 평가 모델 점수가 아닙니다. Ch 29 b2 「최종 품질과 실행 비용」의 「최종 품질」이 이 뜻보다 넓게 읽힙니다. 06을 다시 실행하면 평균이 또 바뀌니 **06은 재실행 금지**를 이어 주세요. `part6-practice.zip`에는 새 06이 들어갔지만 `workflow_tools.py`는 없습니다(§12 9번).
- **Ch 20** `textbook/part5/ch20-tool-node/_src/01-ToolNode와-tools-condition.html` 3행·`04-if-분기와-모델-선택-비교.html` 4행 「Ch18에서는 OpenAI SDK를 직접 호출하고 코드로 단계·**분기**·**병렬** 실행과 종료를 연결했습니다」 — 뜻은 참(함께 보내기·정지 판정). 말은 Ch 18 본문(「갈래」·「함께 보내기」)과 다릅니다.
- **Ch 34** `textbook/part7/ch34-cost-rate-limits/_src/03-모델-라우팅.html` 4행 「Ch 18에서는 코드가 **분기**를 고르는 라우팅 패턴을 구현했습니다」 — 뜻은 참(모델이 종류를 쓰고 코드가 갈래를 고름). 「분기」 → 「갈래」는 그 챕터 몫.
- Ch 17 요약 §13이 넘긴 Ch 18 04 b3 「얼마나」는 04절 개선에서 해소했습니다(「누가 다음 단계를 골랐는지」로).

## 14. 남은 것 (전체 마감 몫 — `textbook/qa/upgrade-final-checklist.md` §2-7)

1. **옛 생성기 셋은 옮겼습니다(삭제 아님, 2026-09-23 완료)**: `textbook/part5/ch18-workflow-patterns/_author.py`(`69d4c684…`)·`labs/part5/ch18-workflow-patterns/author_notebooks.py`(`f9019b10…`)·`figures/_gen_figures.py`(`29aa1214…`, 모두 01절이 `raise SystemExit`로 막은 판) → `qa/upgrade/before/generators/blocked/`(원본 사본은 `before/generators/`, 옮기기 전후 해시 같음). 부르는 스크립트 없음(`grep` — 이름은 챕터 `qa/public-files.json` 제외 목록 글뿐), 옮긴 뒤 `_build.py` HTML 여덟 개 해시 같음.
2. **옛 그림 열여덟 삭제 승인**: `figures/0N-흐름.{svg,excalidraw,caption.md}`(01~06절 각 셋, 본문 참조 0, 사본 `qa/upgrade/before/figures/`). 지우면 `textbook/part5/qa/check_figures.py`로 `figure-consistency.json` ch18 줄을 다시 씀(지금은 Ch 17 `01-1`에서 먼저 멈춤).
3. **`gates-wip-*.json` 열넷 + `gates-closecheck.json` 삭제 승인**(`gates-after.json` 7/7로 갈음).
4. **06·07 코드 셀 주석 「01~05절/01~06절과 같은 …」**: 다음에 06·07을 다시 실행할 때 `author_06.py`·`author_07.py`의 주석을 「03~0N절과 같은 …」으로 고칠 것(06은 Ch 29 계약 — 다시 실행하면 §13 평균 넷을 다시 셈).
5. **Part 5 옛 검사 스크립트 넷(고치지 않음, 마감에서 돌려 본 결과)**: `check_scope.py` — Ch 17 `06-Agent-개요-실습.html` meta 「실습 30분」에서 `Missing scope`(Ch 18 07도 같은 모양, `SECTION_COUNTS` ch18 = 6 ≠ 7) · `finalize_evidence.py` — Ch 18 `_src/01-게이트가-있는-프롬프트-체이닝.html` 감사 해시(2026-09-14)에서 멈춤 · `check_figures.py` — Ch 17 `01-1-고른-쪽으로-가르기.svg`의 `.excalidraw` 짝 요구에서 멈춤 · `check_notebook_readiness.py` — `assert len(reports) == 21`(지금 Part 5 노트북 23)에서 멈춤, **결과 파일을 먼저 씀 → 되돌림**. `check_bundle_execution.py`는 ch18을 다루지 않습니다(묶음 실행 검사 대상 아님 — zip을 풀어 도구 파일 가져오기만 확인).
6. **`llm-practice.zip`**: Part 1부터 낡음. Part 5·6 `check_delivery.py` 모두 **`Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`**(Part 5 115행 · Part 6 117행)에서 멈춤. 스크립트 사본에서 `llm-practice.zip`만 빼고 결과 파일 없이 돌리면 **Part 5**: HTML 29 · 링크 447 · 누락 0 · 복습 오류 0 · 비밀값 0 · `part5-practice.zip` 64항목 대조 통과(part5 노트북 23) / **Part 6**: HTML 59 · 링크 877 · 누락 0 · 복습 오류 0 · 비밀값 0 · `part6-practice.zip` 91항목 대조 통과(part6 노트북 48).
7. **`textbook/_notebook/build_index.py` 40~41행**(Ch 18 설명 「… 호출 수·사용량·**지연**·품질을 비교합니다」, 절 수 6은 실습 절 뺀 수) — 전체 목차 마감 때 `textbook/part5/_build_index.py` 새 문장과 맞출 것.
8. **`qa/research.md`**(2026-09-10 조사·옛 비용 계획 — 「추정 비용」·`max_output_tokens` 상한)와 `qa/verification.md` 위쪽 옛 줄: 학생 묶음 밖 기록이라 그대로(「개선 전 판」 표시). 지울지 전체 마감 때.
9. **Part 6 `workflow_tools.py` 선행 목록**(§12 9번) · **Ch 29 04 평균 넷·품질 칸 뜻**(§13) — Ch 29 작업자 몫.
10. **삭제 승인 대상(캐시·임시)**: `labs/part5/ch18-workflow-patterns/.venv`(macOS 판 135MB)·`.ruff_cache` · `__pycache__` 넷(`labs/…/`·`notebooks/`·`textbook/…/qa/upgrade/`·`qa/upgrade/probe/`) · `.cache/ch18-01-view`~`ch18-07-view` · `.cache/ch18-close`(마감 전 사본·확인 스크립트·그림 확인 사본·옛 검사 로그) · `.cache/vm/venv-ch18-workflow-patterns`(178MB) · 기기 `/tmp/ch18-01`~`/tmp/ch18-07`·`/tmp/ch18-0N-probe-*.txt`·`/tmp/ch18-03-words.py`·`/tmp/ch18-04-*`·`/tmp/ch18-prep`·`/tmp/ch18-close-bundle`·`/tmp/reviewA18`·`/tmp/reviewB18`.
11. **2차 검토**: 검토 둘의 「확인하지 못한 것」(삽화 판독, 한국어 감사 3단)과 §12.

## 15. 검토 1차와 반영 (2026-09-23 마감)

- 판정: **A(01~03·공통) 중 2 · 하 14**, **B(04~07) 중 4 · 하 13**(모두 accept with fixes/조건부 통과, reject 0). A 요약 표의 하 14는 번호 붙은 항목 열셋(A-2~A-10·A-12~A-15)에 해당하며 A-15가 기록 넷을 묶습니다.
- **[중] 6건 반영**: A-1(01 `and` 풀이, 02 `KeyError`와 이음) · A-11·B-14(README 전체) · B-1(04 과제 글이 작업 수를 사실상 정함) · B-2(04 종합 요청 글에 과제 글 없음, 06과 대비) · B-7(05·06·07 공통 사실 「03절부터」, 06·07 코드 주석은 결과 읽기에서 바로잡음) · B-10(06 b6 두 번 달랐던 값을 표와 맞춤).
- **[하] 반영**: A-2(01 「게이트 세 줄과 마지막 줄의 칸 「문제」」, `01-3`) · A-3(01 SDK 풀이) · A-4(01 「JSON」은 요청 글에서, handoff 47행) · A-5(02 Ch 17 01 사실대로) · A-6(02 설계표 빨강 사유) · A-7(03 「병렬」 풀기) · A-8(03 `gather` 셀 다시 실행 안내) · A-9(03 `append` 근거, b7·b10) · A-10(03-2·흔들린 값 비교 — 03-3·b6·b8·정리까지) · A-12·B-5(01~05 비용 문장) · A-13(01 기록 한 줄 뜻 · 03 칸 「단계」) · A-14(`pack.py` 01~07 다시) · A-15(Part 5 소개 7행 고침 · objectives 고침 · Ch 20·34 문장과 옛 그림은 §13·§14에 기록) · B-3(04-3 공통 상자) · B-4(04 `False` 풀이) · B-6(04·05 「고른 쪽」, 01~07 같은 기준) · B-8(05-1 색) · B-9(05 평가 모델 판단 미확인) · B-11(06 조건·「확인할 점」) · B-12(06 백틱) · B-13(07 「새 커널 두 번」) · B-15(Part 6 묶음 다시 만듦) · B-16(objectives·`_build_index.py`) · B-17(§13 인계).
- **미반영(부분)**: **B-15의 「`workflow_tools.py`를 Part 6 선행 목록에 넣기」** — `textbook/part6/prerequisite-files.json`·Ch 29 `qa/prerequisite-files.json`이 보호 파일이고 Ch 29 이후 파일이라 고치지 않고 강사 확인(§12 9번)으로. **B-7의 06·07 코드 셀 주석** — 고치면 `code_sha256`이 바뀌고 06은 Ch 29 계약이라 결과 읽기 문장으로 갈음(§14 4번). **B-2의 「04 종합 머리글에 과제 글을 넣고 다시 실행」 갈래·B-1의 「과제 글 바꾸기」 갈래** — 04는 다시 실행하지 않는다는 챕터 리드 결정대로 문장만(§12 4번). **05 첫 바퀴 판정의 흔들린 값 비교**는 검토 B 판정대로 두고 강사 확인(§12 3번). 검토의 「사람이 정해야 할 것」(07 슬러그·코드 줄·06 공정성·탐색 입력)은 결정하지 않고 §12에 올림.
- **노트북 해시 전후**(`code_sha256` / `outputs_sha256`, 앞 12자, 모두 그대로): 01 `59dc63e1ad01`/`0648caf5eda2` · 02 `131bfefdf7fa`/`9d513ff82008` · 03 `6b0b093c85f9`/`80f57237f0fb` · 04 `139e85bb40a0`/`535067a66d5a` · 05 `5105ffa21a98`/`225de9dfb60b` · 06 `f37b5df47a1a`/`ecb0d885b86c` · 07 `601c4110c6b8`/`a5745346607e`. 일곱 노트북 모두 `metadata.verification`과 계산값이 같고, 셀별로 바뀐 것은 마크다운뿐(01 일곱 · 02 둘 · 03 다섯 · 04 여섯 · 05 넷(+ `05-1` 첨부 PNG) · 06 넷 · 07 둘), 코드 셀·출력·노트북 메타데이터 0. 노트북 파일 해시는 마크다운 때문에 바뀜(06 `c7740afa…` → `5ba7f5a0…`).
- **06 Ch 29 계약 재확인**: Ch 29 04 cell 8·10·16 읽기 코드를 파이썬으로 흉내 → `Ch18 실제 표 행: 5` · 마지막 다섯 줄 여섯 칸 · `ok` 다섯 · 평균 `0.96 / 2.8 / 862.2 / 4.206` · PASS.
- 고친 방법: 생성기·노트북 마크다운·`_src`를 `mdpatch.py`로 같이(적용 전 대조 스크립트로 코드 셀 0회·생성기 횟수 확인) → `run_section.sh … NN --no-exec` 일곱 번 · `.mmd` **다섯 장** 다시 렌더(`01-3`·`03-2`·`03-3`·`04-3`·`05-1`, `--force`, `03-3`·`04-3`은 라벨 꺾임으로 두 번), **모두 PNG를 다른 이름으로 복사해 직접 열어 도식 읽기와 맞는 것을 확인** · 노트북 첨부 새 PNG 하나(`05-1`) · 캡션 파일 둘(`03-3`·`04-3`)을 `_src` 캡션과 같게 · `_build.py`. 마감 뒤 생성기 `author_01~07.py`의 `cells()`(paired 경계 나누기 포함)·`SRC_HTML`이 노트북·`_src`와 글자까지 같음(7/7), 금지어 셈은 마감 전과 같음(03 「병렬」 +2 = 풀이 둘).

## 마감 뒤 보완 (2026-09-23, 챕터 리드)

- §8·§12 9번의 「Part 6 선행 목록에 도구 파일 없음」은 마감 직후 해소했습니다. `workflow_tools.py`를 `textbook/part6/prerequisite-files.json`·`textbook/part6/ch29-agent-evaluation/qa/prerequisite-files.json`에 더하고 `final-artifact-hashes.json`에 해시 줄을 넣은 뒤 `part6-practice.zip`을 다시 만들었습니다(`dacb688e…`, 89파일). 자세한 기록은 `handoff.md` 끝 「마감 뒤 챕터 리드 보완」.
