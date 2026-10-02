"""생성기(author_NN.py)가 만드는 마크다운·코드·_src가 지금 파일과 같은지 쓰기 없이 확인."""
import importlib.util, json, sys, glob
from pathlib import Path
sys.dont_write_bytecode = True
gen, nbp = sys.argv[1], sys.argv[2]
src = sys.argv[3] if len(sys.argv) > 3 else None
spec = importlib.util.spec_from_file_location("gen_mod", gen)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
if hasattr(mod, "cells"):
    cells = mod.cells()
else:
    fn = [getattr(mod, n) for n in dir(mod) if n.startswith("section_")][0]
    _, _, cells = fn()
nb = json.load(open(nbp, encoding="utf-8"))
t = lambda s: s if isinstance(s, str) else "".join(s)
a = [(c["cell_type"], t(c["source"])) for c in cells]
b = [(c["cell_type"], t(c["source"])) for c in nb["cells"]]
print("cells", len(a), len(b))
diff = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
print("differing cells:", diff[:20])
for i in diff[:3]:
    x, y = a[i][1], b[i][1]
    k = next((j for j in range(min(len(x), len(y))) if x[j] != y[j]), min(len(x), len(y)))
    print(i, a[i][0], "GEN:", repr(x[max(0,k-40):k+60]), "\n   NB:", repr(y[max(0,k-40):k+60]))
if src and hasattr(mod, "src_html"):
    print("src same:", mod.src_html() == Path(src).read_text(encoding="utf-8"))
