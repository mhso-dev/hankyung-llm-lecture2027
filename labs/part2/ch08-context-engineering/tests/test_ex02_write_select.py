from pathlib import Path

from context_lab import load_memory, save_memory, select_documents


def test_external_memory_round_trip_and_manual_selection(tmp_path: Path) -> None:
    rows = [
        {"doc_id": "A", "text": "정답과 무관"},
        {"doc_id": "B", "text": "선택할 내용"},
    ]
    path = tmp_path / "memory.json"
    save_memory(path, rows)
    selected = select_documents(load_memory(path), ["B", "B", "missing"])
    assert selected == [rows[1]]
