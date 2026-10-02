"""Regression tests for the visible failure/repair lesson boundary."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from execute import code_hash, output_hash
from render import expand_notebooks
from test_render import notebook


def paired_notebook():
    nb = notebook()
    for stage, code, output in [
        ("before", "print('failure')", "failure\n"),
        ("after", "print('repaired')", "repaired\n"),
    ]:
        cell = copy.deepcopy(nb["cells"][0])
        cell.update(source=code, execution_count=len(nb["cells"]) + 1,
                    metadata={"lesson_part": stage})
        cell["outputs"][0]["text"] = output
        nb["cells"].append(cell)
    nb["metadata"]["verification"].update(
        code_sha256=code_hash(nb), outputs_sha256=output_hash(nb))
    return nb


class SplitRenderTests(unittest.TestCase):
    def expand(self, nb, body):
        with tempfile.TemporaryDirectory() as tmp:
            lab = Path(tmp)
            (lab / "notebooks").mkdir()
            (lab / "notebooks/test.ipynb").write_text(json.dumps(nb))
            return expand_notebooks(body, lab)

    def test_example_and_repair_are_once_in_the_requested_sections(self):
        body = ('<h2 id="b5">실행 예제</h2>{{notebook:test|example}}'
                '<h2 id="b6">일부러 실패해 보기</h2>{{notebook:test|failure}}')
        result = self.expand(paired_notebook(), body)
        example, failure = result.split('<h2 id="b6">', 1)
        self.assertEqual(example.count('class="language-python nb-source"'), 1)
        self.assertEqual(failure.count('class="language-python nb-source"'), 2)
        self.assertIn('data-lesson-stage="before"', failure)
        self.assertIn('data-lesson-stage="after"', failure)
        self.assertIn('Before', failure)
        self.assertIn('After', failure)
        self.assertEqual(result.count('class="copy-all"'), 1)
        self.assertEqual(result.count('download="test.ipynb"'), 1)

    def test_missing_or_repeated_half_is_rejected(self):
        for body in ['{{notebook:test|example}}', '{{notebook:test|failure}}',
                     '{{notebook:test|example}}{{notebook:test|example}}{{notebook:test|failure}}']:
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.expand(paired_notebook(), body)

    def test_inverted_or_missing_repair_is_rejected(self):
        for stage in ['before', 'example']:
            nb = paired_notebook()
            nb['cells'][-1]['metadata']['lesson_part'] = stage
            with self.subTest(stage=stage), self.assertRaises(ValueError):
                self.expand(nb, '{{notebook:test|example}}{{notebook:test|failure}}')

    def test_empty_result_is_not_evidence_of_a_repair(self):
        nb = paired_notebook()
        nb['cells'][-1]['outputs'][0]['text'] = ''
        nb['metadata']['verification']['outputs_sha256'] = output_hash(nb)
        with self.assertRaisesRegex(ValueError, 'observed output'):
            self.expand(nb, '{{notebook:test|example}}{{notebook:test|failure}}')

    def test_experiment_uses_one_unsplit_token_without_stages(self):
        nb = notebook()
        nb['metadata']['lesson_format'] = 'experiment'
        result = self.expand(nb, '{{notebook:test}}')
        self.assertIn('data-lesson-format="experiment"', result)
        self.assertNotIn('data-lesson-stage=', result)
        self.assertEqual(result.count('class="language-python nb-source"'), 1)

    def test_experiment_rejects_split_tokens_and_before_cells(self):
        nb = notebook()
        nb['metadata']['lesson_format'] = 'experiment'
        with self.assertRaisesRegex(ValueError, 'unsplit'):
            self.expand(nb, '{{notebook:test|example}}{{notebook:test|failure}}')
        nb = paired_notebook()
        nb['metadata']['lesson_format'] = 'experiment'
        with self.assertRaisesRegex(ValueError, 'only example'):
            self.expand(nb, '{{notebook:test}}')
