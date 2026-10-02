import _paths  # noqa: F401
import tiktoken
from langchain_core.documents import Document

from document_processing import split_char, split_recursive, split_token


def main() -> None:
    text = "제1조 배송\n\n제주 지역은 이틀이 더 필요합니다. 고객은 배송 상태를 확인합니다. " * 12
    docs = [Document(page_content=text, metadata={"doc_id": "배송", "page": 1})]
    char = split_char(docs, chunk_size=120, overlap=20)
    recursive = split_recursive(docs, chunk_size=120, overlap=20)
    token = split_token(docs, chunk_tokens=50, overlap_tokens=8)
    print(f"char_chunks={len(char)} max_chars={max(len(d.page_content) for d in char)}")
    print(f"recursive_chunks={len(recursive)} max_chars={max(len(d.page_content) for d in recursive)}")
    print(f"token_chunks={len(token)} replacement_chars={sum('�' in d.page_content for d in token)}")
    codec = tiktoken.get_encoding("cl100k_base")
    print(
        f"token_first=chars:{len(token[0].page_content)},tokens:{len(codec.encode(token[0].page_content))}"
    )
    recursive_overlap = recursive[0].page_content[-20:].strip() in recursive[1].page_content
    print(f"recursive_literal_tail_overlap={recursive_overlap} (separator boundaries may vary)")
    print(f"metadata_preserved={all(d.metadata['doc_id'] == '배송' for d in char + recursive + token)}")


if __name__ == "__main__":
    main()
