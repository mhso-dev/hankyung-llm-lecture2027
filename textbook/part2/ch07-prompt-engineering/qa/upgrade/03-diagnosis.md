# 03-Few-shot-예시-선택 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 03, `figures/03-Few-shot-선택.*`). 수정 전 게이트는 챕터 `gates-before.json`의 03 행.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 2 | 0 |
| G2 | 1 | 0 |
| G3 | 0 | 0 |
| G4 | 1 | 0 |
| G5 | 5 | 0 |
| G6 | 14 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 7 | 22(준비 3) |
| 검사한 문장 | 107 | 407 |

G8: `run_section.sh` 새 커널 PASS 두 번(2026-09-17, 22 코드 셀, 두 번째 실행 출력이 교재 출력), 결과 읽기·본문은 `mdpatch.py` 세 번 → `--no-exec`로 렌더·첨부·빌드·verify(`PASS 8 sections / 97 code cells`)·게이트 0. `visual.cjs` 1280px·390px PASS(공용 도구는 고치지 않고 `/tmp/ch07-03/vis/vis.cjs` 사본 + HTML 사본, 작은 글자·대비·잘림·가로 스크롤·깨진 그림·복사 불일치 0). 코드 셀 출력 칸은 셀마다 1개(요청 반복문 없음). 노트북 코드 셀 출력 텍스트 이어 붙인 SHA-256 `8fbb98d1…18419ce4654`. `runs/` 파일은 건드리지 않음(Ch 7 `prompt-ab-continuity.json` `e124b791…` 그대로).

## 수정 전 주요 문제

- G1: 한 셀에 함수 두 개(`run`·`mention_flags`), 딕셔너리 내포식. 그 밖에 `raise RuntimeError`(A 트랙 미교육), `import json, os, time` 한 줄, `json.dumps(…, indent=2)`로 사용량 딕셔너리 전체 출력(영어 키 `text`·`usage`·`latency_s`), `{"zero_shot": …}.items()` 반복
- G2: 비교 셀 `print(…, json.dumps(mention_flags(…)))` 두 겹 호출
- G4: 모델 셀 `init_chat_model("openai:gpt-5.4-mini", max_tokens=220)` — `temperature=0`·`reasoning_effort="none"` 없음
- G5: 제목 셀·핵심 그림·결과 읽기 셀 없음(5건)
- G6: 70자 초과 5(데이터 누출 정의, 예시 설명, `relevant_example + "\n\n" + TASK` 설명, 참고 자료 두 줄), 영문 시작 8(「Zero-shot과」「Few-shot의」「LangChain은」「`run(messages)`는」 등), 5문장 넘는 단락 1
- G7: Mermaid 0(옛 Excalidraw `03-Few-shot-선택.svg` 1장), 삽화 0, 설계표 없음
- 내용: (1) 01·02가 나눈 글과 다른 옛 대문자 `TASK`(규정·형식·고객 말이 한 글)를 user에 넣고 system에 「분류/다음 행동/고객 문장 형식으로 답하세요」를 둬, 02 과업 명세 목록에서 「예시만 더한다」가 이어지지 않음. (2) 예시 답이 `분류=… / 다음 행동=… / 고객 문장=…` 한 줄 모양이라 system 형식 문장과 모양이 달라, 「관련 예시가 A-1042를 생략」한 원인이 예시 관련성인지 예시 모양인지 가릴 수 없음. (3) b6 표의 102·156·150토큰, 183·196·214 등은 옛 실행(2026-09-09) 값이고 모델 설정이 규격과 다름. (4) 정의 6개 `<dl>`만 있고 일상 예·코드 모습 없음, 감정 분류 경계 사례는 실행과 무관. (5) 참고 자료 LangChain Memory concepts·LangSmith quickstart는 이 절 주장과 연결이 약함. (6) b3 「02절에서 과업과 출력 형식을 말로 지정」은 맞지만 developer 자리라는 점이 빠짐
- 앞 절·앞 챕터와 어긋남: 01·02·Ch 6 기록 모양(한국어 키·`timed_invoke`·`make_prompt_record`)과 다른 영어 키, 「raw 응답」「표본」 같은 말, `TASK`·`MENTIONS` 대문자 이름

## 바꾼 것

- 모델: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(nbkit `key_and_model_cells`, 실행일 줄 `RUN_DAY = "2026-09-17"`). 출력 상한 없음
- 데이터(02 인계 반영): 2절에서 02의 `persona_text`·`inquiry_text`·`goal_text`·`required_text`·`forbidden_text`·`format_text`·`task_text`를 글자까지 같게 다시 만듦. 예시 없음 목록 `zero_messages`는 02 `task_messages`와 같은 목록(입력 134토큰, 02와 같음). 예시 두 개는 개선 전 주제(셔츠 단추·B-203 / 뉴스레터 글꼴)를 유지하고 답을 02 출력 형식 세 줄(`분류:`·`다음 행동:`·`고객에게 보낼 한 문장:`)로 새로 씀. `make_example_text(example_inquiry, example_answer)`가 「예시 문의:」「예시 답:」 줄을 붙임. developer 글 = `task_text + "\n\n" + 예시 글`(`"\n\n"` = 빈 줄 하나, 처음 쓰는 자리에서 한 문장). 확인 단어 `check_words` 01·02와 같음, 새 `example_words = ["B-203", "단추", "글꼴"]`
- 예시 자리 결정(02 인계 「예시를 developer 안에 넣는지 한 문장으로」): OpenAI Prompt engineering 안내서(2026-09-17 확인) 「Typically, you will provide examples as part of a developer message」에 따라 developer 글 안, 과업 명세 뒤. user/assistant 메시지 쌍으로 넣는 방법과 langchain-core 1.6.2 `FewShotChatMessagePromptTemplate`·example selector(`langchain_core/example_selectors/`)는 설치 소스로 이름만 확인하고 「실행하지 않음」(b7)
- 조건 설계: 세 목록 `[("system", persona), ("developer", 개발자 글), ("user", inquiry)]`, system·user 같음을 `==`·`and` + `assert`로 확인. 값 바꿔 보기는 관련 예시 답의 줄바꿈 두 곳만 ` / `로 바꾼 `oneline_answer`(낱말 같음, 개선 전 예시의 한 줄 모양을 이어 받음)
- 기본 경로: 설치 → import(`time`·`init_chat_model`) → 키 → 모델 → 2절 02 글 → 3절 함수 정의·관련 예시·관련 없는 예시 → 4절 developer 글·줄 수 10·세 목록 `assert` → 5절 `timed_invoke()`·`make_prompt_record()`(01·02 같은 코드)·세 요청 → 6절 기록표·예시가 더한 입력 → 7절 첫 줄(가운데 두어 줄 끝 공백이 보이게)·글자 수·줄 수 → 8절 확인 단어·예시 낱말 → 9절 한 줄 모양 예시·요청·나란히 보기 → 실험 결과 해석·정리
- 요청 수: 노트북 4번(mini). 탐색 실행 5번(`/tmp/ch07-03/probe1.py` 네 조건: 예시 없음·관련·관련 없음·개선 전 한 줄 예시 답 그대로, `probe2.py` 낱말은 두고 줄바꿈만 바꾼 한 줄 예시) + 새 커널 실행 2번 × 4 = 합계 13번. 예상 비용 합계 약 0.01달러 미만(Ch 6 06절 mini 요금 기준)
- 실행 출력(2026-09-17, 두 번째 새 커널): 기록표 `예시 없음 | 134 | 97 | stop | 1.48`·`관련 예시 | 225 | 75 | stop | 1.22`·`관련 없는 예시 | 211 | 86 | stop | 1.03`, 더한 입력 91·77, 답 모양 첫 줄 「분류: 파손으로 인한 교환 문의」(줄 끝 공백)·「분류: 교환 요청(파손)」·「분류: 교환 문의」(줄 끝 공백), 156·119·144자, 모두 3줄, 확인 단어 모두 True, 예시 낱말 모두 False, 한 줄 예시 `관련 예시 | 225 | 75 | 119 | 3 | True`·`한 줄 모양 관련 예시 | 225 | 76 | 123 | 2 | True`. 원문: 관련 예시 답 다음 행동 줄 「파손 사진을 받아 주문번호 A-1042로 교환 접수를 진행합니다」(예시 「떨어진 단추 사진을 받고 주문번호 B-203으로 교환 접수를 진행합니다」와 같은 문장 모양), 한 줄 예시 답은 분류·다음 행동을 ` / `로 이은 첫 줄 + 고객 문장 둘째 줄. 네 답 모두 보상 약속 없음(원문 읽기)
- 두 번 실행에서 달라진 것(구조는 같음): 첫 실행은 출력 83·75·85토큰, 144·119·141자, 1.36·1.23·1.29초, 한 줄 예시 답은 세 부분 모두 ` / `로 이은 1줄(77토큰 127자). 입력 134·225·211·225는 탐색·두 실행 모두 같음. 관련 예시 답은 두 새 커널 실행에서 글자까지 같았음. 한 줄 예시 줄 수: 탐색 2·첫 실행 1·둘째 실행 2 → 본문 b6에 「한 번도 세 줄이 되지 않음」까지만. 개선 전 한 줄 예시 답을 그대로 쓴 탐색 답도 1줄
- 결과 읽기 작성 방식: 모델 출력에 기대는 결과 읽기 9곳은 생성기에 `[[READ_…]]` 자리 표시로 두고 두 번째 새 커널 뒤 `mdpatch.py`(`/tmp/ch07-03/reps1.json`)로 생성기·노트북에 함께 채움. **생성기에는 채운 글이 남아 있음**(Ch 6 07 인계의 「자리 표시가 남은 생성기」 문제 없음). 다시 실행하면 결과 읽기를 새 출력과 다시 대조해야 함
- 문서·소스 확인(2026-09-17): OpenAI Prompt engineering(Few-shot learning 「including a handful of input/output examples in the prompt, rather than fine-tuning」, 「show a diverse range of possible inputs」, 예시는 developer 메시지의 한 부분), langchain-core 1.6.2 `prompts/few_shot.py`(`FewShotPromptTemplate`·`FewShotChatMessagePromptTemplate`)·`example_selectors/`(`LengthBasedExampleSelector`·`SemanticSimilarityExampleSelector` 등)
- 본문 10블록 다시 씀: 학습 목표 4, 이 절의 질문, 앞에서 배운 내용 표(02·01·Ch 6 01·06·Ch 2 04·Ch 1) + 02 목록을 그대로 둔다는 단락·예시 자리 단락·개선 전 설계 단락, 비유(02 책상 두 개 → 세 개, 클립보드 집게의 견본 카드), 예시·Zero-shot·Few-shot, 관련성, 예시 값·데이터 누출, 용어 표 6개, 실행 예제 뒤 「세 조건의 기록」, 실험 결과 해석(표시 모두 True·원문 문장 모양·분류 이름 원인 보류·출력 토큰 차이 보류·세 번 실행 범위·개선 전 결과와 비교 보류) + 「예시 답 모양만 바꾸면」, 주의 메모 9개(탐색 실행과 첫 줄 출력을 답을 본 뒤 정했다는 사실 포함, 규격 §3), 복습 5문제, 참고 자료 3개
- 그림: Mermaid 4장(03-1 예시가 들어가는 자리, 03-2 세 조건 기록, 03-3 예시에서 따라온 것, 03-4 예시 답 모양만 바꾸기), 삽화 1장(03-5 견본 카드, job a08db0f8-7878-4715-abb8-c1e9368cd995, 2크레딧, 1회 생성 통과, 원본 SHA-256 `1b99b0b7…6bed841c`, 저장 PNG 픽셀 대조 차이 0). 옛 `{{svg:03-Few-shot-선택}}`은 본문에서 뺌(파일은 `figures/`에 남기고 `before/figures/`에 사본). 빨강 0장, 파랑 0장
- Ch 6·01·02 인계 반영: 문자열 `invoke`·`ChatPromptTemplate`(코드)·f-string·`Path`·`next`·해시·`join`·`strip`·`startswith`·`count`·`+=` 0건. 요청 반복문 없음(요청 셀마다 요청 뒤 한 번 출력). `timed_invoke`·`make_prompt_record`·한국어 키·기록표 모양·확인 단어·조건 이름 방식 01·02와 같음. 그림 색 01·02와 같음(넣은 글 초록·모델 보라·확인 값 노랑·정하지 않는 것 회색). 「조각」·「청크」·「칸(필드)」·「출력 상한」 쓰지 않음. `runs/` 건드리지 않음. temperature 0 ≠ `do_sample=False` 한 문장(모델 셀), 답 문장 `assert` 없음(튜플 같음·줄 수 없음)

## 검토자가 볼 곳

1. 조건 설계: 예시를 developer 글 안(과업 명세 뒤)에 둔 결정과, 예시 답을 02 출력 형식 세 줄로 새로 쓴 것(개선 전 한 줄 모양 예시는 9절 값 바꿔 보기로 옮김). 「관련 예시 A-1042 생략」이라는 개선 전 관찰을 b6에서 「설정이 여러 곳 달라 한 원인으로 말하지 않음」으로 처리한 방식
2. 결론 범위: 관련 예시 답의 「문장 모양을 따름」을 세 번 본 모양으로 적고, 분류 이름·출력 토큰 차이·한 줄 예시 줄 수(2·1·2)의 원인은 보류한 문장(b6·노트북 5·6·9절)
3. 7절 첫 줄을 가운데 둔 출력(줄 끝 공백이 ` |` 앞 빈칸으로 보임)을 탐색 뒤 정했다고 b7에 밝힌 문장, 삽화 03-5의 명찰 모양이 02-5와 조금 다르다는 검수 메모

## 검토

- 별도 세션 검토 1차(2026-09-17, `qa/upgrade/review-round1-A.md`): **accept**(하 2, 공통 C-2 반영 전제). 반영: C-2(중) b3 셋째 단락을 「01·02절이 회사 규정·답 형식·고객 말을 … 나눴으므로」로, b6 「개선 전 이 절(2026-09-09)」 단락 삭제, b7 일곱째 항목 「낱말도 조금 다른 한 줄 예시 답」, 노트북 [39] 개선 전 두 문장·[41] 한 문장 삭제. 03-1 그림 03-3 「따라온 것」 라벨을 「다음 행동 줄 문장 모양」으로 고쳐 다시 렌더(PNG 확인, 폭 502), 도식 읽기 「줄 수 3은 예시 없음 답도 같아서 예시에서 왔다고 하지 않습니다」, alt·`caption.md`·`03-figures.md`. 03-2 b8·노트북 정리 「튜플로 적은 메시지 목록」(권고 「튜플을 직접 적어 만든」은 b8 문장이 G6 70자를 넘어 줄임). C-1 강의·실습 범위 문장(노트북 준비물·b5): 강의 3~7절, 실습 8·9절 — **강사 확인 대상**. 결정 Q3 권고대로 예시를 developer 글 안에 둔 설계·결론 범위 유지.
- 반영 방법: `mdpatch.py` → `run_section.sh … 03 --no-exec`(노트북 재실행 없음, 코드 셀·출력·`verification` 메타데이터로 만든 해시가 반영 전과 같음). 마감 게이트 `gates-after.json`(`--strict`) G1~G7 0, 코드 셀 22, 검사 문장 404. 리뷰 묶음은 다시 만들었고 반영 전 묶음은 `qa/upgrade/before/review-round1/review-pack/`에 있습니다.

## 남은 것

- 기기 `/tmp/ch07-03`(탐색 스크립트·`run1.ipynb`·`run2.ipynb`·visual 사본·치환 json·삽화 원본 `illus-03-5-a.png`·`illus-03-5-check.png`)는 정리 대상
- 옛 도식 `figures/03-Few-shot-선택.*`는 정리 대상 목록에만 적음(삭제하지 않음)
- 작업 중 챕터 전체 wip 게이트를 한 번 실행해 `qa/upgrade/gates-wip.json`(8절 전체 wip)이 새로 생김 → 정리 대상
- 별도 세션 검토, 강사 확인
