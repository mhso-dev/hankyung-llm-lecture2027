"""사용: python3 textbook/_notebook/upgrade/mdpatch.py <챕터 경로> NN reps.json
[[old,new],...]를 생성기·노트북 마크다운 셀·_src에 같이 적용합니다(재실행 없이 설명만 고칠 때)."""
import glob, json, sys
from pathlib import Path
ROOT = Path.home() / "mnt/한국경제신문"
ch = ROOT / sys.argv[1]; n = sys.argv[2]; reps = json.load(open(sys.argv[3]))
lab = ROOT / (json.load(open(ch / "chapter.json"))["lab_path"] if (ch / "chapter.json").exists() else "labs/" + sys.argv[1].split("textbook/", 1)[1])
gen = ch / f"qa/upgrade/author_{n}.py"
if not gen.exists(): gen = ch / "qa/upgrade/author_upgrade.py"
nb_path = Path(glob.glob(str(lab / f"notebooks/{n}-*.ipynb"))[0])
src_path = Path(glob.glob(str(ch / f"_src/{n}-*.html"))[0])
g = gen.read_text(); nb = json.loads(nb_path.read_text()); src = src_path.read_text()
for old, new in reps:
    hits = 0
    if old in g: g = g.replace(old, new); hits += 1
    for c in nb["cells"]:
        if c["cell_type"] == "markdown":
            s = c["source"] if isinstance(c["source"], str) else "".join(c["source"])
            if old in s: c["source"] = s.replace(old, new); hits += 1
    if old in src: src = src.replace(old, new); hits += 1
    print(("OK " if hits else "MISS ") + old[:50])
gen.write_text(g); nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n"); src_path.write_text(src)
