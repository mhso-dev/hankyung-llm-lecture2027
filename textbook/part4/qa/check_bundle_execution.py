"""Run representative offline lessons from an extracted practice archive."""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
QA = Path(__file__).resolve().parent


def command(args, cwd):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stdout[-2000:] + result.stderr[-2000:])
    return result.stdout[-2000:]


def main():
    archive = ROOT / 'textbook/downloads/part4-practice.zip'
    records = []
    with tempfile.TemporaryDirectory(prefix='part4-bundle-') as folder:
        with ZipFile(archive) as bundle:
            bundle.extractall(folder)
        extracted = Path(folder) / 'part4-practice'
        for chapter, pattern in (
            ('ch13-langgraph-basics', '05-*.ipynb'),
            ('ch15-evaluation-advanced', '08-*.ipynb'),
        ):
            lab = extracted / 'labs/part4' / chapter
            notebook = next((lab / 'notebooks').glob(pattern))
            before = json.loads(notebook.read_text())['metadata']['verification']['code_sha256']
            command(['uv', 'sync', '--locked'], lab)
            output = command([
                'uv', 'run', '--project', str(lab), '--with', 'nbclient==0.11.0',
                '--with', 'python-dotenv==1.2.3', 'python',
                str(ROOT / 'textbook/_notebook/execute.py'), str(notebook),
                '--cwd', str(lab / 'notebooks'), '--kernel-python', str(lab / '.venv/bin/python'),
            ], lab)
            after = json.loads(notebook.read_text())['metadata']['verification']
            assert after['status'] == 'passed' and after['code_sha256'] == before
            records.append({'notebook': str(notebook.relative_to(extracted)),
                            'code_sha256': before, 'verification': after,
                            'ran_from_notebooks_folder': True, 'output': output.strip()})
        lab = extracted / 'labs/part4/ch16-guardrails'
        command(['uv', 'sync', '--locked'], lab)
        tests = command(['uv', 'run', 'python', '-m', 'pytest', '-q'], lab)
        module = ROOT / 'labs/part4/ch16-guardrails/notebooks/guardrails.py'
        report = {'archive': archive.name,
                  'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
                  'lessons': records, 'guardrails_tests': tests.strip(),
                  'guardrails_sha256': hashlib.sha256(module.read_bytes()).hexdigest(),
                  'scope': 'Two offline notebooks and the reusable module tests in a clean extraction; no API key copied.'}
        (QA / 'bundle-execution.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
