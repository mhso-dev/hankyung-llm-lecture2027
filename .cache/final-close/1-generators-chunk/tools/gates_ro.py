"""upgrade_gates.check_section만 불러 쓰기 없이 셈."""
import importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path.home() / "mnt/한국경제신문"
spec = importlib.util.spec_from_file_location("ug", ROOT / "textbook/_notebook/checks/upgrade_gates.py")
ug = importlib.util.module_from_spec(spec); spec.loader.exec_module(ug)
for ch in sys.argv[1:]:
    chapter = ROOT / ch
    cfg = json.loads((chapter / "chapter.json").read_text(encoding="utf-8")) if (chapter / "chapter.json").is_file() else None
    lab = ROOT / cfg["lab_path"] if cfg else ROOT / "labs" / chapter.relative_to(ROOT / "textbook")
    slugs = [s["slug"] for s in cfg["sections"]] if cfg else sorted(p.stem for p in (chapter / "_src").glob("[0-9][0-9]-*.html"))
    for slug in slugs:
        r = ug.check_section(chapter, lab, slug)
        bad = {k: v for k, v in r["issues"].items() if v}
        print(ch.split('/')[-1], slug[:30], r["sentences"], "PASS" if r["passed"] else bad)
