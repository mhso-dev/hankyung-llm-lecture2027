"""실행한 노트북(묶음 사본)과 저장 노트북을 셀별로 견준다. 쓰는 법: cmp_nb.py 결과.json 실행본:저장본 ..."""
import json, sys, hashlib, difflib, os
HOME = os.path.expanduser('~')


def norm(outputs):
    res = []
    for o in outputs:
        o = json.loads(json.dumps(o))
        o.pop('execution_count', None)
        if isinstance(o.get('text'), list):
            o['text'] = ''.join(o['text'])
        for k, v in list(o.get('data', {}).items()):
            if isinstance(v, list):
                o['data'][k] = ''.join(v)
        res.append(o)
    return res


def merge_streams(outs):
    res = []
    for o in outs:
        if res and o.get('output_type') == 'stream' and res[-1].get('output_type') == 'stream' and res[-1].get('name') == o.get('name'):
            res[-1] = dict(res[-1], text=res[-1]['text'] + o['text'])
        else:
            res.append(dict(o))
    return res


def text(outs):
    parts = []
    for o in outs:
        if 'text' in o:
            parts.append(o['text'])
        for k, v in o.get('data', {}).items():
            if k.startswith('text/plain'):
                parts.append(v)
        if o.get('output_type') == 'error':
            parts.append(o.get('ename', '') + ': ' + o.get('evalue', ''))
    return ''.join(parts).replace(HOME, '[사용자 폴더]')


out = sys.argv[1]
report = []
for pair in sys.argv[2:]:
    run, saved = pair.split(':', 1)
    a = json.load(open(run)); b = json.load(open(saved))
    ca = [c for c in a['cells'] if c['cell_type'] == 'code']
    cb = [c for c in b['cells'] if c['cell_type'] == 'code']
    src = lambda c: c['source'] if isinstance(c['source'], str) else ''.join(c['source'])
    same, split, diffs = 0, 0, []
    for i, (x, y) in enumerate(zip(ca, cb), 1):
        if src(x) != src(y):
            diffs.append({'code_cell': i, 'kind': 'source differs'}); continue
        if norm(x.get('outputs', [])) == norm(y.get('outputs', [])):
            same += 1
        elif merge_streams(norm(x.get('outputs', []))) == merge_streams(norm(y.get('outputs', []))):
            split += 1
        else:
            d = list(difflib.unified_diff(text(norm(y.get('outputs', []))).splitlines(),
                                          text(norm(x.get('outputs', []))).splitlines(), 'saved', 'run', lineterm='', n=0))
            diffs.append({'code_cell': i, 'kind': 'outputs differ', 'diff': d[:40]})
    va = a['metadata'].get('verification', {}); vb = b['metadata'].get('verification', {})
    report.append({'run': run.replace(HOME, '~'), 'saved': saved, 'code_cells': len(cb), 'run_code_cells': len(ca),
                   'same_cells': same, 'stream_split_only_cells': split, 'diff_cells': len(diffs),
                   'code_sha256_same': va.get('code_sha256') == vb.get('code_sha256'),
                   'outputs_sha256_run': va.get('outputs_sha256'), 'outputs_sha256_saved': vb.get('outputs_sha256'),
                   'saved_file_sha256': hashlib.sha256(open(saved, 'rb').read()).hexdigest(),
                   'diffs': diffs})
    print(f"{saved}: 코드 셀 {len(cb)} · 같음 {same} · 스트림 나뉨만 {split} · 다름 {len(diffs)} {[d['code_cell'] for d in diffs]} · code_sha256 같음 {va.get('code_sha256') == vb.get('code_sha256')} · outputs_sha256 같음 {va.get('outputs_sha256') == vb.get('outputs_sha256')}")
json.dump(report, open(out, 'w'), ensure_ascii=False, indent=2)
