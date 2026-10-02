"""Ch 4 도식을 같은 요소 목록에서 SVG와 Excalidraw JSON으로 생성합니다."""

from __future__ import annotations

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLORS = {
    "blue": ("#dbeafe", "#2563eb"),
    "green": ("#dcfce7", "#16a34a"),
    "yellow": ("#fef3c7", "#d97706"),
    "red": ("#fee2e2", "#dc2626"),
}

FIGURES = [
    ("01-dataframe-flow", "조건 선택과 자료형 확인", [
        (30, 75, 160, 70, "주문 3행\n금액: 정수", "green"),
        (280, 75, 160, 70, "status == paid\n행·열 선택", "blue"),
        (530, 75, 160, 70, "O101·O103\n합계 59,000", "yellow"),
        (280, 185, 160, 55, "금액: 문자열\n잘못된 연결", "red"),
    ]),
    ("02-relational-keys", "기본 키와 외래 키", [
        (30, 75, 180, 80, "고객 표\nC001은 한 행", "green"),
        (270, 75, 180, 80, "주문 표\nC001은 두 행", "green"),
        (510, 75, 180, 80, "many_to_one\n결과 3행", "yellow"),
        (270, 185, 180, 55, "고객 키 중복\n결과 5행", "red"),
    ]),
    ("03-sql-query", "SQL 조회 함수의 경계", [
        (30, 75, 160, 70, "database +\ncustomer_id", "green"),
        (280, 75, 160, 70, "SELECT·JOIN\nWHERE·ORDER BY", "blue"),
        (530, 75, 160, 70, "사전 목록\nO101·O103", "green"),
        (280, 185, 160, 55, "문자열 결합\n조건식 변경", "red"),
    ]),
    ("04-rest-pagination", "REST 페이지네이션 종료", [
        (30, 75, 180, 80, "GET page=1\nA01·A02", "green"),
        (270, 75, 180, 80, "next_page=2\nGET page=2", "blue"),
        (510, 75, 180, 80, "3건 확인\nnext_page=None", "yellow"),
        (270, 185, 180, 55, "첫 페이지만 읽음\nA03 누락", "red"),
    ]),
    ("05-document-parsing", "HTML 구조에서 필드 추출", [
        (30, 75, 180, 80, "HTML 원문\narticle·h1·time", "green"),
        (270, 75, 180, 80, "lxml 파서\n요소 트리", "blue"),
        (510, 75, 180, 80, "id·title·summary\npublished", "green"),
        (270, 185, 180, 55, "없는 선택자\nNone 확인", "red"),
    ]),
]


def svg(name: str, title: str, boxes: list[tuple]) -> str:
    parts = [
        '<svg style="min-width:720px" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 270" width="720" height="270" role="img"',
        f' aria-labelledby="title-{name} desc-{name}">',
        f'<title id="title-{name}">{html.escape(title)}</title>',
        f'<desc id="desc-{name}">파란 입력에서 노란 처리를 거쳐 초록 결과가 나오며 빨간 상자는 실패 사례를 나타냅니다.</desc>',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#2563eb"/></marker></defs>',
        '<rect width="720" height="270" fill="#fff"/>',
        f'<text x="24" y="35" font-size="20" font-weight="700" fill="#111827">{html.escape(title)}</text>',
        '<path d="M210 110H265" stroke="#2563eb" stroke-width="3" marker-end="url(#arrow)"/>',
        '<path d="M450 110H505" stroke="#2563eb" stroke-width="3" marker-end="url(#arrow)"/>',
        '<path d="M360 155V180" stroke="#dc2626" stroke-width="3" marker-end="url(#arrow)"/>',
    ]
    for x, y, w, h, label, color in boxes:
        fill, stroke = COLORS[color]
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        lines = label.split("\n")
        for index, line in enumerate(lines):
            parts.append(f'<text x="{x+w/2}" y="{y+h/2-9+index*23}" text-anchor="middle" font-size="16" fill="#111827">{html.escape(line)}</text>')
    parts.append('</svg>')
    return "\n".join(parts)


def excalidraw(name: str, title: str, boxes: list[tuple]) -> dict:
    elements = []
    for index, (x, y, w, h, label, color) in enumerate(boxes, 1):
        fill, stroke = COLORS[color]
        elements.append({"type":"rectangle","id":f"box-{index}","x":x,"y":y,"width":w,"height":h,
                         "angle":0,"strokeColor":stroke,"backgroundColor":fill,"fillStyle":"solid",
                         "strokeWidth":2,"strokeStyle":"solid","roughness":1,"opacity":100,"groupIds":[],
                         "frameId":None,"roundness":{"type":3},"seed":index,"version":1,"versionNonce":index,
                         "isDeleted":False,"boundElements":[],"updated":0,"link":None,"locked":False})
        elements.append({"type":"text","id":f"text-{index}","x":x+12,"y":y+18,"width":w-24,"height":42,
                         "angle":0,"strokeColor":"#111827","backgroundColor":"transparent","fillStyle":"solid",
                         "strokeWidth":1,"strokeStyle":"solid","roughness":1,"opacity":100,"groupIds":[],
                         "frameId":None,"roundness":None,"seed":index+10,"version":1,"versionNonce":index+10,
                         "isDeleted":False,"boundElements":[],"updated":0,"link":None,"locked":False,
                         "text":label,"fontSize":16,"fontFamily":1,"textAlign":"center","verticalAlign":"middle",
                         "originalText":label,"lineHeight":1.25,"autoResize":True})
    for index, (x, y, dx, dy, color) in enumerate([
        (210, 110, 55, 0, "#2563eb"),
        (450, 110, 55, 0, "#2563eb"),
        (360, 155, 0, 25, "#dc2626"),
    ], 1):
        elements.append({"type":"arrow","id":f"arrow-{index}","x":x,"y":y,"width":dx,"height":dy,
                         "angle":0,"strokeColor":color,"backgroundColor":"transparent","fillStyle":"solid",
                         "strokeWidth":3,"strokeStyle":"solid","roughness":1,"opacity":100,"groupIds":[],
                         "frameId":None,"roundness":{"type":2},"seed":index+30,"version":1,"versionNonce":index+30,
                         "isDeleted":False,"boundElements":[],"updated":0,"link":None,"locked":False,
                         "points":[[0,0],[dx,dy]],"lastCommittedPoint":None,"startBinding":None,"endBinding":None,
                         "startArrowhead":None,"endArrowhead":"arrow","elbowed":False})
    return {"type":"excalidraw","version":2,"source":"ch04 figures/_gen_figures.py",
            "elements":elements,"appState":{"viewBackgroundColor":"#ffffff"},"files":{},
            "metadata":{"title":title,"semanticColors":"blue=learner condition/flow, green=tool/data, yellow=measurement/evaluation, red=failure"}}


for figure_name, figure_title, figure_boxes in FIGURES:
    (HERE / f"{figure_name}.svg").write_text(svg(figure_name, figure_title, figure_boxes), encoding="utf-8")
    (HERE / f"{figure_name}.excalidraw").write_text(
        json.dumps(excalidraw(figure_name, figure_title, figure_boxes), ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", figure_name)
