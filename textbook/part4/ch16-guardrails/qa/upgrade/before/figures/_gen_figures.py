"""절별 도식 정본: 같은 요소에서 SVG와 Excalidraw를 생성합니다."""

from __future__ import annotations

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLORS = {
    "data": "#DDEDE8",
    "code": "#DDEAF4",
    "model": "#E9E0F3",
    "metric": "#F7EDC7",
    "failure": "#F4D9D5",
}


def common(ident, kind, x, y, w, h):
    return {
        "id": ident,
        "type": kind,
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": "#334155",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": 1,
        "version": 1,
        "versionNonce": 1,
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
    }


def make(name, nodes, edges):
    elements = []
    shapes = []
    positions = {}
    marker = name + "-arrow"
    for ident, label, role, col, row in nodes:
        x, w = (
            (16, 328)
            if col == -1
            else (
                (10 + int(col[1]) * 118, 104)
                if isinstance(col, str)
                else (16 + col * 180, 148)
            )
        )
        y, h = 16 + row * 118, 78
        positions[ident] = (x, y, w, h)
        box = common(name + "-" + ident, "rectangle", x, y, w, h)
        box.update(
            backgroundColor=COLORS[role], roundness={"type": 3}, boundElements=[]
        )
        elements.append(box)
        shapes.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{COLORS[role]}" stroke="#334155" stroke-width="2"/>'
        )
        lines = label.split("|")
        for n, line in enumerate(lines):
            ly = y + (h - len(lines) * 26) / 2 + n * 26
            tid = name + "-" + ident + "-text-" + str(n)
            text = common(tid, "text", x + 5, ly, w - 10, 26)
            text.update(
                strokeColor="#172033",
                text=line,
                originalText=line,
                fontSize=20,
                fontFamily=1,
                textAlign="center",
                verticalAlign="middle",
                containerId=None,
                autoResize=True,
                lineHeight=1.3,
            )
            elements.append(text)
            shapes.append(
                f'<text x="{x + w / 2}" y="{ly + 20}" text-anchor="middle" font-size="20" font-family="sans-serif" fill="#172033">{html.escape(line)}</text>'
            )
    for i, (start, end) in enumerate(edges):
        x, y, w, h = positions[start]
        xx, yy, ww, _hh = positions[end]
        sx, sy = x + w / 2, y + h + 3
        ex, ey = xx + ww / 2, yy - 5
        mid = (sy + ey) / 2
        points = (
            [[0, 0], [0, mid - sy], [ex - sx, mid - sy], [ex - sx, ey - sy]]
            if sx != ex
            else [[0, 0], [0, ey - sy]]
        )
        if any(
            ry > sy and ry + rh < ey and rx < sx < rx + rw
            for rx, ry, rw, rh in positions.values()
        ):
            points = [
                [0, 0],
                [6 - sx, 0],
                [6 - sx, ey - sy - 8],
                [ex - sx, ey - sy - 8],
                [ex - sx, ey - sy],
            ]
        arrow = common(
            name + "-edge-" + str(i), "arrow", sx, sy, abs(ex - sx), abs(ey - sy)
        )
        arrow.update(
            points=points,
            startBinding=None,
            endBinding=None,
            startArrowhead=None,
            endArrowhead="arrow",
            elbowed=False,
        )
        elements.append(arrow)
        command = " ".join(
            ("M" if j == 0 else "L") + f"{sx + px} {sy + py}"
            for j, (px, py) in enumerate(points)
        )
        shapes.append(
            f'<path d="{command}" fill="none" stroke="#334155" stroke-width="2" marker-end="url(#{marker})"/>'
        )
    height = 32 + (max(n[4] for n in nodes) + 1) * 118 - 40
    description = " / ".join(n[1].replace("|", " ") for n in nodes)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 {height}" style="width:360px;max-width:100%;height:auto;display:block;margin:0 auto" role="img" aria-label="{html.escape(description, quote=True)}"><title>{html.escape(description)}</title><defs><marker id="{marker}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#334155"/></marker></defs>'
        + "".join(shapes)
        + "</svg>"
    )
    editable = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": {},
    }
    return svg, editable


def main():
    for name, (nodes, edges) in FIGURES.items():
        assert len(nodes) <= 7
        svg, drawing = make(name, nodes, edges)
        (HERE / (name + ".svg")).write_text(svg)
        (HERE / (name + ".excalidraw")).write_text(
            json.dumps(drawing, ensure_ascii=False, indent=2) + "\n"
        )
        caption = CAPTIONS[name] + "\n\n"
        caption += "초록은 자료, 파랑은 코드로 정한 처리, 보라는 모델 계산, 노랑은 측정·평가, 빨강은 오류·격리를 나타냅니다.\n"
        (HERE / (name + ".caption.md")).write_text(caption)
    print(f"{len(FIGURES)} figures generated")


CAPTIONS={'01-흐름': '질문이 비어 있거나 길이 제한을 넘었는지 확인한 뒤 모델을 호출합니다. 답변의 출처 ID와 쪽 번호를 허용 목록과 대조하며, 목록에 없는 출처는 '
          '오류로 처리합니다. 이 검사는 답변 내용 전체의 진위를 판정하지 않습니다.',
 '02-흐름': '합성 문장에서 정해 둔 전화번호·이메일 등의 형식을 찾아 마스킹합니다. 변경된 문장과 탐지 수를 확인한 뒤, 규칙이 찾지 못하는 형식도 살펴봅니다. '
          '모든 개인정보를 탐지한 결과로 확대하지 않습니다.',
 '03-흐름': '시스템 정책을 별도로 유지하면서 오래된 대화를 자르거나 모델로 요약합니다. 요약은 최근 대화와 함께 참고 자료로 전달하며, 정리 전후에 조건이 '
          '보존됐는지와 글자 수가 어떻게 달라졌는지를 확인합니다.',
 '04-흐름': '현재 호출 수와 예상 비용에 다음 호출을 더한 값을 상한과 비교합니다. 제한을 넘으면 호출 전에 중단합니다. 이때 누적하는 계획 비용은 실제 '
          '청구액과 구분해 확인합니다.',
 '05-흐름': '주 처리의 응답을 반환하거나, 허용한 오류일 때 정한 횟수 안에서 재시도합니다. 재시도를 소진하면 폴백을 실행하고 결정과 오류를 감사 기록에 '
          '남깁니다. 각 실험에서 실제로 실행한 경로를 출력으로 확인합니다.',
 '06-흐름': '검색 문서에 의심 문구가 하나라도 있으면 통합 모듈은 요청 전체를 중단합니다. 의심 문구를 찾지 못한 문서는 자료로 구분해 모델에 전달하고 출처와 '
          '기록을 확인합니다. 탐지 규칙의 통과를 모든 공격에 대한 안전 판정으로 취급하지 않습니다.'}

FIGURES={'01-흐름': ([('a', '입력 질문', 'data', -1, 0),
            ('b', '빈값·길이 확인', 'code', -1, 1),
            ('c', '문서를 넣어 답변 생성', 'model', -1, 2),
            ('d', '출처 ID·쪽 번호|허용 목록과 대조', 'code', -1, 3),
            ('e', '허용된 출처', 'metric', 0, 4),
            ('f', '없는 출처|오류로 중단', 'failure', 1, 4)],
           [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('d', 'f')]),
 '02-흐름': ([('a', '합성 개인정보 문장', 'data', -1, 0),
            ('b', '정해 둔 형식 탐지|전화 · 이메일 등', 'code', -1, 1),
            ('c', '찾은 부분을 마스킹', 'code', -1, 2),
            ('d', '마스킹 문장·탐지 수', 'metric', -1, 3),
            ('e', '찾지 못한 형식도 확인', 'failure', -1, 4)],
           [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')]),
 '03-흐름': ([('a', '시스템 정책·대화 기록', 'data', -1, 0),
            ('b', '시스템 정책|별도로 유지', 'code', 0, 1),
            ('c', '오래된 대화|자르거나 요약', 'model', 1, 1),
            ('d', '최근 대화와 조합|요약은 참고 자료', 'code', -1, 2),
            ('e', '보존·누락된 조건 확인', 'metric', -1, 3)],
           [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'), ('d', 'e')]),
 '04-흐름': ([('a', '호출 횟수·예상 비용', 'data', -1, 0),
            ('b', '다음 호출을 더해|상한과 비교', 'code', -1, 1),
            ('c', '상한 이내|호출 허용', 'code', 0, 2),
            ('d', '상한 초과|호출 전 중단', 'failure', 1, 2),
            ('e', '계획 비용과 실제 비용|구분해 확인', 'metric', -1, 3)],
           [('a', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'e'), ('d', 'e')]),
 '05-흐름': ([('a', '주 처리 호출', 'code', -1, 0),
            ('b', '정상 응답|반환', 'data', 0, 1),
            ('c', '허용한 오류|횟수 내 재시도', 'code', 1, 1),
            ('d', '재시도 소진|폴백 실행', 'code', 1, 2),
            ('e', '결정·오류를 감사 기록|민감 원문은 제외', 'metric', -1, 3)],
           [('a', 'b'), ('a', 'c'), ('c', 'd'), ('b', 'e'), ('d', 'e')]),
 '06-흐름': ([('a', '검색된 문서|신뢰하지 않는 입력', 'data', -1, 0),
            ('b', '공격 문구 탐지', 'code', -1, 1),
            ('c', '의심 문서|전체 요청 중단', 'failure', 0, 2),
            ('d', '의심 없음|자료로 구분', 'code', 1, 2),
            ('e', '모델 답변 생성', 'model', 1, 3),
            ('f', '출처·응답·기록 확인', 'metric', -1, 4)],
           [('a', 'b'), ('b', 'c'), ('b', 'd'), ('d', 'e'), ('e', 'f')])}

if __name__ == "__main__":
    main()
