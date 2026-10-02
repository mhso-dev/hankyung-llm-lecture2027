"""Build Part 1 navigation and a bundle of verified public practice files."""
from __future__ import annotations

import hashlib
import html
import json
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUNTIME = HERE.parent / "_notebook"
sys.path.insert(0, str(RUNTIME))
from build_bundle import practice_files
from verify import verify_lesson

CHAPTERS = (
    ("ch01-development-environment", "개발환경", 5, 3, 6,
     "개발 도구를 준비하고 경로·가상환경·디버거를 확인합니다."),
    ("ch02-python", "파이썬 프로그래밍", 12, 28, 13,
     "문법·함수·테스트를 익힌 뒤 A/B 두 학습 경로 모두 비동기 실행까지 이어집니다."),
    ("ch03-git-github", "Git과 GitHub 협업", 5, 11, 6,
     "변경을 커밋하고 리뷰합니다. 충돌을 해결하고 변경과 이력을 복구합니다."),
    ("ch04-data-tools", "데이터 다루기", 5, 11, 6,
     "표·SQL·HTTP·문서에서 자료를 조회하고 재사용할 함수를 검증합니다."),
    ("ch05-llm-principles", "LLM 동작 원리", 10, 6, 9,
     "로컬 모델로 토큰·임베딩·샘플링을 관찰하고 모델 답변을 해석할 수 있는 범위를 구분합니다."),
)

START = """# Part 1 실습 시작하기

Ch 1부터 Ch 5까지 순서대로 학습합니다. 이 묶음에는 40개 기본 노트북과 각 장의 준비 파일이 있습니다. 압축을 푼 뒤 `labs/part1`의 폴더 구조를 유지합니다.

각 장의 `README.md`에서 준비 방법을 확인합니다. Python 3.12와 uv를 준비하고 해당 장 폴더에서 `uv sync --locked`를 실행합니다. VS Code의 Python 인터프리터와 Jupyter 커널은 해당 장의 `.venv`를 선택합니다. 노트북의 첫 셀부터 Shift+Enter로 실행합니다. 설치 셀이 있으면 셀 실행이 끝날 때까지 기다립니다.

Ch 1·2는 환경과 파이썬, Ch 3은 Git, Ch 4는 데이터 조회, Ch 5는 LLM의 동작을 다룹니다. Ch 2의 A/B 경로 모두 12절 비동기 실행을 학습합니다. Ch 3에서는 실습용 저장소와 가상 시크릿을 사용합니다. 작업 중인 실제 저장소에 이력 변경 명령을 옮겨 실행하지 않습니다. GitHub PR 화면에서 수행할 절차와 로컬 저장소에서 실행한 실습은 구분해 읽습니다.

Ch 4는 로컬 HTTP 서버와 학습 데이터를 사용합니다. 함께 제공한 조회 함수와 테스트는 해당 장의 README에 따라 확인합니다. Ch 5의 모델 파일은 처음 실행할 때 인터넷으로 내려받습니다. 모델 가중치는 이 ZIP에 포함하지 않습니다. 필요한 메모리와 최초 다운로드는 Ch 5의 README에서 확인합니다. Part 1에는 유료 모델 API 키가 필요하지 않습니다. 첫 외부 모델 API 호출은 Ch 6에서 학습합니다.

기본 결과를 확인한 뒤 안내된 값 하나를 바꿔 비교합니다. 실행 도중 변수가 준비되지 않았다는 오류가 나오면 첫 셀부터 실행했는지 확인합니다. 이전 실행 상태가 혼동되면 커널을 다시 시작합니다. 모델 출력과 처리 시간은 실행 환경에 따라 달라질 수 있습니다.

`manifest.json`은 파일 경로와 SHA-256 값을 기록한 목록입니다. HTML은 교재를 읽고 코드를 복사하는 화면이며 실제 코드 실행은 노트북에서 합니다.
"""


def main() -> None:
    rows, reports = [], []
    for slug, title, lecture, practice, count, description in CHAPTERS:
        chapter = HERE / slug
        config = json.loads((chapter / "chapter.json").read_text())
        sections = config["sections"]
        if len(sections) != count or not (chapter / "index.html").is_file():
            raise ValueError(f"Incomplete chapter: {slug}")
        links = []
        for section in sections:
            name = section["slug"]
            notebook = ROOT / "labs/part1" / slug / "notebooks" / f"{name}.ipynb"
            reports.append(verify_lesson(notebook, chapter / f"{name}.html"))
            label = section.get("title", name.replace("-", " "))
            links.append(f'<li><a href="{slug}/{html.escape(name, quote=True)}.html">{html.escape(label)}</a></li>')
        number = int(slug[2:4])
        rows.append(f'<section><h2><a href="{slug}/index.html">Ch {number} · {title}</a></h2>'
                    f'<p>{description}</p><p>강의 {lecture}시간 · 실습 {practice}시간 · {count}절</p>'
                    f'<ol>{"".join(links)}</ol></section>')
    css = (RUNTIME / "theme.css").read_text()
    css += """*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,sans-serif;
    line-height:1.8;word-break:keep-all;color:#202020;background:white}
    a{color:#2456a6;overflow-wrap:anywhere}h1{font-size:30px;line-height:1.4}
    h2{font-size:24px;margin-top:40px}p,li{font-size:16px}li{margin:8px 0}
    .intro{padding:18px;background:#f5f7fa;border:1px solid #cbd5e1;border-radius:8px}"""
    page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1"><title>Part 1 · 개발 기반</title>
    <style>{css}</style></head><body><main class="page"><header class="top">
    <p><a href="../index.html">전체 교재</a></p><h1>Part 1 · 개발 기반</h1>
    <p>Ch 1–5 · 40절 · 총 96시간 · 강의 37시간 · 실습 59시간</p></header>
    <div class="intro"><p>환경을 준비하고 파이썬 코드를 작성하는 것부터 시작합니다.
    Git으로 변경을 관리하고 데이터 조회 함수를 만든 뒤, 로컬 모델로 LLM의 동작을 관찰합니다.</p>
    <p><a href="../downloads/part1-practice.zip" download>Part 1 노트북과 준비 파일 받기</a></p>
    <p>각 장의 README에 따라 Python 3.12 커널을 준비하고 첫 셀부터 실행합니다.
    Part 1에는 유료 모델 API 키가 필요하지 않습니다. Ch 5는 모델 파일의 최초 다운로드가 필요합니다.</p></div>
    {"".join(rows)}
    <section><h2>다음 학습과 이어지는 지점</h2><p>Ch 2의 비동기 코드는 Ch 18·30에서,
    Ch 4의 데이터 조회 함수는 Ch 19의 도구 작성에서 다시 사용합니다.
    Ch 5를 마치면 <a href="../part2/ch06-langchain-start/index.html">Ch 6 LangChain 시작</a>에서
    외부 모델 API를 처음 호출합니다.</p></section></main></body></html>'''
    (HERE / "index.html").write_text(page, encoding="utf-8")
    files = [path for path in practice_files(ROOT) if path.is_relative_to(ROOT / "labs/part1")]
    output = HERE.parent / "downloads/part1-practice.zip"
    output.parent.mkdir(exist_ok=True)
    prefix, manifest = "part1-practice/", []
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        archive.writestr(prefix + "시작하기.md", START)
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            data = path.read_bytes()
            archive.writestr(prefix + relative, data)
            manifest.append({"path": relative, "sha256": hashlib.sha256(data).hexdigest()})
        archive.writestr(prefix + "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    with ZipFile(output) as archive:
        assert archive.testzip() is None
        assert sum(name.endswith(".ipynb") for name in archive.namelist()) == len(reports)
        assert not any(Path(name).name == ".env" for name in archive.namelist())
        for entry in manifest:
            assert hashlib.sha256(archive.read(prefix + entry["path"])).hexdigest() == entry["sha256"]
    qa = HERE / "qa"
    qa.mkdir(exist_ok=True)
    (qa / "integration-results.json").write_text(json.dumps({
        "sections": len(reports), "code_cells": sum(row["code_cells"] for row in reports),
        "notebook_html_downloads_match": True, "bundle_files": len(files),
        "bundle_manifest_verified": True,
        "bundle_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
    }, ensure_ascii=False, indent=2))
    print(f"Part 1: {len(reports)} verified sections; {len(files)} bundled files")


if __name__ == "__main__":
    main()
