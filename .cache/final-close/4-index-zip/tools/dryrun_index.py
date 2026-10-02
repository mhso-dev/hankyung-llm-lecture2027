"""전체 마감 4단계: Part 목차 스크립트를 쓰기 없이 실행해 바뀔 내용을 본다.

파일 쓰기(Path.write_text)는 가로채 메모리에만 두고, zip은 .cache 임시 경로로 돌린다.
사용: python3 dryrun_index.py <tag> [part 번호 ...]   (번호 0 = 전체 목차 build_index.py)
"""
from __future__ import annotations

import difflib
import hashlib
import json
import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[4]
TMP = ROOT / '.cache/final-close/4-index-zip/tmp'
LOG = ROOT / '.cache/final-close/4-index-zip/log'
captured: dict[pathlib.Path, str] = {}
real_write_text = pathlib.Path.write_text


def fake_write_text(self, data, encoding=None, errors=None, newline=None):
    p = self.resolve()
    if p.is_relative_to(TMP):
        return real_write_text(self, data, encoding=encoding)
    captured[p] = data
    return len(data)


def run(n: int, tag: str) -> None:
    captured.clear()
    if n == 0:
        script = ROOT / 'textbook/_notebook/build_index.py'
    else:
        script = ROOT / f'textbook/part{n}/_build_index.py'
    sys.path.insert(0, str(ROOT / 'textbook/_notebook'))
    ns = {'__file__': str(script), '__name__': 'dryrun'}
    pathlib.Path.write_text = fake_write_text
    try:
        code = compile(script.read_text(), str(script), 'exec')
        exec(code, ns)
        if n != 0:
            real_zip = ROOT / f'textbook/downloads/part{n}-practice.zip'
            tmp_zip = TMP / f'dry-{tag}-part{n}-practice.zip'
            RealZip = zipfile.ZipFile

            def zip_wrapper(path, mode='r', *a, **k):
                if pathlib.Path(path).resolve() == real_zip.resolve():
                    path = tmp_zip
                return RealZip(path, mode, *a, **k)
            ns['ZipFile'] = zip_wrapper
            ns['main']()
    finally:
        pathlib.Path.write_text = real_write_text
    report = {'script': str(script.relative_to(ROOT)), 'writes': {}}
    for p, data in captured.items():
        r = str(p.relative_to(ROOT))
        old = p.read_text() if p.exists() else ''
        same = old == data
        entry = {'same': same, 'old_sha256': hashlib.sha256(old.encode()).hexdigest(),
                 'new_sha256': hashlib.sha256(data.encode()).hexdigest()}
        if not same:
            d = list(difflib.unified_diff(old.splitlines(), data.splitlines(), r, r + ' (new)', lineterm='', n=0))
            entry['diff_lines'] = len(d)
            (LOG / f'dry-{tag}-{r.replace("/", "_")}.diff').write_bytes('\n'.join(d).encode())
        report['writes'][r] = entry
    if n != 0:
        tz = TMP / f'dry-{tag}-part{n}-practice.zip'
        with zipfile.ZipFile(real_zip) as a, zipfile.ZipFile(tz) as b:
            an, bn = set(a.namelist()), set(b.namelist())
            changed = sorted(x for x in an & bn if a.read(x) != b.read(x))
            report['zip'] = {'old_entries': len(an), 'new_entries': len(bn),
                             'only_old': sorted(an - bn), 'only_new': sorted(bn - an), 'changed': changed}
    print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    tag = sys.argv[1]
    for n in map(int, sys.argv[2:]):
        run(n, tag)
