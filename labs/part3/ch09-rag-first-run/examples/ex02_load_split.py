"""02절 — 로더와 스플리터. PDF가 Document로, Document가 청크로 바뀌는 과정을 눈으로 본다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tiktoken

from rag import corpus_paths, load_pdfs, split_docs

paths = corpus_paths(["easy"])
docs = load_pdfs(paths)
print(f"PDF {len(paths)}개 → Document {len(docs)}개 (쪽 단위)")
print("첫 Document metadata:", docs[0].metadata)
print("첫 Document 앞 120자:", repr(docs[0].page_content[:120]))

for size, overlap in [(500, 50), (1000, 100), (300, 0)]:
    chunks = split_docs(docs, chunk_size=size, chunk_overlap=overlap)
    lens = [len(c.page_content) for c in chunks]
    print(
        f"chunk_size={size:4d} overlap={overlap:3d} → 청크 {len(chunks):3d}개, "
        f"길이 최소 {min(lens)} / 평균 {sum(lens) // len(lens)} / 최대 {max(lens)}"
    )

chunks = split_docs(docs, chunk_size=500, chunk_overlap=50)
c = chunks[3]
print("\n청크 #3 metadata:", c.metadata)
print("청크 #3 끝 80자:", repr(c.page_content[-80:]))
print("청크 #4 앞 80자:", repr(chunks[4].page_content[:80]))

# 한국어는 글자 수와 토큰 수가 다르다 — 청크 크기 단위를 헷갈리지 말 것
enc = tiktoken.get_encoding("cl100k_base")
sample = c.page_content
print(f"\n청크 #3: {len(sample)}자 = {len(enc.encode(sample))} 토큰 (cl100k_base)")
