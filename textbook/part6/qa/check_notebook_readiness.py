"""Check the beginner-facing constraints that execution alone does not prove.

전체 마감 2026-10-01: 노트북 수 고정값(Part 5 21개·Part 6 47개 — 실습 절 전)을 지금 구조에 맞게 고침 —
각 챕터 chapter.json의 절 목록(챕터 끝 실습 절 포함)과 노트북 이름이 같아야 한다. 나머지 규칙은 그대로.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> None:
    reports = []
    for path in sorted((ROOT / 'labs/part6').glob('*/notebooks/*.ipynb')):
        notebook = json.loads(path.read_text())
        cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        missing_comments, missing_annotations = [], []
        generic_comments = []
        has_install_cell = any('%pip install' in ''.join(cell['source']) for cell in cells)
        assertions, maximum = 0, 0
        for index, cell in enumerate(cells, 1):
            source = ''.join(cell['source'])
            maximum = max(maximum, len(source.splitlines()))
            if not any(line.strip().startswith('#') for line in source.splitlines()):
                missing_comments.append(index)
            if '이 셀의 학습 동작을 실행하고 출력으로 확인합니다' in source:
                generic_comments.append(index)
            python = '\n'.join(line for line in source.splitlines()
                               if not line.lstrip().startswith(('%', '!')))
            tree = ast.parse(python)
            assertions += sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    args = node.args.posonlyargs + node.args.args + node.args.kwonlyargs
                    if node.returns is None or any(arg.annotation is None and arg.arg not in
                                                  ('self', 'cls') for arg in args):
                        missing_annotations.append(node.name)
        reports.append({'notebook': str(path.relative_to(ROOT)), 'code_cells': len(cells),
                        'max_cell_lines': maximum, 'missing_comments': missing_comments,
                        'missing_annotations': missing_annotations, 'assertions': assertions,
                        'has_install_cell': has_install_cell, 'generic_comments': generic_comments})
    (Path(__file__).parent / 'notebook-readiness.json').write_text(
        json.dumps(reports, ensure_ascii=False, indent=2))
    expected = []
    for config in sorted((ROOT / 'textbook/part6').glob('ch*/chapter.json')):
        lab = json.loads(config.read_text())['lab_path']
        expected += [f"{lab}/notebooks/{s['slug']}.ipynb" for s in json.loads(config.read_text())['sections']]
    assert sorted(r['notebook'] for r in reports) == sorted(expected), 'Notebooks differ from chapter.json sections'
    assert all(r['max_cell_lines'] <= 25 and not r['missing_comments'] and
               not r['missing_annotations'] and not r['generic_comments']
               and r['assertions'] and r['has_install_cell']
               for r in reports), reports
    print(f'{len(reports)} notebooks: install cells, annotated functions, purpose comments, assertions, and <=25 lines/cell')


if __name__ == '__main__':
    main()
