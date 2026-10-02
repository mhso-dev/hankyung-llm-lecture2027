# 03-SQL로-조회-함수-만들기

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 1h | 실습 2h | 코드 Jupyter Notebook | 새 용어 9 -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2>
<div class="goal"><ul><li>SQL 문장 <code>CREATE TABLE</code>, <code>INSERT INTO</code>, <code>SELECT</code>의 뜻을 말하고, 기본 키와 외래 키 제약이 막은 행을 출력에서 확인할 수 있습니다.</li><li><code>WHERE</code>, <code>ORDER BY</code>, <code>JOIN</code>을 쓴 SQL로, 고객 번호를 받아 딕셔너리 목록을 반환하는 조회 함수를 만들 수 있습니다.</li><li>입력 글을 SQL에 이어 붙이면 결과가 달라지는 이유를 설명하고, 자리표시자로 값만 넘기도록 고칠 수 있습니다.</li></ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2>
<p>02절에서는 고객 표와 주문 표를 CSV 파일로 두고 pandas로 이었습니다. 실제 서비스에서는 이런 표를 데이터베이스에 두는 경우가 많습니다. 여러 프로그램이 같은 표를 읽고, 규칙에 어긋난 행은 넣는 순간 막을 수 있기 때문입니다.</p>
<p>에이전트가 「김하나 고객의 주문을 알려 줘」에 답하려면, 고객 번호로 데이터베이스를 조회하는 함수가 필요합니다. 이 함수에 넘기는 고객 번호는 사용자가 적은 글에서 옵니다. 그 글을 SQL 문장에 그대로 이어 붙이면, 사용자가 문장의 뜻을 바꿀 수 있습니다.</p>
<p>그래서 이 절에서는 SQL 문장을 하나씩 실행해 본 뒤 조회 함수로 묶습니다. 마지막에 입력을 이어 붙인 함수와 자리표시자를 쓴 함수에 같은 입력을 넣어 비교합니다. Ch 19에서는 이런 조회 함수를 에이전트가 부르는 도구로 씁니다.</p>
<p><strong>이 절의 질문</strong> — 입력 글이 SQL 문장의 뜻을 바꾸지 못하게 하려면, 조회 함수에 고객 번호를 어떻게 넘겨야 할까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2>
<p>02절에서는 고객 번호로 고객 표와 주문 표를 이었습니다. 메서드 <code>merge()</code>의 기본값은 내부 조인이라, 고객 표에 없는 C003의 주문이 오류 없이 빠졌습니다. C001 줄이 두 번 든 고객 표에서는 주문이 두 번 세어졌고, 인자 <code>validate="many_to_one"</code>으로 막았습니다.</p>
<p>01절에서는 마스크를 <code>loc</code>에 넣어 행을 고르고, 조회 함수 <code>fetch_orders()</code>가 딕셔너리 목록을 반환하게 했습니다. 이 절에서는 SQL의 <code>WHERE</code>가 마스크의 일을 맡습니다. 새 조회 함수도 같은 딕셔너리 목록을 반환합니다.</p>
<p>Ch 2 03절의 튜플과 풀어 담기, 04절의 함수 정의, 05절의 여러 줄 글과 <code>try/except 오류이름</code>을 그대로 씁니다. Ch 2 01절에서는 변수를 넣은 f-string으로 글을 만들었습니다. 이 절의 Before 함수가 그 f-string으로 SQL 글을 만듭니다.</p>
<p>Ch 3 01절의 커밋은 Git 저장소에 파일 상태를 기록했습니다. 이 절의 커밋은 이름만 같고, 데이터베이스에 넣은 행을 확정하는 일입니다. Ch 1 05절의 연산자 <code>or</code>는 SQL 조건의 <code>OR</code>와 뜻이 같습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2>
<h3>비유로 시작하기</h3>
<p>가게 창고에 주문 서류를 꺼내 달라는 요청서 양식이 있다고 해 봅니다. 인쇄된 줄 사이에 고객 번호를 적는 빈칸 하나가 있습니다. 직원은 인쇄된 줄대로 일하고, 빈칸 안의 글은 고객 번호 하나로 봅니다.</p>
<p>누군가 받은 쪽지를 빈칸에 붙였는데, 쪽지가 길어 빈칸 밖의 인쇄된 줄까지 덮었다고 해 봅니다. 직원은 덮인 자리의 글까지 요청으로 읽고, 서류를 모두 꺼냅니다. 같은 쪽지를 투명 봉투에 넣어 빈칸 안에만 끼우면 인쇄된 줄은 그대로입니다. 그런 번호의 서류는 없으니 꺼낸 서류도 없습니다.</p>
<p>이 장면을 SQL로 옮기면 인쇄된 줄이 SQL 문장, 빈칸이 자리표시자 <code>?</code>, 투명 봉투가 따로 넘기는 값 목록입니다. 빈칸 밖까지 덮은 쪽지는 f-string으로 SQL에 이어 붙인 입력입니다.</p>
{{img:03-5-요청서-빈칸|왼쪽에는 긴 분홍 쪽지가 요청서의 파란 빈칸에서 아래 인쇄된 줄까지 덮고 옆 쟁반에 초록 서류철 두 개와 파란 서류철 하나가 있고, 오른쪽에는 같은 쪽지를 접어 넣은 투명 봉투가 빈칸 안에만 있고 쟁반이 빈 삽화|쪽지가 빈칸 밖 줄까지 덮으면 서류를 모두 꺼냅니다. 봉투에 넣어 빈칸 안에만 두면 꺼낸 서류가 없습니다.}}
<p><strong>그림 읽기</strong> — 가운데 세로선의 왼쪽이 이어 붙인 경우, 오른쪽이 따로 넘긴 경우입니다. 두 칸에는 같은 요청서와 나무 쟁반이 있습니다. 왼쪽 요청서에서는 긴 분홍 쪽지가 파란 빈칸에서 시작해 아래 인쇄된 줄들을 비스듬히 덮었습니다. 옆 쟁반에는 초록 서류철 두 개와 파란 서류철 하나, 곧 주문 세 건이 모두 꺼내져 있습니다.</p>
<p>오른쪽 요청서에서는 같은 쪽지를 접어 넣은 투명 봉투가 파란 빈칸 안에만 있고, 인쇄된 줄은 모두 보입니다. 옆 쟁반은 비어 있습니다.</p>
<h3>이 절에서 쓰는 말</h3>
<table><thead><tr><th>용어</th><th>뜻</th><th>이 절에서 보이는 모습</th></tr></thead><tbody>
<tr><td>데이터베이스(database)</td><td>여러 표를 한곳에 모아 두고, 정해진 문장으로 읽고 쓰는 저장소</td><td>파일 하나에 두 테이블을 담은 <code>shop.db</code></td></tr>
<tr><td>SQL(Structured Query Language)</td><td>데이터베이스에 표를 만들고, 행을 넣고, 읽으라고 적는 언어</td><td><code>SELECT * FROM orders</code></td></tr>
<tr><td>테이블(table)</td><td>데이터베이스 안의 표. 열 이름과 자료형을 먼저 정해 둡니다</td><td><code>customers</code>, <code>orders</code></td></tr>
<tr><td>연결(connection)</td><td>데이터베이스와 명령을 주고받는 통로</td><td><code>sqlite3.connect("shop.db")</code>가 반환한 객체</td></tr>
<tr><td>커서(cursor)</td><td>실행한 SQL의 결과 행을 들고 있는 객체</td><td><code>cursor.fetchall()</code>, <code>cursor.rowcount</code></td></tr>
<tr><td>제약(constraint)</td><td>테이블에 적어 두고, 어기는 행을 막는 조건</td><td><code>PRIMARY KEY</code>, <code>NOT NULL</code>, <code>FOREIGN KEY</code></td></tr>
<tr><td>커밋(commit)</td><td>데이터베이스에 한 변경을 파일에 확정하는 일. Git 커밋과 이름만 같습니다</td><td><code>connection.commit()</code></td></tr>
<tr><td>자리표시자(placeholder)</td><td>SQL 문장에서 값이 들어갈 자리를 비워 둔 표시</td><td><code>WHERE orders.customer_id = ?</code></td></tr>
<tr><td>SQL 주입(SQL injection)</td><td>입력 글이 SQL 문장의 일부로 읽혀 문장의 뜻이 바뀌는 문제</td><td><code>C001' OR '1'='1</code>로 3건</td></tr>
</tbody></table>
<h3>이 절에서 실행하는 SQL 문장</h3>
<p>SQL 문장은 영어 낱말로 시작해 무엇을 할지 적습니다. 아래 표는 노트북에서 실행한 순서대로, 문장마다 뜻과 일상 예와 코드를 나란히 적었습니다.</p>
<table><thead><tr><th>문장</th><th>뜻</th><th>일상 예</th><th>노트북 코드</th></tr></thead><tbody>
<tr><td><code>PRAGMA foreign_keys = ON</code></td><td>SQLite의 외래 키 검사를 이 연결에서 켭니다</td><td>주문을 받기 전에 손님 카드부터 찾아보기로 정하기</td><td>연결 직후 한 번(3절)</td></tr>
<tr><td><code>CREATE TABLE</code></td><td>새 테이블과 열, 제약을 만듭니다</td><td>새 장부 첫 줄에 칸 이름 적기</td><td><code>customer_id TEXT PRIMARY KEY</code>(4·5절)</td></tr>
<tr><td><code>INSERT INTO … VALUES</code></td><td>테이블에 행을 넣습니다</td><td>장부에 새 줄 적기</td><td><code>('C001', '김하나')</code>(6절)</td></tr>
<tr><td><code>SELECT … FROM</code></td><td>테이블에서 열을 골라 읽습니다</td><td>「주문 장부의 모든 칸을 보여 주세요」</td><td><code>SELECT * FROM orders</code>(7절)</td></tr>
<tr><td><code>WHERE</code></td><td>남길 행의 조건을 적습니다</td><td>「C001 고객 줄만」</td><td><code>WHERE customer_id = 'C001'</code>(8절)</td></tr>
<tr><td><code>ORDER BY</code></td><td>행의 순서를 정합니다. 방향을 적지 않으면 작은 값부터입니다</td><td>금액이 작은 쪽지부터 늘어놓기</td><td><code>ORDER BY amount</code>(9절)</td></tr>
<tr><td><code>JOIN … ON</code></td><td>짝 조건이 맞는 두 테이블의 행을 잇습니다</td><td>쪽지의 번호로 손님 카드 찾기</td><td><code>ON orders.customer_id = customers.customer_id</code>(10절)</td></tr>
</tbody></table>
<h3>요청 문장을 SQL 조각으로 나누기</h3>
<p>「C001 고객의 주문 번호, 이름, 금액을 주문 번호 순서로」라는 요청에는 네 가지 결정이 들어 있습니다. 읽을 열, 이을 테이블, 고를 행, 순서입니다. SQL 문장은 이 넷을 <code>SELECT</code>, <code>FROM … JOIN … ON</code>, <code>WHERE</code>, <code>ORDER BY</code> 조각에 한 가지씩 적습니다.</p>
<p>조각 중 부를 때마다 달라지는 것은 고객 번호 하나입니다. 그래서 함수의 SQL 문장에는 고객 번호 자리에 물음표를 적고, 값은 따로 넘깁니다.</p>
{{mermaid:03-1-요청과-SQL-조각|C001 고객의 주문 번호, 이름, 금액을 주문 번호 순서로 달라는 요청이 SELECT, FROM JOIN ON, WHERE 물음표, ORDER BY 네 조각으로 나뉘고, 물음표 자리에 값 C001이 들어가 O101 김하나 32000과 O103 김하나 27000 두 행이 나오는 그림|요청 한 문장을 SQL 조각 네 개로 나눴습니다. 달라지는 고객 번호 C001만 물음표 자리에 따로 들어갑니다.}}
<p><strong>도식 읽기</strong> — 위에서 아래로 읽습니다. 맨 위 회색 상자는 말로 한 요청이고, 파란 상자 네 개는 그 요청을 나눠 적은 SQL 조각입니다. 조각은 위부터 읽을 열, 이을 테이블과 짝 조건, 고를 행의 조건, 정렬 기준입니다.</p>
<p>오른쪽 초록 상자는 함수가 받은 값 C001이고, WHERE 조각의 물음표 자리로 들어갑니다. 맨 아래 노란 상자는 노트북 15절에서 출력으로 확인한 두 주문입니다.</p>
<h3>값은 문장과 따로 넘깁니다</h3>
<p>메서드 <code>execute()</code>에 SQL 글 하나만 넣으면, 데이터베이스는 그 글 전체를 SQL 문장으로 읽습니다. 입력 글을 f-string으로 이어 붙였다면 입력도 문장의 일부가 됩니다.</p>
<p>둘째 인자에 값 목록을 따로 넣으면 이야기가 다릅니다. SQL 문장은 물음표가 있는 모양 그대로 읽히고, 목록의 값은 물음표 자리의 값으로만 쓰입니다. 입력에 따옴표나 <code>OR</code>가 있어도 고객 번호 글자의 일부일 뿐입니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2>
<p>노트북은 임시 폴더에 데이터베이스 파일 <code>shop.db</code>를 만들고, 02절과 같은 고객 두 명과 주문 세 건을 테이블에 넣습니다. SQL 문장을 하나씩 실행하며 행을 읽고, 고르고, 정렬하고, 두 테이블을 잇습니다. 이어서 제약에 걸리는 행을 넣어 본 뒤, 고객 번호로 주문을 찾는 함수를 만듭니다.</p>
<p>모델을 부르지 않으므로 API 키가 필요 없고 비용도 들지 않습니다. 따로 설치하는 패키지도 없습니다. 교재 출력은 Python 3.12.13과 그 Python이 쓰는 SQLite 3.53.1로 만들었습니다.</p>
<p><strong>강의와 실습 범위</strong> — 강의 시간에는 노트북의 4~10번과 14·15·17·18번 소제목을 설명합니다. 4~10번은 테이블 만들기부터 JOIN까지이고, 14·15·17·18번은 조회 함수와 Before/After입니다. 2·3번, 11~13번(제약과 남은 행 수), 16번(값 바꿔 보기)은 셀을 함께 실행합니다. 결과 읽기는 실습 시간에 이어서 읽습니다.</p>
{{notebook:03-SQL로-조회-함수-만들기|example}}
<p class="look"><b>확인할 점</b> — 9절에서 <code>ORDER BY amount</code>를 더하자 O103이 먼저 나왔는지 봅니다. 11·12절의 오류 메시지가 서로 다른 제약 이름을 적었는지 확인합니다. 15절 합계가 02절과 같은 <code>59000</code>인지도 봅니다.</p>
<h3>테이블을 만들고 제약 확인하기</h3>
<p>행은 고객부터 넣었습니다. 외래 키 검사를 켠 연결에서는 주문이 가리킬 고객 행이 먼저 있어야 하기 때문입니다. 행을 넣은 뒤에는 <code>commit()</code>으로 확정했습니다.</p>
<p>이미 있는 C001로 고객을 한 번 더 넣자 <code>UNIQUE constraint failed: customers.customer_id</code>가 나왔습니다. 고객 테이블에 없는 C003으로 주문을 넣자 <code>FOREIGN KEY constraint failed</code>가 나왔습니다. 두 오류 뒤에 센 행 수는 고객 2, 주문 3으로 그대로였습니다.</p>
<p>02절 pandas에서는 겹친 키가 행을 늘리고, 짝 없는 키가 행을 조용히 뺐습니다. 데이터베이스 제약은 그런 행이 들어오는 순간에 막았습니다.</p>
{{mermaid:03-2-테이블과-제약|sqlite3.connect와 PRAGMA foreign_keys = ON, CREATE TABLE 두 번으로 shop.db 안에 두 테이블을 만들고, INSERT INTO와 commit으로 2행과 3행을 넣은 뒤, C001을 한 번 더 넣으면 UNIQUE constraint failed, O104 C003을 넣으면 FOREIGN KEY constraint failed가 나오고, 남은 행 수는 고객 2와 주문 3인 흐름도|제약이 두 행을 막았습니다. 겹친 고객 번호와 짝 없는 고객 번호가 모두 넣는 순간 거절되어 행 수는 그대로입니다.}}
<p><strong>도식 읽기</strong> — 위에서 아래로 읽습니다. 파란 상자는 실행한 코드이고, 초록 상자는 그 코드가 <code>shop.db</code> 안에 만든 두 테이블입니다. 행을 넣은 파란 상자에는 출력으로 본 넣은 행 수 2와 3을 함께 적었습니다.</p>
<p>그 아래 노란 상자 두 개는 제약에 걸려, 코드가 받아 출력한 오류입니다. 왼쪽은 겹친 기본 키, 오른쪽은 짝 없는 외래 키입니다. 맨 아래 노란 상자는 두 오류 뒤에 센 행 수, 고객 2와 주문 3입니다.</p>
<h3>조회 함수로 묶기</h3>
<p>함수 <code>find_customer_orders()</code>는 데이터베이스 파일 이름과 고객 번호를 받습니다. 함수 안에서 새 연결을 열고, 물음표를 둔 SQL 문장과 값 목록 <code>[customer_id]</code>를 <code>execute()</code>에 넣습니다. 결과 튜플은 풀어 담기로 나눠 딕셔너리로 만들고, 연결을 닫은 뒤 목록을 반환합니다.</p>
<p>고객 번호 C001로 부르자 딕셔너리 두 개가 나왔고, 금액을 더한 출력은 <code>김하나 고객의 주문 합계: 59000</code>이었습니다. 고객 번호만 C002로 바꾸자 딕셔너리 하나, <code>주문 수: 1</code>이었습니다.</p>
{{mermaid:03-3-조회-함수|입력 shop.db와 C001이 find_customer_orders 함수로 들어가 딕셔너리 2개 O101과 O103 김하나, 합계 59000이 나오고, 점선으로 C002를 넣으면 딕셔너리 1개 O102 이두리 18000이 나오는 그림|같은 함수에 고객 번호만 바꿔 넣었습니다. C001은 두 건과 합계 59000, C002는 한 건입니다.}}
<p><strong>도식 읽기</strong> — 왼쪽에서 오른쪽으로 읽습니다. 왼쪽 초록 상자는 함수에 넣은 인자, 가운데 파란 상자는 우리가 정의한 함수, 오른쪽 노란 상자는 출력으로 확인한 반환값입니다.</p>
<p>실선은 C001로 부른 호출이고, 딕셔너리 2개와 합계 59000이 나왔습니다. 점선은 고객 번호만 C002로 바꾼 호출이고, O102 이두리 18000 딕셔너리 1개가 나왔습니다.</p>
<h2 id="b6"><span class="no">6</span>일부러 실패해 보기</h2>
<p>Before 함수는 물음표 대신 f-string으로 고객 번호를 SQL 글에 바로 넣고, 만든 SQL을 출력합니다. 보통 고객 번호 C001로 부른 뒤, 따옴표와 <code>OR</code>가 섞인 입력 <code>C001' OR '1'='1</code>로 다시 부릅니다.</p>
<p>After에서는 같은 입력을 14절에서 만든 자리표시자 함수에 넣습니다. 두 함수는 SQL 조건 줄과, Before가 만든 SQL을 출력하는 줄만 다릅니다.</p>
{{notebook:03-SQL로-조회-함수-만들기|failure}}
<p>Before 함수에 C001을 넣었을 때는 조건 줄이 <code>WHERE orders.customer_id = 'C001'</code>이었고 <code>찾은 주문 수: 2</code>였습니다. 이상한 입력을 넣자 조건 줄이 <code>WHERE orders.customer_id = 'C001' OR '1'='1'</code>로 바뀌었습니다. 입력의 첫 따옴표가 글자 값을 일찍 닫았고, 늘 참인 <code>OR '1'='1'</code>이 조건으로 붙었습니다.</p>
<p>그래서 <code>찾은 주문 수: 3</code>이 나왔고, 목록에 이두리 고객의 주문 O102도 들어갔습니다. 셀은 오류 없이 끝났습니다. 고객 C001을 물었는데 다른 고객의 주문을 꺼냈으니, 에이전트 도구라면 남의 주문을 알려 주게 됩니다.</p>
<p>After 함수에 같은 입력을 넣자 <code>[]</code>와 <code>찾은 주문 수: 0</code>이 나왔습니다. 입력 글 전체가 고객 번호 하나로 비교되었고, 그런 고객 번호의 주문은 없었습니다.</p>
{{mermaid:03-4-이어-붙이기-비교|Before는 입력 C001' OR '1'='1을 f-string으로 이어 붙여 조건이 customer_id = 'C001' OR '1'='1'이 되고 O102 이두리를 포함한 3건이라는 빨간 결과로 이어지고, After는 같은 입력을 물음표 자리의 값 목록으로 넘겨 0건 빈 목록이 되는 비교 그림|같은 입력, 다른 넘기는 방법. 이어 붙이면 조건이 바뀌어 3건, 자리표시자로 넘기면 0건입니다.}}
<p><strong>도식 읽기</strong> — 위 칸이 Before, 아래 칸이 After이고, 칸마다 왼쪽에서 오른쪽으로 읽습니다. 두 칸의 초록 입력 상자에는 같은 글 <code>C001' OR '1'='1</code>이 들어갑니다. 위 칸 가운데 파란 상자는 f-string으로 만든 SQL의 조건이고, 입력 속 <code>OR</code>가 조건으로 들어갔습니다.</p>
<p>위 칸 끝의 빨간 상자는 틀린 결과, O102 이두리를 포함한 3건입니다. 아래 칸 가운데 상자는 물음표를 둔 조건이고, 입력 글은 값 목록으로 따로 갑니다. 끝의 노란 상자는 출력으로 확인한 0건, 빈 목록입니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2>
<ul><li>자리표시자는 값이 들어갈 자리에 쓰는 표시입니다. 테이블 이름이나 열 이름 자리에 물음표를 쓰는 경우는 이번에 실행하지 않았습니다.</li>
<li>외래 키 검사는 연결마다 켭니다. 14절 함수의 새 연결은 검사를 켜지 않았지만 행을 읽기만 합니다. 검사를 켜지 않은 연결로 행을 넣는 경우는 이번에 실행하지 않았습니다.</li>
<li>Python 설명서는 넣은 행을 잃지 않도록 연결을 닫기 전에 <code>commit()</code>을 부르라고 적습니다. 커밋 없이 닫는 경우는 이번에 실행하지 않았습니다.</li>
<li>함수 안에서 SQL을 실행하다 오류가 나면 <code>close()</code> 줄까지 가지 못합니다. 오류가 나도 연결을 닫는 방법(Ch 2 09절의 <code>finally</code>, 확장 경로)은 이 절에서 쓰지 않았습니다.</li>
<li>설명서의 예시는 값 목록으로 튜플 <code>(customer_id,)</code>를 많이 씁니다. 값이 하나인 튜플은 끝에 쉼표가 있어야 합니다. 이 절은 쉼표 규칙을 피하려고 목록 <code>[customer_id]</code>를 썼습니다.</li>
<li>빈 목록 <code>[]</code>은 「그 고객 번호의 주문이 없다」만 알려 줍니다. 입력이 이상했는지는 알려 주지 않으므로, 도구 결과를 설명할 때 그대로 전합니다.</li>
<li>실습 폴더 <code>data/customers.csv</code>에는 C003 박세진이 있습니다. 이 절의 C003은 02절처럼 고객 테이블에 없는 번호로 썼습니다.</li>
<li>실습 폴더 <code>data_tools.py</code>의 <code>find_customer_orders()</code>는 키 이름과 정렬 순서가 이 절 함수와 다릅니다. Ch 19 01절이 도구로 다시 쓰는 것은 같은 파일의 <code>fetch_orders(csv_path, *, status=None)</code>입니다.</li>
<li>교재 출력은 2026-09-16에 Linux의 Python 3.12.13, SQLite 3.53.1로 만들었습니다. Python 3.12의 sqlite3는 SQLite 3.7.15 이상을 요구합니다. 외래 키 검사는 SQLite 3.6.19부터 있습니다. 다른 버전과 운영체제에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2>
<ul><li>SQL 문장 <code>CREATE TABLE</code>로 테이블과 제약을 만들고, <code>INSERT INTO</code>로 행을 넣고, <code>SELECT</code>로 읽습니다. 넣은 행은 <code>commit()</code>으로 확정합니다.</li><li>읽기 문장에는 <code>WHERE</code>로 조건, <code>ORDER BY</code>로 순서, <code>JOIN … ON</code>으로 짝을 적습니다. 기본 키와 외래 키 제약은 겹친 번호와 짝 없는 번호를 넣는 순간 막았습니다.</li><li>입력 글을 f-string으로 SQL에 이어 붙인 함수는 3건을 찾았습니다. 자리표시자 <code>?</code>로 값만 넘긴 함수는 0건이었습니다.</li></ul>
<p><strong>다음 학습과 이어지는 지점</strong> — 04절에서는 데이터베이스 대신 HTTP 주소로 데이터를 주는 REST 서비스를 조회합니다. 여러 페이지로 나뉜 목록을 끝까지 읽는 함수를 만들고, 이 절처럼 딕셔너리 목록을 반환합니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz"><summary>문제와 해설</summary>
<p class="quiz-q">1. 명령 <code>WHERE</code>와 <code>ORDER BY</code>는 각각 무엇을 정하나요? 9절에서 <code>ORDER BY amount</code>를 더하자 무엇이 바뀌었나요? · 기초</p><p class="quiz-a"><b>해설</b> — 명령 <code>WHERE</code>는 남길 행의 조건을, <code>ORDER BY</code>는 행의 순서를 정합니다. 고른 행은 O101과 O103 그대로였습니다. 금액이 작은 O103 27000이 O101 32000보다 먼저 나왔습니다.</p>
<p class="quiz-q">2. 6절에서 행을 넣은 뒤 <code>commit()</code>을 부른 이유는 무엇인가요? Git 커밋과는 어떻게 다른가요? · 기초</p><p class="quiz-a"><b>해설</b> — 넣은 행을 데이터베이스 파일에 확정하려고 불렀습니다. 확정한 행은 15절에서 함수가 연 새 연결에서도 읽혔습니다. Git 커밋은 저장소에 파일 상태를 기록하는 일이라 이름만 같습니다.</p>
<p class="quiz-q">3. 02절에서 고객 번호 C003인 주문은 <code>merge()</code>에서 조용히 빠졌습니다. 이 절에서 C003 주문을 넣었을 때는 어떻게 되었나요? · 적용</p><p class="quiz-a"><b>해설</b> — 넣는 순간 <code>FOREIGN KEY constraint failed</code> 오류가 나서 행이 들어가지 않았습니다. 주문 테이블의 행 수는 3 그대로였습니다. 3절에서 이 연결의 외래 키 검사를 켰기 때문입니다.</p>
<p class="quiz-q">4. Before 함수에 <code>C001' OR '1'='1</code>을 넣었더니 주문 3건이 나왔습니다. 만든 SQL의 조건은 무엇이었고, 왜 3건인가요? · 분석</p><p class="quiz-a"><b>해설</b> — 조건은 <code>WHERE orders.customer_id = 'C001' OR '1'='1'</code>이었습니다. 입력의 따옴표가 글자 값을 닫고, 뒤의 <code>OR '1'='1'</code>이 SQL 조건이 되었습니다. 늘 참인 조건이 붙어 모든 주문이 골라졌습니다.</p>
<p class="quiz-q">5. 같은 입력을 자리표시자 함수에 넣었더니 빈 목록이 나왔습니다. 둘째 인자 <code>[customer_id]</code>는 어떤 일을 했나요? · 분석</p><p class="quiz-a"><b>해설</b> — 입력 글을 SQL 문장과 따로, 물음표 자리의 값으로 넘겼습니다. 그래서 따옴표와 <code>OR</code>까지 고객 번호 글자 하나로 비교되었습니다. 그런 고객 번호의 주문은 없어 빈 목록이 나왔습니다.</p>
</details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2>
<ul><li><a href="https://docs.python.org/3.12/library/sqlite3.html">Python 3.12 공식 문서: sqlite3</a> · 확인 2026-09-16 · 실행 Python 3.12.13</li><li><a href="https://www.sqlite.org/lang_select.html">SQLite 공식 문서: SELECT</a> · 확인 2026-09-16 · 실행 SQLite 3.53.1</li><li><a href="https://www.sqlite.org/foreignkeys.html">SQLite 공식 문서: Foreign Key Support</a> · 확인 2026-09-16 · 실행 SQLite 3.53.1</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# SQL로 조회 함수 만들기

**이 노트북에서 할 일**

1. 02절의 고객 표와 주문 표를 SQLite 데이터베이스 파일에 테이블로 만들고 행을 넣습니다.
2. SQL 문장으로 행을 고르고 정렬하고 두 테이블을 이은 뒤, 고객 번호로 주문을 찾는 함수를 만듭니다.
3. 입력 글을 SQL에 이어 붙인 함수가 다른 고객의 주문까지 꺼내는 장면을 보고, 자리표시자로 고칩니다.

**준비물** — API 키 불필요. 데이터베이스 파일은 노트북이 임시 폴더에 직접 만듭니다.
모델 호출은 0번이고 비용은 들지 않습니다. 실행 시간은 1분 이내입니다.

**강의와 실습 범위** — 강의 시간에는 4~10번과 14·15·17·18번 소제목을 설명합니다.
4~10번은 테이블 만들기부터 JOIN까지이고, 14·15·17·18번은 조회 함수와 Before/After입니다.
2·3번, 11~13번(제약과 남은 행 수), 16번(값 바꿔 보기)은 셀을 함께 실행합니다. 결과 읽기는 실습 시간에 이어서 읽습니다.

**기준 버전** — 이 절은 따로 설치하는 패키지 없이 Python에 들어 있는 모듈 sqlite3만 씁니다.
교재 출력은 2026-09-16에 Python 3.12.13과 그 Python이 쓰는 SQLite 3.53.1로 만들었습니다.
Python 3.12 설명서에 따르면 모듈 sqlite3는 SQLite 3.7.15 이상을 요구합니다.
외래 키 검사는 SQLite 3.6.19부터 있습니다. 다른 SQLite 버전에서는 오류 메시지 글이 다를 수 있고, 이번에 실행하지 않았습니다.

실습 폴더 `labs/part1/ch04-data-tools`에서 Ch 1 3절처럼 `uv sync --locked`로 환경을 만듭니다.
커널에서 이 폴더의 `.venv`를 고른 뒤 첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![C001 고객의 주문 번호, 이름, 금액을 주문 번호 순서로 달라는 요청이 SELECT, FROM JOIN ON, WHERE 물음표, ORDER BY 네 조각으로 나뉘고, 물음표 자리에 값 C001이 들어가 O101 김하나 32000과 O103 김하나 27000 두 행이 나오는 그림](attachment:03-1-요청과-SQL-조각.png)

위에서 아래로 읽습니다. 맨 위 회색 상자는 말로 한 요청이고, 그 아래 파란 상자 네 개가 요청을 나눠 적은 SQL 조각입니다.
오른쪽 초록 상자 C001은 함수가 받은 고객 번호로, WHERE 조각의 물음표 자리에 들어갑니다.
맨 아래 노란 상자는 노트북에서 출력으로 확인한 두 행입니다.

### [2] markdown {}

## 1. 준비

이 노트북은 데이터베이스 파일 하나를 만듭니다. 01·02절처럼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다.
실습 폴더에는 파일이 생기지 않습니다.

코드의 import 두 줄은 Ch 2 07절에서 배운 import 문입니다. 표준 라이브러리 모듈 os와 tempfile을 불러옵니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.784012Z', 'iopub.status.busy': '2026-09-16T16:17:20.783837Z', 'iopub.status.idle': '2026-09-16T16:17:20.789758Z', 'shell.execute_reply': '2026-09-16T16:17:20.789070Z'}, 'lesson_role': 'setup'}

```python
# 데이터베이스 파일을 둘 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다
import os
import tempfile

# mkdtemp()는 운영체제 임시 폴더 안에 새 폴더를 만들고 그 경로를 반환합니다
practice_folder = tempfile.mkdtemp(prefix="ch04-03-")
# chdir()는 터미널의 cd처럼 현재 작업 폴더를 옮깁니다
os.chdir(practice_folder)
file_names = os.listdir()
print("현재 작업 폴더의 파일:", file_names)
```

출력:
```
현재 작업 폴더의 파일: []

```

### [4] markdown {}

**결과 읽기** — 현재 작업 폴더의 파일은 `[]`로, 빈 폴더에서 시작합니다.
폴더의 경로는 컴퓨터마다 달라서 출력하지 않았습니다.

### [5] markdown {}

## 2. 데이터베이스와 sqlite3

데이터베이스(database)는 여러 표를 한곳에 모아 두고, 정해진 문장으로 읽고 쓰는 저장소입니다.
도서관 서고와 비슷합니다. 책장이 표이고, 사서에게 요청서를 내면 사서가 책을 찾아 줍니다.

이 절에서 쓰는 SQLite 데이터베이스는 표 여러 개를 파일 하나에 담습니다. 서버 프로그램을 따로 켜지 않아도 됩니다.
표준 라이브러리에 SQLite를 다루는 모듈 sqlite3가 들어 있어서, 따로 설치하지 않습니다.

실행 전에 예상합니다. 숫자와 점으로 된 버전 글 한 줄이 출력될 것입니다.

### [6] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.791277Z', 'iopub.status.busy': '2026-09-16T16:17:20.791151Z', 'iopub.status.idle': '2026-09-16T16:17:20.794308Z', 'shell.execute_reply': '2026-09-16T16:17:20.793573Z'}}

```python
# Python에 들어 있는 SQLite 모듈을 불러옵니다
import sqlite3

# sqlite_version에는 이 모듈이 함께 쓰는 SQLite의 버전 글이 들어 있습니다
print("SQLite 버전:", sqlite3.sqlite_version)
```

출력:
```
SQLite 버전: 3.53.1

```

### [7] markdown {}

**결과 읽기** — 출력은 `SQLite 버전: 3.53.1`입니다. 이 커널의 Python 3.12.13이 쓰는 SQLite 버전입니다.
다른 버전이 나오면 뒤에서 보는 오류 메시지 글이 조금 다를 수 있습니다.

### [8] markdown {}

## 3. 데이터베이스 파일 열기

데이터베이스와 명령을 주고받으려면 먼저 연결(connection)을 만듭니다. 전화를 걸어 통화가 이어진 상태와 비슷합니다.
함수 `sqlite3.connect()`에 파일 이름을 넣으면 연결 객체를 반환합니다. 그 이름의 파일이 없으면 새로 만듭니다.

데이터베이스에 표를 만들고, 행을 넣고, 읽으라고 적는 언어가 SQL(Structured Query Language)입니다.
연결 객체의 메서드 `execute()`는 SQL 문장 글 하나를 데이터베이스에 보내 실행합니다.

첫 SQL 문장 `PRAGMA foreign_keys = ON`은 SQLite의 설정 하나인 외래 키 검사를 켭니다.
SQLite 데이터베이스는 이 검사를 끈 채로 시작하고, 연결마다 따로 켜야 합니다. 검사가 하는 일은 12절에서 확인합니다.

실행 전에 예상합니다. 폴더 목록에 `shop.db` 하나가 보일 것입니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.795608Z', 'iopub.status.busy': '2026-09-16T16:17:20.795476Z', 'iopub.status.idle': '2026-09-16T16:17:20.798492Z', 'shell.execute_reply': '2026-09-16T16:17:20.798000Z'}}

```python
# shop.db 파일에 연결하고, 이 연결에서 외래 키 검사를 켭니다
# connect()는 파일이 없으면 새로 만들고, 연결 객체를 반환합니다
connection = sqlite3.connect("shop.db")
connection.execute("PRAGMA foreign_keys = ON")
file_names = os.listdir()
print("현재 작업 폴더의 파일:", file_names)
```

출력:
```
현재 작업 폴더의 파일: ['shop.db']

```

### [10] markdown {}

**결과 읽기** — 현재 작업 폴더의 파일은 `['shop.db']`로 예상과 같습니다.
설정을 켜는 문장은 출력을 남기지 않습니다. 아직 표가 없어서 이 파일은 비어 있습니다.

### [11] markdown {}

## 4. 고객 표 만들기 — CREATE TABLE

데이터베이스 안의 표를 테이블(table)이라고 부릅니다. 02절에서 CSV 파일로 만든 표와 같은 모양입니다.
SQL 문장 `CREATE TABLE`은 새 테이블을 만듭니다. 새 장부의 첫 줄에 칸 이름을 적어 두는 일과 비슷합니다.

괄호 안에는 열마다 이름, 자료형, 조건을 한 줄씩 적고 쉼표로 나눕니다.
자료형 `TEXT`는 글자입니다. 조건 `PRIMARY KEY`는 이 열을 02절의 기본 키로 정합니다.
조건 `NOT NULL`은 이 칸을 비워 둘 수 없다는 뜻입니다. 이렇게 테이블에 적어 둔 조건을 제약(constraint)이라고 부릅니다.

SQL 문장이 여러 줄이라, Ch 2 05절의 여러 줄 글 `"""…"""`에 담아 변수에 저장한 뒤 넘깁니다.
메서드 `execute()`가 반환하는 값은 7절에서 씁니다. 여기서는 변수 `cursor`에 받아만 둡니다.
실행 전에 예상합니다. 테이블을 만드는 문장은 출력을 남기지 않을 것입니다.

### [12] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.799668Z', 'iopub.status.busy': '2026-09-16T16:17:20.799566Z', 'iopub.status.idle': '2026-09-16T16:17:20.817699Z', 'shell.execute_reply': '2026-09-16T16:17:20.817189Z'}}

```python
# 고객 번호를 기본 키로 둔 고객 테이블을 만듭니다
customer_table_sql = """CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL
)"""
cursor = connection.execute(customer_table_sql)
```

출력:
```

```

### [13] markdown {}

**결과 읽기** — 출력이 없습니다. 오류 없이 끝났으므로 고객 테이블 `customers`가 만들어졌습니다.
테이블이 정말 있는지는 6절에서 행을 넣으며 확인합니다.

### [14] markdown {}

## 5. 주문 표 만들기 — FOREIGN KEY

주문 테이블의 열은 02절 `orders.csv`와 같은 네 개입니다. 금액 열의 자료형 `INTEGER`는 정수입니다.

마지막 줄 `FOREIGN KEY (customer_id) REFERENCES customers (customer_id)`가 02절의 외래 키를 적은 제약입니다.
뜻은 「이 테이블의 고객 번호 열에는, 고객 테이블의 고객 번호 열에 있는 값만 넣을 수 있다」입니다.
주문 쪽지에 붙일 스티커 색을, 카드 상자에 이미 있는 카드 색에서만 고르는 일과 같습니다.

실행 전에 예상합니다. 이 셀도 출력이 없을 것입니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.818973Z', 'iopub.status.busy': '2026-09-16T16:17:20.818843Z', 'iopub.status.idle': '2026-09-16T16:17:20.825698Z', 'shell.execute_reply': '2026-09-16T16:17:20.825263Z'}}

```python
# 고객 번호를 외래 키로 둔 주문 테이블을 만듭니다
order_table_sql = """CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    status TEXT NOT NULL,
    amount INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
)"""
cursor = connection.execute(order_table_sql)
```

출력:
```

```

### [16] markdown {}

**결과 읽기** — 출력이 없습니다. 이제 `shop.db` 안에 테이블 두 개가 있습니다.
두 테이블의 고객 번호 열은 기본 키와 외래 키로 이어졌습니다.

### [17] markdown {}

## 6. 두 표에 행 넣기 — INSERT INTO

SQL 문장 `INSERT INTO 테이블 VALUES (값, 값)`은 테이블에 행을 넣습니다. 장부에 새 줄을 적는 일입니다.
괄호 하나가 행 하나이고, 괄호 여러 개를 쉼표로 이으면 여러 행을 한 번에 넣습니다.
SQL에서 글자 값은 작은따옴표로 감싸고, 숫자는 그대로 적습니다.

메서드 `execute()`가 반환하는 커서(cursor) 객체의 속성 `rowcount`에는 바뀐 행 수가 들어 있습니다.
고객을 먼저 넣습니다. 외래 키 검사가 켜져 있어서, 주문이 가리킬 고객이 먼저 있어야 합니다.

넣은 행은 연결의 메서드 `commit()`을 불러야 파일에 확정됩니다. 이 확정을 커밋(commit)이라고 부릅니다.
Ch 3 01절의 Git 커밋과 이름은 같지만, 여기서는 데이터베이스에 한 변경을 확정하는 일입니다.

실행 전에 예상합니다. 고객 테이블에 2행, 주문 테이블에 3행을 넣었다고 출력될 것입니다.

### [18] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.827093Z', 'iopub.status.busy': '2026-09-16T16:17:20.826976Z', 'iopub.status.idle': '2026-09-16T16:17:20.833536Z', 'shell.execute_reply': '2026-09-16T16:17:20.833137Z'}}

```python
# 고객 두 명과 주문 세 건을 두 테이블에 넣습니다
cursor = connection.execute("""INSERT INTO customers VALUES
    ('C001', '김하나'),
    ('C002', '이두리')""")
print("고객 테이블에 넣은 행 수:", cursor.rowcount)
cursor = connection.execute("""INSERT INTO orders VALUES
    ('O101', 'C001', 'paid', 32000),
    ('O102', 'C002', 'pending', 18000),
    ('O103', 'C001', 'paid', 27000)""")
print("주문 테이블에 넣은 행 수:", cursor.rowcount)
# 넣은 행을 파일에 확정합니다
connection.commit()
```

출력:
```
고객 테이블에 넣은 행 수: 2
주문 테이블에 넣은 행 수: 3

```

### [19] markdown {}

**결과 읽기** — 출력은 `고객 테이블에 넣은 행 수: 2`와 `주문 테이블에 넣은 행 수: 3`으로 예상과 같습니다.
커밋은 출력을 남기지 않습니다. 넣은 행은 15절에서 새 연결을 열어 읽어 봅니다.

### [20] markdown {}

## 7. 표 전체 읽기 — SELECT와 FROM

SQL 문장 `SELECT 열 FROM 테이블`은 테이블에서 행을 읽습니다. 사서에게 「주문 장부의 모든 칸을 보여 주세요」라고 적어 내는 요청입니다.
명령 `SELECT` 뒤에는 읽을 열을, `FROM` 뒤에는 테이블 이름을 적습니다. 별표 `*`는 모든 열이라는 뜻입니다.

읽기 문장을 실행하면 커서가 결과 행을 들고 있습니다. 커서의 메서드 `fetchall()`은 남은 결과 행을 모두 목록으로 반환합니다.
목록 안의 행 하나는 Ch 2 03절에서 배운 튜플이고, 열 순서대로 값이 들어 있습니다.

실행 전에 예상합니다. 주문 세 행이 튜플 세 개로 출력될 것입니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.834556Z', 'iopub.status.busy': '2026-09-16T16:17:20.834456Z', 'iopub.status.idle': '2026-09-16T16:17:20.837150Z', 'shell.execute_reply': '2026-09-16T16:17:20.836779Z'}}

```python
# 주문 테이블의 모든 열과 모든 행을 읽습니다
cursor = connection.execute("SELECT * FROM orders")
# fetchall()은 결과 행을 튜플 목록으로 반환합니다
rows = cursor.fetchall()
print("읽은 행:")
for row in rows:
    print(row)
```

출력:
```
읽은 행:
('O101', 'C001', 'paid', 32000)
('O102', 'C002', 'pending', 18000)
('O103', 'C001', 'paid', 27000)

```

### [22] markdown {}

**결과 읽기** — 라벨 줄 아래 첫 줄 `('O101', 'C001', 'paid', 32000)`부터 세 줄이 출력되었습니다.
튜플 안의 값은 테이블을 만들 때 적은 열 순서입니다. 금액 `32000`은 따옴표가 없어 정수입니다.

이번 출력은 넣은 순서와 같습니다. 하지만 SQLite 설명서는 순서를 정하지 않은 읽기의 행 순서를 약속하지 않습니다.
순서를 정하는 방법은 9절에서 봅니다.

### [23] markdown {}

## 8. 조건으로 행 고르기 — WHERE

명령 `WHERE` 뒤에는 남길 행의 조건을 적습니다. 「고객 번호가 C001인 주문만」처럼 장부에서 줄을 고르는 일입니다.
01절에서 마스크를 `loc`에 넣어 행을 고르던 일을 SQL 문장 안에 적는 모양입니다.

같은지 비교할 때 SQL에서는 `=` 하나를 씁니다. 뜻은 Python의 `==`와 같습니다.
이번에는 `SELECT` 뒤에 열 이름 두 개를 적어, 주문 번호와 금액만 읽습니다.

실행 전에 예상합니다. 김하나 고객의 주문 O101과 O103이 값 두 개짜리 튜플로 나올 것입니다.

### [24] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.838161Z', 'iopub.status.busy': '2026-09-16T16:17:20.838051Z', 'iopub.status.idle': '2026-09-16T16:17:20.840347Z', 'shell.execute_reply': '2026-09-16T16:17:20.840000Z'}}

```python
# 고객 번호가 C001인 주문의 번호와 금액만 읽습니다
where_sql = "SELECT order_id, amount FROM orders WHERE customer_id = 'C001'"
cursor = connection.execute(where_sql)
rows = cursor.fetchall()
print("읽은 행:")
for row in rows:
    print(row)
```

출력:
```
읽은 행:
('O101', 32000)
('O103', 27000)

```

### [25] markdown {}

**결과 읽기** — 출력은 `('O101', 32000)`과 `('O103', 27000)` 두 줄로 예상과 같습니다.
고객 C002의 주문 O102는 조건에 맞지 않아 빠졌습니다.

### [26] markdown {}

## 9. 순서 정하기 — ORDER BY

명령 `ORDER BY` 뒤에는 정렬 기준 열을 적습니다. 주문 쪽지를 금액이 작은 것부터 늘어놓는 일입니다.
방향을 적지 않으면 작은 값부터 정렬합니다. 큰 값부터 정렬하려면 열 이름 뒤에 `DESC`를 붙이는데, 이번에는 실행하지 않았습니다.

앞 셀과 같은 조건에 `ORDER BY amount`만 더합니다. 문장이 길어져 여러 줄 글에 담았습니다.
실행 전에 예상합니다. 금액이 작은 O103이 O101보다 먼저 나올 것입니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.841436Z', 'iopub.status.busy': '2026-09-16T16:17:20.841343Z', 'iopub.status.idle': '2026-09-16T16:17:20.844031Z', 'shell.execute_reply': '2026-09-16T16:17:20.843588Z'}}

```python
# 같은 조건의 주문을 금액이 작은 것부터 정렬해 읽습니다
order_by_sql = """SELECT order_id, amount FROM orders
WHERE customer_id = 'C001'
ORDER BY amount"""
cursor = connection.execute(order_by_sql)
rows = cursor.fetchall()
print("읽은 행:")
for row in rows:
    print(row)
```

출력:
```
읽은 행:
('O103', 27000)
('O101', 32000)

```

### [28] markdown {}

**결과 읽기** — 라벨 줄 아래 첫 행이 `('O103', 27000)`, 둘째 행이 `('O101', 32000)`으로 순서가 바뀌었습니다.
고른 행은 앞 셀과 같은 두 개이고, 순서만 금액 기준으로 정해졌습니다.

### [29] markdown {}

## 10. 두 표 잇기 — JOIN과 ON

주문 테이블에는 고객 이름이 없습니다. 02절처럼 고객 번호로 고객 테이블을 이어야 이름을 읽을 수 있습니다.
명령 `JOIN` 뒤에는 이을 테이블을, `ON` 뒤에는 짝을 찾는 조건을 적습니다. 02절 `merge()`의 기본값과 같은 내부 조인입니다.

두 테이블에 모두 `customer_id` 열이 있어서, 열 이름 앞에 테이블 이름과 점을 붙여 구분합니다.
예를 들어 `orders.customer_id`는 주문 테이블의 고객 번호이고, `customers.customer_id`는 고객 테이블의 고객 번호입니다.

실행 전에 예상합니다. 02절 연결 결과처럼 3행이고, O101과 O103에 김하나가 붙을 것입니다.

### [30] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.844923Z', 'iopub.status.busy': '2026-09-16T16:17:20.844835Z', 'iopub.status.idle': '2026-09-16T16:17:20.847571Z', 'shell.execute_reply': '2026-09-16T16:17:20.847065Z'}}

```python
# 주문 테이블과 고객 테이블을 고객 번호로 이어, 주문마다 고객 이름을 붙입니다
join_sql = """SELECT orders.order_id, customers.name, orders.amount
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
ORDER BY orders.order_id"""
cursor = connection.execute(join_sql)
rows = cursor.fetchall()
print("읽은 행:")
for row in rows:
    print(row)
print("연결한 행 수:", len(rows))
```

출력:
```
읽은 행:
('O101', '김하나', 32000)
('O102', '이두리', 18000)
('O103', '김하나', 27000)
연결한 행 수: 3

```

### [31] markdown {}

**결과 읽기** — `('O101', '김하나', 32000)`, `('O102', '이두리', 18000)`, `('O103', '김하나', 27000)` 세 줄입니다.
마지막 줄 `연결한 행 수: 3`도 02절에서 연결한 표의 행 수와 같습니다.

### [32] markdown {}

## 11. 제약이 막는 행 넣어 보기 — 겹친 기본 키

02절 Before에서는 C001 줄이 두 번 든 고객 표를 연결해 주문이 두 번 세어졌습니다.
데이터베이스는 그런 줄이 들어오는 순간에 막을 수 있습니다. 이미 있는 고객 번호 C001로 고객 한 명을 더 넣어 봅니다.

제약을 어기는 변경이 들어오면 모듈 sqlite3는 오류 IntegrityError를 냅니다.
이 오류 이름은 sqlite3 모듈 안에 있어 `sqlite3.IntegrityError`처럼 점으로 이어 적습니다. 02절 `pd.errors.MergeError`와 같은 모양입니다.
Ch 2 05절처럼 이 오류 이름만 받는 `try/except`로 감싸 셀을 끝까지 실행합니다.

실행 전에 예상합니다. 기본 키가 겹쳐서 넣기 오류 메시지가 출력될 것입니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.848603Z', 'iopub.status.busy': '2026-09-16T16:17:20.848499Z', 'iopub.status.idle': '2026-09-16T16:17:20.850792Z', 'shell.execute_reply': '2026-09-16T16:17:20.850328Z'}}

```python
# 이미 있는 고객 번호 C001로 고객 한 명을 더 넣어 봅니다
try:
    connection.execute("INSERT INTO customers VALUES ('C001', '김하나')")
except sqlite3.IntegrityError as error:
    print("넣기 오류:", error)
```

출력:
```
넣기 오류: UNIQUE constraint failed: customers.customer_id

```

### [34] markdown {}

**결과 읽기** — 출력은 `넣기 오류: UNIQUE constraint failed: customers.customer_id`입니다.
고객 테이블의 고객 번호 열이 「값이 모두 달라야 한다(UNIQUE)」는 조건을 어겼다는 뜻입니다.
기본 키에는 이 조건이 들어 있습니다. 행이 정말 들어가지 않았는지는 13절에서 셉니다.

### [35] markdown {}

## 12. 제약이 막는 행 넣어 보기 — 짝 없는 외래 키

02절 값 바꿔 보기에서는 고객 표에 없는 번호 C003을 쓴 주문이, 내부 조인에서 오류 없이 빠졌습니다.
이번에는 그런 주문을 넣는 순간에 막히는지 봅니다. 주문 O104의 고객 번호를 C003으로 적어 넣습니다.

실행 전에 예상합니다. 3절에서 켠 외래 키 검사가 이 행을 거절해, 넣기 오류 메시지가 출력될 것입니다.

### [36] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.851845Z', 'iopub.status.busy': '2026-09-16T16:17:20.851746Z', 'iopub.status.idle': '2026-09-16T16:17:20.854183Z', 'shell.execute_reply': '2026-09-16T16:17:20.853634Z'}}

```python
# 고객 테이블에 없는 번호 C003으로 주문 한 건을 넣어 봅니다
try:
    connection.execute("INSERT INTO orders VALUES ('O104', 'C003', 'paid', 9000)")
except sqlite3.IntegrityError as error:
    print("넣기 오류:", error)
```

출력:
```
넣기 오류: FOREIGN KEY constraint failed

```

### [37] markdown {}

**결과 읽기** — 출력은 `넣기 오류: FOREIGN KEY constraint failed`입니다. 외래 키 제약을 어겼다는 뜻입니다.
고객 테이블에 C003이 없어서, 이 주문은 가리킬 고객이 없습니다.

### [38] markdown {}

## 13. 남은 행 세고 연결 닫기

두 오류 뒤에 테이블마다 행이 몇 개인지 셉니다. 넣으려던 C001 고객과 O104 주문이 들어가지 않았다면 6절과 같아야 합니다.
확인이 끝나면 연결의 메서드 `close()`로 연결을 닫습니다. 14절의 함수는 부를 때마다 새 연결을 엽니다.

실행 전에 예상합니다. 고객 테이블은 2행, 주문 테이블은 3행일 것입니다.

### [39] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.855045Z', 'iopub.status.busy': '2026-09-16T16:17:20.854962Z', 'iopub.status.idle': '2026-09-16T16:17:20.857458Z', 'shell.execute_reply': '2026-09-16T16:17:20.856997Z'}}

```python
# 두 테이블에 남은 행 수를 셉니다
cursor = connection.execute("SELECT * FROM customers")
customer_rows = cursor.fetchall()
print("고객 테이블의 행 수:", len(customer_rows))
cursor = connection.execute("SELECT * FROM orders")
order_rows = cursor.fetchall()
print("주문 테이블의 행 수:", len(order_rows))
# 테이블을 만들고 확인하는 일이 끝나서 연결을 닫습니다
connection.close()
```

출력:
```
고객 테이블의 행 수: 2
주문 테이블의 행 수: 3

```

### [40] markdown {}

**결과 읽기** — 출력은 `고객 테이블의 행 수: 2`와 `주문 테이블의 행 수: 3`으로 6절과 같습니다.
제약에 걸린 두 행은 테이블에 들어가지 않았습니다. 연결을 닫는 줄은 출력을 남기지 않습니다.

### [41] markdown {}

## 14. 고객 번호로 주문을 찾는 함수 — 자리표시자

이제 8~10절의 조각을 모아, 고객 번호 하나를 받아 주문을 찾는 함수를 만듭니다.
고객 번호는 부를 때마다 달라집니다. 그래서 SQL 문장에는 값 대신 물음표 `?`를 적어 둡니다. 이 물음표를 자리표시자(placeholder)라고 부릅니다.

인쇄된 신청서의 빈칸과 비슷합니다. 누가 빈칸에 무엇을 적어도 인쇄된 문장은 바뀌지 않습니다.
메서드 `execute()`의 둘째 인자에 값 목록 `[customer_id]`를 넣으면, 목록의 값이 물음표 자리에 차례로 들어갑니다.

함수는 01절 `fetch_orders()`처럼 딕셔너리 목록을 반환합니다. 결과 튜플 한 줄은 Ch 2 03절의 풀어 담기로 변수 세 개에 나눕니다.
실행 전에 예상합니다. 함수를 정의만 하는 셀이라 출력은 없을 것입니다.

### [42] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.858267Z', 'iopub.status.busy': '2026-09-16T16:17:20.858192Z', 'iopub.status.idle': '2026-09-16T16:17:20.860454Z', 'shell.execute_reply': '2026-09-16T16:17:20.859964Z'}}

```python
# 데이터베이스 파일 이름과 고객 번호를 받아, 그 고객의 주문을 딕셔너리 목록으로 반환합니다
def find_customer_orders(database_name: str, customer_id: str) -> list:
    sql = """SELECT orders.order_id, customers.name, orders.amount
    FROM orders JOIN customers ON orders.customer_id = customers.customer_id
    WHERE orders.customer_id = ?
    ORDER BY orders.order_id"""
    connection = sqlite3.connect(database_name)
    # 둘째 인자 목록의 값이 물음표 자리에 들어갑니다
    cursor = connection.execute(sql, [customer_id])
    rows = cursor.fetchall()
    connection.close()
    records = []
    for order_id, name, amount in rows:
        record = {"order_id": order_id, "name": name, "amount": amount}
        records.append(record)
    return records
```

출력:
```

```

### [43] markdown {}

**결과 읽기** — 출력이 없습니다. 함수 `find_customer_orders()`가 정의되었습니다.
함수 안의 변수 `connection`은 Ch 2 04절의 지역 변수라, 13절에서 닫은 연결과 다른 새 연결입니다.

### [44] markdown {}

## 15. 함수 부르기 — 김하나 고객의 주문 합계

고객 번호 `"C001"`로 함수를 부르고, 반환된 딕셔너리의 금액을 Ch 2 03절의 `+=`로 더합니다.
실행 전에 예상합니다. 주문 O101과 O103이 나오고, 합계는 02절과 같은 59000일 것입니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.861475Z', 'iopub.status.busy': '2026-09-16T16:17:20.861388Z', 'iopub.status.idle': '2026-09-16T16:17:20.863964Z', 'shell.execute_reply': '2026-09-16T16:17:20.863478Z'}}

```python
# 고객 C001의 주문을 찾고, 금액을 모두 더합니다
kim_records = find_customer_orders("shop.db", "C001")
print("조회 결과:", kim_records)
kim_total = 0
for record in kim_records:
    kim_total += record["amount"]
print("김하나 고객의 주문 합계:", kim_total)
assert kim_total == 59000
```

출력:
```
조회 결과: [{'order_id': 'O101', 'name': '김하나', 'amount': 32000}, {'order_id': 'O103', 'name': '김하나', 'amount': 27000}]
김하나 고객의 주문 합계: 59000

```

### [46] markdown {}

**결과 읽기** — 첫 줄 `조회 결과:` 뒤에는 딕셔너리 두 개가 있고, 이름 `'김하나'`와 금액 `32000`, `27000`이 들어 있습니다.
둘째 줄은 `김하나 고객의 주문 합계: 59000`으로 02절에서 pandas로 낸 합계와 같습니다.
6절에서 커밋한 행을 새 연결에서도 읽었습니다.

### [47] markdown {}

## 16. 값 하나 바꿔 보기 — 고객 번호 C002

SQL 문장은 그대로 두고, 함수에 넣는 고객 번호만 `"C002"`로 바꿉니다.
실행 전에 예상합니다. 이두리 고객의 주문 O102 하나만 딕셔너리 목록에 들어 있을 것입니다.

### [48] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.864689Z', 'iopub.status.busy': '2026-09-16T16:17:20.864620Z', 'iopub.status.idle': '2026-09-16T16:17:20.866658Z', 'shell.execute_reply': '2026-09-16T16:17:20.866235Z'}}

```python
# 고객 번호만 C002로 바꿔 같은 함수를 부릅니다
lee_records = find_customer_orders("shop.db", "C002")
print("조회 결과:", lee_records)
print("주문 수:", len(lee_records))
```

출력:
```
조회 결과: [{'order_id': 'O102', 'name': '이두리', 'amount': 18000}]
주문 수: 1

```

### [49] markdown {}

**결과 읽기** — 첫 줄 `조회 결과:` 뒤는 `[{'order_id': 'O102', 'name': '이두리', 'amount': 18000}]`로 딕셔너리 하나입니다.
마지막 줄 `주문 수: 1`도 예상과 같습니다. 물음표 자리에 들어간 값만 바뀌고, 반환 모양은 그대로입니다.

### [50] markdown {'lesson_part': 'before'}

## 17. Before — 입력 글을 SQL 문장에 바로 이어 붙인 함수

조회 함수가 에이전트 도구가 되면, 사용자 문장에서 고른 값이 함수에 들어갑니다. 사용자는 고객 번호 자리에 무엇이든 적을 수 있습니다.

Before 함수는 물음표 대신, Ch 2 01절의 f-string으로 고객 번호를 SQL 글에 바로 넣습니다. 여러 줄 글 앞에 `f`를 붙인 모양입니다.
글자 값은 SQL에서 작은따옴표로 감싸야 해서 `'{customer_id}'`로 적었습니다. 만든 SQL 글은 함수 안에서 출력합니다.
나머지 줄은 14절 함수와 같습니다.

실행 전에 예상합니다. 함수를 정의만 하는 셀이라 출력은 없을 것입니다.

### [51] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.867467Z', 'iopub.status.busy': '2026-09-16T16:17:20.867401Z', 'iopub.status.idle': '2026-09-16T16:17:20.870068Z', 'shell.execute_reply': '2026-09-16T16:17:20.869596Z'}, 'lesson_part': 'before'}

```python
# Before: 고객 번호를 f-string으로 SQL 글에 바로 넣어 주문을 찾습니다
def find_orders_before(database_name: str, customer_id: str) -> list:
    sql = f"""SELECT orders.order_id, customers.name, orders.amount
    FROM orders JOIN customers ON orders.customer_id = customers.customer_id
    WHERE orders.customer_id = '{customer_id}'
    ORDER BY orders.order_id"""
    print("만든 SQL:", sql)
    connection = sqlite3.connect(database_name)
    cursor = connection.execute(sql)
    rows = cursor.fetchall()
    connection.close()
    records = []
    for order_id, name, amount in rows:
        record = {"order_id": order_id, "name": name, "amount": amount}
        records.append(record)
    return records
```

출력:
```

```

### [52] markdown {'lesson_part': 'before'}

**결과 읽기** — 출력이 없습니다. 함수 `find_orders_before()`가 정의되었습니다.

먼저 보통 고객 번호 `"C001"`로 불러 봅니다.
실행 전에 예상합니다. 만든 SQL의 조건 줄에 C001이 들어가고, 15절과 같은 주문 두 개를 찾을 것입니다.

### [53] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.870975Z', 'iopub.status.busy': '2026-09-16T16:17:20.870899Z', 'iopub.status.idle': '2026-09-16T16:17:20.873207Z', 'shell.execute_reply': '2026-09-16T16:17:20.872791Z'}, 'lesson_part': 'before'}

```python
# Before: 보통 고객 번호로 불러 봅니다
normal_records = find_orders_before("shop.db", "C001")
print("찾은 주문 수:", len(normal_records))
```

출력:
```
만든 SQL: SELECT orders.order_id, customers.name, orders.amount
    FROM orders JOIN customers ON orders.customer_id = customers.customer_id
    WHERE orders.customer_id = 'C001'
    ORDER BY orders.order_id
찾은 주문 수: 2

```

### [54] markdown {'lesson_part': 'before'}

**결과 읽기** — 만든 SQL의 조건 줄은 `WHERE orders.customer_id = 'C001'`입니다.
마지막 줄 `찾은 주문 수: 2`로 15절과 같습니다. 보통 입력에서는 이 함수의 문제가 보이지 않습니다.

이번에는 고객 번호 자리에 `C001' OR '1'='1`이 들어왔다고 해 봅니다. 따옴표와 SQL 낱말이 섞인 이상한 입력입니다.
조건 사이의 `OR`는 Ch 1 05절 Python의 `or`처럼 「둘 중 하나라도 참이면 참」입니다. 비교 `'1'='1'`은 글자 1과 글자 1이 같아서 늘 참입니다.

실행 전에 예상합니다. 고객 C001만 물었으니 주문 두 개가 나와야 맞습니다.

### [55] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.874067Z', 'iopub.status.busy': '2026-09-16T16:17:20.873978Z', 'iopub.status.idle': '2026-09-16T16:17:20.876572Z', 'shell.execute_reply': '2026-09-16T16:17:20.875981Z'}, 'lesson_part': 'before'}

```python
# Before: 따옴표와 OR가 섞인 입력으로 같은 함수를 부릅니다
typed_id = "C001' OR '1'='1"
wrong_records = find_orders_before("shop.db", typed_id)
print("조회 결과:", wrong_records)
print("찾은 주문 수:", len(wrong_records))
```

출력:
```
만든 SQL: SELECT orders.order_id, customers.name, orders.amount
    FROM orders JOIN customers ON orders.customer_id = customers.customer_id
    WHERE orders.customer_id = 'C001' OR '1'='1'
    ORDER BY orders.order_id
조회 결과: [{'order_id': 'O101', 'name': '김하나', 'amount': 32000}, {'order_id': 'O102', 'name': '이두리', 'amount': 18000}, {'order_id': 'O103', 'name': '김하나', 'amount': 27000}]
찾은 주문 수: 3

```

### [56] markdown {'lesson_part': 'before'}

**결과 읽기** — 만든 SQL의 조건 줄이 `WHERE orders.customer_id = 'C001' OR '1'='1'`로 바뀌었습니다.
입력의 첫 따옴표가 글자 값을 일찍 닫았고, 뒤의 `OR '1'='1'`은 SQL 조건으로 읽혔습니다.

조건이 모든 행에서 참이 되어, 마지막 줄은 `찾은 주문 수: 3`입니다. 목록에는 이두리 고객의 주문 `O102`도 들어 있습니다.
셀은 오류 없이 끝났습니다. 입력 글이 SQL 문장의 뜻을 바꾸는 이 문제를 SQL 주입(SQL injection)이라고 부릅니다.

### [57] markdown {'lesson_part': 'after'}

## 18. After — 자리표시자로 값만 넘기기

14절에서 만든 함수 `find_customer_orders()`에 같은 입력을 넣습니다. 이 함수는 SQL 문장에 물음표를 두고, 입력은 둘째 인자로 따로 넘깁니다.
따로 넘긴 값은 SQL 문장으로 읽히지 않습니다. 따옴표와 OR까지 모두 고객 번호 글자 하나로 비교됩니다.

실행 전에 예상합니다. 고객 번호가 이 긴 글과 똑같은 주문은 없으므로 빈 목록이 나올 것입니다.

### [58] code {'execution': {'iopub.execute_input': '2026-09-16T16:17:20.877498Z', 'iopub.status.busy': '2026-09-16T16:17:20.877419Z', 'iopub.status.idle': '2026-09-16T16:17:20.879696Z', 'shell.execute_reply': '2026-09-16T16:17:20.879258Z'}, 'lesson_part': 'after'}

```python
# After: 같은 입력을 자리표시자 함수에 넣습니다
safe_records = find_customer_orders("shop.db", typed_id)
print("조회 결과:", safe_records)
print("찾은 주문 수:", len(safe_records))
assert safe_records == []
```

출력:
```
조회 결과: []
찾은 주문 수: 0

```

### [59] markdown {'lesson_part': 'after'}

**결과 읽기** — 첫 줄은 `조회 결과: []`로 빈 목록이고, 둘째 줄은 `찾은 주문 수: 0`입니다.
입력이 조건의 뜻을 바꾸지 못해, 다른 고객의 주문이 나오지 않았습니다. 검사 줄 `assert`도 멈추지 않았습니다.
보통 고객 번호에서 이 함수가 두 주문을 찾는 모습은 15절에서 이미 확인했습니다.

### [60] markdown {'lesson_part': 'after'}

## 정리

- SQL 문장 `CREATE TABLE`로 테이블과 제약을 만들고, `INSERT INTO`로 행을 넣고, `SELECT`로 읽습니다. 넣은 행은 `commit()`으로 확정합니다.
- 읽기 문장에는 `WHERE`로 조건, `ORDER BY`로 순서, `JOIN … ON`으로 짝을 적습니다. 기본 키와 외래 키 제약은 겹친 번호와 짝 없는 번호를 넣는 순간 막았습니다.
- 입력 글을 f-string으로 SQL에 이어 붙인 함수는 3건을 찾았습니다. 자리표시자 `?`로 값만 넘긴 함수는 0건이었습니다.

이번에는 Linux의 Python 3.12.13과 SQLite 3.53.1로 실행했습니다. 다른 운영체제와 SQLite 버전에서는 실행하지 않았습니다.
다음 절에서는 데이터베이스 대신 HTTP 주소로 데이터를 주는 REST 서비스에서, 여러 페이지로 나뉜 목록을 끝까지 읽습니다.

## 그림

### 03-1-요청과-SQL-조각.mmd

```mermaid
flowchart TB
  %% classes
  REQ["요청: C001 고객의<br>주문 번호 · 이름 · 금액을<br>주문 번호 순서로"]
  SEL["SELECT orders.order_id,<br>customers.name, orders.amount"]:::flow
  FRM["FROM orders<br>JOIN customers<br>ON 고객 번호가 같은 행끼리"]:::flow
  WHR["WHERE orders.customer_id = ?"]:::flow
  VAL["값 목록 · C001"]:::tool
  ORD["ORDER BY orders.order_id"]:::flow
  RES["결과 2행<br>O101 · 김하나 · 32000<br>O103 · 김하나 · 27000"]:::measure
  REQ --> SEL --> FRM --> WHR --> ORD --> RES
  VAL --> WHR
```

- 설명 대상 문장: SQL 문장은 읽을 열, 이을 테이블, 고를 행, 순서를 `SELECT`, `FROM … JOIN … ON`, `WHERE`, `ORDER BY` 조각에 한 가지씩 적습니다.
- 캡션: 요청 한 문장을 SQL 조각 네 개로 나눴습니다. 달라지는 고객 번호 C001만 물음표 자리에 따로 들어갑니다.
- 읽는 법: 위에서 아래로 읽습니다. 맨 위 회색 상자는 말로 한 요청, 파란 상자 네 개는 위부터 읽을 열(SELECT), 이을 테이블과 짝 조건(FROM · JOIN · ON), 고를 행(WHERE ?), 정렬 기준(ORDER BY)입니다. 오른쪽 초록 상자 값 목록 · C001이 WHERE 조각의 물음표 자리로 들어갑니다. 맨 아래 노란 상자는 노트북 15절 출력의 두 주문 O101 · 김하나 · 32000, O103 · 김하나 · 27000입니다. 노트북 「오늘 볼 그림」에도 씁니다.
- alt: C001 고객의 주문 번호, 이름, 금액을 주문 번호 순서로 달라는 요청이 SELECT, FROM JOIN ON, WHERE 물음표, ORDER BY 네 조각으로 나뉘고, 물음표 자리에 값 C001이 들어가 O101 김하나 32000과 O103 김하나 27000 두 행이 나오는 그림

### 03-2-테이블과-제약.mmd

```mermaid
flowchart TB
  %% classes
  CON["sqlite3.connect(shop.db)<br>PRAGMA<br>foreign_keys = ON"]:::flow
  CRT["CREATE TABLE customers<br>CREATE TABLE orders"]:::flow
  DB["shop.db 안의 두 테이블<br>기본 키 · 외래 키 customer_id"]:::tool
  INS["INSERT INTO → commit()<br>넣은 행 수 2 · 3"]:::flow
  PK["C001 한 번 더 넣기<br>UNIQUE constraint failed"]:::measure
  FK["O104 · C003 넣기<br>FOREIGN KEY<br>constraint failed"]:::measure
  CNT["남은 행 수<br>고객 2 · 주문 3"]:::measure
  CON --> CRT --> DB --> INS
  INS --> PK
  INS --> FK
  PK --> CNT
  FK --> CNT
```

- 설명 대상 문장: 데이터베이스 제약은 겹친 키와 짝 없는 키를 가진 행이 들어오는 순간에 막았습니다.
- 캡션: 제약이 두 행을 막았습니다. 겹친 고객 번호와 짝 없는 고객 번호가 모두 넣는 순간 거절되어 행 수는 그대로입니다.
- 읽는 법: 위에서 아래로 읽습니다. 파란 상자는 실행한 코드(연결과 외래 키 검사 켜기, 테이블 두 개 만들기, 행 넣기와 커밋), 초록 상자는 shop.db 안에 만든 두 테이블입니다. 행을 넣은 상자에 출력 `고객 테이블에 넣은 행 수: 2`, `주문 테이블에 넣은 행 수: 3`의 2 · 3을 적었습니다. 노란 상자 두 개는 코드가 받아 출력한 오류 `UNIQUE constraint failed`(왼쪽, 11절)와 `FOREIGN KEY constraint failed`(오른쪽, 12절), 맨 아래 노란 상자는 13절 출력 고객 2 · 주문 3입니다.
- alt: sqlite3.connect와 PRAGMA foreign_keys = ON, CREATE TABLE 두 번으로 shop.db 안에 두 테이블을 만들고, INSERT INTO와 commit으로 2행과 3행을 넣은 뒤, C001을 한 번 더 넣으면 UNIQUE constraint failed, O104 C003을 넣으면 FOREIGN KEY constraint failed가 나오고, 남은 행 수는 고객 2와 주문 3인 흐름도

### 03-3-조회-함수.mmd

```mermaid
flowchart LR
  %% classes
  IN1["입력<br>shop.db · C001"]:::tool
  IN2["값 바꿔 보기<br>shop.db · C002"]:::tool
  FN["find_customer_orders()<br>? 자리에 고객 번호<br>→ fetchall → for<br>→ 딕셔너리 목록"]:::flow
  OUT1["딕셔너리 2개<br>O101 · O103 김하나<br>합계 59000"]:::measure
  OUT2["딕셔너리 1개<br>O102 이두리 18000"]:::measure
  IN1 --> FN
  IN2 -.-> FN
  FN --> OUT1
  FN -.-> OUT2
```

- 설명 대상 문장: 함수 `find_customer_orders()`는 물음표를 둔 SQL 문장과 값 목록 `[customer_id]`를 `execute()`에 넣고, 결과를 딕셔너리 목록으로 반환합니다.
- 캡션: 같은 함수에 고객 번호만 바꿔 넣었습니다. C001은 두 건과 합계 59000, C002는 한 건입니다.
- 읽는 법: 왼쪽에서 오른쪽으로 읽습니다. 왼쪽 초록 상자는 넣은 인자, 가운데 파란 상자는 정의한 함수(? 자리에 고객 번호 → fetchall → for → 딕셔너리 목록), 오른쪽 노란 상자는 출력으로 확인한 반환값입니다. 실선은 C001 호출(딕셔너리 2개 O101 · O103 김하나, `김하나 고객의 주문 합계: 59000`), 점선은 값 바꿔 보기 C002 호출(딕셔너리 1개 O102 이두리 18000, `주문 수: 1`)입니다.
- alt: 입력 shop.db와 C001이 find_customer_orders 함수로 들어가 딕셔너리 2개 O101과 O103 김하나, 합계 59000이 나오고, 점선으로 C002를 넣으면 딕셔너리 1개 O102 이두리 18000이 나오는 그림

### 03-4-이어-붙이기-비교.mmd

```mermaid
flowchart TB
  %% classes
  subgraph BEFORE["Before · f-string으로 SQL에 이어 붙이기"]
    direction LR
    b1["입력<br>C001' OR '1'='1"]:::tool
    b2["만든 SQL 조건<br>customer_id = 'C001'<br>OR '1'='1'"]:::flow
    b3["찾은 주문 3건<br>O102 이두리 포함"]:::fail
    b1 --> b2 --> b3
  end
  subgraph AFTER["After · 자리표시자로 값만 넘기기"]
    direction LR
    a1["같은 입력"]:::tool
    a2["SQL 조건<br>customer_id = ?<br>값 목록에 입력 글"]:::flow
    a3["찾은 주문 0건<br>빈 목록"]:::measure
    a1 --> a2 --> a3
  end
  BEFORE --> AFTER
```

- 설명 대상 문장: 입력 글을 f-string으로 SQL에 이어 붙이면 조건이 바뀌어 3건이 나오고, 자리표시자로 값만 넘기면 0건입니다.
- 캡션: 같은 입력, 다른 넘기는 방법. 이어 붙이면 조건이 바뀌어 3건, 자리표시자로 넘기면 0건입니다.
- 읽는 법: 위 칸이 Before, 아래 칸이 After이고, 칸마다 왼쪽에서 오른쪽으로 읽습니다. 두 칸의 초록 입력 상자에는 같은 글 `C001' OR '1'='1`이 들어갑니다. Before 가운데 파란 상자는 f-string으로 만든 조건 `customer_id = 'C001' OR '1'='1'`, 끝의 빨간 상자는 틀린 결과 `찾은 주문 수: 3`(O102 이두리 포함)입니다. After 가운데 파란 상자는 물음표 조건과 값 목록, 끝의 노란 상자는 `[]`과 `찾은 주문 수: 0`입니다.
- alt: Before는 입력 C001' OR '1'='1을 f-string으로 이어 붙여 조건이 customer_id = 'C001' OR '1'='1'이 되고 O102 이두리를 포함한 3건이라는 빨간 결과로 이어지고, After는 같은 입력을 물음표 자리의 값 목록으로 넘겨 0건 빈 목록이 되는 비교 그림

### 03-5-요청서-빈칸.prompt.md

# 삽화 — 03-5 요청서 빈칸

- 상태: 2026-09-16 생성·검수 통과(2회 생성, 1차는 채택 보류). 모델 nano_banana_pro(서버 표기 nano_banana_2), 16:9, 2k(2752×1536), 장당 2크레딧, 합계 4크레딧(잔액 2912에서 시작). 채택 job 7e78bd4b-8ac2-4bc3-b805-13a448bcfc69. 교재 파일은 폭 1100px로 줄여 저장했고, 저장 PNG를 채택 job 결과(같은 폭으로 줄임)와 픽셀 대조해 차이 0을 확인(1차 결과와는 전 영역이 달라 1차본이 저장되지 않았음도 확인).
- 1차(채택 보류): job deb486a8-0b82-4ec3-a120-677e2fab8280. 관계(쪽지가 줄을 덮음 → 서류철 모두, 봉투가 빈칸 안 → 빈 쟁반)는 읽혔으나, 왼쪽 쟁반과 서류철이 가운데 세로선에 잘리고 오른쪽 쟁반이 그림 오른쪽 끝에 잘림. 한 칸의 물건이 옆 칸으로 넘어가는 것처럼 보여 여백·크기 문장(「nothing touches or crosses the middle line or the picture edges」, 「exactly three short paper folders … fully inside the tray」)을 더해 한 번 더 만듦.
- 검수 메모(저장 파일 기준): 가운데 세로선 왼쪽 칸 — 클립보드 요청서 위쪽 굵은 회색 줄 아래에 파란 빈칸, 그 아래 인쇄 줄 네 개. 긴 분홍 쪽지(회색 물결 낙서)가 빈칸 안에서 시작해 아래 줄들을 비스듬히 덮고 요청서 밖으로 나감. 옆 나무 쟁반에 초록·파랑·초록 서류철 세 개. 오른쪽 칸 — 같은 요청서에서 접힌 분홍 쪽지를 넣은 투명 봉투가 파란 빈칸 안에만 있고 인쇄 줄이 모두 보임. 옆 나무 쟁반은 비어 있음. 두 칸 물건이 모두 칸 안에 들어옴. 그림만 보고 「빈칸 밖까지 덮으면 다 꺼내고, 빈칸 안에 담으면 나오지 않는다」가 읽힘. 인쇄 줄 수는 프롬프트(네 줄)와 달리 굵은 줄 하나 + 네 줄이지만 관계와 무관해 채택.
- 설명 대상 문장: 이 장면을 SQL로 옮기면 인쇄된 줄이 SQL 문장, 빈칸이 자리표시자 `?`, 투명 봉투가 따로 넘기는 값 목록입니다. 빈칸 밖까지 덮은 쪽지는 f-string으로 SQL에 이어 붙인 입력입니다.
- 넣을 자리: 03절 핵심 개념 「비유로 시작하기」 셋째 단락 바로 아래
- 구성 요소와 배치(왼쪽 칸 → 오른쪽 칸): 칸마다 왼쪽에 파란 빈칸이 있는 클립보드 요청서, 오른쪽에 나무 쟁반. 왼쪽 칸은 긴 분홍 쪽지가 빈칸 밖 인쇄 줄을 덮고 쟁반에 서류철 세 개. 오른쪽 칸은 같은 쪽지가 투명 봉투에 담겨 빈칸 안에만 있고 쟁반이 빔.
- 시선 순서: 왼쪽 요청서(덮인 줄) → 왼쪽 쟁반(서류철 세 개) → 세로선 → 오른쪽 요청서(봉투가 빈칸 안) → 빈 쟁반
- 대응: 인쇄된 줄 = SQL 문장, 파란 빈칸 = 자리표시자 `?`, 분홍 쪽지 = 입력 글 `C001' OR '1'='1`, 줄을 덮은 쪽지 = f-string으로 이어 붙인 입력(Before), 투명 봉투 = 값 목록 `[customer_id]`(After), 서류철 세 개(초록 둘·파랑 하나) = 주문 세 건(김하나 O101·O103, 이두리 O102), 빈 쟁반 = 빈 목록 `[]`

## 프롬프트 (채택본, 2차)

Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos.
Two equal panels side by side, separated by a thin vertical gray line in the exact middle of the picture. Wide white margins everywhere: every object is small enough to sit fully inside its own panel with clear empty space around it, and nothing touches or crosses the middle line or the picture edges. The same objects appear in both panels at the same size and position. In each panel, on the left half there is a white request form clipped to a brown clipboard, seen from the front. The form shows exactly four printed gray horizontal lines and one empty rectangular box with a blue outline placed between the first and the second printed line. On the right half of each panel, with a clear gap from the clipboard and from the middle line, there is one small shallow wooden tray seen from the front, fully visible.
Left panel: a long pink paper strip covered with gray wavy scribble lines is glued so that it starts inside the blue box and runs diagonally down and out of the box, clearly covering the three printed gray lines below the box. The wooden tray in the left panel holds exactly three short paper folders standing up, fully inside the tray: two green folders and one blue folder.
Right panel: the same pink paper strip is folded small and sealed inside a small clear plastic sleeve, and the sleeve sits completely inside the blue box. All four printed gray lines are fully visible and nothing covers them. The wooden tray in the right panel is completely empty.
No people, no hands, no monitors, no screens, no computers, no pens, no drawers, no other objects.

## 프롬프트 (1차, 채택 보류)

1차는 위 문장에서 여백 문장(Wide white margins … picture edges), 「small … fully visible」, 「exactly three short … fully inside the tray」가 없었습니다.

