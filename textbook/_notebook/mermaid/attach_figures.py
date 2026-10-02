"""노트북 설명 셀의 ![대체 텍스트](attachment:이름.png) 에 figures/이름.png 를 셀 첨부로 넣습니다.

코드 셀과 출력은 건드리지 않으므로 실행 검증 해시가 유지됩니다.
사용: python attach_figures.py 노트북.ipynb 챕터/figures
"""
from __future__ import annotations

import base64
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image


def encoded_png(path: Path, width: int = 1100) -> str:
    image = Image.open(path).convert("RGB")
    if image.width > width:
        image = image.resize((width, round(width * image.height / image.width)), Image.Resampling.LANCZOS)
    buffer = io.BytesIO()
    image.save(buffer, "PNG", optimize=True)
    return base64.b64encode(buffer.getvalue()).decode()


def attach(notebook: Path, figures: Path) -> int:
    nb = json.loads(notebook.read_text(encoding="utf-8"))
    count = 0
    for cell in nb["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        source = cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])
        names = re.findall(r"\(attachment:([^)]+)\)", source)
        if not names:
            continue
        cell["attachments"] = {}
        for name in names:
            path = figures / name
            if not path.is_file():
                raise FileNotFoundError(f"그림이 없습니다: {path}")
            cell["attachments"][name] = {"image/png": encoded_png(path)}
            count += 1
    notebook.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return count


if __name__ == "__main__":
    print("attached", attach(Path(sys.argv[1]), Path(sys.argv[2])))
