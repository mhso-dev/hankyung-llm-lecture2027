"""절별 도식 정본: 같은 요소에서 SVG와 Excalidraw를 생성합니다."""

from __future__ import annotations

# [품질 개선 2026-09-21] 이 생성기는 개선 전(2026-09-10) 판을 만든 도구입니다.
# 절 개선본은 `textbook/part4/ch15-evaluation-advanced/qa/upgrade/author_NN.py`가 만듭니다.
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


CAPTIONS={'01-평가-흐름': 'Ch 12의 36행은 검색 설정별 평가 기록입니다. 각 행 안의 질문별 정답과 후보를 읽어 누락 사례를 분류하고, 답변 평가가 필요한 사례에는 '
             '전달 문서와 생성 답변을 따로 준비합니다.',
 '02-평가-흐름': '네 상자는 각 평가에서 무엇을 비교하는지 보여 줍니다. Correctness는 답변과 정답 답변, Relevance는 답변과 질문, '
             'Groundedness는 답변과 전달 문서, Retrieval relevance는 검색 문서와 질문을 비교합니다.',
 '03-평가-흐름': '같은 두 답변을 A·B와 B·A 순서로 각각 제시합니다. 모델이 고른 위치를 원래 후보 ID로 바꾸어 비교해야, 위치가 달라졌다는 사실과 선호 '
             '후보가 바뀌었다는 사실을 구분할 수 있습니다.',
 '04-평가-흐름': '교재에서 제시한 라벨과 judge의 값을 같은 사례 ID로 짝지어 일치율을 계산합니다. 이 라벨을 사람이 실제로 수집한 평가 자료와 구분하고, '
             '불일치 사례의 원문과 판정 이유를 확인합니다.',
 '05-평가-흐름': '호출 시작부터 첫 텍스트가 도착할 때까지의 시간을 TTFT로, 응답 완료까지의 시간을 total로 측정합니다. 입력·출력 토큰과 캐시 사용량을 '
             '별도 항목으로 기록해 시간과 사용량을 섞지 않습니다.',
 '06-평가-흐름': '합성 대화 비용을 작은 순서로 정렬하고 표본 수와 백분위수 계산 규칙을 고정합니다. p50·p95·p99를 읽은 뒤 비용이 큰 사례를 '
             '확인합니다. 이 예제의 분포를 실제 서비스에서 측정한 비용 분포로 해석하지 않습니다.',
 '07-평가-흐름': '같은 사례의 이전 결과와 변경 후 결과를 비교합니다. 이전에는 성공했지만 변경 후 실패한 사례를 표시하고 원인을 수정한 뒤 다시 검사합니다. '
             '평균 점수만으로는 이런 사례를 찾지 못할 수 있습니다.',
 '08-평가-흐름': '사례마다 custom_id를 부여해 JSONL 요청을 작성하고 형식과 중복 ID를 검사합니다. 모의 결과를 ID로 다시 연결하는 연습은 실제 '
             'Batch를 제출해 완료한 기록과 구분합니다.'}

FIGURES={'01-평가-흐름': ([('a', 'Ch 12 검색 설정 36행', 'data', -1, 0),
               ('b', '질문별 정답·후보 확인', 'code', -1, 1),
               ('c', '누락 사례 분류', 'metric', -1, 2),
               ('d', '답변·전달 문서 준비', 'data', -1, 3),
               ('e', '실패에 맞는 평가 선택', 'code', -1, 4)],
              [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')]),
 '02-평가-흐름': ([('a', 'Correctness|답변 ↔ 정답 답변', 'metric', -1, 0),
               ('b', 'Relevance|답변 ↔ 질문', 'metric', -1, 1),
               ('c', 'Groundedness|답변 ↔ 전달 문서', 'metric', -1, 2),
               ('d', 'Retrieval relevance|검색 문서 ↔ 질문', 'metric', -1, 3)],
              []),
 '03-평가-흐름': ([('a', '같은 답변 후보 A·B', 'data', -1, 0),
               ('b', 'A → B 순서|judge 호출', 'model', 0, 1),
               ('c', 'B → A 순서|judge 호출', 'model', 1, 1),
               ('d', '선택 위치를|원래 후보 ID로 변환', 'code', -1, 2),
               ('e', '후보별 선택 일치 비교', 'metric', -1, 3)],
              [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'), ('d', 'e')]),
 '04-평가-흐름': ([('a', '교재 제시 라벨|사람 수집 라벨과 구분', 'data', -1, 0),
               ('b', '같은 사례의 judge 값', 'model', -1, 1),
               ('c', '사례 ID로 짝 맞추기', 'code', -1, 2),
               ('d', '일치 수 ÷ 비교 사례 수', 'metric', -1, 3),
               ('e', '불일치 사례의 원문 확인', 'metric', -1, 4)],
              [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')]),
 '05-평가-흐름': ([('a', '호출 시작 시각', 'metric', -1, 0),
               ('b', '첫 텍스트 도착|TTFT 측정', 'metric', -1, 1),
               ('c', '마지막 응답 완료|total 측정', 'metric', -1, 2),
               ('d', '입력 · 출력 · 캐시|서로 구분해 기록', 'metric', -1, 3)],
              [('a', 'b'), ('b', 'c'), ('c', 'd')]),
 '06-평가-흐름': ([('a', '대화별 비용 자료|합성 예제 범위 확인', 'data', -1, 0),
               ('b', '작은 비용부터 정렬', 'code', -1, 1),
               ('c', '표본 수·계산 규칙 고정', 'code', -1, 2),
               ('d', 'p50 · p95 · p99', 'metric', -1, 3),
               ('e', '비용이 큰 사례 확인', 'metric', -1, 4)],
              [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')]),
 '07-평가-흐름': ([('a', '고정 사례·평가 기준', 'data', -1, 0),
               ('b', '이전 결과', 'data', 0, 1),
               ('c', '변경 후 결과', 'data', 1, 1),
               ('d', '같은 사례 ID로 비교', 'code', -1, 2),
               ('e', '이전 성공·현재 실패|사례 표시', 'failure', -1, 3),
               ('f', '원인을 수정한 뒤 재검사', 'code', -1, 4)],
              [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'), ('d', 'e'), ('e', 'f')]),
 '08-평가-흐름': ([('a', '평가할 사례·프롬프트', 'data', -1, 0),
               ('b', 'custom_id 부여', 'code', -1, 1),
               ('c', 'JSONL 요청 작성', 'code', -1, 2),
               ('d', '형식·ID 중복 검사', 'metric', -1, 3),
               ('e', '모의 결과를 ID로 연결|실제 제출·완료와 구분', 'code', -1, 4)],
              [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')])}

if __name__ == "__main__":
    main()
