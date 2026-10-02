# 07-구조화-출력-프롬프트-진단 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 07, `figures/07-structured-diagnosis.*`). 수정 전 게이트는 챕터 `gates-before.json`의 07 행.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 4 | 0 |
| G2 | 1 | 0 |
| G3 | 0 | 0 |
| G4 | 1 | 0 |
| G5 | 5 | 0 |
| G6 | 18 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 7 | 24(준비 3) |
| 검사한 문장 | 117 | 434 |

G8: `run_section.sh` 새 커널 PASS 두 번(2026-09-17, 24 코드 셀, 두 번째 실행 출력이 교재 출력), 결과 읽기는 `mdpatch.py` 두 번(`/tmp/ch07-07/reps1.json` 자리 표시 채우기, `reps2.json` G6 노트북 10곳) → `--no-exec`로 렌더·첨부·빌드·verify(`PASS 8 sections / 157 code cells`)·게이트 0(`gates-wip-07.json`, `--section 07`으로만 실행). verify 계약의 07 `outputs_sha256` `e759b37b…`. `visual.cjs` 1280px·390px PASS(공용 도구는 고치지 않고 `/tmp/ch07-07/vis/vis.cjs` 사본 + HTML 사본, 작은 글자·대비·잘림·가로 스크롤·깨진 그림·복사 불일치 0). 코드 셀 출력 칸은 셀마다 0~1개(요청 반복문 셀은 반복이 끝난 뒤 `모은 기록 수:` 한 줄만 출력). 노트북 코드 셀 출력 텍스트 이어 붙인 SHA-256 `12387bd6…ef593d0ae`(두 번째 새 커널 사본 `/tmp/ch07-07/run2.ipynb`와 같음, 설명만 고친 뒤에도 같음). `runs/` 파일은 건드리지 않음(`provider-comparison-continuity.json`·`prompt-ab-continuity.json`은 08 전용).
meta 「강의 0.5h | 실습 0.5h」는 개선 전 값을 유지했지만 코드 셀 24개·문장 434개라 시수와 맞지 않을 수 있음 → 강사 확인 대상.

## 수정 전 주요 문제

- G1(4): 한 셀에 함수 두 개(`run`·`mention_flags`), 딕셔너리 내포식 3(`mention_flags`, 요청 3번을 `{name: run(...) for ...}` 한 줄로, `{f: f in parsed for f in fields}`). 그 밖에 `raise RuntimeError`(A 트랙 미교육), `import json, os, time` 한 줄, 예외 튜플 `except (json.JSONDecodeError, TypeError)`(미교육), `json.dumps(…, indent=2)` 전체 출력(영어 키 `parsed`·`fields`·`error`), 결과 출력 `print("\n", name, …)`에 사용량 딕셔너리 통째
- G2: 한 글자 변수 `f`. G4: 모델 셀 `max_tokens=220`, `temperature=0`·`reasoning_effort="none"` 없음
- G5: 제목 셀·핵심 그림 없음, 결과 읽기 셀 없음·출력 인용 없음(5건)
- G6: 70자 초과 6, 영문 시작 10(「`brief`는」「`fields`는」「`schema`는」「`json.loads(result["text"])`는」「`{f: f in parsed for f in fields}`는」 등), 5문장 넘는 단락 2
- G7: Mermaid 0(옛 Excalidraw `07-structured-diagnosis.svg` 1장, 폭 980), 삽화 0, 설계표 없음
- 내용: (1) b3 「이번 챕터에서는 역할별 메시지, 과업 제약, 관련 예시가 출력에 미치는 영향을 비교」 — 04 틀·05 근거·06 합의가 빠짐(06 인계). (2) 목록 system 「고객 지원 데이터를 만듭니다.」 + user(JSON 지시 + 옛 `TASK`) — 01~06 목록(system 페르소나·developer 과업 명세·user 고객 문의)과 다름, b3 「JSON을 요구하는 user 메시지의 구체성」도 01~06(출력 형식은 developer)과 다름. (3) b4 「필드(field)」 — Ch 6 03 「칸(필드)」은 양식 클래스 자리이고 딕셔너리 자리는 「키」(Ch 6 인계). (4) b4 「코드 울타리」「목록 JSON」「허용값·자료형」을 말로만 적고 노트북은 실행하지 않음, 자동 검사는 키 존재까지. (5) b6 숫자(98·110·137, 244·199·243)는 2026-09-09 한 번 실행(규격과 다른 설정). (6) 참고 자료 확인일 2026-09-09, LangChain 문서 둘은 본문에서 인용하지 않음. (7) 새 용어 6개가 `<p>`에 흩어지고 일상 예·코드 모습 없음. (8) b8 「버전별 아티팩트로 저장」 — 08 개선 전 b2와 맞지만 말이 어려움
- 앞 절·앞 챕터와 어긋남: 01~06·Ch 6 기록 모양(한국어 키·`timed_invoke`·`make_prompt_record`)과 다른 영어 키, 대문자 `TASK`·`MENTIONS`, 옛 `run()`, 요청 반복을 내포식 한 줄로

## 바꾼 것

- 모델: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(nbkit `key_and_model_cells`, 실행일 줄 `RUN_DAY = "2026-09-17"`). 출력 상한 없음
- 데이터·설계(06 인계 반영): 2절 06과 글자까지 같은 페르소나·고객 문의·목표·필수 정보·금지 사항·출력 형식 글. 3절 출력 형식 한 글만 세 단계로 바꿈 — `json_format_text = "분류, 다음 행동, 고객에게 보낼 한 문장을 JSON으로 답하세요."`, `keys_format_text`(+ 키 이름 category·next_action·customer_message), `rules_format_text`(+ category 허용 이름·세 값은 글 + 코드 블록 표시나 설명 글 없이 JSON 객체 하나). 개선 전 세 조건 brief/fields/schema와 영어 키 세 개, 허용 이름 배송·교환·환불(06 `allowed_labels`와 같음)을 이어 씀. `task_start_text`(앞 세 글 + 줄바꿈) + 출력 형식으로 목록 세 개, system·user 같음 `assert`. 05·06처럼 튜플 목록(틀 안 씀)
- 직접 적은 글(요청 없음): 4절 키가 맞는 JSON 글 `json.loads()` → `dict`·키 목록, 코드 블록 표시를 붙인 글 → `json.JSONDecodeError`를 받아 이름·메시지 출력(`Expecting value: line 1 column 1 (char 0)`, Ch 6 01 모양, 점 이은 오류 이름·ValueError 한 종류 한 문장). 5절 함수 넷 — `parse_json_answer(answer_text)` → `(읽은 값, 읽음/구문 오류)`, `find_missing_keys(parsed_value)`(딕셔너리 `in` 한 문장), `find_value_problems(parsed_value)`(`type(값).__name__ != "str"`·category 허용 이름, 06 `find_label()`처럼 고쳐 세지 않음), `check_layers(answer_text)` → 한국어 키 딕셔너리 `JSON 읽기`·`값 종류`·`없는 키`·`값 규칙 문제`(딕셔너리일 때만 키·값 검사, 아니면 「검사 안 함」) — 직접 적은 글 다섯 개(코드 블록 표시·한국어 키·다른 값·배열·모두 맞음)로 확인 `assert`. 개선 전 본문이 말로만 적은 코드 울타리·배열·허용값·자료형을 실제 실행
- 요청: 6절 `timed_invoke`·`make_prompt_record`(01~06 같은 코드, 키 6개), 7절 `condition_lists` 튜플 목록을 `for`로 풀어 요청 3번(반복문 안 `append`만, 끝난 뒤 출력), 8절 기록표·더한 입력 토큰, 9절 층별 검사 표, 10절 「값 규칙」 답 키마다 값·확인 단어 표시, 11절 값 바꿔 보기(고객 문의만 03 관련 없는 예시 「뉴스레터 글꼴을 바꾸고 싶습니다.」로, 요청 1번)·category 값 꺼내기
- 새로 풀어 쓴 것(처음 쓰는 자리 한두 문장): JSON 글(딕셔너리 비슷한 모양, Ch 4 04·Ch 6 06 이음), 코드 블록 표시, `json.JSONDecodeError`, 딕셔너리 `in`, `list(딕셔너리.keys())`, 글 안 큰따옴표를 작은따옴표로 감싸기, 한국어 기록 키와 JSON 영어 키 구분. 쓰지 않은 것: f-string·`Path`·`next`·해시·`**` 풀기·글 슬라이싱·`startswith`·`strip`(06은 씀, 07은 불필요)·`join`·`+=`·`sum`·`max`·`isinstance`·예외 튜플·내포식·조건 표현식·`with_structured_output`·틀·`@`·`BaseModel`(§2-2 링크 불필요)
- 요청 수: 노트북 4번(mini). 탐색 실행 5번(`/tmp/ch07-07/probe1.py`: 세 목록 + 글꼴 문의를 「값 규칙」·「JSON만」 목록으로, 문구는 탐색 뒤 바꾸지 않음) + 새 커널 실행 2번 × 4 = 합계 13번. 예상 비용 합계 약 0.007달러(Ch 6 06절 mini 요금, 세 실행 토큰으로 계산)
- 실행 출력(2026-09-17, 두 번째 새 커널): 「JSON만」 `{"분류":"교환 접수",…}`(한국어 키 셋), 「키 이름」 `{"category":"교환 요청",…}`, 「값 규칙」 `{"category":"교환",…}`, 세 답 모두 코드 블록 표시 없음·보상 약속 없음. 기록표 `JSON만 | 130 | 93 | stop | 1.26`·`키 이름 | 145 | 90 | stop | 1.58`·`값 규칙 | 191 | 109 | stop | 1.4`, 더한 입력 15·46. 층별 `['category', 'next_action', 'customer_message'] | []`·`[] | ['category 값이 허용 이름 밖']`·`[] | []`. 「값 규칙」 next_action `주문번호 A-1042의 교환 접수를 도와드릴 수 있으며, …사진을 보내주시면 확인 후 진행하겠습니다.`(고객에게 하는 말) ↔ 「키 이름」 next_action `파손 사진을 요청한 뒤 교환 접수를 진행하세요.`(상담원이 할 일). 확인 단어 세 줄 모두 `[True, True, True]`. 글꼴 문의 `{"category":"배송","next_action":"뉴스레터 글꼴 변경은 주문 배송 관련 문의가 아니므로, …"}`·`읽음 | [] | []`·`169 | 95`
- 두 번 실행과 탐색에서 달라진 것(구조·층별 결과·입력 토큰은 세 번 모두 같음 130·145·191·169): 첫 실행 출력 93·96·89, 글꼴 79, 「JSON만」 분류 값 「교환 접수」, 글꼴 category 배송(주문번호를 요청). 탐색: 출력 96·83·92, 「JSON만」 분류 「교환 요청」, 글꼴 category **환불**, 「JSON만」 목록 + 글꼴 문의는 한국어 키·`기능 문의`. 「값 규칙」 next_action이 고객에게 하는 말·「키 이름」 next_action이 상담원 지시인 것은 세 번 모두 → 본문 「이번 세 실행에서 본 모양으로만」
- 결과 읽기 작성 방식: 모델 출력에 기대는 결과 읽기 8곳 + 해석·정리를 생성기에 자리 표시로 두고 두 번째 새 커널 뒤 `mdpatch.py`로 생성기·노트북에 함께 채움(생성기에 채운 글이 남음). 「오늘 볼 그림」 alt는 `FIG1ALT` 낱말 자리 표시(06 인계). 직접 적은 글 결과 읽기는 생성기에 바로 쓰고 첫 실행 출력과 대조
- 문서 확인(2026-09-17, WebFetch): Python 3.12 `json` 문서 「JSONDecodeError – When the data being deserialized is not a valid JSON document」, 「Subclass of ValueError」, 변환표 object → dict·array → list·string → str. OpenAI Structured Outputs 안내서 「Structured Outputs is the evolution of JSON mode. While both ensure valid JSON is produced, only Structured Outputs ensure schema adherence.」·「We recommend always using Structured Outputs instead of JSON mode when possible.」. 본문 b4·b7·b10은 이 문장 기준. 이 절 요청은 `response_format`을 주지 않은 보통 `invoke`라 「두 기능을 모두 켜지 않은 보통 요청」. Ch 6 03 경로 설명(양식이 JSON 스키마로 실림·호출 객체가 읽음)은 Ch 6 03 `_src` b4 문장(openai 3.10.0 소스 확인)을 이어 씀. 개선 전 LangChain Models·Structured output 링크는 본문에서 인용하지 않아 뺌
- 본문 10블록 다시 씀: 학습 목표 4, 이 절의 질문, 앞에서 배운 내용 표(06·05·03·02·01·Ch 6 06·03·01) + 06 이어짐 단락 + 개선 전 설계 고친 단락, 비유(06 책상 → 길과 문 셋·카드 셋·돋보기, 택배 접수대 층 순서 — Ch 6 01 택배 접수대 일상 예를 넓힘), JSON 답과 세 층 검사, 출력 형식 글 세 단계, Ch 6 03절 양식 클래스와 다른 점(OpenAI 문서 문장), 용어 표 6개(구문 오류·필요한 키·값 규칙·코드 블록 표시·세 층 검사·내용 오류 — Ch 6 03 파싱·JSON 스키마·양식 클래스는 다시 정의하지 않음), 실행 예제 뒤 「세 답이 걸린 층」, 실험 결과 해석(「고객 문의만 바꾸면」), 주의 메모 8개(탐색 뒤 정한 문구와 탐색 요청 수, 규격 §3), 복습 5문제, 참고 자료 3개
- 그림: Mermaid 4장(07-1 네 층 검사, 07-2 세 답의 층별 결과, 07-3 글로 요청과 양식 클래스, 07-4 고객 문의만 바꾸기), 삽화 1장(07-5 세 문과 카드, job 35a358eb-1327-4eb6-9728-82abec251886, 2크레딧, 1회 생성 통과, 원본 SHA-256 `ea624f54…7526245`, 저장 PNG 픽셀 대조 차이 0). 옛 `{{svg:07-structured-diagnosis}}`는 본문에서 뺌(파일은 `figures/`에 남기고 `before/figures/`에 사본). 빨강 0장(구문 오류는 받아 기록한 결과, 내용 오류는 사람의 판단이라 노랑), 회색 = 실행 안 한 Ch 6 03 경로(07-3), 파랑 = 정의한 함수·원문 읽기 단계. 렌더 도장 파일은 지우지 않음(mmd 내용을 바꿔 다시 렌더)
- Ch 6·01~06 인계 반영: 옛 `TASK`·`run()`·`mention_flags()` 0건. `timed_invoke`·`make_prompt_record`·한국어 키 6개·기록표 모양·`check_words`·조건 이름 방식·`allowed_labels`(06) 같음. 그림 색 01~06과 같음. JSON 자리는 「키」(Ch 6 인계), 「필드」「칸」「조각」「청크」「출력 상한」「쟁반」「카드 꽂이」「우편함」「투명 봉투」 쓰지 않음, 「양식」은 Ch 6 03 양식 클래스를 가리킬 때만. temperature 0 ≠ `do_sample=False` 한 문장(모델 셀)
- 08절 호환: 08 노트북·본문은 07 결과·함수·파일을 읽지 않음(08 노트북 셀 확인, `labs/part2/ch08-context-engineering/tests`도 07 노트북 이름 없음). 08 개선 전 b3 「반복 표본, JSON 필드 진단을 차례로 확인」은 07 개선 뒤 「JSON 답 세 층 검사」로 고치면 맞음(08 작업자 몫)

## 검토자가 볼 곳

1. 결론 범위: b6 「「값 규칙」 next_action은 고객에게 하는 말」(세 실행 모두 봄, 일반화 안 함), 「글꼴 문의 category 배송 = 내용 오류」(사람의 판단, 탐색은 환불), 「구문 오류는 모델 답에서 보지 못함」
2. 문서 인용: b4 「Ch 6 03절 양식 클래스와 다른 점」의 OpenAI Structured Outputs 두 문장 요약과 「이 절 요청은 두 기능을 모두 켜지 않은 보통 요청이라 JSON 글이 온다는 보장부터 없음」, b7 권장 문장
3. 삽화 07-5: 뒤쪽 물건이 책상 뒤 위쪽에 떠 있고 셋째 카드도 누워 있음(프롬프트는 upright) — 그림 읽기가 문 사이 위치와 돋보기로 가리키는지. meta 시수(강사 확인)

## 검토

- 별도 세션 검토 1차(2026-09-17, `qa/upgrade/review-round1-B.md`): **accept-with-fixes**(중 1·하 3, 공통 C-2 반영 전제). 반영: 07-1(중) 노트북 [51]·b6 「고객 문의만 바꾸면」 셋째 단락을 「허용 이름 셋 가운데 이 문의에 맞는 이름이 없어, 규칙을 지킨 답은 어느 이름을 적어도 문의와 맞지 않음 / 셋 가운데 어느 이름을 고르는지는 실행마다 달랐고 그 까닭은 단정 안 함」으로. [51]은 「실행 전에 예상한 대로입니다」(권고 「11절 앞에서」는 이 결과 읽기가 11절 안이라 바꿈). 복습 5 해설 끝 한 문장, 노트북 실험 결과 해석 「맞는 분류가 없었고, 답은 분류 값에 배송을 적었습니다」. 07-2 b6 새 단락·노트북 [45] 두 문장(과업 명세가 다음 행동 키의 뜻을 정하지 않음 → 키의 뜻을 출력 형식에 적어야 한다는 신호). 07-3 b4 「두 기능을 켜는 인자(`response_format`)를 주지 않은 보통 `invoke()` 요청」. 07-4 노트북 [41] 「190은 Ch 6 07절 노트북 출력이고, 61은 작업 중 기기 셸에서 한 번 잰 값이라 Ch 6 07절 본문에만 있습니다」(권고 한 문장이 70자를 넘어 줄임). C-2 b3 두 곳, C-4 b5 「조건마다 큰 상자 하나씩」, meta(**강사 확인**). 결정 Q2 권고대로 「값 규칙」 말투 관찰·내용 오류 사람 판단·노랑·삽화 07-5 유지.
- 반영 방법: `mdpatch.py` → `run_section.sh … 07 --no-exec`(노트북 재실행 없음, 코드 셀·출력·`verification` 메타데이터로 만든 해시가 반영 전과 같음). 마감 게이트 `gates-after.json`(`--strict`) G1~G7 0, 코드 셀 24, 검사 문장 440. 리뷰 묶음은 다시 만들었고 반영 전 묶음은 `qa/upgrade/before/review-round1/review-pack/`에 있습니다.

## 남은 것

- 기기 `/tmp/ch07-07`(탐색 스크립트·`run1.ipynb`·`run2.ipynb`·visual 사본·치환 json·삽화 원본 `illus-07-5-a.png`·확인용 `check-07-5-a.png`)은 정리 대상
- 옛 도식 `figures/07-structured-diagnosis.*`는 정리 대상 목록에만 적음(삭제하지 않음)
- 별도 세션 검토, 강사 확인(meta 시수)
