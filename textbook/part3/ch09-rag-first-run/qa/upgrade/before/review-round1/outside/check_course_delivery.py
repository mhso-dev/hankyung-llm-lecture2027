"""Check published Part 3 links, public archives, and notebook totals."""
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'textbook/_notebook'))
from execute import secret_values


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.quizzes = 0
        self.in_summary = False
        self.summary_questions = 0
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "summary":
            self.in_summary = True
        if tag in ('a', 'img'):
            self.links.append(attrs.get('href' if tag == 'a' else 'src', ''))
        if 'quiz-q' in attrs.get('class', '').split():
            self.quizzes += 1

    def handle_endtag(self, tag):
        if tag == "summary":
            self.in_summary = False
    def handle_data(self, data):
        if self.in_summary and re.match(r"문제 \d+(?:$|\s+·)", data.strip()):
            self.summary_questions += 1

part = ROOT / 'textbook'
chapters = sorted(p for p in part.glob('part*/ch*') if p.is_dir())
pages = [part / 'index.html', *sorted(part.glob('part*/index.html'))]
notebooks = []
for chapter in chapters:
    pages.extend(chapter.glob('*.html'))
    notebooks.extend((ROOT / 'labs' / chapter.parent.name / chapter.name / 'notebooks').glob('*.ipynb'))
secrets = [s.encode() for s in secret_values(ROOT)]
missing = []
exposed = []
links = quizzes = scanned = 0
for page in pages:
    data = page.read_bytes()
    scanned += 1
    if any(secret in data for secret in secrets):
        exposed.append(str(page.relative_to(ROOT)))
    parser = Links()
    parser.feed(data.decode())
    quizzes += max(parser.quizzes, parser.summary_questions)
    for href in parser.links:
        link = urlsplit(href)
        if link.scheme or link.netloc:
            continue
        if not link.path and not link.fragment:
            continue
        links += 1
        target = (page.parent / unquote(link.path)).resolve() if link.path else page
        if not target.is_file():
            missing.append({'page':str(page.relative_to(ROOT)), 'target':href})
        elif link.fragment and target.suffix == '.html':
            target_parser = Links()
            target_parser.feed(target.read_text())
            if unquote(link.fragment) not in target_parser.ids:
                missing.append({'page':str(page.relative_to(ROOT)), 'target':href,
                                'reason':'missing fragment'})
archives = []
for name in ('part1-practice.zip', 'part2-practice.zip', 'part3-practice.zip', 'llm-practice.zip'):
    path = ROOT / 'textbook/downloads' / name
    with ZipFile(path) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert not any(Path(name).name == '.env' for name in names)
        assert not any(name.endswith('-solution.ipynb') for name in names)
        assert not any(name.endswith('labs/data/rag-corpus/queries.jsonl') for name in names)
        assert not any('/.venv/' in name or '/.cache/' in name for name in names)
        prefix = names[0].split('/')[0] + '/'
        manifest = json.loads(archive.read(prefix + 'manifest.json'))
        for entry in manifest:
            actual = hashlib.sha256(archive.read(prefix + entry['path'])).hexdigest()
            assert actual == entry['sha256'], f'Archive hash mismatch: {entry["path"]}'
        for name_in_zip in names:
            scanned += 1
            if any(secret in archive.read(name_in_zip) for secret in secrets):
                exposed.append(f'{name}:{name_in_zip}')
        archives.append({'file':name, 'entries':len(names), 'notebooks':sum(n.endswith('.ipynb') for n in names), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
counts = []
for path in sorted(notebooks):
    nb = json.loads(path.read_text())
    cells = [c for c in nb['cells'] if c['cell_type'] == 'code']
    assert all(c['execution_count'] is not None for c in cells)
    assert not any(o.get('output_type') == 'error' for c in cells for o in c.get('outputs', []))
    counts.append(len(cells))
report = {'html_pages':len(pages), 'local_links':links, 'missing_links':missing,
          'notebooks':len(notebooks), 'code_cells':sum(counts), 'quiz_questions':quizzes,
          'svg_figures':sum(len(list((p/'figures').glob('[0-9]*.svg'))) for p in chapters),
          'excalidraw_sources':sum(len(list((p/'figures').glob('[0-9]*.excalidraw'))) for p in chapters),
          'scanned_public_items':scanned, 'exposed_credentials':exposed, 'archives':archives}

assert len(notebooks) == 87, f'Expected 87 student notebooks; found {len(notebooks)}'
assert quizzes >= 87 * 3, f'Missing review questions: {quizzes}'
(part / 'qa/continuity-evidence/course-delivery-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
assert not missing and not exposed, 'Delivery check failed; see report'
print(json.dumps(report, ensure_ascii=False, indent=2))
