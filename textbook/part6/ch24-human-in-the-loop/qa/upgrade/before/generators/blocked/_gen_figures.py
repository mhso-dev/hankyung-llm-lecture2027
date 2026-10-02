"""Generate Ch23/Ch24 diagrams with the established Part 5 renderer."""
# 개선 전(2026-09-14) Ch 24 그림 생성기입니다. 지금 교재 그림(Mermaid·삽화)은 이 파일이 만들지 않습니다.
# 실행하면 figures/NN-흐름.{svg,excalidraw,caption.md}를 옛 판으로 덮어씁니다. 읽기 자료로만 둡니다.
# 절 생성기는 textbook/part6/ch24-human-in-the-loop/qa/upgrade/author_NN.py입니다.
raise SystemExit("개선 전 그림 생성기입니다. textbook/part6/ch24-human-in-the-loop/qa/upgrade/author_NN.py를 쓰세요.")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "part5"))
from _figure import linear, render
HERE = Path(__file__).resolve().parent
RAW = {
    '01-흐름': ([('요청 상태 저장', 'code'), ('interrupt 승인 질문', 'code'), ('사람의 승인/거절', 'data'), ('승인일 때만 로컬 쓰기', 'tool')], '승인 게이트를 부작용 앞에 두어 거절된 요청의 쓰기를 막습니다.'),
    '02-흐름': ([('interrupt에서 중단', 'code'), ('Command(resume=값)', 'code'), ('노드 처음부터 재실행', 'code'), ('검증 뒤 완료 또는 재질문', 'code')], 'Command의 값이 같은 스레드의 interrupt 반환값으로 전달됩니다.'),
    '03-흐름': ([('get_state_history', 'code'), ('과거 체크포인트 선택', 'code'), ('update_state로 값 변경', 'code'), ('새 분기 invoke', 'code')], '과거 상태를 갱신하면 원본을 보존한 다른 분기에서 후속 노드를 다시 실행합니다.')}
if __name__ == "__main__":
    for name, (items, caption) in RAW.items():
        render(HERE, name, linear(items, caption))
    print(f"generated {len(RAW)} SVG/Excalidraw pairs")
