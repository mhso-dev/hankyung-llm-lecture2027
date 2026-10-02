"""Compare real diagram labels and connectors across SVG and Excalidraw.

전체 마감 2026-10-01: 옛 20행(모든 챕터에 figures/_gen_figures.py 요구)을 지금 구조에 맞게 고침 — 개선한 챕터는
원고가 부르는 Mermaid 원본(.mmd)과 렌더(.svg·.png·.render.json), 삽화(.png·.prompt.md)가 있고 옛 생성기가 막혀
qa/upgrade/before/generators/blocked/에 있어야 하며, Mermaid 그림도 .excalidraw 짝처럼 원본과 견준다(라벨·화살촉·상자 수·렌더 도장).
이번 개선에서 제외한 Ch 32·33은 옛 구조(figures/_gen_figures.py + .excalidraw 짝) 그대로 본다.
"""
from __future__ import annotations

import ast
import hashlib
import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

PART = Path(__file__).resolve().parents[1]
MERMAID = PART.parent / '_notebook/mermaid'
EXCLUDED = {'ch32-docker', 'ch33-cicd'}  # 이번 품질 개선에서 제외한 챕터(옛 생성기·옛 그림 구조)
SKIP = re.compile(r'^(?:classDef|class|style|linkStyle|subgraph|direction|click)\b|^end$')
LINK = re.compile(r'\s*(<?(?:-{2,}|-\.+-|={2,})[>xo]?)\s*')


def normalize(value: str) -> str:
    return re.sub(r'\s+', '', value)


def squeezed(text):
    return re.sub(r'\s+', '', text)


def mermaid_lines(text):
    body = re.sub(r'(?s)^---\n.*?\n---\n', '', text)
    return [line.strip() for line in body.splitlines() if line.strip() and not line.strip().startswith('%%')]


def entity(text):
    # Mermaid 글자 코드(#lt;·#35;)와 HTML 이름을 글자로 바꾼다
    text = re.sub(r'#(\d+);', lambda match: chr(int(match.group(1))), text)
    text = re.sub(r'#([A-Za-z]+);', lambda match: html.unescape('&' + match.group(1) + ';'), text)
    return html.unescape(text)


def mermaid_labels(text):
    lines = mermaid_lines(text)
    kind, labels = lines[0].split()[0], []
    for line in lines[1:]:
        if kind == 'flowchart' and (line.startswith('subgraph') or not SKIP.match(line)):
            labels += re.findall(r'"([^"]*)"', line) + re.findall(r'\|([^|"]+)\|', line)
            plain = re.sub(r'"[^"]*"', '', line)
            labels += re.findall(r'<?--\s+([^\s>-][^>]*?)\s+--[->]', plain)
            labels += re.findall(r'-\.\s+([^.]+?)\s+\.->', plain) + re.findall(r'==\s+([^=]+?)\s+==>', plain)
            labels += re.findall(r'[\[\(\{]+([^\[\]\(\)\{\}"|]+)[\]\)\}]+', plain)
            bare = re.match(r'subgraph\s+([^\s\["]+)\s*$', line)
            labels += [bare.group(1)] if bare else []
        elif kind == 'sequenceDiagram':
            member = re.match(r'(?:participant|actor)\s+(\S+)(?:\s+as\s+(.+))?$', line)
            note = re.match(r'[Nn]ote\s+(?:over|left of|right of)\s+[^:]+:\s*(.+)$', line)
            block = re.match(r'(?:alt|else|opt|loop|par|and|critical|break)\b\s*(.*)$', line)
            message = re.match(r'[^:]+?(?:->>|-->>|->|-->|-x|--x|-\)|--\))[+-]?[^:]+:\s*(.*)$', line)
            if member:
                labels.append(member.group(2) or member.group(1))
            elif note or block:
                labels.append((note or block).group(1))
            elif message and not line.startswith('rect'):
                labels.append(message.group(1))
        elif kind == 'xychart-beta':
            labels += re.findall(r'"([^"]*)"', line)
        elif kind == 'gantt' and not re.match(r'(?:dateFormat|axisFormat|tickInterval|todayMarker|excludes)\b', line):
            heading = re.match(r'(?:title|section)\s+(.+)$', line) or re.match(r'([^:]+):', line)
            labels += [heading.group(1)] if heading else []
    return [entity(label) for label in labels if label.strip()]


def mermaid_arrows(text):
    lines = mermaid_lines(text)
    kind, count = lines[0].split()[0], 0
    for line in lines[1:]:
        if kind == 'sequenceDiagram':
            count += bool(':' in line and re.match(r'[^:]+?(?:->>|-->>|-x|--x|-\)|--\))', line))
        if kind != 'flowchart' or SKIP.match(line):
            continue
        plain = re.sub(r'\|[^|]*\|', '', re.sub(r'"[^"]*"', '""', line))
        plain = re.sub(r'<--\s[^<>]*?-->', ' <--> ', plain)
        plain = re.sub(r'(?<![<-])--\s[^<>-]*?-->', ' --> ', plain)
        plain = re.sub(r'(?<![<-])--\s[^<>-]*?---', ' --- ', plain)
        plain = re.sub(r'-\.\s[^.]*?\.->', ' -.-> ', plain)
        parts = LINK.split(re.sub(r'==\s[^=]*?==>', ' ==> ', plain).replace('~~~', ' '))
        for index in range(1, len(parts), 2):
            right = parts[index + 1] if index + 1 < len(parts) else ''
            pairs = (parts[index - 1].count('&') + 1) * (right.count('&') + 1)
            count += pairs * ((parts[index][-1] in '>xo') + (parts[index][0] == '<'))
    return count


def render_digest(source):
    # textbook/_notebook/mermaid/render_mermaid.py가 .render.json에 적는 값과 같은 셈
    classes = (MERMAID / 'classes.mmd').read_text(encoding='utf-8')
    prepared = re.sub(r'(?m)^\s*%% classes\s*$', classes.rstrip('\n'), source.read_text(encoding='utf-8'))
    config = (MERMAID / 'config.json').read_text(encoding='utf-8')
    return hashlib.sha256((prepared + config).encode('utf-8')).hexdigest()


def label_visible(label, texts):
    whole = squeezed(re.sub(r'<br\s*/?>', '', label))
    if any(whole in text for text in texts):
        return True
    parts = [squeezed(part) for part in re.split(r'<br\s*/?>|\\n', label) if squeezed(part)]
    return bool(parts) and all(any(part in text for text in texts) for part in parts)


def is_blocked(script: Path) -> bool:
    # 맨 위 문장들 가운데 최상위 raise SystemExit(...)가 있으면 실행이 막힌 옛 생성기다
    for node in ast.parse(script.read_text()).body[:12]:
        if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) and getattr(node.exc.func, 'id', '') == 'SystemExit':
            return True
    return False


def check_current_sources(chapter: Path) -> None:
    figures = chapter / 'figures'
    assert not (figures / '_gen_figures.py').exists(), chapter
    blocked = chapter / 'qa/upgrade/before/generators/blocked/_gen_figures.py'
    assert blocked.is_file() and is_blocked(blocked), blocked
    raw = ''.join(path.read_text() for path in sorted((chapter / '_src').glob('[0-9][0-9]-*.html')))
    diagrams = re.findall(r'\{\{mermaid:([^|}]+)', raw)
    assert diagrams, chapter
    for name in diagrams:
        for suffix in ('.mmd', '.svg', '.png', '.render.json'):
            assert (figures / f'{name}{suffix}').is_file(), (chapter.name, name + suffix)
    for name in re.findall(r'\{\{img:([^|}]+)', raw):
        for suffix in ('.png', '.prompt.md'):
            assert (figures / f'{name}{suffix}').is_file(), (chapter.name, name + suffix)


def mermaid_report(source: Path) -> dict:
    svg_path = source.with_suffix('.svg')
    svg = ET.fromstring(svg_path.read_text())
    text = source.read_text(encoding='utf-8')
    kind = mermaid_lines(text)[0].split()[0]
    labels = mermaid_labels(text)
    texts = [squeezed(''.join(item.itertext())) for item in svg.iter() if item.tag.split('}')[-1] == 'text']
    missing = [label for label in labels if not label_visible(label, texts)]
    assert not missing, (source, missing)
    assert labels, source
    arrows = mermaid_arrows(text)
    svg_arrows = sum(('marker-end' in item.attrib) + ('marker-start' in item.attrib) for item in svg.iter())
    assert arrows == svg_arrows and (arrows or kind in ('xychart-beta', 'gantt')), (source, arrows, svg_arrows)
    boxes = None
    if kind == 'flowchart':
        boxes = sum(item.tag.split('}')[-1] == 'g' and 'node' in (item.get('class') or '').split() for item in svg.iter())
        assert 1 <= boxes <= 7, (source, boxes)
    stamp = json.loads(source.with_suffix('.render.json').read_text())
    assert stamp.get('sha256') == render_digest(source), f'Stale Mermaid render: {source}'
    assert source.with_suffix('.png').is_file(), source
    return {'file': str(svg_path.relative_to(PART)), 'editable_source': 'mmd', 'kind': kind,
            'labels': len(labels), 'arrows': arrows, 'boxes': boxes, 'render_current': True, 'matched': True}


def main():
    reports = []
    for chapter in sorted(PART.glob('ch*')):
        figures = chapter / 'figures'
        if chapter.name in EXCLUDED:
            assert (figures / '_gen_figures.py').is_file(), chapter
        else:
            check_current_sources(chapter)
            reports.extend(mermaid_report(source) for source in sorted(figures.glob('*.mmd')))
        for drawing in sorted(figures.glob('*.excalidraw')):
            doc = json.loads(drawing.read_text())
            svg = ET.fromstring(drawing.with_suffix('.svg').read_text())
            elements = [item for item in doc['elements'] if not item.get('isDeleted')]
            raw_labels = [item['text'] for item in elements if item['type']=='text']
            labels = [normalize(label) for label in raw_labels]
            svg_labels = [normalize(''.join(item.itertext())) for item in svg.iter()
                          if item.tag.split('}')[-1]=='text']
            missing = [label for label in raw_labels
                       if normalize(label) not in svg_labels
                       and not all(normalize(line) in svg_labels for line in label.splitlines())]
            assert not missing, (drawing, missing, svg_labels)
            assert labels, drawing
            arrows = sum(item['type']=='arrow' for item in elements)
            svg_arrows = sum('marker-end' in item.attrib for item in svg.iter())
            assert arrows and arrows == svg_arrows, (drawing, arrows, svg_arrows)
            boxes = sum(item['type'] in ('rectangle','ellipse','diamond') for item in elements)
            assert 1 <= boxes <= 7, (drawing, boxes)
            reports.append({'file':str(drawing.relative_to(PART)), 'labels':len(labels),
                            'arrows':arrows, 'boxes':boxes, 'matched':True})
    (PART/'qa/figure-consistency.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
    mermaid = sum(item.get('editable_source') == 'mmd' for item in reports)
    print(f'PASS {len(reports)} SVG/source pairs ({mermaid} Mermaid .mmd, {len(reports) - mermaid} Excalidraw): '
          'labels, arrows, editable nodes')


if __name__=='__main__':
    main()
