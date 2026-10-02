# 07-Persistence-실습

## _src 본문 (HTML 원본)

```html
<!--meta: 실습 30분 | 코드 notebooks/07-Persistence-실습.ipynb | 새 용어 0 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>SQLite 체크포인터를 붙인 그래프를 실패 흉내로 멈추고, 새 연결로 다시 연 그래프에서 이어 갈 수 있습니다.</li>
<li>멈춘 노드가 이어 갈 때 처음부터 다시 실행되는 것을, 부른 횟수와 칸 값으로 확인할 수 있습니다.</li>
<li>쓰기 방식 하나만 바꿔 다시 실행하고, 대출 기록 파일의 줄 수로 두 실행을 견줄 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>이 챕터에서는 상태를 남기고 이어 가는 기능을 절마다 따로 익혔습니다. <a href="03-스레드-재개와-대화-이어가기.html">03절</a>은 체크포인트를 SQLite 파일에 남기고, 새 연결로 같은 스레드를 이어 갔습니다. <a href="05-pending-writes와-장애-복구.html">05절</a>은 실패 흉내로 멈춘 실행을, 원인을 없앤 뒤 <code>invoke(None, config)</code>로 이어 갔습니다. <a href="06-노드-재시작과-멱등성.html">06절</a>은 다시 실행된 노드가 바깥에 한 쓰기를 멱등 키로 한 번만 남겼습니다. 실제 창구 프로그램에서는 이 일들이 한 처리 안에서 함께 일어납니다.</p>
<p>이번 실습은 세 기능을 자료실 대출 처리 한 건에 모아 실행합니다. 쓰기 방식 하나만 바꿔 한 번 더 실행하고, 두 실행을 견줍니다. 06절도 같은 두 쓰기 방식을 견줬고, 그때는 자식 프로세스를 강제로 끝내 노드를 다시 실행하게 했습니다. 새로 볼 것은 같은 커널 안의 실패 흉내로 멈추고 새 연결에서 이어 갈 때도, 같은 차이가 나는지입니다.</p>
<p>이번 절은 이 챕터의 실습입니다. 01~06절에서 쓴 이름과 Ch 2에서 배운 문법만 쓰고, 따로 내는 과제는 없습니다. 강사와 함께 노트북 셀을 차례로 실행합니다.</p>
<p><strong>이 절의 질문</strong> — 대출 기록을 적은 노드가 멈췄다가 이어 가면, 그 노드는 어디서부터 다시 실행될까요? 쓰기 방식 하나를 바꾸면 결과의 어디까지 달라질까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>이번 실습은 아래 절에서 배운 이름을 그대로 씁니다. 함수는 도구 파일 <code>checkpoint_tools.py</code>에서 가져오고, 상태 형식과 노드는 노트북에 적습니다.</p>
<table><thead><tr><th>절</th><th>배운 것</th><th>실습에서 쓰는 곳</th></tr></thead><tbody><tr><td><a href="01-체크포인터와-스레드.html">01절</a></td><td>체크포인터·체크포인트·스레드, 설정 딕셔너리의 <code>thread_id</code>, 같은 스레드로 다시 부를 때의 규칙</td><td>이용자 번호를 스레드 이름으로 쓴 설정 딕셔너리</td></tr><tr><td><a href="03-스레드-재개와-대화-이어가기.html">03절</a></td><td>SQLite 체크포인터(<code>SqliteSaver</code>), 연결을 닫고 새 연결·새 그래프로 같은 스레드 이어 가기</td><td>파일 <code>idempotent-1.sqlite</code>·<code>naive-1.sqlite</code>, 멈춘 뒤 새 연결로 다시 연 그래프</td></tr><tr><td><a href="04-내구-실행-모드-비교.html">04절</a></td><td>함수 <code>read_saved</code>·<code>read_record</code>·<code>new_prefix</code>(도구 파일), 저장 시점의 기본값</td><td>파일에 남은 칸 값·다음 노드·체크포인트 수, 대출 기록 파일의 키, 실행마다 새 파일 앞머리</td></tr><tr><td><a href="05-pending-writes와-장애-복구.html">05절</a></td><td>실패 흉내(<code>TimeoutError</code>·<code>failure_plan</code>)와 부른 횟수(<code>call_count</code>), 원인을 없앤 뒤 <code>invoke(None, config)</code></td><td>둘째 노드의 알림 실패, 이어 갈 때 노드마다 부른 횟수</td></tr><tr><td><a href="06-노드-재시작과-멱등성.html">06절</a></td><td>멱등 키, 함수 <code>append_key</code>·<code>append_key_once</code>(도구 파일), 쓰기 방식 <code>naive</code>·<code>idempotent</code></td><td>대출 키 <code>loan-2307</code>, 둘째 노드의 대출 기록, 실행 2에서 바꾸는 값</td></tr><tr><td><a href="../../part4/ch13-langgraph-basics/02-State-갱신.html">Ch 13 02절</a></td><td>이어 붙이기 규칙 <code>operator.add</code></td><td>칸 <code>notes</code></td></tr></tbody></table>
<p>붙인 기능은 03절 SQLite 체크포인터, 05절 실패 흉내와 이어 가기, 06절 멱등 키 확인 셋입니다. 멱등 키 확인이 흐름 안에서 일하려면, 기록을 적은 노드가 다시 실행되어야 합니다. 그래서 기록을 적는 노드 안에, 기록 뒤에 실패 흉내를 두었습니다. 06절 주의 메모에서 노트북 밖에서만 확인했다고 적은 장면을, 이번에는 노트북에서 실행합니다. 04절 함수 둘은 결과를 읽는 데만 씁니다.</p>
<p><a href="02-PostgresSaver-준비와-스키마.html">02절</a> PostgreSQL 체크포인터는 서버를 따로 켜야 해 뺐습니다. 04절 저장 시점 비교와 강제 종료는 04절과 06절에서 이미 견줬습니다. 자식 프로세스를 띄우면 코드와 실행 시간도 늘어, 이번에는 한 커널 안에서 끝냅니다. 05절의 같은 단계 두 노드와 남은 쓰기는, 노드 하나가 멈추는 이번 흐름에 나오지 않아 뺐습니다. 03절 메시지 칸은 이번 처리에 대화가 없어 뺐습니다.</p>
<p>다른 챕터의 실습은 모델을 몇 번 부르지만, 이 챕터의 실습은 모델을 부르지 않습니다. 01절처럼 매번 같은 값을 내는 우리 노드여야, 파일에 남은 값이 맞는지 출력으로 가를 수 있기 때문입니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p><a href="01-체크포인터와-스레드.html">01절</a>부터 한 수를 둘 때마다 즉석사진을 찍어 판의 모습을 남겼습니다. 06절에서는 판 옆에 기보를 두고, 둔 수를 한 줄씩 적었습니다. 이번에는 판 앞에 사진 한 장과 기보 한 장을 나란히 두고, 리본 하나로 판과 이어 둡니다. 수를 두다가 말 하나가 쓰러지면, 사진을 보고 그 수를 다시 둡니다. 기보에 그 수가 이미 적혀 있으면 다시 적지 않습니다.</p>
{{img:07-4-리본으로-이은-사진과-기보|흰 바탕에 나무 탁자 하나를 조금 위에서 본 그림입니다. 탁자 위쪽에 체스판 하나가 있고, 말들은 대부분 서 있지만 판 가운데의 흰 나이트 하나는 옆으로 누워 있습니다. 판 앞 탁자 위 왼쪽에는 작은 체스판이 찍힌 즉석사진 한 장이, 오른쪽에는 검은 나이트 그림 하나가 그려진 흰 종이 한 장이 있습니다. 빨간 리본 하나가 판 앞 가장자리에서 탁자 앞 끝까지 사진과 종이 사이로 이어지고, 두 물건 사이에 나비매듭이 있습니다. 글자·숫자·사람·카메라는 없는 그림|판 위의 말 하나가 쓰러졌고, 판 앞에는 판을 찍은 사진 한 장과 표시 하나가 적힌 기보 한 장이 리본으로 판과 이어져 있습니다.}}
<p class="look"><b>그림 읽기</b> — 나무 탁자 위쪽에 체스판 하나가 있고, 판 가운데의 흰 나이트 하나만 옆으로 누워 있습니다. 판 앞 왼쪽에는 작은 체스판이 찍힌 즉석사진 한 장, 오른쪽에는 검은 나이트 그림 하나가 그려진 흰 종이 한 장이 있습니다. 빨간 리본 하나가 판 앞 가장자리에서 두 물건 사이를 지나 탁자 끝까지 이어지고, 두 물건 사이에 매듭이 있습니다. 누운 나이트가 멈춘 노드 <code>record_loan</code>, 사진이 SQLite 파일에 남은 마지막 체크포인트, 종이가 대출 기록 파일입니다. 종이의 나이트 그림 하나가 대출 키 한 줄이고, 판 위 말의 개수·색과 판의 칸 수는 무엇과도 짝짓지 않습니다.</p>
<p>리본은 판 앞 가장자리에서 사진과 기보 사이를 지나며, 두 물건이 이 판 하나에 딸린 것임을 보이려고 둔 소품입니다. 말이 쓰러져도 사진이 남아 있으면, 그 자리부터 다시 둘 수 있습니다. 다시 둘 때 기보를 먼저 보면, 이미 적힌 수를 한 번 더 적지 않습니다.</p>
<h3>실습 조립의 구성</h3>
{{mermaid:07-1-세-절-기능을-붙인-대출-처리-그래프|위에서 아래로 읽는 그림입니다. 맨 위에 초록 상자 쓰기 방식 write_plan 실행 1 idempotent 실행 2 naive, 파란 상자 05절 실패 흉내 failure_plan TimeoutError, 파란 상자 06절 append_key_once 도구 파일이 나란히 있고, 세 상자에서 화살표가 파란 상자 노드 record_loan 대출 키를 적은 뒤 알림에서 멈출 수 있음으로 모입니다. 노드 record_loan 오른쪽에는 초록 상자 대출 신청 한 건 스레드 M-0317 대출 키 loan-2307과 회색 상자 03절 SqliteSaver SQLite 파일이 있습니다. 노드 record_loan, invoke 화살표가 붙은 대출 신청, SqliteSaver에서 화살표 셋이 맨 아래 회색 상자 SQLite 체크포인터를 붙인 그래프 노드 receive_request 노드 record_loan으로 모이는 그림|05절 실패 흉내와 06절 함수는 노드 record_loan 안에서 쓰고, 03절 SQLite 체크포인터는 그래프에 붙였습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 파란 상자는 우리가 적은 코드이고, 회색 상자는 라이브러리가 준 체크포인터와 그것을 붙인 그래프입니다. 05절 실패 흉내와 06절 함수는 노드 <code>record_loan</code> 안에서 씁니다. 노드와 대출 신청과 체크포인터에서 온 화살표 셋이 맨 아래 그래프로 모입니다. 초록 상자 둘 가운데 쓰기 방식이 실행 2에서 바꾸는 값이고, 대출 신청은 두 실행에 같게 넣습니다.</p>
<table><thead><tr><th>이름</th><th>하는 일</th><th>가져온 곳</th></tr></thead><tbody><tr><td><code>call_count</code>·<code>failure_plan</code>·<code>write_plan</code></td><td>노드마다 부른 횟수, 실패 흉내, 쓰기 방식과 파일 앞머리</td><td>05절 모양(쓰기 방식 딕셔너리는 이 절에서 더함)</td></tr><tr><td><code>LoanState</code>·<code>receive_request</code>·<code>record_loan</code></td><td>상태 형식과 노드 둘</td><td>06절 모양(칸·노드 이름을 바꾸고 부른 횟수·실패 흉내를 더함)</td></tr><tr><td><code>append_key()</code>·<code>append_key_once()</code></td><td>기록 파일에 키 한 줄 적기, 이미 적힌 키면 건너뛰기</td><td>도구 파일(06절)</td></tr><tr><td><code>read_saved()</code>·<code>read_record()</code>·<code>new_prefix()</code></td><td>새 연결로 파일에 남은 체크포인트 읽기, 기록 파일의 키 목록, 아직 쓰지 않은 파일 앞머리 고르기</td><td>도구 파일(04절)</td></tr></tbody></table>
<h3>두 번의 실행</h3><p>실행 1은 쓰기 방식 <code>idempotent</code>, 실행 2는 <code>naive</code>로 같은 대출 신청을 처리합니다. 두 실행 모두 둘째 노드를 실패 흉내로 멈춘 뒤, 연결을 닫고 새 연결로 연 그래프에서 이어 갑니다. 이용자 번호·대출 키·설계 객체·실패 흉내는 두 실행이 같습니다. 두 실행의 기록이 섞이지 않게, 파일 이름은 쓰기 방식 이름에 번호를 붙인 앞머리로 씁니다. 앞머리는 04절 함수 <code>new_prefix</code>가 고르고, 설정 셀을 다시 실행하면 번호가 올라 새 파일을 씁니다.</p>
<h3>비교와 경계</h3><p>05절에서는 같은 단계의 두 노드 가운데 하나만 멈췄습니다. 먼저 끝난 노드의 쓰기가 체크포인트에 딸려 남아, 이어 갈 때 그 노드는 다시 실행하지 않았습니다. 이번 흐름의 첫째 노드는 앞 단계에서 이미 끝나, 그 결과가 체크포인트에 있습니다. 그래서 이어 갈 때 다시 실행하는 것은 멈춘 둘째 노드뿐입니다.</p><p>멈춘 노드는 첫 줄부터 다시 실행됩니다. 설치판 소스 <code>langgraph/pregel/main.py</code> 2967~2968행은 이어 갈 때 쓰기가 없는 작업만 실행하고, 05절에서도 본 자리입니다. 체크포인트는 칸 값과 칸에 낸 갱신만 담습니다. 그래서 노드가 바깥에 한 쓰기는 06절처럼 노드 스스로 한 번만 반영되게 적어야 합니다.</p><p>세 딕셔너리도 체크포인트 밖에 있습니다. 부른 횟수가 이어 가는 동안 계속 늘어난 것도, 실행 2 전에 코드로 처음 값에 맞춘 것도 그 때문입니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 오늘 처리할 대출 한 건의 값을 정하고, 세 딕셔너리·상태 형식·노드 둘·설계 객체를 만듭니다. 실행 1은 파일 <code>idempotent-1.sqlite</code>로 둘째 노드를 멈춘 뒤, 연결을 닫고 새 그래프로 이어 갑니다. 실행 2는 쓰기 방식 하나만 <code>naive</code>로 바꿔 같은 차례를 되풀이하고, 마지막에 두 실행을 견줍니다.</p><p>이 절은 모델을 부르지 않아 모델 요청은 0번이고, API 키 셀도 없습니다. 자식 프로세스는 띄우지 않습니다. SQLite 파일과 대출 기록 파일은 노트북이 만든 빈 임시 폴더에 생깁니다.</p>
{{notebook:07-Persistence-실습}}
<p class="look"><b>확인할 점</b> — 노트북 5절에서 <code>다음 노드: ('record_loan',)</code>과 <code>멈추기 전에 적힌 키: ['loan-2307']</code>을 봅니다. 이어 간 뒤 <code>부른 횟수: {'receive_request': 1, 'record_loan': 2}</code>와 <code>같은 키가 적힌 줄 수: 1</code>인지 확인합니다. 6절에서는 <code>같은 키가 적힌 줄 수: 2</code>를 보고, 7절 두 줄로 두 실행을 맞춰 봅니다.</p>
<h3>실행 1의 실제 순서</h3>
{{mermaid:07-2-실행-1의-실제-차례|위에서 아래로 상자 일곱이 한 줄로 이어진 흐름도입니다. 첫 파란 상자는 invoke 대출 신청 스레드 M-0317 receive_request 마침, 둘째 파란 상자는 record_loan 대출 키를 적은 뒤 실패 흉내로 멈춤입니다. 셋째 노란 상자는 받은 오류 TimeoutError 부른 횟수 두 노드 한 번씩, 넷째 노란 상자는 파일에 남은 것 다음 노드 record_loan 체크포인트 셋 기록 파일 키 한 줄입니다. 다섯째 파란 상자는 연결을 닫고 새 연결 새 그래프 실패 흉내를 끄고 invoke None, 여섯째 파란 상자는 record_loan을 처음부터 다시 실행 키를 찾아 건너뜀입니다. 일곱째 노란 상자는 이어 간 뒤 receive_request 한 번 record_loan 두 번 칸 notes 신청 받음 건너뜀 체크포인트 넷 기록 파일 키 한 줄인 그림|실행 1에서 record_loan은 대출 키를 적은 뒤 멈췄고, 새 그래프로 이어 갈 때 처음부터 다시 실행되어 키를 건너뛰었습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 한 줄로 읽습니다. 파란 상자는 우리가 부른 코드와 노드가 한 일이고, 노란 상자는 노트북 5절 출력입니다. 셋째·넷째 상자가 멈춘 뒤 남은 것이고, 다섯째 상자에서 새 연결로 파일을 다시 엽니다. 맨 아래 상자에서 <code>record_loan</code>은 두 번 불렸지만, 기록 파일의 키는 넷째 상자와 같은 한 줄입니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>두 실행은 쓰기 방식 하나만 달랐습니다. 결과는 아래 표와 같았습니다.</p>
<table><thead><tr><th>실행</th><th>쓰기 방식</th><th>멈춘 뒤 다음 노드<br>체크포인트 수 · 적힌 키</th><th>이어 간 뒤 부른 횟수</th><th>이어 간 뒤 칸 <code>notes</code><br>체크포인트 수</th><th>같은 키가 적힌 줄 수</th></tr></thead><tbody><tr><td>실행 1</td><td><code>idempotent</code></td><td><code>('record_loan',)</code><br>3 · <code>['loan-2307']</code></td><td><code>{'receive_request': 1, 'record_loan': 2}</code></td><td><code>['신청 받음', '건너뜀']</code><br>4</td><td>1</td></tr><tr><td>실행 2(바꾼 값)</td><td><code>naive</code></td><td><code>('record_loan',)</code><br>3 · <code>['loan-2307']</code></td><td><code>{'receive_request': 1, 'record_loan': 2}</code></td><td><code>['신청 받음', '적음']</code><br>4</td><td>2</td></tr></tbody></table>
{{mermaid:07-3-쓰기-방식만-바꾼-두-실행|맨 위 초록 상자 바꾼 값 하나 쓰기 방식 실행 1 idempotent 실행 2 naive에서 아래 칸 둘로 화살표가 갑니다. 왼쪽 칸 실행 1 idempotent에는 파란 상자 다시 실행한 record_loan append_key_once가 키를 찾아 건너뜀에서 노란 상자 기록 파일에 같은 키 한 줄 칸 notes 신청 받음 건너뜀으로 화살표가 갑니다. 오른쪽 칸 실행 2 naive에는 파란 상자 다시 실행한 record_loan append_key가 검사 없이 한 줄 더에서 노란 상자 기록 파일에 같은 키 두 줄 칸 notes 신청 받음 적음으로 화살표가 갑니다. 맨 아래 회색 상자에 두 실행 같음 멈춘 뒤 다음 노드 record_loan 체크포인트 셋 이어 간 뒤 체크포인트 넷 receive_request 한 번 record_loan 두 번이 적힌 그림|쓰기 방식만 바꾸자 기록 파일의 같은 키 줄 수가 한 줄에서 두 줄로 바뀌었고, 멈춘 자리와 부른 횟수는 같았습니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 초록 상자는 두 실행에서 바꾼 값 하나입니다. 왼쪽 칸이 실행 1, 오른쪽 칸이 실행 2이고, 칸 안은 위에서 아래로 다시 실행한 <code>record_loan</code>이 한 일과 그 결과입니다. 노란 상자는 노트북 5·6절 출력이고, 맨 아래 회색 상자는 두 실행 출력에서 모두 확인한 공통점입니다. 두 칸끼리는 화살표로 잇지 않았습니다.</p>
<p>두 실행 모두 둘째 노드는 기록을 적은 뒤 멈췄고, 파일에는 첫째 노드까지의 체크포인트 셋이 남았습니다. 새 연결로 연 그래프는 두 실행 모두 멈춘 자리를 읽었고, 둘째 노드만 처음부터 다시 실행했습니다. 부른 횟수와 체크포인트 수는 두 실행이 같았습니다.</p><p>달라진 것은 다시 실행된 <code>record_loan</code>이 한 일입니다. 쓰기 방식 <code>idempotent</code>는 기록 파일에서 키를 찾아 <code>건너뜀</code>을 냈고, 대출 기록은 한 줄이었습니다. 쓰기 방식 <code>naive</code>는 검사 없이 한 줄을 더 적어, 같은 키가 두 줄 남았습니다. 06절 주의 메모가 노트북 밖에서 본 결과와 같은 차이입니다.</p><p>모델을 부르지 않아, 이 값들은 새 커널로 다시 실행해도 같아야 합니다. 새 커널로 두 번 실행했을 때 코드 셀 22개의 출력이 모두 같았습니다. 노트북 밖 준비 확인에서도 같은 흐름을 열 번 되풀이해, 한 번도 다른 값이 나오지 않았습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>대출 키 <code>loan-2307</code>은 이 절에서 실행 전에 정한 값입니다. 이용자 번호 <code>M-0317</code>은 <a href="../ch21-create-agent/03-AgentState와-context-schema.html">Ch 21 03절</a> 값 그대로이고, 실제 이용자와 대출이 아닙니다.</li><li>대출 기록과 알림은 실제 서비스를 부르지 않았습니다. 기록은 파일 한 줄로, 알림은 실패 흉내로만 대신했습니다.</li><li>실패 흉내는 기록을 적은 뒤에 두었습니다. 기록을 적기 전에 멈추는 장면은 이번에 실행하지 않았습니다.</li><li>06절 주의 메모는 실패 흉내로 멈춘 뒤 이어 가는 장면을 노트북 밖에서만 확인했다고 적었습니다. 이 실습은 그 장면을 노트북에서 실행했고, 두 쓰기 방식의 줄 수도 06절 메모와 같았습니다.</li><li>부른 횟수·실패 흉내·쓰기 방식 딕셔너리는 체크포인트 밖에 있습니다. 그래서 실행 2를 시작하기 전에 코드로 처음 값에 다시 맞췄습니다.</li><li>두 실행은 파일을 따로 썼습니다. 스레드 이름이 같아, 한 파일을 함께 쓰면 01절의 규칙대로 실행 2가 실행 1의 스레드에 이어 붙게 됩니다. 그 장면은 이번에 실행하지 않았습니다.</li><li>설정 셀은 3절 딕셔너리 셀과 6절 첫 셀입니다. 이 셀을 다시 실행하면 파일 앞머리의 번호가 올라, 앞 실행의 파일과 섞이지 않는 새 파일을 씁니다. 그래서 실행 하나를 그 설정 셀부터 다시 실행해도 같은 결과가 나옵니다.</li><li>실패 원인을 없애지 않고 이어 가는 장면은 이번에 실행하지 않았습니다. 05절 노트북 밖 확인에서는 같은 실패 흉내로 다시 멈췄습니다.</li><li>저장 시점은 적지 않아 기본값으로 실행했습니다. 다른 저장 시점과 강제 종료는 이번에 실행하지 않았습니다.</li><li>이 절의 멱등 키 확인은 06절처럼 기록 파일을 읽은 뒤에 적습니다. 여러 프로그램이 같은 파일에 함께 쓰는 장면은 이번에 실행하지 않았습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13과 SQLite 3.53.1로 만들었습니다. Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>대출 기록을 적은 노드가 실패 흉내로 멈추자, 체크포인트에는 그 노드의 갱신이 없고 기록 파일에는 한 줄이 남았습니다.</li><li>새 연결로 연 그래프가 <code>None</code>으로 이어 가자, 첫째 노드는 두고 멈춘 노드만 처음부터 다시 실행했습니다.</li><li>쓰기 방식 <code>idempotent</code>는 대출 기록을 한 줄, <code>naive</code>는 같은 키를 두 줄 남겼습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 이 절로 Ch 23이 끝납니다. <a href="../ch24-human-in-the-loop/01-interrupt-승인-게이트.html">Ch 24 01절</a>에서는 되돌리기 어려운 일을 하기 전에, 사람이 확인하는 자리에서 그래프를 멈추는 방법을 다룹니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. [하] 두 실행에서 바꾼 값은 무엇이고, 같게 둔 것은 무엇입니까?</p><p class="quiz-a">쓰기 방식을 <code>idempotent</code>에서 <code>naive</code>로 바꿨습니다. 이용자 번호·대출 키·설계 객체·실패 흉내·이어 가는 방법은 같게 두었습니다. 파일 이름은 두 실행의 기록이 섞이지 않게 쓰기 방식 이름에 번호를 붙인 앞머리로 썼습니다.</p><p class="quiz-q">2. [중] 멈춘 뒤 체크포인트에는 <code>record_loan</code>이 낸 글이 없는데, 기록 파일에 키가 한 줄 있었던 까닭은 무엇입니까?</p><p class="quiz-a">노드 <code>record_loan</code>이 기록을 적은 뒤 실패 흉내로 멈췄기 때문입니다. 칸에 낼 갱신은 노드가 끝나야 저장되지만, 파일 쓰기는 이미 끝나 있었습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">3. [중] 이어 갈 때 <code>receive_request</code>는 다시 불리지 않고 <code>record_loan</code>은 다시 불린 까닭은 무엇입니까?</p><p class="quiz-a">첫째 노드는 앞 단계에서 끝나 그 결과가 체크포인트에 있었습니다. 둘째 노드는 끝나지 못해 갱신이 저장되지 않았고, 그래서 처음부터 다시 실행했습니다. 부른 횟수 <code>{'receive_request': 1, 'record_loan': 2}</code>로 확인했습니다. 틀렸다면 노트북 5절과 05절을 다시 읽습니다.</p><p class="quiz-q">4. [상] 동료가 「체크포인터를 SQLite 파일에 두었으니, 멈췄다 이어 가도 대출 기록은 한 번만 남는다」고 말합니다. 이 절 결과로 무엇이라고 답하나요?</p><p class="quiz-a">그렇지 않다고 답합니다. 체크포인트는 칸 값과 칸에 낸 갱신만 담고, 노드가 바깥 파일에 쓴 줄은 담지 않습니다. 쓰기 방식 <code>naive</code>에서는 같은 키가 두 줄 남았습니다. 한 줄만 남긴 것은 멱등 키를 확인한 <code>append_key_once</code>였습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li>01절 — 체크포인터·스레드와 설정 딕셔너리의 <code>thread_id</code>.</li><li>03절 — SQLite 체크포인터와, 새 연결·새 그래프로 이어 가기.</li><li>04절 — 함수 <code>read_saved</code>·<code>read_record</code>와 저장 시점의 기본값.</li><li>05절 — 실패 흉내와 <code>invoke(None, config)</code>.</li><li>06절 — 멱등 키와 함수 <code>append_key</code>·<code>append_key_once</code>.</li><li>langgraph 1.2.11 소스 <code>langgraph/pregel/main.py</code> 2967~2968행 — 이어 갈 때 쓰기가 없는 작업만 실행하는 자리입니다.</li><li>같은 판 <code>langgraph/pregel/_loop.py</code> 856행·861~865행 — 입력이 <code>None</code>이면 이어 가는 것으로 보는 자리입니다.</li><li>기준 버전은 노트북 1절 첫 셀에서 설치한 패키지 둘의 판입니다.</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# Persistence 실습: 멈춘 대출 처리를 이어 가고 기록은 한 번만 남기기

**이 노트북에서 할 일**

1. 대출 신청 한 건을 처리하는 그래프에 SQLite 체크포인터와 멱등 키 확인을 붙입니다.
2. 대출 기록을 적은 노드를 실패 흉내로 멈추고, 새 연결로 파일을 다시 열어 이어 갑니다.
3. 쓰기 방식 하나만 바꿔 다시 실행하고, 대출 기록 파일의 줄 수로 두 실행을 견줍니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
01절처럼 매번 같은 값을 내는 우리 노드로, 저장된 값이 맞는지 출력으로 가릅니다.

실패는 모두 이 절에서 일부러 만든 실패 흉내입니다.
대출 기록은 실제 서비스가 아니라, 기록 파일에 대출 키를 한 줄 적는 것으로 대신합니다.
자식 프로세스는 띄우지 않고, 모든 일을 이 커널 안에서 합니다.

노트북은 빈 임시 폴더를 만들어 그 폴더에서 실행합니다.
SQLite 파일과 대출 기록 파일은 이 임시 폴더에 생기고, 실습 폴더에는 파일을 남기지 않습니다.
읽어 오는 자료 파일은 없습니다.

걸린 시간은 재지 않습니다.
교재 출력을 만든 실행에서는 노트북 전체가 5초 안에 끝났습니다.
설치 셀에 걸리는 시간은 네트워크에 따라 달라집니다.

**기준 버전** — 첫 셀에서 패키지 둘을 설치합니다.
그래프는 langgraph 1.2.11입니다.
SQLite 체크포인터는 langgraph-checkpoint-sqlite 3.0.3에 들어 있습니다.

교재 출력은 Linux의 Python 3.12.13과, 그 Python에 들어 있는 SQLite 3.53.1로 만들었습니다.
Windows·macOS에서는 실행하지 않았습니다.

**실습 범위** — 이 절은 챕터 끝 실습 절이고 30분 안에 끝나는 분량입니다.
강사와 함께 첫 셀부터 차례로 실행하고, 따로 내는 과제는 없습니다.
01~06절에서 쓴 이름과 Ch 2에서 배운 문법만 씁니다.

실습 폴더 `labs/part6/ch23-persistence`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 읽는 그림입니다. 맨 위에 초록 상자 쓰기 방식 write_plan 실행 1 idempotent 실행 2 naive, 파란 상자 05절 실패 흉내 failure_plan TimeoutError, 파란 상자 06절 append_key_once 도구 파일이 나란히 있고, 세 상자에서 화살표가 파란 상자 노드 record_loan 대출 키를 적은 뒤 알림에서 멈출 수 있음으로 모입니다. 노드 record_loan 오른쪽에는 초록 상자 대출 신청 한 건 스레드 M-0317 대출 키 loan-2307과 회색 상자 03절 SqliteSaver SQLite 파일이 있습니다. 노드 record_loan, invoke 화살표가 붙은 대출 신청, SqliteSaver에서 화살표 셋이 맨 아래 회색 상자 SQLite 체크포인터를 붙인 그래프 노드 receive_request 노드 record_loan으로 모이는 그림](attachment:07-1-세-절-기능을-붙인-대출-처리-그래프.png)

위에서 아래로 읽습니다.
파란 상자는 우리가 적은 코드이고, 회색 상자는 라이브러리가 준 체크포인터와 그것을 붙인 그래프입니다.
05절 실패 흉내와 06절 함수는 노드 `record_loan` 안에서 씁니다.
노드와 대출 신청과 체크포인터에서 온 화살표 셋이 맨 아래 그래프로 모입니다.
초록 상자 둘 가운데 쓰기 방식이 실행 2에서 바꾸는 값이고, 대출 신청은 두 실행에 같게 넣습니다.

### [2] markdown {}

## 1. 준비

이번 절은 이 챕터의 실습입니다.
03절 SQLite 체크포인터, 05절 실패 흉내와 이어 가기, 06절 멱등 키 확인을 대출 처리 한 건에 모읍니다.
첫 셀은 패키지 둘을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:31.665020Z', 'iopub.status.busy': '2026-09-25T12:36:31.664830Z', 'iopub.status.idle': '2026-09-25T12:36:32.096778Z', 'shell.execute_reply': '2026-09-25T12:36:32.096156Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "langgraph==1.2.11" "langgraph-checkpoint-sqlite==3.0.3"
from importlib.metadata import version

print("langgraph:", version("langgraph"))
print("langgraph-checkpoint-sqlite:", version("langgraph-checkpoint-sqlite"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
langgraph: 1.2.11
langgraph-checkpoint-sqlite: 3.0.3

```

### [4] markdown {}

**결과 읽기** — 출력 줄 `langgraph: 1.2.11`과 `langgraph-checkpoint-sqlite: 3.0.3`이 보입니다.
두 판 모두 실습 폴더 잠금과 같은 판입니다.
이 노트북의 출력은 2026-09-25에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
상태 형식과 그래프 이름은 Ch 13 01·02절, `sqlite3`와 `SqliteSaver`는 03절과 같습니다.
마지막 줄은 04절과 06절에서 배운 함수 다섯을 도구 파일 `checkpoint_tools.py`에서 가져옵니다.
이 절에서 새로 가져오는 이름은 없습니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.098136Z', 'iopub.status.busy': '2026-09-25T12:36:32.098041Z', 'iopub.status.idle': '2026-09-25T12:36:32.604711Z', 'shell.execute_reply': '2026-09-25T12:36:32.604288Z'}, 'lesson_role': 'setup'}

```python
# 그래프 이름(Ch 13 01·02절)과 SQLite 체크포인터(03절)를 가져오고, 04·06절에서 배운 함수 다섯을 도구 파일에서 가져옵니다
import operator
import sqlite3
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from checkpoint_tools import append_key, append_key_once, new_prefix, read_record, read_saved

print("도구 파일에서 가져온 함수:", "append_key, append_key_once, new_prefix, read_record, read_saved")
```

출력:
```
도구 파일에서 가져온 함수: append_key, append_key_once, new_prefix, read_record, read_saved

```

### [6] markdown {}

**결과 읽기** — 출력 줄 `도구 파일에서 가져온 함수: append_key, append_key_once, new_prefix, read_record, read_saved`가 보입니다.
함수 `read_saved`·`read_record`·`new_prefix`는 04절 노트북 3절에서 처음 적은 함수입니다.
함수 `append_key`와 `append_key_once`는 06절 노트북 2절에서 처음 적은 함수입니다.
이 절에서 도구 파일에 더한 함수는 없습니다.

앞에서 배운 함수는 `checkpoint_tools.py`에 모아 두었습니다.
파일을 열면 코드를 볼 수 있습니다.
노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.
그래서 임시 폴더로 작업 위치를 옮기기 전에 가져왔습니다.

교재 출력은 프로젝트 맨 위에서 커널을 띄운 실행입니다.
실행 도구가 도구 파일 폴더를 따로 알려 주어, 그 자리에서도 가져오기가 되었습니다.

다음 셀은 01절처럼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다.
이 절의 SQLite 파일과 대출 기록 파일은 모두 이 임시 폴더에 생깁니다.

### [7] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.605379Z', 'iopub.status.busy': '2026-09-25T12:36:32.605317Z', 'iopub.status.idle': '2026-09-25T12:36:32.607338Z', 'shell.execute_reply': '2026-09-25T12:36:32.606982Z'}, 'lesson_role': 'setup'}

```python
# 파일이 생기는지 볼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다(Ch 4 03절과 같은 모양)
import os
import tempfile

# mkdtemp()는 운영체제 임시 폴더 안에 새 폴더를 만들고, 그 폴더의 위치를 글로 내놓습니다
practice_folder = tempfile.mkdtemp(prefix="ch23-07-")
# chdir()는 터미널의 cd처럼 현재 작업 폴더를 옮깁니다
os.chdir(practice_folder)
print("임시 폴더 이름에 ch23-07-이 들어 있는가:", "ch23-07-" in practice_folder)
print("현재 작업 폴더의 파일:", os.listdir())
```

출력:
```
임시 폴더 이름에 ch23-07-이 들어 있는가: True
현재 작업 폴더의 파일: []

```

### [8] markdown {}

**결과 읽기** — 출력 줄 `임시 폴더 이름에 ch23-07-이 들어 있는가: True`로, 이 절의 폴더를 만들었습니다.
출력 줄 `현재 작업 폴더의 파일: []`로, 빈 폴더에서 시작합니다.

## 2. 오늘 처리할 대출 한 건

이번 실습은 자료실 창구에 들어온 대출 신청 한 건을 처리합니다.
처리는 노드 둘로 나눕니다.
첫째 노드는 신청을 받고, 둘째 노드는 대출 기록 파일에 대출 키를 적은 뒤 이용자에게 알림을 보냅니다.
알림은 실제로 보내지 않고, 보내다가 시간이 초과되는 실패 흉내만 냅니다.

다음 셀은 오늘 쓸 두 값을 정하고 출처와 함께 출력합니다.
두 값 모두 실행 전에 정했습니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.607876Z', 'iopub.status.busy': '2026-09-25T12:36:32.607820Z', 'iopub.status.idle': '2026-09-25T12:36:32.609682Z', 'shell.execute_reply': '2026-09-25T12:36:32.609357Z'}}

```python
# 오늘 처리할 대출 신청 한 건의 값 둘을 정합니다(실행 전에 정한 값)
member_id = "M-0317"
loan_key = "loan-2307"
print("이용자 번호:", member_id)
print("이용자 번호 출처: Ch 21 03절 실행 정보의 이용자 번호 그대로")
print("대출 키:", loan_key)
print("대출 키 출처: 이 절에서 실행 전에 정한 값(06절 주문 키 order-2306과 같은 모양)")
```

출력:
```
이용자 번호: M-0317
이용자 번호 출처: Ch 21 03절 실행 정보의 이용자 번호 그대로
대출 키: loan-2307
대출 키 출처: 이 절에서 실행 전에 정한 값(06절 주문 키 order-2306과 같은 모양)

```

### [10] markdown {}

**결과 읽기** — 출력 줄 `이용자 번호: M-0317`과 `대출 키: loan-2307`로 오늘 쓸 값을 확인합니다.
이용자 번호는 스레드 이름으로 씁니다.
01절에서 본 대로, 스레드 이름은 설정 딕셔너리의 `thread_id`에 적습니다.

대출 키는 06절의 주문 키처럼 멱등 키로 씁니다.
같은 대출이면 다시 실행해도 늘 같은 값이어야 합니다.
두 실행 모두 같은 이용자 번호와 같은 대출 키를 씁니다.

## 3. 재료 · 딕셔너리 셋과 상태 형식, 노드 둘

다음 셀은 05절처럼 노드마다 부른 횟수를 셀 딕셔너리와, 실패 흉내를 정할 딕셔너리를 만듭니다.
05절의 `failure_plan`에서 기다릴 초는 뺐습니다.
이번 그래프에는 같은 단계에서 함께 실행되는 노드가 없기 때문입니다.
셋째 딕셔너리 `write_plan`은 대출 기록을 적는 쓰기 방식과, 파일 이름의 앞머리를 정합니다.

앞머리는 04절 함수 `new_prefix`로, 쓰기 방식 이름 뒤에 번호를 붙여 고릅니다.
이 셀을 다시 실행하면 번호가 올라, 앞 실행의 파일과 섞이지 않는 새 파일을 씁니다.
그래서 실행 1을 처음부터 다시 보려면 이 셀부터, 실행 2는 6절 첫 셀부터 차례로 다시 실행합니다.

### [11] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.610256Z', 'iopub.status.busy': '2026-09-25T12:36:32.610205Z', 'iopub.status.idle': '2026-09-25T12:36:32.611993Z', 'shell.execute_reply': '2026-09-25T12:36:32.611703Z'}}

```python
# 노드마다 부른 횟수, 실패 흉내, 쓰기 방식과 파일 앞머리를 정할 딕셔너리 셋을 만듭니다(05절 모양)
call_count = {"receive_request": 0, "record_loan": 0}
failure_plan = {"fail": True}
# 실행 1의 쓰기 방식은 이미 적힌 키를 건너뛰는 idempotent입니다
write_plan = {"mode": "idempotent"}
# 파일 앞머리는 쓰기 방식 이름에 번호를 붙여 고릅니다(04절 함수 — 이 셀을 다시 실행하면 새 번호)
write_plan["prefix"] = new_prefix(write_plan["mode"])
print("부른 횟수:", call_count)
print("실패 흉내:", failure_plan)
print("쓰기 방식:", write_plan)
```

출력:
```
부른 횟수: {'receive_request': 0, 'record_loan': 0}
실패 흉내: {'fail': True}
쓰기 방식: {'mode': 'idempotent', 'prefix': 'idempotent-1'}

```

### [12] markdown {}

**결과 읽기** — 출력 줄 `부른 횟수: {'receive_request': 0, 'record_loan': 0}`과 `실패 흉내: {'fail': True}`입니다.
출력 줄 `쓰기 방식: {'mode': 'idempotent', 'prefix': 'idempotent-1'}`가 실행 1의 설정입니다.
실행 2에서는 쓰기 방식 하나만 바꾸고, 앞머리는 그 이름을 따라 새로 고릅니다.
값 `idempotent`는 06절 `append_key_once`로, 값 `naive`는 `append_key`로 적는다는 뜻입니다.
세 딕셔너리는 체크포인트 밖에 있고, 노드가 노트북에서 만든 이름 그대로 읽고 고칩니다.

다음 셀은 상태 형식입니다.
칸 `loan_key`에 대출 키를, 칸 `notes`에 노드가 한 일을 담습니다.
06절 `OrderState`와 모양은 같고, 칸 이름이 달라 새 이름 `LoanState`를 붙입니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.612526Z', 'iopub.status.busy': '2026-09-25T12:36:32.612481Z', 'iopub.status.idle': '2026-09-25T12:36:32.613882Z', 'shell.execute_reply': '2026-09-25T12:36:32.613608Z'}}

```python
# 대출 키 칸과, 노드가 한 일을 이어 붙이는 칸을 둔 상태 형식을 만듭니다(06절 OrderState와 같은 모양)
class LoanState(TypedDict):
    loan_key: str
    notes: Annotated[list[str], operator.add]
```

출력:
```

```

### [14] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 `notes`에는 Ch 13 02절의 이어 붙이기 규칙을 적었습니다.

다음 셀은 첫째 노드 `receive_request`입니다.
부른 횟수에 1을 더하고, 한 일 `신청 받음`을 칸 `notes`에 냅니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.614472Z', 'iopub.status.busy': '2026-09-25T12:36:32.614426Z', 'iopub.status.idle': '2026-09-25T12:36:32.615904Z', 'shell.execute_reply': '2026-09-25T12:36:32.615551Z'}}

```python
# 첫째 노드: 부른 횟수에 1을 더하고, 한 일 "신청 받음"을 목록에 담아 냅니다
def receive_request(state):
    call_count["receive_request"] = call_count["receive_request"] + 1
    return {"notes": ["신청 받음"]}
```

출력:
```

```

### [16] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 둘째 노드 `record_loan`입니다.
쓰기 방식대로 대출 기록 파일에 대출 키를 적고, 실패 흉내가 켜져 있으면 `TimeoutError`를 냅니다.
오류 메시지는 05절 실패 흉내와 같은 글입니다.
기록 파일 이름은 `write_plan`에 담은 앞머리 뒤에 끝말을 붙여, 두 실행의 기록이 섞이지 않게 합니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.616485Z', 'iopub.status.busy': '2026-09-25T12:36:32.616432Z', 'iopub.status.idle': '2026-09-25T12:36:32.618390Z', 'shell.execute_reply': '2026-09-25T12:36:32.618091Z'}}

```python
# 둘째 노드: 쓰기 방식대로 대출 키를 기록 파일에 적은 뒤, 실패 흉내가 켜져 있으면 알림을 보내다 멈춥니다
def record_loan(state):
    call_count["record_loan"] = call_count["record_loan"] + 1
    record_name = write_plan["prefix"] + ".record"
    if write_plan["mode"] == "idempotent":
        note = append_key_once(record_name, state["loan_key"])
    else:
        note = append_key(record_name, state["loan_key"])
    # 알림은 실제로 보내지 않고, 시간 초과처럼 멈추는 실패 흉내만 냅니다
    if failure_plan["fail"]:
        raise TimeoutError("이 절에서 만든 실패 흉내입니다.")
    return {"notes": [note]}
```

출력:
```

```

### [18] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
기록 파일에 적는 줄이 실패 흉내보다 앞에 있습니다.
그래서 실패 흉내로 멈추면, 칸에 낼 글은 없어도 기록 파일에는 이미 한 줄이 적혀 있습니다.

다음 셀은 두 노드를 차례로 잇는 설계 객체를 만듭니다.
06절 설계 객체와 같은 모양이고, 상태 형식과 노드 이름만 다릅니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.618876Z', 'iopub.status.busy': '2026-09-25T12:36:32.618833Z', 'iopub.status.idle': '2026-09-25T12:36:32.620983Z', 'shell.execute_reply': '2026-09-25T12:36:32.620629Z'}}

```python
# 노드 둘을 START → receive_request → record_loan → END로 잇는 설계 객체를 만듭니다
builder = StateGraph(LoanState)
builder.add_node("receive_request", receive_request)
builder.add_node("record_loan", record_loan)
builder.add_edge(START, "receive_request")
builder.add_edge("receive_request", "record_loan")
builder.add_edge("record_loan", END)
print("등록한 노드:", list(builder.nodes))
```

출력:
```
등록한 노드: ['receive_request', 'record_loan']

```

### [20] markdown {}

**결과 읽기** — 출력 줄 `등록한 노드: ['receive_request', 'record_loan']`입니다.
설계 객체 `builder`는 두 실행에 함께 씁니다.

## 4. 결과를 볼 기록 장치

결과는 04절 함수 둘로 봅니다.
함수 `read_saved`는 새 연결로 SQLite 파일을 열어, 한 스레드의 칸 값·다음 노드·체크포인트 수를 읽습니다.
읽은 뒤에는 연결을 닫습니다.
함수 `read_record`는 기록 파일의 줄을 목록으로 내놓습니다.

## 5. 실행 1 · 멈춘 처리를 새 연결에서 이어 가기

다음 셀은 03절처럼 실행 1의 SQLite 파일에 연결을 열고, SQLite 체크포인터를 붙여 컴파일합니다.
파일 이름은 3절에서 고른 앞머리 뒤에 끝말 `.sqlite`를 붙인 이름입니다.
스레드 이름은 이용자 번호이고, 설정 딕셔너리는 두 실행에 함께 씁니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.621502Z', 'iopub.status.busy': '2026-09-25T12:36:32.621455Z', 'iopub.status.idle': '2026-09-25T12:36:32.623885Z', 'shell.execute_reply': '2026-09-25T12:36:32.623528Z'}}

```python
# 실행 1의 SQLite 파일(앞머리 + .sqlite)에 연결을 열고, SQLite 체크포인터를 붙여 설계 객체를 컴파일합니다(03절 모양)
one_prefix = write_plan["prefix"]
one_conn = sqlite3.connect(one_prefix + ".sqlite", check_same_thread=False)
one_saver = SqliteSaver(one_conn)
one_graph = builder.compile(checkpointer=one_saver)
# 스레드 이름은 이용자 번호이고, 이 설정 딕셔너리를 두 실행에 함께 씁니다
config = {"configurable": {"thread_id": member_id}}
print("SQLite 파일 이름:", one_prefix + ".sqlite")
print("붙은 체크포인터의 종류:", type(one_graph.checkpointer).__name__)
print("스레드 이름:", config["configurable"]["thread_id"])
```

출력:
```
SQLite 파일 이름: idempotent-1.sqlite
붙은 체크포인터의 종류: SqliteSaver
스레드 이름: M-0317

```

### [22] markdown {}

**결과 읽기** — 출력 줄 `SQLite 파일 이름: idempotent-1.sqlite`·`붙은 체크포인터의 종류: SqliteSaver`·`스레드 이름: M-0317`입니다.

다음 셀은 대출 신청을 입력으로 넣어 실행하고, 실패 흉내를 받아 출력합니다.
저장 시점은 적지 않아, 04절에서 본 기본값으로 실행됩니다.
실행 전에 예상해 봅니다.
첫째 노드는 끝나고, 둘째 노드는 기록을 적은 뒤 멈출 것입니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.624445Z', 'iopub.status.busy': '2026-09-25T12:36:32.624391Z', 'iopub.status.idle': '2026-09-25T12:36:32.640779Z', 'shell.execute_reply': '2026-09-25T12:36:32.640482Z'}}

```python
# 대출 신청을 입력으로 넣어 실행하고, 둘째 노드가 낸 실패 흉내를 받아 출력합니다(저장 시점은 기본값)
loan_request = {"loan_key": loan_key, "notes": []}
try:
    one_graph.invoke(loan_request, config)
except TimeoutError as error:
    print("오류 종류:", type(error).__name__)
    print("오류 메시지:", error)
print("부른 횟수:", call_count)
```

출력:
```
오류 종류: TimeoutError
오류 메시지: 이 절에서 만든 실패 흉내입니다.
부른 횟수: {'receive_request': 1, 'record_loan': 1}

```

### [24] markdown {}

**결과 읽기** — 출력 줄 `오류 종류: TimeoutError`와 `오류 메시지: 이 절에서 만든 실패 흉내입니다.`가 받은 오류입니다.
출력 줄 `부른 횟수: {'receive_request': 1, 'record_loan': 1}`로, 두 노드가 한 번씩 불렸습니다.
오류는 셀이 받아 출력해, 노트북은 멈추지 않았습니다.

다음 셀은 04절 함수 `read_saved`로 파일에 남은 체크포인트를 읽고, `read_record`로 기록 파일을 읽습니다.
실행 전에 예상해 봅니다.
다음 노드는 `record_loan`이고, 기록 파일에는 키가 이미 한 줄 있을 것입니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.641292Z', 'iopub.status.busy': '2026-09-25T12:36:32.641240Z', 'iopub.status.idle': '2026-09-25T12:36:32.643684Z', 'shell.execute_reply': '2026-09-25T12:36:32.643496Z'}}

```python
# 멈춘 뒤 파일에 남은 체크포인트와, 대출 기록 파일에 적힌 키를 읽습니다(04절 함수 둘 — 도구 파일)
one_saved = read_saved(builder, one_prefix + ".sqlite", member_id)
print("남은 칸 값:", one_saved["칸 값"])
print("다음 노드:", one_saved["다음 노드"])
print("체크포인트 수:", one_saved["체크포인트 수"])
one_before = read_record(one_prefix + ".record")
print("멈추기 전에 적힌 키:", one_before)
```

출력:
```
남은 칸 값: {'loan_key': 'loan-2307', 'notes': ['신청 받음']}
다음 노드: ('record_loan',)
체크포인트 수: 3
멈추기 전에 적힌 키: ['loan-2307']

```

### [26] markdown {}

**결과 읽기** — 출력 줄 `다음 노드: ('record_loan',)`와 `체크포인트 수: 3`입니다.
출력 줄 `남은 칸 값: {'loan_key': 'loan-2307', 'notes': ['신청 받음']}`에는 첫째 노드가 낸 글만 있습니다.
출력 줄 `멈추기 전에 적힌 키: ['loan-2307']`로, 기록 파일에는 이미 한 줄이 있습니다.
체크포인트에는 기록을 마친 흔적이 없는데, 바깥 파일에는 기록이 남았습니다.

06절에서 강제 종료로 본 어긋남이, 실패 흉내로 멈출 때도 생겼습니다.
체크포인트 수 3은 06절에서 둘째 노드 안에서 끊긴 뒤의 수와 같습니다.

다음 셀은 03절처럼 첫 연결을 닫고, 같은 파일에 새 연결·새 체크포인터·새 그래프를 만듭니다.
창구 프로그램을 닫았다가 다시 연 것과 같습니다.
새 그래프가 파일에서 읽은 다음 노드와 칸 `notes`도 출력합니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.644243Z', 'iopub.status.busy': '2026-09-25T12:36:32.644195Z', 'iopub.status.idle': '2026-09-25T12:36:32.648088Z', 'shell.execute_reply': '2026-09-25T12:36:32.647839Z'}}

```python
# 첫 연결을 닫고, 같은 파일에 새 연결·새 체크포인터·새 그래프를 만들어 스레드를 읽습니다(03절 모양)
one_conn.close()
one_conn_again = sqlite3.connect(one_prefix + ".sqlite", check_same_thread=False)
one_saver_again = SqliteSaver(one_conn_again)
one_graph_again = builder.compile(checkpointer=one_saver_again)
reopened = one_graph_again.get_state(config)
print("새 그래프가 읽은 다음 노드:", reopened.next)
print("새 그래프가 읽은 칸 notes:", reopened.values["notes"])
```

출력:
```
새 그래프가 읽은 다음 노드: ('record_loan',)
새 그래프가 읽은 칸 notes: ['신청 받음']

```

### [28] markdown {}

**결과 읽기** — 출력 줄 `새 그래프가 읽은 다음 노드: ('record_loan',)`입니다.
첫 연결과 첫 그래프는 더 쓰지 않지만, 새 그래프가 파일에서 멈춘 자리를 읽었습니다.
출력 줄 `새 그래프가 읽은 칸 notes: ['신청 받음']`도 앞 셀과 같습니다.

다음 셀은 실패 원인을 없애고, 05절처럼 새 입력 없이(`None`) 같은 스레드를 이어 갑니다.
이어 가는 그래프는 방금 만든 새 그래프입니다.
실행 전에 예상해 봅니다.
첫째 노드는 다시 불리지 않고, 둘째 노드 `record_loan`은 처음부터 다시 실행될 것입니다.
다시 실행된 `record_loan`은 기록 파일에서 키를 찾아, 쓰지 않고 건너뛸 것입니다.

### [29] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.648580Z', 'iopub.status.busy': '2026-09-25T12:36:32.648537Z', 'iopub.status.idle': '2026-09-25T12:36:32.653247Z', 'shell.execute_reply': '2026-09-25T12:36:32.652982Z'}}

```python
# 실패 흉내를 끄고, 새 그래프로 새 입력 없이(None) 같은 스레드를 이어 갑니다(05절처럼)
failure_plan["fail"] = False
one_result = one_graph_again.invoke(None, config)
print("칸 notes:", one_result["notes"])
print("부른 횟수:", call_count)
```

출력:
```
칸 notes: ['신청 받음', '건너뜀']
부른 횟수: {'receive_request': 1, 'record_loan': 2}

```

### [30] markdown {}

**결과 읽기** — 출력 줄 `부른 횟수: {'receive_request': 1, 'record_loan': 2}`입니다.
이어 가는 동안 `record_loan`만 한 번 더 불렸고, 첫째 노드는 다시 불리지 않았습니다.
출력 줄 `칸 notes: ['신청 받음', '건너뜀']`의 `건너뜀`은 다시 실행된 `record_loan`이 낸 글입니다.
멈춘 첫 실행이 낼 글 `적음`은 칸에 없습니다.
노드가 끝나지 못해, 그 노드가 칸에 낼 갱신이 저장되지 않았기 때문입니다.

다음 셀은 이어 간 뒤의 체크포인트와 대출 기록 파일을 봅니다.
실행 전에 예상해 봅니다.
기록 파일에는 키가 한 줄만 있을 것입니다.

### [31] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.653804Z', 'iopub.status.busy': '2026-09-25T12:36:32.653759Z', 'iopub.status.idle': '2026-09-25T12:36:32.656726Z', 'shell.execute_reply': '2026-09-25T12:36:32.656397Z'}}

```python
# 이어 간 뒤 남은 체크포인트와, 대출 기록 파일에 같은 키가 적힌 줄 수를 봅니다
one_after = read_saved(builder, one_prefix + ".sqlite", member_id)
print("다음 노드:", one_after["다음 노드"])
print("체크포인트 수:", one_after["체크포인트 수"])
one_keys = read_record(one_prefix + ".record")
one_count = one_keys.count(loan_key)
print("대출 기록 파일의 키:", one_keys)
print("같은 키가 적힌 줄 수:", one_count)
# 우리 코드가 정하는 값이라 실행마다 같아야 합니다
assert one_count == 1, "쓰기 방식 idempotent는 같은 키를 한 줄만 남겨야 합니다"
```

출력:
```
다음 노드: ()
체크포인트 수: 4
대출 기록 파일의 키: ['loan-2307']
같은 키가 적힌 줄 수: 1

```

### [32] markdown {}

**결과 읽기** — 출력 줄 `다음 노드: ()`와 `체크포인트 수: 4`로, 이 스레드의 처리가 끝났습니다.
출력 줄 `같은 키가 적힌 줄 수: 1`입니다.
노드 `record_loan`은 두 번 실행되었지만, 대출 기록에는 한 번 실행한 것과 같은 한 줄만 남았습니다.

이 실행에서 세 절의 기능이 모두 쓰였습니다.
멈춘 자리는 03절처럼 SQLite 파일에 남아, 새 연결로 연 그래프도 읽었습니다.
05절처럼 원인을 없앤 뒤 `None`으로 이어 갔습니다.
다시 실행된 노드의 되풀이는 06절 멱등 키 확인이 막았습니다.

## 6. 실행 2 · 쓰기 방식만 바꾸기

실행 2에서는 쓰기 방식 하나만 `naive`로 바꿉니다.
06절에서는 자식 프로세스를 강제로 끝내, 노드를 다시 실행하게 했습니다.
이번에는 같은 커널 안의 실패 흉내로 멈춘 뒤 새 연결로 이어 갈 때도, 같은 차이가 나는지 봅니다.
다음 셀은 쓰기 방식을 바꾸고, 부른 횟수와 실패 흉내를 처음 값으로 다시 맞춥니다.
파일 앞머리는 실행 1처럼 쓰기 방식 이름을 따라 새로 고릅니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.657186Z', 'iopub.status.busy': '2026-09-25T12:36:32.657143Z', 'iopub.status.idle': '2026-09-25T12:36:32.658827Z', 'shell.execute_reply': '2026-09-25T12:36:32.658562Z'}}

```python
# 실행 2 · 바꿀 값: 쓰기 방식 하나만 naive로 바꾸고, 부른 횟수와 실패 흉내는 처음 값으로 다시 맞춥니다
write_plan["mode"] = "naive"
# 파일 앞머리는 실행 1처럼 쓰기 방식 이름을 따라 새로 고릅니다
write_plan["prefix"] = new_prefix(write_plan["mode"])
call_count["receive_request"] = 0
call_count["record_loan"] = 0
failure_plan["fail"] = True
print("쓰기 방식:", write_plan)
print("부른 횟수:", call_count)
print("실패 흉내:", failure_plan)
```

출력:
```
쓰기 방식: {'mode': 'naive', 'prefix': 'naive-1'}
부른 횟수: {'receive_request': 0, 'record_loan': 0}
실패 흉내: {'fail': True}

```

### [34] markdown {}

**결과 읽기** — 출력 줄 `쓰기 방식: {'mode': 'naive', 'prefix': 'naive-1'}`가 실행 2의 설정입니다.
출력 줄 `부른 횟수: {'receive_request': 0, 'record_loan': 0}`과 `실패 흉내: {'fail': True}`는 실행 1을 시작할 때와 같습니다.

다음 셀은 새 앞머리 `naive-1`의 SQLite 파일에 연결을 열어 컴파일하고, 같은 대출 신청으로 실행합니다.
스레드 이름은 실행 1과 같은 `M-0317`이지만, 파일이 달라 실행 1의 체크포인트와 섞이지 않습니다.
03절 8절에서 파일 이름만 바꾸면, 스레드 이름이 같아도 빈 딕셔너리를 읽은 것과 같습니다.
실행 전에 예상해 봅니다.
실행 1처럼 둘째 노드가 기록을 적은 뒤 멈출 것입니다.

### [35] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.659362Z', 'iopub.status.busy': '2026-09-25T12:36:32.659317Z', 'iopub.status.idle': '2026-09-25T12:36:32.671915Z', 'shell.execute_reply': '2026-09-25T12:36:32.671548Z'}}

```python
# 실행 2의 SQLite 파일에 연결을 열어 컴파일하고, 같은 대출 신청으로 실행해 실패 흉내를 받아 출력합니다
two_prefix = write_plan["prefix"]
two_conn = sqlite3.connect(two_prefix + ".sqlite", check_same_thread=False)
two_saver = SqliteSaver(two_conn)
two_graph = builder.compile(checkpointer=two_saver)
try:
    two_graph.invoke(loan_request, config)
except TimeoutError as error:
    print("오류 종류:", type(error).__name__)
print("부른 횟수:", call_count)
```

출력:
```
오류 종류: TimeoutError
부른 횟수: {'receive_request': 1, 'record_loan': 1}

```

### [36] markdown {}

**결과 읽기** — 출력 줄 `오류 종류: TimeoutError`와 `부른 횟수: {'receive_request': 1, 'record_loan': 1}`은 실행 1과 같습니다.

다음 셀은 멈춘 뒤 파일에 남은 체크포인트와 대출 기록 파일을 읽습니다.

### [37] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.672462Z', 'iopub.status.busy': '2026-09-25T12:36:32.672414Z', 'iopub.status.idle': '2026-09-25T12:36:32.674874Z', 'shell.execute_reply': '2026-09-25T12:36:32.674573Z'}}

```python
# 멈춘 뒤 실행 2의 SQLite 파일에 남은 체크포인트와, 대출 기록 파일에 적힌 키를 읽습니다
two_saved = read_saved(builder, two_prefix + ".sqlite", member_id)
print("다음 노드:", two_saved["다음 노드"])
print("체크포인트 수:", two_saved["체크포인트 수"])
two_before = read_record(two_prefix + ".record")
print("멈추기 전에 적힌 키:", two_before)
```

출력:
```
다음 노드: ('record_loan',)
체크포인트 수: 3
멈추기 전에 적힌 키: ['loan-2307']

```

### [38] markdown {}

**결과 읽기** — 출력 줄 `다음 노드: ('record_loan',)`와 `체크포인트 수: 3`은 실행 1과 같습니다.
출력 줄 `멈추기 전에 적힌 키: ['loan-2307']`도 같습니다.
체크포인트 수 3으로, 이 파일의 스레드는 빈 상태에서 시작했습니다.

다음 셀은 실행 1처럼 연결을 닫고 새 연결·새 그래프를 만든 뒤, 실패 흉내를 끄고 이어 갑니다.
실행 전에 예상해 봅니다.
다시 실행된 `record_loan`이 검사 없이 같은 키를 한 줄 더 적을 것입니다.

### [39] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.675410Z', 'iopub.status.busy': '2026-09-25T12:36:32.675363Z', 'iopub.status.idle': '2026-09-25T12:36:32.682007Z', 'shell.execute_reply': '2026-09-25T12:36:32.681679Z'}}

```python
# 연결을 닫고 새 연결·새 그래프를 만든 뒤, 실패 흉내를 끄고 새 입력 없이(None) 이어 갑니다
two_conn.close()
two_conn_again = sqlite3.connect(two_prefix + ".sqlite", check_same_thread=False)
two_saver_again = SqliteSaver(two_conn_again)
two_graph_again = builder.compile(checkpointer=two_saver_again)
failure_plan["fail"] = False
two_result = two_graph_again.invoke(None, config)
print("칸 notes:", two_result["notes"])
print("부른 횟수:", call_count)
```

출력:
```
칸 notes: ['신청 받음', '적음']
부른 횟수: {'receive_request': 1, 'record_loan': 2}

```

### [40] markdown {}

**결과 읽기** — 출력 줄 `부른 횟수: {'receive_request': 1, 'record_loan': 2}`는 실행 1과 같습니다.
출력 줄 `칸 notes: ['신청 받음', '적음']`의 `적음`은 다시 실행된 `record_loan`이 한 줄을 더 적었다는 뜻입니다.

다음 셀은 이어 간 뒤의 체크포인트와 대출 기록 파일을 봅니다.

### [41] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.682488Z', 'iopub.status.busy': '2026-09-25T12:36:32.682445Z', 'iopub.status.idle': '2026-09-25T12:36:32.685012Z', 'shell.execute_reply': '2026-09-25T12:36:32.684736Z'}}

```python
# 이어 간 뒤 남은 체크포인트와, 대출 기록 파일에 같은 키가 적힌 줄 수를 봅니다
two_after = read_saved(builder, two_prefix + ".sqlite", member_id)
print("다음 노드:", two_after["다음 노드"])
print("체크포인트 수:", two_after["체크포인트 수"])
two_keys = read_record(two_prefix + ".record")
two_count = two_keys.count(loan_key)
print("대출 기록 파일의 키:", two_keys)
print("같은 키가 적힌 줄 수:", two_count)
# 우리 코드가 정하는 값이라 실행마다 같아야 합니다
assert two_count == 2, "쓰기 방식 naive는 같은 키를 두 줄 남겨야 합니다"
```

출력:
```
다음 노드: ()
체크포인트 수: 4
대출 기록 파일의 키: ['loan-2307', 'loan-2307']
같은 키가 적힌 줄 수: 2

```

### [42] markdown {}

**결과 읽기** — 출력 줄 `같은 키가 적힌 줄 수: 2`입니다.
대출은 한 건인데, 대출 기록에 같은 키가 두 줄 남았습니다.
출력 줄 `다음 노드: ()`와 `체크포인트 수: 4`는 실행 1과 같습니다.
체크포인트로 보면 두 실행은 같은 자리에서 멈추고, 같은 자리에서 끝났습니다.
달라진 것은 바깥 파일의 줄 수입니다.

## 7. 두 실행 견주기

다음 셀은 두 실행의 파일을 앞머리마다 새 연결로 다시 읽어, 한 줄씩 견줍니다.

### [43] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.685480Z', 'iopub.status.busy': '2026-09-25T12:36:32.685434Z', 'iopub.status.idle': '2026-09-25T12:36:32.688790Z', 'shell.execute_reply': '2026-09-25T12:36:32.688493Z'}}

```python
# 두 실행이 파일에 남긴 것을 파일 앞머리마다 한 줄씩 견줍니다(파일을 새 연결로 다시 읽음)
print("파일 앞머리 | 칸 notes | 체크포인트 수 | 같은 키가 적힌 줄 수")
for name_prefix in [one_prefix, two_prefix]:
    saved = read_saved(builder, name_prefix + ".sqlite", member_id)
    keys = read_record(name_prefix + ".record")
    print(name_prefix, "|", saved["칸 값"]["notes"], "|", saved["체크포인트 수"], "|", keys.count(loan_key))
```

출력:
```
파일 앞머리 | 칸 notes | 체크포인트 수 | 같은 키가 적힌 줄 수
idempotent-1 | ['신청 받음', '건너뜀'] | 4 | 1
naive-1 | ['신청 받음', '적음'] | 4 | 2

```

### [44] markdown {}

**결과 읽기** — 라벨 줄 아래 두 줄은 `idempotent-1 | ['신청 받음', '건너뜀'] | 4 | 1`과 `naive-1 | ['신청 받음', '적음'] | 4 | 2`입니다.
두 실행에서 다른 것은 칸 `notes`의 마지막 글과, 기록 파일의 줄 수입니다.
체크포인트 수와, 이어 갈 때 부른 횟수는 같았습니다.

다음 셀은 남은 연결을 닫고, 작업 폴더의 파일을 봅니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-25T12:36:32.689293Z', 'iopub.status.busy': '2026-09-25T12:36:32.689249Z', 'iopub.status.idle': '2026-09-25T12:36:32.693019Z', 'shell.execute_reply': '2026-09-25T12:36:32.692732Z'}}

```python
# 남은 연결 둘을 닫고, 작업 폴더에 남은 파일을 이름 차례로 봅니다
one_conn_again.close()
two_conn_again.close()
file_names = sorted(os.listdir())
print("현재 작업 폴더의 파일:", file_names)
```

출력:
```
현재 작업 폴더의 파일: ['idempotent-1.record', 'idempotent-1.sqlite', 'naive-1.record', 'naive-1.sqlite']

```

### [46] markdown {}

**결과 읽기** — 출력 줄 `현재 작업 폴더의 파일: ['idempotent-1.record', 'idempotent-1.sqlite', 'naive-1.record', 'naive-1.sqlite']`입니다.
연결을 모두 닫아, SQLite 옆 파일(`-wal`·`-shm`)은 남지 않았습니다.
파일은 모두 임시 폴더에 있어, 실습 폴더에는 남지 않습니다.

## 정리

1. 대출 기록을 적은 노드가 실패 흉내로 멈추자, 체크포인트에는 그 노드의 갱신이 없고 기록 파일에는 한 줄이 남았습니다.
2. 새 연결로 연 그래프가 `None`으로 이어 가자, 첫째 노드는 두고 멈춘 노드만 처음부터 다시 실행했습니다.
3. 쓰기 방식 `idempotent`는 대출 기록을 한 줄, `naive`는 같은 키를 두 줄 남겼습니다.

이 절로 Ch 23이 끝납니다.
Ch 24 01절에서는 되돌리기 어려운 일을 하기 전에, 사람이 확인하는 자리에서 그래프를 멈추는 방법을 다룹니다.

## 그림

### 07-1-세-절-기능을-붙인-대출-처리-그래프.mmd

```mermaid
flowchart TB
  %% classes
  mode["쓰기 방식<br>write_plan<br>실행 1 idempotent<br>실행 2 naive"]:::tool
  p05["05절 실패 흉내<br>failure_plan<br>TimeoutError"]:::flow
  p06["06절<br>append_key_once<br>도구 파일"]:::flow
  rec["노드 record_loan<br>대출 키를 적은 뒤<br>알림에서 멈출 수 있음"]:::flow
  sav["03절<br>SqliteSaver<br>SQLite 파일"]
  req["대출 신청 한 건<br>스레드 M-0317<br>대출 키 loan-2307"]:::tool
  gra["SQLite 체크포인터를<br>붙인 그래프<br>노드 receive_request<br>노드 record_loan"]
  mode --> rec
  p05 --> rec
  p06 --> rec
  rec --> gra
  req -->|invoke| gra
  sav --> gra
  p06 ~~~ sav
  p06 ~~~ req
```

05절 실패 흉내와 06절 함수는 노드 record_loan 안에서 쓰고, 03절 SQLite 체크포인터는 그래프에 붙였습니다.

### 07-2-실행-1의-실제-차례.mmd

```mermaid
flowchart TB
  %% classes
  s1["invoke 대출 신청<br>스레드 M-0317<br>receive_request 마침"]:::flow
  s2["record_loan<br>대출 키를 적은 뒤<br>실패 흉내로 멈춤"]:::flow
  s3["받은 오류 TimeoutError<br>부른 횟수 두 노드 한 번씩"]:::measure
  s4["파일에 남은 것<br>다음 노드 record_loan<br>체크포인트 셋<br>기록 파일 키 한 줄"]:::measure
  s5["연결을 닫고<br>새 연결 · 새 그래프<br>실패 흉내를 끄고<br>invoke None"]:::flow
  s6["record_loan을<br>처음부터 다시 실행<br>키를 찾아 건너뜀"]:::flow
  s7["이어 간 뒤<br>receive_request 한 번<br>record_loan 두 번<br>칸 notes 신청 받음 · 건너뜀<br>체크포인트 넷<br>기록 파일 키 한 줄"]:::measure
  s1 --> s2
  s2 --> s3
  s3 --> s4
  s4 --> s5
  s5 --> s6
  s6 --> s7
```

실행 1에서 record_loan은 대출 키를 적은 뒤 멈췄고, 새 그래프로 이어 갈 때 처음부터 다시 실행되어 키를 건너뛰었습니다.

### 07-3-쓰기-방식만-바꾼-두-실행.mmd

```mermaid
flowchart TB
  %% classes
  top["바꾼 값 하나 · 쓰기 방식<br>실행 1 idempotent<br>실행 2 naive"]:::tool
  subgraph r1["실행 1 · idempotent"]
    direction TB
    a1["다시 실행한 record_loan<br>append_key_once가<br>키를 찾아 건너뜀"]:::flow
    a2["기록 파일에 같은 키 한 줄<br>칸 notes 신청 받음 · 건너뜀"]:::measure
    a1 --> a2
  end
  subgraph r2["실행 2 · naive"]
    direction TB
    b1["다시 실행한 record_loan<br>append_key가<br>검사 없이 한 줄 더"]:::flow
    b2["기록 파일에 같은 키 두 줄<br>칸 notes 신청 받음 · 적음"]:::measure
    b1 --> b2
  end
  cm["두 실행 같음<br>멈춘 뒤 다음 노드 record_loan<br>체크포인트 셋<br>이어 간 뒤 체크포인트 넷<br>receive_request 한 번<br>record_loan 두 번"]
  top --> r1
  top --> r2
  r1 ~~~ cm
  r2 ~~~ cm
```

쓰기 방식만 바꾸자 기록 파일의 같은 키 줄 수가 한 줄에서 두 줄로 바뀌었고, 멈춘 자리와 부른 횟수는 같았습니다.

### 07-4-리본으로-이은-사진과-기보.prompt.md

# 07-4-리본으로-이은-사진과-기보 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락, 마감 2026-09-25에 지금 본문 글로 맞춤): 01절부터 한 수를 둘 때마다 즉석사진을 찍어 판의 모습을 남겼습니다. 06절에서는 판 옆에 기보를 두고, 둔 수를 한 줄씩 적었습니다. 이번에는 판 앞에 사진 한 장과 기보 한 장을 나란히 두고, 리본 하나로 판과 이어 둡니다. 수를 두다가 말 하나가 쓰러지면, 사진을 보고 그 수를 다시 둡니다. 기보에 그 수가 이미 적혀 있으면 다시 적지 않습니다.

구성 요소와 배치: 나무 탁자 **하나**(조금 위에서 봄) · 가운데 체스판 **하나**(말은 서 있고, **흰 나이트 하나만** 판 위에 옆으로 누움 — 멈춘 노드 `record_loan`) · 판 앞에 크게 놓인 물건 **둘**을 **빨간 리본 하나**로 묶음(세 절 기능을 한 흐름에 모음): 왼쪽 즉석사진 **한 장**(작은 체스판이 찍힘 — 파일에 남은 체크포인트), 오른쪽 흰 종이 **한 장**에 검은 나이트 실루엣 **하나**(기보 — 대출 키 한 줄). 01~06이 쓴 장면(탁자 둘·사진 여러 장 줄·사진첩·빈 나무 상자·쓰러진 판·카메라·종이 두 장의 표시 둘/하나)은 되풀이하지 않고, 새 소품 **리본**(과정 grep 0건)으로 「묶어 조립함」을 보임. 사람·손·화살표·화면·시계·글자·숫자·연필·앞 챕터 소품(쟁반·서랍·바구니·저울·울타리·발자국·공구판·승강 상자·식당 전표·집게·세탁기·선반·도장·카드·봉투) 없음.

시선 순서: 가운데 판과 누운 나이트 → 판 앞 리본으로 묶은 사진과 기보.

검수 기준: 그림만 보고 「판 하나에 사진 한 장과 기록 한 장이 함께 묶여 있고, 판 위 말 하나가 쓰러져 있다」가 읽히는가. 누운 말이 정확히 하나인가, 사진이 정확히 한 장인가, 종이의 표시가 정확히 하나인가, 두 물건이 리본 하나로 묶였는가. 글자·숫자·사람·손·카메라가 없는가.

비유 계열: 챕터 리드 결정 11 **「체스판과 즉석사진」**(01절이 엶) — 07은 01~06의 사진(체크포인트)·기보(바깥 기록)를 판 하나에 묶음.

## 프롬프트 (1차, 채택)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. One wooden table seen from slightly above. In the middle of the table lies one chessboard; all chess pieces stand upright on it except exactly one white knight, which lies on its side on the board. In front of the chessboard lie exactly two large flat items side by side, tied together with one red ribbon: on the left, one instant photo whose picture shows a small chessboard; on the right, one blank sheet of white paper with exactly one small black knight silhouette drawn in ink. The paper has no lines and no writing. No camera, no second chessboard, no second photo, no pencil, no people, no hands, no arrows, no screens, no clocks, no trays, no drawers, no baskets, no shelves, no envelopes, no clips, no photo albums, no boxes, no stamps, no cards.
```

## 상태

- 2026-09-25 · `nano_banana_pro`(`jobs_wait` 응답 모델 이름 `nano_banana_2` — 01-5~06-5와 같은 표시) · 16:9 · 2k · `use_unlim: false` · count 1. 생성 전 잔액 **2433.75**(바로 앞 거래 10:57:21Z는 06절 몫).
- **1차 job `a6c8200a-a747-4590-824a-e3c904038749` 채택** — 거래 **2026-09-25T11:32:55Z 「Nano Banana Pro −2」**(결과 파일 이름 `hf_20260925_113255_a6c8200a…`와 시각이 같음). 이 절 몫은 거래 한 줄, **2크레딧**. 재생성 0회. 결과 원본 `95379c0b95fcbe6ce733eed1fa06c84730fc97b8aaaecf11e34fb4d83a5fb202`(2752 × 1536).
- **그림에서 확인한 것(그림 읽기·alt에 반영)**: 흰 바탕 위 나무 탁자 하나(조금 위에서 봄, 다리 넷 가운데 넷이 보임). 탁자 위쪽 체스판 하나, 말들은 대부분 서 있고 **판 가운데 흰 나이트 하나만 옆으로 누움**(확대해 확인 — 서 있는 흰 나이트 둘·앞으로 나온 검은 나이트 하나는 짝짓지 않음). 판 앞 왼쪽 **즉석사진 한 장**(흰 테두리, 사진 속 작은 체스판), 오른쪽 **흰 종이 한 장에 검은 나이트 실루엣 하나**(줄·글자 없음). **빨간 리본 하나**가 판 앞 가장자리에서 두 물건 사이를 지나 탁자 앞 끝까지 세로로 이어지고 탁자 앞면으로 늘어짐, 두 물건 사이에 나비매듭(고리 둘이 사진 오른쪽 모서리·종이 왼쪽 가장자리에 닿음). 글자·숫자·사람·손·화살표·화면·시계·카메라·연필·사진첩·상자 없음.
- **검수 판정**: 「누운 말 하나 · 사진 한 장 · 종이의 표시 하나」는 그대로 보임. 리본은 **두 물건을 감싸 묶지 않고, 판에서 두 물건 사이로 이어진 모양**이라 검수 기준의 「리본 하나로 묶였는가」는 글자 그대로는 아님 → 재생성하지 않고, 본문 비유·alt·캡션·그림 읽기를 **보이는 대로 「리본 하나로 판과 이어 둠」**으로 고쳐 채택(파일 이름도 `…묶은…` → `…이은…`, `mv -n`). 판단 근거: 관계(판 하나에 딸린 사진 한 장과 기록 한 장, 쓰러진 말 하나)는 그림만 보고 읽히고, 재생성에서 개수가 틀릴 위험(01·02 선례)이 더 큼.
- 저장: 기기 셸에서 결과 URL을 `curl`로 받아(`/tmp/ch23-07/illu-1-orig.png`) `UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pillow`로 RGB·폭 1100px(LANCZOS)로 줄여 `figures/07-4-리본으로-이은-사진과-기보.png`(1100 × 614, `68179ede219b521ffffdcb9f5c52db84617434e3ca94ce0190d785a20624d32e`)로 저장했습니다.
- 결과 URL을 한 번 더 받아(`illu-1-again.png`, 원본과 해시 같음) 같은 폭으로 줄인 그림과 저장 PNG를 픽셀 대조했습니다(`ImageChops.difference` bbox `None`, 최대 차이 0). 저장 PNG의 사본(`.cache/ch23-07-view/illu-saved.png`, 해시 같음)과 원본 확대 두 장(`illu-crop-front.png`·`illu-crop-knight.png`)을 직접 열어 개수를 세고 그림 읽기를 썼습니다.

