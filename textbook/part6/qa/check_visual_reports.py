"""Require a current desktop/mobile report for every published Part 6 page.

전체 마감 2026-10-01: 화면 수 고정값 116(실습 절 전)을 지금 구조에 맞게 고침 — 챕터마다 chapter.json의 절(챕터 끝 실습 절 포함)과
index.html, Part 6 목차·전체 목차가 공개 쪽이고, 그 수의 두 너비(1280·390)만큼 기록이 있어야 한다.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
QA = Path(__file__).resolve().parent


def main() -> None:
    folders = sorted((ROOT / 'textbook/part6').glob('ch*'))
    folders += [ROOT / 'textbook/part6', ROOT / 'textbook']
    records = []
    for folder in folders:
        pages = {path.name: path for path in folder.glob('*.html')}
        report_path = ROOT / 'textbook/_notebook/checks' / folder.name / 'visual-results.json'
        report = json.loads(report_path.read_text())
        expected = {(name, width) for name in pages for width in (1280, 390)}
        actual = {(item['file'], item['width']) for item in report}
        assert actual == expected and len(report) == len(expected), folder
        for item in report:
            path = pages[item['file']]
            assert item['passed'], (folder.name, item)
            assert path.stat().st_mtime <= report_path.stat().st_mtime, f'Stale visual report: {path}'
            records.append({'path': str(path.relative_to(ROOT)), 'width': item['width'],
                            'html_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                            'passed': True})
    published = 2  # textbook/part6/index.html · textbook/index.html
    for config in sorted((ROOT / 'textbook/part6').glob('ch*/chapter.json')):
        published += len(json.loads(config.read_text())['sections']) + 1  # 절 쪽 + 챕터 index.html
    assert len(records) == 2 * published, (len(records), 2 * published)
    (QA / 'visual-results.json').write_text(json.dumps(
        {'screens': len(records), 'all_current_and_passed': True, 'records': records},
        ensure_ascii=False, indent=2))
    print(f'{len(records)} current desktop/mobile checks passed')


if __name__ == '__main__':
    main()
