"""Create one new chapter and its first lesson without overwriting files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SLUG = re.compile(r"^[0-9A-Za-z가-힣][0-9A-Za-z가-힣_-]*$")
CHAPTER_SLUG = re.compile(r"^ch\d{2}-[0-9A-Za-z가-힣][0-9A-Za-z가-힣_-]*$")
SECTION_SLUG = re.compile(r"^\d{2}-[0-9A-Za-z가-힣][0-9A-Za-z가-힣_-]*$")


def _safe_child(root: Path, *parts: str) -> Path:
    target = root.joinpath(*parts).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("생성 경로가 프로젝트 루트를 벗어납니다.") from exc
    return target


def _validate_slug(value: str, label: str) -> None:
    if not SLUG.fullmatch(value) or value in {".", ".."}:
        raise ValueError(f"{label}에는 글자·숫자·밑줄·하이픈만 사용할 수 있습니다: {value!r}")


def _validate_project_slugs(chapter: str, section: str) -> None:
    _validate_slug(chapter, "chapter")
    _validate_slug(section, "section")
    if not CHAPTER_SLUG.fullmatch(chapter):
        raise ValueError("chapter는 ch와 두 자리 번호로 시작해야 합니다. 예: ch42-evaluation")
    if not SECTION_SLUG.fullmatch(section):
        raise ValueError("section은 두 자리 번호로 시작해야 합니다. 예: 01-평가-준비")


def _markdown(source: str, lesson_part: str | None = None) -> dict:
    metadata = {} if lesson_part is None else {"lesson_part": lesson_part}
    return {"cell_type": "markdown", "id": "", "metadata": metadata, "source": source.splitlines(keepends=True)}


def _code(prompt: str, lesson_part: str | None = None) -> dict:
    metadata = {} if lesson_part is None else {"lesson_part": lesson_part}
    source = f'# [[작성: {prompt}]]\nraise NotImplementedError("수업 코드를 작성한 뒤 실행하세요.")'
    return {"cell_type": "code", "execution_count": None, "id": "", "metadata": metadata, "outputs": [], "source": source.splitlines(keepends=True)}


def _notebook(title: str, lesson_format: str) -> dict:
    cells = [
        _markdown(f"# {title}\n\n[[작성: 이 실습에서 확인할 질문을 한 문장으로 씁니다.]]"),
        _markdown("## 실행 환경 준비\n\n[[작성: Python 3.12, 패키지, .env와 실습 파일 경로를 안내합니다.]]"),
        _code("빈 커널에서 필요한 패키지와 입력 파일을 준비합니다."),
        _markdown("## 기본 실행\n\n[[작성: 새 변수와 주요 인자, 반환값을 먼저 설명합니다.]]"),
        _code("가장 작은 완성 예제를 실행하고 핵심 결과를 출력합니다."),
        _markdown("## 중간 결과 관찰\n\n[[작성: 출력에서 무엇을 확인할지 설명합니다.]]"),
        _code("중간 변수 또는 반환값을 출력하고 확인 조건을 검사합니다."),
        _markdown("## 값 하나를 바꿔 비교\n\n[[작성: 한 값만 바꾸고 나머지 조건을 고정합니다.]]"),
        _code("한 값만 바꾼 결과를 기본값과 나란히 출력합니다."),
    ]
    if lesson_format == "paired":
        cells.extend([
            _markdown("## 실패 재현\n\n[[작성: 어떤 잘못된 코드가 어떤 관찰 결과를 만드는지 설명합니다.]]", "before"),
            _code("실제 실패 또는 잘못된 값을 재현하고 관찰 결과를 출력합니다.", "before"),
            _markdown("## 수정\n\n[[작성: 같은 문제에서 바꾼 코드 한 줄과 수정 이유를 설명합니다.]]", "after"),
            _code("같은 문제를 고치고 성공 결과를 출력한 뒤 검사합니다.", "after"),
        ])
    else:
        cells.extend([
            _markdown("## 반복 실험과 결과 해석\n\n[[작성: 바꿀 조건, 고정할 조건, 반복 횟수와 판정 기준을 설명합니다.]]"),
            _code("조건별 반복 실험을 실행하고 원자료와 집계 결과를 출력합니다."),
        ])
    for index, cell in enumerate(cells, 1):
        cell["id"] = f"cell-{index:02d}"
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "lesson_format": lesson_format,
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def _source(slug: str, lesson_format: str) -> str:
    notebook = f"{{{{notebook:{slug}}}}}" if lesson_format == "experiment" else f"{{{{notebook:{slug}|example}}}}"
    if lesson_format == "experiment":
        failure = "<p>[[작성: 실제 결과 표와 관찰 범위, 결론의 한계를 씁니다.]]</p>"
    else:
        failure = f"<p>[[작성: 실패 원인, 바꾼 조건과 수정 이유를 설명합니다.]]</p>{{{{notebook:{slug}|failure}}}}"
    failure_title = "실험 결과 해석" if lesson_format == "experiment" else "일부러 실패해 보기"
    return f'''<!--meta: 강의 [[작성: Nh]] | 실습 [[작성: Nh]] | 코드 Jupyter Notebook | 새 용어 [[작성: N]] -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul><li>[[작성: 관찰 가능한 학습 목표]]</li></ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>[[작성: 앞뒤 챕터와 연결되는 이유]]</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>[[작성: 필요한 선수 지식과 파일·함수]]</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>쉬운 예</h3><p>[[작성: 구체적인 상황]]</p><h3>정의</h3><p>[[작성: 처음 나오는 기술 용어를 쉬운 말과 함께 정의]]</p><h3>도식 읽기</h3><p>[[작성: 도식 자리와 축·색·화살표를 읽는 법, 또는 이 절에서 도식을 생략한 이유]]</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>[[작성: 실행 순서와 확인할 출력]]</p>{notebook}<p class="look"><b>확인할 점</b> — [[작성: 기본 실행과 값 하나 변경에서 볼 차이]]</p>
<h2 id="b6"><span class="no">6</span>{failure_title}</h2>{failure}
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>[[작성: 제한 조건과 그 이유]]</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>[[작성: 핵심 요약]]</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — [[작성: 다음 절에서 다시 쓰는 결과]]</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz"><summary>문제와 해설</summary><p class="quiz-q">[[작성: 문제]]</p><p class="quiz-a">[[작성: 정답과 해설]]</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li>[[작성: 공식 문서 URL · 확인 날짜 · 기준 버전]]</li></ul>
'''


def create_scaffold(*, root: Path, part: int, chapter: str, title: str, section: str, lesson_format: str) -> tuple[Path, Path]:
    root = root.resolve()
    if part < 1:
        raise ValueError("part는 1 이상의 정수여야 합니다.")
    _validate_project_slugs(chapter, section)
    if lesson_format not in {"paired", "experiment"}:
        raise ValueError("format은 paired 또는 experiment여야 합니다.")
    template_runtime = root / "textbook" / "_template" / "builder.py"
    notebook_runtime = root / "textbook" / "_notebook" / "render.py"
    if not template_runtime.is_file() or not notebook_runtime.is_file():
        raise FileNotFoundError("root에 textbook/_template과 textbook/_notebook 공통 도구가 필요합니다.")
    chapter_dir = _safe_child(root, "textbook", f"part{part}", chapter)
    lab_dir = _safe_child(root, "labs", f"part{part}", chapter)
    if chapter_dir.exists() or lab_dir.exists():
        raise FileExistsError("기존 챕터 또는 실습 폴더는 덮어쓰지 않습니다.")
    section_title = re.sub(r"^\d+-", "", section).replace("-", " ")
    config = {
        "part": part,
        "part_title": f"Part {part} · [[작성: 파트 이름]]",
        "chapter": chapter,
        "title": title,
        "hours": "[[작성: 총 Nh · 강의 Nh · 실습 Nh]]",
        "objectives": ["[[작성: 이 챕터를 마치면 할 수 있는 일]]"],
        "lab_path": f"labs/part{part}/{chapter}",
        "sections": [{"slug": section, "title": section_title, "format": lesson_format}],
    }
    chapter_files = {
        "chapter.json": json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        "_build.py": '''from pathlib import Path\nimport sys\n\nHERE = Path(__file__).resolve().parent\nROOT = HERE.parents[2]\nsys.path.insert(0, str(ROOT / "textbook" / "_template"))\nfrom builder import build_chapter\n\nif __name__ == "__main__":\n    for path in build_chapter(HERE, root=ROOT):\n        print("wrote", path.name)\n''',
        f"_src/{section}.html": _source(section, lesson_format),
        "집필점검표.md": """# 집필 점검표\n\n자세한 기준은 `textbook/AUTHORING.md`를 따릅니다. 각 행에 실제 셀과 출력을 기록합니다.\n\n| 확인 항목 | 작성자 기록 | 독립 검토 |\n| --- | --- | --- |\n| 학습 질문 한 문장 | [[작성: 질문]] | [[작성: 검토 결과]] |\n| 고정한 조건 | [[작성: 원문·질문·모델 등]] | [[작성: 검토 결과]] |\n| 바꾼 값 또는 실패 원인 | [[작성: 값과 이유]] | [[작성: 검토 결과]] |\n| 실제 연산과 셀 | [[작성: 메서드·셀 번호]] | [[작성: 검토 결과]] |\n| 실제 출력 | [[작성: 관찰한 값]] | [[작성: 검토 결과]] |\n| 해석 범위 | [[작성: 알 수 있는 것과 없는 것]] | [[작성: 검토 결과]] |\n\n- [ ] 모든 `[[작성: ...]]` 항목을 실제 내용으로 바꿨습니다.\n- [ ] 모든 코드 셀을 Python 3.12 새 커널에서 실행했습니다.\n- [ ] API 키·개인 경로·강사 노트가 학생 파일에 없습니다.\n""",
    }
    notebook = _notebook(section_title, lesson_format)
    for relative, content in chapter_files.items():
        path = chapter_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    notebook_path = lab_dir / "notebooks" / f"{section}.ipynb"
    notebook_path.parent.mkdir(parents=True, exist_ok=True)
    notebook_path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return chapter_dir, lab_dir


def add_section(
    *, root: Path, part: int, chapter: str, section: str, lesson_format: str, title: str | None = None
) -> tuple[Path, Path]:
    """Add a lesson to an existing scaffold without overwriting lesson files."""
    root = root.resolve()
    _validate_project_slugs(chapter, section)
    if lesson_format not in {"paired", "experiment"}:
        raise ValueError("format은 paired 또는 experiment여야 합니다.")
    chapter_dir = _safe_child(root, "textbook", f"part{part}", chapter)
    lab_dir = _safe_child(root, "labs", f"part{part}", chapter)
    config_path = chapter_dir / "chapter.json"
    if not config_path.is_file() or not lab_dir.is_dir():
        raise FileNotFoundError("먼저 같은 part와 chapter로 첫 절을 생성해야 합니다.")
    source_path = chapter_dir / "_src" / f"{section}.html"
    notebook_path = lab_dir / "notebooks" / f"{section}.ipynb"
    if source_path.exists() or notebook_path.exists():
        raise FileExistsError("기존 절 파일은 덮어쓰지 않습니다.")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("part") != part or config.get("chapter") != chapter:
        raise ValueError("chapter.json의 part 또는 chapter가 요청과 다릅니다.")
    section_number = section.split("-", 1)[0]
    if any(item.get("slug", "").split("-", 1)[0] == section_number for item in config.get("sections", [])):
        raise FileExistsError("chapter.json에 같은 절 번호가 이미 있습니다.")
    section_title = re.sub(r"^\d+-", "", section).replace("-", " ")
    config["sections"].append({"slug": section, "title": section_title, "format": lesson_format})
    source_path.write_text(_source(section, lesson_format), encoding="utf-8")
    notebook_path.parent.mkdir(parents=True, exist_ok=True)
    notebook_path.write_text(
        json.dumps(_notebook(section_title, lesson_format), ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return source_path, notebook_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--part", type=int, required=True)
    parser.add_argument("--chapter", required=True, help="예: ch42-evaluation")
    parser.add_argument("--title", required=True, help="챕터 제목")
    parser.add_argument("--section", required=True, help="예: 01-평가-준비")
    parser.add_argument("--format", choices=["paired", "experiment"], required=True, dest="lesson_format")
    parser.add_argument("--add-section", action="store_true", help="기존 챕터에 새 절만 추가")
    args = parser.parse_args()
    add_only = args.add_section
    delattr(args, "add_section")
    if add_only:
        source_path, notebook_path = add_section(**vars(args))
        print(source_path)
        print(notebook_path)
    else:
        chapter_dir, lab_dir = create_scaffold(**vars(args))
        print(chapter_dir)
        print(lab_dir)


if __name__ == "__main__":
    main()
