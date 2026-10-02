# 08-OpenAPI와-TS-SDK

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 0.75h | 실습 2h | 코드 notebooks/08-OpenAPI와-TS-SDK.ipynb | 새 용어 2 -->
<style>html,body{overflow-x:hidden}.notebook,.nb-cell,.nb-main,.nb-input,.nb-result{min-width:0;max-width:100%}.nb-input pre,.nb-output{box-sizing:border-box;max-width:100%;overflow-x:auto}code.nb-source{display:block!important;width:100%!important;min-width:0!important;overflow-x:auto!important;padding:0!important}</style>
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>
<li>앱 객체의 메서드 <code>openapi</code>가 만든 응답 문서에서, 요청 주소와 입력 형식·응답 형식이 적힌 칸을 찾을 수 있습니다.</li>
<li>생성 SDK에서 요청 주소마다 만든 함수를 읽고, SSE 쪽 함수의 한계를 설명할 수 있습니다.</li>
<li>의존성 하나만 바꾼 실험으로, 응답 문서에 보안 방식 칸이 생기는 조건을 출력으로 확인할 수 있습니다.</li>
</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>웹 화면을 만드는 사람은 파이썬 앱 파일을 읽지 않고도 이 앱을 불러야 합니다. 어떤 요청 주소가 있고, 요청 본문에 어떤 칸을 채우며, 어떤 응답이 오는지 알아야 합니다. 이것을 사람이 손으로 옮겨 적으면, 앱을 고칠 때마다 두 글이 어긋나기 쉽습니다. 그래서 앱 객체가 코드에서 직접 만든 문서 하나를 두고, 앱을 부르는 코드도 그 문서로 만듭니다.</p><p>제목의 OpenAPI는 요청 주소와 입력 형식·응답 형식을 JSON으로 적는 규격의 이름입니다. 이 절에서는 그 규격으로 적은 문서를 응답 문서라고 부릅니다. 제목의 TS는 TypeScript의 줄임말로, JavaScript에 자료의 형식을 적을 수 있게 한 언어입니다. 제목의 SDK는 Software Development Kit의 줄임말로, 서비스를 부르는 코드를 묶어 둔 것입니다. 이 절에서는 응답 문서로 만든 TS 코드 묶음을 생성 SDK라고 부릅니다.</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p><a href="01-비동기-라우팅과-스키마.html">01절</a>에서는 처리 함수 매개변수 힌트에 적은 양식 클래스가 요청 본문의 입력 형식이 되었습니다. 맞지 않는 요청은 처리 함수 전에 422를 받았습니다. 데코레이터 줄의 <code>response_model</code>에 적은 양식 클래스는 응답 형식이 되어, 내보낼 칸만 골랐습니다. 이 절은 그 두 형식이 응답 문서에 어떻게 적히는지 봅니다.</p><p><a href="../../part5/ch19-model-tools/02-Pydantic-인자와-반환-스키마.html">Ch 19 02절</a>에서는 양식 클래스를 메서드 <code>model_json_schema()</code>로 딕셔너리로 바꿔, 칸마다 적힌 규칙을 봤습니다. 이 절의 응답 문서에 적힌 입력 형식도, 같은 방법으로 만든 딕셔너리와 같았습니다.</p><p><a href="05-POST-SSE-이벤트-설계.html">05절</a>에서는 인자 <code>response_class</code>로 SSE를 보내면, 응답 문서의 본문 종류가 <code>text/event-stream</code>이 되는 것을 봤습니다. <a href="06-fetch-재연결과-오류-이벤트.html">06절</a>에서는 TS 파일 <code>client/stream.ts</code>가 함수 <code>fetch</code>로 SSE 사건을 읽는 모양을 글로 읽었습니다. <a href="07-인증-CORS-타임아웃.html">07절</a>에서는 보안 도구 클래스 <code>HTTPBearer</code>를 쓴 새 앱의 응답 문서에만 보안 방식 칸이 있었습니다. 실습 앱은 접근 토큰을 요청 머리 매개변수 <code>authorization</code>으로 받아, 보안 방식 칸이 없었습니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>비유로 시작하기</h3><p>차량 공장은 새 화물 열차를 만들기 전에, 탁자 위에 작은 축소 모형부터 받습니다. 모형에는 칸 다섯이 차례대로 놓여 있고, 칸마다 색이 칠해져 있습니다. 공장은 모형만 보고 실제 칸을 만들고, 한 가지 색으로 칠한 칸은 벽과 지붕까지 갖춘 칸으로 만듭니다. 줄무늬만 그린 칸은 공장이 모르는 표시라서, 바닥만 있는 빈 칸으로 둡니다.</p><p>축소 모형이 응답 문서이고, 모형의 칸 하나가 요청 주소 하나입니다. 공장은 생성기이고, 공장이 만든 실제 칸이 생성 SDK의 함수입니다. 줄무늬 칸은 응답 형식을 키 <code>itemSchema</code>로 적은 SSE 요청 주소입니다. 바닥만 있는 칸은 <code>Promise&lt;void&gt;</code>를 내놓는 함수입니다.</p><p>비유와 다른 점이 있습니다. 응답 문서는 사람이 만들지 않고, 앱 객체가 처리 함수와 양식 클래스에서 만듭니다. 생성기가 줄무늬를 모른다는 것은 노트북 밖에서 생성기를 실행했을 때 나온 경고로만 확인했습니다. 이 노트북에서는 생성기를 실행하지 않았습니다.</p>
{{img:08-5-모형을-보고-만든-화물-칸|흰 바탕에 앞쪽 나무 탁자 위 작은 모형 열차 칸 다섯이 한 줄로 놓여 있습니다. 왼쪽 셋은 올리브색 칸이고, 오른쪽 둘은 흰색과 회색 빗금 줄무늬 칸입니다. 탁자 뒤 비스듬한 선로에는 실제 화물 칸 다섯이 같은 차례로 서 있습니다. 왼쪽 셋은 벽과 지붕이 있는 올리브색 칸이고, 오른쪽 둘은 바닥과 바퀴만 있는 빈 칸입니다. 기관차·사람·글자·숫자·화살표는 없는 그림|모형에서 한 가지 색인 칸 셋은 벽과 지붕이 있는 실제 칸이 되었고, 줄무늬 칸 둘은 바닥만 있는 빈 칸이 되었습니다.}}
<p class="look"><b>그림 읽기</b> — 앞쪽 나무 탁자 위 모형 칸 다섯은 왼쪽 셋이 올리브색, 오른쪽 둘이 흰색과 회색의 빗금 줄무늬입니다. 뒤쪽 선로의 실제 화물 칸 다섯도 같은 차례로 서 있습니다. 왼쪽 셋은 벽과 지붕이 있는 올리브색 칸이고, 오른쪽 둘은 바닥과 바퀴만 있는 빈 칸입니다. 모형이 응답 문서이고, 실제 칸 다섯이 생성 SDK의 함수 다섯입니다. 줄무늬 칸 둘이 <code>itemSchema</code>로 적은 SSE 요청 주소이고, 빈 칸 둘이 <code>Promise&lt;void&gt;</code>를 내놓는 함수입니다.</p>
<h3>응답 문서의 모양</h3><p>앱 객체의 메서드 <code>openapi</code>는 앱에 이은 처리 함수를 모두 훑어, 응답 문서를 딕셔너리로 만듭니다. 맨 위 칸은 넷입니다. 칸 <code>openapi</code>에는 규격의 판 <code>3.1.0</code>이, 칸 <code>info</code>에는 앱의 제목과 판이 적힙니다. 칸 <code>paths</code>는 요청 주소마다 요청 방식과 요청 본문, 응답을 적습니다. 칸 <code>components</code>는 여러 곳에서 쓰는 형식을 모아 둡니다.</p><p>요청 주소 쪽에는 형식을 다시 적지 않고, 키 <code>$ref</code>로 칸 <code>components</code>의 자리를 가리킵니다. 요청 주소마다 붙는 이름 <code>operationId</code>는 처리 함수 이름과 요청 주소, 요청 방식을 이어 만듭니다. 앱 객체는 처음 만든 문서를 속성 <code>openapi_schema</code>에 담아 두고, 다음부터는 같은 객체를 내놓습니다. 요청 주소 <code>/openapi.json</code>으로 받는 문서도 이 딕셔너리를 JSON 글로 바꾼 것입니다.</p>
<table><thead><tr><th>말</th><th>뜻</th></tr></thead><tbody><tr><td>응답 문서(OpenAPI 문서)</td><td>앱 객체가 요청 주소마다 받는 요청과 내놓는 응답의 모양을, OpenAPI 규격에 맞춰 적은 JSON 문서입니다. 만들 열차를 작게 줄인 모형이, 칸의 차례와 칸마다 실을 짐의 모양을 보여 주는 것과 같습니다. 이 절에서는 메서드 <code>app.openapi()</code>가 이 문서를 딕셔너리로 내놓고, 실습 폴더의 <code>openapi.json</code>이 같은 문서를 JSON 글로 적은 파일입니다.</td></tr><tr><td>생성 SDK</td><td>응답 문서를 생성기에 넣어 만든, 앱을 부르는 코드 묶음입니다. 차량 공장이 축소 모형만 보고 실제 화물 칸을 만드는 것과 같습니다. 이 절에서는 생성기 <code>typescript-fetch</code> 7.25.0이 만든 <code>client/generated/</code>의 파일 열여덟(TS 파일 열하나와 설명 문서 일곱)이 생성 SDK입니다.</td></tr></tbody></table>
<p>새 말을 이 절 코드에서 보면 이렇습니다. 응답 문서는 <code>app.openapi()</code>가 내놓은 딕셔너리였고, 실습 폴더의 <code>openapi.json</code>과 글이 같았습니다. 생성 SDK의 <code>DefaultApi.ts</code>에는 요청 주소마다 함수가 하나씩 있었습니다.</p>
{{mermaid:08-1-앱-객체에서-생성-SDK까지|위에서 아래로 읽는 흐름도입니다. 초록 상자 실습 앱 객체 app 처리 함수 다섯에서, 회색 상자 FastAPI가 처리 함수와 양식 클래스를 훑어 적음을 지나 노란 상자 응답 문서 딕셔너리 OpenAPI 3.1.0 요청 주소 다섯으로 갑니다. 이어서 노란 상자 실습 폴더 openapi.json 새로 만든 글과 같음 True, 회색 상자 생성기 7.25.0 typescript-fetch 노트북 밖 README 명령을 지나 초록 상자 생성 SDK client/generated 요청 주소마다 함수 하나에 닿는 그림|앱 객체가 만든 응답 문서는 실습 폴더의 openapi.json과 같았고, 생성 SDK는 그 문서로 노트북 밖에서 만든 코드입니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 초록 상자는 실습 폴더의 앱과 파일이고, 노란 상자 둘은 노트북 2절과 3절의 출력입니다. 회색 상자 둘은 라이브러리와 생성기가 하는 일이고, 생성기는 이 노트북에서 실행하지 않았습니다.</p>
<h3>생성 SDK를 만드는 곳</h3><p>생성 SDK는 노트북 밖에서 README 명령으로 만듭니다. 명령 <code>npx @openapitools/openapi-generator-cli generate</code>가 응답 문서를 읽고, 생성기 <code>typescript-fetch</code>로 TS 파일을 씁니다. 생성기는 Java 프로그램이라서, JDK 11 이상이 필요합니다. 생성기 판은 실습 폴더의 파일 <code>openapitools.json</code>이 <code>7.25.0</code>으로 정합니다.</p><p>생성기는 JSON 글로 답하는 요청 주소마다 응답 형식이 있는 함수를 만들었습니다. SSE 사건으로 답하는 요청 주소는 응답 형식을 키 <code>itemSchema</code>로 적고, 생성 SDK의 그 함수는 응답 본문을 값으로 주지 않습니다. 노트북 밖에서 생성기를 실행해 보니, 생성기는 키 <code>itemSchema</code>를 뜻밖의 칸이라고 경고했습니다. 그래서 SSE 사건은 <a href="06-fetch-재연결과-오류-이벤트.html">06절</a>의 손으로 쓴 <code>client/stream.ts</code>가 읽습니다.</p><p>이 노트북에서는 생성기와 TS 검사 도구를 실행하지 않았습니다. 만들어 둔 생성 SDK 파일을 파이썬으로 열어, 필요한 줄을 찾아 읽기만 했습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북 2절은 메서드 <code>openapi</code>로 응답 문서를 만들고, 요청 주소와 형식이 적힌 칸을 차례로 꺼냅니다. 3절은 그 문서를 JSON 글로 바꿔, 실습 폴더의 <code>openapi.json</code>과 견줍니다. 4절은 생성 SDK 파일을 열어, 요청 주소마다 만든 함수와 요청 인자, 칸 이름을 찾습니다.</p><p>5절은 의존성 하나만 바꾼 두 실행으로 실험합니다. 모델 요청은 0번이고, API 키 없이 실행합니다. 서버 프로그램을 띄우지 않아 네트워크와 포트, 자식 프로세스를 쓰지 않습니다. 실습 폴더의 파일은 읽기만 하며, 걸린 시간은 재지 않았습니다.</p>
{{notebook:08-OpenAPI와-TS-SDK}}
<p class="look"><b>확인할 점</b> — 노트북 2절에서 <code>OpenAPI 판: 3.1.0</code>과 <code>요청 주소 수: 5</code>를 찾습니다. 3절에서는 <code>두 글이 같은가: True</code>를 봅니다. 4절에서는 <code>생성기 판: 7.25.0</code>과, 140행·278행의 <code>Promise&lt;void&gt;</code>를 확인합니다.</p>
{{mermaid:08-2-요청-주소-v1-chat의-칸|위에서 아래로 읽는 흐름도입니다. 맨 위 초록 상자 POST /v1/chat operationId chat_v1_chat_post에서 노란 상자 넷으로 갈라집니다. 넷은 요청 본문 형식 ChatRequest를 가리킴, 200 응답 형식 ChatResponse를 가리킴, 422 응답 입력 형식 검사, 매개변수 authorization 자리 header입니다. 요청 본문 형식 상자 아래에는 노란 상자 components의 ChatRequest 꼭 채울 칸 둘 question 1자 이상 500자 이하가 있는 그림|요청 주소 /v1/chat의 칸은 요청 본문과 200 응답의 형식을 components 쪽 자리로 가리켰고, 가리킨 ChatRequest에 글자 수 조건이 적혀 있었습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 초록 상자는 실습 앱의 요청 주소 하나이고, 노란 상자는 모두 노트북 2절의 출력입니다. 요청 본문 형식 상자는 형식을 다시 적지 않고, 맨 아래 상자의 자리를 가리킵니다.</p>
{{mermaid:08-3-요청-주소와-생성-함수|위에서 아래로 읽는 흐름도입니다. 노란 상자 JSON 요청 주소 셋 본문 종류 아래 schema와 노란 상자 SSE 요청 주소 둘 본문 종류 아래 itemSchema가 회색 상자 생성기 typescript-fetch 노트북 밖으로 모입니다. 생성기에서 노란 상자 함수 셋 ChatResponse나 HealthResponse를 내놓는 Promise와, 노란 상자 함수 둘 void를 내놓는 Promise 응답 본문을 읽지 않음으로 갈라집니다. 함수 둘 상자에서 점선이 초록 상자 SSE 사건은 손으로 쓴 client/stream.ts가 fetch로 읽음으로 이어지는 그림|JSON 요청 주소 셋의 함수는 응답 형식을 내놓았고, SSE 요청 주소 둘의 함수는 void를 내놓아 SSE 사건은 손으로 쓴 TS 파일이 읽습니다.}}
<p class="look"><b>도식 읽기</b> — 위에서 아래로 읽습니다. 위 노란 상자 둘은 노트북 2절, 아래 노란 상자 둘은 4절의 출력이고, 회색 상자 생성기는 노트북에서 실행하지 않았습니다. 점선은 생성 SDK 대신 다른 파일이 맡는 갈래이고, 초록 상자는 06절에서 글로 읽은 실습 폴더 파일입니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>가설은 07절의 결과에서 세웠습니다. 07절의 두 앱은 인증을 적는 방법뿐 아니라, 처리 함수와 요청 주소도 달랐습니다. 이 실험은 같은 처리 함수 <code>health</code>를 같은 요청 주소 <code>GET /v1/ping</code>으로 새 앱 객체 둘에 이었습니다. 바꾼 것은 인자 <code>dependencies</code>에 적은 것 하나입니다. 실행 1은 실습 앱의 제공 함수 <code>require_token</code>이고, 실행 2는 보안 객체 <code>HTTPBearer()</code>입니다.</p>
{{mermaid:08-4-의존성-하나만-바꾼-두-응답-문서|맨 위 파란 상자 같은 처리 함수 health GET /v1/ping 새 앱 객체 아래에 칸 둘이 나란히 있습니다. 왼쪽 칸 실행 1 제공 함수에는 초록 상자 dependencies에 require_token에서 노란 상자 보안 방식 칸 False 매개변수 authorization 응답 코드 200과 422로 이어집니다. 오른쪽 칸 실행 2 보안 객체에는 파란 상자 dependencies에 HTTPBearer 객체에서 노란 상자 보안 방식 칸 True security 칸 HTTPBearer 응답 코드 200으로 이어집니다. 두 칸은 맨 아래 회색 상자 두 실행 모두 머리 없음 401 교재용 접근 토큰 200으로 모이는 그림|의존성 하나만 보안 객체로 바꾸자, 상태 코드는 같았는데 응답 문서에 보안 방식 칸과 security 칸이 생겼습니다.}}
<p class="look"><b>도식 읽기</b> — 맨 위 파란 상자는 두 실행이 함께 쓴 처리 함수와 요청 주소입니다. 왼쪽 칸이 실행 1, 오른쪽 칸이 실행 2이고, 칸마다 위가 의존성, 아래가 노트북 5절의 출력입니다. 맨 아래 회색 상자는 두 실행에서 같았던 상태 코드입니다.</p>
<table><thead><tr><th>견준 것</th><th>실행 1(제공 함수)</th><th>실행 2(보안 객체)</th></tr></thead><tbody><tr><td>바꾼 값 — 인자 <code>dependencies</code></td><td><code>[Depends(require_token)]</code></td><td><code>[Depends(bearer)]</code> — <code>bearer = HTTPBearer()</code></td></tr><tr><td>보안 방식 칸 <code>securitySchemes</code></td><td><code>False</code></td><td><code>True</code> — <code>{'HTTPBearer': {'type': 'http', 'scheme': 'bearer'}}</code></td></tr><tr><td>요청 주소의 칸 <code>security</code></td><td><code>False</code></td><td><code>True</code> — <code>[{'HTTPBearer': []}]</code></td></tr><tr><td>요청 주소의 칸 <code>parameters</code></td><td><code>True</code> — <code>authorization</code>·<code>header</code></td><td><code>False</code></td></tr><tr><td>응답 코드</td><td><code>['200', '422']</code></td><td><code>['200']</code></td></tr><tr><td>머리 없는 요청</td><td><code>401</code></td><td><code>401</code></td></tr><tr><td>교재용 접근 토큰을 실은 요청</td><td><code>200</code></td><td><code>200</code></td></tr></tbody></table>
<p>두 실행은 머리 없는 요청에 401을, 교재용 접근 토큰을 실은 요청에 200을 보냈습니다. 두 요청에서 상태 코드는 같았지만, 응답 문서는 달랐습니다. 실행 2에만 칸 <code>components</code>의 보안 방식과 요청 주소의 칸 <code>security</code>가 생겼습니다. 실행 1은 접근 토큰을 매개변수 <code>authorization</code>으로 적었고, 그래서 422 응답도 함께 적혔습니다.</p><p>문서를 읽는 쪽에서 보면 이 차이가 큽니다. 실행 1의 문서에는 넣을 수 있는 요청 머리 하나가 적혀 있을 뿐, 그 값이 인증에 쓰인다는 표시는 없습니다. 실행 2의 문서는 이 요청 주소가 Bearer 방식의 인증을 쓴다고 적습니다. 실습 앱은 실행 1 모양이라, 생성 SDK도 접근 토큰을 요청마다 인자 <code>authorization</code>으로 받았습니다.</p><p>노트북 밖에서 두 실행의 응답 문서를 생성기에 한 번씩 넣어 보았습니다. 실행 1의 문서로 만든 함수는 인자 <code>authorization</code>을 받았습니다. 실행 2의 문서로 만든 함수에는 그 인자가 없고, 설정 칸 <code>accessToken</code>의 값으로 요청 머리 <code>Authorization</code>을 채웠습니다. 이 노트북에서는 실행하지 않았고, 생성기 7.25.0에서 한 번 본 결과입니다.</p>
<p>새 커널로 두 번 실행해 견주자, 코드 셀의 출력이 셀마다 모두 같았습니다. 한 번은 프로젝트 맨 위에서, 한 번은 <code>notebooks/</code> 폴더에서 연 커널이었습니다. 노트북 밖에서도 같은 장면을 파이썬 파일로 다섯 번 실행해, 출력이 모두 같았습니다. 모델을 부르지 않아, 응답 문서의 칸은 앱과 설치판 라이브러리의 코드가 정합니다.</p>
<p class="look"><b>확인할 점</b> — 5절 실행 1의 <code>보안 방식 칸이 있는가: False</code>와, 실행 2의 <code>보안 방식 칸이 있는가: True</code>를 찾습니다. 결과 표의 줄 <code>security 칸 | False | True</code>와 <code>머리 없는 요청 | 401 | 401</code>도 확인합니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul><li>실습 폴더의 <code>openapi.json</code>은 지금 앱으로 만든 글과 같아서, 이 노트북은 파일을 다시 쓰지 않았습니다. 앱 파일의 요청 주소나 양식 클래스를 바꾸면 응답 문서가 바뀝니다. 그때는 파일과 생성 SDK를 함께 다시 만들고, README의 TS 검사 명령도 다시 실행합니다.</li><li>앱 객체는 처음 만든 응답 문서를 속성 <code>openapi_schema</code>에 담아 둡니다. 설치판 fastapi <code>applications.py</code> 1083~1084행이 문서가 없을 때만 새로 만듭니다. 그래서 문서를 만든 뒤에 이은 요청 주소는 문서에 나오지 않습니다. 이 노트북에서는 실행하지 않았고, 노트북 밖에서 한 번 확인했습니다.</li><li>노트북 밖에서 README 명령으로 생성기를 실행하자, 요청 주소 둘의 <code>itemSchema</code>가 뜻밖의 칸이라는 경고가 나왔습니다. 명령의 <code>--skip-validate-spec</code>이 문서 검사를 건너뛰게 해, 생성은 끝까지 갔습니다. 빈 폴더에 처음 만들면 목록 파일 <code>.openapi-generator/FILES</code>에 한 줄이 더 있었습니다. 같은 폴더에 한 번 더 만들자, 실습 폴더의 생성 SDK와 파일이 모두 글자까지 같았습니다.</li><li>실습 폴더 README의 TS 검사 명령은 판을 적은 <code>npx --package typescript@7.0.2 tsc …</code>입니다. 노트북 밖에서 2026-09-29에 최신 판을 받아 실행하자 판이 7.0.2였고, 오류 없이 끝났습니다. 다른 판에서는 실행하지 않았습니다.</li><li>생성 SDK는 가져오는 줄에 파일 확장자를 적지 않습니다. 그래서 Node.js v22.23.2가 TS 파일을 바로 읽는 방식으로는 돌지 않았습니다. 노트북 밖에서 불러 보니 오류 <code>ERR_MODULE_NOT_FOUND</code>가 났습니다. 실습 폴더 README의 시험 명령은 생성 SDK가 아니라, 직접 적은 시험 파일 <code>client/test_stream.ts</code>를 이 방식으로 실행합니다. 06절에서 노트북 밖에 실행해 통과했고, 이 절에서는 실행하지 않았습니다.</li><li>생성 SDK 파일의 머리 주석은 손으로 고치지 말라고 적습니다. 생성기를 다시 실행하면 파일을 새로 쓰기 때문입니다. 고칠 일이 있으면 앱 파일을 고친 뒤 다시 만듭니다.</li><li>생성 SDK의 TS 형식에는 칸 이름과 글이라는 형식만 있고, 글자 수와 <code>pattern</code> 조건은 없습니다. 그 조건은 서버의 입력 형식 검사가 맡아, 어기면 422로 답합니다.</li><li>실행 2의 보안 객체는 <a href="07-인증-CORS-타임아웃.html">07절</a>에서 본 것처럼 접근 토큰 글을 견주지 않습니다. 응답 문서에 보안 방식 칸이 생겨도, 글을 견주는 줄은 우리 코드가 따로 적어야 합니다. 이 절은 실습 앱의 인증을 바꾸지 않았고, 응답 문서와 생성 SDK도 그대로 두었습니다.</li><li>걸린 시간은 재지 않았습니다. 교재 출력은 Linux의 Python 3.12.13으로 만들었고, 다른 판과 Windows·macOS에서는 실행하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul><li>메서드 <code>openapi</code>가 내놓은 응답 문서는 실습 폴더 <code>openapi.json</code>과 글이 같았습니다.</li><li>생성 SDK에서 SSE 사건으로 답하는 요청 주소 둘의 함수는 <code>Promise&lt;void&gt;</code>를 내놓았습니다.</li><li>의존성 하나만 보안 객체로 바꾸자, 상태 코드는 같은데 응답 문서에 보안 방식 칸이 생겼습니다.</li></ul><p><strong>다음 학습과 이어지는 지점</strong> — <a href="09-실제-Agent-HTTP-통합.html">09절</a>에서는 실제로 모델을 부르는 에이전트를 요청 주소 <code>/v1/chat/live</code>로 부릅니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz" open><summary>문제 5개 · 해설 포함</summary><p class="quiz-q">1. 응답 문서에서 요청 주소 목록은 어느 칸에 있고, 이 앱에는 몇 개였나요?</p><p class="quiz-a">칸 <code>paths</code>에 있고, 다섯 개였습니다. 문서를 내주는 요청 주소 <code>/openapi.json</code>은 목록에 없습니다. 틀렸다면 노트북 2절을 다시 읽습니다.</p><p class="quiz-q">2. 요청 본문 형식에 적힌 키 <code>$ref</code>는 무엇을 뜻하나요?</p><p class="quiz-a">같은 문서의 다른 자리를 가리키는 표시입니다. 값 <code>#/components/schemas/ChatRequest</code>는 칸 <code>components</code> 안의 형식 <code>ChatRequest</code>를 가리킵니다. 틀렸다면 노트북 2절을 다시 읽습니다.</p><p class="quiz-q">3. 동료가 「생성 SDK의 함수 <code>chatStreamV1ChatStreamPost</code>로 SSE 사건을 받으면 된다」고 말합니다. 맞나요?</p><p class="quiz-a">맞지 않습니다. 그 함수는 <code>Promise&lt;void&gt;</code>를 내놓고, 받은 응답을 <code>VoidApiResponse</code>로 감싸 본문을 읽지 않습니다. SSE 사건은 06절의 <code>client/stream.ts</code>가 읽습니다. 틀렸다면 노트북 4절을 다시 읽습니다.</p><p class="quiz-q">4. 앱 파일의 양식 클래스를 고쳤다면, <code>openapi.json</code>과 생성 SDK는 어떻게 하나요?</p><p class="quiz-a">응답 문서가 바뀌므로 파일을 다시 쓰고, 생성기로 생성 SDK를 다시 만듭니다. 생성 SDK 파일을 손으로 고치지 않습니다. 틀렸다면 노트북 3절과 4절을 다시 읽습니다.</p><p class="quiz-q">5. 5절 실험에서 바꾼 값은 무엇이고, 응답 문서에 무엇이 생겼나요?</p><p class="quiz-a">인자 <code>dependencies</code>에 적은 것을 제공 함수 <code>require_token</code>에서 보안 객체로 바꿨습니다. 실행 2에만 보안 방식 칸과 칸 <code>security</code>가 생겼고, 상태 코드는 두 실행이 같았습니다. 틀렸다면 노트북 5절을 다시 읽습니다.</p></details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul><li><div><a href="https://fastapi.tiangolo.com/tutorial/first-steps/">FastAPI First Steps</a></div>확인 2026-09-29 · OpenAPI는 API의 요청 주소와 매개변수, 주고받는 자료를 적는 규격이라고 적습니다. 라이브러리 FastAPI가 이 문서를 만들어 <code>/openapi.json</code>으로 내준다고 적습니다. 클라이언트 코드를 만드는 데 쓸 수 있다고도 적습니다.</li><li><div><a href="https://fastapi.tiangolo.com/advanced/generate-clients/">FastAPI Generating SDKs</a></div>확인 2026-09-29 · <code>operationId</code>는 함수 이름과 요청 주소, 요청 방식으로 만든다고 적습니다. 도구로 OpenAPI Generator를 들고, 앱을 바꾸면 다시 만들라고 적습니다.</li><li><div><a href="https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/">FastAPI Dependencies in path operation decorators</a></div>확인 2026-09-29 · 인자 <code>dependencies</code>는 <code>Depends()</code>의 목록이라고 적습니다. 값은 쓰지 않지만 보통 의존성처럼 실행되고, 오류로 멈출 수 있다고 적습니다.</li><li><div><a href="https://openapi-generator.tech/docs/generators/typescript-fetch/">OpenAPI Generator typescript-fetch</a></div>확인 2026-09-29 · Fetch API로 부르는 TS 코드를 만든다고 적습니다. 보안 방식 BearerToken을 지원하고, 칸 이름을 바꾸는 설정의 기본값은 camelCase라고 적습니다.</li><li><div><a href="https://github.com/OpenAPITools/openapi-generator-cli">OpenAPI Generator CLI</a></div>확인 2026-09-29 · JDK 11이 가장 낮게 지원하는 판이라고 적습니다. 생성기 판을 <code>openapitools.json</code>에 적어 둔다고 적습니다.</li><li>설치판 fastapi 0.135.0 소스 <code>applications.py</code> 1069행이 메서드 <code>openapi</code>입니다. 1083~1084행은 문서가 없을 때만 만들고, 1117행은 <code>/openapi.json</code>을 문서에서 뺍니다.</li><li>같은 판 <code>openapi/utils.py</code> 289~296행은 보안 객체를 찾아 칸 <code>security</code>를 적습니다. 457~470행은 매개변수나 요청 본문이 있을 때만 422를 적고, 573~575행은 보안 방식을 칸 <code>components</code>에 모읍니다. <code>utils.py</code> 95~100행은 <code>operationId</code>를 만듭니다.</li><li>실습 폴더에서는 <code>openapi.json</code>과 <code>openapitools.json</code>을 읽었습니다. 생성 SDK 파일 <code>DefaultApi.ts</code>는 머리 주석 7·10·12행과 요청 인자 37~82행을 읽었습니다. 같은 파일의 함수와 응답을 감싸는 줄은 134·140·184·190·221·227·272·278·322·328행입니다. 파일 <code>models/ChatRequest.ts</code>는 25·29·52·68행을 읽었습니다.</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# OpenAPI와 TS SDK

**이 노트북에서 할 일**

1. 앱 객체가 만든 응답 문서에서 요청 주소와 입력 형식·응답 형식을 찾습니다.
2. 응답 문서로 만든 TS 코드(생성 SDK)에서 요청 주소마다 만든 함수를 읽습니다.
3. 인증을 적는 자리 하나만 바꾸면 응답 문서가 어떻게 바뀌는지 실험합니다.

**준비물** — 이 노트북은 모델을 부르지 않습니다.
모델 요청은 0번이고, API 키 없이 실행합니다.
예상 비용도 0달러입니다.
실습 앱의 에이전트 그래프도 이 절에서는 부르지 않습니다.
그래서 다시 실행해도 같은 값이 나와야 합니다.

요청은 시험용 클라이언트로 같은 노트북 안에서 보냅니다.
서버 프로그램을 띄우지 않고, 네트워크와 포트를 쓰지 않습니다.
실습 폴더의 파일을 가져오고 읽기만 하며, 쓰는 파일은 없습니다.
TS 코드를 만드는 생성기와 TS 검사 도구는 노트북에서 실행하지 않습니다.

걸린 시간은 재지 않았습니다.
앞 절에서 배운 함수는 이 절에서 쓰지 않아, 도구 파일도 가져오지 않습니다.

**기준 버전** — 첫 셀에서 패키지 여섯을 설치합니다.
판은 fastapi 0.135.0, httpx 0.28.1, pydantic 2.12.5, starlette 1.6.0입니다.
패키지 langgraph 1.2.11과 langchain 1.4.0은 실습 앱 파일이 가져오는 패키지입니다.
여섯 모두 실습 폴더 잠금과 같은 판입니다.

교재 출력은 Linux의 Python 3.12.13으로 만들었습니다.
다른 판과 Windows·macOS에서는 실행하지 않았습니다.

**강의와 실습 범위** — 강의 시간에는 2~4절을 읽고, 5절 실험의 가설을 함께 세웁니다.
5절의 두 실행은 실습 시간에 실행합니다.

실습 폴더 `labs/part7/ch30-fastapi-serving`에서 `uv sync --locked`를 실행합니다.
그다음 `notebooks/` 폴더의 이 노트북을 열고, 실습 폴더의 `.venv` 커널을 고릅니다.
첫 셀부터 순서대로 실행합니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위에서 아래로 읽는 흐름도입니다. 초록 상자 실습 앱 객체 app 처리 함수 다섯에서, 회색 상자 FastAPI가 처리 함수와 양식 클래스를 훑어 적음을 지나 노란 상자 응답 문서 딕셔너리 OpenAPI 3.1.0 요청 주소 다섯으로 갑니다. 이어서 노란 상자 실습 폴더 openapi.json 새로 만든 글과 같음 True, 회색 상자 생성기 7.25.0 typescript-fetch 노트북 밖 README 명령을 지나 초록 상자 생성 SDK client/generated 요청 주소마다 함수 하나에 닿는 그림](attachment:08-1-앱-객체에서-생성-SDK까지.png)

위에서 아래로 읽습니다.
초록 상자는 실습 폴더의 앱과 파일이고, 노란 상자 둘은 노트북 2절과 3절의 출력입니다.
회색 상자 둘은 라이브러리와 생성기가 하는 일이고, 생성기는 이 노트북에서 실행하지 않았습니다.

### [2] markdown {}

## 1. 준비

07절에서는 보안 도구 클래스 `HTTPBearer`를 쓴 새 앱의 응답 문서에만 보안 방식 칸이 있는 것을 봤습니다.
이 절은 앱 객체가 만드는 응답 문서를 처음부터 읽습니다.
제목의 OpenAPI는 요청 주소와 입력 형식·응답 형식을 JSON으로 적는 규격의 이름입니다.
제목의 TS는 TypeScript의 줄임말로, JavaScript에 자료의 형식을 적을 수 있게 한 언어입니다.
제목의 SDK는 Software Development Kit의 줄임말로, 서비스를 부르는 코드를 묶어 둔 것입니다.

이 절에서는 OpenAPI 규격으로 적은 문서를 응답 문서, 그 문서로 만든 TS 코드 묶음을 생성 SDK라고 부릅니다.
두 말은 2절과 4절에서 자세히 풉니다.
첫 셀은 패키지 여섯을 설치하고 설치된 판 번호를 출력합니다.
설치에는 몇십 초가 걸릴 수 있습니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:44.419786Z', 'iopub.status.busy': '2026-09-29T10:49:44.419615Z', 'iopub.status.idle': '2026-09-29T10:49:45.066130Z', 'shell.execute_reply': '2026-09-29T10:49:45.065639Z'}, 'lesson_role': 'setup'}

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

**결과 읽기** — 출력 줄 `fastapi: 0.135.0`과 `starlette: 1.6.0`이 보입니다.
여섯 모두 실습 폴더 잠금과 같은 판이고, 07절과 같은 목록입니다.
응답 문서를 만드는 코드는 패키지 fastapi에 들어 있습니다.
이 절은 모델 객체를 만들지 않아, API 키를 확인하는 셀도 없습니다.

다음 셀은 이 절에서 쓸 이름을 가져옵니다.
모듈 json은 딕셔너리를 JSON 글로 바꾸고, 파일의 JSON 글을 읽을 때 씁니다.
클래스 `HTTPBearer`는 07절에서 본 보안 도구 클래스로, 5절 실험에서 씁니다.

### [5] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.067208Z', 'iopub.status.busy': '2026-09-29T10:49:45.067120Z', 'iopub.status.idle': '2026-09-29T10:49:45.286713Z', 'shell.execute_reply': '2026-09-29T10:49:45.286325Z'}, 'lesson_role': 'setup'}

```python
# 이 절에서 쓸 이름을 가져옵니다(os와 json은 Python에 들어 있는 모듈입니다)
import os
import json
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer
from fastapi.testclient import TestClient

print("가져온 이름:", "json, Depends, FastAPI, HTTPBearer, TestClient")
```

출력:
```
가져온 이름: json, Depends, FastAPI, HTTPBearer, TestClient

```

### [6] markdown {}

**결과 읽기** — 출력 줄 `가져온 이름: json, Depends, FastAPI, HTTPBearer, TestClient`가 보입니다.
이 절은 앞 절에서 배운 함수를 쓰지 않아, 도구 파일 `serve_tools.py`를 가져오지 않습니다.

다음 셀은 01절 2절과 같은 파일 위치 셀로, 후보 셋 가운데 실습 폴더를 고릅니다.

### [7] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.287405Z', 'iopub.status.busy': '2026-09-29T10:49:45.287352Z', 'iopub.status.idle': '2026-09-29T10:49:45.289708Z', 'shell.execute_reply': '2026-09-29T10:49:45.289378Z'}}

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

다음 셀은 작업 폴더를 실습 폴더로 옮긴 뒤 이름을 가져옵니다.
앱 파일에서 앱 객체 `app`과 처리 함수 `health`, 제공 함수 `require_token`을 가져옵니다.
양식 클래스 `ChatRequest`는 01절에서 본 입력 형식의 클래스입니다.
앱 객체의 속성 `openapi_schema`도 함께 출력합니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.290371Z', 'iopub.status.busy': '2026-09-29T10:49:45.290325Z', 'iopub.status.idle': '2026-09-29T10:49:45.790317Z', 'shell.execute_reply': '2026-09-29T10:49:45.789861Z'}}

```python
# 작업 폴더를 실습 폴더로 옮기고, 앱 객체·처리 함수·제공 함수·양식 클래스를 가져옵니다
os.chdir(lab_path)
from agent_service.app import app, health, require_token
from agent_service.schemas import ChatRequest
print("가져온 앱 객체의 종류:", type(app).__name__)
print("가져온 함수:", health.__name__, require_token.__name__)
print("응답 문서를 담아 둘 속성 openapi_schema:", app.openapi_schema)
```

출력:
```
가져온 앱 객체의 종류: FastAPI
가져온 함수: health require_token
응답 문서를 담아 둘 속성 openapi_schema: None

```

### [10] markdown {}

**결과 읽기** — 출력 줄 `가져온 앱 객체의 종류: FastAPI`와 `가져온 함수: health require_token`이 보입니다.
속성 `openapi_schema`는 아직 `None`입니다.
앱 객체는 응답 문서를 처음 부탁받을 때 만들어, 이 속성에 담아 둡니다.
그런지는 2절에서 확인합니다.

## 2. 앱 객체가 만드는 응답 문서

응답 문서(OpenAPI 문서)는 앱 객체가 요청 주소마다 받는 요청과 내놓는 응답의 모양을 적은 JSON 문서입니다.
만들 열차를 작게 줄인 모형이, 칸의 차례와 칸마다 실을 짐의 모양을 보여 주는 것과 같습니다.
이 앱에서는 앱 객체의 메서드 `openapi`가 이 문서를 딕셔너리로 내놓습니다.
문서의 모양은 OpenAPI 규격이 정하고, 맨 위 칸 `openapi`에 그 규격의 판이 적힙니다.

다음 셀은 메서드 `openapi`를 불러 응답 문서를 만들고, 맨 위 칸을 봅니다.

### [11] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.790968Z', 'iopub.status.busy': '2026-09-29T10:49:45.790912Z', 'iopub.status.idle': '2026-09-29T10:49:45.795679Z', 'shell.execute_reply': '2026-09-29T10:49:45.795327Z'}}

```python
# 앱 객체의 메서드 openapi를 불러 응답 문서를 만들고, 맨 위 칸을 봅니다
openapi_doc = app.openapi()
print("받은 값의 종류:", type(openapi_doc).__name__)
print("맨 위 칸:", list(openapi_doc))
print("OpenAPI 판:", openapi_doc["openapi"])
print("칸 info:", openapi_doc["info"])
```

출력:
```
받은 값의 종류: dict
맨 위 칸: ['openapi', 'info', 'paths', 'components']
OpenAPI 판: 3.1.0
칸 info: {'title': '교육용 Agent API', 'version': '1.0.0'}

```

### [12] markdown {}

**결과 읽기** — 출력 줄 `OpenAPI 판: 3.1.0`이 보입니다.
맨 위 칸은 넷이고, 칸 `info`에는 앱 파일 17행에 적은 제목과 판 `1.0.0`이 들어 있습니다.
판 `1.0.0`은 이 앱에 붙인 판이고, 패키지 fastapi의 판과는 다른 값입니다.
칸 `paths`는 요청 주소마다 받는 요청과 응답을 적고, 칸 `components`는 여러 곳에서 쓰는 형식을 모아 둡니다.

다음 셀은 칸 `paths`에 적힌 요청 주소와 요청 방식을 한 줄씩 출력합니다.

### [13] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.796286Z', 'iopub.status.busy': '2026-09-29T10:49:45.796231Z', 'iopub.status.idle': '2026-09-29T10:49:45.798032Z', 'shell.execute_reply': '2026-09-29T10:49:45.797673Z'}}

```python
# 칸 paths에 적힌 요청 주소와, 요청 주소마다 받는 요청 방식을 한 줄씩 출력합니다
print("요청 주소 수:", len(openapi_doc["paths"]))
print("요청 주소 | 요청 방식")
for address in openapi_doc["paths"]:
    print(address, "|", list(openapi_doc["paths"][address]))
```

출력:
```
요청 주소 수: 5
요청 주소 | 요청 방식
/health | ['get']
/v1/chat | ['post']
/v1/chat/live | ['post']
/v1/chat/stream | ['post']
/v1/chat/live/stream | ['post']

```

### [14] markdown {}

**결과 읽기** — 출력 줄 `요청 주소 수: 5`와, 라벨 줄 아래 다섯 줄이 보입니다.
앱 파일에서 요청 주소 데코레이터 줄로 이은 처리 함수 다섯이 모두 적혔습니다.
요청 주소 `/openapi.json`은 이 목록에 없습니다.
설치판 fastapi `applications.py` 1117행이 문서를 내주는 요청 주소를 문서에서 빼기 때문입니다.

다음 셀은 01절부터 써 온 요청 주소 `/v1/chat`의 칸을 꺼냅니다.
요청 본문과 응답의 형식이 어떻게 적혔는지 봅니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.798598Z', 'iopub.status.busy': '2026-09-29T10:49:45.798544Z', 'iopub.status.idle': '2026-09-29T10:49:45.800713Z', 'shell.execute_reply': '2026-09-29T10:49:45.800330Z'}}

```python
# 요청 주소 /v1/chat의 POST 칸에서, 이름표와 요청 본문·응답의 형식이 적힌 자리를 꺼냅니다
chat_operation = openapi_doc["paths"]["/v1/chat"]["post"]
print("POST /v1/chat의 칸:", list(chat_operation))
print("operationId:", chat_operation["operationId"])
print("요청 본문 형식:", chat_operation["requestBody"]["content"]["application/json"]["schema"])
print("응답 코드:", list(chat_operation["responses"]))
print("200 응답 형식:", chat_operation["responses"]["200"]["content"]["application/json"]["schema"])
print("매개변수 이름과 자리:", chat_operation["parameters"][0]["name"], chat_operation["parameters"][0]["in"])
```

출력:
```
POST /v1/chat의 칸: ['summary', 'operationId', 'parameters', 'requestBody', 'responses']
operationId: chat_v1_chat_post
요청 본문 형식: {'$ref': '#/components/schemas/ChatRequest'}
응답 코드: ['200', '422']
200 응답 형식: {'$ref': '#/components/schemas/ChatResponse'}
매개변수 이름과 자리: authorization header

```

### [16] markdown {}

**결과 읽기** — 출력 줄 `응답 코드: ['200', '422']`와 `operationId: chat_v1_chat_post`가 보입니다.
요청 본문 형식과 200 응답 형식에는 형식 대신 키 `$ref` 하나가 있습니다.
키 `$ref`는 같은 문서의 다른 자리를 가리키는 표시입니다.
값 `#/components/schemas/ChatRequest`는 맨 위 칸 `components`에서 `schemas`, `ChatRequest` 차례로 들어간 자리입니다.
응답 코드 422는 01절에서 본 입력 형식 검사의 응답입니다.

칸 `operationId`는 요청 주소마다 붙는 이름입니다.
설치판 fastapi `utils.py` 95~100행이 처리 함수 이름과 요청 주소, 요청 방식을 이어 만듭니다.
매개변수 `authorization`은 07절에서 본 것처럼, 요청 머리에서 읽는 값입니다.

다음 셀은 칸 `components`에 모은 형식 이름과, 입력 형식 `ChatRequest`의 칸 조건을 봅니다.
마지막 줄은 Ch 19 02절에서 쓴 메서드 `model_json_schema`로 만든 딕셔너리와 견줍니다.

### [17] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.801331Z', 'iopub.status.busy': '2026-09-29T10:49:45.801265Z', 'iopub.status.idle': '2026-09-29T10:49:45.803521Z', 'shell.execute_reply': '2026-09-29T10:49:45.803139Z'}}

```python
# 칸 components에 모은 형식 이름과, 입력 형식 ChatRequest에 적힌 칸 조건을 봅니다
format_table = openapi_doc["components"]["schemas"]
print("형식 이름:", list(format_table))
print("ChatRequest의 꼭 채울 칸:", format_table["ChatRequest"]["required"])
print("칸 question:", format_table["ChatRequest"]["properties"]["question"])
print("칸 thread_id의 pattern:", format_table["ChatRequest"]["properties"]["thread_id"]["pattern"])
print("model_json_schema()로 만든 딕셔너리와 같은가:", ChatRequest.model_json_schema() == format_table["ChatRequest"])
```

출력:
```
형식 이름: ['ChatRequest', 'ChatResponse', 'HTTPValidationError', 'HealthResponse', 'ValidationError']
ChatRequest의 꼭 채울 칸: ['question', 'thread_id']
칸 question: {'type': 'string', 'maxLength': 500, 'minLength': 1, 'title': 'Question', 'examples': ['휴관일을 알려 주세요']}
칸 thread_id의 pattern: ^[a-zA-Z0-9_-]{1,64}$
model_json_schema()로 만든 딕셔너리와 같은가: True

```

### [18] markdown {}

**결과 읽기** — 출력 줄 `칸 question:`에 `'maxLength': 500`과 `'minLength': 1`이 보입니다.
실습 파일 `schemas.py`의 양식 클래스에 `Field`로 적은 글자 수 조건이 그대로 적혔습니다.
꼭 채울 칸은 `question`과 `thread_id` 둘이고, 칸 `thread_id`에는 글 모양 조건 `pattern`이 있습니다.
마지막 줄은 `True`로, Ch 19 02절 방법으로 만든 딕셔너리와 같았습니다.

형식 이름 다섯 가운데 `HTTPValidationError`와 `ValidationError`는 422 응답을 적으려고 라이브러리가 더한 형식입니다.
앱 파일에는 이 두 이름의 클래스가 없습니다.

다음 셀은 JSON 글로 답하는 `/v1/chat`과, SSE 사건으로 답하는 `/v1/chat/stream`의 200 응답을 견줍니다.
본문 종류와, 그 아래에 적힌 키를 봅니다.

### [19] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.804140Z', 'iopub.status.busy': '2026-09-29T10:49:45.804083Z', 'iopub.status.idle': '2026-09-29T10:49:45.805921Z', 'shell.execute_reply': '2026-09-29T10:49:45.805601Z'}}

```python
# 요청 주소 /v1/chat과 /v1/chat/stream의 200 응답에서, 본문 종류와 그 아래 키를 견줍니다
chat_content = chat_operation["responses"]["200"]["content"]
stream_operation = openapi_doc["paths"]["/v1/chat/stream"]["post"]
stream_content = stream_operation["responses"]["200"]["content"]
print("/v1/chat:", list(chat_content), list(chat_content["application/json"]))
print("/v1/chat/stream:", list(stream_content), list(stream_content["text/event-stream"]))
```

출력:
```
/v1/chat: ['application/json'] ['schema']
/v1/chat/stream: ['text/event-stream'] ['itemSchema']

```

### [20] markdown {}

**결과 읽기** — 출력 줄 `/v1/chat/stream: ['text/event-stream'] ['itemSchema']`가 보입니다.
요청 주소 `/v1/chat`은 본문 종류 `application/json` 아래에 키 `schema`로 응답 형식을 적었습니다.
SSE 사건으로 답하는 요청 주소는 키 `itemSchema`로, SSE 사건 하나의 형식을 적었습니다.
05절의 작은 앱에서 본 것처럼, 이 키 아래에 칸 `data`·`event`·`id`·`retry`가 적힙니다.
이 차이가 4절의 생성 SDK에서 다시 나옵니다.

다음 셀은 메서드 `openapi`를 한 번 더 불러, 처음 받은 딕셔너리와 같은 객체인지 봅니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.806597Z', 'iopub.status.busy': '2026-09-29T10:49:45.806550Z', 'iopub.status.idle': '2026-09-29T10:49:45.808323Z', 'shell.execute_reply': '2026-09-29T10:49:45.808044Z'}}

```python
# 메서드 openapi를 한 번 더 불러, 처음 받은 딕셔너리와 같은 객체인지 봅니다
second_doc = app.openapi()
print("두 번째로 받은 값이 같은 객체인가:", second_doc is openapi_doc)
print("속성 openapi_schema가 같은 객체인가:", app.openapi_schema is openapi_doc)
```

출력:
```
두 번째로 받은 값이 같은 객체인가: True
속성 openapi_schema가 같은 객체인가: True

```

### [22] markdown {}

**결과 읽기** — 두 줄 모두 `True`입니다.
연산자 `is`는 두 이름이 같은 객체를 가리키는지 봅니다.
앱 객체는 처음 만든 문서를 속성 `openapi_schema`에 담아 두고, 다음부터는 그 객체를 그대로 내놓습니다.
설치판 fastapi `applications.py` 1083~1084행이 문서가 없을 때만 새로 만듭니다.

그래서 문서를 만든 뒤에 이은 요청 주소는 문서에 나오지 않습니다.
이 노트북에서는 실행하지 않았고, 노트북 밖에서 한 번 확인했습니다.

다음 셀은 요청 주소 `/openapi.json`으로 같은 문서를 받아 봅니다.
시험용 클라이언트로 GET을 보냅니다.

### [23] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.808837Z', 'iopub.status.busy': '2026-09-29T10:49:45.808791Z', 'iopub.status.idle': '2026-09-29T10:49:45.819587Z', 'shell.execute_reply': '2026-09-29T10:49:45.819269Z'}}

```python
# 시험용 클라이언트로 요청 주소 /openapi.json에 GET을 보내, 받은 문서가 같은지 봅니다
client = TestClient(app)
doc_response = client.get("/openapi.json")
print("상태 코드:", doc_response.status_code)
print("본문 종류:", doc_response.headers["content-type"])
print("메서드 openapi가 내놓은 딕셔너리와 같은가:", doc_response.json() == openapi_doc)
```

출력:
```
상태 코드: 200
본문 종류: application/json
메서드 openapi가 내놓은 딕셔너리와 같은가: True

```

### [24] markdown {}

**결과 읽기** — 출력 줄 `상태 코드: 200`과 `본문 종류: application/json`이 보입니다.
받은 문서를 읽은 딕셔너리는 메서드 `openapi`가 내놓은 딕셔너리와 같았습니다.
실습 폴더 README는 서버를 띄운 뒤 주소 `/docs`와 `/openapi.json`에서 이 문서를 보라고 적습니다.
이 절에서는 서버를 띄우지 않아, 그 화면은 열지 않았습니다.

## 3. 응답 문서와 openapi.json

실습 폴더 맨 위에는 파일 `openapi.json`이 있습니다.
응답 문서를 JSON 글로 적은 파일이고, 4절의 생성 SDK는 이 문서를 생성기에 넣어 만든 코드입니다.
다음 셀은 응답 문서를 이 파일과 같은 설정의 JSON 글로 바꿔, 파일 글과 견줍니다.
인자 `ensure_ascii=False`는 한글을 그대로 적게 하고, 인자 `indent`는 칸마다 줄을 바꿔 들여 쓰게 합니다.
파일은 읽기만 하고 다시 쓰지 않습니다.

### [25] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.820222Z', 'iopub.status.busy': '2026-09-29T10:49:45.820172Z', 'iopub.status.idle': '2026-09-29T10:49:45.822601Z', 'shell.execute_reply': '2026-09-29T10:49:45.822266Z'}}

```python
# 응답 문서를 openapi.json과 같은 설정의 JSON 글로 바꾸고, 파일 글과 견줍니다(파일은 읽기만 합니다)
openapi_text = json.dumps(openapi_doc, ensure_ascii=False, indent=2)
with open("openapi.json", encoding="utf-8") as doc_file:
    file_text = doc_file.read()
print("새로 만든 글의 글자 수:", len(openapi_text))
print("파일 글의 글자 수:", len(file_text))
print("두 글이 같은가:", openapi_text == file_text)
print("ensure_ascii를 뺀 글과 같은가:", json.dumps(openapi_doc, indent=2) == file_text)
print("파일 첫 세 줄:", file_text.splitlines()[:3])
```

출력:
```
새로 만든 글의 글자 수: 9987
파일 글의 글자 수: 9987
두 글이 같은가: True
ensure_ascii를 뺀 글과 같은가: False
파일 첫 세 줄: ['{', '  "openapi": "3.1.0",', '  "info": {']

```

### [26] markdown {}

**결과 읽기** — 출력 줄 `두 글이 같은가: True`가 보입니다.
두 글의 글자 수도 `9987`로 같습니다.
인자 `ensure_ascii`를 뺀 글은 한글이 유니코드 번호로 적혀, 파일 글과 같지 않았습니다.
파일 첫 줄은 중괄호이고, 둘째 줄에 규격의 판이 적혀 있습니다.

지금 앱으로 만든 글과 파일 글이 같으므로, 이 노트북은 파일을 다시 쓰지 않습니다.
파일로 쓸 때는 이 글을 `with open(…, "w", encoding="utf-8")`로 연 파일에 적습니다.
앱 파일의 요청 주소나 양식 클래스를 바꾸면 이 글이 달라집니다.
그때는 파일과 생성 SDK를 함께 다시 만듭니다.

## 4. 생성 SDK 읽기

생성 SDK는 응답 문서를 생성기에 넣어 만든, 앱을 부르는 코드 묶음입니다.
차량 공장이 축소 모형만 보고 실제 화물 칸을 만드는 것과 같습니다.
이 실습 폴더에서는 `client/generated/` 폴더의 파일 열여덟(TS 파일 열하나와 설명 문서 일곱)이 생성 SDK입니다.
생성기는 OpenAPI Generator의 `typescript-fetch`로, 06절에서 본 함수 `fetch`로 요청을 보내는 코드를 만듭니다.
생성기는 Java 프로그램이라서, README 명령으로 노트북 밖에서 실행합니다.

다음 셀은 이 절에서 쓸 함수를 정의합니다.
글 줄 목록에서 낱말이 든 줄을 찾아, 줄 번호와 함께 출력합니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.823183Z', 'iopub.status.busy': '2026-09-29T10:49:45.823137Z', 'iopub.status.idle': '2026-09-29T10:49:45.824643Z', 'shell.execute_reply': '2026-09-29T10:49:45.824346Z'}}

```python
# 글 줄 목록에서 word가 든 줄을 찾아, 줄 번호와 앞뒤 공백을 뺀 줄을 한 줄씩 출력합니다
def print_lines_with(text_lines, word):
    print("줄 번호 | 줄")
    for index in range(len(text_lines)):
        if word in text_lines[index]:
            print(index + 1, "|", text_lines[index].strip())
```

출력:
```

```

### [28] markdown {}

**결과 읽기** — 정의 셀이라 출력이 없습니다.
메서드 `strip`은 줄 앞뒤의 공백을 뺀 글을 내놓습니다.
줄 번호는 0부터 세는 자리에 1을 더해, 파일을 열었을 때의 줄 번호와 맞춥니다.

다음 셀은 파일 `openapitools.json`에서 생성기 판을 읽습니다.
그다음 생성 SDK 파일 `DefaultApi.ts`의 머리 주석에서 줄 셋을 찾습니다.
함수 `json.load`는 연 파일의 JSON 글을 읽어 파이썬 값으로 바꿉니다.

### [29] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.825252Z', 'iopub.status.busy': '2026-09-29T10:49:45.825206Z', 'iopub.status.idle': '2026-09-29T10:49:45.828210Z', 'shell.execute_reply': '2026-09-29T10:49:45.827805Z'}}

```python
# openapitools.json에서 생성기 판을 읽고, 생성 SDK 파일 DefaultApi.ts의 머리 주석에서 줄 셋을 찾습니다
with open("openapitools.json", encoding="utf-8") as tools_file:
    generator_config = json.load(tools_file)
print("생성기 판:", generator_config["generator-cli"]["version"])
with open("client/generated/apis/DefaultApi.ts", encoding="utf-8") as ts_file:
    ts_lines = ts_file.read().splitlines()
print_lines_with(ts_lines, "The version of the OpenAPI document")
print_lines_with(ts_lines, "auto generated")
print_lines_with(ts_lines, "Do not edit")
```

출력:
```
생성기 판: 7.25.0
줄 번호 | 줄
7 | * The version of the OpenAPI document: 1.0.0
줄 번호 | 줄
10 | * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
줄 번호 | 줄
12 | * Do not edit the class manually.

```

### [30] markdown {}

**결과 읽기** — 출력 줄 `생성기 판: 7.25.0`이 보입니다.
7행에는 응답 문서의 칸 `info`에 있던 판 `1.0.0`이 적혔습니다.
10행과 12행은 이 파일을 생성기가 만들었으니, 손으로 고치지 말라는 주석입니다.
고칠 일이 있으면 앱 파일을 고치고, 응답 문서와 생성 SDK를 다시 만듭니다.

다음 셀은 같은 파일에서 요청 주소마다 만든 함수를 찾습니다.
네 칸 들여 쓴 `async`로 시작하고, 이름에 `Raw(`와 `RequestOpts(`가 없는 줄이 앱을 부를 때 쓰는 함수입니다.
메서드 `rstrip`은 줄 끝의 공백과 `{`를 빼고, 메서드 `split`은 주어진 글에서 나눕니다.

### [31] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.828755Z', 'iopub.status.busy': '2026-09-29T10:49:45.828711Z', 'iopub.status.idle': '2026-09-29T10:49:45.830704Z', 'shell.execute_reply': '2026-09-29T10:49:45.830346Z'}}

```python
# DefaultApi.ts에서 요청 주소마다 만든 함수의 이름과, 내놓는 값의 형식을 찾습니다
print("줄 번호 | 함수 이름 | 내놓는 값")
for index in range(len(ts_lines)):
    line = ts_lines[index]
    if line.startswith("    async ") and "Raw(" not in line and "RequestOpts(" not in line:
        signature = line.strip().rstrip(" {")
        name = signature.split("(")[0]
        returned = signature.split("): ")[-1]
        print(index + 1, "|", name, "|", returned)
```

출력:
```
줄 번호 | 함수 이름 | 내놓는 값
140 | async chatStreamV1ChatStreamPost | Promise<void>
190 | async chatV1ChatPost | Promise<ChatResponse>
227 | async healthHealthGet | Promise<HealthResponse>
278 | async liveChatStreamV1ChatLiveStreamPost | Promise<void>
328 | async liveChatV1ChatLivePost | Promise<ChatResponse>

```

### [32] markdown {}

**결과 읽기** — 라벨 줄 아래 다섯 줄이, 요청 주소 다섯에 하나씩 만든 함수입니다.
JSON 글로 답하는 요청 주소 셋의 함수는 `Promise<ChatResponse>`나 `Promise<HealthResponse>`를 내놓습니다.
SSE 사건으로 답하는 요청 주소 둘의 함수는 140행과 278행에서 `Promise<void>`를 내놓습니다.
형식 `Promise`는 TS에서 await로 기다려 값을 받는 객체이고, `void`는 줄 값이 없다는 표시입니다.

함수 이름은 2절의 칸 `operationId`를 TS 이름 모양으로 바꾼 것입니다.
예를 들어 `chat_v1_chat_post`가 190행의 `chatV1ChatPost`가 되었습니다.
이름 앞의 `async`는 TS에서도 비동기 함수라는 표시입니다.

다음 셀은 이 함수들이 받은 응답을 어떻게 감싸는지 찾습니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.831299Z', 'iopub.status.busy': '2026-09-29T10:49:45.831248Z', 'iopub.status.idle': '2026-09-29T10:49:45.832777Z', 'shell.execute_reply': '2026-09-29T10:49:45.832495Z'}}

```python
# DefaultApi.ts에서 받은 응답을 감싸는 줄을 찾습니다 — 본문을 읽지 않는 쪽과 JSON으로 읽는 쪽
print_lines_with(ts_lines, "VoidApiResponse(response")
print_lines_with(ts_lines, "JSONApiResponse(response")
```

출력:
```
줄 번호 | 줄
134 | return new runtime.VoidApiResponse(response);
272 | return new runtime.VoidApiResponse(response);
줄 번호 | 줄
184 | return new runtime.JSONApiResponse(response, (jsonValue) => ChatResponseFromJSON(jsonValue));
221 | return new runtime.JSONApiResponse(response, (jsonValue) => HealthResponseFromJSON(jsonValue));
322 | return new runtime.JSONApiResponse(response, (jsonValue) => ChatResponseFromJSON(jsonValue));

```

### [34] markdown {}

**결과 읽기** — 첫 라벨 줄 아래 134행과 272행이 받은 응답을 `VoidApiResponse`로 감쌉니다.
둘째 라벨 줄 아래 세 줄은 `JSONApiResponse`로 감싸고, 본문 JSON을 `ChatResponse` 같은 형식으로 바꿉니다.
SSE 사건으로 답하는 요청 주소 둘의 함수는 응답 본문을 읽어 값으로 주지 않는다는 뜻입니다.
2절에서 본 것처럼, 두 요청 주소는 응답 형식을 키 `schema`가 아니라 `itemSchema`로 적었습니다.

노트북 밖에서 생성기를 실행해 보니, 생성기는 키 `itemSchema`를 뜻밖의 칸이라고 경고했습니다.
SSE 사건은 06절에서 글로 읽은 TS 파일 `client/stream.ts`가 함수 `fetch`로 읽습니다.
생성 SDK와 손으로 쓴 이 파일이 요청 주소를 나눠 맡습니다.

다음 셀은 요청 인자의 칸을 적은 TS 선언과, 그 안의 칸 `authorization`을 찾습니다.

### [35] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.833280Z', 'iopub.status.busy': '2026-09-29T10:49:45.833235Z', 'iopub.status.idle': '2026-09-29T10:49:45.834875Z', 'shell.execute_reply': '2026-09-29T10:49:45.834550Z'}}

```python
# 요청 인자의 칸을 적은 TS 선언과, 그 안의 칸 authorization이 적힌 줄을 찾습니다
print_lines_with(ts_lines, "export interface")
print_lines_with(ts_lines, "authorization?:")
```

출력:
```
줄 번호 | 줄
37 | export interface ChatStreamV1ChatStreamPostRequest {
52 | export interface ChatV1ChatPostRequest {
63 | export interface LiveChatStreamV1ChatLiveStreamPostRequest {
74 | export interface LiveChatV1ChatLivePostRequest {
줄 번호 | 줄
45 | authorization?: string | null;
60 | authorization?: string | null;
71 | authorization?: string | null;
82 | authorization?: string | null;

```

### [36] markdown {}

**결과 읽기** — 첫 라벨 줄 아래 네 줄은 요청 인자의 칸을 적은 TS 선언 `interface`입니다.
둘째 라벨 줄 아래 45·60·71·82행에서, 네 선언 모두 칸 `authorization?: string | null`을 가집니다.
칸 이름 뒤의 `?`는 넣지 않아도 되는 칸이라는 표시입니다.
실습 앱이 접근 토큰을 요청 머리 매개변수로 받아서, 생성 SDK도 요청마다 인자로 받습니다.
요청 주소 `/health`는 접근 토큰을 받지 않아, 요청 인자 선언이 없습니다.

다음 셀은 생성 SDK의 `models/ChatRequest.ts`에서 줄 넷을 찾습니다.
칸 이름의 줄, JSON 칸 이름으로 옮기는 두 줄, 글자 수 조건의 줄입니다.

### [37] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.835421Z', 'iopub.status.busy': '2026-09-29T10:49:45.835378Z', 'iopub.status.idle': '2026-09-29T10:49:45.837640Z', 'shell.execute_reply': '2026-09-29T10:49:45.837349Z'}}

```python
# models/ChatRequest.ts에서 칸 이름의 줄, JSON 칸 이름으로 옮기는 줄, 글자 수 조건의 줄을 찾습니다
with open("client/generated/models/ChatRequest.ts", encoding="utf-8") as model_file:
    model_lines = model_file.read().splitlines()
print_lines_with(model_lines, ": string;")
print_lines_with(model_lines, "json['thread_id']")
print_lines_with(model_lines, "value['threadId']")
print_lines_with(model_lines, "Length")
```

출력:
```
줄 번호 | 줄
25 | question: string;
29 | threadId: string;
줄 번호 | 줄
52 | 'threadId': json['thread_id'],
줄 번호 | 줄
68 | 'thread_id': value['threadId'],
줄 번호 | 줄

```

### [38] markdown {}

**결과 읽기** — 첫 라벨 줄 아래 25행과 29행이 입력 형식 `ChatRequest`의 두 칸입니다.
응답 문서의 칸 이름 `thread_id`가 TS 쪽에서는 `threadId`로 바뀌었습니다.
52행은 받은 JSON의 `thread_id`를 `threadId`로 옮기고, 68행은 보낼 때 다시 `thread_id`로 적습니다.
마지막 라벨 줄 아래에는 아무 줄도 없습니다.

생성기 문서는 칸 이름을 바꾸는 설정의 기본값이 낙타 등 모양 이름(camelCase)이라고 적습니다.
TS 형식에는 칸 이름과 글이라는 형식만 있고, 글자 수 조건은 없습니다.
그 조건은 서버의 입력 형식 검사가 맡아, 어기면 422로 답합니다.

## 5. 실험: 인증을 적는 자리 바꾸기

07절에서는 `HTTPBearer`를 쓴 새 앱의 응답 문서에만 보안 방식 칸이 있었습니다.
그런데 07절의 두 앱은 처리 함수와 요청 주소, 요청 방식도 서로 달랐습니다.
보안 방식 칸이 인증을 적는 방법 때문에 생겼는지 보려면, 다른 것은 같게 두고 그 하나만 바꿔야 합니다.
이 실험은 새 앱 객체 둘에 같은 처리 함수 `health`를 같은 요청 주소로 잇습니다.
바꿀 값은 의존성으로 적는 것 하나입니다.

인자 `dependencies`는 처리 함수의 매개변수로 받지 않을 의존성을 적는 자리입니다.
FastAPI 문서는 여기에 적은 의존성도 보통 의존성처럼 실행되고, 오류로 멈출 수 있다고 적습니다.
메서드 `add_api_route`는 05절에서 본, 처리 함수를 요청 방식과 요청 주소에 잇는 메서드입니다.

**가설** — 07절의 결과대로라면, 실행 2에만 보안 방식 칸 `securitySchemes`가 생길 것입니다.
실행 1은 실습 앱처럼, 매개변수 `authorization`이 요청 머리 자리로 적힐 것입니다.
머리 없는 요청은 두 실행 모두 401을 받을 것입니다.

**실행 1** — 다음 셀은 실습 앱의 제공 함수 `require_token`을 의존성으로 적습니다.
실행 전에 예상해 봅니다.
응답 코드 목록에 422가 있을까요?

### [39] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.838177Z', 'iopub.status.busy': '2026-09-29T10:49:45.838132Z', 'iopub.status.idle': '2026-09-29T10:49:45.841361Z', 'shell.execute_reply': '2026-09-29T10:49:45.841018Z'}}

```python
# 실행 1: 실습 앱의 제공 함수 require_token을 의존성으로 적어, 처리 함수 health를 새 앱 객체에 잇습니다
header_app = FastAPI()
header_app.add_api_route("/v1/ping", health, methods=["GET"], dependencies=[Depends(require_token)])
header_doc = header_app.openapi()
header_operation = header_doc["paths"]["/v1/ping"]["get"]
print("보안 방식 칸이 있는가:", "securitySchemes" in header_doc["components"])
print("요청 주소에 적힌 칸:", list(header_operation))
print("매개변수 이름과 자리:", header_operation["parameters"][0]["name"], header_operation["parameters"][0]["in"])
print("응답 코드:", list(header_operation["responses"]))
```

출력:
```
보안 방식 칸이 있는가: False
요청 주소에 적힌 칸: ['summary', 'operationId', 'parameters', 'responses']
매개변수 이름과 자리: authorization header
응답 코드: ['200', '422']

```

### [40] markdown {}

**결과 읽기** — 출력 줄 `보안 방식 칸이 있는가: False`와 `응답 코드: ['200', '422']`가 보입니다.
제공 함수의 매개변수 `authorization`이 요청 주소의 매개변수로 적혔습니다.
매개변수가 있으니, 그 값이 맞지 않을 때의 422 응답도 함께 적혔습니다.
설치판 fastapi `openapi/utils.py` 457~470행이 매개변수나 요청 본문이 있을 때만 422를 적습니다.

**실행 2** — 다음 셀은 값 하나만 바꿔, 의존성에 보안 객체를 적습니다.
보안 객체 `bearer`는 07절처럼 `HTTPBearer()`로 만듭니다.
요청 주소와 요청 방식, 처리 함수는 실행 1과 같습니다.
실행 전에 예상해 봅니다.
요청 주소에 적힌 칸은 어떻게 바뀔까요?

### [41] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.841855Z', 'iopub.status.busy': '2026-09-29T10:49:45.841812Z', 'iopub.status.idle': '2026-09-29T10:49:45.844716Z', 'shell.execute_reply': '2026-09-29T10:49:45.844387Z'}}

```python
# 실행 2: 값 하나만 바꿔, 의존성에 보안 객체를 적고 같은 처리 함수를 같은 요청 주소에 잇습니다
bearer = HTTPBearer()
bearer_app = FastAPI()
bearer_app.add_api_route("/v1/ping", health, methods=["GET"], dependencies=[Depends(bearer)])
bearer_doc = bearer_app.openapi()
bearer_operation = bearer_doc["paths"]["/v1/ping"]["get"]
print("보안 방식 칸이 있는가:", "securitySchemes" in bearer_doc["components"])
print("요청 주소에 적힌 칸:", list(bearer_operation))
print("보안 방식:", bearer_doc["components"]["securitySchemes"])
print("요청 주소의 security 칸:", bearer_operation["security"])
print("응답 코드:", list(bearer_operation["responses"]))
```

출력:
```
보안 방식 칸이 있는가: True
요청 주소에 적힌 칸: ['summary', 'operationId', 'responses', 'security']
보안 방식: {'HTTPBearer': {'type': 'http', 'scheme': 'bearer'}}
요청 주소의 security 칸: [{'HTTPBearer': []}]
응답 코드: ['200']

```

### [42] markdown {}

**결과 읽기** — 출력 줄 `보안 방식 칸이 있는가: True`와 `응답 코드: ['200']`이 보입니다.
칸 `components`에 보안 방식 `HTTPBearer`가 생겼고, 요청 주소에는 칸 `security`가 생겼습니다.
칸 `parameters`는 없어졌고, 매개변수가 없으니 422도 적히지 않았습니다.
설치판 `openapi/utils.py` 289~296행이 보안 객체를 찾아 칸 `security`를 적습니다.
같은 파일 573~575행은 찾은 보안 방식을 칸 `components`에 모읍니다.

다음 셀은 두 앱 객체에 요청을 보내, 상태 코드도 견줍니다.
머리 없는 요청과, 교재용 접근 토큰을 실은 요청입니다.

### [43] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.845207Z', 'iopub.status.busy': '2026-09-29T10:49:45.845168Z', 'iopub.status.idle': '2026-09-29T10:49:45.850693Z', 'shell.execute_reply': '2026-09-29T10:49:45.850355Z'}}

```python
# 두 앱 객체에 머리 없는 요청과 교재용 접근 토큰을 실은 요청을 보내, 상태 코드를 봅니다
auth_headers = {"Authorization": "Bearer local-demo-token"}
header_client = TestClient(header_app)
bearer_client = TestClient(bearer_app)
header_plain = header_client.get("/v1/ping")
header_token = header_client.get("/v1/ping", headers=auth_headers)
bearer_plain = bearer_client.get("/v1/ping")
bearer_token = bearer_client.get("/v1/ping", headers=auth_headers)
print("실행 1:", header_plain.status_code, header_plain.json(), header_token.status_code)
print("실행 2:", bearer_plain.status_code, bearer_plain.json(), bearer_token.status_code)
```

출력:
```
실행 1: 401 {'detail': '인증 정보가 올바르지 않습니다'} 200
실행 2: 401 {'detail': 'Not authenticated'} 200

```

### [44] markdown {}

**결과 읽기** — 두 줄 모두 머리 없는 요청은 `401`, 교재용 접근 토큰을 실은 요청은 `200`입니다.
상태 코드는 같았고, 401 응답 본문의 글만 달랐습니다.
07절에서 본 것처럼 실행 2의 보안 객체는 접근 토큰 글을 견주지 않습니다.
이 셀에서는 틀린 글을 보내지 않아, 그 차이는 보지 않았습니다.

다음 셀은 두 실행을 한 표로 모읍니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-29T10:49:45.851224Z', 'iopub.status.busy': '2026-09-29T10:49:45.851175Z', 'iopub.status.idle': '2026-09-29T10:49:45.853386Z', 'shell.execute_reply': '2026-09-29T10:49:45.852998Z'}}

```python
# 두 실행의 의존성·응답 문서의 칸·상태 코드를 한 표로 모읍니다
print("견준 것 | 실행 1 | 실행 2")
print("의존성에 적은 것 | require_token | HTTPBearer()")
print("보안 방식 칸 |", "securitySchemes" in header_doc["components"], "|", "securitySchemes" in bearer_doc["components"])
print("security 칸 |", "security" in header_operation, "|", "security" in bearer_operation)
print("parameters 칸 |", "parameters" in header_operation, "|", "parameters" in bearer_operation)
print("응답 코드 |", list(header_operation["responses"]), "|", list(bearer_operation["responses"]))
print("머리 없는 요청 |", header_plain.status_code, "|", bearer_plain.status_code)
print("교재용 접근 토큰 |", header_token.status_code, "|", bearer_token.status_code)
```

출력:
```
견준 것 | 실행 1 | 실행 2
의존성에 적은 것 | require_token | HTTPBearer()
보안 방식 칸 | False | True
security 칸 | False | True
parameters 칸 | True | False
응답 코드 | ['200', '422'] | ['200']
머리 없는 요청 | 401 | 401
교재용 접근 토큰 | 200 | 200

```

### [46] markdown {}

**결과 읽기** — 라벨 줄 아래 일곱 줄이 두 실행을 견줍니다.
줄 `보안 방식 칸 | False | True`와 `security 칸 | False | True`가 보입니다.
줄 `parameters 칸 | True | False`에서, 매개변수 칸은 실행 1에만 있습니다.
상태 코드 두 줄은 `머리 없는 요청 | 401 | 401`과 `교재용 접근 토큰 | 200 | 200`으로 같습니다.

**결론** — 바꾼 값은 인자 `dependencies`에 적은 것 하나였습니다.
두 요청의 상태 코드는 같았지만, 응답 문서는 달랐습니다.
보안 객체를 적은 실행 2에만 보안 방식 칸과 칸 `security`가 생겼습니다.
실습 앱은 실행 1 모양이라, 4절의 생성 SDK도 접근 토큰을 요청마다 인자로 받았습니다.
이 노트북은 걸린 시간을 재지 않았고, 응답 문서의 칸과 상태 코드만 확인했습니다.

## 정리

1. 메서드 `openapi`가 내놓은 응답 문서는 실습 폴더 `openapi.json`과 글이 같았습니다.
2. 생성 SDK에서 SSE 사건으로 답하는 요청 주소 둘의 함수는 `Promise<void>`를 내놓았습니다.
3. 의존성 하나만 보안 객체로 바꾸자, 상태 코드는 같은데 응답 문서에 보안 방식 칸이 생겼습니다.

09절에서는 실제로 모델을 부르는 에이전트를 요청 주소 `/v1/chat/live`로 부릅니다.

## 그림

### 08-1-앱-객체에서-생성-SDK까지.mmd

```mermaid
flowchart TB
  %% classes
  app["실습 앱 객체 app<br>처리 함수 다섯"]:::tool
  lib["FastAPI가 처리 함수와<br>양식 클래스를 훑어 적음"]
  doc["응답 문서 딕셔너리<br>OpenAPI 3.1.0<br>요청 주소 다섯"]:::measure
  file["실습 폴더 openapi.json<br>새로 만든 글과 같음 True"]:::measure
  gen["생성기 7.25.0<br>typescript-fetch<br>노트북 밖 README 명령"]
  sdk["생성 SDK<br>client/generated<br>요청 주소마다 함수 하나"]:::tool
  app --> lib --> doc --> file --> gen --> sdk
```

앱 객체가 만든 응답 문서는 실습 폴더의 openapi.json과 같았고, 생성 SDK는 그 문서로 노트북 밖에서 만든 코드입니다.

### 08-2-요청-주소-v1-chat의-칸.mmd

```mermaid
flowchart TB
  %% classes
  op["POST /v1/chat<br>operationId<br>chat_v1_chat_post"]:::tool
  body["요청 본문 형식<br>ChatRequest를<br>가리킴"]:::measure
  ok["200 응답 형식<br>ChatResponse를<br>가리킴"]:::measure
  bad["422 응답<br>입력 형식 검사"]:::measure
  param["매개변수<br>authorization<br>자리 header"]:::measure
  comp["components의<br>ChatRequest<br>꼭 채울 칸 둘<br>question 1자 이상<br>500자 이하"]:::measure
  op --> body
  op --> ok
  op --> bad
  op --> param
  body --> comp
```

요청 주소 /v1/chat의 칸은 요청 본문과 200 응답의 형식을 components 쪽 자리로 가리켰고, 가리킨 ChatRequest에 글자 수 조건이 적혀 있었습니다.

### 08-3-요청-주소와-생성-함수.mmd

```mermaid
flowchart TB
  %% classes
  jsonpath["JSON 요청 주소 셋<br>본문 종류 아래 schema"]:::measure
  ssepath["SSE 요청 주소 둘<br>본문 종류 아래 itemSchema"]:::measure
  gen["생성기 typescript-fetch<br>노트북 밖"]
  fjson["함수 셋<br>ChatResponse나<br>HealthResponse를<br>내놓는 Promise"]:::measure
  fsse["함수 둘<br>void를 내놓는 Promise<br>응답 본문을 읽지 않음"]:::measure
  ts["SSE 사건은<br>손으로 쓴 client/stream.ts가<br>fetch로 읽음"]:::tool
  jsonpath --> gen
  ssepath --> gen
  gen --> fjson
  gen --> fsse
  fsse -.-> ts
```

JSON 요청 주소 셋의 함수는 응답 형식을 내놓았고, SSE 요청 주소 둘의 함수는 void를 내놓아 SSE 사건은 손으로 쓴 TS 파일이 읽습니다.

### 08-4-의존성-하나만-바꾼-두-응답-문서.mmd

```mermaid
flowchart TB
  %% classes
  same["같은 처리 함수 health<br>GET /v1/ping<br>새 앱 객체"]:::flow
  subgraph r1["실행 1 · 제공 함수"]
    direction TB
    a1["dependencies에<br>require_token"]:::tool
    a2["보안 방식 칸 False<br>매개변수 authorization<br>응답 코드 200·422"]:::measure
    a1 --> a2
  end
  subgraph r2["실행 2 · 보안 객체"]
    direction TB
    b1["dependencies에<br>HTTPBearer 객체"]:::flow
    b2["보안 방식 칸 True<br>security 칸 HTTPBearer<br>응답 코드 200"]:::measure
    b1 --> b2
  end
  both["두 실행 모두<br>머리 없음 401<br>교재용 접근 토큰 200"]
  same --> r1
  same --> r2
  r1 --> both
  r2 --> both
```

의존성 하나만 보안 객체로 바꾸자, 상태 코드는 같았는데 응답 문서에 보안 방식 칸과 security 칸이 생겼습니다.

### 08-5-모형을-보고-만든-화물-칸.prompt.md

# 08-5-모형을-보고-만든-화물-칸 (Higgsfield 삽화)

설명 대상 문장(본문 b4 비유 단락): 차량 공장은 새 화물 열차를 만들기 전에, 탁자 위에 작은 축소 모형부터 받습니다. 모형에는 칸 다섯이 차례대로 놓여 있고, 칸마다 색이 칠해져 있습니다. 공장은 모형만 보고 실제 칸을 만들고, 한 가지 색으로 칠한 칸은 벽과 지붕까지 갖춘 칸으로 만듭니다. 줄무늬만 그린 칸은 공장이 모르는 표시라서, 바닥만 있는 빈 칸으로 둡니다. … 축소 모형이 응답 문서이고, 모형의 칸 하나가 요청 주소 하나입니다. 공장은 생성기이고, 공장이 만든 실제 칸이 생성 SDK의 함수입니다.

구성 요소와 배치: 앞쪽 **나무 탁자** 위 **축소 모형 칸 다섯**(= 응답 문서의 요청 주소 다섯 — 노트북 셀 [6] `요청 주소 수: 5`) — 앞 셋 **올리브색 단색**(= JSON 요청 주소 셋, 키 `schema`), 뒤 둘 **흰색·회색 빗금 줄무늬**(= SSE 요청 주소 둘, 키 `itemSchema` — 셀 [9]) · 탁자 뒤 선로 위 **실제 화물 칸 다섯**(= 생성 SDK 함수 다섯 — 셀 [15]) 같은 차례 — 앞 셋 **벽과 지붕이 있는 올리브색 덮개 칸**(= 형식을 내놓는 함수 셋), 뒤 둘 **바닥과 바퀴만 있는 빈 평판 칸**(= `Promise<void>` 둘). 공장(생성기)은 그리지 않음. 비유 계열 「화물 열차와 번호판 차량」의 「편성도」 후보를 종이 대신 **축소 모형**으로(종이·판은 글자·표지판이 들기 쉬움). 01~07 소품(창고·파란 규격 틀·흰 차단봉·빈 화차 / 주황·파란 기관차·초록 짐칸·세 줄 선로 / 짙은 회색 기관차·갈색 뚜껑 없는 짐칸·노란 손수레·나무 상자·꾸러미 더미·멈춤 막이 / 짙은 빨강 기관차·옅은 회색 평판 짐칸·청록 통·겨자색 끝 칸·콘크리트 짐 내리는 자리 / 하늘색 닫힌 짐칸·짙은 초록 네모 판·흰 동그라미 번호판·연한 주황 끝 칸·짙은 갈색 네모 판·자갈 비스듬한 구도 / 크림색 짐칸·검은 세모 판·분홍 끝 칸·두 줄 선로·회색 지붕 / 은색 짐칸·노란·파란 트럭·흰 천 자루·노란 꼬리표·색 번호판) 되풀이 안 함. 금지 소품(오르골·종이띠·도킹 포트·정거장·우주선·온실·모종판·예인선·바지선·밧줄·홈통·물방울·도미노·체스판·즉석사진·세탁기·승강 상자·전표·가마·물레·발자국·말뚝·쟁반·서랍·바구니·저울·도장·개찰구·플러그·공항 검사·안내 데스크·주문표·창구·택배·출입구) 없음. 사람·손·글자·숫자·화살표·표지판·화면·건물·승강장·기관차 없음.

시선 순서: 탁자 위 모형(단색 셋 → 줄무늬 둘) → 뒤쪽 실제 칸(덮개 칸 셋 → 빈 칸 둘).

검수 기준: 그림만 보고 「모형의 단색 칸은 벽과 지붕이 있는 실제 칸이 되었고, 줄무늬 칸은 바닥만 있는 빈 칸이 되었다」가 읽히는가. 모형 칸 다섯·실제 칸 다섯, 셋과 둘을 셀 수 있는가. 차례가 같은가. 사람·글자·숫자·화살표 없음. 흰 여백이 크지 않은가.

## 프롬프트 (1차, 채택)

```text
Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos. Close elevated three-quarter view, objects drawn large to fill the frame. In the foreground, a small light-wood tabletop holds a tiny scale model train of exactly five small cars in one row: the first three cars are painted solid olive green, the last two cars are painted with white and gray diagonal stripes. Directly behind the table, on a railway track, a full-size freight train of exactly five cars in the same order: the first three are olive green covered hopper cars with walls and roofs, the last two are bare empty flatcars with only a floor and wheels and nothing on them. No locomotive, no people, no hands, no arrows, no signs, no buildings, no platforms, no screens.
```

## 상태

- 2026-09-29 · `generate_image` 한 번(재생성 0), `params` = `{"model":"nano_banana_pro","prompt":…,"aspect_ratio":"16:9","resolution":"2k","use_unlim":false,"count":1}`. `generate_image` 응답 모델 `nano_banana_pro`, **`jobs_wait` 응답 모델 표시 `nano_banana_2`**(01~07과 같은 표시, 거래 표시는 「Nano Banana Pro」 — 기록만). 서비스 쪽 실패 0.
- 생성 전 잔액 **2275**(`balance`), 바로 앞 거래 2026-09-29T10:15:02.663841Z는 Ch 30 07절 몫.
- **1차 job `ee589176-cd27-4481-8d0e-a5ddede7df50`** — 거래 2026-09-29T10:52:17.842524Z 「Nano Banana Pro −2」(**이 절 몫 2크레딧**, 잔액 2275 → 2273). 원본 `311b5a7cce6416530b1cf4aba2a49c60d78dba8f86408188f4f8a5d11ba1dbd3`(2752 × 1536).
- **그림에서 확인한 것(그림 읽기·alt에 반영)**: 흰 바탕 · 앞쪽 연한 나무 탁자 위 모형 칸 **다섯**이 한 줄 — 왼쪽 **셋 올리브색**(닫힌 상자 모양 칸), 오른쪽 **둘 흰색·회색 빗금 줄무늬** · 탁자 뒤 왼쪽 위에서 오른쪽 아래로 비스듬한 선로 위 실제 화물 칸 **다섯** 같은 차례 — 왼쪽 **셋 올리브색 덮개 칸**(벽·지붕·호퍼 아래), 오른쪽 **둘 바닥과 바퀴만 있는 빈 평판 칸**(연한 크림색 바닥·올리브색 틀). 기관차·사람·손·글자·숫자·화살표·표지판·화면·건물·승강장 없음. 거의 흰 가로줄 **21줄 / 614줄**(07 109줄보다 적음 — 비스듬한 선로가 위쪽을 채움, 오른쪽 위·아래 모서리에 흰 바탕).
- **설계와 다른 점**: 모형 칸은 실제 칸(호퍼 모양)과 달리 닫힌 상자 모양 — 색·차례·개수로 짝이 읽혀 채택. 빈 평판 칸의 바닥은 올리브색이 아니라 크림색(값과 짝짓지 않음).
- 검수: 「모형의 단색 칸 셋은 벽과 지붕이 있는 실제 칸, 줄무늬 칸 둘은 바닥만 있는 빈 칸」이 그림만으로 읽힘 → 채택(재생성 한도 1회를 쓰지 않음).
- 저장: 기기 셸에서 결과 URL을 `curl`로 받아(`/tmp/ch30-08/illu/illu-1-orig.png`) `UV_CACHE_DIR=/tmp/uv-cache uv run --no-project --with pillow`로 RGB·폭 1100px(LANCZOS)로 줄여 `figures/08-5-모형을-보고-만든-화물-칸.png`(1100 × 614, `eca09ae9b8d5793697226a76a59602b12f47263d097f02666d437b569f45c631`)로 저장했습니다.
- 결과 URL을 한 번 더 받아(`illu-1-again.png`, 원본과 해시 같음) 같은 폭으로 줄인 그림과 저장 PNG를 픽셀 대조했습니다(`ImageChops.difference` bbox `None`, 최대 차이 0). 저장 PNG와 같은 보기 사본(`.cache/ch30-08-view/illu-1-1100.png` — bbox `None`)과 원본 위·아래 절반 확대 둘을 직접 열어 개수를 세고 그림 읽기를 썼습니다.

