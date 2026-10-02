"""Check published Part 6 pages, notebooks, archives, and public-data boundaries.

전체 마감 2026-10-01(4단계): 묶음 경계 규칙을 지금 구조에 맞게 고침 — `labs/data/rag-corpus/queries.jsonl`은
2026-09-17(Ch 9 마감)부터 공개 파일이라 `llm-practice.zip`에 들어 있음(Part 3·4 `check_delivery.py`와 같은 규칙).
"""
from __future__ import annotations

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
from execute import secret_values  # noqa: E402 — shared notebook tooling lives beside the chapters.
from verify import verify_lesson  # noqa: E402 — shared notebook tooling lives beside the chapters.


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.questions = 0
        self.quiz_blocks = 0
        self.answers = 0
        self.summary_questions = 0
        self.in_summary = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag in ('a', 'img'):
            self.links.append(attrs.get('href' if tag == 'a' else 'src', ''))
        if tag == 'summary':
            self.in_summary = True
        if 'quiz-q' in (attrs.get('class') or '').split():
            self.questions += 1
        if tag == 'details' and 'quiz' in (attrs.get('class') or '').split():
            self.quiz_blocks += 1
        if 'quiz-a' in (attrs.get('class') or '').split():
            self.answers += 1

    def handle_endtag(self, tag):
        if tag == 'summary':
            self.in_summary = False

    def handle_data(self, data):
        if self.in_summary and re.match(r'문제\s*\d+', data.strip()):
            self.summary_questions += 1


def read_page(path):
    page = Page()
    page.feed(path.read_text())
    return page


def main():
    part = ROOT / 'textbook/part6'
    chapters = sorted(part.glob('ch*/chapter.json'))
    assert len(chapters) == 9
    pages = [part / 'index.html', ROOT / 'textbook/index.html']
    lessons, lesson_pages = [], set()
    for config_path in chapters:
        config = json.loads(config_path.read_text())
        chapter = config_path.parent
        pages.append(chapter / 'index.html')
        for lesson in config['sections']:
            page = chapter / (lesson['slug'] + '.html')
            notebook = ROOT / config['lab_path'] / 'notebooks' / (lesson['slug'] + '.ipynb')
            lessons.append(verify_lesson(notebook, page))
            pages.append(page)
            lesson_pages.add(page)
    secrets = [value.encode() for value in secret_values(ROOT)]
    missing, exposed, quiz_errors, personal_paths = [], [], [], []
    links = questions = 0
    for path in pages:
        data = path.read_bytes()
        if any(secret in data for secret in secrets):
            exposed.append(str(path.relative_to(ROOT)))
        if b'/Users/mhso/' in data or b'/var/folders/' in data:
            personal_paths.append(str(path.relative_to(ROOT)))
        page = read_page(path)
        count = max(page.questions, page.summary_questions, page.quiz_blocks)
        if path in lesson_pages:
            questions += count
            if not 3 <= count <= 5 or page.answers != count:
                quiz_errors.append({'file': path.name, 'questions': count, 'answers': page.answers})
            if not all(f'b{i}' in page.ids for i in range(1, 11)):
                missing.append({'page': path.name, 'reason': 'missing fixed section'})
        for href in page.links:
            link = urlsplit(href)
            if link.scheme or link.netloc or not (link.path or link.fragment):
                continue
            links += 1
            target = (path.parent / unquote(link.path)).resolve() if link.path else path
            invalid = not target.is_file()
            if not invalid and link.fragment and target.suffix == '.html':
                invalid = unquote(link.fragment) not in read_page(target).ids
            if invalid:
                missing.append({'page': str(path.relative_to(ROOT)), 'target': href})
    archives = []
    for name in ('part6-practice.zip', 'llm-practice.zip'):
        path = ROOT / 'textbook/downloads' / name
        with ZipFile(path) as archive:
            assert archive.testzip() is None
            names = archive.namelist()
            prefix = names[0].split('/')[0] + '/'
            assert not any(Path(n).name == '.env' or '/.venv/' in n or '/.cache/' in n for n in names)
            # 전체 마감 2026-10-01(4단계): queries.jsonl은 Ch 9 06절·harness.py가 읽어 2026-09-17부터 묶음에 넣는다
            # (Ch 9 마감 — Part 3·4 검사와 같은 규칙). 정답키 생성기(build/)·queries.csv·풀이 노트북은 그대로 막는다.
            assert not any(n.endswith('-solution.ipynb') or '/rag-corpus/build/' in n
                           or n.endswith('/rag-corpus/queries.csv') for n in names)
            manifest = json.loads(archive.read(prefix + 'manifest.json'))
            for entry in manifest:
                content = archive.read(prefix + entry['path'])
                assert hashlib.sha256(content).hexdigest() == entry['sha256']
                assert content == (ROOT / entry['path']).read_bytes(), f'Stale file: {entry["path"]}'
            for item in names:
                if any(secret in archive.read(item) for secret in secrets):
                    exposed.append(f'{name}:{item}')
            archives.append({'file': name, 'entries': len(names),
                             'part6_notebooks': sum('/labs/part6/' in n and n.endswith('.ipynb') for n in names),
                             'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    report = {'html_pages': len(pages), 'local_links': links, 'missing_links': missing,
              'lessons': len(lessons), 'code_cells': sum(r['code_cells'] for r in lessons),
              'max_cell_lines': max(r['max_cell_lines'] for r in lessons),
              'quiz_questions': questions, 'quiz_errors': quiz_errors,
              'svg_figures': len(list(part.glob('ch*/figures/[0-9]*.svg'))),
              'excalidraw_sources': len(list(part.glob('ch*/figures/[0-9]*.excalidraw'))),
              'exposed_credentials': exposed, 'personal_paths': personal_paths,
              'archives': archives}
    (part / 'qa/delivery-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    assert not missing and not exposed and not quiz_errors and not personal_paths, (
        'Delivery check failed; see report')
    assert all(item['part6_notebooks'] == len(lessons) for item in archives)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
