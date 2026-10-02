"""§2-7 리팩터 수치: 노트북마다 코드 셀 수와 코드 줄 수(주석·빈 줄 제외)를 센다.

사용: python3 textbook/_notebook/upgrade/count_code.py <노트북 폴더> [<비교할 노트북 폴더>] [--tools 도구파일.py]
  폴더 하나면 그 폴더의 [0-9][0-9]-*.ipynb 를 센다. 둘이면 앞을 「전」, 뒤를 「후」로 표를 만든다.
  --tools 를 주면 도구 파일의 코드 줄(주석·빈 줄·독스트링 제외)도 따로 센다.
세는 법: 코드 셀의 줄 가운데 공백만 있는 줄과 `#`로 시작하는 줄을 뺀 수(`%pip` 줄은 센다).
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


def count_notebook(path: Path) -> tuple[int, int]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = 0
    lines = 0
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        cells += 1
        source = cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])
        for line in source.splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                lines += 1
    return cells, lines


def count_tools(path: Path) -> int:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    docstring_lines = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant) and isinstance(first.value.value, str):
                docstring_lines.update(range(first.lineno, first.end_lineno + 1))
    total = 0
    for number, line in enumerate(source.splitlines(), start=1):
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and number not in docstring_lines:
            total += 1
    return total


def main() -> int:
    args = sys.argv[1:]
    tools = None
    if "--tools" in args:
        index = args.index("--tools")
        tools = Path(args[index + 1])
        args = args[:index] + args[index + 2:]
    folders = [Path(arg) for arg in args]
    rows = {}
    for column, folder in enumerate(folders):
        for path in sorted(folder.glob("[0-9][0-9]-*.ipynb")):
            rows.setdefault(path.name[:2], [None] * len(folders))[column] = count_notebook(path)
    if len(folders) == 1:
        print("절 | 코드 셀 | 코드 줄")
    else:
        print("절 | 코드 셀 전 → 후 | 코드 줄 전 → 후 | 줄 차이")
    sums = [[0, 0] for _ in folders]
    for number in sorted(rows):
        values = rows[number]
        for column, value in enumerate(values):
            if value:
                sums[column][0] += value[0]
                sums[column][1] += value[1]
        if len(folders) == 1:
            print(number, "|", values[0][0], "|", values[0][1])
        else:
            before, after = values[0], values[1]
            print(number, "|", before[0], "→", after[0], "|", before[1], "→", after[1], "|", after[1] - before[1])
    if len(folders) == 1:
        print("합계 |", sums[0][0], "|", sums[0][1])
    else:
        print("합계 |", sums[0][0], "→", sums[1][0], "|", sums[0][1], "→", sums[1][1], "|", sums[1][1] - sums[0][1])
    if tools:
        print("도구 파일", tools.name, "코드 줄:", count_tools(tools))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
