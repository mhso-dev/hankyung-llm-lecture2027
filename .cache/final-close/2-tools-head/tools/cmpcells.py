"""cmpcells.py SAVED.ipynb RUN.ipynb — 코드 셀마다 출력이 같은지(그대로 / 같은 이름 스트림을 이어 붙여) 셉니다."""
import json, sys, hashlib
def s(x): return x if isinstance(x, str) else ''.join(x)
def norm(outs, merge):
    res = []
    for o in outs:
        o = json.loads(json.dumps(o))
        o.pop('execution_count', None)
        if 'text' in o: o['text'] = s(o['text'])
        for k, v in o.get('data', {}).items():
            if isinstance(v, list) and k.startswith('text/'): o['data'][k] = s(v)
        if merge and o.get('output_type') == 'stream' and res and res[-1].get('output_type') == 'stream' and res[-1].get('name') == o.get('name'):
            res[-1]['text'] += o['text']; continue
        res.append(o)
    return res
a = json.load(open(sys.argv[1], encoding='utf-8')); b = json.load(open(sys.argv[2], encoding='utf-8'))
ca = [c for c in a['cells'] if c['cell_type'] == 'code']; cb = [c for c in b['cells'] if c['cell_type'] == 'code']
assert [s(c['source']) for c in ca] == [s(c['source']) for c in cb], 'code differs'
exact = merged = 0; diffs = []; monly = []
for i, (x, y) in enumerate(zip(ca, cb)):
    if norm(x.get('outputs', []), False) == norm(y.get('outputs', []), False): exact += 1; merged += 1
    elif norm(x.get('outputs', []), True) == norm(y.get('outputs', []), True): merged += 1; monly.append(i)
    else: diffs.append(i)
va = a['metadata'].get('verification', {}); vb = b['metadata'].get('verification', {})
print(sys.argv[1].split('/')[-1], 'code cells', len(ca), 'same', exact, 'same(merged streams)', merged, 'stream-split-only cells', monly, 'diff cells', diffs,
      '| outputs_sha256 saved', va.get('outputs_sha256', '-')[:12], 'run', vb.get('outputs_sha256', '-')[:12], 'equal' if va.get('outputs_sha256') == vb.get('outputs_sha256') else 'differ',
      '| code_sha256 equal', va.get('code_sha256') == vb.get('code_sha256'))
for i in diffs[:5]:
    print('  cell', i, 'saved:', json.dumps(norm(ca[i].get('outputs', []), True), ensure_ascii=False)[:300])
    print('  cell', i, 'run  :', json.dumps(norm(cb[i].get('outputs', []), True), ensure_ascii=False)[:300])
