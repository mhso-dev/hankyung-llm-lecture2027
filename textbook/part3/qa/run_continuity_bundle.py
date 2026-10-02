"""Execute the student handoff path from an extracted ZIP in fresh kernels."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = Path(__file__).parent / 'continuity-evidence'
LESSONS = (
    ('ch09-rag-first-run', '06-실험-하네스.ipynb'),
    ('ch10-document-processing', '08-인덱싱-비교-실험.ipynb'),
    ('ch11-evaluation', '06-실험-로그와-자동-실행.ipynb'),
)


def main() -> None:
    from dotenv import dotenv_values

    reuse_upstream = '--reuse-upstream' in sys.argv
    previous = json.loads((EVIDENCE / 'bundle-execution-results.json').read_text()) if reuse_upstream else None
    archive_path = ROOT / 'textbook/downloads/part3-practice.zip'
    work = Path(tempfile.mkdtemp(prefix='hankyung-continuity-'))
    with ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            assert not Path(name).is_absolute() and '..' not in Path(name).parts
        archive.extractall(work)
    extracted = work / 'part3-practice'
    # Keep credentials in the subprocess environment, never in evidence or ZIP.
    environment = os.environ.copy()
    for key, value in dotenv_values(ROOT / '.env').items():
        if key.endswith('API_KEY') and value:
            environment[key] = value
    assert environment.get('OPENAI_API_KEY'), 'OPENAI_API_KEY is required for the actual API path'
    (extracted / '.env').write_text('# Verification credentials are supplied through the process environment.\n')
    output = EVIDENCE / 'bundle-execution'
    output.mkdir(exist_ok=True)
    reports = previous['notebooks'][:2] if previous else []
    lessons = LESSONS
    if previous:
        old_manifest = {row['path']: row['sha256'] for row in json.loads((Path(previous['temporary_extraction']) / 'manifest.json').read_text())}
        new_manifest = json.loads((extracted / 'manifest.json').read_text())
        for row in new_manifest:
            if row['path'].startswith(('labs/part3/ch09-rag-first-run/', 'labs/part3/ch10-document-processing/', 'labs/data/')):
                assert old_manifest.get(row['path']) == row['sha256'], 'Upstream execution inputs changed'
        for chapter, _ in LESSONS[:2]:
            shutil.copytree(output / chapter / 'runs', extracted / 'labs/part3' / chapter / 'runs', dirs_exist_ok=True)
        (EVIDENCE / 'bundle-execution-before-evaluator-refresh.json').write_text(json.dumps(previous, ensure_ascii=False, indent=2))
        lessons = LESSONS[2:]
    try:
        for chapter, lesson in lessons:
            lab = extracted / 'labs/part3' / chapter
            notebook = lab / 'notebooks' / lesson
            command = ['uv', 'run', '--project', str(lab), '--python', '3.12',
                       '--with', 'nbclient==0.11.0', '--with', 'ipykernel==7.3.0',
                       '--with', 'pip', '--with', 'python-dotenv==1.2.3',
                       'python', str(ROOT / 'textbook/_notebook/execute.py'), str(notebook),
                       '--cwd', str(notebook.parent)]
            result = subprocess.run(command, env=environment, text=True, capture_output=True)
            text = result.stdout + result.stderr
            for key, value in environment.items():
                if any(part in key for part in ('API_KEY', 'TOKEN', 'SECRET')) and len(value) > 10:
                    text = text.replace(value, '[비밀값]')
            text = text.replace(str(Path.home()), '[사용자 폴더]')
            (output / f'{chapter}.txt').write_text(text)
            assert result.returncode == 0, f'{chapter} execution failed; see redacted log'
            nb = json.loads(notebook.read_text())
            reports.append({'notebook': f'labs/part3/{chapter}/notebooks/{lesson}',
                            'working_directory': 'extracted notebook directory',
                            'verification': nb['metadata']['verification']})
            shutil.copy2(notebook, output / f'{chapter}-{lesson}')
            for source in (lab / 'runs').rglob('*'):
                if source.is_file() and 'continuity' in str(source.relative_to(lab / 'runs')):
                    target = output / chapter / source.relative_to(lab)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)
            print(f'ZIP fresh kernel passed: {chapter}', flush=True)
    finally:
        (extracted / '.env').unlink(missing_ok=True)
    report = {'archive_sha256': hashlib.sha256(archive_path.read_bytes()).hexdigest(),
              'source': 'part3-practice.zip', 'data_or_student_module_fallback': False,
              'verification_runner': 'textbook/_notebook/execute.py (outside ZIP, verification only)',
              'notebooks': reports, 'temporary_extraction': str(extracted),
              'credentials_written': False,
              'reused_verified_upstream_runs': bool(previous),
              'upstream_execution_inputs_unchanged': bool(previous)}
    (EVIDENCE / 'bundle-execution-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print('Extracted ZIP handoff path completed', flush=True)


if __name__ == '__main__':
    main()
