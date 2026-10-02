"""치환 목록을 메모리에서 적용한 뒤 G6(문장 길이·영어 시작·금지어·빽빽한 단락)과 G5 인용을 셈."""
import importlib.util, json, sys, re
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path.home() / "mnt/한국경제신문"
spec = importlib.util.spec_from_file_location("ug", ROOT / "textbook/_notebook/checks/upgrade_gates.py")
ug = importlib.util.module_from_spec(spec); spec.loader.exec_module(ug)
nb_p, src_p, reps_p = sys.argv[1:4]
reps = json.load(open(reps_p, encoding="utf-8"))
nb = json.load(open(nb_p, encoding="utf-8")); src = open(src_p, encoding="utf-8").read()
t = lambda s: s if isinstance(s, str) else "".join(s)
for old, new in reps:
    src = src.replace(old, new)
    for c in nb["cells"]:
        if c["cell_type"] == "markdown":
            s = t(c["source"])
            if old in s: c["source"] = s.replace(old, new)
tmp = Path(reps_p).with_suffix(".sim.ipynb"); tmp.write_text(json.dumps(nb, ensure_ascii=False), encoding="utf-8")
r = ug.check_notebook(tmp)
g6s = ug.g6_prose(src); g6n = ug.g6_prose("\n\n".join(r.pop("prose")))
for k in ("long", "english_start", "banned", "dense_paragraphs"):
    for x in g6s[k]: print("SRC", k, ug.measured_length(x) if k == "long" else "", x[:160])
    for x in g6n[k]: print("NB ", k, ug.measured_length(x) if k == "long" else "", x[:160])
print("G1-G5:", {k: v for k, v in r.items() if v and k != "code_cells"})
