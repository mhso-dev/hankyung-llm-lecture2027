import json, sys, hashlib
sys.path.insert(0, __import__('os').path.expanduser('~/mnt/한국경제신문/textbook/_notebook'))
sys.dont_write_bytecode = True
from execute import code_hash, output_hash
for p in sys.argv[1:]:
    nb = json.load(open(p, encoding='utf-8')); v = nb['metadata'].get('verification', {})
    ch, oh = code_hash(nb), output_hash(nb)
    print(f"code {ch[:16]} (meta {v.get('code_sha256','')[:16]} {'=' if ch==v.get('code_sha256') else 'X'}) out {oh[:16]} (meta {v.get('outputs_sha256','')[:16]} {'=' if oh==v.get('outputs_sha256') else 'X'}) file {hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]} {p.split('/')[-1]}")
