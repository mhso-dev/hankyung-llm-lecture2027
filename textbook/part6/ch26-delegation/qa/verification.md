# Ch26 검증 기록

> **개선 전 판 표시(마감 2026-09-28)** — 위쪽 목록은 개선 전(2026-09-11) 검증 기록입니다. 지금 기록은 「품질 개선 검증」 표와 맨 아래 「마감」 절입니다.

- 실행일: 2026-09-11
- 환경: Python 3.12.13, LangChain 1.4.0, langchain-openai 1.6.0, LangGraph 1.2.11
- 새 커널 실행: 4개 노트북, 코드 셀 23개 모두 성공
- 정적 검증: 4개 절, 코드 셀 최대 23줄, 설치 셀·한국어 목적 주석·함수 타입 힌트·assert 확인
- 실제 API: Subagent 도구, Handoff 상태 전환, Router 분류와 병렬 실행, 세 구조 비교 실행
- 구조 비교: create_agent가 `policy_tool` 선택, Handoff 조건부 엣지가 `shipping→refund→done` 선택, Router 구조화 출력이 `policy`와 `shipping` 선택
- 비용: 2026-09-11 GPT-5.4 mini 공식 일반 입력 0.75달러·캐시 입력 0.075달러·출력 4.50달러/100만 토큰을 적용하고 `cache_read`를 분리
- 빌드: index와 4개 절 HTML 생성 성공
- 화면: 1280px와 390px에서 5개 페이지 모두 글자 크기·대비·잘림·가로 넘침·SVG 경계·복사·다운로드 검사 통과
- 비밀값: 키 값 출력 없음, `.env` 공개 목록 제외
- 언어 검토: 후속 독립 검토 예정

## 확인 필요 항목

- 한 질문의 호출 수와 비용은 구조 이해를 위한 실행 결과이며 운영 평균을 나타내지 않습니다.
- `langgraph-supervisor` 직접 구현 권고를 `langgraph-swarm` 전체의 폐기 권고로 확대하지 않았습니다.

## 품질 개선 검증 (2026-09-28~)

위 기록은 개선 전(2026-09-11) 판입니다. 절별 세부는 `qa/upgrade/NN-diagnosis.md`에 있습니다.

| 절 | 게이트 G1~G7 | 새 커널 | verify | 빌드 | 그림 |
| --- | --- | --- | --- | --- | --- |
| 01 Subagent 도구 위임 | 28 → **0 (PASS)**, `qa/upgrade/gates-wip-01.json`(코드 셀 28, 검사 문장 378). 첫 실행 전 G1 0 · G2 0 · G6 4는 실행 전 고침, G7은 그림 전. AST 따로 금지 문법 0건(`extra_check.py` — 도구 파일 `estimate_cost`의 `.get` 둘은 허용 표시), 준비 셀 밖 셀 최대 7줄·함수 본문 최대 6줄·호출 깊이 최대 2, 금지어 0건(제목·첫 풀이 「Subagent」, 코드 이름 `supervisor`, 「캐시 입력」 말고) | `PASS 01-Subagent-도구-위임.ipynb: 28 cells`(2026-09-28). 첫 실행 판 A1(06:12:16Z)·B1 뒤 호출 깊이 3 두 줄을 고쳐 다시 실행 → 교재 출력 **A2**(06:21:38Z, `code_sha256` `499eb8665ba1…`)·사본 **B2**(06:21:48Z, 그림 라벨 확인 전) 셀별 대조 **24/28 같음**(갈린 넷은 최종 답 글·토큰 둘·예상 비용 셀). 노트북 밖 흔들림 확인 30요청(`01-probe.md` — 한 번 맡김 10/10). 모델 요청 노트북 한 번 6 · 작업 전체 54, 예상 비용 합 약 0.019달러 | `PASS 4 sections / 47 code cells (max 22 lines)` | HTML `{{`·`[[` 0건, Mermaid SVG 5 + 삽화 1 인라인. `visual.cjs`는 기기에 Playwright가 없어 돌리지 않음(마감 몫) | Mermaid 5장(폭 575·724·593·538·613, PNG 직접 확인, 빨강 0) · 삽화 1장 `01-6-큰-배와-작은-보트`(job `4b22c6aa-…` 1차 채택, 2크레딧, 픽셀 대조 차이 0) |
| 02 Handoff 상태 전환 | 31 → **0 (PASS)**, `qa/upgrade/gates-wip-02.json`(코드 셀 31, 검사 문장 443). 첫 실행 전 G1 0 · G2 0 · G6 6은 실행 전 고침, G7은 그림 전. AST 따로 금지 문법 0건(`extra_check.py` — 넘기기 도구 `runtime: ToolRuntime`은 허용 표시, `try` 한 셀), 준비 셀 밖 셀 최대 10줄·함수 본문 최대 5줄·호출 깊이 최대 2(첫 실행 전 `depth.py`), 금지어 0건(제목·첫 풀이·링크 제목 「Handoff」, 새 용어 「핸드오프」, 「체크포인터」·「프로그램」 속 거짓 양성 말고) | `PASS 02-Handoff-상태-전환.ipynb: 31 cells`(2026-09-28). 교재 출력 **A**(06:55:51Z, `code_sha256` `2d1b15cf6e77…`, 첫 실행 — 다시 실행 없음)·사본 **B**(06:56:15Z, 그림 라벨 확인 전) 셀별 대조 **29/31 같음**(갈린 둘은 7절 토큰·답 글 셀, 4절 stderr 경고 셀은 같음). 노트북 밖 흔들림 확인 15요청(`02-probe.md` — 첫 차례 넘김 5/5). 모델 요청 노트북 한 번 3(2~5절 0) · 작업 전체 21, 예상 비용 합 약 0.0077달러 | `PASS 4 sections / 72 code cells (max 22 lines)` | HTML `{{`·`[[` 0건, Mermaid SVG 5 + 삽화 1 인라인, 노트북 첨부 1. `visual.cjs`는 기기에 Playwright가 없어 돌리지 않음(마감 몫) | Mermaid 5장(폭 516·767·499·671·830, PNG 직접 확인, 빨강 0, 앞 절반 보라 0) · 삽화 1장 `02-6-밧줄이-넘어간-예인선`(job `a5f38f61-…` 1차 채택, 2크레딧, 픽셀 대조 차이 0) |
| 03 Router 분류와 병렬 실행 | 31 → **0 (PASS)**, `qa/upgrade/gates-wip-03.json`(코드 셀 25, 검사 문장 389). 첫 실행 전(`gates-wip-03-03.json`) G1 0 · G2 0 · G6 2는 실행 전 고침, G7은 그림 전. AST 따로 금지 문법 0건(`extra_check.py` — 허용 표시도 0), 준비 셀 밖 셀 최대 10줄·함수 본문 최대 8줄·호출 깊이 최대 2(첫 실행 전 `depth.py`), 금지어 0건(제목·첫 풀이 「Router」·「병렬」, 새 용어 「라우터」, 앞 절 용어 「핸드오프」, 「체크포인터」·「프로그램」 속 거짓 양성, 링크 주소 속 슬러그 말고) | `PASS 03-Router-분류와-병렬-실행.ipynb: 25 cells`(2026-09-28). 교재 출력 **A**(07:31:39Z, `code_sha256` `940a1065dba4…`, 첫 실행 — 다시 실행 없음, 뒤에 설명 한 셀만 `syncmd03.py`)·사본 **B**(07:31:56Z, 그림 라벨 확인 전) 셀별 대조 **25/25 같음**. 노트북 밖 흔들림 확인 15요청(`03-probe.md` — 두 분야 5/5). 모델 요청 노트북 한 번 3(2~4절 0) · 작업 전체 21, 예상 비용 합 약 0.0052달러 | `PASS 4 sections / 93 code cells (max 22 lines)` | HTML `{{`·`[[` 0건, Mermaid SVG 4 + 삽화 1 인라인, 노트북 첨부 1. `visual.cjs`는 기기에 Playwright가 없어 돌리지 않음(마감 몫) | Mermaid 4장(폭 595·667·509·780, PNG 직접 확인, 빨강 0, 앞 절반 보라 0) · 삽화 1장 `03-5-분류-부두를-떠나는-짐배`(1차 job `259573d7-…` 채택 — 재생성 1회 `2cc1b543-…` 탈락, 4크레딧, 픽셀 대조 차이 0, 배 넷·묶는 줄 강사 확인) |
| 04 호출 수·비용·종료 조건 비교 | 38 → **0 (PASS)**, `qa/upgrade/gates-wip-04.json`(코드 셀 30, 검사 문장 461). 첫 실행 전(`gates-wip-04-04.json`) G1 0 · G2 0 · G6 5는 실행 전 고침, G7은 그림 전. AST 따로 금지 문법 0건(`extra_check.py` — 넘기기 도구 `runtime: ToolRuntime`·도구 파일 `estimate_cost`의 `.get` 둘은 허용 표시), 준비 셀 밖 셀 최대 10줄·함수 본문 최대 6줄·호출 깊이 최대 2(첫 실행 전 `depth.py`), 금지어 0건(새 용어·앞 절 용어 「라우터」·「핸드오프」, 코드 이름 `supervisor`, 문서 이름 Subagents·Handoffs, 「체크포인터」·「프로그램」 속 거짓 양성 말고) | `PASS 04-호출-수-비용-종료-조건-비교.ipynb: 30 cells`(2026-09-28). 교재 출력 **A**(08:26:33Z, `code_sha256` `bc1e02160142…`, 첫 실행 — 다시 실행 없음, 뒤에 자리 표시만 `fillph04.py`)·사본 **B**(08:27:02Z) 셀별 대조 **29/30 같음**(6절 요청 수 표의 토큰·비용만 갈림). 노트북 밖 흔들림 확인 60요청 + 거절 10(`04-probe.md`). 모델 요청 노트북 한 번 11(+ 거절 1) · 작업 전체 82(+ 거절 12), 예상 비용 합 약 0.029달러 | `PASS 4 sections / 114 code cells (max 19 lines)` | HTML `{{`·`[[` 0건, Mermaid SVG 4 + 삽화 1 인라인, 노트북 첨부 1. `visual.cjs`는 기기에 Playwright가 없어 돌리지 않음(마감 몫) | Mermaid 4장(폭 686·675·352·574, PNG 직접 확인, 빨강 0, 보라는 응답을 받은 모델 요청만) · 삽화 1장 `04-5-짐이-다-찬-배와-문에-막힌-배`(2차 job `aa467cf6-…` 채택 — 1차 `5b8c9141-…` 탈락, 4크레딧, 픽셀 대조 차이 0) |
| 05 위임 구조 실습(새 절) | 새 절 → **0 (PASS)**, `qa/upgrade/gates-wip-05.json`(코드 셀 21, 검사 문장 321). 첫 실행 전 G1 0 · G2 0 · G3 0 · G4 0 · G6 0(G5 1·G7 3은 그림 전 — 핵심 그림 첨부·Mermaid·삽화·설계표). AST 따로 금지 문법 0건(`extra_check.py` — 도구 파일 `estimate_cost`의 `.get` 둘만 허용 표시), 01~04 노트북·도구 파일과 AST 대조 새 노드 종류·내장 이름·속성·키워드 인자·연산자 0(`inventory.py`), 준비 셀 밖 셀 최대 9줄·함수 본문 최대 6줄·호출 깊이 최대 2(첫 실행 전), 금지어 0건(「체크포인터」 속 「포인터」·문서 이름 Subagents·02절이 정의한 「핸드오프」 말고) | `PASS 05-위임-구조-실습.ipynb: 21 cells`(2026-09-28). 교재 출력 **A**(09:02:47Z, `code_sha256` `52feb1f894ef…`·`outputs_sha256` `5e0677ed5b5b…`, 첫 실행 — 다시 실행 없음, 뒤에 자리 표시만 `fillph05.py`)·사본 **B**(09:03:10Z) 셀별 대조 **21/21 같음**(`outputs_sha256` 같음). 노트북 밖 흔들림 확인 85요청(`05-probe.md` — §0 분류 모델 흐름 60, §0-2 노트북 판 25). 모델 요청 노트북 한 번 5 · 작업 전체 95, 예상 비용 합 약 0.034달러 | `PASS 5 sections / 135 code cells (max 19 lines)` | HTML `{{`·`[[` 0건, Mermaid SVG 3 + 삽화 1 인라인, 노트북 첨부 1(05-1). `visual.cjs`는 기기에 Playwright가 없어 돌리지 않음(마감 몫) | Mermaid 3장(폭 497·266·624, PNG 직접 확인, 빨강 0, 보라는 응답을 받은 모델 요청만 — 05-2) · 삽화 1장 `05-4-항아리를-내려놓은-기중기와-멈춘-기중기`(1차 job `e567da77-…` 채택, 2크레딧, 픽셀 대조 차이 0) |

## 마감 (2026-09-28)

| 검사 | 결과 |
| --- | --- |
| 게이트 `upgrade_gates.py … --label after` | **5/5 PASS, G1~G7 모두 0**(`qa/upgrade/gates-after.json`, 코드 셀 28·31·25·30·21 = 135, 검사 문장 393·463·390·477·321). 수정 전 네 절 128(`gates-before.json`) |
| AST 따로(`extra_check.py`) | 금지 문법 0 — 허용 표시 02 셀 52·04 셀 28 `runtime: ToolRuntime`, 도구 파일 `estimate_cost`의 `.get` 둘 |
| `verify.py --chapter` | **PASS 5 sections / 135 code cells (max 19 lines)**(`notebook-contracts-part6-ch26-delegation.json` `28c2358b…` 그대로) |
| 빌드 HTML 여섯(다섯 절 + `index.html`) | `{{`·`[[` **0건** |
| 화면 `visual.cjs` 1280px·390px | HTML 여섯 **12행 모두 PASS**(`textbook/_notebook/checks/ch26-delegation/visual-results.json`). 작업 VM에 playwright가 없어 기기 `/tmp/pw`에 `playwright@1.63.0`(npm, 캐시 `/tmp/npm-cache-ch26close`)·`/tmp/pw-browsers`에 chromium-headless-shell 1243을 설치하고 `NODE_PATH=/tmp/pw/node_modules PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers LD_LIBRARY_PATH=/tmp/libs/…`로 원본 `visual.cjs`를 그대로 돌림. Part 6 공용 `qa/visual-results.json`은 Ch 26 줄만 10 → 12 |
| 생성기 대조 | 다섯 생성기 `cells()` = 노트북(60·66·54·64·46셀 차이 0), `src_html()` = `_src` 5/5, 도구 파일 사슬(`check_tools()`·쓰기 가드 01 skip·04 skip·05 same, 디스크 = `TOOLS_05` `c3c1709a…`) |
| 노트북 해시 전후 | 다섯 모두 `code_sha256`·`outputs_sha256`·`executed_at` 같음(요약 §17) |
| 학생 묶음 | `_build_index.py` → `Part 6: 53 verified sections; 102 bundled files`, `part6-practice.zip` `11057938…`(105항목, Ch 26 9파일·continuity-guide 디스크와 같음, `__pycache__`·`.env` 0) |
| 묶음 실행 `check_bundle_execution.py` | **PASS**(Ch 24 01·Ch 28 01 — Ch 26은 목록 밖), `bundle-execution.json` `4f1cd14a…` |
| 전달 `check_delivery.py` | `llm-practice.zip` Part 1 Stale(117행)에서 멈춤(알려진 일, 결과 파일 안 바뀜) — 그 zip을 뺀 사본 대조 누락 링크 0·복습 오류 0·비밀값 0·개인 경로 0 |
| 옛 검사 넷 | 모두 Ch 26 전에 멈춤(`check_scope` Ch 21 07 · `check_figures` Ch 21 `.excalidraw` · `check_notebook_readiness` 47 ≠ 53 — 결과 파일 되돌림 · `check_visual_reports` Ch 22) |
| 보호 파일 190개 | 149 같음 · 39 의도한 변경 · 2 옮김(옛 생성기 둘) — `qa/upgrade/manifest-changes.md` 「마감 뒤」 |
