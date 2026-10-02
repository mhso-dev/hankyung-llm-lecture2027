"""전체 마감 4단계: 학생 묶음 zip 10개를 디스크·공개 목록과 대조(읽기 전용).

사용: python3 zipcheck.py <결과 JSON 경로>
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'textbook/_notebook'))
from build_bundle import practice_files  # noqa: E402

DL = ROOT / 'textbook/downloads'
FORBIDDEN_PARTS = {'__pycache__', '.venv', '.pytest_cache', '.ipynb_checkpoints'}
FORBIDDEN_NAMES = {'.env', '.DS_Store'}
OLD_GENERATOR = re.compile(r'(^|/)(_gen_figures\.py|_make_notebooks\.py|_make_sources\.py|_author[^/]*\.py|author_[^/]*\.py)$')
OLD_CH34_RUNS = {f'labs/part7/ch34-cost-rate-limits/runs/{n}' for n in
                 ('cache-measurement.json', 'batch-input.jsonl', 'routing-comparison.json')}
FIG_SUFFIX = ('.svg', '.png', '.excalidraw', '.mmd', '.jpg', '.jpeg', '.webp')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def chapter_notebooks(part: str, chapter: str) -> list[str]:
    cfg = json.loads((ROOT / 'textbook' / part / chapter / 'chapter.json').read_text())
    return [f'labs/{part}/{chapter}/notebooks/{s["slug"]}.ipynb' for s in cfg['sections']]


def expected_sets() -> dict[str, tuple[str, list[str], dict[str, bytes | None]]]:
    allf = [rel(p) for p in practice_files(ROOT)]
    part3_public = set(json.loads((ROOT / 'textbook/part3/public-files.json').read_text()))
    part3_public.discard('labs/part3/continuity-guide.md')
    pre6 = json.loads((ROOT / 'textbook/part6/prerequisite-files.json').read_text())
    pre7 = json.loads((ROOT / 'textbook/part7/prerequisite-files.json').read_text())
    def gen(*names, start=None):
        d = {n: None for n in names}
        if start is not None:
            d['시작하기.md'] = start
        return d
    ch01 = 'labs/part1/ch01-development-environment'
    ch02 = 'labs/part1/ch02-python'
    sets = {
        'ch01-practice.zip': ('ch01-practice/',
            chapter_notebooks('part1', 'ch01-development-environment')
            + [f'{ch01}/{n}' for n in ('README.md', 'pyproject.toml', 'uv.lock', 'hello.py')],
            gen('manifest.json', start=(ROOT / ch01 / 'README.md').read_bytes())),
        'ch02-practice.zip': ('ch02-practice/',
            chapter_notebooks('part1', 'ch02-python')
            + [f'{ch02}/{n}' for n in ('README.md', 'pyproject.toml', 'uv.lock')],
            gen('manifest.json', start=(ROOT / ch02 / 'README.md').read_bytes())),
        'llm-practice.zip': ('llm-practice/', allf,
            gen('manifest.json', 'env.example', start=(ROOT / 'textbook/_notebook/practice-start.md').read_bytes())),
        'part1-practice.zip': ('part1-practice/', [p for p in allf if p.startswith('labs/part1/')],
            gen('manifest.json', '시작하기.md')),
        'part2-practice.zip': ('part2-practice/', [p for p in allf if p.startswith('labs/part2/')],
            gen('manifest.json', 'env.example', '시작하기.md')),
        'part3-practice.zip': ('part3-practice/', [p for p in allf if p.startswith(('labs/part3/', 'labs/data/'))],
            gen('manifest.json', 'env.example', '시작하기.md')),
        'part4-practice.zip': ('part4-practice/', [p for p in allf if p.startswith(('labs/part4/', 'labs/data/')) or p in part3_public],
            gen('manifest.json', 'env.example', start=(ROOT / 'textbook/part4/practice-start.md').read_bytes())),
        'part5-practice.zip': ('part5-practice/', [p for p in allf if p.startswith(('labs/part5/', 'labs/part1/ch04-data-tools/'))],
            gen('manifest.json', 'env.example', start=(ROOT / 'textbook/part5/practice-start.md').read_bytes())),
        'part6-practice.zip': ('part6-practice/', list(dict.fromkeys([p for p in allf if p.startswith('labs/part6/')] + pre6)),
            gen('manifest.json', 'env.example', start=(ROOT / 'textbook/part6/practice-start.md').read_bytes())),
        'part7-practice.zip': ('part7-practice/', list(dict.fromkeys([p for p in allf if p.startswith('labs/part7/')] + pre7)),
            gen('manifest.json', 'env.example', start=(ROOT / 'textbook/part7/practice-start.md').read_bytes())),
    }
    return sets


def check(name: str, prefix: str, expected: list[str], generated: dict[str, bytes | None]) -> dict:
    path = DL / name
    data = path.read_bytes()
    out = {'zip': name, 'sha256': sha(data), 'bytes': len(data),
           'mtime_utc': __import__('datetime').datetime.utcfromtimestamp(path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if not n.endswith('/')]
        out['entries'] = len(names)
        out['testzip_ok'] = z.testzip() is None
        bad_prefix = [n for n in names if not n.startswith(prefix)]
        inner = {n[len(prefix):]: n for n in names if n.startswith(prefix)}
        same, diff, disk_missing, extra = [], [], [], []
        exp = set(expected)
        for r, full in inner.items():
            if r in generated:
                continue
            disk = ROOT / r
            if not disk.is_file():
                disk_missing.append(r)
            elif sha(z.read(full)) == sha(disk.read_bytes()):
                same.append(r)
            else:
                diff.append(r)
            if r not in exp:
                extra.append(r)
        missing = sorted(exp - set(inner))
        gen_report = {}
        for g, want in generated.items():
            if g not in inner:
                gen_report[g] = 'absent'
            elif want is None:
                gen_report[g] = 'present'
            else:
                gen_report[g] = 'same' if z.read(inner[g]) == want else 'DIFF'
        manifest_ok = None
        if 'manifest.json' in inner:
            man = json.loads(z.read(inner['manifest.json']))
            def key(e):
                p = e['path']
                return p[len(prefix):] if p.startswith(prefix) else p
            mpaths = {key(e): e['sha256'] for e in man}
            manifest_ok = (set(mpaths) == set(r for r in inner if r not in generated)
                           and all(sha(z.read(inner[p])) == h for p, h in mpaths.items() if p in inner))
            out['manifest_rows'] = len(man)
        forb = [r for r in inner if (set(Path(r).parts) & FORBIDDEN_PARTS) or Path(r).name in FORBIDDEN_NAMES
                or r.endswith('.pyc')]
        oldgen = [r for r in inner if OLD_GENERATOR.search(r) or '/before/' in r or '/blocked/' in r]
        oldruns = [r for r in inner if r in OLD_CH34_RUNS]
        figs = [r for r in inner if r.lower().endswith(FIG_SUFFIX)]
    nb = [r for r in inner if r.endswith('.ipynb')]
    out.update({
        'bad_prefix': bad_prefix, 'same': len(same), 'diff': diff, 'disk_missing': disk_missing,
        'extra_vs_public': extra, 'missing_vs_public': missing, 'generated': gen_report,
        'manifest_ok': manifest_ok, 'forbidden': forb, 'old_generators': oldgen, 'old_ch34_runs': oldruns,
        'figure_files': figs, 'notebooks': len(nb),
        'notebooks_diff': len([r for r in diff if r.endswith('.ipynb')]),
        'expected_files': len(expected),
    })
    return out


def main() -> None:
    results = [check(n, *spec) for n, spec in expected_sets().items()]
    Path(sys.argv[1]).write_text(json.dumps(results, ensure_ascii=False, indent=2))
    for r in results:
        print(f"{r['zip']:20} {r['sha256'][:12]} ent={r['entries']:4} nb={r['notebooks']:3} same={r['same']:4} "
              f"diff={len(r['diff']):3} (nb {r['notebooks_diff']}) diskmiss={len(r['disk_missing'])} "
              f"missing={len(r['missing_vs_public'])} extra={len(r['extra_vs_public'])} gen={r['generated']} "
              f"man={r['manifest_ok']} forb={len(r['forbidden'])} oldgen={len(r['old_generators'])} "
              f"ch34runs={len(r['old_ch34_runs'])} figs={len(r['figure_files'])} {r['mtime_utc']}")


if __name__ == '__main__':
    main()
