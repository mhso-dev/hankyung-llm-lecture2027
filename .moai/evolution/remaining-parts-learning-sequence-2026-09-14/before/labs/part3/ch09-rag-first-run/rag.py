"""Ch 9 — RAG 첫 완주.

다섯 단계를 각각 평범한 파이썬 함수로 만든다.
    load_pdfs → split_docs → build_index → search → generate
각 함수의 입력과 출력이 그대로 보이므로 어느 단계가 망가졌는지 바로 찾을 수 있다.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

# 프로젝트 루트의 .env에서 OPENAI_API_KEY를 읽는다 (코드에 키를 적지 않는다)
load_dotenv(Path(__file__).resolve().parents[3] / ".env")

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "rag-corpus"

# [[미정: 임베딩 모델]] — 확정 전까지 OpenAI text-embedding-3-small 로 진행
DEFAULT_EMBEDDING = "text-embedding-3-small"
DEFAULT_CHAT = "openai:gpt-5.4-mini"


# ---------------------------------------------------------------- 1. 로드
def load_pdfs(paths: list[Path]) -> list[Document]:
    """PDF 한 쪽을 Document 하나로 만든다.

    metadata에 doc_id·page를 남겨 둔다 — 출처 인용(04절)과 평가(Ch 11)가 이 값을 쓴다.
    """
    docs: list[Document] = []
    for path in paths:
        reader = PdfReader(str(path))
        doc_id = path.stem.split("-")[0]  # "E01.pdf" → "E01", "S01-E01-scan.pdf" → "S01"
        for page_no, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if not text.strip():
                continue  # 스캔본처럼 텍스트 레이어가 없는 쪽은 건너뛴다 (Ch 10 OCR)
            docs.append(
                Document(
                    page_content=text,
                    metadata={"doc_id": doc_id, "page": page_no, "source": path.name},
                )
            )
    return docs


def corpus_paths(tiers: list[str] | None = None) -> list[Path]:
    """rag-corpus에서 난이도별 PDF 경로를 모은다. tiers 미지정 시 easy·medium·hard."""
    tiers = tiers or ["easy", "medium", "hard"]
    paths: list[Path] = []
    for tier in tiers:
        paths.extend(sorted((DATA_DIR / "pdf" / tier).glob("*.pdf")))
    return paths


# ---------------------------------------------------------------- 2. 분할
def split_docs(
    docs: list[Document], chunk_size: int = 500, chunk_overlap: int = 50
) -> list[Document]:
    """쪽 단위 Document를 글자 수 기준 청크로 나눈다. metadata는 청크마다 복사된다."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],  # 큰 경계부터 시도한다
    )
    chunks = splitter.split_documents(docs)
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i  # 디버깅할 때 "몇 번 청크"로 부르기 위해
    return chunks


# ---------------------------------------------------------------- 3. 색인
def build_index(
    chunks: list[Document], embedding_model: str = DEFAULT_EMBEDDING
) -> InMemoryVectorStore:
    """청크를 임베딩해 메모리 벡터스토어에 넣는다. 한 번 만들면 dump()로 저장할 수 있다."""
    embeddings = OpenAIEmbeddings(model=embedding_model)
    store = InMemoryVectorStore(embedding=embeddings)
    store.add_documents(chunks)
    return store


# ---------------------------------------------------------------- 4. 검색
def search(store: InMemoryVectorStore, query: str, k: int = 4) -> list[tuple[Document, float]]:
    """질문과 가장 가까운 청크 k개를 (청크, 유사도) 쌍으로 반환한다. 점수가 높을수록 가깝다."""
    return store.similarity_search_with_score(query, k=k)


# ---------------------------------------------------------------- 5. 생성
SYSTEM_PROMPT = """당신은 사내 문서 안내 담당자입니다.
아래 [문서] 절만 근거로 한국어로 답하세요.
답의 근거가 된 문장 뒤에 [doc_id p.페이지] 형식으로 출처를 붙이세요."""


def format_context(hits: list[tuple[Document, float]]) -> str:
    """검색 결과를 모델이 읽을 문자열로 바꾼다. 출처 표기는 여기서 정한 형식을 따른다."""
    blocks = []
    for doc, _score in hits:
        tag = f"[{doc.metadata['doc_id']} p.{doc.metadata['page']}]"
        blocks.append(f"{tag}\n{doc.page_content}")
    return "\n\n---\n\n".join(blocks)


@dataclass
class Answer:
    question: str
    text: str
    sources: list[str] = field(default_factory=list)  # ["E01 p.2", ...]
    input_tokens: int = 0
    output_tokens: int = 0


def generate(
    question: str,
    hits: list[tuple[Document, float]],
    chat_model: str = DEFAULT_CHAT,
    system_prompt: str = SYSTEM_PROMPT,
) -> Answer:
    """검색된 청크를 프롬프트에 넣고 답을 만든다."""
    model = init_chat_model(chat_model)
    context = format_context(hits)
    messages = [
        ("system", system_prompt),
        ("user", f"[문서]\n{context}\n\n[질문]\n{question}"),
    ]
    response = model.invoke(messages)
    usage = response.usage_metadata or {}
    sources = [f"{d.metadata['doc_id']} p.{d.metadata['page']}" for d, _ in hits]
    return Answer(
        question=question,
        text=str(response.content),
        sources=sources,
        input_tokens=usage.get("input_tokens", 0),
        output_tokens=usage.get("output_tokens", 0),
    )


# ---------------------------------------------------------------- 조립
def answer(store: InMemoryVectorStore, question: str, k: int = 4, **kw: str) -> Answer:
    """search → generate 두 단계를 잇는다. 이것이 Ch 9 RAG의 전부다."""
    hits = search(store, question, k=k)
    return generate(question, hits, **kw)


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY가 .env에 없습니다")
    docs = load_pdfs(corpus_paths(["easy"]))
    chunks = split_docs(docs)
    store = build_index(chunks)
    result = answer(store, "미르시립도서관의 정기 휴관일은 언제인가요?")
    print(result.text)
    print("출처 후보:", result.sources)
