"""Ch21 개념 도식을 SVG와 Excalidraw JSON으로 생성합니다."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "part5"))
from _figure import linear, render

HERE = Path(__file__).resolve().parent
SPECS = {
    "01-흐름": linear([("사용자 질문", "data"), ("model", "model"), ("도구 선택", "model"), ("ToolNode", "tool"), ("model 또는 END", "model")], "create_agent가 구성한 ReAct 루프입니다. 모델이 도구 호출을 만들면 ToolNode가 실행하고, 호출이 없으면 종료합니다."),
    "02-흐름": linear([("출력 스키마", "data"), ("ToolStrategy", "code"), ("ProviderStrategy", "model"), ("structured_response", "metric")], "두 전략은 스키마를 강제하는 위치가 다르지만 검증된 결과는 structured_response 상태 키로 반환합니다."),
    "03-흐름": linear([("invoke 입력", "data"), ("AgentState 누적", "code"), ("context 주입", "data"), ("도구가 context 읽기", "tool"), ("최종 상태", "metric")], "AgentState는 실행 결과에 남고 context는 호출 동안 도구와 미들웨어가 읽습니다."),
    "04-흐름": linear([("0.x API 목록", "data"), ("이름·형식 대조", "code"), ("v1 create_agent", "model"), ("회귀 실행", "metric")], "이전 호출을 현재 API 서명과 대조한 뒤 같은 입력으로 회귀 검사를 실행합니다."),
    "05-흐름": linear([("질문", "data"), ("검색 여부 판단", "model"), ("search_rules", "tool"), ("재검색 판단", "model"), ("근거 답 또는 모름", "data")], "Agentic RAG에서는 모델이 검색 여부와 재검색 여부를 정하고 근거가 없으면 제한을 설명합니다."),
    "06-흐름": linear([("같은 평가셋", "data"), ("고정 RAG", "code"), ("Agentic RAG", "model"), ("정확도·토큰·지연", "metric")], "같은 질문과 자료를 두 경로에 입력하고 정확도, 토큰, 지연, 실패 양상을 같은 열로 비교합니다."),
}
if __name__ == "__main__":
    for name, spec in SPECS.items():
        render(HERE, name, spec)
    print("generated", len(SPECS))
