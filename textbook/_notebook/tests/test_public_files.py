"""Protect bundle boundaries when a parent directory is a symbolic link."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_bundle import check_public_file


class PublicFileTests(unittest.TestCase):
    def test_regular_file_inside_root_is_allowed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / 'labs/part5/data/example.json'
            path.parent.mkdir(parents=True)
            path.write_text('{}')
            check_public_file(root, path)

    def test_symlink_parent_is_rejected_even_if_target_is_inside_root(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / 'actual'
            target.mkdir()
            (target / 'example.json').write_text('{}')
            (root / 'shortcut').symlink_to(target, target_is_directory=True)
            with self.assertRaises(ValueError):
                check_public_file(root, root / 'shortcut/example.json')

    def test_symlink_parent_outside_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            root, outside = base / 'project', base / 'outside'
            root.mkdir()
            outside.mkdir()
            (outside / 'private.txt').write_text('private fixture')
            (root / 'data').symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                check_public_file(root, root / 'data/private.txt')

    def test_absolute_external_and_missing_files_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'project'
            root.mkdir()
            external = Path(folder) / 'external.txt'
            external.write_text('fixture')
            for path in (external, root / 'missing'):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    check_public_file(root, path)
