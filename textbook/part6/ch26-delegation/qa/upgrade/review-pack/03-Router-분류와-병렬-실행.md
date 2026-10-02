# 03-Router-분류와-병렬-실행

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 1h | 실습 1h | 코드 notebooks/03-Router-분류와-병렬-실행.ipynb | 새 용어 4 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>조건 함수가 내놓은 <code>Send</code> 목록으로 고른 분야의 노드만 실행하고, 답을 한 칸에 모을 수 있습니다.</li>
<li>체크포인트의 단계 번호로 두 분야 노드가 같은 단계에서 실행된 것을 설명할 수 있습니다.</li>
<li>모델이 분야를 고르는 라우터를 만들고, 모델 요청 수를 분류 1 + 고른 분야 수로 셀 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>도서관 창구에 「책을 연장하고 싶은데, 토요일에도 여나요?」라는 문의가 오면 두 담당의 답이 필요합니다. 대출 규정 담당과 시설 담당이 저마다 한 부분씩 알고 있기 때문입니다. <a href="01-Subagent-도구-위임.html">01절</a>의 서브에이전트는 중앙 에이전트가 담당에게 일을 맡기고 답을 받아 왔습니다. <a href="02-Handoff-상태-전환.html">02절</a>의 핸드오프는 다음 차례에 대화할 담당을 바꾸었지만, 한 차례에는 한 담당만 답했습니다.</p><p>이 절은 문의를 먼저 분류해, 고른 담당 여럿에게 이번 차례에 함께 보내고 답을 모읍니다. 절 제목의 Router는 이 일을 하는 라우터를 가리킵니다. 제목의 병렬 실행은 Ch 18 03절의 함께 보내기를 가리키고, 본문에서는 그 말로 씁니다. 여러 담당에게 보낸 답이 섞이지 않으려면, 어떻게 보내고 어떻게 모을지를 코드로 정해야 합니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href="../../part4/ch13-langgraph-basics/05-Send-동적-팬아웃.html">Ch 13 05절</a>에서는 조건 함수가 <code>Send</code> 목록을 내놓아, 목록 길이만큼 같은 노드를 실행했습니다. 여러 갈래가 같은 칸에 값을 내므로 그 칸에 이어 붙이기 규칙을 적었습니다. 결과가 모이는 차례는 우리가 정하지 않아, 자리 번호를 함께 보내 차례를 맞췄습니다. <a href="../ch23-persistence/01-체크포인터와-스레드.html">Ch 23 01절</a>에서는 체크포인트마다 단계 번호가 붙는 것을 보았습니다.</p><p><a href="../../part5/ch18-workflow-patterns/02-실패를-처리하는-라우팅.html">Ch 18 02절</a>의 라우팅은 모델이 쓴 종류를 보고, 코드가 준비한 갈래로 보냈습니다. <a href="../../part5/ch18-workflow-patterns/03-병렬-섹셔닝과-투표.html">03절</a>의 함께 보내기는 서로 기다릴 필요가 없는 요청 여럿을 함께 보냈습니다. 두 절 모두 OpenAI SDK로 모델을 불렀고, 함께 보내기는 표준 라이브러리 asyncio로 했습니다.</p><p><a href="../../part2/ch06-langchain-start/03-구조화-출력과-검증.html">Ch 6 03절</a>에서는 <code>with_structured_output</code>으로 양식 클래스 객체를 받았습니다. 인자 <code>include_raw=True</code>를 주면 모델 응답도 함께 받았습니다. <a href="../ch21-create-agent/02-구조화-출력-두-전략.html">Ch 21 02절</a>의 양식 클래스는 칸에 <code>Literal</code>을 적어 정해 둔 값만 받게 했습니다. <a href="01-Subagent-도구-위임.html">01절</a>은 도구 없는 전문 에이전트를 만들었고, <a href="02-Handoff-상태-전환.html">02절</a>은 상호대차 담당을 더했습니다. 함수 <code>sum_usage</code>는 01·02절처럼 도구 파일에서 가져옵니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>항구의 분류 부두 곁에 작은 짐배 여러 척이 대어 있습니다. 부두에서는 짐의 행선지를 보고, 필요한 배에만 짐을 싣습니다. 짐을 실은 배들은 한꺼번에 부두를 떠나, 나란히 건너편 모음 부두로 갑니다. 짐을 싣지 않은 배는 부두에 그대로 남습니다.</p><p>분류 부두가 분류 노드이고, 짐을 싣고 떠난 배가 고른 분야 노드, 모음 부두가 종합 노드입니다. 짐을 실은 배만 떠나듯, 분야 칸에 이름이 적힌 분야 노드만 실행됩니다. 싣는 짐이 하나도 없으면 아무 배도 떠나지 않고, 모음 부두에도 짐이 오지 않습니다.</p><p>비유와 다른 점이 있습니다. 짐배는 물길마다 걸리는 시간이 다르지만, 이 절은 걸린 시간을 재지 않았습니다. 이 절이 보인 것은 두 분야 노드가 같은 단계에서 실행되었다는 차례입니다. 또 모음 부두의 짐은 배를 보면 어디서 왔는지 알지만, 답 칸의 답은 분야 이름을 함께 담아야 누구의 답인지 압니다.</p>
{{img:03-5-분류-부두를-떠나는-짐배|흰 바탕 아래쪽에 파란 바다가 있는 항구 그림입니다. 왼쪽에 회색 돌 부두가 있고, 빈 나무배 둘이 부두 위쪽 끝과 아래쪽 옆에 하나씩 붙어 가는 줄로 기둥에 묶여 있습니다. 가운데에는 자루를 하나씩 실은 나무배 둘이 나란히 오른쪽 위를 향해 떠 있습니다. 오른쪽에는 아무것도 놓이지 않은 긴 나무 부두가 물속 기둥 위에 서 있습니다. 글자·숫자·사람·손·화살표는 없는 그림|자루를 실은 두 배만 돌 부두를 떠나 나란히 건너편 부두로 가고, 빈 배는 돌 부두에 남아 있습니다.}}
<p class="look"><b>그림 읽기</b> — 왼쪽 돌 부두에는 빈 나무배 둘이 줄로 기둥에 묶여 있고, 오른쪽 긴 부두는 비어 있습니다. 가운데의 자루를 하나씩 실은 나무배 둘은 부두를 떠나, 나란히 오른쪽을 향해 떠 있습니다. 돌 부두가 분류 노드, 자루를 실은 두 배가 고른 두 분야 노드, 오른쪽 부두가 종합 노드입니다. 빈 배를 묶은 줄은 부두에 남았다는 모습일 뿐, 02절 그림의 밧줄과 짝짓지 않습니다. 빈 배의 수와 자루의 무늬도 어떤 값과도 짝짓지 않습니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>라우터(router)</td><td>요청을 분류해, 맞는 전문 에이전트에게 보내는 쪽입니다. 고른 담당이 여럿이면 함께 보냅니다. Ch 18 02절의 라우팅을 하는 쪽이라는 뜻입니다. 안내 데스크 직원이 문의지를 읽고 분야별 창구 여러 곳에 한꺼번에 나눠 주는 것과 같습니다. 이 절에서는 분류 노드와, 그 뒤 조건 함수 <code>send_to_desks</code>가 내놓는 <code>Send</code> 목록입니다.</td></tr><tr><td>분류 노드</td><td>문의를 읽고 답할 분야의 이름 목록을 분야 칸에 적는 노드입니다. 안내 데스크 직원이 문의지에 창구 이름을 적는 일과 같습니다. 이 절에서는 노드 <code>classify</code>이고, 앞 절반은 글자 규칙 함수, 뒤 절반은 분류 모델을 부르는 함수입니다.</td></tr><tr><td>분야 노드</td><td>분야 하나를 맡아 답을 내는 노드입니다. 분야별 창구 하나와 같습니다. 이 절에서는 노드 셋 <code>loan_desk</code>·<code>interlibrary_desk</code>·<code>facility_desk</code>이고, 함수 하나를 함께 씁니다.</td></tr><tr><td>종합 노드</td><td>여러 분야 노드의 답을 한 글로 엮는 노드입니다. 창구마다 받은 답을 안내문 한 장에 옮겨 적는 일과 같습니다. 이 절에서는 <code>join_answers</code>이고, 모델을 부르지 않고 분야 이름 차례로 엮습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 노트북 3절 출력 <code>분야 칸: ['loan_desk', 'facility_desk']</code>가 분류 노드가 적은 값입니다. 체크포인트 목록의 <code>1 | ('loan_desk', 'facility_desk')</code>는 라우터가 두 분야 노드로 보낸 자리입니다.</p>
{{mermaid:03-1-분야마다-함께-보내는-라우터|위에서 아래로 읽는 흐름도입니다. 맨 위 회색 둥근 상자 START 시작점에서 실선이 파란 상자 classify 분류 노드로 갑니다. 이 상자에는 분야 칸에 이름 목록을 냄, 뒤에 조건 함수 send_to_desks라고 적혀 있습니다. 분류 노드에서 Send라고 적힌 점선 셋이 나란히 놓인 파란 상자 loan_desk 대출 규정 담당, interlibrary_desk 상호대차 담당, facility_desk 시설 담당으로 갑니다. 세 상자에서 실선이 모두 파란 상자 join_answers 종합 노드 분야 이름 차례로 엮음으로 모이고, 거기서 실선이 회색 둥근 상자 END 끝점으로 가는 그림|분류 노드 뒤 조건 함수가 분야 이름마다 Send를 내놓고, 고른 분야 노드의 답이 종합 노드에 모입니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 점선과 실선의 자리는 노트북 2절에서 출력한 구조 문자열의 화살표 여덟 줄과 같습니다. 파란 상자는 우리가 적은 노드이고, 회색 둥근 상자는 시작점과 끝점입니다. 조건 함수 send_to_desks는 노드가 아니어서 따로 상자를 두지 않고 분류 노드 상자 안에 적었습니다. 점선 셋은 갈 수 있는 곳이고, 실제로 가는 곳은 분야 칸에 적힌 이름이 정합니다.</p>
<h3>고른 분야 노드만 같은 단계에서 실행됩니다</h3><p>분류 노드가 분야 칸에 이름 둘을 적으면, 조건 함수 <code>send_to_desks</code>는 <code>Send</code> 둘을 내놓습니다. 객체 <code>Send</code> 하나마다 분야 노드가 한 번 실행되고, 두 실행은 같은 단계에 묶입니다. 고르지 않은 분야 노드는 등록만 되어 있고 실행되지 않습니다. 걸린 시간은 이번에 재지 않았으므로, 함께 실행해서 빨라졌는지는 적지 않습니다.</p>
<h3>답마다 분야 이름을 함께 담습니다</h3><p>여러 분야 노드가 같은 단계에 답 칸에 값을 내므로, 답 칸에는 이어 붙이기 규칙이 있어야 합니다. Ch 13 05절에서 본 대로 결과가 모이는 차례는 우리가 정하지 않습니다. 그래서 갈래별 상태에 분야 이름을 넣고, 분야 노드는 그 이름을 답과 함께 냅니다. 종합 노드는 모인 차례가 아니라 분야 이름 목록의 차례로 답을 엮습니다.</p>
<h3>서브에이전트·핸드오프와 무엇이 다른가</h3><p>01절의 서브에이전트는 중앙 에이전트가 도구로 담당을 불러 답을 받아 왔습니다. 02절의 핸드오프는 다음 차례에 대화할 담당을 바꾸었습니다. 라우터는 이번 차례에 여러 담당에게 함께 보내고 답을 모을 뿐, 다음 차례의 담당을 바꾸지 않습니다. 공식 문서도 라우터는 요청마다 따로 분류하고, 호출 사이에 기억이 없다고 적습니다.</p><p>Ch 18 02·03절도 코드가 준비한 갈래로 보냈다는 점은 이 절과 같습니다. 다만 그 두 절은 OpenAI SDK로 모델을 부르고, 코드가 갈래를 골라 asyncio로 함께 보냈습니다. 이 절은 LangGraph 그래프 안에서 <code>Send</code>로 고른 분야마다 노드를 실행하고, 이어 붙이기 규칙을 적은 칸으로 모읍니다. 02절의 <code>Command(goto=…)</code>는 노드 하나로 가고, <code>Send</code> 목록은 여러 노드로 갑니다. 공식 문서도 한 담당에게만 보낼 때는 <code>Command(goto=…)</code>를, 여러 담당에게는 <code>Send</code>를 씁니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2~4절은 모델을 부르지 않습니다. 2절은 분야 이름 셋과 글자 규칙 분류 노드, 조건 함수, 분야 노드, 종합 노드로 그래프를 만듭니다. 3절은 두 분야가 걸리는 문의를 넣고, 체크포인트의 단계 번호를 봅니다. 4절은 값 바꿔 보기로 걸리는 분야가 없는 문의를 넣습니다.</p><p>5~6절은 실제 OpenAI 모델 <code>gpt-5.4-mini</code>를 temperature 0으로 부릅니다. 분류 노드는 양식 클래스를 붙인 분류 모델을, 분야 노드는 도구 없는 전문 에이전트를 부릅니다. 모델 요청은 분류 1번에 고른 분야 수를 더한 수이고, 두 분야를 고르면 노트북 한 번에 3번입니다. 요금표로 어림한 예상 비용은 0.001달러 아래이고, 청구 금액이 아닙니다. 읽거나 쓰는 파일은 없습니다.</p>
{{notebook:03-Router-분류와-병렬-실행}}
<p class="look"><b>확인할 점</b> — 노트북 3절에서 <code>답 칸 줄 수: 2</code>와, 종합 칸에 상호대차 담당의 줄이 없는지 봅니다. 체크포인트 목록의 <code>1 | ('loan_desk', 'facility_desk')</code> 줄로 두 분야 노드가 같은 단계에서 실행된 것을 확인합니다. 4절에서는 오류 없이 <code>종합 칸이 빈 글인가: True</code>가 나오는지 봅니다.</p>
{{mermaid:03-2-같은-단계에서-실행된-두-분야|위에서 아래로 읽는 흐름도입니다. 맨 위 노란 상자 체크포인트 단계 0 다음 노드 classify에서 노란 상자 체크포인트 단계 1 다음 노드 loan_desk facility_desk로 화살표가 갑니다. 단계 1 상자에서 화살표 둘이 나란한 파란 상자 loan_desk 단계 2에서 실행과 facility_desk 단계 2에서 실행으로 갑니다. 그 오른쪽 회색 상자 interlibrary_desk Send 없음 실행되지 않음은 단계 1 상자와 화살표 없는 점선으로만 이어집니다. 두 파란 상자에서 화살표가 노란 상자 체크포인트 단계 2 다음 노드 join_answers로 모이고, 다시 노란 상자 체크포인트 단계 3 다음 노드 없음으로 이어지는 그림|단계 1이 끝난 뒤 다음 노드가 둘이었고, 두 분야 노드는 같은 단계 2에서 실행되었습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 노란 상자 넷은 노트북 3절에서 출력한 체크포인트의 단계 번호와 다음 노드이고, 출력과 달리 옛것부터 놓았습니다. 단계 -1 줄은 그림에서 뺐습니다. 가운데 파란 상자 둘은 같은 단계 2에서 실행된 분야 노드입니다. 오른쪽 회색 상자는 등록은 되어 있지만 분야 칸에 이름이 없어 실행되지 않은 노드입니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>앞 절반의 값은 모델을 부르지 않아 실행마다 같습니다. 글자 규칙이 두 분야를 고르자 <code>Send</code> 둘이 만들어져, 두 분야 노드만 실행되었습니다. 체크포인트 목록에서 단계 1 뒤에 실행할 노드가 둘이었고, 두 노드는 같은 단계 2에서 실행되었습니다. 종합 노드는 단계 3에서 한 번 실행되어, 두 답을 분야 이름 차례로 엮었습니다.</p>
{{mermaid:03-3-걸린-분야가-없는-문의|위에서 아래로 읽는 그림입니다. 왼쪽 초록 상자 3절 두 분야가 걸린 문의 연장과 운영이 든 글에서 노란 상자 분야 칸 loan_desk facility_desk 답 칸 줄 수 2 마지막 단계 3으로 화살표가 갑니다. 오른쪽 초록 상자 4절 걸린 분야가 없는 문의 우산을 두고 온 글에서 노란 상자 분야 칸 빈 목록 답 칸 줄 수 0 종합 칸이 빈 글 True 마지막 단계 1 오류 없음으로 화살표가 갑니다. 두 줄 아래 가운데 회색 상자에는 두 실행 모두 같은 그래프 router_graph, Send 수는 분야 칸의 이름 수라고 적힌 그림|걸리는 말이 없는 문의는 분야 칸이 빈 목록이라, 분야 노드와 종합 노드 없이 단계 1에서 조용히 끝났습니다.}}
<p class="look"><b>도식 읽기</b> — 왼쪽은 노트북 3절, 오른쪽은 4절의 값 바꿔 보기입니다. 초록 상자는 넣은 문의이고, 노란 상자는 두 절에서 출력으로 확인한 값입니다. 두 줄은 같은 그래프에 문의만 바꾼 나란한 결과라, 서로 화살표로 잇지 않았습니다. 맨 아래 회색 상자는 두 실행 모두에 해당하는 코드 쪽 사실입니다.</p>
<p>걸리는 분야가 없는 문의에서는 분야 칸이 빈 목록이었습니다. 객체 <code>Send</code>가 하나도 없어 분야 노드와 종합 노드가 실행되지 않았고, 오류 없이 단계 1에서 끝났습니다. 02절의 이름 오타에 이어 조용히 끝나는 두 번째 경우이고, 이번에는 경고 글도 없었습니다. 공식 문서도 라우터가 전문 에이전트를 하나도 부르지 않을 수 있다고 적습니다.</p><p>모델로 바꾼 그래프는 2절 그래프와 구조 문자열이 같았습니다. 아래 표는 6절 한 번 실행의 값과 교재 출력의 토큰 수입니다. 토큰 수는 다시 실행하면 달라질 수 있습니다.</p>
<table><thead><tr><th>값</th><th>교재 출력</th><th>다시 실행하면</th></tr></thead><tbody><tr><td>모델이 고른 분야</td><td><code>loan_desk</code> · <code>facility_desk</code></td><td>모델이 정해 달라질 수 있음</td></tr><tr><td>답 칸 줄 수</td><td>2</td><td>고른 분야 수와 같음</td></tr><tr><td>모델 요청 수</td><td>3</td><td>분류 1 + 고른 분야 수</td></tr><tr><td>입력 토큰(교재 출력)</td><td>468</td><td>달라질 수 있음</td></tr><tr><td>출력 토큰(교재 출력)</td><td>87</td><td>달라질 수 있음</td></tr></tbody></table>
<p>이번 실행에서 분류 모델은 글자 규칙과 같은 두 분야를 골랐습니다. 요청은 분류 1번과 두 전문 에이전트 1번씩으로 3번이었습니다. 라우터의 요청은 분류 1 + 고른 분야 수라, 한 분야만 고르면 2번, 셋을 고르면 4번이 됩니다. 흔들림 확인 다섯 번과 두 커널에서 모두 두 분야를 골랐습니다.</p>
{{mermaid:03-4-모델이-분야를-고른-실행|위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 3절과 같은 문의 글에서 파란 상자 classify_by_model with_structured_output include_raw=True로 화살표가 갑니다. 거기서 분류 요청이라는 화살표가 보라 상자 분류 모델 gpt-5.4-mini 요청 1로 갑니다. 보라 상자에서 고른 이름마다 Send라고 적힌 점선 둘이, 칸 두 분야를 고른 실행 안의 나란한 보라 상자 loan_desk 전문 에이전트 요청 1과 facility_desk 전문 에이전트 요청 1로 갑니다. 칸 오른쪽 회색 상자 interlibrary_desk 전문 에이전트 부르지 않음은 분류 모델 상자와 화살표 없는 점선으로만 이어집니다. 두 보라 상자에서 화살표가 노란 상자 모델 요청 수 3, 분류 1 + 고른 분야 수, 답 칸 줄 수와 고른 분야 수가 같음 True로 모이는 그림|두 분야를 고른 실행에서 요청은 분류 1번과 고른 두 전문 에이전트 1번씩, 모두 3번이었습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 보라 상자는 이 절에서 실제로 부른 모델 gpt-5.4-mini가 요청을 받은 자리입니다. 점선은 고른 이름이 분야 칸에 적히고 조건 함수가 Send를 만드는 두 걸음을 줄여 그린 것입니다. 두 보라 상자를 묶은 칸은 모델이 두 분야를 고른 실행이라는 뜻이고, 흔들림 확인 다섯 번과 두 커널에서 모두 그랬습니다. 노란 상자는 노트북 6절 출력이고, 회색 상자는 이번 실행에서 부르지 않은 전문 에이전트입니다.</p>
<p>새 커널로 두 번 실행해 견주자, 스물다섯 셀의 출력이 두 번 모두 같았습니다. 토큰 수와 답 글이 찍힌 6절의 셀 둘도 이번 두 번에서는 같았습니다. 그래도 노트북 밖 흔들림 확인에서는 출력 토큰과 답 글이 실행마다 조금씩 달랐으므로, 이 값은 결론에 쓰지 않습니다.</p>
<p class="look"><b>확인할 점</b> — 노트북 6절에서 <code>모델 요청 수</code> 줄을 <code>고른 분야 수</code> 줄과 견줍니다. <code>답 칸 줄 수와 고른 분야 수가 같은가: True</code>도 확인합니다. 고르는 분야는 모델이 정하므로, 다시 실행하면 달라질 수 있습니다. 교재 출력의 토큰 수와 답 글도 다시 실행하면 달라질 수 있어, 이 절의 결론에 쓰지 않았습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>고르는 분야는 분류 모델이 정합니다. 노트북 밖에서 6절 실행을 다섯 번 보내자, 다섯 번 모두 같은 두 분야를 골랐습니다. 그래도 같은 요청이 실행한 때에 따라 달라질 수 있습니다. 한 분야만 고르면 요청은 2번, 답 칸은 한 줄이 됩니다.</li><li>시설 규정 글은 이 절이 실행 전에 정한 교재용 한 문장이고, 운영 시각은 Ch 21 01절 규정 글에서 가져왔습니다. 대출·상호대차 규정 글은 01·02절 글과 같습니다. 흐름을 보여 주려고 정한 예이고, 실제 도서관 규정이 아닙니다.</li><li>걸린 시간은 재지 않았습니다. 설치판 langgraph 1.2.11 <code>pregel/_runner.py</code> 135~138행은 한 단계의 작업을 함께 실행한다고 적습니다. 이 절이 출력으로 본 것은 같은 단계라는 차례뿐이고, 걸린 초를 잰 주제는 Ch 18 03절입니다.</li><li>설치판 소스는 같은 단계의 갱신을 정해진 차례로 적용합니다. 이 절은 그 차례에 기대지 않으려고 답마다 분야 이름을 담았고, 그 차례는 노트북에서 확인하지 않았습니다.</li><li>같은 분야 이름이 분야 칸에 두 번 들어가면 <code>Send</code>도 둘이라, 그 분야 노드가 두 번 실행됩니다. 노트북 밖에서 모델 없는 작은 그래프로 확인했고, 노트북에서는 실행하지 않았습니다.</li><li>분류 결과를 읽지 못하면 키 <code>parsed</code>가 <code>None</code>이 되어 분류 노드가 멈춥니다. 이번 실행과 흔들림 확인 다섯 번에서 읽기 오류는 없었습니다. 실제 서비스에서는 이 경우와 빈 분류의 답을 코드로 정해 둡니다.</li><li>공식 문서의 라우터는 분류가 문의를 분야마다 나눠 보내고, 결과를 엮는 단계를 둡니다. 이 절은 문의 글 전체를 보냈고, 시스템 메시지 글로 자기 규정 부분에만 답하게 했습니다. 종합은 모델 없이 코드로 엮었고, 모델에 맡기면 요청이 1번 늘어납니다.</li><li>라우터는 요청마다 따로 분류해, 호출 사이에 기억이 없습니다. 공식 문서는 여러 차례 대화에 라우터를 도구로 감싸 대화 에이전트가 부르는 모양을 적습니다. 이 모양은 이 절에서 실행하지 않았습니다.</li><li>실행 한도 10은 01·02절과 같은 값입니다. 이 그래프는 되돌아가는 엣지가 없어 세 단계면 끝나고, 한도를 넘는 장면은 실행하지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>조건 함수가 분야 이름마다 <code>Send</code>를 내놓자, 고른 분야 노드만 같은 단계에서 실행되었습니다.</li><li>답마다 분야 이름을 함께 담아 모았고, 걸리는 분야가 없으면 종합 노드 없이 조용히 끝났습니다.</li><li>모델이 분야를 고르는 라우터의 요청은 분류 1 + 고른 분야 수였습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href="04-호출-수-비용-종료-조건-비교.html">04절</a>에서는 같은 과제를 세 구조로 실행해, 호출 수와 비용과 종료 조건을 견줍니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 두 분야가 걸린 문의에서 상호대차 담당 노드가 실행되지 않은 까닭은 무엇인가요?</p><p class="quiz-a">조건 함수는 분야 칸의 이름마다 <code>Send</code>를 만들었고, 분야 칸에 상호대차 담당 이름이 없었기 때문입니다. 등록한 노드라도 <code>Send</code>가 없으면 실행되지 않습니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">2. 두 분야 노드가 같은 단계에서 실행된 것은 무엇으로 확인했나요?</p><p class="quiz-a">체크포인트 목록에서 단계 1 줄의 다음 노드가 둘이었습니다. 두 노드는 단계 2에서 함께 실행되었고, 걸린 시간은 재지 않았습니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">3. 걸리는 분야가 없는 문의는 어떻게 끝났나요?</p><p class="quiz-a">오류 없이 분류 노드만 실행되고 단계 1에서 끝났습니다. 분야 노드와 종합 노드가 실행되지 않아 종합 칸은 빈 글이었습니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">4. 동료가 「라우터는 분야가 몇 개든 분류와 종합으로 요청이 늘 두 번」이라고 말합니다. 이 절의 셈으로는 어떻게 되나요?</p><p class="quiz-a">분류 1 + 고른 분야 수입니다. 분야 노드마다 전문 에이전트를 한 번 부르고, 이 절의 종합 노드는 코드라 요청이 없습니다. 두 분야를 고르면 3번입니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langchain/multi-agent/router">LangChain Router</a></div>확인 2026-09-28 · 분류 단계가 입력을 분류해 전문 에이전트에게 보내는 모양입니다. 전문 에이전트를 하나도 안 부르거나 여럿을 함께 부를 수 있고, 결과를 한 답으로 엮는다고 적습니다. 여러 담당에게는 <code>Send</code> 목록을, 한 담당에게는 <code>Command(goto=…)</code>를 씁니다. 요청마다 따로 분류해 호출 사이에 기억이 없다고도 적습니다.</li><li>langgraph 1.2.11 소스 <code>types.py</code> 704행부터가 <code>Send</code>의 정의입니다. 조건부 엣지에서 다음 단계의 노드를 따로 정한 상태로 부를 때 쓴다고 적습니다.</li><li>같은 판 <code>pregel/_runner.py</code> 135~138행은 한 단계의 작업을 함께 실행하는 자리입니다. <code>pregel/_algo.py</code> 253~256행은 같은 단계의 갱신을 적용하는 차례를 정하는 자리입니다.</li><li><a href="../../part4/ch13-langgraph-basics/05-Send-동적-팬아웃.html">Ch 13 05절</a>에서 <code>Send</code>와 팬아웃을, <a href="../../part5/ch18-workflow-patterns/02-실패를-처리하는-라우팅.html">Ch 18 02절</a>에서 라우팅을 보았습니다. <a href="../../part5/ch18-workflow-patterns/03-병렬-섹셔닝과-투표.html">Ch 18 03절</a>에서는 함께 보내기를 보았습니다.</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# Router 분류와 병렬 실행

**이 노트북에서 할 일**

1. 모델 없이, 조건 함수가 내놓은 `Send` 목록으로 고른 분야의 노드만 실행하고 답을 한 칸에 모읍니다.
2. 체크포인트의 단계 번호로 두 분야 노드가 같은 단계에서 실행된 것을 보고, 걸리는 분야가 없을 때를 봅니다.
3. 실제 모델이 분야를 고르는 라우터를 실행하고, 모델 요청 수를 고른 분야 수와 견줍니다.

**준비물** — 2~4절은 모델을 부르지 않아 API 키 없이 실행됩니다.
5~6절은 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 6절에서 그래프를 한 번 실행합니다.
모델 요청은 분류 1번에 고른 분야 수만큼 더해지고, 두 분야를 고르면 3번입니다.
요금표로 어림한 예상 비용은 0.001달러 아래이고, 청구 금액이 아닙니다.

모델이 고르는 분야와 답 글은 실행마다 달라질 수 있습니다.
걸린 시간은 재지 않았습니다.

읽거나 쓰는 파일은 없고, 체크포인트는 프로그램 메모리에만 둡니다.
앞 챕터에서 배운 함수 하나는 도구 파일 `delegation_tools.py`에서 가져옵니다.

**기준 버전** — 첫 셀에서 패키지 다섯을 설치합니다.
판은 langchain 1.4.0과 langchain-openai 1.6.0입니다.
langgraph 1.2.11과 pydantic 2.13.5, python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~3절과 5절을 읽습니다.
분야마다 노드를 두고 `Send`로 함께 보내는 모양과, 모델이 분야를 고르는 자리입니다.
4절은 걸리는 분야가 없는 문의로 바꿔 보는 자리이고, 6절은 모델을 부르는 실행입니다.
이 두 자리는 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch26-delegation`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 읽는 흐름도입니다. 맨 위 회색 둥근 상자 START 시작점에서 실선이 파란 상자 classify 분류 노드로 갑니다. 이 상자에는 분야 칸에 이름 목록을 냄, 뒤에 조건 함수 send_to_desks라고 적혀 있습니다. 분류 노드에서 Send라고 적힌 점선 셋이 나란히 놓인 파란 상자 loan_desk 대출 규정 담당, interlibrary_desk 상호대차 담당, facility_desk 시설 담당으로 갑니다. 세 상자에서 실선이 모두 파란 상자 join_answers 종합 노드 분야 이름 차례로 엮음으로 모이고, 거기서 실선이 회색 둥근 상자 END 끝점으로 가는 그림](attachment:03-1-분야마다-함께-보내는-라우터.png)

위에서 아래로 읽습니다.
점선과 실선의 자리는 노트북 2절에서 출력한 구조 문자열의 화살표 여덟 줄과 같습니다.
파란 상자는 우리가 적은 노드이고, 회색 둥근 상자는 시작점과 끝점입니다.
조건 함수 send_to_desks는 노드가 아니어서 따로 상자를 두지 않고 분류 노드 상자 안에 적었습니다.
점선 셋은 갈 수 있는 곳이고, 실제로 가는 곳은 분야 칸에 적힌 이름이 정합니다.

### [2] markdown {}

## 1. 준비

이 절에서는 문의를 분류해, 맞는 담당 여럿에게 한꺼번에 보내는 모양을 봅니다.
절 제목의 Router는 라우터를 가리키고, 뜻은 2절에서 풉니다.
제목의 병렬 실행은 Ch 18 03절의 함께 보내기를 가리키고, 본문에서는 그 말로 씁니다.

첫 셀은 패키지 다섯을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:35.342196Z', 'iopub.status.busy': '2026-09-28T07:31:35.342020Z', 'iopub.status.idle': '2026-09-28T07:31:36.012967Z', 'shell.execute_reply': '2026-09-28T07:31:36.012410Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "langchain==1.4.0" "langchain-openai==1.6.0" "langgraph==1.2.11" "pydantic==2.13.5" "python-dotenv==1.2.3"
from importlib.metadata import version

print("langchain:", version("langchain"))
print("langchain-openai:", version("langchain-openai"))
print("langgraph:", version("langgraph"))
print("pydantic:", version("pydantic"))
print("python-dotenv:", version("python-dotenv"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
langchain: 1.4.0
langchain-openai: 1.6.0
langgraph: 1.2.11
pydantic: 2.13.5
python-dotenv: 1.2.3

```

### [4] markdown {}

**결과 읽기** — 출력 줄 `langgraph: 1.2.11`과 `pydantic: 2.13.5`가 보입니다.
다섯 판 모두 실습 폴더 잠금과 같은 판입니다.
양식 클래스를 만드는 패키지 pydantic은 langchain과 함께 설치되고, 이 절이 직접 가져와 판을 적었습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
상태 형식과 그래프를 만드는 이름과 객체 `Send`는 Ch 13에서 썼습니다.
체크포인터 `InMemorySaver`는 Ch 23 01절에서 썼습니다.
양식 클래스를 적는 `BaseModel`·`Field`·`Literal`은 Ch 21 02절에서 썼습니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:36.014037Z', 'iopub.status.busy': '2026-09-28T07:31:36.013941Z', 'iopub.status.idle': '2026-09-28T07:31:36.620416Z', 'shell.execute_reply': '2026-09-28T07:31:36.620035Z'}, 'lesson_role': 'setup'}

```python
# 상태 형식(Ch 13 01·02절)·그래프와 Send(Ch 13 05절)·체크포인터(Ch 23 01절) 이름을 가져옵니다
import operator
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
# 양식 클래스(Ch 6 03절·Ch 21 02절)·에이전트(Ch 21 01절)·모델(Ch 6 01절)·메시지(Ch 13 04절) 이름을 가져옵니다
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import AnyMessage, HumanMessage
# 앞 챕터에서 배운 함수 하나는 도구 파일에서 가져옵니다
from delegation_tools import sum_usage

print("도구 파일에서 가져온 함수:", "sum_usage")
```

출력:
```
도구 파일에서 가져온 함수: sum_usage

```

### [6] markdown {}

**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: sum_usage`가 보입니다.
Ch 19 05절 함수 `sum_usage`는 목록 안 응답마다 요청 하나로 세고 토큰을 더합니다.

앞에서 배운 함수는 `delegation_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
교재 출력을 만든 실행 도구는 이 폴더를 따로 알려 주어, 다른 자리에서 시작해도 가져오기가 되었습니다.

## 2. 분야마다 노드를 두고 함께 보내기

01절의 서브에이전트는 중앙 에이전트가 담당에게 일을 맡기고 답을 받아 왔습니다.
02절의 핸드오프는 다음 차례에 대화할 담당 자체를 바꾸었습니다.
이 절은 문의를 먼저 분류하고, 고른 담당 여럿에게 이번 차례에 함께 보냅니다.

이렇게 요청을 분류해 맞는 전문 에이전트에게 보내는 쪽을 라우터(router)라고 부릅니다.
고른 담당이 여럿이면 함께 보냅니다.
Ch 18 02절의 라우팅(routing)을 하는 쪽이라는 뜻입니다.

안내 데스크 직원이 문의지를 읽고, 분야별 창구 여러 곳에 한꺼번에 나눠 주는 것과 같습니다.
이 절 코드에서는 분류 노드가 분야 칸에 이름을 적고, 조건 함수가 그 이름마다 `Send`를 만듭니다.
라우터는 이번 차례의 답을 모을 뿐, 다음 차례의 담당을 바꾸지 않습니다.

분야는 01·02절의 두 담당에 시설 담당 `facility_desk`를 더한 셋입니다.
2~4절은 모델을 부르지 않고, 분류도 글자 규칙이 맡습니다.
먼저 분야 이름 셋과, 앞 절반의 분야 노드가 낼 답 한 줄을 정합니다.

### [7] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:36.621125Z', 'iopub.status.busy': '2026-09-28T07:31:36.621052Z', 'iopub.status.idle': '2026-09-28T07:31:36.623235Z', 'shell.execute_reply': '2026-09-28T07:31:36.622845Z'}}

```python
# 분야 셋의 이름(노드 이름으로도 씀)과, 앞 절반의 분야 노드가 낼 교재용 답 한 줄을 정합니다
desk_names = ["loan_desk", "interlibrary_desk", "facility_desk"]
desk_notes = {}
desk_notes["loan_desk"] = "대출 규정 담당이 답합니다"
desk_notes["interlibrary_desk"] = "상호대차 담당이 답합니다"
desk_notes["facility_desk"] = "시설 담당이 답합니다"
print("분야 이름:", desk_names)
```

출력:
```
분야 이름: ['loan_desk', 'interlibrary_desk', 'facility_desk']

```

### [8] markdown {}

**결과 읽기** — 출력 줄 `분야 이름: ['loan_desk', 'interlibrary_desk', 'facility_desk']`가 보입니다.
이 이름은 그래프의 노드 이름으로도 씁니다.
답 한 줄은 누가 답했는지만 보여 주려고 정한 교재용 글입니다.

다음 셀은 상태 형식입니다.
분야 칸 `desks`에는 분류가 고른 분야 이름 목록을 적고, 답 칸 `answers`에는 분야마다 낸 답을 모읍니다.
여러 갈래가 같은 단계에 답 칸에 값을 내므로, Ch 13 05절처럼 이어 붙이기 규칙을 적습니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:36.623827Z', 'iopub.status.busy': '2026-09-28T07:31:36.623768Z', 'iopub.status.idle': '2026-09-28T07:31:36.625354Z', 'shell.execute_reply': '2026-09-28T07:31:36.625134Z'}}

```python
# 문의 칸·분야 칸·답 칸·종합 칸을 둔 상태 형식을 만듭니다(답 칸에만 Ch 13 02절 이어 붙이기 규칙)
class RouteState(TypedDict):
    question: str
    desks: list[str]
    answers: Annotated[list[dict], operator.add]
    summary: str
```

출력:
```

```

### [10] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
규칙을 적은 칸은 답 칸 하나이고, 문의 칸·분야 칸·종합 칸은 새 값이 오면 덮어씁니다.
종합 칸 `summary`에는 마지막 노드가 답을 한 글로 모아 적습니다.

다음 셀은 분류 노드입니다.
문의 글에 「연장」이 있으면 대출 규정 담당, 「다른 도서관」이 있으면 상호대차 담당을 고릅니다.
「운영」이 있으면 시설 담당을 고르고, 걸리는 말이 여럿이면 모두 고릅니다.

### [11] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:36.625882Z', 'iopub.status.busy': '2026-09-28T07:31:36.625822Z', 'iopub.status.idle': '2026-09-28T07:31:36.627361Z', 'shell.execute_reply': '2026-09-28T07:31:36.627108Z'}}

```python
# 앞 절반의 분류 노드입니다. 문의 글에 든 말로 분야를 고르고, 고른 이름 목록을 분야 칸에 냅니다
def classify_by_words(state):
    desks = []
    if "연장" in state["question"]:
        desks.append("loan_desk")
    if "다른 도서관" in state["question"]:
        desks.append("interlibrary_desk")
    if "운영" in state["question"]:
        desks.append("facility_desk")
    return {"desks": desks}
```

출력:
```

```

### [12] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
세 `if`가 따로 검사하므로, 고른 분야는 하나도 없을 수도, 셋일 수도 있습니다.
분류는 이 셀의 글자 규칙이 정하고, 5절에서는 모델이 정합니다.

다음 셀은 분류 노드 뒤에 둘 조건 함수입니다.
Ch 13 05절처럼 분야 칸의 이름마다 `Send` 하나를 만들어 목록으로 내놓습니다.
객체 `Send`의 둘째 자리 딕셔너리는 그 실행 하나만 읽는 갈래별 상태가 됩니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:36.628016Z', 'iopub.status.busy': '2026-09-28T07:31:36.627955Z', 'iopub.status.idle': '2026-09-28T07:31:36.629705Z', 'shell.execute_reply': '2026-09-28T07:31:36.629337Z'}}

```python
# 분류 노드 뒤에 둘 조건 함수입니다. 분야 칸의 이름마다 Send 하나를 만들어 목록으로 내놓습니다
def send_to_desks(state):
    sends = []
    for desk in state["desks"]:
        # Send의 첫 자리는 갈 노드 이름, 둘째 자리는 그 실행에만 넘길 갈래별 상태입니다(Ch 13 05절)
        branch = {"desk": desk, "question": state["question"]}
        sends.append(Send(desk, branch))
    return sends
```

출력:
```

```

### [14] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
갈래별 상태에는 분야 이름과 문의 글 둘을 담았습니다.
분야 이름을 함께 보내야, 노드가 낸 답에도 어느 분야의 답인지 적을 수 있습니다.

다음 셀은 앞 절반의 분야 노드입니다.
세 분야 노드가 이 함수 하나를 함께 쓰고, 갈래별 상태의 분야 이름으로 누구인지 가립니다.
답 칸에는 분야 이름과 답 한 줄을 한 딕셔너리로 함께 냅니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:36.630358Z', 'iopub.status.busy': '2026-09-28T07:31:36.630293Z', 'iopub.status.idle': '2026-09-28T07:31:36.632043Z', 'shell.execute_reply': '2026-09-28T07:31:36.631722Z'}}

```python
# 앞 절반의 분야 노드입니다. 갈래별 상태의 분야 이름을 읽어, 이름과 답 한 줄을 함께 답 칸에 냅니다
def desk_reply(state):
    answer = {"desk": state["desk"], "reply": desk_notes[state["desk"]]}
    return {"answers": [answer]}
```

출력:
```

```

### [16] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
Ch 13 05절에서 본 대로, 결과가 모이는 차례는 우리가 정하지 않습니다.
그래서 답마다 분야 이름을 함께 담아, 모인 차례와 관계없이 누구의 답인지 알게 합니다.

다음 셀은 답을 모으는 종합 노드입니다.
분야 이름 목록의 차례대로 답 칸에서 그 분야의 답을 찾아, 한 줄씩 이어 붙입니다.
모델을 부르지 않는 보통 함수입니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:36.632647Z', 'iopub.status.busy': '2026-09-28T07:31:36.632593Z', 'iopub.status.idle': '2026-09-28T07:31:36.634523Z', 'shell.execute_reply': '2026-09-28T07:31:36.634164Z'}}

```python
# 종합 노드입니다. 분야 이름 목록의 차례대로 답 칸에서 그 분야의 답을 찾아 한 줄씩 이어 붙입니다
def join_answers(state):
    summary = ""
    for desk in desk_names:
        for answer in state["answers"]:
            if answer["desk"] == desk:
                summary = summary + "[" + desk + "] " + answer["reply"] + "\n"
    return {"summary": summary}
```

출력:
```

```

### [18] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
종합 칸의 줄 차례는 답 칸에 모인 차례가 아니라, 이 함수가 도는 분야 이름 차례를 따릅니다.
Ch 13 05절이 자리 번호로 차례를 맞춘 것과 같은 생각입니다.

다음 셀은 노드 다섯과 엣지로 그래프를 만들고, 체크포인터를 붙여 컴파일합니다.
세 분야 노드는 `for` 한 번으로 등록하고, 저마다 종합 노드로 가는 고정 엣지를 둡니다.
조건부 엣지의 셋째 자리에는 조건 함수가 갈 수 있는 분야 이름 목록을 적습니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:36.635242Z', 'iopub.status.busy': '2026-09-28T07:31:36.635191Z', 'iopub.status.idle': '2026-09-28T07:31:36.638638Z', 'shell.execute_reply': '2026-09-28T07:31:36.638279Z'}}

```python
# 노드 다섯과 엣지로 그래프를 만들고, 체크포인터를 붙여 컴파일합니다(출력 없음)
router_builder = StateGraph(RouteState)
router_builder.add_node("classify", classify_by_words)
router_builder.add_node("join_answers", join_answers)
# 세 분야 노드는 함수 하나를 함께 쓰고, 저마다 종합 노드로 가는 고정 엣지를 둡니다
for desk in desk_names:
    router_builder.add_node(desk, desk_reply)
    router_builder.add_edge(desk, "join_answers")
router_builder.add_edge(START, "classify")
# 셋째 자리의 이름 목록은 조건 함수가 갈 수 있는 곳이라, 구조 문자열에 점선으로 그려집니다
router_builder.add_conditional_edges("classify", send_to_desks, desk_names)
router_builder.add_edge("join_answers", END)
router_graph = router_builder.compile(checkpointer=InMemorySaver())
```

출력:
```

```

### [20] markdown {}

**결과 읽기** — 설계 객체를 만들고 컴파일만 하는 셀이라 출력이 없습니다.
분야 노드 셋이 모두 종합 노드로 가는 엣지를 가졌습니다.
종합 노드가 몇 번 실행되는지는 3절에서 체크포인트로 봅니다.

다음 셀은 등록한 노드와 구조 문자열의 화살표 줄을 출력합니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:36.639227Z', 'iopub.status.busy': '2026-09-28T07:31:36.639174Z', 'iopub.status.idle': '2026-09-28T07:31:36.658523Z', 'shell.execute_reply': '2026-09-28T07:31:36.658167Z'}}

```python
# 등록한 노드와, 그래프가 스스로 그린 구조 문자열에서 화살표가 있는 줄을 출력합니다(02절과 같은 모양)
print("등록한 노드:", list(router_builder.nodes))
structure_text = router_graph.get_graph().draw_mermaid()
print("구조 문자열에서 화살표가 있는 줄:")
for line in structure_text.split("\n"):
    if "->" in line:
        print(line.strip())
```

출력:
```
등록한 노드: ['classify', 'join_answers', 'loan_desk', 'interlibrary_desk', 'facility_desk']
구조 문자열에서 화살표가 있는 줄:
__start__ --> classify;
classify -.-> facility_desk;
classify -.-> interlibrary_desk;
classify -.-> loan_desk;
facility_desk --> join_answers;
interlibrary_desk --> join_answers;
loan_desk --> join_answers;
join_answers --> __end__;

```

### [22] markdown {}

**결과 읽기** — 출력 줄 `등록한 노드: ['classify', 'join_answers', 'loan_desk', 'interlibrary_desk', 'facility_desk']`가 보입니다.
라벨 줄 아래 `classify -.-> loan_desk;`처럼 분류 노드에서 세 분야로 가는 줄은 점선입니다.
조건 함수가 고를 수 있는 곳이라 점선이고, `loan_desk --> join_answers;` 같은 고정 엣지는 실선입니다.
조건 함수 `send_to_desks`는 노드가 아니라 등록한 노드 목록에 없습니다.

## 3. 두 분야가 걸린 문의

첫 문의는 책 연장과 토요일 운영 시간을 함께 묻습니다.
실행 전에 예상해 봅니다.
글자 규칙이 대출 규정 담당과 시설 담당을 고르고, 두 분야 노드만 실행될 것입니다.

다음 셀은 스레드 `route-1`에 첫 문의를 넣어 실행합니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:36.659124Z', 'iopub.status.busy': '2026-09-28T07:31:36.659072Z', 'iopub.status.idle': '2026-09-28T07:31:36.666562Z', 'shell.execute_reply': '2026-09-28T07:31:36.666176Z'}}

```python
# 스레드 route-1에 두 분야가 걸리는 문의를 넣어 실행하고, 분야 칸·답 칸·종합 칸을 봅니다
first_question = "빌린 책을 연장하려면 어떻게 하나요? 토요일 운영 시간도 알려 주세요."
route_config = {"configurable": {"thread_id": "route-1"}}
first_input = {"question": first_question, "desks": [], "answers": [], "summary": ""}
first_result = router_graph.invoke(first_input, route_config)
print("분야 칸:", first_result["desks"])
print("답 칸 줄 수:", len(first_result["answers"]))
print("종합 칸:")
print(first_result["summary"])
```

출력:
```
분야 칸: ['loan_desk', 'facility_desk']
답 칸 줄 수: 2
종합 칸:
[loan_desk] 대출 규정 담당이 답합니다
[facility_desk] 시설 담당이 답합니다


```

### [24] markdown {}

**결과 읽기** — 출력 줄 `분야 칸: ['loan_desk', 'facility_desk']`와 `답 칸 줄 수: 2`가 보입니다.
고른 분야 수만큼 답이 모였습니다.
라벨 줄 아래 종합 칸은 `[loan_desk] 대출 규정 담당이 답합니다`와 `[facility_desk] 시설 담당이 답합니다` 두 줄입니다.
상호대차 담당의 줄이 없어, 고르지 않은 분야 노드는 실행되지 않았습니다.

다음 셀은 이 실행이 저장한 체크포인트를 Ch 23 01절 메서드 `get_state_history`로 읽습니다.
체크포인트마다 단계 번호와, 그다음 단계에서 실행할 노드를 출력합니다.
이 메서드는 최신 체크포인트부터 내놓으므로, 아래 줄부터 거꾸로 읽습니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:36.667394Z', 'iopub.status.busy': '2026-09-28T07:31:36.667333Z', 'iopub.status.idle': '2026-09-28T07:31:36.669637Z', 'shell.execute_reply': '2026-09-28T07:31:36.669260Z'}}

```python
# 저장된 체크포인트마다 단계 번호와 다음에 실행할 노드를 봅니다(Ch 23 01절 — 최신 체크포인트부터 나옴)
print("단계 번호 | 다음에 실행할 노드")
for snapshot in router_graph.get_state_history(route_config):
    # 칸 metadata의 step이 단계 번호이고, next는 그다음 단계에서 실행할 노드 이름입니다
    print(snapshot.metadata["step"], "|", snapshot.next)
```

출력:
```
단계 번호 | 다음에 실행할 노드
3 | ()
2 | ('join_answers',)
1 | ('loan_desk', 'facility_desk')
0 | ('classify',)
-1 | ('__start__',)

```

### [26] markdown {}

**결과 읽기** — 라벨 줄 아래 맨 아래 줄은 `-1 | ('__start__',)`이고, 위로 가며 단계가 늘어납니다.
줄 `1 | ('loan_desk', 'facility_desk')`는 단계 1이 끝난 뒤 다음에 실행할 노드가 둘이라는 뜻입니다.
두 분야 노드는 같은 단계 2에서 함께 실행되었습니다.
줄 `2 | ('join_answers',)`로 종합 노드는 단계 3에서 한 번 실행되었고, 맨 위 줄 `3 | ()`에서 끝났습니다.

같은 단계에서 실행되었다는 것은 차례에 관한 사실입니다.
두 노드를 함께 실행해 걸린 시간이 얼마나 줄었는지는 이번에 재지 않았습니다.

## 4. 걸리는 분야가 없으면

이번에는 값 하나만 바꿔 봅니다.
바꿀 값은 문의 글이고, 글자 규칙에 걸리는 말이 없는 글을 새 스레드 `route-2`에 넣습니다.
실행 전에 예상해 봅니다.
분야 칸이 빈 목록이면 `Send`도 없으니, 분야 노드와 종합 노드가 하나도 실행되지 않을 것입니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:36.670329Z', 'iopub.status.busy': '2026-09-28T07:31:36.670269Z', 'iopub.status.idle': '2026-09-28T07:31:36.673583Z', 'shell.execute_reply': '2026-09-28T07:31:36.673243Z'}}

```python
# 값 바꿔 보기: 글자 규칙에 걸리는 말이 없는 문의를 새 스레드 route-2에 넣어 실행합니다
empty_config = {"configurable": {"thread_id": "route-2"}}
empty_input = {"question": "자료실에 우산을 두고 온 것 같아요.", "desks": [], "answers": [], "summary": ""}
empty_result = router_graph.invoke(empty_input, empty_config)
print("분야 칸:", empty_result["desks"])
print("답 칸 줄 수:", len(empty_result["answers"]))
print("종합 칸이 빈 글인가:", empty_result["summary"] == "")
empty_state = router_graph.get_state(empty_config)
print("마지막 체크포인트의 단계 번호:", empty_state.metadata["step"], "| 다음에 실행할 노드:", empty_state.next)
```

출력:
```
분야 칸: []
답 칸 줄 수: 0
종합 칸이 빈 글인가: True
마지막 체크포인트의 단계 번호: 1 | 다음에 실행할 노드: ()

```

### [28] markdown {}

**결과 읽기** — 오류 없이 셀이 끝났고, 출력 줄 `분야 칸: []`과 `답 칸 줄 수: 0`이 보입니다.
출력 줄 `종합 칸이 빈 글인가: True`로, 종합 노드도 실행되지 않았습니다.
출력 줄 `마지막 체크포인트의 단계 번호: 1 | 다음에 실행할 노드: ()`는 단계 1 뒤에 남은 노드가 없다는 뜻입니다.
분류 노드만 실행되고, 그래프가 조용히 끝났습니다.

02절 4절에서는 `goto`에 없는 노드 이름을 적자 조용히 끝났습니다.
이 장면은 조용히 끝나는 두 번째 경우이고, 이번에는 경고 글도 없었습니다.
걸리는 분야가 없을 때의 답은 코드가 따로 정해야 하고, 지나간 노드를 출력해 보는 편이 안전합니다.

## 5. 모델이 분야를 고르는 라우터

이제 분류를 실제 모델에 맡기고, 분야 노드는 전문 에이전트를 부르게 바꿉니다.
그래프 모양은 2절과 같고, 분류 노드와 분야 노드의 속만 바뀝니다.
공식 문서의 라우터도 분류에 모델을 쓰고, 고른 분야마다 `Send`로 보냅니다.

### [29] markdown {}

API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다.

### [30] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:36.674147Z', 'iopub.status.busy': '2026-09-28T07:31:36.674096Z', 'iopub.status.idle': '2026-09-28T07:31:36.680244Z', 'shell.execute_reply': '2026-09-28T07:31:36.679888Z'}, 'lesson_role': 'setup'}

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

### [31] markdown {}

실습에 쓸 모델을 준비합니다.
temperature 값을 0으로 두어 매번 비슷한 답을 고르게 합니다.

### [32] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:36.680814Z', 'iopub.status.busy': '2026-09-28T07:31:36.680760Z', 'iopub.status.idle': '2026-09-28T07:31:37.653707Z', 'shell.execute_reply': '2026-09-28T07:31:37.653443Z'}}

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

### [33] markdown {}

**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 2026-09-28에 이 모델로 실행한 결과입니다.
temperature 값을 0으로 두어도, 실행마다 답 문장이 달라질 수 있습니다.
이 셀은 모델 객체만 만들고, 모델 요청은 아직 보내지 않습니다.
분류 모델과 전문 에이전트 셋이 이 모델 객체 하나를 함께 씁니다.

다음 셀은 세 담당의 규정 글을 정합니다.
대출 규정은 01절 글, 상호대차 규정은 02절 글 그대로입니다.
시설 규정은 이 절이 정한 교재용 한 문장이고, 운영 시각은 Ch 21 01절 규정 글과 같습니다.

### [34] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:37.654501Z', 'iopub.status.busy': '2026-09-28T07:31:37.654443Z', 'iopub.status.idle': '2026-09-28T07:31:37.656604Z', 'shell.execute_reply': '2026-09-28T07:31:37.656272Z'}}

```python
# 세 담당의 교재용 규정 글을 정합니다(대출은 01절, 상호대차는 02절 글 그대로이고, 시설은 이 절이 정한 한 문장)
loan_rules = "[교재용 대출·반납 규정] 일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다. 반납 예정일 전에 한 번, 7일 연장할 수 있습니다."
loan_rules = loan_rules + " 예약한 사람이 있는 책은 연장할 수 없습니다. 연체한 일수만큼 새 대출이 제한됩니다."
interlibrary_rules = "[교재용 상호대차 규정] 다른 도서관의 책은 자료실 창구에서 상호대차로 신청합니다."
interlibrary_rules = interlibrary_rules + " 신청한 책은 보통 3~5일 뒤에 도착합니다."
interlibrary_rules = interlibrary_rules + " 책이 도착하면 문자로 알리고, 7일 안에 찾아가야 합니다."
facility_rules = "[교재용 시설 규정] 자료실은 평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다."
print("시설 규정:", facility_rules)
```

출력:
```
시설 규정: [교재용 시설 규정] 자료실은 평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.

```

### [35] markdown {}

**결과 읽기** — 출력 줄 `시설 규정: [교재용 시설 규정] 자료실은 평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.`가 보입니다.
세 규정 글 모두 교재용으로 만든 글이고, 실제 도서관 규정이 아닙니다.

다음 셀은 이 규정 글로 도구 없는 전문 에이전트 셋을 만듭니다.
시스템 메시지 글에는 문의 가운데 자기 규정에 해당하는 부분에만 한 문장으로 답하라고 적습니다.
분야 노드가 분야 이름으로 에이전트를 찾도록, 딕셔너리에 분야 이름을 키로 담습니다.

### [36] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:37.657147Z', 'iopub.status.busy': '2026-09-28T07:31:37.657097Z', 'iopub.status.idle': '2026-09-28T07:31:37.661728Z', 'shell.execute_reply': '2026-09-28T07:31:37.661473Z'}}

```python
# 세 규정 글로 도구 없는 전문 에이전트 셋을 만들고, 분야 이름으로 찾을 수 있게 딕셔너리에 담습니다
answer_rule = " 문의 가운데 아래 교재용 규정에 해당하는 부분에만 한 문장의 한국어로 답하세요.\n"
loan_text = "도서관 자료실의 대출 규정 담당입니다." + answer_rule + loan_rules
interlibrary_text = "도서관 자료실의 상호대차 담당입니다." + answer_rule + interlibrary_rules
facility_text = "도서관 자료실의 시설 담당입니다." + answer_rule + facility_rules
desk_agents = {}
desk_agents["loan_desk"] = create_agent(model, tools=[], system_prompt=loan_text, name="loan_desk")
desk_agents["interlibrary_desk"] = create_agent(model, tools=[], system_prompt=interlibrary_text, name="interlibrary_desk")
desk_agents["facility_desk"] = create_agent(model, tools=[], system_prompt=facility_text, name="facility_desk")
print("전문 에이전트:", list(desk_agents))
```

출력:
```
전문 에이전트: ['loan_desk', 'interlibrary_desk', 'facility_desk']

```

### [37] markdown {}

**결과 읽기** — 출력 줄 `전문 에이전트: ['loan_desk', 'interlibrary_desk', 'facility_desk']`가 보입니다.
딕셔너리의 키는 2절 분야 이름과 같고, 에이전트 이름도 같은 글로 붙였습니다.
01절에서 본 것처럼 도구 없는 전문 에이전트는 한 번 부르면 모델 요청이 1번입니다.

다음 셀은 분류 모델이 채울 양식 클래스입니다.
클래스 `BaseModel`을 이어받은 클래스는 칸 이름과 칸에 들어갈 값의 형식을 적는 틀입니다.
주문서 양식에 칸마다 적을 것을 정해 두는 것과 같고, 뜻은 Ch 2 10절에 있습니다.
이 셀에서는 칸 `desks` 하나에, 분야 이름 셋 가운데에서 고른 이름의 목록만 받게 적습니다.
표시 `Literal`은 Ch 21 02절처럼 괄호 안 값 가운데 하나만 받고, `list[…]`로 감싸 그런 값의 목록을 받습니다.

### [38] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:37.662281Z', 'iopub.status.busy': '2026-09-28T07:31:37.662232Z', 'iopub.status.idle': '2026-09-28T07:31:37.664172Z', 'shell.execute_reply': '2026-09-28T07:31:37.663903Z'}}

```python
# 분류 모델이 채울 양식 클래스입니다. 칸 desks에는 분야 이름 셋 가운데에서 고른 이름의 목록이 들어갑니다
class DeskChoice(BaseModel):
    desks: list[Literal["loan_desk", "interlibrary_desk", "facility_desk"]] = Field(description="문의에 답할 담당 이름 목록")
```

출력:
```

```

### [39] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
빈 목록도 이 형식에 맞으므로, 모델은 분야를 하나도 고르지 않을 수 있습니다.
함수 `Field`의 설명 글은 Ch 6 03절에서 본 대로 칸의 뜻을 알려 줄 뿐, 규칙이 아닙니다.

다음 셀은 분류에 쓸 시스템 메시지 글을 정하고, 모델 객체에 양식 클래스를 붙입니다.
Ch 6 03절처럼 인자 `include_raw=True`를 주면 결과가 딕셔너리가 됩니다.
키 `raw`에는 모델 응답, `parsed`에는 양식 클래스 객체, `parsing_error`에는 읽기 오류가 담깁니다.
이 절은 모델 응답도 받아, 분류 요청까지 셉니다.

### [40] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:37.664683Z', 'iopub.status.busy': '2026-09-28T07:31:37.664629Z', 'iopub.status.idle': '2026-09-28T07:31:37.669580Z', 'shell.execute_reply': '2026-09-28T07:31:37.669167Z'}}

```python
# 분류에 쓸 시스템 메시지 글을 정하고, 모델 객체에 양식 클래스를 붙여 분류 모델을 만듭니다(요청은 아직 없음)
classify_text = "도서관 자료실 문의 창구의 안내 도우미입니다. 문의를 읽고 답할 담당을 모두 고르세요."
classify_text = classify_text + " loan_desk는 대출·반납·연장·연체, interlibrary_desk는 다른 도서관 책을 빌려 오는 상호대차를 맡습니다."
classify_text = classify_text + " facility_desk는 자료실 운영 시간과 시설을 맡습니다. 맡을 담당이 없으면 빈 목록을 내세요."
# include_raw=True를 주면 결과가 딕셔너리가 되고, 키 raw에 모델 응답이 함께 담깁니다(Ch 6 03절)
classifier = model.with_structured_output(DeskChoice, include_raw=True)
print("분류 모델의 종류:", type(classifier).__name__)
```

출력:
```
분류 모델의 종류: RunnableSequence

```

### [41] markdown {}

**결과 읽기** — 출력 줄 `분류 모델의 종류: RunnableSequence`가 보입니다.
Ch 6 03절처럼 이 셀은 호출 객체만 만들고, 모델 요청은 아직 보내지 않습니다.
시스템 메시지 글에는 세 분야가 맡는 일과, 맡을 담당이 없으면 빈 목록을 내라는 문장을 적었습니다.

다음 셀은 뒤 절반의 상태 형식입니다.
2절 상태 형식에 응답 칸 `responses`를 더해, 분류 모델과 전문 에이전트의 응답을 모읍니다.
칸 구성이 달라 이름을 새로 붙이고, 응답 칸에도 이어 붙이기 규칙을 적습니다.

### [42] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:37.670203Z', 'iopub.status.busy': '2026-09-28T07:31:37.670156Z', 'iopub.status.idle': '2026-09-28T07:31:37.672454Z', 'shell.execute_reply': '2026-09-28T07:31:37.672183Z'}}

```python
# 2절 상태 형식에 응답 칸을 더한 상태 형식을 만듭니다(응답 칸에도 이어 붙이기 규칙, 칸 구성이 달라 새 이름)
class ModelRouteState(TypedDict):
    question: str
    desks: list[str]
    answers: Annotated[list[dict], operator.add]
    summary: str
    responses: Annotated[list[AnyMessage], operator.add]
```

출력:
```

```

### [43] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
응답 칸의 응답 하나가 모델 요청 하나이므로, 6절에서 함수 `sum_usage`로 셉니다.
응답의 형식은 Ch 13 04절의 공통 형식 `AnyMessage`로 적었습니다.

다음 셀은 모델이 분야를 고르는 분류 노드입니다.
문의 글을 시스템 메시지 글과 함께 분류 모델에 보냅니다.
고른 분야 목록은 분야 칸에, 결과의 모델 응답은 응답 칸에 냅니다.

### [44] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:37.672931Z', 'iopub.status.busy': '2026-09-28T07:31:37.672886Z', 'iopub.status.idle': '2026-09-28T07:31:37.674571Z', 'shell.execute_reply': '2026-09-28T07:31:37.674209Z'}}

```python
# 뒤 절반의 분류 노드입니다. 분류 모델이 고른 이름 목록은 분야 칸에, 모델 응답은 응답 칸에 냅니다
def classify_by_model(state):
    messages = [("system", classify_text), ("user", state["question"])]
    result = classifier.invoke(messages)
    choice = result["parsed"]
    return {"desks": choice.desks, "responses": [result["raw"]]}
```

출력:
```

```

### [45] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
분야 칸의 값은 2절 글자 규칙과 같은 모양의 이름 목록이라, 조건 함수 `send_to_desks`를 그대로 씁니다.
읽기 오류가 나면 키 `parsed`가 `None`이 되어 이 노드가 멈추고, 이 절은 그 경우를 따로 받지 않았습니다.

다음 셀은 뒤 절반의 분야 노드입니다.
갈래별 상태의 분야 이름으로 전문 에이전트를 찾아 문의 글을 맡기고, 마지막 응답을 받습니다.
01절 도구 함수 안의 `invoke`처럼, 전문 에이전트는 문의 글 한 줄로 시작한 새 메시지 목록으로 일합니다.

### [46] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:37.675112Z', 'iopub.status.busy': '2026-09-28T07:31:37.675055Z', 'iopub.status.idle': '2026-09-28T07:31:37.676803Z', 'shell.execute_reply': '2026-09-28T07:31:37.676497Z'}}

```python
# 뒤 절반의 분야 노드입니다. 분야 이름으로 전문 에이전트를 찾아 문의를 맡기고, 이름과 답 글을 함께 냅니다
def ask_desk(state):
    agent = desk_agents[state["desk"]]
    result = agent.invoke({"messages": [HumanMessage(content=state["question"])]})
    reply = result["messages"][-1]
    answer = {"desk": state["desk"], "reply": reply.text}
    return {"answers": [answer], "responses": [reply]}
```

출력:
```

```

### [47] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
답 칸에는 2절처럼 분야 이름과 답 글을 함께 담고, 응답 칸에는 응답 객체를 냅니다.
세 분야 노드가 이 함수 하나를 함께 씁니다.

다음 셀은 2절과 같은 호출로 그래프를 만듭니다.
분류 노드 자리에 모델 분류 노드를, 분야 노드 자리에 전문 에이전트를 부르는 노드를 넣습니다.
조건 함수와 종합 노드는 2절 함수를 그대로 쓰고, 체크포인터는 붙이지 않습니다.

### [48] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:37.677386Z', 'iopub.status.busy': '2026-09-28T07:31:37.677334Z', 'iopub.status.idle': '2026-09-28T07:31:37.680736Z', 'shell.execute_reply': '2026-09-28T07:31:37.680427Z'}}

```python
# 2절과 같은 호출로, 분류 노드와 분야 노드 자리에 뒤 절반의 두 함수를 넣은 그래프를 만듭니다(출력 없음)
model_builder = StateGraph(ModelRouteState)
model_builder.add_node("classify", classify_by_model)
model_builder.add_node("join_answers", join_answers)
for desk in desk_names:
    model_builder.add_node(desk, ask_desk)
    model_builder.add_edge(desk, "join_answers")
model_builder.add_edge(START, "classify")
model_builder.add_conditional_edges("classify", send_to_desks, desk_names)
model_builder.add_edge("join_answers", END)
model_graph = model_builder.compile()
```

출력:
```

```

### [49] markdown {}

**결과 읽기** — 설계 객체를 만들고 컴파일만 하는 셀이라 출력이 없습니다.
분류 노드와 분야 노드의 함수만 바꾸고, 노드 이름과 엣지는 2절 그래프와 같게 적었습니다.
구조 문자열이 2절과 같은지는 다음 셀에서 함께 봅니다.

## 6. 실행하고 요청 세기

다음 셀은 3절의 첫 문의를 그대로 넣어 실행합니다.
설정 딕셔너리에는 01·02절처럼 실행 한도 10을 적습니다.
이 그래프는 되돌아가는 엣지가 없어 세 단계면 끝나지만, 모델이 도는 그래프에는 한도를 함께 줍니다.
실행 전에 예상해 봅니다.
모델이 대출 규정 담당과 시설 담당을 고르면, 요청은 분류 1번과 두 담당 2번으로 3번일 것입니다.

### [50] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:37.681308Z', 'iopub.status.busy': '2026-09-28T07:31:37.681250Z', 'iopub.status.idle': '2026-09-28T07:31:39.772527Z', 'shell.execute_reply': '2026-09-28T07:31:39.771239Z'}}

```python
# 3절의 첫 문의를 넣어 실행하고, 구조 문자열과 모델이 고른 분야·답 칸·종합 칸을 봅니다(분야 둘이면 요청 3번)
model_structure = model_graph.get_graph().draw_mermaid()
print("2절 그래프와 구조 문자열이 같은가:", model_structure == structure_text)
# 되돌아가는 엣지가 없어 세 단계면 끝나지만, 모델이 도는 그래프에는 실행 한도를 함께 줍니다(Ch 20 03절)
model_config = {"recursion_limit": 10}
model_input = {"question": first_question, "desks": [], "answers": [], "summary": "", "responses": []}
model_result = model_graph.invoke(model_input, model_config)
print("모델이 고른 분야:", model_result["desks"])
print("답 칸 줄 수:", len(model_result["answers"]))
print("종합 칸:")
print(model_result["summary"])
```

출력:
```
2절 그래프와 구조 문자열이 같은가: True
모델이 고른 분야: ['loan_desk', 'facility_desk']
답 칸 줄 수: 2
종합 칸:
[loan_desk] 일반 도서는 반납 예정일 전에 한 번만 7일 연장할 수 있으며, 예약한 사람이 있는 책은 연장할 수 없습니다.
[facility_desk] 자료실은 평일 09:00~20:00, 토요일 10:00~17:00에 운영합니다.


```

### [51] markdown {}

**결과 읽기** — 출력 줄 `2절 그래프와 구조 문자열이 같은가: True`가 보입니다.
출력 줄 `모델이 고른 분야: ['loan_desk', 'facility_desk']`와 `답 칸 줄 수: 2`가 보입니다.
이번 실행에서 분류 모델은 2절 글자 규칙과 같은 두 분야를 골랐습니다.
라벨 줄 아래 종합 칸의 두 줄은 `[loan_desk]`와 `[facility_desk]`로 시작합니다.

고른 분야는 모델이 정하는 값이라 실행마다 달라질 수 있습니다.
노트북 밖에서 같은 실행을 다섯 번 보냈을 때는 다섯 번 모두 이 두 분야를 골랐습니다.
이번 실행의 두 답 글은 연장 규정과 운영 시각을 한 문장씩 쓴 글이었고, 실행마다 달라질 수 있습니다.

다음 셀은 응답 칸의 응답으로 모델 요청 수를 세고, 고른 분야 수와 견줍니다.

### [52] code {'execution': {'iopub.execute_input': '2026-09-28T07:31:39.774717Z', 'iopub.status.busy': '2026-09-28T07:31:39.774551Z', 'iopub.status.idle': '2026-09-28T07:31:39.778596Z', 'shell.execute_reply': '2026-09-28T07:31:39.777931Z'}}

```python
# 응답 칸의 응답으로 모델 요청 수와 토큰을 세고, 고른 분야 수와 견줍니다
model_usage = sum_usage(model_result["responses"])
desk_count = len(model_result["desks"])
print("고른 분야 수:", desk_count)
print("응답 칸 줄 수:", len(model_result["responses"]))
print("모델 요청 수:", model_usage["requests"])
print("답 칸 줄 수와 고른 분야 수가 같은가:", len(model_result["answers"]) == desk_count)
print("입력 토큰:", model_usage["input_tokens"], "| 출력 토큰:", model_usage["output_tokens"])
```

출력:
```
고른 분야 수: 2
응답 칸 줄 수: 3
모델 요청 수: 3
답 칸 줄 수와 고른 분야 수가 같은가: True
입력 토큰: 468 | 출력 토큰: 87

```

### [53] markdown {}

**결과 읽기** — 출력 줄 `고른 분야 수: 2`와 `모델 요청 수: 3`이 보입니다.
요청 3번은 분류 모델 1번과, 고른 두 분야의 전문 에이전트 1번씩입니다.
라우터의 요청은 분류 1 + 고른 분야 수이고, 종합 노드는 코드라 요청을 더하지 않습니다.
출력 줄 `답 칸 줄 수와 고른 분야 수가 같은가: True`로, 고른 분야마다 답 한 줄이 모였습니다.

이번 실행에서는 출력 줄 `입력 토큰: 468 | 출력 토큰: 87`이었습니다.
토큰 수는 실행마다 달라질 수 있습니다.
종합을 모델에게 맡기면 요청이 1번 더 늘어나고, 이 절에서는 실행하지 않았습니다.

## 정리

1. 조건 함수가 분야 이름마다 `Send`를 내놓자, 고른 분야 노드만 같은 단계에서 실행되었습니다.
2. 답마다 분야 이름을 함께 담아 모았고, 걸리는 분야가 없으면 종합 노드 없이 조용히 끝났습니다.
3. 모델이 분야를 고르는 라우터의 요청은 분류 1 + 고른 분야 수였습니다.

04절에서는 같은 과제를 서브에이전트·핸드오프·라우터 세 구조로 실행해, 호출 수와 비용과 종료 조건을 견줍니다.

## 그림

### 03-1-분야마다-함께-보내는-라우터.mmd

```mermaid
flowchart TB
  %% classes
  s(["START 시작점"])
  c["classify 분류 노드<br>분야 칸에 이름 목록을 냄<br>뒤에 조건 함수 send_to_desks"]:::flow
  l["loan_desk<br>대출 규정 담당"]:::flow
  i["interlibrary_desk<br>상호대차 담당"]:::flow
  f["facility_desk<br>시설 담당"]:::flow
  j["join_answers 종합 노드<br>분야 이름 차례로 엮음"]:::flow
  e(["END 끝점"])
  s --> c
  c -.->|Send| l
  c -.->|Send| i
  c -.->|Send| f
  l --> j
  i --> j
  f --> j
  j --> e
```

분류 노드 뒤 조건 함수가 분야 이름마다 Send를 내놓고, 고른 분야 노드의 답이 종합 노드에 모입니다.

### 03-2-같은-단계에서-실행된-두-분야.mmd

```mermaid
flowchart TB
  %% classes
  c0["체크포인트 단계 0<br>다음 노드 classify"]:::measure
  c1["체크포인트 단계 1<br>다음 노드 loan_desk · facility_desk"]:::measure
  l["loan_desk<br>단계 2에서 실행"]:::flow
  f["facility_desk<br>단계 2에서 실행"]:::flow
  x["interlibrary_desk<br>Send 없음 · 실행되지 않음"]
  c2["체크포인트 단계 2<br>다음 노드 join_answers"]:::measure
  c3["체크포인트 단계 3<br>다음 노드 없음"]:::measure
  c0 --> c1
  c1 --> l
  c1 --> f
  c1 -.- x
  l --> c2
  f --> c2
  c2 --> c3
```

단계 1이 끝난 뒤 다음 노드가 둘이었고, 두 분야 노드는 같은 단계 2에서 실행되었습니다.

### 03-3-걸린-분야가-없는-문의.mmd

```mermaid
flowchart TB
  %% classes
  qa["3절 두 분야가 걸린 문의<br>연장과 운영이 든 글"]:::tool
  qb["4절 걸린 분야가 없는 문의<br>우산을 두고 온 글"]:::tool
  ra["분야 칸 loan_desk · facility_desk<br>답 칸 줄 수 2<br>마지막 단계 3"]:::measure
  rb["분야 칸 빈 목록<br>답 칸 줄 수 0<br>종합 칸이 빈 글 True<br>마지막 단계 1 · 오류 없음"]:::measure
  n["두 실행 모두 같은 그래프 router_graph<br>Send 수는 분야 칸의 이름 수"]
  qa --> ra
  qb --> rb
  ra ~~~ n
  rb ~~~ n
```

걸리는 말이 없는 문의는 분야 칸이 빈 목록이라, 분야 노드와 종합 노드 없이 단계 1에서 조용히 끝났습니다.

### 03-4-모델이-분야를-고른-실행.mmd

```mermaid
flowchart TB
  %% classes
  q["3절과 같은 문의 글"]:::tool
  c["classify_by_model<br>with_structured_output<br>include_raw=True"]:::flow
  m["분류 모델 gpt-5.4-mini<br>요청 1"]:::model
  x["interlibrary_desk<br>전문 에이전트 부르지 않음"]
  subgraph picked ["두 분야를 고른 실행"]
    direction LR
    l["loan_desk<br>전문 에이전트 요청 1"]:::model
    f["facility_desk<br>전문 에이전트 요청 1"]:::model
  end
  r["모델 요청 수 3<br>분류 1 + 고른 분야 수<br>답 칸 줄 수와 고른 분야 수가 같음 True"]:::measure
  q --> c
  c -->|분류 요청| m
  m -.->|고른 이름마다 Send| l
  m -.->|고른 이름마다 Send| f
  m -.- x
  l --> r
  f --> r
```

두 분야를 고른 실행에서 요청은 분류 1번과 고른 두 전문 에이전트 1번씩, 모두 3번이었습니다.

### 03-5-분류-부두를-떠나는-짐배.prompt.md

# 03-5-분류-부두를-떠나는-짐배 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 항구의 분류 부두 곁에 작은 짐배 여러 척이 대어 있습니다. 부두에서는 짐의 행선지를 보고, 필요한 배에만 짐을 싣습니다. 짐을 실은 배들은 한꺼번에 부두를 떠나, 나란히 건너편 모음 부두로 갑니다. 짐을 싣지 않은 배는 부두에 그대로 남습니다.

구성 요소와 배치: 항구를 조금 위에서 봄 · 왼쪽 **돌 부두**(= 분류 노드) · **같은 모양 작은 나무배** 가운데 **자루를 하나씩 실은 둘이 나란히 같은 쪽으로 떠남**(= 고른 두 분야 노드 — `Send` 둘) · **빈 배는 돌 부두에 남음**(= 고르지 않은 분야 노드) · 오른쪽 **비어 있는 긴 나무 부두**(= 종합 노드, 짐이 모일 자리). 비유 계열 **「항구의 예인선과 바지선」**(01-6 큰 화물선·작은 보트·부두 상자 셋, 02-6 넓은 바지선·예인선 둘·밧줄·매듭 — 소품을 바꿈: 돌 부두·나무배·자루·나무 부두). 물길은 나란히 같은 쪽(Ch 13 「세 갈래 길」처럼 갈라지지 않게). 금지 소품(쟁반·서랍·바구니·저울·울타리·발자국·공구판·승강 상자·세탁기·체스판·즉석사진·도미노·홈통·물방울·가마·전표·구슬·모래시계·회전 레일·도장·컨베이어) 없음. 사람·손·동물·글자·숫자·화살표·화면·시계·표지 없음.

시선 순서: 왼쪽 돌 부두 → 나란히 떠나는 자루 실은 배 둘 → 부두에 남은 빈 배 → 오른쪽 빈 나무 부두.

검수 기준: 그림만 보고 「자루를 실은 배만 부두를 떠나 같은 쪽으로 나란히 가고, 빈 배는 부두에 남았다」가 읽히는가. 배가 셋인가(자루 실은 둘 + 빈 하나), 밧줄·상자·큰 배·예인선·글자·숫자·사람·화살표가 없는가.

## 프롬프트 (1차 — 채택, 아래 상태 참고)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. A small harbor seen from slightly above. On the left, a short stone pier. Three identical small flat wooden cargo boats: two of them each carry one burlap sack and are leaving the stone pier together, side by side, moving in parallel in the same direction toward the right; the third boat is empty and stays at the stone pier. On the right, a long empty wooden pier waiting for the sacks. Calm water with only a few simple wave lines. No people, no hands, no animals, no arrows, no ropes, no crates, no big ships, no tugboats, no signs, no screens, no pipes, no water drops.
```

## 프롬프트 (2차 — 재생성, 탈락)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. A small harbor seen from slightly above. On the left, a short stone pier. Exactly three identical small wooden rowboats in total. Two boats each carry one plain burlap sack with no marks and are moving away from the stone pier together, side by side in parallel, both heading right, with short wake lines behind them. The third boat is empty and floats still right beside the stone pier. On the right, a long empty wooden pier waiting for the sacks. Calm water with only a few simple wave lines. No other boats, no people, no hands, no animals, no arrows, no ropes, no mooring posts, no crates, no signs, no screens, no pipes, no water drops.
```

## 상태

- 2026-09-28 · `nano_banana_pro`(`jobs_wait` 응답 모델 이름 `nano_banana_2` — 01-6·02-6과 같은 표시) · 16:9 · 2k · `use_unlim: false` · count 1. 생성 전 잔액 **2357**(바로 앞 거래 06:59:30.294738Z는 02절 02-6 몫).
- **1차 job `259573d7-645d-445e-939c-953721479054`** — 거래 **2026-09-28T07:34:42.898259Z 「Nano Banana Pro −2」**(결과 파일 이름 `hf_20260928_073442_259573d7…`). 원본 `6b3fe8ebe8527f36235dba2eca5327916bdf846c6d740c80af4c9acf856bb5c3`(2752 × 1536). 처음 검수에서는 **탈락으로 판정**: 배가 넷(빈 배 둘이 돌 부두 위쪽·아래쪽에 하나씩), 빈 배 둘이 가는 줄로 부두 기둥에 묶임(밧줄은 02-6 소품), 자루에 `#` 꼴 기운 자국 무늬.
- **2차 job `2cc1b543-1314-4ace-8b67-842adc0b069c`**(재생성 1회 — 한도) — 거래 **2026-09-28T07:36:00.330729Z 「Nano Banana Pro −2」**(`hf_20260928_073600_2cc1b543…`). 원본 `51ddf96ae0097e1269c034ece31cc03171f3db6a9ac5044fb90de6bf0e2a7a3c`(2752 × 1536, RGBA). **탈락**: 배가 다시 넷이고, 빈 배 하나가 부두가 아닌 물 가운데에서 자루 실은 배와 겹쳐 떠 있어 「짐을 실은 배만 떠난다」가 흐려짐. 자루의 `#` 꼴 무늬도 그대로.
- **채택: 1차**(두 장 가운데 관계가 더 분명한 쪽 — 짐을 실은 두 배만 물 위로 나와 나란히 같은 쪽을 향하고, 빈 배는 모두 돌 부두에 붙어 있음). 배 수(넷)는 그림 읽기에서 「빈 배의 수는 값과 짝짓지 않는다」로 밝히고, 본문 비유를 「짐배 여러 척」으로 씀. 묶는 줄·자루 무늬는 **강사 확인 대상**. 이 절 몫 크레딧은 거래 두 줄 **4크레딧**(재생성 1회).
- **그림에서 확인한 것(그림 읽기·alt에 반영)**: 위쪽 흰 바탕, 아래 파란 바다(흰 물결선 여러 줄). 왼쪽 회색 돌 부두 — 빈 나무배 **둘**이 부두 위쪽 끝과 아래쪽 옆에 하나씩 붙어 있고, 저마다 가는 줄로 회색 기둥에 묶임. 가운데 **자루를 하나씩 실은 나무배 둘**이 나란히 오른쪽 위를 향함(자루에 `#` 꼴 기운 자국). 오른쪽 **아무것도 놓이지 않은 긴 나무 부두**가 물속 기둥 위에 있음. 글자·숫자·사람·손·화살표·화면·시계·표지·물방울·홈통·상자·큰 배·예인선 없음.
- 저장: 기기 셸에서 결과 URL을 `curl`로 받아(`/tmp/ch26-03/illu/illu-1-orig.png`) `UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pillow`로 RGB·폭 1100px(LANCZOS)로 줄여 `figures/03-5-분류-부두를-떠나는-짐배.png`(1100 × 614, `2108359e7211419471bc1c9cd39c6b63ee3c921753166468a2be8c495225d366`)로 저장했습니다.
- 결과 URL을 한 번 더 받아(`illu-1-again.png`, 원본과 해시 같음) 같은 폭으로 줄인 그림과 저장 PNG를 픽셀 대조했습니다(`ImageChops.difference` bbox `None`, 최대 차이 0). 저장 PNG와 같은 사본(`.cache/ch26-03-view/illu-1-1100.png`)을 직접 열어 개수를 세고 그림 읽기를 썼습니다.

