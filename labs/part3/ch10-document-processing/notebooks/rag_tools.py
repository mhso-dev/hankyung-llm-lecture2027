"""Ch 10 문서 처리 — 앞 절과 앞 챕터에서 배운 함수를 모아 둔 도구 파일입니다.

뒤 절 노트북은 이 파일의 함수를 `from rag_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
노트북에서 만든 이름(encoding 등)을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
"""

from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document


# Ch 8 01절에서 배웠습니다 — 조각 세는 규칙 객체로 글 하나를 조각 번호 목록으로 바꾸고, 그 개수(조각 수)를 반환합니다
# Ch 8 01절 판은 바깥 이름 encoding을 읽었고, 이 판은 조각 세는 규칙 객체를 첫 인자로 받습니다(Ch 9 도구 파일 판과 같음)
def count_tokens(encoding, text):
    token_ids = encoding.encode(text)
    return len(token_ids)


# Ch 8 03절에서 배웠습니다 — 글에 들어 있지 않은 지킬 말만 모아 목록으로 반환합니다
def find_missing_words(text, words):
    missing = []
    for word in words:
        if word not in text:
            missing.append(word)
    return missing


# Ch 9 02절에서 배웠습니다 — PDF 경로와 문서 이름을 받아, 쪽마다 본문과 메타데이터를 담은 Document 목록을 반환합니다
def load_pdf_pages(pdf_path, doc_id):
    reader = PdfReader(pdf_path)
    page_documents = []
    page_number = 1
    for page in reader.pages:
        metadata = {"doc_id": doc_id, "page": page_number, "source": doc_id + ".pdf"}
        page_document = Document(page_content=page.extract_text(), metadata=metadata)
        page_documents.append(page_document)
        page_number = page_number + 1
    return page_documents


# Ch 9 03절에서 배웠습니다 — 문서 청크 하나를 받아 기록의 doc_id·page 두 칸으로 [E01 p.2] 모양의 출처 표시를 만들어 반환합니다
def make_source_mark(chunk):
    doc_id = chunk.metadata["doc_id"]
    page = chunk.metadata["page"]
    source_mark = f"[{doc_id} p.{page}]"
    return source_mark


# 01절에서 배웠습니다 — 파일 경로·쪽 번호·읽은 방법 이름을 받아 다섯 칸 출처 기록을 만들어 반환합니다
def make_source_record(file_path, page, parser):
    path_object = Path(file_path)
    suffix = path_object.suffix
    file_type = suffix.replace(".", "").lower()
    record = {"doc_id": path_object.stem, "source": path_object.name,
              "file_type": file_type, "parser": parser, "page": page}
    return record


# 02절에서 배웠습니다 — 머리글 하나와 칸 하나를 받아 「머리글: 값」 꼴로 짝지은 글을 만들어 반환합니다(아래 make_row_text 안에서 씁니다)
def make_cell_text(label, cell):
    value = cell
    if value == "":
        value = "(값 없음)"
    return label + ": " + value


# 02절에서 배웠습니다 — 머리글 행과 표의 한 행을 받아 칸마다 머리글을 붙인 한 줄 글을 만들어 반환합니다
def make_row_text(header_row, row):
    row_text = ""
    cell_number = 0
    for cell in row:
        cell_text = make_cell_text(header_row[cell_number], cell)
        if row_text != "":
            row_text = row_text + " / "
        row_text = row_text + cell_text
        cell_number = cell_number + 1
    return row_text


# 03절에서 배웠습니다 — 파일 경로와 읽은 방법 이름을 받아 쪽 번호가 없는 네 칸 출처 기록을 만들어 반환합니다
def make_unit_record(file_path, parser):
    path_object = Path(file_path)
    suffix = path_object.suffix
    file_type = suffix.replace(".", "").lower()
    record = {"doc_id": path_object.stem, "source": path_object.name,
              "file_type": file_type, "parser": parser}
    return record


# 03절에서 배웠습니다 — 문서 청크 하나를 받아 파일 형식과 자리 칸 row를 넣은 출처 표시를 만들어 반환합니다
def make_unit_mark(chunk):
    doc_id = chunk.metadata["doc_id"]
    file_type = chunk.metadata["file_type"]
    unit_mark = f"[{doc_id} {file_type}]"
    if "row" in chunk.metadata:
        row_number = chunk.metadata["row"]
        unit_mark = f"[{doc_id} {file_type} row.{row_number}]"
    return unit_mark


# 04절에서 배웠습니다 — 태그 이름에서 이름 공간을 떼고 뒤쪽 이름만 남겨 반환합니다(아래 read_body_text 안에서 씁니다)
def make_local_name(tag_name):
    return tag_name.split("}")[-1]


# 04절에서 배웠습니다 — XML 요소 나무에서 고른 이름의 요소만 찾아 글을 순서대로 이어 붙여 반환합니다
def read_body_text(xml_root, wanted_name):
    body_text = ""
    for node in xml_root.iter():
        local_name = make_local_name(node.tag)
        if local_name != wanted_name:
            continue
        if node.text is not None:
            body_text = body_text + node.text
    return body_text


# 04절에서 배웠습니다 — 문서 청크 하나를 받아 파일 형식과 자리 칸 section을 넣은 출처 표시를 만들어 반환합니다
def make_section_mark(chunk):
    doc_id = chunk.metadata["doc_id"]
    file_type = chunk.metadata["file_type"]
    section_mark = f"[{doc_id} {file_type}]"
    if "section" in chunk.metadata:
        section_number = chunk.metadata["section"]
        section_mark = f"[{doc_id} {file_type} section.{section_number}]"
    return section_mark


# 05절에서 배웠습니다 — 글 목록을 받아 문자 수를 순서대로 모아 반환합니다
def make_length_list(chunk_texts):
    lengths = []
    for chunk_text in chunk_texts:
        lengths.append(len(chunk_text))
    return lengths


# 05절에서 배웠습니다 — 문서 청크 글 목록에서 지킬 말이 모두 든 문서 청크의 번호(1부터)를 모아 반환합니다
def find_chunks_with_words(chunk_texts, words):
    found_numbers = []
    number = 1
    for chunk_text in chunk_texts:
        missing = find_missing_words(chunk_text, words)
        if missing == []:
            found_numbers.append(number)
        number = number + 1
    return found_numbers
