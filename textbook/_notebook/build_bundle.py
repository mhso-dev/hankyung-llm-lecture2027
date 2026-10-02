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
                      'part3/ch10-document-processing', 'part3/ch11-evaluation',
                      'part3/ch12-retrieval-tuning',
                      'part4/ch13-langgraph-basics', 'part4/ch14-rag-patterns',
                      'part4/ch15-evaluation-advanced', 'part4/ch16-guardrails',
                      'part5/ch17-agent-overview', 'part5/ch18-workflow-patterns',
                      'part5/ch19-model-tools', 'part5/ch20-tool-node',
                      'part6/ch21-create-agent', 'part6/ch22-middleware',
                      'part6/ch23-persistence', 'part6/ch24-human-in-the-loop',
                      'part6/ch25-streaming', 'part6/ch26-delegation',
                      'part6/ch27-deepagents', 'part6/ch28-mcp',
                      'part6/ch29-agent-evaluation',
                      'part7/ch30-fastapi-serving', 'part7/ch31-database',
                      'part7/ch32-docker', 'part7/ch33-cicd',
                      'part7/ch34-cost-rate-limits')
FIXTURES = ('sample.docx', 'sample.csv', 'sample.html', 'legacy-signature.hwp',
            'minimal-marker.hwpx')


def check_public_file(root: Path, path: Path) -> None:
    """Require an ordinary file below root, with no symlink directory shortcuts."""
    try:
        relative = path.absolute().relative_to(root.absolute())
    except ValueError as exc:
        raise ValueError(f'Public file is outside the project: {path}') from exc
    if '..' in relative.parts or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Public file resolves outside the project: {path}')
    current = root
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            raise ValueError(f'Public path contains a symbolic link: {path}')
    if not path.is_file():
        raise ValueError(f'Public file is missing: {path}')


def practice_files(root: Path) -> list[Path]:
    # Published HTML source slugs select basic lessons, never exercise/solution files.
    notebooks = [root / 'labs' / chapter / 'notebooks' / f'{source.stem}.ipynb'
                 for chapter in PUBLISHED_CHAPTERS
                 for source in sorted((root / 'textbook' / chapter / '_src').glob('[0-9][0-9]-*.html'))]
    for path in notebooks:
        check_public_file(root, path)
        notebook = json.loads(path.read_text())
        validate(notebook)
        validate_parts(notebook)
    # Public corpus PDFs, source metadata, and fixtures; exclude private answer keys.
    data = sorted((root / 'labs/data/rag-corpus/pdf').glob('*/*.pdf'))
    data.append(root / 'labs/data/rag-corpus/manifest.json')
    # Ch 9 06절 노트북이 정답 쪽을 대조하려고 읽는 질의셋. 정답키 생성기(build/)는 넣지 않는다.
    data.append(root / 'labs/data/rag-corpus/queries.jsonl')
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
    part2_data = [root / 'labs/part2' / chapter / 'runs' / name for chapter, name in (
        ('ch06-langchain-start', 'provider-comparison-continuity.json'),
        ('ch07-prompt-engineering', 'prompt-ab-continuity.json'),
        ('ch08-context-engineering', 'context-design-continuity.json'),
    )]
    if not all(path.is_file() and not path.is_symlink() for path in part2_data):
        raise ValueError('A Part 2 continuity record is missing or a symbolic link')
    part1_setup = [root / 'labs' / chapter / name
                   for chapter in ('part1/ch03-git-github', 'part1/ch04-data-tools',
                                   'part1/ch05-llm-principles')
                   for name in ('pyproject.toml', 'uv.lock', 'README.md')]
    if not all(path.is_file() and not path.is_symlink() for path in part1_setup):
        raise ValueError('A new Part 1 setup file is missing or a symbolic link')
    ch04_data = [root / 'labs/part1/ch04-data-tools' / name for name in (
        'data_tools.py', 'tests/test_data_tools.py', 'data/customers.csv',
        'data/orders.csv', 'data/article.html', 'data/article-text.json', 'data/articles.json',
        'data/robots.txt', 'data/README.md',
    )]
    if not all(path.is_file() and not path.is_symlink() for path in ch04_data):
        raise ValueError('A Ch 4 public data or function file is missing or a symbolic link')
    # §2-7 도구 파일(llm_tools.py 등, 2026-09-21): Part 1·2는 textbook/part{1,2}/public-files.json이 있으면 그 목록을 더한다
    part12_data = []
    for part in ('part1', 'part2'):
        part_manifest = root / 'textbook' / part / 'public-files.json'
        if not part_manifest.is_file():
            continue
        for name in json.loads(part_manifest.read_text()):
            relative = Path(name)
            if relative.is_absolute() or '..' in relative.parts or not name.startswith(f'labs/{part}/'):
                raise ValueError(f'Invalid public {part} path: {name}')
            if any(item.startswith('.') for item in relative.parts) or relative.suffix in ('.env', '.pem', '.key'):
                raise ValueError(f'Private {part} path: {name}')
            part12_data.append(root / relative)
    if not all(path.is_file() and not path.is_symlink() for path in part12_data):
        raise ValueError('A public Part 1·2 file is missing or a symbolic link')
    part3_setup = [root / 'labs' / chapter / name
                   for chapter in PUBLISHED_CHAPTERS if chapter.startswith('part3/')
                   for name in ('pyproject.toml', 'uv.lock', 'README.md')]
    manifest_path = root / 'textbook/part3/public-files.json'
    public_paths = json.loads(manifest_path.read_text())
    part3_data = []
    for name in public_paths:
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or not name.startswith('labs/part3/'):
            raise ValueError(f'Invalid public Part 3 path: {name}')
        if relative.name.startswith('.') or relative.suffix in ('.env', '.pem', '.key'):
            raise ValueError(f'Private Part 3 path: {name}')
        part3_data.append(root / relative)
    if not all(path.is_file() and not path.is_symlink() for path in part3_setup + part3_data):
        raise ValueError('A public Part 3 file is missing or a symbolic link')
    part4_setup = [root / 'labs' / chapter / name
                   for chapter in PUBLISHED_CHAPTERS if chapter.startswith('part4/')
                   for name in ('pyproject.toml', 'uv.lock', 'README.md')]
    part4_data = []
    for name in json.loads((root / 'textbook/part4/public-files.json').read_text()):
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or not name.startswith('labs/part4/'):
            raise ValueError(f'Invalid public Part 4 path: {name}')
        if any(part.startswith('.') for part in relative.parts) or relative.suffix in ('.env', '.pem', '.key'):
            raise ValueError(f'Private Part 4 path: {name}')
        part4_data.append(root / relative)
    if not all(path.is_file() and not path.is_symlink() for path in part4_setup + part4_data):
        raise ValueError('A public Part 4 file is missing or a symbolic link')
    part5_setup = [root / 'labs' / chapter / name
                   for chapter in PUBLISHED_CHAPTERS if chapter.startswith('part5/')
                   for name in ('pyproject.toml', 'uv.lock', 'README.md')]
    part5_data = []
    for name in json.loads((root / 'textbook/part5/public-files.json').read_text()):
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or not name.startswith('labs/part5/'):
            raise ValueError(f'Invalid public Part 5 path: {name}')
        if any(part.startswith('.') for part in relative.parts) or relative.suffix in ('.env', '.pem', '.key'):
            raise ValueError(f'Private Part 5 path: {name}')
        part5_data.append(root / relative)
    if not all(path.is_file() and not path.is_symlink() for path in part5_setup + part5_data):
        raise ValueError('A public Part 5 file is missing or a symbolic link')
    part6_setup = [root / 'labs' / chapter / name
                   for chapter in PUBLISHED_CHAPTERS if chapter.startswith('part6/')
                   for name in ('pyproject.toml', 'uv.lock', 'README.md')]
    part6_data = []
    for name in json.loads((root / 'textbook/part6/public-files.json').read_text()):
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or not name.startswith('labs/part6/'):
            raise ValueError(f'Invalid public Part 6 path: {name}')
        if any(part.startswith('.') for part in relative.parts) or relative.suffix in ('.env', '.pem', '.key'):
            raise ValueError(f'Private Part 6 path: {name}')
        part6_data.append(root / relative)
    if not all(path.is_file() and not path.is_symlink() for path in part6_setup + part6_data):
        raise ValueError('A public Part 6 file is missing or a symbolic link')
    part7_setup = [root / 'labs' / chapter / name
                   for chapter in PUBLISHED_CHAPTERS if chapter.startswith('part7/')
                   for name in ('pyproject.toml', 'uv.lock', 'README.md')]
    part7_data = []
    for name in json.loads((root / 'textbook/part7/public-files.json').read_text()):
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or not name.startswith('labs/part7/'):
            raise ValueError(f'Invalid public Part 7 path: {name}')
        # Actions configuration is public; secret files and other hidden paths are not.
        hidden = [part for part in relative.parts if part.startswith('.')]
        allowed_workflow = (hidden == ['.github'] and '.github/workflows/' in name
                            and relative.suffix in ('.yml', '.yaml'))
        allowed_setup = (len(relative.parts) == 4
                         and relative.name in ('.dockerignore', '.env.example'))
        if (hidden and not (allowed_workflow or allowed_setup)) or relative.suffix in ('.env', '.pem', '.key'):
            raise ValueError(f'Private Part 7 path: {name}')
        part7_data.append(root / relative)
    if not all(path.is_file() and not path.is_symlink() for path in part7_setup + part7_data):
        raise ValueError('A public Part 7 file is missing or a symbolic link')
    files = list(dict.fromkeys(notebooks + data + setup + ch02_setup + part1_setup
                              + ch04_data + part12_data + part2_setup + part2_data + part3_setup + part3_data
                              + part4_setup + part4_data + part5_setup + part5_data
                              + part6_setup + part6_data + part7_setup + part7_data))
    for path in files:
        check_public_file(root, path)
    return files


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
