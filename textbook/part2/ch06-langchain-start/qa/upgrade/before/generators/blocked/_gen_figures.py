"""의미 기반 SVG와 편집 가능한 Excalidraw 원본을 생성합니다."""

from __future__ import annotations

raise SystemExit("옛 도식 생성기 — 품질 개선 뒤 실행 금지. 지금 판 그림은 figures/*.mmd를 textbook/_notebook/mermaid/render_mermaid.py로 렌더하고, 절 생성기는 qa/upgrade/author_*.py")

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
C = {
    "g": "#DDEDE8",
    "b": "#DDEAF4",
    "p": "#E9E0F3",
    "y": "#F7EDC7",
    "r": "#F4D9D5",
    "i": "#252522",
    "l": "#5B5B55",
}


def box(x, y, w, h, label, color, ident):
    label_y = y + 20 if ident in {"loop", "harness", "context"} else y + h / 2
    if "|" in label:
        first, second = label.split("|", 1)
        visible = f'<tspan x="{x + w / 2}" dy="-5">{first}</tspan><tspan x="{x + w / 2}" dy="20">{second}</tspan>'
    else:
        visible = label
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="11" fill="{C[color]}" stroke="{C["l"]}" stroke-width="2"/><text x="{x + w / 2}" y="{label_y}" text-anchor="middle" font-family="sans-serif" font-size="15" fill="{C["i"]}">{visible}</text>'
    base = {
        "type": "rectangle",
        "version": 1,
        "versionNonce": 1,
        "index": "a0",
        "isDeleted": False,
        "id": ident,
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": C["l"],
        "backgroundColor": C[color],
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 3},
        "seed": 1,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
    }
    plain = label.replace("|", "\n")
    text = {
        "type": "text",
        "version": 1,
        "versionNonce": 2,
        "index": "a1",
        "isDeleted": False,
        "id": ident + "-text",
        "x": x + 8,
        "y": label_y - 12,
        "width": w - 16,
        "height": 40 if "|" in label else 20,
        "angle": 0,
        "strokeColor": C["i"],
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": 2,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
        "fontSize": 15,
        "fontFamily": 1,
        "text": plain,
        "textAlign": "center",
        "verticalAlign": "middle",
        "containerId": ident,
        "originalText": plain,
        "autoResize": True,
        "lineHeight": 1.25,
    }
    return s, [base, text]


def arrow(x1, y1, x2, y2, ident, dash=False):
    dash_attr = 'stroke-dasharray="7 5"' if dash else ""
    s = f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{C["l"]}" stroke-width="2.5" {dash_attr} marker-end="url(#arr)"/>'
    bx, by = min(x1, x2), min(y1, y2)
    e = {
        "type": "arrow",
        "version": 1,
        "versionNonce": 3,
        "index": "a2",
        "isDeleted": False,
        "id": ident,
        "x": bx,
        "y": by,
        "width": abs(x2 - x1),
        "height": abs(y2 - y1),
        "angle": 0,
        "strokeColor": C["l"],
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "dashed" if dash else "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 2},
        "seed": 3,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
        "points": [[x1 - bx, y1 - by], [x2 - bx, y2 - by]],
        "lastCommittedPoint": None,
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": None,
        "endArrowhead": "arrow",
        "elbowed": False,
    }
    return s, [e]


def build(name, title, desc, boxes, arrows):
    parts = []
    elements = []
    for item in boxes:
        s, e = box(*item)
        parts.append(s)
        elements += e
    for item in arrows:
        s, e = arrow(*item)
        parts.append(s)
        elements += e
    legend = f'<rect x="25" y="365" width="15" height="15" fill="{C["g"]}"/><text x="46" y="379" font-size="15">입력·맥락</text><rect x="155" y="365" width="15" height="15" fill="{C["b"]}"/><text x="176" y="379" font-size="15">프로그램 흐름</text><rect x="320" y="365" width="15" height="15" fill="{C["p"]}"/><text x="341" y="379" font-size="15">모델·응답</text><rect x="465" y="365" width="15" height="15" fill="{C["y"]}"/><text x="486" y="379" font-size="15">측정·검증</text><rect x="620" y="365" width="15" height="15" fill="{C["r"]}"/><text x="641" y="379" font-size="15">오류</text>'
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 410" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">{desc}</desc><defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{C["l"]}"/></marker></defs><rect width="800" height="410" fill="#fff"/><text x="400" y="32" text-anchor="middle" font-family="sans-serif" font-size="21" font-weight="700">{title}</text>{"".join(parts)}{legend}</svg>'
    (HERE / f"{name}.svg").write_text(svg, encoding="utf-8")
    data = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
        "files": {},
    }
    (HERE / f"{name}.excalidraw").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


build(
    "01-layer-map",
    "용어 포함 관계와 제품 계층",
    "왼쪽은 네 용어의 포함 관계, 오른쪽은 세 제품의 역할입니다.",
    [
        (45, 55, 440, 275, "루프(loop)", "b", "loop"),
        (70, 80, 390, 225, "하네스(harness)", "b", "harness"),
        (95, 105, 340, 175, "컨텍스트(context)", "g", "context"),
        (120, 130, 290, 125, "프롬프트(prompt)", "g", "prompt"),
        (535, 65, 215, 58, "LangGraph · 런타임", "b", "lg"),
        (535, 150, 215, 58, "LangChain · 프레임워크", "b", "lc"),
        (535, 235, 215, 58, "DeepAgents · 하네스", "b", "da"),
    ],
    [],
)
build(
    "02-provider-switch",
    "같은 메시지와 세 provider",
    "한 메시지가 세 제공자로 갈라졌다가 AIMessage 경계로 모입니다.",
    [
        (20, 150, 120, 64, "같은 메시지", "g", "msg"),
        (180, 150, 130, 64, "init_chat_model", "b", "init"),
        (365, 55, 135, 58, "OpenAI", "p", "o"),
        (365, 150, 135, 58, "Anthropic", "p", "a"),
        (365, 245, 135, 58, "Google", "p", "gg"),
        (650, 150, 125, 64, "AIMessage", "p", "ai"),
    ],
    [
        (140, 182, 180, 182, "m-i", False),
        (310, 182, 365, 84, "o1", False),
        (310, 182, 365, 179, "a1", False),
        (310, 182, 365, 274, "g1", False),
        (500, 84, 650, 182, "o2", False),
        (500, 179, 650, 182, "a2", False),
        (500, 274, 650, 182, "g2", False),
    ],
)
build(
    "03-structured-output",
    "스키마가 생성과 검증에 적용되는 위치",
    "스키마가 모델 출력 형식을 제시하고 응답을 검증한 뒤 StudyCard 객체로 만듭니다.",
    [
        (25, 150, 135, 62, "자연어 요청", "g", "req"),
        (230, 150, 140, 62, "채팅 모델", "p", "model"),
        (440, 150, 150, 62, "파싱 · 필드 검증", "y", "valid"),
        (650, 150, 125, 62, "StudyCard", "p", "parsed"),
        (335, 55, 150, 58, "Pydantic 스키마", "y", "schema"),
    ],
    [
        (160, 181, 230, 181, "r-m", False),
        (370, 181, 440, 181, "m-v", False),
        (590, 181, 650, 181, "v-p", False),
        (410, 113, 300, 150, "s-m", True),
        (410, 113, 515, 150, "s-v", True),
    ],
)
build(
    "04-streaming",
    "청크를 결합한 뒤 최종 표현 읽기",
    "청크를 결합한 후 text와 content_blocks를 각각 읽습니다.",
    [
        (30, 150, 125, 62, "질문", "g", "q"),
        (240, 150, 175, 62, "AIMessageChunk들", "p", "chunks"),
        (500, 150, 235, 62, "결합된 AIMessageChunk", "p", "combined"),
        (500, 255, 235, 58, "text · content_blocks", "y", "views"),
    ],
    [
        (155, 181, 240, 181, "q-c", False),
        (415, 181, 500, 181, "c-co", False),
        (618, 212, 618, 255, "co-v", True),
    ],
)
build(
    "05-resilience",
    "재시도와 폴백의 다른 경로",
    "재시도는 같은 호출로 돌아가고 폴백은 대체 경로로 이동합니다.",
    [
        (35, 150, 125, 62, "기본 호출", "b", "call"),
        (250, 150, 145, 62, "일시 오류", "r", "err"),
        (520, 65, 195, 62, "제한된 재시도", "b", "retry"),
        (520, 240, 195, 62, "폴백", "b", "fallback"),
    ],
    [
        (160, 181, 250, 181, "c-e", False),
        (395, 165, 520, 96, "e-r", False),
        (618, 127, 98, 150, "r-back", True),
        (395, 197, 520, 271, "e-f", False),
    ],
)
build(
    "06-observation",
    "같은 과제의 제공자별 측정",
    "동일 과제를 세 제공자에 보내고 실행 상태와 토큰, 지연, 비용을 기록합니다.",
    [
        (30, 150, 130, 62, "동일 과제", "g", "task"),
        (245, 55, 140, 58, "OpenAI", "p", "mo"),
        (245, 150, 140, 58, "Anthropic", "p", "ma"),
        (245, 245, 140, 58, "Google", "p", "mg"),
        (555, 70, 205, 220, "토큰 · 지연 · 비용|실행 상태 포함", "y", "measure"),
    ],
    [
        (160, 181, 245, 84, "t-o", False),
        (160, 181, 245, 179, "t-a", False),
        (160, 181, 245, 274, "t-g", False),
        (385, 84, 555, 105, "o-row", False),
        (385, 179, 555, 180, "a-row", False),
        (385, 274, 555, 255, "g-row", False),
    ],
)
print("wrote 6 SVG and Excalidraw pairs")
