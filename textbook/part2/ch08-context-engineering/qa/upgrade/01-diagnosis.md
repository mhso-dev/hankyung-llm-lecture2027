# 01-컨텍스트와-토큰-예산 — 품질 개선 진단과 결과

작성 2026-09-17. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`·`html`·`notebooks`의 01, `figures/01-*`, 옛 빌더 사본 `_build.before-upgrade.py`, 옛 생성기 사본 `_make_notebooks.before-guard.py`). 챕터 전체 수정 전 게이트는 이 절 작업 전에 남긴 `gates-before.json`(6절 합계 G1 4·G2 6·G3 2·G4 6·G5 80·G6 159·G7 17 = 274, 0/6).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 0 | 0 |
| G3 | 0 | 0 |
| G4 | 1 | 0 |
| G5 | 12 | 0 |
| G6 | 25 | 0 |
| G7 | 2 | 0 |
| 코드 셀 | 13 | 22(준비 3) |
| 검사한 문장 | 172 | 405 |

G8: `run_section.sh` 새 커널 PASS 두 번(2026-09-17 09:24·09:25, 22 코드 셀, 두 실행의 `outputs_sha256` 모두 `b790d25d2d4da658fe4e30f5757bbf63d6a25f46b32826eeab55ab17379707b3` — 출력 글자까지 같음). 이 챕터는 `chapter.json`이 없어 `run_section.sh`가 verify를 건너뛰므로 `verify.py --chapter textbook/part2/ch08-context-engineering`를 따로 실행해 `PASS 6 sections / 89 code cells (max 25 lines)`(max 25는 개선 전 02~06). 빌드 HTML에 치환 안 된 `{{` 0건, `figure.mmd` 4·`figure.illustration` 1. `visual.cjs` 1280px·390px PASS(공용 도구는 고치지 않고 `/tmp/ch08-01/vis/vis.cjs` 사본 + HTML 사본). `runs/` 파일은 읽지도 쓰지도 않음(`context-design-continuity.json` `88b3520b…`·수정 시각 2026-09-09 17:40 그대로, Ch 7 `a8aaafb7…`, Ch 6 `f18920c6…`). Ch 8 `test_ch06_ch08_continuity.py`는 작업 전후 같은 결과(3 통과·알려진 실패 2, Ch 7 요약 §9).

## 수정 전 주요 문제

- G4: 모델 셀 `init_chat_model("openai:gpt-5.4-mini", reasoning_effort="none", max_tokens=300)` — `temperature=0` 없음
- G5: 제목 셀·핵심 그림 없음, 결과 읽기 셀 없음 9건, 마지막 After 코드 뒤 설명 없음
- G6: 70자 초과 17(참고 자료 4 포함), 영문+조사 시작 1(「`return`은」), 5문장 넘는 단락 6
- G7: Mermaid 0(옛 Excalidraw `01-컨텍스트-예산.svg`), 설계표 없음. 옛 삽화 `01-책상-예산.png`(2026-09-08, 두 책상·선반)는 있었지만 `{{img:이름|alt}}` 두 칸 모양
- 사다리 밖 문법(게이트가 세지 않은 것): `raise FileNotFoundError`·`raise RuntimeError`·`raise ValueError`·`raise AssertionError`(A 트랙 미교육, Ch 7 요약 §5), 함수 안 `raise`, try `else`, f-string 삼중 따옴표 프롬프트(Ch 6·7 기본 경로 0건), 타입힌트 `-> int`, 영어 라벨 `input_tokens:`
- 내용: (1) b3 「특정 함수 이름을 가정하지 않고」 — Ch 6·7이 가르친 `init_chat_model`·튜플 목록·`usage_metadata`를 잇지 않음. (2) b4 「이 장의 노트북은 `max_tokens=300`으로 생성 상한」인데 예산 계산 `input_budget(4096, 300, 128)`과 모델 설정이 따로 놀고, 값 바꿔 보기(300 → 600)는 산술만(본문도 「모델 설정은 바뀌지 않는다」고 인정). (3) 실패 재현이 `total=300`으로 함수가 `ValueError`를 내는 것뿐이라 모델 호출이 없고, 「출력 예약분을 먼저 떼야 하는 이유」가 실제로 보이지 않음. (4) 추정 42토큰(prompt 글만)과 실제 66토큰(system 포함)을 비교해, 차이가 system 메시지를 빼고 센 탓인지 형식 표시 탓인지 섞임. (5) 용어 「출력 예약분」을 Ch 5 04 「출력 몫」·Ch 6 01 「출력 상한」과 잇는 문장 없음(Part 1 과정 요약 §5 인계). (6) 「수업 예산」과 모델 한도 400,000을 말로만 구분, 참고 자료 확인일 2026-09-08. (7) b2 「어떤 자료를 포함할지 모델이 스스로 판단하고 도구를 호출하는 단계는 Ch 20부터」 — 뒤 챕터 확인 없음
- 앞 챕터와 어긋남: Ch 7 메시지 모양(system 페르소나·developer 과업 명세·user)을 쓰지 않고 system 「근거에 있는 정보만…」 + user f-string. 근거 표기 `[E01 p.2] 정기 휴관일은 매주 월요일입니다.`는 E01 원문(「매주 월요일은 정기 휴관일 입니다.」)과 문장 순서가 다름

## 바꾼 것

- **빌더(`_build.py`, 이 절에서 먼저 처리, PLAYBOOK §2 7단계)**: `textbook/_template/builder.py`의 `_inline_mermaid`·`_inline_img`와 같은 출력을 내는 `inline_mermaid(spec)`·`inline_illustration(name, spec)`을 더함. `{{mermaid:이름|alt|캡션}}` → `<figure class="mmd">`(SVG 폭 `min(760, viewBox 폭)`, `role="img" aria-label`), `{{img:이름|alt|캡션}}` → `<figure class="illustration">` + `<figcaption>`. **두 칸 `{{img:이름|alt}}`은 개선 전과 같은 `<img alt>`**(alt를 이스케이프하지 않는 옛 동작까지 유지). 치환 뒤 `{{svg|img|mermaid|notebook|code|output:` 토큰이 남으면 `ValueError`로 멈춤. `{{notebook:slug}}`·`|example`·`|failure`는 원래부터 공용 `render.expand_notebooks`가 처리(규격대로 동작 확인). 확인: (a) 바꾸기 전 다시 빌드한 7개 HTML = 디스크 HTML(해시 같음), (b) 바꾼 뒤 다시 빌드한 7개 HTML = (a)와 해시 같음(01 `_src`가 옛 두 칸 `{{img:}}`일 때), (c) Ch 7 그림으로 `inline_mermaid`·세 칸 `inline_illustration`·빈 캡션 출력이 `_template/builder.py`와 문자열까지 같음(`/tmp/ch08-01/tokentest.py`), (d) 01 개선 뒤에도 02~06·index HTML 해시 같음. 공용 도구(`_template`, `_notebook`)는 고치지 않음
- **옛 생성기**: `labs/part2/ch08-context-engineering/_make_notebooks.py`의 `from __future__ import annotations` 바로 뒤에 설명 주석 + `raise SystemExit(...)`(실행하면 종료 코드 1로 멈춤 확인). 실행하지 않음. 챕터 마감 때 `qa/upgrade/before/generators/`로 `mv -n`
- 모델: `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(출력 상한 없음, `출력 상한(max_tokens): None` 출력). Before·After는 같은 설정에 `max_tokens`만 준 모델 객체를 새로 만듦(Ch 6 01 모양). 키 셀은 nbkit `KEY`, 실행일 줄은 생성기 `RUN_DAY = "2026-09-17"`
- 데이터: 개선 전 질문(미르시립도서관 정기 휴관일)·출처 표시 `[E01 p.2]`를 유지하고, 근거를 Ch 9가 쓰는 `labs/data/rag-corpus/build/html/E01.html` 2쪽 「2. 이용 시간」 원문으로 바꿈(원문 줄바꿈 「정기 휴관일\n입니다」만 붙여 씀). 질문에 「공휴일이 월요일과 겹치면 어떻게 되나요?」를 더해 답이 두 가지 사실을 담게 함(Before에서 끊긴 답이 무엇을 잃는지 보이게). 긴 자료는 같은 쪽 「1. 도서관 소개」 두 문단과 구역별 이용 시간 표(6행을 `|`로 이은 글). `data/memory.json`은 읽지 않음(02·06 테스트 대상, 바꾸지 않음). paired 형식 유지
- 기본 경로: 설치(버전 6줄) → import(`tiktoken`·`init_chat_model`) → 키 → 모델 → 2절 페르소나·과업 명세 / 근거·질문 / 소개 문단·구역 표(`len`) → 3절 user 글·Ch 7 모양 목록·`intro_text in user_text` False·메시지 수 `assert` → 4절 `input_budget(total_budget, output_reserve, safety_margin)`(뺄셈만, `raise` 없음)·600/120/40 → 440 → 5절 `tiktoken.encoding_for_model("gpt-5.4-mini")`·`name`·질문 글자 45/토큰 32 → `count_tokens(text)`(바깥 `encoding` 읽기) → 예산표 15/37/135/187·True → 6절 요청·답 → 실제 201/52/stop·차이 14·여유분 안 True·예약분 안 True → 7절 값 바꿔 보기(긴 목록 570·False·넘침 130, 요청 없음) → 8절 Before(남은 칸 `600 - 570 = 30`을 `max_tokens`로, `assert`)·요청·끊긴 답·584/30/length·합계 614·예산 넘음 True → 9절 After(가용분 440으로 두 목록 검사 False/True, `max_tokens=output_reserve` `assert`)·3절 목록 요청·답·201/52/stop·합계 253·True → 정리
- 쓰지 않은 것: f-string·`raise`·try·내포식·조건 표현식·`Path`·`json`·`+=`·`sum`·`@`·`BaseModel`·타입힌트·반복문 안 요청. 새로 쓴 모양: 라이브러리 tiktoken(`encoding_for_model`·`name`·`encode`), 비교식을 `print` 인자로(`long_estimate <= available`), 인자 셋 함수, 함수가 바깥 이름 `encoding` 읽기(Ch 5 모양)
- 요청 수: 노트북 3번(mini). 탐색 실행 4번(`/tmp/ch08-01/probe1.py` 짧은·긴 목록 `max_tokens=128`, `probe2.py` Before `max_tokens=30`·After `max_tokens=120`) + 새 커널 실행 2번 × 3 = 합계 10번. 예상 비용 합계 약 0.004달러(Ch 6 06절 mini 요금 기준)
- 탐색 뒤 정한 값(규격 §3, 본문 b7에 과정 공개): 탐색에서 추정 187·570, 실제 입력 201·584(차이 14 두 번 같음), 끝까지 쓴 답 62·62·52토큰, Before 30에서 `length`. 이를 보고 수업 예산 600(긴 목록이 가용분 440을 넘고, 남은 칸 30이 답보다 작게), 출력 예약분 120(답 62의 두 배 안팎), 여유분 40(차이 14의 약 세 배)을 정함. 처음 후보는 Ch 5 04 연습용 한도와 같은 512였으나 긴 목록 추정 570이 예산을 넘어 남은 칸이 음수가 되므로 버림
- 실행 출력(2026-09-17, 두 번째 새 커널 = 첫 번째와 같음): `토큰화 규칙 이름: o200k_base`, `질문 글자 수: 45`·`질문 토큰 수: 32`, `페르소나 | 15`·`과업 명세 | 37`·`근거와 질문 | 135`·`추정 입력 합계: 187`, 6절 답 「미르시립도서관의 정기 휴관일은 매주 월요일입니다. 공휴일이 월요일과 겹치면 그 다음 날인 화요일에도 휴관합니다. [E01 p.2]」·`실제 입력 토큰 수: 201`·`실제 출력 토큰 수: 52`·`실제 입력 - 추정 입력: 14`, `긴 목록 추정 입력 합계: 570`·`넘친 토큰 수: 130`, Before 답 「미르시립도서관의 정기 휴관일은 매주 월요일이며, 법정 공휴일에도 휴」·`584`·`30`·`length`·`실제 합계: 614`, After 답(6절과 같은 글자)·`201`·`52`·`stop`·`실제 합계: 253`. 탐색 실행의 짧은 목록 답(62토큰)은 「법정 공휴일에도 휴관합니다」를 담았고 노트북 두 실행 답(52토큰)은 담지 않음 → 노트북 6절 결과 읽기에 「이번 답에 나오지 않았습니다」로만 적음
- 라이브러리 확인(설치 버전 소스): tiktoken 0.14.0 `model.py` `MODEL_PREFIX_TO_ENCODING["gpt-5"] = "o200k_base"`(`encoding_for_model("gpt-5.4-mini")` → `o200k_base`). langchain-openai 1.6.0 `ChatOpenAI.max_tokens` 기본 None, `init_chat_model(…, max_tokens=30)` → 속성 30(탐색·노트북 출력). 실습 폴더 `uv.lock`의 openai는 3.8.0(Ch 6·7은 3.10.0) → 준비물·b3·b7에 적음. `get_num_tokens_from_messages()`(메시지마다 3토큰을 더하는 langchain-openai 추정)는 실행하지 않아 본문에 쓰지 않음
- 문서 확인(2026-09-17): OpenAI 모델 안내 `gpt-5.4-mini` 「400,000 context window」·「128,000 max output tokens」·스냅숏 `gpt-5.4-mini-2026-03-17`, Anthropic 「Effective context engineering for AI agents」(2025-09-29) 컨텍스트 정의 「the set of tokens included when sampling」·「smallest possible set of high-signal tokens」
- 용어: 「출력 예약분」을 이 챕터 이름으로 정하고 「Ch 5 04절 출력 몫, Ch 6 01절 출력 상한과 같은 크기를 가리키는 이름. 예산표에서는 예약분, 모델 설정에서는 출력 상한」으로 이음(노트북 4절·b4 정의 단락·용어 표). Ch 5 04 `_src` 용어 표가 이미 「Ch 8 01절에서는 출력 예약분이라고 부름」이라고 적어 둔 것과 맞음. 「조각」은 Ch 5 토큰을 가리킬 때만(「Ch 5 01절에서 「조각」이라고 부른 단위」), 「청크」는 쓰지 않음. 새 용어 표 7개(컨텍스트, 컨텍스트 윈도, 토큰 예산, 출력 예약분, 여유분, 입력 가용분, 추정 토큰 수) = meta 「새 용어 7」
- meta 시수: 「강의 1h | 실습 1h」 유지. 01~06 절 합 강의 6h·실습 10h = `_build.py` `render_index()` 「16h · 강의 6h · 실습 10h」(규격 §7-2)
- 그림: Mermaid 4장(01-1 예산표·01-2 추정과 실제·01-3 긴 목록·01-4 Before-After, PNG 직접 확인, viewBox 599·435·741·739) + 삽화 01-5 책상 구역 1장(1회 생성 채택, job `8cb93eb3-ada6-4d2e-8903-71cf60da5803`, 2크레딧, 잔액 2848 → 2846 확인). 옛 `01-컨텍스트-예산.svg/.excalidraw`·`01-책상-예산.png/.caption.md`는 지우지 않고 본문에서 쓰지 않음(정리 대상)
- 본문: 10블록 모두 다시 씀. b3 표(Ch 5 01·04, Ch 6 01, Ch 7 01~03), b4 비유·컨텍스트·예산표·용어 표, b5 추정과 실제·긴 목록, b6 Before/After 해석(빨강 1상자), b7 탐색 뒤 정한 값·여유분 근거·토큰화 규칙·추론 설정 미실행·기준 버전, b8 02절·Ch 9 연결, b9 복습 5문제, b10 참고 자료 확인일 2026-09-17. 제작 이력 문장 없음(규격 §4)

## 검토

- 스스로 확인: 결과 읽기·본문·캡션·그림 라벨의 숫자를 두 번째 새 커널 출력과 대조(G5·G7 0). 그림 방향 말(01-1·01-2 TB 「위에서 아래로」, 01-3·01-4 칸 안 「왼쪽에서 오른쪽으로」), 색 이름(초록·파랑·보라·노랑·빨강·회색)을 PNG와 대조. 01-4의 두 칸은 입력 목록이 달라 입력 토큰 수를 효과로 비교하지 않고, After 답이 6절과 같았다는 것은 b6 문장에만 적음(규격 §5-3)
- 삽화 검수(저장 파일 기준, `figures/01-5-책상-구역.prompt.md`): 세로 테이프 두 줄·빈 띠·빈 답안지 자리·바닥 상자 관계가 그림만으로 읽힘. 약점 두 가지(뒤쪽 가로 테이프 한 줄, 답안지가 동그라미 칸 답안지)는 그림 읽기에 적음
- 별도 세션 검토(2026-09-17, `review-round1-A.md`): **accept**, 상 0·중 0·하 1(+ 챕터 공통 C-1~C-6). 반영: 01-1 그림 01-1 맨 아래 노드 「입력 가용분 안에 드는가 True」(mmd 수정 → 자동 다시 렌더, alt·caption·노트북 [1]), C-3 「빈자리」 다섯 자리 → 「여분 자리」, C-3 (5) b8 「입력을 작게 하는 첫 방법」, C-5 준비물·b5 「강의와 실습 범위」(강의 2~6절·실습 7~9절, 강사 확인). 미반영: C-5 [16] 셀 나누기(코드 변경이라 재실행 필요 — 챕터 요약 §12). Q1(탐색 뒤 정한 600·120·40 공개·01-4 빨강·187/201 설명) 유지. 반영은 `mdpatch.py` → `run_section.sh … 01 --no-exec`(재실행 없음, 노트북 코드·출력·`verification` 해시 반영 전후 같음), 반영 전 사본 `before/review-round1/`, 마감 게이트 `gates-after.json` 0

## 남은 것

- 뒤 절 작업자에게: `qa/upgrade/handoff.md` §01 → §02
- 정리 대상(삭제 승인 필요, 목록만): `figures/01-컨텍스트-예산.svg`·`.excalidraw`·`01-책상-예산.png`·`.caption.md`(옛 도식·삽화), `qa/upgrade/gates-wip-01.json`, 기기 `/tmp/ch08-01`
- 챕터 마감 때: 옛 생성기 `before/generators/`로 이동, `index-body.html`의 01절 「주요 내용」 열(「컨텍스트 윈도, 입력 구성, 출력 예약, 토큰 추정」)은 지금도 맞음
