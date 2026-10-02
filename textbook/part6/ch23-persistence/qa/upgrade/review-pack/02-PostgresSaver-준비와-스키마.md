# 02-PostgresSaver-준비와-스키마

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 1h | 실습 1.5h | 코드 notebooks/02-PostgresSaver-준비와-스키마.ipynb | 새 용어 3 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>PostgreSQL 체크포인터를 표 만들기 전에 쓰면 받는 오류와, 메서드 <code>setup()</code> 뒤의 결과를 견줄 수 있습니다.</li>
<li>메서드 <code>setup()</code>이 만든 표 넷과 표 만들기 기록을 SQL로 읽을 수 있습니다.</li>
<li>체크포인트가 표 <code>checkpoints</code>에 스레드마다 한 줄씩 쌓이는 것을 셀 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p><a href="01-체크포인터와-스레드.html">01절</a>의 체크포인터 <code>InMemorySaver</code>는 이 프로그램의 메모리에만 저장했습니다. 체크포인트를 프로그램 밖에 남기려면, 파일이나 데이터베이스에 써야 합니다. 이 절은 PostgreSQL 데이터베이스의 표에 쓰는 체크포인터 <code>PostgresSaver</code>를 씁니다. 이 체크포인터는 쓰기 전에, 체크포인트를 담을 표를 먼저 만들어야 합니다.</p><p>표를 만들지 않고 실행하면 무엇이 일어나는지가 이 절의 Before입니다. 표를 만든 뒤 같은 입력으로 실행하는 것이 After입니다. 제목의 마지막 말은 체크포인터가 쓰는 표들의 구조, 곧 표 이름과 표의 칸을 가리킵니다. SQL 낱말 <code>SCHEMA</code>는 같은 영어 낱말이지만, 이 절은 그것을 이름 공간이라고 부르고 제목의 말과 나눠 씁니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href="../../part3/ch12-retrieval-tuning/02-pgvector와-HNSW.html">Ch 12 02절</a>에서는 패키지 psycopg로 PostgreSQL에 붙어, 메서드 <code>execute</code>와 <code>fetchone</code>으로 문장을 실행했습니다. 값은 자리표시자 <code>%s</code>로 넘겼고, 오류는 <code>except psycopg.Error as error</code>로 받았습니다. 이 절도 같은 접속 글과 같은 Docker 컨테이너를 씁니다.</p><p><a href="../../part1/ch04-data-tools/03-SQL로-조회-함수-만들기.html">Ch 4 03절</a>에서는 SQLite 표를 <code>SELECT … WHERE … ORDER BY</code>로 조회했습니다. 이 절은 같은 모양의 문장으로, PostgreSQL이 보여 주는 표 목록과 칸 목록을 읽습니다. 오류를 그 셀에서만 받는 <code>try</code>·<code>except</code>는 <a href="../../part1/ch02-python/05-파일과-예외.html">Ch 2 05절</a>에서 배웠습니다.</p><p><a href="01-체크포인터와-스레드.html">01절</a>에서는 체크포인터를 붙인 그래프로 스레드 <code>customer-a</code>의 합계를 3에서 7로 이어 갔습니다. 체크포인트는 실행 한 번에 셋씩, 모두 여섯이 쌓였습니다. 이 절은 같은 상태 형식과 노드로 그래프를 만들고, 체크포인터만 바꿉니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>01절의 체스판과 즉석사진을 떠올립니다. 사진을 오래 남기려면, 사진을 꽂아 둘 사진첩이 있어야 합니다. 그런데 새로 산 사진첩에는 비닐 속지가 끼워져 있지 않습니다. 속지가 없으면 사진을 찍고도 꽂을 자리가 없습니다.</p><p>속지를 먼저 끼워 두면, 그때부터 사진을 꽂을 수 있습니다. 데이터베이스의 이름 공간이 사진첩 한 권이고, 표가 속지입니다. 메서드 <code>setup()</code>은 빈 사진첩에 속지를 끼우는 일이고, 이 절에서는 표 넷을 한꺼번에 만듭니다. 사진 한 장이 표 <code>checkpoints</code>의 한 줄, 곧 체크포인트 하나입니다. 01절의 메모리 체크포인터는 사진첩까지 카메라가 들고 있었다면, 이 절은 사진첩을 카메라 밖에 둡니다.</p>
{{img:02-5-속지를-끼운-사진첩과-빈-사진첩|흰 바탕에 넓은 나무 탁자 하나가 있고, 그 위에 펼친 고리 사진첩 둘이 왼쪽과 오른쪽에 떨어져 놓인 그림입니다. 왼쪽 사진첩의 고리에는 사진을 꽂는 비닐 속지가 없고, 안쪽에는 파란 판만 있습니다. 왼쪽 사진첩 밖 탁자 위에는 작은 체스판이 찍힌 즉석사진 한 장이 따로 놓여 있습니다. 오른쪽 사진첩의 고리에는 비닐 속지 한 장이 끼워져 있고, 같은 즉석사진 여섯 장이 두 장씩 세 줄로 꽂혀 있습니다. 두 사진첩 사이 앞쪽에는 즉석카메라 하나가 있는 그림|속지가 없는 왼쪽 사진첩에는 사진을 꽂을 자리가 없고, 속지를 끼운 오른쪽 사진첩에는 사진 여섯 장이 꽂혔습니다.}}
<p class="look"><b>그림 읽기</b> — 탁자 위에 펼친 사진첩 둘이 왼쪽과 오른쪽에 있고, 그 사이 앞쪽에 카메라 하나가 있습니다. 왼쪽 사진첩은 Before로, 고리에 비닐 속지가 없어 사진 한 장이 사진첩 밖에 따로 놓였습니다. 오른쪽 사진첩은 After로, 속지 한 장에 사진 여섯 장이 두 장씩 세 줄로 꽂혔습니다. 속지는 표 <code>checkpoints</code>, 사진 여섯 장은 스레드 <code>customer-a</code>의 여섯 줄, 카메라는 01절처럼 체크포인터입니다. 나머지 표 셋은 그림에 없고, 사진첩 안쪽의 파란 판은 코드의 무엇과도 짝짓지 않습니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>이름 공간(SQL 낱말 <code>SCHEMA</code>)</td><td>한 데이터베이스 안에서 표들을 이름으로 묶어 두는 자리입니다. 사진첩 한 권에 그 사진첩의 속지만 끼워 두는 것과 같습니다. 이 절에서는 <code>CREATE SCHEMA ch23_lab</code>으로 만들고, 체크포인터의 표가 모두 여기에 생깁니다.</td></tr><tr><td>표 만들기(<code>setup()</code>)</td><td>체크포인터가 쓸 표를 데이터베이스에 만드는 일입니다. 빈 사진첩에 속지를 끼우는 일과 같습니다. 이 절에서는 메서드 <code>saver.setup()</code>이 표 넷을 만들었습니다.</td></tr><tr><td>표 만들기 기록(표 <code>checkpoint_migrations</code>)</td><td>표 만들기 문장 가운데 어디까지 실행했는지, 판 번호로 적어 두는 표입니다. 속지를 끼울 때마다 끼운 차례를 적어 두는 목록과 같습니다. 이 절에서는 판 번호 0부터 9까지 열 줄이 적혔습니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 이름 공간은 노트북 2절의 <code>CREATE SCHEMA ch23_lab</code>으로 만들고, 3절의 <code>SET search_path TO ch23_lab</code>으로 체크포인터 연결에 알려 줍니다. 표 만들기는 6절의 <code>saver.setup()</code> 한 줄입니다. 표 만들기 기록은 6절 출력 <code>표 만들기 기록 줄 수: 10</code>의 열 줄입니다.</p>
{{mermaid:02-1-연결-둘과-이름-공간-하나|위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 접속 글 하나 127.0.0.1:55432 rag_lab에서 화살표 두 개가 나갑니다. 왼쪽 화살표는 초록 상자 체크포인터 연결 saver_conn autocommit=True dict_row search_path ch23_lab으로 가고, 그 아래 회색 상자 체크포인터 PostgresSaver 그래프 graph에 붙음으로 이어집니다. 오른쪽 화살표는 초록 상자 조회 연결 conn autocommit=True로 갑니다. 회색 상자에서 체크포인트를 씀, 조회 연결에서 표 이름과 줄 수를 읽음이라고 적힌 화살표가 맨 아래 칸 이름 공간 ch23_lab으로 모이고, 칸 안 노란 상자에는 setup() 뒤 표 넷 checkpoints checkpoint_blobs checkpoint_writes checkpoint_migrations가 적힌 그림|접속 글 하나로 연결 둘을 열어, 하나는 체크포인터에 넘기고 하나로는 이름 공간 ch23_lab의 표를 직접 읽습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 초록 상자는 우리가 넘긴 접속 글과 그것으로 연 연결 둘이고, 회색 상자는 라이브러리의 체크포인터입니다. 왼쪽 연결은 체크포인터에 넘기고, 오른쪽 연결로는 우리가 표를 직접 읽습니다. 노란 상자는 노트북 6절에서 출력으로 확인한 표 넷입니다.</p>
<h3>표를 먼저 만들어야 하는 까닭</h3><p>그래프는 실행을 시작할 때 그 스레드의 마지막 체크포인트를 찾고, 단계를 마칠 때마다 체크포인트를 씁니다. PostgreSQL 체크포인터는 이 일을 표 <code>checkpoints</code>에 문장을 보내 합니다. 표가 없으면 첫 문장에서 PostgreSQL이 오류를 냅니다. 설치판 소스의 메서드 설명도, 처음 쓸 때 사용자가 <code>setup()</code>을 직접 불러야 한다고 적습니다.</p><p>메서드 <code>setup()</code>이 실행하는 문장은 클래스의 속성 <code>MIGRATIONS</code>에 열 개가 들어 있습니다. 속성 이름은 <a href="../ch21-create-agent/04-0x에서-1x로-마이그레이션.html">Ch 21 04절</a>의 「옮기기」와 같은 영어 낱말이지만, 여기서는 표를 만들고 고치는 문장의 차례입니다. 실행한 문장은 표 만들기 기록에 판 번호로 남습니다. 설치판 소스에서 다음에 부르면, 기록 표를 만드는 0번 문장을 먼저 실행합니다. 이 문장은 표가 이미 있으면 아무 일도 하지 않고, 그 뒤에는 마지막 판 번호 뒤 문장만 실행합니다.</p>
<h3>다른 상황에 적용</h3><p>새 데이터베이스에 체크포인터를 처음 붙일 때 <code>setup()</code>을 한 번 부릅니다. 표를 이미 만든 데이터베이스라면, 노트북 8절처럼 다시 불러도 기록과 쌓인 줄이 그대로였습니다. 여러 프로그램이 같은 표를 함께 쓰는 모습은 이번에 실행하지 않았습니다.</p>
<h3>비교와 경계</h3><p>01절 <code>InMemorySaver</code>는 표를 만들 일이 없었지만, 체크포인트가 프로그램의 메모리에만 있었습니다. 이 절의 체크포인트는 데이터베이스 서버의 표에 남아, 다른 연결로도 셀 수 있었습니다. 체크포인터의 연결을 닫은 뒤에도 표의 줄 수는 그대로였습니다. <a href="03-스레드-재개와-대화-이어가기.html">03절</a>에서 쓸 SQLite 체크포인터는 필요할 때 표를 스스로 만듭니다. 설치한 langgraph-checkpoint-sqlite 3.0.3 소스가 그렇게 적습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북을 실행하기 전에 PostgreSQL 서버를 켜 둡니다. Ch 12 02절에서 만든 Docker 컨테이너 <code>hankyung-part3-pgvector</code>를 그대로 씁니다. 꺼져 있으면 <code>docker start hankyung-part3-pgvector</code>로 켭니다. 컨테이너가 없으면 이 챕터 실습 폴더 <code>README.md</code>에 적은 <code>docker run</code> 명령으로 만들고, 같은 명령이 노트북 첫 셀에도 있습니다. 접속 글은 Ch 12 02절과 같은 <code>postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab</code>입니다.</p><p>노트북은 데이터베이스 <code>rag_lab</code> 안에 이름 공간 <code>ch23_lab</code>을 만들어 씁니다. 다시 실행하면 그 이름 공간만 지우고 처음부터 만듭니다. 01절처럼 매번 같은 값을 내는 우리 노드로 저장된 값을 가르려고, 모델은 부르지 않습니다. 모델 요청은 0번이고, API 키 셀도 없습니다.</p><p>예시 부분은 데이터베이스에 붙어 이름 공간을 만들고, 체크포인터와 01절 그래프를 준비합니다. 체크포인터가 실행할 표 만들기 문장 열 개의 첫 줄도 미리 봅니다.</p>
{{notebook:02-PostgresSaver-준비와-스키마|example}}
<p class="look"><b>확인할 점</b> — 노트북 2절에서 이름 공간 <code>ch23_lab</code>이 빈 목록 <code>[]</code>으로 시작하는지 봅니다. 3절 출력 <code>{'search_path': 'ch23_lab'}</code>로 체크포인터 연결이 이 이름 공간을 보는지 확인합니다. 3절 출력 <code>표 만들기 문장 수: 10</code>의 열 문장이 6절에서 실행됩니다.</p>
{{mermaid:02-2-표-만들기-문장-열과-기록-열-줄|위에서 아래로 읽는 흐름도입니다. 맨 위 회색 상자 표 만들기 문장 열 개 속성 MIGRATIONS 번호 0부터 9에서 파란 상자 saver.setup() 처음 부름으로 갑니다. 그 아래 칸 setup() 뒤 이름 공간 ch23_lab 안에는 왼쪽 노란 상자 표 넷과 오른쪽 노란 상자 표 만들기 기록 판 번호 0부터 9 열 줄이 나란히 있습니다. 칸에서 파란 상자 saver.setup() 한 번 더를 지나, 맨 아래 노란 상자 기록 열 줄 그대로 customer-a 여섯 줄 그대로로 가는 그림|표 만들기 문장 열 개가 한 번씩 실행되어 판 번호 열 줄이 적혔고, 둘째 setup()은 기록을 늘리지 않았습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 회색 상자는 설치판 체크포인터 클래스가 가진 문장 목록이고, 노트북 3절에서 첫 줄만 보았습니다. 파란 상자는 우리가 부른 메서드이고, 노란 상자는 노트북 6·8절 출력입니다. 기록 열 줄과 문장 열 개는 판 번호로 짝을 이룹니다.</p>
<h2 id="b6"><span class="no">6</span>일부러 실패해 보기</h2><p>아래 Before 셀은 표 만들기 <code>setup()</code>을 부르지 않은 채, 01절 첫 실행과 같은 입력으로 그래프를 실행합니다. 이어지는 After 셀은 <code>setup()</code>을 부른 뒤 같은 실행을 합니다. After 뒤에는 표의 구조와 쌓인 줄을 보고, 값 두 가지를 바꿔 봅니다.</p>
{{notebook:02-PostgresSaver-준비와-스키마|failure}}
{{mermaid:02-3-표를-만들기-전과-뒤|위에서 아래로 읽는 그림입니다. 맨 위 파란 상자 같은 그래프 graph 같은 체크포인터 스레드 customer-a 입력 total 0 amount 3에서 칸 둘로 화살표가 갑니다. 왼쪽 칸 Before setup() 없이에는 빨간 상자 받은 오류 UndefinedTable 표 checkpoints 없음 오류 번호 42P01 아래로 빨간 상자 멈춘 뒤에도 ch23_lab 안의 표 없음이 있습니다. 오른쪽 칸 After setup() 뒤에는 노란 상자 표 넷 표 만들기 기록 열 줄 아래로 노란 상자 첫 실행 합계 3 둘째 실행 amount 4 합계 7이 있는 그림|같은 그래프와 같은 입력인데, 표를 만들기 전에는 UndefinedTable을 받고 표를 만든 뒤에는 01절처럼 합계 7이 됩니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 파란 상자는 두 칸이 함께 쓰는 그래프와 입력입니다. 왼쪽 칸은 노트북 5절 Before, 오른쪽 칸은 6절 After이고, 칸 안은 위에서 아래로 읽습니다. 빨간 상자는 Before의 결함 결과이고, 노란 상자는 After에서 출력으로 확인한 값입니다. 두 칸의 차이는 메서드 <code>setup()</code>을 불렀는지 하나입니다.</p>
<table><thead><tr><th>견준 것</th><th>Before(표 만들기 전)</th><th>After(표 만들기 뒤)</th></tr></thead><tbody><tr><td>메서드 <code>setup()</code></td><td>부르지 않음</td><td>부름</td></tr><tr><td>스레드 <code>customer-a</code> 첫 실행</td><td>받은 오류 <code>UndefinedTable</code>·오류 번호 <code>42P01</code></td><td>합계 3</td></tr><tr><td>같은 스레드 둘째 실행</td><td>—</td><td>합계 7</td></tr><tr><td>이름 공간 <code>ch23_lab</code> 안의 표</td><td>없음 <code>[]</code></td><td>넷</td></tr><tr><td>표 만들기 기록</td><td>—</td><td>열 줄(판 번호 0~9)</td></tr><tr><td>표 <code>checkpoints</code>의 <code>customer-a</code> 줄</td><td>—</td><td>여섯</td></tr></tbody></table>
<p>표를 만들기 전에는 첫 실행에서 오류 <code>UndefinedTable</code>을 받았고, 오류 번호는 <code>42P01</code>이었습니다. 오류 글은 표 <code>checkpoints</code>가 없다는 것이었고, 그래프는 결과를 내놓지 못했습니다. 실행이 멈춘 뒤에도 이름 공간 <code>ch23_lab</code>에는 표가 하나도 생기지 않았습니다. 체크포인터를 만들어 그래프에 붙이는 것만으로는 표가 준비되지 않습니다.</p><p>메서드 <code>setup()</code>을 부르자 표 넷이 생겼고, 표 만들기 기록에 판 번호 0부터 9까지 열 줄이 적혔습니다. 그 뒤 Before와 같은 입력으로 첫 실행은 합계 3, 둘째 실행은 합계 7이 되어 01절과 같았습니다. 그래프·체크포인터·입력은 Before와 같고, 달라진 것은 <code>setup()</code> 한 줄입니다.</p><p>스레드 <code>customer-a</code>의 체크포인트 여섯은 표 <code>checkpoints</code>의 여섯 줄이었고, 스레드 <code>customer-b</code>는 세 줄이었습니다. 두 스레드의 줄은 한 표에 있고, 칸 <code>thread_id</code>의 값으로 갈립니다. 메서드 <code>setup()</code>을 한 번 더 불러도 오류 없이 기록은 열 줄 그대로였습니다. 체크포인터의 연결을 닫은 뒤에도 다른 연결로 센 줄 수는 그대로였습니다.</p>
{{mermaid:02-4-스레드마다-표에-쌓인-줄|칸 둘이 나란히 놓이고 그 아래에 상자 둘이 있는 그림입니다. 왼쪽 칸 스레드 customer-a에는 노란 상자 get_state_history 체크포인트 여섯 아래 노란 상자 표 checkpoints 여섯 줄이 있습니다. 오른쪽 칸 스레드 customer-b에는 노란 상자 실행 결과 합계 4 아래 노란 상자 표 checkpoints 세 줄이 있습니다. 두 칸 아래 회색 상자에는 두 스레드 모두 같은 표 checkpoints 칸 thread_id의 값으로 갈림, 맨 아래 노란 상자에는 체크포인터 연결을 닫은 뒤에도 customer-a 여섯 줄 작업 폴더 파일 없음이 적힌 그림|두 스레드의 체크포인트가 같은 표 checkpoints에 여섯 줄과 세 줄로 쌓였고, 체크포인터 연결을 닫은 뒤에도 줄 수는 그대로였습니다.}}
<p class="look"><b>도식 읽기</b> — 칸 둘이 스레드 둘이고, 칸 안은 위에서 아래로 읽습니다. 칸 안 노란 상자는 노트북 7·8절 출력입니다. 가운데 회색 상자는 두 칸에 모두 해당하는 사실입니다. 맨 아래 노란 상자는 노트북 9절 출력입니다.</p>
<p>모델을 부르지 않아, 노트북 출력은 새 커널로 두 번 실행해도 글자까지 같아야 합니다. 새 커널로 두 번 실행했을 때 코드 셀 28개의 출력이 모두 같았습니다. 두 실행 모두 이름 공간 <code>ch23_lab</code>이 없는 데이터베이스에서 시작했습니다.</p>
<p class="look"><b>확인할 점</b> — 노트북 5절 출력 <code>받은 오류: UndefinedTable</code>·<code>오류 번호: 42P01</code>과 6절 출력 <code>setup() 뒤 표 수: 4</code>로 Before와 After를 견줍니다. 7절 출력 <code>표 checkpoints의 customer-a 줄 수: 6</code>과 8절 줄 <code>customer-b | 3</code>으로 줄이 스레드마다 쌓이는 것을 셉니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>이 절의 준비물 안내는 Ch 12와 같은 Docker 이미지 <code>pgvector/pgvector:0.8.2-pg17</code>로 만든 컨테이너를 씁니다. 이번 교재 출력은 그 환경에서 만들지 않았습니다. 같은 접속 글로 켠 PostgreSQL 17.11 서버에서 만들었고, 판 번호 줄은 서버에 따라 다르게 나올 수 있습니다.</li><li>서버가 꺼져 있으면 노트북 2절의 연결 셀이 <code>OperationalError</code>로 멈춥니다. 표가 없어서 나는 Before의 <code>UndefinedTable</code>과는 다른 오류입니다. 이 장면은 노트북 밖에서 확인했고, 노트북에서는 실행하지 않았습니다.</li><li>접속 글의 암호는 Ch 12와 같은 수업 전용 값입니다. 다른 환경에 쓰지 않고, 노트북은 접속 글을 출력하지 않습니다.</li><li>노트북은 이름 공간 <code>ch23_lab</code>을 지우고 다시 만듭니다. 이 이름 공간에 다른 표를 두지 않습니다.</li><li>연결을 직접 만들어 넘길 때는 <code>autocommit=True</code>와 <code>row_factory=dict_row</code>를 함께 주라고 설치판 패키지 설명이 적습니다. 둘 가운데 하나를 빠뜨린 장면은 이번에 실행하지 않았습니다.</li><li>공식 문서 예시는 <code>with PostgresSaver.from_conn_string(접속 글) as saver:</code> 모양을 씁니다. 이 절은 Ch 12 02절처럼 연결을 직접 열고 닫았습니다. 설치판 소스에서 이 모양은 같은 두 인자에 <code>prepare_threshold=0</code>을 더해 연결을 열고, <code>with</code> 블록이 끝나면 연결을 닫습니다. 이 모양은 노트북에서 실행하지 않았습니다.</li><li>표 <code>checkpoint_blobs</code>와 <code>checkpoint_writes</code>의 쓰임은 설치판 소스로만 보았고, 줄은 읽지 않았습니다. 체크포인트에 딸린 쓰기는 <a href="05-pending-writes와-장애-복구.html">05절</a>에서 다룹니다.</li><li>칸 <code>checkpoint_id</code>처럼 실행마다 달라지는 값은 출력하지 않았습니다.</li><li>여러 프로그램이 같은 표를 함께 쓰는 모습, 연결 묶음(<code>psycopg_pool</code>), 권한 나누기, 백업은 이번에 실행하지 않았습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>표 만들기 전에 실행하자, 표 <code>checkpoints</code>가 없어 오류 <code>UndefinedTable</code>을 받았습니다.</li><li>메서드 <code>setup()</code>은 표 넷을 만들고, 표 만들기 기록에 판 번호 열 줄을 적었습니다.</li><li>표를 만든 뒤에는 01절처럼 합계 7이 되었고, 체크포인트 여섯이 표에 여섯 줄로 쌓였습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href="03-스레드-재개와-대화-이어가기.html">03절</a>에서는 연결과 그래프 객체를 새로 만들어도, 같은 스레드의 대화를 이어 가는지 봅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 표 만들기 <code>setup()</code>을 부르기 전에 그래프를 실행하자 어떤 오류를 받았고, 그 까닭은 무엇인가요?</p><p class="quiz-a">오류 <code>UndefinedTable</code>을 받았습니다. 그래프가 체크포인트를 찾을 표 <code>checkpoints</code>가 아직 없었기 때문입니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p><p class="quiz-q">2. 메서드 <code>setup()</code>을 부른 뒤 이름 공간 <code>ch23_lab</code>에 무엇이 생겼나요?</p><p class="quiz-a">표 넷이 생겼고, 그 가운데 표 만들기 기록에는 판 번호 0부터 9까지 열 줄이 적혔습니다. 틀렸다면 노트북 6절을 다시 읽습니다.</p><p class="quiz-q">3. 스레드 <code>customer-a</code>의 체크포인트 여섯은 데이터베이스의 어디에 있었나요?</p><p class="quiz-a">표 <code>checkpoints</code>에 칸 <code>thread_id</code>가 <code>customer-a</code>인 줄 여섯으로 있었습니다. 틀렸다면 노트북 7절을 다시 읽습니다.</p><p class="quiz-q">4. 메서드 <code>setup()</code>을 두 번째로 부르면 어떻게 되었고, 그 까닭은 무엇인가요?</p><p class="quiz-a">오류 없이 표 만들기 기록이 열 줄 그대로였습니다. 설치판 소스에서 <code>setup()</code>은 기록 표를 만드는 0번 문장을 먼저 실행하는데, 표가 이미 있어 아무 일도 하지 않았습니다. 그 뒤 마지막 판 번호 다음 문장부터 실행하는데, 남은 문장이 없었습니다. 틀렸다면 노트북 8절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://docs.langchain.com/oss/python/langgraph/checkpointers">LangGraph Checkpointers</a></div>확인 2026-09-25 · PostgreSQL 체크포인터 <code>PostgresSaver</code>와, 만든 뒤 <code>setup()</code>을 부르는 예를 적습니다.</li><li><div><a href="https://docs.langchain.com/oss/python/langgraph/persistence">LangGraph Persistence</a></div>확인 2026-09-25 · 프로그램 밖에 남기는 체크포인터로 <code>PostgresSaver</code>를 적습니다.</li><li><div>langgraph-checkpoint-postgres 3.0.5 패키지 설명</div>처음 쓸 때 <code>setup()</code>을 부르라고 적습니다. 연결을 직접 만들 때 줄 두 인자도 적습니다.</li><li>같은 판 소스 <code>langgraph/checkpoint/postgres/__init__.py</code> 54~75행은 <code>from_conn_string</code>, 77~102행은 <code>setup()</code>입니다.</li><li>같은 파일 301~308행은 수·글이 아닌 칸 값을 표 <code>checkpoint_blobs</code>에 따로 두는 자리, 336~351행은 쓰기를 담는 자리입니다.</li><li>같은 판 <code>langgraph/checkpoint/postgres/base.py</code> 37~85행은 표 만들기 문장 목록 <code>MIGRATIONS</code>입니다.</li><li><div>langgraph-checkpoint-sqlite 3.0.3 소스</div><code>langgraph/checkpoint/sqlite/__init__.py</code> 122~128행은 SQLite 체크포인터의 <code>setup()</code> 설명입니다.</li><li>langgraph 1.2.11 소스 <code>langgraph/pregel/_loop.py</code> 1651~1654행 — 실행을 시작할 때 마지막 체크포인트를 찾는 자리입니다.</li><li>psycopg 3.3.3 소스 <code>psycopg/connection.py</code> 155~176행 — <code>with</code> 블록이 끝날 때 연결을 닫는 자리입니다.</li><li>Ch 12 02절에서 psycopg와 자리표시자를 보았습니다. Ch 4 03절에서 SQL 조회를, 01절에서 체크포인터와 스레드를 보았습니다.</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# PostgresSaver 준비와 스키마

**이 노트북에서 할 일**

1. 01절 그래프에 PostgreSQL 체크포인터를 붙이고, 표를 만들기 전에 실행해 받은 오류를 봅니다.
2. 메서드 `setup()`으로 표를 만든 뒤 같은 입력으로 다시 실행하고, 생긴 표와 표 만들기 기록을 읽습니다.
3. 체크포인트가 데이터베이스 표에 스레드마다 한 줄씩 쌓이는 것을 셉니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
01절처럼 매번 같은 값을 내는 우리 노드로, 저장된 값이 맞는지 출력으로 가릅니다.

PostgreSQL 서버가 `127.0.0.1:55432`에서 켜져 있어야 합니다.
Ch 12 02절에서 만든 Docker 컨테이너 `hankyung-part3-pgvector`를 그대로 씁니다.
꺼져 있으면 터미널에서 `docker start hankyung-part3-pgvector`로 켭니다.
컨테이너가 없으면 Ch 12 실습 폴더 `README.md`와 같은 아래 명령으로 먼저 만듭니다.

```bash
docker run --name hankyung-part3-pgvector \
  -e POSTGRES_USER=student \
  -e POSTGRES_PASSWORD=local-practice-only \
  -e POSTGRES_DB=rag_lab \
  -p 127.0.0.1:55432:5432 \
  -d pgvector/pgvector:0.8.2-pg17
```

노트북은 데이터베이스 `rag_lab` 안에 이름 공간 `ch23_lab`을 만들어 씁니다.
다시 실행하면 그 이름 공간만 지우고 처음부터 만듭니다.
작업 폴더에는 파일을 쓰지 않고, 읽어 오는 자료 파일도 없습니다.
교재 출력을 만든 실행에서는 노트북 전체가 5초 안에 끝났습니다.

**기준 버전** — 첫 셀에서 패키지 셋을 설치합니다.
판은 langgraph 1.2.11과 langgraph-checkpoint-postgres 3.0.5입니다.
패키지 psycopg의 판은 3.3.3입니다.

교재 출력은 Linux의 Python 3.12.13과 PostgreSQL 17.11 서버로 만들었습니다.
그 서버는 Docker 컨테이너가 아니라, 같은 접속 글로 켠 서버입니다.
데이터베이스 PostgreSQL의 필수 최소 판은 설치한 패키지 설명에 없고, 17 말고는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~7절을 읽습니다.
데이터베이스에 붙고, 표를 만들기 전과 뒤를 견주고, 쌓인 줄을 세는 자리입니다.
8·9절은 값을 바꿔 보고 연결을 닫는 자리이고, 실습 시간에 실행합니다.

실습 폴더 `labs/part6/ch23-persistence`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 접속 글 하나 127.0.0.1:55432 rag_lab에서 화살표 두 개가 나갑니다. 왼쪽 화살표는 초록 상자 체크포인터 연결 saver_conn autocommit=True dict_row search_path ch23_lab으로 가고, 그 아래 회색 상자 체크포인터 PostgresSaver 그래프 graph에 붙음으로 이어집니다. 오른쪽 화살표는 초록 상자 조회 연결 conn autocommit=True로 갑니다. 회색 상자에서 체크포인트를 씀, 조회 연결에서 표 이름과 줄 수를 읽음이라고 적힌 화살표가 맨 아래 칸 이름 공간 ch23_lab으로 모이고, 칸 안 노란 상자에는 setup() 뒤 표 넷 checkpoints checkpoint_blobs checkpoint_writes checkpoint_migrations가 적힌 그림](attachment:02-1-연결-둘과-이름-공간-하나.png)

위에서 아래로 읽습니다.
초록 상자는 우리가 넘긴 접속 글과 그것으로 연 연결 둘이고, 회색 상자는 라이브러리의 체크포인터입니다.
왼쪽 연결은 체크포인터에 넘기고, 오른쪽 연결로는 우리가 표를 직접 읽습니다.
노란 상자는 노트북 6절에서 출력으로 확인한 표 넷입니다.

### [2] markdown {}

## 1. 준비

01절의 체크포인터 `InMemorySaver`는 이 프로그램의 메모리에만 저장했습니다.
이 절은 체크포인트를 PostgreSQL 데이터베이스의 표에 쓰는 체크포인터 `PostgresSaver`를 씁니다.
이 체크포인터는 쓰기 전에, 체크포인트를 담을 표를 먼저 만들어야 합니다.
표를 만들지 않고 실행한 것이 5절의 Before, 표를 만든 뒤 실행한 것이 6절의 After입니다.

첫 셀은 패키지 셋을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:25.156377Z', 'iopub.status.busy': '2026-09-25T08:37:25.156185Z', 'iopub.status.idle': '2026-09-25T08:37:25.644147Z', 'shell.execute_reply': '2026-09-25T08:37:25.643593Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "langgraph==1.2.11" "langgraph-checkpoint-postgres==3.0.5" "psycopg[binary,pool]==3.3.3"
from importlib.metadata import version

print("langgraph:", version("langgraph"))
print("langgraph-checkpoint-postgres:", version("langgraph-checkpoint-postgres"))
print("psycopg:", version("psycopg"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
langgraph: 1.2.11
langgraph-checkpoint-postgres: 3.0.5
psycopg: 3.3.3

```

### [4] markdown {}

**결과 읽기** — 출력 줄 `langgraph: 1.2.11`·`langgraph-checkpoint-postgres: 3.0.5`·`psycopg: 3.3.3`이 보입니다.
세 판 모두 실습 폴더 잠금과 같은 판입니다.
이 노트북의 출력은 2026-09-25에 이 판으로 실행한 결과입니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
상태 형식과 그래프를 만드는 이름은 01절과 같습니다.
패키지 psycopg는 Ch 12 02절에서 PostgreSQL에 붙을 때 쓴 패키지입니다.
새로 가져오는 이름은 `dict_row`와 체크포인터 `PostgresSaver` 둘이고, 뜻은 3절에서 풉니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:25.645262Z', 'iopub.status.busy': '2026-09-25T08:37:25.645170Z', 'iopub.status.idle': '2026-09-25T08:37:26.255217Z', 'shell.execute_reply': '2026-09-25T08:37:26.254820Z'}, 'lesson_role': 'setup'}

```python
# 01절 그래프 이름(Ch 13 01·02절)에, PostgreSQL에 붙는 이름과 체크포인터 하나를 더해 가져옵니다
import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
# 패키지 psycopg는 Ch 12 02절에서 PostgreSQL에 붙을 때 쓴 패키지입니다
import psycopg
from psycopg.rows import dict_row
# 체크포인트를 PostgreSQL 표에 쓰는 체크포인터입니다
from langgraph.checkpoint.postgres import PostgresSaver

print("이 절에서 새로 가져온 이름:", "dict_row", "PostgresSaver")
```

출력:
```
이 절에서 새로 가져온 이름: dict_row PostgresSaver

```

### [6] markdown {}

**결과 읽기** — 출력 줄 `이 절에서 새로 가져온 이름: dict_row PostgresSaver`가 보입니다.
이름 `dict_row`는 패키지 psycopg에 들어 있습니다.
체크포인터 `PostgresSaver`는 첫 셀에서 설치한 langgraph-checkpoint-postgres에 들어 있습니다.

다음 셀은 01절처럼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다.
이 절의 체크포인트는 데이터베이스 서버에 저장되니, 작업 폴더에는 파일이 생기지 않을 것입니다.
9절에서 폴더가 그대로 비어 있는지 봅니다.

### [7] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.255878Z', 'iopub.status.busy': '2026-09-25T08:37:26.255821Z', 'iopub.status.idle': '2026-09-25T08:37:26.257887Z', 'shell.execute_reply': '2026-09-25T08:37:26.257621Z'}, 'lesson_role': 'setup'}

```python
# 파일이 생기는지 볼 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다(Ch 4 03절과 같은 모양)
import os
import tempfile

# mkdtemp()는 운영체제 임시 폴더 안에 새 폴더를 만들고, 그 폴더의 위치를 글로 내놓습니다
practice_folder = tempfile.mkdtemp(prefix="ch23-02-")
# chdir()는 터미널의 cd처럼 현재 작업 폴더를 옮깁니다
os.chdir(practice_folder)
print("임시 폴더 이름에 ch23-02-이 들어 있는가:", "ch23-02-" in practice_folder)
print("현재 작업 폴더의 파일:", os.listdir())
```

출력:
```
임시 폴더 이름에 ch23-02-이 들어 있는가: True
현재 작업 폴더의 파일: []

```

### [8] markdown {}

**결과 읽기** — 출력 줄 `임시 폴더 이름에 ch23-02-이 들어 있는가: True`로, 이 절의 폴더를 만들었습니다.
출력 줄 `현재 작업 폴더의 파일: []`로, 빈 폴더에서 시작합니다.

## 2. 데이터베이스에 붙기

이 절은 Ch 12 02절의 PostgreSQL 컨테이너를 그대로 씁니다.
다음 셀은 Ch 12 02절과 같은 접속 글로 데이터베이스에 붙고, 서버 판 번호를 봅니다.
함수 `psycopg.connect`와 인자 `autocommit=True`는 그 절에서 배웠습니다.
메서드 `cursor`·`execute`·`fetchone`도 그 절과 같습니다.
접속 글에는 수업 전용 암호가 들어 있어 출력하지 않습니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.258503Z', 'iopub.status.busy': '2026-09-25T08:37:26.258447Z', 'iopub.status.idle': '2026-09-25T08:37:26.271476Z', 'shell.execute_reply': '2026-09-25T08:37:26.271103Z'}}

```python
# Ch 12 02절과 같은 접속 글로 데이터베이스에 붙고, 서버 판 번호를 봅니다
database_url = "postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab"
conn = psycopg.connect(database_url, autocommit=True)
cur = conn.cursor()
cur.execute("SELECT current_setting('server_version')")
print("PostgreSQL 판:", cur.fetchone()[0])
```

출력:
```
PostgreSQL 판: 17.11

```

### [10] markdown {}

**결과 읽기** — 출력 줄 `PostgreSQL 판: 17.11`이 보입니다.
서버에 붙었고, 문장 하나를 실행해 답을 받았습니다.
이 판 번호는 교재 출력을 만든 서버의 값이라, 컨테이너에 따라 다르게 나올 수 있습니다.
서버가 꺼져 있으면 이 셀이 오류 `OperationalError`로 멈춥니다.
이 장면은 노트북 밖에서 확인했고, 이 노트북에서는 실행하지 않았습니다.

체크포인터의 표는 데이터베이스 안의 이름 공간 하나에 모아 둡니다.
이름 공간(SQL 낱말 `SCHEMA`)은 한 데이터베이스 안에서 표들을 이름으로 묶어 두는 자리입니다.
사진첩 한 권에 그 사진첩의 속지만 끼워 두는 것과 같습니다.
이 절의 이름 공간은 `ch23_lab`이고, Ch 12 표와 섞이지 않게 따로 둡니다.

다음 셀은 이름 공간 `ch23_lab` 안의 표 이름을 목록으로 읽는 함수입니다.
데이터베이스 PostgreSQL은 이름 공간 `information_schema`의 목록 `tables`에 표를 한 줄씩 보여 줍니다.
Ch 4 03절의 `SELECT … WHERE … ORDER BY` 모양으로, 이름 공간이 `ch23_lab`인 줄만 이름 차례로 읽습니다.

### [11] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.272066Z', 'iopub.status.busy': '2026-09-25T08:37:26.272014Z', 'iopub.status.idle': '2026-09-25T08:37:26.273865Z', 'shell.execute_reply': '2026-09-25T08:37:26.273549Z'}}

```python
# 이름 공간 ch23_lab 안의 표 이름을 이름 차례로 읽어, 목록으로 내놓습니다
def table_names(cursor):
    sql = "SELECT table_name FROM information_schema.tables"
    sql = sql + " WHERE table_schema = 'ch23_lab' ORDER BY table_name"
    cursor.execute(sql)
    names = []
    # 줄마다 첫 칸이 표 이름입니다
    for row in cursor.fetchall():
        names.append(row[0])
    return names
```

출력:
```

```

### [12] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `table_names`는 인자로 받은 커서로 문장을 실행하고, 줄마다 첫 칸인 표 이름을 목록에 담습니다.

다음 셀은 이름 공간 `ch23_lab`을 만듭니다.
문장 `DROP SCHEMA IF EXISTS ch23_lab CASCADE`는 그 이름 공간이 있으면 안의 표까지 함께 지웁니다.
노트북을 다시 실행해도 빈 이름 공간에서 시작하려는 줄이고, 다른 이름 공간의 표는 지우지 않습니다.
문장 `CREATE SCHEMA ch23_lab`이 빈 이름 공간을 새로 만듭니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.274427Z', 'iopub.status.busy': '2026-09-25T08:37:26.274376Z', 'iopub.status.idle': '2026-09-25T08:37:26.283858Z', 'shell.execute_reply': '2026-09-25T08:37:26.283565Z'}}

```python
# 이 절의 표를 담을 이름 공간 ch23_lab을, 있으면 안의 표까지 지우고 빈 채로 새로 만듭니다
cur.execute("DROP SCHEMA IF EXISTS ch23_lab CASCADE")
cur.execute("CREATE SCHEMA ch23_lab")
print("ch23_lab 안의 표:", table_names(cur))
```

출력:
```
ch23_lab 안의 표: []

```

### [14] markdown {}

**결과 읽기** — 출력 줄 `ch23_lab 안의 표: []`입니다.
이름 공간은 생겼지만, 아직 표는 하나도 없습니다.

## 3. PostgreSQL 체크포인터 만들기

이 체크포인터는 데이터베이스에 붙은 연결 하나를 받아, 그 연결로 체크포인트를 쓰고 읽습니다.
다음 셀은 체크포인터가 쓸 연결을 2절 연결과 따로 엽니다.
인자 `row_factory=dict_row`는 받아 온 줄을, 칸 이름이 키인 딕셔너리로 내놓게 합니다.
설치판 패키지 설명은 연결을 직접 만들 때 이 인자와 `autocommit=True`를 함께 주라고 적습니다.
문장 `SET search_path TO ch23_lab`은 이 연결이 이름 공간을 적지 않은 표 이름을 `ch23_lab`에서 찾게 합니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.284396Z', 'iopub.status.busy': '2026-09-25T08:37:26.284338Z', 'iopub.status.idle': '2026-09-25T08:37:26.289007Z', 'shell.execute_reply': '2026-09-25T08:37:26.288763Z'}}

```python
# 체크포인터가 쓸 연결을 따로 열고, 이 연결이 표를 찾을 이름 공간을 ch23_lab으로 정합니다
saver_conn = psycopg.connect(database_url, autocommit=True, row_factory=dict_row)
saver_cur = saver_conn.cursor()
saver_cur.execute("SET search_path TO ch23_lab")
# SHOW 문장은 설정 값 하나를 한 줄로 내놓습니다
saver_cur.execute("SHOW search_path")
print("체크포인터 연결이 표를 찾는 이름 공간:", saver_cur.fetchone())
```

출력:
```
체크포인터 연결이 표를 찾는 이름 공간: {'search_path': 'ch23_lab'}

```

### [16] markdown {}

**결과 읽기** — 출력 줄 `체크포인터 연결이 표를 찾는 이름 공간: {'search_path': 'ch23_lab'}`입니다.
받아 온 줄이 튜플이 아니라, 칸 이름 `search_path`가 키인 딕셔너리로 나왔습니다.
이 연결로 이름 공간을 적지 않은 표를 만들면, 그 표도 `ch23_lab`에 생깁니다.

다음 셀은 이 연결을 넘겨 체크포인터를 만듭니다.
클래스 `PostgresSaver`는 연결 하나를 받아, 체크포인트를 PostgreSQL 표에 쓰는 체크포인터를 만듭니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.289519Z', 'iopub.status.busy': '2026-09-25T08:37:26.289471Z', 'iopub.status.idle': '2026-09-25T08:37:26.290946Z', 'shell.execute_reply': '2026-09-25T08:37:26.290709Z'}}

```python
# 이 연결을 넘겨 PostgreSQL 체크포인터를 만듭니다(아직 표를 만들지 않음)
saver = PostgresSaver(saver_conn)
print("체크포인터의 종류:", type(saver).__name__)
```

출력:
```
체크포인터의 종류: PostgresSaver

```

### [18] markdown {}

**결과 읽기** — 출력 줄 `체크포인터의 종류: PostgresSaver`입니다.
설치판 소스로 보면, 체크포인터를 만드는 것만으로는 데이터베이스에 문장을 보내지 않습니다.

표를 만드는 일은 메서드 `setup()`이 맡습니다.
이 메서드가 실행할 문장들은 클래스의 속성 `MIGRATIONS`에 목록으로 들어 있습니다.
속성 이름은 Ch 21 04절의 「옮기기」와 같은 영어 낱말이지만, 여기서는 표를 만들고 고치는 문장의 차례입니다.
다음 셀은 데이터베이스에 보내지 않고, 이 목록의 문장마다 첫 줄만 봅니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.291428Z', 'iopub.status.busy': '2026-09-25T08:37:26.291380Z', 'iopub.status.idle': '2026-09-25T08:37:26.293181Z', 'shell.execute_reply': '2026-09-25T08:37:26.292950Z'}}

```python
# 표 만들기 때 차례로 실행할 문장 목록에서, 문장마다 첫 줄만 봅니다(데이터베이스에는 보내지 않음)
statements = PostgresSaver.MIGRATIONS
print("표 만들기 문장 수:", len(statements))
print("번호 | 문장의 첫 줄")
for number in range(len(statements)):
    # 앞뒤 빈칸과 줄바꿈을 떼고, 첫 줄만 남깁니다
    first_line = statements[number].strip().splitlines()[0]
    print(number, "|", first_line)
```

출력:
```
표 만들기 문장 수: 10
번호 | 문장의 첫 줄
0 | CREATE TABLE IF NOT EXISTS checkpoint_migrations (
1 | CREATE TABLE IF NOT EXISTS checkpoints (
2 | CREATE TABLE IF NOT EXISTS checkpoint_blobs (
3 | CREATE TABLE IF NOT EXISTS checkpoint_writes (
4 | ALTER TABLE checkpoint_blobs ALTER COLUMN blob DROP not null;
5 | SELECT 1;
6 | CREATE INDEX CONCURRENTLY IF NOT EXISTS checkpoints_thread_id_idx ON checkpoints(thread_id);
7 | CREATE INDEX CONCURRENTLY IF NOT EXISTS checkpoint_blobs_thread_id_idx ON checkpoint_blobs(thread_id);
8 | CREATE INDEX CONCURRENTLY IF NOT EXISTS checkpoint_writes_thread_id_idx ON checkpoint_writes(thread_id);
9 | ALTER TABLE checkpoint_writes ADD COLUMN IF NOT EXISTS task_path TEXT NOT NULL DEFAULT '';

```

### [20] markdown {}

**결과 읽기** — 출력 줄 `표 만들기 문장 수: 10`입니다.
라벨 줄 `번호 | 문장의 첫 줄` 아래 열 줄을 봅니다.
번호 0부터 3까지 네 문장이 표 넷을 만들고, 번호 6부터 8까지 세 문장은 칸 `thread_id`에 색인을 만듭니다.
번호 4와 9는 이미 만든 표의 칸을 고치고, 번호 5의 `SELECT 1;`은 아무것도 바꾸지 않는 문장입니다.

## 4. 01절 그래프에 붙이기

그래프는 01절과 같은 상태 형식과 노드로 만듭니다.
다음 두 셀은 01절 2절의 상태 형식 셀·노드 셀과 글자까지 같습니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.293648Z', 'iopub.status.busy': '2026-09-25T08:37:26.293602Z', 'iopub.status.idle': '2026-09-25T08:37:26.295111Z', 'shell.execute_reply': '2026-09-25T08:37:26.294871Z'}}

```python
# 합계·이번 수·실행 흔적 칸을 둔 상태 형식을 만듭니다(실행 흔적 칸에만 Ch 13 02절 이어 붙이기 규칙)
class CountState(TypedDict):
    total: int
    amount: int
    trace: Annotated[list[str], operator.add]
```

출력:
```

```

### [22] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
칸 `total`은 합계, `amount`는 이번 수, `trace`는 실행 흔적입니다.

다음 셀은 01절과 같은 노드 함수입니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.295541Z', 'iopub.status.busy': '2026-09-25T08:37:26.295499Z', 'iopub.status.idle': '2026-09-25T08:37:26.296881Z', 'shell.execute_reply': '2026-09-25T08:37:26.296588Z'}}

```python
# 합계 칸에 이번 수를 더한 값과, 실행 흔적에 넣을 자기 이름을 냅니다
def add_amount(state):
    new_total = state["total"] + state["amount"]
    # 규칙을 적은 실행 흔적 칸에는 자기 몫 한 칸만 냅니다(Ch 13 02절)
    return {"total": new_total, "trace": ["add"]}
```

출력:
```

```

### [24] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
함수 `add_amount`는 합계에 이번 수를 더한 값과, 실행 흔적 한 칸을 냅니다.

다음 셀은 01절처럼 노드 하나와 엣지 둘을 설계 객체에 적습니다.
컴파일할 때 인자 `checkpointer`에 3절의 PostgreSQL 체크포인터를 넘깁니다.
01절 4절과 다른 곳은 넘긴 체크포인터 하나뿐입니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.297377Z', 'iopub.status.busy': '2026-09-25T08:37:26.297334Z', 'iopub.status.idle': '2026-09-25T08:37:26.299878Z', 'shell.execute_reply': '2026-09-25T08:37:26.299553Z'}}

```python
# 01절과 같은 노드 하나·엣지 둘을 설계 객체에 적고, PostgreSQL 체크포인터와 함께 컴파일합니다
builder = StateGraph(CountState)
builder.add_node("add", add_amount)
builder.add_edge(START, "add")
builder.add_edge("add", END)
graph = builder.compile(checkpointer=saver)
print("붙은 체크포인터의 종류:", type(graph.checkpointer).__name__)
```

출력:
```
붙은 체크포인터의 종류: PostgresSaver

```

### [26] markdown {}

**결과 읽기** — 출력 줄 `붙은 체크포인터의 종류: PostgresSaver`입니다.
그래프에 PostgreSQL 체크포인터가 붙었습니다.
아직 메서드 `setup()`을 부르지 않았으니, 2절에서 만든 이름 공간에는 표가 없습니다.

다음 셀은 01절 5절과 같은 설정 딕셔너리를 만듭니다.
스레드 이름도 01절과 같은 `customer-a`입니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.300463Z', 'iopub.status.busy': '2026-09-25T08:37:26.300418Z', 'iopub.status.idle': '2026-09-25T08:37:26.301903Z', 'shell.execute_reply': '2026-09-25T08:37:26.301592Z'}}

```python
# 설정 딕셔너리의 키 configurable 아래에 스레드 이름 thread_id를 적습니다
config_a = {"configurable": {"thread_id": "customer-a"}}
print("스레드 customer-a의 설정:", config_a)
```

출력:
```
스레드 customer-a의 설정: {'configurable': {'thread_id': 'customer-a'}}

```

### [28] markdown {}

**결과 읽기** — 출력 줄 `스레드 customer-a의 설정: {'configurable': {'thread_id': 'customer-a'}}`입니다.
01절 노트북의 체크포인트는 그 커널의 메모리에 있었고, 이 노트북과는 상관이 없습니다.

### [29] markdown {'lesson_part': 'before'}

## 5. 표를 만들기 전에 실행하기 (Before)

### [30] markdown {'lesson_part': 'before'}

다음 셀은 표 만들기 `setup()`을 부르지 않은 채, 01절 첫 실행과 같은 입력으로 그래프를 실행합니다.
실행 전에 예상해 봅니다.
체크포인트를 담을 표가 없으니, 어딘가에서 멈출 것입니다.
이 셀만 올라온 오류를 받아 출력하고, 셀은 끝까지 갑니다.
받는 오류는 Ch 12 02절처럼 psycopg 오류 전체인 `psycopg.Error`입니다.

### [31] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.302408Z', 'iopub.status.busy': '2026-09-25T08:37:26.302355Z', 'iopub.status.idle': '2026-09-25T08:37:26.306713Z', 'shell.execute_reply': '2026-09-25T08:37:26.306333Z'}, 'lesson_part': 'before'}

```python
# 표 만들기 setup()을 부르지 않은 채 01절 첫 실행과 같은 입력으로 실행합니다(이 셀만 올라온 오류를 받아 출력합니다)
try:
    graph.invoke({"total": 0, "amount": 3, "trace": []}, config_a)
except psycopg.Error as error:
    print("받은 오류:", type(error).__name__)
    # diag.message_primary는 서버가 보낸 오류 글, sqlstate는 오류 번호입니다
    print("오류 글:", error.diag.message_primary)
    print("오류 번호:", error.sqlstate)
```

출력:
```
받은 오류: UndefinedTable
오류 글: relation "checkpoints" does not exist
오류 번호: 42P01

```

### [32] markdown {'lesson_part': 'before'}

**결과 읽기** — 출력 줄 `받은 오류: UndefinedTable`입니다.
오류 글 `relation "checkpoints" does not exist`는 표 `checkpoints`가 없다는 뜻입니다.
출력 줄 `오류 번호: 42P01`은 PostgreSQL이 이 오류에 붙이는 다섯 글자 번호입니다.
오류 이름 `UndefinedTable`은 `psycopg.Error`의 한 종류라, 이 `except` 줄이 받았습니다.

설치판 소스로 보면, 그래프는 실행을 시작할 때 그 스레드의 마지막 체크포인트를 먼저 찾습니다.
찾을 표가 없어 그 자리에서 멈췄고, 메서드 `invoke`는 결과를 내놓지 못했습니다.
오류를 받지 않는 실제 프로그램이라면 여기서 멈춥니다.
이것이 이 절의 Before 결함입니다.
노트북 밖에서 본 `OperationalError`는 서버가 꺼져서 난 오류였고, 이 오류는 서버에 붙었지만 표가 없어서 났습니다.

다음 셀은 실행이 멈춘 뒤, 이름 공간 `ch23_lab`에 표가 생겼는지 다시 봅니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.307272Z', 'iopub.status.busy': '2026-09-25T08:37:26.307229Z', 'iopub.status.idle': '2026-09-25T08:37:26.308807Z', 'shell.execute_reply': '2026-09-25T08:37:26.308612Z'}, 'lesson_part': 'before'}

```python
# 실행이 멈춘 뒤, 이름 공간 ch23_lab에 표가 생겼는지 다시 봅니다
print("ch23_lab 안의 표:", table_names(cur))
```

출력:
```
ch23_lab 안의 표: []

```

### [34] markdown {'lesson_part': 'before'}

**결과 읽기** — 출력 줄 `ch23_lab 안의 표: []`로, 표는 여전히 하나도 없습니다.
체크포인터를 붙인 그래프를 실행해도, 이 체크포인터는 표를 스스로 만들지 않았습니다.

### [35] markdown {'lesson_part': 'after'}

## 6. 표를 만든 뒤 실행하기 (After)

### [36] markdown {'lesson_part': 'after'}

이제 결함을 고칩니다.
표 만들기(`setup()`)는 체크포인터가 쓸 표를 데이터베이스에 만드는 일입니다.
빈 사진첩에 속지를 끼워, 사진을 꽂을 자리를 먼저 마련하는 것과 같습니다.
다음 셀은 3절의 문장들을 실행하는 메서드 `saver.setup()`을 부르고, 이름 공간 `ch23_lab`의 표를 다시 봅니다.
셀 끝 `assert`는 실행마다 같아야 하는 표 수에만 겁니다.

### [37] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.309371Z', 'iopub.status.busy': '2026-09-25T08:37:26.309322Z', 'iopub.status.idle': '2026-09-25T08:37:26.319617Z', 'shell.execute_reply': '2026-09-25T08:37:26.319332Z'}, 'lesson_part': 'after'}

```python
# 표 만들기 setup()을 부르고, 이름 공간 ch23_lab에 생긴 표를 봅니다
saver.setup()
names_after = table_names(cur)
print("setup() 뒤 표 수:", len(names_after))
print("ch23_lab 안의 표:", names_after)
# 설치판의 표 만들기 문장이 정하는 수라, 실행마다 같아야 합니다
assert len(names_after) == 4, "setup() 뒤 표는 넷이어야 합니다"
```

출력:
```
setup() 뒤 표 수: 4
ch23_lab 안의 표: ['checkpoint_blobs', 'checkpoint_migrations', 'checkpoint_writes', 'checkpoints']

```

### [38] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `setup() 뒤 표 수: 4`입니다.
라벨 `ch23_lab 안의 표:` 뒤 목록에 표 넷이 이름 차례로 있습니다.
표 `checkpoints`는 체크포인트를 한 줄씩 담는 표이고, 7절에서 줄을 셉니다.
나머지 셋의 쓰임은 설치판 소스로 보면 이렇습니다.
표 `checkpoint_blobs`는 수·글이 아닌 칸 값을, `checkpoint_writes`는 체크포인트에 딸린 쓰기를 따로 담습니다.

표 `checkpoint_migrations`는 표 만들기 기록입니다.
표 만들기 기록은 표 만들기 문장 가운데 어디까지 실행했는지 판 번호로 적어 두는 표입니다.
속지를 끼울 때마다 끼운 차례를 적어 두는 목록과 같습니다.
다음 셀은 이 표에 적힌 판 번호를 작은 것부터 읽습니다.

### [39] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.320139Z', 'iopub.status.busy': '2026-09-25T08:37:26.320092Z', 'iopub.status.idle': '2026-09-25T08:37:26.321829Z', 'shell.execute_reply': '2026-09-25T08:37:26.321505Z'}, 'lesson_part': 'after'}

```python
# 표 만들기 기록 checkpoint_migrations에 적힌 판 번호를 작은 것부터 읽습니다
cur.execute("SELECT v FROM ch23_lab.checkpoint_migrations ORDER BY v")
versions = []
for row in cur.fetchall():
    versions.append(row[0])
print("표 만들기 기록 줄 수:", len(versions))
print("판 번호:", versions)
```

출력:
```
표 만들기 기록 줄 수: 10
판 번호: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

```

### [40] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `표 만들기 기록 줄 수: 10`과 `판 번호: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`입니다.
3절에서 본 표 만들기 문장 열 개가 모두 실행되어, 문장마다 판 번호 한 줄이 적혔습니다.
설치판 소스에서 `setup()`은 먼저 이 기록 표를 만드는 0번 문장을 실행합니다.
그 문장은 표가 이미 있으면 아무 일도 하지 않고, 그다음에는 마지막 판 번호 뒤 문장만 실행합니다.
그래서 이 기록이 있으면, 이미 실행한 1번부터의 문장은 다시 실행하지 않습니다.

다음 셀은 5절과 같은 입력으로 스레드 `customer-a`의 첫 실행을 합니다.
실행 전에 예상해 봅니다.
이제 표가 있으니 01절 첫 실행처럼 합계 3이 나올 것입니다.

### [41] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.322336Z', 'iopub.status.busy': '2026-09-25T08:37:26.322283Z', 'iopub.status.idle': '2026-09-25T08:37:26.327420Z', 'shell.execute_reply': '2026-09-25T08:37:26.327115Z'}, 'lesson_part': 'after'}

```python
# 5절 Before와 같은 입력으로 스레드 customer-a의 첫 실행을 합니다
first_result = graph.invoke({"total": 0, "amount": 3, "trace": []}, config_a)
print("첫 실행 결과:", first_result)
```

출력:
```
첫 실행 결과: {'total': 3, 'amount': 3, 'trace': ['add']}

```

### [42] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `첫 실행 결과: {'total': 3, 'amount': 3, 'trace': ['add']}`는 01절 첫 실행과 같습니다.
5절과 같은 그래프·체크포인터·입력이고, 달라진 것은 `setup()` 한 줄뿐입니다.

다음 셀은 01절 6절처럼 같은 스레드로 이번 수 4만 넣어 다시 실행합니다.
체크포인터가 표에서 합계 3을 읽어 오면, 01절처럼 합계 7이 될 것입니다.
셀 끝 `assert`는 실행마다 같아야 하는 합계에만 겁니다.

### [43] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.327935Z', 'iopub.status.busy': '2026-09-25T08:37:26.327885Z', 'iopub.status.idle': '2026-09-25T08:37:26.331763Z', 'shell.execute_reply': '2026-09-25T08:37:26.331544Z'}, 'lesson_part': 'after'}

```python
# 같은 스레드로 이번 수 4만 넣어 다시 실행합니다(01절 6절 둘째 실행과 같은 입력)
second_result = graph.invoke({"amount": 4}, config_a)
print("둘째 실행 결과:", second_result)
# 표에 저장된 합계 3에서 이어 가므로, 실행마다 같아야 하는 값입니다
assert second_result["total"] == 7, "같은 스레드의 둘째 실행은 합계 7이어야 합니다"
```

출력:
```
둘째 실행 결과: {'total': 7, 'amount': 4, 'trace': ['add', 'add']}

```

### [44] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `둘째 실행 결과: {'total': 7, 'amount': 4, 'trace': ['add', 'add']}`입니다.
합계가 표에 저장된 3에서 이어져 7이 되었고, 01절 6절과 같은 값입니다.
체크포인터를 `InMemorySaver`에서 `PostgresSaver`로 바꿔도, 같은 스레드로 다시 실행한 결과는 같았습니다.

## 7. 표의 구조와 쌓인 줄 보기

이 절 제목의 마지막 말은 체크포인터가 쓰는 표들의 구조, 곧 표 이름과 표의 칸을 가리킵니다.
SQL 낱말 `SCHEMA`는 같은 영어 낱말이지만, 이 절은 그것을 이름 공간이라고 불렀습니다.
표 이름은 6절에서 보았으니, 이번에는 표 `checkpoints`의 칸을 봅니다.
다음 셀은 표 하나의 칸 이름을 놓인 차례대로 읽는 함수입니다.
표 이름은 이 문장의 값 자리라, Ch 12 02절처럼 자리표시자 `%s`로 넘깁니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.332280Z', 'iopub.status.busy': '2026-09-25T08:37:26.332236Z', 'iopub.status.idle': '2026-09-25T08:37:26.333809Z', 'shell.execute_reply': '2026-09-25T08:37:26.333574Z'}, 'lesson_part': 'after'}

```python
# 이름 공간 ch23_lab의 표 하나에 있는 칸 이름을 놓인 차례대로 읽어, 목록으로 내놓습니다
def column_names(cursor, table_name):
    sql = "SELECT column_name FROM information_schema.columns"
    sql = sql + " WHERE table_schema = 'ch23_lab' AND table_name = %s"
    sql = sql + " ORDER BY ordinal_position"
    cursor.execute(sql, (table_name,))
    names = []
    for row in cursor.fetchall():
        names.append(row[0])
    return names
```

출력:
```

```

### [46] markdown {'lesson_part': 'after'}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
목록 `columns`는 `tables`와 같은 이름 공간 `information_schema`에 있고, 표의 칸을 한 줄씩 보여 줍니다.
칸 `ordinal_position`은 그 표에서 칸이 놓인 차례입니다.

다음 셀은 표 `checkpoints`의 칸 이름을 봅니다.

### [47] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.334385Z', 'iopub.status.busy': '2026-09-25T08:37:26.334331Z', 'iopub.status.idle': '2026-09-25T08:37:26.337922Z', 'shell.execute_reply': '2026-09-25T08:37:26.337618Z'}, 'lesson_part': 'after'}

```python
# 체크포인트를 담는 표 checkpoints의 칸 이름을 봅니다
print("표 checkpoints의 칸:", column_names(cur, "checkpoints"))
```

출력:
```
표 checkpoints의 칸: ['thread_id', 'checkpoint_ns', 'checkpoint_id', 'parent_checkpoint_id', 'type', 'checkpoint', 'metadata']

```

### [48] markdown {'lesson_part': 'after'}

**결과 읽기** — 라벨 `표 checkpoints의 칸:` 뒤 목록에 칸 이름 일곱 개가 있습니다.
칸 `thread_id`에 스레드 이름이 들어가, 한 표 안에서 스레드마다 줄을 가를 수 있습니다.
칸 `checkpoint`에는 체크포인트 내용이 들어갑니다.
칸 `checkpoint_id`는 체크포인트마다 다른 이름이라, 이 절은 그 값을 출력하지 않습니다.

다음 셀은 표 `checkpoints`에서 스레드 이름 하나의 줄 수를 세는 함수입니다.
스레드 이름을 자리표시자 `%s`로 넘기고, Ch 12 02절처럼 `count(*)`로 줄 수를 셉니다.

### [49] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.338438Z', 'iopub.status.busy': '2026-09-25T08:37:26.338389Z', 'iopub.status.idle': '2026-09-25T08:37:26.339680Z', 'shell.execute_reply': '2026-09-25T08:37:26.339498Z'}, 'lesson_part': 'after'}

```python
# 표 checkpoints에서 스레드 이름 하나의 줄 수를 셉니다(스레드 이름은 자리표시자 %s로 넘김)
def count_checkpoints(cursor, thread_name):
    sql = "SELECT count(*) FROM ch23_lab.checkpoints WHERE thread_id = %s"
    cursor.execute(sql, (thread_name,))
    return cursor.fetchone()[0]
```

출력:
```

```

### [50] markdown {'lesson_part': 'after'}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
원소 하나짜리 튜플 `(thread_name,)`은 값 하나를 자리표시자에 넘기는 모양입니다.

다음 셀은 스레드 `customer-a`의 체크포인트를 두 가지로 셉니다.
하나는 01절의 메서드 `get_state_history`, 다른 하나는 표 `checkpoints`의 줄 수입니다.
표는 체크포인터의 연결이 아니라, 2절에서 연 연결로 셉니다.
셀 끝 `assert`는 두 수가 같은지에만 겁니다.

### [51] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.340146Z', 'iopub.status.busy': '2026-09-25T08:37:26.340099Z', 'iopub.status.idle': '2026-09-25T08:37:26.342874Z', 'shell.execute_reply': '2026-09-25T08:37:26.342538Z'}, 'lesson_part': 'after'}

```python
# 스레드 customer-a의 체크포인트 목록 수와, 2절 연결로 센 표 checkpoints의 줄 수를 견줍니다
history_a = list(graph.get_state_history(config_a))
print("get_state_history로 센 수:", len(history_a))
rows_a = count_checkpoints(cur, "customer-a")
print("표 checkpoints의 customer-a 줄 수:", rows_a)
# 체크포인트 하나가 한 줄이라, 실행마다 같아야 하는 관계입니다
assert rows_a == len(history_a), "체크포인트 수와 표의 줄 수가 같아야 합니다"
```

출력:
```
get_state_history로 센 수: 6
표 checkpoints의 customer-a 줄 수: 6

```

### [52] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `get_state_history로 센 수: 6`과 `표 checkpoints의 customer-a 줄 수: 6`입니다.
01절처럼 실행 두 번에 체크포인트가 셋씩, 모두 여섯이 쌓였습니다.
체크포인트 하나가 표 `checkpoints`의 한 줄입니다.
체크포인터가 쓴 줄을, 다른 연결에서도 같은 수로 셀 수 있었습니다.

## 8. 값 바꿔 보기 · 표 만들기를 한 번 더, 스레드 이름 바꾸기

첫째로 바꿀 것은 `setup()`을 부르는 횟수입니다.
실행 전에 예상해 봅니다.
표 만들기 기록이 있으니 새로 실행할 문장이 없어, 기록은 열 줄 그대로일 것입니다.
표 `checkpoints`에 쌓인 줄도 그대로 남을 것입니다.

### [53] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.343393Z', 'iopub.status.busy': '2026-09-25T08:37:26.343349Z', 'iopub.status.idle': '2026-09-25T08:37:26.345361Z', 'shell.execute_reply': '2026-09-25T08:37:26.345049Z'}, 'lesson_part': 'after'}

```python
# 값 바꿔 보기: 표가 이미 있는데 setup()을 한 번 더 부르고, 기록과 쌓인 줄을 다시 셉니다
saver.setup()
cur.execute("SELECT count(*) FROM ch23_lab.checkpoint_migrations")
print("둘째 setup() 뒤 표 만들기 기록 줄 수:", cur.fetchone()[0])
print("customer-a 줄 수:", count_checkpoints(cur, "customer-a"))
```

출력:
```
둘째 setup() 뒤 표 만들기 기록 줄 수: 10
customer-a 줄 수: 6

```

### [54] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `둘째 setup() 뒤 표 만들기 기록 줄 수: 10`과 `customer-a 줄 수: 6`입니다.
두 번째로 불러도 오류가 없었고, 표 만들기 기록과 쌓인 줄이 그대로입니다.
이 판에서는 표를 이미 만든 데이터베이스에서 `setup()`을 다시 불러도 괜찮았습니다.

둘째로 바꿀 것은 스레드 이름 하나입니다.
다음 셀은 01절 9절과 같은 셀로, 새 스레드 `customer-b`에 합계 0과 이번 수 4를 넣습니다.
실행 전에 예상해 봅니다.
표 `checkpoints`에는 스레드 `customer-b`의 줄이 따로 세 줄 생길 것입니다.

### [55] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.345860Z', 'iopub.status.busy': '2026-09-25T08:37:26.345817Z', 'iopub.status.idle': '2026-09-25T08:37:26.350011Z', 'shell.execute_reply': '2026-09-25T08:37:26.349688Z'}, 'lesson_part': 'after'}

```python
# 값 바꿔 보기: 스레드 이름만 customer-b로 바꾸고, 새 스레드라 합계 0부터 넣습니다
config_b = {"configurable": {"thread_id": "customer-b"}}
other_result = graph.invoke({"total": 0, "amount": 4, "trace": []}, config_b)
print("customer-b 실행 결과:", other_result)
```

출력:
```
customer-b 실행 결과: {'total': 4, 'amount': 4, 'trace': ['add']}

```

### [56] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `customer-b 실행 결과: {'total': 4, 'amount': 4, 'trace': ['add']}`는 01절 9절과 같습니다.

다음 셀은 두 스레드의 줄 수를 라벨 줄 아래에 차례로 출력합니다.

### [57] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.350533Z', 'iopub.status.busy': '2026-09-25T08:37:26.350487Z', 'iopub.status.idle': '2026-09-25T08:37:26.352293Z', 'shell.execute_reply': '2026-09-25T08:37:26.352006Z'}, 'lesson_part': 'after'}

```python
# 두 스레드의 표 checkpoints 줄 수를 라벨 줄 아래에 차례로 출력합니다
print("스레드 | 표 checkpoints의 줄 수")
for thread_name in ["customer-a", "customer-b"]:
    print(thread_name, "|", count_checkpoints(cur, thread_name))
```

출력:
```
스레드 | 표 checkpoints의 줄 수
customer-a | 6
customer-b | 3

```

### [58] markdown {'lesson_part': 'after'}

**결과 읽기** — 라벨 줄 `스레드 | 표 checkpoints의 줄 수` 아래 두 줄입니다.
줄 `customer-a | 6`과 `customer-b | 3`으로, 스레드마다 실행 횟수에 맞는 줄이 따로 쌓였습니다.
두 스레드의 줄은 같은 표에 있고, 칸 `thread_id`의 값으로 갈립니다.

## 9. 연결 닫기와 작업 폴더

다음 셀은 체크포인터의 연결을 먼저 닫고, 2절 연결로 스레드 `customer-a`의 줄 수를 다시 셉니다.
그다음 2절 연결도 닫습니다.
실행 전에 예상해 봅니다.
체크포인트가 데이터베이스 서버의 표에 있으니, 체크포인터 연결을 닫아도 여섯 줄 그대로일 것입니다.

### [59] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.352837Z', 'iopub.status.busy': '2026-09-25T08:37:26.352789Z', 'iopub.status.idle': '2026-09-25T08:37:26.354436Z', 'shell.execute_reply': '2026-09-25T08:37:26.354153Z'}, 'lesson_part': 'after'}

```python
# 체크포인터의 연결을 먼저 닫고 2절 연결로 줄 수를 다시 센 뒤, 2절 연결도 닫습니다
saver_conn.close()
print("체크포인터 연결 닫힘:", saver_conn.closed)
print("customer-a 줄 수:", count_checkpoints(cur, "customer-a"))
conn.close()
print("조회 연결 닫힘:", conn.closed)
```

출력:
```
체크포인터 연결 닫힘: True
customer-a 줄 수: 6
조회 연결 닫힘: True

```

### [60] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `체크포인터 연결 닫힘: True`와 `customer-a 줄 수: 6`입니다.
체크포인터의 연결을 닫은 뒤에도, 표의 줄은 그대로 남았습니다.
출력 줄 `조회 연결 닫힘: True`로 두 연결을 모두 닫았습니다.
그래프 `graph`의 체크포인터는 닫힌 연결을 가지고 있어, 이 노트북은 여기부터 그래프를 쓰지 않습니다.

다음 셀은 01절 11절처럼 작업 폴더에 파일이 생겼는지 봅니다.

### [61] code {'execution': {'iopub.execute_input': '2026-09-25T08:37:26.354931Z', 'iopub.status.busy': '2026-09-25T08:37:26.354886Z', 'iopub.status.idle': '2026-09-25T08:37:26.356686Z', 'shell.execute_reply': '2026-09-25T08:37:26.356392Z'}, 'lesson_part': 'after'}

```python
# 지금까지 실행하는 동안 작업 폴더에 파일이 생겼는지 봅니다
file_names = os.listdir()
print("현재 작업 폴더의 파일:", file_names)
print("파일 수:", len(file_names))
```

출력:
```
현재 작업 폴더의 파일: []
파일 수: 0

```

### [62] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `현재 작업 폴더의 파일: []`과 `파일 수: 0`입니다.
체크포인트는 작업 폴더가 아니라 데이터베이스 서버에 저장되었습니다.

## 정리

1. 표 만들기 전에 실행하자, 표 `checkpoints`가 없어 오류 `UndefinedTable`을 받았습니다.
2. 메서드 `setup()`은 표 넷을 만들고, 표 만들기 기록에 판 번호 열 줄을 적었습니다.
3. 표를 만든 뒤에는 01절처럼 합계 7이 되었고, 체크포인트 여섯이 표에 여섯 줄로 쌓였습니다.

03절에서는 연결과 그래프 객체를 새로 만들어도, 같은 스레드의 대화를 이어 가는지 봅니다.

## 그림

### 02-1-연결-둘과-이름-공간-하나.mmd

```mermaid
flowchart TB
  %% classes
  url["접속 글 하나<br>127.0.0.1:55432 · rag_lab"]:::tool
  qc["조회 연결 conn<br>autocommit=True"]:::tool
  sc["체크포인터 연결 saver_conn<br>autocommit=True<br>dict_row<br>search_path ch23_lab"]:::tool
  sv["체크포인터 PostgresSaver<br>그래프 graph에 붙음"]
  subgraph ns["이름 공간 ch23_lab"]
    direction TB
    tb["setup() 뒤 표 넷<br>checkpoints<br>checkpoint_blobs<br>checkpoint_writes<br>checkpoint_migrations"]:::measure
  end
  url --> qc
  url --> sc
  sc --> sv
  sv -->|체크포인트를 씀| ns
  qc -->|표 이름과 줄 수를 읽음| ns
```

접속 글 하나로 연결 둘을 열어, 하나는 체크포인터에 넘기고 하나로는 이름 공간 ch23_lab의 표를 직접 읽습니다.

### 02-2-표-만들기-문장-열과-기록-열-줄.mmd

```mermaid
flowchart TB
  %% classes
  ms["표 만들기 문장 열 개<br>속성 MIGRATIONS<br>번호 0부터 9"]
  s1["saver.setup()<br>처음 부름"]:::flow
  subgraph rs["setup() 뒤 이름 공간 ch23_lab"]
    direction LR
    tt["표 넷"]:::measure
    mg["표 만들기 기록<br>판 번호 0부터 9 · 열 줄"]:::measure
    tt ~~~ mg
  end
  s2["saver.setup()<br>한 번 더"]:::flow
  r2["기록 열 줄 그대로<br>customer-a 여섯 줄 그대로"]:::measure
  ms --> s1
  s1 --> rs
  rs --> s2
  s2 --> r2
```

표 만들기 문장 열 개가 한 번씩 실행되어 판 번호 열 줄이 적혔고, 둘째 setup()은 기록을 늘리지 않았습니다.

### 02-3-표를-만들기-전과-뒤.mmd

```mermaid
flowchart TB
  %% classes
  gr["같은 그래프 graph<br>같은 체크포인터<br>스레드 customer-a<br>입력 total 0 · amount 3"]:::flow
  subgraph bf["Before · setup() 없이"]
    direction TB
    b1["받은 오류 UndefinedTable<br>표 checkpoints 없음<br>오류 번호 42P01"]:::fail
    b2["멈춘 뒤에도<br>ch23_lab 안의 표 없음"]:::fail
    b1 --> b2
  end
  subgraph af["After · setup() 뒤"]
    direction TB
    a1["표 넷<br>표 만들기 기록 열 줄"]:::measure
    a2["첫 실행 합계 3<br>둘째 실행 amount 4 · 합계 7"]:::measure
    a1 --> a2
  end
  gr --> bf
  gr --> af
```

같은 그래프와 같은 입력인데, 표를 만들기 전에는 UndefinedTable을 받고 표를 만든 뒤에는 01절처럼 합계 7이 됩니다.

### 02-4-스레드마다-표에-쌓인-줄.mmd

```mermaid
flowchart TB
  %% classes
  subgraph ta["스레드 customer-a"]
    direction TB
    h1["get_state_history<br>체크포인트 여섯"]:::measure
    r1["표 checkpoints<br>여섯 줄"]:::measure
    h1 ~~~ r1
  end
  subgraph tbb["스레드 customer-b"]
    direction TB
    h2["실행 결과<br>합계 4"]:::measure
    r2["표 checkpoints<br>세 줄"]:::measure
    h2 ~~~ r2
  end
  cm["두 스레드 모두<br>같은 표 checkpoints<br>칸 thread_id의 값으로 갈림"]
  cl["체크포인터 연결을<br>닫은 뒤에도<br>customer-a 여섯 줄<br>작업 폴더 파일 없음"]:::measure
  ta ~~~ cm
  tbb ~~~ cm
  cm ~~~ cl
```

두 스레드의 체크포인트가 같은 표 checkpoints에 여섯 줄과 세 줄로 쌓였고, 체크포인터 연결을 닫은 뒤에도 줄 수는 그대로였습니다.

### 02-5-속지를-끼운-사진첩과-빈-사진첩.prompt.md

# 02-5-속지를-끼운-사진첩과-빈-사진첩 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 사진을 오래 남기려면, 사진을 꽂아 둘 사진첩이 있어야 합니다. 그런데 새로 산 사진첩에는 비닐 속지가 끼워져 있지 않습니다. 속지가 없으면 사진을 찍고도 꽂을 자리가 없습니다. … 데이터베이스의 이름 공간이 사진첩 한 권이고, 표가 속지입니다. 메서드 `setup()`은 빈 사진첩에 속지를 끼우는 일이고 … 사진 한 장이 표 `checkpoints`의 한 줄, 곧 체크포인트 하나입니다.

구성 요소와 배치: 넓은 나무 탁자 하나 위에 **펼친 고리 사진첩 둘**(= 이름 공간 `ch23_lab`의 Before·After) · 왼쪽 사진첩은 **고리에 속지 없음**(= `setup()` 전, 표 없음) + 사진첩 밖 탁자에 **즉석사진 한 장**(= 꽂을 자리가 없는 체크포인트, Before 결함) · 오른쪽 사진첩은 **비닐 속지**(= 표 `checkpoints`)에 **즉석사진 여섯 장**(= `customer-a` 체크포인트 여섯, 표의 여섯 줄) · 두 사진첩 사이에 **즉석카메라 하나**(= 체크포인터, 01절 짝). 사람·손·화살표·화면·시계·앞 챕터 소품(쟁반·서랍·바구니·저울·울타리·발자국·공구판·승강 상자·식당 전표·집게·세탁기·선반·도장·카드·봉투) 없음.

시선 순서: 두 사진첩(속지 없음 ↔ 속지 있음) → 왼쪽 밖에 떨어진 사진 한 장 ↔ 오른쪽 속지의 사진 여섯 장 → 가운데 카메라.

검수 기준: 그림만 보고 「왼쪽은 꽂을 자리가 없어 사진이 밖에 있고, 오른쪽은 속지에 사진이 꽂혀 있다」가 읽히는가. 사진 수(왼쪽 밖 한 장·오른쪽 여섯 장)와 카메라 하나를 셀 수 있는가. 글자·숫자·사람이 없는가.

비유 계열: 챕터 리드 결정 11 **「체스판과 즉석사진」**(01절이 엶). 인계의 02 후보(빈 사진첩에 속지를 먼저 붙이기 ↔ 사진첩 없이 쌓인 사진, 「선반」 금지)를 따름.

## 프롬프트 (1차, 탈락)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. Exactly two identical open ring-binder photo albums lie side by side on a wide wooden table, with a clear gap between them. The left album is empty: its metal rings hold no pages at all, and exactly one instant photo lies loose on the table beside it. The right album has exactly four clear plastic pocket pages on its rings, fanned out so all four page edges are clearly visible; the top page holds exactly six instant photos in two neat rows of three. Every instant photo has a thick white frame and shows a tiny chessboard. Exactly one instant camera sits on the table between the two albums. No people, no hands, no arrows, no screens, no clocks, no trays, no drawers, no baskets, no shelves, no envelopes, no clips.
```

## 프롬프트 (2차, 채택)

1차에서 오른쪽 맨 위 속지의 사진이 아홉 장(세 장씩 세 줄)으로 나왔고, 겹친 속지의 수도 셀 수 없었습니다. 속지 넷을 그리려던 것을 빼고 「속지 한 장, 주머니 여섯」으로 줄였고, 왼쪽 사진이 사진첩에 닿지 않게 적었습니다.

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. Exactly two identical open ring-binder photo albums lie side by side on a wide wooden table, with a clear gap between them. The left album is empty: its metal rings hold no pages at all, and exactly one instant photo lies loose on the table next to it, not touching the album. The right album holds exactly one clear plastic pocket page on its rings. That page has exactly six pockets in two neat rows of three, and each pocket holds one instant photo. Every instant photo has a thick white frame and shows a tiny chessboard. Exactly one instant camera sits on the table between the two albums. No other pages, no other photos. No people, no hands, no arrows, no screens, no clocks, no trays, no drawers, no baskets, no shelves, no envelopes, no clips.
```

## 상태

- 2026-09-25 · `nano_banana_pro`(`jobs_wait` 응답 모델 이름 `nano_banana_2` — 01-5와 같은 표시) · 16:9 · 2k · `use_unlim: false` · count 1. 생성 전 잔액 **2445.75**(바로 앞 거래 08:05:55Z는 01절 몫).
- **1차 job `a9632856-4ca1-4d66-90b4-956ca02806a1` 탈락** — 거래 **2026-09-25T08:39:59Z 「Nano Banana Pro −2」**(결과 파일 이름 `hf_20260925_083959_a9632856…`). 결과 원본 `5d1177739a49ffe99d2c2987e79845ca8ef270bd4dd5bc2a06d4364b98855256`(2752 × 1536). 폭 1100 사본과 오른쪽 부분 확대를 직접 보고 세어 보니 **맨 위 속지의 사진이 아홉 장(세 장씩 세 줄)**이고, 아래 속지에도 사진 가장자리가 보이며 겹친 속지 수를 셀 수 없었습니다 — 검수 기준 「오른쪽 여섯 장」에 맞지 않아 탈락(서비스 쪽 실패 아님, 재생성 1회 사용). 왼쪽 빈 고리·사진 한 장·카메라 하나는 맞았습니다.
- **2차 job `21f990d2-0483-48b0-ac22-14fdae21a1f5` 채택** — 거래 **2026-09-25T08:42:00Z 「Nano Banana Pro −2」**(결과 파일 이름 `hf_20260925_084200_21f990d2…`와 시각이 같음). 이 절 몫은 거래 두 줄, **4크레딧**(잔액 2445.75 → 2441.75). 결과 원본 `fe4ab9c23c375cebac40611686a7b8fea6834430ab6afbb6fb37ee6843aa0139`(2752 × 1536).
- **그림에서 확인한 것(그림 읽기·alt에 반영)**: 흰 바탕 위 넓은 나무 탁자 하나. 탁자 위에 **펼친 고리 사진첩 둘**(왼쪽·오른쪽, 둘 다 파란 표지). **왼쪽 사진첩**: 고리 넷에 비닐 속지가 없고, 안쪽 오른편에 파란 판(한쪽에 작은 턱이 있는 판 — 사진을 꽂는 속지가 아님)만 있음. 왼쪽 사진첩 밖 왼쪽 아래 탁자 위에 **즉석사진 한 장**(사진첩에 닿지 않음). **오른쪽 사진첩**: 고리에 **비닐 속지 한 장**, 주머니 여섯에 **즉석사진 여섯 장 — 두 장씩 세 줄**(프롬프트의 「세 장씩 두 줄」과 방향만 다름, 수는 맞음). 사진마다 흰 테두리 안에 작은 체스판. 두 사진첩 사이 앞쪽에 **초록빛 즉석카메라 하나**. 글자·숫자·사람·손·화살표·화면·시계·쟁반·서랍·바구니·선반·봉투·집게 없음.
- 저장: 기기 셸에서 결과 URL을 `curl`로 받아(`/tmp/ch23-02/illu-2-orig.png`) `UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pillow`로 RGB·폭 1100px(LANCZOS)로 줄여 `figures/02-5-속지를-끼운-사진첩과-빈-사진첩.png`(1100 × 614, `02f1edef4afc4ff4144577ea971d1114a56f39725dde8355a2d7bf47788ba545`)로 저장했습니다.
- 결과 URL을 한 번 더 받아(`illu-2-again.png`, 원본과 해시 같음) 같은 폭으로 줄인 그림과 저장 PNG를 픽셀 대조했습니다(`ImageChops.difference` bbox `None`, 최대 차이 0). 1차 탈락본과는 다름(bbox 전체, 최대 차이 255). 같은 파일(`.cache/ch23-02-view/illu-2-1100.png`, 해시 같음)을 직접 열어 개수를 세고 그림 읽기를 썼습니다.

