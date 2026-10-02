raise SystemExit("옛 도식 생성기 — 품질 개선 뒤 실행 금지. 지금 판 그림은 figures/*.mmd를 textbook/_notebook/mermaid/render_mermaid.py로 렌더하고, 절 생성기는 qa/upgrade/author_*.py")

import json
from pathlib import Path


OUT = Path(__file__).parent
FIGURES = {
    "01-평가셋-구조": ("질문 30개", "정답 문서 ID", "개발·시험 분리"),
    "02-recall-후보": ("전체 말뭉치", "후보 50개", "정답 포함 여부"),
    "03-precision-상위": ("후보 목록", "상위 5개", "정답 비율"),
    "04-ndcg-순위": ("관련도", "순위 할인", "0~1 정규화"),
    "05-오류-분기": ("후보 누락", "순위 누락", "조건별 기록"),
    "06-실험-루프": ("설정 고정", "지표 계산", "로그 한 행"),
}


for stem, labels in FIGURES.items():
    boxes = []
    elements = []
    for index, label in enumerate(labels):
        x = 30 + index * 210
        color = ("#eef2ff", "#ecfdf5", "#fff7ed")[index]
        stroke = ("#4f46e5", "#047857", "#c2410c")[index]
        boxes.append(f'<rect x="{x}" y="55" width="170" height="80" rx="12" fill="{color}" stroke="{stroke}" stroke-width="2"/><text x="{x+85}" y="102" text-anchor="middle" font-size="18" fill="#1f2937">{label}</text>')
        elements.append({"id": f"box{index}", "type": "rectangle", "x": x, "y": 55, "width": 170, "height": 80, "strokeColor": stroke, "backgroundColor": color, "label": label})
        if index < 2:
            boxes.append(f'<path d="M {x+170} 95 L {x+205} 95" stroke="#6b7280" stroke-width="3" marker-end="url(#arrow)"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 190" role="img" aria-labelledby="title desc">
<title id="title">{labels[0]}에서 {labels[2]}까지의 흐름</title><desc id="desc">세 단계가 왼쪽에서 오른쪽으로 이어집니다.</desc>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#6b7280"/></marker></defs>
<rect width="650" height="190" fill="#ffffff"/>{''.join(boxes)}
<text x="325" y="170" text-anchor="middle" font-size="14" fill="#4b5563">한 단계의 출력이 다음 단계의 입력이 됩니다.</text></svg>'''
    (OUT / f"{stem}.svg").write_text(svg, encoding="utf-8")
    source = {"type": "excalidraw", "version": 2, "source": "ch11-evaluation", "elements": elements, "appState": {"viewBackgroundColor": "#ffffff"}, "files": {}}
    (OUT / f"{stem}.excalidraw").write_text(json.dumps(source, ensure_ascii=False, indent=2), encoding="utf-8")
