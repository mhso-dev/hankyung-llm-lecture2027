# Ch25 검증 기록

> **개선 전 판 표시(마감 2026-09-25)** — 바로 아래 실행일·환경·관찰·「확인 필요 항목」은 개선 전(2026-09-11) 기록입니다(노트북 셋·코드 셀 13, 03의 모드별 따로 세 번 요청·「TTFT 근삿값」·「추정 비용」·「조각」 — 지금 교재와 다름). 지금 기록은 아래 「품질 개선 검증」 표와 맨 아래 「마감」 절입니다.

- 실행일: 2026-09-11
- 환경: Python 3.12.13, LangChain 1.4.0, langchain-openai 1.6.0, LangGraph 1.2.11
- 새 커널 실행: 3개 노트북, 코드 셀 13개 모두 성공
- 정적 검증: 3개 절, 코드 셀 최대 25줄, 설치 셀·한국어 목적 주석·함수 타입 힌트·assert 확인
- 실제 API: 01은 API 호출 없이 로컬 그래프로 실행했고, 02와 03은 `gpt-5.4-mini`로 실행
- 관찰: 01의 7개 모드 실행 성공. 02는 messages 사건 88개와 내용 조각 84개를 구분하고, 이어 붙인 답변과 최종 상태가 같음을 확인. 03은 세 별도 호출에서 first_event·TTFT 근삿값·total·usage·추정 비용을 분리 기록
- 빌드: index와 3개 절 HTML 생성 성공
- 화면: 1280px와 390px에서 4개 페이지 모두 글자 크기·대비·잘림·가로 넘침·SVG 경계·복사·다운로드 검사 통과
- 비밀값: 키 값 출력 없음, `.env` 공개 목록 제외
- 언어 검토: 독립 검토 완료. `textbook/part6/qa/language/ch25-final.md`와 JSON에 Phase 6 판정 및 게이트 결과 기록

## 확인 필요 항목

- 네트워크 지연, 생성 길이, usage는 실행할 때마다 달라지므로 운영 기준을 정할 때 같은 입력의 반복 측정이 필요합니다.

## 품질 개선 검증 (2026-09-25~)

위 기록은 개선 전(2026-09-11) 판입니다. 절별 세부는 `qa/upgrade/NN-diagnosis.md`에 있습니다.

| 절 | 게이트 G1~G7 | 새 커널 | verify | 빌드 | 그림 |
| --- | --- | --- | --- | --- | --- |
| 01 일곱 가지 stream mode | 40 → **0 (PASS)**, `qa/upgrade/gates-wip-01.json`(코드 셀 28, 검사 문장 387). 첫 실행 전 G1 0 · G2 0 · G6 2는 실행 전 고침, G7 18은 그림 전. AST 따로 금지 문법 0건(`extra_check.py`), 셀 최대 9줄·함수 본문 최대 5줄·호출 깊이 최대 2, 금지어 0건(「체크포인터」 안 「포인터」·Ch 23 03 「스레드 재개」 문장 말고) | `PASS 01-일곱-가지-stream-mode.ipynb: 28 cells`(2026-09-25). `code_sha256` `650e86fce1fa…`로 **새 커널 네 번**(T 17:40:32 사본 · B 17:40:45 사본(그림 전) · A 17:44:48 · A2 17:46:35 `run_section.sh`, UTC) 모두 셀별 출력 **28/28 같음**, `outputs_sha256` 네 번 모두 `5027ff86da5a…`. 모델 요청 0번, `OPENAI_API_KEY` 없이 실행 | `PASS 3 sections / 37 code cells (max 25 lines)`(최대 25줄은 개선 전 02·03) | `_build.py` 통과, 01 HTML `{{`·`[[` 0건, 02·03·`index.html` 해시 그대로 | Mermaid 4장(원본 폭 725·252·529·798), 삽화 1장(1차 job `cde26edf-d411-4ad1-a753-2407b4441a4c` 채택, 2크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |
| 02 토큰과 중간 진행 스트리밍 | 34 → **0 (PASS)**, `qa/upgrade/gates-wip-02.json`(코드 셀 25, 검사 문장 340). 첫 실행 전 G1 0 · G2 0 · G6 3은 실행 전 고침, G7 18은 그림 전. AST 따로 금지 문법 0건(`extra_check.py`, 노트북 + 도구 파일), 셀 최대 9줄·함수 본문 최대 8줄·호출 깊이 최대 2, 금지어 0건(「체크포인터」 안 「포인터」 말고), 한정어 없는 「청크」는 5절 코드 주석 한 곳(다음 재실행 때 고침) | `PASS 02-토큰과-중간-진행-스트리밍.ipynb: 25 cells`(2026-09-25). `code_sha256` `68b434d3f859…`로 **새 커널 세 번**(T 18:10:42 사본 · B 18:10:57 사본(그림 전) · A 18:14:46 `run_section.sh`, UTC). T·B 25/25 같음(`outputs_sha256` `7ab4b07f8699…`), A(교재 출력, `2238f293d766…`)와 B는 17/25 같음 — 갈린 여덟은 모두 스트림 청크 수·자리·답 글·출력 토큰 셀. 모델 요청 노트북 한 번 2번 + 노트북 밖 흔들림 확인 10번 = 16번, 예상 비용 약 0.004달러(청구 금액 아님) | `PASS 3 sections / 58 code cells (max 25 lines)`(최대 25줄은 개선 전 03) | `_build.py` 통과, 챕터 HTML `{{` 0건, 01·03·`index.html` 해시 그대로 | Mermaid 4장(원본 폭 547·245·576·646), 삽화 1장(1차 job `d0559a2f-890b-4c5f-8c53-170f13bf922f` 채택, 2크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |
| 03 TTFT와 total 비교 | 50 → **0 (PASS)**, `qa/upgrade/gates-wip-03.json`(코드 셀 24, 검사 문장 349). 첫 실행 전 G1 0 · G2 0 · G6 1은 실행 전 고침, G7 18은 그림 전. AST 따로 금지 문법 0건(`extra_check.py` 03 판 — 도구 파일 `estimate_cost`의 `.get` 둘은 허용 표시), 셀 최대 10줄·함수 본문 최대 7줄·호출 깊이 최대 2, 금지어 0건(제목·본문 첫 자리 풀이의 「TTFT」·「total」, 「체크포인터」 안 「포인터」, 「캐시 입력」 말고) | `PASS 03-TTFT와-total-비교.ipynb: 24 cells`(2026-09-25). `code_sha256` `ffe254e0d3c2…`로 **새 커널 세 번**(T 18:41:53 사본 · B 18:42:02 사본(그림 전) · A 18:45:21 `run_section.sh`, UTC). T·B 16/24, B·A 19/24 같음 — 세 번 가운데 갈린 여덟은 모두 사건 수·초·출력 토큰·예상 비용 셀, A(교재 출력) `outputs_sha256` `9a11da7a456d…`. 모델 요청 노트북 한 번 2번 + 노트북 밖 흔들림 확인 10번 = 16번, 예상 비용 약 0.004달러(청구 금액 아님) | `PASS 3 sections / 77 code cells (max 12 lines)` | `_build.py` 통과, 03 HTML `{{`·`[[` 0건, 01·02·`index.html` 해시 그대로 | Mermaid 4장(원본 폭 259·344·440·595), 삽화 1장(1차 job `f3a1cbad-825c-4153-a304-0a33fb213357` 채택, 2크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |
| 04 Streaming 실습(새 절) | 새로 만듦 → **0 (PASS)**, `qa/upgrade/gates-wip-04.json`(코드 셀 20, 검사 문장 317 — 처음 313으로 잘못 적음, 마감에서 바로잡음), 챕터 전체 `gates-wip-ch25-after04.json` 4/4 PASS. 첫 실행 전 G1 0 · G2 0 · G6 1은 실행 전 고침, G5 1·G7 3은 그림 전. AST 따로 금지 문법 0건(`extra_check.py` 03 판 — 도구 파일 `.get` 둘 허용 표시), 01~03 노트북과 대조한 새 AST 노드·내장 이름·속성·키워드 0(`astdiff.py`), 셀 최대 9줄·함수 본문 최대 8줄·호출 깊이 최대 2, 금지어 0건(「체크포인터」 안 「포인터」 말고) | `PASS 04-Streaming-실습.ipynb: 20 cells`(2026-09-25). `code_sha256` `0c0ecd220c78…`로 **새 커널 세 번**(T 19:15:45 사본 · **A 19:16:02 `run_section.sh`(교재 출력, 그림 전)** · B 19:16:16 사본(그림 전), UTC) — 셀별 출력 A·B 15/20, A·T 15/20 같음(갈린 다섯은 사건 수·답 글·초 셀), A `outputs_sha256` `40744b4c3929…`. 모델 요청 노트북 한 번 3번 + 노트북 밖 흔들림 확인 10번 = 19번, 예상 비용 약 0.006달러(청구 금액 아님). 03 노트북은 다시 실행하지 않음(`code_sha256`·`outputs_sha256` 그대로) | `PASS 4 sections / 97 code cells (max 12 lines)` | `_build.py` 통과, 04 HTML `{{`·`[[` 0건, 03 HTML은 다음 절 줄·b8 링크만 바뀜, 01·02 HTML 해시 그대로 · `_build_index.py` `Part 6: 52 verified sections; 100 bundled files` · `check_delivery.py`는 `llm-practice.zip` Part 1 항목(알려진 일)에서 멈춤 | Mermaid 3장(원본 폭 344·263·587), 삽화 1장(1차 job `8af32746-…` 탈락 → 2차 job `61323491-89d7-4fc5-97b4-755d9b4d9e2c` 채택, 4크레딧, 저장 PNG와 job 결과 픽셀 대조 차이 0) |

## 마감 (2026-09-25, 검토 1차 반영)

검토 A(중 2·하 15)·B(중 4·하 8)를 반영했습니다(요약 `qa/upgrade/chapter-summary.md` §17). **노트북은 다시 실행하지 않았습니다** — 네 노트북 `code_sha256`·`outputs_sha256`·`executed_at`이 전후 같음(01 `650e86fce1fa…`/`5027ff86da5a…` · 02 `68b434d3f859…`/`2238f293d766…` · 03 `ffe254e0d3c2…`/`9a11da7a456d…` · 04 `0c0ecd220c78…`/`40744b4c3929…`). 파일 해시만 바뀜(01~03 마크다운·그림 첨부, 04는 파일도 그대로). 마감 모델 요청 0번, 삽화 생성 0번.

| 검사 | 결과 |
| --- | --- |
| 게이트 `upgrade_gates.py … --label after` | **4/4 PASS, G1~G7 모두 0**(`qa/upgrade/gates-after.json`, 코드 셀 28·25·24·20 = 97, 검사 문장 395·344·358·317 = 1,414) — 수정 전 세 절 124 |
| AST 따로(`extra_check.py`, 노트북 넷·도구 파일) | 금지 문법 0, 허용 표시만(도구 파일 `estimate_cost`의 `.get` 둘) · 준비 셀 밖 셀 최대 9·9·10·9줄 |
| `verify.py --chapter` | `PASS 4 sections / 97 code cells (max 12 lines)` |
| 빌드 HTML 다섯 | `{{`·`[[` 0건 · 캡션 파일 = `_src` 캡션(어긋남 0) |
| `visual.cjs` 1280px·390px | **10행 PASS**(네 절 + `index.html`), Part 6 공용 결과는 Ch 25 줄만 8 → 10(`screens` 122 → 124) |
| 생성기 대조 | 네 생성기 `--src-only` 뒤 `_src` 4/4 같음, `cells()`가 노트북과 59·54·52·44셀 같음(코드 셀 글 같음) · `author_04.TOOLS` = 디스크 도구 파일 · `check_same_as_01`·`check_tools`(03·04)·`check_same_as_02` 통과 · `strip_later_imports(디스크)`가 02·03 판으로 시작 |
| Part 6 `check_bundle_execution.py` | **PASS**(Ch 24 01 `7187f7a39f3f…` · Ch 28 01 — Ch 25는 목록에 없음), `bundle-execution.json` `a72edd8a…` → `baaaf52f…`, zip `71683e44…` |
| Part 6 `check_delivery.py` | `llm-practice.zip` Part 1 Stale(117행)에서 멈춤 — 그 zip을 뺀 사본 대조: HTML 63 · 링크 1,224 · 누락 0 · 절 52 · 코드 셀 807 · 복습 197문항 오류 0 · 비밀값 0 · 개인 경로 0 · `part6-practice.zip` 103항목 |
| 옛 검사 넷 | `check_scope`(Ch 21 07)·`check_figures`(Ch 21 01-1)·`check_notebook_readiness`(`== 47`, 결과 파일 되돌림)·`check_visual_reports`(ch22) — 모두 Ch 25 전에 멈춤 |
| 보호 파일 147개 | `qa/upgrade/manifest-changes.md` 「마감 뒤」 |
| 다시 렌더한 그림 | `01-1`·`02-3`·`03-3`(`--force`, PNG 직접 확인, 01-1은 노트북 첨부도 갈아 끼움) |
