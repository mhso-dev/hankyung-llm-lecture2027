"""Verify that reviewed student files still match the final audit manifests."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
QA = Path(__file__).resolve().parent


def main():
    records = []
    for chapter in range(13, 17):
        report = QA / 'language' / f'ch{chapter}-final-audit-2026-09-10.md'
        text = report.read_text()
        assert '최종 판정: `accept`' in text, report
        snapshots = set(re.findall(r'snapshots/[^`\s]+\.txt', text))
        assert len(snapshots) >= 3, report
        checked = 0
        for name in sorted(snapshots):
            path = QA / 'language' / name
            manifest = json.loads(path.with_suffix('.manifest.json').read_text())
            assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest['sha256'], path
            items = manifest.get('items', manifest.get('files'))
            assert isinstance(items, list), path
            for item in items:
                source = ROOT / item['path']
                assert hashlib.sha256(source.read_bytes()).hexdigest() == item['source_sha256'], source
                checked += 1
        records.append({'chapter': chapter, 'accept': True, 'reviewed_files_unchanged': checked})
    (QA / 'language-freeze.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
    print(json.dumps(records, ensure_ascii=False))


if __name__ == '__main__':
    main()
