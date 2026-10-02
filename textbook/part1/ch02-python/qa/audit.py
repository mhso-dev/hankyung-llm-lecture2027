"""Chapter delivery checks supplementing the shared notebook verifier."""
from __future__ import annotations

import ast
import hashlib
import json
import re
from html import unescape
from pathlib import Path
from xml.etree import ElementTree

CHAPTER = Path(__file__).resolve().parents[1]
ROOT = CHAPTER.parents[2]
LAB = ROOT / 'labs/part1/ch02-python'


def audit() -> list[dict]:
    config = json.loads((CHAPTER / 'chapter.json').read_text())
    assert len(config['sections']) == 12
    records = []
    for section in config['sections']:
        slug = section['slug']
        source = (CHAPTER / '_src' / f'{slug}.html').read_text()
        plain = unescape(re.sub('<[^>]+>', '', source))
        assert '[[작성:' not in source, slug
        titles = re.findall(r'<h2 id="b\d+">(.*?)</h2>', source, re.S)
        titles = [re.sub(r'^\d+', '', re.sub('<[^>]+>', '', title)).strip() for title in titles]
        assert titles == ['학습 목표', '이 내용을 배우는 이유', '앞에서 배운 내용', '핵심 개념', '실행 예제',
                          '일부러 실패해 보기', '주의할 점과 실무 메모', '정리와 다음 절', '복습 문제', '참고 자료'], (slug, titles)
        assert len(plain) >= 2500, (slug, len(plain))
        quizzes = max(len(re.findall(r'class=["\']quiz["\']', source)),
                      len(re.findall(r'class=["\']quiz-q["\']', source)))
        assert quizzes == 4, (slug, quizzes)
        notebook = json.loads((LAB / 'notebooks' / f'{slug}.ipynb').read_text())
        codes = [''.join(c['source']) for c in notebook['cells'] if c['cell_type'] == 'code']
        assert all(any('#' in line and re.search('[가-힣]', line) for line in s.splitlines()) for s in codes), f'{slug}: comment missing'
        for text in codes:
            cleaned = '\n'.join(line for line in text.splitlines() if not line.startswith('%'))
            tree = ast.parse(cleaned)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    assert node.returns is not None, (slug, node.name, 'return hint')
                    for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
                        assert arg.arg in {'self', 'cls'} or arg.annotation is not None, (slug, node.name, arg.arg)
        figures = re.findall(r'\{\{svg:([^}]+)\}\}', source)
        assert figures, slug
        for name in figures:
            ElementTree.parse(CHAPTER / 'figures' / f'{name}.svg')
            diagram = json.loads((CHAPTER / 'figures' / f'{name}.excalidraw').read_text())
            assert diagram['type'] == 'excalidraw'
        page = CHAPTER / f'{slug}.html'
        assert page.is_file(), slug
        records.append({'section': slug, 'prose_characters': len(plain),
                        'quizzes': quizzes,
                        'code_cells': len(codes), 'max_cell_lines': max(len(s.splitlines()) for s in codes),
                        'figures': figures, 'page_sha256': hashlib.sha256(page.read_bytes()).hexdigest()})
    for page in CHAPTER.glob('*.html'):
        for href in re.findall(r'href=["\']([^"\']+)', page.read_text()):
            if href.startswith(('http:', 'https:', 'data:', '#')):
                continue
            assert (page.parent / href.split('#')[0]).exists(), (page.name, href)
    return records


if __name__ == '__main__':
    result = audit()
    (CHAPTER / 'qa/delivery-audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f'PASS {len(result)} lessons, {sum(r["quizzes"] for r in result)} quizzes, {sum(r["code_cells"] for r in result)} cells')
