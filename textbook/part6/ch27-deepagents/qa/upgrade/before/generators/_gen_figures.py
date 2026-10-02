"""Generate the eight Ch27 diagrams from the shared Part 5 renderer."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "part5"))
from _figure import linear, render

HERE = Path(__file__).resolve().parent

SPECS = {
    "01-흐름": linear([("LangChain create_agent", "code"), ("DeepAgents 하네스", "code"), ("7개 기능", "data"), ("모델·도구 반복", "model")], "프레임워크 위에 하네스 기능을 조립해 모델과 도구가 반복하는 긴 작업을 실행합니다."),
    "02-흐름": linear([("create_deep_agent", "code"), ("백엔드·미들웨어", "code"), ("파일·위임 도구", "tool"), ("CompiledStateGraph", "data")], "생성 함수가 백엔드와 미들웨어를 조립해 실행 그래프를 반환합니다."),
    "03-흐름": linear([("0.6 기본 플래닝", "code"), ("0.7 opt-in", "code"), ("빈 작성 프롬프트", "data"), ("첫 턴 토큰 측정", "metric")], "0.7에서는 플래닝을 선택해 추가하며 프롬프트 변화의 효과는 정해진 조건에서 측정합니다."),
    "04-흐름": linear([("조사 원문", "data"), ("write_file", "tool"), ("/research/*.md", "data"), ("read_file로 다시 읽기", "tool")], "조사 원문에서 추출한 중간 결과를 파일에 저장하고 경로로 다시 읽습니다."),
    "05-흐름": linear([("긴 대화·큰 도구 결과", "data"), ("요약 또는 오프로딩", "tool"), ("요약 메시지·파일 경로", "data"), ("다음 모델 호출", "model")], "긴 대화는 요약하고 큰 도구 결과는 파일로 옮겨 다음 모델 호출의 입력을 관리합니다."),
    "06-흐름": linear([("부모의 완료 조건", "data"), ("task 위임", "tool"), ("격리된 조사 문맥", "data"), ("최종 보고 반환", "data")], "부모가 완료 조건을 전달하면 서브에이전트가 별도 문맥에서 조사하고 보고를 반환합니다."),
    "07-흐름": linear([("검증된 제공 자료", "data"), ("source_lookup", "tool"), ("source-reviewer의 모델 판단", "model"), ("/research/final.md", "data")], "이 실습은 제공한 공식 자료만 조회하고 근거·범위·출처 식별자를 파일에 저장합니다."),
    "08-흐름": linear([("경로별 권한 규칙", "data"), ("통합 실행 코드", "code"), ("파일·ToolMessage 검사", "metric"), ("종료 판정", "data")], "허용된 파일과 거부된 도구 결과를 함께 검사해 종료를 판정합니다."),
}

if __name__ == "__main__":
    for name, spec in SPECS.items():
        render(HERE, name, spec)
    print(f"generated {len(SPECS)} SVG/Excalidraw pairs")
