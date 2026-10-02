"""Validate source/build structure and exact execution evidence inclusion."""
from __future__ import annotations

import ast
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT.parents[2] / 'labs' / 'part3' / 'ch10-document-processing'
rows = []
for source in sorted((ROOT / '_src').glob('[0-9][0-9]-*.html')):
    raw = source.read_text()
    rendered = (ROOT / source.name).read_text()
    prose = re.sub(r'<pre\b.*?</pre>', '', raw, flags=re.S)
    prose = re.sub(r'\{\{.*?\}\}|<!--.*?-->', '', prose, flags=re.S)
    prose = html.unescape(re.sub('<[^>]+>', '', prose))
    errors = []
    ids = re.findall(r'id="(b\d+)"', raw)
    if ids != [f'b{i}' for i in range(1,12)]: errors.append('11 ordered blocks missing or duplicate')
    if len(re.findall('[가-힣]', prose)) < 2500: errors.append('fewer than 2500 Korean characters')
    if '{{' in rendered: errors.append('unresolved placeholder')
    if not re.search(r'<details[^>]*class="instructor"', raw): errors.append('instructor details absent')
    codes = re.findall(r'\{\{code:([^}]+)\}\}', raw)
    outputs = re.findall(r'\{\{output:([^}]+)\}\}', raw)
    if not codes or not outputs: errors.append('executed source or output absent')
    for spec in codes:
        filename, _, name = spec.partition('#')
        text = (LAB / filename).read_text()
        if name:
            node = next(n for n in ast.walk(ast.parse(text)) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and n.name == name)
            text = '\n'.join(text.splitlines()[node.lineno-1:node.end_lineno])
        if html.escape(text.rstrip()) not in rendered: errors.append(f'code mismatch {spec}')
    for name in outputs:
        text=(LAB/'runs'/'examples'/name).read_text().rstrip()
        if html.escape(text) not in rendered:errors.append(f'output mismatch {name}')
    if re.search('함정|돌려줍|돌립니다|당연히|쉽게|회수 지점|선수 지식 회수',prose):errors.append('prohibited wording')
    for href in re.findall(r'href="([^"#]+)(?:#[^"]*)?"', rendered):
        if not href.startswith(('https://','http://')) and not (ROOT/href).exists(): errors.append(f'missing link {href}')
    rows.append({'section':source.name,'korean_chars':len(re.findall('[가-힣]',prose)),'code_blocks':len(codes),'outputs':len(outputs),'errors':errors,'pass':not errors})
report={'sections':len(rows),'passed':sum(r['pass'] for r in rows),'results':rows}
(ROOT/'qa'/'content-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(0 if len(rows)==8 and all(r['pass'] for r in rows) else 1)
