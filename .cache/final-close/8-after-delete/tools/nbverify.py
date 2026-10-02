import json, hashlib, re
from pathlib import Path
ROOT = Path.home() / "mnt" / "한국경제신문"
G = json.load(open("/sessions/rcw-01fa62dwjghtyrmrgyqrfwx5/mnt/한국경제신문/.cache/final-close/8-after-delete/log/gates-result.json"))

def src(c):
    return c['source'] if isinstance(c['source'], str) else ''.join(c['source'])

def code_hash(nb):
    source = [src(c) for c in nb['cells'] if c['cell_type'] == 'code']
    return hashlib.sha256(json.dumps(source, ensure_ascii=False).encode()).hexdigest()

def output_hash(nb):
    outputs = json.loads(json.dumps([c.get('outputs', []) for c in nb['cells'] if c['cell_type'] == 'code']))
    for group in outputs:
        for output in group:
            if isinstance(output.get('text'), list):
                output['text'] = ''.join(output['text'])
            for mime, value in output.get('data', {}).items():
                if isinstance(value, list) and mime.startswith('text/'):
                    output['data'][mime] = ''.join(value)
    return hashlib.sha256(json.dumps(outputs, ensure_ascii=False, sort_keys=True).encode()).hexdigest()

def out_text(o):
    if o.get('output_type') == 'stream':
        t = o.get('text', '')
        return t if isinstance(t, str) else ''.join(t)
    if o.get('output_type') == 'error':
        return '\n'.join(o.get('traceback', [])) + '\n' + o.get('ename', '') + ': ' + o.get('evalue', '')
    d = o.get('data', {}).get('text/plain', '')
    return d if isinstance(d, str) else ''.join(d)

ANSI = re.compile(r'\x1b\[[0-9;]*m')
result = {}
for name, v in G.items():
    lab = ROOT / v['lab']
    nbdir = lab / 'notebooks'
    files = sorted(nbdir.glob('*.ipynb'))
    slugset = set(v['slugs'])
    rows = []
    for f in files:
        nb = json.loads(f.read_text(encoding='utf-8'))
        ver = nb.get('metadata', {}).get('verification')
        ch, oh = code_hash(nb), output_hash(nb)
        ncode = sum(1 for c in nb['cells'] if c['cell_type'] == 'code')
        row = {'file': f.name, 'section': f.stem in slugset, 'has_ver': ver is not None}
        if ver:
            row.update(status=ver.get('status'), allow_errors=ver.get('allow_errors'),
                       code_ok=ver.get('code_sha256') == ch, out_ok=ver.get('outputs_sha256') == oh,
                       cells_ok=ver.get('code_cells') == ncode, executed_at=ver.get('executed_at'),
                       fresh=ver.get('fresh_kernel'))
        # errors
        errs = []
        cells = nb['cells']
        for i, c in enumerate(cells):
            if c['cell_type'] != 'code':
                continue
            for o in c.get('outputs', []):
                t = ANSI.sub('', out_text(o))
                is_err = o.get('output_type') == 'error'
                tb = 'Traceback' in t
                errline = any(l.startswith('Error') for l in t.splitlines())
                if is_err or tb or errline:
                    prev = ''
                    j = i - 1
                    while j >= 0 and cells[j]['cell_type'] != 'markdown':
                        j -= 1
                    if j >= 0:
                        prev = src(cells[j])
                    nxt = ''
                    j = i + 1
                    while j < len(cells) and cells[j]['cell_type'] != 'markdown':
                        j += 1
                    if j < len(cells):
                        nxt = src(cells[j])
                    first_line = src(c).splitlines()[0] if src(c).strip() else ''
                    tags = c.get('metadata', {}).get('tags', [])
                    errs.append({'cell': i, 'kind': 'error_output' if is_err else ('traceback_text' if tb else 'Error_line'),
                                 'ename': o.get('ename'), 'tags': tags,
                                 'lesson_part': c.get('metadata', {}).get('lesson_part'),
                                 'first_line': first_line[:120],
                                 'err_lines': [l[:160] for l in t.splitlines() if l.startswith('Error') or 'Traceback' in l or (is_err and l.startswith(str(o.get('ename'))))][:3],
                                 'prev_md': prev[:300].replace('\n', ' '), 'next_md': nxt[:300].replace('\n', ' ')})
        row['errors'] = errs
        rows.append(row)
    result[name] = rows
Path('/sessions/rcw-01fa62dwjghtyrmrgyqrfwx5/mnt/한국경제신문/.cache/final-close/8-after-delete/log/nbverify-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding='utf-8')
tot = 0; nover = 0; bad = []; errnb = []
for name, rows in result.items():
    for r in rows:
        tot += 1
        if not r['has_ver']:
            nover += 1
            bad.append((name, r['file'], 'no_verification', r['section']))
        else:
            if not (r['code_ok'] and r['out_ok'] and r['cells_ok'] and r['status'] == 'passed'):
                bad.append((name, r['file'], f"status={r['status']} code={r['code_ok']} out={r['out_ok']} cells={r['cells_ok']}", r['section']))
        if r['errors']:
            errnb.append((name, r['file'], len(r['errors'])))
print('notebooks', tot, 'no_ver', nover)
print('section notebooks', sum(1 for rows in result.values() for r in rows if r['section']))
for b in bad: print('BAD', b)
print('--- error notebooks', len(errnb))
for e in errnb: print(e)
