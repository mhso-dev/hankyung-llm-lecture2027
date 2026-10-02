"""Build the Ch2-only student bundle from explicitly selected public files.

전체 마감 2026-10-01: 13절(실습)이 붙어 zip 항목이 17 → 18이 되어, 항목 수를 공개 파일 수 + 2(시작하기·manifest)로 셉니다.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

CHAPTER = Path(__file__).resolve().parents[1]
ROOT = CHAPTER.parents[2]
LAB = ROOT / 'labs/part1/ch02-python'
sys.path.insert(0, str(ROOT / 'textbook/_notebook'))
from render import validate, validate_parts


def main() -> None:
    config = json.loads((CHAPTER / 'chapter.json').read_text())
    files = [LAB / 'notebooks' / f'{s["slug"]}.ipynb' for s in config['sections']]
    for path in files:
        nb = json.loads(path.read_text())
        validate(nb)
        validate_parts(nb)
    files.extend(LAB / name for name in ('README.md', 'pyproject.toml', 'uv.lock'))
    output = ROOT / 'textbook/downloads/ch02-practice.zip'
    manifest = []
    with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        for path in files:
            assert path.is_file() and not path.is_symlink()
            relative = Path('ch02-practice') / path.relative_to(ROOT)
            content = path.read_bytes()
            archive.writestr(relative.as_posix(), content)
            manifest.append({'path': relative.as_posix(), 'sha256': hashlib.sha256(content).hexdigest()})
        archive.writestr('ch02-practice/시작하기.md', (LAB / 'README.md').read_text())
        archive.writestr('ch02-practice/manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2))
    with ZipFile(output) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(files) + 2
        assert archive.read("ch02-practice/시작하기.md") == (LAB / "README.md").read_bytes()
        for row in manifest:
            assert hashlib.sha256(archive.read(row['path'])).hexdigest() == row['sha256']
    print(f'Ch2 bundle: {len(files)} public files, SHA-256 verified')


if __name__ == '__main__':
    main()
