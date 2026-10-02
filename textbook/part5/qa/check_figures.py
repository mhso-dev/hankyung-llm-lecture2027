"""Compare visible labels and arrows in SVG and editable Excalidraw sources.

전체 마감 2026-10-01: 그림 이름 규칙(figures/NN-k-이름.mmd → .svg·.png, 렌더 도장 .render.json)을 지금 구조에 맞게 고침.
Mermaid로 렌더한 SVG는 짝 원본 .mmd와 견주고(원본 라벨이 SVG에 보이는지 · 화살촉 수 · 렌더 도장이 지금 원본·설정과 같은지 · PNG),
.excalidraw 짝이 있는 옛 SVG는 전처럼 견준다. 편집 원본(.mmd·.excalidraw)이 없는 SVG는 전처럼 멈춘다.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

PART = Path(__file__).resolve().parents[1]
NS = {'svg': 'http://www.w3.org/2000/svg'}
MERMAID = PART.parent / '_notebook/mermaid'
SKIP = re.compile(r'^(?:classDef|class|style|linkStyle|subgraph|direction|click)\b|^end$')
LINK = re.compile(r'\s*(<?(?:-{2,}|-\.+-|={2,})[>xo]?)\s*')


def normalized(text):
    return ' '.join(text.split())


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


def mermaid_report(path, source):
    svg = ET.fromstring(path.read_text())
    text = source.read_text(encoding='utf-8')
    texts = [squeezed(''.join(e.itertext())) for e in svg.iter() if e.tag.split('}')[-1] == 'text']
    labels = mermaid_labels(text)
    missing = [label for label in labels if not label_visible(label, texts)]
    svg_arrows = sum(('marker-end' in e.attrib) + ('marker-start' in e.attrib) for e in svg.iter())
    source_arrows = mermaid_arrows(text)
    stamp = path.with_suffix('.render.json')
    current = stamp.is_file() and json.loads(stamp.read_text()).get('sha256') == render_digest(source)
    return {'file': str(path.relative_to(PART)), 'editable_source': 'mmd',
            'labels_match': bool(labels) and not missing, 'missing_labels': missing,
            'svg_arrows': svg_arrows, 'mmd_arrows': source_arrows, 'arrows_match': svg_arrows == source_arrows,
            'render_current': current, 'png_present': path.with_suffix('.png').is_file(),
            'svg_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'mmd_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}


def main():
    reports = []
    for path in sorted(PART.glob('ch*/figures/[0-9]*.svg')):
        if path.with_suffix('.mmd').is_file():
            reports.append(mermaid_report(path, path.with_suffix('.mmd')))
            continue
        drawing = path.with_suffix('.excalidraw')
        assert drawing.is_file(), f'Missing editable source: {path.name}'
        svg = ET.fromstring(path.read_text())
        source = json.loads(drawing.read_text())
        elements = [e for e in source['elements'] if not e.get('isDeleted')]
        svg_labels = sorted(normalized(''.join(e.itertext())) for e in svg.findall('.//svg:text', NS))
        source_labels = sorted(normalized(e['text']) for e in elements if e['type'] == 'text')
        svg_arrows = sum(bool(e.get('marker-end')) for e in svg.iter())
        source_arrows = sum(e['type'] == 'arrow' for e in elements)
        reports.append({'file': str(path.relative_to(PART)),
                        'labels_match': svg_labels == source_labels,
                        'svg_arrows': svg_arrows, 'excalidraw_arrows': source_arrows,
                        'arrows_match': svg_arrows == source_arrows,
                        'svg_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                        'excalidraw_sha256': hashlib.sha256(drawing.read_bytes()).hexdigest()})
    assert reports, 'No Part 5 figures found'
    (PART / 'qa/figure-consistency.json').write_text(json.dumps(reports, ensure_ascii=False, indent=2))
    assert all(r['labels_match'] and r['arrows_match'] and r.get('render_current', True) and r.get('png_present', True)
               for r in reports), 'Figure mismatch; see report'
    mermaid = sum(r.get('editable_source') == 'mmd' for r in reports)
    print(f'{len(reports)} SVG/source pairs ({mermaid} Mermaid .mmd, {len(reports) - mermaid} Excalidraw): '
          'labels and arrow counts match, Mermaid renders current')


if __name__ == '__main__':
    main()
