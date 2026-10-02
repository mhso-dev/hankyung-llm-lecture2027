"""Ch 29 04절 품질 개선본 생성기 (QUALITY-UPGRADE.md §2·§2-7·§3·§4·§6).

사용:
  python3 -B author_04.py              → 도구 파일(가드) + 노트북 + _src 본문을 다시 쓴다(노트북 출력이 지워지므로 새 커널로 다시 실행)
  python3 -B author_04.py --src-only   → _src 본문만 다시 쓴다(노트북·도구 파일은 그대로)
  python3 -B author_04.py --tools-copy DIR → 디스크의 도구 파일을 DIR에 복사한다(새 커널 사본 B 실행용)
  python3 -B author_04.py --try DIR    → 노트북과 이 판 도구 파일을 DIR에만 쓴다(실습 폴더를 건드리지 않는 시험 실행·묶음 확인용)
이후 run_section.sh 가 새 커널 실행 → Mermaid 렌더 → 그림 첨부 → 빌드 → verify → 게이트를 잇는다.
수정 전 노트북·본문은 qa/upgrade/before/ 에 있다(준비 담당이 복사). **experiment 형식 유지**.
슬러그 `04-운영-지표와-Ch18-궤적-비교` 고정(Ch 21 06 b2가 링크). 제목 「Ch18 궤적」은 제목에만 — 본문은 Ch 18 기록에 도구 차례가 없다고 밝힘(강사 확인).

## 결정 1 — 모델 없음, 계약 파일 둘을 읽기만 (챕터 리드 결정 1·3, handoff §03 → §04)

Ch 18 06 노트북(`5ba7f5a0…`)은 실행하지 않고 **저장된 출력**의 「 | 」 줄(머리 `pattern` 뺌) 마지막 다섯을 여섯 칸으로 읽는다
(Ch 18 06 b7 「Ch 29 04절이 저장된 출력에서 읽습니다」). Ch 21 06 `data/rag-comparison.json`(`25cfe5df…`)은 줄 셋을 읽는다.
모델 요청 0 · 키 셀·dotenv 없음 · 파일 쓰기 0. 파일 찾기는 Ch 21 06 author_06.py ROOT_FIND 모양(candidates 세 자리 + for·break + assert) —
`textbook/`·`커리큘럼_v6.html`에 기대지 않아 학생 묶음(`notebooks/`에서 열면 `../../../..`)에서도 돈다.

## 결정 2 — 공통 칸 여섯 (이름·요청 수·도구 요청 수·토큰 수·걸린 초·점수)

Ch 18 도구 요청 수는 기록에 칸이 없어 `None`(옛 판의 손 값 0을 쓰지 않음 — 과정 「모르는 값 None」). 점수 = Ch 18 품질 ÷ 만점 5(코드 검사) ·
Ch 21 `float(agent_supported)`(평가 모델 판정) — 잣대가 달라 본문에서 밝히고 견주지 않는다. `model_calls`·`tool_calls`·`agent_latency_s`는 Ch 21 06이 적은 이름 그대로 읽는다.

## 결정 3 — 결론은 세는 값, 걸린 초·토큰 수는 표·결과 읽기 둘째 단락·b7에만

결론·그림·정리·복습: 줄 수(5·3)·상태 ok 5/5·품질 만점 4/5·요청 수(2·2·3·5·2 / 2·2·2)·03절 셈(요청 수 = 도구 요청 수 + 1, 세 줄 True)·검색 기록 수 = 도구 요청 수·
95 백분위수 자리(줄 셋이면 3 = 가장 큰 값, 줄 수 표 3·5·19·20·100)·값 바꿔 보기(백분위 50 → 자리 2).
걸린 초·토큰 수(평균 862.2·4.206 / 688.0·1.731, 95 백분위수 2.003·699)는 「각 기록이 한 번 실행한 값」 한정과 함께 표·둘째 단락·b7에만 — 순위 없음.
`assert`는 기록 모양(Ch 18 표 줄 ≥ 5·상태 ok 전부·Ch 21 줄 3·줄마다 도구 요청 수 ≥ 1)에만, 걸린 초·토큰에는 걸지 않는다.

## 결정 4 — 도구 파일 eval_tools.py 04절 판 (handoff §03 → §04 8번)

03판 뒤에 Ch 15 06 노트북 셀 `average`(셀 43)·`nearest_rank`(셀 49)를 셀의 주석과 본문 글자 그대로 더한다
(주석 `# Ch 15 06절에서 배웠습니다 — Ch 15 06절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다`, `nearest_rank_p95` 새 이름 없음).
`nearest_rank`가 `math.ceil`을 써서 가져오기 줄 `import math`를 머리 설명과 첫 `# Ch` 주석 사이(02판 가져오기 줄 뒤)에 둔다.
대조 사슬: author_03.check_tools()(안에서 02·01까지) → strip_later_imports(04판).startswith(strip_later_imports(03판)) → 셀 글 해시·Ch 15 노트북 디스크 셀·AST
→ `average`는 Ch 15 rag_tools.py 판과 AST 같음. 쓰기 가드: 없거나 01·02·03판·이 판일 때만 쓰고 더 긴 판은 skip. 01·02·03 생성기가 이 판을 skip하는지 판정만 흉내 낸다.
04판을 가져오는 노트북(01~04)은 `math`가 표준 라이브러리라 설치 셀 변경 없음. 04 설치 셀은 도구 파일이 가져오는 `langchain==1.4.0` 하나.

## 쓰지 않은 것

f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`next`·`all`·`any`·`sum`·`max`·`min`·`enumerate`·`zip`·`getattr`·`statistics`·
`key=`·`reverse=`·`set`·`setdefault`·노트북 `.get`·`.items`·`+=`·기본값 매개변수·힌트·대입 풀기·별표 풀기·`while`·`try`·
세미콜론·`isinstance`·클래스·데코레이터·`async`. 호출 깊이 2 이하. 앞에서 가르친 이름만: `json.loads`·`with open`(Ch 21 06)·`os.path.exists`(자리 찾기 셀)·
`join`(Ch 16 01)·`splitlines`·`startswith`(03)·`strip`·`split`·`sorted`(Ch 6 06·Ch 15 06)·`math.ceil`(Ch 15 06)·`round`·`float`·음수 슬라이스(Ch 16 03).
`float(참·거짓 값)`은 처음이라 한 문장으로 푼다.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
sys.path.insert(0, str(HERE))
import author_01  # noqa: E402  01절 도구 파일 01판·본문 도우미
import author_02  # noqa: E402  02절 가져오기 줄·도구 파일 02판
import author_03  # noqa: E402  03절 도구 파일 03판
from nbkit import code, install_source, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part6/ch29-agent-evaluation/notebooks"
FIGS = ROOT / "textbook/part6/ch29-agent-evaluation/figures"
SLUG = "04-운영-지표와-Ch18-궤적-비교"
TITLE_TEXT = "운영 지표와 Ch18 궤적 비교"
SRC = ROOT / "textbook/part6/ch29-agent-evaluation/_src" / (SLUG + ".html")
TOOLS_PATH = LAB / "eval_tools.py"
NB15 = ROOT / "labs/part4/ch15-evaluation-advanced/notebooks/06-대화당-비용-백분위수.ipynb"
NB15_SHA = "b688b514f7bed500222622b2489b0d0e6483e89fcf184ac9cd3ea6d73ca976d5"
RAG15 = ROOT / "labs/part4/ch15-evaluation-advanced/notebooks/rag_tools.py"
RAG15_SHA = "6c59d0f239370dbc208a7ca2be71fbe2147574e2ea13d5d044ce0ced5afdbea1"
CONTRACTS = {
    ROOT / "labs/part6/ch21-create-agent/data/rag-comparison.json": "25cfe5df3cfd729c130bce4af26c716cfcc3bcd4b4ff6e4a9d0a725816b02f51",
    ROOT / "labs/part5/ch18-workflow-patterns/notebooks/06-같은-과제로-다섯-패턴-비교.ipynb": "5ba7f5a01fa8a8625a4673e6f6a007691907078b20c41ee828aa266252ba0b20",
}
RUNS_SENTENCE = os.environ.get("AUTHOR04_RUNS_SENTENCE", "새 커널로 두 번 실행해 견주자, 코드 셀 스물다섯의 출력이 셀마다 모두 같았습니다. 이 절은 모델을 부르지 않고 저장된 기록만 읽어, 앞 챕터를 다시 실행하지 않는 한 같은 값이 나옵니다.")
html_text = author_01.html_text
table_html = author_01.table_html


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------- 도구 파일 eval_tools.py (04절 판)
NOTE_15 = "Ch 15 06절에서 배웠습니다 — Ch 15 06절 노트북 셀의 주석과 본문을 글자 그대로 옮겼습니다"
MATH_IMPORT = "# 04절에서 옮긴 함수 nearest_rank(Ch 15 06절)가 쓰는 올림 함수 math.ceil의 모듈을 가져옵니다\nimport math\n"
CELLS_15 = [
    ("average", "2cf4a63e544d3ec4160f0f2dbca6ee34f4fdf6791a44b9509c9dc6c827aabb63"),
    ("nearest_rank", "11176f41d723eb79c2030f1985694f10e63d0b872770de4c2b638715753f9d7b"),
]
TOOL_ORDER = author_03.TOOL_ORDER + ["average", "nearest_rank"]
IMPORT_LINES = author_02.IMPORT_LINES + ["import math"]
HEAD = author_01.TOOLS_HEAD + author_02.TOOLS_IMPORTS


def ch15_cell(name: str) -> str:
    """Ch 15 06절 노트북에서 함수 name을 정의한 코드 셀 글을 그대로 꺼냅니다(읽기만)."""
    found = []
    for source in author_03.notebook_code_sources(NB15):
        if ("def " + name + "(") in source:
            found.append(source)
    assert len(found) == 1, name
    return found[0]


def tools_text() -> str:
    assert file_sha(NB15) == NB15_SHA, "Ch 15 06절 노트북이 마감 판과 다릅니다"
    assert author_03.TOOLS.startswith(HEAD), "03판 머리가 예상과 다릅니다"
    text = HEAD + MATH_IMPORT + author_03.TOOLS[len(HEAD):]
    for name, cell_sha in CELLS_15:
        text = text + "\n\n# " + NOTE_15 + "\n" + ch15_cell(name) + "\n"
    return text


TOOLS = tools_text()


def check_tools() -> None:
    """04절 판이 03절 판(대조 사슬)으로 시작하고, 더한 함수 둘이 Ch 15 06절 노트북 셀과 글자·AST 모두 같은지 봅니다."""
    author_03.check_tools()
    strip = author_01.strip_later_imports
    assert strip(TOOLS).startswith(strip(author_03.TOOLS)), "04절 판이 03절 판으로 시작하지 않습니다"
    # 전체 마감(2026-09-30)에서 도구 파일 머리 설명 줄만 고쳐 03판 617a82bc… → b1fd3492…(함수 본문 같음)
    assert sha(author_03.TOOLS) == "b1fd3492ca3714242acd200bdc34baa730ad80bc43f58c37125fe0356f25f721", "03판이 기록 해시와 다릅니다"
    assert TOOLS.startswith(HEAD + MATH_IMPORT + author_03.TOOLS[len(HEAD):])
    tree = ast.parse(TOOLS)
    names = []
    imports = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.append(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
    assert names == TOOL_ORDER, names
    assert imports == IMPORT_LINES, imports
    # 가져오기 줄 주석이 # Ch 로 시작하지 않아야 strip_later_imports가 첫 함수 주석까지 뺀다
    assert not MATH_IMPORT.startswith("# Ch")
    # Ch 15 06절 노트북 셀 둘: 고정 해시 · 디스크 셀 · AST
    nb15 = author_03.notebook_code_sources(NB15)
    rag = RAG15.read_text(encoding="utf-8")
    assert file_sha(RAG15) == RAG15_SHA, "Ch 15 rag_tools.py가 마감 판과 다릅니다"
    rag_tree = ast.parse(rag)
    for name, cell_sha in CELLS_15:
        cell = ch15_cell(name)
        assert sha(cell) == cell_sha, name + " 셀 글이 고정 해시와 다릅니다"
        assert cell in nb15
        assert ("# " + NOTE_15 + "\n" + cell + "\n") in TOOLS
        mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        theirs = [ast.dump(n) for n in ast.parse(cell).body if isinstance(n, ast.FunctionDef)]
        assert mine == theirs and len(mine) == 1, name
    # average는 Ch 15 도구 파일 rag_tools.py 판과도 본문이 같음(nearest_rank는 Ch 15 도구 파일에 없음)
    mine = [ast.dump(n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "average"]
    theirs = [ast.dump(n) for n in rag_tree.body if isinstance(n, ast.FunctionDef) and n.name == "average"]
    assert mine == theirs and len(mine) == 1, "average가 Ch 15 rag_tools.py 판과 다릅니다"
    none = [n for n in rag_tree.body if isinstance(n, ast.FunctionDef) and n.name == "nearest_rank"]
    assert not none
    # 앞 절 생성기의 쓰기 가드가 이 판을 덮어쓰지 않는지(판정만 흉내 — 실행하지 않음)
    assert author_03.later_version(TOOLS), "03 생성기가 이 판을 skip하지 않습니다"
    assert author_02.later_version(TOOLS), "02 생성기가 이 판을 skip하지 않습니다"
    assert strip(TOOLS).startswith(author_01.TOOLS) and TOOLS != author_01.TOOLS, "01 생성기가 이 판을 skip하지 않습니다"


def check_contracts() -> None:
    """계약 파일 둘이 기록 해시 그대로인지 봅니다(읽기만 — 이 생성기와 노트북은 두 파일을 쓰지 않음)."""
    for path in CONTRACTS:
        assert file_sha(path) == CONTRACTS[path], str(path) + " 해시가 계약과 다릅니다"


def later_version(current: str) -> bool:
    """뒤 절이 함수·가져오기 줄을 더한 판인지: 가져오기 줄을 뺀 글이 이 판(가져오기 줄을 뺀 글)으로 시작하면 참."""
    plain = author_01.strip_later_imports(current)
    return current != TOOLS and plain.startswith(author_01.strip_later_imports(TOOLS))


def write_tools(path: Path) -> None:
    current = ""
    if path.is_file():
        current = path.read_text(encoding="utf-8")
    if current == TOOLS:
        print("same", path)
    elif current in ("", author_01.TOOLS, author_02.TOOLS, author_03.TOOLS):
        path.write_text(TOOLS, encoding="utf-8")
        print("wrote", path)
    elif later_version(current):
        print("skip", path, "(뒤 절이 함수를 더한 판 — 덮어쓰지 않음)")
    else:
        raise AssertionError("도구 파일이 01·02·03·04절 판이 아닙니다")


# ---------------------------------------------------------------- 노트북 코드 셀
INSTALL = install_source(["langchain==1.4.0"])

IMPORTS = r'''# 기록 파일을 찾고 읽는 모듈 둘과, 올림 함수 ceil이 든 모듈 math(Ch 15 06절)를 가져옵니다
import json
import math
import os
# 앞에서 배운 함수는 도구 파일에서 가져옵니다
from eval_tools import average, nearest_rank

print("도구 파일에서 가져온 함수:", "average, nearest_rank")'''

ROOT_FIND = r'''# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part6/ch21-create-agent/data"):
        root_path = candidate
        break
print("고른 자리:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."'''

PATHS = r'''# 두 기록 파일의 자리를 만들고, 둘 다 있는지 봅니다(두 파일은 읽기만 하고 고치지 않습니다)
ch18_path = root_path + "/labs/part5/ch18-workflow-patterns/notebooks/06-같은-과제로-다섯-패턴-비교.ipynb"
ch21_path = root_path + "/labs/part6/ch21-create-agent/data/rag-comparison.json"
print("Ch 18 06절 노트북이 있는가:", os.path.exists(ch18_path))
print("Ch 21 06절 비교 기록이 있는가:", os.path.exists(ch21_path))'''

READ18 = r'''# Ch 18 06절 노트북 파일을 JSON으로 읽습니다(그 노트북은 실행하지 않고, 저장된 출력만 씁니다)
with open(ch18_path, encoding="utf-8") as file:
    ch18_notebook = json.loads(file.read())
print("셀 수:", len(ch18_notebook["cells"]))'''

DEF_PRINTED = r'''# 코드 셀 하나의 저장된 출력 가운데 print로 찍힌 글(stream)만 한 줄씩 나눠 목록으로 내놓습니다
def printed_lines_of(cell):
    lines = []
    for output in cell["outputs"]:
        if output["output_type"] == "stream":
            printed_text = "".join(output["text"])
            for line in printed_text.splitlines():
                lines.append(line)
    return lines'''

COLLECT = r'''# 코드 셀마다 저장된 출력 줄을 모두 모읍니다(마크다운 셀에는 출력이 없어 건너뜁니다)
printed_lines = []
for cell in ch18_notebook["cells"]:
    if cell["cell_type"] == "code":
        for line in printed_lines_of(cell):
            printed_lines.append(line)
print("저장된 출력 줄 수:", len(printed_lines))'''

TABLE_LINES = r'''# 칸 구분 「 | 」가 든 줄 가운데 머리 줄(pattern으로 시작)을 뺀 표 줄만 모읍니다
table_lines = []
for line in printed_lines:
    if " | " in line:
        if not line.startswith("pattern"):
            table_lines.append(line)
print("표 줄 수:", len(table_lines))
assert len(table_lines) >= 5, "Ch 18 06절 노트북에 저장된 비교 표가 다섯 줄보다 적습니다."'''

SHOW_FIVE = r'''# 표 줄 가운데 마지막 다섯 줄을 Ch 18 다섯 흐름의 기록으로 씁니다(칸: 패턴·요청 수·토큰 수·걸린 초·품질·상태)
ch18_lines = table_lines[-5:]
print("Ch 18 표 다섯 줄:")
for line in ch18_lines:
    print(line)'''

DEF_SPLIT = r'''# 표 줄 하나를 「|」로 나누고, 칸마다 앞뒤 빈칸을 뺀 글을 목록으로 내놓습니다
def split_row(line):
    parts = []
    for part in line.split("|"):
        parts.append(part.strip())
    return parts'''

DEF_CH18 = r'''# 나눈 Ch 18 표 줄 하나를 공통 칸 딕셔너리로 옮겨 담아 내놓습니다(도구 요청 수는 기록에 없어 None)
def ch18_row(parts, full_quality):
    return {
        "이름": "Ch 18 " + parts[0],
        "요청 수": int(parts[1]),
        "도구 요청 수": None,
        "토큰 수": int(parts[2]),
        "걸린 초": float(parts[3]),
        "점수": int(parts[4]) / full_quality,
    }'''

BUILD18 = r'''# Ch 18 다섯 줄을 공통 칸으로 옮겨 담고, 상태 칸이 ok인 줄을 셉니다(품질 칸의 만점은 코드 검사 다섯 항목)
full_quality = 5
ch18_rows = []
ok_count = 0
for line in ch18_lines:
    parts = split_row(line)
    ch18_rows.append(ch18_row(parts, full_quality))
    if parts[5] == "ok":
        ok_count = ok_count + 1
print("옮겨 담은 줄 수:", len(ch18_rows), "| 상태가 ok인 줄 수:", ok_count)
assert ok_count == len(ch18_rows), "Ch 18 표에 상태가 ok가 아닌 줄이 있습니다."'''

READ21 = r'''# Ch 21 06절이 쓴 비교 기록 파일을 읽고, 줄 수·한 줄의 칸 수·질문 번호를 봅니다
with open(ch21_path, encoding="utf-8") as file:
    ch21_records = json.loads(file.read())
qids = []
for record in ch21_records:
    qids.append(record["qid"])
print("줄 수:", len(ch21_records), "| 한 줄의 칸 수:", len(ch21_records[0]))
print("질문 번호:", qids)
assert len(ch21_records) == 3, "Ch 21 비교 기록은 질문 세 줄이어야 합니다."'''

DEF_CH21 = r'''# Ch 21 비교 기록 한 줄을 공통 칸 딕셔너리로 옮겨 담아 내놓습니다(점수는 평가 모델 판정 — 참이면 1.0)
def ch21_row(record):
    return {
        "이름": "Ch 21 " + record["qid"],
        "요청 수": record["agent_usage"]["model_calls"],
        "도구 요청 수": record["tool_calls"],
        "토큰 수": record["agent_usage"]["input_tokens"] + record["agent_usage"]["output_tokens"],
        "걸린 초": record["agent_latency_s"],
        "점수": float(record["agent_supported"]),
    }'''

BUILD21 = r'''# Ch 21 세 줄을 공통 칸으로 옮겨 담고, 줄마다 도구 요청 수가 1 이상인지 확인합니다
ch21_rows = []
for record in ch21_records:
    ch21_rows.append(ch21_row(record))
    assert record["tool_calls"] >= 1, "도구를 부르지 않은 줄이 있습니다."
print("옮겨 담은 줄 수:", len(ch21_rows))
print("첫 줄:", ch21_rows[0])'''

DEF_SHOW = r'''# 공통 칸 딕셔너리 한 줄을 「|」로 이은 표 한 줄로 출력합니다(내놓는 값 없음)
def show_row(row):
    print(row["이름"], "|", row["요청 수"], "|", row["도구 요청 수"], "|", row["토큰 수"], "|", row["걸린 초"], "|", row["점수"])'''

TABLE = r'''# 두 기록의 여덟 줄을 공통 칸 표 하나로 출력합니다(걸린 초와 토큰 수는 각 기록이 한 번 실행한 값)
print("이름 | 요청 수 | 도구 요청 수 | 토큰 수 | 걸린 초 | 점수")
for row in ch18_rows:
    show_row(row)
for row in ch21_rows:
    show_row(row)'''

CALLS21 = r'''# 03절의 요청 수 셈(도구를 요청한 응답 수 + 1)이 Ch 21 세 줄에 맞는지, 검색 기록 수도 함께 봅니다
print("질문 | 요청 수 | 도구 요청 수 | 요청 수 = 도구 요청 수 + 1 | 검색 기록 수")
for record in ch21_records:
    calls = record["agent_usage"]["model_calls"]
    tools = record["tool_calls"]
    searches = len(record["agent_trace"])
    print(record["qid"], "|", calls, "|", tools, "|", calls == tools + 1, "|", searches)'''

SUCCESS = r'''# 두 기록이 잘됐다고 적은 줄을 기록마다 제 잣대로 셉니다(Ch 18은 상태·품질 칸, Ch 21은 평가 모델 판정)
full_count = 0
for row in ch18_rows:
    if row["점수"] == 1.0:
        full_count = full_count + 1
supported_count = 0
for record in ch21_records:
    if record["agent_supported"]:
        supported_count = supported_count + 1
print("Ch 18 상태가 ok인 줄:", ok_count, "| 품질이 만점인 줄:", full_count, "| 전체:", len(ch18_rows))
print("Ch 21 평가 모델 판정이 참인 줄:", supported_count, "| 전체:", len(ch21_rows))'''

DEF_COLUMN = r'''# 공통 칸 딕셔너리 목록에서 칸 이름 하나의 값만 차례대로 모아 목록으로 내놓습니다
def column_values(rows, key):
    values = []
    for row in rows:
        values.append(row[key])
    return values'''

MEAN18 = r'''# Ch 18 다섯 줄에서 칸마다 값을 모아 평균을 냅니다(Ch 15 06절 함수 average, 소수 셋째 자리까지)
print("Ch 18 다섯 줄의 평균:")
for key in ["요청 수", "점수", "토큰 수", "걸린 초"]:
    values = column_values(ch18_rows, key)
    mean_value = round(average(values), 3)
    print(key, "|", mean_value)'''

MEAN21 = r'''# Ch 21 세 줄에서도 칸마다 평균을 냅니다(도구 요청 수 칸은 이 기록에만 있습니다)
print("Ch 21 세 줄의 평균:")
for key in ["요청 수", "도구 요청 수", "점수", "토큰 수", "걸린 초"]:
    values = column_values(ch21_rows, key)
    mean_value = round(average(values), 3)
    print(key, "|", mean_value)'''

P95 = r'''# Ch 21 세 줄의 걸린 초와 토큰 수를 줄 세워 보고, 95 백분위수를 찾습니다(Ch 15 06절 함수 nearest_rank)
percent = 95
ch21_seconds = column_values(ch21_rows, "걸린 초")
ch21_tokens = column_values(ch21_rows, "토큰 수")
rank = math.ceil(percent * len(ch21_seconds) / 100)
print("95 백분위수 자리:", rank, "| 줄 수:", len(ch21_seconds))
print("줄 세운 걸린 초:", sorted(ch21_seconds))
print("95 백분위수 걸린 초:", nearest_rank(ch21_seconds, percent))
print("줄 세운 토큰 수:", sorted(ch21_tokens))
print("95 백분위수 토큰 수:", nearest_rank(ch21_tokens, percent))'''

RANK = r'''# 줄 수마다 95 백분위수가 몇 번째 자리인지 셉니다(자리 = 95 × 줄 수 ÷ 100을 올린 정수)
print("줄 수 | 95 백분위수 자리 | 가장 큰 값의 자리인가")
for row_count in [3, 5, 19, 20, 100]:
    rank = math.ceil(percent * row_count / 100)
    print(row_count, "|", rank, "|", rank == row_count)'''

P50 = r'''# 값 바꿔 보기: 백분위 하나만 95에서 50으로 바꿔, 같은 세 줄에서 자리와 값을 봅니다
changed_percent = 50
changed_rank = math.ceil(changed_percent * len(ch21_seconds) / 100)
print("50 백분위수 자리:", changed_rank)
print("50 백분위수 걸린 초:", nearest_rank(ch21_seconds, changed_percent))
print("50 백분위수 토큰 수:", nearest_rank(ch21_tokens, changed_percent))'''


# ---------------------------------------------------------------- 그림 (설계표 qa/upgrade/04-figures.md)
FIG1 = "04-1-두-기록을-같은-칸으로"
FIG1_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 둘은 앞 챕터가 남긴 기록입니다. 왼쪽 상자는 Ch 18 06절 노트북에 저장된 비교 표 다섯 줄로, 칸 calls·tokens·latency_s·quality/5·status가 있습니다. 오른쪽 상자는 Ch 21 06절 비교 기록 파일로, 질문 세 줄에 칸 열둘이 있고 model_calls·tool_calls·agent_latency_s 등이 적혀 있습니다. 왼쪽 상자는 파란 상자 ch18_row, 도구 요청 수는 None, 점수는 품질 ÷ 5로 이어집니다. 오른쪽 상자는 파란 상자 ch21_row, 점수는 평가 모델 판정, 참이면 1.0으로 이어집니다. 두 파란 상자는 맨 아래 노란 상자 공통 칸 표 여덟 줄로 모이고, 칸은 이름·요청 수·도구 요청 수·토큰 수·걸린 초·점수인 그림"
FIG1_CAP = "칸 이름이 다른 두 기록을 함수 둘로 옮겨 담자, 공통 칸 여섯의 표 여덟 줄이 되었습니다."
FIG1_READ = """위에서 아래로 읽습니다.
초록 상자 둘은 앞 챕터가 남긴 기록이고, 파란 상자 둘은 이 노트북 4절에서 정의한 함수입니다.
노란 상자는 4절에서 출력한 공통 칸 표입니다.
Ch 18 쪽 도구 요청 수는 기록에 칸이 없어 None으로 두었습니다.
칸 점수는 두 기록의 잣대가 서로 달라, 두 쪽을 견주지 않습니다."""

FIG2 = "04-2-저장된-출력에서-표-줄-찾기"
FIG2_ALT = "위에서 아래로 한 줄로 이어지는 흐름도입니다. 맨 위 초록 상자 Ch 18 06절 노트북 파일, 셀 쉰여덟, 실행하지 않음에서 파란 상자 printed_lines_of, 코드 셀의 stream 출력만 한 줄씩 모음으로 갑니다. 이어서 노란 상자 저장된 출력 줄 예순아홉, 파란 상자 칸 구분이 든 줄만 남기고 머리 줄 pattern은 뺌, 노란 상자 표 줄 다섯으로 이어집니다. 표 줄 다섯 상자에는 chaining·routing·parallel·orchestrator_worker·generator_evaluator가 적혀 있습니다. 다시 파란 상자 split_row와 ch18_row, 상태 칸 ok 세기를 지나 노란 상자 상태가 ok인 줄 다섯, assert 통과로 끝나는 그림"
FIG2_CAP = "저장된 출력 줄 예순아홉에서 표 줄 다섯을 찾았고, 다섯 줄 모두 상태가 ok였습니다."
FIG2_READ = """위에서 아래로 읽습니다.
초록 상자는 읽기만 하는 Ch 18 06절 노트북 파일이고, 파란 상자 셋은 이 노트북 3·4절의 코드입니다.
노란 상자 셋은 3·4절 셀 출력입니다.
표 줄은 그 노트북이 비교 표를 찍은 셀의 저장된 출력에서 나왔습니다.
그 노트북을 실행하지 않아, 모델 요청은 한 번도 나가지 않습니다."""

FIG3 = "04-3-세는-값으로-읽기"
FIG3_ALT = "두 칸을 왼쪽과 오른쪽에 나란히 둔 그림입니다. 왼쪽 칸 Ch 18 기록 다섯 줄에는 위에서부터 노란 상자 요청 수 2·2·3·5·2번 흐름마다 다름, 노란 상자 상태 ok 다섯 줄 품질 만점 네 줄, 회색 상자 도구 요청 수 기록에 없음 None이 있습니다. 오른쪽 칸 Ch 21 기록 세 줄에는 위에서부터 노란 상자 요청 수 2번씩 도구 요청 1 + 1 세 줄 모두 True, 노란 상자 평가 모델 판정 참 세 줄, 노란 상자 검색 기록 하나씩 도구 요청 수와 같음이 있습니다. 두 칸 사이에는 화살표가 없는 그림"
FIG3_CAP = "이 기록에서 Ch 21 세 줄은 모두 요청 2번 = 도구 요청 1 + 1이었고, Ch 18 다섯 흐름은 요청 수가 흐름마다 달랐습니다."
FIG3_READ = """두 칸을 나란히 읽습니다.
왼쪽 칸은 Ch 18 기록 다섯 줄, 오른쪽 칸은 Ch 21 기록 세 줄의 세는 값입니다.
노란 상자는 노트북 4·5절 셀 출력이고, 회색 상자는 기록에 없어 None으로 둔 칸입니다.
두 칸은 과제가 다르고 저마다 한 번 실행한 기록이라, 화살표 없이 나란히 두었습니다.
상태 칸과 평가 모델 판정은 잣대가 달라, 줄 수를 서로 견주지 않습니다."""

FIG4 = "04-4-95-백분위수의-자리"
FIG4_ALT = "위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 Ch 21 세 줄, 걸린 초와 토큰 수, 작은 값부터 줄 세움에서 파란 상자 둘로 화살표가 갈라집니다. 왼쪽 파란 상자 nearest_rank 백분위 95에서는 아래 노란 상자 자리 3 가장 큰 값으로 화살표가 가고, 점선이 가운데 노란 상자 줄 수 표, 열아홉 줄까지 자리가 줄 수와 같음, 스무 줄에서 자리 19로 이어집니다. 오른쪽 파란 상자 값 바꿔 보기 백분위 50에서는 아래 노란 상자 자리 2 가운데 값으로 화살표가 가는 그림"
FIG4_CAP = "줄이 셋이면 95 백분위수는 자리 3의 가장 큰 값이고, 백분위를 50으로 바꾸자 자리 2의 가운데 값이 나왔습니다."
FIG4_READ = """위에서 아래로 읽습니다.
초록 상자는 Ch 21 세 줄의 값이고, 파란 상자 둘은 노트북 7절의 함수 부르기와 8절에서 바꾼 백분위입니다.
노란 상자는 7·8절 셀 출력입니다.
점선 아래 상자는 같은 셈을 줄 수만 바꿔 센 7절의 표입니다.
걸린 초와 토큰 수의 값은 한 번 실행한 값이라 그림에 넣지 않았습니다."""

ILLU = "04-5-받침대에-걸린-종이띠"
ILLU_ALT = "흰 바탕 위쪽에 가로로 긴 나무 막대 하나가 있고, 막대 아래 작은 고리들에 크림색 종이띠 여덟 개가 곧게 걸려 있습니다. 왼쪽에 띠 다섯이 한 무리로, 오른쪽에 띠 셋이 한 무리로 걸렸고, 두 무리 사이에는 띠가 걸리지 않은 고리 둘이 있는 빈틈이 있습니다. 오른쪽 끝에도 빈 고리가 하나 있습니다. 띠마다 둥근 구멍이 세로로 한 줄 뚫려 있고, 왼쪽 무리의 다섯째 띠는 조금 짧습니다. 사람·손·글자·숫자·음표·화살표는 없는 그림"
ILLU_CAP = "나무 막대 하나에 종이띠 여덟 개가 왼쪽 다섯, 오른쪽 셋의 두 무리로 걸려 있습니다."
ILLU_READ = "흰 바탕 위쪽의 나무 막대 하나에 종이띠 여덟 개가 왼쪽 다섯, 오른쪽 셋의 두 무리로 걸려 있습니다. 막대가 공통 칸으로 모은 표 하나이고, 띠 하나가 실행 한 번의 기록 한 줄입니다. 왼쪽 다섯은 Ch 18 다섯 흐름이고, 오른쪽 셋은 Ch 21 세 질문입니다. 두 무리 사이의 빈틈은 과제가 다른 두 기록을 한 무리로 섞지 않는다는 뜻입니다. 구멍의 수, 띠의 길이, 빈 고리는 어떤 값과도 짝짓지 않습니다."

TITLE = """# """ + TITLE_TEXT + """

**이 노트북에서 할 일**

1. Ch 18 06절 노트북에 저장된 출력과 Ch 21 06절의 비교 기록 파일을 읽기만 합니다.
2. 두 기록의 줄을 같은 칸 이름의 딕셔너리로 옮겨 담고, 요청 수와 성공 여부를 셉니다.
3. 칸마다 평균과 95 백분위수를 보고, 줄이 셋이면 95 백분위수가 가장 큰 값이 되는 까닭을 셉니다.

**준비물** — 이 노트북은 모델을 부르지 않아 API 키가 필요 없습니다.
모델 요청은 0번이고, 요금도 들지 않습니다.
읽는 파일은 앞 챕터 파일 둘과 같은 폴더의 도구 파일 `eval_tools.py`이고, 쓰는 파일은 없습니다.
두 파일은 Ch 18 06절과 Ch 21 06절을 한 번 실행해 남긴 기록이고, 이 노트북은 두 절을 다시 실행하지 않습니다.
이 노트북은 걸린 시간을 재지 않고, 기록에 적힌 걸린 초를 읽기만 합니다.

**기준 버전** — 첫 셀에서 패키지 하나를 설치합니다.
판은 langchain 1.4.0이고, 도구 파일이 메시지 클래스를 가져올 때 씁니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~5절을 읽습니다.
두 기록을 찾아 읽고, 같은 칸 이름으로 옮겨 담아 세는 자리입니다.
6~8절은 평균과 95 백분위수를 보고 백분위 하나를 바꿔 보는 실습이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch29-agent-evaluation`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다."""


def cells() -> list[dict]:
    return [
        md(TITLE, html="skip"),
        md("## 오늘 볼 그림\n\n![" + FIG1_ALT + "](attachment:" + FIG1 + ".png)\n\n" + FIG1_READ, html="skip"),
        md("""## 1. 준비

01~03절은 궤적 하나를 코드 규칙과 평가 모델로 판정했습니다.
이 절은 모델을 부르지 않고, 앞 챕터가 남긴 실행 기록 두 개를 읽어 운영 지표를 견줍니다.
뜻과 구성은 본문 「핵심 개념」에서 풉니다.

첫 셀은 패키지 하나를 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다."""),
        setup(INSTALL),
        md("""**결과 읽기** — 출력 줄 `langchain: 1.4.0`이 보입니다.
실습 폴더 잠금과 같은 판입니다.
이 노트북의 셀은 langchain을 직접 쓰지 않습니다.
도구 파일 `eval_tools.py`가 맨 위에서 메시지 클래스를 가져오기 때문에 설치합니다.

다음 셀은 이 절에서 쓸 모듈과 함수를 가져옵니다.
모듈 `json`과 `os`는 Ch 21 06절처럼 파일을 찾고 읽을 때 씁니다.
모듈 `math`의 함수 `math.ceil`은 Ch 15 06절에서 본 올림 함수입니다."""),
        setup(IMPORTS),
        md("""**결과 읽기** — 라벨 `도구 파일에서 가져온 함수:` 뒤에 `average`와 `nearest_rank`가 보입니다.
앞에서 배운 함수는 `eval_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.

노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다.

두 함수는 Ch 15 06절 노트북에서 배웠고, 이 절부터 도구 파일에서 가져옵니다.
도구 파일에는 그 노트북 셀의 주석과 본문을 글자 그대로 옮겼고, 인자도 같습니다.
함수 `average(values)`는 값 목록의 평균을 소수 여섯째 자리까지 냅니다.
함수 `nearest_rank(values, percent)`는 가장 가까운 자리 방식으로 백분위수 하나를 냅니다.

## 2. 두 기록 파일 찾기

이 절이 읽는 기록은 둘입니다.
하나는 Ch 18 06절 노트북에 저장된 비교 표 출력이고, 다른 하나는 Ch 21 06절이 쓴 비교 기록 파일입니다.
두 파일은 다른 챕터 폴더에 있어, 다음 셀은 먼저 프로젝트 맨 위 폴더를 찾습니다.
셀 모양은 Ch 21 06절의 자리 찾기 셀과 같고, 확인하는 폴더만 다릅니다."""),
        code(ROOT_FIND),
        md("""**결과 읽기** — 출력 줄 `고른 자리: .`은 교재 출력을 프로젝트 맨 위에서 실행했다는 뜻입니다.
교재 출력은 실행 도구가 프로젝트 맨 위 폴더에서 커널을 띄운 실행이라 `.`이 찍혔습니다.
노트북을 `notebooks/` 폴더에서 열면 이 줄에 `../../../..`가 찍힙니다.
학생 묶음을 풀어 `notebooks/` 폴더에서 열어도 같은 자리를 찾습니다.

다음 셀은 두 기록 파일의 자리를 만들고, 파일이 있는지 봅니다."""),
        code(PATHS),
        md("""**결과 읽기** — 출력 줄 `Ch 18 06절 노트북이 있는가: True`와 `Ch 21 06절 비교 기록이 있는가: True`가 보입니다.
두 파일 모두 이 자리에 있습니다.

## 3. Ch 18 기록: 저장된 출력에서 표 줄 찾기

Ch 18 06절은 같은 과제를 다섯 흐름으로 실행하고, 비교 표를 출력했습니다.
표의 칸은 패턴·요청 수·토큰 수·걸린 초·품질·상태 여섯입니다.
이 표에는 도구를 부른 차례가 없습니다.
Ch 18의 다섯 흐름은 도구 호출 요청을 쓰지 않았기 때문입니다.
그래서 Ch 18 줄은 궤적이 아니라, 흐름 하나를 실행한 기록 한 줄로 읽습니다.

노트북 파일(`.ipynb`)은 셀의 글과 저장된 출력을 담은 JSON 파일입니다.
다음 셀은 Ch 18 06절 노트북 파일을 JSON으로 읽고, 셀 수를 봅니다.
그 노트북은 실행하지 않습니다."""),
        code(READ18),
        md("""**결과 읽기** — 출력 줄 `셀 수: 58`이 보입니다.
비교 표는 그 가운데 한 코드 셀의 저장된 출력에 있습니다.
이 절이 읽는 비교 표는 Ch 18 06절을 한 번 실행해 저장한 출력입니다.

셀마다 저장된 출력은 칸 `outputs`의 목록에 있습니다.
출력 가운데 `print`로 찍힌 글은 칸 `output_type`이 `stream`이고, 글은 칸 `text`에 줄 목록으로 들어 있습니다.
다음 셀은 코드 셀 하나에서 이 글만 모아 한 줄씩 내놓는 함수를 정의합니다.
글 메서드 `join`(Ch 16 01절)으로 줄 목록을 한 글로 잇고, `splitlines`(03절)로 다시 줄마다 나눕니다."""),
        code(DEF_PRINTED),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `printed_lines_of(cell)`는 코드 셀 하나를 받아, `print`로 찍힌 줄의 목록을 내놓습니다.

다음 셀은 이 함수로 노트북의 모든 코드 셀에서 저장된 출력 줄을 모읍니다.
마크다운 셀에는 칸 `outputs`가 없어, 칸 `cell_type`이 `code`인 셀만 봅니다."""),
        code(COLLECT),
        md("""**결과 읽기** — 출력 줄 `저장된 출력 줄 수: 69`가 보입니다.
Ch 18 06절 노트북의 코드 셀들이 찍은 줄을 모두 모은 수입니다.

비교 표 줄은 칸을 「 | 」로 나눠 찍었습니다.
표 맨 위의 머리 줄은 `pattern`으로 시작해, 표 줄에서 뺍니다.
다음 셀은 「 | 」가 든 줄 가운데 머리 줄이 아닌 줄만 모읍니다.
03절에서 쓴 글 메서드 `startswith`로 머리 줄을 가립니다."""),
        code(TABLE_LINES),
        md("""**결과 읽기** — 출력 줄 `표 줄 수: 5`가 보이고, `assert`도 오류 없이 지나갔습니다.
Ch 18 06절 표의 다섯 흐름이 한 줄씩입니다.

다음 셀은 표 줄 가운데 마지막 다섯 줄을 Ch 18 기록으로 씁니다.
비교 표는 Ch 18 06절 노트북의 뒤쪽에서 한 번 찍히므로, 마지막 다섯 줄이 그 표입니다.
번호 `[-5:]`는 Ch 16 03절에서 본 음수 슬라이스로, 끝에서 다섯 개를 자릅니다."""),
        code(SHOW_FIVE),
        md("""**결과 읽기** — 라벨 줄 `Ch 18 표 다섯 줄:` 아래 다섯 줄이 보입니다.
첫 줄은 `chaining | 2 | 712 | 3.756 | 5 | ok`이고, 마지막 줄은 `generator_evaluator`로 시작합니다.

줄마다 차례대로 패턴 이름·요청 수·토큰 수·걸린 초·품질·상태입니다.
요청 수는 모델 요청 수이고, 토큰 수는 입력 토큰과 출력 토큰을 더한 값입니다.
품질은 안내문을 코드로 검사해 센 0~5이고, 평가 모델의 점수가 아닙니다.

## 4. 공통 칸으로 옮겨 담기

두 기록은 칸 이름이 다릅니다.
Ch 18 표의 `calls`와 Ch 21 기록의 `model_calls`는 이름이 다르지만, 둘 다 모델 요청 수입니다.
이런 값을 같은 이름의 칸으로 옮겨 담으면, 두 기록을 한 표에 모을 수 있습니다.
이렇게 맞춘 칸을 이 절에서는 공통 칸이라고 부릅니다.
공통 칸은 이름·요청 수·도구 요청 수·토큰 수·걸린 초·점수 여섯입니다.

다음 셀은 표 줄 하나를 칸 여섯으로 나누는 함수를 정의합니다.
글 메서드 `split`으로 「|」에서 나누고, `strip`으로 칸마다 앞뒤 빈칸을 뺍니다."""),
        code(DEF_SPLIT),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `split_row(line)`는 표 줄 하나를 받아, 글 여섯 개의 목록을 내놓습니다.

다음 셀은 나눈 칸 여섯을 공통 칸 딕셔너리로 옮겨 담는 함수를 정의합니다.
Ch 18 기록에는 도구 요청 수 칸이 없어, 그 칸은 모르는 값 `None`으로 둡니다.
점수는 품질을 만점으로 나눠 0~1로 맞추고, 만점은 인자 `full_quality`로 받습니다."""),
        code(DEF_CH18),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `ch18_row(parts, full_quality)`는 나눈 칸 목록과 품질 만점을 받아, 공통 칸 딕셔너리 하나를 내놓습니다.
요청 수·토큰 수·품질은 `int`로, 걸린 초는 `float`로 바꿔 숫자로 담습니다.

다음 셀은 Ch 18 다섯 줄을 모두 옮겨 담고, 상태 칸이 `ok`인 줄을 셉니다.
품질 만점은 코드 검사 항목 수 5입니다.
다섯 흐름이 모두 끝까지 갔는지는 기록의 모양이라 `assert`로 확인합니다."""),
        code(BUILD18),
        md("""**결과 읽기** — 출력 줄 `옮겨 담은 줄 수: 5 | 상태가 ok인 줄 수: 5`가 보이고, `assert`도 지나갔습니다.
다섯 흐름 모두 상태가 `ok`였습니다.

이제 Ch 21 기록을 읽습니다.
Ch 21 06절은 질문 세 개를 고정 흐름과 에이전트 흐름으로 견주고, 질문마다 비교 기록 한 줄을 파일에 썼습니다.
이 절은 그 가운데 에이전트 흐름의 칸만 읽습니다.
다음 셀은 파일을 읽고, 줄 수와 질문 번호를 봅니다."""),
        code(READ21),
        md("""**결과 읽기** — 출력 줄 `줄 수: 3 | 한 줄의 칸 수: 12`와 `질문 번호: ['C01', 'C05', 'C07']`이 보입니다.
줄이 셋이라 `assert`도 지나갔습니다.

한 줄의 칸 열둘 가운데 이 절은 여섯을 읽습니다.
질문 번호 `qid`, 사용량 `agent_usage`, 도구 요청 수 `tool_calls`, 걸린 초 `agent_latency_s`가 그 가운데 넷입니다.
나머지 둘은 평가 모델 판정 `agent_supported`와 검색 기록 `agent_trace`입니다.
다음 셀은 한 줄을 공통 칸 딕셔너리로 옮겨 담는 함수를 정의합니다.
참·거짓 값에 `float`를 쓰면, 참은 `1.0`이 되고 거짓은 `0.0`이 됩니다."""),
        code(DEF_CH21),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `ch21_row(record)`는 비교 기록 한 줄을 받아, 공통 칸 딕셔너리 하나를 내놓습니다.
토큰 수는 입력 토큰과 출력 토큰을 더해, Ch 18 표의 토큰 수와 같은 뜻으로 맞춥니다.

다음 셀은 세 줄을 모두 옮겨 담습니다.
Ch 21 06절은 이 파일의 줄마다 도구 요청 수가 1 이상이라고 적어 두었습니다.
그래서 줄마다 이 값을 `assert`로 확인합니다."""),
        code(BUILD21),
        md("""**결과 읽기** — 출력 줄 `옮겨 담은 줄 수: 3`이 보이고, `assert`도 세 줄 모두 지나갔습니다.
라벨 `첫 줄:` 뒤 딕셔너리의 칸 `'요청 수': 2`와 `'도구 요청 수': 1`이 보입니다.

다음 셀은 공통 칸 딕셔너리 한 줄을 표 한 줄로 출력하는 함수를 정의합니다.
Ch 18 줄과 Ch 21 줄에 같은 함수를 씁니다."""),
        code(DEF_SHOW),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `show_row(row)`는 칸 여섯을 「|」로 이어 한 줄로 출력하고, 내놓는 값은 없습니다.

다음 셀은 두 기록의 여덟 줄을 공통 칸 표 하나로 출력합니다.
표 하나에 모아도, 두 기록의 과제와 조건은 서로 다릅니다."""),
        code(TABLE),
        md("""**결과 읽기** — 라벨 줄 `이름 | 요청 수 | 도구 요청 수 | 토큰 수 | 걸린 초 | 점수` 아래 여덟 줄이 보입니다.
Ch 18 다섯 줄은 `Ch 18 chaining | 2 | None`처럼 도구 요청 수가 `None`입니다.
Ch 21 세 줄은 `Ch 21 C01 | 2 | 1`처럼 요청 수 2, 도구 요청 수 1입니다.

토큰 수와 걸린 초는 각 기록이 한 번 실행한 값입니다.
교재 출력에서는 Ch 18 걸린 초가 `1.043`부터 `6.966`까지, Ch 21 걸린 초가 `1.36`부터 `2.003`까지였습니다.
두 기록은 과제·질문·요청을 보낸 방법이 달라, 이 값으로 어느 쪽이 낫다고 정하지 않습니다.
점수 칸도 Ch 18은 코드 검사, Ch 21은 평가 모델 판정이라 잣대가 다릅니다.

## 5. 세는 값으로 읽기

03절에서 본 것처럼, 에이전트의 모델 요청 수는 「도구를 요청한 응답 수 + 1」입니다.
Ch 21 기록의 칸 `tool_calls`는 도구 메시지 수입니다.
도구 메시지가 하나이면, 도구를 요청한 응답도 하나입니다.
다음 셀은 이 셈이 세 줄에 맞는지 보고, 칸 `agent_trace`에 든 검색 기록 수도 셉니다."""),
        code(CALLS21),
        md("""**결과 읽기** — 라벨 줄 아래 세 줄 `C01 | 2 | 1 | True | 1`, `C05 | 2 | 1 | True | 1`, `C07 | 2 | 1 | True | 1`이 보입니다.
세 줄 모두 요청 수가 도구 요청 수에 1을 더한 값과 같았습니다.
검색 기록 수도 줄마다 1로, 도구 요청 수와 같았습니다.

요청 수는 도구를 요청한 응답 하나와 답을 쓴 응답 하나를 더한 2입니다.
03절의 에이전트는 도구 둘을 차례로 불러 요청이 3번이었고, 이 기록은 도구 하나라 2번입니다.
도구를 한 번 부른 것은 Ch 21 06절의 실행에서 모델이 고른 일이라, 그 절을 다시 실행하면 달라질 수 있습니다.

다음 셀은 두 기록이 잘됐다고 적은 줄을 셉니다.
Ch 18은 상태 칸과 품질 칸, Ch 21은 평가 모델 판정으로 셉니다."""),
        code(SUCCESS),
        md("""**결과 읽기** — 출력 줄 `Ch 18 상태가 ok인 줄: 5 | 품질이 만점인 줄: 4 | 전체: 5`가 보입니다.
출력 줄 `Ch 21 평가 모델 판정이 참인 줄: 3 | 전체: 3`도 보입니다.

Ch 18 상태 칸은 흐름이 끝까지 갔는지, 품질 칸은 안내문이 코드 검사를 몇 항목 지났는지입니다.
Ch 21 판정은 답이 준 문서로 뒷받침되는지를 평가 모델이 Ch 21 06절에서 한 번 본 값입니다.
세 값 모두 「잘됐다」를 세지만 잣대가 서로 달라, 줄 수를 두 기록 사이에서 견주지 않습니다.

## 6. 칸마다 평균

다음 셀은 공통 칸 딕셔너리 목록에서 칸 하나의 값만 모으는 함수를 정의합니다.
이 목록을 Ch 15 06절 함수 `average`와 `nearest_rank`에 넘깁니다."""),
        code(DEF_COLUMN),
        md("""**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `column_values(rows, key)`는 딕셔너리 목록과 칸 이름을 받아, 그 칸의 값 목록을 내놓습니다.

다음 셀은 Ch 18 다섯 줄에서 칸마다 평균을 냅니다.
도구 요청 수 칸은 `None`이라 평균을 내지 않습니다.
기록의 걸린 초가 소수 셋째 자리까지라, `round`로 평균도 셋째 자리까지 남깁니다."""),
        code(MEAN18),
        md("""**결과 읽기** — 라벨 줄 `Ch 18 다섯 줄의 평균:` 아래 네 줄이 보입니다.
출력 줄 `요청 수 | 2.8`과 `점수 | 0.96`이 보입니다.
요청 수 합 14를 다섯 흐름으로 나눈 값이고, 점수는 다섯 줄 가운데 넷이 만점이라 0.96입니다.

교재 출력에서는 `토큰 수 | 862.2`, `걸린 초 | 4.206`이었습니다.
두 값은 Ch 18 06절을 한 번 실행한 값이라, 그 절을 다시 실행하면 달라집니다.

다음 셀은 Ch 21 세 줄에서 같은 칸마다 평균을 냅니다.
도구 요청 수 칸도 함께 봅니다."""),
        code(MEAN21),
        md("""**결과 읽기** — 라벨 줄 `Ch 21 세 줄의 평균:` 아래 다섯 줄이 보입니다.
출력 줄 `요청 수 | 2.0`과 `도구 요청 수 | 1.0`, `점수 | 1.0`이 보입니다.
세 줄의 값이 모두 같아, 평균도 그 값입니다.

교재 출력에서는 `토큰 수 | 688.0`, `걸린 초 | 1.731`이었습니다.
두 값도 Ch 21 06절을 한 번 실행한 값입니다.
Ch 18 평균과 나란히 놓아도, 과제가 달라 어느 쪽이 빠르거나 적다고 읽지 않습니다.

## 7. 95 백분위수

평균만으로는 오래 걸린 실행이 있었는지 알기 어렵습니다.
Ch 15 06절에서는 값을 줄 세워 95번째 백분위수를 봤습니다.
가장 가까운 자리 방식에서 자리는 95 × 줄 수 ÷ 100을 올린 정수이고, 줄 세운 값에서 그 자리의 값을 고릅니다.

다음 셀은 Ch 21 세 줄의 걸린 초와 토큰 수로 이 자리와 값을 봅니다.
실행 전에 예상해 봅니다. 줄이 셋이면 95 백분위수는 몇 번째 자리일까요?"""),
        code(P95),
        md("""**결과 읽기** — 출력 줄 `95 백분위수 자리: 3 | 줄 수: 3`이 보입니다.
95 × 3 ÷ 100 = 2.85를 올리면 3이라, 줄 세운 세 값 가운데 세 번째, 곧 가장 큰 값입니다.

교재 출력에서는 라벨 `줄 세운 걸린 초:` 뒤가 `[1.36, 1.829, 2.003]`이었습니다.
그래서 `95 백분위수 걸린 초: 2.003`이었고, 토큰 수도 가장 큰 값 `699`였습니다.
두 값은 Ch 21 06절을 한 번 실행한 값입니다.

줄이 셋일 때만 이런지 궁금합니다.
다음 셀은 같은 셈을 줄 수만 바꿔, 95 백분위수가 가장 큰 값의 자리인지 봅니다."""),
        code(RANK),
        md("""**결과 읽기** — 라벨 줄 아래 다섯 줄이 보입니다.
줄 `3 | 3 | True`, `5 | 5 | True`, `19 | 19 | True`는 자리가 줄 수와 같았습니다.
줄 `20 | 19 | False`부터는 가장 큰 값이 아닌 자리를 골랐습니다.

줄이 열아홉 이하이면 95 백분위수는 늘 가장 큰 값입니다.
그래서 줄이 적은 기록의 95 백분위수는 가장 큰 값 하나를 다시 읽는 것과 같습니다.
오래 걸린 실행이 얼마나 드문지 보려면, 같은 서비스의 실행을 훨씬 많이 모아야 합니다.

## 8. 값 바꿔 보기: 백분위 하나만 바꾸기

이제 값 하나만 바꿔 봅니다.
바꿀 값은 백분위이고, 95를 50으로 바꿉니다.
줄 수와 값 목록은 그대로 둡니다.
실행 전에 예상해 봅니다. 줄 셋에서 50 백분위수는 몇 번째 자리일까요?"""),
        code(P50),
        md("""**결과 읽기** — 출력 줄 `50 백분위수 자리: 2`가 보입니다.
50 × 3 ÷ 100 = 1.5를 올린 2라, 줄 세운 세 값의 가운데 값입니다.

교재 출력에서는 `50 백분위수 걸린 초: 1.829`, `50 백분위수 토큰 수: 684`였습니다.
95 백분위수와 달리 가장 큰 값이 아닌 가운데 값이 나왔습니다.
백분위를 바꾸면 자리가 바뀌고, 자리가 바뀌면 고르는 값이 바뀝니다.

## 정리

1. 두 기록의 여덟 줄을 공통 칸 여섯의 딕셔너리로 옮겨 담았습니다. 기록에 없는 Ch 18 도구 요청 수는 `None`으로 두었습니다.
2. 이 기록에서 Ch 21 세 줄은 모두 요청 2번·도구 요청 1번으로, 03절의 요청 수 셈과 맞았습니다. Ch 18 다섯 흐름은 요청 수가 흐름마다 달랐고, 다섯 줄 모두 상태가 ok였습니다. 두 기록의 값은 모두 앞 챕터를 한 번 실행한 값입니다.
3. 줄이 셋이면 95 백분위수의 자리가 3이라 가장 큰 값이 나옵니다. 줄이 스무 개는 되어야 가장 큰 값에서 떨어집니다.

다음 학습은 05절 실습입니다. 그 절에서는 03절의 평가받는 에이전트를 호출 한도만 바꿔 두 번 실행하고, 네 모드와 공통 칸으로 두 실행을 견줍니다."""),
    ]


def notebook_cells() -> list[dict]:
    return cells()


# ---------------------------------------------------------------- _src 본문
def mermaid_block(name: str, alt: str, caption: str, reading: str) -> str:
    return ("{{mermaid:" + name + "|" + alt + "|" + caption + "}}\n"
            + '<p class="look"><b>도식 읽기</b> — ' + html_text(reading) + "</p>\n")


def illustration_block() -> str:
    """삽화 PNG와 그림 읽기가 있을 때만 본문에 넣습니다(첫 실행 때는 그림 파일이 없어 빌드가 멈추지 않게)."""
    if not (FIGS / (ILLU + ".png")).is_file() or not ILLU_READ or not ILLU_ALT:
        return ""
    return ("{{img:" + ILLU + "|" + ILLU_ALT + "|" + ILLU_CAP + "}}\n"
            + '<p class="look"><b>그림 읽기</b> — ' + ILLU_READ + "</p>\n")


L_01 = "01-에이전트-평가-세-전략.html"
L_02 = author_01.L_02
L_03 = author_01.L_03
L_CH15_06 = "../../part4/ch15-evaluation-advanced/06-대화당-비용-백분위수.html"
L_CH16_01 = "../../part4/ch16-guardrails/01-입출력-출처-검증.html"
L_CH16_03 = author_01.L_CH16_03
L_CH18_06 = "../../part5/ch18-workflow-patterns/06-같은-과제로-다섯-패턴-비교.html"
L_CH21_06 = author_01.L_CH21_06
L_CH30_01 = "../../part7/ch30-fastapi-serving/01-비동기-라우팅과-스키마.html"
L_05 = "05-Agent-평가-실습.html"

TERM_ROWS = [
    ("운영 지표", "에이전트를 실행할 때마다 모으는 값입니다. 요청 수·도구 요청 수·토큰 수·걸린 초·성공 여부가 여기에 듭니다. 가게가 날마다 손님 수와 매출을 적어 두는 장부와 같습니다. 이 절에서는 두 기록의 줄마다 이 값을 딕셔너리 한 개로 옮겨 담았습니다."),
    ("공통 칸", "서로 다른 기록의 값을 같은 이름의 칸으로 옮겨 담은 것입니다. 기록에 없는 칸은 지어내지 않고 <code>None</code>으로 둡니다. 두 가게의 장부를 같은 양식에 옮겨 적는 것과 같습니다. 이 절의 공통 칸은 이름·요청 수·도구 요청 수·토큰 수·걸린 초·점수 여섯입니다."),
]

VALUE_ROWS = [
    ("요청 수 평균", "<code>2.8</code>", "<code>2.0</code>", "세는 값(모델이 정한 몫 있음)"),
    ("도구 요청 수 평균", "기록에 없음", "<code>1.0</code>", "세는 값(모델이 고른 횟수)"),
    ("점수 평균", "<code>0.96</code>(품질 ÷ 5)", "<code>1.0</code>(평가 모델 판정)", "잣대가 달라 견주지 않음"),
    ("토큰 수 평균", "<code>862.2</code>", "<code>688.0</code>", "실행마다 달라지는 값"),
    ("걸린 초 평균", "<code>4.206</code>", "<code>1.731</code>", "실행마다 달라지는 값"),
    ("95 백분위수 걸린 초", "셈하지 않음", "<code>2.003</code>(자리 3, 가장 큰 값)", "실행마다 달라지는 값"),
    ("95 백분위수 토큰 수", "셈하지 않음", "<code>699</code>(자리 3, 가장 큰 값)", "실행마다 달라지는 값"),
]

LOOK_B5 = "노트북 3절에서 <code>표 줄 수: 5</code>와 <code>옮겨 담은 줄 수: 5 | 상태가 ok인 줄 수: 5</code>를 봅니다. 4절에서 <code>줄 수: 3 | 한 줄의 칸 수: 12</code>와 공통 칸 표 여덟 줄을 찾습니다. 5절에서는 세 줄 모두 <code>True</code>인 요청 수 셈을 확인합니다."
LOOK_B6 = "노트북 6절에서 <code>요청 수 | 2.8</code>과 <code>요청 수 | 2.0</code>을, 7절에서 <code>95 백분위수 자리: 3 | 줄 수: 3</code>을 확인합니다. 8절에서 <code>50 백분위수 자리: 2</code>를 봅니다. 앞 챕터를 다시 실행하면 표의 값이 모두 달라질 수 있습니다."


def runs_paragraph() -> str:
    if not RUNS_SENTENCE:
        return ""
    return "<p>" + RUNS_SENTENCE + "</p>\n"


def src_html() -> str:
    terms = table_html(["말", "뜻"], TERM_ROWS)
    value_table = table_html(["값", "Ch 18 다섯 줄", "Ch 21 세 줄", "성격"], VALUE_ROWS)
    text = """<!--meta: 강의 0.75h | 실습 1.25h | 코드 notebooks/""" + SLUG + """.ipynb | 새 용어 2 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>앞 챕터가 저장한 실행 기록 두 개를 찾아 읽고, 같은 칸 이름의 딕셔너리로 옮겨 담을 수 있습니다.</li>
<li>요청 수·도구 요청 수·성공 여부 같은 세는 값으로 두 기록을 읽고, 그 값도 한 번 실행한 값임을 말할 수 있습니다.</li>
<li>걸린 초와 토큰 수의 평균과 95 백분위수를 셈하고, 줄이 적을 때의 한계를 설명할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href=\"""" + L_01 + """\">01절</a>~<a href=\"""" + L_03 + """\">03절</a>은 궤적 하나를 놓고, 에이전트가 제대로 움직였는지를 판정했습니다. 서비스로 내놓은 에이전트는 실행할 때마다 요청 수·걸린 초·토큰 수 같은 값을 남깁니다. 이런 값을 모아 두어야 요청이 늘었는지, 오래 걸린 실행이 있었는지 볼 수 있습니다. 그런데 기록마다 칸 이름과 담긴 뜻이 달라, 그대로는 한 표에 모을 수 없습니다.</p><p>이 절은 모델을 부르지 않고, 앞 챕터가 남긴 기록 두 개를 읽습니다. <a href=\"""" + L_CH18_06 + """\">Ch 18 06절</a> 노트북에 저장된 비교 표와, <a href=\"""" + L_CH21_06 + """\">Ch 21 06절</a>이 쓴 비교 기록 파일입니다. 두 기록을 같은 칸 이름으로 옮겨 담고, 세는 값부터 읽습니다. 제목에는 「Ch18 궤적」이라고 적었지만, Ch 18 기록에는 도구를 부른 차례가 없습니다. Ch 18 기록은 흐름 하나의 요청 수·토큰 수·걸린 초·품질·상태 칸뿐입니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href=\"""" + L_01 + """\">01절</a>에서는 최종 답 평가·한 단계 평가·궤적 평가를, <a href=\"""" + L_02 + """\">02절</a>에서는 네 모드를 봤습니다. <a href=\"""" + L_03 + """\">03절</a>에서는 평가받는 에이전트를 실제로 한 번 실행하고, 그 궤적을 모드와 평가 모델로 판정했습니다. 같은 절에서 모델 요청 수를 「도구를 요청한 응답 수 + 1」로 셌습니다. 이 절은 그 셈을 Ch 21 기록에 그대로 씁니다.</p><p><a href=\"""" + L_CH18_06 + """\">Ch 18 06절</a>에서는 같은 과제를 다섯 흐름으로 실행해, 흐름마다 비교 표 한 줄을 만들었습니다. 표의 품질 칸은 안내문을 코드로 검사해 센 0~5이고, 평가 모델의 점수가 아닙니다. 그 절은 이 표를 Ch 29 04절이 저장된 출력에서 읽는다고 적었습니다. 그래서 이 절은 Ch 18 06절 노트북을 실행하지 않고, 파일에 저장된 출력만 읽습니다.</p><p><a href=\"""" + L_CH21_06 + """\">Ch 21 06절</a>에서는 고정 흐름과 에이전트 흐름을 질문 세 개로 견주고, 비교 기록 파일을 썼습니다. 에이전트 흐름의 요청 수·도구 요청 수·토큰 수·걸린 초와 평가 모델 판정이 질문마다 한 줄씩 담겼습니다. 이 절은 그 파일을 읽기만 하고, 줄 수와 줄마다 도구 요청 수가 1 이상인지를 <code>assert</code>로 확인합니다. 파일 자리를 찾는 셀은 그 절의 자리 찾기 셀과 모양이 같습니다.</p><p><a href=\"""" + L_CH15_06 + """\">Ch 15 06절</a>에서는 평균을 내는 함수 <code>average</code>와, 가장 가까운 자리 방식으로 백분위수를 찾는 함수 <code>nearest_rank</code>를 배웠습니다. 두 함수는 이 절부터 도구 파일에서 가져옵니다. 값을 줄 세우는 <code>sorted</code>와 올림 함수 <code>math.ceil</code>도 그 절에서 썼습니다. 글 메서드 <code>join</code>은 <a href=\"""" + L_CH16_01 + """\">Ch 16 01절</a>, 음수 슬라이스는 <a href=\"""" + L_CH16_03 + """\">Ch 16 03절</a>에서 봤습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>오르골 가게 두 곳이 한 주 동안 울린 곡을 모아 본다고 해 봅니다. 두 가게는 곡마다 쓴 종이띠를 서로 다른 막대에 걸어 두었습니다. 띠를 나무 막대 하나에 옮겨 걸면, 띠가 몇 개인지와 어느 가게에서 왔는지가 한눈에 보입니다.</p><p>막대 하나가 공통 칸으로 모은 표이고, 띠 하나가 실행 한 번의 기록 한 줄입니다. 걸어 둔 띠는 몇 번을 다시 세어도 같지만, 가게가 곡을 다시 울리면 새 띠의 구멍은 달라질 수 있습니다. 이 절은 걸어 둔 띠를 세기만 하고, 곡을 다시 울리지는 않습니다. 그래서 결론은 이 띠들에 대한 사실로만 적습니다.</p><p>비유와 다른 점도 있습니다. 오르골 띠에는 구멍만 있지만, 기록 한 줄에는 요청 수·토큰 수·걸린 초 같은 값이 칸마다 들어 있습니다.</p>
""" + illustration_block() + """<h3>운영 지표와 공통 칸</h3><p>운영 지표는 에이전트를 실행할 때마다 모으는 값입니다. 요청 수·도구 요청 수·토큰 수·걸린 초·성공 여부가 여기에 듭니다. 앞 챕터의 두 기록에도 이런 값이 있지만, 칸 이름이 서로 다릅니다. Ch 18 표의 <code>calls</code>와 Ch 21 기록의 <code>model_calls</code>는 이름이 다르지만, 둘 다 모델 요청 수입니다.</p><p>그래서 두 값을 같은 칸 「요청 수」로 옮겨 담습니다. 이렇게 맞춘 칸을 이 절에서는 공통 칸이라고 부릅니다. 기록에 없는 칸은 지어내지 않고 <code>None</code>으로 둡니다. Ch 18 기록에는 도구 요청 수 칸이 없어, 그 칸은 <code>None</code>입니다.</p><p>같은 이름의 칸에 담아도 뜻까지 같아지지는 않습니다. 칸 「점수」에는 Ch 18 품질을 만점 5로 나눈 값과, Ch 21 평가 모델 판정(참이면 1.0)을 담았습니다. 앞은 코드 검사, 뒤는 평가 모델 판정이라 잣대가 다릅니다. 이 절은 두 점수를 서로 견주지 않고, 기록마다 따로 읽습니다.</p>
""" + terms + """
<p>새 말을 이 절 코드에서 보면 이렇습니다. 공통 칸은 함수 <code>ch18_row</code>와 <code>ch21_row</code>가 내놓는 딕셔너리의 키 여섯입니다. 운영 지표는 그 딕셔너리에 담긴 값이고, 노트북 4절의 표 여덟 줄이 그 모습입니다.</p>
""" + mermaid_block(FIG1, FIG1_ALT, FIG1_CAP, FIG1_READ) + """<h3>세는 값도 한 번 실행한 값입니다</h3><p>두 기록의 값은 모두 앞 챕터를 한 번 실행해 남긴 값입니다. 이 노트북은 기록을 읽기만 해서, 몇 번을 실행해도 같은 값이 나옵니다. 그러나 앞 챕터를 다시 실행하면 기록의 값이 바뀔 수 있습니다.</p><p>요청 수처럼 세는 값에도 그 실행에서 모델이 정한 몫이 있습니다. <a href=\"""" + L_CH18_06 + """\">Ch 18 06절</a>의 요청 수 가운데 2·2·3은 코드가 정했고, 5와 2는 모델 답이 정한 작업 수와 바퀴 수에서 나왔습니다. Ch 21 기록의 도구 요청 수 1은 모델이 검색을 한 번 고른 결과이고, 판정은 평가 모델이 한 번 내린 값입니다. 걸린 초와 토큰 수는 네트워크 상태와 모델이 쓴 글에 따라 실행마다 달라집니다.</p><p>다시 실행해도 그대로인 것은 「요청 수 = 도구를 요청한 응답 수 + 1」처럼 흐름의 짜임새가 정한 셈입니다. Ch 18 06절이 노트북 밖 다섯 번에서 본 요청 수도 모두 2·2·3·5·2였지만, 그 다섯 번의 값일 뿐입니다. 그래서 이 절은 이 기록에서 센 값과, 그 셈이 기록과 맞는지를 결론으로 삼습니다. 이 기록만으로 두 짜임새의 일반 성질을 정하지 않고, 걸린 초와 토큰 수는 표와 결과 읽기 둘째 단락에만 둡니다.</p><p>95 백분위수는 <a href=\"""" + L_CH15_06 + """\">Ch 15 06절</a>의 가장 가까운 자리 방식으로 셉니다. 자리는 95 × 줄 수 ÷ 100을 올린 정수이고, 줄 세운 값에서 그 자리의 값을 고릅니다. 줄이 셋이면 95 × 3 ÷ 100 = 2.85를 올려 자리 3, 곧 가장 큰 값입니다. 줄이 열아홉 이하이면 자리가 늘 줄 수와 같아, 95 백분위수는 가장 큰 값이 됩니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 프로젝트 맨 위를 찾고, 두 기록 파일이 있는지 봅니다. 3절은 Ch 18 06절 노트북 파일에서 저장된 출력 줄을 모아, 비교 표 다섯 줄을 찾습니다. 4절은 두 기록의 줄을 공통 칸 딕셔너리로 옮겨 담아 표 하나로 출력합니다. 5절은 요청 수 셈과 성공 여부를 세고, 6절은 칸마다 평균을 냅니다. 7절은 95 백분위수를 찾고, 8절은 백분위 하나만 바꿔 봅니다.</p><p>모델 요청은 0번이고, API 키도 필요 없습니다. 읽는 파일은 앞 챕터 파일 둘과 도구 파일 <code>eval_tools.py</code>이고, 쓰는 파일은 없습니다. 이 노트북은 걸린 시간을 재지 않고, 기록에 적힌 걸린 초를 읽기만 합니다.</p>
{{notebook:""" + SLUG + """}}
<p class="look"><b>확인할 점</b> — """ + LOOK_B5 + """</p>
""" + mermaid_block(FIG2, FIG2_ALT, FIG2_CAP, FIG2_READ) + """<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>이 기록에서 Ch 18 다섯 흐름은 요청 수가 2·2·3·5·2번으로 흐름마다 달랐고, 다섯 줄 모두 상태가 ok였습니다. Ch 21 세 질문은 모두 요청 2번·도구 요청 1번이었습니다. 03절의 셈대로, 요청 수는 도구를 요청한 응답 수 1에 1을 더한 값과 같았습니다. 줄마다 검색 기록도 하나씩이라, 도구 요청 수와 맞았습니다.</p><p>잘됐다고 적은 줄은 기록마다 제 잣대로 셌습니다. 이 기록에서는 Ch 18 다섯 줄 가운데 넷이 품질 만점이었고, Ch 21은 세 줄 모두 평가 모델 판정이 참이었습니다. 평가 모델 판정은 Ch 21 06절을 한 번 실행한 값입니다. 칸 「점수」의 평균은 Ch 18이 0.96, Ch 21이 1.0이지만, 잣대가 달라 서로 견주지 않습니다.</p>
""" + mermaid_block(FIG3, FIG3_ALT, FIG3_CAP, FIG3_READ) + """<p>줄이 셋인 Ch 21 기록에서 95 백분위수의 자리는 3, 곧 가장 큰 값의 자리였습니다. 줄 수 표를 보면 줄이 열아홉일 때까지 자리가 줄 수와 같고, 스무 줄부터 가장 큰 값에서 떨어집니다. 백분위를 50으로 바꾸자 자리가 2가 되어, 줄 세운 세 값의 가운데 값이 나왔습니다. 줄이 적은 기록의 95 백분위수는 가장 큰 값 하나를 다시 읽는 것과 같습니다.</p>
""" + mermaid_block(FIG4, FIG4_ALT, FIG4_CAP, FIG4_READ) + """<p>아래 표는 노트북 6·7절의 평균과 95 백분위수입니다. 표의 값은 모두 각 기록이 한 번 실행해 남긴 값이고, 걸린 초와 토큰 수는 특히 실행마다 달라집니다. 두 기록은 과제·질문·요청을 보낸 방법이 달라, 이 표의 값으로 어느 쪽이 낫다고 정하지 않습니다.</p>
""" + value_table + """
""" + runs_paragraph() + """<p class="look"><b>확인할 점</b> — """ + LOOK_B6 + """</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>이 절은 Ch 18 06절 노트북과 Ch 21 06절 비교 기록 파일을 읽기만 합니다. 두 절을 다시 실행하면 두 파일이 바뀌어, 이 절의 표와 평균도 따라 바뀝니다. 교재 출력을 그대로 두려면 두 절은 다시 실행하지 않습니다.</li><li>Ch 18 표는 Ch 18 06절 노트북을 한 번 실행해 저장한 출력입니다. Ch 21 기록도 Ch 21 06절을 한 번 실행해 쓴 파일입니다. Ch 21 도구 요청 수는 모델이 고른 값이고, 평가 모델 판정은 그 한 번의 실행에서 나온 값입니다. 걸린 초는 네트워크와 서비스 상태에 따라, 토큰 수는 모델이 쓴 답에 따라 달라집니다. 그래서 두 값은 결론·그림·정리에 쓰지 않았습니다.</li><li>두 기록은 과제가 다릅니다. Ch 18은 안내문 하나를 쓰는 과제를 OpenAI 요청으로 바로 보냈습니다. Ch 21은 도서관 질문 셋을 검색 도구가 붙은 에이전트로 보냈습니다. 같은 칸에 담았어도, 두 기록의 값으로 어느 짜임새가 빠르거나 싸다고 정하지 않습니다.</li><li>Ch 18 기록에는 도구 요청 수 칸이 없어 <code>None</code>으로 두었습니다. Ch 18의 다섯 흐름은 도구 호출 요청을 쓰지 않았지만, 이 사실은 Ch 18 절에서 온 것이고 기록에서 읽은 값이 아닙니다.</li><li>Ch 21 기록의 도구 요청 수는 도구 메시지를 센 값입니다. 세 줄 모두 1이라, 도구를 요청한 응답도 하나씩입니다. 한 응답이 도구를 여럿 요청하면 도구 메시지 수와 응답 수가 달라지니, 03절의 셈에는 응답 수를 넣습니다.</li><li>이 절의 <code>assert</code>는 기록의 모양에만 걸었습니다. Ch 18 표 줄 수·상태 칸, Ch 21 줄 수·도구 요청 수입니다. 걸린 초와 토큰 수에는 걸지 않았습니다.</li><li>Ch 18 표는 저장된 출력에서 칸 구분 「 | 」가 든 줄을 찾아 읽습니다. 그래서 Ch 18 06절은 표의 칸 이름을 영어로 두고, 표 뒤에 칸을 나눈 줄을 더 찍지 않았습니다. 그 절의 흐름 하나라도 상태가 ok가 아니면 이 절의 확인 줄이 멈춥니다.</li><li>줄 셋의 95 백분위수는 가장 큰 값과 같아, 오래 걸린 실행이 얼마나 드문지는 말해 주지 않습니다. 이 절의 기록만으로 서비스의 기준값을 정하지 않습니다. 기준값을 정하려면 같은 서비스의 실행을 훨씬 많이 모아야 합니다.</li><li>파일 자리 찾기는 프로젝트 맨 위·실습 폴더 맨 위·<code>notebooks</code> 폴더 세 자리에서 봅니다. 학생 묶음과 같은 폴더 구성에서 <code>notebooks</code> 폴더를 열어 실행해 보니, 키 없이 끝까지 실행되었습니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>Ch 18 06절의 저장된 출력과 Ch 21 06절의 비교 기록을 읽어, 여덟 줄을 공통 칸 여섯의 딕셔너리로 옮겨 담았습니다. 기록에 없는 Ch 18 도구 요청 수는 <code>None</code>으로 두었습니다.</li><li>이 기록에서 Ch 18 다섯 흐름은 요청 수가 흐름마다 달랐고, Ch 21 세 질문은 모두 요청 2번·도구 요청 1번이었습니다. 두 기록 모두 앞 챕터를 한 번 실행한 값이고, Ch 21의 요청 수는 03절의 셈과 맞았습니다.</li><li>줄이 셋이면 95 백분위수의 자리가 3이라, 가장 큰 값이 그대로 나옵니다. 줄이 스무 개는 되어야 95 백분위수가 가장 큰 값에서 떨어집니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href=\"""" + L_05 + """\">05절</a>은 이 챕터의 실습입니다. 03절의 평가받는 에이전트를 호출 한도만 바꿔 두 번 실행하고, 네 모드와 공통 칸으로 두 실행을 견줍니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. Ch 18 표를 공통 칸으로 옮겨 담을 때, 도구 요청 수 칸을 0이 아니라 <code>None</code>으로 둔 까닭은 무엇인가요?</p><p class="quiz-a">Ch 18 기록에는 도구 요청 수 칸이 없기 때문입니다. 0을 적으면 기록에서 읽지 않은 값을 지어낸 것이 됩니다. 기록에 없는 값은 모르는 값 <code>None</code>으로 둡니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">2. Ch 21 기록의 한 줄이 요청 수 2, 도구 요청 수 1이었습니다. 03절의 셈과 맞는지 어떻게 확인하나요?</p><p class="quiz-a">도구 메시지가 하나이면 도구를 요청한 응답도 하나입니다. 그 응답 하나에 답을 쓴 응답 하나를 더하면 2라 셈과 맞습니다. 다만 도구를 한 번 부른 것은 Ch 21 06절을 한 번 실행했을 때 모델이 고른 일이고, 셈만 짜임새가 정한 규칙입니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">3. 칸 「점수」의 평균이 Ch 18은 0.96, Ch 21은 1.0이었습니다. 이 값으로 Ch 21 쪽이 더 잘했다고 말할 수 있나요?</p><p class="quiz-a">말할 수 없습니다. Ch 18 점수는 코드 검사 품질을 5로 나눈 값이고, Ch 21 점수는 평가 모델 판정입니다. 잣대와 과제가 달라, 기록마다 따로 읽습니다. 틀렸다면 본문 「운영 지표와 공통 칸」을 다시 읽습니다.</p><p class="quiz-q">4. 걸린 초가 기록된 실행이 스무 줄이면, 가장 가까운 자리 방식의 95 백분위수는 몇 번째 자리의 값인가요? 그 값은 가장 큰 값인가요?</p><p class="quiz-a">95 × 20 ÷ 100 = 19라 열아홉 번째 자리의 값입니다. 스무 줄 가운데 가장 큰 값은 스무 번째라, 95 백분위수는 가장 큰 값이 아닙니다. 줄이 열아홉 이하이면 95 백분위수는 늘 가장 큰 값입니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/langsmith/dashboards">LangSmith Dashboards</a></div>확인 2026-09-29 · 기본 대시보드가 추적 수·걸린 시간·오류 비율, 토큰 수와 비용을 보여 준다고 적습니다. 도구 실행도 도구 이름별 실행 수·오류 비율·걸린 시간으로 나눠 보여 준다고 적습니다.</li><li><div><a href="https://en.wikipedia.org/wiki/Percentile">Percentile (Wikipedia)</a></div>확인 2026-09-29 · 백분위수를 세는 여러 방식 가운데 가장 가까운 자리 방식(nearest-rank)을 적습니다. 100 백분위수는 줄 세운 목록의 가장 큰 값으로 정의한다고 적습니다.</li><li><div><a href="https://docs.python.org/3/library/math.html#math.ceil">Python math.ceil</a></div>확인 2026-09-29 · 값보다 크거나 같은 정수 가운데 가장 작은 정수를 내놓는다고 적습니다.</li><li>Ch 15 06절 노트북 <code>06-대화당-비용-백분위수.ipynb</code>의 함수 <code>average</code>·<code>nearest_rank</code> 셀을 도구 파일에 글자 그대로 옮겼습니다.</li><li>Ch 18 06절 노트북 <code>06-같은-과제로-다섯-패턴-비교.ipynb</code>의 비교 표 출력(머리 줄과 다섯 줄)을 읽었습니다.</li><li>Ch 21 06절 비교 기록 파일 <code>data/rag-comparison.json</code>(줄 셋, 칸 열둘)에서 칸 여섯을 읽었습니다.</li></ul>
"""
    return text


def write_src(path: Path) -> Path:
    path.write_text(src_html(), encoding="utf-8")
    return path


if __name__ == "__main__":
    check_contracts()
    check_tools()
    if "--tools-copy" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--tools-copy") + 1])
        (target / "eval_tools.py").write_text(TOOLS_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        print("wrote tools copy in", target)
        raise SystemExit(0)
    if "--try" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--try") + 1])
        write_tools(target / "eval_tools.py")
        print("wrote", write_notebook(target, "04", SLUG, "experiment", notebook_cells()))
        if "--with-src" in sys.argv:
            print("wrote", write_src(target / "src.html"))
        raise SystemExit(0)
    print("wrote", write_src(SRC))
    if "--src-only" not in sys.argv:
        # 도구 파일은 없거나 01·02·03판·이 판일 때만 쓴다. 뒤 절이 함수를 더한 판이면 덮어쓰지 않는다(Ch 24 마감 A-10·Ch 25~28 교훈).
        write_tools(TOOLS_PATH)
        path = write_notebook(LAB, "04", SLUG, "experiment", notebook_cells())
        print("wrote", path)
