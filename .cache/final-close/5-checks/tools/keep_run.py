"""5단계 실행 감싸개 — 검사 스크립트를 고치지 않고 그대로 돌리되, 파일을 지우지 않게 한다.

- tempfile.TemporaryDirectory → 지우지 않는 폴더(FC5_WORK 아래 mkdtemp), 끝나도 그대로 둠
- tempfile.mkdtemp 기본 위치 → FC5_WORK
- pathlib.Path.unlink → FC5_WORK 아래 경로면 지우지 않고 기록만(FC5_WORK/unlink-skipped.txt)
쓰는 법: FC5_WORK=<폴더> python3 keep_run.py <스크립트> [인자...]
"""
import os, sys, runpy, tempfile, pathlib

base = pathlib.Path(os.environ['FC5_WORK']).resolve()
base.mkdir(parents=True, exist_ok=True)
_mkdtemp = tempfile.mkdtemp


def mkdtemp(suffix=None, prefix=None, dir=None):
    return _mkdtemp(suffix, prefix, str(base) if dir is None else dir)


class KeepDir:
    def __init__(self, suffix=None, prefix=None, dir=None, ignore_cleanup_errors=False, **kw):
        self.name = mkdtemp(suffix, prefix, dir)
        print(f'[keep_run] 지우지 않는 임시 폴더: {self.name}', flush=True)

    def __enter__(self):
        return self.name

    def __exit__(self, *exc):
        return False

    def cleanup(self):
        pass


_unlink = pathlib.Path.unlink


def unlink(self, missing_ok=False):
    try:
        inside = pathlib.Path(os.path.abspath(self)).is_relative_to(base)
    except Exception:
        inside = False
    if inside:
        with open(base / 'unlink-skipped.txt', 'a', encoding='utf-8') as f:
            f.write(f'{self}\texists={self.exists()}\n')
        print(f'[keep_run] 지우지 않음: {self}', flush=True)
        return None
    return _unlink(self, missing_ok=missing_ok)


tempfile.mkdtemp = mkdtemp
tempfile.TemporaryDirectory = KeepDir
pathlib.Path.unlink = unlink
script = sys.argv[1]
sys.argv = sys.argv[1:]
runpy.run_path(script, run_name='__main__')
