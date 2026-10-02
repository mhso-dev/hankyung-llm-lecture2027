"""Check the delivered HTML against every executed lesson notebook."""
import argparse
import ast
import base64
import json
import re
from html.parser import HTMLParser
from pathlib import Path

from render import lesson_part, text, validate, validate_parts

ROOT = Path(__file__).resolve().parents[2]


def _chapter_dirs(root: Path, chapter: Path | None) -> list[Path]:
    root = root.resolve()
    if chapter is not None:
        selected = chapter if chapter.is_absolute() else root / chapter
        selected = selected.resolve()
        textbook = (root / 'textbook').resolve()
        assert selected.parent.parent == textbook, (
            f'Chapter must be a textbook/part*/ch* directory: {selected}')
        assert selected.parent.name.startswith('part') and selected.name.startswith('ch'), (
            f'Chapter must use part*/ch* names: {selected}')
        assert selected.is_dir(), f'Chapter directory does not exist: {selected}'
        return [selected]
    return sorted(path for path in (root / 'textbook').glob('part*/ch*')
                  if (path / '_src').is_dir())


def discover_lessons(root: Path = ROOT,
                     chapter: Path | None = None) -> list[tuple[Path, Path]]:
    """Return canonical (notebook, built HTML) pairs declared by lesson sources."""
    root = root.resolve()
    chapters = _chapter_dirs(root, chapter)
    assert chapters, f'No textbook chapters with _src directories under: {root}'
    lessons = []
    for chapter_dir in chapters:
        sources = sorted((chapter_dir / '_src').glob('[0-9][0-9]-*.html'))
        assert sources, f'No lesson sources in: {chapter_dir / "_src"}'
        numbers = {}
        for source in sources:
            number = source.stem[:2]
            assert number not in numbers, (
                f'Duplicate lesson number {number}: {numbers.get(number)} and {source}')
            numbers[number] = source
            relative = chapter_dir.relative_to(root / 'textbook')
            notebook = root / 'labs' / relative / 'notebooks' / f'{source.stem}.ipynb'
            page = chapter_dir / f'{source.stem}.html'
            assert notebook.is_file(), f'Missing notebook for {source}: {notebook}'
            assert page.is_file(), f'Missing built HTML for {source}: {page}'
            lessons.append((notebook, page))
    return lessons


def report_path(root: Path = ROOT, chapter: Path | None = None) -> Path:
    root = root.resolve()
    checks = root / 'textbook' / '_notebook' / 'checks'
    if chapter is None:
        return checks / 'notebook-contracts.json'
    selected = chapter if chapter.is_absolute() else root / chapter
    selected = selected.resolve()
    return checks / f'notebook-contracts-{selected.parent.name}-{selected.name}.json'


class Cells(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []
        self.active = False
        self.download = None
        self.foreign_python = 0
        self.outputs = []
        self.in_output = False

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag == 'pre' and 'nb-output' in (attr.get('class') or ''):
            self.outputs.append('')
            self.in_output = True
        if tag == 'code' and 'nb-source' in (attr.get('class') or ''):
            self.sources.append('')
            self.active = True
        elif tag == 'code' and 'language-python' in (attr.get('class') or ''):
            self.foreign_python += 1
        if tag == 'a' and (attr.get('download') or '').endswith('.ipynb'):
            href = attr.get('href')
            assert href, 'Notebook download must have a target'
            self.download = json.loads(base64.b64decode(href.split(',', 1)[1]))

    def handle_endtag(self, tag):
        if tag == 'code':
            self.active = False
        if tag == 'pre':
            self.in_output = False

    def handle_data(self, data):
        if self.active:
            self.sources[-1] += data
        if self.in_output:
            self.outputs[-1] += data



def check_imports(tree: ast.AST, path: Path) -> None:
    forbidden = {'openai', 'rag', 'context_lab', 'document_processing',
                 'experiment', 'harness', 'prompts'}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            modules = [node.module or '']
        else:
            continue
        for module in modules:
            assert module.split('.')[0] not in forbidden, (
                f'Use LangChain directly; no SDK or project helper import: {module} in {path}')


def check_failure_section(nb: dict, html: str, page: Path) -> None:
    failure = re.search(r'<h2 id="b6".*?</h2>(.*?)(?=<h2 id="b7")', html, re.DOTALL)
    assert failure, f'Missing failure section: {page}'
    failure_parser = Cells()
    failure_parser.feed(failure[1])
    lesson_format = nb.get('metadata', {}).get('lesson_format', 'paired')
    if lesson_format == 'experiment':
        assert not failure_parser.sources, f'Experiment result interpretation must have no code: {page}'
        assert 'data-lesson-stage=' not in failure[1], (
            f'Experiment result interpretation must have no Before/After stage: {page}')
        return
    failure_sources = [text(c['source']) for c in nb['cells']
                       if c['cell_type'] == 'code' and lesson_part(c) in {'before', 'after'}]
    assert failure_parser.sources == failure_sources, f'Failure code must appear in b6: {page}'
    for stage in ('before', 'after'):
        assert failure[1].count(f'data-lesson-stage="{stage}"') == 1, page


def verify_lesson(path: Path, page: Path, root: Path = ROOT) -> dict:
    nb = json.loads(path.read_text())
    validate(nb)
    validate_parts(nb)
    lesson_format = nb.get('metadata', {}).get('lesson_format', 'paired')
    html = page.read_text()
    assert '강사 노트' not in html and 'class="instructor"' not in html, (
        f'Student textbook must not include instructor notes: {page}')
    assert re.findall(r'<h2 id="b(\d+)"', html) == [str(i) for i in range(1, 11)], (
        f'Student textbook requires 10 ordered sections: {page}')
    assert '{{notebook:' not in html, f'Unexpanded notebook: {page}'
    parser = Cells()
    parser.feed(html)
    sources = [text(c['source']) for c in nb['cells'] if c['cell_type'] == 'code']
    assert parser.sources == sources, f'HTML/source mismatch: {page}'
    assert parser.foreign_python == 0, f'Unverified Python block outside notebook: {page}'
    assert parser.download == nb, f'Notebook download differs from source: {page}'
    outputs = [text(o.get('text', '') if o['output_type'] == 'stream'
                    else o.get('data', {}).get('text/plain', ''))
               for cell in nb['cells'] for o in cell.get('outputs', [])]
    assert parser.outputs == outputs, f'HTML/output mismatch: {page}'
    check_failure_section(nb, html, page)
    for source in sources:
        assert '__file__' not in source and 'sys.path' not in source, path
        assert not re.search(r'\bTODO\b', source), f'Incomplete exercise: {path}'
        python = '\n'.join(line for line in source.splitlines() if not line.startswith('%'))
        check_imports(ast.parse(python), path)
    lengths = [len(source.splitlines()) for source in sources]
    assert lengths, f'Lesson notebook has no code cells: {path}'
    assert max(lengths) <= 25, f'Long cell needs no more than 25 lines: {path}'
    return {'notebook': str(path.relative_to(root)), 'html': str(page.relative_to(root)),
            'code_cells': len(sources), 'code_lines': sum(lengths),
            'max_cell_lines': max(lengths), 'verification': nb['metadata']['verification'],
            'python_version': nb['metadata']['language_info']['version'],
            'lesson_format': lesson_format,
            'html_matches': True, 'download_matches': True, 'outputs_match': True,
            'failure_section_matches': True,
            'before_cells': sum(c['cell_type'] == 'code' and lesson_part(c) == 'before'
                                for c in nb['cells']),
            'after_cells': sum(c['cell_type'] == 'code' and lesson_part(c) == 'after'
                               for c in nb['cells'])}


def main(argv: list[str] | None = None, root: Path = ROOT) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chapter', type=Path,
                        help='Verify one textbook/part*/ch* directory')
    args = parser.parse_args(argv)
    reports = [verify_lesson(path, page, root)
               for path, page in discover_lessons(root, args.chapter)]
    output = report_path(root, args.chapter)
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(reports, ensure_ascii=False, indent=2))
    print(f'PASS {len(reports)} sections / '
          f'{sum(report["code_cells"] for report in reports)} code cells '
          f'(max {max(report["max_cell_lines"] for report in reports)} lines)')


if __name__ == '__main__':
    main()
