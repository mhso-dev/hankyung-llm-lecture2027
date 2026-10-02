"""Build the Part 2 reading entry and a verified public notebook bundle."""

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
    ("ch06-langchain-start", "Ch 6 · LangChain 시작", 6, 10, 7,
     "메시지를 보내고 응답을 읽습니다. 출력 형식과 오류를 확인하고 토큰·비용·지연을 기록합니다."),
    ("ch07-prompt-engineering", "Ch 7 · 프롬프트 엔지니어링", 8, 16, 9,
     "같은 과제에서 지시와 예시를 바꾸고, 실제 답과 사용량을 비교합니다."),
    ("ch08-context-engineering", "Ch 8 · 컨텍스트 엔지니어링", 6, 10, 7,
     "필요한 자료를 선택하고 정리합니다. 입력 길이와 정보 배치에 따른 답의 변화를 관찰합니다."),
)

START = """# Part 2 실습 시작하기

이 묶음은 Ch 6·7·8의 개념 절과 대응하는 실행 노트북입니다. 압축을 푼 `part2-practice` 폴더 전체를 유지하고 Ch 6의 01절부터 시작합니다. VS Code에서 지금 학습할 챕터 폴더(예: `labs/part2/ch06-langchain-start`)를 엽니다. 그 폴더의 터미널에서 `uv sync --locked`로 Python 3.12·패키지·커널을 준비합니다. 다음 챕터에서도 해당 챕터 폴더에서 같은 명령을 실행합니다.

압축 해제한 최상위 `part2-practice` 폴더의 `env.example`을 같은 위치에 `.env`라는 이름으로 복사하고 사용할 제공자의 키를 저장합니다. 기본 실습에는 `OPENAI_API_KEY`가 필요합니다. Ch 6의 세 제공자 비교에 참여하려면 `ANTHROPIC_API_KEY`와 `GOOGLE_API_KEY`도 준비합니다. 키가 없는 제공자는 미실행으로 표시됩니다. 키를 노트북 코드나 출력에 적지 않습니다.

노트북을 열고 이 챕터의 `.venv`를 커널로 선택한 뒤 첫 셀부터 `Shift+Enter`로 실행합니다. 설치 셀이 끝날 때까지 기다린 뒤 설명 → 코드 → 출력 순서로 읽습니다. API를 다시 호출하면 사용량에 따른 비용이 발생합니다. 모델의 문장과 처리 시간은 교재에 저장된 결과와 달라질 수 있습니다.

각 절은 새 커널에서 독립 실행합니다. `NameError`는 앞 셀을 빠뜨렸는지, `ModuleNotFoundError`는 이 챕터의 `uv sync --locked` 실행과 `.venv` 커널 선택을 확인합니다. 설치 셀이 있는 절은 해당 셀도 실행합니다. 키 오류는 `.env` 파일명과 변수 이름만 확인하고 키 값을 출력하지 않습니다. 변수 상태가 헷갈리면 커널을 다시 시작한 뒤 첫 셀부터 실행합니다.

`manifest.json`은 파일별 SHA-256 값을 기록한 목록입니다. 제공된 가상 기관·정책·문의는 학습용 예시이며 실제 기관의 안내가 아닙니다.
"""


def main() -> None:
    rows = []
    files = []
    reports = []
    # 절 수(count)는 강의 시간(lecture)과 따로 둔다: 챕터 끝 실습 절이 더해져 절 수 ≠ 강의 시간(2026-09-21, Ch 7 §2-7 리팩터)
    for slug, title, lecture, practice, count, description in CHAPTERS:
        chapter = HERE / slug
        lab = ROOT / "labs" / "part2" / slug
        sources = sorted((chapter / "_src").glob("[0-9][0-9]-*.html"))
        if len(sources) != count or not (chapter / "index.html").is_file():
            raise ValueError(f"Incomplete chapter: {slug}")
        for source in sources:
            notebook = lab / "notebooks" / f"{source.stem}.ipynb"
            reports.append(verify_lesson(notebook, chapter / source.name))
            files.append(notebook)
        for name in ("pyproject.toml", "uv.lock", "README.md"):
            path = lab / name
            if not path.is_file() or path.is_symlink():
                raise ValueError(f"Missing public setup file: {path}")
            files.append(path)
        links = "".join(
            f'<li><a href="{slug}/{html.escape(source.name, quote=True)}">'
            f'{html.escape(source.stem.replace("-", " "))}</a></li>'
            for source in sources
        )
        rows.append(
            f'<section><h2><a href="{slug}/index.html">{html.escape(title)}</a></h2>'
            f'<p>{description}</p><p>강의 {lecture}시간 · 실습 {practice}시간 · '
            f'{len(sources)}절</p><ol>{links}</ol></section>'
        )

    css = (RUNTIME / "theme.css").read_text()
    css += """
    *{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,sans-serif;
    line-height:1.8;word-break:keep-all;color:#202020;background:#fff}
    a{color:#2456a6;overflow-wrap:anywhere}h1{font-size:30px;line-height:1.4}
    h2{font-size:24px;margin-top:40px}li{margin:8px 0}p,li{font-size:16px}
    .intro{padding:18px;background:#f5f7fa;border:1px solid #cbd5e1;border-radius:8px}
    """
    page = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Part 2 · LangChain과 프롬프트</title><style>{css}</style></head>
    <body><main class="page"><header class="top"><p><a href="../index.html">전체 교재</a></p>
    <h1>Part 2 · LangChain과 프롬프트</h1>
    <p>Ch 6–8 · 23절 · 총 56시간 · 강의 20시간 · 실습 36시간</p></header>
    <div class="intro"><p>모델에 첫 메시지를 보내는 것부터 시작합니다. 같은 과제의 프롬프트와
    입력 자료를 바꾸며 답이 어떻게 달라지는지 직접 확인합니다. Ch 6 → Ch 7 → Ch 8 순서로 읽습니다.</p>
    <p><a href="../downloads/part2-practice.zip" download>Part 2 노트북과 준비 파일 받기</a></p>
    <p>HTML은 설명을 읽고 코드를 복사하는 화면입니다. 코드는 Python 3.12 Jupyter 커널에서
    첫 셀부터 실행합니다. API 키를 준비하는 방법은 묶음의 ‘시작하기.md’에 있습니다.</p></div>
    {''.join(rows)}
    <section><h2>실행 결과를 읽을 때</h2><p>교재에는 실제 실행한 결과가 저장되어 있습니다.
    모델의 답과 지연 시간은 실행마다 달라질 수 있습니다. 사용량이 제공되지 않거나 키가 없어
    실행하지 못한 항목을 0으로 해석하지 않습니다. 한두 과제의 비교 결과로 모델 전체의 우열을 정하지 않습니다.</p>
    <p>Ch 8을 마치면 <a href="../part3/ch09-rag-first-run/index.html">Ch 9 RAG</a>에서
    필요한 자료를 검색해 질문과 함께 전달하는 실습으로 이어갑니다.</p></section>
    </main></body></html>"""
    (HERE / "index.html").write_text(page)

    output = HERE.parent / "downloads" / "part2-practice.zip"
    files = [path for path in practice_files(ROOT)
             if path.relative_to(ROOT).as_posix().startswith("labs/part2/")]
    output.parent.mkdir(exist_ok=True)
    prefix = "part2-practice/"
    manifest = []
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        archive.writestr(prefix + "시작하기.md", START)
        archive.writestr(prefix + "env.example",
                         "OPENAI_API_KEY=\nANTHROPIC_API_KEY=\nGOOGLE_API_KEY=\n")
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            data = path.read_bytes()
            archive.writestr(prefix + relative, data)
            manifest.append({"path": relative, "sha256": hashlib.sha256(data).hexdigest()})
        archive.writestr(prefix + "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    with ZipFile(output) as archive:
        assert archive.testzip() is None
        assert not any(Path(name).name == ".env" for name in archive.namelist())
        for entry in manifest:
            assert hashlib.sha256(archive.read(prefix + entry["path"])).hexdigest() == entry["sha256"]
    qa = HERE / "qa"
    qa.mkdir(exist_ok=True)
    (qa / "integration-results.json").write_text(json.dumps({
        "sections": len(reports),
        "code_cells": sum(report["code_cells"] for report in reports),
        "notebook_html_downloads_match": True,
        "bundle_files": len(files),
        "bundle_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "bundle_manifest_verified": True,
    }, ensure_ascii=False, indent=2))
    print(f"Part 2: {len(reports)} verified sections; {len(files)} bundled files")


if __name__ == "__main__":
    main()
