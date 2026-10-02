"""Ch 9 도식 생성기 — 같은 요소 목록에서 .excalidraw(JSON)과 .svg(확정본)를 함께 만든다.

색 규칙(AGENTS.md §16): 학생 흐름=파랑, 모델 판단=보라, 도구·데이터=초록, 측정=노랑, 실패=빨강.
실행: python _gen_figures.py  (표준 라이브러리만 사용)
"""

from __future__ import annotations

raise SystemExit("옛 도식 생성기 — 품질 개선 뒤 실행 금지. 지금 판 그림은 figures/*.mmd를 textbook/_notebook/mermaid/render_mermaid.py로 렌더하고, 절 생성기는 qa/upgrade/author_*.py")

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

BLUE = ("#a5d8ff", "#4a9eed")
GREEN = ("#b2f2bb", "#22c55e")
TEAL = ("#c3fae8", "#22c55e")
YELLOW = ("#fff3bf", "#f59e0b")
RED = ("#ffc9c9", "#ef4444")
WHITE = ("#ffffff", "#757575")
ZONE_BLUE = ("#dbe4ff", "#4a9eed")
ZONE_GREEN = ("#d3f9d8", "#22c55e")
ZONE_YELLOW = ("#fff8dc", "#f59e0b")
ZONE_RED = ("#ffe3e3", "#ef4444")

# 선과 채움은 의미 색을 유지하고, 글자는 흰 배경에서 WCAG 4.5:1 이상인 색을 쓴다.
TEXT_BY_STROKE = {
    "#4a9eed": "#1e40af",
    "#22c55e": "#166534",
    "#f59e0b": "#92400e",
    "#ef4444": "#991b1b",
    "#757575": "#595959",
}


def box(id_, x, y, w, h, text, colors, fs=16, dashed=False):
    return {"kind": "box", "id": id_, "x": x, "y": y, "w": w, "h": h, "text": text,
            "fill": colors[0], "stroke": colors[1], "fs": fs, "dashed": dashed}


def zone(id_, x, y, w, h, colors, title="", fs=15):
    return {"kind": "zone", "id": id_, "x": x, "y": y, "w": w, "h": h,
            "fill": colors[0], "stroke": colors[1], "title": title, "fs": fs}


def arrow(id_, pts, color="#4a9eed", label="", dashed=False, fs=14):
    return {"kind": "arrow", "id": id_, "pts": pts, "color": color, "label": label,
            "dashed": dashed, "fs": fs}


def text(id_, x, y, s, fs=16, color="#1e1e1e", anchor="start"):
    return {"kind": "text", "id": id_, "x": x, "y": y, "text": s, "fs": fs, "color": color,
            "anchor": anchor}


def dot(id_, x, y, r, colors, label="", fs=14):
    return {"kind": "dot", "id": id_, "x": x, "y": y, "r": r, "fill": colors[0],
            "stroke": colors[1], "label": label, "fs": fs}


# ------------------------------------------------------------------ 도식 정의
FIG1 = dict(
    name="01-파이프라인", w=800, h=500,
    title="RAG의 두 단계: 문서를 준비하고 질문에 답하기",
    elements=[
        zone("z1", 30, 60, 740, 150, ZONE_GREEN, "① 색인 (문서·청크 설정·임베딩 모델이 바뀔 때 다시 만들기)"),
        box("b1", 50, 110, 140, 70, "수업용 PDF\nE01.pdf", GREEN),
        arrow("a1", [(190, 145), (230, 145)]),
        box("b2", 230, 110, 140, 70, "PDF 읽기 →\n청크 나누기", BLUE),
        arrow("a2", [(370, 145), (410, 145)], label="청크"),
        box("b3", 410, 110, 140, 70, "임베딩\nembed", BLUE),
        arrow("a3", [(550, 145), (590, 145)], label="벡터"),
        box("b4", 590, 110, 150, 70, "벡터스토어\nInMemoryVectorStore", TEAL, fs=14),
        zone("z2", 30, 250, 740, 230, ZONE_BLUE, "② 질문 처리 (질문할 때마다): 검색 → 답 만들기"),
        text("q", 60, 338, "질문", 18),
        arrow("a4", [(110, 330), (170, 330)]),
        box("b5", 170, 295, 150, 70, "가까운 청크 검색\nk=2", BLUE),
        arrow("a5", [(665, 180), (665, 240), (500, 240), (500, 280), (245, 280), (245, 295)], color="#22c55e",
              label="질문 벡터로 이웃 찾기", dashed=True),
        arrow("a6", [(320, 330), (370, 330)], label="청크 k개"),
        box("b6", 370, 295, 150, 70, "문맥과 질문을\n프롬프트로 합치기", BLUE),
        arrow("a7", [(520, 330), (570, 330)]),
        box("b7", 570, 295, 150, 70, "LLM으로\n답 만들기", BLUE),
        arrow("a8", [(645, 365), (645, 405)]),
        text("out", 645, 430, "답 + 출처 [E01 p.2]", 16, "#1e1e1e", anchor="middle"),
        text("n1", 60, 420, "파랑 = 학생 코드가 고정한 흐름 · 모델은 이 흐름을 판단하지 않는다", 14, "#595959"),
        text("n2", 60, 445, "초록 = 문서·데이터 저장소   (몇 번 검색할지도 학생이 정한다)", 14, "#757575"),
    ],
)

FIG2 = dict(
    name="02-청크-경계", w=800, h=440,
    title="PDF 한 쪽을 작은 청크로 나누고 이웃 청크의 글을 겹치기",
    elements=[
        box("page", 40, 60, 720, 50, "E01 p.2 Document   출처 정보: {doc_id: E01, page: 2}", GREEN, fs=15),
        arrow("d1", [(200, 110), (200, 160)]),
        text("d1t", 215, 135, "RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)", 14, "#2563eb"),
        box("c3", 40, 165, 340, 68, "청크 #0 (최대 500자)\nPDF 본문 앞부분…", BLUE, fs=14),
        box("c4", 330, 245, 340, 68, "청크 #1\n앞 청크의 끝 50자 + 다음 본문…", BLUE, fs=14),
        box("c5", 640, 245, 120, 68, "다음 청크…", BLUE, fs=14),
        zone("ov", 330, 160, 50, 150, ZONE_YELLOW, ""),
        text("ovt", 355, 325, "겹침 50자", 14, "#92400e", anchor="middle"),
        text("m1", 40, 360, "모든 청크에 출처 정보가 복사된다 → {doc_id: E01, page: 2}", 15, "#15803d"),
        text("m2", 40, 390, "경계 근처의 글자는 겹쳐 남을 수 있습니다. 겹침이 0이면 단어나 문장이 경계에서 잘릴 수 있습니다.", 14, "#757575"),
        text("m3", 40, 415, "500은 토큰 수가 아니라 글자 수다. 이 실습은 실제 청크 길이를 출력해 확인한다.", 14, "#757575"),
    ],
)

FIG3 = dict(
    name="03-벡터-검색", w=800, h=480,
    title="질문과 뜻이 가까운 문서를 k개 고르는 검색",
    elements=[
        zone("sp", 40, 60, 480, 380, ZONE_GREEN, "글의 뜻을 숫자로 나타낸 공간 (그림은 2차원으로 단순화)"),
        dot("p1", 200, 200, 10, GREEN, "D01 휴관일"),
        dot("p2", 250, 250, 10, GREEN, "D02 점심 영업"),
        dot("p3", 150, 300, 10, GREEN, "D03 급여일"),
        dot("p4", 310, 305, 10, GREEN, "추가 문서"),
        dot("p5", 420, 130, 8, GREEN, "다른 문서"),
        dot("p6", 460, 380, 8, GREEN, "다른 문서"),
        dot("p7", 90, 130, 8, GREEN, "다른 문서"),
        dot("q", 230, 230, 12, BLUE, ""),
        text("ql", 175, 222, "질문 ★", 15, "#2563eb"),
        {"kind": "circle", "id": "kc", "x": 230, "y": 230, "r": 125, "stroke": "#4a9eed"},
        text("kl", 290, 120, "k=2 범위", 14, "#2563eb"),
        box("s1", 560, 80, 210, 60, "질문도 같은 방식으로\n숫자 벡터로 바꾸기", BLUE, fs=14),
        arrow("a1", [(560, 110), (345, 220)], color="#4a9eed", label="", dashed=True),
        box("s2", 560, 170, 210, 90, "similarity_search_with_score\n(query, k=1 또는 2)\n→ [(Document, 점수)]", BLUE, fs=14),
        box("s3", 560, 290, 210, 70, "k=1: 가장 가까운\nD01 한 건", RED, fs=14),
        box("s4", 560, 380, 210, 55, "k=2: D01은 유지되고\n후보 한 건이 추가된다", YELLOW, fs=14),
    ],
)

FIG4 = dict(
    name="05-실패-경로", w=800, h=520,
    title="같은 출력, 다른 원인 — '문서에서 찾을 수 없습니다'는 두 가지 뜻이다",
    elements=[
        text("q", 105, 235, "질문", 16, "#1e40af", anchor="middle"),
        arrow("a0", [(170, 235), (200, 235)]),
        box("s", 200, 200, 140, 70, "top-k 검색\n(학생 코드)", BLUE),
        arrow("a1", [(340, 215), (450, 120)], color="#22c55e", label="정답 청크 포함", fs=14),
        arrow("a2", [(340, 235), (450, 235)], color="#ef4444", label="검색 실패·정답 누락", fs=14),
        arrow("a3", [(340, 255), (450, 360)], color="#757575", label="문서에 처음부터 없음", fs=14),
        box("r1", 450, 85, 130, 70, "LLM", BLUE),
        box("r2", 450, 200, 130, 70, "LLM", BLUE),
        box("r3", 450, 325, 130, 70, "LLM", BLUE),
        arrow("b1", [(580, 120), (620, 120)]),
        arrow("b2", [(580, 235), (620, 235)]),
        arrow("b3", [(580, 360), (620, 360)]),
        box("o1", 620, 85, 160, 70, "규정 답 + 근거\nANSWER", GREEN, fs=15),
        zone("z", 610, 190, 180, 215, ZONE_YELLOW, ""),
        box("o2", 620, 200, 160, 70, "\"찾을 수 없습니다\"\n또는 지어낸 숫자", RED, fs=14),
        box("o3", 620, 325, 160, 70, "\"찾을 수 없습니다\"\n(올바른 답)", YELLOW, fs=14),
        text("n1", 40, 440, "두 경우 모두 같은 거부 문장이 나올 수 있다. 검색된 문서 ID를 보면 원인을 구분할 수 있다.", 14, "#1e1e1e"),
        text("n2", 40, 465, "'찾을 수 없습니다'라는 지시는 검색에서 빠진 정답 문서를 다시 가져오지 못한다.", 14, "#757575"),
        text("n3", 40, 490, "검색 문제는 검색된 문서 ID와 본문을 먼저 확인해 찾아낸다.", 14, "#757575"),
    ],
)

FIG5 = dict(
    name="06-하네스-루프", w=800, h=470,
    title="설정을 하나 바꾸고 결과를 한 줄로 남기는 반복 실험",
    elements=[
        box("cfg", 40, 100, 170, 80, "설정 딕셔너리\n청크 크기 · k · 모델", BLUE, fs=14),
        arrow("a1", [(210, 140), (270, 140)]),
        text("a1t", 240, 88, "k만 1 → 2", 14, "#2563eb", anchor="middle"),
        box("h", 270, 100, 170, 80, "색인 설정을 JSON으로 바꾸고\n해시 만들기", BLUE, fs=14),
        arrow("a2", [(355, 180), (355, 230)], color="#22c55e", label="해시가 같으면 다시 쓰기", dashed=True),
        box("idx", 270, 230, 170, 70, "cache 딕셔너리\n이미 만든 벡터스토어", TEAL, fs=14),
        arrow("a3", [(440, 140), (500, 140)]),
        text("a3t", 470, 88, "질문 검색", 14, "#2563eb", anchor="middle"),
        box("run", 500, 100, 150, 80, "저장된 벡터스토어에서\nk=2로 검색", BLUE, fs=14),
        arrow("a4", [(575, 180), (575, 230)], color="#f59e0b"),
        box("log", 480, 230, 190, 70, "임시 runs.jsonl에 한 줄\n설정 · 해시 · 재사용 여부 · 검색 ID", YELLOW, fs=14),
        box("det", 480, 320, 190, 60, "저장한 한 줄을 다시 읽고\n원래 딕셔너리와 비교", YELLOW, fs=14),
        arrow("a5", [(575, 300), (575, 320)], color="#f59e0b"),
        box("met", 690, 230, 90, 70, "품질 점수\nCh 11에서 추가", YELLOW, fs=14, dashed=True),
        arrow("a6", [(480, 280), (455, 280), (455, 335), (125, 335), (125, 180)], color="#4a9eed",
              dashed=True),
        text("a6t", 290, 355, "기록을 읽고 → 다음 설정 하나를 바꾸고 → 다시 실행", 14, "#2563eb", anchor="middle"),
        text("n1", 40, 420, "같은 순서로 기록하면 어떤 설정에서 어떤 결과가 나왔는지 나중에 비교할 수 있다.", 14, "#757575"),
        text("n2", 40, 445, "지금 기록에는 품질 점수가 없다. Ch 11에서 검색 결과를 평가하는 점수를 추가한다.", 14, "#757575"),
    ],
)

FIGS = [FIG1, FIG2, FIG3, FIG4, FIG5]


# ------------------------------------------------------------------ SVG
def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_text_lines(x, y, lines, fs, color, anchor="middle", weight="normal"):
    lh = fs * 1.35
    top = y - lh * (len(lines) - 1) / 2
    out = [f'<text x="{x}" y="{top:.1f}" font-size="{fs}" fill="{color}" text-anchor="{anchor}" '
           f'dominant-baseline="middle" font-weight="{weight}">']
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else lh
        out.append(f'<tspan x="{x}" dy="{dy:.1f}">{esc(line)}</tspan>')
    out.append("</text>")
    return "".join(out)


def to_svg(fig) -> str:
    w, h = fig["w"], fig["h"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'font-family="Pretendard, \'Noto Sans KR\', \'Apple SD Gothic Neo\', \'Malgun Gothic\', sans-serif" '
        f'role="img" aria-label="{esc(fig["title"])}">',
        "<defs>",
    ]
    for cid, col in [("blue", "#4a9eed"), ("green", "#22c55e"),
                     ("yellow", "#f59e0b"), ("red", "#ef4444"), ("gray", "#757575")]:
        parts.append(
            f'<marker id="m-{cid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
    parts.append("</defs>")
    parts.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')
    parts.append(svg_text_lines(20, 30, [fig["title"]], 18, "#1e1e1e", anchor="start", weight="bold"))
    color_id = {"#4a9eed": "blue", "#22c55e": "green", "#f59e0b": "yellow",
                "#ef4444": "red", "#757575": "gray"}
    for e in fig["elements"]:
        k = e["kind"]
        if k == "zone":
            parts.append(f'<rect x="{e["x"]}" y="{e["y"]}" width="{e["w"]}" height="{e["h"]}" rx="12" '
                         f'fill="{e["fill"]}" fill-opacity="0.35" stroke="{e["stroke"]}" stroke-width="1"/>')
            if e["title"]:
                parts.append(svg_text_lines(e["x"] + 14, e["y"] + 16, [e["title"]], e["fs"],
                                            TEXT_BY_STROKE.get(e["stroke"], e["stroke"]), anchor="start"))
        elif k == "box":
            dash = ' stroke-dasharray="6 4"' if e["dashed"] else ""
            parts.append(f'<rect x="{e["x"]}" y="{e["y"]}" width="{e["w"]}" height="{e["h"]}" rx="10" '
                         f'fill="{e["fill"]}" stroke="{e["stroke"]}" stroke-width="2"{dash}/>')
            parts.append(svg_text_lines(e["x"] + e["w"] / 2, e["y"] + e["h"] / 2,
                                        e["text"].split("\n"), e["fs"], "#1e1e1e"))
        elif k == "arrow":
            pts = " ".join(f"{x},{y}" for x, y in e["pts"])
            dash = ' stroke-dasharray="7 5"' if e["dashed"] else ""
            mid = color_id.get(e["color"], "blue")
            parts.append(f'<polyline points="{pts}" fill="none" stroke="{e["color"]}" stroke-width="2" '
                         f'marker-end="url(#m-{mid})"{dash}/>')
            if e["label"]:
                (x1, y1), (x2, y2) = e["pts"][0], e["pts"][-1]
                if len(e["pts"]) > 2:
                    (x1, y1), (x2, y2) = e["pts"][1], e["pts"][2]
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 12
                tw = len(e["label"]) * e["fs"] * 0.62 + 10
                parts.append(f'<rect x="{mx - tw / 2:.1f}" y="{my - e["fs"] * 0.75:.1f}" width="{tw:.1f}" '
                             f'height="{e["fs"] * 1.5:.1f}" fill="#ffffff" fill-opacity="0.9" rx="4"/>')
                parts.append(svg_text_lines(mx, my, [e["label"]], e["fs"],
                                            TEXT_BY_STROKE.get(e["color"], e["color"])))
        elif k == "text":
            parts.append(svg_text_lines(e["x"], e["y"], [e["text"]], e["fs"], e["color"], anchor=e["anchor"]))
        elif k == "dot":
            parts.append(f'<circle cx="{e["x"]}" cy="{e["y"]}" r="{e["r"]}" fill="{e["fill"]}" '
                         f'stroke="{e["stroke"]}" stroke-width="2"/>')
            if e["label"]:
                parts.append(svg_text_lines(e["x"] + e["r"] + 6, e["y"], [e["label"]], e["fs"],
                                            "#166534", anchor="start"))
        elif k == "circle":
            parts.append(f'<circle cx="{e["x"]}" cy="{e["y"]}" r="{e["r"]}" fill="none" '
                         f'stroke="{e["stroke"]}" stroke-width="2" stroke-dasharray="6 4"/>')
    parts.append("</svg>")
    return "\n".join(parts)


# ------------------------------------------------------------------ Excalidraw JSON
def to_excalidraw(fig) -> dict:
    els = []
    seq = 0

    def base(t, id_, x, y, w, h, **kw):
        nonlocal seq
        seq += 1
        d = {"type": t, "id": id_, "x": x, "y": y, "width": w, "height": h, "angle": 0,
             "strokeColor": "#1e1e1e", "backgroundColor": "transparent", "fillStyle": "solid",
             "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
             "groupIds": [], "frameId": None, "roundness": None, "seed": seq, "version": 1,
             "versionNonce": seq, "isDeleted": False, "boundElements": [], "updated": 0, "link": None,
             "locked": False}
        d.update(kw)
        return d

    def txt(id_, x, y, s, fs, color, align="center", w=None):
        lines = s.split("\n")
        width = w or max(len(line) for line in lines) * fs * 0.62
        height = fs * 1.25 * len(lines)
        return base("text", id_, x - (width / 2 if align == "center" else 0), y - height / 2, width, height,
                    text=s, fontSize=fs, fontFamily=1, textAlign=align, verticalAlign="middle",
                    strokeColor=color, originalText=s, lineHeight=1.25, autoResize=True)

    els.append(txt("title", 20, 30, fig["title"], 20, "#1e1e1e", align="left"))
    for e in fig["elements"]:
        k = e["kind"]
        if k == "zone":
            els.append(base("rectangle", e["id"], e["x"], e["y"], e["w"], e["h"], backgroundColor=e["fill"],
                            strokeColor=e["stroke"], strokeWidth=1, opacity=35, roundness={"type": 3}))
            if e["title"]:
                els.append(txt(e["id"] + "_t", e["x"] + 14, e["y"] + 16, e["title"], e["fs"],
                               TEXT_BY_STROKE.get(e["stroke"], e["stroke"]), "left"))
        elif k == "box":
            els.append(base("rectangle", e["id"], e["x"], e["y"], e["w"], e["h"], backgroundColor=e["fill"],
                            strokeColor=e["stroke"], roundness={"type": 3},
                            strokeStyle="dashed" if e["dashed"] else "solid"))
            els.append(txt(e["id"] + "_t", e["x"] + e["w"] / 2, e["y"] + e["h"] / 2, e["text"], e["fs"], "#1e1e1e"))
        elif k == "arrow":
            x0, y0 = e["pts"][0]
            pts = [[x - x0, y - y0] for x, y in e["pts"]]
            els.append(base("arrow", e["id"], x0, y0, e["pts"][-1][0] - x0, e["pts"][-1][1] - y0, points=pts,
                            strokeColor=e["color"], endArrowhead="arrow", startArrowhead=None,
                            strokeStyle="dashed" if e["dashed"] else "solid", lastCommittedPoint=None,
                            startBinding=None, endBinding=None, elbowed=False))
            if e["label"]:
                (x1, y1), (x2, y2) = (e["pts"][1], e["pts"][2]) if len(e["pts"]) > 2 else (e["pts"][0], e["pts"][-1])
                els.append(txt(e["id"] + "_l", (x1 + x2) / 2, (y1 + y2) / 2 - 12, e["label"], e["fs"],
                               TEXT_BY_STROKE.get(e["color"], e["color"])))
        elif k == "text":
            els.append(txt(e["id"], e["x"], e["y"], e["text"], e["fs"], e["color"], "left" if e["anchor"] == "start" else "center"))
        elif k == "dot":
            els.append(base("ellipse", e["id"], e["x"] - e["r"], e["y"] - e["r"], e["r"] * 2, e["r"] * 2,
                            backgroundColor=e["fill"], strokeColor=e["stroke"]))
            if e["label"]:
                els.append(txt(e["id"] + "_l", e["x"] + e["r"] + 6, e["y"], e["label"], e["fs"], "#166534", "left"))
        elif k == "circle":
            els.append(base("ellipse", e["id"], e["x"] - e["r"], e["y"] - e["r"], e["r"] * 2, e["r"] * 2,
                            strokeColor=e["stroke"], strokeStyle="dashed"))
    return {"type": "excalidraw", "version": 2, "source": "ch09 _gen_figures.py", "elements": els,
            "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}


if __name__ == "__main__":
    for fig in FIGS:
        (HERE / f"{fig['name']}.svg").write_text(to_svg(fig), encoding="utf-8")
        (HERE / f"{fig['name']}.excalidraw").write_text(
            json.dumps(to_excalidraw(fig), ensure_ascii=False, indent=1), encoding="utf-8")
        print("wrote", fig["name"])
