# 02-도구-오류와-ToolMessage

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 0.75h | 실습 1.25h | 코드 notebooks/02-도구-오류와-ToolMessage.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>도구 실행 노드(<code>ToolNode</code>)의 기본값에서 도구가 낸 <code>ValueError</code>가 그래프 실행을 멈추는 것을 확인할 수 있습니다.</li>
<li>오류 처리 인자(<code>handle_tool_errors</code>)에 오류 처리 함수를 넘겨, 도구 오류를 도구 메시지로 바꿀 수 있습니다.</li>
<li>받을 오류 표시가 <code>ValueError</code>인 함수를 넘긴 노드가, 인자 이름이 틀린 요청의 오류는 받지 않는 것을 확인할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href="01-ToolNode와-tools-condition.html">01절</a> 그래프에서 도구는 한 번도 오류를 내지 않았습니다. 실제 도구는 일을 끝내지 못할 때가 있습니다. 이 절의 도구는 딕셔너리에 없는 주제어를 받으면 <code>ValueError</code>를 냅니다. 이때 그래프 실행이 멈추면, 모델은 무엇이 잘못됐는지 듣지 못하고 답도 적지 못합니다.</p><p><a href="../ch19-model-tools/06-오류와-읽기-쓰기-분리.html">Ch 19 06절</a>에서는 도구마다 오류 담기 설정을 켜서 도구 오류를 도구 메시지에 담았습니다. 이 절은 같은 일을 도구 실행 노드 쪽에서 합니다. 도구 실행 노드는 그래프 안의 도구 호출 요청을 모두 실행하므로, 오류를 다룰 규칙도 한 곳에 둘 수 있습니다. 제목의 <code>ToolMessage</code>는 <a href="../ch19-model-tools/05-bind_tools와-병렬-호출.html">Ch 19 05절</a>에서 본 도구 메시지입니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href="../ch19-model-tools/02-Pydantic-인자와-반환-스키마.html">Ch 19 02절</a>에서는 도구가 몸통을 실행하기 전에 인자를 입력 형식에 맞춰 보는 일을 입력 검사라고 불렀습니다. 05절에서는 도구 메시지의 호출 ID가 요청의 <code>id</code>를 옮겨 적는다는 것을 보았습니다. 06절에서는 도구 속성 <code>handle_tool_error</code>를 켜서, <code>ToolException</code>을 결과 상태 <code>error</code>인 도구 메시지로 바꿨습니다. 그 절은 <code>ValueError</code> 같은 다른 오류는 설정을 켜도 그대로 올라온다고 적었습니다.</p><p><a href="../../part1/ch02-python/05-파일과-예외.html">Ch 2 05절</a>에서는 <code>try/except 오류이름 as error</code>로 오류를 그 셀에서만 받았습니다. <a href="../../part4/ch16-guardrails/01-입출력-출처-검증.html">Ch 16 01절</a>에서는 <code>raise</code>로 오류를 일부러 냈습니다. 이 절의 도구도 같은 <code>raise</code> 줄로 <code>ValueError</code>를 냅니다.</p><p>01절에서는 도구 실행 노드와 도구 조건 함수로, 모델과 도구를 오가는 그래프를 만들었습니다. 01절 5절에서는 조건 함수에 넣어 보려고 응답을 손으로 만들었습니다. 이 절도 같은 모양으로 도구 호출 요청을 손으로 만들어, 모델 없이 오류 장면을 만듭니다. 상태 형식 <code>AgentState</code>·모델 노드·이름표 표는 01절 코드를 그대로 씁니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절의 두 층 자료실을 다시 떠올립니다. 사서가 주차 규정을 찾아 달라는 쪽지를 상자에 넣어 서고로 내려보냈습니다. 그런데 서고에는 주차 규정 책이 없습니다. 서고가 일을 멈추고 상자를 붙들어 두면, 창구의 사서는 아무 소식도 받지 못합니다.</p><p>서고에 규칙이 하나 있다면 다릅니다. 찾지 못한 까닭을 빈 카드에 적어, 상자에 싣고 올려 보내는 규칙입니다. 사서는 그 카드를 읽고, 손님에게 주차 규정은 찾을 수 없다고 답합니다. 쪽지와 카드에는 Ch 19 05절처럼 같은 색 집게가 꽂혀, 어느 쪽지의 답인지 알려 줍니다.</p><p>서고가 멈추는 것이 이 절의 Before이고, 빈 카드를 올려 보내는 것이 After입니다. 빈 카드는 결과 상태 <code>error</code>인 도구 메시지, 같은 색 집게는 호출 ID입니다. 빈 카드를 쓸지 정하는 서고의 규칙이 오류 처리 인자입니다. 카드에 적을 글을 쓰는 일이 오류 처리 함수입니다.</p>
{{img:02-5-빈-카드를-싣고-온-상자|흰 바탕 그림으로 두 층 자료실 벽을 잘라 보인 모습입니다. 위층 가운데에는 위가 빈 긴 나무 창구가 있고, 아래층 가운데에는 칸마다 가운데가 비고 양 끝에만 파란 책이 꽂힌 책장이 있습니다. 벽 속 왼쪽과 오른쪽에 회색 승강 통로가 하나씩 세로로 나 있습니다. 왼쪽 통로의 나무 상자는 아래층 바닥에 있고, 위 틈으로 흰 종이 쪽지 하나가 반쯤 삐져나와 있습니다. 오른쪽 통로의 같은 모양 나무 상자는 위층 창구 옆까지 올라와 있고, 위 틈으로 아무것도 적히지 않은 옅은 회색 카드 하나가 반쯤 삐져나와 있는 그림|쪽지만 든 왼쪽 상자는 아래층에 머물렀고, 오른쪽 상자는 빈 카드를 싣고 창구 옆으로 올라왔습니다.}}
<p class="look"><b>그림 읽기</b> — 위층에는 긴 나무 창구가 있고, 아래층 책장은 칸마다 가운데가 비어 파란 책이 양 끝에만 있습니다. 책장의 빈칸은 찾는 주제의 자료가 서고에 없다는 뜻입니다. 왼쪽 통로의 상자는 흰 쪽지 하나만 반쯤 내민 채 아래층에 머물러 있고, 이것이 Before의 멈춘 실행입니다. 오른쪽 통로의 같은 상자는 회색 카드 하나를 싣고 창구 옆까지 올라왔고, 이 카드가 결과 상태 <code>error</code>인 도구 메시지입니다. 그림에는 글자를 넣지 않았지만, 본문 비유에서는 이 카드에 찾지 못한 까닭이 적혀 있습니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>오류 처리 인자(handle_tool_errors)</td><td>도구 실행 노드를 만들 때 넘기는 인자입니다. 도구를 실행하다 난 오류 가운데 무엇을 받아 도구 메시지로 바꿀지 정합니다. 빈 카드를 쓸지 정하는 서고의 규칙과 같습니다.</td></tr><tr><td>오류 처리 함수</td><td>도구 실행 노드가 넘긴 오류 하나를 받아, 도구 메시지에 담을 글을 내놓는 함수입니다. 오류 처리 인자에 넘깁니다. 빈 카드에 적을 글을 쓰는 일과 같습니다.</td></tr><tr><td>받을 오류 표시</td><td>오류 처리 함수의 첫 매개변수 뒤에 적는 <code>: ValueError</code> 같은 표시입니다. 도구 실행 노드가 이 표시를 읽어, 이 종류의 오류만 함수에 넘깁니다. 서고 규칙에 「주제가 없을 때만 빈 카드를 쓴다」고 적어 둔 것과 같습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 오류 처리 인자는 <code>ToolNode(tools, handle_tool_errors=handle_policy_error)</code>의 인자 이름입니다. 오류 처리 함수는 <code>handle_policy_error</code>이고, 받을 오류 표시는 그 첫 줄의 <code>error: ValueError</code>입니다. 오류 처리 인자를 주지 않은 <code>ToolNode(tools)</code>는 기본값으로 움직입니다.</p>
{{mermaid:02-1-받을-오류와-두-갈래|위에서 아래로 읽는 그림으로 맨 위 초록 상자 손으로 만든 도구 호출 요청 lookup_policy 주제어 주차에서 회색 상자 도구 실행 노드 tools 도구를 실행으로 화살표가 갑니다. 이 상자에서 점선 두 갈래가 나가 오류 없음이면 회색 상자 도구 메시지 결과 상태 success로, 오류가 남이면 회색 상자 오류 처리 인자가 받을 오류인지 정함으로 갑니다. 그 상자에서 다시 점선 두 갈래가 나가, 받음이면 노란 상자 도구 메시지 결과 상태 error, 내용은 오류 처리 함수의 글, 호출 ID는 요청 id 그대로로 갑니다. 받지 않음이면 빨간 상자 오류가 그래프 밖으로 올라와 실행이 멈춤으로 가는 그림|도구가 오류를 내면 오류 처리 인자가 받을지 정하고, 받으면 도구 메시지가 되며 받지 않으면 실행이 멈춥니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽고, 점선은 갈래입니다. 맨 위 초록 상자는 5절 요청이고, 오류 없음 갈래는 8절 둘째 도구 메시지에서 본 흐름입니다. 회색 상자는 도구 실행 노드 안에서 LangGraph가 하는 일입니다. 도구가 오류를 내면, 오류 처리 인자가 그 오류를 받을지 정합니다. 노란 상자는 7절 After, 빨간 상자는 6절 Before에서 출력으로 확인한 결과입니다.</p>
<h3>오류 담기 설정과 오류 처리 인자</h3><p>Ch 19 06절의 오류 담기 설정 <code>handle_tool_error</code>는 도구 하나에 붙는 속성입니다. 그 도구 안에서 난 <code>ToolException</code>만 도구 메시지로 바꿨습니다. 이 절의 오류 처리 인자 <code>handle_tool_errors</code>는 이름 끝에 s가 붙고, 도구 실행 노드에 붙습니다. 노드가 도구를 실행하다 난 오류 가운데 무엇을 받을지 우리가 정합니다. 이 절의 도구는 <code>ValueError</code>를 내므로, 06절 설정으로는 받지 못하고 이 인자로는 받을 수 있습니다.</p>
<h3>다른 상황에 적용</h3><p>도구 목록에 도구가 여럿이어도 오류 처리 인자는 도구 실행 노드에 한 번만 넘깁니다. 예를 들어 Ch 19의 주문 찾기 도구를 목록에 더하면, 없는 주문 번호에서 난 오류도 같은 규칙으로 다룹니다. 오류 이름이 다르면 받을 오류 표시도 그 이름에 맞춰야 합니다. 이 조합은 이번에 실행하지 않았습니다.</p>
<h3>비교와 경계</h3><p>오류 처리 인자는 받을 오류를 넓게도 좁게도 정할 수 있습니다. 인자를 <code>True</code>로 주거나 받을 오류 표시가 없는 함수를 넘기면, 모든 오류를 받습니다. 인자를 <code>False</code>로 주면 입력 검사에서 걸린 오류까지 올라옵니다. 모든 오류를 같은 글로 바꾸면, 잘못된 인자와 도구 안의 고장을 가르기 어렵습니다. 세 설정은 노트북 밖에서 확인했고, 노트북에서는 실행하지 않았습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 01절과 같은 규정 딕셔너리와 도구를 만들고, 없는 주제어로 도구를 직접 불러 봅니다. 그다음 01절의 상태 형식·모델 노드·이름표 표를 다시 만들고, 도구 실행 노드 하나를 받아 그래프를 만드는 함수를 정의합니다. 이 그래프는 01절과 같은 모양이고, 시작 엣지만 도구 실행 노드로 옮겼습니다. 마지막으로 주차 규정을 찾아 달라는 도구 호출 요청을 손으로 만들어 첫 상태에 넣습니다.</p><p>예시 부분은 모델을 부르지 않습니다. 모델은 7절부터 <code>gpt-5.4-mini</code>를 temperature 0과 추론 끔(<code>reasoning_effort="none"</code>)으로 부릅니다. 교재 출력에서 모델 요청은 모두 3번입니다.</p>
{{notebook:02-도구-오류와-ToolMessage|example}}
<p class="look"><b>확인할 점</b> — 노트북 3절 출력 <code>받은 오류: ValueError</code>로 도구가 직접 낸 오류를 봅니다. 같은 셀의 입력 형식에서 인자 <code>topic</code>의 자료형이 <code>string</code>뿐인 것도 봅니다. 노트북 5절 출력 <code>요청의 id: hand_call_park</code>는 7절 호출 ID와 견줄 값입니다.</p>
{{mermaid:02-2-시작-엣지를-옮긴-그래프|위에서 아래로 읽는 그림으로 맨 위 초록 상자 첫 상태 질문 하나와 손으로 만든 응답 하나 흔적 빈 목록에서 invoke 화살표가 회색 가상 시작점 START로 갑니다. START에서 옮긴 시작 엣지라고 적힌 화살표가 회색 상자 도구 실행 노드 tools ToolNode 설정만 바꿔 끼움으로 가고, 도구 실행 노드에서 실선 화살표가 파란 상자 모델 노드 model 함수 call_model로 갑니다. 모델 노드에서 점선 두 갈래가 나가, 도구 호출 요청 있음 이름표 tools는 도구 실행 노드로, 도구 호출 요청 없음 이름표 END는 회색 가상 끝점 END로 가는 그림|01절 그래프에서 시작 엣지만 도구 실행 노드로 옮겨, 첫 상태에 넣은 요청부터 실행합니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 초록 상자를 뺀 상자 넷과 화살표 넷은 노트북 6절 구조 문자열과 같습니다. 맨 위 초록 상자는 5절에서 만든 첫 상태입니다. 시작 엣지가 도구 실행 노드로 가는 것만 01절 그래프와 다릅니다. 파란 상자는 우리가 적은 모델 노드, 회색은 LangGraph가 준 것입니다.</p>
<h2 id="b6"><span class="no">6</span>실패 확인</h2><p>아래 Before 셀은 01절처럼 도구 목록만 넘긴 도구 실행 노드로, 손으로 만든 주차 요청을 실행합니다. 이어지는 After 셀은 오류 처리 함수를 넘긴 노드로 같은 요청을 실행합니다. 마지막 값 바꿔 보기는 요청을 인자 이름이 틀린 요청으로 바꿔, 두 노드에 다시 넣습니다.</p>
{{notebook:02-도구-오류와-ToolMessage|failure}}
{{mermaid:02-3-기본값과-오류-처리-함수|위에 초록 상자 같은 첫 상태 주차 질문과 손으로 만든 요청 lookup_policy 주차 hand_call_park가 있고, 아래에 칸 둘이 나란히 있는 그림입니다. 왼쪽 칸 Before ToolNode tools 기본값에는 빨간 상자 ValueError 지원하지 않는 주제 주차에서 빨간 상자 그래프 실행이 멈춤 도구 메시지 없음 모델 요청 없음으로 화살표가 갑니다. 오른쪽 칸 After 오류 처리 함수 handle_policy_error에는 노란 상자 도구 메시지 결과 상태 error 호출 ID hand_call_park에서 보라 상자 모델 요청 한 번 gpt-5.4-mini, 노란 상자 마지막 응답 도구 호출 요청 0건으로 화살표가 이어지는 그림|같은 요청에서 기본값 노드는 ValueError로 멈췄고, 오류 처리 함수를 넘긴 노드는 도구 메시지를 모델 노드로 보냈습니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 초록 상자는 두 칸에 똑같이 넣은 첫 상태입니다. 왼쪽 칸이 Before, 오른쪽 칸이 After이고 다른 것은 도구 실행 노드의 오류 처리 인자 하나입니다. 빨간 상자는 Before의 결함 결과이고, 노란 상자는 After 셀의 출력입니다. 보라 상자는 실제로 부른 모델 <code>gpt-5.4-mini</code>입니다.</p>
<p>기본값 도구 실행 노드에서는 도구가 낸 <code>ValueError</code>가 그래프 밖까지 올라와 실행이 멈췄습니다. 그래프는 실행 결과를 내놓지 못했고, 도구 메시지도 모델 요청도 없었습니다. 모델은 주차 규정을 찾지 못했다는 것을 듣지 못했습니다.</p><p>오류 처리 함수를 넘긴 After에서는 같은 요청의 오류가 결과 상태 <code>error</code>인 도구 메시지가 되었습니다. 도구 메시지의 호출 ID는 손으로 만든 요청의 <code>id</code>인 <code>hand_call_park</code> 그대로였습니다. 그래프는 멈추지 않고 모델 노드로 갔고, 모델은 도구 메시지를 읽고 도구 없이 답했습니다. 새 커널로 두 번 실행했을 때와 노트북 밖 다섯 번 모두, 이 흐름의 모델 요청은 1번이었습니다.</p><p>값 바꿔 보기에서는 질문도 01절 대출 질문으로 두고, 인자 이름을 <code>주제</code>로 잘못 적은 요청을 넣었습니다. 이 요청은 몸통 전에 입력 검사에서 걸렸고, 도구 실행 노드는 이 오류를 <code>ToolInvocationError</code>로 감쌌습니다. 표시가 <code>ValueError</code>인 함수를 넘긴 After 노드는 이 오류를 받지 않았고, 그래프가 멈췄습니다. 받을 오류 표시가 그 까닭이라는 것은 설치판 소스와 노트북 밖 확인이 근거이고, 노트북에서는 실행하지 않았습니다.</p><p>반대로 Before의 기본값 노드는 이 오류를 결과 상태 <code>error</code>인 도구 메시지로 바꿨습니다. 모델은 그 글을 읽고 인자 이름을 <code>topic</code>으로 고쳐 다시 요청했고, 규정을 찾아 답했습니다. 이 두 요청에서는 두 설정이 받은 오류가 서로 엇갈렸습니다. <a href="../ch19-model-tools/07-모델과-도구-실습.html">Ch 19 07절</a>이 소스로 적은 「값 검사 오류는 흐름을 멈춘다」는, 우리가 쓴 <code>for</code> 루프와 도구 속성 이야기입니다.</p>
{{mermaid:02-4-받을-오류-표시가-가른-요청|위쪽에 칸 둘이 나란히 있는 그림으로 왼쪽 칸 기본값 ToolNode tools에는 빨간 상자 주차 요청 ValueError로 멈춤과 노란 상자 인자 이름이 틀린 요청 도구 메시지 error 모델이 topic 대출로 다시 요청이 위아래로 있습니다. 오른쪽 칸 오류 처리 함수 받을 오류 표시 ValueError에는 노란 상자 주차 요청 도구 메시지 error와 노란 상자 인자 이름이 틀린 요청 ToolInvocationError로 멈춤이 위아래로 있습니다. 맨 아래 회색 상자에 노드가 감싼 ToolInvocationError는 ValueError가 아님, 두 요청에서 받은 오류가 서로 엇갈림이라고 적힌 그림|받을 오류 표시가 ValueError인 함수를 넘긴 노드는 입력 검사 오류를 받지 않아, 이 두 요청에서 두 설정이 받은 오류가 엇갈렸습니다.}}
<p class="look"><b>도식 읽기</b> — 위쪽 칸 둘은 도구 실행 노드의 두 설정입니다. 칸마다 위 상자가 주차 요청, 아래 상자가 인자 이름이 틀린 요청입니다. 빨간 상자는 Before 결함 결과이고, 노란 상자는 After와 값 바꿔 보기 셀의 출력입니다. 맨 아래 회색 상자의 앞 세 줄은 설치판 소스로 확인한 사실이고, 뒤 두 줄은 두 요청의 출력을 견준 것입니다. 칸 안의 두 상자는 서로 다른 요청이라 화살표로 잇지 않았습니다.</p>
<p class="look"><b>확인할 점</b> — 노트북 6절 출력 <code>받은 오류: ValueError</code>와 7절 출력 <code>결과 상태: error</code>·<code>요청 id와 같은가: True</code>로 Before와 After를 견줍니다. 노트북 8절 출력 <code>받은 오류: ToolInvocationError</code>와 <code>실행 흔적 칸: ['model', 'model']</code>로 두 설정이 받는 오류를 견줍니다. 답 글은 실행마다 달라질 수 있어 결론에 쓰지 않았습니다. 교재 출력에서는 주차 질문의 답 글이 대출·운영·연체 규정을 대신 권했습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>노트북을 실행하기 전에 노트북 밖에서 After 흐름과, 값 바꿔 보기의 기본값 노드 흐름을 다섯 번씩 보냈습니다. 실행 흔적, 메시지 종류, 다시 보낸 요청의 인자가 다섯 번 모두 같았습니다.</li><li>같은 요청도 실행한 때에 따라, 모델이 도구 메시지를 읽고 할 일이 달라질 수 있습니다. 그래서 결론의 중심은 도구 실행 노드가 정하는 값, 곧 오류 이름·결과 상태·호출 ID에 두었습니다.</li><li>도구 호출 요청 둘은 흐름을 보여 주려고 이 절에서 손으로 만든 예입니다. 모델이 이런 요청을 얼마나 자주 보내는지는 재지 않았습니다. <a href="05-ToolNode-실습.html">05절</a> 노트북 밖 확인에서는 같은 주차 질문에 모델이 주제어 <code>주차</code>를 적지 않았습니다.</li><li>질문 둘도 이 절에서 정한 예이고, 대출 질문은 01절 7절과 같은 글입니다.</li><li>오류 처리 함수의 안내 글도 이 절에서 정한 글입니다. 무엇이 잘못됐는지와 찾을 수 있는 주제어를 적었고, 다시 요청하라는 말은 넣지 않았습니다.</li><li>받을 오류 표시는 라이브러리가 읽어 동작을 정하는 값입니다. 이 절에서 노드나 도움 함수의 매개변수에 자료형 표시를 적은 곳은 이 함수 하나입니다.</li><li>이 절의 오류 처리 함수는 도구 몸통이 낸 <code>ValueError</code>만 받도록 좁힌 설계입니다. 입력 검사 오류까지 함께 받는 방법, 예를 들어 받을 오류 표시를 뺀 함수를 넘기는 방법은 이번에 실행하지 않았습니다.</li><li>오류 처리 인자를 <code>True</code>·<code>False</code>로 주거나 표시 없는 함수를 넘긴 결과는 노트북 밖에서 확인했습니다. 설치한 langgraph-prebuilt 1.1.0으로 확인했고, 노트북에서는 실행하지 않았습니다.</li><li>도구 메시지의 오류 글에는 비밀 값, 내부 파일 위치, 긴 오류 추적 글을 넣지 않습니다. 모델에게는 다음 할 일을 정하는 데 필요한 만큼만 보냅니다.</li><li>쓰기 도구가 일부 일을 한 뒤 오류를 내면, 다시 요청할 때 같은 쓰기가 두 번 일어날 수 있습니다. 멈춘 실행을 다시 이어 가는 방법은 <a href="../../part6/ch23-persistence/04-내구-실행-모드-비교.html">Ch 23 04절</a>(강제 종료 뒤)과 <a href="../../part6/ch23-persistence/05-pending-writes와-장애-복구.html">05절</a>(실패한 단계)에서 다룹니다. 같은 쓰기를 한 번만 반영하는 방법은 <a href="../../part6/ch23-persistence/06-노드-재시작과-멱등성.html">Ch 23 06절</a>에서 다룹니다.</li><li>모델 서비스 쪽 오류, 곧 요청 한도 초과·서버 오류·시간 제한은 이 절에서 다루지 않았습니다.</li><li>모델이 정하는 값, 곧 다시 보낸 요청과 답 글에는 <code>assert</code>를 걸지 않았습니다. 셀의 <code>assert</code>는 도구 실행 노드가 정하는 결과 상태와 호출 ID에만 걸었습니다.</li><li>걸린 시간과 토큰은 재지 않았습니다. 모델 요청 수는 실행 흔적 칸의 길이로 셌습니다.</li><li>예상 비용은 2026-09-17 요금표로 어림하면 노트북 한 번에 0.01달러 아래이고, 청구 금액이 아닙니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>도구 실행 노드의 기본값은 도구가 낸 <code>ValueError</code>를 그대로 올려, 그래프 실행이 멈췄습니다.</li><li>오류 처리 함수를 넘기자 같은 오류가 결과 상태 <code>error</code>인 도구 메시지가 되어 모델 노드로 갔습니다.</li><li>받을 오류 표시 <code>ValueError</code>에 맞지 않는 입력 검사 오류는 오류 처리 함수로 가지 않았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href="03-recursion-limit과-명시적-종료.html">03절</a>에서는 그래프가 도구 쪽을 되풀이하는 횟수의 한도와, 흐름을 끝내는 조건을 봅니다. 01절 그래프는 이 한도를 따로 정하지 않고 실행했습니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 도구 목록만 넘겨 만든 도구 실행 노드에서, 도구가 낸 <code>ValueError</code>는 어떻게 되었나요?</p><p class="quiz-a">기본값은 이 오류를 받지 않고 그대로 올려, 그래프 실행이 멈췄습니다. 도구 메시지도 모델 요청도 없어, 모델은 무엇이 잘못됐는지 듣지 못했습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">2. After에서 셋째 메시지는 무엇이었고, 그 호출 ID는 어디서 왔나요?</p><p class="quiz-a">결과 상태가 <code>error</code>인 도구 메시지였습니다. 호출 ID <code>hand_call_park</code>는 손으로 만든 요청의 <code>id</code>를 도구 실행 노드가 옮겨 적은 것입니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">3. Ch 19 06절의 오류 담기 설정과 이 절의 오류 처리 인자는 무엇이 다른가요?</p><p class="quiz-a">오류 담기 설정은 도구 하나에 붙는 속성이고 <code>ToolException</code>만 받습니다. 오류 처리 인자는 도구 실행 노드에 넘기는 인자이고, 받을 오류 종류를 우리가 정합니다. 틀렸다면 본문 4 「핵심 개념」의 「오류 담기 설정과 오류 처리 인자」를 다시 읽습니다.</p><p class="quiz-q">4. 인자 이름이 틀린 요청에서 After 노드가 그래프를 멈춘 까닭은 무엇인가요?</p><p class="quiz-a">도구 실행 노드는 입력 검사 오류를 <code>ToolInvocationError</code>로 감싸 넘기고, 이 이름은 <code>ValueError</code>의 한 종류가 아닙니다. 감싸기 전 원래 오류인 값 검사 오류는 설치판에서 <code>ValueError</code>의 한 종류입니다. 표시가 <code>ValueError</code>인 함수를 넘긴 After 노드는 감싼 오류를 받지 않았고, 표시의 효과는 설치판 소스로 확인했습니다. 틀렸다면 노트북 8절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://reference.langchain.com/python/langgraph.prebuilt/tool_node/ToolNode">ToolNode API 참조</a></div>확인 2026-09-24 · 인자 <code>handle_tool_errors</code>의 자료형과 기본값 이름만 적습니다. 동작은 설치판 소스로 확인했습니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langchain/tools">LangChain Tools</a></div>확인 2026-09-24 · 도구 오류를 도구 메시지로 바꾸는 예가 있습니다. 그 예는 미들웨어를 쓰고, 이 절은 도구 실행 노드의 인자를 씁니다.</li><li>langgraph-prebuilt 1.1.0 소스 <code>langgraph/prebuilt/tool_node.py</code> 383~391행입니다. 기본값 함수는 입력 검사 오류만 글로 바꾸고, 다른 오류는 다시 올립니다.</li><li>같은 소스 444~507행 — 받을 오류 표시를 읽는 함수입니다. 표시가 없으면 모든 오류를 받습니다.</li><li>같은 소스 957~967행 — 입력 검사 오류를 <code>ToolInvocationError</code>로 감싸는 자리입니다.</li><li>같은 소스 1002~1012행 — 받은 오류로 결과 상태 <code>error</code>와 호출 ID를 담은 도구 메시지를 만드는 자리입니다.</li><li>Ch 19 02·05·06절 — 입력 검사, 호출 ID, 오류 담기 설정과 결과 상태.</li><li>Ch 2 05절·Ch 16 01절 — <code>try/except</code>와 <code>raise</code>.</li><li>01절 — 도구 실행 노드, 도구 조건 함수, 되돌아가는 엣지.</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# 도구 오류와 ToolMessage

**이 노트북에서 할 일**

1. 도구가 오류를 낼 때, 도구 실행 노드의 기본값에서 그래프 실행이 어떻게 되는지 봅니다.
2. 오류 처리 함수를 넘겨, 같은 오류를 결과 상태 `error`인 도구 메시지로 바꿉니다.
3. 인자 이름이 틀린 요청으로 바꿔, 두 설정이 그 오류를 받는지 견줍니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 교재 출력에서 모델 요청은 모두 3번입니다.
7절에서 1번, 8절에서 2번을 보냈습니다.
도구 호출 요청은 손으로 만들어 넣고, 모델은 도구 메시지가 생긴 뒤에만 부릅니다.
요금표로 어림한 예상 비용은 모두 합쳐 0.01달러 아래이고, 청구 금액이 아닙니다.

도구는 노트북 안 규정 딕셔너리를 읽기만 하고, 읽는 파일과 새로 쓰는 파일은 없습니다.
Ch 19 함수 둘은 도구 파일 `graph_tools.py`에서 가져옵니다.
교재 출력을 만든 실행에서는 노트북 전체가 10초 안에 끝났습니다.
모델 응답을 기다리는 시간은 네트워크와 실행 때에 따라 달라집니다.

**기준 버전** — 첫 셀에서 패키지 다섯을 설치합니다.
판은 langgraph 1.2.11, langchain 1.4.0, langchain-core 1.6.2입니다.
langchain-openai 1.6.0과 python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3~7절을 읽습니다.
도구와 그래프를 준비하고, 기본값(Before)과 오류 처리 함수(After)를 견주는 자리입니다.
8절은 요청 하나를 바꿔 두 설정을 다시 견주는 자리이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part5/ch20-tool-node`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 읽는 그림으로 맨 위 초록 상자 손으로 만든 도구 호출 요청 lookup_policy 주제어 주차에서 회색 상자 도구 실행 노드 tools 도구를 실행으로 화살표가 갑니다. 이 상자에서 점선 두 갈래가 나가 오류 없음이면 회색 상자 도구 메시지 결과 상태 success로, 오류가 남이면 회색 상자 오류 처리 인자가 받을 오류인지 정함으로 갑니다. 그 상자에서 다시 점선 두 갈래가 나가, 받음이면 노란 상자 도구 메시지 결과 상태 error, 내용은 오류 처리 함수의 글, 호출 ID는 요청 id 그대로로 갑니다. 받지 않음이면 빨간 상자 오류가 그래프 밖으로 올라와 실행이 멈춤으로 가는 그림](attachment:02-1-받을-오류와-두-갈래.png)

위에서 아래로 읽고, 점선은 갈래입니다.
맨 위 초록 상자는 5절 요청이고, 오류 없음 갈래는 8절 둘째 도구 메시지에서 본 흐름입니다.
회색 상자는 도구 실행 노드 안에서 LangGraph가 하는 일입니다.
도구가 오류를 내면, 오류 처리 인자가 그 오류를 받을지 정합니다.
노란 상자는 7절 After, 빨간 상자는 6절 Before에서 출력으로 확인한 결과입니다.

### [2] markdown {}

## 1. 준비

01절에서는 도구 실행 노드(`ToolNode`)가 도구 호출 요청을 실행하고 도구 메시지를 더했습니다.
그때 도구는 한 번도 오류를 내지 않았습니다.
이 절은 도구가 오류를 낼 때 도구 실행 노드가 무엇을 하는지 봅니다.
제목의 `ToolMessage`는 Ch 19 05절에서 본 도구 메시지입니다.

첫 셀은 패키지 다섯 개를 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:20.828851Z', 'iopub.status.busy': '2026-09-24T06:47:20.828713Z', 'iopub.status.idle': '2026-09-24T06:47:21.516084Z', 'shell.execute_reply': '2026-09-24T06:47:21.515503Z'}, 'lesson_role': 'setup'}

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
그래프·메시지·도구 이름은 01절과 같습니다.
Ch 19 06절의 오류 이름 `ToolException`을 하나 더 가져오고, 쓰는 곳은 8절입니다.
도구 파일에서는 Ch 19 함수 `show_messages`와 `tool_call_names`를 가져옵니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:21.517168Z', 'iopub.status.busy': '2026-09-24T06:47:21.517076Z', 'iopub.status.idle': '2026-09-24T06:47:22.231680Z', 'shell.execute_reply': '2026-09-24T06:47:22.231015Z'}, 'lesson_role': 'setup'}

```python
# 01절 이름에 Ch 19 06절 오류 이름 하나를 더하고, 도구 파일 함수 둘을 가져옵니다
import operator
from typing import Annotated
from typing_extensions import TypedDict

from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, AnyMessage, HumanMessage
from langchain.tools import ToolException, tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from graph_tools import show_messages, tool_call_names

print("01절에 더해 가져온 이름:", "ToolException")
```

출력:
```
01절에 더해 가져온 이름: ToolException

```

### [6] markdown {}

**결과 읽기** — 출력 줄 `01절에 더해 가져온 이름: ToolException`이 보입니다.

앞에서 배운 함수는 `graph_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다. 커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.

함수 `tool_call_names`는 Ch 19 04절, 함수 `show_messages`는 Ch 19 06절에서 배웠습니다.
두 함수는 01절에서 쓴 도구 파일의 함수 그대로입니다.

## 2. 키와 모델 준비

모델은 01절과 같은 `gpt-5.4-mini`이고, 과정의 같은 설정으로 부릅니다.

### [7] markdown {}

API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다.

### [8] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:22.232860Z', 'iopub.status.busy': '2026-09-24T06:47:22.232768Z', 'iopub.status.idle': '2026-09-24T06:47:22.243839Z', 'shell.execute_reply': '2026-09-24T06:47:22.243364Z'}, 'lesson_role': 'setup'}

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
temperature 값을 0으로 두어도, 모델이 도구 메시지를 읽고 할 일이 매번 같다고 보장하지는 않습니다.

### [10] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:22.244899Z', 'iopub.status.busy': '2026-09-24T06:47:22.244822Z', 'iopub.status.idle': '2026-09-24T06:47:23.377114Z', 'shell.execute_reply': '2026-09-24T06:47:23.376756Z'}}

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

## 3. 규정 자료와 도구

자료와 도구는 01절과 같은 코드입니다.
다음 셀은 01절처럼 주제어를 키, 규정 글을 값으로 둔 딕셔너리를 만듭니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.377803Z', 'iopub.status.busy': '2026-09-24T06:47:23.377747Z', 'iopub.status.idle': '2026-09-24T06:47:23.379464Z', 'shell.execute_reply': '2026-09-24T06:47:23.379151Z'}}

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

### [14] markdown {}

**결과 읽기** — 출력 줄 `규정 주제어: ['대출', '운영', '연체']`로 키 셋을 확인합니다.
이 셀은 01절 셀과 글자까지 같습니다.

다음 셀은 01절과 같은 도구 `lookup_policy`를 만듭니다.
코드는 01절과 같고, 오류를 내는 줄 위 주석 한 줄만 이 절에 맞게 고쳤습니다.
딕셔너리에 없는 주제어면 Ch 16 01절처럼 `raise`로 `ValueError`를 냅니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.380028Z', 'iopub.status.busy': '2026-09-24T06:47:23.379964Z', 'iopub.status.idle': '2026-09-24T06:47:23.382473Z', 'shell.execute_reply': '2026-09-24T06:47:23.382133Z'}}

```python
# 주제어 하나로 규정 글 하나를 찾는 도구를 만듭니다(맨 @tool 줄 — Ch 19 01절)
@tool
def lookup_policy(topic: str):
    """교육센터 자료실 규정 하나를 주제어로 찾습니다. topic에는 대출, 운영, 연체 가운데 하나를 넣습니다."""
    # 딕셔너리에 없는 주제어면 오류를 냅니다(이 절은 이 오류를 그래프 안에서 다룹니다)
    if topic not in POLICIES:
        raise ValueError("지원하지 않는 주제: " + topic)
    return POLICIES[topic]
```

출력:
```

```

### [16] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
Ch 19 06절의 도구는 오류 이름으로 `ToolException`을 썼습니다.
이 도구가 내는 오류는 `ValueError`이고, 이 차이는 7절에서 다시 봅니다.

다음 셀은 도구의 입력 형식을 보고, 없는 주제어 `"주차"`로 도구를 직접 불러 봅니다.
실행 전에 예상해 봅니다.
입력 형식의 자료형이 글자뿐이면, `"주차"`도 입력 검사를 지나 몸통에서 오류가 날 것입니다.
이 셀만 그 오류를 받아 출력하고, 셀은 끝까지 갑니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.383011Z', 'iopub.status.busy': '2026-09-24T06:47:23.382949Z', 'iopub.status.idle': '2026-09-24T06:47:23.387801Z', 'shell.execute_reply': '2026-09-24T06:47:23.387553Z'}}

```python
# 입력 형식을 보고, 없는 주제어로 도구를 직접 불러 봅니다(이 셀만 오류를 받아 출력합니다)
print("입력 형식:", lookup_policy.args)
try:
    lookup_policy.invoke({"topic": "주차"})
except ValueError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:", error)
```

출력:
```
입력 형식: {'topic': {'title': 'Topic', 'type': 'string'}}
받은 오류: ValueError
오류 글: 지원하지 않는 주제: 주차

```

### [18] markdown {}

**결과 읽기** — 라벨 `입력 형식:` 뒤 딕셔너리에서 인자 `topic`의 자료형은 `string`뿐입니다.
Ch 19 02절의 고를 수 있는 값(`Literal`)처럼, 넣을 수 있는 값을 정해 두지 않았습니다.
그래서 `"주차"`도 입력 검사를 지났고, 출력 줄 `받은 오류: ValueError`처럼 몸통에서 오류가 났습니다.
라벨 `오류 글:` 뒤 `지원하지 않는 주제: 주차`는 `raise` 줄에 적은 글입니다.

Ch 2 05절에서 본 것처럼, 오류를 받지 않는 실제 프로그램이라면 여기서 멈춥니다.
그래프 안에서 이 도구가 오류를 내면 어떻게 되는지는 6절에서 봅니다.

다음 셀은 01절처럼 도구 목록을 모델에게 알려 줍니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.388446Z', 'iopub.status.busy': '2026-09-24T06:47:23.388400Z', 'iopub.status.idle': '2026-09-24T06:47:23.390285Z', 'shell.execute_reply': '2026-09-24T06:47:23.389904Z'}}

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
이 셀은 01절 셀과 글자까지 같고, 아직 모델 요청은 보내지 않았습니다.

## 4. 상태 형식·노드·그래프

상태 형식과 모델 노드, 이름표 표는 01절 셀과 글자까지 같습니다.
다음 셀은 메시지 칸과 실행 흔적 칸에 규칙을 적은 상태 형식 `AgentState`를 만듭니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.390817Z', 'iopub.status.busy': '2026-09-24T06:47:23.390767Z', 'iopub.status.idle': '2026-09-24T06:47:23.392458Z', 'shell.execute_reply': '2026-09-24T06:47:23.392205Z'}}

```python
# 메시지 칸과 실행 흔적 칸에 각각 규칙을 적은 상태 형식을 만듭니다(Ch 13 04절 모양)
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    trace: Annotated[list[str], operator.add]
```

출력:
```

```

### [22] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 구성이 01절과 같아서, 이름도 `AgentState` 그대로 씁니다.

다음 셀은 01절의 모델 노드 함수입니다.
메시지 칸 전체를 도구를 알려 준 모델에 보내고, 응답 하나와 노드 이름 `"model"`만 냅니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.393046Z', 'iopub.status.busy': '2026-09-24T06:47:23.392987Z', 'iopub.status.idle': '2026-09-24T06:47:23.394503Z', 'shell.execute_reply': '2026-09-24T06:47:23.394179Z'}}

```python
# 메시지 칸 전체를 도구를 알려 준 모델에 보내고, 응답 하나와 노드 이름만 냅니다
def call_model(state):
    response = bound_model.invoke(state["messages"])
    return {"messages": [response], "trace": ["model"]}
```

출력:
```

```

### [24] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 노드를 한 번 지날 때마다 모델 요청이 한 번 나갑니다.
그래서 01절처럼 실행 흔적 칸의 `model` 수가 모델 요청 수입니다.

다음 셀은 도구 조건 함수의 이름표 둘을 갈 곳에 잇는 이름표 표입니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.395035Z', 'iopub.status.busy': '2026-09-24T06:47:23.394973Z', 'iopub.status.idle': '2026-09-24T06:47:23.396507Z', 'shell.execute_reply': '2026-09-24T06:47:23.396172Z'}}

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

### [26] markdown {}

**결과 읽기** — 라벨 줄 아래 두 줄 `tools -> tools`와 `__end__ -> __end__`는 01절과 같습니다.

다음 셀은 도구 실행 노드 하나를 받아 그래프를 만드는 함수입니다.
이 절은 도구 실행 노드의 설정만 바꿔 가며 같은 그래프를 두 번 만들기 때문입니다.
그래프 모양은 01절과 같고, 시작 엣지만 도구 실행 노드로 옮겼습니다.
첫 상태에 손으로 만든 도구 호출 요청을 넣고, 그 요청부터 실행하려는 것입니다.
상태 형식·모델 노드·이름표 표는 앞 셀에서 만든 것을 그대로 씁니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.396999Z', 'iopub.status.busy': '2026-09-24T06:47:23.396953Z', 'iopub.status.idle': '2026-09-24T06:47:23.398545Z', 'shell.execute_reply': '2026-09-24T06:47:23.398220Z'}}

```python
# 도구 실행 노드 하나를 받아, 01절 그래프에서 시작 엣지만 옮긴 그래프를 만들어 내놓습니다
def build_graph(tool_node):
    builder = StateGraph(AgentState)
    builder.add_node("model", call_model)
    builder.add_node("tools", tool_node)
    # 첫 상태에 넣은 도구 호출 요청부터 실행하려고, 시작 엣지를 도구 실행 노드로 둡니다
    builder.add_edge(START, "tools")
    builder.add_conditional_edges("model", tools_condition, path_map)
    builder.add_edge("tools", "model")
    return builder.compile()
```

출력:
```

```

### [28] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `build_graph`는 받은 도구 실행 노드를 이름 `"tools"`로 등록하고, 컴파일한 그래프를 내놓습니다.
조건부 엣지와 엣지 `tools → model`은 01절과 같은 자리입니다.
다른 곳은 시작 엣지 `builder.add_edge(START, "tools")` 한 줄뿐입니다.
모델이 요청을 쓰는 보통 그래프는 01절처럼 시작 엣지가 모델 노드로 가고, 05절 실습도 그 모양을 씁니다.

## 5. 손으로 만든 도구 호출 요청

01절 5절에서는 도구 조건 함수에 넣어 보려고 응답을 손으로 만들었습니다.
이 절도 같은 모양으로, 도구 호출 요청 하나를 담은 응답을 손으로 만듭니다.
모델이 주차 규정을 찾아 달라는 요청을 보냈다고 치는 것입니다.
모델이 이런 요청을 언제 보내는지가 아니라, 요청이 온 뒤의 일을 보려는 것입니다.

### [29] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.399031Z', 'iopub.status.busy': '2026-09-24T06:47:23.398971Z', 'iopub.status.idle': '2026-09-24T06:47:23.400826Z', 'shell.execute_reply': '2026-09-24T06:47:23.400532Z'}}

```python
# 주차 규정을 찾아 달라는 도구 호출 요청 하나를 손으로 만들고, 질문과 함께 첫 상태에 넣습니다
park_call = {"name": "lookup_policy", "args": {"topic": "주차"}, "id": "hand_call_park", "type": "tool_call"}
park_request = AIMessage(content="", tool_calls=[park_call])
park_question = "자료실 주차 규정을 알려 주세요."
park_state = {"messages": [HumanMessage(content=park_question), park_request], "trace": []}
print("손으로 만든 응답의 도구 호출 요청:", tool_call_names(park_request))
print("요청의 인자:", park_call["args"])
print("요청의 id:", park_call["id"])
```

출력:
```
손으로 만든 응답의 도구 호출 요청: ['lookup_policy']
요청의 인자: {'topic': '주차'}
요청의 id: hand_call_park

```

### [30] markdown {}

**결과 읽기** — 출력 줄 `손으로 만든 응답의 도구 호출 요청: ['lookup_policy']`입니다.
출력 줄 `요청의 인자: {'topic': '주차'}`와 `요청의 id: hand_call_park`도 보입니다.
이 요청은 우리가 손으로 만든 것이고, 모델이 쓴 요청이 아닙니다.
첫 상태의 메시지 칸에는 질문과 이 응답, 두 메시지가 들어 있습니다.

### [31] markdown {'lesson_part': 'before'}

## 6. 기본값 그대로 실행하기 (Before)

### [32] markdown {'lesson_part': 'before'}

먼저 01절처럼 도구 목록만 넘겨 도구 실행 노드를 만듭니다.
오류를 어떻게 다룰지 정하는 인자를 주지 않았으니, 도구 실행 노드는 기본값으로 움직입니다.
다음 셀은 이 노드로 그래프를 만들고, 그래프가 스스로 그린 구조 문자열을 봅니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.401343Z', 'iopub.status.busy': '2026-09-24T06:47:23.401296Z', 'iopub.status.idle': '2026-09-24T06:47:23.406920Z', 'shell.execute_reply': '2026-09-24T06:47:23.406554Z'}, 'lesson_part': 'before'}

```python
# Before: 01절처럼 도구 목록만 넘긴 도구 실행 노드로 그래프를 만들고, 구조 문자열을 봅니다
default_node = ToolNode(tools)
before_graph = build_graph(default_node)
before_structure = before_graph.get_graph().draw_mermaid()
print("그래프가 그린 구조:")
print(before_structure)
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
	__start__ --> tools;
	model -.-> __end__;
	model -.-> tools;
	tools --> model;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc


```

### [34] markdown {'lesson_part': 'before'}

**결과 읽기** — 라벨 줄 `그래프가 그린 구조:` 아래 화살표 줄 넷을 봅니다.
줄 `__start__ --> tools;`가 01절과 다른 시작 엣지입니다.
줄 `tools --> model;`은 01절의 되돌아가는 엣지이고, 여기서는 도구 실행 노드 다음 차례를 정합니다.
줄 `model -.-> tools;`와 `model -.-> __end__;`는 01절과 같은 조건부 엣지의 두 갈래입니다.

다음 셀은 5절의 첫 상태로 이 그래프를 실행합니다.
실행 전에 예상해 봅니다.
도구 실행 노드가 주차 요청을 실행하면, 도구가 3절처럼 `ValueError`를 낼 것입니다.
이 셀만 그 오류를 받아 출력하고, 셀은 끝까지 갑니다.

### [35] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.407505Z', 'iopub.status.busy': '2026-09-24T06:47:23.407462Z', 'iopub.status.idle': '2026-09-24T06:47:23.410066Z', 'shell.execute_reply': '2026-09-24T06:47:23.409772Z'}, 'lesson_part': 'before'}

```python
# Before 그래프를 주차 요청이 든 첫 상태로 실행합니다(이 셀만 올라온 오류를 받아 출력합니다)
try:
    before_graph.invoke(park_state)
except ValueError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:", error)
```

출력:
```
받은 오류: ValueError
오류 글: 지원하지 않는 주제: 주차

```

### [36] markdown {'lesson_part': 'before'}

**결과 읽기** — 출력 줄 `받은 오류: ValueError`처럼 도구의 오류가 그래프 밖 셀까지 올라왔습니다.
라벨 `오류 글:` 뒤 글은 3절과 같은 `지원하지 않는 주제: 주차`입니다.
그래프 실행은 도구 실행 노드에서 멈췄고, 메서드 `invoke`는 실행 결과를 내놓지 못했습니다.
모델 노드는 도구 실행 노드 다음 차례라, 이 실행에서는 모델 요청도 나가지 않았습니다.

오류를 받지 않는 실제 프로그램이라면 여기서 멈춥니다.
모델은 주차 규정을 찾지 못했다는 것을 듣지 못하고, 답도 적지 못합니다.
이것이 Before의 결함입니다.
설치한 langgraph-prebuilt 1.1.0 소스에서도 기본값은 `ValueError`를 받지 않고 다시 올립니다.

### [37] markdown {'lesson_part': 'after'}

## 7. 오류 처리 함수로 실행하기 (After)

### [38] markdown {'lesson_part': 'after'}

이제 결함을 고칩니다.
도구 실행 노드를 만들 때 인자 `handle_tool_errors`에 오류 처리 함수를 넘깁니다.
오류 처리 인자는 도구를 실행하다 난 오류 가운데, 무엇을 받아 도구 메시지로 바꿀지 정하는 인자입니다.
자료실로 치면 서고가 쪽지대로 찾지 못했을 때, 상자를 멈출지 빈 카드를 실어 올릴지 정하는 규칙입니다.
코드에서는 `ToolNode(tools, handle_tool_errors=handle_policy_error)` 한 줄입니다.

이 인자는 Ch 19 06절 도구 속성 `handle_tool_error`와 이름 끝 한 글자가 다릅니다.
06절의 오류 담기 설정(단수)은 도구 하나에 붙고, `ToolException`만 받았습니다.
이 절의 오류 처리 인자(복수)는 도구 실행 노드에 붙고, 받을 오류 종류를 우리가 정합니다.
이 절의 도구는 `ValueError`를 내므로, 06절의 도구 속성으로는 받을 수 없습니다.

다음 셀은 오류 처리 함수입니다.
오류 처리 함수는 도구 실행 노드가 넘긴 오류 하나를 받아, 도구 메시지에 담을 글을 내놓는 함수입니다.
첫 매개변수 뒤 `: ValueError`는 받을 오류 표시입니다.
도구 실행 노드는 이 표시를 읽고, `ValueError`일 때만 이 함수에 오류를 넘깁니다.
Ch 19 01절 `@tool` 함수의 `: str`처럼, 이 표시도 라이브러리가 읽는 값입니다.

### [39] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.410568Z', 'iopub.status.busy': '2026-09-24T06:47:23.410527Z', 'iopub.status.idle': '2026-09-24T06:47:23.412177Z', 'shell.execute_reply': '2026-09-24T06:47:23.411803Z'}, 'lesson_part': 'after'}

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

### [40] markdown {'lesson_part': 'after'}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `handle_policy_error`는 받은 오류의 글을 `str`로 꺼내 안내 글 가운데에 넣습니다.
안내 글에는 무엇이 잘못됐는지와, 이 도구로 찾을 수 있는 주제어를 함께 적었습니다.
Ch 19 06절 오류 글처럼, 모델이 읽고 다음 할 일을 정할 수 있게 하려는 것입니다.

다음 셀은 이 함수를 그래프 없이 한 번 불러, 어떤 글을 내놓는지 봅니다.
3절 도구와 같은 글을 담은 `ValueError`를 직접 만들어 넣습니다.

### [41] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.412700Z', 'iopub.status.busy': '2026-09-24T06:47:23.412654Z', 'iopub.status.idle': '2026-09-24T06:47:23.414458Z', 'shell.execute_reply': '2026-09-24T06:47:23.414140Z'}, 'lesson_part': 'after'}

```python
# 3절과 같은 글의 ValueError를 만들어, 도구 실행 노드 없이 오류 처리 함수에 넣어 봅니다
sample_error = ValueError("지원하지 않는 주제: 주차")
guide_text = handle_policy_error(sample_error)
print("내놓은 글:", guide_text)
```

출력:
```
내놓은 글: 규정을 찾지 못했습니다(지원하지 않는 주제: 주차). 이 도구로 찾을 수 있는 주제어는 대출, 운영, 연체입니다.

```

### [42] markdown {'lesson_part': 'after'}

**결과 읽기** — 라벨 `내놓은 글:` 뒤에 안내 글 한 줄이 보입니다.
괄호 안 `지원하지 않는 주제: 주차`가 오류의 글이고, 괄호 뒤 문장이 주제어 안내입니다.
도구 실행 노드는 받은 오류를 이 함수에 넣고, 내놓은 글을 도구 메시지의 내용으로 씁니다.

다음 셀은 이 함수를 넘긴 도구 실행 노드로, 같은 함수 `build_graph`로 그래프를 만듭니다.
6절과 다른 곳은 도구 실행 노드를 만드는 줄 하나뿐입니다.

### [43] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.414944Z', 'iopub.status.busy': '2026-09-24T06:47:23.414901Z', 'iopub.status.idle': '2026-09-24T06:47:23.418001Z', 'shell.execute_reply': '2026-09-24T06:47:23.417629Z'}, 'lesson_part': 'after'}

```python
# After: 오류 처리 함수를 넘긴 도구 실행 노드로, 같은 함수 build_graph로 그래프를 만듭니다
policy_node = ToolNode(tools, handle_tool_errors=handle_policy_error)
after_graph = build_graph(policy_node)
after_structure = after_graph.get_graph().draw_mermaid()
print("만든 것의 종류:", type(policy_node).__name__)
print("구조 문자열이 Before와 같은가:", after_structure == before_structure)
```

출력:
```
만든 것의 종류: ToolNode
구조 문자열이 Before와 같은가: True

```

### [44] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `만든 것의 종류: ToolNode`입니다.
출력 줄 `구조 문자열이 Before와 같은가: True`로, 그래프 모양은 Before와 같습니다.
달라진 것은 도구 실행 노드의 오류 처리 인자 하나입니다.

다음 셀은 5절의 같은 첫 상태로 After 그래프를 실행합니다.
실행 전에 예상해 봅니다.
이번에는 오류가 도구 메시지가 되어, 도구 실행 노드 다음 차례인 모델 노드로 갈 것입니다.
모델 노드를 지나면 모델 요청이 한 번 나갑니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:23.418538Z', 'iopub.status.busy': '2026-09-24T06:47:23.418494Z', 'iopub.status.idle': '2026-09-24T06:47:24.799697Z', 'shell.execute_reply': '2026-09-24T06:47:24.798960Z'}, 'lesson_part': 'after'}

```python
# After 그래프를 같은 첫 상태로 실행합니다(모델 노드를 지날 때마다 모델 요청 1번)
after_result = after_graph.invoke(park_state)
print("실행 흔적 칸:", after_result["trace"])
print("메시지 칸:")
show_messages(after_result["messages"])
```

출력:
```
실행 흔적 칸: ['model']
메시지 칸:
HumanMessage
AIMessage | 도구 호출 요청: ['lookup_policy']
ToolMessage | 결과 상태: error | 내용: 규정을 찾지 못했습니다(지원하지 않는 주제: 주차). 이 도구로 찾을 수 있는 주제어는 대출, 운영, 연체입니다.
AIMessage | 도구 호출 요청: []

```

### [46] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `실행 흔적 칸: ['model']`로 모델 노드를 한 번 지났고, 모델 요청은 1번입니다.
라벨 줄 `메시지 칸:` 아래 셋째 줄이 도구 메시지이고, 결과 상태가 `error`입니다.
그 내용은 앞에서 오류 처리 함수를 그래프 없이 불렀을 때 내놓은 글과 같습니다.
넷째 줄 `AIMessage | 도구 호출 요청: []`는 모델이 도구 메시지를 읽고 도구 없이 적은 응답입니다.
Before에서 그래프를 멈춘 같은 요청이, 이번에는 도구 메시지가 되어 모델 노드까지 갔습니다.

모델이 다시 도구를 요청할지는 모델이 정하는 값이라, 실행한 때에 따라 달라질 수 있습니다.
노트북 밖에서 같은 흐름을 다섯 번 보냈을 때는 다섯 번 모두 이 차례였습니다.

다음 셀은 셋째 메시지인 도구 메시지를 따로 봅니다.

### [47] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:24.801100Z', 'iopub.status.busy': '2026-09-24T06:47:24.800963Z', 'iopub.status.idle': '2026-09-24T06:47:24.804231Z', 'shell.execute_reply': '2026-09-24T06:47:24.803714Z'}, 'lesson_part': 'after'}

```python
# 셋째 메시지(도구 메시지)의 종류·결과 상태·호출 ID를 봅니다
error_message = after_result["messages"][2]
print("셋째 메시지의 종류:", type(error_message).__name__)
print("결과 상태:", error_message.status)
print("호출 ID:", error_message.tool_call_id)
print("요청 id와 같은가:", error_message.tool_call_id == park_call["id"])
# 두 값은 모델이 아니라 도구 실행 노드가 정하므로 매번 같아야 합니다
assert error_message.status == "error", "받은 오류는 결과 상태가 error인 도구 메시지가 되어야 합니다"
assert error_message.tool_call_id == park_call["id"], "도구 메시지에는 요청 id가 옮겨져야 합니다"
```

출력:
```
셋째 메시지의 종류: ToolMessage
결과 상태: error
호출 ID: hand_call_park
요청 id와 같은가: True

```

### [48] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `셋째 메시지의 종류: ToolMessage`와 `결과 상태: error`입니다.
출력 줄 `호출 ID: hand_call_park`는 5절 손으로 만든 요청의 id 그대로입니다.
출력 줄 `요청 id와 같은가: True`로, 도구 실행 노드가 오류 때도 호출 ID를 옮겨 적었습니다.
Ch 19 05절의 같은 색 집게처럼, 이 도구 메시지가 어느 요청의 결과인지 알려 줍니다.
두 값은 도구 실행 노드가 정하므로, 셀 끝 `assert`로 확인했습니다.

다음 셀은 메시지 칸의 마지막 응답을 봅니다.

### [49] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:24.805347Z', 'iopub.status.busy': '2026-09-24T06:47:24.805262Z', 'iopub.status.idle': '2026-09-24T06:47:24.807627Z', 'shell.execute_reply': '2026-09-24T06:47:24.807066Z'}, 'lesson_part': 'after'}

```python
# 메시지 칸의 마지막 응답을 봅니다(도구 호출 요청 수와 답 글)
last_message = after_result["messages"][-1]
print("마지막 응답의 도구 호출 요청 수:", len(last_message.tool_calls))
print("답 글:")
print(last_message.content)
```

출력:
```
마지막 응답의 도구 호출 요청 수: 0
답 글:
죄송하지만, 현재 제가 확인할 수 있는 자료실 규정은 **대출, 운영, 연체** 주제만입니다.  
**주차 규정**은 이 자료로는 찾을 수 없습니다.

원하시면 대신 아래 중 하나를 알려드릴 수 있어요:
- 자료실 **대출 규정**
- 자료실 **운영 규정**
- 자료실 **연체 규정**

```

### [50] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `마지막 응답의 도구 호출 요청 수: 0`입니다.
라벨 줄 `답 글:` 아래가 모델이 도구 메시지를 읽고 쓴 답입니다.

답 글의 문장은 실행마다 달라질 수 있어, 결론에 쓰지 않습니다.
이번 실행에서는 답 글이 주차 규정은 이 자료로는 찾을 수 없다고 적고, 대출·운영·연체 규정을 대신 권했습니다.
답 글의 별표 두 개(`**`)는 모델이 굵은 글씨를 표시하려고 붙인 기호입니다.

## 8. 값 바꿔 보기 · 인자 이름이 틀린 요청

바꿀 값은 손으로 만든 도구 호출 요청 하나입니다.
주제어 값은 맞지만, 인자 이름을 `topic` 대신 `주제`로 잘못 적은 요청으로 바꿉니다.
질문도 이 요청에 맞게 01절 7절의 대출 질문으로 둡니다.
도구 실행 노드 둘과 그래프 둘은 6·7절에서 만든 것을 그대로 씁니다.

### [51] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:24.808715Z', 'iopub.status.busy': '2026-09-24T06:47:24.808632Z', 'iopub.status.idle': '2026-09-24T06:47:24.811746Z', 'shell.execute_reply': '2026-09-24T06:47:24.811032Z'}, 'lesson_part': 'after'}

```python
# 바꿀 값: 인자 이름을 topic 대신 주제로 잘못 적은 요청을 손으로 만들어 첫 상태에 넣습니다
key_call = {"name": "lookup_policy", "args": {"주제": "대출"}, "id": "hand_call_key", "type": "tool_call"}
key_request = AIMessage(content="", tool_calls=[key_call])
key_question = "자료실에서 일반 도서를 며칠 빌릴 수 있나요?"
key_state = {"messages": [HumanMessage(content=key_question), key_request], "trace": []}
print("요청의 인자:", key_call["args"])
arg_names = list(lookup_policy.args.keys())
print("입력 형식의 인자 이름:", arg_names)
```

출력:
```
요청의 인자: {'주제': '대출'}
입력 형식의 인자 이름: ['topic']

```

### [52] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `요청의 인자: {'주제': '대출'}`입니다.
출력 줄 `입력 형식의 인자 이름: ['topic']`과 견주면, 꼭 채울 인자 `topic`이 빠졌습니다.
이 요청은 도구 몸통까지 가지 못하고, Ch 19 02절의 입력 검사에서 걸릴 것입니다.

다음 셀은 이 첫 상태로 After 그래프를 실행합니다.
도구 실행 노드는 입력 검사에서 걸린 오류를 `ToolInvocationError`라는 이름으로 감쌉니다.
이 오류는 Ch 19 06절 `ToolException`의 한 종류라, 셀은 그 이름으로 받습니다.
실행 전에 예상해 봅니다.
이 오류는 `ValueError`가 아니니, 오류 처리 함수로 가지 않고 그래프 밖으로 올라올 것입니다.

### [53] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:24.813119Z', 'iopub.status.busy': '2026-09-24T06:47:24.812995Z', 'iopub.status.idle': '2026-09-24T06:47:24.816673Z', 'shell.execute_reply': '2026-09-24T06:47:24.816250Z'}, 'lesson_part': 'after'}

```python
# 인자 이름이 틀린 요청을 After 그래프로 실행합니다(이 셀만 올라온 오류를 받아 출력합니다)
try:
    after_graph.invoke(key_state)
except ToolException as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:")
    print(error)
```

출력:
```
받은 오류: ToolInvocationError
오류 글:
Error invoking tool 'lookup_policy' with kwargs {'주제': '대출'} with error:
 topic: Field required
 Please fix the error and try again.

```

### [54] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `받은 오류: ToolInvocationError`처럼 오류가 그래프 밖 셀까지 올라왔습니다.
라벨 줄 `오류 글:` 아래 영어 글의 `topic: Field required`는 꼭 채울 인자가 없다는 뜻입니다.
7절에서 도구 메시지를 만든 같은 노드가, 요청만 바꾸자 그래프를 멈췄습니다.

이 출력은 표시가 `ValueError`인 함수를 넘긴 노드가 이 오류를 받지 않았다는 것까지 보여 줍니다.
받을 오류 표시가 받는 오류 종류를 정한다는 것은 설치판 소스와 노트북 밖 확인이 근거입니다.
표시를 뺀 함수를 넘기면 이 오류도 받았지만, 노트북에서는 실행하지 않았습니다.

다음 셀은 같은 요청을 6절 Before 그래프, 곧 기본값 도구 실행 노드로 실행합니다.
실행 전에 예상해 봅니다.
설치판 소스에서 기본값은 입력 검사에서 걸린 오류만 받아 도구 메시지로 바꿉니다.
그렇다면 이번에는 도구 메시지가 모델 노드로 가고, 모델 요청이 나갈 것입니다.

### [55] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:24.817689Z', 'iopub.status.busy': '2026-09-24T06:47:24.817612Z', 'iopub.status.idle': '2026-09-24T06:47:26.603897Z', 'shell.execute_reply': '2026-09-24T06:47:26.603106Z'}, 'lesson_part': 'after'}

```python
# 같은 요청을 Before 그래프, 곧 기본값 도구 실행 노드로 실행합니다(모델 요청이 나갑니다)
key_result = before_graph.invoke(key_state)
print("실행 흔적 칸:", key_result["trace"])
print("메시지 칸:")
show_messages(key_result["messages"])
```

출력:
```
실행 흔적 칸: ['model', 'model']
메시지 칸:
HumanMessage
AIMessage | 도구 호출 요청: ['lookup_policy']
ToolMessage | 결과 상태: error | 내용: Error invoking tool 'lookup_policy' with kwargs {'주제': '대출'} with error:
 topic: Field required
 Please fix the error and try again.
AIMessage | 도구 호출 요청: ['lookup_policy']
ToolMessage | 결과 상태: success | 내용: 일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.
AIMessage | 도구 호출 요청: []

```

### [56] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `실행 흔적 칸: ['model', 'model']`로 모델 노드를 두 번 지났습니다.
라벨 줄 `메시지 칸:` 아래 첫 도구 메시지는 결과 상태가 `error`입니다.
그 내용은 앞 셀과 같은 영어 오류 글입니다.
둘째 도구 메시지는 결과 상태가 `success`이고, 마지막 줄 `AIMessage | 도구 호출 요청: []`로 끝났습니다.
Before에서 `ValueError`로 멈춘 기본값 노드가, 입력 검사에서 걸린 오류는 도구 메시지로 바꿨습니다.

Ch 19 07절은 설치판 소스로 「값 검사 오류는 흐름을 멈춘다」고 적었습니다.
그것은 우리가 쓴 `for` 루프와 도구 속성 이야기이고, 도구 실행 노드의 기본값은 다르게 움직입니다.

다음 셀은 첫 도구 메시지와, 그 뒤 응답이 다시 보낸 요청을 봅니다.

### [57] code {'execution': {'iopub.execute_input': '2026-09-24T06:47:26.605339Z', 'iopub.status.busy': '2026-09-24T06:47:26.605201Z', 'iopub.status.idle': '2026-09-24T06:47:26.609079Z', 'shell.execute_reply': '2026-09-24T06:47:26.608304Z'}, 'lesson_part': 'after'}

```python
# 셋째 메시지(첫 도구 메시지)의 결과 상태·호출 ID와, 넷째 메시지(응답)의 도구 호출 요청을 봅니다
key_error = key_result["messages"][2]
print("셋째 메시지의 결과 상태:", key_error.status)
print("요청 id와 같은가:", key_error.tool_call_id == key_call["id"])
retry_response = key_result["messages"][3]
for call in retry_response.tool_calls:
    print("넷째 메시지가 다시 보낸 요청의 인자:", call["args"])
# 결과 상태는 도구 실행 노드가 정하는 값이라 매번 같아야 합니다
assert key_error.status == "error", "입력 검사에서 걸린 오류도 결과 상태가 error인 도구 메시지가 되어야 합니다"
```

출력:
```
셋째 메시지의 결과 상태: error
요청 id와 같은가: True
넷째 메시지가 다시 보낸 요청의 인자: {'topic': '대출'}

```

### [58] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `셋째 메시지의 결과 상태: error`와 `요청 id와 같은가: True`입니다.
기본값 노드도 오류를 담은 도구 메시지에 요청 id를 옮겨 적었습니다.
출력 줄 `넷째 메시지가 다시 보낸 요청의 인자: {'topic': '대출'}`로, 모델이 인자 이름을 고쳤습니다.
셀 끝 `assert`는 도구 실행 노드가 정하는 결과 상태에만 걸었습니다.

인자 이름을 고쳐 다시 요청한 것은 모델이 정한 일이라, 실행한 때에 따라 달라질 수 있습니다.
노트북 밖에서 같은 흐름을 다섯 번 보냈을 때도, 다섯 번 모두 인자 이름을 `topic`으로 고쳐 다시 요청했습니다.

## 9. 네 실행 견주기

같은 그래프에 요청 둘과 도구 실행 노드 설정 둘을 넣은 네 실행은 아래와 같았습니다.

- 주차 요청과 기본값 노드(Before)는 `ValueError`로 멈췄고, 모델 요청은 없었습니다.
- 주차 요청과 오류 처리 함수 노드(After)는 결과 상태 `error`인 도구 메시지를 만들고, 모델 요청이 1번이었습니다.
- 인자 이름이 틀린 요청과 오류 처리 함수 노드는 `ToolInvocationError`로 멈췄습니다.
- 인자 이름이 틀린 요청과 기본값 노드는 도구 메시지를 만들고, 모델 요청이 2번이었습니다.

## 정리

1. 도구 실행 노드의 기본값은 도구가 낸 `ValueError`를 그대로 올려, 그래프 실행이 멈췄습니다.
2. 오류 처리 함수를 넘기자 같은 오류가 결과 상태 `error`인 도구 메시지가 되어 모델 노드로 갔습니다.
3. 받을 오류 표시 `ValueError`에 맞지 않는 입력 검사 오류는 오류 처리 함수로 가지 않았습니다.

03절에서는 그래프가 도구 쪽을 되풀이하는 횟수의 한도와, 흐름을 끝내는 조건을 봅니다.

## 그림

### 02-1-받을-오류와-두-갈래.mmd

```mermaid
flowchart TB
  %% classes
  r["손으로 만든 도구 호출 요청<br>lookup_policy<br>주제어 주차"]:::tool
  n["도구 실행 노드 tools<br>도구를 실행"]
  ok["도구 메시지<br>결과 상태 success"]
  h["오류 처리 인자가<br>받을 오류인지 정함"]
  msg["도구 메시지 · 결과 상태 error<br>내용은 오류 처리 함수의 글<br>호출 ID는 요청 id 그대로"]:::measure
  stop["오류가 그래프 밖으로 올라와<br>실행이 멈춤"]:::fail
  r --> n
  n -.->|오류 없음| ok
  n -.->|오류가 남| h
  h -.->|받음| msg
  h -.->|받지 않음| stop
```

도구가 오류를 내면 오류 처리 인자가 받을지 정하고, 받으면 도구 메시지가 되며 받지 않으면 실행이 멈춥니다.

### 02-2-시작-엣지를-옮긴-그래프.mmd

```mermaid
flowchart TB
  %% classes
  q["첫 상태<br>질문 하나<br>손으로 만든 응답 하나<br>흔적 빈 목록"]:::tool
  s(["가상 시작점 START"])
  t["도구 실행 노드 tools<br>ToolNode<br>설정만 바꿔 끼움"]
  m["모델 노드 model<br>함수 call_model"]:::flow
  e(["가상 끝점 END"])
  q -->|invoke| s
  s -->|옮긴 시작 엣지| t
  t --> m
  m -.->|도구 호출 요청 있음<br>이름표 tools| t
  m -.->|도구 호출 요청 없음<br>이름표 END| e
```

01절 그래프에서 시작 엣지만 도구 실행 노드로 옮겨, 첫 상태에 넣은 요청부터 실행합니다.

### 02-3-기본값과-오류-처리-함수.mmd

```mermaid
flowchart TB
  %% classes
  q["같은 첫 상태 · 주차 질문<br>손으로 만든 요청 lookup_policy 주차<br>id hand_call_park"]:::tool
  subgraph B["Before · ToolNode tools 기본값"]
    direction TB
    b1["ValueError<br>지원하지 않는 주제: 주차"]:::fail
    b2["그래프 실행이 멈춤<br>도구 메시지 없음<br>모델 요청 없음"]:::fail
    b1 --> b2
  end
  subgraph A["After · 오류 처리 함수 handle_policy_error"]
    direction TB
    a1["도구 메시지 결과 상태 error<br>호출 ID hand_call_park"]:::measure
    a2["모델 요청 한 번<br>gpt-5.4-mini"]:::model
    a3["마지막 응답<br>도구 호출 요청 0건"]:::measure
    a1 --> a2
    a2 --> a3
  end
  q --> B
  q --> A
```

같은 요청에서 기본값 노드는 ValueError로 멈췄고, 오류 처리 함수를 넘긴 노드는 도구 메시지를 모델 노드로 보냈습니다.

### 02-4-받을-오류-표시가-가른-요청.mmd

```mermaid
flowchart TB
  %% classes
  subgraph D["기본값 ToolNode tools"]
    direction TB
    d1["주차 요청<br>ValueError로 멈춤"]:::fail
    d2["인자 이름이 틀린 요청<br>도구 메시지 error<br>모델이 topic 대출로<br>다시 요청"]:::measure
    d1 ~~~ d2
  end
  subgraph P["오류 처리 함수 · 받을 오류 표시 ValueError"]
    direction TB
    p1["주차 요청<br>도구 메시지 error"]:::measure
    p2["인자 이름이 틀린 요청<br>ToolInvocationError로 멈춤"]:::measure
    p1 ~~~ p2
  end
  same["노드가 감싼<br>ToolInvocationError는<br>ValueError가 아님<br>두 요청에서 받은 오류가<br>서로 엇갈림"]
  D ~~~ same
  P ~~~ same
```

받을 오류 표시가 ValueError인 함수를 넘긴 노드는 입력 검사 오류를 받지 않아, 이 두 요청에서 두 설정이 받은 오류가 엇갈렸습니다.

### 02-5-빈-카드를-싣고-온-상자.prompt.md

# 02-5-빈-카드를-싣고-온-상자 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 사서가 주차 규정을 찾아 달라는 쪽지를 상자에 넣어 서고로 내려보냈습니다. 그런데 서고에는 주차 규정 카드가 없습니다. 서고가 일을 멈추고 상자를 붙들어 두면, 창구의 사서는 아무 소식도 받지 못합니다. … 찾지 못한 까닭을 빈 카드에 적어, 상자에 싣고 올려 보내는 규칙입니다.

구성 요소와 배치: 01-5와 같은 두 층 자료실 벽(크림색, 다른 구멍 없음). 위층 **긴 나무 창구 하나**(위는 비어 있음 = 모델 노드), 아래층 **파란 책 책장 하나와 눈에 띄는 빈칸**(= 찾는 주제가 자료에 없음). 벽 속 **같은 모양 승강 통로 둘**. **왼쪽 상자는 아래층에 머물고 흰 쪽지만 반쯤 삐져나옴**(= Before, 도구 실행 노드에서 멈춘 실행 — 도구 메시지가 올라오지 않음). **오른쪽 상자는 창구 높이까지 올라왔고 아무것도 적히지 않은 옅은 회색 카드가 반쯤 삐져나옴**(= After, 결과 상태 error인 도구 메시지). 사람·손·화살표·화면·끈·톱니·쟁반·서랍·바구니 없음. 1차에서 넣었던 같은 색 집게 둘은 2차에서 뺐습니다(아래 상태).

시선 순서: 위층 창구 → 두 통로 → 아래에 머문 왼쪽 상자의 쪽지 → 위로 올라온 오른쪽 상자의 빈 카드 → 책장의 빈칸.

검수 기준: 그림만 보고 「통로와 상자는 둘이다」, 「왼쪽 상자는 아래층에 쪽지만 든 채 머물러 있다」, 「오른쪽 상자는 책이 아닌 빈 카드를 싣고 위층으로 올라왔다」가 읽히는가. 카드와 쪽지가 상자 안(반쯤 삐져나온 모양)에 있는가. 글자·숫자·사람이 없는가.

비유 계열: 챕터 리드 결정 9 「자료실 승강 상자」(01절이 엶). 호출 ID는 본문에서만 Ch 19 05절 「같은 색 집게」로 잇고 그림에는 넣지 않았습니다.

## 프롬프트 1차 (탈락)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. Cutaway front view of a two-floor library wall, plain cream with no other opening. Upper floor: one long wooden service counter. Lower floor: one bookshelf with blue books and one clearly empty gap on its middle shelf. Two identical narrow dumbwaiter shafts run straight down through the wall side by side. Left shaft: its small wooden box stays down at the lower floor next to the shelf, holding only one white folded paper slip sticking halfway out, nothing else. Right shaft: its identical small wooden box has come up to the counter, holding one white folded paper slip and one blank pale gray card standing upright, no book; exactly two small orange clips, one on that slip and one on that card. The two boxes are large and easy to see. No people, no hands, no arrows, no screens, no ropes, no gears, no trays, no drawers, no baskets.
```

## 프롬프트 2차 (채택)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. Cutaway front view of a two-floor library wall, plain cream with no other opening. Upper floor: one long wooden service counter with a completely empty top. Lower floor: one bookshelf with blue books and one clearly empty gap on its middle shelf. Two identical dumbwaiter shafts run straight down through the wall side by side. Each shaft holds one large wooden box, easy to see. Left box: stays down at the lower floor, with one white folded paper slip sticking halfway out of it, nothing else. Right box: has come up level with the counter, with one blank pale gray card clearly sticking halfway out of it, no book. No clips, no people, no hands, no arrows, no screens, no ropes, no gears, no trays, no drawers, no baskets.
```

## 상태

- 2026-09-24 · `nano_banana_pro`(`jobs_wait` 응답 모델 이름 `nano_banana_2` — 01-5와 같은 표시) · 16:9 · 2k · `use_unlim: false` · count 1. 생성 전 잔액 **2545.25**, 생성 뒤 **2541.25**.
- **1차 job `c45f175b-d0d2-4be1-8721-7953b16defa8` 탈락**(원본 `fb814928…`, 2752 × 1536, 기기 `/tmp/ch20-02/illu-1-orig.png`): 오른쪽 상자는 올라왔지만 **빈 카드와 쪽지 하나가 상자 밖 창구 위에 놓였고**, 상자 안에도 쪽지가 하나 더 있어 쪽지가 둘·주황 집게가 **셋**이 됨 → 「상자가 빈 카드를 싣고 올라왔다」가 읽히지 않고 집게 짝도 흐려짐. 상자도 작게 그려짐.
- **2차 job `c218209a-3502-4399-98cc-3f2d7e116eea` 채택**(재생성 1회 상한 — 여기서 끝). 창구 위를 비우라고 적고 집게를 빼고, 카드가 상자에서 반쯤 삐져나오게 적었습니다. 거래 기록 **2026-09-24T06:49:17Z · 06:50:29Z 「Nano Banana Pro −2」 두 줄 = 이 절 몫 4크레딧**(결과 파일 이름 `hf_20260924_064917_c45f175b…`·`hf_20260924_065029_c218209a…`와 시각이 같음, 바로 앞 거래 06:18:31Z는 01절 몫).
- **그림에서 확인한 것(그림 읽기·alt·캡션에 반영)**: 두 층을 잘라 보인 크림색 벽. 위층 가운데 긴 나무 창구 **하나**(위가 비어 있음). 아래층 가운데 나무 책장 **하나**, 칸 **셋** 모두 가운데가 비어 있고 파란 책은 양 끝에만 꽂힘(요청한 「가운데 칸 한 곳의 빈칸」보다 넓게 그려짐 — 「찾는 것이 없다」 판독에는 도움). 벽 속 왼쪽·오른쪽에 회색 승강 통로 **둘**. **왼쪽 통로의 나무 상자 하나는 아래층 바닥에 있고, 위 틈으로 흰 쪽지 한 장이 비스듬히 반쯤 삐져나옴**. **오른쪽 통로의 같은 모양 나무 상자 하나는 위층 바닥 높이, 창구 오른쪽 옆에 있고, 위 틈으로 아무것도 적히지 않은 옅은 회색 네모 카드 한 장이 반쯤 삐져나옴**. 상자 위에 틈이 난 모양이라 투표함처럼 보일 수 있음(강사 확인). 글자·숫자·사람·손·화살표·집게·끈·톱니·화면 없음.
- 저장: 기기 셸에서 결과 URL을 `curl`로 받아 `UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pillow`로 RGB·폭 1100px(LANCZOS)로 줄여 `figures/02-5-빈-카드를-싣고-온-상자.png`(1100 × 614, `9e3a716eceac39d06bba74f1db357a61d923e772b37df419f2bf56ca9650a1aa`)로 저장했습니다. 채택 원본 `f52bc44e96616baac688feafa1195a43fad5ba0eac85cfc8c444f279b648b327`(2752 × 1536)은 기기 `/tmp/ch20-02/illu-2-orig.png`에만 있습니다.
- 결과 URL을 다시 받아(`illu-2-again.png`, 같은 해시) 같은 폭으로 줄인 그림과 저장 PNG를 픽셀 대조했습니다(`ImageChops.difference` bbox `None`, 최대 차이 0). 저장 PNG와 두 상자 확대본(`.cache/ch20-02-view/saved-02-5-right.png`·`saved-02-5-left.png`)을 직접 열어 그림 읽기를 썼습니다.

