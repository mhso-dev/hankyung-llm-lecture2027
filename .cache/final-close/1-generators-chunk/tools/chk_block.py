import ast, sys, hashlib
def top_raise(p):
    src = open(p, encoding='utf-8').read()
    t = ast.parse(src)
    for n in t.body:
        if isinstance(n, ast.Raise) and n.lineno <= 60:
            e = n.exc
            f = e.func if isinstance(e, ast.Call) else e
            if isinstance(f, ast.Name) and f.id == 'SystemExit':
                return n.lineno
    return None
for p in sys.argv[1:]:
    h = hashlib.sha256(open(p,'rb').read()).hexdigest()
    n = sum(1 for _ in open(p, encoding='utf-8'))
    print(f"{top_raise(p)}\t{h[:16]}\t{n}\t{p}")
