# Ch 13 07절 「Ch 12 검색을 그래프로 잇기」 품질 개선 기록

규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md`, 계약 `textbook/qa/upgrade-contracts.md`.
생성기 `qa/upgrade/author_07.py` · 설계표 `qa/upgrade/07-figures.md` · 묶음 `qa/upgrade/review-pack/07-RAG-통합과-시각화.md`.
수정 전 원본은 `qa/upgrade/before/`(`_src/07-RAG-통합과-시각화.html`, `notebooks/07-RAG-통합과-시각화.ipynb`, `figures/07-흐름.*`)에 있습니다.
작업일 2026-09-19 · 서비스 요청 **다섯 번**(임베딩 3 + 답 모델 2) · 새 커널 **두 번** 실행.

## 1. 게이트 전후

| 게이트 | 전(`gates-before.json`) | 후(`gates-wip-07.json`) |
|---|---|---|
| G1 문법 사다리 | 13 | **0** |
| G2 셀 모양 | 7 | **0** |
| G3 주석 | 0 | **0** |
| G4 실제 모델 | 0 | **0** |
| G5 노트북 설명 | 9 | **0** |
| G6 문장 | 64 | **0** |
| G7 그림 | 3 | **0** |
| 합계 | **96** | **0 (PASS)** |

- 새 커널: `PASS 07-RAG-통합과-시각화.ipynb: 32 cells`.
- verify: `PASS 7 sections / 184 code cells (max 23 lines)`(챕터 전체).
- 빌드: 여덟 HTML 모두 `{{` 잔존 0건이고 고치지 않은 일곱 파일(01~06절·`index.html`)의 크기가 빌드 전후로 같습니다.
- 수정 전 검사 문장 수는 165개였고 개선 뒤 318개입니다. 코드 셀 32개(설치·import·키·Ch 12 함수 준비 열 개가 `lesson_role="setup"`), 셀당 코드 줄 수 최대 15줄, 함수 본문 최대 10줄.
- **새 커널 두 번 대조**: 코드 셀 32개 가운데 30개의 출력 글자 해시가 같았습니다. 달라진 둘은 실행 2의 모델 답 한 문장(글자 수 85 → 84)과 그 값을 담은 표 줄뿐입니다. 후보 칸·보고 자리 칸·부모 문서 차례·실행 흔적 칸·노드 수·엣지 수는 두 번 모두 같았습니다. **교재 출력은 두 번째 실행 결과**이고 다시 돌려 고르지 않았습니다(규격 §3).

## 2. 수정 전 주요 문제

1. **G6 64건** — 70자 초과 문장 21개, 영문·코드 이름으로 시작해 조사가 바로 붙는 문장 33개, 5문장 넘는 단락 10개. 「load_pages는」·「dense_search는」·「RRF는」·「trace는」으로 시작하는 문장이 본문 전체에 있었습니다. 일곱 절 가운데 게이트 합계가 가장 큰 절이었습니다(96).
2. **G1 13건 — 금지 문법** — 내포식 10건, 제너레이터 식 2건, 한 셀에 함수 둘 1건. `lambda`·`key=`·`reverse=`·f-string·`sorted(..., reverse=True)`도 섞여 있었습니다. 과정 요약 §2-3에서 Part 3가 한 번도 쓰지 않은 문법입니다.
3. **G2 7건 — 셀 모양** — 15줄 초과 셀 다섯, 한 줄 복합문 둘. 코드 셀이 **12개**뿐이라 셀 하나가 상태 형식과 노드 정의와 실행을 함께 맡았습니다.
4. **G5 9건** — 제목 셀과 핵심 그림 첨부가 없었고, 코드 셀 앞뒤 설명 셀이 대부분 없었습니다.
5. **G7 3건** — Mermaid 0장, 삽화 0장, 설계표 없음. 그림은 옛 `07-흐름.svg` 한 장뿐이었고 그 「도식 읽기」가 이 절에 없는 빨강(오류·격리)까지 설명했습니다.
6. **Ch 12 인계 — 낡은 문장**(Ch 12 요약 §13-2, handoff 「§01 → §02」 8항). 옛 생성기 `qa/author_ch13.py` 261행 `"prior"`와 `_src` b3에 「Ch12의 `runs/advanced-continuity-integrated-result.json`에는 Q002 질문, **검색된 E01·E02 쪽**, 실제 모델 응답, 고정 설정이 있습니다」가 있었습니다. 실제 기록을 열어 보니 `retrieved`는 `E01-P03-C02`·`E01-P03-C01`·`E01-P03-C06` 세 건이고 **부모가 모두 `E01`**이며, `settings.reranker`는 `null`, `context_selection`은 `matched-chunk-text`입니다.
7. **본문 숫자가 기록과 어긋남** — b6·b8의 「E01 3쪽과 E02 3쪽을 선택」·「1,230개의 총 토큰」·검증 기록의 `13,186.79ms`는 2026-09-10 실행 값입니다. 걸린 시간은 Ch 12부터 한 번도 재지 않기로 했습니다(규격 §3).
8. **앞 절과 이어지지 않음** — 상태 이름 `RAGState`의 칸이 아홉인데 01~06절 이름·값이 하나도 나오지 않았고, 노드가 `state['trace'] + ['이름']`으로 앞 값까지 함께 내 01절 이전 모양이었습니다(02절이 정한 약속과 어긋남).
9. **Ch 12와 다른 문서 청크를 새로 만듦** — 옛 노드 `load_pages`가 `pypdf`로 PDF 여섯 건을 다시 읽어 쪽마다 `{doc_id}-P{page:02d}-C01` 하나씩 35개를 만들었습니다. Ch 12 문서 청크 175개와 ID 체계는 같지만 내용이 다른 별도 자료였습니다.
10. **리랭커를 부름** — 옛 `rerank` 노드가 `BAAI/bge-reranker-v2-m3`를 올렸습니다. 모델 파일 약 2.2GB, 최대 RSS 약 3.1GB로 기기 메모리 3.8GB에 빠듯합니다(contracts §7).

## 3. 바꾼 것

### Ch 12 인계 처리 (handoff 「§06 → §07」 3항 — 이 절 차례)

- **무엇을 고쳤나**: (1) 옛 생성기 `qa/author_ch13.py`의 `"prior"` 문장(handoff의 251행 → 지금 **261행**), (2) 그 문장이 그대로 들어가 있던 `_src/07-RAG-통합과-시각화.html` **b3**.
- **어떻게 고쳤나**: 먼저 `labs/part3/ch12-retrieval-tuning/runs/advanced-continuity-integrated-result.json`을 직접 열어 값을 확인했습니다(`qid` `Q002`, `gold_doc_ids` `["E01"]`, `retrieved` 세 건 `E01-P03-C02`·`E01-P03-C01`·`E01-P03-C06`, `settings.reranker` `null`, `settings.context_selection` `matched-chunk-text`, `settings.weights` `[0.0, 1.0]`, `settings.dimensions` `256`, `settings.chat` `gpt-5.4-mini`). 그다음 b3을 「그 기록이 모델에 넣은 문서 청크는 세 건이고 부모가 모두 `E01`입니다」·「설정 칸 `reranker`의 값은 `None`이라 Ch 12는 리랭킹을 쓰지 않았습니다」·「설정 칸 `context_selection`의 값은 `matched-chunk-text`라 모델에 넣은 것은 쪽 전체가 아니라 문서 청크 본문입니다」로 다시 썼습니다.
- **노트북에도 출력으로 남김**: 3절 셀이 그 세 값을 그대로 출력합니다(`앞 기록이 넣은 문서 청크: ['E01-P03-C02', 'E01-P03-C01', 'E01-P03-C06']`·`앞 기록의 리랭커 설정: None`·`앞 기록이 넣은 것: matched-chunk-text`). 본문 문장과 노트북 출력이 같은 값을 가리킵니다.
- **옛 생성기**: `qa/author_ch13.py`는 첫머리에서 실행을 막아 둔 읽기 자료입니다(01절에서 처리). handoff가 가리킨 251행은 01절이 머리말 주석을 더하면서 **261행**으로 밀려 있었습니다. 그 줄의 `"prior"` 문자열을 지금 값으로 고치고 바로 위에 네 줄 주석으로 무엇을 왜 고쳤는지 적었습니다. `"concept"`·`"observe"`·`"notes"`의 「E01 3쪽과 E02 3쪽」·「1,230 tokens」는 **그 옛 노트북 자신의 실행 결과**를 적은 문장이라 개선 전 기록으로 그대로 두었습니다(코드 셀 목록도 같은 까닭으로 그대로입니다). 고친 뒤 `ast.parse`로 문법을 확인했습니다.
- **`qa/verification.md`·`집필점검표.md`의 옛 표**: 2026-09-10 값(`13,186.79ms` 등)은 개선 전 기록이라 지우지 않고, 새 값을 개선 표에 덧붙였습니다(handoff 3항 마지막 줄).

### 설계 결정

- **상태 형식 이름 `RagState`**(칸 여덟 `question`·`weights`·`distance_ids`·`word_ids`·`candidate_ids`·`picked_ids`·`answer`·`trace`). 옛 이름 `RAGState`를 01~06절 이름 모양(`FlowState`·`RuleState`·`RouteState`·`ChatState`·`FanState`·`DecisionState`)에 맞춰 적었습니다. 칸이 이 챕터에서 가장 많아 새 이름을 붙였습니다(handoff 2항).
- **노드 다섯·고정 엣지 여섯**: `search_distance`·`search_words`·`fuse`·`pick_report`·`make_reply`. 갈래가 없어 조건 함수도 `Send`도 `Command`도 쓰지 않습니다. 이 절은 부품을 한 줄기로 잇는 자리입니다.
- **노드 `normalize`를 넣지 않았습니다.** 질문이 Ch 12 `Q002`라 앞뒤에 빈칸이 없습니다(handoff 2항). 그 사실을 b3에 한 문장으로 적었습니다.
- **리랭커를 부르지 않습니다.** 기기 메모리 3.8GB에 07절 리랭커 최대 RSS 약 3.1GB는 빠듯하고, Ch 12 12·13절이 고른 설정도 `reranker: null`입니다(contracts §7, Ch 12 요약 §6). 까닭을 b7 두 줄에 적었습니다.
- **PDF를 다시 읽지 않습니다.** Ch 12 기록의 `settings.input`이 `advanced-documents.json chunk text`이고 `context_selection`이 `matched-chunk-text`라 Ch 12 문서 청크 175개를 그대로 씁니다. `pypdf`·`numpy`·`scikit-learn`·`sentence-transformers` 네 패키지가 설치 목록에서 빠졌습니다.
- **`numpy`·`sklearn`을 쓰지 않습니다**(과정 요약 §2-3). Ch 12 01절 순수 파이썬 거리 함수 네 개를 글자까지 같은 코드로 가져왔습니다.
- **값 바꿔 보기는 가중치 한 자리**입니다. 설정을 상태의 칸(`weights`)에 담아 두어 그래프를 고치지 않고 넣는 값만 바꿉니다. 이 절이 새로 여는 말 「설정 칸」이 그 자리입니다(meta 「새 용어 1」).
- **파일을 쓰지 않습니다**(§5 참고). 옛 07절은 `runs/graph-integrated-result.json`을 다시 썼습니다.

### Ch 12에서 그대로 가져온 함수와 값 (contracts §4)

- 함수 열한 개를 **이름·인자·코드까지 같게** 다시 정의했습니다: `dot_product`·`vector_length`·`cosine_similarity`·`cosine_distance`(Ch 12 01절), `kiwi_terms`(04절), `rank_by_distance`·`rank_by_bm25`(05절), `fuse_scores`·`fuse_rank`(06절), `unique_chunk_ids`·`parent_ids_of`(07절).
- 값도 같습니다: `similarity_top` 1 · `keep_tags` 아홉 개 · `rank_constant` 60 · `candidate_count` 8 · `report_place` 5 · `context_count` 3 · 임베딩 `text-embedding-3-small`·`dimensions=256` · 답 모델 `gpt-5.4-mini`.
- **준비 셀 묶기**(Ch 12 09절부터 쓴 방법): 함수 열한 개를 준비 셀 여섯 개에 담고 `lesson_role="setup"` + `upgrade_allow=["multiple_defs_in_cell"]`를 붙였습니다. 이 방법이 없으면 코드 셀이 마흔 개를 넘습니다.

### 노트북 (코드 셀 12 → 32)

- 제목 셀·「오늘 볼 그림」 셀을 넣고 설명 → 코드 → 결과 읽기를 반복합니다. 준비 셀은 설치·import·키와 Ch 12 함수 준비 일곱 개를 합쳐 열 개입니다.
- 1~2절 준비, 3절 Ch 12 자료 읽기, 4절 값 정하기, 5절 Ch 12 함수 준비, 6절 상태 형식과 출력 함수, 7절 노드 다섯, 8절 조립과 구조 확인, 9절 실행 1, 10절 값 바꿔 보기, 11절 기록 표입니다.
- **여러 줄로 나오는 값은 개수만 적었습니다**(규격 §2-4): 순위 두 칸은 문서 청크 수만, 답 칸은 글자 수만 적고 답은 라벨 줄 아래 따로 출력합니다.
- `assert`는 경로 확인 한 곳뿐입니다. **모델 답 `assert`는 0건**입니다(규격 §3). 옛 노트북에는 `assert '[E01 p.3]' in result['answer']`가 있었습니다.
- 내포식 열 개와 제너레이터 식 둘은 빈 목록 + `for` + `append`로 풀었고, f-string은 글 `+`로, `sorted(..., reverse=True)`는 Ch 12 방식(점수에 음수를 붙여 `sorted`)으로 바꿨습니다.

### 본문 (`_src/07-RAG-통합과-시각화.html`)

- 학습 질문을 「Ch 12에서 만든 검색과 답 만들기를 노드로 나눠 한 그래프로 이을 수 있을까요?」로 다듬었습니다(옛 질문의 뜻 유지).
- b3을 다섯 단락으로 다시 썼습니다: 01~06절 한 줄 요약, **Ch 12 기록의 지금 값**, 이 절이 그 기록에서 가져오는 것, 이어 쓰는 함수와 값, 노드 `normalize`를 뺀 까닭과 용어 약속.
- b4에 용어 표 둘을 두었습니다. 새 말은 「설정 칸」 하나이고, Ch 12에서 이어 쓰는 말 네 개(1차 검색·보고 자리·순위 합치기·부모 문서)를 따로 적었습니다.
- b6에서 **줄이 나온 차례는 실행 차례가 아니라는 사실**을 새로 적었습니다(구조 문자열의 여섯 줄이 선언 차례로 나옴).
- b7 열세 줄 가운데 리랭커를 빼는 까닭, PDF를 다시 읽지 않는 까닭, 임베딩 값의 흔들림, 모델 답 `assert` 금지, 걸린 시간을 재지 않았다는 문장을 새로 넣었습니다.
- 「reciprocal rank fusion(RRF)」·「재정렬」·「융합」·「필드」·「분기」·「경로」·「반환」을 Ch 12·01~06절 말(「순위 합치기」·「리랭킹」·「칸」·「갈래」·「길」·「내놓다」)로 바꿨습니다.
- meta의 `코드` 칸을 `notebooks/07-RAG-통합과-시각화.ipynb`로 고치고 「새 용어 5 → 1」로 바꿨습니다. **시수는 강의 2h · 실습 2h 그대로**라 절 meta 합이 `chapter.json`의 총 16h와 같습니다.

### 그림 (0장 → Mermaid 4장 + 삽화 1장)

- `07-1-부품-다섯을-한-줄기로`(TB, viewBox 205) · `07-2-답을-쓰는-노드`(TB, 200) · `07-3-가중치-하나만-바꾼-두-실행`(LR 칸 둘, 728) · `07-4-선언한-구조와-실행-흔적`(LR 칸 둘, 761). 넷 다 폭 868 아래입니다.
- **이 챕터에서 처음 보라가 나오는 절**입니다(`07-2`의 모델 상자 하나). 받아 출력한 오류가 없어 빨강은 0장입니다.
- 삽화 `07-5-한-줄로-이어진-작업대-다섯`은 1차 job `d7735964-c264-4072-ab5f-11383b0ccb04`로 바로 채택했습니다(2크레딧, 잔액 2693 → 2691). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이가 없음을 확인했습니다(규격 §5-4).
- 삽화에서 상자 칸이 프롬프트의 여덟이 아니라 **여섯**으로 나왔습니다. 상태의 칸 수와 잇지 않고 「칸이 나뉜 상자」로만 적고, 「그림 읽기」·alt·캡션은 저장한 파일을 보고 「여섯 칸」으로 썼습니다(04절 메모와 같은 사례).
- 옛 `figures/07-흐름.svg`·`.excalidraw`·`.caption.md`는 지우지 않고 `qa/upgrade/before/figures/`에 복사해 두었습니다.

## 4. 실행 환경 메모

- 가상환경 `$ROOT/.cache/vm/venv-ch13-langgraph-basics`에 **07절 패키지를 새로 넣었습니다**(handoff 챕터 공통 항목대로 `bin/python -m pip install`). 넣은 것: `langchain-openai==1.6.1` · `python-dotenv==1.2.3` · `rank-bm25==0.2.2` · `kiwipiepy==0.23.2`. 함께 딸려 온 것: `openai 3.16.2` · `tiktoken 0.14.0` · `numpy 2.5.3` · `jiter 0.17.0` · `regex 2026.9.10` · `kiwipiepy_model 0.23.0` · `tqdm 4.70.1`.
- **잠금과 다른 판 하나**: 실습 폴더 `uv.lock`은 `openai 3.11.0`을 고정하는데 작업 환경에는 `3.16.2`가 들어갔습니다. 마운트 폴더에서는 내림 설치가 막혀 있어 그대로 두었습니다. 노트북 설치 셀은 `openai`를 직접 적지 않고 판 번호도 출력하지 않아 교재 출력에는 나타나지 않습니다. 학생 환경은 `uv sync --locked`로 만들므로 `3.11.0`을 씁니다.
- `sentence-transformers`·`pypdf`·`scikit-learn`은 **설치하지 않았습니다**(이 절이 쓰지 않음). 실습 폴더 `pyproject.toml`·`uv.lock`에는 그대로 남아 있습니다(§5).
- 기기 셸 호출당 180초 제한 때문에 실행과 `--no-exec`을 따로 불렀습니다. 노트북 한 번 실행은 60초 안팎이었습니다.
- 탐색 실행 스크립트는 `/tmp/ch13-07/probe1.py`~`probe3.py`입니다(임베딩 결과를 `/tmp/ch13-07/vectors.json`에 담아 다시 부르지 않았습니다).

## 5. 산출 파일 계약 (규격 §7-2, contracts §3)

- **읽기만 한 파일 둘**: `labs/part3/ch12-retrieval-tuning/data/advanced-documents.json`, `labs/part3/ch12-retrieval-tuning/runs/advanced-continuity-integrated-result.json`. 바이트를 고치지 않았습니다. Ch 9~12 기록과 Ch 6~8 사슬도 열지 않았습니다.
- **이 절은 `runs/`에 쓰지 않습니다.** Part 3 실습 절 넷 선례이고 contracts §3 마지막 줄 권고입니다. 쓰는 쪽이 없으므로 `graph-integrated-result.json`의 바이트도 그대로입니다.
- **읽는 쪽 확인**(2026-09-19, `grep -rln --exclude-dir=.venv "graph-integrated-result" textbook labs`): 코드로 읽는 쪽은 **없습니다**. 나온 자리는 묶음 목록 둘(`textbook/part4/public-files.json`·`textbook/part4/ch13-langgraph-basics/qa/public-files.json`), 문서 넷(`textbook/part4/qa/independent-meaning-review.md`·`language/` 스냅숏 셋), 이 챕터 기록 파일들, 그리고 묶음 zip 둘(`part4-practice.zip`·`llm-practice.zip`)뿐입니다. `textbook/part4/qa/*.py`(`check_delivery.py`·`check_bundle_execution.py`·`check_figures.py`·`check_language_freeze.py`)에는 이 파일 이름이 없습니다.
- **남은 것(챕터 마감 몫)**: `labs/part4/ch13-langgraph-basics/runs/graph-integrated-result.json`은 이제 **개선 전 07절이 남긴 파일**이고 이 절이 다시 만들지 않습니다. 내용도 지금 절과 다릅니다(`reranker: BAAI/bge-reranker-v2-m3`, `duration_ms: 13186.79`, `retrieved`에 `E02-P03-C01`). 학생 묶음 목록 둘이 이 파일을 담고 있어 **그대로 두면 학생이 노트북과 어긋나는 기록을 받습니다**. 마감 때 (a) 삭제 승인을 받아 지우고 묶음 목록 둘에서 빼거나, (b) 08 실습 절이 같은 칸 모양으로 다시 쓰도록 정해야 합니다. 목록 하나(`textbook/part4/public-files.json`)는 챕터 밖 파일이라 이 절에서 고치지 않았습니다.
- **묶음 허용 목록**: 이 절이 읽는 파일이 **줄었습니다**(PDF 여섯 건을 더 읽지 않음). `qa/public-files.json`의 `requires_existing_public_files`에 남은 PDF 여섯 줄은 이제 이 챕터가 쓰지 않는 항목이지만, 다른 챕터가 같은 파일을 쓰고 목록을 줄여도 얻는 것이 없어 그대로 두었습니다. 새로 읽게 된 파일은 없습니다.

## 6. 검토에서 볼 곳

1. b3의 Ch 12 기록 값 네 가지(`Q002`·`['E01']`·문서 청크 세 건·`None`·`matched-chunk-text`)가 노트북 3절 출력과 글자까지 같은지.
2. 리랭커를 뺀 결정과 그 까닭(b7 두 줄)이 Ch 12 요약 §6·contracts §7과 어긋나지 않는지.
3. `07-3`의 노란 상자 두 개가 두 실행의 **출력으로 확인한 값**만 담고 있는지(답 문장 자체는 넣지 않았음).
4. b6 마지막 단락이 결론을 질문 하나·설정 두 벌로 한정하고 있는지.

## 7. 남은 것

- **`runs/graph-integrated-result.json` 처리**(§5 「남은 것」). 챕터 마감에서 사용자 결정이 필요합니다.
- **실습 폴더 `pyproject.toml`·`uv.lock`의 쓰지 않는 패키지 넷**(`numpy`·`pypdf`·`scikit-learn`·`sentence-transformers`). 이 절이 더 이상 부르지 않지만 빼려면 `uv.lock`과 묶음 둘을 다시 만들어야 해 마감 몫으로 미뤘습니다(Ch 12 요약 §12와 같은 사례).
- **실습 폴더 README**(`labs/part4/ch13-langgraph-basics/README.md`)의 07절 단락을 이 절 구성에 맞게 고쳤습니다(PDF 다시 읽기·리랭커·「미화 1달러 미만」 → Ch 12 문서 청크·리랭커 없음·요청 다섯 번·미화 0.01달러 아래). 실습 폴더 README는 학생 묶음에 들어갑니다.
- 별도 세션 검토(규격 §7 사람 검토 네 항목)와 한국어 감사 3단.

## 8. 검토 반영 (2026-09-19, `review-round1.md`)

- **[하] 07-1 삽화 칸 수**: `07-5`의 alt와 「그림 읽기」의 「여섯 칸으로 나뉜 열린 나무 상자」를 「**여러 칸으로** 나뉜 …」으로 고치고, b4 비유 단락에 「상자의 칸 수는 이 절 상태의 칸 수와 맞추지 않았습니다」를 한 줄 더했습니다. 이 절 상태 `RagState`의 칸은 여덟이고 삽화는 2 × 3 = 여섯 칸입니다. **삽화는 다시 만들지 않았습니다**(`.prompt.md` 32행이 이미 같은 사실을 적어 두었습니다).
- **[하] 08-3의 같은 자리**: 노트북 6절 결과 읽기의 「**이 값은** 호출마다 아주 조금씩 달라져 …」를 「**벡터 안의 숫자는** …」으로 고쳤습니다. 바로 앞 값 `문서 청크 벡터 수: 175`는 흔들리지 않습니다. 08절 같은 자리도 함께 고쳤습니다.
- **[하] 챕터 공통 C-4**: `pack.py`로 `review-pack/07-RAG-통합과-시각화.md`를 다시 만들었습니다(08절 작업에서 b8을 고친 뒤 묶음을 다시 만들지 않아 낡아 있었습니다). 이번 마감에서 **여덟 절 묶음을 모두 다시 만들었습니다.**
- **[하] 챕터 공통 C-7**: `qa/public-files.json`에서 노트북 줄만 글로브이고 `runs/graph-integrated-result.json`은 **명시 한 줄**(10행)이라는 사실을 `handoff.md` 「실습 → 챕터 검토」 §4에 바로잡아 적었습니다. `requires_existing_public_files`의 PDF 여섯 줄은 이 챕터가 더 읽지 않지만 이번에도 그대로 두었습니다(까닭은 §7에 적어 둔 그대로).
- **`openai` 판 차이(3.16.2 ↔ 잠금 3.11.0)**: 검토 권고대로 **07·08절을 다시 실행하지 않았습니다.** 학생 묶음(`%pip` 여섯 줄에 `openai` 없음, `langchain-openai==1.6.1`이 요구하는 판을 `3.11.0`이 만족)과 노트북 출력 표기(판을 찍는 셀 여섯 개에 `openai` 없음)에 영향이 없습니다. 기록은 `chapter-summary.md` 「기준 버전」과 `textbook/qa/upgrade-contracts.md` §8에 한 줄씩 남겼습니다.
- 결정 요청 네 건(Ch 12 함수 11개 재정의·요청 5번·`openai` 판·리랭커 제외)은 권고대로 그대로 두었습니다. §6 「검토에서 볼 곳」 네 질문은 검토가 모두 [확인]으로 답했습니다(b3 값 일곱 개가 셀 15 출력과 같음, 리랭커 제외가 contracts §7과 어긋나지 않음, `07-3` 노란 상자 두 개가 출력 값만 담음, b6 마지막 단락이 결론을 한정함).
- `mdpatch.py`로 고쳤고 **노트북은 다시 실행하지 않았습니다**(코드 변경 0건, `code_sha256`·`outputs_sha256` 그대로).
- 반영 뒤 `--label after --strict` 게이트 G1~G7 0, 코드 셀 32, 검사 문장 320.
