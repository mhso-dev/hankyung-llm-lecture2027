"""조건 (가): 도구 파일 머리 글(모듈 설명 문자열 줄)·해시가 노트북 마크다운·출력(·코드)·_src·HTML에 나오는지 (읽기만).
사용: headscan.py ROOT LAB_DIR TEXTBOOK_DIR TOOL_NAME [추가해시 ...]"""
import ast, hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(sys.argv[1]); lab = ROOT / sys.argv[2]; tb = ROOT / sys.argv[3]; name = sys.argv[4]
extra = sys.argv[5:]
tool = lab / 'notebooks' / name
text = tool.read_text(encoding='utf-8')
doc = ast.get_docstring(ast.parse(text), clean=False) or ''
lines = [l.strip() for l in doc.splitlines() if len(l.strip()) >= 8]
h = hashlib.sha256(text.encode()).hexdigest()
needles = [('head', l) for l in lines]
for hh in [h] + extra:
    needles += [('hash', hh[:8]), ('hash', hh[:12])]
print('tool', tool.relative_to(ROOT), h, 'head lines', len(lines))
def texts_of_nb(nb):
    for i, c in enumerate(nb['cells']):
        src = c['source'] if isinstance(c['source'], str) else ''.join(c['source'])
        if c['cell_type'] == 'markdown':
            yield ('md', i, src)
        elif c['cell_type'] == 'code':
            yield ('code', i, src)
            for o in c.get('outputs', []):
                t = o.get('text', '')
                if isinstance(t, list): t = ''.join(t)
                yield ('out', i, t)
                for mime, v in o.get('data', {}).items():
                    if isinstance(v, list): v = ''.join(v)
                    if isinstance(v, str): yield ('out', i, v)
                if 'traceback' in o: yield ('out', i, '\n'.join(o['traceback']))
hits = 0
for p in sorted((lab / 'notebooks').glob('*.ipynb')):
    nb = json.loads(p.read_text(encoding='utf-8'))
    for kind, i, t in texts_of_nb(nb):
        for nk, n in needles:
            if n in t:
                hits += 1; print('HIT', kind, nk, p.name, 'cell', i, repr(n[:60]))
        if kind == 'code' and ('__doc__' in t or ('open(' in t and name in t)):
            print('CODE-READS-TOOL?', p.name, i)
files = sorted((tb / '_src').glob('*.html')) + sorted(tb.glob('*.html')) + [lab / 'README.md']
for p in files:
    t = p.read_text(encoding='utf-8')
    for nk, n in needles:
        if n in t:
            print('HIT-TEXT', nk, p.relative_to(ROOT), repr(n[:60]))
print('notebook hits', hits)
