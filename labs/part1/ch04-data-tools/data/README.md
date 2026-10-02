# Ch 4 실습 데이터

모든 자료는 외부 서비스와 무관한 교육용 가상 데이터입니다. `customers.csv`와 `orders.csv`는 키와 조인을, `articles.json`은 로컬 REST 페이지네이션을, `article.html`과 `robots.txt`는 문서 파싱과 접근 정책 확인을 연습하는 데 사용합니다. 이름과 식별자는 실제 인물·주문·기사를 나타내지 않습니다.

01~04·06 노트북은 필요한 입력을 임시 폴더에 직접 만듭니다. 05 노트북은 이 폴더의 `article.html`·`robots.txt`를 읽고 `article-text.json`을 다시 씁니다. 이 폴더의 파일은 `data_tools.py`와 pytest가 재사용 함수의 파일 입력을 검증할 때도 사용합니다. `article-text.json`은 `article.html`에서 파싱한 ID·제목·요약·발행일과 모델 입력용 `text`를 담은 Ch 5 전달 파일입니다. pytest는 이 JSON이 현재 HTML을 다시 파싱한 결과와 같은지 확인합니다.
