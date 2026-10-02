"""Measure lesson scope, declared hours and prose without counting rendered code.

전체 마감 2026-10-01: 챕터 끝 실습 절(규격 §7-2 — 마지막 절 `NN-…-실습`, meta 「실습 30분」)을 지금 구조에 맞게 읽음 —
SECTION_COUNTS는 실습 절을 넣은 절 수, 실습 절은 분 단위 meta와 새 용어 수를 읽고 챕터 시수 합에는 넣지 않음(규격 §7-2 「시수」·「절 시수 합」).
"""
from __future__ import annotations

import json
import re
from html import unescape
from pathlib import Path

PART = Path(__file__).resolve().parents[1]
EXPECTED = {'ch21-create-agent': (6,10), 'ch22-middleware': (8,16),
            'ch23-persistence': (6,10), 'ch24-human-in-the-loop': (3,5),
            'ch25-streaming': (3,5), 'ch26-delegation': (4,4),
            'ch27-deepagents': (8,16), 'ch28-mcp': (5,11),
            'ch29-agent-evaluation': (3,5)}
SECTION_COUNTS = dict(zip(EXPECTED, (7,9,7,4,4,5,9,6,5)))  # 챕터 끝 실습 절 포함(2026-10-01)


def main():
    reports = []
    failures = []
    for slug, expected in EXPECTED.items():
        folder = PART / slug
        config = json.loads((folder / 'chapter.json').read_text())
        if len(config['sections']) != SECTION_COUNTS[slug]:
            failures.append(f'{slug}: expected {SECTION_COUNTS[slug]} sections')
        lessons = []
        for index, item in enumerate(config['sections']):
            path = folder / '_src' / (item['slug'] + '.html')
            source = path.read_text()
            assert '[[작성:' not in source, path
            meta = re.search(r'<!--meta:(.*?)-->', source, re.S)
            assert meta, path
            terms = re.search(r'새 용어\s*(\d+)', meta[1])
            # 챕터 끝 실습 절(마지막 절, 이름 끝 「-실습」)은 「실습 30분」처럼 분으로 적고 챕터 시수에 더하지 않는다(규격 §7-2)
            chapter_practice = index == len(config['sections']) - 1 and item['slug'].endswith('-실습')
            if chapter_practice:
                minutes = re.search(r'실습\s*(\d+)\s*분', meta[1])
                assert minutes and terms, f'Missing scope: {path}'
                lecture = practice = ('0', '0')
            else:
                lecture = re.search(r'강의\s*([\d.]+)h', meta[1])
                practice = re.search(r'실습\s*([\d.]+)h', meta[1])
                assert lecture and practice and terms, f'Missing scope: {path}'
            prose = re.sub(r'<code\b[^>]*>.*?</code>', '', source, flags=re.S)
            prose = re.sub(r'<!--.*?-->|<[^>]+>|\{\{.*?\}\}', '', prose, flags=re.S)
            prose = unescape(prose)
            lessons.append({'slug': item['slug'], 'lecture_hours': float(lecture[1]),
                            'practice_hours': float(practice[1]), 'new_terms': int(terms[1]),
                            'prose_characters': len(re.sub(r'\s+', '', prose)),
                            'hangul_characters': len(re.findall(r'[가-힣]', prose))})
            if chapter_practice:
                lessons[-1].update({'chapter_end_practice': True, 'practice_minutes': int(minutes[1])})
            if int(terms[1]) > 7:
                failures.append(f'{slug}/{item["slug"]}: more than seven new terms')
        hours = (sum(r['lecture_hours'] for r in lessons), sum(r['practice_hours'] for r in lessons))
        if any(abs(a-b) > .015 for a, b in zip(hours, expected)):
            failures.append(f'{slug}: hours {hours} != {expected}')
        reports.append({'chapter': slug, 'lessons': lessons, 'hours': hours,
                        'expected_hours': expected, 'prose_characters': sum(r['prose_characters'] for r in lessons)})
    result = {'chapters': reports, 'failures': failures,
              'prose_note': 'Whitespace, HTML tags, inline code and notebook placeholders excluded; character counts support manual depth review.'}
    (PART / 'qa/lesson-scope.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    assert not failures, failures
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
