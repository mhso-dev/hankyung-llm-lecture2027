"""Ch 10 도식 생성기 — 한 요소 목록에서 SVG와 Excalidraw 원본을 함께 만든다.

색 규칙(AGENTS.md §16): 학생 흐름=파랑, 도구·데이터=초록,
측정·평가=노랑, 실패=빨강. 이 장의 임베딩은 모델 판단이 아니므로 보라색을 쓰지 않는다.
실행: python _gen_figures.py  (표준 라이브러리만 사용)
"""

from __future__ import annotations

# 품질 개선(2026-09-18, Ch10 01절, QUALITY-UPGRADE.md §8·PLAYBOOK §2-1): 이 옛 도식 생성기는 실행하지 않습니다.
# 개선한 절의 도식은 figures/NN-k-이름.mmd 를 textbook/_notebook/mermaid/render_mermaid.py 로 렌더해 만듭니다.
# 이 파일을 실행하면 아직 개선하지 않은 02~08절이 쓰는 옛 SVG와 Excalidraw까지 다시 써서 개선본과 섞입니다.
# 챕터를 마감할 때 qa/upgrade/before/generators/ 로 옮깁니다(삭제하지 않습니다).
raise SystemExit("Ch 10 품질 개선 뒤에는 이 도식 생성기를 실행하지 않습니다. render_mermaid.py 를 쓰세요.")

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

BLUE = ("#a5d8ff", "#4a9eed")
GREEN = ("#b2f2bb", "#22c55e")
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


def text(id_, x, y, s, fs=15, color="#1e1e1e", anchor="start"):
    return {"kind": "text", "id": id_, "x": x, "y": y, "text": s, "fs": fs,
            "color": color, "anchor": anchor}


# ------------------------------------------------------------------ 도식 정의
FIG1 = dict(
    name="01-문서-계약", w=900, h=350,
    title="파일에서 읽은 내용과 출처를 후속 두 칸에 옮길 준비",
    alt="파일별로 본문과 출처를 확인한 뒤 후속 단계의 page_content와 metadata에 옮기는 흐름",
    caption="01절은 출처를 준비하고 02~04절은 본문과 구조를 읽습니다. 후속 단계에서 두 결과를 Document의 두 칸에 옮깁니다.",
    elements=[
        box("source", 40, 120, 150, 80, "원본 파일\nPDF · DOCX · HTML", GREEN, fs=15),
        arrow("a1", [(190, 160), (265, 160)], label="읽기"),
        box("loader", 265, 120, 150, 80, "01 출처 준비\n02~04 내용 읽기", BLUE, fs=14),
        arrow("a2", [(415, 160), (500, 160)], label="후속 단계"),
        zone("contract", 500, 75, 360, 180, ZONE_GREEN, "Document로 옮길 두 칸"),
        box("text", 530, 125, 135, 80, "page_content\n본문 문자열", GREEN, fs=14),
        box("meta", 695, 125, 135, 80, "metadata\n출처 · 쪽 · 형식", GREEN, fs=14),
        text("note", 450, 300, "01~04절 기본 노트북은 두 칸에 옮길 값까지 확인합니다.", 15, "#595959", "middle"),
    ],
)

FIG2 = dict(
    name="02-표-구조", w=900, h=440,
    title="표를 텍스트로 바꿀 때 — 머리글과 행의 대응을 보존한다",
    alt="같은 표가 구조 손실 경로에서는 값만 나열되고 구조 보존 경로에서는 각 행에 머리글이 반복되는 비교",
    caption="표의 각 값을 어느 열의 값인지 알 수 있게 변환해야 검색 결과만 읽어도 행의 의미가 유지됩니다.",
    elements=[
        box("table", 35, 155, 170, 110, "원본 표\n이름 | 부서 | 역할\n민수 | 개발 | 백엔드", GREEN, fs=14),
        arrow("lost_a", [(205, 180), (310, 115)], color="#ef4444", label="셀만 추출"),
        arrow("keep_a", [(205, 235), (310, 315)], color="#22c55e", label="행 단위 변환"),
        zone("lost_z", 310, 65, 545, 135, ZONE_RED, "구조 손실"),
        box("lost", 345, 105, 205, 65, "민수 개발 백엔드", RED),
        box("lost_mean", 590, 105, 225, 65, "각 값의 열을\n확인하기 어렵습니다", RED, fs=14),
        zone("keep_z", 310, 245, 545, 145, ZONE_GREEN, "구조 보존"),
        box("keep", 345, 295, 235, 65, "이름: 민수\n부서: 개발 | 역할: 백엔드", GREEN, fs=14),
        box("keep_mean", 620, 295, 195, 65, "머리글과 값의\n대응이 남습니다", GREEN, fs=14),
    ],
)

FIG3 = dict(
    name="03-형식별-단위", w=900, h=430,
    title="문서 형식마다 의미 있는 단위가 다르다",
    alt="DOCX는 문단과 표, HTML은 제목과 본문, CSV는 머리글이 붙은 행으로 변환되는 세 경로",
    caption="파일을 같은 문자열로 평탄화하기 전에 형식이 가진 구조를 의미 있는 단위로 변환합니다.",
    elements=[
        box("docx", 50, 90, 150, 65, "DOCX", GREEN),
        box("html", 50, 185, 150, 65, "HTML", GREEN),
        box("csv", 50, 280, 150, 65, "CSV", GREEN),
        arrow("a1", [(200, 122), (320, 122)], label="구조 읽기"),
        arrow("a2", [(200, 217), (320, 217)], label="구조 읽기"),
        arrow("a3", [(200, 312), (320, 312)], label="구조 읽기"),
        box("docx_u", 320, 80, 240, 85, "문단 + 표\n스타일 · 표 위치 메타데이터", BLUE, fs=14),
        box("html_u", 320, 175, 240, 85, "제목 + 본문\nh1~h6 계층 · URL", BLUE, fs=14),
        box("csv_u", 320, 270, 240, 85, "머리글이 붙은 행\n행 번호 · 열 이름", BLUE, fs=14),
        arrow("join1", [(560, 122), (690, 217)], color="#22c55e"),
        arrow("join2", [(560, 217), (690, 217)], color="#22c55e"),
        arrow("join3", [(560, 312), (690, 217)], color="#22c55e"),
        box("contract", 690, 170, 170, 95, "타입이 있는 단위\ntext + type + source", GREEN, fs=14),
        text("note", 450, 390, "형식의 구조를 보존하면 청킹 기준과 출처 표시를 문서 유형에 맞게 선택할 수 있습니다.", 15, "#595959", "middle"),
    ],
)

FIG4 = dict(
    name="04-hwp-hwpx", w=900, h=430,
    title="HWP와 HWPX는 확장자뿐 아니라 내부 구조가 다르다",
    alt="HWP는 전용 파서가 필요하다고 분류하고 HWPX는 ZIP 안의 본문 XML을 읽습니다. Document 변환은 후속 단계입니다.",
    caption="HWP는 바이너리 전용 파서가 필요하고, HWPX는 ZIP 안의 XML을 읽으므로 내부가 ZIP인지 확인한 뒤 알맞은 읽기 방법을 선택합니다.",
    elements=[
        box("input", 45, 165, 145, 75, "한글 문서", GREEN),
        arrow("to_branch", [(190, 202), (285, 202)]),
        box("branch", 285, 165, 145, 75, "형식 판별\n확장자 + 매직 바이트", BLUE, fs=14),
        arrow("hwp_a", [(430, 185), (535, 115)], label=".hwp"),
        arrow("hwpx_a", [(430, 220), (535, 300)], label=".hwpx"),
        zone("hwp_z", 535, 60, 250, 130, ZONE_RED, "HWP 경로"),
        box("hwp", 560, 105, 200, 60, "미지원으로 분류\n전용 파서 필요", RED, fs=14),
        zone("hwpx_z", 535, 245, 250, 130, ZONE_GREEN, "HWPX 경로"),
        box("hwpx", 560, 290, 200, 60, "본문 XML만 선택\n문자열 추출", GREEN, fs=14),
        arrow("out1", [(760, 135), (805, 190)], color="#22c55e"),
        arrow("out2", [(760, 320), (805, 225)], color="#22c55e"),
        box("out", 805, 175, 85, 65, "후속 단계\nDocument\n변환", GREEN, fs=14),
        text("note", 450, 405, "HWPX를 일반 XML 파일로 가정하거나 HWP를 텍스트 파일처럼 열면 본문 순서를 복원할 수 없습니다.", 14, "#595959", "middle"),
    ],
)

FIG5 = dict(
    name="05-청크-경계", w=900, h=470,
    title="같은 원문을 문자·재귀·토큰 기준으로 나누기",
    alt="같은 문서를 문자 수, 토큰 수, 재귀 구분자 기준으로 자르는 방법과 겹침 구간을 비교한 도식",
    caption="문자 수와 토큰 수는 같은 숫자라도 경계가 다르며, 재귀 분할은 문단과 문장 구분자를 우선 사용합니다.",
    elements=[
        box("doc", 45, 75, 810, 55, "원문: 첫 문단 …… 문장 A. 문장 B. …… 둘째 문단 …… 문장 C.", GREEN, fs=14),
        zone("char_z", 45, 165, 250, 205, ZONE_BLUE, "문자 수 기준"),
        box("char1", 70, 220, 125, 60, "목표 35자", BLUE),
        box("char2", 145, 290, 125, 60, "겹침 5자", YELLOW, fs=14),
        zone("token_z", 325, 165, 250, 205, ZONE_BLUE, "토큰 수 기준"),
        box("token1", 350, 220, 125, 60, "목표 20토큰", BLUE),
        box("token2", 425, 290, 125, 60, "겹침 4토큰", YELLOW, fs=14),
        zone("rec_z", 605, 165, 250, 205, ZONE_GREEN, "재귀 구분자 기준"),
        box("rec1", 630, 220, 200, 60, "문단 → 문장 → 공백\n→ 문자 순으로 분할", GREEN, fs=14),
        box("rec2", 655, 300, 150, 45, "35자 → 50자 비교", BLUE, fs=14),
        text("note", 450, 420, "겹침은 경계의 문맥을 남기지만, 중복 문장이 늘어 처리량이 커질 수 있습니다.", 15, "#595959", "middle"),
    ],
)

FIG6 = dict(
    name="06-구조-의미-청킹", w=900, h=455,
    title="구조 청킹과 의미 청킹 — 경계를 정하는 신호가 다르다",
    alt="제목 계층을 따라 나누는 구조 청킹과 문장 임베딩 거리의 임계값을 따라 나누는 의미 청킹의 비교",
    caption="구조 청킹은 문서 작성자가 남긴 제목을 사용하고, 의미 청킹은 인접 문장의 임베딩 거리가 임계값을 넘는 지점을 사용합니다.",
    elements=[
        zone("struct_z", 45, 70, 380, 300, ZONE_GREEN, "구조 청킹"),
        box("head", 80, 125, 145, 70, "제목 계층\nH1 → H2 → H3", GREEN, fs=14),
        arrow("s_a", [(225, 160), (280, 160)], color="#22c55e", label="경계"),
        box("sections", 280, 125, 110, 70, "절 단위\n청크", BLUE, fs=14),
        text("s_note", 80, 245, "장점: 출처와 문서 논리가 선명합니다.", 14, "#15803d"),
        text("s_note2", 80, 280, "조건: 제목 구조가 일관되어야 합니다.", 14, "#595959"),
        zone("semantic_z", 475, 70, 380, 300, ZONE_YELLOW, "의미 청킹"),
        box("sent", 510, 125, 145, 70, "인접 문장\n임베딩 거리", GREEN, fs=14),
        arrow("m_a", [(655, 160), (710, 160)], color="#f59e0b", label="임계값 초과"),
        box("meaning", 710, 125, 110, 70, "의미 전환\n경계", YELLOW, fs=14),
        text("m_note", 510, 245, "장점: 제목이 없는 본문의 전환을 찾습니다.", 14, "#b45309"),
        text("m_note2", 510, 280, "설정: 임베딩 모델과 나누는 기준값을 정합니다.", 14, "#595959"),
        text("note", 450, 415, "두 방법은 모델의 답변 판단이 아니라, 학생이 선택한 규칙과 측정 기준으로 청크 경계를 만듭니다.", 15, "#595959", "middle"),
    ],
)

FIG7 = dict(
    name="07-임베딩-캐시", w=900, h=470,
    title="캐시 이름에 어떤 설정을 구분해 넣어야 할까요?",
    alt="본문 해시, 임베딩 모델, 벡터 차원, 전처리 버전으로 캐시 키를 만들고 일치하면 히트, 하나라도 다르면 미스로 분기하는 흐름",
    caption="본문과 모델 설정을 구분해 저장하는 설계입니다. 모델·차원·전처리 조건이 바뀌면 캐시 이름에도 반영해야 합니다.",
    elements=[
        box("text", 45, 80, 170, 60, "본문 해시", GREEN),
        box("model", 45, 155, 170, 60, "임베딩 모델", GREEN),
        box("dim", 45, 230, 170, 60, "벡터 차원", GREEN),
        box("ver", 45, 305, 170, 60, "전처리 버전", GREEN),
        arrow("a1", [(215, 110), (350, 220)], color="#22c55e"),
        arrow("a2", [(215, 185), (350, 220)], color="#22c55e"),
        arrow("a3", [(215, 260), (350, 220)], color="#22c55e"),
        arrow("a4", [(215, 335), (350, 220)], color="#22c55e"),
        box("key", 350, 175, 180, 90, "캐시 키\n(text, model, dim, version)", BLUE, fs=14),
        arrow("hit_a", [(530, 200), (650, 125)], color="#22c55e", label="완전 일치"),
        arrow("miss_a", [(530, 240), (650, 320)], color="#ef4444", label="하나라도 변경"),
        box("hit", 650, 85, 200, 80, "캐시 히트\n저장한 벡터 재사용", GREEN, fs=14),
        box("miss", 650, 280, 200, 80, "캐시 미스\n새 임베딩 계산·저장", RED, fs=14),
        text("note", 450, 425, "실습: namespace에 차원을 빼면 128차원 설정에서도 예전 256차원 벡터를 읽습니다.", 14, "#595959", "middle"),
    ],
)

FIG8 = dict(
    name="08-실험-격자", w=900, h=470,
    title="세 번 실행해 한 조건씩 비교하기",
    alt="같은 원문과 질문에서 45자 small 모델, 30자 small 모델, 30자 large 모델을 차례로 실행하는 비교 순서",
    caption="같은 원문과 질문을 유지하고, 먼저 청크 크기만 바꾼 뒤 같은 30자 청크에서 모델만 바꾸어 비교합니다.",
    elements=[
        box("fixed", 45, 130, 150, 80, "고정값\n원문 · 질문 · k=2", GREEN, fs=14),
        arrow("a1", [(205, 170), (275, 170)]),
        box("base", 275, 115, 155, 110, "기준 실행\n45자 · small", BLUE, fs=14),
        arrow("a2", [(430, 170), (520, 170)], label="크기만 변경"),
        box("small", 520, 115, 155, 110, "청킹 변경\n30자 · small", YELLOW, fs=14),
        arrow("a3", [(675, 170), (765, 170)], label="모델만 변경"),
        box("large", 765, 115, 110, 110, "모델 변경\n30자 · large", RED, fs=14),
        zone("compare1", 245, 270, 450, 70, ZONE_BLUE, "청크 크기 효과: 기준 실행 ↔ 청킹 변경"),
        zone("compare2", 500, 355, 375, 55, ZONE_YELLOW, "모델 효과: 청킹 변경 ↔ 모델 변경"),
        text("note", 450, 455, "한 번에 한 조건만 바뀐 두 실행을 비교합니다.", 15, "#595959", "middle"),
    ],
)

FIGS = [FIG1, FIG2, FIG3, FIG4, FIG5, FIG6, FIG7, FIG8]


# ------------------------------------------------------------------ SVG
def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


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
        f'font-family="Pretendard, Noto Sans KR, Apple SD Gothic Neo, Malgun Gothic, sans-serif" '
        f'role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(fig["title"])}</title>',
        f'<desc id="desc">{esc(fig["alt"])}</desc>',
        "<defs>",
    ]
    for cid, col in [("blue", "#4a9eed"), ("green", "#22c55e"), ("yellow", "#f59e0b"),
                     ("red", "#ef4444"), ("gray", "#757575")]:
        parts.append(f'<marker id="m-{cid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" '
                     f'markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
    parts.extend(["</defs>", f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
                  svg_text_lines(20, 30, [fig["title"]], 18, "#1e1e1e", "start", "bold")])
    color_id = {"#4a9eed": "blue", "#22c55e": "green", "#f59e0b": "yellow",
                "#ef4444": "red", "#757575": "gray"}
    for e in fig["elements"]:
        k = e["kind"]
        if k == "zone":
            parts.append(f'<rect x="{e["x"]}" y="{e["y"]}" width="{e["w"]}" height="{e["h"]}" rx="12" '
                         f'fill="{e["fill"]}" fill-opacity="0.35" stroke="{e["stroke"]}" stroke-width="1"/>')
            if e["title"]:
                parts.append(svg_text_lines(e["x"] + 14, e["y"] + 18, [e["title"]], e["fs"],
                                            TEXT_BY_STROKE[e["stroke"]], "start"))
        elif k == "box":
            dash = ' stroke-dasharray="6 4"' if e["dashed"] else ""
            parts.append(f'<rect x="{e["x"]}" y="{e["y"]}" width="{e["w"]}" height="{e["h"]}" rx="10" '
                         f'fill="{e["fill"]}" stroke="{e["stroke"]}" stroke-width="2"{dash}/>')
            parts.append(svg_text_lines(e["x"] + e["w"] / 2, e["y"] + e["h"] / 2,
                                        e["text"].split("\n"), e["fs"], "#1e1e1e"))
        elif k == "arrow":
            pts = " ".join(f"{x},{y}" for x, y in e["pts"])
            dash = ' stroke-dasharray="7 5"' if e["dashed"] else ""
            marker = color_id.get(e["color"], "blue")
            parts.append(f'<polyline points="{pts}" fill="none" stroke="{e["color"]}" stroke-width="2" '
                         f'marker-end="url(#m-{marker})"{dash}/>')
            if e["label"]:
                (x1, y1), (x2, y2) = (e["pts"][1], e["pts"][2]) if len(e["pts"]) > 2 else (e["pts"][0], e["pts"][-1])
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 12
                tw = len(e["label"]) * e["fs"] * 0.95 + 12
                parts.append(f'<rect x="{mx - tw / 2:.1f}" y="{my - e["fs"] * 0.75:.1f}" width="{tw:.1f}" '
                             f'height="{e["fs"] * 1.5:.1f}" fill="#ffffff" fill-opacity="0.94" rx="4"/>')
                parts.append(svg_text_lines(mx, my, [e["label"]], e["fs"],
                                            TEXT_BY_STROKE.get(e["color"], "#243142")))
        elif k == "text":
            parts.append(svg_text_lines(e["x"], e["y"], [e["text"]], e["fs"], e["color"], e["anchor"]))
    parts.append("</svg>")
    return "\n".join(parts)


# ------------------------------------------------------------------ Excalidraw JSON
def to_excalidraw(fig) -> dict:
    els = []
    seq = 0

    def base(t, id_, x, y, w, h, **kw):
        nonlocal seq
        seq += 1
        item = {"type": t, "id": id_, "x": x, "y": y, "width": w, "height": h, "angle": 0,
                "strokeColor": "#1e1e1e", "backgroundColor": "transparent", "fillStyle": "solid",
                "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
                "groupIds": [], "frameId": None, "roundness": None, "seed": seq, "version": 1,
                "versionNonce": seq, "isDeleted": False, "boundElements": [], "updated": 0,
                "link": None, "locked": False}
        item.update(kw)
        return item

    def txt(id_, x, y, s, fs, color, align="center"):
        lines = s.split("\n")
        width = max(len(line) for line in lines) * fs
        height = fs * 1.25 * len(lines)
        return base("text", id_, x - (width / 2 if align == "center" else 0), y - height / 2, width, height,
                    text=s, fontSize=fs, fontFamily=1, textAlign=align, verticalAlign="middle",
                    strokeColor=color, originalText=s, lineHeight=1.25, autoResize=True)

    els.append(txt("title", 20, 30, fig["title"], 20, "#1e1e1e", "left"))
    for e in fig["elements"]:
        k = e["kind"]
        if k == "zone":
            els.append(base("rectangle", e["id"], e["x"], e["y"], e["w"], e["h"],
                            backgroundColor=e["fill"], strokeColor=e["stroke"], strokeWidth=1,
                            opacity=35, roundness={"type": 3}))
            if e["title"]:
                els.append(txt(e["id"] + "_t", e["x"] + 14, e["y"] + 18, e["title"], e["fs"],
                               TEXT_BY_STROKE[e["stroke"]], "left"))
        elif k == "box":
            els.append(base("rectangle", e["id"], e["x"], e["y"], e["w"], e["h"],
                            backgroundColor=e["fill"], strokeColor=e["stroke"], roundness={"type": 3},
                            strokeStyle="dashed" if e["dashed"] else "solid"))
            els.append(txt(e["id"] + "_t", e["x"] + e["w"] / 2, e["y"] + e["h"] / 2,
                           e["text"], e["fs"], "#1e1e1e"))
        elif k == "arrow":
            x0, y0 = e["pts"][0]
            pts = [[x - x0, y - y0] for x, y in e["pts"]]
            els.append(base("arrow", e["id"], x0, y0, e["pts"][-1][0] - x0, e["pts"][-1][1] - y0,
                            points=pts, strokeColor=e["color"], endArrowhead="arrow", startArrowhead=None,
                            strokeStyle="dashed" if e["dashed"] else "solid", lastCommittedPoint=None,
                            startBinding=None, endBinding=None, elbowed=False))
            if e["label"]:
                (x1, y1), (x2, y2) = (e["pts"][1], e["pts"][2]) if len(e["pts"]) > 2 else (e["pts"][0], e["pts"][-1])
                els.append(txt(e["id"] + "_l", (x1 + x2) / 2, (y1 + y2) / 2 - 12,
                               e["label"], e["fs"], TEXT_BY_STROKE.get(e["color"], "#243142")))
        elif k == "text":
            els.append(txt(e["id"], e["x"], e["y"], e["text"], e["fs"], e["color"],
                           "left" if e["anchor"] == "start" else "center"))
    return {"type": "excalidraw", "version": 2, "source": "ch10 _gen_figures.py",
            "elements": els, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}


def caption_text(fig) -> str:
    return (f'# {fig["title"]}\n\n'
            f'- 설명 대상: {fig["caption"]}\n'
            f'- 캡션: {fig["caption"]}\n'
            f'- 시선 순서: 왼쪽 입력 → 가운데 변환 또는 비교 → 오른쪽 결과\n'
            f'- alt: {fig["alt"]}\n'
            '- 삽화 판단: 구성 요소와 관계를 정확히 표시해야 하므로 기술 도식이 더 적합합니다.\n')


if __name__ == "__main__":
    for fig in FIGS:
        (HERE / f"{fig['name']}.svg").write_text(to_svg(fig), encoding="utf-8")
        (HERE / f"{fig['name']}.excalidraw").write_text(
            json.dumps(to_excalidraw(fig), ensure_ascii=False, indent=1), encoding="utf-8")
        (HERE / f"{fig['name']}.caption.md").write_text(caption_text(fig), encoding="utf-8")
        print("wrote", fig["name"])
