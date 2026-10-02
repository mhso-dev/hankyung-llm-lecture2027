"""Ch31 도식을 SVG와 Excalidraw JSON으로 생성합니다."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPECS = {
    "01-흐름": (["비동기 요청 3건", "작업별 AsyncSession", "연결 풀", "PostgreSQL 응답"], "비동기 세션과 연결 풀"),
    "02-흐름": (["출금", "트랜잭션 경계", "입금 전 오류", "전체 롤백"], "두 변경의 원자성"),
    "03-흐름": (["리비전 파일", "upgrade head", "버전 표와 tickets", "downgrade base"], "Alembic 적용과 롤백"),
    "04-흐름": (["동시 요청", "크기 1인 풀", "대기 제한", "반환 또는 TimeoutError"], "커넥션 풀 대기"),
    "05-흐름": (["documents + HNSW", "체크포인터 표", "ch31_shared", "pg_dump 백업"], "한 스키마의 검색과 실행 상태"),
}
COLORS = ["#DDEAF4", "#F4D9D5", "#DDEDE8", "#E8E2F4"]


def render(name: str, labels: list[str], title: str) -> None:
    width, height = 380, 430
    rects, texts, arrows, elements = [], [], [], []
    for i, label in enumerate(labels):
        x, y = 30, 20 + i * 100
        rects.append(f'<rect x="{x}" y="{y}" width="320" height="65" rx="10" fill="{COLORS[i]}" stroke="#334155" stroke-width="2"/>')
        texts.append(f'<text x="190" y="{y+39}" text-anchor="middle" font-size="18" font-family="sans-serif" fill="#172033">{label}</text>')
        elements.append({"type":"rectangle","id":f"r{i}","x":x,"y":y,"width":320,"height":65,"strokeColor":"#334155","backgroundColor":COLORS[i],"fillStyle":"solid","strokeWidth":2,"roughness":0,"opacity":100})
        elements.append({"type":"text","id":f"t{i}","x":45,"y":y+20,"width":290,"height":24,"text":label,"fontSize":18,"fontFamily":1,"textAlign":"center","verticalAlign":"middle","strokeColor":"#172033"})
        if i < len(labels)-1:
            arrows.append(f'<path d="M190 {y+65} L190 {y+96}" stroke="#334155" stroke-width="2" marker-end="url(#a)"/>')
            elements.append({"type":"arrow","id":f"a{i}","x":190,"y":y+65,"width":0,"height":31,"points":[[0,0],[0,31]],"strokeColor":"#334155","strokeWidth":2,"roughness":0,"endArrowhead":"arrow"})
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="width:340px;max-width:none;height:auto;display:block;margin:0 auto" role="img" aria-label="{title}"><title>{title}</title><defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#334155"/></marker></defs>{''.join(arrows+rects+texts)}</svg>'''
    (HERE / f"{name}.svg").write_text(svg, encoding="utf-8")
    data = {"type":"excalidraw","version":2,"source":"ch31-generator","elements":elements,"appState":{"viewBackgroundColor":"#ffffff"},"files":{}}
    (HERE / f"{name}.excalidraw").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (HERE / f"{name}.caption.md").write_text(title+"의 흐름을 왼쪽에서 오른쪽으로 읽습니다.\n",encoding="utf-8")


if __name__ == "__main__":
    for name, (labels, title) in SPECS.items():
        render(name, labels, title)
    print("generated", len(SPECS))
