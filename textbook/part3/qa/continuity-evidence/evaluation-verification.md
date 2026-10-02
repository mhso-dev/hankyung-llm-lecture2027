# Ch 9·10 → Ch 11 → Ch 12 평가 연결 수정 후 검증

> 검증일: 2026-09-10  
> 수정 범위: `textbook/part3/ch11-evaluation`, `labs/part3/ch11-evaluation`  
> 수정 전 보존본: `textbook/part3/qa/continuity-evidence/before.tar.gz`

## 수정 내용과 최종 연결 관계

| 연결 구간 | 수정 후 구현 | 판정 |
| --- | --- | --- |
| Ch 9 → Ch 11 | Ch 9 06이 공개 PDF 18개와 Ch 11 정본 Q001에서 검색한 후 `continuity-ch09-search.jsonl`에 문서·쪽·청크 ID, 순위, 점수를 남깁니다. Ch 11 06은 이 파일의 질문·정답 ID·순위를 정본 질의셋과 대조한 뒤 검색 지표만 계산합니다. 생성 답변은 Ch 15 평가 대상으로 남겼습니다. | PASS |
| Ch 10 → Ch 11 | Ch 10 08이 실제 PDF 18개에서 3개 청킹 방식×2개 임베딩 모델을 실행하고, 6개 실행을 `continuity-ch10-indexing.jsonl`에 나눠 보존합니다. Ch 11 로더는 같은 Q001이라도 `source_run_id`별로 덮어쓰지 않고 평가합니다. | PASS |
| 다중 정답 Recall | Ch 11 05의 Recall@50도 다른 절 및 `evaluate.py`와 같이 `검색된 정답 문서 수 / 전체 정답 문서 수`로 계산합니다. 노트북 함수 AST를 실행하는 회귀 검사에서 정답 2개 중 1개 검색 시 0.5를 확인했습니다. | PASS |
| Ch 11 독립 기준선 | 기준선은 TF-IDF가 아니라 단어·한글 두 글자 조각 겹침을 사용하며, 검색된 쪽 단위 후보의 `doc_id`, `page`, `chunk_id`, `rank`, `score`를 `top_results`에 보존합니다. 기본 CLI 분할은 dev 15개이고, test 15개는 `--split test`를 명시해야 실행됩니다. | PASS |
| 후보 수가 다른 로그 | Ch 9의 저장 후보는 2개이므로 `recall_at_logged_candidates`만 계산하고 @5·@50 지표는 `null`로 남깁니다. Ch 10의 저장 후보는 5개이므로 @5는 계산하고 Recall@50은 `null`로 남깁니다. | PASS |
| Ch 11 → Ch 12 | Ch 11의 설정 선택 경로를 dev 15개로 제한했습니다. Ch 12에서는 dev 15개로 설정을 비교하고 선택한 설정을 test 15개로 한 번 확인합니다. Q001 연결 로그, Ch 11의 dev/test 기준선, Ch 12의 청킹·MMR 관찰, Q002 통합 RAG 실행은 서로 다른 질문 수·검색기·평가 단위를 밝히고 직접 수치 비교를 금지했습니다. | PASS |

## 실행 검증

- Python 3.12와 `textbook/_notebook/execute.py`로 Ch 11 노트북 01~06을 새 커널에서 순차 실행했습니다. 코드 셀 수는 각각 5, 6, 5, 5, 5, 6개이며 모두 PASS입니다. Ch 11은 외부 API를 호출하지 않습니다.
- 노트북 06이 읽은 원본은 Ch 9 1행과 Ch 10 6행입니다. 원본 SHA-256은 각각 `4f9fce621e29c4e267d466a38629d6ee78da876593f882397e0ed5e25f5bae61`, `37949f0c677e91de29602f853f968b335dd8ea8aace55e50953e3ef51343b192`입니다.
- Ch 11이 새로 만든 `continuity-upstream-20260909T164029097591Z.json`은 Ch 9 실행 1개와 Ch 10 실행 6개를 별도 `run_id`로 보존합니다. SHA-256은 `fd74213a159bf795b4ca22e3a8c291539589ec4c01c0f71936c37430c41b1a69`입니다. 질문별 `candidate_count`와 `candidate_doc_ids`에는 지표 계산에 쓴 전체 고유 후보가 있고, `returned_count`는 보고용 `top_results` 수와 같습니다. `top_results`에는 문서·쪽·청크 ID, 순위, 점수가 모두 있습니다.
- dev 기준선 15개는 Recall@5 1.000, Recall@50 1.000, Precision@5 0.200, nDCG@5 0.8928526174입니다. test 확인 15개의 nDCG@5는 0.9174573005입니다. dev/test 결과는 각각 `continuity-baseline-dev-20260910.json`, `continuity-baseline-test-20260910.json`에 나눠 보존했습니다. SHA-256은 각각 `de421859fa2c79e34295b3315f06e9167aaa98b872ee1c127ed265d6ea522a97`, `32796e86e8dc409dcc18236284433771ff3720e10a27855dda78fa8339d62da1`입니다. 두 실행의 `run_id`는 UTC 시각을 포함해 서로 다릅니다.
- 전체 검사 stdout은 `textbook/part3/qa/continuity-evidence/evaluation-tests.txt`에 보존했습니다.
- README에 적힌 작업 폴더 `labs/part3/ch11-evaluation`에서 안내 명령을 그대로 실행했습니다. 저장소 루트 기준 입력 경로로 Ch 9 1행과 Ch 10 6행을 읽어 `runs/continuity-upstream-20260910.json`을 만들었고, 실행별 질문 수 `[1, 1, 1, 1, 1, 1, 1]`을 확인했습니다.
- `uv run --project labs/part3/ch11-evaluation --with pytest==9.0.2 pytest -q labs/part3/ch11-evaluation/tests/test_evaluate.py`는 8개 회귀 검사를 모두 통과했습니다. 다중 정답 질문의 부분 Recall, 상위 5개 밖 후보로 Recall@50 재계산, 후보 수 경계, 문서 ID 중복, 쪽 후보 출처 항목, 빈 정답, Ch 9·10 스키마, 질문 불일치 거부를 확인했습니다.
- `uv run --project labs/part3/ch11-evaluation --with ruff==0.15.7 ruff check labs/part3/ch11-evaluation/evaluate.py labs/part3/ch11-evaluation/tests/test_evaluate.py labs/part3/ch11-evaluation/_make_notebooks.py`도 통과했습니다.
- `_build.py`로 index와 6개 절을 다시 빌드했습니다. `verify.py` 결과는 `PASS 6 sections / 32 code cells (max 24 lines)`입니다. `_src` 본문, HTML, 노트북 코드·출력이 같은 dev/test 분할과 지표 정책을 설명합니다.

## 한국어 및 의미 검토

- 작성자와 분리된 검토자가 Ch 10의 실제 산출물, Ch 11의 dev/test 사용, 후보 수와 지표 컷오프, Ch 12의 Q002 통합 RAG 실행 단위를 다시 대조했습니다. 지적된 문장은 `_src`에 반영한 뒤 재빌드했습니다. 최종 독립 검토는 8개 회귀 검사와 dev 기준선·Ch 9·10 연결 실행의 필드 및 지표를 직접 재확인했고, Ch 11 범위에 남은 중요 결함이 없다고 판정했습니다.
- 코드, 명령, 파일 경로는 문장 감사 대상에서 제외했습니다. 외부 맞춤법 서비스를 이용한 일괄 검사는 `korean-spell-check` 절차의 상업적 대량 전송 제한 때문에 생략했습니다. 대신 로컬 한국어 3단 감사와 분리된 검토자의 전문 의미 대조를 반영했습니다.

## 남은 한계

- Ch 9·10 연결 로그는 Q001 한 문항으로 파일 전달·스키마·지표 연결을 확인합니다. 검색 품질의 일반적인 우열을 판정하는 근거로 사용하지 않습니다.
- Ch 11 독립 기준선의 고유 문서는 17개이므로 Recall@50은 천장에 도달합니다. 50위 경계 공식은 51개 고유 문서를 사용한 별도 통제 목록으로 검사했습니다.
- Ch 11은 검색 순위만 평가합니다. 생성 답변의 충실성·정확성 평가는 Ch 15의 학습 범위입니다.
