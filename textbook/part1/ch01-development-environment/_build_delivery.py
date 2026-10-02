"""Package the verified Ch 1 notebooks and portable setup files.

전체 마감 2026-10-01: 실습 절(06)이 붙어 기본 노트북이 6개가 되어, 노트북 수를 chapter.json 절 수에서 읽습니다.
"""
import hashlib
import json
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'textbook' / '_notebook'))
from render import validate, validate_parts

lab = ROOT / 'labs' / 'part1' / HERE.name
notebooks = sorted((lab / 'notebooks').glob('[0-9][0-9]-*.ipynb'))
assert len(notebooks) == len(json.loads((HERE / 'chapter.json').read_text())['sections'])
for path in notebooks:
    notebook = json.loads(path.read_text())
    validate(notebook)
    validate_parts(notebook)
files = notebooks + [lab / name for name in ('README.md', 'pyproject.toml', 'uv.lock', 'hello.py')]
assert all(path.is_file() and not path.is_symlink() for path in files)
output = ROOT / 'textbook' / 'downloads' / 'ch01-practice.zip'
output.parent.mkdir(exist_ok=True)
prefix = 'ch01-practice/'
manifest = []
with ZipFile(output, 'w', compression=ZIP_DEFLATED) as archive:
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        content = path.read_bytes()
        archive.writestr(prefix + relative, content)
        manifest.append({'path': relative, 'sha256': hashlib.sha256(content).hexdigest()})
    archive.writestr(prefix + '시작하기.md', (lab / 'README.md').read_text())
    archive.writestr(prefix + 'manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2))
with ZipFile(output) as archive:
    assert archive.testzip() is None
    assert not any(Path(name).name == '.env' or '/.venv/' in name for name in archive.namelist())
    for entry in manifest:
        assert hashlib.sha256(archive.read(prefix + entry['path'])).hexdigest() == entry['sha256']
print(f'Ch 1 practice bundle: {len(files)} verified files, {output.stat().st_size} bytes')
