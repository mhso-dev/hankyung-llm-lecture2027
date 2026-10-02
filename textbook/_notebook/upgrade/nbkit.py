"""품질 개선 노트북 생성기 공용 조각 (QUALITY-UPGRADE.md §2·§3·§6).

챕터별 생성기 `textbook/part{P}/ch{CC}-{slug}/qa/upgrade/author_upgrade.py`에서
    import sys; sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade")); from nbkit import *
로 불러 씁니다. 원형은 Ch 22 생성기입니다.
"""
from __future__ import annotations

import json
from pathlib import Path

import datetime as _dt, os as _os
# 실행 날짜 줄: 생성기를 실행한 날(= 새 커널 실행 날). 특정 날짜로 고정하려면 UPGRADE_RUN_DATE를 준다.
RUN_DATE = _os.environ.get("UPGRADE_RUN_DATE") or _dt.date.today().isoformat()


def md(source: str, **metadata) -> dict:
    return {"cell_type": "markdown", "id": "", "metadata": metadata, "source": source.strip("\n")}


def code(source: str, **metadata) -> dict:
    return {"cell_type": "code", "execution_count": None, "id": "", "metadata": metadata, "outputs": [], "source": source.strip("\n")}


def setup(source: str) -> dict:
    """준비 셀(설치·import·키 확인). 게이트 G5의 앞뒤 설명 셀 검사에서 빠집니다."""
    return code(source, lesson_role="setup")


def install_source(packages: list[str]) -> str:
    """고정 버전 패키지를 설치하고 버전을 출력하는 첫 셀. packages 예: ["langchain==1.4.0", "python-dotenv==1.2.3"]"""
    quoted = " ".join(f'"{p}"' for p in packages)
    names = [p.split("==")[0].split("[")[0] for p in packages]
    lines = ["# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다", f"%pip install -q {quoted}", "from importlib.metadata import version", ""]
    lines += [f'print("{n}:", version("{n}"))' for n in names]
    return "\n".join(lines)


KEY = '''# .env 파일에서 OpenAI API 키를 읽습니다(키 값은 출력하지 않습니다)
import os
from dotenv import find_dotenv, load_dotenv

env_path = find_dotenv(usecwd=True)
load_dotenv(env_path)
has_key = os.getenv("OPENAI_API_KEY") is not None
print("OPENAI_API_KEY 설정 여부:", has_key)
assert has_key, "프로젝트 폴더의 .env 파일에 OPENAI_API_KEY를 적어 주세요."'''


def model_source(name: str = "openai:gpt-5.4-mini") -> str:
    return f'''# 실습에 쓸 모델을 준비합니다
model = init_chat_model(
    "{name}",
    temperature=0,
    reasoning_effort="none",
)
print("모델 이름:", model.model_name)
print("temperature:", model.temperature)'''


def title_cells(title: str, todo: list[str], ready: str, figure: str | None, figure_alt: str, figure_read: str,
                install: str) -> list[dict]:
    """제목 셀 → 오늘 볼 그림 → 준비 소제목 → 설치 셀. ready에는 키·데이터·호출 수·실행 시간·예상 비용을 적습니다."""
    steps = "\n".join(f"{number}. {item}" for number, item in enumerate(todo, start=1))
    cells = [md(f"# {title}\n\n**이 노트북에서 할 일**\n\n{steps}\n\n**준비물** — {ready}", html="skip")]
    if figure:
        cells.append(md(f"## 오늘 볼 그림\n\n![{figure_alt}](attachment:{figure})\n\n{figure_read}", html="skip"))
    cells += [
        md("## 1. 준비\n\n첫 셀은 패키지를 설치하고 설치된 버전을 출력합니다. 설치에는 몇십 초가 걸릴 수 있습니다."),
        setup(install),
    ]
    return cells


def key_and_model_cells(model_name: str = "openai:gpt-5.4-mini", note: str = "temperature 값을 0으로 두어 매번 비슷한 답을 고르게 합니다.") -> list[dict]:
    short = model_name.split(":")[-1]
    return [
        md("API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다."),
        setup(KEY),
        md(f"실습에 쓸 모델을 준비합니다.\n{note}"),
        code(model_source(model_name)),
        md(f"**결과 읽기** — 모델 이름 `{short}`, temperature `0.0`이 보이면 준비가 끝났습니다.\\n이 노트북의 출력은 {RUN_DATE}에 이 모델로 실행한 결과입니다.".replace("\\n", "\n")),
    ]


def split_part_boundaries(cells: list[dict]) -> list[dict]:
    """paired 노트북: 결과 읽기와 다음 소제목이 한 셀에 있고 lesson_part가 바뀌면 둘로 나눕니다."""
    result = []
    previous_part = None
    for cell in cells:
        part = cell["metadata"].get("lesson_part")
        text = cell["source"]
        if cell["cell_type"] == "markdown" and part != previous_part and "\n\n## " in text:
            head, tail = text.split("\n\n## ", 1)
            head_meta = {key: value for key, value in cell["metadata"].items() if key != "lesson_part"}
            if previous_part is not None:
                head_meta["lesson_part"] = previous_part
            result.append(md(head, **head_meta))
            result.append(md("## " + tail, **cell["metadata"]))
        else:
            result.append(cell)
        if cell["cell_type"] == "code":
            previous_part = part
    return result


def write_notebook(lab_notebooks: Path, number: str, slug: str, lesson_format: str, cells: list[dict]) -> Path:
    if lesson_format == "paired":
        cells = split_part_boundaries(cells)
    for index, cell in enumerate(cells):
        cell["id"] = f"s{number}-c{index:02d}"
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "lesson_format": lesson_format,
            "quality_upgrade": RUN_DATE,
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path = lab_notebooks / f"{slug}.ipynb"
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return path
