"""품질 개선 게이트 G1~G7 (textbook/QUALITY-UPGRADE.md §7).

사용: python textbook/_notebook/checks/upgrade_gates.py textbook/part6/ch22-middleware --label before
결과: 챕터 qa/upgrade/gates-{label}.json. --strict 를 주면 실패가 있을 때 종료 코드 1.
G8(새 커널 실행·verify.py·visual.cjs)은 기존 도구로 따로 실행한다.
"""
from __future__ import annotations

import argparse
import ast
import io
import json
import re
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

BOILERPLATE = re.compile(r"#\s*이 셀은 .*(수행|출력)합니다")
FAKE_MODEL = re.compile(r"BaseChatModel\b|FakeListChatModel|GenericFakeChatModel|FakeMessagesListChatModel|class\s+Scripted")
BANNED_WORDS = ["당연히", "간단히", "쉽게", "한 겹 더", "함정", "돌려줍니다", "돌립니다", "돌려 보", "재 보", "회수"]
SCHEMA_BASES = {"BaseModel", "TypedDict"}
ENGLISH_START = re.compile(r"^(?:`[^`]{1,40}`|[A-Za-z][A-Za-z0-9_.@()\-]{0,30})(은|는|이|가|을|를|의|과|와|로|으로|에)(?=\s)")
MAX_SENTENCE = 70
MAX_CODE_LINES = 15


def text(value) -> str:
    return value if isinstance(value, str) else "".join(value)


def allowed(cell: dict) -> set[str]:
    return set(cell.get("metadata", {}).get("upgrade_allow", []))


def is_deep_dive(cell: dict) -> bool:
    return cell.get("metadata", {}).get("lesson_level") == "deep-dive"


def code_only(source: str) -> str:
    lines = []
    for line in source.splitlines():
        stripped = line.lstrip()
        lines.append("pass" if stripped.startswith(("%", "!")) else line)
    return "\n".join(lines)


def g1_ladder(source: str, allow: set[str]) -> list[str]:
    found: list[str] = []
    try:
        tree = ast.parse(code_only(source))
    except SyntaxError as exc:
        return [f"syntax_error:{exc.lineno}"]
    names = {
        ast.Lambda: "lambda", ast.ListComp: "list_comprehension", ast.DictComp: "dict_comprehension",
        ast.SetComp: "set_comprehension", ast.GeneratorExp: "generator_expression", ast.IfExp: "conditional_expression",
        ast.NamedExpr: "walrus", ast.Global: "global", ast.Nonlocal: "nonlocal",
    }
    for node in ast.walk(tree):
        for kind, label in names.items():
            if isinstance(node, kind):
                found.append(label)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.args.vararg or node.args.kwarg:
                found.append("varargs_def")
            inner = [child for child in ast.walk(node) if child is not node and isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))]
            if inner and not isinstance(node, ast.ClassDef):
                found.append("nested_def")
            body = [stmt for stmt in node.body if not (isinstance(stmt, ast.Expr) and isinstance(getattr(stmt, "value", None), ast.Constant))]
            if len(body) > 10:
                found.append("long_function")
        if isinstance(node, ast.ClassDef):
            bases = {getattr(base, "id", getattr(base, "attr", "")) for base in node.bases}
            only_fields = all(isinstance(stmt, (ast.AnnAssign, ast.Expr, ast.Pass)) for stmt in node.body)
            if not (bases & SCHEMA_BASES and only_fields):
                found.append("class_def")
    top_defs = [stmt for stmt in tree.body if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef))]
    if len(top_defs) > 1:
        found.append("multiple_defs_in_cell")
    return [item for item in found if item not in allow]


def call_chain_depth(node: ast.AST) -> int:
    depth = 0
    while isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        depth += 1
        node = node.func.value
    return depth


def g2_shape(source: str, allow: set[str]) -> list[str]:
    found: list[str] = []
    for line in source.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "%", "!")):
            continue
        try:
            tokens = list(tokenize.generate_tokens(io.StringIO(line.strip() + "\n").readline))
            if any(tok.type == tokenize.OP and tok.string == ";" for tok in tokens):
                found.append("semicolon")
        except (tokenize.TokenError, IndentationError):
            pass
    code_lines = [l for l in source.splitlines() if l.strip() and not l.strip().startswith(("#", "%", "!"))]
    if len(code_lines) > MAX_CODE_LINES:
        found.append(f"over_{MAX_CODE_LINES}_lines")
    try:
        tree = ast.parse(code_only(source))
    except SyntaxError:
        return found
    compound = (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    for node in ast.walk(tree):
        if isinstance(node, compound) and node.body and node.body[0].lineno == node.lineno:
            found.append("one_line_compound")
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and len(node.id) == 1 and node.id not in {"i", "_"}:
            found.append(f"one_letter_name:{node.id}")
        if isinstance(node, ast.arg) and len(node.arg) == 1 and node.arg not in {"i", "_"}:
            found.append(f"one_letter_arg:{node.arg}")
        if isinstance(node, ast.Call) and call_chain_depth(node) >= 3:
            found.append("method_chain_3plus")
        if isinstance(node, ast.Call):
            nested = [arg for arg in node.args if isinstance(arg, ast.Call) and any(isinstance(a, ast.Call) for a in arg.args)]
            if nested:
                found.append("nested_call_2plus")
    return [item for item in found if item.split(":")[0] not in allow]


def outputs_text(cell: dict) -> str:
    parts = []
    for output in cell.get("outputs", []):
        if output.get("output_type") == "stream":
            parts.append(text(output.get("text", "")))
        else:
            parts.append(text(output.get("data", {}).get("text/plain", "")))
    return "".join(parts)


def strip_markup(value: str) -> str:
    value = re.sub(r"<pre[\s\S]*?</pre>", " ", value)
    value = re.sub(r"<(svg|table|script|style)[\s\S]*?</\1>", " ", value)
    value = re.sub(r"\{\{[^}]*\}\}", " ", value)
    value = re.sub(r"<code>([^<]*)</code>", r"`\1`", value)
    value = re.sub(r"<(h[1-6])[^>]*>[\s\S]*?</\1>", "\n", value)
    value = re.sub(r"<!--[\s\S]*?-->", " ", value)
    value = re.sub(r"<br\s*/?>", "\n", value)
    value = re.sub(r"</(p|li|summary|figcaption|div|td|th)>", "\n\n", value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"https?://\S+", "", value)
    value = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", value)
    value = re.sub(r"(?m)^#{1,6} .*$", "\n", value)
    return value


def sentences(paragraph: str) -> list[str]:
    parts = re.split(r"(?<=[다요까])[.?!]\s+|(?<=[다요까])[.?!]$", paragraph.strip())
    return [p.strip() for p in parts if p and len(p.strip()) >= 6 and re.search(r"[가-힣]", p)]


def measured_length(sentence: str) -> int:
    return len(re.sub(r"`[^`]*`", "코드", sentence))


def g6_prose(raw: str) -> dict:
    cleaned = strip_markup(raw)
    long_sentences, english_starts, banned, dense_paragraphs = [], [], [], []
    total = 0
    for paragraph in re.split(r"\n\s*\n|\n(?=\s*(?:\d+\.|[-*])\s)", cleaned):
        paragraph = " ".join(paragraph.split())
        items = sentences(paragraph)
        total += len(items)
        if len(items) > 5:
            dense_paragraphs.append(paragraph[:60])
        for sentence in items:
            if measured_length(sentence) > MAX_SENTENCE:
                long_sentences.append(sentence)
            if ENGLISH_START.match(sentence):
                english_starts.append(sentence[:40])
            for word in BANNED_WORDS:
                if word in sentence:
                    banned.append(f"{word}: {sentence[:40]}")
    return {"sentences": total, "long": long_sentences, "english_start": english_starts,
            "banned": banned, "dense_paragraphs": dense_paragraphs}


def check_notebook(path: Path) -> dict:
    nb = json.loads(path.read_text(encoding="utf-8"))
    cells = nb["cells"]
    result = {"code_cells": 0, "G1": [], "G2": [], "G3": [], "G4": [], "G5": [], "prose": []}
    first = cells[0] if cells else {}
    if first.get("cell_type") != "markdown" or "이 노트북에서 할 일" not in text(first.get("source", "")):
        result["G5"].append("title_cell_missing")
    has_figure = any(c["cell_type"] == "markdown" and "attachment:" in text(c["source"]) for c in cells[:4])
    if not has_figure:
        result["G5"].append("core_figure_attachment_missing")
    for index, cell in enumerate(cells):
        source = text(cell["source"])
        if cell["cell_type"] == "markdown":
            result["prose"].append(source)
            continue
        if cell["cell_type"] != "code":
            continue
        result["code_cells"] += 1
        where = f"cell{index}"
        allow = allowed(cell)
        if FAKE_MODEL.search(source):
            result["G4"].append(f"{where}:fake_model")
        for call in re.finditer(r"init_chat_model\(([^)]*)\)", source, re.DOTALL):
            if "temperature=0" not in call[1]:
                result["G4"].append(f"{where}:temperature_missing")
        if not is_deep_dive(cell):
            result["G1"] += [f"{where}:{item}" for item in g1_ladder(source, allow)]
            result["G2"] += [f"{where}:{item}" for item in g2_shape(source, allow)]
        if BOILERPLATE.search(source):
            result["G3"].append(f"{where}:boilerplate_comment")
        lines = [l for l in source.splitlines() if l.strip()]
        if lines and not lines[0].lstrip().startswith("#"):
            result["G3"].append(f"{where}:first_line_comment_missing")
        role = cell.get("metadata", {}).get("lesson_role")
        previous = cells[index - 1] if index > 0 else None
        following = cells[index + 1] if index + 1 < len(cells) else None
        if role != "setup":
            if not previous or previous["cell_type"] != "markdown":
                result["G5"].append(f"{where}:explanation_before_missing")
            if not following or following["cell_type"] != "markdown":
                result["G5"].append(f"{where}:result_reading_after_missing")
            else:
                quoted = re.findall(r"`([^`]+)`", text(following["source"]))
                produced = outputs_text(cell)
                if produced.strip() and not any(q.strip() and q.strip() in produced for q in quoted):
                    result["G5"].append(f"{where}:result_reading_quotes_no_output")
                reading = text(following["source"]).split("\n\n")[0]
                if produced.strip() and reading.startswith("**결과 읽기**"):
                    for q in re.findall(r"`([^`]+)`", reading):
                        if re.search(r"\d", q) and q.strip() not in produced:
                            result["G5"].append(f"{where}:result_reading_number_not_in_output:{q}")
    return result


def figure_numbers(mmd: str) -> list[str]:
    labels = re.findall(r'"([^"]*)"|\[([^\]]*)\]|\(([^)]*)\)', mmd)
    numbers = []
    for groups in labels:
        label = next((g for g in groups if g), "")
        numbers += re.findall(r"\d[\d,.]*\d|\d{2,}", label)
    return numbers


def check_section(chapter: Path, lab: Path, slug: str) -> dict:
    number = slug[:2]
    source_path = chapter / "_src" / f"{slug}.html"
    raw = source_path.read_text(encoding="utf-8")
    notebook = check_notebook(lab / "notebooks" / f"{slug}.ipynb")
    prose_notebook = g6_prose("\n\n".join(notebook.pop("prose")))
    prose_source = g6_prose(raw)
    figures = chapter / "figures"
    mermaid_tokens = re.findall(r"\{\{mermaid:([^|}]+)", raw)
    image_tokens = re.findall(r"\{\{img:([^|}]+)", raw)
    prompts = sorted(p.name for p in figures.glob(f"{number}-*.prompt.md"))
    g7: list[str] = []
    if not 3 <= len(mermaid_tokens) <= 5:
        g7.append(f"mermaid_count:{len(mermaid_tokens)}")
    illustrations = len(set(image_tokens)) + len([p for p in prompts if p.replace(".prompt.md", "") not in image_tokens])
    if not 1 <= illustrations <= 2:
        g7.append(f"illustration_count:{illustrations}")
    if not (chapter / "qa" / "upgrade" / f"{number}-figures.md").is_file():
        g7.append("figure_design_table_missing")
    nb_json = json.loads((lab / "notebooks" / f"{slug}.ipynb").read_text(encoding="utf-8"))
    all_outputs = "".join(outputs_text(c) for c in nb_json["cells"] if c["cell_type"] == "code")
    for name in mermaid_tokens:
        mmd = figures / f"{name}.mmd"
        for suffix in (".mmd", ".svg", ".png", ".caption.md"):
            if not (figures / f"{name}{suffix}").is_file():
                g7.append(f"{name}{suffix}_missing")
        if mmd.is_file():
            missing = [n for n in figure_numbers(mmd.read_text(encoding="utf-8")) if n not in all_outputs and n not in raw]
            if missing:
                g7.append(f"{name}:label_numbers_not_in_outputs:{','.join(sorted(set(missing)))}")
    for name in image_tokens:
        if not (figures / f"{name}.caption.md").is_file():
            g7.append(f"{name}.caption.md_missing")
    g6 = {
        "sentences": prose_source["sentences"] + prose_notebook["sentences"],
        "long": prose_source["long"] + prose_notebook["long"],
        "english_start": prose_source["english_start"] + prose_notebook["english_start"],
        "banned": prose_source["banned"] + prose_notebook["banned"],
        "dense_paragraphs": prose_source["dense_paragraphs"] + prose_notebook["dense_paragraphs"],
    }
    gates = {
        "G1": notebook["G1"], "G2": notebook["G2"], "G3": notebook["G3"], "G4": notebook["G4"], "G5": notebook["G5"],
        "G6": [f"long:{s}" for s in g6["long"]] + [f"english_start:{s}" for s in g6["english_start"]]
              + [f"banned:{s}" for s in g6["banned"]] + [f"dense_paragraph:{s}" for s in g6["dense_paragraphs"]],
        "G7": g7,
    }
    return {"slug": slug, "code_cells": notebook["code_cells"], "sentences": g6["sentences"],
            "counts": {key: len(value) for key, value in gates.items()},
            "passed": all(not value for value in gates.values()), "issues": gates}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("chapter", type=Path)
    parser.add_argument("--label", default="after")
    parser.add_argument("--section", help="두 자리 절 번호만 검사")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    chapter = (args.chapter if args.chapter.is_absolute() else ROOT / args.chapter).resolve()
    if (chapter / "chapter.json").is_file():
        config = json.loads((chapter / "chapter.json").read_text(encoding="utf-8"))
        lab = ROOT / config["lab_path"]
        all_slugs = [s["slug"] for s in config["sections"]]
    else:  # chapter.json 없이 자체 _build.py를 쓰는 챕터(Ch 8~10)
        config = {"chapter": chapter.name}
        lab = ROOT / "labs" / chapter.relative_to(ROOT / "textbook")
        all_slugs = sorted(p.stem for p in (chapter / "_src").glob("[0-9][0-9]-*.html"))
    sections = [slug for slug in all_slugs if not args.section or slug.startswith(args.section)]
    reports = [check_section(chapter, lab, slug) for slug in sections]
    totals = {gate: sum(r["counts"][gate] for r in reports) for gate in ["G1", "G2", "G3", "G4", "G5", "G6", "G7"]}
    summary = {"chapter": config["chapter"], "label": args.label, "totals": totals,
               "passed_sections": sum(r["passed"] for r in reports), "sections": reports}
    out = chapter / "qa" / "upgrade" / (f"gates-{args.label}.json" if not args.section else f"gates-{args.label}-{args.section}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"totals": totals, "passed_sections": f"{summary['passed_sections']}/{len(reports)}", "report": str(out.relative_to(ROOT))}, ensure_ascii=False))
    for r in reports:
        print(r["slug"], r["counts"], "PASS" if r["passed"] else "")
    return 1 if args.strict and not all(r["passed"] for r in reports) else 0


if __name__ == "__main__":
    raise SystemExit(main())
