"""예제 공용 — 저장된 색인을 불러오거나 새로 만든다 (03절에서 만든 .cache 재사용)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from rag import DEFAULT_EMBEDDING, build_index, corpus_paths, load_pdfs, split_docs

CACHE = Path(__file__).resolve().parents[1] / ".cache"


def get_store(
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    tiers: tuple[str, ...] = ("easy", "medium", "hard"),
    embedding_model: str = DEFAULT_EMBEDDING,
) -> InMemoryVectorStore:
    name = f"index-{'-'.join(tiers)}-{chunk_size}-{chunk_overlap}-{embedding_model}.json"
    path = CACHE / name
    emb = OpenAIEmbeddings(model=embedding_model)
    if path.exists():
        return InMemoryVectorStore.load(str(path), emb)
    chunks = split_docs(load_pdfs(corpus_paths(list(tiers))), chunk_size, chunk_overlap)
    store = build_index(chunks, embedding_model)
    CACHE.mkdir(exist_ok=True)
    store.dump(str(path))
    return store
