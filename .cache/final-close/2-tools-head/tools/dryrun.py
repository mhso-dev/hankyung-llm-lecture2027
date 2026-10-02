"""dryrun.py OUTDIR GENERATOR [생성기 인자...]
생성기를 __main__으로 돌리되 파일 쓰기(open 쓰기·Path.write_text/bytes)를 모두 가로채 기록만 하고,
디스크의 같은 파일과 바이트가 같은지 출력한다. 지우기·옮기기·subprocess는 막는다(부르면 멈춤).
다른 내용은 OUTDIR/<파일 이름>.dry 로만 남긴다(OUTDIR은 .cache 아래)."""
import sys, os, io, builtins, pathlib, runpy, hashlib, shutil, subprocess
sys.dont_write_bytecode = True
outdir = pathlib.Path(sys.argv[1]); gen = os.path.abspath(sys.argv[2]); args = sys.argv[3:]
writes = []
real_open = builtins.open
_real_write_text = pathlib.Path.write_text
_real_mkdir = pathlib.Path.mkdir
def record(path, data):
    writes.append((os.path.abspath(str(path)), data))
class RecText(io.StringIO):
    def __init__(self, path, encoding): super().__init__(); self._p = path; self._e = encoding or 'utf-8'
    def close(self):
        if not self.closed: record(self._p, self.getvalue().encode(self._e))
        super().close()
class RecBytes(io.BytesIO):
    def __init__(self, path): super().__init__(); self._p = path
    def close(self):
        if not self.closed: record(self._p, self.getvalue())
        super().close()
def fake_open(file, mode='r', *a, **k):
    if isinstance(file, int) or not any(ch in mode for ch in 'wax+'):
        return real_open(file, mode, *a, **k)
    if 'a' in mode or '+' in mode:
        raise RuntimeError('dryrun: append/update open blocked: %s' % file)
    enc = k.get('encoding') or (a[1] if len(a) > 1 else None)
    return RecBytes(file) if 'b' in mode else RecText(file, enc)
builtins.open = fake_open; io.open = fake_open
def fake_write_text(self, data, encoding=None, errors=None, newline=None):
    record(self, data.encode(encoding or 'utf-8')); return len(data)
def fake_write_bytes(self, data):
    record(self, bytes(data)); return len(data)
def fake_mkdir(self, mode=0o777, parents=False, exist_ok=False):
    if not self.exists(): print('dryrun: mkdir skipped', self)
pathlib.Path.write_text = fake_write_text; pathlib.Path.write_bytes = fake_write_bytes; pathlib.Path.mkdir = fake_mkdir
def blocked(name):
    def f(*a, **k): raise RuntimeError('dryrun: blocked ' + name)
    return f
for mod, names in [(os, ['remove', 'unlink', 'rename', 'replace', 'rmdir', 'removedirs', 'system', 'makedirs']),
                   (shutil, ['copy', 'copy2', 'copyfile', 'copytree', 'move', 'rmtree']),
                   (subprocess, ['run', 'Popen', 'call', 'check_call', 'check_output'])]:
    for n in names: setattr(mod, n, blocked(mod.__name__ + '.' + n))
pathlib.Path.unlink = blocked('Path.unlink'); pathlib.Path.rename = blocked('Path.rename'); pathlib.Path.replace = blocked('Path.replace'); pathlib.Path.rmdir = blocked('Path.rmdir')
sys.path.insert(0, os.path.dirname(gen))
sys.argv = [gen] + args
code = 0
try:
    runpy.run_path(gen, run_name='__main__')
except SystemExit as e:
    code = e.code
except Exception as e:
    code = 'EXC ' + type(e).__name__ + ': ' + str(e)[:300]
builtins.open = real_open; io.open = real_open; pathlib.Path.write_text = _real_write_text; pathlib.Path.mkdir = _real_mkdir
print('== dryrun', os.path.basename(gen), ' '.join(args), 'exit', code)
for p, data in writes:
    if os.path.exists(p):
        with real_open(p, 'rb') as f: disk = f.read()
        st = 'SAME' if disk == data else 'DIFF'
    else:
        st = 'NEW'
    print('  write', st, p.split('/한국경제신문/')[-1], len(data), hashlib.sha256(data).hexdigest()[:12])
    if st != 'SAME':
        _real_mkdir(outdir, parents=True, exist_ok=True)
        with real_open(outdir / (os.path.basename(p) + '.dry'), 'wb') as f: f.write(data)
