"""Check lesson structure, prose preservation, and local navigation."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def prose(raw: str) -> str:
    raw = re.sub(r'<pre\b.*?</pre>|<!--.*?-->|\{\{.*?\}\}', '', raw, flags=re.DOTALL)
    return html.unescape(re.sub(r'<[^>]+>', '', raw))


def main() -> None:
    rows = []
    for source in sorted((ROOT / '_src').glob('*.html')):
        raw = source.read_text()
        rendered = (ROOT / source.name).read_text()
        before = (ROOT / 'qa' / 'before' / source.name).read_text()
        errors = []
        count = len(re.findall('[가-힣]', prose(raw)))
        prior_count = len(re.findall('[가-힣]', prose(before)))
        if source.name != 'index.html':
            if re.findall(r'id="(b\d+)"', raw) != [f'b{i}' for i in range(1, 12)]:
                errors.append('11 ordered lesson blocks missing')
            if '<details class="instructor"' not in raw:
                errors.append('instructor notes missing')
            if len(re.findall('class="quiz-q"', raw)) != len(re.findall('class="quiz-q"', before)):
                errors.append('question count changed')
        if count < prior_count * .85:
            errors.append('prose substantially shortened')
        if re.search(r'\{\{(?:svg|img|code|output):', rendered):
            errors.append('unresolved build placeholder')
        ids = set(re.findall(r'id=[\'"]([^\'"]+)', rendered))
        for href in re.findall(r'href=[\'"]([^\'"]+)', rendered):
            link = urlsplit(html.unescape(href))
            if link.scheme or link.netloc:
                continue
            target = ROOT / unquote(link.path) if link.path else ROOT / source.name
            if not target.exists():
                errors.append(f'missing local link: {href}')
            elif link.fragment and not link.path and unquote(link.fragment) not in ids:
                errors.append(f'missing local anchor: {href}')
        rows.append({'page': source.name, 'korean_chars': count,
                     'before_korean_chars': prior_count, 'errors': errors, 'pass': not errors})
    report = {'pages': len(rows), 'passed': sum(r['pass'] for r in rows), 'results': rows}
    (ROOT / 'qa' / 'structure-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if len(rows) == 7 and all(r['pass'] for r in rows) else 1)


if __name__ == '__main__':
    main()
