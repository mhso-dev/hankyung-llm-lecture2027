"""Freeze verified public artifacts and independent language-review evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
QA = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    accepted = {}
    review18 = json.loads((QA / 'language/ch18-final.json').read_text())
    for entries in review18['hashes'].values():
        for path, value in entries.items():
            accepted[path] = value['final'] if isinstance(value, dict) else value
    review19 = json.loads((QA / 'language/ch19-final.json').read_text())
    for path, value in review19['accepted_source_hashes_sha256'].items():
        target = ('labs/part5/ch19-model-tools/README.md' if path == 'labs/README.md'
                  else 'textbook/part5/ch19-model-tools/' + path)
        accepted[target] = value
    review20 = json.loads((QA / 'language/ch20-final.json').read_text())
    accepted.update(review20['source_sha256'])
    accepted.update(review20['built_sha256'])
    accepted.update({
        'textbook/part5/_src/index.html': '160d152361fffe749fb8954644a5ce4d843e7cfdf978cfa5777b3c8c74eb794a',
        'textbook/part5/practice-start.md': '5ca16b81221be4881ac4afe31d8584919b5321ccca210f4489bfdf566f6c96c3',
        'labs/part5/continuity-guide.md': 'e0ddb44f1bd6747c9089a2381d96fbace204ba84804bcbb553c5414e9588da6a',
    })
    for path, expected in accepted.items():
        assert digest(ROOT / path) == expected, f'Audit hash mismatch: {path}'
    delivery = json.loads((QA / 'delivery-results.json').read_text())
    bundle = json.loads((QA / 'bundle-execution.json').read_text())
    assert bundle['archive_sha256'] == delivery['archives'][0]['sha256']
    paths = set()
    for chapter in sorted((ROOT / 'textbook/part5').glob('ch*')):
        paths.update(chapter.glob('*.html'))
        paths.update(chapter.glob('_src/*.html'))
        paths.update(chapter.glob('figures/*.svg'))
        paths.update(chapter.glob('figures/*.excalidraw'))
        paths.add(chapter / 'chapter.json')
    for lab in (ROOT / 'labs/part5').glob('ch*'):
        paths.update(lab.glob('notebooks/*.ipynb'))
        for name in ('README.md', 'pyproject.toml', 'uv.lock'):
            paths.add(lab / name)
        paths.update(path for path in lab.glob('data/*') if path.is_file())
    for relative in ('textbook/part5/index.html', 'textbook/part5/_src/index.html',
                     'textbook/part5/practice-start.md', 'labs/part5/continuity-guide.md',
                     'textbook/part5/public-files.json', 'textbook/index.html',
                     'textbook/downloads/part5-practice.zip',
                     'textbook/downloads/llm-practice.zip', '.moai/context.md'):
        paths.add(ROOT / relative)
    paths.update(QA.glob('language/*-final.md'))
    paths.update(QA.glob('language/*-final.json'))
    paths.update(QA.glob('*-technical-review.md'))
    paths.update([QA / 'verification.md', QA / 'independent-meaning-review.md'])
    files = [{'path': str(p.relative_to(ROOT)), 'sha256': digest(p)}
             for p in sorted(paths)]
    result = {'date': '2026-09-10', 'files': files,
              'language_hashes_checked': len(accepted),
              'delivery': delivery,
              'representative_extracted_execution_matches_final_archive': True}
    (QA / 'final-manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f'Final manifest: {len(files)} files; {len(accepted)} language hashes matched')


if __name__ == '__main__':
    main()
