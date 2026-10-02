# 2026-09-25 Ch 25 01절 품질 개선: 옛 그림(0N-흐름.svg·.excalidraw·.caption.md)을 만드는 옛 생성기입니다.
# 개선본 그림은 qa/upgrade/author_NN.py와 figures/NN-k-*.mmd(Mermaid)·삽화가 대신합니다.
# 이 파일을 실행하면 옛 그림을 다시 쓰므로, 아래 줄에서 실행을 막습니다. 옮기기(mv -n)는 챕터 마감 몫입니다.
raise SystemExit("옛 Ch 25 그림 생성기입니다. 개선본 그림은 qa/upgrade/author_NN.py와 figures/NN-k-*.mmd를 쓰세요.")
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "part5"))
from _figure import linear, render

SPECS = {
    "01-흐름": linear([("그래프 실행", "code"), ("7개 stream mode", "data"), ("화면·로그 소비자", "metric")], "같은 그래프 실행을 일곱 stream mode로 관찰하는 흐름"),
    "02-흐름": linear([("모델 노드 실행", "model"), ("messages · updates · custom", "data"), ("답변 조각 · 단계 · 진행률", "metric")], "답변 조각, 노드 변경분, 사용자 정의 진행 상황을 구분하는 흐름"),
    "03-흐름": linear([("같은 질문·모델", "code"), ("updates · messages · custom", "data"), ("first_event · TTFT · total", "metric")], "같은 입력으로 세 번 호출하여 첫 사건과 전체 시간을 측정하고 messages에서 첫 답변 조각의 도착 시간을 측정하는 흐름"),
}

for name, spec in SPECS.items():
    render(HERE, name, spec)
