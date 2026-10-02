# 2026-09-28 Ch 27 01절 품질 개선: 옛 원고(_src 여덟)·노트북 여덟을 만드는 옛 생성기입니다.
# 개선본은 절마다 qa/upgrade/author_NN.py가 대신합니다(QUALITY-UPGRADE.md §8, PLAYBOOK §2-1).
# 이 파일을 실행하면 옛 판을 다시 쓰려 하므로, 아래 줄에서 실행을 막습니다. 옮기기(mv -n)는 챕터 마감 몫입니다.
from __future__ import annotations
raise SystemExit("옛 Ch 27 원고·노트북 생성기입니다. 개선본은 qa/upgrade/author_NN.py를 쓰세요.")

import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
LAB = HERE.parents[2] / "labs" / "part6" / "ch27-deepagents"
NB_DIR = LAB / "notebooks"
SRC_DIR = HERE / "_src"

SECTIONS = [
    ("01-하네스와-일곱-기능", "하네스와 일곱 기능", "하네스가 프레임워크 위에서 어떤 문제를 해결하는지 분류합니다.", "설정", "관찰"),
    ("02-create-deep-agent와-도구", "create_deep_agent와 도구", "생성 함수의 인자와 기본 도구 표면을 설치된 0.7.0에서 확인합니다.", "도구", "구성"),
    ("03-플래닝과-시스템-프롬프트", "플래닝과 시스템 프롬프트", "0.7에서 플래닝과 기본 프롬프트가 어떻게 달라졌는지 측정 범위와 함께 확인합니다.", "프롬프트", "비교"),
    ("04-파일시스템과-중간-결과", "파일시스템과 중간 결과", "FilesystemBackend로 조사 중간 결과를 실제 디스크에 저장하고 다시 읽습니다.", "파일", "저장"),
    ("05-컨텍스트-관리와-오프로딩", "컨텍스트 관리와 오프로딩", "요약과 큰 도구 결과 오프로딩이 컨텍스트 크기를 다루는 위치를 구분합니다.", "컨텍스트", "축소"),
    ("06-서브에이전트-위임", "서브에이전트 위임", "조사 역할을 서브에이전트로 분리할 때 전달되는 입력과 반환 결과를 확인합니다.", "위임", "격리"),
    ("07-출처-검증형-deep-research", "출처 검증형 deep research", "제공한 공식 자료만 조회하는 도구를 가진 조사 에이전트를 실행하고 근거 파일을 남깁니다.", "출처", "검증"),
    ("08-통합-실행과-운영-한계", "통합 실행과 운영 한계", "허용된 보고서 쓰기와 차단된 파일 쓰기를 함께 실행하고 종료 산출물을 검증합니다.", "운영", "측정"),
]

SOURCES = """<ul><li><a href=\"https://docs.langchain.com/oss/python/deepagents/overview\">Deep Agents 개요</a> — 2026-09-11 확인</li><li><a href=\"https://docs.langchain.com/oss/python/deepagents/backends\">Deep Agents 백엔드</a> — 2026-09-11 확인</li><li><a href=\"https://docs.langchain.com/oss/python/deepagents/subagents\">Deep Agents 서브에이전트</a> — 2026-09-11 확인</li><li><a href=\"https://github.com/langchain-ai/deepagents/releases/tag/deepagents%3D%3D0.7.0\">deepagents 0.7.0 릴리스</a> — 2026-09-11 확인</li><li><a href=\"https://developers.openai.com/api/docs/models/gpt-5.4-mini\">gpt-5.4-mini 모델과 가격</a> — 2026-09-11 확인</li><li><a href=\"https://github.com/langchain-ai/deepagents/blob/main/LICENSE\">Deep Agents MIT 라이선스</a> — 예제의 기관명·자료·프롬프트는 교재용으로 새로 작성했습니다.</li></ul>"""

SPECIAL = {
"01-하네스와-일곱-기능": """DeepAgents 0.7.0의 생성 함수와 미들웨어 조립 코드를 기준으로 이 장에서는 일곱 기능을 <strong>파일시스템, 서브에이전트, 컨텍스트 요약, 스킬, 장기 메모리, 파일 권한과 사람 승인, 비동기 서브에이전트</strong>로 분류합니다. 이는 현재 공개 API를 배우기 위한 분류입니다. 과거 글의 ‘4대 요소’와 숫자만 비교하지 말고 설치한 버전에서 실제로 조립되는 기능을 확인해야 합니다.""",
"02-create-deep-agent와-도구": """<code>create_deep_agent</code>는 LangChain의 <code>create_agent</code> 위에 파일시스템과 위임, 요약 미들웨어를 조립합니다. 기본 파일 도구는 <code>ls</code>, <code>read_file</code>, <code>write_file</code>, <code>edit_file</code>, <code>delete</code>, <code>glob</code>, <code>grep</code>입니다. <code>execute</code>는 실행을 지원하는 샌드박스 백엔드가 있을 때만 실제 명령을 수행합니다. 0.7에서는 <code>write_file</code>이 기존 파일 전체를 교체할 수 있으므로 권한 규칙이 중요합니다.""",
"03-플래닝과-시스템-프롬프트": """0.7.0부터 <code>TodoListMiddleware</code>와 <code>write_todos</code>는 기본 구성에서 빠졌습니다. 계획이 필요한 애플리케이션만 <code>middleware=[TodoListMiddleware()]</code>로 추가합니다. 작성된 기본 시스템 프롬프트도 비어 있으며, 파일 도구와 위임 도구의 스키마와 겹치던 설명이 줄었습니다. 릴리스 PR의 65% 감소는 <code>gpt-5.5</code>에 ‘hello’를 보낸 첫 턴에서 5,395토큰과 1,895토큰을 비교한 값입니다. 전체 작업의 총 토큰이나 모든 모델의 절감률로 일반화할 수 없습니다.""",
"04-파일시스템과-중간-결과": """<code>FilesystemBackend</code>는 에이전트가 보는 가상 경로를 지정한 <code>root_dir</code> 아래의 실제 파일에 연결합니다. 0.7의 기본 <code>virtual_mode=True</code>는 <code>..</code>로 루트 밖을 가리키는 경로를 거부합니다. 조사 에이전트는 원자료 전체를 대화에 계속 두는 대신 <code>/research/source-a.md</code>처럼 중간 결과를 저장하고 필요한 부분만 읽을 수 있습니다.""",
"05-컨텍스트-관리와-오프로딩": """컨텍스트 관리는 두 위치에서 일어납니다. <code>SummarizationMiddleware</code>는 오래된 대화 메시지를 요약하고, <code>FilesystemMiddleware</code>는 큰 도구 결과가 한도를 넘으면 파일로 옮긴 뒤 미리보기와 경로를 남깁니다. 파일을 만들었다는 사실만으로 정보가 정확해지는 것은 아닙니다. 원문 식별자와 출처 URL을 함께 저장해야 이후 요약을 검증할 수 있습니다.""",
"06-서브에이전트-위임": """서브에이전트는 별도 메시지 문맥에서 조사하고 최종 보고만 부모에게 반환합니다. 상세한 도구 출력이 부모 문맥을 채우는 일을 줄일 수 있지만, 호출 비용과 조정 시간이 추가됩니다. 부모와 선언형 서브에이전트가 같은 백엔드를 사용하면 파일 경로를 중간 결과의 인계 지점으로 쓸 수 있습니다. 완료 조건은 ‘조사하기’가 아니라 ‘URL·핵심 주장·한계를 파일에 기록하기’처럼 확인 가능하게 적습니다.""",
"07-출처-검증형-deep-research": """이 실습의 deep research는 웹 전체를 자율 탐색하지 않습니다. 교재가 미리 검증해 제공한 Deep Agents 공식 문서와 0.7.0 릴리스 자료를 <code>source_lookup</code> 도구로 조회합니다. 따라서 실행 결과는 <strong>제공 자료에 대한 출처 검증형 조사</strong>입니다. 검색 누락, 상충 자료 탐색, 웹페이지 변경 감지는 포함하지 않으며 실제 서비스에서는 검색 도구와 URL 허용 정책을 별도로 설계해야 합니다.""",
"08-통합-실행과-운영-한계": """통합 에이전트는 기능 수보다 실행 경계를 먼저 정합니다. 이 실습은 <code>/run/report.md</code> 쓰기를 허용하고 <code>/blocked.txt</code> 쓰기를 거부합니다. 종료는 모델의 완료 문장이 아니라 허용된 파일 본문, 거부 ToolMessage, 차단 파일의 부재를 함께 검사해 판정합니다.""",
}

DETAILS = {
"01-하네스와-일곱-기능": {
"why":"Ch 6에서 그린 계층 지도에서는 하네스를 모델 호출 바깥의 실행 틀로만 표시했습니다. 이제 설치된 패키지의 조립 코드를 읽어 그 틀이 실제로 무엇을 더하는지 확인합니다. 기능을 일곱 이름으로 외우는 것이 목적이 아니라, 파일이 사라졌는지·위임 도구가 없는지·요약이 동작하지 않는지에 따라 확인할 위치를 찾는 것이 목적입니다.",
"prior":"Ch 21의 create_agent는 모델과 도구의 반복을 만들었습니다. Ch 23의 체크포인터는 실행 상태를 이어 주었고 Ch 24는 사람 승인을, Ch 26은 위임 구조를 다뤘습니다. DeepAgents는 이 기능을 대체하지 않고 LangChain과 LangGraph 위에서 긴 작업에 자주 필요한 구성을 묶습니다.",
"diagram":"LangChain create_agent에서 시작해 DeepAgents 하네스를 거쳐 7개 기능과 긴 작업 실행으로 내려갑니다. 세 번째 상자의 7개 기능은 모두 항상 활성화된다는 뜻이 아닙니다. skills·memory·permissions·async subagents는 인자를 전달할 때 추가됩니다.",
"run":"설치된 create_deep_agent 소스에서 일곱 미들웨어 이름을 찾습니다. 출력의 True는 해당 조립 경로가 소스에 존재한다는 뜻입니다. 이어서 True의 개수를 세고 7인지 검증합니다.",
"interpret":"실행 결과에서 파일시스템·서브에이전트·컨텍스트 요약·스킬·장기 메모리·권한과 사람 승인·비동기 서브에이전트가 모두 True였고 합계는 7이었습니다. 이 실험은 코드 경로의 존재를 확인합니다. 실제 도구 선택과 저장 결과는 뒤 절에서 별도로 실행합니다.",
"next":"다음 절에서는 이름 목록을 넘어 create_deep_agent가 만든 그래프에 질문을 보내고 course_lookup 도구가 선택되는지 확인합니다.",
"quiz":[("일곱 기능 중 인자를 전달할 때만 조립되는 예를 두 가지 쓰세요.","skills, memory, permissions/HITL, async subagents 중 두 가지를 들 수 있습니다."),("모든 값이 True이면 기능 품질도 검증된 것인가요?","아닙니다. 소스에 조립 경로가 있음을 확인했으며 실제 선택과 결과 품질은 실행 평가가 필요합니다."),("하네스와 LangGraph의 관계를 설명하세요.","DeepAgents는 LangChain의 에이전트 구성과 LangGraph 런타임 위에 긴 작업용 기능을 미리 조립합니다.")]},
"02-create-deep-agent와-도구": {
"why":"함수 시그니처만 읽으면 tools 인자가 있다는 사실은 알 수 있지만 모델이 도구를 선택하고 결과를 다시 읽는지는 알 수 없습니다. 이 절은 Chapter 27이라는 고정 입력을 course_lookup에 전달하고 HumanMessage → AIMessage → ToolMessage → AIMessage 순서를 실제로 확인합니다.",
"prior":"Ch 19에서 @tool로 함수 설명과 입력 스키마를 만들었고 Ch 21에서 create_agent에 도구를 전달했습니다. 같은 방식을 유지하되 생성 함수만 create_deep_agent로 바꿉니다. course_lookup은 네트워크를 사용하지 않는 교재용 고정 자료입니다.",
"diagram":"create_deep_agent가 백엔드·미들웨어를 조립하고 파일·위임 도구를 더한 뒤 CompiledStateGraph를 반환하는 순서입니다. 실행 출력의 model과 tools 노드는 마지막 상자에 포함된 내부 실행 노드입니다.",
"run":"init_chat_model로 gpt-5.4-mini를 준비하고 course_lookup 하나를 추가합니다. 질문에는 도구 이름과 Chapter 27을 명시합니다. 호출 뒤 각 메시지 타입과 tool_call 이름, ToolMessage 내용을 출력하고 두 조건을 assert로 확인합니다.",
"interpret":"저장된 실행은 그래프 노드에 model과 tools를 표시했고, 메시지 사이에 course_lookup 이름의 ToolMessage를 남겼습니다. 도구 결과는 ‘DeepAgents 하네스’였습니다. 이는 이 입력에서 모델이 사용자 도구를 선택했다는 한 사례이며 다른 질문의 선택률은 보여 주지 않습니다.",
"next":"다음 절에서는 기본에서 빠진 write_todos를 TodoListMiddleware로 직접 추가하고 실제 계획 상태를 확인합니다.",
"quiz":[("도구 실행을 직접 증명하는 메시지 타입은 무엇인가요?","course_lookup 이름과 반환값을 담은 ToolMessage입니다."),("create_deep_agent에 tools를 전달하면 기본 파일 도구가 제거되나요?","아닙니다. 사용자 도구는 기본 하네스 도구에 추가됩니다."),("한 번 선택된 결과로 도구 선택 정확도를 말할 수 있나요?","말할 수 없습니다. 여러 질문과 기대 도구를 정해 반복 평가해야 합니다.")]},
"03-플래닝과-시스템-프롬프트": {
"why":"계획 도구가 기본이라고 가정한 0.6 예제는 0.7에서 그대로 동작하지 않습니다. 필요한 애플리케이션만 TodoListMiddleware를 추가해야 합니다. 프롬프트 감소 수치도 측정 조건을 떼어 내면 과장되므로 실제 write_todos 호출과 릴리스 PR의 조건을 함께 봅니다.",
"prior":"Ch 26에서 위임 완료 조건을 문장으로 적었습니다. 할 일 목록은 완료 조건을 여러 단계의 상태로 관리하는 수단입니다. 모든 짧은 질문에 계획을 만들 필요는 없으므로 0.7의 opt-in 방향과 연결됩니다.",
"diagram":"0.6 기본 플래닝에서 0.7 opt-in으로 이동한 뒤 빈 작성 프롬프트와 첫 턴 토큰 측정으로 이어집니다. 마지막 상자는 전체 작업 비용이 아니라 gpt-5.5 hello 첫 턴 한 조건의 측정입니다.",
"run":"TodoListMiddleware를 middleware 인자에 넣고 두 할 일을 write_todos로 먼저 기록하라고 요청합니다. tool_calls와 todos 상태를 출력합니다. 이어서 PR의 5,395와 1,895를 같은 식으로 계산해 64.9%, 반올림 65%인지 확인합니다.",
"interpret":"모델은 write_todos를 두 번 호출했고 버전 확인과 결과 설명을 모두 completed로 기록했습니다. 이 상태는 계획 도구가 실제로 추가됐음을 보여 줍니다. 65%는 이 실행에서 측정한 값이 아니라 릴리스 PR의 gpt-5.5 첫 턴 비교를 재계산한 값입니다.",
"next":"다음 절에서는 대화 안의 계획 대신 파일시스템에 조사 중간 결과를 남겨 실행 사이의 인계 지점을 만듭니다.",
"quiz":[("0.7에서 write_todos를 쓰려면 무엇을 추가하나요?","TodoListMiddleware()를 create_deep_agent의 middleware 목록에 추가합니다."),("64.9%를 모든 작업의 절감률로 쓸 수 없는 이유는 무엇인가요?","gpt-5.5의 hello 첫 턴과 특정 두 버전 표면을 비교한 값이기 때문입니다."),("todos의 in_progress는 실패를 뜻하나요?","아닙니다. 아직 완료 표시로 갱신되지 않은 진행 상태입니다.")]},
"04-파일시스템과-중간-결과": {
"why":"조사 원문을 부모 메시지에 계속 붙이면 다음 호출에도 같은 긴 내용이 들어갑니다. 파일 경로를 인계 지점으로 쓰면 원자료별 메모를 분리하고 필요한 부분만 다시 읽을 수 있습니다. 이 절은 가상 경로와 실제 저장 루트를 구분합니다.",
"prior":"Ch 2에서 Path와 UTF-8 파일을 다뤘고 Ch 23에서 상태 저장 범위를 구분했습니다. FilesystemBackend의 파일은 체크포인터 메시지와 다른 저장 표면입니다. root_dir 아래에 저장하되 모델에는 /research/source-a.md라는 가상 경로를 보여 줍니다.",
"diagram":"조사 원문→write_file→/research/*.md→read_file로 다시 읽기 순서입니다. 세 번째 상자가 중간 결과의 인계 지점입니다. 화살표는 파일 내용이 자동으로 모델 입력에 들어간다는 뜻이 아니라, 필요할 때 read_file로 선택해 읽는 순서입니다.",
"run":"교재 상대 위치의 workspace를 백엔드 루트로 정하고 /research/source-a.md에 두 줄을 씁니다. ReadResult의 file_data에서 UTF-8 내용을 읽고 ls의 entries에서 가상 경로를 찾습니다. 출력에는 개인 절대 경로를 표시하지 않습니다.",
"interpret":"WriteResult가 반환됐고 읽은 내용은 ‘자료 A’ 제목과 하네스 설명 두 줄이었습니다. 목록에는 /research/source-a.md가 포함됐습니다. 이 결과는 같은 노트북 안의 실제 파일 쓰기와 읽기를 증명하지만 여러 스레드의 영속성은 측정하지 않습니다.",
"next":"다음 절에서는 파일시스템이 큰 도구 결과를 자동으로 옮기는 경우를 실행해 수동 중간 저장과 자동 오프로딩을 구분합니다.",
"quiz":[("root_dir와 /research/source-a.md는 각각 무엇인가요?","root_dir는 호스트의 저장 범위이고 /research/source-a.md는 에이전트가 보는 가상 경로입니다."),("ls 결과만으로 파일 본문을 확인할 수 있나요?","아닙니다. entries는 경로와 메타데이터를 보여 주며 본문은 read 결과에서 확인합니다."),("경로를 저장하면 출처 정확성도 보장되나요?","보장되지 않습니다. URL과 원문 식별자를 내용에 함께 기록하고 대조해야 합니다.")]},
"05-컨텍스트-관리와-오프로딩": {
"why":"도구가 수만 자를 반환하면 다음 모델 호출의 입력이 급격히 커집니다. DeepAgents는 한도를 넘은 텍스트를 파일로 옮기고 미리보기와 경로만 ToolMessage에 남길 수 있습니다. 이 절은 200토큰이라는 작은 실습 한도로 이 동작을 눈에 보이게 만듭니다.",
"prior":"앞 절에서는 write를 직접 호출해 중간 파일을 만들었습니다. 이번에는 모델이 large_result 도구를 선택하고 FilesystemMiddleware가 결과 크기를 검사합니다. 두 방식 모두 파일을 쓰지만 시작 조건이 다릅니다.",
"diagram":"긴 대화·큰 도구 결과에서 요약 또는 오프로딩으로 갈라진 뒤 요약 메시지·파일 경로가 다음 모델 호출에 전달됩니다. 이 실습은 큰 도구 결과의 오프로딩 경로만 실행하며 오래된 대화 요약 임계점은 별도 장기 실행이 필요합니다.",
"run":"large_result는 같은 근거 문장을 3,000번 반환합니다. FilesystemMiddleware의 한도를 200토큰으로 낮추고 모델에 도구를 한 번 호출하게 합니다. ToolMessage 길이, /large_tool_results/ 아래 파일, 최종 답을 차례로 검사합니다.",
"interpret":"원문 전체 대신 약 1,600자의 안내가 ToolMessage에 남았고, large_tool_results 아래에 호출 ID 이름의 파일이 생성됐습니다. 최종 답변 내용은 출력하거나 검사하지 않았습니다. 파일 생성은 확인했지만 자동 요약의 장기 품질이나 원문 전체 다시 읽기 성공률은 측정하지 않았습니다.",
"next":"다음 절에서는 큰 세부 조사 자체를 별도 문맥으로 보내 부모에게 최종 보고만 반환하는 위임을 실행합니다.",
"quiz":[("이 절에서 200은 무엇의 단위인가요?","FilesystemMiddleware가 큰 도구 결과를 옮길지 판단하는 실습용 토큰 한도입니다."),("ToolMessage가 1,600자면 원문이 손실된 것인가요?","원문은 파일에 저장되고 ToolMessage에는 미리보기와 다시 읽을 경로가 남습니다."),("오프로딩과 대화 요약은 같은 처리인가요?","아닙니다. 큰 도구 결과를 파일로 옮기는 처리와 오래된 메시지를 요약하는 처리를 구분합니다.")]},
"06-서브에이전트-위임": {
"why":"부모가 원문 조회와 세부 검증을 모두 수행하면 도구 출력이 부모 문맥에 쌓입니다. source-reviewer에 한 자료의 확인을 맡기면 부모는 task의 최종 보고를 받아 요약에 집중할 수 있습니다. 위임 여부는 task ToolMessage로 확인합니다.",
"prior":"Ch 26에서 서브에이전트의 완료 조건을 적었습니다. 이번 완료 조건은 release ID를 source_lookup으로 조회하고 지원되는 주장 하나를 반환하는 것입니다. 웹 검색 전체가 아니라 제공 자료 한 건에 대한 검증입니다.",
"diagram":"부모의 완료 조건→task 위임→격리된 조사 문맥→최종 보고 반환 순서입니다. source_lookup의 세부 ToolMessage는 서브에이전트 문맥에 머물고 부모 상태에는 task 반환 보고가 남습니다.",
"run":"source-reviewer의 이름·설명·시스템 지침·도구를 선언합니다. 부모에게 task를 사용해 source_lookup('release')를 실행하라고 요청합니다. 부모의 tool_calls에서 task를 찾고 task ToolMessage에 planning opt-in 주장이 있는지 확인합니다.",
"interpret":"부모 호출 목록에는 task가 있었고 위임 반환에는 release 자료와 planning opt-in 주장이 포함됐습니다. 부모 메시지에서 source_lookup 호출 자체가 보이지 않는 것은 문맥 격리의 결과입니다. 한 번의 반환만으로 누락률이나 잘못된 위임률은 알 수 없습니다.",
"next":"다음 절에서는 두 자료를 각각 확인하고 검증 주장·범위 한계·출처 ID를 하나의 final.md로 합칩니다.",
"quiz":[("부모 상태에서 실제 위임을 확인한 도구 이름은 무엇인가요?","task입니다."),("source_lookup ToolMessage가 부모 목록에 없는 이유는 무엇인가요?","서브에이전트가 별도 문맥에서 실행되고 최종 보고만 task 결과로 반환하기 때문입니다."),("완료 조건에 source ID를 쓰는 이유는 무엇인가요?","어떤 제공 자료를 확인해야 하는지 모호하지 않게 만들기 위해서입니다.")]},
"07-출처-검증형-deep-research": {
"why":"deep research라는 이름만 붙여도 출처가 자동으로 검증되지는 않습니다. 조사 도구가 어떤 자료를 반환하는지, 서브에이전트가 어떤 범위에서 결론을 내리는지, 최종 파일에 식별자가 남는지를 설계해야 합니다.",
"prior":"앞 절은 release 한 건을 위임했습니다. 이번에는 overview와 release 두 제공 자료를 조회하고 부모가 /research/final.md를 작성합니다. FilesystemBackend는 부모와 서브에이전트가 같은 경로를 인계 지점으로 쓰게 합니다.",
"diagram":"검증된 제공 자료→source_lookup→source-reviewer→/research/final.md 순서입니다. 첫 상자가 웹 전체가 아니라 교재가 제공한 두 문자열이라는 점이 이 실습의 범위를 결정합니다.",
"run":"overview와 release를 딕셔너리로 준비하고 source_lookup만 조사 도구로 제공합니다. 부모는 두 검증을 위임한 뒤 Verified claims, Scope limits, Source ids의 세 제목으로 파일을 씁니다. 파일 본문에 세 제목이 모두 있는지 assert로 확인합니다.",
"interpret":"실제 실행은 final.md에 하네스 정의, 0.7 opt-in과 빈 프롬프트, 65% 측정 범위를 기록했습니다. Scope limits에는 짧은 제공 자료만 확인했고 다른 웹 자료는 찾지 않았다고 명시했습니다. 저장된 실행의 부모 마지막 응답은 입력 2,379·출력 34·합계 2,413토큰이었지만 서브에이전트 전체 사용량 합계는 아닙니다.",
"next":"마지막 절에서는 새 작업 폴더에서 허용 쓰기와 거부 쓰기를 함께 실행해 운영 경계와 종료 결과를 확인합니다.",
"quiz":[("이 실습을 웹 전체 deep research라고 부를 수 없는 이유는 무엇인가요?","source_lookup이 미리 제공한 overview와 release 두 자료만 반환하기 때문입니다."),("final.md의 Scope limits가 필요한 이유는 무엇인가요?","확인하지 않은 자료와 결론의 적용 범위를 독자가 구분할 수 있게 합니다."),("부모 마지막 응답의 토큰을 전체 실행 비용에 바로 쓸 수 있나요?","아닙니다. 서브에이전트 호출 전체 합계가 포함됐는지 별도로 측정해야 합니다.")]},
"08-통합-실행과-운영-한계": {
"why":"기능이 모두 연결돼도 쓰기 범위와 종료 조건이 없으면 운영 가능한 에이전트가 아닙니다. 이 절은 앞 절의 파일을 읽지 않는 새 백엔드에서 허용 경로와 차단 경로를 동시에 요청하고 결과 메시지로 경계를 확인합니다.",
"prior":"Ch 24의 사람 승인과 이 장의 permissions는 도구 실행 경계를 다룹니다. 이 실습은 interrupt 대신 deny를 사용해 /blocked.txt 쓰기를 즉시 거부합니다. /run/report.md의 status: complete는 확인 가능한 종료 산출물입니다.",
"diagram":"경로별 권한 규칙→통합 실행→허용 파일과 거부 ToolMessage→종료 판정 순서입니다. 이번 코드는 사용량을 집계하지 않고 권한 거부와 산출물 검증에 집중합니다.",
"run":"workspace-08을 새 root_dir로 만들고 /blocked.txt에 대한 write deny 규칙을 추가합니다. 모델에게 /run/report.md에는 완료 상태를 쓰고 /blocked.txt에도 같은 내용을 시도하게 합니다. ReadResult와 permission denied ToolMessage를 각각 검증합니다.",
"interpret":"/run/report.md에는 status: complete가 저장됐고 /blocked.txt 쓰기는 permission denied로 반환됐습니다. 모델은 두 결과를 설명하고 종료했습니다. 이는 한 경로 규칙의 동작을 확인한 것이며 삭제·glob·서브에이전트 상속 규칙은 별도 테스트가 필요합니다.",
"next":"Ch 28에서는 허용된 기능을 MCP 서버로 공개하고 클라이언트가 발견·호출하는 경계를 배웁니다.",
"quiz":[("허용된 종료 산출물의 경로와 내용은 무엇인가요?","/run/report.md이며 내용은 status: complete입니다."),("/blocked.txt가 만들어지지 않은 근거는 무엇인가요?","write_file의 ToolMessage가 permission denied를 반환했고 deny 규칙이 적용됐습니다."),("deny와 interrupt의 차이는 무엇인가요?","deny는 호출을 거부하고, interrupt는 체크포인터와 승인 처리를 구성했을 때 사람의 결정을 기다립니다.")]},
}

REVIEWED_B7_HTML = {'01-하네스와-일곱-기능': '<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>소스 문자열 검색은 조립 경로의 존재만 보여 줍니다. 실제 도구 선택과 산출물은 기능별 실행으로 확인합니다.</li><li>이 장은 설치된 '
                  '<code>deepagents==0.7.0</code> 소스와 릴리스 노트를 기준으로 읽습니다.</li></ul>',
 '02-create-deep-agent와-도구': '<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li><code>create_deep_agent</code>가 반환한 그래프는 <code>invoke</code>할 때 '
                             '모델과 도구를 실행합니다.</li><li>도구 선택 여부는 최종 문장만으로 판단하지 말고 <code>tool_calls</code>와 <code>ToolMessage</code>를 함께 검사합니다.</li></ul>',
 '03-플래닝과-시스템-프롬프트': '<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li><code>completed</code>는 모델이 todo를 완료 상태로 기록한 값입니다. 버전 정보나 설명 산출물의 정확성은 따로 '
                     '검증합니다.</li><li>65%는 릴리스 PR의 제한된 첫 턴 수치를 재계산한 값이며 이 노트북의 실측 사용량이 아닙니다.</li></ul>',
 '04-파일시스템과-중간-결과': '<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>사용자 입력을 경로로 바로 사용하지 않고 허용된 실습 루트 아래로 제한합니다.</li><li>쓰기 반환값과 재읽기 본문을 함께 검사해 '
                    '실제 저장을 확인합니다.</li></ul>',
 '05-컨텍스트-관리와-오프로딩': '<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>ToolMessage의 미리보기는 원문 파일의 대체물이 아닙니다. 후속 판단에 원문이 필요하면 파일을 다시 읽어야 '
                     '합니다.</li><li>실행별 오프로딩 파일의 보존 기간과 삭제 시점을 정합니다.</li></ul>',
 '06-서브에이전트-위임': '<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>부모의 <code>task</code> 반환은 자식 작업의 요약입니다. 자식의 세부 도구 궤적과 산출물 검증은 별도 관측으로 '
                 '남깁니다.</li><li>위임 지시에는 사용할 자료, 출처 표기, 완료 조건을 함께 적습니다.</li></ul>',
 '07-출처-검증형-deep-research': '<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>이 실습의 <code>source_lookup</code>은 제공된 두 자료만 읽습니다. 웹 전체를 조사했다는 결론을 '
                            '내릴 수 없습니다.</li><li>부모 마지막 응답의 usage는 서브에이전트 전체 사용량이 아닙니다.</li></ul>',
 '08-통합-실행과-운영-한계': '<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>권한 판정은 도구 실행 직전에 적용합니다. 모델이 차단 경로를 요청해도 실제 파일은 만들어지지 않아야 합니다.</li><li>허용된 '
                    '파일 본문, 거부 ToolMessage, 차단 파일의 부재를 함께 검사합니다.</li></ul>'}
REVIEWED_CORE_HTML = {'01-하네스와-일곱-기능': '<p>하네스(harness)는 모델 하나를 뜻하지 않습니다. 모델 호출 주위에 도구, 파일 저장, 위임, 요약, 권한 같은 반복 기능을 조립해 긴 작업을 실행하는 틀입니다. 이 셀은 '
                  '<code>inspect.getsource(create_deep_agent)</code>로 설치된 0.7.0의 생성 함수 소스를 문자열로 읽고, 각 기능을 조립하는 이름이 실제로 들어 있는지 확인합니다. <code>in source</code> '
                  '결과가 <code>True</code>라는 것은 생성 경로에 관련 코드가 존재한다는 뜻이며, 모든 실행에서 그 기능이 활성화되었다는 뜻은 아닙니다.</p><p>프레임워크와 하네스의 차이는 추상화 수준입니다. LangGraph는 상태와 노드의 실행 '
                  '순서를 구성하고, LangChain의 에이전트는 모델과 도구 반복을 구성합니다. Deep Agents 하네스는 그 위에 장기 작업에서 반복되는 파일·서브에이전트·컨텍스트 관리 기능을 미리 조립합니다. 짧은 한 번의 도구 호출에는 하네스의 추가 표면이 '
                  '필요하지 않을 수 있습니다. 기능 수를 비교할 때는 기본 활성 기능과 인자를 전달해야 생기는 선택 기능을 구분해야 합니다.</p>',
 '02-create-deep-agent와-도구': '<p><code>create_deep_agent(model=..., tools=[...])</code>는 설정을 저장하는 객체가 아니라 호출 가능한 <code>CompiledStateGraph</code>를 반환합니다. '
                             '<code>tools</code>에는 업무 도구를 전달하고, 파일 도구와 위임 도구는 하네스의 미들웨어가 조건에 따라 더합니다. <code>agent.invoke({&#x27;messages&#x27;: '
                             '[...]})</code>를 호출해야 실제 모델과 도구 반복이 시작됩니다. 반환 딕셔너리의 <code>messages</code>에는 사용자 메시지, 도구 호출을 요청한 AI 메시지, 도구 결과, 최종 AI 메시지가 순서대로 '
                             '남습니다.</p><p>기본 도구가 보인다고 해서 모든 경로에 접근할 수 있는 것은 아닙니다. 파일 도구의 실제 범위는 연결한 backend와 permissions가 정합니다. <code>course_lookup</code> 같은 '
                             '업무 도구는 모델이 필요하다고 판단할 때 호출하지만, 필수 호출을 보장해야 한다면 시스템 지침만 의존하지 말고 궤적 검사나 명시적 그래프 경로를 추가합니다. 이 예제는 도구 호출과 <code>ToolMessage</code> '
                             '존재를 확인하며, 답변의 사실 정확성은 반환한 고정 수업 자료 범위에서만 판단할 수 있습니다.</p>',
 '03-플래닝과-시스템-프롬프트': '<p><code>TodoListMiddleware()</code>는 모델에게 <code>write_todos</code> 도구와 그 사용 지침을 추가합니다. 이를 <code>middleware=[...]</code>로 전달하는 것은 모든 요청에 '
                     '계획을 강제한다는 뜻이 아니라, 모델이 할 일 목록을 기록할 수 있는 기능을 선택적으로 연결하는 것입니다. <code>write_todos</code> 호출은 계획 내용을 상태에 남기고 후속 단계가 이를 읽게 합니다. 두 할 일을 요청한 '
                     '예제에서 도구 호출과 저장된 todo 상태를 함께 확인해야 ‘계획 기능이 연결되었다’고 말할 수 있습니다.</p><p>시스템 프롬프트 길이와 작업 품질은 같은 측정값이 아닙니다. 기본 지침을 줄이면 첫 호출 입력은 작아질 수 있지만, 업무에 '
                     '필요한 제약까지 빠지면 재시도나 잘못된 도구 사용이 늘 수 있습니다. 반대로 모든 짧은 질문에 todo 작성을 요구하면 계획 도구 호출 자체가 불필요한 단계가 됩니다. 플래닝은 여러 산출물, 선후 관계, 중간 검증이 있는 작업에 적용하고, 한 '
                     '단계 조회에는 직접 도구 호출을 우선합니다.</p>',
 '04-파일시스템과-중간-결과': '<p><code>FilesystemBackend(root_dir=...)</code>는 에이전트가 사용하는 <code>/research/source-a.md</code> 같은 가상 경로를 실습 폴더의 실제 경로로 대응시킵니다. 가상 경로의 '
                    '<code>/</code>는 컴퓨터의 파일 시스템 루트를 뜻하지 않습니다. <code>write_file</code>은 문자열을 저장하고 성공 여부를 구조화된 결과로 반환하며, <code>read_file</code>은 필요할 때 내용을 다시 '
                    '가져옵니다. 파일을 썼다는 사실만으로 다음 모델 호출이 자동으로 그 내용을 읽는 것은 아니므로, 읽기 호출과 전달 시점을 명시해야 합니다.</p><p>중간 결과를 파일에 두는 방법은 대화 상태에 모든 문자열을 유지하는 방법과 장단점이 다릅니다. '
                    '파일은 큰 자료를 이름과 경로로 인계하고 실행 뒤에도 검사하기 좋지만, 오래된 파일을 잘못 읽거나 여러 실행이 같은 경로를 덮어쓸 수 있습니다. 실행 ID별 폴더, 출처 ID, 생성 시각, 완료 상태를 함께 기록하면 어느 작업의 자료인지 구분할 '
                    '수 있습니다. 비밀이나 개인정보가 있는 자료는 저장 경로의 접근 권한과 보존 기간도 정해야 합니다.</p>',
 '05-컨텍스트-관리와-오프로딩': '<p>오프로딩(offloading)은 큰 도구 결과의 원문을 파일로 옮기고 <code>ToolMessage</code>에는 미리보기와 경로만 남기는 처리입니다. 이 예제의 <code>FilesystemMiddleware</code> 한도는 도구 '
                     '결과가 어느 크기에서 파일로 이동하는지 정합니다. 모델은 경로를 보고 필요할 때 파일 도구로 일부를 다시 읽습니다. 요약은 여러 메시지의 뜻을 짧게 다시 쓰는 처리이고, 오프로딩은 원문을 다른 저장 위치에 보존한다는 점이 '
                     '다릅니다.</p><p>두 방법은 손실 위험도 다릅니다. 요약은 원문에 있던 조건이나 예외를 생략할 수 있으므로 중요한 수치와 출처를 별도로 유지해야 합니다. 오프로딩은 원문을 보존하지만 모델이 다시 읽지 않은 부분은 현재 판단에 사용되지 '
                     '않습니다. 이번 출력에서 <code>ToolMessage</code>에 파일 경로가 남고 실제 파일이 존재하는지는 오프로딩을 확인하지만, 오래된 대화가 정확히 요약되는지는 확인하지 않습니다. 장기 대화 요약은 별도의 반복 실행과 사실 보존 '
                     '평가가 필요합니다.</p>',
 '06-서브에이전트-위임': '<p><code>subagents=[{...}]</code>의 각 사전은 이름, 역할 설명, 시스템 지침, 사용할 도구를 정의합니다. 부모 모델은 <code>task</code> 도구의 설명을 보고 어떤 서브에이전트에 무엇을 맡길지 결정합니다. 동기 '
                 '서브에이전트 호출에서는 부모가 작업이 끝날 때까지 기다리고, 부모 상태에는 세부 도구 기록 전체 대신 최종 반환 보고가 들어옵니다. 같은 backend를 전달하면 부모와 자식이 파일 경로로 중간 결과를 공유할 수 있습니다.</p><p>위임 지시는 '
                 '‘조사해 주세요’보다 결과 형식과 완료 조건을 포함해야 합니다. 예를 들어 ‘0.7 변경 두 가지, 각 출처 ID, 확인하지 못한 범위를 반환’이라고 적으면 부모가 빠진 항목을 검사할 수 있습니다. 서브에이전트는 문맥을 격리하지만 도구 권한까지 '
                 '자동으로 줄이지는 않습니다. 공식 문서에서 확인되는 것처럼 사용자 정의 서브에이전트의 도구·스킬·권한 상속 규칙은 항목마다 다르므로, 필요한 표면만 명시적으로 전달합니다.</p>',
 '07-출처-검증형-deep-research': '<p><code>source_lookup</code>은 웹 검색기가 아니라 교재가 제공한 두 자료를 ID로 찾아 반환하는 도구입니다. 조사 에이전트는 이 제한된 자료를 읽고 주장, 근거 ID, 범위 한계를 '
                            '<code>/research/final.md</code>에 저장합니다. 여기서 출처 검증은 보고서의 문장이 허용된 자료 중 어느 항목에 기대는지 추적하는 과정입니다. URL이나 출처 ID가 있다는 사실만으로 원문이 주장을 실제로 '
                            '뒷받침하는 것은 아니므로 주장과 근거 문장을 함께 대조해야 합니다.</p><p>실제 웹 조사에는 이 예제에 없는 단계가 더 필요합니다. 검색 결과의 누락을 줄이기 위한 여러 질의, 원문 페이지 열기, 발행일과 버전 확인, 서로 맞지 '
                            '않는 자료 비교, 접근 실패 기록이 필요합니다. 제공 자료 두 개만 조회한 이번 실험은 재현성이 높지만 범위 밖의 반례를 발견할 수 없습니다. 따라서 결과를 ‘Deep Agents 0.7에 대해 제공된 두 공식 자료에서 확인한 '
                            '내용’으로 한정하고 웹 전체를 조사한 결론으로 표현하지 않습니다.</p>',
 '08-통합-실행과-운영-한계': '<p>권한 규칙은 모델에게 부탁하는 문장이 아니라 도구 실행 직전에 판정되는 실행 경계여야 합니다. 이 예제는 허용된 보고서 경로와 차단된 <code>/blocked.txt</code> 경로를 각각 요청하고, 도구 결과에서 성공과 '
                    '<code>permission denied</code>를 확인합니다. 모델이 차단 파일을 쓰려고 시도했다는 사실과 파일이 실제로 만들어졌다는 사실은 다릅니다. 거부 결과가 메시지에 남아도 최종 답변이 성공처럼 말할 수 있으므로 파일 존재와 도구 '
                    '결과를 함께 검사합니다.</p><p>정지 조건도 권한과 같은 방식으로 관찰 가능해야 합니다. ‘보고서 작성 완료’는 지정 경로의 파일, 필수 항목, 검증 결과가 모두 있을 때 판정합니다. 최대 반복 수는 무한 실행을 막는 경계일 뿐 업무 완료를 '
                    '증명하지 않습니다. 이 실습은 사용량을 집계하지 않습니다. 종료 판정을 위해 허용된 파일 본문, 거부 ToolMessage, 차단 파일의 부재를 서로 다른 검사로 남깁니다.</p>'}
REVIEWED_SUMMARY = {'01-하네스와-일곱-기능': '실행 결과에서 파일시스템·서브에이전트·컨텍스트 요약·스킬·장기 메모리·권한과 사람 승인·비동기 서브에이전트가 모두 True였고 합계는 7이었습니다.',
 '02-create-deep-agent와-도구': '저장된 실행은 그래프 노드에 model과 tools를 표시했고, 메시지 사이에 course_lookup 이름의 ToolMessage를 남겼습니다.',
 '03-플래닝과-시스템-프롬프트': '모델은 write_todos를 두 번 호출했고 두 항목을 모두 completed로 기록했습니다. completed는 모델이 남긴 계획 상태이며 업무 결과 검증은 아닙니다.',
 '04-파일시스템과-중간-결과': 'WriteResult가 반환됐고 읽은 내용은 ‘자료 A’ 제목과 하네스 설명 두 줄이었습니다.',
 '05-컨텍스트-관리와-오프로딩': '원문 전체 대신 약 1,600자의 안내가 ToolMessage에 남았고, large_tool_results 아래에 호출 ID 이름의 파일이 생성됐습니다.',
 '06-서브에이전트-위임': '부모 호출 목록에는 task가 있었고 위임 반환에는 release 자료와 planning opt-in 주장이 포함됐습니다.',
 '07-출처-검증형-deep-research': '실제 실행은 <code>/research/final.md</code>에 주장, 출처 ID, 조사 범위 한계를 저장했습니다.',
 '08-통합-실행과-운영-한계': '<code>/run/report.md</code>의 완료 내용과 <code>/blocked.txt</code> 쓰기 거부를 함께 확인했습니다.'}
REVIEWED_STEP_MARKDOWN = {'01-하네스와-일곱-기능': ['## 실행 환경 준비\n\n상위 폴더의 .env를 찾아 키 값은 출력하지 않고 버전만 확인합니다.\n',
                   '## 단계 1\n'
                   '\n'
                   '설치한 0.7.0의 생성 함수 소스에서 일곱 기능이 조립되는 경로를 찾습니다.\n'
                   '\n'
                   '### 코드 읽기와 비교 경계\n'
                   '\n'
                   '하네스(harness)는 모델 하나를 뜻하지 않습니다. 모델 호출 주위에 도구, 파일 저장, 위임, 요약, 권한 같은 반복 기능을 조립해 긴 작업을 실행하는 틀입니다. 이 셀은 `inspect.getsource(create_deep_agent)`로 '
                   '설치된 0.7.0의 생성 함수 소스를 문자열로 읽고, 각 기능을 조립하는 이름이 실제로 들어 있는지 확인합니다. `in source` 결과가 `True`라는 것은 생성 경로에 관련 코드가 존재한다는 뜻이며, 모든 실행에서 그 기능이 활성화되었다는 '
                   '뜻은 아닙니다.\n'
                   '\n'
                   '프레임워크와 하네스의 차이는 추상화 수준입니다. LangGraph는 상태와 노드의 실행 순서를 구성하고, LangChain의 에이전트는 모델과 도구 반복을 구성합니다. Deep Agents 하네스는 그 위에 장기 작업에서 반복되는 '
                   '파일·서브에이전트·컨텍스트 관리 기능을 미리 조립합니다. 짧은 한 번의 도구 호출에는 하네스의 추가 표면이 필요하지 않을 수 있습니다. 기능 수를 비교할 때는 기본 활성 기능과 인자를 전달해야 생기는 선택 기능을 구분해야 합니다.\n',
                   '## 단계 2\n\n찾은 일곱 항목이 모두 True인지와 합계가 7인지 확인합니다.\n\n모든 값이 `True`라는 결과는 설치된 소스에 조립 경로가 있다는 뜻입니다. 각 기능이 실제 요청에서 선택되는지는 뒤 절의 실행 결과로 확인합니다.\n'],
 '02-create-deep-agent와-도구': ['## 실행 환경 준비\n\n상위 폴더의 .env를 찾아 키 값은 출력하지 않고 버전만 확인합니다.\n',
                              '## 단계 1\n'
                              '\n'
                              '고정 수업 자료를 반환하는 course_lookup 도구와 에이전트를 만듭니다.\n'
                              '\n'
                              '### 코드 읽기와 비교 경계\n'
                              '\n'
                              '`create_deep_agent(model=..., tools=[...])`는 설정을 저장하는 객체가 아니라 호출 가능한 `CompiledStateGraph`를 반환합니다. `tools`에는 업무 도구를 전달하고, 파일 도구와 '
                              "위임 도구는 하네스의 미들웨어가 조건에 따라 더합니다. `agent.invoke({'messages': [...]})`를 호출해야 실제 모델과 도구 반복이 시작됩니다. 반환 딕셔너리의 `messages`에는 사용자 메시지, 도구 "
                              '호출을 요청한 AI 메시지, 도구 결과, 최종 AI 메시지가 순서대로 남습니다.\n'
                              '\n'
                              '기본 도구가 보인다고 해서 모든 경로에 접근할 수 있는 것은 아닙니다. 파일 도구의 실제 범위는 연결한 backend와 permissions가 정합니다. `course_lookup` 같은 업무 도구는 모델이 필요하다고 판단할 때 '
                              '호출하지만, 필수 호출을 보장해야 한다면 시스템 지침만 의존하지 말고 궤적 검사나 명시적 그래프 경로를 추가합니다. 이 예제는 도구 호출과 `ToolMessage` 존재를 확인하며, 답변의 사실 정확성은 반환한 고정 수업 자료 '
                              '범위에서만 판단할 수 있습니다.\n',
                              '## 단계 2\n'
                              '\n'
                              '모델에게 course_lookup 호출을 요청하고 메시지 순서를 출력합니다.\n'
                              '\n'
                              '`invoke()`가 반환한 메시지 목록에서 AI의 `tool_calls`, `course_lookup` ToolMessage, 마지막 AIMessage를 순서대로 찾습니다. 이 순서가 도구가 실제로 실행된 근거입니다.\n',
                              '## 단계 3\n\nAI 도구 호출과 course_lookup ToolMessage가 모두 있는지 확인합니다.'],
 '03-플래닝과-시스템-프롬프트': ['## 실행 환경 준비\n\n상위 폴더의 .env를 찾아 키 값은 출력하지 않고 버전만 확인합니다.\n',
                      '## 단계 1\n'
                      '\n'
                      '0.7에서 opt-in인 TodoListMiddleware를 에이전트에 추가합니다.\n'
                      '\n'
                      '### 코드 읽기와 비교 경계\n'
                      '\n'
                      '`TodoListMiddleware()`는 모델에게 `write_todos` 도구와 그 사용 지침을 추가합니다. 이를 `middleware=[...]`로 전달하는 것은 모든 요청에 계획을 강제한다는 뜻이 아니라, 모델이 할 일 목록을 기록할 '
                      '수 있는 기능을 선택적으로 연결하는 것입니다. `write_todos` 호출은 계획 내용을 상태에 남기고 후속 단계가 이를 읽게 합니다. 두 할 일을 요청한 예제에서 도구 호출과 저장된 todo 상태를 함께 확인해야 ‘계획 기능이 '
                      '연결되었다’고 말할 수 있습니다.\n'
                      '\n'
                      '시스템 프롬프트 길이와 작업 품질은 같은 측정값이 아닙니다. 기본 지침을 줄이면 첫 호출 입력은 작아질 수 있지만, 업무에 필요한 제약까지 빠지면 재시도나 잘못된 도구 사용이 늘 수 있습니다. 반대로 모든 짧은 질문에 todo 작성을 요구하면 '
                      '계획 도구 호출 자체가 불필요한 단계가 됩니다. 플래닝은 여러 산출물, 선후 관계, 중간 검증이 있는 작업에 적용하고, 한 단계 조회에는 직접 도구 호출을 우선합니다.\n'
                      '\n'
                      '`todos` 상태의 `completed`는 모델이 해당 항목을 완료로 기록했다는 뜻입니다. 버전 확인 결과나 설명 산출물을 실제로 검증했다는 증거가 아니므로, 산출물을 따로 검사해야 합니다.\n',
                      '## 단계 2\n\n두 할 일을 기록하도록 요청하고 write_todos 호출과 상태를 확인합니다.\n',
                      '## 단계 3\n'
                      '\n'
                      '릴리스 PR의 제한된 첫 턴 토큰 수로 감소율을 다시 계산합니다.\n'
                      '\n'
                      '감소율은 현재 실행의 사용량이 아니라 릴리스 PR에 적힌 5,395와 1,895를 재계산한 값입니다. 예제의 todo 상태와 서로 다른 근거입니다.\n'],
 '04-파일시스템과-중간-결과': ['## 실행 환경 준비\n\n상위 폴더의 .env를 찾아 키 값은 출력하지 않고 버전만 확인합니다.\n',
                     '## 단계 1\n'
                     '\n'
                     '가상 경로를 실습 작업 폴더에 연결하고 중간 파일을 씁니다.\n'
                     '\n'
                     '### 코드 읽기와 비교 경계\n'
                     '\n'
                     '`FilesystemBackend(root_dir=...)`는 에이전트가 사용하는 `/research/source-a.md` 같은 가상 경로를 실습 폴더의 실제 경로로 대응시킵니다. 가상 경로의 `/`는 컴퓨터의 파일 시스템 루트를 뜻하지 '
                     '않습니다. `write_file`은 문자열을 저장하고 성공 여부를 구조화된 결과로 반환하며, `read_file`은 필요할 때 내용을 다시 가져옵니다. 파일을 썼다는 사실만으로 다음 모델 호출이 자동으로 그 내용을 읽는 것은 아니므로, 읽기 '
                     '호출과 전달 시점을 명시해야 합니다.\n'
                     '\n'
                     '중간 결과를 파일에 두는 방법은 대화 상태에 모든 문자열을 유지하는 방법과 장단점이 다릅니다. 파일은 큰 자료를 이름과 경로로 인계하고 실행 뒤에도 검사하기 좋지만, 오래된 파일을 잘못 읽거나 여러 실행이 같은 경로를 덮어쓸 수 있습니다. 실행 '
                     'ID별 폴더, 출처 ID, 생성 시각, 완료 상태를 함께 기록하면 어느 작업의 자료인지 구분할 수 있습니다. 비밀이나 개인정보가 있는 자료는 저장 경로의 접근 권한과 보존 기간도 정해야 합니다.\n',
                     '## 단계 2\n\n저장한 파일의 본문과 가상 경로 목록을 다시 읽어 확인합니다.\n\n쓰기 반환값만으로 내용 보존을 결론내리지 않습니다. 같은 가상 경로를 다시 읽은 본문과 목록을 함께 검사합니다.\n'],
 '05-컨텍스트-관리와-오프로딩': ['## 실행 환경 준비\n\n상위 폴더의 .env를 찾아 키 값은 출력하지 않고 버전만 확인합니다.\n',
                      '## 단계 1\n'
                      '\n'
                      '큰 결과를 반환하는 도구와 200토큰 한도의 파일시스템 미들웨어를 준비합니다.\n'
                      '\n'
                      '### 코드 읽기와 비교 경계\n'
                      '\n'
                      '오프로딩(offloading)은 큰 도구 결과의 원문을 파일로 옮기고 `ToolMessage`에는 미리보기와 경로만 남기는 처리입니다. 이 예제의 `FilesystemMiddleware` 한도는 도구 결과가 어느 크기에서 파일로 이동하는지 '
                      '정합니다. 모델은 경로를 보고 필요할 때 파일 도구로 일부를 다시 읽습니다. 요약은 여러 메시지의 뜻을 짧게 다시 쓰는 처리이고, 오프로딩은 원문을 다른 저장 위치에 보존한다는 점이 다릅니다.\n'
                      '\n'
                      '두 방법은 손실 위험도 다릅니다. 요약은 원문에 있던 조건이나 예외를 생략할 수 있으므로 중요한 수치와 출처를 별도로 유지해야 합니다. 오프로딩은 원문을 보존하지만 모델이 다시 읽지 않은 부분은 현재 판단에 사용되지 않습니다. 이번 출력에서 '
                      '`ToolMessage`에 파일 경로가 남고 실제 파일이 존재하는지는 오프로딩을 확인하지만, 오래된 대화가 정확히 요약되는지는 확인하지 않습니다. 장기 대화 요약은 별도의 반복 실행과 사실 보존 평가가 필요합니다.\n',
                      '## 단계 2\n'
                      '\n'
                      '도구를 호출해 ToolMessage에 남은 안내와 최종 답을 출력합니다.\n'
                      '\n'
                      'ToolMessage의 길이와 안내 문구를 출력해 원문 전체가 대화에 남지 않았는지 확인합니다. 마지막 AI 답변의 내용은 이 셀의 검사 대상이 아닙니다.\n',
                      '## 단계 3\n\n원문 대신 파일 경로가 남았는지와 실제 저장 파일을 확인합니다.\n\n실제 파일 존재와 파일의 원문 길이를 확인해야 오프로딩을 검증할 수 있습니다. 미리보기 문장만으로는 저장 성공을 알 수 없습니다.\n'],
 '06-서브에이전트-위임': ['## 실행 환경 준비\n\n상위 폴더의 .env를 찾아 키 값은 출력하지 않고 버전만 확인합니다.\n',
                  '## 단계 1\n'
                  '\n'
                  '고정 자료 조회 도구를 쓰는 source-reviewer 서브에이전트를 선언합니다.\n'
                  '\n'
                  '### 코드 읽기와 비교 경계\n'
                  '\n'
                  '`subagents=[{...}]`의 각 사전은 이름, 역할 설명, 시스템 지침, 사용할 도구를 정의합니다. 부모 모델은 `task` 도구의 설명을 보고 어떤 서브에이전트에 무엇을 맡길지 결정합니다. 동기 서브에이전트 호출에서는 부모가 작업이 끝날 '
                  '때까지 기다리고, 부모 상태에는 세부 도구 기록 전체 대신 최종 반환 보고가 들어옵니다. 같은 backend를 전달하면 부모와 자식이 파일 경로로 중간 결과를 공유할 수 있습니다.\n'
                  '\n'
                  '위임 지시는 ‘조사해 주세요’보다 결과 형식과 완료 조건을 포함해야 합니다. 예를 들어 ‘0.7 변경 두 가지, 각 출처 ID, 확인하지 못한 범위를 반환’이라고 적으면 부모가 빠진 항목을 검사할 수 있습니다. 서브에이전트는 문맥을 격리하지만 도구 '
                  '권한까지 자동으로 줄이지는 않습니다. 공식 문서에서 확인되는 것처럼 사용자 정의 서브에이전트의 도구·스킬·권한 상속 규칙은 항목마다 다르므로, 필요한 표면만 명시적으로 전달합니다.\n',
                  '## 단계 2\n'
                  '\n'
                  '부모가 task 도구로 release 확인을 위임하고 반환 보고를 검사합니다.\n'
                  '\n'
                  '부모에서 보이는 `task` 호출과 반환 보고를 검사합니다. 자식 문맥의 `source_lookup` 세부 호출은 부모 메시지에 노출되지 않으므로 별도 관측이 필요합니다.\n'],
 '07-출처-검증형-deep-research': ['## 실행 환경 준비\n\n상위 폴더의 .env를 찾아 키 값은 출력하지 않고 버전만 확인합니다.\n',
                             '## 단계 1\n'
                             '\n'
                             '제공한 두 자료만 반환하는 조사 도구와 공유 파일 백엔드를 준비합니다.\n'
                             '\n'
                             '### 코드 읽기와 비교 경계\n'
                             '\n'
                             '`source_lookup`은 웹 검색기가 아니라 교재가 제공한 두 자료를 ID로 찾아 반환하는 도구입니다. 조사 에이전트는 이 제한된 자료를 읽고 주장, 근거 ID, 범위 한계를 `/research/final.md`에 '
                             '저장합니다. 여기서 출처 검증은 보고서의 문장이 허용된 자료 중 어느 항목에 기대는지 추적하는 과정입니다. URL이나 출처 ID가 있다는 사실만으로 원문이 주장을 실제로 뒷받침하는 것은 아니므로 주장과 근거 문장을 함께 대조해야 '
                             '합니다.\n'
                             '\n'
                             '실제 웹 조사에는 이 예제에 없는 단계가 더 필요합니다. 검색 결과의 누락을 줄이기 위한 여러 질의, 원문 페이지 열기, 발행일과 버전 확인, 서로 맞지 않는 자료 비교, 접근 실패 기록이 필요합니다. 제공 자료 두 개만 조회한 '
                             '이번 실험은 재현성이 높지만 범위 밖의 반례를 발견할 수 없습니다. 따라서 결과를 ‘Deep Agents 0.7에 대해 제공된 두 공식 자료에서 확인한 내용’으로 한정하고 웹 전체를 조사한 결론으로 표현하지 않습니다.\n',
                             '## 단계 2\n'
                             '\n'
                             '두 자료를 위임 검토한 뒤 근거, 범위 한계, 출처 ID를 파일로 저장합니다.\n'
                             '\n'
                             '결과 파일에서 주장과 출처 ID, 조사 범위 한계를 함께 확인합니다. 제공된 두 자료 밖의 웹 문서를 찾았다고 해석하면 안 됩니다.\n'],
 '08-통합-실행과-운영-한계': ['## 실행 환경 준비\n\n상위 폴더의 .env를 찾아 키 값은 출력하지 않고 버전만 확인합니다.\n',
                     '## 단계 1\n'
                     '\n'
                     '새 작업 폴더와 /blocked.txt 쓰기 거부 규칙을 준비합니다.\n'
                     '\n'
                     '### 코드 읽기와 비교 경계\n'
                     '\n'
                     '권한 규칙은 모델에게 부탁하는 문장이 아니라 도구 실행 직전에 판정되는 실행 경계여야 합니다. 이 예제는 허용된 보고서 경로와 차단된 `/blocked.txt` 경로를 각각 요청하고, 도구 결과에서 성공과 `permission denied`를 '
                     '확인합니다. 모델이 차단 파일을 쓰려고 시도했다는 사실과 파일이 실제로 만들어졌다는 사실은 다릅니다. 거부 결과가 메시지에 남아도 최종 답변이 성공처럼 말할 수 있으므로 파일 존재와 도구 결과를 함께 검사합니다.\n'
                     '\n'
                     '정지 조건도 권한과 같은 방식으로 관찰 가능해야 합니다. ‘보고서 작성 완료’는 지정 경로의 파일, 필수 항목, 검증 결과가 모두 있을 때 판정합니다. 최대 반복 수는 무한 실행을 막는 경계일 뿐 업무 완료를 증명하지 않습니다. 이 실습은 사용량을 집계하지 않습니다. 종료 판정을 위해 허용된 파일 본문, 거부 ToolMessage, 차단 파일의 부재를 서로 다른 검사로 남깁니다.\n',
                     '## 단계 2\n\n허용 보고서와 차단 파일에 차례로 쓰도록 요청합니다.\n\n허용 경로와 차단 경로를 한 요청에 넣어 성공과 거부를 함께 관찰합니다. 단순히 최종 답변을 읽지 말고 도구 메시지를 확인해야 합니다.\n',
                     '## 단계 3\n'
                     '\n'
                     '완료 보고서와 permission denied 도구 결과를 함께 확인합니다.\n'
                     '\n'
                     '종료 조건은 허용된 보고서의 내용과 차단 도구의 `permission denied` 결과를 모두 확인합니다. 모델의 완료 문장만으로는 충분하지 않습니다.\n']}

def make_html(slug: str, title: str, question: str, left: str, right: str) -> str:
    concept = SPECIAL[slug]
    d = DETAILS[slug]
    quizzes = ''.join(f'<details class="quiz"><summary>문제 {i}</summary><p class="quiz-q">{q}</p><p class="quiz-a"><b>해설</b> {a}</p></details>' for i,(q,a) in enumerate(d['quiz'],1))
    return f'''<!--meta: 강의 1h | 실습 2h | 코드 Jupyter Notebook | 새 용어 4 -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul><li>{question}</li><li>실행 출력에서 {title}의 구성과 결과를 구분할 수 있습니다.</li><li>이 실험이 확인한 범위를 설명할 수 있습니다.</li></ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>{d['why']}</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>{d['prior']}</p><p>노트북은 앞 절 변수에 의존하지 않으며 Python 3.12, <code>deepagents==0.7.0</code>, <code>langchain==1.4.0</code>을 설치하고 상위 폴더의 <code>.env</code>를 찾습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>정의와 구체적인 상황</h3><p>{concept}</p><h3>코드 읽기와 비교 경계</h3>{REVIEWED_CORE_HTML[slug]}<h3>도식 읽기</h3><p>{{{{svg:{slug[:2]}-흐름}}}}</p><p>{d['diagram']}</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>{d['run']}</p>{{{{notebook:{slug}}}}}<p class="look"><b>확인할 점</b> 출력값과 <code>assert</code> 조건이 같은 사실을 확인하는지 대조합니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>{d['interpret']}</p>
{REVIEWED_B7_HTML[slug]}
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>{question}</li><li>{REVIEWED_SUMMARY[slug]}</li><li>버전과 측정 범위를 실행 기록에 함께 남깁니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — {d['next']}</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>{quizzes}
<h2 id="b10"><span class="no">10</span>참고 자료</h2><p>확인 날짜: 2026-09-11. 기준 환경: Python 3.12, DeepAgents 0.7.0, LangChain 1.4.0, langchain-openai 1.6.0.</p>{SOURCES}
'''

INSTALL = "# 실습에서 검증한 패키지 버전을 현재 커널에 설치합니다.\n%pip install -q deepagents==0.7.0 langchain==1.4.0 langchain-openai==1.6.0 python-dotenv==1.2.3"
COMMON_SETUP = """from importlib.metadata import version
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

# 현재 폴더부터 상위 폴더까지 .env를 찾고 값은 출력하지 않습니다.
env_path = find_dotenv(usecwd=True)
load_dotenv(env_path)
cwd = Path.cwd().resolve()
LAB = next(
    parent / 'labs/part6/ch27-deepagents'
    for parent in [cwd, *cwd.parents]
    if (parent / 'labs/part6/ch27-deepagents/pyproject.toml').is_file()
)
print('deepagents', version('deepagents'))
print('langchain', version('langchain'))
assert version('deepagents') == '0.7.0'"""

CODES = {
"01-하네스와-일곱-기능": ["""# 생성 함수가 조립하는 일곱 기능의 코드 경로를 확인합니다.
import inspect
import deepagents.graph as graph
source = inspect.getsource(graph.create_deep_agent)
features = {
    '파일시스템': 'FilesystemMiddleware' in source,
    '서브에이전트': 'SubAgentMiddleware' in source,
    '컨텍스트 요약': 'create_summarization_middleware' in source,
    '스킬': 'SkillsMiddleware' in source,
    '장기 메모리': 'MemoryMiddleware' in source,
    '권한·사람 승인': 'HumanInTheLoopMiddleware' in source,
    '비동기 서브에이전트': 'AsyncSubAgentMiddleware' in source,
}
for name, found in features.items(): print(name, found)""", """# 일곱 기능의 조립 경로가 모두 확인됐는지 검사합니다.
print('확인한 기능 수:', sum(features.values()))
assert all(features.values())"""],
"02-create-deep-agent와-도구": ["""from langchain.chat_models import init_chat_model
from langchain.tools import tool
from deepagents import create_deep_agent

@tool
def course_lookup(chapter: int) -> str:
    \"\"\"Return the fixed course topic for one chapter.\"\"\"
    return {27: 'DeepAgents 하네스'}[chapter]

# 모델과 한 개의 수업 조회 도구를 가진 에이전트를 만듭니다.
model = init_chat_model('openai:gpt-5.4-mini')
agent = create_deep_agent(model=model, tools=[course_lookup])
print('그래프 노드:', sorted(agent.get_graph().nodes))""", """# 모델이 course_lookup을 선택하도록 구체적인 질문을 보냅니다.
result = agent.invoke({'messages':[{'role':'user','content':'course_lookup으로 Chapter 27 주제를 확인한 뒤 한 문장으로 답하세요.'}]})
for message in result['messages']:
    print(type(message).__name__, getattr(message, 'name', None))""", """# AI 도구 호출과 도구 반환 메시지가 모두 있는지 확인합니다.
calls = [call for m in result['messages'] for call in getattr(m, 'tool_calls', [])]
tool_messages = [m for m in result['messages'] if type(m).__name__ == 'ToolMessage']
print('호출 도구:', [call['name'] for call in calls])
print('도구 결과:', [m.content for m in tool_messages if m.name == 'course_lookup'])
assert any(call['name'] == 'course_lookup' for call in calls)
assert any(m.name == 'course_lookup' and 'DeepAgents' in str(m.content) for m in tool_messages)"""],
"03-플래닝과-시스템-프롬프트": ["""from langchain.chat_models import init_chat_model
from langchain.agents.middleware import TodoListMiddleware
from deepagents import create_deep_agent

# 0.7에서는 플래닝 미들웨어를 직접 추가합니다.
model = init_chat_model('openai:gpt-5.4-mini')
agent = create_deep_agent(model=model, middleware=[TodoListMiddleware()])
print('opt-in 미들웨어:', 'TodoListMiddleware')""", """# 두 단계 계획을 먼저 기록하도록 요청합니다.
result = agent.invoke({'messages':[{'role':'user','content':'먼저 write_todos로 버전 확인과 결과 설명의 두 할 일을 기록하고, 그 다음 짧게 완료하세요.'}]})
calls = [call for m in result['messages'] for call in getattr(m, 'tool_calls', [])]
print('호출 도구:', [call['name'] for call in calls])
print('todos 상태:', result.get('todos'))
assert any(call['name'] == 'write_todos' for call in calls)
assert result.get('todos')""", """# 릴리스 PR의 한정된 첫 턴 비교를 계산합니다.
before, after = 5395, 1895
reduction = (before - after) / before
print('gpt-5.5 hello 첫 턴:', before, '->', after, f'({reduction:.1%})')
assert round(reduction, 2) == 0.65"""],
"04-파일시스템과-중간-결과": ["""# 가상 경로를 실제 실습 작업 폴더에 연결하고 중간 파일을 씁니다.
from deepagents.backends import FilesystemBackend
workspace = LAB / 'workspace'
workspace.mkdir(parents=True, exist_ok=True)
backend = FilesystemBackend(root_dir=workspace)
result = backend.write('/research/source-a.md', '# 자료 A\\n공식 문서에서 확인한 하네스 설명')
print(type(result).__name__, 'workspace/research/source-a.md')""", """# 저장한 중간 파일의 본문과 가상 경로 목록을 다시 읽습니다.
read = backend.read('/research/source-a.md')
print(read.file_data['content'])
print('목록:', [item['path'] for item in backend.ls('/research').entries])
assert read.file_data['content'].startswith('# 자료 A')
assert any(item['path'] == '/research/source-a.md' for item in backend.ls('/research').entries)"""],
"05-컨텍스트-관리와-오프로딩": ["""from langchain.chat_models import init_chat_model
from langchain.tools import tool
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from deepagents.middleware.filesystem import FilesystemMiddleware

@tool
def large_result() -> str:
    \"\"\"Return a deliberately large local research result.\"\"\"
    return '근거 문장입니다. ' * 3000

# 작은 한도를 사용해 큰 도구 결과의 파일 이동을 관찰합니다.
workspace = LAB / 'workspace-05'
workspace.mkdir(parents=True, exist_ok=True)
backend = FilesystemBackend(root_dir=workspace)
filesystem = FilesystemMiddleware(backend=backend, tool_token_limit_before_evict=200)
agent = create_deep_agent(model=init_chat_model('openai:gpt-5.4-mini'), tools=[large_result], backend=backend, middleware=[filesystem])""", """# 큰 결과를 호출한 뒤 핵심만 답하도록 요청합니다.
result = agent.invoke({'messages':[{'role':'user','content':'large_result를 한 번 호출하고 첫 문장의 뜻만 답하세요.'}]})
tool_messages = [m for m in result['messages'] if type(m).__name__ == 'ToolMessage' and m.name == 'large_result']
print('도구 메시지 길이:', len(str(tool_messages[0].content)))
print('도구 메시지:', str(tool_messages[0].content)[:500])
assert tool_messages""", """# 원문 대신 파일 경로가 남고 실제 파일이 생성됐는지 확인합니다.
import re

notice = str(tool_messages[0].content)
match = re.search(r'path: (/[^\\s]+)', notice)
assert match is not None
saved_path = workspace / match.group(1).lstrip('/')
stored = saved_path.read_text(encoding='utf-8')
expected = '근거 문장입니다. ' * 3000
print('이번 생성 파일:', saved_path.relative_to(workspace).as_posix())
print('저장 본문 길이:', len(stored))
assert len(notice) < 3000
assert saved_path.is_file() and stored == expected
assert result['messages'][-1].text"""],
"06-서브에이전트-위임": ["""# 고정 자료 조회 도구와 검토 전용 서브에이전트를 준비합니다.
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from deepagents import create_deep_agent

@tool
def source_lookup(source_id: str) -> str:
    \"\"\"Return one fixed, pre-verified course source.\"\"\"
    return {'release':'DeepAgents 0.7 makes planning opt-in.'}[source_id]

researcher = {'name':'source-reviewer','description':'Check provided source claims.',
 'system_prompt':'Use source_lookup and return the source id and supported claim.', 'tools':[source_lookup]}
agent = create_deep_agent(model=init_chat_model('openai:gpt-5.4-mini'), tools=[source_lookup], subagents=[researcher])""", """# 부모가 source-reviewer에게 release 확인을 위임합니다.
result = agent.invoke({'messages':[{'role':'user','content':"task 도구로 source-reviewer에게 source_lookup('release')를 실행해 주장을 확인하게 하고 결과를 한국어로 요약하세요."}]})
calls = [call for m in result['messages'] for call in getattr(m, 'tool_calls', [])]
tasks = [m for m in result['messages'] if type(m).__name__ == 'ToolMessage' and m.name == 'task']
print('부모 호출:', [call['name'] for call in calls])
print('위임 반환:', str(tasks[0].content)[:500])
assert any(call['name'] == 'task' for call in calls)
assert tasks and 'planning opt-in' in str(tasks[0].content).lower()"""],
"07-출처-검증형-deep-research": ["""# 검증된 제공 자료만 조회하는 조사 도구와 공유 백엔드를 준비합니다.
from langchain.tools import tool
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
provided = {
 'overview': 'Deep Agents is an agent harness built on LangChain and LangGraph. It provides filesystem, subagents, and context management.',
 'release': 'In 0.7.0 TodoListMiddleware became opt-in and the authored base prompt became empty. The 65% value was one gpt-5.5 hello-turn comparison.'
}
@tool
def source_lookup(source_id: str) -> str:
    \"\"\"Return one pre-verified course source by its id: overview or release.\"\"\"
    return provided.get(source_id, 'UNKNOWN SOURCE')
workspace = LAB / 'workspace'
backend = FilesystemBackend(root_dir=workspace)
researcher = {'name':'source-reviewer','description':'Verify claims against provided sources.',
 'system_prompt':'Use source_lookup. Return source id, supported claim, and limitation.', 'tools':[source_lookup]}
agent = create_deep_agent(model='openai:gpt-5.4-mini', tools=[source_lookup], subagents=[researcher], backend=backend)""", """# 두 자료의 검증을 위임하고 근거·한계·출처 ID를 파일로 저장합니다.
prompt = '''Delegate overview and release checks to source-reviewer. Then write /research/final.md with
three headings: Verified claims, Scope limits, Source ids. Use only source_lookup evidence.'''
result = agent.invoke({'messages':[{'role':'user','content':prompt}]})
final = result['messages'][-1]
usage = getattr(final, 'usage_metadata', None)
print('최종 응답:', final.text[:500])
print('사용량:', usage)
saved = backend.read('/research/final.md')
print('저장 파일:', saved.file_data['content'][:700])
assert all(heading in saved.file_data['content'] for heading in ['Verified claims','Scope limits','Source ids'])"""],
"08-통합-실행과-운영-한계": ["""from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from deepagents.middleware.filesystem import FilesystemPermission

# 이 노트북만의 새 작업 폴더와 차단 규칙을 준비합니다.
workspace = LAB / 'workspace-08'
workspace.mkdir(parents=True, exist_ok=True)
backend = FilesystemBackend(root_dir=workspace)
deny_blocked = FilesystemPermission(operations=['write'], paths=['/blocked.txt'], mode='deny')
agent = create_deep_agent(model=init_chat_model('openai:gpt-5.4-mini'), backend=backend, permissions=[deny_blocked])""", """# 허용 경로에는 보고서를 쓰고 차단 경로에는 쓰기를 시도합니다.
prompt = '''write_file로 /run/report.md에 "status: complete"를 쓰세요.
그 다음 /blocked.txt에도 같은 내용을 쓰려고 시도하고, 두 결과를 설명한 뒤 종료하세요.'''
result = agent.invoke({'messages':[{'role':'user','content':prompt}]})
tool_messages = [m for m in result['messages'] if type(m).__name__ == 'ToolMessage']
for message in tool_messages: print(message.name, str(message.content)[:300])""", """# 종료 조건과 권한 거부를 실제 파일과 도구 메시지로 확인합니다.
report = backend.read('/run/report.md')
denied = [m for m in tool_messages if 'permission' in str(m.content).lower() or 'denied' in str(m.content).lower()]
print('보고서:', report.file_data['content'])
print('최종 답변:', result['messages'][-1].text)
assert report.file_data['content'].strip() == 'status: complete'
assert denied
assert result['messages'][-1].text"""],
}

def notebook(slug: str, title: str, question: str) -> dict:
    cells = [
      {"cell_type":"markdown","id":"cell-01","metadata":{},"source":[f"# {title}\n\n{question}"]},
      {"cell_type":"markdown","id":"cell-02","metadata":{},"source":["## 설치\n\n고정된 패키지를 현재 커널에 설치합니다."]},
      {"cell_type":"code","execution_count":None,"id":"cell-03","metadata":{},"outputs":[],"source":[INSTALL]},
      {"cell_type":"markdown","id":"cell-04","metadata":{},"source":["## 실행 환경 준비\n\n상위 폴더의 .env를 찾아 키 값은 출력하지 않고 버전만 확인합니다."]},
      {"cell_type":"code","execution_count":None,"id":"cell-05","metadata":{},"outputs":[],"source":COMMON_SETUP.splitlines(True)},
    ]
    for index, code in enumerate(CODES[slug], start=1):
        step_markdown = REVIEWED_STEP_MARKDOWN[slug][index]
        cells.append({"cell_type":"markdown","id":f"step-{index}-text","metadata":{},"source":[step_markdown]})
        cells.append({"cell_type":"code","execution_count":None,"id":f"step-{index}-code","metadata":{},"outputs":[],"source":code.splitlines(True)})
    return {"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.12"},"lesson_format":"experiment"},"nbformat":4,"nbformat_minor":5}

def refuse_existing_drafts() -> None:
    """Stop this initial-draft generator before it overwrites reviewed files."""
    targets = [
        *(SRC_DIR / f"{slug}.html" for slug, *_ in SECTIONS),
        *(NB_DIR / f"{slug}.ipynb" for slug, *_ in SECTIONS),
    ]
    existing = [path for path in targets if path.exists()]
    if existing:
        paths = "\n".join(f"- {path.relative_to(HERE.parents[2])}" for path in existing)
        raise FileExistsError(
            "Ch27 초안 생성기는 기존 교재 원본이나 노트북을 덮어쓰지 않습니다. "
            "기존 파일을 검토하고 필요한 부분만 직접 수정하세요.\n"
            f"{paths}"
        )


def main() -> None:
    refuse_existing_drafts()
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    NB_DIR.mkdir(parents=True, exist_ok=True)
    for slug, title, question, left, right in SECTIONS:
        (SRC_DIR / f"{slug}.html").write_text(make_html(slug,title,question,left,right), encoding="utf-8")
        (NB_DIR / f"{slug}.ipynb").write_text(json.dumps(notebook(slug,title,question),ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
    print('authored', len(SECTIONS), 'sections and notebooks')

if __name__ == '__main__': main()
