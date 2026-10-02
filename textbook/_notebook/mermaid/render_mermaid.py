"""챕터 figures/*.mmd 를 SVG(HTML 인라인용)와 PNG(노트북 첨부용)로 렌더합니다.

사용: python textbook/_notebook/mermaid/render_mermaid.py textbook/part6/ch22-middleware [--force]
준비: mermaid/README.md 의 설치 절차(mermaid-cli, Chromium 라이브러리).
.mmd 안의 `%% classes` 줄은 AGENTS.md §16 의미 색 classDef 다섯 줄로 바뀝니다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "config.json"
CLASSES = (HERE / "classes.mmd").read_text(encoding="utf-8")
DEFAULT_MMDC = "/tmp/mmd/node_modules/.bin/mmdc"


def mmdc_command() -> list[str]:
    configured = os.environ.get("MMDC", DEFAULT_MMDC)
    if Path(configured).is_file():
        return [configured]
    return ["npx", "--no-install", "mmdc"]


def svg_id(name: str) -> str:
    return "mmd-" + hashlib.sha1(name.encode("utf-8")).hexdigest()[:10]


def render(source: Path, force: bool) -> str:
    text = source.read_text(encoding="utf-8")
    prepared = re.sub(r"(?m)^\s*%% classes\s*$", CLASSES.rstrip("\n"), text)
    digest = hashlib.sha256((prepared + CONFIG.read_text(encoding="utf-8")).encode("utf-8")).hexdigest()
    stamp = source.with_suffix(".render.json")
    svg = source.with_suffix(".svg")
    png = source.with_suffix(".png")
    if not force and stamp.is_file() and svg.is_file() and png.is_file():
        if json.loads(stamp.read_text(encoding="utf-8")).get("sha256") == digest:
            return "skip"
    with tempfile.TemporaryDirectory(prefix="mmd-") as folder:
        temp = Path(folder) / "diagram.mmd"
        temp.write_text(prepared, encoding="utf-8")
        puppeteer = Path(folder) / "puppeteer.json"
        puppeteer.write_text(json.dumps({"args": ["--no-sandbox", "--disable-gpu"]}), encoding="utf-8")
        base = mmdc_command() + ["-i", str(temp), "-c", str(CONFIG), "-p", str(puppeteer), "-b", "white"]
        for extra in (["-o", str(svg), "-I", svg_id(source.stem)], ["-o", str(png), "-s", "2"]):
            done = subprocess.run(base + extra, capture_output=True, text=True)
            if done.returncode != 0:
                raise SystemExit(f"렌더 실패: {source.name}\n{done.stderr[-1500:]}")
    stamp.write_text(json.dumps({"sha256": digest}, ensure_ascii=False), encoding="utf-8")
    return "rendered"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("chapter", type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--only", help="이 문자열로 시작하는 파일만")
    args = parser.parse_args()
    figures = args.chapter / "figures"
    for source in sorted(figures.glob("*.mmd")):
        if args.only and not source.name.startswith(args.only):
            continue
        print(render(source, args.force), source.name, flush=True)


if __name__ == "__main__":
    main()
