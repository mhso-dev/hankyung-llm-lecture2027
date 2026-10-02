from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FLOWS = {
    "01": ["소스 코드", "pytest·Ruff", "wheel 빌드", "CI 종료"],
    "02": ["평가 사례", "후보 함수 실행", "사실·궤적 채점", "PASS·FAIL"],
    "03": ["Docker build", "v1·v2 inspect", "image ID 기록", "배포 대상"],
    "04": ["구간별 메트릭", "연속 구간 계산", "최장 streak", "FIRING"],
    "05": ["v2 health 503", "rollback 사건", "v1 재시작", "health 200"],
}


def element(kind: str, element_id: str, x: int, y: int, width: int, height: int, **extra):
    base = {
        "id": element_id, "type": kind, "x": x, "y": y, "width": width, "height": height,
        "angle": 0, "strokeColor": "#334155", "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid", "roughness": 0,
        "opacity": 100, "groupIds": [], "frameId": None, "index": element_id,
        "roundness": {"type": 3}, "seed": len(element_id) * 137, "version": 1,
        "versionNonce": len(element_id) * 271, "isDeleted": False, "boundElements": [],
        "updated": 1, "link": None, "locked": False,
    }
    base.update(extra)
    return base


for number, labels in FLOWS.items():
    elements = []
    for index, label in enumerate(labels):
        x = 45 + index * 230
        elements.append(element("rectangle", f"{number}-box-{index}", x, 100, 175, 90,
                                backgroundColor="#dbeafe" if index < 2 else "#dcfce7"))
        elements.append(element("text", f"{number}-text-{index}", x + 12, 130, 151, 30,
                                text=label, fontSize=20, fontFamily=1, textAlign="center",
                                verticalAlign="middle", containerId=f"{number}-box-{index}",
                                originalText=label, autoResize=True, lineHeight=1.25,
                                baseline=20, roundness=None))
        if index < 3:
            elements.append(element("arrow", f"{number}-arrow-{index}", x + 175, 145, 55, 0,
                                    points=[[0, 0], [55, 0]], lastCommittedPoint=None,
                                    startBinding=None, endBinding=None, startArrowhead=None,
                                    endArrowhead="arrow", elbowed=False, roundness={"type": 2}))
    drawing = {
        "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
        "elements": elements, "appState": {"viewBackgroundColor": "#f8fafc"}, "files": {},
    }
    (HERE / f"{number}-흐름.excalidraw").write_text(
        json.dumps(drawing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    boxes = []
    for index, label in enumerate(labels):
        x = 45 + index * 230
        color = "#dbeafe" if index < 2 else "#dcfce7"
        boxes.append(f'<rect x="{x}" y="100" width="175" height="90" rx="14" fill="{color}" stroke="#334155" stroke-width="2"/>')
        boxes.append(f'<text x="{x + 87}" y="153" text-anchor="middle" font-family="sans-serif" font-size="19" fill="#0f172a">{label}</text>')
        if index < 3:
            boxes.append(f'<path d="M{x + 175} 145H{x + 220}" stroke="#334155" stroke-width="3" marker-end="url(#a)"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="290" viewBox="0 0 960 290" role="img"><defs><marker id="a" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#334155"/></marker></defs><rect width="960" height="290" rx="20" fill="#f8fafc"/>{''.join(boxes)}</svg>'''
    (HERE / f"{number}-흐름.svg").write_text(svg, encoding="utf-8")

print(f"generated {len(FLOWS)} editable diagrams")
