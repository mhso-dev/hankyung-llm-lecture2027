# 04-HWP와-HWPX

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 1h | 실습 2h | 코드 04-HWP와-HWPX.ipynb | 새 용어 4 -->

<h2 id="b1"><span class="no">1</span>학습 목표</h2>
<div class="goal"><ul>
<li>이 절을 마치면 견본 두 개의 앞 여덟 바이트와 압축 묶음 여부를 읽어 두 형식을 가를 수 있습니다.</li>
<li>이 절을 마치면 HWPX 압축 묶음에서 본문 XML을 골라 글이 든 요소의 글을 꺼낼 수 있습니다.</li>
<li>이 절을 마치면 쪽이 없는 형식의 출처 기록에 자리 칸 <code>section</code>을 더해 출처 표시를 만들 수 있습니다.</li>
</ul></div>

<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2>
<p>01~03절에서 읽은 형식은 PDF·DOCX·HTML·CSV였습니다. 국내 공공기관과 기업의 문서 저장소에는 한글 문서도 함께 있습니다. 확장자는 <code>.hwp</code>와 <code>.hwpx</code> 두 가지입니다.</p>
<p>두 확장자는 한 글자만 다릅니다. 그래서 같은 방법으로 읽을 수 있다고 보기 쉽습니다. 그런데 파일 안의 모양이 다릅니다.</p>
<p>형식 HWPX는 공개된 규격을 따르는 개방형 문서 형식입니다. 규격 이름은 OWPML이고 국가표준으로 등록되어 있습니다. 파일 하나 안에 XML을 압축 묶음으로 담습니다. 이 견본에는 항목이 두 개이고 본문 XML은 하나입니다.</p>
<p>형식 HWP는 그렇지 않습니다. 압축 묶음을 다루는 도구로 열면 오류가 납니다. 두 형식을 한 방법으로 읽으려고 하면 그 자리에서 멈춥니다.</p>
<p>이 절은 모든 한글 문서를 읽는 방법을 다루지 않습니다. 파일 앞부분을 보고 갈래를 정하고, 갈래마다 할 일을 나누는 것까지입니다. 읽는 파일은 견본 두 개입니다. 폴더 <code>labs/part3/ch10-document-processing/fixtures/</code>의 <code>legacy-signature.hwp</code>와 <code>minimal-marker.hwpx</code>입니다. 형식을 가르는 연습을 위해 만든 아주 작은 파일이고 실제 업무 문서가 아닙니다.</p>

<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2>
<ul>
<li><strong>네 칸 출처 기록</strong> — 03절에서 정했습니다. 쪽이 없는 형식은 <code>doc_id</code>·<code>source</code>·<code>file_type</code>·<code>parser</code> 네 칸만 적습니다.</li>
<li><strong>자리 칸</strong> — 03절에서 정한 말입니다. 본문이 파일의 어디에서 왔는지 적는 칸이고, CSV에서는 <code>row</code>였습니다.</li>
<li><strong>출처 표시</strong> — 03절 <code>make_unit_mark()</code>는 기록의 <code>row</code> 칸을 읽어 <code>[sample csv row.2]</code>를 만듭니다.</li>
<li><strong>태그 나무</strong> — 03절에서 HTML을 태그 나무로 읽고 태그 이름으로 글을 골랐습니다. 이 절의 XML도 같은 모양입니다.</li>
<li><strong>파일 열기와 오류 받기</strong> — Ch 2 05절에서 <code>with open(...)</code>과 <code>try/except 이름 as error</code>를 배웠습니다. 점을 이은 오류 이름은 Ch 4에서 배웠습니다.</li>
<li><strong>파서 이름</strong> — 01절에서 정한 <code>parser</code> 칸에 적는 이름입니다. 지금까지 <code>pypdf-plain</code>·<code>pdfplumber</code>·<code>python-docx</code>·<code>beautifulsoup</code>·<code>csv.DictReader</code> 다섯 개가 나왔습니다.</li>
</ul>
<p>노트북은 03절 <code>make_unit_record()</code>와 <code>make_unit_mark()</code>를 도구 파일 <code>rag_tools.py</code>에서 가져옵니다.</p>

<h2 id="b4"><span class="no">4</span>핵심 개념</h2>
<h3>비유 — 잠긴 상자와 지퍼 주머니</h3>
<p>책상 위에 비슷한 크기의 묶음 두 개가 놓여 있다고 생각해 보세요. 하나는 뚜껑이 닫힌 금속 상자이고, 하나는 지퍼가 달린 천 주머니입니다.</p>
<p>금속 상자는 앞면에 자물쇠 구멍이 있습니다. 열쇠가 없으면 안을 볼 수 없습니다. 주머니는 지퍼를 열면 안에 든 종이가 그대로 보입니다.</p>
<p>두 묶음 앞면에는 같은 모양의 둥근 딱지가 하나씩 붙어 있습니다. 무늬만 서로 다릅니다. 겉을 보고 어느 쪽이 어떤 묶음인지 가르는 표시입니다.</p>
{{img:04-5-잠긴-상자와-주머니|평면 그림으로 왼쪽에 뚜껑이 닫힌 회색 금속 상자가 있고 앞면에 자물쇠 구멍과 점무늬 둥근 딱지가 있으며 그림 안에 열쇠가 없고 오른쪽에 지퍼가 반쯤 열린 천 주머니가 있어 입구에서 흰 종이 두 장이 반쯤 빠져나와 있는데 한 장에는 얇은 가로줄 몇 개가 있고 다른 한 장은 거의 비어 있으며 주머니 앞면에는 줄무늬 둥근 딱지가 있고 주머니 아래에 흰 봉투 하나가 놓여 있으며 모서리에 빈 꼬리표가 끈으로 달려 있음|겉모양은 비슷하지만 왼쪽은 열 수 없고 오른쪽만 안의 종이가 보입니다}}
<p><strong>그림 읽기</strong> — 위쪽 두 묶음을 왼쪽에서 오른쪽으로 보고, 그다음 아래 봉투를 봅니다. 왼쪽 금속 상자는 뚜껑이 닫혀 있고 앞면에 자물쇠 구멍이 있으며 열쇠는 그림에 없습니다. 오른쪽 주머니는 지퍼가 반쯤 열려 종이 두 장이 빠져나와 있고, 한 장에만 얇은 가로줄이 있습니다. 두 묶음의 둥근 딱지는 모양이 같고 무늬가 다릅니다. 아래 봉투는 01절에서 정한 출처 기록이고, 모서리의 빈 꼬리표가 이 절에서 더하는 자리 칸입니다.</p>

<h3>이 절에서 쓰는 말</h3>
<table><thead><tr><th>용어</th><th>뜻과 일상 예</th><th>이 절에서 보이는 모습</th></tr></thead><tbody>
<tr><td>형식 표시(file signature)</td><td>파일 맨 앞 몇 바이트에 형식마다 정해진 값으로 적혀 있는 표시. 책 표지 뒤에 찍어 둔 도장과 같음. 03절에서 본 CSV 파일 앞의 인코딩 표시와는 다른 것</td><td>노트북 3절 <code>HWP 견본의 앞 여덟 바이트: d0cf11e0a1b11ae1</code></td></tr>
<tr><td>이진 파일(binary file)</td><td>글자로 바꾸지 않고 숫자 그대로 읽어야 하는 파일. 사진 파일과 같음</td><td>노트북 3절 <code>open(file_path, "rb")</code>으로 여덟 바이트를 읽는 함수</td></tr>
<tr><td>압축 묶음(ZIP)</td><td>파일 여러 개를 눌러 담아 한 파일로 만든 것. 서류 여러 장을 지퍼 주머니 하나에 넣는 것과 같음</td><td>노트북 5절 <code>압축 묶음 안의 항목 수: 2</code></td></tr>
<tr><td>이름 공간(namespace)</td><td>XML 태그 이름 앞에 붙여 어느 규격의 태그인지 알려 주는 주소. 같은 이름의 사람을 회사 이름과 함께 부르는 것과 같음</td><td>노트북 7절 <code>맨 위 요소의 태그 이름:</code> 줄의 중괄호 부분</td></tr>
</tbody></table>
<p>파서·파일 형식·출처 기록·출처 계보는 01절과 같은 뜻입니다. 글자 층·표 읽기는 02절과 같은 뜻입니다. 문단·꾸밈 이름·태그·자리 칸은 03절과 같은 뜻이고, 문서 청크·메타데이터·출처 표시는 Ch 9에서 정한 뜻 그대로입니다.</p>

<h3>도식 — 갈래를 먼저 정하고 갈래마다 할 일을 나눕니다</h3>
{{mermaid:04-1-두-형식-가르기|초록 상자 견본 두 개 legacy-signature.hwp와 minimal-marker.hwpx에서 파란 상자 앞 여덟 바이트와 압축 묶음 여부를 봄으로 내려온 뒤 노란 상자 두 개 HWP 후보 압축 묶음 아님과 HWPX 압축 묶음 맞음으로 갈라지고 왼쪽은 회색 상자 전용 도구가 필요함 이 절에서 본문을 읽지 않음에서 끝나며 오른쪽은 노란 상자 본문 XML 하나를 골라 글 15자를 꺼냄을 거쳐 초록 상자 다섯 칸 출처 기록 page 칸 없음 section 칸 1로 이어지는 흐름도|앞 여덟 바이트와 압축 묶음 여부로 갈래를 정하면 갈래마다 할 일이 달라집니다}}
<p><strong>도식 읽기</strong> — 위에서 아래로 봅니다. 맨 위 초록 상자가 이 절이 읽는 견본 두 개입니다. 그 아래 파란 상자가 파일 앞부분을 보는 단계입니다.</p>
<p>거기서 길이 두 갈래로 갈라집니다. 노란 상자 두 개가 노트북 3·4절 출력으로 정한 갈래입니다. 왼쪽 갈래는 회색 상자에서 끝납니다. 회색은 이 절에서 실행하지 않은 단계라는 뜻입니다.</p>
<p>오른쪽 갈래만 아래로 이어집니다. 노트북 5~8절에서 본문 XML 하나를 골라 글 15자를 꺼냈습니다. 맨 아래 초록 상자가 그 글에 붙이는 출처 기록입니다. 칸은 다섯 개인데 마지막 칸 이름이 <code>page</code>가 아니라 <code>section</code>입니다.</p>

<h3>두 형식을 어떻게 가르는가</h3>
<p>아래 표는 노트북 3·4절 출력을 견본별로 모은 것입니다. 둘째 열이 앞 여덟 바이트이고, 셋째 열이 압축 묶음 여부입니다.</p>
<table>
<tr><th>견본</th><th>앞 여덟 바이트</th><th>압축 묶음</th><th>이 절에서 한 일</th><th><code>parser</code> 칸 이름</th></tr>
<tr><td><code>legacy-signature.hwp</code></td><td><code>d0cf11e0a1b11ae1</code></td><td><code>False</code></td><td>「HWP 후보」로 갈라 두기</td><td>적지 않음</td></tr>
<tr><td><code>minimal-marker.hwpx</code></td><td><code>504b030414000000</code></td><td><code>True</code></td><td>본문 XML을 골라 글 15자 꺼내기</td><td><code>zip-xml</code></td></tr>
</table>
<p>앞 네 글자 <code>504b</code>는 압축 묶음 파일이 쓰는 값입니다. 그래서 확장자를 보지 않고도 압축 묶음인지 짐작할 수 있습니다.</p>
<p>표 첫 행의 값 <code>d0cf11e0a1b11ae1</code>은 여러 프로그램이 함께 쓰는 옛 문서 묶음 형식의 값입니다. 이 값 하나로 한글 문서라고 단정할 수 없습니다. 그래서 이 절은 그 갈래를 「HWP 후보」라고 부릅니다. 실습 폴더 모듈도 같은 뜻의 이름을 씁니다.</p>

<h2 id="b5"><span class="no">5</span>실행 예제</h2>
<p>내려받은 실습 폴더에서 노트북을 열고 위에서 아래로 실행합니다. API 키는 필요하지 않고 모델과 임베딩에는 요청을 한 번도 보내지 않습니다. 첫 셀의 패키지 설치만 인터넷을 씁니다. 압축 묶음과 XML을 읽는 도구는 Python에 들어 있어 따로 설치하지 않습니다.</p>
<p>이 페이지의 출력은 2026-09-21에 실행한 결과입니다. 모델을 부르지 않으므로 같은 판에서 다시 실행해도 같은 값이 나왔습니다. 새 커널로 두 번 실행해 스물두 개 코드 셀의 출력이 모두 같은 것을 확인했습니다.</p>
<p>강의 시간에는 노트북 2~8절을 설명합니다. 견본 찾기, 앞 여덟 바이트, 압축 묶음 여부, 항목 목록, 본문 XML 고르기, 글 꺼내기입니다. 9~10절 출처 기록과 값 바꿔 보기, 11~12절 Before·After는 함께 실행하고 실습 시간에 다시 읽습니다.</p>
{{mermaid:04-2-압축-묶음-속|초록 상자 minimal-marker.hwpx 압축 묶음 항목 2개에서 파란 상자 이름 조건 두 개로 고름 Contents/section 시작 .xml 끝으로 내려온 뒤 길이 둘로 갈라져 왼쪽은 회색 상자 Contents/content.hpf 고르지 않음에서 끝나고 오른쪽은 노란 상자 Contents/section0.xml 본문 XML 1개와 노란 상자 요소 이름 네 개 section p run t와 노란 상자 t 요소의 글 15자 한글 문서 처리 실습입니다로 차례로 이어지는 흐름도|항목 2개 가운데 본문 XML 1개만 고르고 맨 안쪽 t 요소에서 글 15자를 얻습니다}}
<p><strong>도식 읽기</strong> — 위에서 아래로 봅니다. 맨 위 초록 상자가 압축 묶음으로 연 견본입니다. 그 아래 파란 상자가 항목 이름으로 고르는 단계입니다.</p>
<p>거기서 길이 둘로 갈라집니다. 왼쪽 회색 상자는 고르지 않은 항목입니다. 이름이 <code>.xml</code>로 끝나지 않아 조건에 맞지 않았습니다. 오른쪽 노란 상자만 아래로 이어집니다.</p>
<p>노트북 7절 출력 <code>요소 이름: ['section', 'p', 'run', 't']</code>이 가운데 노란 상자입니다. 요소가 요소를 품은 모양입니다. 글은 맨 안쪽 <code>t</code>에만 들어 있어서 맨 아래 상자의 글 15자를 그 요소에서 얻었습니다.</p>
{{mermaid:04-3-자리-칸-표시|왼쪽 줄기에 초록 상자 03절 CSV 기록 row 칸 있음에서 파란 상자 make_unit_mark 함수 row 칸을 읽음을 거쳐 노란 상자 대괄호 sample csv row.2로 이어지고 오른쪽 줄기에 초록 상자 04절 HWPX 기록 section 칸 있음에서 파란 상자 make_unit_mark 함수 section 칸을 읽지 않음과 파란 상자 make_section_mark 함수 section 칸을 읽음 둘로 갈라져 각각 노란 상자 대괄호 minimal-marker hwpx 자리 칸이 표시에 없음과 노란 상자 대괄호 minimal-marker hwpx section.1로 이어지는 흐름도|같은 함수가 section 칸을 읽지 않아 자리 칸이 표시에 나오지 않습니다}}
<p><strong>도식 읽기</strong> — 줄기 두 개를 왼쪽에서 오른쪽으로 보고, 줄기마다 위에서 아래로 읽습니다. 왼쪽 줄기가 03절 CSV 기록이고 오른쪽 줄기가 이 절 HWPX 기록입니다.</p>
<p>오른쪽 줄기는 기록 하나에서 파란 상자 두 개로 나란히 갈라집니다. 왼쪽 함수는 03절 코드 그대로라 <code>row</code> 칸만 읽습니다. 그래서 노란 상자에 자리 칸이 없습니다.</p>
<p>오른쪽 함수는 <code>section</code> 칸을 읽습니다. 그래서 노란 상자가 <code>[minimal-marker hwpx section.1]</code>이 됩니다. 출처 표시의 모양은 함수가 읽는 칸이 정합니다.</p>
{{notebook:04-HWP와-HWPX|example}}

<h2 id="b6"><span class="no">6</span>일부러 실패해 보기</h2>
<p>이번에는 확장자만 보고 읽는 방법을 정해 봅니다. 이름이 한글 문서 확장자로 끝나니 압축 묶음이겠다고 보는 것입니다. Before 셀은 HWP 견본을 그대로 압축 묶음으로 엽니다.</p>
<p>After 셀은 3·4절에서 본 값 두 개로 갈래를 먼저 정합니다. 갈래마다 할 일을 나누면 HWP 견본에서 멈추지 않습니다.</p>
{{mermaid:04-4-확장자만-믿기|위 칸 Before에 초록 상자 legacy-signature.hwp와 파란 상자 압축 묶음으로 열기와 빨간 상자 BadZipFile 오류 항목 목록 빈 목록이 왼쪽에서 오른쪽으로 있고 아래 칸 After에 초록 상자 견본 두 개와 파란 상자 앞 여덟 바이트와 압축 묶음 여부로 가름과 노란 상자 HWP 후보는 전용 도구가 필요함 HWPX는 본문 15자가 같은 방향으로 있으며 맨 아래에 회색 상자 HWP 본문은 두 실행에서 모두 얻지 못함이 있는 비교 흐름도|Before는 오류에서 멈추고 After는 갈래를 먼저 정해 멈추지 않습니다}}
<p><strong>도식 읽기</strong> — 위 칸이 Before, 아래 칸이 After이고 칸마다 왼쪽에서 오른쪽으로 봅니다. 위 칸의 빨간 상자가 Before 결과입니다. 노트북 11절 출력 <code>받은 오류 이름: BadZipFile</code>과 <code>읽은 항목 이름 목록: []</code>이 그것입니다.</p>
<p>아래 칸의 노란 상자가 After 결과입니다. 갈래를 먼저 정해서 두 견본을 차례로 보고도 멈추지 않았습니다. 노트북 12절 출력 <code>갈래별 결과:</code> 줄에 칸 두 개가 있습니다.</p>
<p>맨 아래 회색 상자는 두 실행에 모두 해당합니다. Before도 After도 HWP에서 본문을 얻지 못했습니다. After 셀이 바꾼 것은 멈추지 않고 갈래를 적어 둔 것까지입니다.</p>
{{notebook:04-HWP와-HWPX|failure}}

<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2>
<ul>
<li><strong>확장자 이름만으로 읽는 방법을 정하지 않습니다.</strong> 이름은 사람이 바꿀 수 있고 형식 표시와 따로 있습니다. 노트북 11절에서 확장자만 믿고 열었더니 <code>BadZipFile</code> 오류에서 멈췄습니다. 앞 여덟 바이트와 압축 묶음 여부를 먼저 보고 갈래를 정합니다.</li>
<li><strong>형식 표시 하나로 형식을 단정하지 않습니다.</strong> 노트북 3절에서 본 <code>d0cf11e0a1b11ae1</code>은 여러 프로그램이 함께 쓰는 옛 문서 묶음 형식의 값입니다. 그래서 이 절은 갈래 이름을 「HWP 후보」로 두었습니다. 실습 폴더 모듈은 같은 갈래를 <code>ole-candidate</code>라고 적습니다.</li>
<li><strong>압축 묶음을 열었다는 것과 본문을 제대로 읽었다는 것은 다릅니다.</strong> 이 견본은 항목 두 개에 문단 하나가 든 아주 작은 파일입니다. 표·각주·그림이 든 문서에서 요소의 순서를 어떻게 다룰지는 이번에 실행하지 않았습니다. 본문 XML이 여러 개인 문서도 이번에 읽지 않았습니다.</li>
<li><strong>자리 칸 이름과 표시 함수를 짝지어 둡니다.</strong> 노트북 9절에서 03절 <code>make_unit_mark()</code>를 그대로 부르자 <code>[minimal-marker hwpx]</code>까지만 나왔습니다. 그 함수는 <code>row</code> 칸만 읽기 때문입니다. 이 절은 그 함수를 고치지 않고 <code>make_section_mark()</code>를 하나 더 만들었습니다.</li>
<li><strong>실습 폴더 모듈은 자리 칸 세 개를 한 함수에서 봅니다.</strong> <code>labs/part3/ch10-document-processing/document_processing.py</code>는 문서 청크 이름을 만들 때 <code>page</code>·<code>section</code>·<code>row</code>를 차례로 보고 먼저 있는 칸을 씁니다. 같은 파일의 <code>load_hwpx()</code>는 본문 XML을 이름의 번호 순서대로 읽고 <code>parser</code> 칸에 <code>zip-xml</code>을 적습니다. 글이 빈 XML에서는 <code>Document</code>를 만들지 않습니다. 이번 노트북에서는 그 모듈을 부르지 않았습니다.</li>
<li><strong>형식 HWP를 읽어야 하면 길이 세 가지입니다.</strong> 첫째는 믿을 수 있는 환경에서 HWPX나 PDF로 바꾼 뒤 그 산출물을 읽는 길입니다. 둘째는 공급자가 주는 도구를 쓰는 길이고, 셋째는 상용 파서에 보내는 길입니다. 어느 길이든 원본과 변환본을 잇는 기록을 남겨야 나중에 되짚을 수 있습니다. 세 길 모두 이 절에서 실행하지 않았습니다.</li>
<li><strong>외부 서비스에 보내도 되는 문서인지 먼저 확인합니다.</strong> 계약서·인사 문서처럼 사람 정보가 든 파일은 회사 승인을 받고 보냅니다. 서비스가 파일을 얼마나 오래 두는지도 함께 확인합니다.</li>
<li><strong>변환에 성공했다는 말은 내용이 그대로 남았다는 뜻이 아닙니다.</strong> 문단·표·병합 칸·각주·그림을 각각 확인하고 성공·부분 성공·실패로 갈라 적습니다. 대표 문서 몇 건은 사람이 원본과 견줍니다.</li>
</ul>

<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2>
<ul>
<li>확장자는 한 글자 차이인데 앞 여덟 바이트가 달랐습니다. 두 값은 <code>d0cf11e0a1b11ae1</code>과 <code>504b030414000000</code>입니다.</li>
<li>형식 HWPX는 압축 묶음이어서 항목 두 개가 보였고, 이름 조건 두 개로 본문 XML 하나를 골랐습니다.</li>
<li>태그 이름에는 이름 공간이 붙어 있습니다. 중괄호 뒤 이름으로 견주어야 글이 든 요소를 찾을 수 있었습니다.</li>
<li>글은 맨 안쪽 요소 <code>t</code>에 있었습니다. 고를 이름을 <code>p</code>로 바꾸자 본문이 0자였습니다.</li>
<li>쪽이 없는 형식이라 네 칸에 자리 칸 <code>section</code>을 더해 다섯 칸으로 적었습니다. 출처 표시는 <code>[minimal-marker hwpx section.1]</code> 모양입니다.</li>
<li>확장자만 보고 열면 <code>BadZipFile</code> 오류에서 멈췄습니다. 갈래를 먼저 정하면 멈추지 않았고, 그래도 HWP 본문은 얻지 못했습니다.</li>
</ul>
<p><strong>다음 학습과 이어지는 지점</strong> — 05절에서는 이렇게 읽은 글을 작은 문서 청크로 나눕니다. 같은 글을 세 가지 방식으로 나누고 나눈 자리와 길이를 견줍니다. 그때도 이 절에서 적은 출처 기록이 문서 청크마다 따라갑니다.</p>
<p>01~04절에서 형식 다섯 가지를 읽었습니다. 06~08절은 나눈 문서 청크를 임베딩해 색인하고 검색 결과를 견줍니다. 형식이 섞인 색인에서 결과를 볼 때 <code>page</code>·<code>section</code>·<code>row</code> 가운데 어느 칸이 있는지가 원본을 되짚는 길이 됩니다.</p>

<h2 id="b9"><span class="no">9</span>복습 문제</h2>
<details class="quiz" open><summary>문제 4개 · 해설 포함</summary>
<p class="quiz-q">1. [하] 확장자가 <code>.hwp</code>와 <code>.hwpx</code>로 한 글자만 다른데 읽는 방법을 나누는 까닭은 무엇입니까?</p>
<p class="quiz-a">파일 안의 모양이 다르기 때문입니다. 노트북 4절 출력 <code>HWP 견본이 압축 묶음인가: False</code>와 <code>HWPX 견본이 압축 묶음인가: True</code>가 그것입니다. 형식 HWPX만 압축 묶음이라 그 안의 XML을 꺼낼 수 있었습니다.</p>
<p class="quiz-q">2. [중] 태그 이름을 그대로 <code>"t"</code>와 견주면 글을 얻지 못하는 까닭은 무엇입니까?</p>
<p class="quiz-a">태그 이름 앞에 이름 공간이 붙어 있기 때문입니다. 노트북 7절 출력에서 맨 위 요소의 이름은 중괄호로 감싼 주소와 <code>section</code>이 이어진 글이었습니다. 중괄호 뒤 이름만 떼어 견주어야 글이 든 요소를 찾을 수 있습니다.</p>
<p class="quiz-q">3. [중] 03절 <code>make_unit_mark()</code>로 HWPX 기록의 출처 표시를 만들면 무엇이 빠집니까?</p>
<p class="quiz-a">자리 칸 <code>section</code>의 값이 빠집니다. 그 함수는 기록의 <code>row</code> 칸만 읽어서 <code>[minimal-marker hwpx]</code>까지만 만듭니다. 이 절은 <code>make_section_mark()</code>를 따로 만들어 <code>[minimal-marker hwpx section.1]</code>을 얻었습니다.</p>
<p class="quiz-q">4. [상] 앞 여덟 바이트가 <code>d0cf11e0a1b11ae1</code>인 파일을 「HWP」가 아니라 「HWP 후보」로 적어 두는 것이 나은 까닭은 무엇입니까?</p>
<p class="quiz-a">이 값을 여러 프로그램이 함께 쓰기 때문입니다. 값이 같다고 한글 문서라고 단정하면 다른 형식의 파일을 한글 문서로 세게 됩니다. 갈래를 후보로 적어 두면 뒤에서 전용 도구로 확인할 여지가 남습니다.</p>
</details>

<h2 id="b10"><span class="no">10</span>참고 자료</h2>
<ul>
<li><div><a href="https://www.hancom.co.kr/support/faqCenter/faq/detail/2784">한컴 지원센터 「HWPX 관련 자주하는 질문 및 답변안내」</a></div>확인 2026-09-18 · 형식 HWPX가 OWPML로 만들어졌고 국가표준으로 등록되어 있다는 설명 참고.</li>
<li><div><a href="https://docs.python.org/3/library/zipfile.html">Python 공식 문서 zipfile</a></div>확인 2026-09-18 · <code>is_zipfile()</code>·<code>ZipFile</code>·<code>namelist()</code>·<code>read()</code> 참고.</li>
<li><div><a href="https://docs.python.org/3/library/xml.etree.elementtree.html">Python 공식 문서 xml.etree.ElementTree</a></div>확인 2026-09-18 · <code>fromstring()</code>과 요소의 <code>tag</code>·<code>text</code>·<code>iter()</code> 참고.</li>
<li><div><a href="https://docs.python.org/3/library/functions.html#open">Python 공식 문서 open</a></div>확인 2026-09-18 · 모드 <code>"rb"</code>로 이진 파일을 읽는 방법 참고.</li>
<li><div><a href="https://reference.langchain.com/python/langchain-core/documents">LangChain 공식 API Document</a></div>확인 2026-09-18 · <code>page_content</code>와 <code>metadata</code> 구조 참고.</li>
<li>기준 버전은 Python 3.12.13과 langchain-core 1.6.2입니다. 압축 묶음과 XML을 읽는 도구는 Python에 들어 있는 것을 썼습니다. 판을 고정한 기준은 실습 폴더의 잠금 파일입니다.</li>
</ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# HWP와 HWPX

**이 노트북에서 할 일**

1. 견본 두 개의 앞부분을 읽어 HWP와 HWPX를 가릅니다.
2. HWPX 압축 묶음을 열어 본문 XML을 고르고 글을 꺼냅니다.
3. 쪽이 없는 형식의 출처 기록에 자리 칸을 더해 출처 표시를 만듭니다.

**준비물** — API 키가 필요 없습니다. 모델과 임베딩에는 요청을 한 번도 보내지 않습니다.
첫 셀의 패키지 설치만 인터넷을 씁니다.
그래서 예상 비용은 0달러입니다. 실행 시간은 패키지 설치를 빼면 10초 안팎입니다.

데이터는 견본 두 개입니다. 폴더 `labs/part3/ch10-document-processing/fixtures/`의
`legacy-signature.hwp`와 `minimal-marker.hwpx`입니다.
01절 2절에서 확장자만 세어 보았던 파일입니다.
두 견본은 형식을 가르는 연습을 위해 만든 아주 작은 파일이고 실제 업무 문서가 아닙니다.

**강의와 실습 범위** — 강의 시간에는 2~8절을 설명합니다.
견본 찾기, 앞 여덟 바이트, 압축 묶음 여부, 항목 목록, 본문 XML 고르기, 글 꺼내기입니다.
9~10절 출처 기록과 값 바꿔 보기, 11~12절 Before·After는 함께 실행하고 실습 시간에 다시 읽습니다.

**기준 버전** — 실습 폴더에 고정한 패키지 판을 씁니다. langchain-core 1.6.2입니다.
압축 묶음과 XML을 읽는 도구는 Python에 들어 있어 따로 설치하지 않습니다.
교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 버전과 Windows·macOS에서는 이번에 실행하지 않았습니다.

실습 폴더 `labs/part3/ch10-document-processing`에서 `uv sync --locked`를 실행합니다.
그다음 이 폴더의 `.venv` 커널을 고르고 첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![초록 상자 견본 두 개 legacy-signature.hwp와 minimal-marker.hwpx에서 파란 상자 앞 여덟 바이트와 압축 묶음 여부를 봄으로 내려온 뒤 노란 상자 두 개 HWP 후보 압축 묶음 아님과 HWPX 압축 묶음 맞음으로 갈라지고 왼쪽은 회색 상자 전용 도구가 필요함 이 절에서 본문을 읽지 않음에서 끝나며 오른쪽은 노란 상자 본문 XML 하나를 골라 글 15자를 꺼냄을 거쳐 초록 상자 다섯 칸 출처 기록 page 칸 없음 section 칸 1로 이어지는 흐름도](attachment:04-1-두-형식-가르기.png)

위에서 아래로 봅니다. 파란 상자에서 견본 두 개의 갈래가 갈립니다.
왼쪽 갈래는 이 절에서 본문을 읽지 않고 회색 상자에서 끝납니다.
오른쪽 갈래만 압축 묶음을 열어 글을 꺼내고, 맨 아래 초록 상자에서 출처 기록으로 모입니다.

### [2] markdown {}

## 1. 준비

첫 셀은 패키지를 설치하고 설치된 버전을 출력합니다. 설치에는 몇십 초가 걸릴 수 있습니다.
이 절에서 따로 설치할 것은 `Document`를 만드는 langchain-core 하나뿐입니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.298614Z', 'iopub.status.busy': '2026-09-21T06:25:35.298428Z', 'iopub.status.idle': '2026-09-21T06:25:35.751997Z', 'shell.execute_reply': '2026-09-21T06:25:35.751348Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓰는 패키지를 설치하고 버전을 확인합니다
%pip install -q "langchain-core==1.6.2"
from importlib.metadata import version

print("langchain-core:", version("langchain-core"))
```

출력:
```
Note: you may need to restart the kernel to use updated packages.
langchain-core: 1.6.2

```

### [4] markdown {}

**결과 읽기** — 출력 줄은 `langchain-core: 1.6.2` 한 줄입니다.
준비물에 적은 기준 버전과 같습니다.
압축 묶음과 XML을 읽는 도구는 Python에 들어 있어 설치 목록에 없습니다.

다음 셀은 이 절에서 쓸 이름을 불러옵니다.
이름 `zipfile`은 압축 묶음을 다루는 도구이고 `ElementTree`는 XML을 읽는 도구입니다.
두 도구의 뜻은 3~7절에서 처음 쓰는 자리에 적었습니다.

앞에서 배운 함수는 `rag_tools.py`에 모아 두었습니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일입니다.
이 노트북은 03절 `make_unit_record()`와 `make_unit_mark()`를 가져옵니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.753133Z', 'iopub.status.busy': '2026-09-21T06:25:35.753039Z', 'iopub.status.idle': '2026-09-21T06:25:35.923862Z', 'shell.execute_reply': '2026-09-21T06:25:35.923455Z'}, 'lesson_role': 'setup'}

```python
# 파일 앞부분 읽기·압축 묶음 열기·XML 읽기·문서 객체 만들기에 쓸 이름을 불러옵니다
import os
import zipfile
from xml.etree import ElementTree

from langchain_core.documents import Document
# 03절 함수 두 개를 도구 파일에서 가져옵니다
from rag_tools import make_unit_mark, make_unit_record
```

출력:
```

```

### [6] markdown {}

## 2. 견본 두 개 찾기

01~03절과 같은 방법으로 프로젝트 맨 위 경로를 고릅니다.
후보 세 개를 차례로 확인하고, 있는 경로에서 멈춥니다.
찾는 폴더는 03절과 같은 견본 폴더입니다.

실행 전에 예상합니다. 프로젝트 맨 위에서 열었다면 첫째 후보를 고를 것입니다.

### [7] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.924701Z', 'iopub.status.busy': '2026-09-21T06:25:35.924617Z', 'iopub.status.idle': '2026-09-21T06:25:35.926770Z', 'shell.execute_reply': '2026-09-21T06:25:35.926395Z'}}

```python
# 작업 폴더에서 본 프로젝트 맨 위 경로를 후보 세 개 가운데에서 고릅니다
candidates = [".", "../../..", "../../../.."]
root_path = None
for candidate in candidates:
    if os.path.exists(candidate + "/labs/part3/ch10-document-processing/fixtures"):
        root_path = candidate
        break
print("고른 경로:", root_path)
assert root_path is not None, "notebooks 폴더나 실습 폴더 맨 위에서 노트북을 열어 주세요."
```

출력:
```
고른 경로: .

```

### [8] markdown {}

**결과 읽기** — 출력 줄은 `고른 경로: .`입니다. `assert`도 통과했습니다.
교재 출력은 프로젝트 맨 위를 작업 폴더로 삼아 실행해서 첫째 후보를 골랐습니다.

다음 셀은 읽을 견본 두 개의 경로를 만듭니다.
확장자 `.hwp`와 `.hwpx`는 한 글자만 다릅니다.
그런데 파일 안의 모양은 아주 다릅니다. 3절부터 그것을 확인합니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.927488Z', 'iopub.status.busy': '2026-09-21T06:25:35.927423Z', 'iopub.status.idle': '2026-09-21T06:25:35.929399Z', 'shell.execute_reply': '2026-09-21T06:25:35.929049Z'}}

```python
# 읽을 견본 두 개의 경로를 만들고 파일이 있는지 확인합니다
fixtures_path = root_path + "/labs/part3/ch10-document-processing/fixtures"
hwp_path = fixtures_path + "/legacy-signature.hwp"
hwpx_path = fixtures_path + "/minimal-marker.hwpx"
print("HWP 견본이 있는가:", os.path.exists(hwp_path))
print("HWPX 견본이 있는가:", os.path.exists(hwpx_path))
```

출력:
```
HWP 견본이 있는가: True
HWPX 견본이 있는가: True

```

### [10] markdown {}

**결과 읽기** — 출력 두 줄이 모두 `True`입니다.
두 파일은 01절 2절에서 확장자 다섯 가지를 셀 때 이름만 보았던 파일입니다.
나머지 세 개는 03절에서 읽은 `sample.docx`·`sample.html`·`sample.csv`입니다.

### [11] markdown {}

## 3. 앞 여덟 바이트 읽기

파일에는 **형식 표시**가 있습니다. 맨 앞 몇 바이트에 형식마다 정해진 값이 적혀 있는 것입니다.
책 표지 뒤에 찍어 둔 도장과 같습니다. 도장을 보면 어느 출판사 책인지 알 수 있습니다.
이 값은 파일 이름과 따로 있어서 확장자를 바꿔도 그대로 남습니다.

이 값을 읽으려면 파일을 **이진 파일**로 열어야 합니다.
글자로 바꾸지 않고 숫자 그대로 읽는 방법입니다. 사진 파일을 열 때와 같습니다.
Ch 2 05절에서 배운 `open()`에 모드 `"rb"`를 주면 그렇게 열립니다.
메서드 `read(8)`은 앞에서 여덟 바이트만 읽고, `hex()`는 그 값을 열여섯 글자로 적습니다.

### [12] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.929963Z', 'iopub.status.busy': '2026-09-21T06:25:35.929901Z', 'iopub.status.idle': '2026-09-21T06:25:35.931384Z', 'shell.execute_reply': '2026-09-21T06:25:35.931063Z'}}

```python
# 파일을 이진 파일로 열어 앞 여덟 바이트를 읽고 열여섯 글자 값으로 만들어 반환합니다
def read_head_hex(file_path):
    with open(file_path, "rb") as binary_file:
        head_bytes = binary_file.read(8)
    return head_bytes.hex()
```

출력:
```

```

### [13] markdown {}

**결과 읽기** — 이 셀은 함수를 만들기만 하므로 출력이 없습니다.

모드 `"rb"`에서 `r`은 읽기이고 `b`는 이진 파일입니다.
03절에서 CSV를 열 때는 모드를 주지 않아 글자로 읽었습니다.

다음 셀은 견본 두 개의 앞 여덟 바이트를 읽어 견줍니다.

### [14] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.931962Z', 'iopub.status.busy': '2026-09-21T06:25:35.931906Z', 'iopub.status.idle': '2026-09-21T06:25:35.934245Z', 'shell.execute_reply': '2026-09-21T06:25:35.933842Z'}}

```python
# 견본 두 개의 앞 여덟 바이트를 읽어 값이 같은지 봅니다
hwp_head = read_head_hex(hwp_path)
hwpx_head = read_head_hex(hwpx_path)
print("HWP 견본의 앞 여덟 바이트:", hwp_head)
print("HWPX 견본의 앞 여덟 바이트:", hwpx_head)
print("두 값이 같은가:", hwp_head == hwpx_head)
```

출력:
```
HWP 견본의 앞 여덟 바이트: d0cf11e0a1b11ae1
HWPX 견본의 앞 여덟 바이트: 504b030414000000
두 값이 같은가: False

```

### [15] markdown {}

**결과 읽기** — 출력 첫 줄은 `HWP 견본의 앞 여덟 바이트: d0cf11e0a1b11ae1`입니다.
둘째 줄은 `HWPX 견본의 앞 여덟 바이트: 504b030414000000`입니다.
마지막 줄 `두 값이 같은가: False`를 보세요. 두 파일의 앞부분이 서로 다릅니다.

앞 네 글자 `504b`는 압축 묶음 파일이 쓰는 값입니다.
HWP 견본의 값은 여러 프로그램이 함께 쓰는 옛 문서 묶음 형식의 값입니다.
그래서 이 값만으로 HWP 파일이라고 단정할 수 없습니다.
이 노트북은 그 갈래를 「HWP 후보」라고 부릅니다.

### [16] markdown {}

## 4. 압축 묶음인지 보기

**압축 묶음**은 파일 여러 개를 눌러 담아 한 파일로 만든 것입니다.
서류 여러 장을 지퍼 주머니 하나에 넣어 들고 다니는 것과 같습니다.
겉은 파일 하나인데 안에는 파일 여러 개가 들어 있습니다.

압축 묶음을 다루는 도구 `zipfile`이 Python에 들어 있습니다.
함수 `zipfile.is_zipfile(경로)`는 그 파일이 압축 묶음인지 보고 `True`나 `False`를 냅니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.934809Z', 'iopub.status.busy': '2026-09-21T06:25:35.934769Z', 'iopub.status.idle': '2026-09-21T06:25:35.937173Z', 'shell.execute_reply': '2026-09-21T06:25:35.936800Z'}}

```python
# 견본 두 개가 압축 묶음인지 각각 확인합니다
hwp_is_zip = zipfile.is_zipfile(hwp_path)
hwpx_is_zip = zipfile.is_zipfile(hwpx_path)
print("HWP 견본이 압축 묶음인가:", hwp_is_zip)
print("HWPX 견본이 압축 묶음인가:", hwpx_is_zip)
```

출력:
```
HWP 견본이 압축 묶음인가: False
HWPX 견본이 압축 묶음인가: True

```

### [18] markdown {}

**결과 읽기** — 출력 첫 줄은 `HWP 견본이 압축 묶음인가: False`입니다.
다음 줄 `HWPX 견본이 압축 묶음인가: True`를 보세요.
확장자는 한 글자만 다른데 파일 안의 모양이 다릅니다.

형식 HWPX는 공개된 규격을 따르고 그 안에 XML을 압축 묶음으로 담습니다.
이 견본에는 항목이 두 개이고 본문 XML은 하나입니다.
형식 HWP는 그렇지 않아서 압축 묶음을 다루는 도구로 열 수 없습니다.
그래서 두 형식은 읽는 방법을 나누어야 합니다.

### [19] markdown {}

## 5. 압축 묶음 안의 항목 목록

클래스 `zipfile.ZipFile(경로)`는 압축 묶음을 엽니다.
메서드 `namelist()`는 그 안에 든 항목 이름을 목록으로 냅니다.

02절 `pdfplumber.open()`과 03절 `open()`처럼 `with`로 엽니다.
블록이 끝나면 파일이 닫힙니다. 라이브러리 객체에 `with`를 쓰는 세 번째 자리입니다.

### [20] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.937699Z', 'iopub.status.busy': '2026-09-21T06:25:35.937650Z', 'iopub.status.idle': '2026-09-21T06:25:35.940035Z', 'shell.execute_reply': '2026-09-21T06:25:35.939646Z'}}

```python
# HWPX 견본을 압축 묶음으로 열어 안에 든 항목 이름을 봅니다
with zipfile.ZipFile(hwpx_path) as archive:
    entry_names = archive.namelist()
print("압축 묶음 안의 항목 수:", len(entry_names))
print("항목 이름:", entry_names)
```

출력:
```
압축 묶음 안의 항목 수: 2
항목 이름: ['Contents/content.hpf', 'Contents/section0.xml']

```

### [21] markdown {}

**결과 읽기** — 출력 줄은 `압축 묶음 안의 항목 수: 2`입니다.
다음 줄 `항목 이름: ['Contents/content.hpf', 'Contents/section0.xml']`이 그 이름입니다.
이름에 `/`가 있어서 압축 묶음 안에도 폴더가 있다는 것을 알 수 있습니다.

항목 두 개는 하는 일이 다릅니다. 이름이 `section0.xml`인 항목이 본문입니다.
항목 `content.hpf`는 묶음에 무엇이 들어 있는지 적어 둔 것입니다.
실제 문서에서는 항목이 더 많을 수 있습니다. 이 견본에는 두 개뿐이고, 다른 문서는 이번에 열지 않았습니다.

### [22] markdown {}

## 6. 본문 XML 고르기

항목 이름으로 본문을 고릅니다. 조건은 두 개입니다.
이름이 `Contents/section`으로 시작하고 `.xml`로 끝나는 항목만 고릅니다.

메서드 `startswith()`는 글이 그 글자로 시작하는지 보고 `endswith()`는 끝나는지 봅니다.
조건 하나만 쓰면 본문이 아닌 항목이 함께 들어올 수 있습니다.
실습 폴더 모듈도 같은 조건 두 개를 함께 씁니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.940590Z', 'iopub.status.busy': '2026-09-21T06:25:35.940542Z', 'iopub.status.idle': '2026-09-21T06:25:35.942420Z', 'shell.execute_reply': '2026-09-21T06:25:35.942088Z'}}

```python
# 항목 이름이 두 조건을 모두 만족하는 것만 본문 XML 목록에 담습니다
section_names = []
for entry_name in entry_names:
    starts_with_section = entry_name.startswith("Contents/section")
    ends_with_xml = entry_name.endswith(".xml")
    if starts_with_section and ends_with_xml:
        section_names.append(entry_name)
print("본문 XML 수:", len(section_names))
print("본문 XML 이름:", section_names)
```

출력:
```
본문 XML 수: 1
본문 XML 이름: ['Contents/section0.xml']

```

### [24] markdown {}

**결과 읽기** — 출력 줄은 `본문 XML 수: 1`입니다.
다음 줄 `본문 XML 이름: ['Contents/section0.xml']`이 고른 이름입니다.
항목 `content.hpf`는 `.xml`로 끝나지 않아서 들어오지 않았습니다.

본문이 XML 여러 개에 나뉘어 있는 문서도 있습니다. 그때는 이름의 번호 순서대로 읽어야 합니다.
이 견본에는 본문 XML이 하나뿐이어서 순서를 맞출 일이 없었습니다.

### [25] markdown {}

## 7. XML 나무와 요소 이름

본문 XML은 태그로 감싼 글입니다. 03절 HTML과 같은 모양입니다.
다만 태그 이름을 문서 규격이 정해 두었습니다.

압축 묶음에서 항목 하나를 꺼내려면 메서드 `read(이름)`을 씁니다.
이 메서드는 글이 아니라 바이트를 냅니다.
함수 `ElementTree.fromstring(바이트)`에 그 값을 넣으면 요소 나무의 맨 위 요소를 얻습니다.
요소 나무는 태그가 태그를 품은 모양이고 03절에서 본 태그 나무와 같습니다.

### [26] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.943066Z', 'iopub.status.busy': '2026-09-21T06:25:35.943006Z', 'iopub.status.idle': '2026-09-21T06:25:35.945232Z', 'shell.execute_reply': '2026-09-21T06:25:35.944912Z'}}

```python
# 본문 XML 항목을 바이트로 꺼내 요소 나무의 맨 위 요소를 만듭니다
with zipfile.ZipFile(hwpx_path) as archive:
    xml_bytes = archive.read(section_names[0])
root = ElementTree.fromstring(xml_bytes)
print("꺼낸 바이트 수:", len(xml_bytes))
print("맨 위 요소의 태그 이름:", root.tag)
```

출력:
```
꺼낸 바이트 수: 204
맨 위 요소의 태그 이름: {http://www.hancom.co.kr/hwpml/2011/paragraph}section

```

### [27] markdown {}

**결과 읽기** — 출력 첫 줄은 `꺼낸 바이트 수: 204`입니다.
다음 줄 `맨 위 요소의 태그 이름: {http://www.hancom.co.kr/hwpml/2011/paragraph}section`을 보세요.
태그 이름 `section` 앞에 중괄호로 감싼 주소가 붙어 있습니다.

이 주소가 **이름 공간**입니다. 어느 규격의 태그인지 알려 주는 표시입니다.
같은 이름의 사람을 회사 이름과 함께 부르는 것과 같습니다.
이름 공간이 붙어 있으면 태그 이름을 그대로 견줄 수 없습니다. 11절에서 그 결과를 확인합니다.

### [28] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.945748Z', 'iopub.status.busy': '2026-09-21T06:25:35.945700Z', 'iopub.status.idle': '2026-09-21T06:25:35.947165Z', 'shell.execute_reply': '2026-09-21T06:25:35.946924Z'}}

```python
# 태그 이름에서 이름 공간을 떼고 뒤쪽 이름만 남겨 반환합니다
def make_local_name(tag_name):
    return tag_name.split("}")[-1]
```

출력:
```

```

### [29] markdown {}

**결과 읽기** — 이 셀은 함수를 만들기만 하므로 출력이 없습니다.

메서드 `split("}")`는 닫는 중괄호를 기준으로 글을 잘라 목록으로 만듭니다.
그 목록의 마지막 자리 `[-1]`가 이름 공간을 뗀 이름입니다.
이름 공간이 없는 태그는 잘리지 않아 이름이 그대로 남습니다.

다음 셀은 나무 안의 요소를 모두 돌며 이름을 모읍니다.
메서드 `iter()`는 맨 위 요소와 그 안의 요소를 차례로 냅니다.

### [30] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.947741Z', 'iopub.status.busy': '2026-09-21T06:25:35.947698Z', 'iopub.status.idle': '2026-09-21T06:25:35.949456Z', 'shell.execute_reply': '2026-09-21T06:25:35.949124Z'}}

```python
# 나무 안의 요소를 차례로 돌며 이름 공간을 뗀 이름을 모읍니다
local_names = []
for node in root.iter():
    local_names.append(make_local_name(node.tag))
print("요소 수:", len(local_names))
print("요소 이름:", local_names)
```

출력:
```
요소 수: 4
요소 이름: ['section', 'p', 'run', 't']

```

### [31] markdown {}

**결과 읽기** — 출력 줄은 `요소 수: 4`입니다.
다음 줄 `요소 이름: ['section', 'p', 'run', 't']`이 나무 안의 이름입니다.
요소 `section`이 맨 위이고 그 안에 `p`가 있습니다. 문단 하나를 뜻합니다.
요소 `p` 안에는 `run`이 있고 그 안에 `t`가 있습니다.

글은 맨 안쪽 `t`에 들어 있습니다. 문서 규격이 그렇게 정해 두었습니다.
03절 HTML에서 제목이 `h1`에 들어 있던 것과 같은 이야기입니다.

### [32] markdown {}

## 8. 글이 든 요소만 골라 이어 붙이기

이름이 `t`인 요소만 골라 글을 이어 붙입니다.
요소에 글이 없으면 `node.text`가 `None`입니다. 그때는 건너뜁니다.

고를 이름은 인자로 받습니다. 10절에서 그 값만 바꾸기 때문입니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.950062Z', 'iopub.status.busy': '2026-09-21T06:25:35.950016Z', 'iopub.status.idle': '2026-09-21T06:25:35.951467Z', 'shell.execute_reply': '2026-09-21T06:25:35.951216Z'}}

```python
# 나무에서 고른 이름의 요소만 찾아 글을 순서대로 이어 붙여 반환합니다
def read_body_text(xml_root, wanted_name):
    body_text = ""
    for node in xml_root.iter():
        local_name = make_local_name(node.tag)
        if local_name != wanted_name:
            continue
        if node.text is not None:
            body_text = body_text + node.text
    return body_text
```

출력:
```

```

### [34] markdown {}

**결과 읽기** — 이 셀은 함수를 만들기만 하므로 출력이 없습니다.

문장 `continue`는 그 아래를 건너뛰고 다음 요소로 넘어갑니다.
그래서 이름이 다른 요소의 글은 모으지 않습니다.
값 `None`은 글이 아예 없다는 뜻이고 빈 글과 다릅니다.

다음 셀은 이름 `t`를 넣어 본문을 얻습니다.

### [35] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.951939Z', 'iopub.status.busy': '2026-09-21T06:25:35.951885Z', 'iopub.status.idle': '2026-09-21T06:25:35.953423Z', 'shell.execute_reply': '2026-09-21T06:25:35.953109Z'}}

```python
# 이름이 t인 요소의 글만 모아 본문을 만듭니다
wanted_name = "t"
body_text = read_body_text(root, wanted_name)
print("고른 요소 이름:", wanted_name)
print("본문 글자 수:", len(body_text))
print("본문:")
print(body_text)
```

출력:
```
고른 요소 이름: t
본문 글자 수: 15
본문:
한글 문서 처리 실습입니다.

```

### [36] markdown {}

**결과 읽기** — 출력 줄은 `본문 글자 수: 15`입니다.
`본문:` 라벨 줄 아래 한 줄을 보세요. 꺼낸 글은 `한글 문서 처리 실습입니다.`입니다.
마침표까지 세어 열다섯 글자입니다.

이 글은 견본 하나에서 얻은 한 문단입니다.
표·각주·그림이 든 실제 문서에서도 같은 방법으로 본문을 얻는지는 실행하지 않았습니다.

### [37] markdown {}

## 9. 출처 기록에 자리 칸 더하기

형식 HWPX에도 쪽이 없습니다. 그래서 03절에서 정한 대로 네 칸만 적습니다.
칸은 `doc_id`·`source`·`file_type`·`parser`입니다.

다만 본문이 어느 XML에서 왔는지는 적을 수 있습니다.
03절 CSV의 `row`처럼 **자리 칸**을 하나 더합니다.
이 형식의 자리 칸 이름은 `section`이고 실습 폴더 모듈도 같은 이름을 씁니다.

네 칸 기록은 준비 셀에서 가져온 03절 `make_unit_record()`로 만듭니다. 칸 이름도 03절과 같습니다.
`parser` 칸에 적을 이름이 이 절에서 하나 늘어납니다.
압축 묶음을 열어 XML을 읽었으므로 `zip-xml`이라고 적습니다. 실습 폴더 모듈과 같은 글입니다.

다음 셀은 기록을 만들고 자리 칸을 하나 더합니다.

### [38] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.954029Z', 'iopub.status.busy': '2026-09-21T06:25:35.953973Z', 'iopub.status.idle': '2026-09-21T06:25:35.955961Z', 'shell.execute_reply': '2026-09-21T06:25:35.955516Z'}}

```python
# HWPX 기록을 만들고 자리 칸 section을 하나 더합니다
hwpx_record = make_unit_record(hwpx_path, "zip-xml")
hwpx_record["section"] = 1
print("HWPX 기록:", hwpx_record)
print("기록의 칸 수:", len(hwpx_record))
print("page 칸이 있는가:", "page" in hwpx_record)
print("section 칸의 값:", hwpx_record["section"])
```

출력:
```
HWPX 기록: {'doc_id': 'minimal-marker', 'source': 'minimal-marker.hwpx', 'file_type': 'hwpx', 'parser': 'zip-xml', 'section': 1}
기록의 칸 수: 5
page 칸이 있는가: False
section 칸의 값: 1

```

### [39] markdown {}

**결과 읽기** — 출력 첫 줄 `HWPX 기록:` 뒤에 `{'doc_id': 'minimal-marker', 'source': 'minimal-marker.hwpx', 'file_type': 'hwpx', 'parser': 'zip-xml', 'section': 1}`이 보입니다.
다음 줄은 `기록의 칸 수: 5`입니다.
셋째 줄 `page 칸이 있는가: False`를 보세요. 쪽 번호 칸은 넣지 않았습니다.

마지막 줄 `section 칸의 값: 1`은 첫 본문 XML에서 왔다는 뜻입니다.
번호를 1부터 센 까닭은 실습 폴더 모듈이 그렇게 세기 때문입니다.
03절 CSV의 `row` 칸은 2부터 셌습니다. 그 파일은 첫 줄이 칸 이름 줄이었기 때문입니다.

준비 셀에서 가져온 03절 `make_unit_mark()`는 기록의 `row` 칸만 봅니다.
그래서 `section` 칸이 있어도 그 값은 표시에 들어가지 않습니다.

자리 칸 이름이 형식마다 달라서 함수를 하나 더 만듭니다.
03절 함수는 고치지 않고 이름을 다르게 둡니다. 05절 이후에도 두 함수를 가려 쓰기 때문입니다.

### [40] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.956569Z', 'iopub.status.busy': '2026-09-21T06:25:35.956528Z', 'iopub.status.idle': '2026-09-21T06:25:35.958349Z', 'shell.execute_reply': '2026-09-21T06:25:35.957954Z'}}

```python
# 문서 청크 하나를 받아 파일 형식과 section 칸을 넣은 출처 표시를 만들어 반환합니다
def make_section_mark(chunk):
    doc_id = chunk.metadata["doc_id"]
    file_type = chunk.metadata["file_type"]
    section_mark = f"[{doc_id} {file_type}]"
    if "section" in chunk.metadata:
        section_number = chunk.metadata["section"]
        section_mark = f"[{doc_id} {file_type} section.{section_number}]"
    return section_mark
```

출력:
```

```

### [41] markdown {}

**결과 읽기** — 이 셀은 함수를 만들기만 하므로 출력이 없습니다.

함수 `make_unit_mark()`에서 읽는 칸 이름만 `row`에서 `section`으로 바꾼 코드입니다.
자리 칸이 없는 기록에는 파일 형식까지만 붙습니다.

다음 셀은 본문과 기록으로 `Document` 하나를 만들어 두 표시를 견줍니다.

### [42] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.958829Z', 'iopub.status.busy': '2026-09-21T06:25:35.958780Z', 'iopub.status.idle': '2026-09-21T06:25:35.961010Z', 'shell.execute_reply': '2026-09-21T06:25:35.960648Z'}}

```python
# 본문과 기록으로 Document를 만들고 두 함수가 만든 출처 표시를 견줍니다
hwpx_document = Document(page_content=body_text, metadata=hwpx_record)
unit_mark = make_unit_mark(hwpx_document)
section_mark = make_section_mark(hwpx_document)
print("본문 글자 수:", len(hwpx_document.page_content))
print("메타데이터 칸 수:", len(hwpx_document.metadata))
print("row 칸을 보는 표시:", unit_mark)
print("section 칸을 보는 표시:", section_mark)
```

출력:
```
본문 글자 수: 15
메타데이터 칸 수: 5
row 칸을 보는 표시: [minimal-marker hwpx]
section 칸을 보는 표시: [minimal-marker hwpx section.1]

```

### [43] markdown {}

**결과 읽기** — 출력 첫 두 줄은 `본문 글자 수: 15`와 `메타데이터 칸 수: 5`입니다.
셋째 줄 `row 칸을 보는 표시: [minimal-marker hwpx]`를 보세요.
기록에 `section` 칸이 있는데도 그 값이 표시에 없습니다.
마지막 줄은 `section 칸을 보는 표시: [minimal-marker hwpx section.1]`입니다.

출처 표시의 모양은 함수가 읽는 칸이 정합니다.
그래서 형식마다 자리 칸 이름을 정해 두고 표시를 만드는 함수와 짝을 맞춥니다.

### [44] markdown {}

## 10. 값 하나만 바꿔 보기

바꾸는 값은 고를 요소 이름 하나입니다. `"t"`에서 `"p"`로 바꿉니다.
함수는 고치지 않고 인자만 바꿉니다.

실행 전에 예상합니다. 요소 `p`는 문단을 감싸는 이름이라 글이 바로 들어 있지 않을 것입니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.961531Z', 'iopub.status.busy': '2026-09-21T06:25:35.961490Z', 'iopub.status.idle': '2026-09-21T06:25:35.963160Z', 'shell.execute_reply': '2026-09-21T06:25:35.962794Z'}}

```python
# 고를 요소 이름만 p로 바꿔 같은 함수를 다시 부릅니다
changed_name = "p"
changed_text = read_body_text(root, changed_name)
print("바꾼 요소 이름:", changed_name)
print("본문 글자 수:", len(changed_text))
print("빈 글인가:", changed_text == "")
```

출력:
```
바꾼 요소 이름: p
본문 글자 수: 0
빈 글인가: True

```

### [46] markdown {}

**결과 읽기** — 출력 줄은 `본문 글자 수: 0`입니다. 8절에서는 15자였습니다.
마지막 줄 `빈 글인가: True`를 보세요. 글을 하나도 얻지 못했습니다.

7절 출력 `요소 이름: ['section', 'p', 'run', 't']`을 다시 보세요.
요소 `p`는 나무에 있습니다. 그런데 글은 그 안쪽 `t`에 들어 있습니다.
고를 이름을 잘못 정하면 파일을 열고도 본문이 비어 있습니다.

### [47] markdown {'lesson_part': 'before'}

## 11. 일부러 실패해 보기

이번에는 확장자만 보고 읽는 방법을 정해 봅니다.
이름이 한글 문서 확장자로 끝나니 압축 묶음이겠다고 보는 것입니다.
Before 셀은 HWP 견본을 그대로 압축 묶음으로 엽니다.

오류가 나면 셀이 멈춥니다. 그래서 그 오류 이름만 받아 출력합니다.
Ch 2 05절에서 배운 모양이고 점을 이은 오류 이름은 Ch 4에서 배웠습니다.

### [48] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.963685Z', 'iopub.status.busy': '2026-09-21T06:25:35.963647Z', 'iopub.status.idle': '2026-09-21T06:25:35.965699Z', 'shell.execute_reply': '2026-09-21T06:25:35.965418Z'}, 'lesson_part': 'before'}

```python
# 확장자만 보고 HWP 견본을 압축 묶음으로 열어 봅니다
opened_names = []
error_name = ""
error_message = ""
try:
    with zipfile.ZipFile(hwp_path) as archive:
        opened_names = archive.namelist()
except zipfile.BadZipFile as error:
    error_name = type(error).__name__
    error_message = str(error)
print("읽은 항목 이름 목록:", opened_names)
print("받은 오류 이름:", error_name)
print("받은 오류 글:", error_message)
```

출력:
```
읽은 항목 이름 목록: []
받은 오류 이름: BadZipFile
받은 오류 글: File is not a zip file

```

### [49] markdown {'lesson_part': 'before'}

**결과 읽기** — 출력 첫 줄은 `읽은 항목 이름 목록: []`입니다. 항목을 하나도 얻지 못했습니다.
다음 줄 `받은 오류 이름: BadZipFile`이 받은 오류의 이름입니다.
마지막 줄은 `받은 오류 글: File is not a zip file`입니다.

오류가 알려 주는 것은 「압축 묶음이 아니다」까지입니다.
이 파일이 정말 한글 문서인지, 본문이 무엇인지는 알려 주지 않습니다.
확장자 이름만으로 읽는 방법을 정하면 이런 자리에서 멈춥니다.

### [50] markdown {'lesson_part': 'after'}

## 12. 고쳐서 다시 실행하기

3·4절에서 본 값 두 개로 갈래를 먼저 정합니다.
앞 여덟 바이트와 압축 묶음 여부입니다.
갈래마다 할 일을 나누면 HWP 견본에서 멈추지 않습니다.

### [51] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.966270Z', 'iopub.status.busy': '2026-09-21T06:25:35.966228Z', 'iopub.status.idle': '2026-09-21T06:25:35.967794Z', 'shell.execute_reply': '2026-09-21T06:25:35.967471Z'}, 'lesson_part': 'after'}

```python
# 앞 여덟 바이트와 압축 묶음 여부로 파일의 갈래를 정해 반환합니다
ole_marker = "d0cf11e0a1b11ae1"


def recognize_file_kind(file_path):
    head_hex = read_head_hex(file_path)
    if head_hex == ole_marker:
        return "hwp-후보"
    if zipfile.is_zipfile(file_path):
        return "hwpx"
    return "모름"
```

출력:
```

```

### [52] markdown {'lesson_part': 'after'}

**결과 읽기** — 이 셀은 이름 하나를 담고 함수를 만들기만 하므로 출력이 없습니다.

값 `d0cf11e0a1b11ae1`은 3절 출력에서 본 HWP 견본의 앞 여덟 바이트입니다.
이름에 담아 두고 식 안에 그대로 쓰지 않습니다.
함수는 이 이름을 함수 밖에서 읽습니다. Ch 5에서 배운 모양입니다.

갈래 이름 `hwp-후보`에 「후보」를 붙인 까닭이 있습니다.
이 값은 여러 프로그램이 함께 쓰는 옛 문서 묶음 형식의 값이기 때문입니다.

다음 셀은 HWPX 파일 하나를 열어 본문을 꺼내는 함수를 만듭니다.
5~8절에서 한 일을 함수 하나에 모은 것입니다.

### [53] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.968314Z', 'iopub.status.busy': '2026-09-21T06:25:35.968270Z', 'iopub.status.idle': '2026-09-21T06:25:35.969735Z', 'shell.execute_reply': '2026-09-21T06:25:35.969476Z'}, 'lesson_part': 'after'}

```python
# HWPX 파일 하나를 열어 본문 XML의 글을 꺼내 반환합니다
def read_hwpx_body(file_path):
    with zipfile.ZipFile(file_path) as archive:
        xml_bytes = archive.read(section_names[0])
    xml_root = ElementTree.fromstring(xml_bytes)
    return read_body_text(xml_root, wanted_name)
```

출력:
```

```

### [54] markdown {'lesson_part': 'after'}

**결과 읽기** — 이 셀도 함수를 만들기만 하므로 출력이 없습니다.

이 함수는 6절에서 이 견본에서 고른 이름을 그대로 씁니다.
다른 HWPX 파일이나 본문 XML이 여러 개인 문서를 읽으려면 이름을 고르는 부분까지 함수 안으로 옮겨야 합니다.

다음 셀은 견본 두 개를 차례로 보며 갈래마다 할 일을 나눕니다.

### [55] code {'execution': {'iopub.execute_input': '2026-09-21T06:25:35.970279Z', 'iopub.status.busy': '2026-09-21T06:25:35.970238Z', 'iopub.status.idle': '2026-09-21T06:25:35.973336Z', 'shell.execute_reply': '2026-09-21T06:25:35.973014Z'}, 'lesson_part': 'after'}

```python
# 갈래를 먼저 정하고 갈래마다 할 일을 나누어 결과를 적습니다
read_report = {}
for file_path in [hwp_path, hwpx_path]:
    file_kind = recognize_file_kind(file_path)
    if file_kind == "hwpx":
        read_report[file_kind] = read_hwpx_body(file_path)
    else:
        read_report[file_kind] = "전용 도구가 필요합니다"
print("갈래별 결과:", read_report)
assert read_report["hwpx"] == body_text
```

출력:
```
갈래별 결과: {'hwp-후보': '전용 도구가 필요합니다', 'hwpx': '한글 문서 처리 실습입니다.'}

```

### [56] markdown {'lesson_part': 'after'}

**결과 읽기** — 출력 줄 `갈래별 결과:` 뒤에 `{'hwp-후보': '전용 도구가 필요합니다', 'hwpx': '한글 문서 처리 실습입니다.'}`가 보입니다.
칸 두 개가 갈래 이름이고 값이 갈래마다 한 일입니다.
`assert`도 통과했습니다. 8절에서 얻은 본문과 같은 글입니다.

이번에는 멈추지 않았습니다. 그렇지만 HWP 본문을 읽은 것은 아닙니다.
두 실행 모두 HWP에서 얻은 본문은 없습니다.
After 셀이 바꾼 것은 멈추지 않고 갈래를 적어 둔 것까지입니다.
형식 HWP를 읽으려면 그 형식을 아는 전용 도구가 필요하고 이 절에서는 부르지 않았습니다.

### [57] markdown {'lesson_part': 'after'}

## 13. 정리

1. 확장자는 한 글자 차이인데 앞 여덟 바이트가 달랐습니다. 두 값은 `d0cf11e0a1b11ae1`과 `504b030414000000`입니다.
2. 형식 HWPX는 압축 묶음이어서 항목 두 개가 보였고 그 가운데 본문 XML 하나를 골랐습니다.
3. 글은 맨 안쪽 요소 `t`에 있었습니다. 고를 이름을 `p`로 바꾸자 본문이 0자였습니다.
4. 쪽이 없는 형식이라 네 칸에 자리 칸 `section`을 더해 다섯 칸으로 적었습니다.
5. 확장자만 보고 열면 `BadZipFile` 오류에서 멈췄습니다. 갈래를 먼저 정하면 멈추지 않았습니다.

다음 05절에서는 이렇게 읽은 글을 작은 문서 청크로 나눕니다.
같은 글을 세 가지 방식으로 나누고 나눈 자리와 길이를 견줍니다.
그때도 이 절에서 적은 출처 기록이 문서 청크마다 따라갑니다.

## 그림

### 04-1-두-형식-가르기.mmd

```mermaid
flowchart TB
  %% classes
  f1["견본 두 개<br>legacy-signature.hwp · minimal-marker.hwpx"]:::tool
  chk["앞 여덟 바이트와<br>압축 묶음 여부를 봄"]:::flow
  k1["HWP 후보<br>압축 묶음 아님"]:::measure
  k2["HWPX<br>압축 묶음 맞음"]:::measure
  no1["전용 도구가 필요함<br>이 절에서 본문을 읽지 않음"]
  x1["본문 XML 하나를 골라<br>글 15자를 꺼냄"]:::measure
  rec["다섯 칸 출처 기록<br>page 칸 없음 · section 칸 1"]:::tool
  f1 --> chk
  chk --> k1
  chk --> k2
  k1 --> no1
  k2 --> x1
  x1 --> rec
```

- 설명 대상 문장: 이름은 비슷하지만 파일 안의 모양이 달라서 읽는 방법을 나누어야 합니다.
- 캡션: 앞 여덟 바이트와 압축 묶음 여부로 갈래를 정하면 갈래마다 할 일이 달라집니다
- 읽는 법: 위에서 아래로 봅니다. 파란 상자에서 갈래가 갈리고, 왼쪽 갈래는 회색 상자에서 끝나며 오른쪽 갈래만 글을 꺼내 초록 상자 출처 기록으로 모입니다.
- alt: 초록 상자 견본 두 개 legacy-signature.hwp와 minimal-marker.hwpx에서 파란 상자 앞 여덟 바이트와 압축 묶음 여부를 봄으로 내려온 뒤 노란 상자 두 개 HWP 후보 압축 묶음 아님과 HWPX 압축 묶음 맞음으로 갈라지고 왼쪽은 회색 상자 전용 도구가 필요함 이 절에서 본문을 읽지 않음에서 끝나며 오른쪽은 노란 상자 본문 XML 하나를 골라 글 15자를 꺼냄을 거쳐 초록 상자 다섯 칸 출처 기록 page 칸 없음 section 칸 1로 이어지는 흐름도

### 04-2-압축-묶음-속.mmd

```mermaid
flowchart TB
  %% classes
  z1["minimal-marker.hwpx<br>압축 묶음 · 항목 2개"]:::tool
  pick["이름 조건 두 개로 고름<br>Contents/section 시작<br>.xml 끝"]:::flow
  e1["Contents/content.hpf<br>고르지 않음"]
  e2["Contents/section0.xml<br>본문 XML 1개"]:::measure
  tree["요소 이름 네 개<br>section · p · run · t"]:::measure
  body["t 요소의 글 15자<br>한글 문서 처리 실습입니다."]:::measure
  z1 --> pick
  pick --> e1
  pick --> e2
  e2 --> tree
  tree --> body
```

- 설명 대상 문장: 압축 묶음을 열어 본문 XML을 고르고 글이 든 요소만 골라 글을 꺼냅니다.
- 캡션: 항목 2개 가운데 본문 XML 1개만 고르고 맨 안쪽 t 요소에서 글 15자를 얻습니다
- 읽는 법: 위에서 아래로 봅니다. 파란 상자에서 길이 둘로 갈라지고, 왼쪽 회색 상자는 고르지 않은 항목이며 오른쪽 노란 상자만 아래로 이어집니다.
- alt: 초록 상자 minimal-marker.hwpx 압축 묶음 항목 2개에서 파란 상자 이름 조건 두 개로 고름 Contents/section 시작 .xml 끝으로 내려온 뒤 길이 둘로 갈라져 왼쪽은 회색 상자 Contents/content.hpf 고르지 않음에서 끝나고 오른쪽은 노란 상자 Contents/section0.xml 본문 XML 1개와 노란 상자 요소 이름 네 개 section p run t와 노란 상자 t 요소의 글 15자 한글 문서 처리 실습입니다로 차례로 이어지는 흐름도

### 04-3-자리-칸-표시.mmd

```mermaid
flowchart TB
  %% classes
  c1["03절 CSV 기록<br>row 칸 있음"]:::tool
  c2["make_unit_mark()<br>row 칸을 읽음"]:::flow
  c3["[sample csv row.2]"]:::measure
  h1["04절 HWPX 기록<br>section 칸 있음"]:::tool
  h2["make_unit_mark()<br>section 칸을 읽지 않음"]:::flow
  h3["[minimal-marker hwpx]<br>자리 칸이 표시에 없음"]:::measure
  h4["make_section_mark()<br>section 칸을 읽음"]:::flow
  h5["[minimal-marker hwpx section.1]"]:::measure
  c1 --> c2
  c2 --> c3
  h1 --> h2
  h2 --> h3
  h1 --> h4
  h4 --> h5
```

- 설명 대상 문장: 출처 표시의 모양은 함수가 읽는 칸이 정합니다.
- 캡션: 같은 함수가 section 칸을 읽지 않아 자리 칸이 표시에 나오지 않습니다
- 읽는 법: 줄기 두 개를 왼쪽에서 오른쪽으로 보고, 줄기마다 위에서 아래로 읽습니다. 오른쪽 줄기의 기록 하나에서 함수 두 개로 갈라져 표시가 둘 나옵니다.
- alt: 왼쪽 줄기에 초록 상자 03절 CSV 기록 row 칸 있음에서 파란 상자 make_unit_mark 함수 row 칸을 읽음을 거쳐 노란 상자 대괄호 sample csv row.2로 이어지고 오른쪽 줄기에 초록 상자 04절 HWPX 기록 section 칸 있음에서 파란 상자 make_unit_mark 함수 section 칸을 읽지 않음과 파란 상자 make_section_mark 함수 section 칸을 읽음 둘로 갈라져 각각 노란 상자 대괄호 minimal-marker hwpx 자리 칸이 표시에 없음과 노란 상자 대괄호 minimal-marker hwpx section.1로 이어지는 흐름도

### 04-4-확장자만-믿기.mmd

```mermaid
flowchart TB
  %% classes
  subgraph BEFORE["Before · 확장자만 보고 압축 묶음으로 열기"]
    direction LR
    b1["legacy-signature.hwp"]:::tool
    b2["압축 묶음으로 열기"]:::flow
    b3["BadZipFile 오류<br>항목 목록 빈 목록"]:::fail
    b1 --> b2
    b2 --> b3
  end
  subgraph AFTER["After · 갈래를 먼저 정하기"]
    direction LR
    a1["견본 두 개"]:::tool
    a2["앞 여덟 바이트와<br>압축 묶음 여부로 가름"]:::flow
    a3["HWP 후보는 전용 도구가 필요함<br>HWPX는 본문 15자"]:::measure
    a1 --> a2
    a2 --> a3
  end
  note1["HWP 본문은 두 실행에서 모두 얻지 못함"]
  BEFORE ~~~ AFTER
  AFTER ~~~ note1
```

- 설명 대상 문장: 확장자 이름만으로 읽는 방법을 정하면 오류에서 멈춥니다.
- 캡션: Before는 오류에서 멈추고 After는 갈래를 먼저 정해 멈추지 않습니다
- 읽는 법: 위 칸이 Before, 아래 칸이 After이고 칸마다 왼쪽에서 오른쪽으로 봅니다. 맨 아래 회색 상자는 두 실행에 모두 해당하는 값입니다.
- alt: 위 칸 Before에 초록 상자 legacy-signature.hwp와 파란 상자 압축 묶음으로 열기와 빨간 상자 BadZipFile 오류 항목 목록 빈 목록이 왼쪽에서 오른쪽으로 있고 아래 칸 After에 초록 상자 견본 두 개와 파란 상자 앞 여덟 바이트와 압축 묶음 여부로 가름과 노란 상자 HWP 후보는 전용 도구가 필요함 HWPX는 본문 15자가 같은 방향으로 있으며 맨 아래에 회색 상자 HWP 본문은 두 실행에서 모두 얻지 못함이 있는 비교 흐름도

### 04-5-잠긴-상자와-주머니.prompt.md

# 04-5 잠긴 상자와 주머니 (Higgsfield 삽화)

- 상태: 2026-09-18 채택. 모델 `nano_banana_pro`(응답 모델 이름 `nano_banana_2`), 16:9, 2k, 2크레딧. 1차 job `ed86ddc5-f230-47ae-a72d-f5e4bbc969ac` 채택(재생성 없음, 탈락 0). 생성 뒤 잔액 2802.
- 저장: 원본 2752×1536을 폭 1100px로 줄여 `figures/04-5-잠긴-상자와-주머니.png`로 두었습니다(원본은 저장하지 않음). 저장 PNG를 채택 job 결과와 같은 폭으로 줄여 픽셀 대조했고 차이가 없었습니다(규격 §5-4).
- 설명 대상 문장: 겉모양이 비슷한 두 묶음인데 하나는 열 수 없고 하나는 안의 종이가 보입니다.
- 구성 요소와 배치: 왼쪽에 닫힌 회색 금속 상자(앞면에 자물쇠 구멍, 그림 안에 열쇠 없음), 오른쪽에 지퍼가 반쯤 열린 천 주머니(입구에서 흰 종이 두 장이 반쯤 빠져나와 있고 한 장에는 얇은 가로줄 몇 개, 다른 한 장은 거의 빈 종이). 두 묶음 앞면에 같은 모양의 둥근 딱지가 하나씩 있고 무늬만 다릅니다(왼쪽 점무늬, 오른쪽 줄무늬). 주머니 아래에 흰 봉투 하나가 놓여 있고 모서리에 빈 꼬리표가 끈으로 달려 있습니다.
- 시선 순서: 왼쪽 상자 → 오른쪽 주머니와 빠져나온 종이 두 장 → 두 묶음의 딱지 무늬 → 아래 봉투와 꼬리표.
- 검수(그림만 보고 관계가 읽히는가): 왼쪽은 열 수 없고 오른쪽은 열려 안의 종이가 보입니다. 종이 두 장 가운데 한 장만 줄이 있어 본문과 목록의 차이가 보입니다. 딱지 무늬가 달라 겉에 붙은 표시로 갈래를 가른다는 것이 읽힙니다. 봉투와 꼬리표는 열린 쪽에서만 나옵니다. 글자·숫자·화면 요소는 없습니다.
- 비유 계열: 01절 봉투(출처 기록)를 이어 쓰고, 꼬리표가 03·04절 자리 칸입니다.

## 프롬프트

```text
Simple flat educational illustration, white background, limited soft palette,
clean outlines, plain everyday objects, no text, no letters, no numbers, no logos.
Two containers of the same size stand side by side on a plain surface.
On the left, a closed grey metal box with a small keyhole on its front and a lid
that is clearly shut tight; no key anywhere in the picture.
On the right, a soft cloth pouch with its zipper pulled halfway open, and two small
white sheets of paper clearly sticking halfway out of the pouch opening, one sheet
carrying a few thin horizontal lines and the other sheet almost blank.
Each container wears one small round sticker of the same shape on its front, but the
two stickers carry clearly different simple patterns: dots on the left sticker,
stripes on the right sticker.
Below the right pouch lies one plain white envelope, flat, with a small blank paper
tag tied to its corner by a short string.
No monitors, no screens, no keyboards, no people, no text of any kind.
```

