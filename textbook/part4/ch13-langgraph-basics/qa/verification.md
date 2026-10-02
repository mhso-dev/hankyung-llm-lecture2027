# Ch13 실행 및 빌드 검증

## 새 커널 실행

2026-09-10에 `textbook/_notebook/execute.py`로 7개 노트북을 각각 새 Python 3.12.13 커널에서 실행했습니다. 모든 노트북은 `status=passed`, `fresh_kernel=true`, `allow_errors=false`이며 코드와 출력 SHA-256을 메타데이터에 기록했습니다.

커리큘럼의 LangGraph 1.2 계열 안에서 1.2.11을 고정했습니다. LangChain 1.4.0이 `langgraph>=1.2.11,<1.3.0`을 요구하므로 1.2.0과 함께 해석할 수 없었습니다. `pyproject.toml`, `uv.lock`, 노트북 설치 셀, 본문 참고 버전, 실제 출력은 모두 1.2.11로 맞췄습니다.

01~06절은 강의 1시간·실습 1시간씩, 07절은 통합 범위에 맞춰 강의 2시간·실습 2시간으로 배정했습니다. 합계는 챕터 설정과 같은 강의 8시간·실습 8시간입니다. 절별 새 용어는 실제 첫 정의를 기준으로 3~7개이며 상한 7개를 지켰습니다.

| 절 | 코드 셀 | 핵심 실제 출력 |
| --- | ---: | --- |
| 01 | 6 | `normalize → make_query`, 질문 변경 뒤 같은 노드 순서 |
| 02 | 5 | `query` 덮어쓰기, `log` 세 항목 누적 |
| 03 | 5 | 0.82는 `generate`, 0.41은 `request_more` |
| 04 | 5 | human·ai 두 메시지, 같은 h1 ID 내용 교체 |
| 05 | 5 | 입력 문서 3건은 결과 3건, 1건은 결과 1건 |
| 06 | 5 | `sufficient/generate`, `insufficient/request_more` |
| 07 | 12 | PDF 6건 35쪽, E01 p.3·E02 p.3, 7권·14일 답변, 1,230 tokens |

07절은 Ch12 Q002와 제공 PDF를 읽어 `text-embedding-3-small` 256차원 임베딩, Kiwi BM25, RRF(k=60), `BAAI/bge-reranker-v2-m3`, `gpt-5.4-mini`를 실제 실행했습니다. 통합 실행은 13,186.79ms였고 결과는 `labs/part4/ch13-langgraph-basics/runs/graph-integrated-result.json`에 저장했습니다. 이 한 질문의 실행은 흐름과 입출력 형식을 확인하며 전체 검색·생성 품질을 평가하지 않습니다.

## 정적·화면 검증

- 빌드: `_build.py`가 `index.html`과 7개 절 HTML을 생성했습니다.
- 노트북 계약: `verify.py --chapter textbook/part4/ch13-langgraph-basics`가 7절, 코드 셀 43개, 셀 최대 24줄을 통과했습니다.
- 화면: `visual.cjs`가 1280px·390px의 16개 화면을 검사했습니다. 작은 글자, 대비 실패, 잘림, 본문 밖 텍스트, SVG 경계 초과, 가로 넘침, 깨진 이미지, 복사 오류는 모두 0건입니다.
- 본문 분량: HTML 태그를 제외한 7절 합계는 20,308자입니다.

## 확인 필요 항목

- 별도 한국어 검토 세션의 최종 판정은 `accept`입니다. 기록은 `textbook/part4/qa/language/ch13-final-audit-2026-09-10.md`에 있습니다.
- Excalidraw MCP 미제공 환경이어서 연결 도구의 미리보기는 사용하지 않았습니다. SVG와 Excalidraw JSON은 같은 생성 데이터로 만들고 브라우저에서 SVG 경계를 검사했습니다.

## 품질 개선 검증 (규격 `textbook/QUALITY-UPGRADE.md`, 2026-09-19~)

위 기록은 개선 전(2026-09-10) 것입니다. 개선한 절은 아래 표에 절 단위로 덧붙입니다.
절별 기록은 `qa/upgrade/NN-diagnosis.md`, 절 사이 인계는 `qa/upgrade/handoff.md`, 검토용 묶음은 `qa/upgrade/review-pack/`입니다.

| 절 | 게이트 G1~G7 | 새 커널 | verify | 빌드 | 그림 |
| --- | --- | --- | --- | --- | --- |
| 01 StateGraph와 노드·엣지 | 44 → **0 (PASS)**, `qa/upgrade/gates-wip-01.json` | `PASS 01-StateGraph와-노드-엣지.ipynb: 24 cells`(2026-09-19). 같은 코드로 **새 커널 두 번** 실행해 셀별 출력 글자 수와 해시가 모두 같았고 교재에 실린 출력은 마지막 실행입니다. **모델 요청 0번**이라 실행마다 달라지는 값이 없습니다. | `PASS 7 sections / 61 code cells (max 24 lines)` | 빌드 HTML 여덟 개 모두 `{{` 잔존 0건. 고치지 않은 02~07절 HTML과 `index.html`의 sha256이 빌드 전후로 같습니다. | Mermaid 4장(`01-1`~`01-4`, 원본 폭 256·473·810·791) · 삽화 1장(`01-5`, 1차 job `a4d78b83…` 채택, 2크레딧). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/01-figures.md`. |
| 02 상태 갱신 | 33 → **0 (PASS)**, `qa/upgrade/gates-wip-02.json` | `PASS 02-State-갱신.ipynb: 22 cells`(2026-09-19). 같은 코드로 **새 커널 두 번** 실행해 셀별 출력 글자 수와 해시가 모두 같았고 교재에 실린 출력은 마지막 실행입니다. **모델 요청 0번**이라 실행마다 달라지는 값이 없습니다. | `PASS 7 sections / 78 code cells (max 24 lines)` | 빌드 HTML 여덟 개 모두 `{{` 잔존 0건. 고치지 않은 01·03~07절 HTML과 `index.html`의 sha256이 빌드 전후로 같습니다. | Mermaid 4장(`02-1`~`02-4`, 원본 폭 820·479·845·844) · 삽화 1장(`02-5`, **2차 job `dd55cde4…` 채택**, 1차 job `685f1306…` 탈락, 두 상자가 같아 보임). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/02-figures.md`. |
| 03 조건부 엣지 | 35 → **0 (PASS)**, `qa/upgrade/gates-wip-03.json` | `PASS 03-조건부-엣지.ipynb: 26 cells`(2026-09-19). 같은 코드로 **새 커널 두 번** 실행해 셀별 출력 글자 수와 해시가 모두 같았고 교재에 실린 출력은 마지막 실행입니다. **모델 요청 0번**이라 실행마다 달라지는 값이 없습니다. | `PASS 7 sections / 99 code cells (max 24 lines)` | 빌드 HTML 여덟 개 모두 `{{` 잔존 0건. `_build.py`를 다시 돌려 여덟 개의 sha256이 모두 같았습니다. | Mermaid 4장(`03-1`~`03-4`, 원본 폭 745·421·820·777) · 삽화 1장(`03-5`, **1차 job `426e9a61…` 채택**, 2크레딧). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/03-figures.md`. |
| 04 add_messages 리듀서 | 53 → **0 (PASS)**, `qa/upgrade/gates-wip-04.json` | `PASS 04-add_messages-리듀서.ipynb: 27 cells`(2026-09-19). 같은 코드로 **새 커널 두 번** 실행해 셀별 출력 글자 수와 해시가 모두 같았고 교재에 실린 출력은 마지막 실행입니다. **모델 요청 0번**이라 실행마다 달라지는 값은 번호를 적지 않은 메시지에 자동으로 붙는 번호 하나뿐이고, 그 값은 어디에도 인용하지 않았습니다. | `PASS 7 sections / 121 code cells (max 24 lines)` | 빌드 HTML 여덟 개 모두 `{{` 잔존 0건. 고치지 않은 01~03·05~07절 HTML과 `index.html`의 sha256이 빌드 전후로 같습니다. | Mermaid 4장(`04-1`~`04-4`, 원본 폭 572·468·842·829) · 삽화 1장(`04-5`, **1차 job `0726f190…` 채택**, 2크레딧). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/04-figures.md`. |
| 05 Send와 동적 팬아웃 | 33 → **0 (PASS)**, `qa/upgrade/gates-wip-05.json` | `PASS 05-Send-동적-팬아웃.ipynb: 26 cells`(2026-09-19). 같은 코드로 **새 커널 두 번** 실행해 셀별 출력 글자 해시 26개가 모두 같았고 교재에 실린 출력은 마지막 실행입니다. **모델 요청 0번**이라 실행마다 달라지는 값이 없습니다. 팬아웃 결과가 모이는 차례도 두 번 모두 같았지만 라이브러리 약속이 아니라 결론·그림에 넣지 않았습니다. | `PASS 7 sections / 142 code cells (max 24 lines)` | 빌드 HTML 여덟 개 모두 `{{` 잔존 0건. 고치지 않은 01~04·06~07절 HTML과 `index.html`의 크기가 빌드 전후로 같습니다. | Mermaid 4장(`05-1`~`05-4`, 원본 폭 249·465·707·806) · 삽화 1장(`05-5`, **1차 job `56af192a…` 채택**, 2크레딧). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/05-figures.md`. |
| 06 Command의 갱신과 이동 | 43 → **0 (PASS)**, `qa/upgrade/gates-wip-06.json` | `PASS 06-Command-갱신과-이동.ipynb: 27 cells`(2026-09-19). 같은 코드로 **새 커널 두 번** 실행해 셀별 출력 글자 해시 27개가 모두 같았고 교재에 실린 출력은 마지막 실행입니다. **모델 요청 0번**이라 실행마다 달라지는 값이 없습니다. | `PASS 7 sections / 164 code cells (max 24 lines)` | 빌드 HTML 여덟 개 모두 `{{` 잔존 0건. 고치지 않은 01~05·07절 HTML과 `index.html`의 sha256이 빌드 전후로 같습니다. | Mermaid 4장(`06-1`~`06-4`, 원본 폭 445·421·721·743) · 삽화 1장(`06-5`, **1차 job `008657f6…` 채택**, 2크레딧). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 설계표 `qa/upgrade/06-figures.md`. |

- 챕터 수정 전 게이트: `qa/upgrade/gates-before.json`(2026-09-19, 일곱 절 합계 **337** = 44·33·35·53·33·43·96, 통과 0/7).
- 옛 생성기 `qa/author_ch13.py`와 `figures/_gen_figures.py`는 첫머리 주석과 `raise SystemExit(...)`로 실행을 막았습니다(`from __future__` 다음 줄에 두어야 합니다). 파일은 지우지 않았고 챕터 마감 때 `qa/upgrade/before/generators/`로 옮깁니다.
- 실습 폴더에 `tests/`가 없어 작업 전후로 견줄 실습 폴더 테스트가 없습니다. `uv sync --locked`는 마운트 폴더 삭제 제한 때문에 돌리지 않았고, `uv.lock`에 dev `pip==26.2`가 있는 것만 확인했습니다.
- 화면 검사(`visual.cjs`)와 `gates-after.json`은 챕터 마감 때 한 번에 돌립니다.
- 02절은 패키지를 더 넣지 않았습니다. 01절이 만든 `.cache/vm/venv-ch13-langgraph-basics`를 그대로 썼고 `%pip` 셀도 `langgraph==1.2.11` 한 줄 그대로라 실습 폴더 `pyproject.toml`·`uv.lock`을 손대지 않았습니다.
- 그림 색: 02절은 「낸 갱신」 상자를 **파랑**으로 뒀습니다. 01절 `01-2`는 노드를 직접 불러 갱신을 출력했기에 노랑이었지만, 02절은 갱신을 출력하지 않아 규격 §5-3 「노랑 상자에는 출력으로 확인한 값만」에 맞췄습니다.
- 03절은 패키지를 더 넣지 않았습니다. `%pip` 셀도 `langgraph==1.2.11` 한 줄 그대로라 실습 폴더 `pyproject.toml`·`uv.lock`을 손대지 않았습니다.
- 03절 그림 폭: `03-2`를 `flowchart LR`로 그렸더니 원본 폭이 1255가 되어 `flowchart TB`(421 × 563)로 바꾸고 「도식 읽기」의 방향 말도 「위에서 아래로」로 고쳤습니다. `03-3`(922 → 820)·`03-4`(902 → 777)는 라벨을 `<br>`로 더 잘라 줄였습니다.
- 03절이 남긴 옛 그림 `figures/03-흐름.svg`·`.excalidraw`·`.caption.md`는 지우지 않았고 `qa/upgrade/before/figures/`에도 복사해 두었습니다.
- 04절은 `%pip` 셀에 `langchain==1.4.0`이 하나 늘었습니다(메시지 클래스가 `langchain.messages`에 있어서). 실습 폴더 `pyproject.toml`의 `dependencies`와 `uv.lock`에 **이미 같은 판이 고정돼 있어** 두 파일을 손대지 않았습니다(`uv.lock`에 `langchain == 1.4.0`·`langgraph == 1.2.11`·dev `pip == 26.2` 확인, 규격 §7-2). 마운트 폴더 삭제 제한 때문에 `uv sync --locked`는 돌리지 않았습니다.
- 04절 그림 색: 함수 `add_messages`는 **라이브러리가 주는 것이라 회색**으로 뒀습니다(`START`·`END`와 같은 판단). 우리가 만든 노드와 그 노드가 낸 갱신은 파랑입니다. 05절 `Send`도 같은 자리로 봅니다.
- 04절 그림 폭: `04-3`이 처음 869여서 회색 상자 라벨을 한 줄 줄이고 칸 제목을 `operator.add로 붙인 뒤`로 고쳐 842로 맞췄습니다.
- 04절 삽화는 오른쪽 상자의 쪽지 넷 가운데 두 장이 같은 모양으로 보이지 않습니다. 「그림 읽기」는 꽂힌 쪽지 수가 셋과 넷으로 다르다는 것만 짚습니다(저장 파일을 열어 보고 씀, 규격 §5-4).
- 04절이 남긴 옛 그림 `figures/04-흐름.svg`·`.excalidraw`·`.caption.md`는 지우지 않았고 `qa/upgrade/before/figures/`에도 복사해 두었습니다.
- 05절은 패키지를 더 넣지 않았습니다. `%pip` 셀이 `langgraph==1.2.11` 한 줄이라 실습 폴더 `pyproject.toml`·`uv.lock`을 손대지 않았습니다(04절이 더한 `langchain==1.4.0`은 이 절에서 부르지 않습니다).
- 05절 그림 색: `Send`는 **라이브러리가 주는 것이라 회색**입니다(04절 `add_messages`와 같은 자리). 받아 출력한 오류 `InvalidUpdateError`는 **노랑**입니다(규격 §5-3, Before 아닌 절에서 받은 오류, Ch 6 02-1 선례).
- 05절 그림 폭: `05-1`·`05-2`를 `flowchart LR`로 그렸더니 원본 폭이 1051과 905여서 둘 다 `flowchart TB`(249·465)로 바꾸고 「도식 읽기」의 방향 말도 「위에서 아래로」로 고쳤습니다.
- 05절 팬아웃 차례: 탐색 실행 다섯 번과 본 실행 두 번 모두 `D01`·`D02`·`D03` 차례였습니다. 라이브러리가 약속한 것이 아니므로 본문에는 「이번 실행에서는」으로 한정했고 그림 라벨과 정리 세 줄에서는 뺐습니다.
- 05절이 남긴 옛 그림 `figures/05-흐름.svg`·`.excalidraw`·`.caption.md`는 지우지 않았고 `qa/upgrade/before/figures/`에도 복사해 두었습니다.
- 06절은 패키지를 더 넣지 않았습니다. `%pip` 셀이 `langgraph==1.2.11` 한 줄이라 실습 폴더 `pyproject.toml`·`uv.lock`을 손대지 않았습니다.
- 06절은 옛 노트북 반환형 `Command[Literal[...]]`를 빼고 `add_node(..., destinations=(...))`로 바꿨습니다. `Literal`은 Part 3에서 0건이고 01~05절도 쓰지 않아 새 문법을 겹치지 않으려고 고른 길입니다(과정 요약 §2-3).
- 06절 그림 색: `Command`는 **라이브러리가 주는 것이라 회색**입니다(04절 `add_messages`·05절 `Send`와 같은 자리). 그 객체를 내놓는 노드 `route`와 객체 안에 담은 값 둘은 파랑입니다. 받아 출력한 오류가 없어 **빨강 0장**이고 모델을 부르지 않아 **보라 0장**입니다.
- 06절 그림 폭: `06-1`·`06-2`는 상자가 넷 이상 이어져 처음부터 `flowchart TB`로 그렸습니다(445·421). 05절 메모를 그대로 따랐습니다.
- 06절이 출력으로 확인한 `destinations`의 자리: 적어 두면 구조 문자열에 `route -.-> ask_more;`와 `route -.-> make_answer;`가 생기고 적지 않으면 `route --> __end__;` 한 줄만 남습니다. 두 판의 실행 결과는 같았습니다(`목적지를 적어 둔 판의 결과와 같은가: True`).
- 06절이 남긴 옛 그림 `figures/06-흐름.svg`·`.excalidraw`·`.caption.md`는 지우지 않았고 `qa/upgrade/before/figures/`에도 복사해 두었습니다.
- 07절은 **패키지를 새로 넣었습니다**. `%pip` 셀이 `langgraph==1.2.11`·`langchain==1.4.0`·`langchain-openai==1.6.1`·`python-dotenv==1.2.3`·`kiwipiepy==0.23.2`·`rank-bm25==0.2.2` 여섯 줄입니다. 여섯 판 모두 실습 폴더 `pyproject.toml`·`uv.lock`에 **이미 고정돼 있어** 두 파일을 손대지 않았습니다(규격 §7-2). 작업 가상환경에는 `bin/python -m pip install`로 직접 넣었습니다(마운트 폴더에서 `uv pip install`이 멈춤, handoff 챕터 공통).
- 07절이 **쓰지 않게 된 패키지 넷**: `pypdf`·`numpy`·`scikit-learn`·`sentence-transformers`. 개선 전 07절이 PDF를 다시 읽고 리랭커를 올리며 쓰던 것입니다. `pyproject.toml`·`uv.lock`에는 그대로 두었습니다(빼려면 잠금과 묶음 둘을 다시 만들어야 해 챕터 마감 몫).
- 07절은 **Ch 12 인계**(Ch 12 요약 §13-2)를 처리했습니다. 통합 기록의 지금 값을 직접 열어 확인한 뒤 옛 생성기 `qa/author_ch13.py` 261행 `"prior"`와 `_src` b3을 고쳤습니다. 지금 값은 `retrieved` 세 건(`E01-P03-C02`·`E01-P03-C01`·`E01-P03-C06`, 부모가 모두 `E01`)·`settings.reranker` `null`·`settings.context_selection` `matched-chunk-text`입니다. 노트북 3절이 같은 값을 출력으로도 보입니다.
- 07절 그림 색: **이 챕터에서 처음 보라가 나오는 절**입니다(`07-2`의 모델 상자 하나, 실제로 부른 모델). 받아 출력한 오류가 없어 빨강은 0장입니다. 상태·칸·넣은 값·문서 청크는 초록, 우리가 만든 노드는 파랑, 출력으로 확인한 값은 노랑입니다.
- 07절 그림 폭: `07-1`(205)·`07-2`(200)는 상자가 다섯 이상 이어져 처음부터 `flowchart TB`로 그렸습니다. 이 챕터에서 가장 좁고 긴 그림이고 높이가 752와 501입니다. `07-3`(728)·`07-4`(761)는 `LR` + 칸 두 개 그대로 지나갔습니다.
- 07절 삽화는 상자 칸이 프롬프트의 여덟이 아니라 **여섯**으로 나왔습니다. 상태의 칸 수와 잇지 않고 「칸이 나뉜 상자」로만 적고, 「그림 읽기」·alt·캡션은 저장한 파일을 보고 「여섯 칸」으로 썼습니다(규격 §5-4).
- 07절은 **파일을 쓰지 않습니다**. Ch 12 파일 둘은 읽기만 했고 바이트가 그대로입니다. 개선 전 07절이 남긴 `labs/part4/ch13-langgraph-basics/runs/graph-integrated-result.json`은 이제 이 절이 만들지 않는 파일이고 내용도 지금 절과 다릅니다(`reranker`가 `BAAI/bge-reranker-v2-m3`, `duration_ms` `13186.79`). 학생 묶음 목록 둘이 그 파일을 담고 있어 **챕터 마감에서 삭제 승인 또는 08 실습 절 재작성으로 정해야 합니다**(`07-diagnosis.md` §5).
- 07절 새 커널 두 번 대조: 코드 셀 32개 가운데 30개의 출력 글자 해시가 같았고, 달라진 둘은 실행 2의 모델 답 한 문장(글자 수 85 → 84)과 그 값을 담은 표 줄뿐입니다. 후보 칸·보고 자리 칸·부모 문서 차례·실행 흔적 칸은 두 번 모두 같았습니다. 교재 출력은 두 번째 실행 결과이고 다시 돌려 고르지 않았습니다(규격 §3).
- 07절이 남긴 옛 그림 `figures/07-흐름.svg`·`.excalidraw`·`.caption.md`는 지우지 않았고 `qa/upgrade/before/figures/`에도 복사해 두었습니다.
- 08절은 **새로 만든 챕터 끝 실습 절**입니다(규격 §7-2). `chapter.json`에 `experiment`로 더했고 **챕터 시수에 더하지 않았습니다**(meta 「실습 30분」). 절 meta 시수 합은 그대로 강의 8h·실습 8h입니다.
- 08절은 패키지를 더 넣지 않았습니다. `%pip` 셀이 07절과 같은 여섯 줄이고 여섯 판 모두 실습 폴더 `pyproject.toml`·`uv.lock`에 이미 고정돼 있습니다(규격 §7-2).
- 08절이 읽는 파일은 `labs/part3/ch12-retrieval-tuning/data/advanced-documents.json` 하나이고 **07절이 이미 요구하던 파일**입니다. 새 파일을 읽지 않아 묶음 허용 목록에서 고칠 것은 노트북 한 줄뿐이었습니다(`textbook/part4/public-files.json`, `qa/public-files.json`은 `notebooks/*.ipynb` 글로브).
- 08절은 **파일을 쓰지 않습니다**(Part 3 실습 절 넷·07절 선례, contracts §3). 그래서 `runs/graph-integrated-result.json`은 07절 때와 같은 상태로 남았고 **챕터 마감의 결정 대상**입니다. 08절이 다시 쓰지 않은 까닭 네 가지는 `08-diagnosis.md` §5에 있습니다(칸 `duration_ms`를 지키려면 걸린 시간을 재야 하고, 칸 `usage`는 실행 1에만 있으며, 칸 `node_trace`·`retrieved`의 값이 이 절 그래프와 다르고, 실습 절은 파일을 쓰지 않는 쪽이 안전함). 2026-09-19에 `grep -rn "graph-integrated-result" --exclude-dir=.venv textbook labs`로 다시 확인한 결과 **코드로 읽는 쪽은 없습니다**.
- 08절 그림 색: `START`·`END`와 라이브러리가 주는 것은 회색, 우리가 만든 노드 다섯은 파랑, 우리가 넣은 값(질문·기준값)은 초록, 출력으로 확인한 값은 노랑, 실제로 부른 모델은 보라입니다. 받아 출력한 오류가 없어 **빨강 0장**입니다.
- 08절 그림 폭: `08-1`(405)·`08-2`(415)는 처음부터 `flowchart TB`로 그렸고 `08-3`(791)은 `LR` + 칸 두 개입니다. 모두 약 868 아래입니다. 렌더 PNG를 열어 보니 `08-2`의 기준값 초록 상자가 **오른쪽**에 놓여 alt와 「도식 읽기」의 방향 말을 왼쪽에서 오른쪽으로 고쳤습니다(규격 §5-3).
- 08절 삽화는 1차 job `6b2dd10a-680d-4338-afbf-bf97365639ce`를 채택했습니다. 저장 PNG(1100 × 613)를 채택 job 결과에서 같은 폭으로 줄인 그림과 픽셀 단위로 대조해 차이가 없었습니다(`ImageChops.difference` bbox `None`, 규격 §5-4). 프롬프트에 적지 않은 연장이 작업대마다 놓여 나와 alt에 「연장이 놓인」으로 적었습니다.
- 08절 기준값 `5.0`·`9.0`은 **탐색 실행 뒤 정한 예**입니다(규격 §3). 낱말 순위 1위의 점수가 `7.64`라는 것을 먼저 보고 위아래로 하나씩 잡아 두 길이 모두 보이게 했습니다. 본문 b4 「두 번의 실행」과 b7 둘째 줄에 그 사실을 적었습니다.
- 08절 새 커널 두 번 대조: 코드 셀 **32개 모두** 출력 글자 수와 해시가 같았습니다(모델 답 한 문장까지 같음). 그래도 모델 문장은 실행마다 달라질 수 있어 낱말을 확인 줄로 보지 않았고 그림 라벨에도 넣지 않았습니다(과정 요약 §6).
- 08절 뒤 절 수 검사·과정 단계 검사(규격 §7-2): `textbook/part4/_build_index.py`에는 **절 수 칸이 없어**(슬러그·강의 시수·실습 시수·설명 네 칸) 고칠 곳이 없었고 실제로 돌려 `Part 4: 31 verified sections; 88 bundled files`를 확인했습니다(30 → 31). `textbook/qa/check_course_continuity.py`는 202행 묶음 목록에 **part4가 없어** 고칠 해시 허용 목록이 없었고, 돌리면 이 절 작업 전과 같은 자리인 **212행 `Stale archive: part1-practice.zip/labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`**에서 멈춥니다.
- 07절 「다음 학습과 이어지는 지점」과 07 노트북 정리 셀은 `mdpatch.py`로 08절을 가리키게 고쳤습니다(**07절은 다시 실행하지 않음**, 규격 §3). 같은 자리의 「이 챕터에서 모델을 부른 절은 이 절 하나입니다」는 08절이 생겨 사실이 아니게 되어 뺐습니다.

## 챕터 마감 검증 (2026-09-19, 검토 1차 반영 뒤)

위 「품질 개선 검증」 표의 개선 전 블록(25~28행)은 **7절 기준**입니다. 8절 기준 수치는 아래와 같습니다.

| 항목 | 개선 전(2026-09-10, 7절) | 마감(2026-09-19, 8절) |
| --- | --- | --- |
| 절 HTML | `index.html` + **7개** | `index.html` + **8개** |
| 코드 셀 | 43 | **216** |
| `visual.cjs` 화면 | 16 | **18**(1280px·390px 각 9쪽, 전부 PASS) |
| Mermaid·삽화 | 절마다 옛 도식 1장 | Mermaid **31장** · 삽화 **8장** |
| 게이트 | 일곱 절 합계 337(통과 0/7) | **8/8 PASS, G1~G7 0**(`qa/upgrade/gates-after.json`) |

- `verify.py --chapter textbook/part4/ch13-langgraph-basics` → `PASS 8 sections / 216 code cells (max 23 lines)`.
- 화면 검사는 공용 `textbook/_notebook/visual.cjs`의 `/tmp/ch13close/visual.cjs` 사본으로 돌렸습니다(`require('playwright-core')`·`executablePath`·출력 폴더만 다름). **공용 원본은 고치지 않았습니다.** 결과는 공용 `textbook/_notebook/checks/ch13-langgraph-basics/visual-results.json` **18행**이고 스크린숏 네 장(index·01절)도 다시 찍었습니다.
- **노트북 재실행 0회**: 여덟 노트북 모두 `execute.py`의 해시 함수로 다시 계산한 `code_sha256`·`outputs_sha256`이 저장된 값과 같습니다(예: 08절 `ebec81cd…`·`3e2576c3…`).
- 검토 반영은 `mdpatch.py`·`_src` 직접 편집·`.mmd` 두 장 다시 렌더(`03-2`·`08-2`)·`run_section.sh … --no-exec`로만 했습니다. **렌더 도장(`*.render.json`) 31개를 지우지 않았고 다시 계산한 해시가 모두 같습니다.**
- 보호 파일: `textbook/part3/qa/continuity-evidence/before-manifest.json`의 `runs/`·`data/` **125개를 바이트로 다시 계산해 어긋난 항목 0건**입니다. `labs/part4/ch13-langgraph-basics/runs/graph-integrated-result.json`도 `c704a2eb…` 그대로이고 **이 챕터는 `runs/`에 쓰지 않습니다**.
- 묶음: `python3 textbook/part4/_build_index.py` → `Part 4: 31 verified sections; 88 bundled files`, `textbook/downloads/part4-practice.zip` **91항목**. `textbook/part4/qa/check_delivery.py`는 그 묶음을 통과한 뒤 **`llm-practice.zip`의 Ch 1 01절 노트북에서 `Stale file`로 멈춥니다**(2026-09-14 판, 전체 마감 몫). `textbook/part3/qa/check_continuity.py`는 154행 part2 zip, `textbook/qa/check_course_continuity.py`는 212행 part1 zip에서 멈추고 **작업 전과 같은 자리**입니다.


## §2-7 리팩터 검증 (2026-09-21)

규격 §2-7(앞에서 배운 함수는 도구 파일 `labs/part4/ch13-langgraph-basics/notebooks/rag_tools.py`에서, 벡터 계산은 NumPy로)을 적용한 뒤의 검증입니다. 세부는 `qa/upgrade/handoff.md` 「§2-7 리팩터 (2026-09-21)」.

| 절 | 바뀐 것 | 새 커널 두 번 | 리팩터 전 출력과 |
| --- | --- | --- | --- |
| 01 | 없음(다시 실행 안 함) | — | 같음(노트북 그대로) |
| 02 | `print_state` 가져옴, 설치 `numpy==2.5.3` | PASS 21 cells, 두 번 셀별 출력 글자·`outputs_sha256` `9bd1044d…` 같음 | 설치 셀 `numpy: 2.5.3` 줄만 다름 |
| 03 | `normalize`·`make_query` 가져옴 | PASS 24 cells, 두 번 같음(`51c489c1…`) | 설치 셀 줄만 다름 |
| 04 | 없음(다시 실행 안 함) | — | 같음 |
| 05 | 마크다운 두 곳만(`--no-exec`) | — | 같음(노트북 해시 그대로) |
| 06 | `normalize`·`make_answer`·`ask_more` 가져옴 | PASS 24 cells, 두 번 같음(`e2daa2a0…`) | 설치 셀 줄만 다름 |
| 07 | Ch 12 함수 여섯 개 가져옴(준비 셀 일곱 → 문서 청크 짝 셀 하나) | PASS 26 cells, 두 번 셀별 출력 글자 26/26 같음(`outputs_sha256`은 `%pip` 스트림 조각 수로만 다름) | 실행 2 답 표현과 `답 칸의 글자 수 \| 84` → `89`만 다름(인용 안 함). 보고 자리·부모 차례·실행 흔적 같음 |
| 08 | `normalize`와 Ch 12 함수 여섯 개 가져옴(준비 셀 여섯 → 설명 소절) | PASS 25 cells, 두 번 25/25 같음(`f371b90b…`) | 실행 1 모델 답 표현만 다름. 점수 `7.64`·기준값 `5.0`/`9.0`에 따른 길·보고 자리 같음 |

- `upgrade_gates.py --label after-2-7` → **8/8 PASS, G1~G7 0**. `verify.py --chapter` → `PASS 8 sections / 197 code cells (max 18 lines)`. 빌드 HTML 9개 `{{` 0건.
- `visual.cjs`(사본 `/tmp/ch13-27/vis/vis.cjs`) 02·03·05·06·07·08 × 1280px·390px **12/12 PASS** → `qa/upgrade/visual-after-2-7.json`(공용 `checks/ch13-langgraph-basics/visual-results.json`은 그대로).
- 도구 파일: Ch 12 구역 11개가 Ch 12 도구 파일과 AST 같음, 01~06 구역 5개가 각 절 노트북 판과 AST 같음, 금지 문법 0건, 함수 본문 최대 8줄. SHA-256 `6dc956c5…`.
- Ch 12 읽는 파일: `advanced-documents.json` `832d89c2…`(그대로)·`advanced-continuity-integrated-result.json` `7b142cd5…`(Ch 12 §2-7 판), 07절 3절 출력 일곱 값 리팩터 전과 같음. `runs/graph-integrated-result.json` `c704a2eb…` 그대로.
- 묶음: `_build_index.py` → `Part 4: 32 verified sections; 94 bundled files`, `part4-practice.zip` `484a448d…`. `check_delivery.py`는 `part4-practice.zip` 통과 뒤 `llm-practice.zip` Ch 1 01절 노트북에서 `Stale file`(전과 같은 자리). 묶음을 풀어 `notebooks/`에서 08절을 PYTHONPATH 없이 새 커널로 실행 → PASS.
- 서비스 요청 22번(임베딩 15 · 답 모델 7), 0.01달러 아래.
- **04·05 `normalize` 정리(2026-09-21, 같은 날)**: 04·05도 도구 파일의 02절 판 `normalize`를 가져오게 바꿈(정의 셀 둘 삭제, 설치 셀 `numpy==2.5.3`). 04 PASS 26 cells·05 PASS 25 cells, 새 커널 두 번 셀별 출력 글자 같음(모델 요청 0번), 리팩터 전과 설치 셀 `numpy: 2.5.3` 한 줄만 다름. 게이트 8/8·`verify` `PASS 8 sections / 195 code cells (max 18 lines)`·`{{` 0·visual 04·05 4/4(`visual-after-2-7.json` 14/14). `part4-practice.zip` `07a40b22…`(95파일), `check_delivery.py`는 전과 같은 자리에서 멈춤, 묶음 `notebooks/`에서 04·05 PYTHONPATH 없이 PASS. 세부 `qa/upgrade/handoff.md` 「04·05 `normalize` 정리」.
