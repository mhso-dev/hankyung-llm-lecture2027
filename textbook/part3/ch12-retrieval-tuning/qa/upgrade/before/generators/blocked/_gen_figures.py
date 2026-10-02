"""Ch12 도식 정본: 같은 노드·화살표로 SVG와 Excalidraw를 생성합니다."""
from __future__ import annotations

# 품질 개선(2026-09-18, Ch 12 01절, QUALITY-UPGRADE.md §8·PLAYBOOK §2-1): 이 옛 도식 생성기는 실행하지 않습니다.
# 개선한 절의 도식은 figures/NN-k-이름.mmd 를 textbook/_notebook/mermaid/render_mermaid.py 로 렌더해 만듭니다.
# 이 파일을 실행하면 아직 개선하지 않은 02~12절이 쓰는 옛 SVG와 Excalidraw까지 다시 써서 개선본과 섞입니다.
# 챕터를 마감할 때 qa/upgrade/before/generators/ 로 옮깁니다(삭제하지 않습니다).
raise SystemExit("Ch 12 품질 개선 뒤에는 이 도식 생성기를 실행하지 않습니다. render_mermaid.py 를 쓰세요.")

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLORS = {'data': '#DDEDE8', 'code': '#DDEAF4', 'model': '#E9E0F3',
          'metric': '#F7EDC7', 'failure': '#F4D9D5'}
# 세로 배치는 PC와 모바일에서 같은 순서로 읽습니다. 색은 처리 의미에 대응합니다.
FIGURES = {
    '01-정확-검색': [('문서 12개·질문 벡터', 'data'), ('모든 벡터 거리 계산', 'code'),
                   ('가까운 거리부터 정렬', 'code'), ('top-3·Recall@3 확인', 'metric')],
    '02-HNSW': [('같은 벡터·질문 저장', 'data'), ('정확 검색과|HNSW 검색 실행', 'code'),
               ('ef_search만 변경', 'code'), ('결과 순위·거리 비교', 'metric')],
    '03-필터-반복탐색': [('common 3,000개|rare 12개', 'data'),
                       ('같은 필터·LIMIT 5|반복 탐색 끔', 'code'),
                       ('이번 실행: 반환 0개', 'failure'),
                       ('strict_order로|반복 탐색 켬', 'code'),
                       ('이번 실행: 반환 5개', 'metric')],
    '04-Kiwi-BM25': [('원문과 질문', 'data'), ('같은 Kiwi 토큰 정책', 'code'),
                    ('형태소 배열', 'data'), ('BM25 문서 점수·순위', 'metric')],
    '05-dense-sparse': [('같은 문서·질문·k=3', 'data'),
                       ('두 방법으로 각각 검색|dense / Kiwi·BM25', 'code'),
                       ('문서 ID와 순위 비교', 'metric'), ('같은 8개 질문 평가', 'metric')],
    '06-RRF': [('dense 상위 6개|sparse 상위 6개', 'data'),
               ('순위별 가중 점수|weight / (60 + rank)', 'code'),
               ('문서 ID별 점수 합산', 'code'), ('결합 top-3', 'data'),
               ('같은 평가셋으로 확인', 'metric')],
    '07-리랭킹-흐름': [('질문과 1차 후보 8개', 'data'),
                      ('CrossEncoder|질문·본문 점수', 'model'),
                      ('점수 내림차순 정렬', 'code'), ('상위 5개 후보', 'data')],
    '08-후보-모델-격자': [('개발 질문 15개', 'data'), ('후보 5·10·20개', 'code'),
                        ('같은 후보에|두 모델 점수 계산', 'model'),
                        ('Recall·nDCG·시간', 'metric')],
    '09-부모-자식-검색': [('질문과 자식 청크', 'data'), ('자식 청크 검색', 'code'),
                        ('parent_id로 부모 조회', 'code'), ('중복 없는 부모 원문', 'data')],
    '10-mmr-선택': [('질문·후보 벡터', 'data'), ('질문과 관련성 계산', 'code'),
                   ('선택한 청크와의|중복을 함께 계산', 'code'),
                   ('λ별 관련성·다양성', 'metric')],
    '11-질문-재작성': [('대화 맥락과 후속 질문', 'data'), ('독립 질문으로 재작성', 'model'),
                      ('원문·재작성으로 검색|RRF로 후보 병합', 'code'),
                      ('근거 문서와 순위 비교', 'metric')],
    '12-통합-RAG': [('제공 PDF와 질문', 'data'),
                   ('dense·Kiwi BM25|각각 검색', 'code'),
                   ('RRF로 후보 병합', 'code'),
                   ('CrossEncoder 재정렬', 'model'),
                   ('쪽 본문·출처 선택', 'code'),
                   ('선택 자료로 답변 생성', 'model'),
                   ('답변·출처·실행 기록', 'metric')],
    '12-실험-로그': [('가설과 개발용 질문', 'data'), ('개발 설정 36개 평가', 'metric'),
                    ('개발 지표로 설정 선택', 'code'), ('고정 설정으로 시험 1회', 'metric'),
                    ('설정·지표·시간 로그', 'metric')],
}


def common(ident: str, kind: str, x: float, y: float, width: float, height: float) -> dict:
    return {'id': ident, 'type': kind, 'x': x, 'y': y, 'width': width, 'height': height,
            'angle': 0, 'strokeColor': '#334155', 'backgroundColor': 'transparent',
            'fillStyle': 'solid', 'strokeWidth': 2, 'strokeStyle': 'solid',
            'roughness': 0, 'opacity': 100, 'groupIds': [], 'frameId': None,
            'roundness': None, 'seed': 1, 'version': 1, 'versionNonce': 1,
            'isDeleted': False, 'boundElements': [], 'updated': 1, 'link': None,
            'locked': False}


def make(name: str, nodes: list[tuple[str, str]]) -> tuple[str, dict]:
    elements, shapes = [], []
    width, box_height, gap = 360, 72, 38
    canvas_height = 28 + len(nodes) * box_height + (len(nodes) - 1) * gap
    marker = name + '-arrow'
    for index, (label, role) in enumerate(nodes):
        x, y, w = 16, 14 + index * (box_height + gap), 328
        ident = f'{name}-node-{index}'
        box = common(ident, 'rectangle', x, y, w, box_height)
        box.update(backgroundColor=COLORS[role], roundness={'type': 3},
                   boundElements=[{'id': ident + '-label', 'type': 'text'}])
        elements.append(box)
        lines = label.split('|')
        text_height = 27 * len(lines)
        label_y = y + (box_height - text_height) / 2
        text = common(ident + '-label', 'text', x + 8, label_y, w - 16, text_height)
        text.update(strokeColor='#172033', text='\n'.join(lines), originalText='\n'.join(lines),
                    fontSize=22, fontFamily=1, textAlign='center', verticalAlign='middle',
                    containerId=ident, autoResize=True, lineHeight=1.2273)
        elements.append(text)
        shapes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{box_height}" '
                      f'rx="10" fill="{COLORS[role]}" stroke="#334155" stroke-width="2"/>')
        for line_index, line in enumerate(lines):
            baseline = label_y + 22 + line_index * 27
            shapes.append(f'<text x="180" y="{baseline}" text-anchor="middle" '
                          f'font-size="22" font-family="sans-serif" fill="#172033">'
                          f'{html.escape(line)}</text>')
        if index < len(nodes) - 1:
            start, length = y + box_height + 4, gap - 10
            arrow = common(f'{name}-edge-{index}', 'arrow', 180, start, 0, length)
            arrow.update(points=[[0, 0], [0, length]], startBinding=None, endBinding=None,
                         startArrowhead=None, endArrowhead='arrow', elbowed=False)
            elements.append(arrow)
            shapes.append(f'<path d="M180 {start} v{length}" fill="none" '
                          f'stroke="#334155" stroke-width="2" marker-end="url(#{marker})"/>')
    description = ' → '.join(label.replace('|', ' ') for label, _ in nodes)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {canvas_height}" '
           f'style="width:360px;max-width:100%;height:auto;display:block;margin:0 auto" '
           f'role="img" aria-label="{html.escape(description, quote=True)}">'
           f'<title>{html.escape(description)}</title><defs><marker id="{marker}" '
           'markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
           '<path d="M0,0 L8,4 L0,8 Z" fill="#334155"/></marker></defs>'
           + ''.join(shapes) + '</svg>')
    excalidraw = {'type': 'excalidraw', 'version': 2, 'source': 'https://excalidraw.com',
                  'elements': elements, 'appState': {'gridSize': None,
                  'viewBackgroundColor': '#FFFFFF'}, 'files': {}}
    return svg, excalidraw


def main() -> None:
    for name, nodes in FIGURES.items():
        svg, editable = make(name, nodes)
        (HERE / f'{name}.svg').write_text(svg)
        (HERE / f'{name}.excalidraw').write_text(json.dumps(editable, ensure_ascii=False, indent=2)+'\n')
        caption = ('위에서 아래로 읽습니다. 초록은 입력·문서, 파랑은 작성한 처리, '
                   '보라는 모델 계산, 노랑은 측정·기록을 나타냅니다.\n\n'
                   + ' → '.join(label.replace('|', ' ') for label, _ in nodes) + '\n')
        (HERE / f'{name}.caption.md').write_text(caption)
    print(f'Generated {len(FIGURES)} matching SVG/Excalidraw diagrams')


if __name__ == '__main__':
    main()
