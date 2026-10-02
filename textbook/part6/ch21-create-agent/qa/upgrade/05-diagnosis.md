# 05절 진단과 개선 기록 — retriever를 도구로 전환 (experiment)

- 대상: `_src/05-retriever를-도구로-전환.html` · `labs/part6/ch21-create-agent/notebooks/05-retriever를-도구로-전환.ipynb` · 도구 파일 `labs/part6/ch21-create-agent/notebooks/runner_tools.py` · 그림 `figures/05-1`~`05-5`.
- 생성기: `qa/upgrade/author_05.py`(노트북 + `_src`, `e4c30c3c…`). 흔들림 확인: `qa/upgrade/05-probe.md` · `probe/probe05.py` · 기록 `probe/probe-{S5,SP}.jsonl`. 그림 설계표: `qa/upgrade/05-figures.md`. 검토 묶음: `qa/upgrade/review-pack/05-retriever를-도구로-전환.md`.
- 작업일 2026-09-25(UTC 04:1x~04:4x). 형식 **experiment 유지**, **슬러그 그대로**(04 생성기 `L_05`가 링크).

## 1. 게이트 전후

| | 코드 셀 | 문장 | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 합 |
|---|---|---|---|---|---|---|---|---|---|---|
| 전 (`gates-before.json`) | 5 | 69 | 4 | 4 | 0 | 0 | 6 | 14 | 3 | **31** |
| 첫 실행 전 (`/tmp/ch21-05/gates-wip-05-05.first.json`, 노트북만 쓴 판) | 26 | — | 0 | 0 | 0 | 0 | 0 | 3 | 18 | — |
| 후 (`gates-wip-05.json`·`gates-wip-05-05.json`) | **26** | **377** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0 (PASS)** |

- 첫 실행 전 G1·G2는 **0**(과제 지시대로 첫 실행 전에 먼저 검사). G6 3 = `_src` 긴 문장 셋(b3 문서 모음 문장·b7 운영 시간 문장·b8 다음 절 문장) → 둘로 나눔. G7 18 = 그림·설계표가 아직 없던 때의 값.
- AST 따로(`/tmp/ch21-05/extra_check.py` — 04 판 그대로, 머리 설명만 05 판): 노트북 **위반 0건**, 도구 파일 2건 = `estimate_cost`의 `.get` 둘(Ch 6 06 원본 예외, 01~04와 같음). 새로 옮긴 다섯 함수는 0건(NumPy 호출 `np.array`·`@`·`np.linalg.norm`·`np.argsort`는 도구 파일에만). 클래스 0, 데코레이터는 맨 `@tool` 하나(매개변수 `query: str`만, 반환 힌트 없음), f-string·내포식·`lambda`·조건 표현식·기본값·튜플 풀기·`elif`·`+=`·`next`·`sum` 0.
- 금지어(`/tmp/ch21-05/ban_check.py` — 04 판 + 「검색기」·「리트리버」·「recall」·「Recall」·「top-k」·「정확도」·「동적」·「검색 인터페이스」·「스키마」): 노트북·`_src`·캡션 넷·`.mmd` 넷 **0건**. 「한 겹 더」 0건. 「retriever」는 제목 말로 노트북 1절·`_src` b2·용어 표에서 「검색 함수」로 풂(아래 §12).
- 코드 줄(`count_code.py`) 35 → **166**(셀 5 → 26). 준비 셀이 아닌 셀의 주석 뺀 코드 최대 **10줄**(`DOC_TEXTS`·`PICK`), 함수 본문 **6줄**(문 넷 — `search_documents`), 셀당 정의 하나, 첫 줄 주석 100%.

## 2. 수정 전 주요 문제 (준비 노트 §2 05, 인계 §04 → §05 2항)

1. **제목의 retriever가 코드에 없음**: 임베딩·벡터 검색 없이 딕셔너리 `DOCS` 셋의 **낱말 겹침**(`k in query or any(w in query for w in v.split())`). 한 글자 낱말 「수」·「도서는」이 질문에 있으면 대출 줄이 걸려 거의 모든 질문에 붙음(옛 출력에 도구 메시지가 없어 확인 안 됨). b4 「리트리버(retriever)는 … 검색 인터페이스」는 코드와 어긋남.
2. **G1 4**: 도구 몸통의 내포식·제너레이터 식 `any`·조건 표현식 · f-string 안 계산 · 반환 힌트 `-> str` · 한 글자 이름 `k`·`v`·`w`·`m` · 도구가 전역 목록 `SEARCH_LOG`를 바꾸는 부작용.
3. **모델 이름 글자** `create_agent("openai:gpt-5.4-mini", …)`(temperature·reasoning_effort 없음) · 규정 글이 01 `POLICIES`와 다름(「14일 동안 5권」·토요일 없음).
4. **모델 선택·모델 글에 `assert`**: `SEARCH_LOG and "3" in 답 글` · `SEARCH_LOG` 비지 않음. 주차 질문의 `['주차 요금', '주차료']` 재검색은 한 번 본 모델 선택.
5. **학습 목표 「재검색 횟수와 답변 범위를 제한」은 시스템 메시지 글의 「한 번」뿐**(코드 제한 없음) · b7 「recall」·「지연」·「절당 1달러 미만」 · 틀 문장(b3·b5·b6·b8) · 결과 읽기 셀 0 · 옛 그림 `{{svg:05-흐름}}` 한 장.
6. **금지어**(옛 판): 「지연」 4 · 「반환」 6 · 「경로」 3 · 「로그」 4 · 「거부」 2 · 「recall」 2 · 「인터페이스」 2 · 「파이프라인」 1 · 「리트리버」·「retriever」 7 · 「Agentic」 5.

## 3. 바꾼 것 (챕터 리드 결정)

- **Ch 9~14에서 배운 검색을 도구로 감쌈**: Ch 14 `labs/part4/ch14-rag-patterns/data/documents.json`(12건)·`queries.json`(8건)을 **읽기만**(자리 찾기 셀은 Ch 14 06절 셀과 글자까지 같음, 파일 읽기·임베딩 셀은 코드 줄이 같고 첫 줄 주석만 다름 — 생성기 `check_same_as_before()`가 Ch 14 06 노트북 셀과 대조). 문서 글은 Ch 12·14의 「제목 + 빈칸 + 본문」, 문서 ID → 글 딕셔너리 `text_by_doc`(Ch 14 01절 모양). 임베딩 `OpenAIEmbeddings(model="text-embedding-3-small", dimensions=256)`(Ch 14 06절 설정 그대로 — 출력 `임베딩 모델 이름: text-embedding-3-small`·`벡터의 숫자 개수 설정: 256`).
- **임베딩 요청 줄이기**: Ch 14 실습 폴더에 **저장된 문서 임베딩 파일이 없음**(`data/`는 JSON 둘, `runs/pattern-comparison.json`은 결과 기록, `labs/part3`·`labs/part4`에 `.npy` 0건 — Ch 10 `.cache/embeddings*`는 다른 문서·설정) → 문서 벡터를 노트북 안에서 `embed_documents` **한 번**(열두 건을 한 요청 — `langchain_openai/embeddings/base.py` 260행 기본 1000건·577~620행)으로 만들고 파일로 쓰지 않음. 노트북 임베딩 요청 **6번**(문서 1 · 질문 글 직접 검색 1 · 같은 검색어 다시 부르기 1 · 도구 안 3)을 준비물·9절 셈(`임베딩 요청 합계: 6`)·b5·b7에.
- **도구 파일에 검색 함수 다섯을 옮김**(§5): `cosine_similarity`·`cosine_distance`·`rank_by_distance`·`print_ranked`·`search_hits`. 노트북은 `search_hits`·`print_ranked`만 직접 부르고 나머지 셋은 `search_hits` 안에서 불림.
- **검색 도구**(06이 그대로 쓸 수 있게 이름·인자·모양을 정함):
  ```python
  @tool
  def search_documents(query: str):
      """교육센터 자료실 안내 문서 열두 건에서 검색어와 가까운 문서 세 건을 찾습니다. query에는 찾을 내용을 짧은 검색어로 넣습니다."""
      hit_list = search_hits(embedding_model, query, doc_vectors, doc_ids, top_count)
      found_text = ""
      for hit in hit_list:
          doc_id = hit["doc_id"]
          found_text = found_text + "[" + doc_id + "] " + text_by_doc[doc_id] + "\n"
      return found_text
  ```
  `top_count = 3`(Ch 14 `top_three`). 도구 메시지 = Ch 14 `build_answer_prompt` 자료 줄과 같은 「[문서 ID] 제목 본문」 세 줄, **거리는 넣지 않음**(끝자리 흔들림이 도구 메시지 글·입력 토큰에 들어가지 않게). 도구 객체는 노트북 전역 `embedding_model`·`doc_vectors`·`doc_ids`·`text_by_doc`·`top_count`에 기댐(01 `POLICIES`와 같은 까닭 — 도구 파일 함수는 인자로만).
- **모델 셀·그래프 모양·용어는 01 그대로**: `key_and_model_cells("openai:gpt-5.4-mini")` 객체 → `create_agent(model, tools=[search_documents], system_prompt=system_text)`. 시스템 메시지 글은 01 글과 **첫 문장이 같고**(생성기 대조) 둘째 문장(도구 이름·근거), 셋째 문장 「찾은 문서에 답이 없으면 검색어를 바꿔 한 번만 더 검색하고, 그래도 없으면 문서에서 찾지 못했다고 답하세요.」를 더함 — **코드 제한이 아닌 글**임을 6절·8절·b4·b6·b7·정리·복습 4에. `print_branches`로 노드·조건 함수가 01과 같음을 출력(6절).
- **「retriever」 풀기**: 과정 요약 §5 Ch 9~12 금지어에 「검색기」가 있어(과제 지시의 「검색기」는 쓸 수 없음) 용어 표 말을 **「검색 함수(retriever)」**로 — 「질문 글을 받아 가까운 문서를 거리 차례로 찾아 내놓는 함수 · 이 절에서는 Ch 14 06절 `search_hits`」. 노트북 1절·`_src` b2 첫 자리에서 「제목의 retriever는 질문을 받아 가까운 문서를 찾아 주는 검색 부분을 가리키는 영어 말」로 풂. `as_retriever()`는 과정 미교육이라 「이번에 실행하지 않았습니다」(b4 비교와 경계). 강사 확인 대상 1.
- **용어 셋**(meta 「새 용어 5」 → 3): 검색 함수(retriever) · 검색 도구 · 검색어(query). 일반 말: 문서 ID 줄·임베딩 요청·다시 검색(Ch 14 06절 말)·자를 개수(`top_count`). meta 시수 「강의 1h | 실습 2h」 그대로.
- **자료 차이 한 문장**(챕터 리드 결정): Ch 14 `FAC-003` 「평일 자료실은 오전 9시부터 오후 9시까지」 ↔ 01~04 `POLICIES` 「평일은 09:00~20:00」 — 노트북 3절 결과 읽기 둘째 단락·`_src` b3·b7에 「서로 다른 자료, 01절 자료를 고치지 않음」. 토요일 닫는 시각은 두 자료 모두 17:00(오후 5시)이라 그 한 줄도 적음.
- **값 바꿔 보기 = 질문 하나**: `C05` 「토요일 자료실 폐관 시각은?」(정답 문서 ID `FAC-003`) → 「자료실 주차 요금은 얼마인가요?」(문서 열두 건에 없음). 거리 검색은 관련 문서가 없어도 가까운 문서 셋을 내놓는다는 점(첫 줄 `FAC-002` 프린터 이용 요금)과 다시 검색이 모델 선택이라는 점을 봄.
- **`assert`는 코드가 정하는 값에만**: 도구 메시지마다 문서 ID 줄 수 `== top_count`(9절 — 도구 몸통이 정함) · 호출 ID 짝(9절 `agent_row`) · 자리 찾기 결과 있음. 검색어·답 글·검색 횟수·같은 검색어 다시 부르기 결과에는 걸지 않음(마지막 것은 임베딩 서비스 값에 기대므로 출력만).
- **같은 검색어 → 같은 문서 차례**: 첫 응답의 도구 호출 요청을 Ch 19 05절처럼 `search_documents.invoke(요청)`으로 다시 보내 `도구 메시지 글과 같은가: True`(7절, A·B 모두) · 노트북 밖 15/15 같은 글.
- **본문 10블록 다시 씀**: 비유 「세탁기」 05(사람이 먼저 붓는 계량컵 ↔ 세탁기에 꽂아 둔 세제 통) · 용어 표 · 그림 넷 + 삽화 · b6 표(두 질문의 메시지 수·응답 수·도구 메시지 수·문서 ID·도구 안 임베딩 요청·입력 토큰) · b7 열한 줄 · 복습 넷 · 참고 자료 여덟 줄(공식 Retrieval 문서 2026-09-25 확인 + 설치판 소스 행 번호). 제작 이력 문장 0. 옛 그림 `figures/05-흐름.*`은 그대로(본문 참조 0).
- **b8 다음 절 문장**: 「06절에서는 같은 평가 질문을 두 흐름으로 보내 견줍니다. 검색을 먼저 하는 흐름과, 검색 도구를 쓰는 에이전트 흐름입니다.」(06 설계를 묶지 않게 제목 뜻 + Ch 29 계약이 요구하는 두 흐름만).

## 4. 흔들림 확인 (규격 §2-7 10번 끝 — `05-probe.md`)

- 규칙을 §0에 먼저 적고(04:18Z) 첫 요청 04:19:01Z. S5(`C05`)·SP(주차) **다섯 번씩**: 두 설정 모두 **5/5 같은 모양** — S5 Human·AI·Tool·AI, `search_documents` 한 번, 도구 메시지 `FAC-003, LIB-002, ACC-004`, 입력 토큰 242·396 · SP Human·AI·Tool·AI·Tool·AI, 응답마다 요청 하나로 **두 응답에 걸쳐 검색 두 번**(`주차 요금` → `주차`), 도구 메시지 `FAC-002, ACC-004, ACC-001` / `FAC-004, ACC-004, FAC-002`, 입력 토큰 243·397·549. 호출 ID 짝 10/10, 같은 검색어 다시 부르기 15/15 같은 글.
- 흔들린 값: SP 5회차 마지막 출력 토큰 51(나머지 21)·답 글 두 문장 · S5 답 글·출력 토큰은 밖 5/5 `43`, 노트북 A·B는 `44`(답 글의 굵은 글씨 자리가 다름) → 출력 토큰·예상 비용·답 글은 결과 읽기 둘째 단락에만.
- 판단: 입력 그대로, 메시지 모양·요청 수·도구 메시지 수·문서 ID를 결론·그림에. 검색어 글은 5번·A·B 모두 같았지만 **모델 글**이라 둘째 단락에만(그림 라벨에 넣지 않음).

## 5. 도구 파일 `notebooks/runner_tools.py`

- **해시 변천**: `6ce7a8d2…`(03절 끝·04절 그대로) → **`8538fedb9943a783183958eb0ef3de619a73762c4735b3576c80681efd911eda`**(05절 끝, 156줄). 바꾼 것: 머리 독스트링 한 줄(「05절부터 쓰는 검색 함수 다섯은 Ch 14 도구 파일 rag_tools.py에서 본문을 글자 그대로 옮겼습니다(벡터 계산은 NumPy — Ch 5 02절).」) + **`import numpy as np`**(import 0 → 1) + 맨 뒤 함수 다섯.
- 옮긴 함수(Ch 14 `rag_tools.py` `868a653e…`와 **def 줄~끝 줄 글자와 AST가 같음** — 옮길 때 스크립트 대조 + 생성기 `check_same_as_before()`가 실행마다 대조): `cosine_similarity`(`# Ch 5 02절에서 배웠습니다`) · `cosine_distance`·`rank_by_distance`(`# Ch 12 01절`) · `print_ranked`(`# Ch 12 05절`) · `search_hits`(`# Ch 14 06절`, 인자 `(embedding_model, question, doc_vectors, doc_ids, top_count)` — Ch 14와 같음). 주석 머리는 이 파일 모양(「Ch N MM절에서 배웠습니다 — Ch 14 도구 파일 rag_tools.py의 같은 이름 함수를 옮겼습니다」 + 설명 줄)으로 다시 적고, 함수 안 주석은 그대로.
- **01~04 영향**: 가져오는 이름이 그대로라 코드·출력 영향 없음(가져오기 줄 넷을 venv에서 import로 확인, 02~04 생성기 `check_same_as_before()` 통과). 다만 **01~04 설치 셀에는 `numpy`가 없는데** 이제 도구 파일을 가져오면 NumPy도 가져옴 — 실습 폴더 `.venv`(잠금 `numpy 2.5.3`, `pyproject.toml` `numpy>=2.0`)에서는 그대로 돌고, 01~04는 다시 실행하지 않음. 챕터 마감 때 01~04 설치 셀에 `"numpy==2.5.3"`를 더할지(코드 바뀜 → 다시 실행) 정할 것(인계).
- 묶음 목록 두 곳은 도구 파일 줄이 이미 있음(01이 올림). `part6-practice.zip` 안 판은 옛 판(마감 몫).

## 6. 새 커널 두 번 (규격 §2-7 9번 끝)

- A `run_section.sh`(셀 실행 기록 04:32:12.47~04:32:21.36Z, 약 9초) · B 사본 `/tmp/ch21-05/B.ipynb`를 `execute.py`로(04:32:39~47Z, `UV_…`·`PYTHONPATH=…/notebooks`). **그림 그리기 전에 두 번 모두 실행**.
- `code_sha256` `d3898188b127…` 둘 다 · **셀별 출력 글자 26/26 같음**(`cmp.py` — 답 글·출력 토큰 `44`·예상 비용 `0.000677`·검색어까지 같음). `execute.py`의 `outputs_sha256`은 A `19cc75e8dabc…` ↔ B `53957a546533…`로 다름 — 설치 셀 출력이 A는 stream 둘, B는 stream 하나로 나뉘어 담긴 차이뿐(글자 같음, 과정 요약 §9 「셀별 출력 글자 해시로 대조」). 교재 출력 = A.
- 설명만 고친 세 번(`mdpatch.py` — 출력 토큰 `43`→`44`·비용 `0.000672`→`0.000677`·준비물 「20초」→「10초」 / 그림 alt 넷 / 「Ch 14」→「Ch 14 06절」 한정·도식 읽기 한 줄)은 `--no-exec`로, 노트북 출력은 A 그대로(대조 26/26).

## 7. 결정적 값과 흔들린 값의 자리

| 값 | 성격 | 둔 자리 |
|---|---|---|
| 명세의 인자 `['query']` · 노드·조건 함수(01과 같음) · 문서·질문 수 · 설정 256 | 코드·자료 | 첫 단락·결론·그림 |
| 메시지 수 `4`·`6` · 응답마다 요청 수 `1`·`1`·`0` · 모델 요청 `2`·`3` · 도구 메시지 `1`·`2` · 문서 ID(두 흐름 모두) · 입력 토큰 `638`·`1189` | 모델 선택이지만 밖 5/5·A·B 같음 | 첫 단락·b6 표·그림(흔들림 가능성은 b7·결과 읽기에 조건으로) |
| 도구 메시지마다 문서 셋 · 호출 ID 짝 · 도구 메시지 수 = 도구 안 임베딩 요청 수 | 코드 | `assert`·결론·그림 공통 회색 상자 |
| 같은 검색어 다시 부르기 `True` | 임베딩 값(밖 15/15·A·B 같음) | 첫 단락·결론, `assert` 없음 |
| 검색어 글 · 답 글 · 출력 토큰 `44`·`59` · 예상 비용 `0.000677`·`0.001157` · 직접 검색 셋째 자리 `FAC-004`·거리 `0.72` | 모델 글·흔들림 | 결과 읽기 둘째 단락만(그림·정리·복습에 없음) |

## 8. 그림

- Mermaid **4장**(`05-1` flowchart TB 한 줄 여섯 상자 270.5 · `05-2` flowchart TB + subgraph 둘(위아래) 309.8 · `05-3` sequenceDiagram 세로선 넷·`box Lavender` 둘 825(첫 판 1065.5 → 참여자 라벨 줄이고 `actorMargin: 30`·메모 줄 나눔 → 885 → 825) · `05-4` flowchart TB + subgraph 둘 + 공통 상자 594.1, 모두 868 이하), **빨강 0**, 보라는 실제로 부른 모델 둘(임베딩 모델 상자·sequenceDiagram 띠 둘, 05-2 모델이 고르는 자리). PNG 넷을 직접 열어 봄(`.cache/ch21-05-view/`) — 저절로 꺾인 라벨(05-1 「요청 한 / 번」·05-4 맨 위 상자)·넘친 메모(05-3 끝 메모)를 `<br>`로 미리 나눠 다시 렌더. 조건 함수는 상자로 그리지 않고 05-3 화살표 라벨로만. 검색어 글자는 그림에 넣지 않음.
- 삽화 **1장** `05-5-세제-통을-꽂아-둔-세탁기`(비유 계열 **「세탁기」** 05 — 인계 후보 「투입구」를 관·서랍 금지 때문에 **꽂아 둔 통**으로) — **1차 job `93792124-8b54-4597-b916-7feef71a54d3` 채택**, 재생성 0, **2크레딧**(거래 **2026-09-25T04:35:43Z** 「Nano Banana Pro −2」, 생성 전 잔액 2455.75, 바로 앞 거래 04:00:15Z는 04절 몫). 응답 모델 이름 표시 `nano_banana_2`(01~04와 같음). 원본 `845224ee…`(2752 × 1536) → 저장 `e80b5eee…`(1100 × 614), 픽셀 대조 bbox `None`·최대 차이 0. 벽이 옅은 베이지, 버튼이 윗면이 아니라 앞면 위쪽 띠 오른쪽, 앞면 위쪽 띠 왼쪽에 서랍처럼 보이는 네모 칸(프롬프트 「no drawers」와 다름) — 관계와 무관해 채택, 그림 읽기에 버튼은 「둥근 버튼 하나」로만 적고 네모 칸은 짝짓지 않음(`.prompt.md` 상태).

## 9. 서비스 요청과 비용

| 구분 | 모델(`gpt-5.4-mini`) | 임베딩(`text-embedding-3-small`) |
|---|---|---|
| 노트북 밖 확인(S5·SP 다섯 번씩) | 25 | 34(문서 2 · 질문 글 2 · 도구 안 15 · 다시 부르기 15) |
| 새 커널 A | 5 | 6 |
| 새 커널 B | 5 | 6 |
| **합** | **35** | **46** |

- 요금표(2026-09-17, 100만 토큰당 mini 0.75·0.075·4.50 · 임베딩 0.02)로 어림한 **예상 비용 약 0.013달러**(모델 몫 약 0.0130 — 밖 0.0093 · A 0.0018 · B 0.0018, 임베딩 몫 약 0.00006 — 문서 요청 한 번 640토큰 × 4 + 검색어 약 405토큰을 `cl100k_base`로 센 어림). 청구 금액 아님. 노트북 한 번은 모델 몫 `0.000677 + 0.001157 = 0.001834`달러.
- 삽화 2크레딧(거래 04:35:43Z). 참고 자료 확인 WebFetch 1번(LangChain Retrieval — 「the retrieval step is always executed before the generation step」 ↔ Agentic RAG 「decides when and how to retrieve」, LLM 요청 수 「known and capped」 ↔ 가변). 걸린 시간은 재지 않음(준비물 「10초 안에」는 셀 실행 기록 A).

## 10. 챕터 밖 수정

| 파일 | 무엇을 |
|---|---|
| `textbook/_notebook/checks/notebook-contracts-part6-ch21-create-agent.json` | `verify.py --chapter`가 다시 씀(`8bd08465…` → `cb9db81faf515372d429a65aba09fbfa459e0416e7343a64d9a29c4404dbd427`) |

- 챕터 안(실습 폴더 포함): `labs/…/notebooks/05-*.ipynb`(새 판, `4c2eac65…`) · **도구 파일 `runner_tools.py`**(§5) · `_src/05-*.html`(`7736c51a…`) · 빌드 HTML `05-*.html`(`afcb826c…`, `{{` 0건)·목차·이웃 절 HTML(빌드) · `figures/05-1`~`05-5` 새 파일(`.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`·`.prompt.md`) · `qa/upgrade/` 새 파일(`author_05.py`·`05-probe.md`·`probe/probe05.py`·`probe/probe-S5.jsonl`·`probe/probe-SP.jsonl`·`05-figures.md`·`05-diagnosis.md`·`gates-wip-05*.json`·`review-pack/05-*.md`) · `handoff.md`·`manifest-changes.md`·`집필점검표.md`·`qa/verification.md` 05 행.
- **고치지 않은 것**: Ch 14 자료·도구 파일(읽기·가져오기만, 해시 그대로 — 노트북 밖 확인은 `sys.dont_write_bytecode`로 바이트 코드도 쓰지 않음, `__pycache__` 시각 그대로) · 실습 폴더 `pyproject.toml`·`uv.lock`·README·`data/rag-comparison.json` · 01~04 파일(노트북·`_src`·생성기) · `chapter.json` · `textbook/part6/index.html`(마감 몫) · Ch 22·Ch 29·Ch 30 파일 · 공용 도구·게이트·`verify.py` · 옛 그림.
- **파일 삭제 0건**.

## 11. 뒤 챕터가 Ch 21·retriever에 기대는 문장 (고치지 않음, 참·거짓만)

`grep -rn 'Ch *21\|retriever' textbook/part6/*/_src textbook/part7`(Ch 21 자신 제외).

| 자리 | 문장 | 판정 |
|---|---|---|
| Part 6·7 `_src` 전부 | 「retriever」 0건 · Ch 21 05절을 가리키는 문장 0건 | 기댈 문장 없음 |
| Ch 22 01 `_src` 4·9행 | 「Ch21에서는 create_agent() 함수로 에이전트를 만들었습니다」·「Ch21 01절에서 … 모델을 부르고, 모델이 요청하면 도구를 실행하고, 다시 모델을 부릅니다」 | 참(05도 같은 흐름 — `C05` 질문 모델 → 도구 → 모델) |
| Ch 27 01·02 `_src` 4행 | 「Ch 21의 create_agent는 모델과 도구의 반복을 만들었습니다」·「Ch 21에서 create_agent에 도구를 전달했습니다」 | 참(05 `tools=[search_documents]`) |
| Ch 29 01 `_src` 4행 | 「Ch11 평가셋과 Ch21 에이전트를 사용합니다」 | 느슨함(Ch 29 01 노트북은 Ch 21 파일을 읽지 않음, 05 검색 도구는 Ch 14 문서 모음 — Ch 29 몫) |
| Ch 29 04 `_src`·노트북 c12~c18 | `rag-comparison.json` 3줄·519.7토큰·1.880초·p95 2.094초 | 05는 파일을 쓰지 않아 **지금 참**(현재 파일 `122cfce2…`에서 평균 토큰 519.7·걸린 초 1.88·p95 2.094·토큰 p95 541을 다시 셈) — 06이 다시 쓰면 바뀜(인계) |
| Ch 30 01·02·03·09 `_src`·`_generate.py` | 「Ch21에서 Agent 실행 객체를 만들었습니다」·「init_chat_model과 create_agent로 도구 호출 Agent」·「상태 사전」 | 참(05도 모델 객체 + `create_agent`). 「사전」은 Ch 30 몫 |

## 12. 강사 확인 대상

1. **「retriever」 풀이 말** — 과제 지시는 과정 말 「검색기」로 풀라고 했으나 과정 요약 §5·Ch 12 요약이 「검색기」를 금지어로 둠 → 「검색 함수(retriever)」로 풂. 제목의 「retriever」는 그대로(04 「마이그레이션」과 같은 처리).
2. 시스템 메시지 글에 다시 검색 규칙(「한 번만 더」)을 적어 모델 선택을 보인 설계 — 코드 제한이 아님을 본문 여섯 자리에 적음. 코드로 막는 방법(미들웨어)은 Ch 22 04절 몫.
3. 코드 줄 35 → 166(셀 5 → 26) — 규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」와 견줘. 늘어난 몫은 Ch 14 자료 준비(자리 찾기·읽기·글 잇기·질문 고르기·임베딩 — Ch 14 06과 같은 코드), 검색 함수 직접 부르기, 도구 명세·그래프 모양 확인, 두 질문 실행과 셈(문서 줄·기록·임베딩 요청·사용량·비용).
4. 01~04 설치 셀에 `numpy`가 없는데 도구 파일이 NumPy를 가져옴(§5) — 마감 때 설치 셀에 더할지.

## 13. 남은 것 · 지워야 하지만 지우지 않은 것

- 마감 몫: 01~04 설치 셀 `numpy` 여부 · `part6-practice.zip` 재생성(도구 파일 새 판) · 옛 그림 `05-흐름.{svg,excalidraw,caption.md}` 삭제 승인 · `chapter.json` `objectives`·Part 목차.
- 삭제 승인 대상(만들었지만 지우지 않음): 기기 `/tmp/ch21-05/`(`probe-S5.jsonl`·`probe-SP.jsonl`(사본은 `probe/`에)·`A.ipynb`·`B.ipynb`·`cmp.py`·`resize.py`·`pixcmp.py`·`illu-1-orig.png` 4.0MB·`illu-1-1100.png`·`extra_check.py`·`ban_check.py`·`reps1.json`~`reps3.json`·`runner_tools.before.py`·`gates-wip-05-05.first.json`) · `.cache/ch21-05-view/`(그림 확인 사본 다섯) · `labs/…/notebooks/__pycache__/`·`qa/upgrade/__pycache__/`(있으면) · `qa/upgrade/gates-wip-05*.json` · `qa/upgrade/gates-wip-ch21-after05.json`(챕터 전체 확인 — 01~05 PASS, 06은 아직 63: G1 26 · G4 1 · G5 13 · G6 20 · G7 3).

## 마감 반영 (2026-09-25, 챕터 마감 담당)

검토 1차(`review-round1-A.md`·`review-round1-B.md`) 반영과 챕터 마감에서 이 절에 한 일입니다. 전체 기록은 `chapter-summary.md`, 절 사이 기록은 `handoff.md` 「검토 반영과 챕터 마감 (2026-09-25)」입니다.

- **다시 실행하지 않음**(마크다운·그림만 — `code_sha256` `d3898188…`·`outputs_sha256` `19cc75e8…` 전후 같음, 노트북 파일 `4c2eac65…` → `6598d4f0…`).
- **B-1(05 쪽)**: 1절 「벡터 계산에 쓰는 NumPy가 01~04절보다 하나 더 들어갑니다」 → 「01~04절처럼 numpy도 함께 설치합니다 · 이 절부터는 도구 파일의 거리 계산 함수가 NumPy로 벡터를 계산합니다」(01~04 설치 셀에 `numpy`를 더해 사실이 바뀜).
- **A-13 색**: `05-1` `mk["create_agent …"]`의 `:::flow`를 빼 회색(라이브러리가 준 함수 — 01-1·07-1과 같음) → `--force` 렌더, 노트북 첨부 PNG 새 판, alt(「회색 상자 create_agent …」)·도식 읽기(「파란 상자 둘은 우리가 적은 코드로 … 회색 상자 둘은 라이브러리가 준 함수 create_agent와, 그 함수가 만든 그래프입니다」) 같게, PNG 확인.
- **B-5**: b6 「두 번째 검색은 … 「한 번만 더 검색」을 모델이 따른 결과입니다」 → 「… 「한 번만 더 검색」과 맞았습니다 · 규칙 문장을 뺀 실행은 하지 않아, 규칙 때문인지는 확인하지 않았습니다」.
- **A-15(기록만 — 코드 그대로)**: 도구 파일로 옮기며 줄이거나 다시 쓴 주석 — `cosine_distance`는 Ch 14 판 둘째 주석 줄 「Ch 12 01절 판은 바깥 이름 similarity_top을 읽었고, 이 판은 같은 값 1을 함수 안에서 정합니다」를 옮기지 않음(Ch 12 판 차이 설명이라 이 파일에서는 필요가 적음) · `search_hits`는 Ch 14 주석 두 줄(「06절에서 배웠습니다 — …」·「06절 판은 바깥 이름 embedding_model·doc_vectors·doc_ids·top_all을 읽었고 …」)을 「Ch 14 06절에서 배웠습니다 — Ch 14 도구 파일 … 옮겼습니다」 + 뜻 한 줄 + 「Ch 14 06절 노트북 판은 바깥 이름을 읽었고, 이 판은 임베딩 모델·문서 벡터·문서 ID·자를 개수를 인자로 받습니다」로 다시 씀. 위 §5 「주석 머리는 이 파일 모양으로 다시 적고」의 자세한 내용(규격 §4 2026-09-20).
- 위 §12-4·§13 「01~04 설치 셀 `numpy`」는 마감에서 더하고 다시 실행해 끝남. 게이트 0(검사 문장 379).
