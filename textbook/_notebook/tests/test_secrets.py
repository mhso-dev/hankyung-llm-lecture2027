import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from execute import redact, secret_values


class SecretTests(unittest.TestCase):
    def test_parent_dotenv_is_included_in_secret_scan(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            child = root / 'notebooks'
            child.mkdir()
            fake = 'fake-test-key-never-valid-12345'
            (root / '.env').write_text(f'OPENAI_API_KEY={fake}\n')
            values = secret_values(child)
            self.assertIn(fake, values)
            self.assertNotIn(fake, redact(f'Error includes {fake}', values))


if __name__ == '__main__':
    unittest.main()
