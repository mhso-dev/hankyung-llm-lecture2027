"""Capture changed prose for independent reading without exposing code or outputs."""
import difflib
import hashlib
import json
import re
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = Path(__file__).parent / 'continuity-evidence'


def prose(path: str, raw: bytes) -> str:
    text = raw.decode()
    if path.endswith('.ipynb'):
        text = '\n\n'.join(''.join(c['source']) for c in json.loads(text)['cells'] if c['cell_type'] == 'markdown')
    text = re.sub(r'<(?:script|style|pre)\b[^>]*>.*?</(?:script|style|pre)>', '[보호된 코드]', text, flags=re.S)
    text = re.sub(r'<code\b[^>]*>.*?</code>', '[보호된 인라인 코드]', text, flags=re.S)
    text = re.sub(r'```.*?```', '[보호된 코드]', text, flags=re.S)
    return text


with tarfile.open(EVIDENCE / 'before.tar.gz') as archive:
    entries = {member.name: member for member in archive.getmembers() if member.isfile()}
    records = []
    for name, member in entries.items():
        if not ('/_src/' in name or '/notebooks/' in name or name.endswith('README.md')):
            continue
        path = ROOT / name
        old = archive.extractfile(member).read()
        current = path.read_bytes()
        if old == current:
            continue
        original, revised = prose(name, old), prose(name, current)
        if original == revised:
            continue
        records.append({'path': name, 'sha256': hashlib.sha256(current).hexdigest(),
                        'before_prose': original, 'current_prose': revised,
                        'prose_diff': '\n'.join(difflib.unified_diff(original.splitlines(), revised.splitlines(), fromfile='before', tofile='current', n=2))})
(EVIDENCE / 'changed-prose.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
print(f'{len(records)} changed prose files captured')
