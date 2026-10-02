# 05-retriever를-도구로-전환

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 1h | 실습 2h | 코드 notebooks/05-retriever를-도구로-전환.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>Ch 14 06절 검색 함수 <code>search_hits</code>를 <code>@tool</code> 도구로 감싸 <code>create_agent</code>에 넘길 수 있습니다.</li>
<li>모델이 채운 검색어와 도구 메시지의 문서 ID를 출력으로 읽고, 같은 검색어면 같은 문서가 나오는지 확인할 수 있습니다.</li>
<li>다시 검색을 시스템 메시지 글로만 정했을 때, 검색 횟수가 코드 제한이 아니라 모델 선택임을 설명할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>제목의 retriever는 질문을 받아 가까운 문서를 찾아 주는 검색 부분을 가리키는 영어 말입니다. 이 과정에서는 <a href="../../part4/ch14-rag-patterns/06-CRAG.html">Ch 14 06절</a> 검색 함수 <code>search_hits</code>가 그 일을 했습니다. 이 절은 그 검색 함수를 에이전트 그래프의 도구로 바꿉니다.</p><p>Ch 14 06절에서는 코드가 질문 글을 그대로 검색에 넣어 먼저 한 번 검색했습니다. 다시 검색할지도 코드가 첫 자리 거리를 기준값과 견주어 정했습니다. Ch 14의 다른 절에서 모델이 질문을 고쳐 썼을 때도, 검색을 부르는 때는 코드가 정했습니다. 검색 함수를 도구로 감싸면, 검색할지와 무엇으로 검색할지를 모델이 고릅니다.</p><p>모델이 고르는 값은 편리하지만 흔들릴 수 있습니다. 그래서 이 절은 모델이 고른 값과 코드가 정한 값을 출력에서 나눠 셉니다. 검색어와 검색 횟수는 모델 쪽이고, 도구 메시지의 문서 개수와 호출 ID 짝은 코드 쪽입니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href="../../part3/ch09-rag-first-run/01-RAG-지도.html">Ch 9 01절</a>에서 임베딩 모델 <code>OpenAIEmbeddings</code>로 글을 벡터로 바꿨고, <a href="../../part3/ch10-document-processing/07-한국어-임베딩과-캐시.html">Ch 10 07절</a>에서 벡터 크기 인자 <code>dimensions</code>를 보았습니다. <a href="../../part1/ch05-llm-principles/02-임베딩과-의미-유사도.html">Ch 5 02절</a>에서는 코사인 유사도를 NumPy로 계산했습니다. <a href="../../part3/ch12-retrieval-tuning/01-벡터-거리와-정확-검색.html">Ch 12 01절</a>에서는 코사인 거리와 거리 순위 함수를, <a href="../../part3/ch12-retrieval-tuning/05-dense와-sparse-비교.html">05절</a>에서는 순위 출력 함수 <code>print_ranked</code>를 적었습니다.</p><p><a href="../../part4/ch14-rag-patterns/06-CRAG.html">Ch 14 06절</a>은 질문 하나를 벡터로 바꿔 거리 순위를 만드는 <code>search_hits</code>를 적었습니다. 같은 절은 첫 자리 거리가 기준값보다 크면 한 번만 다시 검색하게 했고, 그 상한을 코드로 확인했습니다. 문서 모음은 Ch 12와 같은 문서 열두 건과 질문 여덟 건입니다. 질문마다 <a href="../../part3/ch11-evaluation/01-질의셋과-정답-문서-ID.html">Ch 11 01절</a>의 정답 문서 ID가 적혀 있습니다.</p><p><a href="../../part5/ch19-model-tools/01-tool과-Ch4-함수-재사용.html">Ch 19 01절</a>에서는 맨 <code>@tool</code>로 도구를 만들고 도구 명세를 보았습니다. <a href="../../part5/ch19-model-tools/05-bind_tools와-병렬-호출.html">Ch 19 05절</a>에서는 도구 호출 요청을 도구에 넘겨 도구 메시지를 받았습니다. <a href="01-create-agent와-ReAct-루프.html">01절</a>에서는 함수 <code>create_agent</code>와 함수 <code>agent_row</code>를, <a href="02-구조화-출력-두-전략.html">02절</a>에서는 함수 <code>print_branches</code>를 보았습니다.</p><p>05절부터는 Ch 14 문서 모음을 씁니다. Ch 14 운영 시간 문서는 평일 운영을 오전 9시부터 오후 9시까지로 적습니다. 01~04절 규정 딕셔너리는 평일 09:00~20:00으로 적었습니다. 두 글은 서로 다른 자료이고, 이 절은 01절 자료를 고치지 않습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절에서는 에이전트 그래프를 버튼 하나로 도는 세탁기에 견주었습니다. 이번에는 세제를 넣는 두 방법을 떠올려 봅니다. 하나는 빨래를 넣을 때마다 사람이 세제를 한 컵씩 먼저 붓는 방법입니다. 다른 하나는 세제 통을 세탁기에 꽂아 두고, 세탁기가 필요할 때 끌어 쓰게 하는 방법입니다.</p><p>Ch 14의 흐름은 앞의 방법처럼, 코드가 질문마다 검색을 먼저 한 번 했습니다. 이 절의 흐름은 뒤의 방법입니다. 세제 통이 검색 함수이고, 통을 꽂는 자리가 검색 도구입니다. 세탁기인 에이전트 그래프 안에서 모델이 필요할 때 검색을 부릅니다.</p>
{{img:05-5-세제-통을-꽂아-둔-세탁기|옅은 베이지 벽과 바닥이 보이는 방을 그린 그림입니다. 가운데에 흰 앞문형 세탁기 한 대가 크게 서 있고, 앞면 위쪽 띠의 오른쪽에 둥근 버튼 하나, 앞면에 둥근 유리문 하나가 있습니다. 유리문 안에서 빨래와 옅은 파란 거품이 돕니다. 세탁기 윗면 왼쪽의 둥근 구멍에 연녹색 세제 통 한 개가 거꾸로 기울어 꽂혀 있습니다. 세탁기 왼쪽 바닥에는 빈 연녹색 계량컵 한 개가 기계와 떨어져 놓여 있는 그림|바닥의 빈 계량컵은 쓰이지 않고, 세제는 세탁기에 꽂아 둔 통에서 세탁기가 끌어 씁니다.}}
<p class="look"><b>그림 읽기</b> — 가운데에 흰 세탁기 한 대가 있고, 둥근 버튼 하나와 둥근 유리문 하나가 있습니다. 윗면 왼쪽 구멍에는 연녹색 세제 통 한 개가 거꾸로 꽂혀 있고, 유리문 안에는 옅은 파란 거품이 보입니다. 왼쪽 바닥의 빈 계량컵 하나는 기계와 떨어져, 쓰이지 않은 채 놓여 있습니다. 꽂혀 있는 세제 통이 검색 도구로 감싼 검색 함수이고, 세탁기가 필요할 때 끌어 씁니다. 빈 계량컵은 사람이 매번 먼저 붓는 방법, 곧 Ch 14처럼 코드가 검색을 먼저 하는 흐름입니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>검색 함수(retriever)</td><td>질문 글을 받아 가까운 문서를 거리 차례로 찾아 내놓는 함수입니다. 제목의 retriever가 이 일을 하는 부분을 가리키고, 이 절에서는 Ch 14 06절 <code>search_hits</code>입니다. 비유에서 세제 통과 같습니다.</td></tr><tr><td>검색 도구</td><td>검색 함수를 <code>@tool</code>로 감싼 도구입니다. 모델이 도구 호출 요청을 보낼 때만 실행되고, 찾은 문서의 글을 도구 메시지로 내놓습니다. 비유에서 세제 통을 꽂는 자리와 같습니다.</td></tr><tr><td>검색어(query)</td><td>모델이 검색 도구의 인자 <code>query</code>에 적은 글입니다. 질문 글과 같을 수도 다를 수도 있고, 실행마다 달라질 수 있습니다. 비유에서 세탁기가 그때그때 정하는 세제의 양과 같습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 검색 함수는 노트북 4절 <code>search_hits(embedding_model, c05_question, …)</code> 줄입니다. 검색 도구는 5절 <code>@tool</code> 아래 <code>search_documents</code>이고, 6절에서 <code>tools=[search_documents]</code>로 넘깁니다. 검색어는 7절 출력의 인자 <code>{'query': …}</code>입니다.</p>
{{mermaid:05-1-검색-함수를-도구로-감싼-자리|위에서 아래로 한 줄로 이어지는 그림으로 맨 위 초록 상자 Ch 14 문서 열두 건 documents.json 읽기만에서 보라 상자 임베딩 모델 text-embedding-3-small 벡터 크기 256 문서 벡터 열두 개 임베딩 요청 한 번으로 화살표가 갑니다. 이어서 파란 상자 검색 함수 search_hits Ch 14 06절 도구 파일, 파란 상자 검색 도구 search_documents 인자 query 문서 세 건의 글, 회색 상자 create_agent 모델 객체 도구 하나 시스템 메시지 글이 차례로 이어지고, 맨 아래 회색 상자 에이전트 그래프 모델 노드와 도구 실행 노드 01절과 같은 모양으로 끝나는 그림|Ch 14 문서 벡터와 검색 함수 search_hits를 도구 search_documents로 감싸 create_agent에 넘겨도, 에이전트 그래프의 모양은 01절과 같습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 초록 상자는 Ch 14 문서 파일이고, 보라 상자는 실제로 부른 임베딩 모델입니다. 파란 상자 둘은 우리가 적은 코드로, 검색 함수를 도구로 감싸는 차례입니다. 회색 상자 둘은 라이브러리가 준 함수 create_agent와, 그 함수가 만든 그래프입니다. 노트북 6절 출력으로 01절과 같은 모양임을 확인했습니다.</p>
<h3>검색어와 검색 횟수를 정하는 쪽</h3><p>Ch 14 06절에서는 첫 검색어가 질문 글 그대로였습니다. 다시 검색할지는 첫 자리 거리를 기준값과 견주어 코드가 정했고, 다시 검색은 한 번까지였습니다. 이 절에서는 검색어를 모델이 인자로 적습니다. 다시 검색하라는 규칙은 시스템 메시지 글에만 있고, 그 횟수를 세거나 막는 코드는 없습니다.</p>
{{mermaid:05-2-검색어와-횟수를-정하는-쪽|위아래 칸 둘이 있는 그림으로 위 칸 Ch 14 06절 흐름 코드가 정함에는 회색 상자 첫 검색어 질문 글 그대로와 회색 상자 다시 검색할지 첫 자리 거리를 기준값과 견주어 코드가 정함 다시 검색 상한 한 번을 코드로 확인이 위아래로 놓여 있습니다. 아래 칸 이 절 흐름 모델이 고름에는 보라 상자 검색어 모델이 인자 query에 적음, 초록 상자 다시 검색 시스템 메시지 글 한 번만 더 검색 세거나 막는 코드 없음, 노란 상자 C05 질문 검색 한 번 주차 질문 검색 두 번이 위아래로 놓여 있는 그림|Ch 14 06절에서는 다시 검색할지와 그 상한을 코드가 정했고, 이 절에서는 검색어와 검색 횟수를 모델이 고릅니다.}}
<p class="look"><b>도식 읽기</b> — 위 칸이 Ch 14 06절 흐름, 아래 칸이 이 절 흐름입니다. 위 칸 회색 상자는 다른 챕터 노트북의 코드와 출력입니다. 아래 칸 보라 상자는 실제로 부른 모델이 고르는 자리이고, 초록 상자는 우리가 적은 시스템 메시지 글입니다. 노란 상자는 노트북 7·8절 출력입니다. 두 칸은 나란히 견주는 것이라 화살표로 잇지 않았습니다.</p>
<h3>다른 상황에 적용</h3><p>Ch 19의 주문 조회 흐름에 사내 안내 문서 검색을 더한다면, 같은 방법으로 검색 함수를 도구 하나로 감쌀 수 있습니다. 모델은 주문 질문에는 주문 도구를, 안내 질문에는 검색 도구를 고를 것입니다. 이 조합은 이번에 실행하지 않았습니다.</p>
<h3>비교와 경계</h3><p>LangChain에는 벡터스토어를 검색 객체로 바꾸는 <code>as_retriever()</code>도 있지만, 과정에서 쓰지 않았고 이번에도 실행하지 않았습니다. 이 절의 검색 도구는 Ch 14에서 적은 평범한 함수를 감싼 것입니다. 검색을 늘 먼저 하는 흐름과 이 흐름을 같은 질문으로 견주는 일은 <a href="06-같은-평가셋으로-RAG-비교.html">06절</a>에서 합니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 먼저 Ch 14 문서 파일과 질문 파일을 읽고, 문서 열두 건을 벡터로 바꿉니다. 질문 글을 그대로 검색 함수에 넣어 거리 순위를 본 뒤, 검색 함수를 도구로 감싸 에이전트 그래프에 넣습니다. <code>C05</code> 질문을 보내고, 같은 검색어로 도구를 다시 불러 봅니다. 값 바꿔 보기로 질문 하나만 문서에 없는 주차 질문으로 바꿉니다.</p><p>모델은 01절과 같은 <code>gpt-5.4-mini</code>이고, temperature 0과 추론 끔(<code>reasoning_effort="none"</code>)으로 부릅니다. 임베딩 모델은 Ch 14와 같은 <code>text-embedding-3-small</code>이고 벡터 크기는 256입니다. 교재 출력에서 모델 요청은 모두 5번, 임베딩 요청은 모두 6번입니다.</p>
{{notebook:05-retriever를-도구로-전환}}
<p class="look"><b>확인할 점</b> — 노트북 5절에서 명세의 인자가 <code>['query']</code> 하나인지 봅니다. 노트북 7절에서 도구 메시지가 문서 세 줄이고, 같은 검색어로 다시 부른 글이 같은지 확인합니다. 8절에서 응답마다 도구 호출 요청 수가 <code>1</code>·<code>1</code>·<code>0</code>인지 봅니다. 검색어와 답 글은 실행마다 달라질 수 있어 결론에 쓰지 않았습니다.</p>
{{mermaid:05-3-C05-질문의-차례|세로선 넷이 있는 차례 그림으로 왼쪽부터 노트북 코드 agent.invoke, 연보라 띠 안의 모델 노드 gpt-5.4-mini, 도구 실행 노드 search_documents, 연보라 띠 안의 임베딩 모델 text-embedding-3-small입니다. 노트북 코드가 모델 노드에 C05 질문 하나를 보내고 노란 메모 요청 1 도구 호출 요청 search_documents 인자 query가 붙습니다. 모델 노드에서 도구 실행 노드로 model_to_tools 화살표가 가고, 도구 실행 노드에서 임베딩 모델로 search_hits 화살표, 임베딩 모델에서 도구 실행 노드로 임베딩 요청 1번 점선이 돌아옵니다. 노란 메모 도구 메시지 success 문서 세 줄 FAC-003 LIB-002 ACC-004가 붙고, 도구 실행 노드에서 모델 노드로 tools_to_model 화살표, 노란 메모 요청 2 도구 호출 요청 0건, 모델 노드에서 노트북 코드로 END 점선이 갑니다. 마지막 노란 메모에 메시지 넷 모델 요청 두 번 임베딩 요청 한 번 호출 ID 짝 True가 적힌 그림|C05 질문에서 모델은 검색 도구를 한 번 불렀고, 도구 실행 노드의 검색 한 번에 임베딩 요청이 한 번 나갔습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽고, 세로선은 왼쪽부터 노트북 코드, 모델 노드, 도구 실행 노드, 임베딩 모델입니다. 연보라 띠 둘은 실제로 부른 모델 <code>gpt-5.4-mini</code>와 <code>text-embedding-3-small</code>이 있는 자리입니다. 노란 메모는 모두 노트북 7절과 9절 출력입니다. 임베딩 요청은 도구 실행 노드 안에서 검색 함수가 보냈고, 모델 노드는 도구 메시지 글만 받았습니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>실험에서 바꾼 것은 질문 하나입니다. 모델·검색 도구·시스템 메시지 글·문서 벡터·<code>top_count</code>는 그대로였습니다.</p>
<table><thead><tr><th>실행</th><th>메시지 수</th><th>응답 수(모델 요청)</th><th>도구 메시지 수</th><th>도구 메시지의 문서 ID</th><th>도구 안 임베딩 요청</th><th>입력 토큰</th></tr></thead><tbody><tr><td>C05 질문(7절)</td><td>4</td><td>2</td><td>1</td><td><code>FAC-003</code>·<code>LIB-002</code>·<code>ACC-004</code></td><td>1</td><td>638</td></tr><tr><td>주차 질문(8절, 바꾼 값)</td><td>6</td><td>3</td><td>2</td><td>첫째 <code>FAC-002</code>·<code>ACC-004</code>·<code>ACC-001</code> / 둘째 <code>FAC-004</code>·<code>ACC-004</code>·<code>FAC-002</code></td><td>2</td><td>1189</td></tr></tbody></table>
{{mermaid:05-4-질문만-바꾼-두-실행|맨 위 초록 상자 같은 에이전트 그래프 같은 시스템 메시지 글 바꾼 것은 질문 하나에서 칸 둘로 화살표가 갑니다. 왼쪽 칸 C05 질문 토요일 폐관 시각의 노란 상자에는 검색 한 번 도구 메시지 하나 첫 줄 FAC-003 모델 요청 두 번 입력 토큰 638, 오른쪽 칸 바꾼 값 주차 요금 질문의 노란 상자에는 검색 두 번 다시 검색 한 번 도구 메시지 둘 첫 줄 FAC-002와 FAC-004 모델 요청 세 번 입력 토큰 1189가 적혀 있습니다. 맨 아래 회색 상자에는 두 질문 공통 도구 메시지마다 문서 세 건 응답마다 도구 호출 요청 한 건 이하 호출 ID 짝 True가 적힌 그림|질문 하나만 바꾸자 검색은 한 번에서 두 번으로, 모델 요청은 두 번에서 세 번으로 늘었고, 도구 메시지마다 문서는 세 건이었습니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 초록 상자는 두 실행에 같았던 조건입니다. 아래 칸 둘은 왼쪽이 7절 실행, 오른쪽이 8절 값 바꿔 보기입니다. 노란 상자는 노트북 7~9절 출력입니다. 맨 아래 회색 상자는 두 칸 출력에서 모두 확인한 공통점입니다. 칸끼리는 화살표로 잇지 않았습니다.</p>
<p>두 질문 모두 도구 메시지마다 문서는 세 건이었습니다. 이 개수는 도구 몸통이 <code>top_count</code>로 정하는 값입니다. 주차 질문처럼 관련 문서가 없어도 거리가 가까운 문서 세 건이 나왔고, 답이 없다는 판단은 모델이 글을 읽고 내렸습니다.</p><p>검색 횟수는 <code>C05</code> 질문 한 번, 주차 질문 두 번이었습니다. 주차 질문의 두 번째 검색은 시스템 메시지 글의 「한 번만 더 검색」과 맞았습니다. 규칙 문장을 뺀 실행은 하지 않아, 규칙 때문인지는 확인하지 않았습니다. 코드가 횟수를 막은 것이 아니므로, 모델이 달리 고르면 모델 요청 수와 임베딩 요청 수가 함께 달라집니다.</p><p>새 커널로 두 번 실행했을 때 표의 값은 두 번 모두 같았습니다. 노트북 밖에서 두 질문을 다섯 번씩 보냈을 때도 같았습니다. 같은 검색어로 다시 부른 결과는 노트북 7절과 노트북 밖 확인 열다섯 번에서 모두 같은 글이었습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>노트북을 실행하기 전에 노트북 밖에서 두 질문을 다섯 번씩 보냈습니다. 메시지 종류와 차례, 응답마다 요청 수, 검색어, 도구 메시지의 문서 ID, 입력 토큰이 다섯 번 모두 같았습니다. 같은 요청도 실행한 때에 따라 모델이 고르는 검색어와 검색 횟수가 달라질 수 있습니다. 그때는 도구 메시지 수·모델 요청 수·임베딩 요청 수가 함께 달라집니다.</li><li>시스템 메시지 글의 「한 번만 더 검색」은 모델에게 적은 규칙입니다. 그래프에는 검색 횟수를 세거나 막는 줄이 없고, 함수 <code>create_agent</code>에는 모델 요청 수 한도 인자가 없습니다. 호출 수를 코드로 막는 미들웨어는 <a href="../ch22-middleware/04-호출-한도와-재시도-폴백.html">Ch 22 04절</a>에서 배웁니다. <a href="../../part5/ch20-tool-node/03-recursion-limit과-명시적-종료.html">Ch 20 03절</a>의 실행 한도는 그래프 단계 수라, 검색 횟수와 같은 값이 아닙니다.</li><li>모델이 규칙을 넘겨 세 번 검색하는 실행은 이번에 없었고, 실행하지 않았습니다. 모델이 검색 도구를 부르지 않는 경우와 도구 안에서 오류가 나는 경우도 이번에 실행하지 않았습니다.</li><li>셀의 <code>assert</code>는 도구 메시지마다 문서 개수와 호출 ID 짝에만 걸었습니다. 검색어와 답 글은 모델이 쓴 글이라 <code>assert</code>하지 않았고 결론에도 쓰지 않았습니다.</li><li>같은 검색어로 다시 부른 결과가 같은지는 출력으로만 보았습니다. 임베딩 값은 요청마다 소수 끝자리에서 아주 조금 달라질 수 있어, 거리가 거의 같은 두 문서는 차례가 바뀔 수 있습니다. 그래서 이 비교에는 <code>assert</code>를 걸지 않았습니다.</li><li>Ch 14 실습 폴더에는 저장해 둔 문서 벡터 파일이 없습니다. 그래서 문서 벡터를 노트북마다 한 번 만들고, 파일로 쓰지 않았습니다.</li><li>Ch 14 운영 시간 문서는 평일 운영을 오전 9시~오후 9시로 적습니다. 01절 규정 딕셔너리는 평일 09:00~20:00으로 적었고, 두 글은 서로 다른 자료입니다. 이 절은 01절 자료를 고치지 않았습니다.</li><li><code>C05</code> 질문, 주차 질문, 도구 글, 시스템 메시지 글, <code>top_count</code> 3은 흐름을 보여 주려고 정한 예입니다. 모두 노트북 밖 확인 전에 정했습니다.</li><li>함수 <code>search_hits</code>·<code>print_ranked</code>와 거리 함수 셋은 Ch 14 도구 파일에서 본문을 글자 그대로 옮겼습니다. 함수 <code>estimate_cost</code>는 <a href="../../part2/ch06-langchain-start/06-토큰-비용-지연-비교.html">Ch 6 06절</a>에서 배웠습니다.</li><li>예상 비용은 모델 몫만 2026-09-17 요금표로 어림했고, 노트북 한 번에 0.01달러 아래이며 청구 금액이 아닙니다. 임베딩 요금(100만 토큰당 0.02달러)은 토큰 수를 세지 않아 넣지 않았습니다. 걸린 시간은 재지 않았습니다.</li><li>교재 출력은 Linux의 Python 3.12.13으로 만들었습니다. 다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>Ch 14 06절 검색 함수 <code>search_hits</code>를 <code>@tool</code> 도구로 감싸자, 모델이 인자 <code>query</code>에 검색어를 적어 검색을 불렀습니다.</li><li>같은 검색어로 도구를 다시 부르면 같은 문서 셋이 같은 차례로 나왔고, 도구 메시지마다 문서는 <code>top_count</code>건이었습니다.</li><li>문서에 답이 없는 질문에서 모델은 검색을 두 번 했고, 「한 번만 더」는 시스템 메시지 글일 뿐 코드 제한이 아니었습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href="06-같은-평가셋으로-RAG-비교.html">06절</a>에서는 같은 평가 질문을 두 흐름으로 보내 견줍니다. 검색을 먼저 하는 흐름과, 검색 도구를 쓰는 에이전트 흐름입니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 검색 도구 <code>search_documents</code>의 도구 명세에 실린 인자는 무엇이고, 그 값은 누가 채웠나요?</p><p class="quiz-a">인자는 <code>query</code> 하나이고, 모델이 검색어를 적어 채웠습니다. 문서 벡터와 자를 개수는 노트북이 정해 둔 값이라 명세에 없습니다. 틀렸다면 노트북 5절과 7절을 다시 읽습니다.</p><p class="quiz-q">2. 첫 응답의 도구 호출 요청을 도구에 다시 보냈을 때 무엇이 같았고, 왜 <code>assert</code>를 걸지 않았나요?</p><p class="quiz-a">다시 받은 도구 메시지 글이 처음 도구 메시지 글과 같았습니다. 같은 검색어면 같은 문서 셋이 같은 차례로 나옵니다. 다만 임베딩 값이 요청마다 아주 조금 달라질 수 있어 <code>assert</code>는 걸지 않았습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">3. 주차 질문에서 검색 도구는 관련 문서가 없는데도 무엇을 내놓았나요?</p><p class="quiz-a">거리가 가까운 차례로 문서 세 건을 내놓았고, 첫 도구 메시지의 첫 줄은 프린터 이용 문서 <code>FAC-002</code>였습니다. 답이 없다는 판단은 모델이 도구 메시지 글을 읽고 내렸습니다. 틀렸다면 노트북 8절을 다시 읽습니다.</p><p class="quiz-q">4. 「한 번만 더 검색」 규칙은 어디에 적혀 있고, 이번 검색 횟수는 무엇이 정했나요?</p><p class="quiz-a">규칙은 시스템 메시지 글에만 있고, 검색 횟수는 모델이 골랐습니다. 그래프에는 횟수를 세거나 막는 코드가 없습니다. Ch 14 06절은 다시 검색의 상한을 코드로 정했다는 점이 다릅니다. 틀렸다면 노트북 6절과 8절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langchain/retrieval">LangChain Retrieval</a></div>확인 2026-09-25 · 검색을 늘 먼저 하는 흐름과 에이전트가 검색 시점을 고르는 흐름을 나눠 설명합니다.</li><li>langchain 1.4.0 소스 <code>langchain/agents/factory.py</code> 840~858행 — 함수 <code>create_agent</code>의 인자 목록이고, 모델 요청 수 한도 인자는 없습니다.</li><li>langchain-openai 1.6.0 소스 <code>langchain_openai/embeddings/base.py</code> 260행 — 한 요청에 담는 글 수의 기본값 1000입니다.</li><li>같은 소스 577~620행은 글 목록을 요청 단위로 묶는 자리입니다.</li><li>같은 소스 796~807행은 질문 한 줄을 벡터로 바꾸는 <code>embed_query</code>입니다.</li><li>Ch 14 06절에서 검색 함수 <code>search_hits</code>와 다시 검색의 상한을, Ch 12 01절에서 코사인 거리를 보았습니다.</li><li>Ch 19 01·05절에서 도구 명세와 도구 호출 요청을 도구에 넘기는 법을 보았습니다.</li><li>01절에서 함수 <code>create_agent</code>와 <code>agent_row</code>를, 02절에서 함수 <code>print_branches</code>를 보았습니다.</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# retriever를 도구로 전환

**이 노트북에서 할 일**

1. Ch 14 06절 검색 함수 `search_hits`로 질문 하나를 검색해, 거리 순위를 먼저 봅니다.
2. 그 검색 함수를 `@tool` 도구로 감싸 `create_agent`에 넘기고, 모델이 채운 검색어와 도구 메시지를 봅니다.
3. 질문 하나만 문서에 답이 없는 질문으로 바꿔, 모델이 다시 검색하는지 셉니다.

**준비물** — 프로젝트 폴더의 `.env` 파일에 `OPENAI_API_KEY`가 있어야 합니다.
모델은 `gpt-5.4-mini`이고, 교재 출력에서 모델 요청은 모두 5번입니다.
7절에서 2번, 8절에서 3번을 보냈습니다.
임베딩 모델은 `text-embedding-3-small`이고, 임베딩 요청은 모두 6번입니다.

모델이 검색 도구를 부르는 횟수가 달라지면, 모델 요청 수와 임베딩 요청 수가 함께 달라집니다.
요금표로 어림한 예상 비용은 모두 합쳐 0.01달러 아래이고, 청구 금액이 아닙니다.
읽는 파일은 Ch 14 실습 폴더의 `documents.json`과 `queries.json` 둘이고, 읽기만 합니다.
문서 벡터는 이 노트북에서 한 번 만들고, 파일로 쓰지 않습니다.

앞에서 배운 함수 일곱은 도구 파일 `runner_tools.py`에서 가져옵니다.
교재 출력을 만든 실행에서는 노트북 전체가 10초 안에 끝났습니다.
모델과 임베딩 응답을 기다리는 시간은 네트워크와 실행 때에 따라 달라집니다.

**기준 버전** — 첫 셀에서 패키지 여섯을 설치합니다.
판은 langchain 1.4.0, langchain-core 1.6.2, langchain-openai 1.6.0입니다.
langgraph 1.2.11, numpy 2.5.3, python-dotenv 1.2.3도 함께 설치합니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 이번에 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 3~6절을 읽습니다.
문서와 검색 함수를 준비하고, 검색 함수를 도구로 감싸 에이전트 그래프에 넣는 자리입니다.
7~9절은 질문을 보내고 질문 하나를 바꿔 보는 자리이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch21-create-agent`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 한 줄로 이어지는 그림으로 맨 위 초록 상자 Ch 14 문서 열두 건 documents.json 읽기만에서 보라 상자 임베딩 모델 text-embedding-3-small 벡터 크기 256 문서 벡터 열두 개 임베딩 요청 한 번으로 화살표가 갑니다. 이어서 파란 상자 검색 함수 search_hits Ch 14 06절 도구 파일, 파란 상자 검색 도구 search_documents 인자 query 문서 세 건의 글, 회색 상자 create_agent 모델 객체 도구 하나 시스템 메시지 글이 차례로 이어지고, 맨 아래 회색 상자 에이전트 그래프 모델 노드와 도구 실행 노드 01절과 같은 모양으로 끝나는 그림](attachment:05-1-검색-함수를-도구로-감싼-자리.png)

위에서 아래로 읽습니다.
초록 상자는 Ch 14 문서 파일이고, 보라 상자는 실제로 부른 임베딩 모델입니다.
파란 상자 둘은 우리가 적은 코드로, 검색 함수를 도구로 감싸는 차례입니다.
회색 상자 둘은 라이브러리가 준 함수 create_agent와, 그 함수가 만든 그래프입니다.
노트북 6절 출력으로 01절과 같은 모양임을 확인했습니다.

### [2] markdown {}

## 1. 준비

01~04절의 에이전트 그래프는 노트북 안 규정 딕셔너리를 찾는 도구를 썼습니다.
이 절에서는 Ch 14에서 쓴 문서 열두 건과 검색 함수를 가져와, 그 검색을 도구로 바꿉니다.
제목의 retriever는 질문을 받아 가까운 문서를 찾아 주는 검색 부분을 가리키는 영어 말입니다.
이 노트북에서는 Ch 14 06절 검색 함수 `search_hits`가 그 일을 합니다.

첫 셀은 패키지 여섯 개를 설치하고 설치된 판 번호를 출력합니다.
01~04절처럼 numpy도 함께 설치합니다.
이 절부터는 도구 파일의 거리 계산 함수가 NumPy로 벡터를 계산합니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:12.471699Z', 'iopub.status.busy': '2026-09-25T04:32:12.471531Z', 'iopub.status.idle': '2026-09-25T04:32:13.210755Z', 'shell.execute_reply': '2026-09-25T04:32:13.210268Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "langchain==1.4.0" "langchain-core==1.6.2" "langchain-openai==1.6.0" "langgraph==1.2.11" "numpy==2.5.3" "python-dotenv==1.2.3"
from importlib.metadata import version

print("langchain:", version("langchain"))
print("langchain-core:", version("langchain-core"))
print("langchain-openai:", version("langchain-openai"))
print("langgraph:", version("langgraph"))
print("numpy:", version("numpy"))
print("python-dotenv:", version("python-dotenv"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
langchain: 1.4.0
langchain-core: 1.6.2
langchain-openai: 1.6.0
langgraph: 1.2.11
numpy: 2.5.3
python-dotenv: 1.2.3

```

### [4] markdown {}

**결과 읽기** — 출력 줄 `langchain: 1.4.0`·`langchain-core: 1.6.2`·`langchain-openai: 1.6.0`이 보입니다.
출력 줄 `langgraph: 1.2.11`·`numpy: 2.5.3`·`python-dotenv: 1.2.3`도 잠금과 같은 판입니다.
이 노트북의 출력은 2026-09-25에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
임베딩 모델 `OpenAIEmbeddings`는 Ch 9 01절에서 처음 썼습니다.
함수 `convert_to_openai_tool`은 Ch 19 01절에서 도구 명세를 볼 때 썼습니다.
모듈 `json`과 `os`는 Ch 14에서 문서 파일을 읽고 폴더를 찾을 때 썼습니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:13.211876Z', 'iopub.status.busy': '2026-09-25T04:32:13.211777Z', 'iopub.status.idle': '2026-09-25T04:32:14.476824Z', 'shell.execute_reply': '2026-09-25T04:32:14.476633Z'}, 'lesson_role': 'setup'}

```python
# 문서 파일을 읽을 이름, 임베딩 모델, 에이전트와 도구를 만드는 이름을 가져옵니다
import json
import os

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langchain.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_openai import OpenAIEmbeddings

# 앞에서 배운 함수는 도구 파일에서 가져옵니다(search_hits·print_ranked는 이 절부터 가져옵니다)
from runner_tools import agent_row, estimate_cost, print_branches, print_ranked
from runner_tools import search_hits, show_messages, sum_usage

print("이 챕터에서 처음 가져온 이름:", "OpenAIEmbeddings", "search_hits", "print_ranked")
```

출력:
```
이 챕터에서 처음 가져온 이름: OpenAIEmbeddings search_hits print_ranked

```

### [6] markdown {}

**결과 읽기** — 출력 줄 `이 챕터에서 처음 가져온 이름: OpenAIEmbeddings search_hits print_ranked`가 보입니다.
Ch 9~14에서 쓴 이름이지만, 이 챕터에서는 처음 가져옵니다.

앞에서 배운 함수는 `runner_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다. 커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다.

함수 `search_hits`는 Ch 14 06절, `print_ranked`는 Ch 12 05절에서 배웠습니다.
함수 `search_hits`가 안에서 부르는 `rank_by_distance`·`cosine_distance`·`cosine_similarity`도 함께 옮겼습니다.
다섯 함수 모두 Ch 14 도구 파일에서 본문을 글자 그대로 옮겼고, 인자 모양도 Ch 14와 같습니다.
거리 계산은 Ch 5 02절처럼 NumPy로 합니다.
나머지 다섯 이름은 01~03절에서 이 도구 파일로 옮긴 함수입니다.

## 2. 키와 모델 준비

모델은 01절과 같은 `gpt-5.4-mini`이고, 과정의 같은 설정으로 부릅니다.
이렇게 만든 모델 객체를 이 절의 에이전트 그래프에 넘깁니다.

### [7] markdown {}

API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다.

### [8] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:14.480970Z', 'iopub.status.busy': '2026-09-25T04:32:14.480877Z', 'iopub.status.idle': '2026-09-25T04:32:14.485135Z', 'shell.execute_reply': '2026-09-25T04:32:14.484976Z'}, 'lesson_role': 'setup'}

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
temperature 값을 0으로 두어도, 모델이 쓰는 답 글과 검색어가 매번 같다고 보장하지는 않습니다.

### [10] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:14.485543Z', 'iopub.status.busy': '2026-09-25T04:32:14.485458Z', 'iopub.status.idle': '2026-09-25T04:32:14.851762Z', 'shell.execute_reply': '2026-09-25T04:32:14.851367Z'}}

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
이 노트북의 출력은 2026-09-25에 이 모델로 실행한 결과입니다.

### [12] markdown {}

## 3. Ch 14 문서와 질문

05절부터는 Ch 14 실습 폴더의 문서 모음을 씁니다.
Ch 14에서 검색에 쓴 문서 열두 건과 질문 여덟 건입니다.
두 파일이 Ch 14 폴더에 있으므로, 다음 셀은 먼저 프로젝트 맨 위 폴더를 찾습니다.
다음 셀은 Ch 14 06절 셀과 글자까지 같은 코드입니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:14.852481Z', 'iopub.status.busy': '2026-09-25T04:32:14.852423Z', 'iopub.status.idle': '2026-09-25T04:32:14.854506Z', 'shell.execute_reply': '2026-09-25T04:32:14.854249Z'}, 'lesson_role': 'setup'}

```python
# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part4/ch14-rag-patterns/data"):
        root_path = candidate
        break
print("고른 자리:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."
```

출력:
```
고른 자리: .

```

### [14] markdown {}

**결과 읽기** — 출력 줄 `고른 자리: .`은 교재 출력을 프로젝트 맨 위에서 실행했다는 뜻입니다.
교재 출력은 실행 도구에 도구 파일 폴더를 따로 알려 준 실행이라 `.`이 찍혔습니다.
노트북을 `notebooks/` 폴더에서 열면 이 줄에 `../../../..`가 찍힙니다.

다음 셀은 두 파일을 읽습니다.
코드 줄은 Ch 14 06절과 같고, 첫 줄 주석만 이 절에 맞게 고쳤습니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:14.855011Z', 'iopub.status.busy': '2026-09-25T04:32:14.854960Z', 'iopub.status.idle': '2026-09-25T04:32:14.857467Z', 'shell.execute_reply': '2026-09-25T04:32:14.857141Z'}}

```python
# Ch 14 폴더의 문서 파일과 질문 파일을 읽습니다(읽기만 하고 고치지 않습니다)
data_path = root_path + "/labs/part4/ch14-rag-patterns/data"
with open(data_path + "/documents.json", encoding="utf-8") as file:
    docs = json.loads(file.read())
with open(data_path + "/queries.json", encoding="utf-8") as file:
    queries = json.loads(file.read())
print("문서 수:", len(docs))
print("질문 수:", len(queries))
```

출력:
```
문서 수: 12
질문 수: 8

```

### [16] markdown {}

**결과 읽기** — 출력 줄 `문서 수: 12`와 `질문 수: 8`로, Ch 14와 같은 자료입니다.
두 파일은 Ch 14 실습 폴더의 파일이라, 이 노트북은 읽기만 합니다.

다음 셀은 Ch 14처럼 문서마다 제목과 본문을 빈칸 하나로 이어 붙입니다.
문서 ID로 그 글을 찾는 딕셔너리 `text_by_doc`도 함께 만듭니다.
5절 검색 도구가 찾은 문서의 글을 이 딕셔너리에서 꺼냅니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:14.858008Z', 'iopub.status.busy': '2026-09-25T04:32:14.857962Z', 'iopub.status.idle': '2026-09-25T04:32:14.859727Z', 'shell.execute_reply': '2026-09-25T04:32:14.859488Z'}}

```python
# 문서 12건의 제목과 본문을 이어 붙이고, 문서 ID 목록과 문서 ID로 글을 찾는 딕셔너리를 만듭니다
doc_texts = []
doc_ids = []
text_by_doc = {}
for doc in docs:
    # Ch 12·14와 같은 「제목 + 빈칸 + 본문」 모양입니다
    doc_text = doc["title"] + " " + doc["text"]
    doc_texts.append(doc_text)
    doc_ids.append(doc["doc_id"])
    text_by_doc[doc["doc_id"]] = doc_text
print("문서 ID 목록:")
print(doc_ids)
```

출력:
```
문서 ID 목록:
['LIB-001', 'LIB-002', 'LIB-003', 'LIB-004', 'FAC-001', 'FAC-002', 'FAC-003', 'FAC-004', 'ACC-001', 'ACC-002', 'ACC-003', 'ACC-004']

```

### [18] markdown {}

**결과 읽기** — 라벨 줄 `문서 ID 목록:` 아래에 `LIB-001`부터 `ACC-004`까지 열두 개가 보입니다.
Ch 14 06절 출력과 같은 차례입니다.

다음 셀은 질문 파일에서 `C05` 질문을 고릅니다.
질문마다 적힌 정답 문서 ID(Ch 11 01절 말)도 함께 꺼내, 그 문서의 글을 봅니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:14.860263Z', 'iopub.status.busy': '2026-09-25T04:32:14.860216Z', 'iopub.status.idle': '2026-09-25T04:32:14.861832Z', 'shell.execute_reply': '2026-09-25T04:32:14.861589Z'}}

```python
# 질문 파일에서 C05 질문과 그 정답 문서 ID를 고르고, 정답 문서의 글을 봅니다
c05_question = ""
gold_doc_id = ""
for query in queries:
    if query["qid"] == "C05":
        c05_question = query["question"]
        gold_doc_id = query["gold_doc_id"]
print("질문:", c05_question)
print("정답 문서 ID:", gold_doc_id)
print("정답 문서의 글:", text_by_doc[gold_doc_id])
```

출력:
```
질문: 토요일 자료실 폐관 시각은?
정답 문서 ID: FAC-003
정답 문서의 글: 운영 시간 평일 자료실은 오전 9시부터 오후 9시까지 운영합니다. 토요일은 오후 5시에 문을 닫습니다.

```

### [20] markdown {}

**결과 읽기** — 출력 줄 `질문: 토요일 자료실 폐관 시각은?`과 `정답 문서 ID: FAC-003`입니다.
출력 줄 `정답 문서의 글:` 뒤에 운영 시간 문서의 글이 보입니다.
이 문서는 평일 자료실을 오전 9시부터 오후 9시까지 연다고 적습니다.

01절 규정 딕셔너리는 평일 운영을 09:00~20:00으로 적었습니다.
두 글은 서로 다른 자료라, 이 절은 01절 딕셔너리를 쓰지 않고 고치지도 않습니다.
토요일에 닫는 시각은 두 자료 모두 오후 5시(17:00)입니다.

## 4. 문서 벡터와 검색 함수

다음 셀은 Ch 14 06절과 같은 임베딩 모델과 벡터 크기로 문서 열두 건을 벡터로 바꿉니다.
벡터 크기 인자 `dimensions`는 Ch 10 07절에서 배웠습니다.
메서드 `embed_documents`는 글 목록을 받아 벡터 목록을 내놓고, 이 셀의 임베딩 요청은 1번입니다.
Ch 14 폴더에는 저장해 둔 문서 벡터 파일이 없어, 이 노트북에서 만들고 파일로 쓰지 않습니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:14.862320Z', 'iopub.status.busy': '2026-09-25T04:32:14.862277Z', 'iopub.status.idle': '2026-09-25T04:32:15.531392Z', 'shell.execute_reply': '2026-09-25T04:32:15.530461Z'}}

```python
# Ch 14 06절과 같은 임베딩 모델과 벡터 크기로 문서 12건을 벡터로 바꿉니다(임베딩 요청 1번)
embedding_model_name = "text-embedding-3-small"
vector_dimensions = 256
embedding_model = OpenAIEmbeddings(model=embedding_model_name, dimensions=vector_dimensions)
doc_vectors = embedding_model.embed_documents(doc_texts)
print("임베딩 모델 이름:", embedding_model.model)
print("벡터의 숫자 개수 설정:", embedding_model.dimensions)
print("문서 벡터 수:", len(doc_vectors))
```

출력:
```
임베딩 모델 이름: text-embedding-3-small
벡터의 숫자 개수 설정: 256
문서 벡터 수: 12

```

### [22] markdown {}

**결과 읽기** — 출력 줄 `임베딩 모델 이름: text-embedding-3-small`과 `벡터의 숫자 개수 설정: 256`입니다.
출력 줄 `문서 벡터 수: 12`로, 문서마다 벡터가 하나씩 생겼습니다.
설정 둘은 Ch 14 06절 출력과 같습니다.

다음 셀은 Ch 14 06절처럼 질문 글을 그대로 검색 함수에 넣습니다.
함수 `search_hits`는 질문 글을 벡터로 바꾸고, 거리가 작은 차례로 문서 `top_count`건을 내놓습니다.
부를 때마다 임베딩 요청이 1번 나갑니다.
자를 개수 `top_count`는 Ch 14에서 나란히 볼 때 쓴 3으로 둡니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:15.533428Z', 'iopub.status.busy': '2026-09-25T04:32:15.533273Z', 'iopub.status.idle': '2026-09-25T04:32:15.685986Z', 'shell.execute_reply': '2026-09-25T04:32:15.685095Z'}}

```python
# Ch 14처럼 질문 글을 그대로 검색 함수에 넣어, 거리가 가까운 문서 세 건을 봅니다(임베딩 요청 1번)
top_count = 3
question_hits = search_hits(embedding_model, c05_question, doc_vectors, doc_ids, top_count)
print("질문 글을 그대로 검색한 순위:")
print_ranked(question_hits, "거리")
```

출력:
```
질문 글을 그대로 검색한 순위:
순위 | 문서 ID | 거리
1 | FAC-003 | 0.6
2 | LIB-002 | 0.67
3 | FAC-004 | 0.72

```

### [24] markdown {}

**결과 읽기** — 라벨 줄 `질문 글을 그대로 검색한 순위:` 아래 표의 첫 줄이 `1 | FAC-003 | 0.6`입니다.
정답 문서 `FAC-003`이 첫 자리에 왔고, 둘째 자리는 `LIB-002`입니다.
거리는 작을수록 가깝고, Ch 12 01절처럼 소수 둘째 자리까지 남긴 값입니다.

임베딩 값은 요청마다 아주 조금 달라질 수 있어, 거리의 끝자리가 바뀔 수 있습니다.
이번 실행에서는 셋째 자리가 `FAC-004`, 거리는 `0.72`였습니다.

## 5. 검색 함수를 도구로 감싸기

검색 함수를 도구로 감싸면, 모델이 도구 호출 요청으로 검색을 부를 수 있습니다.
도구의 매개변수 `query`에는 모델이 적은 검색어가 들어옵니다.
도구 몸통은 그 검색어로 `search_hits`를 부르고, 찾은 문서마다 문서 ID와 글을 한 줄씩 잇습니다.
이어 붙인 글이 도구 메시지가 되어, 다음 모델 요청에 실립니다.

도구 안에서 쓰는 `doc_vectors`·`doc_ids`·`text_by_doc`는 이 노트북에서 만든 이름입니다.
01절 도구가 딕셔너리 `POLICIES`를 읽은 것과 같은 모양입니다.
도구 메시지에는 거리를 넣지 않고, 문서 ID와 글만 적습니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:15.687897Z', 'iopub.status.busy': '2026-09-25T04:32:15.687732Z', 'iopub.status.idle': '2026-09-25T04:32:15.694234Z', 'shell.execute_reply': '2026-09-25T04:32:15.693480Z'}}

```python
# 검색 함수 search_hits를 도구로 감쌉니다(맨 @tool 줄 — Ch 19 01절, 부를 때마다 임베딩 요청 1번)
@tool
def search_documents(query: str):
    """교육센터 자료실 안내 문서 열두 건에서 검색어와 가까운 문서 세 건을 찾습니다. query에는 찾을 내용을 짧은 검색어로 넣습니다."""
    hit_list = search_hits(embedding_model, query, doc_vectors, doc_ids, top_count)
    # 문서마다 [문서 ID]와 글을 한 줄로 이어, 도구 메시지가 될 글을 만듭니다(Ch 14 01절 자료 줄과 같은 모양)
    found_text = ""
    for hit in hit_list:
        doc_id = hit["doc_id"]
        found_text = found_text + "[" + doc_id + "] " + text_by_doc[doc_id] + "\n"
    return found_text
```

출력:
```

```

### [26] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
도구 이름은 함수 이름 `search_documents`이고, 모델이 읽는 설명 글은 독스트링입니다.
이 도구를 부를 때마다 몸통의 `search_hits`가 임베딩 요청을 1번 보냅니다.

다음 셀은 Ch 19 01절처럼 도구 이름과 입력 형식, 도구 명세의 인자를 봅니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:15.695712Z', 'iopub.status.busy': '2026-09-25T04:32:15.695578Z', 'iopub.status.idle': '2026-09-25T04:32:15.702314Z', 'shell.execute_reply': '2026-09-25T04:32:15.701756Z'}}

```python
# 도구 이름, 모델이 채울 인자(입력 형식), 모델 요청에 실릴 도구 명세의 인자를 봅니다(Ch 19 01절)
arg_names = list(search_documents.args.keys())
tool_spec = convert_to_openai_tool(search_documents)
spec_args = tool_spec["function"]["parameters"]["properties"]
spec_names = list(spec_args.keys())
print("도구 이름:", search_documents.name)
print("입력 형식의 인자:", arg_names)
print("명세의 인자:", spec_names)
```

출력:
```
도구 이름: search_documents
입력 형식의 인자: ['query']
명세의 인자: ['query']

```

### [28] markdown {}

**결과 읽기** — 출력 줄 `도구 이름: search_documents`와 `입력 형식의 인자: ['query']`입니다.
출력 줄 `명세의 인자: ['query']`로, 모델에게 보이는 인자는 `query` 하나입니다.
모델이 채울 값은 검색어뿐이고, 문서 벡터와 자를 개수는 노트북이 정해 둔 값입니다.

## 6. 검색 도구를 넣은 에이전트 그래프

시스템 메시지 글의 첫 문장은 01절 4절 글과 같습니다.
둘째 문장은 도구 이름과 근거를 이 절 도구에 맞게 고쳤습니다.
셋째 문장은 찾은 문서에 답이 없을 때 검색어를 바꿔 한 번만 더 검색하라는 규칙입니다.
이 규칙은 모델에게 적은 글이고, 검색 횟수를 세거나 막는 코드는 없습니다.

다음 셀은 01절처럼 모델 객체·도구 목록·시스템 메시지 글을 넘겨 에이전트 그래프를 만듭니다.

### [29] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:15.703311Z', 'iopub.status.busy': '2026-09-25T04:32:15.703213Z', 'iopub.status.idle': '2026-09-25T04:32:15.710976Z', 'shell.execute_reply': '2026-09-25T04:32:15.710471Z'}}

```python
# 모델 객체·검색 도구·시스템 메시지 글을 넘겨 에이전트 그래프를 만듭니다(요청은 아직 보내지 않음)
system_text = "교육센터 자료실 안내 도우미입니다. 자료실 이용을 묻는 질문에는 search_documents 도구로 찾은 문서 글에 근거해 답하세요. 찾은 문서에 답이 없으면 검색어를 바꿔 한 번만 더 검색하고, 그래도 없으면 문서에서 찾지 못했다고 답하세요."
agent = create_agent(model, tools=[search_documents], system_prompt=system_text)
print("만든 것의 종류:", type(agent).__name__)
```

출력:
```
만든 것의 종류: CompiledStateGraph

```

### [30] markdown {}

**결과 읽기** — 출력 줄 `만든 것의 종류: CompiledStateGraph`로, 01절과 같은 종류의 그래프입니다.
이 줄에서는 모델 요청도 임베딩 요청도 나가지 않습니다.

다음 셀은 02절 함수 `print_branches`로 노드와 조건 함수를 봅니다.

### [31] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:15.712029Z', 'iopub.status.busy': '2026-09-25T04:32:15.711938Z', 'iopub.status.idle': '2026-09-25T04:32:15.713958Z', 'shell.execute_reply': '2026-09-25T04:32:15.713462Z'}}

```python
# 검색 도구를 넣은 에이전트 그래프의 노드와 조건 함수를 봅니다(02절 함수 print_branches — 도구 파일)
print("등록된 노드:", list(agent.builder.nodes))
print_branches(agent)
```

출력:
```
등록된 노드: ['model', 'tools']
tools | 조건 함수: tools_to_model | 갈 수 있는 곳: ['model']
model | 조건 함수: model_to_tools | 갈 수 있는 곳: ['tools', '__end__']

```

### [32] markdown {}

**결과 읽기** — 출력 줄 `등록된 노드: ['model', 'tools']`는 01절과 같습니다.
출력 줄 `tools | 조건 함수: tools_to_model | 갈 수 있는 곳: ['model']`도 01절과 같습니다.
출력 줄 `model | 조건 함수: model_to_tools | 갈 수 있는 곳: ['tools', '__end__']`도 01절과 같습니다.
도구를 검색 도구로 바꿔도 에이전트 그래프의 모양은 바뀌지 않았습니다.

## 7. C05 질문 보내기

실행 전에 예상해 봅니다.
모델이 검색 도구를 한 번 부르고, 도구 메시지 첫 줄에 정답 문서 `FAC-003`이 올 것입니다.
그러면 모델 요청은 2번, 도구 안 임베딩 요청은 1번입니다.
메시지 칸에는 메시지 넷이 남을 것입니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:15.714942Z', 'iopub.status.busy': '2026-09-25T04:32:15.714848Z', 'iopub.status.idle': '2026-09-25T04:32:18.379484Z', 'shell.execute_reply': '2026-09-25T04:32:18.378482Z'}}

```python
# C05 질문을 에이전트 그래프에 보냅니다(모델 노드마다 모델 요청 1번, 검색 도구마다 임베딩 요청 1번)
c05_state = {"messages": [HumanMessage(content=c05_question)]}
c05_result = agent.invoke(c05_state)
print("메시지 칸의 메시지 수:", len(c05_result["messages"]))
print("메시지 칸:")
show_messages(c05_result["messages"])
```

출력:
```
메시지 칸의 메시지 수: 4
메시지 칸:
HumanMessage
AIMessage | 도구 호출 요청: ['search_documents']
ToolMessage | 결과 상태: success | 내용: [FAC-003] 운영 시간 평일 자료실은 오전 9시부터 오후 9시까지 운영합니다. 토요일은 오후 5시에 문을 닫습니다.
[LIB-002] 연체와 대출 제한 반납 예정일을 넘기면 연체한 날짜만큼 새 대출이 제한됩니다. 연체료는 부과하지 않습니다.
[ACC-004] 졸업생 회원 졸업생은 동문 회원으로 전환한 뒤 자료실을 이용할 수 있습니다. 대출 권수는 두 권입니다.

AIMessage | 도구 호출 요청: []

```

### [34] markdown {}

**결과 읽기** — 출력 줄 `메시지 칸의 메시지 수: 4`입니다.
라벨 줄 `메시지 칸:` 아래 둘째 줄 `AIMessage | 도구 호출 요청: ['search_documents']`에서 검색 도구를 불렀습니다.
셋째 줄 도구 메시지의 내용은 문서 세 줄이고, 첫 줄이 `[FAC-003]`으로 시작합니다.
마지막 줄 `AIMessage | 도구 호출 요청: []`에서 요청이 없어 흐름이 끝났습니다.

다음 셀은 첫 응답에서 모델이 도구 호출 요청에 채운 인자를 봅니다.

### [35] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:18.381380Z', 'iopub.status.busy': '2026-09-25T04:32:18.381217Z', 'iopub.status.idle': '2026-09-25T04:32:18.384548Z', 'shell.execute_reply': '2026-09-25T04:32:18.383954Z'}}

```python
# 둘째 메시지(첫 응답)에 담긴 검색 도구 호출 요청의 이름과, 모델이 채운 인자(검색어)를 봅니다
c05_first = c05_result["messages"][1]
for call in c05_first.tool_calls:
    print("도구 이름:", call["name"], "| 인자:", call["args"])
```

출력:
```
도구 이름: search_documents | 인자: {'query': '토요일 자료실 폐관 시각'}

```

### [36] markdown {}

**결과 읽기** — 출력 줄은 `도구 이름: search_documents | 인자:`로 시작합니다.
인자 딕셔너리의 키는 `query` 하나입니다.
Ch 14 06절에서는 코드가 질문 글을 그대로 검색에 넣었습니다.
이 흐름에서는 검색에 넣을 글을 모델이 인자로 적습니다.

검색어는 모델이 쓴 글이라 실행마다 달라질 수 있습니다.
이번 실행에서는 `{'query': '토요일 자료실 폐관 시각'}`으로, 질문 글 끝의 「은?」만 뺀 글이었습니다.
그래서 도구 메시지 셋째 줄이 4절 순위의 셋째 자리와 달랐습니다.

같은 검색어로 검색하면 같은 문서가 나오는지 봅니다.
다음 셀은 첫 응답의 도구 호출 요청을 Ch 19 05절처럼 도구에 그대로 다시 보냅니다.
도구 호출 요청을 통째로 넘기면 도구 메시지가 나오고, 임베딩 요청이 1번 더 나갑니다.

### [37] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:18.385806Z', 'iopub.status.busy': '2026-09-25T04:32:18.385685Z', 'iopub.status.idle': '2026-09-25T04:32:18.543129Z', 'shell.execute_reply': '2026-09-25T04:32:18.542316Z'}}

```python
# 첫 응답의 도구 호출 요청을 도구에 그대로 다시 보내, 같은 검색어면 같은 글이 나오는지 봅니다(임베딩 요청 1번)
first_call = c05_first.tool_calls[0]
again_message = search_documents.invoke(first_call)
c05_tool_message = c05_result["messages"][2]
print("다시 받은 메시지의 종류:", type(again_message).__name__)
print("도구 메시지 글과 같은가:", again_message.content == c05_tool_message.content)
```

출력:
```
다시 받은 메시지의 종류: ToolMessage
도구 메시지 글과 같은가: True

```

### [38] markdown {}

**결과 읽기** — 출력 줄 `다시 받은 메시지의 종류: ToolMessage`입니다.
출력 줄 `도구 메시지 글과 같은가: True`로, 같은 검색어가 같은 문서 셋을 같은 차례로 내놓았습니다.
검색어가 같으면 거리 순위는 검색 함수의 계산으로 정해집니다.

이 비교에는 `assert`를 걸지 않았습니다.
임베딩 값이 요청마다 아주 조금 달라질 수 있어, 거리가 거의 같은 두 문서는 차례가 바뀔 수 있기 때문입니다.

다음 셀은 메시지 칸의 마지막 응답을 봅니다.

### [39] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:18.544633Z', 'iopub.status.busy': '2026-09-25T04:32:18.544494Z', 'iopub.status.idle': '2026-09-25T04:32:18.547615Z', 'shell.execute_reply': '2026-09-25T04:32:18.547038Z'}}

```python
# 메시지 칸의 마지막 응답을 봅니다(도구 호출 요청 수와 답 글)
c05_last = c05_result["messages"][-1]
print("마지막 응답의 도구 호출 요청 수:", len(c05_last.tool_calls))
print("답 글:")
print(c05_last.content)
```

출력:
```
마지막 응답의 도구 호출 요청 수: 0
답 글:
토요일 자료실은 **오후 5시**에 폐관합니다.

```

### [40] markdown {}

**결과 읽기** — 출력 줄 `마지막 응답의 도구 호출 요청 수: 0`입니다.
라벨 줄 `답 글:` 아래가 모델이 도구 메시지를 보고 쓴 답입니다.

답 글은 모델이 쓴 글이라 실행마다 글자가 달라질 수 있습니다.
이번 실행에서는 토요일 폐관 시각을 오후 5시로 답했고, 문서 `FAC-003`의 글과 같은 시각입니다.

## 8. 값 바꿔 보기 · 문서에 없는 질문

바꿀 값은 질문 하나이고, 에이전트 그래프와 시스템 메시지 글은 그대로 둡니다.
문서 열두 건에 주차 이야기가 없는 질문으로 바꿉니다.
실행 전에 예상해 봅니다.
검색 도구는 관련 문서가 없어도 거리가 가까운 문서 세 건을 내놓을 것입니다.
모델이 규칙대로 한 번 더 검색하면, 모델 요청은 3번이고 도구 메시지는 둘일 것입니다.

### [41] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:18.548876Z', 'iopub.status.busy': '2026-09-25T04:32:18.548756Z', 'iopub.status.idle': '2026-09-25T04:32:21.333247Z', 'shell.execute_reply': '2026-09-25T04:32:21.332299Z'}}

```python
# 바꿀 값: 질문 하나만, 문서 12건에 답이 없는 질문으로 바꿔 같은 에이전트 그래프에 보냅니다
parking_question = "자료실 주차 요금은 얼마인가요?"
parking_state = {"messages": [HumanMessage(content=parking_question)]}
parking_result = agent.invoke(parking_state)
print("메시지 칸의 메시지 수:", len(parking_result["messages"]))
print("메시지 칸:")
show_messages(parking_result["messages"])
```

출력:
```
메시지 칸의 메시지 수: 6
메시지 칸:
HumanMessage
AIMessage | 도구 호출 요청: ['search_documents']
ToolMessage | 결과 상태: success | 내용: [FAC-002] 프린터 이용 흑백 인쇄는 장당 50원이고 컬러 인쇄는 장당 300원입니다. 결제는 학생증 잔액을 사용합니다.
[ACC-004] 졸업생 회원 졸업생은 동문 회원으로 전환한 뒤 자료실을 이용할 수 있습니다. 대출 권수는 두 권입니다.
[ACC-001] 비밀번호 재설정 비밀번호를 잊으면 등록한 이메일로 재설정 링크를 받습니다. 링크는 30분 동안 유효합니다.

AIMessage | 도구 호출 요청: ['search_documents']
ToolMessage | 결과 상태: success | 내용: [FAC-004] 분실물 보관 분실물은 안내 데스크에서 30일 동안 보관합니다. 신분증으로 본인 확인 후 수령합니다.
[ACC-004] 졸업생 회원 졸업생은 동문 회원으로 전환한 뒤 자료실을 이용할 수 있습니다. 대출 권수는 두 권입니다.
[FAC-002] 프린터 이용 흑백 인쇄는 장당 50원이고 컬러 인쇄는 장당 300원입니다. 결제는 학생증 잔액을 사용합니다.

AIMessage | 도구 호출 요청: []

```

### [42] markdown {}

**결과 읽기** — 출력 줄 `메시지 칸의 메시지 수: 6`입니다.
라벨 줄 `메시지 칸:` 아래에 `AIMessage | 도구 호출 요청: ['search_documents']`가 두 번 보입니다.
도구 메시지도 둘이고, 두 도구 메시지 모두 문서 세 줄을 담았습니다.
첫 도구 메시지의 첫 줄은 `[FAC-002]`로, 주차가 아니라 프린터 이용 요금 문서입니다.
검색 함수는 거리가 가까운 차례로 늘 `top_count`건을 내놓으므로, 관련 문서가 없어도 문서가 나옵니다.

다음 셀은 응답마다 도구 호출 요청 수와 검색어를 봅니다.

### [43] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:21.335638Z', 'iopub.status.busy': '2026-09-25T04:32:21.335434Z', 'iopub.status.idle': '2026-09-25T04:32:21.339134Z', 'shell.execute_reply': '2026-09-25T04:32:21.338514Z'}}

```python
# 응답마다 검색 도구 호출 요청 수와, 모델이 채운 인자(검색어)를 차례로 봅니다
for message in parking_result["messages"]:
    if type(message).__name__ == "AIMessage":
        print("응답 | 도구 호출 요청 수:", len(message.tool_calls))
        for call in message.tool_calls:
            print("  인자:", call["args"])
```

출력:
```
응답 | 도구 호출 요청 수: 1
  인자: {'query': '주차 요금'}
응답 | 도구 호출 요청 수: 1
  인자: {'query': '주차'}
응답 | 도구 호출 요청 수: 0

```

### [44] markdown {}

**결과 읽기** — 라벨이 `응답 | 도구 호출 요청 수:`인 줄이 셋이고, 값은 차례로 `1`·`1`·`0`입니다.
응답마다 검색 요청을 하나씩 보내, 검색을 두 응답에 걸쳐 두 번 했습니다.
시스템 메시지 글의 「한 번만 더 검색」대로, 다시 검색은 한 번이었습니다.
그래프에는 검색 횟수를 세거나 막는 줄이 없고, 세 번째 검색을 고른 실행은 이번에 없었습니다.

검색어는 실행마다 달라질 수 있습니다.
이번 실행에서는 첫 검색어가 `{'query': '주차 요금'}`, 둘째가 `{'query': '주차'}`였습니다.

다음 셀은 바꾼 질문의 마지막 응답을 봅니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:21.340609Z', 'iopub.status.busy': '2026-09-25T04:32:21.340491Z', 'iopub.status.idle': '2026-09-25T04:32:21.343323Z', 'shell.execute_reply': '2026-09-25T04:32:21.342647Z'}}

```python
# 바꾼 질문의 마지막 응답을 봅니다(도구 호출 요청 수와 답 글)
parking_last = parking_result["messages"][-1]
print("마지막 응답의 도구 호출 요청 수:", len(parking_last.tool_calls))
print("답 글:")
print(parking_last.content)
```

출력:
```
마지막 응답의 도구 호출 요청 수: 0
답 글:
자료실 주차 요금에 대한 내용은 문서에서 찾지 못했습니다.

```

### [46] markdown {}

**결과 읽기** — 출력 줄 `마지막 응답의 도구 호출 요청 수: 0`입니다.
라벨 줄 `답 글:` 아래가 모델이 도구 메시지 둘을 보고 쓴 답입니다.

답 글은 실행마다 글자가 달라질 수 있습니다.
이번 실행에서는 문서에서 주차 요금을 찾지 못했다는 뜻의 한 문장이었습니다.

## 9. 요청 수와 예상 비용

다음 셀은 두 결과의 도구 메시지마다 문서 ID를 꺼내 셉니다.
도구 몸통은 줄 머리에 대괄호로 문서 ID를 적으므로, 대괄호로 시작하는 줄이 문서 한 건입니다.
메서드 `split`으로 줄을 나누고, `]` 앞 글자에서 첫 글자를 빼면 문서 ID가 남습니다.

### [47] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:21.344629Z', 'iopub.status.busy': '2026-09-25T04:32:21.344494Z', 'iopub.status.idle': '2026-09-25T04:32:21.348114Z', 'shell.execute_reply': '2026-09-25T04:32:21.347455Z'}}

```python
# 두 결과의 도구 메시지마다, [로 시작하는 줄에서 문서 ID를 꺼내 셉니다
for result in [c05_result, parking_result]:
    for message in result["messages"]:
        if type(message).__name__ == "ToolMessage":
            found_ids = []
            for line in message.content.split("\n"):
                if line.startswith("["):
                    found_ids.append(line.split("]")[0][1:])
            print("도구 메시지의 문서 ID:", found_ids)
            # 줄 수는 도구 몸통이 top_count로 정하는 값이라, 모델이 무엇을 검색해도 같아야 합니다
            assert len(found_ids) == top_count, "도구 메시지마다 문서 줄이 top_count개여야 합니다"
```

출력:
```
도구 메시지의 문서 ID: ['FAC-003', 'LIB-002', 'ACC-004']
도구 메시지의 문서 ID: ['FAC-002', 'ACC-004', 'ACC-001']
도구 메시지의 문서 ID: ['FAC-004', 'ACC-004', 'FAC-002']

```

### [48] markdown {}

**결과 읽기** — 라벨이 `도구 메시지의 문서 ID:`인 줄이 셋입니다.
첫 줄 `['FAC-003', 'LIB-002', 'ACC-004']`는 7절, 둘째·셋째 줄은 8절의 도구 메시지입니다.
세 줄 모두 문서 ID가 셋이고, 셀의 `assert`는 이 개수에만 걸었습니다.
개수는 도구 몸통이 `top_count`로 정하는 값이라, 모델이 무엇을 검색해도 같습니다.

8절 두 도구 메시지는 이번 실행에서 `['FAC-002', 'ACC-004', 'ACC-001']`과 `['FAC-004', 'ACC-004', 'FAC-002']`였습니다.
검색어가 달라지면 이 차례도 달라질 수 있습니다.

다음 셀은 01절 10절 함수 `agent_row`로 두 질문을 한 줄씩 적습니다.

### [49] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:21.349661Z', 'iopub.status.busy': '2026-09-25T04:32:21.349546Z', 'iopub.status.idle': '2026-09-25T04:32:21.352717Z', 'shell.execute_reply': '2026-09-25T04:32:21.352230Z'}}

```python
# 두 질문의 기록을 한 줄씩 적어 출력합니다(01절 10절 함수 agent_row — 도구 파일)
run_rows = []
run_rows.append(agent_row("C05 질문", c05_result))
run_rows.append(agent_row("주차 질문", parking_result))
print("질문 | 모델 요청 수 | 도구 메시지 수 | 호출 ID 짝")
for row in run_rows:
    print(row["질문"], "|", row["모델 요청 수"], "|", row["도구 메시지 수"], "|", row["호출 ID 짝"])
    # 도구 메시지마다 요청 id를 옮겨 적는 것은 코드가 하는 일이라, 짝은 매번 맞아야 합니다
    assert row["호출 ID 짝"], "도구 메시지마다 같은 차례의 요청 id가 옮겨져야 합니다"
```

출력:
```
질문 | 모델 요청 수 | 도구 메시지 수 | 호출 ID 짝
C05 질문 | 2 | 1 | True
주차 질문 | 3 | 2 | True

```

### [50] markdown {}

**결과 읽기** — 라벨 줄 아래 두 줄이 `C05 질문 | 2 | 1 | True`와 `주차 질문 | 3 | 2 | True`입니다.
두 질문 모두 모델 요청 수가 도구 메시지 수보다 1 많았습니다.
01절에서 본 것처럼, 이 셈은 응답마다 요청을 하나씩 받을 때만 맞습니다.
호출 ID 짝은 두 질문 모두 맞았고, 셀의 `assert`로 확인했습니다.

검색 도구는 부를 때마다 임베딩 요청을 1번 보냅니다.
그래서 도구 메시지 수가 곧 도구 안 임베딩 요청 수입니다.
다음 셀은 이 노트북이 보낸 임베딩 요청을 셉니다.
검색 함수를 직접 부른 곳은 4절 질문 글 검색과 7절 다시 부르기, 두 곳입니다.

### [51] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:21.353880Z', 'iopub.status.busy': '2026-09-25T04:32:21.353788Z', 'iopub.status.idle': '2026-09-25T04:32:21.356627Z', 'shell.execute_reply': '2026-09-25T04:32:21.356020Z'}}

```python
# 이 노트북이 보낸 임베딩 요청을 셉니다(도구 메시지 하나 = 도구 안 검색 한 번 = 임베딩 요청 1번)
doc_requests = 1
direct_requests = 2
tool_requests = run_rows[0]["도구 메시지 수"] + run_rows[1]["도구 메시지 수"]
embed_total = doc_requests + direct_requests + tool_requests
print("문서 벡터를 만든 요청:", doc_requests)
print("검색 함수를 직접 부른 요청(4절·7절):", direct_requests)
print("검색 도구 안에서 보낸 요청:", tool_requests)
print("임베딩 요청 합계:", embed_total)
```

출력:
```
문서 벡터를 만든 요청: 1
검색 함수를 직접 부른 요청(4절·7절): 2
검색 도구 안에서 보낸 요청: 3
임베딩 요청 합계: 6

```

### [52] markdown {}

**결과 읽기** — 출력 줄 `검색 도구 안에서 보낸 요청: 3`과 `임베딩 요청 합계: 6`입니다.
문서 벡터를 만든 요청 1번과 직접 부른 요청 2번을 더한 값입니다.
모델이 검색을 더 고르면 도구 안 요청과 합계가 함께 늘어납니다.

다음 셀은 Ch 19 05절 함수 `sum_usage`로 두 결과의 모델 요청 수와 토큰을 더합니다.

### [53] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:21.357678Z', 'iopub.status.busy': '2026-09-25T04:32:21.357594Z', 'iopub.status.idle': '2026-09-25T04:32:21.359878Z', 'shell.execute_reply': '2026-09-25T04:32:21.359424Z'}}

```python
# 두 결과의 모델 요청 수와 입력·출력 토큰을 더합니다(Ch 19 05절 함수 sum_usage)
c05_usage = sum_usage(c05_result["messages"])
parking_usage = sum_usage(parking_result["messages"])
print("C05 질문 사용량:", c05_usage)
print("주차 질문 사용량:", parking_usage)
```

출력:
```
C05 질문 사용량: {'requests': 2, 'input_tokens': 638, 'output_tokens': 44}
주차 질문 사용량: {'requests': 3, 'input_tokens': 1189, 'output_tokens': 59}

```

### [54] markdown {}

**결과 읽기** — `C05 질문 사용량:`은 `'requests': 2`, `주차 질문 사용량:`은 `'requests': 3`입니다.
입력 토큰은 C05 질문 `'input_tokens': 638`, 주차 질문 `'input_tokens': 1189`입니다.
주차 질문은 모델 요청이 한 번 더 있어, 입력 토큰 합이 더 컸습니다.
요청마다 어느 몫이 몇 토큰인지는 나눠 세지 않았습니다.

출력 토큰은 모델이 쓴 글에 따라 실행마다 달라질 수 있습니다.
이번 실행에서는 C05 질문 `'output_tokens': 44`, 주차 질문 `'output_tokens': 59`였습니다.

다음 셀은 Ch 6 06절 함수 `estimate_cost`로 두 사용량의 예상 비용을 셉니다.
요금은 2026-09-17 요금표의 100만 토큰당 달러입니다.

### [55] code {'execution': {'iopub.execute_input': '2026-09-25T04:32:21.361047Z', 'iopub.status.busy': '2026-09-25T04:32:21.360950Z', 'iopub.status.idle': '2026-09-25T04:32:21.363674Z', 'shell.execute_reply': '2026-09-25T04:32:21.363283Z'}}

```python
# 2026-09-17 요금표(100만 토큰당 달러)로 두 결과의 모델 몫 예상 비용을 셉니다(Ch 6 06절 함수 estimate_cost)
input_rate = 0.75
cached_input_rate = 0.075
output_rate = 4.50
c05_cost = round(estimate_cost(c05_usage, input_rate, cached_input_rate, output_rate), 6)
parking_cost = round(estimate_cost(parking_usage, input_rate, cached_input_rate, output_rate), 6)
print("C05 질문 예상 비용(달러):", c05_cost)
print("주차 질문 예상 비용(달러):", parking_cost)
```

출력:
```
C05 질문 예상 비용(달러): 0.000677
주차 질문 예상 비용(달러): 0.001157

```

### [56] markdown {}

**결과 읽기** — 라벨 `C05 질문 예상 비용(달러):`와 `주차 질문 예상 비용(달러):` 뒤 값이 모델 몫의 예상 비용입니다.
요금표로 어림한 값이고, 청구 금액이 아닙니다.
임베딩 요금은 넣지 않았습니다.
이 노트북은 임베딩 요청의 토큰 수를 세지 않기 때문입니다.

출력 토큰이 실행마다 달라질 수 있어, 이 값도 달라질 수 있습니다.
이번 실행에서는 C05 질문 `0.000677`달러, 주차 질문 `0.001157`달러였습니다.

## 정리

1. Ch 14 06절 검색 함수 `search_hits`를 `@tool` 도구로 감싸자, 모델이 인자 `query`에 검색어를 적어 검색을 불렀습니다.
2. 같은 검색어로 도구를 다시 부르면 같은 문서 셋이 같은 차례로 나왔고, 도구 메시지마다 문서는 `top_count`건이었습니다.
3. 문서에 답이 없는 질문에서 모델은 검색을 두 번 했고, 「한 번만 더」는 시스템 메시지 글일 뿐 코드 제한이 아니었습니다.

06절에서는 같은 평가 질문을 두 흐름으로 보내 견줍니다.
검색을 먼저 하는 흐름과, 검색 도구를 쓰는 에이전트 흐름입니다.

## 그림

### 05-1-검색-함수를-도구로-감싼-자리.mmd

```mermaid
flowchart TB
  %% classes
  docs["Ch 14 문서 열두 건<br>documents.json · 읽기만"]:::tool
  emb["임베딩 모델 text-embedding-3-small<br>벡터 크기 256<br>문서 벡터 열두 개<br>임베딩 요청 한 번"]:::model
  hits["검색 함수 search_hits<br>Ch 14 06절 · 도구 파일"]:::flow
  wrap["검색 도구 search_documents<br>인자 query · 문서 세 건의 글"]:::flow
  mk["create_agent<br>모델 객체 · 도구 하나<br>시스템 메시지 글"]
  g["에이전트 그래프<br>모델 노드 · 도구 실행 노드<br>01절과 같은 모양"]
  docs --> emb
  emb --> hits
  hits --> wrap
  wrap --> mk
  mk --> g
```

Ch 14 문서 벡터와 검색 함수 search_hits를 도구 search_documents로 감싸 create_agent에 넘겨도, 에이전트 그래프의 모양은 01절과 같습니다.

### 05-2-검색어와-횟수를-정하는-쪽.mmd

```mermaid
flowchart TB
  %% classes
  subgraph up["Ch 14 06절 흐름 · 코드가 정함"]
    direction TB
    a1["첫 검색어<br>질문 글 그대로"]
    a2["다시 검색할지<br>첫 자리 거리를 기준값과<br>견주어 코드가 정함<br>다시 검색 상한 한 번을<br>코드로 확인"]
    a1 ~~~ a2
  end
  subgraph dn["이 절 흐름 · 모델이 고름"]
    direction TB
    b1["검색어<br>모델이 인자 query에 적음"]:::model
    b2["다시 검색<br>시스템 메시지 글<br>한 번만 더 검색<br>세거나 막는 코드 없음"]:::tool
    b3["C05 질문 · 검색 한 번<br>주차 질문 · 검색 두 번"]:::measure
    b1 ~~~ b2
    b2 ~~~ b3
  end
  up ~~~ dn
```

Ch 14 06절에서는 다시 검색할지와 그 상한을 코드가 정했고, 이 절에서는 검색어와 검색 횟수를 모델이 고릅니다.

### 05-3-C05-질문의-차례.mmd

```mermaid
%%{init: {"sequence": {"messageAlign": "left", "actorMargin": 30}}}%%
sequenceDiagram
  participant P as 노트북 코드<br>agent.invoke
  box Lavender
  participant M as 모델 노드<br>gpt-5.4-mini
  end
  participant T as 도구 실행 노드<br>search_documents
  box Lavender
  participant E as 임베딩 모델<br>text-embedding<br>-3-small
  end
  P->>M: C05 질문 하나
  Note over M: 요청 1<br>도구 호출 요청<br>search_documents<br>인자 query
  M->>T: model_to_tools
  T->>E: search_hits
  E-->>T: 임베딩 요청 1번
  Note over T: 도구 메시지<br>success · 문서 세 줄<br>FAC-003<br>LIB-002<br>ACC-004
  T->>M: tools_to_model
  Note over M: 요청 2<br>도구 호출 요청 0건
  M-->>P: END
  Note over P,M: 메시지 넷<br>모델 요청 두 번<br>임베딩 요청 한 번<br>호출 ID 짝 True
```

C05 질문에서 모델은 검색 도구를 한 번 불렀고, 도구 실행 노드의 검색 한 번에 임베딩 요청이 한 번 나갔습니다.

### 05-4-질문만-바꾼-두-실행.mmd

```mermaid
flowchart TB
  %% classes
  q["같은 에이전트 그래프<br>같은 시스템 메시지 글<br>바꾼 것은 질문 하나"]:::tool
  subgraph c5["C05 질문 · 토요일 폐관 시각"]
    direction TB
    a1["검색 한 번<br>도구 메시지 하나<br>첫 줄 FAC-003<br>모델 요청 두 번<br>입력 토큰 638"]:::measure
  end
  subgraph pk["바꾼 값 · 주차 요금 질문"]
    direction TB
    b1["검색 두 번 · 다시 검색 한 번<br>도구 메시지 둘<br>첫 줄 FAC-002 · FAC-004<br>모델 요청 세 번<br>입력 토큰 1189"]:::measure
  end
  same["두 질문 공통<br>도구 메시지마다 문서 세 건<br>응답마다 도구 호출 요청<br>한 건 이하<br>호출 ID 짝 True"]
  q --> c5
  q --> pk
  c5 ~~~ same
  pk ~~~ same
```

질문 하나만 바꾸자 검색은 한 번에서 두 번으로, 모델 요청은 두 번에서 세 번으로 늘었고, 도구 메시지마다 문서는 세 건이었습니다.

### 05-5-세제-통을-꽂아-둔-세탁기.prompt.md

# 05-5-세제-통을-꽂아-둔-세탁기 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 하나는 빨래를 넣을 때마다 사람이 세제를 한 컵씩 먼저 붓는 방법입니다. 다른 하나는 세제 통을 세탁기에 꽂아 두고, 세탁기가 필요할 때 끌어 쓰게 하는 방법입니다. … 세제 통이 검색 함수이고, 통을 꽂는 자리가 검색 도구입니다. 세탁기인 에이전트 그래프 안에서 모델이 필요할 때 검색을 부릅니다.

구성 요소와 배치: **흰 앞문형 세탁기 한 대**(01~04 그림과 같은 계열 — 둥근 버튼 하나·앞면 둥근 유리문 하나, = 에이전트 그래프) · 세탁기 **윗면 왼쪽 구멍에 거꾸로 꽂힌 세제 통 하나**(라벨·글자 없음, = 검색 도구로 감싼 검색 함수) · 유리문 안 **옅은 파란 거품**(세제가 쓰이고 있음) · 세탁기 왼쪽 **바닥의 빈 계량컵 하나**(= 사람이 매번 먼저 붓는 방법, Ch 14처럼 코드가 검색을 먼저 하는 흐름 — 쓰이지 않음). 사람·손·화살표·화면·눈금 다이얼·관·바구니·선반·서랍 없음. 01~04 소품(대야·빨래판·헹굼 통·나무 판·몸체 틈·주황 카드·셔츠 이름표·회색 상자와 관·연노랑 수건)과 앞 챕터 소품(쟁반·서랍·바구니·저울·울타리·발자국·공구판·승강 상자·식당 전표·집게·Ch 14 나무판·구멍·마개) 되풀이 금지 — 04-5의 「관으로 이어진 상자」와 겹치지 않게 관 없이 **통을 직접 꽂음**.

시선 순서: 세탁기 한 대 → 윗면에 꽂힌 세제 통(기계에 붙어 있음) → 유리문 안 거품 → 바닥의 빈 계량컵(떨어져 쓰이지 않음).

검수 기준: 그림만 보고 「세제 통은 기계에 꽂혀 있다」, 「계량컵은 비어 기계 밖 바닥에 떨어져 있다」, 「세탁기·세제 통·계량컵이 하나씩」이 읽히는가. 글자·숫자·사람이 없는가.

비유 계열: 챕터 리드 결정 11 **「세탁기(코스 버튼과 동그란 창)」**(01절이 엶) — 05는 인계 「05 후보」(세제 통에서 필요할 때만 세제가 들어가는 투입구)를 투입구 대신 **꽂아 둔 통**으로 그림(관·서랍 금지 때문).

## 프롬프트 (1차, 채택)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. A plain wall with no opening and a plain floor. In the center stands exactly one large white front-loading washing machine with exactly one round button on the top right and exactly one round glass door on the front, laundry with a little pale blue foam inside the door. Exactly one large plain light green detergent jug stands upside down on the top left of the machine, its neck clearly plugged into a round hole in the top panel. On the floor to the left of the machine stands exactly one small empty plain measuring cup. No people, no hands, no arrows, no screens, no dials, no labels on the jug, no tubes, no baskets, no shelves, no drawers.
```

## 상태

- 2026-09-25 · `nano_banana_pro`(`jobs_wait` 응답 모델 이름 `nano_banana_2` — 01~04와 같은 표시) · 16:9 · 2k · `use_unlim: false` · count 1. 생성 전 잔액 **2455.75**(바로 앞 거래 04:00:15Z 「Nano Banana Pro −2」는 04절 몫).
- **1차 job `93792124-8b54-4597-b916-7feef71a54d3` 채택**(재생성 없음). 거래 기록 **2026-09-25T04:35:43Z 「Nano Banana Pro −2」** 한 줄이 이 절 몫입니다(결과 파일 이름 `hf_20260925_043543_93792124…`와 시각이 같음). 결과 원본 `845224ee4b879b6d1a2a4ec05213e7687a6765d8f77b1757c4e31defe15c2c0c`(2752 × 1536).
- **그림에서 확인한 것(그림 읽기·alt·캡션에 반영)**: 옅은 베이지 벽과 바닥, 벽 아래 가로 띠(프롬프트 첫 문장의 흰 바탕과 달리 벽이 옅은 베이지 — 04-5와 같음, 관계와 무관해 채택). 가운데 흰 앞문형 세탁기 **한 대**. 둥근 회색 버튼 **하나**는 윗면이 아니라 **앞면 위쪽 띠의 오른쪽**(프롬프트 「top right」와 자리가 조금 다름 — 그림 읽기에는 「둥근 버튼 하나」로만 적음). 앞면 위쪽 띠의 왼쪽에 네모 칸 하나가 그려져 서랍처럼 보이기도 함(프롬프트 「no drawers」와 다름 — 관계와 무관해 채택, 코드의 무엇과도 짝짓지 않음). 앞면 **둥근 유리문 하나**, 안에 빨래와 **옅은 파란 거품**. 윗면 왼쪽 **둥근 구멍에 연녹색 세제 통 한 개**가 목을 아래로 해 기울어 꽂힘(손잡이 구멍 있음, 라벨·글자 없음). 세탁기 왼쪽 바닥에 **빈 연녹색 계량컵 한 개**(눈금 없음), 기계와 떨어져 있음. 글자·숫자·사람·손·화살표·화면·다이얼·관·바구니·선반 없음.
- 저장: 기기 셸에서 결과 URL을 `curl`로 받아(`/tmp/ch21-05/illu-1-orig.png`) `UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pillow`로 RGB·폭 1100px(LANCZOS)로 줄여 `figures/05-5-세제-통을-꽂아-둔-세탁기.png`(1100 × 614, `e80b5eee16db4d3a08487a62d97c397240eb51ca2693cc87c7b0751580eb5ba9`)로 저장했습니다.
- 받은 원본을 같은 폭으로 다시 줄인 그림과 저장 PNG를 픽셀 대조했습니다(`ImageChops.difference` bbox `None`, 최대 차이 0). 같은 크기 사본(`.cache/ch21-05-view/illu.png`)을 직접 열어 개수를 세고 그림 읽기를 썼습니다.

