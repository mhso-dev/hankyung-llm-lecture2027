import sys, json
from pathlib import Path
ROOT = Path.home() / "mnt" / "한국경제신문"
sys.path.insert(0, str(ROOT / "textbook/_notebook"))
import verify
G = json.load(open("/sessions/rcw-01fa62dwjghtyrmrgyqrfwx5/mnt/한국경제신문/.cache/final-close/8-after-delete/log/gates-result.json"))
out = {}
for name, v in G.items():
    ch = ROOT / "textbook" / v["part"] / name
    try:
        lessons = verify.discover_lessons(ROOT, ch)
    except AssertionError as e:
        out[name] = {"error": str(e)[:300]}; continue
    rows = []; fails = []
    for nb, page in lessons:
        try:
            r = verify.verify_lesson(nb, page, ROOT)
            rows.append((r["code_cells"], r["max_cell_lines"]))
        except AssertionError as e:
            fails.append((nb.name, str(e)[:200]))
        except Exception as e:
            fails.append((nb.name, repr(e)[:200]))
    out[name] = {"sections": len(lessons), "passed": len(rows), "code_cells": sum(a for a, b in rows), "max_lines": max([b for a, b in rows] or [0]), "fails": fails}
    print(name, out[name]["sections"], out[name]["passed"], out[name]["code_cells"], out[name]["max_lines"], fails, flush=True)
Path("/sessions/rcw-01fa62dwjghtyrmrgyqrfwx5/mnt/한국경제신문/.cache/final-close/8-after-delete/log/verifyro-result.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
