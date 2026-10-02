"""Execute lesson notebooks in fresh Jupyter kernels and retain real outputs.

uv run --project LAB --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip --with python-dotenv==1.2.3 python execute.py NOTEBOOK...
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def code_hash(nb: dict) -> str:
    source = [c['source'] if isinstance(c['source'], str) else ''.join(c['source'])
              for c in nb['cells'] if c['cell_type'] == 'code']
    return hashlib.sha256(json.dumps(source, ensure_ascii=False).encode()).hexdigest()


def output_hash(nb: dict) -> str:
    outputs = json.loads(json.dumps([c.get('outputs', []) for c in nb['cells']
                                    if c['cell_type'] == 'code']))
    for group in outputs:
        for output in group:
            if isinstance(output.get('text'), list):
                output['text'] = ''.join(output['text'])
            for mime, value in output.get('data', {}).items():
                if isinstance(value, list) and mime.startswith('text/'):
                    output['data'][mime] = ''.join(value)
    return hashlib.sha256(json.dumps(outputs, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def secret_values(cwd: Path) -> list[str]:
    from dotenv import dotenv_values

    values = [value for name, value in os.environ.items()
              if any(word in name for word in ('API_KEY', 'SECRET', 'TOKEN')) and len(value) > 10]
    for parent in [cwd, *cwd.parents]:
        env_file = parent / '.env'
        if env_file.is_file():
            values += [value for name, value in dotenv_values(env_file).items()
                       if any(word in name for word in ('API_KEY', 'SECRET', 'TOKEN'))
                       and value and len(value) > 10]
            break
    return values


def redact(value: str, secrets: list[str]) -> str:
    for secret in secrets:
        value = value.replace(secret, '[비밀값]')
    return value.replace(str(Path.home()), '[사용자 폴더]')


def execute(path: Path, cwd: Path, kernel_python: str) -> dict:
    import nbformat
    from jupyter_client.kernelspec import KernelSpecManager
    from jupyter_client.manager import KernelManager
    from nbclient import NotebookClient

    version = subprocess.check_output(
        [kernel_python, '-c', 'import platform; print(platform.python_version())'], text=True
    ).strip()
    if not version.startswith('3.12.'):
        raise ValueError(f'Python 3.12 required; selected kernel uses {version}')
    secrets = secret_values(cwd)
    nb = nbformat.read(path, as_version=4)
    if str(Path.home()) in json.dumps([cell.source for cell in nb.cells]):
        raise ValueError('Personal absolute path in notebook source; use portable setup paths')
    if any(secret in nbformat.writes(nb) for secret in secrets):
        raise ValueError('Credential found in notebook; refusing execution')
    original_hash = code_hash(nb)
    for cell in nb.cells:
        if cell.cell_type == 'code':
            cell.outputs = []
            cell.execution_count = None
    nb.metadata.pop('verification', None)
    with tempfile.TemporaryDirectory(prefix='lesson-kernel-') as folder:
        kernel_dir = Path(folder) / 'python3'
        kernel_dir.mkdir()
        (kernel_dir / 'kernel.json').write_text(json.dumps({
            'argv': [kernel_python, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
            'display_name': 'Python 3.12', 'language': 'python',
        }))
        manager = KernelManager(kernel_name='python3',
            kernel_spec_manager=KernelSpecManager(kernel_dirs=[folder]))
        client = NotebookClient(nb, km=manager, timeout=240, allow_errors=False,
            resources={'metadata': {'path': str(cwd)}})
        try:
            client.execute()
        except Exception as exc:  # noqa: BLE001 — redact external error details before rethrow
            errors = [{'cell': i + 1, 'type': out.get('ename'),
                       'message': redact(out.get('evalue', ''), secrets)}
                      for i, cell in enumerate(nb.cells) for out in cell.get('outputs', [])
                      if out.get('output_type') == 'error']
            path.with_suffix('.failure.json').write_text(json.dumps(
                {'status': 'failed', 'error': type(exc).__name__, 'cells': errors},
                ensure_ascii=False, indent=2))
            print(f'FAIL {path.name}: {type(exc).__name__}; see .failure.json', flush=True)
            raise RuntimeError(f'Notebook execution failed: {path.name}') from None
        finally:
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
    if any(value in nbformat.writes(nb) for value in secrets):
        raise ValueError('Credential found in notebook output; refusing to save')
    for cell in nb.cells:
        if cell.cell_type == 'code':
            cell.outputs = [nbformat.from_dict(json.loads(redact(json.dumps(out), [])))
                            for out in cell.outputs]
    if code_hash(nb) != original_hash:
        raise ValueError('Notebook source changed during execution')
    if nb.metadata.get('language_info', {}).get('version') != version:
        raise ValueError('Kernel reported an unexpected Python version')
    report = {'status': 'passed', 'executed_at': datetime.now(timezone.utc).isoformat(),
              'code_sha256': code_hash(nb), 'outputs_sha256': output_hash(nb),
              'code_cells': sum(c.cell_type == 'code' for c in nb.cells),
              'fresh_kernel': True, 'allow_errors': False, 'python_version': version}
    nb.metadata.verification = report
    nbformat.validate(nb)
    nbformat.write(nb, path)
    path.with_suffix('.failure.json').unlink(missing_ok=True)
    print(f'PASS {path.name}: {report["code_cells"]} cells', flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('notebooks', nargs='+', type=Path)
    parser.add_argument('--cwd', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--kernel-python', default=sys.executable)
    args = parser.parse_args()
    for notebook in args.notebooks:
        execute(notebook.resolve(), args.cwd.resolve(), args.kernel_python)
