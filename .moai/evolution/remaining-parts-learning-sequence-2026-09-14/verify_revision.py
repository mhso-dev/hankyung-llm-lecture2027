"""Compare the remaining parts revision with its saved pre-edit notebooks and sources."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'textbook/_notebook'))
from execute import code_hash, output_hash
from render import validate, validate_parts, text


def markdown_cells(notebook):
    return [text(c['source']) for c in notebook['cells'] if c['cell_type'] == 'markdown']


def main():
    rows = []
    for chapter in sorted(ROOT.glob('textbook/part[2-7]/ch*')):
        for src in sorted((chapter / '_src').glob('[0-9]*.html')):
            slug = src.stem
            path = ROOT / 'labs' / chapter.parent.name / chapter.name / 'notebooks' / (slug + '.ipynb')
            old_path = HERE / 'before' / path.relative_to(ROOT)
            nb, old = json.loads(path.read_text()), json.loads(old_path.read_text())
            try:
                validate(nb)
                validate_parts(nb)
            except Exception as error:
                raise RuntimeError(f"{path}: {error}") from error
            source_changed = src.read_bytes() != (HERE / 'before' / src.relative_to(ROOT)).read_bytes()
            markdown_changed = markdown_cells(nb) != markdown_cells(old)
            assert source_changed, f'Section not revised: {src}'
            assert markdown_changed, f'Notebook prose not revised: {path}'
            same_code, same_outputs = code_hash(nb) == code_hash(old), output_hash(nb) == output_hash(old)
            if not same_code:
                assert nb['metadata']['verification']['executed_at'] != old['metadata']['verification']['executed_at'], path
            rows.append({
                'chapter': chapter.name, 'section': slug,
                'source_revised': source_changed, 'notebook_markdown_revised': markdown_changed,
                'code_preserved': same_code, 'outputs_preserved': same_outputs,
                'execution_verified_at': nb['metadata']['verification']['executed_at'],
                'code_cells': sum(c['cell_type'] == 'code' for c in nb['cells']),
                'source_sha256': hashlib.sha256(src.read_bytes()).hexdigest(),
                'notebook_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            })
    assert len(rows) == 179
    report = {'sections': len(rows), 'code_cells': sum(r['code_cells'] for r in rows),
              'notebooks_with_changed_code': sum(not r['code_preserved'] for r in rows),
              'notebooks_with_preserved_code_and_outputs': sum(r['code_preserved'] and r['outputs_preserved'] for r in rows),
              'rows': rows}
    (HERE / 'revision-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != 'rows'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
