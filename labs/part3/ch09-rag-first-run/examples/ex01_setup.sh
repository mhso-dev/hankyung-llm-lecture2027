cd labs/part3/ch09-rag-first-run
uv sync
uv run python examples/ex02_load_split.py
uv run python examples/ex03_index_search.py
uv run python examples/ex04_generate.py
uv run python examples/ex05_failure.py
uv run python harness.py
uv run pytest -q
