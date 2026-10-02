# Ch 14 최종 검증

- 실행일: 2026-09-10 KST
- 환경: Python 3.12.13, LangChain 1.4.0, langchain-openai 1.6.1, NumPy 2.5.3
- 노트북: 9개를 각각 새 커널에서 순차 실행했습니다. 공통 실행기의 결과는 `PASS 01`부터 `PASS 09`까지이며 코드 셀은 73개, 셀당 최대 25줄입니다.
- API: `.env`에서 키의 존재만 확인했습니다. `text-embedding-3-small` 256차원 임베딩과 `gpt-4.1-mini` 생성을 실제 호출했습니다.
- 실행 비용: 09절 비교 로그의 아홉 행 추정 비용 합계는 0.0009992달러입니다. 임베딩 가격은 포함하지 않은 생성 모델 추정치이며 실제 청구액과 다를 수 있습니다.
- 빌드: `_build.py`가 목차와 9개 HTML을 생성했습니다. `verify.py`는 `PASS 9 sections / 73 code cells (max 25 lines)`를 반환했습니다.
- 시각 검사: Playwright 1.55.0으로 1280px·390px에서 10개 HTML을 검사했습니다. 본문·부연 글자 크기, 대비, 잘림, 페이지 가로 넘침, SVG 경계, 깨진 이미지, 셀 복사, 전체 복사, 노트북 다운로드가 모두 0건 오류였습니다.
- 도식: SVG 9개와 Excalidraw JSON 9개가 있으며 절별 캡션의 처리 순서와 대응합니다.
- 본문: `_src` 9개 파일 합계 44,468자이며 각 절은 고정 10블록과 복습 문제 4개를 포함합니다. 중복된 결과·한계 문단을 제거하고 절별 입력·출력, 흐름 규칙, 실제 확인 항목으로 교체했습니다.
- 배포: `qa/public-files.json`의 공개 파일이 모두 존재합니다. `.env`, `.venv`, 실패 로그, 생성 스크립트는 제외했습니다.
- 잠금·정적 검사: `uv lock --check`, 생성 스크립트 `py_compile`, JSON 구문 검사가 통과했습니다.

검증 해시:

- `chapter.json`: `f12b535deb222682179ca72154cac00054e227b04f79ea083d87f3b13cf8152d`
- `runs/pattern-comparison.json`: `8b1fd13cd844fcf9d62d5abaa616932b015ed3d3d8b6dc40a73bb7ffd3e8a091`

한국어 감사: [최종 감사 기록](../../qa/language/ch14-final-audit-2026-09-10.md)에서 학생 본문 9절, README, 노트북 마크다운 9개, 캡션과 SVG 18개를 전문 정독했으며 Phase 6 판정은 `accept`입니다. 남은 S1 의미 결함은 없습니다.

확인 필요 항목: 다른 운영체제와 다른 API 시점의 재실행은 확인하지 않았습니다. 최종 의미 교정에서는 노트북 코드와 저장 출력을 바꾸거나 API를 다시 호출하지 않았습니다.

## 품질 개선 검증 (규격 `textbook/QUALITY-UPGRADE.md`, 2026-09-19~)

위 기록은 개선 전(2026-09-10) 것입니다. 개선한 절은 아래 표에 절 단위로 덧붙입니다.
절별 기록은 `qa/upgrade/NN-diagnosis.md`, 절 사이 인계는 `qa/upgrade/handoff.md`, 검토용 묶음은 `qa/upgrade/review-pack/`입니다.

| 절 | 게이트 G1~G7 | 새 커널 | verify | 빌드 | 그림 |
| --- | --- | --- | --- | --- | --- |
| 01 대화 히스토리와 질문 재작성 | 49 → **0 (PASS)**, `qa/upgrade/gates-wip-01.json` | `PASS 01-대화-히스토리와-질문-재작성.ipynb: 29 cells`(2026-09-19). 같은 코드로 **새 커널 두 번** 실행해 `code_sha256` 29/29가 같았고 셀별 출력 글자는 26/29가 같았습니다. 갈린 셋은 마지막 값 바꿔 보기 갈래(기록 없는 재작성 문장과 그 검색·표 줄)이고, 교재에 실린 출력은 마지막 실행입니다. **서비스 요청 여덟 번**(임베딩 5 + 답 모델 3). | `PASS 9 sections / 94 code cells (max 25 lines)` | 빌드 HTML 열 개 모두 `{{` 잔존 0건. `_build.py`를 두 번 돌려 열 개의 sha256이 모두 같았습니다. | Mermaid 4장(`01-1`~`01-4`, 원본 폭 472·644·806·718) · 삽화 1장(`01-5`, **1차 job `06946d71…` 채택**, 2크레딧). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/01-figures.md`. |
| 02 Multi Query | 56 → **0 (PASS)**, `qa/upgrade/gates-wip-02.json` | `PASS 02-Multi-Query.ipynb: 30 cells`(2026-09-19). 같은 코드로 **새 커널 두 번** 실행해 `code_sha256` 30/30이 같았고(`c79ab59d…`) 셀별 출력 글자는 26/30이 같았습니다. 갈린 넷은 모델이 쓴 변형 질문과 거기서 이어지는 표이고, 교재에 실린 출력은 두 번째 실행입니다. **서비스 요청 열한 번**(임베딩 9 + 답 모델 2). | `PASS 9 sections / 116 code cells (max 25 lines)` | 빌드 HTML 열 개 모두 `{{` 잔존 0건. `_build.py`를 두 번 돌려 열 개의 sha256이 모두 같았습니다. | Mermaid 4장(`02-1`~`02-4`, 원본 폭 282·260·803·816) · 삽화 1장(`02-5`, **1차 job `a96d371e…` 채택**, 2크레딧, 잔액 2687 → 2685). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/02-figures.md`. |
| 03 질의 분해 | 50 → **0 (PASS)**, `qa/upgrade/gates-wip-03.json` | `PASS 03-질의-분해.ipynb: 30 cells`(2026-09-19). 같은 코드로 **새 커널 두 번** 실행해 `code_sha256` 30/30이 같았고(`a13e3005…`) 셀별 출력 글자는 26/30이 같았습니다. 갈린 넷은 모델이 쓴 하위 질문과 거기서 이어지는 합치기 결과이고, 교재에 실린 출력은 두 번째 실행입니다. **합친 뒤 두 근거의 자리가 `4`·`6`과 `2`·`7`로 갈려 본문·그림 라벨·정리·복습 해설에서 뺐습니다.** **서비스 요청 아홉 번**(임베딩 7 + 답 모델 2). | `PASS 9 sections / 138 code cells (max 25 lines)` | 빌드 HTML 열 개 모두 `{{` 잔존 0건. `_build.py`를 두 번 돌려 열 개의 sha256이 모두 같았습니다. | Mermaid 4장(`03-1`~`03-4`, 원본 폭 237·469·814·256) · 삽화 1장(`03-5`, **1차 job `3a22bd58…` 채택**, 2크레딧, 잔액 2685 → 2683). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/03-figures.md`. |
| 04 Step back | 53 → **0 (PASS)**, `qa/upgrade/gates-wip-04.json` | `PASS 04-Step-back.ipynb: 26 cells`(2026-09-19). 같은 코드로 **새 커널 두 번** 실행해 `code_sha256` 26/26이 같았고(`5a56ba1f…`) 셀별 출력 글자는 22/26이 같았습니다. 갈린 넷은 모델이 쓴 넓힌 질문과 거기서 이어지는 순위 표·기록 표이고, 교재에 실린 출력은 두 번째 실행입니다. **넓힌 질문 검색 순위 표의 둘째·셋째 자리가 갈려 본문·그림 라벨에서 뺐습니다.** 정답 자리 넷(`8`·`1`·`1`·`1`)과 첫 자리 문서 넷은 두 실행에서 같았습니다. **서비스 요청 일곱 번**(임베딩 5 + 답 모델 2). | `PASS 9 sections / 156 code cells (max 25 lines)` | 빌드 HTML 열 개 모두 `{{` 잔존 0건. `_build.py`를 두 번 돌려 열 개의 sha256이 모두 같았습니다. | Mermaid 4장(`04-1`~`04-4`, 원본 폭 237·590·464·806) · 삽화 1장(`04-5`, **2차 job `11810810…` 채택**, 재생성 1회, 4크레딧, 잔액 2683 → 2679). 1차 job `cee387e7…`은 큰 판이 구멍 위가 아니라 옆에 놓여 떨어뜨렸습니다. 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/04-figures.md`. |
| 05 HyDE | 53 → **0 (PASS)**, `qa/upgrade/gates-wip-05.json` | `PASS 05-HyDE.ipynb: 27 cells`(2026-09-19). 같은 코드로 **새 커널 두 번** 실행해 `code_sha256` 27/27이 같았고(`c3f18065…`) 셀별 출력 글자는 21/27이 같았습니다. 갈린 여섯은 모델이 지은 가상 문서와 거기서 이어지는 순위 표·기록 표이고, 교재에 실린 출력은 두 번째 실행입니다. **값 바꿔 보기 갈래의 정답 자리가 넷과 여덟로 갈려 본문·그림 라벨에서 뺐고 「앞 세 자리 밖」으로만 적었습니다.** 정답 자리 셋(`4`·`1`·`3`)과 첫 자리 문서 넷(`FAC-003`·`LIB-004`·`LIB-001`·`LIB-001`)은 두 실행에서 같았습니다. **서비스 요청 일곱 번**(임베딩 5 + 답 모델 2). | `PASS 9 sections / 175 code cells (max 25 lines)` | 빌드 HTML 열 개 모두 `{{` 잔존 0건. `_build.py`를 두 번 돌려 열 개의 sha256이 모두 같았습니다. | Mermaid 4장(`05-1`~`05-4`, 원본 폭 222·457·464·810) · 삽화 1장(`05-5`, **2차 job `0f3d7f04…` 채택**, 재생성 1회, 4크레딧, 잔액 2679 → 2675). 1차 job `822783c3…`은 두 판 모두 구멍이 보이지 않아 떨어뜨렸습니다. 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/05-figures.md`. |
| 06 CRAG | 47 → **0 (PASS)**, `qa/upgrade/gates-wip-06.json` | `PASS 06-CRAG.ipynb: 29 cells`(2026-09-19). 같은 코드로 **새 커널 두 번** 실행해 `code_sha256` 29/29가 같았고(`63633705…`) 셀별 출력 글자도 **29/29가 같았습니다**. 모델이 쓴 보정 질문까지 두 실행에서 같았지만, 탐색 실행에서 그 문장과 보정 검색의 거리가 갈렸으므로 두 값은 본문·그림 라벨·정리·복습에 넣지 않았습니다. 첫 검색 순위 표(`ACC-001` 0.74 · `LIB-003` 0.77 · `FAC-002` 0.79)와 정답 자리 셋·하나, 판정 `True`, 횟수 1과 0은 두 실행에서 같습니다. **서비스 요청 열두 번**(임베딩 11 + 답 모델 1, 기준값을 늘린 갈래에서는 답 모델 0번). | `PASS 9 sections / 196 code cells (max 25 lines)` | 빌드 HTML 열 개 모두 `{{` 잔존 0건. `_build.py`를 두 번 돌려 열 개의 sha256이 모두 같았습니다. | Mermaid 4장(`06-1`~`06-4`, 원본 폭 219·594·580·791, 갈래는 점선 `-.->`) · 삽화 1장(`06-5`, **1차 job `e67369f8…` 채택**, 재생성 0회, 2크레딧, 잔액 2675 → 2673). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/06-figures.md`. |
| 07 Self-RAG | 47 → **0 (PASS)**, `qa/upgrade/gates-wip-07.json` | `PASS 07-Self-RAG.ipynb: 29 cells`(2026-09-19). 같은 코드로 **새 커널 두 번** 실행해 `code_sha256` 29/29가 같았고(`6eaf93a1…`) 셀별 출력 글자도 **29/29가 같았습니다**. 모델이 쓴 답 초안과 고친 답까지 두 실행에서 같았지만, 탐색 실행에서 답 초안의 쉼표 하나와 검사 초안의 근거 점수(`0.86`↔`0.78`)가 갈렸으므로 두 값은 본문 결론·그림 라벨·정리·복습에 넣지 않았습니다. 눈금 `0.98`·`0.5`, 기준값 `0.9`, 순위 표(`LIB-003` 0.35 · `ACC-002` 0.56 · `LIB-004` 0.66), 정답 자리 하나, 근거 글자 수 `206`, 판정 `True`·`False`, 고친 횟수 1과 0, 고친 답 점수 `0.98`은 두 실행에서 같습니다. **서비스 요청 아홉 번**(임베딩 2 + 답 모델 7, 점수가 기준값에 못 미친 갈래는 답 모델 3번·미친 갈래는 1번). | `PASS 9 sections / 217 code cells (max 25 lines)` | 빌드 HTML 열 개 모두 `{{` 잔존 0건. `_build.py`를 두 번 돌려 열 개의 sha256이 모두 같았습니다. | Mermaid 4장(`07-1`~`07-4`, 원본 폭 234·620·539·764, 갈래는 점선 `-.->`) · 삽화 1장(`07-5`, **1차 job `8ccddc1a…` 채택**, 재생성 0회, 2크레딧, 잔액 2673 → 2671). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/07-figures.md`. |

| 08 RAPTOR 계층 요약 | 62 → **0 (PASS)**, `qa/upgrade/gates-wip-08.json` | `PASS 08-RAPTOR-계층-요약.ipynb: 30 cells`(2026-09-19). 같은 코드로 **새 커널 두 번** 실행해 `code_sha256` 30/30이 같았고(`dae4dbec…`) 셀별 출력 글자도 **30/30이 같았습니다**(`outputs_sha256`은 표준 출력이 스트림 덩어리로 나뉜 수만 달라 갈렸고 글자는 같습니다). 그 앞 판으로 돌린 두 실행에서는 모델이 쓴 요약 글·글자 수(`library` 83↔85자, `account` 77↔81자)와 질문·요약 거리(`account` `0.61`↔`0.6`, `library` `0.87`↔`0.86`)가 갈렸으므로 그 값들은 본문 결론·그림 라벨·정리·복습에 넣지 않았습니다. 갈래 이름 셋, 갈래별 문서 ID, `고른 갈래: account`·`library`, `본 문서 수` 12와 4, `정답 문서의 자리` 1과 0, 원문 순위 표(`ACC-001` 0.16 · `ACC-003` 0.61 · `FAC-004` 0.68), 요약 수 3은 두 실행에서 같습니다. **서비스 요청 일곱 번**(임베딩 4 = 문서 1 + 요약 1 + 질문 2, 답 모델 3 = 갈래마다 요약 1). | `PASS 9 sections / 239 code cells (max 25 lines)` | 빌드 HTML 열 개 모두 `{{` 잔존 0건. `_build.py`를 두 번 돌려 열 개의 sha256이 모두 같았습니다. | Mermaid 4장(`08-1`~`08-4`, 원본 폭 234·535·482·833, 고르는 자리는 점선 `-.->`) · 삽화 1장(`08-5`, **1차 job `ccf91ecb…` 채택**, 재생성 0회, 2크레딧, 잔액 2671 → 2669). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/08-figures.md`. |
| 09 패턴 비교와 선택 | 84 → **0 (PASS)**, `qa/upgrade/gates-wip-09.json` | `PASS 09-패턴-비교와-선택.ipynb: 29 cells`(2026-09-19). 같은 코드로 **새 커널 네 번** 실행해 `code_sha256` 29/29가 네 번 모두 같았고(`6393e086…`) 셀별 출력 글자는 **27/29가 같았습니다**. 갈린 둘은 견주기 표 셀과 값 바꿔 보기 셀이고, 그 안에서 갈린 칸은 패턴을 얹은 여섯 칸 가운데 셋입니다(`변형 질문 | C02`의 자리 6·5·5·4, `가상 문서 | C02`의 자리 5·3·1·1, `가상 문서 | C05`의 자리 1·2·1·1). 그 셋은 본문 결론·그림 라벨·정리·복습에 넣지 않았습니다. 기준선 자리 셋(`C02` 7 · `C05` 1 · `C06` 1), `변형 질문 | C05`·`변형 질문 | C06`·`가상 문서 | C06`의 자리 1, 패턴별 요청 수(1 · 4 · 2), `실제로 센 서비스 요청 수: 21`, 질문 벌 세 줄, 파일 줄 수 9와 칸 이름 일곱은 네 번 모두 같습니다. 교재에 실린 출력은 **네 번째 실행**입니다. **서비스 요청 스물두 번**(임베딩 16 = 문서 1 + 실행 아홉에서 15, 답 모델 6 = 변형 질문 3 + 가상 문서 3, 실행 하나에 기준선 1 · 변형 질문 4 · 가상 문서 2). | `PASS 9 sections / 259 code cells (max 23 lines)` | 빌드 HTML 열 개 모두 `{{` 잔존 0건. `_build.py`를 두 번 돌려 열 개의 sha256이 모두 같았습니다. | Mermaid 4장(`09-1`~`09-4`, 원본 폭 419·824·241·320, 점선 0장) · 삽화 1장(`09-5`, **1차 job `a97f306c…` 채택**, 재생성 0회, 2크레딧, 잔액 2669 → 2667). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/09-figures.md`. |
| 10 RAG 패턴 실습 (**새 절**) | **0 (PASS)**, `qa/upgrade/gates-wip-10.json`(새 절이라 수정 전 값이 없습니다. 첫 게이트 실행은 G6 2건이었고 `mdpatch.py`로 고쳤습니다) | `PASS 10-RAG-패턴-실습.ipynb: 30 cells`(2026-09-20). 같은 코드로 **새 커널 두 번** 실행해 **30/30 셀의 출력이 글자까지 같았습니다**(`code_sha256` `ffcd7850…`·`outputs_sha256` `c9e2668d…`). 교재에 실린 출력은 두 번째 실행입니다. 다만 **하루 전 탐색 실행과는 보정 질문 문장이 갈렸고**, 그 탓에 실행 1의 마지막 검색 값(첫 자리 문서·정답 자리)이 달라졌습니다. 그래서 보정 뒤 자리는 한 번 본 결과로 한정해 적고 결론을 넓히지 않았습니다. `첫 검색의 첫 자리 거리` `0.64`·`0.44`, `다시 검색한 횟수` 1·0, `첫 검색의 정답 자리` 2·1, 요청 수 5·4·10은 두 실행에서 같습니다. **서비스 요청 열 번**(임베딩 5 = 문서 1 + 실행마다 2, 답 모델 5 = 실행 1 세 번 + 실행 2 두 번). | `PASS 10 sections / 289 code cells (max 23 lines)` | 빌드 HTML **열한 개** 모두 `{{` 잔존 0건. `_build.py`를 두 번 돌려 열한 개의 sha256이 모두 같았습니다. | Mermaid 3장(`10-1`~`10-3`, 원본 폭 323·460·309, 갈래는 점선 `-.->`, 비교 그림은 `~~~`) · 삽화 1장(`10-4`, **1차 job `fc5d546d…` 채택**, 재생성 0회, 2크레딧, 잔액 2667 → **2665**). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/10-figures.md`. |
- 챕터 수정 전 게이트: `qa/upgrade/gates-before.json`(2026-09-19, 아홉 절 합계 **501** = 49·56·50·53·53·47·47·62·84, 통과 0/9).
- 보호 파일 20개(`qa/upgrade/before-manifest.json`, Ch 14·Ch 12·Ch 13의 `runs/`·`data/`)를 01절부터 08절까지 각 절 작업 끝에 다시 계산해 **어긋난 항목 0건**입니다.
- **09절만 다릅니다.** 09절이 산출 파일 `labs/part4/ch14-rag-patterns/runs/pattern-comparison.json`을 다시 써서 **스무 개 가운데 그 하나만 의도적으로 달라졌고 나머지 열아홉은 그대로**입니다(`8b1fd13cd844fcf9d62d5abaa616932b015ed3d3d8b6dc40a73bb7ffd3e8a091` → `94d10997803eabdc37111b484bc832ccaf6d2e07b6ebd4c9855b0311de897f50`, 4540바이트 → 4454바이트). 이 파일은 학생 묶음 파일이고 코드로 읽는 곳이 없어 칸을 이 챕터가 실제로 재는 값으로 다시 짰습니다. `before-manifest.json`은 수정 전 기록이라 고치지 않았습니다.
- 옛 생성기 셋(`_make_sources.py`·`figures/_gen_figures.py`·`labs/part4/ch14-rag-patterns/_make_notebooks.py`)은 첫머리 주석과 `raise SystemExit(...)`로 실행을 막았습니다. 파일은 지우지 않았고 챕터 마감 때 `qa/upgrade/before/generators/`로 옮깁니다.
- 01절부터 07절까지 실습 폴더 `pyproject.toml`·`uv.lock`을 손대지 않았습니다. `%pip` 세 줄(`langchain==1.4.0`·`langchain-openai==1.6.1`·`python-dotenv==1.2.3`)이 모두 잠금에 같은 판으로 있고 dev `pip==26.2`도 있습니다. 마운트 폴더 삭제 제한 때문에 `uv sync --locked`는 돌리지 않았습니다.
- 01절이 만든 가상환경은 `$ROOT/.cache/vm/venv-ch14-rag-patterns`입니다(Python 3.12.13, 전체 마감 때 삭제 승인 대상).
- 화면 검사(`visual.cjs`)와 `gates-after.json`은 챕터 마감 때 한 번에 돌립니다.
- 10절 작업 끝에 챕터 전체 게이트를 한 번 돌려 `qa/upgrade/gates-wip.json`을 남겼습니다(**열 절 모두 G1~G7 0건 PASS**).
- **10절(실습 절)은 파일을 쓰지 않아 보호 파일 20개가 09절 끝 상태 그대로입니다**(열아홉 개는 `before-manifest.json`과 같고 `runs/pattern-comparison.json`은 09절이 쓴 `94d10997…` 그대로).
- 10절을 더하면서 챕터 밖 파일 셋을 함께 고쳤습니다: `textbook/part4/public-files.json`(10절 노트북 한 줄), `labs/part4/ch14-rag-patterns/README.md`(10절 한 단락), `textbook/downloads/part4-practice.zip`(`textbook/part4/_build_index.py`로 다시 만듦, `Part 4: 32 verified sections; 89 bundled files`). 챕터 안에서는 `chapter.json`(`sections`에 10절, **시수 그대로**)과 `qa/public-files.json`을 고쳤습니다.
- `textbook/part4/_build_index.py`에는 **절 수 칸이 없습니다**(`CHAPTERS`는 슬러그·강의 시수·실습 시수·설명 네 칸이고 절 수는 `chapter.json`에서 셉니다). 고칠 곳이 없어 그대로 두고 실행만 했습니다.
- `textbook/qa/check_course_continuity.py`는 **part4 묶음을 보지 않습니다**(203행 목록이 part1~3과 `llm-practice.zip`). 고칠 해시 허용 목록이 없어 그대로 두고 돌렸고, 212행 `Stale archive: part1-practice.zip/…01-과정-지도와-학습-규칙.ipynb`에서 멈춥니다(10절 작업 전과 같은 자리).
- `textbook/part4/qa/check_delivery.py`는 `part4-practice.zip`을 지나 **`llm-practice.zip`의 111행 `Stale file: labs/part1/…01-과정-지도와-학습-규칙.ipynb`에서 멈춥니다**(전체 묶음은 전체 마감 때 다시 만듭니다).

## 챕터 마감 검증 (2026-09-20)

검토 둘(`../qa/upgrade/review-round1-A.md` 01~05절 · `review-round1-B.md` 06~10절)을 반영한 뒤 돌린 결과입니다. **노트북은 다시 실행하지 않았습니다.**

| 검사 | 명령 | 결과 |
|---|---|---|
| 품질 게이트 | `python3 textbook/_notebook/checks/upgrade_gates.py textbook/part4/ch14-rag-patterns --label after` | **10/10 PASS**, `{"G1":0,"G2":0,"G3":0,"G4":0,"G5":0,"G6":0,"G7":0}` (`qa/upgrade/gates-after.json`) |
| 노트북·HTML 대조 | `verify.py --chapter textbook/part4/ch14-rag-patterns` | `PASS 10 sections / 289 code cells (max 23 lines)` |
| 화면 검사 | `node textbook/_notebook/visual.cjs textbook/part4/ch14-rag-patterns` | **22행**(HTML 열한 개 × 1280px·390px) **모두 PASS**, small·contrast·clipped·outside·svgBounds·horizontal·brokenImages·copyErrors·failureErrors 전부 0 |
| 빌드 | `_build.py` | HTML 열한 개, `{{` 잔존 **0건** |
| Part 4 목차·묶음 | `python3 textbook/part4/_build_index.py` | `Part 4: 32 verified sections; 89 bundled files` |
| 배포 검사 | `python3 textbook/part4/qa/check_delivery.py` | `part4-practice.zip` **통과**(zip 92항목·manifest 89항목, 해시 어긋남 0·Stale 0) → `llm-practice.zip` **111행 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`에서 멈춤**(낡은 항목 139개, 전체 마감 몫. 이 챕터 작업 전과 같은 자리) |

### 게이트 전후

| 절 | 수정 전 | 마감 뒤 |
|---|---|---|
| 01 대화 히스토리와 질문 재작성 | 49 | 0 PASS |
| 02 Multi Query | 56 | 0 PASS |
| 03 질의 분해 | 50 | 0 PASS |
| 04 Step back | 53 | 0 PASS |
| 05 HyDE | 53 | 0 PASS |
| 06 CRAG | 47 | 0 PASS |
| 07 Self-RAG | 47 | 0 PASS |
| 08 RAPTOR 계층 요약 | 62 | 0 PASS |
| 09 패턴 비교와 선택 | 84 | 0 PASS |
| 10 RAG 패턴 실습 (새 절) | — | 0 PASS |
| **합계** | **501**(통과 0/9) | **0**(통과 **10/10**) |

### 노트북 해시 (재실행 0건)

열 노트북 모두 `metadata.verification`의 `code_sha256`·`outputs_sha256`이 작업 전과 같고, 저장된 코드 셀·출력에서 `execute.py`의 `code_hash()`·`output_hash()`로 다시 계산한 값도 기록과 **10/10 일치**합니다. 고친 방법은 `mdpatch.py`(생성기 + 노트북 **마크다운 셀** + `_src`) · `.mmd` 다섯 장 다시 렌더 · `attach_figures.py`(`03-1` 한 장, 코드 셀과 출력을 건드리지 않음) · `_build.py`뿐입니다.

| 노트북 | `code_sha256` | `outputs_sha256` |
|---|---|---|
| 01 | `56001b9f9000…` | `279bce134185…` |
| 02 | `c79ab59d7c0d…` | `d307058100ea…` |
| 03 | `a13e30058506…` | `dcb1d5f79098…` |
| 04 | `5e0fe272144c…` | `b9076b0f6765…` |
| 05 | `df29b68a2db7…` | `bc9122049cb0…` |
| 06 | `c2998d5ccc3e…` | `845f1e01dfa3…` |
| 07 | `dc6d13198bbe…` | `f63c15445925…` |
| 08 | `dae4dbecd019…` | `74220eed519d…` |
| 09 | `6393e086804a…` | `3403115c9409…` |
| 10 | `ffcd78508693…` | `c9e2668d6da0…` |

### 보호 파일 20개

- **열아홉 개가 `qa/upgrade/before-manifest.json` 값 그대로**입니다.
- `labs/part4/ch14-rag-patterns/runs/pattern-comparison.json` 하나만 다르고 **09절이 의도적으로 쓴 값 그대로**입니다(`8b1fd13cd844fcf9…` → `94d10997803eabdc37111b484bc832ccaf6d2e07b6ebd4c9855b0311de897f50`, 4540 → 4454바이트).

### 다시 렌더한 그림 다섯 장 (PNG를 직접 열어 확인)

| 그림 | 무엇을 | 렌더 폭 |
|---|---|---|
| `02-4-늘려도-앞으로-오지-않는-질문` | 회색 상자를 「C01과 C02에 같은 머리글과 같은 가중치를 씀」으로(검토 A B-2) | 816 |
| `03-1-한-질문에-섞인-사실-둘-나누기` | 질문 라벨을 노트북 출력 낱말 그대로(검토 A C-1) | 251(237 → 251) |
| `04-2-좁히기와-넓히기` | 파랑 「한 단계 넓히기」 + 노랑 「넓힌 질문 한 줄」로 나눔(검토 A D-1) | 590 |
| `10-2-실행-1의-실제-순서` | 기준값 초록 → **파랑**, 갈린 값 뺌, 「보정 질문으로 다시 검색」·「답 쓰기」 더함(검토 B B-7·B-8·B-11·B-14) | 460 |
| `10-3-두-실행-비교` | 「마지막 검색의 정답 자리」 둘 뺌 → 상자 아홉 → **일곱**(검토 B B-8·B-10·B-11) | 301(309 → 301) |

### 옛 생성기 옮기기 (규격 §8)

`_make_sources.py` · `figures/_gen_figures.py` · `labs/part4/ch14-rag-patterns/_make_notebooks.py` 셋을 `qa/upgrade/before/generators/`로 `mv -n` 했습니다. **지우지 않았습니다.** `_build.py`·`run_section.sh`·`upgrade_gates.py`·`verify.py`·`_build_index.py`·`check_delivery.py`·`build_bundle.py` 어디도 이 세 파일을 부르지 않는 것을 `grep`으로 확인했습니다(남은 참조는 `.moai/evolution/…/baseline-files.json`의 옛 기록과 `qa/public-files.json`의 `excluded` 목록뿐이고 둘 다 스크립트가 아닙니다). 옮긴 뒤 `_build_index.py`를 다시 돌려 묶음 항목 수가 그대로인 것(89)을 확인했습니다.

## §2-7 리팩터 검증 (2026-09-21)

규격 §2-7(앞에서 배운 함수는 도구 파일 `labs/part4/ch14-rag-patterns/notebooks/rag_tools.py`에서, 벡터 계산은 NumPy로)을 적용한 뒤의 검증입니다. 세부는 `qa/upgrade/handoff.md` 「§2-7 리팩터 (2026-09-21)」, 셀별 두 실행 대조는 `qa/upgrade/ab-2-7.json`.

| 절 | 바뀐 것 | 새 커널 두 번(B `code_sha256` · `outputs_sha256`) | 리팩터 전 출력과 |
| --- | --- | --- | --- |
| 01 | 함수 넷 가져옴, 준비 셀 넷 뺌 | PASS 25 cells, A ↔ B 22/25 같음(`d395612f…` · `1290fed0…`) | 재작성 문장 조사·기록 없는 재작성 문장과 자리(10 → 8)만 다름 |
| 02 | 여섯 가져옴(`fuse_rank`·`run_row`) | PASS 23 cells, 18/23(`29dcca64…` · `a77a4434…`) | 변형 질문 문장과 목록별 첫 자리만 다름, `C01` 2 → 1·`C02` 7 → 4 같음 |
| 03 | 일곱 가져옴 | PASS 23 cells, 22/23(`3ee3dade…` · `8c4eeafb…`) | 하위 질문 문장·합친 뒤 자리(2·7 → 4·6)만 다름 |
| 04 | 일곱 가져옴(`run_row`) | PASS 20 cells, 15/20(`6d4540d2…` · `0c6c63e9…`) | 넓힌 질문 문장과 그 순위 표 뒤 두 줄만 다름, 8 → 1 같음 |
| 05 | 여섯 가져옴 | PASS 22 cells, 16/22(`927c34cf…` · `0f1b0c4d…`) | 가상 문서 문장과 바꾼 질문 가상 문서 자리(8 → 4, 둘 다 앞 세 자리 밖)만 다름 |
| 06 | 다섯 가져옴 | PASS 24 cells, 21/24(`5e7c80c4…` · `acbc4b81…`) | 같음(A만 보정 질문 문장·거리 다름) |
| 07 | 일곱 가져옴(`build_answer_prompt`·`keeps_word`) | PASS 26 cells, 21/26(`f8d16e40…` · `448f1f48…`) | 눈금 높은 쪽 0.98 → 1.0, 통제 답 0.78 → 0.86, 답 쉼표 |
| 08 | 넷 가져옴, `rank_summaries` 줄임 | PASS 27 cells, 25/27(`458ea943…` · `c5b3f82f…`) | 요약 글·글자 수·요약 거리만 다름 |
| 09 | 일곱 가져옴 | PASS 22 cells, 20/22(`5eb19a00…` · `d3a1f7cf…`) | 패턴 칸 `C02` 두 칸(4 → 5, 1 → 3)만 다름, 산출 파일 `94d10997…` → `49eabfd4…` |
| 10 | 일곱 가져옴(인자 바뀐 판) | PASS 24 cells, **24/24**(`b1dfbc5c…` · `c9bc34d2…`) | 첫 자리 거리 0.64·0.44 → 0.6·0.37, 실행 1 보정 뒤 자리 5 → 2·답 표시 False → True |

- `upgrade_gates.py --label after-2-7` → **10/10 PASS, G1~G7 0**. `verify.py --chapter` → `PASS 10 sections / 236 code cells (max 13 lines)`. 빌드 HTML 11개 `{{` 0건.
- `visual.cjs`(사본 `/tmp/ch14-27/vis/vis.cjs`, 파일마다 새 창) 01~10 × 1280px·390px **20/20 PASS** → `qa/upgrade/visual-after-2-7.json`(공용 `checks/ch14-rag-patterns/visual-results.json` 22행은 그대로).
- 도구 파일: Ch 12·Ch 11 구역 7개가 Ch 12 도구 파일과 AST 같음, `print_ranked`가 Ch 12 05절 판과 AST 같음, 01~06 구역 인자 그대로인 6개가 각 절 판과 AST 같음, 인자 바뀐 7개는 같은 입력에서 같은 값(가짜 모델 대조). 금지 문법 0건, 함수 본문 최대 8줄. SHA-256 `868a653e…`.
- 다시 렌더한 그림 네 장(`01-1`·`01-3`·`10-2`·`10-3`)은 SVG 글자·폭으로 확인했고 PNG 화면 확인은 하지 못했습니다(기기 셸 도구만 쓰는 조건).
- 묶음: `_build_index.py` → `Part 4: 32 verified sections; 95 bundled files`, `part4-practice.zip` `1069996a…`. `check_delivery.py`는 `part4-practice.zip` 통과 뒤 `llm-practice.zip` Ch 1 01절 노트북에서 `Stale file`(전과 같은 자리). 묶음을 풀어 `notebooks/`에서 10절을 PYTHONPATH 없이 새 커널로 실행 → PASS.
- 서비스 요청 214번(임베딩 143 · 답 모델 71), 0.05달러 아래.

