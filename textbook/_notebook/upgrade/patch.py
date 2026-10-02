"""여러 파일에 정확한 치환을 한 번에 적용합니다. 모든 치환이 기대 횟수만큼 맞을 때만 저장합니다.

    import sys; sys.path.insert(0, "textbook/_notebook/upgrade")
    from patch import Patch
    P = Patch("textbook/part1/ch02-python", "03")
    P.gen(old, new)                 # 절 생성기 qa/upgrade/author_03.py (없으면 author_upgrade.py)
    P.rep("_src/03-....html", old, new)
    P.write("figures/03-1-이름.mmd", text)
    P.save()
"""
import sys
from pathlib import Path

ROOT = Path.home() / "mnt/한국경제신문"


class Patch:
    def __init__(self, chapter: str | Path, section: str | None = None):
        self.ch = Path(chapter) if Path(chapter).is_absolute() else ROOT / chapter
        own = self.ch / f"qa/upgrade/author_{section}.py" if section else None
        self.generator = own if own and own.exists() else self.ch / "qa/upgrade/author_upgrade.py"
        self.files: dict[Path, str] = {}
        self.errors: list[str] = []

    def _path(self, rel) -> Path:
        p = rel if isinstance(rel, Path) and rel.is_absolute() else self.ch / rel
        if p not in self.files:
            self.files[p] = p.read_text(encoding="utf-8")
        return p

    def rep(self, rel, old: str, new: str, count: int = 1) -> None:
        p = self._path(rel)
        n = self.files[p].count(old)
        if n != count:
            self.errors.append(f"{p.name}: {n}건(기대 {count}) :: {old[:60]!r}")
            return
        self.files[p] = self.files[p].replace(old, new)

    def gen(self, old: str, new: str, count: int = 1) -> None:
        self.rep(self.generator, old, new, count)

    def write(self, rel, text: str) -> None:
        p = rel if isinstance(rel, Path) and rel.is_absolute() else self.ch / rel
        self.files[p] = text

    def save(self) -> None:
        if self.errors:
            print("저장 안 함. 실패:")
            for e in self.errors:
                print("  ", e)
            sys.exit(1)
        for p, t in self.files.items():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(t, encoding="utf-8")
        print("저장:", len(self.files), "파일")
