# Ch 11→12 및 Ch 12 연결성 수정 전 검토

- 검토일: 2026-09-10
- 범위: `textbook/part3/ch12-retrieval-tuning`, `labs/part3/ch12-retrieval-tuning`, 선수 산출물 `labs/part3/ch09-rag-first-run/notebooks`, `textbook/part3/ch11-evaluation/_src/06-실험-로그와-자동-실행.html`, `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl`
- 수정 전 원본: `textbook/part3/qa/continuity-evidence/before.tar.gz`, `before-manifest.json`

| 연결 구간 | 앞 챕터의 약속 | 다음 챕터의 실제 구현 | 수정 전 근거 | 판정·영향 | 최소 수정 계획 |
| --- | --- | --- | --- | --- | --- |
| Ch 9→Ch 12 01절 | Ch 9 학생용 노트북에서 백터 스토어의 유사도 검색을 실행합니다. | Ch 12 01절이 거리 계산과 정확 검색을 직접 구현합니다. | Ch 12 `_src/01-...html:4`는 Ch 9의 `search()`를 선수 함수로 적지만, 현재 Ch 9 학생 노트북은 `store.similarity_search(...)`를 사용합니다. `search()`는 내부 모듈 `rag.py:92`에만 존재합니다. | 중요도 중. 학생이 자신이 배우지 않은 함수를 찾게 됩니다. | 현재 학생 노트북의 실제 호출인 `InMemoryVectorStore.similarity_search()`와 반환된 `Document` 스키마로 바꿉니다. |
| Ch 11→Ch 12 07~12절 | Ch 11 06절은 같은 평가 파일로 30건 이상의 설정 로그를 축적하고, 입력 지문·질문 분할·질문별 결과를 보존하도록 약속합니다. | Ch 12 `advanced-queries.json`은 Ch 11 `evaluation-queries.jsonl` 30문항과 정규화한 JSON 기준으로 일치하고 dev/test가 15/15로 유지됩니다. 12절은 36개 dev 설정과 1개 test 결과를 계산합니다. | `cmp` 정규화 비교 종료값 0. 그러나 노트북 셀 2는 Ch 12 복제본만 읽고 Ch 11 원본과의 일치를 확인하지 않습니다. 셀 10·12의 로그는 `corpus_sha256`, `query_sha256`, 평균 `metrics`만 저장하고 Ch 11이 약속한 `corpus_fingerprint`, `slices`, 질문별 `results`가 없습니다. | 중요도 높음. 현재 질문은 같지만 복제본이 드리프트해도 실행이 통과하며, 평균이 바뀌 이유를 질문별로 추적할 수 없습니다. | Ch 11 원본과 Ch 12 배포 복제본을 실행 중 비교하고 원본 해시를 기록합니다. 질문별 상위 ID·지표와 분할별 집계를 저장하고, 기존 로그를 덮어쓰지 않는 `continuity` 이름을 사용합니다. |
| Ch 12 01~06절→07~12절 | 전반은 거리·HNSW·필터·BM25·RRF를 작은 입력으로 분리해 관찰합니다. | 후반은 Ch 11의 30문항과 PDF 6건에 리랭킹·부모 반환·MMR·재작성·튜닝을 적용합니다. | `README.md:20`에 12문서·8질문과 PDF 6건·30질문이 적혀 있으나, 07절 본문은 데이터 전환의 이유, ID 단위(`doc_id`→`parent_id`, `chunk_id`, `page`), 전반 수치와 후반 수치를 직접 비교할 수 없는 이유를 한곳에서 안내하지 않습니다. | 중요도 중. 독립 노트북이 실행되어도 수치의 평가 단위가 바뀐 사실을 놓칠 수 있습니다. | 07절의 선수 설명과 README에 전환 이유·필드 대응·비교 한계를 추가합니다. 독립 실행을 위한 Ch 12 복제본은 유지합니다. |
| Ch 12 12절 내부 | 36개 설정으로 선택한 검색 구성을 시험 문항에서 한 번 확인합니다. 또 전체 RAG 처리를 1문항에서 실행합니다. | 36건은 TF-IDF+MMR 검색 설정의 15개 dev 검색 평가이고, 통합 1건은 별도의 dense+BM25+RRF+CrossEncoder+생성 스모크 실행입니다. | `_src/12-...html:5,7,9`, 노트북 셀 13~23, `runs/advanced-integrated-result.json:1-19`. 통합 로그는 `qid`, `gold_doc_ids`, 실행 종류, 평가 범위가 없고, 정리에서 ‘선택한 구성 요소’라고 표현합니다. | 중요도 높음. 검색 평가 36건과 생성 결과 1건을 같은 실험군의 후속 검증으로 잘못 비교할 수 있고, 답변 정확성을 평가했다고 오해할 수 있습니다. | 통합 로그에 `run_type=generation_smoke_test`, `qid`, `gold_doc_ids`, `retrieval_metrics=null`, `generation_evaluation.status=not_evaluated`를 기록합니다. 본문·노트북·README에 설정군·질문 수·평가 단위가 달라 수치를 직접 비교할 수 없고, 생성 평가는 Ch 15의 범위임을 명시합니다. |
| Ch 12→Ch 13·15 | Ch 12는 검색 설정과 RAG 단계를 후속 챕터에 넘깁니다. | 현재 12절은 Ch 13에 ‘이 설정’을 기준선으로 사용한다고만 합니다. | `_src/12-...html:9`. TF-IDF+MMR 선택 설정과 통합 구성이 다른데 어느 산출물을 Ch 13이 받는지 모호하고, 생성 답변 평가를 Ch 15로 넘기는 경계가 없습니다. | 중요도 중. 후속 구현이 잘못된 로그를 기준으로 삼거나 생성 1건을 품질 검증으로 해석할 수 있습니다. | Ch 13에는 통합 처리의 입력·반환 형식과 단계 순서를, Ch 15에는 생성 미평가 상태와 평가 대상 로그를 넘긴다고 구분합니다. |

## 수정 전 확인한 일치 조건

- Ch 11과 Ch 12의 30문항은 `qid`, `tier`, `question`, `type`, `gold_doc_ids`, `answerable`, `split`이 일치하며 dev/test가 각각 15문항입니다.
- `advanced-documents.json`은 부모 6건과 자식 청크 175개를 담고, 자식의 `parent_id`는 부모의 `doc_id`에 대응합니다. `chunk_id` 형식은 `E02-P03-C01`처럼 문서·쪽·청크 위치를 포함합니다.
- 01~06절의 12문서·8질문은 개별 원리를 짧은 셀로 관찰하기 위한 별도 교육용 입력입니다. Ch 11 30문항의 평가 결과와 직접 비교하지 않습니다.

