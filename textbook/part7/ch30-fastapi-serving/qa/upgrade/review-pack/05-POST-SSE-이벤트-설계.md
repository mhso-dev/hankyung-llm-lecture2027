# 05-POST-SSE-이벤트-설계

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 1.25h | 실습 2.75h | 코드 notebooks/05-POST-SSE-이벤트-설계.ipynb | 새 용어 4 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>처리 함수 <code>chat_stream</code>이 <code>yield</code>로 내놓는 <code>ServerSentEvent</code>의 칸 <code>event</code>·<code>id</code>·<code>data</code>를 읽을 수 있습니다.</li>
<li>SSE 응답 본문을 빈 줄로 나누고, 칸 <code>data</code>의 JSON 글을 파이썬 값으로 읽을 수 있습니다.</li>
<li>인자 <code>response_class</code> 하나를 뺀 실험으로, SSE와 JSON 줄 형식의 차이를 출력으로 확인할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href="04-astream과-응답-스트림.html">04절</a>의 진행 값은 같은 프로그램 안의 파이썬 값이었습니다. 웹 화면이 받으려면 그 값을 HTTP 응답의 글로 적어 보내야 합니다. 받는 쪽은 그 글에서 이어 붙일 값과 끝을 알리는 값을 가를 수 있어야 합니다. 그래서 사건마다 이름과 번호를 붙여 보냅니다.</p><p>제목의 SSE는 Server-Sent Events의 줄임말입니다. 서버가 한 응답 안에서 사건을 차례로 글로 적어 보내는 형식입니다. 제목의 POST는 <a href="01-비동기-라우팅과-스키마.html">01절</a>에서 본 요청 방식이고, 질문을 요청 본문에 담아 보냅니다. 제목의 이벤트는 이 절에서 SSE 사건이라고 부릅니다. 제목의 설계는 사건 이름과 번호, 자료를 어느 칸에 둘지 정하는 일입니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href="04-astream과-응답-스트림.html">04절</a>에서는 비동기 메서드 <code>astream</code>을 부르기만 해서 비동기 제너레이터를 받았습니다. 반복 <code>async for</code>로 모드 <code>custom</code>의 진행 값 여섯을 받았고, 진행 값은 칸 <code>token</code> 하나인 딕셔너리였습니다. 그 절의 6절은 앱 파일 110·111행이 같은 모드로 <code>astream</code>을 부르는 줄을 보였습니다.</p><p><a href="../../part6/ch25-streaming/01-일곱-가지-stream-mode.html">Ch 25 01절</a>에서는 메서드가 하나씩 내놓는 값을 스트림 사건, 노드가 쓰기 함수로 보낸 값을 진행 값이라고 불렀습니다. <a href="../../part6/ch25-streaming/02-토큰과-중간-진행-스트리밍.html">Ch 25 02절</a>은 한 실행에서 모드 셋을 함께 받았습니다. 사건 짝의 모드 이름으로 진행 값과 스트림 청크를 가르고, 모드 차례를 읽었습니다. 이 절의 SSE 사건은 모드 이름 대신 칸 <code>event</code>에 사건 이름을 적어 가릅니다.</p><p><a href="01-비동기-라우팅과-스키마.html">01절</a>에서는 시험용 클라이언트로 요청을 보내고, 응답 형식과 응답 머리를 봤습니다. <a href="02-의존성으로-Agent-주입.html">02절</a>에서는 의존성과 제공 함수를 배우고, 제공 함수를 직접 불러 값을 봤습니다. 그 절에서 <code>asyncio.wait_for</code>로 시간 제한을 거는 줄도 읽었습니다.</p><p><a href="../../part2/ch06-langchain-start/04-스트리밍과-content-blocks.html">Ch 6 04절</a>에서는 메서드 <code>stream()</code>이 제너레이터를 내놓았습니다. <a href="../../part1/ch02-python/12-async와-await.html">Ch 2 12절</a>에서는 비동기 함수와 await를 배웠습니다. 함수 <code>json.loads</code>는 Ch 15 02절에서 모델이 쓴 JSON 글을 읽을 때 썼습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>화물역으로 짐칸 일곱 량이 이어진 화물 열차가 들어옵니다. 짐칸 여섯의 옆면에는 같은 색 이름판과 작은 번호판이 하나씩 붙어 있습니다. 맨 끝 칸에는 색이 다른 이름판만 있고, 번호판은 없습니다. 역에서는 이름판을 보고 짐을 내릴 칸과, 열차가 다 왔다는 칸을 가릅니다.</p><p>짐칸 하나가 SSE 사건 하나이고, 이름판이 칸 <code>event</code>의 사건 이름입니다. 번호판이 칸 <code>id</code>의 사건 번호이고, 칸에 실린 짐이 칸 <code>data</code>의 자료입니다. 이름판만 단 끝 칸은 사건 번호가 없는 <code>done</code> 사건입니다.</p><p>비유와 다른 점이 있습니다. 실제 SSE 사건은 칸 이름과 값을 글로 적은 줄이고, 사건 사이는 빈 줄로 나뉩니다. 또 이 절의 시험용 클라이언트는 열차가 다 들어온 뒤에 칸을 한꺼번에 받습니다. 그래서 칸이 들어온 때가 아니라, 칸이 이어진 차례만 봅니다.</p>
{{img:05-5-이름판과-번호판을-단-화물-칸|흰 바탕에 자갈 바닥 위 선로 하나가 오른쪽 아래에서 왼쪽 위로 비스듬히 놓여 있습니다. 선로 위에 닫힌 짐칸 일곱이 한 줄로 이어져 있고, 칸 사이는 연결 고리로 조금씩 떨어져 있습니다. 오른쪽 아래부터 하늘색 짐칸 여섯에는 옆면마다 짙은 초록 네모 판 하나와 작은 흰 동그라미 판 하나가 붙어 있습니다. 맨 왼쪽 위 끝의 연한 주황 짐칸에는 짙은 갈색 네모 판 하나만 있고, 흰 동그라미 판은 없습니다. 기관차·사람·글자·숫자·화살표는 없는 그림|같은 이름판과 번호판을 단 하늘색 칸 여섯 뒤에, 이름판만 다른 주황 칸 하나가 끝에 붙어 있습니다.}}
<p class="look"><b>그림 읽기</b> — 오른쪽 아래부터 하늘색 짐칸 여섯이 한 줄로 이어지고, 왼쪽 위 끝에 연한 주황 짐칸 하나가 붙어 있습니다. 하늘색 칸마다 옆면에 짙은 초록 네모 판과 작은 흰 동그라미 판이 하나씩 있습니다. 주황 칸에는 짙은 갈색 네모 판 하나만 있고, 흰 동그라미 판이 없습니다. 칸 하나가 SSE 사건 하나이고, 네모 판이 사건 이름, 흰 동그라미 판이 사건 번호입니다. 그림의 번호판은 모두 같은 흰 동그라미이지만, 실제 사건 번호는 <code>sse-1:0</code>부터 칸마다 하나씩 커집니다.</p>
<h3>SSE와 SSE 사건</h3><p>SSE 응답은 한 응답의 본문에 사건을 차례로 적은 글입니다. 사건 하나는 여러 줄이고, 줄마다 칸 이름과 값을 쌍점과 공백으로 잇습니다. 사건과 사건 사이는 빈 줄 하나로 나뉩니다. 웹 표준 문서인 WHATWG의 HTML 표준은 받는 쪽이 빈 줄을 만나면 그때까지 읽은 사건을 내보낸다고 적습니다.</p><p>04절의 스트림 사건은 메서드 <code>astream</code>이 내놓는 파이썬 값입니다. SSE 사건은 응답 본문에 적힌 글입니다. 처리 함수 <code>chat_stream</code>은 스트림 사건 하나를 SSE 사건 하나로 바꿔 보냅니다. 끝에는 사건 이름이 <code>done</code>인 사건을 하나 더 보냅니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>SSE(Server-Sent Events)</td><td>서버가 한 응답 안에서 사건을 하나씩 글로 적어 보내는 형식입니다. 화물역에 열차 한 편이 칸을 차례로 달고 들어오는 일과 같습니다. 이 절에서는 본문 종류가 <code>text/event-stream</code>인 응답이 SSE입니다.</td></tr><tr><td>SSE 사건</td><td>SSE 응답에서 빈 줄로 끝나는 줄 묶음 하나입니다. 줄마다 칸 이름과 값을 쌍점과 공백으로 이어 적습니다. 화물 열차의 칸 하나에 이름판과 번호판, 짐이 함께 있는 것과 같습니다. 이 절에서는 칸 <code>event</code>(사건 이름)·<code>data</code>(자료)·<code>id</code>(사건 번호)로 된 사건이 일곱 나왔습니다.</td></tr><tr><td>비동기 제너레이터 함수(async generator function)</td><td>정의 줄이 <code>async def</code>이고 몸통에 <code>yield</code>가 있는 함수입니다. 부르면 몸통을 실행하지 않고 비동기 제너레이터를 내놓고, 값을 하나 꺼낼 때마다 다음 <code>yield</code>까지 실행됩니다. 빵을 한 판 구울 때마다 진열대에 내놓고, 다음 판은 멈춘 자리에서 이어 굽는 일과 같습니다. 이 절에서는 처리 함수 <code>chat_stream</code>과 노트북의 <code>stream_answer</code>가 그렇습니다.</td></tr><tr><td>JSON 줄 형식(JSON Lines)</td><td>한 줄에 JSON 글 하나를 적고, 줄바꿈 뒤에 다음 값을 적는 형식입니다. 출석부에 한 줄에 한 사람씩 적는 일과 같습니다. 이 절에서는 실행 2의 본문 종류 <code>application/jsonl</code>이 이 형식입니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 처리 함수 <code>chat_stream</code>을 부르기만 하자 받은 값의 종류가 <code>async_generator</code>였습니다. 응답 본문을 빈 줄로 나누자 SSE 사건이 일곱 나왔습니다. 인자 <code>response_class</code>를 빼자 본문 종류가 <code>application/jsonl</code>이 되었습니다.</p>
{{mermaid:05-1-진행-값에서-SSE-사건까지|위에서 아래로 읽는 흐름도입니다. 초록 상자 요청 본문 질문 반납 기한을 알려 주세요와 thread_id sse-1에서 초록 상자 처리 함수 chat_stream이 astream 모드 custom을 부름으로 이어집니다. 노란 상자 진행 값 여섯 칸 token 하나씩을 지나, 초록 상자 진행 값마다 yield로 사건 이름 token과 사건 번호 sse-1:0에서 sse-1:5, 초록 상자 끝에 yield로 사건 이름 done 하나 사건 번호 없음으로 갑니다. 이어서 회색 상자 라이브러리가 사건마다 줄 event data id로 적음을 지나 노란 상자 응답 본문 SSE 사건 일곱 text/event-stream에 닿는 그림|처리 함수 chat_stream은 진행 값 여섯마다 사건 이름 token을, 끝에 done을 yield로 내놓았고, 라이브러리가 이를 SSE 사건 일곱의 글로 적었습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 초록 상자는 우리가 보낸 요청 본문과 실습 앱 파일의 줄이고, 회색 상자는 라이브러리가 하는 일입니다. 노란 상자 둘은 노트북 2절과 3절의 출력입니다.</p>
<h3>yield로 내놓는 처리 함수</h3><p>처리 함수 <code>chat_stream</code>의 정의 줄은 <code>async def</code>이고, 몸통에 <code>yield</code>가 셋 있습니다. Python 언어 참조는 <code>async def</code> 안에 <code>yield</code>가 있으면 비동기 제너레이터 함수라고 적습니다. 이 함수를 부르면 몸통을 실행하지 않고 비동기 제너레이터를 내놓습니다. 값을 하나 꺼낼 때마다 몸통이 다음 <code>yield</code> 줄까지 실행되어, 그 값을 내놓고 멈춥니다.</p><p>데코레이터 줄에 <code>response_class=EventSourceResponse</code>를 적으면, 라이브러리가 내놓은 값을 SSE 사건의 글로 적어 보냅니다. 양식 클래스 <code>ServerSentEvent</code>를 내놓으면 그 칸 <code>event</code>·<code>data</code>·<code>id</code>가 줄 머리가 됩니다. 칸 <code>data</code>의 값은 늘 JSON 글로 적힙니다. 설치판 fastapi <code>routing.py</code> 507행이 <code>json.dumps</code>를 기본 설정으로 써서, 한글이 <code>\uc9c8</code> 같은 유니코드 번호로 나갑니다.</p><p>109행 <code>async with asyncio.timeout(timeout):</code>은 들여 쓴 줄 전체에 시간 제한을 겁니다. Python 문서는 정한 초를 넘기면 그 일을 취소하고, 오류 <code>TimeoutError</code>로 바꾼다고 적습니다. <a href="02-의존성으로-Agent-주입.html">02절</a>의 <code>asyncio.wait_for</code>와 같은 일을 여러 줄을 감싸는 모양으로 합니다. 이 절에서는 시간 제한을 넘기는 장면을 실행하지 않았고, <a href="06-fetch-재연결과-오류-이벤트.html">06절</a>에서 봅니다.</p>
{{mermaid:05-2-SSE-사건-하나의-칸|위에서 아래로 읽는 흐름도입니다. 노란 상자 응답 본문 글 text/event-stream에서 파란 상자 split_sse 빈 줄로 나눠 SSE 사건 일곱으로 갑니다. 노란 상자 첫 SSE 사건 글 event: token, data: JSON 글, id: sse-1:0을 지나 파란 상자 parse_sse 처음 쌍점과 공백에서 한 번만 나눔, 노란 상자 칸 이름 셋 event data id로 이어집니다. 마지막으로 파란 상자 json.loads로 칸 data를 읽음과 노란 상자 읽은 값 dict 처리 함수가 내놓은 값과 같음 True에 닿는 그림|응답 본문 글을 빈 줄로 나누면 SSE 사건 일곱이 되고, 사건 하나를 줄마다 나누면 칸 event·data·id가 되며, 칸 data의 JSON 글은 json.loads로 읽었습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 파란 상자 셋은 노트북 3절에서 우리가 쓴 함수와 줄이고, 노란 상자 넷은 그 셀들의 출력입니다. 칸 data의 글은 JSON 글이라, 한 번 더 읽어야 파이썬 값이 됩니다.</p>
<h3>요청 방식 POST와 받는 쪽</h3><p>FastAPI 문서는 SSE가 GET만이 아니라 어느 요청 방식에서나 된다고 적습니다. 이 앱은 질문과 스레드 이름(칸 <code>thread_id</code>)을 요청 본문에 담아야 해서 POST로 받습니다. 웹 문서 MDN이 적은 브라우저의 <code>EventSource</code> 생성자는 주소와 선택 칸 <code>withCredentials</code>만 받습니다. 요청 본문과 요청 머리를 적을 자리가 없어, 이 앱의 응답은 <a href="06-fetch-재연결과-오류-이벤트.html">06절</a>에서 함수 <code>fetch</code>로 읽습니다. 이 절은 브라우저에서 실행하지 않았습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 앱 파일 95~124행을 출력해 처리 함수 <code>chat_stream</code>의 줄을 읽습니다. 그 처리 함수를 HTTP 없이 바로 부르고, <code>async for</code>로 <code>ServerSentEvent</code> 일곱을 꺼냅니다. 3절은 시험용 클라이언트로 같은 질문을 POST로 보내고, 본문 글을 SSE 사건으로 나눕니다. 사건마다 칸을 딕셔너리로 바꾸고, 칸 <code>data</code>를 <code>json.loads</code>로 읽습니다.</p><p>4절은 인자 <code>response_class</code> 하나만 바꾼 두 실행으로 실험합니다. 모델 요청은 0번이고, API 키 없이 실행합니다. 서버 프로그램을 띄우지 않아 네트워크와 포트, 자식 프로세스를 쓰지 않습니다. 실습 폴더의 파일을 가져오고 읽기만 하며, 걸린 시간은 재지 않았습니다.</p>
{{notebook:05-POST-SSE-이벤트-설계}}
<p class="look"><b>확인할 점</b> — 노트북 2절에서 <code>부르기만 해서 받은 값의 종류: async_generator</code>와 <code>내놓은 값 수: 7</code>을 찾습니다. 3절에서는 <code>본문 종류: text/event-stream; charset=utf-8</code>과 <code>SSE 사건 수: 7</code>을 봅니다. 줄 <code>7 | done | 없음</code>과 <code>처리 함수가 내놓은 값과 같은가: True</code>도 확인합니다.</p>
{{mermaid:05-3-처리-함수가-내놓은-값과-응답-글|맨 위에 초록 상자 처리 함수 chat_stream 질문 반납 기한을 알려 주세요가 있고, 그 아래 갈래 둘이 나란히 놓여 있습니다. 왼쪽 갈래는 파란 상자 바로 부름 async for로 꺼냄에서 노란 상자 ServerSentEvent 일곱 token 여섯 done 하나로 갑니다. 오른쪽 갈래는 파란 상자 시험용 클라이언트로 POST 본문을 끝까지 모아 받음에서 노란 상자 본문 글 SSE 사건 일곱 칸 data는 JSON 글로 갑니다. 두 갈래는 노란 상자 token 사건의 data가 처리 함수 값과 같음 True로 모이는 그림|처리 함수를 바로 불러 꺼낸 값과, HTTP 응답 글을 나눠 읽은 값이 같았습니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 초록 상자는 실습 앱 파일의 처리 함수입니다. 왼쪽 갈래는 노트북 2절, 오른쪽 갈래는 3절에서 우리가 쓴 줄과 그 출력입니다. 맨 아래 노란 상자는 두 갈래의 값을 견준 3절 출력입니다. 오른쪽 파란 상자의 「본문을 끝까지 모아 받음」은 설치판 starlette 소스로 본 동작입니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>가설은 FastAPI 문서에서 세웠습니다. SSE 쪽 문서는 <code>yield</code>와 <code>response_class=EventSourceResponse</code>를 함께 적으라고 합니다. JSON Lines 쪽 문서는 <code>response_class</code> 없이 <code>yield</code>만 쓰면 JSON 줄 형식으로 보낸다고 적습니다. 두 실행에서 처리 함수와 질문은 같았고, 바꾼 것은 인자 <code>response_class</code> 하나였습니다.</p>
{{mermaid:05-4-response-class-유무와-응답-모양|맨 위에 파란 상자 같은 처리 함수 stream_answer 같은 질문 yield 일곱 번이 있고, 그 아래 칸 둘이 나란히 놓여 있습니다. 왼쪽 칸 실행 1 response_class 있음에는 파란 상자 response_class=EventSourceResponse, 노란 상자 본문 종류 text/event-stream, 노란 상자 SSE 사건 일곱 event: 줄 일곱이 위에서 아래로 있습니다. 오른쪽 칸 실행 2 response_class 없음에는 파란 상자 response_class 빼기만 함, 노란 상자 본문 종류 application/jsonl, 노란 상자 JSON 줄 일곱 event: 줄 없음이 위에서 아래로 있는 그림|같은 처리 함수가 같은 값 일곱을 내놓아도, 인자 response_class를 빼자 본문이 SSE 사건이 아니라 JSON 줄 일곱이 되었습니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 파란 상자는 두 실행이 함께 쓴 처리 함수입니다. 왼쪽 칸이 실행 1, 오른쪽 칸이 실행 2이고, 칸마다 맨 위 파란 상자가 바꾼 값입니다. 노란 상자는 4절 출력이고, 실험 절이라 빨강은 쓰지 않았습니다.</p>
<table><thead><tr><th>견준 것</th><th>실행 1(인자 있음)</th><th>실행 2(인자 뺌)</th></tr></thead><tbody><tr><td>바꾼 값 <code>response_class</code></td><td><code>EventSourceResponse</code></td><td>없음</td></tr><tr><td>상태 코드</td><td><code>200</code></td><td><code>200</code></td></tr><tr><td>본문 종류</td><td><code>text/event-stream; charset=utf-8</code></td><td><code>application/jsonl</code></td></tr><tr><td>덩어리 수</td><td>SSE 사건 <code>7</code></td><td>JSON 줄 <code>7</code></td></tr><tr><td><code>event:</code>로 시작하는 줄 수</td><td><code>7</code></td><td><code>0</code></td></tr><tr><td>응답 머리 수</td><td><code>3</code></td><td><code>1</code></td></tr><tr><td>응답 문서의 본문 종류</td><td><code>['text/event-stream']</code></td><td><code>['application/jsonl']</code></td></tr></tbody></table>
<p>실행 1의 본문은 3절에서 앱의 <code>chat_stream</code>이 보낸 글과 같았습니다. 작은 판에서 뺀 시간 제한과 이어 받기, 오류 처리 줄은 이 질문의 응답 글을 바꾸지 않았습니다. 실행 2는 상태 코드가 같은 200이었지만, 본문 종류가 <code>application/jsonl</code>이었습니다. 줄 <code>event:</code>는 하나도 없고, SSE 응답 머리 둘도 붙지 않았습니다.</p><p>실행 2의 줄 하나는 <code>ServerSentEvent</code>의 칸 여섯을 키로 가진 JSON 글이었습니다. FastAPI 문서대로, 내놓는 값 힌트가 없어 라이브러리가 객체를 JSON 글로 바꾼 것입니다. 덩어리 수는 두 실행 모두 일곱으로, 처리 함수가 <code>yield</code>로 내놓은 수와 같았습니다. 응답 문서에 적힌 본문 종류도 인자 하나로 달라졌습니다.</p><p>그래서 사건 이름으로 사건을 가르는 받는 쪽에 보내려면, 데코레이터 줄에 이 인자를 적어야 합니다. 앱의 <code>chat_stream</code>이 이 인자를 적은 까닭입니다. 다만 이 결과는 설치판 fastapi 0.135.0에서 본 것이고, 다른 판에서는 실행하지 않았습니다.</p>
<p>새 커널로 두 번 실행해 견주자, 코드 셀의 출력이 셀마다 모두 같았습니다. 한 번은 프로젝트 맨 위에서, 한 번은 <code>notebooks/</code> 폴더에서 연 커널이었습니다. 노트북 밖에서도 같은 장면을 파이썬 파일로 다섯 번 실행해, 출력이 모두 같았습니다. 모델을 부르지 않아, 사건의 차례와 개수는 노드 코드와 처리 함수가 정합니다.</p>
<p class="look"><b>확인할 점</b> — 4절 실행 1의 출력 <code>3절 앱 응답 본문과 같은가: True</code>를 찾습니다. 실행 2의 출력 <code>본문 종류: application/jsonl</code>과 <code>event: 로 시작하는 줄 수: 0</code>을 확인합니다. 결과 표의 줄 <code>덩어리 수 | 7 | 7</code>도 봅니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>시험용 클라이언트는 앱이 응답을 다 보낸 뒤 본문을 한꺼번에 줍니다. 설치판 starlette <code>testclient.py</code> 296·341·365행이 본문을 한 곳에 모은 뒤 응답을 만듭니다. 그래서 이 절 결과로는 사건마다 도착한 때를 말할 수 없습니다. 도착한 차례를 보려면 서버 프로그램을 따로 띄워야 하고, 이 절에서는 하지 않았습니다.</li><li>함수 <code>parse_sse</code>는 FastAPI가 적는 모양만 다룹니다. 줄 끝은 <code>\n</code>이고, 칸 이름 뒤에 쌍점과 공백이 하나 있는 모양입니다. WHATWG 표준은 쌍점으로 시작하는 줄을 버리고, 쌍점 뒤 공백이 없는 줄도 읽습니다. 이 함수는 그런 줄을 따로 다루지 않고, 쌍점과 공백이 없는 줄을 만나면 오류로 멈춥니다. 이 절에서는 그런 줄을 넣어 보지 않았습니다.</li><li>FastAPI 문서와 설치판 <code>sse.py</code> 218·222행은 사건 없이 15초가 지나면 쉼 신호 줄 <code>: ping</code>을 보낸다고 적습니다. 이 절의 응답은 바로 끝나 그 줄이 없었고, 이 절에서는 실행하지 않았습니다. 함수 <code>parse_sse</code>는 이 줄을 거르지 않습니다.</li><li>칸 <code>data</code>는 늘 JSON 글입니다. FastAPI 문서는 글 값도 따옴표를 붙여 적는다고 적고, 이 절에서는 글 값을 보내 보지 않았습니다. 화면에 붙이기 전에 <code>json.loads</code>로 읽어야 한글이 원래 글로 돌아옵니다.</li><li>사건 번호 <code>sse-1:0</code>에는 스레드 이름이 들어 있습니다. 이 스레드는 Ch 23 01절의 대화 하나이고, 01·03절에서 말한 실행 흐름의 스레드(Ch 2 12절)와 다른 뜻입니다. 끊긴 뒤 이어 받을 때 이 번호를 요청 머리 <code>Last-Event-ID</code>로 보내며, <a href="06-fetch-재연결과-오류-이벤트.html">06절</a>에서 봅니다. 이 절에서는 그 요청 머리를 보내지 않았습니다.</li><li>앱 객체의 메서드 <code>add_api_route</code>는 설치판 fastapi <code>applications.py</code> 1162행에 있습니다. 이 메서드는 1192행에서 앱 객체 안의 <code>self.router</code>가 가진 같은 이름 메서드(<code>routing.py</code> 1292행)를 부릅니다. 데코레이터 줄도 <code>routing.py</code> 1375·1406행에서 그 메서드를 부릅니다. 실습 앱은 데코레이터 줄을 쓰고, 이 절 실험만 같은 함수를 두 번 잇으려고 이 메서드를 썼습니다.</li><li>응답 문서(OpenAPI)는 <a href="08-OpenAPI와-TS-SDK.html">08절</a>에서 자세히 봅니다. 모델이 쓴 글을 SSE로 보내는 처리 함수는 <a href="09-실제-Agent-HTTP-통합.html">09절</a>에서 씁니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>처리 함수 <code>chat_stream</code>은 비동기 제너레이터 함수로, 진행 값마다 사건 이름 <code>token</code>을 붙여 <code>yield</code>로 내놓았습니다.</li><li>응답 본문은 빈 줄로 끝나는 SSE 사건 일곱이었고, 칸 <code>data</code>를 읽은 값은 처리 함수가 내놓은 값과 같았습니다.</li><li>인자 <code>response_class</code>를 빼자 같은 값 일곱이 JSON 줄 형식으로 나갔고, 줄 <code>event:</code>는 0개였습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href="06-fetch-재연결과-오류-이벤트.html">06절</a>에서는 끊긴 뒤 사건 번호로 이어 받는 방법과, 오류 사건 <code>error</code>를 봅니다. 브라우저 쪽 함수 <code>fetch</code>가 SSE 사건을 읽는 모양도 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 5개 · 해설 포함</summary><p class="quiz-q">1. SSE 응답 본문에서 사건 하나와 다음 사건은 무엇으로 나뉘나요?</p><p class="quiz-a">빈 줄 하나로 나뉩니다. 그래서 본문 글을 줄바꿈 두 개로 나누면 사건 글이 됩니다. 이 절에서는 나눈 글 여덟 가운데 끝의 빈 글을 빼고 사건 일곱을 얻었습니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">2. 처리 함수 <code>chat_stream</code>을 부르기만 하면 무엇을 받고, 몸통은 언제 실행되나요?</p><p class="quiz-a">비동기 제너레이터를 받고, 그 줄에서는 몸통이 실행되지 않습니다. 값을 하나 꺼낼 때마다 몸통이 다음 <code>yield</code>까지 실행됩니다. 틀렸다면 노트북 2절을 다시 읽습니다.</p><p class="quiz-q">3. 동료가 「칸 <code>data</code>의 글을 그대로 화면에 붙이면 된다」고 말합니다. 맞나요?</p><p class="quiz-a">맞지 않습니다. 칸 <code>data</code>는 JSON 글이고, 한글이 유니코드 번호로 적혀 있습니다. 함수 <code>json.loads</code>로 읽어야 <code>{'token': '질문을 '}</code> 같은 값이 됩니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">4. 사건 이름이 <code>done</code>인 사건에는 왜 칸 <code>id</code>가 없나요?</p><p class="quiz-a">앱 파일 118행이 <code>done</code> 사건을 만들 때 칸 <code>id</code>를 적지 않기 때문입니다. 사건 번호는 <code>token</code> 사건에만 붙고, 06절에서 이어 받을 자리로 씁니다. 틀렸다면 노트북 2절과 3절을 다시 읽습니다.</p><p class="quiz-q">5. 인자 <code>response_class</code>를 빼면 본문 종류와 줄 <code>event:</code>의 수는 어떻게 되나요?</p><p class="quiz-a">본문 종류가 <code>application/jsonl</code>이 되고, 줄 <code>event:</code>는 하나도 없습니다. 같은 값 일곱이 한 줄에 JSON 글 하나씩 나갑니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://fastapi.tiangolo.com/tutorial/server-sent-events/">FastAPI Server-Sent Events (SSE)</a></div>확인 2026-09-29 · <code>yield</code>와 <code>response_class=EventSourceResponse</code>로 SSE를 보낸다고 적습니다. 0.135.0에서 들어왔고, 어느 요청 방식에서나 된다고 적습니다. 칸 <code>data</code>는 늘 JSON으로 적고, 쉼 신호는 15초마다라고 적습니다.</li><li><div><a href="https://fastapi.tiangolo.com/tutorial/stream-json-lines/">FastAPI Stream JSON Lines</a></div>확인 2026-09-29 · <code>response_class</code> 없이 <code>yield</code>만 쓰면 <code>application/jsonl</code>로 보낸다고 적습니다. 내놓는 값 힌트가 없으면 <code>jsonable_encoder</code>로 바꾼다고 적고, 0.134.0에서 들어왔습니다.</li><li><div><a href="https://html.spec.whatwg.org/multipage/server-sent-events.html">HTML Standard Server-sent events</a></div>확인 2026-09-29 · 빈 줄을 만나면 사건을 내보내고, 첫 쌍점 앞을 칸 이름으로 읽는다고 적습니다. 칸은 <code>event</code>·<code>data</code>·<code>id</code>·<code>retry</code>만 읽고, 쌍점으로 시작하는 줄은 버린다고 적습니다.</li><li><div><a href="https://developer.mozilla.org/en-US/docs/Web/API/EventSource/EventSource">MDN EventSource() constructor</a></div>확인 2026-09-29 · 생성자가 주소와 선택 칸 <code>withCredentials</code>만 받는다고 적습니다.</li><li><div><a href="https://docs.python.org/3.12/library/asyncio-task.html#asyncio.timeout">Python asyncio.timeout</a></div>확인 2026-09-29 · 정한 초를 넘기면 작업을 취소하고 <code>TimeoutError</code>로 바꾼다고 적습니다. 3.11에서 들어왔습니다.</li><li><div><a href="https://docs.python.org/3.12/reference/expressions.html#asynchronous-generator-functions">Python Asynchronous generator functions</a></div>확인 2026-09-29 · <code>async def</code> 안에 <code>yield</code>가 있으면 비동기 제너레이터 함수라고 적습니다. 부르면 비동기 제너레이터 객체를 내놓는다고 적습니다.</li><li>설치판 fastapi 0.135.0 소스 <code>sse.py</code> 20행이 <code>EventSourceResponse</code>, 42행이 <code>ServerSentEvent</code>(칸 여섯)입니다. 같은 파일 146~214행은 줄을 <code>event</code>·<code>data</code>·<code>id</code>·<code>retry</code> 차례로 적고 빈 줄로 끝냅니다. 218·222행은 쉼 신호 줄과 15초입니다.</li><li>설치판 fastapi <code>routing.py</code> 491~522행이 내놓은 값을 SSE 사건의 글로 바꾸고, 507행이 <code>json.dumps</code>를 씁니다. 572·574행은 응답 머리 둘을 붙이고, 576~608행은 JSON 줄 형식입니다. 926~931행은 <code>response_class</code>로 둘을 가르고, <code>openapi/utils.py</code> 361~395행이 응답 문서를 적습니다.</li><li>설치판 fastapi <code>applications.py</code> 1162행이 <code>add_api_route</code>이고, 1192행이 <code>routing.py</code> 1292행의 같은 이름 메서드를 부릅니다. 같은 파일 1375·1406행의 데코레이터도 그 메서드를 부릅니다. 설치판 starlette 1.6.0 <code>testclient.py</code> 296·341·365행은 본문을 모은 뒤 응답을 만듭니다.</li><li>실습 폴더 <code>agent_service/app.py</code> 95~124행이 함수 <code>_event_id</code>와 처리 함수 <code>chat_stream</code>입니다.</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# POST SSE 이벤트 설계

**이 노트북에서 할 일**

1. 실습 앱의 처리 함수 `chat_stream`이 진행 값을 SSE 사건으로 내놓는 줄을 읽습니다.
2. 시험용 클라이언트로 받은 응답 글을 SSE 사건으로 나누고, 칸마다 읽습니다.
3. 인자 `response_class` 하나만 빼면 같은 처리 함수의 응답이 어떻게 바뀌는지 실험합니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
예상 비용도 0달러입니다.
실습 앱의 에이전트 그래프는 모델을 쓰지 않고, 정해 둔 말로 답합니다.
그래서 다시 실행해도 같은 값이 나와야 합니다.

요청은 시험용 클라이언트로 같은 노트북 안에서 보냅니다.
서버 프로그램을 띄우지 않고, 네트워크와 포트를 쓰지 않습니다.
실습 폴더의 파일을 가져오고 읽기만 하며, 쓰는 파일은 없습니다.

걸린 시간은 재지 않았습니다.
이 절은 응답 글에 적힌 사건의 차례와 칸만 봅니다.
앞 챕터에서 배운 함수는 이 절에서 쓰지 않아, 도구 파일도 가져오지 않습니다.

**기준 버전** — 첫 셀에서 패키지 여섯을 설치합니다.
판은 fastapi 0.135.0, httpx 0.28.1, pydantic 2.12.5, starlette 1.6.0입니다.
패키지 langgraph 1.2.11과 langchain 1.4.0은 실습 앱 파일이 가져오는 패키지입니다.
여섯 모두 실습 폴더 잠금과 같은 판입니다.

교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~3절을 읽고, 4절 실험의 가설을 함께 세웁니다.
4절의 두 실행은 실습 시간에 실행합니다.

실습 폴더 `labs/part7/ch30-fastapi-serving`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 읽는 흐름도입니다. 초록 상자 요청 본문 질문 반납 기한을 알려 주세요와 thread_id sse-1에서 초록 상자 처리 함수 chat_stream이 astream 모드 custom을 부름으로 이어집니다. 노란 상자 진행 값 여섯 칸 token 하나씩을 지나, 초록 상자 진행 값마다 yield로 사건 이름 token과 사건 번호 sse-1:0에서 sse-1:5, 초록 상자 끝에 yield로 사건 이름 done 하나 사건 번호 없음으로 갑니다. 이어서 회색 상자 라이브러리가 사건마다 줄 event data id로 적음을 지나 노란 상자 응답 본문 SSE 사건 일곱 text/event-stream에 닿는 그림](attachment:05-1-진행-값에서-SSE-사건까지.png)

위에서 아래로 읽습니다.
초록 상자는 우리가 보낸 요청 본문과 실습 앱 파일의 줄이고, 회색 상자는 라이브러리가 하는 일입니다.
노란 상자 둘은 노트북 2절과 3절의 출력입니다.

### [2] markdown {}

## 1. 준비

04절에서는 비동기 메서드 `astream`으로 노드의 진행 값을 같은 프로그램 안에서 받았습니다.
이 절은 그 진행 값을 웹 응답에 실어 보내는 처리 함수를 봅니다.
제목의 SSE는 Server-Sent Events의 줄임말입니다.
서버가 한 응답 안에서 사건을 차례로 글로 적어 보내는 형식입니다.
제목의 POST는 01절에서 본 요청 방식이고, 제목의 이벤트는 이 절에서 SSE 사건이라고 부릅니다.

첫 셀은 패키지 여섯을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:38.081371Z', 'iopub.status.busy': '2026-09-29T08:53:38.081212Z', 'iopub.status.idle': '2026-09-29T08:53:38.731905Z', 'shell.execute_reply': '2026-09-29T08:53:38.731361Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "fastapi==0.135.0" "httpx==0.28.1" "pydantic==2.12.5" "starlette==1.6.0" "langgraph==1.2.11" "langchain==1.4.0"
from importlib.metadata import version

print("fastapi:", version("fastapi"))
print("httpx:", version("httpx"))
print("pydantic:", version("pydantic"))
print("starlette:", version("starlette"))
print("langgraph:", version("langgraph"))
print("langchain:", version("langchain"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
fastapi: 0.135.0
httpx: 0.28.1
pydantic: 2.12.5
starlette: 1.6.0
langgraph: 1.2.11
langchain: 1.4.0

```

### [4] markdown {}

**결과 읽기** — 출력 줄 `fastapi: 0.135.0`과 `langgraph: 1.2.11`이 보입니다.
여섯 모두 실습 폴더 잠금과 같은 판이고, 04절과 같은 목록입니다.
FastAPI 문서는 이 절에서 쓰는 SSE 기능이 0.135.0에서 들어왔다고 적습니다.
이 절은 모델 객체를 만들지 않아, API 키를 확인하는 셀도 없습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
모듈 `json`은 JSON 글을 파이썬 값으로 읽을 때 씁니다.
모듈 `fastapi.sse`에서는 SSE 응답에 쓰는 이름 둘을 가져옵니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:38.732986Z', 'iopub.status.busy': '2026-09-29T08:53:38.732896Z', 'iopub.status.idle': '2026-09-29T08:53:38.935748Z', 'shell.execute_reply': '2026-09-29T08:53:38.935323Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓸 이름을 가져옵니다(os·json은 Python에 들어 있는 모듈입니다)
import os
import json
from fastapi import FastAPI
from fastapi.sse import EventSourceResponse, ServerSentEvent
from fastapi.testclient import TestClient

print("가져온 이름:", "json, FastAPI, TestClient")
print("fastapi.sse에서 가져온 이름:", "EventSourceResponse, ServerSentEvent")
```

출력:
```
가져온 이름: json, FastAPI, TestClient
fastapi.sse에서 가져온 이름: EventSourceResponse, ServerSentEvent

```

### [6] markdown {}

**결과 읽기** — 출력 줄 `fastapi.sse에서 가져온 이름: EventSourceResponse, ServerSentEvent`가 보입니다.
클래스 `EventSourceResponse`는 SSE로 보내는 응답의 종류를 가리킵니다.
클래스 `ServerSentEvent`는 SSE 사건 하나의 칸을 담는 양식 클래스입니다.
두 이름은 2절에서 앱 파일의 줄로 먼저 보고, 4절에서 우리가 직접 씁니다.

다음 셀은 01절 2절과 같은 파일 위치 셀로, 후보 셋 가운데 실습 폴더를 고릅니다.

### [7] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:38.936420Z', 'iopub.status.busy': '2026-09-29T08:53:38.936368Z', 'iopub.status.idle': '2026-09-29T08:53:38.938703Z', 'shell.execute_reply': '2026-09-29T08:53:38.938321Z'}}

```python
# 노트북을 연 자리에서 본 실습 폴더의 위치를 후보 셋 가운데에서 고릅니다
candidates = ["..", ".", "labs/part7/ch30-fastapi-serving"]
lab_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/agent_service/schemas.py"):
        lab_path = candidate
        break
print("실습 폴더를 찾았는가:", lab_path is not None)
assert lab_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."
```

출력:
```
실습 폴더를 찾았는가: True

```

### [8] markdown {}

**결과 읽기** — 출력 줄 `실습 폴더를 찾았는가: True`가 보입니다.
고른 후보는 연 자리마다 달라서 출력하지 않습니다.

다음 셀은 04절처럼 작업 폴더를 실습 폴더로 옮긴 뒤 이름을 가져옵니다.
그래프 파일에서 에이전트 그래프 `agent`를, 앱 파일에서 앱 객체 `app`과 처리 함수 `chat_stream`을 가져옵니다.
입력 형식 파일에서는 요청 본문의 양식 클래스 `ChatRequest`를 가져옵니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:38.939279Z', 'iopub.status.busy': '2026-09-29T08:53:38.939233Z', 'iopub.status.idle': '2026-09-29T08:53:39.438124Z', 'shell.execute_reply': '2026-09-29T08:53:39.437747Z'}}

```python
# 작업 폴더를 실습 폴더로 옮기고, 그래프·앱 객체·처리 함수·양식 클래스를 가져옵니다
os.chdir(lab_path)
from agent_service.agent import agent
from agent_service.app import app, chat_stream
from agent_service.schemas import ChatRequest
print("가져온 앱 객체의 종류:", type(app).__name__)
print("가져온 처리 함수의 이름:", chat_stream.__name__)
```

출력:
```
가져온 앱 객체의 종류: FastAPI
가져온 처리 함수의 이름: chat_stream

```

### [10] markdown {}

**결과 읽기** — 출력 줄 `가져온 앱 객체의 종류: FastAPI`와 `가져온 처리 함수의 이름: chat_stream`이 보입니다.
양식 클래스 `ChatRequest`는 01절에서 읽은 입력 형식으로, 칸 `question`과 `thread_id`를 받습니다.

## 2. 처리 함수 chat_stream과 yield

04절 6절에서는 앱 파일 110·111행이 모드 `custom`으로 `astream`을 부르는 것을 봤습니다.
그 두 줄은 처리 함수 `chat_stream` 안에 있습니다.
다음 셀은 앱 파일을 글로 읽어, 사건 번호를 만드는 함수와 `chat_stream`의 줄을 줄 번호와 함께 출력합니다.

### [11] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.438805Z', 'iopub.status.busy': '2026-09-29T08:53:39.438747Z', 'iopub.status.idle': '2026-09-29T08:53:39.441675Z', 'shell.execute_reply': '2026-09-29T08:53:39.441315Z'}}

```python
# 앱 파일을 글로 읽어, 95~124행(함수 _event_id와 처리 함수 chat_stream)을 줄 번호와 함께 출력합니다
first_line = 95
last_line = 124
with open("agent_service/app.py", encoding="utf-8") as app_file:
    app_lines = app_file.read().splitlines()
print("줄 번호 | 줄")
for index in range(first_line - 1, last_line):
    print(index + 1, "|", app_lines[index])
```

출력:
```
줄 번호 | 줄
95 | def _event_id(thread_id: str, index: int) -> str:
96 |     return f"{thread_id}:{index}"
97 | 
98 | 
99 | @app.post("/v1/chat/stream", response_class=EventSourceResponse)
100 | async def chat_stream(
101 |     body: ChatRequest,
102 |     runtime: AgentDep,
103 |     _token: AuthDep,
104 |     timeout: TimeoutDep,
105 |     start: ResumeIndexDep,
106 | ) -> AsyncIterable[ServerSentEvent]:
107 |     index = 0
108 |     try:
109 |         async with asyncio.timeout(timeout):
110 |             async for chunk in runtime.astream(
111 |                 {"messages": [body.question]}, stream_mode="custom"
112 |             ):
113 |                 if index >= start:
114 |                     yield ServerSentEvent(
115 |                         data=chunk, event="token", id=_event_id(body.thread_id, index)
116 |                     )
117 |                 index += 1
118 |         yield ServerSentEvent(data={"thread_id": body.thread_id}, event="done")
119 |     except Exception:
120 |         logger.exception("Agent SSE stream failed", extra={"thread_id": body.thread_id})
121 |         yield ServerSentEvent(
122 |             data={"code": "stream_failed", "message": "Agent 스트림이 중단되었습니다"},
123 |             event="error",
124 |         )

```

### [12] markdown {}

**결과 읽기** — 라벨 줄 아래 99행은 `99 | @app.post("/v1/chat/stream", response_class=EventSourceResponse)`입니다.
데코레이터 줄의 인자 `response_class`가 이 처리 함수의 응답을 SSE로 보내게 합니다.
114~116행은 받은 진행 값마다 `ServerSentEvent`를 만들어 `yield`로 내놓습니다.
칸 `data`에 진행 값, 칸 `event`에 사건 이름 `token`, 칸 `id`에 사건 번호를 넣습니다.
118행은 반복이 끝난 뒤, 사건 이름이 `done`인 사건을 하나 더 내놓습니다.

사건 번호는 95~96행 함수 `_event_id`가 스레드 이름과 자리 번호를 `:`로 이어 만듭니다.
여기서 스레드는 칸 `thread_id`가 가리키는 대화 하나(Ch 23 01절)로, 01·03절에서 말한 실행 흐름의 스레드와 뜻이 다릅니다.
113행의 `start`는 이어 받을 자리이고, 117행은 자리 번호를 하나씩 키웁니다.
이어 받기와 119~124행의 오류 사건 `error`는 06절에서 봅니다.

109행 `async with asyncio.timeout(timeout):`은 들여 쓴 줄 전체에 시간 제한을 겁니다.
Python 문서는 정한 초를 넘기면 그 일을 취소하고, 오류 `TimeoutError`로 바꾼다고 적습니다.
02절에서 본 `asyncio.wait_for`와 같은 일을, 여러 줄을 감싸는 모양으로 합니다.
이 절에서는 시간 제한을 넘기는 장면을 실행하지 않았고, 06절에서 봅니다.

다음 셀은 처리 함수 `chat_stream`을 HTTP 없이 바로 불러, 받은 값의 종류를 봅니다.
02절에서 제공 함수를 직접 불렀듯, 의존성이 넘겨 줄 값을 우리가 인자로 적습니다.
시간 제한은 앱의 제공 함수 `get_timeout`이 내놓는 2.0초로, 이어 받을 자리는 처음인 0으로 둡니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.442266Z', 'iopub.status.busy': '2026-09-29T08:53:39.442216Z', 'iopub.status.idle': '2026-09-29T08:53:39.444346Z', 'shell.execute_reply': '2026-09-29T08:53:39.443958Z'}}

```python
# 처리 함수 chat_stream을 HTTP 없이 바로 불러, 받은 값의 종류를 봅니다
request_body = ChatRequest(question="반납 기한을 알려 주세요", thread_id="sse-1")
timeout_seconds = 2.0
# 의존성이 넘겨 줄 값(그래프·접근 토큰·시간 제한 초·이어 받을 자리)을 인자로 직접 적습니다
direct_stream = chat_stream(
    body=request_body, runtime=agent, _token="local-demo-token",
    timeout=timeout_seconds, start=0,
)
print("부르기만 해서 받은 값의 종류:", type(direct_stream).__name__)
```

출력:
```
부르기만 해서 받은 값의 종류: async_generator

```

### [14] markdown {}

**결과 읽기** — 출력 줄 `부르기만 해서 받은 값의 종류: async_generator`가 보입니다.
04절에서 `astream`을 부르기만 했을 때와 같은 종류입니다.
이 줄에서는 몸통이 아직 실행되지 않았고, 그래프도 부르지 않았습니다.

정의 줄이 `async def`이고 몸통에 `yield`가 있는 함수를 비동기 제너레이터 함수라고 합니다.
부르면 몸통을 바로 실행하지 않고, 04절에서 본 비동기 제너레이터를 내놓습니다.
값을 하나 꺼낼 때마다 몸통이 다음 `yield` 줄까지 실행되어, 그 줄의 값을 내놓고 멈춥니다.
빵을 한 판 구울 때마다 진열대에 내놓고, 다음 판은 멈춘 자리에서 이어 굽는 일과 같습니다.
B 트랙에서 Ch 2 09절을 배웠다면, 그 절의 `yield`를 `async def` 안에 쓴 모양입니다.

다음 셀은 04절처럼 `async for`로 값을 꺼내, 종류와 칸 셋을 한 줄씩 출력합니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.444941Z', 'iopub.status.busy': '2026-09-29T08:53:39.444891Z', 'iopub.status.idle': '2026-09-29T08:53:39.449212Z', 'shell.execute_reply': '2026-09-29T08:53:39.448954Z'}}

```python
# async for로 처리 함수가 yield로 내놓은 값을 꺼내, 종류와 칸 셋을 한 줄씩 출력합니다
yielded_items = []
print("종류 | event | id | data")
async for item in direct_stream:
    print(type(item).__name__, "|", item.event, "|", item.id, "|", item.data)
    yielded_items.append(item)
print("내놓은 값 수:", len(yielded_items))
```

출력:
```
종류 | event | id | data
ServerSentEvent | token | sse-1:0 | {'token': '질문을 '}
ServerSentEvent | token | sse-1:1 | {'token': '확인했습니다: '}
ServerSentEvent | token | sse-1:2 | {'token': '반납 '}
ServerSentEvent | token | sse-1:3 | {'token': '기한을 '}
ServerSentEvent | token | sse-1:4 | {'token': '알려 '}
ServerSentEvent | token | sse-1:5 | {'token': '주세요 '}
ServerSentEvent | done | None | {'thread_id': 'sse-1'}
내놓은 값 수: 7

```

### [16] markdown {}

**결과 읽기** — 라벨 줄 아래 첫 줄은 `ServerSentEvent | token | sse-1:0 | {'token': '질문을 '}`입니다.
여섯째 줄까지 사건 이름은 `token`이고, 사건 번호가 `sse-1:0`부터 `sse-1:5`까지 하나씩 커집니다.
마지막 줄은 `ServerSentEvent | done | None | {'thread_id': 'sse-1'}`로, 사건 번호가 없습니다.
출력 줄 `내놓은 값 수: 7`도 보입니다.

칸 `data`의 여섯 값은 04절에서 받은 진행 값과 같은 모양입니다.
115행 `data=chunk`가 받은 진행 값을 그대로 넣기 때문입니다.
여기까지는 파이썬 객체이고, 아직 웹 응답의 글이 아닙니다.

## 3. 응답 글을 SSE 사건으로 나누기

이제 같은 질문을 HTTP 요청으로 보냅니다.
01절의 시험용 클라이언트로 요청 방식 POST를 보내고, 요청 머리에는 02절의 교재용 접근 토큰을 담습니다.
다음 셀은 요청을 보내고 상태 코드와 응답 머리의 칸 `content-type`을 출력합니다.
이 칸은 본문이 어떤 모양의 글인지 알리는 칸이라, 출력 라벨을 「본문 종류」로 붙였습니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.449903Z', 'iopub.status.busy': '2026-09-29T08:53:39.449851Z', 'iopub.status.idle': '2026-09-29T08:53:39.462291Z', 'shell.execute_reply': '2026-09-29T08:53:39.461925Z'}}

```python
# 시험용 클라이언트로 요청 주소 /v1/chat/stream에 같은 질문을 POST로 보냅니다
client = TestClient(app)
auth_headers = {"Authorization": "Bearer local-demo-token"}
question_body = {"question": "반납 기한을 알려 주세요", "thread_id": "sse-1"}
response = client.post("/v1/chat/stream", json=question_body, headers=auth_headers)
print("상태 코드:", response.status_code)
print("본문 종류:", response.headers["content-type"])
```

출력:
```
상태 코드: 200
본문 종류: text/event-stream; charset=utf-8

```

### [18] markdown {}

**결과 읽기** — 출력 줄 `상태 코드: 200`과 `본문 종류: text/event-stream; charset=utf-8`이 보입니다.
본문 종류 `text/event-stream`이 SSE 응답이라는 표시이고, 뒤쪽은 글자를 UTF-8로 적었다는 뜻입니다.
처리 함수의 데코레이터 줄에 적은 `EventSourceResponse`가 이 본문 종류를 정합니다.

다음 셀은 응답 머리의 이름 목록과, 처리 함수에 적지 않은 칸 둘의 값을 출력합니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.462845Z', 'iopub.status.busy': '2026-09-29T08:53:39.462797Z', 'iopub.status.idle': '2026-09-29T08:53:39.464750Z', 'shell.execute_reply': '2026-09-29T08:53:39.464355Z'}}

```python
# 응답 머리의 이름 목록과, 처리 함수에 적지 않은 칸 둘의 값을 출력합니다
print("응답 머리 이름:", list(response.headers))
print("cache-control:", response.headers["cache-control"])
print("x-accel-buffering:", response.headers["x-accel-buffering"])
```

출력:
```
응답 머리 이름: ['content-type', 'cache-control', 'x-accel-buffering']
cache-control: no-cache
x-accel-buffering: no

```

### [20] markdown {}

**결과 읽기** — 출력 줄 `응답 머리 이름: ['content-type', 'cache-control', 'x-accel-buffering']`이 보입니다.
칸 `cache-control`의 값은 `no-cache`이고, 칸 `x-accel-buffering`의 값은 `no`입니다.
처리 함수에 적지 않은 두 칸은 설치판 fastapi `routing.py` 572·574행이 붙입니다.
FastAPI 문서는 앞 칸이 응답을 저장해 두고 다시 쓰는 일을 막는다고 적습니다.
뒤 칸은 Nginx 같은 중간 서버가 응답을 모아 두었다 보내지 않게 한다고 적습니다.

다음 셀은 응답 본문 글을 줄바꿈까지 그대로 출력합니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.465277Z', 'iopub.status.busy': '2026-09-29T08:53:39.465223Z', 'iopub.status.idle': '2026-09-29T08:53:39.466873Z', 'shell.execute_reply': '2026-09-29T08:53:39.466564Z'}}

```python
# 응답 본문 글을 줄바꿈까지 그대로 출력합니다
print("응답 본문 글:")
print(response.text)
```

출력:
```
응답 본문 글:
event: token
data: {"token": "\uc9c8\ubb38\uc744 "}
id: sse-1:0

event: token
data: {"token": "\ud655\uc778\ud588\uc2b5\ub2c8\ub2e4: "}
id: sse-1:1

event: token
data: {"token": "\ubc18\ub0a9 "}
id: sse-1:2

event: token
data: {"token": "\uae30\ud55c\uc744 "}
id: sse-1:3

event: token
data: {"token": "\uc54c\ub824 "}
id: sse-1:4

event: token
data: {"token": "\uc8fc\uc138\uc694 "}
id: sse-1:5

event: done
data: {"thread_id": "sse-1"}



```

### [22] markdown {}

**결과 읽기** — 라벨 줄 아래 첫 세 줄은 `event: token`, `data: {"token": "\uc9c8\ubb38\uc744 "}`, `id: sse-1:0`입니다.
줄마다 칸 이름, 쌍점과 공백, 값이 차례로 있습니다.
그 뒤 빈 줄 하나가 SSE 사건 하나의 끝입니다.
맨 끝 사건은 `event: done`과 `data: {"thread_id": "sse-1"}` 두 줄이고, 줄 `id:`가 없습니다.

칸 `data`의 한글은 「질」이 `\uc9c8`로 적히듯, 유니코드 번호로 적혀 나갑니다.
설치판 `routing.py` 507행이 `json.dumps`로 JSON 글을 만들 때, 기본 설정이 한글을 이렇게 적기 때문입니다.
사건의 차례는 2절에서 처리 함수가 내놓은 차례와 같습니다.

시험용 클라이언트는 앱이 응답을 다 보낸 뒤 본문을 한꺼번에 줍니다.
설치판 starlette `testclient.py` 296·341·365행이 본문을 한 곳에 모은 뒤 응답을 만듭니다.
그래서 이 글로는 사건마다 도착한 때를 말할 수 없고, 적힌 차례만 봅니다.

다음 셀은 본문 글을 빈 줄로 나눠, SSE 사건 글의 목록을 내놓는 함수를 정의합니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.467412Z', 'iopub.status.busy': '2026-09-29T08:53:39.467363Z', 'iopub.status.idle': '2026-09-29T08:53:39.469001Z', 'shell.execute_reply': '2026-09-29T08:53:39.468662Z'}}

```python
# 본문 글을 빈 줄로 나눠, 빈 글을 뺀 SSE 사건 글의 목록을 내놓습니다
def split_sse(body_text):
    found = []
    # SSE 사건 하나는 빈 줄로 끝나므로, 줄바꿈 두 개가 사건 사이의 경계입니다
    for part in body_text.split("\n\n"):
        if part != "":
            found.append(part)
    return found
```

출력:
```

```

### [24] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
글 `"\n\n"`은 줄바꿈 두 개로, 한 줄이 끝난 뒤 빈 줄이 하나 있다는 뜻입니다.
나눈 글 가운데 빈 글은 빼고, 사건 글만 모아 내놓습니다.

다음 셀은 본문 글을 빈 줄로만 나눈 수와, 함수 `split_sse`로 모은 사건 수를 견줍니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.469492Z', 'iopub.status.busy': '2026-09-29T08:53:39.469444Z', 'iopub.status.idle': '2026-09-29T08:53:39.471277Z', 'shell.execute_reply': '2026-09-29T08:53:39.470951Z'}}

```python
# 본문 글을 빈 줄로만 나눈 수와, 함수 split_sse로 모은 SSE 사건 수를 견줍니다
parts = response.text.split("\n\n")
print("빈 줄로 나눈 글 수:", len(parts))
print("마지막 글이 빈 글인가:", parts[-1] == "")
sse_texts = split_sse(response.text)
print("SSE 사건 수:", len(sse_texts))
```

출력:
```
빈 줄로 나눈 글 수: 8
마지막 글이 빈 글인가: True
SSE 사건 수: 7

```

### [26] markdown {}

**결과 읽기** — 출력 줄 `빈 줄로 나눈 글 수: 8`과 `마지막 글이 빈 글인가: True`가 보입니다.
본문 글이 빈 줄로 끝나서, 나눈 글의 맨 끝이 빈 글 하나입니다.
함수 `split_sse`가 빈 글을 빼자 출력 줄 `SSE 사건 수: 7`이 나왔습니다.
2절에서 처리 함수가 내놓은 값 수 일곱과 같습니다.

다음 셀은 SSE 사건 글 하나를 받아, 칸 이름을 키로 한 딕셔너리로 바꾸는 함수를 정의합니다.
줄마다 처음 나온 쌍점과 공백에서 한 번만 나눕니다.
칸 `data`의 JSON 글 안에도 쌍점과 공백이 있어, 여러 번 나누면 값이 쪼개지기 때문입니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.471759Z', 'iopub.status.busy': '2026-09-29T08:53:39.471716Z', 'iopub.status.idle': '2026-09-29T08:53:39.473475Z', 'shell.execute_reply': '2026-09-29T08:53:39.473169Z'}}

```python
# SSE 사건 글 하나를 받아, 줄마다 칸 이름과 값으로 나눈 딕셔너리를 내놓습니다
def parse_sse(sse_text):
    fields = {}
    for line in sse_text.split("\n"):
        # split의 둘째 인자 1은 처음 나온 자리에서 한 번만 나눈다는 뜻입니다
        name_and_value = line.split(": ", 1)
        fields[name_and_value[0]] = name_and_value[1]
    return fields
```

출력:
```

```

### [28] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
메서드 `split`에 둘째 인자 `1`을 주면, 처음 나온 자리에서 한 번만 나눈 목록을 내놓습니다.
목록의 첫째가 칸 이름이고, 둘째가 값입니다.

다음 셀은 일곱 사건 글을 모두 딕셔너리로 바꾸고, 첫 사건과 끝 사건을 출력합니다.

### [29] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.473967Z', 'iopub.status.busy': '2026-09-29T08:53:39.473924Z', 'iopub.status.idle': '2026-09-29T08:53:39.475688Z', 'shell.execute_reply': '2026-09-29T08:53:39.475310Z'}}

```python
# 일곱 SSE 사건 글을 모두 딕셔너리로 바꾸고, 첫 사건과 끝 사건을 출력합니다
sse_fields = []
for sse_text in sse_texts:
    sse_fields.append(parse_sse(sse_text))
print("첫 사건의 칸 이름:", list(sse_fields[0]))
print("첫 사건의 칸:", sse_fields[0])
print("끝 사건의 칸:", sse_fields[-1])
```

출력:
```
첫 사건의 칸 이름: ['event', 'data', 'id']
첫 사건의 칸: {'event': 'token', 'data': '{"token": "\\uc9c8\\ubb38\\uc744 "}', 'id': 'sse-1:0'}
끝 사건의 칸: {'event': 'done', 'data': '{"thread_id": "sse-1"}'}

```

### [30] markdown {}

**결과 읽기** — 출력 줄 `첫 사건의 칸 이름: ['event', 'data', 'id']`가 보입니다.
첫 사건의 칸 `id`는 `'id': 'sse-1:0'`이고, 칸 `data`의 값은 아직 JSON 글입니다.
끝 사건의 칸에는 `event`와 `data` 둘만 있고, 칸 `id`가 없습니다.
칸이 적힌 차례는 설치판 fastapi `sse.py` 199~207행이 정한 차례와 같습니다.

다음 셀은 일곱 사건의 자리와 사건 이름, 사건 번호를 한 줄씩 출력합니다.

### [31] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.476327Z', 'iopub.status.busy': '2026-09-29T08:53:39.476280Z', 'iopub.status.idle': '2026-09-29T08:53:39.478259Z', 'shell.execute_reply': '2026-09-29T08:53:39.477902Z'}}

```python
# 일곱 사건의 자리·사건 이름·사건 번호를 한 줄씩 출력합니다(번호가 없으면 없음)
print("자리 | event | id")
for index in range(len(sse_fields)):
    fields = sse_fields[index]
    event_id = "없음"
    if "id" in fields:
        event_id = fields["id"]
    print(index + 1, "|", fields["event"], "|", event_id)
```

출력:
```
자리 | event | id
1 | token | sse-1:0
2 | token | sse-1:1
3 | token | sse-1:2
4 | token | sse-1:3
5 | token | sse-1:4
6 | token | sse-1:5
7 | done | 없음

```

### [32] markdown {}

**결과 읽기** — 라벨 줄 아래 첫 줄은 `1 | token | sse-1:0`이고, 여섯째 줄은 `6 | token | sse-1:5`입니다.
마지막 줄은 `7 | done | 없음`입니다.
사건 이름은 여섯 번 `token`, 한 번 `done`이고, 사건 번호는 `token` 사건에만 있습니다.
사건 번호 끝의 수는 0부터 세어, 자리보다 하나 작습니다.

받는 쪽은 사건 이름으로 이어 붙일 사건과 끝을 알리는 사건을 가릅니다.
사건 번호는 06절에서 끊긴 뒤 이어 받을 자리를 알릴 때 씁니다.

다음 셀은 첫 사건의 칸 `data` 글을 `json.loads`로 읽어, 파이썬 값으로 바꿉니다.
함수 `json.loads`는 Ch 15 02절에서 모델이 쓴 JSON 글을 읽을 때 썼습니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.478753Z', 'iopub.status.busy': '2026-09-29T08:53:39.478713Z', 'iopub.status.idle': '2026-09-29T08:53:39.480603Z', 'shell.execute_reply': '2026-09-29T08:53:39.480244Z'}}

```python
# 첫 사건의 칸 data 글을 json.loads로 읽어, 파이썬 값으로 바꿉니다
first_data = sse_fields[0]["data"]
print("칸 data의 글:", first_data)
first_value = json.loads(first_data)
print("json.loads로 읽은 값:", first_value)
print("읽은 값의 종류:", type(first_value).__name__)
```

출력:
```
칸 data의 글: {"token": "\uc9c8\ubb38\uc744 "}
json.loads로 읽은 값: {'token': '질문을 '}
읽은 값의 종류: dict

```

### [34] markdown {}

**결과 읽기** — 출력 줄 `칸 data의 글: {"token": "\uc9c8\ubb38\uc744 "}`가 보입니다.
함수 `json.loads`로 읽자 출력 줄 `json.loads로 읽은 값: {'token': '질문을 '}`이 나왔습니다.
읽은 값의 종류는 `dict`이고, 유니코드 번호로 적혔던 한글이 원래 글로 돌아왔습니다.

다음 셀은 `token` 사건의 칸 `data`를 모두 읽어 모으고, 2절에서 처리 함수가 내놓은 값과 견줍니다.

### [35] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.481169Z', 'iopub.status.busy': '2026-09-29T08:53:39.481127Z', 'iopub.status.idle': '2026-09-29T08:53:39.482926Z', 'shell.execute_reply': '2026-09-29T08:53:39.482619Z'}}

```python
# token 사건의 칸 data를 모두 읽어 모으고, 처리 함수가 내놓은 칸 data와 견줍니다
token_values = []
for fields in sse_fields:
    if fields["event"] == "token":
        token_values.append(json.loads(fields["data"]))
direct_values = []
for item in yielded_items:
    if item.event == "token":
        direct_values.append(item.data)
print("token 사건에서 읽은 값 수:", len(token_values))
print("처리 함수가 내놓은 값과 같은가:", token_values == direct_values)
```

출력:
```
token 사건에서 읽은 값 수: 6
처리 함수가 내놓은 값과 같은가: True

```

### [36] markdown {}

**결과 읽기** — 출력 줄 `token 사건에서 읽은 값 수: 6`과 `처리 함수가 내놓은 값과 같은가: True`가 보입니다.
응답 글을 나누고 칸 `data`를 읽은 값이, 2절에서 처리 함수가 내놓은 값과 같았습니다.
라이브러리가 글로 적고 우리가 다시 읽는 사이에, 값은 바뀌지 않았습니다.

## 4. 실험: response_class를 빼기

2절에서 처리 함수 `chat_stream`의 데코레이터 줄에는 인자 `response_class=EventSourceResponse`가 있었습니다.
FastAPI 문서는 `yield`를 쓰는 처리 함수에 이 인자를 적으면 SSE로 보낸다고 적습니다.
이 실험은 이 인자를 빼면 응답이 어떻게 되는지 봅니다.
바꿀 값은 인자 `response_class` 하나이고, 처리 함수와 질문은 그대로 둡니다.

**가설** — FastAPI 문서의 JSON Lines 쪽은 `response_class` 없이 `yield`만 쓰면 JSON 줄 형식으로 보낸다고 적습니다.
JSON 줄 형식(JSON Lines)은 한 줄에 JSON 글 하나를 적는 형식입니다.
출석부에 한 줄에 한 사람씩 적는 일과 같고, 이 형식의 본문 종류는 `application/jsonl`입니다.
실행 2에서는 본문 종류가 `application/jsonl`이 되고, 줄 `event:`가 사라질 것입니다.
처리 함수가 내놓는 값은 두 실행 모두 일곱이라, 나온 덩어리 수는 같을 것입니다.

두 실행에 쓸 처리 함수를 먼저 정의합니다.
앱의 `chat_stream`에서 시간 제한과 이어 받기, 접근 토큰, 오류 처리 줄을 뺀 작은 판입니다.
그래프는 의존성으로 받지 않고, 1절에서 가져온 `agent`를 바로 씁니다.
데코레이터 줄이 없어, 이 셀에서는 아직 요청 주소에 잇지 않습니다.

### [37] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.483419Z', 'iopub.status.busy': '2026-09-29T08:53:39.483375Z', 'iopub.status.idle': '2026-09-29T08:53:39.485274Z', 'shell.execute_reply': '2026-09-29T08:53:39.484923Z'}}

```python
# 앱 chat_stream에서 시간 제한·이어 받기·접근 토큰·오류 처리를 뺀 작은 처리 함수를 정의합니다
async def stream_answer(body: ChatRequest):
    graph_input = {"messages": [body.question]}
    index = 0
    async for chunk in agent.astream(graph_input, stream_mode="custom"):
        event_id = body.thread_id + ":" + str(index)
        yield ServerSentEvent(data=chunk, event="token", id=event_id)
        index = index + 1
    yield ServerSentEvent(data={"thread_id": body.thread_id}, event="done")
```

출력:
```

```

### [38] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
정의 줄이 `async def`이고 몸통에 `yield`가 둘 있어, 이 함수도 비동기 제너레이터 함수입니다.
사건 번호는 앱의 함수 `_event_id`처럼 스레드 이름과 자리 번호를 `:`로 이어 만듭니다.
함수 `str`은 자리 번호를 글로 바꿉니다.

다음 셀은 본문 글에서 `event: `로 시작하는 줄을 세는 함수를 정의합니다.
두 실행의 본문에 사건 이름 줄이 몇 개 있는지 견줄 때 씁니다.

### [39] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.485813Z', 'iopub.status.busy': '2026-09-29T08:53:39.485773Z', 'iopub.status.idle': '2026-09-29T08:53:39.487407Z', 'shell.execute_reply': '2026-09-29T08:53:39.487127Z'}}

```python
# 본문 글을 줄로 나눠, "event: "로 시작하는 줄의 수를 내놓습니다
def count_event_lines(body_text):
    count = 0
    for line in body_text.splitlines():
        if line.startswith("event: "):
            count = count + 1
    return count
```

출력:
```

```

### [40] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
메서드 `startswith`는 글이 주어진 글로 시작하면 `True`를 내놓습니다.

**실행 1** — 다음 셀은 새 앱 객체를 만들고, 인자 `response_class=EventSourceResponse`를 주어 처리 함수를 잇습니다.
메서드 `add_api_route`는 처리 함수를 요청 방식과 요청 주소에 잇는 메서드입니다.
설치판 소스에서는 데코레이터 줄 `@app.post(…)`도 안에서 같은 이름의 메서드를 부릅니다.
같은 함수를 두 실행에 그대로 쓰려고, 데코레이터 줄 대신 이 메서드를 씁니다.

실행 전에 예상해 봅니다.
본문 글은 3절에서 앱이 보낸 글과 같을까요?

### [41] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.487953Z', 'iopub.status.busy': '2026-09-29T08:53:39.487908Z', 'iopub.status.idle': '2026-09-29T08:53:39.492388Z', 'shell.execute_reply': '2026-09-29T08:53:39.491978Z'}}

```python
# 실행 1: response_class=EventSourceResponse를 주어 처리 함수를 잇고, 같은 질문을 보냅니다
sse_app = FastAPI()
sse_app.add_api_route("/v1/chat/stream", stream_answer, methods=["POST"], response_class=EventSourceResponse)
sse_client = TestClient(sse_app)
run1 = sse_client.post("/v1/chat/stream", json=question_body)
print("상태 코드:", run1.status_code)
print("본문 종류:", run1.headers["content-type"])
print("3절 앱 응답 본문과 같은가:", run1.text == response.text)
print("event: 로 시작하는 줄 수:", count_event_lines(run1.text))
```

출력:
```
상태 코드: 200
본문 종류: text/event-stream; charset=utf-8
3절 앱 응답 본문과 같은가: True
event: 로 시작하는 줄 수: 7

```

### [42] markdown {}

**결과 읽기** — 출력 줄 `상태 코드: 200`과 `본문 종류: text/event-stream; charset=utf-8`이 보입니다.
출력 줄 `3절 앱 응답 본문과 같은가: True`도 보입니다.
작은 판이 보낸 본문 글이, 3절에서 앱의 `chat_stream`이 보낸 글과 같았습니다.
사건 이름 줄은 `event: 로 시작하는 줄 수: 7`로 일곱입니다.

**실행 2** — 다음 셀은 새 앱 객체에 같은 처리 함수를 잇되, 인자 `response_class`만 뺍니다.
요청 주소와 요청 방식, 처리 함수, 질문은 실행 1과 같습니다.
실행 전에 예상해 봅니다.
본문 종류와 사건 이름 줄의 수는 어떻게 바뀔까요?

### [43] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.492959Z', 'iopub.status.busy': '2026-09-29T08:53:39.492916Z', 'iopub.status.idle': '2026-09-29T08:53:39.496645Z', 'shell.execute_reply': '2026-09-29T08:53:39.496318Z'}}

```python
# 실행 2: 값 하나만 바꿔, response_class를 빼고 같은 처리 함수를 잇고 같은 질문을 보냅니다
plain_app = FastAPI()
plain_app.add_api_route("/v1/chat/stream", stream_answer, methods=["POST"])
plain_client = TestClient(plain_app)
run2 = plain_client.post("/v1/chat/stream", json=question_body)
print("상태 코드:", run2.status_code)
print("본문 종류:", run2.headers["content-type"])
print("응답 머리 이름:", list(run2.headers))
print("event: 로 시작하는 줄 수:", count_event_lines(run2.text))
```

출력:
```
상태 코드: 200
본문 종류: application/jsonl
응답 머리 이름: ['content-type']
event: 로 시작하는 줄 수: 0

```

### [44] markdown {}

**결과 읽기** — 출력 줄 `상태 코드: 200`과 `본문 종류: application/jsonl`이 보입니다.
출력 줄 `응답 머리 이름: ['content-type']`와 `event: 로 시작하는 줄 수: 0`도 보입니다.
응답은 성공했지만, 본문 종류가 SSE가 아니고 사건 이름 줄도 없습니다.
실행 1에 있던 칸 `cache-control`과 `x-accel-buffering`도 붙지 않았습니다.

다음 셀은 실행 2의 본문 글을 줄로 나눠, 줄 수와 첫 줄·끝 줄을 출력합니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.497206Z', 'iopub.status.busy': '2026-09-29T08:53:39.497156Z', 'iopub.status.idle': '2026-09-29T08:53:39.498755Z', 'shell.execute_reply': '2026-09-29T08:53:39.498416Z'}}

```python
# 실행 2의 본문 글을 줄로 나눠, 줄 수와 첫 줄·끝 줄을 출력합니다
run2_lines = run2.text.splitlines()
print("줄 수:", len(run2_lines))
print("첫 줄:", run2_lines[0])
print("끝 줄:", run2_lines[-1])
```

출력:
```
줄 수: 7
첫 줄: {"data": {"token": "\uc9c8\ubb38\uc744 "}, "raw_data": null, "event": "token", "id": "sse-1:0", "retry": null, "comment": null}
끝 줄: {"data": {"thread_id": "sse-1"}, "raw_data": null, "event": "done", "id": null, "retry": null, "comment": null}

```

### [46] markdown {}

**결과 읽기** — 출력 줄 `줄 수: 7`이 보입니다.
첫 줄에는 `"event": "token", "id": "sse-1:0"`이 들어 있고, 끝 줄에는 `"event": "done", "id": null`이 있습니다.
줄 하나에 JSON 글이 하나씩 있고, 줄 사이에 빈 줄이 없습니다.
사건 이름과 번호가 줄 머리가 아니라, JSON 글의 키로 적혔습니다.

다음 셀은 실행 2의 첫 줄을 `json.loads`로 읽어, 키 목록과 칸 값을 봅니다.

### [47] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.499304Z', 'iopub.status.busy': '2026-09-29T08:53:39.499264Z', 'iopub.status.idle': '2026-09-29T08:53:39.500913Z', 'shell.execute_reply': '2026-09-29T08:53:39.500595Z'}}

```python
# 실행 2의 첫 줄을 json.loads로 읽어, 키 목록과 칸 data·값이 없는 칸을 봅니다
first_item = json.loads(run2_lines[0])
print("첫 줄을 읽은 값의 키:", list(first_item))
print("칸 data:", first_item["data"])
print("칸 raw_data·retry·comment:", first_item["raw_data"], first_item["retry"], first_item["comment"])
```

출력:
```
첫 줄을 읽은 값의 키: ['data', 'raw_data', 'event', 'id', 'retry', 'comment']
칸 data: {'token': '질문을 '}
칸 raw_data·retry·comment: None None None

```

### [48] markdown {}

**결과 읽기** — 출력 줄 `첫 줄을 읽은 값의 키: ['data', 'raw_data', 'event', 'id', 'retry', 'comment']`가 보입니다.
양식 클래스 `ServerSentEvent`의 칸 여섯이 모두 키로 들어 있습니다.
칸 `data`는 `{'token': '질문을 '}`로 실행 1과 같은 값이고, 적지 않은 세 칸은 `None`입니다.
실행 2에서는 우리가 내놓은 객체가 SSE 사건이 아니라, 칸 여섯을 가진 JSON 글로 나갔습니다.

다음 셀은 두 앱의 응답 문서에서, 응답 200의 본문 종류와 항목 형식을 꺼냅니다.
메서드 `openapi`는 앱이 받는 요청과 내놓는 응답을 적은 문서를 딕셔너리로 내놓습니다.
이 문서(OpenAPI)는 08절에서 자세히 봅니다.

### [49] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.501427Z', 'iopub.status.busy': '2026-09-29T08:53:39.501388Z', 'iopub.status.idle': '2026-09-29T08:53:39.505270Z', 'shell.execute_reply': '2026-09-29T08:53:39.505025Z'}}

```python
# 두 앱의 응답 문서에서, 요청 주소 응답 200의 본문 종류와 항목 형식을 꺼냅니다
run1_spec = sse_app.openapi()["paths"]["/v1/chat/stream"]["post"]
run2_spec = plain_app.openapi()["paths"]["/v1/chat/stream"]["post"]
run1_content = run1_spec["responses"]["200"]["content"]
run2_content = run2_spec["responses"]["200"]["content"]
print("실행 1 본문 종류:", list(run1_content))
print("실행 1 항목 형식의 칸:", list(run1_content["text/event-stream"]["itemSchema"]["properties"]))
print("실행 2 본문 종류:", list(run2_content))
print("실행 2 항목 형식:", run2_content["application/jsonl"]["itemSchema"])
```

출력:
```
실행 1 본문 종류: ['text/event-stream']
실행 1 항목 형식의 칸: ['data', 'event', 'id', 'retry']
실행 2 본문 종류: ['application/jsonl']
실행 2 항목 형식: {}

```

### [50] markdown {}

**결과 읽기** — 출력 줄 `실행 1 본문 종류: ['text/event-stream']`과 `실행 2 본문 종류: ['application/jsonl']`이 보입니다.
실행 1의 항목 형식에는 칸 `['data', 'event', 'id', 'retry']`가 적혀 있습니다.
실행 2의 항목 형식은 빈 딕셔너리 `{}`입니다.
응답 문서에 적히는 본문 종류도 인자 `response_class` 하나로 달라졌습니다.

다음 셀은 두 실행을 한 표로 모읍니다.
덩어리 수는 실행 1이 SSE 사건 수, 실행 2가 JSON 줄 수입니다.

### [51] code {'execution': {'iopub.execute_input': '2026-09-29T08:53:39.505824Z', 'iopub.status.busy': '2026-09-29T08:53:39.505778Z', 'iopub.status.idle': '2026-09-29T08:53:39.507603Z', 'shell.execute_reply': '2026-09-29T08:53:39.507276Z'}}

```python
# 두 실행의 상태 코드·본문 종류·덩어리 수·event: 줄 수·응답 머리 수를 한 표로 모읍니다
run1_count = len(split_sse(run1.text))
print("견준 것 | 실행 1 | 실행 2")
print("response_class | EventSourceResponse | 없음")
print("상태 코드 |", run1.status_code, "|", run2.status_code)
print("본문 종류 |", run1.headers["content-type"], "|", run2.headers["content-type"])
print("덩어리 수 |", run1_count, "|", len(run2_lines))
print("event: 줄 수 |", count_event_lines(run1.text), "|", count_event_lines(run2.text))
print("응답 머리 수 |", len(run1.headers), "|", len(run2.headers))
```

출력:
```
견준 것 | 실행 1 | 실행 2
response_class | EventSourceResponse | 없음
상태 코드 | 200 | 200
본문 종류 | text/event-stream; charset=utf-8 | application/jsonl
덩어리 수 | 7 | 7
event: 줄 수 | 7 | 0
응답 머리 수 | 3 | 1

```

### [52] markdown {}

**결과 읽기** — 라벨 줄 아래 여섯 줄이 두 실행을 견줍니다.
본문 종류 줄은 `본문 종류 | text/event-stream; charset=utf-8 | application/jsonl`입니다.
덩어리 수는 `덩어리 수 | 7 | 7`로 같고, 사건 이름 줄은 `event: 줄 수 | 7 | 0`입니다.
응답 머리 수는 `응답 머리 수 | 3 | 1`이고, 상태 코드는 두 실행 모두 200입니다.

**결론** — 바꾼 값은 인자 `response_class` 하나였습니다.
같은 처리 함수가 같은 값 일곱을 내놓았지만, 이 인자가 없으면 본문이 JSON 줄 일곱이 되었습니다.
받는 쪽이 사건 이름을 찾는 줄 `event:`와, SSE 응답 머리 둘도 사라졌습니다.
그래서 앱의 `chat_stream`은 데코레이터 줄에 이 인자를 적어 SSE로 보냅니다.
이 노트북은 걸린 시간을 재지 않았고, 응답 글의 모양과 차례만 확인했습니다.

## 정리

1. 처리 함수 `chat_stream`은 비동기 제너레이터 함수로, 진행 값마다 사건 이름 `token`을 붙여 `yield`로 내놓았습니다.
2. 응답 본문은 빈 줄로 끝나는 SSE 사건 일곱이었고, 칸 `data`를 읽은 값은 처리 함수가 내놓은 값과 같았습니다.
3. 인자 `response_class`를 빼자 같은 값 일곱이 JSON 줄 형식으로 나갔고, 줄 `event:`는 0개였습니다.

06절에서는 끊긴 뒤 사건 번호로 이어 받는 방법과, 오류 사건 `error`를 봅니다.

## 그림

### 05-1-진행-값에서-SSE-사건까지.mmd

```mermaid
flowchart TB
  %% classes
  req["요청 본문<br>질문 반납 기한을 알려 주세요<br>thread_id sse-1"]:::tool
  runs["처리 함수 chat_stream이<br>astream 모드 custom을 부름"]:::tool
  prog["진행 값 여섯<br>칸 token 하나씩"]:::measure
  tok["진행 값마다 yield<br>사건 이름 token<br>사건 번호 sse-1:0에서 sse-1:5"]:::tool
  fin["끝에 yield<br>사건 이름 done 하나<br>사건 번호 없음"]:::tool
  lib["라이브러리가 사건마다<br>줄 event data id로 적음"]
  out["응답 본문 SSE 사건 일곱<br>text/event-stream"]:::measure
  req --> runs --> prog --> tok --> fin --> lib --> out
```

처리 함수 chat_stream은 진행 값 여섯마다 사건 이름 token을, 끝에 done을 yield로 내놓았고, 라이브러리가 이를 SSE 사건 일곱의 글로 적었습니다.

### 05-2-SSE-사건-하나의-칸.mmd

```mermaid
flowchart TB
  %% classes
  body["응답 본문 글<br>text/event-stream"]:::measure
  sp["split_sse<br>빈 줄로 나눠<br>SSE 사건 일곱"]:::flow
  first["첫 SSE 사건 글<br>event: token<br>data: JSON 글<br>id: sse-1:0"]:::measure
  pa["parse_sse<br>처음 쌍점과 공백에서<br>한 번만 나눔"]:::flow
  names["칸 이름 셋<br>event data id"]:::measure
  lo["json.loads로<br>칸 data를 읽음"]:::flow
  val["읽은 값 dict<br>처리 함수가 내놓은<br>값과 같음 True"]:::measure
  body --> sp --> first --> pa --> names --> lo --> val
```

응답 본문 글을 빈 줄로 나누면 SSE 사건 일곱이 되고, 사건 하나를 줄마다 나누면 칸 event·data·id가 되며, 칸 data의 JSON 글은 json.loads로 읽었습니다.

### 05-3-처리-함수가-내놓은-값과-응답-글.mmd

```mermaid
flowchart TB
  %% classes
  fn["처리 함수 chat_stream<br>질문 반납 기한을 알려 주세요"]:::tool
  direct["바로 부름<br>async for로 꺼냄"]:::flow
  objs["ServerSentEvent 일곱<br>token 여섯 done 하나"]:::measure
  http["시험용 클라이언트로 POST<br>본문을 끝까지 모아 받음"]:::flow
  texts["본문 글 SSE 사건 일곱<br>칸 data는 JSON 글"]:::measure
  same["token 사건의 data<br>처리 함수 값과 같음 True"]:::measure
  fn --> direct --> objs --> same
  fn --> http --> texts --> same
```

처리 함수를 바로 불러 꺼낸 값과, HTTP 응답 글을 나눠 읽은 값이 같았습니다.

### 05-4-response-class-유무와-응답-모양.mmd

```mermaid
flowchart TB
  %% classes
  same["같은 처리 함수 stream_answer<br>같은 질문 yield 일곱 번"]:::flow
  subgraph r1["실행 1 · response_class 있음"]
    direction TB
    a1["response_class=<br>EventSourceResponse"]:::flow
    b1["본문 종류<br>text/event-stream"]:::measure
    c1["SSE 사건 일곱<br>event: 줄 일곱"]:::measure
    a1 --> b1 --> c1
  end
  subgraph r2["실행 2 · response_class 없음"]
    direction TB
    a2["response_class<br>빼기만 함"]:::flow
    b2["본문 종류<br>application/jsonl"]:::measure
    c2["JSON 줄 일곱<br>event: 줄 없음"]:::measure
    a2 --> b2 --> c2
  end
  same --> r1
  same --> r2
```

같은 처리 함수가 같은 값 일곱을 내놓아도, 인자 response_class를 빼자 본문이 SSE 사건이 아니라 JSON 줄 일곱이 되었습니다.

### 05-5-이름판과-번호판을-단-화물-칸.prompt.md

# 05-5-이름판과-번호판을-단-화물-칸 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 화물역으로 짐칸 일곱 량이 이어진 화물 열차가 들어옵니다. 짐칸 여섯의 옆면에는 같은 색 이름판과 작은 번호판이 하나씩 붙어 있습니다. 맨 끝 칸에는 색이 다른 이름판만 있고, 번호판은 없습니다. … 짐칸 하나가 SSE 사건 하나이고, 이름판이 칸 event의 사건 이름입니다. 번호판이 칸 id의 사건 번호이고, 칸에 실린 짐이 칸 data의 자료입니다. 이름판만 단 끝 칸은 사건 번호가 없는 done 사건입니다.

구성 요소와 배치: **선로 하나**(자갈 바닥) · 한 줄로 이어진 **짐칸 일곱**(기관차 없음 — 칸이 곧 SSE 사건이라 기관차는 대응하는 것이 없어 뺌) = 똑같은 하늘색 닫힌 짐칸 **여섯**(옆면마다 짙은 초록 네모 판 **하나**(= 사건 이름 `token`) + 작은 흰 동그라미 판 **하나**(= 사건 번호)) + 맨 끝 연한 주황 짐칸 **하나**(짙은 갈색 네모 판 **하나**만(= 사건 이름 `done`), 동그라미 판 **없음**(= `done`은 사건 번호 없음 — 노트북 셀 [15] `7 | done | 없음`)) · 칸 사이는 작은 틈과 연결 고리(= 사건 사이의 빈 줄). 번호판은 글자·숫자 없는 모양으로(흰 동그라미). 비유 계열 **「화물 열차와 번호판 차량」 — 번호판을 처음 그림**. 01 소품(창고·파란 규격 틀·흰 차단봉·빈 화차)·02 소품(주황·파란 기관차·초록 짐칸·세 줄 선로)·03 소품(짙은 회색 기관차·갈색 뚜껑 없는 짐칸·노란 손수레·나무 상자·꾸러미 더미·멈춤 막이)·04 소품(짙은 빨강 기관차·옅은 회색 평판 짐칸·청록 통·겨자색 망루 끝 칸·콘크리트 짐 내리는 자리) 되풀이 안 함. 금지 소품(오르골·종이띠·도킹 포트·정거장·우주선·온실·모종판·예인선·바지선·밧줄·홈통·물방울·도미노·체스판·즉석사진·세탁기·승강 상자·전표·가마·물레·발자국·말뚝·쟁반·서랍·바구니·저울·도장·개찰구·플러그·공항 검사·안내 데스크·주문표·창구·택배·출입구) 없음. 사람·손·글자·숫자·화살표·표지판·화면·건물 없음. 03·04의 위아래 흰 여백을 되풀이하지 않게 구도를 적음.

시선 순서: 하늘색 짐칸 여섯(같은 초록 네모 판과 흰 동그라미 판) → 맨 끝 주황 짐칸(갈색 네모 판만, 동그라미 판 없음).

검수 기준: 그림만 보고 「같은 판 두 개를 단 칸 여섯 뒤에, 판이 하나뿐이고 색이 다른 칸 하나가 끝에 붙어 있다」가 읽히는가. 짐칸 일곱(하늘색 여섯·주황 하나)이 서로 떨어져 셀 수 있는가. 하늘색 칸마다 네모 판 하나·동그라미 판 하나인가. 끝 칸에 동그라미 판이 없는가. 글자·숫자·사람·화살표가 없는가. 흰 여백이 크지 않은가.

## 프롬프트 (1차, 탈락)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. Close side view of a short freight train standing on one straight track laid on a wide gravel bed, no locomotive. Exactly seven short, boxy, tall boxcars coupled in one row; together they fill the frame from the left edge to the right edge and take up most of the picture height. Exactly six identical sky-blue boxcars, each with exactly one dark green rectangular plate and exactly one small round white plate side by side on its side wall. At the far left end, exactly one pale orange boxcar of the same shape with only one dark brown rectangular plate and no round plate. The plates are plain, with no marks. No people, no arrows, no signs, no screens, no buildings.
```

## 프롬프트 (2차 — 재생성 1회, 채택)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. Elevated three-quarter view of one straight railway track on a gravel bed running diagonally from the lower right corner to the upper left corner, so the train fills the whole frame. On it stand exactly seven separate short boxcars in one row, each car clearly separated from the next by a small gap with a coupler, no locomotive, all seven cars fully visible. The six cars nearest the lower right are identical sky-blue boxcars; each shows on its long side exactly one dark green rectangular plate and exactly one small round white plate. The last car, at the upper left end, is a pale orange boxcar of the same shape with only one dark brown rectangular plate and no round plate. Plain plates with no marks. No people, no arrows, no signs, no screens, no buildings.
```

## 상태

- 2026-09-29 · `generate_image` 두 번(재생성 1회 — 규격 §5-4 한도 안), `params` = `{"model":"nano_banana_pro","prompt":…,"aspect_ratio":"16:9","resolution":"2k","use_unlim":false,"count":1}`. `generate_image` 응답 모델 `nano_banana_pro`, **`jobs_wait` 응답 모델 표시 `nano_banana_2`**(01~04와 같은 표시, 거래 표시는 「Nano Banana Pro」 — 기록만). 서비스 쪽 실패 0.
- 생성 전 잔액 **2283**, 바로 앞 거래 2026-09-29T08:20:53.295871Z는 Ch 30 04절 몫.
- **1차 job `262db619-003e-4c20-9757-5b23ae54e936`** — 거래 2026-09-29T08:56:21.752543Z 「Nano Banana Pro −2」. 원본 `866c0735d1a7d539b2ddb9c08d2750b5cc96cd921216e00edf7a2c227af71d12`(2752 × 1536). 옆에서 본 구도로, 하늘색 칸이 서로 붙어 **긴 칸 하나(판 짝 셋)·칸 하나(판 짝 둘)·오른쪽 끝에서 잘린 칸 하나(판 짝 하나)**로 그려짐 — 판 짝은 여섯이지만 칸이 여섯으로 나뉘지 않아 「칸 하나 = 사건 하나」가 읽히지 않고, 주황 칸도 왼쪽 끝에서 잘림, 위아래 흰 여백 약 25% → **탈락**.
- **2차 job `c1305011-96f8-4680-af9d-b00658587772`** — 거래 2026-09-29T08:57:46.544682Z 「Nano Banana Pro −2」. 원본 `0b6fc1024ee06fd2e62dbbc1317993e154a7e08df94603a3926f1869c24ecf95`(2752 × 1536). 비스듬한 구도(handoff §04 → §05 11 권고)로 칸 일곱이 서로 떨어져 셀 수 있음 → **채택**. **이 절 몫 거래 두 줄, 4크레딧**(잔액 2283 → 2279).
- **그림에서 확인한 것(그림 읽기·alt에 반영)**: 흰 바탕에 자갈 바닥 위 선로 **하나**가 오른쪽 아래에서 왼쪽 위로 비스듬히 · 선로 위 닫힌 짐칸 **일곱**이 한 줄, 칸 사이 작은 틈과 검은 연결 고리 · 오른쪽 아래부터 하늘색 짐칸 **여섯**, 칸마다 옆면에 짙은 초록 네모 판 **하나**와 작은 흰 동그라미 판 **하나** · 맨 왼쪽 위 끝 연한 주황 짐칸 **하나**, 짙은 갈색 네모 판 **하나**만, 흰 동그라미 판 **없음**. 기관차·사람·손·글자·숫자·화살표·표지판·화면·건물 없음. 거의 흰 가로줄 **6줄 / 614줄**(04 채택본 423줄) — 흰 부분은 오른쪽 위·왼쪽 아래 삼각형 자리뿐.
- 검수: 「같은 판 두 개를 단 칸 여섯 뒤에, 판이 하나뿐이고 색이 다른 칸 하나가 끝에 붙어 있다」가 그림만으로 읽힘 → 채택. **그림과 비유 글의 차이**: 그림 속 열차는 서 있고(본문 비유는 「들어옵니다」 — 그림 읽기는 보이는 것만 적음), 번호판은 모두 같은 흰 동그라미(실제 사건 번호는 칸마다 하나씩 커짐 — 그림 읽기에 밝힘), 짐은 닫힌 칸 안이라 보이지 않음.
- 저장: 기기 셸에서 결과 URL을 `curl`로 받아(`/tmp/ch30-05/illu/illu-2-orig.png`) `UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pillow`로 RGB·폭 1100px(LANCZOS)로 줄여 `figures/05-5-이름판과-번호판을-단-화물-칸.png`(1100 × 614, `eb733ea5956e99e4816aca625fd8273f75c5afc3838ca137789e0954cc671241`)로 저장했습니다.
- 결과 URL을 한 번 더 받아(`illu-2-again.png`, 원본과 해시 같음) 같은 폭으로 줄인 그림과 저장 PNG를 픽셀 대조했습니다(`ImageChops.difference` bbox `None`, 최대 차이 0). 저장 PNG와 같은 사본(`.cache/ch30-05-view/illu-2-1100.png`)을 직접 열어 개수를 세고 그림 읽기를 썼습니다.

