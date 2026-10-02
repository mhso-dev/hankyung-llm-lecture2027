"""05절 — 첫 실패를 일부러 본다.

1) 검색이 엉뚱한 청크를 가져왔는데 모델이 그럴듯한 숫자를 만들어 내는가 (환각)
2) "모르면 모른다고 하라"로 막히는가
3) 그것으로 부족한 경우 — 답이 문서에 있는데도 "찾을 수 없습니다"가 나온다
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _index import get_store

from rag import generate, search

store = get_store()

HELPFUL = """당신은 친절한 고객 안내 도우미입니다.
아래 [문서]를 참고해 고객이 만족하도록 구체적으로 답하세요."""

STRICT = """당신은 사내 문서 안내 담당자입니다. 아래 [문서] 절만 근거로 한국어로 답하세요.
답의 근거가 된 문장 뒤에 [doc_id p.페이지] 형식으로 출처를 붙이세요.
[문서]에 답이 없으면 추측하지 말고 정확히 "문서에서 찾을 수 없습니다"라고만 답하세요."""


def run(label: str, question: str, system_prompt: str, k: int = 4) -> None:
    hits = search(store, question, k=k)
    res = generate(question, hits, system_prompt=system_prompt)
    print(f"\n[{label}] {question}")
    print("  검색:", [f"{d.metadata['doc_id']} p.{d.metadata['page']}" for d, _ in hits])
    print("  답변:", res.text.replace("\n", " ")[:300])


print("### 1. 검색이 빗나간 질문 — 친절한 프롬프트 (k=2), 같은 질문 5회")
Q = "누리테크 A/S 접수 후 답변은 얼마나 걸리나요?"  # 문서 어디에도 답변 소요 시간은 없다
hits = search(store, Q, k=2)
print("  검색:", [f"{d.metadata['doc_id']} p.{d.metadata['page']}" for d, _ in hits])
made_up = 0
for i in range(5):
    text = generate(Q, hits, system_prompt=HELPFUL).text.replace("\n", " ")
    fabricated = "일 이내" in text or "시간 이내" in text
    made_up += fabricated
    print(f"  {i + 1}회 {'환각' if fabricated else '회피'}: {text[:110]}…")
print(f"  → 5회 중 {made_up}회가 문서에 없는 기한을 지어냈습니다")

print("\n### 2. 같은 질문 — '모르면 모른다' 지시")
run("strict", "누리테크 A/S 접수 후 답변은 얼마나 걸리나요?", STRICT, k=2)
run("strict", "미르시립도서관의 2025년 연간 방문자 수는?", STRICT, k=2)

print("\n### 3. 답이 문서에 있는데도 '찾을 수 없습니다'가 나오는 경우")
run("strict", "책을 3일 늦게 반납하면 어떤 불이익이 있나요?", STRICT)  # E01 p.3에 있음
run(
    "strict", "2024년에 발생한 누리테크 직원의 미사용 연차 4일은 어떻게 처리되나요?", STRICT
)  # M05 부칙에 있음
