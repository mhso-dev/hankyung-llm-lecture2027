import math
import sys
from pathlib import Path

import pytest
import tiktoken
from langchain_core.documents import Document

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from document_processing import split_char, split_semantic, split_structural, split_token


def pages() -> list[Document]:
    return [
        Document(page_content="가" * 80, metadata={"doc_id": "guide", "page": 1}),
        Document(page_content="나" * 80, metadata={"doc_id": "guide", "page": 2}),
    ]


def test_split_char_makes_chunk_ids_unique_across_source_pages() -> None:
    chunks = split_char(pages(), chunk_size=30, overlap=5)

    ids = [chunk.metadata["chunk_id"] for chunk in chunks]
    assert len(ids) == len(set(ids))
    assert any(":page1:" in chunk_id for chunk_id in ids)
    assert any(":page2:" in chunk_id for chunk_id in ids)


def test_split_token_preserves_unicode_codepoints() -> None:
    text = "한글·emoji 👩🏽‍💻·accent café " * 20

    chunks = split_token(
        [Document(page_content=text, metadata={"doc_id": "unicode", "page": 1})],
        chunk_tokens=24,
        overlap_tokens=4,
    )

    assert chunks
    assert all("�" not in chunk.page_content for chunk in chunks)


def test_split_token_never_exceeds_token_limit() -> None:
    codec = tiktoken.get_encoding("cl100k_base")

    chunks = split_token(pages(), chunk_tokens=20, overlap_tokens=3)

    assert all(len(codec.encode(chunk.page_content)) <= 20 for chunk in chunks)


def test_split_token_handles_codepoint_larger_than_token_limit_explicitly() -> None:
    codec = tiktoken.get_encoding("cl100k_base")
    doc = Document(page_content="힐", metadata={"doc_id": "unicode", "page": 1})

    try:
        chunks = split_token([doc], chunk_tokens=1, overlap_tokens=0)
    except ValueError:
        return

    assert all("�" not in chunk.page_content for chunk in chunks)
    assert all(len(codec.encode(chunk.page_content)) <= 1 for chunk in chunks)


def test_split_structural_splits_oversized_final_block_to_max_chars() -> None:
    doc = Document(
        page_content="# 짧은 절\n\n본문\n\n# 마지막 절\n\n" + "마지막블록 " * 60,
        metadata={"doc_id": "guide", "page": 1},
    )

    chunks = split_structural([doc], max_chars=50)

    assert len(chunks) > 2
    assert all(len(chunk.page_content) <= 50 for chunk in chunks)


@pytest.mark.parametrize("threshold", [math.nan, math.inf, -1.01, 1.01])
def test_split_semantic_rejects_invalid_threshold(threshold: float) -> None:
    with pytest.raises(ValueError, match="threshold"):
        split_semantic(pages(), embedder=lambda texts: [[1.0] for _ in texts], threshold=threshold)


def test_split_semantic_rejects_vector_count_mismatch() -> None:
    doc = Document(page_content="첫 문장입니다. 둘째 문장입니다.", metadata={"doc_id": "guide"})

    with pytest.raises(ValueError, match="문장 수"):
        split_semantic([doc], embedder=lambda _texts: [[1.0]], threshold=0.5)


def test_split_semantic_starts_new_chunk_below_similarity_threshold() -> None:
    doc = Document(page_content="첫 문장입니다. 둘째 문장입니다.", metadata={"doc_id": "guide"})

    chunks = split_semantic(
        [doc], embedder=lambda _texts: [[1.0, 0.0], [0.0, 1.0]], threshold=0.5
    )

    assert [chunk.page_content for chunk in chunks] == ["첫 문장입니다.", "둘째 문장입니다."]


def test_split_semantic_splits_oversized_group_to_max_chars() -> None:
    doc = Document(page_content=("같은 주제 문장입니다. " * 30), metadata={"doc_id": "guide"})

    chunks = split_semantic(
        [doc], embedder=lambda texts: [[1.0] for _ in texts], threshold=0.5, max_chars=45
    )

    assert len(chunks) > 1
    assert all(len(chunk.page_content) <= 45 for chunk in chunks)
