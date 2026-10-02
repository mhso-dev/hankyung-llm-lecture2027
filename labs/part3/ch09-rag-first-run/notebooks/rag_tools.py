"""Ch 9 RAG 첫 실행 — 앞 절과 앞 챕터에서 배운 함수를 모아 둔 도구 파일입니다.

뒤 절 노트북은 이 파일의 함수를 `from rag_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
노트북에서 만든 이름(encoding, persona_text, task_text, closure_keep_words 등)을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
"""

from pypdf import PdfReader
from langchain_core.documents import Document


# Ch 8 01절에서 배웠습니다 — 토큰화 규칙 객체로 글 하나를 토큰 번호 목록으로 바꾸고, 그 개수(토큰 수)를 반환합니다
# Ch 8 01절 판은 바깥 이름 encoding을 읽었고, 이 판은 토큰화 규칙 객체를 첫 인자로 받습니다(Ch 8 도구 파일 판과 같음)
def count_tokens(encoding, text):
    token_ids = encoding.encode(text)
    return len(token_ids)


# Ch 8 02절에서 배웠습니다 — 답 글에 출처 표시가 들어 있는 기록만 골라 목록으로 반환합니다
def find_cited_notes(answer_text, notes):
    cited = []
    for note in notes:
        mark = "[" + note["출처"] + "]"
        if mark in answer_text:
            cited.append(note)
    return cited


# Ch 8 03절에서 배웠습니다 — 글에 들어 있지 않은 지킬 말만 모아 목록으로 반환합니다
def find_missing_words(text, words):
    missing = []
    for word in words:
        if word not in text:
            missing.append(word)
    return missing


# Ch 8 04절에서 배웠습니다 — 기록 목록과 질문 하나로 Ch 7 모양의 메시지 목록(system·developer·user)을 만들어 반환합니다
# Ch 8 04절 판은 바깥 이름 persona_text·task_text를 읽었고, 이 판은 두 글을 앞의 두 인자로 받습니다(Ch 8 도구 파일 판과 같음)
def build_notes_messages(persona_text, task_text, notes, question):
    evidence_text = ""
    for note in notes:
        evidence_text = evidence_text + "[" + note["출처"] + "] " + note["내용"] + "\n"
    user_text = evidence_text + "\n" + "질문: " + question
    messages = [
        ("system", persona_text),
        ("developer", task_text),
        ("user", user_text),
    ]
    return messages


# Ch 8 04절에서 배웠습니다 — 답의 출처 표시와 같은 기록의 출처, 답에서 빠진 지킬 말을 딕셔너리로 반환합니다
# Ch 8 04절 판은 바깥 이름 closure_keep_words를 읽었고, 이 판은 지킬 말 목록을 셋째 인자로 받습니다(Ch 8 도구 파일 판과 같음)
def check_answer(answer_text, notes, keep_words):
    cited = find_cited_notes(answer_text, notes)
    cited_sources = []
    for note in cited:
        cited_sources.append(note["출처"])
    missing = find_missing_words(answer_text, keep_words)
    check = {"답의 출처 표시와 같은 기록": cited_sources, "답에서 빠진 지킬 말": missing}
    return check


# 02절에서 배웠습니다 — PDF 경로와 문서 이름을 받아, 쪽마다 본문과 메타데이터를 담은 Document 목록을 반환합니다
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


# 04절에서 배웠습니다 — 문서 청크 하나를 받아, 문서 이름과 쪽 번호로 만든 출처와 본문을 담은 기록을 반환합니다
def make_note(chunk):
    doc_id = chunk.metadata["doc_id"]
    page = chunk.metadata["page"]
    note = {"출처": f"{doc_id} p.{page}", "내용": chunk.page_content}
    return note


# 05절에서 배웠습니다 — 정답 출처 가운데 검색 출처 목록에 없는 것만 모아 반환합니다
def find_missing_sources(hit_sources, answer_sources):
    missing = []
    for source in answer_sources:
        if source not in hit_sources:
            missing.append(source)
    return missing
