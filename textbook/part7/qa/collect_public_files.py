"""Collect explicit chapter manifests; never discover arbitrary files for publication."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PART = ROOT / 'textbook/part7'


def main() -> None:
    chapters = sorted(PART.glob('ch*/chapter.json'))
    assert len(chapters) == 5, 'All five chapters must be present'
    public = {'labs/part7/continuity-guide.md'}
    prerequisites = set()
    for config in chapters:
        manifest = config.parent / 'qa/public-files.json'
        names = json.loads(manifest.read_text())
        assert isinstance(names, list), manifest
        for name in names:
            path = Path(name)
            assert not path.is_absolute() and '..' not in path.parts, name
            # Chapter delivery inventories may also name built reading pages.
            # The practice ZIP includes only the explicitly listed lab files.
            if name.startswith(f'textbook/part7/{config.parent.name}/'):
                assert (ROOT / path).is_file(), name
                continue
            assert name.startswith('labs/part7/'), name
            assert (ROOT / path).is_file(), name
            public.add(name)
        prerequisite = config.parent / 'qa/prerequisite-files.json'
        if prerequisite.exists():
            names = json.loads(prerequisite.read_text())
            assert isinstance(names, list), prerequisite
            prerequisites.update(name for name in names if name.startswith('labs/'))
    for filename, names in (('public-files.json', public),
                            ('prerequisite-files.json', prerequisites)):
        (PART / filename).write_text(json.dumps(sorted(names), ensure_ascii=False, indent=2) + '\n')
    print(f'Explicit public files: {len(public)}; prerequisites: {len(prerequisites)}')


if __name__ == '__main__':
    main()
