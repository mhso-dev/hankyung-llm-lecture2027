"""04절 — 생성과 출처 인용. 모델에게 실제로 무엇을 보냈는지, 무엇이 돌아왔는지 본다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _index import get_store

from rag import SYSTEM_PROMPT, answer, format_context, search

store = get_store()

for question in [
    "미르시립도서관의 정기 휴관일은 언제인가요?",
    "별빛제과 수습 기간 급여는 정규 급여의 몇 %인가요?",
]:
    hits = search(store, question, k=4)
    print("=" * 70)
    print("질문:", question)
    print(
        "검색 결과:", [f"{d.metadata['doc_id']} p.{d.metadata['page']} ({s:.2f})" for d, s in hits]
    )
    result = answer(store, question, k=4)
    print("답변:", result.text)
    print(f"토큰: 입력 {result.input_tokens} / 출력 {result.output_tokens}")

# 모델에게 실제로 보내는 문자열을 한 번 눈으로 확인한다
hits = search(store, "미르시립도서관의 정기 휴관일은 언제인가요?", k=2)
print("\n=== 시스템 프롬프트 ===\n" + SYSTEM_PROMPT)
print("\n=== [문서] 절 (k=2, 앞 500자) ===\n" + format_context(hits)[:500] + " …")
