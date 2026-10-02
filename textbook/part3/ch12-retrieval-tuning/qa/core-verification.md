# Ch 12 전반 실행 검증

## 새 커널 실행

2026-09-09에 `textbook/_notebook/execute.py`로 01~06 노트북을 각각 새 Python 3.12.13 커널에서 실행했습니다. 최종 실행은 모두 `status=passed`이며, 노트북 내부에 코드와 출력 SHA-256이 기록되어 있습니다.

| 절 | 코드 셀 | 핵심 실제 출력 |
|---|---:|---|
| 01 | 6 | cosine 7/8, L2 7/8 |
| 02 | 7 | pgvector 0.8.2, vector(2001) HNSW 실패, halfvec(2001) 성공 |
| 03 | 6 | iterative scan off 0개, strict_order 5개 |
| 04 | 6 | Kiwi+BM25 8/8 |
| 05 | 8 | dense 7/8, sparse 8/8, 차이 C02 |
| 06 | 8 | dense 7/8, sparse 8/8, RRF 7/8 |

모든 코드 셀은 16줄 이하입니다. 01·02·05·06절은 `.env`의 OpenAI API 키로 실제 임베딩을 호출했습니다. 03절은 실제 PostgreSQL HNSW SQL을 실행했고, 04절은 로컬 Kiwi와 BM25를 실행했습니다.

## 데이터베이스 경계

- 컨테이너: `hankyung-part3-pgvector`
- 이미지: `pgvector/pgvector:0.8.2-pg17`
- 호스트 공개: `127.0.0.1:55432`
- 변경 표: `ch12_core_hnsw`, `ch12_core_dim_vector`, `ch12_core_dim_halfvec`, `ch12_core_filter`

## 제한

전체 챕터 빌드·정적 검사·PC 1280px·모바일 390px 화면 검사는 07~12절과 SVG/Excalidraw가 준비된 뒤 수행합니다. 현재 실행 결과는 12개 교육용 문서와 8개 질문에 한정합니다. Ch 11의 30개 평가 질문에서는 Recall@50이 포화되어 있으므로 후속 종합 비교는 Recall@5, Precision@5, nDCG@5, 반환 문서 수를 함께 사용해야 합니다.
