import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verify


def add_lesson(root: Path, part: str, chapter: str, stem: str) -> tuple[Path, Path]:
    source = root / "textbook" / part / chapter / "_src" / f"{stem}.html"
    notebook = root / "labs" / part / chapter / "notebooks" / f"{stem}.ipynb"
    page = source.parent.parent / f"{stem}.html"
    source.parent.mkdir(parents=True, exist_ok=True)
    notebook.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("<h2>source</h2>")
    notebook.write_text(json.dumps({"cells": [], "metadata": {}}))
    page.write_text("<h2>built</h2>")
    return notebook, page


class DiscoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_discovers_lessons_from_sources_without_fixed_count(self) -> None:
        first = add_lesson(self.root, "part1", "ch01-demo", "01-first")
        second = add_lesson(self.root, "part1", "ch01-demo", "02-second")
        self.assertEqual(verify.discover_lessons(self.root), [first, second])

    def test_selected_chapter_uses_separate_report(self) -> None:
        add_lesson(self.root, "part1", "ch01-old", "01-old")
        expected = add_lesson(self.root, "part2", "ch22-new", "01-new")
        chapter = self.root / "textbook" / "part2" / "ch22-new"
        self.assertEqual(verify.discover_lessons(self.root, chapter), [expected])
        self.assertEqual(verify.report_path(self.root, chapter).name,
                         "notebook-contracts-part2-ch22-new.json")
        self.assertEqual(verify.report_path(self.root).name, "notebook-contracts.json")

    def test_rejects_missing_notebook(self) -> None:
        _, page = add_lesson(self.root, "part1", "ch01-demo", "01-first")
        notebook = self.root / "labs/part1/ch01-demo/notebooks/01-first.ipynb"
        notebook.unlink()
        with self.assertRaisesRegex(AssertionError, "Missing notebook"):
            verify.discover_lessons(self.root, page.parent)

    def test_rejects_chapter_without_lesson_sources(self) -> None:
        chapter = self.root / "textbook/part1/ch01-empty"
        (chapter / "_src").mkdir(parents=True)
        with self.assertRaisesRegex(AssertionError, "No lesson sources"):
            verify.discover_lessons(self.root, chapter)

    def test_ignores_extra_exercise_notebooks(self) -> None:
        expected = add_lesson(self.root, "part1", "ch01-demo", "01-first")
        extra = self.root / "labs/part1/ch01-demo/notebooks/01-first-exercise.ipynb"
        extra.write_text(json.dumps({"cells": [], "metadata": {}}))
        self.assertEqual(verify.discover_lessons(self.root), [expected])

    def test_rejects_missing_built_html(self) -> None:
        _, page = add_lesson(self.root, "part1", "ch01-demo", "01-first")
        page.unlink()
        with self.assertRaisesRegex(AssertionError, "Missing built HTML"):
            verify.discover_lessons(self.root, page.parent)

    def test_rejects_duplicate_section_numbers(self) -> None:
        add_lesson(self.root, "part1", "ch01-demo", "01-first")
        add_lesson(self.root, "part1", "ch01-demo", "01-second")
        chapter = self.root / "textbook/part1/ch01-demo"
        with self.assertRaisesRegex(AssertionError, "Duplicate lesson number 01"):
            verify.discover_lessons(self.root, chapter)

    def test_rejects_non_part_or_non_chapter_names(self) -> None:
        for part, chapter in [("misc", "ch01-demo"), ("part1", "lesson01")]:
            with self.subTest(part=part, chapter=chapter):
                selected = self.root / "textbook" / part / chapter
                selected.mkdir(parents=True)
                with self.assertRaisesRegex(AssertionError, r"part\*/ch\*"):
                    verify.discover_lessons(self.root, selected)

    def test_existing_validation_helpers_remain_available(self) -> None:
        self.assertTrue(callable(verify.check_imports))
        self.assertTrue(callable(verify.check_failure_section))


if __name__ == "__main__":
    unittest.main()
