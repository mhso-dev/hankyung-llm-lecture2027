"""Check published Part 2 links, public archives, and notebook totals.

전체 마감 2026-10-01: 노트북·코드 셀 고정값(20개·180셀 — 품질 개선 전)을 지금 구조에 맞게 고침 —
노트북 23개(20 + 챕터 끝 실습 절 3)·코드 셀 470개(2026-10-01에 센 값, 각 노트북 verification.code_cells 합과 같음).
"""
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'textbook/_notebook'))
from execute import secret_values


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.quizzes = 0
        self.in_summary = False
        self.summary_questions = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
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

part = ROOT / 'textbook/part2'
chapters = sorted(p for p in part.glob('ch*') if p.is_dir())
pages = [part / 'index.html', ROOT / 'textbook/index.html']
notebooks = []
for chapter in chapters:
    pages.extend(chapter.glob('*.html'))
    notebooks.extend((ROOT / 'labs/part2' / chapter.name / 'notebooks').glob('*.ipynb'))
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
        if link.scheme or link.netloc or not link.path:
            continue
        links += 1
        if not (page.parent / unquote(link.path)).resolve().exists():
            missing.append({'page':str(page.relative_to(ROOT)), 'target':href})
archives = []
for name in ('part2-practice.zip', 'llm-practice.zip'):
    path = ROOT / 'textbook/downloads' / name
    with ZipFile(path) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert not any(Path(name).name == '.env' for name in names)
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
assert not missing and not exposed, 'Delivery check failed; see report'
assert len(notebooks) == 23 and sum(counts) == 470
(part / 'qa/delivery-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
print(json.dumps(report, ensure_ascii=False, indent=2))
