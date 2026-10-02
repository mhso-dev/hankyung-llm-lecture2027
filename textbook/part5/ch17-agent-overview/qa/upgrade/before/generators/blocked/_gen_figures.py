"""Ch 17 절별 SVG와 Excalidraw 정본을 같은 요소에서 생성합니다."""

from __future__ import annotations

# 개선 전(2026-09-10) 생성기입니다. 지금 교재·노트북은 이 파일이 만들지 않습니다.
# 실행하면 figures/0N-흐름.* 그림 열다섯 개를 옛 판으로 덮어씁니다. 읽기 자료로만 둡니다.
# 절 생성기는 textbook/part5/ch17-agent-overview/qa/upgrade/author_NN.py입니다.
raise SystemExit("개선 전 생성기입니다. textbook/part5/ch17-agent-overview/qa/upgrade/author_NN.py를 쓰세요.")

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLORS = {"data": "#DDEDE8", "code": "#DDEAF4", "model": "#E9E0F3", "metric": "#F7EDC7"}

FIGURES = {
    "01-흐름": [
        ("a", "입력과 현재 상태", "data"), ("b", "다음 단계 결정", "model"),
        ("c", "코드 경로 또는 모델 선택", "code"), ("d", "관찰 결과", "data"),
    ],
    "02-흐름": [
        ("a", "현재 실패 증거", "data"), ("b", "경로 예측 가능성", "code"),
        ("c", "워크플로우 우선", "code"), ("d", "품질·비용 비교 계획", "metric"),
    ],
    "03-흐름": [
        ("a", "모델의 다음 행동", "model"), ("b", "도구 실행과 결과", "data"),
        ("c", "상태 갱신", "data"), ("d", "완료·상한·사람 확인", "metric"),
    ],
    "04-흐름": [
        ("a", "한 요청의 궤적", "data"), ("b", "단계·반복", "code"),
        ("c", "비용·지연", "metric"), ("d", "원인 위치와 평가", "metric"),
    ],
    "05-흐름": [
        ("a", "공식 공개 추적 단서", "data"), ("b", "모델·코드·미확인 구분", "code"),
        ("c", "중간 프로젝트 진단", "data"), ("d", "구조 선택과 다음 측정", "metric"),
    ],
}


def common(ident: str, kind: str, x: int, y: int, w: int, h: int) -> dict:
    return {
        "id": ident, "type": kind, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": "#334155", "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid", "roughness": 0,
        "opacity": 100, "groupIds": [], "frameId": None, "roundness": None, "seed": 17,
        "version": 1, "versionNonce": 1, "isDeleted": False, "boundElements": [],
        "updated": 1, "link": None, "locked": False,
    }


def make(name: str, nodes: list[tuple[str, str, str]]) -> tuple[str, dict]:
    elements, shapes = [], []
    positions = {}
    for row, (ident, label, role) in enumerate(nodes):
        x, y, w, h = 20, 18 + row * 112, 320, 68
        positions[ident] = (x, y, w, h)
        box = common(f"{name}-{ident}", "rectangle", x, y, w, h)
        box.update(backgroundColor=COLORS[role], roundness={"type": 3})
        elements.append(box)
        text = common(f"{name}-{ident}-text", "text", x + 10, y + 19, w - 20, 30)
        text.update(strokeColor="#172033", text=label, originalText=label, fontSize=20,
                    fontFamily=1, textAlign="center", verticalAlign="middle", containerId=None,
                    autoResize=True, lineHeight=1.3)
        elements.append(text)
        shapes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{COLORS[role]}" stroke="#334155" stroke-width="2"/>')
        shapes.append(f'<text x="180" y="{y + 42}" text-anchor="middle" font-size="20" font-family="sans-serif" fill="#172033">{html.escape(label)}</text>')
    for row in range(len(nodes) - 1):
        y1, y2 = 86 + row * 112, 126 + row * 112
        arrow = common(f"{name}-edge-{row}", "arrow", 180, y1, 0, y2 - y1)
        arrow.update(points=[[0, 0], [0, y2 - y1]], startArrowhead=None, endArrowhead="arrow",
                     startBinding=None, endBinding=None, elbowed=False)
        elements.append(arrow)
        shapes.append(f'<path d="M180 {y1} L180 {y2}" stroke="#334155" stroke-width="2" marker-end="url(#{name}-arrow)"/>')
    height = 18 + len(nodes) * 112 - 44
    title = " → ".join(label for _, label, _ in nodes)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 {height}" style="width:360px;max-width:100%;height:auto;display:block;margin:0 auto" role="img" aria-label="{html.escape(title, quote=True)}"><title>{html.escape(title)}</title><defs><marker id="{name}-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#334155"/></marker></defs>' + "".join(shapes) + "</svg>")
    drawing = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
               "elements": elements, "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"}, "files": {}}
    return svg, drawing


def main() -> None:
    for name, nodes in FIGURES.items():
        svg, drawing = make(name, nodes)
        (HERE / f"{name}.svg").write_text(svg, encoding="utf-8")
        (HERE / f"{name}.excalidraw").write_text(json.dumps(drawing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        caption = "초록은 입력과 관찰 자료, 파랑은 코드로 정한 처리와 제한, 보라는 모델 판단, 노랑은 측정과 평가를 나타냅니다. 화살표는 실행 또는 판단 자료가 이어지는 방향입니다.\n"
        (HERE / f"{name}.caption.md").write_text(caption, encoding="utf-8")
    print("5 figures generated")


if __name__ == "__main__":
    main()
