"""Check representative offline lessons in an extracted, independent student folder."""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
QA = Path(__file__).resolve().parent


def command(args: list[str], cwd: Path) -> str:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stdout[-2000:] + result.stderr[-2000:])
    return result.stdout[-2000:]


def main() -> None:
    archive = ROOT / 'textbook/downloads/part5-practice.zip'
    records = []
    with tempfile.TemporaryDirectory(prefix='part5-bundle-') as folder:
        with ZipFile(archive) as bundle:
            bundle.extractall(folder)
        extracted = Path(folder) / 'part5-practice'
        for chapter, pattern in (
            ('ch17-agent-overview', '05-*.ipynb'),
            ('ch19-model-tools', '01-*.ipynb'),
            ('ch20-tool-node', '03-*.ipynb'),
        ):
            lab = extracted / 'labs/part5' / chapter
            notebook = next((lab / 'notebooks').glob(pattern))
            original = json.loads(notebook.read_text())['metadata']['verification']['code_sha256']
            command(['uv', 'sync', '--locked'], lab)
            output = command([
                'uv', 'run', '--project', str(lab), '--with', 'nbclient==0.11.0',
                '--with', 'python-dotenv==1.2.3', 'python',
                str(ROOT / 'textbook/_notebook/execute.py'), str(notebook),
                '--cwd', str(lab / 'notebooks'), '--kernel-python', str(lab / '.venv/bin/python'),
            ], lab)
            after = json.loads(notebook.read_text())['metadata']['verification']
            assert after['status'] == 'passed' and after['code_sha256'] == original
            records.append({'notebook': str(notebook.relative_to(extracted)),
                            'code_sha256': original, 'verification': after,
                            'ran_from_notebooks_folder': True, 'output': output.strip()})
        report = {'archive': archive.name,
                  'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
                  'lessons': records,
                  'scope': 'Three representative offline notebooks; no API key copied. Canonical notebooks separately contain full fresh-kernel evidence.'}
        (QA / 'bundle-execution.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
