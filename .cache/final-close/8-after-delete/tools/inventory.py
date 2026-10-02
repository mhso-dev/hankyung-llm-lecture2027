"""연결 폴더 목록(경로·크기·mtime_ns)과 결과 파일 sha256 — 검사 전후 견줌용. 읽기만 함."""
import hashlib, json, os, sys
from pathlib import Path
ROOT = Path.home() / "mnt" / "한국경제신문"
out = Path(sys.argv[1])
SKIP_DIRS = {".venv"}
SKIP_PREFIX = [".cache/vm/pgenv", ".cache/vm/pgdata", ".cache/final-close/8-after-delete"]
rows = {}
pyc = []
for dp, dns, fns in os.walk(ROOT):
    rel = os.path.relpath(dp, ROOT)
    if any(rel == p or rel.startswith(p + "/") for p in SKIP_PREFIX):
        dns[:] = []; continue
    keep = []
    for d in dns:
        if d in SKIP_DIRS: continue
        if d == "__pycache__": pyc.append(os.path.normpath(os.path.join(rel, d)))
        keep.append(d)
    dns[:] = keep
    for f in fns:
        p = os.path.join(dp, f)
        try: st = os.lstat(p)
        except FileNotFoundError: continue
        rows[os.path.normpath(os.path.join(rel, f))] = [st.st_size, st.st_mtime_ns]
json.dump({"files": rows, "pycache": sorted(pyc)}, open(out, "w"), ensure_ascii=False)
print("files", len(rows), "pycache", len(pyc))
