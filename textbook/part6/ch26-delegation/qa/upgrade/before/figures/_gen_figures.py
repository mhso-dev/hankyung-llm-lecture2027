from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "part5"))
from _figure import linear, render

SPECS = {
    "01-흐름": linear([("사용자 요청", "data"), ("중앙 에이전트", "model"), ("전문 에이전트 도구", "tool"), ("최종 답변", "metric")], "중앙 에이전트가 전문 에이전트를 도구로 호출하는 흐름"),
    "02-흐름": linear([("사용자 턴", "data"), ("active_agent 변경", "code"), ("체크포인트 저장", "tool"), ("다음 턴 이어가기", "metric")], "Handoff가 활성 담당자 상태를 저장하고 다음 턴으로 이어지는 흐름"),
    "03-흐름": linear([("요청 분류", "model"), ("복수 전문 경로", "code"), ("병렬 실행", "tool"), ("결과 종합", "metric")], "Router가 입력을 분류하고 선택된 전문 경로를 병렬 실행하는 흐름"),
    "04-흐름": linear([("같은 고객 과제", "data"), ("세 위임 구조", "model"), ("실제 API 호출 계측", "code"), ("호출 수·비용·종료 조건", "metric")], "같은 과제를 세 위임 구조로 실행하고 비용과 종료 조건을 비교하는 흐름"),
}

for name, spec in SPECS.items():
    render(HERE, name, spec)
