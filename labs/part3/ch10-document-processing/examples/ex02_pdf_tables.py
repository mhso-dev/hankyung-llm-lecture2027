from _paths import CORPUS

from document_processing import detect_scanned_pdf, load_pdf, load_pdf_tables_pdfplumber


def main() -> None:
    digital = CORPUS / "pdf" / "easy" / "E02.pdf"
    scanned = CORPUS / "pdf" / "scanned" / "S01-E01-scan.pdf"
    plain = load_pdf(digital, mode="plain")
    layout = load_pdf(digital, mode="layout")
    table_docs = load_pdf_tables_pdfplumber(digital)
    report = detect_scanned_pdf(scanned)
    print(f"digital_pages={len(plain)}")
    print(f"page2_plain_chars={len(plain[1].page_content)}")
    print(f"page2_layout_chars={len(layout[1].page_content)}")
    print(f"plain_has_table_gap={'  ' in plain[1].page_content}")
    print(f"layout_has_table_gap={'  ' in layout[1].page_content}")
    print(f"pdfplumber_tables={sum(int(doc.metadata['table_count']) for doc in table_docs)}")
    print(f"pdfplumber_table_cells={' | ' in ''.join(doc.page_content for doc in table_docs)}")
    plain_lines = [
        line.strip()
        for line in plain[3].page_content.splitlines()
        if any(label in line for label in ("기간", "1일차", "1주차"))
    ][:3]
    table_rows = table_docs[3].page_content.rsplit("\n\n", 1)[-1].splitlines()[:3]
    print("pypdf_plain_page4=" + " / ".join(plain_lines))
    print("pdfplumber_page4_rows=" + " / ".join(table_rows))
    print(f"scan_pages_without_text={list(report.pages_without_text)}")
    print(f"likely_scanned={report.likely_scanned}")
    print("ocr_status=not_run")


if __name__ == "__main__":
    main()
