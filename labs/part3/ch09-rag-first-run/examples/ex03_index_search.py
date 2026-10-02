"""03절 — 임베딩·벡터스토어·top-k 검색. 질문이 어떤 청크를 끌어오는지 점수와 함께 본다."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from rag import DEFAULT_EMBEDDING, build_index, corpus_paths, load_pdfs, search, split_docs

INDEX_PATH = (
    Path(__file__).resolve().parents[1]
    / ".cache"
    / "index-easy-medium-hard-500-50-text-embedding-3-small.json"
)

docs = load_pdfs(corpus_paths(["easy", "medium", "hard"]))
chunks = split_docs(docs, chunk_size=500, chunk_overlap=50)
print(f"문서 {len(docs)}쪽 → 청크 {len(chunks)}개")

if INDEX_PATH.exists():
    store = InMemoryVectorStore.load(str(INDEX_PATH), OpenAIEmbeddings(model=DEFAULT_EMBEDDING))
    print("저장된 색인을 불러왔습니다:", INDEX_PATH.name)
else:
    t = time.time()
    store = build_index(chunks)
    print(f"임베딩 + 색인 {time.time() - t:.1f}초")
    INDEX_PATH.parent.mkdir(exist_ok=True)
    store.dump(str(INDEX_PATH))
    print("색인을 저장했습니다:", INDEX_PATH.name)

# 임베딩 벡터가 무엇인지 한 번 본다
emb = OpenAIEmbeddings(model=DEFAULT_EMBEDDING)
v = emb.embed_query("도서관 휴관일")
print(f"\n'도서관 휴관일' → 길이 {len(v)} 벡터, 앞 4개 값 {[round(x, 4) for x in v[:4]]}")


def show(query: str, k: int = 4) -> None:
    print(f"\n질문: {query}")
    for doc, score in search(store, query, k=k):
        m = doc.metadata
        head = doc.page_content[:60].replace("\n", " ")
        print(f"  {score:.3f}  [{m['doc_id']} p.{m['page']} #{m['chunk_id']}]  {head}…")


show("미르시립도서관의 정기 휴관일은 언제인가요?")
show("도우미봇 R2 배터리는 몇 시간 가나요?")
show("오로라 로지스틱스 사고 원인은 무엇인가요?")
