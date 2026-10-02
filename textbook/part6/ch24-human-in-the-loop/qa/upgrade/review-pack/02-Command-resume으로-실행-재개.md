# 02-Command-resume으로-실행-재개

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 1h | 실습 1.5h | 코드 notebooks/02-Command-resume으로-실행-재개.ipynb | 새 용어 2 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>허용 답 목록으로 사람의 답을 검사하고, 목록에 없는 답이면 조건부 엣지로 같은 자리에서 다시 물을 수 있습니다.</li>
<li>노드 안 <code>while True</code>로 다시 묻는 모양과 견주어, 부른 횟수와 체크포인트 수가 어떻게 다른지 설명할 수 있습니다.</li>
<li>체크포인터가 없거나 스레드 이름이 다를 때, 사람의 답을 넘기면 받는 오류를 읽을 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>사람이 늘 정해 둔 답만 보내지는 않습니다. 승인 화면에 <code>approve</code>와 <code>reject</code>를 적어 두어도, <code>maybe</code>나 <code>yes</code> 같은 글이 올 수 있습니다. 이런 답을 승인으로 여기거나 실행을 버리면, 사람에게 확인을 받은 뜻이 없어집니다. 그래서 받은 답을 검사하고, 목록에 없는 답이면 까닭을 알려 준 뒤 같은 자리에서 다시 묻습니다.</p><p>다시 묻는 코드는 노드 안의 반복문으로도, 조건부 엣지로도 만들 수 있습니다. 공식 문서는 반복문 모양을 쓰지 말고 조건부 엣지를 쓰라고 적습니다. 이 절은 두 모양에 같은 답을 차례로 넣고, 노드가 몇 번 시작했는지와 체크포인트 수를 세어 그 까닭을 봅니다. 절 제목은 <a href="01-interrupt-승인-게이트.html">01절</a>의 <code>Command(resume=…)</code>로 멈춘 실행을 이어 가는 일을 가리킵니다. 본문에서는 01절처럼 사람의 답으로 이어 가기라고 씁니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href="01-interrupt-승인-게이트.html">01절</a>에서는 노드 안에서 함수 <code>interrupt</code>를 부르자 그래프가 멈추고, 결과의 키 <code>__interrupt__</code>에 질문 값이 남았습니다. 사람의 답을 <code>Command(resume=…)</code>에 담아 이어 가자, 노드는 멈춘 줄이 아니라 첫 줄부터 다시 실행되었습니다. 01절의 After 노드는 <code>approve</code>가 아닌 답을 모두 쓰지 않는 쪽으로 다루었고, 다른 글은 넣어 보지 않았습니다. 이 절은 01절이 남긴 그 자리, 허용하지 않는 답을 다룹니다.</p><p><a href="../../part4/ch13-langgraph-basics/03-조건부-엣지.html">Ch 13 03절</a>에서는 조건 함수가 상태를 읽어 이름표를 내놓고, 이름표 표 <code>path_map</code>이 이름표를 다음 노드에 이었습니다. <a href="../../part5/ch20-tool-node/03-recursion-limit과-명시적-종료.html">Ch 20 03절</a>에서는 조건 함수가 끝점 <code>END</code>를 내놓아 반복을 끝냈습니다. <a href="../../part5/ch20-tool-node/01-ToolNode와-tools-condition.html">Ch 20 01절</a>의 되돌아가는 엣지는 도구 노드에서 모델 노드로 갔고, 이 절의 조건부 엣지는 같은 노드로 되돌아갑니다. 체크포인트 수와 <code>get_state_history</code>는 <a href="../ch23-persistence/01-체크포인터와-스레드.html">Ch 23 01절</a>에서 보았습니다. 실패한 작업의 오류를 읽는 속성 <code>tasks</code>는 <a href="../ch23-persistence/05-pending-writes와-장애-복구.html">Ch 23 05절</a>에서 보았습니다.</p><p><a href="../../part4/ch16-guardrails/01-입출력-출처-검증.html">Ch 16 01절</a>은 출처 표시의 허용 목록을, <a href="../../part5/ch18-workflow-patterns/02-실패를-처리하는-라우팅.html">Ch 18 02절</a>은 보내도 되는 종류 이름의 허용 목록을 만들었습니다. 이 절의 허용 답 목록도 같은 뜻의 허용 목록이고, 받아들일 사람의 답을 적습니다. Ch 18 02절의 되묻기는 검사를 지나지 못한 문의에 답하지 않고 흐름을 끝냈습니다. 이 절의 다시 묻기는 흐름을 끝내지 않고, 멈춘 그래프가 같은 자리에서 다시 멈춥니다.</p><p>오류를 받아 출력하는 셀은 <a href="../../part1/ch02-python/05-파일과-예외.html">Ch 2 05절</a>처럼 <code>try</code>와 <code>except 오류이름 as error</code>로 감쌉니다. 이 절은 파일을 쓰지 않아, 도구 파일 <code>approval_tools.py</code>에서 가져오는 함수는 없습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절의 도미노 줄을 다시 봅니다. 가운데 비워 둔 자리에 사람이 도미노가 아닌 둥근 구슬을 놓았다고 합시다. 구슬은 뒤쪽 도미노를 밀지 못해, 줄은 빈자리에서 그대로 멈춰 있습니다. 이때 구슬을 치우고 무엇이 맞지 않았는지 알려 준 뒤, 맞는 도미노를 다시 기다립니다.</p><p>빈자리에 맞는 도미노의 모양이 허용 답 목록이고, 구슬을 치우고 다시 기다리는 일이 다시 묻기입니다. 맞는 도미노가 놓여야 뒤쪽 줄이 넘어가는 것은 01절과 같습니다.</p>
{{img:02-6-빈자리에-놓인-구슬과-도미노|흰 바탕에 흰 탁자 하나를 조금 위에서 본 그림입니다. 탁자 위에 나무 도미노 두 줄이 위아래로 놓였습니다. 위 줄은 왼쪽 도미노가 넘어져 있고, 가운데 빈자리에 파란 구슬 하나가 놓였으며, 구슬 오른쪽 도미노는 모두 서 있습니다. 아래 줄은 가운데에 연두색 도미노 하나가 누워 있고, 그 양쪽 도미노까지 줄 전체가 오른쪽 끝까지 넘어져 있습니다. 글자·숫자·사람·손은 없는 그림|빈자리에 구슬이 놓인 위 줄은 그대로 멈춰 있고, 맞는 도미노가 놓인 아래 줄은 끝까지 넘어갔습니다.}}
<p class="look"><b>그림 읽기</b> — 흰 탁자 위에 도미노 두 줄이 위아래로 있습니다. 위 줄은 빈자리에 파란 구슬이 놓여, 구슬 오른쪽 도미노가 모두 서 있습니다. 아래 줄은 빈자리에 연두색 도미노가 놓여, 오른쪽 끝까지 모두 넘어졌습니다. 구슬이 허용 답 목록에 없는 답(<code>maybe</code>), 연두색 도미노가 목록에 있는 답(<code>approve</code>)입니다. 도미노의 개수와 탁자 다리는 무엇과도 짝짓지 않습니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>허용 답 목록</td><td>사람의 답으로 받아들일 값만 적어 둔 목록입니다. 도미노 줄의 빈자리에 맞는 도미노 모양을 정해 두는 것과 같습니다. 이 절에서는 목록 <code>allowed_answers</code>이고, 받은 답이 목록에 있는지 <code>in</code>으로 검사합니다. Ch 16 01절·Ch 18 02절의 허용 목록과 같은 뜻이라 새 말로 세지 않습니다.</td></tr><tr><td>다시 묻기</td><td>받아들이지 않는 답이 오면, 까닭을 질문 값에 담아 같은 자리에서 한 번 더 멈추는 일입니다. 빈자리의 구슬을 치우고, 맞는 도미노를 다시 기다리는 것과 같습니다. 이 절에서는 노드가 칸 <code>error</code>에 까닭을 적고, 조건부 엣지가 같은 노드로 되돌아갑니다. 흐름을 끝내고 되묻던 Ch 18 02절의 되묻기와 달리, 멈춘 자리에서 다시 멈춥니다.</td></tr><tr><td>차례 맞추기</td><td>한 노드 안에서 함수 <code>interrupt</code>를 여러 번 부를 때, 받은 답을 부른 차례대로 맞추는 일입니다. 도미노 줄을 처음부터 다시 세울 때, 전에 놓았던 물건을 같은 자리에 차례대로 다시 놓는 것과 같습니다. 이 절에서는 권하지 않는 모양 <code>ask_in_loop</code>이 이어 갈 때마다 앞선 답을 차례대로 다시 받습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 허용 답 목록은 노트북 2절 출력 <code>허용 답 목록: ['approve', 'reject']</code>입니다. 다시 묻기는 3절에서 <code>maybe</code>로 이어 간 셀이고, 질문 값 끝에 <code>'error': '허용하지 않는 값: maybe'</code>가 실렸습니다. 차례 맞추기는 4절 <code>yes</code> 셀에서 한 번 시작한 노드가 <code>interrupt</code>를 세 번 부른 모습입니다.</p>
{{mermaid:02-1-조건부-엣지로-다시-묻는-그래프|위에서 아래로 읽는 그림입니다. 맨 위에 회색 둥근 상자 가상 시작점 START, 초록 상자 허용 답 목록 approve reject, 초록 상자 사람의 답 Command resume으로 넘김이 나란히 놓이고, 셋에서 파란 상자 노드 ask_once로 화살표가 갑니다. 파란 상자에는 interrupt를 한 번 부르고 받은 답을 목록으로 검사가 적혀 있고, 그 아래 회색 마름모 조건 함수 after_answer로 화살표가 갑니다. 마름모에서 나가는 점선 둘 가운데 하나는 오류 칸에 글 있음 이름표 ask_again으로 파란 상자에 되돌아가고, 다른 하나는 오류 칸 빈 글 이름표 END로 맨 아래 회색 둥근 상자 가상 끝점 END에 닿는 그림|노드는 interrupt를 한 번만 부르고 마치며, 오류 칸에 글이 있으면 조건부 엣지가 같은 노드로 되돌아가 다시 묻습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 초록 상자는 우리가 넣은 값과 사람의 답이고, 파란 상자는 우리가 적은 노드입니다. 회색 마름모는 노드로 등록하지 않는 조건 함수 <code>after_answer</code>이고, 마름모에서 나가는 점선 둘이 조건부 엣지입니다. 오류 칸에 글이 있으면 같은 노드로 되돌아가 다시 묻고, 빈 글이면 끝점으로 갑니다.</p>
<h3>다시 묻기를 조건부 엣지로 만드는 까닭</h3><p>공식 문서의 멈춤 표시 규칙은 <code>interrupt</code>를 실행마다 같지 않을 수 있는 반복문으로 되풀이해 부르지 말라고 적습니다. 답을 검사하는 <code>while True</code> 반복문도 여기에 든다고 적고, 대신 조건부 엣지를 쓰라고 적습니다. 권하는 모양은 노드에서 <code>interrupt</code>를 한 번만 부르고, 오류 글은 상태에 담아 노드를 마치는 것입니다. 그다음 조건부 엣지로 노드에 되돌아가, 받아들일 답이 올 때까지 묻습니다.</p><p>까닭은 01절에서 본 성질에 있습니다. 이어 갈 때 노드는 첫 줄부터 다시 실행되고, 노드 안 <code>interrupt</code>가 여럿이면 받은 답을 부른 차례대로 맞춥니다. 설치판 소스 <code>langgraph/types.py</code> 864~868행이 이 두 가지를 적습니다. 그래서 반복문 모양은 다시 물을 때마다 앞선 바퀴를 모두 다시 실행해, 앞선 답을 차례대로 다시 받습니다. 공식 문서도 첫째 이어 가기는 한 바퀴를, 둘째는 두 바퀴를 다시 실행한다고 적습니다.</p>
<h3>다른 상황에 적용</h3><p>승인 말고도 배송 방법 고르기나 분류 고르기처럼, 사람이 정해 둔 값 가운데 하나를 골라야 하는 자리에 같은 모양을 씁니다. 허용 답 목록만 바꾸면 됩니다. 사람이 쓴 글을 그대로 명령으로 쓰지 않고, 목록으로 검사한 값만 칸에 냅니다. 이 절은 글로 된 답만 검사했고, 딕셔너리 같은 답은 넣어 보지 않았습니다.</p>
<h3>비교와 경계</h3><p>01절의 After 노드는 답을 검사하지 않고, <code>approve</code>일 때만 결제 기록을 적었습니다. 이 절은 답을 목록으로 검사하고, 목록에 없으면 다시 묻습니다. <a href="../../part5/ch17-agent-overview/03-모델-도구-루프와-정지-조건.html">Ch 17 03절</a>의 사람 확인은 멈추고 사람에게 넘길 뿐이었습니다. 이 절은 멈춘 실행을 이어 가며, 받아들일 답이 올 때까지 다시 묻습니다. 지난 체크포인트로 돌아가 다시 실행하는 일은 <a href="03-상태-기록과-다른-분기-재실행.html">03절</a>에서 다룹니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 허용 답 목록과 상태 형식, 질문 값을 만드는 함수를 준비합니다. 3절은 조건부 엣지로 다시 묻는 그래프에 답 <code>maybe</code>·<code>yes</code>·<code>approve</code>를 차례로 넣고, 답마다 세 횟수를 셉니다. 4절은 같은 답을 노드 안 <code>while True</code> 모양에 넣어 견줍니다. 6절은 사람의 답이 멈춘 질문에 닿지 않는 오류 둘을 봅니다.</p><p>이 절은 모델을 부르지 않아 모델 요청은 0번이고, API 키 셀도 없습니다. 사람의 답도 셀에 적은 값이라, 같은 입력에 늘 같은 출력이 나옵니다. 실제 서비스라면 질문 값을 화면에 띄우고, 사람이 고른 답을 같은 자리에 넣습니다. 체크포인트는 메모리에만 저장해, 파일은 하나도 쓰지 않습니다.</p>
{{notebook:02-Command-resume으로-실행-재개}}
<p class="look"><b>확인할 점</b> — 노트북 3절에서 <code>maybe</code>로 이어 간 셀의 질문 값 끝에 <code>'error': '허용하지 않는 값: maybe'</code>가 실렸는지 봅니다. 같은 셀의 <code>노드가 시작한 횟수: 3</code>과 <code>체크포인트 수: 3</code>도 확인합니다. <code>approve</code> 셀에서 <code>다음에 실행할 노드: ()</code>와 <code>체크포인트 수: 5</code>가 나오는지 봅니다.</p>
{{mermaid:02-2-답마다-본-질문-값과-체크포인트|위에서 아래로 상자 일곱이 한 줄로 이어진 그림입니다. 노란 상자 첫 실행 질문 값 오류 글 빈 글 주문 키 order-2402 체크포인트 둘, 초록 상자 사람의 답 maybe, 노란 상자 다음 질문 값 오류 글 허용하지 않는 값 maybe 노드 두 번 시작 체크포인트 셋이 차례로 있습니다. 그 아래 초록 상자 사람의 답 yes, 노란 상자 다음 질문 값 오류 글 허용하지 않는 값 yes 노드 두 번 시작 체크포인트 넷이 있습니다. 맨 아래는 초록 상자 사람의 답 approve와 노란 상자 칸 answer approve 다음 노드 없음 체크포인트 다섯인 그림|목록에 없는 답마다 오류 글이 실린 질문으로 다시 멈췄고, 체크포인트는 답마다 하나씩 늘었습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 한 줄로 읽습니다. 초록 상자는 셀에 적어 넣은 사람의 답이고, 노란 상자는 노트북 3절에서 그 답 다음에 출력된 값입니다. 목록에 없는 답을 넣은 두 셀에서는 노드가 두 번씩 시작했고, 체크포인트가 하나씩 늘었습니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>노트북 5절은 두 모양에 같은 답을 같은 차례로 넣고, 답마다 센 세 값을 모았습니다. 아래 표의 세 수는 차례대로 노드가 시작한 횟수, <code>interrupt</code>를 부른 횟수, 체크포인트 수입니다. 모두 그 셀까지 쌓인 수입니다.</p>
<table><thead><tr><th>답</th><th>조건부 엣지 모양(시작 · 부름 · 체크포인트)</th><th><code>while True</code> 모양(시작 · 부름 · 체크포인트)</th></tr></thead><tbody><tr><td>첫 실행</td><td>1 · 1 · 2</td><td>1 · 1 · 2</td></tr><tr><td><code>maybe</code></td><td>3 · 3 · 3</td><td>2 · 3 · 2</td></tr><tr><td><code>yes</code></td><td>5 · 5 · 4</td><td>3 · 6 · 2</td></tr><tr><td><code>approve</code></td><td>6 · 6 · 5</td><td>4 · 9 · 3</td></tr></tbody></table>
<p>두 모양 모두 사람에게 같은 질문 값을 보였고, 마지막 결과도 같았습니다. 달랐던 것은 노드가 시작한 횟수와 <code>interrupt</code>를 부른 횟수, 체크포인트 수입니다. 조건부 엣지 모양은 노드가 한 번 시작할 때마다 한 번만 불렀고, 답마다 체크포인트가 하나씩 늘었습니다. 반복문 모양은 노드가 끝나지 않아 체크포인트가 <code>2</code>에 머물렀고, 부른 횟수가 <code>1</code>·<code>3</code>·<code>6</code>·<code>9</code>로 쌓였습니다.</p>
{{mermaid:02-3-while-True-노드가-앞선-답을-다시-받는-차례|위에서 아래로 상자 여섯이 한 줄로 이어진 그림입니다. 파란 상자 Command resume=approve 스레드 loop로 invoke, 파란 상자 노드 ask_in_loop를 처음부터 다시 실행이 차례로 있습니다. 그 아래 회색 상자 둘은 첫째 interrupt 소스 확인 앞선 답 maybe를 다시 받음, 둘째 interrupt 소스 확인 앞선 답 yes를 다시 받음입니다. 그다음 노란 상자 셋째 interrupt 새 답 approve를 받아 노드가 끝남, 맨 아래 노란 상자 이 셀에서 부른 횟수 셋 누적 아홉 체크포인트 셋인 그림|while True 모양은 이어 갈 때마다 노드를 처음부터 다시 실행했고, 소스 설명대로라면 앞선 답을 부른 차례대로 다시 받습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 파란 상자는 우리가 부른 줄과 노드이고, 노란 상자는 노트북 4절 <code>approve</code> 셀의 출력입니다. 회색 상자 둘은 셀 출력에 따로 찍지 않은 값입니다. 설치판 소스 <code>types.py</code> 866~868행의 설명(부른 차례대로 답을 맞춤)으로 적었습니다. 이 셀에서 부른 횟수가 셋이고 마지막에 <code>approve</code>를 받았으므로, 앞의 두 부름이 앞선 답 둘을 받은 자리입니다.</p>
<p>반복문 모양에서 셀마다 늘어난 부름은 둘·셋·셋이었습니다. 노드가 처음부터 다시 실행되어, 반복문도 첫 바퀴부터 다시 돌았기 때문입니다. 설치판 설명(<code>types.py</code> 866~868행)대로라면 앞선 바퀴의 <code>interrupt</code>는 멈추지 않고, 전에 받은 답을 차례대로 다시 내놓습니다. 그러면 <code>approve</code> 셀의 세 부름 가운데 둘은 앞선 답을 다시 받은 부름입니다. 부름마다 받은 값은 셀에 찍지 않았습니다.</p><p>조건부 엣지 모양에서는 목록에 없는 답 하나에 노드가 두 번 시작했습니다. 한 번은 멈춘 노드가 다시 실행되어 답을 받고 마친 것이고, 한 번은 조건부 엣지로 새로 실행되어 멈춘 것입니다. 노드 안에서 <code>interrupt</code>를 한 번만 부르니, 앞선 답을 다시 받는 부름은 없습니다. 노드가 오류 글을 내고 마칠 때마다 체크포인트가 하나씩 늘었습니다.</p><p>노드가 시작한 횟수만 보면 조건부 엣지 모양이 <code>6</code>번으로, 반복문 모양의 <code>4</code>번보다 많습니다. 목록 밖 답마다 노드를 마치고 새로 시작해, 답 하나에 늘 두 번씩 늘었기 때문입니다. 이 절의 출력으로 보면, 조건부 엣지를 권하는 까닭은 시작 수가 아니라 <code>interrupt</code>를 부른 수에 있습니다.</p><p>부른 수는 조건부 엣지 모양이 <code>1</code>·<code>3</code>·<code>5</code>·<code>6</code>, 반복문 모양이 <code>1</code>·<code>3</code>·<code>6</code>·<code>9</code>였습니다. 반복문 모양은 이어 갈 때마다 앞선 바퀴를 다시 돌아, 목록 밖 답이 쌓일수록 한 셀의 부름이 커집니다. 부른 수를 센 줄은 함수 <code>interrupt</code> 바로 앞 줄이라, 그 줄도 9번과 6번 실행되었습니다. 01절처럼 그 자리에 쓰기가 있으면 두 모양 모두 되풀이되고, 반복문 모양에서 더 많이 되풀이됩니다.</p>
{{mermaid:02-4-두-모양의-부른-횟수와-체크포인트|위에 회색 상자 하나가 있고 아래에 칸 둘이 나란히 놓인 그림입니다. 회색 상자에는 두 모양 같음 답 차례 maybe yes approve 질문 값과 마지막 결과가 같음이 적혀 있고, 두 칸으로 화살표가 갑니다. 칸 조건부 엣지 모양 ask_once에는 파란 상자 interrupt를 한 번 부르고 노드를 마침 조건부 엣지로 되돌아감 아래에 노란 상자 interrupt 부른 횟수 누적 하나 셋 다섯 여섯과 노란 상자 체크포인트 둘 셋 넷 다섯이 있습니다. 칸 while True 모양 ask_in_loop 권하지 않음에는 파란 상자 노드 안 반복문에서 interrupt를 되풀이해 부름 아래에 노란 상자 interrupt 부른 횟수 누적 하나 셋 여섯 아홉과 노란 상자 체크포인트 둘 둘 둘 셋이 있는 그림|같은 답 차례에서 조건부 엣지 모양은 체크포인트가 답마다 하나씩 늘었고, while True 모양은 부른 횟수만 크게 쌓였습니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 회색 상자는 두 모양 모두에서 출력으로 확인한 값입니다. 칸 둘은 3절과 4절의 두 모양이고, 칸 맨 위 파란 상자는 두 노드가 다시 묻는 방법입니다. 칸 안의 노란 상자는 노트북 5절 견주기 출력의 네 줄을 차례로 적은 것입니다. 노란 상자 둘은 같은 셀들에서 함께 센 값이라 화살표 없이 쌓았습니다. 오른쪽 칸의 <code>while True</code> 모양은 공식 문서가 권하지 않는 모양입니다.</p>
<p>노트북 6절에서는 사람의 답이 멈춘 질문에 닿지 않는 장면 둘을 보았습니다. 체크포인터 없이 컴파일한 그래프는 첫 실행에서 멈춤 표시를 냈지만, 답을 넘기자 <code>RuntimeError</code>를 받았습니다. 멈춘 적 없는 스레드 <code>other</code>로 답을 넘기자, 그래프가 빈 상태로 노드를 실행해 <code>KeyError</code>를 받았습니다. 두 오류 모두 셀에서 받아 출력했고, 3절 스레드 <code>edge</code>의 칸 값은 그대로였습니다.</p>
{{mermaid:02-5-사람의-답이-질문에-닿지-않은-두-장면|위에 회색 상자 하나가 있고 아래에 칸 둘이 나란히 놓인 그림입니다. 회색 상자에는 두 장면 같음 노드 ask_once 사람의 답 approve가 적혀 있고, 두 칸으로 화살표가 갑니다. 칸 체크포인터 없이 컴파일에는 노란 상자 첫 실행은 멈춤 표시 하나 아래에 노란 상자 답을 넘기자 받은 오류 RuntimeError가 있습니다. 칸 멈춘 적 없는 스레드 other에는 노란 상자 답을 넘기자 받은 오류 KeyError order_key 아래에 노란 상자 스레드 other 칸 값 없음 다음 노드 ask_once가 있는 그림|체크포인터가 없거나 스레드 이름이 다르면, 사람의 답은 멈춘 질문에 닿지 않고 오류가 났습니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 회색 상자는 두 장면에 모두 해당합니다. 칸 둘은 노트북 6절의 두 장면이고, 칸 안은 위에서 아래로 셀 출력의 차례입니다. 노란 상자는 모두 셀에서 받아 출력한 값이고, 오류도 받아 출력했으므로 노랑입니다.</p>
<p>모델을 부르지 않아, 노트북 출력은 새 커널로 다시 실행해도 같아야 합니다. 새 커널로 두 번 실행했을 때 코드 셀 28개의 출력이 모두 같았습니다.</p>
<p class="look"><b>확인할 점</b> — 노트북 5절 견주기에서 <code>approve | 조건부 엣지 | 6 | 6 | 5</code>와 <code>approve | while True | 4 | 9 | 3</code>을 봅니다. 6절에서 <code>받은 오류: RuntimeError</code>와 <code>받은 오류: KeyError</code>, <code>스레드 other의 칸 값: {}</code>가 나오는지 확인합니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>노드 안 <code>while True</code>로 다시 묻는 모양은 실습 코드에 쓰지 않습니다. 이 절은 까닭을 보려고 노트북 4절에서 한 번 실행했습니다. 반복문 안에 실행마다 달라지는 줄이 있으면 질문과 답의 짝이 어긋날 수 있다고 공식 문서는 적습니다. 그런 장면은 이번에 실행하지 않았습니다.</li><li>노드 안에서 <code>interrupt</code>를 여러 번 부르면 답을 부른 차례로만 맞춥니다. 공식 문서는 그래서 조건에 따라 부르는 차례를 바꾸지 말라고 적습니다. 차례를 바꾸는 장면은 이번에 실행하지 않았습니다.</li><li>사람의 답은 멈춘 때와 같은 스레드 이름으로 보냅니다. 다른 이름으로 보내자 이 판에서는 <code>KeyError</code>처럼 스레드를 알려 주지 않는 오류가 났습니다. 체크포인터 없이 컴파일한 그래프는 첫 실행에서 멈췄지만, 답을 넘기자 <code>RuntimeError</code>가 났습니다.</li><li>노트북 밖 확인에서 끝난 스레드 <code>edge</code>에 답 <code>reject</code>를 한 번 더 보내자, 오류 없이 칸 값과 체크포인트 수가 그대로였습니다. 이 장면은 노트북에서 실행하지 않았습니다.</li><li>노트북 밖에서 같은 두 그래프에 목록 밖 답 다섯 개와 <code>approve</code>를 차례로 넣어 보았습니다. 끝났을 때 시작·부름·체크포인트는 조건부 엣지 모양이 12·12·8, 반복문 모양이 7·27·3이었습니다. 목록 밖 답이 늘수록 부른 수의 차이가 벌어졌고, 이 장면은 노트북에서 실행하지 않았습니다.</li><li>세 횟수는 노드 하나와 답 셋으로 만든 이 그래프의 값입니다. 노드나 답의 수가 다르면 수도 달라집니다.</li><li>셀 하나만 다시 실행하면 같은 스레드에 답이 더해지고 부른 기록 목록도 늘어, 값이 달라집니다. 처음 값으로 다시 보려면 1절 임시 폴더 셀부터 다시 실행합니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>목록에 없는 답(<code>maybe</code>·<code>yes</code>)을 받자, 노드가 칸 <code>error</code>에 까닭을 적고 조건부 엣지로 같은 노드에서 다시 물었습니다.</li><li>노드 안 <code>while True</code>로 다시 물어도 결과는 같았지만, 앞선 답을 다시 받는 부름이 쌓여 <code>interrupt</code>를 아홉 번 불렀습니다.</li><li>체크포인터 없이 답을 넘기면 <code>RuntimeError</code>를, 멈춘 적 없는 스레드로 넘기면 <code>KeyError</code>를 받았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href="03-상태-기록과-다른-분기-재실행.html">03절</a>에서는 지난 체크포인트를 골라 값을 바꾸고, 그 자리부터 다시 실행해 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 3절에서 <code>maybe</code>로 이어 간 셀 한 번에 노드 <code>ask_once</code>가 두 번 시작한 까닭은 무엇인가요?</p><p class="quiz-a">멈춘 노드가 처음부터 다시 실행되어 <code>maybe</code>를 받고, 오류 글을 내고 마쳤습니다. 그다음 조건 함수가 이름표 <code>ask_again</code>을 내놓아 같은 노드가 다시 실행되고 멈췄기 때문입니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">2. 4절 <code>while True</code> 모양에서 <code>yes</code>로 이어 간 셀은 <code>interrupt</code>를 세 번 불렀습니다. 까닭은 무엇인가요?</p><p class="quiz-a">노드가 처음부터 다시 실행되어 반복문도 첫 바퀴부터 돌았기 때문입니다. 둘째 부름이 <code>yes</code>를 받고 셋째 부름에서 멈춘 것은, 셋째 질문의 오류 글로 보입니다. 첫째 부름이 <code>maybe</code>를 다시 받은 것은 셀에 찍지 않았고, 설치판 설명으로 압니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">3. 4절 모양에서는 <code>maybe</code>와 <code>yes</code> 뒤에도 체크포인트가 2 그대로였습니다. 3절 모양과 무엇이 달랐나요?</p><p class="quiz-a">4절 노드는 끝나지 않고 멈춰 있어 체크포인트가 늘지 않았습니다. 3절 노드는 목록에 없는 답을 받을 때마다 오류 글을 내고 마쳐, 체크포인트가 하나씩 늘었습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">4. 멈춘 적 없는 스레드 <code>other</code>로 <code>approve</code>를 넘기자 <code>KeyError</code>가 난 까닭은 무엇인가요?</p><p class="quiz-a">그 스레드에는 저장된 상태가 없어, 그래프가 빈 상태로 노드를 실행했습니다. 노드가 칸 <code>order_key</code>를 읽는 줄에서 오류가 났습니다. 사람의 답은 멈춘 스레드 이름으로 보내야 합니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langgraph/interrupts">LangGraph Interrupts</a></div>확인 2026-09-25 · 「Rules of interrupts」 절의 문장입니다. <code>Do not loop interrupt calls using logic that isn't deterministic across executions, including while True validation loops. Use a conditional edge instead</code></li><li>같은 문서 「Validating human input」 절은 노드에서 <code>interrupt</code>를 한 번만 부르라고 적습니다. 오류 글은 상태에 담고, 조건부 엣지로 되돌아가라고 적습니다. 반복문 모양은 이어 갈 때마다 앞선 바퀴를 모두 다시 실행한다고도 적습니다.</li><li>같은 문서는 노드 안 여러 <code>interrupt</code>를 차례로만 맞추므로 차례를 바꾸지 말라고 적습니다. 이어 갈 때는 멈춘 때와 같은 스레드 이름을 쓰라고도 적습니다.</li><li>langgraph 1.2.11 소스 <code>langgraph/types.py</code> 864~868행 — 이어 갈 때 노드를 처음부터 다시 실행한다는 설명입니다. 노드 안 여러 <code>interrupt</code>에는 답을 부른 차례로 맞춘다고도 적습니다.</li><li>같은 판 <code>langgraph/pregel/_loop.py</code> 904~908행 — 체크포인터 없이 <code>Command(resume=…)</code>을 넘기면 <code>RuntimeError</code>를 내는 자리입니다.</li><li>Ch 13 03절에서 조건부 엣지와 이름표 표를, Ch 20 03절에서 끝점 <code>END</code>로 끝내는 조건 함수를 보았습니다.</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# Command resume으로 실행 재개

**이 노트북에서 할 일**

1. 사람의 답이 허용 답 목록에 없으면, 까닭을 알려 주고 같은 자리에서 다시 묻습니다.
2. 조건부 엣지로 다시 묻는 모양과 노드 안 `while True`로 다시 묻는 모양에 같은 답을 넣어 견줍니다.
3. 체크포인터가 없을 때와 스레드 이름이 다를 때, 사람의 답을 넘기면 어떤 오류가 나는지 봅니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
사람의 답은 우리가 셀에 적어 넣는 값(`"maybe"`·`"yes"`·`"approve"`)입니다.
실제 서비스라면 화면에서 사람이 고른 값을 같은 자리에 넣습니다.
매번 같은 값을 내는 우리 노드로, 노드가 시작한 횟수와 체크포인트 수를 셉니다.

체크포인트는 메모리에만 저장하고, 파일은 하나도 쓰지 않습니다.
그래도 01절과 같은 모양으로 빈 임시 폴더를 만들고, 마지막 셀에서 그 폴더가 비어 있는지 봅니다.
읽어 오는 자료 파일은 없습니다.
걸린 시간은 재지 않았습니다.

**기준 버전** — 첫 셀에서 패키지 둘을 설치합니다.
그래프는 langgraph 1.2.11, 체크포인터는 langgraph-checkpoint 4.2.0에 들어 있습니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.
설치 셀에 걸리는 시간은 네트워크에 따라 달라집니다.

**강의와 실습 범위** — 강의 시간에는 2~3절을 읽습니다.
받은 답을 허용 답 목록으로 검사하고, 조건부 엣지로 다시 묻는 자리입니다.
4~6절은 권하지 않는 모양과 견주고 오류 장면을 보는 자리이고, 실습 시간에 실행합니다.
셀 하나만 다시 실행하면 같은 스레드에 답이 더해지고 부른 기록 목록도 늘어, 값이 달라집니다.
처음 값으로 다시 보려면 1절 임시 폴더 셀부터 다시 실행합니다.

실습 폴더 `labs/part6/ch24-human-in-the-loop`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 읽는 그림입니다. 맨 위에 회색 둥근 상자 가상 시작점 START, 초록 상자 허용 답 목록 approve reject, 초록 상자 사람의 답 Command resume으로 넘김이 나란히 놓이고, 셋에서 파란 상자 노드 ask_once로 화살표가 갑니다. 파란 상자에는 interrupt를 한 번 부르고 받은 답을 목록으로 검사가 적혀 있고, 그 아래 회색 마름모 조건 함수 after_answer로 화살표가 갑니다. 마름모에서 나가는 점선 둘 가운데 하나는 오류 칸에 글 있음 이름표 ask_again으로 파란 상자에 되돌아가고, 다른 하나는 오류 칸 빈 글 이름표 END로 맨 아래 회색 둥근 상자 가상 끝점 END에 닿는 그림](attachment:02-1-조건부-엣지로-다시-묻는-그래프.png)

위에서 아래로 읽습니다.
초록 상자는 우리가 넣은 값과 사람의 답이고, 파란 상자는 우리가 적은 노드입니다.
회색 마름모는 노드로 등록하지 않는 조건 함수 `after_answer`이고, 마름모에서 나가는 점선 둘이 조건부 엣지입니다.
오류 칸에 글이 있으면 같은 노드로 되돌아가 다시 묻고, 빈 글이면 끝점으로 갑니다.

### [2] markdown {}

## 1. 준비

01절에서는 사람의 답이 `approve`인지 아닌지만 보았습니다.
실제 화면에서는 사람이 `maybe`처럼 정해 두지 않은 답을 보낼 수도 있습니다.
이 절에서는 받아들일 답을 목록으로 정해 두고, 목록에 없는 답이면 까닭을 알려 준 뒤 다시 묻습니다.
절 제목은 01절의 `Command(resume=…)`로 멈춘 실행을 이어 가는 일을 가리킵니다.
본문에서는 01절처럼 사람의 답으로 이어 가기라고 씁니다.

첫 셀은 01절과 같은 패키지 둘을 설치하고, 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:56.495101Z', 'iopub.status.busy': '2026-09-25T14:23:56.494926Z', 'iopub.status.idle': '2026-09-25T14:23:56.898406Z', 'shell.execute_reply': '2026-09-25T14:23:56.897872Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "langgraph==1.2.11" "langgraph-checkpoint==4.2.0"
from importlib.metadata import version

print("langgraph:", version("langgraph"))
print("langgraph-checkpoint:", version("langgraph-checkpoint"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
langgraph: 1.2.11
langgraph-checkpoint: 4.2.0

```

### [4] markdown {}

**결과 읽기** — 출력 줄 `langgraph: 1.2.11`과 `langgraph-checkpoint: 4.2.0`이 보입니다.
두 판 모두 실습 폴더 잠금과 같은 판입니다.
이 노트북의 출력은 2026-09-25에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
상태 형식과 그래프 이름은 Ch 13 01절, 체크포인터 `InMemorySaver`는 Ch 23 01절과 같습니다.
함수 `interrupt`와 객체 `Command`는 01절에서 가져온 이름 그대로입니다.
이 절은 파일을 쓰지 않아, 도구 파일 `approval_tools.py`에서는 아무것도 가져오지 않습니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:56.899607Z', 'iopub.status.busy': '2026-09-25T14:23:56.899518Z', 'iopub.status.idle': '2026-09-25T14:23:57.373671Z', 'shell.execute_reply': '2026-09-25T14:23:57.373325Z'}, 'lesson_role': 'setup'}

```python
# 그래프 이름(Ch 13 01절)·체크포인터(Ch 23 01절)와, 01절에서 쓴 멈춤 표시 이름 둘을 가져옵니다
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
# interrupt는 노드를 멈추는 함수, Command는 멈춘 그래프에 사람의 답을 넘길 때 쓰는 객체입니다(01절)
from langgraph.types import Command, interrupt

print("langgraph.graph에서 가져온 이름:", "StateGraph, START, END")
print("langgraph.types에서 가져온 이름:", "Command, interrupt")
```

출력:
```
langgraph.graph에서 가져온 이름: StateGraph, START, END
langgraph.types에서 가져온 이름: Command, interrupt

```

### [6] markdown {}

**결과 읽기** — 출력 줄 `langgraph.types에서 가져온 이름: Command, interrupt`가 보입니다.

다음 셀은 01절처럼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다.
이 절은 파일을 쓰지 않지만, 마지막 셀에서 이 폴더가 그대로 비어 있는지 봅니다.
폴더 위치는 컴퓨터마다 달라 출력하지 않고, 폴더 이름의 앞머리만 확인합니다.

### [7] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.374339Z', 'iopub.status.busy': '2026-09-25T14:23:57.374282Z', 'iopub.status.idle': '2026-09-25T14:23:57.376601Z', 'shell.execute_reply': '2026-09-25T14:23:57.376212Z'}, 'lesson_role': 'setup'}

```python
# 파일이 생기는지 볼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다(Ch 23 01절과 같은 모양)
import os
import tempfile

# mkdtemp()는 운영체제 임시 폴더 안에 새 폴더를 만들고, 그 폴더의 위치를 글로 내놓습니다
practice_folder = tempfile.mkdtemp(prefix="ch24-02-")
# chdir()는 터미널의 cd처럼 현재 작업 폴더를 옮깁니다
os.chdir(practice_folder)
print("임시 폴더 이름에 ch24-02-이 들어 있는가:", "ch24-02-" in practice_folder)
print("현재 작업 폴더의 파일:", os.listdir())
```

출력:
```
임시 폴더 이름에 ch24-02-이 들어 있는가: True
현재 작업 폴더의 파일: []

```

### [8] markdown {}

**결과 읽기** — 출력 줄 `임시 폴더 이름에 ch24-02-이 들어 있는가: True`로, 이 절의 폴더를 만들었습니다.
출력 줄 `현재 작업 폴더의 파일: []`로, 빈 폴더에서 시작합니다.

## 2. 허용 답 목록과 질문 값

허용 답 목록은 사람의 답으로 받아들일 값만 적어 둔 목록입니다.
01절의 도미노 줄로 말하면, 빈자리에 맞는 도미노의 모양을 정해 두는 것과 같습니다.
이 절 코드에서는 목록 `allowed_answers`이고, 받은 답이 목록에 있는지 `in`으로 검사합니다.
Ch 16 01절·Ch 18 02절의 허용 목록과 같은 뜻이고, 여기서는 사람의 답에 씁니다.

다음 셀은 목록을 만들고, 목록에 있는 답과 없는 답을 하나씩 검사해 봅니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.377145Z', 'iopub.status.busy': '2026-09-25T14:23:57.377092Z', 'iopub.status.idle': '2026-09-25T14:23:57.378845Z', 'shell.execute_reply': '2026-09-25T14:23:57.378538Z'}}

```python
# 사람의 답으로 받아들일 값 둘을 허용 답 목록에 적고, 답 둘을 검사해 봅니다
allowed_answers = ["approve", "reject"]
print("허용 답 목록:", allowed_answers)
# in은 목록에 같은 값이 있으면 True, 없으면 False를 내놓습니다
print("approve가 목록에 있는가:", "approve" in allowed_answers)
print("maybe가 목록에 있는가:", "maybe" in allowed_answers)
```

출력:
```
허용 답 목록: ['approve', 'reject']
approve가 목록에 있는가: True
maybe가 목록에 있는가: False

```

### [10] markdown {}

**결과 읽기** — 출력 줄 `허용 답 목록: ['approve', 'reject']`입니다.
출력 줄 `approve가 목록에 있는가: True`와 `maybe가 목록에 있는가: False`가 보입니다.
이 절의 노드는 받은 답을 이 목록으로 검사합니다.

다음 셀은 이 절의 상태 형식을 만듭니다.
칸 `order_key`는 주문 키, 칸 `answer`는 받아들인 사람의 답입니다.
칸 `error`는 바로 앞 답을 받아들이지 않은 까닭을 적는 글 칸이고, 빈 글이면 까닭이 없다는 뜻입니다.
세 칸 모두 규칙을 적지 않아, 새 값이 오면 덮어씁니다.
01절의 `ApprovalState`와 칸이 달라, 이름도 새로 붙였습니다.

### [11] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.379377Z', 'iopub.status.busy': '2026-09-25T14:23:57.379322Z', 'iopub.status.idle': '2026-09-25T14:23:57.380904Z', 'shell.execute_reply': '2026-09-25T14:23:57.380655Z'}}

```python
# 주문 키·사람의 답·오류 글 칸을 둔 상태 형식을 만듭니다(Ch 13 01절 모양, 세 칸 모두 규칙 없음)
class ReviewState(TypedDict):
    order_key: str
    answer: str
    error: str
```

출력:
```

```

### [12] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 절의 그래프는 모두 이 상태 형식을 씁니다.

다음 셀은 질문 값을 만드는 함수입니다.
01절의 질문 값에 허용 답 목록과 오류 글을 더합니다.
사람은 이 질문 값을 보고, 보낼 수 있는 답과 앞 답을 받아들이지 않은 까닭을 봅니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.381495Z', 'iopub.status.busy': '2026-09-25T14:23:57.381441Z', 'iopub.status.idle': '2026-09-25T14:23:57.383274Z', 'shell.execute_reply': '2026-09-25T14:23:57.382938Z'}}

```python
# 주문 키와 오류 글을 받아 질문 값 딕셔너리를 만듭니다(오류 글이 빈 글이면 처음 묻는 질문입니다)
def make_question(order_key, error_text):
    question = {"order_key": order_key, "question": "결제할까요?"}
    # 사람이 보낼 수 있는 답과, 바로 앞 답을 받아들이지 않은 까닭을 함께 보입니다
    question["allowed"] = allowed_answers
    question["error"] = error_text
    return question
```

출력:
```

```

### [14] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
오류 글이 빈 글이면 처음 묻는 질문이고, 글이 있으면 다시 묻는 질문입니다.
3절과 4절의 두 노드가 모두 이 함수로 질문 값을 만듭니다.

다음 셀은 횟수를 세어 출력하는 함수입니다.
01절에서는 노드 안의 `print`로, 노드가 시작할 때마다 한 줄을 찍었습니다.
이 절의 노드는 시작할 때 글 `시작`을, 함수 `interrupt`를 부르기 바로 앞에 글 `질문`을 목록에 적습니다.
그 목록에서 두 글의 수를 세고, 체크포인트 수와 함께 출력합니다.
센 세 값은 한 줄로 묶어, 인자로 받은 목록 끝에 덧붙입니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.383824Z', 'iopub.status.busy': '2026-09-25T14:23:57.383775Z', 'iopub.status.idle': '2026-09-25T14:23:57.385562Z', 'shell.execute_reply': '2026-09-25T14:23:57.385264Z'}}

```python
# 부른 기록 목록에서 노드 시작 수와 interrupt 부른 수를 세고, 체크포인트 수와 함께 출력합니다
def record_counts(calls, graph, config, rows):
    history = list(graph.get_state_history(config))
    counts = [calls.count("시작"), calls.count("질문"), len(history)]
    print("노드가 시작한 횟수:", counts[0])
    print("interrupt를 부른 횟수:", counts[1])
    print("체크포인트 수:", counts[2])
    # 센 세 값을 한 줄로 rows 끝에 덧붙여, 5절에서 두 모양을 견줄 때 씁니다
    rows.append(counts)
```

출력:
```

```

### [16] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
체크포인트 수는 Ch 23 01절처럼 `get_state_history`가 내놓은 목록의 길이로 셉니다.
세 수는 모두 이 함수를 부를 때까지 쌓인 수입니다.

## 3. 조건부 엣지로 다시 묻기

다시 묻기는 받아들이지 않는 답이 오면, 까닭을 질문 값에 담아 같은 자리에서 한 번 더 멈추는 일입니다.
도미노 줄의 빈자리에 맞지 않는 구슬이 놓이면, 구슬을 치우고 맞는 도미노를 다시 기다리는 것과 같습니다.
이 절 코드에서는 노드가 칸 `error`에 까닭을 적고, 조건부 엣지가 같은 노드로 되돌아가는 모양입니다.
Ch 18 02절의 되묻기는 흐름을 끝내고 다시 물었지만, 이 절은 멈춘 그래프가 같은 자리에서 다시 멈춥니다.

공식 문서는 이 모양을 권합니다.
노드 안에서 함수 `interrupt`는 한 번만 부르고, 오류 글은 상태에 담아 노드를 마칩니다.
그다음 조건부 엣지로 노드에 되돌아가, 받아들일 답이 올 때까지 묻습니다.
다음 셀은 그 노드입니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.386089Z', 'iopub.status.busy': '2026-09-25T14:23:57.386025Z', 'iopub.status.idle': '2026-09-25T14:23:57.387735Z', 'shell.execute_reply': '2026-09-25T14:23:57.387392Z'}}

```python
# 권하는 모양: 질문 값을 만들어 interrupt를 한 번만 부르고, 답을 검사해 답 칸이나 오류 칸에 냅니다
def ask_once(state):
    edge_calls.append("시작")
    question = make_question(state["order_key"], state["error"])
    # interrupt를 부르기 바로 앞에 적어, 부른 횟수를 셀 수 있게 합니다
    edge_calls.append("질문")
    answer = interrupt(question)
    if answer in allowed_answers:
        return {"answer": answer, "error": ""}
    return {"error": "허용하지 않는 값: " + answer}
```

출력:
```

```

### [18] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
목록에 있는 답이면 칸 `answer`에 답을 내고, 칸 `error`는 빈 글로 비웁니다.
목록에 없는 답이면 받은 값을 넣은 오류 글만 칸 `error`에 내고, 칸 `answer`는 그대로 둡니다.
노드는 어느 쪽이든 끝나고, 다시 물을지는 다음 셀의 조건 함수가 정합니다.
목록 `edge_calls`는 뒤의 그래프를 만드는 셀에서 만듭니다.

Ch 13 03절의 조건 함수는 상태를 읽고, 다음에 갈 곳의 이름표를 내놓았습니다.
다음 셀의 조건 함수는 칸 `error`를 봅니다.
오류 글이 없으면 끝점 `END`를, 있으면 이름표 `ask_again`을 내놓습니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.388285Z', 'iopub.status.busy': '2026-09-25T14:23:57.388235Z', 'iopub.status.idle': '2026-09-25T14:23:57.389617Z', 'shell.execute_reply': '2026-09-25T14:23:57.389299Z'}}

```python
# 칸 error를 보고, 오류 글이 없으면 끝점 END를, 있으면 이름표 "ask_again"을 내놓는 조건 함수입니다
def after_answer(state):
    if state["error"] == "":
        return END
    return "ask_again"
```

출력:
```

```

### [20] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
Ch 20 03절의 `next_or_end`처럼, 끝낼 때는 이름표 대신 `END`를 바로 내놓습니다.

다음 셀은 조건 함수를 그래프 없이 직접 불러, 오류 칸에 따라 무엇을 내놓는지 봅니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.390211Z', 'iopub.status.busy': '2026-09-25T14:23:57.390162Z', 'iopub.status.idle': '2026-09-25T14:23:57.391828Z', 'shell.execute_reply': '2026-09-25T14:23:57.391538Z'}}

```python
# 조건 함수를 그래프 없이 직접 불러, 오류 칸이 빈 글일 때와 글이 있을 때 내놓는 값을 봅니다
done_state = {"order_key": "order-2402", "answer": "approve", "error": ""}
again_state = {"order_key": "order-2402", "answer": "대기", "error": "허용하지 않는 값: maybe"}
print("오류 칸이 빈 글일 때:", after_answer(done_state))
print("오류 칸에 글이 있을 때:", after_answer(again_state))
```

출력:
```
오류 칸이 빈 글일 때: __end__
오류 칸에 글이 있을 때: ask_again

```

### [22] markdown {}

**결과 읽기** — 출력 줄 `오류 칸이 빈 글일 때: __end__`입니다.
Ch 20 03절에서 본 것처럼, 끝점 `END`의 값은 글 `__end__`입니다.
출력 줄 `오류 칸에 글이 있을 때: ask_again`으로, 다시 물을 때의 이름표가 나왔습니다.

다음 셀은 이름표 표를 만듭니다.
이름표 `ask_again`은 노드 `ask_once`로, 끝점 `END`는 끝점으로 잇습니다.
조건부 엣지가 가리키는 곳이 자기 자신이면, 그 노드를 한 번 더 실행합니다.
Ch 20 01절의 되돌아가는 엣지는 다른 노드로 갔고, 이 절의 엣지는 같은 노드로 갑니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.392400Z', 'iopub.status.busy': '2026-09-25T14:23:57.392348Z', 'iopub.status.idle': '2026-09-25T14:23:57.394136Z', 'shell.execute_reply': '2026-09-25T14:23:57.393850Z'}}

```python
# 조건 함수의 이름표를 실제로 갈 곳에 잇는 이름표 표를 만듭니다(Ch 13 03절 · Ch 20 03절)
path_map = {"ask_again": "ask_once", END: END}
print("이름표와 갈 곳을 이은 표:")
for label in path_map:
    print(label, "->", path_map[label])
```

출력:
```
이름표와 갈 곳을 이은 표:
ask_again -> ask_once
__end__ -> __end__

```

### [24] markdown {}

**결과 읽기** — 라벨 줄 아래에 `ask_again -> ask_once`와 `__end__ -> __end__` 두 줄이 보입니다.

다음 셀은 노드 하나와 조건부 엣지로 그래프를 만들고, 체크포인터를 붙여 컴파일합니다.
노드 `ask_once`에서 끝점으로 가는 고정 엣지는 적지 않습니다.
끝낼지 다시 물을지는 조건부 엣지가 정하기 때문입니다.
부른 기록 목록 `edge_calls`와, 답마다 센 값을 모을 목록 `edge_rows`도 여기서 만듭니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.394660Z', 'iopub.status.busy': '2026-09-25T14:23:57.394610Z', 'iopub.status.idle': '2026-09-25T14:23:57.397181Z', 'shell.execute_reply': '2026-09-25T14:23:57.396827Z'}}

```python
# 노드 ask_once에서 나가는 엣지를 조건부 엣지로 적고, 체크포인터를 붙여 컴파일합니다
edge_builder = StateGraph(ReviewState)
edge_builder.add_node("ask_once", ask_once)
edge_builder.add_edge(START, "ask_once")
edge_builder.add_conditional_edges("ask_once", after_answer, path_map)
edge_graph = edge_builder.compile(checkpointer=InMemorySaver())
# 노드가 적을 부른 기록 목록과, 답마다 센 세 값을 모을 목록입니다
edge_calls = []
edge_rows = []
print("고정 엣지로 적은 수:", len(edge_builder.edges))
print("조건부 엣지를 적은 노드 수:", len(edge_builder.branches))
```

출력:
```
고정 엣지로 적은 수: 1
조건부 엣지를 적은 노드 수: 1

```

### [26] markdown {}

**결과 읽기** — 출력 줄 `고정 엣지로 적은 수: 1`과 `조건부 엣지를 적은 노드 수: 1`입니다.
고정 엣지 하나는 가상 시작점 `START`에서 노드로 가는 엣지입니다.

다음 셀은 주문 키 `order-2402`로 첫 실행을 합니다.
스레드 이름은 `edge`입니다.
실행 전에 예상해 봅니다.
01절처럼 노드는 멈춤 표시에서 멈추고, 질문 값의 오류 글은 빈 글일 것입니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.397713Z', 'iopub.status.busy': '2026-09-25T14:23:57.397650Z', 'iopub.status.idle': '2026-09-25T14:23:57.402888Z', 'shell.execute_reply': '2026-09-25T14:23:57.402635Z'}}

```python
# 첫 실행: 주문 키 order-2402를 스레드 edge로 넣어 멈추게 하고, 질문 값과 세 횟수를 봅니다
edge_config = {"configurable": {"thread_id": "edge"}}
first_input = {"order_key": "order-2402", "answer": "대기", "error": ""}
edge_result = edge_graph.invoke(first_input, edge_config)
print("질문 값:", edge_result["__interrupt__"][0].value)
record_counts(edge_calls, edge_graph, edge_config, edge_rows)
```

출력:
```
질문 값: {'order_key': 'order-2402', 'question': '결제할까요?', 'allowed': ['approve', 'reject'], 'error': ''}
노드가 시작한 횟수: 1
interrupt를 부른 횟수: 1
체크포인트 수: 2

```

### [28] markdown {}

**결과 읽기** — 출력 줄 `질문 값: {'order_key': 'order-2402', 'question': '결제할까요?', 'allowed': ['approve', 'reject'], 'error': ''}`입니다.
허용 답 목록이 질문 값에 실렸고, 오류 글은 빈 글입니다.
출력 줄 `노드가 시작한 횟수: 1`과 `interrupt를 부른 횟수: 1`, `체크포인트 수: 2`가 보입니다.
체크포인트 둘은 01절의 첫 실행과 같습니다.

다음 셀은 허용 답 목록에 없는 사람의 답 `maybe`로 이어 갑니다.
실행 전에 예상해 봅니다.
노드는 처음부터 다시 실행되어 답을 받고, 칸 `error`에 글을 적고 끝납니다.
그다음 조건부 엣지로 같은 노드가 다시 실행되어, 오류 글을 담은 질문에서 멈출 것입니다.

### [29] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.403434Z', 'iopub.status.busy': '2026-09-25T14:23:57.403392Z', 'iopub.status.idle': '2026-09-25T14:23:57.406321Z', 'shell.execute_reply': '2026-09-25T14:23:57.406019Z'}}

```python
# 허용 답 목록에 없는 사람의 답 "maybe"로 이어 가고, 다음 질문 값과 세 횟수를 봅니다
edge_result = edge_graph.invoke(Command(resume="maybe"), edge_config)
print("질문 값:", edge_result["__interrupt__"][0].value)
record_counts(edge_calls, edge_graph, edge_config, edge_rows)
```

출력:
```
질문 값: {'order_key': 'order-2402', 'question': '결제할까요?', 'allowed': ['approve', 'reject'], 'error': '허용하지 않는 값: maybe'}
노드가 시작한 횟수: 3
interrupt를 부른 횟수: 3
체크포인트 수: 3

```

### [30] markdown {}

**결과 읽기** — 출력 줄 `질문 값:` 끝에 `'error': '허용하지 않는 값: maybe'`가 실렸습니다.
출력 줄 `노드가 시작한 횟수: 3`과 `interrupt를 부른 횟수: 3`, `체크포인트 수: 3`입니다.
이 셀 한 번에 노드가 두 번 시작했습니다.
한 번은 멈춘 노드가 처음부터 다시 실행되어 `maybe`를 받은 것이고, 한 번은 조건부 엣지로 다시 실행되어 멈춘 것입니다.
오류 글을 내고 마친 노드의 체크포인트가 하나 늘었습니다.

다음 셀은 역시 목록에 없는 사람의 답 `yes`로 이어 갑니다.
실행 전에 예상해 봅니다.
앞 셀과 같이 노드가 두 번 시작하고, 체크포인트가 하나 늘 것입니다.

### [31] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.406764Z', 'iopub.status.busy': '2026-09-25T14:23:57.406722Z', 'iopub.status.idle': '2026-09-25T14:23:57.409457Z', 'shell.execute_reply': '2026-09-25T14:23:57.409133Z'}}

```python
# 역시 목록에 없는 사람의 답 "yes"로 이어 가고, 다음 질문 값과 세 횟수를 봅니다
edge_result = edge_graph.invoke(Command(resume="yes"), edge_config)
print("질문 값:", edge_result["__interrupt__"][0].value)
record_counts(edge_calls, edge_graph, edge_config, edge_rows)
```

출력:
```
질문 값: {'order_key': 'order-2402', 'question': '결제할까요?', 'allowed': ['approve', 'reject'], 'error': '허용하지 않는 값: yes'}
노드가 시작한 횟수: 5
interrupt를 부른 횟수: 5
체크포인트 수: 4

```

### [32] markdown {}

**결과 읽기** — 출력 줄 `질문 값:` 끝의 오류 글이 `'error': '허용하지 않는 값: yes'`로 바뀌었습니다.
출력 줄 `노드가 시작한 횟수: 5`와 `interrupt를 부른 횟수: 5`, `체크포인트 수: 4`입니다.
앞 셀과 같이 노드는 두 번 시작했고, 체크포인트는 하나 늘었습니다.
칸 `error`는 규칙 없는 칸이라, 새 오류 글이 앞 글을 덮어썼습니다.

다음 셀은 목록에 있는 사람의 답 `approve`로 이어 갑니다.
실행 전에 예상해 봅니다.
노드는 답을 칸 `answer`에 내고, 오류 칸이 비어 조건부 엣지가 끝점으로 갈 것입니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.409967Z', 'iopub.status.busy': '2026-09-25T14:23:57.409919Z', 'iopub.status.idle': '2026-09-25T14:23:57.412798Z', 'shell.execute_reply': '2026-09-25T14:23:57.412456Z'}}

```python
# 목록에 있는 사람의 답 "approve"로 이어 가고, 결과와 세 횟수, 다음에 실행할 노드를 봅니다
edge_result = edge_graph.invoke(Command(resume="approve"), edge_config)
print("이어 간 뒤 결과:", edge_result)
record_counts(edge_calls, edge_graph, edge_config, edge_rows)
edge_state = edge_graph.get_state(edge_config)
print("다음에 실행할 노드:", edge_state.next)
# 우리 노드와 라이브러리가 정하는 횟수라 실행마다 같아야 합니다
assert edge_rows[3] == [6, 6, 5], "조건부 엣지 모양은 노드 시작 여섯, interrupt 여섯, 체크포인트 다섯이어야 합니다"
```

출력:
```
이어 간 뒤 결과: {'order_key': 'order-2402', 'answer': 'approve', 'error': ''}
노드가 시작한 횟수: 6
interrupt를 부른 횟수: 6
체크포인트 수: 5
다음에 실행할 노드: ()

```

### [34] markdown {}

**결과 읽기** — 출력 줄 `이어 간 뒤 결과: {'order_key': 'order-2402', 'answer': 'approve', 'error': ''}`에는 키 `__interrupt__`가 없습니다.
출력 줄 `노드가 시작한 횟수: 6`과 `interrupt를 부른 횟수: 6`, `체크포인트 수: 5`입니다.
이번에는 노드가 한 번만 시작했고, 조건 함수가 `END`를 내놓아 실행이 끝났습니다.
출력 줄 `다음에 실행할 노드: ()`로, 더 실행할 노드가 없습니다.

이 모양에서는 노드가 시작한 횟수와 함수 `interrupt`를 부른 횟수가 늘 같았습니다.
노드가 한 번 시작할 때마다 `interrupt`를 한 번만 부르기 때문입니다.

## 4. 권하지 않는 모양: 노드 안에서 while True로 다시 묻기

이번에는 같은 다시 묻기를 노드 하나 안의 반복문으로 만듭니다.
공식 문서는 노드 안에서 `while True`로 함수 `interrupt`를 되풀이해 부르지 말라고 적습니다.
이 절은 왜 권하지 않는지 보려고 이 모양을 한 번만 실행합니다.
실습 코드에 옮겨 쓰는 모양은 3절입니다.

반복문 `while True`는 조건이 늘 참이라, 안에서 `return`을 만나야 끝납니다.
다음 셀의 노드는 목록에 없는 답을 받으면 오류 글을 담은 질문 값을 새로 만들고, 반복문 처음으로 갑니다.

### [35] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.413288Z', 'iopub.status.busy': '2026-09-25T14:23:57.413242Z', 'iopub.status.idle': '2026-09-25T14:23:57.414998Z', 'shell.execute_reply': '2026-09-25T14:23:57.414698Z'}}

```python
# 권하지 않는 모양: 노드 안 while True에서 interrupt를 되풀이해 부르며 다시 묻습니다(공식 문서가 쓰지 말라는 모양)
def ask_in_loop(state):
    loop_calls.append("시작")
    question = make_question(state["order_key"], "")
    while True:
        loop_calls.append("질문")
        answer = interrupt(question)
        if answer in allowed_answers:
            return {"answer": answer, "error": ""}
        # 목록에 없는 답이면 오류 글을 담은 질문 값을 새로 만들고, 반복문 처음으로 가서 다시 묻습니다
        question = make_question(state["order_key"], "허용하지 않는 값: " + answer)
```

출력:
```

```

### [36] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
이 노드는 오류 글을 상태 칸에 적지 않고, 노드 안에서 새 질문 값을 만들어 다시 멈춥니다.
그래서 노드 하나 안에서 함수 `interrupt`를 여러 번 부르게 됩니다.

다음 셀은 01절처럼 노드 하나를 `START` → 노드 → `END`로 잇고, 체크포인터를 붙여 컴파일합니다.
부른 기록 목록 `loop_calls`와 센 값을 모을 목록 `loop_rows`도 새로 만듭니다.

### [37] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.415525Z', 'iopub.status.busy': '2026-09-25T14:23:57.415483Z', 'iopub.status.idle': '2026-09-25T14:23:57.417574Z', 'shell.execute_reply': '2026-09-25T14:23:57.417252Z'}}

```python
# 노드 하나를 START → ask_in_loop → END로 잇고, 체크포인터를 붙여 컴파일합니다(01절 모양)
loop_builder = StateGraph(ReviewState)
loop_builder.add_node("ask_in_loop", ask_in_loop)
loop_builder.add_edge(START, "ask_in_loop")
loop_builder.add_edge("ask_in_loop", END)
loop_graph = loop_builder.compile(checkpointer=InMemorySaver())
# 노드가 적을 부른 기록 목록과, 답마다 센 세 값을 모을 목록입니다
loop_calls = []
loop_rows = []
print("고정 엣지로 적은 수:", len(loop_builder.edges))
print("조건부 엣지를 적은 노드 수:", len(loop_builder.branches))
```

출력:
```
고정 엣지로 적은 수: 2
조건부 엣지를 적은 노드 수: 0

```

### [38] markdown {}

**결과 읽기** — 출력 줄 `고정 엣지로 적은 수: 2`와 `조건부 엣지를 적은 노드 수: 0`입니다.
3절 그래프와 달리 조건부 엣지가 없고, 다시 묻는 일은 모두 노드 안에서 일어납니다.

다음 셀은 3절과 같은 입력으로 첫 실행을 합니다.
스레드 이름은 `loop`입니다.
실행 전에 예상해 봅니다.
첫 실행은 3절과 같이 노드가 한 번 시작하고, 한 번 부른 뒤 멈출 것입니다.

### [39] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.418091Z', 'iopub.status.busy': '2026-09-25T14:23:57.418043Z', 'iopub.status.idle': '2026-09-25T14:23:57.420577Z', 'shell.execute_reply': '2026-09-25T14:23:57.420294Z'}}

```python
# 첫 실행: 3절과 같은 입력 first_input을 새 스레드 loop로 넣고, 질문 값과 세 횟수를 봅니다
loop_config = {"configurable": {"thread_id": "loop"}}
loop_result = loop_graph.invoke(first_input, loop_config)
print("질문 값:", loop_result["__interrupt__"][0].value)
record_counts(loop_calls, loop_graph, loop_config, loop_rows)
```

출력:
```
질문 값: {'order_key': 'order-2402', 'question': '결제할까요?', 'allowed': ['approve', 'reject'], 'error': ''}
노드가 시작한 횟수: 1
interrupt를 부른 횟수: 1
체크포인트 수: 2

```

### [40] markdown {}

**결과 읽기** — 출력 줄 `질문 값:`의 딕셔너리는 3절 첫 실행의 질문 값과 같습니다.
출력 줄 `노드가 시작한 횟수: 1`과 `interrupt를 부른 횟수: 1`, `체크포인트 수: 2`도 3절과 같습니다.

다음 셀은 3절과 같은 답 `maybe`로 이어 갑니다.
실행 전에 예상해 봅니다.
01절에서 본 대로 노드는 처음부터 다시 실행됩니다.
그러면 반복문 첫 바퀴의 `interrupt`가 무엇을 내놓을지 생각해 봅니다.

### [41] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.421138Z', 'iopub.status.busy': '2026-09-25T14:23:57.421091Z', 'iopub.status.idle': '2026-09-25T14:23:57.423695Z', 'shell.execute_reply': '2026-09-25T14:23:57.423355Z'}}

```python
# 3절과 같은 사람의 답 "maybe"로 이어 가고, 다음 질문 값과 세 횟수를 봅니다
loop_result = loop_graph.invoke(Command(resume="maybe"), loop_config)
print("질문 값:", loop_result["__interrupt__"][0].value)
record_counts(loop_calls, loop_graph, loop_config, loop_rows)
```

출력:
```
질문 값: {'order_key': 'order-2402', 'question': '결제할까요?', 'allowed': ['approve', 'reject'], 'error': '허용하지 않는 값: maybe'}
노드가 시작한 횟수: 2
interrupt를 부른 횟수: 3
체크포인트 수: 2

```

### [42] markdown {}

**결과 읽기** — 출력 줄 `질문 값:` 끝의 `'error': '허용하지 않는 값: maybe'`는 3절과 같습니다.
그런데 출력 줄 `노드가 시작한 횟수: 2`와 `interrupt를 부른 횟수: 3`, `체크포인트 수: 2`는 3절과 다릅니다.
이 셀에서 노드는 한 번 시작했지만, 함수 `interrupt`를 두 번 불렀습니다.
첫 부름은 넘겨받은 `maybe`를 내놓았고, 둘째 부름에서 오류 글을 담은 질문으로 멈췄습니다.
노드가 끝나지 않아, 체크포인트는 늘지 않았습니다.

다음 셀은 3절과 같은 답 `yes`로 이어 갑니다.
실행 전에 예상해 봅니다.
노드가 다시 처음부터 실행되니, 반복문도 첫 바퀴부터 다시 돕니다.

### [43] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.424225Z', 'iopub.status.busy': '2026-09-25T14:23:57.424183Z', 'iopub.status.idle': '2026-09-25T14:23:57.426434Z', 'shell.execute_reply': '2026-09-25T14:23:57.426170Z'}}

```python
# 3절과 같은 사람의 답 "yes"로 이어 가고, 다음 질문 값과 세 횟수를 봅니다
loop_result = loop_graph.invoke(Command(resume="yes"), loop_config)
print("질문 값:", loop_result["__interrupt__"][0].value)
record_counts(loop_calls, loop_graph, loop_config, loop_rows)
```

출력:
```
질문 값: {'order_key': 'order-2402', 'question': '결제할까요?', 'allowed': ['approve', 'reject'], 'error': '허용하지 않는 값: yes'}
노드가 시작한 횟수: 3
interrupt를 부른 횟수: 6
체크포인트 수: 2

```

### [44] markdown {}

**결과 읽기** — 출력 줄 `질문 값:` 끝의 오류 글은 `'error': '허용하지 않는 값: yes'`로, 3절과 같습니다.
출력 줄 `노드가 시작한 횟수: 3`과 `interrupt를 부른 횟수: 6`, `체크포인트 수: 2`입니다.
이 셀에서 노드는 한 번 시작해 함수 `interrupt`를 세 번 불렀습니다.
셋째 부름의 질문에 오류 글 `yes`가 실렸으니, 둘째 부름이 `yes`를 받은 것입니다.
첫 부름은 앞선 답 `maybe`를 다시 받았고, 이 값은 셀 출력에 따로 찍지 않았습니다.

차례 맞추기는 한 노드 안에서 함수 `interrupt`를 여러 번 부를 때, 받은 답을 부른 차례대로 맞추는 일입니다.
도미노 줄을 처음부터 다시 세울 때, 전에 놓았던 물건을 같은 자리에 차례대로 다시 놓는 것과 같습니다.
이 셀에서 첫 부름이 `maybe`를, 둘째 부름이 `yes`를 받은 것이 이 모습입니다.
설치판 소스 `langgraph/types.py` 866~868행이 노드 안의 여러 `interrupt`에 답을 부른 차례로 맞춘다고 적습니다.

다음 셀은 `approve`로 이어 갑니다.
실행 전에 예상해 봅니다.
노드는 앞선 답 둘을 차례대로 다시 받은 뒤, 셋째 부름에서 `approve`를 받아 끝날 것입니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.426984Z', 'iopub.status.busy': '2026-09-25T14:23:57.426942Z', 'iopub.status.idle': '2026-09-25T14:23:57.429495Z', 'shell.execute_reply': '2026-09-25T14:23:57.429225Z'}}

```python
# 3절과 같은 사람의 답 "approve"로 이어 가고, 결과와 세 횟수, 다음에 실행할 노드를 봅니다
loop_result = loop_graph.invoke(Command(resume="approve"), loop_config)
print("이어 간 뒤 결과:", loop_result)
record_counts(loop_calls, loop_graph, loop_config, loop_rows)
loop_state = loop_graph.get_state(loop_config)
print("다음에 실행할 노드:", loop_state.next)
# 우리 노드와 라이브러리가 정하는 횟수라 실행마다 같아야 합니다
assert loop_rows[3] == [4, 9, 3], "while True 모양은 노드 시작 넷, interrupt 아홉, 체크포인트 셋이어야 합니다"
```

출력:
```
이어 간 뒤 결과: {'order_key': 'order-2402', 'answer': 'approve', 'error': ''}
노드가 시작한 횟수: 4
interrupt를 부른 횟수: 9
체크포인트 수: 3
다음에 실행할 노드: ()

```

### [46] markdown {}

**결과 읽기** — 출력 줄 `이어 간 뒤 결과: {'order_key': 'order-2402', 'answer': 'approve', 'error': ''}`는 3절 결과와 같습니다.
출력 줄 `노드가 시작한 횟수: 4`와 `interrupt를 부른 횟수: 9`, `체크포인트 수: 3`입니다.
출력 줄 `다음에 실행할 노드: ()`로, 실행이 끝났습니다.
사람에게 보인 질문과 마지막 결과는 3절과 같았고, 다른 것은 부른 횟수와 체크포인트 수입니다.

## 5. 두 모양 견주기

다음 셀은 3절과 4절에서 답마다 센 세 값을 한 표로 모읍니다.
두 모양 모두 같은 답을 같은 차례(`maybe` → `yes` → `approve`)로 받았습니다.

### [47] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.430017Z', 'iopub.status.busy': '2026-09-25T14:23:57.429970Z', 'iopub.status.idle': '2026-09-25T14:23:57.431909Z', 'shell.execute_reply': '2026-09-25T14:23:57.431588Z'}}

```python
# 두 모양에서 답마다 센 세 값을, 답과 모양 이름을 붙여 한 줄씩 출력합니다
turns = ["첫 실행", "maybe", "yes", "approve"]
print("답 | 모양 | 노드가 시작한 횟수 | interrupt를 부른 횟수 | 체크포인트 수")
for i in range(len(turns)):
    print(turns[i], "| 조건부 엣지 |", edge_rows[i][0], "|", edge_rows[i][1], "|", edge_rows[i][2])
    print(turns[i], "| while True |", loop_rows[i][0], "|", loop_rows[i][1], "|", loop_rows[i][2])
```

출력:
```
답 | 모양 | 노드가 시작한 횟수 | interrupt를 부른 횟수 | 체크포인트 수
첫 실행 | 조건부 엣지 | 1 | 1 | 2
첫 실행 | while True | 1 | 1 | 2
maybe | 조건부 엣지 | 3 | 3 | 3
maybe | while True | 2 | 3 | 2
yes | 조건부 엣지 | 5 | 5 | 4
yes | while True | 3 | 6 | 2
approve | 조건부 엣지 | 6 | 6 | 5
approve | while True | 4 | 9 | 3

```

### [48] markdown {}

**결과 읽기** — 라벨 줄 아래 마지막 두 줄은 `approve | 조건부 엣지 | 6 | 6 | 5`와 `approve | while True | 4 | 9 | 3`입니다.
조건부 엣지 모양은 두 번째 수와 첫 번째 수가 줄마다 같았고, 체크포인트가 답마다 하나씩 늘었습니다.
`while True` 모양은 체크포인트가 `2`에 머물다 끝에 하나 늘었고, 부른 횟수는 `1`·`3`·`6`·`9`로 쌓였습니다.

반복문 모양에서 셀마다 늘어난 부름은 둘·셋·셋이었습니다.
노드가 처음부터 다시 실행되어, 반복문도 첫 바퀴부터 다시 돌았기 때문입니다.
공식 문서도 반복문 모양은 첫째 이어 가기 때 한 바퀴를, 둘째 때 두 바퀴를 다시 실행한다고 적습니다.
조건부 엣지 모양은 받은 답마다 노드를 마치고 체크포인트를 남겨, 앞선 답을 다시 받는 부름이 없습니다.

노드가 시작한 횟수(`6`과 `4`)만 보면 조건부 엣지 모양이 더 많습니다.
목록 밖 답마다 노드를 마치고 새로 시작해, 답 하나에 늘 두 번씩 늘었기 때문입니다.
권하는 까닭은 시작 수가 아니라, 답이 늘수록 반복문 쪽에서 더 빨리 늘어난 부른 수에 있습니다.
부른 수를 센 줄은 `interrupt` 바로 앞 줄이라, 01절처럼 그 자리에 쓰기가 있으면 그만큼 되풀이됩니다.

## 6. 사람의 답이 멈춘 질문에 닿지 않을 때

마지막으로, 사람의 답을 넘겼는데 멈춘 질문에 닿지 않는 장면 둘을 봅니다.
01절에서는 멈춤 표시를 쓰려면 체크포인터와 스레드 이름이 있어야 한다는 공식 문서 문장만 보았습니다.
여기서는 둘 가운데 하나씩을 어긋나게 해서 실행하고, 받은 오류를 출력합니다.
오류를 받는 셀은 Ch 2 05절처럼 `try`와 `except 오류이름 as error`로 감쌉니다.
이 `try`는 노드 밖에서 `invoke`를 감싼 것이라, 01절이 권하지 않은 노드 안 감싸기와 다릅니다.

감싸는 `try`가 없으면 이 셀은 오류에서 멈춥니다.
셀에서는 그 오류 이름만 받아 끝까지 실행하지만, 실제 프로그램이라면 여기서 멈춥니다.

다음 셀은 3절의 설계 객체 `edge_builder`를 체크포인터 없이 한 번 더 컴파일합니다.
노드와 조건부 엣지는 3절 그래프와 같습니다.

### [49] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.432409Z', 'iopub.status.busy': '2026-09-25T14:23:57.432369Z', 'iopub.status.idle': '2026-09-25T14:23:57.434696Z', 'shell.execute_reply': '2026-09-25T14:23:57.434358Z'}}

```python
# 3절의 설계 객체를 체크포인터 없이 한 번 더 컴파일하고, 3절과 같은 입력으로 첫 실행을 합니다
plain_graph = edge_builder.compile()
plain_config = {"configurable": {"thread_id": "plain"}}
plain_result = plain_graph.invoke(first_input, plain_config)
print("결과의 키:", list(plain_result))
print("멈춤 표시 수:", len(plain_result["__interrupt__"]))
```

출력:
```
결과의 키: ['order_key', 'answer', 'error', '__interrupt__']
멈춤 표시 수: 1

```

### [50] markdown {}

**결과 읽기** — 출력 줄 `결과의 키: ['order_key', 'answer', 'error', '__interrupt__']`와 `멈춤 표시 수: 1`이 보입니다.
체크포인터가 없어도 첫 실행은 오류 없이 멈춤 표시에서 멈췄습니다.

다음 셀은 같은 설정으로 사람의 답 `approve`를 넘겨 봅니다.
실행 전에 예상해 봅니다.
멈춘 자리가 어디에도 저장되지 않았으니, 이어 갈 수 없을 것입니다.

### [51] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.435216Z', 'iopub.status.busy': '2026-09-25T14:23:57.435173Z', 'iopub.status.idle': '2026-09-25T14:23:57.436983Z', 'shell.execute_reply': '2026-09-25T14:23:57.436651Z'}}

```python
# 체크포인터 없는 그래프에 같은 설정으로 사람의 답 "approve"를 넘겨 봅니다(오류를 받아 출력합니다)
try:
    plain_graph.invoke(Command(resume="approve"), plain_config)
except RuntimeError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:", error)
```

출력:
```
받은 오류: RuntimeError
오류 글: Cannot use Command(resume=...) without checkpointer

```

### [52] markdown {}

**결과 읽기** — 출력 줄 `받은 오류: RuntimeError`와 `오류 글: Cannot use Command(resume=...) without checkpointer`입니다.
오류 글은 체크포인터 없이는 `Command(resume=...)`을 쓸 수 없다는 뜻입니다.
설치판 소스 `langgraph/pregel/_loop.py` 904~908행이 이 오류를 내는 자리입니다.
멈춤 표시가 보였다고 해서, 사람의 답으로 이어 갈 수 있는 것은 아니었습니다.

다음 셀은 체크포인터가 있는 3절 그래프에, 멈춘 적이 없는 새 스레드 이름 `other`로 답을 넘깁니다.
실행 전에 예상해 봅니다.
스레드 `other`에는 멈춘 질문이 없으니, 이 답은 어느 질문에도 닿지 않을 것입니다.

### [53] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.437536Z', 'iopub.status.busy': '2026-09-25T14:23:57.437492Z', 'iopub.status.idle': '2026-09-25T14:23:57.440308Z', 'shell.execute_reply': '2026-09-25T14:23:57.440006Z'}}

```python
# 3절 그래프에, 멈춘 적 없는 스레드 이름 other로 사람의 답 "approve"를 넘겨 봅니다(오류를 받아 출력합니다)
other_config = {"configurable": {"thread_id": "other"}}
try:
    edge_graph.invoke(Command(resume="approve"), other_config)
except KeyError as error:
    print("받은 오류:", type(error).__name__)
    print("오류 글:", error)
```

출력:
```
받은 오류: KeyError
오류 글: 'order_key'

```

### [54] markdown {}

**결과 읽기** — 출력 줄 `받은 오류: KeyError`와 `오류 글: 'order_key'`입니다.
오류 글은 딕셔너리에 키 `order_key`가 없다는 뜻이고, 스레드 이름이 틀렸다고는 알려 주지 않습니다.
무슨 일이 있었는지 다음 셀에서 스레드 `other`의 상태를 읽어 봅니다.

### [55] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.440781Z', 'iopub.status.busy': '2026-09-25T14:23:57.440740Z', 'iopub.status.idle': '2026-09-25T14:23:57.442713Z', 'shell.execute_reply': '2026-09-25T14:23:57.442352Z'}}

```python
# 스레드 other에 남은 칸 값·다음 노드·작업의 오류와, 3절 스레드 edge의 칸 값을 봅니다
other_state = edge_graph.get_state(other_config)
print("스레드 other의 칸 값:", other_state.values)
print("스레드 other의 다음 노드:", other_state.next)
print("멈춘 작업의 오류:", other_state.tasks[0].error)
edge_after = edge_graph.get_state(edge_config)
print("스레드 edge의 칸 값:", edge_after.values)
```

출력:
```
스레드 other의 칸 값: {}
스레드 other의 다음 노드: ('ask_once',)
멈춘 작업의 오류: KeyError('order_key')
스레드 edge의 칸 값: {'order_key': 'order-2402', 'answer': 'approve', 'error': ''}

```

### [56] markdown {}

**결과 읽기** — 출력 줄 `스레드 other의 칸 값: {}`로, 이 스레드에는 칸 값이 하나도 없습니다.
출력 줄 `스레드 other의 다음 노드: ('ask_once',)`와 `멈춘 작업의 오류: KeyError('order_key')`입니다.
그래프가 빈 상태로 노드 `ask_once`를 실행했고, 칸 `order_key`를 읽는 줄에서 오류가 났습니다.
Ch 23 05절처럼 실패한 노드가 다음 노드로 남고, 작업에 오류가 적혔습니다.
출력 줄 `스레드 edge의 칸 값: {'order_key': 'order-2402', 'answer': 'approve', 'error': ''}`는 3절이 끝난 값 그대로입니다.

사람의 답은 멈춘 스레드와 같은 이름으로 보내야 그 질문에 닿습니다.
다음 셀은 작업 폴더에 남은 파일을 봅니다.
이 절은 체크포인트를 메모리에만 저장해, 파일이 없어야 합니다.

### [57] code {'execution': {'iopub.execute_input': '2026-09-25T14:23:57.443232Z', 'iopub.status.busy': '2026-09-25T14:23:57.443191Z', 'iopub.status.idle': '2026-09-25T14:23:57.444830Z', 'shell.execute_reply': '2026-09-25T14:23:57.444507Z'}}

```python
# 작업 폴더에 남은 파일을 봅니다(이 절은 체크포인트를 메모리에만 저장했습니다)
file_names = sorted(os.listdir())
print("작업 폴더의 파일:", file_names)
print("파일 수:", len(file_names))
```

출력:
```
작업 폴더의 파일: []
파일 수: 0

```

### [58] markdown {}

**결과 읽기** — 출력 줄 `작업 폴더의 파일: []`와 `파일 수: 0`입니다.
임시 폴더는 처음처럼 비어 있고, 이 절은 파일을 하나도 쓰지 않았습니다.

## 정리

1. 목록에 없는 답(`maybe`·`yes`)을 받자, 노드가 칸 `error`에 까닭을 적고 조건부 엣지로 같은 노드에서 다시 물었습니다.
2. 노드 안 `while True`로 다시 물어도 결과는 같았지만, 앞선 답을 다시 받는 부름이 쌓여 `interrupt`를 아홉 번 불렀습니다.
3. 체크포인터 없이 답을 넘기면 `RuntimeError`를, 멈춘 적 없는 스레드로 넘기면 `KeyError`를 받았습니다.

03절에서는 지난 체크포인트를 골라 값을 바꾸고, 그 자리부터 다시 실행해 봅니다.

## 그림

### 02-1-조건부-엣지로-다시-묻는-그래프.mmd

```mermaid
flowchart TB
  %% classes
  s(["가상 시작점 START"])
  a["허용 답 목록<br>approve · reject"]:::tool
  h["사람의 답<br>Command resume으로<br>넘김"]:::tool
  n["노드 ask_once<br>interrupt를 한 번 부르고<br>받은 답을 목록으로 검사"]:::flow
  c{"조건 함수<br>after_answer"}
  e(["가상 끝점 END"])
  s --> n
  a --> n
  h --> n
  n --> c
  c -.->|오류 칸에 글 있음<br>이름표 ask_again| n
  c -.->|오류 칸 빈 글<br>이름표 END| e
```

노드는 interrupt를 한 번만 부르고 마치며, 오류 칸에 글이 있으면 조건부 엣지가 같은 노드로 되돌아가 다시 묻습니다.

### 02-2-답마다-본-질문-값과-체크포인트.mmd

```mermaid
flowchart TB
  %% classes
  q1["첫 실행 질문 값<br>주문 키 order-2402<br>오류 글 빈 글 · 체크포인트 둘"]:::measure
  m["사람의 답 maybe"]:::tool
  q2["다음 질문 값 오류 글<br>허용하지 않는 값 maybe<br>노드 두 번 시작<br>체크포인트 셋"]:::measure
  y["사람의 답 yes"]:::tool
  q3["다음 질문 값 오류 글<br>허용하지 않는 값 yes<br>노드 두 번 시작<br>체크포인트 넷"]:::measure
  a["사람의 답 approve"]:::tool
  r["칸 answer approve<br>다음 노드 없음<br>체크포인트 다섯"]:::measure
  q1 --> m
  m --> q2
  q2 --> y
  y --> q3
  q3 --> a
  a --> r
```

목록에 없는 답마다 오류 글이 실린 질문으로 다시 멈췄고, 체크포인트는 답마다 하나씩 늘었습니다.

### 02-3-while-True-노드가-앞선-답을-다시-받는-차례.mmd

```mermaid
flowchart TB
  %% classes
  c["Command<br>resume=approve<br>스레드 loop로 invoke"]:::flow
  s["노드 ask_in_loop를<br>처음부터 다시 실행"]:::flow
  i1["첫째 interrupt<br>소스 확인<br>앞선 답 maybe를 다시 받음"]
  i2["둘째 interrupt<br>소스 확인<br>앞선 답 yes를 다시 받음"]
  i3["셋째 interrupt<br>새 답 approve를 받아<br>노드가 끝남"]:::measure
  r["이 셀에서 부른 횟수 셋<br>누적 아홉 · 체크포인트 셋"]:::measure
  c --> s
  s --> i1
  i1 --> i2
  i2 --> i3
  i3 --> r
```

while True 모양은 이어 갈 때마다 노드를 처음부터 다시 실행했고, 소스 설명대로라면 앞선 답을 부른 차례대로 다시 받습니다.

### 02-4-두-모양의-부른-횟수와-체크포인트.mmd

```mermaid
flowchart TB
  %% classes
  cm["두 모양 같음<br>답 차례<br>maybe · yes · approve<br>질문 값과 마지막 결과가 같음"]
  subgraph E["조건부 엣지 모양 · ask_once"]
    direction TB
    e1["interrupt를 한 번 부르고<br>노드를 마침<br>조건부 엣지로 되돌아감"]:::flow
    e2["interrupt 부른 횟수 누적<br>하나 · 셋 · 다섯 · 여섯"]:::measure
    e3["체크포인트<br>둘 · 셋 · 넷 · 다섯"]:::measure
    e1 --> e2
    e2 ~~~ e3
  end
  subgraph L["while True 모양 · ask_in_loop · 권하지 않음"]
    direction TB
    l1["노드 안 반복문에서<br>interrupt를 되풀이해 부름"]:::flow
    l2["interrupt 부른 횟수 누적<br>하나 · 셋 · 여섯 · 아홉"]:::measure
    l3["체크포인트<br>둘 · 둘 · 둘 · 셋"]:::measure
    l1 --> l2
    l2 ~~~ l3
  end
  cm --> E
  cm --> L
```

같은 답 차례에서 조건부 엣지 모양은 체크포인트가 답마다 하나씩 늘었고, while True 모양은 부른 횟수만 크게 쌓였습니다.

### 02-5-사람의-답이-질문에-닿지-않은-두-장면.mmd

```mermaid
flowchart TB
  %% classes
  cm["두 장면 같음<br>노드 ask_once<br>사람의 답 approve"]
  subgraph P["체크포인터 없이 컴파일"]
    direction TB
    p1["첫 실행은 멈춤 표시 하나"]:::measure
    p2["답을 넘기자 받은 오류<br>RuntimeError"]:::measure
    p1 --> p2
  end
  subgraph O["멈춘 적 없는 스레드 other"]
    direction TB
    o1["답을 넘기자 받은 오류<br>KeyError order_key"]:::measure
    o2["스레드 other 칸 값 없음<br>다음 노드 ask_once"]:::measure
    o1 --> o2
  end
  cm --> P
  cm --> O
```

체크포인터가 없거나 스레드 이름이 다르면, 사람의 답은 멈춘 질문에 닿지 않고 오류가 났습니다.

### 02-6-빈자리에-놓인-구슬과-도미노.prompt.md

# 02-6-빈자리에-놓인-구슬과-도미노 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 01절의 도미노 줄을 다시 봅니다. 가운데 비워 둔 자리에 사람이 도미노가 아닌 둥근 구슬을 놓았다고 합시다. 구슬은 뒤쪽 도미노를 밀지 못해, 줄은 빈자리에서 그대로 멈춰 있습니다. … 빈자리에 맞는 도미노의 모양이 허용 답 목록이고, 구슬을 치우고 다시 기다리는 일이 다시 묻기입니다. 맞는 도미노가 놓여야 뒤쪽 줄이 넘어가는 것은 01절과 같습니다.

구성 요소와 배치: 흰 탁자 **하나**(조금 위에서 봄) · 나무 도미노 **두 줄**(위아래) · 위 줄: 왼쪽 도미노 넘어짐 → 가운데 빈자리에 **파란 구슬 하나**(맞지 않는 물건 = 허용 답 목록에 없는 답 `maybe`) → 구슬 오른쪽 도미노는 **모두 서 있음**(줄이 그대로 멈춤 = 다시 묻는 동안) · 아래 줄: 가운데에 **연두색 도미노 하나**(맞는 도미노 = 목록에 있는 답 `approve`) → 줄 전체가 **오른쪽 끝까지 넘어짐**(이어 감). 비유 계열 **「도미노 줄과 비워 둔 자리」**(챕터 리드 결정 10, 01절이 엶 — 01-5는 컵 두 개, 02는 구슬과 색이 다른 도미노). 「조각」이라는 말은 쓰지 않음. 앞 챕터 소품(도장·쟁반·서랍·바구니·저울·울타리·발자국·공구판·승강 상자·세탁기·체스판·즉석사진·기보·리본)과 01절 컵 없음. 사람·손·화살표·화면·시계·글자·숫자 없음.

시선 순서: 위 줄 왼쪽 넘어진 도미노 → 빈자리의 파란 구슬 → 서 있는 도미노 / 아래 줄 넘어진 도미노 → 가운데 연두색 도미노 → 오른쪽 끝까지 넘어진 도미노.

검수 기준: 그림만 보고 「구슬이 놓인 줄은 멈췄고, 맞는 도미노가 놓인 줄은 끝까지 넘어갔다」가 읽히는가. 줄이 둘이고, 위 줄 빈자리에 구슬 하나·구슬 오른쪽은 서 있음, 아래 줄 가운데 색이 다른 도미노 하나·줄 전체가 넘어짐인가. 글자·숫자·사람·손·컵이 없는가.

## 프롬프트 (1차, 채택)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. Two long straight rows of wooden dominoes on a plain white table, one row in the upper half and one row in the lower half, seen from slightly above. Upper row: the dominoes on the left have fallen flat, then there is one gap in the middle holding one round blue marble, and every domino to the right of the marble still stands upright. Lower row: one pale green domino sits in the middle of the row, and every domino in the row, including the green one, has fallen flat in one continuous line all the way to the right end. No people, no hands, no arrows, no cups, no screens, no clocks, no trays, no drawers, no baskets, no fences, no chess pieces, no photos, no stamps.
```

## 상태

- 2026-09-25 · `nano_banana_pro`(`jobs_wait` 응답 모델 이름 `nano_banana_2` — 01절·Ch 23과 같은 표시) · 16:9 · 2k · `use_unlim: false` · count 1. 생성 전 잔액 **2429.75**(바로 앞 거래 13:52:58Z는 01절 몫).
- **1차 job `1939b15e-9adb-4dfb-affd-cbde22c5aca2` 채택** — 거래 **2026-09-25T14:26:19Z 「Nano Banana Pro −2」**(결과 파일 이름 `hf_20260925_142619_1939b15e…`와 시각이 같음). 이 절 몫은 거래 한 줄, **2크레딧**. 재생성 0회. 결과 원본 `5bba5d1b5efe5921e084e13474332ffb2479859dec653a122e9683ac8c417631`(2752 × 1536).
- **그림에서 확인한 것(그림 읽기·alt에 반영)**: 흰 바탕 위 흰 탁자 하나(조금 위에서 봄). 나무 도미노 두 줄이 위아래로 놓임. **위 줄**: 왼쪽 도미노 다섯이 오른쪽으로 기울어 넘어져 있고(맨 오른쪽 하나는 납작하게 누움), 가운데 빈자리에 **파란 구슬 하나**, 구슬 오른쪽 도미노 일곱이 **모두 서 있음**. **아래 줄**: 가운데에 **연두색 도미노 하나**가 납작하게 누워 있고, 왼쪽 일곱과 오른쪽 일곱이 모두 기울어 넘어져 오른쪽 끝까지 이어짐. 글자·숫자·사람·손·화살표·화면·컵·앞 챕터 소품 없음. 도미노 개수는 본문에서 짝짓지 않음(그림 읽기에 적음).
- 저장: 기기 셸에서 결과 URL을 `curl`로 받아(`/tmp/ch24-02/illu/illu-1-orig.png`) `UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pillow`로 RGB·폭 1100px(LANCZOS)로 줄여 `figures/02-6-빈자리에-놓인-구슬과-도미노.png`(1100 × 614, `8bffb4becf276a45b5fe8eed728612234ecadd1288d533fc28c1acfec1d4ded5`)로 저장했습니다.
- 결과 URL을 한 번 더 받아(`illu-1-again.png`, 원본과 해시 같음) 같은 폭으로 줄인 그림과 저장 PNG를 픽셀 대조했습니다(`ImageChops.difference` bbox `None`, 최대 차이 0). 저장 PNG와 해시가 같은 사본(`.cache/ch24-02-view/illu-1-1100.png`)을 직접 열어 개수를 세고 그림 읽기를 썼습니다.

