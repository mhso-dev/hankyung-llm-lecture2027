# Ch24 실행 검증

> **개선 전 판 표시(마감 2026-09-25)** — 바로 아래 실행일·환경·「실제 결과」·「검증 명령 결과」는 개선 전(2026-09-11) 기록입니다(노트북 셋·코드 셀 13, 실습 폴더 로컬 파일 쓰기 — 지금 교재와 다름). 지금 기록은 아래 「품질 개선 검증」 표와 맨 아래 「마감」 절입니다.

- 실행일: 2026-09-11
- 환경: Python 3.12.13, LangGraph 1.2.11
- 노트북: 3개를 각각 새 커널에서 실행했습니다. 공통 검증기는 13개 코드 셀과 셀당 최대 24줄을 확인했습니다.
- 외부 동작: 실습 폴더의 로컬 텍스트 파일만 사용했습니다. 모델 API, 데이터베이스, 외부 업무 시스템은 호출하지 않았습니다.

## 실제 결과

- 01절: 부작용 뒤에 interrupt를 둔 실행은 거절해도 `transfer-local`이 2회 기록됐습니다. interrupt를 먼저 둔 실행은 `status='rejected'`를 반환하고 파일을 만들지 않았습니다.
- 02절: 첫 interrupt payload를 확인했고 `maybe`를 전달하자 오류가 포함된 두 번째 payload가 반환됐습니다. `approve`로 재개한 결과 `decision='approve'`, `next=()`였습니다.
- 03절: 원본 할인율 0.1의 최종 가격은 9000이었습니다. `discount` 직전 체크포인트의 할인율을 0.2로 바꾼 분기는 8000이었고 원본 결과는 9000으로 보존됐습니다.

## 검증 명령 결과

- `execute.py notebooks/*.ipynb --cwd <project-root>` → 3개 PASS
- `_build.py` → index와 절 3개 생성
- `verify.py --chapter textbook/part6/ch24-human-in-the-loop` → `PASS 3 sections / 13 code cells (max 24 lines)`
- `visual.cjs textbook/part6/ch24-human-in-the-loop` → 1280px·390px에서 3개 절과 index 모두 PASS
- 01절을 `--cwd labs/part6/ch24-human-in-the-loop/notebooks`로 다시 실행해 노트북 폴더 기준 상대경로 실행을 확인했습니다.
- Part 6 노트북 준비 검사에서 Ch24 3개는 설치 셀, 구체적 목적 주석, 함수 타입 힌트, assert, 셀당 25줄 이하를 모두 충족했습니다.

## 확인 필요 항목

- 한국어 감사 3단은 집필자와 다른 검토 세션에서 수행할 예정입니다.

## 품질 개선 검증 (규격 `textbook/QUALITY-UPGRADE.md`, 2026-09-25~)

위 기록은 개선 전(2026-09-11) 것입니다. 개선한 절은 아래 표에 절 단위로 덧붙입니다.
절별 기록은 `qa/upgrade/NN-diagnosis.md`, 절 사이 인계는 `qa/upgrade/handoff.md`, 검토용 묶음은 `qa/upgrade/review-pack/`입니다.

| 절 | 게이트 G1~G7 | 새 커널 | verify | 빌드 | 그림 |
| --- | --- | --- | --- | --- | --- |
| 01 interrupt 승인 게이트 | 33 → **0 (PASS)**, `qa/upgrade/gates-wip-01.json`(코드 셀 28, 검사 문장 383, 첫 실행 전 `gates-wip-01-01.json` G1 0 · G2 0 · G6 4는 실행 전 고침, G7 18은 그림 전). AST 따로 금지 문법 0건(허용 표시 키워드 없는 `sorted` 하나), 금지어 0건(「체크포인터」 안 「포인터」·「프로그램」 안 「로그」·제목 「승인 게이트」 풀이·Ch 23 「스레드 재개」 구분 문장 말고) | `PASS 01-interrupt-승인-게이트.ipynb: 28 cells`(2026-09-25). `code_sha256` `7187f7a39f3f…`로 **새 커널 두 번**(A 13:50:55~56 `run_section.sh` · B 13:51:07~08 사본, UTC) 실행해 셀별 출력 **28/28 같음**, `outputs_sha256` A·B 모두 `fbaaa8908bd1…`. 모델 요청 0번. **키 없는 묶음 모양 실행**(공개 목록의 Ch 24 파일 일곱만 `/tmp`에 두고 `uv sync --locked` → 묶음 검사와 같은 `execute.py … --cwd notebooks --kernel-python .venv/bin/python`, `OPENAI_API_KEY`·`PYTHONPATH` 없이) PASS, `code_sha256` 같음, 셀별 출력 28/28 같음 | `PASS 3 sections / 37 code cells (max 24 lines)`(최대 24줄은 개선 전 02·03) | `_build.py` 통과, 01 HTML `{{` 0건, 02·03·`index.html` 해시 그대로 | Mermaid 4장(원본 폭 241·284·576·576), 삽화 1장(1차 job `fb67df97-9798-43b5-b80c-cb1cdcf01e37` 채택, 2크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |
| 02 Command resume으로 실행 재개 | 27 → **0 (PASS)**, `qa/upgrade/gates-wip-02.json`(코드 셀 28, 검사 문장 396, 첫 실행 전 `gates-wip-02-02.json` G1 0 · G2 0 · G6 4는 실행 전 고침, G7 22는 그림 전). AST 따로 금지 문법 0건(허용 표시 — 4절 권하지 않는 모양 `while True` 하나 · 6절 노드 밖 `try`/`except RuntimeError`·`KeyError` 둘 · 키워드 없는 `sorted` 하나, 게이트는 `while`을 세지 않음), 금지어 0건(「체크포인터」 안 「포인터」·제목과 슬러그의 「재개」 말고) | `PASS 02-Command-resume으로-실행-재개.ipynb: 28 cells`(2026-09-25). `code_sha256` `ead91c80882f…`로 **새 커널 두 번**(A 14:23:56~57 `run_section.sh` · B 14:24:08~09 사본, UTC) 실행해 셀별 출력 **28/28 같음**(`outputs_sha256` A `b3385367b194…` · B `d6b3bdf6ba2e…` — 설치 셀 스트림 나뉨 차이뿐). 실습 폴더 밖 사본 T 먼저 PASS. 모델 요청 0번 | `PASS 3 sections / 61 code cells (max 19 lines)`(최대 19줄은 개선 전 03) | `_build.py` 통과, 02 HTML `{{` 0건, 01·03·`index.html` 해시 그대로 | Mermaid 5장(원본 폭 657·272·262·665·621), 삽화 1장(1차 job `1939b15e-9adb-4dfb-affd-cbde22c5aca2` 채택, 2크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |
| 03 상태 기록과 다른 분기 재실행 | 33 → **0 (PASS)**, `qa/upgrade/gates-wip-03.json`(코드 셀 28, 검사 문장 412, 첫 실행 전 `gates-wip-03-03.json` G1 0 · G2 0 · G6 3은 실행 전 고침, G7 18은 그림 전). AST 따로 금지 문법 0건(허용 표시 키워드 없는 `sorted` 하나), 금지어 0건(제목·슬러그의 「분기」·「재실행」·「체크포인터」 안 「포인터」·「새 가지(fork)」 원어 풀이·라벨의 값 이름 `fork`·도구 파일 코드 변수 말고) | `PASS 03-상태-기록과-다른-분기-재실행.ipynb: 28 cells`(2026-09-25). `code_sha256` `12b29f1517d5…`로 **새 커널 두 번**(A 14:52:28~29 `run_section.sh` · B 14:52:40 사본, UTC — 그림 전) 실행해 셀별 출력 **28/28 같음**(`outputs_sha256` A `aab2462d34f9…` · B `0482bf847552…` — 설치 셀 스트림 나뉨 차이뿐). 실습 폴더 밖 사본 T 먼저 PASS. 모델 요청 0번. 새 도구 파일로 **01 사본도 PASS·28/28 같음·`code_sha256` `7187f7a39f3f…` 그대로** | `PASS 3 sections / 84 code cells (max 11 lines)` | `_build.py` 통과, 03 HTML `{{` 0건, 01·02·`index.html` 해시 그대로 | Mermaid 4장(원본 폭 657·497·630·561), 삽화 1장(1차 job `b6d66b2b-9e64-4f57-88fb-e4f905ccbb7e` 채택, 2크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |
| 04 Human-in-the-Loop 실습(새 절) | 새 절 → **0 (PASS)**, `qa/upgrade/gates-wip-04.json`(코드 셀 28, 검사 문장 365, 첫 실행 전 `gates-wip-04-04.json` G1~G6 0 · G7 14는 그림 전). 챕터 전체 `gates-wip-ch24-after04.json` 4/4 PASS. AST 따로 금지 문법 0건(허용 표시 키워드 없는 `sorted` 하나), 01~03 노트북에 없는 내장 이름·속성·키워드 인자 0(새 import는 도구 파일의 `find_before` — 03 함수), 호출 깊이 최대 2, 금지어 0건(「체크포인터」 안 「포인터」·03 슬러그 링크의 「분기」 말고) | `PASS 04-Human-in-the-Loop-실습.ipynb: 28 cells`(2026-09-25). `code_sha256` `c4722b0d084f…`로 **새 커널 두 번**(A 15:27:35.00~35.99 `run_section.sh` · B 15:27:55 사본, UTC — 그림 전) 실행해 셀별 출력 **28/28 같음**(`outputs_sha256` A `2aeaebb25174…` · B `afed104f1fe1…` — 설치 셀 스트림 나뉨 차이뿐). 실습 폴더 밖 사본 T 먼저 PASS(28/28 같음). 노트북 밖 준비 확인 다섯 번 같음. 모델 요청 0번 | `PASS 4 sections / 112 code cells (max 12 lines)` | `_build.py` 통과, 04 HTML `{{` 0건, 01·02 HTML 해시 그대로, 03 HTML은 다음 절 이동 줄과 b8 링크로 바뀜(03 노트북 그대로), `index.html`에 04 줄 | Mermaid 3장(원본 폭 609·269·539), 삽화 1장(1차 job `8434076e-428a-4312-8a2b-0716be792e1a` 채택, 2크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |

## 마감 (2026-09-25, 검토 1차 반영)

검토 A(중 6·하 8)·B(중 5·하 12)를 반영했습니다(요약 `qa/upgrade/chapter-summary.md` §17). **노트북은 다시 실행하지 않았습니다** — 네 노트북 `code_sha256`·`outputs_sha256`·`executed_at`이 전후 같음(01 `7187f7a39f3f…`/`fbaaa8908bd1…` · 02 `ead91c80882f…`/`b3385367b194…` · 03 `12b29f1517d5…`/`aab2462d34f9…` · 04 `c4722b0d084f…`/`2aeaebb25174…`).

| 검사 | 결과 |
| --- | --- |
| 게이트 `upgrade_gates.py … --label after` | **4/4 PASS, G1~G7 모두 0**(`qa/upgrade/gates-after.json`, 코드 셀 28·28·28·28, 검사 문장 388·421·417·367) — 수정 전 세 절 93 |
| AST 따로(`extra_check.py`, 노트북 넷·도구 파일) | 금지 문법 0, 허용 표시만(02 `while True` 하나·노드 밖 `try` 둘·키워드 없는 `sorted` 넷) |
| `verify.py --chapter` | `PASS 4 sections / 112 code cells (max 12 lines)` |
| 빌드 HTML 다섯 | `{{`·`[[` 0건 |
| `visual.cjs` 1280px·390px | **10행 PASS**(네 절 + `index.html`), Part 6 공용 결과는 Ch 24 줄만 8 → 10 |
| 생성기 대조 | 네 생성기 `--src-only` 뒤 `_src` 4/4 같음, `cells()`가 노트북과 62·59·59·59셀 같음(코드 셀 글 같음) |
| Part 6 `check_bundle_execution.py` | **PASS**(Ch 24 01 `code_sha256` `7187f7a39f3f…` · Ch 28 01), `bundle-execution.json` → `a72edd8a…`, zip `edd8c3be…` |
| Part 6 `check_delivery.py` | `llm-practice.zip` Part 1 Stale(117행)에서 멈춤 — 그 zip을 뺀 사본 대조: HTML 62 · 링크 1,160 · 누락 0 · 절 51 · 복습 193문항 오류 0 · 비밀값 0 · 개인 경로 0 |
| 옛 검사 넷 | `check_scope`(Ch 21 07)·`check_figures`(Ch 21 01-1)·`check_notebook_readiness`(`== 47`, 결과 파일 되돌림)·`check_visual_reports`(ch22) — 모두 Ch 24 전에 멈춤 |
| 보호 파일 131개 | 102 같음 · 27 바뀜 · 2 옮김(`qa/upgrade/manifest-changes.md` 「마감 뒤」) |
| 다시 렌더한 그림 | `03-3`·`04-2`·`04-3`(`--force`, PNG 직접 확인) |
