# 01-계층-지도와-첫-호출 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`·`figures/01-layer-map.*`·`집필점검표.md`). 챕터 첫 절이라 챕터 전체 수정 전 게이트 `gates-before.json`을 먼저 남겼습니다(6절 합계 G1 13·G2 8·G3 0·G4 8·G5 81·G6 145·G7 18).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 2 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 1 | 0 |
| G5 | 13 | 0 |
| G6 | 32 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 8 | 15(준비 3) |
| 검사한 문장 | 167 | 349 |

G8: `run_section.sh` 새 커널 PASS(2026-09-16), `verify.py --chapter` PASS(6절), `visual.cjs` 1280px·390px PASS(공용 도구는 고치지 않고 `/tmp/ch06-01/vis/` 사본으로 실행. 처음 390px에서 학습 목표 「LangChain·LangGraph·DeepAgents를」이 끊기지 않는 한 낱말이 되어 가로 스크롤 → 쉼표로 고침).

## 수정 전 주요 문제

- G1: `[role for role, _ in messages]` 목록 내포식, `all(isinstance(...) for ...)` 제너레이터 식
- G4: 모델 셀에 `temperature=0` 없음(`max_tokens=180, timeout=30, max_retries=1`)
- 실패 장면이 실제 오류가 아님: 직접 쓴 `if not all(...)` 검사가 `raise TypeError`를 냄(본문도 「LangChain 내부 검증이나 실제 API 오류를 재현한 결과가 아닙니다」라고 적음). `raise`·`isinstance`·try `else`는 기본 경로 미교육
- G5: 제목 셀·핵심 그림 첨부·결과 읽기 셀 없음(13건)
- G6: 70자 초과 7, 영문 시작 22(「LangChain은」, 「`model`은」 등), 5문장 넘는 단락 3
- G7: Mermaid 0(옛 Excalidraw `01-layer-map.svg` 1장), 삽화 0, 설계표 없음
- 앞 챕터와 어긋남: b3 「Ch 5의 모델 선택표」(Ch 5 08에는 「선택표」 없음), 「그 기준으로 미리 고정한」(근거 없음), b5 「출력 상한」을 Ch 5 출력 몫과 잇지 않음, temperature 설명 없음, `.env` 무시 규칙 확인 없음

## 바꾼 것

- 모델: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(nbkit `key_and_model_cells`, 실행 날짜 줄). 키는 루트 `.env`에서만 읽고 값은 출력하지 않음. 모델 호출 4번(첫 호출·질문 바꾸기·출력 상한 12·After)
- 기본 경로: 설치(버전 4줄) → import → 키 → 모델 → 2절 객체 종류·`max_tokens` None(요청 0번) → 3절 튜플 목록을 `for role, content in messages:`로 출력 → 4절 `invoke` → 5절 `usage_metadata`·`response_metadata["finish_reason"]` → 6절 값 바꿔 보기 1(질문만) → 7절 값 바꿔 보기 2(`max_tokens=12`, 새 모델 객체) → 8절 Before(`questions.get("단점")` → `None` → 실제 `ValidationError`, 요청 전) → 9절 After(`get("단점", default_question)` → `AIMessage`, 객체 종류 `assert`)
- 실행 출력(2026-09-16): `ChatOpenAI`·`None`, `AIMessage`, 입력 36·출력 41·합계 77·`stop`, 출력 상한 12 → `LangChain 모델 인터페이스의 장점`·12·`length`, `2 validation errors for HumanMessage`, After `답: AIMessage`
- 라이브러리 확인(설치 버전 소스): 튜플 → `HumanMessage` 변환은 `langchain_core/messages/utils.py` `_convert_to_message`(1.6.2)에서 요청 전에 일어남(클라이언트 호출을 가로챈 탐색 실행에서 요청 0건). `pydantic_core.ValidationError`는 `ValueError`의 하위 클래스이지만 노트북은 `from pydantic import ValidationError`로 이름을 그대로 받음. `ChatOpenAI`에 `invoke`·`stream`·`batch`·`ainvoke` 있음, `BaseMessage.text`는 속성
- 탐색 실행(교재 밖, 기기 셸 `/tmp/ch06-01/probe_*.py`): 다른 질문으로 `max_tokens=12` 끊김(`length`)을 먼저 확인한 뒤 12로 정함 → 본문 b7·노트북 7절에 「끊기는 모습을 보려고 정한 예, 탐색 실행 뒤 정함」을 밝힘(규격 §3). 탐색 호출 2번(합계 모델 호출: 노트북 4 + 탐색 2 = 6)
- Ch 5 인계 반영: (1) temperature 0 ≠ `do_sample=False`(모델 셀 결과 읽기·b3 표·b7), (2) 출력 상한 `max_tokens` = 출력 몫 `max_new_tokens`, 모자라면 오류 없이 끊김 → 7절에서 실제로 확인하고 b5·용어 표·복습 5에 한 문장으로 이음, (3) 「모델 선택표」 → 「Ch 5 08절의 필수 조건과 선택 기준」, 이 모델을 그 절차로 비교하지 않았다고 적음, (4) 07절 판정 규칙 한계와 「질문 세 개·모델 하나·한 번 실행」 범위(b7·4절 결과 읽기), 토큰 수를 Qwen 조각 수와 비교하지 않음(5절·b5)
- Ch 3 인계: `.env`가 무시 규칙에 걸리는지 `git status --short --ignored`로 확인(키 셀 설명·b3 표·b7), 이미 커밋했으면 Ch 3 05절 순서로 폐기·교체(b7)
- A 트랙: `ValidationError`·Pydantic을 세 문장(뜻 → 택배 접수대 송장 → 노트북 오류)으로 풀고 Ch 2 10절 링크, 「A 트랙에서 건너뛰었다면」 한 문장. `@`·`BaseModel`·`*args`는 쓰지 않음
- 본문 10블록 다시 씀: 이 절의 질문, 앞에서 배운 내용 표(Ch 2 03·05, Ch 3 01·05, Ch 5 04·06·07·08), 네 범위 설명(뜻 → 창구 비유 → 노트북 모습), 세 제품 표(Ch 13·20·27 제목은 각 `chapter.json`에서 확인), 용어 표 9개, 호출 메서드 표(stream 04절 실행, batch·ainvoke 이 챕터에서 실행하지 않음), 복습 5문제(끊긴 답 추가)
- 그림: Mermaid 4장(01-1 계층 지도, 01-2 첫 호출 순서, 01-3 출력 상한 비교, 01-4 Before/After), 삽화 1장(01-5 상담 창구 회전 받침, job 5316229f-c92f-45b3-a562-9208ceda7568, 2크레딧, 1회 생성 통과, 저장 PNG 픽셀 대조 차이 0). 옛 `{{svg:01-layer-map}}`는 본문에서 뺌(파일은 `figures/`에 남기고 `before/figures/`에 사본)
- 옛 생성기: `labs/part2/ch06-langchain-start/_make_notebooks.py` 첫머리(`from __future__` 뒤)에 설명 주석 + `raise SystemExit(...)`. 실행하면 종료 코드 1로 멈추는 것 확인. 챕터 마감 때 `qa/upgrade/before/generators/`로 옮길 대상. `figures/_gen_figures.py`·`01-layer-map.*`는 정리 대상 목록에만 적음

## 검토

- 별도 세션 검토 1차(2026-09-17, `qa/upgrade/review-round1.md`): **accept**(상 0·중 0·하 2, 챕터 공통 C-1 반영 전제). 반영 결과(같은 날 마감 세션): C-1 준비물 요금 문장 「(06절 4절에서 2026-09-17에 확인한 공식 요금 기준)」, 01-1 b4 그림 읽기에 회전판 두 문장(단락을 둘로 나눔, 삽화는 다시 만들지 않음), 01-2 노트북 키 확인 설명에 「이 명령은 노트북 셀이 아니라 프로젝트 폴더의 터미널에서 실행합니다. 이 노트북은 그 결과를 출력하지 않습니다.」 결정 Q1(Before 빨강·출력 상한 12 실험·삽화 유지) 권고대로. 반영 방법: `mdpatch.py` → `run_section.sh … 01 --no-exec`(노트북 재실행 없음, 코드 셀·출력 그대로), 마감 게이트 `gates-after.json` G1~G7 0.
- 리뷰 묶음(반영 뒤 다시 만듦): `qa/upgrade/review-pack/`, 반영 전 묶음 `qa/upgrade/before/review-round1/review-pack/`
- 검토자가 볼 곳: (1) Before 빨강 판단(받아 출력했지만 받지 않으면 멈추는 결함 결과, Ch 4 05-3 선례), (2) 삽화의 둥근 판이 「회전 받침 = 루프」로 읽히는지(포함 관계는 뚜렷, 회전은 약함), (3) 7절 출력 상한 실험을 01절에 넣은 범위(Ch 5 인계를 실행으로 확인하려고 더함, 호출 1번)

## 남은 것

- 실행 환경: 기기 루트 여유 약 666MB라 가상환경을 `$ROOT/.cache/vm/venv-ch06-langchain-start`(uv 캐시 `$ROOT/.cache/vm/uv`)에 만듦. `run_section.sh`가 자동으로 씀. 전체 마감 때 `.cache/vm`과 함께 정리 대상
- 기기 `/tmp/ch06-01`(탐색 스크립트·visual 사본·옛 생성기 백업), `qa/upgrade/__pycache__`(생성기 컴파일 확인 때 생김)는 정리 대상
- 강사 확인
