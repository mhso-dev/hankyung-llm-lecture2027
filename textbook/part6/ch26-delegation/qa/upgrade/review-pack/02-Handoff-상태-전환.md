# 02-Handoff-상태-전환

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 1h | 실습 1h | 코드 notebooks/02-Handoff-상태-전환.ipynb | 새 용어 4 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>노드가 <code>Command</code>로 담당을 넘기고, 다음 차례가 받은 담당에서 시작하는 그래프를 만들 수 있습니다.</li>
<li>도구로 담당을 넘길 때 도구 메시지를 함께 담아야 하는 까닭을 출력으로 설명할 수 있습니다.</li>
<li>모델이 담당을 넘기는 두 차례 대화에서, 응답을 쓴 담당과 모델 요청 수를 셀 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href="01-Subagent-도구-위임.html">01절</a>의 서브에이전트는 중앙 에이전트에게 불려 답만 써 주었습니다. 문의한 사람과 대화하는 쪽은 끝까지 중앙 에이전트였습니다. 그런데 도서관에서는 대출 창구 직원이 이용자를 상호대차 창구로 보내기도 합니다. 그러면 그다음 질문은 상호대차 창구 직원과 나눕니다.</p><p>이 절은 이렇게 다음 차례에 대화할 담당을 바꾸는 모양을 봅니다. 절 제목의 Handoff는 이 모양을 가리키고, 본문에서는 핸드오프라고 씁니다. 넘겨받은 담당이 다음 차례에도 이어서 대화하려면, 지금 담당이 누구인지를 상태에 적고 저장해야 합니다. 이 절은 그 칸이 어떻게 적히고 읽히는지를 출력으로 봅니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href="../../part4/ch13-langgraph-basics/06-Command-갱신과-이동.html">Ch 13 06절</a>에서는 노드가 <code>Command</code> 하나에 갱신과 다음 노드 이름을 함께 담았습니다. 그때 인자 <code>destinations</code>는 구조 문자열에만 쓰였습니다. <a href="../../part5/ch20-tool-node/04-if-분기와-모델-선택-비교.html">Ch 20 04절</a>은 시작점 <code>START</code> 뒤에 조건부 엣지를 두어 첫 노드를 골랐습니다. <a href="../ch23-persistence/01-체크포인터와-스레드.html">Ch 23 01절</a>은 체크포인터와 스레드 이름으로, 앞 실행의 칸 값에서 이어 실행했습니다.</p><p><a href="../../part5/ch19-model-tools/05-bind_tools와-병렬-호출.html">Ch 19 05절</a>에서 도구 메시지는 호출 ID로 도구 요청과 짝지어졌습니다. <a href="../../part5/ch20-tool-node/01-ToolNode와-tools-condition.html">Ch 20 01절</a>은 모델을 부르지 않고, 도구 요청을 담은 응답을 손으로 만들어 도구 실행 노드에 넣었습니다. <a href="../ch21-create-agent/03-AgentState와-context-schema.html">Ch 21 03절</a>은 도구 매개변수에 실행 객체 표시 <code>ToolRuntime</code>을 붙여 <code>runtime.context</code>를 읽었습니다. <a href="../ch24-human-in-the-loop/01-interrupt-승인-게이트.html">Ch 24 01절</a>은 <code>Command(resume=…)</code>로 멈춘 실행에 사람의 답을 넣었습니다.</p><p><a href="01-Subagent-도구-위임.html">01절</a>은 전문 에이전트를 도구로 감싸, 중앙 에이전트가 일을 맡기는 서브에이전트를 보았습니다. 이 절의 두 담당도 <code>create_agent</code>로 만들고, 모델 객체 하나를 함께 씁니다. 함수 <code>show_messages</code>와 <code>sum_usage</code>는 01절처럼 도구 파일 <code>delegation_tools.py</code>에서 가져옵니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>항구에서 짐을 실은 바지선은 스스로 가지 못하고, 예인선이 밧줄로 끌어 줍니다. 바지선이 어느 자리에 이르면 밧줄을 다음 예인선에 옮겨 겁니다. 그때부터 바지선을 끄는 배는 다음 예인선이고, 앞 예인선은 밧줄을 푼 채 옆에 떠 있습니다. 누가 끄는지는 밧줄이 어느 배에 걸려 있는지를 보면 압니다.</p><p>바지선이 문의한 사람과의 대화이고, 두 예인선이 대출 규정 담당과 상호대차 담당입니다. 밧줄이 걸린 배는 담당 칸 <code>active_agent</code>에 적힌 담당입니다. 체크포인터가 그 칸을 저장하므로, 다음 차례에도 밧줄은 다음 예인선에 걸린 채로 시작합니다.</p><p>비유와 다른 점이 있습니다. 예인선은 밧줄만 옮기면 되지만, 도구로 넘길 때는 넘기기 요청과 그 답을 메시지로 직접 담아야 합니다. 요청만 담고 답을 빠뜨리면, 대화 기록에 답이 없는 요청이 남습니다.</p>
{{img:02-6-밧줄이-넘어간-예인선|흰 바탕에 잔잔한 파란 바다가 아래쪽에 있는 항구 그림입니다. 가운데에 나무 상자 넷을 실은 넓은 나무 바지선 한 척이 떠 있습니다. 바지선 앞쪽 기둥에 묶인 밧줄 한 줄이 오른쪽 빨간 예인선의 뒤쪽에 걸려 있습니다. 왼쪽의 파란 예인선은 바지선 바로 옆에 떠 있고, 자기 밧줄은 갑판 위에 감긴 채 바지선과 이어져 있지 않습니다. 글자·숫자·사람·손·화살표는 없는 그림|바지선을 끄는 밧줄은 오른쪽 예인선에 걸려 있고, 왼쪽 예인선의 밧줄은 제 갑판에 감겨 있습니다.}}
<p class="look"><b>그림 읽기</b> — 가운데 넓은 나무 바지선에는 나무 상자 넷이 실려 있습니다. 바지선 앞 기둥에서 나온 밧줄 한 줄이 오른쪽 빨간 예인선에 걸려 있어, 지금 바지선을 끄는 배는 이 배입니다. 왼쪽 파란 예인선은 바지선 옆에 붙어 있지만, 밧줄이 자기 갑판에 감겨 있어 바지선과 이어지지 않았습니다. 바지선이 문의한 사람과의 대화이고, 밧줄이 걸린 빨간 예인선이 담당 칸에 적힌 상호대차 담당입니다. 두 배의 색과 상자의 수는 어떤 값과도 짝짓지 않습니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>핸드오프(handoff)</td><td>다음 차례에 문의한 사람과 대화할 담당 자체를 바꾸는 일입니다. 전화 상담원이 담당 부서로 전화를 연결해 주면, 그다음 말은 그 부서 직원과 나누는 것과 같습니다. 이 절에서는 노드나 도구가 <code>Command</code>로 다음 노드를 고르고, 담당 칸에 새 담당 이름을 남깁니다.</td></tr><tr><td>담당 칸</td><td>다음 차례에 대화할 담당 이름을 적어 두는 상태 칸입니다. 창구 앞에 걸어 둔 「지금 담당」 명패와 같습니다. 이 절에서는 칸 <code>active_agent</code>이고, 조건 함수 <code>pick_desk</code>가 이 칸을 읽어 첫 노드를 고릅니다.</td></tr><tr><td>하위 그래프</td><td>다른 그래프의 노드로 들어간 컴파일한 그래프입니다. 한 부서가 안에서 일을 나눠 해도, 회사 조직도에서는 칸 하나로 보이는 것과 같습니다. 이 절에서는 메서드 <code>add_node</code>에 함수 대신 넘긴 작은 그래프와 두 에이전트 그래프입니다.</td></tr><tr><td>넘기기 도구</td><td>모델이 불러 담당을 넘기는 도구입니다. 창구 직원이 누르는 「담당 돌리기」 단추와 같습니다. 이 절에서는 <code>transfer_to_interlibrary</code>이고, <code>Command(…, graph=Command.PARENT)</code>와 도구 메시지를 함께 내놓습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 노트북 3절 출력 <code>저장된 담당 칸: interlibrary_desk</code>가 핸드오프 뒤 담당 칸의 값입니다. 둘째 차례의 출력 <code>이번 차례에 지난 노드: ['interlibrary_desk']</code>는 받은 담당에서 시작했다는 표시입니다.</p>
{{mermaid:02-1-코드가-넘기는-두-담당|위에서 아래로 읽는 흐름도입니다. 맨 위 회색 원통 InMemorySaver 스레드마다 담당 칸 저장이 다음 차례에 읽음이라는 선으로 그 아래 회색 둥근 상자 START 시작점 조건 함수 pick_desk가 담당 칸을 읽고 고름과 이어집니다. 시작점에서 점선 둘이 나가, 담당 칸이 빈 글이면 파란 상자 loan_desk 대출 규정 담당 Command로 넘기거나 답함으로, 담당 칸이 interlibrary_desk면 파란 상자 interlibrary_desk 상호대차 담당으로 갑니다. loan_desk에서 goto interlibrary_desk 점선이 상호대차 담당으로, goto END 점선이 회색 둥근 상자 END 끝점으로 갑니다. 상호대차 담당에서는 실선이 끝점으로 가는 그림|시작점 뒤 조건 함수가 저장된 담당 칸을 읽어 첫 노드를 고르고, 첫 담당은 Command로 상호대차 담당에게 넘깁니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 시작점 아래 점선과 실선의 자리는 노트북 2절에서 출력한 구조 문자열의 화살표 다섯 줄과 같습니다. 파란 상자는 우리가 적은 노드이고, 회색 둥근 상자는 시작점과 끝점입니다. 조건 함수 pick_desk는 노드가 아니어서 따로 상자를 두지 않고 시작점 상자 안에 적었습니다. 맨 위 회색 원통은 체크포인터이고, 선은 다음 차례에 조건 함수가 저장된 담당 칸을 읽는다는 뜻입니다.</p>
<h3>담당 칸과 체크포인터가 다음 차례를 정합니다</h3><p>노드 <code>loan_desk</code>는 글에 「다른 도서관」이 있으면 <code>Command(goto="interlibrary_desk", update=…)</code>를 내놓습니다. 갱신에 담당 칸 값 <code>interlibrary_desk</code>가 들어 있어, 넘긴 사실이 상태에 남습니다. 시작점 뒤 조건 함수 <code>pick_desk</code>는 이 칸을 읽고 이번 차례를 시작할 노드를 고릅니다. 체크포인터가 스레드마다 칸 값을 저장하므로, 같은 스레드의 다음 차례는 받은 담당에서 시작합니다.</p><p>01절의 서브에이전트와 견주면 차이가 분명합니다. 서브에이전트는 답을 받아 오고, 문의한 사람과는 중앙 에이전트가 계속 대화했습니다. 핸드오프는 답을 받아 오지 않고, 다음 차례부터 받은 담당이 직접 대화합니다. 그래서 이 절 그래프에는 중앙 에이전트가 없고, 담당끼리 넘깁니다.</p>
<h3>도구로 넘길 때는 도구 메시지를 함께 담습니다</h3><p>모델이 넘기게 하려면 넘기기 도구를 둡니다. 도구가 내놓는 <code>Command</code>가 지금 그래프로 가면, 도구 실행 노드가 도구 메시지 짝을 검사해 없으면 오류를 냅니다. 하위 그래프 안에서 <code>graph=Command.PARENT</code>로 바깥 그래프에 가면 이 검사를 하지 않습니다. 또 하위 그래프 안에서 모델이 쓴 요청 응답은 바깥 그래프에 저절로 들어가지 않습니다. 그래서 공식 문서의 넘기기 도구는 도구 요청이 든 응답과 도구 메시지를 갱신에 함께 담습니다.</p><p>객체 <code>Command</code>는 이 과정에서 세 자리에 나왔습니다. Ch 13 06절은 노드가 다음 노드를 고를 때 <code>goto</code>를 썼습니다. Ch 24 01절은 멈춘 실행에 사람의 답을 넣을 때 <code>resume</code>을 썼습니다. 이 절의 <code>graph=Command.PARENT</code>는 하위 그래프 안에서 바깥 그래프의 노드로 갈 때 씁니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2~5절은 모델을 부르지 않습니다. 넘기는 구조와 체크포인터의 동작을 실행마다 같은 값으로 먼저 보려는 것입니다. 2절은 두 담당 노드와 조건 함수로 그래프를 만들고 체크포인터를 붙입니다. 3절은 같은 스레드에 두 글을 차례로 넣고, 값 바꿔 보기로 새 스레드에 둘째 글을 넣습니다. 4절은 넘길 노드 이름을 잘못 적어 보고, 5절은 도구 메시지 없이 넘기는 도구 둘을 손으로 만든 응답으로 실행합니다.</p><p>6~7절은 실제 OpenAI 모델 <code>gpt-5.4-mini</code>를 temperature 0으로 부릅니다. 두 담당을 에이전트로 바꾼 바깥 그래프를 같은 스레드로 두 차례 실행합니다. 첫 차례에 넘기면 요청이 2번, 둘째 차례가 1번이라 노트북 한 번에 모두 3번입니다. 요금표로 어림한 예상 비용은 0.002달러 아래이고, 청구 금액이 아닙니다. 읽거나 쓰는 파일은 없습니다.</p>
{{notebook:02-Handoff-상태-전환}}
<p class="look"><b>확인할 점</b> — 노트북 3절에서 <code>이번 차례에 지난 노드: ['interlibrary_desk']</code>와, 새 스레드의 <code>실행 흔적 칸: ['loan_desk']</code>를 견줍니다. 4절에서는 오류 없이 <code>답 칸이 빈 글인가: True</code>가 나오는지 봅니다. 5절에서는 <code>받은 오류: ValueError</code>와, 바깥 그래프의 메시지 목록에 도구 메시지가 없는지 확인합니다.</p>
{{mermaid:02-2-같은-스레드의-두-차례|큰 칸 둘이 위아래로 놓인 그림입니다. 위 큰 칸 스레드 desk-1 안에는 작은 칸 둘이 나란히 있습니다. 왼쪽 작은 칸 첫 차례에는 초록 상자 다른 도서관 책을 묻는 글에서 노란 상자 실행 흔적 loan_desk interlibrary_desk 담당 칸 저장 interlibrary_desk로 화살표가 갑니다. 저장된 담당 칸이라는 화살표가 오른쪽 작은 칸 둘째 차례로 가고, 그 칸에는 초록 상자 며칠 뒤에 받는지 묻는 글에서 노란 상자 이번 차례에 지난 노드 interlibrary_desk 상호대차 담당이 답함으로 화살표가 갑니다. 아래 큰 칸 스레드 desk-2에는 초록 상자 같은 둘째 글에서 노란 상자 실행 흔적 loan_desk 대출 규정 담당이 답함으로 화살표가 가는 그림|같은 스레드의 둘째 차례는 상호대차 담당에서 바로 시작했고, 새 스레드에 넣은 같은 글은 첫 담당이 받았습니다.}}
<p class="look"><b>도식 읽기</b> — 위 큰 칸은 같은 스레드 desk-1의 두 차례이고, 아래 큰 칸은 스레드 이름만 바꾼 값 바꿔 보기입니다. 초록 상자는 넣은 글이고, 노란 상자는 노트북 3절의 출력입니다. 두 작은 칸 사이 화살표는 첫 차례에 저장된 담당 칸이 둘째 차례로 이어진다는 뜻입니다. 아래 큰 칸은 위 칸과 저장된 값을 나누지 않아 화살표 없이 두었습니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>앞 절반의 값은 모델을 부르지 않아 실행마다 같습니다. 첫 차례는 첫 담당이 넘기고 받은 담당이 답해, 실행 흔적에 노드 이름이 둘 남았습니다. 같은 스레드의 둘째 차례는 저장된 담당 칸을 읽고 상호대차 담당 한 노드만 지났습니다. 새 스레드에 같은 둘째 글을 넣자, 첫 담당이 받아 직접 답했습니다.</p>
{{mermaid:02-3-이름-오타는-조용히-끝남|위에서 아래로 읽는 흐름도입니다. 맨 위 파란 상자 loan_desk_typo goto interlibrary_dsk 담당 칸 interlibrary_desk에서 오른쪽 아래로 화살표가 노란 상자 경고 글 한 줄 없는 이름으로 쓴 값은 무시함 오류 없이 끝남으로 가고, 다시 아래 노란 상자 실행 흔적 loan_desk 답 칸이 빈 글 True 담당 칸 interlibrary_desk로 갑니다. 파란 상자의 왼쪽 아래에는 회색 상자 interlibrary_desk 실행되지 않음이 이름이 달라 가지 않음이라는 점선으로만 이어진 그림|넘길 노드 이름에서 글자 하나를 빠뜨리자, 오류 없이 첫 담당만 지나고 끝났고 담당 칸만 넘긴 것처럼 바뀌었습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 파란 상자는 이름을 잘못 적은 우리 노드이고, 노란 상자 둘은 노트북 4절에서 출력으로 확인한 값입니다. 회색 상자는 등록은 되어 있지만 이번 실행에서 지나지 않은 노드입니다. 점선에 화살표가 없는 것은, 적은 이름이 달라 그 노드로 가지 않았다는 뜻입니다.</p>
<p>넘길 노드 이름에서 글자 하나를 빠뜨리자, 오류 없이 첫 담당만 지나고 끝났습니다. 담당 칸은 넘긴 것처럼 <code>interlibrary_desk</code>로 바뀌었지만, 답 칸은 비어 있었습니다. 출력에 남은 것은 경고 글 한 줄뿐이라, 이름 오타는 멈춤으로 드러나지 않습니다.</p>
{{mermaid:02-4-도구-메시지-짝-검사|맨 위 초록 상자 손으로 만든 응답 도구 요청 하나 도구 메시지 없음에서 화살표 둘이 나란한 두 칸으로 갑니다. 왼쪽 칸 지금 그래프로 가는 Command에는 파란 상자 hand_off_plain 담당 칸만 갱신에서 노란 상자 받은 오류 ValueError 짝이 되는 도구 메시지가 없음으로 화살표가 갑니다. 오른쪽 칸 graph=Command.PARENT에는 파란 상자 hand_off_parent 바깥 그래프의 상호대차 담당으로에서 노란 상자 오류 없음 담당 칸 interlibrary_desk HumanMessage AIMessage 도구 요청 AIMessage 받은 쪽이 손으로 적은 답으로 화살표가 갑니다. 맨 아래 회색 상자 짝 검사는 지금 그래프로 갈 때만 소스 확인 tool_node.py가 있는 그림|도구 메시지 없이 넘기자, 지금 그래프로 가는 쪽은 ValueError로 멈췄고 바깥 그래프로 가는 쪽은 답 없는 도구 요청을 남기고 넘어갔습니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 초록 상자는 노트북 5절에서 손으로 만든 응답이고, 두 칸은 가는 그래프만 다른 두 도구입니다. 파란 상자는 우리가 적은 도구이고, 노란 상자는 5절에서 받아 출력한 오류와 메시지 목록입니다. 오른쪽 칸은 손으로 만든 응답을 바깥 그래프 입력에 넣어 둔 장면입니다. 그 목록에는 도구 요청 뒤에 도구 메시지가 없고, 받은 쪽이 손으로 적은 답이 바로 붙었습니다. 맨 아래 회색 상자는 설치판 소스로 확인한 까닭이라 출력 값과 색을 달리했습니다.</p>
<p>도구 메시지 없이 넘기는 두 도구는 결과가 갈렸습니다. 지금 그래프로 가는 <code>Command</code>는 <code>ValueError</code>로 멈췄습니다. 바깥 그래프로 가는 <code>Command</code>는 오류 없이 넘어갔지만, 기록에는 도구 요청 바로 뒤에 받은 쪽 노드가 적은 응답이 붙었습니다. 이 장면은 도구 요청이 든 응답을 바깥 그래프 입력에 손으로 넣어 둔 경우입니다. 오류가 나지 않은 쪽이 오히려 망가진 기록을 남긴 셈입니다.</p><p>실제 모델로 바꾼 바깥 그래프는 2절 그래프와 구조 문자열이 같았습니다. 아래 표는 7절 두 차례의 값과 교재 출력의 토큰 수입니다. 토큰 수는 다시 실행하면 달라질 수 있습니다.</p>
<table><thead><tr><th>값</th><th>첫 차례(넘긴 차례)</th><th>둘째 차례</th><th>다시 실행하면</th></tr></thead><tbody><tr><td>담당 칸</td><td><code>interlibrary_desk</code></td><td><code>interlibrary_desk</code></td><td>넘기는지에 따라 달라질 수 있음</td></tr><tr><td>응답을 쓴 담당</td><td><code>loan_desk</code> · <code>interlibrary_desk</code></td><td><code>interlibrary_desk</code></td><td>넘기는지에 따라 달라질 수 있음</td></tr><tr><td>모델 요청 수</td><td>2</td><td>1</td><td>넘긴 차례는 첫 담당 1 + 받은 담당 1</td></tr><tr><td>입력 토큰(교재 출력)</td><td>471</td><td>259</td><td>달라질 수 있음</td></tr><tr><td>출력 토큰(교재 출력)</td><td>80</td><td>45</td><td>달라질 수 있음</td></tr></tbody></table>
<p>이번 실행에서 대출 규정 담당의 모델은 첫 차례에 넘기기 도구를 불렀고, 받은 담당이 답했습니다. 넘기기 도구가 담은 도구 메시지는 도구 요청과 호출 ID가 짝지어졌습니다. 둘째 차례는 2절 그래프처럼 받은 담당에서 시작해 요청이 1번이었습니다. 넘긴 차례의 요청은 첫 담당 1 + 받은 담당 1이고, 다음 차례는 받은 담당 1입니다. 흔들림 확인 다섯 번과 두 커널에서 모두 첫 차례에 넘겼습니다.</p>
{{mermaid:02-5-모델이-넘긴-두-차례|세로선 셋이 있는 차례 그림입니다. 왼쪽부터 바깥 그래프 team_graph, 연보라 띠 안의 대출 규정 담당 loan_desk와 상호대차 담당 interlibrary_desk입니다. 노란 메모 넘긴 실행 첫 차례 담당 칸 빈 글 뒤, 바깥 그래프에서 조건 함수가 첫 담당을 고름 화살표가 대출 규정 담당으로 갑니다. 대출 규정 담당에 노란 메모 첫 차례 요청 1 넘기기 도구 요청이 붙고, Command.PARENT 도구 메시지 함께라는 점선이 바깥 그래프로 돌아옵니다. 바깥 그래프에 노란 메모 도구 메시지가 그 요청의 답 True가 붙고, goto interlibrary_desk 화살표가 상호대차 담당으로 가며 노란 메모 첫 차례 요청 2 답이 붙습니다. 이어 노란 메모 둘째 차례 저장된 담당 칸 interlibrary_desk 뒤, 조건 함수가 받은 담당을 고름 화살표가 상호대차 담당으로 바로 가고 노란 메모 둘째 차례 요청 1 답이 붙은 그림|넘긴 실행에서 첫 차례는 첫 담당과 받은 담당이 한 번씩 요청했고, 둘째 차례는 받은 담당만 한 번 요청했습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 실행 차례대로 읽고, 세로선은 왼쪽부터 바깥 그래프, 대출 규정 담당, 상호대차 담당입니다. 연보라 띠는 실제로 부른 모델 gpt-5.4-mini가 요청을 받은 두 담당입니다. 노란 메모는 노트북 7절 출력이고, 요청 번호는 그 차례 안에서 나간 차례입니다. 실선 화살표는 바깥 그래프가 노드를 부르는 쪽, 점선 화살표는 넘기기 도구의 Command가 바깥으로 올라오는 쪽입니다.</p>
<p>모델을 부르는 7절은 답 글과 토큰 수가 실행마다 달라질 수 있습니다. 새 커널로 두 번 실행해 견주자, 토큰 수와 답 글이 찍힌 7절의 셀 둘만 달랐습니다. 응답을 쓴 담당, 호출 ID 짝, 요청 수가 찍힌 셀을 포함한 나머지 스물아홉 셀은 두 번 모두 같았습니다. 경고 글 한 줄이 찍힌 4절 셀도 두 번 같았습니다.</p>
<p class="look"><b>확인할 점</b> — 노트북 7절에서 <code>도구 메시지가 그 요청의 답인가: True</code>를 확인합니다. 두 차례의 <code>응답을 쓴 담당</code> 줄과 <code>모델 요청 수</code> 줄을 견줍니다. 넘길지는 모델이 정하므로, 다시 실행하면 달라질 수 있습니다. 교재 출력의 토큰 수와 답 글도 다시 실행하면 달라질 수 있어, 이 절의 결론에 쓰지 않았습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>넘길지는 대출 규정 담당의 모델이 정합니다. 노트북 밖에서 7절의 두 차례를 다섯 번 보내자, 다섯 번 모두 첫 차례에 넘겼습니다. 그래도 같은 요청이 실행한 때에 따라 달라질 수 있습니다. 넘기지 않으면 첫 차례 요청은 대출 규정 담당 1번이 되고, 담당 칸이 빈 글로 남아 다음 차례도 첫 담당에서 시작합니다.</li><li>상호대차 규정 글은 이 절이 실행 전에 정한 교재용 글이고, 실제 도서관 규정이 아닙니다. 대출 규정 글은 01절 글과 같습니다. 흐름을 보여 주려고 정한 예입니다.</li><li>공식 문서는 대부분의 핸드오프에 한 에이전트와 미들웨어로 만드는 모양을 권합니다. 여러 에이전트 하위 그래프 모양은 담당마다 따로 만든 에이전트가 필요할 때 쓰라고 적습니다. 이 절은 2절 바깥 그래프를 그대로 잇도록 하위 그래프 모양을 골랐고, 미들웨어 모양은 실행하지 않았습니다.</li><li>공식 문서의 예와 다른 점도 있습니다. 문서는 두 담당 모두에게 넘기기 도구를 주고, 담당 노드를 함수로 감싸고, 담당 뒤에 조건부 엣지를 둡니다. 이 절은 받는 쪽에 도구를 주지 않았고, 에이전트 그래프를 바로 노드로 넣었습니다. 그래서 한 번 넘긴 스레드는 뒤 차례도 모두 상호대차 담당이 받습니다. 대출 문의로 돌아가는 장면은 이 절에서 실행하지 않았습니다.</li><li>받는 쪽에도 넘기기 도구를 주면 두 담당이 서로 넘기며 끝나지 않을 수 있습니다. 그래서 7절 설정에 실행 한도 10을 함께 주었고, 한도를 넘는 장면은 이번에 실행하지 않았습니다.</li><li>넘기면서 하위 그래프를 떠날 때, 그 안에서 더한 메시지는 바깥에 저절로 들어가지 않습니다. 노트북 밖에서 모델 없는 작은 그래프로 확인했고, 노트북에서는 실행하지 않았습니다.</li><li>대출 규정 담당이 넘기지 않고 답을 마치면, 이어지는 엣지가 없어 그 차례의 실행이 끝납니다. 이 장면은 노트북에서 실행하지 않았습니다. 공식 문서의 예도 한 응답에 넘기기 도구 하나만 부른 경우를 전제한다고 적습니다. 이번 흔들림 확인 다섯 번에는 한 응답에 넘기기 요청이 둘인 경우도 없었고, 그런 실행은 04절 4절에서 봅니다.</li><li>도구 메시지가 빠진 기록으로 서비스 모델을 부르는 장면은 실행하지 않았습니다. 넘길 노드 이름의 오타는 설치판 langgraph 1.2.11 <code>pregel/_algo.py</code> 311~313행이 경고만 남기고 넘어갑니다. 넘긴 뒤에는 지나간 노드를 출력해 보는 편이 안전합니다.</li><li>체크포인터 <code>InMemorySaver</code>는 프로그램 메모리에만 저장합니다. 커널을 새로 띄워도 담당 칸을 이어 가려면, 상태를 저장하는 다른 체크포인터를 씁니다. <a href="../ch23-persistence/02-PostgresSaver-준비와-스키마.html">Ch 23 02절</a>은 PostgreSQL, <a href="../ch23-persistence/03-스레드-재개와-대화-이어가기.html">03절</a>은 SQLite 체크포인터였고, 이 절에서는 실행하지 않았습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>노드가 <code>Command</code>로 다음 노드와 담당 칸을 함께 바꾸면, 다음 차례에 대화할 담당이 바뀝니다.</li><li>같은 스레드의 다음 차례는 저장된 담당 칸을 읽고 받은 담당에서 시작했고, 새 스레드는 첫 담당에서 시작했습니다.</li><li>도구로 넘길 때는 도구 메시지를 함께 담습니다. 요청은 넘긴 차례에 첫 담당 1 + 받은 담당 1, 다음 차례에 받은 담당 1입니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href="03-Router-분류와-병렬-실행.html">03절</a>에서는 요청을 분류해, 고른 담당 여럿에게 함께 보내는 모양을 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 같은 스레드의 둘째 차례가 첫 담당을 건너뛴 까닭은 무엇인가요?</p><p class="quiz-a">시작점 뒤 조건 함수가 체크포인트에 저장된 담당 칸 <code>interlibrary_desk</code>를 읽고, 그 노드에서 시작했기 때문입니다. 새 스레드에는 저장된 칸이 없어 첫 담당에서 시작했습니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">2. 넘길 노드 이름을 <code>goto</code>에 잘못 적으면 어떻게 되었나요?</p><p class="quiz-a">오류 없이 경고 글 한 줄만 남기고 끝났습니다. 실행 흔적에는 첫 담당만 있었고 답 칸은 비었지만, 담당 칸은 넘긴 것처럼 바뀌었습니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">3. 넘기기 도구가 도구 메시지를 직접 만들어 갱신에 담는 까닭은 무엇인가요?</p><p class="quiz-a">바깥 그래프로 가는 <code>Command</code>는 도구 실행 노드가 도구 메시지 짝을 검사하지 않습니다. 하위 그래프 안에서 쓴 요청 응답도 바깥에 저절로 들어가지 않아, 도구가 요청 응답과 도구 메시지를 함께 담습니다. 요청 응답만 담고 도구 메시지를 빠뜨리면, 오류 없이 답이 없는 도구 요청이 기록에 남습니다. 틀렸다면 노트북 5절과 6절을 다시 읽습니다.</p><p class="quiz-q">4. 동료가 「핸드오프도 첫 담당이 답을 받아 최종 답을 쓰니, 넘긴 차례의 요청은 셋」이라고 말합니다. 이 절의 셈으로는 몇 번인가요?</p><p class="quiz-a">두 번입니다. 첫 담당의 넘기기 요청 1과 받은 담당의 답 1이고, 받은 담당의 답이 그대로 그 차례의 답입니다. 첫 담당은 답을 받아 다시 쓰지 않습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs">LangChain Handoffs</a></div>확인 2026-09-28 · 상태 칸으로 담당을 바꾸고 차례를 넘어 그 칸을 저장하는 모양이 있습니다. 도구 요청에는 호출 ID가 같은 도구 메시지가 있어야 하고, 없으면 대화 기록이 망가진다고 적습니다. 한 에이전트와 미들웨어 모양, 여러 에이전트 하위 그래프 모양을 함께 적습니다. 예는 한 응답에 넘기기 도구 하나만 부른 경우를 전제한다고 적습니다.</li><li>langgraph 1.2.11 소스 <code>types.py</code> 799~848행은 <code>Command</code>의 칸이고, 806행이 <code>Command.PARENT</code>의 뜻입니다.</li><li>langgraph-prebuilt 1.1.0 소스 <code>prebuilt/tool_node.py</code> 1559~1563행은 도구 메시지 짝을 검사하는 자리입니다. 지금 그래프로 가는 <code>Command</code>만 검사합니다. 이 패키지는 langgraph를 설치하면 함께 설치됩니다.</li><li>langgraph 1.2.11 소스 <code>pregel/_algo.py</code> 311~313행은 없는 이름으로 쓴 값을 경고만 남기고 버리는 자리입니다.</li><li>langchain 1.4.0 소스 <code>agents/factory.py</code> 1455~1456행은 에이전트 이름을 응답의 칸 <code>name</code>에 넣는 자리입니다.</li><li>객체 <code>Command</code>의 갱신과 이동은 Ch 13 06절에서 보았습니다. 시작점 뒤 조건부 엣지는 Ch 20 04절, 체크포인터와 스레드는 Ch 23 01절에서 보았습니다.</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# Handoff 상태 전환

**이 노트북에서 할 일**

1. 모델 없이, 노드가 담당을 넘기고 체크포인터가 다음 차례의 담당을 이어 주는 그래프를 만듭니다.
2. 도구가 담당을 넘길 때 도구 메시지가 빠지면 생기는 일을, 손으로 만든 응답으로 봅니다.
3. 실제 모델이 넘기기 도구로 담당을 넘기는 두 차례 대화에서, 응답을 쓴 담당과 요청 수를 셉니다.

**준비물** — 2~5절은 모델을 부르지 않아 API 키 없이 실행됩니다.
6~7절은 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 7절에서 같은 스레드로 두 차례 실행합니다.
첫 차례에 담당을 넘기면 요청이 2번, 둘째 차례가 1번이라 모두 3번입니다.
요금표로 어림한 예상 비용은 0.002달러 아래이고, 청구 금액이 아닙니다.

2~5절에서 모델을 뺀 것은 넘기는 구조와 체크포인터의 동작을 실행마다 같은 값으로 먼저 보려는 것입니다.
모델의 답 글과 넘기는지는 실행마다 달라질 수 있습니다.
걸린 시간은 재지 않았습니다.

읽거나 쓰는 파일은 없고, 체크포인트는 프로그램 메모리에만 둡니다.
앞 챕터에서 배운 함수 둘은 도구 파일 `delegation_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 넷을 설치합니다.
판은 langchain 1.4.0과 langchain-openai 1.6.0입니다.
langgraph 1.2.11과 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~3절과 6절을 읽습니다.
노드와 도구가 담당을 넘기는 모양과, 다음 차례가 받은 담당에서 시작하는 자리입니다.
4~5절은 넘길 이름과 도구 메시지를 바꿔 보는 자리이고, 7절은 모델을 부르는 실행입니다.
이 두 자리는 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch26-delegation`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 읽는 흐름도입니다. 맨 위 회색 원통 InMemorySaver 스레드마다 담당 칸 저장이 다음 차례에 읽음이라는 선으로 그 아래 회색 둥근 상자 START 시작점 조건 함수 pick_desk가 담당 칸을 읽고 고름과 이어집니다. 시작점에서 점선 둘이 나가, 담당 칸이 빈 글이면 파란 상자 loan_desk 대출 규정 담당 Command로 넘기거나 답함으로, 담당 칸이 interlibrary_desk면 파란 상자 interlibrary_desk 상호대차 담당으로 갑니다. loan_desk에서 goto interlibrary_desk 점선이 상호대차 담당으로, goto END 점선이 회색 둥근 상자 END 끝점으로 갑니다. 상호대차 담당에서는 실선이 끝점으로 가는 그림](attachment:02-1-코드가-넘기는-두-담당.png)

위에서 아래로 읽습니다.
시작점 아래 점선과 실선의 자리는 노트북 2절에서 출력한 구조 문자열의 화살표 다섯 줄과 같습니다.
파란 상자는 우리가 적은 노드이고, 회색 둥근 상자는 시작점과 끝점입니다.
조건 함수 pick_desk는 노드가 아니어서 따로 상자를 두지 않고 시작점 상자 안에 적었습니다.
맨 위 회색 원통은 체크포인터이고, 선은 다음 차례에 조건 함수가 저장된 담당 칸을 읽는다는 뜻입니다.

### [2] markdown {}

## 1. 준비

이 절에서는 담당끼리 문의를 넘기는 모양을 봅니다.
절 제목의 Handoff는 핸드오프를 가리키고, 뜻은 2절에서 풉니다.

첫 셀은 패키지 넷을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:45.349270Z', 'iopub.status.busy': '2026-09-28T06:55:45.349089Z', 'iopub.status.idle': '2026-09-28T06:55:46.051236Z', 'shell.execute_reply': '2026-09-28T06:55:46.050688Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "langchain==1.4.0" "langchain-openai==1.6.0" "langgraph==1.2.11" "python-dotenv==1.2.3"
from importlib.metadata import version

print("langchain:", version("langchain"))
print("langchain-openai:", version("langchain-openai"))
print("langgraph:", version("langgraph"))
print("python-dotenv:", version("python-dotenv"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
langchain: 1.4.0
langchain-openai: 1.6.0
langgraph: 1.2.11
python-dotenv: 1.2.3

```

### [4] markdown {}

**결과 읽기** — 출력 줄 `langchain: 1.4.0`과 `langgraph: 1.2.11`이 보입니다.
네 판 모두 실습 폴더 잠금과 같은 판입니다.
체크포인터 `InMemorySaver`가 든 패키지는 langgraph를 설치하면 함께 설치됩니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
상태 형식과 그래프를 만드는 이름은 Ch 13에서 썼습니다.
체크포인터 `InMemorySaver`는 Ch 23 01절, 도구 실행 노드 `ToolNode`는 Ch 20 01절에서 썼습니다.
실행 객체 표시 `ToolRuntime`은 Ch 21 03절, 메시지 클래스 `ToolMessage`는 Ch 19 05절에서 보았습니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.052420Z', 'iopub.status.busy': '2026-09-28T06:55:46.052331Z', 'iopub.status.idle': '2026-09-28T06:55:46.577056Z', 'shell.execute_reply': '2026-09-28T06:55:46.576640Z'}, 'lesson_role': 'setup'}

```python
# 상태 형식(Ch 13 01·02절)·그래프와 Command(Ch 13 06절)·체크포인터(Ch 23 01절) 이름을 가져옵니다
import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.types import Command
# 에이전트(Ch 21 01절)·모델(Ch 6 01절)·메시지(Ch 13 04절·Ch 19 05절)·도구(Ch 19 01절·Ch 21 03절) 이름을 가져옵니다
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, AnyMessage, HumanMessage, ToolMessage
from langchain.tools import ToolRuntime, tool
# 앞 챕터에서 배운 함수 둘은 도구 파일에서 가져옵니다
from delegation_tools import show_messages, sum_usage

print("도구 파일에서 가져온 함수:", "show_messages, sum_usage")
```

출력:
```
도구 파일에서 가져온 함수: show_messages, sum_usage

```

### [6] markdown {}

**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: show_messages, sum_usage`가 보입니다.
Ch 19 06절 함수 `show_messages`는 메시지 목록을 한 줄씩 출력합니다.
Ch 19 05절 함수 `sum_usage`는 목록 안 응답마다 요청 하나로 세고 토큰을 더합니다.

앞에서 배운 함수는 `delegation_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다.

## 2. 코드가 담당을 넘기는 그래프

01절에서는 중앙 에이전트가 대출 규정 담당에게 일을 맡기고 답을 받아 왔습니다.
이 절에서는 문의한 사람이 담당과 바로 이야기하고, 담당이 다음 담당에게 문의를 넘깁니다.
이렇게 다음 차례에 대화할 담당 자체를 바꾸는 일을 핸드오프(handoff)라고 부릅니다.
전화 상담원이 담당 부서로 전화를 연결해 주면, 그다음 말은 그 부서 직원과 나누는 것과 같습니다.
이 절 코드에서는 노드가 `Command`로 다음 노드를 고르고, 칸 `active_agent`에 새 담당 이름을 남깁니다.

담당은 01절의 대출 규정 담당 `loan_desk`와, 새로 둔 상호대차 담당 `interlibrary_desk` 둘입니다.
상호대차는 다른 도서관의 책을 빌려 오는 일입니다.
2~5절은 모델을 부르지 않고, 담당 노드가 코드로 정한 규칙대로 넘깁니다.

먼저 상태 형식을 만듭니다.
칸 `active_agent`에는 다음 차례에 대화할 담당 이름을 적고, 이 절에서는 담당 칸이라고 부릅니다.
칸 `trace`에는 Ch 13 02절처럼 이어 붙이기 규칙을 적어, 지난 노드 이름이 쌓이게 합니다.

### [7] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.577806Z', 'iopub.status.busy': '2026-09-28T06:55:46.577742Z', 'iopub.status.idle': '2026-09-28T06:55:46.579463Z', 'shell.execute_reply': '2026-09-28T06:55:46.579162Z'}}

```python
# 문의 글·담당 칸·답 칸·실행 흔적 칸을 둔 상태 형식을 만듭니다(실행 흔적 칸에만 Ch 13 02절 이어 붙이기 규칙)
class DeskState(TypedDict):
    message: str
    active_agent: str
    reply: str
    trace: Annotated[list[str], operator.add]
```

출력:
```

```

### [8] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 넷 가운데 규칙을 적은 칸은 실행 흔적 칸 하나이고, 나머지 셋은 새 값이 오면 덮어씁니다.
체크포인터를 붙이면 실행 흔적 칸은 같은 스레드에서 차례를 넘어 계속 쌓입니다.

다음 셀은 첫 담당인 대출 규정 담당 노드입니다.
문의 글에 「다른 도서관」이 있으면 상호대차 담당에게 넘기고, 없으면 직접 답합니다.
넘길 때는 Ch 13 06절처럼 `Command` 하나에 담당 칸 갱신과 다음 노드 이름을 함께 담습니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.580004Z', 'iopub.status.busy': '2026-09-28T06:55:46.579941Z', 'iopub.status.idle': '2026-09-28T06:55:46.581694Z', 'shell.execute_reply': '2026-09-28T06:55:46.581366Z'}}

```python
# 첫 담당(대출 규정 담당) 노드입니다. 글에 「다른 도서관」이 있으면 상호대차 담당에게 넘기고, 없으면 직접 답합니다
def loan_desk(state):
    if "다른 도서관" in state["message"]:
        # 담당 칸 갱신과 다음 노드 이름을 Command 하나에 함께 담습니다(Ch 13 06절)
        update = {"active_agent": "interlibrary_desk", "trace": ["loan_desk"]}
        return Command(goto="interlibrary_desk", update=update)
    # 직접 답할 때는 다음 노드 이름으로 끝점 END를 적습니다
    update = {"active_agent": "loan_desk", "reply": "대출 규정 담당이 답합니다", "trace": ["loan_desk"]}
    return Command(goto=END, update=update)
```

출력:
```

```

### [10] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
넘기는 쪽 갱신에는 답 칸이 없어, 답은 받은 담당이 씁니다.
두 쪽 모두 담당 칸에는 다음 차례에 대화할 담당 이름을 적습니다.
넘길지는 이 셀의 글자 규칙이 정하고, 6절에서는 모델이 정합니다.

다음 셀은 상호대차 담당 노드입니다.

### [11] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.582222Z', 'iopub.status.busy': '2026-09-28T06:55:46.582171Z', 'iopub.status.idle': '2026-09-28T06:55:46.583605Z', 'shell.execute_reply': '2026-09-28T06:55:46.583308Z'}}

```python
# 상호대차 담당 노드입니다. 답 칸과 실행 흔적 칸에 자기 몫만 냅니다
def interlibrary_desk(state):
    return {"reply": "상호대차 담당이 답합니다", "trace": ["interlibrary_desk"]}
```

출력:
```

```

### [12] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
상호대차 담당은 담당 칸을 건드리지 않고, 답 칸과 실행 흔적 칸에 자기 몫만 냅니다.
답 글은 교재용으로 정한 한 줄이고, 누가 답했는지만 보여 줍니다.

다음 셀은 시작점 `START` 뒤에 둘 조건 함수입니다.
Ch 20 04절처럼 시작점 뒤에 조건부 엣지를 두면, 상태를 보고 첫 노드를 고를 수 있습니다.
이 함수는 저장된 담당 칸을 읽어, 상호대차 담당이면 그 노드에서 시작하게 합니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.584153Z', 'iopub.status.busy': '2026-09-28T06:55:46.584094Z', 'iopub.status.idle': '2026-09-28T06:55:46.585385Z', 'shell.execute_reply': '2026-09-28T06:55:46.585156Z'}}

```python
# 시작점 뒤에 둘 조건 함수입니다. 저장된 담당 칸을 읽어, 이번 차례를 시작할 노드 이름을 내놓습니다
def pick_desk(state):
    if state["active_agent"] == "interlibrary_desk":
        return "interlibrary_desk"
    return "loan_desk"
```

출력:
```

```

### [14] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
담당 칸이 빈 글이거나 `loan_desk`이면 첫 담당에서 시작합니다.
조건 함수는 노드가 아니라, 조건부 엣지가 부르는 함수입니다.

다음 셀은 두 노드와 조건 함수로 그래프를 만들고 체크포인터를 붙입니다.
노드 `loan_desk`를 등록할 때는 인자 `destinations`에 갈 수 있는 곳을 적습니다.
Ch 13 06절처럼 이 인자는 실행이 아니라 구조 문자열에만 쓰입니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.585890Z', 'iopub.status.busy': '2026-09-28T06:55:46.585838Z', 'iopub.status.idle': '2026-09-28T06:55:46.588470Z', 'shell.execute_reply': '2026-09-28T06:55:46.588170Z'}}

```python
# 두 담당 노드와 조건 함수로 그래프를 만들고, 체크포인터를 붙여 컴파일합니다
desk_builder = StateGraph(DeskState)
# 인자 destinations는 이 노드의 Command가 갈 수 있는 곳이고, 구조 문자열에만 쓰입니다(Ch 13 06절)
desk_builder.add_node("loan_desk", loan_desk, destinations=("interlibrary_desk", END))
desk_builder.add_node("interlibrary_desk", interlibrary_desk)
desk_builder.add_conditional_edges(START, pick_desk, ["loan_desk", "interlibrary_desk"])
desk_builder.add_edge("interlibrary_desk", END)
desk_graph = desk_builder.compile(checkpointer=InMemorySaver())
print("등록한 노드:", list(desk_builder.nodes))
```

출력:
```
등록한 노드: ['loan_desk', 'interlibrary_desk']

```

### [16] markdown {}

**결과 읽기** — 출력 줄 `등록한 노드: ['loan_desk', 'interlibrary_desk']`가 보입니다.
조건 함수 `pick_desk`는 노드로 등록하지 않아 이 목록에 없습니다.

다음 셀은 그래프가 그린 구조 문자열에서 화살표가 있는 줄만 출력합니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.588964Z', 'iopub.status.busy': '2026-09-28T06:55:46.588911Z', 'iopub.status.idle': '2026-09-28T06:55:46.607155Z', 'shell.execute_reply': '2026-09-28T06:55:46.606772Z'}}

```python
# 그래프가 스스로 그린 구조 문자열에서 화살표가 있는 줄만 골라 출력합니다(Ch 13 06절과 같은 모양)
structure_text = desk_graph.get_graph().draw_mermaid()
print("구조 문자열에서 화살표가 있는 줄:")
for line in structure_text.split("\n"):
    if "->" in line:
        print(line.strip())
```

출력:
```
구조 문자열에서 화살표가 있는 줄:
__start__ -.-> interlibrary_desk;
__start__ -.-> loan_desk;
loan_desk -.-> __end__;
loan_desk -.-> interlibrary_desk;
interlibrary_desk --> __end__;

```

### [18] markdown {}

**결과 읽기** — 라벨 줄 아래에 화살표 줄 다섯이 보입니다.
줄 `__start__ -.-> loan_desk;`와 `__start__ -.-> interlibrary_desk;`는 조건 함수가 고를 두 시작 노드입니다.
줄 `loan_desk -.-> interlibrary_desk;`와 `loan_desk -.-> __end__;`는 적어 둔 목적지라 점선입니다.
줄 `interlibrary_desk --> __end__;`만 실선인 고정 엣지입니다.

## 3. 같은 스레드에서 두 차례 묻기

첫 차례에는 다른 도서관의 책을 묻고, 둘째 차례에는 신청하면 며칠 뒤에 받는지 묻습니다.
둘째 글에는 「다른 도서관」이 없어, 첫 담당이 받으면 직접 답합니다.
실행 전에 예상해 봅니다.
같은 스레드라면 둘째 차례는 저장된 담당 칸을 읽고 상호대차 담당에서 바로 시작할 것입니다.

다음 셀은 스레드 `desk-1`에 첫 글을 넣어 실행합니다.
실행 뒤 Ch 23 01절 메서드 `get_state`로 저장된 마지막 체크포인트를 읽습니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.607736Z', 'iopub.status.busy': '2026-09-28T06:55:46.607673Z', 'iopub.status.idle': '2026-09-28T06:55:46.612459Z', 'shell.execute_reply': '2026-09-28T06:55:46.612202Z'}}

```python
# 스레드 desk-1에 첫 글을 넣어 실행하고, 저장된 마지막 체크포인트를 읽습니다(Ch 23 01절)
first_question = "다른 도서관에 있는 책도 빌려 볼 수 있나요?"
desk_config = {"configurable": {"thread_id": "desk-1"}}
first_input = {"message": first_question, "active_agent": "", "reply": "", "trace": []}
first_result = desk_graph.invoke(first_input, desk_config)
print("담당 칸:", first_result["active_agent"], "| 답 칸:", first_result["reply"])
print("실행 흔적 칸:", first_result["trace"])
saved = desk_graph.get_state(desk_config)
print("저장된 담당 칸:", saved.values["active_agent"])
print("다음에 실행할 노드:", saved.next)
```

출력:
```
담당 칸: interlibrary_desk | 답 칸: 상호대차 담당이 답합니다
실행 흔적 칸: ['loan_desk', 'interlibrary_desk']
저장된 담당 칸: interlibrary_desk
다음에 실행할 노드: ()

```

### [20] markdown {}

**결과 읽기** — 출력 줄 `담당 칸: interlibrary_desk | 답 칸: 상호대차 담당이 답합니다`가 보입니다.
출력 줄 `실행 흔적 칸: ['loan_desk', 'interlibrary_desk']`로, 첫 담당이 넘기고 받은 담당이 답했습니다.
출력 줄 `저장된 담당 칸: interlibrary_desk`는 체크포인트에 남은 값입니다.
출력 줄 `다음에 실행할 노드: ()`는 그래프가 끝까지 실행되어 남은 노드가 없다는 뜻입니다.

다음 셀은 같은 스레드에 둘째 글만 넣어 실행합니다.
담당 칸·답 칸·실행 흔적 칸은 넣지 않고, 체크포인트에 저장된 값을 씁니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.613032Z', 'iopub.status.busy': '2026-09-28T06:55:46.612980Z', 'iopub.status.idle': '2026-09-28T06:55:46.615803Z', 'shell.execute_reply': '2026-09-28T06:55:46.615488Z'}}

```python
# 같은 스레드에 둘째 글만 넣어 실행하고, 이번 차례에 더해진 실행 흔적만 잘라 봅니다
second_question = "신청하면 며칠 뒤에 받을 수 있나요?"
second_result = desk_graph.invoke({"message": second_question}, desk_config)
first_count = len(first_result["trace"])
second_trace = second_result["trace"][first_count:]
print("담당 칸:", second_result["active_agent"], "| 답 칸:", second_result["reply"])
print("실행 흔적 칸:", second_result["trace"])
print("이번 차례에 지난 노드:", second_trace)
```

출력:
```
담당 칸: interlibrary_desk | 답 칸: 상호대차 담당이 답합니다
실행 흔적 칸: ['loan_desk', 'interlibrary_desk', 'interlibrary_desk']
이번 차례에 지난 노드: ['interlibrary_desk']

```

### [22] markdown {}

**결과 읽기** — 출력 줄 `이번 차례에 지난 노드: ['interlibrary_desk']`가 보입니다.
둘째 차례는 첫 담당을 건너뛰고 상호대차 담당에서 바로 시작했습니다.
조건 함수가 체크포인트에 저장된 담당 칸 `interlibrary_desk`를 읽었기 때문입니다.
출력 줄 `실행 흔적 칸: ['loan_desk', 'interlibrary_desk', 'interlibrary_desk']`에는 앞 차례 흔적 뒤에 이름 하나가 더해졌습니다.

같은 스레드에서는 저장된 칸 값에서 시작하고, 새 입력에 넣은 칸만 바뀝니다.
그래서 담당 칸은 첫 차례에 넘겨받은 값 그대로였습니다.

다음 셀은 값 하나만 바꿔 봅니다.
바꿀 값은 스레드 이름이고, 같은 둘째 글을 새 스레드 `desk-2`에 넣습니다.
새 스레드에는 저장된 칸이 없어, Ch 23 01절처럼 칸을 모두 채운 입력을 넣습니다.
실행 전에 예상해 봅니다.
저장된 담당이 없으니 첫 담당에서 시작하고, 첫 담당이 직접 답할 것입니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.616308Z', 'iopub.status.busy': '2026-09-28T06:55:46.616256Z', 'iopub.status.idle': '2026-09-28T06:55:46.619663Z', 'shell.execute_reply': '2026-09-28T06:55:46.619257Z'}}

```python
# 값 바꿔 보기: 스레드 이름만 desk-2로 바꾸고, 새 스레드라 칸을 모두 채운 입력으로 둘째 글을 넣습니다
other_config = {"configurable": {"thread_id": "desk-2"}}
other_input = {"message": second_question, "active_agent": "", "reply": "", "trace": []}
other_result = desk_graph.invoke(other_input, other_config)
print("담당 칸:", other_result["active_agent"], "| 답 칸:", other_result["reply"])
print("실행 흔적 칸:", other_result["trace"])
```

출력:
```
담당 칸: loan_desk | 답 칸: 대출 규정 담당이 답합니다
실행 흔적 칸: ['loan_desk']

```

### [24] markdown {}

**결과 읽기** — 출력 줄 `담당 칸: loan_desk | 답 칸: 대출 규정 담당이 답합니다`가 보입니다.
출력 줄 `실행 흔적 칸: ['loan_desk']`로, 새 스레드는 첫 담당에서 시작했습니다.
같은 둘째 글이라도 어느 스레드로 보내느냐에 따라 받는 담당이 달랐습니다.
다음 차례의 담당은 글이 아니라, 스레드에 저장된 담당 칸이 정합니다.

## 4. 넘길 노드 이름을 잘못 적으면

넘길 노드 이름은 `goto`에 글로 적습니다.
이 글에 오타가 있으면 어떻게 되는지 봅니다.
바꿀 값은 첫 담당 노드가 적는 다음 노드 이름입니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.620284Z', 'iopub.status.busy': '2026-09-28T06:55:46.620228Z', 'iopub.status.idle': '2026-09-28T06:55:46.622105Z', 'shell.execute_reply': '2026-09-28T06:55:46.621752Z'}}

```python
# 넘길 노드 이름에서 글자 하나(e)를 빠뜨린 첫 담당 노드입니다(interlibrary_desk가 아니라 interlibrary_dsk)
def loan_desk_typo(state):
    update = {"active_agent": "interlibrary_desk", "trace": ["loan_desk"]}
    return Command(goto="interlibrary_dsk", update=update)
```

출력:
```

```

### [26] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
담당 칸에는 `interlibrary_desk`를 바르게 적고, 다음 노드 이름만 글자 하나를 빠뜨렸습니다.
이 그래프에는 이름이 `interlibrary_dsk`인 노드가 없습니다.

다음 셀은 이 노드를 첫 담당 자리에 둔 작은 그래프를 새로 만들어, 3절의 첫 글로 실행합니다.
2절 그래프와 달리 시작 엣지는 고정이고, 체크포인터와 `destinations`는 두지 않았습니다.
실행 전에 예상해 봅니다.
없는 노드로 가라고 했으니 오류가 날 것 같습니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.622691Z', 'iopub.status.busy': '2026-09-28T06:55:46.622631Z', 'iopub.status.idle': '2026-09-28T06:55:46.626254Z', 'shell.execute_reply': '2026-09-28T06:55:46.625894Z'}}

```python
# 오타 난 노드를 첫 담당 자리에 둔 그래프를 만들어, 3절의 첫 글로 실행합니다(체크포인터 없음)
typo_builder = StateGraph(DeskState)
typo_builder.add_node("loan_desk", loan_desk_typo)
typo_builder.add_node("interlibrary_desk", interlibrary_desk)
typo_builder.add_edge(START, "loan_desk")
typo_builder.add_edge("interlibrary_desk", END)
typo_result = typo_builder.compile().invoke(first_input)
print("담당 칸:", typo_result["active_agent"])
print("실행 흔적 칸:", typo_result["trace"])
print("답 칸이 빈 글인가:", typo_result["reply"] == "")
```

출력:
```
Task loan_desk with path ('__pregel_pull', 'loan_desk') wrote to unknown channel branch:to:interlibrary_dsk, ignoring it.
담당 칸: interlibrary_desk
실행 흔적 칸: ['loan_desk']
답 칸이 빈 글인가: True

```

### [28] markdown {}

**결과 읽기** — 오류 없이 셀이 끝났고, 출력 줄 `실행 흔적 칸: ['loan_desk']`가 보입니다.
상호대차 담당은 실행되지 않았고, 출력 줄 `답 칸이 빈 글인가: True`처럼 아무도 답하지 않았습니다.
그런데 출력 줄 `담당 칸: interlibrary_desk`는 넘긴 것처럼 바뀌었습니다.
출력에는 경고 글 한 줄이 함께 보이고, 이 글만 이름이 틀렸다는 것을 알려 줍니다.

경고 글 끝의 `wrote to unknown channel branch:to:interlibrary_dsk, ignoring it.`은 없는 이름으로 가려던 값을 버렸다는 뜻입니다.
설치판 langgraph 1.2.11 `pregel/_algo.py` 311~313행이 이 경고만 남기고 넘어가는 자리입니다.
이 글은 파이썬 표준 모듈 `logging`으로 남긴 경고라, 기록 설정에 따라 보이지 않을 수도 있습니다.
이름 오타는 실행을 멈추지 않으므로, 넘긴 뒤에는 실행 흔적 칸처럼 지나간 노드를 출력해 보는 편이 안전합니다.

## 5. 도구가 넘길 때는 도구 메시지를 함께

6절에서는 모델이 도구를 불러 담당을 넘깁니다.
도구가 내놓는 `Command`에는 지켜야 할 약속이 하나 있습니다.
Ch 19 05절에서 본 것처럼, 도구 요청 하나에는 같은 호출 ID의 도구 메시지가 짝지어 있어야 합니다.
이 절에서는 모델 없이, Ch 20 01절처럼 손으로 만든 응답으로 이 약속을 봅니다.

다음 셀은 메시지 칸과 담당 칸을 둔 상태 형식입니다.
칸 구성이 2절과 달라 이름을 새로 붙이고, 6~7절의 바깥 그래프도 이 형식을 씁니다.

### [29] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.626930Z', 'iopub.status.busy': '2026-09-28T06:55:46.626874Z', 'iopub.status.idle': '2026-09-28T06:55:46.628565Z', 'shell.execute_reply': '2026-09-28T06:55:46.628214Z'}}

```python
# 메시지 칸(Ch 13 04절 메시지 규칙)과 담당 칸을 둔 상태 형식을 만듭니다(5~7절에서 씀)
class TeamState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    active_agent: str
```

출력:
```

```

### [30] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
메시지 칸에는 Ch 13 04절 메시지 규칙 `add_messages`를 적었습니다.
담당 칸에는 규칙을 적지 않아 새 값이 오면 덮어씁니다.

다음 두 셀은 도구 메시지 없이 담당을 넘기는 도구 둘입니다.
첫 도구는 지금 그래프의 담당 칸만 바꾸는 `Command`를 내놓습니다.

함수 위의 `@tool` 줄은 데코레이터 줄입니다.
데코레이터 줄은 함수 위에 붙여 그 함수를 다른 것으로 감싸는 표시이고, 뜻은 Ch 2 09절에 있습니다.
이 셀에서는 이 줄이 아래 함수를 도구로 등록하고, Ch 19 01절처럼 독스트링이 도구 설명이 됩니다.

### [31] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.629214Z', 'iopub.status.busy': '2026-09-28T06:55:46.629157Z', 'iopub.status.idle': '2026-09-28T06:55:46.631548Z', 'shell.execute_reply': '2026-09-28T06:55:46.631196Z'}}

```python
# 도구 메시지 없이, 지금 그래프의 담당 칸만 바꾸는 Command를 내놓는 도구입니다
@tool
def hand_off_plain():
    """상호대차 담당에게 넘깁니다(도구 메시지를 넣지 않고, 지금 그래프로)."""
    return Command(update={"active_agent": "interlibrary_desk"})
```

출력:
```

```

### [32] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 도구에는 모델이 넘길 인자가 없고, 담당 칸 갱신 하나만 담은 `Command`를 내놓습니다.
갱신에 메시지 칸이 없으니, 도구 요청에 답하는 도구 메시지도 없습니다.

다음 셀의 둘째 도구는 인자 `graph=Command.PARENT`를 더합니다.
도구를 부른 그래프가 다른 그래프의 노드로 들어 있을 때, 그 바깥 그래프에서 `goto` 노드를 찾으라는 표시입니다.
설치판 langgraph 1.2.11 `types.py` 806행은 이 값을 가장 가까운 바깥 그래프라고 적습니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.632233Z', 'iopub.status.busy': '2026-09-28T06:55:46.632175Z', 'iopub.status.idle': '2026-09-28T06:55:46.634701Z', 'shell.execute_reply': '2026-09-28T06:55:46.634369Z'}}

```python
# 도구 메시지 없이, 바깥 그래프의 상호대차 담당 노드로 가는 Command를 내놓는 도구입니다
@tool
def hand_off_parent():
    """상호대차 담당에게 넘깁니다(도구 메시지를 넣지 않고, 바깥 그래프로)."""
    update = {"active_agent": "interlibrary_desk"}
    # graph=Command.PARENT는 이 그래프를 노드로 둔 바깥 그래프에서 goto 노드를 찾으라는 표시입니다
    return Command(goto="interlibrary_desk", update=update, graph=Command.PARENT)
```

출력:
```

```

### [34] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
갱신과 다음 노드 이름은 2절 첫 담당 노드와 같은 모양이고, 가는 그래프만 다릅니다.
이 도구도 도구 메시지를 넣지 않았습니다.

다음 셀은 두 도구를 가진 도구 실행 노드 하나로 작은 그래프를 만듭니다.

### [35] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.635414Z', 'iopub.status.busy': '2026-09-28T06:55:46.635362Z', 'iopub.status.idle': '2026-09-28T06:55:46.638986Z', 'shell.execute_reply': '2026-09-28T06:55:46.638584Z'}}

```python
# 두 도구를 가진 도구 실행 노드(Ch 20 01절) 하나로 작은 그래프를 만듭니다
tools_builder = StateGraph(TeamState)
tools_builder.add_node("tools", ToolNode([hand_off_plain, hand_off_parent]))
tools_builder.add_edge(START, "tools")
tools_builder.add_edge("tools", END)
tools_graph = tools_builder.compile()
print("등록한 노드:", list(tools_builder.nodes))
```

출력:
```
등록한 노드: ['tools']

```

### [36] markdown {}

**결과 읽기** — 출력 줄 `등록한 노드: ['tools']`가 보입니다.
시작점에서 도구 실행 노드로 가고, 도구 실행 노드에서 끝나는 그래프입니다.

다음 셀은 모델을 부르지 않고, 첫 도구를 요청하는 응답을 손으로 만들어 넣습니다.
응답에 담는 도구 요청은 Ch 19 04절의 칸 넷(`name`·`args`·`id`·`type`)입니다.
올라오는 오류는 Ch 23 01절처럼 이 셀에서만 이름을 적어 받고 출력합니다.

### [37] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.639610Z', 'iopub.status.busy': '2026-09-28T06:55:46.639550Z', 'iopub.status.idle': '2026-09-28T06:55:46.643242Z', 'shell.execute_reply': '2026-09-28T06:55:46.642881Z'}}

```python
# 모델 없이, hand_off_plain 요청을 담은 응답을 손으로 만들어 넣고 올라온 오류를 받아 출력합니다
plain_call = {"name": "hand_off_plain", "args": {}, "id": "hand_call_1", "type": "tool_call"}
plain_request = AIMessage(content="", tool_calls=[plain_call])
try:
    tools_graph.invoke({"messages": [plain_request], "active_agent": ""})
except ValueError as error:
    error_text = str(error)
    print("받은 오류:", type(error).__name__)
    print("오류 글 앞부분:", error_text[:66])
```

출력:
```
받은 오류: ValueError
오류 글 앞부분: Expected to have a matching ToolMessage in Command.update for tool

```

### [38] markdown {}

**결과 읽기** — 출력 줄 `받은 오류: ValueError`가 보입니다.
오류 글은 `Expected to have a matching ToolMessage in Command.update for tool`로 시작합니다.
도구 요청에 짝이 되는 도구 메시지가 `Command`의 갱신에 없다는 뜻입니다.
지금 그래프로 가는 `Command`는 도구 실행 노드가 이 짝을 검사합니다.

다음 셀은 둘째 도구가 갈 바깥 그래프의 받는 쪽 노드입니다.
상호대차 담당이 답한 것처럼, 응답 한 줄을 손으로 적어 냅니다.

### [39] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.643849Z', 'iopub.status.busy': '2026-09-28T06:55:46.643799Z', 'iopub.status.idle': '2026-09-28T06:55:46.645563Z', 'shell.execute_reply': '2026-09-28T06:55:46.645259Z'}}

```python
# 바깥 그래프의 받는 쪽 노드입니다. 상호대차 담당의 답 한 줄을 손으로 적어 냅니다(모델 없음)
def interlibrary_note(state):
    note = AIMessage(content="상호대차 담당이 답합니다.")
    return {"messages": [note]}
```

출력:
```

```

### [40] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
모델을 부르지 않고, 정해 둔 글을 응답으로 내놓는 보통 함수입니다.

다음 셀은 앞에서 만든 작은 그래프를 첫 담당 노드로 등록한 바깥 그래프를 만듭니다.
메서드 `add_node`에 함수 대신 컴파일한 그래프를 넘기면, 그 그래프가 노드 하나로 실행됩니다.
이렇게 다른 그래프의 노드로 들어간 그래프를 하위 그래프라고 부릅니다.
한 부서가 안에서 일을 나눠 해도, 회사 조직도에서는 칸 하나로 보이는 것과 같습니다.

### [41] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.646177Z', 'iopub.status.busy': '2026-09-28T06:55:46.646121Z', 'iopub.status.idle': '2026-09-28T06:55:46.648513Z', 'shell.execute_reply': '2026-09-28T06:55:46.648179Z'}}

```python
# 앞에서 만든 작은 그래프를 첫 담당 노드로 등록한 바깥 그래프를 만듭니다(작은 그래프는 하위 그래프가 됨)
outer_builder = StateGraph(TeamState)
outer_builder.add_node("loan_desk", tools_graph)
outer_builder.add_node("interlibrary_desk", interlibrary_note)
outer_builder.add_edge(START, "loan_desk")
outer_builder.add_edge("interlibrary_desk", END)
outer_graph = outer_builder.compile()
print("바깥 그래프의 노드:", list(outer_builder.nodes))
```

출력:
```
바깥 그래프의 노드: ['loan_desk', 'interlibrary_desk']

```

### [42] markdown {}

**결과 읽기** — 출력 줄 `바깥 그래프의 노드: ['loan_desk', 'interlibrary_desk']`가 보입니다.
노드 `loan_desk`의 속은 도구 실행 노드 하나를 가진 작은 그래프이고, 이 그래프가 하위 그래프입니다.

다음 셀은 둘째 도구를 요청하는 응답을 손으로 만들어, 사람 글 뒤에 붙여 넣습니다.
실행 전에 예상해 봅니다.
도구 메시지가 없으니 이번에도 오류가 날 것 같습니다.

### [43] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.649104Z', 'iopub.status.busy': '2026-09-28T06:55:46.649043Z', 'iopub.status.idle': '2026-09-28T06:55:46.652692Z', 'shell.execute_reply': '2026-09-28T06:55:46.652390Z'}}

```python
# 사람 글 뒤에 hand_off_parent 요청을 담은 응답을 손으로 붙여 바깥 그래프를 실행하고, 메시지 목록을 봅니다
parent_call = {"name": "hand_off_parent", "args": {}, "id": "hand_call_2", "type": "tool_call"}
parent_request = AIMessage(content="", tool_calls=[parent_call])
outer_input = {"messages": [HumanMessage(content=first_question), parent_request], "active_agent": ""}
outer_result = outer_graph.invoke(outer_input)
print("담당 칸:", outer_result["active_agent"])
print("메시지 목록:")
show_messages(outer_result["messages"])
```

출력:
```
담당 칸: interlibrary_desk
메시지 목록:
HumanMessage
AIMessage | 도구 호출 요청: ['hand_off_parent']
AIMessage | 도구 호출 요청: []

```

### [44] markdown {}

**결과 읽기** — 오류 없이 끝났고, 출력 줄 `담당 칸: interlibrary_desk`가 보입니다.
라벨 줄 아래 둘째 줄은 `AIMessage | 도구 호출 요청: ['hand_off_parent']`이고, 다음 줄이 받은 쪽의 응답입니다.
도구 요청에 답하는 도구 메시지가 목록에 없습니다.
설치판 `prebuilt/tool_node.py` 1559~1563행은 가는 그래프가 지금 그래프일 때만 짝을 검사합니다.

이 장면은 도구 요청이 든 응답을 바깥 그래프 입력에 손으로 넣어 둔 경우입니다.
이 기록을 모델에 보내면, 답이 없는 도구 요청이 든 목록을 보내게 됩니다.
공식 문서는 이 짝이 없으면 대화 기록이 망가진다고 적습니다.
이 기록으로 서비스 모델을 부르는 장면은 실행하지 않았습니다.
그래서 6절의 넘기기 도구는 도구 메시지를 직접 만들어 갱신에 함께 담습니다.

## 6. 모델이 넘기는 두 담당

이제 두 담당을 실제 모델로 만든 에이전트로 바꿉니다.
바깥 그래프 모양은 2절과 같고, 노드 자리에 에이전트 그래프가 들어갑니다.
넘길지는 대출 규정 담당의 모델이 넘기기 도구를 부를지로 정해집니다.
이 모양은 공식 문서의 여러 에이전트 하위 그래프 모양입니다.

### [45] markdown {}

API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다.

### [46] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.653305Z', 'iopub.status.busy': '2026-09-28T06:55:46.653245Z', 'iopub.status.idle': '2026-09-28T06:55:46.659571Z', 'shell.execute_reply': '2026-09-28T06:55:46.659221Z'}, 'lesson_role': 'setup'}

```python
# .env 파일에서 OpenAI API 키를 읽습니다(키 값은 출력하지 않습니다)
import os
from dotenv import find_dotenv, load_dotenv

env_path = find_dotenv(usecwd=True)
load_dotenv(env_path)
has_key = os.getenv("OPENAI_API_KEY") is not None
print("OPENAI_API_KEY 설정 여부:", has_key)
assert has_key, "프로젝트 폴더의 .env 파일에 OPENAI_API_KEY를 적어 주세요."
```

출력:
```
OPENAI_API_KEY 설정 여부: True

```

### [47] markdown {}

실습에 쓸 모델을 준비합니다.
temperature 값을 0으로 두어 매번 비슷한 답을 고르게 합니다.

### [48] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:46.660266Z', 'iopub.status.busy': '2026-09-28T06:55:46.660212Z', 'iopub.status.idle': '2026-09-28T06:55:47.646661Z', 'shell.execute_reply': '2026-09-28T06:55:47.646257Z'}}

```python
# 실습에 쓸 모델을 준비합니다
model = init_chat_model(
    "openai:gpt-5.4-mini",
    temperature=0,
    reasoning_effort="none",
)
print("모델 이름:", model.model_name)
print("temperature:", model.temperature)
```

출력:
```
모델 이름: gpt-5.4-mini
temperature: 0.0

```

### [49] markdown {}

**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 2026-09-28에 이 모델로 실행한 결과입니다.
temperature 값을 0으로 두어도, 실행마다 답 문장이 달라질 수 있습니다.
이 셀은 모델 객체만 만들고, 모델 요청은 아직 보내지 않습니다.
이 절의 두 에이전트는 이 모델 객체 하나를 함께 씁니다.

다음 셀은 받는 쪽인 상호대차 담당을 만듭니다.
01절의 대출 규정 담당처럼 도구 없이, 교재용 규정 글을 시스템 메시지 글에 넣습니다.
이 규정 글은 교재용으로 만든 글이고, 실제 도서관 규정이 아닙니다.
에이전트 이름은 2절 그래프의 노드 이름과 같게 `interlibrary_desk`로 붙입니다.

### [50] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:47.647430Z', 'iopub.status.busy': '2026-09-28T06:55:47.647361Z', 'iopub.status.idle': '2026-09-28T06:55:47.652521Z', 'shell.execute_reply': '2026-09-28T06:55:47.652261Z'}}

```python
# 교재용 상호대차 규정 글을 시스템 메시지 글에 넣어, 도구 없는 상호대차 담당 에이전트를 만듭니다
interlibrary_rules = "[교재용 상호대차 규정] 다른 도서관의 책은 자료실 창구에서 상호대차로 신청합니다."
interlibrary_rules = interlibrary_rules + " 신청한 책은 보통 3~5일 뒤에 도착합니다."
interlibrary_rules = interlibrary_rules + " 책이 도착하면 문자로 알리고, 7일 안에 찾아가야 합니다."
interlibrary_text = "도서관 자료실의 상호대차 담당입니다. 아래 교재용 규정만 근거로 두 문장의 한국어로 답하세요.\n"
interlibrary_text = interlibrary_text + interlibrary_rules
# 인자 name에 적은 이름은 이 에이전트가 쓴 응답의 칸 name에도 들어갑니다
interlibrary_agent = create_agent(model, tools=[], system_prompt=interlibrary_text, name="interlibrary_desk")
print("에이전트 이름:", interlibrary_agent.name)
```

출력:
```
에이전트 이름: interlibrary_desk

```

### [51] markdown {}

**결과 읽기** — 출력 줄 `에이전트 이름: interlibrary_desk`가 보입니다.
인자 `name`에 적은 이름은 이 에이전트가 쓴 응답의 칸 `name`에도 들어갑니다.
설치판 langchain 1.4.0 `agents/factory.py` 1455~1456행이 그 자리입니다.

다음 셀은 대출 규정 담당이 부를 넘기기 도구입니다.
넘기기 도구는 모델이 불러 담당을 넘기는 도구이고, 공식 문서의 모양을 따릅니다.

매개변수 `runtime`의 표시 `ToolRuntime`은 Ch 21 03절의 실행 객체 표시입니다.
Ch 21 03절은 대괄호에 실행 정보 형식을 적어 `ToolRuntime[MemberContext]`로 썼습니다.
이 절은 실행 정보를 쓰지 않아 대괄호 없이 적습니다.
그 절에서는 `runtime.context`만 읽었고, 이 절에서는 속성 둘을 새로 읽습니다.
속성 `state`는 도구를 부른 에이전트의 상태이고, `tool_call_id`는 이 도구 요청의 호출 ID입니다.

### [52] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:47.653273Z', 'iopub.status.busy': '2026-09-28T06:55:47.653217Z', 'iopub.status.idle': '2026-09-28T06:55:47.660642Z', 'shell.execute_reply': '2026-09-28T06:55:47.660230Z'}}

```python
# 대출 규정 담당이 부를 넘기기 도구입니다. 도구 메시지를 함께 담아, 바깥 그래프의 상호대차 담당으로 넘깁니다
@tool
def transfer_to_interlibrary(runtime: ToolRuntime):
    """다른 도서관의 책을 빌려 오는 상호대차 문의를 상호대차 담당에게 넘깁니다."""
    # 실행 객체의 state는 도구를 부른 에이전트의 상태이고, 마지막 메시지가 이 도구를 요청한 응답입니다
    last_message = runtime.state["messages"][-1]
    # tool_call_id는 이 도구 요청의 호출 ID라, 도구 메시지를 그 요청의 답으로 짝짓습니다
    transfer_message = ToolMessage(content="상호대차 담당에게 넘겼습니다.", tool_call_id=runtime.tool_call_id)
    update = {"active_agent": "interlibrary_desk", "messages": [last_message, transfer_message]}
    return Command(goto="interlibrary_desk", update=update, graph=Command.PARENT)
```

출력:
```

```

### [53] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
갱신에는 담당 칸 값과 메시지 둘이 들어갑니다.
메시지 둘은 이 도구를 요청한 응답과, 그 요청에 답하는 도구 메시지입니다.

넘기면서 하위 그래프를 떠날 때, 하위 그래프 안에서 더한 메시지는 바깥에 저절로 들어가지 않습니다.
이 동작은 노트북 밖에서 모델 없는 작은 그래프로 확인했고, 노트북에서는 실행하지 않았습니다.
그래서 도구 요청이 든 응답도 갱신에 직접 담습니다.

객체 `Command`는 이 과정에서 세 자리에 나왔습니다.
Ch 13 06절은 노드가 다음 노드를 고를 때 `goto`를 썼습니다.
Ch 24 01절은 멈춘 실행에 사람의 답을 넣을 때 `resume`을 썼습니다.
이 절의 `graph=Command.PARENT`는 하위 그래프 안에서 바깥 그래프의 노드로 갈 때 씁니다.

### [54] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:47.661445Z', 'iopub.status.busy': '2026-09-28T06:55:47.661384Z', 'iopub.status.idle': '2026-09-28T06:55:47.666203Z', 'shell.execute_reply': '2026-09-28T06:55:47.665366Z'}}

```python
# 01절 규정 글에, 상호대차 문의는 넘기라는 문장을 더한 시스템 메시지 글로 대출 규정 담당 에이전트를 만듭니다
loan_rules = "[교재용 대출·반납 규정] 일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다. 반납 예정일 전에 한 번, 7일 연장할 수 있습니다."
loan_rules = loan_rules + " 예약한 사람이 있는 책은 연장할 수 없습니다. 연체한 일수만큼 새 대출이 제한됩니다."
loan_text = "도서관 자료실의 대출 규정 담당입니다. 아래 교재용 규정만 근거로 두 문장의 한국어로 답하세요."
loan_text = loan_text + " 다른 도서관의 책을 빌려 오는 상호대차 문의는 직접 답하지 말고 transfer_to_interlibrary 도구로 넘기세요.\n"
loan_text = loan_text + loan_rules
loan_agent = create_agent(model, tools=[transfer_to_interlibrary], system_prompt=loan_text, name="loan_desk")
print("에이전트 이름:", loan_agent.name)
```

출력:
```
에이전트 이름: loan_desk

```

### [55] markdown {}

**결과 읽기** — 출력 줄 `에이전트 이름: loan_desk`가 보입니다.
규정 글은 01절 대출 규정 담당과 같은 네 문장입니다.
시스템 메시지 글에는 상호대차 문의를 직접 답하지 말고 넘기기 도구로 넘기라는 문장을 더했습니다.
받는 쪽인 상호대차 담당에게는 넘기기 도구를 주지 않았습니다.

다음 셀은 2절 그래프와 같은 호출로 바깥 그래프를 만듭니다.
노드 자리에 함수 대신 두 에이전트 그래프를 넘기므로, 두 담당이 하위 그래프가 됩니다.
시작점 뒤 조건 함수는 2절의 `pick_desk`를 그대로 씁니다.

### [56] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:47.667541Z', 'iopub.status.busy': '2026-09-28T06:55:47.667457Z', 'iopub.status.idle': '2026-09-28T06:55:47.670646Z', 'shell.execute_reply': '2026-09-28T06:55:47.670256Z'}}

```python
# 2절 그래프와 같은 호출로, 노드 자리에 두 에이전트 그래프를 넣은 바깥 그래프를 만듭니다
team_builder = StateGraph(TeamState)
team_builder.add_node("loan_desk", loan_agent, destinations=("interlibrary_desk", END))
team_builder.add_node("interlibrary_desk", interlibrary_agent)
team_builder.add_conditional_edges(START, pick_desk, ["loan_desk", "interlibrary_desk"])
team_builder.add_edge("interlibrary_desk", END)
team_graph = team_builder.compile(checkpointer=InMemorySaver())
team_structure = team_graph.get_graph().draw_mermaid()
print("2절 그래프와 구조 문자열이 같은가:", team_structure == structure_text)
```

출력:
```
2절 그래프와 구조 문자열이 같은가: True

```

### [57] markdown {}

**결과 읽기** — 출력 줄 `2절 그래프와 구조 문자열이 같은가: True`가 보입니다.
바깥에서 보면 노드 둘과 점선·실선의 자리가 2절 그래프와 같습니다.
달라진 것은 노드의 속이고, 코드 규칙 대신 모델이 넘길지를 고릅니다.

## 7. 두 차례 실행하고 요청 세기

응답을 쓴 담당을 보려고, 응답의 칸 `name`을 모으는 함수를 먼저 만듭니다.

### [58] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:47.671315Z', 'iopub.status.busy': '2026-09-28T06:55:47.671255Z', 'iopub.status.idle': '2026-09-28T06:55:47.673001Z', 'shell.execute_reply': '2026-09-28T06:55:47.672634Z'}}

```python
# 메시지 목록에서 응답(AIMessage)마다, 그 응답을 쓴 에이전트 이름(칸 name)을 모아 내놓습니다
def writer_names(messages):
    names = []
    for message in messages:
        if type(message).__name__ == "AIMessage":
            names.append(message.name)
    return names
```

출력:
```

```

### [59] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
응답이 아닌 메시지는 건너뛰고, 응답마다 이름 하나를 모읍니다.

다음 셀은 스레드 `team-1`에 3절의 첫 글을 넣어 실행합니다.
설정 딕셔너리에는 스레드 이름과 함께 Ch 20 03절의 실행 한도 10을 적습니다.
실행 전에 예상해 봅니다.
대출 규정 담당이 넘기면, 요청은 넘기기 도구 요청 하나와 받은 담당의 답 하나로 2번일 것입니다.

### [60] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:47.673676Z', 'iopub.status.busy': '2026-09-28T06:55:47.673613Z', 'iopub.status.idle': '2026-09-28T06:55:50.086289Z', 'shell.execute_reply': '2026-09-28T06:55:50.085278Z'}}

```python
# 스레드 team-1에 3절의 첫 글을 넣어 실행하고, 메시지 목록을 봅니다(넘기면 모델 요청 2번)
# 받은 담당도 넘기기 도구를 가지면 서로 넘기며 끝나지 않을 수 있어, 실행 한도 10을 함께 줍니다(Ch 20 03절)
team_config = {"configurable": {"thread_id": "team-1"}, "recursion_limit": 10}
team_input = {"messages": [HumanMessage(content=first_question)], "active_agent": ""}
team_first = team_graph.invoke(team_input, team_config)
team_messages = team_first["messages"]
print("담당 칸:", team_first["active_agent"])
print("메시지 목록:")
show_messages(team_messages)
```

출력:
```
담당 칸: interlibrary_desk
메시지 목록:
HumanMessage
AIMessage | 도구 호출 요청: ['transfer_to_interlibrary']
ToolMessage | 결과 상태: success | 내용: 상호대차 담당에게 넘겼습니다.
AIMessage | 도구 호출 요청: []

```

### [61] markdown {}

**결과 읽기** — 출력 줄 `담당 칸: interlibrary_desk`가 보입니다.
라벨 줄 아래 둘째 줄 `AIMessage | 도구 호출 요청: ['transfer_to_interlibrary']`는 대출 규정 담당의 응답입니다.
셋째 줄은 넘기기 도구가 만든 도구 메시지이고, 넷째 줄이 받은 담당의 응답입니다.
이번 실행에서 대출 규정 담당의 모델은 넘기기 도구를 불렀습니다.

넘길지는 모델이 정하는 값이라 실행마다 달라질 수 있습니다.
노트북 밖에서 같은 두 차례를 다섯 번 보냈을 때는 다섯 번 모두 첫 차례에 넘겼습니다.

다음 셀은 이번 차례에 더해진 메시지에서, 응답을 쓴 담당과 모델 요청 수를 셉니다.
입력은 사람 글 하나였으므로, 결과 목록에서 첫 줄 뒤가 이번 차례에 더해진 메시지입니다.

### [62] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:50.088026Z', 'iopub.status.busy': '2026-09-28T06:55:50.087858Z', 'iopub.status.idle': '2026-09-28T06:55:50.091690Z', 'shell.execute_reply': '2026-09-28T06:55:50.091029Z'}}

```python
# 이번 차례에 더해진 메시지에서 응답을 쓴 담당, 호출 ID 짝, 모델 요청 수를 봅니다
team_new = team_messages[1:]
print("응답을 쓴 담당:", writer_names(team_new))
request_id = team_messages[1].tool_calls[0]["id"]
print("도구 메시지가 그 요청의 답인가:", team_messages[2].tool_call_id == request_id)
first_usage = sum_usage(team_new)
print("모델 요청 수:", first_usage["requests"])
print("입력 토큰:", first_usage["input_tokens"], "| 출력 토큰:", first_usage["output_tokens"])
print("받은 담당의 답 글:", team_messages[-1].text)
```

출력:
```
응답을 쓴 담당: ['loan_desk', 'interlibrary_desk']
도구 메시지가 그 요청의 답인가: True
모델 요청 수: 2
입력 토큰: 471 | 출력 토큰: 80
받은 담당의 답 글: 네, 다른 도서관의 책도 자료실 창구에서 상호대차로 신청하실 수 있습니다.  
신청한 책은 보통 3~5일 뒤 도착하며, 도착하면 문자로 알려드리고 7일 안에 찾아가셔야 합니다.

```

### [63] markdown {}

**결과 읽기** — 출력 줄 `응답을 쓴 담당: ['loan_desk', 'interlibrary_desk']`가 보입니다.
출력 줄 `도구 메시지가 그 요청의 답인가: True`로, 도구 요청과 도구 메시지의 호출 ID가 짝지어졌습니다.
출력 줄 `모델 요청 수: 2`는 첫 담당의 넘기기 요청 하나와 받은 담당의 답 하나입니다.
넘긴 차례의 요청은 첫 담당 1 + 받은 담당 1입니다.

이번 실행에서는 출력 줄 `입력 토큰: 471 | 출력 토큰: 80`이었습니다.
받은 담당의 답 글은 상호대차 규정 글의 세 문장을 두 줄로 옮겨 쓴 글이었습니다.
토큰 수와 답 글은 실행마다 달라질 수 있습니다.

다음 셀은 같은 스레드에 3절의 둘째 글만 넣어 실행합니다.
실행 전에 예상해 봅니다.
2절 그래프처럼 저장된 담당 칸을 읽고 상호대차 담당에서 시작해, 요청은 1번일 것입니다.

### [64] code {'execution': {'iopub.execute_input': '2026-09-28T06:55:50.093044Z', 'iopub.status.busy': '2026-09-28T06:55:50.092917Z', 'iopub.status.idle': '2026-09-28T06:55:50.972790Z', 'shell.execute_reply': '2026-09-28T06:55:50.971790Z'}}

```python
# 같은 스레드에 3절의 둘째 글만 넣어 실행하고, 이번 차례에 더해진 메시지만 잘라 봅니다
second_input = {"messages": [HumanMessage(content=second_question)]}
team_second = team_graph.invoke(second_input, team_config)
second_new = team_second["messages"][len(team_messages):]
print("담당 칸:", team_second["active_agent"])
print("이번 차례에 더해진 메시지 수:", len(second_new))
print("응답을 쓴 담당:", writer_names(second_new))
second_usage = sum_usage(second_new)
print("모델 요청 수:", second_usage["requests"])
print("입력 토큰:", second_usage["input_tokens"], "| 출력 토큰:", second_usage["output_tokens"])
print("받은 담당의 답 글:", team_second["messages"][-1].text)
```

출력:
```
담당 칸: interlibrary_desk
이번 차례에 더해진 메시지 수: 2
응답을 쓴 담당: ['interlibrary_desk']
모델 요청 수: 1
입력 토큰: 259 | 출력 토큰: 45
받은 담당의 답 글: 신청한 책은 보통 3~5일 뒤에 도착합니다.  
책이 도착하면 문자로 알려드리며, 7일 안에 찾아가셔야 합니다.

```

### [65] markdown {}

**결과 읽기** — 출력 줄 `담당 칸: interlibrary_desk`와 `응답을 쓴 담당: ['interlibrary_desk']`가 보입니다.
출력 줄 `이번 차례에 더해진 메시지 수: 2`는 사람 글 하나와 받은 담당의 응답 하나입니다.
출력 줄 `모델 요청 수: 1`로, 대출 규정 담당은 이번 차례에 요청을 보내지 않았습니다.
다음 차례에는 받은 담당의 요청 1번만 나갑니다.

이번 실행에서는 출력 줄 `입력 토큰: 259 | 출력 토큰: 45`였습니다.
받은 담당의 답 글은 도착 날짜와 찾아가는 기한을 두 줄로 쓴 글이었고, 실행마다 달라질 수 있습니다.

## 정리

1. 노드가 `Command`로 다음 노드와 담당 칸을 함께 바꾸면, 다음 차례에 대화할 담당이 바뀝니다.
2. 같은 스레드의 다음 차례는 저장된 담당 칸을 읽고 받은 담당에서 시작했습니다. 새 스레드는 첫 담당에서 시작했습니다.
3. 도구로 넘길 때는 도구 메시지를 함께 담습니다. 요청은 넘긴 차례에 첫 담당 1 + 받은 담당 1, 다음 차례에 받은 담당 1입니다.

03절에서는 요청을 분류해, 고른 담당 여럿에게 함께 보내는 모양을 봅니다.

## 그림

### 02-1-코드가-넘기는-두-담당.mmd

```mermaid
flowchart TB
  %% classes
  s(["START 시작점<br>조건 함수 pick_desk가<br>담당 칸을 읽고 고름"])
  l["loan_desk<br>대출 규정 담당<br>Command로 넘기거나 답함"]:::flow
  i["interlibrary_desk<br>상호대차 담당"]:::flow
  e(["END 끝점"])
  m[("InMemorySaver<br>스레드마다 담당 칸 저장")]
  s -.->|담당 칸이 빈 글이면| l
  s -.->|담당 칸이 interlibrary_desk면| i
  l -.->|goto interlibrary_desk| i
  l -.->|goto END| e
  i --> e
  m ---|다음 차례에 읽음| s
```

시작점 뒤 조건 함수가 저장된 담당 칸을 읽어 첫 노드를 고르고, 첫 담당은 Command로 상호대차 담당에게 넘깁니다.

### 02-2-같은-스레드의-두-차례.mmd

```mermaid
flowchart TB
  %% classes
  subgraph D1[스레드 desk-1]
    direction LR
    subgraph A[첫 차례]
      direction TB
      a1["다른 도서관<br>책을 묻는 글"]:::tool
      a2["실행 흔적<br>loan_desk<br>interlibrary_desk<br>담당 칸 저장<br>interlibrary_desk"]:::measure
      a1 --> a2
    end
    subgraph B[둘째 차례]
      direction TB
      b1["며칠 뒤에<br>받는지 묻는 글"]:::tool
      b2["이번 차례에<br>지난 노드<br>interlibrary_desk<br>상호대차 담당이 답함"]:::measure
      b1 --> b2
    end
    A -->|저장된 담당 칸| B
  end
  subgraph D2[스레드 desk-2]
    direction TB
    c1["같은 둘째 글"]:::tool
    c2["실행 흔적<br>loan_desk<br>대출 규정 담당이 답함"]:::measure
    c1 --> c2
  end
  D1 ~~~ D2
```

같은 스레드의 둘째 차례는 상호대차 담당에서 바로 시작했고, 새 스레드에 넣은 같은 글은 첫 담당이 받았습니다.

### 02-3-이름-오타는-조용히-끝남.mmd

```mermaid
flowchart TB
  %% classes
  t["loan_desk_typo<br>goto interlibrary_dsk<br>담당 칸 interlibrary_desk"]:::flow
  i["interlibrary_desk<br>실행되지 않음"]
  w["경고 글 한 줄<br>없는 이름으로 쓴 값은 무시함<br>오류 없이 끝남"]:::measure
  r["실행 흔적 loan_desk<br>답 칸이 빈 글 True<br>담당 칸 interlibrary_desk"]:::measure
  t --> w
  w --> r
  t -.-|이름이 달라 가지 않음| i
```

넘길 노드 이름에서 글자 하나를 빠뜨리자, 오류 없이 첫 담당만 지나고 끝났고 담당 칸만 넘긴 것처럼 바뀌었습니다.

### 02-4-도구-메시지-짝-검사.mmd

```mermaid
flowchart TB
  %% classes
  h["손으로 만든 응답<br>도구 요청 하나<br>도구 메시지 없음"]:::tool
  subgraph A[지금 그래프로 가는 Command]
    direction TB
    a1["hand_off_plain<br>담당 칸만 갱신"]:::flow
    a2["받은 오류 ValueError<br>짝이 되는 도구 메시지가 없음"]:::measure
    a1 --> a2
  end
  subgraph B[graph=Command.PARENT]
    direction TB
    b1["hand_off_parent<br>바깥 그래프의<br>상호대차 담당으로"]:::flow
    b2["오류 없음<br>담당 칸 interlibrary_desk<br>HumanMessage<br>AIMessage 도구 요청<br>AIMessage 받은 쪽이<br>손으로 적은 답"]:::measure
    b1 --> b2
  end
  n["짝 검사는<br>지금 그래프로 갈 때만<br>소스 확인 tool_node.py"]
  h --> A
  h --> B
  A ~~~ n
  B ~~~ n
```

도구 메시지 없이 넘기자, 지금 그래프로 가는 쪽은 ValueError로 멈췄고 바깥 그래프로 가는 쪽은 답 없는 도구 요청을 남기고 넘어갔습니다.

### 02-5-모델이-넘긴-두-차례.mmd

```mermaid
%%{init: {"sequence": {"messageAlign": "left"}}}%%
sequenceDiagram
  participant G as 바깥 그래프<br>team_graph
  box Lavender
  participant L as 대출 규정 담당<br>loan_desk
  participant I as 상호대차 담당<br>interlibrary_desk
  end
  Note over G: 넘긴 실행 첫 차례<br>담당 칸 빈 글
  G->>L: 조건 함수가 첫 담당을 고름
  Note over L: 첫 차례 요청 1<br>넘기기 도구 요청
  L-->>G: Command.PARENT · 도구 메시지 함께
  Note over G: 도구 메시지가 그 요청의 답 True
  G->>I: goto interlibrary_desk
  Note over I: 첫 차례 요청 2<br>답
  Note over G: 둘째 차례<br>저장된 담당 칸 interlibrary_desk
  G->>I: 조건 함수가 받은 담당을 고름
  Note over I: 둘째 차례 요청 1<br>답
```

넘긴 실행에서 첫 차례는 첫 담당과 받은 담당이 한 번씩 요청했고, 둘째 차례는 받은 담당만 한 번 요청했습니다.

### 02-6-밧줄이-넘어간-예인선.prompt.md

# 02-6-밧줄이-넘어간-예인선 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 항구에서 짐을 실은 바지선은 스스로 가지 못하고, 예인선이 밧줄로 끌어 줍니다. 바지선이 어느 자리에 이르면 밧줄을 다음 예인선에 옮겨 겁니다. 그때부터 바지선을 끄는 배는 다음 예인선이고, 앞 예인선은 밧줄을 푼 채 옆에 떠 있습니다. … 밧줄이 걸린 배는 담당 칸 `active_agent`에 적힌 담당입니다.

구성 요소와 배치: 항구를 옆에서 봄 · 가운데 **짐 상자를 실은 넓은 바지선 하나**(= 문의한 사람과의 대화) · 바지선 앞에서 나온 **밧줄 한 줄이 오른쪽 예인선에 분명히 묶임**(= 담당 칸에 적힌 다음 차례의 담당) · 왼쪽에 **밧줄이 제 갑판에 감긴 채 바지선과 이어지지 않은 예인선 하나**(= 넘겨준 앞 담당). 비유 계열 **「항구의 예인선과 바지선」**(01절이 엶 — 01-6은 큰 화물선·작은 보트·부두 상자, 02는 바지선과 예인선 둘·밧줄로 소품을 바꿈). 금지 소품(쟁반·서랍·바구니·저울·울타리·발자국·공구판·승강 상자·세탁기·체스판·즉석사진·도미노·홈통·물방울·가마·전표·구슬·모래시계·회전 레일·도장·컨베이어) 없음. 사람·손·동물·글자·숫자·화살표·화면·시계·표지 없음.

시선 순서: 가운데 바지선 → 오른쪽 예인선에 걸린 밧줄 → 밧줄이 감긴 채 떨어져 있는 왼쪽 예인선.

검수 기준: 그림만 보고 「바지선을 끄는 밧줄이 오른쪽 예인선 하나에만 걸려 있고, 왼쪽 예인선은 밧줄이 이어지지 않았다」가 읽히는가. 바지선이 하나인가, 밧줄이 한 줄인가, 예인선이 둘인가. 글자·숫자·사람·손·화살표·물방울·홈통이 없는가.

## 프롬프트 (1차, 채택)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. A small harbor seen from the side, filling the frame. In the middle, one flat wooden barge loaded with a few wooden crates. One thick rope runs from the front of the barge and is clearly tied to the back of one tugboat on the right, which pulls the barge forward. On the left, a second tugboat floats beside the barge, its loose rope coiled on its own deck and not connected to the barge. Calm flat water with only a few simple wave lines. No people, no hands, no animals, no arrows, no screens, no clocks, no signs, no pipes, no water drops.
```

## 상태

- 2026-09-28 · `nano_banana_pro`(`jobs_wait` 응답 모델 이름 `nano_banana_2` — 01-6과 같은 표시) · 16:9 · 2k · `use_unlim: false` · count 1. 생성 전 잔액 **2359**(바로 앞 거래 06:14:29.026844Z는 01절 01-6 몫).
- **1차 job `a5f38f61-56f9-48aa-9045-e0e1c994bd54` 채택** — 거래 **2026-09-28T06:59:30.294738Z 「Nano Banana Pro −2」**(결과 파일 이름 `hf_20260928_065930_a5f38f61…`와 시각이 맞음). 이 절 몫은 거래 한 줄, **2크레딧**. 재생성 0회. 결과 원본 `7989148f1ff1d0c31c1de25f8c9c48df38b6d89f8a60f1c3e8639a8b8bf450c5`(2752 × 1536).
- **그림에서 확인한 것(그림 읽기·alt에 반영)**: 흰 바탕, 아래쪽 파란 바다(흰 물결선 여러 줄). 가운데 넓은 나무 바지선 **하나** — 나무 상자 **넷**(왼쪽 큰 상자 하나, 오른쪽 아래 둘·위 하나). 바지선 오른쪽 끝 기둥에서 나온 밧줄 **한 줄**이 가운데에 매듭 하나를 지나 오른쪽 **빨간 예인선** 뒤쪽에 걸림. 왼쪽 **파란 예인선**은 바지선 왼쪽 끝에 붙어 떠 있고, 갑판 앞쪽에 밧줄이 감겨 있어 바지선과 이어지지 않음. 두 예인선 모두 굴뚝·선실·타이어 두 개. 글자·숫자·사람·손·화살표·화면·시계·표지·물방울·홈통 없음.
- 검수: 「밧줄이 오른쪽 예인선 하나에만 걸림 · 왼쪽 예인선은 밧줄이 감긴 채 이어지지 않음」이 그림만으로 읽힘 → 채택. 파란 예인선이 바지선에 맞닿아 보이는 점과 밧줄 가운데 매듭은 관계 판독을 흐리지 않아 두었습니다(강사 확인 대상에 한 줄). 두 배의 색·상자 수는 그림 읽기에서 뜻을 두지 않는다고 밝힘.
- 저장: 기기 셸에서 결과 URL을 `curl`로 받아(`/tmp/ch26-02/illu/illu-1-orig.png`) `UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pillow`로 RGB·폭 1100px(LANCZOS)로 줄여 `figures/02-6-밧줄이-넘어간-예인선.png`(1100 × 614, `f6431cc15158d4b920fb23de4a46143cd29dfe2707f925d1d5b3e0918f155fcc`)로 저장했습니다.
- 결과 URL을 한 번 더 받아(`illu-1-again.png`, 원본과 해시 같음) 같은 폭으로 줄인 그림과 저장 PNG를 픽셀 대조했습니다(`ImageChops.difference` bbox `None`, 최대 차이 0). 저장 PNG와 같은 사본(`.cache/ch26-02-view/illu-1-1100.png`)을 직접 열어 개수를 세고 그림 읽기를 썼습니다.

