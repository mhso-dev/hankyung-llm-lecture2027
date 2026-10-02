"""Exercise the real kernel boundary without making network/API requests."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

import nbformat

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from execute import execute
from render import validate


class ExecutionTests(unittest.TestCase):
    def test_output_redaction_preserves_executed_source(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / 'lesson.ipynb'
            source = 'from pathlib import Path\nprint(Path.home())'
            nbformat.write(nbformat.v4.new_notebook(cells=[
                nbformat.v4.new_code_cell(source)]), path)
            execute(path, root, sys.executable)
            saved = nbformat.read(path, as_version=4)
            self.assertEqual(saved.cells[0].source, source)
            self.assertEqual(saved.cells[0].outputs[0].text.strip(), '[사용자 폴더]')
            validate(saved)

    def test_parent_secret_is_redacted_in_failure_diagnostics(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            child = root / 'notebooks'
            child.mkdir()
            fake = 'fake-test-key-never-valid-54321'
            (root / '.env').write_text(f'OPENAI_API_KEY={fake}\n')
            path = child / 'lesson.ipynb'
            source = ('from dotenv import load_dotenv, find_dotenv\nimport os\n'
                      'load_dotenv(find_dotenv(usecwd=True), override=True)\n'
                      'raise ValueError(os.getenv("OPENAI_API_KEY"))')
            nbformat.write(nbformat.v4.new_notebook(cells=[
                nbformat.v4.new_code_cell(source)]), path)
            with self.assertRaises(RuntimeError):
                execute(path, child, sys.executable)
            diagnosis = path.with_suffix('.failure.json').read_text()
            self.assertNotIn(fake, diagnosis)
            self.assertEqual(json.loads(diagnosis)['cells'][0]['type'], 'ValueError')
            self.assertNotIn('verification', nbformat.read(path, as_version=4).metadata)


if __name__ == '__main__':
    unittest.main()
