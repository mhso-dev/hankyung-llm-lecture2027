"""Ch 8 도식 생성기 — 같은 요소 목록에서 Excalidraw와 SVG를 함께 만든다.

색 규칙(AGENTS.md §16): 학생 흐름=파랑, 모델 판단=보라, 도구·데이터=초록,
측정=노랑, 실패=빨강.
실행: python _gen_figures.py  (표준 라이브러리만 사용)
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

BLUE = ("#dbeafe", "#2563eb")
PURPLE = ("#ede9fe", "#7c3aed")
GREEN = ("#dcfce7", "#16a34a")
YELLOW = ("#fef3c7", "#d97706")
RED = ("#fee2e2", "#dc2626")
WHITE = ("#ffffff", "#64748b")
ZONE_BLUE = ("#eff6ff", "#2563eb")
ZONE_YELLOW = ("#fffbeb", "#d97706")


def box(id_, x, y, w, h, label, colors, fs=18, dashed=False):
    return {
        "kind": "box", "id": id_, "x": x, "y": y, "w": w, "h": h,
        "text": label, "fill": colors[0], "stroke": colors[1], "fs": fs,
        "dashed": dashed,
    }


def zone(id_, x, y, w, h, colors, title="", fs=16):
    return {
        "kind": "zone", "id": id_, "x": x, "y": y, "w": w, "h": h,
        "fill": colors[0], "stroke": colors[1], "title": title, "fs": fs,
    }


def arrow(id_, pts, color="#2563eb", label="", dashed=False, fs=16):
    return {
        "kind": "arrow", "id": id_, "pts": pts, "color": color,
        "label": label, "dashed": dashed, "fs": fs,
    }


def line(id_, pts, color="#94a3b8", dashed=False):
    return {
        "kind": "line", "id": id_, "pts": pts, "color": color,
        "dashed": dashed,
    }


def text(id_, x, y, value, fs=16, color="#1e293b", anchor="start"):
    return {
        "kind": "text", "id": id_, "x": x, "y": y, "text": value,
        "fs": fs, "color": color, "anchor": anchor,
    }


def dot(id_, x, y, r=9, colors=YELLOW):
    return {
        "kind": "dot", "id": id_, "x": x, "y": y, "r": r,
        "fill": colors[0], "stroke": colors[1], "label": "", "fs": 16,
    }


FIG1 = {
    "name": "01-컨텍스트-예산",
    "w": 800,
    "h": 390,
    "title": "고정된 컨텍스트 한도 안에서 예산을 배분합니다",
    "elements": [
        zone("limit", 35, 72, 730, 220, ZONE_YELLOW, "고정 한도: 입력과 출력이 함께 사용"),
        box("instruction", 55, 130, 125, 105, "지시\n18%", BLUE),
        box("question", 190, 130, 110, 105, "질문\n10%", BLUE),
        box("evidence", 310, 130, 195, 105, "근거\n36%", GREEN),
        box("output", 515, 130, 135, 105, "출력 예약\n26%", PURPLE),
        box("margin", 660, 130, 85, 105, "여유\n10%", WHITE, fs=16, dashed=True),
        text("note", 55, 330, "근거를 추가하면 다른 영역의 예산이 줄어듭니다.", 18, "#92400e"),
    ],
}


FIG2 = {
    "name": "02-저장과-선택",
    "w": 800,
    "h": 400,
    "title": "외부 저장과 컨텍스트 선택은 서로 다른 단계입니다",
    "elements": [
        box("write", 35, 145, 120, 80, "Write\n기록", BLUE),
        arrow("a1", [(155, 185), (190, 185)]),
        box("store", 190, 130, 155, 110, "외부 저장소\n대화 기록·문서", GREEN),
        arrow("a2", [(345, 185), (390, 185)]),
        box("select", 390, 145, 135, 80, "Select\n관련 기록 선택", BLUE, fs=16),
        arrow("a3", [(525, 185), (555, 185)]),
        box("message", 555, 145, 105, 80, "메시지\n본문", GREEN),
        arrow("a4", [(660, 185), (680, 185)], color="#7c3aed"),
        box("llm", 680, 145, 85, 80, "LLM", PURPLE),
        text("warning", 190, 300, "저장만으로 모델에 전달되지는 않습니다", 20, "#b91c1c"),
        text("detail", 190, 335, "Select를 실행해야 저장된 내용이 모델 입력에 포함됩니다.", 16),
    ],
}


FIG3 = {
    "name": "03-압축과-분리",
    "w": 800,
    "h": 510,
    "title": "압축은 조건과 출처를 보존하고 작업은 메시지로 분리합니다",
    "elements": [
        box("source", 40, 190, 145, 90, "원문\n조건·출처 포함", GREEN),
        arrow("a1", [(185, 235), (235, 235)]),
        box("compact", 235, 175, 170, 120, "업무별 선택·압축\n조건과 출처 유지", BLUE),
        arrow("a2", [(405, 220), (455, 150)]),
        arrow("a3", [(405, 250), (455, 330)]),
        box("msg-a", 455, 110, 130, 80, "메시지 A\n대출 안내", BLUE, fs=16),
        box("msg-b", 455, 290, 130, 80, "메시지 B\n휴관 안내", BLUE, fs=16),
        arrow("a4", [(585, 150), (635, 150)], color="#7c3aed"),
        arrow("a5", [(585, 330), (635, 330)], color="#7c3aed"),
        box("out-a", 635, 110, 130, 80, "답 생성 A", PURPLE, fs=16),
        box("out-b", 635, 290, 130, 80, "답 생성 B", PURPLE, fs=16),
        text("security", 235, 440, "메시지에 이름표를 붙여도 다른 자료의 접근을 막지는 못합니다.", 18, "#b91c1c"),
    ],
}


FIG4 = {
    "name": "04-실패-진단",
    "w": 800,
    "h": 490,
    "title": "무엇을 넣었고 어떤 답이 나왔는지 함께 확인합니다",
    "elements": [
        box("error", 45, 110, 170, 80, "잘못된 정보\n틀린 메모를 재사용", RED),
        box("irrelevant", 235, 110, 170, 80, "불필요한 자료\n중요한 내용을 놓침", RED),
        box("similar", 45, 245, 170, 80, "비슷한 대상\n이름·내용을 혼동", RED, fs=16),
        box("conflict", 235, 245, 170, 80, "서로 다른 규정\n어느 것을 따를까?", RED),
        arrow("a1", [(215, 150), (475, 205)], color="#dc2626"),
        arrow("a2", [(405, 150), (475, 215)], color="#dc2626"),
        arrow("a3", [(215, 285), (475, 235)], color="#dc2626"),
        arrow("a4", [(405, 285), (475, 225)], color="#dc2626"),
        box("diagnose", 475, 165, 280, 120, "입력과 답 비교\n무슨 자료를 넣었는가?\n답에서 무엇이 틀렸는가?", YELLOW, fs=16),
        text("note", 475, 345, "오답 문장만 보면\n네 가지 원인을 구분하기 어렵습니다.", 16, "#92400e"),
    ],
}


FIG5 = {
    "name": "05-길이와-위치",
    "w": 800,
    "h": 430,
    "title": "입력 길이에 따른 정답 확인 결과를 비교합니다",
    "elements": [
        text("fixed", 400, 45, "질문·정답 근거·모델·중앙 배치는 동일", 20, anchor="middle"),
        box("short", 40, 85, 220, 100, "짧은 입력\n주변 문장 없음", BLUE, fs=19),
        box("medium", 290, 85, 220, 100, "중간 입력\n근거 앞뒤 각 120회", BLUE, fs=19),
        box("long", 540, 85, 220, 100, "긴 입력\n근거 앞뒤 각 1,200회", BLUE, fs=19),
        arrow("a1", [(150, 185), (150, 220), (300, 260)]),
        arrow("a2", [(400, 185), (400, 260)]),
        arrow("a3", [(650, 185), (650, 220), (500, 260)]),
        box("measure", 190, 260, 420, 90, "각 길이를 3회씩 호출\n입력 토큰·실제 답·정답 확인 결과 기록", YELLOW, fs=18),
        text("read", 400, 390, "입력이 길어졌을 때 정답 확인 결과도 달라졌는지 비교", 18, anchor="middle"),
    ],
}


FIG6 = {
    "name": "06-단계적-공개",
    "w": 800,
    "h": 410,
    "title": "단계적 공개는 목록에서 필요한 본문만 선택합니다",
    "elements": [
        box("list", 35, 145, 155, 90, "문서 목록\n제목·요약", GREEN),
        arrow("a1", [(190, 190), (235, 190)]),
        box("select", 235, 130, 180, 120, "학생 규칙으로\n관련 문서 선택", BLUE),
        arrow("a2", [(415, 190), (465, 190)]),
        box("body", 465, 145, 135, 90, "선택한\n문서 본문", GREEN),
        arrow("a3", [(600, 190), (650, 190)], color="#7c3aed"),
        box("generate", 650, 145, 120, 90, "LLM\n생성", PURPLE),
        text("link", 235, 315, "Ch 9에서는 검색이 Select 단계를 자동화합니다.", 18, "#1d4ed8"),
    ],
}


FIGS = [FIG1, FIG2, FIG3, FIG4, FIG5, FIG6]


def esc(value: str) -> str:
    return (
        value.replace("&", "&amp;").replace("<", "&lt;")
        .replace(">", "&gt;").replace('"', "&quot;")
    )


def svg_text_lines(x, y, lines, fs, color, anchor="middle", weight="normal"):
    line_height = fs * 1.35
    top = y - line_height * (len(lines) - 1) / 2
    parts = [
        (f'<text x="{x}" y="{top:.1f}" font-size="{fs}" fill="{color}" '
        f'text-anchor="{anchor}" dominant-baseline="middle" font-weight="{weight}">')
    ]
    for index, item in enumerate(lines):
        dy = 0 if index == 0 else line_height
        parts.append(f'<tspan x="{x}" dy="{dy:.1f}">{esc(item)}</tspan>')
    parts.append("</text>")
    return "".join(parts)


def to_svg(fig) -> str:
    width, height = fig["w"], fig["h"]
    parts = [
        (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" '
        f'font-family="Pretendard, Noto Sans KR, Apple SD Gothic Neo, sans-serif" '
        f'role="img" aria-label="{esc(fig["title"])}">'),
        f'<title>{esc(fig["title"])}</title>',
        "<defs>",
    ]
    for marker_id, color in [
        ("blue", "#2563eb"), ("purple", "#7c3aed"),
        ("green", "#16a34a"), ("yellow", "#d97706"),
        ("red", "#dc2626"), ("gray", "#64748b"),
    ]:
        parts.append(
            f'<marker id="m-{marker_id}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>'
        )
    parts.extend(["</defs>", f'<rect width="{width}" height="{height}" fill="#ffffff"/>'])
    parts.append(svg_text_lines(20, 32, [fig["title"]], 20, "#1e293b", "start", "bold"))
    color_ids = {
        "#2563eb": "blue", "#7c3aed": "purple", "#16a34a": "green",
        "#d97706": "yellow", "#dc2626": "red", "#64748b": "gray",
    }
    for element in fig["elements"]:
        kind = element["kind"]
        if kind == "zone":
            parts.append(
                f'<rect x="{element["x"]}" y="{element["y"]}" width="{element["w"]}" '
                f'height="{element["h"]}" rx="12" fill="{element["fill"]}" '
                f'stroke="{element["stroke"]}" stroke-width="1.5"/>'
            )
            if element["title"]:
                parts.append(svg_text_lines(
                    element["x"] + 14, element["y"] + 20, [element["title"]],
                    element["fs"], "#1e293b", "start", "bold",
                ))
        elif kind == "box":
            dash = ' stroke-dasharray="7 5"' if element["dashed"] else ""
            parts.append(
                f'<rect x="{element["x"]}" y="{element["y"]}" width="{element["w"]}" '
                f'height="{element["h"]}" rx="10" fill="{element["fill"]}" '
                f'stroke="{element["stroke"]}" stroke-width="2"{dash}/>'
            )
            parts.append(svg_text_lines(
                element["x"] + element["w"] / 2,
                element["y"] + element["h"] / 2,
                element["text"].split("\n"), element["fs"], "#1e293b",
            ))
        elif kind == "arrow":
            points = " ".join(f"{x},{y}" for x, y in element["pts"])
            dash = ' stroke-dasharray="7 5"' if element["dashed"] else ""
            marker_id = color_ids.get(element["color"], "blue")
            parts.append(
                f'<polyline points="{points}" fill="none" stroke="{element["color"]}" '
                f'stroke-width="2.5" marker-end="url(#m-{marker_id})"{dash}/>'
            )
        elif kind == "line":
            points = " ".join(f"{x},{y}" for x, y in element["pts"])
            dash = ' stroke-dasharray="7 5"' if element["dashed"] else ""
            parts.append(
                f'<polyline points="{points}" fill="none" stroke="{element["color"]}" '
                f'stroke-width="1.5"{dash}/>'
            )
        elif kind == "text":
            parts.append(svg_text_lines(
                element["x"], element["y"], element["text"].split("\n"),
                element["fs"], element["color"], element["anchor"],
            ))
        elif kind == "dot":
            parts.append(
                f'<circle cx="{element["x"]}" cy="{element["y"]}" r="{element["r"]}" '
                f'fill="{element["fill"]}" stroke="{element["stroke"]}" stroke-width="2"/>'
            )
    parts.append("</svg>")
    return "\n".join(parts)


def to_excalidraw(fig) -> dict:
    elements = []
    sequence = 0

    def base(element_type, id_, x, y, width, height, **extra):
        nonlocal sequence
        sequence += 1
        value = {
            "type": element_type, "id": id_, "x": x, "y": y,
            "width": width, "height": height, "angle": 0,
            "strokeColor": "#1e293b", "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
            "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": None, "seed": sequence, "version": 1,
            "versionNonce": sequence, "isDeleted": False, "boundElements": [],
            "updated": 0, "link": None, "locked": False,
        }
        value.update(extra)
        return value

    def txt(id_, x, y, value, fs, color, align="center"):
        lines = value.split("\n")
        width = max(len(item) for item in lines) * fs * 0.72
        height = fs * 1.35 * len(lines)
        left = x - width / 2 if align == "center" else x
        return base(
            "text", id_, left, y - height / 2, width, height, text=value,
            fontSize=fs, fontFamily=1, textAlign=align, verticalAlign="middle",
            strokeColor=color, originalText=value, lineHeight=1.25, autoResize=True,
        )

    elements.append(txt("title", 20, 32, fig["title"], 20, "#1e293b", "left"))
    for element in fig["elements"]:
        kind = element["kind"]
        if kind == "zone":
            elements.append(base(
                "rectangle", element["id"], element["x"], element["y"],
                element["w"], element["h"], backgroundColor=element["fill"],
                strokeColor=element["stroke"], strokeWidth=1,
                roundness={"type": 3},
            ))
            if element["title"]:
                elements.append(txt(
                    element["id"] + "_t", element["x"] + 14,
                    element["y"] + 20, element["title"], element["fs"],
                    "#1e293b", "left",
                ))
        elif kind == "box":
            elements.append(base(
                "rectangle", element["id"], element["x"], element["y"],
                element["w"], element["h"], backgroundColor=element["fill"],
                strokeColor=element["stroke"], roundness={"type": 3},
                strokeStyle="dashed" if element["dashed"] else "solid",
            ))
            elements.append(txt(
                element["id"] + "_t", element["x"] + element["w"] / 2,
                element["y"] + element["h"] / 2, element["text"],
                element["fs"], "#1e293b",
            ))
        elif kind in {"arrow", "line"}:
            x0, y0 = element["pts"][0]
            points = [[x - x0, y - y0] for x, y in element["pts"]]
            elements.append(base(
                "arrow" if kind == "arrow" else "line", element["id"], x0, y0,
                element["pts"][-1][0] - x0, element["pts"][-1][1] - y0,
                points=points, strokeColor=element["color"],
                endArrowhead="arrow" if kind == "arrow" else None,
                startArrowhead=None,
                strokeStyle="dashed" if element.get("dashed") else "solid",
                lastCommittedPoint=None, startBinding=None, endBinding=None,
            ))
        elif kind == "text":
            align = "left" if element["anchor"] == "start" else "center"
            elements.append(txt(
                element["id"], element["x"], element["y"], element["text"],
                element["fs"], element["color"], align,
            ))
        elif kind == "dot":
            elements.append(base(
                "ellipse", element["id"], element["x"] - element["r"],
                element["y"] - element["r"], element["r"] * 2,
                element["r"] * 2, backgroundColor=element["fill"],
                strokeColor=element["stroke"],
            ))
    return {
        "type": "excalidraw", "version": 2,
        "source": "ch08-context-engineering/figures/_gen_figures.py",
        "elements": elements,
        "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
        "files": {},
    }


if __name__ == "__main__":
    for figure in FIGS:
        (HERE / f"{figure['name']}.svg").write_text(to_svg(figure), encoding="utf-8")
        (HERE / f"{figure['name']}.excalidraw").write_text(
            json.dumps(to_excalidraw(figure), ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
        print("wrote", figure["name"])
