"""Regression checks for source extraction and preserved textbook evidence."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chapter_builder", ROOT / "_build.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class SourceExtractionTests(unittest.TestCase):
    def test_decorated_class_keeps_its_decorator(self):
        with tempfile.TemporaryDirectory() as folder:
            lab = Path(folder)
            (lab / "sample.py").write_text("@dataclass\nclass Answer:\n    text: str\n")
            with patch.object(builder, "LAB", lab):
                self.assertIn("@dataclass", builder.source_code("sample.py#Answer"))

    def test_multiple_symbols_follow_source_order_and_escape_html(self):
        with tempfile.TemporaryDirectory() as folder:
            lab = Path(folder)
            (lab / "sample.py").write_text(
                'def first():\n    return "<tag>"\n\ndef second():\n    return 2\n'
            )
            with patch.object(builder, "LAB", lab):
                text = builder.source_code("sample.py#second,first")
                self.assertLess(text.index("first"), text.index("second"))
                self.assertIn("&lt;tag&gt;", text)
                with self.assertRaises(ValueError):
                    builder.source_code("sample.py#missing")

    def test_output_is_read_verbatim_and_html_escaped(self):
        with tempfile.TemporaryDirectory() as folder:
            lab = Path(folder)
            (lab / "runs" / "examples").mkdir(parents=True)
            (lab / "runs" / "examples" / "saved.txt").write_text("<answer> & 1\n")
            with patch.object(builder, "LAB", lab):
                self.assertEqual(builder.example_output("saved.txt"), "&lt;answer&gt; &amp; 1")
                with self.assertRaises(FileNotFoundError):
                    builder.example_output("missing.txt")


if __name__ == "__main__":
    unittest.main()
