"""노트북 파일 해시·메타 code/outputs 해시·다시 잰 값을 표로 출력 (읽기만)."""
import hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(sys.argv[1])
def code_hash(nb):
    source = [c['source'] if isinstance(c['source'], str) else ''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code']
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
for lab in sys.argv[2:]:
    for p in sorted((ROOT / lab / 'notebooks').glob('*.ipynb')):
        raw = p.read_bytes()
        nb = json.loads(raw)
        v = nb.get('metadata', {}).get('verification', {})
        print('\t'.join([str(p.relative_to(ROOT)), hashlib.sha256(raw).hexdigest(), v.get('code_sha256', '-'), v.get('outputs_sha256', '-'), code_hash(nb), output_hash(nb), str(v.get('executed_at', '-'))]))
