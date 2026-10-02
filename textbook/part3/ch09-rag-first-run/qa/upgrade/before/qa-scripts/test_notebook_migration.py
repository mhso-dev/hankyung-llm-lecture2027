import json
from pathlib import Path

CHAPTER = Path(__file__).resolve().parents[1]
LAB = CHAPTER.parents[2] / "labs" / "part3" / "ch09-rag-first-run"
SECTIONS = [
    "01-RAG-지도",
    "02-로더와-스플리터",
    "03-임베딩과-벡터스토어",
    "04-생성과-출처-인용",
    "05-첫-실패-보기",
    "06-실험-하네스",
]


def test_existing_chapter_structure_is_complete() -> None:
    for slug in SECTIONS:
        source = (CHAPTER / "_src" / f"{slug}.html").read_text(encoding="utf-8")
        for block in range(1, 11):
            assert f'id="b{block}"' in source
        assert 'id="b11"' not in source
        assert '<details class="quiz"' in source
        assert '<details class="instructor"' not in source


def test_visual_and_review_material_exists_before_migration() -> None:
    sources = [
        (CHAPTER / "_src" / f"{slug}.html").read_text(encoding="utf-8")
        for slug in SECTIONS
    ]
    assert sum(text.count("{{svg:") for text in sources) == 5
    assert sum(text.count("{{img:") for text in sources) == 3
    assert sum(text.count('class="quiz-q"') for text in sources) >= 18
    assert all('<h2 id="b5">' in text and '<h2 id="b6">' in text for text in sources)


def test_each_section_embeds_its_matching_notebook() -> None:
    for slug in SECTIONS:
        source = (CHAPTER / "_src" / f"{slug}.html").read_text(encoding="utf-8")
        assert source.count(f"{{{{notebook:{slug}|example}}}}") == 1
        assert source.count(f"{{{{notebook:{slug}|failure}}}}") == 1
        assert "{{code:" not in source[source.index('<h2 id="b5"'):source.index('<h2 id="b7"')]


def test_notebooks_are_short_and_self_contained() -> None:
    for slug in SECTIONS:
        path = LAB / "notebooks" / f"{slug}.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        assert notebook["nbformat"] == 4
        code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
        install_cell = "".join(code_cells[0]["source"])
        assert install_cell.count("%pip install -q") == 1
        assert all(
            not line.strip() or line.lstrip().startswith("#")
            for line in install_cell.split("%pip install -q", maxsplit=1)[0].splitlines()
        )
        uses_dotenv = any("find_dotenv(usecwd=True)" in "".join(cell["source"]) for cell in code_cells)
        assert max(len(cell["source"]) for cell in code_cells) <= 25
        for index, cell in enumerate(notebook["cells"]):
            if cell["cell_type"] == "code" and index > 0:
                assert notebook["cells"][index - 1]["cell_type"] == "markdown"
        joined = "\n".join("".join(cell["source"]) for cell in code_cells)
        parts = [cell.get("metadata", {}).get("lesson_part", "example") for cell in notebook["cells"]]
        assert parts == sorted(parts, key={"example": 0, "before": 1, "after": 2}.get)
        assert {"before", "after"}.issubset(parts)
        for part in ("before", "after"):
            staged = [cell for cell in notebook["cells"] if cell.get("metadata", {}).get("lesson_part") == part]
            assert {cell["cell_type"] for cell in staged} == {"markdown", "code"}
            assert any(cell.get("outputs") for cell in staged if cell["cell_type"] == "code")
        assert "__file__" not in joined
        assert "sys.path" not in joined
        assert "from rag import" not in joined
        assert "from harness import" not in joined
        assert "TODO" not in joined
        assert "except " in joined
        assert "assert " in joined
        if slug == "02-로더와-스플리터":
            assert "OPENAI_API_KEY" not in joined
            assert not uses_dotenv
        else:
            assert "OPENAI_API_KEY" in joined
            assert uses_dotenv
        verification = notebook["metadata"]["verification"]
        assert verification["status"] == "passed"
        assert verification["fresh_kernel"] is True
        assert verification["allow_errors"] is False
