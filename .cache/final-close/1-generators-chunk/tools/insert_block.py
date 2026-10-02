import ast, sys
FIG = 'raise SystemExit("옛 도식 생성기 — 품질 개선 뒤 실행 금지. 지금 판 그림은 figures/*.mmd를 textbook/_notebook/mermaid/render_mermaid.py로 렌더하고, 절 생성기는 qa/upgrade/author_*.py")\n'
GEN = 'raise SystemExit("옛 생성기 — 품질 개선 뒤 실행 금지. 지금 판은 qa/upgrade/author_*.py")\n'
for p in sys.argv[1:]:
    src = open(p, encoding='utf-8').read()
    tree = ast.parse(src)
    pos = 0
    body = tree.body
    i = 0
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], 'value', None), ast.Constant) and isinstance(body[0].value.value, str):
        pos = body[0].end_lineno; i = 1
    while i < len(body) and isinstance(body[i], ast.ImportFrom) and body[i].module == '__future__':
        pos = body[i].end_lineno; i += 1
    line = FIG if p.endswith('_gen_figures.py') else GEN
    lines = src.splitlines(keepends=True)
    ins = ['\n', line] if pos > 0 else [line, '\n']
    new = ''.join(lines[:pos] + ins + lines[pos:])
    ast.parse(new)
    open(p, 'w', encoding='utf-8').write(new)
    print(pos + (2 if pos > 0 else 1), p)
