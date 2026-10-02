"""Regression tests for code-copy fidelity and execution evidence gates."""
import json
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from execute import code_hash, output_hash
from render import render_notebook, validate


class CodeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside = False
        self.code = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'code' and 'nb-source' in dict(attrs).get('class', ''):
            self.inside = True

    def handle_endtag(self, tag):
        if tag == 'code':
            self.inside = False

    def handle_data(self, data):
        if self.inside:
            self.code += data


def notebook():
    nb = {'cells': [{'cell_type': 'code', 'source': 'if 1 < 2:\n    print("한글 & <tag>")\n',
                    'execution_count': 1, 'outputs': [{'output_type': 'stream',
                    'name': 'stdout', 'text': '한글 & <tag>\n'}]}],
          'metadata': {'language_info': {'version': '3.12.13'}}}
    nb['metadata']['verification'] = {'status': 'passed', 'fresh_kernel': True,
        'code_sha256': code_hash(nb), 'outputs_sha256': output_hash(nb),
        'executed_at': '2026-09-08T00:00:00Z'}
    return nb


class RenderTests(unittest.TestCase):
    def test_progress_output_survives_html_file_roundtrip(self):
        from verify import Cells

        nb = notebook()
        expected = '\rLoading: 0%\rLoading: 100%\r\n완료 & <tag>\n'
        nb['cells'][0]['outputs'][0]['text'] = expected
        nb['metadata']['verification']['outputs_sha256'] = output_hash(nb)
        with tempfile.TemporaryDirectory() as tmp:
            lab = Path(tmp)
            (lab / 'notebooks').mkdir()
            (lab / 'notebooks/test.ipynb').write_text(json.dumps(nb))
            page = lab / 'test.html'
            page.write_text(render_notebook(lab, 'test'))
            parser = Cells()
            parser.feed(page.read_text())
        self.assertEqual(parser.outputs, [expected])

    def test_copy_source_preserves_indentation_html_and_newlines(self):
        nb = notebook()
        with tempfile.TemporaryDirectory() as tmp:
            lab = Path(tmp)
            (lab / 'notebooks').mkdir()
            (lab / 'notebooks/test.ipynb').write_text(json.dumps(nb))
            rendered = render_notebook(lab, 'test')
        parser = CodeParser()
        parser.feed(rendered)
        self.assertEqual(parser.code, nb['cells'][0]['source'])
        self.assertIn('download="test.ipynb"', rendered)
        self.assertIn('한글 &amp; &lt;tag&gt;', rendered)

    def test_stale_code_is_rejected(self):
        nb = notebook()
        nb['cells'][0]['source'] += 'print(3)'
        with self.assertRaisesRegex(ValueError, 'code changed'):
            validate(nb)

    def test_tampered_output_is_rejected(self):
        nb = notebook()
        nb['cells'][0]['outputs'][0]['text'] = 'fabricated output'
        with self.assertRaisesRegex(ValueError, 'outputs changed'):
            validate(nb)

    def test_wrong_python_version_is_rejected(self):
        nb = notebook()
        nb['metadata']['language_info']['version'] = '3.13.1'
        with self.assertRaisesRegex(ValueError, 'Python 3.12'):
            validate(nb)

    def test_changed_execution_count_is_rejected(self):
        nb = notebook()
        nb['cells'][0]['execution_count'] = 42
        with self.assertRaisesRegex(ValueError, 'sequential'):
            validate(nb)

    def test_json_text_arrays_have_the_same_output_hash(self):
        nb = notebook()
        expected = output_hash(nb)
        nb['cells'][0]['outputs'][0]['text'] = ['한글 & <tag>\n']
        self.assertEqual(output_hash(nb), expected)

    def test_missing_verification_and_unexecuted_cells_are_rejected(self):
        nb = notebook()
        nb['metadata'] = {}
        with self.assertRaises(ValueError):
            validate(nb)
        nb = notebook()
        nb['cells'][0]['execution_count'] = None
        with self.assertRaisesRegex(ValueError, 'Unexecuted'):
            validate(nb)


if __name__ == '__main__':
    unittest.main()
