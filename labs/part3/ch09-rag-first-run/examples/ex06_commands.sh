uv run python harness.py
uv run python harness.py --set split.chunk_size=1000 --set split.chunk_overlap=100 --set name=chunk1000
uv run python harness.py --set retrieval.k=8 --set name=k8
uv run python harness.py --set generation.prompt=helpful --set name=helpful
