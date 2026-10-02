"""절별 도식 정본: 같은 요소에서 SVG와 Excalidraw를 생성합니다."""

from __future__ import annotations
# [품질 개선 2026-09-19] 이 생성기는 개선 전(2026-09-10) 판을 만든 도구입니다.
# 절 개선본은 `textbook/part4/ch14-rag-patterns/qa/upgrade/author_NN.py`가 만듭니다.
# 이 파일을 실행하면 개선한 절이 되돌아가므로 실행을 막아 둡니다(PLAYBOOK §2-1, 규격 §8).
# 읽기 자료로는 그대로 씁니다. 챕터 마감 때 `qa/upgrade/before/generators/`로 옮깁니다.
raise SystemExit("개선 전 생성기입니다. qa/upgrade/author_NN.py를 쓰세요.")
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


CAPTIONS={'01-대화-히스토리와-질문-재작성-flow': '후속 질문에 빠진 대상을 대화 기록에서 보충해 독립적인 검색 질문을 만듭니다. 이 질문으로 검색한 원문과 문서 '
                            'ID를 확인한 뒤 근거를 넣어 답변을 생성합니다.',
 '02-Multi-Query-flow': '하나의 질문에서 여러 검색 질문을 만든 뒤 각각 문서를 검색합니다. 나란한 상자는 서로 다른 질문의 검색이며, 문서 ID로 '
                        '후보를 합친 뒤 정답 문서의 포함 여부와 순위를 확인합니다.',
 '03-질의-분해-flow': '여러 조건을 묻는 질문을 하위 질문으로 나누어 조건별 근거를 검색합니다. 원문을 합친 뒤에는 하위 질문 하나만 답하지 않고 원 질문의 '
                  '조건을 모두 다뤘는지 확인합니다.',
 '04-Step-back-flow': '구체적인 원 질문을 유지하면서 상위 개념을 묻는 질문을 추가합니다. 두 질문의 검색 결과를 합칠 때 원 질문의 고유명사나 '
                      '조건이 사라지지 않았는지 확인합니다.',
 '05-HyDE-flow': '모델이 만든 가상 문서를 임베딩해 실제 문서 벡터를 검색합니다. 가상 문서의 내용이 사실인지 확인한 것은 아니므로 답변의 근거와 출처는 '
                 '검색한 실제 원문에서 가져옵니다.',
 '06-CRAG-flow': '첫 검색의 점수를 코드에 적은 임계값과 비교합니다. 기준을 충족하면 결과를 유지하고, 미달하면 한 번 재검색한 뒤 선택한 문서로 답변을 '
                 '생성합니다. 마지막 기록에서 추가 호출 여부를 확인합니다.',
 '07-Self-RAG-flow': '생성한 답변과 전달 문서를 비교해 근거 일치 점수를 얻습니다. 코드가 점수를 임계값과 비교해 답변을 유지하거나 수정 경로를 '
                     '실행합니다. 통제 실험에서는 근거 밖 문장을 직접 넣었다는 조건을 함께 읽습니다.',
 '08-RAPTOR-계층-요약-flow': '범주별 원문을 요약하고 요약과 원문을 임베딩합니다. 질문과 가까운 요약 범주를 선택한 뒤 그 범주의 원문을 검색하며, '
                         'child ID로 어떤 문서에서 만든 요약인지 확인합니다.',
 '09-패턴-비교와-선택-flow': '같은 문서·질문·정답을 유지하면서 기준선과 검색 패턴을 각각 실행합니다. 후보와 답변뿐 아니라 검색 지표·시간·사용량·비용을 '
                      '함께 저장해 품질과 추가 호출 부담을 비교합니다.'}

FIGURES={'01-대화-히스토리와-질문-재작성-flow': ([('a', '대화 기록·후속 질문', 'data', -1, 0),
                              ('b', '독립 질문으로 재작성', 'model', -1, 1),
                              ('c', '재작성 질문으로 검색', 'code', -1, 2),
                              ('d', '실제 원문·문서 ID', 'data', -1, 3),
                              ('e', '근거를 넣어 답변 생성', 'model', -1, 4)],
                             [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')]),
 '02-Multi-Query-flow': ([('a', '원 질문', 'data', -1, 0),
                          ('b', '여러 검색 질문 생성', 'model', -1, 1),
                          ('c', '변형 질문 1|검색', 'code', 0, 2),
                          ('d', '변형 질문 2|검색', 'code', 1, 2),
                          ('e', '문서 ID별 후보 병합', 'code', -1, 3),
                          ('f', '정답 포함·순위 확인', 'metric', -1, 4)],
                         [('a', 'b'),
                          ('b', 'c'),
                          ('b', 'd'),
                          ('c', 'e'),
                          ('d', 'e'),
                          ('e', 'f')]),
 '03-질의-분해-flow': ([('a', '두 조건을 묻는 질문', 'data', -1, 0),
                    ('b', '하위 질문으로 분해', 'model', -1, 1),
                    ('c', '조건 1|근거 검색', 'code', 0, 2),
                    ('d', '조건 2|근거 검색', 'code', 1, 2),
                    ('e', '두 조건의 원문 병합', 'code', -1, 3),
                    ('f', '원 질문에 맞춰 생성', 'model', -1, 4)],
                   [('a', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'e'), ('d', 'e'), ('e', 'f')]),
 '04-Step-back-flow': ([('a', '구체적인 원 질문', 'data', -1, 0),
                        ('b', '상위 개념 질문 생성', 'model', -1, 1),
                        ('c', '원 질문|검색', 'code', 0, 2),
                        ('d', '상위 질문|검색', 'code', 1, 2),
                        ('e', '두 검색 결과 병합', 'code', -1, 3),
                        ('f', '원 질문의 조건 확인', 'metric', -1, 4)],
                       [('a', 'b'),
                        ('a', 'c'),
                        ('b', 'd'),
                        ('c', 'e'),
                        ('d', 'e'),
                        ('e', 'f')]),
 '05-HyDE-flow': ([('a', '원 질문', 'data', -1, 0),
                   ('b', '가상 문서 생성', 'model', -1, 1),
                   ('c', '가상 문서를 임베딩', 'model', -1, 2),
                   ('d', '실제 문서 벡터 검색', 'code', -1, 3),
                   ('e', '검색한 원문·문서 ID', 'data', -1, 4),
                   ('f', '답변 근거는 원문 사용', 'metric', -1, 5)],
                  [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f')]),
 '06-CRAG-flow': ([('a', '1차 검색 결과·점수', 'data', -1, 0),
                   ('b', '점수와 임계값 비교', 'code', -1, 1),
                   ('c', '기준 이상|검색 결과 유지', 'code', 0, 2),
                   ('d', '기준 미만|재검색 1회', 'code', 1, 2),
                   ('e', '선택 문서로 답변 생성', 'model', -1, 3),
                   ('f', '경로·추가 호출 확인', 'metric', -1, 4)],
                  [('a', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'e'), ('d', 'e'), ('e', 'f')]),
 '07-Self-RAG-flow': ([('a', '근거 문서·생성 답변', 'data', -1, 0),
                       ('b', '근거 일치 점수 생성', 'model', -1, 1),
                       ('c', '임계값과 비교', 'code', -1, 2),
                       ('d', '통과|답변 유지', 'code', 0, 3),
                       ('e', '미달|수정 경로', 'code', 1, 3),
                       ('f', '답변과 근거 다시 확인', 'metric', -1, 4)],
                      [('a', 'b'),
                       ('b', 'c'),
                       ('c', 'd'),
                       ('c', 'e'),
                       ('d', 'f'),
                       ('e', 'f')]),
 '08-RAPTOR-계층-요약-flow': ([('a', '원문 그룹 1|문서 ID 목록', 'data', 0, 0),
                           ('b', '원문 그룹 2|문서 ID 목록', 'data', 1, 0),
                           ('c', '그룹별 요약 생성', 'model', -1, 1),
                           ('d', '요약·원문 임베딩', 'model', -1, 2),
                           ('e', '여러 계층에서 검색', 'code', -1, 3),
                           ('f', 'child ID로 원문 연결', 'code', -1, 4),
                           ('g', '요약과 원문 내용 비교', 'metric', -1, 5)],
                          [('a', 'c'),
                           ('b', 'c'),
                           ('c', 'd'),
                           ('d', 'e'),
                           ('e', 'f'),
                           ('f', 'g')]),
 '09-패턴-비교와-선택-flow': ([('a', '같은 문서·질문·정답', 'data', -1, 0),
                        ('b', '기준선과 패턴별 실행', 'code', -1, 1),
                        ('c', '후보 ID·순위·답변', 'data', -1, 2),
                        ('d', '검색 지표·시간·사용량·비용', 'metric', -1, 3),
                        ('e', '조건·결과를 함께 저장', 'metric', -1, 4)],
                       [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')])}

if __name__ == "__main__":
    main()
