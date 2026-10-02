from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "textbook" / "_template"))
from builder import build_chapter

if __name__ == "__main__":
    for path in build_chapter(HERE, root=ROOT):
        print("wrote", path.name)
