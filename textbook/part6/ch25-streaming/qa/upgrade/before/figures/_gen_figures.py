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
