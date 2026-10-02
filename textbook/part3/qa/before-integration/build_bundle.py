"""Bundle verified notebooks and the public files needed to run them."""
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from render import validate, validate_parts

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'textbook/downloads/llm-practice.zip'
PREFIX = 'llm-practice/'
PUBLISHED_CHAPTERS = ('part1/ch01-development-environment', 'part1/ch02-python',
                      'part1/ch03-git-github', 'part1/ch04-data-tools',
                      'part1/ch05-llm-principles',
                      'part2/ch06-langchain-start', 'part2/ch07-prompt-engineering',
                      'part2/ch08-context-engineering', 'part3/ch09-rag-first-run',
                      'part3/ch10-document-processing')
FIXTURES = ('sample.docx', 'sample.csv', 'sample.html', 'legacy-signature.hwp',
            'minimal-marker.hwpx')


def practice_files(root: Path) -> list[Path]:
    # Published HTML source slugs select basic lessons, never exercise/solution files.
    notebooks = [root / 'labs' / chapter / 'notebooks' / f'{source.stem}.ipynb'
                 for chapter in PUBLISHED_CHAPTERS
                 for source in sorted((root / 'textbook' / chapter / '_src').glob('[0-9][0-9]-*.html'))]
    for path in notebooks:
        notebook = json.loads(path.read_text())
        validate(notebook)
        validate_parts(notebook)
    # Student corpus PDFs and five fixtures only; exclude answer keys and generated intermediates.
    data = sorted((root / 'labs/data/rag-corpus/pdf').glob('*/*.pdf'))
    data += [root / 'labs/part3/ch10-document-processing/fixtures' / name for name in FIXTURES]
    if not all(path.is_file() and not path.is_symlink() for path in data):
        raise ValueError('A student fixture is missing or is a symbolic link')
    setup = [root / 'labs/part1/ch01-development-environment' / name
             for name in ('pyproject.toml', 'uv.lock', 'hello.py', 'README.md')]
    if not all(path.is_file() and not path.is_symlink() for path in setup):
        raise ValueError('Ch 1 setup file is missing or a symbolic link')
    ch02_setup = [root / 'labs/part1/ch02-python' / name
                  for name in ('pyproject.toml', 'uv.lock', 'README.md')]
    if not all(path.is_file() and not path.is_symlink() for path in ch02_setup):
        raise ValueError('Ch 2 setup file is missing or a symbolic link')
    part2_setup = [root / 'labs' / chapter / name
                   for chapter in PUBLISHED_CHAPTERS if chapter.startswith('part2/')
                   for name in ('pyproject.toml', 'uv.lock', 'README.md')]
    if not all(path.is_file() and not path.is_symlink() for path in part2_setup):
        raise ValueError('A Part 2 setup file is missing or a symbolic link')
    part1_setup = [root / 'labs' / chapter / name
                   for chapter in ('part1/ch03-git-github', 'part1/ch04-data-tools',
                                   'part1/ch05-llm-principles')
                   for name in ('pyproject.toml', 'uv.lock', 'README.md')]
    if not all(path.is_file() and not path.is_symlink() for path in part1_setup):
        raise ValueError('A new Part 1 setup file is missing or a symbolic link')
    ch04_data = [root / 'labs/part1/ch04-data-tools' / name for name in (
        'data_tools.py', 'tests/test_data_tools.py', 'data/customers.csv',
        'data/orders.csv', 'data/article.html', 'data/articles.json',
        'data/robots.txt', 'data/README.md',
    )]
    if not all(path.is_file() and not path.is_symlink() for path in ch04_data):
        raise ValueError('A Ch 4 public data or function file is missing or a symbolic link')
    return notebooks + data + setup + ch02_setup + part1_setup + ch04_data + part2_setup


def main() -> None:
    files = practice_files(ROOT)
    OUTPUT.parent.mkdir(exist_ok=True)
    readme = (Path(__file__).parent / 'practice-start.md').read_text()
    manifest = []
    with ZipFile(OUTPUT, 'w', compression=ZIP_DEFLATED) as archive:
        archive.writestr(PREFIX + '시작하기.md', readme)
        archive.writestr(PREFIX + 'env.example',
                         'OPENAI_API_KEY=\nANTHROPIC_API_KEY=\nGOOGLE_API_KEY=\n')
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            content = path.read_bytes()
            archive.writestr(PREFIX + relative, content)
            manifest.append({'path': relative, 'sha256': hashlib.sha256(content).hexdigest()})
        archive.writestr(PREFIX + 'manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2))
    with ZipFile(OUTPUT) as archive:
        assert archive.testzip() is None
        assert not any(Path(name).name == '.env' for name in archive.namelist())
        for entry in manifest:
            assert hashlib.sha256(archive.read(PREFIX + entry['path'])).hexdigest() == entry['sha256']
    print(f'Bundle: {len(files)} files; {OUTPUT.stat().st_size} bytes; hashes verified')


if __name__ == '__main__':
    main()
