"""importcheck.py LAB_NOTEBOOKS_DIR MODULE OLD_TOOL NEW_TOOL — 노트북마다 도구 파일에서 가져오는 이름이 새 파일에 있고,
그 함수의 AST가 옛 파일과 같은지, 옛·새 파일의 모든 최상위 문(설명 문자열 뺌)이 같은지 봅니다(쓰기 없음)."""
import ast, json, sys
from pathlib import Path
lab = Path(sys.argv[1]); mod = sys.argv[2]
old = ast.parse(Path(sys.argv[3]).read_text(encoding='utf-8')); new = ast.parse(Path(sys.argv[4]).read_text(encoding='utf-8'))
def defs(t): return {n.name: ast.dump(n) for n in t.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
do, dn = defs(old), defs(new)
print('top-level (docstring 뺌) same:', [ast.dump(n) for n in old.body[1:]] == [ast.dump(n) for n in new.body[1:]], '| functions', len(dn), '| all defs same', do == dn)
for p in sorted(lab.glob('*.ipynb')):
    nb = json.loads(p.read_text(encoding='utf-8')); names = []
    for c in nb['cells']:
        if c['cell_type'] != 'code': continue
        src = c['source'] if isinstance(c['source'], str) else ''.join(c['source'])
        src = '\n'.join(l for l in src.splitlines() if not l.lstrip().startswith(('%', '!')))
        try: tree = ast.parse(src)
        except SyntaxError: continue
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom) and n.module == mod: names += [a.name for a in n.names]
            if isinstance(n, ast.Import) and any(a.name == mod for a in n.names): names.append('*module*')
    ok = all(nm in dn and dn[nm] == do.get(nm) for nm in names if nm != '*module*')
    print(' ', p.name, 'imports', names or '-', 'OK' if ok else 'PROBLEM')
