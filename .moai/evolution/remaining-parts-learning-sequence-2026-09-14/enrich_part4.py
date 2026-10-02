from __future__ import annotations
raise SystemExit("옛 Part 4 보조 스크립트(enrich_part4.py)입니다. 실행하면 Ch 13~16 개선본을 옛 글로 덮어씁니다. 개선본은 각 챕터 qa/upgrade/author_NN.py를 쓰세요.")

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "labs/part4"))
from notebook_guidance import inject_guidance
CHAPTERS = [
    (
        ROOT / "textbook/part4/ch13-langgraph-basics",
        ROOT / "labs/part4/ch13-langgraph-basics/notebooks",
        ROOT / "textbook/part4/ch13-langgraph-basics/qa/depth-notes.json",
    ),
    (
        ROOT / "textbook/part4/ch14-rag-patterns",
        ROOT / "labs/part4/ch14-rag-patterns/notebooks",
        ROOT / "textbook/part4/ch14-rag-patterns/depth-notes.json",
    ),
    (
        ROOT / "textbook/part4/ch15-evaluation-advanced",
        ROOT / "labs/part4/ch15-evaluation-advanced/notebooks",
        ROOT / "textbook/part4/ch15-evaluation-advanced/depth-notes.json",
    ),
    (
        ROOT / "textbook/part4/ch16-guardrails",
        ROOT / "labs/part4/ch16-guardrails/notebooks",
        ROOT / "labs/part4/ch16-guardrails/depth-notes.json",
    ),
]


def html_block(note: dict[str, str]) -> str:
    return (
        f"<h3>호출 표기와 실행 시점</h3><p>{note['mechanics']}</p>"
        f"<h3>다른 상황에 적용</h3><p>{note['transfer']}</p>"
        f"<h3>비교와 경계</h3><p>{note['boundary']}</p>"
    )


def markdown_block(note: dict[str, str]) -> str:
    return (
        "## 개념을 코드에 연결하기\n\n"
        f"**호출 표기와 실행 시점.** {note['mechanics']}\n\n"
        f"**다른 상황에 적용.** {note['transfer']}\n\n"
        f"**비교와 경계.** {note['boundary']}\n"
    )


def apply() -> None:
    changed_sources = 0
    changed_notebooks = 0
    for book_dir, notebook_dir, notes_path in CHAPTERS:
        notes = json.loads(notes_path.read_text(encoding="utf-8"))
        for slug, note in notes.items():
            source_path = book_dir / "_src" / f"{slug}.html"
            source = source_path.read_text(encoding="utf-8")
            marker = "<h3>호출 표기와 실행 시점</h3>"
            if marker not in source:
                anchor = "<h3>도식 읽기</h3>"
                if anchor not in source and "<figure>{{svg:" in source:
                    anchor = "<figure>{{svg:"
                if anchor not in source:
                    raise ValueError(f"도식 읽기 위치 없음: {source_path}")
                source = source.replace(anchor, html_block(note) + anchor, 1)
                source_path.write_text(source, encoding="utf-8")
                changed_sources += 1

            notebook_path = notebook_dir / f"{slug}.ipynb"
            original_text = notebook_path.read_text(encoding="utf-8")
            notebook = json.loads(original_text)
            for cell in notebook["cells"]:
                if cell.get("id") == "concept-depth":
                    refreshed = markdown_block(note).splitlines(keepends=True)
                    if cell["source"] != refreshed:
                        cell["source"] = refreshed
                    break
            if not any(cell.get("id") == "concept-depth" for cell in notebook["cells"]):
                notebook["cells"].insert(
                    1,
                    {
                        "cell_type": "markdown",
                        "id": "concept-depth",
                        "metadata": {},
                        "source": markdown_block(note).splitlines(keepends=True),
                    },
                )
            inject_guidance(notebook)
            rendered = json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"
            if rendered != original_text:
                notebook_path.write_text(rendered, encoding="utf-8")
                changed_notebooks += 1
    print(f"sources={changed_sources} notebooks={changed_notebooks}")


if __name__ == "__main__":
    apply()
