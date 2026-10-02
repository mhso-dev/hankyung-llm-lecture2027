# 01-SQLAlchemy-비동기-PostgreSQL

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 1h | 실습 2h | 코드 notebooks/01-SQLAlchemy-비동기-PostgreSQL.ipynb | 새 용어 5 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>비동기 엔진과 연결 풀을 만들고, 빌린 연결이 블록 끝에서 풀에 다시 들어가는 것을 출력으로 확인할 수 있습니다.</li>
<li>블록 <code>engine.begin()</code>으로 이름 공간과 표를 만들어 확정하고, 값 자리를 둔 SQL 글 객체로 줄을 읽을 수 있습니다.</li>
<li>조회 셋을 차례로 기다릴 때와 <code>gather()</code>로 함께 기다릴 때의 기록 차례와 연결 수, 걸린 시간을 견줄 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>이 챕터는 에이전트 서비스가 쓰는 자료와 실행 상태를 PostgreSQL 데이터베이스에 남깁니다. 챕터 제목의 DB는 데이터베이스(database)입니다. 상태 영속화는 <a href="../../part6/ch23-persistence/01-체크포인터와-스레드.html">Ch 23</a>에서 배운 상태 저장(Persistence)과 같은 뜻입니다.</p><p><a href="../../part7/ch30-fastapi-serving/01-비동기-라우팅과-스키마.html">Ch 30 01절</a>에서는 처리 함수를 <code>async def</code>로 적었습니다. 처리 함수가 데이터베이스의 답을 기다리는 동안에도, 이벤트 루프는 다른 요청을 받을 수 있어야 합니다. 그래서 이 절은 비동기로 말을 주고받는 드라이버로 데이터베이스에 붙습니다. 그리고 같은 조회 셋을 차례로 기다릴 때와 함께 기다릴 때를 견줍니다.</p><p>절 제목의 SQLAlchemy는 파이썬 코드로 데이터베이스에 SQL 글을 보내게 해 주는 라이브러리입니다. 데이터베이스 서버 PostgreSQL은 <a href="../../part3/ch12-retrieval-tuning/02-pgvector와-HNSW.html">Ch 12 02절</a>과 <a href="../../part6/ch23-persistence/02-PostgresSaver-준비와-스키마.html">Ch 23 02절</a>에서 쓴 서버입니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href="../../part1/ch02-python/12-async와-await.html">Ch 2 12절</a>에서는 <code>async def</code>로 비동기 함수를 적고, await로 코루틴을 기다렸습니다. 두 확인을 await 줄 두 개로 차례로 기다린 뒤, <code>gather()</code>에 함께 넣어 걸린 시간을 견줬습니다. 걸린 초는 <code>time.perf_counter()</code>로 읽은 두 값을 빼서 셈했습니다. 이 절은 그 두 가지 기다리는 방법을 데이터베이스 조회에 씁니다.</p><p><a href="../../part1/ch04-data-tools/03-SQL로-조회-함수-만들기.html">Ch 4 03절</a>에서는 sqlite3로 표를 만들고 줄을 넣은 뒤 <code>commit()</code>으로 확정했습니다. 그 절은 입력 글을 SQL 문장과 따로, 물음표 자리의 값으로 넘겼습니다. Ch 12 02절에서는 Docker로 켠 PostgreSQL 서버에 접속 글로 붙었습니다. Ch 23 02절에서는 SQL 낱말 <code>SCHEMA</code>를 이름 공간이라고 부르고, 절마다 제 이름 공간을 지우고 다시 만들었습니다.</p><p><a href="../../part6/ch28-mcp/01-MCP-구조와-capability-협상.html">Ch 28 01절</a>은 셀 맨 위에 await 줄을 바로 쓰는 것이 노트북 도구(IPython)의 기능이라고 풀었습니다. <a href="../../part7/ch30-fastapi-serving/03-ainvoke-요청-응답.html">Ch 30 03절</a>에서는 셀 맨 위 await로 그래프의 <code>ainvoke</code>를 기다렸습니다. 이 절도 셀 맨 위의 await와 <code>async with</code>를 씁니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>옛 전화 교환대의 판 하나를 떠올려 봅니다. 판에는 선을 꽂는 자리가 셋 있고, 자리마다 위에 작은 불이 달려 있습니다. 선을 꽂으면 그 자리에 불이 켜지고, 선이 이어진 동안에만 말이 오갑니다.</p><p>같은 판 둘을 나란히 놓습니다. 왼쪽 판에는 선 하나만 꽂혀 불 하나가 켜져 있고, 두 자리는 비어 있습니다. 오른쪽 판에는 세 자리 모두 선이 꽂혀 불 셋이 켜져 있습니다.</p><p>판이 엔진의 연결 풀이고, 꽂는 자리 셋이 인자 <code>pool_size=3</code>입니다. 꽂힌 선 하나가 연결 하나입니다. 왼쪽 판은 선 하나로 문의 셋을 차례로 받은 실행 1이 끝난 모습입니다. 오른쪽 판은 선 셋으로 셋을 함께 받은 실행 2가 끝난 모습입니다.</p><p>비유와 다른 점이 있습니다. 실제 풀의 연결은 쓰지 않는 동안에도 서버와 끊기지 않은 채 풀에 남아 있습니다. 그래서 불이 켜진 자리는 서버와 이어진 채 쉬고 있는 연결로 읽습니다.</p>
{{img:01-5-불이-하나-켜진-판과-셋-켜진-판|흰 바탕에 같은 모양의 갈색 나무 판 둘이 나란히 놓여 화면을 가로로 채웁니다. 판마다 위에 작은 둥근 불 셋, 아래에 금색 테두리의 둥근 꽂는 자리 셋이 한 줄로 있습니다. 왼쪽 판은 왼쪽 자리 하나에만 검은 선이 꽂혀 곧게 아래로 늘어지고, 그 위 불 하나만 노랗게 켜져 있습니다. 나머지 두 자리는 비어 있고 불 둘은 회색입니다. 오른쪽 판은 세 자리 모두 검은 선이 꽂혀 아래로 늘어지고, 불 셋이 모두 노랗게 켜져 있습니다. 사람·손·글자·숫자·화살표는 없는 그림|선 하나만 꽂힌 왼쪽 판은 불 하나가, 선 셋이 꽂힌 오른쪽 판은 불 셋이 켜져 있습니다.}}
<p class="look"><b>그림 읽기</b> — 흰 바탕에 같은 나무 판 둘이 나란히 있습니다. 판마다 둥근 불 셋과 그 아래 꽂는 자리 셋이 한 줄로 있습니다. 왼쪽 판은 왼쪽 자리에만 검은 선 하나가 꽂혀, 그 위 불 하나만 노랗게 켜져 있습니다. 오른쪽 판은 세 자리에 선 셋이 꽂혀 불 셋이 모두 켜져 있습니다. 판이 연결 풀이고, 꽂힌 선 하나가 연결 하나이며, 켜진 불의 수가 끝난 뒤 쉬고 있는 연결 수 하나와 셋입니다.</p>
<h3>엔진·연결·연결 풀</h3><p>비동기 엔진은 접속 글과 연결 풀을 쥔 객체입니다. 연결이 필요하면 풀에서 하나를 빌리고, 풀에 쉬는 연결이 없으면 새로 엽니다. 블록 <code>async with engine.connect()</code>가 끝나면 라이브러리가 빌린 연결을 닫아 풀에 다시 넣습니다. 이때 서버와 이어진 통로는 끊지 않고, 04절은 이 일을 반납이라고 부릅니다. SQLAlchemy 문서도 블록이 끝나 연결을 닫으면 그 연결이 풀에 놓인다고 적습니다.</p><p>접속 글의 앞부분 <code>postgresql+asyncpg</code>는 서버 종류와 드라이버를 함께 적은 것입니다. 이 절의 드라이버 asyncpg는 서버의 답을 await로 기다리게 해 줍니다. 그래서 서버를 기다리는 동안 이벤트 루프가 다른 코루틴을 진행할 수 있습니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>비동기 엔진(<code>AsyncEngine</code>)</td><td>데이터베이스에 붙는 방법과 연결 풀을 함께 관리하는 객체입니다. 만들 때는 서버에 붙지 않고, 연결이 필요할 때 엽니다. 차단기를 올려 두어도 스위치를 켜야 불이 들어오는 것과 같습니다. 이 절에서는 <code>create_async_engine(database_url, pool_size=3, max_overflow=0)</code>으로 만듭니다.</td></tr><tr><td>드라이버(driver)</td><td>파이썬과 데이터베이스 서버 사이에서 말을 주고받는 패키지입니다. 외국 손님과 가게 주인 사이에서 말을 옮겨 주는 통역사와 같습니다. 이 절에서는 접속 글의 <code>+asyncpg</code>가 비동기 드라이버 asyncpg를 고릅니다.</td></tr><tr><td>연결(connection)</td><td>엔진이 서버와 열어 둔 통로 하나로, SQL 글을 보내고 답을 받는 자리입니다. 전화가 이어져 있는 동안에만 말을 주고받는 것과 같습니다. 이 절에서는 블록 <code>async with engine.connect() as conn:</code>의 <code>conn</code>입니다.</td></tr><tr><td>연결 풀(connection pool)</td><td>한 번 연 연결을 서버와 끊지 않고 모아 두었다가 다시 빌려 주는 곳입니다. 공용 자전거를 빌려 타고, 다 타면 거치대에 다시 세워 두는 것과 같습니다. 이 절에서는 인자 <code>pool_size=3</code>·<code>max_overflow=0</code>이 크기를 정합니다. 메서드 <code>checkedin()</code>은 쉬고 있는 연결 수, <code>checkedout()</code>은 빌려 간 연결 수입니다.</td></tr><tr><td>SQL 글 객체(<code>text()</code>)</td><td>SQL 글 하나를 연결로 보낼 수 있게 감싼 객체입니다. 글 속 <code>:id</code> 같은 자리에는 실행할 때 따로 넘긴 값이 들어갑니다. 빈칸이 있는 신청서에 이름을 따로 적어 내는 것과 같습니다. 이 절에서는 <code>read_sql</code>이고, 종류는 <code>TextClause</code>입니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 엔진은 <code>엔진의 종류: AsyncEngine</code>으로, 연결 풀의 크기는 <code>풀에 둘 연결 수: 3</code>으로 출력됩니다. 연결 블록 안에서는 <code>블록 안 - 빌려 간 연결 수: 1</code>이었고, 블록이 끝난 뒤 쉬고 있는 연결이 하나가 되었습니다. SQL 글 객체는 <code>객체의 종류: TextClause</code>로 보입니다.</p>
{{mermaid:01-1-엔진과-연결-풀|위에서 아래로 읽는 흐름도입니다. 초록 상자 접속 글 postgresql+asyncpg 127.0.0.1:55431/ch31_lab에서 파란 상자 create_async_engine pool_size=3 max_overflow=0으로, 다시 회색 상자 엔진의 연결 풀 AsyncAdaptedQueuePool 풀에 둘 연결 수 셋으로 화살표가 갑니다. 풀에서 파란 상자 async with engine.connect() 연결 하나를 빌림으로, 다시 회색 상자 PostgreSQL 서버 데이터베이스 ch31_lab으로 이어집니다. 파란 상자에서 노란 상자 블록 안 빌려 간 연결 하나 블록 밖 쉬고 있는 연결 하나로도 화살표가 가는 그림|엔진은 연결 풀을 두고, async with로 빌린 연결은 블록이 끝나자 서버와 끊기지 않은 채 풀에 쉬는 연결 하나로 남았습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 초록 상자는 셀에 적은 접속 글이고, 파란 상자 둘은 우리가 부른 함수와 블록입니다. 회색 상자 둘은 라이브러리의 연결 풀과 데이터베이스 서버입니다. 노란 상자는 노트북 2절 출력으로 확인한 연결 수입니다.</p>
<h3>SQL 글 객체와 begin 블록</h3><p>함수 <code>text</code>는 SQL 글 하나를 연결로 보낼 수 있는 객체로 감쌉니다. 메서드 <code>execute</code>가 그 객체를 서버에 보내고, await로 답을 기다린 뒤 결과 객체를 내놓습니다. 글 속 <code>:id</code>·<code>:seconds</code>는 값이 들어갈 자리이고, 값은 딕셔너리로 따로 넘깁니다. Ch 4 03절의 물음표 자리와 같은 일입니다.</p><p>메서드 <code>engine.begin()</code>도 연결을 하나 빌리지만, 블록 안의 SQL 글을 한 묶음으로 실행합니다. 블록이 오류 없이 끝나면 바꾼 내용을 확정하고, 이것이 Ch 4 03절의 커밋과 같은 일입니다. 블록 안에서 오류가 나면 확정하지 않는데, 그 모양은 <a href="02-트랜잭션과-원자성.html">02절</a>에서 봅니다.</p><h3>차례로 기다리기와 함께 기다리기</h3><p>함수 <code>pg_sleep</code>으로 서버가 기다리는 동안, 파이썬 쪽은 할 일이 없습니다. await 줄은 그동안 이벤트 루프에 차례를 넘깁니다. 코루틴 셋을 <code>gather()</code>에 함께 넣으면, 하나가 서버의 답을 기다리는 동안 다른 코루틴도 요청을 보냅니다. 그래서 세 기다림이 겹칩니다.</p><p>이 절의 함수 <code>read_question</code>은 부를 때마다 연결을 따로 빌립니다. 그래서 셋이 함께 기다리는 동안 풀에 연결 셋이 필요했습니다. 차례로 기다릴 때는 한 문의가 끝나야 다음 문의가 연결을 빌리므로, 연결 하나로 충분했습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 접속 글을 정하고 비동기 엔진을 만든 뒤, 연결 하나를 빌려 서버에 묻습니다. 3절은 <code>engine.begin()</code> 블록으로 이름 공간 <code>ch31_async</code>와 표를 만들고 문의 세 줄을 넣습니다. 4절은 값 자리를 둔 SQL 글 객체와 함수 <code>read_question</code>을 만들어 문의 하나를 읽습니다. 5~8절은 가설을 세우고 두 실행을 견주고, 9절은 이름 공간을 지웁니다.</p><p>모델 요청은 0번이고, API 키 없이 실행합니다. 데이터베이스 서버는 Docker 컨테이너 <code>kdt-ch31-postgres</code>를 <code>127.0.0.1:55431</code>에서 켜 둡니다. 작업 폴더에 파일을 쓰지 않습니다.</p>
{{notebook:01-SQLAlchemy-비동기-PostgreSQL}}
<p class="look"><b>확인할 점</b> — 노트북 2절에서 <code>풀에 둘 연결 수: 3</code>과 <code>블록 밖 - 빌려 간 연결 수: 0</code>을 봅니다. 3절에서 <code>넣은 줄 수: 3</code>과 줄 목록 셋을 확인합니다. 4절의 <code>적힌 기록: [('시작', 1), ('끝', 1)]</code>과 <code>풀에 쉬고 있는 연결 수: 1</code>도 찾습니다. 서버 버전 줄의 버전 번호는 켠 서버에 따라 다를 수 있습니다.</p>
{{mermaid:01-2-이름-공간-준비와-확정|위에서 아래로 읽는 흐름도입니다. 파란 상자 async with engine.begin() 연결 하나를 빌림에서 begin 블록 안 한 묶음이라는 칸으로 화살표가 갑니다. 칸 안에는 파란 상자 셋이 위에서 아래로 이어집니다. DROP SCHEMA IF EXISTS ch31_async CASCADE, CREATE SCHEMA ch31_async와 CREATE TABLE requests, INSERT로 문의 세 줄을 넣음입니다. 칸에서 회색 상자 블록이 오류 없이 끝남 바꾼 내용을 확정으로, 다시 초록 상자 표 requests 문의 세 줄 환불 배송 결제로, 마지막으로 노란 상자 넣은 줄 셋 다시 읽은 줄 셋으로 이어지는 그림|begin 블록 안의 SQL 글 넷을 한 묶음으로 실행하자, 블록 끝에서 확정되어 표에 문의 세 줄이 남았습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 칸 안 파란 상자 셋은 노트북 3절에서 우리가 보낸 SQL 글입니다. 회색 상자는 블록이 끝날 때 라이브러리가 하는 확정이고, 초록 상자는 표에 남은 자료입니다. 노란 상자는 3절 두 셀의 출력으로 확인한 줄 수입니다.</p>
{{mermaid:01-3-연결-하나로-차례로-기다린-실행-1|위에서 아래로 읽는 흐름도입니다. 노란 상자 빈 풀에서 시작 쉬고 있는 연결 없음에서 파란 상자 셋이 차례로 이어집니다. 문의 1 연결을 빌림 0.15초 기다림 풀에 다시 넣음, 문의 2 같은 연결을 빌림 0.15초 기다림 풀에 다시 넣음, 문의 3 같은 연결을 빌림 0.15초 기다림 풀에 다시 넣음입니다. 마지막 노란 상자에는 기록 앞 셋 시작 1 끝 1 시작 2, 쉬고 있는 연결 하나가 적힌 그림|차례로 기다린 실행 1은 문의 하나가 끝난 뒤에야 다음 문의를 시작했고, 연결 하나를 세 번 빌렸다가 다시 넣었습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 위 노란 상자는 노트북 6절 준비 셀의 출력이고, 파란 상자 셋은 await 줄 셋이 차례로 부른 함수입니다. 아래 노란 상자는 6절 마지막 셀에서 확인한 기록과 연결 수입니다. 라벨의 「같은 연결」은 출력만으로 가른 것이 아닙니다. 끝난 뒤 쉬고 있는 연결이 하나였다는 출력과, 풀이 연 연결을 다시 쓴다는 문서(10블록)를 함께 읽은 것입니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>가설은 이랬습니다. 기다리는 방법만 바꿔 셋을 함께 기다리면, 세 기다림이 겹쳐 걸린 시간이 짧아질 것입니다. 받은 값 목록은 두 실행이 같을 것입니다. 아래 표는 두 실행에서 본 값을 모은 것이고, 걸린 초는 교재 출력의 값입니다.</p>
<table><thead><tr><th>견준 것</th><th>실행 1(차례로)</th><th>실행 2(함께)</th></tr></thead><tbody><tr><td>바꾼 것(기다리는 방법)</td><td>await 줄 셋으로 하나씩</td><td><code>asyncio.gather()</code>에 코루틴 셋</td></tr><tr><td>받은 값 목록</td><td><code>['환불', '배송', '결제']</code></td><td><code>['환불', '배송', '결제']</code></td></tr><tr><td>적힌 기록 앞 세 개</td><td>시작 1 · 끝 1 · 시작 2</td><td>시작 1 · 시작 2 · 시작 3</td></tr><tr><td>끝난 뒤 풀에 쉬고 있는 연결 수</td><td><code>1</code></td><td><code>3</code></td></tr><tr><td>걸린 시간(초, 교재 출력 — 다시 실행하면 달라짐)</td><td>0.48</td><td>0.19</td></tr></tbody></table>
{{mermaid:01-4-차례로와-함께-견주기|위에 회색 상자 하나가 있고 아래에 칸 둘이 나란히 놓인 그림입니다. 회색 상자 두 실행 같음 함수 read_question 문의 셋 문의마다 0.15초에서 두 칸으로 화살표가 갑니다. 왼쪽 칸 실행 1 차례로에는 파란 상자 await 줄 셋 아래 노란 상자 기록 앞 셋 시작 1 끝 1 시작 2, 쉬고 있는 연결 하나가 있습니다. 오른쪽 칸 실행 2 함께에는 파란 상자 gather에 코루틴 셋 아래 노란 상자 기록 앞 셋 시작 1 시작 2 시작 3, 쉬고 있는 연결 셋이 있습니다. 두 칸에서 맨 아래 노란 상자 받은 값 목록 같음 True, 함께 기다린 시간이 더 짧음 True로 화살표가 모이는 그림|기다리는 방법 하나만 바꾸자, 셋이 모두 시작한 뒤 연결 셋을 빌렸고 받은 값은 같은 채 먼저 끝났습니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 회색 상자는 두 실행에서 같았던 조건입니다. 왼쪽 칸이 실행 1, 오른쪽 칸이 실행 2이고, 파란 상자가 바꾼 기다리는 방법입니다. 노란 상자는 노트북 6·7·8절 출력입니다. 걸린 초는 실행할 때마다 달라져 그림에 적지 않고, 참·거짓 비교만 적었습니다.</p>
<p>받은 값 목록은 두 실행에서 같았습니다. 실행 2에서 어느 문의가 먼저 끝나는지는 실행마다 달랐지만, 함수 <code>gather()</code>는 넣은 차례대로 값을 모았습니다. 그래서 목록의 차례도 실행 1과 같았습니다.</p><p>두 실행을 가른 것은 기록의 차례와 풀의 연결 수입니다. 실행 1은 문의 하나가 끝나야 다음 문의가 시작했고, 연결 하나로 충분했습니다. 실행 2는 셋이 모두 시작한 뒤에야 끝이 적혔고, 풀이 연결 셋을 만들었습니다. 이 두 값이 세 기다림이 겹쳤다는 것을 보여 줍니다.</p><p>함께 기다린 실행 2가 먼저 끝났고, 비교 줄 <code>함께 기다린 시간이 더 짧은가: True</code>가 그 결과입니다. 걸린 초는 실행마다 달라져 결론에 쓰지 않고, 참·거짓 비교만 씁니다. 이 결과는 서버가 기다리기만 하는 조회 셋에서 본 것입니다. 서버가 계산을 많이 하는 조회나, 차례가 정해진 SQL 글은 이번에 견주지 않았습니다.</p><p>새 커널로 두 번 실행해 견주자, 코드 셀 스물하나 가운데 걸린 초가 찍힌 셀 둘만 달랐습니다. 한 번은 프로젝트 맨 위에서, 한 번은 <code>notebooks/</code> 폴더에서 연 커널이었습니다. 두 셀은 실행 1의 걸린 시간과 두 실행을 견준 표입니다. 기록 차례·연결 수·받은 값과 두 비교의 <code>True</code>는 두 번 모두 같았습니다.</p>
<p class="look"><b>확인할 점</b> — 6절과 7절의 <code>적힌 기록 앞 세 개:</code> 두 줄과 <code>풀에 쉬고 있는 연결 수:</code> 두 줄을 견줍니다. 8절 두 비교가 모두 <code>True</code>인지 봅니다. 교재 출력의 걸린 시간은 차례로 0.48초, 함께 0.19초였고, 다시 실행하면 달라집니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>걸린 시간은 이 절의 주제라서 실제로 쟀습니다. 초 값은 교재 출력을 만든 기기에서 <code>time.perf_counter()</code>로 읽은 값이라, 기기와 서버에 따라 달라집니다. 결론에는 기록 차례와 연결 수, 받은 값, 비교 줄의 참·거짓만 썼습니다.</li><li>노트북을 쓰기 전에 노트북 밖에서 같은 두 실행을 파이썬 파일로 여섯 번 실행했습니다. 기록 앞 세 개와 연결 수, 받은 값, 비교 줄의 참은 여섯 번 모두 같았습니다. 걸린 초는 차례로 0.47~0.48초, 함께 0.19~0.20초였습니다. 같은 커널에서 노트북 전체를 세 번 이어 실행했을 때도 같았습니다. 함께 기다린 실행에서 어느 문의가 먼저 끝났는지는 실행마다 달라, 노트북은 기록 앞 세 개만 출력합니다.</li><li>이 절은 작업마다 연결을 따로 빌렸습니다. 연결 하나나 <code>AsyncSession</code> 하나를 여러 작업이 함께 쓰는 장면은 실행하지 않았습니다. SQLAlchemy 문서는 <code>AsyncSession</code> 하나를 여러 작업이 함께 쓰면 안전하지 않다고 적고, 작업마다 따로 쓰라고 합니다.</li><li>풀에 둘 연결 수가 함께 기다릴 작업 수보다 적으면, 남은 작업은 연결이 빌 때까지 기다립니다. 이번에 실행하지 않았고, 연결 풀이 모자란 장면은 <a href="04-커넥션-풀-고갈과-대응.html">04절</a>에서 봅니다.</li><li>비동기 함수 안에서 동기로 기다리는 드라이버를 부르면, 그동안 이벤트 루프가 멈춥니다. <a href="../../part7/ch30-fastapi-serving/01-비동기-라우팅과-스키마.html">Ch 30 01절</a>이 노트북 밖에서 본 차단 호출과 같은 까닭이고, 이 절에서는 실행하지 않았습니다.</li><li>Docker 문서는 컨테이너 포트를 열면 기본으로 이 컴퓨터 밖에서도 붙을 수 있다고 적습니다. 그래서 명령에 <code>127.0.0.1</code>을 적어 이 컴퓨터에서만 붙게 했고, 접속 글도 같은 주소를 씁니다. 비밀번호 <code>postgres</code>는 연습용 값이라 다른 서버에 쓰지 않습니다.</li><li>이 노트북은 <code>.env</code> 파일을 읽지 않고, 2절 셀에 적은 접속 글만 씁니다. 실습 폴더의 <code>app/</code> 파일과 <code>AsyncSession</code>은 이 절에서 쓰지 않았습니다.</li><li>교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다. 그 서버는 Docker 컨테이너가 아니라 같은 접속 글로 켠 서버이고, pgvector 확장은 0.8.1입니다. Docker 이미지로 켜면 버전 번호의 끝자리가 다를 수 있습니다. 다른 버전과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>비동기 엔진은 연결 풀을 두었고, <code>async with</code>로 빌린 연결은 블록이 끝나자 풀에 다시 들어갔습니다.</li><li>블록 <code>engine.begin()</code>은 이름 공간·표·세 줄을 한 묶음으로 실행하고, 끝에서 확정했습니다.</li><li>기다리는 방법만 바꾸자, 함께 기다린 실행이 연결 셋을 빌려 받은 값은 같은 채 먼저 끝났습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href="02-트랜잭션과-원자성.html">02절</a>에서는 두 계좌의 잔액을 바꾸는 이체를 봅니다. 바꾼 내용을 따로 확정할 때와 한 블록으로 확정할 때를 견줍니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 5개 · 해설 포함</summary><p class="quiz-q">1. 엔진을 만든 직후 풀에 쉬고 있는 연결 수는 몇이었고, 연결 블록이 끝난 뒤에는 몇이 되었나요?</p><p class="quiz-a">처음에는 0이었고, 블록이 끝난 뒤 1이 되었습니다. 빌린 연결이 서버와 끊기지 않은 채 풀에 다시 들어갔기 때문입니다. 틀렸다면 노트북 2절을 다시 읽습니다.</p><p class="quiz-q">2. 블록 <code>engine.begin()</code>과 <code>engine.connect()</code>는 무엇이 다른가요?</p><p class="quiz-a">둘 다 연결을 하나 빌립니다. 블록 <code>engine.begin()</code>은 안의 SQL 글을 한 묶음으로 실행하고, 오류 없이 끝나면 확정합니다. 이 절은 표를 만들고 줄을 넣을 때 이 블록을 썼습니다. 틀렸다면 노트북 3절을 다시 읽습니다.</p><p class="quiz-q">3. SQL 글 <code>… WHERE id = :id</code>에서 <code>:id</code>는 무엇이고, 값은 어떻게 넘겼나요?</p><p class="quiz-a">값이 들어갈 자리입니다. 메서드 <code>execute</code>의 둘째 인자로, 자리 이름을 키로 한 딕셔너리 <code>{"id": item_id, …}</code>를 넘겼습니다. Ch 4 03절의 물음표 자리와 같은 일입니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">4. 실행 2가 끝난 뒤 풀에 쉬고 있는 연결 수가 셋이 된 까닭은 무엇인가요?</p><p class="quiz-a">셋이 모두 시작한 뒤에야 끝이 적혔습니다. 셋이 같은 때에 연결을 빌려야 해서, 풀이 연결 셋을 만들었습니다. 실행 1은 연결 하나를 세 번 빌렸습니다. 틀렸다면 노트북 6·7절을 다시 읽습니다.</p><p class="quiz-q">5. 동료가 「<code>gather()</code>로 묶으면 어떤 조회든 빨라진다」고 말합니다. 맞나요?</p><p class="quiz-a">이 절로는 그렇게 말할 수 없습니다. 이 절은 서버가 기다리기만 하는 조회 셋을, 작업마다 연결을 따로 빌려 견줬습니다. 계산이 많은 조회는 견주지 않았고, 풀의 연결이 모자라면 작업이 연결을 기다립니다. 틀렸다면 본문 6블록과 7블록을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html">SQLAlchemy Asynchronous I/O (asyncio)</a></div>확인 2026-09-29 · 함수 <code>create_async_engine</code>이 비동기 엔진을 만들고, <code>connect()</code>·<code>begin()</code>이 연결을 준다고 적습니다. 엔진을 다 쓰면 await로 <code>dispose()</code>를 부르라고 합니다. <code>AsyncSession</code> 하나를 여러 작업이 함께 쓰면 안전하지 않다고 적습니다.</li><li><div><a href="https://docs.sqlalchemy.org/en/20/core/connections.html">SQLAlchemy Working with Engines and Connections</a></div>확인 2026-09-29 · 블록이 끝나 연결을 닫으면, 그 연결이 풀에 놓인다고 적습니다. 블록 <code>begin()</code>은 오류 없이 끝나면 확정하고, 오류가 나면 확정하지 않는다고 적습니다.</li><li><div><a href="https://docs.sqlalchemy.org/en/20/core/pooling.html">SQLAlchemy Connection Pooling</a></div>확인 2026-09-29 · 풀은 연 연결을 메모리에 두었다가 다시 쓴다고 적습니다. 인자 <code>pool_size</code>는 풀에 계속 두는 연결 수이고, <code>max_overflow</code>는 그 위로 더 만들 수 있는 연결 수입니다. 비동기 엔진은 따로 정하지 않으면 <code>AsyncAdaptedQueuePool</code>을 쓴다고 적습니다.</li><li><div><a href="https://www.postgresql.org/docs/17/functions-datetime.html">PostgreSQL 17 Delaying Execution</a></div>확인 2026-09-29 · 함수 <code>pg_sleep</code>은 정한 초만큼 기다리고, 적어도 정한 초만큼은 기다린다고 적습니다.</li><li><div><a href="https://docs.docker.com/engine/network/port-publishing/">Docker Port publishing</a></div>확인 2026-09-29 · 컨테이너 포트를 열면 기본으로 바깥에서도 붙을 수 있다고 적습니다. 주소 <code>127.0.0.1</code>을 함께 적으면 이 컴퓨터에서만 붙을 수 있습니다.</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# SQLAlchemy 비동기 PostgreSQL

**이 노트북에서 할 일**

1. 비동기 엔진을 만들고, 연결 풀에서 연결을 빌려 PostgreSQL 서버에 SQL 글을 보냅니다.
2. 이름 공간 하나에 표를 만들고, 문의 세 줄을 넣고 읽습니다.
3. 오래 걸리는 조회 셋을 차례로 기다릴 때와 함께 기다릴 때를 견줍니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
예상 비용도 0달러입니다.

PostgreSQL 서버가 `127.0.0.1:55431`에서 켜져 있어야 합니다.
이 챕터의 여섯 절은 Docker 컨테이너 `kdt-ch31-postgres` 하나를 함께 씁니다.
컨테이너가 없으면 터미널에서 아래 명령으로 먼저 만듭니다.

```bash
docker run --name kdt-ch31-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=ch31_lab \
  -p 127.0.0.1:55431:5432 \
  -d pgvector/pgvector:0.8.1-pg17
```

비밀번호 `postgres`는 이 실습에서만 쓰는 연습용 값입니다.
줄 `-p 127.0.0.1:55431:5432`는 이 컴퓨터 안에서만 서버에 붙을 수 있게 묶는 설정입니다.
컨테이너가 꺼져 있으면 `docker start kdt-ch31-postgres`로 다시 켭니다.

노트북은 데이터베이스 `ch31_lab` 안에 이름 공간 `ch31_async`를 만들어 쓰고, 끝에서 지웁니다.
작업 폴더에 파일을 쓰지 않고, 읽어 오는 자료 파일도 없습니다.
걸린 시간은 이 절의 주제라서 실제로 잽니다.
초 값은 실행할 때마다 조금씩 달라집니다.

**기준 버전** — 첫 셀에서 패키지 둘을 설치합니다.
버전은 sqlalchemy 2.0.43과 asyncpg 0.30.0이고, 실습 폴더 잠금과 같습니다.
데이터베이스는 pgvector 확장이 든 PostgreSQL 17을 쓰고, 이 절은 pgvector를 쓰지 않습니다.

교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다.
그 서버는 Docker 컨테이너가 아니라, 같은 접속 글로 켠 서버입니다.
Docker 이미지로 켜면 서버 버전 번호의 끝자리가 다를 수 있습니다.
다른 버전과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~4절을 읽습니다.
엔진·연결·이름 공간·SQL 글 객체를 처음 보는 자리입니다.
5~8절은 가설을 세우고 두 실행을 견주는 실험이고, 실습 시간에 실행합니다.
9절은 만든 이름 공간을 지우는 정리입니다.

실습 폴더 `labs/part7/ch31-database`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 읽는 흐름도입니다. 초록 상자 접속 글 postgresql+asyncpg 127.0.0.1:55431/ch31_lab에서 파란 상자 create_async_engine pool_size=3 max_overflow=0으로, 다시 회색 상자 엔진의 연결 풀 AsyncAdaptedQueuePool 풀에 둘 연결 수 셋으로 화살표가 갑니다. 풀에서 파란 상자 async with engine.connect() 연결 하나를 빌림으로, 다시 회색 상자 PostgreSQL 서버 데이터베이스 ch31_lab으로 이어집니다. 파란 상자에서 노란 상자 블록 안 빌려 간 연결 하나 블록 밖 쉬고 있는 연결 하나로도 화살표가 가는 그림](attachment:01-1-엔진과-연결-풀.png)

위에서 아래로 읽습니다.
초록 상자는 셀에 적은 접속 글이고, 파란 상자 둘은 우리가 부른 함수와 블록입니다.
회색 상자 둘은 라이브러리의 연결 풀과 데이터베이스 서버입니다.
노란 상자는 노트북 2절 출력으로 확인한 연결 수입니다.

### [2] markdown {}

## 1. 준비

이 챕터는 에이전트 서비스가 쓰는 자료와 실행 상태를 PostgreSQL 데이터베이스에 남깁니다.
챕터 제목의 DB는 데이터베이스(database)입니다.
상태 영속화는 Ch 23에서 배운 상태 저장(Persistence)과 같은 뜻입니다.

절 제목의 SQLAlchemy는 파이썬 코드로 데이터베이스에 SQL 글을 보내고 결과를 받게 해 주는 라이브러리입니다.
데이터베이스 서버 PostgreSQL은 Ch 12 02절과 Ch 23 02절에서 쓴 서버입니다.
비동기는 Ch 2 12절의 `async`·await 방식으로 서버의 답을 기다린다는 뜻입니다.

첫 셀은 패키지 둘을 설치하고 설치된 버전 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:35.391824Z', 'iopub.status.busy': '2026-09-29T21:08:35.391658Z', 'iopub.status.idle': '2026-09-29T21:08:36.000457Z', 'shell.execute_reply': '2026-09-29T21:08:35.999711Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "sqlalchemy[asyncio]==2.0.43" "asyncpg==0.30.0"
from importlib.metadata import version

print("sqlalchemy:", version("sqlalchemy"))
print("asyncpg:", version("asyncpg"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
sqlalchemy: 2.0.43
asyncpg: 0.30.0

```

### [4] markdown {}

**결과 읽기** — 출력 줄 `sqlalchemy: 2.0.43`과 `asyncpg: 0.30.0`이 보입니다.
둘 모두 실습 폴더 잠금과 같은 버전입니다.
패키지 이름 뒤의 `[asyncio]`는 비동기 기능에 필요한 패키지 greenlet도 함께 설치하라는 표시입니다.
패키지 asyncpg는 파이썬에서 PostgreSQL 서버와 비동기로 말을 주고받는 패키지입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
모듈 `asyncio`와 `time`은 Ch 2 12절에서 쓴 모듈입니다.
함수 `text`와 `create_async_engine`은 패키지 sqlalchemy에서 가져옵니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.001752Z', 'iopub.status.busy': '2026-09-29T21:08:36.001587Z', 'iopub.status.idle': '2026-09-29T21:08:36.136741Z', 'shell.execute_reply': '2026-09-29T21:08:36.136354Z'}, 'lesson_role': 'setup'}

```python
# 시간 재기·비동기 실행·SQL 글·비동기 엔진에 쓸 이름을 가져옵니다
import asyncio
import time
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

print("가져온 이름:", "text", "create_async_engine")
```

출력:
```
가져온 이름: text create_async_engine

```

### [6] markdown {}

**결과 읽기** — 출력 줄 `가져온 이름: text create_async_engine`이 보입니다.
이 노트북에는 API 키를 확인하는 셀이 없습니다.
모델을 부르지 않기 때문입니다.

## 2. 데이터베이스에 붙기

데이터베이스에 붙으려면 어느 서버의 어느 데이터베이스에 누구로 붙을지 적은 접속 글이 필요합니다.
이 절의 접속 글은 Ch 12 02절처럼 `postgresql`로 시작하고, 그 뒤에 `+asyncpg`를 붙입니다.
드라이버(driver)는 파이썬과 데이터베이스 서버 사이에서 말을 주고받는 패키지입니다.
외국 손님과 가게 주인 사이에서 말을 옮겨 주는 통역사와 비슷합니다.
글 `+asyncpg`는 비동기로 말을 주고받는 드라이버 asyncpg를 쓰라는 표시입니다.

이 노트북은 `.env` 파일을 읽지 않고, 다음 셀에 적은 연습용 접속 글을 씁니다.
서버를 다른 주소나 계정으로 켰다면 이 셀의 글만 고칩니다.

### [7] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.137424Z', 'iopub.status.busy': '2026-09-29T21:08:36.137355Z', 'iopub.status.idle': '2026-09-29T21:08:36.139280Z', 'shell.execute_reply': '2026-09-29T21:08:36.138908Z'}}

```python
# 데이터베이스 접속 글을 정합니다(비밀번호 postgres는 이 실습에서만 쓰는 연습용 값입니다)
database_url = "postgresql+asyncpg://postgres:postgres@127.0.0.1:55431/ch31_lab"
# 비밀번호가 찍히지 않게, 글을 @에서 나눠 앞의 드라이버 부분과 뒤의 서버 부분만 출력합니다
url_parts = database_url.split("@")
print("드라이버 부분:", database_url.split("://")[0])
print("서버 주소와 데이터베이스:", url_parts[1])
```

출력:
```
드라이버 부분: postgresql+asyncpg
서버 주소와 데이터베이스: 127.0.0.1:55431/ch31_lab

```

### [8] markdown {}

**결과 읽기** — 출력 줄 `드라이버 부분: postgresql+asyncpg`가 보입니다.
라벨 `서버 주소와 데이터베이스:` 뒤의 `127.0.0.1:55431/ch31_lab`은 서버 주소·포트 번호와 데이터베이스 이름입니다.
메서드 `split`은 글을 주어진 글자에서 나눈 목록을 내놓습니다.
비밀번호가 든 가운데 부분은 출력하지 않았습니다.

다음 셀은 이 접속 글로 비동기 엔진을 만듭니다.
함수 `create_async_engine`은 접속 글을 받아 비동기 엔진(`AsyncEngine`)을 내놓습니다.

엔진은 데이터베이스에 붙는 방법과 연결 풀을 함께 관리하는 객체입니다.
만들 때는 서버에 붙지 않고, 연결이 필요할 때 엽니다.
차단기를 올려 두어도 스위치를 켜야 불이 들어오는 것과 비슷합니다.

연결 풀(connection pool)은 한 번 연 연결을 서버와 끊지 않고 모아 두었다가 다시 빌려 주는 곳입니다.
공용 자전거 거치대에서 자전거를 빌려 타고, 다 타면 거치대에 다시 세워 두는 것과 비슷합니다.
인자 `pool_size=3`은 풀에 둘 연결 수이고, `max_overflow=0`은 그 밖에 더 만들 연결 수입니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.139850Z', 'iopub.status.busy': '2026-09-29T21:08:36.139806Z', 'iopub.status.idle': '2026-09-29T21:08:36.175317Z', 'shell.execute_reply': '2026-09-29T21:08:36.174914Z'}}

```python
# 접속 글로 비동기 엔진을 만듭니다(풀에 둘 연결 수 3, 그 밖에 더 만들 연결 수 0)
engine = create_async_engine(database_url, pool_size=3, max_overflow=0)
print("엔진의 종류:", type(engine).__name__)
print("풀의 종류:", type(engine.pool).__name__)
print("풀에 둘 연결 수:", engine.pool.size())
# 엔진을 만들기만 해서는 서버에 붙지 않아, 풀에 연결이 아직 없습니다
print("풀에 쉬고 있는 연결 수:", engine.pool.checkedin())
```

출력:
```
엔진의 종류: AsyncEngine
풀의 종류: AsyncAdaptedQueuePool
풀에 둘 연결 수: 3
풀에 쉬고 있는 연결 수: 0

```

### [10] markdown {}

**결과 읽기** — 출력 줄 `엔진의 종류: AsyncEngine`과 `풀에 둘 연결 수: 3`이 보입니다.
풀의 종류 `AsyncAdaptedQueuePool`은 비동기 엔진이 따로 정하지 않으면 쓰는 풀입니다.
출력 줄 `풀에 쉬고 있는 연결 수: 0`은 아직 연 연결이 없다는 뜻입니다.
메서드 `size`는 풀에 둘 연결 수를, `checkedin`은 풀에서 쉬고 있는 연결 수를 셉니다.

다음 셀은 풀에서 연결을 하나 빌려 서버에 묻습니다.
연결(connection)은 엔진이 서버와 열어 둔 통로 하나로, SQL 글을 보내고 답을 받는 자리입니다.
전화가 이어져 있는 동안에만 말을 주고받는 것과 비슷합니다.
블록 `async with engine.connect() as conn:`은 연결 하나를 빌려 이름 `conn`에 담고, 블록이 끝나면 풀에 다시 넣습니다.

함수 `text`는 SQL 글 하나를 연결로 보낼 수 있는 객체로 감쌉니다.
메서드 `execute`는 그 객체를 서버에 보내고, await로 답을 기다린 뒤 결과 객체를 내놓습니다.
메서드 `fetchone`은 결과에서 첫 줄 하나를 꺼내고, `checkedout`은 빌려 간 연결 수를 셉니다.
셀 맨 위의 `async with`와 await는 Ch 28·30처럼 노트북 도구(IPython)의 기능입니다.

### [11] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.175924Z', 'iopub.status.busy': '2026-09-29T21:08:36.175868Z', 'iopub.status.idle': '2026-09-29T21:08:36.190041Z', 'shell.execute_reply': '2026-09-29T21:08:36.189704Z'}}

```python
# 풀에서 연결 하나를 빌려 서버에 묻고, 블록 안과 밖에서 풀의 연결 수를 봅니다
async with engine.connect() as conn:
    result = await conn.execute(text("SELECT current_database(), current_setting('server_version')"))
    row = result.fetchone()
    print("블록 안 - 빌려 간 연결 수:", engine.pool.checkedout())
print("데이터베이스와 서버 버전:", row)
# 블록이 끝나면 연결은 서버와 끊기지 않은 채 풀에 다시 들어갑니다
print("블록 밖 - 빌려 간 연결 수:", engine.pool.checkedout())
print("풀에 쉬고 있는 연결 수:", engine.pool.checkedin())
```

출력:
```
블록 안 - 빌려 간 연결 수: 1
데이터베이스와 서버 버전: ('ch31_lab', '17.11')
블록 밖 - 빌려 간 연결 수: 0
풀에 쉬고 있는 연결 수: 1

```

### [12] markdown {}

**결과 읽기** — 출력 줄 `블록 안 - 빌려 간 연결 수: 1`과 `블록 밖 - 빌려 간 연결 수: 0`이 보입니다.
라벨 `데이터베이스와 서버 버전:` 뒤에는 `('ch31_lab', '17.11')`이 찍혔습니다.
블록이 끝난 뒤 `풀에 쉬고 있는 연결 수: 1`이 되었습니다.
블록이 끝나자 라이브러리가 빌린 연결을 닫아 풀에 다시 넣었고, 서버와 이어진 통로는 끊지 않았습니다.
04절은 이 일을 반납이라고 부릅니다.

PostgreSQL 함수 `current_database()`는 붙은 데이터베이스 이름을 내놓습니다.
함수 `current_setting('server_version')`은 서버 버전 번호를 내놓습니다.
버전 `17.11`은 교재 출력을 만든 서버의 버전이고, Docker 이미지로 켜면 끝자리가 다를 수 있습니다.

## 3. 이름 공간과 표 준비

이 절의 표는 이름 공간 `ch31_async`에 둡니다.
이름 공간은 Ch 23 02절에서 SQL 낱말 `SCHEMA`를 부른 말로, 한 데이터베이스 안에서 표들을 이름으로 묶어 두는 자리입니다.
여섯 절이 같은 데이터베이스를 쓰므로, 절마다 제 이름 공간을 씁니다.

메서드 `engine.begin()`도 연결을 하나 빌리지만, 블록 안의 SQL 글을 한 묶음으로 실행합니다.
블록이 오류 없이 끝나면 바꾼 내용을 확정합니다.
Ch 4 03절에서 sqlite3의 `commit()`으로 넣은 행을 확정한 커밋과 같은 일입니다.
블록 안에서 오류가 나면 확정하지 않는데, 그 모양은 02절에서 봅니다.

문장 `DROP SCHEMA IF EXISTS ch31_async CASCADE`는 그 이름 공간이 있으면 안의 표까지 함께 지웁니다.
그래서 이 셀을 다시 실행해도 빈 이름 공간에서 다시 시작합니다.
문장 `CREATE TABLE`과 `INSERT INTO`는 Ch 4 03절처럼 표를 만들고 줄을 넣습니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.190630Z', 'iopub.status.busy': '2026-09-29T21:08:36.190582Z', 'iopub.status.idle': '2026-09-29T21:08:36.195837Z', 'shell.execute_reply': '2026-09-29T21:08:36.195467Z'}}

```python
# 이름 공간 ch31_async를 지우고 다시 만든 뒤, 표 requests에 문의 세 줄을 넣습니다
table_sql = "CREATE TABLE ch31_async.requests (id int PRIMARY KEY, question text)"
insert_sql = "INSERT INTO ch31_async.requests VALUES (1, '환불'), (2, '배송'), (3, '결제')"
# begin() 블록은 안의 SQL 글을 한 묶음으로 실행하고, 오류 없이 끝나면 확정합니다
async with engine.begin() as conn:
    await conn.execute(text("DROP SCHEMA IF EXISTS ch31_async CASCADE"))
    await conn.execute(text("CREATE SCHEMA ch31_async"))
    await conn.execute(text(table_sql))
    inserted = await conn.execute(text(insert_sql))
print("넣은 줄 수:", inserted.rowcount)
```

출력:
```
넣은 줄 수: 3

```

### [14] markdown {}

**결과 읽기** — 출력 줄 `넣은 줄 수: 3`이 보입니다.
결과 객체의 속성 `rowcount`는 그 SQL 글이 바꾼 줄 수입니다.
블록이 오류 없이 끝나, 이름 공간·표·세 줄을 한꺼번에 확정했습니다.

다음 셀은 연결을 다시 빌려, 표의 줄을 모두 읽습니다.
문장 `ORDER BY id`는 번호 차례로 줄을 고르게 합니다.
메서드 `fetchall`은 결과의 줄을 모두 목록으로 꺼냅니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.196460Z', 'iopub.status.busy': '2026-09-29T21:08:36.196409Z', 'iopub.status.idle': '2026-09-29T21:08:36.198829Z', 'shell.execute_reply': '2026-09-29T21:08:36.198490Z'}}

```python
# 표의 줄을 번호 차례로 모두 읽어, 줄 수와 줄 목록을 봅니다
async with engine.connect() as conn:
    result = await conn.execute(text("SELECT id, question FROM ch31_async.requests ORDER BY id"))
    rows = result.fetchall()
print("줄 수:", len(rows))
print("줄 목록:", rows)
```

출력:
```
줄 수: 3
줄 목록: [(1, '환불'), (2, '배송'), (3, '결제')]

```

### [16] markdown {}

**결과 읽기** — 출력 줄 `줄 수: 3`과 `줄 목록: [(1, '환불'), (2, '배송'), (3, '결제')]`이 보입니다.
줄 하나는 칸 둘(`id`·`question`)을 가진 튜플 모양으로 찍힙니다.
문의 세 줄이 번호 차례로 표에 있습니다.

## 4. 문의 하나를 읽는 함수

이번에는 SQL 글을 먼저 객체로 만들어 변수에 담아 둡니다.
글 `:seconds`와 `:id`는 값이 들어갈 자리이고, Ch 4 03절의 물음표 자리와 같은 일을 합니다.
값은 실행할 때 SQL 글과 따로 넘깁니다.
빈칸이 있는 신청서를 먼저 만들어 두고, 이름은 낼 때 따로 적는 것과 비슷합니다.

PostgreSQL 함수 `pg_sleep`은 정한 초만큼 기다린 뒤 다음으로 넘어갑니다.
이 절은 오래 걸리는 조회를 흉내 내려고, 줄을 고르기 전에 이 함수로 기다리게 합니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.199322Z', 'iopub.status.busy': '2026-09-29T21:08:36.199274Z', 'iopub.status.idle': '2026-09-29T21:08:36.200917Z', 'shell.execute_reply': '2026-09-29T21:08:36.200684Z'}}

```python
# 기다릴 초와 문의 번호가 들어갈 자리를 둔 SQL 글을 객체로 만듭니다
# pg_sleep(초)은 PostgreSQL이 그 초만큼 기다린 뒤 줄을 고르게 합니다(오래 걸리는 조회를 흉내 냄)
read_sql = text("SELECT question FROM ch31_async.requests, pg_sleep(:seconds) WHERE id = :id")
print("객체의 종류:", type(read_sql).__name__)
print("SQL 글:", read_sql)
```

출력:
```
객체의 종류: TextClause
SQL 글: SELECT question FROM ch31_async.requests, pg_sleep(:seconds) WHERE id = :id

```

### [18] markdown {}

**결과 읽기** — 출력 줄 `객체의 종류: TextClause`가 보입니다.
라벨 `SQL 글:` 뒤에는 자리 `:seconds`와 `:id`가 그대로 남아 있습니다.
이 셀은 객체를 만들기만 했고, 서버에는 아직 아무것도 보내지 않았습니다.

다음 셀의 함수 `read_question`은 문의 번호와 기다릴 초를 받아, 그 문의의 질문 글을 내놓습니다.
함수 안에서 연결을 하나 빌리고, 블록이 끝나면 풀에 다시 넣습니다.
목록 `step_log`에는 시작과 끝을 차례로 적어, 뒤에서 두 실행의 차례를 봅니다.
정의 줄의 `async def`는 Ch 2 12절의 비동기 함수입니다.

메서드 `execute`의 둘째 인자는 자리 이름을 키로 한 딕셔너리입니다.
메서드 `scalar_one`은 결과가 꼭 한 줄일 때 그 줄의 첫 칸 값을 꺼냅니다.
줄이 없거나 둘 이상이면 오류를 낸다고 문서에 적혀 있고, 이번에 실행하지 않았습니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.201485Z', 'iopub.status.busy': '2026-09-29T21:08:36.201439Z', 'iopub.status.idle': '2026-09-29T21:08:36.203466Z', 'shell.execute_reply': '2026-09-29T21:08:36.203100Z'}}

```python
# 문의 번호 하나로 표에서 질문을 읽어 내놓습니다(연결 하나를 빌렸다가 풀에 다시 넣습니다)
async def read_question(item_id, wait_seconds):
    step_log.append(("시작", item_id))
    async with engine.connect() as conn:
        # 자리 이름을 키로 한 딕셔너리로, 자리에 넣을 값을 SQL 글과 따로 넘깁니다
        values = {"id": item_id, "seconds": wait_seconds}
        result = await conn.execute(read_sql, values)
        question = result.scalar_one()
    step_log.append(("끝", item_id))
    return question
```

출력:
```

```

### [20] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
목록 `step_log`는 다음 셀에서 만듭니다.
함수는 불릴 때 그 목록을 찾아 기록을 더합니다.

다음 셀은 기록 목록을 빈 목록으로 만들고, 0초로 문의 1번을 읽어 봅니다.
기다릴 초로 0을 넣으면 서버가 기다리지 않고 바로 줄을 고릅니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.204022Z', 'iopub.status.busy': '2026-09-29T21:08:36.203979Z', 'iopub.status.idle': '2026-09-29T21:08:36.206274Z', 'shell.execute_reply': '2026-09-29T21:08:36.205966Z'}}

```python
# 기록 목록을 비우고, 기다리지 않게 0초로 문의 1번을 읽어 봅니다
step_log = []
first_question = await read_question(1, 0)
print("받은 값:", first_question)
print("적힌 기록:", step_log)
print("풀에 쉬고 있는 연결 수:", engine.pool.checkedin())
```

출력:
```
받은 값: 환불
적힌 기록: [('시작', 1), ('끝', 1)]
풀에 쉬고 있는 연결 수: 1

```

### [22] markdown {}

**결과 읽기** — 출력 줄 `받은 값: 환불`과 `적힌 기록: [('시작', 1), ('끝', 1)]`이 보입니다.
출력 줄 `풀에 쉬고 있는 연결 수: 1`은 2절 끝과 같은 수입니다.
풀이 새 연결을 만들지 않고, 쉬고 있던 연결 하나를 빌려 주었다가 다시 받았습니다.

## 5. 가설과 두 실행에 쓸 값

이제 실험을 합니다.
문의 셋을 0.15초씩 기다리게 해서 읽고, 걸린 시간을 잽니다.
실행 1은 await 줄 셋으로 문의를 하나씩 차례로 기다립니다.
실행 2에서 바꾸는 것은 기다리는 방법 하나입니다.
같은 문의 셋을 Ch 2 12절의 `gather()`에 함께 넣어 기다립니다.

실행 전에 가설을 세웁니다.
차례로 기다리면 기다림이 이어져, 걸린 시간이 적어도 0.15초의 세 배가 될 것입니다.
함께 기다리면 연결 셋이 서버의 답을 같은 때에 기다려, 걸린 시간이 그보다 짧을 것입니다.
받은 값 목록은 두 실행이 같을 것입니다.

다음 셀은 두 실행에 똑같이 쓸 값을 정합니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.206756Z', 'iopub.status.busy': '2026-09-29T21:08:36.206714Z', 'iopub.status.idle': '2026-09-29T21:08:36.208513Z', 'shell.execute_reply': '2026-09-29T21:08:36.208184Z'}}

```python
# 두 실행에 똑같이 쓸 값을 정합니다(문의마다 서버가 기다릴 초와 문의 수)
wait_seconds = 0.15
question_count = 3
# pg_sleep은 적어도 정한 초만큼 기다리므로, 차례로 기다리면 이 값보다 짧을 수 없습니다
least_seconds = round(wait_seconds * question_count, 2)
print("문의마다 기다릴 초:", wait_seconds)
print("차례로 기다리면 적어도 걸릴 초:", least_seconds)
```

출력:
```
문의마다 기다릴 초: 0.15
차례로 기다리면 적어도 걸릴 초: 0.45

```

### [24] markdown {}

**결과 읽기** — 출력 줄 `문의마다 기다릴 초: 0.15`와 `차례로 기다리면 적어도 걸릴 초: 0.45`가 보입니다.
PostgreSQL 문서는 함수 `pg_sleep`이 적어도 정한 초만큼 기다린다고 적습니다.
그래서 차례로 기다린 실행 1은 0.45초보다 짧을 수 없습니다.

## 6. 실행 1: 차례로 기다리기

두 실행을 같은 조건에서 시작하려고, 실행마다 먼저 풀을 비웁니다.
메서드 `engine.dispose()`는 풀에 쉬고 있는 연결을 모두 닫고, 빈 풀로 다시 시작합니다.
엔진을 다 쓴 뒤에도 부르는 메서드이고, await로 기다립니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.208991Z', 'iopub.status.busy': '2026-09-29T21:08:36.208947Z', 'iopub.status.idle': '2026-09-29T21:08:36.211705Z', 'shell.execute_reply': '2026-09-29T21:08:36.211348Z'}}

```python
# 풀에 쉬고 있는 연결을 모두 닫아 빈 풀로 만들고, 기록 목록을 비웁니다
await engine.dispose()
step_log = []
print("풀에 쉬고 있는 연결 수:", engine.pool.checkedin())
print("적힌 기록:", step_log)
```

출력:
```
풀에 쉬고 있는 연결 수: 0
적힌 기록: []

```

### [26] markdown {}

**결과 읽기** — 출력 줄 `풀에 쉬고 있는 연결 수: 0`과 `적힌 기록: []`이 보입니다.
풀과 기록 목록이 모두 비었습니다.

다음 셀은 시작 시각을 적고, await 줄 셋으로 문의 1·2·3번을 차례로 읽은 뒤 끝 시각을 적습니다.
함수 `time.perf_counter`로 걸린 초를 셈하는 방법은 Ch 2 12절과 같습니다.
걸린 초는 함수 `round`로 소수 둘째 자리까지 남깁니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.212206Z', 'iopub.status.busy': '2026-09-29T21:08:36.212160Z', 'iopub.status.idle': '2026-09-29T21:08:36.696237Z', 'shell.execute_reply': '2026-09-29T21:08:36.695413Z'}}

```python
# 실행 1: 문의 셋을 await 줄로 하나씩 차례로 기다리고, 받은 값 목록과 걸린 시간을 봅니다
start_time = time.perf_counter()
first = await read_question(1, wait_seconds)
second = await read_question(2, wait_seconds)
third = await read_question(3, wait_seconds)
elapsed = time.perf_counter() - start_time
one_by_one = [first, second, third]
one_by_one_seconds = round(elapsed, 2)
print("받은 값 목록:", one_by_one)
print("걸린 시간(초):", one_by_one_seconds)
```

출력:
```
받은 값 목록: ['환불', '배송', '결제']
걸린 시간(초): 0.48

```

### [28] markdown {}

**결과 읽기** — 출력 줄 `받은 값 목록: ['환불', '배송', '결제']`이 보입니다.
문의 번호 차례대로 질문 글을 받았습니다.

이번 실행에서는 `걸린 시간(초): 0.48`이었습니다.
5절에서 셈한 0.45초보다 조금 깁니다.
초 값은 실행할 때마다 조금씩 달라져, 결론에는 쓰지 않습니다.

다음 셀은 기록 목록의 앞 세 개와 기록 수, 끝난 뒤 풀에 쉬고 있는 연결 수를 봅니다.
슬라이싱 `[:3]`은 목록의 앞에서 세 개를 꺼냅니다.

### [29] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.698143Z', 'iopub.status.busy': '2026-09-29T21:08:36.697989Z', 'iopub.status.idle': '2026-09-29T21:08:36.702389Z', 'shell.execute_reply': '2026-09-29T21:08:36.701326Z'}}

```python
# 실행 1의 기록 앞 세 개와 기록 수, 끝난 뒤 풀에 쉬고 있는 연결 수를 봅니다
one_by_one_idle = engine.pool.checkedin()
print("적힌 기록 앞 세 개:", step_log[:3])
print("적힌 기록 수:", len(step_log))
print("풀에 쉬고 있는 연결 수:", one_by_one_idle)
```

출력:
```
적힌 기록 앞 세 개: [('시작', 1), ('끝', 1), ('시작', 2)]
적힌 기록 수: 6
풀에 쉬고 있는 연결 수: 1

```

### [30] markdown {}

**결과 읽기** — 출력 줄 `적힌 기록 앞 세 개: [('시작', 1), ('끝', 1), ('시작', 2)]`가 보입니다.
문의 1번이 끝난 뒤에야 2번이 시작했습니다.
출력 줄 `적힌 기록 수: 6`은 문의 셋마다 시작과 끝이 하나씩 적혔다는 뜻입니다.
출력 줄 `풀에 쉬고 있는 연결 수: 1`은 연결 하나를 세 번 빌리고 다시 넣었다는 뜻입니다.

## 7. 실행 2: 함께 기다리기

실행 1과 같이 풀을 비우고 기록 목록을 비웁니다.

### [31] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.704155Z', 'iopub.status.busy': '2026-09-29T21:08:36.703995Z', 'iopub.status.idle': '2026-09-29T21:08:36.709734Z', 'shell.execute_reply': '2026-09-29T21:08:36.709171Z'}}

```python
# 풀에 쉬고 있는 연결을 모두 닫아 빈 풀로 만들고, 기록 목록을 비웁니다
await engine.dispose()
step_log = []
print("풀에 쉬고 있는 연결 수:", engine.pool.checkedin())
print("적힌 기록:", step_log)
```

출력:
```
풀에 쉬고 있는 연결 수: 0
적힌 기록: []

```

### [32] markdown {}

**결과 읽기** — 출력 줄 `풀에 쉬고 있는 연결 수: 0`과 `적힌 기록: []`이 보입니다.
실행 1을 시작할 때와 같은 조건입니다.

다음 셀은 함수 `read_question`을 await 없이 불러, 코루틴 셋을 만들기만 합니다.
Ch 2 12절에서 본 것처럼, 코루틴은 만들어도 아직 본문을 실행하지 않습니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.711195Z', 'iopub.status.busy': '2026-09-29T21:08:36.711049Z', 'iopub.status.idle': '2026-09-29T21:08:36.714011Z', 'shell.execute_reply': '2026-09-29T21:08:36.713467Z'}}

```python
# 실행 2: 같은 문의 셋의 코루틴을 await 없이 만들기만 하고, 기록 목록을 봅니다
first_waiting = read_question(1, wait_seconds)
second_waiting = read_question(2, wait_seconds)
third_waiting = read_question(3, wait_seconds)
print("만든 값의 종류:", type(first_waiting).__name__)
print("적힌 기록:", step_log)
```

출력:
```
만든 값의 종류: coroutine
적힌 기록: []

```

### [34] markdown {}

**결과 읽기** — 출력 줄 `만든 값의 종류: coroutine`과 `적힌 기록: []`이 보입니다.
코루틴 셋을 만들었지만 어느 것도 아직 시작하지 않아, 기록 목록이 비어 있습니다.

다음 셀은 코루틴 셋을 `asyncio.gather`에 함께 넣고 await로 기다립니다.
함수 `gather`는 넣은 코루틴을 함께 진행하고, 모두 끝나면 넣은 차례대로 받은 값 목록을 만듭니다.
Ch 2 12절처럼 코루틴을 인자로 하나씩 적어 넣습니다.

### [35] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.715013Z', 'iopub.status.busy': '2026-09-29T21:08:36.714927Z', 'iopub.status.idle': '2026-09-29T21:08:36.908806Z', 'shell.execute_reply': '2026-09-29T21:08:36.907998Z'}}

```python
# gather()에 코루틴 셋을 함께 넣어 기다리고, 받은 값 목록과 걸린 시간을 봅니다
start_time = time.perf_counter()
together = await asyncio.gather(first_waiting, second_waiting, third_waiting)
elapsed = time.perf_counter() - start_time
together_seconds = round(elapsed, 2)
print("받은 값 목록:", together)
print("걸린 시간(초):", together_seconds)
```

출력:
```
받은 값 목록: ['환불', '배송', '결제']
걸린 시간(초): 0.19

```

### [36] markdown {}

**결과 읽기** — 출력 줄 `받은 값 목록: ['환불', '배송', '결제']`이 보입니다.
실행 1과 같은 목록이고, 차례도 넣은 차례 그대로입니다.

이번 실행에서는 `걸린 시간(초): 0.19`였습니다.
두 실행의 초는 8절에서 한 표에 놓고 봅니다.

다음 셀은 실행 1과 같은 모양으로 기록과 풀을 봅니다.

### [37] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.910456Z', 'iopub.status.busy': '2026-09-29T21:08:36.910297Z', 'iopub.status.idle': '2026-09-29T21:08:36.914417Z', 'shell.execute_reply': '2026-09-29T21:08:36.913480Z'}}

```python
# 실행 2의 기록 앞 세 개와 기록 수, 끝난 뒤 풀에 쉬고 있는 연결 수를 봅니다
together_idle = engine.pool.checkedin()
print("적힌 기록 앞 세 개:", step_log[:3])
print("적힌 기록 수:", len(step_log))
print("풀에 쉬고 있는 연결 수:", together_idle)
```

출력:
```
적힌 기록 앞 세 개: [('시작', 1), ('시작', 2), ('시작', 3)]
적힌 기록 수: 6
풀에 쉬고 있는 연결 수: 3

```

### [38] markdown {}

**결과 읽기** — 출력 줄 `적힌 기록 앞 세 개: [('시작', 1), ('시작', 2), ('시작', 3)]`이 보입니다.
셋 가운데 어느 것도 끝나기 전에 셋이 모두 시작했습니다.
출력 줄 `적힌 기록 수: 6`은 실행 1과 같습니다.
출력 줄 `풀에 쉬고 있는 연결 수: 3`은 실행 1의 하나와 다릅니다.
셋이 같은 때에 연결을 빌려야 해서, 풀이 연결 셋을 만들었습니다.

앞 셋 다음에 어느 문의가 먼저 끝나는지는 실행할 때마다 달라질 수 있습니다.
그래서 기록은 앞 세 개만 출력했습니다.

## 8. 두 실행 견주기

다음 셀은 두 실행의 값을 한 줄씩 출력합니다.

### [39] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.916089Z', 'iopub.status.busy': '2026-09-29T21:08:36.915933Z', 'iopub.status.idle': '2026-09-29T21:08:36.919052Z', 'shell.execute_reply': '2026-09-29T21:08:36.918408Z'}}

```python
# 두 실행을 한 줄씩 견줍니다(걸린 시간은 실행할 때마다 조금씩 달라집니다)
print("실행 | 받은 값 목록 | 풀에 쉬고 있는 연결 수 | 걸린 시간(초)")
print("차례로 |", one_by_one, "|", one_by_one_idle, "|", one_by_one_seconds)
print("함께 |", together, "|", together_idle, "|", together_seconds)
```

출력:
```
실행 | 받은 값 목록 | 풀에 쉬고 있는 연결 수 | 걸린 시간(초)
차례로 | ['환불', '배송', '결제'] | 1 | 0.48
함께 | ['환불', '배송', '결제'] | 3 | 0.19

```

### [40] markdown {}

**결과 읽기** — 라벨 줄 `실행 | 받은 값 목록 | 풀에 쉬고 있는 연결 수 | 걸린 시간(초)` 아래 두 줄이 두 실행입니다.
받은 값 목록은 두 줄이 같고, 풀에 쉬고 있는 연결 수는 `1`과 `3`입니다.

이번 실행에서는 걸린 시간이 차례로 0.48초, 함께 0.19초였습니다.
다시 실행하면 두 초 값은 조금씩 달라집니다.

다음 셀은 두 가지를 참·거짓으로 봅니다.
받은 값 목록이 같은지와, 함께 기다린 시간이 더 짧은지입니다.

### [41] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.920373Z', 'iopub.status.busy': '2026-09-29T21:08:36.920253Z', 'iopub.status.idle': '2026-09-29T21:08:36.923701Z', 'shell.execute_reply': '2026-09-29T21:08:36.922637Z'}}

```python
# 두 실행의 받은 값이 같은지와, 함께 기다린 쪽이 먼저 끝났는지를 참·거짓으로 봅니다
same_answers = one_by_one == together
together_faster = together_seconds < one_by_one_seconds
print("받은 값 목록이 같은가:", same_answers)
print("함께 기다린 시간이 더 짧은가:", together_faster)
```

출력:
```
받은 값 목록이 같은가: True
함께 기다린 시간이 더 짧은가: True

```

### [42] markdown {}

**결과 읽기** — 출력 줄 `받은 값 목록이 같은가: True`와 `함께 기다린 시간이 더 짧은가: True`가 보입니다.
받은 값은 같았고, 함께 기다린 실행이 먼저 끝났습니다.
가설과 맞는 결과입니다.

둘째 줄은 걸린 초에서 나온 참·거짓입니다.
교재를 만들며 새 커널로 두 번, 같은 커널에서 세 번, 노트북 밖에서 여섯 번 실행했을 때 모두 참이었습니다.
서버와 컴퓨터가 다르면 초 값은 달라집니다.

## 9. 정리: 이름 공간 지우기

다음 셀은 이름 공간 `ch31_async`를 안의 표까지 지우고, 엔진의 풀도 비웁니다.
PostgreSQL 함수 `to_regnamespace`는 그 이름 공간이 있으면 이름을, 없으면 빈 값(NULL)을 내놓습니다.
파이썬에서는 빈 값을 `None`으로 받습니다.

### [43] code {'execution': {'iopub.execute_input': '2026-09-29T21:08:36.925104Z', 'iopub.status.busy': '2026-09-29T21:08:36.924989Z', 'iopub.status.idle': '2026-09-29T21:08:36.937986Z', 'shell.execute_reply': '2026-09-29T21:08:36.937413Z'}}

```python
# 끝 정리: 이름 공간 ch31_async를 안의 표까지 지우고, 남았는지 물은 뒤 풀을 비웁니다
async with engine.begin() as conn:
    await conn.execute(text("DROP SCHEMA ch31_async CASCADE"))
    result = await conn.execute(text("SELECT to_regnamespace('ch31_async')"))
    left_namespace = result.scalar_one()
await engine.dispose()
print("남은 이름 공간:", left_namespace)
print("풀에 쉬고 있는 연결 수:", engine.pool.checkedin())
```

출력:
```
남은 이름 공간: None
풀에 쉬고 있는 연결 수: 0

```

### [44] markdown {}

**결과 읽기** — 출력 줄 `남은 이름 공간: None`과 `풀에 쉬고 있는 연결 수: 0`이 보입니다.
이름 공간이 지워졌고, 풀의 연결도 모두 닫혔습니다.
이 노트북을 처음부터 다시 실행하면, 3절이 이름 공간을 새로 만들어 같은 출력이 나옵니다.

## 정리

1. 비동기 엔진은 연결 풀을 두었고, `async with`로 빌린 연결은 블록이 끝나자 서버와 끊기지 않은 채 풀에 다시 들어갔습니다.
2. 차례로 기다린 실행은 연결 하나를 세 번 빌렸고, `gather()`로 함께 기다린 실행은 셋이 모두 시작한 뒤 연결 셋을 빌렸습니다.
3. 받은 값 목록은 두 실행이 같았고, 함께 기다린 실행이 차례로 기다린 실행보다 먼저 끝났습니다.

02절에서는 두 계좌의 잔액을 바꾸는 이체에서, 바꾼 내용을 따로 확정할 때와 한 블록으로 확정할 때를 견줍니다.

## 그림

### 01-1-엔진과-연결-풀.mmd

```mermaid
flowchart TB
  %% classes
  url["접속 글<br>postgresql+asyncpg<br>127.0.0.1:55431/ch31_lab"]:::tool
  eng["create_async_engine<br>pool_size=3<br>max_overflow=0"]:::flow
  pool["엔진의 연결 풀<br>AsyncAdaptedQueuePool<br>풀에 둘 연결 수 셋"]
  conn["async with<br>engine.connect()<br>연결 하나를 빌림"]:::flow
  pg["PostgreSQL 서버<br>데이터베이스 ch31_lab"]
  seen["블록 안 빌려 간 연결 하나<br>블록 밖 쉬고 있는 연결 하나"]:::measure
  url --> eng --> pool --> conn --> pg
  conn --> seen
```

엔진은 연결 풀을 두고, async with로 빌린 연결은 블록이 끝나자 서버와 끊기지 않은 채 풀에 쉬는 연결 하나로 남았습니다.

### 01-2-이름-공간-준비와-확정.mmd

```mermaid
flowchart TB
  %% classes
  beg["async with engine.begin()<br>연결 하나를 빌림"]:::flow
  subgraph blk["begin 블록 안 · 한 묶음"]
    direction TB
    s1["DROP SCHEMA IF EXISTS<br>ch31_async CASCADE"]:::flow
    s2["CREATE SCHEMA<br>ch31_async<br>CREATE TABLE requests"]:::flow
    s3["INSERT로<br>문의 세 줄을 넣음"]:::flow
    s1 --> s2 --> s3
  end
  ok["블록이 오류 없이 끝남<br>바꾼 내용을 확정"]
  rows["표 requests 문의 세 줄<br>환불 · 배송 · 결제"]:::tool
  cnt["넣은 줄 셋<br>다시 읽은 줄 셋"]:::measure
  beg --> blk --> ok --> rows --> cnt
```

begin 블록 안의 SQL 글 넷을 한 묶음으로 실행하자, 블록 끝에서 확정되어 표에 문의 세 줄이 남았습니다.

### 01-3-연결-하나로-차례로-기다린-실행-1.mmd

```mermaid
flowchart TB
  %% classes
  start["빈 풀에서 시작<br>쉬고 있는 연결 없음"]:::measure
  q1["문의 1 · 연결을 빌림<br>0.15초 기다림<br>풀에 다시 넣음"]:::flow
  q2["문의 2 · 같은 연결을 빌림<br>0.15초 기다림<br>풀에 다시 넣음"]:::flow
  q3["문의 3 · 같은 연결을 빌림<br>0.15초 기다림<br>풀에 다시 넣음"]:::flow
  done["기록 앞 셋<br>시작 1 · 끝 1 · 시작 2<br>쉬고 있는 연결 하나"]:::measure
  start --> q1 --> q2 --> q3 --> done
```

차례로 기다린 실행 1은 문의 하나가 끝난 뒤에야 다음 문의를 시작했고, 연결 하나를 세 번 빌렸다가 다시 넣었습니다.

### 01-4-차례로와-함께-견주기.mmd

```mermaid
flowchart TB
  %% classes
  same["두 실행 같음<br>함수 read_question<br>문의 셋 · 문의마다 0.15초"]
  subgraph r1["실행 1 · 차례로"]
    direction TB
    m1["await 줄 셋"]:::flow
    o1["기록 앞 셋<br>시작 1 · 끝 1 · 시작 2<br>쉬고 있는 연결 하나"]:::measure
    m1 --> o1
  end
  subgraph r2["실행 2 · 함께"]
    direction TB
    m2["gather에 코루틴 셋"]:::flow
    o2["기록 앞 셋<br>시작 1 · 시작 2 · 시작 3<br>쉬고 있는 연결 셋"]:::measure
    m2 --> o2
  end
  res["받은 값 목록 같음 True<br>함께 기다린 시간이<br>더 짧음 True"]:::measure
  same --> r1
  same --> r2
  r1 --> res
  r2 --> res
```

기다리는 방법 하나만 바꾸자, 셋이 모두 시작한 뒤 연결 셋을 빌렸고 받은 값은 같은 채 먼저 끝났습니다.

### 01-5-불이-하나-켜진-판과-셋-켜진-판.prompt.md

# 01-5-불이-하나-켜진-판과-셋-켜진-판 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 옛 전화 교환대의 판 하나를 떠올려 봅니다. 판에는 선을 꽂는 자리가 셋 있고, 자리마다 위에 작은 불이 달려 있습니다. … 같은 판 둘을 나란히 놓습니다. 왼쪽 판에는 선 하나만 꽂혀 불 하나가 켜져 있고, 두 자리는 비어 있습니다. 오른쪽 판에는 세 자리 모두 선이 꽂혀 불 셋이 켜져 있습니다. 판이 엔진의 연결 풀이고, 꽂는 자리 셋이 인자 `pool_size=3`입니다. 꽂힌 선 하나가 연결 하나입니다.

구성 요소와 배치: **같은 판 정확히 둘**(= 연결 풀, 실행 1·실행 2가 끝난 모습) · **판마다 꽂는 자리 셋과 그 위 불 셋**(= `pool_size=3`) · **왼쪽 판에 꽂힌 선 하나·켜진 불 하나**(= 실행 1 뒤 쉬고 있는 연결 수 `1`) · **오른쪽 판에 꽂힌 선 셋·켜진 불 셋**(= 실행 2 뒤 `3`). 비유 계열 **「전화 교환대」**(챕터 리드 결정 12 — 01절이 엶, 사람 없이 판·꽂는 자리·선·불빛만). 금지 소품(화물 열차·번호판·오르골·종이띠·도킹 포트·정거장·온실·모종판·예인선·밧줄·홈통·물방울·도미노·체스판·즉석사진·세탁기·승강 상자·전표·가마·발자국·쟁반·서랍·바구니·저울·공항 검사·안내 데스크 + 옛 원고 식당·은행 창구·창고) 없음. 사람·손·글자·숫자·화살표·전화기·헤드셋·화면 없음.

시선 순서: 왼쪽 판의 켜진 불 하나와 꽂힌 선 하나 → 오른쪽 판의 켜진 불 셋과 꽂힌 선 셋.

검수 기준: 그림만 보고 「같은 판 둘 가운데 왼쪽은 선 하나·불 하나, 오른쪽은 선 셋·불 셋」이 세어서 읽히는가. 판이 정확히 둘, 판마다 자리 셋·불 셋인가. 꽂히지 않은 선이 없는가. 글자·숫자·사람·화살표가 없는가.

## 프롬프트 (1차, 탈락)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. Close-up view, two identical old wooden telephone switchboard panels stand side by side and fill almost the whole frame. Each panel has exactly three large round jacks in one horizontal row, and one small round lamp directly above each jack. Left panel: exactly one black patch cord plugged into its left jack, the lamp above it glowing warm yellow; the other two jacks are empty and their lamps are dark gray. Right panel: exactly three black patch cords plugged into all three jacks, all three lamps glowing warm yellow. The cords hang down in loose curves below the panels. No people, no hands, no arrows, no telephones, no headsets, no screens.
```

## 프롬프트 (2차, 채택 — 재생성 1회)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. Close-up view, two identical old wooden telephone switchboard panels stand side by side and fill almost the whole frame. Each panel has exactly three large round jacks in one horizontal row, and one small round lamp directly above each jack. Left panel: exactly one short black cord is plugged into its left jack and hangs straight down, the lamp above it glowing warm yellow; the other two jacks are empty and their lamps are dark gray. Right panel: exactly three short black cords are plugged into all three jacks and hang straight down side by side, all three lamps glowing warm yellow. Every cord starts at a jack and ends just below its panel. Only these four cords in the picture, no loose cords, no loops, nothing behind the panels. No people, no hands, no arrows, no telephones, no headsets, no screens.
```

## 상태

- 2026-09-29 · `generate_image` 두 번, `params` = `{"model":"nano_banana_pro","prompt":…,"aspect_ratio":"16:9","resolution":"2k","use_unlim":false,"count":1}`. `generate_image` 응답 모델 `nano_banana_pro`, **`jobs_wait` 응답 모델 표시 `nano_banana_2`**(Ch 25~30과 같은 표시, 거래 표시는 「Nano Banana Pro」 — 기록만).
- 생성 전 잔액 **2265**, 바로 앞 거래 2026-09-29T12:29:22.775608Z는 Ch 30 10절 몫(이 절 아님).
- **1차 job `3d304f8c-ae4f-4151-9dd1-9f8356fe351f` 탈락** — 거래 2026-09-29T15:57:33.157368Z 「Nano Banana Pro −2」. 원본 `a1d4f850…`(2752 × 1536, RGB). 판 둘·자리 셋·불 셋·켜진 불 하나 ↔ 셋·꽂힌 선 하나 ↔ 셋은 맞았으나, **두 판 아래로 판 뒤에서 나온 듯한 검은 선 고리가 여럿 늘어져** 「꽂힌 선 하나」를 세어 읽기 어려움(꽂히지 않은 선처럼 보임).
- **2차 job `55814eca-21ec-4435-9945-4f45614baf2a` 채택** — 거래 2026-09-29T15:58:41.127217Z 「Nano Banana Pro −2」. 원본 `67c67b5421c2760db78aecfc974a419f4d658c447c6907c489cf0e033cc3416b`(2752 × 1536, **RGBA** → RGB로 바꿔 저장). **이 절 몫 거래 두 줄, 4크레딧**(잔액 2265 → 2261), 재생성 1회.
- **그림에서 확인한 것(그림 읽기·alt에 반영)**: 흰 바탕에 같은 모양의 갈색 나무 판 **둘**이 나란히 · 판마다 위에 작은 둥근 불 **셋**, 아래에 금색 테두리의 둥근 꽂는 자리 **셋**이 한 줄 · 왼쪽 판: 왼쪽 자리에만 검은 선 **하나**가 꽂혀 곧게 아래로, 그 위 불 **하나**만 노랑, 나머지 자리 둘은 비고 불 둘은 회색 · 오른쪽 판: 세 자리 모두 검은 선(모두 **셋**)이 꽂혀 곧게 아래로, 불 **셋** 모두 노랑. 선은 모두 넷이고 꽂히지 않은 선 없음. 글자·숫자·사람·손·화살표·전화기·화면 없음.
- 검수: 「왼쪽 판은 선 하나·불 하나, 오른쪽 판은 선 셋·불 셋」이 그림만으로 세어서 읽힘 → 채택. **그림과 프롬프트의 차이**: 두 판의 바깥 모서리(왼쪽 판의 왼쪽 끝·오른쪽 판의 오른쪽 끝)가 그림 가장자리에서 조금 잘림 · 위아래 흰 여백이 거의 흰 가로줄 172/614(약 4분의 1 — 판이 가로로 넓어 위아래가 남음, 강사 확인) · 판 모양이 옛 교환대보다 벽에 거는 나무 판에 가까움(그림 읽기는 「나무 판」으로 적음).
- 저장: 기기 셸에서 결과 URL을 `curl`로 받아(`/tmp/ch31-01/illu/illu-2-orig.png`) `UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pillow`로 RGB·폭 1100px(LANCZOS)로 줄여 `figures/01-5-불이-하나-켜진-판과-셋-켜진-판.png`(1100 × 614, `98fad365a4695b74b956d8e72fe949b29e45827cf363f2a48b93b7135a99612d`)로 저장했습니다.
- 결과 URL을 한 번 더 받아(`illu-2-again.png`, 원본과 해시 같음) 같은 폭으로 줄인 그림과 저장 PNG를 픽셀 대조했습니다(`ImageChops.difference` bbox `None`, 최대 차이 0). 저장 PNG와 같은 사본(`.cache/ch31-01-view/illu-2-1100.png`)을 직접 열어 개수를 세고 그림 읽기를 썼습니다.

