import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]


def load_function(notebook_path: Path, function_name: str):
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    namespace = {}
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        try:
            tree = ast.parse("".join(cell["source"]))
        except SyntaxError:  # Jupyter의 %pip 매직은 Python AST 대상이 아닙니다.
            continue
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        for function in functions:
            if function.name == function_name:
                exec(compile(ast.Module([function], []), str(notebook_path), "exec"), namespace)
                return namespace[function_name]
    raise AssertionError(f"{function_name} not found in {notebook_path}")


def test_cached_input_cost_is_separated_in_all_three_chapters():
    usage = {
        "input_tokens": 100,
        "output_tokens": 10,
        "input_token_details": {"cache_read": 40},
    }
    ch06 = load_function(
        ROOT / "labs/part2/ch06-langchain-start/notebooks/06-토큰-비용-지연-비교.ipynb",
        "estimate_cost",
    )
    assert ch06(usage, 0.75, 0.075, 4.50) == 0.000093
    for chapter, notebook in [
        ("ch07-prompt-engineering", "08-프롬프트-버전과-AB-비교.ipynb"),
        ("ch08-context-engineering", "06-단계적-공개와-설계-비교.ipynb"),
    ]:
        estimate = load_function(ROOT / f"labs/part2/{chapter}/notebooks/{notebook}", "estimate_openai_cost")
        assert estimate(usage) == 0.000093


def test_ch08_source_ids_match_preserved_memory():
    memory = json.loads(
        (ROOT / "labs/part2/ch08-context-engineering/data/memory.json").read_text(encoding="utf-8")
    )
    expected = {row["doc_id"]: row["text"] for row in memory}
    for name in ["02-Write와-Select.ipynb", "06-단계적-공개와-설계-비교.ipynb"]:
        source = (ROOT / "labs/part2/ch08-context-engineering/notebooks" / name).read_text(encoding="utf-8")
        assert "90분 무료" not in source
        assert expected["E01-p5"] in source
    compress_source = (ROOT / "labs/part2/ch08-context-engineering/notebooks/03-Compress와-Isolate.ipynb").read_text(encoding="utf-8")
    assert "임시 휴관은 별도 공지" not in compress_source
    assert "성인 회원 1명 기준" not in compress_source
    assert "공휴일이 월요일과 겹치면 다음 화요일도 휴관" in compress_source
    assert "회원 한 사람의 도서 대출 기준" in compress_source


def test_legacy_logs_are_unchanged():
    expected = {
        "labs/part2/ch07-prompt-engineering/runs/prompt-ab-v1.json": "16a4b67210853c925e75ced02cc88fa704957aa196a2572a05f8fce49fbf4341",
        "labs/part2/ch08-context-engineering/runs/ex01_budget.jsonl": "e3b6a71d178c73157c9a142ef2bda0bdb45d37a63d3b7899a2659e2c9892f70f",
        "labs/part2/ch08-context-engineering/runs/ex04_failures.jsonl": "d23dbb45347449ffa19b5d1f90fb116e2c413bbb25286132dda7bd012eef3394",
        "labs/part2/ch08-context-engineering/runs/ex05_rot.jsonl": "6a9db92797954f446e2663f9c73a3dbe62aef4d97ae545857ce7dc27acd9db00",
        "labs/part2/ch08-context-engineering/runs/ex06_compare.jsonl": "5cb060d68bafe10ada1dd5378b1355996b66361b7d67e7e864c75a38bbdc5c0c",
    }
    for relative, digest in expected.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest


def test_log_paths_are_portable_from_student_working_directories():
    cases = [
        ("ch06-langchain-start", "06-토큰-비용-지연-비교.ipynb"),
        ("ch07-prompt-engineering", "08-프롬프트-버전과-AB-비교.ipynb"),
        ("ch08-context-engineering", "06-단계적-공개와-설계-비교.ipynb"),
    ]
    for chapter, notebook in cases:
        path = ROOT / "labs/part2" / chapter / "notebooks" / notebook
        source = path.read_text(encoding="utf-8")
        assert "[Path.cwd(), *Path.cwd().parents]" in source
        assert "runs_dir = course_root" in source
        for cwd in [path.parent, path.parent.parent]:
            found = next(
                (candidate for candidate in [cwd, *cwd.parents] if (candidate / "labs/part2").is_dir()),
                None,
            )
            assert found == ROOT


def test_continuity_logs_form_a_hash_verified_chain():
    ch06_path = ROOT / "labs/part2/ch06-langchain-start/runs/provider-comparison-continuity.json"
    ch07_path = ROOT / "labs/part2/ch07-prompt-engineering/runs/prompt-ab-continuity.json"
    ch08_path = ROOT / "labs/part2/ch08-context-engineering/runs/context-design-continuity.json"
    ch06 = json.loads(ch06_path.read_text(encoding="utf-8"))
    ch07 = json.loads(ch07_path.read_text(encoding="utf-8"))
    ch08 = json.loads(ch08_path.read_text(encoding="utf-8"))
    assert ch07["source_record"]["run_id"] == ch06["run_id"]
    assert ch07["source_record"]["sha256"] == hashlib.sha256(ch06_path.read_bytes()).hexdigest()
    assert ch08["source_record"]["run_id"] == ch07["run_id"]
    assert ch08["source_record"]["sha256"] == hashlib.sha256(ch07_path.read_bytes()).hexdigest()
    pricing = {"ordinary_input": 0.75, "cached_input": 0.075, "output": 4.50}
    assert ch06["pricing"]["openai"] == pricing
    assert ch07["settings"]["pricing_usd_per_million"] == pricing
    assert ch08["settings"]["pricing_usd_per_million"] == pricing
    assert len(ch07["versions"]) == 3
    assert len(ch08["results"]) == 3
