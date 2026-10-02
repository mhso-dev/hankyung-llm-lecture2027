from __future__ import annotations

import re


API_EXPLANATIONS = [
    (r"StateGraph\(", "`StateGraph(StateType)`은 상태 형식을 입력으로 받아 그래프 설계 객체를 만듭니다."),
    (r"\.add_node\(", "`add_node(name, function)`은 그래프 이름과 실제 실행할 함수를 연결하며, 이 호출만으로 함수 본문이 실행되지는 않습니다."),
    (r"\.add_edge\(", "`add_edge(from, to)`는 두 노드의 고정 이동 순서를 등록합니다."),
    (r"\.add_conditional_edges\(", "`add_conditional_edges(source, path)`는 source가 끝난 뒤 path 함수를 호출해 다음 목적지를 고릅니다."),
    (r"\.compile\(\)", "`compile()`은 선언한 노드와 엣지로 `invoke()`할 실행 객체를 반환합니다."),
    (r"\.invoke\(", "`invoke(input)`가 나타나는 줄에서 실제 그래프 또는 모델 실행이 시작되고 반환값이 왼쪽 변수에 저장됩니다."),
    (r"Annotated\[", "`Annotated[value_type, reducer]`는 값의 형식과 새 갱신을 합칠 함수를 함께 표시합니다."),
    (r"add_messages\(", "`add_messages(left, right)`는 메시지 ID를 기준으로 새 메시지를 추가하거나 같은 ID의 메시지를 교체한 목록을 반환합니다."),
    (r"HumanMessage\(", "`HumanMessage(content=..., id=...)`는 사용자 역할의 본문과 식별자를 가진 메시지 객체를 만듭니다."),
    (r"AIMessage\(", "`AIMessage(content=..., id=...)`는 모델 역할의 메시지 객체를 만듭니다."),
    (r"Send\(", "`Send(node, arg)`는 실행할 노드 이름과 그 실행 하나에 전달할 작은 상태를 묶습니다."),
    (r"Command\(", "`Command(update=..., goto=...)`는 상태 갱신값과 다음 목적지를 함께 반환합니다."),
    (r"draw_mermaid\(", "`draw_mermaid()`는 컴파일된 그래프의 노드와 연결을 Mermaid 문자열로 반환하며 그래프를 다시 실행하지 않습니다."),
    (r"OpenAIEmbeddings\(", "`OpenAIEmbeddings(...)`는 문자열을 수치 벡터로 변환할 임베딩 클라이언트를 준비합니다. 실제 호출은 `embed_query()`나 `embed_documents()`에서 일어납니다."),
    (r"embed_documents\(", "`embed_documents(texts)`는 여러 문장을 입력받아 문장 수만큼의 벡터를 반환합니다."),
    (r"embed_query\(", "`embed_query(text)`는 검색 질문 한 개를 벡터 하나로 반환합니다."),
    (r"cosine_similarity\(", "`cosine_similarity(A, B)`는 두 벡터 묶음의 방향 유사도를 행렬로 반환하며 정답 확률을 반환하지 않습니다."),
    (r"BM25Okapi\(", "`BM25Okapi(tokenized_documents)`는 토큰 목록으로 희소 검색 점수를 계산할 인덱스를 준비합니다."),
    (r"CrossEncoder\(", "`CrossEncoder(model_name)`은 질문·문서 쌍을 함께 읽어 재정렬 점수를 계산할 모델을 준비합니다."),
    (r"init_chat_model\(", "`init_chat_model(...)`은 채팅 모델 객체를 만들며, 이 줄에서는 아직 답변을 생성하지 않습니다."),
    (r"json\.loads\(", "`json.loads(text)`는 JSON 문자열을 파이썬 딕셔너리나 목록으로 변환해 반환합니다."),
    (r"\.read_text\(", "`read_text()`는 파일 내용을 문자열로 반환합니다."),
    (r"\.write_text\(", "`write_text(text)`가 실행되는 줄에서 문자열이 실제 파일에 저장됩니다."),
    (r"hashlib\.sha256\(", "`sha256(bytes)`는 같은 입력인지 비교할 해시 객체를 만들며 원문을 복원하는 암호화 함수가 아닙니다."),
    (r"re\.sub\(", "`re.sub(pattern, replacement, text)`는 패턴에 맞는 부분을 replacement로 바꾼 새 문자열을 반환합니다."),
    (r"re\.findall\(", "`re.findall(pattern, text)`는 패턴과 일치한 항목 목록을 반환합니다."),
    (r"@dataclass", "`@dataclass`는 아래 클래스의 필드로 초기화 메서드 등을 만들어 주는 데코레이터입니다."),
    (r"nearest_rank\(", "`nearest_rank(values, percentile)`은 값을 정렬한 뒤 지정 백분위의 가장 가까운 순위 값을 반환합니다."),
]


def _source(cell: dict) -> str:
    value = cell.get("source", "")
    return "".join(value) if isinstance(value, list) else value


def explain_code(source: str) -> str:
    statements: list[str] = []
    executable_source = "\n".join(
        line for line in source.splitlines()
        if not line.lstrip().startswith("#")
    )
    if executable_source.lstrip().startswith("%pip"):
        return ("\n\n**이 셀의 코드 읽기.** `%pip install`은 이 노트북 커널이 사용할 "
                "패키지를 설치합니다. 앞 셀의 값을 입력으로 사용하지 않으며, 설치가 끝난 뒤의 "
                "코드 셀에서 패키지를 가져와 사용합니다.")
    if re.search(r"^trace\s*=\s*\{", executable_source, flags=re.MULTILINE):
        return "\n\n**이 셀의 코드 읽기.** 이 셀은 한 요청의 시작·종료 시각과 children에 담을 단계별 시각을 고정된 합성값으로 새로 만듭니다. 실제 요청을 실행해 측정한 시간이 아니며, 다음 셀에서 기록 구조와 소요 시간 계산을 관찰하기 위한 자료입니다."
    definitions = re.findall(r"^def\s+([A-Za-z_]\w*)\(([^)]*)\)", source, flags=re.MULTILINE)
    classes = re.findall(r"^class\s+([A-Za-z_]\w*)", source, flags=re.MULTILINE)
    if classes:
        names = ", ".join(f"`{name}`" for name in classes[:3])
        statements.append(f"이 셀을 실행하면 {names} 클래스 정의가 준비됩니다. 클래스 본문은 정의 시 처리되지만 인스턴스 값은 나중에 객체를 만들 때 생깁니다.")
    if definitions:
        rendered = ", ".join(f"`{name}({params.strip()})`" for name, params in definitions[:3])
        statements.append(f"{rendered}는 함수를 정의하는 표기입니다. 이 셀에서는 함수 객체만 준비되고 들여쓴 본문은 뒤에서 함수를 호출할 때 실행됩니다.")
        if "return " in source:
            statements.append("`return` 뒤의 값은 화면 출력이 아니라 호출한 코드로 전달되는 반환값입니다.")
        names = {name for name, _ in definitions}
        if "retry_with_fallback" in names:
            statements.append("`attempts`는 주 처리의 최대 호출 횟수입니다. 이 함수는 `TimeoutError`만 잡고, 세 번째 반환값에는 폴백 호출 한 번까지 포함한 총 호출 수를 담습니다.")
        if "safe_audit" in names:
            statements.append("`safe_audit`는 event, 마스킹된 query, query_hash, detail만 JSONL 한 행으로 저장하며 오류 종류와 호출 횟수는 저장하지 않습니다.")
    for pattern, explanation in API_EXPLANATIONS:
        if re.search(pattern, executable_source) and explanation not in statements:
            if pattern == r"\.invoke\(" and definitions:
                statements.append("`invoke(input)`는 정의한 함수를 뒤에서 호출할 때 해당 함수 본문 안에서 모델이나 그래프를 실행하고 응답 객체를 반환합니다.")
            else:
                statements.append(explanation)
        if len(statements) >= 5:
            break
    if "for " in source and not definitions:
        statements.append("`for` 블록은 입력 항목을 하나씩 처리하며, 반복이 끝난 뒤 모은 값이 다음 셀의 입력이 됩니다.")
    if "try:" in source and "except " in source:
        caught = ", ".join(re.findall(r"except\s+([^:\n]+)", source))
        statements.append(f"`try` 안의 작업에서 {caught} 예외가 발생할 때만 대응하는 `except` 블록이 실행됩니다.")
    if "print(" in source:
        statements.append("`print()`는 확인용 문자열을 화면에 표시할 뿐 함수의 반환값을 바꾸지 않습니다.")
    if "assert " in source:
        statements.append("`assert`는 조건이 참이면 출력 없이 통과하고 거짓이면 실행을 중단하므로, 바로 앞 결과를 검증하는 역할을 합니다.")
    if not statements:
        statements.append("이 셀은 앞 셀에서 만든 값을 입력으로 읽어 위에서 아래 순서로 처리하고, 왼쪽 변수에 다음 셀이 사용할 결과를 저장합니다.")
    return "\n\n**이 셀의 코드 읽기.** " + " ".join(statements[:6])


def inject_guidance(notebook: dict) -> dict:
    cells = notebook["cells"]
    index = 0
    guide_number = 1
    while index < len(cells):
        cell = cells[index]
        if cell.get("cell_type") != "code":
            index += 1
            continue
        source = _source(cell)
        note = explain_code(source)
        if index > 0 and cells[index - 1].get("cell_type") == "markdown":
            previous = _source(cells[index - 1])
            if "**이 셀의 코드 읽기.**" in previous:
                previous = previous.split("\n\n**이 셀의 코드 읽기.**", 1)[0]
            cells[index - 1]["source"] = (previous.rstrip() + note + "\n").splitlines(keepends=True)
        else:
            metadata = {}
            if "lesson_part" in cell.get("metadata", {}):
                metadata["lesson_part"] = cell["metadata"]["lesson_part"]
            cells.insert(index, {
                "cell_type": "markdown",
                "id": f"code-guide-{guide_number:02d}",
                "metadata": metadata,
                "source": ("### 다음 코드 셀 읽기" + note + "\n").splitlines(keepends=True),
            })
            guide_number += 1
            index += 1
        index += 1
    return notebook
