"""Generate matching SVG and editable Excalidraw sources for Ch 5."""

from __future__ import annotations

raise SystemExit("옛 도식 생성기 — 품질 개선 뒤 실행 금지. 지금 판 그림은 figures/*.mmd를 textbook/_notebook/mermaid/render_mermaid.py로 렌더하고, 절 생성기는 qa/upgrade/author_*.py")

import json
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent

DIAGRAMS = {
    "01-concept": [("문장", "#dcfce7"), ("토큰화기", "#dcfce7"), ("토큰 ID 열", "#dcfce7"), ("토큰 수 측정", "#fef3c7")],
    "02-concept": [("문장 4개", "#dcfce7"), ("384차원 벡터", "#dcfce7"), ("코사인 유사도", "#fef3c7"), ("순서·간격 확인", "#fef3c7")],
    "03-concept": [("입력 토큰", "#dcfce7"), ("관련성 비중", "#dbeafe"), ("정보 표현", "#dcfce7"), ("가중치=이유 아님", "#fee2e2")],
    "04-concept": [("총 512", "#dcfce7"), ("출력 64 예약", "#dbeafe"), ("입력 448", "#fef3c7"), ("실제 토큰 측정", "#fef3c7")],
    "05-concept": [("3개 길이", "#dbeafe"), ("3개 위치", "#dbeafe"), ("9개 조건 생성", "#dcfce7"), ("위치 차이 관찰", "#fef3c7")],
    "06-temperature-sampling": [("동일 프롬프트", "#dcfce7"), ("T=0.3 / T=1.0", "#dbeafe"), ("각 3회 샘플링", "#ede9fe"), ("둘 다 3/3 서로 다름", "#fef3c7")],
    "07-hallucination-conditions": [("근거 없는 질문", "#dcfce7"), ("다음 토큰 예측", "#ede9fe"), ("추측/불확실 표현", "#ede9fe"), ("근거 확인 필요", "#fee2e2")],
    "08-model-selection": [("작업·라이선스", "#dcfce7"), ("필수 조건 필터", "#dbeafe"), ("후보 모델", "#dcfce7"), ("자체 평가 필요", "#fef3c7")],
}

for name, boxes in DIAGRAMS.items():
    width, height = 800, 210
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
             f'<title id="title">{escape(name)} 개념 도식</title>',
             '<desc id="desc">네 단계를 왼쪽에서 오른쪽으로 읽는 흐름</desc>',
             '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#475569"/></marker></defs>']
    elements = []
    for index, (label, color) in enumerate(boxes):
        x = 20 + index * 195
        parts.append(f'<rect x="{x}" y="55" width="165" height="90" rx="14" fill="{color}" stroke="#334155" stroke-width="2"/>')
        parts.append(f'<text x="{x+82.5}" y="107" text-anchor="middle" font-family="Noto Sans KR, sans-serif" font-size="17" fill="#172033">{escape(label)}</text>')
        elements.append({"id": f"box-{index}", "type": "rectangle", "x": x, "y": 55, "width": 165, "height": 90, "strokeColor": "#334155", "backgroundColor": color})
        elements.append({"id": f"text-{index}", "type": "text", "x": x + 20, "y": 88, "width": 125, "height": 24, "fontSize": 17, "text": label, "originalText": label, "strokeColor": "#172033", "backgroundColor": "transparent", "textAlign": "center", "verticalAlign": "middle", "containerId": f"box-{index}"})
        if index < len(boxes) - 1:
            parts.append(f'<line x1="{x+165}" y1="100" x2="{x+190}" y2="100" stroke="#475569" stroke-width="2" marker-end="url(#arrow)"/>')
            elements.append({"id": f"arrow-{index}", "type": "arrow", "x": x + 165, "y": 100, "width": 25, "height": 0, "strokeColor": "#475569", "backgroundColor": "transparent", "points": [[0, 0], [25, 0]], "endArrowhead": "arrow"})
    parts.append('</svg>')
    (HERE / f"{name}.svg").write_text('\n'.join(parts), encoding="utf-8")
    (HERE / f"{name}.excalidraw").write_text(json.dumps({"type": "excalidraw", "version": 2, "source": "ch05", "elements": elements, "appState": {"viewBackgroundColor": "#ffffff"}, "files": {}}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", name)
