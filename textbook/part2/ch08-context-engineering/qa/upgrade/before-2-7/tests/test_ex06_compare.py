import importlib.util
from pathlib import Path


def load_example():
    path = Path(__file__).resolve().parents[1] / "examples" / "ex06_compare.py"
    spec = importlib.util.spec_from_file_location("ex06_compare", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_three_designs_preserve_answer_and_source() -> None:
    module = load_example()
    designs = module.build_designs()
    assert set(designs) == {"full", "selected", "compressed"}
    for context in designs.values():
        assert "7권" in context
        assert "14일" in context
        assert "E01" in context


def test_progressive_disclosure_is_fixed_two_stage_loading() -> None:
    catalog, selected = load_example().progressive_disclosure()
    assert len(catalog) == 5
    assert [row["doc_id"] for row in selected] == ["E01-p3"]
