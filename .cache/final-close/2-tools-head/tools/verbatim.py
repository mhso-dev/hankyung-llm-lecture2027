"""verbatim.py TOOL LAB_OF_CHAPTER CHNUM [다른 챕터 원본 파일...] — 도구 파일 함수마다 「# Ch NN MM절」 줄 아래 설명 주석+본문이
그 절 노트북 코드 셀(이 챕터) 또는 주어진 원본 파일(다른 챕터)에 글자 그대로 있는지 봅니다(읽기만)."""
import ast, json, glob, re, sys, os
ROOT = os.path.expanduser('~/mnt/한국경제신문')
tool, lab, chnum = sys.argv[1], sys.argv[2], sys.argv[3]; others = sys.argv[4:]
src = open(tool, encoding='utf-8').read(); lines = src.splitlines()
other_texts = {o: open(o, encoding='utf-8').read() for o in others}
def cells_of(pattern):
    out = []
    for nb in glob.glob(pattern):
        out += [c['source'] if isinstance(c['source'], str) else ''.join(c['source']) for c in json.load(open(nb))['cells'] if c['cell_type'] == 'code']
    return out
for n in ast.parse(src).body:
    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
        top = n.lineno - 1
        while top > 0 and lines[top - 1].startswith('# '): top -= 1
        note = lines[top]; block = '\n'.join(lines[top + 1:n.end_lineno])
        m = re.match(r'# Ch (\d+) (\d+)절', note); ch, sec = m.group(1), m.group(2)
        if ch == chnum:
            ok = any(block in c for c in cells_of(f'{lab}/notebooks/{sec}-*.ipynb')); where = f'this ch {sec} cell'
        else:
            hits = [o.split('/')[-1] for o, t in other_texts.items() if block in t]
            nbhits = [p for p in glob.glob(f'{ROOT}/labs/part*/ch{int(ch):02d}-*/notebooks/{sec}-*.ipynb') if any(block in c for c in cells_of(p))]
            ok = bool(hits or nbhits); where = f'Ch {ch} {sec}: files {hits} nb {[p.split("/")[-1][:20] for p in nbhits]}'
        print(f'{n.name:22s} {"OK" if ok else "NO":3s} {where}')
