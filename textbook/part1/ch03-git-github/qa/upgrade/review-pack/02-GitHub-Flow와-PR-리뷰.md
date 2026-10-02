# 02-GitHub-Flow와-PR-리뷰

## _src 본문 (HTML 원본)

```html
<!--meta: 강의 1h | 실습 2h | 코드 Jupyter Notebook | 새 용어 7 -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2>
<div class="goal"><ul><li>기능 브랜치에 커밋하고 원격 저장소에 올리는 순서를 명령 출력으로 설명할 수 있습니다.</li><li>리뷰할 변경 범위를 <code>git diff origin/main...HEAD</code>로 읽고, 다시 만들 수 있는 리뷰 의견을 적을 수 있습니다.</li><li>리뷰 의견을 반영한 커밋을 받아 와 main에 병합하고, 원격 main까지 같아졌는지 확인할 수 있습니다.</li></ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2>
<p>여러 사람이 한 저장소의 main에 바로 커밋하면, 아무도 확인하지 않은 코드가 모두의 출발점이 됩니다. 한 사람의 실수가 곧바로 팀 전체의 코드에 섞입니다.</p>
<p>그래서 팀은 새 작업을 따로 만든 브랜치에서 합니다. 다른 사람이 그 변경을 읽고 실행해 본 뒤에 main에 합칩니다. GitHub에서는 이 확인 과정을 PR 화면에서 합니다.</p>
<p>이 절은 GitHub 계정 없이 임시 폴더 안에서 같은 순서를 실행합니다. 원격 저장소 하나와 작성자·리뷰어 저장소 둘을 만들어 커밋을 주고받습니다.</p>
<p><strong>이 절의 질문</strong> — 기능 브랜치의 결함을 리뷰에서 찾았다면, 고친 결과가 팀의 main까지 들어갔는지 무엇으로 확인할까요?</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2>
<p>01절에서는 main 브랜치 하나에 커밋 다섯 개를 쌓았습니다. 명령 <code>git add</code>로 색인에 고르고 <code>git commit</code>으로 기록했습니다. 메시지 앞머리 <code>chore:</code>·<code>feat:</code>·<code>fix:</code>로 변경 목적을 적었고, <code>git diff</code>로 바뀐 줄을 읽었습니다.</p>
<p>작성자 정보는 <code>git config</code>로 연습 저장소에만 적었습니다. 그때 이름은 <code>Ch3 Student</code>였고, 이번 리뷰어는 같은 규칙으로 <code>Ch3 Reviewer</code>를 씁니다. 무시 규칙 파일 <code>.gitignore</code>의 <code>__pycache__/</code> 줄도 이어 씁니다.</p>
<p>git 명령은 01절의 함수 <code>run_git()</code>으로 실행합니다. 이번에는 Ch 2 04절의 기본값 매개변수로 폴더 이름 <code>folder</code>를 더합니다. 명령을 실행할 폴더는 Ch 1 05절에서 쓴 인자 <code>cwd</code>로 정합니다.</p>
<p>주문 요약 함수는 Ch 2 04절의 함수 정의와 07절의 타입힌트로 씁니다. 리뷰어의 확인 파일에는 Ch 2 07절의 <code>from … import</code> 문과 05절의 <code>try</code>·<code>except ValueError</code>가 들어갑니다. 확인 파일을 실행하는 함수는 Ch 2 08절 <code>run_pytest()</code>와 같은 모양입니다.</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2>
<h3>비유로 시작하기</h3>
<p>01절의 택배 상자를 이어 떠올립니다. 봉한 상자 하나가 커밋 하나였습니다. 이번에는 상자를 창고 선반에 올리는 팀을 생각합니다.</p>
<p>긴 선반에는 확인을 마친 상자만 올립니다. 새 상자는 먼저 옆 수레에 싣습니다. 동료가 검수대에서 상자를 열어 돋보기로 확인한 뒤에야 선반 끝에 올립니다.</p>
<p>저장소에서는 긴 선반이 main 브랜치, 수레가 기능 브랜치입니다. 검수대의 확인이 PR 리뷰이고, 선반에 올리는 일이 병합입니다.</p>
{{img:02-6-검수대와-선반|위쪽 긴 선반에 갈색 테이프 상자가 줄지어 있고, 아래에서는 수레의 파란 테이프 상자가 검수대에서 돋보기로 확인된 뒤 화살표를 따라 선반 끝에 올라간 삽화|새 상자는 수레에 먼저 싣고, 검수대에서 확인한 뒤 긴 선반에 올립니다. 기능 브랜치의 커밋을 리뷰한 뒤 main에 병합하는 모습과 같습니다.}}
<p><strong>그림 읽기</strong> — 아래 줄을 왼쪽에서 오른쪽으로 따라갑니다. 수레의 파란 테이프 상자가 검수대로 옮겨지고, 한 사람이 열린 상자를 돋보기로 봅니다. 오른쪽 화살표는 위쪽 긴 선반의 끝을 가리킵니다. 선반 끝의 파란 상자 두 개는 확인을 마치고 main에 합쳐진 커밋 두 개에 해당합니다.</p>
<h3>이 절에서 쓰는 말</h3>
<table><thead><tr><th>용어</th><th>뜻</th><th>이 절에서 보이는 모습</th></tr></thead><tbody>
<tr><td>원격 저장소(remote repository)</td><td>여러 사람이 커밋을 올리고 받아 오는 저장소. 복제한 저장소에는 이름 <code>origin</code>으로 적힙니다</td><td><code>team.git</code>, <code>git remote -v</code>의 <code>origin</code></td></tr>
<tr><td>bare 저장소</td><td>작업 폴더 없이 커밋 기록만 담는 저장소. 아무도 이 폴더에서 파일을 고치지 않습니다</td><td><code>git init --bare -b main team.git</code></td></tr>
<tr><td>브랜치(branch)</td><td>커밋이 이어지는 줄기의 이름. 줄기 끝의 커밋을 가리킵니다</td><td><code>main</code>, <code>feature/order-summary</code></td></tr>
<tr><td>기능 브랜치(feature branch)</td><td>기능 하나를 만들려고 main에서 갈라 낸 브랜치</td><td><code>git switch -c feature/order-summary</code></td></tr>
<tr><td>풀 리퀘스트(pull request, PR)</td><td>내 브랜치의 변경을 main에 합쳐 달라고 요청하는 GitHub 기능</td><td><code>git diff --stat origin/main...HEAD</code>와 PR 설명 글(화면은 만들지 않음)</td></tr>
<tr><td>코드 리뷰(code review)</td><td>작성자가 아닌 사람이 변경을 읽고 실행해 보며 문제를 찾는 일</td><td>확인 파일의 <code>빈 값: 주문 건</code>과 리뷰 의견</td></tr>
<tr><td>병합 커밋(merge commit)</td><td>두 줄기를 합치며 만든, 부모 커밋이 둘인 커밋</td><td><code>merge: 주문 요약</code></td></tr>
</tbody></table>
<h3>세 저장소가 주고받는 길</h3>
<p>이 절에는 저장소가 세 개 있습니다. 가운데 <code>team.git</code>은 팀이 함께 쓰는 원격 저장소로, GitHub 서버의 저장소 자리에 있습니다. 작성자와 리뷰어는 각자 원격 저장소를 복제해 자기 폴더에서 일합니다.</p>
<p>명령 <code>git push</code>는 내 커밋을 원격 저장소로 올립니다. 명령 <code>git fetch</code>는 원격 저장소의 새 커밋을 받아 옵니다. 두 사람은 서로 직접 주고받지 않고, 늘 원격 저장소를 거칩니다.</p>
{{mermaid:02-1-세-저장소|위 가운데 원격 저장소 team.git에서 아래 왼쪽 작성자 폴더와 아래 오른쪽 리뷰어 폴더로 clone과 fetch 화살표가 내려가고, 두 폴더에서 push 화살표가 올라가는 흐름도|세 저장소가 커밋을 주고받는 길. 작성자와 리뷰어는 가운데 원격 저장소를 거쳐서만 커밋을 주고받습니다.}}
<p><strong>도식 읽기</strong> — 위 가운데 상자가 원격 저장소, 아래 왼쪽이 작성자, 아래 오른쪽이 리뷰어의 저장소입니다. 세 상자 모두 저장소라서 초록입니다. 아래로 가는 화살표는 받아 오는 명령, 위로 가는 화살표는 올리는 명령입니다.</p>
<p>작성자는 기능 브랜치 <code>feature/order-summary</code>를 올리고, 리뷰어는 그 커밋을 <code>git clone</code>과 <code>git fetch</code>로 받습니다. 병합을 마친 리뷰어가 <code>git push origin main</code>으로 main을 올립니다.</p>
<h3>GitHub Flow 순서</h3>
<p>작업 방식 GitHub Flow는 main을 늘 동작하는 상태로 두는 방식입니다. GitHub 문서의 순서는 여섯 단계입니다.</p>
<ol><li>기능 브랜치를 main에서 만듭니다.</li><li>기능 브랜치에 커밋하고 원격에 올립니다.</li><li>풀 리퀘스트(PR)를 열어 변경 범위와 설명을 보여 줍니다.</li><li>리뷰 의견이 있으면 같은 브랜치에 고친 커밋을 더 올립니다.</li><li>리뷰를 마친 브랜치를 main에 병합합니다.</li><li>병합을 마친 기능 브랜치를 지웁니다.</li></ol>
<p>이 노트북은 3번의 PR 화면을 만들지 않습니다. 대신 PR 화면에 나올 변경 범위와 설명 글을 명령과 파일로 만듭니다. 5번의 병합도 GitHub 버튼 대신 리뷰어가 명령으로 합니다. 6번 브랜치 지우기는 이번에 실행하지 않았습니다.</p>
<p>PR 설명 양식은 저장소의 <code>pull_request_template.md</code> 파일에 둡니다. GitHub 문서에 따르면 이 파일이 기본 브랜치에 있어야 PR 설명 칸에 채워집니다. 그래서 노트북은 이 파일을 main의 첫 커밋에 넣었습니다.</p>
<h3>점 세 개 비교</h3>
<p>PR 화면의 바뀐 파일 목록은 main과 기능 브랜치의 차이입니다. 노트북에서는 명령 <code>git diff origin/main...HEAD</code>로 같은 범위를 봅니다.</p>
<p>이름 <code>origin/main</code>은 내 저장소가 마지막으로 확인한 원격 main의 위치입니다. 점 세 개 <code>...</code>는 두 브랜치가 갈라진 커밋 뒤로 지금 브랜치에 더해진 변경만 보라는 뜻입니다. 이번 실행에서는 그 사이에 main이 움직이지 않았습니다. 원격 main이 먼저 앞으로 간 경우는 실행하지 않았습니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2>
<p>노트북은 원격 저장소 <code>team.git</code>을 만들고, 작성자가 복제해 main에 첫 커밋을 올립니다. 첫 커밋에는 무시 규칙 파일과 PR 템플릿 파일이 들어갑니다. 그다음 기능 브랜치에 주문 요약 함수를 커밋해 원격에 올립니다. 끝으로 PR로 볼 범위와 설명 글을 만듭니다.</p>
<p>함수 <code>run_git()</code>은 01절 모양에 폴더 이름을 더했습니다. 출력 첫 줄의 <code>author $</code>나 <code>reviewer $</code>를 보면 어느 저장소의 명령인지 알 수 있습니다. 커밋 번호와 임시 폴더 경로는 실행할 때마다 달라지므로, 커밋 메시지와 브랜치 이름을 봅니다.</p>
<p>마지막으로 리뷰어가 원격 저장소를 복제합니다. 값 하나 바꿔 보기에서는 리뷰어 폴더의 브랜치만 main에서 기능 브랜치로 바꿔 파일 목록을 비교합니다. 모델을 부르지 않으므로 API 키가 필요 없고 비용도 들지 않습니다.</p>
<p>강의 시간에는 6~8번과 11~12번 소제목을 설명합니다. 6~8번은 기능 브랜치·올리기·PR 범위이고, 11~12번은 리뷰와 병합입니다. 1~5번과 9~10번은 셀을 함께 실행하고, 결과 읽기는 실습 시간에 이어서 읽습니다.</p>
{{notebook:02-GitHub-Flow와-PR-리뷰|example}}
<p class="look"><b>확인할 점</b> — 기능 커밋 뒤 <code>git branch -v</code>에서 기능 브랜치만 새 커밋을 가리키는지 봅니다. 리뷰어 폴더의 파일 목록에 <code>summary.py</code>가 브랜치를 옮긴 뒤에만 나오는지도 확인합니다.</p>
<h3>기능 브랜치만 앞으로 옮겨 갑니다</h3>
<p>브랜치는 폴더를 통째로 복사한 것이 아닙니다. 줄기 끝의 커밋을 가리키는 이름입니다. 새 커밋을 만들면 지금 있는 브랜치의 이름만 그 커밋으로 옮겨 갑니다.</p>
{{mermaid:02-2-브랜치-두-줄기|작성자 저장소 칸 안에 chore 커밋에서 feat 커밋으로 이어지는 초록 상자 두 개가 있고, 회색 main 이름은 chore 커밋을, 회색 feature/order-summary 이름은 feat 커밋을 점선으로 가리키는 그림|기능 브랜치를 원격에 올린 뒤의 브랜치 이름. 새 커밋으로 옮겨 간 이름은 지금 있는 기능 브랜치뿐입니다.}}
<p><strong>도식 읽기</strong> — 테두리 칸 안의 초록 상자 두 개가 작성자 저장소의 커밋이고, 위에서 아래로 만든 순서입니다. 회색 상자는 브랜치 이름이고, 점선은 그 이름이 가리키는 커밋으로 이어집니다.</p>
<p>위의 <code>main</code> 이름은 첫 커밋 <code>chore: 저장소와 PR 템플릿 시작</code>에 남았습니다. 오른쪽 <code>* feature/order-summary</code> 이름은 새 커밋 <code>feat: 주문 요약 함수 추가</code>를 가리킵니다. 별표는 지금 있는 브랜치 표시이고, 짝은 <code>git branch -vv</code>의 대괄호 속 이름입니다.</p>
<h2 id="b6"><span class="no">6</span>일부러 실패해 보기</h2>
<p>Before에서는 리뷰어가 기능 브랜치의 첫 함수를 읽고 실행합니다. 확인 파일은 함수에 보통 값 3과 빈 글자를 넣습니다. 타입힌트 <code>int</code>는 Ch 2 07절에서 본 것처럼 값을 검사하지 않습니다.</p>
<p>After에서는 작성자가 Ch 2 01절의 형 변환 <code>int()</code>로 건수를 바꾸도록 고칩니다. 고친 커밋을 같은 기능 브랜치에 올리고, 리뷰어가 받아 와 main에 병합합니다. 확인 파일과 넣는 값은 Before와 같습니다. 함수 <code>int()</code>는 숫자 모양 글 <code>"3"</code>도 정수 3으로 바꾸므로, 고친 함수는 그런 글도 받습니다. 이 경우는 이번에 실행하지 않았습니다.</p>
{{notebook:02-GitHub-Flow와-PR-리뷰|failure}}
<p>기능 브랜치에서 실행한 확인 파일은 오류 없이 <code>빈 값: 주문 건</code>을 출력했습니다. 건수가 빠진 틀린 글이 조용히 만들어졌습니다. PR 설명의 빈 값 확인 칸이 비어 있어서 리뷰어가 직접 실행해 찾은 결함입니다.</p>
<p>리뷰 의견에는 넣은 값, 실제 결과, 기대하는 동작을 함께 적었습니다. 「빈 글자를 넣으면 오류 없이 <code>주문 건</code>이 나옵니다. 숫자로 바꿀 수 없는 값은 오류로 알려 주세요.」 GitHub 화면에 의견을 적는 장면은 이번에 실행하지 않았습니다.</p>
<p>병합한 main에서는 같은 확인 파일이 <code>입력 오류: invalid literal for int() with base 10: ''</code>를 출력했습니다. 함수 안의 <code>int()</code>가 낸 <code>ValueError</code>를 확인 파일의 <code>except</code> 블록이 받아 출력했습니다. 보통 값은 두 번 모두 <code>보통 값 3: 주문 3건</code>이었습니다.</p>
<p>틀린 값을 빈 결과로 감추지 않고 오류로 드러내는 방법은 Ch 2 05절의 결론과 같습니다. 오류 글도 Ch 2 13절 실습에서 「많이」를 정수로 바꿀 때 본 모양과 같습니다.</p>
{{mermaid:02-4-확인-결과-비교|Before 칸은 summary.py, 확인 파일 실행, 빨간 빈 값 주문 건 결과로 이어지고, After 칸은 int(count)로 고친 summary.py, 같은 확인 파일 실행, 노란 입력 오류 결과로 이어지는 비교 그림|같은 확인 파일의 결과. 기능 브랜치의 첫 함수는 틀린 글을 조용히 만들었고, 병합한 main의 함수는 오류를 드러냈습니다.}}
<p><strong>도식 읽기</strong> — 위 칸이 Before, 아래 칸이 After이고, 칸마다 왼쪽에서 오른쪽으로 읽습니다. 초록 상자는 함수 파일, 파란 상자는 우리가 실행한 확인입니다.</p>
<p>위 칸 끝의 빨간 상자는 오류 없이 나온 틀린 글 <code>빈 값: 주문 건</code>입니다. 아래 칸 끝의 노란 상자는 확인 파일이 받아서 출력한 오류입니다. 프로그램을 멈추지 않고 출력한 오류라서 노랑으로 칠했습니다. 두 칸 사이 화살표 위 글자는 결과를 바꾼 일입니다.</p>
<h3>리뷰에서 병합까지 실제 순서</h3>
<p>두 확인 사이에 세 저장소는 커밋을 여러 번 주고받았습니다. 리뷰어는 병합 결과를 확인한 뒤에 main을 올렸습니다.</p>
{{mermaid:02-3-주고받는-순서|작성자, 원격 team.git, 리뷰어 세로줄 사이로 push, clone, fetch 화살표가 위에서 아래로 이어지고, 리뷰어 줄에 확인 파일 실행 메모 두 개가 있는 순서도|리뷰에서 병합까지 실제 순서. 리뷰어는 병합한 main을 확인한 뒤에 원격에 올렸습니다.}}
<p><strong>도식 읽기</strong> — 위에서 아래로 시간 순서입니다. 세로줄 셋은 왼쪽부터 작성자, 원격, 리뷰어의 저장소입니다. 실선 화살표는 요청한 명령, 점선 화살표는 받아 온 결과입니다. 노란 메모는 리뷰어 저장소에서 확인 파일을 실행한 시점입니다.</p>
<p>작성자가 고친 커밋을 올린 뒤, 리뷰어가 받아 온 기능 브랜치의 짝 표시는 <code>behind 1</code>이었습니다. 병합과 확인을 마친 main의 짝 표시는 <code>ahead 3</code>이었습니다. 명령 <code>git push origin main</code> 뒤에는 이 표시가 사라졌습니다. 마지막 화살표에서 작성자도 <code>git fetch</code>로 <code>merge: 주문 요약</code>을 받았습니다.</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2>
<ul><li>이 노트북은 네트워크와 GitHub 계정 없이 임시 폴더의 원격 저장소로 실행했습니다. 실제 PR 화면, 리뷰 승인, 병합 버튼은 이번에 실행하지 않았습니다.</li>
<li>PR 설명의 확인 칸은 실행을 대신하지 않습니다. 어떤 값을 넣어 무엇을 봤는지 함께 적습니다.</li>
<li>리뷰 의견은 사람보다 코드를 향해 씁니다. 넣은 값, 실제 결과, 기대하는 동작을 적으면 작성자가 같은 결과를 다시 만들 수 있습니다.</li>
<li>명령 <code>git fetch</code>는 <code>origin/</code>으로 시작하는 이름만 옮기고 내 브랜치는 그대로 둡니다. 받아 온 뒤 <code>git branch -vv</code>의 <code>behind</code>·<code>ahead</code> 표시로 짝과 비교합니다.</li>
<li>병합 방법은 저장소마다 정합니다. 이 절은 병합 커밋을 남기는 <code>--no-ff</code>만 실행했습니다. 다른 방법인 fast-forward·squash·rebase 병합은 실행하지 않았습니다.</li>
<li>병합을 마친 기능 브랜치는 지워서 끝난 작업임을 알립니다. 브랜치를 지워도 병합한 커밋 기록은 남는다고 GitHub 문서에 적혀 있습니다. 이 장면은 실행하지 않았습니다.</li>
<li>교재 출력은 Linux의 Git 2.34.1에서 실행한 결과입니다. 다른 운영체제인 Windows와 macOS에서는 실행하지 않았습니다. 확인 파일을 실행하는 함수의 <code>text=True</code> 글자 규칙도 다른 운영체제에서는 확인하지 않았습니다.</li></ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2>
<ul><li>새 작업은 기능 브랜치에 커밋하고, <code>git push</code>로 원격 저장소에 올립니다. 새 커밋으로 옮겨 가는 이름은 지금 있는 브랜치 하나입니다.</li><li>PR에서는 <code>git diff origin/main...HEAD</code>로 변경 범위를 읽고, 리뷰어가 직접 실행해 결함을 찾습니다.</li><li>고친 커밋은 같은 브랜치에 올립니다. 리뷰어는 <code>git fetch</code> 뒤 main에 병합하고, 확인한 다음 원격까지 올립니다.</li></ul>
{{mermaid:02-5-병합-이력|아래 chore 커밋에서 왼쪽 main 줄기는 바로 위 merge 커밋으로, 오른쪽 기능 브랜치 줄기는 feat와 fix 커밋을 거쳐 merge 커밋으로 이어지고, 회색 main 이름이 merge 커밋을 가리키는 그림|병합 뒤의 이력. 병합 커밋 merge: 주문 요약은 부모 커밋이 둘이고, main과 origin/main이 함께 가리킵니다.}}
<p><strong>도식 읽기</strong> — 아래에서 위로 읽습니다. 노트북 마지막의 <code>git log --oneline --graph</code> 출력을 옮긴 그림이고, 초록 상자 하나가 커밋 하나입니다.</p>
<p>맨 아래 첫 커밋에서 줄기가 둘로 갈라집니다. 오른쪽 기능 브랜치 줄기에는 <code>feat: 주문 요약 함수 추가</code>와 <code>fix: 빈 주문 건수 입력 확인</code>이 쌓였습니다. 맨 위 <code>merge: 주문 요약</code>은 두 줄기를 합친 병합 커밋입니다. 회색 이름 상자는 원격에 올린 뒤 <code>main</code>과 <code>origin/main</code>이 이 커밋을 함께 가리킨다는 뜻입니다.</p>
<p><strong>다음 학습과 이어지는 지점</strong> — 03절에서는 두 사람이 같은 줄을 다르게 고쳐 병합이 멈추는 경우를 봅니다. 충돌 표시를 읽고 합칠 결과를 직접 정합니다.</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2><details class="quiz"><summary>문제와 해설</summary>
<p class="quiz-q">1. 기능 브랜치에 커밋했을 때 main 브랜치는 어느 커밋을 가리키나요? · 기초</p><p class="quiz-a"><b>해설</b> — 첫 커밋을 그대로 가리킵니다. 노트북의 <code>git branch -v</code>에서 main은 <code>chore: 저장소와 PR 템플릿 시작</code>에 남았습니다. 새 커밋으로 옮겨 간 이름은 지금 있는 기능 브랜치뿐이었습니다.</p>
<p class="quiz-q">2. 리뷰어가 복제한 직후 폴더에 <code>summary.py</code>가 없었던 이유는 무엇인가요? · 기초</p><p class="quiz-a"><b>해설</b> — 복제한 저장소는 원격의 main 브랜치로 시작하는데, 이 파일은 기능 브랜치에만 있었기 때문입니다. 명령 <code>git switch feature/order-summary</code> 뒤에 목록에 나왔습니다.</p>
<p class="quiz-q">3. 명령 <code>git fetch</code> 뒤 리뷰어의 목록에 <code>behind 1</code>이 나왔습니다. 리뷰어 작업 폴더의 <code>summary.py</code>도 고친 내용으로 바뀌었나요? · 적용</p><p class="quiz-a"><b>해설</b> — 아닙니다. 명령 <code>git fetch</code>는 <code>origin/feature/order-summary</code> 이름만 옮기고 내 브랜치와 작업 폴더는 그대로 둡니다. 그래서 리뷰어는 main으로 옮긴 뒤 원격 쪽 이름을 병합했습니다.</p>
<p class="quiz-q">4. 「함수가 좀 이상해요」보다 노트북의 리뷰 의견이 나은 이유는 무엇인가요? · 적용</p><p class="quiz-a"><b>해설</b> — 넣은 값인 빈 글자와 실제 결과 <code>주문 건</code>을 적었습니다. 숫자로 바꿀 수 없으면 오류로 알려 달라는 기대 동작도 적었습니다. 그래서 작성자가 같은 결과를 다시 만들고 무엇을 고칠지 알 수 있습니다.</p>
<p class="quiz-q">5. 고친 결과가 팀의 main까지 들어갔다는 것을 노트북에서는 무엇으로 확인했나요? · 분석</p><p class="quiz-a"><b>해설</b> — 먼저 병합한 main에서 확인 파일을 실행해 <code>입력 오류</code> 줄을 봤습니다. 그다음 <code>git branch -vv</code>의 <code>[origin/main: ahead 3]</code>이 올린 뒤 <code>[origin/main]</code>으로 바뀐 것을 봤습니다. 끝으로 작성자 저장소의 <code>git log --oneline -1 origin/main</code>에서 <code>merge: 주문 요약</code>을 확인했습니다.</p>
</details>
<h2 id="b10"><span class="no">10</span>참고 자료</h2>
<ul><li><a href="https://docs.github.com/en/get-started/using-github/github-flow">GitHub Docs: GitHub flow</a> · 확인 2026-09-16 · 웹 문서</li><li><a href="https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository">GitHub Docs: PR 템플릿 만들기</a> · 확인 2026-09-16 · 웹 문서</li><li><a href="https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews">GitHub Docs: Pull Request 리뷰</a> · 확인 2026-09-09 · 웹 문서</li><li><a href="https://git-scm.com/docs/git-fetch">Git 공식 문서: git-fetch</a> · 확인 2026-09-16 · 실행 Git 2.34.1</li><li><a href="https://git-scm.com/docs/git-merge">Git 공식 문서: git-merge(--no-ff)</a> · 확인 2026-09-16 · 실행 Git 2.34.1</li><li><a href="https://git-scm.com/docs/git-diff">Git 공식 문서: git-diff(점 세 개 비교)</a> · 확인 2026-09-16 · 실행 Git 2.34.1</li></ul>
```

## 노트북 셀 (순서대로)

### [0] markdown {'html': 'skip'}

# GitHub Flow와 PR 리뷰

**이 노트북에서 할 일**

1. 임시 폴더에 팀 원격 저장소 하나와 작성자·리뷰어 저장소 두 개를 만듭니다.
2. 기능 브랜치에 커밋을 쌓아 원격에 올리고, PR로 볼 변경 범위와 설명을 만듭니다.
3. 리뷰에서 찾은 빈 값 결함을 고치고, 병합한 main을 원격까지 올립니다.

**준비물** — API 키 불필요. 데이터 파일도 없습니다. 모델 호출은 0번이고 비용은 들지 않습니다.
실행 시간은 1분 이내입니다. 01절에서 쓴 Git이 필요합니다.

**강의와 실습 범위** — 강의 시간에는 6~8번과 11~12번 소제목을 설명합니다.
6~8번은 기능 브랜치·올리기·PR 범위이고, 11~12번은 리뷰와 병합입니다.
1~5번과 9~10번은 셀을 함께 실행하고, 결과 읽기는 실습 시간에 이어서 읽습니다.

실습 폴더 `labs/part1/ch03-git-github`에서 `uv sync --locked`로 만든 `.venv`를 커널로 고릅니다.
첫 셀부터 순서대로 실행합니다. GitHub 계정과 네트워크는 쓰지 않습니다.
팀 원격 저장소도 임시 폴더 안에 만들므로, 실제 PR 화면은 이 노트북에 나오지 않습니다.

### [1] markdown {'html': 'skip'}

## 오늘 볼 그림

![위 가운데 팀 원격 저장소 team.git과 아래 왼쪽 작성자 저장소, 아래 오른쪽 리뷰어 저장소가 clone, push, fetch로 커밋을 주고받는 흐름도](attachment:02-1-세-저장소.png)

위 가운데 상자가 팀이 함께 쓰는 원격 저장소이고, 아래 왼쪽은 작성자, 아래 오른쪽은 리뷰어의 저장소입니다.
아래로 가는 화살표는 받아 오는 명령, 위로 가는 화살표는 올리는 명령입니다.
작성자와 리뷰어는 서로 직접 주고받지 않고, 늘 원격 저장소를 거칩니다.

### [2] markdown {}

## 1. 준비

이 절도 설치할 패키지가 없습니다. 01절처럼 빈 임시 폴더를 만들고 그 폴더로 작업 위치를 옮깁니다.
이번에는 그 안에 저장소 폴더 세 개를 만듭니다. 폴더 이름의 앞머리만 `ch03-02-`로 바꿨습니다.

### [3] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.569511Z', 'iopub.status.busy': '2026-09-16T12:28:43.569320Z', 'iopub.status.idle': '2026-09-16T12:28:43.575814Z', 'shell.execute_reply': '2026-09-16T12:28:43.574987Z'}, 'lesson_role': 'setup'}

```python
# 저장소 세 개를 담을 빈 임시 폴더를 만들고, 그 폴더로 작업 위치를 옮깁니다
import os
import tempfile

# mkdtemp()는 운영체제 임시 폴더 안에 새 폴더를 만들고 그 경로를 반환합니다
practice_folder = tempfile.mkdtemp(prefix="ch03-02-")
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

### [5] markdown {}

## 2. git 명령 함수에 폴더 더하기

01절의 `run_git()` 함수는 현재 작업 폴더에서만 git 명령을 실행했습니다. 이번 절은 저장소 세 개를 오가며 명령을 실행합니다.
그래서 같은 이름으로 함수를 다시 정의하고, 명령을 실행할 폴더를 받는 매개변수 `folder`를 더합니다.

- 매개변수 `folder`의 기본값은 `"."`입니다. 점 하나는 현재 작업 폴더를 뜻합니다. 기본값 매개변수는 Ch 2 04절에서 배웠습니다.
- 함수 `subprocess.run()`에 인자 `cwd=folder`를 더합니다. Ch 1 05절에서 쓴 인자로, 명령을 실행할 폴더를 정합니다.
- 출력 첫 줄에는 폴더 이름을 붙여 `author $ git push`처럼 보여 줍니다. 어느 저장소에서 실행한 명령인지 바로 읽을 수 있습니다.

나머지 줄은 01절과 같습니다. 같은 이름으로 다시 정의하면 뒤의 셀은 새 함수를 씁니다.
실행 전에 예상합니다. 정의 셀이라 출력은 없을 것입니다.

### [6] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.577418Z', 'iopub.status.busy': '2026-09-16T12:28:43.577274Z', 'iopub.status.idle': '2026-09-16T12:28:43.580660Z', 'shell.execute_reply': '2026-09-16T12:28:43.580178Z'}}

```python
# git 명령을 폴더 하나에서 실행하고, 폴더 이름과 명령, 출력을 함께 보여 주는 함수
import shlex
import subprocess


def run_git(command: str, folder: str = "."):
    full_command = "git " + command
    # split()은 따옴표로 묶은 메시지를 공백이 있어도 한 낱말로 둡니다
    arguments = shlex.split(full_command)
    # cwd 인자에 적은 폴더에서 명령을 실행하고, 글자는 UTF-8 규칙으로 읽습니다
    result = subprocess.run(arguments, capture_output=True, encoding="utf-8", cwd=folder)
    print(folder, "$", full_command)
    print(result.stdout + result.stderr)
    # 종료 코드가 0이 아닐 때만 숫자를 보여 줍니다
    if result.returncode != 0:
        print("종료 코드:", result.returncode)
```

출력:
```

```

### [7] markdown {}

**결과 읽기** — 예상대로 출력이 없습니다. 함수를 새로 정의하기만 했습니다.

### [8] markdown {}

## 3. 팀이 함께 쓰는 원격 저장소 만들기

여러 사람이 같은 코드를 고치려면 모두가 커밋을 올리고 받아 오는 저장소가 하나 필요합니다.
이런 저장소를 원격 저장소(remote repository)라고 부릅니다. 실무에서는 GitHub 서버의 저장소가 이 역할을 합니다.
이 노트북은 네트워크를 쓰지 않고, 임시 폴더 안의 `team.git` 폴더를 원격 저장소로 씁니다.

옵션 `--bare`는 작업 폴더 없이 커밋 기록만 담는 저장소를 만듭니다. 이런 저장소를 bare 저장소라고 부릅니다.
아무도 이 폴더에서 파일을 직접 고치지 않으므로 작업 폴더가 필요 없습니다. 옵션 `-b main`은 01절처럼 첫 브랜치 이름을 정합니다.

실행 전에 예상합니다. 빈 저장소를 만들었다는 줄이 나오고, 작업 폴더에 `team.git` 폴더가 생길 것입니다.

### [9] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.582073Z', 'iopub.status.busy': '2026-09-16T12:28:43.581954Z', 'iopub.status.idle': '2026-09-16T12:28:43.597044Z', 'shell.execute_reply': '2026-09-16T12:28:43.596489Z'}}

```python
# 팀 원격 저장소로 쓸 bare 저장소를 만들고, 작업 폴더의 파일을 봅니다
run_git("init --bare -b main team.git")
file_names = os.listdir()
print("현재 작업 폴더의 파일:", file_names)
```

출력:
```
. $ git init --bare -b main team.git
Initialized empty Git repository in [사용자 폴더]/tmp/ch03-02-8hklh3oc/team.git/

현재 작업 폴더의 파일: ['team.git']

```

### [10] markdown {}

**결과 읽기** — 첫 줄 `. $ git init --bare -b main team.git`의 점은 현재 작업 폴더에서 실행했다는 표시입니다.
둘째 줄 `Initialized empty Git repository`는 빈 저장소를 만들었다는 뜻입니다. 파일 목록은 `['team.git']`입니다.
01절과 달리 경로가 `.git/`이 아니라 `team.git/`으로 끝납니다. bare 저장소는 폴더 자체가 기록을 담기 때문입니다.

### [11] markdown {}

## 4. 작성자가 원격 저장소 복제하기

작성자는 원격 저장소를 복제(clone)해 자기 저장소를 만듭니다. 명령 `git clone team.git author`는 기록을 받아 `author` 폴더를 만듭니다.
복제한 저장소에는 원격 저장소의 위치가 `origin`이라는 이름으로 적힙니다. 처음 복제한 원격에 붙이는 관례적인 이름입니다.
명령 `git remote -v`는 저장소에 적힌 원격 이름과 위치를 보여 줍니다.

복제한 뒤 작성자 정보는 01절처럼 이 저장소에만 적습니다. 함수의 두 번째 인자 `"author"`가 명령을 실행할 폴더입니다.
실행 전에 예상합니다. 원격 저장소가 비어 있으므로, 빈 저장소를 복제했다는 안내가 나올 것입니다.

### [12] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.598234Z', 'iopub.status.busy': '2026-09-16T12:28:43.598116Z', 'iopub.status.idle': '2026-09-16T12:28:43.611428Z', 'shell.execute_reply': '2026-09-16T12:28:43.611059Z'}}

```python
# 원격 저장소를 author 폴더로 복제하고, 원격 이름을 본 뒤 작성자 정보를 이 저장소에만 적습니다
run_git("clone team.git author")
run_git("remote -v", "author")
run_git('config user.name "Ch3 Student"', "author")
run_git("config user.email student@example.com", "author")
run_git("config user.name", "author")
```

출력:
```
. $ git clone team.git author
Cloning into 'author'...
warning: You appear to have cloned an empty repository.
done.

author $ git remote -v
origin	[사용자 폴더]/tmp/ch03-02-8hklh3oc/team.git (fetch)
origin	[사용자 폴더]/tmp/ch03-02-8hklh3oc/team.git (push)

author $ git config user.name "Ch3 Student"

author $ git config user.email student@example.com

author $ git config user.name
Ch3 Student


```

### [13] markdown {}

**결과 읽기** — 줄 `Cloning into 'author'...`는 복제를 시작했다는 뜻입니다.
경고 `You appear to have cloned an empty repository`는 커밋이 없는 저장소를 복제했다는 안내이고, 종료 코드 줄은 없습니다.

둘째 명령의 출력에서 이름 `origin` 뒤의 경로가 원격 저장소의 위치입니다.
줄 끝의 `(fetch)`는 받아 올 때, `(push)`는 올릴 때 쓰는 위치입니다. 경로는 실행할 때마다 달라집니다.

뒤의 세 명령 줄 앞에도 `author $`가 붙어, 작성자 폴더에서 실행했음을 알 수 있습니다.
마지막 명령의 결과 `Ch3 Student`가 작성자 저장소에 저장된 이름입니다.

### [14] markdown {}

## 5. main에 첫 커밋을 만들어 원격에 올리기

팀 저장소의 출발점이 될 파일 두 개를 작성자가 만듭니다. 무시 규칙 파일 `.gitignore`에는 01절에서 쓴 `__pycache__/` 한 줄을 적습니다.

다른 파일 `pull_request_template.md`는 PR 설명의 빈 양식입니다. 풀 리퀘스트(PR)는 8번에서 자세히 설명합니다.
저장소에 이 이름의 파일이 있으면 GitHub가 PR 설명 칸에 양식을 채워 둡니다. 이번에 GitHub 화면에서는 확인하지 않았습니다.

파일 이름 앞의 `author/`는 Ch 1 02절에서 배운 상대 경로로, 작성자 폴더 안을 가리킵니다.
실행 전에 예상합니다. 두 파일이 main 브랜치의 첫 커밋에 들어갈 것입니다.

### [15] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.612346Z', 'iopub.status.busy': '2026-09-16T12:28:43.612248Z', 'iopub.status.idle': '2026-09-16T12:28:43.619569Z', 'shell.execute_reply': '2026-09-16T12:28:43.619131Z'}}

```python
# 작성자 저장소에 무시 규칙과 PR 템플릿을 만들고 첫 커밋으로 기록합니다
template_text = """## 변경 내용
- (여기에 적기)

## 확인한 입력
- [ ] 빈 값을 넣어 실행
"""
with open("author/.gitignore", "w", encoding="utf-8") as file:
    file.write("__pycache__/\n")
with open("author/pull_request_template.md", "w", encoding="utf-8") as file:
    file.write(template_text)
run_git("add .gitignore pull_request_template.md", "author")
run_git('commit -m "chore: 저장소와 PR 템플릿 시작"', "author")
```

출력:
```
author $ git add .gitignore pull_request_template.md

author $ git commit -m "chore: 저장소와 PR 템플릿 시작"
[main (root-commit) e439789] chore: 저장소와 PR 템플릿 시작
 2 files changed, 6 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 pull_request_template.md


```

### [16] markdown {}

**결과 읽기** — 표시 `main (root-commit)`은 main 브랜치의 첫 커밋이라는 뜻입니다.
요약 줄 `2 files changed`로 두 파일이 함께 들어간 것을 확인합니다.

### [17] markdown {}

지금 이 커밋은 작성자 저장소에만 있습니다. 명령 `git push`는 내 저장소의 커밋을 원격 저장소로 올립니다.
명령 `git push -u origin main`은 main 브랜치를 원격 `origin`에 올린다는 뜻입니다.

옵션 `-u`는 내 main과 원격의 main을 짝으로 적어 둡니다. 그다음부터는 `git push`만 적어도 같은 짝으로 올립니다.
실행 전에 예상합니다. 원격 저장소에 main 브랜치가 새로 생겼다는 줄이 나올 것입니다.

### [18] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.620465Z', 'iopub.status.busy': '2026-09-16T12:28:43.620377Z', 'iopub.status.idle': '2026-09-16T12:28:43.629415Z', 'shell.execute_reply': '2026-09-16T12:28:43.629007Z'}}

```python
# 작성자의 main 브랜치를 원격 저장소에 올리고 짝으로 적어 둡니다
run_git("push -u origin main", "author")
```

출력:
```
author $ git push -u origin main
Branch 'main' set up to track remote branch 'main' from 'origin'.
To [사용자 폴더]/tmp/ch03-02-8hklh3oc/team.git
 * [new branch]      main -> main


```

### [19] markdown {}

**결과 읽기** — 표시 `[new branch]`는 원격 저장소에 브랜치가 새로 생겼다는 뜻입니다.
같은 줄의 `main -> main`은 내 main을 원격의 main으로 올렸다는 뜻입니다.
출력 첫 줄 `Branch 'main' set up to track`은 옵션 `-u`로 두 main을 짝으로 적었다는 안내입니다.

### [20] markdown {}

## 6. 기능 브랜치 만들기

브랜치(branch)는 커밋이 이어지는 줄기의 이름입니다. 01절에서는 main 브랜치 하나에만 커밋을 쌓았습니다.

작업 방식 GitHub Flow는 main을 늘 동작하는 상태로 두고, 새 작업은 따로 만든 브랜치에서 합니다.
이렇게 기능 하나를 만들려고 main에서 갈라 낸 브랜치를 기능 브랜치(feature branch)라고 부릅니다.

명령 `git switch -c feature/order-summary`는 지금 커밋에서 새 브랜치를 만들고 그 브랜치로 옮겨 갑니다.
옵션 `-c`는 새로 만들기(create)를 뜻합니다. 명령 `git branch`는 브랜치 목록을 보여 줍니다.
실행 전에 예상합니다. 목록에 브랜치 두 개가 나오고, 새 브랜치 앞에 표시가 붙을 것입니다.

### [21] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.630309Z', 'iopub.status.busy': '2026-09-16T12:28:43.630238Z', 'iopub.status.idle': '2026-09-16T12:28:43.634327Z', 'shell.execute_reply': '2026-09-16T12:28:43.634022Z'}}

```python
# 작성자 저장소에서 기능 브랜치를 만들어 옮겨 가고, 브랜치 목록을 봅니다
run_git("switch -c feature/order-summary", "author")
run_git("branch", "author")
```

출력:
```
author $ git switch -c feature/order-summary
Switched to a new branch 'feature/order-summary'

author $ git branch
* feature/order-summary
  main


```

### [22] markdown {}

**결과 읽기** — 줄 `Switched to a new branch 'feature/order-summary'`는 새 브랜치로 옮겨 갔다는 뜻입니다.
목록의 `* feature/order-summary`에서 별표는 지금 있는 브랜치를 가리킵니다. 아래 줄의 `main`도 그대로 남아 있습니다.

### [23] markdown {}

기능 브랜치에 주문 요약 함수 파일 `summary.py`를 커밋합니다. 함수는 주문 건수를 받아 01절 `app.py`처럼 「주문 N건」 글을 반환합니다.
파일에 적는 글은 Ch 2 04절의 함수 정의이고, 매개변수 옆 `int`는 Ch 2 07절의 타입힌트입니다.

명령 `git branch -v`는 브랜치마다 가리키는 커밋의 메시지도 함께 보여 줍니다.
실행 전에 예상합니다. 기능 브랜치만 새 커밋을 가리키고, main은 첫 커밋에 남을 것입니다.

### [24] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.635037Z', 'iopub.status.busy': '2026-09-16T12:28:43.634962Z', 'iopub.status.idle': '2026-09-16T12:28:43.641306Z', 'shell.execute_reply': '2026-09-16T12:28:43.640969Z'}}

```python
# 기능 브랜치에 주문 요약 함수 파일을 커밋하고, 브랜치마다 가리키는 커밋을 봅니다
summary_text = """def summarize(count: int) -> str:
    return f"주문 {count}건"
"""
with open("author/summary.py", "w", encoding="utf-8") as file:
    file.write(summary_text)
run_git("add summary.py", "author")
run_git('commit -m "feat: 주문 요약 함수 추가"', "author")
run_git("branch -v", "author")
```

출력:
```
author $ git add summary.py

author $ git commit -m "feat: 주문 요약 함수 추가"
[feature/order-summary 2d95a9b] feat: 주문 요약 함수 추가
 1 file changed, 2 insertions(+)
 create mode 100644 summary.py

author $ git branch -v
* feature/order-summary 2d95a9b feat: 주문 요약 함수 추가
  main                  e439789 chore: 저장소와 PR 템플릿 시작


```

### [25] markdown {}

**결과 읽기** — 커밋 요약 줄은 `1 file changed, 2 insertions(+)`입니다.
브랜치 목록에서 기능 브랜치는 `feat: 주문 요약 함수 추가` 커밋을 가리킵니다. main 브랜치는 `chore: 저장소와 PR 템플릿 시작` 커밋에 남았습니다.
새 커밋을 만들면 지금 있는 브랜치만 앞으로 옮겨 갑니다.

### [26] markdown {}

## 7. 기능 브랜치를 원격 저장소에 올리기

기능 브랜치도 원격 저장소에 올려야 다른 사람이 볼 수 있습니다. main 브랜치를 올릴 때처럼 옵션 `-u`로 짝을 적습니다.
명령 `git branch -vv`는 브랜치마다 짝이 된 원격 브랜치의 이름을 대괄호 안에 보여 줍니다.

실행 전에 예상합니다. 두 브랜치 모두 대괄호 안에 `origin/`으로 시작하는 이름이 나올 것입니다.

### [27] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.641965Z', 'iopub.status.busy': '2026-09-16T12:28:43.641897Z', 'iopub.status.idle': '2026-09-16T12:28:43.650430Z', 'shell.execute_reply': '2026-09-16T12:28:43.650088Z'}}

```python
# 기능 브랜치를 원격에 올리고, 브랜치마다 짝이 된 원격 브랜치를 봅니다
run_git("push -u origin feature/order-summary", "author")
run_git("branch -vv", "author")
```

출력:
```
author $ git push -u origin feature/order-summary
Branch 'feature/order-summary' set up to track remote branch 'feature/order-summary' from 'origin'.
To [사용자 폴더]/tmp/ch03-02-8hklh3oc/team.git
 * [new branch]      feature/order-summary -> feature/order-summary

author $ git branch -vv
* feature/order-summary 2d95a9b [origin/feature/order-summary] feat: 주문 요약 함수 추가
  main                  e439789 [origin/main] chore: 저장소와 PR 템플릿 시작


```

### [28] markdown {}

**결과 읽기** — 표시 `[new branch]`로 원격에 기능 브랜치가 생긴 것을 확인합니다.
목록의 `[origin/feature/order-summary]`와 `[origin/main]`이 짝이 된 원격 브랜치의 이름입니다.

이름 `origin/main`은 작성자 저장소가 마지막으로 확인한 원격 main의 위치입니다. 원격 저장소를 매번 새로 읽는 이름은 아닙니다.

### [29] markdown {}

## 8. PR로 볼 변경 범위와 설명 만들기

풀 리퀘스트(pull request, PR)는 내 브랜치의 변경을 main에 합쳐 달라고 요청하는 GitHub 기능입니다.
PR 화면에는 바뀐 파일, 설명 글, 리뷰 의견이 한곳에 모입니다.
이 노트북은 GitHub를 쓰지 않으므로, PR 화면에 나올 변경 범위와 설명 글을 직접 만듭니다.

명령 `git diff --stat origin/main...HEAD`는 원격 main과 지금 브랜치를 비교합니다.
점 세 개 `...`는 두 브랜치가 갈라진 커밋 뒤로 지금 브랜치에 더해진 변경만 보라는 뜻입니다. 옵션 `--stat`은 파일별 줄 수만 보여 줍니다.

실행 전에 예상합니다. 이번 기능 브랜치에서 더한 `summary.py` 한 파일만 나올 것입니다.

### [30] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.651154Z', 'iopub.status.busy': '2026-09-16T12:28:43.651083Z', 'iopub.status.idle': '2026-09-16T12:28:43.653874Z', 'shell.execute_reply': '2026-09-16T12:28:43.653494Z'}}

```python
# PR에 나올 변경 범위를 파일별 줄 수로 요약합니다
run_git("diff --stat origin/main...HEAD", "author")
```

출력:
```
author $ git diff --stat origin/main...HEAD
 summary.py | 2 ++
 1 file changed, 2 insertions(+)


```

### [31] markdown {}

**결과 읽기** — 줄 `summary.py | 2 ++`는 이 파일에 두 줄이 더해졌다는 뜻입니다. 요약 줄은 `1 file changed, 2 insertions(+)`입니다.
첫 커밋에 있던 두 파일은 이번 범위에 들어가지 않았습니다.

### [32] markdown {}

PR 설명은 저장소에 있는 템플릿을 채워 씁니다. 템플릿 파일을 읽기 모드 `"r"`로 열어 글을 읽고, 빈칸 `(여기에 적기)`를 바꿉니다.
글의 메서드 `replace()`는 Ch 1 04절에서 쓴 메서드로, 앞 글을 뒤 글로 바꾼 새 글을 반환합니다.

확인 칸 `- [ ] 빈 값을 넣어 실행`은 작성자가 아직 해 보지 않아 그대로 둡니다. 대괄호 안에 x를 적으면 확인했다는 표시입니다.
실행 전에 예상합니다. 변경 내용 칸만 채워지고, 확인 칸은 빈 대괄호로 남을 것입니다.

### [33] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.654558Z', 'iopub.status.busy': '2026-09-16T12:28:43.654493Z', 'iopub.status.idle': '2026-09-16T12:28:43.656220Z', 'shell.execute_reply': '2026-09-16T12:28:43.655954Z'}}

```python
# 저장소의 PR 템플릿을 읽고, 변경 내용 칸을 채워 PR 설명 글을 만듭니다
with open("author/pull_request_template.md", "r", encoding="utf-8") as file:
    saved_template = file.read()
pr_text = saved_template.replace("(여기에 적기)", "주문 건수를 글로 만드는 summarize() 함수 추가")
print("PR 설명 글:")
print(pr_text)
```

출력:
```
PR 설명 글:
## 변경 내용
- 주문 건수를 글로 만드는 summarize() 함수 추가

## 확인한 입력
- [ ] 빈 값을 넣어 실행


```

### [34] markdown {}

**결과 읽기** — 줄 `- 주문 건수를 글로 만드는 summarize() 함수 추가`가 채워진 변경 내용입니다.
확인 칸은 `- [ ] 빈 값을 넣어 실행`으로 비어 있습니다.
실제 GitHub에서는 이 글을 PR 설명 칸에 적습니다. 이번에는 PR 화면을 만들지 않았습니다.

### [35] markdown {}

## 9. 리뷰어가 원격 저장소 복제하기

코드 리뷰(code review)는 작성자가 아닌 사람이 변경을 읽고 실행해 보며 문제를 찾는 일입니다.
리뷰어는 자기 저장소를 따로 복제해 기능 브랜치를 확인합니다. 병합 커밋도 만들 것이므로 리뷰어 정보를 적습니다.
이름은 작성자와 같은 규칙으로 `Ch3 Reviewer`를 씁니다.

복제한 뒤 폴더의 파일 목록도 봅니다. 목록 순서는 컴퓨터마다 다를 수 있어 Ch 2 03절의 `sorted()`로 정렬합니다.
실행 전에 예상합니다. 원격에 커밋이 있으니 경고 없이 복제되고, 목록에 `summary.py`는 없을 것입니다.

### [36] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.656949Z', 'iopub.status.busy': '2026-09-16T12:28:43.656873Z', 'iopub.status.idle': '2026-09-16T12:28:43.667309Z', 'shell.execute_reply': '2026-09-16T12:28:43.666988Z'}}

```python
# 원격 저장소를 reviewer 폴더로 복제하고, 리뷰어 정보를 적은 뒤 파일 목록을 봅니다
run_git("clone team.git reviewer")
run_git('config user.name "Ch3 Reviewer"', "reviewer")
run_git("config user.email reviewer@example.com", "reviewer")
file_names = os.listdir("reviewer")
print("reviewer 폴더의 파일:", sorted(file_names))
```

출력:
```
. $ git clone team.git reviewer
Cloning into 'reviewer'...
done.

reviewer $ git config user.name "Ch3 Reviewer"

reviewer $ git config user.email reviewer@example.com

reviewer 폴더의 파일: ['.git', '.gitignore', 'pull_request_template.md']

```

### [37] markdown {}

**결과 읽기** — 복제 출력에는 빈 저장소 경고가 없습니다. 파일 목록은 `['.git', '.gitignore', 'pull_request_template.md']`입니다.
복제한 저장소는 원격의 main 브랜치로 시작합니다. 그래서 기능 브랜치에만 있는 `summary.py`는 보이지 않습니다.

### [38] markdown {}

## 10. 값 하나 바꿔 보기 — 브랜치를 main에서 기능 브랜치로

같은 리뷰어 폴더에서 브랜치 하나만 바꿔 파일 목록을 다시 봅니다. 명령 `git switch feature/order-summary`는 그 브랜치로 옮겨 갑니다.
리뷰어 저장소에는 아직 이 이름의 브랜치가 없습니다. 이럴 때 원격에 같은 이름이 있으면, 그 원격 브랜치와 짝인 브랜치를 새로 만듭니다.

실행 전에 예상합니다. 옮겨 간 뒤에는 목록에 `summary.py`가 더해질 것입니다.

### [39] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.668026Z', 'iopub.status.busy': '2026-09-16T12:28:43.667960Z', 'iopub.status.idle': '2026-09-16T12:28:43.671458Z', 'shell.execute_reply': '2026-09-16T12:28:43.671043Z'}}

```python
# 리뷰어 저장소를 기능 브랜치로 옮기고, 파일 목록을 다시 봅니다
run_git("switch feature/order-summary", "reviewer")
file_names = os.listdir("reviewer")
print("reviewer 폴더의 파일:", sorted(file_names))
```

출력:
```
reviewer $ git switch feature/order-summary
Branch 'feature/order-summary' set up to track remote branch 'feature/order-summary' from 'origin'.
Switched to a new branch 'feature/order-summary'

reviewer 폴더의 파일: ['.git', '.gitignore', 'pull_request_template.md', 'summary.py']

```

### [40] markdown {}

**결과 읽기** — 줄 `set up to track remote branch`는 원격 브랜치와 짝인 브랜치를 새로 만들었다는 안내입니다.
파일 목록 끝에 `'summary.py'`가 더해졌습니다. 같은 폴더라도 브랜치를 옮기면 작업 폴더의 파일이 바뀝니다.

### [41] markdown {'lesson_part': 'before'}

## 11. Before — 리뷰어가 기능 브랜치를 읽고 실행하기

리뷰어는 줄 수 요약보다 실제로 바뀐 줄을 먼저 읽습니다. 옵션 `--stat` 없이 같은 범위를 비교합니다.
실행 전에 예상합니다. 더하기(+) 줄 두 개로 된 함수가 나올 것입니다.

### [42] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.672109Z', 'iopub.status.busy': '2026-09-16T12:28:43.672048Z', 'iopub.status.idle': '2026-09-16T12:28:43.674501Z', 'shell.execute_reply': '2026-09-16T12:28:43.674186Z'}, 'lesson_part': 'before'}

```python
# Before: 리뷰어가 기능 브랜치에서 더해진 줄을 읽습니다
run_git("diff origin/main...HEAD", "reviewer")
```

출력:
```
reviewer $ git diff origin/main...HEAD
diff --git a/summary.py b/summary.py
new file mode 100644
index 0000000..25319f7
--- /dev/null
+++ b/summary.py
@@ -0,0 +1,2 @@
+def summarize(count: int) -> str:
+    return f"주문 {count}건"


```

### [43] markdown {'lesson_part': 'before'}

**결과 읽기** — 더하기 줄 `+def summarize(count: int) -> str:`와 `+    return f"주문 {count}건"`이 기능 브랜치가 더한 전부입니다.
타입힌트 `int`가 있어도 Ch 2 07절에서 본 것처럼 값을 검사하지는 않습니다.
PR 설명의 빈 값 확인 칸도 비어 있었으므로, 리뷰어가 직접 실행해 봅니다.

### [44] markdown {'lesson_part': 'before'}

확인 파일을 새 Python으로 실행하는 함수 `run_python()`을 만듭니다. 뼈대는 Ch 2 08절 `run_pytest()`와 같습니다.
목록 첫 칸 `sys.executable`은 지금 노트북을 실행하는 Python 프로그램의 경로이고, 둘째 칸이 실행할 파일 이름입니다.
인자 `cwd=folder`로 실행할 폴더를 정합니다.

글자는 Ch 2 08절처럼 인자 `text=True`로 받습니다. 새로 실행한 Python은 컴퓨터의 기본 규칙으로 글자를 내보내므로, 받는 쪽도 같은 규칙으로 읽습니다.
출력을 보여 주는 네 줄은 `run_git()`과 같습니다. 실행 전에 예상합니다. 정의 셀이라 출력은 없을 것입니다.

### [45] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.675209Z', 'iopub.status.busy': '2026-09-16T12:28:43.675150Z', 'iopub.status.idle': '2026-09-16T12:28:43.677259Z', 'shell.execute_reply': '2026-09-16T12:28:43.676913Z'}, 'lesson_part': 'before'}

```python
# 폴더 하나에서 Python 파일을 실행하고, 출력과 종료 코드를 보여 주는 함수
import sys


def run_python(file_name: str, folder: str):
    arguments = [sys.executable, file_name]
    # 출력을 모아 두고, Ch 2 08절처럼 글로 받습니다
    result = subprocess.run(arguments, capture_output=True, text=True, cwd=folder)
    print(folder, "$ python", file_name)
    print(result.stdout + result.stderr)
    if result.returncode != 0:
        print("종료 코드:", result.returncode)
```

출력:
```

```

### [46] markdown {'lesson_part': 'before'}

**결과 읽기** — 예상대로 출력이 없습니다. 함수를 만들기만 했습니다.

### [47] markdown {'lesson_part': 'before'}

리뷰어가 확인 파일 `check_summary.py`를 자기 폴더에 만듭니다. 이 파일은 함수에 보통 값 3과 빈 글자 `""`를 차례로 넣습니다.
첫 줄은 Ch 2 07절의 `from … import` 문으로, 같은 폴더의 `summary.py`에서 함수를 불러옵니다.

빈 글자 쪽은 Ch 2 05절처럼 `try`와 `except ValueError`로 감쌉니다. 숫자로 바꿀 수 없다는 오류가 나면 멈추지 않고 내용을 출력합니다.
확인 파일은 리뷰어만 쓰는 파일이라 커밋하지 않습니다.
실행 전에 예상합니다. 빈 글자를 넣으면 건수가 비어 있는 글이 나올 것입니다.

### [48] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.677946Z', 'iopub.status.busy': '2026-09-16T12:28:43.677880Z', 'iopub.status.idle': '2026-09-16T12:28:43.689621Z', 'shell.execute_reply': '2026-09-16T12:28:43.689244Z'}, 'lesson_part': 'before'}

```python
# Before: 보통 값과 빈 글자를 넣어 보는 확인 파일을 만들고 기능 브랜치에서 실행합니다
check_text = """from summary import summarize

print("보통 값 3:", summarize(3))
try:
    print("빈 값:", summarize(""))
except ValueError as error:
    print("입력 오류:", error)
"""
with open("reviewer/check_summary.py", "w", encoding="utf-8") as file:
    file.write(check_text)
run_python("check_summary.py", "reviewer")
```

출력:
```
reviewer $ python check_summary.py
보통 값 3: 주문 3건
빈 값: 주문 건


```

### [49] markdown {'lesson_part': 'before'}

**결과 읽기** — 보통 값은 `보통 값 3: 주문 3건`으로 맞게 나왔습니다. 빈 글자는 오류 없이 `빈 값: 주문 건`이 나왔습니다.
건수가 빠진 틀린 글이 조용히 만들어졌고, 입력 오류 줄은 없습니다.

리뷰어는 PR에 이렇게 의견을 남깁니다. 「빈 글자를 넣으면 오류 없이 `주문 건`이 나옵니다. 숫자로 바꿀 수 없는 값은 오류로 알려 주세요.」
의견에는 넣은 값, 실제 결과, 기대하는 동작을 함께 적습니다. 그래야 작성자가 같은 결과를 다시 만들 수 있습니다.
이번에는 GitHub 화면에 의견을 적지 않았습니다.

### [50] markdown {'lesson_part': 'after'}

## 12. After — 고친 커밋을 올리고 main에 병합하기

작성자는 리뷰 의견대로 함수를 고칩니다. 글을 만들기 전에 Ch 2 01절의 형 변환 `int()`로 건수를 정수로 바꿉니다.
빈 글자처럼 정수로 바꿀 수 없는 값이 오면 `int()`에서 `ValueError`가 납니다. Ch 2 05절처럼 틀린 값을 빈 결과로 감추지 않고 드러내는 방법입니다.

함수 `int()`는 숫자 모양 글 `"3"`도 정수 3으로 바꾸므로, 고친 함수는 그런 글도 받습니다. 이 경우는 이번에 실행하지 않았습니다.

고친 커밋은 같은 기능 브랜치에 쌓고 `git push`로 올립니다. 옵션 `-u`로 짝을 적어 두었으므로 원격과 브랜치 이름은 적지 않습니다.
실행 전에 예상합니다. 비교 결과에 빼기 줄 하나와 더하기 줄 세 개가 나올 것입니다.

### [51] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.690217Z', 'iopub.status.busy': '2026-09-16T12:28:43.690163Z', 'iopub.status.idle': '2026-09-16T12:28:43.701441Z', 'shell.execute_reply': '2026-09-16T12:28:43.701027Z'}, 'lesson_part': 'after'}

```python
# After: 작성자가 함수를 고쳐 커밋하고, 같은 기능 브랜치를 원격에 올립니다
fixed_text = """def summarize(count: int) -> str:
    # 정수로 바꿀 수 없는 값이면 ValueError가 납니다
    number = int(count)
    return f"주문 {number}건"
"""
with open("author/summary.py", "w", encoding="utf-8") as file:
    file.write(fixed_text)
run_git("diff", "author")
run_git("add summary.py", "author")
run_git('commit -m "fix: 빈 주문 건수 입력 확인"', "author")
run_git("push", "author")
```

출력:
```
author $ git diff
diff --git a/summary.py b/summary.py
index 25319f7..6c43abd 100644
--- a/summary.py
+++ b/summary.py
@@ -1,2 +1,4 @@
 def summarize(count: int) -> str:
-    return f"주문 {count}건"
+    # 정수로 바꿀 수 없는 값이면 ValueError가 납니다
+    number = int(count)
+    return f"주문 {number}건"

author $ git add summary.py

author $ git commit -m "fix: 빈 주문 건수 입력 확인"
[feature/order-summary e05b0df] fix: 빈 주문 건수 입력 확인
 1 file changed, 3 insertions(+), 1 deletion(-)

author $ git push
To [사용자 폴더]/tmp/ch03-02-8hklh3oc/team.git
   2d95a9b..e05b0df  feature/order-summary -> feature/order-summary


```

### [52] markdown {'lesson_part': 'after'}

**결과 읽기** — 비교 결과에서 `-    return f"주문 {count}건"` 줄이 빠지고 `+    number = int(count)` 줄이 더해졌습니다.
커밋 요약 줄은 `1 file changed, 3 insertions(+), 1 deletion(-)`입니다.
올리기 출력의 `feature/order-summary -> feature/order-summary`는 원격의 기능 브랜치가 새 커밋으로 옮겨 갔다는 뜻입니다.

### [53] markdown {'lesson_part': 'after'}

리뷰어 저장소는 아직 고친 커밋을 모릅니다. 명령 `git fetch`는 원격 저장소의 새 커밋을 받아 오고, `origin/`으로 시작하는 이름만 옮깁니다.
내 브랜치는 옮기지 않으므로 작업 폴더의 파일도 그대로입니다.

받아 온 뒤 `git branch -vv`로 짝과 비교한 결과를 봅니다.
실행 전에 예상합니다. 리뷰어의 기능 브랜치가 원격보다 커밋 하나 뒤처졌다는 표시가 나올 것입니다.

### [54] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.702221Z', 'iopub.status.busy': '2026-09-16T12:28:43.702164Z', 'iopub.status.idle': '2026-09-16T12:28:43.709428Z', 'shell.execute_reply': '2026-09-16T12:28:43.709064Z'}, 'lesson_part': 'after'}

```python
# After: 리뷰어 저장소에서 원격의 새 커밋을 받아 오고, 짝과 비교한 결과를 봅니다
run_git("fetch", "reviewer")
run_git("branch -vv", "reviewer")
```

출력:
```
reviewer $ git fetch
From [사용자 폴더]/tmp/ch03-02-8hklh3oc/team
   2d95a9b..e05b0df  feature/order-summary -> origin/feature/order-summary

reviewer $ git branch -vv
* feature/order-summary 2d95a9b [origin/feature/order-summary: behind 1] feat: 주문 요약 함수 추가
  main                  e439789 [origin/main] chore: 저장소와 PR 템플릿 시작


```

### [55] markdown {'lesson_part': 'after'}

**결과 읽기** — 받아 오기 출력의 `feature/order-summary -> origin/feature/order-summary`는 원격 이름 쪽만 새 커밋으로 옮겼다는 뜻입니다.
목록의 `behind 1`은 리뷰어의 기능 브랜치가 짝보다 커밋 1개 뒤라는 뜻입니다.

### [56] markdown {'lesson_part': 'after'}

리뷰 의견이 반영됐으니 기능 브랜치를 main에 병합(merge)합니다. 병합은 두 브랜치의 커밋 줄기를 하나로 합치는 일입니다.
리뷰어는 main으로 옮긴 뒤 방금 받아 온 원격 이름 `origin/feature/order-summary`를 병합합니다. 리뷰어의 기능 브랜치는 한 커밋 뒤처져 있기 때문입니다.

옵션 `--no-ff`는 병합 커밋을 꼭 만들라는 뜻입니다. 병합 커밋(merge commit)은 부모 커밋이 둘인 커밋입니다.
이 옵션이 없으면 main 이름만 앞으로 옮기는 fast-forward 병합이 될 수 있습니다. 그 경우는 이번에 실행하지 않았습니다.

실행 전에 예상합니다. 병합 커밋이 만들어지고, main에 `summary.py`가 들어올 것입니다.

### [57] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.710196Z', 'iopub.status.busy': '2026-09-16T12:28:43.710130Z', 'iopub.status.idle': '2026-09-16T12:28:43.714900Z', 'shell.execute_reply': '2026-09-16T12:28:43.714539Z'}, 'lesson_part': 'after'}

```python
# After: 리뷰어가 main으로 옮겨 원격의 기능 브랜치를 병합 커밋으로 합칩니다
run_git("switch main", "reviewer")
run_git('merge --no-ff origin/feature/order-summary -m "merge: 주문 요약"', "reviewer")
```

출력:
```
reviewer $ git switch main
Your branch is up to date with 'origin/main'.
Switched to branch 'main'

reviewer $ git merge --no-ff origin/feature/order-summary -m "merge: 주문 요약"
Merge made by the 'ort' strategy.
 summary.py | 4 ++++
 1 file changed, 4 insertions(+)
 create mode 100644 summary.py


```

### [58] markdown {'lesson_part': 'after'}

**결과 읽기** — 줄 `Merge made by the 'ort' strategy.`는 병합 커밋을 만들었다는 뜻입니다. 따옴표 안 ort는 병합 방법의 이름입니다.
요약 줄 `1 file changed, 4 insertions(+)`는 main에서 본 변경입니다. 없던 `summary.py`가 고친 네 줄로 들어왔습니다.

### [59] markdown {'lesson_part': 'after'}

병합한 main에서 Before와 같은 확인 파일을 다시 실행합니다. 확인 파일은 커밋하지 않았으므로 브랜치를 옮겨도 폴더에 남아 있습니다.
원격에 올리기 전에 병합 결과를 먼저 확인하는 순서입니다.
실행 전에 예상합니다. 보통 값은 그대로이고, 빈 값 쪽에는 입력 오류 줄이 나올 것입니다.

### [60] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.715521Z', 'iopub.status.busy': '2026-09-16T12:28:43.715455Z', 'iopub.status.idle': '2026-09-16T12:28:43.725356Z', 'shell.execute_reply': '2026-09-16T12:28:43.724954Z'}, 'lesson_part': 'after'}

```python
# After: 병합한 main에서 Before와 같은 확인 파일을 실행합니다
run_python("check_summary.py", "reviewer")
```

출력:
```
reviewer $ python check_summary.py
보통 값 3: 주문 3건
입력 오류: invalid literal for int() with base 10: ''


```

### [61] markdown {'lesson_part': 'after'}

**결과 읽기** — 보통 값은 Before와 같은 `보통 값 3: 주문 3건`입니다.
빈 글자는 `입력 오류: invalid literal for int() with base 10: ''`로 바뀌었습니다.
함수 안의 `int()`가 오류를 냈고, 확인 파일의 `except` 블록이 받아 출력했습니다.
오류 글은 Ch 2 13절 실습에서 「많이」를 정수로 바꿀 때 본 것과 같은 모양입니다. 종료 코드 줄이 없으므로 확인 파일은 끝까지 실행됐습니다.

### [62] markdown {'lesson_part': 'after'}

병합 커밋은 아직 리뷰어 저장소에만 있습니다. 올리기 전과 뒤에 `git branch -vv`를 한 번씩 실행해 짝과 비교합니다.
리뷰어의 main은 복제할 때 이미 원격 main과 짝이 됐습니다. 그래도 어디로 올리는지 보이도록 `origin main`을 적습니다.

명령 `git log --oneline --graph`는 커밋 이력을 줄기 모양 그림과 함께 보여 줍니다.
실행 전에 예상합니다. 올리기 전에는 main이 원격보다 앞섰다는 표시가 나오고, 올린 뒤에는 사라질 것입니다.

### [63] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.726005Z', 'iopub.status.busy': '2026-09-16T12:28:43.725954Z', 'iopub.status.idle': '2026-09-16T12:28:43.734586Z', 'shell.execute_reply': '2026-09-16T12:28:43.734213Z'}, 'lesson_part': 'after'}

```python
# After: 앞선 main을 원격에 올리고, 올리기 전과 뒤의 짝 비교와 이력을 봅니다
run_git("branch -vv", "reviewer")
run_git("push origin main", "reviewer")
run_git("branch -vv", "reviewer")
run_git("log --oneline --graph", "reviewer")
```

출력:
```
reviewer $ git branch -vv
  feature/order-summary 2d95a9b [origin/feature/order-summary: behind 1] feat: 주문 요약 함수 추가
* main                  7c8816b [origin/main: ahead 3] merge: 주문 요약

reviewer $ git push origin main
To [사용자 폴더]/tmp/ch03-02-8hklh3oc/team.git
   e439789..7c8816b  main -> main

reviewer $ git branch -vv
  feature/order-summary 2d95a9b [origin/feature/order-summary: behind 1] feat: 주문 요약 함수 추가
* main                  7c8816b [origin/main] merge: 주문 요약

reviewer $ git log --oneline --graph
*   7c8816b merge: 주문 요약
|\  
| * e05b0df fix: 빈 주문 건수 입력 확인
| * 2d95a9b feat: 주문 요약 함수 추가
|/  
* e439789 chore: 저장소와 PR 템플릿 시작


```

### [64] markdown {'lesson_part': 'after'}

**결과 읽기** — 올리기 전 목록의 `[origin/main: ahead 3]`은 리뷰어 main이 원격 main보다 커밋 3개 앞섰다는 뜻입니다.
기능 커밋 두 개와 병합 커밋 하나입니다. 올린 뒤에는 `[origin/main]`만 남아 두 main이 같은 커밋을 가리킵니다.

이력 그림 맨 위가 병합 커밋 `merge: 주문 요약`이고, 그 아래로 줄기가 둘로 갈라집니다.
오른쪽 줄기에 `fix: 빈 주문 건수 입력 확인`과 `feat: 주문 요약 함수 추가`가 있습니다. 두 줄기가 다시 만나는 맨 아래가 첫 커밋입니다.

### [65] markdown {'lesson_part': 'after'}

마지막으로 작성자 저장소에서 확인합니다. 작성자는 main을 직접 고치지 않았습니다.

명령 `git fetch`로 받아 온 뒤, 이름 `origin/main`이 가리키는 커밋을 봅니다. 옵션 `-1`은 가장 최근 커밋 한 개만 보여 달라는 뜻입니다.
실행 전에 예상합니다. 리뷰어가 올린 병합 커밋이 나올 것입니다.

### [66] code {'execution': {'iopub.execute_input': '2026-09-16T12:28:43.735254Z', 'iopub.status.busy': '2026-09-16T12:28:43.735197Z', 'iopub.status.idle': '2026-09-16T12:28:43.741353Z', 'shell.execute_reply': '2026-09-16T12:28:43.741044Z'}, 'lesson_part': 'after'}

```python
# After: 작성자 저장소에서 원격의 새 main을 받아 오고, 가장 최근 커밋을 봅니다
run_git("fetch", "author")
run_git("log --oneline -1 origin/main", "author")
```

출력:
```
author $ git fetch
From [사용자 폴더]/tmp/ch03-02-8hklh3oc/team
   e439789..7c8816b  main       -> origin/main

author $ git log --oneline -1 origin/main
7c8816b merge: 주문 요약


```

### [67] markdown {'lesson_part': 'after'}

**결과 읽기** — 받아 오기 출력의 `-> origin/main`은 작성자 저장소의 원격 이름이 새 커밋으로 옮겨 갔다는 뜻입니다.
마지막 줄의 `merge: 주문 요약`이 원격 main의 가장 최근 커밋입니다. 리뷰어가 올린 병합 결과를 작성자 저장소에서도 확인했습니다.

## 정리

- 새 작업은 기능 브랜치에 커밋하고, `git push`로 원격 저장소에 올립니다.
- PR에서는 `git diff origin/main...HEAD`로 변경 범위를 읽고, 리뷰어가 직접 실행해 결함을 찾습니다.
- 고친 커밋을 같은 브랜치에 올리고, 리뷰어는 `git fetch` 뒤 main에 병합해 원격까지 올립니다.

이번에는 Linux의 Git 2.34.1로, 임시 폴더의 원격 저장소를 써서 실행했습니다. GitHub 화면과 다른 운영체제에서는 실행하지 않았습니다.
다음 절에서는 두 브랜치가 같은 줄을 다르게 고쳐 병합이 멈추는 경우를 다룹니다.

## 그림

### 02-1-세-저장소.mmd

```mermaid
flowchart TB
  %% classes
  TEAM["team.git<br>팀 원격 저장소<br>bare, 작업 폴더 없음"]:::tool
  AUTH["author 폴더<br>작성자 Ch3 Student"]:::tool
  REV["reviewer 폴더<br>리뷰어 Ch3 Reviewer"]:::tool
  TEAM -- "git clone<br>git fetch" --> AUTH
  AUTH -- "git push<br>feature/order-summary" --> TEAM
  TEAM -- "git clone<br>git fetch" --> REV
  REV -- "git push<br>origin main" --> TEAM
```

- 설명 대상 문장: 작성자와 리뷰어는 각자 원격 저장소를 복제해 자기 폴더에서 일합니다. 두 사람은 서로 직접 주고받지 않고, 늘 원격 저장소를 거칩니다.
- 캡션: 세 저장소가 커밋을 주고받는 길. 작성자와 리뷰어는 가운데 원격 저장소를 거쳐서만 커밋을 주고받습니다.
- 읽는 법: 위 가운데 team.git(원격, bare), 아래 왼쪽 author(Ch3 Student), 아래 오른쪽 reviewer(Ch3 Reviewer). 세 상자 모두 저장소라 초록. 아래로 가는 화살표는 받아 오기(`git clone`, `git fetch`), 위로 가는 화살표는 올리기(`git push` feature/order-summary, `git push origin main`). 노트북 코드 4·9·12·18·21·22 셀의 명령과 같습니다. 작성자 쪽 화살표에도 코드 22의 `git fetch`를 적었습니다.
- alt: 위 가운데 원격 저장소 team.git에서 아래 왼쪽 작성자 폴더와 아래 오른쪽 리뷰어 폴더로 clone과 fetch 화살표가 내려가고, 두 폴더에서 push 화살표가 올라가는 흐름도

### 02-2-브랜치-두-줄기.mmd

```mermaid
flowchart TB
  %% classes
  M["main<br>짝 origin/main"]
  F["* feature/order-summary<br>짝 origin/<br>feature/order-summary"]
  subgraph HIST["작성자 저장소 · git branch -vv"]
    direction LR
    C1["chore: 저장소와<br>PR 템플릿 시작"]:::tool
    C2["feat: 주문 요약<br>함수 추가"]:::tool
    C1 --> C2
  end
  M -. "가리킴" .-> C1
  F -. "가리킴" .-> C2
```

- 설명 대상 문장: 새 커밋을 만들면 지금 있는 브랜치의 이름만 그 커밋으로 옮겨 갑니다.
- 캡션: 기능 브랜치를 원격에 올린 뒤의 브랜치 이름. 새 커밋으로 옮겨 간 이름은 지금 있는 기능 브랜치뿐입니다.
- 읽는 법: 테두리 칸 안 초록 상자 두 개가 커밋(위가 먼저). 회색 상자는 브랜치 이름, 점선은 가리키는 커밋. 노트북 코드 8 `git branch -v`의 `* feature/order-summary … feat: 주문 요약 함수 추가`, `main … chore: 저장소와 PR 템플릿 시작`과 코드 9 `push -u` 뒤 `git branch -vv`의 `[origin/feature/order-summary]`·`[origin/main]`을 옮겼습니다.
- alt: 작성자 저장소 칸 안에 chore 커밋에서 feat 커밋으로 이어지는 초록 상자 두 개가 있고, 회색 main 이름은 chore 커밋을, 회색 feature/order-summary 이름은 feat 커밋을 점선으로 가리키는 그림

### 02-3-주고받는-순서.mmd

```mermaid
%%{init: {"sequence": {"messageAlign": "left"}}}%%
sequenceDiagram
  participant A as 작성자 author
  participant T as 원격 team.git
  participant R as 리뷰어 reviewer
  A->>T: push -u origin feature/order-summary
  R->>T: clone, switch 기능 브랜치
  T-->>R: summary.py 받음
  Note over R: Before<br>확인 파일 실행<br>리뷰 의견 남김
  A->>T: push (fix 커밋)
  R->>T: fetch
  T-->>R: fix 커밋 받음 (behind 1)
  Note over R: switch main<br>merge --no-ff<br>After 확인 파일 실행
  R->>T: push origin main (ahead 3)
  A->>T: fetch
  T-->>A: origin/main = merge: 주문 요약
```

- 설명 대상 문장: 리뷰어는 병합 결과를 확인한 뒤에 main을 올렸습니다.
- 캡션: 리뷰에서 병합까지 실제 순서. 리뷰어는 병합한 main을 확인한 뒤에 원격에 올렸습니다.
- 읽는 법: 위에서 아래로 시간 순서. 세로줄은 왼쪽부터 작성자·원격·리뷰어. 노란 메모는 리뷰어 저장소에서 확인 파일을 실행한 시점(Before는 기능 브랜치, After는 병합 뒤 main). 실선은 요청한 명령, 점선은 받아 온 결과(04-2·05-3·06-2와 같은 규칙). 라벨은 왼쪽 정렬로 세로선과 겹치지 않게 했고, 그림 폭을 줄이려고 리뷰어 화살표의 브랜치 이름 feature/order-summary는 「기능 브랜치」로 적었습니다. 화살표 라벨의 `behind 1`, `ahead 3`, `merge: 주문 요약`은 노트북 코드 18·21·22 셀 출력입니다.
- alt: 작성자, 원격 team.git, 리뷰어 세로줄 사이로 push, clone, fetch 화살표가 위에서 아래로 이어지고, 리뷰어 줄에 확인 파일 실행 메모 두 개가 있는 순서도

### 02-4-확인-결과-비교.mmd

```mermaid
flowchart TB
  %% classes
  subgraph BEFORE["Before · 기능 브랜치의 첫 함수"]
    direction LR
    b1["summary.py<br>글에 count를 그대로 넣음"]:::tool
    b2["확인 파일 실행<br>보통 값 3, 빈 글자"]:::flow
    b3["빈 값: 주문 건<br>오류 없이 틀린 글"]:::fail
    b1 --> b2 --> b3
  end
  subgraph AFTER["After · 병합한 main"]
    direction LR
    a1["summary.py<br>number = int(count)"]:::tool
    a2["같은 확인 파일 실행<br>보통 값 3, 빈 글자"]:::flow
    a3["입력 오류: invalid literal<br>for int() with base 10"]:::measure
    a1 --> a2 --> a3
  end
  BEFORE -- "fix 커밋, fetch, merge --no-ff" --> AFTER
```

- 설명 대상 문장: 기능 브랜치에서 실행한 확인 파일은 오류 없이 `빈 값: 주문 건`을 출력했습니다. 병합한 main에서는 같은 확인 파일이 입력 오류를 출력했습니다.
- 캡션: 같은 확인 파일의 결과. 기능 브랜치의 첫 함수는 틀린 글을 조용히 만들었고, 병합한 main의 함수는 오류를 드러냈습니다.
- 읽는 법: 위 칸 Before, 아래 칸 After, 칸마다 왼쪽에서 오른쪽. 초록은 함수 파일, 파랑은 실행한 확인. Before 끝 빨강 `빈 값: 주문 건`(오류 없이 나온 틀린 결과 = Before 결함), After 끝 노랑 `입력 오류: invalid literal for int() with base 10: ''`(확인 파일의 except가 받아 출력한 오류, 규격 §5-3). 보통 값은 두 번 모두 `보통 값 3: 주문 3건`.
- alt: Before 칸은 summary.py, 확인 파일 실행, 빨간 빈 값 주문 건 결과로 이어지고, After 칸은 int(count)로 고친 summary.py, 같은 확인 파일 실행, 노란 입력 오류 결과로 이어지는 비교 그림

### 02-5-병합-이력.mmd

```mermaid
flowchart BT
  %% classes
  C1["chore: 저장소와<br>PR 템플릿 시작"]:::tool
  C2["feat: 주문 요약<br>함수 추가"]:::tool
  C3["fix: 빈 주문 건수<br>입력 확인"]:::tool
  C4["merge: 주문 요약<br>부모 커밋 둘"]:::tool
  M["main · origin/main"]
  C1 -- "main 줄기" --> C4
  C1 -- "기능 브랜치 줄기" --> C2
  C2 --> C3
  C3 --> C4
  M -. "가리킴" .-> C4
```

- 설명 대상 문장: 리뷰어는 `git fetch` 뒤 main에 병합하고, 확인한 다음 원격까지 올립니다.
- 캡션: 병합 뒤의 이력. 병합 커밋 merge: 주문 요약은 부모 커밋이 둘이고, main과 origin/main이 함께 가리킵니다.
- 읽는 법: 아래에서 위로. 노트북 코드 21 셀 `git log --oneline --graph` 출력과 같은 모양으로, 오른쪽 기능 브랜치 줄기에 feat·fix 커밋, 왼쪽 main 줄기는 첫 커밋에서 병합 커밋으로 바로 이어집니다. 회색 상자는 올린 뒤 `[origin/main]` 짝 표시.
- alt: 아래 chore 커밋에서 왼쪽 main 줄기는 바로 위 merge 커밋으로, 오른쪽 기능 브랜치 줄기는 feat와 fix 커밋을 거쳐 merge 커밋으로 이어지고, 회색 main 이름이 merge 커밋을 가리키는 그림

### 02-6-검수대와-선반.prompt.md

# 삽화 — 02-6 검수대와 선반

- 상태: 2026-09-16 생성·검수 통과(1회 생성, 탈락 0). 모델 nano_banana_pro(서버 표기 nano_banana_2), 16:9, 2k(2752×1536), 2크레딧. job a99974d7-0e8b-4f89-820b-55eeabc3b5a5. 교재 파일은 폭 1100px로 줄여 저장.
- 검수 메모: 아래 줄 수레(파란 테이프 상자) → 화살표 → 검수대(돋보기로 열린 상자를 보는 사람, 상자를 든 사람) → 위로 꺾인 화살표 → 긴 선반 끝의 파란 상자 두 개 순서로 관계가 읽힘. 화면·글자 없음. 선반 위 갈색 상자 네 개와 파란 상자 두 개 사이에 빈칸이 있으나 같은 선반 위에 있어 「같은 줄에 합류」로 읽힘. 수레에도 파란 상자가 남아 있는 것처럼 보이는 것은 시간 순서의 앞 장면으로 읽음(01-5 택배 상자와 같은 한 장 연속 장면 구도).
- 설명 대상 문장: 긴 선반에는 확인을 마친 상자만 올립니다. 새 상자는 먼저 옆 수레에 싣습니다. 동료가 검수대에서 상자를 열어 돋보기로 확인한 뒤에야 선반 끝에 올립니다.
- 넣을 자리: 02절 핵심 개념 「비유로 시작하기」 단락 바로 아래
- 구성 요소와 배치: 위쪽 가로로 긴 선반(갈색 테이프 상자 줄). 아래 줄 왼쪽 → 오른쪽: ① 파란 테이프 상자 두 개를 실은 손수레 ② 탁자에서 돋보기로 열린 상자를 보는 사람 + 옆에서 상자를 든 사람 ③ 위로 꺾여 선반 끝을 가리키는 회색 화살표, 선반 끝의 파란 테이프 상자 두 개.
- 시선 순서: 수레 → 화살표 → 검수대 → 위로 꺾인 화살표 → 선반 끝
- 대응: 긴 선반 = main, 수레 = 기능 브랜치, 파란 상자 = 기능 브랜치의 커밋(feat·fix), 검수대 = PR 리뷰, 선반 끝에 올리기 = 병합. 01-5 택배 상자(봉한 상자 = 커밋)를 이어 씀.

## 프롬프트

Simple flat educational illustration, white background, limited soft palette, clean outlines, plain everyday objects, no text, no letters, no numbers, no logos.
A small storeroom scene read from left to right. Across the top of the image runs one long wooden shelf. On the left and middle part of this shelf sits a neat row of four identical cardboard boxes sealed with brown tape; the right end of the shelf is empty at first glance except for the two boxes described in zone 3.
Below the shelf, three zones in one row on a plain light floor, with a thin gray arrow between each zone:
(1) Left: a small hand cart on the floor carrying two cardboard boxes sealed with bright blue tape. The cart is clearly separate from the shelf.
(2) Middle: a plain table. One person holds a magnifying glass over one of the blue-taped boxes, which is opened on the table. A second person stands next to the table holding the other blue-taped box.
(3) Right: a thin gray arrow rises from the table up to the right end of the long shelf, where exactly two blue-taped boxes now sit at the end of the row of brown-taped boxes, joining the same row.
Only two people. No monitors, no screens, no computers, no signs, no labels with writing, no other shelves, no trucks, no conveyor belts.

