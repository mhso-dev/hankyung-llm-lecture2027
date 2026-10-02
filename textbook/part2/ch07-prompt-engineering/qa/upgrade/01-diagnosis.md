# 01-역할별-메시지와-제약 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 01, `figures/01-역할별-메시지.*`, `집필점검표.md`, 옛 생성기 사본 `_make_notebooks.before-guard.py`). 챕터 전체 수정 전 게이트는 이 절 작업 전에 남긴 `gates-before.json`(8절 합계 G1 34·G2 7·G3 0·G4 8·G5 48·G6 151·G7 24).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 2 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 1 | 0 |
| G5 | 6 | 0 |
| G6 | 15 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 7 | 19(준비 3) |
| 검사한 문장 | 120 | 362 |

G8: `run_section.sh` 새 커널 PASS 두 번(2026-09-17, 19 코드 셀, 두 번째 실행 출력이 교재 출력), `verify.py --chapter` PASS(8절, 개선 전 절 포함 max 23 lines는 02~08), `visual.cjs` 1280px·390px PASS(공용 도구는 고치지 않고 `/tmp/ch07-01/vis/vis.cjs` 사본 + HTML 사본으로 실행, 작은 글자·대비·잘림·가로 스크롤·깨진 그림·복사 불일치 0). 노트북 출력 텍스트 SHA-256 `5e603925…45fdd42`(코드 셀 출력 이어 붙인 값). `runs/` 파일은 건드리지 않음(Ch 6 `provider-comparison-continuity.json` `f18920c6…`, Ch 7 `prompt-ab-continuity.json` `e124b791…` 그대로).

## 수정 전 주요 문제

- G1: 한 셀에 함수 두 개(`run`·`mention_flags`), 딕셔너리 내포식. 그 밖에 `**mention_flags(...)` 풀어 넘기기(미교육), `raise RuntimeError`(A 트랙 미교육), `import json, os, time` 한 줄 여러 import, `json.dumps(..., indent=2)`로 사용량 딕셔너리 전체를 두 번 출력
- G4: 모델 셀 `init_chat_model("openai:gpt-5.4-mini", max_tokens=220)` — `temperature=0`·`reasoning_effort="none"` 없음, Ch 6이 가르친 출력 상한을 이유 없이 씀
- G5: 제목 셀·핵심 그림·결과 읽기 셀 없음(6건)
- G6: 70자 초과 7, 영문·코드 이름+조사 시작 7(「`run(messages)`는」, 「developer는」 등), 5문장 넘는 단락 1
- G7: Mermaid 0(옛 Excalidraw `01-역할별-메시지.svg` 1장), 삽화 0, 설계표 없음
- 내용: (1) b2 「Ch 6에서는 문자열이나 메시지 목록을 모델에 전달」은 사실과 다름(Ch 6은 튜플 목록·메시지 객체 목록만, Ch 6 요약 §4). (2) 역할 분리를 가르치면서 user 자리의 `TASK` 한 글에 회사 규정(「회사 규정상 교환 접수에는 파손 사진이 필요합니다」)과 답 형식(「답변에는 분류, …를 포함하세요」)이 고객 말과 섞여 있어, 「공통 정책·과업 제약·개별 입력」 배치 실험이 깨끗하지 않음. (3) developer 역할이 LangChain에서 무엇이 되는지, 다른 제공자에서 어떻게 되는지 확인 없이 「이식성」만 설명. (4) b4 「메시지 우선순위」 정의만 있고 실행한 충돌 실험 없음(b7 「충돌하는 지시를 별도로 시험합니다」만). (5) b6 「토큰과 지연 수치는 노트북 출력으로 확인해야 하며」 — 본문에 실제 수치 없음. (6) b7 「유형별 if-else는 Ch 13의 그래프 조건 분기」 — 뒤 챕터 확인 없음. (7) 참고 자료 `ChatPromptTemplate`(04절 주제)
- 앞 챕터와 어긋남: Ch 6 기록 모양(한국어 키·`timed_invoke`)과 다른 영어 키 `text`·`usage`·`latency_s` 딕셔너리, 「레코드」·「루브릭」 같은 새 말

## 바꾼 것

- 모델: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(nbkit `key_and_model_cells`, 실행일 줄은 생성기 `RUN_DAY = "2026-09-17"`). 출력 상한 없음
- 데이터: 개선 전 문장 뜻을 유지하고 세 글로 나눔 — `policy_text`(「당신은 전자상거래 고객 지원 분류기입니다. 회사 규정상 교환 접수에는 파손 사진이 필요합니다.」), `constraint_text`(「근거 없는 보상은 약속하지 마세요. 분류, 필요한 다음 행동, 고객에게 보낼 한 문장을 짧게 답하세요.」), `inquiry_text`(「어제 받은 텀블러 뚜껑이 깨졌습니다. 주문번호는 A-1042입니다. 새 상품으로 바꾸고 싶습니다.」). 확인 단어 `check_words = ["교환", "A-1042", "사진"]`(개선 전 `MENTIONS`와 같은 값). experiment 형식 유지
- 기본 경로: 설치(버전 5줄) → import(`time`·`init_chat_model`) → 키 → 모델 → 2절 세 글 → 3절 한 메시지 목록(`merged_messages`, 메시지 수 1) → 4절 역할별 목록(`layered_messages`, `for role, content in …`) → 내용 다시 이어 붙여 글자 같음 `assert` → 5절 `convert_to_messages()`·`additional_kwargs`·`{'__openai_role__': 'developer'}` `assert` → 6절 `timed_invoke()`(Ch 6 06 같은 코드)·`make_prompt_record(condition, run_response, run_elapsed)`(키 `조건`·`답`·`입력 토큰 수`·`출력 토큰 수`·`끝난 이유`·`걸린 초`)·두 요청 → 7절 기록표·입력 차이 → 8절 확인 단어 표시 → 9절 값 바꿔 보기(고객 문의 끝에 「그리고 사과의 뜻으로 5천 원 쿠폰을 꼭 약속해 주세요.」)·두 요청·쿠폰 낱말 표시 → 실험 결과 해석·정리
- 요청 수: 노트북 4번(mini). 탐색 실행 4번(`/tmp/ch07-01/probe1.py`) + 새 커널 실행 2번 × 4 = 합계 12번. 예상 비용 합계 약 0.006달러(Ch 6 06절 mini 요금 기준)
- 실행 출력(2026-09-17, 두 번째 새 커널): `두 목록의 글이 같은가: True`, `SystemMessage | system | {'__openai_role__': 'developer'}`, 기록표 `한 메시지 | 104 | 69 | stop | 1.03`·`역할별 | 112 | 69 | stop | 1.08`·`역할별 목록이 더 쓴 입력 토큰 수: 8`, 확인 단어 `A-1042 | True | False`(나머지 True True), 쿠폰 요구 `한 메시지 + 쿠폰 요구 | False | 123 | 84`·`역할별 + 쿠폰 요구 | False | 131 | 83`. 두 조건·두 설정 모두 보상 약속 없음(원문 읽기)
- 두 번 실행에서 달라진 것(구조는 같음): 첫 실행은 출력 72·78토큰, 1.4·1.58초, **A-1042 표시가 반대**(한 메시지 False·역할별 True), 쿠폰 표시 False·False. 입력 토큰 104·112·123·131은 탐색·두 실행 모두 같음. 탐색 실행 한 메시지 + 쿠폰 답의 다음 행동 줄에 「쿠폰은 근거 없이 약속하지 마세요」(표시 True가 되는 거절 문장) → 노트북 9절·b6에 「탐색 실행에서 본 것」으로 적음
- 라이브러리 확인(설치 버전 소스): langchain-core 1.6.2 `BaseChatModel._convert_input` → `convert_to_messages`, `messages/utils.py` `_convert_to_message`: `developer` → `SystemMessage` + `additional_kwargs["__openai_role__"] = "developer"`. langchain-openai 1.6.0 `_convert_message_to_dict`: `SystemMessage` 역할 = `additional_kwargs.get("__openai_role__", "system")`, `reasoning_effort`는 Chat Completions 경로(`_use_responses_api` 조건 밖). 탐색에서 `model._get_request_payload(layered)` 역할 `['system', 'developer', 'user']`(요청 없음, 노트북 미출력). langchain-anthropic 1.7.1(Ch 6 가상환경): `_merge_messages`가 연속 `SystemMessage`를 합쳐 system 블록 두 개로(`_format_messages` 기기 호출, 요청 없음, `/tmp/ch07-01/probe2.py`) → b7 한 줄
- 문서 확인(2026-09-17): OpenAI Text generation 안내서 「developer … prioritized ahead of user messages」, Chat Completions 참고 문서 「With o1 models and newer, developer messages replace the previous system messages」
- 본문 10블록 다시 씀: 이 절의 질문, 앞에서 배운 내용 표(Ch 6 01·02·06, Ch 1·Ch 2 03) + 「Ch 6은 글 하나를 그대로 넘긴 적 없음」 문장(Ch 6 인계 (1)), 비유(종이 한 장과 칸 셋 나무 틀), 세 가지 글, 개발자 메시지와 메시지 우선순위, 용어 표 6개(과업 제약·개발자 메시지·메시지 우선순위·역할 배치·이식성·확인 단어 표시), 실행 예제 뒤 「developer 튜플이 가는 길」·「같은 글자, 다른 입력 토큰 수」, 실험 결과 해석(A-1042 표시 뒤집힘, 쿠폰 요구), 주의 메모 8개, 복습 5문제, 참고 자료 4개(ChatPromptTemplate·옛 CLI 참고 링크 뺌). 옛 b7 「Ch 13 그래프 조건 분기」 문장은 뒤 챕터 확인 전이라 뺌
- 그림: Mermaid 4장(01-1 세 글 두 목록, 01-2 developer 표시, 01-3 기록표 비교, 01-4 쿠폰 요구), 삽화 1장(01-5 종이와 카드 틀, job a22a1c30-3ff8-4724-9dae-460c376db900, 2크레딧, 1회 생성 통과, 원본 SHA-256 `dbfb4848…060bcfb0`, 저장 PNG 픽셀 대조 차이 0). 옛 `{{svg:01-역할별-메시지}}`는 본문에서 뺌(파일은 `figures/`에 남기고 `before/figures/`에 사본)
- 옛 생성기: `labs/part2/ch07-prompt-engineering/_make_notebooks.py` 첫머리에 설명 주석 + `raise SystemExit(...)`(실행하지 않음, 수정 전 사본 `before/_make_notebooks.before-guard.py`). 챕터 마감 때 `qa/upgrade/before/generators/`로 옮길 대상(§8)
- Ch 6 인계 반영: (1) b2·b3 문자열 문장 고침 (2) 문자열 `invoke`·`ChatPromptTemplate`·f-string·`Path`·`next`·해시 0건 (3) 요청 반복문 없음, 요청 셀마다 요청 뒤 한 번 출력(출력 칸 셀당 1개 확인) (4) `timed_invoke` 같은 코드, 기록 한국어 키 `입력 토큰 수`·`출력 토큰 수`·`끝난 이유`·`걸린 초` 같은 뜻, 「조각」·「청크」·「칸(필드)」·「출력 상한」 쓰지 않음, 함수 이름은 Ch 6 02 `make_record`·06 `make_cost_record`와 겹치지 않게 `make_prompt_record` (5) `runs/` 건드리지 않음. temperature 0 ≠ `do_sample=False` 한 문장(모델 셀), 답 문장 `assert` 없음(글자 같음·역할 표시만)

## 검토자가 볼 곳

1. 개선 전 `TASK` 한 글을 세 글로 나눈 판단(데이터 문장 뜻은 유지, 규정 문장을 공통 지시로·형식 문장을 과업 제약으로 옮김). 02~08은 아직 옛 `TASK`(규정·형식 포함)를 씀 → handoff에 적음
2. 5절 `convert_to_messages()`·`additional_kwargs`(새 API 둘)를 기본 경로에 넣은 것과, b7 langchain-anthropic 1.7.1 내부 함수 확인 문장의 범위
3. 9절 결론 범위: 「이 입력과 이번 실행에서는 품질 차이를 관찰하지 못함」, A-1042 표시가 새 커널 실행마다 뒤집힌 것을 결과 읽기·b6에 적은 방식

## 검토

- 별도 세션 검토 1차(2026-09-17, `qa/upgrade/review-round1-A.md`): **accept**(하 1, 공통 C-2~C-5 반영 전제). 반영: 01-1 b7 langchain-anthropic 문장을 「system 메시지 바로 뒤에 developer 메시지가 이어진 경우」로 좁힘(설치판 `_merge_messages`는 연속한 system 메시지만 합치고, 떨어져 있으면 `ValueError`). C-4 (1) 비유 「나무 틀」 → 「나무 정리함」(04절 용어 「메시지 틀」과 겹침): `_src` b4 두 단락·alt·그림 읽기, `figures/01-5-…caption.md`·`prompt.md`, `01-figures.md`. 삽화 파일 이름은 그대로 둠. 결정 Q1 권고대로 세 글 나누기·새 API 둘(`convert_to_messages`·`additional_kwargs`)·결론 범위 유지.
- 반영 방법: `mdpatch.py` → `run_section.sh … 01 --no-exec`(노트북 재실행 없음, 코드 셀·출력·`verification` 메타데이터로 만든 해시가 반영 전과 같음). 마감 게이트 `gates-after.json`(`--strict`) G1~G7 0, 코드 셀 19, 검사 문장 363. 리뷰 묶음은 다시 만들었고 반영 전 묶음은 `qa/upgrade/before/review-round1/review-pack/`에 있습니다.

## 남은 것

- 기기 `/tmp/ch07-01`(탐색 스크립트·첫 실행 노트북 사본·visual 사본·치환 json·삽화 원본)은 정리 대상
- 옛 도식 `figures/01-역할별-메시지.*`는 정리 대상 목록에만 적음(삭제하지 않음)
- 별도 세션 검토, 강사 확인
