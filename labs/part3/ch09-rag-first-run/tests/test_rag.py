"""02~04절 예제의 검증 — API 없이 도는 것과 API가 필요한 것을 나눈다."""

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from langchain_core.documents import Document

from rag import DATA_DIR, build_index, corpus_paths, format_context, load_pdfs, search, split_docs

needs_api = pytest.mark.skipif(not os.environ.get("OPENAI_API_KEY"), reason="OPENAI_API_KEY 없음")


def test_load_pdfs_keeps_doc_id_and_page() -> None:
    docs = load_pdfs([DATA_DIR / "pdf" / "easy" / "E01.pdf"])
    assert len(docs) == 5  # E01은 5쪽
    assert docs[0].metadata == {"doc_id": "E01", "page": 1, "source": "E01.pdf"}
    assert "미르시립도서관" in docs[0].page_content


def test_load_pdfs_skips_pages_without_text_layer() -> None:
    scanned = load_pdfs([DATA_DIR / "pdf" / "scanned" / "S01-E01-scan.pdf"])
    assert scanned == []  # 스캔본은 텍스트가 없다 → Ch 10 OCR


def test_corpus_paths_counts() -> None:
    assert len(corpus_paths(["easy"])) == 6
    assert len(corpus_paths()) == 18  # easy + medium + hard


def test_split_respects_chunk_size_and_copies_metadata() -> None:
    docs = load_pdfs(corpus_paths(["easy"]))
    chunks = split_docs(docs, chunk_size=500, chunk_overlap=50)
    assert all(len(c.page_content) <= 500 for c in chunks)
    assert all({"doc_id", "page", "chunk_id"} <= c.metadata.keys() for c in chunks)
    assert [c.metadata["chunk_id"] for c in chunks] == list(range(len(chunks)))


def test_overlap_repeats_text_between_neighbors() -> None:
    doc = Document(
        page_content="가나다라마바사아자차카타파하 " * 40, metadata={"doc_id": "T", "page": 1}
    )
    chunks = split_docs([doc], chunk_size=100, chunk_overlap=30)
    tail, head = chunks[0].page_content[-15:], chunks[1].page_content
    assert tail.strip() in head  # 앞 청크 끝이 다음 청크 앞에 다시 나온다


def test_format_context_tags_each_chunk() -> None:
    hits = [(Document(page_content="본문", metadata={"doc_id": "E01", "page": 2}), 0.9)]
    assert format_context(hits) == "[E01 p.2]\n본문"


@needs_api
def test_search_returns_k_hits_sorted_by_score() -> None:
    docs = load_pdfs([DATA_DIR / "pdf" / "easy" / "E01.pdf"])
    store = build_index(split_docs(docs))
    hits = search(store, "미르시립도서관의 정기 휴관일은 언제인가요?", k=4)
    assert len(hits) == 4
    scores = [s for _, s in hits]
    assert scores == sorted(scores, reverse=True)
    assert any("휴관" in d.page_content for d, _ in hits)
