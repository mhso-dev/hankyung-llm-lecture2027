# 07절 진단과 기록 — create_agent 실습 (챕터 끝 실습 절, 새로 만듦)

- 대상(새 파일): `_src/07-create-agent-실습.html` · `labs/part6/ch21-create-agent/notebooks/07-create-agent-실습.ipynb` · 그림 `figures/07-1`~`07-4` · 빌드 `07-create-agent-실습.html`.
- 생성기: `qa/upgrade/author_07.py`(노트북 + `_src`, `f1247c72…` — 설명 채움 뒤 판은 아래 §11). 흔들림 확인: `qa/upgrade/07-probe.md` · `probe/probe07.py`(`353dd545…`) · 기록 `probe/probe-07.jsonl`(`c4d6bd62…`). 그림 설계표: `qa/upgrade/07-figures.md`. 검토 묶음: `qa/upgrade/review-pack/07-create-agent-실습.md`.
- 작업일 2026-09-25(UTC 05:3x~06:0x). 슬러그 **`07-create-agent-실습`**(규격 §7-2 `{NN}-{챕터 이름}-실습`, 선례 `05-ToolNode-실습`·`07-모델과-도구-실습`·`09-Middleware-실습` — 챕터 제목 앞말, 01 슬러그처럼 밑줄은 줄표). 제목 「create_agent 실습: 대출 문의 에이전트에 양식과 실행 정보 붙이기」, `format: experiment`, meta 「실습 30분 | … | 새 용어 0」, **`hours` 「총 16h · 강의 6h · 실습 10h」 그대로**.

## 1. 게이트

| | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전 | — (새 절) | | | | | | | | | |
| 첫 실행 전 (`/tmp/ch21-07/gates-wip-07-07.first.json`, 생성기만 돌린 판) | 24 | 315 | **0** | **0** | 0 | 0 | 0 | 4 | 14 | — |
| 후 (`gates-wip-07.json`·`gates-wip-07-07.json`) | **24** | **343** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G1·G2 **0**. G6 4 = 70자 넘는 정리 문장 둘(노트북·`_src` 같은 문장)·기준 버전 한 줄·「numpy는」으로 시작하는 문장 → 실행 전에 고침(고친 뒤 기준 버전 단락이 여섯 문장이 되어 한 번 더 나눔). G7 14 = 그림·설계표가 없던 때.
- 챕터 전체(`gates-wip-ch21-after07.json`): **01~07 일곱 절 모두 PASS**(G1~G7 0).
- AST 따로(`/tmp/ch21-07/extra_check.py` — 06절 판 그대로): 노트북 **위반 0건**, 허용 표시 1건 = `ToolRuntime[MemberContext]`(03절 셀 그대로). 클래스 둘은 칸만 적은 `TypedDict`(03절 셀)·`BaseModel`(칸 둘 `Field(description=)`) · 데코레이터는 맨 `@tool` 둘(01·03절 셀) · 힌트는 `topic: str`·`runtime: ToolRuntime[MemberContext]`(앞 절 셀 그대로) · f-string·내포식·제너레이터 식·`lambda`·조건 표현식·기본값·튜플 풀기·`elif`·`+=`·`next`·`sum`·`set`·`.get`·세미콜론·`try` 0 · 호출 안 호출 안 호출 0. 이 절이 정의한 평범한 함수 0.
- **01~06에서 쓰지 않은 이름 대조**(`/tmp/ch21-07/names_check.py` — 07 코드 셀의 이름·속성·키워드 인자·import를 01~06 노트북 코드 셀 전체와 대조): 내장 이름 0 · 키워드 인자 0 · import 0 · 속성 둘 = `can_borrow`·`answer`(이 절 양식 클래스의 칸 이름 — 02절 `.topic`과 같은 칸 읽기). 새 문법·새 API·새 말 **0**.
- 셀 모양: 코드 셀 **24**(준비 셋: 설치·가져오기·키), 준비 셀이 아닌 셀의 주석 뺀 코드 최대 **10줄**(5절 `AGENT`), 함수 본문 최대 5줄(`check_my_loan`, 03절 셀), 셀당 정의 하나, 첫 줄 주석 100%.
- 금지어(`/tmp/ch21-07/ban_check.py` — 06절 판): 노트북·`_src`·`.mmd` 셋·캡션 넷에서 걸린 것은 「캐시 입력」 한 곳(허용 말)뿐. 「한 겹 더」 0건. 빌드 HTML `{{` 0건.

## 2. 설계 — 붙인 기능과 뺀 것 (규격 §7-2 1번, 인계 「§06 → 실습(07)」 6항)

| 절 | 붙인 기능 | 흐름 안에서 쓰였는가(코드로 센 값) |
|---|---|---|
| 01 | `create_agent(model, tools=[…], system_prompt=…)` · `POLICIES`·`lookup_policy`(셀 글자 그대로) · 시스템 메시지 글 앞 두 문장 · `agent_row` | **쓰임** — 두 실행 모두 첫 응답 `['check_my_loan', 'lookup_policy']`, `lookup_policy` 인자 `{'topic': '대출'}`, 도구 메시지 `success`(`lookup_policy \| 두 실행의 글이 같은가: True`) |
| 02 | 양식 클래스(`BaseModel`·`Field`·`Literal`, `LoanAnswer`) + 도구 전략 `ToolStrategy` → 칸 `structured_response` · `print_branches` | **쓰임** — 둘째 응답 `['LoanAnswer']`, `structured_response의 종류: LoanAnswer`, `정해 둔 두 값 안인가: True`(두 실행), 결과 키 `['messages', 'structured_response']` |
| 03 | `context_schema=MemberContext` · `check_my_loan(runtime: ToolRuntime[MemberContext])`(셀 글자 그대로) · `invoke(…, context=…)` | **쓰임** — 도구 메시지 `이용자 M-0317: 연체가 없어 …` / `… 연체 3일. 연체한 일수만큼 …`, `check_my_loan \| 두 실행의 글이 같은가: False` |

- **값 하나만 바꿈**: 실행 정보의 `overdue_days` 0 → 3(**03절 8절 값 바꿔 보기와 같은 값**) — 그래서 b2·노트북 7절 앞에 「새로 볼 것은 바뀐 도구 메시지가 양식의 칸 값까지 이어지는지」 한 문장. 03은 도구 메시지까지만 보였고, 07은 그 글이 모델이 채우는 양식 칸 `can_borrow`(가능 → 불가)까지 이어지는 것을 보이고, 도구 몸통과 같은 규칙으로 코드가 정한 값과 견줌(8절 `RULE_CHECK`, `assert` 없음).
- **문의 글**(이 절에서 새로 정함, 출력 줄 「문의 출처」): 「제가 지금 새 책을 빌릴 수 있는지 확인해 주세요. 일반 도서 대출 규정도 함께 알려 주세요.」 — 두 도구가 모두 있어야 답할 수 있게 해 세 부품이 한 흐름에서 모두 쓰이게 함(Ch 20 리뷰 B-8 교훈 — 붙이기만 한 부품 없음). 이용자 번호·연체 일수는 03절 7·8절 값 그대로(출력 줄 「출처」).
- **양식 클래스를 새로 적은 까닭**: 02절 `PolicyAnswer`는 주제어 칸 `topic`과 답 칸이라, 이번 문의의 결과(새 대출 가능 여부)를 담을 칸이 없음. 같은 모양(`BaseModel` 하나, `Field(description=)` 칸 둘 — 생성기 `check_same_as_before()`가 AST로 대조)으로 칸만 바꿈. 주제어 칸을 두면 실행 2에서 모델이 대출/연체 가운데 무엇을 적을지가 흔들려 결론에 쓸 수 없음.
- **도구 전략을 고른 까닭**: 인계 권고(02 도구 전략) + 양식 값이 도구 호출 요청으로 메시지 칸에 남아 흐름 전체를 메시지 칸에서 셀 수 있음. 제공자 전략·양식 클래스 그대로는 **뺌**(02절 비교 되풀이).
- **뺀 것**(b3 둘째 단락): 03 상태 칸 더하기(부품 넷 — 규칙 2~3개 넘음, 문의 처리에 쓰이지 않음) · 04 옛 함수(붙일 부품 아님, 모델 요청 없는 절) · 05 검색 도구(문서 벡터 1 + 검색마다 임베딩 1 → 3~5번 넘기 쉬움) · 06 평가·**계약 파일 `data/rag-comparison.json`(읽지도 쓰지도 않음 — 노트북·본문·README에 밝힘)**. 06 b7 「실행하지 않음」(검색 안 하는 질문·다시 검색·도구 오류 등)은 새로 풀지 않음.
- 시스템 메시지 글 = 01 글 + 빈칸 + 03 글의 둘째 문장(생성기가 문자열로 대조, 흔들림 확인과도 대조).

## 3. 흔들림 확인 (규격 §7-2 6번 — `07-probe.md`)

- 모델 없는 확인 먼저(요청 0, 가짜 키 글자 — `/tmp/ch21-07/nomodel_check.py`): 그래프 모양·도구 명세·양식 모양.
- 규칙(후보 A·B, 판단 넷)을 §0에 먼저 적고(05:36Z) 첫 요청 05:36:37Z. **후보 A 두 설정 × 다섯 번 = 20요청**.
- **10/10 같음**: 메시지 여섯 · 첫 응답 두 도구(`check_my_loan {}`·`lookup_policy {'topic': '대출'}`) · 둘째 응답 `LoanAnswer` 하나 · 응답 2 · 도구 메시지 셋 · 호출 ID 짝 · `LoanAnswer` · `can_borrow` R0 「가능」 5/5 · R3 「불가」 5/5 · 입력 토큰 336·440 / 336·448 · 첫 출력 47.
- 흔들림: `answer` 칸 글(앞머리·연체 규정 덧붙임) · 둘째 출력 토큰(R0 57~59, R3 61~75).
- **판단**: A가 규칙 넷(양식 값 · 두 도구 · 양식 도구 따로 · 요청 2 + 2 = 4)을 모두 채움 → A 그대로(**탐색으로 고른 입력 아님**, 후보 B는 보내지 않음). b7에 과정·후보 B가 무엇이었는지 적음.

## 4. 새 커널 두 번 (규격 §2-7 9번 끝 — 그림 그리기 전)

- **A** `run_section.sh`(셀 실행 기록 05:48:21.6~27.5Z, 약 6초 → 준비물 「10초 안에」). 첫 호출은 그림 PNG가 없어 `attach_figures.py`에서 멈춤(실행·저장은 끝난 뒤 — 이후 `--no-exec`로 첨부·빌드·verify·게이트).
- **B** 사본 `/tmp/ch21-07/B.ipynb`를 `execute.py`로(05:48:54.7~49:00.8Z, 키는 루트 `.env`를 `execute.py` 기본 작업 폴더에서 읽음 — 출력·저장 없음). 이 절은 파일을 쓰지 않아 B가 교재 파일을 건드릴 일이 없음.
- `code_sha256` `bf48d2353026…` 둘 다 · **셀별 출력 글자 24/24 같음** · `outputs_sha256` 둘 다 `7f670216e9960677…`(답 칸 글·출력 토큰까지 같았음). 교재 출력 = A.
- 설명만 채운 두 번(`mdpatch.py` — `/tmp/ch21-07/reps1.json` 그림 alt·읽기 여덟과 결과 읽기 둘째 단락 다섯·b6 한 문장 / `reps2.json` b4 비유 한 문장)은 노트북 코드·출력 그대로(A와 24/24 같음 확인). 생성기 `cells()`가 지금 노트북의 셀 53개 글을 그대로 다시 만들고, `src_html()`이 지금 `_src`와 같음(대조함).

## 5. 결정적 값과 흔들린 값의 자리

| 값 | 성격 | 둔 자리 |
|---|---|---|
| 그래프 노드·조건 함수·상태 칸 · 결과 키 · 메시지 수 6 · 응답마다 요청 이름 · 모델 요청 2·2 · 도구 메시지 3·3 · 호출 ID 짝 · 두 도구의 도구 메시지 글 · `LoanAnswer`·두 값 안 | 코드 또는 모델 선택(밖 10/10·A·B 같음) | 첫 단락·결론·그림·정리·복습 |
| `can_borrow` 가능·불가 · 규칙 값과 같음 | 모델이 채운 칸(밖 10/10·A·B 같음) | 첫 단락·b6(「모델이 채운 칸이라 늘 그렇다고 보장할 수 없다」와 함께)·그림 07-2·07-3(「모델이 채운 양식 칸」 라벨)·정리 3 |
| 입력 토큰 776·784 | 밖 5/5·A·B 같음 | 결과 읽기 첫 단락·b6 표 |
| 답 칸 글 · 「3일간」(모델이 끌어낸 말) · 출력 토큰 104·117 · 예상 비용 0.00105·0.001115 | 모델 글·흔들림(밖에서 달랐음) | 결과 읽기 둘째 단락(「이번 실행에서는」)·b7만 |

## 6. 그림

- Mermaid **3장**(규격 §7-2 그림 = 조립도 · 실행 1 실제 순서 · 실행 1·2 비교): `07-1` flowchart TB 상자 일곱 699.8 · `07-2` sequenceDiagram 세로선 셋·`box Lavender` 하나·`messageAlign: left` **865**(첫 렌더 895 → 메모를 줄 나눠 줄임) · `07-3` flowchart TB + subgraph 둘 + 공통 회색 `~~~` 694.4 — **모두 868 이하, 빨강 0**, 보라는 07-2 모델 노드 띠 하나. PNG 셋을 직접 열어 봄(`.cache/ch21-07-view/`) — 07-3 저절로 꺾인 라벨(맨 위 초록·공통 회색)을 `<br>`로 미리 나눠 다시 렌더. 조건 함수는 07-2 화살표 라벨로만, 양식 도구 메시지를 붙이는 자리와 END 갈래는 「소스 확인 ·」.
- **색 주의(강사·마감 확인)**: 이 절 지시대로 `create_agent`·에이전트 그래프를 **회색**으로 칠함. 01-1은 「create_agent 한 줄」을 우리가 적은 줄로 보아 **파랑**으로 칠했음 — 챕터 안에서 같은 요소의 색이 다름(규격 §5-3 「같은 요소는 절 안 모든 그림에서 같은 색」은 절 안 규칙이라 어긋남은 아니지만 챕터 검토 대상).
- 삽화 **1장** `07-4-열쇠와-선반을-붙인-세탁기`(비유 계열 「세탁기」 07 — 새 소품 열쇠·고리·선반·청바지로 「한 대에 모아 붙임」) — **1차 job `e07bcac2-0ee6-46cd-b848-fa69f49d02e0` 채택**, 재생성 0, **2크레딧**(거래 **2026-09-25T05:51:28Z** 「Nano Banana Pro −2」, 생성 전 잔액 2451.75, 바로 앞 거래 05:16:45Z는 06절 몫). 응답 모델 표시 `nano_banana_2`(01~06과 같음). 원본 `cb3b9d2f…`(2752 × 1536) → 저장 `cea2b935…`(1100 × 614), 픽셀 대조 bbox `None`·최대 차이 0. PNG를 직접 보고 셈(확대 두 장 포함): 세탁기 하나·버튼 하나·유리문 하나(파란 빨래)·왼쪽 옆면 고리 하나·금색 열쇠 하나(은색 고리)·오른쪽 옆면 흰 선반 하나(받침 나사가 기계 옆면에)·갠 청바지 한 벌. 관계와 무관한 차이(베이지 벽 면·갈색 고리·앞면 위쪽 띠의 칸 선)는 `.prompt.md`에 적고 그림 읽기에서 부르지 않음.

## 7. 서비스 요청과 비용

| 구분 | 모델(`gpt-5.4-mini`) | 임베딩 |
|---|---|---|
| 노트북 밖 흔들림 확인(A 두 설정 × 다섯 번) | 20 | 0 |
| 모델 없는 확인(가짜 키) | 0 | 0 |
| 새 커널 A | 4 | 0 |
| 새 커널 B | 4 | 0 |
| **합** | **28** | **0** |

- 노트북 한 번 **4번**(실습 절 3~5번 안, 강사 확인 대상 아님). 준비물에는 「두 도구를 따로 부르면 모두 6번까지」 범위를 적음(밖 10/10에서는 늘 2번씩).
- 요금표(2026-09-17, 100만 토큰당 0.75·0.075·4.50)로 어림한 **예상 비용 약 0.0152달러**: 밖 0.010832(기록한 사용량으로 셈) · A 0.002165(`0.00105 + 0.001115`) · B 0.002165. 청구 금액 아님.
- 삽화 2크레딧(거래 05:51:28Z). WebFetch 0.

## 8. 도구 파일 `notebooks/runner_tools.py`

- **바꾸지 않음**(`f4113158c0ccaee1205f0eabe315ef153e14c4dc6bcfd70ae8a9378edda96bdf` 그대로). 이 절이 쓰는 앞 절 평범한 함수 다섯(`agent_row`·`estimate_cost`·`print_branches`·`show_messages`·`sum_usage`)은 모두 이미 있음 — 가져오기는 알파벳 순 한 줄 + 고정 세 문장 + 커널 폴더 한 문장. 노트북에만 있는 앞 절 평범한 함수(04 `print_arrow_lines`·06 `doc_ids_in`·`search_trace`)는 쓰지 않음.
- 노트북 전역(`POLICIES`)에 기대는 도구 둘·실행 정보 형식은 노트북에 다시 적고 01·03 생성기 상수와 **문자열 대조**(`check_same_as_before()`가 실행마다), 도구 파일의 `agent_row`·`print_branches`는 01·02 생성기 셀과 AST 대조.
- 설치 셀에 `numpy==2.5.3`(도구 파일이 가져옴 — 05·06과 같음)·`pydantic==2.13.5`(노트북이 직접 가져옴 — 02와 같음). 판은 잠금과 같음.

## 9. 06절 이음새 (06 노트북은 다시 실행하지 않음)

- 06 b8·노트북 정리 끝 「07절 실습에서는 이 챕터에서 만든 에이전트 그래프와 함수를 모아(모읍니다), 자료실 문의 하나를 처리합니다.」 → **07 내용과 맞음**(01~03 에이전트 그래프·도구 파일 함수로 문의 하나). 01~05 b8처럼 **`_src` b8에 07 링크만 더함**: `author_06.py`(`7cf50d68…` → `bb014ce7…`, `_src` 문장 한 곳 — 고치기 전 생성기 `src_html()`이 그때 `_src`와 같음을 먼저 확인) → `author_06.py --src-only`(`_src/06` `0b5083fb…` → `d0a7413b…`) → `run_section.sh … 06 --no-exec`(게이트 06 0건). 노트북 문장은 링크를 넣지 않는 선례(노트북 정리 끝은 01~05도 글자만)라 `mdpatch.py`를 쓰지 않음.
- **06 노트북 그대로**: 파일 `768d4f9e45f2…`(전후 같음) · `code_sha256` `ca14949bb0f9…` · `outputs_sha256` `1ded374d9f64…` 그대로.
- **계약 파일 그대로**: `data/rag-comparison.json` **`25cfe5df3cfd729c130bce4af26c716cfcc3bcd4b4ff6e4a9d0a725816b02f51`**(전후 같음 — 07은 읽지도 쓰지도 않음).
- 06 빌드 HTML은 다음 절 링크(「챕터 끝」 → 07절)와 b8 링크로 `0dca4add…` → `81d3cf12…`. 01·02·04·05 빌드 HTML은 각 진단에 적힌 해시와 같음(`00ce823f`·`cc88e29e`·`6db1dc62`·`afcb826c`), 03은 04절이 제목을 바꾼 뒤 다음 절 링크 글자가 바뀐 판(`95e72567…`, 이 절 전과 같은 빌드 입력).

## 10. 챕터 밖 수정 · 보호 파일

| 파일 | 무엇을 |
|---|---|
| `textbook/part6/index.html` | `python3 textbook/part6/_build_index.py`가 다시 씀 — Ch 21 「7절」·07 링크·04 새 제목 글자(`a606f921…` → `32fbf36e8ab0…`, 보호 파일) |
| `textbook/downloads/part6-practice.zip` | 같은 스크립트가 다시 만듦(`0543ea63…` → `278766340335…`, 보호 파일) — 07 노트북·06 새 노트북·도구 파일 `f4113158…`·계약 파일 `25cfe5df…`·README 새 판이 처음 들어감(`part6-practice/labs/part6/ch21-create-agent/` 항목 12) |
| `textbook/part6/qa/integration-results.json` | 같은 스크립트가 다시 씀(`8be394e0…` → `119d32c66612…`, 보호 파일) |
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | `verify.py --chapter`가 다시 씀(`a5d1415d…` → `71f81c16bb74…`, 보호 파일·기록 파일) |

- 챕터 안(실습 폴더 포함): `chapter.json`(07절 추가, `f163836b…` → `67d7c5e2…`, `hours`·`objectives` 그대로) · 실습 폴더 `README.md`(맨 아래 07 한 단락, `c9adbb9d…`) · 06 `author_06.py`·`_src/06`·빌드 HTML(§9) · 새 파일(노트북 07 `746b3a46…`·`_src/07` `ede51742…`(설명 채움 전 판 — 최종은 §11)·빌드 `07-*.html`·`index.html` `02cd183c…`·`figures/07-*`·`qa/upgrade/` 새 파일) · `handoff.md` 「실습 → 챕터 검토」·`manifest-changes.md` 07 줄·`집필점검표.md`·`qa/verification.md` 07 행.
- **보호 파일 73개**: **65개 같음 · 8개 바뀜** = 06절 끝까지 바뀐 다섯(`_author_ch21_ch29.py`·`part6/public-files.json`·챕터 `qa/public-files.json`·계약 파일·notebook-contracts — 이 절은 notebook-contracts만 다시 씀) + **이 절이 지시대로 `_build_index.py`로 바꾼 셋**(`part6/index.html`·`part6-practice.zip`·`integration-results.json`). `public-files.json` 둘은 **고치지 않음**(명시 목록 — 07 줄은 마감 몫, Ch 22 09도 목록에 없음).
- **고치지 않은 것**: 01~05 파일(노트북·`_src`·생성기) · 도구 파일 · 계약 파일 · Ch 29 파일 · Ch 22 파일 · 공용 도구·게이트·`verify.py`·`build_index.py`·`_build_index.py` · 실습 폴더 `pyproject.toml`·`uv.lock` · 옛 그림. **파일 삭제 0건**.

## 11. 검사 결과 (Part 6)

- `run_section.sh … 07 --no-exec`: 게이트 **0**, `verify.py --chapter` **`PASS 7 sections / 180 code cells (max 16 lines)`**(16줄은 05·06 가져오기 준비 셀 — 07은 가져오기 준비 셀 15줄, 준비 셀이 아닌 셀 최대 10줄), 빌드 HTML 일곱·목차 `{{` 0건.
- `python3 textbook/part6/_build_index.py` → **`Part 6: 49 verified sections; 94 bundled files`**(절 수는 링크 수로 셈 — Ch 21 「강의 6시간 · 실습 10시간 · 7절」, 19행 설명 문장은 그대로·마감 몫).
- `check_delivery.py` → **117행 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`에서 멈춤**(`llm-practice.zip` — 알려진 일, 전체 마감 몫). 그 전 단계(HTML 쪽·절 검사·링크·`part6-practice.zip` 매니페스트 신선도·비밀값)는 지나감. `delivery-results.json`은 쓰기 전에 멈춰 **안 바뀜**(2026-09-10 판).
- 묶음 실행 검사(`check_bundle_execution.py`)·`visual.cjs`·옛 검사 넷은 **돌리지 않음**(마감 몫).
- 최종 해시: 생성기 `author_07.py` 설명 채움 뒤 판·`_src/07`·빌드 HTML은 `handoff.md` 「실습 → 챕터 검토」 3번에 적음.

## 12. 강사 확인 대상

1. **제목 표기** — `chapter.json` 07 제목 「create_agent 실습: …」은 밑줄을 살림(이 절 지시·챕터 제목 「create_agent — …」과 같음). 01 제목은 「create agent와 ReAct 루프」(밑줄 없음) — 챕터 안 표기가 둘(준비 노트 §7-5와 함께 결정).
2. **실행 2가 03절 8절과 같은 값(연체 0 → 3)을 바꿈** — 「새로 볼 것」을 양식 칸까지 이어지는지로 둠. 다른 값(이용자 번호 등)을 바꾸면 결과가 도구 메시지 글자 하나뿐이라 고르지 않음.
3. **양식 클래스 `LoanAnswer`를 새로 적음**(02 `PolicyAnswer`와 같은 모양, 칸 이름·설명 글은 흐름을 보여 주려고 정한 예) · **문의 글도 새로 정함**(두 도구가 모두 필요하게 — 붙인 부품이 모두 쓰이도록 설계한 예).
4. **07-1 색** — `create_agent`·그래프 회색(이 절 지시) ↔ 01-1 파랑(§6).
5. 03에서 이어진 것: `ToolRuntime[MemberContext]` 대괄호(03 진단 강사 확인) · 01~04 설치 셀에 `numpy`가 없는 문제(07은 넣음 — 마감 결정).

## 13. 남은 것 · 지워야 하지만 지우지 않은 것

- 마감 몫: `handoff.md` 「실습 → 챕터 검토」 5번.
- 삭제 승인 대상(만들었지만 지우지 않음): 기기 `/tmp/ch21-07/`(`A.ipynb`·`B.ipynb`·`probe-07.jsonl`(사본은 `probe/`에)·`illu-1-orig.png` 3.3MB·`illu-1-1100.png`·`nomodel_check.py`·`names_check.py`·`manifest_check.py`·`extra_check.py`·`ban_check.py`·`cmp.py`·`resize.py`·`pixcmp.py`·`reps1.json`·`reps2.json`·`gates-wip-07-07.first.json`·`chapter.before.json`·`author_06.before.py`·`README.before.md`·`집필점검표.before.md`·`verification.before.md`·`manifest-before07.txt`·`hashes-before07.txt`·`before-build-index.txt`) · 기기 `/tmp/nbout.py`(출력 보기용) · `.cache/ch21-07-view/`(그림 확인 사본 일곱) · (07은 `__pycache__`를 새로 만들지 않음 — `labs/…/notebooks/__pycache__/runner_tools.cpython-312.pyc`는 05:11 판 그대로, `qa/upgrade/__pycache__/`도 07 작업 전 판) · `qa/upgrade/gates-wip-07*.json`·`gates-wip-ch21-after07.json`.

## 마감 반영 (2026-09-25, 챕터 마감 담당)

검토 1차(`review-round1-A.md`·`review-round1-B.md`) 반영과 챕터 마감에서 이 절에 한 일입니다. 전체 기록은 `chapter-summary.md`, 절 사이 기록은 `handoff.md` 「검토 반영과 챕터 마감 (2026-09-25)」입니다.

- **다시 실행하지 않음**(설치 셀에 이미 `numpy==2.5.3` — `code_sha256` `bf48d235…`·`outputs_sha256` `7f670216…` 전후 같음, 노트북 파일 `746b3a46…` → `a1ac0fcf…`(마크다운만)).
- **B-12·A-13 색**: 챕터 리드 결정대로 **라이브러리가 준 `create_agent`는 회색** — 07-1은 그대로 두고 01-1·05-1을 회색으로 맞춤(위 §12-4 해결). 도식 읽기 「회색은 라이브러리가 준 함수」는 그대로 참.
- **B-13**: 준비물·b2 「01~06절에서 쓴 이름과 문법만」 → 「01~06절에서 쓴 이름과 **Ch 2에서 배운 문법**만」(8절 `if … and …:`의 `and`는 01~06 노트북에 없던 Ch 2 문법 — 코드는 그대로). 위 §1 「새 것은 이 절 변수 이름과 양식 칸 이름뿐」에 `and` 한 항목을 더해 읽을 것.
- **B-14**: 복습 3을 03 복습 3과 다른 물음으로 — 「연체 일수만 바꿨을 때 칸 `can_borrow`는 어떻게 바뀌었고, 그 값은 누가 채웠으며 무엇과 견줘 확인했나요?」(해설: `가능` → `불가` · 모델이 바뀐 도구 메시지 글을 받은 뒤 채움 · 8절 규칙 값과 견줘 두 실행 모두 같음 · `assert`는 걸지 않음).
- **B-15**: b4 그림 읽기 뒤 단락을 둘로 나눠 이음 문장 — 「03절 그림의 윗면 틈에 꽂은 카드처럼, 기계가 읽지만 빨래와 함께 나오지 않습니다」 · 「02절 그림에서 개는 판을 거쳐 나온 셔츠처럼, 정해 둔 모양으로 갠 빨래입니다」(삽화는 다시 만들지 않음).
- 1절 「도구 파일이 05절부터 numpy를 가져오므로 …」 → 「도구 파일이 NumPy를 쓰므로, 01~06절처럼 numpy도 함께 설치합니다」(01~04에도 더해 사실이 바뀜).
- 위 §12-1(제목 표기)은 01·03 제목에 밑줄을 살려 챕터 안이 한 가지 표기가 됨. 게이트 0(검사 문장 347).
