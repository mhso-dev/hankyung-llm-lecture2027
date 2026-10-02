"""headfix.py SPEC.json — 도구 파일 머리 설명 줄만 바꾼다.
SPEC: {"tool": 도구 파일, "gens": [머리 글을 가진 생성기 파일...], "reps": [[옛 줄, 새 줄], ...]}
- 옛 줄은 도구 파일과 각 생성기에 꼭 한 번씩 있어야 한다(아니면 멈춤).
- 바꾼 도구 파일은 모듈 설명 문자열만 다르고, 나머지 AST·설명 문자열 뒤 글자가 옛 파일과 같아야 한다(아니면 멈춤).
- 기본은 확인만(--write를 주면 쓴다)."""
import ast, hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
spec = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
write = '--write' in sys.argv
tool = Path(spec['tool']); old = tool.read_text(encoding='utf-8')
new = old
for a, b in spec['reps']:
    assert old.count(a) == 1, ('tool count', old.count(a), a)
    new = new.replace(a, b)
t_old = ast.parse(old); t_new = ast.parse(new)
d_old = ast.get_docstring(t_old, clean=False); d_new = ast.get_docstring(t_new, clean=False)
assert d_old != d_new
assert [ast.dump(n) for n in t_old.body[1:]] == [ast.dump(n) for n in t_new.body[1:]], 'body differs'
end_old = t_old.body[0].end_lineno; end_new = t_new.body[0].end_lineno
assert old.splitlines(True)[end_old:] == new.splitlines(True)[end_new:], 'text after docstring differs'
print('tool', tool, hashlib.sha256(old.encode()).hexdigest(), '->', hashlib.sha256(new.encode()).hexdigest())
print('docstring lines', len(d_old.splitlines()), '->', len(d_new.splitlines()), '| body nodes same', len(t_old.body) - 1)
gnew = {}
for g in spec['gens']:
    gp = Path(g); gt = gp.read_text(encoding='utf-8'); nt = gt
    for a, b in spec['reps']:
        assert gt.count(a) == 1, ('gen count', g, gt.count(a), a)
        nt = nt.replace(a, b)
    ast.parse(nt)
    gnew[gp] = nt
    print('gen', gp.name, hashlib.sha256(gt.encode()).hexdigest()[:12], '->', hashlib.sha256(nt.encode()).hexdigest()[:12])
if write:
    for gp, nt in gnew.items():
        gp.write_text(nt, encoding='utf-8')
    tool.write_text(new, encoding='utf-8')
    print('written')
