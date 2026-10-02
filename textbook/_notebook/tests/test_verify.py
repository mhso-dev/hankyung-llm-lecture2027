"""Regression coverage for student-facing import boundaries."""
import ast
import base64
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify import Cells, check_failure_section, check_imports


class DownloadTests(unittest.TestCase):
    def test_bundle_link_does_not_replace_notebook_download(self) -> None:
        notebook = {"cells": [], "nbformat": 4}
        encoded = base64.b64encode(json.dumps(notebook).encode()).decode()
        notebook_link = f'<a download="lesson.ipynb" href="data:application/json;base64,{encoded}">Notebook</a>'
        bundle_link = '<a download href="../../downloads/llm-practice.zip">Files</a>'
        for links in [notebook_link + bundle_link, bundle_link + notebook_link]:
            parser = Cells()
            parser.feed(links)
            self.assertEqual(parser.download, notebook)


class ImportBoundaryTests(unittest.TestCase):
    def check(self, source: str) -> None:
        check_imports(ast.parse(source), Path("lesson.ipynb"))

    def test_plain_project_imports_are_rejected(self) -> None:
        for source in ["import context_lab", "import rag as lesson", "import harness.tools"]:
            with self.subTest(source=source), self.assertRaises(AssertionError):
                self.check(source)

    def test_from_project_imports_are_rejected(self) -> None:
        for source in ["from context_lab import build", "from experiment.cache import load"]:
            with self.subTest(source=source), self.assertRaises(AssertionError):
                self.check(source)

    def test_direct_sdk_imports_are_rejected(self) -> None:
        for source in ["import openai as api", "from openai import OpenAI"]:
            with self.subTest(source=source), self.assertRaises(AssertionError):
                self.check(source)

    def test_langchain_and_standard_library_imports_are_allowed(self) -> None:
        self.check("from langchain.chat_models import init_chat_model\n"
                   "from langchain_openai import OpenAIEmbeddings\n"
                   "import json, pathlib")

    def test_ch18_direct_sdk_curriculum_exception(self) -> None:
        path = Path('labs/part5/ch18-workflow-patterns/notebooks/01-example.ipynb')
        for source in ('import openai as api', 'from openai import OpenAI, AsyncOpenAI'):
            check_imports(ast.parse(source), path)
        for source in ('import langchain', 'from langgraph.graph import StateGraph',
                       'from langchain_openai import ChatOpenAI', 'import harness'):
            with self.subTest(source=source), self.assertRaises(AssertionError):
                check_imports(ast.parse(source), path)

    def test_ch18_exception_does_not_apply_to_other_folders(self) -> None:
        for folder in ('labs/part4/ch18-workflow-patterns/notebooks',
                       'labs/part5/ch19-model-tools/notebooks',
                       'labs/part5/ch18-workflow-patterns-other/notebooks',
                       'labs/part5/ch18-workflow-patterns/notebooks/../../ch19-model-tools/notebooks'):
            with self.subTest(folder=folder), self.assertRaises(AssertionError):
                check_imports(ast.parse('import openai'), Path(folder) / '01-example.ipynb')


class ExperimentSectionTests(unittest.TestCase):
    def test_result_interpretation_has_no_code_or_pair_stages(self) -> None:
        nb = {"metadata": {"lesson_format": "experiment"}, "cells": []}
        page = Path("experiment.html")
        valid = '<h2 id="b6">결과 해석</h2><p>반복 측정값을 비교합니다.</p><h2 id="b7">주의</h2>'
        check_failure_section(nb, valid, page)
        for invalid in [
            '<h2 id="b6">결과 해석</h2><code class="language-python nb-source">print(1)</code><h2 id="b7">주의</h2>',
            '<h2 id="b6">결과 해석</h2><div data-lesson-stage="before"></div><h2 id="b7">주의</h2>',
        ]:
            with self.subTest(invalid=invalid), self.assertRaises(AssertionError):
                check_failure_section(nb, invalid, page)
