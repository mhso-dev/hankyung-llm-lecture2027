# Part 3 개념 학습 순서 개정 기록

- 담당 범위: Part 3 Ch 9~12, 교재 원본 32절과 대응 노트북 32개
- 개정 기준: 핵심 개념의 필요 이유, 호출 표기, 입력·처리·반환, 실제 실행 시점을 첫 코드 전에 설명하고 다른 상황과 가까운 개념의 경계를 연결함
- 코드 변경: 없음. 기존 32개 노트북의 코드 셀·출력·실행 번호를 개정 전 스냅숏과 비교해 모두 동일함
- 생성기: Ch 11 `_make_notebooks.py`의 공통 도입부를 절별 설명과 동기화함. 임시 폴더 생성 결과와 현재 노트북의 셀 종류·소스를 6개 모두 대조함

## 절별 근거

| 절 | 첫 사용 설명 보정 | 다른 상황·비교와 결과 해석 |
| --- | --- | --- |
| 09-01 | `PdfReader` → `Document` → 스플리터 → `similarity_search()` → `invoke()`의 입력·반환과 색인/질문 실행 시점을 코드 앞에 배치 | 점수 없는 `Document` 목록 반환과 질문만 바뀌는 경우의 재실행 범위를 구분 |
| 09-02 | `pages[1]`, `extract_text()`, `split_documents()`의 표기와 반환 타입 설명 | 문자열만 나누는 `split_text()`와 메타데이터를 보존하는 Document 분할 비교, 조항 ID 사례 |
| 09-03 | 임베딩 객체 생성과 `add_documents()`의 실제 API 호출 시점, `InMemoryVectorStore`의 `(Document, 코사인 유사도)` 반환 설명 | 유사도는 클수록 가깝지만 확률이 아니라는 경계, 제품 코드 질문의 sparse 검색 연결 |
| 09-04 | 검색 Document를 문맥 문자열로 바꾼 뒤 `invoke()`하는 과정과 `AIMessage.text` 설명 | 출처 입력·출처 표시·주장 근거 검증을 세 단계로 구분 |
| 09-05 | 후보 누락과 생성 실패를 검색된 문서 ID로 구분 | `k=1`/`k=2` 비교가 적용되는 원인과 정답 문서가 이미 검색된 경우의 조사 경계 설명 |
| 09-06 | YAML 읽기부터 색인·검색·생성·`record` 조립·JSONL 쓰기까지 셀별 실행 순서 설명 | 하나의 가상 진입 함수나 반환 사전을 주장하지 않고 한 조건 변경과 로그 성공의 경계를 구분 |
| 10-01 | `Path` 속성과 메서드 표기, 현재 노트북은 출처 사전까지만 만들고 LangChain `Document`는 다음 단계라는 범위 설명 | 개정판 규정의 문서 ID·시행일 메타데이터 사례 |
| 10-02 | `PdfReader`, `extract_text()`, `selected.extract_tables()`의 표→행→셀 중첩 반환 구조 설명 | 디지털 PDF 텍스트 추출과 스캔 PDF OCR의 경계, 촬영 영수증 사례 |
| 10-03 | DOCX 문단, `find_all(["h1", "p"])`의 HTML 태그 목록, CSV 행 사전의 서로 다른 반환 구조 설명 | 형식별 구조를 한 문자열로 합치기 전에 보존할 관계를 결정 |
| 10-04 | ZIP 검사, `with ZipFile`, XML 파싱과 네임스페이스 설명 | HWPX 최소 표식 성공과 레거시 HWP·실제 문서 호환성의 경계 |
| 10-05 | 스플리터 생성과 `split_text()` 실행 시점, 목표 길이와 실제 길이 설명 | 문자·재귀·토큰 청킹의 경계와 문단 구조/입력 한도 상황 비교 |
| 10-06 | Markdown 제목 규칙과 SemanticChunker의 임베딩 호출 시점 설명 | 구조가 분명한 매뉴얼과 제목 없는 인터뷰 기록 비교 |
| 10-07 | `embed_documents()`의 입력 순서·반환 벡터, 캐시 래퍼의 조회 순서 설명 | 캐시 파일 수와 API 호출 횟수의 경계, 모델·차원별 네임스페이스 사례 |
| 10-08 | 짧은 문자열의 `split_text(text)`와 PDF `Document` 목록의 `split_documents(pages)`를 구분 | 3개 청킹 × 2개 임베딩에서 청크 수·시간과 검색 품질의 경계를 구분 |
| 11-01 | JSONL 한 행, `gold_doc_ids`, 페이지 후보와 고유 `doc_id`, dev/test 라벨 설명 | `search()`가 문서별 최고 점수 페이지 하나를 남기는 실제 기준선 설명 |
| 11-02 | `search()`의 중복 제거와 `recall_at()`의 상위 k·정답 비교 책임을 분리 | 6위가 Recall@5와 @50에서 달라지는 경계, 후보와 첫 화면 평가 비교 |
| 11-03 | `search()`가 만든 고유 문서 순위와 `precision_at()`의 고정 분모 k를 분리 | 단일 정답과 여러 정답 평가셋의 최댓값 차이, Precision@1 비교 |
| 11-04 | 관련도 배열 → DCG → IDCG → nDCG의 계산 흐름 설명 | 이진 관련도와 등급 관련도 정책의 차이, `assert`와 검색 품질의 경계 |
| 11-05 | 슬라이스 집계 입력과 오류 라벨의 의미 설명 | 조건별 평균과 원인 추론의 경계, 복합 원인에서 원문 확인 필요성 |
| 11-06 | 노트북의 `subprocess.run()`, `evaluate.py`의 `Path.write_text(json.dumps(...))`, 노트북의 `read_text()`·`json.loads()` 책임 설명 | 파일 읽기·스키마 통과·지표 개선 구분, 말뭉치 지문과 지표 정책 비교 조건 |
| 12-01 | 코사인 유사도와 L2 거리의 방향, 정확 검색의 모든 문서 비교 설명 | 정규화 벡터와 일반 벡터의 순위 경계, 코드 문자열 sparse 검색 연결 |
| 12-02 | pgvector 거리 SQL, 정확 검색과 HNSW 경로, `ef_search` 설명 | 작은 자료의 동일 순위와 일반 재현율 보장의 경계, 정확 검색 기준선 비교 |
| 12-03 | 근사 후보 뒤 필터가 적용되는 순서와 결과 부족 원인 설명 | strict/relaxed iterative scan과 탐색 한도·반환 개수 기록 비교 |
| 12-04 | Kiwi 토큰 객체, `Token.form`, BM25 통계 준비와 점수 반환 설명 | 형태소 검색 토큰과 모델 입력 토큰 구분, ISBN과 의미 변형 질문 비교 |
| 12-05 | dense 연속 벡터와 sparse 형태소 표현의 입력·점수 차이 설명 | 의미 변형과 정확 표기 사례, 8개 질문의 관찰을 일반 우열로 확대하지 않음 |
| 12-06 | 서로 다른 원점수 대신 순위 항을 더하는 RRF 입력·반환 설명 | 양쪽 상위/한쪽 전용 문서 비교, sparse 가중치와 BM25 원점수의 경계 |
| 12-07 | `CrossEncoder.predict()`의 질문-후보 쌍 입력과 로짓 반환 설명 | 후보 2개에도 E01이 있어 누락은 실증하지 않았음을 명시하고, 입력 후보 밖 문서를 점수화하지 않는 구조적 경계로 한정 |
| 12-08 | 공통 후보 점수 저장 뒤 5·10·20 범위를 자르는 비교 설명 | 실제 6행의 Recall·nDCG가 모두 1.000으로 포화됨을 명시하고, 후보 범위와 모델 순위 효과가 드러나는 가상 수계산을 별도 제시 |
| 12-09 | 자식 청크 검색과 `parent_id` 부모 반환·중복 제거 설명 | `child_k`와 부모 수가 비례하지 않는 사례, 넓은 부모 문맥의 한계 |
| 12-10 | MMR의 관련성 항·중복 억제 항·λ·반환 인덱스 설명 | 여러 관점 질문과 단일 정확 조항 질문 비교, 다양성과 정답 관련성의 경계 |
| 12-11 | 대화 기록+후속 질문 입력, `invoke()` 재작성 반환, 검색 실행 연결 설명 | 조건 삭제·추가 위험과 원문/재작성문 RRF 보존, 이미 독립적인 질문 비교 |
| 12-12 | 36개 개발 설정 평가·선택과 시험 질문의 1회 최종 확인, 실제 저장 필드 설명 | 로그에 없는 가설 필드를 제거하고 TF-IDF 평가와 별도 통합 RAG 스모크의 단위를 구분 |

## 독립 검토 보정 라운드

- `review-part3.md`의 필수 6묶음과 국소 18건을 실제 코드·저장 출력에 맞춰 교재 원본과 노트북에 반영함.
- Ch12 07~12의 반복된 도서관 비유·공통 실행 안내·비용 문장을 절별 관찰로 교체함: 07은 후보 누락 미관찰, 08은 6행 지표 포화, 09는 자식 3·8·20과 부모 2·2·3, 10은 관련성 0 선택, 11은 E01 순위 개선 미관찰, 12는 dev/test 격리와 실제 로그 필드에 초점을 둠.
- Ch11 생성기의 절별 설명과 노트북을 함께 수정하고 임시 생성본 6개와 현재 노트북의 셀 종류·소스를 다시 대조함.

## 참고 노트북과 공식 근거

- 참고 노트북: `02_langchain-basics/06_RAG/6-7_RAG Process/00-RAG-Basic.ipynb`의 색인/실행 단계 분리, `6-2_Chunking/02-RecursiveCharacterTextSplitter.ipynb`의 분할 기준 비교, `6-6_Reranker/01-Cross-Encoder-Reranker.ipynb`의 2단계 검색 전개를 비교함. 내부 강사 지시·오래된 API·임의 권장 수치는 가져오지 않음.
- LangChain RecursiveCharacterTextSplitter 공식 문서: https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter · 확인 2026-09-14.
- LangChain vector store 공식 문서: https://docs.langchain.com/oss/python/integrations/vectorstores · 확인 2026-09-14.
- LangChain retrieval 공식 문서: https://docs.langchain.com/oss/python/deepagents/retrieval · 확인 2026-09-14. 에이전트 구현은 Ch 9~12 범위에 포함하지 않음.
- pgvector 공식 README v0.8.6: https://github.com/pgvector/pgvector · 확인 2026-09-14. 정확/근사 검색, 거리 연산자, HNSW `ef_search`, 필터 후 iterative scan의 strict/relaxed 동작을 대조함.
- Sentence Transformers CrossEncoder 공식 문서: https://www.sbert.net/docs/cross_encoder/usage/usage.html · 확인 2026-09-14. 쌍 점수화, 로짓 범위 주의, top-k 재정렬 용도를 대조함.
- scikit-learn nDCG 공식 API: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html · 확인 2026-09-14. DCG를 이상적 DCG로 정규화하는 정의를 대조함.

## 검증

- 장별 빌드: Ch 9 6절, Ch 10 8절, Ch 11 6절, Ch 12 12절 모두 성공.
- 공통 노트북 검증: Ch 9 `6 sections / 60 code cells (max 25 lines)`, Ch 10 `8 / 66 (max 24)`, Ch 11 `6 / 32 (max 24)`, Ch 12 `12 / 81 (max 25)` 통과. 합계 32절·239개 코드 셀.
- 회귀 테스트: Ch 9 10개, Ch 10 38개, Ch 11 8개, Ch 12 4개, 합계 60개 통과.
- 원본 비교: 대응 노트북 32개의 코드 셀 `source`·`outputs`·`execution_count` 해시 동일. 교재 `_src` 32개는 모두 개정됨.
- JSON 형식: 노트북 32개 모두 `jq empty` 통과.
- 독립 검토 1차 보류 사유를 모두 보정함. 최종 언어 감사와 전체 화면·배포 묶음 검증은 root 검토 단계에서 수행 예정.

- Root 최종 보정: Ch09-05 핵심 개념의 잔존 메서드명을 실제 `similarity_search()`와 `Document.metadata["doc_id"]` 접근으로 교정했습니다. 코드·출력은 그대로입니다.
