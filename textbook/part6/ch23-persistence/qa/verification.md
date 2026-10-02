# Ch23 실행 검증

> **맨 위부터 「품질 개선 검증」 앞까지는 개선 전 판(2026-09-11)입니다.** 지금 교재의 검증은 아래 「품질 개선 검증」 표와 끝의 「챕터 마감 (2026-09-25)」에 있습니다.

- 실행일: 2026-09-11
- 환경: Python 3.12.13, LangGraph 1.2.11, langgraph-checkpoint-sqlite 3.0.3, langgraph-checkpoint-postgres 3.0.5, psycopg 3.3.3, PostgreSQL 17
- 노트북: 6개를 각각 새 커널에서 실행했습니다. 공통 검증기는 29개 코드 셀과 셀당 최대 23줄을 확인했습니다.
- 외부 동작: Docker의 로컬 PostgreSQL과 실습 폴더의 SQLite·텍스트 파일만 사용했습니다. 모델 API와 외부 업무 시스템은 호출하지 않았습니다.

## 실제 결과

- 01절: 같은 `customer-a` 스레드는 `3 → 7`로 이어졌고 `customer-b`는 4에서 독립적으로 시작했습니다.
- 02절: `setup()` 전 PostgreSQL `UndefinedTable`을 재현했습니다. setup 뒤 결과는 `value=12`였고 `checkpoint_blobs`, `checkpoint_migrations`, `checkpoint_writes`, `checkpoints` 표를 확인했습니다.
- 03절: 첫 SQLite 연결을 닫은 뒤 새 연결과 새 그래프 객체에서 `질문 1 → 답변 1 → 질문 2 → 답변 3` 순서를 복원했습니다.
- 04절: 두 번째 노드 진입 직후 자식 프로세스를 종료했습니다. `exit`의 중단 전 상태는 없고 재개 호출 로그는 `first, second, first, second`였습니다. 이번 실행의 `async`와 `sync`는 `completed=['first']`를 보존했고 호출 로그는 `first, second, second`였습니다. 세 모드 모두 실제 재개 뒤 `['first', 'second']`로 완료했습니다.
- 05절: 첫 실행 호출은 `good, flaky`, 재개 뒤 전체 호출은 `good, flaky, flaky`였습니다. 최종 상태는 `good-result`와 `flaky-result`를 모두 포함했습니다.
- 06절: 외부 쓰기 뒤 자식 프로세스를 종료하고 재개했습니다. naive 방식은 `order-2306`을 2회, 멱등 키 방식은 1회 기록했습니다.

## 검증 명령 결과

- `execute.py notebooks/*.ipynb --cwd <project-root>` → 6개 PASS
- `_build.py` → index와 절 6개 생성
- `verify.py --chapter textbook/part6/ch23-persistence` → `PASS 6 sections / 29 code cells (max 23 lines)`
- `visual.cjs textbook/part6/ch23-persistence` → 1280px·390px에서 6개 절과 index 모두 PASS
- Part 6 노트북 준비 검사에서 Ch23 6개는 설치 셀, 구체적 목적 주석, 함수 타입 힌트, assert, 셀당 25줄 이하를 모두 충족했습니다.
- `ruff check`와 `python -m py_compile`로 두 worker와 집필 생성 스크립트를 검사해 통과했습니다.
- 검증에 사용한 `kdt-ch23-postgres` 컨테이너는 최종 검사 뒤 중지하고 제거했습니다.

## 확인 필요 항목

- 한국어 감사 3단은 집필자와 다른 검토 세션에서 수행할 예정입니다.
- `async` 저장 결과는 종료 타이밍과 저장 장치에 따라 달라질 수 있습니다.

## 품질 개선 검증 (규격 `textbook/QUALITY-UPGRADE.md`, 2026-09-25~)

위 기록은 개선 전(2026-09-11) 것입니다. 개선한 절은 아래 표에 절 단위로 덧붙입니다.
절별 기록은 `qa/upgrade/NN-diagnosis.md`, 절 사이 인계는 `qa/upgrade/handoff.md`, 검토용 묶음은 `qa/upgrade/review-pack/`입니다.

| 절 | 게이트 G1~G7 | 새 커널 | verify | 빌드 | 그림 |
| --- | --- | --- | --- | --- | --- |
| 01 체크포인터와 스레드 | 32 → **0 (PASS)**, `qa/upgrade/gates-wip-01.json`(검사 문장 349, 첫 실행 전 `gates-wip-01-01.json` G1 0 · G2 0 · G6 1 · G7 6은 실행 전 고침). AST 따로 0건, 금지어 0건(「프로그램」 안 「로그」·b7 Store 한 줄 말고) | `PASS 01-체크포인터와-스레드.ipynb: 28 cells`(2026-09-25). `code_sha256` `9d71f6f9522f…`로 **새 커널 두 번**(A 08:04:28~29 `run_section.sh` · B 08:04:47~48 사본, UTC) 실행해 셀별 출력 **28/28 같음**, `outputs_sha256` A·B 모두 `4315f7f9e3d3…`. 모델 요청 0번 | `PASS 6 sections / 53 code cells (max 23 lines)`(최대 23줄은 개선 전 02~06) | `_build.py` 통과, 01 HTML `{{` 0건, 02~06·`index.html` 내용 변화 없음 | Mermaid 4장(원본 폭 493·669·552·808), 삽화 1장(2차 job `547c15e2-02f2-43a4-be28-24aa6a51fbde` 채택, 1차 개수 틀림으로 탈락, 4크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |
| 02 PostgresSaver 준비와 스키마 | 40 → **0 (PASS)**, `qa/upgrade/gates-wip-02.json`(검사 문장 366, 첫 실행 전 `gates-wip-02-02.json` G1 0 · G2 0, G6 5는 실행 전 고침). AST 따로 0건, 금지어 0건(제목의 「스키마」·「프로그램」 안 「로그」 말고) | `PASS 02-PostgresSaver-준비와-스키마.ipynb: 28 cells`(2026-09-25). `code_sha256` `5b4fa7cf7d92…`로 **새 커널 두 번**(A 08:37:25~26 `run_section.sh` 새 클러스터 · B 08:37:47~48 사본, 이름 공간을 지운 뒤, UTC) 셀별 출력 **28/28 같음**, `outputs_sha256` A·B 모두 `abb4f3d737b3…`. 모델 요청 0번. PostgreSQL은 `pre_exec.sh`가 같은 호출 안에서 켜고 `trap EXIT`로 끔(매 호출 뒤 `pg_isready` no response) | `PASS 6 sections / 77 code cells (max 23 lines)`(최대 23줄은 개선 전 03~06) | `_build.py` 통과, 02 HTML `{{` 0건, `figure.mmd` 4·`figure.illustration` 1, 01·03~06·`index.html` 내용 변화 없음 | Mermaid 4장(원본 폭 501·463·679·535, 빨강은 02-3 Before 두 상자만), 삽화 1장(2차 job `21f990d2-0483-48b0-ac22-14fdae21a1f5` 채택, 1차 사진 수 틀림으로 탈락, 4크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |
| 03 스레드 재개와 대화 이어가기 | 25 → **0 (PASS)**, `qa/upgrade/gates-wip-03.json`(검사 문장 360, 첫 실행 전 `gates-wip-03-03.json` G1 0 · G2 4 · G6 5는 실행 전 고침 → 0). AST 따로 금지 문법 0건(허용 표시 `sorted` 넷·`with SqliteSaver.from_conn_string` 하나), 금지어 0건(「프로그램」 안 「로그」 말고) | `PASS 03-스레드-재개와-대화-이어가기.ipynb: 29 cells`(2026-09-25). `code_sha256` `fe89a30aec83…`로 **새 커널 두 번**(A 09:08:54~56 `run_section.sh` · B 09:09:09~10 사본, UTC) 셀별 출력 **29/29 같음**, 셀별 출력 글자 해시 A·B 모두 `f75291e01abd…`(`outputs_sha256`은 설치 셀 stdout 조각 수만 달라 A `952dc36685ea…` · B `c5bca6072631…`). 모델 요청 0번 | `PASS 6 sections / 101 code cells (max 23 lines)`(최대 23줄은 개선 전 04~06) | `_build.py` 통과, 03 HTML `{{` 0건, 01·02·04~06·`index.html` 내용 변화 없음 | Mermaid 4장(원본 폭 311·256·791·578, 빨강 0·보라 0), 삽화 1장(1차 job `33fe798b-3ff5-4698-9d41-c7f224ec12e2` 채택, 재생성 0, 2크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |
| 04 내구 실행 모드 비교 | 44 → **0 (PASS)**, `qa/upgrade/gates-wip-04.json`(검사 문장 372, 첫 실행 전 `gates-wip-04-04.json` G1 0 · G2 0 · G6 4 → 0은 실행 전 고침). AST 따로 금지 문법 0건(노트북·worker — 허용 표시 `sorted` 하나), 금지어 0건(「프로그램」 안 「로그」·제목·슬러그 말고) | `PASS 04-내구-실행-모드-비교.ipynb: 28 cells`(2026-09-25). `code_sha256` `ff4e48c4a731…`로 **새 커널 두 번**(A 09:44:13~24 `run_section.sh` · B 사본 `execute.py`, UTC) 셀별 출력 **27/28 같음** — 다른 한 셀은 6절 되풀이 셀의 `async` 줄(A `4 \| 5` · B `5 \| 5`, 결과 읽기 둘째 단락·b7에만), `exit`·`sync` 값은 모두 같음. 셀별 출력 글자 해시 A `e6dea0cc185d…` · B `04d21e195c37…`. 모델 요청 0번. 노트북 밖 확인 `04-probe.md`(`exit`·`sync` 20/20, `async` 40/40 남음, 끝까지 실행 20/20). 남은 자식 프로세스 0(`ps`) | `PASS 6 sections / 123 code cells (max 23 lines)`(최대 23줄은 개선 전 05·06) | `_build.py` 통과, 04 HTML `{{`·`[[` 0건, SVG 넷·삽화 하나, 01~03·05·06·`index.html` 내용 변화 없음 | Mermaid 4장(원본 폭 836·274·478·547, 빨강 0·보라 0, `async` 강제 종료 값 없음), 삽화 1장(1차 job `ec7db33b-866a-4529-b5d8-e5487a00baad` 채택, 재생성 0, 2크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |
| 05 pending writes와 장애 복구 | 36 → **0 (PASS)**, `qa/upgrade/gates-wip-05.json`(검사 문장 301, 첫 실행 전 `gates-wip-05-05.json` G1 0 · G2 0 · G6 3 → 0은 실행 전 고침). AST 따로 금지 문법 0건(허용 표시 `sorted` 셋), 금지어 0건(「pending writes」는 제목·슬러그 말고 0) | `PASS 05-pending-writes와-장애-복구.ipynb: 21 cells`(2026-09-25). `code_sha256` `06cd28c63aff…`로 **새 커널 두 번**(A 10:21:44~45 `run_section.sh` · B 10:22:03 사본 `execute.py`, UTC) 셀별 출력 **21/21 같음**, `outputs_sha256` A·B 모두 `b39f9ee7fbdf…`, 셀별 출력 글자 해시 `35c0e884b421…` 두 번 같음. 모델 요청 0번. 노트북 밖 확인 `05-probe.md`(판 A2 저장 시점마다 100/100 같음 · A1 100/100 · B·C 10/10 · D 20/20) | `PASS 6 sections / 139 code cells (max 19 lines)`(최대 19줄은 개선 전 06) | `_build.py` 통과, 05 HTML `{{`·`[[` 0건, SVG 넷·삽화 하나, 01~04·06·`index.html` 내용 변화 없음 | Mermaid 4장(원본 폭 496·244·428·601, 빨강 0·보라 0), 삽화 1장(1차 job `c7b590e1-63af-4046-8b1e-246fba15464f` 채택, 재생성 0, 2크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |
| 06 노드 재시작과 멱등성 | 28 → **0 (PASS)**, `qa/upgrade/gates-wip-06.json`(검사 문장 348, 첫 실행 전 검사 G1 0 · G2 0 · G6 2 → 0은 실행 전 고침 — `gates-wip-06-06.json`은 마지막 확인에서 다시 써 지금은 0). AST 따로 금지 문법 0건(노트북·worker·도구 파일 — 허용 표시 `sorted` 하나), 금지어 0건(「재시작」은 제목·b2 제목 풀이·용어 표·「새 말을 코드에서」·노트북 정의 한 곳, 「프로그램」 안 「로그」 말고) | `PASS 06-노드-재시작과-멱등성.ipynb: 23 cells`(2026-09-25). `code_sha256` `52c92b7d3410…`로 **새 커널 두 번**(A 10:54:39~53 `run_section.sh` · B 10:55:31 사본 `execute.py`, UTC) 셀별 출력 **23/23 같음**, `outputs_sha256` A·B 모두 `8cf67c492cc6…`, 셀별 출력 글자 해시 `898ec83a882c…` 두 번 같음. 모델 요청 0번. 노트북 밖 확인 `06-probe.md`(판 A 쓰기 방식마다 20/20 같음 · 판 B 10/10). 남은 자식 프로세스 0(`ps`) | `PASS 6 sections / 157 code cells (max 14 lines)` | `_build.py` 통과, 06 HTML `{{`·`[[` 0건, SVG 넷·삽화 하나, Before/After 칸 표시 있음, 01~05·`index.html` 내용 변화 없음 | Mermaid 4장(원본 폭 390·273·495·658, **빨강은 06-4 Before 결과 한 상자만**, 보라 0), 삽화 1장(1차 job `db7ef025-73f3-4dde-82f6-5943c262272f` 채택, 재생성 0, 2크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |
| 07 Persistence 실습(새 절) | 새 절 → **0 (PASS)**, `qa/upgrade/gates-wip-07.json`(검사 문장 333, 첫 실행 전 `--label wip-07 --section 07` G1 0 · G2 0 · G6 1(「되돌립니다」) → 0은 실행 전 고침, G7 14는 그림 전). AST 따로 금지 문법 0건(허용 표시 `sorted` 하나), 01~06에 없는 내장 이름·속성·키워드 인자 0(import 둘은 06절 함수를 도구 파일에서 가져오는 줄), 금지어 0건(「프로그램」 안 「로그」 말고), 「재시작」 0(06 슬러그 링크 말고) | `PASS 07-Persistence-실습.ipynb: 22 cells`(2026-09-25). `code_sha256` `c950067c72cc…`로 **새 커널 두 번**(A 11:27:23~25 `run_section.sh` · B 11:27:49~51 사본 `execute.py`, UTC) 셀별 출력 **22/22 같음**, `outputs_sha256` A·B 모두 `5db80578cc6b…`, 셀별 출력 글자 해시 `25a27d2a6cc4…` 두 번 같음. 모델 요청 0번. 노트북 밖 준비 확인(같은 흐름 10회, 회마다 두 실행) 출력 10/10 같음. 자식 프로세스 0 | `PASS 7 sections / 179 code cells (max 14 lines)` | `_build.py` 통과, 07 HTML `{{`·`[[` 0건, SVG 셋·삽화 하나, 07 쪽 링크 59개 모두 있음. 01~05 HTML 내용 변화 없음, 06 HTML은 b8 07 링크·다음 절 링크, `index.html`은 07 링크 | Mermaid 3장(원본 폭 836·263·655, 빨강 0·보라 0), 삽화 1장(1차 job `a6c8200a-a747-4590-824a-e3c904038749` 채택, 재생성 0, 2크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |

## 챕터 마감 (2026-09-25)

검토 1차(A 01~03·공통 중 2·하 17, B 04~07 상 1·중 2·하 12)를 반영하고 챕터를 마감했습니다. 전체 기록은 `qa/upgrade/chapter-summary.md`, 절별은 각 `qa/upgrade/NN-diagnosis.md` 끝 「마감 반영」입니다.

| 항목 | 결과 |
| --- | --- |
| 게이트 `qa/upgrade/gates-after.json` | **7/7 PASS, G1~G7 모두 0** · 코드 셀 28·28·29·27·21·23·22 = 178 · 검사 문장 352·377·364·393·307·356·344 = 2,493 |
| AST 따로(노트북 일곱·도구 파일·worker 둘) | 금지 문법 0 · 허용 표시만(키워드 없는 `sorted` 열 곳 — 03 넷·04 하나·05 셋·06 하나·07 하나 · 03 `with SqliteSaver.from_conn_string` 하나) · 07이 01~06에 없는 이름을 쓰지 않음 |
| `verify.py --chapter` | `PASS 7 sections / 178 code cells (max 14 lines)` |
| 빌드 HTML 여덟(일곱 절 + `index.html`) | `{{` 0건 |
| `visual.cjs` 1280px·390px | **16행 PASS** · Part 6 공용 `qa/visual-results.json`은 Ch 23 줄만 14 → 16(07 두 줄 더함, 새 HTML 해시) · `screens` 118 → 120 |
| 다시 실행한 노트북 | **04·06·07**(모델 요청 0) — 새 커널 두 번 04 **26/27**(다른 셀은 6절 되풀이 `async` 줄뿐, 교재 출력 5/5 · 다시 4/5) · 06 **23/23** · 07 **22/22**. 셀을 다시 실행해도 같은지 노트북 밖 확인(04·06 4/4·4/4·1/1, 07 앞머리 번호 줄 말고 같음) |
| 다시 실행하지 않은 노트북 | **01·02·03·05** — `code_sha256`·`outputs_sha256`·`executed_at` 전후 같음(마크다운만). 02는 PostgreSQL을 켜지 않고 `pre_exec.sh` 없는 단계로 빌드 |
| Part 6 `check_delivery.py` | `llm-practice.zip`의 `Stale file: labs/part1/…/01-과정-지도와-학습-규칙.ipynb`(117행)에서 멈춤(알려진 일, 결과 파일 안 바뀜). 그 zip을 뺀 사본 대조: HTML 61 · 링크 1,091 · 누락 0 · 절 50 · 복습 189문항 오류 0 · 비밀값 0 · 개인 경로 0 · `part6-practice.zip` 99항목(노트북 50) |
| Part 6 `check_bundle_execution.py` | **PASS**(Ch 24 01·Ch 28 01 각 4셀 — Ch 23은 대상 아님), `UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache`·`UV_LINK_MODE=symlink` 환경 변수만 |
| 학생 묶음 | `python3 textbook/part6/_build_index.py` → `Part 6: 50 verified sections; 96 bundled files`, `part6-practice.zip` `aa82b386b154…`, 안의 Ch 23 파일 13개가 모두 디스크와 같음 |
| 옛 검사 스크립트 넷 | 고치지 않음 — 모두 Ch 23에 닿기 전에 멈춤(`check_scope.py` Ch 21 07 「실습 30분」 · `check_figures.py` Ch 21 01-1 `.excalidraw` 짝 · `check_notebook_readiness.py` `len == 47` — 결과 파일을 먼저 써서 실행 전 사본으로 되돌림 · `check_visual_reports.py` `ch22-middleware`) |
| 남은 자식 프로세스·PostgreSQL 서버 | 0(`ps -eo pid,args` + `awk`) |
