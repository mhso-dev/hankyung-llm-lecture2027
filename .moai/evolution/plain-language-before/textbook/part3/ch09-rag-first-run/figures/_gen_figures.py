"""Ch 9 도식 생성기 — 같은 요소 목록에서 .excalidraw(JSON)과 .svg(확정본)를 함께 만든다.

색 규칙(AGENTS.md §16): 학생 흐름=파랑, 모델 판단=보라, 도구·데이터=초록, 측정=노랑, 실패=빨강.
실행: python _gen_figures.py  (표준 라이브러리만 사용)
"""

from __future__ import annotations

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
    title="RAG 파이프라인 — 색인은 한 번, 질의는 매번",
    elements=[
        zone("z1", 30, 60, 740, 150, ZONE_GREEN, "① 색인 (문서가 바뀔 때 한 번)"),
        box("b1", 50, 110, 140, 70, "PDF 문서\n(rag-corpus)", GREEN),
        arrow("a1", [(190, 145), (230, 145)]),
        box("b2", 230, 110, 140, 70, "로더 → 스플리터\nload / split", BLUE),
        arrow("a2", [(370, 145), (410, 145)], label="청크"),
        box("b3", 410, 110, 140, 70, "임베딩\nembed", BLUE),
        arrow("a3", [(550, 145), (590, 145)], label="벡터"),
        box("b4", 590, 110, 150, 70, "벡터스토어\nInMemoryVectorStore", TEAL, fs=14),
        zone("z2", 30, 250, 740, 230, ZONE_BLUE, "② 질의(질문마다): 검색 → 생성"),
        text("q", 60, 338, "질문", 18),
        arrow("a4", [(110, 330), (170, 330)]),
        box("b5", 170, 295, 150, 70, "top-k 검색\nsearch(k=4)", BLUE),
        arrow("a5", [(665, 180), (665, 240), (500, 240), (500, 280), (245, 280), (245, 295)], color="#22c55e",
              label="질문 벡터로 이웃 찾기", dashed=True),
        arrow("a6", [(320, 330), (370, 330)], label="청크 k개"),
        box("b6", 370, 295, 150, 70, "프롬프트 조립\nformat_context", BLUE),
        arrow("a7", [(520, 330), (570, 330)]),
        box("b7", 570, 295, 150, 70, "LLM 생성\ngenerate", BLUE),
        arrow("a8", [(645, 365), (645, 405)]),
        text("out", 645, 430, "답 + 출처 [E01 p.2]", 16, "#1e1e1e", anchor="middle"),
        text("n1", 60, 420, "파랑 = 학생 코드가 고정한 흐름 · 모델은 이 흐름을 판단하지 않는다", 14, "#595959"),
        text("n2", 60, 445, "초록 = 문서·데이터 저장소   (몇 번 검색할지도 학생이 정한다)", 14, "#757575"),
    ],
)

FIG2 = dict(
    name="02-청크-경계", w=800, h=440,
    title="한 쪽(Document)이 청크로 나뉘는 방식 — 겹침(overlap)이 경계의 문장을 살린다",
    elements=[
        box("page", 40, 60, 720, 50, "E01 p.3 — Document 하나 (약 1,100자)   metadata: {doc_id: E01, page: 3}", GREEN, fs=15),
        arrow("d1", [(200, 110), (200, 160)]),
        text("d1t", 215, 135, "RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)", 14, "#2563eb"),
        box("c3", 40, 165, 340, 68, "청크 #3 (498자)\n…3일 늦게 반납하면 반납일부터 3일 동안 새로\n대출할 수 없습니다. 연체료(금전)는 받지 않습니다.", BLUE, fs=14),
        box("c4", 330, 245, 340, 68, "청크 #4\n동안 새로 대출할 수 없습니다. 연체료(금전)는\n받지 않습니다. 자료를 분실하거나 훼손했을 때는…", BLUE, fs=14),
        box("c5", 640, 245, 120, 68, "청크 #5 …", BLUE, fs=14),
        zone("ov", 330, 160, 50, 150, ZONE_YELLOW, ""),
        text("ovt", 355, 325, "겹침 50자", 14, "#92400e", anchor="middle"),
        text("m1", 40, 360, "청크마다 metadata가 복사된다 → {doc_id: E01, page: 3, chunk_id: 3}", 15, "#15803d"),
        text("m2", 40, 390, "경계에 걸린 문장은 두 청크에 모두 들어간다. 겹침이 0이면 문장이 반으로 잘린 채 색인된다.", 14, "#757575"),
        text("m3", 40, 415, "500은 '글자 수'다. 같은 500자가 토큰으로는 약 430개였다(02절 실행 결과).", 14, "#757575"),
    ],
)

FIG3 = dict(
    name="03-벡터-검색", w=800, h=480,
    title="top-k 검색 — 질문 벡터와 가까운 청크 벡터 k개를 고른다 (점수 = 코사인 유사도)",
    elements=[
        zone("sp", 40, 60, 480, 380, ZONE_GREEN, "임베딩 공간 (1,536차원을 2차원으로 그린 것)"),
        dot("p1", 200, 200, 10, GREEN, "E01 p.1 표지 0.649"),
        dot("p2", 250, 250, 10, GREEN, "E01 p.2 이용시간 0.565"),
        dot("p3", 150, 300, 10, GREEN, "M04 p.3 0.494"),
        dot("p4", 310, 305, 10, GREEN, "H03 p.2 0.464"),
        dot("p5", 420, 130, 8, GREEN, "E05 p.3"),
        dot("p6", 460, 380, 8, GREEN, "M02 p.4"),
        dot("p7", 90, 130, 8, GREEN, "H06 p.6"),
        dot("q", 230, 230, 12, BLUE, ""),
        text("ql", 175, 222, "질문 ★", 15, "#2563eb"),
        {"kind": "circle", "id": "kc", "x": 230, "y": 230, "r": 125, "stroke": "#4a9eed"},
        text("kl", 290, 120, "k=4 범위", 14, "#2563eb"),
        box("s1", 560, 80, 210, 60, "질문 → embed_query()\n→ 1,536차원 벡터", BLUE, fs=14),
        arrow("a1", [(560, 110), (345, 220)], color="#4a9eed", label="", dashed=True),
        box("s2", 560, 170, 210, 90, "similarity_search_with_score\n(query, k=4)\n→ [(청크, 점수)] × 4", BLUE, fs=14),
        box("s3", 560, 290, 210, 70, "표지 청크가 1위 —\n제목 단어만 겹쳐도 점수가 높다", RED, fs=14),
        box("s4", 560, 380, 210, 55, "답은 2위 청크에 있었다\n→ k를 1로 두면 놓친다", YELLOW, fs=14),
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
        arrow("a3", [(340, 255), (450, 360)], color="#757575", label="문서에 애초에 없음", fs=14),
        box("r1", 450, 85, 130, 70, "LLM", BLUE),
        box("r2", 450, 200, 130, 70, "LLM", BLUE),
        box("r3", 450, 325, 130, 70, "LLM", BLUE),
        arrow("b1", [(580, 120), (620, 120)]),
        arrow("b2", [(580, 235), (620, 235)]),
        arrow("b3", [(580, 360), (620, 360)]),
        box("o1", 620, 85, 160, 70, "정답 + 출처\n[E01 p.2]", GREEN, fs=15),
        zone("z", 610, 190, 180, 215, ZONE_YELLOW, ""),
        box("o2", 620, 200, 160, 70, "\"찾을 수 없습니다\"\n또는 지어낸 숫자", RED, fs=14),
        box("o3", 620, 325, 160, 70, "\"찾을 수 없습니다\"\n(이건 정답)", YELLOW, fs=14),
        text("n1", 40, 440, "가운데와 아래 출력이 같은 문자열이다. 정답 문서 ID가 없으면 둘을 구분할 방법이 없다 → Ch 11 질의셋·Recall@k", 14, "#1e1e1e"),
        text("n2", 40, 465, "'모르면 모른다' 프롬프트는 빨간 경로의 '지어낸 숫자'만 줄인다. 검색 자체는 못 고친다 → Ch 12", 14, "#757575"),
        text("n3", 40, 490, "프롬프트로 세운 규칙은 문서 안 지시문으로 뒤집힐 수 있다 → Ch 16 가드레일", 14, "#757575"),
    ],
)

FIG5 = dict(
    name="06-하네스-루프", w=800, h=470,
    title="실험 하네스 — 설정 바꾸기 → 실행 → 한 줄 기록, 한 명령으로",
    elements=[
        box("cfg", 40, 100, 170, 80, "config.yaml\nchunk_size · k · 모델 · 프롬프트", BLUE, fs=14),
        arrow("a1", [(210, 140), (270, 140)]),
        text("a1t", 240, 88, "--set a.b=값", 14, "#2563eb", anchor="middle"),
        box("h", 270, 100, 170, 80, "harness.py\n설정 해시로 색인 캐시 판단", BLUE, fs=14),
        arrow("a2", [(355, 180), (355, 230)], color="#22c55e", label="같은 설정이면 재사용", dashed=True),
        box("idx", 270, 230, 170, 70, ".cache/index-{hash}.json\n색인(임베딩 결과)", TEAL, fs=14),
        arrow("a3", [(440, 140), (500, 140)]),
        text("a3t", 470, 88, "질의셋 N개 실행", 14, "#2563eb", anchor="middle"),
        box("run", 500, 100, 150, 80, "search → generate\n(rag.py 함수 그대로)", BLUE, fs=14),
        arrow("a4", [(575, 180), (575, 230)], color="#f59e0b"),
        box("log", 480, 230, 190, 70, "runs/runs.jsonl 에 한 줄\n설정·규모·시간·토큰·비용", YELLOW, fs=14),
        box("det", 480, 320, 190, 60, "runs/{run_id}.jsonl\n질문별 검색 결과·답변", YELLOW, fs=14),
        arrow("a5", [(575, 300), (575, 320)], color="#f59e0b"),
        box("met", 690, 230, 90, 70, "metrics: {}\nCh 11", YELLOW, fs=14, dashed=True),
        arrow("a6", [(480, 280), (455, 280), (455, 335), (125, 335), (125, 180)], color="#4a9eed",
              dashed=True),
        text("a6t", 290, 355, "한 줄 읽고 → 다음 가설 → 설정 수정 → 다시 실행", 14, "#2563eb", anchor="middle"),
        text("n1", 40, 420, "한 번 도는 데 걸리는 시간이 실험 횟수를 정한다. Ch 12는 5일 동안 이 루프를 30번 이상 돈다.", 14, "#757575"),
        text("n2", 40, 445, "지금 로그에는 지표가 없다 — 답이 좋아졌는지는 아직 눈으로 본다. 그 칸을 Ch 11이 채운다.", 14, "#757575"),
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
