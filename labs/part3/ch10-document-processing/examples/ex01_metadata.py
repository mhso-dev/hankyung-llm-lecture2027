import _paths  # noqa: F401

from document_processing import normalize_metadata


def main() -> None:
    raw = {"doc_id": "계약-01", "page": "2", "department": "구매팀", "tags": ["납품", "검수"]}
    print(normalize_metadata(raw, source="계약서.PDF", file_type="PDF", parser="pypdf-plain"))


if __name__ == "__main__":
    main()
