# Ch21 실행 검증

> 이 파일 위쪽(「실제 결과」·「자동·화면 검증」·「해석 제한」)은 **개선 전 판(2026-09-11)** 기록입니다. 지금 값은 아래 「품질 개선 검증」 표에 있습니다.

- 실행일: 2026-09-11
- Python 3.12, langchain 1.4.0, langchain-openai 1.6.0, langgraph 1.2.11
- 실제 모델: gpt-5.4-mini, 실제 임베딩: text-embedding-3-small

## 실제 결과

- 01절: CompiledStateGraph의 Mermaid PNG 8,388바이트와 PNG 서명을 확인했습니다. 메시지는 Human→AI 도구 호출→Tool→AI 답 순서였고 입력 379·출력 47토큰, 추정 0.000496달러였습니다.
- 02절: ToolStrategy는 메시지 3개·AIMessage 1개, ProviderStrategy는 메시지 2개·AIMessage 1개였습니다. 두 결과 모두 R-14와 14일을 검증했습니다.
- 03절: `request_tag=lesson-03`은 상태에 남고 `student-7:read-only`는 도구가 context에서 읽었습니다. 최종 상태에 context 키는 없었습니다.
- 04절: 설치된 `create_agent` 서명에서 6개 핵심 인자를 확인하고 v1 최소 실행을 완료했습니다.
- 05절: 예약 질문은 3일을 답했고 자료에 없는 주차 질문은 검색어를 바꾸어 재검색한 뒤 규정이 없다고 답했습니다.
- 06절: Ch14 C01·C05·C07을 두 경로로 실행했습니다. Agent는 3/3, 고정 RAG는 2/3 supported였습니다. 원문 답·검색 ID·trace·모든 AIMessage 사용량·모델/도구 호출 수·전체 지연을 `rag-comparison.json`에 저장했습니다.

## 자동·화면 검증

- 공통 검증기: 6절, 38개 코드 셀, 최대 15줄로 통과했습니다.
- readiness: 주석 누락 0, 타입 힌트 누락 0, 일반 주석 0, 모든 노트북 assert 포함입니다.
- 화면: 1280px·390px의 7개 페이지에서 작은 글자, 대비, 잘림, 화면 밖 요소, SVG 경계, 가로 스크롤, 깨진 이미지, 복사 오류가 모두 0입니다.
- 도식: SVG·Excalidraw 6쌍을 동일 명세에서 생성했습니다.

## 해석 제한과 확인 필요 항목

세 질문의 한 차례 실행이므로 일반적인 성능 우열을 정하지 않습니다. 고정 RAG의 C01 실패는 검색된 두 문서 중 전자책 정보를 함께 답한 사례입니다. 별도 한국어 감사 3단과 독립 기술 검토는 후속 세션에서 수행합니다. Excalidraw MCP가 없어 기존 생성기를 사용했습니다.

## 품질 개선 검증 (규격 `textbook/QUALITY-UPGRADE.md`, 2026-09-25~)

위 기록은 개선 전(2026-09-11) 것입니다. 개선한 절은 아래 표에 절 단위로 덧붙입니다.
절별 기록은 `qa/upgrade/NN-diagnosis.md`, 절 사이 인계는 `qa/upgrade/handoff.md`, 검토용 묶음은 `qa/upgrade/review-pack/`입니다.

| 절 | 게이트 G1~G7 | 새 커널 | verify | 빌드 | 그림 |
| --- | --- | --- | --- | --- | --- |
| 01 create agent와 ReAct 루프 | 46 → **0 (PASS)**, `qa/upgrade/gates-wip-01.json`(검사 문장 392, 첫 실행 전 `gates-wip-01-01.json` G1 0 · G2 0 · G6 10은 실행 전 고침) | `PASS 01-create-agent와-ReAct-루프.ipynb: 23 cells`(2026-09-25). `code_sha256` `becd09fa7fbb…`로 **새 커널 두 번**(A 02:19:51~58 `run_section.sh` · B 02:20:2x 사본, UTC) 실행해 셀별 출력 **23/23 같음**, `outputs_sha256` 둘 다 `89e69f57f1cd…`(교재 출력 = A). 그림은 A·B 대조 뒤 확정. **모델 요청 5번**(노트북 밖 흔들림 확인 25번 — `qa/upgrade/01-probe.md`, 15/15 같음). 셀 실행 기록 A 약 7.5초. 노트북 파일 `f5e6c60b…` | `PASS 6 sections / 55 code cells (max 16 lines)`(16줄은 아직 고치지 않은 06절, 01절 준비 셀이 아닌 셀은 주석 뺀 코드 최대 8줄) | 빌드 HTML `01-create-agent와-ReAct-루프.html` `{{` 0건(`00ce823f…`) | Mermaid 4장(`01-1`~`01-4`, 원본 폭 645·688·851·851, 빨강 0, 보라는 `01-3` 모델 노드 띠 하나) · 삽화 1장(`01-5`, **1차 job `5589dc15…` 채택**, 2크레딧 — 거래 02:22:03Z). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0. 설계표 `qa/upgrade/01-figures.md` |
| 02 구조화 출력 두 전략 | 39 → **0 (PASS)**, `qa/upgrade/gates-wip-02.json`(검사 문장 381, 첫 실행 전 검사 G1 0 · G2 2 · G6 4는 실행 전 고침 — `gates-wip-02-02.json`은 고친 뒤 판) | `PASS 02-구조화-출력-두-전략.ipynb: 28 cells`(2026-09-25). `code_sha256` `cc31fb4586c9…`로 **새 커널 두 번**(A 02:51:30~37 `run_section.sh` · B 02:52:03~11 사본, UTC) 실행해 셀별 출력 **28/28 같음**, `outputs_sha256` 둘 다 `4c4b79dfa046…`(교재 출력 = A). 그림은 A·B 대조 뒤 확정. **모델 요청 6번**(노트북 밖 흔들림 확인 30번 — `qa/upgrade/02-probe.md`, 15/15 같음). 셀 실행 기록 A 약 7.5초. 노트북 파일 `920244fc…`(그림 첨부 뒤) · 도구 파일 `runner_tools.py` `eb408639…` → `ab31d0c1…`(`agent_row` 더함) | `PASS 6 sections / 78 code cells (max 16 lines)`(16줄은 아직 고치지 않은 06절, 02절 준비 셀이 아닌 셀은 주석 뺀 코드 최대 9줄) | 빌드 HTML `02-구조화-출력-두-전략.html` `{{` 0건(`cc88e29e…`) | Mermaid 4장(`02-1`~`02-4`, 원본 폭 681·592·852·860, 빨강 0, 보라는 `02-3` 모델 노드 띠 하나) · 삽화 1장(`02-5`, **1차 job `28a107c2…` 채택**, 2크레딧 — 거래 02:54:19Z). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0. 설계표 `qa/upgrade/02-figures.md` |
| 03 AgentState와 context schema | 41 → **0 (PASS)**, `qa/upgrade/gates-wip-03.json`(검사 문장 354, 첫 실행 전 검사 G1 0 · G2 0 · G6 1 · G7 6은 실행 전 고침 — `gates-wip-03-03.json`은 고친 뒤 판) | `PASS 03-AgentState와-context-schema.ipynb: 24 cells`(2026-09-25). `code_sha256` `0f23718b4749…`로 **새 커널 두 번**(A 03:26:51~57 `run_section.sh` · B 03:27:14~21 사본, UTC) 실행해 셀별 출력 **20/24 같음**(갈린 넷 = 7·8절 답 글의 쉼표 자리 · 연체 0일 출력 토큰 `45`↔`44` · 그 예상 비용 — 모두 둘째 단락 값), `outputs_sha256` A `8854500f33cc…` · B `108a34f71670…`(교재 출력 = A). 그림은 A·B 대조 뒤 확정. **모델 요청 4번**(노트북 밖 흔들림 확인 20번 — `qa/upgrade/03-probe.md`, 10/10 같음, 모델 없는 주입 확인 요청 0). 셀 실행 기록 A 약 6초. 노트북 파일 `890665f1…`(그림 첨부·설명 고침 뒤, 출력은 A 그대로) · 도구 파일 `runner_tools.py` `ab31d0c1…` → `6ce7a8d2…`(`print_branches` 더함) | `PASS 6 sections / 97 code cells (max 16 lines)`(16줄은 아직 고치지 않은 06절, 03절 준비 셀이 아닌 셀은 주석 뺀 코드 최대 9줄) | 빌드 HTML `03-AgentState와-context-schema.html` `{{` 0건(`b237631c…`), 챕터 HTML 여섯 모두 `{{` 0건 | Mermaid 4장(`03-1`~`03-4`, 원본 폭 677·326·821.5·642, 빨강 0, 보라는 `03-3` 모델 노드 띠 하나) · 삽화 1장(`03-5`, **1차 job `b8f3d50e…` 채택**, 2크레딧 — 거래 03:28:19Z). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0. 설계표 `qa/upgrade/03-figures.md` |
| 04 0.x에서 1.x로 마이그레이션 | 31 → **0 (PASS)**, `qa/upgrade/gates-wip-04.json`(검사 문장 354, 첫 실행 전 검사 G1 0 · G2 0 · G6 1 · G7 18은 실행 전 고침 — `gates-wip-04-04.json`은 고친 뒤 판) | `PASS 04-0x에서-1x로-마이그레이션.ipynb: 24 cells`(2026-09-25). `code_sha256` `ba1d0a4506cf…`로 **새 커널 두 번**(A 03:58:09~11 `run_section.sh` · B 03:58:38~40 사본, UTC — 그림 그리기 전) 실행해 셀별 출력 **24/24 같음**, `outputs_sha256` 둘 다 `ad1cedfe20eb…`(교재 출력 = A). **모델 요청 0번**(그래프를 만들기만 함 — 흔들림 확인 대상 없음, 모델 없는 확인 `probe/check04_*.py` 둘도 요청 0). 셀 실행 기록 A 약 2.2초. 노트북 파일 `cbba4573…`(그림 첨부·설명 고침 뒤, 출력은 A 그대로) · 도구 파일 `runner_tools.py` 그대로(`6ce7a8d2…`) | `PASS 6 sections / 116 code cells (max 16 lines)`(16줄은 아직 고치지 않은 06절, 04절 준비 셀이 아닌 셀은 주석 뺀 코드 최대 9줄) | 빌드 HTML `04-0x에서-1x로-마이그레이션.html` `{{` 0건(`6db1dc62…`, `<title>` 새 제목 글자), 챕터 HTML 여섯·목차 모두 `{{` 0건 | Mermaid 4장(`04-1`~`04-4`, 원본 폭 699.8·588.5·518.8·639.8, 빨강 0, 보라 0 — 모델을 부르지 않음) · 삽화 1장(`04-5`, **1차 job `99f146c5…` 채택**, 2크레딧 — 거래 04:00:15Z). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0. 설계표 `qa/upgrade/04-figures.md` |
| 05 retriever를 도구로 전환 | 31 → **0 (PASS)**, `qa/upgrade/gates-wip-05.json`·`gates-wip-05-05.json`(검사 문장 377, 첫 실행 전 검사 G1 0 · G2 0 · G6 3 · G7 18은 실행 전 고침) | `PASS 05-retriever를-도구로-전환.ipynb: 26 cells`(2026-09-25). `code_sha256` `d3898188b127…`로 **새 커널 두 번**(A 04:32:12~21 `run_section.sh` · B 04:32:39~47 사본, UTC — 그림 그리기 전) 실행해 셀별 출력 **26/26 같음**(`execute.py` `outputs_sha256`은 A `19cc75e8dabc…` · B `53957a546533…` — 설치 셀 stream이 둘/하나로 나뉜 차이뿐, 교재 출력 = A). **모델 요청 5번 · 임베딩 요청 6번**, 흔들림 확인 노트북 밖 S5·SP 다섯 번씩(모델 25 · 임베딩 34, 모양 10/10 같음). 셀 실행 기록 A 약 9초. 노트북 파일 `4c2eac65…`(그림 첨부·설명 고침 뒤, 출력은 A 그대로) · 도구 파일 `runner_tools.py` `6ce7a8d2…` → `8538fedb…`(검색 함수 다섯 + NumPy import) | `PASS 6 sections / 137 code cells (max 16 lines)`(16줄은 아직 고치지 않은 06절, 05절 준비 셀이 아닌 셀은 주석 뺀 코드 최대 10줄) | 빌드 HTML `05-retriever를-도구로-전환.html` `{{` 0건(`afcb826c…`), 챕터 HTML 여섯·목차 모두 `{{` 0건 | Mermaid 4장(`05-1`~`05-4`, 원본 폭 270.5·309.8·825·594.1, 빨강 0, 보라 = 실제로 부른 모델·임베딩 모델) · 삽화 1장(`05-5`, **1차 job `93792124…` 채택**, 2크레딧 — 거래 04:35:43Z). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0. 설계표 `qa/upgrade/05-figures.md` |
| 06 같은 평가셋으로 RAG 비교 | 63 → **0 (PASS)**, `qa/upgrade/gates-wip-06.json`·`gates-wip-06-06.json`(검사 문장 401, 첫 실행 전 검사 G1 0 · G2 0 · G6 4 · G7 3은 실행 전 고침, 첫 `--no-exec` G5 1은 `mdpatch.py`로 고침) · 챕터 전체 `gates-wip-ch21-after06.json` 6/6 PASS | `PASS 06-같은-평가셋으로-RAG-비교.ipynb: 31 cells`(2026-09-25). `code_sha256` `ca14949bb0f9…`로 **새 커널 두 번**(A 05:11:39~57 `run_section.sh` — 교재 파일과 **계약 파일 `data/rag-comparison.json` `25cfe5df…`**를 씀 · B 05:12:20~35 사본을 `execute.py --cwd /tmp/ch21-06/Broot`로 — 계약 파일을 `Broot` 아래에 써 교재 파일은 A 판 그대로, UTC — 그림 그리기 전) 실행해 셀별 출력 **26/31 같음**(갈린 다섯 = `C07` 검색어·출력 토큰과 `C07` 입력 토큰·답 글과 까닭·토큰 합과 걸린 초·에이전트 예상 비용 — 모두 둘째 단락 값), `outputs_sha256` A `1ded374d9f64…` · B `73835ba84e3a…`(교재 출력 = A). **모델 요청 15번 · 임베딩 7번**(노트북 밖 흔들림 확인 모델 75·임베딩 32 — `qa/upgrade/06-probe.md`). **Ch 29 04 흉내 검사 PASS**(`assert` 셋) — 새 인용값은 `06-diagnosis.md` §6 | `verify.py --chapter` PASS(6절, 코드 셀 156, 최대 16줄) | `_build.py` — `06-같은-평가셋으로-RAG-비교.html` `{{` 0건 | Mermaid 4장(폭 554·623·661·626) + 삽화 1장(1차 job `48eec35d…`, 2크레딧, 픽셀 대조 차이 0) |
| 07 create_agent 실습(새 절) | 새 절 → **0 (PASS)**, `qa/upgrade/gates-wip-07.json`·`gates-wip-07-07.json`(검사 문장 343, 첫 실행 전 검사 G1 0 · G2 0 · G6 4는 실행 전 고침 — 첫 판 `/tmp/ch21-07/gates-wip-07-07.first.json`) · 챕터 전체 `gates-wip-ch21-after07.json` **7/7 PASS** | `PASS 07-create-agent-실습.ipynb: 24 cells`(2026-09-25). `code_sha256` `bf48d2353026…`로 **새 커널 두 번**(A 05:48:21~27 `run_section.sh` · B 05:48:54~49:00 사본 `/tmp/ch21-07/B.ipynb`, UTC — 그림 그리기 전) 실행해 셀별 출력 **24/24 같음**, `outputs_sha256` 둘 다 `7f670216e996…`(교재 출력 = A). **모델 요청 4번**(노트북 밖 흔들림 확인 20번 — `qa/upgrade/07-probe.md`, 후보 A 규칙 넷 10/10). 셀 실행 기록 A 약 6초. 노트북 파일 `746b3a46…`(그림 첨부·설명 채움 뒤, 출력은 A 그대로) · 도구 파일 그대로(`f4113158…`) | `verify.py --chapter` `PASS 7 sections / 180 code cells (max 16 lines)`(07절 준비 셀이 아닌 셀은 주석 뺀 코드 최대 10줄) | `_build.py` — `07-create-agent-실습.html` `{{` 0건(`a5d78783…`), 목차 `index.html`(`02cd183c…`)·06 HTML(다음 절 링크, `81d3cf12…`) | Mermaid 3장(`07-1`~`07-3`, 원본 폭 699.8·865·694.4, 빨강 0, 보라는 `07-2` 모델 노드 띠 하나) · 삽화 1장(`07-4`, **1차 job `e07bcac2…` 채택**, 2크레딧 — 거래 05:51:28Z). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0. 설계표 `qa/upgrade/07-figures.md` |

### 챕터 마감 검증 (2026-09-25, 검토 1차 반영 뒤)

| 항목 | 결과 |
| --- | --- |
| 게이트 `qa/upgrade/gates-after.json` | **7/7 PASS, G1~G7 모두 0** — 검사 문장 396·389·355·355·379·411·347 = 2,632, 코드 셀 23·28·24·24·26·31·24 = 180(수정 전 `gates-before.json` 여섯 절 합 251: G1 37 · G2 11 · G4 1 · G5 44 · G6 140 · G7 18) |
| AST 따로(`extra_check.py` 06절 판) | 11건 모두 허용 예외(03 `LibraryState(AgentState)` · 03·07 `ToolRuntime[MemberContext]` · 04 `inspect.signature`·`warnings.catch_warnings`·`issubclass` · 도구 파일 `.get` 둘) |
| `verify.py --chapter` | `PASS 7 sections / 180 code cells (max 16 lines)` |
| 빌드 HTML 여덟(일곱 절 + `index.html`) | `{{` 0건 |
| `visual.cjs` 1280px·390px | **16행 모두 PASS**(`textbook/_notebook/checks/ch21-create-agent/visual-results.json`) — Part 6 공용 `visual-results.json`은 Ch 21 줄만 14 → 16 |
| 다시 실행한 노트북 | 01·02·03·04(설치 셀에 `numpy==2.5.3`). 04는 새 커널 두 번 24/24 같음, 01~03은 앞 교재 출력과 셀별 대조 22/23 · 27/28 · 19/24(다른 셀은 설치 셀 + 03의 흔들리는 값 넷 — 둘째 단락만 새 값). 모델 요청 5 + 6 + 4 + 0 = 15번 |
| 다시 실행하지 않은 노트북 | 05·06·07 — `code_sha256`·`outputs_sha256`·`executed_at` 전후 같음(마크다운·05 첨부 그림만) |
| 계약 파일 `data/rag-comparison.json` | `25cfe5df3cfd…` 그대로, Ch 29 04 흉내 검사(cell 12·14·16·18) **PASS** — 평균 토큰 688 · 걸린 초 1.731 · p95 2.003 · 토큰 p95 699 |
| `part6-practice.zip` | `3755de3d15b36c8d249fa6d4bfa18aeacf057c6f4e5038547e669cedc82e48ed`(97항목, Ch 21 열둘·Ch 14 자료 둘·Ch 22 01 노트북이 디스크와 같음, `__pycache__` 0) — `Part 6: 49 verified sections; 94 bundled files` |
| Part 6 `check_bundle_execution.py` | PASS(Ch 24 01 4셀 · Ch 28 01 4셀 — Ch 21은 실행 대상 아님), 환경 변수 `UV_CACHE_DIR=…/.cache/vm/bundle-check/uv-cache`·`UV_LINK_MODE=symlink`만 줌 |
| Part 6 `check_delivery.py` | `llm-practice.zip`의 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`에서 멈춤(알려진 일, 결과 파일 안 바뀜). 그 zip만 뺀 사본(`.cache/ch21-close/dx/`)은 HTML 60 · 링크 995 · 누락 0 · 절 49 · 복습 185문항 오류 0 · 비밀값 0 · 개인 경로 0 · `part6-practice.zip` 97항목(part6 노트북 49 = 절 49) 통과 |
| 옛 검사 스크립트(고치지 않음) | `check_scope.py` — Ch 21 `_src/07-create-agent-실습.html` 「실습 30분」에서 `Missing scope` · `check_figures.py` — `01-1-한-줄이-만든-에이전트-그래프.svg`의 `.excalidraw` 짝 요구 · `check_notebook_readiness.py` — `assert len(reports) == 47`(결과 파일을 먼저 써서 실행 전 사본으로 되돌림) · `check_visual_reports.py` — Ch 21은 지나가고 `ch22-middleware`(09 줄 없음)에서 멈춤 |
| 보호 파일 73개 | **60 같음 · 13 바뀜**(모두 의도 — `qa/upgrade/manifest-changes.md` 「챕터 마감 끝」) |
