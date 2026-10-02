"""Render Part 5 graph specifications to matching SVG and editable Excalidraw."""
from __future__ import annotations
import html
import json
from pathlib import Path

COLORS = {"data": "#DDEDE8", "tool": "#DDEDE8", "code": "#DDEAF4", "model": "#E9E0F3", "metric": "#F7EDC7", "failure": "#F4D9D5"}

def element(ident, kind, x, y, width, height):
    return dict(id=ident, type=kind, x=x, y=y, width=width, height=height,
                angle=0, strokeColor="#334155", backgroundColor="transparent", fillStyle="solid",
                strokeWidth=2, strokeStyle="solid", roughness=0, opacity=100, groupIds=[],
                frameId=None, roundness=None, seed=1, version=1, versionNonce=1, isDeleted=False,
                boundElements=[], updated=1, link=None, locked=False)

def render(directory: Path, name: str, spec: dict) -> None:
    width, height = spec.get("size", (380, 650))
    elements, shapes = [], []
    def label(ident, value, x, y, span):
        for i, line in enumerate(value.split("\n")):
            text = element(f"{ident}-{i}", "text", x, y+i*25, span, 25)
            text.update(text=line, originalText=line, fontSize=18, fontFamily=2,
                        textAlign="center", verticalAlign="middle", containerId=None,
                        autoResize=False, lineHeight=1.3889)
            elements.append(text)
            shapes.append(f'<text x="{x+span/2}" y="{y+19+i*25}" text-anchor="middle" font-size="18" font-family="sans-serif" fill="#172033">{html.escape(line)}</text>')
    for i, edge in enumerate(spec["edges"]):
        points = edge[0]
        x, y = points[0]
        arrow = element(f"{name}-arrow-{i}", "arrow", x, y,
                        max(p[0] for p in points)-min(p[0] for p in points),
                        max(p[1] for p in points)-min(p[1] for p in points))
        arrow.update(points=[[px-x, py-y] for px, py in points], startBinding=None,
                     endBinding=None, lastCommittedPoint=None, startArrowhead=None,
                     endArrowhead="arrow", elbowed=False)
        elements.append(arrow)
        path = "M" + " L".join(f"{px},{py}" for px, py in points)
        shapes.append(f'<path d="{path}" fill="none" stroke="#334155" stroke-width="2" marker-end="url(#{name}-arrow)"/>')
        if len(edge)>1:
            value, tx, ty, span = edge[1]
            label(f"{name}-edge-label-{i}", value, tx, ty, span)
    for i, (value, role, x, y, w, h) in enumerate(spec["nodes"]):
        box = element(f"{name}-box-{i}", "rectangle", x, y, w, h)
        box.update(backgroundColor=COLORS[role], roundness={"type": 3})
        elements.append(box)
        shapes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{COLORS[role]}" stroke="#334155" stroke-width="2"/>')
        label(f"{name}-label-{i}", value, x+8, y+(h-25*len(value.split(chr(10))))/2, w-16)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="width:{width}px;max-width:none;height:auto;display:block;margin:0 auto" role="img" aria-label="{html.escape(spec["caption"], quote=True)}"><title>{html.escape(spec["caption"])}</title><defs><marker id="{name}-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#334155"/></marker></defs>{"".join(shapes)}</svg>'
    drawing = dict(type="excalidraw", version=2, source="https://excalidraw.com", elements=elements,
                   appState={"gridSize": None, "viewBackgroundColor": "#ffffff"}, files={})
    (directory/f"{name}.svg").write_text(svg)
    (directory/f"{name}.excalidraw").write_text(json.dumps(drawing, ensure_ascii=False, indent=2)+"\n")
    (directory/f"{name}.caption.md").write_text(spec["caption"]+"\n")

def linear(labels, caption):
    return {"size": (380, 30+100*len(labels)), "caption": caption,
            "nodes": [(label, role, 30, 20+100*i, 320, 65) for i,(label,role) in enumerate(labels)],
            "edges": [([(190,85+100*i),(190,116+100*i)],) for i in range(len(labels)-1)]}
