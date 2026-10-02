import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]


def find_function(tree: ast.Module, function_name: str):
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    for function in functions:
        if function.name == function_name:
            return function
    return None


def imports_from_tools(tree: ast.Module, function_name: str) -> bool:
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "llm_tools":
            if function_name in [alias.name for alias in node.names]:
                return True
    return False


def load_function(notebook_path: Path, function_name: str):
    # 노트북 코드 셀에서 함수 정의를 찾습니다. §2-7 리팩터(2026-09-21) 뒤에는 앞에서 배운 함수를
    # 노트북 폴더의 도구 파일 llm_tools.py에서 가져오므로, 노트북이 그 이름을 llm_tools에서 가져오면
    # 도구 파일의 정의를 읽습니다. 가져오지도 정의하지도 않으면 실패합니다.
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    namespace = {}
    imported = False
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        try:
            tree = ast.parse("".join(cell["source"]))
        except SyntaxError:  # Jupyter의 %pip 매직은 Python AST 대상이 아닙니다.
            continue
        function = find_function(tree, function_name)
        if function is not None:
            exec(compile(ast.Module([function], []), str(notebook_path), "exec"), namespace)
            return namespace[function_name]
        imported = imported or imports_from_tools(tree, function_name)
    tools_path = notebook_path.parent / "llm_tools.py"
    if imported and tools_path.exists():
        function = find_function(ast.parse(tools_path.read_text(encoding="utf-8")), function_name)
        if function is not None:
            exec(compile(ast.Module([function], []), str(tools_path), "exec"), namespace)
            return namespace[function_name]
    raise AssertionError(f"{function_name} not found in {notebook_path} or its llm_tools.py import")


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


def code_source(notebook_path: Path) -> str:
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    return "\n".join("".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "code")


def test_log_paths_are_portable_from_student_working_directories():
    # 학생 노트북은 기본 경로 문법 사다리(A 트랙) 때문에 Path·next·내포식을 쓰지 않고,
    # 작업 폴더에서 본 상대 경로를 os.path.exists로 고릅니다(품질 개선 2026-09-17).
    # 이 테스트는 노트북이 그 방식을 쓰는지와, 그 상대 경로가 설명한 작업 폴더에서 실제 runs를 가리키는지 확인합니다.
    # Ch 6 06·Ch 7 08: notebooks 폴더("../runs")와 프로젝트 맨 위(긴 경로)만 지원합니다.
    # 실습 폴더 맨 위에서 열면 두 경로가 모두 없어 멈추는 것은 알려진 제한 R-1입니다(Ch 7 요약 §9).
    for chapter, notebook in [
        ("ch06-langchain-start", "06-토큰-비용-지연-비교.ipynb"),
        ("ch07-prompt-engineering", "08-프롬프트-버전과-AB-비교.ipynb"),
    ]:
        path = ROOT / "labs/part2" / chapter / "notebooks" / notebook
        source = code_source(path)
        assert 'os.path.exists("../runs")' in source
        assert f'"labs/part2/{chapter}/runs' in source
        assert (path.parent / "../runs").resolve() == (ROOT / "labs/part2" / chapter / "runs")
        assert (ROOT / "labs/part2" / chapter / "runs").is_dir()

    # Ch 8 06: 후보 세 개 가운데 runs·notebooks 폴더가 모두 있는 첫 후보를 고르므로
    # notebooks 폴더·실습 폴더 맨 위·프로젝트 맨 위 세 곳에서 모두 같은 실습 폴더를 찾습니다(R-1 해소).
    lab = ROOT / "labs/part2/ch08-context-engineering"
    source = code_source(lab / "notebooks/06-단계적-공개와-설계-비교.ipynb")
    candidates = ["labs/part2/ch08-context-engineering", "..", "."]
    assert 'for candidate in ["labs/part2/ch08-context-engineering", "..", "."]:' in source
    assert 'os.path.exists(candidate + "/runs")' in source
    assert 'os.path.exists(candidate + "/notebooks")' in source
    assert 'lab_folder + "/../ch07-prompt-engineering/runs/prompt-ab-continuity.json"' in source
    assert 'lab_folder + "/runs/context-design-continuity.json"' in source
    for cwd in [lab / "notebooks", lab, ROOT]:
        found = None
        for candidate in candidates:
            if (cwd / candidate / "runs").is_dir() and (cwd / candidate / "notebooks").is_dir():
                found = cwd / candidate
                break
        assert found is not None and found.resolve() == lab.resolve()
        ch07_file = found / "../ch07-prompt-engineering/runs/prompt-ab-continuity.json"
        assert ch07_file.resolve() == ROOT / "labs/part2/ch07-prompt-engineering/runs/prompt-ab-continuity.json"


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
