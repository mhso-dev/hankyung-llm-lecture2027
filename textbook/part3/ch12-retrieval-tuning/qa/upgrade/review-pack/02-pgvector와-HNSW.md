# 02-pgvector와-HNSW

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 1h | 실습 3h | 코드 notebooks/02-pgvector와-HNSW.ipynb | 새 용어 8 -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul><li>이 절을 마치면 pgvector 표에 벡터를 넣고 거리 연산자로 가까운 문서를 받을 수 있습니다.</li><li>HNSW 색인을 만들고 실행 계획이 어느 읽기 방법을 골랐는지 확인할 수 있습니다.</li><li>색인 경로와 순차 스캔 경로의 결과를 01절 정확 검색 순위와 견줄 수 있습니다.</li></ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>01절 정확 검색은 문서를 모두 재므로 문서가 늘면 계산할 값도 늘어납니다. 그래서 실제 서비스는 벡터를 데이터베이스에 저장하고 색인으로 후보를 줄입니다. 색인은 후보를 모두 살펴보지 않으므로 정확 검색과 다른 결과가 나올 수 있습니다.</p><p>이 절은 01절과 같은 문서 12개 벡터를 PostgreSQL 표에 넣고 두 읽기 방법을 견줍니다. 자료형과 차원 수, 거리 연산자, 색인 설정을 함께 적어 두어야 같은 결과를 다시 만들 수 있습니다. 색인을 만들면 검색이 늘 색인을 타는지도 실행으로 확인합니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>01절에서 문서 12개와 질문 8개를 숫자 256개짜리 벡터로 바꿨습니다. 코사인 유사도를 NumPy로 계산하고, 가장 큰 값 1에서 빼 코사인 거리로 만들었습니다. 첫 질문의 상위 3개는 <code>LIB-004</code>·<code>LIB-001</code>·<code>LIB-003</code>이었습니다. 이 절은 같은 자료를 쓰고 01절 함수 <code>cosine_distance()</code>를 그대로 가져옵니다.</p><p>Ch 4 03절에서 sqlite3로 표를 만들고 <code>SELECT</code>와 <code>WHERE</code>, <code>ORDER BY</code>로 조회했습니다. 값은 자리표시자 <code>?</code>로 따로 넘겨 입력 글이 문장의 뜻을 바꾸지 못하게 막았습니다. 이 절은 같은 방법으로 PostgreSQL에 붙고 자리표시자 모양만 <code>%s</code>로 바뀝니다.</p><p>Ch 11은 정답 문서 ID와 고유 문서 목록, 자르는 자리, 재현율, 질문 평균을 가르쳤습니다. 이 절은 01절과 같은 인자 모양으로 그 함수 네 개를 가져와 씁니다.</p><p>노트북은 앞에서 배운 함수 다섯 개를 실습 폴더의 도구 파일 <code>notebooks/rag_tools.py</code>에서 한 줄로 가져옵니다. 01절 <code>cosine_distance()</code>와 Ch 11 지표 함수 네 개입니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>서가 두 칸에 같은 책이 같은 자리로 서 있습니다. 한 칸은 책끼리 이어 둔 끈이 없어 끝에서부터 책등을 하나씩 살펴야 합니다. 다른 칸은 책 사이에 끈이 이어져 있어 그 끈을 따라 몇 권만 살펴봅니다. 책이 몇 권뿐이라면 두 칸에서 고른 책이 같을 수 있습니다.</p>
{{img:02-5-서가와-끈|나란히 놓인 나무 서가 두 칸에 주황 책 세 권과 옅은 회색 책들이 같은 자리로 서 있고 왼쪽 칸에는 책을 잇는 것이 없으며 오른쪽 칸에는 책과 책 사이를 잇는 가는 끈이 있고 두 서가 아래 작은 나무 쟁반에 각각 주황 책 세 권이 눕혀 쌓여 있는 그림|왼쪽 칸에는 책을 잇는 끈이 없고 오른쪽 칸에는 있지만 두 쟁반에 놓인 주황 책 세 권은 같습니다.}}
<p class="look"><b>그림 읽기</b> — 서가 한 칸이 표 하나이고 책 한 권이 표의 행 하나입니다. 두 칸의 책 자리는 같고 주황 책 세 권도 같은 자리에 있습니다. 왼쪽 칸에는 책을 잇는 것이 없어 끝에서부터 차례로 살펴야 합니다. 오른쪽 칸의 가는 끈은 색인이 미리 이어 둔 이웃 관계입니다. 두 서가 아래 쟁반에 놓인 주황 책 세 권은 두 칸에서 고른 결과가 같다는 뜻입니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>pgvector</td><td>데이터베이스 PostgreSQL에 벡터 칸과 거리 연산자, 근사 검색 색인을 더해 주는 확장입니다.</td></tr><tr><td>HNSW</td><td>벡터를 여러 층의 이웃 그래프로 잇는 근사 검색 색인입니다.</td></tr><tr><td>거리 연산자 <code>&lt;=&gt;</code></td><td>두 벡터의 코사인 거리를 내는 SQL 연산자입니다. 값이 작을수록 가깝습니다.</td></tr><tr><td>연산자 클래스(operator class)</td><td>색인이 어느 자로 정렬할지 정하는 이름입니다. 코사인 거리에는 <code>vector_cosine_ops</code>를 씁니다.</td></tr><tr><td>실행 계획(execution plan)</td><td>데이터베이스가 한 질의를 어떤 방법으로 읽을지 정한 순서입니다. 그 순서를 정하는 부분을 계획기라고 부릅니다.</td></tr><tr><td>순차 스캔(sequential scan)</td><td>표의 행을 처음부터 끝까지 차례로 읽는 방법입니다.</td></tr><tr><td><code>ef_search</code></td><td>색인을 따라갈 때 살펴볼 후보 목록의 크기입니다. 기본값은 40입니다.</td></tr><tr><td><code>halfvec</code></td><td>벡터의 숫자 하나를 절반 크기로 저장하는 자료형입니다. 정밀도가 낮은 대신 색인 차원 한도가 넓습니다.</td></tr></tbody></table>
{{mermaid:02-1-두-읽기-방법|나란히 놓인 두 칸의 흐름도로 맨 위 초록 상자 질문 벡터 1개에서 왼쪽 칸 순차 스캔 경로의 파란 상자 표의 행 12개를 차례로 읽기와 파란 상자 코사인 거리 12개를 작은 값부터 정렬로 내려가고 오른쪽 칸 색인 경로의 파란 상자 이웃 그래프 따라가기와 파란 상자 살펴본 후보에서 고르기로 내려가며 두 칸이 아래 노란 상자 두 경로의 상위 세 개가 같았음으로 모이는 그림|순차 스캔은 표의 행 12개를 차례로 읽고 색인 경로는 이웃 그래프를 따라가지만 이번 상위 세 개는 같았습니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 초록 상자가 질문 벡터입니다. 왼쪽 칸이 순차 스캔 경로이고 오른쪽 칸이 색인 경로이며 두 칸 모두 위에서 아래로 읽습니다. 파란 상자 네 개는 우리가 보낸 SQL이 거치는 처리 단계입니다. 두 칸이 만나는 아래 노란 상자는 출력으로 확인한 값입니다.</p>
<h3>SQL 한 문장과 두 가지 읽기 방법</h3><p>pgvector 확장은 PostgreSQL에 <code>vector</code> 자료형과 거리 연산자를 더합니다. 칸을 <code>vector(256)</code>으로 만들면 숫자 256개짜리 벡터만 들어갑니다. 문장 <code>ORDER BY embedding &lt;=&gt; %s LIMIT %s</code>는 코사인 거리가 작은 행부터 받습니다. 받아 올 줄 수도 값으로 넘깁니다.</p><p>색인을 만들어도 데이터베이스가 늘 색인을 쓰는 것은 아닙니다. 계획기가 표의 크기와 통계를 보고 읽기 방법을 고릅니다. 그래서 검색 SQL 앞에 <code>EXPLAIN</code>을 붙여 무엇을 골랐는지 확인합니다. 색인을 쓰려면 검색 SQL의 거리 연산자와 색인의 연산자 클래스도 맞아야 합니다.</p>
{{mermaid:02-2-표에-넣고-색인-만들기|위에서 아래로 내려가는 흐름도로 초록 상자 교육용 문서 12개에서 임베딩 요청 1번 화살표를 지나 초록 상자 문서 벡터 12개로 가고 INSERT 12줄 화살표를 지나 초록 상자 표 ch12_core_hnsw로 가고 CREATE INDEX 화살표를 지나 초록 상자 HNSW 색인으로 간 뒤 맨 아래 노란 상자 색인이 있어도 계획기가 순차 스캔을 고를 수 있음으로 이어지는 그림|문서 12개를 벡터로 바꿔 표의 벡터 칸에 넣고 그 칸에 HNSW 색인을 만듭니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 초록 상자 네 개가 이 절에서 만드는 자료와 표, 색인입니다. 화살표 라벨은 그 단계에서 보내는 요청과 실행하는 SQL 문장입니다. 맨 아래 노란 상자는 색인을 만든 뒤에도 출력으로 확인한 사실입니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>01절과 같은 문서 12개를 벡터로 바꿔 표 <code>ch12_core_hnsw</code>에 넣습니다. 첫 질문을 색인 없이 검색하고, HNSW 색인을 만든 뒤 같은 SQL을 다시 실행합니다. 마지막으로 설정 <code>enable_seqscan</code>만 off로 바꿔 색인 경로로 읽게 합니다. 임베딩 요청은 문서 한 번과 질문 여덟 번으로 모두 아홉 번입니다.</p>
{{notebook:02-pgvector와-HNSW}}
{{mermaid:02-3-세-실행의-계획|위에서 아래로 내려가는 흐름도로 맨 위 파란 상자 같은 검색 SQL 한 문장에서 파란 상자 실행 1 색인 없는 표와 파란 상자 실행 2 색인 있는 표와 파란 상자 실행 3 enable_seqscan을 off로 세 갈래로 갈라지고 각각 노란 상자 계획 줄 Seq Scan과 계획 줄 Seq Scan과 계획 줄 Index Scan으로 내려간 뒤 맨 아래 노란 상자 세 실행의 상위 세 개가 같았음으로 모이는 그림|색인을 만든 실행 2까지 계획 줄은 Seq Scan이고 설정을 off로 바꾼 실행 3에서 Index Scan으로 바뀝니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 맨 위 파란 상자의 SQL 한 문장을 세 실행에서 그대로 씁니다. 가운데 파란 상자 세 개가 세 실행이고 다른 점은 색인이 있는지와 설정 하나입니다. 노란 상자 세 개는 <code>EXPLAIN</code> 출력에서 고른 계획 줄이고, 색인을 만든 실행 2에서도 순차 스캔이었습니다. 맨 아래 노란 상자는 세 실행의 상위 3개가 같았다는 출력입니다.</p>
<p class="look"><b>확인할 점</b> — 교재 출력의 판 번호는 <code>PostgreSQL 판: 17.11</code>과 <code>pgvector 확장 판: 0.8.1</code>입니다. 표에 들어간 행은 12개이고 벡터 칸은 숫자 256개짜리입니다. 세 실행의 상위 3개는 모두 <code>1 | LIB-004 | 0.43</code>, <code>2 | LIB-001 | 0.56</code>, <code>3 | LIB-003 | 0.62</code>입니다. 둘째 줄의 <code>0.56</code>은 01절이 파이썬으로 낸 값과 같습니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>질문 여덟 개를 두 경로로 모두 재니 네 칸이 질문마다 같았습니다. 질문 평균 재현율도 자리 1에서 <code>0.75</code>, 자리 2와 자리 3에서 <code>0.875</code>로 두 경로가 같았습니다. 이 값은 01절 정확 검색의 질문 평균과도 같습니다. 문서가 12개뿐이라 색인이 후보를 줄이지 못했기 때문으로 보입니다.</p><p>설정 <code>ef_search</code>를 4와 40으로 바꿨을 때도 상위 3개가 같았습니다. 다음 그림은 차원 수를 2001로 올려 색인 한도를 확인한 결과입니다.</p>
{{mermaid:02-4-차원-수와-색인-한계|나란히 놓인 두 칸의 흐름도로 왼쪽 칸 자료형 vector에서는 초록 상자 칸 vector(2001)이 노란 상자 HNSW 색인을 만들지 못함 2000차원까지라는 알림으로 내려가고 오른쪽 칸 자료형 halfvec에서는 초록 상자 칸 halfvec(2001)이 노란 상자 HNSW 색인을 만들었습니다로 내려가며 두 칸이 아래 회색 상자 이 챕터가 쓰는 숫자 256개는 한도 안으로 모이는 그림|vector 칸에는 2001차원 HNSW 색인을 만들지 못했고 halfvec 칸에는 만들었습니다.}}
<p class="look"><b>도식 읽기</b> — 왼쪽 칸이 자료형 <code>vector</code>이고 오른쪽 칸이 <code>halfvec</code>입니다. 두 칸 모두 위에서 아래로 읽습니다. 위 초록 상자는 만든 칸이고 아래 노란 상자는 코드가 받아 출력한 결과입니다. 맨 아래 회색 상자는 두 칸에 함께 해당하는 사실입니다. 이 챕터가 쓰는 숫자 256개는 두 자료형 모두에서 한도 안입니다.</p>
<p>이 결과로 어느 읽기 방법이 빠른지는 말할 수 없습니다. 검색 시간을 이번에 재지 않았고 표의 행이 12개뿐입니다. 두 경로가 같은 결과를 냈다는 것도 이번 자료에서 본 것입니다. 큰 말뭉치와 전체 질문 묶음에서 재현율과 걸린 시간을 함께 재는 일은 이번에 실행하지 않았습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>색인을 만들었다는 사실만으로 색인을 탄다고 볼 수 없습니다. 실행 계획을 함께 확인합니다.</li><li>검색 SQL의 거리 연산자와 색인의 연산자 클래스가 맞아야 색인을 쓸 수 있습니다. 코사인 거리에는 <code>vector_cosine_ops</code>를 씁니다.</li><li>이 절은 검색 시간을 재지 않았습니다. 작은 표에서는 차례로 읽는 쪽이 더 빠를 수 있고, 이번 실행에서도 계획기가 그쪽을 골랐습니다.</li><li>작은 표에서 두 경로의 결과가 같았다고 큰 자료에서도 같다고 볼 수 없습니다. 설정 <code>ef_search</code>와 말뭉치 크기를 바꿔 재현율을 함께 재야 합니다.</li><li>자료형 <code>halfvec</code>은 색인 차원 한도를 넓히지만 숫자를 절반 크기로 저장합니다. 저장 크기와 검색 품질을 함께 견줘야 합니다.</li><li>교재 출력은 pgvector 0.8.1이 든 PostgreSQL 17.11에서 만들었습니다. 실습 폴더 안내는 <code>pgvector/pgvector:0.8.2-pg17</code> 이미지를 씁니다. 그 이미지에서는 확장 판이 0.8.2이고 이번 교재 출력은 그 환경에서 만들지 않았습니다. 참고 자료로 적은 공식 문서는 v0.8.6 기준이고 이 절이 쓰는 기능의 필수 최소 판은 0.7.0입니다. 판 번호가 달라도 이 절에서 쓰는 기능은 같습니다.</li><li>데이터베이스 포트는 <code>127.0.0.1:55432</code>에만 엽니다. 실습 암호를 서비스에 쓰지 않고 접속 글을 출력하지 않습니다.</li><li>이 절은 파일을 쓰지 않습니다. 검색에 쓴 표 <code>ch12_core_hnsw</code>는 지우지 않고 그대로 남깁니다.</li><li>이 절의 문서 12개와 질문 8개는 01절과 같은 교육용 자료입니다. Ch 11 개발 분할 15문항에서 얻은 값과 나란히 놓지 않습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>벡터를 <code>vector(256)</code> 칸에 넣으면 거리 연산자 <code>&lt;=&gt;</code>로 코사인 거리 순서를 받을 수 있습니다.</li><li>색인을 만들어도 계획기가 색인 경로를 고른다고 보장하지 않습니다. 실행 계획으로 확인합니다.</li><li>이번 실행에서는 두 경로의 상위 3개와 질문 평균 재현율이 01절 정확 검색과 모두 같았습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — 03절에서는 범주 칸이 있는 표를 새로 만들고 메타데이터 필터를 함께 걸어 검색합니다. 필터를 걸면 받아 온 줄 수가 받아 올 줄 수보다 적어질 수 있습니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 4개 · 해설 포함</summary><p class="quiz-q">1. 색인을 만든 뒤에도 실행 계획을 확인해야 하는 까닭은 무엇입니까?</p><p class="quiz-a">계획기가 표의 크기와 통계를 보고 읽기 방법을 고르기 때문입니다. 이 절 실행 2에서는 색인이 있어도 순차 스캔을 골랐습니다. 틀렸다면 「SQL 한 문장과 두 가지 읽기 방법」을 다시 읽습니다.</p><p class="quiz-q">2. 코사인 거리로 정렬하는 HNSW 색인에는 어느 연산자 클래스를 씁니까?</p><p class="quiz-a">이름 <code>vector_cosine_ops</code>를 씁니다. 검색 SQL의 연산자 <code>&lt;=&gt;</code>와 짝이 맞아야 색인을 쓸 수 있습니다. 틀렸다면 「핵심 개념」의 용어 표를 다시 읽습니다.</p><p class="quiz-q">3. 숫자 2001개짜리 벡터에 HNSW 색인을 만들려면 어느 자료형을 씁니까?</p><p class="quiz-a">자료형 <code>halfvec</code>을 씁니다. 자료형 <code>vector</code>는 2000차원까지라는 알림을 냈습니다. 틀렸다면 「실험 결과 해석」의 그림을 다시 읽습니다.</p><p class="quiz-q">4. 이번 실험에서 두 경로의 결과가 같았으므로 색인이 필요 없다고 말할 수 있습니까?</p><p class="quiz-a">말할 수 없습니다. 표의 행이 12개뿐이고 검색 시간을 재지 않았습니다. 큰 자료에서 재현율과 걸린 시간을 함께 재야 합니다. 틀렸다면 「주의할 점과 실무 메모」를 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://github.com/pgvector/pgvector/tree/v0.8.6#hnsw">pgvector HNSW</a></div>색인 만들기와 <code>ef_search</code> 설명 · 확인 2026-09-18</li><li><div><a href="https://github.com/pgvector/pgvector/tree/v0.8.6#half-precision-vectors">pgvector Half-Precision Vectors</a></div>자료형 <code>halfvec</code>과 차원 한도 설명 · 확인 2026-09-18</li><li><div><a href="https://www.postgresql.org/docs/17/using-explain.html">PostgreSQL Using EXPLAIN</a></div>실행 계획 읽는 법 · 확인 2026-09-18</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# pgvector와 HNSW

**이 노트북에서 할 일**

1. 01절과 같은 문서 12개 벡터를 PostgreSQL 표의 벡터 칸에 넣습니다.
2. 거리 연산자로 가까운 문서를 받아 01절 정확 검색 순위와 대조합니다.
3. HNSW 색인을 만들고 실행 계획이 어느 읽기 방법을 고르는지 봅니다.
4. 설정 하나만 바꿔 색인 경로로 검색하고 두 경로의 결과를 견줍니다.

**준비물** — 프로젝트 맨 위 `.env` 파일의 `OPENAI_API_KEY`가 필요합니다.
pgvector 확장이 든 PostgreSQL이 `127.0.0.1:55432`에서 켜져 있어야 합니다.
실습 폴더 `README.md`의 Docker 명령으로 데이터베이스를 먼저 켭니다.
읽는 자료는 01절과 같은 문서 파일과 질문 파일 두 개입니다.

임베딩 요청은 문서 한 번과 질문 여덟 번으로 모두 아홉 번입니다.
보내는 글은 900자 아래이고 예상 비용은 0.01달러 아래입니다.
실행 시간은 40초 안팎입니다.

**데이터** — 두 파일 모두 실습 묶음에 들어 있습니다.

- 문서 `labs/part3/ch12-retrieval-tuning/data/core-documents.json`(12개)
- 질문 `labs/part3/ch12-retrieval-tuning/data/core-queries.json`(8개)

**강의와 실습 범위** — 강의 시간에는 2~4절과 9~11절을 읽습니다.
데이터베이스에 붙기, 표 만들기, 행 넣기, 실행 1과 색인 만들기, 실행 2입니다.
5절은 도구 파일에서 가져온 01절 함수를 소개하고 6절은 실행만 하고 넘어갑니다.
7·8절과 12~14절은 함께 실행하고 실습 시간에 다시 읽습니다.

**기준 버전** — 첫 셀에서 psycopg 3.3.5와 python-dotenv 1.2.3을 설치합니다.
패키지 langchain-openai 1.6.1과 numpy 2.5.3도 함께 설치합니다.
데이터베이스는 pgvector 확장이 든 PostgreSQL 17을 씁니다.
필수 최소는 pgvector 0.7.0입니다. 자료형 `halfvec`이 그 판에서 생겼습니다.

교재 출력은 PostgreSQL 17.11과 pgvector 0.8.1에서 만들었습니다.
실습 폴더 안내대로 Docker 이미지를 쓰면 확장 판 번호가 0.8.2로 나옵니다.
참고 자료로 적은 공식 문서는 v0.8.6 기준입니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 버전과 Windows·macOS에서는 이번에 실행하지 않았습니다.

실습 폴더 `labs/part3/ch12-retrieval-tuning`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![나란히 놓인 두 칸의 흐름도로 맨 위 초록 상자 질문 벡터 1개에서 왼쪽 칸 순차 스캔 경로의 파란 상자 표의 행 12개를 차례로 읽기와 파란 상자 거리 12개를 작은 값부터 정렬로 내려가고 오른쪽 칸 색인 경로의 파란 상자 이웃 그래프 따라가기와 파란 상자 살펴본 후보에서 고르기로 내려가며 두 칸이 아래 노란 상자 두 경로의 상위 3개가 같았음으로 모이는 그림](attachment:02-1-두-읽기-방법.png)

왼쪽 칸은 표의 행을 처음부터 끝까지 읽는 순차 스캔이고 오른쪽 칸은 HNSW 색인을 따라가는 경로입니다.
두 칸 모두 위에서 아래로 읽습니다.
맨 아래 노란 상자는 이 노트북의 출력으로 확인한 값입니다.

### [2] markdown {}

## 1. 준비

첫 셀은 패키지 네 개를 설치하고 설치된 버전을 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:06.492850Z', 'iopub.status.busy': '2026-09-21T07:40:06.492706Z', 'iopub.status.idle': '2026-09-21T07:40:06.976586Z', 'shell.execute_reply': '2026-09-21T07:40:06.975804Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "psycopg[binary]==3.3.5" "python-dotenv==1.2.3" "langchain-openai==1.6.1" "numpy==2.5.3"
from importlib.metadata import version

print("psycopg:", version("psycopg"))
print("python-dotenv:", version("python-dotenv"))
print("langchain-openai:", version("langchain-openai"))
print("numpy:", version("numpy"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
psycopg: 3.3.5
python-dotenv: 1.2.3
langchain-openai: 1.6.1
numpy: 2.5.3

```

### [4] markdown {}

**결과 읽기** — 설치가 끝나면 `psycopg: 3.3.5`와 `python-dotenv: 1.2.3`이 보입니다.
출력에는 `langchain-openai: 1.6.1`과 `numpy: 2.5.3`도 함께 보입니다. 네 줄이 모두 보이면 다음 셀로 넘어갑니다.
패키지 NumPy는 도구 파일이 코사인 거리를 계산할 때 씁니다.

다음 셀은 이 절에서 쓸 이름을 불러옵니다.
이름 `psycopg`는 PostgreSQL에 붙는 패키지입니다.
Ch 4 03절에서 쓴 `sqlite3`와 하는 일이 같고 붙는 데이터베이스만 다릅니다.

앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
이 노트북은 01절 `cosine_distance()`와 Ch 11 지표 함수 네 개를 가져옵니다.
Ch 11 01절 `unique_doc_ids()`·`find_gold_rank()`, 02절 `recall_at()`·`mean_score()`입니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:06.977886Z', 'iopub.status.busy': '2026-09-21T07:40:06.977779Z', 'iopub.status.idle': '2026-09-21T07:40:08.188283Z', 'shell.execute_reply': '2026-09-21T07:40:08.188063Z'}, 'lesson_role': 'setup'}

```python
# 자료 파일 읽기·데이터베이스 접속·임베딩에 쓸 이름을 불러옵니다
import json

import psycopg
from langchain_openai import OpenAIEmbeddings
# 01절과 Ch 11 01·02절 함수 다섯 개를 도구 파일에서 가져옵니다
from rag_tools import cosine_distance, find_gold_rank, mean_score
from rag_tools import recall_at, unique_doc_ids

print("불러온 이름:", "json", "psycopg", "OpenAIEmbeddings")
```

출력:
```
불러온 이름: json psycopg OpenAIEmbeddings

```

### [6] markdown {}

**결과 읽기** — 출력 줄은 `불러온 이름: json psycopg OpenAIEmbeddings` 하나입니다.
이름 `json`은 Python에 들어 있어 설치가 필요 없습니다.
도구 파일에서 가져온 함수 다섯 개는 출력하지 않습니다.

다음 셀은 API 키가 있는지 확인합니다. `True` 값이 나오면 다음으로 넘어갑니다.

### [7] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:08.190666Z', 'iopub.status.busy': '2026-09-21T07:40:08.190543Z', 'iopub.status.idle': '2026-09-21T07:40:08.194288Z', 'shell.execute_reply': '2026-09-21T07:40:08.194055Z'}, 'lesson_role': 'setup'}

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

### [8] markdown {}

**결과 읽기** — 출력 줄은 `OPENAI_API_KEY 설정 여부: True`입니다.
키 값은 출력하지 않습니다.

다음 셀은 프로젝트 맨 위 폴더를 찾습니다.
01절과 같은 코드입니다. 후보 경로를 차례로 보고 자료 폴더가 있는 곳에서 멈춥니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:08.194748Z', 'iopub.status.busy': '2026-09-21T07:40:08.194704Z', 'iopub.status.idle': '2026-09-21T07:40:08.196230Z', 'shell.execute_reply': '2026-09-21T07:40:08.196048Z'}, 'lesson_role': 'setup'}

```python
# 노트북을 어느 폴더에서 열어도 프로젝트 맨 위를 찾게 후보 세 개를 차례로 봅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part3/ch12-retrieval-tuning/data"):
        root_path = candidate
        break
print("고른 경로:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."
```

출력:
```
고른 경로: .

```

### [10] markdown {}

**결과 읽기** — 출력 줄은 `고른 경로: .`입니다. `assert`도 통과했습니다.
교재 출력은 프로젝트 맨 위를 작업 폴더로 삼아 실행해서 첫째 후보를 골랐습니다.

다음 셀은 01절이 쓴 문서 파일과 질문 파일을 그대로 읽습니다.

### [11] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:08.197105Z', 'iopub.status.busy': '2026-09-21T07:40:08.197009Z', 'iopub.status.idle': '2026-09-21T07:40:08.199425Z', 'shell.execute_reply': '2026-09-21T07:40:08.199185Z'}, 'lesson_role': 'setup'}

```python
# 01절과 같은 문서 파일과 질문 파일을 불러옵니다
data_path = root_path + "/labs/part3/ch12-retrieval-tuning/data"
with open(data_path + "/core-documents.json", encoding="utf-8") as file:
    docs = json.loads(file.read())
with open(data_path + "/core-queries.json", encoding="utf-8") as file:
    queries = json.loads(file.read())
print("문서 수:", len(docs))
print("질문 수:", len(queries))
```

출력:
```
문서 수: 12
질문 수: 8

```

### [12] markdown {}

**결과 읽기** — `문서 수: 12`와 `질문 수: 8`이 보입니다.
01절과 같은 자료라 이 절의 결과를 01절 순위와 그대로 견줄 수 있습니다.

## 2. 데이터베이스에 붙기

접속 글에는 사용자 이름과 암호, 서버 주소와 문가름 번호, 데이터베이스 이름이 들어갑니다.
이 암호는 수업 전용이라 다른 곳에 쓰지 않습니다. 접속 글은 출력하지 않습니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:08.199973Z', 'iopub.status.busy': '2026-09-21T07:40:08.199919Z', 'iopub.status.idle': '2026-09-21T07:40:08.201395Z', 'shell.execute_reply': '2026-09-21T07:40:08.201131Z'}}

```python
# 데이터베이스 접속 글과 이 절에서 쓸 표·색인 이름을 정합니다
database_url = "postgresql://student:local-practice-only@127.0.0.1:55432/rag_lab"
table_name = "ch12_core_hnsw"
index_name = "ch12_core_hnsw_idx"
print("표 이름:", table_name)
print("색인 이름:", index_name)
```

출력:
```
표 이름: ch12_core_hnsw
색인 이름: ch12_core_hnsw_idx

```

### [14] markdown {}

**결과 읽기** — `표 이름: ch12_core_hnsw`와 `색인 이름: ch12_core_hnsw_idx`가 보입니다.
표 이름을 변수에 담아 두면 SQL 문장을 만들 때 같은 이름을 되풀이해 적지 않습니다.

다음 셀은 이 절에서 되풀이해 쓸 값에 이름을 붙입니다.
숫자 `256`은 01절과 같은 벡터의 숫자 개수입니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:08.202046Z', 'iopub.status.busy': '2026-09-21T07:40:08.201981Z', 'iopub.status.idle': '2026-09-21T07:40:08.203724Z', 'shell.execute_reply': '2026-09-21T07:40:08.203436Z'}}

```python
# 이 절에서 되풀이해 쓸 값에 이름을 붙입니다
vector_dimensions = 256
top_three = 3
top_all = 12
cutoff_values = [1, 2, 3]
print("벡터의 숫자 개수:", vector_dimensions)
print("받아 올 문서 수 두 가지:", top_three, top_all)
print("자르는 자리 세 가지:", cutoff_values)
```

출력:
```
벡터의 숫자 개수: 256
받아 올 문서 수 두 가지: 3 12
자르는 자리 세 가지: [1, 2, 3]

```

### [16] markdown {}

**결과 읽기** — `벡터의 숫자 개수: 256`과 `자르는 자리 세 가지: [1, 2, 3]`이 보입니다.
`받아 올 문서 수 두 가지: 3 12` 줄의 앞 값은 상위 3개를 볼 때, 뒤 값은 자리를 끝까지 볼 때 씁니다.

다음 셀은 데이터베이스에 붙습니다.
함수 `psycopg.connect(접속 글)`은 연결 객체를 반환합니다.
인자 `autocommit=True`를 주면 문장마다 결과를 바로 확정합니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:08.204278Z', 'iopub.status.busy': '2026-09-21T07:40:08.204224Z', 'iopub.status.idle': '2026-09-21T07:40:08.224630Z', 'shell.execute_reply': '2026-09-21T07:40:08.224208Z'}}

```python
# 데이터베이스에 붙어 pgvector 확장을 켜고 두 판 번호를 봅니다
conn = psycopg.connect(database_url, autocommit=True)
cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
cur.execute("SELECT current_setting('server_version')")
print("PostgreSQL 판:", cur.fetchone()[0])
cur.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'")
print("pgvector 확장 판:", cur.fetchone()[0])
```

출력:
```
PostgreSQL 판: 17.11
pgvector 확장 판: 0.8.1

```

### [18] markdown {}

**결과 읽기** — `PostgreSQL 판: 17.11`과 `pgvector 확장 판: 0.8.1`이 보입니다.
문장 `CREATE EXTENSION IF NOT EXISTS vector`는 pgvector를 이 데이터베이스에서 쓰게 켭니다.
확장이 이미 켜져 있으면 아무 일도 하지 않습니다.

교재 출력을 만든 데이터베이스의 확장 판은 위 줄에 보이는 번호입니다.
실습 폴더 안내대로 Docker 이미지를 쓰면 확장 판 번호가 0.8.2로 나옵니다.
판 번호가 달라도 이 절에서 쓰는 기능은 같습니다.

## 3. 문서를 벡터로 바꾸기

01절과 같은 모델과 같은 숫자 개수로 벡터를 만듭니다.
같은 벡터를 써야 01절 순위와 대조할 수 있습니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:08.225352Z', 'iopub.status.busy': '2026-09-21T07:40:08.225279Z', 'iopub.status.idle': '2026-09-21T07:40:08.586141Z', 'shell.execute_reply': '2026-09-21T07:40:08.585735Z'}}

```python
# 01절과 같은 임베딩 모델과 벡터의 숫자 개수를 씁니다(요청은 아직 보내지 않습니다)
embedding_model_name = "text-embedding-3-small"
embedding_model = OpenAIEmbeddings(model=embedding_model_name, dimensions=vector_dimensions)
print("임베딩 모델 이름:", embedding_model.model)
print("벡터의 숫자 개수 설정:", embedding_model.dimensions)
```

출력:
```
임베딩 모델 이름: text-embedding-3-small
벡터의 숫자 개수 설정: 256

```

### [20] markdown {}

**결과 읽기** — `임베딩 모델 이름: text-embedding-3-small`과 `벡터의 숫자 개수 설정: 256`이 보입니다.
이 셀은 객체만 만들므로 요청을 보내지 않습니다.
이 노트북의 출력은 2026-09-21에 이 모델로 실행한 결과입니다.

다음 셀은 문서 12개를 한 번에 임베딩합니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:08.586849Z', 'iopub.status.busy': '2026-09-21T07:40:08.586789Z', 'iopub.status.idle': '2026-09-21T07:40:08.882724Z', 'shell.execute_reply': '2026-09-21T07:40:08.882060Z'}}

```python
# 문서 12개의 제목과 본문을 이어 붙여 한 번에 임베딩합니다(임베딩 요청 1번)
doc_texts = []
doc_ids = []
for doc in docs:
    doc_texts.append(doc["title"] + " " + doc["text"])
    doc_ids.append(doc["doc_id"])
doc_vectors = embedding_model.embed_documents(doc_texts)
print("문서 벡터 수:", len(doc_vectors))
print("첫 문서 벡터의 숫자 개수:", len(doc_vectors[0]))
```

출력:
```
문서 벡터 수: 12
첫 문서 벡터의 숫자 개수: 256

```

### [22] markdown {}

**결과 읽기** — `문서 벡터 수: 12`와 `첫 문서 벡터의 숫자 개수: 256`이 보입니다.
문서 열두 개를 한 번에 보냈으므로 임베딩 요청은 한 번입니다.

## 4. 표에 넣기

벡터를 담을 칸의 자료형은 `vector(256)`입니다.
숫자 개수가 다른 벡터는 이 칸에 들어가지 않습니다.
문장 `DROP TABLE IF EXISTS`는 같은 이름의 표가 있으면 지우고 없으면 넘어갑니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:08.883853Z', 'iopub.status.busy': '2026-09-21T07:40:08.883784Z', 'iopub.status.idle': '2026-09-21T07:40:08.922160Z', 'shell.execute_reply': '2026-09-21T07:40:08.921715Z'}}

```python
# 벡터 칸이 있는 표를 새로 만듭니다(같은 이름의 옛 표는 먼저 지웁니다)
cur.execute("DROP TABLE IF EXISTS " + table_name)
create_sql = "CREATE TABLE " + table_name + " (doc_id text PRIMARY KEY, category text,"
create_sql = create_sql + " embedding vector(" + str(vector_dimensions) + "))"
cur.execute(create_sql)
print("표 만들기 SQL:")
print(create_sql)
```

출력:
```
표 만들기 SQL:
CREATE TABLE ch12_core_hnsw (doc_id text PRIMARY KEY, category text, embedding vector(256))

```

### [24] markdown {}

**결과 읽기** — 라벨 줄 아래에 `CREATE TABLE ch12_core_hnsw (doc_id text PRIMARY KEY, category text, embedding vector(256))`가 보입니다.
칸 `doc_id`는 기본 키라 같은 문서 ID를 두 번 넣을 수 없습니다.
Ch 4 03절에서 sqlite3로 만든 표와 문장 모양이 같습니다.

다음 셀은 문서 12개를 표에 넣습니다.
pgvector 확장은 벡터를 `[0.1,0.2]`처럼 대괄호로 묶은 글로 읽습니다.
그래서 `str(목록)`으로 바꾼 글을 값으로 넘깁니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:08.923037Z', 'iopub.status.busy': '2026-09-21T07:40:08.922958Z', 'iopub.status.idle': '2026-09-21T07:40:08.937238Z', 'shell.execute_reply': '2026-09-21T07:40:08.936790Z'}}

```python
# 문서 벡터를 글로 바꿔 표에 한 줄씩 넣고 들어간 행 수를 셉니다
insert_sql = "INSERT INTO " + table_name + " VALUES (%s, %s, %s)"
for i in range(len(docs)):
    vector_text = str(doc_vectors[i])
    cur.execute(insert_sql, (docs[i]["doc_id"], docs[i]["category"], vector_text))
cur.execute("SELECT count(*) FROM " + table_name)
print("표에 들어간 행 수:", cur.fetchone()[0])
```

출력:
```
표에 들어간 행 수: 12

```

### [26] markdown {}

**결과 읽기** — `표에 들어간 행 수: 12`가 보입니다.
SQL 함수 `count(*)`는 표의 행 수를 셉니다.
값을 넘기는 자리표시자가 Ch 4 03절 sqlite3의 `?`에서 `%s`로 바뀌었습니다.
자리표시자를 쓰는 까닭은 Ch 4 03절과 같습니다. 입력 글이 문장의 뜻을 바꾸지 못하게 막습니다.

## 5. 01절 거리 함수 이어 쓰기

01절에서 만든 함수 `cosine_distance()`를 준비 셀에서 가져왔습니다.
코사인 유사도를 가장 큰 값 1에서 뺀 값이고 작을수록 가깝습니다.
이 절에서 쓸 pgvector의 `<=>` 연산자가 내는 값도 같은 코사인 거리입니다.
6절에서 이 함수로 낸 값과 데이터베이스가 낸 값을 견줍니다.

## 6. 질문 벡터와 파이썬 계산값

질문 8개를 하나씩 임베딩합니다.
뒤에서 질문마다 순위를 낼 때 다시 쓰므로 목록에 모두 담아 둡니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:08.937987Z', 'iopub.status.busy': '2026-09-21T07:40:08.937910Z', 'iopub.status.idle': '2026-09-21T07:40:10.204024Z', 'shell.execute_reply': '2026-09-21T07:40:10.203055Z'}}

```python
# 질문 8개를 하나씩 임베딩해 질문 벡터 목록을 만듭니다(임베딩 요청 8번)
query_vectors = []
for query in queries:
    query_vectors.append(embedding_model.embed_query(query["question"]))
first_question_vector = query_vectors[0]
print("질문 벡터 수:", len(query_vectors))
print("첫 질문:", queries[0]["qid"], "|", queries[0]["question"])
print("첫 질문의 정답 문서 ID:", queries[0]["gold_doc_id"])
```

출력:
```
질문 벡터 수: 8
첫 질문: C01 | 책을 빌릴 수 있는 기간은 며칠인가요?
첫 질문의 정답 문서 ID: LIB-001

```

### [28] markdown {}

**결과 읽기** — `질문 벡터 수: 8`이 보입니다.
`첫 질문: C01 | 책을 빌릴 수 있는 기간은 며칠인가요?`이고 정답 문서 ID는 `LIB-001`입니다.
질문은 하나씩 보내므로 요청이 여덟 번입니다. 여기까지 요청은 모두 아홉 번입니다.

다음 셀은 첫 질문과 첫 문서 사이의 거리를 파이썬으로 먼저 계산합니다.
데이터베이스가 낸 값과 견줄 값입니다.

### [29] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.207227Z', 'iopub.status.busy': '2026-09-21T07:40:10.206990Z', 'iopub.status.idle': '2026-09-21T07:40:10.211688Z', 'shell.execute_reply': '2026-09-21T07:40:10.210991Z'}}

```python
# 01절 함수로 첫 질문과 첫 문서 사이의 코사인 거리를 미리 계산해 둡니다
first_doc_vector = doc_vectors[0]
python_distance = cosine_distance(first_question_vector, first_doc_vector)
print("첫 문서 ID:", doc_ids[0])
print("파이썬으로 낸 코사인 거리:", round(python_distance, 2))
```

출력:
```
첫 문서 ID: LIB-001
파이썬으로 낸 코사인 거리: 0.56

```

### [30] markdown {}

**결과 읽기** — `첫 문서 ID: LIB-001`이고 `파이썬으로 낸 코사인 거리: 0.56`입니다.
01절에서 같은 함수로 낸 값과 같습니다.
소수 셋째 자리 아래는 실행마다 조금 달라지므로 둘째 자리까지만 출력했습니다.

## 7. 거리 연산자로 검색하기

연산자 `<=>`는 두 벡터의 코사인 거리를 냅니다.
낱말 `ORDER BY`는 그 값이 작은 행부터 정렬합니다.
낱말 `LIMIT`은 앞에서 몇 줄만 받을지 정하고 이 절에서 처음 나옵니다.

### [31] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.213051Z', 'iopub.status.busy': '2026-09-21T07:40:10.212917Z', 'iopub.status.idle': '2026-09-21T07:40:10.215746Z', 'shell.execute_reply': '2026-09-21T07:40:10.215085Z'}}

```python
# 코사인 거리가 작은 문서부터 받아 오는 SQL 문장을 만듭니다
search_sql = "SELECT doc_id, embedding <=> %s FROM " + table_name
search_sql = search_sql + " ORDER BY embedding <=> %s LIMIT %s"
print("검색 SQL:")
print(search_sql)
```

출력:
```
검색 SQL:
SELECT doc_id, embedding <=> %s FROM ch12_core_hnsw ORDER BY embedding <=> %s LIMIT %s

```

### [32] markdown {}

**결과 읽기** — 라벨 줄 아래에 `SELECT doc_id, embedding <=> %s FROM ch12_core_hnsw ORDER BY embedding <=> %s LIMIT %s`가 보입니다.
자리표시자가 세 개입니다. 앞 두 개는 질문 벡터이고 마지막은 받아 올 줄 수입니다.
같은 질문 벡터를 두 자리에 넘겨 고른 값과 정렬 기준을 맞춥니다.

다음 셀은 이 SQL을 실행해 목록으로 돌려주는 함수입니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.217179Z', 'iopub.status.busy': '2026-09-21T07:40:10.217048Z', 'iopub.status.idle': '2026-09-21T07:40:10.220025Z', 'shell.execute_reply': '2026-09-21T07:40:10.219459Z'}}

```python
# 질문 벡터 하나로 표를 검색해 문서 ID와 코사인 거리 목록을 반환합니다
def run_search(question_vector, top_count):
    # 벡터를 글로 바꿔 %s 자리에 값으로 넘깁니다
    vector_text = str(question_vector)
    cur.execute(search_sql, (vector_text, vector_text, top_count))
    hit_list = []
    for row in cur.fetchall():
        hit_list.append({"doc_id": row[0], "거리": round(row[1], 2)})
    return hit_list
```

출력:
```

```

### [34] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
메서드 `cur.fetchall()`은 받은 줄을 튜플 목록으로 냅니다. 각 튜플의 앞 값이 문서 ID입니다.

다음 셀은 검색 결과를 표 모양으로 출력하는 함수입니다.

### [35] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.221350Z', 'iopub.status.busy': '2026-09-21T07:40:10.221256Z', 'iopub.status.idle': '2026-09-21T07:40:10.223509Z', 'shell.execute_reply': '2026-09-21T07:40:10.223114Z'}}

```python
# 검색 결과를 순위·문서 ID·코사인 거리 세 칸으로 출력합니다
def print_hits(hit_list):
    print("순위 | 문서 ID | 코사인 거리")
    for rank_number in range(len(hit_list)):
        row = hit_list[rank_number]
        print(rank_number + 1, "|", row["doc_id"], "|", row["거리"])
```

출력:
```

```

### [36] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.

## 8. 실행 계획 보기

데이터베이스는 같은 SQL을 여러 방법으로 읽을 수 있습니다.
문장 앞에 `EXPLAIN`을 붙이면 어떤 방법을 골랐는지 알려 줍니다.
계획은 여러 줄이라 표를 어떻게 읽는지 적힌 줄만 골라 봅니다.

### [37] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.224741Z', 'iopub.status.busy': '2026-09-21T07:40:10.224626Z', 'iopub.status.idle': '2026-09-21T07:40:10.227442Z', 'shell.execute_reply': '2026-09-21T07:40:10.226838Z'}}

```python
# 실행 계획에서 표를 어떻게 읽는지 적힌 줄만 골라 반환합니다
def find_scan_line(question_vector):
    vector_text = str(question_vector)
    cur.execute("EXPLAIN " + search_sql, (vector_text, vector_text, top_three))
    scan_line = ""
    for row in cur.fetchall():
        if "Scan" in row[0]:
            scan_line = row[0]
            break
    return scan_line.strip()
```

출력:
```

```

### [38] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 설정 `enable_seqscan`을 바꾸는 함수입니다.
이 설정을 off로 두면 계획기가 순차 스캔을 고르지 못합니다.

### [39] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.228613Z', 'iopub.status.busy': '2026-09-21T07:40:10.228509Z', 'iopub.status.idle': '2026-09-21T07:40:10.230959Z', 'shell.execute_reply': '2026-09-21T07:40:10.230372Z'}}

```python
# 계획기가 순차 스캔을 고를 수 있는지 여부를 바꾸고 바뀐 값을 반환합니다
def set_seqscan(setting_value):
    # SET 문장에는 자리표시자를 쓸 수 없어 같은 일을 하는 함수로 값을 넘깁니다
    cur.execute("SELECT set_config('enable_seqscan', %s, false)", (setting_value,))
    cur.execute("SHOW enable_seqscan")
    return cur.fetchone()[0]
```

출력:
```

```

### [40] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.

## 9. 실행 1 — 색인 없는 표

실행 전에 예상해 봅니다. 색인이 없으니 표의 행을 처음부터 끝까지 읽을 것입니다.
상위 3개는 01절 정확 검색과 같기를 바랍니다.

### [41] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.231977Z', 'iopub.status.busy': '2026-09-21T07:40:10.231872Z', 'iopub.status.idle': '2026-09-21T07:40:10.240481Z', 'shell.execute_reply': '2026-09-21T07:40:10.240051Z'}}

```python
# 실행 1: 색인이 없는 표에서 첫 질문을 검색하고 실행 계획도 봅니다
print("이 표의 색인:", "없음")
print("실행 계획의 읽기 방법 줄:")
print(find_scan_line(first_question_vector))
no_index_hits = run_search(first_question_vector, top_three)
print_hits(no_index_hits)
```

출력:
```
이 표의 색인: 없음
실행 계획의 읽기 방법 줄:
->  Seq Scan on ch12_core_hnsw  (cost=0.00..19.75 rows=650 width=48)
순위 | 문서 ID | 코사인 거리
1 | LIB-004 | 0.43
2 | LIB-001 | 0.56
3 | LIB-003 | 0.62

```

### [42] markdown {}

**결과 읽기** — `이 표의 색인: 없음`이고 계획 줄에 `Seq Scan on ch12_core_hnsw`가 적혀 있습니다.
줄 앞의 화살표 표시는 계획이 여러 층일 때 아래 층을 가리킵니다.
괄호 안의 비용 어림 값과 행 수 어림은 실행 환경에 따라 달라집니다.

라벨 줄 아래 세 줄은 `1 | LIB-004 | 0.43`, `2 | LIB-001 | 0.56`, `3 | LIB-003 | 0.62`입니다.
01절 정확 검색의 상위 3개와 문서 ID·순서·거리 값이 모두 같습니다.
둘째 줄의 `0.56`은 6절에서 파이썬으로 낸 값과도 같습니다.

## 10. 색인 만들기

이제 HNSW 색인을 만듭니다.
연산자 클래스 `vector_cosine_ops`는 색인이 코사인 거리로 정렬한다는 뜻입니다.
검색 SQL의 연산자와 색인의 연산자 클래스가 맞아야 색인을 쓸 수 있습니다.

### [43] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.241420Z', 'iopub.status.busy': '2026-09-21T07:40:10.241344Z', 'iopub.status.idle': '2026-09-21T07:40:10.248539Z', 'shell.execute_reply': '2026-09-21T07:40:10.248089Z'}}

```python
# 코사인 거리에 맞는 연산자 클래스로 HNSW 색인을 만듭니다
index_sql = "CREATE INDEX " + index_name + " ON " + table_name
index_sql = index_sql + " USING hnsw (embedding vector_cosine_ops)"
cur.execute(index_sql)
print("색인 만들기 SQL:")
print(index_sql)
```

출력:
```
색인 만들기 SQL:
CREATE INDEX ch12_core_hnsw_idx ON ch12_core_hnsw USING hnsw (embedding vector_cosine_ops)

```

### [44] markdown {}

**결과 읽기** — 라벨 줄 아래에 `CREATE INDEX ch12_core_hnsw_idx ON ch12_core_hnsw USING hnsw (embedding vector_cosine_ops)`가 보입니다.
문장을 실행하는 동안 pgvector가 벡터 12개를 이웃 그래프로 잇습니다.

## 11. 실행 2 — 색인 있는 표

실행 전에 예상해 봅니다. 색인을 만들었으니 계획이 색인 경로로 바뀔 것 같습니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.249327Z', 'iopub.status.busy': '2026-09-21T07:40:10.249256Z', 'iopub.status.idle': '2026-09-21T07:40:10.252398Z', 'shell.execute_reply': '2026-09-21T07:40:10.251968Z'}}

```python
# 실행 2: 색인이 있는 표에서 같은 SQL을 실행하고 계획을 다시 봅니다
print("이 표의 색인:", index_name)
print("실행 계획의 읽기 방법 줄:")
print(find_scan_line(first_question_vector))
with_index_hits = run_search(first_question_vector, top_three)
print_hits(with_index_hits)
```

출력:
```
이 표의 색인: ch12_core_hnsw_idx
실행 계획의 읽기 방법 줄:
->  Seq Scan on ch12_core_hnsw  (cost=0.00..2.18 rows=12 width=48)
순위 | 문서 ID | 코사인 거리
1 | LIB-004 | 0.43
2 | LIB-001 | 0.56
3 | LIB-003 | 0.62

```

### [46] markdown {}

**결과 읽기** — `이 표의 색인: ch12_core_hnsw_idx`인데 계획 줄에 여전히 `Seq Scan on ch12_core_hnsw`가 적혀 있습니다.
예상과 달랐습니다. 색인을 만들어도 계획기가 색인 경로를 고른다고 보장하지 않습니다.
상위 3개는 실행 1과 같은 `1 | LIB-004 | 0.43`, `2 | LIB-001 | 0.56`, `3 | LIB-003 | 0.62`입니다.

괄호 안 `rows` 값은 계획기가 어림한 행 수입니다.
색인을 만든 뒤에는 그 값이 12이고 실행 1에서는 650이었습니다.
이 표는 행이 12개뿐이라 계획기가 차례로 읽는 쪽의 비용을 더 작게 어림했습니다.

## 12. 값 바꿔 보기 — 색인 경로로 읽게 하기

바꿀 값은 설정 `enable_seqscan` 하나입니다. on에서 off로 바꿉니다.
실행 전에 예상해 봅니다. 계획이 색인 경로로 바뀌고 상위 3개는 그대로일 것입니다.

### [47] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.253126Z', 'iopub.status.busy': '2026-09-21T07:40:10.253059Z', 'iopub.status.idle': '2026-09-21T07:40:10.256231Z', 'shell.execute_reply': '2026-09-21T07:40:10.255823Z'}}

```python
# 실행 3: 설정 enable_seqscan만 off로 바꿔 색인 경로를 고르게 합니다
print("enable_seqscan 설정:", set_seqscan("off"))
print("실행 계획의 읽기 방법 줄:")
print(find_scan_line(first_question_vector))
index_path_hits = run_search(first_question_vector, top_three)
print_hits(index_path_hits)
```

출력:
```
enable_seqscan 설정: off
실행 계획의 읽기 방법 줄:
->  Index Scan using ch12_core_hnsw_idx on ch12_core_hnsw  (cost=12.09..20.27 rows=12 width=48)
순위 | 문서 ID | 코사인 거리
1 | LIB-004 | 0.43
2 | LIB-001 | 0.56
3 | LIB-003 | 0.62

```

### [48] markdown {}

**결과 읽기** — `enable_seqscan 설정: off`이고 계획 줄이 `Index Scan using ch12_core_hnsw_idx`로 바뀌었습니다.
이제 HNSW 색인의 이웃 그래프를 따라가 후보를 고릅니다.
상위 3개는 `1 | LIB-004 | 0.43`, `2 | LIB-001 | 0.56`, `3 | LIB-003 | 0.62`로 실행 1·2와 같습니다.
이번 실행에서는 색인 경로가 정확 검색과 같은 세 문서를 같은 순서로 냈습니다.

다음 셀은 색인 경로에서 `ef_search` 값만 바꿔 봅니다.
이 값은 색인을 따라갈 때 살펴볼 후보 목록의 크기이고 기본값은 40입니다.
결과에서 문서 ID만 뽑는 일은 준비 셀에서 가져온 함수 `unique_doc_ids()`가 맡습니다.

### [49] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.257000Z', 'iopub.status.busy': '2026-09-21T07:40:10.256921Z', 'iopub.status.idle': '2026-09-21T07:40:10.259828Z', 'shell.execute_reply': '2026-09-21T07:40:10.259420Z'}}

```python
# 색인 경로에서 ef_search만 4와 40으로 바꿔 상위 3개를 견줍니다
ef_values = [4, 40]
ef_rows = []
for ef_value in ef_values:
    cur.execute("SELECT set_config('hnsw.ef_search', %s, false)", (str(ef_value),))
    hit_list = run_search(first_question_vector, top_three)
    ef_rows.append({"ef_search": ef_value, "문서 ID": unique_doc_ids(hit_list)})
print("ef_search | 상위 3개 문서 ID")
for row in ef_rows:
    print(row["ef_search"], "|", row["문서 ID"])
```

출력:
```
ef_search | 상위 3개 문서 ID
4 | ['LIB-004', 'LIB-001', 'LIB-003']
40 | ['LIB-004', 'LIB-001', 'LIB-003']

```

### [50] markdown {}

**결과 읽기** — 라벨 줄 아래 두 줄에서 `ef_search`가 `4`일 때와 `40`일 때 상위 3개가 같습니다.
두 줄 모두 `['LIB-004', 'LIB-001', 'LIB-003']`입니다.
문서가 12개뿐이라 후보를 4개만 살펴도 같은 세 문서에 닿았습니다.

반복이 끝난 뒤 설정 값은 기본값과 같은 40입니다.
큰 자료에서 값을 줄이면 결과가 달라질 수 있습니다. 이번에 그 경우는 실행하지 않았습니다.

## 13. 차원 수와 색인 한도

이 챕터가 벡터의 숫자 개수를 256으로 둔 까닭을 확인합니다.
자료형 `vector`와 `halfvec`에 2001차원 칸을 만들고 색인을 만들어 봅니다.
자료형 `halfvec`은 숫자 하나를 절반 크기로 저장해 정밀도가 낮은 대신 한도가 넓습니다.

### [51] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.260592Z', 'iopub.status.busy': '2026-09-21T07:40:10.260519Z', 'iopub.status.idle': '2026-09-21T07:40:10.262685Z', 'shell.execute_reply': '2026-09-21T07:40:10.262273Z'}}

```python
# 자료형과 차원 수를 받아 HNSW 색인을 만들어 보고 결과 글을 반환합니다
def try_hnsw_index(type_name, dimension_count):
    # 표 이름과 자료형 이름은 값이 아니라 문장의 일부라 자리표시자로 넘길 수 없습니다
    dim_table = "ch12_dim_" + type_name
    cur.execute("DROP TABLE IF EXISTS " + dim_table)
    cur.execute("CREATE TABLE " + dim_table + " (embedding " + type_name + "(" + str(dimension_count) + "))")
    try:
        cur.execute("CREATE INDEX ON " + dim_table + " USING hnsw (embedding " + type_name + "_cosine_ops)")
        return "색인을 만들었습니다"
    except psycopg.Error as error:
        return error.diag.message_primary
```

출력:
```

```

### [52] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
문장 `try`로 오류를 받아 결과 글로 바꿉니다. 셀은 끝까지 실행됩니다.
속성 `error.diag.message_primary`는 데이터베이스가 보낸 오류 한 줄입니다.

다음 셀은 두 자료형에 같은 차원 수로 색인을 만들어 봅니다.

### [53] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.263423Z', 'iopub.status.busy': '2026-09-21T07:40:10.263353Z', 'iopub.status.idle': '2026-09-21T07:40:10.279228Z', 'shell.execute_reply': '2026-09-21T07:40:10.278820Z'}}

```python
# vector와 halfvec에 2001차원 칸을 만들어 색인 한도를 확인합니다
dimension_count = 2001
dimension_rows = []
for type_name in ["vector", "halfvec"]:
    outcome_text = try_hnsw_index(type_name, dimension_count)
    dimension_rows.append({"자료형": type_name, "결과": outcome_text})
print("자료형 | 차원 수 | 색인 결과")
for row in dimension_rows:
    print(row["자료형"], "|", dimension_count, "|", row["결과"])
```

출력:
```
자료형 | 차원 수 | 색인 결과
vector | 2001 | column cannot have more than 2000 dimensions for hnsw index
halfvec | 2001 | 색인을 만들었습니다

```

### [54] markdown {}

**결과 읽기** — 라벨 줄 아래 두 줄이 나옵니다.
자료형 `vector`는 `column cannot have more than 2000 dimensions for hnsw index`를 냈습니다.
자료형 `halfvec`은 `색인을 만들었습니다`입니다.

이 절이 쓰는 벡터의 숫자 개수 256은 2000이라는 한도 안에 있습니다.
차원 수를 더 늘리려면 자료형을 바꿔야 한다는 점을 여기서 확인했습니다.

## 14. 질문 여덟 개로 두 경로 견주기

질문 하나로는 두 경로가 같다고 말할 수 없습니다.
준비 셀에서 가져온 Ch 11 지표 함수 네 개로 질문 여덟 개를 두 경로에서 모두 잽니다.
정답 자리는 `find_gold_rank()`, 재현율은 `recall_at()`, 질문 평균은 `mean_score()`가 냅니다.

다음 셀은 질문 하나를 한 경로로 재어 기록 한 줄을 만드는 함수입니다.
받아 올 문서 수를 12로 두어 정답 문서의 자리를 끝까지 봅니다.

### [55] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.279900Z', 'iopub.status.busy': '2026-09-21T07:40:10.279838Z', 'iopub.status.idle': '2026-09-21T07:40:10.281863Z', 'shell.execute_reply': '2026-09-21T07:40:10.281494Z'}}

```python
# 질문 하나를 한 경로로 검색해 기록 한 줄을 만듭니다
def score_one(query_index, path_name):
    query = queries[query_index]
    gold_doc_ids = [query["gold_doc_id"]]
    hit_list = run_search(query_vectors[query_index], top_all)
    found_ids = unique_doc_ids(hit_list)
    row = {"경로": path_name, "질문": query["qid"]}
    row["정답 자리"] = find_gold_rank(found_ids, gold_doc_ids)
    for cutoff in cutoff_values:
        row["자리 " + str(cutoff)] = recall_at(found_ids, gold_doc_ids, cutoff)
    return row
```

출력:
```

```

### [56] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.

다음 셀은 질문 여덟 개를 두 경로로 모두 잽니다.
질문 벡터를 이미 만들어 두었으므로 임베딩 요청이 늘지 않습니다.

### [57] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.282489Z', 'iopub.status.busy': '2026-09-21T07:40:10.282436Z', 'iopub.status.idle': '2026-09-21T07:40:10.287411Z', 'shell.execute_reply': '2026-09-21T07:40:10.287119Z'}}

```python
# 질문 여덟 개를 두 경로로 모두 검색해 기록 줄을 담습니다(임베딩 요청은 더 보내지 않습니다)
score_rows = []
for path_name in ["순차 스캔", "색인"]:
    if path_name == "색인":
        set_seqscan("off")
    else:
        set_seqscan("on")
    for query_index in range(len(queries)):
        score_rows.append(score_one(query_index, path_name))
print("담은 기록 줄 수:", len(score_rows))
```

출력:
```
담은 기록 줄 수: 16

```

### [58] markdown {}

**결과 읽기** — `담은 기록 줄 수: 16`이 보입니다. 질문 여덟 개에 경로 두 가지를 곱한 수입니다.

다음 셀은 담은 줄을 표로 출력합니다.

### [59] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.288030Z', 'iopub.status.busy': '2026-09-21T07:40:10.287969Z', 'iopub.status.idle': '2026-09-21T07:40:10.290206Z', 'shell.execute_reply': '2026-09-21T07:40:10.289886Z'}}

```python
# 경로·질문·정답 자리·자리 1·자리 3 다섯 칸을 라벨 줄 아래에 차례로 출력합니다
print("경로 | 질문 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율")
for row in score_rows:
    print(row["경로"], "|", row["질문"], "|", row["정답 자리"], "|", row["자리 1"], "|", row["자리 3"])
```

출력:
```
경로 | 질문 | 정답 자리 | 자리 1 재현율 | 자리 3 재현율
순차 스캔 | C01 | 2 | 0.0 | 1.0
순차 스캔 | C02 | 7 | 0.0 | 0.0
순차 스캔 | C03 | 1 | 1.0 | 1.0
순차 스캔 | C04 | 1 | 1.0 | 1.0
순차 스캔 | C05 | 1 | 1.0 | 1.0
순차 스캔 | C06 | 1 | 1.0 | 1.0
순차 스캔 | C07 | 1 | 1.0 | 1.0
순차 스캔 | C08 | 1 | 1.0 | 1.0
색인 | C01 | 2 | 0.0 | 1.0
색인 | C02 | 7 | 0.0 | 0.0
색인 | C03 | 1 | 1.0 | 1.0
색인 | C04 | 1 | 1.0 | 1.0
색인 | C05 | 1 | 1.0 | 1.0
색인 | C06 | 1 | 1.0 | 1.0
색인 | C07 | 1 | 1.0 | 1.0
색인 | C08 | 1 | 1.0 | 1.0

```

### [60] markdown {}

**결과 읽기** — 라벨 줄 아래 열여섯 줄에서 정답 자리가 대부분 `1`입니다.
질문 `C01`은 두 경로 모두 정답 자리 `2`입니다.
질문 `C02`는 두 경로 모두 정답 자리 `7`이라 자리 3 재현율이 `0.0`입니다.
같은 질문 줄에서 순차 스캔과 색인의 네 칸이 모두 같습니다.
이 값들은 01절 표의 같은 질문 줄과도 같습니다.

다음 셀은 자르는 자리마다 질문 평균 재현율을 견줍니다.

### [61] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.290862Z', 'iopub.status.busy': '2026-09-21T07:40:10.290807Z', 'iopub.status.idle': '2026-09-21T07:40:10.293004Z', 'shell.execute_reply': '2026-09-21T07:40:10.292641Z'}}

```python
# 두 경로의 질문 평균 재현율을 자르는 자리마다 견줍니다
print("경로 | 자르는 자리 | 질문 평균 재현율")
for path_name in ["순차 스캔", "색인"]:
    picked = []
    for row in score_rows:
        if row["경로"] == path_name:
            picked.append(row)
    for cutoff in cutoff_values:
        scores = []
        for row in picked:
            scores.append(row["자리 " + str(cutoff)])
        print(path_name, "|", cutoff, "|", mean_score(scores))
```

출력:
```
경로 | 자르는 자리 | 질문 평균 재현율
순차 스캔 | 1 | 0.75
순차 스캔 | 2 | 0.875
순차 스캔 | 3 | 0.875
색인 | 1 | 0.75
색인 | 2 | 0.875
색인 | 3 | 0.875

```

### [62] markdown {}

**결과 읽기** — 라벨 줄 아래 여섯 줄이 나옵니다.
순차 스캔은 자리 1에서 `0.75`, 자리 2에서 `0.875`, 자리 3에서 `0.875`입니다.
색인 경로도 세 값이 같습니다.
01절 정확 검색의 질문 평균과도 같은 값입니다.

다음 셀은 실습에서 만든 표 가운데 차원 한도용 두 개를 지우고 연결을 닫습니다.
검색에 쓴 표 `ch12_core_hnsw`는 지우지 않고 그대로 남깁니다.

### [63] code {'execution': {'iopub.execute_input': '2026-09-21T07:40:10.293644Z', 'iopub.status.busy': '2026-09-21T07:40:10.293588Z', 'iopub.status.idle': '2026-09-21T07:40:10.300529Z', 'shell.execute_reply': '2026-09-21T07:40:10.300214Z'}}

```python
# 차원 한도를 보려고 만든 표 두 개를 지우고 연결을 닫습니다
cur.execute("DROP TABLE IF EXISTS ch12_dim_vector")
cur.execute("DROP TABLE IF EXISTS ch12_dim_halfvec")
set_seqscan("on")
conn.close()
print("연결 닫힘:", conn.closed)
```

출력:
```
연결 닫힘: True

```

### [64] markdown {}

**결과 읽기** — `연결 닫힘: True`가 보입니다.
연결을 닫으면 이 노트북에서 만든 커서도 함께 쓸 수 없게 됩니다.

## 정리

1. pgvector 표의 `vector(256)` 칸에 벡터를 넣고 `<=>` 연산자로 코사인 거리 순서를 받았습니다.
2. 색인을 만들어도 계획기가 색인 경로를 고른다고 보장하지 않습니다. 이 표에서는 `EXPLAIN`이 순차 스캔을 보여 주었습니다.
3. 이번 실행에서는 두 경로의 상위 3개와 질문 평균 재현율이 01절 정확 검색과 모두 같았습니다.

03절에서는 범주 칸이 있는 표를 새로 만들고 메타데이터 필터를 함께 걸어 검색합니다.
필터를 걸면 받아 온 줄 수가 받아 올 줄 수보다 적어질 수 있습니다.

## 그림

### 02-1-두-읽기-방법.mmd

```mermaid
flowchart TB
  %% classes
  question["질문 벡터 1개<br>숫자 256개"]:::tool
  subgraph seq["순차 스캔 경로"]
    direction TB
    seq_read["표의 행 12개를<br>차례로 읽기"]:::flow
    seq_sort["코사인 거리 12개를<br>작은 값부터 정렬"]:::flow
  end
  subgraph hnsw["색인 경로"]
    direction TB
    idx_walk["HNSW 색인의<br>이웃 그래프 따라가기"]:::flow
    idx_pick["살펴본 후보에서<br>가까운 것 고르기"]:::flow
  end
  question --> seq_read
  question --> idx_walk
  seq_read --> seq_sort
  idx_walk --> idx_pick
  seq_sort --> same["두 경로의 상위 세 개가 같았음<br>LIB-004 · LIB-001 · LIB-003"]:::measure
  idx_pick --> same
```

순차 스캔은 표의 행 12개를 차례로 읽고 색인 경로는 이웃 그래프를 따라가지만 이번 상위 세 개는 같았습니다.

### 02-2-표에-넣고-색인-만들기.mmd

```mermaid
flowchart TB
  %% classes
  docs["교육용 문서 12개<br>01절과 같은 자료"]:::tool
  vectors["문서 벡터 12개<br>숫자 256개씩"]:::tool
  table["표 ch12_core_hnsw<br>벡터 칸 vector(256)"]:::tool
  index["HNSW 색인<br>vector_cosine_ops"]:::tool
  plan["색인이 있어도 계획기가<br>순차 스캔을 고를 수 있음"]:::measure
  docs -->|임베딩 요청 1번| vectors
  vectors -->|INSERT 12줄| table
  table -->|CREATE INDEX| index
  index --> plan
```

문서 12개를 벡터로 바꿔 표의 벡터 칸에 넣고 그 칸에 HNSW 색인을 만듭니다.

### 02-3-세-실행의-계획.mmd

```mermaid
flowchart TB
  %% classes
  sql["같은 검색 SQL 한 문장<br>ORDER BY 거리 LIMIT 3"]:::flow
  run_one["실행 1<br>색인 없는 표"]:::flow
  run_two["실행 2<br>색인 있는 표"]:::flow
  run_three["실행 3<br>enable_seqscan을 off로"]:::flow
  plan_one["계획 줄 Seq Scan"]:::measure
  plan_two["계획 줄 Seq Scan"]:::measure
  plan_three["계획 줄 Index Scan"]:::measure
  same["세 실행의 상위 세 개가 같았음<br>LIB-004 · LIB-001 · LIB-003"]:::measure
  sql --> run_one --> plan_one --> same
  sql --> run_two --> plan_two --> same
  sql --> run_three --> plan_three --> same
```

색인을 만든 실행 2까지 계획 줄은 Seq Scan이고 설정을 off로 바꾼 실행 3에서 Index Scan으로 바뀝니다.

### 02-4-차원-수와-색인-한계.mmd

```mermaid
flowchart TB
  %% classes
  subgraph plain["자료형 vector"]
    direction TB
    v_col["칸 vector(2001)"]:::tool
    v_result["HNSW 색인을 만들지 못함<br>2000차원까지라는 알림"]:::measure
  end
  subgraph half["자료형 halfvec"]
    direction TB
    h_col["칸 halfvec(2001)"]:::tool
    h_result["HNSW 색인을<br>만들었습니다"]:::measure
  end
  v_col --> v_result
  h_col --> h_result
  v_result --> here["이 챕터가 쓰는 숫자 256개는 한도 안"]
  h_result --> here
```

vector 칸에는 2001차원 HNSW 색인을 만들지 못했고 halfvec 칸에는 만들었습니다.

### 02-5-서가와-끈.prompt.md

# 02-5-서가와-끈 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 한 칸은 책끼리 이어 둔 끈이 없어 책등을 끝에서부터 하나씩 살펴야 하고, 다른 칸은 끈을 따라 몇 권만 살펴보는데 두 칸에서 고른 책이 같습니다.

구성 요소와 배치(저장한 그림 기준): 나란히 놓인 나무 서가 두 칸에 같은 책이 같은 자리에 서 있습니다(= 같은 표의 행). 두 칸 모두 주황 책이 세 권이고 나머지는 옅은 회색 책입니다(= 이번 검색의 상위 세 개와 나머지). 왼쪽 칸에는 책을 잇는 것이 없습니다(= 색인 없는 표). 오른쪽 칸에는 책과 책 사이를 잇는 가는 끈이 있습니다(= HNSW 색인의 이웃 그래프). 두 서가 아래 작은 나무 쟁반에는 각각 주황 책 세 권이 눕혀 쌓여 있습니다(= 두 경로가 고른 같은 상위 세 개).

시선 순서: 왼쪽 서가의 책 → 오른쪽 서가의 끈 → 아래 두 쟁반의 같은 세 권.

검수 기준: 그림만 보고 「왼쪽 칸에는 책을 잇는 끈이 없고 오른쪽 칸에는 있다」와 「두 쟁반에 같은 주황 책 세 권이 있다」가 읽히는가.

Ch 9~Ch 12 비유 계열과의 관계: 책과 책등 = 문서와 문서 ID(Ch 11 01-6, Ch 12 01-5), 나무 쟁반 = 골라낸 후보 목록(Ch 11 02-5). 책 사이의 끈 = 색인의 이웃 그래프는 이 절에서 새로 정한 뜻입니다. 01절의 노란 쪽지(질문)와 실(거리)은 이 그림에 넣지 않았습니다. 이 절의 비교 대상이 질문과 문서 사이가 아니라 두 읽기 방법이기 때문입니다. 카드 상자(Ch 9 색인)·흰 카드(Ch 9 문서 청크)·봉투(Ch 10 출처 기록)·서랍(Ch 10 벡터 캐시)은 뜻이 정해져 있어 쓰지 않았습니다.

## 프롬프트 (2차, 채택)

```text
Simple flat educational illustration, white background, limited soft palette,
clean outlines, plain everyday objects, no text, no letters, no numbers, no logos.

Two identical wooden shelf compartments stand side by side. Each compartment holds
exactly twelve upright books of the same size: three books have orange spines and
nine books have pale grey spines, in the same order in both compartments. In the
left compartment every one of the twelve books is pulled forward by the same small
amount, so all twelve spines stick out in one even row, and nothing links them. In
the right compartment thin grey cords join each book to its neighbour, and only the
three orange books are pulled forward while the nine grey books stay pushed back.
Below each compartment a small wooden tray holds exactly three orange books lying
flat in a stack. No hands, no people, no screens, no arrows.
```

## 상태

- 2026-09-18 · `nano_banana_pro`(응답 모델 이름 `nano_banana_2`) · 16:9 · 2k · `use_unlim: false` · 장당 2크레딧 · 2회 생성 4크레딧 · 생성 뒤 잔액 2754.5.
- 1차 job `ea23bfff-515c-46c6-b18b-297df295a6ef` **탈락**: 두 서가에 손이 하나씩 있었지만 두 손 모양이 같아 「한쪽은 모두 살피고 다른 쪽은 몇 권만 살핀다」가 읽히지 않았습니다. 왼쪽 쟁반에는 책 세 권, 오른쪽 쟁반에는 두 권이 놓여 「두 경로가 같은 세 권을 골랐다」가 거꾸로 읽혔습니다. 원본 해시 `78274c93e67f0a2fb5b8027f7b59aeba60fd64f206cb2d624c2738d16b4bf550`.
- 2차 job `da509d1b-71a8-443d-b281-ed4ba2cb0999` **채택**: 손을 빼고 두 쟁반에 주황 책 세 권씩을 두어 「같은 세 권」이 읽힙니다. 오른쪽 칸에만 책과 책 사이를 잇는 끈이 있습니다. 원본 해시 `86553ee7cd1049246546a19cf2dbac93f39247839b93254506980a7c3524b172`.
- **프롬프트와 그림이 다른 점(그림 읽기에 반영)**: 프롬프트는 「열두 권」과 「왼쪽은 열두 권 모두, 오른쪽은 세 권만 앞으로 나온다」를 적었지만 그림은 책을 열세 권 그렸고 앞으로 나온 정도의 차이가 보이지 않습니다. 그래서 본문 비유·alt·캡션·「그림 읽기」에 책 수를 적지 않고, 읽히는 두 관계(끈의 있음과 없음, 두 쟁반의 같은 세 권)만 설명했습니다.
- 저장: 폭 1100px로 줄여 `figures/02-5-서가와-끈.png`(1100 × 614). 원본 2752px는 저장하지 않았습니다. 저장 PNG를 채택 job 결과에서 같은 폭으로 줄인 그림과 픽셀 단위로 대조해 차이가 없음을 확인했고(`ImageChops.difference` 범위 `None`), 1차 탈락본과는 다름을 확인했습니다(규격 §5-4).

