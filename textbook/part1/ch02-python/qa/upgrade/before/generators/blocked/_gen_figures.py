"""Ch2 lesson diagrams, SVG and editable Excalidraw from one element list."""
from __future__ import annotations

raise SystemExit("옛 도식 생성기 — 품질 개선 뒤 실행 금지. 지금 판 그림은 figures/*.mmd를 textbook/_notebook/mermaid/render_mermaid.py로 렌더하고, 절 생성기는 qa/upgrade/author_*.py")

import json
from pathlib import Path
from xml.etree import ElementTree

HERE = Path(__file__).resolve().parent

BLUE = ("#dbeafe", "#2563eb")
GREEN = ("#dcfce7", "#16a34a")
YELLOW = ("#fef3c7", "#d97706")
RED = ("#fee2e2", "#dc2626")
GRAY = ("#f3f4f6", "#6b7280")

TEXT_BY_STROKE = {
    "#2563eb": "#1e40af",
    "#16a34a": "#166534",
    "#d97706": "#92400e",
    "#dc2626": "#991b1b",
    "#6b7280": "#4b5563",
}


def box(id_, x, y, w, h, label, colors, fs=16, dashed=False):
    return {"kind": "box", "id": id_, "x": x, "y": y, "w": w, "h": h,
            "label": label, "fill": colors[0], "stroke": colors[1], "fs": fs,
            "dashed": dashed}


def arrow(id_, points, color="#2563eb", label="", fs=14, dashed=False):
    return {"kind": "arrow", "id": id_, "points": points, "color": color,
            "label": label, "fs": fs, "dashed": dashed}


def text(id_, x, y, label, fs=16, color="#111827", anchor="start", weight="normal"):
    return {"kind": "text", "id": id_, "x": x, "y": y, "label": label,
            "fs": fs, "color": color, "anchor": anchor, "weight": weight}


def esc(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def svg_text(x, y, label, fs, color, anchor="middle", weight="normal"):
    lines = label.split("\n")
    line_height = fs * 1.35
    top = y - line_height * (len(lines) - 1) / 2
    parts = [f'<text x="{x}" y="{top:.1f}" font-size="{fs}" fill="{color}" '
             f'text-anchor="{anchor}" dominant-baseline="middle" font-weight="{weight}">']
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        parts.append(f'<tspan x="{x}" dy="{dy:.1f}">{esc(line)}</tspan>')
    parts.append("</text>")
    return "".join(parts)


def to_svg(figure):
    w, h = figure["w"], figure["h"]
    title_id = f"title-{figure['name']}"
    desc_id = f"desc-{figure['name']}"
    parts = [
        f'<svg style="min-width:{w}px" xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        'font-family="Pretendard, Noto Sans KR, Apple SD Gothic Neo, Malgun Gothic, sans-serif" '
        f'role="img" aria-labelledby="{title_id} {desc_id}">',
        f'<title id="{title_id}">{esc(figure["title"])}</title>',
        f'<desc id="{desc_id}">{esc(figure["caption"])}</desc>',
        "<defs>",
    ]
    marker_colors = {"blue": "#2563eb", "green": "#16a34a", "yellow": "#d97706",
                     "red": "#dc2626", "gray": "#6b7280"}
    for marker_id, color in marker_colors.items():
        parts.append(f'<marker id="m-{marker_id}" viewBox="0 0 10 10" refX="9" refY="5" '
                     f'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
                     f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>')
    parts.extend(["</defs>", f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
                  svg_text(20, 30, figure["title"], 19, "#111827", "start", "bold")])
    marker_for = {value: key for key, value in marker_colors.items()}
    for element in figure["elements"]:
        kind = element["kind"]
        if kind == "box":
            dash = ' stroke-dasharray="7 5"' if element["dashed"] else ""
            parts.append(f'<rect x="{element["x"]}" y="{element["y"]}" width="{element["w"]}" '
                         f'height="{element["h"]}" rx="10" fill="{element["fill"]}" '
                         f'stroke="{element["stroke"]}" stroke-width="2"{dash}/>')
            parts.append(svg_text(element["x"] + element["w"] / 2,
                                  element["y"] + element["h"] / 2,
                                  element["label"], element["fs"], "#111827"))
        elif kind == "arrow":
            point_string = " ".join(f"{x},{y}" for x, y in element["points"])
            dash = ' stroke-dasharray="7 5"' if element["dashed"] else ""
            marker = marker_for[element["color"]]
            parts.append(f'<polyline points="{point_string}" fill="none" stroke="{element["color"]}" '
                         f'stroke-width="2" marker-end="url(#m-{marker})"{dash}/>')
            if element["label"]:
                first, last = element["points"][0], element["points"][-1]
                x, y = (first[0] + last[0]) / 2, (first[1] + last[1]) / 2 - 15
                label_width = max(70, len(element["label"]) * element["fs"] * 0.62 + 14)
                parts.append(f'<rect x="{x - label_width / 2:.1f}" y="{y - 12:.1f}" '
                             f'width="{label_width:.1f}" height="24" rx="4" fill="#ffffff" opacity="0.94"/>')
                parts.append(svg_text(x, y, element["label"], element["fs"],
                                      TEXT_BY_STROKE[element["color"]]))
        elif kind == "text":
            parts.append(svg_text(element["x"], element["y"], element["label"], element["fs"],
                                  element["color"], element["anchor"], element["weight"]))
    parts.append("</svg>")
    return "\n".join(parts)


def to_excalidraw(figure):
    elements = []
    sequence = 0

    def base(element_type, id_, x, y, width, height, **extra):
        nonlocal sequence
        sequence += 1
        data = {"type": element_type, "id": id_, "x": x, "y": y, "width": width,
                "height": height, "angle": 0, "strokeColor": "#111827",
                "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 2,
                "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [],
                "frameId": None, "roundness": None, "seed": sequence,
                "version": 1, "versionNonce": sequence, "isDeleted": False,
                "boundElements": [], "updated": 0, "link": None, "locked": False}
        data.update(extra)
        return data

    def text_element(id_, x, y, label, fs, color, align="center"):
        lines = label.split("\n")
        width = max(len(line) for line in lines) * fs * 0.78
        height = fs * 1.35 * len(lines)
        text_x = x - width / 2 if align == "center" else x
        return base("text", id_, text_x, y - height / 2, width, height, text=label,
                    fontSize=fs, fontFamily=1, textAlign=align, verticalAlign="middle",
                    strokeColor=color, originalText=label, lineHeight=1.35, autoResize=True)

    elements.append(text_element("title", 20, 30, figure["title"], 19, "#111827", "left"))
    for element in figure["elements"]:
        kind = element["kind"]
        if kind == "box":
            elements.append(base("rectangle", element["id"], element["x"], element["y"],
                                 element["w"], element["h"], backgroundColor=element["fill"],
                                 strokeColor=element["stroke"], roundness={"type": 3},
                                 strokeStyle="dashed" if element["dashed"] else "solid"))
            elements.append(text_element(element["id"] + "_text",
                                         element["x"] + element["w"] / 2,
                                         element["y"] + element["h"] / 2,
                                         element["label"], element["fs"], "#111827"))
        elif kind == "arrow":
            x0, y0 = element["points"][0]
            points = [[x - x0, y - y0] for x, y in element["points"]]
            elements.append(base("arrow", element["id"], x0, y0,
                                 element["points"][-1][0] - x0,
                                 element["points"][-1][1] - y0,
                                 points=points, strokeColor=element["color"],
                                 endArrowhead="arrow", startArrowhead=None,
                                 strokeStyle="dashed" if element["dashed"] else "solid",
                                 lastCommittedPoint=None, startBinding=None, endBinding=None,
                                 elbowed=False))
            if element["label"]:
                first, last = element["points"][0], element["points"][-1]
                x, y = (first[0] + last[0]) / 2, (first[1] + last[1]) / 2 - 15
                elements.append(text_element(element["id"] + "_label", x, y,
                                             element["label"], element["fs"],
                                             TEXT_BY_STROKE[element["color"]]))
        elif kind == "text":
            align = "center" if element["anchor"] == "middle" else "left"
            elements.append(text_element(element["id"], element["x"], element["y"],
                                         element["label"], element["fs"], element["color"], align))
    return {"type": "excalidraw", "version": 2, "source": "ch02 _gen_figures.py",
            "elements": elements, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
            "files": {}}


def validate(figure, svg):
    box_count = sum(element["kind"] == "box" for element in figure["elements"])
    assert box_count <= 7, f"{figure['name']}: 상자가 {box_count}개입니다"
    assert all(element.get("fs", 14) >= 14 for element in figure["elements"]), figure["name"]
    assert all(color not in svg.lower() for color in ("#9c36b5", "#800080", "#7950f2")), figure["name"]
    ElementTree.fromstring(svg)



# Diagram specifications are reviewed alongside each lesson's actual examples.
def figures_from_specs():
    palette = {"blue": BLUE, "green": GREEN, "yellow": YELLOW, "red": RED, "gray": GRAY,
               "파랑": BLUE, "초록": GREEN, "노랑": YELLOW, "빨강": RED}
    for path in sorted((HERE.parent / "qa").glob("figures-*.json")):
        specs = json.loads(path.read_text())
        for spec in specs:
            if "elements" in spec:
                yield spec
                continue
            boxes = spec["boxes"]
            count = len(boxes)
            assert 1 <= count <= 7
            elements = []
            # Vertical layout preserves one clear reading order and avoids crossing arrows.
            for i, item in enumerate(boxes):
                y = 75 + i * 110
                colors = palette[item.get("color", "blue")]
                elements.append(box(f"b{i}", 80, y, 560, 76, item["label"], colors, 17))
                if i < count - 1:
                    elements.append(arrow(f"a{i}", [(360, y + 76), (360, y + 110)]))
            yield {"name": spec["name"], "w": 720, "h": 95 + count * 110,
                   "title": spec["title"], "caption": spec["caption"], "elements": elements}

if __name__ == "__main__":
    for figure in figures_from_specs():
        if not any("파랑:" in e.get("label", "") for e in figure["elements"]):
            figure["elements"].append(text("palette", figure["w"] / 2, figure["h"] + 24,
                "파랑: 작성한 흐름 · 초록: 데이터 · 노랑: 확인 · 빨강: 실패", 14, "#4b5563", "middle"))
            figure["h"] += 50
        svg = to_svg(figure)
        validate(figure, svg)
        (HERE / f"{figure['name']}.svg").write_text(svg, encoding="utf-8")
        (HERE / f"{figure['name']}.excalidraw").write_text(
            json.dumps(to_excalidraw(figure), ensure_ascii=False, indent=1), encoding="utf-8")
        print("wrote", figure["name"])
