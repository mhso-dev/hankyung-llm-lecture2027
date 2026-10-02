"""Ch 1 도식 생성기 — 한 요소 목록에서 SVG와 Excalidraw를 함께 만든다.

색 규칙(AGENTS.md §16): 학생이 정한 행동=파랑, 도구·데이터=초록,
측정·확인=노랑, 실패=빨강. 이 장에서는 모델 판단을 다루지 않으므로 보라색을 쓰지 않는다.
실행: python _gen_figures.py
"""

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


FIGURES = [
    {
        "name": "01-learning-cycle", "w": 800, "h": 430,
        "title": "예측하고 확인하며 코드를 바꾸는 학습 순환",
        "caption": "예측한 결과와 실제 결과를 비교하고, 값 하나를 바꾼 뒤 다시 확인합니다.",
        "elements": [
            box("predict", 45, 105, 120, 72, "① 예측\n결과는 6,000", BLUE),
            arrow("a1", [(165, 141), (195, 141)]),
            box("run", 195, 105, 120, 72, "② 실행\n3,000 * 2", BLUE),
            arrow("a2", [(315, 141), (345, 141)]),
            box("observe", 345, 105, 120, 72, "③ 관찰\n6,000", YELLOW),
            arrow("a3", [(465, 141), (495, 141)]),
            box("change", 495, 105, 120, 72, "④ 변경\ncount = 3", BLUE),
            arrow("a4", [(615, 141), (645, 141)]),
            box("verify", 645, 105, 120, 72, "⑤ 검증\n9,000", YELLOW),
            arrow("loop", [(705, 177), (705, 240), (105, 240), (105, 177)], dashed=True),
            text("loop_label", 405, 265, "다음 값으로 반복", 14, "#1e40af", "middle", "bold"),
            text("code1", 170, 300, "price = 3000", 16, "#166534", "middle", "bold"),
            text("code2", 400, 300, "count = 2  →  count = 3", 16, "#1e40af", "middle", "bold"),
            text("code3", 635, 300, "total = price * count", 16, "#166534", "middle", "bold"),
            text("note", 400, 360, "작은 값을 바꾸면 코드와 결과의 관계를 바로 확인할 수 있습니다.", 15,
                 "#4b5563", "middle"),
        ],
    },
    {
        "name": "02-paths", "w": 800, "h": 470,
        "title": "상대 경로는 선택한 기준 폴더에서 시작한다",
        "caption": "data/message.txt를 workspace에 연결하면 실패하고 practice에 연결하면 저장한 파일을 읽습니다.",
        "elements": [
            box("project", 45, 105, 210, 190,
                "workspace/\n└─ practice/\n   └─ data/\n      └─ message.txt", GREEN, 15),
            text("where", 390, 82, "상대 경로: data/message.txt", 16, "#1e40af", "middle", "bold"),
            box("badbase", 300, 115, 190, 70, "잘못 선택한 기준\nworkspace", BLUE),
            arrow("badarrow", [(490, 150), (555, 150)], "#dc2626", "연결"),
            box("badfile", 555, 115, 195, 70, "workspace/data/message.txt\nFileNotFoundError", RED, 14),
            box("goodbase", 300, 250, 190, 70, "올바른 기준\nproject = practice", BLUE),
            arrow("goodarrow", [(490, 285), (555, 285)], "#16a34a", "연결"),
            box("goodfile", 555, 250, 195, 70, "practice/data/message.txt\n안녕, 터미널!", GREEN, 14),
            text("pwd", 300, 380, "기준 폴더 이름과 연결한 전체 경로 확인", 15, "#92400e", "start", "bold"),
            text("rule", 300, 415, "같은 상대 경로를 유지하고 기준 폴더만 바꾸어 결과를 비교합니다.", 15,
                 "#4b5563", "start"),
        ],
    },
    {
        "name": "03-environments", "w": 800, "h": 465,
        "title": "기본 Python에서 서로 다른 가상환경 두 개를 만든다",
        "caption": "uv venv가 env_a와 env_b를 만들고, 각 환경에서 prefix와 base_prefix가 다른지 확인합니다.",
        "elements": [
            box("python", 295, 55, 210, 65, "기본 Python 3.12", GREEN),
            arrow("pa", [(360, 120), (205, 180)], "#2563eb", "uv venv env_a"),
            arrow("pb", [(440, 120), (595, 180)], "#2563eb", "uv venv env_b"),
            box("env_a", 70, 180, 270, 90, "env_a\nenv_a / python_name", GREEN, 15),
            box("env_b", 460, 180, 270, 90, "env_b\nenv_b / python_name", GREEN, 15),
            arrow("ca", [(205, 270), (205, 320)], "#d97706", "prefix 비교"),
            arrow("cb", [(595, 270), (595, 320)], "#d97706", "prefix 비교"),
            box("check_a", 95, 320, 220, 70, "env_a 가상환경\nTrue", YELLOW, 16),
            box("check_b", 485, 320, 220, 70, "env_b 가상환경\nTrue", YELLOW, 16),
            text("rule", 400, 430, "True는 sys.prefix와 sys.base_prefix가 다르다는 뜻입니다.", 15,
                 "#4b5563", "middle", "bold"),
        ],
    },
    {
        "name": "04-debugging", "w": 800, "h": 500,
        "title": "중단점에서 연산 직전과 직후의 값을 확인한다",
        "caption": "F5로 연산 직전에 멈추고 F10으로 실행한 뒤, 연산자 수정 전후의 total을 비교합니다.",
        "elements": [
            box("start", 35, 100, 145, 90, "hello.py 저장\nF5 누르기", BLUE, 15),
            arrow("to_debugger", [(180, 145), (210, 145)], "#2563eb"),
            box("debugger", 210, 100, 145, 90, "선택한 .venv\nPython 디버거", GREEN, 15),
            arrow("to_breakpoint", [(355, 145), (385, 145)], "#d97706"),
            box("breakpoint", 385, 75, 205, 140,
                "중단점: 실행 직전\ntotal = price + count\nprice: 3000\ncount: 2\ntotal: 아직 없음", YELLOW, 14),
            arrow("f10_wrong", [(590, 145), (620, 145)], "#dc2626", "F10"),
            box("wrong", 620, 100, 145, 90, "실행 직후\ntotal: 3002", RED, 15),
            arrow("fix", [(692, 190), (692, 270), (155, 270), (155, 315)],
                  "#2563eb", "+를 *로 변경", dashed=True),
            box("rerun", 35, 315, 240, 80, "저장 → F5 → 중단점 → F10", BLUE, 15),
            arrow("to_right", [(275, 355), (365, 355)], "#d97706", "다시 확인"),
            box("right", 365, 315, 205, 80, "실행 직후\ntotal: 6000", YELLOW, 15),
            text("why", 400, 445, "입력값을 유지하고 연산자만 바꾸어 결과 차이를 확인합니다.", 15,
                 "#4b5563", "middle", "bold"),
        ],
    },
    {
        "name": "05-tool-readiness", "w": 800, "h": 485,
        "title": "설치 여부와 실행 상태를 구분하여 확인한다",
        "caption": "CLI 설치, 서버 실행, Git 저장소 생성은 서로 다른 준비 상태입니다.",
        "elements": [
            box("cli", 45, 105, 205, 80, "Docker CLI 설치\ndocker --version", GREEN, 15),
            arrow("cli_check", [(147, 185), (147, 230)], "#d97706", "명령 확인"),
            box("server", 45, 230, 205, 90, "Docker 서버 실행\ndocker info", GREEN, 15),
            box("git", 350, 105, 205, 80, "Git 설치\ngit --version", GREEN, 15),
            arrow("git_init", [(452, 185), (452, 230)], "#2563eb", "git init"),
            box("repo", 350, 230, 205, 90, "현재 폴더가 저장소\ngit status", BLUE, 15),
            box("check", 620, 145, 140, 135, "각 상태 기록\nCLI 응답 여부\n서버 응답 여부\n저장소 상태", YELLOW, 14),
            arrow("docker_done", [(250, 275), (620, 220)], "#d97706"),
            arrow("git_done", [(555, 275), (620, 245)], "#d97706"),
            text("docker_note", 45, 375, "Docker CLI가 설치되어도 Docker 서버가 실행 중이라는 뜻은 아닙니다.", 15,
                 "#991b1b", "start", "bold"),
            text("git_note", 45, 420, "Git이 설치되어도 현재 폴더가 Git 저장소라는 뜻은 아닙니다.", 15,
                 "#4b5563", "start"),
        ],
    },
]


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
    return {"type": "excalidraw", "version": 2, "source": "ch01 _gen_figures.py",
            "elements": elements, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
            "files": {}}


def validate(figure, svg):
    box_count = sum(element["kind"] == "box" for element in figure["elements"])
    assert box_count <= 7, f"{figure['name']}: 상자가 {box_count}개입니다"
    assert all(element.get("fs", 14) >= 14 for element in figure["elements"]), figure["name"]
    assert all(color not in svg.lower() for color in ("#9c36b5", "#800080", "#7950f2")), figure["name"]
    ElementTree.fromstring(svg)


if __name__ == "__main__":
    for figure in FIGURES:
        svg = to_svg(figure)
        validate(figure, svg)
        (HERE / f"{figure['name']}.svg").write_text(svg, encoding="utf-8")
        (HERE / f"{figure['name']}.excalidraw").write_text(
            json.dumps(to_excalidraw(figure), ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"wrote {figure['name']} — {figure['caption']}")
