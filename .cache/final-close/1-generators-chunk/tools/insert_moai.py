import ast, sys
D = sys.argv[1]
for row in open(sys.argv[2], encoding='utf-8'):
    name, part, chs = row.rstrip('\n').split('\t')
    p = f"{D}/{name}.py"
    src = open(p, encoding='utf-8').read()
    body = ast.parse(src).body
    pos = 0; i = 0
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], 'value', None), ast.Constant) and isinstance(body[0].value.value, str):
        pos = body[0].end_lineno; i = 1
    while i < len(body) and isinstance(body[i], ast.ImportFrom) and body[i].module == '__future__':
        pos = body[i].end_lineno; i += 1
    line = f'raise SystemExit("옛 Part {part} 보조 스크립트({name}.py)입니다. 실행하면 {chs} 개선본을 옛 글로 덮어씁니다. 개선본은 각 챕터 qa/upgrade/author_NN.py를 쓰세요.")\n'
    lines = src.splitlines(keepends=True)
    new = ''.join(lines[:pos] + [line] + lines[pos:])
    ast.parse(new)
    open(p, 'w', encoding='utf-8').write(new)
    print(pos + 1, p)
