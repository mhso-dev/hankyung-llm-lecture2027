# 2026-09-29 Ch 30 01절 품질 개선: 옛 도식(NN-흐름.svg·.excalidraw·.caption.md 스물일곱)을 만드는 옛 생성기입니다.
# 개선본 그림은 절마다 figures/NN-k-이름.mmd(Mermaid)와 삽화 PNG가 대신합니다(QUALITY-UPGRADE.md §5·§8). 이 파일을 실행하면 옛 그림을 다시 쓰려 하므로, 아래 줄에서 실행을 막습니다.
# 내용은 고치지 않았습니다(이 설명 세 줄과 아래 한 줄만 더함). 옮기기(mv -n)는 챕터 마감 몫입니다(Part 7 qa/check_figures.py가 이 파일이 있는지 봅니다 — 마감 때 함께 판단).
"""Ch30 서비스 경계 도식을 SVG와 Excalidraw JSON으로 생성합니다."""
raise SystemExit('옛 Ch 30 도식 생성기입니다. 개선본 그림은 figures/NN-k-이름.mmd와 삽화 PNG를 쓰세요.')
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "part5"))
from _figure import linear, render

HERE = Path(__file__).resolve().parent
SPECS = {
    "01-흐름": linear([("HTTP 요청", "data"), ("Pydantic 검증", "code"), ("async 라우트", "code"), ("JSON 응답", "data")], "요청 본문이 스키마 검증을 통과한 뒤 비동기 라우트에서 처리되어 응답으로 반환됩니다."),
    "02-흐름": linear([("라우트", "code"), ("Depends", "code"), ("Agent 제공자", "model"), ("테스트 대체", "metric")], "Depends가 라우트에 Agent 객체를 제공하며 테스트에서는 같은 자리를 대체 객체로 바꿉니다."),
    "03-흐름": linear([("ChatRequest", "data"), ("ainvoke", "model"), ("최종 상태", "data"), ("ChatResponse", "data")], "요청 스키마의 질문이 Agent 상태가 되고 ainvoke의 최종 상태에서 답을 골라 응답 스키마로 반환합니다."),
    "04-흐름": linear([("질문 상태", "data"), ("astream", "model"), ("token 조각", "data"), ("클라이언트 표시", "metric")], "astream이 생성 중 기록한 조각을 차례로 전달하므로 클라이언트는 최종 완료 전부터 내용을 표시할 수 있습니다."),
    "05-흐름": linear([("POST 본문", "data"), ("SSE 연결", "code"), ("token id data", "data"), ("done", "metric")], "POST 요청 하나가 SSE 연결을 열고 식별자가 있는 token 이벤트 뒤에 완료 이벤트를 전송합니다."),
    "06-흐름": linear([("마지막 id 저장", "data"), ("fetch 재요청", "code"), ("Last-Event-ID", "data"), ("다음 이벤트", "metric")], "브라우저 클라이언트가 마지막 식별자를 저장하고 POST 재요청 헤더에 실어 서버가 다음 이벤트부터 전송하게 합니다."),
    "07-흐름": linear([("브라우저 출처", "data"), ("CORS", "code"), ("Bearer Depends", "code"), ("timeout", "metric")], "허용한 출처와 인증을 통과한 요청만 Agent 호출로 이어지고 시간 상한을 넘으면 명시적인 결과로 끝납니다."),
    "08-흐름": linear([("Pydantic 모델", "data"), ("OpenAPI", "code"), ("SDK 생성기", "code"), ("TypeScript 호출", "metric")], "백엔드 모델과 라우트 선언에서 OpenAPI가 생성되고 같은 문서로 TypeScript 클라이언트 코드를 만듭니다."),
    "09-흐름": linear([("HTTP 질문", "data"), ("create_agent", "model"), ("운영시간 도구", "code"), ("모델 token SSE", "metric")], "실제 OpenAI 모델 Agent가 운영 시간 도구를 호출하고 ainvoke 응답과 astream token 이벤트를 HTTP로 반환합니다."),
}

if __name__ == "__main__":
    for name, spec in SPECS.items():
        render(HERE, name, spec)
    print("generated", len(SPECS))
