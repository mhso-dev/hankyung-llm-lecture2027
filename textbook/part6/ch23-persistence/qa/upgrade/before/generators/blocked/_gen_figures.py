"""Generate Ch23/Ch24 diagrams with the established Part 5 renderer."""
# 개선 전(2026-09-14) Ch 23 그림 생성기입니다. 지금 교재 그림(Mermaid·삽화)은 이 파일이 만들지 않습니다.
# 실행하면 figures/NN-흐름.{svg,excalidraw,caption.md}를 옛 판으로 덮어씁니다. 읽기 자료로만 둡니다.
# 절 생성기는 textbook/part6/ch23-persistence/qa/upgrade/author_NN.py입니다.
raise SystemExit("개선 전 그림 생성기입니다. textbook/part6/ch23-persistence/qa/upgrade/author_NN.py를 쓰세요.")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "part5"))
from _figure import linear, render
HERE = Path(__file__).resolve().parent
RAW = {
    '01-흐름': ([('입력 + thread_id', 'code'), ('체크포인트 저장', 'code'), ('같은 스레드 재개', 'code'), ('다른 스레드 격리', 'code')], 'thread_id가 관련 체크포인트를 묶어 같은 스레드의 상태만 이어 줍니다.'),
    '02-흐름': ([('PostgreSQL 연결', 'data'), ('PostgresSaver.setup', 'code'), ('체크포인트 표', 'data'), ('그래프 실행 저장', 'code')], 'setup이 스키마를 준비한 뒤 그래프 실행이 체크포인트와 중간 쓰기를 저장합니다.'),
    '03-흐름': ([('프로세스 1 실행', 'code'), ('SQLite 체크포인트', 'data'), ('프로세스 1 종료', 'code'), ('프로세스 2 재개', 'code')], '프로세스 객체가 달라져도 같은 저장소와 thread_id로 상태를 이어 갑니다.'),
    '04-흐름': ([('노드 1 완료', 'code'), ('sync: 저장 후 이동', 'code'), ('async: 저장과 다음 노드 겹침', 'code'), ('exit: 종료 시 저장', 'code')], '세 내구 실행 모드는 저장 완료와 다음 노드 실행의 순서를 다르게 정합니다.'),
    '05-흐름': ([('같은 단계 병렬 실행', 'code'), ('good 성공 → pending write', 'code'), ('flaky 실패', 'failure'), ('재개: flaky만 재실행', 'code')], 'pending write가 성공한 병렬 노드의 결과를 보존해 재개 시 중복 실행을 줄입니다.'),
    '06-흐름': ([('외부 쓰기', 'tool'), ('상태 반환 전 종료', 'failure'), ('노드 처음부터 재시작', 'code'), ('operation_id로 중복 차단', 'code')], '노드는 처음부터 재시작되므로 외부 쓰기는 operation_id를 사용해 멱등하게 처리합니다.')}
if __name__ == "__main__":
    for name, (items, caption) in RAW.items():
        render(HERE, name, linear(items, caption))
    print(f"generated {len(RAW)} SVG/Excalidraw pairs")
