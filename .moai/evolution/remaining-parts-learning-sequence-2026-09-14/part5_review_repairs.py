"""독립 검토에서 확인된 Part 5 설명 오류와 코드 직전 안내를 보정한다."""

from __future__ import annotations
raise SystemExit("옛 Part 5 보조 스크립트(part5_review_repairs.py)입니다. 실행하면 Ch 18~20 개선본을 옛 글로 덮어씁니다. 개선본은 각 챕터 qa/upgrade/author_NN.py를 쓰세요.")

import hashlib
import json
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[3]
EVOLUTION = Path(__file__).resolve().parent
ENRICH = runpy.run_path(str(EVOLUTION / "part5_enrich.py"), run_name="part5_enrich_data")
LESSONS = ENRICH["LESSONS"]
markdown_body_to_html = ENRICH["markdown_body_to_html"]


CH18_DIRECT = {
    "동기 API 호출과 사용량 측정에 필요한 도구를 준비합니다.":
        "`load_dotenv(find_dotenv(usecwd=True))`는 현재 폴더에서 위로 올라가며 `.env`를 찾아 환경 변수에 넣습니다. `OpenAI(timeout=45.0, max_retries=0)`는 동기 클라이언트를 만들며 아직 모델을 호출하지 않습니다. `calls`는 이후 성공 응답의 지연과 토큰 수를 모을 빈 목록입니다.",
    "비동기 API 호출과 사용량 측정에 필요한 도구를 준비합니다.":
        "`load_dotenv(find_dotenv(usecwd=True))`는 현재 폴더에서 위로 올라가며 `.env`를 찾아 환경 변수에 넣습니다. `AsyncOpenAI(timeout=45.0, max_retries=0)`는 비동기 클라이언트를 만들며 아직 모델을 호출하지 않습니다. `calls`는 이후 성공 응답의 지연과 토큰 수를 모을 빈 목록입니다.",
    "동기 Responses API의 JSON 응답과 사용량을 기록합니다.":
        "`call_json(instructions, prompt, limit)`은 지시문·사용자 입력·최대 출력 토큰을 받습니다. 함수 안의 `client.responses.create()`에서 실제 요청이 발생하며, 응답의 JSON 텍스트를 파이썬 사전으로 바꾸어 반환합니다. `calls`에는 성공 응답의 지연과 입력·출력 토큰만 추가됩니다.",
    "비동기 Responses API의 JSON 응답과 사용량을 기록합니다.":
        "`call_json(instructions, prompt, limit)`은 지시문·사용자 입력·최대 출력 토큰을 받는 코루틴입니다. `await client.responses.create()`에서 실제 요청을 기다리고, 응답의 JSON 텍스트를 파이썬 사전으로 바꾸어 반환합니다. `calls`에는 성공 응답의 지연과 입력·출력 토큰만 추가됩니다.",
    "동기 응답의 answer 형식을 엄격하게 검사합니다.":
        "`call_answer()`는 `answer` 문자열 하나만 허용하는 JSON Schema를 요청에 넣습니다. SDK 응답을 사전으로 바꾼 뒤 값이 문자열이며 비어 있지 않은지 다시 검사하고 사전을 반환합니다. 스키마 통과는 답의 사실 정확성까지 보장하지 않습니다.",
    "비동기 응답의 answer 형식을 엄격하게 검사합니다.":
        "`call_answer()`는 `answer` 문자열 하나만 허용하는 JSON Schema를 요청에 넣는 코루틴입니다. 비동기 SDK 응답을 사전으로 바꾼 뒤 값이 문자열이며 비어 있지 않은지 다시 검사하고 사전을 반환합니다. 스키마 통과는 답의 사실 정확성까지 보장하지 않습니다.",
    "반환된 토큰 사용량으로 할인 없는 비용을 추정합니다.":
        "`cost_usd(records)`는 앞에서 모은 성공 응답의 입력·출력 토큰을 합산해 이 실습에 고정한 단가를 적용합니다. `score_of(data)`는 평가 점수가 불리언이 아닌 숫자이며 0~100 범위인지 확인한 뒤 정수로 반환합니다. 두 함수 모두 모델을 호출하지 않습니다.",
}


CH19_DIRECT = {
    "Ch 4의 검증한 조회 함수 본문을 그대로 사용합니다.":
        "다음 셀은 Ch 4에서 검증한 `fetch_orders(csv_path, status=...)`의 본문을 같은 입력·반환 형식으로 다시 선언합니다. CSV 경로와 선택 상태를 받아 각 행을 사전으로 담은 목록을 반환하며, 아직 LangChain 도구를 만들거나 모델을 호출하지 않습니다.",
    "Ch 4의 검증한 조회 함수를 준비합니다.":
        "다음 셀은 Ch 4의 `fetch_orders(csv_path, status=...)`를 같은 입력·반환 형식으로 다시 선언합니다. CSV 경로와 선택 상태를 받아 각 행을 사전으로 담은 목록을 반환하며, 아직 LangChain 도구를 만들거나 모델을 호출하지 않습니다.",
    "Ch 4의 조회 함수를 준비합니다.":
        "다음 셀은 Ch 4의 `fetch_orders()`를 이 노트북에서 독립 실행할 수 있도록 준비합니다. CSV 경로와 선택 상태를 입력받고 사전 목록을 반환하며, 뒤에서 Pydantic 입력·반환 검증의 대상 함수가 됩니다.",
    "세 도구가 함께 사용할 조회 함수를 준비합니다.":
        "다음 셀은 세 도구가 함께 호출할 `fetch_orders()`를 준비합니다. CSV 경로와 선택 상태를 입력받아 사전 목록을 반환하므로, 뒤의 도구들은 파일 읽기 코드를 반복하지 않고 선택 목적만 다르게 정의할 수 있습니다.",
    "상태별 목록 도구에 선택 조건을 설명합니다.":
        "`@tool`은 바로 아래 함수를 `StructuredTool`로 감싸며 함수 이름·문서 문자열·타입 힌트를 설명서로 만듭니다. `list_orders_by_status()`는 상태 문자열을 입력받아 여러 주문 사전을 반환하고, 이 셀에서는 도구 정의만 하므로 모델이나 CSV 조회는 아직 실행되지 않습니다.",
    "한 건 조회와 금액 집계의 이름·반환 목적을 구분합니다.":
        "다음 셀은 정확한 ID로 한 행을 찾는 도구와 상태별 건수·합계를 계산하는 도구를 정의합니다. 둘 다 `@tool`로 감싸지만 입력 이름과 반환 모양이 다릅니다. 함수 본문은 실제 `invoke()`가 호출될 때 실행됩니다.",
    "읽기 도구가 조회할 주문 행을 메모리에 준비합니다.":
        "다음 셀의 `ORDERS`는 외부 시스템 대신 사용할 교육용 주문 목록입니다. 각 사전은 주문 ID·상태·금액을 담고, 뒤의 읽기 도구는 이 목록에서 한 행을 찾습니다. 목록을 선언하는 것만으로 읽기나 취소 동작이 실행되지는 않습니다.",
    "같은 모델과 temperature를 두 비교 조건에 사용합니다.":
        "다음 셀은 두 설명 조건에 공통으로 사용할 모델과 생성 설정을 만듭니다. 같은 모델·온도를 유지해야 뒤에서 관찰한 선택 차이를 설명 문구의 차이와 연결할 수 있습니다. 실제 호출은 각 조건의 `invoke()`가 실행될 때 시작됩니다.",
    "두 조건이 공유하는 주문 조회 함수를 준비합니다.":
        "다음 셀은 모호한 설명 조건과 구체적 설명 조건이 함께 사용할 주문 조회 함수를 준비합니다. 두 조건에서 함수 본문과 반환값을 같게 두어 모델에게 보이는 설명만 비교 변수로 남깁니다.",
    "한 건 조회와 집계 도구의 사용 조건을 적습니다.":
        "다음 셀은 정확한 주문 ID 조회와 상태별 금액 집계를 정의합니다. 두 조건의 공개 도구 이름과 입력 스키마는 같게 유지하고 문서 문자열만 다르게 만들 수 있도록 함수 역할을 분리합니다.",
    "같은 모델을 도구 요청과 최종 답변에 사용합니다.":
        "다음 셀은 도구 요청을 만드는 첫 호출과 도구 결과를 읽는 마지막 호출에 공통으로 쓸 모델을 만듭니다. 모델 객체 생성만으로 API 요청은 발생하지 않으며, 뒤의 `invoke()`에서 실제 호출이 시작됩니다.",
    "주문 CSV를 읽는 함수를 준비합니다.":
        "다음 셀은 주문 CSV 경로와 선택 상태를 받아 사전 목록을 반환하는 `fetch_orders()`를 준비합니다. 뒤의 두 도구가 같은 데이터 읽기 규칙을 사용하도록 하며, 정의 시점에는 파일을 읽지 않습니다.",
    "상태로 목록을 조회하는 도구를 준비합니다.":
        "`list_orders_by_status(status)`는 상태 문자열을 받아 여러 주문을 반환하는 읽기 도구입니다. `@tool`이 설명서를 만들고 실제 CSV 조회는 도구의 `invoke()`가 호출될 때 실행됩니다.",
    "주문 ID로 한 건을 조회하는 도구를 준비합니다.":
        "`get_order_by_id(order_id)`는 ID 문자열을 받아 일치하는 주문 사전 하나를 반환합니다. 일치 항목이 없으면 오류 사전을 반환합니다. `@tool`은 이 입력과 반환 목적을 모델이 읽는 설명서로 만들며, 정의 시점에는 조회가 실행되지 않습니다.",
    "모델과 도구 호출 비용을 준비합니다.":
        "다음 셀은 모델 이름과 토큰 단가, 응답의 사용량을 읽는 `usage_of()`를 정의합니다. 실제 모델 요청은 뒤에서 도구를 바인딩한 모델의 `invoke()`를 호출할 때 발생합니다.",
}


def comment_text(cell: dict) -> str:
    first = "".join(cell["source"]).splitlines()[0].strip()
    return first.removeprefix("#").strip()


def new_markdown(key: str, index: int, text: str, lesson_part: str | None) -> dict:
    metadata = {"revision": "2026-09-14-direct-cell-reading"}
    if lesson_part:
        metadata["lesson_part"] = lesson_part
    return {
        "cell_type": "markdown",
        "id": hashlib.sha256(f"{key}:{index}:direct".encode()).hexdigest()[:8],
        "metadata": metadata,
        "source": ("### 다음 셀을 읽는 방법\n\n" + text + "\n").splitlines(keepends=True),
    }


def update_revision_cells(path: Path, key: str) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    before, applied = LESSONS[key]
    for cell in data["cells"]:
        if cell.get("metadata", {}).get("revision") != "2026-09-14-first-use-depth":
            continue
        current = "".join(cell["source"])
        cell["source"] = (before if current.startswith("## 코드를") else applied).splitlines(keepends=True)
    return data


def add_direct_guides(data: dict, key: str) -> None:
    if any(c.get("metadata", {}).get("revision") == "2026-09-14-direct-cell-reading" for c in data["cells"]):
        return
    chapter = key.split("/", 1)[0]
    mapping = CH18_DIRECT if chapter == "ch18-workflow-patterns" else CH19_DIRECT
    cells = []
    for index, cell in enumerate(data["cells"]):
        if cell["cell_type"] == "code" and cells and cells[-1]["cell_type"] == "code":
            explanation = mapping.get(comment_text(cell))
            if explanation is None:
                raise ValueError(f"코드 직전 설명을 찾을 수 없습니다: {key} / {comment_text(cell)}")
            part = cell.get("metadata", {}).get("lesson_part")
            cells.append(new_markdown(key, index, explanation, part))
        cells.append(cell)
    data["cells"] = cells


def update_source(key: str) -> None:
    chapter, slug = key.split("/", 1)
    path = ROOT / "textbook/part5" / chapter / "_src" / f"{slug}.html"
    source = path.read_text(encoding="utf-8")
    start = source.index("<h3>코드를 읽기 전에</h3>")
    end = source.index("<h3>다른 상황과 개념 경계</h3>", start)
    before = LESSONS[key][0]
    replacement = "<h3>코드를 읽기 전에</h3>" + markdown_body_to_html(before)
    path.write_text(source[:start] + replacement + source[end:], encoding="utf-8")


def replace_in_file(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            return
        raise ValueError(f"교체할 문구가 없습니다: {relative} / {old}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def main() -> None:
    for key in LESSONS:
        chapter, slug = key.split("/", 1)
        notebook = ROOT / "labs/part5" / chapter / "notebooks" / f"{slug}.ipynb"
        data = update_revision_cells(notebook, key)
        if chapter in {"ch18-workflow-patterns", "ch19-model-tools"}:
            add_direct_guides(data, key)
        if key.endswith("ch18-workflow-patterns/03-병렬-섹셔닝과-투표"):
            for cell in data["cells"]:
                if cell["cell_type"] == "code":
                    cell["source"] = [line.replace("완료 순서 보존:", "입력 순서대로 반환:") for line in cell["source"]]
        notebook.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        update_source(key)

    replace_in_file(
        "textbook/part5/ch18-workflow-patterns/_src/04-동적-오케스트레이터와-워커.html",
        "2개보다 적으면 고정된 기본 목록으로 바꾸어 오류를 숨기지 않고 중단합니다.",
        "2개보다 적으면 고정된 기본 목록으로 바꾸지 않고 오류를 숨기지 않은 채 중단합니다.",
    )
    replace_in_file(
        "textbook/part5/ch20-tool-node/_src/01-ToolNode와-tools-condition.html",
        "이때 MessagesState의 add_messages 리듀서가 HumanMessage, AIMessage, ToolMessage를 실행 순서대로 보존합니다.",
        "이때 직접 정의한 AgentState의 messages 필드에 붙인 add_messages 리듀서가 HumanMessage, AIMessage, ToolMessage를 실행 순서대로 보존합니다. trace 필드는 실행한 노드 이름을 별도로 누적합니다.",
    )
    replace_in_file(
        "textbook/part5/ch20-tool-node/_src/03-recursion-limit과-명시적-종료.html",
        "상태에 남은 작업 수를 두고 END로 이동하는 명시적 종료 조건을 구현할 수 있습니다.",
        "상태에 누적한 실행 횟수를 기준으로 END로 이동하는 명시적 종료 조건을 구현할 수 있습니다.",
    )
    old_observe = (
        "섹셔닝 세 호출의 반환 목록은 목적, 절차, 지원 순서를 보존했습니다. 병렬 벽시계 시간은 "
        "4.619초였고 개별 호출 지연의 합은 9.263초였습니다. 이 한 번의 실행에서는 함께 기다린 "
        "시간이 개별 지연 합보다 짧았습니다. 투표 원자료는 A, A, B였으며 유효표 집계는 A 2표, "
        "B 1표였습니다. 집계에서 제외한 표는 0개였습니다. 전체 성공 응답은 8개, 입력 1,257토큰, "
        "출력 555토큰, 사용량 기준 추정 비용은 0.003440달러였습니다."
    )
    new_observe = (
        "섹셔닝 세 호출의 반환 목록은 목적, 절차, 지원이라는 입력 순서로 나타났습니다. 병렬 벽시계 "
        "시간은 3.268초였고 개별 호출 지연의 합은 9.431초였습니다. 이 한 번의 실행에서는 함께 "
        "기다린 시간이 개별 지연 합보다 짧았습니다. 투표 원자료는 A, tie, A였으며 유효표 집계는 "
        "A 2표였습니다. 집계에서 제외한 표는 1개였습니다. 전체 성공 응답은 8개, 입력 1,233토큰, "
        "출력 549토큰, 사용량 기준 추정 비용은 0.003395달러였습니다."
    )
    old_interpretation = (
        "이 결과는 <code>gather</code>가 호출을 겹쳐 기다렸다는 한 번의 관찰입니다. 이번에 9.263초의 "
        "개별 지연 합과 4.619초의 벽시계 시간 사이에서 나타난 차이가 반복된다고 일반화할 수 없습니다. "
        "서비스 부하와 네트워크가 바뀌면 지연도 달라집니다. 투표 결과 A는 이 세 평가 프롬프트의 "
        "결과이며 정답이나 보편적 선호를 뜻하지 않습니다. A와 B가 같은 수를 받으면 <code>tie</code>, "
        "유효표가 하나도 없으면 <code>undecided</code>로 반환합니다."
    )
    new_interpretation = (
        "이 결과는 <code>gather</code>가 호출을 겹쳐 기다렸다는 한 번의 관찰입니다. 이번에 9.431초의 "
        "개별 지연 합과 3.268초의 벽시계 시간 사이에서 나타난 차이가 반복된다고 일반화할 수 없습니다. "
        "서비스 부하와 네트워크가 바뀌면 지연도 달라집니다. 투표 결과 A는 이 세 평가 프롬프트의 "
        "결과이며 정답이나 보편적 선호를 뜻하지 않습니다. 한 평가자의 <code>tie</code>는 원표에 "
        "남지만 A/B 승자 집계에서는 제외됐습니다. A와 B가 같은 수를 받으면 <code>tie</code>, 유효표가 "
        "하나도 없으면 <code>undecided</code>로 반환합니다."
    )
    for target in [
        "textbook/part5/ch18-workflow-patterns/_src/03-병렬-섹셔닝과-투표.html",
        "textbook/part5/ch18-workflow-patterns/_author.py",
    ]:
        replace_in_file(target, old_observe, new_observe)
        replace_in_file(target, old_interpretation, new_interpretation)
    print("Part 5 독립 검토 보정과 코드 직전 설명을 반영했습니다.")


if __name__ == "__main__":
    main()
