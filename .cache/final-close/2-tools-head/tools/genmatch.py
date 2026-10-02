"""genmatch.py TEXTBOOK_CH_DIR LAB_DIR NN [NN...] — 생성기 cells()가 지금 노트북 셀 글과 같은지 셉니다(쓰기 없음).
다른 셀은 번호·종류와 첫 차이 줄을 보입니다."""
import sys, json, glob, importlib, os
sys.dont_write_bytecode = True
ROOT = os.path.expanduser('~/mnt/한국경제신문')
CH = os.path.join(ROOT, sys.argv[1]); LAB = os.path.join(ROOT, sys.argv[2], 'notebooks')
sys.path.insert(0, CH + '/qa/upgrade'); sys.path.insert(0, ROOT + '/textbook/_notebook/upgrade')
import nbkit
def s(x): return x if isinstance(x, str) else ''.join(x)
for n in sys.argv[3:]:
    mod = importlib.import_module('author_' + n)
    gen = mod.cells()
    nbp = glob.glob(LAB + '/' + n + '-*.ipynb')[0]
    nb = json.load(open(nbp, encoding='utf-8'))
    if len(gen) != len(nb['cells']):
        gen = nbkit.split_part_boundaries(gen)
    same = 0; diffs = []
    for i, (g, c) in enumerate(zip(gen, nb['cells'])):
        gs = s(g['source']).strip('\n'); cs = s(c['source']).strip('\n')
        if gs == cs and g['cell_type'] == c['cell_type']:
            same += 1
        else:
            gl = gs.splitlines(); cl = cs.splitlines(); k = 0
            while k < min(len(gl), len(cl)) and gl[k] == cl[k]: k += 1
            diffs.append((i, c['cell_type'], (gl[k] if k < len(gl) else '')[:90], (cl[k] if k < len(cl) else '')[:90]))
    print(n, 'cells same', same, '/', len(gen), 'nb', len(nb['cells']), 'diff', len(diffs))
    for d in diffs[:6]: print('   ', d)
