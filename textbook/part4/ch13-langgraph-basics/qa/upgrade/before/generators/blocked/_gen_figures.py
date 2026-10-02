# 옛 도식 생성기 — 실행하지 마세요 (QUALITY-UPGRADE.md §8, PLAYBOOK §2-1).
# 품질 개선 전 figures/NN-흐름.svg·.excalidraw 를 만들던 파일입니다.
# 지금 절 도식은 figures/NN-k-이름.mmd 를 render_mermaid.py 로 렌더합니다.
# 이 파일을 실행하면 옛 SVG가 다시 생기므로 아래 raise 줄로 실행을 막습니다.
# 챕터 마감 때 qa/upgrade/before/generators/ 로 mv -n 합니다(삭제 아님).
"""절별 도식 정본: 같은 요소에서 SVG와 Excalidraw를 생성합니다."""

from __future__ import annotations

raise SystemExit("옛 도식 생성기입니다. figures/NN-k-이름.mmd 와 render_mermaid.py 를 쓰세요.")

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


CAPTIONS={'01-흐름': '입력한 question의 앞뒤 공백을 normalize에서 제거한 뒤 make_query에서 검색어를 만듭니다. 맨 아래 query와 trace를 '
          '읽어 변환 결과와 두 함수의 실행 순서를 확인합니다.',
 '02-흐름': '노드가 반환한 값 중 query는 새 문자열로 교체하고 log는 리듀서의 규칙에 따라 기록을 누적합니다. 아래 상태를 읽을 때 두 키가 서로 다른 '
          '방식으로 갱신되는지 확인합니다.',
 '03-흐름': '검색 점수를 임계값과 비교한 결과에 따라 답변 경로 또는 보완 경로를 선택합니다. 나란한 두 상자 중 어느 경로를 실행했는지는 맨 아래 실행 '
          '기록으로 확인합니다.',
 '04-흐름': 'add_messages는 새로 받은 메시지의 ID를 기존 목록과 대조합니다. 같은 ID이면 내용을 갱신하고, 새 ID이면 메시지를 추가하므로 목록의 '
          '개수와 내용이 서로 다르게 바뀔 수 있습니다.',
 '05-흐름': 'Send는 문서마다 inspect_document 작업을 만듭니다. 문서가 3건이면 나란한 세 상자에서 길이를 검사하고 결과를 results에 '
          '모읍니다. 입력을 1건으로 바꾸면 검사 작업과 결과도 하나가 됩니다.',
 '06-흐름': 'Command는 상태에 반영할 update와 다음 노드를 가리키는 goto를 함께 반환합니다. 아래 두 상자는 반환값의 두 역할을 구분한 것이며, '
          '맨 아래에서 바뀐 상태와 실제 이동 경로를 확인합니다.',
 '07-흐름': '제공 문서를 임베딩 검색과 BM25로 검색하고 RRF로 후보를 합친 뒤 CrossEncoder로 재정렬합니다. 선택한 본문과 출처를 모델에 전달해 '
          '답변을 생성합니다. 이 그림의 처리 단계와 실제 그래프 노드 이름은 노트북의 Mermaid 출력으로 대조합니다.'}

FIGURES={'01-흐름': ([('a', 'question 입력', 'data', -1, 0),
            ('b', 'normalize|앞뒤 공백 제거', 'code', -1, 1),
            ('c', 'make_query|검색어 작성', 'code', -1, 2),
            ('d', 'query · trace 확인', 'metric', -1, 3)],
           [('a', 'b'), ('b', 'c'), ('c', 'd')]),
 '02-흐름': ([('a', '기존 State|query · log', 'data', -1, 0),
            ('b', '노드 반환값|바꿀 키만 포함', 'code', -1, 1),
            ('c', 'query|새 값으로 교체', 'code', 0, 2),
            ('d', 'log|기록 누적', 'code', 1, 2),
            ('e', '갱신된 State 비교', 'metric', -1, 3)],
           [('a', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'e'), ('d', 'e')]),
 '03-흐름': ([('a', '검색 점수', 'data', -1, 0),
            ('b', '임계값과 비교|조건 함수 실행', 'code', -1, 1),
            ('c', '기준 이상|답변 경로', 'code', 0, 2),
            ('d', '기준 미만|보완 경로', 'code', 1, 2),
            ('e', '선택된 경로 확인', 'metric', -1, 3)],
           [('a', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'e'), ('d', 'e')]),
 '04-흐름': ([('a', '기존 메시지 목록', 'data', -1, 0),
            ('b', '새 메시지의 ID|add_messages', 'code', -1, 1),
            ('c', '같은 ID|메시지 갱신', 'code', 0, 2),
            ('d', '새 ID|목록에 추가', 'code', 1, 2),
            ('e', 'ID별 내용·개수 확인', 'metric', -1, 3)],
           [('a', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'e'), ('d', 'e')]),
 '05-흐름': ([('a', 'documents|문서 3건 또는 1건', 'data', -1, 0),
            ('b', 'Send|문서별 작업 생성', 'code', -1, 1),
            ('c', '문서 1|길이 검사', 'code', 't0', 2),
            ('d', '문서 2|길이 검사', 'code', 't1', 2),
            ('e', '문서 3|길이 검사', 'code', 't2', 2),
            ('f', 'results 리듀서|검사 결과 병합', 'code', -1, 3),
            ('g', '문서 수·결과 개수 확인', 'metric', -1, 4)],
           [('a', 'b'),
            ('b', 'c'),
            ('b', 'd'),
            ('b', 'e'),
            ('c', 'f'),
            ('d', 'f'),
            ('e', 'f'),
            ('f', 'g')]),
 '06-흐름': ([('a', '현재 상태 읽기', 'data', -1, 0),
            ('b', '파이썬 조건 판정', 'code', -1, 1),
            ('c', 'Command 반환|update와 goto', 'code', -1, 2),
            ('d', 'update|상태에 반영', 'code', 0, 3),
            ('e', 'goto|다음 노드', 'code', 1, 3),
            ('f', '상태·실행 경로 확인', 'metric', -1, 4)],
           [('a', 'b'), ('b', 'c'), ('c', 'd'), ('c', 'e'), ('d', 'f'), ('e', 'f')]),
 '07-흐름': ([('a', '제공 문서·질문', 'data', -1, 0),
            ('b', '임베딩 · BM25|각각 검색', 'code', -1, 1),
            ('c', 'RRF|후보 순위 병합', 'code', -1, 2),
            ('d', 'CrossEncoder|후보 재정렬', 'model', -1, 3),
            ('e', '본문·출처 선택', 'code', -1, 4),
            ('f', '선택한 근거로 생성', 'model', -1, 5),
            ('g', '답변·출처·경로 기록', 'metric', -1, 6)],
           [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f'), ('f', 'g')])}

if __name__ == "__main__":
    main()
