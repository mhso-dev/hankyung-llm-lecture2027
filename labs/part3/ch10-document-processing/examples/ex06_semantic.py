import _paths  # noqa: F401
from langchain_core.documents import Document

from document_processing import educational_feature_vectors, split_semantic, split_structural


def main() -> None:
    text = """# 배송
제주 배송에는 이틀이 더 필요합니다. 제주 배송 상태는 앱에서 확인합니다.

# 환불
환불은 수령 후 7일 이내 신청합니다. 환불 금액은 결제 수단으로 반환합니다."""
    docs = [Document(page_content=text, metadata={"doc_id": "안내"})]
    structural = split_structural(docs, max_chars=90)
    semantic = split_semantic(
        docs,
        embedder=lambda texts: educational_feature_vectors(texts, dimensions=256),
        threshold=0.62,
    )
    print(f"structural_chunks={len(structural)}")
    print(f"semantic_chunks={len(semantic)}")
    print("semantic_backend=educational-feature-hash (not a model-quality benchmark)")
    print(f"chunk_ids={[doc.metadata['chunk_id'] for doc in semantic]}")
    for index, chunk in enumerate(semantic, start=1):
        print(f"semantic_{index}={chunk.page_content}")


if __name__ == "__main__":
    main()
