from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "textbook" / "_template"))
from builder import build_chapter

if __name__ == "__main__":
    paths = build_chapter(HERE, root=ROOT)
    index = HERE / "index.html"
    intro = (HERE / "_src/index.html").read_text(encoding="utf-8")
    if "[[작성:" in intro:
        raise ValueError("Unfinished chapter introduction")
    index.write_text(index.read_text(encoding="utf-8").replace("<h2>절 목록</h2>", intro + "<h2>절 목록</h2>"), encoding="utf-8")
    for path in paths:
        print("wrote", path.name)
