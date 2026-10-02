# 05-ToolNode-실습

## _src 본문 (HTML 원본)

```html
<!--meta: 실습 30분 | 코드 notebooks/05-ToolNode-실습.ipynb | 새 용어 0 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>01절 그래프에 02절 오류 처리 함수와 03절 설정 딕셔너리를 붙여, 자료실 문의 하나를 처리할 수 있습니다.</li>
<li>붙여 둔 오류 처리 함수가 이번 흐름에서 쓰였는지, 도구 메시지의 결과 상태로 확인할 수 있습니다.</li>
<li>실행 흔적과 도구 메시지 수로 노드 실행 수를 세고, 실행 한도와 견줄 수 있습니다.</li>
<li>실행 한도 하나만 노드 실행 수와 같게 줄여 다시 실행하고, 두 실행의 결과를 견줄 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>이 챕터에서는 그래프 부품을 절마다 따로 익혔습니다. <a href="01-ToolNode와-tools-condition.html">01절</a>은 모델 노드와 도구 실행 노드를 되돌아가는 엣지로 이었습니다. <a href="02-도구-오류와-ToolMessage.html">02절</a>은 도구가 낸 오류를 도구 메시지로 바꾸는 오류 처리 함수를 봤습니다. <a href="03-recursion-limit과-명시적-종료.html">03절</a>은 실행 한도와 명시적 종료를 봤습니다. 실제 창구에서는 이 부품들이 한 그래프 안에서 함께 일합니다.</p>
<p>이번 실습은 01절 그래프에 오류 처리 함수와 실행 한도를 붙여, 자료실 문의 하나를 처리합니다. 실행 한도 하나만 바꿔 한 번 더 실행하고, 두 실행을 견줍니다. 실행 1은 01절 대출 흐름과 같은 차례입니다. 새로 볼 것은 한도를 그 흐름의 노드 실행 수와 같게 줄인 실행 2입니다. 03절은 이 경계를 모델 없는 그래프에서만 실행했습니다.</p>
<p>오류 처리 함수는 붙여 두었지만, 이번 두 실행에서는 쓰이지 않았습니다. 실행 1에서는 도구 메시지의 결과 상태 <code>success</code>로 그 사실을 확인합니다.</p>
<p>이번 절은 이 챕터의 실습입니다. 01~04절에서 쓴 이름과 문법만 쓰고 따로 내는 과제는 없습니다. 강사와 함께 노트북 셀을 차례로 실행합니다.</p>
<p><strong>이 절의 질문</strong> — 모델이 도구를 부르는 그래프에서, 실행 한도를 노드 실행 수와 같게 두면 어떻게 될까요? 한도에 닿은 실행에서 우리는 무엇을 받지 못할까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>이번 실습은 아래 절에서 배운 이름을 그대로 씁니다. 함수는 도구 파일 <code>graph_tools.py</code>에서 가져오고, 도구와 노드와 오류 처리 함수는 노트북에 적습니다.</p>
<table><thead><tr><th>절</th><th>배운 것</th><th>실습에서 쓰는 곳</th></tr></thead><tbody><tr><td><a href="01-ToolNode와-tools-condition.html">01절</a></td><td>모델 노드·도구 실행 노드(<code>ToolNode</code>)·도구 조건 함수(<code>tools_condition</code>)·되돌아가는 엣지, 상태 형식 <code>AgentState</code>, 함수 <code>call_id_lists</code>·<code>run_row</code></td><td>그래프 조립, 구조 문자열, 실행 1의 기록 한 줄</td></tr><tr><td><a href="02-도구-오류와-ToolMessage.html">02절</a></td><td>오류 처리 인자(<code>handle_tool_errors</code>)·오류 처리 함수 <code>handle_policy_error</code>·받을 오류 표시</td><td>도구 실행 노드 <code>policy_node</code>, 오류 처리 함수를 그래프 없이 불러 보는 셀 · 흐름에서는 쓰이지 않음(결과 상태 <code>success</code>로 확인)</td></tr><tr><td><a href="03-recursion-limit과-명시적-종료.html">03절</a></td><td>설정 딕셔너리·실행 한도(<code>recursion_limit</code>)·단계·명시적 종료, 오류 <code>GraphRecursionError</code>, 노드 실행 수보다 하나 큰 한도부터 통과</td><td>실행 1·2의 설정, 실행 2의 오류 받기, 두 실행 견주기</td></tr><tr><td><a href="04-if-분기와-모델-선택-비교.html">04절</a></td><td>도구 파일에 더한 함수 <code>sum_usage</code>(<a href="../ch19-model-tools/05-bind_tools와-병렬-호출.html">Ch 19 05절</a>)·<code>estimate_cost</code>(<a href="../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html">Ch 6 06절</a>)와 요금 변수</td><td>실행 1의 요청 수와 예상 비용</td></tr><tr><td><a href="../ch19-model-tools/06-오류와-읽기-쓰기-분리.html">Ch 19 06절</a></td><td>함수 <code>show_messages</code>와 결과 상태</td><td>메시지 칸 출력</td></tr></tbody></table>
<p>세 절의 기능을 고른 까닭은, 이 챕터의 그래프 하나에 모두 붙일 수 있기 때문입니다. 오류 처리 함수는 도구 실행 노드를 만드는 줄에 붙습니다. 실행 한도는 메서드 <code>invoke</code>의 둘째 인자에 붙습니다. 그래프 모양은 01절과 같아, 두 실행에서 바뀌는 것은 한도 하나뿐입니다. 요청 수는 모델이 도구를 부른 수에 마지막 답 하나를 더한 수라, 실행 전에 범위로 어림할 수 있습니다.</p>
<p>오류 처리 함수는 붙여 두었지만, 이번 두 실행에서는 쓰이지 않았습니다. 문의에 든 대출이 딕셔너리에 있는 주제어라, 도구가 오류를 내지 않았기 때문입니다. 딕셔너리에 없는 주제를 묻는 문의는 노트북 밖에서 먼저 보내 봤습니다. 모델이 그 주제어를 도구에 넣지 않아, 실습 문의로 쓰지 않았습니다. 그 결과는 본문 7에 적었습니다.</p>
<p>04절 두 그래프 견주기는 04절 실험을 되풀이하게 되어 뺐습니다. 02절 Before의 기본값 도구 실행 노드와 03절 Before의 끝나는 엣지가 없는 그래프도 뺐습니다. 두 장면은 앞 절에서 결함으로 이미 봤고, 이번에는 제대로 조립한 그래프에 한도 하나만 바꿉니다. 01절의 인사 질문과 운영·연체 질문은 요청 수를 늘려 뺐습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절부터 이어 온 두 층 자료실에, 앞 절 소품을 승강 통로 하나에 모아 붙여 봅니다. 서고 옆 벽에는 02절의 빈 카드를 꽂아 둔 주머니가 있습니다. 쪽지에 적힌 책이 서고에 없으면, 서고는 책 대신 이 주머니의 빈 카드를 상자에 싣습니다. 통로 옆 벽에는 03절 계수기 판이 있어, 상자가 한 층을 들를 때마다 등이 하나씩 켜집니다. 창구 층에는 03절 받침이 있어, 찾을 쪽지가 남지 않으면 상자가 거기에 섭니다.</p>
{{img:05-4-받침에-선-상자와-빈-카드-주머니|흰 바탕 그림으로 두 층 자료실 벽을 잘라 보인 모습입니다. 가운데에 회색 승강 통로 하나가 아래층부터 위층까지 세로로 나 있습니다. 위층 왼쪽에는 긴 나무 창구가, 아래층 왼쪽에는 파란 책이 꽂힌 책장이 있습니다. 통로 안 위층 높이의 나무 받침 위에 나무 상자 하나가 얹혀 있고, 상자 위로 흰 쪽지 한 장과 파란 책 한 권이 반쯤 나와 있습니다. 위층 통로 오른쪽 벽에는 둥근 등 여섯이 세로로 달린 판이 있고, 위의 셋은 꺼진 회색, 아래 셋은 노랗게 켜져 있습니다. 아래층 통로 오른쪽 벽에는 빈 회색 카드 여러 장이 꽂힌 나무 주머니가 있는 그림|상자는 계수기 등이 셋만 켜진 채 창구 층 받침에 섰고, 빈 카드 주머니는 쓰이지 않았습니다.}}
<p class="look"><b>그림 읽기</b> — 가운데 승강 통로는 하나이고, 위층 높이의 나무 받침 위에 상자 하나가 얹혀 있습니다. 상자에는 흰 쪽지 한 장과 파란 책 한 권이 반쯤 나와 있습니다. 통로 오른쪽 위층 벽의 판에는 둥근 등 여섯이 있고, 아래 셋만 노랗게 켜져 있습니다. 아래층 오른쪽 벽의 주머니에는 빈 회색 카드가 여러 장 꽂혀 있습니다.</p>
<p class="look">쪽지는 도구 호출 요청, 파란 책은 결과 상태 <code>success</code>인 도구 메시지입니다. 빈 카드 주머니는 오류 처리 함수, 계수기 판은 실행 한도, 받침은 명시적 종료입니다. 계수기 판은 한도 10을 등 여섯으로 줄여 그렸고, 켜진 등 셋만 실행 1이 지난 단계 셋입니다. 대출 쪽지라 책이 서고에 있어, 빈 카드는 쓰이지 않았습니다. 계수기 칸 수를 셋으로 줄인 실행 2에서는, 등 셋이 켜질 때 칸이 다 차서 상자가 받침에 얹히기 전에 멈춥니다.</p>
<h3>실습 조립의 구성</h3>
{{mermaid:05-1-오류-처리-함수와-한도를-붙인-그래프|위에서 아래로 읽는 그림으로 맨 위에 초록 상자 둘이 나란히 있습니다. 왼쪽은 첫 상태 대출 문의 하나, 오른쪽은 설정 딕셔너리 03절 recursion_limit 10입니다. 두 상자에서 invoke 첫째 인자와 둘째 인자 화살표가 아래 01절 그래프 모양 칸으로 갑니다. 칸 안에서 회색 가상 시작점 START가 보라 상자 모델 노드 model로 가고, 모델 노드에서 점선 두 갈래가 나갑니다. 요청 있음 이름표 tools 갈래는 회색 상자 도구 실행 노드 tools ToolNode로, 요청 없음 명시적 종료 갈래는 회색 가상 끝점 END로 갑니다. 도구 실행 노드에서 되돌아가는 엣지 실선이 모델 노드로 오고, 도구 실행 노드와 선으로 이은, 양옆에 세로줄이 한 줄씩 더 있는 파란 상자 오류 처리 함수 02절 handle_policy_error 이번 흐름에서 쓰이지 않음이 있는 그림|01절 그래프에 02절 오류 처리 함수와 03절 실행 한도를 붙였고, 오류 처리 함수는 이번 두 실행에서 쓰이지 않았습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 아래 칸에서 오류 처리 함수를 뺀 상자 넷과 화살표 넷은 노트북 5절 구조 문자열과 같습니다. 보라 상자는 모델에 요청을 보내는 모델 노드이고, 회색은 LangGraph가 준 것입니다. 오류 처리 함수는 노드가 아니라서 양옆에 세로줄이 더 있는 파란 상자로 그렸고, 이번 두 실행에서는 쓰이지 않았습니다. 맨 위 초록 상자 둘은 메서드 <code>invoke</code>에 넘기는 두 인자이고, 실행 2에서는 오른쪽 한도만 바꿉니다.</p>
<table><thead><tr><th>이름</th><th>하는 일</th><th>가져온 곳</th></tr></thead><tbody><tr><td><code>call_model</code>·<code>path_map</code>·<code>tools_condition</code></td><td>모델 노드, 이름표 표, 도구 조건 함수(그래프 모양)</td><td>01절 셀 그대로</td></tr><tr><td><code>policy_node</code></td><td>오류 처리 함수를 넘긴 도구 실행 노드</td><td>02절 7절 모양</td></tr><tr><td><code>limit_config</code>·<code>tight_config</code></td><td>실행 1·2의 설정 딕셔너리(한도 10·노드 실행 수)</td><td>03절 4절 모양</td></tr><tr><td><code>run_row()</code>·<code>show_messages()</code></td><td>실행 결과를 기록 한 줄로 만들기, 메시지 칸 출력</td><td>도구 파일(01절·Ch 19 06절)</td></tr><tr><td><code>sum_usage()</code>·<code>estimate_cost()</code></td><td>요청 수와 토큰 더하기, 예상 비용</td><td>도구 파일(Ch 19 05절·Ch 6 06절)</td></tr></tbody></table>
<h3>두 번의 실행</h3><p>실행 1은 03절과 같은 한도 10으로 실행합니다. 실행 2는 한도 하나만 실행 1에서 센 노드 실행 수와 같게 줄입니다. 첫 상태·그래프·모델 설정은 두 실행이 같습니다.</p><p>노드 실행 수는 실행 흔적 칸의 <code>model</code> 수에 도구 메시지 수를 더해 셉니다. 01절에서 본 것처럼 도구 실행 노드는 흔적 칸을 쓰지 않기 때문입니다. 한 응답에 요청을 하나까지만 받게 해, 도구 실행 노드가 한 번 실행될 때 도구 메시지가 하나 생깁니다.</p>
<h3>비교와 경계</h3><p>도구가 낸 <code>ValueError</code>는 오류 처리 함수가 받아 도구 메시지로 바꾸고, 흐름은 모델 노드로 이어집니다. 02절에서 본 장면입니다. 실행 한도에 닿아 난 <code>GraphRecursionError</code>는 도구가 낸 오류가 아닙니다. 오류 처리 함수는 이 오류를 받지 않고, 오류는 메서드 <code>invoke</code> 밖으로 올라옵니다. 그러면 그때까지 쌓인 메시지도 결과로 받지 못합니다.</p><p>이 오류 처리 함수의 받을 오류 표시는 <code>ValueError</code> 하나입니다. 02절 값 바꿔 보기의 인자 이름이 틀린 요청처럼, 입력 검사에서 걸린 오류는 받지 않아 흐름이 멈춥니다. 02절에서 본 장면이고, 이번에는 실행하지 않았습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 문의 글로 첫 상태를 만들고, 01~03절 셀로 자료·도구·모델·오류 처리 함수를 준비합니다. 오류 처리 함수는 그래프 없이 한 번 불러, 내놓는 글을 봅니다. 그다음 01절 그래프에 오류 처리 함수를 넘긴 도구 실행 노드를 넣어 조립합니다. 실행 1은 한도 10으로, 실행 2는 한도만 노드 실행 수와 같게 줄여 실행합니다. 마지막에 두 실행을 견주고, 실행 1의 요청 수와 예상 비용을 셉니다.</p><p>실제 OpenAI 모델을 부릅니다. 교재 출력은 2026-09-24에 실행한 결과입니다. 모델은 <code>gpt-5.4-mini</code>이고 temperature 0과 추론 끔(<code>reasoning_effort="none"</code>)으로 부릅니다.</p><p>교재 출력에서 모델 요청은 실행 1이 2번이었습니다. 실행 2는 결과를 받지 못해 노트북에서는 셀 수 없고, 노트북 밖 다섯 번에서는 2번이었습니다. 그래서 모델 요청은 모두 4번으로 어림합니다.</p><p>요금표로 어림한 예상 비용은 0.01달러 아래이고, 청구 금액과는 다를 수 있습니다. 새로 쓰는 파일은 없습니다.</p>
{{notebook:05-ToolNode-실습}}
<p class="look"><b>확인할 점</b> — 노트북 6절 출력 <code>실행 흔적 칸: ['model', 'model']</code>과 <code>노드 실행 수: 3</code>으로 실행 1의 흐름을 봅니다. 노트북 7절 출력 <code>받은 오류: GraphRecursionError</code>로 실행 2가 멈춘 것을 봅니다. 노트북 8절 출력 <code>실행 2 한도가 그 값보다 작은가: True</code>로 셈과 결과를 맞춰 봅니다. 답 글 문장과 출력 토큰은 여러분의 실행에서 교재 출력과 다를 수 있습니다.</p>
<h3>실행 1의 실제 순서</h3>
{{mermaid:05-2-실행-1이-지난-단계-셋|세로선 셋이 있는 차례 그림으로 왼쪽부터 노트북 코드 graph.invoke, 연보라 띠 안의 모델 노드 model gpt-5.4-mini, 도구 실행 노드 policy_node입니다. 노트북 코드가 모델 노드에 첫 상태 한도 10을 보내고, 노란 메모 단계 1 요청 1 lookup_policy 인자 대출이 붙습니다. 모델 노드에서 도구 실행 노드로 tools_condition tools 화살표가 가고, 노란 메모 단계 2 도구 메시지 success 오류 처리 함수 쓰이지 않음이 붙습니다. 도구 실행 노드에서 모델 노드로 되돌아가는 엣지가 오고, 노란 메모 단계 3 요청 2 도구 호출 요청 0건 뒤에 모델 노드에서 노트북 코드로 tools_condition END 점선이 갑니다. 마지막 노란 메모에 명시적 종료 한도 10에 닿지 않음, 흔적 model 두 번 노드 실행 수 3, 호출 ID 짝 True가 적힌 그림|실행 1은 모델 노드, 도구 실행 노드, 모델 노드의 세 단계를 지나 한도 10에 닿기 전에 END로 끝났습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽고, 세로선은 왼쪽부터 노트북 코드, 모델 노드, 도구 실행 노드입니다. 연보라 띠는 실제로 부른 모델 <code>gpt-5.4-mini</code>가 있는 자리입니다. 노란 메모의 단계 번호는 노드를 실행한 차례이고, 세 번째 단계 뒤 도구 조건 함수가 END를 내놓았습니다. 노란 메모는 모두 노트북 6절 출력입니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>두 실행은 실행 한도 하나만 달랐습니다. 결과는 아래 표와 같았습니다.</p>
<table><thead><tr><th>실행</th><th>설정 딕셔너리</th><th>끝까지 갔는가</th><th>실행 흔적</th><th>도구 메시지</th><th>노드 실행 수</th><th>모델 요청 수</th></tr></thead><tbody><tr><td>실행 1</td><td><code>{'recursion_limit': 10}</code></td><td>예, <code>END</code>로 끝남</td><td><code>['model', 'model']</code></td><td><code>success</code> 하나</td><td>3</td><td>2</td></tr><tr><td>실행 2</td><td><code>{'recursion_limit': 3}</code></td><td>아니요, <code>GraphRecursionError</code></td><td>받지 못함</td><td>받지 못함</td><td>셀 수 없음</td><td>노트북에서 셀 수 없음(밖에서 2)</td></tr></tbody></table>
{{mermaid:05-3-한도-하나만-바꾼-두-실행|맨 위 초록 상자 같은 첫 상태 대출 문의 같은 그래프 같은 모델 설정에서 아래 칸 둘로 화살표가 갑니다. 왼쪽 칸 실행 1 한도 10에는 노란 상자 흔적 model 두 번 노드 실행 수 3 도구 메시지 success 하나와, 노란 상자 마지막 응답 요청 0건 END로 끝나 결과를 받음이 위아래로 있습니다. 오른쪽 칸 실행 2 바꾼 값 한도 3에는 노란 상자 GraphRecursionError Recursion limit of 3, 노란 상자 invoke가 결과를 내놓지 않음 흔적 답 글 사용량 없음, 회색 상자 노트북 밖 다섯 번에서 센 값 모델 요청 두 번 뒤 멈춤이 위아래로 있습니다. 맨 아래 회색 상자에 셈 03절 규칙 노드 실행 수 3이면 한도 4부터 통과가 적힌 그림|한도만 노드 실행 수와 같은 3으로 줄인 실행 2는 GraphRecursionError로 멈춰, 실행 흔적도 답 글도 받지 못했습니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 초록 상자는 두 칸에 똑같이 넣은 첫 상태입니다. 왼쪽 칸이 실행 1, 오른쪽 칸이 한도만 바꾼 실행 2이고, 칸 안 상자들은 화살표로 잇지 않았습니다. 노란 상자는 노트북 6·7절 출력이고, 실행 2에서 받아 출력한 오류도 노랑입니다. 회색 상자 둘은 노트북 밖에서 센 값과 03절 규칙으로 한 셈입니다.</p>
<p>실행 1은 모델 노드·도구 실행 노드·모델 노드를 지나, 도구 조건 함수의 <code>END</code>로 끝났습니다. 노드 실행 수는 3이고, 한도 10에 닿지 않았습니다. 모델은 딕셔너리에 있는 주제어 대출을 적었고, 도구 메시지의 결과 상태는 <code>success</code>였습니다. 도구 오류가 없어 오류 처리 함수는 쓰이지 않았습니다.</p>
<p>실행 2는 한도를 3으로만 바꿨고, <code>GraphRecursionError</code>로 멈췄습니다. 메서드 <code>invoke</code>가 결과를 내놓지 않아, 실행 흔적·답 글·사용량을 하나도 받지 못했습니다. 노트북 밖 다섯 번에서는 실행 2도 모델 노드를 두 번 지났고, 둘째 요청은 답까지 만든 뒤 멈췄습니다. 요청은 나갔지만 답은 받지 못한 셈입니다.</p>
<p>03절 6절에서 모델 없는 그래프는 노드를 세 번 실행하면 한도 3에서 멈추고 한도 4에서 통과했습니다. 이번 모델 흐름도 노드 실행 수 3과 같은 한도에서 멈춰, 03절 경계의 멈추는 쪽과 같았습니다. 한도 4로는 이번에 실행하지 않았습니다.</p>
<p>모델 흐름의 노드 실행 수는 모델이 도구를 몇 번 부르느냐에 달려 있습니다. 실행 2처럼 노드 실행 수와 같은 한도로는 같은 흐름도 멈췄습니다. 통과하는 가장 작은 한도(노드 실행 수 + 1)에 맞춰도, 도구를 한 번 더 부르는 실행은 셈으로 한도에 닿습니다.</p>
<p>노트북 6~8절의 실행 흔적·도구 메시지·노드 실행 수·받은 오류는 새 커널 두 번에서 모두 같았습니다. 노트북 밖에서 같은 두 실행을 다섯 번 보냈을 때도 같았습니다. 두 번에서 달랐던 것은 답 글의 쉼표 하나와 출력 토큰, 그 토큰이 든 예상 비용이었고 결론에 쓰지 않았습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>문의 글은 01절 7절 대출 질문 그대로이고, 실행 전에 정했습니다. 실제 이용자가 보낸 글이 아닙니다.</li><li>노트북을 실행하기 전에 문의 후보를 차례로 정해 두고, 노트북 밖에서 후보마다 두 실행을 다섯 번씩 보냈습니다. 첫 후보는 02절 주차 질문 「자료실 주차 규정을 알려 주세요.」였습니다.</li><li>주차 질문의 첫 요청 열 번 가운데 여덟 번은 모델이 주제어 운영을 적었고, 두 번은 도구를 부르지 않았습니다. 실행 1의 다섯 번은 모두 오류 없이 운영 시간을 답해, 물음과 어긋난 답이 되었습니다.</li><li>둘째 후보 「주제어 주차로 자료실 규정을 찾아 주세요.」는 다섯 번 모두 도구를 부르지 않았습니다. 두 후보 모두 주차를 도구에 넣은 적이 없어, 오류 처리 함수가 쓰이는 장면이 나오지 않았습니다.</li><li>그래서 셋째 후보인 대출 문의를 실습 문의로 썼습니다. 흐름을 보여 주려고 정한 예이고, 후보와 차례는 첫 요청 전에 적어 두었습니다.</li><li>오류 처리 함수는 02절 판 그대로, 도구 몸통이 낸 <code>ValueError</code>만 받도록 좁힌 설계입니다. 딕셔너리에 없는 주제어가 도구에 들어올 때만 일하고, 입력 검사 오류까지 받는 방법은 이번에 실행하지 않았습니다. 모델이 비슷한 다른 주제어로 바꿔 찾으면 오류가 나지 않아, 이 함수로는 어긋난 답을 막지 못합니다.</li><li>대출 문의를 다섯 번씩 보냈을 때, 실행 1은 모두 흔적 <code>['model', 'model']</code>과 노드 실행 수 3이었습니다. 실행 2는 모두 <code>GraphRecursionError</code>였습니다. 같은 요청도 실행한 때에 따라 모델이 도구를 부를지가 달라질 수 있습니다.</li><li>실행 2의 한도는 실행 1에서 센 노드 실행 수를 그대로 쓴 값입니다. 실행 1에서 모델이 도구를 다른 수만큼 부르면, 실행 2의 한도도 함께 달라집니다.</li><li>실행 2의 모델 요청 수 2는 노트북 밖에서 모델 노드를 부른 횟수를 적어 센 값입니다. 노트북의 모델 노드는 01절 셀 그대로라 그 기록이 없습니다.</li><li>인자 <code>parallel_tool_calls=False</code>는 01절 그대로입니다. 한 응답에 요청 여럿을 받으면 도구 실행 노드 한 번에 도구 메시지가 여럿 생겨, 이 절의 노드 실행 수 셈이 맞지 않습니다. 이 조합은 이번에 실행하지 않았습니다.</li><li>모델이 정하는 값, 곧 도구 호출 요청과 답 글에는 <code>assert</code>를 걸지 않았습니다. 이 노트북의 <code>assert</code>는 키 확인 셀 하나뿐입니다.</li><li>이 절은 파일을 쓰지 않습니다. 걸린 시간은 재지 않았습니다.</li><li>예상 비용은 2026-09-17 요금표로 어림한 값이고 청구 금액이 아닙니다. 실행 2에서 나간 요청은 사용량을 받지 못해 예상 비용에 들어 있지 않습니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>01절 그래프에 02절 오류 처리 함수와 03절 설정 딕셔너리를 붙여, 대출 문의를 처리했습니다.</li><li>실행 1은 노드를 세 번 실행하고 <code>END</code>로 끝났고, 도구 오류가 없어 오류 처리 함수는 쓰이지 않았습니다.</li><li>한도만 3으로 줄인 실행 2는 <code>GraphRecursionError</code>로 멈춰, 실행 흔적도 답 글도 받지 못했습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 이 절로 Ch 20이 끝납니다. Ch 21 01절은 이 챕터에서 직접 이은 반복 구조를 함수 <code>create_agent</code> 한 줄로 얻는 법을 다룹니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. [하] 두 실행에서 바꾼 값은 무엇입니까?</p><p class="quiz-a">설정 딕셔너리의 실행 한도 하나입니다. 실행 1은 10, 실행 2는 실행 1의 노드 실행 수와 같은 3이었습니다. 첫 상태와 그래프와 모델 설정은 같게 두었습니다.</p><p class="quiz-q">2. [중] 실행 1의 노드 실행 수를 실행 흔적 칸의 길이만으로 세지 않은 까닭은 무엇입니까?</p><p class="quiz-a">도구 실행 노드는 흔적 칸을 쓰지 않아, 흔적 칸에는 모델 노드만 남기 때문입니다. 그래서 도구 메시지 수를 더해 3을 얻었습니다. 틀렸다면 노트북 6절과 01절을 다시 읽습니다.</p><p class="quiz-q">3. [중] 실행 2에서 우리가 받지 못한 것은 무엇이고, 까닭은 무엇입니까?</p><p class="quiz-a">실행 흔적·답 글·사용량을 받지 못했습니다. 한도 3이 노드 실행 수 3과 같아 <code>GraphRecursionError</code>가 났고, 메서드 <code>invoke</code>가 결과를 내놓지 않았기 때문입니다. 틀렸다면 노트북 7절과 03절을 다시 읽습니다.</p><p class="quiz-q">4. [상] 동료가 「오류 처리 함수를 붙였으니 이 그래프는 오류로 멈추지 않는다」고 말합니다. 이 절 결과로 무엇이라고 답하나요?</p><p class="quiz-a">이 오류 처리 함수는 도구 몸통이 낸 <code>ValueError</code>만 받도록 좁힌 설계라고 답합니다. 실행 2의 한도 오류는 받지 않아 흐름이 멈췄습니다. 02절 8절에서 본 입력 검사 오류도 받지 않습니다. 틀렸다면 노트북 7절과 02절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li>01절 — 모델 노드·도구 실행 노드·도구 조건 함수·되돌아가는 엣지, 함수 <code>run_row</code>.</li><li>02절 — 오류 처리 인자와 오류 처리 함수, 받을 오류 표시.</li><li>03절 — 설정 딕셔너리와 실행 한도, 노드 실행 수와 통과하는 한도의 경계.</li><li>04절 — 도구 파일에 더한 사용량·예상 비용 함수.</li><li>Ch 19 06절 — 함수 <code>show_messages</code>와 결과 상태.</li><li>Ch 6 06절 — 요금표와 예상 비용.</li><li>기준 버전은 노트북 1절 첫 셀에서 설치한 패키지 다섯의 판입니다. 그래프는 langgraph 1.2.11로 만들었습니다.</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# ToolNode 실습: 자료실 문의 그래프에 오류 처리 함수와 실행 한도 붙이기

**이 노트북에서 할 일**

1. 01절 그래프에 02절 오류 처리 함수와 03절 실행 한도를 붙여, 자료실 문의 하나를 처리합니다.
2. 도구 메시지의 결과 상태로 오류 처리 함수가 쓰였는지 보고, 그 흐름의 노드 실행 수를 셉니다.
3. 실행 한도 하나만 노드 실행 수와 같게 줄여 다시 실행하고, 두 실행을 견줍니다.

**준비물** — 프로젝트 맨 위 폴더의 `.env`에 적어 둔 `OPENAI_API_KEY`를 씁니다.
모델은 `gpt-5.4-mini`이고, 교재 출력에서 실행 1의 모델 요청은 2번입니다.
실행 2는 한도에 닿아 결과를 받지 못해, 노트북 안에서는 그 요청 수를 셀 수 없습니다.
노트북 밖에서 같은 흐름을 다섯 번 보냈을 때 실행 2도 2번이어서, 모두 4번으로 어림합니다.

모델이 도구를 몇 번 부르느냐에 따라 요청 수는 달라질 수 있습니다.
요금표로 어림한 예상 비용은 0.01달러 아래이고, 청구 금액이 아닙니다.
도구는 노트북 안 규정 딕셔너리를 읽기만 하고, 읽는 파일과 새로 쓰는 파일은 없습니다.

앞에서 배운 함수 넷은 도구 파일 `graph_tools.py`에서 가져옵니다.
걸린 시간은 재지 않습니다. 교재 출력을 만든 실행에서는 노트북 전체가 10초 안에 끝났습니다.

**기준 버전** — 첫 셀에서 패키지 다섯을 설치합니다.
판은 langgraph 1.2.11, langchain 1.4.0, langchain-core 1.6.2입니다.
langchain-openai 1.6.0과 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**실습 범위** — 이 절은 챕터 끝 실습 절이고 30분 안에 끝나는 분량입니다.
강사와 함께 첫 셀부터 차례로 실행하고, 따로 내는 과제는 없습니다.
01~04절에서 쓴 이름과 문법만 씁니다.

실습 폴더 `labs/part5/ch20-tool-node`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 읽는 그림으로 맨 위에 초록 상자 둘이 나란히 있습니다. 왼쪽은 첫 상태 대출 문의 하나, 오른쪽은 설정 딕셔너리 03절 recursion_limit 10입니다. 두 상자에서 invoke 첫째 인자와 둘째 인자 화살표가 아래 01절 그래프 모양 칸으로 갑니다. 칸 안에서 회색 가상 시작점 START가 보라 상자 모델 노드 model로 가고, 모델 노드에서 점선 두 갈래가 나갑니다. 요청 있음 이름표 tools 갈래는 회색 상자 도구 실행 노드 tools ToolNode로, 요청 없음 명시적 종료 갈래는 회색 가상 끝점 END로 갑니다. 도구 실행 노드에서 되돌아가는 엣지 실선이 모델 노드로 오고, 도구 실행 노드와 선으로 이은, 양옆에 세로줄이 한 줄씩 더 있는 파란 상자 오류 처리 함수 02절 handle_policy_error 이번 흐름에서 쓰이지 않음이 있는 그림](attachment:05-1-오류-처리-함수와-한도를-붙인-그래프.png)

위에서 아래로 읽습니다. 아래 칸에서 오류 처리 함수를 뺀 상자 넷과 화살표 넷은 노트북 5절 구조 문자열과 같습니다.
보라 상자는 모델에 요청을 보내는 모델 노드이고, 회색은 LangGraph가 준 것입니다.
오류 처리 함수는 노드가 아니라서 양옆에 세로줄이 더 있는 파란 상자로 그렸고, 이번 두 실행에서는 쓰이지 않았습니다.
맨 위 초록 상자 둘은 메서드 `invoke`에 넘기는 두 인자이고, 실행 2에서는 오른쪽 한도만 바꿉니다.

### [2] markdown {}

## 1. 준비

이번 절은 이 챕터의 실습입니다.
01절 그래프에 02절 오류 처리 함수와 03절 실행 한도를 붙여, 자료실 문의 하나를 처리합니다.
첫 셀은 패키지 다섯 개를 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:38.905355Z', 'iopub.status.busy': '2026-09-24T08:34:38.905195Z', 'iopub.status.idle': '2026-09-24T08:34:39.585798Z', 'shell.execute_reply': '2026-09-24T08:34:39.585218Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "langgraph==1.2.11" "langchain==1.4.0" "langchain-core==1.6.2" "langchain-openai==1.6.0" "python-dotenv==1.2.3"
from importlib.metadata import version

print("langgraph:", version("langgraph"))
print("langchain:", version("langchain"))
print("langchain-core:", version("langchain-core"))
print("langchain-openai:", version("langchain-openai"))
print("python-dotenv:", version("python-dotenv"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
langgraph: 1.2.11
langchain: 1.4.0
langchain-core: 1.6.2
langchain-openai: 1.6.0
python-dotenv: 1.2.3

```

### [4] markdown {}

**결과 읽기** — 출력 줄 `langgraph: 1.2.11`·`langchain: 1.4.0`·`langchain-core: 1.6.2`가 보입니다.
출력 줄 `langchain-openai: 1.6.0`과 `python-dotenv: 1.2.3`도 잠금과 같은 판입니다.
이 노트북의 출력은 2026-09-24에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
그래프와 메시지 이름은 01절과 같고, 03절에서 본 오류 이름 `GraphRecursionError`를 더합니다.
도구 파일에서는 함수 넷을 가져옵니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:39.586807Z', 'iopub.status.busy': '2026-09-24T08:34:39.586720Z', 'iopub.status.idle': '2026-09-24T08:34:40.124499Z', 'shell.execute_reply': '2026-09-24T08:34:40.124243Z'}, 'lesson_role': 'setup'}

```python
# 01절 그래프 이름에 03절 오류 이름 하나를 더하고, 도구 파일의 함수 넷을 가져옵니다
import operator
from typing import Annotated
from typing_extensions import TypedDict

from langchain.chat_models import init_chat_model
from langchain.messages import AnyMessage, HumanMessage
from langchain.tools import tool
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from graph_tools import estimate_cost, run_row, show_messages, sum_usage

print("이 절에서 도구 파일에 더한 함수:", "call_id_lists", "run_row")
```

출력:
```
이 절에서 도구 파일에 더한 함수: call_id_lists run_row

```

### [6] markdown {}

**결과 읽기** — 출력 줄 `이 절에서 도구 파일에 더한 함수: call_id_lists run_row`가 보입니다.

앞에서 배운 함수는 `graph_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다. 커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.

이 절에서 도구 파일에 01절 함수 둘을 더했습니다.
함수 `run_row`는 실행 결과 하나를 기록 한 줄로 만들고, 안에서 함수 `call_id_lists`를 부릅니다.
두 함수 모두 01절 노트북의 본문을 글자 그대로 옮겼습니다.
함수 `show_messages`는 Ch 19 06절, `sum_usage`는 Ch 19 05절, `estimate_cost`는 Ch 6 06절에서 배웠습니다.

## 2. 키와 모델 준비

모델은 01절과 같은 `gpt-5.4-mini`이고, 과정의 같은 설정으로 부릅니다.

### [7] markdown {}

API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다.

### [8] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:40.125263Z', 'iopub.status.busy': '2026-09-24T08:34:40.125209Z', 'iopub.status.idle': '2026-09-24T08:34:40.130019Z', 'shell.execute_reply': '2026-09-24T08:34:40.129686Z'}, 'lesson_role': 'setup'}

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

### [9] markdown {}

실습에 쓸 모델을 준비합니다.
temperature 값을 0으로 두어도, 모델이 도구 호출 요청을 보낼지가 매번 같다고 보장하지는 않습니다.

### [10] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:40.130607Z', 'iopub.status.busy': '2026-09-24T08:34:40.130553Z', 'iopub.status.idle': '2026-09-24T08:34:41.057163Z', 'shell.execute_reply': '2026-09-24T08:34:41.056808Z'}}

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

### [11] markdown {}

**결과 읽기** — 모델 이름 `gpt-5.4-mini`, temperature `0.0`이 보이면 준비가 끝났습니다.
이 노트북의 출력은 2026-09-24에 이 모델로 실행한 결과입니다.

### [12] markdown {}

## 3. 오늘 처리할 문의

이번 실습은 자료실 창구에 들어온 문의 하나를 그래프로 처리합니다.
문의 글은 01절 7절 대출 질문 그대로이고, 이 절에서 실행 전에 정했습니다.
다음 셀은 문의 글로 첫 상태를 만듭니다.
이 첫 상태를 실행 1과 실행 2에 똑같이 넣습니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:41.057844Z', 'iopub.status.busy': '2026-09-24T08:34:41.057786Z', 'iopub.status.idle': '2026-09-24T08:34:41.059739Z', 'shell.execute_reply': '2026-09-24T08:34:41.059474Z'}}

```python
# 오늘 처리할 자료실 문의 하나로 첫 상태를 만듭니다(01절 7절 대출 질문과 같은 글)
inquiry = "자료실에서 일반 도서를 며칠 빌릴 수 있나요?"
inquiry_state = {"messages": [HumanMessage(content=inquiry)], "trace": []}
print("문의:", inquiry)
print("출처: 01절 7절 대출 질문 그대로, 이 절에서 실행 전에 정함")
state_keys = list(inquiry_state.keys())
print("첫 상태의 칸:", state_keys)
```

출력:
```
문의: 자료실에서 일반 도서를 며칠 빌릴 수 있나요?
출처: 01절 7절 대출 질문 그대로, 이 절에서 실행 전에 정함
첫 상태의 칸: ['messages', 'trace']

```

### [14] markdown {}

**결과 읽기** — 출력 줄 `첫 상태의 칸: ['messages', 'trace']`로 메시지 칸과 실행 흔적 칸을 확인합니다.
메시지 칸에는 문의 하나를 담고, 흔적 칸은 빈 목록으로 두었습니다.
출력 줄 `출처:`는 이 문의가 어디서 왔는지 적은 줄입니다.

## 4. 재료 · 자료와 도구와 오류 처리 함수

다음 셀은 01절과 글자까지 같은 셀로, 주제어를 키로 한 규정 딕셔너리를 만듭니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:41.060290Z', 'iopub.status.busy': '2026-09-24T08:34:41.060232Z', 'iopub.status.idle': '2026-09-24T08:34:41.062013Z', 'shell.execute_reply': '2026-09-24T08:34:41.061781Z'}}

```python
# 교육센터 자료실 규정 셋을, 주제어를 키로 한 딕셔너리에 담습니다(도구가 읽기만 하는 자료)
POLICIES = {
    "대출": "일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.",
    "운영": "평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.",
    "연체": "연체한 일수만큼 새 대출이 제한됩니다.",
}
topics = list(POLICIES.keys())
print("규정 주제어:", topics)
```

출력:
```
규정 주제어: ['대출', '운영', '연체']

```

### [16] markdown {}

**결과 읽기** — 출력 줄 `규정 주제어: ['대출', '운영', '연체']`로 키 셋을 확인합니다.
오늘 문의는 대출 규정을 찾아야 답할 수 있는 질문입니다.

다음 셀은 03·04절과 글자까지 같은 도구 셀입니다.
01절 도구와 코드가 같고, 오류 줄 위 주석 한 줄만 「02절에서 본 ValueError」로 적었습니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:41.062708Z', 'iopub.status.busy': '2026-09-24T08:34:41.062655Z', 'iopub.status.idle': '2026-09-24T08:34:41.065423Z', 'shell.execute_reply': '2026-09-24T08:34:41.065149Z'}}

```python
# 주제어 하나로 규정 글 하나를 찾는 도구를 만듭니다(맨 @tool 줄 — Ch 19 01절)
@tool
def lookup_policy(topic: str):
    """교육센터 자료실 규정 하나를 주제어로 찾습니다. topic에는 대출, 운영, 연체 가운데 하나를 넣습니다."""
    # 딕셔너리에 없는 주제어면 오류를 냅니다(02절에서 본 ValueError입니다)
    if topic not in POLICIES:
        raise ValueError("지원하지 않는 주제: " + topic)
    return POLICIES[topic]
```

출력:
```

```

### [18] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
딕셔너리에 없는 주제어를 받으면, 도구는 `ValueError`를 냅니다.

다음 셀은 01절과 글자까지 같은 셀로, 도구 목록을 모델에게 알려 준 `bound_model`을 만듭니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:41.065906Z', 'iopub.status.busy': '2026-09-24T08:34:41.065852Z', 'iopub.status.idle': '2026-09-24T08:34:41.069066Z', 'shell.execute_reply': '2026-09-24T08:34:41.068784Z'}}

```python
# 도구 목록을 모델에게 알려 줍니다(Ch 19 04절 bind_tools, 요청은 아직 보내지 않음)
tools = [lookup_policy]
# 한 응답에 도구 호출 요청을 하나까지만 받게 합니다(Ch 19 06절과 같은 값)
bound_model = model.bind_tools(tools, parallel_tool_calls=False)
print("실어 보낼 명세 수:", len(bound_model.kwargs["tools"]))
print("여럿 담기:", bound_model.kwargs["parallel_tool_calls"])
```

출력:
```
실어 보낼 명세 수: 1
여럿 담기: False

```

### [20] markdown {}

**결과 읽기** — 출력 줄 `실어 보낼 명세 수: 1`과 `여럿 담기: False`는 01절과 같습니다.
한 응답에는 도구 호출 요청이 하나까지만 담깁니다.
그래서 요청이 든 응답마다 도구 실행 노드가 한 번 실행되고, 도구 메시지가 하나 생깁니다.

다음 셀은 02절 7절과 글자까지 같은 오류 처리 함수입니다.
도구 실행 노드가 넘긴 `ValueError` 하나로, 도구 메시지에 담을 안내 글을 만들어 내놓습니다.
첫 매개변수 뒤 `: ValueError`는 02절에서 본 받을 오류 표시이고, 라이브러리가 이 표시를 읽습니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:41.069637Z', 'iopub.status.busy': '2026-09-24T08:34:41.069588Z', 'iopub.status.idle': '2026-09-24T08:34:41.071324Z', 'shell.execute_reply': '2026-09-24T08:34:41.071082Z'}}

```python
# 도구 실행 노드가 넘긴 ValueError 하나로, 도구 메시지에 담을 안내 글을 만들어 내놓습니다
def handle_policy_error(error: ValueError):
    # 첫 매개변수의 표시 ValueError를 도구 실행 노드가 읽고, 이 종류의 오류만 이 함수에 넘깁니다
    reason = str(error)
    # 무엇이 잘못됐는지와, 이 도구로 찾을 수 있는 주제어를 함께 적습니다
    return "규정을 찾지 못했습니다(" + reason + "). 이 도구로 찾을 수 있는 주제어는 대출, 운영, 연체입니다."
```

출력:
```

```

### [22] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
02절에서 본 설치판 소스대로면, 받을 오류 표시가 `ValueError`인 이 함수에는 다른 종류의 오류가 넘어오지 않습니다.

다음 셀은 이 함수를 그래프 없이 한 번 불러, 어떤 글을 내놓는지 봅니다.
02절 7절 셀과 코드가 같고, 첫 줄 주석만 이 절에 맞게 적었습니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:41.071799Z', 'iopub.status.busy': '2026-09-24T08:34:41.071754Z', 'iopub.status.idle': '2026-09-24T08:34:41.073528Z', 'shell.execute_reply': '2026-09-24T08:34:41.073181Z'}}

```python
# 02절 7절처럼 ValueError 하나를 직접 만들어, 도구 실행 노드 없이 오류 처리 함수에 넣어 봅니다
sample_error = ValueError("지원하지 않는 주제: 주차")
guide_text = handle_policy_error(sample_error)
print("내놓은 글:", guide_text)
```

출력:
```
내놓은 글: 규정을 찾지 못했습니다(지원하지 않는 주제: 주차). 이 도구로 찾을 수 있는 주제어는 대출, 운영, 연체입니다.

```

### [24] markdown {}

**결과 읽기** — 라벨 `내놓은 글:` 뒤에 안내 글 한 줄이 보입니다.
괄호 안 `지원하지 않는 주제: 주차`가 오류의 글이고, 괄호 뒤 문장이 주제어 안내입니다.
조립한 그래프에서 도구가 이 오류를 내면, 이 글이 도구 메시지의 내용이 됩니다.

## 5. 조립 · 01절 그래프에 오류 처리 함수 붙이기

조립에 쓰는 상태 형식과 모델 노드는 01절 셀 그대로입니다.
다음 셀은 01절과 글자까지 같은 상태 형식입니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:41.074042Z', 'iopub.status.busy': '2026-09-24T08:34:41.073987Z', 'iopub.status.idle': '2026-09-24T08:34:41.075441Z', 'shell.execute_reply': '2026-09-24T08:34:41.075194Z'}}

```python
# 메시지 칸과 실행 흔적 칸에 각각 규칙을 적은 상태 형식을 만듭니다(Ch 13 04절 모양)
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    trace: Annotated[list[str], operator.add]
```

출력:
```

```

### [26] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
메시지 칸에는 메시지 리듀서, 실행 흔적 칸에는 이어 붙이기 규칙을 적었습니다.

다음 셀은 01절과 글자까지 같은 모델 노드입니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:41.075993Z', 'iopub.status.busy': '2026-09-24T08:34:41.075948Z', 'iopub.status.idle': '2026-09-24T08:34:41.077521Z', 'shell.execute_reply': '2026-09-24T08:34:41.077270Z'}}

```python
# 메시지 칸 전체를 도구를 알려 준 모델에 보내고, 응답 하나와 노드 이름만 냅니다
def call_model(state):
    response = bound_model.invoke(state["messages"])
    return {"messages": [response], "trace": ["model"]}
```

출력:
```

```

### [28] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 노드를 지날 때마다 모델 요청이 한 번 나가고, 실행 흔적 칸에 `model`이 붙습니다.

다음 셀은 02절 7절처럼 오류 처리 함수를 넘겨 도구 실행 노드를 만듭니다.
오류 처리 인자 `handle_tool_errors`에 4절의 함수를 넘깁니다.

### [29] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:41.078038Z', 'iopub.status.busy': '2026-09-24T08:34:41.077981Z', 'iopub.status.idle': '2026-09-24T08:34:41.079509Z', 'shell.execute_reply': '2026-09-24T08:34:41.079298Z'}}

```python
# 02절 7절처럼 오류 처리 함수를 넘겨 도구 실행 노드를 만듭니다(아직 그래프에 넣지 않음)
policy_node = ToolNode(tools, handle_tool_errors=handle_policy_error)
print("만든 것의 종류:", type(policy_node).__name__)
# 속성 tools_by_name은 01절에서 본 도구 찾기 표입니다
table_keys = list(policy_node.tools_by_name.keys())
print("안에 든 도구 찾기 표의 키:", table_keys)
```

출력:
```
만든 것의 종류: ToolNode
안에 든 도구 찾기 표의 키: ['lookup_policy']

```

### [30] markdown {}

**결과 읽기** — 출력 줄 `만든 것의 종류: ToolNode`와 `안에 든 도구 찾기 표의 키: ['lookup_policy']`입니다.
01절 도구 실행 노드와 다른 것은 오류 처리 인자 하나입니다.

다음 셀은 01절과 글자까지 같은 이름표 표입니다.

### [31] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:41.080091Z', 'iopub.status.busy': '2026-09-24T08:34:41.080044Z', 'iopub.status.idle': '2026-09-24T08:34:41.081530Z', 'shell.execute_reply': '2026-09-24T08:34:41.081201Z'}}

```python
# 도구 조건 함수의 이름표 둘을 실제로 갈 곳에 잇는 이름표 표를 만듭니다(Ch 13 03절)
path_map = {"tools": "tools", END: END}
print("이름표와 갈 곳을 이은 표:")
for label in path_map:
    print(label, "->", path_map[label])
```

출력:
```
이름표와 갈 곳을 이은 표:
tools -> tools
__end__ -> __end__

```

### [32] markdown {}

**결과 읽기** — 라벨 줄 아래 `tools -> tools`와 `__end__ -> __end__` 두 줄입니다.
도구 조건 함수가 `END`를 내놓으면 가상 끝점으로 갑니다.
03절에서 본 명시적 종료를, 이 그래프에서는 01절 도구 조건 함수가 맡습니다.

다음 셀은 01절 6절과 같은 노드와 엣지로 그래프를 조립합니다.
도구 실행 노드 자리에만 `policy_node`를 넣습니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:41.082205Z', 'iopub.status.busy': '2026-09-24T08:34:41.082152Z', 'iopub.status.idle': '2026-09-24T08:34:41.086849Z', 'shell.execute_reply': '2026-09-24T08:34:41.086525Z'}}

```python
# 01절 6절과 같은 노드와 엣지로 그래프를 조립합니다(도구 실행 노드 자리만 policy_node)
builder = StateGraph(AgentState)
builder.add_node("model", call_model)
builder.add_node("tools", policy_node)
builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition, path_map)
builder.add_edge("tools", "model")
graph = builder.compile()
print("등록한 노드:", list(builder.nodes))
```

출력:
```
등록한 노드: ['model', 'tools']

```

### [34] markdown {}

**결과 읽기** — 출력 줄 `등록한 노드: ['model', 'tools']`입니다.
시작 엣지·조건부 엣지·되돌아가는 엣지는 01절과 같은 세 줄입니다.

다음 셀은 01절 6절과 글자까지 같은 셀로, 그래프가 스스로 그린 구조 문자열을 받아 옵니다.

### [35] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:41.087425Z', 'iopub.status.busy': '2026-09-24T08:34:41.087376Z', 'iopub.status.idle': '2026-09-24T08:34:41.090500Z', 'shell.execute_reply': '2026-09-24T08:34:41.090213Z'}}

```python
# 컴파일한 그래프가 스스로 그린 구조 문자열을 받아 옵니다(Ch 13 01절)
structure_text = graph.get_graph().draw_mermaid()
print("그래프가 그린 구조:")
print(structure_text)
```

출력:
```
그래프가 그린 구조:
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	model(model)
	tools(tools)
	__end__([<p>__end__</p>]):::last
	__start__ --> model;
	model -.-> __end__;
	model -.-> tools;
	tools --> model;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc


```

### [36] markdown {}

**결과 읽기** — 라벨 줄 `그래프가 그린 구조:` 아래에서 화살표 줄 넷을 봅니다.
줄 `__start__ --> model`·`model -.-> __end__`·`model -.-> tools`·`tools --> model`입니다.
01절 6절 출력과 같은 넷이라, 오류 처리 함수를 넘겨도 그래프 모양은 그대로입니다.
오류 처리 함수는 노드가 아니라 도구 실행 노드 안에서 쓰여, 구조 문자열에 나오지 않습니다.

## 6. 실행 1 · 한도 10으로 문의 처리하기

첫 실행은 03절 4절과 같은 설정 딕셔너리로 합니다.
실행 한도는 그래프가 한 번 실행에서 진행할 수 있는 단계 수의 한도입니다.
실행 전에 예상해 봅니다.
01절 7절처럼 모델 노드·도구 실행 노드·모델 노드를 지나 끝나고, 모델 요청은 2번일 것입니다.
대출은 딕셔너리에 있는 주제어라, 오류 처리 함수는 쓰이지 않을 것입니다.

### [37] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:41.091024Z', 'iopub.status.busy': '2026-09-24T08:34:41.090967Z', 'iopub.status.idle': '2026-09-24T08:34:43.448026Z', 'shell.execute_reply': '2026-09-24T08:34:43.447372Z'}}

```python
# 실행 1: 03절과 같은 설정 딕셔너리(한도 10)로 문의를 처리합니다(모델 요청 2번 예상)
limit_config = {"recursion_limit": 10}
print("설정 딕셔너리:", limit_config)
one_result = graph.invoke(inquiry_state, limit_config)
print("실행 흔적 칸:", one_result["trace"])
print("메시지 칸의 메시지 수:", len(one_result["messages"]))
```

출력:
```
설정 딕셔너리: {'recursion_limit': 10}
실행 흔적 칸: ['model', 'model']
메시지 칸의 메시지 수: 4

```

### [38] markdown {}

**결과 읽기** — 출력 줄 `설정 딕셔너리: {'recursion_limit': 10}`과 `실행 흔적 칸: ['model', 'model']`입니다.
출력 줄 `메시지 칸의 메시지 수: 4`입니다.
모델 노드를 두 번 지났으니, 모델 요청이 2번 나갔습니다.
한도 10에 닿지 않고, 메서드 `invoke`가 결과를 내놓았습니다.

다음 셀은 메시지 칸을 차례로 출력합니다.

### [39] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:43.449351Z', 'iopub.status.busy': '2026-09-24T08:34:43.449226Z', 'iopub.status.idle': '2026-09-24T08:34:43.451964Z', 'shell.execute_reply': '2026-09-24T08:34:43.451408Z'}}

```python
# 메시지 칸을 차례로 출력합니다(Ch 19 06절 함수 show_messages)
print("메시지 칸:")
show_messages(one_result["messages"])
```

출력:
```
메시지 칸:
HumanMessage
AIMessage | 도구 호출 요청: ['lookup_policy']
ToolMessage | 결과 상태: success | 내용: 일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.
AIMessage | 도구 호출 요청: []

```

### [40] markdown {}

**결과 읽기** — 라벨 줄 아래 네 줄이 메시지 칸입니다.
둘째 줄은 `AIMessage | 도구 호출 요청: ['lookup_policy']`, 넷째 줄은 `AIMessage | 도구 호출 요청: []`입니다.
셋째 줄 도구 메시지는 결과 상태 `success`에 대출 규정 글입니다.
도구가 오류를 내지 않아, 이번 흐름에서 오류 처리 함수는 쓰이지 않았습니다.

다음 셀은 첫 응답에 담긴 요청의 인자와, 도구 메시지의 결과 상태를 봅니다.

### [41] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:43.453236Z', 'iopub.status.busy': '2026-09-24T08:34:43.453127Z', 'iopub.status.idle': '2026-09-24T08:34:43.455806Z', 'shell.execute_reply': '2026-09-24T08:34:43.455364Z'}}

```python
# 첫 응답의 도구 호출 요청 인자와, 셋째 메시지(도구 메시지)의 결과 상태를 봅니다
first_response = one_result["messages"][1]
for call in first_response.tool_calls:
    print("도구 이름:", call["name"], "| 인자:", call["args"])
tool_message = one_result["messages"][2]
print("셋째 메시지의 결과 상태:", tool_message.status)
```

출력:
```
도구 이름: lookup_policy | 인자: {'topic': '대출'}
셋째 메시지의 결과 상태: success

```

### [42] markdown {}

**결과 읽기** — 출력 줄 `도구 이름: lookup_policy | 인자: {'topic': '대출'}`입니다.
출력 줄 `셋째 메시지의 결과 상태: success`입니다.
모델이 딕셔너리에 있는 주제어 `대출`을 골라, 도구가 규정 글을 찾았습니다.
주제어는 모델이 정한 값이라, 실행한 때에 따라 달라질 수 있습니다.

다음 셀은 01절 10절 함수 `run_row`로 실행 결과를 기록 한 줄로 만들고, 노드 실행 수를 셉니다.
01절에서 본 것처럼 도구 실행 노드는 실행 흔적 칸을 쓰지 않습니다.
그래서 모델 노드를 지난 수, 곧 모델 요청 수에 도구 메시지 수를 더합니다.

### [43] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:43.456804Z', 'iopub.status.busy': '2026-09-24T08:34:43.456706Z', 'iopub.status.idle': '2026-09-24T08:34:43.459213Z', 'shell.execute_reply': '2026-09-24T08:34:43.458873Z'}}

```python
# 실행 결과를 기록 한 줄로 만들고, 노드 실행 수를 셉니다(01절 10절 함수 run_row)
one_row = run_row("대출 문의", one_result)
print("기록 한 줄:", one_row)
# 도구 실행 노드는 흔적 칸을 쓰지 않으므로, 도구 메시지 수를 더해 노드 실행 수를 셉니다
one_steps = one_row["모델 요청 수"] + one_row["도구 메시지 수"]
print("노드 실행 수:", one_steps)
```

출력:
```
기록 한 줄: {'질문': '대출 문의', '실행 흔적': ['model', 'model'], '모델 요청 수': 2, '도구 메시지 수': 1, '호출 ID 짝': True}
노드 실행 수: 3

```

### [44] markdown {}

**결과 읽기** — 라벨 `기록 한 줄:` 뒤 딕셔너리에서 `'모델 요청 수': 2`와 `'도구 메시지 수': 1`을 봅니다.
칸 `'호출 ID 짝': True`로, 도구 메시지에 요청 id가 옮겨진 것도 확인합니다.
출력 줄 `노드 실행 수: 3`은 모델 노드 두 번과 도구 실행 노드 한 번입니다.
이 그래프는 단계마다 노드 하나를 실행하므로, 실행 1은 단계 셋을 지났습니다.

다음 셀은 마지막 응답을 봅니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:43.459864Z', 'iopub.status.busy': '2026-09-24T08:34:43.459788Z', 'iopub.status.idle': '2026-09-24T08:34:43.461593Z', 'shell.execute_reply': '2026-09-24T08:34:43.461209Z'}}

```python
# 마지막 응답의 도구 호출 요청 수와 답 글을 봅니다
last_message = one_result["messages"][-1]
print("마지막 응답의 도구 호출 요청 수:", len(last_message.tool_calls))
print("답 글:")
print(last_message.content)
```

출력:
```
마지막 응답의 도구 호출 요청 수: 0
답 글:
자료실의 일반 도서는 **1인 5권까지, 14일 동안** 빌릴 수 있습니다.

```

### [46] markdown {}

**결과 읽기** — 출력 줄 `마지막 응답의 도구 호출 요청 수: 0`입니다.
그래서 도구 조건 함수가 `END`를 내놓아 흐름이 끝났습니다.
03절 말로 명시적 종료이고, 실행 한도에 닿기 전에 일어났습니다.
라벨 줄 `답 글:` 아래는 모델이 도구 메시지를 읽고 쓴 답입니다.

이번 실행에서는 답 글이 도구 메시지의 1인 5권과 14일을 옮겨 적었습니다.
새 커널로 한 번 더 실행했을 때는 답 글의 쉼표 하나가 달랐습니다.
답 글은 실행마다 문장이 달라질 수 있어, 결론에 쓰지 않습니다.

## 7. 실행 2 · 바꿀 값은 실행 한도

바꿀 값은 실행 한도 하나입니다.
한도를 실행 1에서 센 노드 실행 수와 같게 줄이고, 첫 상태·그래프·모델 설정은 그대로 둡니다.
03절 6절에서는 노드를 세 번 실행하는 흐름이 한도 3에서 멈추고 한도 4에서 통과했습니다.
그때는 모델 없는 그래프였고, 이번에는 모델 요청이 든 흐름에서 그 경계의 멈추는 쪽을 봅니다.

다음 셀은 줄인 한도를 담은 설정 딕셔너리를 만듭니다.

### [47] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:43.462303Z', 'iopub.status.busy': '2026-09-24T08:34:43.462236Z', 'iopub.status.idle': '2026-09-24T08:34:43.463982Z', 'shell.execute_reply': '2026-09-24T08:34:43.463683Z'}}

```python
# 바꿀 값: 실행 한도를 실행 1의 노드 실행 수와 같게 줄인 설정 딕셔너리를 만듭니다
tight_config = {"recursion_limit": one_steps}
print("실행 1의 설정 딕셔너리:", limit_config)
print("실행 2의 설정 딕셔너리:", tight_config)
```

출력:
```
실행 1의 설정 딕셔너리: {'recursion_limit': 10}
실행 2의 설정 딕셔너리: {'recursion_limit': 3}

```

### [48] markdown {}

**결과 읽기** — 출력 줄 `실행 2의 설정 딕셔너리: {'recursion_limit': 3}`입니다.
실행 1의 한도 10에서, 한도 하나만 3으로 바뀌었습니다.

다음 셀은 같은 첫 상태를 이 설정으로 실행합니다.
실행 전에 예상해 봅니다.
03절 규칙대로면 한도 3에서는 `GraphRecursionError`가 날 것입니다.
한도에 닿으면 오류가 올라오므로, 이 셀만 그 오류를 받아 출력합니다.

### [49] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:43.464646Z', 'iopub.status.busy': '2026-09-24T08:34:43.464588Z', 'iopub.status.idle': '2026-09-24T08:34:45.241408Z', 'shell.execute_reply': '2026-09-24T08:34:45.240162Z'}}

```python
# 실행 2: 같은 첫 상태를 줄인 한도로 실행합니다(이 셀만 올라온 오류를 받아 출력합니다)
try:
    two_result = graph.invoke(inquiry_state, tight_config)
    print("끝까지 실행 | 실행 흔적 칸:", two_result["trace"])
except GraphRecursionError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:")
    print(error)
```

출력:
```
받은 오류: GraphRecursionError
오류 글:
Recursion limit of 3 reached without hitting a stop condition. You can increase the limit by setting the `recursion_limit` config key.
For troubleshooting, visit: https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT

```

### [50] markdown {}

**결과 읽기** — 출력 줄 `받은 오류: GraphRecursionError`입니다.
라벨 줄 `오류 글:` 아래 첫 줄은 `Recursion limit of 3 reached without hitting a stop condition.`로 시작합니다.
한도 3에 닿아, 메서드 `invoke`가 결과를 내놓지 않았습니다.
그래서 이 셀에서는 실행 흔적도, 답 글도, 사용량도 받지 못했습니다.
이 오류는 도구가 낸 오류가 아니라서, 오류 처리 함수가 받지 않았습니다.

노트북 밖에서 같은 흐름을 다섯 번 보냈을 때는, 실행 2도 모두 모델 노드를 두 번 지난 뒤 멈췄습니다.
둘째 요청은 답 글까지 만들었지만, 그 답은 받지 못했습니다.
노트북의 모델 노드는 01절 셀 그대로라, 부른 횟수를 따로 적지 않습니다.

## 8. 두 실행 견주기

다음 셀은 03절 6절 규칙으로, 실행 1의 흐름이 통과하는 가장 작은 한도를 셈합니다.
노드 실행 수보다 하나 큰 값입니다.
그 값을 두 실행의 한도와 견줍니다.

### [51] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:45.243395Z', 'iopub.status.busy': '2026-09-24T08:34:45.243229Z', 'iopub.status.idle': '2026-09-24T08:34:45.246947Z', 'shell.execute_reply': '2026-09-24T08:34:45.246244Z'}}

```python
# 03절 6절 규칙(노드 실행 수보다 하나 큰 한도부터 통과)으로 통과 한도를 셈하고, 두 한도와 견줍니다
one_more = 1
pass_limit = one_steps + one_more
print("셈으로 통과하는 가장 작은 한도:", pass_limit)
print("실행 1 한도가 그 값보다 작은가:", limit_config["recursion_limit"] < pass_limit)
print("실행 2 한도가 그 값보다 작은가:", tight_config["recursion_limit"] < pass_limit)
```

출력:
```
셈으로 통과하는 가장 작은 한도: 4
실행 1 한도가 그 값보다 작은가: False
실행 2 한도가 그 값보다 작은가: True

```

### [52] markdown {}

**결과 읽기** — 출력 줄 `셈으로 통과하는 가장 작은 한도: 4`입니다.
출력 줄 `실행 1 한도가 그 값보다 작은가: False`와 `실행 2 한도가 그 값보다 작은가: True`입니다.
셈으로는 한도가 그 값보다 작은 실행만 멈춥니다.
한도 10인 실행 1은 끝까지 갔고, 한도 3인 실행 2는 멈춰 셈과 맞았습니다.
한도 4로는 이번에 실행하지 않았습니다.

## 9. 요청 수와 예상 비용

다음 셀은 실행 1의 모델 응답 사용량을 더하고, 04절과 같은 요금표로 예상 비용을 셉니다.
예상 비용은 요금표로 어림한 값이라 청구 금액이 아닙니다.
실행 2는 결과를 받지 못해, 같은 방법으로 사용량을 셀 수 없습니다.

### [53] code {'execution': {'iopub.execute_input': '2026-09-24T08:34:45.248261Z', 'iopub.status.busy': '2026-09-24T08:34:45.248157Z', 'iopub.status.idle': '2026-09-24T08:34:45.251208Z', 'shell.execute_reply': '2026-09-24T08:34:45.250639Z'}}

```python
# 실행 1의 사용량을 더하고, 2026-09-17 요금표로 예상 비용을 셉니다(Ch 19 05절 sum_usage·Ch 6 06절 estimate_cost)
one_usage = sum_usage(one_result["messages"])
print("실행 1 사용량:", one_usage)
pricing_date = "2026-09-17"
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
one_cost = estimate_cost(one_usage, input_rate, cached_input_rate, output_rate)
print("요금 확인 날짜:", pricing_date)
print("실행 1 예상 비용(달러):", round(one_cost, 6))
```

출력:
```
실행 1 사용량: {'requests': 2, 'input_tokens': 378, 'output_tokens': 46}
요금 확인 날짜: 2026-09-17
실행 1 예상 비용(달러): 0.000491

```

### [54] markdown {}

**결과 읽기** — 출력 줄은 `실행 1 사용량: {'requests': 2, 'input_tokens': 378`로 시작합니다.
모델 요청 2번에 입력 토큰 378입니다.
출력 줄 `요금 확인 날짜: 2026-09-17`은 요금표를 확인한 날짜입니다.

칸 `output_tokens`와 예상 비용은 답 글 길이에 따라 실행마다 달라질 수 있습니다.
이번 실행에서는 출력 토큰 46, 예상 비용 0.000491달러였습니다.
새 커널로 한 번 더 실행했을 때는 출력 토큰이 45라 예상 비용도 달랐습니다.
실행 2에서 나간 요청은 사용량을 받지 못해, 이 예상 비용에 들어 있지 않습니다.

## 정리

1. 01절 그래프에 02절 오류 처리 함수와 03절 설정 딕셔너리를 붙여, 대출 문의를 처리했습니다.
2. 실행 1은 노드를 세 번 실행하고 `END`로 끝났고, 도구 오류가 없어 오류 처리 함수는 쓰이지 않았습니다.
3. 한도만 3으로 줄인 실행 2는 `GraphRecursionError`로 멈춰, 실행 흔적도 답 글도 받지 못했습니다.

이 절로 Ch 20이 끝납니다.
Ch 21 01절은 이 챕터에서 직접 이은 반복 구조를 함수 `create_agent` 한 줄로 얻는 법을 다룹니다.

## 그림

### 05-1-오류-처리-함수와-한도를-붙인-그래프.mmd

```mermaid
flowchart TB
  %% classes
  q["첫 상태<br>대출 문의 하나"]:::tool
  cfg["설정 딕셔너리 · 03절<br>recursion_limit 10"]:::tool
  subgraph G["01절 그래프 모양"]
    direction TB
    s(["가상 시작점 START"])
    m["모델 노드 model<br>도구를 알려 준 모델"]:::model
    t["도구 실행 노드 tools<br>ToolNode"]
    h[["오류 처리 함수 · 02절<br>handle_policy_error<br>이번 흐름에서 쓰이지 않음"]]:::flow
    e(["가상 끝점 END"])
    s --> m
    m -.->|요청 있음 · 이름표 tools| t
    t -->|되돌아가는<br>엣지| m
    m -.->|요청 없음 · 명시적 종료| e
    t ---|오류 처리 인자| h
  end
  q -->|invoke 첫째 인자| G
  cfg -->|invoke 둘째 인자| G
```

01절 그래프에 02절 오류 처리 함수와 03절 실행 한도를 붙였고, 오류 처리 함수는 이번 두 실행에서 쓰이지 않았습니다.

### 05-2-실행-1이-지난-단계-셋.mmd

```mermaid
%%{init: {"sequence": {"messageAlign": "left"}}}%%
sequenceDiagram
  participant P as 노트북 코드<br>graph.invoke
  box Lavender
  participant M as 모델 노드 model<br>gpt-5.4-mini
  end
  participant T as 도구 실행 노드<br>policy_node
  P->>M: 첫 상태 · 한도 10
  Note over M: 단계 1 · 요청 1<br>lookup_policy · 인자 대출
  M->>T: tools_condition · tools
  Note over T: 단계 2<br>도구 메시지 success<br>오류 처리 함수 쓰이지 않음
  T->>M: 되돌아가는 엣지
  Note over M: 단계 3 · 요청 2<br>도구 호출 요청 0건
  M-->>P: tools_condition · END
  Note over P,M: 명시적 종료 · 한도 10에 닿지 않음<br>흔적 model 두 번 · 노드 실행 수 3<br>호출 ID 짝 True
```

실행 1은 모델 노드, 도구 실행 노드, 모델 노드의 세 단계를 지나 한도 10에 닿기 전에 END로 끝났습니다.

### 05-3-한도-하나만-바꾼-두-실행.mmd

```mermaid
flowchart TB
  %% classes
  q["같은 첫 상태 · 대출 문의<br>같은 그래프 · 같은 모델 설정"]:::tool
  subgraph R1["실행 1 · 한도 10"]
    direction TB
    a1["흔적 model 두 번<br>노드 실행 수 3<br>도구 메시지 success 하나"]:::measure
    a2["마지막 응답 요청 0건<br>END로 끝나 결과를 받음"]:::measure
    a1 ~~~ a2
  end
  subgraph R2["실행 2 · 바꾼 값 한도 3"]
    direction TB
    b1["GraphRecursionError<br>Recursion limit of 3"]:::measure
    b2["invoke가 결과를 내놓지 않음<br>흔적 · 답 글 · 사용량 없음"]:::measure
    b3["노트북 밖 다섯 번에서 센 값<br>모델 요청 두 번 뒤 멈춤"]
    b1 ~~~ b2
    b2 ~~~ b3
  end
  rule["셈 · 03절 규칙<br>노드 실행 수 3이면<br>한도 4부터 통과"]
  q --> R1
  q --> R2
  R1 ~~~ rule
  R2 ~~~ rule
```

한도만 노드 실행 수와 같은 3으로 줄인 실행 2는 GraphRecursionError로 멈춰, 실행 흔적도 답 글도 받지 못했습니다.

### 05-4-받침에-선-상자와-빈-카드-주머니.prompt.md

# 05-4-받침에-선-상자와-빈-카드-주머니 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 01절부터 이어 온 두 층 자료실에, 앞 절 소품을 승강 통로 하나에 모아 붙여 봅니다. 서고 옆 벽에는 02절 빈 카드를 꽂아 둔 주머니가 있습니다. … 통로 옆 벽에는 03절 계수기 판이 있어, 상자가 한 층을 들를 때마다 등이 하나씩 켜집니다. 창구 층에는 03절 받침이 있어, 찾을 쪽지가 남지 않으면 상자가 거기에 섭니다.

구성 요소와 배치: 01-5~04-5와 같은 두 층 자료실 벽(크림색, 다른 구멍 없음). **통로는 하나**(01~04는 모두 둘 — 이 절은 한 통로에 부품을 모아 「조립」을 보임). 위층 왼쪽 긴 나무 창구 하나, 아래층 왼쪽 파란 책 책장 하나. 통로 안 위층 높이의 나무 받침(= 03절 명시적 종료) 위에 나무 상자 하나, 상자에 흰 쪽지(= 도구 호출 요청)와 파란 책(= 결과 상태 success 도구 메시지)이 반쯤 나옴. 위층 통로 오른쪽 벽에 둥근 등 여섯이 세로로 달린 판(= 03절 계수기, 실행 한도), 아래 셋만 켜짐(= 실행 1이 지난 단계 셋). 아래층 통로 오른쪽 벽에 빈 회색 카드가 꽂힌 나무 주머니(= 02절 오류 처리 함수, 이번에는 쓰이지 않음). 앞 네 장의 두 통로 구도·색 점 판·손잡이는 되풀이하지 않음. 사람·손·화살표·끈·도르래·톱니·집게·화면 없음.

시선 순서: 가운데 통로 → 받침 위 상자(쪽지와 파란 책) → 오른쪽 위 계수기 판(켜진 등 셋) → 오른쪽 아래 빈 카드 주머니.

검수 기준: 그림만 보고 「통로는 하나이고 상자는 창구 층 받침 위에 섰다」, 「상자에 쪽지와 파란 책이 있다」, 「계수기 등은 일부만 켜졌다」, 「빈 카드 주머니는 그대로다」가 읽히는가. 켜진 등이 셋인가. 글자·숫자·사람이 없는가.

비유 계열: 챕터 리드 결정 9 「자료실 승강 상자」. 인계 「§04 → 실습(05)」 8번 「05 실습 삽화는 앞 절 소품을 한 장에 모아 「조립」이 읽히는 새 장면(한 통로에 쪽지·빈 카드·계수기·받침)」대로. 앞 챕터 소품(쟁반·서랍·바구니·저울·울타리·발자국·공구판·식당 전표·집게)·Ch 14 구멍 판은 쓰지 않았습니다.

## 프롬프트 1차 (탈락)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. Cutaway of a two-floor library wall, plain cream with no other opening. Exactly one vertical grey dumbwaiter shaft in the center, reaching from the lower floor up to the upper floor. Upper floor, left of the shaft: one long wooden service counter. At the upper floor level inside the shaft, one small wooden ledge, and one wooden box resting on that ledge; one white paper slip and one blue book stick halfway out of the open top of the box. Lower floor, left of the shaft: one bookshelf with blue books. Lower floor, right of the shaft: one small wooden wall pocket holding a neat stack of blank light-grey cards. On the wall right of the shaft, between the two floors: one tall narrow panel with a single column of ten small round lamps; only the bottom three lamps glow yellow, the other seven are unlit. Large simple objects. No people, no hands, no arrows, no ropes, no pulleys, no gears, no clips, no screens, nothing else on the walls.
```

## 프롬프트 2차 (채택 — 계수기 판만 바꿈)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. Cutaway of a two-floor library wall, plain cream with no other opening. Exactly one vertical grey dumbwaiter shaft in the center, reaching from the lower floor up to the upper floor. Upper floor, left of the shaft: one long wooden service counter. At the upper floor level inside the shaft, one small wooden ledge, and one wooden box resting on that ledge; one white paper slip and one blue book stick halfway out of the open top of the box. Lower floor, left of the shaft: one bookshelf with blue books. Lower floor, right of the shaft: one small wooden wall pocket holding a neat stack of blank light-grey cards. On the upper floor wall right of the shaft: one short vertical panel with exactly six large round lamps in a single column; the bottom three lamps glow yellow and the top three lamps are unlit grey. Large simple objects. No people, no hands, no arrows, no ropes, no pulleys, no gears, no clips, no screens, nothing else on the walls.
```

## 상태

- 2026-09-24 · `nano_banana_pro`(`jobs_wait` 응답 모델 이름 `nano_banana_2` — 01-5~04-5와 같은 표시) · 16:9 · 2k · `use_unlim: false` · count 1. 생성 전 잔액 **2537.25**(바로 앞 거래 08:01:17Z는 04절 몫). 그림은 새 커널 A·B 대조(08:35) 뒤에 만들었습니다.
- **1차 job `25aed51d-7a07-47d8-af52-2c0329f00558` 탈락**(원본 `1ababe163567…`, 2752 × 1536): 통로 하나·받침 위 상자(쪽지와 파란 책)·빈 카드 주머니는 맞았지만, **계수기 등이 열한 개이고 아래 넷이 켜짐**(요청은 열 개·아래 셋). 켜진 등 수가 실행 1의 단계 셋과 어긋나고 판이 층 바닥선에 걸쳐 그려짐.
- **2차 job `1109ab59-ae4b-43ba-a64f-35f77478bb3b` 채택**(재생성 1회 — 상한). 계수기 판만 「위층 벽, 큰 등 정확히 여섯, 아래 셋 켜짐」으로 바꿈. 거래 기록 **08:38:11Z · 08:40:04Z 「Nano Banana Pro −2」 두 줄 = 이 절 몫 4크레딧**. 생성 뒤 잔액 2533.25.
- **그림에서 확인한 것(그림 읽기·alt·캡션에 반영)**: 두 층을 잘라 보인 크림색 벽, 가운데 회색 승강 통로 **하나**(아래층부터 위층까지). 위층 왼쪽 긴 나무 창구 **하나**, 아래층 왼쪽 파란 책 책장 **하나**. 통로 안 **위층 높이**의 나무 받침 **하나** 위에 나무 상자 **하나**, 상자 위로 흰 쪽지 **한 장**과 파란 책 **한 권**이 반쯤 나옴. 위층 통로 오른쪽 벽의 판 **하나**에 둥근 등 **여섯**(세로 한 줄), **위 셋은 꺼진 회색, 아래 셋은 노랗게 켜짐**(켜진 등 둘레에 짧은 빛살 선). 아래층 통로 오른쪽 벽에 빈 회색 카드 **여러 장**(앞에서 보이는 것 넷~다섯)이 꽂힌 나무 주머니 **하나**. 글자·숫자·사람·손·화살표·끈·도르래·톱니·집게·화면 없음. 판의 등 수(여섯)는 한도 10과 다르므로 본문에 「등 수는 한도 값을 그대로 그린 것이 아니다」를 적음.
- 저장: 기기 셸에서 결과 URL을 `curl`로 받아 `UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pillow`로 RGB·폭 1100px(LANCZOS)로 줄여 `figures/05-4-받침에-선-상자와-빈-카드-주머니.png`(1100 × 614, `b786645d60e24e6eaa1c6e557c550a09b3c0da6337cd79e09e15bc1a84a0a371`)로 저장했습니다. 채택 원본 `0abe450e214b206c87051c1eb5d659b984d1ad58a70a36dbf3637693dc6db48d`(2752 × 1536)은 기기 `/tmp/ch20-05/illu-2-orig.png`에만 있습니다.
- 결과 URL을 다시 받아(`illu-2-again.png`, 같은 해시) 같은 폭으로 줄인 그림과 저장 PNG를 픽셀 대조했습니다(`ImageChops.difference` bbox `None`, 가장 큰 차이 0). 저장 PNG와 상자·계수기 판·주머니 확대본(`.cache/ch20-05-view/crop2-box.png`·`crop2-lamps.png`·`crop2-pocket.png`)을 직접 열어 그림 읽기를 썼습니다.

