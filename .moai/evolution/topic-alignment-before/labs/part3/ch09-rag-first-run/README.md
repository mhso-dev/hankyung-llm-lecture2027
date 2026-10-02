# Ch 9 — RAG 첫 완주 + 실험 하네스

기본 학습 경로는 `notebooks/`의 절별 노트북입니다. 각 노트북은 짧은 인라인 문서로 개념을 확인하며, 프로젝트 루트의 `.env`에서 `OPENAI_API_KEY`를 읽습니다. Jupyter에서 노트북을 열고 커널을 다시 시작한 뒤 위에서 아래로 실행합니다.

아래 스크립트와 전체 PDF 말뭉치는 기본 노트북을 마친 뒤 사용하는 선택 확장입니다. 노트북의 작은 실행 결과와 스크립트의 전체 말뭉치 결과는 규모가 다릅니다.

```bash
cd labs/part3/ch09-rag-first-run
uv sync                                   # Python 3.12, langchain 1.4
uv run python examples/ex02_load_split.py # 02절 로더·스플리터
uv run python examples/ex03_index_search.py
uv run python examples/ex04_generate.py
uv run python examples/ex05_failure.py
uv run python harness.py                  # 06절 하네스 → runs/runs.jsonl 한 줄
uv run python harness.py --set split.chunk_size=1000 --set name=chunk1000
uv run pytest -q
```

`OPENAI_API_KEY`는 프로젝트 루트 `.env`에서 읽습니다. `.cache/`(색인)와 `runs/`(실험 로그)는 실행하면 생깁니다.
