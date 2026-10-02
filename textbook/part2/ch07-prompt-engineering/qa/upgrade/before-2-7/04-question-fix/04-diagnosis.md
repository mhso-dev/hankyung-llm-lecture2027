# 04-ChatPromptTemplate과-MessagesPlaceholder — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 04, `figures/04-메시지-템플릿.*`). 수정 전 게이트는 챕터 `gates-before.json`의 04 행.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 3 | 0 |
| G2 | 1 | 0 |
| G3 | 0 | 0 |
| G4 | 1 | 0 |
| G5 | 6 | 0 |
| G6 | 27 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 7 | 24(준비 3) |
| 검사한 문장 | 114 | 466 |

G8: `run_section.sh` 새 커널 PASS 두 번(2026-09-17, 24 코드 셀, 두 번째 실행 출력이 교재 출력), 결과 읽기·본문은 `mdpatch.py` 세 번 → `--no-exec`로 렌더·첨부·빌드·verify(`PASS 8 sections / 114 code cells`)·게이트 0(`gates-wip-04.json`, `--section 04`로만 실행해 `gates-wip.json`은 새로 만들지 않음). `visual.cjs` 1280px·390px PASS(공용 도구는 고치지 않고 `/tmp/ch07-04/vis/vis.cjs` 사본 + HTML 사본, 작은 글자·대비·잘림·가로 스크롤·깨진 그림·복사 불일치 0). 코드 셀 출력 칸은 셀마다 1개(요청 반복문 없음). 노트북 코드 셀 출력 텍스트 이어 붙인 SHA-256 `32b48bc9…8aa555dcc4`(두 번째 새 커널 뒤 설명만 고쳐도 같음). `runs/` 파일은 건드리지 않음.

## 수정 전 주요 문제

- G1: 한 셀에 함수 두 개(`run`·`mention_flags`), 딕셔너리 내포식, 목록 내포식 `[(m.type, m.text[:80]) for m in …]`. 그 밖에 `raise RuntimeError`(A 트랙 미교육), `import json, os, time` 한 줄, `{**base_values, "history": …}` 풀기(미교육), 글 슬라이싱 `text[:80]`, `{"history_empty": …}.items()` 반복
- G2: 한 글자 변수 `m`
- G4: 모델 셀 `init_chat_model("openai:gpt-5.4-mini", max_tokens=220)` — `temperature=0`·`reasoning_effort="none"` 없음
- G5: 제목 셀·핵심 그림·결과 읽기 셀 없음(6건)
- G6: 70자 초과 5, 영문 시작 21(「`ChatPromptTemplate`은」「`MessagesPlaceholder`는」「`optional=True`를」 등), 5문장 넘는 단락 1
- G7: Mermaid 0(옛 Excalidraw `04-메시지-템플릿.svg` 1장), 삽화 0, 설계표 없음
- 내용: (1) 01~03이 나눈 목록과 다른 옛 대문자 `TASK`(규정·형식·고객 말 한 글)를 human 빈자리에 넣고 system에 `{format_rule}` 한 줄 → 03 b8 「`+`로 이어 만든 메시지 목록을 틀로 만든다」가 이어지지 않음. (2) 개선 전 b3 「03절에서 예시 입출력 쌍을 메시지에 추가」는 개선된 03(예시를 developer 글 안에)과 다름. (3) 기록 한 턴이 「세 줄 이내로 써 주세요」라 기록이 무엇을 이어 주는지 보이지 않고, b6 「두 조건 모두 과업 충족」 표 108/146토큰은 옛 실행(2026-09-09)·규격과 다른 설정. (4) 「기본 `MessagesPlaceholder`는 오류가 날 수 있습니다」를 실행하지 않고 적음. (5) 정의 6개 `<dl>`만 있고 일상 예·코드 모습 없음, 「신청서 양식」 비유가 Ch 6 03 양식 클래스(`BaseModel`)와 겹침. (6) developer 역할을 틀에 넣는 문제를 다루지 않음(01~03 목록 모양을 옮기면 실제로 `ValueError`)
- 앞 절·앞 챕터와 어긋남: 01~03·Ch 6 기록 모양(한국어 키·`timed_invoke`·`make_prompt_record`)과 다른 영어 키 `text`·`usage`·`latency_s`, 역할 이름 `human`만 쓰고 01 user ↔ human 연결 없음, `TASK`·`MENTIONS` 대문자 이름

## 바꾼 것

- 모델: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(nbkit `key_and_model_cells`, 실행일 줄 `RUN_DAY = "2026-09-17"`). 출력 상한 없음
- 데이터(03 인계 반영): 2절에서 03 예시 없음 목록 `zero_messages`(= 02 `task_messages`)를 글자까지 같게 다시 만듦. 3절 틀 `prompt = ChatPromptTemplate.from_messages([("system", persona_text), developer_message, ("user", "{inquiry}")])`. 4절에서 `prompt_messages == convert_to_messages(zero_messages)`를 `assert`(True), 5절 입력 토큰 134(02·03과 같음). 재사용은 요청 없이 머그컵 문의 `A-1107`로 한 번 더 채워 앞 두 메시지 같음 `assert`
- developer 역할 결정: langchain-core 1.6.2 `prompts/chat.py` `_create_template_from_message_type`은 역할 이름 human·user·ai·assistant·system·placeholder만 처리 → 3절에서 developer 튜플을 넣어 실제 `ValueError`(`Unexpected message type: developer. …`)를 받아 출력(노랑 성격, 그림에는 넣지 않음). `_convert_to_message_template`의 `BaseMessage` 분기로 01 `convert_to_messages([("developer", task_text)])[0]`(추가 정보 `{'__openai_role__': 'developer'}`)를 틀에 그대로 넣음. 메시지 객체 글은 빈자리를 찾지 않음(`format_messages`에서 그대로 추가)
- 대화 기록(개선 전 「세 줄 이내」 한 턴 대신): 다음 질문 `followup_text = "사진은 어디로 보내면 되나요?"`, 기록 `history_messages = [("user", inquiry_text), ("assistant", template_record["답"])]`(5절 실제 답). assistant 튜플 → `AIMessage | ai`를 처음 쓰는 자리에서 한 문장(Ch 6 02 user ↔ human처럼). 틀 `MessagesPlaceholder("history", optional=True)`를 developer와 user 사이에, user 빈자리 `{question}`. `input_variables` `['question']`·`optional_variables` `['history']`. `optional=True`를 뺀 틀은 `['history', 'question']` + 실제 `KeyError`(`is missing variables {'history'}`, 중괄호 두 번 겹쳐 쓰기 안내 포함)
- 값 바꿔 보기: `MessagesPlaceholder("history", optional=True, n_messages=1)` → 메시지 4개(고객 문의 빠짐, 5절 답만), 요청 1번. 소스 `format_messages`의 `value[-self.n_messages:]`
- 기본 경로: 설치 → import(`time`·`init_chat_model`) → 키 → 모델 → 2절 → 3절 오류·틀 → 4절 채우기·같음·재사용 → 5절 함수 둘·요청 → 6절 기록 자리·기록·두 번 채우기·필수 자리 오류 → 7절 두 요청·기록표·확인 단어 → 8절 n_messages 채우기·요청·나란히 보기 → 실험 결과 해석·정리. `ChatPromptTemplate`·`MessagesPlaceholder`·`convert_to_messages` import는 처음 쓰는 셀에서
- 새로 풀어 쓴 것(처음 쓰는 자리 한두 문장): 글 속 `{이름}` 빈자리(f-string과 다름, Part 1 f-string 연결), 틀의 `invoke()` vs 모델의 `invoke()`(점 앞 객체), `ChatPromptValue`·`to_messages()`, 메시지 객체 목록 `==`, assistant 튜플, `optional=True`, `n_messages`. 쓰지 않은 것: 문자열 하나로 `invoke`(틀·모델 모두), f-string 코드, `Path`·`next`·해시, `**` 풀기, 글 슬라이싱, 내포식·조건 표현식, `+=`, `join`·`strip`, 파이프 `|`
- 요청 수: 노트북 4번(mini). 탐색 실행 4번(`/tmp/ch07-04/probe1.py`: 틀 목록·기록 없음·기록 있음·n_messages=1, 두 오류와 목록 같음도 함께 확인) + 새 커널 실행 2번 × 4 = 합계 12번. 예상 비용 합계 0.01달러 미만(Ch 6 06절 mini 요금 기준)
- 실행 출력(2026-09-17, 두 번째 새 커널): 5절 `분류: 교환 요청(파손)`·`입력 토큰 수: 134`, 기록표 `기록 없음 | 108 | 74 | stop | 0.94`·`기록 있음 | 239 | 81 | stop | 1.19`·`기록이 더한 입력 토큰 수: 131`, 확인 단어 `교환 | True | True`·`A-1042 | False | True`·`사진 | True | True`, 8절 `5절 답에 A-1042가 있는가: True`·`기록 있음 | 5 | 239 | 81 | True`·`최근 메시지 하나 | 4 | 200 | 72 | True`·`빠진 메시지가 차지하던 입력 토큰 수: 39`. 원문: 기록 없음 답 「주문번호와 파손 사진을 함께 보내주시면」(번호 다시 요청)·「이 채팅으로」, 기록 있음 답 「주문번호 A-1042로 확인해 드리겠습니다」·「이 채팅에」·「현재 대화창에」, 최근 메시지 하나 답 분류 「문의 응대」·다음 행동 「사진 전송 가능한 채널을 안내해 주세요」(상담원에게 시키는 말처럼 읽힘)·「현재 대화창에」. 네 답 보상 약속 없음
- 두 번 실행에서 달라진 것(구조는 같음): 첫 실행은 5절 답 끝말만 다름(입력 134 같음), 기록 없음 108/62, 기록 있음 238/84(더한 입력 130), 최근 메시지 하나 199/81(차이 39 같음), 분류 「교환 접수 문의」·다음 행동이 고객에게 하는 말. 탐색 실행: 134/89, 108/65, 239/81, 200/83. A-1042 없음/있음과 「채팅으로 보내라」 안내는 탐색·두 실행 모두 같음 → b6에 「세 번 본 모양이지만 늘 그렇다고 하지 않음」, 채팅 안내는 「과업 명세·기록에 없는 내용」 관찰로만
- 결과 읽기 작성 방식: 모델 출력에 기대는 결과 읽기 9곳은 생성기에 `[[READ_…]]` 자리 표시로 두고 두 번째 새 커널 뒤 `mdpatch.py`(`/tmp/ch07-04/reps1.json`)로 생성기·노트북에 함께 채움(생성기에 채운 글이 남음). 다시 실행하면 결과 읽기를 새 출력과 다시 대조해야 함
- 문서·소스 확인(2026-09-17): LangChain reference `ChatPromptTemplate`(optional_variables·from_messages)·`MessagesPlaceholder`(`optional`·`n_messages=1` 예), `INVALID_PROMPT_INPUT` 오류 안내, 설치한 langchain-core 1.6.2 `prompts/chat.py`(`_create_template_from_message_type`·`_convert_to_message_template`·`MessagesPlaceholder.format_messages`)·`prompts/base.py` `_validate_input`(KeyError 메시지). GitHub 링크는 기기·클라우드 프록시에서 403이라 설치 소스로 확인했다고 적음(03과 같은 방식)
- 본문 10블록 다시 씀: 학습 목표 4, 이 절의 질문, 앞에서 배운 내용 표(03·02·01·Ch 6 01·02·Ch 2 05) + 03 인계 단락·개선 전 설계 단락, 비유(03 책상 → 두 책상의 점선 빈자리와 투명 봉투, 생일 카드, 앞선 통화 메모), 메시지 틀과 빈자리, developer 튜플을 받지 않음, 두 invoke, 대화 기록 자리, 용어 표 6개, 실행 예제 뒤 「두 invoke의 순서」, 실험 결과 해석(03 목록과 같음·낱말 다름, 기록 없음/있음·채팅 안내, n_messages=1·원인 보류·Ch 8 02·03절 연결), 주의 메모 9개(탐색 뒤 정한 설정 포함, 규격 §3), 복습 5문제, 참고 자료 5개
- 그림: Mermaid 4장(04-1 틀에 문의 채우기, 04-2 두 invoke 순서 sequenceDiagram, 04-3 기록 없음과 있음, 04-4 최근 메시지 하나), 삽화 1장(04-5 틀과 빈자리, job 7d972a2c-9f60-4a51-a2b4-d6a77edd4344, 2크레딧, 1회 생성 통과, 원본 SHA-256 `3365f6ae…fac617b889`, 저장 PNG 픽셀 대조 차이 0). 옛 `{{svg:04-메시지-템플릿}}`은 본문에서 뺌(파일은 `figures/`에 남기고 `before/figures/`에 사본). 빨강 0장, 파랑 1곳(04-1 `prompt.invoke → to_messages`, 01 `convert_to_messages` 파랑 선례)
- Ch 6·01~03 인계 반영: 옛 `TASK`·`run()`·`mention_flags()` 0건. `timed_invoke`·`make_prompt_record`·한국어 키·기록표 모양·확인 단어 `check_words`·조건 이름 방식 01~03과 같음. 요청 반복문 없음(요청 셀마다 요청 뒤 한 번 출력). 그림 색 01~03과 같음. 「조각」·「청크」·「칸(필드)」·「출력 상한」·「양식」·「쟁반」·「카드 꽂이」·「우편함」 쓰지 않음(빈자리·틀·투명 봉투). `BaseModel` 없음(구조화 출력 안 씀, §2-2 링크 불필요). `runs/provider-comparison-continuity.json` 안 건드림(08 전용). temperature 0 ≠ `do_sample=False` 한 문장(모델 셀), 답 문장 `assert` 없음(목록 같음·앞 두 메시지 같음만)

## 검토자가 볼 곳

1. developer 역할 처리: 3절에서 실제 `ValueError`를 보이고 01 `convert_to_messages()` 객체로 넣은 설계, 「틀은 역할 이름으로 다섯 가지만 받는다」를 설치 판 소스·오류 메시지 범위로 적은 문장(b4·b7·복습 3)
2. 기록 설계와 결론 범위: 기록을 5절 실제 답으로 만든 것, 기록 없음 답의 A-1042 없음(세 번 같음)과 「사진은 채팅으로」 안내를 과업 명세에 없는 관찰로만 적은 문장(b6·노트북 7절), `n_messages=1` 답의 분류·말투 차이 원인 보류(b6·노트북 8절)
3. 삽화 04-5: 왼쪽 봉투 자리가 오른쪽과 다르고 카메라 메모지가 왼쪽 책상 아래라 그림 읽기에서 「두 책상 모두에 채울 메모지」로 이름 붙인 처리(검수 메모 `figures/04-5-틀과-빈자리.prompt.md`)

## 검토

- 별도 세션 검토 1차(2026-09-17, `qa/upgrade/review-round1-A.md`): **accept-with-fixes**(중 1·하 1, 공통 C-2 반영 전제). 반영: 04-1(중) b4 「튜플을 틀 조각으로 바꾸는 함수도 이 다섯 이름만」을 세 문장(「다섯 이름과 `placeholder`를 처리」 / 「역할 이름 `placeholder`는 메시지 목록 자리, 이 튜플은 이번에 실행하지 않음」 / 「6절은 같은 자리를 `MessagesPlaceholder`로」)으로 고치고 「조각」을 뺌(C-4 (2)). 노트북 [15] 「오류 메시지가 안내하는 역할 이름은 이 다섯 가지이고, developer는 없습니다」, 복습 3 해설 두 문장. 04-2 b6과 노트북 실험 결과 해석에 「필수 정보에 보낼 곳을 적은 요청은 이번에 실행하지 않았습니다」. C-2 b3 둘째 단락. 03-2 노트북 [21] 「튜플로 적은 03절 목록」. C-1 범위 문장 강의 3~6절·실습 7·8절(**강사 확인**). 결정 Q4 권고대로 developer 처리(실제 `ValueError` → 메시지 객체)·「사진은 채팅으로」 원인 보류 유지.
- 반영 방법: `mdpatch.py` → `run_section.sh … 04 --no-exec`(노트북 재실행 없음, 코드 셀·출력·`verification` 메타데이터로 만든 해시가 반영 전과 같음). 마감 게이트 `gates-after.json`(`--strict`) G1~G7 0, 코드 셀 24, 검사 문장 474. 리뷰 묶음은 다시 만들었고 반영 전 묶음은 `qa/upgrade/before/review-round1/review-pack/`에 있습니다.

## 남은 것

- 기기 `/tmp/ch07-04`(탐색 스크립트·`run1.ipynb`·`run2.ipynb`·visual 사본·치환 json·삽화 원본 `illus-04-5-a.png`·`illus-04-5-check.png`)는 정리 대상
- 옛 도식 `figures/04-메시지-템플릿.*`는 정리 대상 목록에만 적음(삭제하지 않음)
- 별도 세션 검토, 강사 확인
