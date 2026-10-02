# Chapter 11 평가 기초 실습

노트북은 각각 새 Python 3.12 커널에서 독립 실행됩니다. 02~07절 노트북은 앞 절과 앞 챕터에서 배운 함수를 `notebooks/rag_tools.py`에서 가져오므로, 이 파일을 노트북과 같은 폴더에 그대로 둡니다. VS Code에서 `labs/part3/ch11-evaluation` 폴더를 열고 그 폴더의 터미널에서 `uv sync --locked`를 실행한 뒤 `.venv`의 Python 3.12 커널을 선택합니다. 제공된 질문 30개와 공개 PDF를 사용하며, 기본 평가는 개발용 15개로 실행됩니다. 전체 30개는 `--split all`을 명시할 때만 사용합니다. 정답 문서 ID는 검색 지표 계산을 위해 포함합니다. 답변 문자열과 비공개 정답 자료는 포함하지 않습니다.

```bash
uv run python evaluate.py --top-k 5 --output runs/baseline.json
```

자동 평가 결과의 기본 스키마는 `run_id`, `run_date`, `settings`, `metrics_policy`, `corpus_fingerprint`, `metrics`, `slices`, `split_slices`, `query_count`, `excluded_query_count`, `results`입니다. `metrics`에는 `recall_at_5`, `recall_at_50`, `precision_at_5`, `ndcg_at_5`가 들어갑니다. 질문별 결과에는 `gold_doc_ids`, `candidate_count`, `candidate_doc_ids`, `returned_count`, `top_results`를 함께 남깁니다. `candidate_count`와 `candidate_doc_ids`는 지표 계산에 사용한 전체 고유 후보를 나타냅니다. `returned_count`는 보고서에 보존한 `top_results`의 수이며, `top_results`에는 문서·쪽·청크 ID, 순위, 점수를 보존합니다. 기본 검색기는 TF-IDF가 아니라 단어와 한글 두 글자 조각 겹침을 사용합니다.

Ch 9·10이 만든 continuity 검색 로그는 다음 명령으로 읽습니다. `--retrieval-log`의 상대 경로는 압축을 풀어 만든 최상위 폴더를 기준으로 적습니다. 이 두 파일은 Q001 하나로 연결 형식을 확인하는 용도입니다. 30개 질문 기준선과 직접 수치를 비교하지 않습니다.

```bash
uv run python evaluate.py \
  --retrieval-log labs/part3/ch09-rag-first-run/runs/continuity-ch09-search.jsonl \
  --retrieval-log labs/part3/ch10-document-processing/runs/continuity-ch10-indexing.jsonl \
  --output runs/continuity-upstream-20260910.json
```

07절 실습 노트북 `notebooks/07-평가-기초-실습.ipynb`는 개발 분할 앞 네 문항으로 자르는 자리만 바꾼 두 실행을 각각 기록 한 줄로 만들어 견줍니다. 임베딩 요청은 색인 한 번과 질문 네 번을 합쳐 다섯 번이고, 이 노트북은 `runs/` 폴더에 파일을 쓰지 않습니다.
