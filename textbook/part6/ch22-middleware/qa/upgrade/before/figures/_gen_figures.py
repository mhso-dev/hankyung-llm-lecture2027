from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "textbook" / "part5"))
from _figure import linear, render


SPECS = {
    "01-미들웨어와-6개-훅-흐름": linear([
        ("입력 상태", "code"), ("before_agent", "code"), ("모델 전·감싸기·후", "model"),
        ("wrap_tool_call", "tool"), ("after_agent", "code")], "여섯 훅은 에이전트·모델·도구 범위에 놓입니다"),
    "02-PII-마스킹-이식-흐름": linear([
        ("PII 네 유형 원문", "code"), ("Ch16 네 유형 완전 치환", "code"),
        ("PIIMiddleware 이메일 처리", "code"), ("모델 입력·출력", "model")], "직접 함수와 내장 PII 미들웨어의 정책 범위는 다릅니다"),
    "03-요약-압축과-Compress-흐름": linear([
        ("원본 메시지 6개", "code"), ("trigger 메시지 4개", "metric"),
        ("오래된 대화 요약", "model"), ("요약문 + 최근 2개", "code"), ("주 모델", "model")], "임계값을 넘으면 오래된 대화를 요약하고 최근 메시지를 보존합니다"),
    "04-호출-한도와-재시도-폴백-흐름": linear([
        ("모델 요청", "code"), ("호출 한도 검사", "metric"), ("일시적 오류", "failure"),
        ("재시도", "code"), ("보조 모델", "model")], "호출 한도와 재시도와 폴백은 서로 다른 조건을 처리합니다"),
    "05-커스텀-예산-미들웨어-흐름": linear([
        ("요청", "code"), ("예상비용 예약", "metric"), ("handler와 모델", "model"),
        ("상한 초과 차단", "failure")], "커스텀 예산 미들웨어는 모델 호출 전에 예상비용을 예약합니다"),
    "06-커스텀-감사-미들웨어-흐름": linear([
        ("사용자 입력", "code"), ("agent_start 최소 기록", "metric"),
        ("lookup_hours", "tool"), ("tool_success 최소 기록", "metric"), ("agent_end", "metric")], "감사 이벤트에는 원문과 도구 결과를 저장하지 않습니다"),
    "07-순서와-합성-흐름": linear([
        ("목록 A · B · C", "code"), ("before A → B → C", "code"),
        ("A(B(C(model)))", "model"), ("after C → B → A", "code")], "before는 순방향이고 wrap과 after 반환은 역방향입니다"),
    "08-컨텍스트-분리와-Isolate-흐름": linear([
        ("loan 3 + hr 2 상태", "code"), ("topic=loan 선택", "code"),
        ("loan 메시지 3개 요청", "code"), ("모델", "model"), ("hr 입력 제외", "failure")], "업무별 메시지 선택은 모델 요청 범위를 줄입니다"),
}


if __name__ == "__main__":
    HERE.mkdir(parents=True, exist_ok=True)
    for name, spec in SPECS.items():
        # 390px 화면의 본문 안쪽 폭에 맞춰 루트 가로 넘침을 막습니다.
        spec["size"] = (360, spec["size"][1])
        render(HERE, name, spec)
        print("wrote", name)
