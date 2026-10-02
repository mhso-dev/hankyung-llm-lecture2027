# 2026-09-28 Ch 28 01절 품질 개선: 옛 도식(NN-흐름.svg·.excalidraw·.caption.md 열다섯)을 만드는 옛 생성기입니다.
# 개선본 그림은 절마다 figures/NN-k-이름.mmd(Mermaid)와 삽화 PNG가 대신합니다(QUALITY-UPGRADE.md §5·§8).
# 이 파일을 실행하면 옛 그림을 다시 쓰려 하므로, 아래 줄에서 실행을 막습니다. 옮기기(mv -n)는 챕터 마감 몫입니다.
"""Ch28 도식의 SVG와 Excalidraw 정본을 함께 생성합니다."""
raise SystemExit("옛 Ch 28 도식 생성기입니다. 개선본 그림은 figures/NN-k-이름.mmd와 삽화 PNG를 쓰세요.")

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "textbook/part5"))
from _figure import linear, render  # noqa: E402


HERE = Path(__file__).resolve().parent
SPECS = {
    "01-흐름": linear(
        [("initialize\n버전·capability", "code"), ("tools/list", "tool"), ("resources/list", "data"), ("prompts/list", "data"), ("호출·읽기·가져오기", "tool")],
        "초기화에서 프로토콜 버전과 capability를 협상한 뒤 도구·리소스·프롬프트를 각 목록 메서드로 발견합니다. 발견과 실제 사용은 별도 요청입니다.",
    ),
    "02-흐름": linear(
        [("일반 Python 함수", "code"), ("@mcp.tool 등록", "code"), ("입력 JSON Schema", "data"), ("tools/list 발견", "tool"), ("tools/call 실행", "tool")],
        "FastMCP 장식자는 함수를 서버 구성 요소로 등록합니다. 타입 힌트와 설명에서 도구 정의가 만들어지고 클라이언트는 목록 조회 뒤 도구를 호출합니다.",
    ),
    "03-흐름": {
        "size": (620, 620),
        "caption": "stdio는 클라이언트가 로컬 하위 프로세스를 시작합니다. Streamable HTTP는 별도 원격 서비스에 연결하며 Origin 검증과 인증·사용자별 인가 경계를 설계합니다.",
        "nodes": [("MCP 클라이언트", "code", 170, 20, 280, 60), ("stdio\n로컬 하위 프로세스", "tool", 25, 190, 260, 75), ("Streamable HTTP\n원격 서비스", "tool", 335, 190, 260, 75), ("선택한 환경 변수\n운영체제 권한", "failure", 25, 390, 260, 75), ("TLS·Authorization\n도구별 인가", "failure", 335, 390, 260, 75), ("읽기 전용 결과", "data", 170, 540, 280, 60)],
        "edges": [([(230, 80), (155, 80), (155, 186)],), ([(390, 80), (465, 80), (465, 186)],), ([(155, 265), (155, 386)],), ([(465, 265), (465, 386)],), ([(155, 465), (155, 510), (240, 510), (240, 536)],), ([(465, 465), (465, 510), (380, 510), (380, 536)],)],
    },
    "04-흐름": linear(
        [("course_server.py", "code"), ("MCPAdapter(Path)", "code"), ("list_tools()", "tool"), ("LangChain BaseTool", "tool"), ("ainvoke({topic})", "code")],
        "MCPAdapter는 로컬 서버 파일을 stdio로 연결하고 MCP 도구 정의를 LangChain BaseTool 인터페이스로 변환합니다. 실제 호출은 서버 프로세스로 전달됩니다.",
    ),
    "05-흐름": {
        "size": (620, 650),
        "caption": "같은 질문과 모델에 직접 도구 한 개, MCP 도구 한 개, MCP 도구 다섯 개를 각각 연결합니다. 도구 수·정의 문자 수·첫 모델 호출 입력 토큰을 따로 기록합니다.",
        "nodes": [("같은 질문·모델 호출", "code", 170, 20, 280, 60), ("직접 도구 1개", "code", 20, 165, 180, 65), ("MCP 도구 1개", "tool", 220, 165, 180, 65), ("MCP 도구 5개", "tool", 420, 165, 180, 65), ("JSON Schema\n문자 수", "data", 55, 340, 230, 70), ("첫 호출\ninput_tokens", "metric", 335, 340, 230, 70), ("프로토콜 바이트와\n모델 토큰 구분", "failure", 130, 540, 360, 75)],
        "edges": [([(230, 80), (110, 80), (110, 161)],), ([(310, 80), (310, 161)],), ([(390, 80), (510, 80), (510, 161)],), ([(110, 230), (110, 300), (170, 300), (170, 336)],), ([(310, 230), (310, 280), (450, 280), (450, 336)],), ([(510, 230), (510, 336)],), ([(170, 410), (170, 490), (260, 490), (260, 536)],), ([(450, 410), (450, 490), (360, 490), (360, 536)],)],
    },
}


if __name__ == "__main__":
    for name, spec in SPECS.items():
        render(HERE, name, spec)
    print(f"generated {len(SPECS)} SVG/Excalidraw pairs")
