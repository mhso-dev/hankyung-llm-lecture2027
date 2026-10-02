# Ch 13 초기 기술 정독

## 검토 범위와 상태

- 검토일: 2026-09-10 (KST)
- 대상: `_src/01`~`07`과 대응 노트북 `01`~`07`의 정적 대조입니다. 소스와 노트북의 파일 시스템 수정 시각은 모두 `2026-09-10 09:15:19 +0900`입니다. 이 시각은 집필 초안의 저장 시각이며 실행 검증 완료를 뜻하지 않습니다.
- 모든 노트북 코드 셀은 `execution_count: null`, `outputs: []`입니다. 따라서 StateGraph, reducer, Send, Command와 RAG 실행 결과는 아직 미확인입니다. 아래의 그래프·코드 문제는 정적 근거로 판정했고, 출력이 필요한 주장은 최종 실행 뒤 다시 확인해야 합니다.
- 범위 적합성: 7개 절이 StateGraph/노드·엣지, 상태 갱신과 reducer, 조건부 엣지, `add_messages`, `Send`, `Command`, 실제 Ch12 문서 기반 RAG 연결을 순서대로 다룹니다. `create_agent`, `ToolNode` 또는 LLM 기반 라우팅을 조기 도입하지 않았습니다. `StateGraph`, `add_messages`, `Send`, `Command`의 공식 API 범위는 [LangGraph Graph API](https://langchain-ai.github.io/langgraph/reference/graphs/), [Send API](https://langchain-ai.github.io/langgraph/reference/types/#send), [Command API](https://langchain-ai.github.io/langgraph/reference/types/#command)를 기준으로 확인했습니다.

## 발견 사항

### T1 — 높음: `load_input`이 그래프 노드·Mermaid·trace에 나타난다는 설명이 실제 선언과 다릅니다

**근거**

- `07-RAG-통합과-시각화.ipynb` 71행 부근에서 Ch12 JSON을 그래프 바깥에서 읽습니다.
- 같은 노트북 185~189행은 `search`, `fuse`, `rerank`, `generate` 네 노드만 등록하고, 입력 `trace`에 `['load_input']`을 미리 넣습니다.
- Mermaid 검증도 212~215행에서 같은 네 노드만 검사합니다.
- 반면 `_src/07-RAG-통합과-시각화.html` 5·7행은 `load_input`을 노드로 정의하고 trace와 Mermaid에 다섯 단계가 모두 나타난다고 설명합니다.

**영향**

학생이 상태 문자열을 미리 넣는 것과 LangGraph 노드 실행을 같은 것으로 배웁니다. 정적 도식·Mermaid·실행 흔적의 대조라는 이 절의 핵심 증거도 성립하지 않습니다.

**수정**

둘 중 하나로 통일합니다.

1. `load_input`을 실제 노드로 추가하고 `START → load_input → search`로 연결합니다. 노드는 파일 경로 또는 로드할 입력을 받고 Ch12 질문·문서를 상태에 반환해야 합니다.
2. 파일 읽기를 그래프 전처리로 유지한다면, 본문·도식·trace에서 `load_input`을 제거합니다. 초기 trace를 임의로 채우지 말고 실제 노드가 추가한 흔적만 출력합니다.

**재확인**

빈 커널 실행 뒤 노드 등록 목록, Mermaid 노드, `trace`가 같은 순서와 같은 이름을 나타내는지 확인합니다.

### T2 — 높음: 답변의 출처 표기를 프롬프트로만 요청하고 검사하지 않습니다

**근거**

- `07-RAG-통합과-시각화.ipynb` 179~192행은 모델에게 문장 끝 출처를 요청하지만 `result['answer']`의 비어 있지 않음과 trace 마지막 값만 단언합니다.
- `_src/07-RAG-통합과-시각화.html` 7~8행은 `[E01 p.3]` 출처 전달과 “근거 본문과 출처 전달 여부를 별도로 검사”한다고 설명합니다.

**영향**

모델이 출처를 누락하거나 선택하지 않은 문서의 출처를 만들어도 실행이 성공합니다. “별도 검사”라는 교재 주장을 코드와 출력으로 뒷받침하지 못합니다.

**수정**

`selected`에서 허용 출처 집합 `(parent_id, page)`을 만들고, 답변에서 추출한 출처가 그 집합에 하나 이상 있는지 검사합니다. 선택 결과가 바뀔 수 있으므로 `[E01 p.3]` 문자열을 고정 성공 조건으로 두지 않습니다. 검사 결과를 상태 또는 출력에 별도 항목으로 남깁니다.

**재확인**

정상 답변·출처 없는 답변·선택 밖 출처 답변을 각각 입력해 정상만 통과하는지 확인합니다. 실제 API 호출 노트북에서는 검증 함수를 분리해 로컬 문자열로도 세 경우를 재현합니다.

### T3 — 중간: 문자 n-gram TF-IDF 순위를 `dense`라고 이름 붙였습니다

**근거**

- `07-RAG-통합과-시각화.ipynb` 108~112행은 `TfidfVectorizer(analyzer='char')`의 점수와 순위를 `dense`, `dense_rank`로 저장합니다.
- `_src/07-RAG-통합과-시각화.html` 8행도 이를 “로컬 dense 기준선”이라고 부릅니다.

**영향**

TF-IDF 문자 n-gram은 희소 어휘 표현입니다. Ch12의 임베딩 기반 dense retrieval과 구별하려는 문장이 오히려 용어를 혼동시킵니다.

**수정 및 재확인**

`tfidf_rank`와 `overlap_rank`처럼 방법을 드러내는 이름으로 상태·출력·본문을 함께 바꾸고, Ch12 임베딩 검색과 점수·표현이 다르다는 설명을 유지합니다. 빈 커널 실행 후 상태 키와 출력 이름을 본문과 대조합니다.

### T4 — 중간: `add_messages`의 직접 reducer 호출을 두 번째 그래프 실행으로 설명합니다

**근거**

- `04-add_messages-리듀서.ipynb` 143~150행은 `add_messages(first['messages'], ...)`를 직접 호출합니다.
- `_src/04-add_messages-리듀서.html` 7행은 “두 번째 그래프 실행에 같은 ID의 수정 메시지를 입력”했다고 설명합니다.

**영향**

리듀서 함수의 동작을 보여 주는 예제는 유효하지만, 그래프 재실행이나 `update_state` 동작을 검증한 예제는 아닙니다.

**수정 및 재확인**

현재 코드를 유지한다면 본문을 “리듀서를 직접 호출”로 고칩니다. 그래프 수준 갱신을 가르치려면 실제 그래프 API를 사용한 별도 셀과 출력을 제공합니다. 수정한 주장에 대응하는 출력의 메시지 수·ID 교체 결과를 확인합니다.

## 최종 실행 뒤 확인할 항목

- 7개 노트북 모두의 실제 출력, 설치 버전, Mermaid, `Send` fan-out 결과와 `Command` 분기 결과를 기록해야 합니다.
- 07번은 `OPENAI_API_KEY`가 필요한 실제 모델 호출이므로, 키 유무와 호출 시각·모델명은 출력에 남기되 키 값은 출력하지 않습니다.
- 출력 확보 전에는 `_src/04`, `_src/07`의 “LangGraph 1.2.11에서 얻은 결과”, “실제 출력과 ... 확인했습니다” 같은 완료형 결과 주장을 확정하면 안 됩니다.

## 2026-09-10 재검

- 04와 05의 저장 출력, 07의 실제 API 실행 출력, 그리고 `runs/graph-integrated-result.json`을 재확인했습니다.
- **T2 출처 검증: 확인됨.** 07은 선택 문서에 E01 3쪽이 있는지와 답변에 `[E01 p.3]`이 있는지 함께 단언합니다. 저장 결과에는 E01-P03-C01·E02-P03-C01, 새 답변, 1,230 total tokens, 13,186.79ms가 있습니다. 이는 Q002 고정 통합 실행의 검사이며 일반적인 답변 사실성 평가가 아닙니다.
- **T3 dense/sparse 용어: 확인됨.** dense node는 `text-embedding-3-small` 256차원 OpenAI 임베딩 코사인 유사도, sparse node는 Kiwi 토큰 기반 BM25를 계산합니다. RRF는 두 순위를 합치고 CrossEncoder가 후보 열 건을 재정렬합니다.
- **T4 add_messages: 확인됨.** 04 본문은 두 번째 그래프 실행이라고 말하지 않고 리듀서를 직접 호출한다고 설명합니다. 실행 출력은 h1 교체 뒤 message 두 건이 유지됨을 보입니다.
- **Send 동적 길이: 확인됨.** 05는 문서 세 건에서 results 세 건, 문서 한 건에서 results 한 건을 출력하고 단언합니다. `documents`와 `results`는 dict 목록 상태로 전달됩니다.

### T5 — 높음: 07 본문은 이전 노드 이름을 아직 trace·Mermaid 결과로 설명합니다

**근거**

- 실제 07 그래프와 저장 run의 node trace는 `load_pages → dense_search → sparse_search → fuse → rerank → generate`입니다.
- `_src/07-RAG-통합과-시각화.html`의 실험 결과 해석은 `load_input, search, fuse, rerank, generate`가 trace·Mermaid에 나타난다고 남아 있습니다.

**영향 및 수정**

실제 그래프와 설명이 다시 어긋납니다. 6절의 노드 목록을 실제 여섯 노드 이름과 순서로 바꾸고 Mermaid 출력과 대조합니다.

## 2026-09-10 최종 원고 대조

- 07 원고의 수정 시각은 09:48:00이며, 6절은 실행 trace와 같은 `load_pages → dense_search → sparse_search → fuse → rerank → generate`를 명시합니다. `runs/graph-integrated-result.json`의 node trace 및 노트북의 Mermaid 그래프와 순서가 같습니다.
- **T5: 해결 확인.** 이전 `load_input, search` 표기는 해당 실험 결과 설명에서 제거됐습니다. 앞부분의 `search, fuse, rerank, generate`는 검색·결합·재정렬·생성의 일반 단계를 설명하는 문장으로 남아 있으나 trace나 Mermaid의 실제 노드명이라고 주장하지 않습니다.
- 이 판정은 07의 노드 설명·저장 실행 결과·출처 assertion의 기술 일치 범위입니다. 도식의 시각 표현과 교재 문체는 별도 검토 범위입니다.
